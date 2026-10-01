# -*- coding: utf-8 -*-
"""register_v8 후속 — en 푸터 이동(영문 컬럼명) + sitemap.html 그리드 + README + PHOTO-ACCURACY."""
import pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from register_v5 import ROOT

# ── sitemap.html 그리드 ──
ALT_FIX = [('sogeumgang', '701m', '1,338m'), ('cheongtaesan', '1,166m', '1,190m'),
           ('heuiyangsan', '607m', '999.1m'), ('bulsan', '497m', '507m')]
NAME_FIX = [('불알산', '불암산'), ('Bulsan', 'Bulamsan')]
for path in (ROOT / 'sitemap.html', ROOT / 'en/sitemap.html'):
    s = path.read_text(encoding='utf-8')
    ko = 'en/' not in str(path.relative_to(ROOT))
    for mid, old, new in ALT_FIX:
        def fix_block(mm):
            return mm.group(0).replace(f'<span class="m-alt">{old}</span>', f'<span class="m-alt">{new}</span>')
        s = re.sub(r'<a href="' + mid + r'-playbook\.html" class="mountain-link-item">.*?</a>', fix_block, s, flags=re.S)
    for o, n in NAME_FIX:
        s = s.replace(f'<span class="m-name">{o}</span>', f'<span class="m-name">{n}</span>')
    to_r = {'cheongtaesan': '강원' if ko else 'Gangwon',
            'heuiyangsan': '경상 / 제주' if ko else 'Gyeongsang/Jeju'}
    for mid in ('cheongtaesan', 'heuiyangsan'):
        m = re.search(r'\s*<a href="' + mid + r'-playbook\.html" class="mountain-link-item">.*?</a>', s, re.S)
        assert m, f'{path.name}: {mid} 미발견'
        item = m.group(0).strip()
        s = s[:m.start()] + s[m.end():]
        to_m = re.search(r'<span class="region-title">' + re.escape(to_r[mid]) + r'</span>', s)
        assert to_m, f'{path.name}: {to_r[mid]} 카드 미발견'
        card_start = s.rfind('<div class="region-card">', 0, to_m.start())
        card_end = s.find('          </div>\n', to_m.end())
        # 카드 내 mountain-link-list의 마지막 </a> 뒤에 삽입
        list_zone_end = s.find('</div>', to_m.end())
        last_a = s.rfind('</a>', to_m.end(), list_zone_end) + len('</a>')
        s = s[:last_a] + '\n' + item + s[last_a:]
    # 배지 재계산
    def fix_badge(mm):
        card = mm.group(0)
        n = len(re.findall(r'mountain-link-item', card))
        return re.sub(r'(<span class="region-badge">)\d+(</span>)', lambda b: b.group(1) + str(n) + b.group(2), card)
    s = re.sub(r'<div class="region-card">.*?</div>\s*</div>\s*</div>', fix_badge, s, flags=re.S)
    path.write_text(s, encoding='utf-8')
    print(f'{path.name}: 그리드 이동·ALT·이름·배지 갱신')

# ── README ──
p = ROOT / 'README.md'
s = p.read_text(encoding='utf-8')
s = s.replace(' · [희양산](./heuiyangsan-playbook.html)', '')
s = s.replace(' · [청태산](./cheongtaesan-playbook.html)', '')
s = s.replace(' · [두타산](./dutasan-playbook.html)', ' · [두타산](./dutasan-playbook.html) · [청태산](./cheongtaesan-playbook.html)')
s = s.replace(' · [신불산](./sinbulsan-playbook.html)', ' · [신불산](./sinbulsan-playbook.html) · [희양산](./heuiyangsan-playbook.html)')
s = s.replace('[불알산](./bulsan-playbook.html)', '[불암산](./bulsan-playbook.html)')
p.write_text(s, encoding='utf-8')
print('README: 정정')

# ── PHOTO-ACCURACY ──
p = ROOT / 'PHOTO-ACCURACY.md'
s = p.read_text(encoding='utf-8')
s = s.replace('| 소금강 | 한국 산악 일반 | 중간 | 설악산 서쪽. 기암괴석과 계곡 |', '| 소금강 | 한국 산악 일반 | 중간 | 오대산 소금강지구(명승 제1호)·노인봉 |')
s = s.replace('| 청태산 | 한국 산악 일반 | 중간 | 백두대간 소백산맥. 활엽수림 능선 |', '| 청태산 | 한국 산악 일반 | 중간 | 횡성·평창 1,190m·자연휴양림 |')
s = s.replace('| 희양산 | 한국 산악 일반 | 중간 | 문경새재 인근. 희양산성 |', '| 희양산 | 한국 산악 일반 | 중간 | 괴산·문경 백두대간 999.1m 암봉 |')
s = s.replace('| 불알산 | 한국 산악 일반 | 중간 | 독바위 전망 |', '| 불암산(구 불알산) | 한국 산악 일반 | 중간 | 정암사·거북바위 바위 능선 |')
p.write_text(s, encoding='utf-8')
print('PHOTO-ACCURACY: 정정')
