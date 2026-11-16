"""Batch 2 — story-driven worlds for Ted Cruz, Rick Scott, Mike Huckabee, Maine GOP and Linda McMahon."""
import math
from versions import HERO, facts_of
from extra import EXTRA
from pages2 import copy, e

UP = 'https://www.harrismediallc.com/wp-content/uploads/'


# ============================================================ TED CRUZ · V2 — THE POLL CLIMB (an upset, drawn)
def h_pollclimb(c, d, i, n):
    fav = 'M0,90 C120,88 220,80 340,78 S560,74 700,80 S880,92 1000,96'
    dog = 'M0,250 C140,246 240,232 360,205 S560,140 680,104 S860,62 1000,40'
    return f'''<section class="hx hx-poll"><div class="v-grain"></div>
<div class="pl-chart" aria-hidden="true"><svg viewBox="0 0 1000 300" preserveAspectRatio="none">
<g class="pl-grid">{''.join(f'<line x1="0" x2="1000" y1="{y}" y2="{y}"/>' for y in (50, 100, 150, 200, 250))}</g>
<path class="pl-fav" d="{fav}"/><path class="pl-dog" d="{dog}"/></svg>
<span class="pl-lab fav">THE FAVORITE</span><span class="pl-lab dog">THE UNDERDOG</span><span class="pl-x">✕</span><span class="pl-stamp">UPSET</span>
<div class="pl-axis"><span>LAUNCH</span><span>THE CAMPAIGN</span><span>ELECTION NIGHT</span></div><div class="pl-note">Illustration</div></div>
<div class="wrap pl-copy">{copy(c, d, i, n)}</div></section>'''


def sig_meter(c, d):
    ticks = ''.join(f'<i style="--a:{-90 + k * 15}deg"></i>' for k in range(13))
    return f'''<section class="sig sig-meter"><div class="wrap sg-2"><div><span class="v2-k">The underdog meter</span><h2 class="v2-h">Counted out. Then counted in.</h2>
<p class="sig-lede">Many have credited Ted Cruz’s successful use of the web as part of his incredible underdog win. Scroll to watch the needle move.</p></div>
<div class="mt" data-meter aria-hidden="true"><div class="mt-dial">{ticks}<span class="mt-needle"></span><span class="mt-hub"></span></div>
<div class="mt-labs"><span>UNDERDOG</span><span>CONTENDER</span><span>WINNER</span></div><div class="mt-read" data-meter-read>UNDERDOG</div></div></div></section>'''


# ============================================================ TED CRUZ · V3 — SCRATCH TO REVEAL
def h_scratch(c, d, i, n):
    p = d['pal']
    return f'''<section class="hx hx-scratch"><div class="v-grain"></div><div class="wrap sr-grid">
<div class="sr-copy">{copy(c, d, i, n)}</div>
<div class="sr-card" aria-label="Scratch to reveal"><div class="sr-under"><img src="{c['logo']}" alt="{e(c['name'])}"><b>UPSET.</b></div>
<canvas class="sr-cover" data-scratch="{p['fg']},{p['a']}" aria-hidden="true"></canvas><span class="sr-hint">SCRATCH TO REVEAL THE RESULT</span></div></div></section>'''


def sig_months(c, d):
    cells = ''.join(f'<i style="--k:{k}"><b>{k + 1:02d}</b></i>' for k in range(36))
    return f'''<section class="sig sig-months"><div class="wrap sg-2"><div><span class="v2-k">The partnership</span><h2 class="v2-h">Three years. Not one cycle.</h2>
<p class="sig-lede">Vincent Harris spent over three years working with Ted Cruz — and HMG counts the Senator among the U.S. Senators whose digital operations it has run.</p></div>
<div class="mo" data-months aria-label="36 months">{cells}</div></div></section>'''


