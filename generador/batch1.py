"""Batch 1 — ten one-of-a-kind heroes and signature sections (Right for America, Likud, NH Senate, Suarez, Rand Paul)."""
import html as H, json, math, random
from versions import HERO, facts_of
from extra import EXTRA
from pages2 import copy, e

UP = 'https://www.harrismediallc.com/wp-content/uploads/'


# =========================================================== RIGHT FOR AMERICA · V2 — AD WALL
def h_adwall(c, d, i, n):
    labels = ['SEARCH', 'YOUTUBE', 'FACEBOOK', 'INSTAGRAM', 'DISPLAY', 'CTV', 'SEARCH', 'REELS', 'FEED', 'PRE-ROLL', 'STORIES', 'GOOGLE']
    pos = ['50% 20%', '30% 30%', '70% 25%', '50% 60%', '20% 15%', '80% 40%', '45% 35%', '60% 10%', '35% 55%', '55% 45%', '25% 40%', '75% 20%']
    screens = ''.join(f'<div class="aw-s" style="--i:{k};--pos:{pos[k]}"><img src="{c["logo"]}" alt="" loading="eager"><span class="aw-l">{labels[k]}</span><span class="aw-live">● LIVE</span></div>' for k in range(12))
    return f'''<section class="hx hx-adwall"><div class="aw-wall" aria-hidden="true">{screens}</div><div class="aw-shade" aria-hidden="true"></div><div class="v-grain"></div>
<div class="wrap aw-copy">{copy(c, d, i, n)}</div><div class="aw-tag" aria-hidden="true">AD WALL · 2024 PRESIDENTIAL CYCLE</div></section>'''


def sig_mixer(c, d):
    g = ['Search', 'YouTube', 'Display', 'Pre-roll']; m = ['Facebook', 'Instagram', 'Reels', 'Stories']
    col = lambda name, items: f'<div class="mx-col" data-reveal><div class="mx-big">{name}</div><ul>' + ''.join(f'<li style="--k:{k}"><i></i>{t}</li>' for k, t in enumerate(items)) + '</ul></div>'
    return f'''<section class="sig sig-mixer"><div class="wrap"><span class="v2-k">Channel mixer</span><h2 class="v2-h">Two platforms. Every placement.</h2>
<p class="sig-lede">By the end of the 2024 Presidential cycle, Right for America was among the largest spenders on Google and Meta in the entire race.</p>
<div class="mx">{col('GOOGLE', g)}{col('META', m)}</div></div></section>'''


# =========================================================== RIGHT FOR AMERICA · V3 — WAVING FLAG
def h_flag(c, d, i, n):
    p = d['pal']
    return f'''<section class="hx hx-flag"><canvas class="fl-canvas" data-flag="{p['a']},{p['fg']},{p['a2']}" aria-hidden="true"></canvas><div class="v-grain"></div>
<div class="wrap fl-copy">{copy(c, d, i, n)}</div><div class="fl-hint" aria-hidden="true">MOVE TO CHANGE THE WIND</div></section>'''


def sig_stars(c, d):
    stars = ''.join(f'<i style="--k:{k}">★</i>' for k in range(50))
    return f'''<section class="sig sig-stars"><div class="wrap sg-2"><div><span class="v2-k">Every state</span><h2 class="v2-h">Every state.<br>Every screen.</h2>
<p class="sig-lede">A national presidential electorate, reached platform by platform — strategy, creative and paid media run by one team.</p></div>
<div class="st-grid" data-starfill aria-hidden="true">{stars}</div></div></section>'''


# =========================================================== LIKUD · V2 — CHAT STREAM
CHATS = ['Shalom! Ready to make a few calls today?', 'Yes, how does it work?', 'I’ll connect you with voters near you.', 'Calling now 📞', 'Thank you — every call counts.',
         'Can I call from Telegram?', 'Of course. Tap to start.', 'Done! Who’s next?', 'You reached 5 voters today.', 'Send me more numbers',
         'Great job! Share with a friend?', 'On Facebook too?', 'Yes — same bot, same mission.', 'Let’s go!']


