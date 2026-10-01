# -*- coding: utf-8 -*-
"""한국 100대 명산 6차(4산) 콘텐츠 — 대암산·백운산(광양)·신불산·감악산.

사실 근거 (2026-09 세션 검증):
- 100대 명산 목록 포함: 위키백과 「대한민국 100대 명산」 목록 × 산림청(2002) 선정 — 4산 모두 등재 확인.
- 대암산: 표고 약 1,304m(향로봉, 양구관광·나무위키·산행기 — 목록 기재는 1,312.6m),
  용늪 천연기념물 제246호·해발 1,280m 고층습원·람사르 1호, 100% 사전예약제(최소 10일 전)·신분증,
  인제 가아리 코스(차량 14km+도보 왕복 약 3시간)·양구 서흥리 코스(주민안내원) —
  sum.inje.go.kr × yg-eco.kr 공공 소스 교차.
- 백운산(광양): 1,222m, 철쭉 5월 말~6월 초, 휴양림 1코스 2.3km 약 2시간(광양시청 공식),
  내회~한재 2.6km·총 3.9km, 논실 종주 약 14km 약 5시간 — 코스 총정리 블로그 × 산행기 교차.
- 신불산: 1,159m 영남알프스 주봉, 간월재→신불산 1.4km·40분 구간표 × 종주 11.0km 약 5시간 ×
  실측 10.2~13.1km — 배내주차장(울주 상북면).
- 감악산: 674.9m(연천봉), 출렁다리 왕복 4.2km, 일주 6.7km 4시간 11분 실측, 감악사·범륜사·임꺽정봉 —
  산행기 다수 교차. 출렁다리 개방시간은 「이용 전 확인」 일반화.
거리·시간은 「약」 근사 표기 원칙. 좌표: 신불산 위키데이터(35.54, 129.056) — 나머지 근사 좌표.
"""
import sys, json as _json, pathlib as _pl, re

IC = 'assets/icons/icons.svg'
L = 'ko'


def pill(icon, label, value):
    return (f'<div class="stat-pill">\n<span class="pill-icon"><svg class="icon-svg"><use href="{IC}#icon-{icon}"></use></svg></span>\n'
            f'<span class="pill-label">{label}</span>\n<span class="pill-value">{value}</span>\n</div>')


def pill_meter(label, n, color):
    segs = ''.join(f'<span class="segment active-{color}"></span>' if i < n else '<span class="segment"></span>' for i in range(5))
    return (f'<div class="stat-pill">\n<span class="pill-icon"><svg class="icon-svg"><use href="{IC}#icon-star"></use></svg></span>\n'
            f'<span class="pill-label">{label}</span>\n'
            f'<div aria-label="난이도: {n}단계" class="difficulty-meter"><div class="meter-segments">{segs}</div></div>\n</div>')


def seg(no, title, km, time, body, bar, kind, tip_text):
    tip = (f'<div class="{kind}"><svg class="icon-svg"><use href="{IC}#icon-{"warning" if kind=="warn" else "tip"}"></use></svg> {tip_text}</div>')
    return (f'<div class="seg"><div class="seg-head"><div class="seg-no">{no}</div><div><div class="seg-title">{title}</div>'
            f'<div class="acc-meta-chips"><span class="meta-chip"><svg class="icon-svg"><use href="{IC}#icon-ruler"></use></svg> {km}</span>'
            f'<span class="meta-chip"><svg class="icon-svg"><use href="{IC}#icon-clock"></use></svg> {time}</span></div></div><div class="seg-arrow">⌄</div></div>'
            f'<div class="seg-body"><p>{body}</p><div class="bar"><div class="fill" style="width:{bar}%"></div></div>{tip}</div></div>')


def tipcard(icon, title, items):
    lis = ''.join(f'<li>{x}</li>' for x in items)
    return f'<div class="card tipcard"><h2><svg class="icon-svg"><use href="{IC}#icon-{icon}"></use></svg> {title}</h2><ul>{lis}</ul></div>'


def cp(n, name, badge, badge_cls, alt, km, amen):
    return (f'<div class="timeline-item{" start" if n==1 else ""}">\n<div class="timeline-marker">{n}</div>\n<div class="timeline-content">\n'
            f'<div class="timeline-header">\n<span class="checkpoint-name">{name}</span>\n<span class="badge {badge_cls}">{badge}</span>\n</div>\n'
            f'<div class="timeline-meta">\n<span class="meta-item"><svg class="icon-svg"><use href="{IC}#icon-mountain"></use></svg> {alt}</span>\n'
            f'<span class="meta-item"><svg class="icon-svg"><use href="{IC}#icon-ruler"></use></svg> {km}</span>\n</div>\n'
            f'<div class="timeline-features">\n<span class="feature-label">{"Amenities" if L=="en" else "편의시설"}:</span> {amen}\n      </div>\n</div>\n</div>')


def elev_svg(gid, color, label, path_pts, peak_xy):
    (px, py) = peak_xy
    return (f'<svg viewbox="0 0 760 220"><defs><lineargradient id="{gid}" x1="0" x2="0" y1="0" y2="1">'
            f'<stop offset="0%" stop-color="{color}" stop-opacity=".34"></stop><stop offset="100%" stop-color="{color}" stop-opacity=".05"></stop></lineargradient></defs>'
            f'<path d="{path_pts} L740 210 L20 210 Z" fill="url(#{gid})"></path><path d="{path_pts}" fill="none" stroke="{color}" stroke-linecap="round" stroke-width="4"></path>'
            f'<circle cx="{px}" cy="{py}" fill="{color}" r="6"></circle><text fill="{color}" font-size="12" x="{px-150}" y="{py-10}">{label}</text></svg>')


def map_svg(color, note, s_label, e_label, path, nodes):
    ns = ''.join(f'<circle cx="{cx}" cy="{cy}" fill="{color}" r="{r}"></circle>' for cx, cy, r in nodes)
    return (f'<svg viewbox="0 0 760 420"><rect fill="var(--surface2)" height="400" rx="22" width="740" x="10" y="10"></rect>'
            f'<path d="{path}" fill="none" stroke="{color}" stroke-linecap="round" stroke-width="6"></path>{ns}'
            f'<text font-size="12" x="{nodes[0][0]-60}" y="{nodes[0][1]+28}">{s_label}</text>'
            f'<text font-size="12" x="{nodes[-1][0]-160}" y="{nodes[-1][1]-18}">{e_label}</text>'
            f'<text fill="var(--muted)" font-size="12" x="34" y="44">{note}</text></svg>')


def panels(courses):
    out = []
    for i, c in enumerate(courses):
        active = ' active' if i == 0 else ''
        flow = '<span class="arr">→</span>'.join(f'<span class="chip">{x}</span>' for x in c['flow'])
        segs = ''.join(seg(*s) for s in c['segs'])
        tips = ''.join(tipcard(*t) for t in c['tips'])
        cps = ''.join(cp(n + 1, *x) for n, x in enumerate(c['cps']))
        out.append(f'''<section class="panel {c['color']}{active}" id="{c['id']}"><div class="panel-top"><span class="level"><svg class="icon-svg"><use href="{IC}#icon-season"></use></svg> {c['level']}</span><div><div class="panel-name">{c['name']}</div><div class="panel-sub">{c['sub']}</div></div></div><div class="tabs"><button class="tab active" data-tab="overview"><svg class="icon-svg"><use href="{IC}#icon-prep"></use></svg> {c['tabs'][0]}</button><button class="tab" data-tab="route"><svg class="icon-svg"><use href="{IC}#icon-book"></use></svg> {c['tabs'][1]}</button><button class="tab" data-tab="map"><svg class="icon-svg"><use href="{IC}#icon-location"></use></svg> {c['tabs'][2]}</button><button class="tab" data-tab="tips"><svg class="icon-svg"><use href="{IC}#icon-tip"></use></svg> {c['tabs'][3]}</button></div>
<div class="playbook-split-container"><div class="playbook-main-col"><div class="tabpane active" data-pane="overview"><div class="course-stats-summary">
{c['pills']}
</div><div class="section-title"><h2>{c['h_flow']}</h2><div class="line"></div></div><div class="card"><div class="flow">{flow}</div></div><div class="section-title"><h2>{c['h_elev']}</h2><div class="line"></div></div><div class="card elev">{elev_svg('g' + c['id'] + c['color'][:2], c['hex'], c['elev_label'], c['elev_path'], c['elev_peak'])}</div><p class="desc">{c['desc']}</p></div><div class="tabpane" data-pane="route"><div class="section-title"><h2>{c['h_route']}</h2><div class="line"></div></div><div class="segments">{segs}</div></div><div class="tabpane" data-pane="tips"><div class="tips-grid">{tips}</div></div></div><div class="playbook-sidebar-col"><div class="tabpane" data-pane="map"><div class="section-title"><h2>{c['h_map']}</h2><div class="line"></div></div><div class="card map">{map_svg(c['hex'], c['map_note'], c['map_start'], c['map_end'], c['map_path'], c['map_nodes'])}</div><div class="section-title"><h2>{c['h_cp']}</h2><div class="line"></div></div><div class="checkpoint-timeline">
{cps}
</div></div></div></div>
</section>''')
    return '\n'.join(out)



