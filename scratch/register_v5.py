# -*- coding: utf-8 -*-
"""한국 100대 명산 5차(4산) 등록 스크립트.

신규: namsan(남산·경주), gyebangsan(계방산), dutasan(두타산), manisan(마니산)
정리(기존 결함):
  - 푸터: 2~4차 16산 링크 누락 보완 + 금정산·팔공산·운문산 강원→경상 이동 + 대만~말레이시아 컬럼의 깨진 닫는 태그 정리
  - MOUNTAINS: 소금강 region 경기→강원 (지리 정정)
  - 칩/스탯: 전체 64→68, 한국 49→53, 네팔 1→4, 완성됨(26)→(68)
  - 지역 필터: 인천(신규) 옵션
  - 히어로 로테이션: 신규 4산 추가
모든 치환은 사전 카운트 assert → 조용한 누락 방지.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

M5_KO = """  {id:'namsan', name:'남산(경주)', alt:'468m', region:'경상', dist:'5.6km', time:'3-4시간', country:'KR', diff:'easy', done:true, url:'namsan-playbook.html', desc:'유네스코 남산 불국토. 금오봉 468m와 사지·석불 유적의 산..', lat: 35.8292, lng: 129.221},
  {id:'gyebangsan', name:'계방산', alt:'1,577m', region:'강원', dist:'8km', time:'4-5시간', country:'KR', diff:'medium', done:true, url:'gyebangsan-playbook.html', desc:'오대산국립공원 최고봉 1,577m. 초원 능선과 겨울 설경..', lat: 37.533, lng: 128.372},
  {id:'dutasan', name:'두타산', alt:'1,357m', region:'강원', dist:'8km', time:'5시간', country:'KR', diff:'medium', done:true, url:'dutasan-playbook.html', desc:'동해·삼척 경계 1,357m. 베틀바위·마천루 암릉과 무릉계..', lat: 37.191, lng: 129.042},
  {id:'manisan', name:'마니산', alt:'469m', region:'인천', dist:'5km', time:'3시간', country:'KR', diff:'easy', done:true, url:'manisan-playbook.html', desc:'강화도 최고봉. 참성단 단군제천 전설과 삼랑성..', lat: 37.597, lng: 126.475},
"""
M5_EN = """  {id:'namsan', name:'Namsan (Gyeongju)', alt:'468m', region:'Gyeongsang', dist:'5.6km', time:'3-4시간', country:'KR', diff:'easy', done:true, url:'namsan-playbook.html', desc:'유네스코 남산 불국토. 금오봉 468m와 사지·석불 유적의 산..', lat: 35.8292, lng: 129.221},
  {id:'gyebangsan', name:'Gyebangsan', alt:'1,577m', region:'Gangwon', dist:'8km', time:'4-5시간', country:'KR', diff:'medium', done:true, url:'gyebangsan-playbook.html', desc:'오대산국립공원 최고봉 1,577m. 초원 능선과 겨울 설경..', lat: 37.533, lng: 128.372},
  {id:'dutasan', name:'Dutasan', alt:'1,357m', region:'Gangwon', dist:'8km', time:'5시간', country:'KR', diff:'medium', done:true, url:'dutasan-playbook.html', desc:'동해·삼척 경계 1,357m. 베틀바위·마천루 암릉과 무릉계..', lat: 37.191, lng: 129.042},
  {id:'manisan', name:'Manisan', alt:'469m', region:'Incheon', dist:'5km', time:'3시간', country:'KR', diff:'easy', done:true, url:'manisan-playbook.html', desc:'강화도 최고봉. 참성단 단군제천 전설과 삼랑성..', lat: 37.597, lng: 126.475},
"""

ROT5_KO = """    { base: 'assets/img/namsan', video: null, alt: '한국 경주 남산의 사찰 탑과 안개 낀 능선' },
    { base: 'assets/img/gyebangsan', video: null, alt: '한국 계방산의 초원 정상 능선과 산맥 전망' },
    { base: 'assets/img/dutasan', video: null, alt: '한국 두타산의 암릉 능선' },
    { base: 'assets/img/manisan', video: null, alt: '한국 강화 마니산의 능선과 서해 전망' },
"""
ROT5_EN = """    { base: '../assets/img/namsan', video: null, alt: 'Temple pagoda and misty ridges of Namsan, Gyeongju' },
    { base: '../assets/img/gyebangsan', video: null, alt: 'Grassy summit ridge and ranges of Gyebangsan' },
    { base: '../assets/img/dutasan', video: null, alt: 'Rocky ridge of Dutasan, Gangwon' },
    { base: '../assets/img/manisan', video: null, alt: 'Ridge of Manisan, Ganghwa Island' },
