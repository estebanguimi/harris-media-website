"""Builders for the per-version art directions (heroes + section modules)."""
# Python 3.8+ compatibility: literals used inside f-strings
_Q1 = 'logo'
import html as H, re, json
from extra import EXTRA, SV
from versions import HERO, facts_of, count_attr, crumbs
from designs import DESIGN, SIG, GF

e = lambda s: H.escape(str(s), quote=True)


def style_vars(d):
    p = d['pal']
    return (f"--bg:{p['bg']};--fg:{p['fg']};--a:{p['a']};--a2:{p['a2']};--ink:{p['ink']};"
            f"--hf:'{p['hf']}', var(--font);--bf:'{p['bf']}', var(--body);--r:{p['r']}px;")


def fonts_link(d):
    fams = {d['pal']['hf'], d['pal']['bf']}
    q = '&'.join('family=' + GF[f] for f in sorted(fams) if f in GF)
    return f'<link href="https://fonts.googleapis.com/css2?{q}&display=swap" rel="stylesheet">' if q else ''


def num(v):
    ca = count_attr(v)
    return f'<span data-count="{ca[0]}" data-suffix="{ca[1]}">{e(v)}</span>' if ca else e(v)


def actions(proof, cls='hx-btn'):
    out = ''
    if proof:
        out += f'<a class="{cls} solid" data-magnet href="{proof[0]}" target="_blank" rel="noopener">{e(proof[1])} ↗</a>'
    return out + f'<a class="{cls}" data-magnet href="#story">The story ↓</a>'


def copy(c, d, i, n, title_cls='hx-title'):
    (l1, l2), lede, proof, word, img2 = HERO[c['slug']]
    return f'''{crumbs(c)}<div class="hx-kick"><span>{i + 1:02d}/{n:02d}</span><b>{e(d['name'])}</b><span>{e(c['tag'])}</span></div>
<h1 class="{title_cls}" data-split data-hovertext>{e(l1)}<br><em>{e(l2)}</em></h1>
<p class="hx-lede">{e(lede)}</p><div class="hx-actions">{actions(proof)}</div>'''


# ================================================================== HEROES
def h_broadcast(c, d, i, n):
    x = EXTRA[c['slug']]
    tick = ' ◆ '.join([c['name'].upper()] + [t for t, _ in x['steps']] + [l.upper() for _, l in facts_of(c['slug'])])
    return f'''<section class="hx hx-broadcast"><div class="v-grain"></div>
<div class="bc-top"><span class="bc-live"><i></i>LIVE</span><span data-clock>--:--:--</span><span>HMG NEWS DESK · {e(c['tag'])}</span></div>
<div class="wrap bc-grid">
  <div class="bc-copy">{copy(c, d, i, n)}</div>
  <div class="bc-frame" data-depth="-10"><img src="{c['logo']}" alt="{e(c['name'])}"><span class="bc-rec">● REC</span><span class="bc-tc" data-timecode>00:00:00:00</span>
    <i class="bc-c tl"></i><i class="bc-c tr"></i><i class="bc-c bl"></i><i class="bc-c br"></i>
    <div class="bc-lower"><b>{e(c['name'])}</b><span>{e(c['world'])} · HARRIS MEDIA GROUP</span></div></div>
</div>
<div class="bc-ticker"><span class="bc-tag">BREAKING</span><div class="bc-tt"><div>{e(tick)} ◆ {e(tick)} ◆ </div></div></div></section>'''


def h_tiles(c, d, i, n):
    return f'''<section class="hx hx-tiles"><div class="v-grain"></div><div class="wrap tl-grid">
<div class="tl-copy">{copy(c, d, i, n)}</div>
<div class="tl-photo" data-tiles="7x9" style="--img:url('{c['logo']}')" role="img" aria-label="{e(c['name'])}"></div>
</div><div class="tl-index" aria-hidden="true">{e(d['name'])} — {e(c['world'])}</div></section>'''


def h_lens(c, d, i, n):
    (l1, l2), lede, proof, word, img2 = HERO[c['slug']]
    t = f'{e(l1)}<br>{e(l2)}'
    return f'''<section class="hx hx-lens"><div class="v-grain"></div>
<div class="ln-stage" data-lens style="--img:url('{img2 or c['logo']}')">
  <div class="ln-base" aria-hidden="true">{t}</div>
  <div class="ln-glass" aria-hidden="true"><div class="ln-in">{t}</div></div>
</div>
<div class="wrap ln-copy">{crumbs(c)}<div class="hx-kick"><span>{i + 1:02d}/{n:02d}</span><b>{e(d['name'])}</b><span>{e(c['tag'])}</span></div>
<h1 class="sr-only">{e(l1)} {e(l2)}</h1><p class="hx-lede">{e(lede)}</p><div class="hx-actions">{actions(proof)}</div></div>
<figure class="ln-photo" data-depth="16"><img src="{c['logo']}" alt="{e(c['name'])}"></figure>
<div class="ln-hint" aria-hidden="true">MOVE THE LENS ACROSS THE TITLE</div></section>'''


