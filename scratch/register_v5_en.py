# -*- coding: utf-8 -*-
"""en/index.html 등록 + sitemap 수정 (register_v5의 후반부 — ko는 이미 적용됨)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import register_v5 as R

R.patch_index(R.ROOT / 'en/index.html', 'en')

# ── sitemap.xml: hreflang 75블록 수정 + 신규 8블록 ──
import re
sp = R.ROOT / 'sitemap.xml'
s = sp.read_text(encoding='utf-8')
BASE = 'https://mttrails.trinos.group/'
fixed = 0
while True:
    # 블록 단위 순회 — 치환 후에도 남은 잘못된 블록을 계속 찾는다
    m = None
    for bm in re.finditer(r'<url>\s*<loc>(.*?)</loc>.*?</url>', s, re.S):
        loc = bm.group(1)
        stem = loc.split('.group/')[1]
        exp_ko = BASE + (stem.split('en/', 1)[1] if stem.startswith('en/') else stem)
        ko_m = re.search(r'hreflang="ko" href="([^"]*)"', bm.group(0))
        if ko_m and ko_m.group(1) != exp_ko:
            m = (bm, loc, exp_ko)
            break
    if not m:
        break
    bm, loc, exp_ko = m
    b = bm.group(0)
    b2 = re.sub(r'hreflang="ko" href="[^"]*"', f'hreflang="ko" href="{exp_ko}"', b)
    b2 = re.sub(r'hreflang="x-default" href="[^"]*"', f'hreflang="x-default" href="{exp_ko}"', b2)
    b2 = re.sub(r'<lastmod>[^<]*</lastmod>', '<lastmod>2026-09-19</lastmod>', b2)
    s = s.replace(b, b2)
    fixed += 1

new_blocks = []
for mid in ('namsan', 'gyebangsan', 'dutasan', 'manisan'):
    ko_stem, en_stem = f'{mid}-playbook.html', f'en/{mid}-playbook.html'
    new_blocks.append(f'''  <url>
    <loc>{BASE}{ko_stem}</loc>
    <xhtml:link rel="alternate" hreflang="ko" href="{BASE}{ko_stem}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE}{en_stem}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{ko_stem}"/>
    <lastmod>2026-09-19</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
''')
    new_blocks.append(f'''  <url>
    <loc>{BASE}{en_stem}</loc>
    <xhtml:link rel="alternate" hreflang="ko" href="{BASE}{ko_stem}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE}{en_stem}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{ko_stem}"/>
    <lastmod>2026-09-19</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
''')
s = s.replace('</urlset>', ''.join(new_blocks) + '</urlset>')
sp.write_text(s, encoding='utf-8')
print(f'sitemap: fixed {fixed} blocks, appended 8, total urls = {s.count("<url>")}')
