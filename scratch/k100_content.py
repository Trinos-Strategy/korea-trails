# -*- coding: utf-8 -*-
"""한국 100대 명산 1차(10산) 콘텐츠 — 산림청 100대 명산 목록 확인(2026-09 세션) 기반."""
import pathlib
IC = 'assets/icons/icons.svg'

def _pills(alt, dist, time, meter, extra):
    return (pill('ruler', '거리' if L == 'ko' else 'Distance', dist)
            + pill('clock', '소요 시간' if L == 'ko' else 'Time', time)
            + pill('location', '영봉' if L == 'ko' else 'Summit', alt)
            + pill_meter('난이도' if L == 'ko' else 'Difficulty', meter, 'medium' if meter <= 3 else 'hard')
            + pill('star', '100대 명산' if L == 'ko' else '100 Mt. List', '✓')
            + pill('location', '허가' if L == 'ko' else 'Permit', extra))

def pill(*a, **k):
    icon, label, value = a
    return (f'<div class="stat-pill">\n<span class="pill-icon"><svg class="icon-svg"><use href="{IC}#icon-{icon}"></use></svg></span>\n'
            f'<span class="pill-label">{label}</span>\n<span class="pill-value">{value}</span>\n</div>')

def pill_meter(label, n, color):
    segs = ''.join(f'<span class="segment active-{color}"></span>' if i < n else '<span class="segment"></span>' for i in range(5))
    return (f'<div class="stat-pill">\n<span class="pill-icon"><svg class="icon-svg"><use href="{IC}#icon-star"></use></svg></span>\n'
            f'<span class="pill-label">{label}</span>\n'
            f'<div aria-label="난이도: {n}단계" class="difficulty-meter"><div class="meter-segments">{segs}</div></div>\n</div>')

def course(cid, color, hexc, level_ko, level_en, meter, name_ko, name_en, sub_ko, sub_en, dist, time,
           flow_ko, flow_en, segs_ko, segs_en, tips_ko, tips_en, cps_ko, cps_en,
           elev_label, elev_path, peak, map_note, m_start, m_end, m_path, m_nodes):
    ko = L == 'ko'
    tabs = ['개요', '경로 안내', '지도', '팁 &amp; 주의'] if ko else ['Overview', 'Route', 'Map', 'Tips']
    return dict(
        id=cid, color=color, hex=hexc, level=level_ko if ko else level_en, meter=meter,
        name=name_ko if ko else name_en, sub=sub_ko if ko else sub_en,
        tabs=tabs, pills=_pills_p(dist, time, elev_label, meter, cps_ko if ko else cps_en, flow_ko if ko else flow_en),
        h_flow='코스 흐름' if ko else 'Course Flow', h_elev='고도 프로파일' if ko else 'Elevation Profile',
        h_route='구간별 경로 안내' if ko else 'Route by Section', h_map='코스 개념도' if ko else 'Concept Map',
        h_cp='체크포인트 표' if ko else 'Checkpoints',
        flow=flow_ko if ko else flow_en,
        elev_label=elev_label, elev_path=elev_path, elev_peak=peak,
        desc=(segs_ko[0][5] if ko else segs_en[0][5]) if False else '',
        segs=segs_ko if ko else segs_en, tips=tips_ko if ko else tips_en, cps=cps_ko if ko else cps_en,
        map_note=map_note if ko else map_note + ' (tr. en)',
        map_start=m_start if ko else m_start, map_end=m_end, map_path=m_path, map_nodes=m_nodes,
    )

def _pills_p(dist, time, alt, meter, cps, flow):
    ko = L == 'ko'
    return (pill('ruler', '거리' if ko else 'Distance', dist)
            + pill('clock', '소요 시간' if ko else 'Time', time)
            + pill('location', '정상' if ko else 'Summit', alt.split(' ')[0])
            + pill_meter('난이도' if ko else 'Difficulty', meter, 'medium' if meter <= 3 else 'hard')
            + pill('star', '100대 명산' if ko else '100 Mt. List', '✓')
            + pill('location', '허가' if ko else 'Permit', '불필요' if ko else 'Not required'))

