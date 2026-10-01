# -*- coding: utf-8 -*-
"""5차 등록 후반부 — README·CREDITS·PHOTO-ACCURACY·deep-info 데이터."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ── README.md ────────────────────────────────────────────────
p = ROOT / 'README.md'
s = p.read_text(encoding='utf-8')
s = s.replace('## 📂 플레이북 현황 (64산)', '## 📂 플레이북 현황 (68산)')
s = s.replace('**등산 플레이북 64종**', '**등산 플레이북 68종**')

ROW_KR = [
    ('강원', [('seoraksan', '설악산'), ('chiaksan', '치악산'), ('odaesan', '오대산'), ('taebaeksan', '태백산'), ('sogeumgang', '소금강'), ('gyebangsan', '계방산'), ('dutasan', '두타산')]),
    ('경기/서울', [('bukhansan', '북한산'), ('dobongsan', '도봉산'), ('myeongseongsan', '명성산'), ('soyosan', '소요산'), ('unaksan', '운악산'), ('gwanaksan', '관악산'), ('suraksan', '수락산'), ('cheonggyesan', '청계산'), ('achasan', '아차산'), ('inwangsan', '인왕산'), ('ansan', '안산'), ('bulsan', '불알산'), ('yongmunsan', '용문산'), ('wanggwan', '왕관산'), ('yumyeongsan', '유명산')]),
    ('충청', [('sobaeksan', '소백산'), ('gyeryongsan', '계룡산'), ('minjusan', '민주지산'), ('sikjangsan', '식장산'), ('woraksan', '월악산'), ('songnisan', '속리산'), ('heuiyangsan', '희양산'), ('cheongtaesan', '청태산')]),
    ('전라', [('jirisan', '지리산'), ('naejangsan', '내장산'), ('deogyusan', '덕유산'), ('wolchulsan', '월출산'), ('mudeungsan', '무등산'), ('duryunsan', '두륜산'), ('daedunsan', '대둔산'), ('maisan', '마이산'), ('unjangsan', '운장산'), ('yeongchwisan', '영취산'), ('baekamsan', '백암산')]),
    ('경상/제주', [('gayasan', '가야산'), ('juwangsan', '주왕산'), ('hallasan', '한라산'), ('geumjeongsan', '금정산'), ('palgongsan', '팔공산'), ('unmunsan', '운문산'), ('gajisan', '가지산'), ('hwawangsan', '화왕산'), ('biseulsan', '비슬산'), ('cheongnyangsan', '청량산'), ('namsan', '남산(경주)')]),
    ('인천', [('manisan', '마니산')]),
]
kr_rows = '\n'.join('| ' + region + ' | ' + ' · '.join(f'[{name}](./{mid}-playbook.html)' for mid, name in links) + ' |' for region, links in ROW_KR)

# 기존 한국 지역 5행을 새 6행으로 교체 (강원 행부터 경상/제주 행까지)
start = s.find('| 강원 |')
assert start > 0, '강원 행 미발견'
end_marker = '| 대만 |'
end = s.find(end_marker, start)
assert end > start
s = s[:start] + kr_rows + '\n' + s[end:]

s = s.replace('**로드맵** — 다음 확장 대상: 타테야마·아리산, 황산·타이산, 동남아·네팔 트레킹. 표준·확장 절차는',
              '**로드맵** — 다음 확장 대상: 한국 100대 명산 미소개 산(순차 확장). 표준·확장 절차는')
p.write_text(s, encoding='utf-8')
print('README: patched')

# ── CREDITS.md ───────────────────────────────────────────────
p = ROOT / 'CREDITS.md'
s = p.read_text(encoding='utf-8')
s += '''
## 한국 100대 명산 5차(4산) — Unsplash (Unsplash License)
※ 일반 사진 대체

| 산 | 사진작가들 |
|---|---|
| 남산(경주)·계방산·두타산·마니산 | (개별 출처는 각 페이지 gallery 참조) |
'''
p.write_text(s, encoding='utf-8')
print('CREDITS: appended')

# ── PHOTO-ACCURACY.md ────────────────────────────────────────
p = ROOT / 'PHOTO-ACCURACY.md'
s = p.read_text(encoding='utf-8')
s = s.replace('| 일반 사진 대체 | 20산 | 한국 100대 명산 1·2차 17산 + 타이산 (CREDITS.md에 명시됨) |',
              '| 일반 사진 대체 | 25산 | 한국 100대 명산 1~5차 24산 + 타이산 (CREDITS.md에 명시됨) |')
assert '1~5차 24산' in s, '요약 행 치환 실패'
old_rows = '| 유명산 | 한국 산악 일반 | 낮음 | 유명사 |'
new_rows = '''| 유명산 | 한국 산악 일반 | 낮음 | 유명사 |
| 남산(경주) | 한국 사찰·산악 일반 | 높음 | 유네스코 남산 불국토 — 방문자 많음 |
| 계방산 | 한국 산악 일반 | 중간 | 오대산국립공원 최고봉, 초원 능선 |
| 두타산 | 한국 산악 일반 | 중간 | 베틀바위·마천루 암릉 |
| 마니산 | 한국 산악 일반 | 중간 | 참성단·삼랑성 |'''
assert s.count(old_rows) == 1, '유명산 행 앵커 실패'
s = s.replace(old_rows, new_rows)
p.write_text(s, encoding='utf-8')
print('PHOTO-ACCURACY: patched (25산, +4 rows)')

# ── deep-info-data.js / -en.js ───────────────────────────────
DI = {
 'namsan': dict(
  note='한국 100대 명산 5차',
  sec=[
   ('book', '입산·예약', [
     ('예약·허가 불필요', '참고', '남산은 별도 예약·허가 없이 등산할 수 있습니다.'),
     ('삼릉 탐방지원센터', '참고', '삼릉 주차장 옆 탐방지원센터에서 안내·화장실을 이용할 수 있습니다.'),
     ('문화재 보호', '필수', '산 전체가 유네스코 세계유산(남산 불국토) 구역 — 석불·탑·절터를 만지거나 낙서하는 행위는 금지입니다.')]),
   ('bus', '교통', [
     ('철도·버스', '참고', 'KTX-이음 경주역 또는 경주시외버스터미널에서 시내버스로 남산 일대(삼릉·통일전 방면) 접근이 일반적입니다. 노선·배차는 이용 전 확인하세요.'),
     ('자가용', '참고', '삼릉 탐방지원센터 주차장을 많이 이용합니다. 성수기 주말은 조기 만찰이 잦습니다.')]),
   ('tent', '숙박', [
     ('경주 시내', '참고', '경주 시내 관광호텔·콘도·게스트하우스가 밀집해 있어 산행 거점으로 좋습니다. 보문관광단지는 차량으로 20~30분 거리입니다.')]),
   ('shield', '안전·비상연락', [
     ('비상 연락', '필수', '산악 사고 시 119로 신고하세요.'),
     ('능선 산행', '권장', '고위봉 방면 능선은 일몰 이후 등산로 식별이 어렵습니다. 헤드램프를 챙기고 일몰 전 하산을 계획하세요.')]),
  ],
  sources=[('유네스코 — 경주역사유적지구', 'https://whc.unesco.org/ko/list/976/'), ('경주시 문화관광', 'https://www.gyeongju.go.kr')],
 ),
 'gyebangsan': dict(
  note='한국 100대 명산 5차',
  sec=[
   ('book', '입산·예약', [
     ('국립공원 탐방', '참고', '오대산국립공원 구역으로 별도 허가 없이 등산할 수 있습니다.'),
     ('통제 확인', '권장', '자연휴식령 지정(연중 여름 기간)·산불조심 기간에는 구간 통제가 있을 수 있으니 이용 전 공단·군 안내를 확인하세요.')]),
   ('bus', '교통', [
     ('자가용', '참고', '운두령 쉼터 주차장과 1100고지 주차장이 주요 출발점입니다. 주말 아침은 조기 만찰이 잦습니다.'),
     ('대중교통', '참고', '평창·횡성 방면 시외버스를 경유해 접근할 수 있으나 구간 배차가 드뭅니다. 이용 전 시간표 확인이 필요합니다.')]),
   ('tent', '숙박', [
     ('진부면·용평 일대', '참고', '용평리조트와 진부면 펜션·민박이 산행 전후 거점으로 널리 쓰입니다.')]),
   ('shield', '안전·비상연락', [
     ('비상 연락', '필수', '산악 사고 시 119로 신고하세요.'),
     ('겨울 산행', '권장', '설경 명소로 겨울 등산객이 많습니다. 아이젠·스파이커와 방풍 장비를 준비하고, 강풍· Blizzard 시에는 일정을 조정하세요.')]),
  ],
  sources=[('오대산국립공원 (국립공원공단)', 'https://www.knps.or.kr'), ('대한민국 구석구석 — 계방산', 'https://korean.visitkorea.or.kr')],
 ),
 'dutasan': dict(
  note='한국 100대 명산 5차',
  sec=[
   ('book', '입산·예약', [
     ('허가 불필요', '참고', '두타산은 별도 예약·허가 없이 등산할 수 있습니다.'),
     ('무릉계 유원지', '참고', '무릉계는 관광지 운영 구간이 있어 요금·주차 체계가 있을 수 있습니다. 이용 전 지자체 안내를 확인하세요.')]),
   ('bus', '교통', [
     ('고속버스', '참고', '동서울터미널에서 동해행 고속버스가 다수 운행합니다. 동해에서 시내버스로 무릉계 방면 접근이 일반적입니다.'),
     ('댓재휴게소', '참고', '삼척 하장면 댓재휴게소(두타로 680)가 최단 코스 출발점입니다. 자가용 접근이 편리합니다.')]),
   ('tent', '숙박', [
     ('동해·삼척 시내', '참고', '동해시·삼척시 숙박시설과 무릉계 인근 민박을 이용할 수 있습니다.')]),
   ('shield', '안전·비상연락', [
     ('비상 연락', '필수', '산악 사고 시 119로 신고하세요.'),
     ('암릉 구간', '필수', '베틀바위·마천루 구간은 암릉이 이어집니다. 우천·강풍·결빙 시에는 통행을 피하고, 낙석 구간에서는 대기하지 마세요.')]),
  ],
  sources=[('삼척시 문화관광', 'https://tour.samcheok.go.kr'), ('동해시 문화관광', 'https://www.dh.go.kr')],
 ),
 'manisan': dict(
  note='한국 100대 명산 5차',
  sec=[
   ('book', '입산·예약', [
     ('국민관광지 운영', '권장', '마니산은 국민관광지로 운영됩니다. 요금·개방시간·참성단 개방 여부는 이용 전 강화군 안내를 확인하세요.')]),
   ('bus', '교통', [
     ('강화 접근', '참고', '강화 버스터미널에서 마니산 방면 시내버스가 있으나 배차 간격이 큽니다. 자가용 이용이 편리합니다.'),
     ('서해안고속도로', '참고', '서울에서 서해안고속도로를 경유해 강화도까지 1시간~1시간 30분 내외로 접근할 수 있습니다.')]),
   ('tent', '숙박', [
     ('강화 읍내', '참고', '강화 읍내의 호텔·게스트하우스를 이용할 수 있으며, 인천·서울에서 당일치기 산행도 일반적입니다.')]),
   ('shield', '안전·비상연락', [
     ('비상 연락', '필수', '산악 사고 시 119로 신고하세요.'),
     ('능선·계단', '권장', '정수사 코스 능선 바위 구간은 결빙 시 통행을 피하세요. 단군로 372계단 하산 시 무릎 부담이 큽니다.')]),
  ],
  sources=[('강화군 — 마니산', 'https://www.ganghwa.go.kr'), ('인천관광', 'https://www.incheonfair.go.kr')],
 ),
}


def render(mid, d, lang):
    if lang == 'en':
        # 영문 데이터는 한국어 항목과 1:1 대응 구조를 유지 (간결 번역)
        bodies = {
         'namsan': [('No reservation or permit needed.', 'Namsan is open to hikers without reservations.'),
                    ('Samneung Trail Center', 'Information and restrooms at the Samneung parking lot.'),
                    ('Heritage protection', 'The whole mountain is a UNESCO World Heritage zone — never touch or mark the remains.')],
         'gyebangsan': [('Park access', 'Inside Odaesan National Park — no permit required.'),
                        ('Check closures', 'Seasonal rest-zone and fire-season closures may apply — check park notices.')],
         'dutasan': [('No permit needed', 'Dutasan is open without reservation.'),
                     ('Mureung Valley', 'The valley is a managed tourist site — check fees and parking with the local government.')],
         'manisan': [('Managed tourist site', 'Manisan operates as a public tourist site — check fees, hours and altar access with Ganghwa County first.')],
        }
    sections = []
    for icon, title, items in d['sec']:
        its = ', '.join(f"{{ h: '{h}', tag: '{tag}', body: '{b}' }}" for h, tag, b in items)
        sections.append(f"{{ icon: '{icon}', title: '{title}', items: [{its}] }}")
    srcs = ', '.join(f"{{ label: '{l}', href: '{h}' }}" for l, h in d['sources'])
    return (f"window.DEEP_INFO['{mid}'] = {{updated:'2026-09 기준',note:'{d['note']}',"
            f"sections:[{', '.join(sections)}],sources:[{srcs}]}};\n")


jp = ROOT / 'assets/js/deep-info-data.js'
s = jp.read_text(encoding='utf-8')
add = '\n/* ── 한국 100대 명산 5차: 남산(경주)·계방산·두타산·마니산 (2026-09 세션 검증) ──\n'
add += ' * 사실 근거: 100대 명산 목록 포함(위키백과 × 산림청 2002 목록), 코스·표고는 공개 산행 기록\n'
add += ' * 및 지자체·공단 안내와 교차 확인. 변동 품목(버스 배차·요금·통제)은 「이용 전 확인」 일반화.\n */\n'
for mid, d in DI.items():
    add += render(mid, d, 'ko') + '\n'
jp.write_text(s.rstrip() + '\n' + add, encoding='utf-8')
print('deep-info-data.js: +4 entries')

pe = ROOT / 'assets/js/deep-info-data-en.js'
s = pe.read_text(encoding='utf-8')
add = '\n/* Korea 100 Famous Mountains, round 5: Namsan (Gyeongju), Gyebangsan, Dutasan, Manisan — KO/EN synced 2026-09. */\n'
EN = {
 'namsan': [('No reservation or permit needed', '참고', 'Namsan is open to hikers without any reservation or permit.'),
            ('Samneung Trail Center', '참고', 'Information desk and restrooms are available at the Samneung parking area.'),
            ('Heritage protection', '필수', 'The entire mountain is a UNESCO World Heritage zone — do not touch or mark the stone remains.')],
 'gyebangsan': [('Park access', '참고', 'Inside Odaesan National Park — no permit required.'),
                ('Check closures', '권장', 'Seasonal rest-zone and fire-season closures may apply — check official notices before your hike.')],
 'dutasan': [('No permit needed', '참고', 'Dutasan is open without any reservation or permit.'),
             ('Mureung Valley', '참고', 'The valley is a managed tourist site — check fees and parking rules before you go.')],
 'manisan': [('Managed tourist site', '권장', 'Manisan operates as a public tourist site — check fees, opening hours and altar access with Ganghwa County first.')],
}

EN_DI = {
 'namsan': dict(
  sec=[
   ('book', 'Entry & Booking', [
     ('No reservation or permit needed', 'Note', 'Namsan is open to hikers without any reservation or permit.'),
     ('Samneung Trail Center', 'Note', 'Information, restrooms and parking are available at the Samneung trail center.'),
     ('Heritage protection', 'Required', 'The whole mountain is a UNESCO World Heritage zone — never touch or mark the stone Buddhas, pagodas or temple sites.')]),
   ('bus', 'Transport', [
     ('Rail & bus', 'Note', 'Take the KTX-Eum to Gyeongju Station or intercity buses to the Gyeongju Terminal, then city buses toward the Namsan area (Samneung / Tongiljeon). Check routes and schedules before travel.'),
     ('By car', 'Note', 'The Samneung trail-center lot is the most used trailhead parking — it fills early on peak-season weekends.')]),
   ('tent', 'Lodging', [
     ('Downtown Gyeongju', 'Note', 'Hotels, condos and guesthouses cluster in central Gyeongju — a convenient base. Bomun tourist district is 20–30 minutes by car.')]),
   ('shield', 'Safety & Emergency', [
     ('Emergency', 'Required', 'In case of mountain accidents call 119.'),
     ('Ridge hikes', 'Recommended', 'The Gowibong-side ridgeline is hard to follow after dark — carry a headlamp and plan to descend before sunset.')]),
  ],
 ),
 'gyebangsan': dict(
  sec=[
   ('book', 'Entry & Booking', [
     ('Park access', 'Note', 'Inside Odaesan National Park — no permit required.'),
     ('Check closures', 'Recommended', 'Seasonal rest-zone (summer) and fire-season closures may restrict sections — check park and county notices before you go.')]),
   ('bus', 'Transport', [
     ('By car', 'Note', 'The Windunderyeong rest-area lot and the 1100 Highlands lot are the main trailheads — both fill early on weekend mornings.'),
     ('Public transport', 'Note', 'Regional buses toward Pyeongchang or Hongcheon get you close, but local connections are infrequent — check timetables in advance.')]),
   ('tent', 'Lodging', [
     ('Jinbu / Yongpyeong area', 'Note', 'Yongpyeong Resort and guesthouses around Jinbu are the usual bases before and after the hike.')]),
   ('shield', 'Safety & Emergency', [
     ('Emergency', 'Required', 'In case of mountain accidents call 119.'),
     ('Winter hiking', 'Recommended', 'Famed for snowscapes — bring crampons/spikes and wind gear, and adjust plans in strong wind or blizzard conditions.')]),
  ],
 ),
 'dutasan': dict(
  sec=[
   ('book', 'Entry & Booking', [
     ('No permit needed', 'Note', 'Dutasan is open without any reservation or permit.'),
     ('Mureung Valley', 'Note', 'Mureung is a managed tourist area — fees and parking rules may apply. Check local-government guidance before visiting.')]),
   ('bus', 'Transport', [
     ('Express bus', 'Note', 'Frequent express buses run from Seoul Dong-Seoul Terminal to Donghae; from town, city buses head toward Mureung Valley.'),
     ('Datjae rest area', 'Note', 'Datjae rest area (680 Duta-ro, Hajang-myeon, Samcheok) is the trailhead for the shortest route — easiest by car.')]),
   ('tent', 'Lodging', [
     ('Donghae & Samcheok towns', 'Note', 'Stay in Donghae or Samcheok, or at guesthouses near Mureung Valley.')]),
   ('shield', 'Safety & Emergency', [
     ('Emergency', 'Required', 'In case of mountain accidents call 119.'),
     ('Crag sections', 'Required', 'The Byeotul Rock and Macheonru sections are continuous crags. Avoid them in rain, strong wind or ice, and never linger under rockfall zones.')]),
  ],
 ),
 'manisan': dict(
  sec=[
   ('book', 'Entry & Booking', [
     ('Managed tourist site', 'Recommended', 'Manisan operates as a public tourist site — check fees, opening hours and whether the Chanseongdan altar is open, with Ganghwa County before your visit.')]),
   ('bus', 'Transport', [
     ('Getting to Ganghwa', 'Note', 'City buses run from Ganghwa Bus Terminal toward Manisan, but services are infrequent — driving is easier.'),
     ('By car', 'Note', 'From Seoul, the West Coast Expressway reaches Ganghwa Island in roughly 1–1.5 hours.')]),
   ('tent', 'Lodging', [
     ('Ganghwa town', 'Note', 'Hotels and guesthouses in Ganghwa town work well; day trips from Incheon or Seoul are also common.')]),
   ('shield', 'Safety & Emergency', [
     ('Emergency', 'Required', 'In case of mountain accidents call 119.'),
     ('Ridge & stairs', 'Recommended', 'Avoid the Jeongsusa ridge rocks when icy. The 372-step Dangun-ro descent is hard on the knees — take it slowly.')]),
  ],
 ),
}
SOURCES = {
 'namsan': [('UNESCO — Gyeongju Historic Areas', 'https://whc.unesco.org/en/list/976/'), ('Gyeongju City', 'https://www.gyeongju.go.kr')],
 'gyebangsan': [('Odaesan National Park (KNPS)', 'https://www.knps.or.kr'), ('Visit Korea — Gyebangsan', 'https://korean.visitkorea.or.kr')],
 'dutasan': [('Samcheok City Tourism', 'https://tour.samcheok.go.kr'), ('Donghae City', 'https://www.dh.go.kr')],
 'manisan': [('Ganghwa County — Manisan', 'https://www.ganghwa.go.kr'), ('Incheon Tourism', 'https://www.incheonfair.go.kr')],
}
for mid, d in EN_DI.items():
    sections = []
    for icon, title, items in d['sec']:
        its = ', '.join(f"{{ h: '{h}', tag: '{tag}', body: '{b}' }}" for h, tag, b in items)
        sections.append(f"{{ icon: '{icon}', title: '{title}', items: [{its}] }}")
    srcs = ', '.join(f"{{ label: '{l}', href: '{h}' }}" for l, h in SOURCES[mid])
    add += (f"window.DEEP_INFO_EN['{mid}'] = {{updated:'2026-09 기준',note:'Korea 100 Famous Mountains round 5',"
            f"sections:[{', '.join(sections)}],sources:[{srcs}]}};\n")
pe.write_text(s.rstrip() + '\n' + add, encoding='utf-8')
print('deep-info-data-en.js: +4 entries (full EN)')
