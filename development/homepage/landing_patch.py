"""Landing tweaks applied after the build:
- top bar: OUR SERVICES opens services.html and a NEWS tab opens blog.html
- right edge: square section navigator (up / 7 sections / down) in the HMG style
Usage: python3 landing_patch.py out/index.html
"""
import re
import sys

p = sys.argv[1]
s = open(p, encoding='utf-8').read()

# ---- top bar -------------------------------------------------------------
nav_a = re.search(r'<a class="([^"]*nav-slide-link whitespace-nowrap)" data-slide="3" href="#slide-4">OUR SERVICES</a>', s)
assert nav_a, 'services tab not found'
s = s.replace(nav_a.group(0), f'<a class="{nav_a.group(1)}" href="services.html">OUR SERVICES</a>', 1)
car = re.search(r'<a class="([^"]*nav-slide-link whitespace-nowrap)" href="careers.html">CAREERS</a>', s)
assert car, 'careers tab not found'
if 'href="blog.html">NEWS</a>' not in s:
    s = s.replace(car.group(0), car.group(0) + f'<a class="{car.group(1)}" href="blog.html">NEWS</a>', 1)

# ---- section navigator ---------------------------------------------------
names = ['HOME', 'WAR ROOM', 'CLIENTS', 'SERVICES', 'WORKS', 'TEAM', 'CONTACT']
chev = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="{}"/></svg>'
dots = ''.join(
    f'<button type="button" class="indicator-dot{" text-primary-container" if k == 0 else " text-outline"}" data-slide="{k}" aria-label="Go to {n.title()}" title="{k + 1:02d} · {n}">'
    f'<span class="rail-lbl"><i>{k + 1:02d}</i>{n}</span><span class="rail-sq"></span></button>' for k, n in enumerate(names))
rail = (f'<nav id="hmg-rail" aria-label="Page sections">'
        f'<button type="button" class="rail-arrow" data-dir="-1" aria-label="Previous section">{chev.format("M6 15l6-6 6 6")}</button>'
        f'<div class="rail-count" aria-hidden="true"><b>01</b><span>/{len(names):02d}</span></div>'
        f'<div class="rail-dots"><span class="rail-line"><i></i></span>{dots}</div>'
        f'<button type="button" class="rail-arrow" data-dir="1" aria-label="Next section">{chev.format("M6 9l6 6 6-6")}</button></nav>')
old = re.search(r'<div class="[^"]*" id="slide-indicators">.*?</div><!-- FULL VIEWPORT', s, re.S)
assert old, 'slide indicators not found'
s = s.replace(old.group(0), rail + '<!-- FULL VIEWPORT', 1)

