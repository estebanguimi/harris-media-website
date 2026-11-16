#!/bin/bash
# Rebuilds generador/landing/index.html (the homepage) from portada-original.html.
# Only needed when the homepage design changes. Requires Python 3.11+ and Node.js 18+.
set -e
cd "$(dirname "$0")"
ROOT=../..
TMP=$(mktemp -d)
[ -d twbuild/node_modules ] || (cd twbuild && npm ci --silent)
python3 build.py portada-original.html "$TMP" "$ROOT/generador/tiles" >/dev/null
python3 inline_tw.py "$TMP/index.html" >/dev/null
python3 - "$TMP/index.html" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
for a, b in [('https://www.harrismediallc.com/careers/', 'careers.html'), ('https://www.harrismediallc.com/meet-the-team/', 'team.html'),
             ('https://www.harrismediallc.com/contact/', 'contact.html')]:
    assert s.count('href="%s"' % a) >= 1, a
    s = s.replace('href="%s"' % a, 'href="%s"' % b)
open(p, 'w', encoding='utf-8').write(s)
PY
python3 landing_patch.py "$TMP/index.html"
cp "$TMP/index.html" "$ROOT/generador/landing/index.html"
rm -rf "$TMP"
echo "Portada actualizada en generador/landing/index.html. Abre el panel y pulsa «Publicar cambios»."
