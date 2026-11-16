"""Harris Media Group — website admin panel.

Start with:  python app.py      (then open http://localhost:8000/admin)

Everything is stored in the `content/` folder (texts as .json + photos and videos in
`content/uploads/`). Pressing "Publish changes" rebuilds the whole website into
`site/`, which is what http://localhost:8000/ serves.
"""
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import threading
import time
import unicodedata
import uuid
from datetime import date, datetime
from functools import wraps

from flask import (Flask, abort, flash, jsonify, redirect, render_template, request, send_from_directory, session, url_for)
from PIL import Image, ImageOps
from werkzeug.security import check_password_hash, generate_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(BASE, 'generator')
def _folder(new, old):
    """English folder name; installs made before the translation keep their Spanish-named folder."""
    n, o = os.path.join(BASE, new), os.path.join(BASE, old)
    return o if os.path.isdir(o) and not os.path.isdir(n) else n


DATA = os.environ.get('HMG_DATA') or _folder('content', 'contenido')
PUBLIC = os.environ.get('HMG_PUBLIC') or os.path.join(BASE, 'site')
PREVIEW = os.path.join(BASE, 'preview')
UPLOADS = os.path.join(DATA, 'uploads')
sys.path.insert(0, GEN)
import richtext  # noqa: E402

def _python():
    """Interpreter used to run the site generator. Under some web hosts (uWSGI, PythonAnywhere)
    sys.executable is the server binary, not Python, so fall back to the environment's python."""
    if os.environ.get('HMG_PYTHON'):
        return os.environ['HMG_PYTHON']
    if os.path.basename(sys.executable or '').lower().startswith('python'):
        return sys.executable
    for c in (os.path.join(sys.prefix, 'bin', 'python3'), os.path.join(sys.prefix, 'Scripts', 'python.exe'), shutil.which('python3') or ''):
        if c and os.path.exists(c):
            return c
    return 'python3'


PYTHON = _python()
MAX_VIDEO_MB = 400
VIDEO_EXT = {'.mp4', '.webm', '.m4v'}
CATEGORIES = [('video', 'Video'), ('social', 'Social'), ('creative', 'Creative'), ('brand', 'Brand')]
DEPTS = [('auto', 'Automatic (based on the job title)'), ('leadership', 'Leadership'), ('accounts', 'Accounts'), ('creative', 'Creative & Web'), ('video', 'Video')]
LANGS = [('English', 'English'), ('Spanish', 'Spanish'), ('Portuguese', 'Portuguese')]
FITS = [('photo', 'Photo (fills the whole frame)'), ('logo', 'Logo (centered on a white background)'), ('shot', 'Screenshot (complete, not cropped)')]

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = (MAX_VIDEO_MB + 50) * 1024 * 1024
LOCK = threading.Lock()
BUILD_LOCK = threading.Lock()
FAILS = {}


# ======================================================================
# storage
# ======================================================================
def path(name):
    return os.path.join(DATA, name + '.json')


def load(name, default=None):
    try:
        with open(path(name), encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] if default is None else default


def save(name, data, dirty=True):
    with LOCK:
        tmp = path(name) + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        os.replace(tmp, path(name))
    if dirty:
        st = load('state', {})
        st['dirty'] = True
        save('state', st, dirty=False)


def slugify(t):
    t = unicodedata.normalize('NFKD', t or '').encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:80] or 'item'


def unique_slug(base, taken):
    s, n = base, 2
    while s in taken:
        s = f'{base}-{n}'; n += 1
    return s


def secret_key():
    p = os.path.join(DATA, '.session-key')
    old = os.path.join(DATA, '.clave-sesion')  # name used before the translation
    if os.path.exists(old) and not os.path.exists(p):
        os.replace(old, p)
    if not os.path.exists(p):
        os.makedirs(DATA, exist_ok=True)
        with open(p, 'w') as f:
            f.write(secrets.token_hex(32))
    return open(p).read().strip()


def save_image(fs, folder, max_side=2000):
    """Validates an uploaded image and stores it as WebP. Returns its site path or raises ValueError."""
    if not fs or not fs.filename:
        return None
    try:
        im = Image.open(fs.stream)
        im = ImageOps.exif_transpose(im)
        im.load()
    except Exception:
        raise ValueError('That file is not a valid image (use JPG, PNG or WebP).')
    if im.mode not in ('RGB', 'RGBA'):
        im = im.convert('RGBA' if 'A' in im.getbands() or im.mode == 'P' else 'RGB')
    im.thumbnail((max_side, max_side))
    name = f'{slugify(os.path.splitext(fs.filename)[0])[:40]}-{uuid.uuid4().hex[:8]}.webp'
    os.makedirs(os.path.join(UPLOADS, folder), exist_ok=True)
    im.save(os.path.join(UPLOADS, folder, name), 'WEBP', quality=86, method=4)
    return f'media/{folder}/{name}'


