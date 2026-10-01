# -*- coding: utf-8 -*-
"""워커 A — Wikidata 표고(P2044) 71산 수집 → scratch/wd_elev.json."""
import json, subprocess, time, urllib.parse, re, pathlib

ROOT = pathlib.Path('/Users/mac/korea-trails')
OUT = ROOT / 'scratch/wd_elev.json'
UA = 'MTTrailsBot/1.0 (contact: dkkim@swonlaw.com)'

PAGE = json.loads((ROOT / 'scratch/coords_verify.json').read_text(encoding='utf-8'))
# coords_verify.json에는 page('lang:title')가 있음


def curl_json(url):
    r = subprocess.run(['curl', '-s', '--max-time', '25', '-A', UA, url], capture_output=True, text=False)
    try:
        return json.loads(r.stdout.decode('utf-8', errors='replace'))
    except Exception:
        return None


def qid_for(lang, title):
    u = (f'https://{lang}.wikipedia.org/w/api.php?action=query&prop=pageprops&format=json'
         f'&redirects=1&titles={urllib.parse.quote(title)}')
    j = curl_json(u)
    if not j:
        return None
    for p in j.get('query', {}).get('pages', {}).values():
        return p.get('pageprops', {}).get('wikibase_item')
    return None


def elev(qid):
    u = f'https://www.wikidata.org/w/api.php?action=wbgetclaims&format=json&property=P2044&entity={urllib.parse.quote(qid)}'
    j = curl_json(u)
    if not j:
        return None
    c = j.get('claims', {}).get('P2044')
    if not c:
        return None
    try:
        return round(float(c[0]['mainsnak']['datavalue']['value']['amount']), 1)
    except Exception:
        return None


cur = {}
for p in ('index.html',):
    s = (ROOT / p).read_text(encoding='utf-8')
    m = re.search(r'window\.MOUNTAINS = \[(.*?)\n\];', s, re.S)
    for e in re.finditer(r"\{id:'(\w+)'[^}]*?alt:'([^']*)'", m.group(1)):
        cur[e.group(1)] = e.group(2)

out = {}
for mid, d in PAGE.items():
    page = d.get('page', '')
    if ':' not in page:
        continue
    lang, title = page.split(':', 1)
    qid = qid_for(lang, title)
    time.sleep(0.15)
    e = elev(qid) if qid else None
    time.sleep(0.15)
    out[mid] = dict(name=d.get('name'), qid=qid, wd_elev=e, cur_alt=cur.get(mid))
    print(mid, qid, e, '|', cur.get(mid), flush=True)

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print('DONE', len(out))
