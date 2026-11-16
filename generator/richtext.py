"""Rich-text sanitizer shared by the admin panel and the site generator.

Only a small set of formatting tags survives; every other tag is unwrapped
(its text is kept) and script/style-like elements are dropped with their content.
"""
import re
from html import escape
from html.parser import HTMLParser

ALLOWED = {'p', 'br', 'h2', 'h3', 'h4', 'strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li', 'blockquote', 'a', 'img', 'figure', 'figcaption', 'hr'}
VOID = {'br', 'img', 'hr'}
DROP = {'script', 'style', 'iframe', 'object', 'embed', 'noscript', 'template', 'svg', 'math', 'form', 'input', 'button', 'select', 'textarea', 'head', 'title', 'meta', 'link'}
ATTRS = {'a': {'href'}, 'img': {'src', 'alt'}}
RENAME = {'b': 'strong', 'i': 'em', 'h1': 'h2'}


def safe_url(u, img=False):
    u = (u or '').strip()
    if not u:
        return ''
    low = re.sub(r'[\s\x00-\x1f]', '', u).lower()
    if low.startswith(('http://', 'https://')) or (not img and low.startswith(('mailto:', 'tel:', '#'))):
        return u
    if ':' not in low.split('/')[0] and not low.startswith('//'):
        return u  # relative path such as media/news/photo.webp or contact.html
    return ''


class _Clean(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.stack, self.skip = [], [], 0

    def handle_starttag(self, tag, attrs):
        if self.skip or tag in DROP:
            if tag not in VOID:
                self.skip += 1
            return
        tag = RENAME.get(tag, tag)
        if tag not in ALLOWED:
            return
        a = dict(attrs)
        keep = []
        if tag == 'a':
            href = safe_url(a.get('href'))
            if href:
                keep.append(f'href="{escape(href)}"')
                if href.startswith('http'):
                    keep.append('target="_blank" rel="noopener"')
        if tag == 'img':
            src = safe_url(a.get('src'), img=True)
            if not src:
                return
            keep.append(f'src="{escape(src)}"')
            keep.append(f'alt="{escape(a.get("alt") or "")}"')
            keep.append('loading="lazy"')
        self.out.append(f'<{tag}{" " + " ".join(keep) if keep else ""}>')
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if not self.skip and RENAME.get(tag, tag) in ALLOWED and RENAME.get(tag, tag) not in VOID and self.stack and self.stack[-1] == RENAME.get(tag, tag):
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.skip:
            if tag in DROP:
                self.skip -= 1
            return
        tag = RENAME.get(tag, tag)
        if tag in self.stack:
            while self.stack:
                t = self.stack.pop()
                self.out.append(f'</{t}>')
                if t == tag:
                    break

    def handle_data(self, data):
        if not self.skip:
            self.out.append(escape(data, quote=False))


def clean(html):
    p = _Clean()
    p.feed(html or '')
    p.close()
    out = ''.join(p.out) + ''.join(f'</{t}>' for t in reversed(p.stack))
    out = re.sub(r'<p>\s*(<br>\s*)*</p>', '', out)  # empty paragraphs
    out = re.sub(r'<p>\s*(<(h[234]|ul|ol|blockquote|figure)>)', r'\1', out)
    return out.strip()


def text(html):
    s = re.sub(r'<(br|/p|/h[234]|/li|/blockquote)[^>]*>', '\n', html or '')
    s = re.sub(r'<[^>]+>', '', s)
    from html import unescape
    return re.sub(r'[ \t]+', ' ', unescape(s)).strip()


def paragraphs(html):
    from html import unescape
    return [re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', '', m))).strip() for m in re.findall(r'<p>(.*?)</p>', html or '', re.S)]
