# -*- coding: utf-8 -*-
"""Path 조립 1단계 — 산별 등산로 way 수집 (mail.ru 200건 제한: bbox 사분할 재귀 우회).

수집 대상: highway=path|footway|steps|track (등산로 후보), out geom.
출력: scratch/ways/<mid>.json  {ways:[{id,name,highway,pts:[[lat,lng],...]}]}
"""
import json, subprocess, time, pathlib, sys

EP = 'https://maps.mail.ru/osm/tools/overpass/api/interpreter'
UA = 'MTTrailsBot/1.0 (contact: dkkim@swonlaw.com)'
OUT = pathlib.Path('/Users/mac/korea-trails/scratch/ways')
OUT.mkdir(exist_ok=True)
HW = '^(path|footway|steps|track)$'


def overpass(q, t=240):
    for _ in range(3):
        r = subprocess.run(['curl', '-s', '--max-time', str(t), '-A', UA, '--data', q, EP],
                           capture_output=True, text=False)
        try:
            return json.loads(r.stdout.decode('utf-8', errors='replace'))
        except Exception:
            time.sleep(4)
    return None


def fetch_bbox(lat1, lng1, lat2, lng2, depth=0, acc=None):
    """bbox 내 등산로 way 수집. 200건 도달 시 4분할."""
    if acc is None:
        acc = {}
    q = (f'[out:json][timeout:120];way["highway"~"{HW}"]'
         f'({lat1:.5f},{lng1:.5f},{lat2:.5f},{lng2:.5f});out geom;')
    j = overpass(q)
    els = (j or {}).get('elements', [])
    if len(els) >= 190 and depth < 3:
        mlat, mlng = (lat1 + lat2) / 2, (lng1 + lng2) / 2
        for (a1, o1, a2, o2) in [(lat1, lng1, mlat, mlng), (lat1, mlng, mlat, lng2),
                                 (mlat, lng1, lat2, mlng), (mlat, mlng, lat2, lng2)]:
            fetch_bbox(a1, o1, a2, o2, depth + 1, acc)
        return acc
    for e in els:
        acc[e['id']] = dict(id=e['id'], name=e.get('tags', {}).get('name', ''),
                            highway=e.get('tags', {}).get('highway', 'path'),
                            pts=[[g['lat'], g['lon']] for g in e.get('geometry', []) if 'lat' in g])
    return acc


def main(mid, lat, lng, radius_km=4.0):
    d = radius_km / 111.0
    acc = fetch_bbox(lat - d, lng - d * 1.35, lat + d, lng + d * 1.35)
    ways = list(acc.values())
    (OUT / f'{mid}.json').write_text(json.dumps(dict(mid=mid, ways=ways), ensure_ascii=False), encoding='utf-8')
    named = sum(1 for w in ways if w['name'])
    print(f'{mid}: {len(ways)} ways (named {named})', flush=True)


if __name__ == '__main__':
    mid, lat, lng = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    main(mid, lat, lng)
