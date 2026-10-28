# -*- coding: utf-8 -*-
"""트랙·페이지 정합 검증 (world.run 게이트용). 종료코드: 0=통과, 1=실패."""
import html.parser, json, pathlib, sys, subprocess

ROOT = pathlib.Path('/Users/mac/korea-trails')
fail = []


class P(html.parser.HTMLParser):
    def error(self, msg):
        raise ValueError(msg)


n = 0
try:
    for f in sorted(ROOT.glob('*.html')) + sorted((ROOT / 'en').glob('*.html')):
        P(convert_charrefs=True).feed(f.read_text(encoding='utf-8'))
        n += 1
except Exception as e:
    fail.append(f'parse {e}')
print(f'parse: {n} files')

TD = ROOT / 'assets/data/tracks'
tot = 0
for f in sorted(TD.glob('*.json')):
    if f.name == 'index.json':
        continue
    try:
        d = json.loads(f.read_text(encoding='utf-8'))
        for r in d['routes']:
            assert len(r['points']) > 30, 'points too few'
            assert 1.0 <= r['km'] <= 60, f'km range {r["km"]}'
            tot += 1
    except Exception as e:
        fail.append(f'track {f.name}: {e}')
print(f'tracks: {tot} routes / {len([f for f in TD.glob("*.json") if f.name != "index.json"])} mountains')

# MOUNTAINS 대칭 + geo 정합
import re
s = (ROOT / 'index.html').read_text(encoding='utf-8')
m = re.search(r'window\.MOUNTAINS = \[(.*?)\n\];', s, re.S)
coords = {e.group(1): (e.group(2), e.group(3)) for e in re.finditer(r"\{id:'(\w+)'[^}]*?lat:\s*([-\d.]+),\s*lng:\s*([-\d.]+)", m.group(1))}
se = (ROOT / 'en/index.html').read_text(encoding='utf-8')
me = re.search(r'window\.MOUNTAINS = \[(.*?)\n\];', se, re.S)
coordse = {e.group(1): (e.group(2), e.group(3)) for e in re.finditer(r"\{id:'(\w+)'[^}]*?lat:\s*([-\d.]+),\s*lng:\s*([-\d.]+)", me.group(1))}
if coords != coordse:
    fail.append('KO/EN MOUNTAINS 좌표 불일치')
geo_bad = 0
for mid, (lat, lng) in coords.items():
    for pth in (ROOT / f'{mid}-playbook.html', ROOT / 'en' / f'{mid}-playbook.html'):
        g = re.search(r'"latitude":\s*([-\d.]+),\s*"longitude":\s*([-\d.]+)', pth.read_text(encoding='utf-8'))
        if not g or abs(float(g.group(1)) - float(lat)) > 1e-9 or abs(float(g.group(2)) - float(lng)) > 1e-9:
            geo_bad += 1
print(f'geo mismatch: {geo_bad}')
if geo_bad:
    fail.append(f'geo mismatch {geo_bad}')

r = subprocess.run(['node', '--check', str(ROOT / 'assets/js/deep-info.js')], capture_output=True, text=True)
if r.returncode != 0:
    fail.append('node --check deep-info.js')
r = subprocess.run(['node', '--check', str(ROOT / 'assets/js/deep-info-data.js')], capture_output=True, text=True)
if r.returncode != 0:
    fail.append('node --check deep-info-data.js')

if fail:
    print('FAIL:', fail)
    sys.exit(1)
print('ALL OK')