def save_video(fs, folder='works'):
    if not fs or not fs.filename:
        return None
    ext = os.path.splitext(fs.filename)[1].lower()
    if ext not in VIDEO_EXT:
        raise ValueError('The video must be MP4 or WebM. (If it is on YouTube, Vimeo, Facebook or Instagram, paste the link instead.)')
    name = f'{slugify(os.path.splitext(fs.filename)[0])[:40]}-{uuid.uuid4().hex[:8]}{ext}'
    os.makedirs(os.path.join(UPLOADS, folder), exist_ok=True)
    dest = os.path.join(UPLOADS, folder, name)
    fs.save(dest)
    if os.path.getsize(dest) > MAX_VIDEO_MB * 1024 * 1024:
        os.remove(dest)
        raise ValueError(f'The video is larger than {MAX_VIDEO_MB} MB. Upload it to YouTube, Vimeo or Facebook and paste the link.')
    return f'media/{folder}/{name}'


def remove_media(p):
    """Deletes an uploaded file that is no longer used (only inside uploads/)."""
    if p and p.startswith('media/') and '_sistema' not in p and '_system' not in p:
        full = os.path.realpath(os.path.join(UPLOADS, p[len('media/'):]))
        if full.startswith(os.path.realpath(UPLOADS) + os.sep) and os.path.isfile(full):
            os.remove(full)


