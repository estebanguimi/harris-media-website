"""Reads the admin panel's content (content/*.json) for the site generator."""
import json
import os
import re
import shutil

import richtext

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
LANG_ORDER = ['English', 'Spanish', 'Portuguese']
PLACEHOLDER = 'media/_sistema/persona.svg'


def load(c, name):
    try:
        return json.load(open(os.path.join(c, name + '.json'), encoding='utf-8'))
    except FileNotFoundError:
        return []


def visible(items, drafts):
    return [x for x in items if drafts or x.get('status') == 'published']


def nice_date(iso):
    try:
        y, m, d = (int(x) for x in iso.split('-'))
        return f'{MONTHS[m - 1]} {d}, {y}'
    except Exception:
        return iso or ''


def team(c, drafts):
    rows = sorted(visible(load(c, 'team'), drafts), key=lambda m: m.get('order', 0))
    TEAM, PROF, DEPT = [], {}, {}
    for m in rows:
        photo = m.get('photo') or m.get('portrait') or PLACEHOLDER
        TEAM.append(dict(slug=m['slug'], name=m['name'], title=m['title'], img=photo, leader=bool(m.get('leader'))))
        bio = {l: richtext.clean(m.get('bio', {}).get(l, '')) for l in LANG_ORDER}
        bio = {l: h for l, h in bio.items() if h}
        first = next(iter(bio.values()), '')
        PROF[m['slug']] = dict(img=m.get('portrait') or photo, langs=[l for l in LANG_ORDER if l in (m.get('langs') or [])],
                               body=richtext.paragraphs(first), bio=bio or {'English': ''})
        if m.get('dept') and m['dept'] != 'auto':
            DEPT[m['title']] = m['dept']
    leaders = [x for x in TEAM if x['leader']][:3] or TEAM[:3]
    return TEAM, PROF, DEPT, leaders


def news(c, drafts):
    rows = sorted(visible(load(c, 'news'), drafts), key=lambda n: n.get('date', ''), reverse=True)
    posts, data, meta = [], {}, {}
    for n in rows:
        body = richtext.clean(n.get('body', ''))
        excerpt = (n.get('excerpt') or '').strip() or richtext.text(body).replace('\n', ' ')[:320]
        posts.append((n['slug'], (n.get('category') or 'News').upper(), nice_date(n.get('date', '')), n.get('image') or None))
        data[n['slug']] = (n['title'], body, excerpt)
        meta[n['slug']] = dict(img=n.get('image') or '', kind=n.get('fit') or 'photo', alt=n.get('image_alt') or n['title'], tag=n.get('lead_tag') or '')
    return posts, (lambda slug: data[slug]), meta


def embed_info(u):
    """Turns a public link into the platform's official embedded player (official cover + plays in place).
    Returns (embed_url, kind, platform) or ('', '', ''). kind: 'video' (16:9), 'vertical' (9:16 reels/shorts),
    'post' (Instagram post or reel card) or 'fbpost' (Facebook post card)."""
    from urllib.parse import quote
    u = (u or '').strip()
    if not re.match(r'^https?://', u):
        return '', '', ''
    m = re.search(r'(?:youtube\.com/(?:watch\?v=|embed/|live/)|youtu\.be/)([\w-]{6,})', u)
    if m:
        return f'https://www.youtube-nocookie.com/embed/{m.group(1)}?rel=0&modestbranding=1&playsinline=1', 'video', 'youtube'
    m = re.search(r'youtube\.com/shorts/([\w-]{6,})', u)
    if m:
        return f'https://www.youtube-nocookie.com/embed/{m.group(1)}?rel=0&modestbranding=1&playsinline=1', 'vertical', 'youtube'
    m = re.search(r'vimeo\.com/(?:video/)?(\d+)', u)
    if m:
        return f'https://player.vimeo.com/video/{m.group(1)}?title=0&byline=0&portrait=0', 'video', 'vimeo'
    m = re.search(r'instagram\.com/(?:[\w.]+/)?(p|reel|reels|tv)/([\w-]+)', u)
    if m:
        kind = 'reel' if m.group(1) in ('reel', 'reels') else m.group(1)
        return f'https://www.instagram.com/{kind}/{m.group(2)}/embed/', 'post', 'instagram'
    if re.search(r'(?:facebook\.com|fb\.watch|fb\.com)', u):
        enc = quote(u, safe='')
        if re.search(r'facebook\.com/(?:reel/|share/r/)', u):
            return f'https://www.facebook.com/plugins/video.php?href={enc}&show_text=false', 'vertical', 'facebook'
        if re.search(r'fb\.watch/|facebook\.com/(?:watch|.*/videos/|video\.php|share/v/)', u):
            return f'https://www.facebook.com/plugins/video.php?href={enc}&show_text=false', 'video', 'facebook'
        return f'https://www.facebook.com/plugins/post.php?href={enc}&show_text=true', 'fbpost', 'facebook'
    return '', '', ''