css = '''<style id="hmg-rail-css">
#hmg-rail{position:fixed;right:22px;top:50%;transform:translateY(-50%);z-index:45;display:flex;flex-direction:column;align-items:center;gap:10px;padding:12px 8px;background:rgba(10,10,10,.72);border:1px solid #2A2A2A;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
#hmg-rail::before,#hmg-rail::after{content:"";position:absolute;width:8px;height:8px;border-color:#FE572E;border-style:solid}
#hmg-rail::before{left:-1px;top:-1px;border-width:2px 0 0 2px}#hmg-rail::after{right:-1px;bottom:-1px;border-width:0 2px 2px 0}
.rail-arrow{width:30px;height:30px;display:grid;place-items:center;border:1px solid #3A3A3A;background:#101010;color:#E5E2E1;cursor:pointer;transition:background .2s,border-color .2s,color .2s}
.rail-arrow:hover:not([disabled]){background:#FE572E;border-color:#FE572E;color:#0A0A0A}
.rail-arrow[disabled]{opacity:.28;cursor:default}
.rail-arrow:focus-visible,#hmg-rail .indicator-dot:focus-visible{outline:2px solid #FE572E;outline-offset:2px}
.rail-count{font:700 10px/1 'organetto-variable','Organetto Variable','Barlow Semi Condensed',sans-serif;letter-spacing:.12em;color:#AB8981;text-align:center}
.rail-count b{display:block;font-size:13px;color:#FE572E;margin-bottom:2px}
.rail-dots{position:relative;display:flex;flex-direction:column;gap:9px;padding:4px 0}
.rail-line{position:absolute;left:50%;top:10px;bottom:10px;width:1px;margin-left:-.5px;background:#2A2A2A}
.rail-line i{display:block;width:100%;height:calc(var(--rp,0)*100%);background:#FE572E;transition:height .5s cubic-bezier(.2,.7,.1,1)}
#hmg-rail .indicator-dot{position:relative;display:grid;place-items:center;width:30px;height:20px;padding:0;margin:0;background:none;border:0;cursor:pointer}
#hmg-rail .indicator-dot>span:last-child{all:unset;position:relative;z-index:1;display:block;width:11px;height:11px;border:1.5px solid #5A5A5A;background:#0A0A0A;box-sizing:border-box;transition:transform .3s cubic-bezier(.2,1.4,.4,1),background .25s,border-color .25s,box-shadow .25s}
#hmg-rail .indicator-dot:hover>span:last-child{border-color:#E5E2E1;transform:scale(1.15)}
#hmg-rail .indicator-dot.text-primary-container>span:last-child{width:14px;height:14px;background:#FE572E;border-color:#FE572E;box-shadow:0 0 0 3px rgba(254,87,46,.18),0 0 14px rgba(254,87,46,.7);transform:rotate(45deg)}
#hmg-rail .indicator-dot.visited>span:last-child{border-color:#FE572E}
.rail-lbl{position:absolute;right:calc(100% + 14px);top:50%;transform:translate(8px,-50%);display:flex;align-items:center;gap:8px;white-space:nowrap;padding:7px 12px;background:#0A0A0A;border:1px solid #2A2A2A;border-left:2px solid #FE572E;font:700 10px/1 'organetto-variable','Organetto Variable','Barlow Semi Condensed',sans-serif;letter-spacing:.22em;color:#E5E2E1;opacity:0;pointer-events:none;transition:opacity .2s,transform .25s}
.rail-lbl i{font-style:normal;color:#FE572E}
#hmg-rail .indicator-dot:hover .rail-lbl,#hmg-rail .indicator-dot:focus-visible .rail-lbl{opacity:1;transform:translate(0,-50%)}
html:not(.dark) #hmg-rail{background:rgba(246,246,246,.85);border-color:#D0D0D0}
html:not(.dark) .rail-arrow{background:#fff;border-color:#D0D0D0;color:#111}
html:not(.dark) #hmg-rail .indicator-dot>span:last-child{background:#fff;border-color:#9A9A9A}
html:not(.dark) .rail-lbl{background:#fff;color:#111;border-color:#D0D0D0}
@media (max-width:1023px){#hmg-rail{right:10px;top:auto;bottom:16px;transform:none;flex-direction:row;gap:6px;padding:6px}.rail-dots,.rail-count{display:none}.rail-arrow{width:38px;height:38px}}
</style>'''
js = '''<script id="hmg-rail-js">
(function(){var rail=document.getElementById("hmg-rail");if(!rail)return;
var dots=[].slice.call(rail.querySelectorAll(".indicator-dot")),n=dots.length,cnt=rail.querySelector(".rail-count b"),arrows=rail.querySelectorAll(".rail-arrow");
function cur(){for(var k=0;k<n;k++)if(dots[k].classList.contains("text-primary-container"))return k;return 0}
var last=-1;function sync(){var k=cur();if(k===last)return;last=k;cnt.textContent=(k<9?"0":"")+(k+1);rail.style.setProperty("--rp",n>1?k/(n-1):0);
dots.forEach(function(d,j){var v=j<k;if(d.classList.contains("visited")!==v)d.classList.toggle("visited",v)});
arrows[0].disabled=k===0;arrows[1].disabled=k===n-1}
new MutationObserver(sync).observe(rail,{subtree:true,attributes:true,attributeFilter:["class"]});
[].forEach.call(arrows,function(a){a.addEventListener("click",function(){var k=cur()+parseInt(a.getAttribute("data-dir"),10);if(k>=0&&k<n)dots[k].click()})});
sync()})();
</script>'''
lock = ('<a class="staff-key" href="admin" title="Team access" aria-label="Team access">'
        '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="1"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg></a>')
cp = '<span class="">© 2026 HARRIS MEDIA GROUP</span>'
assert s.count(cp) == 1, 'copyright not found'
s = s.replace(cp, '<span class="">© 2026 HARRIS MEDIA GROUP' + lock + '</span>', 1)
css = css.replace('</style>', '.staff-key{display:inline-grid;place-items:center;width:20px;height:20px;margin-left:8px;vertical-align:middle;color:inherit;opacity:.22;transition:opacity .2s,color .2s}.staff-key:hover,.staff-key:focus-visible{opacity:1;color:#FE572E}</style>')
s = s.replace('</head>', css + '</head>', 1)
s = s.replace('</body>', js + '</body>', 1)
open(p, 'w', encoding='utf-8').write(s)
print('landing patched')
