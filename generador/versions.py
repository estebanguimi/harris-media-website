"""Three design directions per client: V1 (bespoke world), V2 (cinematic editorial), V3 (interactive)."""
# Python 3.8+ compatibility: literals used inside f-strings
_Q1 = " class=\"on\" aria-current=\"page\""
_Q2 = " class=\"on\""
import html as H, re
from extra import EXTRA, SV

UP = 'https://www.harrismediallc.com/wp-content/uploads/'
e = lambda s: H.escape(str(s), quote=True)

# bg, fg, accent, accent-2, ink-on-accent, heading font, body font
THEME = {
    'right-for-america': ('#07122B', '#F3F5FA', '#E63946', '#FFFFFF', '#FFFFFF', None, None),
    'netanyahu-likud': ('#06143B', '#EEF3FF', '#3D7BFF', '#9CC0FF', '#FFFFFF', None, None),
    'nh-senate-republicans': ('#0E1A12', '#E8EFE6', '#C6F432', '#7FA35A', '#0E1A12', None, None),
    'francis-suarez': ('#12002B', '#F7E9FF', '#FF2E88', '#00E5FF', '#FFFFFF', None, None),
    'rand-paul': ('#020A02', '#C8FFC0', '#39FF14', '#9DFF9D', '#020A02', None, 'ui-monospace, Menlo, Consolas, monospace'),
    'ted-cruz': ('#EFE9DD', '#1A1714', '#B3261E', '#1A1714', '#EFE9DD', '"Times New Roman", Georgia, serif', 'Georgia, serif'),
    'rick-scott': ('#062A2A', '#E6FBF8', '#F28C28', '#36C5C5', '#062A2A', None, None),
    'mike-huckabee': ('#FAF8F2', '#22303C', '#C8102E', '#1A5EA8', '#FFFFFF', None, None),
    'maine-gop': ('#0A1B2E', '#E7EEF5', '#F6D776', '#8FB8DE', '#0A1B2E', None, None),
    'linda-mcmahon': ('#050505', '#F5F2EB', '#FFD666', '#B08A2E', '#050505', None, None),
    'vhha': ('#F3FAFA', '#0B3A3E', '#0E7C86', '#E5484D', '#FFFFFF', None, None),
    'txoga': ('#121212', '#F2E8D5', '#FFB000', '#FF6A00', '#121212', None, None),
    'dan-patrick': ('#0E1B3D', '#F4F1EA', '#BF0A30', '#5B8BD9', '#FFFFFF', None, None),
    'sarah-palin': ('#04111C', '#E3F2F7', '#2EFFAA', '#B39CFF', '#04111C', None, None),
    'doug-collins': ('#111111', '#F7EFE6', '#FF9E5E', '#FF4D4D', '#111111', None, None),
}