def embed_url(u):
    return embed_info(u)[0]


def works(c, drafts):
    rows = sorted(visible(load(c, 'works'), drafts), key=lambda w: w.get('order', 0))
    out = []
    for w in rows:
        emb, kind, plat = embed_info(w.get('video_url'))
        out.append(dict(title=w.get('title') or 'Untitled', client=w.get('client', ''), year=w.get('year', ''), category=w.get('category') or 'creative',
                        image=w.get('image') or ('' if emb else PLACEHOLDER), video=w.get('video', ''), embed=emb, embed_kind=kind, platform=plat,
                        link=(w.get('video_url') or '').strip()))
    return out


def copy_media(c, out):
    src = os.path.join(c, 'uploads')
    if os.path.isdir(src):
        shutil.copytree(src, os.path.join(out, 'media'), dirs_exist_ok=True)


# ----------------------------------------------------------------------
# Homepage "OUR WORKS" gallery wall, rebuilt from the panel's works
# ----------------------------------------------------------------------
PLAY = '<span class="hw-play" aria-hidden="true"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>'


def _esc(s):
    import html
    return html.escape(str(s or ''), quote=True)


def _tile(n, w):
    """One gallery tile. Returns (html, is_wide)."""
    from urllib.parse import quote
    plat, kind, link = w.get('platform'), w.get('embed_kind'), w.get('link', '')
    label = (w.get('category') or 'work').upper()
    title = _esc(w.get('title'))
    head = f'<a class="hw-tile hw-{{k}}" href="our-works.html" tabindex="-1" aria-label="{title}">'
    tag = f'<span class="hw-tag">{n:02d} · {_esc(label)}</span></a>'
    if plat == 'youtube':
        vid = re.search(r'/embed/([\w-]+)', w['embed']).group(1)
        img = (f'<img class="hw-img hw-cover" src="https://i.ytimg.com/vi/{vid}/maxresdefault.jpg" alt="" loading="lazy" '
               f'onerror="this.onerror=null;this.src=\'https://i.ytimg.com/vi/{vid}/hqdefault.jpg\'">')
        return head.format(k='video') + img + PLAY + tag, True
    if plat == 'facebook':
        src = f'https://www.facebook.com/plugins/video.php?href={quote(link, safe="")}&show_text=false&width=420'
        if kind == 'fbpost':
            src = f'https://www.facebook.com/plugins/post.php?href={quote(link, safe="")}&show_text=false&width=420'
        frame = f'<iframe class="hw-embed" src="{_esc(src)}" loading="lazy" scrolling="no" tabindex="-1" title="{title}"></iframe>'
        return head.format(k='video hw-social') + frame + tag, True
    if plat == 'instagram':
        frame = f'<span class="hw-igbox" data-igfit="cover"><iframe class="hw-embed hw-ig" data-ig src="{_esc(w["embed"])}" loading="lazy" scrolling="no" tabindex="-1" title="{title}"></iframe></span>'
        return head.format(k='image hw-social') + frame + tag, False
    if plat == 'vimeo':
        src = w['embed'] + '&background=1&muted=1'
        frame = f'<iframe class="hw-embed" src="{_esc(src)}" loading="lazy" tabindex="-1" title="{title}" allow="autoplay"></iframe>'
        return head.format(k='video hw-social') + frame + tag, True
    if w.get('video'):
        poster = f' poster="{_esc(w["image"])}"' if w.get('image') else ''
        media = (f'<img class="hw-img hw-cover" src="{_esc(w.get("image"))}" alt="" loading="lazy">' if w.get('image') else '') + \
                f'<video class="hw-vid" muted loop playsinline autoplay preload="metadata"{poster}><source src="{_esc(w["video"])}"></video>'
        return head.format(k='video') + media + PLAY + tag, True
    img = f'<img class="hw-img hw-cover" src="{_esc(w.get("image"))}" alt="" loading="lazy">'
    return head.format(k='image') + img + tag, False


