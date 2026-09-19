# -*- coding: utf-8 -*-
"""한국 100대 명산 5차(4산) 콘텐츠 — 남산(경주)·계방산·두타산·마니산.

사실 근거 (2026-09 세션 검증, 2소스 교차):
- 100대 명산 목록 포함: 위키백과 「대한민국 100대 명산」 × 산림청(2002 선정) 목록
- 남산(경주): 금오봉 468m·고위봉 494~495m(산행기 다수 × 위키백과 목록),
  삼릉 탐방지원센터~금오봉 약 5.6km(산행 실측 기록), 유네스코 「남산 불국토」(2018 확장)
- 계방산: 1,577m(대한민국 구석구석 × 여행정보 사이트), 오대산국립공원 최고봉,
  운두령·1100고지 출발 코스(공개 산행기 다수)
- 두타산: 1,357m(위키백과 목록 × 산행기), 댓재휴게소 출발, 무릉계 코스 약 8.2km(산행 실측),
  베틀바위·마천루·산성폭포 지명(산행기 × 지역 보도)
- 마니산: 469m(강화 최고봉), 참성단(천제단)·삼랑성, 단군로 약 5.2km(강화군 안내 인용 산행기),
  정수사 코스 편도 1.7km
거리·시간 중 검증되지 않은 값은 「약」으로 근사 표기하고, 탐방로 상태 등 변동 품목은
「이용 전 확인」 안내로 일반화했다.
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


# ── 사실 테이블 ──────────────────────────────────────────────
# seg: (no, title, km, time, body, bar%, kind, tip)  — 번호·난이도색은 코스별 자동
# cp : (name, badge, badge_cls, alt, km, amen)
F5 = {
 'namsan': dict(
  ko_name='남산(경주)', en_name='Namsan (Gyeongju)', alt='468m', region='경상', en_region='Gyeongsang',
  lat=35.8292, lng=129.2210,
  intro_ko='유네스코 세계유산 「남산 불국토」. 금오봉 468m를 정점으로 사지·석불·탑이 산 전체에 흩어진 열린 야외 박물관입니다.',
  intro_en='UNESCO World Heritage — the Namsan Buddhist Mountain Monastery of Gyeongju, an open-air museum of temple sites, stone Buddhas and pagodas gathered around Geumobong 468 m.',
  permit=('불필요', 'N/A'),
  courses=[
   dict(id='beginner', color='green', hexc='#6a7d4c', meter=2, level=('초급', 'Beginner'),
    name=('삼릉~금오봉 왕복', 'Samneung–Geumobong Round Trip'),
    dist=('약 5.6km', '~5.6 km'), time=('3~4시간', '3–4 h'),
    flow=('삼릉 탐방지원센터', '상선암', '금오봉 468m', '삼릉'),
    desc=('경주 남산의 대표 입문 코스. 삼릉 탐방지원센터에서 시작해 상선암·바둑바위를 지나 '
          '남산의 상징봉 금오봉(468m)에 오르는 왕복 산행이다. 정상에서 경주 분지와 월성 방면 전망이 열린다.',
          'The classic intro route on Gyeongju Namsan. From Samneung Trail Center past Sangseonam and Baduk Rock to the symbolic summit Geumobong (468 m), with open views over the Gyeongju basin.'),
    segs=[
     (1, ('삼릉 탐방지원센터 → 상선암', 'Trail Center → Sangseonam'), '약 2.2km', '1~1.5시간',
      ('삼릉 탐방지원센터 뒤 능선길로 시작해 숲속 완만한 오르막을 따라 상선암에 도달한다. 남산 남쪽 사면의 대표 접근로다.',
       'A gentle forest climb behind Samneung Trail Center leads to Sangseonam, the main approach on the southern slope.'), 35, 'tip',
      ('탐방지원센터에서 화장실·주차를 마치고 출발하면 편하다.', 'Restrooms and parking are at the trail center — use them before starting.')),
     (2, ('상선암 → 바둑바위 → 금오봉', 'Sangseonam → Baduk Rock → Geumobong'), '약 0.6km', '30~40분',
      ('암반 구간이 나타나며 구간이 가파라진다. 바둑바위를 지나면 남산의 상징인 금오봉(468m) 정상. '
       '돌계단과 밧줄이 설치되어 있으나 미끄러지지 않게 주의한다.',
       'The trail steepens over rock steps. Past Baduk Rock stands Geumobong (468 m), the symbolic peak of Namsan. Steps and ropes are in place — watch your footing.'), 65, 'warn',
      ('바위 구간에서는 우천 시 미끄러움에 주의하고, 유적 훼손 방지를 위해 표지 경로를 벗어나지 않는다.',
       'Avoid slipping on wet rock, and stay on marked paths to protect the archaeological remains.')),
     (3, ('금오봉 정상', 'Geumobong summit'), '—', '20~30분',
      ('정상에서 경주 시내·월성·포석 능선이 한눈에 들어온다. 사계절 등산객이 찾는 남산의 전망 포인트다.',
       'The summit opens views over downtown Gyeongju, Wolseong and the Poseok ridge — the classic viewpoint of Namsan.'), 100, 'tip',
      ('정상 주변에도 석조 유적이 있으니 자리를 옮기며 조심스럽게 둘러본다.', 'Stone remains lie near the summit — look around carefully.')),
     (4, ('금오봉 → 삼릉 하산', 'Geumobong → Samneung descent'), '약 2.8km', '1.5~2시간',
      ('올라온 길을 따라 내려온다. 하산길에도 절터와 석조물 자취가 이어지니 서두르지 않고 둘러볼 만하다.',
       'Return the way you came. Temple-site traces continue along the descent — worth a slow look.'), 80, 'tip',
      ('하산 후 삼릉~포석정 문화유산 산책로를 덧붙이면 하루 코스가 완성된다.',
       'After the hike, add the Samneung–Poseokjeong heritage walk for a full day.')),
    ],
    cps=[
     ('삼릉 탐방지원센터', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 200m', '0km', ('주차장·화장실·안내소', 'Parking, restrooms, info desk')),
     ('상선암', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 360m', '2.2km', ('쉼터 없음', 'No facilities')),
     ('금오봉', ('정상', 'Summit'), 'badge-summit', '468m', '2.8km', ('전망·간이화장실(하단)', 'Viewpoint, simple restroom below')),
     ('삼릉', ('도착', 'Finish'), 'badge-trailhead', '해발 약 200m', '5.6km', ('주차장·식당(인근)', 'Parking, nearby restaurants')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 1L·자외선 차단. 바위 구간용 장갑이 있으면 좋다.', 'Hiking shoes, 1 L water, sun protection. Gloves help on the rock steps.')),
     ('book', ('입산', 'Entry'), ('별도 예약·허가 없이 입산할 수 있다. 탐방지원센터 안내를 활용하자.', 'No reservation or permit required. Ask at the trail center for guidance.')),
     ('shield', ('주의', 'Cautions'), ('산 전체가 문화재 구역 — 이동 중 유적을 만지거나 새겨 쓰는 행위는 금물이다.',
      'The whole mountain is a heritage zone — never touch or mark the remains.')),
    ],
    elev_path='M20 190 C150 185, 260 160, 380 120 S560 70, 700 50', elev_peak=(700, 50), elev_label='468m',
    map_note='남산 남사면 삼릉~금오봉', map_start='삼릉', map_end='금오봉',
    map_path='M110 330 C230 310, 330 270, 450 210 S620 110, 690 70', map_nodes=[(110, 330, 10), (450, 210, 8), (690, 70, 12)]),
   dict(id='intermediate', color='blue', hexc='#456e96', meter=3, level=('중급', 'Intermediate'),
    name=('삼불사~금오봉~포석정 순환', 'Sambulsa–Geumobong–Poseokjeong Circuit'),
    dist=('약 9km', '~9 km'), time=('5~6시간', '5–6 h'),
    flow=('삼불사', '삼릉', '금오봉 468m', '포석정', '삼불사'),
    desc=('남산 북사면 문화유산을 한 바퀴 도는 대표 순환 코스. 삼불사 삼층석탑에서 시작해 삼릉·금오봉을 거쳐 '
          '신라 연회지 포석정으로 내려온다. 산행과 유적 관람이 절반씩인 남산다운 코스다.',
          'The signature circuit of Namsan\'s northern heritage. From the Sambulsa three-story pagoda past Samneung and Geumobong down to Poseokjeong, the Silla banquet pavilion — half hike, half open-air museum.'),
    segs=[
     (1, ('삼불사 → 삼릉', 'Sambulsa → Samneung'), '약 2.5km', '1~1.5시간',
      ('삼층석탑이 서 있는 삼불사에서 능선길로 오른다. 남산 북능의 숲길을 따라 삼릉 방향으로 이어진다.',
       'Climb the northern ridge from Sambulsa with its stone pagoda, following the forested north ridge toward Samneung.'), 30, 'tip',
      ('삼불사 주차장(유료 가능성) — 이용 전 요금 안내를 확인하자.', 'Sambulsa parking may charge a fee — check before you go.')),
     (2, ('삼릉 → 금오봉', 'Samneung → Geumobong'), '약 2.8km', '1.5~2시간',
      ('완만한 오르막 후 암반 구간을 지나 금오봉 468m에 오른다. 상선암 코스보다 능선 전망이 길게 이어진다.',
       'A steady climb and short rock section to Geumobong 468 m, with longer ridge views than the Sangseonam approach.'), 65, 'warn',
      ('능선 구간은 바람에 노출되어 있다 — 강풍일 때는 모자를 고정하자.', 'The ridge is exposed — secure your hat on windy days.')),
     (3, ('금오봉 → 포석정', 'Geumobong → Poseokjeong'), '약 3km', '1.5~2시간',
      ('북능을 따라 내려오면 신라 마지막 연회로 전해지는 포석정 터에 닿는다. 곡류천 유적과 반월형 물길이 남아 있다.',
       'Descend the north ridge to the Poseokjeong site, where the Silla banquet pavilion\'s curved water channel still remains.'), 90, 'tip',
      ('유적 구간은 관람 동선을 따라 천천히 — 보행로 이탈은 금지다.', 'Follow the visitor paths through the site — do not stray off-trail.')),
     (4, ('포석정 → 삼불사', 'Poseokjeong → Sambulsa'), '약 1.5km', '30~40분',
      ('평탄한 둘레길을 따라 출발점으로 돌아온다. 남산 구경길 마무리로 가볍다.',
       'An easy flat path returns to the trailhead — a light finish to the circuit.'), 100, 'tip',
      ('시간 여유가 있으면 국립경주박물관에서 남산 출토 석조물를 이어서 볼 수 있다.',
       'With time to spare, see Namsan stone pieces at the Gyeongju National Museum.')),
    ],
    cps=[
     ('삼불사', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 100m', '0km', ('주차장·삼층석탑(보물)', 'Parking, three-story pagoda')),
     ('삼릉', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 250m', '2.5km', ('탐방지원센터·화장실', 'Trail center, restrooms')),
     ('금오봉', ('정상', 'Summit'), 'badge-summit', '468m', '5.3km', ('전망', 'Viewpoint')),
     ('포석정', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 80m', '8.3km', ('유적 전시·안내판', 'Site interpretation boards')),
     ('삼불사', ('도착', 'Finish'), 'badge-trailhead', '해발 약 100m', '9km', ('주차장', 'Parking')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 1.5L·행동식. 유적 구간 안내 지도를 미리 저장해 두자.', 'Hiking shoes, 1.5 L water, snacks. Save an offline map of the heritage sites.')),
     ('book', ('입산', 'Entry'), ('허가 불필요. 포석정·삼릉 등 유적지는 관람 동선 안내를 따른다.', 'No permit required. Follow visitor guidance at Poseokjeong and Samneung.')),
     ('shield', ('주의', 'Cautions'), ('종주 구간 도탈 지점이 많다 — 능선에서 내려가는 갈림길마다 표지를 확인한다.',
      'Many side trails branch off the ridge — check the signs at every junction.')),
    ],
    elev_path='M20 190 C160 180, 300 120, 460 90 S640 150, 740 170', elev_peak=(460, 90), elev_label='468m',
    map_note='남산 북사면 순환', map_start='삼불사', map_end='포석정',
    map_path='M120 320 C220 300, 300 250, 420 200 S600 120, 660 90 S560 250, 400 300 S220 350, 120 320', map_nodes=[(120, 320, 10), (420, 200, 8), (660, 90, 12), (120, 320, 10)]),
   dict(id='advanced', color='red', hexc='#9f5845', meter=4, level=('고급', 'Advanced'),
    name=('동남산~금오봉~고위봉 능선 종주', 'Dongnam Ridge Traverse: Dongnamsan–Geumobong–Gowibong'),
    dist=('약 11km', '~11 km'), time=('6~7시간', '6–7 h'),
    flow=('동남산 입구', '칠불암', '금오봉 468m', '고위봉 495m', '삼릉'),
    desc=('남산 최고봉 고위봉(약 495m)까지 이어지는 능선 종주. 동남산 칠불암 방면에서 능선을 따라 '
          '금오봉을 넘어 고위봉에 오르고 삼릉으로 내려온다. 유적 밀집 능선이라 발걸음이 잦다.',
          'A ridge traverse to Gowibong (~495 m), the highest point of Namsan. From Dongnamsan and Chibulam along the ridge over Geumobong to Gowibong, then down to Samneung — a heritage-dense ridgeline.'),
    segs=[
     (1, ('동남산 입구 → 칠불암', 'Dongnamsan entrance → Chibulam'), '약 2km', '1~1.5시간',
      ('남산 동남 사면에서 숲길을 오라 칠불암에 닿는다. 암석 사이 사지와 석조물가 이어지는 구간이다.',
       'A forested climb on the southeast slope reaches Chibulam, passing temple sites and stone remains.'), 30, 'tip',
      ('칠불암 부근 탐방로는 경사가 있어 비 온후 미끄럽다.', 'The trail near Chibulam is steep and slippery after rain.')),
     (2, ('칠불암 → 금오봉', 'Chibulam → Geumobong'), '약 3.5km', '2~2.5시간',
      ('능선길이 본격화된다. 바위 단차와 완급이 반복되며 금오봉 468m에 오른다.',
       'The ridge proper: repeated rock steps lead to Geumobong 468 m.'), 65, 'warn',
      ('암반 구간 장갑 필수. 낙엽기 미끄럼 사고가 잦은 구간이다.', 'Gloves are essential on the rock; expect slippery leaves in autumn.')),
     (3, ('금오봉 → 고위봉', 'Geumobong → Gowibong'), '약 1.5km', '40~60분',
      ('남산의 최고봉 고위봉(약 495m)으로 이어지는 짧지만 덩치 있는 능선. 100대 명산 표고 495m의 주인공이다.',
       'A short but substantial ridge to Gowibong (~495 m), the true high point behind the 100-mountains elevation figure.'), 85, 'tip',
      ('고위봉 일대 탐방로 상태는 변동이 있을 수 있으니 최근 산행 후기를 참고하자.',
       'Trail conditions around Gowibong vary — check recent trip reports.')),
     (4, ('고위봉 → 삼릉 하산', 'Gowibong → Samneung descent'), '약 4km', '2~2.5시간',
      ('북사면 숲길로 삼릉까지 내려온다. 종주 피로가 몰리는 구간 — 남은 시간을 넉넉히 잡는다.',
       'A forested descent of the north slope to Samneung — legs will be tired; leave slack in your timing.'), 100, 'warn',
      ('일몰이 가까우면 능선에서 바로 하산로로 — 야간 잔류는 금물이다.',
      'Near dusk, leave the ridge for a descent trail — do not stay out after dark.')),
    ],
    cps=[
     ('동남산 입구', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 90m', '0km', ('주차 공간 협소', 'Limited parking')),
     ('칠불암', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 300m', '2km', ('사찰', 'Temple')),
     ('금오봉', ('경유', 'Summit'), 'badge-summit', '468m', '5.5km', ('전망', 'Viewpoint')),
     ('고위봉', ('최고봉', 'High point'), 'badge-summit', '약 495m', '7km', ('전망 없음(삼림)', 'Forested, no view')),
     ('삼릉', ('도착', 'Finish'), 'badge-trailhead', '해발 약 200m', '11km', ('주차장·화장실', 'Parking, restrooms')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·장갑·지팡이·물 1.5L. 능선 종주라 체력 배분이 관건이다.', 'Hiking shoes, gloves, poles, 1.5 L water. Pace yourself — it is a full ridge day.')),
     ('book', ('입산', 'Entry'), ('허가 불필요. 다만 유적 구간 사진 촬영도 삼가는 매너가 필요하다.', 'No permit required, but be restrained with photography inside shrine sites.')),
     ('shield', ('주의', 'Cautions'), ('구간이 길어 일몰 후 하산 가능성이 있다 — 헤드램프를 반드시 챙긴다.',
      'The traverse runs long — carry a headlamp in case of a late descent.')),
    ],
    elev_path='M20 195 C140 170, 260 130, 400 95 S540 85, 600 60 S680 100, 740 130', elev_peak=(600, 60), elev_label='495m',
    map_note='남산 능선 종주', map_start='동남산', map_end='삼릉',
    map_path='M130 340 C230 310, 310 260, 430 210 S600 90, 660 60 S600 200, 440 250 S220 300, 130 340', map_nodes=[(130, 340, 10), (430, 210, 8), (660, 60, 12), (130, 340, 10)]),
  ]),
 'gyebangsan': dict(
  ko_name='계방산', en_name='Gyebangsan', alt='1,577m', region='강원', en_region='Gangwon',
  lat=37.5330, lng=128.3720,
  intro_ko='오대산국립공원의 최고봉 1,577m. 홍천·평창 경계의 광활한 초원 능선과 겨울 설경으로 이름 높은 100대 명산입니다.',
  intro_en='The highest peak of Odaesan National Park at 1,577 m — vast grassy ridges on the Hongcheon–Pyeongchang border, famed for winter snowscapes.',
  permit=('불필요', 'N/A'),
  courses=[
   dict(id='beginner', color='green', hexc='#6a7d4c', meter=2, level=('초급', 'Beginner'),
    name=('1100고지~계방산 최단 왕복', '1100 Highlands Shortest Round Trip'),
    dist=('약 5km', '~5 km'), time=('2.5~3.5시간', '2.5–3.5 h'),
    flow=('1100고지', '계곡길', '계방산 1,577m', '1100고지'),
    desc=('계방산의 최단 등산로. 1100고지 주차장에서 시작해 숲길을 완만하게 오라 정상 초원에 닿는다. '
          '전형적인 육산(육리산) 지형이라 골짜기길이 길고 정상부는 탁 트였다.',
          'The shortest way up Gyebangsan: from the 1100 Highlands parking lot a gentle forest valley climbs to the open summit meadow — classic "yusan" terrain with a long valley and airy top.'),
    segs=[
     (1, ('1100고지 → 계곡길', '1100 Highlands → valley trail'), '약 1.5km', '30~40분',
      ('주차장 뒤 계곡을 따라 완만하게 오른다. 반달휴게소까지 숲길이 좋다.',
       'A gentle valley climb behind the lot leads to the Banhal rest point through good forest.'), 25, 'tip',
      ('1100고지 주차장은 주말 아침에 빨리 차는 편이다.', 'The 1100 lot fills early on weekends.')),
     (2, ('계곡길 → 능선 합류', 'Valley → ridge junction'), '약 1.5km', '1~1.5시간',
      ('계곡길이 가파라지며 능선과 만나는 지점까지 오른다. 이 구간이 최단 코스의 핵심 등반부다.',
       'The valley steepens to the ridge junction — the heart of the climb on this shortest route.'), 60, 'warn',
      ('경사 구간은 지팡이가 편하다. 우천 시 뿌리길 미끄럼 주의.', 'Poles help on the pitch; watch for slippery roots in rain.')),
     (3, ('능선 합류 → 계방산 정상', 'Ridge junction → summit'), '약 0.5km', '20~30분',
      ('능선에 오르면 숲이 드물어지며 정상 초원이 보인다. 삼각점과 안내판이 있는 넓은 정상, 1,577m.',
       'The forest thins to the broad summit meadow with its triangulation post — 1,577 m.'), 85, 'tip',
      ('정상은 바람에 노출되어 있다 — 방풍 자켓을 꺼내자.', 'The summit is exposed — put on a wind shell.')),
     (4, ('정상 → 1100고지 하산', 'Summit → 1100 Highlands descent'), '약 2.5km', '1.5~2시간',
      ('올라온 최단 코스를 그대로 내려온다. 다른 코스와 갈리는 갈림길 표지를 잘 확인한다.',
       'Descend the same shortest route, checking junction signs where other trails branch off.'), 100, 'tip',
      ('시간 여유가 있으면 정상에서 운두령 방면 전망을 즐기고 내려오자.', 'Enjoy the Windunderyeong-side view from the top before descending.')),
    ],
    cps=[
     ('1100고지 주차장', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 1,100m', '0km', ('주차장·화장실', 'Parking, restrooms')),
     ('반달휴게소', ('경유', 'Waypoint'), 'badge-shelter', '해발 약 1,250m', '1.5km', ('쉼터', 'Rest point')),
     ('계방산', ('정상', 'Summit'), 'badge-summit', '1,577m', '2.5km', ('전망', 'Viewpoint')),
     ('1100고지 주차장', ('도착', 'Finish'), 'badge-trailhead', '해발 약 1,100m', '5km', ('주차장', 'Parking')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 1L·방풍. 초봄~늦가을 아침 기온이 낮다.', 'Hiking shoes, 1 L water, wind shell. Mornings stay cold from early spring to late autumn.')),
     ('book', ('입산', 'Entry'), ('오대산국립공원 구간 — 별도 허가는 없으나 자연휴식령 지정 시 통제를 확인한다.',
      'Inside Odaesan National Park — no permit, but check seasonal closure (rest-zone) notices.')),
     ('shield', ('주의', 'Cautions'), ('고도 1,100m 이상 지대라 뇌우 시 하산이 늦다 — 기상 예보를 확인하자.',
      'Above 1,100 m, storms pin you down late — check the forecast.')),
    ],
    elev_path='M20 170 C180 160, 320 130, 470 95 S650 60, 740 46', elev_peak=(740, 46), elev_label='1,577m',
    map_note='계방산 최단 코스', map_start='1100고지', map_end='계방산',
    map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55', map_nodes=[(110, 335, 10), (460, 210, 8), (695, 55, 12)]),
   dict(id='intermediate', color='blue', hexc='#456e96', meter=3, level=('중급', 'Intermediate'),
    name=('운두령~계방산 왕복', 'Windunderyeong–Gyebangsan Round Trip'),
    dist=('약 8km', '~8 km'), time=('4~5시간', '4–5 h'),
    flow=('운두령 쉼터', '전망대', '능선길', '계방산 1,577m', '운두령 쉼터'),
    desc=('계방산의 표준 코스. 운두령 쉼터 주차장에서 전망대·능선길을 거쳐 정상 초원으로 오르는 왕복 산행. '
          '능선 전 구간에서 오대산 능선망 전망이 이어진다.',
          'The standard Gyebangsan route: from Windunderyeong rest area past the viewpoint and ridge to the summit meadow, with Odaesan\'s ridgelines in view throughout.'),
    segs=[
     (1, ('운두령 쉼터 → 전망대', 'Windunderyeong → viewpoint'), '약 1.2km', '30~40분',
      ('쉼터 뒤 완만한 능선길로 시작한다. 전망대에서 계방산 정상 능선이 정면으로 보인다.',
       'A gentle ridgeline start; from the viewpoint the summit ridge shows itself head-on.'), 25, 'tip',
      ('운두령 쉼터에 매점·화장실이 있다.', 'The rest area has a shop and restrooms.')),
     (2, ('전망대 → 능선길', 'Viewpoint → ridge'), '약 2.5km', '1.5~2시간',
      ('능선이 오르내리며 체력을 요구하는 구간. 숲과 트림이 반복되며 고도를 쌓는다.',
       'Rolling ridge ups and downs — the fitness test of the route, gaining height through forest and scrub.'), 60, 'warn',
      ('구간 등반을 반복하니 물을 미리 나눠 마신다.', 'Drink in stages — the rolling climb adds up.')),
     (3, ('능선길 → 계방산 정상', 'Ridge → Gyebangsan summit'), '약 0.8km', '30~40분',
      ('마지막 가파른 구간을 지나 정상 초원. 1,577m 삼각점에서 시원한 360도 전망이 열린다.',
       'A final steep pitch opens onto the summit meadow and its breezy 360-degree panorama at 1,577 m.'), 90, 'tip',
      ('겨울에는 정상부에 눈처녀가 쌓여 아이젠이 필요할 수 있다.', 'In winter the summit may need crampons after fresh snow.')),
     (4, ('정상 → 운두령 하산', 'Summit → Windunderyeong descent'), '약 4km', '2~2.5시간',
      ('능선길을 따라 내려온다. 올라올 때 지나친 전망 포인트를 돌아보며 천천히 내려오자.',
       'Descend the ridge, pausing at the viewpoints rushed on the way up.'), 100, 'tip',
      ('하산 후 근처 목장 카페·식당이 마무리로 알맞다.', 'Nearby ranch cafés and restaurants make a good finish.')),
    ],
    cps=[
     ('운두령 쉼터', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 950m', '0km', ('주차장·매점·화장실', 'Parking, shop, restrooms')),
     ('전망대', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 1,150m', '1.2km', ('전망대', 'Viewing deck')),
     ('계방산', ('정상', 'Summit'), 'badge-summit', '1,577m', '4.5km', ('전망', 'Viewpoint')),
     ('운두령 쉼터', ('도착', 'Finish'), 'badge-trailhead', '해발 약 950m', '8km', ('주차장', 'Parking')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 1.5L·점심. 능선 구간 바람 대비 상의를 챙긴다.', 'Hiking shoes, 1.5 L water, lunch. Bring a wind layer for the ridge.')),
     ('book', ('입산', 'Entry'), ('국립공원 구간 허가 불필요. 산불조심 기간 통제 가능성을 확인한다.',
      'No permit in the park section; check fire-season closures.')),
     ('shield', ('주의', 'Cautions'), ('능선 구간은 뇌우에 노출되어 있다 — 천둥이 들리면 즉시 하산한다.',
      'The ridge is exposed to lightning — descend at the first thunder.')),
    ],
    elev_path='M20 175 C170 165, 300 140, 430 110 S600 60, 740 44', elev_peak=(740, 44), elev_label='1,577m',
    map_note='운두령~계방산', map_start='운두령', map_end='계방산',
    map_path='M110 340 C230 320, 340 270, 450 220 S620 100, 690 60', map_nodes=[(110, 340, 10), (450, 220, 8), (690, 60, 12)]),
   dict(id='advanced', color='red', hexc='#9f5845', meter=4, level=('고급', 'Advanced'),
    name=('도사원 방면 장거리 종주', 'Dosawon Long Traverse'),
    dist=('약 13km', '~13 km'), time=('6~7시간', '6–7 h'),
    flow=('도사원 방면 입구', '능선길', '계방산 1,577m', '운두령 쉼터'),
    desc=('평창 진부면 도사원 방면에서 오르는 장거리 접근 코스로 알려져 있다. 낮은 능선을 오래 따라 '
          '정상까지 이어지는 순정형(굽이마다 오르내리는) 산행이라 시간이 크게 든다. 탐방로 상태는 이용 전 확인이 필요하다.',
          'A long approach from the Dosawon side in Jinbu, Pyeongchang: hours of rolling low ridgeline before the summit — a classic "rolling" day that eats time. Check current trail status before setting out.'),
    segs=[
     (1, ('도사원 방면 입구 → 저능선', 'Dosawon entrance → low ridge'), '약 3km', '1.5~2시간',
      ('계곡 옆 숲길로 시작해 낮은 능선에 오른다. 여기부터가 긴 산행의 시작이다.',
       'A forested valley-side start climbs to the first low ridge — the long day begins here.'), 25, 'tip',
      ('출발 시간을 아침 일찍 잡아야 귀일이 여유롭다.', 'Start early to keep the return relaxed.')),
     (2, ('저능선 → 능선길 반복 등반', 'Low ridge → rolling climbs'), '약 5km', '3~3.5시간',
      ('굽이마다 오르내리는 순정 구간이 이어진다. 체력 배분이 코스 성패를 가른다.',
       'Endless rolling ups and downs — pacing decides the day.'), 60, 'warn',
      ('중간 물 보충 지점이 없다 — 물을 충분히 준비한다.', 'No water sources on the way — carry enough.')),
     (3, ('능선길 → 계방산 정상', 'Ridge → Gyebangsan summit'), '약 2km', '1~1.5시간',
      ('본능선에 합류해 정상 초원으로 오른다. 긴 산행 끝의 개방감이 크다.',
       'Join the main ridge and climb to the summit meadow — open reward after the long approach.'), 90, 'tip',
      ('정상에서 운두령 방면 하산로와 연결된다.', 'The Windunderyeong descent links from the summit.')),
     (4, ('정상 → 운두령 하산', 'Summit → Windunderyeong descent'), '약 4km', '2~2.5시간',
      ('표준 코스를 역주행해 운두령 쉼터로 내려온다. 대중교통 복귀 계획을 미리 세운다.',
       'Follow the standard route down to Windunderyeong — plan the onward transport in advance.'), 100, 'warn',
      ('종주라 원점 회귀가 아니다 — 차량을 미리 배차(셔틀)하거나 대중교통 시간을 확인한다.',
      'It is a point-to-point traverse — arrange a shuttle or check bus times beforehand.')),
    ],
    cps=[
     ('도사원 방면 입구', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 700m', '0km', ('주차 공간 협소', 'Limited parking')),
     ('능선길 반복 구간', ('경유', 'Waypoint'), 'badge-shelter', '해발 약 1,100m', '5km', ('쉼터 없음', 'No facilities')),
     ('계방산', ('정상', 'Summit'), 'badge-summit', '1,577m', '9km', ('전망', 'Viewpoint')),
     ('운두령 쉼터', ('도착', 'Finish'), 'badge-trailhead', '해발 약 950m', '13km', ('주차장·매점', 'Parking, shop')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 2L·점심·헤드램프. 장시간 산행용 배낭 구성이 필요하다.', 'Hiking shoes, 2 L water, lunch, headlamp — a full-day pack.')),
     ('book', ('입산', 'Entry'), ('국립공원 구간 허가 불필요. 도사원 방면 탐방로 개방 상태를 사전에 확인한다.',
      'No permit in the park, but confirm the Dosawon-side trail is open before you go.')),
     ('shield', ('주의', 'Cautions'), ('거리 대비 고도 변화가 커서 오후 늦게 정상에 닿는 실수가 잦다 — 시간을 역산하라.',
      'Common mistake: arriving at the summit too late. Work your timing backward.')),
    ],
    elev_path='M20 185 C150 165, 280 140, 420 110 S560 80, 640 55 S700 80, 740 70', elev_peak=(640, 55), elev_label='1,577m',
    map_note='도사원 방면 종주', map_start='도사원', map_end='운두령',
    map_path='M120 350 C220 330, 320 280, 440 230 S620 90, 690 60', map_nodes=[(120, 350, 10), (440, 230, 8), (690, 60, 12)]),
  ]),
 'dutasan': dict(
  ko_name='두타산', en_name='Dutasan', alt='1,357m', region='강원', en_region='Gangwon',
  lat=37.1910, lng=129.0420,
  intro_ko='동해·삼척 경계의 1,357m. 베틀바위·마천루 등 암릉 비경과 무릉계곡이 어우러진 동해안 최고의 산악 지형입니다.',
  intro_en='1,357 m on the Donghae–Samcheok border — cliff wonders like Byeotul Rock and Macheonru woven with Mureung Valley, the finest mountain terrain on the East Sea coast.',
  permit=('불필요', 'N/A'),
  courses=[
   dict(id='beginner', color='green', hexc='#6a7d4c', meter=2, level=('초급', 'Beginner'),
    name=('댓재~두타산 최단 왕복', 'Datjae Shortest Round Trip'),
    dist=('약 4km', '~4 km'), time=('2.5~3.5시간', '2.5–3.5 h'),
    flow=('댓재휴게소', '숲길 능선', '두타산 1,357m', '댓재휴게소'),
    desc=('두타산의 최단 등산로. 댓재휴게소에서 숲길 능선을 따라 정상까지 왕복하는 가볍고 효율적인 코스다. '
          '정상 근처에서 베틀바위 방면 암릉 전망을 볼 수 있다.',
          'The shortest route up Dutasan — an out-and-back from Datjae rest area along a forested ridge, with views toward the Byeotul Rock cliffs near the top.'),
    segs=[
     (1, ('댓재휴게소 → 숲길 능선', 'Datjae → forest ridge'), '약 1.2km', '30~40분',
      ('댓재휴게소 뒤 숲길로 시작한다. 반달휴게소까지 완만한 오르막이 이어진다.',
       'A forested start behind Datjae rest area climbs gently to the Banhal rest point.'), 25, 'tip',
      ('댓재휴게소에 화장실·매점이 있다 — 출발 전 정비하자.', 'Datjae has restrooms and a shop — sort yourself out before starting.')),
     (2, ('숲길 능선 → 정상 직전', 'Forest ridge → below summit'), '약 1.5km', '1~1.5시간',
      ('늪길이 가파라지며 고도를 쌓는다. 두타산 특유의 울창한 참나무 숲길이다.',
       'The ridge steepens through Dutasan\'s characteristic dense oak forest.'), 60, 'warn',
      ('우천 시 뿌리길이 미끄럽다 — 신발 상태를 확인하자.', 'Watch for slippery roots after rain.')),
     (3, ('두타산 정상', 'Dutasan summit'), '—', '20~30분',
      ('1,357m 삼각점이 있는 넓은 정상. 숲에 가려 전망은 제한적이나 베틀바위 방면 갈림길 전망이 흥미롭다.',
       'A broad summit at 1,357 m with its triangulation post — mostly forested, but glimpses toward the Byeotul Rock cliffs.'), 90, 'tip',
      ('전망은 베틀바위 능선 쪽이 좋다 — 안전선 안에서만 조망하자.', 'Views are better toward Byeotul Rock — stay behind the safety line.')),
     (4, ('정상 → 댓재 하산', 'Summit → Datjae descent'), '약 2km', '1~1.5시간',
      ('올라온 길로 내려온다. 여유가 되면 베틀바위까지 다녀오는 변형도 가능하나 시간을 넉넉히 잡는다.',
       'Return the same way. A detour to Byeotul Rock is possible if you budget the extra time.'), 100, 'tip',
      ('하산 후 댓재휴게소에서 무릉계 방면 차량 이동을 준비하자.', 'After the hike, drive on from Datjae toward Mureung Valley.')),
    ],
    cps=[
     ('댓재휴게소', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 680m', '0km', ('주차장·화장실·매점', 'Parking, restrooms, shop')),
     ('반달휴게소', ('경유', 'Waypoint'), 'badge-shelter', '해발 약 900m', '1.2km', ('쉼터', 'Rest point')),
     ('두타산', ('정상', 'Summit'), 'badge-summit', '1,357m', '2.7km', ('삼각점·안내판', 'Triangulation post, signboard')),
     ('댓재휴게소', ('도착', 'Finish'), 'badge-trailhead', '해발 약 680m', '4km', ('주차장', 'Parking')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 1L. 능선 바람에 걸치는 옷을 준비한다.', 'Hiking shoes, 1 L water, and a layer for ridge wind.')),
     ('book', ('입산', 'Entry'), ('허가 불필요. 댓재휴게소 주차는 성수기 혼잡 — 일찍 도착한다.',
      'No permit needed. Datjae parking jams in peak season — arrive early.')),
     ('shield', ('주의', 'Cautions'), ('정상 인근 암릉 갈림길에서 표지를 반드시 확인 — 베틀바위 방면은 난이도가 다르다.',
      'Check signs at the cliff-side junctions — the Byeotul Rock direction is a different grade.')),
    ],
    elev_path='M20 170 C180 160, 330 120, 480 85 S650 55, 740 44', elev_peak=(740, 44), elev_label='1,357m',
    map_note='댓재~두타산 최단', map_start='댓재', map_end='두타산',
    map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55', map_nodes=[(110, 335, 10), (460, 210, 8), (695, 55, 12)]),
   dict(id='intermediate', color='blue', hexc='#456e96', meter=3, level=('중급', 'Intermediate'),
    name=('무릉계~베틀바위~마천루', 'Mureung Valley–Byeotul Rock–Macheonru'),
    dist=('약 8.2km', '~8.2 km'), time=('5~6시간', '5–6 h'),
    flow=('무릉계 유원지', '산성폭포', '베틀바위', '마천루', '무릉계 유원지'),
    desc=('두타산의 비경을 한 코스에 담은 대표 등반로. 무릉계곡에서 시작해 산성폭포·베틀바위·마천루 바위벼랑을 잇는다. '
          '공개 산행 실측 기준 약 8.2km·5시간 남짓의 구간이다.',
          'The classic loop of Dutasan\'s cliff wonders: from Mureung Valley past Sanseong Falls to Byeotul Rock and the Macheonru crags — about 8.2 km and five hours by public trip logs.'),
    segs=[
     (1, ('무릉계 유원지 → 산성폭포', 'Mureung Valley → Sanseong Falls'), '약 2km', '50~70분',
      ('무릉계 계곡길을 따라 오른다. 도갑사를 지나 산성폭포까지 수려한 계곡 경관이 이어진다.',
       'Follow the valley past Dohak Temple to Sanseong Falls through continuous gorge scenery.'), 25, 'tip',
      ('무릉계 유원지 주차장·화장실 이용 가능.', 'Parking and restrooms at Mureung Valley.')),
     (2, ('산성폭포 → 베틀바위', 'Sanseong Falls → Byeotul Rock'), '약 2.5km', '1.5~2시간',
      ('계곡에서 능선으로 접어 오르막이 강해진다. 거대한 바위장이 베틀바위에 닿으면 두타산 비경이 펼쳐진다.',
       'Leave the valley for the ridge and a steeper pitch; the giant rock of Byeotul opens Dutasan\'s finest scenery.'), 60, 'warn',
      ('베틀바위 직전 구간은 노출된 암반이 있다 — 밧줄을 잡고 이동한다.',
      'Exposed rock before Byeotul — use the fixed ropes.')),
     (3, ('베틀바위 → 마천루', 'Byeotul Rock → Macheonru'), '약 1.7km', '1~1.5시간',
      ('쌍폭포 협곡과 바위벼랑을 잇는 등반로. 마천루 거대 바위 아래가 최대 볼거리다.',
       'The gorge-and-crag section; the colossal Macheonru boulder is the highlight.'), 85, 'warn',
      ('바위 하부 통과 구간은 낙석 주의 — 대기하지 말고 통과한다.',
      'Rockfall zone under the boulder — keep moving, do not linger.')),
     (4, ('마천루 → 무릉계 하산', 'Macheonru → Mureung descent'), '약 2km', '1~1.5시간',
      ('동해시가 조성한 산길을 따라 무릉계로 내려온다. 하산길 경사가 완만해 마무리가 수월하다.',
       'Descend on the jointly built trail back to Mureung Valley on an easy grade.'), 100, 'tip',
      ('하산 후 무릉계 주변 물맛집·식당에서 마무리하자.', 'Finish with a meal around Mureung Valley.')),
    ],
    cps=[
     ('무릉계 유원지', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 150m', '0km', ('주차장·화장실·매점', 'Parking, restrooms, shops')),
     ('산성폭포', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 400m', '2km', ('전망', 'Waterfall viewpoint')),
     ('베틀바위', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 1,000m', '4.5km', ('전망대적 암반', 'Cliff viewpoint')),
     ('마천루', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 1,100m', '6.2km', ('거대 암석 전망', 'Boulder viewpoint')),
     ('무릉계 유원지', ('도착', 'Finish'), 'badge-trailhead', '해발 약 150m', '8.2km', ('주차장', 'Parking')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·장갑·물 1.5L. 암릉 구간이 많아 장갑이 실질적이다.', 'Hiking shoes, gloves, 1.5 L water — gloves earn their keep on the crags.')),
     ('book', ('입산', 'Entry'), ('허가 불필요. 무릉계 유원지는 관광지 요금·주차 체계를 이용 전 확인한다.',
      'No permit; check Mureung Valley fees and parking rules before you go.')),
     ('shield', ('주의', 'Cautions'), ('우천 시 암릉 구간은 위험 — 비 예보일에는 최단 왕복 코스로 대체하자.',
      'Crags turn dangerous in rain — switch to the short loop when rain is forecast.')),
    ],
    elev_path='M20 190 C160 175, 300 120, 450 85 S600 70, 700 60 S720 90, 740 100', elev_peak=(450, 85), elev_label='약 1,100m',
    map_note='무릉계 등반로', map_start='무릉계', map_end='마천루',
    map_path='M120 340 C220 310, 320 260, 440 200 S610 110, 670 80 S620 240, 440 290 S230 340, 120 340', map_nodes=[(120, 340, 10), (440, 200, 8), (670, 80, 12), (120, 340, 10)]),
   dict(id='advanced', color='red', hexc='#9f5845', meter=4, level=('고급', 'Advanced'),
    name=('댓재~두타산~베틀봉~무릉계 종주', 'Datjae–Dutasan–Byeolbong–Mureung Traverse'),
    dist=('약 12km', '~12 km'), time=('7~8시간', '7–8 h'),
    flow=('댓재휴게소', '두타산 1,357m', '베틀봉', '무릉계 유원지'),
    desc=('두타산의 대표 종주. 댓재에서 정상을 거쳐 베틀봉 능선과 베틀바위 비경을 지나 무릉계로 빠지는 '
          '두타산의 알짜 경관을 모두 모으는 코스다. 거리·시간이 크므로 체력과 일광을 넉넉히 잡는다.',
          'The full Dutasan traverse: Datjae over the summit along Byeolbong ridge and the Byeotul Rock wonders down into Mureung Valley — the best of the mountain in one day. Allow generous time and fitness.'),
    segs=[
     (1, ('댓재휴게소 → 두타산 정상', 'Datjae → Dutasan summit'), '약 2.7km', '1.5~2시간',
      ('최단 코스를 그대로 정상까지. 여기까지는 가볍다 — 종주의 본론은 다음 구간이다.',
       'Up the short route to the summit — the easy part; the traverse proper starts beyond.'), 25, 'tip',
      ('댓재 주차장에 차를 두고 무릉계로 복귀할 교통편을 미리 정한다.',
      'Leave a car plan: how you get back from Mureung to Datjae.')),
     (2, ('정상 → 베틀봉', 'Summit → Byeolbong'), '약 3km', '1.5~2시간',
      ('동쪽 능선으로 접어 베틀봉까지 이어진다. 숲길과 암반 구간이 반복되는 본격 능선 산행이다.',
       'Turn east along the ridge to Byeolbong — forest and rock alternating, proper ridge walking.'), 55, 'warn',
      ('능선 중간 이탈로가 거의 없다 — 컨디션 난조 시 되돌아오는 것도 고려하라.',
      'Few escape routes mid-ridge — factor in turning back if form fades.')),
     (3, ('베틀봉 → 베틀바위 → 마천루', 'Byeolbong → Byeotul Rock → Macheonru'), '약 3.5km', '2~2.5시간',
      ('두타산 비경의 연속. 베틀바위 장대한 바위벼랑과 마천루 거대 암석을 거친다.',
       'The highlight run: the long Byeotul cliff band and the great Macheonru boulder.'), 80, 'warn',
      ('암릉 구간 장갑 필수. 우천·강풍 시 이 구간부터 통제한다고 보자.',
      'Gloves mandatory; treat this section as closed in wind or rain.')),
     (4, ('마천루 → 무릉계 하산', 'Macheonru → Mureung descent'), '약 2.8km', '1.5~2시간',
      ('산성폭포를 지나 무릉계로 내려온다. 다리가 뻐근할 무렵 계곡 경관이 피로를 풀어준다.',
       'Past Sanseong Falls into the valley — gorge scenery soothes tired legs.'), 100, 'tip',
      ('무릉계에서 동해 시내로 복귀하는 버스는 막차가 이르다 — 시간을 확인한다.',
      'The Mureung–Donghae bus runs early — check the last departure.')),
    ],
    cps=[
     ('댓재휴게소', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 680m', '0km', ('주차장·매점', 'Parking, shop')),
     ('두타산', ('정상', 'Summit'), 'badge-summit', '1,357m', '2.7km', ('삼각점', 'Triangulation post')),
     ('베틀봉', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 1,200m', '5.7km', ('전망', 'Viewpoint')),
     ('베틀바위·마천루', ('비경', 'Crag wonder'), 'badge-landmark', '해발 약 1,050m', '9.2km', ('암릉 전망', 'Cliff viewpoint')),
     ('무릉계 유원지', ('도착', 'Finish'), 'badge-trailhead', '해발 약 150m', '12km', ('주차장·화장실', 'Parking, restrooms')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·장갑·물 2L·헤드램프. 하루 종일 걷는 구간이다.', 'Hiking shoes, gloves, 2 L water, headlamp — a whole day on the move.')),
     ('book', ('입산', 'Entry'), ('허가 불필요. 종주라 원점 회귀가 아니다 — 차량 셔틀 또는 버스 시간을 사전 확인한다.',
      'No permit, but it is point-to-point — arrange a shuttle or check buses in advance.')),
     ('shield', ('주의', 'Cautions'), ('암릉 연속 구간에서 사고가 잦다 — 우천·강풍·결빙일에는 취소가 정답이다.',
      'The crag section has a real accident record — canceling in wind, rain or ice is the right call.')),
    ],
    elev_path='M20 165 C150 150, 280 105, 420 80 S560 70, 640 90 S700 130, 740 160', elev_peak=(420, 80), elev_label='1,357m',
    map_note='댓재~무릉계 종주', map_start='댓재', map_end='무릉계',
    map_path='M120 90 C240 110, 340 150, 460 200 S620 300, 680 340', map_nodes=[(120, 90, 10), (460, 200, 8), (680, 340, 12)]),
  ]),
 'manisan': dict(
  ko_name='마니산', en_name='Manisan', alt='469m', region='인천', en_region='Incheon',
  lat=37.5970, lng=126.4750,
  intro_ko='강화도의 최고봉 469m. 정상 참성단(천제단)은 단군제천의 전설지이며, 삼랑성과 고려의 산성 유적이 어우러진 역사의 산입니다.',
  intro_en='Ganghwa Island\'s highest peak at 469 m. The summit altar Chanseongdan (Cheonjedan) carries the Dangun legend, woven with the Samnangseong fortress remains — a mountain of history.',
  permit=('관광지 요금', 'Site fee'),
  courses=[
   dict(id='beginner', color='green', hexc='#6a7d4c', meter=2, level=('초급', 'Beginner'),
    name=('단군로 순환', 'Dangun-ro Circuit'),
    dist=('약 5.2km', '~5.2 km'), time=('3시간 내외', 'About 3 h'),
    flow=('마니산 관광지 매표소', '천사계단로', '참성단 469m', '단군로 372계단', '매표소'),
    desc=('마니산의 대표 코스. 국민관광지 매표소에서 천사계단로를 따라 참성단에 오르고, 372계단 단군로로 '
          '내려오는 순환 산행. 단군 신앙의 산을 가장 효율적으로 둘러본다.',
          'The signature Manisan circuit: from the gate past the Heaven Stairs to Chanseongdan summit and down the 372-step Dangun-ro — the most efficient round of the mountain of Dangun worship.'),
    segs=[
     (1, ('매표소 → 천사계단로', 'Gate → Heaven Stairs'), '약 1.5km', '40~50분',
      ('국민관광지 입구에서 숲길로 오른다. 계단과 완경사가 반복되는 접근 구간이다.',
       'A forested approach of steps and gentle pitches from the park gate.'), 25, 'tip',
      ('관광지 요금·개방시간은 강화군 안내를 이용 전 확인한다.', 'Check Ganghwa County notices for the site fee and opening hours.')),
     (2, ('천사계단로 → 참성단', 'Heaven Stairs → Chanseongdan'), '약 1.2km', '50~70분',
      ('계단길이 본격화되며 정상 참성단(해발 469m)에 닿는다. 단군이 제천을 지냈다는 평평한 단상이 서 있다.',
       'The stairway proper leads to Chanseongdan (469 m), the flat altar of the Dangun legend.'), 60, 'warn',
      ('참성단 일대는 바람이 강하다 — 모자를 고정하자.', 'It is windy at the altar — secure your hat.')),
     (3, ('참성단 조망', 'At the altar'), '—', '20~30분',
      ('서해와 강화 해협이 열려 보인다. 장방형 단상과 고찰터를 한 바퀴 돌며 조망한다.',
       'The Yellow Sea and Ganghwa Strait open below; circle the rectangular altar and old shrine site.'), 85, 'tip',
      ('기상이 맑으면 북한산까지 보인다는 기록도 있다.', 'On clear days the view is said to reach Bukhansan.')),
     (4, ('단군로 372계단 하산', 'Dangun-ro descent, 372 steps'), '약 2.5km', '1~1.5시간',
      ('372계단 단군로를 따라 매표소로 내려온다. 계단 하산이라 무릎에 부담 — 지팡이가 유용하다.',
       'Down the 372-step Dangun-ro to the gate — knees will feel it; poles help.'), 100, 'tip',
      ('하산 후 강화 읍내의 향토 음식이 좋은 마무리다.', 'Finish with Ganghwa town food after the descent.')),
    ],
    cps=[
     ('마니산 관광지 매표소', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 60m', '0km', ('주차장·화장실·매점', 'Parking, restrooms, shops')),
     ('천사계단로', ('경유', 'Waypoint'), 'badge-shelter', '해발 약 250m', '1.5km', ('쉼터', 'Rest point')),
     ('참성단', ('정상', 'Summit'), 'badge-summit', '469m', '2.7km', ('단상·안내판', 'Altar, signboards')),
     ('매표소', ('도착', 'Finish'), 'badge-trailhead', '해발 약 60m', '5.2km', ('주차장', 'Parking')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·물 1L·지팡이. 계단 구간이 많아 무릎 보호가 관건이다.', 'Hiking shoes, 1 L water, poles — it is a stair-heavy descent.')),
     ('book', ('입산', 'Entry'), ('국민관광지로 운영 — 요금·참성단 개방시간은 이용 전 강화군 안내를 확인한다.',
      'Managed as a public tourist site — check the fee and altar opening hours with Ganghwa County first.')),
     ('shield', ('주의', 'Cautions'), ('계단 하산 시 무릎 부담이 크다 — 천천히, 측면으로 딛는 요령이 도움이 된다.',
      'Step-downs load the knees — go slow, land sideways.')),
    ],
    elev_path='M20 190 C160 175, 300 130, 450 90 S620 55, 740 46', elev_peak=(740, 46), elev_label='469m',
    map_note='마니산 순환', map_start='매표소', map_end='참성단',
    map_path='M120 340 C230 315, 330 265, 450 205 S620 95, 680 60 S600 230, 430 290 S230 350, 120 340', map_nodes=[(120, 340, 10), (450, 205, 8), (680, 60, 12), (120, 340, 10)]),
   dict(id='intermediate', color='blue', hexc='#456e96', meter=3, level=('중급', 'Intermediate'),
    name=('정수사~참성단 왕복', 'Jeongsusa–Chanseongdan Round Trip'),
    dist=('약 3.4km', '~3.4 km'), time=('2.5~3시간', '2.5–3 h'),
    flow=('정수사', '숲길 능선', '참성단 469m', '정수사'),
    desc=('고즈넉한 정수사 경내를 지나 주능선 바위 구간을 타고 참성단에 오르는 등반가의 코스. '
          '편도 약 1.7km의 짧은 거리에 능선 바위타기가 응축되어 있다.',
          'The climber\'s route: through the quiet Jeongsusa temple grounds and up the main-ridge rock section to the altar — only 1.7 km each way but packed with rock scrambling.'),
    segs=[
     (1, ('정수사 → 숲길', 'Jeongsusa → forest trail'), '약 0.6km', '15~25분',
      ('천 년 사찰 정수사 경내를 지나 뒷산 숲길로 접어든다. 사찰의 종소리와 함께 시작하는 산행이다.',
       'Pass through the thousand-year-old Jeongsusa and enter the forest behind — a temple-bell start.'), 20, 'tip',
      ('정수사 주차는 협소하다 — 이른 아침 방문이 좋다.', 'Jeongsusa parking is tight — come early.')),
     (2, ('숲길 → 능선 바위 구간', 'Forest → ridge rocks'), '약 0.7km', '40~60분',
      ('능선이 시작되며 바위타기가 나온다. 손발을 함께 쓰는 구간이 이어진다.',
       'The ridge begins and the scrambling starts — hands and feet together.'), 55, 'warn',
      ('바위 구간은 우천 시 통행이 어렵다 — 비 예보 시 단군로로 변경한다.',
      'Rock sections are unusable in rain — switch to Dangun-ro if wet.')),
     (3, ('주능선 → 참성단', 'Main ridge → Chanseongdan'), '약 0.4km', '30~40분',
      ('바다 조망과 함께 주능선 약 2km 구간의 정점인 참성단에 도달한다.',
       'With the sea in view, the main ridge tops out at the Chanseongdan altar.'), 85, 'tip',
      ('참성단에서 단군로 쪽 풍경도 보고 하산하자.', 'Look over toward Dangun-ro from the altar before descending.')),
     (4, ('참성단 → 정수사 하산', 'Altar → Jeongsusa descent'), '약 1.7km', '1~1.5시간',
      ('올라온 능선을 따라 정수사로 내려온다. 바위 구간 하산은 오르막보다 딛는 발이 중요하다.',
       'Down the same ridge to Jeongsusa — on rocks the placement of each step matters more than on the climb.'), 100, 'warn',
      ('하산 후 정수사에서 짧은 참배로 마무리하자.', 'Pay a short visit at Jeongsusa to finish.')),
    ],
    cps=[
     ('정수사', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 100m', '0km', ('사찰·주차(협소)', 'Temple, limited parking')),
     ('능선 바위 구간', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 300m', '1.3km', ('없음', 'None')),
     ('참성단', ('정상', 'Summit'), 'badge-summit', '469m', '1.7km', ('단상·전망', 'Altar, viewpoint')),
     ('정수사', ('도착', 'Finish'), 'badge-trailhead', '해발 약 100m', '3.4km', ('사찰', 'Temple')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·장갑. 바위타기 구간이 있어 가방을 작게 꾸린다.', 'Hiking shoes and gloves; keep the pack small for the scrambling.')),
     ('book', ('입산', 'Entry'), ('정수사 코스도 관광지 운영 구간에 속한다 — 요금 체계를 매표소에서 확인한다.',
      'The Jeongsusa route is inside the managed site — confirm the fee scheme at the gate.')),
     ('shield', ('주의', 'Cautions'), ('능선 바위 구간은 결빙 시 절대 통행 금지 — 겨울에는 단군로만 이용한다.',
      'Never take the rock ridge on ice — winter means Dangun-ro only.')),
    ],
    elev_path='M20 185 C170 170, 300 125, 450 85 S620 50, 740 44', elev_peak=(740, 44), elev_label='469m',
    map_note='정수사~참성단', map_start='정수사', map_end='참성단',
    map_path='M110 350 C230 320, 340 270, 460 215 S630 95, 690 60', map_nodes=[(110, 350, 10), (460, 215, 8), (690, 60, 12)]),
   dict(id='advanced', color='red', hexc='#9f5845', meter=4, level=('고급', 'Advanced'),
    name=('함허동천 방면 능선 종주', 'Hamheodongcheon Ridge Traverse'),
    dist=('약 7km', '~7 km'), time=('4~5시간', '4–5 h'),
    flow=('함허동천', '주능선', '참성단 469m', '정수사'),
    desc=('함허동천 계곡에서 주능선으로 접어 참성단을 거쳐 정수사로 종주하는 코스로 알려져 있다. '
          '계곡·능선·바위·사찰을 한 번에 모은 마니산의 알짜 구간이다. 접근 교통은 원점 회귀가 불편하므로 사전 계획이 필요하다.',
          'From the Hamheodongcheon valley onto the main ridge, over the altar and down to Jeongsusa — valley, ridge, rock and temple in one. The point-to-point shape needs transport planning.'),
    segs=[
     (1, ('함허동천 → 능선 접합부', 'Hamheodongcheon → ridge junction'), '약 2km', '1~1.5시간',
      ('거대 암석과 계곡 경관으로 이름 높은 함허동천에서 숲길로 능선에 오른다.',
       'Climb from the boulder-famed Hamheodongcheon valley to the ridge on a forest path.'), 30, 'tip',
      ('함허동천까지는 버스·자전거 접근이 가능하나 배차가 드물다.', 'Buses reach Hamheodongcheon but run infrequently.')),
     (2, ('주능선 → 참성단', 'Main ridge → Chanseongdan'), '약 2.5km', '1.5~2시간',
      ('마니산 주능선의 바위와 숲을 반복하며 참성단에 오른다. 정수사 코스보다 길고 고요한 능선이다.',
       'The long, quiet main ridge alternates rock and forest to the altar — longer than the Jeongsusa line.'), 70, 'warn',
      ('능선 구간 이탈로가 드물다 — 갈림길마다 위치를 확인한다.',
      'Escape trails are sparse — recheck your position at every junction.')),
     (3, ('참성단 → 정수사 하산', 'Altar → Jeongsusa descent'), '약 1.7km', '1~1.5시간',
      ('정수사 능선길의 바위 구간을 따라 내려온다. 종주 마무리 구간에도 집중이 필요하다.',
       'Descend the Jeongsusa ridge rocks — focus to the end of the traverse.'), 95, 'warn',
      ('일몰이 가까우면 서두르지 말고 계단로(단군로)로 전환하는 것이 안전하다.',
      'Near dusk, switch to the stepped Dangun-ro rather than rushing.')),
     (4, ('정수사에서 마무리', 'Finish at Jeongsusa'), '—', '20~30분',
      ('정수사 경내에서 종주를 마무리한다. 강화 버스터미널 방면 복귀 교통을 확인한다.',
       'Close the traverse at Jeongsusa and check the return transport toward Ganghwa terminal.'), 100, 'tip',
      ('터미널 방면 버스는 배차 간격이 크다 — 시간표를 미리 확인한다.',
      'Terminal buses are infrequent — check the timetable first.')),
    ],
    cps=[
     ('함허동천', ('출발', 'Trailhead'), 'badge-trailhead', '해발 약 80m', '0km', ('계곡·주차', 'Valley, parking')),
     ('주능선', ('경유', 'Waypoint'), 'badge-landmark', '해발 약 350m', '2.5km', ('없음', 'None')),
     ('참성단', ('정상', 'Summit'), 'badge-summit', '469m', '4.5km', ('단상·전망', 'Altar, viewpoint')),
     ('정수사', ('도착', 'Finish'), 'badge-trailhead', '해발 약 100m', '7km', ('사찰', 'Temple')),
    ],
    tips=[
     ('backpack', ('준비물', 'Gear'), ('트레킹화·장갑·물 1.5L·헤드램프. 종주형이라 배낭을 완비한다.', 'Hiking shoes, gloves, 1.5 L water, headlamp — a full traverse kit.')),
     ('book', ('입산', 'Entry'), ('관광지 운영 구간을 지난다 — 출발점별 요금 체계가 다를 수 있으니 이용 전 확인한다.',
      'You pass through the managed site — fees may differ by trailhead; check first.')),
     ('shield', ('주의', 'Cautions'), ('원점 회귀가 아닌 종주 — 귀가 교통편을 확정하지 않으면 출발하지 않는다.',
      'Point-to-point: do not start until your return transport is settled.')),
    ],
    elev_path='M20 195 C150 180, 280 140, 420 100 S560 60, 660 50 S710 90, 740 120', elev_peak=(660, 50), elev_label='469m',
    map_note='함허동천~정수사 종주', map_start='함허동천', map_end='정수사',
    map_path='M130 80 C240 110, 340 160, 460 215 S620 320, 670 350', map_nodes=[(130, 80, 10), (460, 215, 8), (670, 350, 12)]),
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

for mid, d in F5.items():
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

_credits = _json.load(open(_pl.Path(__file__).parent / 'k100v5_credits.json'))
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
