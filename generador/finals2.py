"""One-off modules for the second set of final pages + the per-page interaction ownership filter."""
import html as H
from extra import EXTRA, SV

e = lambda s: H.escape(str(s), quote=True)


def svc_term(c, d):
    rows = ''.join(f'<li><a href="services.html#{SV[s]}"><span>$ deploy</span> {e(s.lower().replace(" / ", "_").replace(" ", "_"))} <em>[OK]</em></a></li>' for s in EXTRA[c['slug']]['services'])
    return f'<section class="sx-svcterm"><div class="wrap"><span class="v2-k">disciplines_deployed</span><ul class="st-list">{rows}</ul></div></section>'


def tl_archive(c, d):
    tl = EXTRA[c['slug']]['timeline']
    items = ''.join(f'<li><span class="ar-y">{e(y)}</span><a class="ar-t">{e(t)}</a><span class="ar-c">({k + 1})</span><p>{e(dd)}</p></li>' for k, (y, t, dd) in enumerate(tl))
    return (f'<section class="sx-archive"><div class="wrap ar-grid"><div><span class="v2-k">Blog archive</span><h2 class="v2-h">The story, by date.</h2></div>'
            f'<div class="ar-box"><div class="ar-head">&#9662; ARCHIVE</div><ul>{items}</ul></div></div></section>')


def svc_blogroll(c, d):
    links = ''.join(f'<li><a href="services.html#{SV[s]}">{e(s)}</a> <small>— Harris Media Group</small></li>' for s in EXTRA[c['slug']]['services'])
    return f'<section class="sx-roll"><div class="wrap"><div class="rl"><b>Blogroll · the team behind it</b><ul>{links}</ul></div></div></section>'


def close_signoff(c, d):
    return (f'<section class="sx-sign"><div class="wrap"><p class="sg-txt">{e(EXTRA[c["slug"]]["closing"])}</p>'
            '<svg class="sg-sig" viewBox="0 0 520 120" aria-hidden="true"><path d="M10 80 C40 20 70 20 80 70 S120 110 140 60 S180 10 200 70 S240 100 270 50 S320 30 330 80 S380 90 400 50 S470 40 510 70"/></svg>'
            '<div class="sg-meta">Posted by <b>Harris Media Group</b> · Filed under: Iowa, 2008 · <a href="contact.html">Leave a comment →</a></div></div></section>')


def quote_engrave(c, d):
    q, src = EXTRA[c['slug']]['quote']
    return f'<section class="sx-engrave"><div class="wrap"><div class="eg-plate" data-reveal><p>“{e(q)}”</p><span>— {e(src)}</span></div></div></section>'


def tl_logbook(c, d):
    st = EXTRA[c['slug']]['steps']
    rows = ''.join(f'<tr data-reveal><td>{k + 1:02d}</td><td>{e(t)}</td><td>{e(dd)}</td><td>{"44.31° N" if k % 2 else "69.78° W"}</td></tr>' for k, (t, dd) in enumerate(st))
    return (f'<section class="sx-log"><div class="wrap"><span class="v2-k">Ship’s logbook</span><h2 class="v2-h">Entries from New England.</h2>'
            f'<table class="lb-t"><thead><tr><th>No.</th><th>Entry</th><th>Remarks</th><th>Position</th></tr></thead><tbody>{rows}</tbody></table></div></section>')


def svc_tags(c, d):
    tags = ''.join(f'<a class="tg" href="services.html#{SV[s]}" style="--k:{k}"><i></i>{e(s)}</a>' for k, s in enumerate(EXTRA[c['slug']]['services']))
    return f'<section class="sx-tags"><div class="wrap"><span class="v2-k">Disciplines deployed</span><div class="tg-row">{tags}</div></div></section>'


def close_lighthouse(c, d):
    t = e(EXTRA[c['slug']]['closing'])
    return f'<section class="sx-light" data-beam><div class="wrap"><p class="lh-txt">{t}</p><p class="lh-lit" aria-hidden="true">{t}</p></div><div class="lh-hint" aria-hidden="true">MOVE THE LIGHT</div></section>'


def svc_playbill(c, d):
    cast = ''.join(f'<li><span>{e(s)}</span><i></i><b>HMG</b></li>' for s in EXTRA[c['slug']]['services'])
    return (f'<section class="sx-bill"><div class="wrap"><div class="pb"><div class="pb-top">PLAYBILL</div><h2>Statewide</h2><em>A production of Harris Media Group</em>'
            f'<div class="pb-sub">THE COMPANY</div><ul>{cast}</ul></div></div></section>')


def close_credits(c, d):
    x = EXTRA[c['slug']]
    lines = [('A HARRIS MEDIA GROUP PRODUCTION', ''), ('Starring', c['name']), ('Setting', 'Connecticut · Statewide')]
    lines += [(t.split('·')[0].strip().title(), t.split('·')[-1].strip().title()) for t, _ in x['steps']]
    lines += [('Also in Connecticut', 'Bob Stefanowski'), ('', x['closing'])]
    roll = ''.join(f'<div class="cr-l"><span>{e(a)}</span><b>{e(b)}</b></div>' for a, b in lines)
    return f'<section class="sx-credits"><div class="cr-win" aria-label="{e(x["closing"])}"><div class="cr-roll">{roll}{roll}</div></div></section>'


MODULES2 = dict(svc_term=svc_term, tl_archive=tl_archive, svc_blogroll=svc_blogroll, close_signoff=close_signoff, quote_engrave=quote_engrave,
                tl_logbook=tl_logbook, svc_tags=svc_tags, close_lighthouse=close_lighthouse, svc_playbill=svc_playbill, close_credits=close_credits)


def personalize(html, f):
    """Give each final page sole ownership of its interactions."""
    if not f.get('tilt'):
        html = html.replace(' data-tilt', '')
    if not f.get('magnet'):
        html = html.replace(' data-magnet', '')
    if not f.get('cursor'):
        html = html.replace('<div class="v-cursor" aria-hidden="true"></div>', '')
    if not f.get('par'):
        html = html.replace(' data-depth=', ' data-nodepth=')
    return html
