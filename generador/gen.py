#!/usr/bin/env python3
"""Generates every Harris Media Group subpage from the content of the current site."""
# Python 3.8+ compatibility: literals used inside f-strings
_Q1 = " class=\"is-current\" aria-current=\"page\""
_Q2 = " class=\"accent glow\""
_Q3 = " class=\"on\""
import json, os, re, sys, html as H, shutil, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blocks import blocks

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'site', 'raw')
OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, 'assets', 'works'), exist_ok=True)
for f in ('hmg.css', 'hmg.js', 'worlds.css', 'worlds.js', 'versions.css', 'versions.js', 'versions2.css', 'versions2.js', 'batch1.css', 'batch1.js', 'batch2.css', 'batch2.js', 'finals.css', 'finals.js', 'finals3.css', 'finals3.js', 'sn.css', 'sn.js'):
    shutil.copy(os.path.join(HERE, 'gen', 'assets', f), os.path.join(OUT, 'assets', f))
for i, f in enumerate(sorted(glob.glob(os.path.join(HERE, 'tiles', '*.webp')))):
    shutil.copy(f, os.path.join(OUT, 'assets', 'works', 'work-%02d.webp' % (i + 1)))

UP = 'https://www.harrismediallc.com/wp-content/uploads/'
PHONE = '512-900-9439'
EMAIL_HR = 'hr@harrismediallc.com'
EMAIL_CONTACT = 'contact@harrismediallc.com'
e = lambda s: H.escape(str(s), quote=True)
ARROW = '<span class="arr" aria-hidden="true">→</span>'


def raw(name):
    s = open(os.path.join(RAW, name + '.html'), encoding='utf-8').read()
    # decode Cloudflare-protected e-mails
    def dec(m):
        h = m.group(1); k = int(h[:2], 16)
        return ''.join(chr(int(h[i:i + 2], 16) ^ k) for i in range(2, len(h), 2))
    s = re.sub(r'<a[^>]*data-cfemail="([0-9a-f]+)"[^>]*>.*?</a>', dec, s)
    s = re.sub(r'<span[^>]*data-cfemail="([0-9a-f]+)"[^>]*>.*?</span>', dec, s)
    return s


def strip(t):
    return re.sub(r'<[^>]+>', '', t).strip()


