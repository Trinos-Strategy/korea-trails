# -*- coding: utf-8 -*-
"""71산 좌표 2소스 검증: Wikipedia(ko/en) 좌표 + Wikidata P625.

출력: scratch/coords_verify.json {id: {wiki:[lat,lng], wikidata:[lat,lng], cur:[lat,lng]}}
적용 기준(스크립트 밖에서 판정): wiki와 wikidata가 서로 0.02° 내 일치하고, 현행값과 >0.008° 차이 → 갱신.
"""
import json, subprocess, time, urllib.parse, pathlib

ROOT = '/Users/mac/korea-trails'
OUT = f'{ROOT}/scratch/coords_verify.json'

# 위키피디아 문서명 후보 (ko 위키; 비-한국 산은 en 위키)
PAGE = {
    'seoraksan': ('ko', '설악산'), 'hallasan': ('ko', '한라산'), 'jirisan': ('ko', '지리산'),
    'bukhansan': ('ko', '북한산'), 'sobaeksan': ('ko', '소백산'), 'gayasan': ('ko', '가야산 (대한민국)'),
    'odaesan': ('ko', '오대산'), 'naejangsan': ('ko', '내장산'), 'chiaksan': ('ko', '치악산'),
    'deogyusan': ('ko', '덕유산'), 'gyeryongsan': ('ko', '계룡산'), 'wolchulsan': ('ko', '월출산'),
    'mudeungsan': ('ko', '무등산'), 'duryunsan': ('ko', '두륜산'), 'minjusan': ('ko', '민주지산'),
    'sikjangsan': ('ko', '식장산'), 'woraksan': ('ko', '월악산'), 'dobongsan': ('ko', '도봉산'),
    'soyosan': ('ko', '소요산'), 'juwangsan': ('ko', '주왕산'), 'myeongseongsan': ('ko', '명성산'),
    'unaksan': ('ko', '운악산'), 'taebaeksan': ('ko', '태백산'),
    'yushan': ('en', 'Yushan'), 'xueshan': ('en', 'Xueshan'), 'yangmingshan': ('en', 'Yangmingshan'),
    'alishan': ('en', 'Alishan'), 'huangshan': ('en', 'Huangshan'), 'tateyama': ('en', 'Mount Tate'),
    'fansipan': ('en', 'Fansipan'), 'taishan': ('en', 'Mount Tai'), 'kinabalu': ('en', 'Mount Kinabalu'),
    'rinjani': ('en', 'Mount Rinjani'), 'poonhill': ('en', 'Poon Hill'),
    'gwanaksan': ('ko', '관악산'), 'suraksan': ('ko', '수락산'), 'cheonggyesan': ('ko', '청계산'),
    'achasan': ('ko', '아차산'), 'geumjeongsan': ('ko', '금정산 (부산)'), 'palgongsan': ('ko', '팔공산'),
    'unmunsan': ('ko', '운문산'), 'songnisan': ('ko', '속리산'), 'daedunsan': ('ko', '대둔산'),
    'maisan': ('ko', '마이산'), 'inwangsan': ('ko', '인왕산'), 'gajisan': ('ko', '가지산'),
    'hwawangsan': ('ko', '화왕산'), 'unjangsan': ('ko', '운장산'), 'yeongchwisan': ('ko', '영취산 (여수)'),
    'biseulsan': ('ko', '비슬산'), 'cheongnyangsan': ('ko', '청량산 (봉화)'), 'ansan': ('ko', '안산 (서울)'),
    'bulsan': ('ko', '불암산'), 'sogeumgang': ('ko', '소금강'), 'heuiyangsan': ('ko', '희양산'),
    'cheongtaesan': ('ko', '청태산 (횡성)'), 'baekamsan': ('ko', '백암산 (장성·순창)'),
    'yongmunsan': ('ko', '용문산'), 'yumyeongsan': ('ko', '유명산'), 'namsan': ('ko', '남산 (경주)'),
    'gyebangsan': ('ko', '계방산'), 'dutasan': ('ko', '두타산'), 'manisan': ('ko', '마니산'),
    'daeamsan': ('ko', '대암산'), 'baegunsan': ('ko', '백운산 (정선)'), 'sinbulsan': ('ko', '신불산'),
    'gamaksan': ('ko', '감악산'), 'ebc': ('en', 'Everest Base Camp'), 'act': ('en', 'Annapurna Circuit'),
    'langtang': ('en', 'Langtang National Park'), 'fuji': ('en', 'Mount Fuji'),
}


