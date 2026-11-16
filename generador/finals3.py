"""Story modules for the last five finals (VHHA, TXOGA, Dan Patrick, Sarah Palin, Doug Collins).
Every module here is used by exactly one page."""
import html as H, math
from extra import EXTRA, SV

e = lambda s: H.escape(str(s), quote=True)
steps = lambda c: EXTRA[c['slug']]['steps']
brief = lambda c: EXTRA[c['slug']]['brief']
svcs = lambda c: EXTRA[c['slug']]['services']
closing = lambda c: EXTRA[c['slug']]['closing']


# ===================================================================== VHHA — the clinic
def vh_chart(c, d):
    k, title, paras = brief(c)
    rows = [('ORGANIZATION', 'Virginia Hospital & Healthcare Association'), ('SCOPE', 'Statewide'), ('SECTOR', 'Healthcare advocacy'), ('STATUS', 'Measurable growth')]
    fields = ''.join(f'<div class="vc-f"><span>{a}</span><b>{e(b)}</b></div>' for a, b in rows)
    return f'''<section class="vh-chart-s"><div class="wrap"><div class="vc" data-reveal>
<div class="vc-clip" aria-hidden="true"></div><div class="vc-head"><span>CASE CHART</span><b>{e(title)}</b></div>
<svg class="vc-ecg" viewBox="0 0 600 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 30 H120 L135 30 L145 8 L160 52 L172 30 H300 L315 30 L325 12 L340 48 L352 30 H600"/></svg>
<div class="vc-fields">{fields}</div><div class="vc-notes"><span>CLINICAL NOTES</span>{''.join(f'<p>{e(p)}</p>' for p in paras)}</div></div></div></section>'''


def vh_monitors(c, d):
    waves = ['M0 30 H40 L48 30 L54 6 L62 54 L68 30 H120 L128 30 L134 6 L142 54 L148 30 H200',
             'M0 40 C20 40 25 10 40 10 S60 40 80 40 S105 10 120 10 S140 40 160 40 S185 10 200 10',
             'M0 30 Q25 5 50 30 T100 30 T150 30 T200 30',
             'M0 45 L20 45 L30 15 L45 45 L70 45 L80 15 L95 45 L120 45 L130 15 L145 45 L170 45 L180 15 L195 45']
    labs = ['ECG', 'SpO₂', 'RESP', 'NIBP']
    cards = ''.join(f'''<article class="vm" data-reveal><div class="vm-top"><span>{labs[k]}</span><i></i></div>
<svg viewBox="0 0 200 60" preserveAspectRatio="none" aria-hidden="true"><path d="{waves[k]}"/></svg><h3>{e(t)}</h3><p>{e(dd)}</p></article>''' for k, (t, dd) in enumerate(steps(c)))
    return f'<section class="vh-mon"><div class="wrap"><span class="v2-k">Treatment plan</span><h2 class="v2-h">Four vitals we watch.</h2><div class="vm-grid">{cards}</div></div></section>'


def vh_rx(c, d):
    items = ''.join(f'<li><a href="services.html#{SV[s]}"><b>℞</b>{e(s)}<em>as needed · statewide</em></a></li>' for s in svcs(c))
    return f'''<section class="vh-rx-s"><div class="wrap"><div class="rx" data-reveal><div class="rx-head"><b>Harris Media Group</b><span>Digital practice · Texas · Florida · New England</span></div>
<div class="rx-pt">Patient: <u>Virginia Hospital &amp; Healthcare Association</u></div><ol>{items}</ol><div class="rx-sig">Prescribed by HMG</div></div></div></section>'''


def vh_pulse(c, d):
    return f'''<section class="vh-pulse-s"><div class="wrap"><p class="vp-txt">{e(closing(c))}</p>
<svg class="vp-line" viewBox="0 0 1200 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 60 H420 L440 60 L455 10 L475 110 L490 60 L505 60 L515 35 L530 80 L540 60 H1200"/></svg>
<div class="vp-bpm"><i></i> PULSE · STEADY</div></div></section>'''


