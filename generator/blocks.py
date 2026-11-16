"""Extract ordered content blocks (h1-h4, p, li, img, blockquote) from a WordPress page."""
import re, html as H
from html.parser import HTMLParser

SKIP = {'script', 'style', 'noscript', 'svg', 'header', 'footer', 'nav', 'form', 'head', 'button', 'select', 'iframe'}
BLOCKS = {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'li', 'blockquote', 'div', 'section', 'figcaption', 'td'}
INLINE_KEEP = {'strong': 'strong', 'b': 'strong', 'em': 'em', 'i': 'em'}


class _P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0; self.out = []; self.buf = ''; self.kind = 'p'; self.stack = []

    def flush(self):
        t = re.sub(r'\s+', ' ', self.buf).strip()
        if t and re.sub(r'<[^>]+>', '', t).strip():
            self.out.append((self.kind, t))
        self.buf = ''; self.kind = 'p'

    def handle_starttag(self, t, a):
        a = dict(a)
        if t in SKIP:
            self.skip += 1; return
        if self.skip:
            return
        if t in BLOCKS:
            self.flush()
            self.kind = {'li': 'li', 'blockquote': 'quote'}.get(t, t if t in ('h1', 'h2', 'h3', 'h4', 'h5') else 'p')
            self.stack.append(t)
        elif t == 'br':
            self.buf += ' '
        elif t in INLINE_KEEP:
            self.buf += '<%s>' % INLINE_KEEP[t]
        elif t == 'a' and a.get('href', '').startswith('http') and 'harrismediallc.com' not in a.get('href', ''):
            self.buf += '<a href="%s" target="_blank" rel="noopener">' % H.escape(a['href'])
            self.stack.append('a-open')
        elif t == 'img':
            src = a.get('data-src') or a.get('src') or ''
            if src.startswith('//'):
                src = 'https:' + src
            if src.startswith('http'):
                self.flush(); self.out.append(('img', src + '|' + a.get('alt', '')))

    def handle_endtag(self, t):
        if t in SKIP:
            self.skip = max(0, self.skip - 1); return
        if self.skip:
            return
        if t in BLOCKS:
            self.flush()
        elif t in INLINE_KEEP:
            self.buf += '</%s>' % INLINE_KEEP[t]
        elif t == 'a' and 'a-open' in self.stack:
            self.stack.remove('a-open'); self.buf += '</a>'

    def handle_data(self, d):
        if not self.skip:
            self.buf += H.escape(d, quote=False)


def blocks(raw):
    p = _P(); p.feed(raw); p.flush()
    out = []
    for k, t in p.out:
        t = re.sub(r'<(strong|em)>\s*</\1>', '', t).strip()
        t = re.sub(r'</(strong|em)>(?=[A-Za-z0-9])', r'</\1> ', t)
        if not t or t in ('Skip to content',):
            continue
        if out and out[-1] == (k, t):
            continue
        out.append((k, t))
    return out
