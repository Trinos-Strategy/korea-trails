# -*- coding: utf-8 -*-
"""Path 조립 — OSM way 그래프에서 기점→정점 경로 조립 (다익스트라).

사용: python3 scratch/assemble_tracks.py <mid>   (scratch/ways/<mid>.json 필요)
검증 게이트: ①기점·종점 노드 도달(260m/380m) ②조립 km vs 알레 실측 ±28% ③km 1~45
"""
import heapq, json, math, pathlib, re, sys

ROOT = pathlib.Path('/Users/mac/korea-trails')
WAYS = ROOT / 'scratch/ways'
TD = ROOT / 'assets/data/tracks'
PEN = {'path': 1.0, 'footway': 1.05, 'steps': 1.3, 'track': 1.45}


def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    x = math.cos(la1) * math.cos(la2) * (math.cos(lo2) - math.cos(lo1))
    y = math.cos(la1) * math.sin(lo2) - math.cos(la2) * math.sin(lo1)
    z = math.sin(la2) - math.sin(la1)
    return 6371000.0 * 2 * math.asin(math.sqrt(x * x + y * y + z * z))


def build_graph(ways, tokens):
    adj, coord = {}, {}
    for w in ways:
        hw = w.get('highway') if w.get('highway') in PEN else 'path'
        pen = PEN[hw]
        nm = w.get('name', '')
        if nm:
            pen *= 0.92
            if any(t in nm for t in tokens):
                pen *= 0.55
        pts = w['pts']
        for i in range(len(pts)):
            k = (round(pts[i][0], 6), round(pts[i][1], 6))
            coord.setdefault(k, pts[i])
            if i:
                pk = (round(pts[i - 1][0], 6), round(pts[i - 1][1], 6))
                d = hav(pts[i - 1], pts[i])
                if d > 0:
                    wt = d * pen
                    adj.setdefault(pk, []).append((k, wt))
                    adj.setdefault(k, []).append((pk, wt))
    return adj, coord


def nearest_node(coord, latlng, limit_m):
    best, bd = None, 1e18
    for k, c in coord.items():
        d = hav(c, latlng)
        if d < bd:
            best, bd = k, d
    return (best, bd) if bd <= limit_m else (None, bd)


def component_sizes(adj, coord):
    label, sizes, cid = {}, {}, 0
    seen = set()
    for k in coord:
        if k in seen:
            continue
        stack, n = [k], 0
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            label[u] = cid
            n += 1
            stack.extend(v for v, _ in adj.get(u, []))
        sizes[cid] = n
        cid += 1
    return label, sizes


def nearest_big_node(coord, label, sizes, latlng, limit_m, min_comp=300):
    """작은 고립 조각(노이즈)을 피해 유의미한 컴포넌트의 최근접 노드."""
    best, bd = None, 1e18
    for k, c in coord.items():
        if sizes.get(label.get(k), 0) < min_comp:
            continue
        d = hav(c, latlng)
        if d < bd:
            best, bd = k, d
    return (best, bd) if bd <= limit_m else (None, bd)


def dijkstra(adj, src, dst, coord):
    dist = {src: 0.0}
    prev = {}
    pq = [(0.0, src)]
    seen = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        if u == dst:
            break
        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist.get(v, 1e18):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    if dst not in seen:
        return None, None
    path, u = [dst], dst
    while u != src:
        u = prev[u]
        path.append(u)
    path.reverse()
    km = sum(hav(coord[path[i]], coord[path[i + 1]]) for i in range(len(path) - 1)) / 1000.0
    return path, km


def assemble(ways, start, end, tokens, alle_km):
    adj, coord = build_graph(ways, tokens)
    label, sizes = component_sizes(adj, coord)
    sn, sd = nearest_big_node(coord, label, sizes, start, 2500.0)
    en, ed = nearest_big_node(coord, label, sizes, end, 2500.0)
    if not sn or not en:
        return None, f'노드 미도달 start={sd:.0f}m end={ed:.0f}m'
    if label[sn] != label[en]:
        return None, f'기점-종점 단절 (comp {label[sn]} vs {label[en]}, 크기 {sizes[label[sn]]}/{sizes[label[en]]})'
    path, km = dijkstra(adj, sn, en, coord)
    if not path:
        return None, '경로 없음'
    if not (1.0 <= km <= 45.0):
        return None, f'km 범위 이탈 {km:.1f}'
    if alle_km and abs(km - alle_km) / alle_km > 0.28:
        return None, f'실측 대조 실패 {km:.1f}km vs {alle_km}km'
    pts = [coord[k] for k in path]
    if len(pts) > 300:
        step = math.ceil(len(pts) / 300)
        pts = pts[::step]
    return dict(points=pts, km=round(km, 1), raw_n=len(path)), 'OK'


def main(mid):
    s = (ROOT / 'index.html').read_text(encoding='utf-8')
    m = re.search(r"\{id:'" + mid + r"',\s*name:'([^']+)'[^}]*?lat:\s*([-\d.]+),\s*lng:\s*([-\d.]+)", s)
    mname, summit = m.group(1), [float(m.group(2)), float(m.group(3))]
    ways = json.loads((WAYS / f'{mid}.json').read_text(encoding='utf-8'))['ways']
    alle = json.loads((ROOT / 'scratch/alle_data.json').read_text(encoding='utf-8'))
    routes = []
    for cseq, c in sorted(alle['courses'].items(), key=lambda kv: int(kv[0])):
        if c['mountain'] != mname:
            continue
        pts = c.get('coords') or []
        if not pts:
            print(f'  {c["name"]}: 기점 GPS 없음 — skip', flush=True)
            continue
        start = [pts[0]['lat'], pts[0]['lng']]
        # 종점: 알레 코스 종점 GPS (기점과 800m 이상 떨어져 있을 때), 아니면 정점
        end = [pts[-1]['lat'], pts[-1]['lng']]
        if hav(start, end) < 800.0:
            end = summit
        km_alle = float(re.match(r'([\d.]+)', c['km']).group(1)) if re.match(r'([\d.]+)', c['km']) else None
        tokens = [t for t in re.split(r'[-–\s·]+', c['name'].replace(' 코스', '')) if len(t) >= 2]
        r, msg = assemble(ways, start, end, tokens, km_alle)
        status = f'PASS {r["km"]}km (n={r["raw_n"]})' if r else f'FAIL {msg}'
        print(f'  {c["name"]}: {status} (알레 {km_alle}km)', flush=True)
        if r:
            routes.append(dict(osm='assembled', name=c['name'], km=r['km'], points=r['points']))
    if routes:
        f = TD / f'{mid}.json'
        if f.exists():
            old = json.loads(f.read_text(encoding='utf-8'))
            names = {r['name'] for r in old['routes']}
            routes = old['routes'] + [r for r in routes if r['name'] not in names]
        (TD / f'{mid}.json').write_text(json.dumps(dict(
            mountain=mname, attribution='© OpenStreetMap contributors (ODbL)',
            routes=routes[:3]), ensure_ascii=False), encoding='utf-8')
        print(f'WROTE {mid}: {[r["name"] for r in routes[:3]]}', flush=True)
    else:
        print(f'NO ROUTES for {mid}', flush=True)


if __name__ == '__main__':
    main(sys.argv[1])
