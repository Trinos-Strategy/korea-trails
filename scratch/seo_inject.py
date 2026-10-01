# -*- coding: utf-8 -*-
"""Q3 SEO — JSON-LD(TouristAttraction+BreadcrumbList / WebSite+Organization) + canonical + og:type + twitter 보충."""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://mttrails.trinos.group'


def mountains():
    out = {}
    for page, lang, pfx in (('index.html', 'ko', ''), ('en/index.html', 'en', '../')):
        s = (ROOT / page).read_text(encoding='utf-8')
        m = re.search(r'window\.MOUNTAINS = \[(.*?)\n\];', s, re.S)
        for e in re.finditer(r"\{id:'(\w+)'[^}]*\}", m.group(1)):
            t = e.group(0)
            def f(k):
                mm = re.search(k + r":'([^']*)'", t)
                return mm.group(1) if mm else ''
            out.setdefault(f('id'), {})[lang] = dict(name=f('name'), alt=f('alt'), url=f('url'),
                                                     lat=f('lat') if 'lat:' in t else None,
                                                     lng=f('lng') if 'lng:' in t else None)
    return out


M = mountains()
pages = sorted(ROOT.glob('*.html')) + sorted((ROOT / 'en').glob('*.html'))
n_pb, n_site = 0, 0
for p in pages:
    s = p.read_text(encoding='utf-8')
    rel = str(p.relative_to(ROOT))
    lang = 'en' if rel.startswith('en/') else 'ko'
    is_en = rel.startswith('en/')
    stem = p.stem
    canon = f'{BASE}/{rel}'
    inject = []
    if 'rel="canonical"' not in s:
        inject.append(f'<link href="{canon}" rel="canonical"/>')
    mid = stem.replace('-playbook', '') if stem.endswith('-playbook') else None
    if mid and mid in M:
        d = M[mid].get(lang) or M[mid]['ko']
        alt_ko = d.get('alt', '')
        ld = {
            '@context': 'https://schema.org', '@type': 'TouristAttraction',
            'name': d['name'], 'description': f"{d.get('name','')} 등산 플레이북 — 코스·고도·교통·안전 정보." if lang == 'ko' else f"{d.get('name','')} hiking playbook — courses, elevation, transit and safety.",
            'url': canon,
            'inLanguage': 'ko' if lang == 'ko' else 'en',
        }
        try:
            lat = re.search(r'lat:\s*([\d.]+)', s) or None
            mk = re.search(r"lat:\s*([\d.]+),\s*lng:\s*([\d.]+)", s)
        except Exception:
            mk = None
        # MOUNTAINS 값은 index에 있으므로 원页 아닌 페이지는 M에서 위도 경도 재추출
        row = M[mid].get(lang) or M[mid]['ko']
        src = (ROOT / 'index.html').read_text(encoding='utf-8')
        mm = re.search(r"\{id:'" + mid + r"'[^}]*lat:\s*([\d.]+),\s*lng:\s*([\d.]+)", src)
        if mm:
            ld['geo'] = {'@type': 'GeoCoordinates', 'latitude': float(mm.group(1)), 'longitude': float(mm.group(2))}
        ld['image'] = f'{BASE}/assets/img/{mid}/og.jpg'
        crumb = {
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home' if lang == 'en' else '홈',
                 'item': BASE + ('/en/index.html' if is_en else '/')},
                {'@type': 'ListItem', 'position': 2, 'name': d['name'], 'item': canon},
            ],
        }
        ld_s = json.dumps(ld, ensure_ascii=False).replace('</', '<\\/')
        cr_s = json.dumps(crumb, ensure_ascii=False).replace('</', '<\\/')
        inject.append(f'<script type="application/ld+json">{ld_s}</script>')
        inject.append(f'<script type="application/ld+json">{cr_s}</script>')
        if 'og:type' not in s:
            inject.append('<meta content="article" property="og:type"/>')
        n_pb += 1
    else:
        ld = {'@context': 'https://schema.org', '@type': 'WebSite',
              'name': 'MT Trails', 'url': canon, 'inLanguage': 'ko' if lang == 'ko' else 'en'}
        org = {'@context': 'https://schema.org', '@type': 'Organization', 'name': 'MT Trails',
               'url': BASE, 'logo': f'{BASE}/assets/brand/logo.svg'}
        inject.append(f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')
        inject.append(f'<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>')
        n_site += 1
    if 'twitter:' not in s:
        inject.append('<meta content="summary_large_image" name="twitter:card"/>')
        inject.append('<meta content="MT Trails" name="twitter:site"/>')
    if inject:
        block = '\n'.join('  ' + x for x in inject)
        marker = '</head>'
        assert marker in s, rel
        s = s.replace(marker, block + '\n</head>', 1)
        p.write_text(s, encoding='utf-8')

print(f'SEO 주입: 플레이북 {n_pb} + 사이트 {n_site} = {n_pb + n_site}페이지')
# 재주입 방지 검증
for p in pages:
    s = p.read_text(encoding='utf-8')
    assert s.count('application/ld+json') <= 3, f'과잉 주입: {p}'
print('과잉 주입 없음 ✓')
