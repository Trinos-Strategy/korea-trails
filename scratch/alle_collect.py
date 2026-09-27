# -*- coding: utf-8 -*-
"""alle.co.kr 산·코스 데이터 수집기 (공개 웹 페이지/AJAX만 사용, 요청 간 0.4s 지연).

출력: scratch/alle_data.json
{
  "mountains": {"<seq>": {"name","loc","range","course_cnt","desc","code","courses":[...]}},
  "courses": {"<seq>": {"name","mountain","mountain_seq","region","desc","level","time","km","steps","tags",
                        "waypoints":[{"name","coords":[{lat,lng,label}...]}...],  # naver.me 경유지
                        "segments":[["기점","종점",km,time]...],
                        "amenities":{"<wp name>":[...codes names]},
                        "info":[...주의 문구...],
                        "naver":"naver.me/xxx", "photos":[...] }}
}
"""
import json, math, re, subprocess, sys, time, urllib.parse

BASE = 'https://alle.co.kr/mb'
OUT = 'scratch/alle_data.json'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36'

req_count = 0


def get(url, data=None, binary=False):
    global req_count
    req_count += 1
    cmd = ['curl', '-s', '-A', UA, '--max-time', '25']
    if data is not None:
        cmd += ['--data', data]
    cmd += [url]
    r = subprocess.run(cmd, capture_output=True, text=False)
    b = r.stdout
    if binary:
        return b
    return b.decode('utf-8', errors='replace')


def strip_tags(h):
    t = re.sub(r'<script.*?</script>', '', h, flags=re.S)
    t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = t.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
    return re.sub(r'\s+', ' ', t).strip()


# ── 코드표 (005 레벨 / 006 편의시설, common/lib/code.php에서 수집) ──
LEVEL = {'005001': '쉬움', '005002': '보통', '005003': '약간 어려움', '005004': '어려움', '005005': '매우 어려움'}
AMEN = {'006001': '주차장', '006002': '화장실', '006003': '편의점', '006004': '지하철', '006005': '시내버스',
        '006006': '아웃도어 매장', '006007': '카페', '006008': '탐방센터', '006009': '식당', '006010': '에어건', '006011': '매표소'}


def list_mountains():
    """산 목록 (seq, name, loc, range, course count, 소개)."""
    ms = {}
    for pg in range(1, 6):
        h = get(f'{BASE}/content/lib/ajax.mount.php', f'pg={pg}&pgsize=30')
        if not h.strip():
            break
        for m in re.finditer(
                r'mount_view\?seq=(\d+)".*?img src="[^"]*" alt="([^"]*)".*?class="name">([^<]+)</span>\s*'
                r'<span class="location">([^<]+)</span>(?:.*?class="comment">([^<]*)</span>)?'
                r'.*?class="course">([^<]+)</em>\s*<em class="range">([^<]+)</em>', h, re.S):
            seq = int(m.group(1))
            ms[seq] = dict(name=(m.group(3) or m.group(2)).strip(), loc=re.sub(r'&nbsp;', ' ', m.group(4)).strip(),
                           comment=(m.group(5) or '').strip(), course_cnt=re.sub(r'\D', '', m.group(6)) or '0',
                           range=m.group(7).strip())
        if '<li cpage' not in h and pg > 1 and f'cpagecnt' not in h:
            pass
        time.sleep(0.4)
    return ms


def mountain_code(seq):
    h = get(f'{BASE}/content/mount_view?seq={seq}')
    m = re.search(r'id="code"\s+name="code"\s+value="(\d+)"', h)
    desc = ''
    mm = re.search(r'class="mountain_summary[^"]*">([^<]*)<', h)
    if mm:
        desc = mm.group(1).strip()
    return (m.group(1) if m else None), desc, h


def list_courses(code, level=''):
    out, cpg = {}, 1
    while True:
        h = get(f'{BASE}/content/lib/ajax.mcourse.php', f'code={code}&level={level}&cpg={cpg}&cpgsize=30')
        if not h.strip():
            break
        found = 0
        for m in re.finditer(r'course_view\?seq=(\d+)".*?class="tit_area">\s*<span>([^<]*)</span>\s*<strong>([^<]+)</strong>\s*<em>([^<]*)</em>.*?'
                             r'class="level ([a-z]+)">([^<]*)</strong>\s*<span class="time">\s*([^<]*)</span>\s*<span class="range">([^<]*)</span>\s*'
                             r'<span class="walk">([^<]*)</span>(.*?)(?:</li>|$)', h, re.S):
            seq = int(m.group(1))
            tags = [t.strip() for t in re.findall(r'<span>([^<]+)</span>', m.group(9)) if t.strip()]
            out[seq] = dict(name=m.group(3).strip(), region=re.sub(r'&nbsp;', ' ', m.group(2)).strip(),
                            oneliner=m.group(4).strip(), level=m.group(6).strip(), time=m.group(7).strip(),
                            km=m.group(8).strip(), steps=m.group(9).strip(), tags=tags)
            found += 1
        if not found:
            break
        if f'cpage="{cpg}" cpagecnt="{cpg}"' in h or found < 30:
            # 다음 페이지 존재 여부: cpagecnt는 "마지막 페이지" 표시로 보임 → 정확히는 목록 길이로 판단
            pass
        cpg += 1
        if cpg > 4:
            break
        time.sleep(0.4)
    return out


