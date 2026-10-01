# -*- coding: utf-8 -*-
"""한국 100대 명산 5차(4산) 사진 수집 — Unsplash API → 28파일/산 변환.

규격 (기존 산과 동일):
- hero-{640,1024,1600,2400}.{jpg,webp,avif}  : 가로세로 2.5641:1 (1600x624 기준) 센터 크롭
- g1..g4.{jpg,webp,avif}                     : 3:2 1600x1067
- g1-640.{jpg,webp,avif}                     : 3:2 640x427
- og.png                                     : 1200x630

사용 중인 사진 ID(CREDITS.md + 전체 HTML에서 추출 /tmp/used_all.txt)는 제외.
"""
import json, os, pathlib, sys, urllib.parse, urllib.request
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEY = json.load(open(ROOT / '_orchestration/config.json'))['UNSPLASH_ACCESS_KEY']
USED = set(open('/tmp/used_all.txt').read().split())

MOUNTAINS = {
    'namsan':     ['korean pagoda mountains', 'gyeongju korea', 'buddha statue korea mountain'],
    'gyebangsan': ['korea mountain peaks', 'korea winter mountain', 'korea hiking trail mountain'],
    'dutasan':    ['korea mountain cliff', 'rocky mountain valley stream', 'korea forest mountain stream'],
    'manisan':    ['korea island sea', 'korea coastal mountain', 'sea and mountain korea'],
}
FALLBACK = ['korea mountain', 'korea nature mountains']

def api(path, **params):
    url = 'https://api.unsplash.com/' + path + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'Authorization': f'Client-ID {KEY}'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)

def search(q, pages=2):
    out = []
    for p in range(1, pages + 1):
        try:
            d = api('search/photos', query=q, per_page=15, orientation='landscape', page=p)
        except Exception as e:
            print(f'  search "{q}" p{p} FAIL: {e}')
            break
        out += d.get('results', [])
        if len(d.get('results', [])) < 15:
            break
    return out

def pick(queries, need=5):
    """used 제외, 중복 없이 need개 선택."""
    chosen, seen = [], set()
    for q in queries:
        for p in search(q):
            if len(chosen) >= need:
                return chosen
            if p['id'] in USED or p['id'] in seen:
                continue
            if p['width'] < 2400:
                continue
            seen.add(p['id'])
            chosen.append(p)
    return chosen

def download(photo, dest):
    url = photo['urls']['raw'] + '&w=2400&q=85&fm=jpg&fit=max'
    req = urllib.request.Request(url, headers={'User-Agent': 'mttrails-build/1.0'})
    with urllib.request.urlopen(req, timeout=90) as r, open(dest, 'wb') as f:
        f.write(r.read())

def crop_save(im, aspect, w, h, stem, exts, q_jpg=82, q_webp=80, q_avif=62):
    """센터(약간 상단) 크롭 후 지정 크기로 3형식 저장."""
    src = im
    if src.mode in ('RGBA', 'P'):
        src = src.convert('RGB')
    sw, sh = src.size
    if sw / sh > aspect:            # 소스가 더 넓다 → 가로 크롭
        cw, ch = int(sh * aspect), sh
        box = ((sw - cw) // 2, (sh - ch) // 2)
    else:                            # 소스가 더 높다 → 세로 크롭, 상단 40% 지점
        cw, ch = sw, int(sw / aspect)
        box = (0, min(int((sh - ch) * 0.40), sh - ch))
    crop = src.crop((box[0], box[1], box[0] + cw, box[1] + ch)).resize((w, h), Image.LANCZOS)
    crop.save(stem + '.jpg', 'JPEG', quality=q_jpg, optimize=True, progressive=True)
    crop.save(stem + '.webp', 'WEBP', quality=q_webp, method=6)
    crop.save(stem + '.avif', 'AVIF', quality=q_avif)

def build_files(mid, photo, tmp):
    im = Image.open(tmp)
    outd = ROOT / 'assets/img' / mid
    outd.mkdir(parents=True, exist_ok=True)
    HERO = 2400 / 936          # 2.5641
    # hero 4사이즈
    hero = im
    if hero.mode in ('RGBA', 'P'):
        hero = hero.convert('RGB')
    sw, sh = hero.size
    if sw / sh > HERO:
        cw, ch = int(sh * HERO), sh
        box = ((sw - cw) // 2, (sh - ch) // 2)
    else:
        cw, ch = sw, int(sw / HERO)
        box = (0, min(int((sh - ch) * 0.40), sh - ch))
    crop = hero.crop((box[0], box[1], box[0] + cw, box[1] + ch))
    for w in (2400, 1600, 1024, 640):
        h = round(w / HERO)
        r = crop.resize((w, h), Image.LANCZOS)
        r.save(outd / f'hero-{w}.jpg', 'JPEG', quality=82, optimize=True, progressive=True)
        r.save(outd / f'hero-{w}.webp', 'WEBP', quality=80, method=6)
        r.save(outd / f'hero-{w}.avif', 'AVIF', quality=62)
    # og.png 1200x630 (히어로와 같은 크롭에서 리사이즈)
    og = crop.resize((1200, 630), Image.LANCZOS)
    og.save(outd / 'og.png', 'PNG', optimize=True)
    print(f'  {mid}: hero x12 + og.png')

def build_gallery(mid, photo, idx, tmp):
    im = Image.open(tmp)
    outd = ROOT / 'assets/img' / mid
    g = f'g{idx}'
    crop_save(im, 3 / 2, 1600, 1067, str(outd / g), None)
    if idx == 1:
        crop_save(im, 3 / 2, 640, 427, str(outd / 'g1-640'), None)
    print(f'  {mid}: {g} (x3)')

def main():
    tmp = ROOT / 'scratch/_tmp_photo.jpg'
    credits = {}
    for mid, queries in MOUNTAINS.items():
        print(f'== {mid} ==')
        photos = pick(queries, need=5)
        if len(photos) < 5:
            photos += [p for p in pick(FALLBACK, need=10) if p['id'] not in {x['id'] for x in photos}]
        photos = photos[:5]
        assert len(photos) == 5, f'{mid}: 사진 5장 미달 ({len(photos)})'
        c = {'hero': {}, 'gallery': {}}
        for i, p in enumerate(photos):
            download(p, tmp)
            if i == 0:
                build_files(mid, p, tmp)
                c['hero'] = {'photographer': p['user']['name'], 'url': p['links']['html']}
            else:
                build_gallery(mid, p, i, tmp)
                c['gallery'][f'g{i}'] = {'photographer': p['user']['name'], 'url': p['links']['html']}
            USED.add(p['id'])
        credits[mid] = c
        print(f'  {mid}: done — hero {credits[mid]["hero"]}')
    out = ROOT / 'scratch/k100v5_credits.json'
    json.dump([{k: v} for k, v in credits.items()], open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tmp.unlink(missing_ok=True)
    print('credits →', out)

if __name__ == '__main__':
    main()