# hero copy per client: (line 1, line 2 accent), lede, proof (url, label) or None, particle word, secondary image
HERO = {
    'right-for-america': (('RIGHT FOR', 'AMERICA'), 'The pro-Trump Super PAC whose digital operation HMG ran in the 2024 Presidential cycle — among the largest spenders on Google and Meta in the entire race.',
                          ('https://drive.google.com/file/d/1DRznd864uxirOjhMIlt_bQx2MmH1bvbb/view?usp=sharing', 'View the case'), 'AMERICA', None),
    'netanyahu-likud': (('THE FIRST', 'AI CHATBOT'), 'The first-ever AI-generated and AI-operated chatbot in presidential political history — built by HMG for Prime Minister Benjamin Netanyahu’s Likud.',
                        ('https://drive.google.com/file/d/1Log_w9TUS4wNAAxe7hSFDu8CaUQPsNws/view', 'View the case'), 'LIKUD', UP + '2025/01/Chat-box.png'),
    'nh-senate-republicans': (('TARGET', 'LOCKED.'), 'Best Use of Online Targeting for a State Legislative Campaign — and a caucus that grew to a supermajority over three election cycles.',
                              ('https://drive.google.com/file/d/1rbmmw1RVOGBLwLtVTHeE2lj_E0LmBBru/view', 'View the case'), 'NH', UP + '2025/05/harris-media-new-slider.png'),
    'francis-suarez': (('SOS', 'AMERICA'), 'The Super PAC supporting Miami Mayor Francis Suarez — and the 2024 AAPC Campaign Excellence Award for Digital Campaign of the Year.',
                       ('https://drive.google.com/file/d/1X7S16rBiPGELuqlyJtyiXnwSvFm_2DPa/view', 'View the case'), 'SOS', UP + '2025/01/img-ai-suarez.png'),
    'rand-paul': (('INTERNET', 'ARMY'), 'Senator Rand Paul’s 2016 Presidential campaign set a new standard for digital strategy in politics — and Politico called it an internet army.',
                  ('https://www.politico.com/magazine/story/2015/04/rand-paul-2016-social-media-117132/', 'Read on Politico'), 'RAND', UP + '2025/01/randpaul.png'),
    'ted-cruz': (('THE UNDERDOG', 'WIN'), 'Over three years with Ted Cruz, whose successful use of the web many credit as part of his incredible underdog Senate win.',
                 ('https://www.politico.com/story/2012/07/contenders-secret-mastering-social-media-079213', 'Read on Politico'), 'CRUZ', None),
    'rick-scott': (('DARK', 'HORSE.'), 'Rick Scott overcame all odds to narrowly win Florida’s 2010 governor’s race — with HMG playing an instrumental role in the win.',
                   None, 'SCOTT', None),
    'mike-huckabee': (('FROM AN ASTERISK', 'TO IOWA.'), 'From “an asterisk in the polls” to Iowa Caucus winner — one of the first presidential campaigns to ever use Twitter.',
                      None, 'IOWA', None),
    'maine-gop': (('PLANTING A FLAG', 'IN MAINE.'), 'Work with the Maine Republican Party — and, in November 2025, HMG’s first dedicated New England office in Augusta.',
                  ('https://www.mainegop.com/', 'Visit Maine GOP'), 'MAINE', None),
    'linda-mcmahon': (('LINDA', 'McMAHON'), 'Statewide campaigns in Connecticut for leaders like Linda McMahon — part of HMG’s growing work across New England.',
                      None, 'CT', None),
    'vhha': (('VITAL', 'SIGNS.'), 'The Virginia Hospital & Healthcare Association — a statewide organization proving HMG’s work reaches far beyond campaigns.',
             ('https://vhha.com/', 'Visit VHHA'), 'VHHA', None),
    'txoga': (('UNDER', 'PRESSURE.'), 'The Texas Oil & Gas Association — energy advocacy from a firm that counts more than ten Fortune 500 energy companies as clients.',
              ('https://www.txoga.org/', 'Visit TXOGA'), 'TXOGA', None),
    'dan-patrick': (('LONE', 'STAR.'), 'Lieutenant Governor of Texas Dan Patrick — a Texas client for a firm whose history runs through the Lone Star State.',
                    None, 'TEXAS', None),
    'sarah-palin': (('THE LAST', 'FRONTIER.'), 'Engaging supporters for one of the most recognizable names in conservative politics.',
                    None, 'ALASKA', None),
    'doug-collins': (('ROLL', 'TAPE.'), 'Video-first creative for Doug Collins of Georgia, built for social feeds.',
                     ('https://www.facebook.com/DougCollinsGeorgia/videos/258139055355254', 'Watch the spot'), 'ROLL', None),
}

# facts for clients that had none in EXTRA (only verifiable data)
FACTS = {
    'rick-scott': [('2010', 'Florida governor’s race'), ('7', 'States with successful digital initiatives'), ('FB', 'Facebook corporate case study')],
    'mike-huckabee': [('2008', 'Iowa Caucus winner'), ('2', 'Online communications staffers'), ('2004', 'The year Vincent’s blog began')],
    'maine-gop': [('2', 'Years in Maine before the office'), ('2025', 'Augusta office opens'), ('ME-2', 'LePage for Congress')],
    'linda-mcmahon': [('CT', 'Statewide campaigns'), ('2', 'Statewide CT leaders: McMahon & Stefanowski'), ('NE', 'New England practice')],
    'vhha': [('VA', 'Virginia'), ('STATEWIDE', 'Organization'), ('VHHA', 'Alliance of hospitals & health systems')],
    'dan-patrick': [('TX', 'Lieutenant Governor'), ('254', 'Texas counties'), ('TX', 'HMG office in Texas')],
    'sarah-palin': [('AK', 'Alaska'), ('NATIONAL', 'Supporter base'), ('ENGAGE', 'Supporter engagement')],
    'doug-collins': [('GA', 'Georgia'), ('VIDEO', 'Social-first format'), ('FB', 'Published on Facebook')],
}


def facts_of(slug):
    return EXTRA[slug].get('facts') or FACTS.get(slug, [])


def count_attr(v):
    m = re.fullmatch(r'([\d,]+)(\+?)', v)
    if not m or re.fullmatch(r'(19|20)\d\d', v):
        return None
    return m.group(1).replace(',', ''), m.group(2)


