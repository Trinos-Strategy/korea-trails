# -*- coding: utf-8 -*-
"""Overpass 배치 패스 — 유니언 쿼리로 총 요청 ~16건으로 압축.

1) peak 22산 → 쿼리 1건 (union around) → 로컬 근접 매칭
2) 트랙 phase-1 71산 → 쿼리 3건 (25산씩 union) → 로컬 매칭
3) 트랙 phase-2 (relation geometry) → 10 relation씩 ~10건
출력: scratch/peak_nodes.json(엄격 규칙) + assets/data/tracks/*
"""
import json, math, re, subprocess, time, pathlib

ROOT = pathlib.Path('/Users/mac/korea-trails')
OUTDIR = ROOT / 'assets/data/tracks'
EPS = ['https://overpass.private.coffee/api/interpreter', 'https://overpass.kumi.systems/api/interpreter']


def overpass(query, timeout=280):
    for ep in EPS:
        for attempt in range(2):
            r = subprocess.run(['curl', '-s', '--max-time', str(timeout), '--data', query, ep],
                               capture_output=True, text=False)
            raw = r.stdout.decode('utf-8', errors='replace')
            if raw.startswith('{'):
                try:
                    return json.loads(raw)
                except Exception:
                    pass
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


s = (ROOT / 'index.html').read_text(encoding='utf-8')
m = re.search(r'window\.MOUNTAINS = \[(.*?)\n\];', s, re.S)
cur = {e.group(1): dict(name=e.group(2), alt=e.group(3), lat=float(e.group(4)), lng=float(e.group(5)))
       for e in re.finditer(r"\{id:'(\w+)',\s*name:'([^']+)',\s*alt:'([^']*)'.*?lat:\s*([-\d.]+),\s*lng:\s*([-\d.]+)", m.group(1))}
viol = json.load(open('/tmp/violators.json'))

# ── 1) peak 배치 (1쿼리) ──
parts = []
for mid in viol:
    v = cur[mid]
    parts.append(f'node["natural"="peak"](around:10000,{v["lat"]},{v["lng"]});')
q = '[out:json][timeout:240];(' + ''.join(parts) + ');out body;'
print('PEAK batch query...', flush=True)
j = overpass(q)
nodes = (j or {}).get('elements', [])
print('peak nodes:', len(nodes), flush=True)
peaks = {}
for mid in viol:
    v = cur[mid]
    base = re.sub(r'\(.*?\)', '', v['name']).strip()
    our = float(re.search(r'([\d.]+)', v['alt'].replace(',', '').replace('노인봉', '')).group(1))
    near = [n for n in nodes if n.get('tags', {}).get('ele') and
            hav([n['lat'], n['lon']], [v['lat'], v['lng']]) < 10000]
    best = None
    for n in near:
        e = float(n['tags']['ele'])
        if abs(e - our) <= 100:
            best = (e, n)
            break
    if not best:
        named = [n for n in near if base[:2] in n['tags'].get('name', '')]
        if named:
            tall = max(named, key=lambda n: float(n['tags']['ele']))
            e = float(tall['tags']['ele'])
            if abs(e - our) <= 180:
                best = (e, tall)
    if best:
        e, n = best
        peaks[mid] = dict(name=n['tags'].get('name', ''), ele=e, lat=n['lat'], lng=n['lon'], our=our)
        print(f'PEAK {mid:14s} → {n["tags"].get("name", "")} ele={e:.0f} ({n["lat"]:.5f},{n["lon"]:.5f})', flush=True)
    else:
        peaks[mid] = None
        print(f'PEAK {mid:14s} → none', flush=True)
json.dump(peaks, open(ROOT / 'scratch/peak_nodes.json', 'w'), ensure_ascii=False, indent=1)

# ── 2) 트랙 phase-1 배치 (3쿼리) ──
mids = list(cur)
OVERSEAS = {'yushan', 'xueshan', 'yangmingshan', 'alishan', 'huangshan', 'tateyama', 'fansipan',
            'taishan', 'kinabalu', 'rinjani', 'poonhill', 'ebc', 'act', 'langtang', 'fuji'}
rels_by_mid = {mid: [] for mid in mids}
for ci in range(0, len(mids), 25):
    chunk = mids[ci:ci + 25]
    parts = []
    for mid in chunk:
        v = cur[mid]
        radius = 15000 if mid in OVERSEAS else 8000
        parts.append(f'relation["route"="hiking"](around:{radius},{v["lat"]},{v["lng"]});')
    q = '[out:json][timeout:240];(' + ''.join(parts) + ');out tags center;'
    print(f'REL batch {ci//25+1}/3...', flush=True)
    j = overpass(q)
    els = (j or {}).get('elements', [])
    print('  rels:', len(els), flush=True)
    for mid in chunk:
        v = cur[mid]
        base = re.sub(r'\(.*?\)', '', v['name']).strip()
        got = []
        for r in els:
            nm = r.get('tags', {}).get('name', '')
            if nm and hav([r.get('center', {}).get('lat', v['lat']), r.get('center', {}).get('lon', v['lng'])],
                          [v['lat'], v['lng']]) < (16000 if mid in OVERSEAS else 9000):
                got.append((base in nm or nm in base, r))
        got.sort(key=lambda x: -x[0])
        rels_by_mid[mid] = [r for _, r in got[:6]]
    time.sleep(2)

# ── 3) geometry 배치 (10 relation/쿼리) ──
def rel_distance_geom(rid_batch):
    q = '[out:json][timeout:280];(' + ''.join(f'relation({rid});' for rid in rid_batch) + ');out geom;'
    j = overpass(q)
    out = {}
    for el in (j or {}).get('elements', []):
        pts = []
        for mem in el.get('members', []):
            if mem.get('type') == 'way' and 'geometry' in mem:
                pts.extend([[g['lat'], g['lon']] for g in mem['geometry']])
        out[el['id']] = pts
    return out


index = {}
pending = []
for mid in mids:
    for r in rels_by_mid[mid]:
        pending.append((mid, r['id']))
print('relations to fetch:', len(pending), flush=True)
geom_all = {}
for gi in range(0, len(pending), 10):
    batch = pending[gi:gi + 10]
    ids = [rid for _, rid in batch]
    got = rel_distance_geom(ids)
    geom_all.update(got)
    print(f'geom {gi//10+1}/{(len(pending)+9)//10} → {len(got)}', flush=True)
    time.sleep(2)

for mid in mids:
    v = cur[mid]
    base = re.sub(r'\(.*?\)', '', v['name']).strip()
    picked = []
    for r in rels_by_mid[mid]:
        pts = geom_all.get(r['id'])
        if not pts or len(pts) < 30:
            continue
        d = sum(hav(pts[i - 1], pts[i]) for i in range(1, len(pts)))
        km = round(d / 1000.0, 1)
        if km < 1.0:
            continue
        picked.append(dict(osm=r['id'], name=r.get('tags', {}).get('name', ''), km=km, points=simplify(pts)))
        if len(picked) >= 3:
            break
    index[mid] = dict(name=v['name'], routes=len(picked), kms=[p['km'] for p in picked])
    if picked:
        (OUTDIR / f'{mid}.json').write_text(json.dumps(dict(
            mountain=base, attribution='© OpenStreetMap contributors (ODbL)',
            routes=picked), ensure_ascii=False), encoding='utf-8')
    print(f'TRACK {mid:14s} {v["name"]:10s} picked={len(picked)} {[p["km"] for p in picked]}', flush=True)

(OUTDIR / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')
print('ALL DONE', flush=True)
