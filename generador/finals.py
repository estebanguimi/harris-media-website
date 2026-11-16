"""Final client pages: each mixes the versions the client picked and uses modules no other final page uses
(own title animation, own hover effect, own timeline / closing)."""
import html as H, json, re
from extra import EXTRA, SV
from versions import HERO, THEME, facts_of, upgrade_v1
from designs import DESIGN

e = lambda s: H.escape(str(s), quote=True)

# What each client picked. hero/palette/content: 1 = V1 world, 2/3 = that version's design.
FINAL = {
    # pf = the page's single type system (heading, body) · pal = the page's single palette for every section
    # cur = intro curtain · rv = scroll reveal · fx/hover = title entrance / hover · tilt/magnet/cursor/par = interactions owned by one page
    'right-for-america': dict(hero=1, palette=1, base=3, band='flag', fx='rise', hover='lift', cur='up', rv='rise', tilt=True,
                              pf=('Oswald', 'Work Sans'), secs=['stars', 'odometer', 'bento', 'stack', 'pills', 'close_particles']),
    'netanyahu-likud': dict(hero=1, palette=1, base=1, fx='type', hover='glow', cur='bubble', rv='pop', magnet=True, pf=('Rubik', 'Rubik'),
                            pal=dict(bg='#F4F7FC', fg='#0B1F4D', a='#0038B8', a2='#229ED9', ink='#FFFFFF'),
                            secs=['x_brief', 'donut', 'x_steps', 'x_chips', 'close_fill']),
    'nh-senate-republicans': dict(hero=3, palette=3, base=3, fx='decode', hover='scramble', cur='scan', rv='scan', pf=('Space Mono', 'Space Mono'),
                                  secs=['plaque', 'funnel', 'path', 'svc_term', 'close_type']),
    'francis-suarez': dict(hero=1, palette=1, base=1, fx='flicker', hover='neon', cur='sunset', rv='glow', cursor=True, pf=('Unbounded', 'Outfit'),
                           secs=['aichat', 'hscroll', 'svc_img', 'confetti']),
    'rand-paul': dict(hero=1, palette=2, base=2, fx='stamp', hover='shake', cur='down', rv='press', pf=('JetBrains Mono', 'JetBrains Mono'),
                      pal=dict(bg='#020A02', fg='#C8FFC0', a='#39FF14', a2='#E8D27A', ink='#020A02', r=0),
                      secs=['brief', 'pamphlet', 'zigzag', 'tl_ledger', 'close_marquee']),
    'ted-cruz': dict(hero=2, palette=2, base=2, fx='ink', hover='skew', cur='split', rv='fade', pf=('Bodoni Moda', 'Inter'),
                     secs=['meter', 'words', 'accordion', 'timeline_v', 'close_stamp']),
    'rick-scott': dict(hero=3, palette=3, base=3, fx='flap', hover='flip', cur='diag', rv='slide', pf=('Barlow Condensed', 'Barlow Condensed'),
                       secs=['press', 'finish', 'tl_laps', 'close_flap']),
    'mike-huckabee': dict(hero=2, palette=2, base=2, fx='typewriter', hover='underline', cur='left', rv='print', pf=('Chivo Mono', 'Source Serif 4'),
                          secs=['micro', 'book', 'tl_archive', 'svc_blogroll', 'close_signoff']),
    'maine-gop': dict(hero=3, palette=3, base=3, fx='fog', hover='brass', cur='fade', rv='fog', par=True, pf=('Bebas Neue', 'Manrope'),
                      secs=['newengland', 'release', 'quote_engrave', 'tl_logbook', 'svc_tags', 'close_lighthouse']),
    'linda-mcmahon': dict(hero=2, palette=2, base=2, fx='marquee', hover='spot', cur='iris', rv='spot', pf=('Instrument Serif', 'Karla'),
                          secs=['counties', 'exhibit', 'svc_playbill', 'close_credits']),
    'vhha': dict(hero=1, palette=1, base=1, v1_keep=0, fx='pulse', hover='beat', cur='ekg', rv='heart', pf=('Sora', 'Sora'),
                 pal=dict(bg='#F3FAFA', fg='#0B3A3E', a='#0E7C86', a2='#E5484D', ink='#FFFFFF', r=14),
                 secs=['vh_chart', 'vh_monitors', 'vh_rx', 'vh_pulse']),
    'txoga': dict(hero=1, palette=1, base=1, fx='weld', hover='heat', cur='shutter', rv='drop', pf=('Big Shoulders Display', 'Libre Franklin'),
                  pal=dict(bg='#121212', fg='#F2E8D5', a='#FFB000', a2='#FF6A00', ink='#121212', r=0),
                  secs=['tx_blueprint', 'tx_pipeline', 'tx_switches', 'tx_tank']),
    'dan-patrick': dict(hero=1, palette=1, base=1, fx='engrave', hover='gild', cur='star', rv='unfold', pf=('Cinzel', 'Lora'),
                        pal=dict(bg='#0E1B3D', fg='#F4F1EA', a='#BF0A30', a2='#D4AF37', ink='#FFFFFF', r=0),
                        secs=['dp_proclaim', 'dp_rotunda', 'dp_columns', 'dp_seals', 'dp_constellation']),
    'sarah-palin': dict(hero=1, palette=1, base=1, v1_keep=0, fx='snowfall', hover='frost', cur='aurora', rv='drift', pf=('Fraunces', 'Figtree'),
                        pal=dict(bg='#04111C', fg='#E3F2F7', a='#2EFFAA', a2='#B39CFF', ink='#04111C', r=10),
                        secs=['pl_journal', 'pl_summits', 'pl_signs', 'pl_aurora']),
    'doug-collins': dict(hero=3, palette=1, base=1, fx='cut', hover='rec', cur='leader', rv='cut', pf=('Anton', 'Space Grotesk'),
                         pal=dict(bg='#0E0E0E', fg='#F7EFE6', a='#FF9E5E', a2='#FF3B30', ink='#111111', r=0),
                         secs=['dg_script', 'dg_timeline', 'dg_cans', 'dg_leader']),
}


