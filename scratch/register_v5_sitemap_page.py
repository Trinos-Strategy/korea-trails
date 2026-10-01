# -*- coding: utf-8 -*-
"""sitemap.html / en/sitemap.html 갱신 — 지역 그리드 68산 재생성 + 푸터 재생성."""
import pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from register_v5 import KR_COLS, OTHER_COLS, replace_footer, ROOT

ALT = {
 'bukhansan': '836m', 'dobongsan': '740m', 'myeongseongsan': '922m', 'soyosan': '587m', 'unaksan': '937.5m',
 'gwanaksan': '629m', 'suraksan': '638m', 'cheonggyesan': '618m', 'achasan': '296m', 'inwangsan': '338m',
 'ansan': '500m', 'bulsan': '497m', 'yongmunsan': '1,157m', 'wanggwan': '808m', 'yumyeongsan': '608m',
 'seoraksan': '1,708m', 'chiaksan': '1,288m', 'odaesan': '1,563m', 'taebaeksan': '1,567m',
 'sogeumgang': '701m', 'gyebangsan': '1,577m', 'dutasan': '1,357m',
 'sobaeksan': '1,439m', 'gyeryongsan': '845m', 'minjusan': '1,242m', 'sikjangsan': '656m', 'woraksan': '1,097m',
 'songnisan': '1,058m', 'heuiyangsan': '607m', 'cheongtaesan': '1,166m',
 'jirisan': '1,915m', 'naejangsan': '763m', 'deogyusan': '1,614m', 'wolchulsan': '1,097m', 'mudeungsan': '1,187m',
 'duryunsan': '703m', 'daedunsan': '878m', 'maisan': '683m', 'unjangsan': '1,126m', 'yeongchwisan': '1,090m', 'baekamsan': '1,042m',
 'gayasan': '1,430m', 'juwangsan': '721m', 'hallasan': '1,947m', 'geumjeongsan': '742m', 'palgongsan': '1,192m',
 'unmunsan': '1,188m', 'gajisan': '1,240m', 'hwawangsan': '928m', 'biseulsan': '1,084m', 'cheongnyangsan': '1,093m',
 'namsan': '468m', 'manisan': '469m',
 'yushan': '3,952m', 'xueshan': '3,886m', 'yangmingshan': '1,120m', 'alishan': '2,663m',
 'fuji': '3,776m', 'tateyama': '3,003m', 'huangshan': '1,864m', 'taishan': '1,545m',
 'fansipan': '3,143m', 'kinabalu': '4,095m', 'rinjani': '3,726m',
 'poonhill': '3,210m', 'ebc': '5,364m', 'act': '5,416m', 'langtang': '4,984m',
}
REGION_EN = {'경기/서울': 'Gyeonggi/Seoul', '경상 / 제주': 'Gyeongsang/Jeju'}


def grid(lang):
    cards = []
    for ko_r, en_r, _region, links in KR_COLS:
        title = ko_r if lang == 'ko' else REGION_EN.get(ko_r, en_r)
        items = '\n'.join(
            f'''              <a href="{mid}-playbook.html" class="mountain-link-item">
                <span class="m-name">{(fko if lang == 'ko' else fen)}</span>
                <span class="m-alt">{ALT[mid]}</span>
              </a>''' for mid, fko, fen in links)
        cards.append(f'''          <!-- {title} -->
          <div class="region-card">
            <div class="region-title-wrap">
              <span class="region-title">{title}</span>
              <span class="region-badge">{len(links)}</span>
            </div>
            <div class="mountain-link-list">
{items}
            </div>
          </div>''')
    for ko_c, en_c, links in [c for c in OTHER_COLS if c[0] != '테마별']:
        title = ko_c if lang == 'ko' else en_c
        items = '\n'.join(
            f'''              <a href="{mid}-playbook.html" class="mountain-link-item">
                <span class="m-name">{(fko if lang == 'ko' else fen)}</span>
                <span class="m-alt">{ALT[mid]}</span>
              </a>''' for mid, fko, fen in links)
        cards.append(f'''          <!-- {title} -->
          <div class="region-card">
            <div class="region-title-wrap">
              <span class="region-title">{title}</span>
              <span class="region-badge">{len(links)}</span>
            </div>
            <div class="mountain-link-list">
{items}
            </div>
          </div>''')
    return '        <div class="sitemap-grid-main">\n' + '\n\n'.join(cards) + '\n        </div>'


total = 0
for lang, page in (('ko', 'sitemap.html'), ('en', 'en/sitemap.html')):
    p = ROOT / page
    s = p.read_text(encoding='utf-8')
    start = s.find('        <div class="sitemap-grid-main">')
    assert start > 0, f'{page}: grid 미발견'
    end_marker = '\n        </div>'
    end = s.find(end_marker, start) + len(end_marker)
    s = s[:start] + grid(lang) + s[end:]
    s = replace_footer(s, lang)
    p.write_text(s, encoding='utf-8')
    n = s.count('mountain-link-item')
    total += n
    print(f'{page}: grid+footer 재생성, 링크 {n}개')
print('합계:', total)
