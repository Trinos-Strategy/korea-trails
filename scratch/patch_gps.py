# -*- coding: utf-8 -*-
"""GPS 좌표 정밀화 + dist/time 정밀화 + EN 누출 수리 (PR #36 1트랙).

좌표 출처:
- ko 위키 인포박스(위도도/분/초) × Wikidata P625/en 위키 교차
- 검색 확정: 노인봉(소금강)·비로봉(오대산)·가지산·EBC
거리/시간 출처: alle.co.kr 실측(2026-09-27 수집, scratch/alle_data.json)
"""
import json, pathlib, re

ROOT = pathlib.Path('/Users/mac/korea-trails')

FIXES = {
    # ── ko 위키 인포박스 좌표 (× wd/en 위키 교차 확인) ──
    'gwanaksan':      (37.42889, 126.96361),
    'suraksan':       (37.696046, 127.081947),
    'bulsan':         (37.662081, 127.09877),
    'unmunsan':       (35.615506, 128.959725),
    'heuiyangsan':    (36.71595, 128.0027),
    'unjangsan':      (35.91095, 127.35728),
    'gyeryongsan':    (36.34328, 127.20614),
    'woraksan':       (36.889375, 128.090875),
    'yumyeongsan':    (37.576265, 127.487614),
    # ── wiki == wikidata ──
    'namsan':         (35.768056, 129.225556),
    'naejangsan':     (35.483333, 126.883333),
    'palgongsan':     (36.016944, 128.695),
    'myeongseongsan': (38.106944, 127.337778),
    'unaksan':        (37.878056, 127.325),
    'hwawangsan':     (35.547778, 128.532778),
    'biseulsan':      (35.716667, 128.524444),
    'duryunsan':      (34.472778, 126.637778),
    'wolchulsan':     (34.767778, 126.704444),
    'sikjangsan':     (36.295, 127.48),
    'minjusan':       (36.04, 127.849167),
    'daedunsan':      (36.12, 127.323333),
    'daeamsan':       (38.211111, 128.135),
    'dutasan':        (37.26, 129.1),
    'manisan':        (37.616667, 126.433333),
    'juwangsan':      (36.38922, 129.162589),
    'cheongnyangsan': (36.791389, 128.926944),
    'maisan':         (35.762222, 127.404722),
    'mudeungsan':     (35.1392, 126.9925),
    'ansan':          (37.576667, 126.945),
    'achasan':        (37.566111, 127.1025),
    'chiaksan':       (37.371667, 128.050556),
    'soyosan':        (37.941944, 127.088889),
    'inwangsan':      (37.584722, 126.958611),
    'geumjeongsan':   (35.283056, 129.055556),
    # ── 검색 확정 (나무위키 좌표 2건 일치) ──
    'gajisan':        (35.6203, 129.0031),
    'sogeumgang':     (37.7864, 128.5939),   # 노인봉 1,338m
    'odaesan':        (37.7853, 128.5642),   # 비로봉 1,563m
    # ── 국제 (wiki == wd) ──
    'rinjani':        (-8.414414, 116.459767),
    'yangmingshan':   (25.1775, 121.5475),
    'huangshan':      (30.125, 118.166667),
    'tateyama':       (36.575833, 137.619722),
    'fansipan':       (22.303333, 103.775315),
    'taishan':        (36.255833, 117.1075),
    'poonhill':       (28.400043, 83.68954),
    'langtang':       (28.1738, 85.5531),
    'ebc':            (28.0026, 86.8528),
}

# dist/time 정밀화 (알레 실측) — (파일, old, new)
DIST_TIME = [
    ('index.html', "id:'gwanaksan'", "dist:'6km'", "dist:'6.6km'"),
    ('index.html', "id:'gwanaksan'", "time:'2.5-3시간'", "time:'3-3.5시간'"),
    ('index.html', "id:'suraksan'", "time:'4-5시간'", "time:'약 4시간'"),
    ('index.html', "id:'bulsan'", "dist:'—'", "dist:'4.3-6.3km'"),
    ('en/index.html', "id:'gwanaksan'", "dist:'6km'", "dist:'6.6 km'"),
    ('en/index.html', "id:'gwanaksan'", "time:'2.5–3 h'", "time:'3–3.5 h'"),
    ('en/index.html', "id:'suraksan'", "time:'4–5 h'", "time:'≈ 4 h'"),
    ('en/index.html', "id:'bulsan'", "dist:'—'", "dist:'4.3–6.3 km'"),
]