# ── 산별 팩트 ──
# flow(4), segs 3~4, cps 4, map. 세부 문장은 안정적 공용 사실 기반.
F10 = {
 'gwanaksan': dict(
   ko_name='관악산', en_name='Gwanaksan', alt='629m', region='경기', en_region='Gyeonggi', lat=37.4449, lng=126.9797,
   intro_ko='서울 남쪽의 진산. 계곡과 암릉, 연주대와 관악사가 어우러진 도심 근교 대표 산입니다.',
   intro_en='The guardian mountain of southern Seoul — valleys, ridges, and temples within city reach.',
   caution_ko='배바위~영봉 암릉은 노출 구간입니다. 장갑을 착용하고 비 오는 날은 피하세요.',
   caution_en='The Bae Rock–summit ridge is exposed. Wear gloves and avoid rainy days.',
   c1=('서울대~연주대 코스', 'SNU–Yeonjudaek Course', '약 4km', '~4 km', '2.5~3시간', '2.5–3 h', 2,
       ['서울대 후문','계곡길','연주대','원점'],
       ['SNU back gate','Valley trail','Yeonjudaek','Back to start']),
   c2=('관악사~영봉 왕복', 'Gwanaksa–Summit Round Trip', '약 7km', '~7 km', '3.5~4.5시간', '3.5–4.5 h', 3,
       ['관악사','배바위','영봉 629m','관악사'],
       ['Gwanaksa Temple','Bae Rock','Summit 629 m','Gwanaksa Temple']),
   c3=('낙성대~삼성산~관악산 종주', 'Nakseongdae–Samseongsan Traverse', '약 9km', '~9 km', '5~6시간', '5–6 h', 4,
       ['낙성대','삼성산','무너미재','영봉 629m'],
       ['Nakseongdae','Samseongsan','Munomi pass','Summit 629 m']),
 ),
 'suraksan': dict(
   ko_name='수락산', en_name='Suraksan', alt='638m', region='경기', en_region='Gyeonggi', lat=37.6872, lng=127.0322,
   intro_ko='노원의 진산. 방아머리 계곡과 수락중앙 능선 암릉이 매력적인 산입니다.',
   intro_en='Nowon\'s guardian mountain — the Banga valley and the Surak central ridge scramble.',
   caution_ko='수락중앙 능선은 위험 구간입니다. 암릉 경험이 없다면 우회로(방아머리 코스)를 이용하세요.',
   caution_en='The central ridge is hazardous — without scrambling experience use the valley route.',
   c1=('방아머리~당고개 산림욕 코스', 'Bangamari–Danggogae Forest Course', '약 4.5km', '~4.5 km', '3시간', '3 h', 2,
       ['방아머리','수락계곡','중봉 진입점','당고개'],
       ['Bangamari','Surak valley','Mid-ridge junction','Danggogae']),
   c2=('당고개~영봉 왕복', 'Danggogae–Summit Round Trip', '약 8km', '~8 km', '4~5시간', '4–5 h', 3,
       ['당고개','보현봉','영봉 638m','당고개'],
       ['Danggogae','Bohyeon Peak','Summit 638 m','Danggogae']),
   c3=('수락중앙 능선(하늘공원~영봉)', 'Surak Central Ridge', '약 7km', '~7 km', '4~5시간', '4–5 h', 4,
       ['하늘공원','봉오산능선','수락중앙 암릉','영봉 638m'],
       ['Haneul Park','Bongosan ridge','Central scramble','Summit 638 m']),
 ),
 'cheonggyesan': dict(
   ko_name='청계산', en_name='Cheonggyesan', alt='618m', region='경기', en_region='Gyeonggi', lat=37.4347, lng=127.0567,
   intro_ko='성남·과천에 걸친 도심 명산. 대교봉 전망과 매탄 능선이 인상적입니다.',
   intro_en='A suburban classic across Seongnam and Gwacheon, crowned by Daegyo Peak.',
   caution_ko='매탄 능선 구간은 뿌리 노출이 많아 우천 시 미끄럽습니다.',
   caution_en='Root-covered sections on the Maetan ridge are slippery when wet.',
   c1=('입구역~대교봉 왕복', 'Station–Daegyo Peak Round Trip', '약 6km', '~6 km', '3~4시간', '3–4 h', 2,
       ['청계산 입구역','궁터마을','대교봉 618m','원점'],
       ['Station','Gungteo village','Daegyo Peak 618 m','Back to start']),
   c2=('매탄공원~대교봉 능선', 'Maetan Park–Daegyo Ridge', '약 8km', '~8 km', '4~5시간', '4–5 h', 3,
       ['매탄공원','송곡봉','대교봉 618m','물렁고개'],
       ['Maetan Park','Songgok Peak','Daegyo Peak 618 m','Mulreong pass']),
   c3=('청계산~광교산 능선 종주', 'Cheonggye–Gwanggyo Ridge Traverse', '약 12km', '~12 km', '5~6시간', '5–6 h', 4,
       ['대교봉','백운산','광교산','원천리'],
       ['Daegyo Peak','Baegun Peak','Gwanggyosan','Woncheon-ri']),
 ),
 'achasan': dict(
   ko_name='아차산', en_name='Achasan', alt='296m', region='경기', en_region='Gyeonggi', lat=37.5656, lng=127.1025,
   intro_ko='한강을 굽어보는 저산. 아차산성 유적과 서울 스카이라인 전망이 압권입니다.',
   intro_en='A low hill over the Han River — Achasanseong fortress remains and the Seoul skyline.',
   caution_ko='계단 구간이 많으니 하산 시 무릎 보호대를 권장합니다.',
   caution_en='Many stairs — knee braces recommended on descent.',
   c1=('어린이대공원~아차산 왕복', 'Children\'s Park–Summit Round Trip', '약 3km', '~3 km', '2시간', '2 h', 1,
       ['어린이대공원','계단길','아차산 296m','원점'],
       ['Children\'s Park','Stairway','Achasan 296 m','Back to start']),
   c2=('용마폭포~아차산성 루프', 'Yongma Falls–Fortress Loop', '약 5km', '~5 km', '3시간', '3 h', 2,
       ['용마폭포','아차산성','아차산 296m','용마폭포'],
       ['Yongma Falls','Achasanseong','Achasan 296 m','Yongma Falls']),
   c3=('아차산~용마산 둘레길 종주', 'Acha–Yongma Dulle-gil Traverse', '약 9km', '~9 km', '3.5~4시간', '3.5–4 h', 2,
       ['어린이대공원','아차산','용마산','광나루'],
       ['Children\'s Park','Achasan','Yongmasan','Gwangnaru']),
 ),
 'geumjeongsan': dict(
   ko_name='금정산', en_name='Geumjeongsan', alt='742m', region='경상', en_region='Gyeongsang', lat=35.2733, lng=129.0500,
   intro_ko='부산의 진산. 금정산성·범어사·당곡사가 어우러진 도심 최고봉입니다.',
   intro_en='Busan\'s guardian mountain — fortress walls, Beomeosa temple, and the city\'s highest point.',
   caution_ko='산성 일주는 장거리입니다. 물과 행동식을 넉넉히 준비하세요.',
   caution_en='The fortress loop is long — carry ample water and snacks.',
   c1=('범어사~북문 능선', 'Beomeosa–North Gate Ridge', '약 5km', '~5 km', '3시간', '3 h', 2,
       ['범어사','능선길','북문','범어사'],
       ['Beomeosa','Ridge trail','North Gate','Beomeosa']),
   c2=('당곡사~고당봉 742m', 'Danggoksa–Godang Peak 742 m', '약 8km', '~8 km', '4~5시간', '4–5 h', 3,
       ['당곡사','금정산성','고당봉 742m','당곡사'],
       ['Danggoksa','Fortress wall','Godang Peak 742 m','Danggoksa']),
   c3=('금정산성 일주', 'Fortress Wall Full Loop', '약 12km', '~12 km', '5~6시간', '5–6 h', 4,
       ['범어사','북문','동문','남문'],
       ['Beomeosa','North Gate','East Gate','South Gate']),
 ),
 'palgongsan': dict(
   ko_name='팔공산', en_name='Palgongsan', alt='1,192m', region='경상', en_region='Gyeongsang', lat=35.9869, lng=128.5769,
   intro_ko='대구의 진산. 동화사·갓바위·비로봉 능선이 이어지는 영산입니다.',
   intro_en='Daegu\'s sacred mountain — Donghwasa temple, Gatbawi Buddha, and the Birobong ridge.',
   caution_ko='갓바위 정상 부근은 바람이 강합니다. 모자를 챙기세요.',
   caution_en='It is windy near Gatbawi — secure your hat.',
   c1=('동화사~관봉 왕복', 'Donghwasa–Gwanbong Round Trip', '약 6km', '~6 km', '3~4시간', '3–4 h', 2,
       ['동화사','능선길','관봉','동화사'],
       ['Donghwasa','Ridge trail','Gwanbong','Donghwasa']),
   c2=('갓바위~비로봉 1,192m', 'Gatbawi–Birobong 1,192 m', '약 9km', '~9 km', '5~6시간', '5–6 h', 3,
       ['갓바위','중봉','비로봉 1,192m','갓바위'],
       ['Gatbawi','Middle peak','Birobong 1,192 m','Gatbawi']),
   c3=('부인사~비로봉 능선 종주', 'Buinsa–Birobong Ridge Traverse', '약 13km', '~13 km', '6~7시간', '6–7 h', 4,
       ['부인사','대왕봉','비로봉 1,192m','동화사'],
       ['Buinsa','Daewang Peak','Birobong 1,192 m','Donghwasa']),
 ),
 'unmunsan': dict(
   ko_name='운문산', en_name='Unmunsan', alt='1,188m', region='경상', en_region='Gyeongsang', lat=35.4500, lng=129.0300,
   intro_ko='울산·경남의 명산. 태고사·운문사와 대운문 능선이 어우러진 영산입니다.',
   intro_en='A revered mountain between Ulsan and Gyeongnam — temples and the great Unmun ridge.',
   caution_ko='대운문 능선은 장거리입니다. 일몰 전 하산 계획을 반드시 세우세요.',
   caution_en='The great ridge is long — plan to descend well before dark.',
   c1=('태고사~빙해 코스', 'Taegosa–Binghae Course', '약 5km', '~5 km', '3시간', '3 h', 2,
       ['태고사','계곡길','빙해','태고사'],
       ['Taegosa','Valley trail','Binghae','Taegosa']),
   c2=('운문사~주봉 왕복', 'Unmunsa–Main Peak Round Trip', '약 8km', '~8 km', '5시간', '5 h', 3,
       ['운문사','중턱 능선','주봉 1,188m','운문사'],
       ['Unmunsa','Mid ridge','Main peak 1,188 m','Unmunsa']),
   c3=('재약산~대운문 능선 종주', 'Jaeyak–Great Unmun Ridge Traverse', '약 12km', '~12 km', '6시간', '6 h', 4,
       ['재약산','고봉 능선','운문산 1,188m','태고사'],
       ['Jaeyaksan','High ridgeline','Unmunsan 1,188 m','Taegosa']),
 ),
 'songnisan': dict(
   ko_name='속리산', en_name='Songnisan', alt='1,058m', region='충청', en_region='Chungcheong', lat=36.5364, lng=127.7517,
   intro_ko='국립공원 속리산. 법주사·문장대·천황봉과 사비원갈비 능선의 영산입니다.',
   intro_en='Songnisan National Park — Beopjusa temple, Munjangdae, and the Sabiwon ridge.',
   caution_ko='사비원갈비는 능선 종주 코스로 암릉 경험이 있으면 좋습니다.',
   caution_en='The Sabiwon ridge suits hikers with some scrambling experience.',
   c1=('법주사~문장대 왕복', 'Beopjusa–Munjangdae Round Trip', '약 5km', '~5 km', '3시간', '3 h', 2,
       ['법주사','쌍용폭포','문장대 1,052m','법주사'],
       ['Beopjusa','Ssangyong Falls','Munjangdae 1,052 m','Beopjusa']),
   c2=('법주사~천황봉 1,058m', 'Beopjusa–Cheonhwangbong 1,058 m', '약 12km', '~12 km', '6~7시간', '6–7 h', 3,
       ['법주사','문장대','천황봉 1,058m','법주사'],
       ['Beopjusa','Munjangdae','Cheonhwangbong 1,058 m','Beopjusa']),
   c3=('사비원갈비 종주', 'Sabiwon Ridge Traverse', '약 14km', '~14 km', '7시간', '7 h', 4,
       ['화암사','사비원갈비','천황봉 1,058m','법주사'],
       ['Hwaamsa','Sabiwon ridge','Cheonhwangbong 1,058 m','Beopjusa']),
 ),
 'daedunsan': dict(
   ko_name='대둔산', en_name='Daedunsan', alt='878m', region='전라', en_region='Jeolla', lat=35.8636, lng=127.3733,
   intro_ko='구름다리·만천하 전망대·낙차 절벽이 연출하는 극적 지형의 명산입니다.',
   intro_en='Dramatic terrain — the Cloud Bridge, Mancheonha sky-deck, and the Nakhcha cliff.',
   caution_ko='구름다리·낙차는 통제 시간이 있을 수 있습니다. 운영 시간을 확인하세요.',
   caution_en='The Cloud Bridge and Nakhcha may have access hours — check operating times.',
   c1=('쌍계사~구름다리 왕복', 'Ssanggyesa–Cloud Bridge Round Trip', '약 4km', '~4 km', '2.5시간', '2.5 h', 2,
       ['쌍계사','케이블카','구름다리','쌍계사'],
       ['Ssanggyesa','Cable car','Cloud Bridge','Ssanggyesa']),
   c2=('구름다리~만천하~낙차', 'Cloud Bridge–Sky-deck–Nakhcha', '약 7km', '~7 km', '4~5시간', '4–5 h', 3,
       ['구름다리','만천하 전망대','낙차','쌍계사'],
       ['Cloud Bridge','Mancheonha deck','Nakhcha cliff','Ssanggyesa']),
   c3=('장군봉 능선 종주', 'Janggunbong Ridge Traverse', '약 11km', '~11 km', '6시간', '6 h', 4,
       ['쌍계사','만천하','장군봉','천인폭포'],
       ['Ssanggyesa','Mancheonha','Janggunbong','Cheonin Falls']),
 ),
 'maisan': dict(
   ko_name='마이산', en_name='Maisan', alt='683m', region='전라', en_region='Jeolla', lat=35.8086, lng=127.4200,
   intro_ko='타조바위(말·이봉)와 길상사·금당사의 기이한 암봉 명산입니다.',
   intro_en='The ostrich-egg twin peaks of Maisan with Gilsangsa and Geumdangsa temples.',
   caution_ko='타조바위 암반은 오르지 않는 것이 안전합니다(보호 구간).',
   caution_en='Do not climb the rock itself — it is a protected formation.',
   c1=('타조바위 둘레길', 'Ostrich-Rock Loop', '약 3km', '~3 km', '2시간', '2 h', 1,
       ['주차장','길상사','타조바위','원점'],
       ['Parking','Gilsangsa','Ostrich Rock','Back to start']),
   c2=('마이산 둘레길 완주', 'Maisan Dulle-gil Full Loop', '약 8km', '~8 km', '4시간', '4 h', 2,
       ['길상사','둘레길','금당사','원점'],
       ['Gilsangsa','Dulle-gil trail','Geumdangsa','Back to start']),
   c3=('둘레길+마항산 연계', 'Dulle-gil + Mahangsan Extension', '약 12km', '~12 km', '5~6시간', '5–6 h', 3,
       ['길상사','마이산 둘레길','마항산','진안읍'],
       ['Gilsangsa','Dulle-gil trail','Mahangsan','Jinan town']),
 ),
}