def h_spotlight(c, d, i, n):
    (l1, l2), *_ = HERO[c['slug']]
    return f'''<section class="hx hx-spot" data-spot style="--img:url('{c['logo']}')"><div class="v-grain"></div>
<div class="sp-dark" aria-hidden="true"></div><div class="sp-lit" aria-hidden="true"><div class="sp-word">{e(l2)}</div></div>
<div class="sp-word ghost" aria-hidden="true">{e(l2)}</div>
<div class="wrap sp-copy">{copy(c, d, i, n)}</div><div class="sp-hint" aria-hidden="true">● MOVE THE LIGHT</div></section>'''


def h_kinetic(c, d, i, n):
    x = EXTRA[c['slug']]
    rows = [c['name'].upper(), c['world'], x['big'], c['tag']]
    rr = ''.join(f'<div class="kn-row{" o" if k % 2 else ""}" data-dir="{1 if k % 2 else -1}"><div>{(e(r) + " · ") * 6}</div></div>' for k, r in enumerate(rows))
    return f'''<section class="hx hx-kinetic"><div class="v-grain"></div><div class="kn-rows" aria-hidden="true">{rr}</div>
<div class="kn-disc" aria-hidden="true"><img src="{c['logo']}" alt=""></div>
<div class="wrap kn-copy">{copy(c, d, i, n)}</div></section>'''


def h_imgtext(c, d, i, n):
    (l1, l2), lede, proof, word, img2 = HERO[c['slug']]
    return f'''<section class="hx hx-imgtext"><div class="v-grain"></div>
<div class="it-word" data-pan style="--img:url('{img2 or c['logo']}')" aria-hidden="true">{e(word)}</div>
<div class="it-word outline" aria-hidden="true">{e(word)}</div>
<div class="wrap it-copy">{copy(c, d, i, n)}</div><div class="it-strip" aria-hidden="true"><img src="{c['logo']}" alt=""></div></section>'''


def h_scramble(c, d, i, n):
    lines = [f'> open client_file --id={c["slug"]}', f'  name ........ {c["name"]}', f'  sector ...... {c["tag"]}', f'  concept ..... {d["name"]}']
    lines += [f'  {l.lower()} ... {v}' for v, l in facts_of(c['slug'])[:3]]
    return f'''<section class="hx hx-scramble"><div class="v-grain"></div><div class="sc-grid-bg" aria-hidden="true"></div>
<div class="wrap sc-grid">
  <div class="sc-copy">{copy(c, d, i, n, 'hx-title sc-title')}</div>
  <div class="sc-side"><figure class="sc-photo" data-glitch><img src="{c['logo']}" alt="{e(c['name'])}"><img src="{c['logo']}" alt="" aria-hidden="true"><img src="{c['logo']}" alt="" aria-hidden="true"></figure>
  <pre class="sc-read" data-type='{e(json.dumps(lines))}'></pre></div>
</div></section>'''


def h_blob(c, d, i, n):
    p = d['pal']
    return f'''<section class="hx hx-blob"><canvas class="bl-canvas" data-blob="{p['a']},{p['a2']},{p['fg']}" aria-hidden="true"></canvas><div class="v-grain"></div>
<div class="wrap bl-grid"><div class="bl-copy">{copy(c, d, i, n)}</div>
<figure class="bl-arch" data-depth="12"><img src="{c['logo']}" alt="{e(c['name'])}"><figcaption>{e(c['world'])}</figcaption></figure></div></section>'''


def h_particles(c, d, i, n):
    (l1, l2), lede, proof, word, img2 = HERO[c['slug']]
    p = d['pal']
    return f'''<section class="hx hx-particles v3-hero"><canvas class="v3-canvas" data-word="{e(word)}" data-mode="{d.get('particle') or 'dots'}" data-colors="{p['a']},{p['a2']},{p['fg']}" data-font='900 200px "{p['hf']}", sans-serif' aria-hidden="true"></canvas><div class="v-grain"></div>
<div class="wrap"><div class="v3-copy">{copy(c, d, i, n)}</div></div><div class="v3-hint" aria-hidden="true">move your cursor through the letters</div></section>'''


