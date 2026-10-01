# -*- coding: utf-8 -*-
"""워커 B — OSM Overpass로 71산 실측 등산로(hiking route) 수집 → assets/data/tracks/<mid>.json.

1단계: 산별로 정점 반경 8km의 route=hiking relation 검색(out tags center) → 이름 매칭 선별
2단계: 선별 relation의 실측 geometry 다운로드(out geom) → 거리 계산(하버사인) → ≤300점 단순화
출력: assets/data/tracks/<mid>.json {mountain, attribution, routes:[{name, km, points}]}
     + assets/data/tracks/index.json (커버리지)
ODbL: © OpenStreetMap contributors (attribution 필수 — 렌더러에 명시)
"""
import json, math, re, subprocess, time, pathlib, urllib.parse

ROOT = pathlib.Path('/Users/mac/korea-trails')
OUTDIR = ROOT / 'assets/data/tracks'
OUTDIR.mkdir(parents=True, exist_ok=True)
UA = 'MTTrailsBot/1.0 (contact: dkkim@swonlaw.com)'
EPS = ['https://overpass.private.coffee/api/interpreter', 'https://overpass-api.de/api/interpreter']

cur = {}
s = (ROOT / 'index.html').read_text(encoding='utf-8')
m = re.search(r'window\.MOUNTAINS = \[(.*?)\n\];', s, re.S)
for e in re.finditer(r"\{id:'(\w+)',\s*name:'([^']+)'.*?lat:\s*([-\d.]+),\s*lng:\s*([-\d.]+)", m.group(1)):
    cur[e.group(1)] = dict(name=e.group(2), lat=float(e.group(3)), lng=float(e.group(4)))

# 국제 산(OSM 한국 밖)도 동일 절차 — 네팔 트레킹 루트는 OSM에 잘 매핑됨
OVERSEAS = {'yushan', 'xueshan', 'yangmingshan', 'alishan', 'huangshan', 'tateyama', 'fansipan',
            'taishan', 'kinabalu', 'rinjani', 'poonhill', 'ebc', 'act', 'langtang', 'fuji'}


def overpass(query):
    for ep in EPS:
        r = subprocess.run(['curl', '-s', '--max-time', '90', '-A', UA, '--data', query, ep],
                           capture_output=True, text=False)
        try:
            return json.loads(r.stdout.decode('utf-8', errors='replace'))
        except Exception:
            time.sleep(3)
    return None


def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    x = math.cos(la1) * math.cos(la2) * (math.cos(lo2) - math.cos(lo1))
    y = math.cos(la1) * math.sin(lo2) - math.cos(la2) * math.sin(lo1)
    z = math.sin(la2) - math.sin(la1)
    return 6371000.0 * 2 * math.asin(math.sqrt(x * x + y * y + z * z))


def rel_distance(geom):
    pts = [[g['lat'], g['lon']] for g in geom if 'lat' in g and 'lon' in g]
    d = 0.0
    for i in range(1, len(pts)):
        d += hav(pts[i - 1], pts[i])
    return d, pts


def simplify(pts, cap=300):
    if len(pts) <= cap:
        return pts
    step = len(pts) / cap
    return [pts[int(i * step)] for i in range(cap)]


index = {}
for mid, v in cur.items():
    name = v['name']
    base = re.sub(r'\(.*?\)', '', name).strip()          # '위산(玉山)' → '위산'
    key = base[:3] if not base.endswith('산') else base   # 매칭 키
    radius = 15000 if mid in OVERSEAS else 8000
    q = f'[out:json][timeout:60];relation["route"="hiking"](around:{radius},{v["lat"]},{v["lng"]});out tags center;'
    j = overpass(q)
    time.sleep(1.5)
    rels = (j or {}).get('elements', [])
    cands = []
    for r in rels:
        tg = r.get('tags', {})
        nm = tg.get('name', '')
        if base and (base in nm or nm in base):
            cands.append(r)
    if not cands:
        near = sorted(rels, key=lambda r: math.hypot((r.get('center', {}).get('lat', 0) - v['lat']) * 111000,
                                                     (r.get('center', {}).get('lon', 0) - v['lng']) * 88000))
        cands = [r for r in near[:8] if r.get('tags', {}).get('name')]
        (ROOT / 'scratch/osm_phase1.json').open('a').write(json.dumps(dict(mid=mid, phase='fallback', names=[r.get('tags',{}).get('name','') for r in cands]), ensure_ascii=False) + '\n')
    picked = []
    seen = set()
    for r in cands[:4]:
        rid = r['id']
        if rid in seen:
            continue
        seen.add(rid)
        q2 = f'[out:json][timeout:90];relation({rid});out geom;'
        j2 = overpass(q2)
        time.sleep(1.5)
        els = (j2 or {}).get('elements', [])
        if not els:
            continue
        pts_all = []
        for mem in els[0].get('members', []):
            if mem.get('type') == 'way' and 'geometry' in mem:
                pts_all.extend([[g['lat'], g['lon']] for g in mem['geometry']])
        if len(pts_all) < 30:
            continue
        d_m, pts = rel_distance(pts_all)
        km = round(d_m / 1000.0, 1)
        if km < 1.0:
            continue
        picked.append(dict(osm=rid, name=r.get('tags', {}).get('name', ''), km=km, points=simplify(pts)))
        if len(picked) >= 3:
            break
    index[mid] = dict(name=name, routes=len(picked), kms=[p['km'] for p in picked])
    if picked:
        (OUTDIR / f'{mid}.json').write_text(json.dumps(dict(
            mountain=base, attribution='© OpenStreetMap contributors (ODbL)',
            routes=picked), ensure_ascii=False), encoding='utf-8')
    print(f'{mid:14s} {name:8s} rels={len(rels):3d} picked={len(picked)} {[p["km"] for p in picked]}', flush=True)

(ROOT / 'assets/data/tracks/index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')
print('DONE')