def v1_palette(slug):
    bg, fg, a, a2, ink, *_ = THEME[slug]
    return dict(bg=bg, fg=fg, a=a, a2=a2, ink=ink)


def vx_style(p, own_fonts):
    s = f"--bg:{p['bg']};--fg:{p['fg']};--a:{p['a']};--a2:{p['a2']};--ink:{p['ink']};--r:{p.get('r', 0)}px;"
    if own_fonts:
        s += f"--hf:'{p['hf']}', var(--font);--bf:'{p['bf']}', var(--body);"
    else:
        s += "--hf:var(--font);--bf:var(--body);"
    return s


# ------------------------------------------------------------------ V1-world chapter modules (themed by the world class)
def x_brief(c, d):
    x = EXTRA[c['slug']]; k, title, paras = x['brief']
    return f'''<section class="x-sec x-brief"><div class="x-big" data-px="-0.25" aria-hidden="true">{e(x['big'])}</div><div class="wrap x-brief-grid">
<div data-reveal><span class="x-kicker">{k}</span><h2 class="x-h2">{e(title)}</h2></div><div>{''.join(f'<p class="x-p" data-reveal>{e(p)}</p>' for p in paras)}</div></div></section>'''


def x_steps(c, d):
    x = EXTRA[c['slug']]
    steps = ''.join(f'<article class="x-step" data-reveal data-tilt><span class="x-num">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(dd)}</p></article>' for i, (t, dd) in enumerate(x['steps']))
    return f'''<section class="x-sec x-play x-style-{x['style']}"><div class="wrap"><div class="x-head" data-reveal><span class="x-kicker">THE PLAYBOOK</span><h2 class="x-h2">WHAT WE DID</h2></div>
<div class="x-steps" data-reveal><div class="x-line"></div>{steps}</div></div></section>'''