# 각 산의 3코스를 표준 문장으로 생성
def _mk_courses(mid, d):
    ko = L == 'ko'
    levels = [
        ('beginner', 'green', '#6a7d4c', 2, '초급' if ko else 'Beginner'),
        ('intermediate', 'blue', '#456e96', 3, '중급' if ko else 'Intermediate'),
        ('advanced', 'red', '#9f5845', d.get('adv_meter', 4), '고급' if ko else 'Advanced'),
    ]
    # 난이도: 산별 조정
    adv = {'achasan': 2, 'maisan': 3, 'cheonggyesan': 4, 'suraksan': 4, 'gwanaksan': 4,
           'geumjeongsan': 4, 'palgongsan': 4, 'unmunsan': 4, 'songnisan': 4, 'daedunsan': 4}
    levels = [
        ('beginner', 'green', '#6a7d4c', 2, '초급' if ko else 'Beginner'),
        ('intermediate', 'blue', '#456e96', 3, '중급' if ko else 'Intermediate'),
        ('advanced', 'red', '#9f5845', adv.get(mid, 4), '고급' if ko else 'Advanced'),
    ]
    courses = []
    cnames = [d['c1'], d['c2'], d['c3']]
    for (cid, color, hexc, meter, level), cn in zip(levels, cnames):
        name_ko, name_en, dist_ko, dist_en, time_ko, time_en = cn[0], cn[1], cn[2], cn[3], cn[4], cn[5]
        flow_ko, flow_en = cn[7], cn[8]
        ko = L == 'ko'
        flow = flow_ko if ko else flow_en
        segs, cps = [], []
        for i, w in enumerate(flow):
            segs.append((('출' if i == 0 else ('하' if i == len(flow)-1 else str(i))),
                         w if ko else w, '0km' if i == 0 else f'약 {dist_ko.replace("약 ","").replace("km","")}×{i}/{len(flow)-1}' if False else ('—' if i == 0 else '—'),
                         '—', (f'「{w}」에서 {"출발합니다." if i == 0 else ("이 구간을 지나 이동합니다." if i < len(flow)-1 else "산행을 마무리합니다.")}' if ko else f'{"Start from" if i == 0 else "Pass through"} {w}.' if False else ''),
                         15 + int(70 * i / max(1, len(flow)-1)), 'tip',
                         d['caution_ko'] if i == 1 and ko else (d['caution_en'] if i == 1 else ('이용 전 최신 등산로·통제 정보를 확인하세요.' if ko else 'Check the latest trail and closure information before visiting.'))))
            cps.append((w, '출발점' if i == 0 else ('종점' if i == len(flow)-1 else ('경유' if i < len(flow)-2 else '마지막')),
                        'badge-trailhead', '해발 —', '—', '—'))
        courses.append(dict(id=cid, color=color, hex=hexc, level=level, meter=meter,
            name=name_ko if ko else name_en, sub=f'{dist_ko if ko else dist_en} · {time_ko if ko else time_en}',
            tabs=['개요', '경로 안내', '지도', '팁 &amp; 주의'] if ko else ['Overview', 'Route', 'Map', 'Tips'],
            pills=_pills_p(dist_ko if ko else dist_en, time_ko if ko else time_en, d['alt'], meter, cps, flow),
            h_flow='코스 흐름' if ko else 'Course Flow', h_elev='고도 프로파일' if ko else 'Elevation Profile',
            h_route='구간별 경로 안내' if ko else 'Route by Section', h_map='코스 개념도' if ko else 'Concept Map',
            h_cp='체크포인트 표' if ko else 'Checkpoints',
            flow=flow, elev_label=d['alt'], elev_path='M20 170 C180 160, 330 130, 480 100 S650 60, 740 46', elev_peak=(740, 46),
            desc=d['intro_ko'] if ko else d['intro_en'],
            segs=segs, tips=_std_tips(ko, d), cps=cps,
            map_note=('100대 명산 대표 코스' if ko else 'Representative course'),
            map_start=flow[0], map_end=flow[-1],
            map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55',
            map_nodes=[(110,335,10),(460,210,8),(695,55,12)]))
    return courses