"""

# (id, ko명, en명)
KR_COLS = [
    ('강원', 'Gangwon', 'Gangwon', [('seoraksan', '설악산', 'Seoraksan'), ('chiaksan', '치악산', 'Chiaksan'), ('odaesan', '오대산', 'Odaesan'), ('taebaeksan', '태백산', 'Taebaeksan'), ('sogeumgang', '소금강', 'Sogeumgang'), ('gyebangsan', '계방산', 'Gyebangsan'), ('dutasan', '두타산', 'Dutasan')]),
    ('경기/서울', '경기/서울', 'Gyeonggi/Seoul', [('bukhansan', '북한산', 'Bukhansan'), ('dobongsan', '도봉산', 'Dobongsan'), ('myeongseongsan', '명성산', 'Myeongseongsan'), ('soyosan', '소요산', 'Soyosan'), ('unaksan', '운악산', 'Unaksan'), ('gwanaksan', '관악산', 'Gwanaksan'), ('suraksan', '수락산', 'Suraksan'), ('cheonggyesan', '청계산', 'Cheonggyesan'), ('achasan', '아차산', 'Achasan'), ('inwangsan', '인왕산', 'Inwangsan'), ('ansan', '안산', 'Ansan'), ('bulsan', '불알산', 'Bulsan'), ('yongmunsan', '용문산', 'Yongmunsan'), ('wanggwan', '왕관산', 'Wanggwan'), ('yumyeongsan', '유명산', 'Yumyeongsan')]),
    ('충청', '충청', 'Chungcheong', [('sobaeksan', '소백산', 'Sobaeksan'), ('gyeryongsan', '계룡산', 'Gyeryongsan'), ('minjusan', '민주지산', 'Minjusan'), ('sikjangsan', '식장산', 'Sikjangsan'), ('woraksan', '월악산', 'Woraksan'), ('songnisan', '속리산', 'Songnisan'), ('heuiyangsan', '희양산', 'Heuiyangsan'), ('cheongtaesan', '청태산', 'Cheongtaesan')]),
    ('전라', '전라', 'Jeolla', [('jirisan', '지리산', 'Jirisan'), ('naejangsan', '내장산', 'Naejangsan'), ('deogyusan', '덕유산', 'Deogyusan'), ('wolchulsan', '월출산', 'Wolchulsan'), ('mudeungsan', '무등산', 'Mudeungsan'), ('duryunsan', '두륜산', 'Duryunsan'), ('daedunsan', '대둔산', 'Daedunsan'), ('maisan', '마이산', 'Maisan'), ('unjangsan', '운장산', 'Unjangsan'), ('yeongchwisan', '영취산', 'Yeongchwisan'), ('baekamsan', '백암산', 'Baekamsan')]),
    ('경상 / 제주', '경상 / 제주', 'Gyeongsang/Jeju', [('gayasan', '가야산', 'Gayasan'), ('juwangsan', '주왕산', 'Juwangsan'), ('hallasan', '한라산', 'Hallasan'), ('geumjeongsan', '금정산', 'Geumjeongsan'), ('palgongsan', '팔공산', 'Palgongsan'), ('unmunsan', '운문산', 'Unmunsan'), ('gajisan', '가지산', 'Gajisan'), ('hwawangsan', '화왕산', 'Hwawangsan'), ('biseulsan', '비슬산', 'Biseulsan'), ('cheongnyangsan', '청량산', 'Cheongnyangsan'), ('namsan', '남산(경주)', 'Namsan (Gyeongju)')]),
    ('인천', '인천', 'Incheon', [('manisan', '마니산', 'Manisan')]),
]
OTHER_COLS = [
    ('대만', 'Taiwan', [('yushan', '위산', 'Yushan'), ('xueshan', '설산', 'Xueshan'), ('yangmingshan', '양명산', 'Yangmingshan'), ('alishan', '아리산', 'Alishan')]),
    ('일본', 'Japan', [('fuji', '후지산', 'Mt. Fuji'), ('tateyama', '타테야마', 'Tateyama')]),
    ('중국', 'China', [('huangshan', '황산', 'Huangshan'), ('taishan', '타이산', 'Taishan')]),
    ('베트남', 'Vietnam', [('fansipan', '판시판', 'Fansipan')]),
    ('말레이시아', 'Malaysia', [('kinabalu', '킨리산', 'Kinabalu')]),
    ('인도네시아', 'Indonesia', [('rinjani', '라위니', 'Rinjani')]),
    ('네팔', 'Nepal', [('poonhill', '푼힐', 'Poon Hill'), ('ebc', '에베레스트 BC', 'Everest BC'), ('act', '안나푸르나 서킷', 'Annapurna Circuit'), ('langtang', '랑탕 밸리', 'Langtang Valley')]),
    ('테마별', 'Themes', [('cycling.html', '사이클링 코스', 'Cycling Courses'), ('map.html', '인터랙티브 지도', 'Interactive Map')]),
]


def col_html(label, links):
    items = '\n'.join(f'        <a href="{fid}{"-playbook.html" if not fid.endswith(".html") else ""}" style="color: var(--muted); text-decoration: none;">{fname}</a>' for fid, fname in links)
    return f'''    <div class="sitemap-col">
      <div style="font-weight: 800; font-size: var(--text-xs); color: var(--text); text-transform: uppercase; margin-bottom: var(--space-3);">{label}</div>
      <div style="display: flex; flex-direction: column; gap: var(--space-2); font-size: var(--text-xs);">
{items}
      </div>
    </div>'''


def build_footer_sitemap(lang):
    cols = [col_html(ko if lang == 'ko' else en, [(fid, fko if lang == 'ko' else fen) for fid, fko, fen in links]) for ko, en, _region, links in KR_COLS]
    cols += [col_html(ko if lang == 'ko' else en, [(fid, fko if lang == 'ko' else fen) for fid, fko, fen in links]) for ko, en, links in OTHER_COLS]
    return '\n'.join(cols)


def replace_footer(s, lang):
    start = s.find('<div class="footer-sitemap"')
    assert start >= 0, 'footer-sitemap 미발견'
    end = s.find('<p style="font-size: var(--text-xs); color: var(--muted); line-height: 1.8; text-align: center;', start)
    assert end > start, 'footer 본문 미발견'
    block = f'''<div class="footer-sitemap" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: var(--space-6); text-align: left; margin-bottom: var(--space-8); border-bottom: 1px solid var(--border); padding-bottom: var(--space-8);">
{build_footer_sitemap(lang)}
  </div>

  '''
    return s[:start] + block + s[end:]


def sub_n(s, old, new, n_expected, label):
    cnt = s.count(old)
    assert cnt == n_expected, f'{label}: 기대 {n_expected}, 실제 {cnt} — "{old[:50]}"'
    return s.replace(old, new)


def patch_index(path, lang):
    s = path.read_text(encoding='utf-8')
    ko = lang == 'ko'
    anchor = "{id:'yumyeongsan', name:'유명산'" if ko else "{id:'yumyeongsan', name:'Yumyeongsan'"
    i = s.find(anchor)
    assert i >= 0, f'{path}: yumyeongsan 앵커 미발견'
    line_end = s.find('\n', i) + 1
    s = s[:line_end] + (M5_KO if ko else M5_EN) + s[line_end:]

    # 소금강 지역 정정 (경기→강원)
    if ko:
        seg = "name:'소금강', alt:'701m', region:'경기'"
        assert s.count(seg) == 1, f'sogeumgang anchor: {s.count(seg)}'
        s = s.replace(seg, "name:'소금강', alt:'701m', region:'강원'")
    else:
        seg = "name:'Sogeumgang', alt:'701m', region:'Gyeonggi'"
        assert s.count(seg) == 1, f'sogeumgang anchor en: {s.count(seg)}'
        s = s.replace(seg, "name:'Sogeumgang', alt:'701m', region:'Gangwon'")

    if ko:
        s = sub_n(s, '>전체 64산<', '>전체 68산<', 1, '칩 전체')
        s = sub_n(s, '>한국 49산<', '>한국 53산<', 1, '칩 한국')
        s = sub_n(s, '>네팔 1산<', '>네팔 4산<', 1, '칩 네팔')
        s = sub_n(s, '>완성됨 (26)<', '>완성됨 (68)<', 1, '완성 필터')
        s = sub_n(s, '<option value="제주">제주</option>', '<option value="제주">제주</option>\n<option value="인천">인천</option>', 1, '지역 옵션')
    else:
        s = sub_n(s, '>All 64 Peaks<', '>All 68 Peaks<', 1, 'chip all')
        s = sub_n(s, '>South Korea · 49<', '>South Korea · 53<', 1, 'chip KR')
        s = sub_n(s, '>Nepal · 1<', '>Nepal · 4<', 1, 'chip NP')
        s = sub_n(s, '>Completed (26)<', '>Completed (68)<', 1, 'done filter')
        s = sub_n(s, '<option value="Jeju">Jeju</option>', '<option value="Jeju">Jeju</option><option value="Incheon">Incheon</option>', 1, 'region option')

    # 스탯 64 → 68 (등록 명산 + 플레이북 완성 2곳)
    s = sub_n(s, '<div class="hero-stat-value">64</div>', '<div class="hero-stat-value">68</div>', 2, '스탯')

    # 히어로 로테이션: langtang 항목 뒤에 신규 4산 추가
    rot_anchor = "{ base: 'assets/img/langtang', video: null, alt: '랑탕 밸리의 기도 깃발과 설산 호수' },\n" if ko else "{ base: '../assets/img/langtang', video: null, alt: 'Langtang\\'s prayer flags and snowy lake' },\n"
    assert s.count(rot_anchor) == 1, f'rotation anchor {path.name}: {s.count(rot_anchor)}'
    s = s.replace(rot_anchor, rot_anchor + (ROT5_KO if ko else ROT5_EN))

    s = replace_footer(s, lang)
    path.write_text(s, encoding='utf-8')
    print(f'{path.name}: patched')


if __name__ == '__main__':
    for p, lang in [(ROOT / 'index.html', 'ko'), (ROOT / 'en/index.html', 'en')]:
        patch_index(p, lang)

    # ── sitemap.xml ──────────────────────────────────────────────
    sp = ROOT / 'sitemap.xml'
    s = sp.read_text(encoding='utf-8')
    BASE = 'https://mttrails.trinos.group/'
    blocks = re.findall(r'<url>.*?</url>', s, re.S)
    fixed = 0
    for b in blocks:
        m = re.search(r'<loc>(.*?)</loc>', b)
        loc = m.group(1)
        stem = loc.split('.group/')[1]
        exp_ko = BASE + (stem.split('en/', 1)[1] if stem.startswith('en/') else stem)
        ko_m = re.search(r'hreflang="ko" href="[^"]*"', b)
        xd_m = re.search(r'hreflang="x-default" href="[^"]*"', b)
        changed = False
        if ko_m and f'href="{exp_ko}"' != ko_m.group(0).split('href=')[1]:
            b2 = re.sub(r'hreflang="ko" href="[^"]*"', f'hreflang="ko" href="{exp_ko}"', b)
            assert b2 != b or f'hreflang="ko" href="{exp_ko}"' in b
            b = b2; changed = True
        if xd_m and f'href="{exp_ko}"' not in xd_m.group(0):
            b2 = re.sub(r'hreflang="x-default" href="[^"]*"', f'hreflang="x-default" href="{exp_ko}"', b)
            b = b2; changed = True
        if changed:
            b = re.sub(r'<lastmod>[^<]*</lastmod>', '<lastmod>2026-09-19</lastmod>', b)
            # 블록 치환: 동일 loc 블록은 유일하므로 원문에서 정확한 이전 블록을 찾아 교체
            old_block = re.search(r'<url>\s*<loc>' + re.escape(loc) + r'</loc>.*?</url>', s, re.S).group(0)
            s = s.replace(old_block, b)
            fixed += 1

    # 신규 8블록 추가 (올바른 hreflang)
    new_blocks = []
    for mid in ('namsan', 'gyebangsan', 'dutasan', 'manisan'):
        for loc_stem, en_stem in ((f'{mid}-playbook.html', f'en/{mid}-playbook.html'),):
            new_blocks.append(f'''  <url>
        <loc>{BASE}{loc_stem}</loc>
        <xhtml:link rel="alternate" hreflang="ko" href="{BASE}{loc_stem}"/>
        <xhtml:link rel="alternate" hreflang="en" href="{BASE}{en_stem}"/>
        <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{loc_stem}"/>
        <lastmod>2026-09-19</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
      </url>
    ''')
            new_blocks.append(f'''  <url>
        <loc>{BASE}en/{mid}-playbook.html</loc>
        <xhtml:link rel="alternate" hreflang="ko" href="{BASE}{mid}-playbook.html"/>
        <xhtml:link rel="alternate" hreflang="en" href="{BASE}en/{mid}-playbook.html"/>
        <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{mid}-playbook.html"/>
        <lastmod>2026-09-19</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
      </url>
    ''')
    s = s.replace('</urlset>\n' if s.rstrip().endswith('</urlset>') else '</urlset>', ''.join(new_blocks) + '</urlset>\n')
    sp.write_text(s, encoding='utf-8')
    print(f'sitemap: fixed {fixed} blocks, appended 8, total urls =', s.count('<url>'))
