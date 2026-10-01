# -*- coding: utf-8 -*-
"""정체성 정정 4산 등록 — MOUNTAINS 메타데이터·푸터 지역 이동·sitemap.html 그리드·README·PHOTO-ACCURACY."""
import pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from register_v5 import ROOT

# (id, ko_name, en_name, alt, region_ko, region_en, desc, lat, lng, dist, time)
ROWS = [
    ('sogeumgang', '소금강', 'Sogeumgang', '1,338m(노인봉)', '강원', 'Gangwon',
     '오대산 명승 제1호 계곡. 노인봉 1,338m 능선과 소금강계곡 기암..', 37.40, 128.52, '8.2km', '2-3시간'),
    ('cheongtaesan', '청태산', 'Cheongtaesan', '1,190m', '강원', 'Gangwon',
     '횡성·평창 경계. 국립청태산자연휴양림 6개 등산로와 정상 전망..', 37.44, 128.44, '—', '약 2시간'),
    ('heuiyangsan', '희양산', 'Heuiyangsan', '999.1m', '경상', 'Gyeongsang',
     '괴산·문경 백두대간 화강암 암봉. 지름티재 순환과 백두대간 능선..', 36.65, 127.95, '8.5km', '4시간'),
    ('bulsan', '불암산', 'Bulamsan', '507m', '경기', 'Gyeonggi',
     '노원·의정부 경계. 정암사·거북바위 바위 능선과 수락산 종주..', 37.687, 127.08, '—', '2-3시간'),
]


def patch_mountains(path, lang):
    ko = lang == 'ko'
    s = path.read_text(encoding='utf-8')
    for mid, kn, en, alt, rk, re_, desc, lat, lng, dist, time in ROWS:
        m = re.search(r"\{id:'" + mid + r"',[^}]*\}", s)
        assert m, f'{path}: {mid} 미발견'
        old = m.group(0)
        d_o = re.search(r"dist:'([^']*)'", old).group(1)
        t_o = re.search(r"time:'([^']*)'", old).group(1)
        diff_o = re.search(r"diff:'([^']*)'", old).group(1)
        name = kn if ko else en
        region = rk if ko else re_
        row = ("{id:'%s', name:'%s', alt:'%s', region:'%s', dist:'%s', time:'%s', country:'KR', diff:'%s', done:true, url:'%s-playbook.html', desc:'%s', lat: %s, lng: %s}"
               % (mid, name, alt, region, dist, time, diff_o, mid, desc, lat, lng))
        s = s[:m.start()] + row + s[m.end():]
    path.write_text(s, encoding='utf-8')
    print(f'{path.name}: MOUNTAINS 4산 정정')


patch_mountains(ROOT / 'index.html', 'ko')
patch_mountains(ROOT / 'en/index.html', 'en')

# ── 푸터 지역 이동 (index + en) ──
def footer_move(path, links):
    """links: [(href, ko_label, en_label, from_col, to_col)]"""
    s = path.read_text(encoding='utf-8')
    for href, ko_l, en_l, from_col, to_col in links:
        label = ko_l if 'Wanggwan' not in en_l else en_l
        lab = ko_l if '희양' in ko_l or '청태' in ko_l else en_l
        # 언어별 라벨 결정
        lab = ko_l if 'en/' not in str(path.relative_to(ROOT)) else en_l
        pat = re.compile(r'\n(\s*)<a href="' + href + r'"[^>]*>' + re.escape(lab) + r'</a>')
        m = pat.search(s)
        assert m, f'{path}: {href} 링크 미발견 ({lab})'
        # 제거 후 to_col 카드의 마지막 링크 뒤에 삽입
        s = s[:m.start()] + s[m.end():]
        # to_col 찾기: 컬럼 헤더 텍스트
        to_pat = re.compile(r'(text-transform: uppercase; margin-bottom: var\(--space-3\);">' + re.escape(to_col) + r'</div>\s*<div[^>]*>\s*)(<a )', re.S)
        m2 = to_pat.search(s)
        # 마지막 링크 끝 지점 찾기: to_col 이후 첫 </div>\n    </div> 앞의 마지막 <a ...></a>
        seg_start = m2.start()
        seg_end = s.find('</div>', s.find('</div>', seg_start) + 1)
        insert_pt = s.rfind('</a>', 0, seg_end) + len('</a>')
        indent = '\n        '
        s = s[:insert_pt] + indent + f'<a href="{href}" style="color: var(--muted); text-decoration: none;">{lab}</a>' + s[insert_pt:]
    path.write_text(s, encoding='utf-8')
    print(f'{path.name}: 푸터 이동 완료')


LINKS = [('cheongtaesan-playbook.html', '청태산', 'Cheongtaesan', '충청', '강원'),
         ('heuiyangsan-playbook.html', '희양산', 'Heuiyangsan', '충청', '경상 / 제주')]
footer_move(ROOT / 'index.html', LINKS)
footer_move(ROOT / 'en/index.html', LINKS)

# ── sitemap.html 그리드: 항목 이동 + ALT/이름 갱신 + 배지 재계산 ──
ALT_FIX = [('sogeumgang', '701m', '1,338m'), ('cheongtaesan', '1,166m', '1,190m'),
           ('heuiyangsan', '607m', '999.1m'), ('bulsan', '497m', '507m')]
