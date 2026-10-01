# -*- coding: utf-8 -*-
"""5차 사진 재선정 — manisan(hero,g2)·dutasan(g1,g2,g3) 교체."""
import json, pathlib, sys
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fetch_photos_v5 import ROOT, USED, api, download, build_files, build_gallery, crop_save

USED |= set(json.load(open(ROOT / 'scratch/k100v5_credits.json')) and
            {p['url'].split('-')[-1] for c in json.load(open(ROOT / 'scratch/k100v5_credits.json')) for v in c.values() for p in [v['hero'], *v['gallery'].values()]})

REPL = {
    'manisan': {
        'hero': ['korea mountain trail view', 'green mountains korea fog', 'mountain summit korea'],
        'g2': ['korea mountain forest path', 'hiking korea mountain', 'korea countryside mountain'],
    },
    'dutasan': {
        'g1': ['mountain valley korea stream', 'rocky cliffs forest', 'mountain rock formations'],
        'g2': ['steep mountain cliff', 'mountain gorge rocks', 'mountain ridge hiking'],
        'g3': ['mountain stream forest', 'valley waterfall rocks', 'granite mountain rocks'],
    },
}

def search(q):
    try:
        d = api('search/photos', query=q, per_page=15, orientation='landscape')
        return d.get('results', [])
    except Exception as e:
        print(f'  search "{q}" FAIL: {e}')
        return []

tmp = ROOT / 'scratch/_tmp_photo.jpg'
credits = json.load(open(ROOT / 'scratch/k100v5_credits.json'))
cmap = {list(c.keys())[0]: list(c.values())[0] for c in credits}
tmp_dl = ROOT / 'scratch/_tmp_photo2.jpg'

for mid, slots in REPL.items():
    need_ids = list(slots.keys())
    pool = []
    for q in [x for v in slots.values() for x in v]:
        for p in search(q):
            if p['id'] in USED or p['width'] < 2400 or p in pool:
                continue
            pool.append(p)
    print(f'== {mid}: pool {len(pool)}')
    pi = 0
    for slot in need_ids:
        chosen = None
        while pi < len(pool):
            p = pool[pi]; pi += 1
            try:
                download(p, tmp_dl)
            except Exception as e:
                print('  dl fail', e); continue
            chosen = p
            break
        assert chosen, f'{mid}/{slot}: 교체 사진 없음'
        USED.add(chosen['id'])
        entry = {'photographer': chosen['user']['name'], 'url': chosen['links']['html']}
        if slot == 'hero':
            build_files(mid, chosen, tmp_dl)
            cmap[mid]['hero'] = entry
        else:
            build_gallery(mid, chosen, int(slot[1]), tmp_dl)
            cmap[mid]['gallery'][slot] = entry
        print(f'  {mid}/{slot} ← {entry["photographer"]} {entry["url"].split("/")[-1][:55]}')

tmp_dl.unlink(missing_ok=True); tmp.unlink(missing_ok=True)
json.dump([{k: v} for k, v in cmap.items()], open(ROOT / 'scratch/k100v5_credits.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('credits updated')