def theme_style(slug):
    bg, fg, a, a2, ink, hf, bf = THEME[slug]
    s = f'--bg:{bg};--fg:{fg};--a:{a};--a2:{a2};--ink:{ink};'
    if hf: s += f'--hf:{hf};'
    if bf: s += f'--bf:{bf};'
    return s


def vbar(c, v):
    from designs import DESIGN
    lab = [('', 'VERSION 1', 'WORLD'), ('-v2', 'VERSION 2', DESIGN[(c['slug'], 2)]['name']), ('-v3', 'VERSION 3', DESIGN[(c['slug'], 3)]['name'])]
    links = '<span class="sep"></span>'.join(
        f'<a href="client-{c["slug"]}{suf}.html"{_Q1 if i + 1 == v else ""}>{t}<small>{s}</small></a>'
        for i, (suf, t, s) in enumerate(lab))
    mini = ''.join(f'<a href="client-{c["slug"]}{suf}.html"{_Q2 if i + 1 == v else ""} title="{t}">V{i + 1}</a>' for i, (suf, t, s) in enumerate(lab))
    return (f'<nav class="vbar" aria-label="Design versions"><span class="vb-name">{e(c["name"]).upper()}</span>{links}</nav>'
            f'<nav class="vmini" aria-label="Design versions (compact)"><span>VERSION</span>{mini}</nav>')


def curtain(c, v):
    bg, fg, a, a2, ink, *_ = THEME[c['slug']]
    words = ''.join(f'<span style="animation-delay:{i * 60}ms">{e(w)}&nbsp;</span>' for i, w in enumerate(c['name'].upper().split()))
    return (f'<div class="v-curtain" style="--cur:{a};--cur-ink:{ink}" aria-hidden="true"><div class="ct-in">'
            f'<div class="ct-meta">HMG CLIENT FILE · {e(c["world"])}</div><div class="ct-name">{words}</div><div class="ct-bar"><i></i></div></div></div>')


def crumbs(c):
    return (f'<div class="w-crumbs" style="color:inherit"><a href="index.html">HOME</a><span>/</span><a href="clients.html">OUR CLIENTS</a>'
            f'<span>/</span><span>{e(c["name"]).upper()}</span></div>')