def curl_json(url):
    r = subprocess.run(['curl', '-s', '--max-time', '25', '-A',
                        'MTTrailsBot/1.0 (contact: dkkim@swonlaw.com)', url],
                       capture_output=True, text=False)
    try:
        return json.loads(r.stdout.decode('utf-8', errors='replace'))
    except Exception:
        return None


def wiki_coords(lang, title):
    u = (f'https://{lang}.wikipedia.org/w/api.php?action=query&prop=coordinates&format=json&coprimary=primary'
         f'&titles={urllib.parse.quote(title)}')
    j = curl_json(u)
    if not j:
        return None
    pages = j.get('query', {}).get('pages', {})
    for p in pages.values():
        c = p.get('coordinates')
        if c:
            return [round(c[0]['lat'], 6), round(c[0]['lon'], 6)]
    return None


def wikidata_coords(lang, title):
    """위키피디아 문서 → 위키데이터 항목 → P625."""
    u = (f'https://{lang}.wikipedia.org/w/api.php?action=query&prop=pageprops&format=json'
         f'&titles={urllib.parse.quote(title)}&redirects=1')
    j = curl_json(u)
    if not j:
        return None
    qid = None
    for p in j.get('query', {}).get('pages', {}).values():
        qid = p.get('pageprops', {}).get('wikibase_item')
    if not qid:
        return None
    time.sleep(0.15)
    u2 = (f'https://www.wikidata.org/w/api.php?action=wbgetclaims&format=json&property=P625'
          f'&entity={urllib.parse.quote(qid)}')
    j2 = curl_json(u2)
    if not j2:
        return None
    claims = j2.get('claims', {}).get('P625')
    if not claims:
        return None
    v = claims[0]['mainsnak']['datavalue']['value']
    return [round(v['latitude'], 6), round(v['longitude'], 6)]


def dist(a, b):
    """대략 거리(km)."""
    import math as m
    la1, lo1, la2, lo2 = map(m.radians, [a[0], a[1], b[0], b[1]])
    x = m.cos(la1) * m.cos(la2) * (m.cos(lo2) - m.cos(lo1))
    y = m.cos(la1) * m.sin(lo2) - m.cos(la2) * m.sin(lo1)
    z = m.sin(la2) - m.sin(la1)
    c = m.sqrt(x * x + y * y + z * z)
    return 6371.0 * 2 * m.asin(c / 2)


def main():
    cur = json.load(open('/tmp/cur_coords.json'))
    out = {}
    for mid, (lang, title) in PAGE.items():
        if mid not in cur:
            print('SKIP (not in MOUNTAINS):', mid)
            continue
        w = wiki_coords(lang, title)
        time.sleep(0.2)
        wd = wikidata_coords(lang, title)
        time.sleep(0.2)
        c = [cur[mid]['lat'], cur[mid]['lng']]
        out[mid] = dict(name=cur[mid]['name'], page=f'{lang}:{title}', wiki=w, wikidata=wd, cur=c)
        d_ww = round(dist(w, wd), 3) if w and wd else None
        d_wc = round(dist(w, c), 2) if w else None
        print(f'{mid:14s} {cur[mid]["name"]:10s} wiki={w} wd={wd} | wiki-wd={d_ww}km wiki-cur={d_wc}km')
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('→', OUT)


if __name__ == '__main__':
    main()
