import base64, glob, os, sys

SRC = sys.argv[1]
OUT = sys.argv[2]
TILES = sorted(glob.glob(os.path.join(sys.argv[3], "*.webp")))
os.makedirs(OUT, exist_ok=True)
html = open(SRC, encoding="utf-8").read()

def uri(p):
    return "data:image/webp;base64," + base64.b64encode(open(p, "rb").read()).decode()

imgs = [uri(p) for p in TILES]
# Placeholder labels (replace with real project names)
LABELS = ["TV SPOT", "SOCIAL", "CREATIVE", "BRAND", "DIGITAL", "CAMPAIGN", "VIDEO", "PORTRAIT",
          "ADVERTISING", "CREATIVE", "SOCIAL", "FILM", "TV + CTV", "BRAND", "VIDEO", "SOCIAL", "CAMPAIGN"]

def tile(i, kind, slot):
    """kind: 'video' (wide 16:9, ready for an mp4) or 'image' (square)."""
    label = LABELS[i % len(LABELS)]
    media = f'<span class="hw-img hw-i{i+1}" role="img" aria-label="Harris Media Group work sample {i+1:02d}"></span>'
    if kind == "video":
        # Drop the file at videos/work-XX.mp4 and it plays automatically; until then the image shows.
        media += (f'<video class="hw-vid" muted loop playsinline autoplay preload="metadata">'
                  f'<source src="videos/work-{slot:02d}.mp4" type="video/mp4"></video>'
                  f'<span class="hw-play" aria-hidden="true"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>')
    tag = "VIDEO" if kind == "video" else label
    return (f'<a class="hw-tile hw-{kind}" href="our-works.html" tabindex="-1" aria-label="Work sample {i+1:02d}">'
            f'{media}<span class="hw-tag">{slot:02d} · {tag}</span></a>')

# 3 rows x 6 tiles, pattern VIDEO · IMAGE · VIDEO · IMAGE ... (row 2 offset so columns stagger)
rows_idx = [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11], [12, 13, 14, 15, 16, 0]]
rows_html = ""
slot = 0
for r, idx in enumerate(rows_idx):
    tiles = []
    for p, i in enumerate(idx):
        kind = "video" if (p + r) % 2 == 0 else "image"
        if kind == "video":
            slot += 1
        tiles.append(tile(i, kind, slot if kind == "video" else i + 1))
    seq = "".join(tiles) * 2  # wide enough to cover any screen
    # duplicated set -> seamless loop; second copy hidden from screen readers
    rows_html += (f'<div class="hw-row hw-row-{r+1}"><div class="hw-track">'
                  f'<div class="hw-set">{seq}</div><div class="hw-set" aria-hidden="true">{seq}</div>'
                  f'</div></div>')

CSS = """
/* ===== OUR WORKS GALLERY WALL ===== */
#slide-works{overflow-x:hidden}
#slide-works .hw-wall{position:relative;display:flex;flex-direction:column;gap:14px;overflow:hidden;
  width:100vw;margin-left:calc(50% - 50vw);
  -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 8%,#000 92%,transparent 100%);
          mask-image:linear-gradient(90deg,transparent 0,#000 8%,#000 92%,transparent 100%);}
#slide-works .hw-row{overflow:hidden}
#slide-works .hw-track{display:flex;width:max-content;animation:hwScroll 160s linear infinite}
#slide-works .hw-row-2 .hw-track{animation-direction:reverse;animation-duration:185s}
#slide-works .hw-row-3 .hw-track{animation-duration:140s}
#slide-works .hw-wall:hover .hw-track{animation-play-state:paused}
#slide-works .hw-set{display:flex;gap:14px;padding-right:14px}
#slide-works .hw-tile{position:relative;display:block;flex:0 0 auto;height:clamp(130px,21vh,240px);aspect-ratio:1/1;
  overflow:hidden;background:#141414;border:1px solid #2A2A2A;transition:transform .35s ease,border-color .35s ease,filter .35s ease;filter:saturate(.85) brightness(.82)}
#slide-works .hw-img{position:absolute;inset:0;background-size:cover;background-position:center;transition:transform .6s ease}
#slide-works .hw-tile:hover{border-color:#FE572E;filter:none;transform:translateY(-3px);box-shadow:0 0 24px rgba(254,87,46,.25)}
#slide-works .hw-tile:hover .hw-img{transform:scale(1.06)}
#slide-works .hw-tag{position:absolute;left:0;right:0;bottom:0;padding:6px 8px;font-size:.5rem;letter-spacing:.2em;font-weight:700;
  color:#fff;background:linear-gradient(transparent,rgba(0,0,0,.85));opacity:0;transform:translateY(6px);transition:all .3s ease}
#slide-works .hw-tile:hover .hw-tag{opacity:1;transform:none}
#slide-works .hw-video{aspect-ratio:16/9}
#slide-works .hw-vid{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .5s ease}
#slide-works .hw-vid.is-ready{opacity:1}
#slide-works .hw-play{position:absolute;left:12px;top:12px;width:34px;height:34px;display:flex;align-items:center;justify-content:center;
  font-size:22px;color:#fff;background:rgba(254,87,46,.9);transition:opacity .3s ease}
#slide-works .hw-vid.is-ready ~ .hw-play{opacity:0}
#slide-works .hw-tag{font-size:.6rem;padding:8px 10px}
@keyframes hwScroll{from{transform:translate3d(0,0,0)}to{transform:translate3d(-50%,0,0)}}
@media (hover:none){#slide-works .hw-tile{filter:none}}
@media (prefers-reduced-motion: reduce){#slide-works .hw-track{animation:none}#slide-works .hw-row{overflow-x:auto}}
html:not(.dark) #slide-works{background-color:#F6F6F6 !important}
html:not(.dark) #slide-works .hw-tile{border-color:#E2E2E2;background:#EAEAEA}
"""