# ------------------------------------------------------------------------------------------- V2
def v2(c, i, n):
    s = c['slug']; x = EXTRA[s]; (l1, l2), lede, proof, word, img2 = HERO[s]
    proof_btn = f'<a class="v2-btn solid" data-magnet href="{proof[0]}" target="_blank" rel="noopener">{e(proof[1])} ↗</a>' if proof else ''
    side = ' · '.join([c['tag'], c['world'], 'HARRIS MEDIA GROUP']) + ' · '
    out = [f'''<section class="v2-hero"><div class="v-grain"></div><div class="v2-outline" aria-hidden="true">{e(x['big'])}</div>
<div class="wrap v2-grid">
  <div>{crumbs(c)}<div class="v2-idx">CASE {i + 1:02d} / {n:02d} — {e(c['world'])}</div>
    <h1 class="v2-title" data-split>{e(l1)}<br><em>{e(l2)}</em></h1>
    <p class="v2-lede">{e(lede)}</p>
    <div class="v2-actions">{proof_btn}<a class="v2-btn" data-magnet href="#brief">The story ↓</a></div></div>
  <figure class="v2-photo" data-depth="-14"><img src="{c['logo']}" alt="{e(c['name'])}"><figcaption><span>{e(c['tag'])}</span><span>{i + 1:02d}</span></figcaption></figure>
</div>
<div class="v2-side" aria-hidden="true"><div>{e(side * 8)}</div></div>
<div class="v2-cue" aria-hidden="true">SCROLL<i></i></div></section>''']
    k, title, paras = x['brief']
    fig = f'<figure class="v2-figure" data-reveal><img src="{img2}" alt="{e(c["name"])} campaign" loading="lazy"></figure>' if img2 else ''
    out.append(f'''<section class="v2-sec" id="brief"><div class="wrap v2-sticky">
<div class="pin"><span class="v2-k">{e(k)}</span><h2 class="v2-h" data-reveal>{e(title)}</h2></div>
<div>{''.join(f'<p data-reveal>{e(p)}</p>' for p in paras)}{fig}</div></div></section>''')
    panels = []
    for v, lbl in facts_of(s):
        ca = count_attr(v)
        num = f'<span data-count="{ca[0]}" data-suffix="{ca[1]}">{e(v)}</span>' if ca else e(v)
        panels.append(f'<div class="v2-panel fact"><div class="lbl">FACT</div><div><div class="pn">{num}</div><div class="lbl" style="margin-top:14px">{e(lbl)}</div></div></div>')
    for j, (t, d) in enumerate(x['steps']):
        panels.append(f'<div class="v2-panel"><div class="pn">{j + 1:02d}</div><div><h3>{e(t)}</h3><p>{e(d)}</p></div></div>')
        if j == 1:
            panels.append(f'<div class="v2-panel photo"><img src="{img2 or c["logo"]}" alt="" loading="lazy"></div>')
    out.append(f'''<section class="v2-hs"><div class="v2-hs-pin"><div class="v2-hs-head"><div><span class="v2-k">The file</span><h2 class="v2-h" style="font-size:clamp(2rem,4vw,3.4rem)">Facts & playbook</h2></div><div class="v2-hs-bar"><i></i></div></div>
<div class="v2-hs-track">{''.join(panels)}</div></div></section>''')
    rows = ''.join(f'''<div class="v2-acc-row{' open' if j == 0 else ''}"><button type="button" aria-expanded="{'true' if j == 0 else 'false'}"><span class="an">{j + 1:02d}</span><span class="at">{e(t)}</span><span class="ai">+</span></button>
<div class="ab"><div><p>{e(d)}</p></div></div></div>''' for j, (t, d) in enumerate(x['steps']))
    out.append(f'<section class="v2-sec" style="padding-top:clamp(60px,8vw,110px)"><div class="wrap"><span class="v2-k">The playbook</span><h2 class="v2-h" style="margin-bottom:40px">What we did</h2><div class="v2-acc">{rows}</div></div></section>')
    if x.get('timeline'):
        tl = ''.join(f'<div data-reveal><b>{e(y)}</b><h3>{e(t)}</h3><p>{e(d)}</p></div>' for y, t, d in x['timeline'])
        out.append(f'<section class="v2-sec" style="padding-top:0"><div class="wrap"><span class="v2-k">Timeline</span><h2 class="v2-h" style="margin-bottom:40px">The story so far</h2><div class="v2-tl">{tl}</div></div></section>')
    if x.get('quote'):
        q, src = x['quote']
        out.append(f'<section class="v2-sec" style="padding-top:0"><div class="wrap"><blockquote class="v2-quote" data-reveal>“{e(q)}”<cite>— {e(src)}</cite></blockquote></div></section>')
    svc = ''.join(f'<li><a href="services.html#{SV[t]}">{e(t)}<span>↗</span></a></li>' for t in x['services'])
    out.append(f'<section class="v2-sec" style="padding-top:0"><div class="wrap"><span class="v2-k">Disciplines deployed</span><h2 class="v2-h" style="margin-bottom:30px">The team behind it</h2><ul class="v2-svc">{svc}</ul></div></section>')
    words = [w for w in re.split(r'[.—]\s*', x['closing']) if w.strip()]
    marq = ''.join(f'<span>{e(w.strip())}</span>' for w in words * 3)
    out.append(f'<div class="v2-marq" aria-label="{e(x["closing"])}"><div data-skew><div class="v2-marq-in">{marq}{marq}</div></div></div>')
    return f'<div class="v2" style="{theme_style(s)}">' + '\n'.join(out)