def slugify(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


# ======================================================================
# SHELL
# ======================================================================
NAV = [('index.html', 'HOME', 'home'), ('clients.html', 'OUR CLIENTS', 'clients'), ('services.html', 'OUR SERVICES', 'services'),
       ('our-works.html', 'OUR WORKS', 'works'), ('team.html', 'OUR TEAM', 'team'), ('careers.html', 'CAREERS', 'careers'),
       ('blog.html', 'NEWS', 'blog')]


def head(title, desc, image=None):
    og = '<meta property="og:image" content="%s">' % e(image) if image else ''
    return f'''<!DOCTYPE html>
<html lang="en" class="dark no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
{og}
<meta name="theme-color" content="#0A0A0A">
<link rel="icon" href="{UP}2024/12/cropped-logo-ligth-270x270.png">
<!-- BRAND FONT: Adobe Fonts web project with Organetto Variable (replace XXXXXXX with your kit id) -->
<link rel="stylesheet" href="https://use.typekit.net/XXXXXXX.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Barlow+Semi+Condensed:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<script>try{{if(localStorage.getItem("hmg-theme")==="light")document.documentElement.classList.remove("dark")}}catch(e){{}}</script>
<link rel="stylesheet" href="assets/hmg.css">
</head>
<body>
'''


def header(current):
    links_extra = '<a class="nav-contact" href="contact.html">CONTACT →</a>'
    links = ''.join(
        f'<a href="{h}"{_Q1 if k == current else ""}>{t}</a>' for h, t, k in NAV)
    return f'''<header class="site-header">
  <div class="bar">
    <a class="brand" href="index.html" aria-label="Harris Media Group — Home"><img data-logo src="{UP}2024/12/logo-DARK.png" alt="Harris Media Group"><span class="sep"></span><span class="dot"></span></a>
    <nav class="main-nav" id="main-nav" aria-label="Main">{links}{links_extra}</nav>
    <div class="head-actions">
      <button class="icon-btn" id="theme-btn" type="button" aria-label="Switch theme"></button>
      <a class="btn btn-primary head-cta" href="contact.html"><span class="blip"></span><span class="txt">CONTACT</span></a>
      <button class="icon-btn menu-btn" id="menu-btn" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
    </div>
  </div>
  <div id="hmg-progress"></div>
</header>
<main id="main">
'''


def hero(crumbs, label, lines, lede='', actions='', meta=''):
    cr = ' <span class="meta">/</span> '.join(
        f'<a class="meta" href="{h}">{e(t)}</a>' if h else f'<span class="meta" style="color:var(--accent)">{e(t)}</span>' for h, t in crumbs)
    hl = ''.join(f'<span class="line"><span style="--d:{i}"{_Q2 if acc else ""}>{t}</span></span>'
                 for i, (t, acc) in enumerate(lines))
    return f'''<section class="hero">
  <div class="scan"></div>
  <div class="wrap">
    <div class="crumbs">{cr}</div>
    <span class="label">{label}</span>
    <h1 class="h-xl">{hl}</h1>
    {f'<p class="lede">{lede}</p>' if lede else ''}
    {f'<div class="hero-actions">{actions}</div>' if actions else ''}
  </div>
  {f'<div class="hero-meta meta">{meta}</div>' if meta else ''}
</section>
'''


def sec_head(label, title, right=''):
    return f'''<div class="sec-head" data-reveal>
  <div class="title"><span class="label">{label}</span><span class="sl">//</span><h2 class="h-md">{title}</h2></div>
  {right}
</div>'''


def ticker(items, dark=False):
    return '<div class="ticker%s" aria-hidden="true"><div class="track">%s</div></div>' % (
        ' dark' if dark else '', ''.join(f'<span>{e(t)}</span>' for t in items))


def cta(title_a="HOW CAN WE HELP?", title_b="LET'S TALK."):
    return f'''<section class="section">
  <div class="wrap">
    <div class="cta-block brackets on" data-reveal="scale">
      <div class="row">
        <div>
          <span class="label">{title_a}</span>
          <h2 class="h-lg" style="margin-top:18px">{title_b}<br><span class="accent glow">LET US BUILD YOUR AWARD-WINNING CAMPAIGN.</span></h2>
        </div>
        <div style="display:flex;gap:12px;flex-wrap:wrap">
          <a class="btn btn-primary" href="contact.html"><span class="blip"></span>CONTACT US {ARROW}</a>
          <a class="btn btn-ghost" href="tel:{PHONE.replace('-', '')}">CALL {PHONE}</a>
        </div>
      </div>
      <div class="facts"><span class="meta">REGIONS: NEW ENGLAND • FLORIDA • TEXAS • LATIN AMERICA</span><span class="meta">20+ COUNTRIES · 40+ AWARDS</span></div>
    </div>
  </div>
</section>
'''


def footer(extra=''):
    return f'''</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <a href="index.html" class="brand"><img data-logo src="{UP}2024/12/logo-DARK.png" alt="Harris Media Group" style="height:30px"></a>
        <p class="about">Championing Republican causes and advocacy initiatives through top-tier conservative political marketing and digital creative strategy.</p>
      </div>
      <div><h4>Explore</h4><ul>
        <li><a href="index.html">Home</a></li><li><a href="clients.html">Our Clients</a></li><li><a href="services.html">Our Services</a></li><li><a href="our-works.html">Our Works</a></li>
      </ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="team.html">Our Team</a></li><li><a href="careers.html">Careers</a></li><li><a href="blog.html">News</a></li><li><a href="contact.html">Contact</a></li>
      </ul></div>
      <div><h4>Get in touch</h4><ul>
        <li><a href="tel:{PHONE.replace('-', '')}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL_CONTACT}">{EMAIL_CONTACT}</a></li>
        <li><a href="mailto:{EMAIL_HR}">{EMAIL_HR}</a></li>
        <li><span class="meta">Texas · Florida · New England</span></li>
      </ul></div>
    </div>
    <div class="bottom"><span class="meta">©<span id="year">2026</span> HMG | HM GROUP<a class="staff-key" href="admin" title="Acceso del equipo" aria-label="Acceso del equipo"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="1"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg></a></span><span class="meta">EMPOWERING BRANDS · ELEVATING CAMPAIGNS</span></div>
  </div>
</footer>
{extra}
<script src="assets/hmg.js"></script>
</body>
</html>
'''


def page(fname, title, desc, current, body, image=None, extra=''):
    html = head(title, desc, image) + header(current) + body + footer(extra)
    open(os.path.join(OUT, fname), 'w', encoding='utf-8').write(html)
    PAGES.append(fname)


PAGES = []

# ======================================================================
# DATA
# ======================================================================
T = json.load(open(os.path.join(HERE, 'data_team.json'), encoding='utf-8'))
TEAM = T['team']
PROF = T['profiles']
LEADERS = TEAM[:3]

# ---- CMS content mode: content comes from the admin panel (content/*.json) ----
CONTENT = os.environ.get('HMG_CONTENT')
DRAFTS = os.environ.get('HMG_DRAFTS') == '1'
DEPT_BY_TITLE = {}
if CONTENT:
    import content_mode as CM
    TEAM, PROF, DEPT_BY_TITLE, LEADERS = CM.team(CONTENT, DRAFTS)


def dept(title):
    if title in DEPT_BY_TITLE:
        return DEPT_BY_TITLE[title]
    t = title.lower()
    if 'ceo' in t or 'vp' in t or 'director of accounts' in t or 'operations' in t:
        return 'leadership'
    if 'video' in t or 'videographer' in t or 'producer' in t:
        return 'video'
    if 'design' in t or 'creative' in t or 'developer' in t:
        return 'creative'
    return 'accounts'


DEPTS = [('all', 'ALL'), ('leadership', 'LEADERSHIP'), ('accounts', 'ACCOUNTS'), ('creative', 'CREATIVE & WEB'), ('video', 'VIDEO')]
LANG_SHORT = {'English': 'EN', 'Spanish': 'ES', 'Portuguese': 'PT'}

CLIENTS = [('Pro-Trump.png', 'Right for America PAC', 'Pro-Trump Super PAC', 'presidential'),
           ('Benjamin-Natanyahu.png', 'Benjamin Netanyahu', 'Likud · Israel', 'international'),
           ('NH-SEANET.png', 'NH Senate Republicans', 'State Legislative', 'state'),
           ('Mayor-Francis-Suarez.png', 'Francis Suarez', 'SOS America PAC', 'presidential'),
           ('Rand-Paul-1.png', 'Rand Paul', 'U.S. Senate · President 2016', 'federal'),
           ('../2025/01/Ted-Cruz.png', 'Ted Cruz', 'U.S. Senate', 'federal'),
           ('../2025/01/Rick-Scot.png', 'Rick Scott', 'Governor · U.S. Senate', 'federal'),
           ('Mike-Huckabee-1.png', 'Mike Huckabee', 'Presidential', 'presidential'),
           ('MEGOP.png', 'Maine GOP', 'State Party', 'state'),
           ('Linda.png', 'Linda McMahon', 'Campaign', 'federal'),
           ('Likud.png', 'Virginia Hospital & Healthcare Association', 'Healthcare Advocacy', 'advocacy'),
           ('TXOGA.png', 'TXOGA', 'Texas Oil & Gas Association', 'advocacy'),
           ('../2025/01/Dan-Patrick.png', 'Dan Patrick', 'Lt. Governor · Texas', 'state'),
           ('../2025/01/Sarah-Palin.png', 'Sarah Palin', 'Campaign', 'federal'),
           ('Doug.png', 'Doug Collins', 'Campaign', 'federal')]

CASES = [
    dict(tag='AAPC 2024 · CAMPAIGN OF THE YEAR', kicker='SOS America PAC', title='FRANCIS SUAREZ', chip='AWARD',
         img=UP + '2025/01/img-ai-suarez.png', link='https://drive.google.com/file/d/1X7S16rBiPGELuqlyJtyiXnwSvFm_2DPa/view',
         text='2024 AAPC Campaign Excellence Award — Digital Campaign of the Year for SOS America PAC, the Super PAC supporting Miami Mayor Francis Suarez.'),
    dict(tag='PRESIDENTIAL · 2016', kicker='Politico', title="RAND PAUL'S INTERNET ARMY", chip='FEATURED',
         img=UP + '2025/01/randpaul.png', link='https://www.politico.com/magazine/story/2015/04/rand-paul-2016-social-media-117132/',
         text="Our work on Senator Rand Paul's 2016 Presidential campaign set a new standard for digital strategy in politics, boosting his online impact and positioning him as a digitally savvy GOP candidate."),
    dict(tag='STATE LEGISLATIVE · 2025', kicker='Best Use of Online Targeting', title='NH SENATE REPUBLICANS', chip='AWARD',
         img=UP + '2025/05/harris-media-new-slider.png', link='https://drive.google.com/file/d/1rbmmw1RVOGBLwLtVTHeE2lj_E0LmBBru/view',
         text='Best Use of Online Targeting for a State Legislative Campaign (2025). Our digital strategy helped expand the New Hampshire Senate caucus to a supermajority over three election cycles.'),
    dict(tag='PRIME MINISTER · ISRAEL', kicker='Likud National Liberal Party', title='AI CHATBOT', chip='FIRST-EVER',
         img=UP + '2025/01/Chat-box.png', link='https://drive.google.com/file/d/1Log_w9TUS4wNAAxe7hSFDu8CaUQPsNws/view',
         text="Likud's chat bot facilitated 8,323 voters making phone calls through Telegram & 8,676 voters through Facebook — the first-ever AI-generated and AI-operated chatbot in presidential political history."),
]

STATS = [(16, '', 'Years of trusted expertise'), (20, '+', 'Countries worked in'), (40, '+', 'Awards won'),
         (15, '+', 'Senators / Governors'), (10, '+', 'Fortune 500 energy companies'), (7, '', 'Heads of state')]

FIRSTS = ['Built the first-ever AI-generated and AI-operated chatbot in presidential political history',
          'Ranked first in Google click-to-call advocacy for a campaign',
          'Created the first paid political Snapchat filter',
          'Created the first native Twitter video attack ad']

ICONS = {
    'ads': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 11v2a1 1 0 0 0 1 1h3l5 4V6L7 10H4a1 1 0 0 0-1 1z"/><path d="M16 8a5 5 0 0 1 0 8M19 5a9 9 0 0 1 0 14"/></svg>',
    'web': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="18" height="14" rx="1"/><path d="M3 8h18M8 21h8M12 18v3"/></svg>',
    'tv': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="2" y="6" width="20" height="13" rx="1"/><path d="m8 2 4 4 4-4"/></svg>',
    'social': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>',
    'creative': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="M2 2l7.6 7.6"/><circle cx="11" cy="11" r="2"/></svg>',
    'sms': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="m3 7 9 6 9-6"/></svg>',
    'strategy': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></svg>',
    'ai': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="6" y="6" width="12" height="12" rx="1"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/><path d="M10 10h4v4h-4z"/></svg>',
    'db': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></svg>',
    'video': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="2" y="6" width="14" height="12" rx="1"/><path d="m16 10 6-3v10l-6-3"/></svg>',
}

SERVICES = [
    ('Advertising', 'DISPLAY', 'ads', 'Digital ad campaigns that move voters and shape public opinion — planned, bought and optimized in-house across every major platform.',
     ['Meta', 'Google', 'YouTube', 'Snapchat', 'CTV', 'Programmatic']),
    ('Web Design / Dev', 'IN-HOUSE', 'web', 'Campaign and advocacy websites, donation flows and landing pages designed and built by our own developers — fast, secure and built to convert.',
     ['Websites', 'Landing pages', 'Donation flows', 'UX / UI']),
    ('TV Production / Placement', 'TV + CTV', 'tv', 'Broadcast and connected-TV spots from script to screen, with media placement that puts your message in front of the right households.',
     ['Scripting', 'Production', 'Media buying', 'CTV']),
    ('Social Media', 'META · X', 'social', 'Always-on social strategy, content calendars and community management that build movements, not just followers.',
     ['Content calendars', 'Community', 'Paid social', 'Influencers']),
    ('Creative', 'BRAND', 'creative', 'Rapid creative production — graphics, motion and brand systems that cut through the noise and stay on message.',
     ['Branding', 'Graphics', 'Motion', 'Rapid response']),
    ('SMS / Email', 'A/B', 'sms', 'Fundraising and mobilization programs across email and SMS, with rigorous A/B testing that compounds results every send.',
     ['Fundraising', 'GOTV', 'A/B testing', 'Automation']),
    ('Strategic Consulting', 'DATA', 'strategy', 'Messaging strategy from stump speeches to social copy, backed by data, research and decades of winning campaigns.',
     ['Messaging', 'Research', 'Crisis comms', 'Planning']),
    ('AI', 'AUTOMATION', 'ai', 'The team that built the first-ever AI-generated and AI-operated chatbot in presidential political history — now applied to your campaign.',
     ['Chatbots', 'Automation', 'AI creative', 'Voter contact']),
    ('Database Management', 'CRM', 'db', 'Clean, segmented supporter data and CRM workflows that power targeting, fundraising and turnout.',
     ['CRM', 'Segmentation', 'List building', 'Integrations']),
    ('Video Production', 'FILM', 'video', 'Documentary, testimonial and social-first video produced by our in-house editors and videographers.',
     ['Filming', 'Editing', 'Social cuts', 'Animation']),
]
DELIVER = [('Digital Ad Campaigns', 'Meta, Google, YouTube, and Snapchat'), ('Rapid Creative Production', 'Videos, graphics, and motion content'),
           ('Messaging Strategy', 'From stump speeches to social media copy'), ('Fundraising Support', 'Email campaigns, landing pages, and more'),
           ('Analytics & Reporting', 'Real-time insights and performance tracking')]

REGIONS = [('NEW ENGLAND', 'MAINE'), ('FLORIDA', 'MIAMI'), ('TEXAS', 'ACTIVE'), ('LATIN AMERICA', 'ES · PT')]


def stat_tiles():
    return '<div class="grid g-3">' + ''.join(
        f'<div class="panel stat hover brackets" data-reveal><div class="meta">{i + 1:02d}</div>'
        f'<div class="v"><span data-count="{v}" data-suffix="{s}">0{s}</span></div><div class="k meta" style="color:var(--text-2)">{e(k)}</div><div class="bar"></div></div>'
        for i, (v, s, k) in enumerate(STATS)) + '</div>'


# ======================================================================
# TEAM
# ======================================================================
def member_card(m, big=False):
    p = PROF.get(m['slug'], {})
    langs = ''.join(f'<span class="chip muted">{LANG_SHORT.get(l, l[:2].upper())}</span>' for l in p.get('langs', []))
    return f'''<a class="panel member hover brackets" href="team-{m['slug']}.html" data-cat="{dept(m['title'])}" data-reveal>
  <div class="photo"><img src="{e(m['img'])}" alt="{e(m['name'])}, {e(m['title'])}" loading="lazy"><span class="view">VIEW PROFILE →</span></div>
  <div class="info"><div class="role">{e(m['title'])}</div><h3 class="name">{e(m['name'])}</h3>{f'<div class="langs">{langs}</div>' if langs else ''}</div>
</a>'''


def build_team():
    intro = next(strip(t) for k, t in blocks(raw('meet-the-team')) if strip(t).startswith('At the heart')).replace('GROUP‘s', 'GROUP’s')
    n = len(TEAM)
    langs = {m['slug']: PROF[m['slug']]['langs'] for m in TEAM}
    es = [m for m in TEAM if 'Spanish' in langs[m['slug']]]
    pt = [m for m in TEAM if 'Portuguese' in langs[m['slug']]]
    units = [('leadership', 'LEADERSHIP', 'Strategy, operations and the client relationships behind every win.'),
             ('accounts', 'ACCOUNTS', 'Account executives and coordinators who run campaigns day to day.'),
             ('creative', 'CREATIVE & WEB', 'Creative direction, design and development — all in-house.'),
             ('video', 'VIDEO', 'Producers, videographers and editors who turn messages into content.')]
    by_unit = {k: [m for m in TEAM if dept(m['title']) == k] for k, *_ in units}

    # 1 hero: the face strip
    slices = ''.join(f"""<a class="fs-slice" href="team-{m['slug']}.html" style="--i:{i}" data-i="{i}">
<img src="{e(m['img'])}" alt="{e(m['name'])}, {e(m['title'])}" loading="{'eager' if i < 8 else 'lazy'}">
<span class="fs-cap"><span class="fs-role">{e(m['title'])}</span><span class="fs-name">{e(m['name'])}</span></span><span class="fs-n">{i + 1:02d}</span></a>""" for i, m in enumerate(TEAM))
    slices += '<a class="fs-slice fs-you" href="careers.html" style="--i:%d"><span class="fs-plus">+</span><span class="fs-cap"><span class="fs-role">NOW HIRING</span><span class="fs-name">YOU?</span></span></a>' % n
    body = f"""<section class="th-hero">
<div class="wrap th-top">
  <div class="crumbs"><a class="meta" href="index.html">HOME</a> <span class="meta">/</span> <span class="meta" style="color:var(--accent)">OUR TEAM</span></div>
  <div class="th-headrow">
    <div><span class="label">LEADERSHIP // PEOPLE</span>
    <h1 class="th-title"><span class="ln"><span>THE PEOPLE</span></span><span class="ln"><span class="accent">BEHIND THE WINS.</span></span></h1></div>
    <p class="lede th-lede">{e(intro)}</p>
  </div>
</div>
<div class="facestrip" id="facestrip" aria-label="The HMG team">{slices}</div>
<div class="wrap th-hint meta"><span>HOVER A FACE · CLICK TO OPEN THE PROFILE</span><span>{n} PEOPLE · EN / ES / PT</span></div>
</section>
<section class="th-stats"><div class="wrap th-stats-row">
  <div data-reveal><b><span data-count="{n}">0</span></b><span>PEOPLE</span></div>
  <div data-reveal><b><span data-count="4">0</span></b><span>UNITS</span></div>
  <div data-reveal><b><span data-count="{len(es)}">0</span></b><span>SPANISH SPEAKERS</span></div>
  <div data-reveal><b><span data-count="3">0</span></b><span>LANGUAGES</span></div>
  <div data-reveal><b><span data-count="3">0</span></b><span>REGIONS</span></div>
</div></section>
"""
    # 2 leadership dossiers
    dossiers = ''
    for i, m in enumerate(LEADERS):
        p = PROF[m['slug']]
        paras = [x for x in p['body'] if not x.startswith('[') and len(x) > 120]
        first = paras[0] if paras else ''
        if m['slug'] == 'vincent-harris' and not CONTENT:
            first = next(strip(t) for k, t in blocks(raw('meet-the-team__vincent-harris')) if strip(t).startswith('Vincent Harris is CEO'))
            first = first[:first.find('Previously')].strip()
        if len(first) > 420:
            first = first[:first.rfind('. ', 0, 420) + 1]
        first_name, _, last = m['name'].partition(' ')
        extra = ''
        if m['slug'] == 'vincent-harris':
            extra = '<div class="dz-quotes"><span>“The Man Who Invented the Republican Internet” — <b>Bloomberg</b></span><span>“…a savvy digital whiz…” — <b>New York Times Magazine</b></span></div>'
        dossiers += f"""<article class="dossier{' rev' if i % 2 else ''}" data-reveal>
  <a class="dz-photo" href="team-{m['slug']}.html"><img src="{e(m['img'])}" alt="{e(m['name'])}" loading="lazy"><span class="dz-file">FILE {i + 1:02d} / {len(LEADERS):02d}</span></a>
  <div class="dz-body">
    <span class="label">{e(m['title'])}</span>
    <h3 class="dz-name">{e(first_name)}<br><span class="accent">{e(last)}</span></h3>
    <p class="lede">{e(first)}</p>{extra}
    <a class="btn btn-ghost" href="team-{m['slug']}.html">READ FULL PROFILE {ARROW}</a>
  </div>
</article>"""
    body += f"""<section class="section" id="leadership"><div class="wrap">
{sec_head('LEADERSHIP', 'THE DOSSIERS', '<span class="meta">DECADES OF CAMPAIGN EXPERIENCE</span>')}
{dossiers}
</div></section>
"""
    # 3 org chart of units
    cols = ''
    for k, t, d in units:
        ms = by_unit[k]
        av = ''.join(f'<a href="team-{m["slug"]}.html" title="{e(m["name"])}"><img src="{e(m["img"])}" alt="{e(m["name"])}" loading="lazy"></a>' for m in ms)
        names = ''.join(f'<li><a href="team-{m["slug"]}.html">{e(m["name"])}<small>{e(m["title"])}</small></a></li>' for m in ms)
        cols += f"""<div class="unit" data-reveal><div class="unit-node"><span class="unit-n">{len(ms):02d}</span><h3>{t}</h3><p>{d}</p></div>
<div class="unit-av">{av}</div><ul class="unit-list">{names}</ul>
<button class="unit-go" type="button" data-unit="{k}">VIEW {t} IN ROSTER ↓</button></div>"""
    body += f"""<section class="section alt"><div class="wrap">
{sec_head('THE STRUCTURE', 'ONE TEAM. FOUR UNITS.', '<span class="meta">TEXAS · FLORIDA · NEW ENGLAND</span>')}
<div class="org" data-reveal><div class="org-root"><span class="blip"></span>HARRIS MEDIA GROUP</div><div class="org-lines" aria-hidden="true"><i></i><i></i><i></i><i></i></div></div>
<div class="units">{cols}</div>
</div></section>
"""
    # 4 roster with GRID / INDEX views
    filt = ''.join(f'<button type="button" data-f="{k}"{_Q3 if k == "all" else ""}>{t}</button>' for k, t in DEPTS)
    index_rows = ''.join(f"""<li data-cat="{dept(m['title'])}"><a href="team-{m['slug']}.html" style="--c:#FE572E;--ink:#0A0A0A" data-img="{e(m['img'])}" data-world="{e(m['title'])}">
<span class="rn">{i + 1:02d}</span><span class="nm">{e(m['name'])}</span><span class="wd">{e(m['title'])}</span><span class="ct">{' · '.join(LANG_SHORT.get(l, l) for l in langs[m['slug']]) or 'EN'}</span><span class="ar">→</span><img class="th" src="{e(m['img'])}" alt="" loading="lazy"></a></li>""" for i, m in enumerate(TEAM))
    body += f"""<section class="section" id="roster-sec"><div class="wrap">
{sec_head('FULL ROSTER', 'EVERYONE', '<span class="meta"><span id="team-count">00</span> SHOWN</span>')}
<div class="roster-bar">
  <div class="filters" id="team-filters" data-filters="#roster-grid" data-counter="#team-count" role="group" aria-label="Filter team">{filt}</div>
  <div class="viewtog" role="group" aria-label="View"><button type="button" class="on" data-view="grid">GRID</button><button type="button" data-view="index">INDEX</button></div>
</div>
<div class="grid g-5" id="roster-grid">{''.join(member_card(m) for m in TEAM)}</div>
<ul class="roster is-hidden" id="roster-index">{index_rows}</ul>
</div></section>
<div class="hub-preview" id="hub-preview" aria-hidden="true"><img alt="" src="{e(TEAM[0]['img'])}"><div class="cap"></div></div>
"""
    # 5 languages
    def faces(ms):
        return ''.join(f'<a href="team-{m["slug"]}.html" title="{e(m["name"])}"><img src="{e(m["img"])}" alt="{e(m["name"])}" loading="lazy"></a>' for m in ms)
    body += f"""<section class="section alt"><div class="wrap">
{sec_head('SE HABLA', 'ENGLISH · ESPAÑOL · PORTUGUÊS', '<span class="meta">NEARLY HALF OUR STAFF IS BILINGUAL</span>')}
<p class="lede" style="margin-bottom:34px">Nearly half of our staff are bilingual in English, Spanish and Portuguese — a unique strength that lets us connect with diverse audiences across the U.S. and Latin America.</p>
<div class="langs">
  <div class="lang" data-reveal><div class="lang-top"><b>EN</b><span>ENGLISH</span><em>{n}</em></div><div class="lang-bar"><i style="--w:100%"></i></div></div>
  <div class="lang" data-reveal><div class="lang-top"><b>ES</b><span>ESPAÑOL</span><em>{len(es)}</em></div><div class="lang-bar"><i style="--w:{len(es) * 100 // n}%"></i></div><div class="lang-faces">{faces(es)}</div></div>
  <div class="lang" data-reveal><div class="lang-top"><b>PT</b><span>PORTUGUÊS</span><em>{len(pt)}</em></div><div class="lang-bar"><i style="--w:{max(len(pt) * 100 // n, 4)}%"></i></div><div class="lang-faces">{faces(pt)}</div></div>
</div>
</div></section>
<section class="section"><div class="wrap">
<a class="join" href="careers.html" data-reveal>
  <span class="join-slot" aria-hidden="true">+</span>
  <span><span class="label">CAREERS</span><span class="join-t">THERE’S A SEAT<br><span class="accent">IN THE WAR ROOM.</span></span>
  <span class="lede" style="display:block;margin-top:14px">Creatives, strategists and digital experts — see our open roles in Miami.</span></span>
  <span class="btn btn-primary"><span class="blip"></span>SEE OPEN ROLES {ARROW}</span>
</a>
</div></section>
"""
    body += cta()
    html = head('Meet The Team | Harris Media Group', intro[:155], UP + '2024/12/Vincent-Picture.png').replace(
        '<link rel="stylesheet" href="assets/hmg.css">', '<link rel="stylesheet" href="assets/hmg.css">\n<link rel="stylesheet" href="assets/worlds.css">')
    html += header('team') + body + footer('<script src="assets/worlds.js" defer></script>')
    open(os.path.join(OUT, 'team.html'), 'w', encoding='utf-8').write(html)
    PAGES.append('team.html')


def split_langs(paras, n):
    """Split a bio into language versions (pages list each language one after another)."""
    if n <= 1 or len(paras) < n:
        return [paras]
    if len(paras) % n == 0:
        k = len(paras) // n
        return [paras[i * k:(i + 1) * k] for i in range(n)]
    return [paras]


def profile_body_vincent(bl):
    out = []; quotes = []; gallery = []
    def flush_gallery():
        if gallery:
            if len(gallery) == 1:
                out.append(f'<figure data-reveal><img src="{e(gallery[0])}" alt="Vincent Harris" loading="lazy"></figure>')
            else:
                out.append('<div class="gallery" data-reveal>' + ''.join(f'<img src="{e(g)}" alt="Vincent Harris" loading="lazy">' for g in gallery) + '</div>')
            gallery.clear()
    started = False
    i = 0
    while i < len(bl):
        k, t = bl[i]
        if k == 'img' and not started:
            started = True; i += 1; continue
        if not started:
            i += 1; continue
        if k == 'h2' and i + 1 < len(bl) and bl[i + 1][0] == 'h4':
            quotes.append((t, strip(bl[i + 1][1]).lstrip('—– ').strip())); i += 2; continue
        if k == 'img':
            gallery.append(t.split('|')[0]); i += 1; continue
        flush_gallery()
        if k == 'h2':
            out.append(f'<h2>{t}</h2>')
        elif t.strip() in ('TEX',):
            pass
        elif strip(t).startswith('“'):
            out.append(f'<blockquote>{t}</blockquote>')
        else:
            out.append(f'<p>{t}</p>')
        i += 1
    flush_gallery()
    qhtml = '<div class="grid g-2" style="margin-bottom:40px">' + ''.join(
        f'<div class="panel quote-card" data-reveal><q>{strip(q).strip("“”")}</q><div class="meta" style="margin-top:14px">— {e(src)}</div></div>' for q, src in quotes) + '</div>'
    return qhtml + '<div class="prose">' + '\n'.join(out) + '</div>'


def build_profiles():
    for idx, m in enumerate(TEAM):
        p = PROF[m['slug']]
        langs = p['langs'] or ['English']
        if 'bio' in p:
            portrait = p['img'] or m['img']
            vers = [(l, h) for l, h in p['bio'].items() if h.strip()] or [('English', '')]
            if len(vers) > 1:
                tabs = ''.join(f'<button type="button" data-tab="{i}" class="{"on" if i == 0 else ""}" aria-selected="{"true" if i == 0 else "false"}">{LANG_SHORT.get(l, l)}</button>' for i, (l, h) in enumerate(vers))
                panes = ''.join(f'<div data-pane="{i}"{"" if i == 0 else " hidden"} class="prose">{h}</div>' for i, (l, h) in enumerate(vers))
                bio = f'<div data-tabs><div class="tabs" role="tablist">{tabs}</div>{panes}</div>'
            else:
                bio = f'<div class="prose">{vers[0][1]}</div>'
        elif m['slug'] == 'vincent-harris':
            bio = profile_body_vincent(blocks(raw('meet-the-team__vincent-harris')))
            portrait = UP + '2024/12/vnct-2.png'
        else:
            paras = [l for l in p['body'] if not l.startswith('[')]
            versions = split_langs(paras, len(langs))
            portrait = p['img'] or m['img']
            if len(versions) > 1:
                tabs = ''.join(f'<button type="button" data-tab="{i}" class="{"on" if i == 0 else ""}" aria-selected="{"true" if i == 0 else "false"}">{LANG_SHORT.get(l, l)}</button>' for i, l in enumerate(langs))
                panes = ''.join(f'<div data-pane="{i}"{"" if i == 0 else " hidden"} class="prose">' + ''.join(f'<p>{e(x)}</p>' for x in v) + '</div>' for i, v in enumerate(versions))
                bio = f'<div data-tabs><div class="tabs" role="tablist">{tabs}</div>{panes}</div>'
            else:
                bio = '<div class="prose">' + ''.join(f'<p>{e(x)}</p>' for x in paras) + '</div>'
        prev_m = TEAM[idx - 1]; next_m = TEAM[(idx + 1) % len(TEAM)]
        first, _, last = m['name'].partition(' ')
        langs_html = ''.join(f'<span class="chip">{e(l)}</span>' for l in p['langs'])
        body = hero([('index.html', 'HOME'), ('team.html', 'OUR TEAM'), (None, m['name'].upper())], e(m['title']).upper(),
                    [(e(first).upper(), False), (e(last).upper(), True)], '', '', dept(m['title']).upper() + ' · HMG')
        body += f'''<section class="section"><div class="wrap">
<div class="profile">
  <div class="portrait" data-reveal="left">
    <div class="panel brackets on"><div class="photo ratio-45"><img src="{e(portrait)}" alt="{e(m['name'])}"></div>
    <div class="pad" style="border-top:2px solid var(--accent)"><div class="role meta" style="color:var(--accent)">{e(m['title'])}</div><div class="h-sm" style="margin-top:6px">{e(m['name'])}</div>
    {f'<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:12px">{langs_html}</div>' if langs_html else ''}</div></div>
    <a class="btn btn-primary" style="margin-top:16px;width:100%;justify-content:center" href="contact.html"><span class="blip"></span>WORK WITH US</a>
  </div>
  <div data-reveal>
    <span class="label">BIO</span>
    <div style="margin-top:22px">{bio}</div>
  </div>
</div>
<div class="pager">
  <a class="panel hover" href="team-{prev_m['slug']}.html"><div class="meta">← PREVIOUS</div><div class="h-sm" style="margin-top:8px">{e(prev_m['name'])}</div></a>
  <a class="panel hover r" href="team-{next_m['slug']}.html"><div class="meta">NEXT →</div><div class="h-sm" style="margin-top:8px">{e(next_m['name'])}</div></a>
</div>
</div></section>
'''
        body += cta()
        desc = (strip(p['body'][0]) if p['body'] else m['title'])[:155]
        page(f"team-{m['slug']}.html", f"{m['name']} — {m['title']} | Harris Media Group", desc, 'team', body, portrait)


# ======================================================================
# CLIENTS
# ======================================================================
def build_clients():
    cats = [('all', 'ALL'), ('presidential', 'PRESIDENTIAL'), ('federal', 'FEDERAL'), ('state', 'STATE'), ('international', 'INTERNATIONAL'), ('advocacy', 'ADVOCACY')]
    filt = ''.join(f'<button type="button" data-f="{k}"{_Q3 if k == "all" else ""}>{t}</button>' for k, t in cats)
    logos = ''.join(
        f'<div class="panel hover brackets logo-tile" data-cat="{c}" data-reveal><img src="{UP}2024/12/{f}" alt="{e(n)}" loading="lazy"><div><div class="h-sm" style="font-size:.78rem">{e(n)}</div><div class="meta" style="margin-top:4px">{e(s)}</div></div></div>'
        for f, n, s, c in CLIENTS).replace('2024/12/../', '')
    cases = ''.join(f'''<article class="panel case brackets" data-reveal>
  <div class="photo"><img src="{c['img']}" alt="{e(c['title'])}" loading="lazy"></div>
  <div class="body">
    <div style="display:flex;justify-content:space-between;gap:12px;align-items:center"><span class="meta" style="color:var(--accent)">{c['tag']}</span><span class="chip">{c['chip']}</span></div>
    <div class="meta">{e(c['kicker'])}</div>
    <h3 class="h-md">{e(c['title'])}</h3>
    <p class="lede" style="font-size:1rem">{e(c['text'])}</p>
    <div><a class="btn btn-ghost" href="{c['link']}" target="_blank" rel="noopener">VIEW CASE {ARROW}</a></div>
  </div>
</article>''' for c in CASES)
    firsts = ''.join(f'<li data-reveal><span class="num">{i + 1:02d}</span><span>{e(f)}</span></li>' for i, f in enumerate(FIRSTS))
    regions = ''.join(f'<div data-reveal><div class="meta">{i + 1:02d}</div><div class="h-sm" style="margin-top:10px">{r}</div><div class="meta" style="color:var(--accent);margin-top:6px">{s}</div></div>' for i, (r, s) in enumerate(REGIONS))
    body = hero([('index.html', 'HOME'), (None, 'OUR CLIENTS')], 'WHO WE’VE WORKED WITH', [('TRUSTED BY', False), ('WINNERS', True)],
                'With a proven track record in the U.S. and internationally, HM GROUP is a powerhouse in the political advertising arena. But don’t take our word for it — the numbers speak for themselves.',
                f'<a class="btn btn-primary" href="#case-files">CASE FILES {ARROW}</a><a class="btn btn-ghost" href="#roster">ALL CLIENTS</a>', 'U.S. + INTERNATIONAL')
    body += f'''<section class="section"><div class="wrap">
{sec_head('THE WAR ROOM', 'BY THE NUMBERS', '<span class="meta">GLOBALLY RECOGNIZED</span>')}
{stat_tiles()}
</div></section>
{ticker(['Let us build your award-winning campaign', 'AAPC Digital Campaign of the Year', 'Best Use of Online Targeting 2025', 'Winner: 2026 Best Overall Digital Program'])}
<section class="section" id="case-files"><div class="wrap">
{sec_head('SELECTED WORK', 'CASE FILES', '<span class="meta">04 FEATURED CAMPAIGNS</span>')}
{cases}
</div></section>
<section class="section alt" id="roster"><div class="wrap">
{sec_head('CLIENT ROSTER', 'WHO WE’VE WORKED WITH', '<span class="meta"><span id="cl-count">00</span> CLIENTS</span>')}
<div class="filters" data-filters="#logos" data-counter="#cl-count" style="margin-bottom:28px" role="group" aria-label="Filter clients">{filt}</div>
<div class="grid g-5" id="logos">{logos}</div>
</div></section>
<section class="section"><div class="wrap">
<div class="split">
  <div>
    {sec_head('FIRSTS', 'WE WROTE THE PLAYBOOK')}
    <ol class="firsts">{firsts}</ol>
  </div>
  <div class="panel photo brackets on" data-reveal="scale" style="aspect-ratio:4/5"><img src="{UP}2024/12/Netanyahu-768x484.jpg" alt="Benjamin Netanyahu campaign" loading="lazy"><div class="tag"><div class="meta" style="color:#FFB59A">HEAD OF STATE · ISRAEL</div><div class="h-sm" style="margin-top:6px">2015 & 2022 VICTORIES</div></div></div>
</div>
</div></section>
<section class="section alt"><div class="wrap">
{sec_head('FOOTPRINT', 'YOU CAN FIND US IN…', '<span class="meta">4 REGIONS</span>')}
<div class="regions">{regions}</div>
</div></section>
'''
    body += cta()
    page('clients.html', 'Our Clients & Case Files | Harris Media Group',
         'Presidents, prime ministers, senators and governors: the conservative leaders and causes Harris Media Group has helped win.', 'clients', body, UP + '2025/01/img-ai-suarez.png')


# ======================================================================
# SERVICES
# ======================================================================
def build_services():
    cards = ''.join(f'''<article class="panel svc hover brackets" data-reveal id="{slugify(n)}">
  <div style="display:flex;justify-content:space-between;align-items:flex-start"><div class="ico">{ICONS[ic]}</div><span class="num">{i + 1:02d}.</span></div>
  <div><div class="meta" style="color:var(--accent)">{t}</div><h3 class="h-sm" style="margin-top:6px;font-size:1.1rem">{e(n)}</h3></div>
  <p>{e(d)}</p>
  <ul>{''.join(f'<li class="chip muted">{e(x)}</li>' for x in tags)}</ul>
  <a class="link-arrow" href="contact.html?service={e(n)}">START A PROJECT →</a>
</article>''' for i, (n, t, ic, d, tags) in enumerate(SERVICES))
    deliver = ''.join(f'<div class="panel pad hover" data-reveal><div class="num">{i + 1:02d}</div><div class="h-sm" style="margin-top:12px">{e(a)}</div><p class="lede" style="font-size:.95rem;margin-top:8px">{e(b)}</p></div>' for i, (a, b) in enumerate(DELIVER))
    steps = [('STRATEGY', 'We learn your race, your voters and your goals, then build the plan and the message.'),
             ('CREATIVE', 'Our in-house designers, editors and writers produce everything — fast.'),
             ('LAUNCH', 'Ads, sites, email and SMS go live across every channel at once.'),
             ('OPTIMIZE', 'Real-time reporting and A/B testing turn data into more votes and dollars.')]
    steps_html = ''.join(f'<div class="panel step hover" data-reveal><div class="n">{i + 1:02d}</div><div class="h-sm" style="margin-top:14px">{a}</div><p class="lede" style="font-size:.95rem;margin-top:8px">{b}</p></div>' for i, (a, b) in enumerate(steps))
    body = hero([('index.html', 'HOME'), (None, 'OUR SERVICES')], 'CAPABILITIES & FOOTPRINT', [('10 DISCIPLINES', False), ('ONE TEAM', True)],
                'HM GROUP is the leading digital firm for conservative political marketing and creative strategy. We champion Center-Right causes by providing strategy, advertising, and creative services for award-winning advocacy initiatives and campaigns.',
                f'<a class="btn btn-primary" href="#disciplines">EXPLORE SERVICES {ARROW}</a><a class="btn btn-ghost" href="our-works.html">SEE OUR WORK</a>', 'STRATEGY · ADVERTISING · CREATIVE')
    body += f'''<section class="section" id="disciplines"><div class="wrap">
{sec_head('OUR SERVICES', 'WHAT WE DO', '<span class="meta">10 DISCIPLINES · ONE TEAM</span>')}
<div class="grid g-3 svc-grid">{cards}</div>
</div></section>
{ticker([n for n, *_ in SERVICES], dark=True)}
<section class="section"><div class="wrap">
{sec_head('THE DELIVERABLES', 'WHAT YOU GET')}
<div class="grid g-5">{deliver}</div>
</div></section>
<section class="section alt"><div class="wrap">
{sec_head('PROCESS', 'HOW WE WIN', '<span class="meta">FROM BRIEF TO BALLOT</span>')}
<div class="grid g-4 steps">{steps_html}</div>
</div></section>
<section class="section"><div class="wrap">
{sec_head('TRACK RECORD', 'THE NUMBERS')}
{stat_tiles()}
</div></section>
'''
    body += cta()
    page('services.html', 'Our Services | Harris Media Group',
         'Advertising, web, TV, social, creative, SMS/email, consulting, AI, database and video for conservative campaigns and causes.', 'services', body)


# ======================================================================
# CAREERS
# ======================================================================
JOBS = [('senior-account-executive', 'Senior Account Executive'), ('digital-marketing-coordinator', 'Digital Marketing Coordinator'),
        ('graphic-designer', 'Graphic Designer'), ('digital-marketing-internship-spring-2026', 'Digital Marketing Internship (Spring 2026)'),
        ('graphic-design-internship-spring-2026', 'Graphic Design Internship (Spring 2026)')]


def job_type(t):
    return 'INTERNSHIP' if 'Intern' in t else 'FULL-TIME'


def render_job(bl):
    out = []; listy = False; started = False
    for k, t in bl:
        s = strip(t)
        if k in ('h1', 'h2') and not started:
            started = True; continue
        if not started or k == 'img':
            continue
        if re.match(r'^(Prev|Next)', s):
            continue
        is_head = (k in ('h3', 'h4') or (k == 'p' and len(s) < 60 and s.endswith(':')))
        if is_head:
            out.append(f'<h3>{e(s.rstrip(":"))}</h3>'); listy = not s.lower().startswith(('about', 'please')); continue
        if k == 'li' or (listy and k == 'p' and len(s) < 280 and not s.lower().startswith(('to apply', 'please'))):
            if out and out[-1] == '</ul>':
                out.pop()
            else:
                out.append('<ul>')
            out.append(f'<li>{t}</li>'); out.append('</ul>'); continue
        listy = False if k == 'p' and len(s) >= 280 else listy
        out.append(f'<p>{t}</p>')
    return '\n'.join(out)


def build_careers():
    rows = ''.join(f'''<a class="job" href="careers-{s}.html" data-reveal>
  <span class="num">{i + 1:02d}</span>
  <div><div class="t">{e(t)}</div><div class="meta" style="margin-top:6px">MIAMI, FL · HYBRID</div></div>
  <span class="chip">{job_type(t)}</span>
  <span class="go" aria-hidden="true">→</span>
</a>''' for i, (s, t) in enumerate(JOBS))
    why = [('Meaningful work', 'Help drive causes and ideas that shape a stronger tomorrow.'),
           ('Room to grow', 'Learn, take on new challenges, and build a career with purpose.'),
           ('People who care', 'Work alongside talented, driven professionals who value true collaboration.')]
    why_html = ''.join(f'<div class="panel pad hover brackets" data-reveal><div class="step"><div class="n" style="font-size:3.4rem;font-weight:900;color:transparent;-webkit-text-stroke:1px var(--accent);line-height:1">{i + 1:02d}</div></div><h3 class="h-sm" style="font-size:1.2rem">{a}</h3><p class="lede" style="font-size:.98rem;margin-top:10px">{b}</p></div>' for i, (a, b) in enumerate(why))
    paths = ['Chiefs of Staff for State Representatives', 'Heads of Staff at major tech companies',
             'Government Affairs Executives in the oil and gas industry', 'Digital Advertisers for committees in Washington, D.C.']
    body = hero([('index.html', 'HOME'), (None, 'CAREERS')], 'CAREERS AT HMG', [('WORK THAT', False), ('MOVES PEOPLE', True)],
                'At <strong>HMG</strong>, we’re more than just a workplace. We’re a robust team of creatives, strategists, and digital experts passionate about making a real difference in the world. In the fast-paced arena of political advertising, we provide opportunities for you to grow, learn, and make an impact.',
                f'<a class="btn btn-primary" href="#openings">SEE OPEN ROLES {ARROW}</a><a class="btn btn-ghost" href="mailto:{EMAIL_HR}">SUBMIT YOUR RESUME</a>', f'{len(JOBS)} OPEN ROLES · MIAMI, FL')
    body += f'''<section class="section"><div class="wrap">
<div class="grid g-2" style="align-items:stretch">
  <div class="panel photo brackets on" data-reveal="left" style="min-height:360px"><img src="{UP}2026/09/work-1024x702.avif" alt="The HMG team at work" loading="lazy"></div>
  <div class="panel photo" data-reveal="scale" style="min-height:360px"><img src="{UP}2026/10/bk2.avif" alt="HMG office" loading="lazy"><div class="tag"><div class="meta" style="color:#FFB59A">TEXAS · FLORIDA · NEW ENGLAND</div><div class="h-sm" style="margin-top:6px">A PLACE TO MAKE AN IMPACT</div></div></div>
</div>
</div></section>
<section class="section alt"><div class="wrap">
{sec_head('WHY HMG', 'MORE THAN A WORKPLACE', '<span class="meta">A PLACE TO MAKE AN IMPACT</span>')}
<div class="grid g-3">{why_html}</div>
</div></section>
<section class="section"><div class="wrap">
<div class="grid g-2" style="gap:clamp(28px,5vw,72px)">
  <div data-reveal>
    {sec_head('PATH OF SUCCESS', 'REMARKABLE CAREER PATHS')}
    <p class="lede">Many of our former employees have gone on to achieve remarkable roles, including:</p>
    <ul class="paths" style="margin-top:20px">{''.join(f'<li>{e(p)}</li>' for p in paths)}</ul>
  </div>
  <div class="panel pad brackets on" data-reveal style="align-self:center">
    <span class="label">INTERNSHIP PATH</span>
    <h3 class="h-md" style="margin:16px 0">GET YOUR FOOT IN THE DOOR</h3>
    <p class="lede">Getting your foot in the door as an intern can also be an excellent way to kick-start your career. Some of our current company leaders began as HM GROUP interns, so you never know where the opportunity can take you.</p>
  </div>
</div>
</div></section>
{ticker(['Join a team that drives change', 'Miami, FL · Hybrid', 'Internships open for Spring 2026'])}
<section class="section" id="openings"><div class="wrap">
{sec_head('CURRENT OPENINGS', 'JOIN A TEAM THAT DRIVES CHANGE', f'<span class="meta">{len(JOBS)} ROLES</span>')}
<div>{rows}</div>
</div></section>
<section class="section"><div class="wrap">
<div class="cta-block brackets on" data-reveal="scale"><div class="row">
  <div><span class="label">LET’S DO MEANINGFUL WORK</span><h2 class="h-lg" style="margin-top:18px">DO YOU THINK YOU<br><span class="accent glow">BELONG HERE?</span></h2>
  <p class="lede" style="margin-top:18px">Whether you’re interested in an internship or think you’d be a great addition to our leadership team, we want to hear from you. If you’re creative and passionate about supporting free markets in this country, please submit your resume to <a class="accent" href="mailto:{EMAIL_HR}">{EMAIL_HR}</a>, specifying the position you’re applying for.</p></div>
  <a class="btn btn-primary" href="mailto:{EMAIL_HR}"><span class="blip"></span>SUBMIT YOUR RESUME {ARROW}</a>
</div></div>
</div></section>
'''
    page('careers.html', 'Careers | Harris Media Group', 'Work that moves people. Join HMG’s team of creatives, strategists and digital experts in Miami.', 'careers', body, UP + '2026/09/work-1024x702.avif')

    for i, (s, t) in enumerate(JOBS):
        content = render_job(blocks(raw('careers-old__' + s)))
        others = ''.join(f'<a class="job" href="careers-{s2}.html" style="grid-template-columns:minmax(0,1fr) auto"><div><div class="t" style="font-size:.95rem">{e(t2)}</div><div class="meta" style="margin-top:4px">MIAMI, FL · HYBRID</div></div><span class="go">→</span></a>' for s2, t2 in JOBS if s2 != s)
        subject = 'Application — ' + t
        body = hero([('index.html', 'HOME'), ('careers.html', 'CAREERS'), (None, t.upper())], f'OPEN ROLE · {job_type(t)}',
                    [(e(t).upper(), False)], '', f'<a class="btn btn-primary" href="mailto:{EMAIL_HR}?subject={e(subject)}"><span class="blip"></span>APPLY NOW {ARROW}</a><a class="btn btn-ghost" href="careers.html#openings">ALL ROLES</a>', 'MIAMI, FL · HYBRID')
        body += f'''<section class="section"><div class="wrap"><div class="split">
  <article class="prose" data-reveal>{content}</article>
  <aside class="apply-box" data-reveal>
    <div class="panel pad brackets on">
      <span class="label">APPLY</span>
      <div style="margin-top:18px">
        <div class="info-row"><span class="k meta">ROLE</span><span class="v">{e(t)}</span></div>
        <div class="info-row"><span class="k meta">LOCATION</span><span class="v">Miami, FL</span></div>
        <div class="info-row"><span class="k meta">SCHEDULE</span><span class="v">Hybrid</span></div>
        <div class="info-row"><span class="k meta">TYPE</span><span class="v">{job_type(t).title()}</span></div>
      </div>
      <p class="lede" style="font-size:.92rem;margin:18px 0">Send your resume (and portfolio, if relevant) to <a class="accent" href="mailto:{EMAIL_HR}">{EMAIL_HR}</a> with the position in the subject line.</p>
      <a class="btn btn-primary" style="width:100%;justify-content:center" href="mailto:{EMAIL_HR}?subject={e(subject)}"><span class="blip"></span>APPLY NOW</a>
    </div>
    <div style="margin-top:24px"><div class="meta" style="margin-bottom:10px">OTHER OPENINGS</div>{others}</div>
  </aside>
</div></div></section>
'''
        page(f'careers-{s}.html', f'{t} | Careers at Harris Media Group', f'{t} — Miami, FL (Hybrid). Join Harris Media Group.', 'careers', body)


# ======================================================================
# BLOG / NEWS
# ======================================================================
POSTS = [('hmg-expands-to-new-england-welcomes-representative-reagan-paul-to-lead-regional-growth', 'PRESS RELEASES', 'Nov 13, 2025', None),
         ('floridas-premier-marketing-and-digital-advertising-solutions', 'FLORIDA MARKETING & DIGITAL', 'Jan 21, 2025', None),
         ('innovative-israeli-and-jewish-advocacy-campaigns', 'ISRAELI / JEWISH ADVOCACY', 'Jan 21, 2025', None),
         ('conservative-political-marketing-agency', 'POLITICAL MARKETING', 'Jan 21, 2025', UP + '2025/01/preview-image-1024x512.png'),
         ('global-reach-and-international-campaign-services', 'INTERNATIONAL', 'Jan 21, 2025', None)]


def post_content(slug):
    bl = blocks(raw(slug))
    title = next(strip(t) for k, t in bl if k == 'h1')
    out = []; started = False; listy = False
    for k, t in bl:
        s = strip(t)
        if k == 'h1':
            started = True; continue
        if not started or re.match(r'^(Prev|Next)', s) or k == 'img':
            continue
        if k in ('h2', 'h3', 'h4'):
            out.append(f'<h2>{s}</h2>' if k == 'h2' else f'<h3>{s}</h3>'); listy = 'what you get' in s.lower(); continue
        if listy and k == 'p' and len(s) < 120:
            out.append(f'<ul><li>{t}</li></ul>'); continue
        if s.startswith('“') or s.startswith('"'):
            out.append(f'<blockquote>{t}</blockquote>'); continue
        if s in ('FOR IMMEDIATE RELEASE',) or s.startswith(('About HMG', 'Media Contact')):
            out.append(f'<p><strong>{t}</strong></p>'); continue
        out.append(f'<p>{t}</p>')
    html = '\n'.join(out).replace('</ul>\n<ul>', '')
    excerpt = next((strip(t) for k, t in bl if k == 'p' and len(strip(t)) > 120), '')
    return title, html, excerpt


def cover(img, title):
    if img:
        return f'<img src="{img}" alt="{e(title)}" loading="lazy">'
    words, out = title.split(',')[0].split(), ''
    for w in words:
        if len(out) + len(w) > 34: break
        out = (out + ' ' + w).strip()
    return f'<div class="cover-art"><b>{e(out)}</b></div>'


if CONTENT:
    POSTS, post_content, NEWS_META = CM.news(CONTENT, DRAFTS)


def build_blog():
    data = [(s, c, d, img) + post_content(s) for s, c, d, img in POSTS]
    cats = [('all', 'ALL')] + [(slugify(c), c) for c in dict.fromkeys(p[1] for p in data)]
    filt = ''.join(f'<button type="button" data-f="{k}"{_Q3 if k == "all" else ""}>{t}</button>' for k, t in cats)
    feat = data[0]
    cards = ''.join(f'''<a class="panel post-card hover brackets" href="blog-{s}.html" data-cat="{slugify(c)}" data-reveal>
  <div class="photo">{cover(img, c.title())}</div>
  <div class="body"><div style="display:flex;justify-content:space-between;gap:10px"><span class="meta" style="color:var(--accent)">{c}</span><span class="meta">{d}</span></div>
  <h3>{e(t)}</h3><p>{e(x[:170])}…</p><span class="link-arrow more">READ MORE →</span></div>
</a>''' for s, c, d, img, t, _, x in data[1:])
    body = hero([('index.html', 'HOME'), (None, 'NEWS')], 'NEWSROOM // PRESS', [('NEWS &', False), ('INSIGHTS', True)],
                'Press releases, expansion news and perspectives on conservative political marketing from the Harris Media Group team.', '', f'{len(data)} ARTICLES')
    s, c, d, img, t, _, x = feat
    body += f'''<section class="section"><div class="wrap">
{sec_head('LATEST', 'FEATURED', f'<span class="meta">{c}</span>')}
<a class="panel case hover brackets" href="blog-{s}.html" data-reveal>
  <div class="photo">{cover(img, t)}</div>
  <div class="body"><span class="meta" style="color:var(--accent)">{c} · {d}</span><h3 class="h-md">{e(t)}</h3><p class="lede" style="font-size:1rem">{e(x[:260])}…</p><span class="btn btn-primary" style="align-self:flex-start">READ THE RELEASE {ARROW}</span></div>
</a>
</div></section>
<section class="section alt"><div class="wrap">
{sec_head('ARCHIVE', 'ALL ARTICLES', '<span class="meta"><span id="post-count">00</span> SHOWN</span>')}
<div class="filters" data-filters="#posts" data-counter="#post-count" style="margin-bottom:28px" role="group" aria-label="Filter articles">{filt}</div>
<div class="grid g-2" id="posts">{cards}</div>
</div></section>
'''
    body += cta()
    page('blog.html', 'News & Press | Harris Media Group', 'Press releases and insights from Harris Media Group.', 'blog', body)

    for i, (s, c, d, img, t, html, x) in enumerate(data):
        prv = data[i - 1] if i > 0 else None; nxt = data[i + 1] if i + 1 < len(data) else None
        pager = '<div class="pager">' + (
            f'<a class="panel hover" href="blog-{prv[0]}.html"><div class="meta">← PREVIOUS</div><div class="h-sm" style="margin-top:8px">{e(prv[4])}</div></a>' if prv else '<span></span>') + (
            f'<a class="panel hover r" href="blog-{nxt[0]}.html"><div class="meta">NEXT →</div><div class="h-sm" style="margin-top:8px">{e(nxt[4])}</div></a>' if nxt else '') + '</div>'
        words = t.upper().split()
        mid = max(1, len(words) // 2)
        body = hero([('index.html', 'HOME'), ('blog.html', 'NEWS'), (None, c)], f'{c} · {d.upper()}',
                    [(' '.join(words[:mid]), False), (' '.join(words[mid:]), True)])
        body = body.replace('class="h-xl"', 'class="h-lg"')
        body += f'''<section class="section"><div class="wrap"><div class="article">
{f'<div class="panel photo brackets on ratio-169" data-reveal style="margin-bottom:40px">{cover(img, t)}</div>' if img else ''}
<article class="prose" data-reveal>{html}</article>
<div class="panel pad" style="margin-top:40px;display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between;align-items:center" data-reveal>
  <div><div class="meta">SHARE</div><div style="display:flex;gap:10px;margin-top:10px">
    <a class="chip muted" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text={e(t)}">X</a>
    <a class="chip muted" target="_blank" rel="noopener" href="https://www.linkedin.com/sharing/share-offsite/?url=https://www.harrismediallc.com/{s}/">LINKEDIN</a>
    <a class="chip muted" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u=https://www.harrismediallc.com/{s}/">FACEBOOK</a></div></div>
  <a class="btn btn-ghost" href="blog.html">ALL NEWS</a>
</div>
{pager}
</div></div></section>
'''
        body += cta()
        page(f'blog-{s}.html', f'{t} | Harris Media Group', x[:155], 'blog', body, img)


# ======================================================================
# CONTACT
# ======================================================================
def build_contact():
    opts = ['Advertising', 'Graphic Design', 'Web Design / Dev', 'TV Production / Placement', 'Social Media', 'SMS / Email',
            'Strategic Consulting', 'AI', 'Database Management', 'Video Production', 'Games', 'Fundraising', 'Elections']
    options = '<option value="">I need help with…</option>' + ''.join(f'<option>{e(o)}</option>' for o in opts)
    ac_attr = lambda ac: f' autocomplete="{ac}"' if ac else ''
    f = lambda name, label, typ='text', req=False, ac='': f'<div class="field"><label for="f-{name}">{label}{" *" if req else ""}</label><input id="f-{name}" name="{name}" type="{typ}"{" required" if req else ""}{ac_attr(ac)}><span class="err">Please fill in this field correctly.</span></div>'
    regions = ''.join(f'<div class="info-row"><span class="k meta">{r}</span><span class="v" style="color:var(--accent)">{s}</span></div>' for r, s in REGIONS)
    body = hero([('index.html', 'HOME'), (None, 'CONTACT')], 'CONTACT // DISPATCH', [('LET’S TALK', False), ('ABOUT YOUR NEXT PROJECT', True)],
                'Whether you have questions, need assistance, or are ready to take your campaign or advocacy initiative to the next level, our team is here to help. Fill out the form, and we’ll get back to you promptly.',
                '', 'RESPONSE WITHIN 1 BUSINESS DAY')
    body = body.replace('<h1 class="h-xl">', '<h1 class="h-lg">')
    body += f'''<section class="section"><div class="wrap"><div class="contact-grid">
  <aside data-reveal="left">
    <div class="panel pad brackets on">
      <span class="label">KEEP IN TOUCH</span>
      <div style="margin-top:18px">
        <div class="info-row"><span class="k meta">PHONE</span><a class="v" href="tel:{PHONE.replace('-', '')}">{PHONE}</a></div>
        <div class="info-row"><span class="k meta">EMAIL</span><a class="v" href="mailto:{EMAIL_CONTACT}">{EMAIL_CONTACT}</a></div>
        <div class="info-row"><span class="k meta">CAREERS</span><a class="v" href="mailto:{EMAIL_HR}">{EMAIL_HR}</a></div>
      </div>
    </div>
    <div class="panel pad" style="margin-top:16px">
      <span class="label">WHERE YOU CAN FIND US</span>
      <div style="margin-top:10px">{regions}</div>
    </div>
  </aside>
  <div class="panel pad brackets" data-reveal>
    <span class="label">SEND A MESSAGE</span>
    <h2 class="h-md" style="margin:14px 0 26px">HOW CAN WE HELP?</h2>
    <form id="contact-form" novalidate data-mailto="{EMAIL_CONTACT}" data-endpoint="">
      <div class="grid g-2">
        {f('first_name', 'First Name', req=True, ac='given-name')}
        {f('last_name', 'Last Name', ac='family-name')}
        {f('company', 'Company', ac='organization')}
        {f('phone', 'Phone Number', 'tel', ac='tel')}
      </div>
      <div class="grid" style="margin-top:16px">
        {f('email', 'Email', 'email', True, 'email')}
        <div class="field"><label for="f-service">Select the service you need help with *</label><select id="f-service" name="service" required>{options}</select><span class="err">Please choose a service.</span></div>
        <div class="field"><label for="f-message">Tell us more about what you need</label><textarea id="f-message" name="message" placeholder="I need help with my campaign"></textarea></div>
        <input type="text" name="website" tabindex="-1" autocomplete="off" style="display:none" aria-hidden="true">
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;margin-top:22px">
        <span class="meta">* REQUIRED</span>
        <button class="btn btn-primary" type="submit"><span class="blip"></span>SEND MESSAGE {ARROW}</button>
      </div>
    </form>
    <div class="form-ok" id="form-ok" role="status">
      <div class="h-lg accent glow">THANK YOU.</div>
      <p class="lede" style="margin:16px auto 0">Your message is on its way. Our team will get back to you promptly — or call us at {PHONE}.</p>
    </div>
  </div>
</div></div></section>
{ticker(['Let us build your award-winning campaign', 'New England · Florida · Texas · Latin America', 'Call ' + PHONE])}
'''
    page('contact.html', 'Contact | Harris Media Group', 'Let’s talk about your next project. Call 512-900-9439 or send us a message.', None, body)


# ======================================================================
# OUR WORKS
# ======================================================================
WORKS = [('VIDEO', 'video'), ('SOCIAL', 'social'), ('CREATIVE', 'creative'), ('BRAND', 'brand'), ('SOCIAL', 'social'), ('CREATIVE', 'creative'),
         ('VIDEO', 'video'), ('BRAND', 'brand'), ('SOCIAL', 'social'), ('VIDEO', 'video'), ('CREATIVE', 'creative'), ('VIDEO', 'video'),
         ('BRAND', 'brand'), ('CREATIVE', 'creative'), ('VIDEO', 'video'), ('SOCIAL', 'social'), ('BRAND', 'brand')]


PLATFORM_NAME = {'youtube': 'YouTube', 'vimeo': 'Vimeo', 'facebook': 'Facebook', 'instagram': 'Instagram'}
PLATFORM_ICON = {
    'facebook': '<svg viewBox="0 0 24 24" width="30" height="30" fill="currentColor" aria-hidden="true"><path d="M14 8h3V4h-3c-2.8 0-4 1.8-4 4.3V10H7v4h3v8h4v-8h3l1-4h-4V8.6c0-.4.3-.6.6-.6z"/></svg>',
    'instagram': '<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
    'youtube': '<svg viewBox="0 0 24 24" width="30" height="30" fill="currentColor" aria-hidden="true"><path d="M22 8.2c-.2-1.6-1-2.7-2.6-2.9C16.9 5 12 5 12 5s-4.9 0-7.4.3C3 5.5 2.2 6.6 2 8.2 1.8 9.6 1.8 12 1.8 12s0 2.4.2 3.8c.2 1.6 1 2.7 2.6 2.9 2.5.3 7.4.3 7.4.3s4.9 0 7.4-.3c1.6-.2 2.4-1.3 2.6-2.9.2-1.4.2-3.8.2-3.8s0-2.4-.2-3.8zM10 15.2V8.8l5.2 3.2z"/></svg>',
    'vimeo': '<svg viewBox="0 0 24 24" width="30" height="30" fill="currentColor" aria-hidden="true"><path d="M22 7.4c-.1 2-1.5 4.7-4.2 8.1C15 19.1 12.7 21 10.7 21c-1.2 0-2.3-1.1-3.1-3.4L6 11.8c-.6-2.2-1.2-3.4-1.9-3.4-.2 0-.7.3-1.6.9L1.6 8.2l2.9-2.6C5.8 4.5 6.8 3.9 7.4 3.9c1.6-.2 2.5.9 2.9 3.2.4 2.5.7 4 .8 4.6.4 1.9.9 2.9 1.4 2.9.4 0 1-.6 1.9-1.9.8-1.3 1.3-2.3 1.3-3 .1-1.1-.3-1.7-1.3-1.7-.5 0-.9.1-1.4.3 1-3.1 2.8-4.6 5.4-4.5 2 .1 2.9 1.3 2.8 3.6z"/></svg>',
}


def build_works():
    cats = [('all', 'ALL'), ('video', 'VIDEO'), ('social', 'SOCIAL'), ('creative', 'CREATIVE'), ('brand', 'BRAND')]
    filt = ''.join(f'<button type="button" data-f="{k}"{_Q3 if k == "all" else ""}>{t}</button>' for k, t in cats)
    if CONTENT:
        items = CM.works(CONTENT, DRAFTS)
    else:
        items = [dict(title=f'Project Title {i + 1:02d}', client='CLIENT NAME', year='2026', category=cat, image=f'assets/works/work-{i + 1:02d}.webp', video='', embed='')
                 for i, (lab, cat) in enumerate(WORKS)]
    play = '<span class="play" aria-hidden="true"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>'
    cards = []
    for i, w in enumerate(items):
        is_vid = bool(w.get('video') or w.get('embed'))
        plat = w.get('platform', '')
        if w.get('image'):
            media = f'<img src="{e(w["image"])}" alt="{e(w["title"])}" loading="lazy">'
        else:
            media = f'<div class="work-ph ph-{plat}"><span>{PLATFORM_ICON.get(plat, "")}</span><b>{e(PLATFORM_NAME.get(plat, plat).upper())}</b><i>{e(w["title"])}</i></div>'
        lab = w['category'].upper()
        meta = ' · '.join(x for x in (w.get('client', ''), str(w.get('year', ''))) if x).upper()
        if w.get('embed'):
            kind = w.get('embed_kind') or 'video'
            meta_e = ' · '.join(x for x in (w.get('client', ''), str(w.get('year', ''))) if x).upper()
            cards.append(f'''<article class="panel work embed embed-{kind}{' wide' if kind in ('video', 'fbpost') else ''}" data-cat="{e(w['category'])}" data-reveal>
  <div class="photo"><iframe data-embed-src="{e(w['embed'])}" title="{e(w['title'])}" loading="lazy" scrolling="{'yes' if kind == 'fbpost' else 'no'}" allow="autoplay; encrypted-media; picture-in-picture; fullscreen; clipboard-write; web-share" allowfullscreen></iframe><span class="embed-wait" aria-hidden="true">{PLATFORM_ICON.get(plat, '')}</span></div>
  <div class="info"><span class="num">{i + 1:02d}</span><div><h3>{e(w['title'])}</h3>{f'<div class="meta" style="margin-top:4px">{e(meta_e)}</div>' if meta_e else ''}</div><span class="chip">{e(PLATFORM_NAME.get(plat, lab))}</span></div>
</article>''')
            continue
        cards.append(f'''<article class="panel work hover brackets{' wide' if is_vid else ''}" data-cat="{e(w['category'])}" data-work data-title="{e(w['title'])}" data-label="{e(lab)}"{f' data-video="{e(w["video"])}"' if w.get('video') else ''}{f' data-embed="{e(w["embed"])}" data-embed-kind="{e(w.get("embed_kind", "video"))}"' if w.get('embed') else ''} data-reveal>
  <div class="photo">{media}{play if is_vid and w.get('embed_kind') != 'post' else ''}</div>
  <div class="info"><span class="num">{i + 1:02d}</span><div><h3>{e(w['title'])}</h3>{f'<div class="meta" style="margin-top:4px">{e(meta)}</div>' if meta else ''}</div><span class="chip">{e(lab)}</span></div>
</article>''')
    if not cards:
        cards.append('<p class="lede">New work coming soon.</p>')
    WORKS_N = len(items)
    body = hero([('index.html', 'HOME'), (None, 'OUR WORKS')], 'PORTFOLIO // SELECTED WORK', [('OUR', False), ('WORKS', True)],
                'Campaigns, causes and brands we’ve helped win. Video, social, creative and brand work produced in-house by one team.',
                f'<a class="btn btn-primary" href="#works">BROWSE WORK {ARROW}</a><a class="btn btn-ghost" href="clients.html">CASE FILES</a>', f'{WORKS_N} PROJECTS')
    body += f'''<section class="section" id="works"><div class="wrap">
{sec_head('SELECTED WORK', 'THE REEL', '<span class="meta"><span id="work-count">00</span> PROJECTS</span>')}
<div class="filters" data-filters="#works-grid" data-counter="#work-count" style="margin-bottom:28px" role="group" aria-label="Filter works">{filt}</div>
<div class="works-grid" id="works-grid">{''.join(cards)}</div>
</div></section>
{ticker(['Creative', 'Video', 'Social', 'Brand', 'TV + CTV', 'Web'], dark=True)}
'''
    body += cta()
    lightbox = '''<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Project preview">
  <button class="lb-btn x" aria-label="Close">×</button><button class="lb-btn prev" aria-label="Previous">‹</button>
  <figure><div class="media"></div><figcaption><span class="cap-t"></span><span class="cap-c" style="color:#FE572E"></span></figcaption></figure>
  <button class="lb-btn next" aria-label="Next">›</button>
</div>'''
    page('our-works.html', 'Our Works | Harris Media Group', 'Selected work from Harris Media Group: video, social, creative and brand for campaigns, causes and advocacy.', 'works', body, extra=lightbox)


if os.environ.get('HMG_SEED'):
    import seed; seed.run(globals()); sys.exit()

import worlds
build_team(); build_profiles(); worlds.build(globals()); build_services(); build_careers(); build_blog(); build_contact(); build_works()
import sn; sn.build(globals())
if CONTENT:
    CM.copy_media(CONTENT, OUT)
print(len(PAGES), 'pages')