SECTION = f"""<!-- ==========================================
         SLIDE 5: OUR WORKS (GALLERY WALL)
    =========================================== --><section class="h-[100dvh] w-screen min-h-[100dvh] max-h-[100dvh] overflow-y-auto lg:overflow-hidden flex flex-col justify-center relative bg-[#0A0A0A] px-4 sm:px-8 md:px-12 lg:px-20 pb-6 border-b border-outline-variant/30 shrink-0 pt-28" id="slide-works"><div class="max-w-7xl w-full mx-auto flex flex-col h-full max-h-[86vh] py-2"><div class="flex flex-wrap gap-3 items-center justify-between pb-3 border-b border-outline-variant/30 mb-5"><div class="flex items-center space-x-3"><span class="font-label-sm text-label-sm tracking-[0.2em] text-primary-container uppercase font-bold">PORTFOLIO</span><span class="text-outline">//</span><h2 class="font-organetto text-lg md:text-2xl text-on-surface uppercase tracking-[0.08em] font-bold">OUR WORKS</h2></div><a class="hmg-cta px-3 sm:px-4 py-1.5 bg-primary-container hover:bg-on-surface text-[#0A0A0A] font-organetto text-[0.6875rem] tracking-[0.18em] font-extrabold uppercase border border-primary-container flex items-center space-x-2 transition-colors whitespace-nowrap" href="our-works.html"><span>VIEW ALL WORKS</span><span class="material-symbols-outlined text-sm">arrow_forward</span></a></div><div class="hw-wall my-auto">{rows_html}</div><p class="font-label-sm text-label-sm text-outline tracking-widest uppercase mt-4 text-center">CREATIVE · VIDEO · SOCIAL · BRAND</p></div></section>"""

def must_replace(s, old, new, count=1):
    n = s.count(old)
    assert n == count, (old[:80], n)
    return s.replace(old, new)

# 1) renumber slide indexes (team 4->5, contact 5->6) before inserting new slide
html = must_replace(html, 'data-slide="5"', 'data-slide="6"', 2)
html = must_replace(html, 'data-slide="4"', 'data-slide="5"', 2)
html = must_replace(html, 'title="Slide 06: Contact"', 'title="Slide 07: Contact"')
html = must_replace(html, '>06 · CONTACT<', '>07 · CONTACT<')
html = must_replace(html, 'title="Slide 05: Team"', 'title="Slide 06: Team"')
html = must_replace(html, '>05 · TEAM<', '>06 · TEAM<')

# 2) indicator dot for the new slide, right before the team dot
team_dot = '<button class="indicator-dot group flex items-center space-x-2 text-right transition-all hover:text-on-surface cursor-pointer py-1 text-outline" data-slide="5" title="Slide 06: Team">'
works_dot = ('<button class="indicator-dot group flex items-center space-x-2 text-right transition-all hover:text-on-surface cursor-pointer py-1 text-outline" data-slide="4" title="Slide 05: Our Works">'
             '<span class="hidden group-hover:inline-block font-label-sm text[0.5625rem] tracking-widest uppercase bg-[#000]/95 px-2 py-0.5 border border-[#333]">05 · WORKS</span>'
             '<span class="w-2.5 h-2.5 border border-outline-variant/60 bg-transparent transition-all"></span></button>')