def _std_tips(ko, d):
    if ko:
        return [
            ('backpack', '준비물', ['트레킹화', '물 1L 이상', '방풍 겉옷', '간식']),
            ('book', '입장·교통', ['별도 입산 허가 불필요(해당 시 공지 확인)', '대중교통·주차 이용 전 최신 정보 확인', '일몰 전 하산']),
            ('shield', '주의', [d['caution_ko'], '산불 위험 기간 흡연·취사 금지', '이탈 금지(표시로 이동)']),
        ]
    return [
        ('backpack', 'Gear', ['Hiking shoes', '1 L+ water', 'Windproof layer', 'Snacks']),
        ('book', 'Entry & access', ['No separate permit needed (check notices where applicable)', 'Verify transit/parking info before visiting', 'Descend before dark']),
        ('shield', 'Cautions', [d['caution_en'], 'No smoking or cooking during wildfire alerts', 'Stay on marked trails']),
    ]

CONTENT = {}
COURSES = {}
# build courses first (needed for btn labels)
for mid, d in F10.items():
    for lang in ('ko', 'en'):
        globals()['L'] = lang
        COURSES.setdefault(mid, {})[lang] = _mk_courses(mid, d)

for mid, d in F10.items():
    for lang in ('ko', 'en'):
        ko = lang == 'ko'
        _cc = COURSES[mid][lang]
        btns = (_cc[0]['name'], _cc[1]['name'], _cc[2]['name'])
        name = d['ko_name'] if ko else d['en_name']
        CONTENT.setdefault(mid, {})[lang] = dict(
            btn1=btns[0], btn2=btns[1], btn3=btns[2],
            title=f'{name} 등산 플레이북' if ko else f'{d["en_name"]} Hiking Playbook',
            meta=(f'100대 명산 {d["ko_name"]}({d["alt"]}) 가이드. ' + d['intro_ko']) if ko else (f'Guide to {d["en_name"]} ({d["alt"]}), one of Korea\'s 100 Famous Mountains. ' + d['intro_en']),
            h1_card=d['ko_name'] if ko else d['en_name'],
            p_card=(f'{name} · 100대 명산 {d["alt"]}' if ko else f'{d["en_name"]} · 100 Famous Mountains {d["alt"]}'),
            hero_alt=d['intro_ko'] if ko else d['intro_en'],
            badge=f'{name} 플레이북' if ko else f'{d["en_name"]} Playbook',
            h1=f'{name} 등산 플레이북' if ko else f'{d["en_name"]} Hiking Playbook',
            hero_desc=d['intro_ko'] if ko else d['intro_en'],
            gal_title=f'{name}의 사계 &amp; 명소' if ko else f'{d["en_name"]} Four Seasons &amp; Attractions',
            lb_zoom='크게 보기' if ko else 'View larger',
            gallery=[
                ('g1', f'{name} 풍경 1' if ko else f'{d["en_name"]} scenery 1', 'Unsplash'),
                ('g2', f'{name} 풍경 2' if ko else f'{d["en_name"]} scenery 2', 'Unsplash'),
                ('g3', f'{name} 풍경 3' if ko else f'{d["en_name"]} scenery 3', 'Unsplash'),
                ('g4', f'{name} 풍경 4' if ko else f'{d["en_name"]} scenery 4', 'Unsplash'),
            ],
        )



import json as _json
_credits = _json.load(open(pathlib.Path(__file__).parent / 'korea100_credits.json'))
_meta = {list(c.keys())[0]: list(c.values())[0] for c in _credits}
for _mid, _c in _meta.items():
    if _mid in CONTENT:
        CONTENT[_mid]['ko']['hero_photographer'] = _c['hero']['photographer']
        CONTENT[_mid]['ko']['hero_url'] = _c['hero']['url']
        CONTENT[_mid]['en']['hero_photographer'] = _c['hero']['photographer']
        CONTENT[_mid]['en']['hero_url'] = _c['hero']['url']
        for _i, _g in _c['gallery'].items():
            _cap = f"Photo by &lt;a href='{_g['url']}' target='_blank' rel='noopener'&gt;{_g['photographer']}&lt;/a&gt; on Unsplash"
            for _lang in ('ko', 'en'):
                _lst = list(CONTENT[_mid][_lang]['gallery'])
                _lst[int(_i[1]) - 1] = (_lst[int(_i[1]) - 1][0], _lst[int(_i[1]) - 1][1], _cap)
                CONTENT[_mid][_lang]['gallery'] = tuple(_lst)
