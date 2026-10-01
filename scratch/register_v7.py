# -*- coding: utf-8 -*-
"""품질 업그레이드 등록 — 왕관산 제거(72→71) + 정체성 정정 메타데이터 + 푸터/그리드 재생성."""
import pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from register_v5 import ROOT, col_html, replace_footer

# ── MOUNTAINS 정정 (KO) ──
FIX_KO = [
    ("{id:'yeongchwisan', name:'영취산', alt:'1,090m', region:'전라', dist:'8km', time:'4-5시간', country:'KR', diff:'medium', done:true_PLACEHOLDER", None),
]
sub = [
    # (산id, 새 alt, 새 desc, lat, lng) — 행 전체를 재구성
    ("yeongchwisan", '영취산', '510m', '전라', "여수의 진달래 명산. 진례봉 510m 능선 군락과 4월 진달래 축제..", 34.770, 127.660),
    ("cheongnyangsan", '청량산', '869.7m', '경상', "봉화·안동의 기암 명산. 의상봉 869.7m와 청량사·하늘다리..", 36.880, 128.860),
    ("baekamsan", '백암산', '741.2m', '전라', "장성·순창 경계. 상왕봉 741.2m와 백양사·구암사 능선..", 35.600, 126.880),
    ("ansan", '안산', '296m', '경기', "서울 서대문의 낮은 산. 봉수대(기념물)와 무장애 안산자락길 7km..", 37.574, 126.952),
    ("yumyeongsan", '유명산', '862m', '경기', "가평 설악면의 산. 국립자연휴양림 들머리와 계곡코스, 용문산 종주..", 37.820, 127.530),
    ("hwawangsan", '화왕산', '928m', '경상', "창녕의 진달래 명산. 3대 군락지와 화왕산성·허준 세트장..", 35.550, 128.490),
    ("unjangsan", '운장산', '1,126m', '전라', "진안·완주의 명산. 운장대 1,126m와 칠성대·삼장봉 능선..", 35.660, 127.340),
    ("yongmunsan", '용문산', '1,157m', '경기', "양평의 진산. 용문사·사미기봉·마당바위를 지나 가섭봉 1,157m..", 37.4833, 127.2833),
    ("inwangsan", '인왕산', '338m', '경기', "서울 도심의 성곽 산. 한양도성 인왕구간과 서울 전경 조망..", 37.5839, 126.9659),
    ("gajisan", '가지산', '1,240m', '경상', "영남알프스 최고봉. 석남터널 최단 코스와 통도사 내원계곡..", 35.3686, 129.0758),
    ("biseulsan", '비슬산', '1,084m', '경상', "대구 달성·청도의 천왕봉. 유가사 들머리와 악견 능선·억새밭..", 35.7167, 128.5000),
]
EN_NAME = {'yeongchwisan': 'Yeongchwisan', 'cheongnyangsan': 'Cheongnyangsan', 'baekamsan': 'Baegamsan',
           'ansan': 'Ansan', 'yumyeongsan': 'Yumyeongsan', 'hwawangsan': 'Hwawangsan', 'unjangsan': 'Unjangsan',
           'yongmunsan': 'Yongmunsan', 'inwangsan': 'Inwangsan', 'gajisan': 'Gajisan', 'biseulsan': 'Biseulsan'}
EN_REGION = {'전라': 'Jeolla', '경상': 'Gyeongsang', '경기': 'Gyeonggi', '강원': 'Gangwon', '충청': 'Chungcheong', '인천': 'Incheon'}


def patch_mountains(path, lang):
    s = path.read_text(encoding='utf-8')
    ko = lang == 'ko'
    # 왕관산 행 제거
    m = re.search(r"\s*\{id:'wanggwan',[^}]*\},?", s)
    if m:
        s = s[:m.start()] + s[m.end():]
    # 정정 행 교체 (id 기준)
    for mid, name, alt, region, desc, lat, lng in sub:
        pat = re.compile(r"\{id:'" + mid + r"',[^}]*\}")
        mm = pat.search(s)
        assert mm, f'{path}: {mid} 미발겵'
        nm = name if ko else EN_NAME[mid]
        rg = region if ko else EN_REGION[region]
        ds = desc if ko else desc  # EN도 동일 desc(기존 관례 유지)
        row = ("{id:'%s', name:'%s', alt:'%s', region:'%s', dist:'6km', time:'3-4시간', country:'KR', diff:'medium', done:true, url:'%s-playbook.html', desc:'%s', lat: %s, lng: %s}"
               % (mid, nm, alt, rg, mid, ds, lat, lng))
        # dist/time 원문 유지를 위해 기존 값 추출
        d_old = re.search(r"dist:'([^']*)'", mm.group(0)).group(1)
        t_old = re.search(r"time:'([^']*)'", mm.group(0)).group(1)
        diff_old = re.search(r"diff:'([^']*)'", mm.group(0)).group(1)
        row = row.replace("dist:'6km'", f"dist:'{d_old}'").replace("time:'3-4시간'", f"time:'{t_old}'").replace("diff:'medium'", f"diff:'{diff_old}'")
        s = s[:mm.start()] + row + s[mm.end():]
    path.write_text(s, encoding='utf-8')
    print(f'{path.name}: MOUNTAINS 정정 ({len(sub)}산) + 왕관산 제거')


