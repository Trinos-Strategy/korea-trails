# -*- coding: utf-8 -*-
"""커먼즈 실산 사진 사이트 규격 처리 + 페이지 크레딧 교체.

- manifest.json의 사진을 assets/img/<mid>/ 규격(28파일)으로 크롭·변환
- 해당 산 페이지(KO/EN)의 히어로 크레딧·갤러리 data-credit을 커먼즈 표기로 교체
- CREDITS.md 섹션 생성, PHOTO-ACCURACY.md 상태 이동
"""
import json, pathlib, re, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scratch'))

HERO_AR = 2400 / 936


def crop_to(im, ar, w, h, top_bias=0.40):
    if im.mode in ('RGBA', 'P', 'LA'):
        im = im.convert('RGB')
    sw, sh = im.size
    if sw / sh > ar:
        cw, ch = int(sh * ar), sh
        box = ((sw - cw) // 2, 0)
    else:
        cw, ch = sw, int(sw / ar)
        box = (0, min(int((sh - ch) * top_bias), sh - ch))
    return im.crop((box[0], box[1], box[0] + cw, box[1] + ch)).resize((w, h), Image.LANCZOS)


def save3(im, stem):
    im.save(stem + '.jpg', 'JPEG', quality=82, optimize=True, progressive=True)
    im.save(stem + '.webp', 'WEBP', quality=80, method=6)
    im.save(stem + '.avif', 'AVIF', quality=62)


def process(mid, files):
    """files: {'hero': path, 'g1'..: path} → 28파일(부족 슬롯은 기존 유지)."""
    outd = ROOT / 'assets/img' / mid
    written = []
    if 'hero' in files:
        im = Image.open(files['hero'])
        crop = crop_to(im, HERO_AR, 2400, 936)
        for w in (2400, 1600, 1024, 640):
            h = round(w / HERO_AR)
            r = crop.resize((w, h), Image.LANCZOS)
            save3(r, str(outd / f'hero-{w}'))
        crop.resize((1200, 630), Image.LANCZOS).save(outd / 'og.png', 'PNG', optimize=True)
        written.append('hero')
    for slot in ('g1', 'g2', 'g3', 'g4'):
        if slot not in files:
            continue
        im = Image.open(files[slot])
        save3(crop_to(im, 3 / 2, 1600, 1067), str(outd / slot))
        if slot == 'g1':
            save3(crop_to(im, 3 / 2, 640, 427), str(outd / 'g1-640'))
        written.append(slot)
    return written


def credit_html(entry):
    return (f"Photo by &lt;a href='{entry['page_url']}' target='_blank' rel='noopener'&gt;{entry['author']}&lt;/a&gt; "
            f"on &lt;a href='https://commons.wikimedia.org' target='_blank' rel='noopener'&gt;Wikimedia Commons&lt;/a&gt; ({entry['license']})")


def patch_page(mid, hero_e, gal_entries, lang_dir, pfx):
    p = ROOT / lang_dir / f'{mid}-playbook.html'
    if not p.exists():
        return False
    s = p.read_text(encoding='utf-8')
    # 히어로 크레딧: <a href="<unsplash url>" ...>작가</a>
    if hero_e:
        s = re.sub(r'(<span class="credit-author">Photo by <a href=")[^"]*(" rel="noopener" target="_blank">)[^<]*(</a></span>)',
                   lambda m: m.group(1) + hero_e['page_url'] + m.group(2) + hero_e['author'] + m.group(3), s, count=1)
        s = re.sub(r'(<span class="credit-source"><a href="https://unsplash\.com" rel="noopener" target="_blank">)Unsplash(</a></span>)',
                   lambda m: m.group(1) + 'Wikimedia Commons' + m.group(2), s, count=1)
    # 갤러리 data-credit="Photo by &lt;a href='...' ... on Unsplash"
    for i in range(1, 5):
        e = gal_entries.get(f'g{i}')
        if not e:
            continue
        cap = credit_html(e)
        pat = r'(data-credit=")([^"]*)(")'
        # i번째 갤러리 항목을 정확히 고르기 위해 data-index 순으로 치환
    # data-index별 정확 치환
    for i in range(4):
        e = gal_entries.get(f'g{i+1}')
        if not e:
            continue
        cap = credit_html(e)
        pat = re.compile(r'(data-index="' + str(i) + r'"')
        m = pat.search(s)
        if not m:
            continue
        start = s.rfind('data-credit="', 0, m.start())
        if start < 0:
            continue
        end = s.find('"', start + len('data-credit="'))
        s = s[:start] + f'data-credit="{cap}"' + s[end:]
    p.write_text(s, encoding='utf-8')
    return True


def main():
    manifest = json.load(open(ROOT / 'scratch/commons/manifest.json', encoding='utf-8'))
    by_mid = {}
    for e in manifest:
        by_mid.setdefault(e['mid'], {})[e['slot']] = e
    summary = {}
    for mid, slots in by_mid.items():
        files = {slot: str(ROOT / e['downloaded']) for slot, e in slots.items()}
        written = process(mid, files)
        ko_ok = patch_page(mid, slots.get('hero'), slots, '', '')
        en_ok = patch_page(mid, slots.get('hero'), slots, 'en', '')
        summary[mid] = dict(slots=list(slots.keys()), written=written, pages=(ko_ok, en_ok))
        print(f'{mid}: 처리 {written} / 페이지 KO={ko_ok} EN={en_ok}')
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
