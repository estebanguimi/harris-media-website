"""Creates the admin panel's starting content from the current website.

Run once:  HMG_SEED=<content dir> python3 gen.py <any out dir>
"""
import json
import os
import re
from datetime import datetime
from html import escape

import richtext

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
PERSON_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500"><rect width="400" height="500" fill="#1A1A1A"/><circle cx="200" cy="190" r="80" fill="#333"/><path d="M60 500c0-90 63-150 140-150s140 60 140 150z" fill="#333"/></svg>'''


def iso(d):
    m, day, y = d.replace(',', '').split()
    return f'{int(y):04d}-{MONTHS.index(m) + 1:02d}-{int(day):02d}'


def vincent_bio(g):
    h = g['profile_body_vincent'](g['blocks'](g['raw']('meet-the-team__vincent-harris')))
    h = re.sub(r'<div class="panel quote-card"[^>]*><q>(.*?)</q><div class="meta"[^>]*>(.*?)</div></div>',
               r'<blockquote><p>\1</p><p>\2</p></blockquote>', h, flags=re.S)
    h = re.sub(r'<img ([^>]*)>', r'<figure><img \1></figure>', h)
    return richtext.clean(h)


def run(g):
    c = os.environ['HMG_SEED']
    os.makedirs(os.path.join(c, 'uploads'), exist_ok=True)

    team = []
    for i, m in enumerate(g['TEAM']):
        p = g['PROF'][m['slug']]
        langs = p['langs'] or ['English']
        bio = {}
        if m['slug'] == 'vincent-harris':
            bio['English'] = vincent_bio(g)
            portrait = g['UP'] + '2024/12/vnct-2.png'
        else:
            paras = [x for x in p['body'] if not x.startswith('[')]
            versions = g['split_langs'](paras, len(langs))
            for l, v in zip(langs if len(versions) > 1 else ['English'], versions):
                bio[l] = ''.join(f'<p>{escape(x)}</p>' for x in v)
            portrait = p['img'] or m['img']
        team.append(dict(slug=m['slug'], name=m['name'], title=m['title'], dept='auto', photo=m['img'], portrait=portrait,
                         langs=p['langs'], bio=bio, leader=i < 3, status='published', order=i + 1))

    import sn
    news = []
    for k, (s, cat, d, img) in enumerate(g['POSTS']):
        t, body, x = g['post_content'](s)
        f, kind, alt = sn.NEWS_IMG.get(s, ('', 'photo', ''))
        news.append(dict(slug=s, title=t, category=cat.title().replace('/ ', '/ '), date=iso(d), image=(sn.UPL + f) if f else (img or ''),
                         image_alt=alt, fit=kind, lead_tag='New office · Augusta, Maine' if k == 0 else '', excerpt=x, body=richtext.clean(body),
                         status='published'))

    works = []
    for i, (lab, cat) in enumerate(g['WORKS']):
        works.append(dict(id=f'w{i + 1:03d}', title=f'Project Title {i + 1:02d}', client='Client Name', year='2026', category=cat,
                          image=f'assets/works/work-{i + 1:02d}.webp', video='', video_url='', status='published', order=i + 1))

    stamp = datetime.now().isoformat(timespec='seconds')
    for name, data in (('team', team), ('news', news), ('works', works)):
        json.dump(data, open(os.path.join(c, name + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(dict(dirty=False, published_at=stamp), open(os.path.join(c, 'state.json'), 'w'), indent=1)
    print('seeded', len(team), 'people,', len(news), 'stories,', len(works), 'works')