patch_mountains(ROOT / 'index.html', 'ko')
patch_mountains(ROOT / 'en/index.html', 'en')


def sub_n(s, old, new, n, label):
    cnt = s.count(old)
    if cnt == 0:
        return s  # 이미 적용됨(멱등)
    assert cnt == n, f'{label}: 기대 {n} 실제 {cnt}'
    return s.replace(old, new)


for path, ko in ((ROOT / 'index.html', True), (ROOT / 'en/index.html', False)):
    s = path.read_text(encoding='utf-8')
    if ko:
        s = sub_n(s, '>전체 72산<', '>전체 71산<', 1, '칩 전체')
        s = sub_n(s, '>한국 57산<', '>한국 56산<', 1, '칩 한국')
        s = sub_n(s, '>완성됨 (72)<', '>완성됨 (71)<', 1, '필터')
    else:
        s = sub_n(s, '>All 72 Peaks<', '>All 71 Peaks<', 1, 'chip all')
        s = sub_n(s, '>South Korea · 57<', '>South Korea · 56<', 1, 'chip KR')
        s = sub_n(s, '>Completed (72)<', '>Completed (71)<', 1, 'filter')
    s = sub_n(s, '<div class="hero-stat-value">72</div>', '<div class="hero-stat-value">71</div>', 2, '스탯')
    # 로테이션 왕관산 제거
    s = re.sub(r"\s*\{ base: '[^']*wanggwan'[^}]*\},", '', s, count=1)
    path.write_text(s, encoding='utf-8')
    print(f'{path.name}: 카운트 71·로테이션 정리')

# ── sitemap.xml 왕관산 2블록 제거 ──
sp = ROOT / 'sitemap.xml'
s = sp.read_text(encoding='utf-8')
n = len(re.findall(r'wanggwan', s))
for _ in range(2):
    m = re.search(r'\s*<url>\s*<loc>[^<]*wanggwan[^<]*</loc>.*?</url>', s, re.S)
    s = s[:m.start()] + s[m.end():]
sp.write_text(s, encoding='utf-8')
print(f'sitemap: wanggwan {n}곳 → 제거, 총 {s.count("<url>")} URL')

# ── 푸터/sitemap.html 그리드: 왕관산 제거 재생성 ──
import register_v5 as r5
COLS = [c for c in r5.KR_COLS]
# KR_COLS는 v5 원본(68산 체계)이므로 v6 등록 상태(72)에서 왕관산만 뺀 목록이 필요 → 현재 index.html 푸터는 v6 재생성 상태
# 안전하게: 현재 페이지의 푸터에서 왕관산 링크만 제거
for path, base in ((ROOT / 'index.html', ROOT), (ROOT / 'en/index.html', ROOT / 'en'),
                   (ROOT / 'sitemap.html', ROOT), (ROOT / 'en/sitemap.html', ROOT / 'en')):
    s = path.read_text(encoding='utf-8')
    for nm in ('왕관산', 'Wanggwan', 'Wanggwan'):
        s = re.sub(r'\s*<a href="wanggwan-playbook\.html"[^>]*>' + nm + r'</a>', '', s)
    # sitemap.html 카드 배지 수 감소 (경기 16→15)
    s = s.replace('<span class="region-badge">16</span>', '<span class="region-badge">15</span>')
    path.write_text(s, encoding='utf-8')
    print(f'{path.name}: 왕관산 링크 제거')

# README 행 정리
p = ROOT / 'README.md'
s = p.read_text(encoding='utf-8')
s = s.replace(' · [왕관산](./wanggwan-playbook.html)', '')
s = s.replace('## 📂 플레이북 현황 (72산)', '## 📂 플레이북 현황 (71산)')
s = s.replace('**등산 플레이북 72종**', '**등산 플레이북 71종**')
p.write_text(s, encoding='utf-8')
print('README: 왕관산 제거·71산')

# 파일 삭제
import shutil
for f in [ROOT / 'wanggwan-playbook.html', ROOT / 'en/wanggwan-playbook.html']:
    f.unlink(missing_ok=True)
shutil.rmtree(ROOT / 'assets/img/wanggwan', ignore_errors=True)
print('왕관산 페이지·에셋 삭제')

# ── deep-info: 왕관산 제거 + v3 6산 중복 제거 + 11산 신규 4블록은 별도 파일에서 ──
for f in ('assets/js/deep-info-data.js', 'assets/js/deep-info-data-en.js'):
    p = ROOT / f
    s = p.read_text(encoding='utf-8')
    pre = "DEEP_INFO['" if 'data.js' in f and '-en' not in f else "DEEP_INFO_EN['"
    # 왕관산
    s = re.sub(r"\nwindow\." + pre + r"wanggwan'\] = \{.*?\};", '', s, flags=re.S)
    # v3 6산 중복: 두 번째 등장 제거
    for mid in ('ansan', 'bulsan', 'sogeumgang', 'heuiyangsan', 'cheongtaesan', 'baekamsan'):
        pat = re.compile(r"window\." + pre + mid + r"'\] = \{.*?\};", re.S)
        matches = list(pat.finditer(s))
        if len(matches) > 1:
            second = matches[1]
            s = s[:second.start()] + s[second.end():]
    p.write_text(s, encoding='utf-8')
    print(f'{f}: 왕관산 제거 + 중복 정리')