def h_cinematic(c, d, i, n):
    (l1, l2), lede, proof, word, img2 = HERO[c['slug']]
    x = EXTRA[c['slug']]
    return f'''<section class="hx v2-hero"><div class="v-grain"></div><div class="v2-outline" aria-hidden="true">{e(x['big'])}</div>
<div class="wrap v2-grid"><div>{copy(c, d, i, n)}</div>
<figure class="v2-photo" data-depth="-14"><img src="{c['logo']}" alt="{e(c['name'])}"><figcaption><span>{e(c['tag'])}</span><span>{i + 1:02d}</span></figcaption></figure></div>
<div class="v2-cue" aria-hidden="true">SCROLL<i></i></div></section>'''


HEROES = dict(broadcast=h_broadcast, tiles=h_tiles, lens=h_lens, spotlight=h_spotlight, kinetic=h_kinetic,
              imgtext=h_imgtext, scramble=h_scramble, blob=h_blob, particles=h_particles, cinematic=h_cinematic)


# ================================================================== SECTIONS
def s_brief(c, d):
    k, title, paras = EXTRA[c['slug']]['brief']
    img2 = HERO[c['slug']][4]
    fig = f'<figure class="v2-figure" data-reveal><img src="{img2}" alt="" loading="lazy"></figure>' if img2 else ''
    return f'''<section class="v2-sec"><div class="wrap v2-sticky"><div class="pin"><span class="v2-k">{e(k)}</span><h2 class="v2-h" data-reveal>{e(title)}</h2></div>
<div>{''.join(f'<p data-reveal>{e(p)}</p>' for p in paras)}{fig}</div></div></section>'''


def s_words(c, d):
    k, title, paras = EXTRA[c['slug']]['brief']
    return f'''<section class="sx-words"><div class="wrap"><span class="v2-k">{e(k)} — {e(title)}</span>
<p class="sx-wtext" data-words>{e(' '.join(paras))}</p></div></section>'''


def s_quote_words(c, d):
    x = EXTRA[c['slug']]
    q, src = x.get('quote') or (x['closing'], 'Harris Media Group')
    return f'<section class="sx-words q"><div class="wrap"><span class="v2-k">In their words</span><p class="sx-wtext" data-words>“{e(q)}”</p><div class="sx-cite">— {e(src)}</div></div></section>'


def s_hscroll(c, d):
    x = EXTRA[c['slug']]; img2 = HERO[c['slug']][4]
    panels = [f'<div class="v2-panel fact"><div class="lbl">FACT</div><div><div class="pn">{num(v)}</div><div class="lbl" style="margin-top:14px">{e(l)}</div></div></div>' for v, l in facts_of(c['slug'])]
    for j, (t, dd) in enumerate(x['steps']):
        panels.append(f'<div class="v2-panel"><div class="pn">{j + 1:02d}</div><div><h3>{e(t)}</h3><p>{e(dd)}</p></div></div>')
        if j == 1:
            panels.append(f'<div class="v2-panel photo"><img src="{img2 or c["logo"]}" alt="" loading="lazy"></div>')
    return f'''<section class="v2-hs"><div class="v2-hs-pin"><div class="v2-hs-head"><div><span class="v2-k">The file</span><h2 class="v2-h" style="font-size:clamp(2rem,4vw,3.4rem)">Facts & playbook</h2></div><div class="v2-hs-bar"><i></i></div></div>
<div class="v2-hs-track">{''.join(panels)}</div></div></section>'''


def s_accordion(c, d):
    rows = ''.join(f'''<div class="v2-acc-row{' open' if j == 0 else ''}"><button type="button" aria-expanded="{'true' if j == 0 else 'false'}"><span class="an">{j + 1:02d}</span><span class="at">{e(t)}</span><span class="ai">+</span></button>
<div class="ab"><div><p>{e(dd)}</p></div></div></div>''' for j, (t, dd) in enumerate(EXTRA[c['slug']]['steps']))
    return f'<section class="v2-sec"><div class="wrap"><span class="v2-k">The playbook</span><h2 class="v2-h" style="margin-bottom:40px">What we did</h2><div class="v2-acc">{rows}</div></div></section>'