def h_chatstream(c, d, i, n):
    cols = ''
    for k in range(4):
        msgs = CHATS[k::2] + CHATS[:k + 3]
        b = ''.join(f'<div class="cs-b{" me" if (j + k) % 2 else ""}">{e(t)}</div>' for j, t in enumerate(msgs))
        cols += f'<div class="cs-col" style="--d:{38 + k * 7}s;--o:{k * -9}s"><div class="cs-in">{b}{b}</div></div>'
    return f'''<section class="hx hx-chat"><div class="cs-cols" aria-hidden="true">{cols}</div><div class="cs-fade" aria-hidden="true"></div><div class="v-grain"></div>
<div class="wrap cs-copy"><div class="cs-card">{copy(c, d, i, n)}</div><div class="cs-note">Background conversation is illustrative</div></div></section>'''


def sig_calls(c, d):
    return f'''<section class="sig sig-calls"><div class="wrap"><span class="v2-k">From chat to call</span><h2 class="v2-h">16,999 voters picked up the phone.</h2>
<div class="cl-row">
  <div class="cl" data-reveal><div class="cl-top"><span class="cl-ico">✈</span>TELEGRAM</div><div class="cl-n"><span data-count="8323">0</span></div><div class="cl-bar"><i style="--w:49%"></i></div></div>
  <div class="cl" data-reveal><div class="cl-top"><span class="cl-ico">f</span>FACEBOOK</div><div class="cl-n"><span data-count="8676">0</span></div><div class="cl-bar"><i style="--w:51%"></i></div></div>
  <div class="cl tot" data-reveal><div class="cl-top">TOTAL VOTERS MOBILIZED</div><div class="cl-n"><span data-count="16999">0</span></div><div class="cl-bar"><i style="--w:100%"></i></div></div>
</div></div></section>'''


# =========================================================== LIKUD · V3 — NETWORK GRAPH
def h_network(c, d, i, n):
    p = d['pal']
    return f'''<section class="hx hx-net"><canvas class="nt-canvas" data-net="{p['a']},{p['a2']},{p['fg']}" aria-hidden="true"></canvas><div class="v-grain"></div>
<div class="wrap nt-copy">{copy(c, d, i, n)}</div>
<div class="nt-legend" aria-hidden="true"><span><i style="background:{p['a']}"></i>TELEGRAM</span><span><i style="background:{p['a2']}"></i>FACEBOOK</span><span>● AI HUB</span></div></section>'''


def sig_donut(c, d):
    p = d['pal']; tg = 8323 / 16999
    C = 2 * math.pi * 90
    return f'''<section class="sig sig-donut"><div class="wrap sg-2"><div class="dn-wrap" data-reveal>
<svg viewBox="0 0 220 220" class="dn"><circle cx="110" cy="110" r="90" class="dn-bg"/>
<circle cx="110" cy="110" r="90" class="dn-a" style="stroke:{p['a']};--len:{C * tg:.1f};--c:{C:.1f}"/>
<circle cx="110" cy="110" r="90" class="dn-b" style="stroke:{p['a2']};--len:{C * (1 - tg):.1f};--c:{C:.1f};--off:{-C * tg:.1f}"/></svg>
<div class="dn-mid"><b data-count="16999">0</b><span>VOTERS</span></div></div>
<div><span class="v2-k">The split</span><h2 class="v2-h">Two channels, almost even.</h2>
<ul class="dn-leg"><li><i style="background:{p['a']}"></i><b>8,323</b> voters calling through Telegram</li><li><i style="background:{p['a2']}"></i><b>8,676</b> voters calling through Facebook</li></ul></div></div></section>'''


