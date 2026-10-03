# -*- coding: utf-8 -*-
"""트랙 커버리지 확대 — 코스명 사전 기반 Overpass 매칭 (maps.mail.ru 미러).

1) 산별 코스명 토큰으로 name~regex 매칭 (산명 직접 포함 제외 — 오탐 방지용 BAD 필터)
2) geometry 배치 수집 → 하버사인 km → 정화 규칙(km 1~45, BAD, 최대 3루트)
"""
import json, math, re, subprocess, time, pathlib

TD = pathlib.Path('/Users/mac/korea-trails/assets/data/tracks')
EP = 'https://maps.mail.ru/osm/tools/overpass/api/interpreter'
UA = 'MTTrailsBot/1.0 (contact: dkkim@swonlaw.com)'

targets = json.load(open('/tmp/track_targets.json', encoding='utf-8'))
cur = {}
s = open('/Users/mac/korea-trails/index.html', encoding='utf-8').read()
m = re.search(r'window\.MOUNTAINS = \[(.*?)\n\];', s, re.S)
for e in re.finditer(r"\{id:'(\w+)',\s*name:'([^']+)'.*?lat:\s*([-\d.]+),\s*lng:\s*([-\d.]+)", m.group(1)):
    cur[e.group(1)] = dict(name=re.sub(r'\(.*?\)', '', e.group(2)).strip(), lat=float(e.group(3)), lng=float(e.group(4)))

BAD = re.compile(r'둘레길|서울둘레|City Trail|둘레|생태통로|둘레|구간')


def overpass(q, t=180):
    for _ in range(3):
        r = subprocess.run(['curl', '-s', '--max-time', str(t), '-A', UA, '--data', q, EP],
                           capture_output=True, text=False)
        try:
            return json.loads(r.stdout.decode('utf-8', errors='replace'))
        except Exception:
            time.sleep(4)
    return None


def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    x = math.cos(la1) * math.cos(la2) * (math.cos(lo2) - math.cos(lo1))
    y = math.cos(la1) * math.sin(lo2) - math.cos(la2) * math.sin(lo1)
    z = math.sin(la2) - math.sin(la1)
    return 6371000.0 * 2 * math.asin(math.sqrt(x * x + y * y + z * z))


def simplify(pts, cap=260):
    if len(pts) <= cap:
        return pts
    step = len(pts) / cap
    return [pts[int(i * step)] for i in range(cap)]


# 1단계: 토큰 매칭
all_rels = {}
items = list(targets.items())
for ci in range(0, len(items), 15):
    chunk = items[ci:ci + 15]
    for mid, tokens in chunk:
        v = cur[mid]
        rx = '|'.join(re.escape(t) for t in tokens[:15])
        q = (f'[out:json][timeout:60];relation["route"="hiking"]["name"~"{rx}"]'
             f'(around:9000,{v["lat"]},{v["lng"]});out tags center;')
        j = overpass(q)
        els = (j or {}).get('elements', [])
        got = []
        for r in els:
            nm = r.get('tags', {}).get('name', '')
            if nm and not BAD.search(nm):
                c = r.get('center', {})
                d = hav([c.get('lat', v['lat']), c.get('lon', v['lng'])], [v['lat'], v['lng']])
                if d < 9500:
                    got.append(r)
        got.sort(key=lambda r: -len(r.get('tags', {}).get('name', '')))
        all_rels[mid] = got[:4]
        print(f'{mid:14s} {v["name"]:8s} tokens→{len(got)} rels', flush=True)
        time.sleep(1.5)

pend = [(mid, r['id']) for mid, rs in all_rels.items() for r in rs]
print('geometry to fetch:', len(pend), flush=True)
geom = {}
for gi in range(0, len(pend), 8):
    batch = pend[gi:gi + 8]
    q = '[out:json][timeout:120];(' + ''.join(f'relation({rid});' for _, rid in batch) + ');out geom;'
    j = overpass(q)
    els = (j or {}).get('elements', [])
    for el in els:
        pts = []
        for mem in el.get('members', []):
            if mem.get('type') == 'way' and 'geometry' in mem:
                pts.extend([[g['lat'], g['lon']] for g in mem['geometry']])
        geom[el['id']] = pts
    print(f'geom {gi//8+1}/{(len(pend)+7)//8}: +{len(els)}', flush=True)
    time.sleep(1.5)

n_new = 0
for mid, rs in all_rels.items():
    picked = []
    for r in rs:
        pts = geom.get(r['id'])
        if not pts or len(pts) < 30:
            continue
        d = sum(hav(pts[i - 1], pts[i]) for i in range(1, len(pts)))
        km = round(d / 1000.0, 1)
        if km < 1.0 or km > 45:
            continue
        picked.append(dict(osm=r['id'], name=r.get('tags', {}).get('name', ''), km=km, points=simplify(pts)))
        if len(picked) >= 3:
            break
    if not picked:
        continue
    f = TD / f'{mid}.json'
    if f.exists():
        d_old = json.loads(f.read_text(encoding='utf-8'))
        have_names = {r['name'] for r in d_old['routes']}
        picked = [p for p in picked if p['name'] not in have_names]
        if not picked:
            continue
        picked = (d_old['routes'] + picked)[:3]
    (TD / f'{mid}.json').write_text(json.dumps(dict(
        mountain=cur[mid]['name'], attribution='© OpenStreetMap contributors (ODbL)',
        routes=picked), ensure_ascii=False), encoding='utf-8')
    n_new += 1
    print(f'WROTE {mid:14s}', [f"{p['name']}({p['km']}km)" for p in picked], flush=True)
print('NEW mountains with tracks:', n_new)