# ===================================================================== TXOGA — the plant
def tx_blueprint(c, d):
    k, title, paras = brief(c)
    return f'''<section class="tx-bp"><div class="wrap"><div class="bp" data-reveal>
<span class="bp-dim h" aria-hidden="true"><i>SPEC 01</i></span><span class="bp-dim v" aria-hidden="true"><i>TXOGA</i></span>
<div class="bp-title"><span>DRAWING NO. HMG-TX-01 · ENERGY ADVOCACY</span><h2>{e(title)}</h2></div>
<div class="bp-body">{''.join(f'<p>{e(p)}</p>' for p in paras)}</div>
<div class="bp-stamp"><b>APPROVED</b><span>HARRIS MEDIA GROUP</span></div></div></div></section>'''


def tx_pipeline(c, d):
    st = steps(c)
    valves = ''.join(f'<div class="pv" data-valve="{(k + .6) / len(st):.2f}"><div class="pv-wheel" aria-hidden="true"><i></i><i></i></div><span class="pv-n">{k + 1:02d}</span><h3>{e(t.split("·")[-1].strip())}</h3><p>{e(dd)}</p></div>' for k, (t, dd) in enumerate(st))
    return f'''<section class="tx-pipe" data-pipe><div class="wrap"><span class="v2-k">The line</span><h2 class="v2-h">Four stages. One flow.</h2>
<div class="pp"><div class="pp-tube" aria-hidden="true"><span class="pp-flow"></span></div><div class="pp-valves">{valves}</div></div></div></section>'''


def tx_switches(c, d):
    sw = ''.join(f'<a class="sw-r" href="services.html#{SV[s]}" style="--k:{k}"><span class="sw-led"></span><span class="sw-t">{e(s)}</span><span class="sw-tg"><i></i></span></a>' for k, s in enumerate(svcs(c)))
    return f'<section class="tx-sw"><div class="wrap"><div class="cp" data-reveal><div class="cp-head"><span>CONTROL PANEL</span><span>ALL SYSTEMS · ON</span></div>{sw}</div></div></section>'


def tx_tank(c, d):
    return f'''<section class="tx-tank" data-fill><div class="wrap tk-g"><div class="tk-cyl" aria-hidden="true"><span class="tk-lvl"></span><span class="tk-marks"></span></div>
<p class="tk-txt">{e(closing(c))}</p></div></section>'''


# ===================================================================== DAN PATRICK — the capitol
def dp_proclaim(c, d):
    k, title, paras = brief(c)
    return f'''<section class="dp-pr"><div class="wrap"><div class="pr" data-reveal><div class="pr-seal" aria-hidden="true"><span>★</span></div>
<span class="pr-k">BE IT KNOWN</span><h2>{e(title)}</h2>{''.join(f'<p>{e(p)}</p>' for p in paras)}<div class="pr-sign"><span>Harris Media Group</span><span>Austin · Texas</span></div></div></div></section>'''.replace('Austin · Texas', 'State of Texas')


def dp_rotunda(c, d):
    tl = EXTRA[c['slug']]['timeline']
    n = len(tl)
    items = ''.join(f'<div class="rt-i" style="--a:{180 + (k + .5) * 180 / n:.1f}deg"><b>{e(y)}</b><h3>{e(t)}</h3><p>{e(dd)}</p></div>' for k, (y, t, dd) in enumerate(tl))
    return f'''<section class="dp-rot"><div class="wrap"><span class="v2-k">HMG in Texas</span><h2 class="v2-h">A history under one dome.</h2>
<div class="rt" data-reveal><svg class="rt-dome" viewBox="0 0 600 300" aria-hidden="true"><path d="M20 300 A280 280 0 0 1 580 300"/><path d="M90 300 A210 210 0 0 1 510 300"/>
{''.join(f'<line x1="300" y1="300" x2="{300 + 280 * math.cos(math.radians(180 + a)):.0f}" y2="{300 + 280 * math.sin(math.radians(180 + a)):.0f}"/>' for a in range(15, 180, 30))}</svg><div class="rt-items">{items}</div></div></div></section>'''


