#!/usr/bin/env python3
"""판시판(베트남) + 타이산(중국) + 킨리산(말레이시아) 플레이북 빌더.

사실 게이트 (2026-09 세션 2소스 검증):
- 판시판: Sun World 케이블카 요금(sunparadiseland) × vinpearl(호앙리엔 국립공원
  입장 70,000 VND·등반 허가 300,000 VND·가이드 의무) × vietnam-railway(하노이~사파
  야간열차).
- 타이산: 태안 정부 공식 티켓 페이지(tsgw.taian.gov.cn — 115/100위안·3일 유효·대묘
  포함) × travelchinaguide(케이블카 100위안·홍문 루트·24시간 개방).
- 킨리산: sabahparks 공식 예약 × mountkinabalu.com·borneodream — 일 135명 한정,
  가이드 의무(RM 350, 5인당 1명), 허가 외국인 RM 400, 라반라타 1박 필수.
"""
import pathlib, re, sys

YUSHAN = pathlib.Path('yushan-playbook.html').read_text(encoding='utf-8')
YUSHAN_EN = pathlib.Path('en/yushan-playbook.html').read_text(encoding='utf-8')

IC = 'assets/icons/icons.svg'

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

L = 'ko'

def cp(n, name, badge, badge_cls, alt, km, amen):
    return (f'<div class="timeline-item{" start" if n==1 else ""}">\n<div class="timeline-marker">{n}</div>\n<div class="timeline-content">\n'
            f'<div class="timeline-header">\n<span class="checkpoint-name">{name}</span>\n<span class="badge {badge_cls}">{badge}</span>\n</div>\n'
            f'<div class="timeline-meta">\n<span class="meta-item"><svg class="icon-svg"><use href="{IC}#icon-mountain"></use></svg> {alt}</span>\n'
            f'<span class="meta-item"><svg class="icon-svg"><use href="{IC}#icon-ruler"></use></svg> {km}</span>\n</div>\n'
            f'<div class="timeline-features">\n<span class="feature-label">{"Amenities" if L=="en" else "편의시설"}:</span> {amen}\n      </div>\n</div>\n</div>')

def elev_svg(gradient_id, color, label, path_pts, peak_xy):
    (px, py) = peak_xy
    area = path_pts + ' L740 210 L20 210 Z'
    return (f'<svg viewbox="0 0 760 220"><defs><lineargradient id="{gradient_id}" x1="0" x2="0" y1="0" y2="1">'
            f'<stop offset="0%" stop-color="{color}" stop-opacity=".34"></stop><stop offset="100%" stop-color="{color}" stop-opacity=".05"></stop></lineargradient></defs>'
            f'<path d="{area}" fill="url(#{gradient_id})"></path><path d="{path_pts}" fill="none" stroke="{color}" stroke-linecap="round" stroke-width="4"></path>'
            f'<circle cx="{px}" cy="{py}" fill="{color}" r="6"></circle><text fill="{color}" font-size="12" x="{px-150}" y="{py-10}">{label}</text></svg>')

def map_svg(color, note, start_label, end_label, path, nodes):
    ns = ''.join(f'<circle cx="{cx}" cy="{cy}" fill="{color}" r="{r}"></circle>' for cx, cy, r in nodes)
    return (f'<svg viewbox="0 0 760 420"><rect fill="var(--surface2)" height="400" rx="22" width="740" x="10" y="10"></rect>'
            f'<path d="{path}" fill="none" stroke="{color}" stroke-linecap="round" stroke-width="6"></path>{ns}'
            f'<text font-size="12" x="{nodes[0][0]-60}" y="{nodes[0][1]+28}">{start_label}</text>'
            f'<text font-size="12" x="{nodes[-1][0]-160}" y="{nodes[-1][1]-18}">{end_label}</text>'
            f'<text fill="var(--muted)" font-size="12" x="34" y="44">{note}</text></svg>')

