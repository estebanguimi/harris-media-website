import re, subprocess, sys, os
D = os.path.dirname(os.path.abspath(__file__))
TW = os.path.join(D, "twbuild")
path = sys.argv[1]
html = open(path, encoding="utf-8").read()

cfg_m = re.search(r'<script id="tailwind-config">\s*tailwind\.config\s*=\s*(.*?)</script>', html, re.S)
cfg = cfg_m.group(1).strip().rstrip(";")
# scan a copy without base64 blobs (faster, same classes)
scan = re.sub(r'data:[^"\')]{200,}', 'DATA', html)
open(os.path.join(TW, "scan.html"), "w", encoding="utf-8").write(scan)
open(os.path.join(TW, "tailwind.config.js"), "w").write(
    "const c = " + cfg + ";\nc.content=['./scan.html'];\n"
    "c.plugins=[require('@tailwindcss/forms'),require('@tailwindcss/container-queries')];\nmodule.exports=c;\n")
open(os.path.join(TW, "in.css"), "w").write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n")
subprocess.run([os.path.join(TW, "node_modules/.bin/tailwindcss"), "-i", "in.css", "-o", "out.css", "--minify"],
               cwd=TW, check=True, capture_output=True)
css = open(os.path.join(TW, "out.css")).read()

cdn = '<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>'
assert html.count(cdn) == 1
html = html.replace(cdn, "")
html = html.replace(cfg_m.group(0), "")
# the play CDN appends its stylesheet at the end of <head>; keep the same cascade order
i = html.index("</head>")
html = html[:i] + '<style id="tailwind-compiled">' + css + "</style>" + html[i:]
open(path, "w", encoding="utf-8").write(html)
print("inlined", len(css), "bytes of CSS")