def dp_columns(c, d):
    cols = ''.join(f'<div class="cl-c" style="--k:{k}"><div class="cl-cap"></div><div class="cl-shaft"><span>{k + 1:02d}</span><h3>{e(t)}</h3><p>{e(dd)}</p></div><div class="cl-base"></div></div>' for k, (t, dd) in enumerate(steps(c)))
    return f'<section class="dp-col"><div class="wrap"><span class="v2-k">The playbook</span><h2 class="v2-h">Four columns of a Texas program.</h2><div class="cl-row" data-reveal><div class="cl-ped" aria-hidden="true"></div>{cols}</div></div></section>'


def dp_seals(c, d):
    seals = ''.join(f'<a class="sl" href="services.html#{SV[s]}" style="--k:{k}"><svg viewBox="0 0 120 120" aria-hidden="true"><defs><path id="sp{k}" d="M60 60 m-44 0 a44 44 0 1 1 88 0 a44 44 0 1 1 -88 0"/></defs><text><textPath href="#sp{k}">HARRIS MEDIA GROUP · TEXAS · </textPath></text></svg><b>{e(s)}</b></a>' for k, s in enumerate(svcs(c)))
    return f'<section class="dp-seal"><div class="wrap"><span class="v2-k">Disciplines deployed</span><div class="sl-row">{seals}</div></div></section>'


def dp_constellation(c, d):
    pts = [(300, 20), (370, 220), (580, 220), (410, 340), (480, 560), (300, 430), (120, 560), (190, 340), (20, 220), (230, 220), (300, 20)]
    path = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
    stars = ''.join(f'<circle cx="{x}" cy="{y}" r="5"/>' for x, y in pts[:-1])
    return f'''<section class="dp-cons" data-scrub-host><div class="wrap cs-g"><svg class="cs-svg" viewBox="0 0 600 580" aria-hidden="true"><path data-scrub d="{path}"/>{stars}</svg>
<p class="cs-txt">{e(closing(c))}</p></div></section>'''


# ===================================================================== SARAH PALIN — the frontier
def pl_journal(c, d):
    k, title, paras = brief(c)
    return f'''<section class="pl-jr"><div class="wrap"><div class="jr" data-reveal><div class="jr-l"><span class="jr-date">FIELD NOTES · THE LAST FRONTIER</span><h2>{e(title)}</h2>
<svg class="jr-comp" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="44"/><path d="M50 10 L57 50 L50 90 L43 50Z"/><text x="50" y="8">N</text></svg></div>
<div class="jr-r">{''.join(f'<p>{e(p)}</p>' for p in paras)}<span class="jr-pin">64.2° N · 149.5° W · ALASKA</span></div></div></div></section>'''


def pl_summits(c, d):
    st = steps(c)
    peaks = [(80, 300), (300, 220), (520, 140), (740, 60)]
    ridge = 'M0 360 L80 300 L190 330 L300 220 L410 260 L520 140 L630 190 L740 60 L860 360 Z'
    flags = ''.join(f'<g class="sm-f" style="--k:{k}"><line x1="{x}" y1="{y}" x2="{x}" y2="{y - 46}"/><path d="M{x} {y - 46} l30 9 l-30 9z"/></g>' for k, (x, y) in enumerate(peaks))
    cards = ''.join(f'<div class="sm-c" data-peak="{(k + .5) / len(st):.2f}"><span>SUMMIT {k + 1:02d}</span><h3>{e(t)}</h3><p>{e(dd)}</p></div>' for k, (t, dd) in enumerate(st))
    return f'''<section class="pl-sum" data-summits><div class="wrap"><span class="v2-k">The climb</span><h2 class="v2-h">Four summits.</h2>
<svg class="sm-svg" viewBox="0 0 860 360" preserveAspectRatio="none" aria-hidden="true"><path class="sm-ridge" d="{ridge}"/>{flags}<circle class="sm-me" r="9" cx="0" cy="360"/></svg>
<div class="sm-row">{cards}</div></div></section>'''


