# -*- coding: utf-8 -*-
"""위키미디어 커먼즈 실산 사진 수집 — 우선순위 높음 6산 (staging only)."""
import json, pathlib, re, subprocess, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'scratch' / 'commons'
API = 'https://commons.wikimedia.org/w/api.php'
UA = 'MTTrailsCurator/1.0 (hiking site photo research)'
TARGETS = {
    'gwanaksan': 'Category:Gwanaksan',
    'suraksan': 'Category:Suraksan',
    'geumjeongsan': 'Category:Geumjeongsan',
    'songnisan': 'Category:Songnisan',
    'daedunsan': 'Category:Daedunsan',
    'inwangsan': 'Category:Inwangsan',
}
LICENSES_OK = re.compile(r'^(cc by(?!-nc)[ -]*(2\.0|3\.0|4\.0)|cc by-sa[ -]*(2\.0|3\.0|4\.0)|cc0|public domain)', re.I)
MIN_W = 2000


def api(params):
    params = {**params, 'format': 'json'}
    url = API + '?' + urllib.parse.urlencode(params)
    import time as _t
    for attempt in range(5):
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                d = json.load(r)
            _t.sleep(1.2)
            return d
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 4:
                wait = 30 * (attempt + 1)
                print(f'   429 — {wait}s 대기 후 재시도')
                _t.sleep(wait)
                continue
            raise


def strip_html(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s or '')).strip()


def category_files(cat):
    out, cont = [], None
    for _ in range(3):
        params = {'action': 'query', 'list': 'categorymembers', 'cmtitle': cat, 'cmlimit': 'max', 'cmtype': 'file'}
        if cont:
            params.update(cont)
        d = api(params)
        out += [m['title'] for m in d.get('query', {}).get('categorymembers', [])]
        cont = d.get('continue')
        if not cont:
            break
    return out


def subcategories(cat):
    d = api({'action': 'query', 'list': 'categorymembers', 'cmtitle': cat, 'cmlimit': 'max', 'cmtype': 'subcat'})
    return [m['title'] for m in d.get('query', {}).get('categorymembers', [])]


def imageinfo_batch(titles):
    """최대 50건 일괄 조회 → {title: imageinfo}. 호출 수를 1/50로 줄인다."""
    out = {}
    for i in range(0, len(titles), 50):
        d = api({'action': 'query', 'titles': '|'.join(titles[i:i + 50]), 'prop': 'imageinfo',
                 'iiprop': 'url|size|extmetadata'})
        for p in d.get('query', {}).get('pages', {}).values():
            ii = p.get('imageinfo', [])
            if ii:
                out[p['title']] = ii[0]
    return out


BAD_TITLE = re.compile(r'행사|등산대회|지신|제막|기념|촬영|대회|훈련|교육|사진전|스포츠|클라이밍|레이스|캠페인|봉사|모임|회의', re.I)


def imageinfo(title):
    d = api({'action': 'query', 'titles': title, 'prop': 'imageinfo',
             'iiprop': 'url|size|extmetadata'})
    pages = d.get('query', {}).get('pages', {})
    for p in pages.values():
        ii = p.get('imageinfo', [])
        if ii:
            return ii[0]
    return None


manifest = json.load(open(OUT / 'manifest.json', encoding='utf-8')) if (OUT / 'manifest.json').exists() else []
DONE = {e['mid'] for e in manifest}
manifest = [e for e in manifest if e['mid'] in TARGETS]
for mid, cat in TARGETS.items():
    if mid in DONE:
        print(f'== {mid}: 이미 {sum(1 for e in manifest if e["mid"]==mid)}장 확보 — 스킵', flush=True)
        continue
    (OUT / mid).mkdir(parents=True, exist_ok=True)
    # 파일 후보: 직속 + 하위 카테고리 1depth, imageinfo 검사는 70건 상한
    titles = category_files(cat)
    for sub in subcategories(cat):
        titles += category_files(sub)
    titles = [t for t in titles if re.search(r'\.(jpe?g|png)$', t, re.I)]
    print(f'== {mid} ({cat}): 후보 {len(titles)}', flush=True)
    got, n = 0, 0
    titles = [t for t in titles[:150] if not BAD_TITLE.search(t)]
    infos = imageinfo_batch(titles[:150])
    print(f'   일괄 조회: {len(infos)}건', flush=True)
    for t in titles[:150]:
        if got >= 5:
            break
        ii = infos.get(t)
        if ii is None:
            continue
        if not ii or ii.get('width', 0) < MIN_W:
            continue
        em = ii.get('extmetadata', {})
        lic = strip_html(em.get('LicenseShortName', {}).get('value', ''))
        artist = strip_html(em.get('Artist', {}).get('value', ''))
        if not LICENSES_OK.match(lic) or not artist:
            continue
        n += 1
        ext = '.jpg' if re.search(r'\.jpe?g$', t, re.I) else '.png'
        dest = OUT / mid / f'original-{n}{ext}'
        r = subprocess.run(['curl', '-sL', '-A', UA, '-o', str(dest), ii['url']])
        if r.returncode != 0 or not dest.exists() or dest.stat().st_size < 100_000:
            dest.unlink(missing_ok=True)
            continue
        manifest.append(dict(mid=mid, slot='hero' if got == 0 else f'g{got}', file_title=t,
                             page_url=ii.get('descriptionurl', ''), file_url=ii['url'],
                             downloaded=str(dest.relative_to(ROOT)), author=artist, license=lic,
                             width=ii['width'], height=ii['height'],
                             subject_check=f'{cat} category member'))
        got += 1
        print(f'   [{got}/5] {t[:60]} | {lic} | {ii["width"]}x{ii["height"]} | {artist[:30]}', flush=True)
    if got < 5:
        print(f'   !! {mid}: {got}/5 확보 (기준 미달 통과분만)')

json.dump(manifest, open(OUT / 'manifest.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'manifest: {len(manifest)} entries → {OUT}/manifest.json')
