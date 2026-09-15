import sys, re, pathlib
# -*- coding: utf-8 -*-
"""히말라야 카테고리 3트레킹(EBC·ACT·랑탕) 콘텐츠.

사실 근거 (2026-09 세션 검색): EBC — 사가르마타 국립공원 3,000루피 + 쿰부 파스랑
라무 지자체 허가 3,000루피, TIMS(대행사 발급), 가이드 의무(2023-04~), 12일 표준,
남체 3,440m·딩보체 4,410m 적응일, EBC 5,364m·칼라파타르 5,545m. ACT — ACAP 3,000루피,
12~17일, 토롱라 5,416m, 마낭 3,540m 적응. 랑탕 — 랑탕 국립공원 3,000루피, 7~10일,
캰진곰파 3,870m·체르코리 4,984m. 네팔 비상전화 100/102/112, 시즌 3~5월·10~11월.
"""
YUSHAN = pathlib.Path('yushan-playbook.html').read_text(encoding='utf-8')
YUSHAN_EN = pathlib.Path('en/yushan-playbook.html').read_text(encoding='utf-8')
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

def seg(no, title, km, time, body, bar, tip_kind, tip_text):
    tip = (f'<div class="{tip_kind}"><svg class="icon-svg"><use href="{IC}#icon-{"warning" if tip_kind=="warn" else "tip"}"></use></svg> {tip_text}</div>')
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
        cps = ''.join(cp(n+1, *x) for n, x in enumerate(c['cps']))
        out.append(f'''<section class="panel {c['color']}{active}" id="{c['id']}"><div class="panel-top"><span class="level"><svg class="icon-svg"><use href="{IC}#icon-season"></use></svg> {c['level']}</span><div><div class="panel-name">{c['name']}</div><div class="panel-sub">{c['sub']}</div></div></div><div class="tabs"><button class="tab active" data-tab="overview"><svg class="icon-svg"><use href="{IC}#icon-prep"></use></svg> {c['tabs'][0]}</button><button class="tab" data-tab="route"><svg class="icon-svg"><use href="{IC}#icon-book"></use></svg> {c['tabs'][1]}</button><button class="tab" data-tab="map"><svg class="icon-svg"><use href="{IC}#icon-location"></use></svg> {c['tabs'][2]}</button><button class="tab" data-tab="tips"><svg class="icon-svg"><use href="{IC}#icon-tip"></use></svg> {c['tabs'][3]}</button></div>
<div class="playbook-split-container"><div class="playbook-main-col"><div class="tabpane active" data-pane="overview"><div class="course-stats-summary">
{c['pills']}
</div><div class="section-title"><h2>{c['h_flow']}</h2><div class="line"></div></div><div class="card"><div class="flow">{flow}</div></div><div class="section-title"><h2>{c['h_elev']}</h2><div class="line"></div></div><div class="card elev">{elev_svg('g'+c['id']+c['color'][:2], c['hex'], c['elev_label'], c['elev_path'], c['elev_peak'])}</div><p class="desc">{c['desc']}</p></div><div class="tabpane" data-pane="route"><div class="section-title"><h2>{c['h_route']}</h2><div class="line"></div></div><div class="segments">{segs}</div></div><div class="tabpane" data-pane="tips"><div class="tips-grid">{tips}</div></div></div><div class="playbook-sidebar-col"><div class="tabpane" data-pane="map"><div class="section-title"><h2>{c['h_map']}</h2><div class="line"></div></div><div class="card map">{map_svg(c['hex'], c['map_note'], c['map_start'], c['map_end'], c['map_path'], c['map_nodes'])}</div><div class="section-title"><h2>{c['h_cp']}</h2><div class="line"></div></div><div class="checkpoint-timeline">
{cps}
</div></div></div></div>
</section>''')
    return '\n'.join(out)

def build(mountain, lang):
    global L
    L = lang
    src = YUSHAN if lang == 'ko' else YUSHAN_EN
    pfx = '' if lang == 'ko' else '../'
    T = CONTENT[mountain][lang]

    t = src
    t = re.sub(r'<title>[^<]*</title>', f'<title>{T["title"]}</title>', t, count=1)
    t = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{T["meta"]}" name="description"/>', t, count=1)
    t = t.replace('assets/img/yushan/og.png', f'{pfx}assets/img/{mountain}/og.png')
    if lang == 'ko':
        t = t.replace('href="en/yushan-playbook.html"', f'href="en/{mountain}-playbook.html"')
        t = t.replace('yushan-playbook.html', f'{mountain}-playbook.html')
    else:
        t = t.replace('../yushan-playbook.html', f'../{mountain}-playbook.html')
        t = t.replace('<html data-theme="light" lang="ko">', '<html data-theme="light" lang="en">')
        t = t.replace('href="yushan-playbook.html" hreflang="en"', f'href="{mountain}-playbook.html" hreflang="en"')
        t = t.replace('href="en/yushan-playbook.html" hreflang="en"', f'href="{mountain}-playbook.html" hreflang="en"')

    t = re.sub(r'<h1>[^<]*</h1><p>[^<]*</p>', f'<h1>{T["h1_card"]}</h1><p>{T["p_card"]}</p>', t, count=1)

    hero_start = t.find('<section class="hero hero-bleed">')
    main_idx = t.find('<main class="wrap">', hero_start)
    hero_html = f'''<section class="hero hero-bleed">
<picture class="hero-picture" id="heroFallbackImage">
<source sizes="100vw" srcset="{pfx}assets/img/{mountain}/hero-640.avif 640w, {pfx}assets/img/{mountain}/hero-1024.avif 1024w, {pfx}assets/img/{mountain}/hero-1600.avif 1600w, {pfx}assets/img/{mountain}/hero-2400.avif 2400w" type="image/avif"/>
<source sizes="100vw" srcset="{pfx}assets/img/{mountain}/hero-640.webp 640w, {pfx}assets/img/{mountain}/hero-1024.webp 1024w, {pfx}assets/img/{mountain}/hero-1600.webp 1600w, {pfx}assets/img/{mountain}/hero-2400.webp 2400w" type="image/webp"/>
<img alt="{T['hero_alt']}" class="hero-img" sizes="100vw" src="{pfx}assets/img/{mountain}/hero-1600.jpg" srcset="{pfx}assets/img/{mountain}/hero-640.jpg 640w, {pfx}assets/img/{mountain}/hero-1024.jpg 1024w, {pfx}assets/img/{mountain}/hero-1600.jpg 1600w, {pfx}assets/img/{mountain}/hero-2400.jpg 2400w"/>
</picture>
<div class="hero-overlay"></div>
<div class="hero-content">
<div class="hero-badge"><svg class="icon-svg"><use href="{pfx}assets/icons/icons.svg#icon-mountain"></use></svg> {T['badge']}</div>
<h1 style="color: var(--hero-text); font-family: var(--font-display); font-size: var(--text-2xl); font-weight: 800; line-height: 1.15; margin-bottom: var(--space-4);">{T['h1']}</h1>
<p style="color: var(--hero-text-muted); font-size: var(--text-base); line-height: 1.6; max-width: 56ch; margin: 0 auto var(--space-8);">
      {T['hero_desc']}
    </p>
<div class="selector" style="justify-content: center; margin-top: var(--space-6); margin-bottom: var(--space-4);">
<button class="course-btn active green" data-course="beginner"><svg class="icon-svg"><use href="{pfx}assets/icons/icons.svg#icon-season"></use></svg> {T['btn1']}</button>
<button class="course-btn blue" data-course="intermediate"><svg class="icon-svg"><use href="{pfx}assets/icons/icons.svg#icon-chart"></use></svg> {T['btn2']}</button>
<button class="course-btn red" data-course="advanced"><svg class="icon-svg"><use href="{pfx}assets/icons/icons.svg#icon-mountain"></use></svg> {T['btn3']}</button>
</div>
</div>
<div class="photo-credit hero-credit">
<span class="credit-author">Photo by <a href="{T['hero_url']}" rel="noopener" target="_blank">{T['hero_photographer']}</a></span>
<span class="credit-divider">/</span>
<span class="credit-source"><a href="https://unsplash.com" rel="noopener" target="_blank">Unsplash</a></span>
</div>
</section>
'''
    t = t[:hero_start] + hero_html + t[main_idx:]

    panels_start = t.find('<section class="panel')
    panels_end = t.find('</main>', panels_start)
    t = t[:panels_start] + panels(COURSES[mountain][lang]) + '\n' + t[panels_end:]

    gal_start = t.find('<section class="photo-gallery-section">')
    gal_end = t.find('</section>', gal_start) + len('</section>')
    items = []
    for i, (name, title, cap) in enumerate(T['gallery']):
        items.append(f'''<button aria-haspopup="dialog" aria-label="{title} {T['lb_zoom']}" class="gallery-item" data-credit="{cap}" data-index="{i}">
<picture class="gallery-picture">
<source srcset="{pfx}assets/img/{mountain}/{name}.avif" type="image/avif"/>
<source srcset="{pfx}assets/img/{mountain}/{name}.webp" type="image/webp"/>
<img alt="" class="gallery-img" decoding="async" loading="lazy" src="{pfx}assets/img/{mountain}/{name}.jpg"/>
</picture>
<div class="gallery-caption-overlay">
<span class="gallery-caption-text">{title}</span>
</div>
</button>''')
    gal_html = f'''<section class="photo-gallery-section">
<h2 class="section-title" style="margin-bottom:var(--space-4);font-family:var(--font-display);font-size:var(--text-lg);font-weight:800;">
<span class="section-title-icon"><svg class="icon-svg"><use href="{pfx}assets/icons/icons.svg#icon-camera"></use></svg></span> {T['gal_title']}
  </h2>
<div class="gallery-grid">
{chr(10).join(items)}
</div>
</section>'''
    t = t[:gal_start] + gal_html + t[gal_end:]

    t = t.replace('data-mountain="yushan"', f'data-mountain="{mountain}"', 1)
    t = t.replace('../../assets/img/', '../assets/img/')
    return t

