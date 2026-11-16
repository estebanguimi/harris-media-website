"""Four design versions each for OUR SERVICES and NEWS.

Same corporate HMG line (brand fonts, black/orange tokens, light theme support);
each version owns one experience:
  Services  V1 Index (sticky scroll index)   V2 Matrix (capability matrix)
            V3 Builder (program builder)     V4 Columns (expanding columns + drawn timeline)
  News      V1 Dispatch (broadsheet)         V2 Wire (newswire + live preview pane)
            V3 Spotlight (headline index + floating cover)   V4 Archive (searchable timeline)
"""
# Python 3.8+ compatibility: literals used inside f-strings
_Q1 = " class=\"on\" aria-current=\"page\""
import re
import html as H

e = lambda s: H.escape(str(s), quote=True)

SV_VER = [('services.html', 'INDEX'), ('services-v2.html', 'MATRIX'), ('services-v3.html', 'BUILDER'), ('services-v4.html', 'COLUMNS')]
NW_VER = [('blog.html', 'DISPATCH'), ('blog-v2.html', 'WIRE'), ('blog-v3.html', 'SPOTLIGHT'), ('blog-v4.html', 'ARCHIVE')]

STAGES = ['STRATEGY', 'CREATIVE', 'LAUNCH', 'OPTIMIZE']
# where each discipline typically works inside a program (illustrative)
STAGE_MAP = {
    'Advertising': 'SCLO', 'Web Design / Dev': 'CL', 'TV Production / Placement': 'CL', 'Social Media': 'SCLO',
    'Creative': 'C', 'SMS / Email': 'CLO', 'Strategic Consulting': 'S', 'AI': 'SCLO', 'Database Management': 'SO',
    'Video Production': 'C',
}
GOALS = [
    ('win', 'Win an election', ['Advertising', 'TV Production / Placement', 'Social Media', 'SMS / Email', 'Strategic Consulting', 'Video Production']),
    ('raise', 'Raise money', ['SMS / Email', 'Web Design / Dev', 'Database Management', 'Advertising']),
    ('opinion', 'Move public opinion', ['Advertising', 'Social Media', 'Creative', 'Strategic Consulting', 'Video Production']),
    ('policy', 'Pass or stop legislation', ['Strategic Consulting', 'Advertising', 'Web Design / Dev', 'Social Media']),
    ('launch', 'Launch a brand or cause', ['Creative', 'Web Design / Dev', 'Social Media', 'Video Production']),
    ('rapid', 'Respond fast', ['Creative', 'Social Media', 'SMS / Email', 'AI']),
]
STEPS = [('Strategy', 'We learn your race, your voters and your goals, then build the plan and the message.'),
         ('Creative', 'Our in-house designers, editors and writers produce everything — fast.'),
         ('Launch', 'Ads, sites, email and SMS go live across every channel at once.'),
         ('Optimize', 'Real-time reporting and A/B testing turn data into more votes and dollars.')]