NAME_FIX = [('불알산', '불암산'), ('Bulsan', 'Bulamsan')]
for path in (ROOT / 'sitemap.html', ROOT / 'en/sitemap.html'):
    s = path.read_text(encoding='utf-8')
    for mid, old, new in ALT_FIX:
        s = s.replace(f'href="{mid}-playbook.html" class="mountain-link-item"', f'href="{mid}-playbook.html" class="mountain-link-item"')
        # m-alt 갱신: 해당 링크 블록 내에서
        def fix_block(mm):
            block = mm.group(0)
            return block.replace(f'<span class="m-alt">{old}</span>', f'<span class="m-alt">{new}</span>')
        s = re.sub(r'<a href="' + mid + r'-playbook\.html" class="mountain-link-item">.*?</a>', fix_block, s, flags=re.S)
    for o, n in NAME_FIX:
        s = s.replace(f'<span class="m-name">{o}</span>', f'<span class="m-name">{n}</span>')
    # 항목 이동: cheongtaesan → 강원 카드, heuiyangsan → 경상 카드
    for mid, from_r, to_r in (('cheongtaesan', '충청' if 'en/' not in str(path.relative_to(ROOT)) else 'Chungcheong',
                               '강원' if 'en/' not in str(path.relative_to(ROOT)) else 'Gangwon'),
                              ('heuiyangsan', '충청' if 'en/' not in str(path.relative_to(ROOT)) else 'Chungcheong',
                               '경상 / 제주' if 'en/' not in str(path.relative_to(ROOT)) else 'Gyeongsang/Jeju')):
        m = re.search(r'\s*<a href="' + mid + r'-playbook\.html" class="mountain-link-item">.*?</a>', s, re.S)
        assert m, f'{path}: {mid} 그리드 미발견'
        item = m.group(0)
        s = s[:m.start()] + s[m.end():]
        # to 카드 찾아 리스트 끝에 삽입
        to_m = re.search(r'<span class="region-title">' + re.escape(to_r) + r'</span>', s)
        assert to_m, f'{path}: {to_r} 카드 미발견'
        list_end = s.find('</div>', to_m.end())
        # mountain-link-list의 마지막 항목 뒤
        last_a = s.rfind('</a>', to_m.end(), list_end) + len('</a>')
        s = s[:last_a] + '\n' + item.strip() + s[last_a:]
    # 배지 재계산
    def fix_badge(mm):
        card = mm.group(0)
        n = len(re.findall(r'mountain-link-item', card))
        return re.sub(r'(<span class="region-badge">)\d+(</span>)', lambda b: b.group(1) + str(n) + b.group(2), card)
    s = re.sub(r'<div class="region-card">.*?</div>\s*</div>', fix_badge, s, flags=re.S)
    path.write_text(s, encoding='utf-8')
    print(f'{path.name}: 그리드 이동·ALT·배지 갱신')

# ── README ──
p = ROOT / 'README.md'
s = p.read_text(encoding='utf-8')
# 충청 행에서 청태산·희양산 제거
s = s.replace(' · [희양산](./heuiyangsan-playbook.html)', '')
s = s.replace(' · [청태산](./cheongtaesan-playbook.html)', '')
# 강원 행에 청태산, 경상 행에 희양산 추가
s = s.replace(' · [두타산](./dutasan-playbook.html)', ' · [두타산](./dutasan-playbook.html) · [청태산](./cheongtaesan-playbook.html)')
s = s.replace(' · [신불산](./sinbulsan-playbook.html)', ' · [신불산](./sinbulsan-playbook.html) · [희양산](./heuiyangsan-playbook.html)')
s = s.replace('[불알산](./bulsan-playbook.html)', '[불암산](./bulsan-playbook.html)')
p.write_text(s, encoding='utf-8')
print('README: 지역 이동·불암산 정정')

# ── PHOTO-ACCURACY 비고 갱신 ──
p = ROOT / 'PHOTO-ACCURACY.md'
s = p.read_text(encoding='utf-8')
s = s.replace('| 소금강 | 한국 산악 일반 | 중간 | 설악산 서쪽. 기암괴석과 계곡 |', '| 소금강 | 한국 산악 일반 | 중간 | 오대산 소금강지구(명승 제1호)·노인봉 |')
s = s.replace('| 청태산 | 한국 산악 일반 | 중간 | 백두대간 소백산맥. 활엽수림 능선 |', '| 청태산 | 한국 산악 일반 | 중간 | 횡성·평창 1,190m·자연휴양림 |')
s = s.replace('| 희양산 | 한국 산악 일반 | 중간 | 문경새재 인근. 희양산성 |', '| 희양산 | 한국 산악 일반 | 중간 | 괴산·문경 백두대간 999.1m 암봉 |')
s = s.replace('| 불알산 | 한국 산악 일반 | 중간 | 독바위 전망 |', '| 불암산(구 불알산) | 한국 산악 일반 | 중간 | 정암사·거북바위 바위 능선 |')
p.write_text(s, encoding='utf-8')
print('PHOTO-ACCURACY: 비고 갱신')