# ============================================================ RICK SCOTT · V2 — THE RACETRACK
def h_track(c, d, i, n):
    return f'''<section class="hx hx-track"><div class="v-grain"></div>
<div class="tk-wrap" aria-hidden="true"><svg class="tk" viewBox="0 0 1000 520"><ellipse cx="500" cy="260" rx="440" ry="200" class="tk-out"/><ellipse cx="500" cy="260" rx="360" ry="130" class="tk-in"/>
<ellipse cx="500" cy="260" rx="400" ry="165" class="tk-lane"/><line x1="500" y1="35" x2="500" y2="135" class="tk-finish"/></svg>
<canvas class="tk-canvas" data-race></canvas><span class="tk-flash"></span></div>
<div class="wrap tk-copy">{copy(c, d, i, n)}</div><div class="tk-note" aria-hidden="true">● DARK HORSE &nbsp; ○ THE FIELD · illustration</div></section>'''


def sig_finish(c, d):
    return f'''<section class="sig sig-finish"><div class="wrap"><span class="v2-k">Photo finish</span><h2 class="v2-h">It came down to the wire.</h2>
<p class="sig-lede">Rick Scott overcame all odds to narrowly win Florida’s 2010 race for governor. Drag the finish line.</p>
<div class="pf" data-finish><div class="pf-strip"><span class="pf-h a" style="--x:79%">RS</span><span class="pf-h" style="--x:76.5%">·</span><span class="pf-h" style="--x:70%">·</span></div>
<div class="pf-line"><span>FINISH</span></div><input type="range" min="40" max="95" value="60" aria-label="Move the finish line"></div>
<div class="pf-res" data-finish-res>Slide to the line…</div></div></section>'''


# ============================================================ RICK SCOTT · V3 — SPLIT-FLAP BOARD
def h_flapboard(c, d, i, n):
    rows = ['FLORIDA 2010', 'DARK HORSE', 'NARROW WIN', '7 STATES', 'FACEBOOK CASE STUDY']
    board = ''.join(f'<div class="fb-row" data-flap="{r}">' + ''.join('<span class="fb-c"> </span>' for _ in range(20)) + '</div>' for r in rows)
    return f'''<section class="hx hx-flap"><div class="v-grain"></div><div class="wrap fb-grid">
<div class="fb-copy">{copy(c, d, i, n)}</div>
<div class="fb-board" aria-label="{e(' · '.join(rows))}"><div class="fb-head"><span>RACE CONTROL</span><span>STATUS</span></div>{board}<div class="fb-foot"><i></i>FINAL</div></div></div></section>'''


def sig_press(c, d):
    cards = [('FEATURED IN', 'National Review', 'Governor Scott’s innovative use of the web was featured in the National Review.'),
             ('COVERED BY', 'Florida papers & blogs', 'Numerous Florida papers and blogs covered the campaign’s digital work.'),
             ('CASE STUDY BY', 'Facebook corporate', 'The campaign’s innovative use of the web even led to a case study by Facebook corporate.')]
    cc = ''.join(f'<div class="fc" tabindex="0"><div class="fc-in"><div class="fc-f"><span>{a}</span><b>{b}</b><em>Flip ↻</em></div><div class="fc-b"><p>{t}</p></div></div></div>' for a, b, t in cards)
    return f'<section class="sig sig-press"><div class="wrap"><span class="v2-k">The press</span><h2 class="v2-h">A campaign others studied.</h2><div class="fcs">{cc}</div></div></section>'


# ============================================================ HUCKABEE · V2 — THE 2007 BLOG
def h_blog07(c, d, i, n):
    (l1, l2), lede, proof, word, img2 = HERO[c['slug']]
    posts = [('The asterisk', 'From “an asterisk in the polls” — that’s where it started.'), ('Bloggers welcome', 'Blog interviews, organized one conversation at a time.'),
             ('New: microblogging', 'One of the first campaigns to ever use Twitter.')]
    side = ''.join(f'<li><a>{e(t)}</a></li>' for t, _ in posts)
    return f'''<section class="hx hx-blog"><div class="v-grain"></div><div class="wrap">
<div class="bw" data-depth="6"><div class="bw-chrome"><i></i><i></i><i></i><span class="bw-url">http://www.campaign-blog.example/2007/</span><span class="bw-go">Go</span></div>
<div class="bw-page"><div class="bw-banner"><b>✱ THE CAMPAIGN LOG</b><span>posted daily · since 2007</span></div>
<div class="bw-cols"><article class="bw-main">{copy(c, d, i, n)}</article>
<aside class="bw-side"><div class="bw-box"><b>Recent posts</b><ul>{side}</ul></div><div class="bw-box"><b>Visitors</b><div class="bw-ctr" data-hits>000000</div></div>
<div class="bw-box"><img src="{c['logo']}" alt="{e(c['name'])}"></div><div class="bw-badge">RSS · XML</div></aside></div></div></div></div>
<div class="bw-note" aria-hidden="true">A 2007-style campaign blog — illustration</div></section>'''