# =========================================================== NH SENATE · V2 — TOPOGRAPHIC MAP
def topo_svg(seed=7):
    rnd = random.Random(seed); paths = []
    for ring in range(1, 15):
        cx, cy = 820 + rnd.uniform(-30, 30), 360 + rnd.uniform(-20, 20)
        pts = []
        for a in range(0, 361, 10):
            t = math.radians(a)
            r = ring * 34 * (1 + 0.18 * math.sin(3 * t + ring * .4) + 0.1 * math.cos(5 * t + ring))
            pts.append(f'{cx + r * math.cos(t):.1f},{cy + r * math.sin(t) * .62:.1f}')
        paths.append(f'<path d="M{" L".join(pts)}Z" style="--k:{ring}"/>')
    return ''.join(paths)


def h_topo(c, d, i, n):
    pins = [(62, 30, 'D-1'), (74, 52, 'D-2'), (55, 64, 'D-3'), (82, 34, 'D-4'), (68, 76, 'D-5')]
    pp = ''.join(f'<span class="tp-pin" style="left:{x}%;top:{y}%;--k:{k}"><i></i>{lab}</span>' for k, (x, y, lab) in enumerate(pins))
    return f'''<section class="hx hx-topo" data-topo><svg class="tp-map" viewBox="0 0 1600 760" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{topo_svg()}</svg>
<div class="tp-pins" aria-hidden="true">{pp}</div><div class="tp-read" aria-hidden="true">43.2081° N · 71.5376° W</div><div class="v-grain"></div>
<div class="wrap tp-copy">{copy(c, d, i, n)}</div></section>'''


def sig_funnel(c, d):
    layers = [('NEW HAMPSHIRE', 'The whole state'), ('THE SENATE MAP', 'The districts that decide the majority'),
              ('DECISIVE VOTERS', 'Persuadable and low-propensity voters'), ('THE TARGET', 'Every impression lands where it can move the outcome')]
    ll = ''.join(f'<div class="fn-l" style="--w:{100 - k * 22}%;--k:{k}"><b>{a}</b><span>{b}</span></div>' for k, (a, b) in enumerate(layers))
    return f'''<section class="sig sig-funnel"><div class="wrap"><span class="v2-k">How targeting works</span><h2 class="v2-h">From a whole state to the voters who decide it.</h2>
<div class="fn" data-reveal>{ll}</div></div></section>'''


# =========================================================== NH SENATE · V3 — SCOPE
def scope_svg():
    grid = ''.join(f'<line class="gridl" x1="{x}" y1="0" x2="{x}" y2="760"/>' for x in range(0, 1601, 80)) + ''.join(f'<line class="gridl" x1="0" y1="{y}" x2="1600" y2="{y}"/>' for y in range(0, 761, 80))
    tg = ''.join(f'<g class="tgt"><circle cx="{x}" cy="{y}" r="16"/><circle cx="{x}" cy="{y}" r="4"/><text x="{x + 24}" y="{y + 5}">{lab}</text></g>'
                 for x, y, lab in [(980, 210, 'DISTRICT 01'), (1180, 330, 'DISTRICT 02'), (860, 420, 'DISTRICT 03'), (1320, 520, 'DISTRICT 04'), (1060, 600, 'DISTRICT 05')])
    return f'<svg viewBox="0 0 1600 760" preserveAspectRatio="xMidYMid slice">{grid}{topo_svg(11)}{tg}</svg>'


def h_scope(c, d, i, n):
    ticks = ''.join(f'<i style="--a:{a}deg"></i>' for a in range(0, 360, 15))
    m = scope_svg()
    return f'''<section class="hx hx-scope" data-scope><div class="scp-bg vec" aria-hidden="true"><div class="scp-map">{m}</div></div>
<div class="scp-ret" aria-hidden="true"><div class="scp-view vec"><div class="scp-map">{m}</div></div><div class="scp-ticks">{ticks}</div><span class="scp-h"></span><span class="scp-v"></span><b class="scp-rng">RNG 0420</b></div>
<div class="v-grain"></div><div class="wrap scp-copy">{copy(c, d, i, n)}</div><div class="scp-status" aria-hidden="true">● SCANNING</div></section>'''


