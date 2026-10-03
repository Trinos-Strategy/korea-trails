# -*- coding: utf-8 -*-
"""트랙 확대 2차 — mail.ru 200건 제한 우회: 산별 bbox 쿼리 + 로컬 토큰 매칭."""
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
BAD = re.compile(r'둘레길|서울둘레|City Trail|생태통로')


def overpass(q, t=240):
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


all_rels = {}
for i, (mid, tokens) in enumerate(targets.items()):
    v = cur[mid]
    dlat, dlng = 0.30, 0.36
    q = (f'[out:json][timeout:120];relation["route"="hiking"]'
         f'({v["lat"]-dlat:.4f},{v["lng"]-dlng:.4f},{v["lat"]+dlat:.4f},{v["lng"]+dlng:.4f});out tags center;')
    j = overpass(q)
    els = (j or {}).get('elements', [])
    got = []
    for r in els:
        nm = r.get('tags', {}).get('name', '')
        if not nm or BAD.search(nm):
            continue
        c = r.get('center', {})
        d = hav([c.get('lat', v['lat']), c.get('lon', v['lng'])], [v['lat'], v['lng']])
        if d > 9500:
            continue
        hit = any(t in nm for t in tokens) or v['name'][:3] in nm
        if hit:
            got.append((len(nm), r))
    got.sort(key=lambda x: -x[0])
    all_rels[mid] = [r for _, r in got[:4]]
    print(f'{i+1}/{len(targets)} {mid:14s} {v["name"]:8s} bbox={len(els):3d} hit={len(all_rels[mid])}', flush=True)
    time.sleep(1.2)

pend = [(mid, r['id']) for mid, rs in all_rels.items() for r in rs]
print('geometry:', len(pend), flush=True)
geom = {}
for gi in range(0, len(pend), 8):
    batch = pend[gi:gi + 8]
    q = '[out:json][timeout:180];(' + ''.join(f'relation({rid});' for _, rid in batch) + ');out geom;'
    j = overpass(q)
    for el in (j or {}).get('elements', []):
        pts = []
        for mem in el.get('members', []):
            if mem.get('type') == 'way' and 'geometry' in mem:
                pts.extend([[g['lat'], g['lon']] for g in mem['geometry']])
        geom[el['id']] = pts
    print(f'geom {gi//8+1}/{(len(pend)+7)//8}: +{len((j or {}).get("elements",[]))}', flush=True)
    time.sleep(1.2)

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
print('NEW:', n_new)
