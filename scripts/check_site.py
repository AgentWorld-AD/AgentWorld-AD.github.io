"""Validate the buildless page and its local references using the standard library."""
from html.parser import HTMLParser
from pathlib import Path
import json, re
root=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.refs=[];self.tags=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);self.tags.append((tag,attrs))
        if 'id' in attrs:self.ids.append(attrs['id'])
        for key in ('src','href'):
            if attrs.get(key):self.refs.append(attrs[key])
p=Page(); source=(root/'index.html').read_text();p.feed(source)
assert len(p.ids)==len(set(p.ids)), 'Duplicate IDs'
for ref in p.refs:
    if ref.startswith('#'): assert ref[1:] in p.ids, f'Missing anchor {ref}'
    elif not re.match(r'^[a-z]+:',ref):assert (root/ref).is_file(),f'Missing asset {ref}'
for tag,attrs in p.tags:
    if tag=='img':assert attrs.get('alt') is not None, 'Missing alt text'
    if attrs.get('role')=='tab':assert attrs['aria-controls'] in p.ids
for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>',source,re.S):json.loads(data)
assert 'YOUR_' not in source and 'TODO' not in source
assert 'NeurIPS 2026' in source and 'CVPR' not in source
for value in ['81.17','61.36','54.39','0.40','0.11','653','98']:assert value in source
assert 'paper: \'\', code: \'\'' in (root/'static/js/index.js').read_text()
print(f'OK: {len(p.ids)} unique IDs, {len(p.refs)} references, all local assets and anchors, alt text, structured data, venue and result values.')