def sig_plaque(c, d):
    return f'''<section class="sig sig-plaque"><div class="wrap sg-2"><div><span class="v2-k">The award</span><h2 class="v2-h">Recognized for precision.</h2>
<p class="sig-lede">The program earned the award for Best Use of Online Targeting for a State Legislative Campaign — and a caucus that grew to a supermajority over three cycles.</p></div>
<div class="pq" data-tilt><div class="pq-in"><span class="pq-star">★</span><span class="pq-y">2025</span><b>BEST USE OF ONLINE TARGETING</b><span>FOR A STATE LEGISLATIVE CAMPAIGN</span><em>New Hampshire Senate Republicans · Harris Media Group</em></div></div></div></section>'''


# =========================================================== SUAREZ · V2 — DESKTOP OS
def h_desktop(c, d, i, n):
    (l1, l2), lede, proof, word, img2 = HERO[c['slug']]
    win = lambda cls, title, body, x, y, w: f'<div class="os-w {cls}" style="--x:{x}%;--y:{y}px;--w:{w}px" data-drag><div class="os-bar"><i></i><i></i><i></i><span>{title}</span></div><div class="os-body">{body}</div></div>'
    return f'''<section class="hx hx-desk"><div class="os-sun" aria-hidden="true"></div><div class="v-grain"></div>
<div class="os-desk">
{win('main', 'sos_america.case', copy(c, d, i, n), 4, 170, 640)}
{win('pic', 'campaign.jpg', f'<img src="{c["logo"]}" alt="{e(c["name"])}">', 60, 160, 300)}
{win('ai', 'ask_ai_suarez.app', f'<img src="{img2}" alt="Ask AI Suarez experience">', 66, 470, 340)}
{win('note', 'award.txt', '<p><b>AAPC 2024</b><br>Campaign Excellence Award<br>— Digital Campaign of the Year —</p>', 48, 560, 250)}
</div><div class="os-dock" aria-hidden="true"><span>◐</span><span>✉</span><span>★</span><span>♫</span><span>⌘</span></div>
<div class="os-hint" aria-hidden="true">DRAG THE WINDOWS</div></section>'''


def sig_aichat(c, d):
    qa = [('What is SOS America PAC?', 'The Super PAC that supported Miami Mayor Francis Suarez’s presidential run.'),
          ('What did the digital program win?', 'The 2024 AAPC Campaign Excellence Award for Digital Campaign of the Year.'),
          ('What was “Ask AI Suarez”?', 'An AI-powered experience featured in the award-winning case.')]
    msgs = ''.join(f'<div class="msg ai-m me">{e(q)}</div><div class="msg ai-m bot">{e(a)}</div>' for q, a in qa)
    return f'''<section class="sig sig-aichat"><div class="wrap sg-2"><div><span class="v2-k">Ask the case</span><h2 class="v2-h">An AI campaign, explained by AI.</h2>
<p class="sig-lede">Illustrative demo — answers summarize the case, not the candidate’s words.</p></div>
<div class="ai-box" data-chat><div class="ai-head"><span>✦</span>ASK THE CASE</div>{msgs}<div class="typing" style="display:none"><i></i><i></i><i></i></div></div></div></section>'''


# =========================================================== SUAREZ · V3 — TROPHY RING
def h_ring(c, d, i, n):
    txt = 'DIGITAL CAMPAIGN OF THE YEAR · AAPC 2024 · '
    N = len(txt)
    letters = ''.join(f'<span style="--r:{k * 360 / N:.2f}deg">{e(ch)}</span>' for k, ch in enumerate(txt))
    return f'''<section class="hx hx-ring"><div class="v-grain"></div><div class="wrap rg-grid">
<div class="rg-copy">{copy(c, d, i, n)}</div>
<div class="rg-stage" data-ring aria-hidden="true"><div class="rg-photo"><img src="{c['logo']}" alt=""></div><div class="rg-ring">{letters}</div><div class="rg-ring b">{letters}</div><div class="rg-glow"></div></div>
</div></section>'''