html = must_replace(html, team_dot, works_dot + team_dot)

# 3) nav tab "OUR WORKS" -> subpage, placed after OUR SERVICES
svc = 'data-slide="3" href="#slide-4">OUR SERVICES</a>'
i = html.index(svc) + len(svc)
start = html.rindex("<a ", 0, i)
svc_anchor = html[start:i]
cls = svc_anchor.split('class="', 1)[1].split('"', 1)[0]
works_tab = f'<a class="{cls}" href="our-works.html">OUR WORKS</a>'
html = html[:i] + works_tab + html[i:]

# 4) insert section between Services (slide-4) and Team
marker = "<!-- ==========================================\n         SLIDE 5: OUR TEAM"
html = must_replace(html, marker, SECTION + "<!-- ==========================================\n         SLIDE 6: OUR TEAM")

VIDJS = """<script>document.querySelectorAll('#slide-works .hw-vid').forEach(function(v){
  var ok=function(){v.classList.add('is-ready');};
  if(v.readyState>=2)ok();else v.addEventListener('loadeddata',ok,{once:true});
});</script>"""
html = must_replace(html, "</body>", VIDJS + "</body>")

# 5) CSS (each image defined once)
CSS += "".join(f"#slide-works .hw-i{k+1}{{background-image:url({u})}}\n" for k, u in enumerate(imgs))
html = must_replace(html, "/* Light Mode Overrides */", CSS + "\n/* Light Mode Overrides */")

# 6) team photos: remove black & white filter
team_old = "w-full h-full object-cover grayscale contrast-125 group-hover:scale-105 group-hover:contrast-100 transition-all duration-300"
html = must_replace(html, team_old, "w-full h-full object-cover group-hover:scale-105 transition-all duration-300", 3)

# 7) OUR CLIENTS: nav tab and in-page links go straight to the clients page
html = must_replace(html, 'data-slide="2" href="#slide-3">OUR CLIENTS</a>', 'href="clients.html">OUR CLIENTS</a>')
html = must_replace(html, 'data-slide="2" href="#slide-3">SEE OUR CLIENTS →', 'href="clients.html">SEE OUR CLIENTS →')
CTA_CLS = ("hmg-cta px-3 sm:px-4 py-1.5 bg-primary-container hover:bg-on-surface text-[#0A0A0A] font-organetto "
           "tracking-[0.18em] font-extrabold uppercase border border-primary-container flex items-center space-x-2 transition-colors whitespace-nowrap")
html = must_replace(html, '<span class="font-label-sm text-label-sm text-outline tracking-widest uppercase">04 FEATURED CAMPAIGNS</span>',
                    f'<a class="{CTA_CLS}" href="clients.html"><span class="w-1.5 h-1.5 bg-[#0A0A0A] animate-telemetry"></span><span>VIEW OUR CLIENTS →</span></a>')
html = must_replace(html, '''<span class="">WHO WE'VE WORKED WITH</span>''',
                    '''<a class="text-primary-container font-bold hover:text-on-surface transition-colors" href="clients.html">WHO WE'VE WORKED WITH · VIEW ALL 15 CLIENTS →</a>''')

open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)

# ---------- subpage ----------
CATS = ["VIDEO", "SOCIAL", "CREATIVE", "BRAND", "SOCIAL", "CREATIVE", "VIDEO", "BRAND", "SOCIAL",
        "VIDEO", "CREATIVE", "VIDEO", "BRAND", "CREATIVE", "VIDEO", "SOCIAL", "BRAND"]
cards = ""
for k, src in enumerate(imgs):
    cards += (f'<article class="card" data-cat="{CATS[k]}"><div class="ph"><img src="{src}" alt="Work sample {k+1:02d}" loading="lazy"></div>'
              f'<div class="meta"><span class="num">{k+1:02d}</span><div><h3>PROJECT TITLE {k+1:02d}</h3>'
              f'<p>CLIENT NAME · 2026</p></div><span class="cat">{CATS[k]}</span></div></article>')

page = open(os.path.join(os.path.dirname(__file__), "our-works.template.html"), encoding="utf-8").read()
page = page.replace("{{CARDS}}", cards)
open(os.path.join(OUT, "our-works.html"), "w", encoding="utf-8").write(page)
print("ok", len(html), len(page))
