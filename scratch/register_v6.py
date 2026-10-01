# -*- coding: utf-8 -*-
"""한국 100대 명산 6차(4산) 등록 — index(KO/EN)·sitemap.xml·sitemap.html 그리드."""
import pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from register_v5 import ROOT, KR_COLS, OTHER_COLS, col_html, replace_footer

M6_KO = """  {id:'daeamsan', name:'대암산', alt:'1,304m', region:'강원', dist:'7km', time:'4-5시간', country:'KR', diff:'medium', done:true, url:'daeamsan-playbook.html', desc:'양구·인제의 바위산. 용늪 천연기념물(제246호) 예약 탐방과 백두대간 조망..', lat: 38.098, lng: 127.998},
  {id:'baegunsan', name:'백운산', alt:'1,222m', region:'전라', dist:'7km', time:'4-5시간', country:'KR', diff:'medium', done:true, url:'baegunsan-playbook.html', desc:'광양의 철쭉 명산. 철쭉제 능선과 섬진강 조망..', lat: 35.265, lng: 127.621},
  {id:'sinbulsan', name:'신불산', alt:'1,159m', region:'경상', dist:'11km', time:'5시간', country:'KR', diff:'medium', done:true, url:'sinbulsan-playbook.html', desc:'영남알프스 주봉. 간월재 억새평원과 배내골 능선..', lat: 35.541, lng: 129.061},
  {id:'gamaksan', name:'감악산', alt:'674.9m', region:'경기', dist:'7km', time:'4-5시간', country:'KR', diff:'medium', done:true, url:'gamaksan-playbook.html', desc:'파주의 진산. 감악사·장흥계곡·출렁다리와 한북정맥 능선..', lat: 37.859, lng: 126.926},
"""
M6_EN = """  {id:'daeamsan', name:'Daeamsan', alt:'1,304m', region:'Gangwon', dist:'7km', time:'4-5시간', country:'KR', diff:'medium', done:true, url:'daeamsan-playbook.html', desc:'양구·인제의 바위산. 용늪 천연기념물(제246호) 예약 탐방과 백두대간 조망..', lat: 38.098, lng: 127.998},
  {id:'baegunsan', name:'Baegunsan (Gwangyang)', alt:'1,222m', region:'Jeolla', dist:'7km', time:'4-5시간', country:'KR', diff:'medium', done:true, url:'baegunsan-playbook.html', desc:'광양의 철쭉 명산. 철쭉제 능선과 섬진강 조망..', lat: 35.265, lng: 127.621},
  {id:'sinbulsan', name:'Sinbulsan', alt:'1,159m', region:'Gyeongsang', dist:'11km', time:'5시간', country:'KR', diff:'medium', done:true, url:'sinbulsan-playbook.html', desc:'영남알프스 주봉. 간월재 억새평원과 배내골 능선..', lat: 35.541, lng: 129.061},
  {id:'gamaksan', name:'Gamaksan', alt:'674.9m', region:'Gyeonggi', dist:'7km', time:'4-5시간', country:'KR', diff:'medium', done:true, url:'gamaksan-playbook.html', desc:'파주의 진산. 감악사·장흥계곡·출렁다리와 한북정맥 능선..', lat: 37.859, lng: 126.926},
"""
ROT6_KO = """    { base: 'assets/img/daeamsan', video: null, alt: '한국 대암산의 안개 낀 바위 능선' },
    { base: 'assets/img/baegunsan', video: null, alt: '한국 백운산의 철쭉 능선' },
    { base: 'assets/img/sinbulsan', video: null, alt: '한국 신불산의 억새평원 능선' },
    { base: 'assets/img/gamaksan', video: null, alt: '한국 감악산의 사찰과 계곡' },
"""
ROT6_EN = """    { base: '../assets/img/daeamsan', video: null, alt: 'Misty rock ridges of Daeamsan' },
    { base: '../assets/img/baegunsan', video: null, alt: 'Azalea ridges of Baegunsan, Gwangyang' },
    { base: '../assets/img/sinbulsan', video: null, alt: 'Silver-grass plateau of Sinbulsan' },
    { base: '../assets/img/gamaksan', video: null, alt: 'Temple and valley of Gamaksan' },
"""

KR_COLS_V6 = []
for ko_r, en_r, region, links in KR_COLS:
    links = list(links)
    if ko_r == '강원':
        links.append(('daeamsan', '대암산', 'Daeamsan'))
    elif ko_r == '전라':
        links.append(('baegunsan', '백운산', 'Baegunsan'))
    elif ko_r.startswith('경상'):
        links.append(('sinbulsan', '신불산', 'Sinbulsan'))
    elif ko_r == '경기/서울':
        links.append(('gamaksan', '감악산', 'Gamaksan'))
    KR_COLS_V6.append((ko_r, en_r, region, links))


