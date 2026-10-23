# -*- coding: utf-8 -*-
"""산별 등산로 way 일괄 수집 (bbox는 /tmp/fetch_boxes.json)."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from ov_ways_fetch import fetch_bbox, OUT

boxes = json.load(open('/tmp/fetch_boxes.json', encoding='utf-8'))
for mid, b in boxes.items():
    a1, o1, a2, o2 = b['bbox']
    acc = fetch_bbox(a1, o1, a2, o2)
    ways = list(acc.values())
    (OUT / f'{mid}.json').write_text(json.dumps(dict(mid=mid, ways=ways), ensure_ascii=False), encoding='utf-8')
    print(f"{mid}: {len(ways)} ways (named {sum(1 for w in ways if w['name'])})", flush=True)
print('ALL FETCHED', flush=True)
