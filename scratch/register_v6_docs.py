# -*- coding: utf-8 -*-
"""6차 문서 등록 — README·CREDITS·PHOTO-ACCURACY·deep-info KO/EN."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ── README.md ──
p = ROOT / 'README.md'
s = p.read_text(encoding='utf-8')
s = s.replace('## 📂 플레이북 현황 (68산)', '## 📂 플레이북 현황 (72산)')
s = s.replace('**등산 플레이북 68종**', '**등산 플레이북 72종**')
INS = {
    '강원': ' · [대암산](./daeamsan-playbook.html)',
    '경기/서울': ' · [감악산](./gamaksan-playbook.html)',
    '전라': ' · [백운산](./baegunsan-playbook.html)',
    '경상/제주': ' · [신불산](./sinbulsan-playbook.html)',
}
lines = s.split('\n')
out = []
for ln in lines:
    out.append(ln)
    m = ln.match if False else None
for i, ln in enumerate(lines):
    for region, add in INS.items():
        if ln.startswith(f'| {region} |'):
            lines[i] = ln.rstrip() + add
s = '\n'.join(lines)
p.write_text(s, encoding='utf-8')
import re
rows = re.findall(r'^\| (강원|경기/서울|충청|전라|경상/제주|인천) \|(.+)$', s, re.M)
tot = sum(len(r[1].split('](')) - 1 for r in rows)
print('README: 72산 헤더·기능 행·표 4행 추가 — 한국 행 링크 합계', tot)

# ── CREDITS.md ──
p = ROOT / 'CREDITS.md'
s = p.read_text(encoding='utf-8')
s += '''
## 한국 100대 명산 6차(4산) — Unsplash (Unsplash License)
※ 일반 사진 대체

| 산 | 사진작가들 |
|---|---|
| 대암산·백운산·신불산·감악산 | (개별 출처는 각 페이지 gallery 참조) |
'''
p.write_text(s, encoding='utf-8')
print('CREDITS: appended')

# ── PHOTO-ACCURACY.md ──
p = ROOT / 'PHOTO-ACCURACY.md'
s = p.read_text(encoding='utf-8')
s = s.replace('| 일반 사진 대체 | 25산 | 한국 100대 명산 1~5차 24산 + 타이산 (CREDITS.md에 명시됨) |',
              '| 일반 사진 대체 | 29산 | 한국 100대 명산 1~6차 28산 + 타이산 (CREDITS.md에 명시됨) |')
assert '1~6차 28산' in s
old = '| 마니산 | 한국 산악 일반 | 중간 | 참성단·삼랑성 |'
new = '''| 마니산 | 한국 산악 일반 | 중간 | 참성단·삼랑성 |
| 대암산 | 한국 산악 일반 | 중간 | 용늪 고층습원·백두대간 조망 |
| 백운산 | 한국 산악 일반 | 중간 | 철쭉 능선 |
| 신불산 | 한국 산악 일반 | 중간 | 간월재 억새평원 |
| 감악산 | 한국 산악 일반 | 중간 | 감악사·출렁다리 |'''
assert s.count(old) == 1
s = s.replace(old, new)
p.write_text(s, encoding='utf-8')
print('PHOTO-ACCURACY: 29산, +4행')

# ── deep-info KO/EN ──
DI = {
 'daeamsan': dict(
  note='한국 100대 명산 6차',
  sec=[
   ('book', '입산·예약', [
     ('용늪 100% 사전예약제', '필수', '대암산 용늪(천연기념물 제246호) 탐방은 100% 예약제입니다. 최소 10일 전 신청, 신분증 지참. 인제 코스(sum.inje.go.kr)·양구 코스(yg-eco.kr)는 창구가 다릅니다.'),
     ('일반 등산로', '참고', '향로봉 일반 등산로는 별도 예약이 불필요합니다. 다만 용늪 보호구역은 예약 없이 진입할 수 없습니다.'),
     ('민통선 구역', '필수', '산 일대는 민통선 내 — 신분증 필수이며 군사시설 촬영은 금지입니다.')]),
   ('bus', '교통', [
     ('인제 가아리 코스', '참고', '가아리 탐방안내소 집결 후 차량 14km 이동으로 탐방 출발점에 닿습니다. 대중교통 접근이 어려워 자가용·택시 이용이 일반적입니다.'),
     ('양구 서흥리 코스', '참고', '임시 대암산용늪탐방센터에서 출발합니다. 양구 시내에서 접근하며 배차 정보는 이용 전 확인하세요.')]),
   ('tent', '숙박', [
     ('양구·인제 읍내', '참고', '양구읍·인제읍의 모텔·펜션이 산행 거점입니다. 파로호 인근 숙박도 가깝습니다.')]),
   ('shield', '안전·비상연락', [
     ('비상 연락', '필수', '산악 사고 시 119로 신고하세요.'),
     ('고지대 기상', '권장', '해발 1,280m 습지 일대는 여름에도 쌀쌀합니다. 우천·강풍 시 데크길이 미끄럽습니다.')]),
  ],
  sources=[('인제군 생태관광 — 대암산 용늪', 'https://sum.inje.go.kr'), ('양구군 용늪탐방', 'https://yg-eco.kr')],
 ),
 'baegunsan': dict(
  note='한국 100대 명산 6차',
  sec=[
   ('book', '입산·예약', [
     ('허가 불필요', '참고', '백운산은 별도 예약·허가 없이 등산할 수 있습니다.'),
     ('자연휴양림 요금', '권장', '백운산자연휴양림 구간은 시설 이용·주차 요금 체계가 있습니다 — 광양시청 안내를 이용 전 확인하세요.')]),
   ('bus', '교통', [
     ('대중교통', '참고', '광양·구례 방면 시외버스로 접근 후 로컬 교통이 필요합니다. 들머리(내회·논실·휴양림)별 접근이 다르니 이용 전 확인하세요.'),
     ('자가용', '참고', '철쭉철(5월 말~6월 초) 주말은 도로·주차 혼잡이 극심합니다.')]),
   ('tent', '숙박', [
     ('휴양림·숙박', '참고', '백운산자연휴양림의 숲속집·광양 시내 숙박을 이용할 수 있습니다.')]),
   ('shield', '안전·비상연락', [
     ('비상 연락', '필수', '산악 사고 시 119로 신고하세요.'),
     ('철쭉철 혼잡', '권장', '철쭉제 기간 정상 주변 인파가 몰립니다 — 이른 아침 산행을 권합니다.')]),
  ],
  sources=[('광양시청 — 백운산자연휴양림', 'https://www.gwangyang.go.kr'), ('백운산 철쭉제 안내', 'https://www.gwangyang.go.kr')],
 ),
 'sinbulsan': dict(
  note='한국 100대 명산 6차',
  sec=[
   ('book', '입산·예약', [
     ('허가 불필요', '참고', '신불산은 별도 예약·허가 없이 등산할 수 있습니다(국립공원 아님).')]),
   ('bus', '교통', [
     ('배내주차장', '참고', '울주군 상북면 이천리 배내2공영주차장이 주 들머리입니다. 만차 시 배내1공영주차장을 이용합니다.'),
     ('대중교통', '참고', '울산 시내버스로 배내골 방면 접근이 가능하나 배차가 드뭅니다 — 이용 전 시간표 확인.')]),
   ('tent', '숙박', [
     ('울산·언양 일대', '참고', '울산 시내·언양의 숙박이 산행 거점으로 편리합니다.')]),
   ('shield', '안전·비상연락', [
     ('비상 연락', '필수', '산악 사고 시 119로 신고하세요.'),
     ('억새철·암릉', '권장', '가을 억새철 혼잡하고, 간월산 구간 암릉은 우천 시 위험합니다.')]),
  ],
  sources=[('울산광역시 문화관광 — 영남알프스', 'https://tour.ulsan.go.kr'), ('울주군 문화관광', 'https://www.ulju.go.kr')],
 ),
 'gamaksan': dict(
  note='한국 100대 명산 6차',
  sec=[
   ('book', '입산·예약', [
     ('허가 불필요', '참고', '감악산은 별도 예약·허가 없이 등산할 수 있습니다.'),
     ('출렁다리 운영시간', '권장', '출렁다리는 개방시간이 정해져 있습니다 — 이용 전 파주시 안내를 확인하세요.')]),
   ('bus', '교통', [
     ('대중교통', '참고', '서울·일산에서 운행하는 광역버스로 파주 접근 후 로컬 교통으로 감악사·장흥계곡 방면에 닿습니다. 배차는 이용 전 확인하세요.'),
     ('자가용', '참고', '감악사 주차장·장흥계곡 주차장이 있습니다. 주말 오전 혼잡합니다.')]),
   ('tent', '숙박', [
     ('파주·일산', '참고', '수도권 근교 산이라 당일치기가 일반적입니다. 파주·일산 숙박 가능.')]),
   ('shield', '안전·비상연락', [
     ('비상 연락', '필수', '산악 사고 시 119로 신고하세요.'),
     ('암릉·출렁다리', '권장', '임꺽정봉 전후 암릉은 우천 시 사고가 잦고, 출렁다리는 강풍 시 흔들림이 큽니다.')]),
  ],
  sources=[('파주시 문화관광 — 감악산', 'https://www.paju.go.kr'), ('장흥계곡·출렁다리 안내', 'https://www.paju.go.kr')],
 ),
}
TITLES = {'입산·예약': 'Entry & Booking', '교통': 'Transport', '숙박': 'Lodging', '안전·비상연락': 'Safety & Emergency'}
EN_DI = {
 'daeamsan': [
  [('Yongneup is fully reservation-only', 'Required', 'The Yongneup marsh (Natural Monument No. 246) tour is 100% reservation-based: apply at least 10 days ahead and bring photo ID. Inje (sum.inje.go.kr) and Yanggu (yg-eco.kr) use separate portals.'),
   ('General ridge trail', 'Note', 'The Hyangnobong hiking ridge needs no reservation — but the marsh reserve is off-limits without one.'),
   ('Civilian Control Line', 'Required', 'The area lies inside the CCL — ID is mandatory and photographing military facilities is prohibited.')],
  [('Inje Gaari course', 'Note', 'Meet at the Gaari center, then a 14 km vehicle transfer to the trail start. Driving or taxi is the practical access.'),
   ('Yanggu Seoheung-ri course', 'Note', 'Starts at the temporary Yongneup center near Yanggu — check local transit times in advance.')],
  [('Yanggu & Inje towns', 'Note', 'Motels and pensions in both county seats, or stays near Paroho Lake, make convenient bases.')],
  [('Emergency', 'Required', 'Call 119 for mountain accidents.'),
   ('Highland weather', 'Recommended', 'The 1,280 m moor runs cold even in summer; boardwalks are slippery in rain.')],
 ],
 'baegunsan': [
  [('No permit needed', 'Note', 'Baegunsan is open without reservation or permit.'),
   ('Recreation forest fees', 'Recommended', 'The recreation forest section has facility and parking fees — check Gwangyang City notices before visiting.')],
  [('Public transport', 'Note', 'Reach Gwangyang or Gurye by intercity bus, then local transport to the specific trailhead (Naeroe, Nonsil, or the forest) — verify each in advance.'),
   ('By car', 'Note', 'Azalea-season weekends (late May–early June) bring severe traffic and parking jams.')],
  [('Recreation forest & town', 'Note', 'Forest cabins or Gwangyang town lodging work well.')],
  [('Emergency', 'Required', 'Call 119 for mountain accidents.'),
   ('Festival crowds', 'Recommended', 'The summit area packs during the Azalea Festival — hike early.')],
 ],
 'sinbulsan': [
  [('No permit needed', 'Note', 'Sinbulsan is open without reservation or permit (not a national park).')],
  [('Baenae parking', 'Note', 'Baenae Lot 2 in Icheon-ri, Sangbuk-myeon, Ulju is the main trailhead lot; use Lot 1 when full.'),
   ('Public transport', 'Note', 'City buses from Ulsan reach the Baenaegol area but run infrequently — check timetables.')],
  [('Ulsan & Eonyang', 'Note', 'Town lodging in Ulsan or Eonyang is the practical base.')],
  [('Emergency', 'Required', 'Call 119 for mountain accidents.'),
   ('Silver-grass season & crags', 'Recommended', 'Autumn weekends crowd the trails; the Ganwolsan crags are dangerous in rain.')],
 ],
 'gamaksan': [
  [('No permit needed', 'Note', 'Gamaksan is open without reservation or permit.'),
   ('Bridge hours', 'Recommended', 'The suspension bridge has set opening hours — check Paju City notices before you go.')],
  [('Public transport', 'Note', 'Inter-city buses from Seoul/Ilsan reach Paju, then local transport toward Gamaksa or the valley — verify schedules.'),
   ('By car', 'Note', 'Gamaksa and valley lots; crowded on weekend mornings.')],
  [('Paju & Ilsan', 'Note', 'A capital-area day trip is standard; overnight options in Paju or Ilsan.')],
  [('Emergency', 'Required', 'Call 119 for mountain accidents.'),
   ('Crags & bridge', 'Recommended', 'Crags around Imkkeokjeongbong are accident-prone when wet; the bridge sways in strong wind.')],
 ],
}
SRC_EN = {
 'daeamsan': [('Inje County Eco-tourism — Yongneup', 'https://sum.inje.go.kr'), ('Yanggu Yongneup tours', 'https://yg-eco.kr')],
 'baegunsan': [('Gwangyang City — Recreation Forest', 'https://www.gwangyang.go.kr'), ('Baegunsan Azalea Festival', 'https://www.gwangyang.go.kr')],
 'sinbulsan': [('Ulsan Tourism — Yeongnam Alps', 'https://tour.ulsan.go.kr'), ('Ulju County Tourism', 'https://www.ulju.go.kr')],
 'gamaksan': [('Paju City — Gamaksan', 'https://www.paju.go.kr'), ('Valley & bridge info', 'https://www.paju.go.kr')],
}


def render_ko(mid, d):
    sections = []
    for icon, title, items in d['sec']:
        its = ', '.join(f"{{ h: '{h}', tag: '{tag}', body: '{b}' }}" for h, tag, b in items)
        sections.append(f"{{ icon: '{icon}', title: '{title}', items: [{its}] }}")
    srcs = ', '.join(f"{{ label: '{l}', href: '{u}' }}" for l, u in d['sources'])
    return (f"window.DEEP_INFO['{mid}'] = {{updated:'2026-09 기준',note:'{d['note']}',"
            f"sections:[{', '.join(sections)}],sources:[{srcs}]}};\n")


def render_en(mid, d, en_blocks, sources):
    sections = []
    for i, (icon, title, _items) in enumerate(d['sec']):
        its = ', '.join(f"{{ h: '{h}', tag: '{tag}', body: '{b}' }}" for h, tag, b in en_blocks[i])
        sections.append(f"{{ icon: '{icon}', title: '{TITLES[title]}', items: [{its}] }}")
    srcs = ', '.join(f"{{ label: '{l}', href: '{u}' }}" for l, u in sources)
    return (f"window.DEEP_INFO_EN['{mid}'] = {{updated:'2026-09 기준',note:'Korea 100 Famous Mountains round 6',"
            f"sections:[{', '.join(sections)}],sources:[{srcs}]}};\n")


jp = ROOT / 'assets/js/deep-info-data.js'
s = jp.read_text(encoding='utf-8')
add = '\n/* ── 한국 100대 명산 6차: 대암산·백운산(광양)·신불산·감악산 (2026-09 세션 검증) ──\n'
add += ' * 사실 근거: 100대 목록 포함(위키백과 × 산림청 2002), 대암산 용늪 예약제는\n'
add += ' * sum.inje.go.kr × yg-eco.kr 공공 소스 교차. 나머지 코스·표고는 공개 산행 기록 교차.\n */\n'
for mid, d in DI.items():
    add += render_ko(mid, d) + '\n'
jp.write_text(s.rstrip() + '\n' + add, encoding='utf-8')
print('deep-info-data.js: +4')

pe = ROOT / 'assets/js/deep-info-data-en.js'
s = pe.read_text(encoding='utf-8')
add = '\n/* Korea 100 Famous Mountains round 6: Daeamsan, Baegunsan, Sinbulsan, Gamaksan — KO/EN synced 2026-09. */\n'
for mid, d in DI.items():
    add += render_en(mid, d, EN_DI[mid], SRC_EN[mid]) + '\n'
pe.write_text(s.rstrip() + '\n' + add, encoding='utf-8')
print('deep-info-data-en.js: +4')