# ------------------------------------------------------------------------------------------- V3
def v3(c, i, n):
    s = c['slug']; x = EXTRA[s]; (l1, l2), lede, proof, word, img2 = HERO[s]
    bg, fg, a, a2, ink, hf, bf = THEME[s]
    proof_btn = f'<a class="v3-btn solid" data-magnet href="{proof[0]}" target="_blank" rel="noopener">{e(proof[1])} ↗</a>' if proof else ''
    font = '900 200px ' + (hf or '"Barlow Semi Condensed", sans-serif')
    fs = facts_of(s)
    hud = ''.join(f'<div>{e(l).upper()} <b>{e(v)}</b></div>' for v, l in fs[:3])
    out = [f'''<section class="v3-hero"><canvas class="v3-canvas" data-word="{e(word)}" data-colors="{a},{a2},{fg}" data-font='{e(font)}' aria-hidden="true"></canvas>
<div class="v3-hud" aria-hidden="true"><div>CLIENT <b>{i + 1:02d}/{n:02d}</b></div>{hud}</div>
<div class="wrap"><div class="v3-copy">{crumbs(c)}
<span class="v3-kick"><i></i>{e(c['tag'])}</span>
<h1 class="v3-title" data-split>{e(l1)} <span style="color:var(--a)">{e(l2)}</span></h1>
<p class="v3-lede">{e(lede)}</p>
<div class="v3-actions">{proof_btn}<a class="v3-btn" data-magnet href="#bento">Explore the file ↓</a></div></div></div>
<div class="v3-hint" aria-hidden="true">move your cursor through the letters</div></section>''']
    k, title, paras = x['brief']
    cells = [f'<div class="bx photo h2" data-reveal data-tilt><img src="{c["logo"]}" alt="{e(c["name"])}" loading="lazy"><span class="cap">{e(c["name"]).upper()}</span></div>',
             f'<div class="bx w2" data-reveal><div class="bl">{e(k)}</div><h3>{e(title)}</h3><p>{e(paras[0])}</p></div>']
    for j, (v, l) in enumerate(fs[:3]):
        ca = count_attr(v)
        num = f'<span data-count="{ca[0]}" data-suffix="{ca[1]}">{e(v)}</span>' if ca else e(v)
        cells.append(f'<div class="bx{" acc" if j == 0 else ""}" data-reveal data-tilt><div class="bl">{e(l).upper()}</div><div class="bn">{num}</div></div>')
    if len(paras) > 1:
        cells.append(f'<div class="bx w2" data-reveal><div class="bl">CONTEXT</div><p style="font-size:1.05rem">{e(paras[1])}</p></div>')
    if img2:
        cells.append(f'<div class="bx photo w2" data-reveal data-tilt><img src="{img2}" alt="" loading="lazy"><span class="cap">FROM THE CASE</span></div>')
    if x.get('quote'):
        q, src = x['quote']
        cells.append(f'<div class="bx w2 acc" data-reveal><div class="bl">QUOTE</div><h3 style="font-size:clamp(1.2rem,2vw,1.6rem);line-height:1.2">“{e(q)}”</h3><p>— {e(src)}</p></div>')
    if proof:
        cells.append(f'<a class="bx" href="{proof[0]}" target="_blank" rel="noopener" data-reveal data-tilt><div class="bl">PROOF</div><h3>{e(proof[1])}</h3><span class="go">↗</span></a>')
    cells.append(f'<a class="bx" href="contact.html" data-reveal data-tilt><div class="bl">NEXT STEP</div><h3>Build yours</h3><span class="go">→</span></a>')
    out.append(f'<section class="v3-sec" id="bento"><div class="wrap"><div class="v3-k">client_file.{s}</div><h2 class="v3-h">The file</h2><div class="bento">{"".join(cells)}</div></div></section>')
    steps = ''.join(f'<article class="v3-step" data-node="{(j + .5) / len(x["steps"]):.2f}"><div class="sn">STEP_{j + 1:02d}</div><h3>{e(t)}</h3><p>{e(d)}</p></article>' for j, (t, d) in enumerate(x['steps']))
    out.append(f'''<section class="v3-sec" style="padding-top:20px"><div class="wrap"><div class="v3-k">playbook</div><h2 class="v3-h">What we did</h2>
<div class="v3-path" data-scrub-host><svg viewBox="0 0 120 1000" preserveAspectRatio="none" aria-hidden="true"><path class="ghost" d="M60 0 C 120 160, 0 340, 60 500 S 0 840, 60 1000"/><path data-scrub d="M60 0 C 120 160, 0 340, 60 500 S 0 840, 60 1000"/></svg>
<div class="v3-steps">{steps}</div></div></div></section>''')
    if x.get('timeline'):
        tl = ''.join(f'<div class="bx" data-reveal data-tilt><div class="bl">{e(y)}</div><h3 style="font-size:1.2rem">{e(t)}</h3><p>{e(d)}</p></div>' for y, t, d in x['timeline'])
        out.append(f'<section class="v3-sec" style="padding-top:0"><div class="wrap"><div class="v3-k">timeline</div><h2 class="v3-h">The story so far</h2><div class="bento">{tl}</div></div></section>')
    pills = ''.join(f'<a data-magnet href="services.html#{SV[t]}">{e(t)} ↗</a>' for t in x['services'])
    out.append(f'<section class="v3-sec" style="padding-top:0"><div class="wrap"><div class="v3-k">disciplines_deployed</div><h2 class="v3-h">The team behind it</h2><div class="v3-pills">{pills}</div></div></section>')
    out.append(f'<section class="v3-sec"><div class="wrap"><p class="v3-fill" data-fill>{e(x["closing"])}</p></div></section>')
    return f'<div class="v3" style="{theme_style(s)}"><div class="v-cursor" aria-hidden="true"></div>' + '\n'.join(out)


def upgrade_v1(html):
    """Add film grain and character reveal to a V1 world without touching its design."""
    html = html.replace('<section class="w-hero">', '<section class="w-hero"><div class="v-grain"></div>')
    html = re.sub(r'class="w-title([^"]*)"', r'class="w-title\1" data-split', html)
    return html.replace('<h1 class="headline">', '<h1 class="headline" data-split>')