# ── 히말라야 콘텐츠 ──
CONTENT = {}
COURSES = {}

def _mk(mid, lang, T, courses, region_en, country):
    ko = lang == 'ko'
    CONTENT.setdefault(mid, {})[lang] = dict(T)
    COURSES.setdefault(mid, {})[lang] = courses

# ── EBC ──
T_EBC_KO = dict(
  title='에베레스트 베이스캠프 트레킹 플레이북',
  meta='네팔 에베레스트 베이스캠프(EBC 5,364m) 트레킹 가이드. 남체·딩보체 고도 적응이 포함된 12일 표준 일정의 상세 경로, 허가, 실사 지도 및 팁을 제공합니다.',
  h1_card='에베레스트 베이스캠프', p_card='EBC · 세계 최고의 트레킹 5,364m · 네팔 솔루쿰부',
  hero_alt='기도 깃발과 눈 덮인 히말라야 산맥의 장엄한 풍경',
  badge='EBC 트레킹 플레이북', h1='에베레스트 베이스캠프 트레킹 플레이북',
  hero_desc='세계에서 가장 유명한 트레킹, 에베레스트 베이스캠프(5,364m) 가이드. 남체·딩보체 고도 적응과 허가·비용·안전 팁을 정리했습니다.',
  btn1='초급: 남체 적응 구간', btn2='중급: EBC 표준 12일', btn3='고급: 칼라파타르+고키요 연장',
  hero_photographer='Geetangey', hero_url='https://unsplash.com/photos/dQ2Qkc8ke38',
  gal_title='EBC의 사계 &amp; 명소', lb_zoom='크게 보기',
  gallery=[
   ('g1','설산 정상 등반','Unsplash'), ('g2','백팩 트레킹','Unsplash'),
   ('g3','불교 문과 산맥','Unsplash'), ('g4','베이스캠프 텐트','Unsplash')],
)
T_EBC_EN = dict(
  title='Everest Base Camp Trek Playbook',
  meta='Guide to the Everest Base Camp trek (5,364 m), Nepal — a 12-day standard itinerary with Namche and Dingboche acclimatization, permits, maps, and tips.',
  h1_card='Everest Base Camp', p_card='EBC · The world\'s great trek, 5,364 m · Khumbu, Nepal',
  hero_alt='Prayer flags and snow-capped Himalayan peaks',
  badge='EBC Trek Playbook', h1='Everest Base Camp Trek Playbook',
  hero_desc='A guide to the world\'s most famous trek — Everest Base Camp (5,364 m). Acclimatization at Namche and Dingboche, permits, costs, and safety tips.',
  btn1='Beginner: Namche Section', btn2='Intermediate: Standard 12-Day EBC', btn3='Advanced: Kala Patthar + Gokyo',
  hero_photographer='Geetangey', hero_url='https://unsplash.com/photos/dQ2Qkc8ke38',
  gal_title='EBC Four Seasons &amp; Attractions', lb_zoom='View larger',
  gallery=[
   ('g1','Snow summit climb','Unsplash'), ('g2','Trekking with a backpack','Unsplash'),
   ('g3','Buddhist gate & peaks','Unsplash'), ('g4','Base camp tents','Unsplash')],
)

