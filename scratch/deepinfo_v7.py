# -*- coding: utf-8 -*-
"""Q2 — 재빌드 11산 심화 밴드 4블록 승격 (기존 2블록 엔트리 교체). 사실 근거: 세션 리서치(교통·제도는 일반화)."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

DI = {
 'inwangsan': ('인왕산', '한양도성 인왕구간', [
   ('book', '입산·예약', [('입산 자유','참고','별도 예약 없이 등산할 수 있습니다.'), ('성곽 구간 통제','권장','한양도성 일부 구간은 보호·통제될 수 있습니다 — 방문 전 공식 안내를 확인하세요.')]),
   ('bus', '교통', [('지하철 접근','참고','3호선 무악재역·독립문역, 5호선 광화문역 등 여러 역에서 도보 접근이 가능합니다.'), ('자가용','참고','홍지문·사직공원·와룡공원 인근 주차가 협소합니다 — 대중교통을 권장합니다.')]),
   ('tent', '숙박', [('도심 산행','참고','서울 도심 어디서나 당일 산행이 가능합니다.')]),
   ('shield', '안전·비상연락', [('비상 연락','필수','산악 사고 시 119로 신고하세요.'), ('결빙 주의','권장','탕춘대성 급경사 구간은 겨울 결빙이 잦습니다.')]),
  ], 'https://www.seoulcitywall.go.kr'),
 'gajisan': ('가지산', '영남알프스 최고봉', [
   ('book', '입산·예약', [('입산 자유','참고','별도 예약·허가 없이 등산할 수 있습니다.')]),
   ('bus', '교통', [('석남터널 들머리','참고','울산 쪽 최단 들머리는 석남터널 주차장입니다.'), ('통도사 권역','참고','양산 내원계곡 코스는 통도사 관광단지에서 접근합니다 — 주차 요금은 이용 전 확인.')]),
   ('tent', '숙박', [('양산·울산','참고','통도사 관광단지 숙박시설과 울산 시내가 산행 거점입니다.')]),
   ('shield', '안전·비상연락', [('비상 연락','필수','산악 사고 시 119로 신고하세요.'), ('우천 주의','권장','정상부 암반 구간은 우천 시 매우 미끄럽습니다.')]),
  ], 'https://tour.ulsan.go.kr'),
 'hwawangsan': ('화왕산', '창녕 진달래 명산', [
   ('book', '입산·예약', [('입산 자유','참고','별도 예약 없이 등산할 수 있습니다 — 매표소 운영 여부는 이용 전 확인.')]),
   ('bus', '교통', [('창녕 접근','참고','부산·대구에서 창녕행 버스로 접근 후 부곡온천·자하곡 방면 로컬 교통을 이용합니다.'), ('축제기 혼잡','권장','4월 진달래 축제기에는 셔틀·임시 주차가 운영될 수 있습니다 — 군 안내 확인.')]),
   ('tent', '숙박', [('부곡온천','참고','산 자락의 부곡온천 관광지에 호텔·모텔이 있습니다.')]),
   ('shield', '안전·비상연락', [('비상 연락','필수','산악 사고 시 119로 신고하세요.'), ('군락 보호','필수','진달래 군락지는 지정 탐방로 외 출입이 금지됩니다.')]),
  ], 'https://www.changnyeong.go.kr'),
 'unjangsan': ('운장산', '진안·완주 운장대', [
   ('book', '입산·예약', [('입산 자유','참고','별도 예약·허가 없이 등산할 수 있습니다.')]),
   ('bus', '교통', [('들머리 3종','참고','피암목재(최단)·내처사·독자동 들머리가 있습니다. 대중교통 접근이 어려워 자가용이 일반적입니다.'), ('고개 주차','참고','피암목재 주차 공간이 협소합니다.')]),
   ('tent', '숙박', [('진안·완주','참고','진안읍·완주 회덕 일대 숙박이 가깝습니다.')]),
   ('shield', '안전·비상연락', [('비상 연락','필수','산악 사고 시 119로 신고하세요.'), ('겨울 결빙','권장','1,100m대 능선은 겨울 결빙이 빠릅니다.')]),
  ], 'https://www.jinan.go.kr'),
 'biseulsan': ('비슬산', '대구 달성 천왕봉', [
   ('book', '입산·예약', [('입산 자유','참고','별도 예약·허가 없이 등산할 수 있습니다.')]),
   ('bus', '교통', [('유가사 들머리','참고','대표 들머리는 유가사 주차장입니다 — 대구 시내버스 접근 후 도보.'), ('주말 혼잡','권장','봄 철쭉·가을 억새철 주말 주차가 혼잡합니다.')]),
   ('tent', '숙박', [('대구·달성','참고','대구 도심 및 온천 인근 숙박이 가깝습니다.')]),
   ('shield', '안전·비상연락', [('비상 연락','필수','산악 사고 시 119로 신고하세요.'), ('암반 하산','권장','월광봉~대견봉 암반 하산로는 우천 시 위험합니다.')]),
  ], 'https://www.daegu.go.kr'),
 'yeongchwisan': ('영취산', '여수 진달래 명산', [
   ('book', '입산·예약', [('입산 자유','참고','별도 예약 없이 등산할 수 있습니다.')]),
   ('bus', '교통', [('들머리 3종','참고','돌고개·상암초교·중흥동(GS칼텍스 후문) 코스가 여수시 공식 안내됩니다.'), ('축제기 교통','권장','4월 진달래 축제 기간 차량 진입이 통제될 수 있습니다 — 시 안내 확인.')]),
   ('tent', '숙박', [('여수','참고','여수 시내·돌산 관광 숙박이 가깝습니다.')]),
   ('shield', '안전·비상연락', [('비상 연락','필수','산악 사고 시 119로 신고하세요.'), ('군락 보호','필수','진달래 군락지는 포장 능선길에서 벗어나지 마세요.')]),
  ], 'https://www.yeosu.go.kr'),
 'cheongnyangsan': ('청량산', '봉화·안동 기암 명산', [
   ('book', '입산·예약', [('입산 자유','참고','별도 예약 없이 등산할 수 있습니다.')]),
   ('bus', '교통', [('봉화 접근','참고','태강선·중앙선 철도로 봉화역 접근 후 로컬 교통 — 배차는 이용 전 확인.'), ('청량사 주차','참고','청량사 주차장이 대표 들머리입니다.')]),
   ('tent', '숙박', [('봉화·안동','참고','봉화읍·안동 시내 숙박이 거점입니다.')]),
   ('shield', '안전·비상연락', [('비상 연락','필수','산악 사고 시 119로 신고하세요.'), ('기암 낙석','권장','하늘다리·암반 능선은 낙석·추락 위험이 있습니다.')]),
  ], 'https://www.bonghwa.go.kr'),
 'baekamsan': ('백암산', '장성·순창 상왕봉', [
   ('book', '입산·예약', [('국립공원 구역','권장','내장산국립공원 권역 — 공단 탐방 안내를 준수하세요.')]),
   ('bus', '교통', [('백양사·구암사','참고','양 들머리 모두 사찰 주차장을 이용합니다 — 요금은 이용 전 확인.'), ('대중교통','참고','광주·정읍 방면 교통으로 접근 후 로컬 버스 이용.')]),
   ('tent', '숙박', [('백양사·내장산','참고','백양사 일원과 내장산 관광단지 숙박이 가깝습니다.')]),
   ('shield', '안전·비상연락', [('비상 연락','필수','산악 사고 시 119로 신고하세요.'), ('단풍철 혼잡','권장','가을 내장산 단풍철 주차 혼잡이 극심합니다.')]),
  ], 'https://www.knps.or.kr'),
 'yongmunsan': ('용문산', '양평 가섭봉', [
   ('book', '입산·예약', [('입산 자유','참고','별도 예약 없이 등산할 수 있습니다.')]),
   ('bus', '교통', [('용문사 관광단지','참고','대표 들머리는 관광단지 주차장(유료)입니다.'), ('대중교통','참고','용문역(중앙선)에서 택시·버스 접근 — 배차 확인.')]),
   ('tent', '숙박', [('용문·양평','참고','용문면·양평읍의 펜션·모텔이 거점입니다.')]),
   ('shield', '안전·비상연락', [('비상 연락','필수','산악 사고 시 119로 신고하세요.'), ('암능 주의','권장','마당바위~가섭봉 암능은 우천 시 통행을 피하세요.')]),
  ], 'https://www.yangpyeong.go.kr'),
 'yumyeongsan': ('유명산', '가평 휴양림', [
   ('book', '입산·예약', [('휴양림 요금','권장','국립 유명산자연휴양림 경유 시 주차·입장 요금이 있습니다 — 산림청 안내 확인.')]),
   ('bus', '교통', [('휴양림 들머리','참고','주 등반로는 휴양림 주차장에서 시작합니다.'), ('대중교통','참고','가평·청평 방면 교통 후 로컬 접근 — 자가용이 편리합니다.')]),
   ('tent', '숙박', [('휴양림·가평','참고','휴양림 숙박시설과 가평 펜션촌이 가깝습니다.')]),
   ('shield', '안전·비상연락', [('비상 연락','필수','산악 사고 시 119로 신고하세요.'), ('계곡 수위','권장','장마철 계곡코스 횡동 수위 상승에 주의하세요.')]),
  ], 'https://www.forest.go.kr'),
 'ansan': ('안산', '서대문 봉수대', [
   ('book', '입산·예약', [('입산 자유','참고','무료·예약 없이 이용할 수 있습니다.')]),
   ('bus', '교통', [('지하철 최적','참고','3호선 독립문역·무악재역에서 도보 접근이 가장 편합니다.'), ('무장애 자락길','참고','안산자락길 7km는 전국 최초 순환형 무장애 설계입니다.')]),
   ('tent', '숙박', [('도심 산행','참고','서울 도심 어디서나 당일 산행입니다.')]),
   ('shield', '안전·비상연락', [('비상 연락','필수','산악 사고 시 119로 신고하세요.'), ('야간 조명','권장','일부 구간 야간 조명이 부족합니다 — 야경 산행 시 랜턴 필수.')]),
  ], 'https://parks.seoul.go.kr'),
}
TITLES = {'입산·예약': 'Entry & Booking', '교통': 'Transport', '숙박': 'Lodging', '안전·비상연락': 'Safety & Emergency'}


def ko_entry(mid, name, note, secs, src):
    out = []
    for icon, title, items in secs:
        its = ', '.join(f"{{h:'{h}',tag:'{t}',body:'{b}'}}" for h, t, b in items)
        out.append(f"{{icon:'{icon}',title:'{title}',items:[{its}]}}")
    return (f"window.DEEP_INFO['{mid}'] = {{updated:'2026-09 기준',note:'품질 업그레이드 — {note}',"
            f"sections:[{', '.join(out)}],sources:[{{label:'공식 안내',href:'{src}'}}]}};")


def en_entry(mid, name, note, secs, src):
    out = []
    M = {'참고': 'Note', '필수': 'Required', '권장': 'Recommended'}
    B = {
      '별도 예약 없이 등산할 수 있습니다.': 'Open hiking with no reservation required.',
      '별도 예약·허가 없이 등산할 수 있습니다.': 'No reservation or permit required.',
      '무료·예약 없이 이용할 수 있습니다.': 'Free and open, no reservation.',
      '산악 사고 시 119로 신고하세요.': 'For mountain accidents call 119.',
      '한양도성 일부 구간은 보호·통제될 수 있습니다 — 방문 전 공식 안내를 확인하세요.': 'Some Seoul City Wall sections may be closed for protection — check official notices before visiting.',
      '3호선 무악재역·독립문역, 5호선 광화문역 등 여러 역에서 도보 접근이 가능합니다.': 'Several subway stations (line 3 Muakjae/Dongnimmun, line 5 Gwanghwamun) reach the trailheads on foot.',
      '홍지문·사직공원·와룡공원 인근 주차가 협소합니다 — 대중교통을 권장합니다.': 'Parking near Hongjimun, Sajik and Waryong parks is tight — transit is recommended.',
      '서울 도심 어디서나 당일 산행이 가능합니다.': 'A day hike from anywhere in Seoul.',
      '탕춘대성 급경사 구간은 겨울 결빙이 잦습니다.': 'The steep Tangchundaeseong path often ices over in winter.',
      '울산 쪽 최단 들머리는 석남터널 주차장입니다.': 'The shortest Ulsan-side trailhead is the Seoknam Tunnel parking lot.',
      '양산 내원계곡 코스는 통도사 관광단지에서 접근합니다 — 주차 요금은 이용 전 확인.': 'The Naewon Valley route starts from the Tongdosa tourist area — check parking fees.',
      '통도사 관광단지 숙박시설과 울산 시내가 산행 거점입니다.': 'Tongdosa tourist-area stays or Ulsan city make good bases.',
      '정상부 암반 구간은 우천 시 매우 미끄럽습니다.': 'Summit slabs are extremely slick in rain.',
      '별도 예약 없이 등산할 수 있습니다 — 매표소 운영 여부는 이용 전 확인.': 'No reservation needed; check whether the gate is staffed.',
      '부산·대구에서 창녕행 버스로 접근 후 부곡온천·자하곡 방면 로컬 교통을 이용합니다.': 'Buses from Busan/Daegu to Changnyeong, then local transport toward Bugok Hot Springs or Jahagok.',
      '4월 진달래 축제기에는 셔틀·임시 주차가 운영될 수 있습니다 — 군 안내 확인.': 'April festival shuttles and temporary lots may run — check county notices.',
      '산 자락의 부곡온천 관광지에 호텔·모텔이 있습니다.': 'Hotels cluster at Bugok Hot Springs on the mountain foot.',
      '진달래 군락지는 지정 탐방로 외 출입이 금지됩니다.': 'Keep out of the azalea colonies off the designated paths.',
      '피암목재(최단)·내처사·독자동 들머리가 있습니다. 대중교통 접근이 어려워 자가용이 일반적입니다.': 'Trailheads at Piamokjae (shortest), Naechoesa and Doja-dong; driving is the norm.',
      '피암목재 주차 공간이 협소합니다.': 'Parking at Piamokjae pass is limited.',
      '진안읍·완주 회덕 일대 숙박이 가깝습니다.': 'Jinan town or Wanju Hoedeok offer the nearest stays.',
      '1,100m대 능선은 겨울 결빙이 빠릅니다.': 'The 1,100 m ridge ices early in winter.',
      '대표 들머리는 유가사 주차장입니다 — 대구 시내버스 접근 후 도보.': 'The main trailhead is the Yugasa lot — city bus from Daegu then on foot.',
      '봄 철쭉·가을 억새철 주말 주차가 혼잡합니다.': 'Weekend lots jam in azalea spring and silver-grass autumn.',
      '대구 도심 및 온천 인근 숙박이 가깝습니다.': 'Daegu city or nearby hot-spring lodging works well.',
      '월광봉~대견봉 암반 하산로는 우천 시 위험합니다.': 'The Wolgwang–Daegeon rock descent is dangerous in rain.',
      '돌고개·상암초교·중흥동(GS칼텍스 후문) 코스가 여수시 공식 안내됩니다.': 'Dolgae, Sangam School and Jungheung-dong (GS Caltex rear gate) are the official city routes.',
      '4월 진달래 축제 기간 차량 진입이 통제될 수 있습니다 — 시 안내 확인.': 'Vehicle access may be controlled during the April festival — check city notices.',
      '여수 시내·돌산 관광 숙박이 가깝습니다.': 'Yeosu city and Dolsan tourist lodging are close.',
      '진달래 군락지는 포장 능선길에서 벗어나지 마세요.': 'Do not leave the paved ridge path through the colonies.',
      '태강선·중앙선 철도로 봉화역 접근 후 로컬 교통 — 배차는 이용 전 확인.': 'Trains reach Bonghwa station, then local transport — check schedules.',
      '청량사 주차장이 대표 들머리입니다.': 'The Cheongnyangsa temple lot is the main trailhead.',
      '봉화읍·안동 시내 숙박이 거점입니다.': 'Bonghwa town or Andong city are the usual bases.',
      '하늘다리·암반 능선은 낙석·추락 위험이 있습니다.': 'The Sky Bridge and slab ridge carry rockfall and fall risk.',
      '내장산국립공원 권역 — 공단 탐방 안내를 준수하세요.': 'Within Naejangsan National Park — follow KNPS guidance.',
      '양 들머리 모두 사찰 주차장을 이용합니다 — 요금은 이용 전 확인.': 'Both trailheads use temple parking — check fees.',
      '광주·정읍 방면 교통으로 접근 후 로컬 버스 이용.': 'Reach via Gwangju or Jeongeup, then local buses.',
      '백양사 일원과 내장산 관광단지 숙박이 가깝습니다.': 'Stays near Baekyangsa or the Naejangsan tourist area.',
      '가을 내장산 단풍철 주차 혼잡이 극심합니다.': 'Autumn foliage parking is severely congested.',
      '대표 들머리는 관광단지 주차장(유료)입니다.': 'The main trailhead is the paid tourist-area lot.',
      '용문역(중앙선)에서 택시·버스 접근 — 배차 확인.': 'From Yongmun Station (Jungang line) by taxi or bus — check schedules.',
      '용문면·양평읍의 펜션·모텔이 거점입니다.': 'Pensions and motels in Yongmun-myeon or Yangpyeong town.',
      '마당바위~가섭봉 암능은 우천 시 통행을 피하세요.': 'Avoid the Madang Rock–summit crags in rain.',
      '국립 유명산자연휴양림 경유 시 주차·입장 요금이 있습니다 — 산림청 안내 확인.': 'Via the national recreation forest there are parking and entry fees — check Forest Service notices.',
      '주 등반로는 휴양림 주차장에서 시작합니다.': 'The main route starts at the forest lot.',
      '가평·청평 방면 교통 후 로컬 접근 — 자가용이 편리합니다.': 'Transit to Gapyeong/Cheongpyeong then local access — driving is easier.',
      '휴양림 숙박시설과 가평 펜션촌이 가깝습니다.': 'Forest lodging or Gapyeong pensions are nearby.',
      '장마철 계곡코스 횡동 수위 상승에 주의하세요.': 'Watch stream crossings on the valley route in monsoon.',
      '3호선 독립문역·무악재역에서 도보 접근이 가장 편합니다.': 'Lines 3 Dongnimmun or Muakjae stations offer the easiest foot access.',
      '안산자락길 7km는 전국 최초 순환형 무장애 설계입니다.': 'The 7 km jarak-gil is Korea first barrier-free circular trail.',
      '일부 구간 야간 조명이 부족합니다 — 야경 산행 시 랜턴 필수.': 'Some stretches lack night lighting — carry a light for night views.',
    }
    for icon, title, items in secs:
        its = ', '.join(f"{{h:'{h}',tag:'{M.get(t, t)}',body:'{B.get(b, b)}'}}" for h, t, b in items)
        out.append(f"{{icon:'{icon}',title:'{TITLES[title]}',items:[{its}]}}")
    return (f"window.DEEP_INFO_EN['{mid}'] = {{updated:'2026-09 기준',note:'Quality upgrade — {name}',"
            f"sections:[{', '.join(out)}],sources:[{{label:'Official guide',href:'{src}'}}]}};")


for f, render, pre in (('assets/js/deep-info-data.js', ko_entry, "window.DEEP_INFO['"),
                       ('assets/js/deep-info-data-en.js', en_entry, "window.DEEP_INFO_EN['")):
    p = ROOT / f
    s = p.read_text(encoding='utf-8')
    for mid, (name, note, secs, src) in DI.items():
        pat = re.compile(re.escape(pre + mid + "'") + r"\] = \{.*?\};", re.S)
        ms = list(pat.finditer(s))
        entry = render(mid, name, note, secs, src)
        if ms:
            s = s[:ms[0].start()] + entry + s[ms[0].end():]
        else:
            s = s.rstrip() + '\n' + entry + '\n'
    p.write_text(s, encoding='utf-8')
    print(f, '+11 교체')
import subprocess
for f in ('assets/js/deep-info-data.js', 'assets/js/deep-info-data-en.js'):
    r = subprocess.run(['node', '--check', f], capture_output=True, text=True)
    print(f, 'OK' if r.returncode == 0 else r.stderr[:120])