def sig_micro(c, d):
    st = EXTRA[c['slug']]['steps']
    tl = ['JAN 02, 2008 · 11:04 PM', 'JAN 02, 2008 · 09:18 PM', 'JAN 01, 2008 · 06:40 PM', 'DEC 31, 2007 · 02:15 PM']
    posts = ''.join(f'<article class="mb" data-reveal><div class="mb-h"><span class="mb-av">✱</span><b>campaign_log</b><small>· illustrative</small></div><p><b>{e(t)}</b> — {e(dd)}</p><div class="mb-f"><span>{len(dd)} / 140</span><span>↻ reblog</span></div></article>' for (t, dd) in st)
    return f'''<section class="sig sig-micro"><div class="wrap sg-2"><div><span class="v2-k">Early microblogging</span><h2 class="v2-h">Before “digital strategy” had a name.</h2>
<p class="sig-lede">Blog interviews, a daily online log, one of the first campaigns on Twitter and the Iowa “Blogger Bash” on the eve of the Caucus.</p></div><div class="mbs">{posts}</div></div></section>'''


# ============================================================ HUCKABEE · V3 — ASTERISK TO #1 (99 Iowa counties)
def h_asterisk(c, d, i, n):
    cells = ''.join(f'<i style="--k:{k}"></i>' for k in range(99))
    return f'''<section class="hx hx-ast"><div class="v-grain"></div><div class="wrap as-grid">
<div class="as-copy">{copy(c, d, i, n)}</div>
<div class="as-stage" aria-hidden="true"><div class="as-counties" data-counties>{cells}</div><span class="as-sym">✱</span><span class="as-one">#1</span>
<div class="as-cap"><span>99 IOWA COUNTIES</span><span data-county-read>AN ASTERISK IN THE POLLS</span></div></div></div></section>'''


def sig_book(c, d):
    q = 'Vincent was one of those special young men in whom I see remarkable potential. Humble and polite to the point of being over the top, he was incredibly talented in understanding the power of the Internet and the potential of using a blog to create a daily log of activities and information and to build an online community.'
    return f'''<section class="sig sig-book"><div class="wrap sg-2"><div><span class="v2-k">From the book</span><h2 class="v2-h">“Do the Right Thing,” 2008.</h2>
<p class="sig-lede">Governor Mike Huckabee wrote about the young staffer who helped run his online communications.</p></div>
<div class="bk" data-book><div class="bk-cover"><b>DO THE<br>RIGHT<br>THING</b><span>MIKE HUCKABEE · 2008</span></div><div class="bk-page"><p>“{e(q)}”</p><span>— Gov. Mike Huckabee</span></div></div></div></section>'''


