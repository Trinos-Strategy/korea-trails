# -*- coding: utf-8 -*-
"""deep-info 17엔트리 4블록 승격 — 소금강·청태산·희양산·불암산(세션 검증) + v1 10산·히말라야 3종(기존 게재 사실 재사용+일반화).

사실 근거: 4산은 2026-09-19 세션 리서치(2소스). 히말라야 허가는 세션 검증
(가이드 의무 2023-04·TIMS 약 USD 20·사가르마타/랑탕 NPR 3,000). v1 10산은
사이트 기존 게재 사실 재사용 + 변동 품목 「이용 전 확인」 일반화.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEC_T = {'book': ('입산·예약', 'Entry & Booking'), 'bus': ('교통', 'Transport'),
         'tent': ('숙박', 'Lodging'), 'shield': ('안전·비상연락', 'Safety & Emergency')}
TAG = {'참고': ('참고', 'Note'), '권장': ('권장', 'Recommended'), '필수': ('필수', 'Required')}


def E(mid, name, sections, src_label, src_url):
    """sections: [(icon, [(h_ko, h_en, tag, body_ko, body_en), ...]), ...]"""
    out = {}
    for lang, ix in (('ko', 0), ('en', 1)):
        secs = []
        for icon, items in sections:
            title = SEC_T[icon][0 if lang == 'ko' else 1]
            rendered = []
            for item in items:
                hk = (item[0], item[1]); t = item[2]; bk = (item[3], item[4])
                rendered.append(f"{{h:'{hk[ix]}',tag:'{TAG[t][ix]}',body:'{bk[ix]}'}}")
            its = ', '.join(rendered)
            secs.append(f"{{icon:'{icon}',title:'{title}',items:[{its}]}}")
        key = 'DEEP_INFO' if lang == 'ko' else 'DEEP_INFO_EN'
        note = f'{name} — 4블록 표준(2026-09)' if lang == 'ko' else f'{name} — 4-block standard (2026-09)'
        out[lang] = (f"window.{key}['{mid}'] = {{updated:'2026-09 기준',note:'{note}',"
                     f"sections:[{', '.join(secs)}],"
                     f"sources:[{{label:'{src_label[0 if lang=='ko' else 1]}',href:'{src_url}'}}]}};")
    return out


# 공용 문구
FREE = ('별도 예약·허가 없이 등산할 수 있습니다.', 'Open hiking with no reservation or permit required.')
EMG = ('산악 사고 시 119로 신고하세요.', 'For mountain accidents call 119.')
DAY = ('수도권 접근 도시 산이라 당일 산행이 일반적입니다.', 'A capital-area city hill — day trips are the norm.')

ENTRIES = {
 # ── 4산 (세션 리서치 기반) ──
 'sogeumgang': E('sogeumgang', '소금강', [
   ('book', [
     ('오대산국립공원 구역', '오daesan National Park section'.replace('오dae', 'Odaesan '), '참고',
      '오대산국립공원 소금강지구 — 별도 예약 없이 이용할 수 있습니다. 공단 탐방 안내를 준수하세요.',
      'Inside Odaesan National Park (Sogeumgang district) — open without reservation; follow KNPS guidance.'),
     ('명승 보호', 'Scenic-site protection', '필수',
      '대한민국 명승 제1호 구역 — 바위 오르기·낙서·탐방로 이탈이 금지됩니다.',
      'Korea Scenic Site No. 1 — climbing, carving and leaving the trail are prohibited.')]),
   ('bus', [
     ('진고개 탐방지원센터', 'Jingogae Trail Center', '참고',
      '노인봉 코스는 진고개 탐방지원센터에서 시작합니다. 자가용 접근이 일반적이며 대중교통 배차는 이용 전 확인이 필요합니다.',
      'The Noinbong route starts at Jingogae Trail Center. Driving is the norm; local transit is infrequent — check ahead.'),
     ('계곡 접근', 'Valley access', '참고',
      '소금강계곡(연곡 방면) 입구는 강릉 연곡면 방면에서 접근합니다.',
      'The Sogeumgang valley (Yeon-gok side) is reached from Yeongok-myeon, Gangneung.')]),
   ('tent', [
     ('진부·연곡·둔내', 'Jinbu, Yeongok or Dunnae', '참고',
      '평창 진부면·강릉 연곡면·횡성 둔내면의 펜션·민박이 산행 거점입니다.',
      'Pensions and guesthouses in Jinbu, Yeongok or Dunnae make good bases.')]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('계곡 수위', 'Stream levels', '권장',
      '장마철 계곡 수위가 빠르게 오릅니다 — 우천 시에는 하류 구간만 이용하세요.',
      'Monsoon streams rise fast — keep to lower sections in rain.')]),
  ], ('국립공원공단 — 오대산', 'KNPS — Odaesan'), 'https://www.knps.or.kr'),
 'cheongtaesan': E('cheongtaesan', '청태산', [
   ('book', [
     ('국립자연휴양림', 'National recreation forest', '권장',
      '국립청태산자연휴양림 구역 — 주차·시설 이용 요금이 있을 수 있습니다. 산림청 foresttrip 안내를 이용 전 확인하세요.',
      'Inside the national recreation forest — parking and facility fees may apply; see foresttrip.go.kr before visiting.'),
     ('등산로 6개소', 'Six trails', '참고',
      '6개 등산로의 개방 상태와 난이도가 다릅니다 — 출발 전 휴양림 안내를 확인하세요.',
      'The six trails differ in status and grade — check with the forest office before setting out.')]),
   ('bus', [
     ('둔내 IC', 'Dunnae IC', '참고',
      '둔내 IC에서 차량 약 15분(약 10km) 거리로 영동고속도로 이용이 편리합니다.',
      'About 15 minutes (10 km) from Dunnae IC — easy via the Yeongdong Expressway.'),
     ('대중교통', 'Public transport', '참고',
      '둔내 방면 버스 후 로컬 접근이 필요하나 배차가 드뭅니다 — 자가용이 일반적입니다.',
      'Buses reach the Dunnae area but local connections are rare — driving is the norm.')]),
   ('tent', [
     ('휴양림 숙박시설', 'Forest lodging', '참고',
      '휴양림 숲속집과 둔내면·방림면의 민박·펜션을 이용할 수 있습니다.',
      'Forest cabins and guesthouses in Dunnae or Bangrim are available.')]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('겨울 결빙', 'Winter ice', '권장',
      '1,100m대 산이라 겨울 결빙·적설이 빠릅니다 — 아이젠을 준비하세요.',
      'Above 1,100 m the trails ice and snow early — carry spikes.')]),
  ], ('산림청 foresttrip — 청태산자연휴양림', 'KFS foresttrip — recreation forest'), 'https://www.foresttrip.go.kr'),
 'heuiyangsan': E('heuiyangsan', '희양산', [
   ('book', [('입산 자유', 'Open access', '참고', FREE[0], FREE[1])]),
   ('bus', [
     ('은티마을', 'Eunti village', '참고',
      '문경 가은읍 은티마을이 대표 들머리입니다. 가은역 방면 로컬 교통의 배차는 이용 전 확인이 필요합니다.',
      'Eunti village in Gaeun-eup, Mungyeong is the main trailhead; local transit from Gaeun Station is infrequent — check ahead.'),
     ('대중교통', 'Public transport', '참고',
      '충북 괴산 연풍면 방면 접근도 가능하나 대중교통이 제한적입니다.',
      'Approach via Yeonpung-myeon, Goesan is possible but transit is limited.')]),
   ('tent', [
     ('가은·문경', 'Gaeun and Mungyeong', '참고',
      '가은읍·문경읍의 숙박시설이 거점입니다. 봉암사 일원은 수도원 지역으로 정숙이 필요합니다.',
      'Stay in Gaeun or Mungyeong town. The Bongamsa area is a monastic zone — keep quiet.')]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('화강암 암릉', 'Granite crags', '필수',
      '흑운모 화강암 암릉은 우천·결빙 시 매우 미끄럽습니다 — 장갑을 준비하고 악천후에는 산행을 회수하세요.',
      'The black-mica granite ledges turn treacherous in rain or ice — wear gloves and abandon the plan in bad weather.')]),
  ], ('문경시 문화관광', 'Mungyeong City tourism'), 'https://www.mg21.go.kr'),
 'bulsan': E('bulsan', '불암산', [
   ('book', [
     ('입산 자유', 'Open access', '참고', FREE[0], FREE[1]),
     ('불암산 공영주차장', 'Public lot', '참고',
      '노원구 덕릉로의 공영주차장이 대표 들머리입니다. 주말 오전 만차가 잦습니다.',
      'The public lot on Deungnyeong-ro, Nowon is the main trailhead — it fills on weekend mornings.')]),
   ('bus', [
     ('지하철 접근', 'Subway access', '참고',
      '7호선 마들역·4호선 상계역·6호선 화랑대역 등에서 버스·도보 조합으로 접근합니다.',
      'Reach via line 7 Madul, line 4 Sanggye or line 6 Hwarangdae, then bus and foot.')]),
   ('tent', [('도심 산행', 'Urban hill', '참고', DAY[0], DAY[1])]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('바위 구간', 'Rock steps', '권장',
      '거북바위 등 바위 구간은 장갑을 권장하고 비 온후 미끄러움에 주의하세요.',
      'Wear gloves for the Turtle Rock steps; they are slick after rain.')]),
  ], ('노원구 시설관리', 'Nowon-gu facilities'), 'https://www.nowon.go.kr'),
 # ── v1 10산 (기존 게재 사실 재사용 + 일반화) ──
 'gwanaksan': E('gwanaksan', '관악산', [
   ('book', [('입산 자유', 'Open access', '참고', '서울 도립공원 구역 — ' + FREE[0], 'A Seoul city park — ' + FREE[1])]),
   ('bus', [
     ('지하철 접근', 'Subway access', '참고',
      '2호선 서울대입전역·낙성대역, 4호선 사당역에서 접근합니다. 관악사·연주대 방면 주차는 협소합니다.',
      'Reach via line 2 Seoul National Univ. or Nakseongdae, or line 4 Sadang. Parking near Gwanaksa is tight.')]),
   ('tent', [('도심 산행', 'Urban mountain', '참고', DAY[0], DAY[1])]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('영봉 암릉', 'Yeongbong crags', '필수',
      '영봉 암릉 구간은 추락 사고가 잦은 구간입니다 — 안전선과 지정 등산로를 지키세요.',
      'The Yeongbong ledges see frequent falls — stay behind safety lines on marked trails.')]),
  ], ('서울시 공원', 'Seoul parks'), 'https://parks.seoul.go.kr'),
 'suraksan': E('suraksan', '수락산', [
   ('book', [('입산 자유', 'Open access', '참고', '서울 도립공원 구역 — ' + FREE[0], 'A Seoul city park — ' + FREE[1])]),
   ('bus', [
     ('지하철 접근', 'Subway access', '참고',
      '4호선 수락산역·상계역·장암역에서 접근합니다. 노원골·웅봉 들머리 주차는 이른 아침 확보가 좋습니다.',
      'Reach via line 4 Suraksan, Sanggye or Jangam stations; arrive early for Nowongol parking.')]),
   ('tent', [('도심 산행', 'Urban mountain', '참고', DAY[0], DAY[1])]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('수락중앙 능선 암릉', 'Surak-jungang ledges', '필수',
      '수락중앙 능선 암릉은 추락 위험 구간입니다 — 우천·결빙 시 다른 등산로를 이용하세요.',
      'The central ridge ledges carry fall risk — use other trails in rain or ice.')]),
  ], ('서울시 공원', 'Seoul parks'), 'https://parks.seoul.go.kr'),
 'cheonggyesan': E('cheonggyesan', '청계산', [
   ('book', [('입산 자유', 'Open access', '참고', '도립공원 구역 — ' + FREE[0], 'A city park — ' + FREE[1])]),
   ('bus', [
     ('지하철 접근', 'Subway access', '참고',
      '신분당선 청계산입구역, 4호선 선바위역·대공원역 방면에서 접근합니다. 주말 들머리 주차가 혼잡합니다.',
      'Reach via Sinbundang Cheonggyesan station or line 4 Seonbawi/Grand Park; weekend lots are busy.')]),
   ('tent', [('도심 산행', 'Urban mountain', '참고', DAY[0], DAY[1])]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('대교봉 바위', 'Daegyo Peak rocks', '권장',
      '대교봉 전망 바위 구간은 노출되어 있습니다 — 강풍·우천 시 주의하세요.',
      'The Daegyo Peak lookout rocks are exposed — take care in wind or rain.')]),
  ], ('국립공원공단? 아님 — 과천·성남 도립', 'Seoul-area city parks'), 'https://parks.seoul.go.kr'),
 'achasan': E('achasan', '아차산', [
   ('book', [('입산 자유', 'Open access', '참고', '생활권 도시공원 — ' + FREE[0], 'An urban park — ' + FREE[1])]),
   ('bus', [
     ('지하철 접근', 'Subway access', '참고',
      '5호선 아차산역·광나루역에서 바로 접근하며 한강 공원과 연계 산책이 가능합니다.',
      'Direct access from line 5 Achasan or Gwangnaru stations, with riverside park walks nearby.')]),
   ('tent', [('도심 산행', 'Urban hill', '참고', DAY[0], DAY[1])]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('야간 산행', 'Night hikes', '권장',
      '야경 명소로 야간 산행객이 많습니다 — 조명이 없는 구간에는 랜턴을 지참하세요.',
      'Popular for night views — carry a light for unlit stretches.')]),
  ], ('서울시 공원', 'Seoul parks'), 'https://parks.seoul.go.kr'),
 'geumjeongsan': E('geumjeongsan', '금정산', [
   ('book', [('입산 자유', 'Open access', '참고', '부산 도립공원 구역 — ' + FREE[0], 'A Busan city park — ' + FREE[1])]),
   ('bus', [
     ('지하철 접근', 'Subway access', '참고',
      '1호선 범어사역·두실역·노포역에서 접근합니다. 범어사·세계로 들머리 주차는 혼잡합니다.',
      'Reach via line 1 Beomeosa, Dusil or Nopo stations; trailhead lots are congested.')]),
   ('tent', [
     ('부산 시내', 'Busan city', '참고',
      '온천장·서면 등 부산 시내 숙박이 산행 거점으로 편리합니다.',
      'Hot-spring district and Seomyeon lodging make convenient bases.')]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('능선 바위', 'Ridge rocks', '권장',
      '산성 능선의 바위 구간은 우천 시 미끄럽습니다 — 장갑을 권장합니다.',
      'Fortress-ridge rock steps are slick in rain — gloves recommended.')]),
  ], ('부산시 공원', 'Busan parks'), 'https://www.busan.go.kr'),
 'palgongsan': E('palgongsan', '팔공산', [
   ('book', [('입산 자유', 'Open access', '참고', '대구 도립공원 구역 — ' + FREE[0], 'A Daegu city park — ' + FREE[1])]),
   ('bus', [
     ('동화사 들머리', 'Donghwasa trailhead', '참고',
      '동화사 관광지가 대표 들머리입니다 — 대구 시내버스 접근 후 도보이며 주말 주차가 혼잡합니다.',
      'Donghwasa is the main trailhead — city bus then on foot; weekend parking is busy.')]),
   ('tent', [
     ('대구 시내', 'Daegu city', '참고',
      '대구 시내 숙박에서 당일 산행 동선이 일반적입니다.',
      'Day trips from Daegu city lodging are the norm.')]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('갓바위 암반', 'Gatbawi rocks', '권장',
      '갓바위 암반 계단 구간은 혼잡하고 미끄러울 수 있습니다 — 안전선을 지키세요.',
      'The Gatbawi rock steps are crowded and slippery — stay behind safety lines.')]),
  ], ('대구시 공원', 'Daegu parks'), 'https://www.daegu.go.kr'),
 'unmunsan': E('unmunsan', '운문산', [
   ('book', [('입산 자유', 'Open access', '참고', '울산·경남 군립공원 구역 — ' + FREE[0], 'A county park across Ulsan and Gyeongnam — ' + FREE[1])]),
   ('bus', [
     ('태고사 들머리', 'Taegosa trailhead', '참고',
      '태고사 관광지가 대표 들머리입니다 — 울산·양산 방면 교통 후 로컬 접근이 필요합니다.',
      'Taegosa is the main trailhead — reach via Ulsan or Yangsan then local transport.')]),
   ('tent', [
     ('울산·언양', 'Ulsan and Eonyang', '참고',
      '울산 시내·언양읍 숙박이 산행 거점입니다.',
      'Stay in Ulsan city or Eonyang town.')]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('대운문 능선', 'Daeunmun ridge', '권장',
      '대운문 능선은 바람에 노출되어 있습니다 — 방풍을 준비하세요.',
      'The Daeunmun ridge is exposed — bring a wind shell.')]),
  ], ('울산 시설관리공단', 'Ulsan facilities corp'), 'https://www.uclec.go.kr'),
 'songnisan': E('songnisan', '속리산', [
   ('book', [
     ('국립공원 구역', 'National park', '권장',
      '속리산국립공원 구역 — 국립공원공단 탐방 안내를 준수하세요.',
      'Inside Songnisan National Park — follow KNPS guidance.'),
     ('법주사 들머리', 'Beopjusa trailhead', '참고',
      '법주사 관광지가 대표 들머리입니다 — 주차·문화재 관람 안내를 확인하세요.',
      'Beopjusa is the main trailhead — check parking and temple-visit guidance.')]),
   ('bus', [
     ('대중교통', 'Public transport', '참고',
      '보은읍에서 속리산 방면 버스가 운행합니다 — 배차가 드물어 시간표 확인이 필요합니다.',
      'Buses run from Boeun toward the park but are infrequent — check timetables.')]),
   ('tent', [
     ('속리산 관광단지', 'Park tourist area', '참고',
      '법주사 인근 관광단지 숙박과 보은읍 숙박을 이용할 수 있습니다.',
      'Lodging near Beopjusa or in Boeun town is available.')]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('문장대 암릉', 'Munjangdae ledges', '필수',
      '문장대 암릉은 낙뢰·추락 위험 구간입니다 — 뇌우 시 즉시 하산하세요.',
      'The Munjangdae ledges carry lightning and fall risk — descend at the first storm.')]),
  ], ('국립공원공단 — 속리산', 'KNPS — Songnisan'), 'https://www.knps.or.kr'),
 'daedunsan': E('daedunsan', '대둔산', [
   ('book', [
     ('입산 자유', 'Open access', '참고', '충남 도립공원 구역 — ' + FREE[0], 'A Chungnam provincial park — ' + FREE[1]),
     ('케이블카', 'Cable car', '참고',
      '케이블카 운행 여부·요금은 기상·정비에 따라 변동됩니다 — 이용 전 확인하세요.',
      'Cable-car operation varies with weather and maintenance — check before you go.')]),
   ('bus', [
     ('대중교통', 'Public transport', '참고',
      '대전·계룡시에서 대둔산 방면 버스로 접근합니다 — 배차는 이용 전 확인하세요.',
      'Buses reach the park from Daejeon or Gyeryong — check schedules.')]),
   ('tent', [
     ('대둔산 관광지', 'Park tourist area', '참고',
      '도립공원 관광지 인근 민박·펜션과 금산읍 숙박을 이용할 수 있습니다.',
      'Guesthouses near the park or lodging in Geumsan town are available.')]),
   ('shield', [
     ('비상 연락', 'Emergency', '필수', EMG[0], EMG[1]),
     ('구름다리·전망대', 'Cloud Bridge and deck', '필수',
      '구름다리·만천하 전망대는 강풍 시 통제될 수 있습니다 — 현장 안내를 따르세요.',
      'The Cloud Bridge and Mancheonha deck may close in strong wind — follow on-site notices.')]),
  ], ('충남 도립공원', 'Chungnam provincial park'), 'https://www.chungnam.go.kr'),
 'maisan': E('maisan', '마이산', [
   ('book', [
     ('입산 자유', 'Open access', '참고', '전북 도립공원 구역 — ' + FREE[0], 'A Jeonbuk provincial park — ' + FREE[1]),
     ('타조바위 보호', 'Ostrich-rock protection', '필수',
      '타조바위 쌍봉은 암반 등반이 금지된 보호 대상입니다 — 지정 탐방로만 이용하세요.',
      'Climbing the twin Ostrich Rocks is prohibited — stay on the marked paths.')]),
   ('bus', [
     ('대중교통', 'Public transport', '참고',
      '전주에서 진안 방면 버스로 접근 후 마이산 일원에 닿습니다 — 배차는 이용 전 확인하세요.',
      'Buses run from Jeonju toward Jinan — check schedules.')]),
   ('tent', [
     ('진안읍', 'Jinan town', '참고',
      '진안읍 숙박과 마이산 인근 관광 숙박을 이용할 수 있습니다.',
      'Stay in Jinan town or near the park.')]),
   ('shield', [('비상 연락', 'Emergency', '필수', EMG[0], EMG[1])]),
  ], ('전북 도립공원', 'Jeonbuk provincial park'), 'https://www.jbpolice.go.kr'.replace('police', 'culture')),
 # ── 히말라야 3종 (세션 검증 허가 사실) ──
 'ebc': E('ebc', '에베레스트 BC', [
   ('book', [
     ('사가르마타 국립공원 입장료', 'Sagarmatha NP entry', '필수',
      '외국인 기준 NPR 3,000(약 USD 30)의 입장료가 필요합니다(2025 기준).',
      'Foreign visitors pay NPR 3,000 (about USD 30) entry (as of 2025).'),
     ('가이드 의무', 'Guide mandatory', '필수',
      '2023년 4월부터 외국인 트레커는 등록 가이드 동행이 필수입니다.',
      'Since April 2023 foreign trekkers must travel with a registered guide.'),
     ('TIMS 카드', 'TIMS card', '필수',
      '트레킹 정보관리시스템(TIMS) 등록이 필요합니다 — 독립 트레커 기준 약 USD 20.',
      'TIMS registration is required — about USD 20 for independent trekkers.')]),
   ('bus', [
     ('루클라 비행', 'Lukla flight', '참고',
      '카트만두~루클라 비행이 표준 접근입니다 — 성수기 좌석 확보가 필수입니다.',
      'The Kathmandu–Lukla flight is the standard approach — book well ahead in season.')]),
   ('tent', [
     ('티하우스', 'Teahouses', '참고',
      '루트 전 구간 티하우스(로지) 이용이 일반적입니다 — 성수기 사전 문의를 권장합니다.',
      'Teahouse lodging runs the whole route — book ahead in peak season.')]),
   ('shield', [
     ('고산병 대비', 'Altitude safety', '필수',
      '고산 적응 일정을 확보하고 증상이 나타나면 즉시 하산하세요.',
      'Build acclimatization days and descend immediately if symptoms appear.'),
     ('보험·구조', 'Insurance and rescue', '필수',
      '고산 헬기 구조가 포함된 여행자 보험 가입을 확인하세요.',
      'Confirm travel insurance covering high-altitude helicopter rescue.')]),
  ], ('네팔 정부 트레킹 안내', 'Nepal trekking official info'), 'https://ntb.gov.np'),
 'act': E('act', '안나푸르나 서킷', [
   ('book', [
     ('ACAP 허가', 'ACAP permit', '필수',
      '안나푸르나 보전구역(ACAP) 허가가 필요합니다 — 요금·발급 창구는 이용 전 확인하세요.',
      'An Annapurna Conservation Area Permit is required — check fees and issuance points.'),
     ('가이드 의무', 'Guide mandatory', '필수',
      '2023년 4월부터 외국인 트레커는 등록 가이드 동행이 필수입니다.',
      'Since April 2023 foreign trekkers must travel with a registered guide.'),
     ('TIMS 카드', 'TIMS card', '필수',
      '트레킹 정보관리시스템(TIMS) 등록이 필요합니다.',
      'TIMS registration is required.')]),
   ('bus', [
     ('베시사르 접근', 'Getting to Besisahar', '참고',
      '포카라에서 베시사르(서킷 시작점)까지 육로 이동이 일반적입니다 — 도로 상태가 변동됩니다.',
      'Overland from Pokhara to Besisahar (the circuit start) is standard; road conditions vary.')]),
   ('tent', [
     ('티하우스', 'Teahouses', '참고',
      '루트 전 구간 티하우스 이용이 일반적입니다.',
      'Teahouse lodging runs the whole circuit.')]),
   ('shield', [
     ('토롱라 고도', 'Thorong La altitude', '필수',
      '토롱라 5,416m 통과 전 적응 일정을 확보하고 기상 창을 확인하세요.',
      'Acclimatize before the 5,416 m Thorong La and watch weather windows.'),
     ('보험·구조', 'Insurance and rescue', '필수',
      '고산 구조가 포함된 여행자 보험 가입을 확인하세요.',
      'Confirm insurance covering high-altitude rescue.')]),
  ], ('네팔 정부 트레킹 안내', 'Nepal trekking official info'), 'https://ntb.gov.np'),
 'langtang': E('langtang', '랑탕 밸리', [
   ('book', [
     ('랑탕 국립공원 입장료', 'Langtang NP entry', '필수',
      '랑탕국립공원 입장료(외국인 기준 약 NPR 3,000)가 필요합니다.',
      'Langtang National Park entry (about NPR 3,000 for foreigners) is required.'),
     ('가이드 의무', 'Guide mandatory', '필수',
      '2023년 4월부터 외국인 트레커는 등록 가이드 동행이 필수입니다.',
      'Since April 2023 foreign trekkers must travel with a registered guide.'),
     ('TIMS 카드', 'TIMS card', '필수',
      '트레킹 정보관리시스템(TIMS) 등록이 필요합니다.',
      'TIMS registration is required.')]),
   ('bus', [
     ('사프루벤시 접근', 'Getting to Syabrubesi', '참고',
      '카트만두에서 사프루벤시(들머리)까지 육로 이동이 일반적입니다 — 도로 상태가 변동이 큽니다.',
      'Overland from Kathmandu to Syabrubesi is standard — road conditions vary widely.')]),
   ('tent', [
     ('티하우스', 'Teahouses', '참고',
      '계곡 티하우스 이용이 일반적입니다.',
      'Valley teahouse lodging is standard.')]),
   ('shield', [
     ('비상 연락·보험', 'Emergency and insurance', '필수',
      '고산 구조가 포함된 여행자 보험을 확인하고 우기철 산사태 위험 구간을 피하세요.',
      'Confirm high-altitude rescue insurance and avoid landslide-prone sections in monsoon.')]),
  ], ('네팔 정부 트레킹 안내', 'Nepal trekking official info'), 'https://ntb.gov.np'),
}

for f, key in (('assets/js/deep-info-data.js', 'DEEP_INFO'), ('assets/js/deep-info-data-en.js', 'DEEP_INFO_EN')):
    p = ROOT / f
    s = p.read_text(encoding='utf-8')
    added = 0
    for mid, lines in ENTRIES.items():
        line = lines['ko'] if key == 'DEEP_INFO' else lines['en']
        pat = re.compile(re.escape(f"window.{key}['{mid}']") + r" = \{.*?\};", re.S)
        ms = list(pat.finditer(s))
        if ms:
            s = s[:ms[0].start()] + line + s[ms[0].end():]
        else:
            s = s.rstrip() + '\n' + line + '\n'
        added += 1
    p.write_text(s, encoding='utf-8')
    print(f'{f}: {added}엔트리 적용')

import subprocess
for f in ('assets/js/deep-info-data.js', 'assets/js/deep-info-data-en.js'):
    r = subprocess.run(['node', '--check', str(ROOT / f)], capture_output=True, text=True)
    print(f, 'node --check:', 'OK' if r.returncode == 0 else r.stderr[:150])
