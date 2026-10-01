# -*- coding: utf-8 -*-
"""2차 좌표 정밀화 — DEM QA로 적발된 20산 (OSM peak 노드 × 나무위키 × DEM 국소최대 2소스)."""
import json, pathlib, re

ROOT = pathlib.Path('/Users/mac/korea-trails')
FIXES = {
    # OSM natural=peak 노드 (ele ±100m 일치 + DEM 확인)
    'mudeungsan':   (35.12504, 127.00857),
    'hwawangsan':   (35.54715, 128.53169),
    'daedunsan':    (36.12459, 127.32048),
    'woraksan':     (36.88608, 128.10584),
    'odaesan':      (37.79375, 128.54265),
    'alishan':      (23.53573, 120.80853),
    'chiaksan':     (37.36515, 128.05563),
    'maisan':       (35.76054, 127.41150),
    'cheonggyesan': (37.40409, 127.04377),
    'sobaeksan':    (36.94743, 128.46279),
    'baegunsan':    (35.24090, 127.55767),
    # 나무위키 좌표 × DEM 확인
    'yongmunsan':   (37.56472, 127.54556),
    'songnisan':    (36.54389, 127.87083),
    # DEM 국소최대 × 문서 정점 일치
    'yangmingshan': (25.1685, 121.5565),
    'cheongtaesan': (37.4265, 128.4535),
    'dutasan':      (37.223, 129.1135),
    'yeongchwisan': (34.7915, 127.698),
    'gamaksan':     (37.9415, 126.9715),
    'sogeumgang':   (37.7758, 128.5967),
    'baekamsan':    (35.468, 126.772),
}


def set_latlng(text, mid, lat, lng):
    pat = re.compile(r"(\{id:'" + mid + r"'[^}]*?lat:\s*)([-\d.]+)(,\s*lng:\s*)([-\d.]+)(\})")
    assert len(pat.findall(text)) == 1, mid
    return pat.sub(lambda m: f'{m.group(1)}{lat}{m.group(3)}{lng}{m.group(5)}', text, count=1)


def main():
    for page in ('index.html', 'en/index.html'):
        p = ROOT / page
        s = p.read_text(encoding='utf-8')
        for mid, (lat, lng) in FIXES.items():
            s = set_latlng(s, mid, lat, lng)
        p.write_text(s, encoding='utf-8')
        print('coords', page, len(FIXES))

    # DEEP_COORDS 갱신
    for f in ('assets/js/deep-info-data.js', 'assets/js/deep-info-data-en.js'):
        p = ROOT / f
        s = p.read_text(encoding='utf-8')
        m = re.search(r'window\.DEEP_COORDS = (\{.*?\});\n', s, re.S)
        assert m, f
        coords = json.loads(m.group(1))
        for mid, (lat, lng) in FIXES.items():
            coords[mid][0], coords[mid][1] = lat, lng
        s = s[:m.start()] + 'window.DEEP_COORDS = ' + json.dumps(coords, separators=(',', ':')) + ';\n' + s[m.end():]
        p.write_text(s, encoding='utf-8')
        print('deep_coords', f)

    # JSON-LD geo 갱신
    n = 0
    for mid, (lat, lng) in FIXES.items():
        for f in (ROOT / f'{mid}-playbook.html', ROOT / 'en' / f'{mid}-playbook.html'):
            s = f.read_text(encoding='utf-8')
            pat = re.compile(r'("geo":\s*\{"@type":\s*"GeoCoordinates",\s*"latitude":\s*)([-\d.]+)(,\s*"longitude":\s*)([-\d.]+)(\})')
            s2, c = pat.subn(lambda mm: f'{mm.group(1)}{lat}{mm.group(3)}{lng}{mm.group(5)}', s, count=1)
            assert c == 1, f
            n += s2 != s
            f.write_text(s2, encoding='utf-8')
    print('jsonld geo:', n)


if __name__ == '__main__':
    main()