# ======================================================================
# site build
# ======================================================================
def build(target, drafts=False):
    with BUILD_LOCK:
        tmp = target + '.nuevo'
        shutil.rmtree(tmp, ignore_errors=True)
        env = dict(os.environ, HMG_CONTENT=DATA, HMG_DRAFTS='1' if drafts else '0')
        r = subprocess.run([PYTHON, '-X', 'utf8', '-I', os.path.join(GEN, 'gen.py'), tmp], env=env, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
        if r.returncode != 0:
            shutil.rmtree(tmp, ignore_errors=True)
            app.logger.error(r.stderr)
            raise RuntimeError(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'unknown error')
        landing = os.path.join(GEN, 'landing')
        if not os.path.exists(os.path.join(tmp, 'index.html')):  # the generator builds the homepage with the panel's works
            shutil.copy(os.path.join(landing, 'index.html'), os.path.join(tmp, 'index.html'))
        if os.path.isdir(os.path.join(landing, 'videos')):
            shutil.copytree(os.path.join(landing, 'videos'), os.path.join(tmp, 'videos'), dirs_exist_ok=True)
        old = target + '.anterior'
        shutil.rmtree(old, ignore_errors=True)
        if os.path.isdir(target):
            os.replace(target, old)
        os.replace(tmp, target)
        shutil.rmtree(old, ignore_errors=True)


def publish():
    build(PUBLIC)
    st = load('state', {})
    st.update(dirty=False, published_at=datetime.now().isoformat(timespec='seconds'))
    save('state', st, dirty=False)


def first_run():
    os.makedirs(DATA, exist_ok=True)
    if not os.path.exists(path('team')):
        env = dict(os.environ, HMG_SEED=DATA)
        subprocess.run([PYTHON, '-X', 'utf8', '-I', os.path.join(GEN, 'gen.py'), os.path.join(BASE, '.seed')], env=env, check=True)
        shutil.rmtree(os.path.join(BASE, '.seed'), ignore_errors=True)
    if not os.path.isdir(PUBLIC):
        publish()


# ======================================================================
# auth + csrf
# ======================================================================
def users():
    if not os.path.exists(path('users')) and os.path.exists(path('usuarios')):  # name used before the translation
        os.replace(path('usuarios'), path('users'))
    return load('users', [])


def login_required(f):
    @wraps(f)
    def w(*a, **k):
        if not users():
            return redirect(url_for('setup'))
        if not session.get('user'):
            return redirect(url_for('login', next=request.path))
        return f(*a, **k)
    return w


@app.before_request
def csrf():
    if request.method == 'POST':
        tok = request.form.get('_csrf') or request.headers.get('X-CSRF')
        if not tok or tok != session.get('csrf'):
            abort(400, 'Your session expired. Go back and reload the page.')


@app.context_processor
def ctx():
    if 'csrf' not in session:
        session['csrf'] = secrets.token_hex(16)
    st = load('state', {}) if os.path.exists(path('state')) else {}
    return dict(csrf=session['csrf'], state=st, media=media_url, user=session.get('user'), nice_date=nice_date)


def media_url(p):
    if not p:
        return ''
    if p.startswith(('http://', 'https://')):
        return p
    return '/' + p.lstrip('/')


def nice_date(iso):
    try:
        return datetime.fromisoformat(iso).strftime('%d/%m/%Y')
    except Exception:
        return iso or ''


@app.route('/admin/setup', methods=['GET', 'POST'])
def setup():
    if users():
        return redirect(url_for('login'))
    if request.method == 'POST':
        u, p1, p2 = request.form.get('username', '').strip(), request.form.get('password', ''), request.form.get('password2', '')
        if not u or len(p1) < 8:
            flash('Enter a username and a password of at least 8 characters.', 'error')
        elif p1 != p2:
            flash('The passwords do not match.', 'error')
        else:
            save('users', [dict(user=u, hash=generate_password_hash(p1))], dirty=False)
            session['user'] = u
            flash('Done! Your account has been created.', 'ok')
            return redirect(url_for('dashboard'))
    return render_template('setup.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if not users():
        return redirect(url_for('setup'))
    if request.method == 'POST':
        ip = request.remote_addr or '?'
        recent = [t for t in FAILS.get(ip, []) if t > time.time() - 900]
        if len(recent) >= 10:
            flash('Too many attempts. Please wait 15 minutes.', 'error')
            return render_template('login.html'), 429
        u, p = request.form.get('username', '').strip(), request.form.get('password', '')
        acc = next((x for x in users() if x['user'].lower() == u.lower()), None)
        if acc and check_password_hash(acc['hash'], p):
            FAILS.pop(ip, None)
            session.clear()
            session['user'] = acc['user']
            nxt = request.args.get('next', '')
            return redirect(nxt if nxt.startswith('/admin') else url_for('dashboard'))
        FAILS[ip] = recent + [time.time()]
        time.sleep(1)
        flash('Wrong username or password.', 'error')
    return render_template('login.html')


@app.route('/admin/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/admin/account', methods=['GET', 'POST'])
@login_required
def account():
    us = users()
    if request.method == 'POST':
        act = request.form.get('action')
        if act == 'password':
            me = next(x for x in us if x['user'] == session['user'])
            if not check_password_hash(me['hash'], request.form.get('current', '')):
                flash('The current password is not correct.', 'error')
            elif len(request.form.get('new', '')) < 8:
                flash('The new password must be at least 8 characters long.', 'error')
            else:
                me['hash'] = generate_password_hash(request.form['new'])
                save('users', us, dirty=False)
                flash('Password changed.', 'ok')
        elif act == 'add':
            u, p = request.form.get('username', '').strip(), request.form.get('password', '')
            if not u or len(p) < 8:
                flash('Enter a username and a password of at least 8 characters.', 'error')
            elif any(x['user'].lower() == u.lower() for x in us):
                flash('That username already exists.', 'error')
            else:
                us.append(dict(user=u, hash=generate_password_hash(p)))
                save('users', us, dirty=False)
                flash(f'User "{u}" created.', 'ok')
        elif act == 'remove':
            u = request.form.get('username')
            if u == session['user']:
                flash('You cannot delete your own user.', 'error')
            else:
                save('users', [x for x in us if x['user'] != u], dirty=False)
                flash(f'User "{u}" removed.', 'ok')
        return redirect(url_for('account'))
    return render_template('account.html', users=us)


# ======================================================================
# dashboard + publish
# ======================================================================
@app.route('/admin')
@app.route('/admin/')
@login_required
def dashboard():
    w, n, t = load('works'), load('news'), load('team')
    count = lambda L: (sum(x.get('status') == 'published' for x in L), sum(x.get('status') != 'published' for x in L))
    latest = sorted(n, key=lambda x: x.get('date', ''), reverse=True)[:4]
    return render_template('dashboard.html', cw=count(w), cn=count(n), ct=count(t), latest=latest)


@app.route('/admin/publish', methods=['POST'])
@login_required
def do_publish():
    try:
        publish()
        flash('Website published! The changes are now live.', 'ok')
    except Exception as ex:
        flash(f'Could not publish: {ex}', 'error')
    return redirect(request.form.get('back') or url_for('dashboard'))


def preview_redirect(page):
    try:
        build(PREVIEW, drafts=True)
    except Exception as ex:
        flash(f'Could not create the preview: {ex}', 'error')
        return None
    return redirect(f'/preview/{page}')


@app.route('/preview/')
@app.route('/preview/<path:p>')
@login_required
def preview_files(p='index.html'):
    if not os.path.isdir(PREVIEW):
        return redirect(url_for('dashboard'))
    return send_from_directory(PREVIEW, p)


@app.route('/admin/upload-image', methods=['POST'])
@login_required
def upload_inline():
    try:
        p = save_image(request.files.get('file'), 'inline', 1600)
    except ValueError as ex:
        return jsonify(error=str(ex)), 400
    if not p:
        return jsonify(error='No image was received.'), 400
    return jsonify(url=p)


def move(items, key, val, direction):
    items.sort(key=lambda x: x.get('order', 0))
    i = next((k for k, x in enumerate(items) if x[key] == val), None)
    if i is None:
        abort(404)
    j = i - 1 if direction == 'up' else i + 1
    if 0 <= j < len(items):
        items[i], items[j] = items[j], items[i]
    for k, x in enumerate(items):
        x['order'] = k + 1
    return items


def after_save(page, back):
    if request.form.get('action') == 'preview':
        r = preview_redirect(page)
        if r:
            return r
    return redirect(back)


# ======================================================================
# OUR WORKS
# ======================================================================
def link_preview(url):
    """Official cover of a YouTube / Vimeo / Facebook / Instagram link, as shown on the website."""
    import content_mode
    from urllib.parse import quote
    emb, kind, plat = content_mode.embed_info(url)
    if not emb:
        return None
    label = {'youtube': 'YouTube', 'vimeo': 'Vimeo', 'facebook': 'Facebook', 'instagram': 'Instagram'}[plat]
    if plat == 'youtube':
        vid = re.search(r'/embed/([\w-]+)', emb).group(1)
        return dict(type='img', src=f'https://i.ytimg.com/vi/{vid}/hqdefault.jpg', plat=label, kind=kind)
    if plat == 'facebook':
        what = 'post' if kind == 'fbpost' else 'video'
        return dict(type='frame', src=f'https://www.facebook.com/plugins/{what}.php?href={quote(url.strip(), safe="")}&show_text=false&width=500',
                    plat=label, kind=kind)
    return dict(type='frame', src=emb, plat=label, kind=kind, ig=plat == 'instagram')


@app.context_processor
def preview_helper():
    return dict(link_preview=link_preview)


@app.route('/admin/works')
@login_required
def works_list():
    return render_template('works_list.html', items=sorted(load('works'), key=lambda x: x.get('order', 0)), cats=dict(CATEGORIES))


@app.route('/admin/works/new', methods=['GET', 'POST'])
@app.route('/admin/works/<wid>', methods=['GET', 'POST'])
@login_required
def work_edit(wid=None):
    items = load('works')
    w = next((x for x in items if x['id'] == wid), None) if wid else None
    if wid and not w:
        abort(404)
    if request.method == 'POST':
        f = request.form
        new = dict(w or {}, title=f.get('title', '').strip(), client=f.get('client', '').strip(), year=f.get('year', '').strip(),
                   category=f.get('category') if f.get('category') in dict(CATEGORIES) else 'creative',
                   video_url=f.get('video_url', '').strip(), status='published' if f.get('status') == 'published' else 'draft')
        try:
            img = save_image(request.files.get('image'), 'works')
            vid = save_video(request.files.get('video'))
        except ValueError as ex:
            flash(str(ex), 'error')
            return render_template('work_form.html', w=new, cats=CATEGORIES)
        if img:
            remove_media(new.get('image')); new['image'] = img
        if vid:
            remove_media(new.get('video')); new['video'] = vid; new['video_url'] = ''
        if f.get('remove_video'):
            remove_media(new.get('video')); new['video'] = ''; new['video_url'] = ''
        if new['video_url']:
            import content_mode
            if not content_mode.embed_url(new['video_url']):
                flash('That link is not recognized. Use a YouTube, Vimeo, Facebook or Instagram link (copied from the browser or from the "Share" button).', 'error')
                return render_template('work_form.html', w=new, cats=CATEGORIES)
        if not new['title'] or not (new.get('image') or new.get('video_url')):
            flash('The work needs a title and a cover image (or a video / post link).', 'error')
            return render_template('work_form.html', w=new, cats=CATEGORIES)
        if w:
            items[items.index(w)] = new
        else:
            new['id'] = 'w' + uuid.uuid4().hex[:8]
            new['order'] = 0
            for x in items:
                x['order'] = x.get('order', 0) + 1
            items.append(new)
        save('works', items)
        flash(f'"{new["title"]}" saved. Press "Publish changes" to make it live.', 'ok')
        return after_save('our-works.html', url_for('works_list'))
    return render_template('work_form.html', w=w or dict(status='published', category='video', year=str(date.today().year)), cats=CATEGORIES)


@app.route('/admin/works/<wid>/delete', methods=['POST'])
@login_required
def work_delete(wid):
    items = load('works')
    w = next((x for x in items if x['id'] == wid), None)
    if w:
        remove_media(w.get('image')); remove_media(w.get('video'))
        save('works', [x for x in items if x is not w])
        flash(f'"{w["title"]}" deleted.', 'ok')
    return redirect(url_for('works_list'))


@app.route('/admin/works/<wid>/<any(up,down):d>', methods=['POST'])
@login_required
def work_move(wid, d):
    save('works', move(load('works'), 'id', wid, d))
    return redirect(url_for('works_list') + '#' + wid)


# ======================================================================
# NEWS
# ======================================================================
@app.route('/admin/news')
@login_required
def news_list():
    return render_template('news_list.html', items=sorted(load('news'), key=lambda x: x.get('date', ''), reverse=True))


@app.route('/admin/news/new', methods=['GET', 'POST'])
@app.route('/admin/news/<slug>', methods=['GET', 'POST'])
@login_required
def news_edit(slug=None):
    items = load('news')
    n = next((x for x in items if x['slug'] == slug), None) if slug else None
    if slug and not n:
        abort(404)
    cats = sorted({x.get('category', '') for x in items if x.get('category')})
    if request.method == 'POST':
        f = request.form
        d = f.get('date') or date.today().isoformat()
        new = dict(n or {}, title=f.get('title', '').strip(), category=f.get('category', '').strip() or 'News', date=d,
                   fit=f.get('fit') if f.get('fit') in dict(FITS) else 'photo', image_alt=f.get('image_alt', '').strip(),
                   lead_tag=f.get('lead_tag', '').strip(), excerpt=f.get('excerpt', '').strip(), body=richtext.clean(f.get('body', '')),
                   status='published' if f.get('status') == 'published' else 'draft')
        try:
            img = save_image(request.files.get('image'), 'news')
        except ValueError as ex:
            flash(str(ex), 'error')
            return render_template('news_form.html', n=new, cats=cats, fits=FITS)
        if img:
            remove_media(new.get('image')); new['image'] = img
        if f.get('remove_image'):
            remove_media(new.get('image')); new['image'] = ''
        if not new['title'] or not richtext.text(new['body']):
            flash('The story needs a title and some text.', 'error')
            return render_template('news_form.html', n=new, cats=cats, fits=FITS)
        if n:
            items[items.index(n)] = new
        else:
            new['slug'] = unique_slug(slugify(new['title']), {x['slug'] for x in items})
            items.append(new)
        save('news', items)
        flash(f'"{new["title"]}" saved. Press "Publish changes" to make it live.', 'ok')
        return after_save(f'blog-{new["slug"]}.html', url_for('news_list'))
    return render_template('news_form.html', n=n or dict(status='published', date=date.today().isoformat(), fit='photo'), cats=cats, fits=FITS)


@app.route('/admin/news/<slug>/delete', methods=['POST'])
@login_required
def news_delete(slug):
    items = load('news')
    n = next((x for x in items if x['slug'] == slug), None)
    if n:
        remove_media(n.get('image'))
        save('news', [x for x in items if x is not n])
        flash(f'"{n["title"]}" deleted.', 'ok')
    return redirect(url_for('news_list'))


# ======================================================================
# TEAM
# ======================================================================
@app.route('/admin/team')
@login_required
def team_list():
    return render_template('team_list.html', items=sorted(load('team'), key=lambda x: x.get('order', 0)), depts=dict(DEPTS))


@app.route('/admin/team/new', methods=['GET', 'POST'])
@app.route('/admin/team/<slug>', methods=['GET', 'POST'])
@login_required
def team_edit(slug=None):
    items = load('team')
    m = next((x for x in items if x['slug'] == slug), None) if slug else None
    if slug and not m:
        abort(404)
    if request.method == 'POST':
        f = request.form
        new = dict(m or {}, name=f.get('name', '').strip(), title=f.get('title', '').strip(),
                   dept=f.get('dept') if f.get('dept') in dict(DEPTS) else 'auto',
                   langs=[l for l, _ in LANGS if f.get('lang_' + l)], leader=bool(f.get('leader')),
                   bio={l: richtext.clean(f.get('bio_' + l, '')) for l, _ in LANGS},
                   status='published' if f.get('status') == 'published' else 'draft')
        try:
            photo = save_image(request.files.get('photo'), 'team', 1400)
            portrait = save_image(request.files.get('portrait'), 'team', 1600)
        except ValueError as ex:
            flash(str(ex), 'error')
            return render_template('team_form.html', m=new, depts=DEPTS, langs=LANGS)
        if photo:
            if new.get('portrait') == new.get('photo'):
                new['portrait'] = photo
            remove_media(new.get('photo')); new['photo'] = photo
        if portrait:
            if new.get('portrait') != new.get('photo'):
                remove_media(new.get('portrait'))
            new['portrait'] = portrait
        if not new.get('portrait'):
            new['portrait'] = new.get('photo', '')
        if not new['name'] or not new['title']:
            flash('Enter at least the name and the job title.', 'error')
            return render_template('team_form.html', m=new, depts=DEPTS, langs=LANGS)
        if not new.get('photo'):
            flash('Upload a photo of the person.', 'error')
            return render_template('team_form.html', m=new, depts=DEPTS, langs=LANGS)
        if m:
            items[items.index(m)] = new
        else:
            new['slug'] = unique_slug(slugify(new['name']), {x['slug'] for x in items})
            new['order'] = max([x.get('order', 0) for x in items] or [0]) + 1
            items.append(new)
        save('team', items)
        flash(f'{new["name"]}\'s profile saved. Press "Publish changes" to make it live.', 'ok')
        return after_save(f'team-{new["slug"]}.html', url_for('team_list'))
    return render_template('team_form.html', m=m or dict(status='published', dept='auto', langs=['English'], bio={}), depts=DEPTS, langs=LANGS)


@app.route('/admin/team/<slug>/delete', methods=['POST'])
@login_required
def team_delete(slug):
    items = load('team')
    m = next((x for x in items if x['slug'] == slug), None)
    if m:
        remove_media(m.get('photo'))
        if m.get('portrait') != m.get('photo'):
            remove_media(m.get('portrait'))
        save('team', [x for x in items if x is not m])
        flash(f'{m["name"]}\'s profile deleted.', 'ok')
    return redirect(url_for('team_list'))


@app.route('/admin/team/<slug>/<any(up,down):d>', methods=['POST'])
@login_required
def team_move(slug, d):
    save('team', move(load('team'), 'slug', slug, d))
    return redirect(url_for('team_list') + '#' + slug)


# ======================================================================
# files
# ======================================================================
@app.route('/media/<path:p>')
def media_files(p):
    return send_from_directory(UPLOADS, p)


@app.route('/')
@app.route('/<path:p>')
def site(p='index.html'):
    if p.startswith('admin'):
        abort(404)
    full = os.path.join(PUBLIC, p)
    if os.path.isdir(full):
        p = p.rstrip('/') + '/index.html'
    return send_from_directory(PUBLIC, p)


@app.errorhandler(413)
def too_big(_):
    flash(f'The file is too large (maximum {MAX_VIDEO_MB} MB).', 'error')
    return redirect(request.referrer or url_for('dashboard'))


app.secret_key = secret_key()
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',
                  SESSION_COOKIE_SECURE=os.environ.get('HMG_HTTPS') == '1')

if __name__ == '__main__':
    first_run()
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '127.0.0.1')
    print(f'\n  Admin panel:  http://localhost:{port}/admin\n  Website:      http://localhost:{port}/\n  (Close this window to stop it)\n')
    if os.environ.get('HMG_OPEN') == '1':
        import webbrowser
        threading.Timer(1.5, webbrowser.open, [f'http://localhost:{port}/admin']).start()
    try:
        from waitress import serve
        serve(app, host=host, port=port, threads=8, max_request_body_size=app.config['MAX_CONTENT_LENGTH'])
    except ImportError:
        app.run(host=host, port=port)