def s_bento(c, d):
    s = c['slug']; x = EXTRA[s]; (l1, l2), lede, proof, word, img2 = HERO[s]
    k, title, paras = x['brief']; fs = facts_of(s)
    cells = [f'<div class="bx photo h2" data-reveal data-tilt><img src="{c["logo"]}" alt="{e(c["name"])}" loading="lazy"><span class="cap">{e(c["name"]).upper()}</span></div>',
             f'<div class="bx w2" data-reveal><div class="bl">{e(k)}</div><h3>{e(title)}</h3><p>{e(paras[0])}</p></div>']
    cells += [f'<div class="bx{" acc" if j == 0 else ""}" data-reveal data-tilt><div class="bl">{e(l).upper()}</div><div class="bn">{num(v)}</div></div>' for j, (v, l) in enumerate(fs[:3])]
    if len(paras) > 1:
        cells.append(f'<div class="bx w2" data-reveal><div class="bl">CONTEXT</div><p style="font-size:1.05rem">{e(paras[1])}</p></div>')
    if img2:
        cells.append(f'<div class="bx photo w2" data-reveal data-tilt><img src="{img2}" alt="" loading="lazy"><span class="cap">FROM THE CASE</span></div>')
    if proof:
        cells.append(f'<a class="bx" href="{proof[0]}" target="_blank" rel="noopener" data-reveal data-tilt><div class="bl">PROOF</div><h3>{e(proof[1])}</h3><span class="go">↗</span></a>')
    cells.append('<a class="bx" href="contact.html" data-reveal data-tilt><div class="bl">NEXT STEP</div><h3>Build yours</h3><span class="go">→</span></a>')
    return f'<section class="v3-sec"><div class="wrap"><div class="v3-k">client_file.{s}</div><h2 class="v3-h">The file</h2><div class="bento">{"".join(cells)}</div></div></section>'


def s_path(c, d):
    st = EXTRA[c['slug']]['steps']
    steps = ''.join(f'<article class="v3-step" data-node="{(j + .5) / len(st):.2f}"><div class="sn">STEP_{j + 1:02d}</div><h3>{e(t)}</h3><p>{e(dd)}</p></article>' for j, (t, dd) in enumerate(st))
    return f'''<section class="v3-sec"><div class="wrap"><div class="v3-k">playbook</div><h2 class="v3-h">What we did</h2>
<div class="v3-path" data-scrub-host><svg viewBox="0 0 120 1000" preserveAspectRatio="none" aria-hidden="true"><path class="ghost" d="M60 0 C 120 160, 0 340, 60 500 S 0 840, 60 1000"/><path data-scrub d="M60 0 C 120 160, 0 340, 60 500 S 0 840, 60 1000"/></svg>
<div class="v3-steps">{steps}</div></div></div></section>'''


def s_stack(c, d):
    st = EXTRA[c['slug']]['steps']
    cards = ''.join(f'<article class="stk-card" style="--k:{j}"><div class="stk-n">{j + 1:02d}<small>/{len(st):02d}</small></div><div><h3>{e(t)}</h3><p>{e(dd)}</p></div></article>' for j, (t, dd) in enumerate(st))
    return f'<section class="sx-stack"><div class="wrap"><span class="v2-k">The playbook</span><h2 class="v2-h">What we did</h2><div class="stk">{cards}</div></div></section>'


def s_zigzag(c, d):
    st = EXTRA[c['slug']]['steps']; img2 = HERO[c['slug']][4]
    imgs = [c['logo'], img2 or c['logo']]
    rows = ''.join(f'''<div class="zz-row{' rev' if j % 2 else ''}" data-reveal><figure class="zz-img"><img src="{imgs[j % 2]}" alt="" loading="lazy"><span>{j + 1:02d}</span></figure>
<div class="zz-txt"><span class="v2-k">Step {j + 1:02d}</span><h3>{e(t)}</h3><p>{e(dd)}</p></div></div>''' for j, (t, dd) in enumerate(st))
    return f'<section class="sx-zz"><div class="wrap"><span class="v2-k">The playbook</span><h2 class="v2-h" style="margin-bottom:50px">What we did</h2>{rows}</div></section>'


def s_odometer(c, d):
    fs = facts_of(c['slug'])
    cells = ''.join(f'<div class="od" data-reveal><div class="od-n" data-odo="{e(v)}">{e(v)}</div><div class="od-l">{e(l)}</div></div>' for v, l in fs[:3])
    return f'<section class="sx-odo"><div class="wrap"><span class="v2-k">By the numbers</span><div class="od-row">{cells}</div></div></section>'