def panels_lang(courses):
    out = []
    for i, c in enumerate(courses):
        active = ' active' if i == 0 else ''
        flow = '<span class="arr">→</span>'.join(f'<span class="chip">{x}</span>' for x in c['flow'])
        segs = ''.join(seg(*s) for s in c['segs'])
        tips = ''.join(tipcard(*t) for t in c['tips'])
        cps = ''.join(cp(n+1, *x) for n, x in enumerate(c['cps']))
        out.append(f'''<section class="panel {c['color']}{active}" id="{c['id']}"><div class="panel-top"><span class="level"><svg class="icon-svg"><use href="{IC}#icon-season"></use></svg> {c['level']}</span><div><div class="panel-name">{c['name']}</div><div class="panel-sub">{c['sub']}</div></div></div><div class="tabs"><button class="tab active" data-tab="overview"><svg class="icon-svg"><use href="{IC}#icon-prep"></use></svg> {c['tab_overview']}</button><button class="tab" data-tab="route"><svg class="icon-svg"><use href="{IC}#icon-book"></use></svg> {c['tab_route']}</button><button class="tab" data-tab="map"><svg class="icon-svg"><use href="{IC}#icon-location"></use></svg> {c['tab_map']}</button><button class="tab" data-tab="tips"><svg class="icon-svg"><use href="{IC}#icon-tip"></use></svg> {c['tab_tips']}</button></div>
<div class="playbook-split-container"><div class="playbook-main-col"><div class="tabpane active" data-pane="overview"><div class="course-stats-summary">
{c['pills']}
</div><div class="section-title"><h2>{c['h_flow']}</h2><div class="line"></div></div><div class="card"><div class="flow">{flow}</div></div><div class="section-title"><h2>{c['h_elev']}</h2><div class="line"></div></div><div class="card elev">{elev_svg('g' + c['id'] + c['color'][:2], c['hex'], c['elev_label'], c['elev_path'], c['elev_peak'])}</div><p class="desc">{c['desc']}</p></div><div class="tabpane" data-pane="route"><div class="section-title"><h2>{c['h_route']}</h2><div class="line"></div></div><div class="segments">{segs}</div></div><div class="tabpane" data-pane="tips"><div class="tips-grid">{tips}</div></div></div><div class="playbook-sidebar-col"><div class="tabpane" data-pane="map"><div class="section-title"><h2>{c['h_map']}</h2><div class="line"></div></div><div class="card map">{map_svg(c['hex'], c['map_note'], c['map_start'], c['map_end'], c['map_path'], c['map_nodes'])}</div><div class="section-title"><h2>{c['h_cp']}</h2><div class="line"></div></div><div class="checkpoint-timeline">
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
    t = t[:panels_start] + panels_lang(COURSES[mountain][lang]) + '\n' + t[panels_end:]

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
    # 후처리: 이중 ../ 방지 (og 치환 부작용)
    t = t.replace('../../assets/img/', '../assets/img/')
    return t

# ═══ 판시판 ═══
FANSIPAN = {
 'ko': {
  'title': '판시판 등산 플레이북',
  'meta': '베트남 최고봉 판시판(3,143m, 인도차이나의 지붕) 가이드. 초급 케이블카 정상 코스, 중급 1일 트레킹, 고급 2일 1박 종주 코스의 상세 경로, 실사 지도 및 팁을 제공합니다.',
  'h1_card': '판시판',
  'p_card': 'Fansipan · 인도차이나의 지붕 3,143m · 사파 기점',
  'hero_alt': '사파 계곡의 녹색 산맥과 구름이 어우러진 베트남 고원 풍경',
  'badge': '판시판 플레이북',
  'h1': '판시판 등산 플레이북',
  'hero_desc': '인도차이나 최고봉 판시판(3,143m) 가이드. 케이블카로 정상을 가볍게 보는 코스부터 정상 트레킹, 2일 1박 종주까지의 상세 경로와 팁을 제공합니다.',
  'btn1': '초급: 케이블카 정상 코스', 'btn2': '중급: 1일 트레킹', 'btn3': '고급: 2일 1박 종주',
  'hero_photographer': 'Dang Cong', 'hero_url': 'https://unsplash.com/photos/EAhm0Uoq0Y8',
  'gal_title': '판시판·사파의 사계 &amp; 명소',
  'lb_zoom': '크게 보기',
  'gallery': [
   ('g1', '정상부 초원의 등반객', "Photo by &lt;a href='https://unsplash.com/photos/HsdhP8O6GU0' target='_blank' rel='noopener'&gt;Vu Thang&lt;/a&gt; on Unsplash"),
   ('g2', '사파 계곡 전경', "Photo by &lt;a href='https://unsplash.com/photos/HobTanxdqMI' target='_blank' rel='noopener'&gt;Vivu Vietnam&lt;/a&gt; on Unsplash"),
   ('g3', '계단식 논', "Photo by &lt;a href='https://unsplash.com/photos/BTv0K50c_4M' target='_blank' rel='noopener'&gt;siamak djamei&lt;/a&gt; on Unsplash"),
   ('g4', '산맥을 바라보는 전망대', "Photo by &lt;a href='https://unsplash.com/photos/NI-nrcVHXvE' target='_blank' rel='noopener'&gt;Jean-Baptiste NORE&lt;/a&gt; on Unsplash"),
  ],
 },
 'en': {
  'title': 'Fansipan Hiking Playbook',
  'meta': 'Guide to Fansipan (3,143 m), the Roof of Indochina, Vietnam. Detailed routes, real maps and tips for the cable-car summit course, a 1-day trek, and the 2-day 1-night traverse.',
  'h1_card': 'Fansipan',
  'p_card': 'Fansipan · Roof of Indochina 3,143 m · Base town Sapa',
  'hero_alt': 'Green ranges and clouds over the Sapa valley in Vietnam\'s highlands',
  'badge': 'Fansipan Playbook',
  'h1': 'Fansipan Hiking Playbook',
  'hero_desc': 'A guide to Fansipan (3,143 m), the highest peak of Indochina — from riding the cable car to the summit platforms, to a guided 1-day trek and the 2-day traverse.',
  'btn1': 'Beginner: Cable Car Summit', 'btn2': 'Intermediate: 1-Day Trek', 'btn3': 'Advanced: 2-Day Traverse',
  'hero_photographer': 'Dang Cong', 'hero_url': 'https://unsplash.com/photos/EAhm0Uoq0Y8',
  'gal_title': 'Fansipan & Sapa Four Seasons &amp; Attractions',
  'lb_zoom': 'View larger',
  'gallery': [
   ('g1', 'Hikers on the summit meadow', "Photo by &lt;a href='https://unsplash.com/photos/HsdhP8O6GU0' target='_blank' rel='noopener'&gt;Vu Thang&lt;/a&gt; on Unsplash"),
   ('g2', 'Sapa valley panorama', "Photo by &lt;a href='https://unsplash.com/photos/HobTanxdqMI' target='_blank' rel='noopener'&gt;Vivu Vietnam&lt;/a&gt; on Unsplash"),
   ('g3', 'Terraced fields', "Photo by &lt;a href='https://unsplash.com/photos/BTv0K50c_4M' target='_blank' rel='noopener'&gt;siamak djamei&lt;/a&gt; on Unsplash"),
   ('g4', 'Viewing deck over the ranges', "Photo by &lt;a href='https://unsplash.com/photos/NI-nrcVHXvE' target='_blank' rel='noopener'&gt;Jean-Baptiste NORE&lt;/a&gt; on Unsplash"),
  ],
 },
}
FANSIPAN_COURSES = {
 'ko': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': '초급',
   'name': '케이블카 정상 코스',
   'sub': '사파 → 케이블카(약 15~20분) → 정상 3,143m 전망대 · 2~3시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','산내 도보','약 1km') + pill('clock','소요 시간','2~3h') + pill('location','정상','3,143m') + pill_meter('난이도',1,'medium') + pill('star','케이블카','왕복 약 85만동') + pill('location','기점','사파'),
   'flow': ['사파 케이블카역','정상역 3,143m','빅불봉·전망대','원점'],
   'elev_label': '정상 3,143m', 'elev_peak': (700, 50),
   'elev_path': 'M20 180 C170 150, 320 105, 480 78 S640 58, 700 50',
   'desc': '세계 최장급 무정차 케이블카 중 하나인 선월드 판시판 레전드 케이블카로 인도차이나 최고봉을 가장 쉽게 밟는 코스입니다. 정상역에서 빅불봉(대불)과 전망 단을 둘러보고, 날씨가 맑으면 운해가 펼쳐집니다.',
   'segs': [
     ('출','사파 → 케이블카역','약 3km','차량 10~15분','사파 중심가에서 케이블카역까지 차량으로 이동합니다. 매표는 온라인 선결제가 줄이 가장 짧습니다.','15','tip','성수기 주말은 표가 매진됩니다. 전날 온라인 예약을 권장합니다.'),
     ('1','케이블카 승차','—','약 15~20분','계곡과 삼림 위를 지나 정상역까지 올라갑니다. 고도가 1,600m에서 3,000m 이상으로 급상승하니 귀 압력에 유의하세요.','50','tip','창가 쪽에 서면 사파 계곡 전경이 보입니다.'),
     ('2','정상역 → 빅불봉·전망대','약 0.6km','1~1.5시간','정상역에서 돌계단을 따라 빅불봉(대기원 불상)과 3,143m 삼각점을 둘러봅니다.','88','warn','정상은 연중 쌀쌀합니다(겨울 영하 권). 방한 겉옷을 준비하세요.'),
     ('하','케이블카 복귀','—','약 15~20분','같은 케이블카로 사파 방면으로 하산합니다.','30','tip','오후에는 안개가 자주 끼니 오전 방문이 확률 높습니다.'),
   ],
   'tips': [
     ('backpack','준비물',['방한 겉옷','우비(안개·소나기)','선크림','현금·카드']),
     ('book','요금',['케이블카 왕복 약 70~90만동','국립공원 입장 별도','온라인 선결제 권장']),
     ('warning','주의',['오후 안개 잦음','정상 저온(겨울 결빙)','성수기 표 매진']),
   ],
   'map_note': '케이블카 정상 체험 코스', 'map_start': '사파 케이블카역', 'map_end': '정상 3,143m',
   'map_path': 'M110 335 C240 315, 350 265, 460 210 S620 95, 695 55',
   'map_nodes': [(110,335,10),(460,210,8),(695,55,12)],
   'cps': [
     ('사파 케이블카역','출발점','badge-trailhead','해발 약 1,600m','누적 0km','매표소·기념품점'),
     ('정상역','도착','badge-trailhead','해발 약 3,000m','케이블카 약 15~20분','카페·화장실'),
     ('빅불봉','명소','badge-landmark','해발 약 3,100m','도보 약 15분','계단'),
     ('정상 삼각점 3,143m','봉우리','badge-summit','해발 3,143m','도보 약 25분','전망대'),
     ('원점 복귀','종점','badge-trailhead','해발 약 1,600m','왕복 케이블카','사파 시내'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': '중급',
   'name': '1일 정상 트레킹',
   'sub': '트람톤 게이트 → 정상 왕복 · 약 10km · 8~10시간 · 가이드 필수',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','왕복 거리','약 10km') + pill('clock','소요 시간','8~10h') + pill('location','정상','3,143m') + pill_meter('난이도',3,'medium') + pill('star','가이드','필수') + pill('location','허가','약 30만동'),
   'flow': ['사파 → 트람톤','정글 오르막','정상 3,143m','당일 하산'],
   'elev_label': '정상 3,143m', 'elev_peak': (740, 46),
   'elev_path': 'M20 185 C170 172, 310 140, 460 104 S640 64, 740 46',
   'desc': '국립공원 트레일을 걸어 정상을 왕복하는 1일 집중 코스입니다. 진한 정글·대나무숲·암반을 거쳐 정상에 도달하며, 호앙리엔 국립공원의 등산 허가와 지정 가이드 동반이 의무입니다. 체력 소모가 크지만 오직 걸어서 인도차이나의 지붕을 밟는 값진 경험입니다.',
   'segs': [
     ('출','사파 → 트람톤 게이트','약 15km','차량 40~50분','사파에서 트람톤 게이트까지 차량 이동 후 트레킹을 시작합니다. 허가·가이드 확인 후 출발합니다.','8','tip','출발은 오전 6~7시가 표준입니다. 늦으면 하산이 어두워집니다.'),
     ('1','게이트 → 숲속 오르막','약 3km','2~2.5시간','진흙·뿌리가 많은 정글 오르막이 이어집니다. 우기에는 더 미끄럽습니다.','35','warn','우기(5~9월)에는 거머리가 있어 긴 양말·긴바지가 필요합니다.'),
     ('2','숲속 → 정상 직전 암반대','약 1.5km','2~2.5시간','수목한계를 넘으며 암반과 안개 구간이 나타납니다. 체감 기온이 급락합니다.','70','warn','정상부는 바람이 강하고 기온이 낮습니다. 방한 의류를 꺼내 입으세요.'),
     ('3','정상 도달','—','30분 체류','3,143m 삼각점과 정상탑에서 인도차이나의 지붕을 확인합니다.','95','tip','케이블카 정상역에서 올라오는 일반 관광객과 만나는 지점입니다.'),
     ('하','원점 하산','약 5km','3~4시간','같은 길로 내려옵니다. 하산 발목·무릎 부담이 큽니다.','30','tip','하산 지연 시 야간 정글 보행이 되므로 마감 시간을 엄수하세요.'),
   ],
   'tips': [
     ('backpack','준비물',['트레킹화(미끄럼 방지)','긴바지·긴양말(거머리)','방한 겉옷','물 2L·행동식']),
     ('book','허가·가이드',['국립공원 입장 약 7만동','등반 허가 약 30만동','지정 가이드 동반 의무']),
     ('warning','주의',['우기 거머리·미끄럼','하산 야간화 방지','정상 저온·강풍']),
   ],
   'map_note': '가이드 동반 1일 트레킹', 'map_start': '트람톤 게이트', 'map_end': '정상 3,143m',
   'map_path': 'M100 340 C220 325, 330 285, 440 235 S630 95, 700 56',
   'map_nodes': [(100,340,10),(440,235,8),(700,56,12)],
   'cps': [
     ('트람톤 게이트','출발점','badge-trailhead','해발 약 1,900m','누적 0km','허가 확인소'),
     ('정글 오르막 구간','트레일','badge-trailhead','해발 약 2,400m','누적 약 3km','안내판'),
     ('수목한계 암반대','핵심','badge-summit','해발 약 2,900m','누적 약 4.5km','암반'),
     ('정상 삼각점','봉우리','badge-summit','해발 3,143m','누적 약 5km','전망대·케이블카역'),
     ('원점 하산','종점','badge-trailhead','해발 약 1,900m','왕복 약 10km','차량 대기'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': '고급',
   'name': '2일 1박 종주 코스',
   'sub': '트람톤 → 정상 → 하산 2일 일정 · 약 19km · 야영 1박 · 가이드+포터',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','총 거리','약 19km') + pill('clock','일정','2일 1박') + pill('location','최고점','3,143m') + pill_meter('난이도',4,'hard') + pill('star','구성','가이드+포터') + pill('location','허가','약 30만동'),
   'flow': ['1일차 트람톤→캠프','2일차 정상 등정','케이블카 또는 도보 하산'],
   'elev_label': '정상 3,143m', 'elev_peak': (700, 44),
   'elev_path': 'M20 188 C180 178, 320 150, 460 115 S620 62, 700 44',
   'desc': '정글 오르막을 나눠 걷고 정상 부근 캠프에서 1박하는 2일 종주 코스입니다. 첫날 체력을 아끼고, 둘째 날 아침 정상에 서는 여유 있는 일정으로 1일 트레킹보다 성공률과 쾌적성이 높습니다. 가이드·포터·허가가 모두 포함된 투어 형태가 일반적입니다.',
   'segs': [
     ('1일차','트람톤 → 중간 캠프','약 4km','4~5시간','정글 오르막을 천천히 오르며 중간 캠프(야영)에 도착합니다. 포터가 텐트·식사를 준비합니다.','45','tip','우기에는 캠프가 흐ilde 젖을 수 있으니 방수포를 확인하세요.'),
     ('1일차 밤','캠프 1박','—','—','고산 밤 기온이 낮습니다. 수면배깅과 보온에 신경 씁니다.','—','warn','야간 기온이 5°C 이하로 떨어질 수 있습니다. 보온 장비가 필수입니다.'),
     ('2일차','캠프 → 정상','약 1km','1.5~2시간','가벼운 짐으로 정상부 암반을 오릅니다. 날씨가 맑으면 일출과 함께 운해를 볼 수 있습니다.','92','tip','일출 전 도착이면 케이블카 관광객보다 먼저 정상을 차지합니다.'),
     ('2일차','하산 (도보 또는 케이블카)','약 5~6km','3~5시간','도보로 원점까지 내려가거나, 정상역에서 케이블카로 하산해 사파로 복귀합니다.','30','tip','체력이 남았다면 도보 하산, 무리라면 케이블카 하산도 좋은 선택입니다.'),
   ],
   'tips': [
     ('backpack','준비물',['수면배깅(5°C 이하)','헤드랜턴','방한 의류','여벌 양말·우비']),
     ('book','투어',['2일 투어 약 250~350만동','가이드·포터·허가 포함','사파 현지 여행사 예약']),
     ('warning','주의',['야영지 한랭','우기 진흙·거머리','하산 교통편 시간 확인']),
   ],
   'map_note': '야영 1박 종주 코스', 'map_start': '트람톤 게이트', 'map_end': '정상 3,143m',
   'map_path': 'M95 345 C210 330, 320 295, 430 250 S630 95, 700 54',
   'map_nodes': [(95,345,10),(430,250,8),(700,54,12)],
   'cps': [
     ('트람톤 게이트','출발점','badge-trailhead','해발 약 1,900m','1일차 0km','허가 확인소'),
     ('중간 캠프','야영','badge-shelter','해발 약 2,800m','1일차 약 4km','텐트·취사'),
     ('정상 삼각점','봉우리','badge-summit','해발 3,143m','2일차 약 1km','전망대'),
     ('케이블카 정상역','선택','badge-trailhead','해발 약 3,000m','하산 연계','카페'),
     ('사파 복귀','종점','badge-trailhead','해발 약 1,600m','2일차 마무리','차량'),
   ],
  },
 ],
 'en': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': 'Beginner',
   'name': 'Cable Car Summit Course',
   'sub': 'Sapa → cable car (~15–20 min) → summit 3,143 m platform · 2–3 hours',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','On-mountain walk','~1 km') + pill('clock','Time','2–3 h') + pill('location','Summit','3,143 m') + pill_meter('Difficulty',1,'medium') + pill('star','Cable car','~850k VND RT') + pill('location','Base','Sapa'),
   'flow': ['Sapa cable-car station','Summit station 3,143 m','Big Buddha & decks','Back to start'],
   'elev_label': 'Summit 3,143 m', 'elev_peak': (700, 50),
   'elev_path': 'M20 180 C170 150, 320 105, 480 78 S640 58, 700 50',
   'desc': 'Ride one of the world\'s longest non-stop cable cars (Sun World Fansipan Legend) to stand on the highest point of Indochina the easy way. Explore the Big Buddha and viewing terraces at the summit station; on clear days a sea of clouds spreads below.',
   'segs': [
     ('Start','Sapa → cable-car station','~3 km','10–15 min drive','Transfer by vehicle from central Sapa. Online prepayment gives the shortest queue.','15','tip','Weekend peak-season tickets sell out — book online the day before.'),
     ('1','Ride the cable car','—','~15–20 min','Cross above valleys and forest as you climb from ~1,600 m to over 3,000 m — mind the ear pressure.','50','tip','Stand on the valley side for the Sapa panorama.'),
     ('2','Summit station → Big Buddha & decks','~0.6 km','1–1.5 h','Stone stairs lead to the Great Buddha and the 3,143 m triangulation point.','88','warn','The summit is cold year-round (below freezing in winter) — bring warm layers.'),
     ('Return','Back by cable car','—','~15–20 min','Ride the same cable car down toward Sapa.','30','tip','Mornings are clearest — fog often rolls in after noon.'),
   ],
   'tips': [
     ('backpack','Gear',['Warm jacket','Rain shell (mist/drizzle)','Sunscreen','Cash & card']),
     ('book','Fees',['Cable car ~700–900k VND round trip','National-park entry separate','Online prepayment recommended']),
     ('warning','Cautions',['Frequent afternoon fog','Cold summit (icy winters)','Ticket sellouts in peak season']),
   ],
   'map_note': 'Easy summit via cable car', 'map_start': 'Sapa cable-car station', 'map_end': 'Summit 3,143 m',
   'map_path': 'M110 335 C240 315, 350 265, 460 210 S620 95, 695 55',
   'map_nodes': [(110,335,10),(460,210,8),(695,55,12)],
   'cps': [
     ('Sapa cable-car station','Starting Point','badge-trailhead','~1,600 m','0 km','Ticket office · shops'),
     ('Summit station','Arrival','badge-trailhead','~3,000 m','~15–20 min by car','Cafe · restrooms'),
     ('Big Buddha','Attraction','badge-landmark','~3,100 m','~15 min walk','Stairs'),
     ('Summit point 3,143 m','Summit','badge-summit','3,143 m','~25 min walk','Viewing decks'),
     ('Back to base','End','badge-trailhead','~1,600 m','Round trip by car','Sapa town'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': 'Intermediate',
   'name': '1-Day Summit Trek',
   'sub': 'Tram Ton gate → summit round trip · about 10 km · 8–10 hours · guide mandatory',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Round trip','~10 km') + pill('clock','Time','8–10 h') + pill('location','Summit','3,143 m') + pill_meter('Difficulty',3,'medium') + pill('star','Guide','Mandatory') + pill('location','Permit','~300k VND'),
   'flow': ['Sapa → Tram Ton','Jungle climb','Summit 3,143 m','Same-day descent'],
   'elev_label': 'Summit 3,143 m', 'elev_peak': (740, 46),
   'elev_path': 'M20 185 C170 172, 310 140, 460 104 S640 64, 740 46',
   'desc': 'A demanding single-day round trip through Hoang Lien National Park — dense jungle, bamboo, and rock to the summit. A park climbing permit and a licensed guide are mandatory. High energy cost, but the reward is standing on the Roof of Indochina entirely on foot.',
   'segs': [
     ('Start','Sapa → Tram Ton gate','~15 km','40–50 min drive','Drive to the Tram Ton gate and start trekking after permit and guide checks.','8','tip','The standard start is 06:00–07:00 — late starts risk finishing in the dark.'),
     ('1','Gate → forest climb','~3 km','2–2.5 h','Muddy, rooty jungle uphill. Wetter and slipperier in the rainy season.','35','warn','Leeches appear in the rainy season (May–Sep) — wear long pants and socks.'),
     ('2','Forest → pre-summit rocks','~1.5 km','2–2.5 h','Past the treeline, rock and fog sections appear; felt temperature drops sharply.','70','warn','Strong wind and cold at the top — put on your warm layers.'),
     ('3','Summit','—','30 min stay','Confirm the 3,143 m marker and the summit tower on the Roof of Indochina.','95','tip','You meet the cable-car visitors coming up from the summit station here.'),
     ('Return','Descent','~5 km','3–4 h','Go back the same way; knees and ankles take a beating.','30','tip','Do not overrun your deadline — night jungle walking is dangerous.'),
   ],
   'tips': [
     ('backpack','Gear',['Anti-slip trekking shoes','Long pants & socks (leeches)','Warm jacket','2 L water + trail food']),
     ('book','Permits & guide',['Park entry ~70k VND','Climbing permit ~300k VND','Licensed guide mandatory']),
     ('warning','Cautions',['Rainy-season leeches & mud','No late descents','Cold & wind on summit']),
   ],
   'map_note': 'Guided 1-day trek', 'map_start': 'Tram Ton gate', 'map_end': 'Summit 3,143 m',
   'map_path': 'M100 340 C220 325, 330 285, 440 235 S630 95, 700 56',
   'map_nodes': [(100,340,10),(440,235,8),(700,56,12)],
   'cps': [
     ('Tram Ton gate','Starting Point','badge-trailhead','~1,900 m','0 km','Permit check'),
     ('Jungle climb','Trail','badge-trailhead','~2,400 m','~3 km','Signposts'),
     ('Above-treeline rocks','Key section','badge-summit','~2,900 m','~4.5 km','Rock field'),
     ('Summit marker','Summit','badge-summit','3,143 m','~5 km','Deck · cable-car station'),
     ('Back at Tram Ton','End','badge-trailhead','~1,900 m','~10 km round trip','Vehicles'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': 'Advanced',
   'name': '2-Day 1-Night Traverse',
   'sub': 'Tram Ton → summit → descent over 2 days · ~19 km · 1 camp night · guide + porter',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Total distance','~19 km') + pill('clock','Duration','2 days 1 night') + pill('location','High point','3,143 m') + pill_meter('Difficulty',4,'hard') + pill('star','Format','Guide + porter') + pill('location','Permit','~300k VND'),
   'flow': ['Day 1: Tram Ton → camp','Day 2: summit push','Descend by foot or cable car'],
   'elev_label': 'Summit 3,143 m', 'elev_peak': (700, 44),
   'elev_path': 'M20 188 C180 178, 320 150, 460 115 S620 62, 700 44',
   'desc': 'Split the jungle climb over two days and sleep at a camp near the summit. The relaxed schedule gives higher success odds and comfort than the 1-day trek. Typically booked as a tour that includes guide, porters, permits, and meals.',
   'segs': [
     ('Day 1','Tram Ton → mid camp','~4 km','4–5 h','Climb the jungle steadily to the intermediate camp (tents). Porters set up tents and cook.','45','tip','In the rainy season check the groundsheet — camps can get damp.'),
     ('Day 1 night','Camp overnight','—','—','High-altitude nights are cold. Focus on insulation.','—','warn','Nights can drop below 5°C — warm sleeping gear is essential.'),
     ('Day 2','Camp → summit','~1 km','1.5–2 h','Climb the rocky summit section with a light pack; sunrise above the cloud sea on clear days.','92','tip','Arriving before dawn beats the cable-car crowds to the marker.'),
     ('Day 2','Descent (foot or cable car)','~5–6 km','3–5 h','Walk all the way down, or ride the cable car from the summit station back toward Sapa.','30','tip','Foot descent if you have energy left; the cable car is a fine alternative.'),
   ],
   'tips': [
     ('backpack','Gear',['Sleeping bag (sub-5°C rating)','Headlamp','Warm layers','Spare socks & rain gear']),
     ('book','Tour',['2-day tour ~2.5–3.5M VND','Guide, porter, permits included','Book via Sapa local agencies']),
     ('warning','Cautions',['Cold camps','Rainy-season mud & leeches','Confirm return transport times']),
   ],
   'map_note': 'Overnight traverse', 'map_start': 'Tram Ton gate', 'map_end': 'Summit 3,143 m',
   'map_path': 'M95 345 C210 330, 320 295, 430 250 S630 95, 700 54',
   'map_nodes': [(95,345,10),(430,250,8),(700,54,12)],
   'cps': [
     ('Tram Ton gate','Starting Point','badge-trailhead','~1,900 m','Day 1 · 0 km','Permit check'),
     ('Mid camp','Camp','badge-shelter','~2,800 m','Day 1 · ~4 km','Tents · cooking'),
     ('Summit marker','Summit','badge-summit','3,143 m','Day 2 · ~1 km','Viewing deck'),
     ('Cable-car summit station','Optional','badge-trailhead','~3,000 m','Descent link','Cafe'),
     ('Back in Sapa','End','badge-trailhead','~1,600 m','End of Day 2','Vehicles'),
   ],
  },
 ],
}

# ═══ 타이산 ═══
TAISHAN = {
 'ko': {
  'title': '타이산 등산 플레이북',
  'meta': '중국 오악 중 동악 태산(1,545m) 가이드. 초급 케이블카 당일 왕복, 중급 홍문 루트 왕복, 고급 야간 등반 일출 코스의 상세 경로, 실사 지도 및 팁을 제공합니다.',
  'h1_card': '타이산',
  'p_card': 'Taishan · 오악의 동악 1,545m · 태안(泰安) 기점',
  'hero_alt': '구름을 뚫고 오르는 산중 계단과 등반객의 실루엣',
  'badge': '타이산 플레이북',
  'h1': '타이산 등산 플레이북',
  'hero_desc': '2,000년 넘게 제왕들의 봉선의지가 치러진 중국 오악의 동악 태산. 케이블카 당일 코스부터 7,000계단 홍문 루트, 야간 등반 일출까지의 상세 경로와 팁을 제공합니다.',
  'btn1': '초급: 케이블카 당일 왕복', 'btn2': '중급: 홍문 루트 왕복', 'btn3': '고급: 야간 등반 일출',
  'hero_photographer': 'Leona Lee', 'hero_url': 'https://unsplash.com/photos/lBmf-p8QbcM',
  'gal_title': '타이산의 사계 &amp; 명소',
  'lb_zoom': '크게 보기',
  'gallery': [
   ('g1', '안개 속 돌계단', "Photo by &lt;a href='https://unsplash.com/photos/Ken8B9aKbBI' target='_blank' rel='noopener'&gt;Jun Weng&lt;/a&gt; on Unsplash"),
   ('g2', '산중 사원', "Photo by &lt;a href='https://unsplash.com/photos/zIIlPb5zrVw' target='_blank' rel='noopener'&gt;Yolanda Suen&lt;/a&gt; on Unsplash"),
   ('g3', '능선 산책로', "Photo by &lt;a href='https://unsplash.com/photos/QM8nxL1X8mE' target='_blank' rel='noopener'&gt;Stefan Wagener&lt;/a&gt; on Unsplash"),
   ('g4', '노을 전망', "Photo by &lt;a href='https://unsplash.com/photos/lEf5rkknW_Y' target='_blank' rel='noopener'&gt;Jane Wu&lt;/a&gt; on Unsplash"),
  ],
 },
 'en': {
  'title': 'Mount Tai Hiking Playbook',
  'meta': 'Guide to Mount Tai (Taishan, 1,545 m), the Eastern Great Mountain of China\'s Five. Detailed routes, real maps and tips for the cable-car day trip, the Red Gate round trip, and the night climb for sunrise.',
  'h1_card': 'Mount Tai',
  'p_card': 'Taishan · Eastern Great Mountain 1,545 m · Base city Tai\'an',
  'hero_alt': 'Hikers climbing stone stairs into the clouds',
  'badge': 'Mount Tai Playbook',
  'h1': 'Mount Tai Hiking Playbook',
  'hero_desc': 'For over 2,000 years emperors climbed Taishan for the Fengshan sacrifice. Routes from an easy cable-car day trip to the 7,000-step Red Gate route and the night climb for sunrise.',
  'btn1': 'Beginner: Cable Car Day Trip', 'btn2': 'Intermediate: Red Gate Round Trip', 'btn3': 'Advanced: Night Climb for Sunrise',
  'hero_photographer': 'Leona Lee', 'hero_url': 'https://unsplash.com/photos/lBmf-p8QbcM',
  'gal_title': 'Mount Tai Four Seasons &amp; Attractions',
  'lb_zoom': 'View larger',
  'gallery': [
   ('g1', 'Stone stairs in the fog', "Photo by &lt;a href='https://unsplash.com/photos/Ken8B9aKbBI' target='_blank' rel='noopener'&gt;Jun Weng&lt;/a&gt; on Unsplash"),
   ('g2', 'Mountain temple', "Photo by &lt;a href='https://unsplash.com/photos/zIIlPb5zrVw' target='_blank' rel='noopener'&gt;Yolanda Suen&lt;/a&gt; on Unsplash"),
   ('g3', 'Ridge walkway', "Photo by &lt;a href='https://unsplash.com/photos/QM8nxL1X8mE' target='_blank' rel='noopener'&gt;Stefan Wagener&lt;/a&gt; on Unsplash"),
   ('g4', 'Sunset outlook', "Photo by &lt;a href='https://unsplash.com/photos/lEf5rkknW_Y' target='_blank' rel='noopener'&gt;Jane Wu&lt;/a&gt; on Unsplash"),
  ],
 },
}
TAISHAN_COURSES = {
 'ko': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': '초급',
   'name': '케이블카 당일 왕복',
   'sub': '천외촌 셔틀 → 중천문 케이블카 → 옥황정 1,545m 왕복 · 3~4시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','산내 도보','약 2km') + pill('clock','소요 시간','3~4h') + pill('location','옥황정','1,545m') + pill_meter('난이도',1,'medium') + pill('star','입장료','115위안') + pill('location','케이블카','100위안'),
   'flow': ['천외촌 셔틀','중천문 케이블카','남천문·옥황정','원점'],
   'elev_label': '옥황정 1,545m', 'elev_peak': (700, 52),
   'elev_path': 'M20 170 C180 160, 330 125, 480 95 S640 62, 700 52',
   'desc': '셔틀과 케이블카를 조합해 태산 정상부를 가장 편하게 도는 코스입니다. 남천문·천가(天街)·옥황정을 걸으며 제왕의 산의 상징물을 둘러보고, 날씨가 맑으면 일출·운해도 가능합니다.',
   'segs': [
     ('출','천외촌 셔틀','약 8km','20분','태안 시내에서 천외촌까지 셔틀버스(30위안)로 이동합니다.','12','tip','성수기 셔틀 대기가 깁니다. 이른 오전 도착이 유리합니다.'),
     ('1','중천문 케이블카','—','약 10분','케이블카(100위안)로 중천문→남천문 구간을 한 번에 올라갑니다.','50','tip','창밖 18반(십팔반) 계단의 웅장함을 내려다볼 수 있습니다.'),
     ('2','남천문 → 옥황정','약 1.5km','1~1.5시간','천가(天街)·벽하사(碧霞祠)를 지나 태산 최고점 옥황정(1,545m)에 도달합니다.','88','tip','정상의 「오악독존」 석비가 명소입니다.'),
     ('하','원점 복귀','—','1.5~2시간','케이블카와 셔틀로 되돌아옵니다.','30','tip','일출을 보려면 야간 등반 코스로 연결하세요.'),
   ],
   'tips': [
     ('backpack','준비물',['편한 워킹화','방풍 겉옷','물·간식','여권(실명 확인)']),
     ('book','입장·요금',['입장료 115위안(성수기)·3일 유효·대묘 포함','케이블카 100위안 편도','셔틀 30위안']),
     ('warning','주의',['성수기 인파 대기','정상 강풍·저온','겨울 결빙 구간']),
   ],
   'map_note': '케이블카 당일 코스', 'map_start': '천외촌 셔틀', 'map_end': '옥황정 1,545m',
   'map_path': 'M110 335 C240 315, 350 265, 460 210 S620 95, 695 55',
   'map_nodes': [(110,335,10),(460,210,8),(695,55,12)],
   'cps': [
     ('천외촌 셔틀 하차','출발점','badge-trailhead','해발 약 700m','누적 0km','매표소'),
     ('중천문 케이블카역','승차','badge-trailhead','해발 약 950m','셔틀 도착','역사'),
     ('남천문','관문','badge-landmark','해발 약 1,400m','케이블카 하차','천가 시작'),
     ('옥황정','봉우리','badge-summit','해발 1,545m','누적 약 1.5km','전망대·신사'),
     ('원점 복귀','종점','badge-trailhead','해발 약 700m','왕복','셔틀'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': '중급',
   'name': '홍문 루트 당일 왕복',
   'sub': '홍문 → 중천문 → 남천문 → 옥황정 왕복 · 약 12km · 6~8시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','왕복 거리','약 12km') + pill('clock','소요 시간','6~8h') + pill('location','옥황정','1,545m') + pill_meter('난이도',3,'medium') + pill('star','계단','약 7,000여 개') + pill('location','입장료','115위안'),
   'flow': ['홍문 출발','중천문','십팔반','옥황정 1,545m','도보 하산'],
   'elev_label': '옥황정 1,545m', 'elev_peak': (740, 48),
   'elev_path': 'M20 180 C170 174, 320 150, 470 112 S640 68, 740 48',
   'desc': '2,000년 순례길 그대로인 홍문(红门) 루트를 도보로 왕복하는 태산의 정석 코스입니다. 7,000여 개의 돌계단을 오르며 문방·중천문·십팔반을 거쳐 정상에 서고, 같은 길로 내려옵니다. 옛 제왕과 선비들이 걸은 길 그 자체가 볼거리입니다.',
   'segs': [
     ('출','홍문 출발','0km','—','태안 시내 남쪽 홍문궁에서 시작합니다. 아침 일찍 출발해 오후 하산을 마칩니다.','5','tip','출발 전 홍문궁 주변에서 물·간식을 구비하세요.'),
     ('1','홍문 → 중천문','약 5.5km','2.5~3.5시간','완만한 계단이 계속되며 만선누·두모앙 등 고적을 지납니다.','45','tip','중천문에서 쉬어가며 이후 구간의 강도를 대비하세요.'),
     ('2','중천문 → 남천문 (십팔반)','약 0.8km','1~1.5시간','태산 최대 난관인 십팔반(十八盘)의 가파른 계단을 오릅니다. 남천문는 「천상(天上)」의 관문입니다.','80','warn','계단이 매우 가파릅니다. 지그재그로 페이스를 조절하세요.'),
     ('3','남천문 → 옥황정','약 1.5km','1~1.5시간','천가·벽하사를 지나 옥황정에 도달합니다.','92','tip','정상에서 태안 시내와 운해를 조망합니다.'),
     ('하','도보 하산','약 6km','2.5~3.5시간','같은 홍문 루트로 내려옵니다. 십팔반 하산 시 무릎 보호대가 필수입니다.','30','warn','하산 계단 부담이 큽니다. 무리하면 중천문에서 케이블카를 타세요.'),
   ],
   'tips': [
     ('backpack','준비물',['트레킹화','무릎 보호대','스틱','물 1.5L 이상']),
     ('book','입장',['입장료 115위안·3일 유효','24시간 개방(야간 등반 가능)','대묘 포함']),
     ('warning','주의',['십팔반 급계단','하산 무릎 부담','겨울 결빙']),
   ],
   'map_note': '홍문 정석 도보 루트', 'map_start': '홍문궁', 'map_end': '옥황정 1,545m',
   'map_path': 'M100 345 C220 332, 330 300, 440 250 S630 100, 700 55',
   'map_nodes': [(100,345,10),(440,250,8),(700,55,12)],
   'cps': [
     ('홍문궁','출발점','badge-trailhead','해발 약 250m','누적 0km','문·화장실'),
     ('중천문','휴게','badge-shelter','해발 약 950m','누적 약 5.5km','케이블카역·식당'),
     ('십팔반','핵심','badge-summit','해발 약 1,300m','누적 약 6.3km','급계단'),
     ('남천문','관문','badge-landmark','해발 약 1,400m','누적 약 7km','천가'),
     ('옥황정','봉우리','badge-summit','해발 1,545m','누적 약 8.5km','전망대'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': '고급',
   'name': '야간 등반 일출 코스',
   'sub': '심야 홍문 출발 → 새벽 옥황정 일출 → 하산 · 약 12km · 8~10시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','왕복 거리','약 12km') + pill('clock','소요 시간','8~10h') + pill('location','옥황정','1,545m') + pill_meter('난이도',3,'medium') + pill('star','출발','23:00~01:00') + pill('location','목표','일출'),
   'flow': ['심야 홍문 출발','한랭 새벽 등반','옥황정 일출','하산'],
   'elev_label': '옥황정 일출 1,545m', 'elev_peak': (740, 46),
   'elev_path': 'M20 182 C170 176, 320 148, 470 110 S640 64, 740 46',
   'desc': '태산 24시간 개방을 활용해 심야에 홍문을 나서 새벽 정상 일출을 맞이하는 전통 코스입니다. 헤드랜턴을 켜고 7,000계단을 밤새 올라 일출과 운해를 본 뒤 하산합니다. 「밤새 올라 일출로 갚는다」는 태산 문화의 핵심입니다.',
   'segs': [
     ('출','심야 홍문 출발','0km','23:00~01:00','일출 시각에서 역산해 5~6시간 전에 홍문에서 출발합니다. 헤드랜턴 착용이 필수입니다.','8','tip','야간에는 기온이 낮아 대기·휴식 시 몸이 급격히 식습니다. 행동 보온을 유지하세요.'),
     ('1','홍문 → 중천문','약 5.5km','3~3.5시간','밤 계단길을 조용히 오릅니다. 주변에 같은 야간 등반객이 많아 외롭지 않습니다.','45','warn','한겨울에는 계단 결빙이 있습니다. 아이젠을 준비하세요.'),
     ('2','십팔반 → 옥황정','약 2.3km','1.5~2시간','십팔반의 밤 계단은 더 가파르게 느껴집니다. 남천문을 지나 정상 대기지역에 도착합니다.','85','warn','정상 대기 시간이 길어집니다. 최상위 보온(방한재킷·모자·장갑)을 착용하세요.'),
     ('3','일출 감상','—','30~60분','옥황정·일출봉 전망대에서 일출을 맞이합니다. 운해가 겹치는 날이 최고입니다.','95','tip','일출 후 산상에서 아침을 먹고 하산을 시작하세요.'),
     ('하','하산','약 6km','2.5~3.5시간','도보 하산 또는 중천문 케이블카+셔틀로 복귀합니다.','30','tip','새벽 산행 후 졸음이 오므로 케이블카 조합도 현명한 선택입니다.'),
   ],
   'tips': [
     ('backpack','준비물',['헤드랜턴','방한 재킷·모자·장갑','아이젠(겨울)','따뜻한 음료']),
     ('book','입장',['입장료 115위안(24시간 입산)','일출 시각 사전 확인','주말 인파 유의']),
     ('warning','주의',['새벽 한랭','겨울 결빙 계단','졸음 하산 사고']),
   ],
   'map_note': '야간 등반 일출 코스', 'map_start': '홍문궁(심야)', 'map_end': '옥황정 일출',
   'map_path': 'M100 348 C220 336, 330 302, 440 252 S630 100, 700 52',
   'map_nodes': [(100,348,10),(440,252,8),(700,52,12)],
   'cps': [
     ('홍문궁(심야 출발)','출발점','badge-trailhead','해발 약 250m','누적 0km','야간 개방'),
     ('중천문','휴게','badge-shelter','해발 약 950m','누적 약 5.5km','보급·휴식'),
     ('십팔반','핵심','badge-summit','해발 약 1,300m','누적 약 6.3km','급계단'),
     ('옥황정 일출','봉우리','badge-summit','해발 1,545m','누적 약 8.5km','일출 전망대'),
     ('하산 복귀','종점','badge-trailhead','해발 약 250m','왕복 약 12km','홍문'),
   ],
  },
 ],
 'en': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': 'Beginner',
   'name': 'Cable Car Day Trip',
   'sub': 'Tianwaicun shuttle → Zhongtianmen cable car → Yuhuangding 1,545 m round trip · 3–4 hours',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','On-mountain walk','~2 km') + pill('clock','Time','3–4 h') + pill('location','Yuhuangding','1,545 m') + pill_meter('Difficulty',1,'medium') + pill('star','Entry','115 RMB') + pill('location','Cable car','100 RMB'),
   'flow': ['Tianwaicun shuttle','Zhongtianmen cable car','Nantianmen · Yuhuangding','Back to start'],
   'elev_label': 'Yuhuangding 1,545 m', 'elev_peak': (700, 52),
   'elev_path': 'M20 170 C180 160, 330 125, 480 95 S640 62, 700 52',
   'desc': 'The easiest way around Taishan\'s summit area, combining the shuttle and the Zhongtianmen cable car. Walk Nantianmen, Tianjie (Heaven Street), and the Yuhuangding — with sunrise and cloud-sea chances on clear days.',
   'segs': [
     ('Start','Tianwaicun shuttle','~8 km','20 min','Ride the shuttle bus (30 RMB) from Tai\'an city to Tianwaicun.','12','tip','Queues grow in peak season — arrive early morning.'),
     ('1','Zhongtianmen cable car','—','~10 min','The cable car (100 RMB) lifts you from Zhongtianmen to Nantianmen in one go.','50','tip','Look down at the mighty Eighteen Bends staircase.'),
     ('2','Nantianmen → Yuhuangding','~1.5 km','1–1.5 h','Walk Tianjie street past Bixia Temple to Yuhuangding (1,545 m), the highest point.','88','tip','The "Most Venerated of the Five Greats" stele is a highlight.'),
     ('Return','Back to start','—','1.5–2 h','Return by cable car and shuttle.','30','tip','For sunrise, connect to the night-climb course instead.'),
   ],
   'tips': [
     ('backpack','Gear',['Comfortable walking shoes','Windproof layer','Water & snacks','Passport (real-name check)']),
     ('book','Entry & fees',['Entry 115 RMB peak · valid 3 days · Dai Temple included','Cable car 100 RMB one way','Shuttle 30 RMB']),
     ('warning','Cautions',['Peak-season queues','Cold & windy summit','Icy sections in winter']),
   ],
   'map_note': 'Cable-car day course', 'map_start': 'Tianwaicun shuttle', 'map_end': 'Yuhuangding 1,545 m',
   'map_path': 'M110 335 C240 315, 350 265, 460 210 S620 95, 695 55',
   'map_nodes': [(110,335,10),(460,210,8),(695,55,12)],
   'cps': [
     ('Tianwaicun shuttle stop','Starting Point','badge-trailhead','~700 m','0 km','Ticket office'),
     ('Zhongtianmen cable-car station','Board','badge-trailhead','~950 m','Shuttle arrival','Station'),
     ('Nantianmen','Gate','badge-landmark','~1,400 m','Cable-car top','Tianjie begins'),
     ('Yuhuangding','Summit','badge-summit','1,545 m','~1.5 km','Viewpoint · shrine'),
     ('Back at base','End','badge-trailhead','~700 m','Round trip','Shuttle'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': 'Intermediate',
   'name': 'Red Gate Round Trip',
   'sub': 'Hongmen → Zhongtianmen → Nantianmen → Yuhuangding round trip · about 12 km · 6–8 hours',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Round trip','~12 km') + pill('clock','Time','6–8 h') + pill('location','Yuhuangding','1,545 m') + pill_meter('Difficulty',3,'medium') + pill('star','Stairs','~7,000 steps') + pill('location','Entry','115 RMB'),
   'flow': ['Depart Hongmen','Zhongtianmen','Eighteen Bends','Yuhuangding 1,545 m','Walk down'],
   'elev_label': 'Yuhuangding 1,545 m', 'elev_peak': (740, 48),
   'elev_path': 'M20 180 C170 174, 320 150, 470 112 S640 68, 740 48',
   'desc': 'The classic pilgrimage route, walked the same way for two millennia — up the 7,000-odd stone steps from Hongmen through temples and the fearsome Eighteen Bends to the summit, and back down the same way. The path itself is the attraction.',
   'segs': [
     ('Start','Depart Hongmen','0 km','—','Begin at Hongmen Palace on the south side of Tai\'an. Start early to finish the descent in daylight.','5','tip','Stock up on water and snacks around Hongmen Palace.'),
     ('1','Hongmen → Zhongtianmen','~5.5 km','2.5–3.5 h','Gentle continuous stairs past historic sites such as Wanshanlou and Doumu Palace.','45','tip','Rest well at Zhongtianmen before the steepest section.'),
     ('2','Zhongtianmen → Nantianmen (Eighteen Bends)','~0.8 km','1–1.5 h','The famous Eighteen Bends — Taishan\'s steepest staircase and the gateway to "heaven."','80','warn','Very steep — zigzag and manage your pace.'),
     ('3','Nantianmen → Yuhuangding','~1.5 km','1–1.5 h','Walk Tianjie past Bixia Temple to the summit.','92','tip','Views over Tai\'an city and cloud seas from the top.'),
     ('Return','Descent on foot','~6 km','2.5–3.5 h','Descend the same Red Gate route; knee braces are essential on the Eighteen Bends.','30','warn','The descent is hard on the knees — the Zhongtianmen cable car is a sensible bailout.'),
   ],
   'tips': [
     ('backpack','Gear',['Hiking boots','Knee braces','Trekking poles','1.5 L+ water']),
     ('book','Entry',['Entry 115 RMB · valid 3 days','Open 24 hours (night climbs allowed)','Dai Temple included']),
     ('warning','Cautions',['Steep Eighteen Bends','Knee strain on descent','Icy in winter']),
   ],
   'map_note': 'Classic Red Gate walking route', 'map_start': 'Hongmen Palace', 'map_end': 'Yuhuangding 1,545 m',
   'map_path': 'M100 345 C220 332, 330 300, 440 250 S630 100, 700 55',
   'map_nodes': [(100,345,10),(440,250,8),(700,55,12)],
   'cps': [
     ('Hongmen Palace','Starting Point','badge-trailhead','~250 m','0 km','Gate · restrooms'),
     ('Zhongtianmen','Rest','badge-shelter','~950 m','~5.5 km','Cable-car station · food'),
     ('Eighteen Bends','Key section','badge-summit','~1,300 m','~6.3 km','Steep stairs'),
     ('Nantianmen','Gate','badge-landmark','~1,400 m','~7 km','Tianjie street'),
     ('Yuhuangding','Summit','badge-summit','1,545 m','~8.5 km','Viewpoint'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': 'Advanced',
   'name': 'Night Climb for Sunrise',
   'sub': 'Late-night Hongmen start → dawn Yuhuangding sunrise → descent · about 12 km · 8–10 hours',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Round trip','~12 km') + pill('clock','Time','8–10 h') + pill('location','Yuhuangding','1,545 m') + pill_meter('Difficulty',3,'medium') + pill('star','Start','23:00–01:00') + pill('location','Goal','Sunrise'),
   'flow': ['Late-night Hongmen start','Cold dawn climb','Yuhuangding sunrise','Descent'],
   'elev_label': 'Sunrise at Yuhuangding 1,545 m', 'elev_peak': (740, 46),
   'elev_path': 'M20 182 C170 176, 320 148, 470 110 S640 64, 740 46',
   'desc': 'Use Taishan\'s 24-hour opening: leave Hongmen after midnight, climb the stairs all night with a headlamp, and greet the sunrise from the summit — the heart of Taishan culture ("climb by night, repay with sunrise").',
   'segs': [
     ('Start','Late-night Hongmen start','0 km','23:00–01:00','Depart 5–6 hours before sunrise, working backwards from the sun\'s time. A headlamp is mandatory.','8','tip','You cool down fast during breaks at night — keep moving to stay warm.'),
     ('1','Hongmen → Zhongtianmen','~5.5 km','3–3.5 h','Climb the quiet night stairs; many fellow night climbers make it sociable.','45','warn','Steps can ice over in winter — bring crampons.'),
     ('2','Eighteen Bends → Yuhuangding','~2.3 km','1.5–2 h','The bends feel even steeper at night. Beyond Nantianmen, join the summit waiting crowd.','85','warn','Waiting at the top gets long — wear your best insulation (jacket, hat, gloves).'),
     ('3','Sunrise','—','30–60 min','Greet the sunrise from Yuhuangding or the Riguan platform; cloud seas make it unforgettable.','95','tip','Have breakfast on the summit before starting down.'),
     ('Return','Descent','~6 km','2.5–3.5 h','Walk down, or take the Zhongtianmen cable car plus shuttle.','30','tip','After a sleepless night the cable-car option is a wise choice.'),
   ],
   'tips': [
     ('backpack','Gear',['Headlamp','Insulated jacket, hat, gloves','Crampons (winter)','Hot drink']),
     ('book','Entry',['Entry 115 RMB (24-hour access)','Check sunrise time in advance','Weekend crowds are heavy']),
     ('warning','Cautions',['Pre-dawn cold','Icy steps in winter','Sleepy-descent accidents']),
   ],
   'map_note': 'Night climb for sunrise', 'map_start': 'Hongmen (late night)', 'map_end': 'Sunrise at Yuhuangding',
   'map_path': 'M100 348 C220 336, 330 302, 440 252 S630 100, 700 52',
   'map_nodes': [(100,348,10),(440,252,8),(700,52,12)],
   'cps': [
     ('Hongmen Palace (late night)','Starting Point','badge-trailhead','~250 m','0 km','Open 24 h'),
     ('Zhongtianmen','Rest','badge-shelter','~950 m','~5.5 km','Supplies · rest'),
     ('Eighteen Bends','Key section','badge-summit','~1,300 m','~6.3 km','Steep stairs'),
     ('Yuhuangding sunrise','Summit','badge-summit','1,545 m','~8.5 km','Sunrise deck'),
     ('Return to Hongmen','End','badge-trailhead','~250 m','~12 km round trip','Hongmen'),
   ],
  },
 ],
}

# ═══ 킨리산 ═══
KINABALU = {
 'ko': {
  'title': '킨리산 등산 플레이북',
  'meta': '말레이시아 보르네오 킨리산(4,095m) 가이드. 초급 공원 트레일, 중급 2일 1박 정상 등반(틴포혼→라반라타), 고급 비아페라타 코스의 상세 경로, 실사 지도 및 팁을 제공합니다.',
  'h1_card': '킨리산',
  'p_card': 'Kinabalu · 보르네오의 지붕 4,095m · 세계유산',
  'hero_alt': '구름 위로 솟은 킨리산의 웅장한 화강암 봉우리',
  'badge': '킨리산 플레이북',
  'h1': '킨리산 등산 플레이북',
  'hero_desc': '말레이시아 최고봉 킨리산(4,095m) 가이드. 일일 입산 인원이 제한되는 세계유산 정상 등반(틴포혼→라반라타 1박)의 허가·예약·경로와 팁을 정리했습니다.',
  'btn1': '초급: 공원 트레일', 'btn2': '중급: 2일 1박 정상 등반', 'btn3': '고급: 비아페라타 도전',
  'hero_photographer': 'Ong Cheng Zheng', 'hero_url': 'https://unsplash.com/photos/juFTPN6uv3w',
  'gal_title': '킨리산의 사계 &amp; 명소',
  'lb_zoom': '크게 보기',
  'gallery': [
   ('g1', '암릉을 오르는 등반객', "Photo by &lt;a href='https://unsplash.com/photos/XjUhALD9HO4' target='_blank' rel='noopener'&gt;Ling Tang&lt;/a&gt; on Unsplash"),
   ('g2', '운해 위 정상 능선', "Photo by &lt;a href='https://unsplash.com/photos/QyBVb0zw6Vw' target='_blank' rel='noopener'&gt;Bryan Heng&lt;/a&gt; on Unsplash"),
   ('g3', '정상부 암반대', "Photo by &lt;a href='https://unsplash.com/photos/rZAxaU6Cp2I' target='_blank' rel='noopener'&gt;Ong Cheng Zheng&lt;/a&gt; on Unsplash"),
   ('g4', '구름 앞 산맥', "Photo by &lt;a href='https://unsplash.com/photos/vk2gTv6Qd80' target='_blank' rel='noopener'&gt;Bryan Heng&lt;/a&gt; on Unsplash"),
  ],
 },
 'en': {
  'title': 'Mount Kinabalu Playbook',
  'meta': 'Guide to Mount Kinabalu (4,095 m), Borneo, Malaysia. Detailed routes, real maps and tips for the park trails, the 2-day summit climb via Laban Rata, and the Via Ferrata challenge.',
  'h1_card': 'Mount Kinabalu',
  'p_card': 'Kinabalu · Roof of Borneo 4,095 m · UNESCO World Heritage',
  'hero_alt': 'Kinabalu\'s mighty granite peaks rising above the clouds',
  'badge': 'Mount Kinabalu Playbook',
  'h1': 'Mount Kinabalu Playbook',
  'hero_desc': 'A guide to Malaysia\'s highest peak, Mount Kinabalu (4,095 m) — permits, booking, and routes for the quota-limited UNESCO summit climb via Timpohon Gate and Laban Rata.',
  'btn1': 'Beginner: Park Trails', 'btn2': 'Intermediate: 2-Day Summit Climb', 'btn3': 'Advanced: Via Ferrata',
  'hero_photographer': 'Ong Cheng Zheng', 'hero_url': 'https://unsplash.com/photos/juFTPN6uv3w',
  'gal_title': 'Kinabalu Four Seasons &amp; Attractions',
  'lb_zoom': 'View larger',
  'gallery': [
   ('g1', 'Climbers on the upper trail', "Photo by &lt;a href='https://unsplash.com/photos/XjUhALD9HO4' target='_blank' rel='noopener'&gt;Ling Tang&lt;/a&gt; on Unsplash"),
   ('g2', 'Summit ridge above the clouds', "Photo by &lt;a href='https://unsplash.com/photos/QyBVb0zw6Vw' target='_blank' rel='noopener'&gt;Bryan Heng&lt;/a&gt; on Unsplash"),
   ('g3', 'Summit plateau rocks', "Photo by &lt;a href='https://unsplash.com/photos/rZAxaU6Cp2I' target='_blank' rel='noopener'&gt;Ong Cheng Zheng&lt;/a&gt; on Unsplash"),
   ('g4', 'Ranges before the clouds', "Photo by &lt;a href='https://unsplash.com/photos/vk2gTv6Qd80' target='_blank' rel='noopener'&gt;Bryan Heng&lt;/a&gt; on Unsplash"),
  ],
 },
}
KINABALU_COURSES = {
 'ko': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': '초급',
   'name': '키나발루 공원 트레일',
   'sub': '공원 본부 주변 식물 트레일 · 약 2~3km · 2~3시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','거리','약 2~3km') + pill('clock','소요 시간','2~3h') + pill('location','해발','약 1,500~1,600m') + pill_meter('난이도',1,'medium') + pill('star','특징','세계유산 식물') + pill('location','입장','공원 입장료'),
   'flow': ['공원 본부','식물원 트레일','전망 지점','원점'],
   'elev_label': '공원 트레일', 'elev_peak': (560, 96),
   'elev_path': 'M20 140 C160 135, 300 122, 440 108 S520 102, 560 96',
   'desc': '정상 등반이 부담이라면 키나발루 공원(유네스코 세계유산) 내 완만한 식물 트레일로 킨리산을 만나보세요. 세계에서 가장 풍부한 고산 식물상 중 하나인 소나무·난초·식충식물을 감상하는 가볍고 알찬 코스입니다.',
   'segs': [
     ('출','공원 입구 → 본부','약 0.5km','15분','코타키나발루에서 약 2시간, 공원 게이트에서 입장료를 지불하고 본부로 이동합니다.','15','tip','본부 전시관에서 킨리산의 생태를 먼저 살펴보면 트레일이 두 배 재미있습니다.'),
     ('1','식물원 트레일','약 1.5km','1~1.5시간','산림 트레일을 따라 고산 식물과 새를 관찰합니다.','60','tip','아침이 조류 관찰에 가장 좋습니다.'),
     ('2','전망 지점','—','30분','맑은 날 킨리산 화강암 봉우리가 한눈에 보입니다.','85','tip','구름이 낀 오후보다 오전 전망이 확률이 높습니다.'),
     ('하','원점 복귀','약 0.5km','20분','본부로 되돌아옵니다.','30','tip','정상 등반 계획이라면 이 트레일이 완벽한 적응 산행입니다.'),
   ],
   'tips': [
     ('backpack','준비물',['우비(산간 소나기)','모기약','망원경(선택)','물·간식']),
     ('book','입장',['공원 입장료 별도','정상 등반과는 별개 예약','공원 운영 시간 확인']),
     ('warning','주의',['산간 소나기','미끄러운 흙길','야생동물 거리 유지']),
   ],
   'map_note': '공원 식물 트레일', 'map_start': '공원 본부', 'map_end': '전망 지점',
   'map_path': 'M120 320 C250 305, 360 260, 470 215 S600 165, 660 135',
   'map_nodes': [(120,320,10),(470,215,8),(660,135,12)],
   'cps': [
     ('공원 본부','출발점','badge-trailhead','해발 약 1,550m','누적 0km','전시관·화장실'),
     ('식물원 트레일','트레일','badge-trailhead','해발 약 1,560m','누적 약 1.5km','안내판'),
     ('전망 지점','전망','badge-landmark','해발 약 1,580m','누적 약 2.5km','벤치'),
     ('원점 복귀','종점','badge-trailhead','해발 약 1,550m','왕복 약 3km','본부'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': '중급',
   'name': '2일 1박 정상 등반',
   'sub': '틴포혼 → 라반라타 1박 → 로우스피크 4,095m → 하산 · 약 17km',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','총 거리','약 17km') + pill('clock','일정','2일 1박') + pill('location','로우스피크','4,095m') + pill_meter('난이도',4,'hard') + pill('star','인원 제한','일 135명') + pill('location','가이드','필수'),
   'flow': ['1일차 틴포혼→라반라타','새벽 정상 등반','로우스피크 4,095m','하산'],
   'elev_label': '로우스피크 4,095m', 'elev_peak': (740, 40),
   'elev_path': 'M20 190 C170 182, 320 158, 470 120 S640 62, 740 40',
   'desc': '유네스코 세계유산 킨리산의 표준 정상 등반 코스입니다. 첫날 틴포혼 게이트에서 라반라타(3,270m)까지 오르고 1박, 둘째 날 새벽에 정상 로우스피크(4,095m)에 서고 하산합니다. 일일 135명 입산 제한과 가이드 동반이 의무라 몇 달 전 예약이 필수입니다.',
   'segs': [
     ('1일차','틴포혼 게이트 → 라반라타','약 6km','4~6시간','계단형 산림길을 오르며 식생이 관목·암반이로 바뀝니다. 라반라타(3,270m)에서 1박합니다.','55','warn','고도 상승이 빠릅니다. 두통·구역이 오면 속도를 늦추고 수분을 섭취하세요.'),
     ('1일차 밤','라반라타 1박','—','—','정상 등반 전 이른 취침이 표준입니다(보통 19~20시). 식사는 산장 제공.','—','tip','새벽 일정에 맞춰 장비를 미리 정리하고 잠드세요.'),
     ('2일차','새벽 정상 등반','약 2.7km','2~3시간','새벽 2~3시 로프와 화강암 슬랩 구간을 오라 정상 로우스피크(4,095m)에 선 뒤 일출을 맞이합니다.','92','warn','정상부는 춥고 바람이 강합니다. 헤드랜턴·방한 의류 필수입니다.'),
     ('2일차','라반라타 → 틴포혼 하산','약 8.7km','4~6시간','같은 길로 하산합니다. 하산 계단 부담이 크므로 스틱을 권장합니다. 하산 완료 후 등반 인증서를 받습니다.','30','tip','하산 마감(보통 10:30~11:00)을 엄수해야 합니다.'),
   ],
   'tips': [
     ('backpack','준비물',['헤드랜턴','방한 재킷·장갑·모자','물 2L·행동식','우비']),
     ('book','허가·예약',['사바파크스 공식 예약(일 135명)','가이드 필수(5인당 1명)','패키지 약 RM 1,740~2,180']),
     ('warning','주의',['고산 증상','하산 마감 시간','새벽 한랭·강풍']),
   ],
   'map_note': '표준 2일 정상 등반', 'map_start': '틴포혼 게이트', 'map_end': '로우스피크 4,095m',
   'map_path': 'M95 345 C210 332, 320 300, 430 255 S630 90, 705 50',
   'map_nodes': [(95,345,10),(430,255,8),(705,50,12)],
   'cps': [
     ('틴포혼 게이트','출발점','badge-trailhead','해발 약 1,866m','1일차 0km','게이트·가이드 배정'),
     ('라반라타','산장','badge-shelter','해발 3,270m','1일차 약 6km','숙박·식사'),
     ('새벽 로프 구간','핵심','badge-summit','해발 약 3,800m','2일차 새벽','로프'),
     ('로우스피크','봉우리','badge-summit','해발 4,095m','2일차 약 2.7km','일출 전망'),
     ('틴포혼 복귀','종점','badge-trailhead','해발 약 1,866m','왕복 약 17km','인증서 수령'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': '고급',
   'name': '비아페라타(로우스피크 서킷) 도전',
   'sub': '정상 등반 + 하산 중 비아페라타 경로 · 세계 최고 고도 비아페라타',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','경로','로우스피크 서킷') + pill('clock','추가 시간','2~4h') + pill('location','고도','3,400~3,800m') + pill_meter('난이도',5,'hard') + pill('star','자격','사전 예약 필수') + pill('location','요금','별도 과금'),
   'flow': ['정상 등반','비아페라타 진입','화강암 회랑 횡단','라반라타 복귀'],
   'elev_label': '비아페라타 회랑', 'elev_peak': (620, 58),
   'elev_path': 'M20 185 C170 175, 300 148, 430 112 S560 78, 620 58',
   'desc': '하산길에 접속하는 세계 최고 고도의 비아페라타(고정 로프 등반로) 코스입니다. 정상 등반 후 화강암 절벽을 안전 로프에 매달려 횡단하며, 전문 강사가 동반합니다. 별도 예약·추가 요금이 필요하고 정상 등반 예약과 함께 몇 달 전에 잡아야 합니다.',
   'segs': [
     ('출','정상 등반 (공통)','—','새벽','표준 2일 일정으로 정상 로우스피크까지 등반합니다. 비아페라타 참가자는 강사와 일정을 조율합니다.','30','tip','비아페라타는 체력 소모가 크니 정상 체류를 짧게 하세요.'),
     ('1','비아페라타 진입','—','30분','정상 직하 진입점에서 하네스·카라비너를 점검하고 강사 안전 브리핑을 받습니다.','45','warn','장비 착용 불량은 즉시 중단 사유입니다. 브리핑을 집중하세요.'),
     ('2','화강암 회랑 횡단','약 0.5km','2~3시간','절벽 횡단·낙차 구간을 고정 로프를 따라 이동합니다. 세계에서 가장 높은 곳에서의 비아페라타입니다.','90','warn','고소공포가 심하면 도중 출구(쇼트 코스)를 선택할 수 있습니다.'),
     ('하','라반라타 복귀 후 하산','약 8.7km','4~6시간','라반라타로 돌아가 아침 식사 후 틴포혼으로 하산합니다.','30','tip','비아페라타 후 하산은 다리가 많이 피곤합니다. 스틱 필수입니다.'),
   ],
   'tips': [
     ('backpack','준비물',['하네스(대여 가능)','장갑(필수)','방한 의류','여분 물·행동식']),
     ('book','예약',['비아페라타 별도 예약·요금','정상 등반 예약과 동시 진행','몇 달 전 확보 권장']),
     ('warning','주의',['고공 절벽 횡단','기상 악화 시 중단','체력 소모 큼']),
   ],
   'map_note': '세계 최고 고도 비아페라타', 'map_start': '로우스피크 방면', 'map_end': '비아페라타 회랑',
   'map_path': 'M90 350 C210 335, 320 305, 430 260 S580 120, 640 70',
   'map_nodes': [(90,350,10),(430,260,8),(640,70,12)],
   'cps': [
     ('정상 직하 진입점','진입','badge-summit','해발 약 3,800m','정상 등반 후','강사 배정'),
     ('회랑 횡단 시작','핵심','badge-summit','해발 약 3,750m','진입 직후','고정 로프'),
     ('낙차 구간','핵심','badge-summit','해발 약 3,600m','횡단 중간','사다리'),
     ('종료 지점','종료','badge-trailhead','해발 약 3,400m','횡단 완료','산장 방면'),
     ('라반라타 복귀','복귀','badge-shelter','해발 3,270m','도보 약 30분','식사·하산'),
   ],
  },
 ],
 'en': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': 'Beginner',
   'name': 'Kinabalu Park Trails',
   'sub': 'Botanical trails around park headquarters · about 2–3 km · 2–3 hours',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Distance','~2–3 km') + pill('clock','Time','2–3 h') + pill('location','Elevation','~1,500–1,600 m') + pill_meter('Difficulty',1,'medium') + pill('star','Highlight','UNESCO flora') + pill('location','Entry','Park fee'),
   'flow': ['Park HQ','Botanical trail','Viewpoint','Back to start'],
   'elev_label': 'Park trail', 'elev_peak': (560, 96),
   'elev_path': 'M20 140 C160 135, 300 122, 440 108 S520 102, 560 96',
   'desc': 'If the summit climb is too much, meet Kinabalu on gentle botanical trails inside Kinabalu Park (UNESCO World Heritage) — home to one of the richest alpine floras on Earth: conifers, orchids, and pitcher plants.',
   'segs': [
     ('Start','Park gate → HQ','~0.5 km','15 min','From Kota Kinabalu (~2 hours by road), pay the park entry fee and continue to headquarters.','15','tip','Visit the exhibition hall first — it makes the trail twice as interesting.'),
     ('1','Botanical trail','~1.5 km','1–1.5 h','Follow forest paths observing montane plants and birds.','60','tip','Mornings are best for birdwatching.'),
     ('2','Viewpoint','—','30 min','On clear days the granite pinnacles of Kinabalu appear in full view.','85','tip','Morning views beat cloudy afternoons.'),
     ('Return','Back to HQ','~0.5 km','20 min','Return to headquarters.','30','tip','If you plan the summit climb, this trail is perfect acclimatization.'),
   ],
   'tips': [
     ('backpack','Gear',['Rain shell (mountain showers)','Insect repellent','Binoculars (optional)','Water & snacks']),
     ('book','Entry',['Separate park entry fee','Independent of summit-climb booking','Check park opening hours']),
     ('warning','Cautions',['Mountain showers','Slippery soil','Keep distance from wildlife']),
   ],
   'map_note': 'Park botanical trails', 'map_start': 'Park HQ', 'map_end': 'Viewpoint',
   'map_path': 'M120 320 C250 305, 360 260, 470 215 S600 165, 660 135',
   'map_nodes': [(120,320,10),(470,215,8),(660,135,12)],
   'cps': [
     ('Park HQ','Starting Point','badge-trailhead','~1,550 m','0 km','Exhibition · restrooms'),
     ('Botanical trail','Trail','badge-trailhead','~1,560 m','~1.5 km','Signposts'),
     ('Viewpoint','Viewpoint','badge-landmark','~1,580 m','~2.5 km','Bench'),
     ('Back at HQ','End','badge-trailhead','~1,550 m','~3 km round trip','HQ'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': 'Intermediate',
   'name': '2-Day Summit Climb',
   'sub': 'Timpohon → Laban Rata overnight → Low\'s Peak 4,095 m → descend · about 17 km',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Total distance','~17 km') + pill('clock','Duration','2 days 1 night') + pill('location',"Low's Peak",'4,095 m') + pill_meter('Difficulty',4,'hard') + pill('star','Quota','135 climbers/day') + pill('location','Guide','Mandatory'),
   'flow': ['Day 1: Timpohon → Laban Rata','Dawn summit push',"Low's Peak 4,095 m",'Descend'],
   'elev_label': "Low's Peak 4,095 m", 'elev_peak': (740, 40),
   'elev_path': 'M20 190 C170 182, 320 158, 470 120 S640 62, 740 40',
   'desc': 'The standard summit climb of UNESCO-listed Kinabalu. Day 1 climbs from Timpohon Gate to Laban Rata (3,270 m) for the night; Day 2 ascends in the dark to Low\'s Peak (4,095 m) for sunrise, then descends. A 135-climber daily quota and a mandatory guide mean booking months ahead.',
   'segs': [
     ('Day 1','Timpohon Gate → Laban Rata','~6 km','4–6 h','Staircase forest paths give way to shrub and rock. Overnight at Laban Rata (3,270 m).','55','warn','Altitude gain is fast — slow down and hydrate if headache or nausea appears.'),
     ('Day 1 night','Laban Rata overnight','—','—','Early lights-out is the norm (around 19:00–20:00); meals are provided by the hut.','—','tip','Organize your gear before sleeping for the pre-dawn start.'),
     ('Day 2','Dawn summit push','~2.7 km','2–3 h','From 02:00–03:00 climb ropes and granite slabs to Low\'s Peak (4,095 m) for sunrise.','92','warn','Cold and windy on top — headlamp and insulated layers are essential.'),
     ('Day 2','Laban Rata → Timpohon descent','~8.7 km','4–6 h','Descend the same way; the stairs punish the knees — poles recommended. Collect your certificate at the gate.','30','tip','Respect the descent deadline (usually 10:30–11:00).'),
   ],
   'tips': [
     ('backpack','Gear',['Headlamp','Insulated jacket, gloves, hat','2 L water + trail food','Rain shell']),
     ('book','Permits & booking',['Sabah Parks official booking (135/day)','Guide mandatory (1 per 5 climbers)','Packages ~RM 1,740–2,180']),
     ('warning','Cautions',['Altitude symptoms','Descent deadline','Pre-dawn cold & wind']),
   ],
   'map_note': 'Standard 2-day summit climb', 'map_start': 'Timpohon Gate', 'map_end': "Low's Peak 4,095 m",
   'map_path': 'M95 345 C210 332, 320 300, 430 255 S630 90, 705 50',
   'map_nodes': [(95,345,10),(430,255,8),(705,50,12)],
   'cps': [
     ('Timpohon Gate','Starting Point','badge-trailhead','~1,866 m','Day 1 · 0 km','Gate · guide assignment'),
     ('Laban Rata','Hut','badge-shelter','3,270 m','Day 1 · ~6 km','Lodging · meals'),
     ('Dawn rope section','Key section','badge-summit','~3,800 m','Day 2 pre-dawn','Fixed ropes'),
     ("Low's Peak",'Summit','badge-summit','4,095 m','~2.7 km','Sunrise viewpoint'),
     ('Back at Timpohon','End','badge-trailhead','~1,866 m','~17 km round trip','Certificate'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': 'Advanced',
   'name': 'Via Ferrata (Low\'s Peak Circuit)',
   'sub': 'Summit climb + via ferrata on descent · world\'s highest via ferrata',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Route',"Low's Peak Circuit") + pill('clock','Extra time','2–4 h') + pill('location','Altitude','3,400–3,800 m') + pill_meter('Difficulty',5,'hard') + pill('star','Requirement','Advance booking') + pill('location','Fee','Separate charge'),
   'flow': ['Summit climb','Via ferrata entry','Granite traverse','Return to Laban Rata'],
   'elev_label': 'Ferrata traverse', 'elev_peak': (620, 58),
   'elev_path': 'M20 185 C170 175, 300 148, 430 112 S560 78, 620 58',
   'desc': 'Attach the world\'s highest via ferrata (fixed-rope climbing route) to your descent after the summit push — traversing granite cliffs clipped to safety cables with a professional instructor. Separate booking and fees are required, reserved months ahead together with the summit climb.',
   'segs': [
     ('Start','Summit climb (shared)','—','Pre-dawn','Climb to Low\'s Peak on the standard 2-day schedule. Ferrata participants coordinate timing with the instructor.','30','tip','The ferrata is energy-intensive — keep summit time short.'),
     ('1','Via ferrata entry','—','30 min','At the entry point below the summit, harnesses and carabiners are checked and the instructor gives a safety briefing.','45','warn','Faulty gear fitting is grounds for immediate cancellation — listen closely.'),
     ('2','Granite traverse','~0.5 km','2–3 h','Move along fixed ropes across cliff traverses and drops — the highest via ferrata on Earth.','90','warn','Severe vertigo? A short-course exit exists partway through.'),
     ('Return','Back to Laban Rata, then down','~8.7 km','4–6 h','Return to Laban Rata for breakfast, then descend to Timpohon.','30','tip','Legs will be tired after the ferrata — poles are essential for the descent.'),
   ],
   'tips': [
     ('backpack','Gear',['Harness (rentable)','Gloves (mandatory)','Insulated clothing','Extra water & trail food']),
     ('book','Reservation',['Separate ferrata booking & fee','Combined with summit booking','Reserve months ahead']),
     ('warning','Cautions',['High cliff traverse','Stopped in bad weather','Energy intensive']),
   ],
   'map_note': "World's highest via ferrata", 'map_start': "Toward Low's Peak", 'map_end': 'Ferrata traverse',
   'map_path': 'M90 350 C210 335, 320 305, 430 260 S580 120, 640 70',
   'map_nodes': [(90,350,10),(430,260,8),(640,70,12)],
   'cps': [
     ('Entry below summit','Entry','badge-summit','~3,800 m','After the summit push','Instructor assigned'),
     ('Traverse start','Key section','badge-summit','~3,750 m','Right after entry','Fixed ropes'),
     ('Exposed section','Key section','badge-summit','~3,600 m','Mid-traverse','Ladders'),
     ('Exit point','Exit','badge-trailhead','~3,400 m','Traverse complete','Toward hut'),
     ('Back at Laban Rata','Return','badge-shelter','3,270 m','~30 min walk','Meals · descent'),
   ],
  },
 ],
}

CONTENT = {
  'fansipan': FANSIPAN,
  'taishan': TAISHAN,
  'kinabalu': KINABALU,
}
COURSES = {
  'fansipan': FANSIPAN_COURSES,
  'taishan': TAISHAN_COURSES,
  'kinabalu': KINABALU_COURSES,
}

if __name__ == '__main__':
    mountain, lang = sys.argv[1], sys.argv[2]
    html = build(mountain, lang)
    out = pathlib.Path(f'{mountain}-playbook.html') if lang == 'ko' else pathlib.Path(f'en/{mountain}-playbook.html')
    out.write_text(html, encoding='utf-8')
    print(f'wrote {out} ({len(html.splitlines())} lines)')
