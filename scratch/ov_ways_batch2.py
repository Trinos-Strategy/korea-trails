import json, sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import ov_ways_fetch as F
boxes = json.load(open('/tmp/fetch_boxes.json', encoding='utf-8'))
todo = ['achasan', 'inwangsan', 'dobongsan', 'jirisan', 'seoraksan']
for mid in todo:
    a1, o1, a2, o2 = boxes[mid]['bbox']
    acc = F.fetch_bbox(a1, o1, a2, o2)
    ways = list(acc.values())
    (F.OUT / f'{mid}.json').write_text(json.dumps(dict(mid=mid, ways=ways), ensure_ascii=False), encoding='utf-8')
    print(f"{mid}: {len(ways)} ways (named {sum(1 for w in ways if w['name'])})", flush=True)
    time.sleep(2)
print('DONE2', flush=True)
