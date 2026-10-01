# -*- coding: utf-8 -*-
"""6차 전수 검증 — 파싱·스크립트 문법·대칭·필터·에셋·링크·사이트맵."""
import json, pathlib, re, subprocess, sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
NEW = ('daeamsan', 'baegunsan', 'sinbulsan', 'gamaksan')
issues = []


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = 0

    def error(self, message):
        self.errors += 1
        issues.append(f'parse: {message}')


# 1) HTML 전수 파싱 (root + en)
pages = sorted(ROOT.glob('*.html')) + sorted((ROOT / 'en').glob('*.html'))
for pg in pages:
    parser = Parser()
    parser.feed(pg.read_text(encoding='utf-8'))
    parser.close()
print(f'1) HTML 파싱: {len(pages)}파일 — 오류 {len(issues)}건')

# 2) 인라인 스크립트 node --check (전 페이지)
import tempfile, os
bad = 0
with tempfile.TemporaryDirectory() as td:
    for pg in pages:
        s = pg.read_text(encoding='utf-8')
        for i, sc in enumerate(re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', s, re.S)):
            f = pathlib.Path(td) / 'chk.js'
            f.write_text(sc, encoding='utf-8')
            r = subprocess.run(['node', '--check', str(f)], capture_output=True, text=True)
            if r.returncode != 0:
                bad += 1
                issues.append(f'JS {pg.name} #{i}: {r.stderr.strip().splitlines()[0][:90]}')
print(f'2) 인라인 스크립트 node --check: 실패 {bad}건')

# 3) KR/EN MOUNTAINS 대칭 + 필터 시뮬레이션
def load_mountains(page):
    s = (ROOT / page).read_text(encoding='utf-8')
    m = re.search(r'window\.MOUNTAINS = \[(.*?)\n\];', s, re.S)
    assert m, f'{page}: MOUNTAINS 미발견'
    body = m.group(1)
    out = []
    for entry in re.finditer(r"\{id:'([^']+)'[^}]*\}", body):
        t = entry.group(0)
        def field(k):
            mm = re.search(k + r":'([^']*)'", t)
            return mm.group(1) if mm else None
        out.append(dict(id=field('id'), name=field('name'), region=field('region'), country=field('country'), url=field('url'), diff=field('diff')))
    return out

ko = load_mountains('index.html')
en = load_mountains('en/index.html')
print(f'3) MOUNTAINS: KO {len(ko)} / EN {len(en)} — 대칭 {len(ko) == len(en)}, id 집합 동일 {set(x["id"] for x in ko) == set(x["id"] for x in en)}')
if len(ko) != len(en):
    issues.append(f'MOUNTAINS 비대칭 KO {len(ko)} vs EN {len(en)}')
if set(x['id'] for x in ko) != set(x['id'] for x in en):
    issues.append('MOUNTAINS id 집합 불일치')

from collections import Counter
ck = Counter(x['country'] for x in ko)
print('   국가 분포(KO):', dict(sorted(ck.items())), '합계', sum(ck.values()))
print('   신규 4산 등재:', [x['id'] for x in ko if x['id'] in NEW])
rk = Counter(x['region'] for x in ko if x['country'] == 'KR')
print('   KR 지역 분포:', dict(rk))
# 지역 옵션 커버 확인
sel = (ROOT / 'index.html').read_text(encoding='utf-8')
for region in rk:
    if f'<option value="{region}">' not in sel:
        issues.append(f'지역 옵션 누락(KO): {region}')
sel_en = (ROOT / 'en/index.html').read_text(encoding='utf-8')
for x in en:
    if x['country'] == 'KR' and f'<option value="{x["region"]}">' not in sel_en:
        issues.append(f'지역 옵션 누락(EN): {x["region"]}')

# 4) MOUNTAINS url → 파일 존재
missing = [x['url'] for x in ko if not (ROOT / x['url']).exists()]
missing += [f"en/{x['url']}" for x in en if not (ROOT / 'en' / x['url']).exists()]
print(f'4) 플레이북 파일 존재: 누락 {len(missing)}')
issues += [f'파일 누락: {u}' for u in missing]

# 5) 신규 4산 에셋 28파일 확인
for mid in NEW:
    d = ROOT / 'assets/img' / mid
    need = [f'hero-{w}.{e}' for w in (640, 1024, 1600, 2400) for e in ('jpg', 'webp', 'avif')]
    need += [f'g{i}.{e}' for i in range(1, 5) for e in ('jpg', 'webp', 'avif')]
    need += [f'g1-640.{e}' for e in ('jpg', 'webp', 'avif')] + ['og.png']
    lack = [f for f in need if not (d / f).exists()]
    print(f'5) {mid}: {len(need) - len(lack)}/{len(need)} 에셋' + (f' — 누락 {lack}' if lack else ''))
    issues += [f'{mid} 에셋 누락: {lack}'] if lack else []

# 6) 페이지 무결성: title/hreflang/og/심화밴드/코스수
for mid in NEW:
    for pre, mid_page in ((ROOT / f'{mid}-playbook.html', mid), (ROOT / 'en' / f'{mid}-playbook.html', mid)):
        s = pre.read_text(encoding='utf-8')
        checks = {
            'title': f'<title>' in s,
            'hreflang ko': 'hreflang="ko"' in s,
            'hreflang en': 'hreflang="en"' in s,
            'deep-info mount': f'data-mountain="{mid}"' in s,
            'deep-info script': 'deep-info' in s,
            'no double assets': '../../assets' not in s,
            'og.png': f'{mid}/og.png' in s,
            '3 panels': s.count('class="panel ') == 3,
        }
        fails = [k for k, v in checks.items() if not v]
        if fails:
            issues.append(f'{pre.name}: {fails}')
        print(f'6) {pre.name}: ' + ('OK' if not fails else f'실패 {fails}'))

# 7) 푸터 링크 존재 확인 (root/en)
for base, page in ((ROOT, 'index.html'), (ROOT / 'en', 'index.html')):
    s = (base / page).read_text(encoding='utf-8')
    st = s.find('footer-sitemap')
    seg = s[st:s.find('<p style=', st)]
    links = re.findall(r'<a href="([^"]+)"', seg)
    lack = [h for h in links if not (base / h).exists()]
    print(f'7) {page} 푸터 링크 {len(links)}개 — 누락 {len(lack)}')
    issues += [f'{page} 푸터 누락: {lack}'] if lack else []
    # 한국 링크 수 = 53 (테마별 2 제외)
    kr_links = [h for h in links if h.endswith('-playbook.html') and 'en/' not in h]
    print(f'   플레이북 링크 {len(kr_links)}개')

# 8) 사이트맵 XML 검증
import xml.etree.ElementTree as ET
sp = ROOT / 'sitemap.xml'
try:
    tree = ET.parse(sp)
    ns = {'x': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'xh': 'http://www.w3.org/1999/xhtml'}
    urls = tree.getroot().findall('x:url', {'x': 'http://www.sitemaps.org/schemas/sitemap/0.9'})
    locs = [u.find('x:loc', ns).text for u in urls]
    print(f'8) sitemap XML 파싱 OK — {len(urls)} URL')
    bad_ko = 0
    for u in urls:
        loc = u.find('x:loc', ns).text
        stem = loc.split('.group/')[1]
        exp_ko = 'https://mttrails.trinos.group/' + (stem.split('en/', 1)[1] if stem.startswith('en/') else stem)
        ko_h = u.find('xh:link[@hreflang="ko"]', ns)
        xd_h = u.find('xh:link[@hreflang="x-default"]', ns)
        if ko_h is None or ko_h.get('href') != exp_ko or xd_h is None or xd_h.get('href') != exp_ko:
            bad_ko += 1
    print(f'   hreflang ko 불일치 잔존: {bad_ko}')
    if bad_ko:
        issues.append(f'sitemap hreflang 잔존 불일치 {bad_ko}')
    # sitemap loc ↔ 파일 존재
    noloc = [l for l in locs if not (ROOT / l.split('.group/')[1]).exists()]
    if noloc:
        issues.append(f'sitemap 파일 없음: {noloc[:5]}')
    # 신규 8블록 포함 확인
    for mid in NEW:
        for stem in (f'{mid}-playbook.html', f'en/{mid}-playbook.html'):
            if f'https://mttrails.trinos.group/{stem}' not in locs:
                issues.append(f'sitemap 누락: {stem}')
except ET.ParseError as e:
    issues.append(f'sitemap XML 파싱 실패: {e}')

# 9) deep-info 데이터 문법
for f in ('assets/js/deep-info-data.js', 'assets/js/deep-info-data-en.js'):
    r = subprocess.run(['node', '--check', str(ROOT / f)], capture_output=True, text=True)
    ok = r.returncode == 0
    print(f'9) {f}: node --check {"OK" if ok else "FAIL"}')
    if not ok:
        issues.append(f'{f}: {r.stderr[:120]}')
# 신규 키 존재 + KO/EN 대칭
s1 = (ROOT / 'assets/js/deep-info-data.js').read_text(encoding='utf-8')
s2 = (ROOT / 'assets/js/deep-info-data-en.js').read_text(encoding='utf-8')
for mid in NEW:
    if f"DEEP_INFO['{mid}']" not in s1:
        issues.append(f'deep-info KO 누락: {mid}')
    if f"DEEP_INFO_EN['{mid}']" not in s2:
        issues.append(f'deep-info EN 누락: {mid}')

# 10) 사이트 카운트 일관성
idx = (ROOT / 'index.html').read_text(encoding='utf-8')
en_idx = (ROOT / 'en/index.html').read_text(encoding='utf-8')
for label, txt in (('KO', idx), ('EN', en_idx)):
    checks = [('전체 72산' if label == 'KO' else 'All 72 Peaks') in txt,
              ('한국 57산' if label == 'KO' else 'South Korea · 57') in txt,
              ('네팔 4산' if label == 'KO' else 'Nepal · 4') in txt,
              ('<div class="hero-stat-value">72</div>' in txt),
              ('(72)' in txt)]
    print(f'10) {label} 카운트: ' + ('OK' if all(checks) else f'실패 {checks}'))
    if not all(checks):
        issues.append(f'{label} 카운트 표기 실패')

print()
print('=== 결과 ===')
print(f'이슈 {len(issues)}건')
for i in issues:
    print(' -', i)