# ============================================================ MAINE GOP · V2 — NAUTICAL CHART
def h_chart(c, d, i, n):
    coast = 'M0,420 C80,400 120,430 170,390 S260,350 300,372 S360,330 410,320 S470,290 520,300 S600,250 640,262 S720,220 770,226 S840,190 900,196 L1000,170'
    return f'''<section class="hx hx-chart"><div class="ch-fog a" aria-hidden="true"></div><div class="ch-fog b" aria-hidden="true"></div><div class="v-grain"></div>
<svg class="ch-map" viewBox="0 0 1000 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<g class="ch-grid">{''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="600"/>' for x in range(0, 1001, 100))}{''.join(f'<line x1="0" y1="{y}" x2="1000" y2="{y}"/>' for y in range(0, 601, 100))}</g>
<path class="ch-coast" d="{coast} L1000,0 L0,0 Z"/><path class="ch-coastline" d="{coast}"/>
<path class="ch-route" d="M140,560 C260,520 380,470 470,430 S620,360 700,300 S790,250 812,236"/>
<g class="ch-buoy" style="--k:0"><circle cx="300" cy="500" r="7"/></g><g class="ch-buoy" style="--k:1"><circle cx="560" cy="400" r="7"/></g>
<g class="ch-port"><circle cx="812" cy="236" r="12"/><text x="830" y="226">AUGUSTA</text><text x="830" y="246" class="sm">44.31° N · 69.78° W</text></g>
<text x="150" y="590" class="sm">TWO YEARS IN MAINE</text></svg>
<div class="ch-rose" aria-hidden="true"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="46"/><path d="M50 4 L56 50 L50 96 L44 50Z"/><path d="M4 50 L50 44 L96 50 L50 56Z" class="o"/><text x="50" y="16">N</text></svg></div>
<div class="wrap ch-copy">{copy(c, d, i, n)}</div></section>'''


def sig_release(c, d):
    return f'''<section class="sig sig-release"><div class="wrap sg-2"><div><span class="v2-k">For immediate release</span><h2 class="v2-h">Augusta, Maine — November 2025.</h2>
<p class="sig-lede">After two years of presence in the state, HMG opened its first dedicated New England office and welcomed Representative Reagan Paul.</p>
<a class="hx-btn" href="blog-hmg-expands-to-new-england-welcomes-representative-reagan-paul-to-lead-regional-growth.html">Read the release →</a></div>
<div class="env" data-env><div class="env-back"></div><div class="env-paper"><span>FOR IMMEDIATE RELEASE</span><b>HMG Expands to New England, Welcomes Representative Reagan Paul to Lead Regional Growth</b>
<p>“Republicans aren’t giving up on New England.” — Vincent Harris</p><i></i><i></i><i></i></div><div class="env-front"></div></div></div></section>'''


# ============================================================ MAINE GOP · V3 — PINES & THE FLAG
def pines(seed, h, step):
    pts = []; x = 0; k = seed
    while x <= 1600:
        k = (k * 9301 + 49297) % 233280; tip = h * (.25 + (k / 233280) * .6)
        pts += [f'{x},{h}', f'{x + step / 2},{h - tip:.0f}']; x += step
    return 'M0,' + str(h) + ' L' + ' L'.join(pts) + f' L1600,{h} Z'


def h_flagplant(c, d, i, n):
    layers = ''.join(f'<svg class="pn-l" style="--k:{k}" data-depth="{(k + 1) * 8}" viewBox="0 0 1600 {200 + k * 40}" preserveAspectRatio="none" aria-hidden="true"><path d="{pines(k * 7 + 3, 200 + k * 40, 70 - k * 12)}"/></svg>' for k in range(4))
    return f'''<section class="hx hx-pines"><div class="pn-sky" aria-hidden="true"></div>{layers}
<div class="pn-flag" aria-hidden="true"><span class="pn-pole"></span><span class="pn-cloth"><b>HMG</b></span><span class="pn-pin">AUGUSTA · NOV 2025</span></div><div class="v-grain"></div>
<div class="wrap pn-copy">{copy(c, d, i, n)}</div></section>'''


def sig_newengland(c, d):
    st = [('ME', 'Maine', 'Maine Republican Party · first dedicated office in Augusta · Gov. LePage’s run in ME-2', 1),
          ('NH', 'New Hampshire', 'State Senate caucus to a supermajority · multiple presidential campaigns', 1),
          ('VT', 'Vermont', '', 0), ('MA', 'Massachusetts', '', 0),
          ('CT', 'Connecticut', 'Statewide campaigns for leaders like Linda McMahon and Bob Stefanowski', 1), ('RI', 'Rhode Island', '', 0)]
    tiles = ''.join(f'<div class="ne-t{" on" if on else ""} ne-{a.lower()}" tabindex="{0 if on else -1}"><b>{a}</b><span>{b}</span>{f"<p>{e(t)}</p>" if t else ""}</div>' for a, b, t, on in st)
    return f'''<section class="sig sig-ne"><div class="wrap sg-2"><div><span class="v2-k">The region</span><h2 class="v2-h">New England, state by state.</h2>
<p class="sig-lede">Hover a lit state to see HMG’s work there.</p></div><div class="ne" data-reveal>{tiles}</div></div></section>'''


