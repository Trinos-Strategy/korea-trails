# -*- coding: utf-8 -*-
"""워커 D — 트랙 JSON에 실측 고도 프로파일 첨부 (Open-Meteo Elevation, 50점/호출)."""
import json, math, subprocess, time, pathlib

ROOT = pathlib.Path('/Users/mac/korea-trails')
TD = ROOT / 'assets/data/tracks'


def elev_batch(pairs):
    la = ','.join(f'{p[0]:.5f}' for p in pairs)
    lo = ','.join(f'{p[1]:.5f}' for p in pairs)
    for _ in range(3):
        r = subprocess.run(['curl', '-s', '--max-time', '40',
                            f'https://api.open-meteo.com/v1/elevation?latitude={la}&longitude={lo}'],
                           capture_output=True, text=True)
        try:
            return json.loads(r.stdout)['elevation']
        except Exception:
            time.sleep(3)
    return None


files = sorted(TD.glob('*.json'))
n_route = 0
for f in files:
    if f.name == 'index.json':
        continue
    d = json.loads(f.read_text(encoding='utf-8'))
    changed = False
    for rt in d.get('routes', []):
        if rt.get('profile'):
            continue
        pts = rt['points']
        step = max(1, math.ceil(len(pts) / 100))
        sample = pts[::step]
        el = elev_batch(sample)
        if el and len(el) == len(sample):
            rt['profile'] = [round(v, 1) for v in el]
            n_route += 1
            changed = True
        time.sleep(0.4)
    if changed:
        f.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
        print(f.name, 'profiled', flush=True)
print('DONE routes:', n_route)
