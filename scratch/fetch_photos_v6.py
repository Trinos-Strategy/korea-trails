# -*- coding: utf-8 -*-
"""한국 100대 명산 6차(4산) Unsplash 사진 수집 — fetch_photos_v5 규격 재사용."""
import json, pathlib, re, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fetch_photos_v5 import ROOT, api, download, build_files, build_gallery

MOUNTAINS = {
    'daeamsan': ['korea highland moor', 'mountain wetland bog', 'korea misty ridge'],
    'baegunsan': ['korea azalea mountain', 'korea spring flowers hillside', 'korea flowers ridge hiking'],
    'sinbulsan': ['korea grass ridge mountain', 'korea mountain meadow trail', 'korea silver grass ridge'],
    'gamaksan': ['korean temple mountain valley', 'korea valley stream forest', 'korea temple autumn mountain'],
}
FALLBACK = ['korea mountain', 'korea nature mountains']

# 사용 중 ID: 전체 HTML + CREDITS + v5/v6 크레딧
used = set(subprocess.run(
    ['bash', '-c',
     "grep -rhoE 'unsplash\\.com/photos/[a-zA-Z0-9_-]{11}' *.html en/*.html CREDITS.md | sed 's|.*/||' | sort -u"],
    capture_output=True, text=True, cwd=ROOT).stdout.split())
for cj in ('k100v5_credits.json', 'k100v6_credits.json'):
    f = ROOT / 'scratch' / cj
    if f.exists():
        for c in json.load(open(f)):
            for v in c.values():
                for p in [v['hero'], *v['gallery'].values()]:
                    used.add(p['url'].rstrip('/').split('-')[-1])


def pick(queries, need=5):
    chosen, seen = [], set()
    for q in list(queries) + FALLBACK:
        try:
            d = api('search/photos', query=q, per_page=15, orientation='landscape')
        except Exception as e:
            print(f'  search "{q}" FAIL: {e}')
            continue
        for p in d.get('results', []):
            if len(chosen) >= need:
                return chosen
            if p['id'] in used or p['id'] in seen or p['width'] < 2400:
                continue
            seen.add(p['id'])
            chosen.append(p)
    return chosen


tmp = ROOT / 'scratch/_tmp_v6.jpg'
credits = []
for mid, queries in MOUNTAINS.items():
    print(f'== {mid} ==')
    photos = pick(queries, 5)
    assert len(photos) == 5, f'{mid}: 5장 미달({len(photos)})'
    c = {'hero': {}, 'gallery': {}}
    for i, p in enumerate(photos):
        download(p, tmp)
        if i == 0:
            build_files(mid, p, tmp)
            c['hero'] = {'photographer': p['user']['name'], 'url': p['links']['html']}
        else:
            build_gallery(mid, p, i, tmp)
            c['gallery'][f'g{i}'] = {'photographer': p['user']['name'], 'url': p['links']['html']}
        used.add(p['id'])
        print(f'  {"hero" if i==0 else f"g{i}"}: {p["user"]["name"]} | {(p.get("alt_description") or "")[:55]}')
    credits.append({mid: c})

json.dump(credits, open(ROOT / 'scratch/k100v6_credits.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tmp.unlink(missing_ok=True)

# 검수용 프리뷰 시트
from PIL import Image
for entry in credits:
    mid = list(entry.keys())[0]
    tiles = [Image.open(ROOT / f'assets/img/{mid}/hero-640.jpg').resize((480, 187))] + \
            [Image.open(ROOT / f'assets/img/{mid}/g{i}-640.jpg').resize((480, 320)) for i in range(1, 5)]
    sheet = Image.new('RGB', (960, 187 + 320 * 2 + 20), 'white')
    sheet.paste(tiles[0], (0, 0))
    sheet.paste(tiles[1], (480, 0))
    for k in range(2, 5):
        sheet.paste(tiles[k], (((k - 1) % 2) * 480, 187 + ((k - 1) // 2) * 320))
    sheet.save(ROOT / f'scratch/v6_preview_{mid}.jpg', quality=82)
    print(f'preview → scratch/v6_preview_{mid}.jpg')
print('done')
