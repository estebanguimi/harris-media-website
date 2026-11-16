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