# EN 누출 수리 — desc 번역 (KO 원문 기반, 스타일 「—」+ '..' 유지)
EN_DESC = {
    'inwangsan':      "Seoul's fortress-wall hill — the Inwang section of the Seoul City Wall and downtown panoramas..",
    'gajisan':        "Highest peak of the Yeongnam Alps — the shortest Seoknam-tunnel route and Tongdosa's Naewon valley..",
    'hwawangsan':     "Changnyeong's azalea mountain — three major colonies, Hwawangsanseong fortress and the 'Hur Jun' set..",
    'unjangsan':      "Jinan–Wanju landmark — Unjangdae 1,126 m and the Chilseongdae–Samjangbong ridgeline..",
    'yeongchwisan':   "Yeosu's azalea mountain — ridge-top colonies on Jinnyebong 510 m and the April azalea festival..",
    'biseulsan':      "Cheonwangbong of Daegu Dalseong–Cheongdo — Yugasa trailhead, the Akgeon ridge and silver-grass fields..",
    'cheongnyangsan': "Rock-peak mountain of Bonghwa–Andong — Uisangbong 869.7 m, Cheongnyangsa temple and the Sky Bridge..",
    'ansan':          "A low hill in Seoul's Seodaemun — the beacon mound (monument) and the 7 km barrier-free trail..",
    'bulsan':         "On the Nowon–Uijeongbu border — Jeongamsa temple, the Turtle Rock granite ridge and a Suraksan traverse..",
    'sogeumgang':     "Scenic Site No. 1 of Odaesan — the Noinbong 1,338 m ridge and granite pinnacles of the Sogeum valley..",
    'heuiyangsan':    "Granite crags on the Baekdudaegan between Goesan and Mungyeong — the Jireumtjae loop and main ridge..",
    'cheongtaesan':   "On the Hoengseong–Pyeongchang border — six trails of Cheongtaesan Recreational Forest and summit views..",
    'baekamsan':      "On the Jangseong–Sunchang border — Sangwangbong 741.2 m and the Baekyangsa–Guamsa temple ridge..",
    'yongmunsan':     "Yangpyeong's guardian mountain — via Yongmunsa temple, Samigi-bong and Madangbawu to Gashebong 1,157 m..",
    'yumyeongsan':    "A Gapyeong Seolak-myeon mountain — recreational-forest trailhead, valley course and a Yongmunsan traverse..",
    'namsan':         "UNESCO Gyeongju Namsan — Geumobong 468 m strewn with temple sites and stone Buddhas..",
    'gyebangsan':     "Highest peak of Odaesan National Park at 1,577 m — grassy ridgelines and winter snowscapes..",
    'dutasan':        "1,357 m on the Donghae–Samcheok border — the Loom Rock and Machenru crags, and the Mureung valley..",
    'manisan':        "Highest peak of Ganghwa Island — the Dangun altar legend of Chamsungdan and Samnangseong fortress..",
    'daeamsan':       "A rock mountain of Yanggu–Inje — reserved Yongneup wetland visits (Natural Monument No. 246) and Baekdudaegan views..",
    'baegunsan':      "Gwangyang's azalea mountain — the festival ridge line and Seomjin River views..",
    'sinbulsan':      "Main peak of the Yeongnam Alps — the Ganwoljae silver-grass plateau and Baenaegol ridge..",
    'gamaksan':       "Paju's guardian mountain — Gamaksa temple, Jangheung valley, the suspension bridge and Hanbuk Jeongmaek trail..",
}
EN_TIME = {
    'ansan': '2–3 h', 'bulsan': '2–3 h', 'sogeumgang': '2–3 h', 'heuiyangsan': '4 h',
    'cheongtaesan': '≈ 2 h', 'baekamsan': '4–5 h', 'yongmunsan': '4–5 h', 'yumyeongsan': '3–4 h',
    'namsan': '3–4 h', 'gyebangsan': '4–5 h', 'dutasan': '5 h', 'manisan': '3 h',
    'daeamsan': '4–5 h', 'baegunsan': '4–5 h', 'sinbulsan': '5 h', 'gamaksan': '4–5 h',
}


