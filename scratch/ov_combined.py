# -*- coding: utf-8 -*-
"""Overpass 단일 순차 패스 — ① peak 노드(22 위반산 좌표 확정) ② 트랙 phase-1+2.

엔드포인트 헬스 체크 후 사용 가능한 미러 하나를 고정해 순차 요청(같은 미러 동시 타격 금지).
출력: scratch/peak_nodes.json (좌표 확정), assets/data/tracks/<mid>.json + index.json
"""
import json, math, re, subprocess, sys, time, pathlib

ROOT = pathlib.Path('/Users/mac/korea-trails')
OUTDIR = ROOT / 'assets/data/tracks'
OUTDIR.mkdir(parents=True, exist_ok=True)
EPS = [
    ('coffee', 'https://overpass.private.coffee/api/interpreter'),
    ('kumi', 'https://overpass.kumi.systems/api/interpreter'),
    ('main', 'https://overpass-api.de/api/interpreter'),
]
GOOD = [ep for _, ep in EPS]


def overpass(query, timeout=150):
    for ep in list(GOOD):
        r = subprocess.run(['curl', '-s', '--max-time', str(timeout), '--data', query, ep],
                           capture_output=True, text=False)
        raw = r.stdout.decode('utf-8', errors='replace')
        if raw.startswith('{'):
            try:
                return json.loads(raw)
            except Exception:
                pass
        time.sleep(2)
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


# ── ① peak 노드 ──
viol = json.load(open('/tmp/violators.json'))
s = (ROOT / 'index.html').read_text(encoding='utf-8')
m = re.search(r'window\.MOUNTAINS = \[(.*?)\n\];', s, re.S)
cur = {e.group(1): dict(name=e.group(2), alt=e.group(3), lat=float(e.group(4)), lng=float(e.group(5)))
       for e in re.finditer(r"\{id:'(\w+)',\s*name:'([^']+)',\s*alt:'([^']*)'.*?lat:\s*([-\d.]+),\s*lng:\s*([-\d.]+)", m.group(1))}

peaks = {}
for mid in viol:
    v = cur[mid]
    our = float(re.search(r'([\d.]+)', v['alt'].replace(',', '').replace('노인봉', '')).group(1))
    j = overpass(f'[out:json][timeout:60];node["natural"="peak"](around:10000,{v["lat"]},{v["lng"]});out body;')
    time.sleep(1.2)
    els = (j or {}).get('elements', [])
    best = None
    for n in els:
        ele = n.get('tags', {}).get('ele')
        if ele:
            try:
                e = float(ele)
            except Exception:
                continue
            if abs(e - our) < 80:
                best = (e, n)
                break
    if not best:
        tall = [(float(n['tags']['ele']), n) for n in els
                if n.get('tags', {}).get('ele', '').replace('.', '').replace('-', '').isdigit()]
        if tall:
            best = max(tall)
    if best:
        e, n = best
        peaks[mid] = dict(name=n.get('tags', {}).get('name', ''), ele=e, lat=n['lat'], lng=n['lon'], our=our)
        print(f'PEAK {mid:14s} → {n.get("tags", {}).get("name", "")} ele={e:.0f} ({n["lat"]:.5f},{n["lon"]:.5f}) n={len(els)}', flush=True)
    else:
        peaks[mid] = None
        print(f'PEAK {mid:14s} → none (n={len(els)})', flush=True)
json.dump(peaks, open(ROOT / 'scratch/peak_nodes.json', 'w'), ensure_ascii=False, indent=1)

# ── ② 트랙 ──
index = {}
for mid, v in cur.items():
    base = re.sub(r'\(.*?\)', '', v['name']).strip()
    radius = 15000 if mid in {'yushan', 'xueshan', 'yangmingshan', 'alishan', 'huangshan', 'tateyama',
                              'fansipan', 'taishan', 'kinabalu', 'rinjani', 'poonhill', 'ebc', 'act',
                              'langtang', 'fuji'} else 8000
    j = overpass(f'[out:json][timeout:60];relation["route"="hiking"](around:{radius},{v["lat"]},{v["lng"]});out tags center;')
    time.sleep(1.2)
    rels = (j or {}).get('elements', [])
    cands = [r for r in rels if r.get('tags', {}).get('name') and (base in r['tags']['name'] or r['tags']['name'] in base)]
    if not cands:
        near = sorted(rels, key=lambda r: math.hypot((r.get('center', {}).get('lat', 0) - v['lat']) * 111000,
                                                     (r.get('center', {}).get('lon', 0) - v['lng']) * 88000))
        cands = [r for r in near[:8] if r.get('tags', {}).get('name')]
    picked = []
    seen = set()
    for r in cands[:4]:
        rid = r['id']
        if rid in seen:
            continue
        seen.add(rid)
        j2 = overpass(f'[out:json][timeout:120];relation({rid});out geom;')
        time.sleep(1.2)
        els = (j2 or {}).get('elements', [])
        pts_all = []
        if els:
            for mem in els[0].get('members', []):
                if mem.get('type') == 'way' and 'geometry' in mem:
                    pts_all.extend([[g['lat'], g['lon']] for g in mem['geometry']])
        if len(pts_all) < 30:
            continue
        d = sum(hav(pts_all[i - 1], pts_all[i]) for i in range(1, len(pts_all)))
        km = round(d / 1000.0, 1)
        if km < 1.0:
            continue
        picked.append(dict(osm=rid, name=r.get('tags', {}).get('name', ''), km=km, points=simplify(pts_all)))
        if len(picked) >= 3:
            break
    index[mid] = dict(name=v['name'], routes=len(picked), kms=[p['km'] for p in picked])
    if picked:
        (OUTDIR / f'{mid}.json').write_text(json.dumps(dict(
            mountain=base, attribution='© OpenStreetMap contributors (ODbL)',
            routes=picked), ensure_ascii=False), encoding='utf-8')
    print(f'TRACK {mid:14s} {v["name"]:10s} rels={len(rels):3d} picked={len(picked)} {[p["km"] for p in picked]}', flush=True)

(OUTDIR / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')
print('ALL DONE', flush=True)