def sig_confetti(c, d):
    p = d['pal']
    return f'''<section class="sig sig-confetti"><canvas class="cf-canvas" data-confetti="{p['a']},{p['a2']},{p['fg']}" aria-hidden="true"></canvas><div class="wrap cf-in">
<span class="v2-k">The win</span><div class="cf-card" data-reveal><span>AAPC · 2024</span><b>DIGITAL CAMPAIGN OF THE YEAR</b><em>SOS America PAC · Francis Suarez</em></div>
<button class="hx-btn solid" type="button" data-burst>Celebrate the win ✦</button></div></section>'''


# =========================================================== RAND PAUL · V2 — LIBERTY POSTER
def h_poster(c, d, i, n):
    return f'''<section class="hx hx-poster" data-rays><div class="ps-rays" aria-hidden="true"></div><div class="v-grain"></div>
<div class="wrap ps-grid"><div class="ps-copy">{copy(c, d, i, n)}</div>
<figure class="ps-photo"><div class="ps-half" style="--img:url('{c['logo']}')" role="img" aria-label="{e(c['name'])}"></div><span class="ps-stamp">INTERNET<br>ARMY<small>· 2016 ·</small></span></figure></div>
<div class="ps-band" aria-hidden="true">★ LIBERTY ★ DIGITAL ★ 2016 ★ LIBERTY ★ DIGITAL ★ 2016 ★ LIBERTY ★ DIGITAL ★ 2016 ★</div></section>'''


def sig_pamphlet(c, d):
    st = EXTRA[c['slug']]['steps']
    panels = ''.join(f'<div class="pm-p" style="--k:{k}"><span class="pm-n">{k + 1:02d}</span><h3>{e(t)}</h3><p>{e(dd)}</p></div>' for k, (t, dd) in enumerate(st))
    return f'''<section class="sig sig-pamphlet"><div class="wrap"><span class="v2-k">The pamphlet</span><h2 class="v2-h">How an internet army is built.</h2>
<div class="pm" data-unfold>{panels}</div></div></section>'''


# =========================================================== RAND PAUL · V3 — THE ARMY
def h_army(c, d, i, n):
    p = d['pal']
    return f'''<section class="hx hx-army"><canvas class="ar-canvas" data-army="{p['a']},{p['a2']},{p['fg']}" aria-hidden="true"></canvas><div class="v-grain"></div>
<div class="wrap ar-copy">{copy(c, d, i, n)}</div><div class="ar-count" aria-hidden="true">RECRUITING<b data-armycount>0000</b><small>illustration</small></div></section>'''


def sig_feed(c, d):
    x = EXTRA[c['slug']]
    posts = [(t, dd) for t, dd in x['steps']] + [(l.upper(), v) for v, l in facts_of(c['slug'])]
    cards = ''.join(f'<article class="fd-c"><div class="fd-h"><span class="fd-av">HMG</span><b>Harris Media</b><small>@hmg · campaign log</small></div><h3>{e(t)}</h3><p>{e(dd)}</p><div class="fd-a"><span>↺ share</span><span>♡</span><span>↗</span></div></article>' for t, dd in posts)
    return f'''<section class="sig sig-feed"><div class="wrap sg-2"><div><span class="v2-k">The feed</span><h2 class="v2-h">A campaign that lived online.</h2>
<p class="sig-lede">Politico called it Rand Paul’s internet army: a social presence, a recruiting engine and a content machine running every day.</p></div>
<div class="fd" aria-label="Campaign feed"><div class="fd-in">{cards}{cards}</div></div></div></section>'''


HEROES1 = dict(adwall=h_adwall, flag=h_flag, chatstream=h_chatstream, network=h_network, topo=h_topo, scope=h_scope,
               desktop=h_desktop, ring=h_ring, poster=h_poster, army=h_army)
SIGS1 = dict(mixer=sig_mixer, stars=sig_stars, calls=sig_calls, donut=sig_donut, funnel=sig_funnel, plaque=sig_plaque,
             aichat=sig_aichat, confetti=sig_confetti, pamphlet=sig_pamphlet, feed=sig_feed)