def set_latlng(text, mid, lat, lng):
    """{id:'<mid>' ...} 항목의 lat/lng를 교체. (치환 1건 강제)"""
    pat = re.compile(r"(\{id:'" + mid + r"'[^}]*?lat:\s*)([-\d.]+)(,\s*lng:\s*)([-\d.]+)(\})")
    hits = pat.findall(text)
    assert len(hits) == 1, f'{mid}: {len(hits)} hits'
    new = pat.sub(lambda m: f'{m.group(1)}{lat}{m.group(3)}{lng}{m.group(5)}', text, count=1)
    return new


def main():
    log = {}
    for page in ('index.html', 'en/index.html'):
        p = ROOT / page
        s = p.read_text(encoding='utf-8')
        n = 0
        for mid, (lat, lng) in FIXES.items():
            s2 = set_latlng(s, mid, lat, lng)
            if s2 != s:
                n += 1
            s = s2
        p.write_text(s, encoding='utf-8')
        log[f'coords {page}'] = n

    # dist/time 정밀화
    for page, anchor, old, new in DIST_TIME:
        p = ROOT / page
        s = p.read_text(encoding='utf-8')
        i = s.find(anchor)
        assert i >= 0, anchor
        j = s.find('}', i)
        seg = s[i:j]
        assert seg.count(old) == 1, f'{page} {anchor} {old}: {seg.count(old)}'
        s = s[:i] + seg.replace(old, new) + s[j:]
        p.write_text(s, encoding='utf-8')
    log['dist_time'] = len(DIST_TIME)

    # EN 누출 수리
    p = ROOT / 'en/index.html'
    s = p.read_text(encoding='utf-8')
    n_d = n_t = 0
    for mid, en in EN_DESC.items():
        pat = re.compile(r"(\{id:'" + mid + r"'[^}]*?desc:')(?:[^']*)(')")
        s2, c = pat.subn(lambda m: m.group(1) + en + m.group(2), s, count=1)
        assert c == 1, f'desc {mid} c={c}'
        if s2 != s:
            n_d += 1
        s = s2
    for mid, en in EN_TIME.items():
        pat = re.compile(r"(\{id:'" + mid + r"'[^}]*?time:')(?:[^']*)(')")
        s2, c = pat.subn(lambda m: m.group(1) + en + m.group(2), s, count=1)
        assert c == 1, f'time {mid} c={c}'
        if s2 != s:
            n_t += 1
        s = s2
    p.write_text(s, encoding='utf-8')
    log['en_desc_fixed'] = n_d
    log['en_time_fixed'] = n_t

    # JSON-LD geo 갱신 (playbook 92파일)
    n_geo = 0
    for mid, (lat, lng) in FIXES.items():
        for f in (ROOT / f'{mid}-playbook.html', ROOT / 'en' / f'{mid}-playbook.html'):
            s = f.read_text(encoding='utf-8')
            pat = re.compile(
                r'("geo":\s*\{"@type":\s*"GeoCoordinates",\s*"latitude":\s*)([-\d.]+)(,\s*"longitude":\s*)([-\d.]+)(\})')
            s2, c = pat.subn(lambda m: f'{m.group(1)}{lat}{m.group(3)}{lng}{m.group(5)}', s, count=1)
            assert c == 1, f'geo missing: {f.name}'
            if s2 != s:
                n_geo += 1
            f.write_text(s2, encoding='utf-8')
    log['jsonld_geo_updated'] = n_geo
    print(json.dumps(log, indent=1))


if __name__ == '__main__':
    main()