def course_detail(seq):
    h = get(f'{BASE}/content/course_view?seq={seq}')
    d = {}
    # 네이버 경로 링크
    m = re.search(r'href="(https://naver\.me/[^"]+)"', h)
    if m:
        d['naver'] = m.group(1)
    # 코스 구간(기점/구간/종점)
    wps, segs = [], []
    for m in re.finditer(r'<h3 class="tit">([^<]+)</h3>\s*<p class="range">([^<]*)</p>', h):
        name = m.group(1).strip()
        rng = re.sub(r'\s+', ' ', m.group(2)).replace('&nbsp;', ' ').strip()
        if rng:
            km = re.search(r'([\d.]+)\s*km', rng)
            tm = re.search(r'(\d+)시간\s*(\d+)?분?', rng)
            segs.append([name, (km.group(1) + 'km') if km else '', (tm.group(1) + '시간' + (tm.group(2) or '') + '분') if tm else rng])
        else:
            wps.append(name)
    d['waypoints'] = wps
    d['segments'] = segs
    # 편의시설 코드
    amen = {}
    for m in re.finditer(r'Code\.Load\("utilstxt", "(?:util\d+)", "006000", "([\d,]+)"\)', h):
        codes = [c for c in m.group(1).split(',') if c]
        amen[str(len(amen))] = [AMEN.get(c, c) for c in codes]
    d['amenity_sets'] = amen
    # 코스 정보 문구
    info = []
    m = re.search(r'<h3 class="course_title mb50">코스 정보</h3>(.*?)</ul>', h, re.S)
    if m:
        info = [re.sub(r'\s+', ' ', strip_tags(x)).strip() for x in re.findall(r'<li[^>]*>(.*?)</li>', m.group(1), re.S)]
        info = [x for x in info if x]
    d['info'] = info
    return d, h


def naver_coords(short):
    """naver.me 단축 URL → 리다이렉트 Location에서 구면 Web Mercator 좌표를 WGS84로 디코딩."""
    try:
        r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{redirect_url}', '-A', UA, '--max-time', '20', short],
                           capture_output=True, text=True)
        loc = r.stdout.strip()
        if not loc:
            return None
        pts = []
        for m in re.finditer(r'(\d{6,8}\.\d+),(\d{7}\.\d+),([^/,]+)', urllib.parse.unquote(loc)):
            x, y, label = float(m.group(1)), float(m.group(2)), m.group(3)
            lon = math_deg(x / 6378137.0)
            lat = math_deg(2 * math.atan(math.exp(y / 6378137.0)) - math.pi / 2)
            pts.append(dict(lat=round(lat, 6), lng=round(lon, 6), label=label))
        return pts
    except Exception as e:
        return None


def math_deg(rad):
    import math
    return math.degrees(rad)


def main():
    data = dict(mountains={}, courses={}, meta=dict(collected='2026-09-27', source='alle.co.kr/mb'))
    ms = list_mountains()
    print(f'mountains: {len(ms)}')
    for seq, m in sorted(ms.items()):
        code, desc, _ = mountain_code(seq)
        m['code'] = code
        m['desc'] = desc
        time.sleep(0.4)
        if not code:
            print(f'  [{seq}] {m["name"]}: code NOT FOUND')
            continue
        cs = list_courses(code)
        print(f'  [{seq}] {m["name"]} ({code}): {len(cs)} courses')
        for cseq, c in sorted(cs.items()):
            det, _ = course_detail(cseq)
            c.update(det)
            if c.get('naver'):
                pts = naver_coords(c['naver'])
                c['coords'] = pts
                time.sleep(0.35)
            data['courses'][str(cseq)] = dict(mountain_seq=seq, mountain=m['name'], **c)
            time.sleep(0.4)
        data['mountains'][str(seq)] = m
    json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'requests: {req_count} → {OUT}')
    print(f'mountains: {len(data["mountains"])}, courses: {len(data["courses"])}, with coords: '
          f'{sum(1 for c in data["courses"].values() if c.get("coords"))}')


if __name__ == '__main__':
    main()