def sub_n(s, old, new, n, label):
    cnt = s.count(old)
    assert cnt == n, f'{label}: 기대 {n} 실제 {cnt} — "{old[:40]}"'
    return s.replace(old, new)


def patch_index(path, lang):
    ko = lang == 'ko'
    s = path.read_text(encoding='utf-8')
    anchor = "{id:'manisan', name:'마니산'" if ko else "{id:'manisan', name:'Manisan'"
    i = s.find(anchor)
    assert i >= 0, f'{path}: manisan 앵커 미발견'
    line_end = s.find('\n', i) + 1
    s = s[:line_end] + (M6_KO if ko else M6_EN) + s[line_end:]

    if ko:
        s = sub_n(s, '>전체 68산<', '>전체 72산<', 1, '칩 전체')
        s = sub_n(s, '>한국 53산<', '>한국 57산<', 1, '칩 한국')
        s = sub_n(s, '>완성됨 (68)<', '>완성됨 (72)<', 1, '완성 필터')
    else:
        s = sub_n(s, '>All 68 Peaks<', '>All 72 Peaks<', 1, 'chip all')
        s = sub_n(s, '>South Korea · 53<', '>South Korea · 57<', 1, 'chip KR')
        s = sub_n(s, '>Completed (68)<', '>Completed (72)<', 1, 'done filter')
    s = sub_n(s, '<div class="hero-stat-value">68</div>', '<div class="hero-stat-value">72</div>', 2, '스탯')

    rot_anchor = ("{ base: 'assets/img/manisan', video: null, alt: '한국 강화 마니산의 능선과 서해 전망' },\n" if ko else
                  "{ base: '../assets/img/manisan', video: null, alt: 'Ridge of Manisan, Ganghwa Island' },\n")
    assert s.count(rot_anchor) == 1, f'rotation anchor {path.name}: {s.count(rot_anchor)}'
    s = s.replace(rot_anchor, rot_anchor + (ROT6_KO if ko else ROT6_EN))

    # 푸터 재생성 (v6 컬럼)
    global KR_COLS
    KR_COLS_save = KR_COLS
    import register_v5
    register_v5.KR_COLS = KR_COLS_V6
    s = replace_footer(s, lang)
    register_v5.KR_COLS = KR_COLS_save
    path.write_text(s, encoding='utf-8')
    print(f'{path.name}: patched')


patch_index(ROOT / 'index.html', 'ko')
patch_index(ROOT / 'en/index.html', 'en')

# ── sitemap.xml +8블록 ──
BASE = 'https://mttrails.trinos.group/'
sp = ROOT / 'sitemap.xml'
s = sp.read_text(encoding='utf-8')
blocks = []
for mid in ('daeamsan', 'baegunsan', 'sinbulsan', 'gamaksan'):
    ko_stem, en_stem = f'{mid}-playbook.html', f'en/{mid}-playbook.html'
    blocks.append(f'''  <url>
    <loc>{BASE}{ko_stem}</loc>
    <xhtml:link rel="alternate" hreflang="ko" href="{BASE}{ko_stem}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE}{en_stem}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{ko_stem}"/>
    <lastmod>2026-09-19</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
''')
    blocks.append(f'''  <url>
    <loc>{BASE}{en_stem}</loc>
    <xhtml:link rel="alternate" hreflang="ko" href="{BASE}{ko_stem}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE}{en_stem}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{ko_stem}"/>
    <lastmod>2026-09-19</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
''')
s = s.replace('</urlset>', ''.join(blocks) + '</urlset>')
sp.write_text(s, encoding='utf-8')
print(f'sitemap: +8 → {s.count("<url>")} URL')

# ── sitemap.html 그리드 재생성 (v6) ──
import register_v5_sitemap_page as spg
spg.KR_COLS = KR_COLS_V6
ALT = dict(spg.ALT)
ALT.update(daeamsan='1,304m', baegunsan='1,222m', sinbulsan='1,159m', gamaksan='674.9m')
spg.ALT = ALT
for lang, page in (('ko', 'sitemap.html'), ('en', 'en/sitemap.html')):
    p = ROOT / page
    s = p.read_text(encoding='utf-8')
    start = s.find('        <div class="sitemap-grid-main">')
    assert start > 0
    end_marker = '\n        </div>'
    end = s.find(end_marker, start) + len(end_marker)
    s = s[:start] + spg.grid(lang) + s[end:]
    import register_v5 as r5
    r5_sitemap = r5.replace_footer
    kr_save = r5.KR_COLS
    r5.KR_COLS = KR_COLS_V6
    s = r5_sitemap(s, lang)
    r5.KR_COLS = kr_save
    p.write_text(s, encoding='utf-8')
    print(f'{page}: grid 갱신, 링크 {s.count("mountain-link-item")}개')