# ── 사실 테이블 (2026-09 세션 검증) ──────────────────────────
F6 = {
 'daeamsan': dict(
  ko_name='대암산', en_name='Daeamsan', alt='1,304m', region='강원', en_region='Gangwon',
  lat=38.098, lng=127.998,
  intro_ko='양구·인제의 「큰 바위산」. 정상 향로봉 일대는 백두대간 조망이 열리고, 해발 1,280m 사면의 용늪은 천연기념물 제246호 고층습원입니다.',
  intro_en='The great rock mountain of Yanggu and Inje. Hyangnobong opens views along the Baekdudaegan ridge, and the Yongneup marsh at 1,280 m is Natural Monument No. 246.',
  permit=('용늪 예약 필수', 'Reservation'),
  courses=[
   dict(id='beginner', color='green', hexc='#6a7d4c', meter=2, level=('초급', 'Beginner'),
    name=('가아리 용늪 생태탐방', 'Gaari Yongneup Eco-tour'),
    dist=('약 6km', '~6 km'), time=('3~4시간', '3–4 h'),
    flow=('가아리 탐방안내소', '차량 이동', '용늪 습지', '탐방안내소'),
    desc=('인제군이 운영하는 용늪 공식 생태탐방. 가아리 탐방안내소에서 차량으로 접근해 고층습원 용늪을 '
          '도보 왕복하는 코스다. 100% 사전예약제(최소 10일 전)이며 도보 왕복 약 3시간으로 안내된다.',
          'The official Inje County eco-tour of Yongneup: vehicle approach from the Gaari information center, then a marsh walk of about three hours round trip. Fully reservation-only (at least 10 days ahead).'),
    segs=[
     (1, ('가아리 탐방안내소 집결', 'Check in at Gaari center'), '—', '30분',
      ('예약 확인과 생태 교육을 받는다. 신분증 필수 지참 — 민통선 내 출입 절차가 있다.',
       'Reservation check and a briefing. Bring ID — the area lies inside the Civilian Control Line.'), 10, 'tip',
      ('예약은 sum.inje.go.kr(인제군 생태관광)에서 최소 10일 전까지.', 'Book at sum.inje.go.kr at least 10 days ahead.')),
     (2, ('차량 이동', 'Vehicle transfer'), '약 14km', '30~40분',
      ('안내소에서 탐방 출발점까지 차량으로 이동한다. 도보 왕복 약 3시간 기준의 짧은 습지 코스다.',
       'A vehicle transfer to the trail start; the marsh walk itself is about three hours round trip.'), 25, 'tip',
      ('탐방 시각 10분 전 도착 원칙 — 늦으면 출발에서 제외될 수 있다.', 'Arrive 10 minutes before departure or you may be excluded.')),
     (3, ('용늪 습지 탐방', 'Yongneup marsh walk'), '약 6km', '2~3시간',
      ('해발 1,280m 고층습원 — 한국 람사르 습지 1호. 북방계·남방계 식물이 공존하는 데크길 탐방이다.',
       'A high moor at 1,280 m — Korea\'s first Ramsar wetland, where northern and southern plants coexist along boardwalks.'), 70, 'warn',
      ('데크길 이탈 금지 — 습지 훼손과 안전에 직결된다.', 'Never leave the boardwalk — it protects both the marsh and you.')),
     (4, ('안내소 복귀', 'Return to the center'), '약 14km', '30~40분',
      ('차량으로 안내소로 복귀하며 대암산 탐방을 마무리한다.',
       'Vehicle back to the center to close the tour.'), 100, 'tip',
      ('인근 파로호 전망과 양구 통일관 등 연계 관광이 가능하다.', 'Pair with Paroho Lake views or the Yanggu Unification Hall.')),
    ],
    cps=[
     ('가아리 탐방안내소', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 250m', '0km', ('안내소·주차', 'Info center, parking')),
     ('용늪', ('핵심', 'Highlight'), 'badge-landmark', '해발 약 1,280m', '왕복 도보', ('데크길·해설', 'Boardwalk, guided')),
     ('가아리 탐방안내소', ('도착', 'Finish'), 'badge-trailhead', '해발 약 250m', '약 6km', ('안내소', 'Info center')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('등산화·물·우천 대비. 습지는 기온이 낮고 습하다.', 'Hiking shoes, water, rain gear — the marsh runs cold and damp.')),
     ('book', ('입산·예약', 'Booking'), ('100% 사전예약제 — 인제군 생태관광(sum.inje.go.kr)에서 최소 10일 전 신청, 신분증 필수.',
      'Fully reservation-based: apply at sum.inje.go.kr at least 10 days ahead; ID required.')),
     ('shield', ('주의', 'Cautions'), ('민통선 내 구역 — 지정 코스·안내원 지시를 따르고 군사시설 촬영은 금지다.',
      'Inside the Civilian Control Line — stay on the guided route; photographing military facilities is prohibited.')),
    ],
    elev_path='M20 185 C150 160, 300 110, 460 75 S640 50, 740 44', elev_peak=(740, 44), elev_label='약 1,280m(용늪)',
    map_note='가아리 용늪 탐방', map_start='가아리', map_end='용늪',
    map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55', map_nodes=[(110, 335, 10), (460, 210, 8), (695, 55, 12)]),
   dict(id='intermediate', color='blue', hexc='#456e96', meter=3, level=('중급', 'Intermediate'),
    name=('서흥리 용늪 생태탐방', 'Seoheung-ri Yongneup Eco-tour'),
    dist=('약 7km', '~7 km'), time=('4~5시간', '4–5 h'),
    flow=('임시 용늪탐방센터', '주민안내원 동반', '용늪·향로봉 사면', '센터'),
    desc=('양구군이 운영하는 서흥리 코스 생태탐방. 임시 대암산용늪탐방센터에서 출발해 주민안내원의 안내로 '
          '용늪 일대를 도는 코스다. 역시 100% 사전예약제(yg-eco.kr)이며 출발 10분 전 도착이 원칙이다.',
          'Yanggu County\'s Seoheung-ri eco-tour: from the temporary Yongneup center, a community guide leads the marsh circuit. Also fully reservation-based (yg-eco.kr); arrive 10 minutes before departure.'),
    segs=[
     (1, ('임시 탐방센터 집결', 'Check in at the center'), '—', '30분',
      ('예약 확인 후 주민안내원 배정을 받는다. 신분증 지참 필수.',
       'Reservation check and guide assignment. Bring photo ID.'), 10, 'tip',
      ('예약은 양구 yg-eco.kr — 인제 코스와 창구가 다르다.', 'Book at yg-eco.kr — a different portal from Inje\'s.')),
     (2, ('주민안내원 동반 산행', 'Guided ascent'), '약 3km', '1.5~2시간',
      ('안내원과 함께 숲길을 오른다. 대암산 특유의 바위 지형이 드러나기 시작한다.',
       'A guided forest climb as the mountain\'s namesake rock terrain appears.'), 45, 'tip',
      ('안내원 설명이 탐방의 핵심 — 앞서가지 않는다.', 'The guide\'s commentary is the point — don\'t race ahead.')),
     (3, ('용늪·향로봉 사면', 'Yongneup and Hyangnobong flank'), '약 1.5km', '1~1.5시간',
      ('고층습원의 사면을 따라 데크길·탐방로로 둘러본다. 습지 경관과 아고산 식물이 핵심 볼거리다.',
       'Boardwalks and trails around the high moor — the marsh scenery and subalpine plants are the highlights.'), 75, 'warn',
      ('습지 진입은 지정 데크길만 가능하다.', 'Enter the marsh only on the designated boardwalks.')),
     (4, ('센터 하산', 'Descent to the center'), '약 3km', '1.5~2시간',
      ('올라온 길로 센터로 돌아온다. 전체 일정은 예약 시 안내 기준을 따른다.',
       'Return by the same route. Follow the schedule given at booking.'), 100, 'tip',
      ('세부 소요시간·운영일은 시즌별로 다르니 이용 전 확인한다.', 'Durations and operating days vary by season — check before booking.')),
    ],
    cps=[
     ('임시 용늪탐방센터', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 400m', '0km', ('센터·주차', 'Center, parking')),
     ('주민안내원 동반 구간', ('경유', 'Waypoint'), 'badge-shelter', '해발 약 800m', '3km', ('해설 탐방', 'Guided')),
     ('용늪', ('핵심', 'Highlight'), 'badge-landmark', '해발 약 1,280m', '4.5km', ('데크길', 'Boardwalk')),
     ('임시 용늪탐방센터', ('도착', 'Finish'), 'badge-trailhead', '해발 약 400m', '약 7km', ('센터', 'Center')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('등산화·방풍·물 1L. 고지대라 여름에도 쌀쌀하다.', 'Boots, wind layer, 1 L water — chilly even in summer.')),
     ('book', ('입산·예약', 'Booking'), ('100% 예약제 — yg-eco.kr에서 신청, 탐방 시각 10분 전 도착 원칙.',
      'Fully reserved via yg-eco.kr; be at the center 10 minutes before departure.')),
     ('shield', ('주의', 'Cautions'), ('산불방제 기간 등 계절별 탐방 제한이 있다 — 예약 전 공지를 확인한다.',
      'Seasonal closures apply (fire-prevention periods) — check notices before booking.')),
    ],
    elev_path='M20 195 C160 175, 320 130, 480 95 S650 60, 740 48', elev_peak=(740, 48), elev_label='약 1,280m(용늪)',
    map_note='서흥리 코스', map_start='탐방센터', map_end='용늪',
    map_path='M110 345 C240 320, 350 270, 460 215 S620 100, 690 60', map_nodes=[(110, 345, 10), (460, 215, 8), (690, 60, 12)]),
   dict(id='advanced', color='red', hexc='#9f5845', meter=4, level=('고급', 'Advanced'),
    name=('향로봉 능선 산행', 'Hyangnobong Ridge Hike'),
    dist=('약 9km', '~9 km'), time=('5~6시간', '5–6 h'),
    flow=('들머리', '바위 능선', '향로봉 1,304m', '하산'),
    desc=('대암산의 정상 향로봉(약 1,304m)을 오르는 일반 등산 능선. 정상에서는 금강산–향로봉–설악산으로 '
          '이어지는 북부 백두대간의 조망이 열린다. 용늪 보호구역은 예약 없이는 진입할 수 없다.',
          'The general hiking ridge to the summit Hyangnobong (~1,304 m), opening the northern Baekdudaegan panorama toward Geumgangsan and Seoraksan. The Yongneup reserve itself is off-limits without a reservation.'),
    segs=[
     (1, ('들머리 → 바위 능선', 'Trailhead → rock ridge'), '약 3km', '1.5~2시간',
      ('「큰 바위산」이라는 이름대로 바위 지형이 이어지는 오르막이다.',
       'The climb lives up to the name — continuous rock terrain on the way up.'), 35, 'warn',
      ('젖은 바위는 매우 미끄럽다 — 우천 다음날은 특히 주의.', 'Wet rock is treacherous, especially the day after rain.')),
     (2, ('바위 능선 → 향로봉', 'Rock ridge → Hyangnobong'), '약 2km', '1.5시간',
      ('능선을 따라 오르면 향로봉. 백두대간 능선이 양쪽으로 펼쳐진다.',
       'The ridge tops out at Hyangnobong with the Baekdudaegan spine unfolding both ways.'), 75, 'tip',
      ('정상부는 바람이 강하다 — 방풍 필수.', 'The summit is windy — wind shell essential.')),
     (3, ('향로봉 정상', 'Hyangnobong summit'), '—', '20~30분',
      ('북부 백두대간 조망의 핵심 — 금강산 방면과 설악 방면 능선이 한눈에 들어온다.',
       'The heart of the panorama: ridgelines toward Geumgangsan and Seoraksan in one view.'), 100, 'warn',
      ('민통선 구역 — 지정 등산로 밖 출입과 군사시설 촬영은 금지다.', 'Civilian Control Line — stay on the marked trail; no photographing military facilities.')),
     (4, ('하산', 'Descent'), '약 4km', '2~2.5시간',
      ('들머리로 하산한다. 일몰 전 산행 마무리가 원칙 — 통제 구역 야간 산행은 만천의 대상이다.',
       'Descend to the trailhead. Finish before dark — night hiking in a controlled zone invites trouble.'), 100, 'tip',
      ('능선에서 용늪 방면 갈림길이 보여도 예약 없이는 진입 금지.', 'Ignore junctions toward Yongneup — entry is reservation-only.')),
    ],
    cps=[
     ('들머리', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 500m', '0km', ('주차 협소', 'Limited parking')),
     ('바위 능선', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 1,000m', '3km', ('암릉 조망', 'Rock ridge views')),
     ('향로봉', ('정상', 'Summit'), 'badge-summit', '약 1,304m', '5km', ('백두대간 조망', 'Baekdudaegan panorama')),
     ('들머리', ('도착', 'Finish'), 'badge-trailhead', '해발 약 500m', '약 9km', ('주차', 'Parking')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·장갑·방풍·물 1.5L·헤드램프.', 'Boots, gloves, wind shell, 1.5 L water, headlamp.')),
     ('book', ('입산·예약', 'Booking'), ('일반 등산로는 별도 예약 없음 단, 용늪 보호구역은 100% 예약제 — 접근 불가.',
      'The general ridge needs no reservation; the Yongneup reserve absolutely does.')),
     ('shield', ('주의', 'Cautions'), ('민통선 내 산행 — 출입 절차와 통제 공지를 사전 확인한다.',
      'A Civilian Control Line hike — confirm access procedures and notices beforehand.')),
    ],
    elev_path='M20 190 C150 170, 300 125, 460 90 S640 55, 740 46', elev_peak=(740, 46), elev_label='1,304m',
    map_note='향로봉 능선', map_start='들머리', map_end='향로봉',
    map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55', map_nodes=[(110, 335, 10), (460, 210, 8), (695, 55, 12)]),
  ]),
 'baegunsan': dict(
  ko_name='백운산', en_name='Baegunsan (Gwangyang)', alt='1,222m', region='전라', en_region='Jeolla',
  lat=35.265, lng=127.621,
  intro_ko='광양·구례의 철쭉 명산 1,222m. 능선 전체가 진분홍 철쭉 군락으로 물드는 5월 말~6월 초 철쭉제로 유명합니다.',
  intro_en='The azalea mountain of Gwangyang and Gurye at 1,222 m — its whole ridge flushes pink in late May to early June for the Azalea Festival.',
  permit=('불필요', 'N/A'),
  courses=[
   dict(id='beginner', color='green', hexc='#6a7d4c', meter=2, level=('초급', 'Beginner'),
    name=('자연휴양림 편백숲 코스', 'Recreation Forest Cypress Trail'),
    dist=('약 2.3km', '~2.3 km'), time=('약 2시간', '~2 h'),
    flow=('휴양림 진입도로', '숯가마터', '제비추리봉'),
    desc=('광양시청이 안내하는 백운산자연휴양림 공식 등산로 1코스. 편백숲을 지나 숯가마터를 거쳐 '
          '제비추리봉에 오르는 가벼운 산책·입문 코스다.',
          'Official trail No. 1 of the Baegunsan Recreation Forest per Gwangyang City: a light walk through cypress groves past the charcoal-kiln site to Jebichuri-bong.'),
    segs=[
     (1, ('휴양림 진입도로 → 숯가마터', 'Forest road → kiln site'), '약 1km', '30분',
      ('편백숲 숲길을 따라 완만하게 오른다.',
       'A gentle climb through the cypress stand.'), 30, 'tip',
      ('휴양림 시설(숲해설·물놀이장 등)과 연계하면 하루 일정이 된다.', 'Pair with forest facilities for a full-day outing.')),
     (2, ('숯가마터 → 제비추리봉', 'Kiln site → Jebichuri-bong'), '약 1.3km', '1~1.5시간',
      ('숲길이 이어지며 제비추리봉에 닿는다. 백운산 입문의 정석 구간이다.',
       'Continuing forest to Jebichuri-bong — the classic introduction to Baegunsan.'), 70, 'tip',
      ('표고차는 크지 않지만 숲이 우거져 습하다.', 'Modest elevation gain but humid under the canopy.')),
     (3, ('제비추리봉 → 휴양림 회귀', 'Return to the forest'), '약 2.3km', '1시간',
      ('온 길을 되돌아 휴양림으로 내려온다.',
       'Retrace to the recreation forest.'), 100, 'tip',
      ('휴양림 주차·이용 요금 체계는 이용 전 확인.', 'Check the forest\'s parking and use fees before you go.')),
    ],
    cps=[
     ('휴양림 진입도로', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 400m', '0km', ('주차장·휴양림 시설', 'Parking, facilities')),
     ('숯가마터', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 550m', '1km', ('유적 조망', 'Historic site')),
     ('제비추리봉', ('봉우리', 'Peak'), 'badge-summit', '해발 약 700m', '2.3km', ('숲 전망', 'Forest views')),
     ('휴양림', ('도착', 'Finish'), 'badge-trailhead', '해발 약 400m', '약 4.6km', ('주차장', 'Parking')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('가벼운 트레킹화·물. 산책 수준의 부담 없는 코스.', 'Light shoes and water — an easy-walking route.')),
     ('book', ('입산', 'Entry'), ('휴양림 이용·주차 요금은 광양시청 안내 기준 — 이용 전 확인.', 'Recreation-forest fees per Gwangyang City notices — check ahead.')),
     ('shield', ('주의', 'Cautions'), ('여름철 계곡·숲길 모기 대비.', 'Bring insect protection for the summer woods.')),
    ],
    elev_path='M20 195 C180 185, 350 150, 520 120 S680 95, 740 90', elev_peak=(520, 120), elev_label='약 700m',
    map_note='휴양림 1코스', map_start='휴양림', map_end='제비추리봉',
    map_path='M110 340 C240 320, 350 275, 460 225 S620 115, 690 80', map_nodes=[(110, 340, 10), (460, 225, 8), (690, 80, 12)]),
   dict(id='intermediate', color='blue', hexc='#456e96', meter=3, level=('중급', 'Intermediate'),
    name=('내회~매봉~한재~정상 왕복', 'Naeroe–Maebong–Hanjae Summit Loop'),
    dist=('약 4km', '~4 km'), time=('2~3시간', '2–3 h'),
    flow=('내회 들머리', '매봉', '한재', '백운산 1,222m'),
    desc=('내회 마을에서 매봉·한재를 거쳐 정상으로 이르는 효율적인 왕복 코스. 블로그 총정리 기준 '
          '내회→한재 2.6km, 총 약 3.9km·약 2시간대로 안내된다.',
          'An efficient out-and-back from Naeroe village past Maebong and Hanjae pass to the summit — about 3.9 km and just over two hours per Korean trail round-ups.'),
    segs=[
     (1, ('내회 → 매봉', 'Naeroe → Maebong'), '약 1km', '30~40분',
      ('마을 뒤 숲길로 오른다. 완만한 시작이다.',
       'A gentle start on the forest track behind the village.'), 25, 'tip',
      ('내회 들머리 주차는 좁다 — 철쭉철 혼잡 각오.', 'Naeroe parking is tight — expect crowding in azalea season.')),
     (2, ('매봉 → 한재', 'Maebong → Hanjae'), '약 1.6km', '40~50분',
      ('능선에 붙어 한재(고개)까지 이어진다. 철쭉 군락이 본격적으로 나타난다.',
       'Join the ridge to Hanjae pass as the azalea colonies thicken.'), 55, 'tip',
      ('철쭉은 함부로 꺾지 않는다 — 보호 구역이다.', 'Never pick the azaleas — the colonies are protected.')),
     (3, ('한재 → 백운산 정상', 'Hanjae → summit'), '약 1.3km', '40~50분',
      ('정상 1,222m까지 마지막 오름. 정상에서 섬진강·지리산 능선 조망이 열린다.',
       'The final pitch to the 1,222 m summit opens views over the Seomjin River and the Jirisan ridgelines.'), 90, 'warn',
      ('철쭉철 주말 정상 주변 인파 혼잡 — 대기하며 이동.', 'Summit crowding on festival weekends — be patient.')),
     (4, ('정상 → 내회 하산', 'Summit → Naeroe descent'), '약 3.9km', '1.5시간',
      ('온 길을 되돌아 내려온다.', 'Descend the way you came.'), 100, 'tip',
      ('5월 말~6월 초 철쭉제 기간은 이른 아침 산행을 권한다.', 'Hike early during the late-May–early-June festival.')),
    ],
    cps=[
     ('내회 들머리', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 450m', '0km', ('마을 주차 협소', 'Limited village parking')),
     ('매봉', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 750m', '1km', ('없음', 'None')),
     ('한재', ('경유', 'Waypoint'), 'badge-shelter', '해발 약 900m', '2.6km', ('갈림길', 'Junction')),
     ('백운산', ('정상', 'Summit'), 'badge-summit', '1,222m', '3.9km', ('철쭉·조망', 'Azaleas, panorama')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 1L·봄철 자외선 대비.', 'Boots, 1 L water, spring sun protection.')),
     ('book', ('입산', 'Entry'), ('별도 예약·허가 불필요.', 'No reservation or permit needed.')),
     ('shield', ('주의', 'Cautions'), ('철쭉철 주말 도로·주차 혼잡이 극심하다 — 대중교통·카풀 권장.',
      'Festival-weekend traffic is severe — carpool or use transit.')),
    ],
    elev_path='M20 190 C160 175, 300 135, 460 95 S640 55, 740 46', elev_peak=(740, 46), elev_label='1,222m',
    map_note='내회 코스', map_start='내회', map_end='정상',
    map_path='M110 340 C230 315, 340 265, 450 210 S620 95, 690 58', map_nodes=[(110, 340, 10), (450, 210, 8), (690, 58, 12)]),
   dict(id='advanced', color='red', hexc='#9f5845', meter=4, level=('고급', 'Advanced'),
    name=('논실~한재~신선대~정상~억불봉 종주', 'Nonsil–Hanjae–Summit–Eokbulbong Traverse'),
    dist=('약 14km', '~14 km'), time=('약 5시간', '~5 h'),
    flow=('논실', '한재', '신선대', '백운산 1,222m', '995봉', '억불봉'),
    desc=('백운산 주능선을 종주하는 대표 장거리 코스. 논실에서 한재·신선대를 지나 정상 1,222m에 오른 뒤 '
          '995봉을 거쳐 억불봉(헬기장)까지 이어진다. 공개 코스 총정리 기준 약 14km·약 5시간.',
          'The full Baegunsan ridge: Nonsil past Hanjae and Seonseondae to the 1,222 m summit, then over the 995 peak to Eokbulbong helipad — about 14 km and five hours per Korean route guides.'),
    segs=[
     (1, ('논실 → 한재', 'Nonsil → Hanjae'), '약 5km', '2시간',
      ('들머리에서 완만하게 시작해 능선으로 오른다. 종주의 체력 배분이 시작되는 구간.',
       'A gentle start climbs to the ridge — pacing begins here.'), 35, 'tip',
      ('일찍 출발해 정상 통과를 오전에 마치는 편이 안전하다.', 'Start early enough to top out before midday.')),
     (2, ('한재 → 신선대 → 정상', 'Hanjae → Seonseondae → summit'), '약 3.5km', '1.5시간',
      ('신선대 전망을 지나 백운산 정상 1,222m. 철쭉 능선의 백미다.',
       'Past the Seonseondae viewpoint to the summit — the best of the azalea ridge.'), 70, 'warn',
      ('바위 전망대 구간은 우천 시 미끄럽다.', 'Rock viewpoints are slick when wet.')),
     (3, ('정상 → 995봉', 'Summit → 995 peak'), '약 2.5km', '50분',
      ('정상 이후 내림·오름이 반복된다. 철쭉 군락이 능선을 따라 이어진다.',
       'Rolling ups and downs through continuous azalea colonies.'), 80, 'tip',
      ('995봉 무렵 다리 피로가 온다 — 행동식 보충.', 'Refuel around the 995 peak as fatigue sets in.')),
     (4, ('995봉 → 억불봉', '995 peak → Eokbulbong'), '약 3km', '1시간',
      ('억불봉 헬기장에서 종주 마무리. 하산로를 연결해 귀가한다.',
       'Finish at the Eokbulbong helipad and link a descent trail out.'), 100, 'warn',
      ('종주는 원점회귀가 아니다 — 하산 들머리별 귀가 동선을 미리 확인한다.', 'Point-to-point — plan the exit trailhead and transport in advance.')),
    ],
    cps=[
     ('논실', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 300m', '0km', ('마을 주차', 'Village parking')),
     ('한재', ('경유', 'Waypoint'), 'badge-shelter', '해발 약 900m', '5km', ('갈림길', 'Junction')),
     ('백운산', ('정상', 'Summit'), 'badge-summit', '1,222m', '8.5km', ('철쭉·조망', 'Azaleas, panorama')),
     ('995봉', ('경유', 'Waypoint'), 'badge-landmark', '해발 995m', '11km', ('능선 전망', 'Ridge views')),
     ('억불봉', ('도착', 'Finish'), 'badge-trailhead', '해발 약 900m', '약 14km', ('헬기장 광장', 'Helipad clearing')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 2L·점심·헤드램프 — 하루 종주 구성.', 'Boots, 2 L water, lunch, headlamp — a full-day traverse.')),
     ('book', ('입산', 'Entry'), ('별도 예약·허가 불필요.', 'No reservation or permit needed.')),
     ('shield', ('주의', 'Cautions'), ('봄 철쭉철·가을 단풍철 혼잡 — 종주는 평일을 권한다.',
      'Crowded in azalea and foliage seasons — weekdays are best for the traverse.')),
    ],
    elev_path='M20 180 C140 160, 250 120, 400 80 S560 60, 660 55 S710 90, 740 110', elev_peak=(660, 55), elev_label='1,222m',
    map_note='백운산 종주', map_start='논실', map_end='억불봉',
    map_path='M120 340 C240 300, 350 240, 470 190 S630 90, 690 60', map_nodes=[(120, 340, 10), (470, 190, 8), (690, 60, 12)]),
  ]),
 'sinbulsan': dict(
  ko_name='신불산', en_name='Sinbulsan', alt='1,159m', region='경상', en_region='Gyeongsang',
  lat=35.541, lng=129.061,
  intro_ko='영남알프스의 주봉 1,159m. 간월재~정상의 광활한 억새평원과 배내골 들머리의 능선 산행으로 유명합니다.',
  intro_en='The high point of the Yeongnam Alps at 1,159 m — famed for the vast silver-grass plateau from Ganwoljae pass to the summit, reached from the Baenaegol valley.',
  permit=('불필요', 'N/A'),
  courses=[
   dict(id='beginner', color='green', hexc='#6a7d4c', meter=2, level=('초급', 'Beginner'),
    name=('간월재~신불산 왕복', 'Ganwoljae–Sinbulsan Round Trip'),
    dist=('약 4km', '~4 km'), time=('2~3시간', '2–3 h'),
    flow=('배내주차장', '간월재', '억새평원', '신불산 1,159m'),
    desc=('신불산의 정수를 가장 짧게 맛보는 코스. 간월재에서 정상까지 1.4km·약 40분 거리로, '
          '왕복 산행에 억새평원 전경이 담긴다.',
          'The shortest taste of Sinbulsan\'s essence: 1.4 km and about 40 minutes from Ganwoljae pass to the summit, round-tripping through the silver-grass plateau.'),
    segs=[
     (1, ('배내주차장 → 간월재', 'Baenae parking → Ganwoljae'), '약 0.6km', '15~20분',
      ('배내2공영주차장(만차 시 배내1)에서 간월재까지 접근한다.',
       'From Baenae Lot 2 (Lot 1 when full) up to the pass.'), 20, 'tip',
      ('주차장은 배내골 일대 — 억새철 아침 만차.', 'The lots fill early in silver-grass season.')),
     (2, ('간월재 → 억새평원', 'Ganwoljae → silver-grass plateau'), '약 0.7km', '20분',
      ('간월재를 오르면 광활한 억새평원이 펼쳐진다.',
       'Climb from the pass onto the vast plateau.'), 55, 'tip',
      ('가을 억새철 사진 촬영지로 최고.', 'Prime photo ground in autumn.')),
     (3, ('억새평원 → 신불산 정상', 'Plateau → summit'), '약 0.7km', '20분',
      ('완만한 능선길로 신불산 1,159m에 오른다.',
       'A gentle ridge to the 1,159 m summit.'), 85, 'tip',
      ('정상은 트인 능선 — 바람이 강하다.', 'The open summit is windy.')),
     (4, ('정상 → 간월재·주차장 하산', 'Summit → descent'), '약 1.3km', '40분',
      ('온 길로 내려와 주차장으로 복귀한다.',
       'Return by the same route to the lot.'), 100, 'tip',
      ('시간 여유 시 간월산 방면 조망 후 복귀.', 'If time allows, peek toward Ganwolsan before returning.')),
    ],
    cps=[
     ('배내주차장', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 600m', '0km', ('공영주차장·화장실', 'Public lots, restrooms')),
     ('간월재', ('경유', 'Waypoint'), 'badge-shelter', '해발 약 900m', '0.6km', ('안부', 'Pass')),
     ('억새평원', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 1,000m', '1.3km', ('평원 경관', 'Plateau views')),
     ('신불산', ('정상', 'Summit'), 'badge-summit', '1,159m', '2km', ('영남알프스 조망', 'Yeongnam Alps panorama')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 1L·바람막이 — 능선은 항상 바람이 분다.', 'Boots, 1 L water, windbreaker — the ridge is always breezy.')),
     ('book', ('입산', 'Entry'), ('별도 예약·허가 불필요.', 'No reservation or permit needed.')),
     ('shield', ('주의', 'Cautions'), ('가을 억새철 주말 주차·산행로 혼잡 — 아침 일찍.', 'Autumn weekends jam the lots and trails — go early.')),
    ],
    elev_path='M20 185 C170 165, 320 120, 480 85 S650 50, 740 42', elev_peak=(740, 42), elev_label='1,159m',
    map_note='간월재 왕복', map_start='배내주차장', map_end='신불산',
    map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55', map_nodes=[(110, 335, 10), (460, 210, 8), (695, 55, 12)]),
   dict(id='intermediate', color='blue', hexc='#456e96', meter=3, level=('중급', 'Intermediate'),
    name=('배내고개~간월산~간월재~신불산 종주', 'Baenaegogae–Ganwolsan–Sinbulsan Traverse'),
    dist=('약 11km', '~11 km'), time=('약 5시간', '~5 h'),
    flow=('배내고개', '배내봉', '간월산', '간월재', '신불산 1,159m'),
    desc=('영남알프스의 대표 종주. 배내고개에서 배내봉(1.2km·30분)·간월산(2.8km·60분)을 지나 '
          '간월재(0.8km·15분)를 거쳐 신불산(1.4km·40분)에 이른다 — 공개 구간표 기준 약 11km·약 5시간.',
          'The classic Yeongnam Alps traverse: Baenaegogae past Baenaebong (1.2 km/30 min) and Ganwolsan (2.8 km/60 min) over Ganwoljae (0.8 km/15 min) to Sinbulsan (1.4 km/40 min) — about 11 km and five hours per published segment tables.'),
    segs=[
     (1, ('배내고개 → 배내봉', 'Baenaegogae → Baenaebong'), '1.2km', '30분',
      ('주차장에서 능선으로 붙는 짧은 오름.',
       'A short pitch from the trailhead lot to the ridge.'), 25, 'tip',
      ('배내고개 주차 혼잡 — 억새철 특히.', 'The lot crowds in silver-grass season.')),
     (2, ('배내봉 → 간월산', 'Baenaebong → Ganwolsan'), '2.8km', '60분',
      ('암릉과 숲길이 반복되는 구간. 간월산 정상을 지난다.',
       'Alternating crags and forest across Ganwolsan.'), 55, 'warn',
      ('암릉 구간은 우천 시 위험.', 'Crags turn risky in rain.')),
     (3, ('간월산 → 간월재', 'Ganwolsan → Ganwoljae'), '0.8km', '15분',
      ('안부로 내려섰다가 억새평원이 시작되는 갈림길.',
       'Down to the pass where the plateau begins.'), 70, 'tip',
      ('간월재에서 신불산 왕복 코스와 합류.', 'The short route joins here.')),
     (4, ('간월재 → 신불산', 'Ganwoljae → Sinbulsan'), '1.4km', '40분',
      ('억새평원 능선의 완만한 오름으로 신불산 1,159m 완등.',
       'A gentle plateau climb to the 1,159 m summit.'), 90, 'tip',
      ('정상 후 하산은 배내골 방면 또는 원점회귀 — 사전 계획.', 'Plan the exit (Baenaegol descent or return) before you top out.')),
    ],
    cps=[
     ('배내고개', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 650m', '0km', ('주차장', 'Parking')),
     ('배내봉', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 930m', '1.2km', ('암릉 조망', 'Crag views')),
     ('간월산', ('경유', 'Waypoint'), 'badge-summit', '해발 약 1,019m', '4km', ('정상 조망', 'Summit views')),
     ('간월재', ('경유', 'Waypoint'), 'badge-shelter', '해발 약 900m', '4.8km', ('갈림길', 'Junction')),
     ('신불산', ('정상', 'Summit'), 'badge-summit', '1,159m', '6.2km', ('억새평원 조망', 'Plateau panorama')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 1.5L·점심·방풍.', 'Boots, 1.5 L water, lunch, wind shell.')),
     ('book', ('입산', 'Entry'), ('별도 예약·허가 불필요.', 'No reservation or permit needed.')),
     ('shield', ('주의', 'Cautions'), ('간월산 구간 암릉 — 우천·강풍 시 통보 없이 난이도가 오른다.',
      'Ganwolsan\'s crags jump a grade in wind or rain.')),
    ],
    elev_path='M20 185 C140 165, 260 125, 400 95 S540 85, 620 55 S700 60, 740 48', elev_peak=(620, 55), elev_label='1,159m',
    map_note='영남알프스 종주', map_start='배내고개', map_end='신불산',
    map_path='M120 335 C240 310, 350 255, 470 200 S630 95, 690 60', map_nodes=[(120, 335, 10), (470, 200, 8), (690, 60, 12)]),
   dict(id='advanced', color='red', hexc='#9f5845', meter=4, level=('고급', 'Advanced'),
    name=('배내고개~영축산~신불산~간월산 능선 연계', 'Ridge Link-up via Yeongchuksan'),
    dist=('약 13km', '~13 km'), time=('약 5시간', '~5 h'),
    flow=('배내고개', '영축산', '신불산 1,159m', '간월산', '배내고개'),
    desc=('영축산을 더해 영남알프스 능선을 길게 잇는 연계 코스. 공개 실측 기록 기준 약 13.1km·휴식 '
          '제외 약 4시간 47분. 능선 노출 구간이 길어 기상 영향이 크다.',
          'A longer link-up adding Yeongchuksan to the ridge — about 13.1 km and 4h47m of moving time per public GPS logs. Long exposed ridgelines make weather the deciding factor.'),
    segs=[
     (1, ('배내고개 → 영축산', 'Baenaegogae → Yeongchuksan'), '약 4km', '1.5시간',
      ('영축산 방면 능선으로 붙는다. 숲길과 바위가 섞인 오름.',
       'Onto the Yeongchuksan ridge — mixed forest and rock.'), 35, 'warn',
      ('안부 이탈로가 드물다 — 진행 전 갈림 확인.', 'Few escape routes — check junctions as you go.')),
     (2, ('영축산 → 신불산', 'Yeongchuksan → Sinbulsan'), '약 5km', '2시간',
      ('영축산을 지나 신불산 주능선에 합류한다.',
       'Past Yeongchuksan onto the main Sinbulsan ridge.'), 65, 'tip',
      ('구간이 길다 — 물을 나눠 마신다.', 'A long leg — ration your water.')),
     (3, ('신불산 → 간월산', 'Sinbulsan → Ganwolsan'), '약 2.2km', '1시간',
      ('억새평원을 지나 간월산까지 능선 산행.',
       'Across the plateau to Ganwolsan.'), 85, 'warn',
      ('암릉 구간 재통과 — 컨디션 점검.', 'The crags again — check your condition.')),
     (4, ('간월산 → 배내고개 하산', 'Ganwolsan → descent'), '약 2km', '1시간',
      ('배내고개로 내려와 원점 회귀한다.',
       'Descend to Baenaegogae for a loop finish.'), 100, 'tip',
      ('일몰 여유를 두고 하산 — 능선은 바람이 심해 체온이 빠진다.', 'Descend with daylight to spare — the ridge drains body heat fast.')),
    ],
    cps=[
     ('배내고개', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 650m', '0km', ('주차장', 'Parking')),
     ('영축산', ('경유', 'Waypoint'), 'badge-summit', '해발 약 1,083m', '4km', ('능선 조망', 'Ridge views')),
     ('신불산', ('정상', 'Summit'), 'badge-summit', '1,159m', '9km', ('억새평원', 'Plateau')),
     ('간월산', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 1,019m', '11.2km', ('암릉', 'Crags')),
     ('배내고개', ('도착', 'Finish'), 'badge-trailhead', '해발 약 650m', '약 13km', ('주차장', 'Parking')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 2L·헤드램프·방풍·장갑.', 'Boots, 2 L water, headlamp, wind shell, gloves.')),
     ('book', ('입산', 'Entry'), ('별도 예약·허가 불필요.', 'No reservation or permit needed.')),
     ('shield', ('주의', 'Cautions'), ('장거리 노출 능선 — 뇌우·강풍 예보 시 취소가 정답.',
      'Long exposed ridge — cancel on storm or gale forecasts.')),
    ],
    elev_path='M20 185 C150 160, 280 115, 420 85 S560 60, 660 55 S710 85, 740 105', elev_peak=(660, 55), elev_label='1,159m',
    map_note='영축산 연계', map_start='배내고개', map_end='배내고개',
    map_path='M130 320 C240 290, 350 230, 470 185 S620 90, 660 70 S600 230, 440 280 S230 330, 130 320', map_nodes=[(130, 320, 10), (470, 185, 8), (660, 70, 12), (130, 320, 10)]),
  ]),
 'gamaksan': dict(
  ko_name='감악산', en_name='Gamaksan', alt='674.9m', region='경기', en_region='Gyeonggi',
  lat=37.859, lng=126.926,
  intro_ko='파주·양주·연천에 걸친 한북정맥의 산 674.9m. 감악사와 장흥계곡, 출렁다리가 어우러진 수도권 대표 근교 산입니다.',
  intro_en='A 674.9 m mountain of the Hanbuk-jeongmaek across Paju, Yangju and Yeoncheon — temples, the Jangheung valley and a suspension bridge make it a capital-area favorite.',
  permit=('불필요', 'N/A'),
  courses=[
   dict(id='beginner', color='green', hexc='#6a7d4c', meter=2, level=('초급', 'Beginner'),
    name=('출렁다리 왕복', 'Suspension Bridge Walk'),
    dist=('약 4.2km', '~4.2 km'), time=('약 3시간', '~3 h'),
    flow=('장흥계곡 들머리', '감악산 출렁다리', '장흥계곡'),
    desc=('감악산의 상징 출렁다리를 건너는 가벼운 왕복 코스. 계곡 산책과 조망을 함께 즐길 수 있어 '
          '가족 산행에 인기다.',
          'An easy out-and-back over the mountain\'s signature suspension bridge — valley strolling with views, popular with families.'),
    segs=[
     (1, ('장흥계곡 들머리 → 출렁다리', 'Valley mouth → bridge'), '약 2.1km', '50분',
      ('계곡길을 따라 오른다. 물소리와 함께하는 접근로다.',
       'A stream-side approach with running water all the way.'), 40, 'tip',
      ('출렁다리 개방시간은 이용 전 확인.', 'Check the bridge\'s opening hours before you go.')),
     (2, ('출렁다리 조망', 'On the bridge'), '—', '20~30분',
      ('계곡 위로 놓인 출렁다리에서 산 전망이 열린다.',
       'The bridge opens views over the valley.'), 60, 'warn',
      ('바람 강한 날 흔들림이 크다 — 손잡이 필수.', 'It sways in strong wind — hold the rails.')),
     (3, ('출렁다리 → 들머리 복귀', 'Return'), '약 2.1km', '50분',
      ('계곡길로 되돌아 내려온다.',
       'Back down the valley path.'), 100, 'tip',
      ('여름철 계곡 물놀이와 연계하면 하루 일정.', 'Pair with a summer valley splash for a full day.')),
    ],
    cps=[
     ('장흥계곡 들머리', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 100m', '0km', ('주차·매점', 'Parking, shops')),
     ('출렁다리', ('핵심', 'Highlight'), 'badge-landmark', '해발 약 250m', '2.1km', ('계곡 조망', 'Valley views')),
     ('장흥계곡 들머리', ('도착', 'Finish'), 'badge-trailhead', '해발 약 100m', '약 4.2km', ('주차', 'Parking')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('운동화 수준 가능·물. 아이 동반 시 손잡이 필수.', 'Sneakers fine; hold children\'s hands on the bridge.')),
     ('book', ('입산', 'Entry'), ('별도 예약 불필요 — 출락다리 운영시간만 확인.', 'No reservation needed; just check bridge hours.')),
     ('shield', ('주의', 'Cautions'), ('주말 계곡 주차 혼잡 — 일찍 도착.', 'Weekend parking jams — arrive early.')),
    ],
    elev_path='M20 195 C200 180, 400 140, 560 110 S690 95, 740 92', elev_peak=(740, 92), elev_label='약 250m',
    map_note='출렁다리 왕복', map_start='장흥계곡', map_end='출렁다리',
    map_path='M110 350 C250 320, 380 260, 500 200 S650 110, 700 80', map_nodes=[(110, 350, 10), (500, 200, 8), (700, 80, 12)]),
   dict(id='intermediate', color='blue', hexc='#456e96', meter=3, level=('중급', 'Intermediate'),
    name=('감악사~연천봉 왕복', 'Gamaksa–Yeoncheonbong Round Trip'),
    dist=('약 5.5km', '~5.5 km'), time=('3~4시간', '3–4 h'),
    flow=('감악사 주차장', '감악사', '능선길', '연천봉 674.9m'),
    desc=('감악사에서 주능선을 타고 감악산의 주봉 연천봉에 오르는 표준 왕복 코스. 제1주차장 기준 '
          '원점회귀 약 5.5km 안내가 일반적이다.',
          'The standard round trip from Gamaksa temple up the main ridge to the chief peak Yeoncheonbong — about 5.5 km from the first parking lot.'),
    segs=[
     (1, ('감악사 주차장 → 감악사', 'Parking → Gamaksa'), '약 0.5km', '15분',
      ('고찰 감악사 경내를 지나 등산로로 접어든다.',
       'Through the old Gamaksa temple grounds to the trailhead.'), 10, 'tip',
      ('주차장-사찰 구간 도보 접근 — 주차요금 확인.', 'Short walk from the lot; check parking fees.')),
     (2, ('감악사 → 능선길', 'Gamaksa → ridge'), '약 2km', '1~1.5시간',
      ('숲 오름길로 능선에 붙는다. 오르내림이 반복되는 한북정맥 능선이다.',
       'A forest climb onto the rolling Hanbuk-jeongmaek ridge.'), 50, 'warn',
      ('경사 반복 — 지팡이가 도움된다.', 'Rolling grades — poles help.')),
     (3, ('능선길 → 연천봉', 'Ridge → Yeoncheonbong'), '약 0.7km', '30분',
      ('바위 전망대를 지나 주봉 연천봉 674.9m에 오른다.',
       'Past rock viewpoints to the chief peak at 674.9 m.'), 80, 'tip',
      ('정상에서 임진강 방면 조망.', 'Views toward the Imjin River.')),
     (4, ('연천봉 → 감악사 하산', 'Yeoncheonbong → descent'), '약 2.3km', '1~1.5시간',
      ('감악사로 내려와 산행을 마무리한다.',
       'Descend to Gamaksa to finish.'), 100, 'tip',
      ('사찰 경내 마무리 산책 여유.', 'Linger in the temple grounds.')),
    ],
    cps=[
     ('감악사 주차장', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 150m', '0km', ('주차장·화장실', 'Parking, restrooms')),
     ('감악사', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 200m', '0.5km', ('고찰', 'Old temple')),
     ('능선길', ('경유', 'Waypoint'), 'badge-shelter', '해발 약 500m', '2.5km', ('바위 전망', 'Rock views')),
     ('연천봉', ('정상', 'Summit'), 'badge-summit', '674.9m', '3.2km', ('임진강 조망', 'Imjin River views')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 1L·지팡이.', 'Boots, 1 L water, poles.')),
     ('book', ('입산', 'Entry'), ('별도 예약·허가 불필요.', 'No reservation or permit needed.')),
     ('shield', ('주의', 'Cautions'), ('능선 오르내림 반복 — 하산 무릎 부담 대비.', 'Repeated ups and downs — mind your knees on the way down.')),
    ],
    elev_path='M20 190 C170 172, 320 130, 480 95 S650 62, 740 50', elev_peak=(740, 50), elev_label='674.9m',
    map_note='감악사 코스', map_start='감악사', map_end='연천봉',
    map_path='M110 345 C240 318, 350 268, 460 212 S620 98, 695 58', map_nodes=[(110, 345, 10), (460, 212, 8), (695, 58, 12)]),
   dict(id='advanced', color='red', hexc='#9f5845', meter=4, level=('고급', 'Advanced'),
    name=('출렁다리~범륜사~임꺽정봉~연천봉~까치봉 일주', 'Full Circuit: Bridge–Beomnunsa–Yeoncheonbong–Kkachibong'),
    dist=('약 6.7km', '~6.7 km'), time=('4~5시간', '4–5 h'),
    flow=('출렁다리', '범륜사', '임꺽정봉', '연천봉 674.9m', '까치봉'),
    desc=('감악산의 명소를 모두 잇는 일주 코스. 공개 실측 기록 기준 약 6.7km·휴식 포함 약 4시간 11분 — '
          '암릉과 능선, 사찰·출렁다리까지 감악산의 전부를 담는다.',
          'The full circuit linking every Gamaksan highlight — about 6.7 km and 4h11m with breaks per public logs: crags and ridges, temples and the suspension bridge.'),
    segs=[
     (1, ('출렁다리 → 범륜사', 'Bridge → Beomnunsa'), '약 1.5km', '40분',
      ('출렁다리에서 산허리로 붙어 범륜사에 닿는다.',
       'From the bridge along the flank to Beomnunsa temple.'), 20, 'tip',
      ('범륜사 약수로 유명하다.', 'The temple is known for its spring water.')),
     (2, ('범륜사 → 임꺽정봉', 'Beomnunsa → Imkkeokjeongbong'), '약 2km', '1.5시간',
      ('바위 능선이 본격화된다. 임꺽정 전설이 남은 봉우리다.',
       'The rock ridge begins in earnest toward Imkkeokjeongbong.'), 55, 'warn',
      ('암릉 구간 장갑 필수.', 'Gloves required on the crags.')),
     (3, ('임꺽정봉 → 연천봉', 'Imkkeokjeongbong → Yeoncheonbong'), '약 1.5km', '1시간',
      ('주능선을 타고 주봉 연천봉 674.9m 완등.',
       'Along the main ridge to the chief peak.'), 85, 'tip',
      ('정상 조망 후 까치봉 방면 이어치기.', 'Summit views, then on to Kkachibong.')),
     (4, ('연천봉 → 까치봉 → 하산', 'Yeoncheonbong → Kkachibong → exit'), '약 1.7km', '1시간',
      ('까치봉을 지나 하산로로 벗어난다.',
       'Over Kkachibong to the exit trail.'), 100, 'warn',
      ('하산길 급경사 구간 — 속도 줄이기.', 'Steep pitches on the descent — slow down.')),
    ],
    cps=[
     ('출렁다리', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 250m', '0km', ('주차·매점', 'Parking, shops')),
     ('범륜사', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 300m', '1.5km', ('약수·사찰', 'Spring, temple')),
     ('임꺽정봉', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 600m', '3.5km', ('암릉', 'Crags')),
     ('연천봉', ('정상', 'Summit'), 'badge-summit', '674.9m', '5km', ('조망', 'Panorama')),
     ('까치봉', ('도착', 'Finish'), 'badge-trailhead', '해발 약 400m', '약 6.7km', ('하산로', 'Exit trail')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·장갑·물 1.5L — 암릉 일주 구성.', 'Boots, gloves, 1.5 L water — a crag circuit.')),
     ('book', ('입산', 'Entry'), ('별도 예약·허가 불필요.', 'No reservation or permit needed.')),
     ('shield', ('주의', 'Cautions'), ('임꺽정봉 전후 암릉 — 우천 시 미끄럼 사고 다발.', 'Crags around Imkkeokjeongbong are accident-prone when wet.')),
    ],
    elev_path='M20 190 C150 168, 280 122, 420 88 S560 62, 650 50 S710 80, 740 100', elev_peak=(650, 50), elev_label='674.9m',
    map_note='감악산 일주', map_start='출렁다리', map_end='까치봉',
    map_path='M130 300 C240 320, 340 270, 460 215 S620 110, 680 80 S610 240, 450 285 S240 300, 130 300', map_nodes=[(130, 300, 10), (460, 215, 8), (680, 80, 12), (130, 300, 10)]),
  ]),
}

LEVELS = [('beginner', 'green', '#6a7d4c', 2), ('intermediate', 'blue', '#456e96', 3), ('advanced', 'red', '#9f5845', 4)]


def _peak_of(path):
    """SVG path 문자열에서 y가 가장 작은(화면 최고점=정상) 좌표를 되돌린다."""
    pts = re.findall(r'(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)', path)
    pairs = [(float(x), float(y)) for x, y in pts]
    assert pairs, f'elev_path 좌표 파싱 실패: {path}'
    px, py = min(pairs, key=lambda p: p[1])
    return (int(px), int(py))


CONTENT = {}
COURSES = {}


for mid, d in F6.items():
    for lang in ('ko', 'en'):
        ko = lang == 'ko'
        ix = 0 if ko else 1  # (ko, en) 튜플 인덱스
        L = lang
        courses = []
        for c in d['courses']:
            flow = list(c['flow'])
            pills = (pill('ruler', '거리' if ko else 'Distance', c['dist'][ix]) +
                     pill('clock', '소요' if ko else 'Time', c['time'][ix]) +
                     pill('location', '정상' if ko else 'Summit', d['alt']) +
                     pill_meter('난이도' if ko else 'Difficulty', c['meter'], 'medium' if c['meter'] <= 3 else 'hard') +
                     pill('star', '100대' if ko else '100 Mt.', '✓') +
                     pill('book', '허가' if ko else 'Permit', d['permit'][ix]))
            courses.append(dict(
                id=c['id'], color=c['color'], hex=c['hexc'], meter=c['meter'],
                level=c['level'][ix], name=c['name'][ix], sub=f'{c["dist"][ix]} · {c["time"][ix]}',
                tabs=['개요', '경로 안내', '지도', '팁 &amp; 주의'] if ko else ['Overview', 'Route', 'Map', 'Tips'],
                pills=pills,
                h_flow='코스 흐름' if ko else 'Course Flow', h_elev='고도 프로파일' if ko else 'Elevation Profile',
                h_route='구간별 경로 안내' if ko else 'Route by Section', h_map='코스 개념도' if ko else 'Concept Map',
                h_cp='체크포인트 표' if ko else 'Checkpoints',
                flow=flow, elev_label=c['elev_label'], elev_path=c['elev_path'], elev_peak=_peak_of(c['elev_path']),
                desc=c['desc'][ix],
                segs=[(no, t[ix], km, tm, b[ix], bar, kind, tip[ix]) for (no, t, km, tm, b, bar, kind, tip) in c['segs']],
                tips=[(icon, title[ix], [items[ix]]) for (icon, title, items) in c['tips']],
                cps=[(nm[ix] if isinstance(nm, tuple) else nm, badge[ix], cls, alt, km, amen[ix]) for (nm, badge, cls, alt, km, amen) in c['cps']],
                map_note=c['map_note'][ix], map_start=c['map_start'][ix], map_end=c['map_end'][ix],
                map_path=c['map_path'], map_nodes=c['map_nodes']))
        name = d['ko_name'] if ko else d['en_name']
        CONTENT.setdefault(mid, {})[lang] = dict(
            title=f'{name} 등산 플레이북' if ko else f'{d["en_name"]} Hiking Playbook',
            meta=(f'100대 명산 {d["ko_name"]}({d["alt"]}). ' + d['intro_ko']) if ko else (f'Guide to {d["en_name"]} ({d["alt"]}). ' + d['intro_en']),
            h1_card=d['ko_name'] if ko else d['en_name'],
            p_card=f'{name} · 100대 명산 {d["alt"]}' if ko else f'{d["en_name"]} · 100 Mt. {d["alt"]}',
            hero_alt=d['intro_ko'] if ko else d['intro_en'],
            badge=f'{name} 플레이북' if ko else f'{d["en_name"]} Playbook',
            h1=f'{name} 등산 플레이북' if ko else f'{d["en_name"]} Hiking Playbook',
            hero_desc=d['intro_ko'] if ko else d['intro_en'],
            btn1=d['courses'][0]['name'][ix], btn2=d['courses'][1]['name'][ix], btn3=d['courses'][2]['name'][ix],
            hero_photographer='', hero_url='',
            gal_title=f'{name}의 사계 &amp; 명소' if ko else f'{d["en_name"]} Seasons',
            lb_zoom='크게 보기' if ko else 'View larger',
            gallery=[(f'g{i}', f'{name} 풍경 {i}' if ko else f'{d["en_name"]} scenery {i}', 'Unsplash') for i in range(1, 5)])
        COURSES.setdefault(mid, {})[lang] = courses


_credits = _json.load(open(_pl.Path(__file__).parent / 'k100v6_credits.json'))
_meta = {list(c.keys())[0]: list(c.values())[0] for c in _credits}
for _mid, _c in _meta.items():
    if _mid in CONTENT:
        for _lang in ('ko', 'en'):
            CONTENT[_mid][_lang]['hero_photographer'] = _c['hero']['photographer']
            CONTENT[_mid][_lang]['hero_url'] = _c['hero']['url']
            for _i, _g in _c['gallery'].items():
                _cap = f"Photo by &lt;a href='{_g['url']}' target='_blank' rel='noopener'&gt;{_g['photographer']}&lt;/a&gt; on Unsplash"
                _lst = list(CONTENT[_mid][_lang]['gallery']); _idx = int(_i[1]) - 1
                if _idx < len(_lst):
                    _lst[_idx] = (_lst[_idx][0], _lst[_idx][1], _cap)
                CONTENT[_mid][_lang]['gallery'] = tuple(_lst)