IG_FIT_JS = '/* Instagram: show only the photo / video (hide Instagram\'s own header and footer) */\n(function () {\n  var TOP = 54, BOTTOM = 154;\n  function fit(f, H) {\n    var box = f.parentNode, m = H - TOP - BOTTOM;\n    if (m < 40) return;\n    if ((box.getAttribute("data-igfit") || "shape") === "shape") {\n      var W = box.clientWidth;\n      box.style.aspectRatio = W + " / " + m;\n      f.style.top = -TOP + "px"; f.style.height = H + "px";\n    } else {\n      var bw = box.clientWidth, bh = box.clientHeight, s = Math.max(bh / m, 1);\n      f.style.width = bw + "px"; f.style.height = H + "px"; f.style.transformOrigin = "0 0";\n      f.style.transform = "scale(" + s + ")"; f.style.left = (-(bw * s - bw) / 2) + "px"; f.style.top = (-TOP * s - (m * s - bh) / 2) + "px";\n    }\n    box.classList.add("ig-ready");\n  }\n  window.addEventListener("message", function (e) {\n    if (e.origin !== "https://www.instagram.com") return;\n    var d = e.data;\n    try { if (typeof d === "string") d = JSON.parse(d); } catch (x) { return; }\n    if (!d || d.type !== "MEASURE" || !d.details || !d.details.height) return;\n    var frames = document.querySelectorAll("iframe[data-ig]");\n    for (var k = 0; k < frames.length; k++) if (frames[k].contentWindow === e.source) fit(frames[k], d.details.height);\n  });\n})();\n'


HW_CSS = '''<style id="hw-panel-css">
#slide-works img.hw-cover{width:100%;height:100%;object-fit:cover;display:block}
#slide-works .hw-embed{position:absolute;left:0;top:0;width:100%;height:100%;border:0;pointer-events:none;background:#000}
#slide-works .hw-igbox{position:absolute;inset:0;overflow:hidden;background:#000}
#slide-works .hw-ig{height:calc(100% + 208px);top:-54px;background:#000}
#slide-works .hw-social::after{content:"";position:absolute;inset:0;z-index:1}
#slide-works .hw-social .hw-play,#slide-works .hw-social .hw-tag{z-index:2}
</style>'''


def landing(c, drafts, gen_dir, out):
    """Writes out/index.html: the built homepage with its gallery wall made from the panel's works."""
    s = open(os.path.join(gen_dir, 'landing', 'index.html'), encoding='utf-8').read()
    items = works(c, drafts)
    try:
        i0 = s.index('<div class="hw-wall my-auto">')
        r3 = s.index('<div class="hw-row hw-row-3">', i0)
        j = s.index('</div></div></div>', s.index('<div class="hw-set" aria-hidden="true">', r3)) + len('</div></div></div>')
        assert s[j:j + 6] == '</div>'
    except (ValueError, AssertionError):
        items = []
    if items:
        rows = ''
        k = 0
        for r in range(3):
            tiles = []
            for p in range(6):
                w = items[k % len(items)]
                tiles.append(_tile(k % len(items) + 1, w)[0])
                k += 1
            seq = ''.join(tiles) * (2 if len(items) > 2 else 3)
            rows += (f'<div class="hw-row hw-row-{r + 1}"><div class="hw-track">'
                     f'<div class="hw-set">{seq}</div><div class="hw-set" aria-hidden="true">{seq}</div></div></div>')
        s = s[:i0] + '<div class="hw-wall my-auto">' + rows + '</div>' + s[j + 6:]
        s = s.replace('</head>', HW_CSS + '</head>', 1)
        if 'data-ig ' in rows:
            s = s.replace('</body>', '<script>' + IG_FIT_JS + '</script></body>', 1)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(s)
