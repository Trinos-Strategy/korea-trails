# -*- coding: utf-8 -*-
"""푸터 전면 재생성 (71산 정본, KO/EN 라벨 분리) + sitemap.html 그리드 + README + PHOTO-ACCURACY."""
import pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from register_v5 import ROOT, OTHER_COLS, col_html, replace_footer

# 현재 상태(71산)의 정본 컬럼 — (ko_label, en_label, [(id, ko_name, en_name)])
KR_COLS_V8 = [
    ('강원', 'Gangwon', [
        ('seoraksan', '설악산', 'Seoraksan'), ('chiaksan', '치악산', 'Chiaksan'), ('odaesan', '오대산', 'Odaesan'),
        ('taebaeksan', '태백산', 'Taebaeksan'), ('sogeumgang', '소금강', 'Sogeumgang'), ('gyebangsan', '계방산', 'Gyebangsan'),
        ('dutasan', '두타산', 'Dutasan'), ('daeamsan', '대암산', 'Daeamsan'), ('cheongtaesan', '청태산', 'Cheongtaesan')]),
    ('경기/서울', 'Gyeonggi/Seoul', [
        ('bukhansan', '북한산', 'Bukhansan'), ('dobongsan', '도봉산', 'Dobongsan'), ('myeongseongsan', '명성산', 'Myeongseongsan'),
        ('soyosan', '소요산', 'Soyosan'), ('unaksan', '운악산', 'Unaksan'), ('gwanaksan', '관악산', 'Gwanaksan'),
        ('suraksan', '수락산', 'Suraksan'), ('cheonggyesan', '청계산', 'Cheonggyesan'), ('achasan', '아차산', 'Achasan'),
        ('inwangsan', '인왕산', 'Inwangsan'), ('ansan', '안산', 'Ansan'), ('bulsan', '불암산', 'Bulamsan'),
        ('yongmunsan', '용문산', 'Yongmunsan'), ('yumyeongsan', '유명산', 'Yumyeongsan'), ('gamaksan', '감악산', 'Gamaksan')]),
    ('충청', 'Chungcheong', [
        ('sobaeksan', '소백산', 'Sobaeksan'), ('gyeryongsan', '계룡산', 'Gyeryongsan'), ('minjusan', '민주지산', 'Minjusan'),
        ('sikjangsan', '식장산', 'Sikjangsan'), ('woraksan', '월악산', 'Woraksan'), ('songnisan', '속리산', 'Songnisan')]),
    ('전라', 'Jeolla', [
        ('jirisan', '지리산', 'Jirisan'), ('naejangsan', '내장산', 'Naejangsan'), ('deogyusan', '덕유산', 'Deogyusan'),
        ('wolchulsan', '월출산', 'Wolchulsan'), ('mudeungsan', '무등산', 'Mudeungsan'), ('duryunsan', '두륜산', 'Duryunsan'),
        ('daedunsan', '대둔산', 'Daedunsan'), ('maisan', '마이산', 'Maisan'), ('unjangsan', '운장산', 'Unjangsan'),
        ('yeongchwisan', '영취산', 'Yeongchwisan'), ('baekamsan', '백암산', 'Baegamsan'), ('baegunsan', '백운산', 'Baegunsan')]),
    ('경상 / 제주', 'Gyeongsang/Jeju', [
        ('gayasan', '가야산', 'Gayasan'), ('juwangsan', '주왕산', 'Juwangsan'), ('hallasan', '한라산', 'Hallasan'),
        ('geumjeongsan', '금정산', 'Geumjeongsan'), ('palgongsan', '팔공산', 'Palgongsan'), ('unmunsan', '운문산', 'Unmunsan'),
        ('gajisan', '가지산', 'Gajisan'), ('hwawangsan', '화왕산', 'Hwawangsan'), ('biseulsan', '비슬산', 'Biseulsan'),
        ('cheongnyangsan', '청량산', 'Cheongnyangsan'), ('namsan', '남산(경주)', 'Namsan (Gyeongju)'),
        ('sinbulsan', '신불산', 'Sinbulsan'), ('heuiyangsan', '희양산', 'Heuiyangsan')]),
    ('인천', 'Incheon', [('manisan', '마니산', 'Manisan')]),
]

for path, lang in ((ROOT / 'index.html', 'ko'), (ROOT / 'en/index.html', 'en')):
    s = path.read_text(encoding='utf-8')
    start = s.find('<div class="footer-sitemap"')
    assert start > 0
    end = s.find('<p style="font-size: var(--text-xs); color: var(--muted); line-height: 1.8; text-align: center;', start)
    assert end > start
    cols = [col_html(ko_l if lang == 'ko' else en_l, [(fid, k if lang == 'ko' else e) for fid, k, e in links]) for ko_l, en_l, links in KR_COLS_V8]
    cols += [col_html(ko_c if lang == 'ko' else en_c, [(fid, k if lang == 'ko' else e) for fid, k, e in links]) for ko_c, en_c, links in OTHER_COLS]
    block = ('<div class="footer-sitemap" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); '
             'gap: var(--space-6); text-align: left; margin-bottom: var(--space-8); border-bottom: 1px solid var(--border); '
             'padding-bottom: var(--space-8);">\n' + '\n'.join(cols) + '\n  </div>\n\n  ')
    s = s[:start] + block + s[end:]
    path.write_text(s, encoding='utf-8')
    # 검증
    seg = s[start:s.find('</footer>', start)]
    headers = re.findall(r'<div class="sitemap-col">\s*<div[^>]*>([^<]+)</div>', seg)
    n_links = len(re.findall(r'<a href="', seg))
    print(f'{path.name}: 푸터 재생성 — 컬럼 {headers}')
    assert ('강원' in headers and '경기/서울' in headers) if lang == 'ko' else ('Gangwon' in headers and 'Gyeonggi/Seoul' in headers), '헤더 언어 오류'
    # 4산 위치
    for mid, want in (('cheongtaesan', '강원' if lang == 'ko' else 'Gangwon'),
                      ('heuiyangsan', '경상 / 제주' if lang == 'ko' else 'Gyeongsang/Jeju'),
                      ('bulsan', '경기/서울' if lang == 'ko' else 'Gyeonggi/Seoul'),
                      ('sogeumgang', '강원' if lang == 'ko' else 'Gangwon')):
        found = [h for h, body in re.findall(r'<div class="sitemap-col">\s*<div[^>]*>([^<]+)</div>(.*?)(?=<div class="sitemap-col">|$)', seg, re.S)
                 if f'href="{mid}-playbook.html"' in body]
        assert found == [want], f'{path.name}: {mid} → {found} (기대 {want})'
    print(f'   링크 {n_links}개 · 4산 배치 ✓')