def slug(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


def bar(vers, cur, label):
    links = ''.join(f'<a href="{h}"{_Q1 if i == cur else ""}><b>V{i + 1}</b><span>{n}</span></a>'
                    for i, (h, n) in enumerate(vers))
    return f'<nav class="snbar" aria-label="{label} design versions"><em>{label}</em>{links}</nav>'


def crumbs(name):
    return f'<div class="sn-crumbs"><a href="index.html">HOME</a><span>/</span><b>{name}</b></div>'


# ======================================================================
# SERVICES
# ======================================================================
def s_index(g):
    S = g['SERVICES']; I = g['ICONS']
    nav = ''.join(f'<li><a href="#{slug(n)}" data-spy="{slug(n)}"><i>{k + 1:02d}</i>{e(n)}</a></li>' for k, (n, *_) in enumerate(S))
    ch = ''.join(f'''<article class="ix-ch" id="{slug(n)}" data-spy-target>
  <div class="ix-num" aria-hidden="true">{k + 1:02d}</div>
  <div class="ix-top"><span class="ix-ico">{I[ic]}</span><span class="ix-tag">{t}</span></div>
  <h2>{e(n)}</h2><p>{e(d)}</p>
  <ul>{''.join(f'<li>{e(x)}</li>' for x in tags)}</ul>
  <a class="ix-go" href="contact.html?service={e(n)}">Start a {e(n)} project <span>→</span></a>
</article>''' for k, (n, t, ic, d, tags) in enumerate(S))
    steps = ''.join(f'<li data-reveal><b>{k + 1:02d}</b><h3>{a}</h3><p>{b}</p></li>' for k, (a, b) in enumerate(STEPS))
    return f'''<section class="ix-hero">
  <div class="wrap">{crumbs('OUR SERVICES')}
    <p class="sn-k">Capabilities &amp; footprint</p>
    <h1 class="ix-h1"><span>Ten disciplines.</span><span>One team.</span></h1>
    <div class="ix-intro"><p>HM GROUP is the leading digital firm for conservative political marketing and creative strategy. Strategy, advertising and creative for award-winning advocacy initiatives and campaigns — all in-house.</p>
    <a class="btn btn-primary" href="#ix-body">READ THE INDEX <span class="arr">↓</span></a></div>
  </div>
</section>
<section class="ix-body" id="ix-body"><div class="wrap ix-grid">
  <aside class="ix-nav"><p class="sn-k">Index</p><ol>{nav}</ol><div class="ix-prog"><i></i></div></aside>
  <div class="ix-chs">{ch}</div>
</div></section>
<section class="ix-steps"><div class="wrap"><p class="sn-k">How we win</p><h2 class="sn-h2">From brief to ballot.</h2><ol>{steps}</ol></div></section>'''


def s_matrix(g):
    S = g['SERVICES']; I = g['ICONS']
    head = ''.join(f'<th scope="col" data-col="{k}"><span>{k + 1:02d}</span>{s}</th>' for k, s in enumerate(STAGES))
    rows = ''
    for k, (n, t, ic, d, tags) in enumerate(S):
        m = STAGE_MAP[n]
        cells = ''.join(f'<td data-col="{j}">' + ('<i class="on" aria-label="yes"></i>' if s[0] in m else '<i aria-label="no"></i>') + '</td>' for j, s in enumerate(STAGES))
        rows += f'''<tr class="mx-row" tabindex="0" aria-expanded="false"><th scope="row"><span class="mx-ico">{I[ic]}</span><span class="mx-n">{e(n)}</span><span class="mx-t">{t}</span></th>{cells}<td class="mx-pl" aria-hidden="true">+</td></tr>
<tr class="mx-det"><td colspan="6"><div class="mx-in"><p>{e(d)}</p><ul>{''.join(f'<li>{e(x)}</li>' for x in tags)}</ul><a href="contact.html?service={e(n)}">Request this →</a></div></td></tr>'''
    tiles = ''.join(f'<span style="--k:{k}">{I[ic]}</span>' for k, (n, t, ic, *_) in enumerate(S))
    spec = ''.join(f'<div class="mx-spec-r" data-reveal><span>{k + 1:02d}</span><b>{e(a)}</b><em>{e(b)}</em></div>' for k, (a, b) in enumerate(g['DELIVER']))
    return f'''<section class="mx-hero"><div class="wrap mx-hero-g">
  <div>{crumbs('OUR SERVICES')}<p class="sn-k">Capability matrix</p>
    <h1 class="mx-h1">Every discipline.<br><span>Every stage.</span></h1>
    <p class="sn-lede">One firm covers the whole program — from the first strategy memo to the last optimization. Read across to see where each discipline works.</p></div>
  <div class="mx-tiles" aria-hidden="true">{tiles}</div>
</div></section>
<section class="mx-sec"><div class="wrap">
  <div class="mx-cap"><p class="sn-k">The matrix</p><p class="mx-note">Typical involvement by stage · every program is custom · click a row for detail</p></div>
  <div class="mx-scroll"><table class="mx"><thead><tr><th scope="col" class="mx-c0">Discipline</th>{head}<th></th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>
<section class="mx-spec"><div class="wrap"><p class="sn-k">Spec sheet</p><h2 class="sn-h2">What you get.</h2><div class="mx-spec-l">{spec}</div></div></section>'''


def s_builder(g):
    S = g['SERVICES']; I = g['ICONS']
    goals = ''.join(f'<button type="button" class="bd-goal" data-goal="{k}" aria-pressed="false" data-svcs="{"|".join(v)}">{t}</button>' for k, t, v in GOALS)
    cards = ''.join(f'''<button type="button" class="bd-card" data-svc="{e(n)}" aria-pressed="false">
  <span class="bd-ico">{I[ic]}</span><span class="bd-n">{e(n)}</span><span class="bd-d">{e(d)}</span><span class="bd-chk" aria-hidden="true"></span>
</button>''' for n, t, ic, d, tags in S)
    steps = ''.join(f'<div class="bd-step" data-reveal><span>Phase {k + 1}</span><h3>{a}</h3><p>{b}</p></div>' for k, (a, b) in enumerate(STEPS))
    return f'''<section class="bd-hero"><div class="wrap">{crumbs('OUR SERVICES')}
  <p class="sn-k">Program builder</p>
  <h1 class="bd-h1">Build your program.</h1>
  <p class="sn-lede">Tell us what you need to accomplish. We'll suggest the disciplines most programs like yours start with — then send it to our team as a brief.</p>
</div></section>
<section class="bd-sec"><div class="wrap bd-g">
  <div>
    <div class="bd-q"><span class="bd-qn">01</span><h2>What's the goal?</h2></div>
    <div class="bd-goals" role="group" aria-label="Goals">{goals}</div>
    <div class="bd-q"><span class="bd-qn">02</span><h2>Pick the disciplines.</h2></div>
    <p class="bd-hint">Suggested starting point — every program is custom. Tap any discipline to add or remove it.</p>
    <div class="bd-cards">{cards}</div>
  </div>
  <aside class="bd-sum" aria-live="polite">
    <div class="bd-sum-h"><span>Your brief</span><b id="bd-count">00</b></div>
    <ol id="bd-list"><li class="bd-empty">Choose a goal or a discipline to start.</li></ol>
    <a class="btn btn-primary bd-send" id="bd-send" href="contact.html">SEND THIS BRIEF <span class="arr">→</span></a>
    <button type="button" class="bd-reset" id="bd-reset">Clear</button>
  </aside>
</div></section>
<section class="bd-steps"><div class="wrap"><p class="sn-k">After you send it</p><h2 class="sn-h2">What happens next.</h2><div class="bd-steps-g">{steps}</div></div></section>'''


def s_columns(g):
    S = g['SERVICES']; I = g['ICONS']
    cols = ''.join(f'''<article class="cl-s{" on" if k == 0 else ""}" tabindex="0" aria-label="{e(n)}">
  <div class="cl-big" aria-hidden="true">{k + 1:02d}</div><div class="cl-spine"><b>{k + 1:02d}</b><span>{e(n)}</span></div>
  <div class="cl-open"><span class="cl-ico">{I[ic]}</span><span class="cl-t">{t}</span><h2>{e(n)}</h2><p>{e(d)}</p>
    <ul>{''.join(f'<li>{e(x)}</li>' for x in tags)}</ul><a href="contact.html?service={e(n)}">Start a project →</a></div>
</article>''' for k, (n, t, ic, d, tags) in enumerate(S))
    stats = ''.join(f'<div class="cl-st"><b><span data-count="{v}" data-suffix="{s}">0{s}</span></b><span>{e(k)}</span></div>' for v, s, k in g['STATS'])
    tl = ''.join(f'<li class="cl-tl-i"><span class="cl-dot"></span><b>{k + 1:02d} — {a}</b><p>{b}</p></li>' for k, (a, b) in enumerate(STEPS))
    return f'''<section class="cl-hero"><div class="wrap">{crumbs('OUR SERVICES')}
  <div class="cl-hero-g"><h1 class="cl-h1">What we do</h1><p class="sn-lede">Strategy, advertising and creative for Center-Right causes — ten disciplines, one in-house team. Open any column.</p></div>
</div></section>
<section class="cl-sec"><div class="cl-wrap">{cols}</div></section>
<section class="cl-stats"><div class="wrap cl-st-g">{stats}</div></section>
<section class="cl-tl-s"><div class="wrap cl-tl-g"><div><p class="sn-k">Process</p><h2 class="sn-h2">How a program runs.</h2></div><ol class="cl-tl" data-draw>{tl}</ol></div></section>'''


# ======================================================================
# NEWS
# ======================================================================
def posts(g):
    out = []
    meta = g.get('NEWS_META') or {}
    for s_, c, d, img in g['POSTS']:
        t, _, x = g['post_content'](s_)
        m = meta.get(s_)
        if m is None:
            f, kind, alt = NEWS_IMG.get(s_, ('', 'photo', ''))
            m = dict(img=(UPL + f) if f else (img or ''), kind=kind, alt=alt, tag='New office · Augusta, Maine' if s_.startswith('hmg-expands') else '')
        out.append(dict(s=s_, c=c, d=d, img=img, t=t, x=x, href=f'blog-{s_}.html', y=d.split()[-1], m=d.split()[0], meta=m))
    return out


def art(p, cls='sn-art'):
    if p['img']:
        return f'<img class="{cls}" src="{e(p["img"])}" alt="" loading="lazy">'
    words = p['t'].split(',')[0].split()[:5]
    return f'<div class="{cls} sn-art-t" aria-hidden="true"><span>{e(p["c"])}</span><b>{e(" ".join(words))}</b></div>'


UPL = 'https://www.harrismediallc.com/wp-content/uploads/'
# one HMG image per story (from the firm's own uploads)
NEWS_IMG = {
    'hmg-expands-to-new-england-welcomes-representative-reagan-paul-to-lead-regional-growth': ('2024/12/MEGOP.png', 'logo', 'The Maine Republican Party'),
    'floridas-premier-marketing-and-digital-advertising-solutions': ('2024/12/SOS-america.png', 'shot', 'SOS America PAC website for Mayor Francis Suarez'),
    'innovative-israeli-and-jewish-advocacy-campaigns': ('2024/12/Netanyahu.jpg', 'photo', 'Prime Minister Benjamin Netanyahu'),
    'conservative-political-marketing-agency': ('2025/01/preview-image-1024x512.png', 'photo', 'Harris Media Group and its clients'),
    'global-reach-and-international-campaign-services': ('2024/12/Frame-4.png', 'photo', 'Campaign planning'),
}
STUDIO = [('2024/12/Frame-3.png', 'Ask AI Suarez', 'AI'), ('2024/12/Frame-2.png', 'Spanish-language social for Francis Suarez', 'Social media'),
          ('2024/12/Frame-1.png', 'Energy advocacy reels', 'Video'), ('2024/12/SA-PAC.png', 'SOS America PAC identity', 'Creative')]


def pic(p, cls):
    m = p['meta']
    if not m.get('img'):
        return f'<figure class="{cls} pic-none"><span>{e(p["c"])}</span></figure>'
    return f'<figure class="{cls} pic-{m.get("kind") or "photo"}"><img src="{e(m["img"])}" alt="{e(m.get("alt") or p["t"])}" loading="lazy"></figure>'


def n_dispatch(g):
    P = posts(g)
    if not P:
        return f'<section class="dp-s"><div class="wrap">{crumbs("NEWS")}<header class="dp-mast"><h1>The HMG Dispatch</h1></header><p class="sn-lede" style="padding:60px 0">New stories coming soon.</p></div></section>'
    lead, rest = P[0], P[1:]
    cards = ''.join(f'''<article class="dp-card" data-reveal><a class="dp-card-img" href="{p['href']}" tabindex="-1" aria-hidden="true">{pic(p, 'dp-fig')}</a>
<div class="dp-card-b"><div class="dp-meta"><span class="dp-kick">{e(p['c'].title())}</span><span class="dp-date">{e(p['d'])}</span></div>
<h3><a href="{p['href']}">{e(p['t'])}</a></h3><p>{e(p['x'][:190])}…</p><a class="dp-more" href="{p['href']}">Continue reading →</a></div></article>''' for p in rest)
    brief = ''.join(f'<li><a href="{p["href"]}"><b>{e(p["c"].title())}</b>{e(p["t"])}</a></li>' for p in P)
    studio = ''.join(f'<a class="dp-st" href="our-works.html" data-reveal><figure><img src="{UPL}{f}" alt="{e(c)}" loading="lazy"></figure><span>{e(t)}</span><b>{e(c)}</b></a>' for f, c, t in STUDIO)
    return f'''<section class="dp-s"><div class="wrap">
  <div class="dp-top">{crumbs('NEWS')}<span>Austin · Miami · New England</span></div>
  <header class="dp-mast"><p class="dp-ed">Harris Media Group · Newsroom</p><h1>The HMG Dispatch</h1>
    <div class="dp-line"><span>Vol. 16</span><span>Press releases &amp; perspectives</span><span>{len(P)} stories</span></div></header>

  <div class="dp-lead">
    <article class="dp-main" data-reveal>
      <a class="dp-lead-img" href="{lead['href']}" tabindex="-1" aria-hidden="true">{pic(lead, 'dp-fig dp-fig-lead')}{f'<span class="dp-tag">{e(lead["meta"]["tag"])}</span>' if lead["meta"].get("tag") else ''}</a>
      <div class="dp-meta"><span class="dp-kick">{e(lead['c'].title())}</span><span class="dp-date">{e(lead['d'])}</span></div>
      <h2><a href="{lead['href']}">{e(lead['t'])}</a></h2>
      <div class="dp-body"><p>{e(lead['x'])}</p></div>
      <a class="btn btn-primary" href="{lead['href']}">READ THE RELEASE <span class="arr">→</span></a></article>
    <aside class="dp-side"><p class="dp-side-h">In this edition</p><ol>{brief}</ol>
      <div class="dp-side-box"><b>Media contact</b><p>Press inquiries go to the HMG team.</p><a href="contact.html">Contact us →</a></div></aside>
  </div>

  <div class="dp-sec-h"><h2>More stories</h2><span>{len(rest)} articles</span></div>
  <div class="dp-cards">{cards}</div>

  <div class="dp-sec-h"><h2>From the studio</h2><a href="our-works.html">See our works →</a></div>
  <div class="dp-studio">{studio}</div>
</div></section>'''


def n_wire(g):
    P = posts(g)
    cats = list(dict.fromkeys(p['c'] for p in P))
    tabs = '<button type="button" class="on" data-w="all">ALL <i>%d</i></button>' % len(P) + ''.join(
        f'<button type="button" data-w="{slug(c)}">{e(c)} <i>{sum(p["c"] == c for p in P)}</i></button>' for c in cats)
    rows = ''.join(f'''<a class="wr-row{" on" if k == 0 else ""}" href="{p['href']}" data-w="{slug(p['c'])}" data-t="{e(p['t'])}" data-c="{e(p['c'])}" data-d="{e(p['d'])}" data-x="{e(p['x'][:320])}…">
  <span class="wr-id">HMG-{len(P) - k:03d}</span><span class="wr-d">{e(p['d'].upper())}</span><span class="wr-c">{e(p['c'])}</span><b>{e(p['t'])}</b><span class="wr-go" aria-hidden="true">→</span></a>''' for k, p in enumerate(P))
    p = P[0]
    return f'''<section class="wr-s"><div class="wrap">
  {crumbs('NEWS')}
  <div class="wr-head"><div><p class="sn-k">HMG Newswire</p><h1 class="wr-h1">On the wire.</h1></div>
    <div class="wr-clock"><span class="wr-live"><i></i>LIVE DESK</span><b id="wr-time">--:--:--</b><span>AUSTIN, TX · CT</span></div></div>
  <div class="wr-tabs" role="group" aria-label="Filter by desk">{tabs}</div>
  <div class="wr-g">
    <div class="wr-list" id="wr-list">{rows}</div>
    <aside class="wr-prev" aria-live="polite"><div class="wr-prev-h"><span>Preview</span><span id="wr-pc">{e(p['c'])}</span></div>
      <h2 id="wr-pt">{e(p['t'])}</h2><p class="wr-pd" id="wr-pd">{e(p['d'])}</p><p id="wr-px">{e(p['x'][:320])}…</p>
      <a class="btn btn-primary" id="wr-pa" href="{p['href']}">OPEN STORY <span class="arr">→</span></a></aside>
  </div>
</div></section>'''


def n_spotlight(g):
    P = posts(g)
    rows = ''.join(f'''<li><a class="sp-row" href="{p['href']}" data-k="{k}">
  <span class="sp-i">{k + 1:02d}</span><span class="sp-t">{e(p['t'])}</span><span class="sp-m">{e(p['c'])}<br>{e(p['d'])}</span>
  <span class="sp-mob">{art(p, 'sp-mob-art')}</span></a></li>''' for k, p in enumerate(P))
    floats = ''.join(f'<div class="sp-card" data-k="{k}">{art(p)}</div>' for k, p in enumerate(P))
    return f'''<section class="sp-s"><div class="wrap">
  {crumbs('NEWS')}
  <div class="sp-head"><h1 class="sp-h1">News<span>&amp;</span>Insights</h1><p class="sn-lede">Press releases, expansion news and perspectives on conservative political marketing from the Harris Media Group team.</p></div>
  <ol class="sp-list">{rows}</ol>
</div><div class="sp-float" aria-hidden="true">{floats}</div></section>'''


def n_archive(g):
    P = posts(g)
    cats = list(dict.fromkeys(p['c'] for p in P))
    chips = '<button type="button" class="on" data-a="all">All</button>' + ''.join(f'<button type="button" data-a="{slug(c)}">{e(c.title())}</button>' for c in cats)
    items, last = '', None
    for p in P:
        key = f"{p['m']} {p['y']}"
        if key != last:
            items += f'<li class="ar-mark" data-mark>{e(key)}</li>'; last = key
        items += f'''<li class="ar-it" data-a="{slug(p['c'])}" data-q="{e((p['t'] + ' ' + p['x'] + ' ' + p['c']).lower())}">
  <span class="ar-dot"></span><a href="{p['href']}" class="ar-card">{art(p, 'ar-art')}<div><span class="ar-c">{e(p['c'])} · {e(p['d'])}</span><h3>{e(p['t'])}</h3><p>{e(p['x'][:200])}…</p></div></a></li>'''
    return f'''<section class="ar-s"><div class="wrap">
  {crumbs('NEWS')}
  <div class="ar-head"><div><p class="sn-k">The archive</p><h1 class="ar-h1">Every release, in order.</h1></div>
    <label class="ar-search"><span>Search</span><input id="ar-q" type="search" placeholder="Try “Florida”, “AI”, “New England”…" autocomplete="off"></label></div>
  <div class="ar-chips" role="group" aria-label="Filter by category">{chips}<span class="ar-n"><b id="ar-n">{len(P):02d}</b> results</span></div>
  <ol class="ar-tl" id="ar-tl"><li class="ar-line" aria-hidden="true"><i></i></li>{items}</ol>
  <p class="ar-none" id="ar-none" hidden>No stories match. Try another word.</p>
</div></section>'''


def build(g):
    extra = '<link rel="stylesheet" href="assets/sn.css"><link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;0,6..72,800;1,6..72,400&display=swap" rel="stylesheet"><script src="assets/sn.js" defer></script>'
    desc_s = 'Advertising, web, TV, social, creative, SMS/email, consulting, AI, database and video for conservative campaigns and causes.'
    # final picks: Services = Matrix, News = Dispatch
    g['page']('services.html', 'Our Services | Harris Media Group', desc_s, 'services', '<div class="sn sn-s2">' + s_matrix(g) + '</div>' + g['cta'](), extra=extra)
    g['page']('blog.html', 'News & Press | Harris Media Group', 'Press releases and insights from Harris Media Group.', 'blog', '<div class="sn sn-n1">' + n_dispatch(g) + '</div>' + g['cta'](), extra=extra)