def x_chips(c, d):
    chips = ''.join(f'<a class="x-chip" href="services.html#{SV[s]}">{e(s)} <span aria-hidden="true">↗</span></a>' for s in EXTRA[c['slug']]['services'])
    return f'<section class="x-sec x-tight"><div class="wrap x-svc"><div data-reveal><span class="x-kicker">DISCIPLINES DEPLOYED</span><h2 class="x-h2" style="font-size:clamp(1.6rem,3.2vw,2.6rem)">THE HMG TEAM BEHIND IT</h2></div><div class="x-chips" data-reveal>{chips}</div></div></section>'


# ------------------------------------------------------------------ new one-off modules
def tl_ledger(c, d):
    st = EXTRA[c['slug']]['steps']
    rows = ''.join(f'<li data-reveal><span class="lg-no">No. {k + 1:02d}</span><span class="lg-t">{e(t.split("·")[-1].strip())}</span><span class="lg-dots"></span><span class="lg-d">{e(dd)}</span></li>' for k, (t, dd) in enumerate(st))
    return f'''<section class="sx-ledger"><div class="wrap"><div class="lg-mast"><span>THE CHRONICLE</span><b>Campaign Ledger</b><span>2016 EDITION</span></div>
<ol class="lg">{rows}</ol></div></section>'''


def tl_laps(c, d):
    tl = EXTRA[c['slug']]['timeline']
    laps = ''.join(f'<div class="lp" data-lap="{(k + .5) / len(tl):.2f}"><span class="lp-n">LAP {k + 1:02d}</span><b>{e(y)}</b><h3>{e(t)}</h3><p>{e(dd)}</p></div>' for k, (y, t, dd) in enumerate(tl))
    return f'''<section class="sx-laps" data-laps><div class="wrap"><span class="v2-k">Lap by lap</span><h2 class="v2-h">The race, in four laps.</h2>
<div class="lp-track"><span class="lp-rail"></span><span class="lp-car">RS</span><span class="lp-flag">🏁</span></div><div class="lp-row">{laps}</div></div></section>'''


def close_type(c, d):
    lines = ['> mission_status --client="NH Senate Republicans"', '  cycles ............ 3', '  outcome ........... SUPERMAJORITY',
             '  award ............. BEST USE OF ONLINE TARGETING (2025)', '> target locked.']
    return f'<section class="sx-ctype"><div class="wrap"><pre class="ct-term" data-type=\'{e(json.dumps(lines))}\'></pre></div></section>'


def close_stamp(c, d):
    words = EXTRA[c['slug']]['closing'].rstrip('.').split()
    st = ''.join(f'<span style="--k:{k};--r:{(-8, 5, -3, 7, -6)[k % 5]}deg">{e(w)}</span>' for k, w in enumerate(words))
    return f'<section class="sx-cstamp"><div class="wrap"><p class="cs-w" data-stamps aria-label="{e(EXTRA[c["slug"]]["closing"])}">{st}</p></div></section>'


def close_flap(c, d):
    rows = ['COUNTED OUT.', 'CROSSED FIRST.']
    board = ''.join(f'<div class="fb-row" data-flap="{r}">' + ''.join('<span class="fb-c"> </span>' for _ in range(20)) + '</div>' for r in rows)
    return f'<section class="sx-cflap"><div class="wrap"><div class="fb-board" aria-label="Counted out. Crossed the line first.">{board}<div class="fb-foot"><i></i>FINAL · FLORIDA 2010</div></div></div></section>'


def band_flag(c, p):
    return (f'<section class="flag-band" style="--bg:{p["bg"]};--fg:{p["fg"]};--a:{p["a"]}"><canvas class="fl-canvas" data-flag="{p["a"]},{p["fg"]},{p["a2"]}" aria-hidden="true"></canvas>'
            f'<div class="wrap fb-cap"><span class="v2-k">On air · 2024 presidential cycle</span><p>Presidential scale. Platform by platform. Ad by ad.</p></div>'
            f'<div class="fl-hint" aria-hidden="true">MOVE TO CHANGE THE WIND</div></section>')