C_EBC = {
 'ko': [
  dict(id='beginner', color='green', hex='#6a7d4c', level='초급', meter=3,
    name='루클라~남체 바자르 적응 구간', sub='루클라 2,840m → 남체 바자르 3,440m · 약 20km · 4~5일',
    tabs=['개요','경로 안내','지도','팁 &amp; 주의'],
    pills=pill('ruler','거리','약 20km')+pill('clock','일정','4~5일')+pill('location','남체','3,440m')+pill_meter('난이도',3,'medium')+pill('star','시즌','3~5월·10~11월')+pill('location','허가','2종'),
    h_flow='코스 흐름', h_elev='고도 프로파일', h_route='구간별 경로 안내', h_map='코스 개념도', h_cp='체크포인트 표',
    flow=['루클라 2,840m','파크딩 2,610m','남체 바자르 3,440m','적응 하이킹'],
    elev_label='남체 바자르 3,440m', elev_path='M20 165 C170 155, 320 125, 470 95 S640 70, 740 55', elev_peak=(740,55),
    desc='EBC 트레킹의 입문 구간입니다. 루클라에서 출발해 두다코시 계곡을 따라 히말라야 명물 티하우스 마을 남체 바자르(3,440m)까지 오르며 고도 적응의 기초를 다집니다.',
    segs=[('출','루클라 도착','0km','—','카트만두~루클라 항공(약 35분) 후 출발합니다. 항공편은 날씨 영향이 큽니다.','15','tip','루클라 항공편 지연에 대비해 일정 여유를 두세요.'),('1','루클라 → 파크딩','약 8km','3~4시간','두다코시 계곡을 따라 내려갔다가 파크딩에서 취침합니다.','45','tip','첫날은 가볍게 시작해 몸을 적응시킵니다.'),('2','파크딩 → 남체 바자르','약 8km','5~6시간','히말라야 국립공원 게이트(몬조)를 지나 남체 바자르로 오릅니다. 첫 고산 체크포인트입니다.','85','warn','3,000m를 넘으며 두통·구역이 오면 속도를 늦추세요.'),('하','남체 적응일','—','1일','에베레스트 뷰 호텔 방면 적응 하이킹(오르고 자는 원칙).','—','tip','적응일은 선택이 아니라 필수입니다.')],
    tips=[('backpack','준비물',['수면배깅(-10°C 등급)','헤드랜턴·보조전지','고산 약(의사 상담)','현금(산내 카드 불가)']),('book','허가·비용',['사가르마타 국립공원 3,000루피','쿰부 지자체 허가 3,000루피','가이드 필수(대행사 예약)·패키지 $1,200~2,000']),('shield','주의',['고산 질환(하산이 치료)','루클라 항공 지연','야간 한랭(-10°C 이하)'])],
    cps=[('루클라','출발점','badge-trailhead','2,840m','0km','공항·티하우스'),('몬조 게이트','허가 확인','badge-trailhead','2,835m','약 10km','국립공원 게이트'),('남체 바자르','적응 거점','badge-shelter','3,440m','약 20km','티하우스·병원'),('에베레스트 뷰 하이킹','적응','badge-landmark','3,880m','당일 왕복','전망대')],
    map_note='EBC 입문 적응 구간', map_start='루클라 2,840m', map_end='남체 3,440m',
    map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55', map_nodes=[(110,335,10),(460,210,8),(695,55,12)]),
  dict(id='intermediate', color='blue', hex='#456e96', level='중급', meter=4,
    name='EBC 표준 12일 트레킹', sub='루클라 → 남체·딩보체 적응 → EBC 5,364m · 약 130km · 12일',
    tabs=['개요','경로 안내','지도','팁 &amp; 주의'],
    pills=pill('ruler','거리','약 130km')+pill('clock','일정','12일')+pill('location','EBC','5,364m')+pill_meter('난이도',4,'hard')+pill('star','적응일','2일(남체·딩보)')+pill('location','가이드','필수'),
    h_flow='코스 흐름', h_elev='고도 프로파일', h_route='구간별 경로 안내', h_map='코스 개념도', h_cp='체크포인트 표',
    flow=['루클라','남체 3,440m','딩보체 4,410m','로부체 4,940m','고락섭 5,160m','EBC 5,364m','하산'],
    elev_label='EBC 5,364m', elev_path='M20 195 C170 188, 320 162, 470 126 S640 68, 740 40', elev_peak=(740,40),
    desc='에베레스트 베이스캠프까지 왕복하는 세계적인 트레킹의 표준 12일 일정입니다. 남체(3,440m)·딩보체(4,410m) 2회의 적응일이 안전의 핵심이며, 티하우스 숙박과 가이드 동반이 표준입니다.',
    segs=[('1~3일','루클라 → 남체 바자르','약 20km','3일','두다코시 계곡을 따라 남체로 오르고 1일 적응(에베레스트 뷰 하이킹)을 소화합니다.','30','tip','적응일 하이킹은 「높이 올라 낮게 잔다」 원칙으로 소화합니다.'),('4~6일','남체 → 딩보체','약 20km','3일','텡보체 사원과 아마답람을 거쳐 딩보체(4,410m)에서 2일차 적응을 합니다.','55','warn','딩보체 이후에는 증상에 따라 일정을 조정하세요. 무리하지 않는 것이 최선입니다.'),('7~8일','딩보체 → 로부체 → 고락섭','약 15km','2일','부고산 능선을 지나 로부체(4,940m)에 도착, 고락섭(5,160m)에서 1박합니다.','80','warn','4,900m 이상 구간은 수면 장애가 흔합니다. 약물·행동 요령을 준비하세요.'),('9일','EBC 5,364m 도달','왕복 약 4km','6~8시간','고락섭에서 베이스캠프까지 왕복한 뒤 고락섭으로 복귀합니다. EBC 기념비 암석이 명소입니다.','95','warn','고산 기상이 빠르게 변합니다. 정오 이후 운행은 피하세요.'),('10~12일','하산 → 루클라','약 60km','3일','페리체·남체를 거쳐 빠르게 하산한 뒤 루클라에서 비행기로 복귀합니다.','30','tip','하산 2일 단축도 가능하나 발·무릎 상태를 보고 판단하세요.')],
    tips=[('backpack','준비물',['수면배깅(-15°C 등급)','등산화·게이터','방한 의류 세트','정화 태블릿·간식']),('book','허가·예약',['공원+지자체 허가 약 6,000루피','대행사 패키지 $1,200~2,000','루클라 항공 왕복 ~$400 별도']),('shield','주의',['고산 질환 즉시 하산','기상 악화 시 일정 조정','보험(항공 이송 포함) 필수'])],
    cps=[('루클라','출발점','badge-trailhead','2,840m','0km','공항·티하우스'),('남체 바자르','적응','badge-shelter','3,440m','3일차','티하우스·병원'),('딩보체','적응','badge-shelter','4,410m','6일차','티하우스'),('고락섭','숙박','badge-shelter','5,160m','8일차','티하우스'),('EBC 5,364m','도달','badge-summit','5,364m','9일차','기념비')],
    map_note='EBC 표준 12일 루트', map_start='루클라 2,840m', map_end='EBC 5,364m',
    map_path='M95 345 C210 332, 320 300, 430 255 S630 90, 705 50', map_nodes=[(95,345,10),(430,255,8),(705,50,12)]),
  dict(id='advanced', color='red', hex='#9f5845', level='고급', meter=5,
    name='칼라파타르+고키요 연장 14~16일', sub='EBC + 칼라파타르 5,545m + 고키요 호수 · 약 160km+',
    tabs=['개요','경로 안내','지도','팁 &amp; 주의'],
    pills=pill('ruler','거리','약 160km+')+pill('clock','일정','14~16일')+pill('location','칼라파타르','5,545m')+pill_meter('난이도',5,'hard')+pill('star','연장','고키요 호수')+pill('location','고도','최대 5,545m'),
    h_flow='코스 흐름', h_elev='고도 프로파일', h_route='구간별 경로 안내', h_map='코스 개념도', h_cp='체크포인트 표',
    flow=['EBC 표준','칼라파타르 5,545m','촐라체 고개','고키요 호수','하산'],
    elev_label='칼라파타르 5,545m', elev_path='M20 195 C170 190, 320 168, 470 132 S640 66, 740 40', elev_peak=(740,40),
    desc='EBC 표준 일정에 칼라파타르(5,545m) 새벽 등반과 고키요 호수(4,700~5,000m) 연장을 더한 완성형 루트입니다. 에베레스트의 가장 아름다운 파노라마를 두 번 볼 수 있습니다.',
    segs=[('1~9일','EBC 표준 구간','약 65km','9일','표준 12일 일정과 동일하게 고락섭까지 이동합니다.','30','tip','칼라파타르를 위해 고락섭 1박을 유지하세요.'),('10일','칼라파타르 5,545m 일출','왕복 약 4km','4~5시간','새벽 4~5시에 칼라파타르 정상으로 오라 에베레스트·눕체·로체의 일출 파노라마를 감상합니다.','88','warn','-20°C 이하가 흔합니다. 최상급 방한 장비를 착용하세요.'),('11~13일','촐라체 → 고키요','약 25km','3일','촐라체(5,420m) 고개를 넘어 고기오·타그낙을 거쳐 고키요 호수 군에 도달합니다. 제3호수가 최고 전망입니다.','95','warn','촐라체는 암설+빙판 구간입니다. 가이드 판단에 따라 일정 조정이 필요합니다.'),('14~16일','고키요 → 루클라 하산','약 40km','3일','렌조라(5,360m)를 넘어 남체로 복귀한 뒤 루클라로 하산합니다.','30','tip','렌조라는 촐라체와 비슷한 고도입니다. 연속 고개 통과에 유의하세요.')],
    tips=[('backpack','준비물',['수면배깅(-20°C 등급)','등반 장갑·바라클라바','산소 측정기(권장)','여분 배터리(한랭 소모)']),('book','허가·예약',['허가는 표준과 동일','기간 연장으로 비용 증가','고키요 구간 티하우스 사전 확인']),('shield','주의',['5,500m급 고도 연속','촐라체 암설·빙판','비상 하산 판단'])],
    cps=[('고락섭','거점','badge-shelter','5,160m','9일차','티하우스'),('칼라파타르','정상','badge-summit','5,545m','10일차 새벽','에베레스트 일출'),('촐라체 고개','고개','badge-summit','5,420m','11일차','암설·빙판'),('고키요 제3호수','명소','badge-landmark','~4,950m','12~13일','전망대'),('남체 복귀','하산','badge-shelter','3,440m','14~15일','티하우스')],
    map_note='칼라파타르+고키요 완성형', map_start='루클라', map_end='고키요 호수',
    map_path='M85 350 C200 336, 310 305, 420 258 S620 90, 700 52', map_nodes=[(85,350,10),(430,260,8),(700,52,12)]),
 ],
 'en': [
  dict(id='beginner', color='green', hex='#6a7d4c', level='Beginner', meter=3,
    name='Lukla–Namche Acclimatization Section', sub='Lukla 2,840 m → Namche Bazaar 3,440 m · ~20 km · 4–5 days',
    tabs=['Overview','Route','Map','Tips'],
    pills=pill('ruler','Distance','~20 km')+pill('clock','Duration','4–5 days')+pill('location','Namche','3,440 m')+pill_meter('Difficulty',3,'medium')+pill('star','Season','Mar–May · Oct–Nov')+pill('location','Permits','2 types'),
    h_flow='Course Flow', h_elev='Elevation Profile', h_route='Route by Section', h_map='Concept Map', h_cp='Checkpoints',
    flow=['Lukla 2,840 m','Phakding 2,610 m','Namche Bazaar 3,440 m','Acclimatization hike'],
    elev_label='Namche Bazaar 3,440 m', elev_path='M20 165 C170 155, 320 125, 470 95 S640 70, 740 55', elev_peak=(740,55),
    desc='The entry section of the EBC trek: from Lukla follow the Dudh Koshi valley to the legendary teahouse town of Namche Bazaar (3,440 m), building the base for safe acclimatization.',
    segs=[('Start','Arrive Lukla','0 km','—','Begin after the ~35-minute Kathmandu–Lukla flight, which is weather-dependent.','15','tip','Build slack into your schedule for Lukla flight delays.'),('1','Lukla → Phakding','~8 km','3–4 h','Descend along the Dudh Koshi and overnight at Phakding.','45','tip','Start light — the first day is about settling in.'),('2','Phakding → Namche Bazaar','~8 km','5–6 h','Pass the national park gate at Monjo and climb to Namche — the first altitude checkpoint.','85','warn','Past 3,000 m, slow down if headache or nausea appears.'),('Return','Namche acclimatization day','—','1 day','An acclimatization hike toward Everest View Hotel — "climb high, sleep low."','—','tip','The rest day is a requirement, not an option.')],
    tips=[('backpack','Gear',['Sleeping bag (-10°C rating)','Headlamp & spare batteries','Altitude meds (consult a doctor)','Cash — no cards on the trail']),('book','Permits & costs',['Sagarmatha NP NPR 3,000','Khumbu municipality permit NPR 3,000','Guide mandatory via agency · packages $1,200–2,000']),('shield','Cautions',['Altitude sickness — descent is the cure','Lukla flight delays','Night cold below -10°C'])],
    cps=[('Lukla','Starting Point','badge-trailhead','2,840 m','0 km','Airport · teahouses'),('Monjo gate','Permit check','badge-trailhead','2,835 m','~10 km','Park gate'),('Namche Bazaar','Acclimatization base','badge-shelter','3,440 m','~20 km','Teahouses · clinic'),('Everest View hike','Acclimatization','badge-landmark','3,880 m','Day hike','Viewpoint')],
    map_note='EBC entry acclimatization section', map_start='Lukla 2,840 m', map_end='Namche 3,440 m',
    map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55', map_nodes=[(110,335,10),(460,210,8),(695,55,12)]),
  dict(id='intermediate', color='blue', hex='#456e96', level='Intermediate', meter=4,
    name='Standard 12-Day EBC Trek', sub='Lukla → Namche/Dingboche acclimatization → EBC 5,364 m · ~130 km · 12 days',
    tabs=['Overview','Route','Map','Tips'],
    pills=pill('ruler','Distance','~130 km')+pill('clock','Duration','12 days')+pill('location','EBC','5,364 m')+pill_meter('Difficulty',4,'hard')+pill('star','Rest days','2 (Namche/Dingboche)')+pill('location','Guide','Mandatory'),
    h_flow='Course Flow', h_elev='Elevation Profile', h_route='Route by Section', h_map='Concept Map', h_cp='Checkpoints',
    flow=['Lukla','Namche 3,440 m','Dingboche 4,410 m','Lobuche 4,940 m','Gorak Shep 5,160 m','EBC 5,364 m','Descend'],
    elev_label='EBC 5,364 m', elev_path='M20 195 C170 188, 320 162, 470 126 S640 68, 740 40', elev_peak=(740,40),
    desc='The world-famous round trip to Everest Base Camp on a standard 12-day schedule. Two acclimatization days — Namche (3,440 m) and Dingboche (4,410 m) — are the keys to safety, with teahouse lodging and a guide as the norm.',
    segs=[('Days 1–3','Lukla → Namche Bazaar','~20 km','3 days','Follow the Dudh Koshi to Namche and complete the first acclimatization hike.','30','tip','Do rest-day hikes on the climb-high-sleep-low principle.'),('Days 4–6','Namche → Dingboche','~20 km','3 days','Pass Tengboche monastery and Ama Dablam views to Dingboche (4,410 m) for the second acclimatization.','55','warn','Beyond Dingboche adjust the schedule to symptoms — not pushing on is the best policy.'),('Days 7–8','Dingboche → Lobuche → Gorak Shep','~15 km','2 days','Past memorial ridges to Lobuche (4,940 m), then overnight at Gorak Shep (5,160 m).','80','warn','Sleep disturbances above 4,900 m are common — prepare medication and know the drills.'),('Day 9','EBC 5,364 m','~4 km RT','6–8 h','Day-hike from Gorak Shep to Base Camp and back. The EBC marker rock is the classic photo spot.','95','warn','Alpine weather flips fast — avoid being out after midday.'),('Days 10–12','Descent → Lukla','~60 km','3 days','Fast descent via Pheriche and Namche, then fly out from Lukla.','30','tip','Two days can be shaved off the descent — judge by your feet and knees.')],
    tips=[('backpack','Gear',['Sleeping bag (-15°C rating)','Boots & gaiters','Full insulated set','Purification tablets & snacks']),('book','Permits & booking',['Park + municipality ~NPR 6,000','Agency packages $1,200–2,000','Lukla flights ~$400 RT separate']),('shield','Cautions',['Altitude sickness — descend immediately','Adjust for weather','Insurance incl. helicopter evacuation is essential'])],
    cps=[('Lukla','Starting Point','badge-trailhead','2,840 m','0 km','Airport · teahouses'),('Namche Bazaar','Acclimatization','badge-shelter','3,440 m','Day 3','Teahouses · clinic'),('Dingboche','Acclimatization','badge-shelter','4,410 m','Day 6','Teahouses'),('Gorak Shep','Lodging','badge-shelter','5,160 m','Day 8','Teahouses'),('EBC 5,364 m','Destination','badge-summit','5,364 m','Day 9','Monument')],
    map_note='Standard 12-day EBC route', map_start='Lukla 2,840 m', map_end='EBC 5,364 m',
    map_path='M95 345 C210 332, 320 300, 430 255 S630 90, 705 50', map_nodes=[(95,345,10),(430,255,8),(705,50,12)]),
  dict(id='advanced', color='red', hex='#9f5845', level='Advanced', meter=5,
    name='Kala Patthar + Gokyo Extension (14–16 days)', sub='EBC + Kala Patthar 5,545 m + Gokyo Lakes · ~160 km+',
    tabs=['Overview','Route','Map','Tips'],
    pills=pill('ruler','Distance','~160 km+')+pill('clock','Duration','14–16 days')+pill('location','Kala Patthar','5,545 m')+pill_meter('Difficulty',5,'hard')+pill('star','Extension','Gokyo Lakes')+pill('location','Max altitude','5,545 m'),
    h_flow='Course Flow', h_elev='Elevation Profile', h_route='Route by Section', h_map='Concept Map', h_cp='Checkpoints',
    flow=['EBC standard','Kala Patthar 5,545 m','Cho La pass','Gokyo Lakes','Descend'],
    elev_label='Kala Patthar 5,545 m', elev_path='M20 195 C170 190, 320 168, 470 132 S640 66, 740 40', elev_peak=(740,40),
    desc='The complete route: the standard EBC itinerary plus a dawn climb of Kala Patthar (5,545 m) and the Gokyo Lakes extension (4,700–5,000 m) — two of the finest panoramas on Earth.',
    segs=[('Days 1–9','EBC standard section','~65 km','9 days','Same as the standard itinerary up to Gorak Shep.','30','tip','Keep the Gorak Shep night intact for Kala Patthar.'),('Day 10','Kala Patthar 5,545 m sunrise','~4 km RT','4–5 h','Climb before dawn for the sunrise panorama of Everest, Nuptse, and Lhotse.','88','warn','-20°C is common — wear your best expedition layers.'),('Days 11–13','Cho La → Gokyo','~25 km','3 days','Cross Cho La pass (5,420 m) to Gokyo village and its lakes — the third lake has the best viewpoint.','95','warn','Cho La is scree and ice — adjust the schedule on the guide\'s judgment.'),('Days 14–16','Gokyo → Lukla','~40 km','3 days','Cross Renjo La (5,360 m) back to Namche and descend to Lukla.','30','tip','Renjo La matches Cho La\'s altitude — mind consecutive pass days.')],
    tips=[('backpack','Gear',['Sleeping bag (-20°C rating)','Climbing gloves & balaclava','Pulse oximeter (recommended)','Spare batteries (cold drain)']),('book','Permits & booking',['Same permits as standard','Longer duration increases cost','Check Gokyo teahouse status']),('shield','Cautions',['Consecutive 5,500 m days','Cho La scree & ice','Be ready to bail out'])],
    cps=[('Gorak Shep','Base','badge-shelter','5,160 m','Day 9','Teahouses'),('Kala Patthar','Summit','badge-summit','5,545 m','Day 10 dawn','Everest sunrise'),('Cho La pass','Pass','badge-summit','5,420 m','Day 11','Scree · ice'),('Gokyo third lake','Attraction','badge-landmark','~4,950 m','Days 12–13','Viewpoint'),('Back at Namche','Descent','badge-shelter','3,440 m','Days 14–15','Teahouses')],
    map_note='Kala Patthar + Gokyo complete route', map_start='Lukla', map_end='Gokyo Lakes',
    map_path='M85 350 C200 336, 310 305, 420 258 S620 90, 700 52', map_nodes=[(85,350,10),(430,260,8),(700,52,12)]),
 ],
}

# ── ACT ──
T_ACT_KO = dict(
  title='안나푸르나 서킷 트레킹 플레이북',
  meta='네팔 안나푸르나 서킷(ACT) 트레킹 가이드. 토롱라 고개 5,416m 통과 14일 표준 일정의 상세 경로, ACAP 허가, 실사 지도 및 팁을 제공합니다.',
  h1_card='안나푸르나 서킷', p_card='ACT · 토롱라 5,416m · 14일 표준 서킷',
  hero_alt='안나푸르나 계곡의 마을과 눈 덮인 산맥',
  badge='ACT 트레킹 플레이북', h1='안나푸르나 서킷 트레킹 플레이북',
  hero_desc='세계적 장거리 트레킹 안나푸르나 서킷 가이드. 토롱라 고개(5,416m) 통과와 마낭 적응, 허가·비용·팁을 정리했습니다.',
  btn1='초급: 마낭 구간 트레킹', btn2='중급: 서킷 표준 14일', btn3='고급: 틸리코호 연장',
  hero_photographer='Martin Skřivánek', hero_url='https://unsplash.com/photos/-sz-PCtnmFI',
  gal_title='안나푸르나 서킷의 사계 &amp; 명소', lb_zoom='크게 보기',
  gallery=[('g1','설산 능선','Unsplash'),('g2','녹색 계곡','Unsplash'),('g3','계곡의 강','Unsplash'),('g4','산마을 티하우스','Unsplash')],
)
T_ACT_EN = dict(
  title='Annapurna Circuit Trek Playbook',
  meta='Guide to the Annapurna Circuit (ACT), Nepal — the standard 14-day itinerary crossing Thorong La (5,416 m), with ACAP permits, maps, and tips.',
  h1_card='Annapurna Circuit', p_card='ACT · Thorong La 5,416 m · 14-day standard circuit',
  hero_alt='A village in the Annapurna valley beneath snow-capped ranges',
  badge='ACT Trek Playbook', h1='Annapurna Circuit Trek Playbook',
  hero_desc='A guide to the world-class Annapurna Circuit — crossing Thorong La (5,416 m), acclimatizing at Manang, and everything on permits, costs, and safety.',
  btn1='Beginner: Manang Section', btn2='Intermediate: Standard 14-Day Circuit', btn3='Advanced: Tilicho Lake Extension',
  hero_photographer='Martin Skřivánek', hero_url='https://unsplash.com/photos/-sz-PCtnmFI',
  gal_title='Annapurna Circuit Four Seasons &amp; Attractions', lb_zoom='View larger',
  gallery=[('g1','Snowy ridgelines','Unsplash'),('g2','Green valley','Unsplash'),('g3','River in the valley','Unsplash'),('g4','Mountain teahouse','Unsplash')],
)
C_ACT = {
 'ko': [
  dict(id='beginner', color='green', hex='#6a7d4c', level='초급', meter=3,
    name='마낭 구간 트레킹', sub='서킷 상행 마낭(3,540m)까지 · 약 60km · 7~8일',
    tabs=['개요','경로 안내','지도','팁 &amp; 주의'],
    pills=pill('ruler','거리','약 60km')+pill('clock','일정','7~8일')+pill('location','마낭','3,540m')+pill_meter('난이도',3,'medium')+pill('star','시즌','3~5월·10~11월')+pill('location','허가','ACAP'),
    h_flow='코스 흐름', h_elev='고도 프로파일', h_route='구간별 경로 안내', h_map='코스 개념도', h_cp='체크포인트 표',
    flow=['베시사하르','다라파니','마낭 3,540m','적응 하이킹'],
    elev_label='마낭 3,540m', elev_path='M20 168 C170 158, 320 128, 470 98 S640 70, 740 55', elev_peak=(740,55),
    desc='서킷 상행 구간인 베시사하르부터 마낭(3,540m)까지의 적응 트레킹입니다. 카트만두~포카라 없이 서킷의 정수인 마낭 계곡만 경험하고 싶은 분에게 적합합니다.',
    segs=[('출','베시사하르 출발','0km','—','카트만두·포카라에서 차량으로 베시사하르까지 이동한 뒤 출발합니다.','15','tip','도로 개통으로 앞 구간은 차량 대체가 가능해졌습니다.'),('1','베시사하르 → 다라파니','약 15km','1~2일','마샹디 강을 따라 오르며 카르텀·체메 등 마을을 지납니다.','45','tip','계곡 뷰와 밀밭이 아름다운 구간입니다.'),('2','다라파니 → 마낭','약 12km','1.5~2일','고도가 올라가며 사막성 지형으로 바뀝니다. 마낭에서 1일 적응합니다.','85','warn','마낭 도착일은 고산 증상 체크가 중요합니다. 늦게 도착하면 다음 날 적응하세요.'),('하','마낭 적응 하이킹','—','1일','프라켄 갬파 방면 적응 하이킹을 소화합니다.','—','tip','마낭에서 티하우스가 가장 잘 갖춰져 있습니다.')],
    tips=[('backpack','준비물',['수면배깅','방한 겉옷','정화 태블릿','현금']),('book','허가',['ACAP 약 3,000루피','TIMS(대행사 발급)','가이드 의무(NTB 규정)']),('shield','주의',['마낭 이후 고도 급상승','우기 산사태 구간','일교차 극단'])],
    cps=[('베시사하르','출발점','badge-trailhead','해발 약 760m','0km','버스 터미널'),('다라파니','마을','badge-shelter','해발 약 1,960m','1~2일차','티하우스'),('마낭','적응 거점','badge-shelter','3,540m','약 7일차','티하우스·병원'),('프라켄 하이킹','적응','badge-landmark','해발 약 4,000m','당일 왕복','갬파')],
    map_note='서킷 상행 마낭 구간', map_start='베시사하르', map_end='마낭 3,540m',
    map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55', map_nodes=[(110,335,10),(460,210,8),(695,55,12)]),
  dict(id='intermediate', color='blue', hex='#456e96', level='중급', meter=4,
    name='서킷 표준 14일', sub='베시사하르 → 마낭 → 토롱라 5,416m → 무크티나트 → 포카라 · 약 160km',
    tabs=['개요','경로 안내','지도','팁 &amp; 주의'],
    pills=pill('ruler','거리','약 160km')+pill('clock','일정','14일')+pill('location','토롱라','5,416m')+pill_meter('난이도',4,'hard')+pill('star','적응','마낭 2일')+pill('location','허가','ACAP'),
    h_flow='코스 흐름', h_elev='고도 프로파일', h_route='구간별 경로 안내', h_map='코스 개념도', h_cp='체크포인트 표',
    flow=['베시사하르','마낭 3,540m','토롱라 5,416m','무크티나트','포카라'],
    elev_label='토롱라 5,416m', elev_path='M20 192 C170 186, 320 162, 470 126 S640 62, 740 40', elev_peak=(740,40),
    desc='아나푸르나 산맥을 반 바퀴 도는 세계적 장거리 서킷입니다. 마낭에서 2일 적응 후 토롱라 고개(5,416m)를 넘고, 무크티나트를 거쳐 포카라로 돌아옵니다. 히말라야의 생태·문화·종교를 한 번에 경험합니다.',
    segs=[('1~5일','베시사하르 → 마낭','약 60km','5일','마샹디 계곡을 따라 숲·밀밭·사막 지형으로 변화하며 마낭까지 오릅니다.','30','tip','도로 개통 구간은 차량 대체가 가능해 일정 단축이 가능합니다.'),('6~7일','마낭 적응','—','2일','프라켄 갬파·아이스레이크 하이킹으로 고도 적응을 완료합니다.','55','tip','적응일 하이킹은 토롱라 통과율을 크게 높입니다.'),('8~9일','마낭 → 토롱라 파이어리 캠프','약 12km','2일','야카카르카를 거쳐 하이캠프(토롱라 파이어리 캠프, 4,925m)에서 1박합니다.','80','warn','고지대 숙박이라 심한 두통이면 토롱라 통과를 미루세요.'),('10일','토롱라 5,416m 통과','약 16km','7~9시간','새벽 출발로 토롱라 고개(5,416m)를 통과해 무크티나트로 긴 하산을 합니다. 서킷의 정점입니다.','95','warn','고개는 정오 전 통과가 원칙입니다. 오후 풍설이 위험합니다.'),('11~14일','무크티나트 → 포카라','약 60km','4일','무크티나트 사원을 참배하고 타토파니 온천을 거쳐 포카라로 복귀합니다.','30','tip','지루한 도로 구간은 지프·버스로 대체할 수 있습니다.')],
    tips=[('backpack','준비물',['수면배깅','방한 세트','마스크(황사·먼지)','보조 배터리']),('book','허가·예약',['ACAP 약 3,000루피','패키지 $800~2,500','가이드 ~$21/일(NTB 규정)']),('shield','주의',['토롱라 정오 통과 원칙','고산 질환','하산 계단 무릎 부담'])],
    cps=[('베시사하르','출발점','badge-trailhead','해발 약 760m','0km','터미널'),('마낭','적응 거점','badge-shelter','3,540m','5일차','티하우스·병원'),('토롱라 파이어리 캠프','1박','badge-shelter','4,925m','9일차','산장'),('토롱라 5,416m','정점','badge-summit','5,416m','10일차','차망·게시물'),('무크티나트','사원','badge-temple','해발 약 3,760m','10일차 하산','사원·온천')],
    map_note='서킷 표준 14일 루트', map_start='베시사하르', map_end='포카라',
    map_path='M90 348 C200 336, 310 305, 420 258 S630 95, 700 52', map_nodes=[(90,348,10),(420,258,8),(700,52,12)]),
  dict(id='advanced', color='red', hex='#9f5845', level='고급', meter=5,
    name='틸리코호 연장 16~18일', sub='마낭 → 틸리코 베이스캠프 4,150m → 서킷 복귀 · 약 190km+',
    tabs=['개요','경로 안내','지도','팁 &amp; 주의'],
    pills=pill('ruler','거리','약 190km+')+pill('clock','일정','16~18일')+pill('location','틸리코호','4,919m')+pill_meter('난이도',5,'hard')+pill('star','연장','틸리코 베이스캠프')+pill('location','고도','최대 5,000m+'),
    h_flow='코스 흐름', h_elev='고도 프로파일', h_route='구간별 경로 안내', h_map='코스 개념도', h_cp='체크포인트 표',
    flow=['마낭','틸리코 베이스캠프','틸리코호 4,919m','토롱라','포카라'],
    elev_label='틸리코호 4,919m', elev_path='M20 193 C170 188, 320 166, 470 130 S640 64, 740 42', elev_peak=(740,42),
    desc='서킷의 최고 명소 틸리코호(4,919m)를 마낭에서 연장하는 코스입니다. 고도 5,000m 부근 야영이 포함되어 고산 적응이 완벽한 등반가에게만 적합합니다.',
    segs=[('1~5일','베시사하르 → 마낭','약 60km','5일','표준 상행 구간으로 마낭까지 오릅니다. 적응일을 충분히 확보하세요.','25','tip','틸리코 연장자는 마낭 적응 하이킹을 더 강도 높게 소화하세요.'),('6~7일','마낭 → 틸리코 베이스캠프','약 12km','2일','훙강마을을 거쳐 틸리코 베이스캠프(4,150m)로 오릅니다. 고산 야영입니다.','55','warn','야영지에서 고산 증상이 심하면 다음 날 호수 등반을 포기하세요.'),('8일','틸리코호 4,919m','왕복 약 3km','4~5시간','틸리코 고개(5,315m) 방면 전망 또는 호수 기슭까지 탐방합니다. 터콩(카일라스)의 성호가 보입니다.','90','warn','호수 고도 4,919m — 활동을 최소화하고 수분을 유지하세요.'),('9일차~','서킷 복귀 후 표준 하산','약 80km','6~8일','토롱라를 넘어 무크티나트·타토파니를 거쳐 포카라로 복귀합니다.','30','tip','체력 소모가 커서 도로 구간 차량 대체가 합리적입니다.')],
    tips=[('backpack','준비물',['동계용 수면배깅','야영 장비(산장 옵션 확인)','산소 측정기','고열량 식품']),('book','허가·예약',['ACAP 동일','틸리코 구간 티하우스 한정','가이드 필수']),('shield','주의',['4,900m+ 야영','기상 악화 시 즉시 하강','응급 이송 계획 수립'])],
    cps=[('마낭','분기','badge-shelter','3,540m','5일차','티하우스'),('훙강','마을','badge-shelter','해발 약 3,580m','6일차','티하우스'),('틸리코 베이스캠프','야영','badge-shelter','4,150m','7일차','산장'),('틸리코호 4,919m','명소','badge-landmark','4,919m','8일차','전망'),('무크티나트','사원','badge-temple','해발 약 3,760m','하산','사원')],
    map_note='틸리코호 연장 완성형', map_start='베시사하르', map_end='틸리코호',
    map_path='M85 350 C200 336, 310 305, 420 258 S620 90, 700 52', map_nodes=[(85,350,10),(420,258,8),(700,52,12)]),
 ],
 'en': [
  dict(id='beginner', color='green', hex='#6a7d4c', level='Beginner', meter=3,
    name='Manang Section Trek', sub='Circuit approach to Manang 3,540 m · ~60 km · 7–8 days',
    tabs=['Overview','Route','Map','Tips'],
    pills=pill('ruler','Distance','~60 km')+pill('clock','Duration','7–8 days')+pill('location','Manang','3,540 m')+pill_meter('Difficulty',3,'medium')+pill('star','Season','Mar–May · Oct–Nov')+pill('location','Permit','ACAP'),
    h_flow='Course Flow', h_elev='Elevation Profile', h_route='Route by Section', h_map='Concept Map', h_cp='Checkpoints',
    flow=['Besisahar','Dharapani','Manang 3,540 m','Acclimatization hike'],
    elev_label='Manang 3,540 m', elev_path='M20 168 C170 158, 320 128, 470 98 S640 70, 740 55', elev_peak=(740,55),
    desc='The circuit\'s approach trek from Besisahar to Manang (3,540 m) — for those who want the highlight Manang valley without the full circuit.',
    segs=[('Start','Depart Besisahar','0 km','—','Transfer by road to Besisahar from Kathmandu or Pokhara and set off.','15','tip','Recent road building lets vehicles replace the first sections.'),('1','Besisahar → Dharapani','~15 km','1–2 days','Follow the Marsyangdi river past Karche and Chame.','45','tip','Beautiful valley and millet-field scenery.'),('2','Dharapani → Manang','~12 km','1.5–2 days','The terrain turns alpine-desert as you climb. Spend an acclimatization day in Manang.','85','warn','Check for altitude symptoms on arrival — if late, extend the rest day.'),('Return','Manang acclimatization hike','—','1 day','Do an acclimatization hike toward Praken Gompa.','—','tip','Manang has the best-developed teahouse infrastructure on the circuit.')],
    tips=[('backpack','Gear',['Sleeping bag','Insulated layer','Purification tablets','Cash']),('book','Permits',['ACAP ~NPR 3,000','TIMS (via agency)','Guide mandatory under NTB rules']),('shield','Cautions',['Rapid altitude gain past Manang','Monsoon landslide sections','Extreme diurnal range'])],
    cps=[('Besisahar','Starting Point','badge-trailhead','~760 m','0 km','Bus terminal'),('Dharapani','Village','badge-shelter','~1,960 m','Days 1–2','Teahouses'),('Manang','Acclimatization base','badge-shelter','3,540 m','~Day 7','Teahouses · clinic'),('Praken hike','Acclimatization','badge-landmark','~4,000 m','Day hike','Gompa')],
    map_note='Circuit upper-Manang section', map_start='Besisahar', map_end='Manang 3,540 m',
    map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55', map_nodes=[(110,335,10),(460,210,8),(695,55,12)]),
  dict(id='intermediate', color='blue', hex='#456e96', level='Intermediate', meter=4,
    name='Standard 14-Day Circuit', sub='Besisahar → Manang → Thorong La 5,416 m → Muktinath → Pokhara · ~160 km',
    tabs=['Overview','Route','Map','Tips'],
    pills=pill('ruler','Distance','~160 km')+pill('clock','Duration','14 days')+pill('location','Thorong La','5,416 m')+pill_meter('Difficulty',4,'hard')+pill('star','Acclimatization','2 days in Manang')+pill('location','Permit','ACAP'),
    h_flow='Course Flow', h_elev='Elevation Profile', h_route='Route by Section', h_map='Concept Map', h_cp='Checkpoints',
    flow=['Besisahar','Manang 3,540 m','Thorong La 5,416 m','Muktinath','Pokhara'],
    elev_label='Thorong La 5,416 m', elev_path='M20 192 C170 186, 320 162, 470 126 S640 62, 740 40', elev_peak=(740,40),
    desc='The world-class long circuit around the Annapurna massif. After two acclimatization days in Manang, cross Thorong La (5,416 m), visit Muktinath, and return to Pokhara — ecology, culture, and religion in one trek.',
    segs=[('Days 1–5','Besisahar → Manang','~60 km','5 days','Follow the Marsyangdi valley through forest, fields, and desert-alpine terrain.','30','tip','Road sections can be replaced by vehicles to shorten the schedule.'),('Days 6–7','Manang acclimatization','—','2 days','Complete acclimatization hikes to Praken Gompa or Ice Lake.','55','tip','Rest-day hikes dramatically raise your Thorong La success rate.'),('Days 8–9','Manang → Thorong Phedi','~12 km','2 days','Via Yak Kharka to High Camp (4,925 m) for the night.','80','warn','It is a high-altitude night — severe headache means postponing the pass.'),('Day 10','Cross Thorong La 5,416 m','~16 km','7–9 h','Pre-dawn start over the pass (5,416 m) and a long descent to Muktinath — the summit of the circuit.','95','warn','Cross before noon — afternoon wind and snow are dangerous.'),('Days 11–14','Muktinath → Pokhara','~60 km','4 days','Visit Muktinath temple, soak at Tatopani hot springs, and return to Pokhara.','30','tip','Dull road sections can be replaced by jeep or bus.')],
    tips=[('backpack','Gear',['Sleeping bag','Full insulated set','Dust mask','Power bank']),('book','Permits & costs',['ACAP ~NPR 3,000','Packages $800–2,500','Guide ~$21/day (NTB rules)']),('shield','Cautions',['Cross the pass before noon','Altitude sickness','Knee strain on descents'])],
    cps=[('Besisahar','Starting Point','badge-trailhead','~760 m','0 km','Terminal'),('Manang','Acclimatization base','badge-shelter','3,540 m','Day 5','Teahouses · clinic'),('Thorong Phedi','Overnight','badge-shelter','4,925 m','Day 9','Lodge'),('Thorong La 5,416 m','High point','badge-summit','5,416 m','Day 10','Cairn · prayer flags'),('Muktinath','Temple','badge-temple','~3,760 m','Day 10 descent','Temple · hot springs')],
    map_note='Standard 14-day circuit route', map_start='Besisahar', map_end='Pokhara',
    map_path='M90 348 C200 336, 310 305, 420 258 S630 95, 700 52', map_nodes=[(90,348,10),(420,258,8),(700,52,12)]),
  dict(id='advanced', color='red', hex='#9f5845', level='Advanced', meter=5,
    name='Tilicho Lake Extension (16–18 days)', sub='Manang → Tilicho Base Camp 4,150 m → circuit resume · ~190 km+',
    tabs=['Overview','Route','Map','Tips'],
    pills=pill('ruler','Distance','~190 km+')+pill('clock','Duration','16–18 days')+pill('location','Tilicho Lake','4,919 m')+pill_meter('Difficulty',5,'hard')+pill('star','Extension','Tilicho Base Camp')+pill('location','Max altitude','5,000 m+'),
    h_flow='Course Flow', h_elev='Elevation Profile', h_route='Route by Section', h_map='Concept Map', h_cp='Checkpoints',
    flow=['Manang','Tilicho Base Camp','Tilicho Lake 4,919 m','Thorong La','Pokhara'],
    elev_label='Tilicho Lake 4,919 m', elev_path='M20 193 C170 188, 320 166, 470 130 S640 64, 740 42', elev_peak=(740,42),
    desc='The circuit\'s crown-jewel extension to Tilicho Lake (4,919 m) from Manang — with camping near 5,000 m, this suits only fully acclimatized trekkers.',
    segs=[('Days 1–5','Besisahar → Manang','~60 km','5 days','Climb the standard approach to Manang with ample acclimatization.','25','tip','Tilicho trekkers should push the Manang acclimatization hikes harder.'),('Days 6–7','Manang → Tilicho Base Camp','~12 km','2 days','Via Khangsar to Tilicho Base Camp (4,150 m) — a high camp.','55','warn','If altitude symptoms worsen at the camp, skip the lake climb the next day.'),('Day 8','Tilicho Lake 4,919 m','~3 km RT','4–5 h','Explore the lake shore or the viewpoint toward Tilicho Pass (5,315 m) with views of the Great Barrier.','90','warn','The lake sits at 4,919 m — minimize exertion and stay hydrated.'),('Day 9+','Resume circuit and descend','~80 km','6–8 days','Cross Thorong La, visit Muktinath and Tatopani, and return to Pokhara.','30','tip','After this extension, vehicle replacement of road sections is a reasonable choice.')],
    tips=[('backpack','Gear',['Winter sleeping bag','Camping gear (check lodge options)','Pulse oximeter','High-calorie food']),('book','Permits & booking',['Same ACAP permit','Limited teahouses on the Tilicho section','Guide mandatory']),('shield','Cautions',['Camping near 4,900 m','Descend immediately in bad weather','Have an evacuation plan'])],
    cps=[('Manang','Fork','badge-shelter','3,540 m','Day 5','Teahouses'),('Khangsar','Village','badge-shelter','~3,580 m','Day 6','Teahouses'),('Tilicho Base Camp','Camp','badge-shelter','4,150 m','Day 7','Lodge'),('Tilicho Lake 4,919 m','Attraction','badge-landmark','4,919 m','Day 8','Viewpoint'),('Muktinath','Temple','badge-temple','~3,760 m','Descent','Temple')],
    map_note='Tilicho Lake complete extension', map_start='Besisahar', map_end='Tilicho Lake',
    map_path='M85 350 C200 336, 310 305, 420 258 S620 90, 700 52', map_nodes=[(85,350,10),(420,258,8),(700,52,12)]),
 ],
}

# ── 랑탕 ──
T_LANGTANG_KO = dict(
  title='랑탕 밸리 트레킹 플레이북',
  meta='네팔 랑탕 밸리 트레킹 가이드. 캰진곰파 3,870m·체르코리 4,984m까지 7~10일 일정의 상세 경로, 허가, 실사 지도 및 팁을 제공합니다.',
  h1_card='랑탕 밸리', p_card='Langtang · 캰진곰파 3,870m · 카트만두 근교 트레킹',
  hero_alt='설원 호수에 걸린 기도 깃발과 눈 덮인 산맥',
  badge='랑탕 플레이북', h1='랑탕 밸리 트레킹 플레이북',
  hero_desc='카트만두에서 가장 가까운 히말라야 계곡 트레킹, 랑탕. 캰진곰파(3,870m)와 체르코리(4,984m)까지의 상세 경로와 팁을 제공합니다.',
  btn1='초급: 랑탕 밸리 왕복', btn2='중급: 캰진리 일출 코스', btn3='고급: 체르코리 도전',
  hero_photographer='Sergey Pesterev', hero_url='https://unsplash.com/photos/dstd4DoLQ90',
  gal_title='랑탕의 사계 &amp; 명소', lb_zoom='크게 보기',
  gallery=[('g1','설산 하이킹','Unsplash'),('g2','백팩 트레일','Unsplash'),('g3','설산 능선','Unsplash'),('g4','산기슭 마을','Unsplash')],
)
T_LANGTANG_EN = dict(
  title='Langtang Valley Trek Playbook',
  meta='Guide to the Langtang Valley trek, Nepal — 7–10 day itineraries to Kyanjin Gompa (3,870 m) and Tserko Ri (4,984 m), with permits, maps, and tips.',
  h1_card='Langtang Valley', p_card='Langtang · Kyanjin Gompa 3,870 m · Closest Himalayan valley to Kathmandu',
  hero_alt='Prayer flags over a frozen lake beneath snow-capped ranges',
  badge='Langtang Playbook', h1='Langtang Valley Trek Playbook',
  hero_desc='The closest Himalayan valley trek to Kathmandu — routes to Kyanjin Gompa (3,870 m) and the Tserko Ri viewpoint (4,984 m) with permits and tips.',
  btn1='Beginner: Valley Round Trip', btn2='Intermediate: Kyanjin Ri Sunrise', btn3='Advanced: Tserko Ri Challenge',
  hero_photographer='Sergey Pesterev', hero_url='https://unsplash.com/photos/dstd4DoLQ90',
  gal_title='Langtang Four Seasons &amp; Attractions', lb_zoom='View larger',
  gallery=[('g1','Snow hiking','Unsplash'),('g2','Backpack trail','Unsplash'),('g3','Snowy ridgelines','Unsplash'),('g4','Village at the mountain foot','Unsplash')],
)
C_LANGTANG = {
 'ko': [
  dict(id='beginner', color='green', hex='#6a7d4c', level='초급', meter=2,
    name='랑탕 밸리 왕복 트레킹', sub='시아브루베시 → 캰진곰파 3,870m 왕복 · 약 24km · 6~7일',
    tabs=['개요','경로 안내','지도','팁 &amp; 주의'],
    pills=pill('ruler','왕복 거리','약 24km')+pill('clock','일정','6~7일')+pill('location','캰진곰파','3,870m')+pill_meter('난이도',2,'medium')+pill('star','숙박','티하우스')+pill('location','허가','랑탕 NP'),
    h_flow='코스 흐름', h_elev='고도 프로파일', h_route='구간별 경로 안내', h_map='코스 개념도', h_cp='체크포인트 표',
    flow=['시아브루베시','람첼 2,350m','랑탕 마을 3,430m','캰진곰파 3,870m'],
    elev_label='캰진곰파 3,870m', elev_path='M20 172 C170 162, 320 132, 470 100 S640 68, 740 50', elev_peak=(740,50),
    desc='카트만두에서 차량으로 하루 이동으로 도달하는 가장 가까운 히말라야 계곡 트레킹입니다. 랑탕 국립공원의 숲과 계곡을 따라 캰진곰파(3,870m)까지 왕복합니다.',
    segs=[('출','카트만두 → 시아브루베시','약 122km','차량 6~8시간','산악 도로를 따라 시아브루베시까지 이동한 뒤 트레킹을 시작합니다.','10','tip','우기엔 도로 상태가 나빠집니다. 오전 출발을 권장합니다.'),('1','시아브루베시 → 람첼','약 11km','5~6시간','랑탕 강을 따라 숲속 계단길을 오릅니다. 람첼에서 1박합니다.','45','tip','2015년 지진 이후 재건된 마을들의 회복 이야기를 들어보세요.'),('2','람첼 → 랑탕 마을 → 캰진곰파','약 13km','6~7시간','랑탕 마을(3,430m)을 거쳐 캰진곰파(3,870m)에 도착합니다. 치즈 공장이 유명합니다.','90','tip','캰진곰파에서 야크 치즈를 맛보세요.'),('하','원점 하산','약 24km','2일','같은 길로 시아브루베시까지 하산합니다.','30','tip','하산은 1일에 다 내려올 수 있으나 2일로 나누는 것이 안전합니다.')],
    tips=[('backpack','준비물',['수면배깅','방한 겉옷','헤드랜턴','정화 태블릿']),('book','허가·비용',['랑탕 국립공원 입장 약 3,000루피','가이드 필수','예산 $400~950']),('shield','주의',['새벽 한랭','지진 재건 지역 안전','우기 산사태'])],
    cps=[('시아브루베시','출발점','badge-trailhead','해발 약 1,460m','0km','버스 터미널'),('람첼','마을','badge-shelter','해발 2,350m','1일차 약 11km','티하우스'),('랑탕 마을','마을','badge-shelter','해발 3,430m','2일차','티하우스'),('캰진곰파','도착','badge-landmark','해발 3,870m','2~3일차','치즈 공장·티하우스'),('시아브루베시 복귀','종점','badge-trailhead','해발 약 1,460m','왕복 약 24km','버스')],
    map_note='랑탕 밸리 왕복 트레킹', map_start='시아브루베시', map_end='캰진곰파 3,870m',
    map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55', map_nodes=[(110,335,10),(460,210,8),(695,55,12)]),
  dict(id='intermediate', color='blue', hex='#456e96', level='중급', meter=3,
    name='캰진리 일출 코스', sub='캰진곰파 + 캰진리 4,350m 일출 하이크 · 약 28km · 7~8일',
    tabs=['개요','경로 안내','지도','팁 &amp; 주의'],
    pills=pill('ruler','거리','약 28km')+pill('clock','일정','7~8일')+pill('location','캰진리','4,350m')+pill_meter('난이도',3,'medium')+pill('star','일출','아나푸르나·랑탕리룽')+pill('location','허가','랑탕 NP'),
    h_flow='코스 흐름', h_elev='고도 프로파일', h_route='구간별 경로 안내', h_map='코스 개념도', h_cp='체크포인트 표',
    flow=['시아브루베시','캰진곰파 3,870m','캰진리 4,350m','하산'],
    elev_label='캰진리 4,350m', elev_path='M20 175 C170 165, 320 138, 470 105 S640 66, 740 48', elev_peak=(740,48),
    desc='랑탕 밸리 왕복에 캰진리(4,350m) 일출 하이킹을 더한 코스입니다. 캰진리 정상에서 랑탕리룽(7,234m)과 아나푸르나·감가푸르나의 파노라마가 펼쳐집니다.',
    segs=[('1~3일','시아브루베시 → 캰진곰파','약 24km','3일','왕복 트레킹의 상행 구간을 소화하고 캰진곰파에서 1박합니다.','30','tip','고도 적응을 위해 캰진곰파 도착 후 가벼운 산책을 권장합니다.'),('4일','캰진리 4,350m 일출','왕복 약 5km','4~5시간','새벽 헤드랜턴을 켜고 캰진리 전망대로 오릅니다. 360도 히말라야 파노라마입니다.','92','warn','바람이 매우 강합니다. 방풍 모자·장갑을 착용하세요.'),('5~7일','하산','약 24km','2~3일','같은 길로 시아브루베시까지 하산한 뒤 카트만두로 복귀합니다.','30','tip','하산 중에도 산양 목장과 숲 풍경을 즐길 수 있습니다.')],
    tips=[('backpack','준비물',['헤드랜턴','방풍 모자·장갑','수면배깅','간식']),('book','허가·비용',['랑탕 국립공원 입장 약 3,000루피','가이드 필수','예산 $400~700']),('shield','주의',['캰진리 바람','고도 4,000m+ 적응','우기 도로 지연'])],
    cps=[('시아브루베시','출발점','badge-trailhead','해발 약 1,460m','0km','버스 터미널'),('캰진곰파','거점','badge-landmark','해발 3,870m','2~3일차','치즈 공장'),('캰진리 4,350m','정상','badge-summit','해발 4,350m','4일차 새벽','360도 전망대'),('시아브루베시 복귀','종점','badge-trailhead','해발 약 1,460m','왕복','버스')],
    map_note='캰진리 일출 코스', map_start='시아브루베시', map_end='캰진리 4,350m',
    map_path='M100 340 C220 326, 330 292, 440 245 S630 100, 700 55', map_nodes=[(100,340,10),(440,245,8),(700,55,12)]),
  dict(id='advanced', color='red', hex='#9f5845', level='고급', meter=4,
    name='체르코리(4,984m) 도전', sub='캰진곰파 → 체르코리 4,984m · 약 34km · 9~10일',
    tabs=['개요','경로 안내','지도','팁 &amp; 주의'],
    pills=pill('ruler','거리','약 34km')+pill('clock','일정','9~10일')+pill('location','체르코리','4,984m')+pill_meter('난이도',5,'hard')+pill('star','특징','5,000m급 전망대')+pill('location','허가','랑탕 NP'),
    h_flow='코스 흐름', h_elev='고도 프로파일', h_route='구간별 경로 안내', h_map='코스 개념도', h_cp='체크포인트 표',
    flow=['시아브루베시','캰진곰파 3,870m','체르코리 4,984m','하산'],
    elev_label='체르코리 4,984m', elev_path='M20 190 C170 184, 320 160, 470 122 S640 62, 740 40', elev_peak=(740,40),
    desc='랑탕 트레킹의 최종 관문 체르코리(4,984m)를 오르는 코스입니다. 무산소 상태로 5,000m에 근접하는 전망대로, 캰진곰파 2박 이상 적응 후 도전하는 것이 안전합니다.',
    segs=[('1~3일','시아브루베시 → 캰진곰파','약 24km','3일','표준 상행 구간을 완주하고 캰진곰파에 정착합니다.','30','tip','도착일 오후 캰진곰파 뒷산 가벼운 적응 산책을 권장합니다.'),('4일','캰진리 4,350m 적응','왕복 약 5km','4~5시간','체르코리 전에 캰진리로 고도 적응을 합니다. 이중 적응이 성공률을 높입니다.','55','warn','캰진리에서 증상이 심하면 체르코리를 포기하는 것이 안전합니다.'),('5일','체르코리 4,984m 도전','왕복 약 8km','7~9시간','모라인 사면을 따라 무산소 등반으로 정상에 오릅니다. 5,000m급 파노라마가 펼쳐집니다.','95','warn','고도 5,000m 근접 — 턴어라운드 시간을 정해두고 엄수하세요.'),('6~9일','하산','약 24km','2~3일','같은 길로 하산 후 카트만두로 복귀합니다.','30','tip','하산 후 포카라 연계 일정도 가능합니다.')],
    tips=[('backpack','준비물',['산소 측정기','턴어라운드 알람','방한 완전 세트','비상식량']),('book','허가·비용',['랑탕 국립공원 입장 약 3,000루피','가이드 필수','예산 $650~950']),('shield','주의',['무산소 5,000m 등반','기상 급변','체력 저하 시 즉시 하강'])],
    cps=[('시아브루베시','출발점','badge-trailhead','해발 약 1,460m','0km','버스 터미널'),('캰진곰파','적응 거점','badge-landmark','해발 3,870m','2~3일차','치즈 공장'),('캰진리','적응','badge-summit','해발 4,350m','4일차','360도 전망대'),('체르코리 4,984m','정상','badge-summit','해발 4,984m','5일차','5,000m급 파노라마'),('시아브루베시 복귀','종점','badge-trailhead','해발 약 1,460m','왕복 약 34km','버스')],
    map_note='랑탕 최종 관문 등반', map_start='시아브루베시', map_end='체르코리 4,984m',
    map_path='M90 350 C200 338, 310 308, 420 260 S630 95, 700 50', map_nodes=[(90,350,10),(420,260,8),(700,50,12)]),
 ],
 'en': [
  dict(id='beginner', color='green', hex='#6a7d4c', level='Beginner', meter=2,
    name='Langtang Valley Round Trip', sub='Syabrubesi → Kyanjin Gompa 3,870 m round trip · ~24 km · 6–7 days',
    tabs=['Overview','Route','Map','Tips'],
    pills=pill('ruler','Round trip','~24 km')+pill('clock','Duration','6–7 days')+pill('location','Kyanjin Gompa','3,870 m')+pill_meter('Difficulty',2,'medium')+pill('star','Lodging','Teahouses')+pill('location','Permit','Langtang NP'),
    h_flow='Course Flow', h_elev='Elevation Profile', h_route='Route by Section', h_map='Concept Map', h_cp='Checkpoints',
    flow=['Syabrubesi','Lama Hotel 2,350 m','Langtang village 3,430 m','Kyanjin Gompa 3,870 m'],
    elev_label='Kyanjin Gompa 3,870 m', elev_path='M20 172 C170 162, 320 132, 470 100 S640 68, 740 50', elev_peak=(740,50),
    desc='The closest Himalayan valley trek to Kathmandu — one day\'s drive, then follow the Langtang river through national park forest to Kyanjin Gompa (3,870 m) and back.',
    segs=[('Start','Kathmandu → Syabrubesi','~122 km','6–8 h drive','Transfer on mountain roads and start trekking.','10','tip','Road conditions worsen in the monsoon — morning departures are recommended.'),('1','Syabrubesi → Lama Hotel','~11 km','5–6 h','Climb forest stairs along the Langtang river; overnight at Lama Hotel.','45','tip','Hear the recovery stories of villages rebuilt after the 2015 earthquake.'),('2','Lama Hotel → Langtang village → Kyanjin Gompa','~13 km','6–7 h','Pass Langtang village (3,430 m) to Kyanjin Gompa (3,870 m) — famous for its cheese factory.','90','tip','Try the yak cheese at Kyanjin Gompa.'),('Return','Descent','~24 km','2 days','Descend the same way to Syabrubesi.','30','tip','It can be done in one long day, but two is safer.')],
    tips=[('backpack','Gear',['Sleeping bag','Insulated layer','Headlamp','Purification tablets']),('book','Permits & costs',['Langtang NP entry ~NPR 3,000','Guide mandatory','Budget $400–950']),('shield','Cautions',['Pre-dawn cold','Safety in earthquake-rebuilt areas','Monsoon landslides'])],
    cps=[('Syabrubesi','Starting Point','badge-trailhead','~1,460 m','0 km','Bus terminal'),('Lama Hotel','Village','badge-shelter','2,350 m','Day 1 · ~11 km','Teahouses'),('Langtang village','Village','badge-shelter','3,430 m','Day 2','Teahouses'),('Kyanjin Gompa','Destination','badge-landmark','3,870 m','Days 2–3','Cheese factory · teahouses'),('Back at Syabrubesi','End','badge-trailhead','~1,460 m','~24 km round trip','Bus')],
    map_note='Langtang Valley round trip', map_start='Syabrubesi', map_end='Kyanjin Gompa 3,870 m',
    map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55', map_nodes=[(110,335,10),(460,210,8),(695,55,12)]),
  dict(id='intermediate', color='blue', hex='#456e96', level='Intermediate', meter=3,
    name='Kyanjin Ri Sunrise Course', sub='Kyanjin Gompa + Kyanjin Ri 4,350 m sunrise hike · ~28 km · 7–8 days',
    tabs=['Overview','Route','Map','Tips'],
    pills=pill('ruler','Distance','~28 km')+pill('clock','Duration','7–8 days')+pill('location','Kyanjin Ri','4,350 m')+pill_meter('Difficulty',3,'medium')+pill('star','Sunrise','Langtang Lirung & Annapurna')+pill('location','Permit','Langtang NP'),
    h_flow='Course Flow', h_elev='Elevation Profile', h_route='Route by Section', h_map='Concept Map', h_cp='Checkpoints',
    flow=['Syabrubesi','Kyanjin Gompa 3,870 m','Kyanjin Ri 4,350 m','Descend'],
    elev_label='Kyanjin Ri 4,350 m', elev_path='M20 175 C170 165, 320 138, 470 105 S640 66, 740 48', elev_peak=(740,48),
    desc='The valley round trip plus a sunrise hike up Kyanjin Ri (4,350 m) — a 360-degree panorama over Langtang Lirung (7,234 m) and the Annapurna–Ganesh ranges.',
    segs=[('Days 1–3','Syabrubesi → Kyanjin Gompa','~24 km','3 days','Complete the outbound section and settle at Kyanjin Gompa.','30','tip','A light afternoon walk helps acclimatization on arrival.'),('Day 4','Kyanjin Ri 4,350 m sunrise','~5 km RT','4–5 h','Headlamp up to the Kyanjin Ri platform for the 360-degree Himalayan panorama.','92','warn','Extremely windy — wear a windproof hat and gloves.'),('Days 5–7','Descent','~24 km','2–3 days','Return to Syabrubesi and onward to Kathmandu.','30','tip','Enjoy yak pastures and forest on the way down.')],
    tips=[('backpack','Gear',['Headlamp','Windproof hat & gloves','Sleeping bag','Snacks']),('book','Permits & costs',['Langtang NP entry ~NPR 3,000','Guide mandatory','Budget $400–700']),('shield','Cautions',['Kyanjin Ri winds','Acclimatization above 4,000 m','Monsoon road delays'])],
    cps=[('Syabrubesi','Starting Point','badge-trailhead','~1,460 m','0 km','Bus terminal'),('Kyanjin Gompa','Base','badge-landmark','3,870 m','Days 2–3','Cheese factory'),('Kyanjin Ri 4,350 m','Summit','badge-summit','4,350 m','Day 4 dawn','360° deck'),('Back at Syabrubesi','End','badge-trailhead','~1,460 m','Round trip','Bus')],
    map_note='Kyanjin Ri sunrise course', map_start='Syabrubesi', map_end='Kyanjin Ri 4,350 m',
    map_path='M100 340 C220 326, 330 292, 440 245 S630 100, 700 55', map_nodes=[(100,340,10),(440,245,8),(700,55,12)]),
  dict(id='advanced', color='red', hex='#9f5845', level='Advanced', meter=4,
    name='Tserko Ri Challenge (4,984 m)', sub='Kyanjin Gompa → Tserko Ri 4,984 m · ~34 km · 9–10 days',
    tabs=['Overview','Route','Map','Tips'],
    pills=pill('ruler','Distance','~34 km')+pill('clock','Duration','9–10 days')+pill('location','Tserko Ri','4,984 m')+pill_meter('Difficulty',5,'hard')+pill('star','Feature','~5,000 m viewpoint')+pill('location','Permit','Langtang NP'),
    h_flow='Course Flow', h_elev='Elevation Profile', h_route='Route by Section', h_map='Concept Map', h_cp='Checkpoints',
    flow=['Syabrubesi','Kyanjin Gompa 3,870 m','Tserko Ri 4,984 m','Descend'],
    elev_label='Tserko Ri 4,984 m', elev_path='M20 190 C170 184, 320 160, 470 122 S640 62, 740 40', elev_peak=(740,40),
    desc='The final gate of Langtang trekking — Tserko Ri (4,984 m) approached without supplemental oxygen. At least two nights at Kyanjin Gompa for acclimatization is the safe standard.',
    segs=[('Days 1–3','Syabrubesi → Kyanjin Gompa','~24 km','3 days','Complete the outbound section and settle at Kyanjin Gompa.','30','tip','A light afternoon walk on the back ridge aids acclimatization.'),('Day 4','Kyanjin Ri 4,350 m acclimatization','~5 km RT','4–5 h','Use Kyanjin Ri as an acclimatization climb before Tserko Ri — double adaptation raises success.','55','warn','If symptoms worsen on Kyanjin Ri, giving up Tserko Ri is the safe choice.'),('Day 5','Tserko Ri 4,984 m','~8 km RT','7–9 h','A non-technical climb up moraine slopes to the summit and its near-5,000 m panorama.','95','warn','Approaching 5,000 m — set a turnaround time and keep it.'),('Days 6–9','Descent','~24 km','2–3 days','Return the same way to Syabrubesi and onward to Kathmandu; a Pokhara link is also possible.','30','tip','Pokhara connection after the descent is a popular option.')],
    tips=[('backpack','Gear',['Pulse oximeter','Turnaround alarm','Full expedition set','Emergency food']),('book','Permits & costs',['Langtang NP entry ~NPR 3,000','Guide mandatory','Budget $650–950']),('shield','Cautions',['Non-oxic ~5,000 m climb','Sudden weather changes','Descend immediately when exhausted'])],
    cps=[('Syabrubesi','Starting Point','badge-trailhead','~1,460 m','0 km','Bus terminal'),('Kyanjin Gompa','Acclimatization base','badge-landmark','3,870 m','Days 2–3','Cheese factory'),('Kyanjin Ri','Acclimatization','badge-summit','4,350 m','Day 4','360° deck'),('Tserko Ri 4,984 m','Summit','badge-summit','4,984 m','Day 5','~5,000 m panorama'),('Back at Syabrubesi','End','badge-trailhead','~1,460 m','~34 km round trip','Bus')],
    map_note='Langtang final-gate climb', map_start='Syabrubesi', map_end='Tserko Ri 4,984 m',
    map_path='M90 350 C200 338, 310 308, 420 260 S630 95, 700 50', map_nodes=[(90,350,10),(420,260,8),(700,50,12)]),
 ],
}

_mk('ebc', 'ko', T_EBC_KO, C_EBC['ko'], 'Nepal', 'NP')
_mk('ebc', 'en', T_EBC_EN, C_EBC['en'], 'Nepal', 'NP')
_mk('act', 'ko', T_ACT_KO, C_ACT['ko'], 'Nepal', 'NP')
_mk('act', 'en', T_ACT_EN, C_ACT['en'], 'Nepal', 'NP')
_mk('langtang', 'ko', T_LANGTANG_KO, C_LANGTANG['ko'], 'Nepal', 'NP')
_mk('langtang', 'en', T_LANGTANG_EN, C_LANGTANG['en'], 'Nepal', 'NP')

if __name__ == '__main__':
    mountain, lang = sys.argv[1], sys.argv[2]
    html = build(mountain, lang)
    out = pathlib.Path(f'{mountain}-playbook.html') if lang == 'ko' else pathlib.Path(f'en/{mountain}-playbook.html')
    out.write_text(html, encoding='utf-8')
    print(f'wrote {out} ({len(html.splitlines())} lines)')