def pl_signs(c, d):
    signs = ''.join(f'<a class="sg" href="services.html#{SV[s]}" style="--r:{(-6, 5, -3, 7)[k % 4]}deg;--k:{k}">{e(s)} <span>→</span></a>' for k, s in enumerate(svcs(c)))
    return f'<section class="pl-sg"><div class="wrap sg-wrap"><div class="sg-post" aria-hidden="true"></div><div class="sg-list">{signs}</div><div><span class="v2-k">Trail signs</span><h2 class="v2-h">The team behind it.</h2></div></div></section>'


def pl_aurora(c, d):
    return f'<section class="pl-au"><div class="wrap"><p class="au-txt">{e(closing(c))}</p></div></section>'


# ===================================================================== DOUG COLLINS — the edit bay
def dg_script(c, d):
    k, title, paras = brief(c)
    return f'''<section class="dg-sc"><div class="wrap"><div class="scr" data-reveal><div class="scr-pg">1.</div>
<p class="scr-slug">INT. HMG EDIT BAY — NIGHT</p><p class="scr-act">{e(paras[0])}</p>
<p class="scr-char">HARRIS MEDIA GROUP</p><p class="scr-par">(leaning into the monitor)</p><p class="scr-dia">{e(title.title())}.</p>
<p class="scr-act">{e(paras[1] if len(paras) > 1 else '')}</p><p class="scr-trans">CUT TO:</p></div></div></section>'''


def dg_timeline(c, d):
    st = steps(c)
    clips = ''.join(f'<div class="nl-clip" style="--k:{k}"><b>{e(t.split("·")[-1].strip())}</b></div>' for k, (t, dd) in enumerate(st))
    notes = ''.join(f'<div class="nl-note" data-clip="{(k + .5) / len(st):.2f}"><span>CLIP {k + 1:02d}</span><p>{e(dd)}</p></div>' for k, (t, dd) in enumerate(st))
    return f'''<section class="dg-nle" data-nle><div class="wrap"><span class="v2-k">The edit</span><h2 class="v2-h">On the timeline.</h2>
<div class="nl"><div class="nl-ruler" aria-hidden="true">{''.join(f'<i>00:{s:02d}</i>' for s in range(0, 60, 10))}</div>
<div class="nl-track"><span class="nl-lab">V1</span><div class="nl-lane">{clips}</div></div>
<div class="nl-track a"><span class="nl-lab">A1</span><div class="nl-lane"><div class="nl-wave"></div></div></div><span class="nl-head" aria-hidden="true"></span></div>
<div class="nl-notes">{notes}</div></div></section>'''


def dg_cans(c, d):
    cans = ''.join(f'<a class="can" href="services.html#{SV[s]}" style="--k:{k}"><span class="can-reel" aria-hidden="true"></span><b>{e(s)}</b><small>REEL {k + 1:02d}</small></a>' for k, s in enumerate(svcs(c)))
    return f'<section class="dg-can"><div class="wrap"><span class="v2-k">In the vault</span><h2 class="v2-h">The reels behind the spot.</h2><div class="can-row">{cans}</div></div></section>'


def dg_leader(c, d):
    return f'''<section class="dg-ld" data-leader><div class="ld-box" aria-hidden="true"><span class="ld-sweep"></span><span class="ld-cross"></span><b class="ld-n">3</b></div>
<div class="wrap"><p class="ld-txt">{e(closing(c))}</p></div></section>'''


MODULES3 = dict(vh_chart=vh_chart, vh_monitors=vh_monitors, vh_rx=vh_rx, vh_pulse=vh_pulse,
                tx_blueprint=tx_blueprint, tx_pipeline=tx_pipeline, tx_switches=tx_switches, tx_tank=tx_tank,
                dp_proclaim=dp_proclaim, dp_rotunda=dp_rotunda, dp_columns=dp_columns, dp_seals=dp_seals, dp_constellation=dp_constellation,
                pl_journal=pl_journal, pl_summits=pl_summits, pl_signs=pl_signs, pl_aurora=pl_aurora,
                dg_script=dg_script, dg_timeline=dg_timeline, dg_cans=dg_cans, dg_leader=dg_leader)