def s_timeline_v(c, d):
    x = EXTRA[c['slug']]
    items = x.get('timeline') or [(f'{j + 1:02d}', t, dd) for j, (t, dd) in enumerate(x['steps'])]
    lab = 'Timeline' if x.get('timeline') else 'Step by step'
    it = ''.join(f'<div class="tv-i" data-reveal><b>{e(y)}</b><div><h3>{e(t)}</h3><p>{e(dd)}</p></div></div>' for y, t, dd in items)
    return f'<section class="sx-tv"><div class="wrap"><span class="v2-k">{lab}</span><h2 class="v2-h" style="margin-bottom:46px">The story so far</h2><div class="tv" data-fill><span class="tv-line"></span>{it}</div></div></section>'


def s_svc_img(c, d):
    img2 = HERO[c['slug']][4] or c['logo']
    svc = ''.join(f'<li><a href="services.html#{SV[t]}" data-img="{img2 if k % 2 else c["logo"]}">{e(t)}<span>↗</span></a></li>' for k, t in enumerate(EXTRA[c['slug']]['services']))
    return f'<section class="v2-sec"><div class="wrap"><span class="v2-k">Disciplines deployed</span><h2 class="v2-h" style="margin-bottom:30px">The team behind it</h2><ul class="v2-svc sx-svc">{svc}</ul></div><div class="svc-float" aria-hidden="true"><img alt="" src="{c[_Q1]}"></div></section>'


def services_pills(c, d):
    pills = ''.join(f'<a data-magnet href="services.html#{SV[t]}">{e(t)} ↗</a>' for t in EXTRA[c['slug']]['services'])
    return f'<section class="v3-sec" style="padding-top:0"><div class="wrap"><div class="v3-k">disciplines_deployed</div><h2 class="v3-h">The team behind it</h2><div class="v3-pills">{pills}</div></div></section>'


def s_close_marquee(c, d):
    x = EXTRA[c['slug']]
    words = [w for w in re.split(r'[.—]\s*', x['closing']) if w.strip()]
    marq = ''.join(f'<span>{e(w.strip())}</span>' for w in words * 3)
    return f'<div class="v2-marq" aria-label="{e(x["closing"])}"><div data-skew><div class="v2-marq-in">{marq}{marq}</div></div></div>'


def s_close_fill(c, d):
    return f'<section class="v3-sec"><div class="wrap"><p class="v3-fill" data-fill>{e(EXTRA[c["slug"]]["closing"])}</p></div></section>'


def particle_block(c, d, word=None, caption=None, colors=None, font=None, cls=''):
    w, cap = SIG[c['slug']]
    word = word or w; caption = caption or cap
    return f'''<section class="sx-pt {cls}"><div class="sx-pt-in"><canvas class="sx-pt-c" data-word="{e(word)}" data-mode="{(d or {}).get('particle') or 'dots'}" data-colors="{colors}" data-font='{e(font)}' aria-hidden="true"></canvas>
<div class="wrap sx-pt-cap"><span class="v2-k">Hover the {"number" if any(ch.isdigit() for ch in word) else "word"}</span><p>{e(caption)}</p></div></div></section>'''


def s_close_particles(c, d):
    p = d['pal']
    return particle_block(c, d, colors=f"{p['a']},{p['a2']},{p['fg']}", font=f'900 200px "{p["hf"]}", sans-serif')


SECTIONS = dict(brief=s_brief, words=s_words, quote_words=s_quote_words, hscroll=s_hscroll, accordion=s_accordion,
                bento=s_bento, path=s_path, stack=s_stack, zigzag=s_zigzag, odometer=s_odometer, timeline_v=s_timeline_v,
                svc_img=s_svc_img, close_marquee=s_close_marquee, close_fill=s_close_fill, close_particles=s_close_particles)


def build_version(c, v, i, n, pal=None, hero_html=None):
    d = DESIGN[(c['slug'], v)]
    if pal:
        d = dict(d, pal=dict(d['pal'], **pal))
    import batch1, batch2
    H_ALL = {**HEROES, **batch1.HEROES1, **batch2.HEROES2}; S_ALL = {**batch1.SIGS1, **batch2.SIGS2}
    body = H_ALL[d['hero']](c, d, i, n) if hero_html is None else hero_html
    if d.get('sig'):
        body += S_ALL[d['sig']](c, d)
    secs = d['secs']
    body += '<div id="story"></div>'
    for s in secs:
        if s.startswith('close') and 'svc_img' not in secs:
            body += services_pills(c, d)
        body += SECTIONS[s](c, d)
    cls = f"vx hero-{d['hero']} rad{'' if d['pal']['r'] else '0'}"
    return f'<div class="v2 v3 {cls}" style="{style_vars(d)}"><div class="v-cursor" aria-hidden="true"></div>' + body, fonts_link(d)