# ============================================================ LINDA McMAHON · V2 — CURTAIN & MARQUEE
def h_curtain(c, d, i, n):
    bulbs = ''.join(f'<i style="--k:{k}"></i>' for k in range(44))
    return f'''<section class="hx hx-curtain" data-stage><div class="ct-light" aria-hidden="true"></div>
<div class="ct-l" aria-hidden="true"></div><div class="ct-r" aria-hidden="true"></div><div class="ct-valance" aria-hidden="true"></div><div class="v-grain"></div>
<div class="wrap ct-copy"><div class="ct-marquee"><div class="ct-bulbs" aria-hidden="true">{bulbs}</div>{copy(c, d, i, n)}</div></div>
<div class="ct-floor" aria-hidden="true"></div></section>'''


def sig_counties(c, d):
    cs = ['Litchfield', 'Hartford', 'Tolland', 'Windham', 'Fairfield', 'New Haven', 'Middlesex', 'New London']
    tiles = ''.join(f'<div class="cy" style="--k:{k}"><span>{k + 1:02d}</span><b>{t}</b></div>' for k, t in enumerate(cs))
    return f'''<section class="sig sig-cty"><div class="wrap sg-2"><div><span class="v2-k">Statewide means statewide</span><h2 class="v2-h">Eight counties. One message.</h2>
<p class="sig-lede">A statewide race in Connecticut reaches every county and every media market at once — the kind of program HMG has led for leaders like Linda McMahon.</p></div>
<div class="cty" data-reveal>{tiles}</div></div></section>'''


# ============================================================ LINDA McMAHON · V3 — THE GALLERY
def h_gallery(c, d, i, n):
    return f'''<section class="hx hx-gallery"><div class="gl-room" aria-hidden="true"><span class="gl-floor"></span><span class="gl-wall"></span></div><div class="v-grain"></div>
<div class="wrap gl-grid"><div class="gl-copy">{copy(c, d, i, n)}</div>
<figure class="gl-art" data-depth="10"><div class="gl-lamp"></div><div class="gl-frame"><img src="{c['logo']}" alt="{e(c['name'])}"></div>
<figcaption class="gl-label"><b>Linda McMahon</b><span>Statewide campaigns, Connecticut</span><em>Harris Media Group · Collection</em><small>Room 10 · New England</small></figcaption></figure></div></section>'''


def sig_exhibit(c, d):
    st = EXTRA[c['slug']]['steps']
    frames = ''.join(f'<figure class="ex-f" style="--k:{k}"><div class="ex-in"><span>{k + 1:02d}</span><h3>{e(t)}</h3><p>{e(dd)}</p></div><figcaption>Plate {k + 1} · {e(t.split("·")[0].strip().title())}</figcaption></figure>' for k, (t, dd) in enumerate(st))
    return f'''<section class="sig sig-exhibit"><div class="wrap"><span class="v2-k">The exhibition</span><h2 class="v2-h">A statewide show, in four acts.</h2>
<p class="sig-lede">Drag or scroll sideways through the gallery.</p></div><div class="ex" data-dragscroll>{frames}</div></section>'''


HEROES2 = dict(pollclimb=h_pollclimb, scratch=h_scratch, track=h_track, flapboard=h_flapboard, blog07=h_blog07,
               asterisk=h_asterisk, chart=h_chart, flagplant=h_flagplant, curtain=h_curtain, gallery=h_gallery)
SIGS2 = dict(meter=sig_meter, months=sig_months, finish=sig_finish, press=sig_press, micro=sig_micro, book=sig_book,
             release=sig_release, newengland=sig_newengland, counties=sig_counties, exhibit=sig_exhibit)