WORLD_MODULES = dict(x_brief=x_brief, x_steps=x_steps, x_chips=x_chips)
NEW_MODULES = dict(tl_ledger=tl_ledger, tl_laps=tl_laps, close_type=close_type, close_stamp=close_stamp, close_flap=close_flap)
from finals2 import MODULES2, personalize
NEW_MODULES.update(MODULES2)
from finals3 import MODULES3
NEW_MODULES.update(MODULES3)


def build_final(c, i, n, world_cls, world_fn):
    import pages2 as P2, batch1, batch2
    from designs import GF
    f = FINAL[c['slug']]
    p1 = v1_palette(c['slug'])
    hf, bf = f['pf']
    # one palette for the whole page
    if f.get('pal'):
        pal = dict(f['pal'])
    elif f['palette'] == 1:
        pal = dict(p1)
    else:
        pal = dict(DESIGN[(c['slug'], f['palette'])]['pal'])
    pal.setdefault('r', DESIGN[(c['slug'], f['base'] if f['base'] != 1 else 2)]['pal']['r'])
    pal.update(hf=hf, bf=bf)
    fonts = '<link href="https://fonts.googleapis.com/css2?' + '&'.join('family=' + GF[x] for x in sorted({hf, bf})) + '&display=swap" rel="stylesheet">'
    d = dict(DESIGN[(c['slug'], f['base'] if f['base'] != 1 else 2)], pal=pal)

    # ---------------- hero (+ the V1 world's own sections when the content comes from V1)
    v1 = upgrade_v1(world_fn(c))
    cut = v1.index('</section>') + len('</section>')
    if f.get('v1_keep') is not None:          # keep only the first N V1 sections after the hero
        parts = v1[cut:].split('<section')
        v1 = v1[:cut] + parts[0] + ''.join('<section' + x for x in parts[1:1 + f['v1_keep']])
    if f['hero'] == 1:
        hero = f'<div class="{world_cls}" style="--hot:{pal["a"]}">' + (v1 if f['base'] == 1 else v1[:cut])
        hero_open = True
    else:
        dh = DESIGN[(c['slug'], f['hero'])]
        hpal = dict(dh['pal'], **{k: pal[k] for k in ('bg', 'fg', 'a', 'a2', 'ink')}) if f.get('pal') else dict(dh['pal'])
        hpal.update(hf=hf, bf=bf)
        dh = dict(dh, pal=hpal)
        H_ALL = {**P2.HEROES, **batch1.HEROES1, **batch2.HEROES2}
        hero = f'<div class="v2 v3 vx final-vx" style="{vx_style(hpal, True)}">' + H_ALL[dh['hero']](c, dh, i, n) + '</div>'
        if f['base'] == 1:
            hero += f'<div class="{world_cls}" style="--hot:{pal["a"]}">' + v1[cut:]
            hero_open = True
        else:
            hero_open = False

    # ---------------- sections
    S_ALL = {**batch1.SIGS1, **batch2.SIGS2}
    SEC = {**P2.SECTIONS, 'pills': P2.services_pills, **S_ALL}
    world_part, vx_part = '', ''
    for s in f['secs']:
        if s in WORLD_MODULES:
            world_part += WORLD_MODULES[s](c, d)
        elif s in NEW_MODULES:
            vx_part += NEW_MODULES[s](c, d)
        else:
            vx_part += SEC[s](c, d)
    band = band_flag(c, pal) if f.get('band') == 'flag' else ''
    body = hero + (world_part + '</div>' if hero_open else (f'<div class="{world_cls}">' + world_part + '</div>' if world_part else ''))
    body += band + f'<div class="v2 v3 vx final-vx" style="{vx_style(pal, True)}"><div class="v-cursor" aria-hidden="true"></div>' + vx_part
    attrs = (f'data-fx="{f["fx"]}" data-hfx="{f["hover"]}" data-rv="{f["rv"]}"' + (' data-par' if f.get('par') else '')
             + f' class="pf-page" style="--pf-h:\'{hf}\';--pf-b:\'{bf}\';--hot:{pal["a"]}"')
    return f'<div {attrs}>' + personalize(body, f), fonts   # caller closes the vx div + fx div
