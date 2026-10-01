# -*- coding: utf-8 -*-
"""Q4 이미지 경량화 — og.png→og.jpg 변환 + hero-2400 재인코딩(>700KB)."""
import glob, os, pathlib, re, subprocess
from PIL import Image

ROOT = pathlib.Path('.').resolve()

# 1) og.png → og.jpg (사진은 JPEG가 원칙)
converted = []
for f in sorted(glob.glob('assets/img/*/og.png')):
    size = os.path.getsize(f)
    if size <= 200_000:  # 이미 작으면 유지
        continue
    im = Image.open(f).convert('RGB')
    jpg = f[:-4] + '.jpg'
    im.save(jpg, 'JPEG', quality=85, optimize=True, progressive=True)
    new = os.path.getsize(jpg)
    if new < size * 0.55:
        os.remove(f)
        converted.append((size // 1024, new // 1024, jpg))
    else:
        os.remove(jpg)
print(f'og 변환: {len(converted)}개')
for old, new, f in converted[:6]:
    print(f'  {f}: {old}KB → {new}KB')

# 2) hero-2400 >700KB 재인코딩 (원본 백업은 git이 담당)
reenc = []
for f in sorted(glob.glob('assets/img/*/hero-2400.jpg')):
    if os.path.getsize(f) <= 700_000:
        continue
    im = Image.open(f)
    im.save(f + '.tmp', 'JPEG', quality=76, optimize=True, progressive=True)
    old, new = os.path.getsize(f), os.path.getsize(f + '.tmp')
    if new < old * 0.6:
        os.replace(f + '.tmp', f)
        reenc.append((old // 1024, new // 1024, f))
    else:
        os.remove(f + '.tmp')
print(f'hero 재인코딩: {len(reenc)}개')
for old, new, f in reenc:
    print(f'  {f}: {old}KB → {new}KB')

# 3) HTML 참조 교체 — 변환된 산만 (og.jpg가 실재하는 경우에만)
n_refs = 0
pages_fixed = set()
converted_mids = {f.split('/')[-2] for _, _, f in converted}
pages = list(pathlib.Path('.').glob('*.html')) + list(pathlib.Path('en').glob('*.html'))
for p in pages:
    s = p.read_text(encoding='utf-8')
    orig = s
    for mid in converted_mids:
        s = s.replace(f'img/{mid}/og.png', f'img/{mid}/og.jpg')
    if s != orig:
        n_refs += orig.count('og.png') - s.count('og.png')
        p.write_text(s, encoding='utf-8')
        pages_fixed.add(str(p))
print(f'og 참조 교체: {n_refs}곳 / {len(pages_fixed)}페이지')
