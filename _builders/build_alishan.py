#!/usr/bin/env python3
"""아리산(阿里山) 플레이북 빌더 — yushan 스켈레톤 변환.

사실 게이트: 입장료 NT$300·축산선 요금·해발 2,216m/2,451m — afrch.forest.gov.tw(공식) ×
recreation.forest.gov.tw(공식) × taiwantrip.com.tw 교차검증 (2026-09 세션).
대탑산 2,663m·거리·소요는 「약」 표기.
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

def panels_lang(_title_site, courses):
    out = []
    for i, c in enumerate(courses):
        active = ' active' if i == 0 else ''
        hexc = c['hex']
        flow = '<span class="arr">→</span>'.join(f'<span class="chip">{x}</span>' for x in c['flow'])
        segs = ''.join(seg(*s) for s in c['segs'])
        tips = ''.join(tipcard(*t) for t in c['tips'])
        cps = ''.join(cp(n+1, *x) for n, x in enumerate(c['cps']))
        out.append(f'''<section class="panel {c['color']}{active}" id="{c['id']}"><div class="panel-top"><span class="level"><svg class="icon-svg"><use href="{IC}#icon-season"></use></svg> {c['level']}</span><div><div class="panel-name">{c['name']}</div><div class="panel-sub">{c['sub']}</div></div></div><div class="tabs"><button class="tab active" data-tab="overview"><svg class="icon-svg"><use href="{IC}#icon-prep"></use></svg> {c['tab_overview']}</button><button class="tab" data-tab="route"><svg class="icon-svg"><use href="{IC}#icon-book"></use></svg> {c['tab_route']}</button><button class="tab" data-tab="map"><svg class="icon-svg"><use href="{IC}#icon-location"></use></svg> {c['tab_map']}</button><button class="tab" data-tab="tips"><svg class="icon-svg"><use href="{IC}#icon-tip"></use></svg> {c['tab_tips']}</button></div>
<div class="playbook-split-container"><div class="playbook-main-col"><div class="tabpane active" data-pane="overview"><div class="course-stats-summary">
{c['pills']}
</div><div class="section-title"><h2>{c['h_flow']}</h2><div class="line"></div></div><div class="card"><div class="flow">{flow}</div></div><div class="section-title"><h2>{c['h_elev']}</h2><div class="line"></div></div><div class="card elev">{elev_svg('g' + c['id'][:3], hexc, c['elev_label'], c['elev_path'], c['elev_peak'])}</div><p class="desc">{c['desc']}</p></div><div class="tabpane" data-pane="route"><div class="section-title"><h2>{c['h_route']}</h2><div class="line"></div></div><div class="segments">{segs}</div></div><div class="tabpane" data-pane="tips"><div class="tips-grid">{tips}</div></div></div><div class="playbook-sidebar-col"><div class="tabpane" data-pane="map"><div class="section-title"><h2>{c['h_map']}</h2><div class="line"></div></div><div class="card map">{map_svg(hexc, c['map_note'], c['map_start'], c['map_end'], c['map_path'], c['map_nodes'])}</div><div class="section-title"><h2>{c['h_cp']}</h2><div class="line"></div></div><div class="checkpoint-timeline">
{cps}
</div></div></div></div>
</section>''')
    return '\n'.join(out)

def build(lang):
    global L
    L = lang
    src = YUSHAN if lang == 'ko' else YUSHAN_EN
    pfx = '' if lang == 'ko' else '../'
    T = CONTENT[lang]

    t = src
    t = re.sub(r'<title>[^<]*</title>', f'<title>{T["title"]}</title>', t, count=1)
    t = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{T["meta"]}" name="description"/>', t, count=1)
    t = t.replace('assets/img/yushan/og.png', f'{pfx}assets/img/alishan/og.png')
    t = t.replace('hreflang="ko" rel="alternate"/><link href="en/yushan-playbook.html"', 'hreflang="ko" rel="alternate"/><link href="en/alishan-playbook.html"') if lang == 'ko' else t
    t = t.replace('href="en/yushan-playbook.html"', 'href="en/alishan-playbook.html"') if lang == 'ko' else t
    t = t.replace('../yushan-playbook.html', '../alishan-playbook.html') if lang == 'en' else t
    t = t.replace('yushan-playbook.html', 'alishan-playbook.html') if lang == 'ko' else t
    t = t.replace('<html data-theme="light" lang="ko">', '<html data-theme="light" lang="en">') if lang == 'en' else t

    t = re.sub(r'<h1>[^<]*</h1><p>[^<]*</p>', f'<h1>{T["h1_card"]}</h1><p>{T["p_card"]}</p>', t, count=1)

    hero_start = t.find('<section class="hero hero-bleed">')
    main_marker = '<main class="wrap">'
    main_idx = t.find(main_marker, hero_start)
    hero_html = f'''<section class="hero hero-bleed">
<picture class="hero-picture" id="heroFallbackImage">
<source sizes="100vw" srcset="{pfx}assets/img/alishan/hero-640.avif 640w, {pfx}assets/img/alishan/hero-1024.avif 1024w, {pfx}assets/img/alishan/hero-1600.avif 1600w, {pfx}assets/img/alishan/hero-2400.avif 2400w" type="image/avif"/>
<source sizes="100vw" srcset="{pfx}assets/img/alishan/hero-640.webp 640w, {pfx}assets/img/alishan/hero-1024.webp 1024w, {pfx}assets/img/alishan/hero-1600.webp 1600w, {pfx}assets/img/alishan/hero-2400.webp 2400w" type="image/webp"/>
<img alt="{T['hero_alt']}" class="hero-img" sizes="100vw" src="{pfx}assets/img/alishan/hero-1600.jpg" srcset="{pfx}assets/img/alishan/hero-640.jpg 640w, {pfx}assets/img/alishan/hero-1024.jpg 1024w, {pfx}assets/img/alishan/hero-1600.jpg 1600w, {pfx}assets/img/alishan/hero-2400.jpg 2400w"/>
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
<span class="credit-author">Photo by <a href="https://unsplash.com/photos/xQLF2p80cAc" rel="noopener" target="_blank">Wildeagle z</a></span>
<span class="credit-divider">/</span>
<span class="credit-source"><a href="https://unsplash.com" rel="noopener" target="_blank">Unsplash</a></span>
</div>
</section>
'''
    t = t[:hero_start] + hero_html + t[main_idx:]

    panels_start = t.find('<section class="panel')
    panels_end = t.find('</main>', panels_start)
    panels = panels_lang(None, COURSES[lang])
    t = t[:panels_start] + panels + '\n' + t[panels_end:]

    gal_start = t.find('<section class="photo-gallery-section">')
    gal_end = t.find('</section>', gal_start) + len('</section>')
    caps = T['gallery']
    items = []
    for i, (name, title, cap) in enumerate(caps):
        items.append(f'''<button aria-haspopup="dialog" aria-label="{title} {T['lb_zoom']}" class="gallery-item" data-credit="{cap}" data-index="{i}">
<picture class="gallery-picture">
<source srcset="{pfx}assets/img/alishan/{name}.avif" type="image/avif"/>
<source srcset="{pfx}assets/img/alishan/{name}.webp" type="image/webp"/>
<img alt="" class="gallery-img" decoding="async" loading="lazy" src="{pfx}assets/img/alishan/{name}.jpg"/>
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

    t = t.replace('data-mountain="yushan"', 'data-mountain="alishan"', 1)
    return t

CONTENT = {
  'ko': {
    'title': '아리산 등산 플레이북',
    'meta': '대만 아리산 국가삼림유락구 가이드. 초급 거목군 목도 루프, 중급 축산 일출 코스, 고급 대탑산 등반 코스의 상세 경로, 실사 지도 및 팁을 제공합니다.',
    'h1_card': '아리산',
    'p_card': 'Alishan · 운해의 숲 · 해발 약 2,200m 고산 휴양 명소',
    'hero_alt': '운해가 뒤덮은 아리산의 웅장한 산맥과 새벽 하늘',
    'badge': '아리산 플레이북',
    'h1': '아리산 등산 플레이북',
    'hero_desc': '대만 대표 고산 휴양지 아리산 가이드. 자매담·거목군 목도 트레일부터 축산 일출 열차, 아리산 최고봉 대탑산(2,663m) 등반까지의 상세 경로와 팁을 제공합니다.',
    'btn1': '초급: 거목 트레일 루프', 'btn2': '중급: 축산 일출 코스', 'btn3': '고급: 대탑산 등반',
    'gal_title': '아리산의 사계 &amp; 명소',
    'lb_zoom': '크게 보기',
    'gallery': [
      ('g1', '아리산 삼림철도', "Photo by &lt;a href='https://unsplash.com/photos/2hwNYr_8qTc' target='_blank' rel='noopener'&gt;Arthur Tseng&lt;/a&gt; on Unsplash"),
      ('g2', '거목군 목도의 삼나무 숲', "Photo by &lt;a href='https://unsplash.com/photos/kj8mMBMomsw' target='_blank' rel='noopener'&gt;Changhyun Cho&lt;/a&gt; on Unsplash"),
      ('g3', '축산 일출', "Photo by &lt;a href='https://unsplash.com/photos/Fv_QUy1KRC0' target='_blank' rel='noopener'&gt;Y S&lt;/a&gt; on Unsplash"),
      ('g4', '숲속 목교', "Photo by &lt;a href='https://unsplash.com/photos/rfmkZRHk6Qw' target='_blank' rel='noopener'&gt;Suzi Kim&lt;/a&gt; on Unsplash"),
    ],
  },
  'en': {
    'title': 'Alishan Hiking Playbook',
    'meta': 'Guide to Alishan National Forest Recreation Area, Taiwan. Detailed routes, real maps and tips for the Giant Tree Trail loop, the Zhushan sunrise train course, and the Datashan summit hike.',
    'h1_card': 'Alishan',
    'p_card': 'Alishan · Sea of clouds · Alpine resort at about 2,200 m',
    'hero_alt': 'Alishan\'s majestic ranges above a sea of clouds under a dawn sky',
    'badge': 'Alishan Playbook',
    'h1': 'Alishan Hiking Playbook',
    'hero_desc': 'A guide to Taiwan\'s iconic alpine retreat, Alishan — from the Sisters Ponds and Giant Tree Trail boardwalks to the Zhushan sunrise train and the summit of Datashan (2,663 m), the highest peak of the Alishan Range.',
    'btn1': 'Beginner: Giant Tree Loop', 'btn2': 'Intermediate: Zhushan Sunrise', 'btn3': 'Advanced: Datashan Summit',
    'gal_title': 'Alishan Four Seasons &amp; Attractions',
    'lb_zoom': 'View larger',
    'gallery': [
      ('g1', 'Alishan Forest Railway', "Photo by &lt;a href='https://unsplash.com/photos/2hwNYr_8qTc' target='_blank' rel='noopener'&gt;Arthur Tseng&lt;/a&gt; on Unsplash"),
      ('g2', 'Cypress forest on the Giant Tree Trail', "Photo by &lt;a href='https://unsplash.com/photos/kj8mMBMomsw' target='_blank' rel='noopener'&gt;Changhyun Cho&lt;/a&gt; on Unsplash"),
      ('g3', 'Zhushan sunrise', "Photo by &lt;a href='https://unsplash.com/photos/Fv_QUy1KRC0' target='_blank' rel='noopener'&gt;Y S&lt;/a&gt; on Unsplash"),
      ('g4', 'Wooden bridge in the forest', "Photo by &lt;a href='https://unsplash.com/photos/rfmkZRHk6Qw' target='_blank' rel='noopener'&gt;Suzi Kim&lt;/a&gt; on Unsplash"),
    ],
  },
}

COURSES = {
 'ko': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': '초급',
   'name': '거목군 목도 루프 코스',
   'sub': '자매담 → 거목군 목도 → 향림신목 · 약 3km · 2~3시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','거리','약 3km') + pill('clock','소요 시간','2~3h') + pill('location','해발','약 2,200m') + pill_meter('난이도',2,'medium') + pill('star','추천 시간','오전') + pill('location','입장료','NT$300'),
   'flow': ['타방센터(자매담)','거목군 목도','향림신목','원점'],
   'elev_label': '거목군 목도 능선', 'elev_peak': (600, 78),
   'elev_path': 'M20 160 C160 150, 300 128, 440 110 S580 90, 600 78',
   'desc': '아리산의 핵심 명소를 한 바퀴에 담는 대표 산책 루프입니다. 자매담 두 연못에서 시작해 수천 그루 삼나무가 늘어선 거목군 목도를 걷고, 천 년 넘은 향림신목을 감상합니다. 완만한 목도와 계단 위주라 초보자도 무리 없이 걷는 코스입니다.',
   'segs': [
     ('출','타방센터 → 자매담','약 0.5km','20~30분','여객센터에서 자매담까지 이어지는 계단길입니다. 두 개의 연못 — 자매담의 고요한 수면과 정자가 첫 볼거리입니다.','15','tip','아침 일찍이면 연못 위에 안개가 깔린 환상적인 풍경을 볼 수 있습니다.'),
     ('1','자매담 → 거목군 목도','약 1.0km','40~60분','거목군 목도가 시작됩니다. 목판길이 거대 삼나무 사이로 이어지며 공기가 맑습니다.','55','tip','천 년삼(香林神木) 방면 표지판을 따라 걷습니다.'),
     ('2','거목군 목도 → 향림신목','약 1.0km','40~60분','천 년이 넘은 향림신목과 신목역(삼림철도)을 지나 소평(沼平) 방면으로 이어집니다.','85','warn','계단이 이어지는 구간이므로 하산 시 무릎 보호대가 유용합니다.'),
     ('하','소평공원 → 원점','약 0.5km','20~30분','소평공원의 벚나무 가로수길을 지나 출발점으로 돌아옵니다.','30','tip','봄철 벚꽃 시즌에는 소평공원 자체가 명소입니다.'),
   ],
   'tips': [
     ('backpack','준비물',['편한 워킹화','방한 겉옷(아침 저온)','물·간식','우비(안개·소나기)']),
     ('book','입장·요금',['입장료 NT$300','대중교통 이용 시 NT$150 할인','삼림철도 지선 별도 요금']),
     ('warning','주의',['아침 기온 10°C 이하 잦음','안개로 시야 제한','성수기 인파']),
   ],
   'map_note': '아리산 핵심 트레일 루프', 'map_start': '타방센터·자매담', 'map_end': '향림신목',
   'map_path': 'M120 320 C240 300, 340 250, 440 210 S600 150, 660 120',
   'map_nodes': [(120,320,10),(440,210,8),(660,120,12)],
   'cps': [
     ('타방센터(자매담)','출발점','badge-trailhead','해발 약 2,150m','누적 0km','화장실·매점·버스정류장'),
     ('거목군 목도','트레일','badge-landmark','해발 약 2,180m','누적 약 1.5km','목판길·안내판'),
     ('향림신목','명소','badge-landmark','해발 약 2,200m','누적 약 2.5km','천 년삼'),
     ('소평공원','휴게','badge-trailhead','해발 약 2,180m','누적 약 2.8km','벚나무길·정자'),
     ('원점(타방센터)','종점','badge-trailhead','해발 약 2,150m','누적 약 3km','식당가'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': '중급',
   'name': '축산 일출 열차 코스',
   'sub': '아리산역 → 축산역(약 25분) → 축산 전망대 일출 → 수진사 · 새벽 일정',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','열차 편도','약 25분') + pill('clock','전체 일정','3~4h') + pill('location','축산역','2,451m') + pill_meter('난이도',2,'medium') + pill('star','출발 시각','일출 1시간 전') + pill('location','요금','NT$150'),
   'flow': ['아리산역 탑승','축산역 2,451m','일출 전망대','수진사·하산'],
   'elev_label': '축산역 2,451m', 'elev_peak': (740, 60),
   'elev_path': 'M20 170 C180 160, 340 130, 500 100 S660 72, 740 60',
   'desc': '아리산의 대명사인 운해 일출을 즐기는 코스입니다. 새벽에 아리산역에서 축산선 열차(약 25분, NT$150)를 타고 해발 2,451m의 축산역으로 올라 일출 전망대에서 태양이 운해 위로 떠오르는 광경을 봅니다. 하산 후 수진사(受鎮宮)와 자연 트레일을 더해 반나절 일정으로 완성됩니다.',
   'segs': [
     ('출','아리산역 탑승','0km','일출 약 1시간 전','일출 시각에 맞춰 출발 시각이 계절별로 달라집니다. 전날 역이나 온라인에서 다음 날 시각을 꼭 확인하고 미리 ticket을 구매하세요.','12','warn','성수기 열차표는 조기 매진됩니다. 전날 예약 또는 이른 도착이 필수입니다.'),
     ('1','축산역 → 일출 전망대','약 0.3km','10~15분','축산역에서 전망대까지 짧은 오르막입니다. 어두운 새벽 이동이므로 헤드랜턴이나 휴대폰 조명을 준비합니다.','50','tip','기온이 낮으므로 도착 직전까지 방한 외투를 입고 있어야 합니다.'),
     ('2','일출 감상','—','30~60분','태양이 운해(바다구름) 위로 떠오르는 순간입니다. 운해는 비 온 다음 날 아침에 나타날 확률이 높습니다.','80','tip','일출 후에는 반대편 대탑산 능선의 실루엣도 감상할 수 있습니다.'),
     ('하','수진사 · 아리산역 하산','약 1km','40~60분','축산에서 걸어 내려오며 수진사(受鎮宮)를 들릅니다. 아리산역 부근에서 삼림철도 지선(신목선·조평선) 또는 도보로 원점에 돌아옵니다.','35','tip','지선 열차(NT$100)를 이용하면 발을 아낄 수 있습니다.'),
   ],
   'tips': [
     ('backpack','준비물',['방한 외투·모자','헤드랜턴','따뜻한 음료','현금(열차표)']),
     ('book','요금',['축산선 편도 NT$150','지선 편도 NT$100','입장료 별도(NT$300)']),
     ('warning','주의',['새벽 기온 급강하','표 조기 매진','안개 시 일출 불가']),
   ],
   'map_note': '새벽 일출 특별 일정', 'map_start': '아리산역 2,216m', 'map_end': '축산 일출대 2,451m',
   'map_path': 'M110 330 C240 310, 360 260, 470 210 S620 110, 690 70',
   'map_nodes': [(110,330,10),(470,210,8),(690,70,12)],
   'cps': [
     ('아리산역','출발점','badge-trailhead','해발 2,216m','누적 0km','역사·매표소'),
     ('축산역','도착','badge-trailhead','해발 2,451m','열차 약 25분','전망대 방면'),
     ('축산 일출 전망대','명소','badge-landmark','해발 약 2,450m','도보 약 10분','파고라·전망대'),
     ('수진사','사찰','badge-temple','해발 약 2,180m','하산 도보 약 30분','신사·매점'),
     ('아리산역 복귀','종점','badge-trailhead','해발 2,216m','지선 또는 도보','식당가'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': '고급',
   'name': '대탑산 등반 코스',
   'sub': '소평 → 대탑산 정상 2,663m 왕복 · 약 7.2km · 4~5시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','왕복 거리','약 7.2km') + pill('clock','소요 시간','4~5h') + pill('location','대탑산','2,663m') + pill_meter('난이도',3,'medium') + pill('star','권장 출발','오전 7~8시') + pill('location','입장료','NT$300'),
   'flow': ['소평출발','계단길 순환','대탑산 2,663m','원점 하산'],
   'elev_label': '대탑산 2,663m', 'elev_peak': (740, 44),
   'elev_path': 'M20 180 C170 172, 300 150, 430 116 S600 66, 740 44',
   'desc': '아리산 산맥의 최고봉 대탑산(2,663m)을 목표로 하는 유일한 본격 등반 코스입니다. 소평 출발로 편도 약 3.6km의 계단·토사 길이 이어지며, 정상 전망대에서는 유산·타루코 능선이 한눈에 펼쳐집니다. 거리는 짧지만 고도 상승이 집중되어 체력 관리가 필요합니다.',
   'segs': [
     ('출','소평 → 등산로 입구','약 0.5km','15~20분','소평공원 옆 등산로 입구에서 시작합니다. 오전 7~8시 출발이 안전하며, 오후에는 안개와 뇌우가 잦습니다.','12','tip','출발 전 소평 매점에서 물을 보충하세요. 등산로 중간에는 보급이 없습니다.'),
     ('1','입구 → 능선 갈림길','약 1.8km','1~1.5시간','계단과 토사 길이 교차하며 꾸준히 오릅니다. 숲이 무성해 시야는 제한적입니다.','42','warn','비 온 뒤에는 진흙·미끄럼 구간이 생깁니다. 아이젠보다는 스틱이 유용합니다.'),
     ('2','능선 갈림길 → 정상','약 1.8km','1~1.5시간','나무 뿌리 울퉁불퉁한 능선길을 따라 정상 직전 암반까지 오릅니다. 정상에는 전망대가 있습니다.','80','warn','정상 직전 구간은 바람이 강합니다. 모자·경량 재킷을 꼭 챙기세요.'),
     ('하','정상 → 소평 하산','약 3.6km','1.5~2시간','같은 길로 하산합니다. 계단 하산이라 무릎 부담이 크므로 스틱을 활용합니다.','30','tip','오후 늦게까지 체류하지 말고 하산 마감 시간을 지키세요.'),
   ],
   'tips': [
     ('backpack','준비물',['트레킹화(미끄럼 방지)','스틱·무릎 보호대','물 1.5L 이상','방풍 재킷']),
     ('book','입장',['입장료 NT$300','등반 허가 불필요','하산 마감 시간 확인']),
     ('warning','주의',['오후 안개·뇌우 잦음','계단 하산 무릎 부담','중간 보급 없음']),
   ],
   'map_note': '아리산 최고봉 등반 코스', 'map_start': '소평 출발', 'map_end': '대탑산 2,663m',
   'map_path': 'M100 340 C220 325, 330 290, 440 240 S620 100, 700 56',
   'map_nodes': [(100,340,10),(440,240,8),(700,56,12)],
   'cps': [
     ('소평 등산로 입구','출발점','badge-trailhead','해발 약 2,180m','누적 0km','매점·화장실'),
     ('중간 휴게 지점','휴게','badge-shelter','해발 약 2,350m','누적 약 1.8km','벤치'),
     ('능선 갈림길','분기','badge-trailhead','해발 약 2,500m','누적 약 3.6km','안내판'),
     ('대탑산 직전 암반','정상부','badge-summit','해발 약 2,600m','누적 약 3.4km','로프'),
     ('대탑산 전망대','봉우리','badge-summit','해발 2,663m','누적 약 3.6km','전망대'),
   ],
  },
 ],
 'en': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': 'Beginner',
   'name': 'Giant Tree Trail Loop',
   'sub': 'Sisters Ponds → Giant Tree Trail → Xianglin Sacred Tree · about 3 km · 2–3 hours',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Distance','~3 km') + pill('clock','Time','2–3 h') + pill('location','Elevation','~2,200 m') + pill_meter('Difficulty',2,'medium') + pill('star','Best time','Morning') + pill('location','Entry','NT$300'),
   'flow': ['Visitor Center (Sisters Ponds)','Giant Tree Trail','Xianglin Sacred Tree','Back to start'],
   'elev_label': 'Giant Tree Trail ridge', 'elev_peak': (600, 78),
   'elev_path': 'M20 160 C160 150, 300 128, 440 110 S580 90, 600 78',
   'desc': 'The signature loop covering Alishan\'s essential sights. Start at the twin Sisters Ponds, walk the Giant Tree Trail lined with thousands of cypresses, and admire the millennium-old Xianglin Sacred Tree. Gentle boardwalks and stairs make this an easy walk for beginners.',
   'segs': [
     ('Start','Visitor Center → Sisters Ponds','~0.5 km','20–30 min','Stairs lead from the visitor center down to the two calm ponds of Sisters Ponds — the first highlight, framed by pavilions.','15','tip','Early morning mist over the ponds makes for magical photos.'),
     ('1','Sisters Ponds → Giant Tree Trail','~1.0 km','40–60 min','The Giant Tree Trail begins here, a boardwalk winding among giant cypresses in remarkably fresh air.','55','tip','Follow the signs toward the Xianglin Sacred Tree (thousand-year cypress).'),
     ('2','Giant Tree Trail → Xianglin Sacred Tree','~1.0 km','40–60 min','Pass the ancient Xianglin Sacred Tree and Shenmu Station of the forest railway, continuing toward Zhaoping.','85','warn','This section is stair-heavy — knee braces help on the way down.'),
     ('Return','Zhaoping Park → start','~0.5 km','20–30 min','Walk back through Zhaoping Park\'s cherry tree avenue to the starting point.','30','tip','In spring the park itself becomes a cherry-blossom attraction.'),
   ],
   'tips': [
     ('backpack','Gear',['Comfortable walking shoes','Warm layer (cold mornings)','Water & snacks','Rain shell (mist/drizzle)']),
     ('book','Entry & fees',['Entry NT$300','NT$150 discount with public bus ticket','Branch trains charged separately']),
     ('warning','Cautions',['Mornings often below 10°C','Fog limits visibility','Crowds in peak season']),
   ],
   'map_note': 'Alishan core trail loop', 'map_start': 'Visitor Center · Sisters Ponds', 'map_end': 'Xianglin Sacred Tree',
   'map_path': 'M120 320 C240 300, 340 250, 440 210 S600 150, 660 120',
   'map_nodes': [(120,320,10),(440,210,8),(660,120,12)],
   'cps': [
     ('Visitor Center (Sisters Ponds)','Starting Point','badge-trailhead','~2,150 m','0 km','Restrooms · shops · bus stop'),
     ('Giant Tree Trail','Trail','badge-landmark','~2,180 m','~1.5 km','Boardwalk · signs'),
     ('Xianglin Sacred Tree','Attraction','badge-landmark','~2,200 m','~2.5 km','Millennium cypress'),
     ('Zhaoping Park','Rest','badge-trailhead','~2,180 m','~2.8 km','Cherry avenue · pavilion'),
     ('Back at Visitor Center','End','badge-trailhead','~2,150 m','~3 km','Restaurant row'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': 'Intermediate',
   'name': 'Zhushan Sunrise Train Course',
   'sub': 'Alishan Station → Zhushan Station (~25 min) → sunrise platform → Shouzhen Temple · pre-dawn schedule',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Train one-way','~25 min') + pill('clock','Total plan','3–4 h') + pill('location','Zhushan Station','2,451 m') + pill_meter('Difficulty',2,'medium') + pill('star','Departure','1 h before sunrise') + pill('location','Fare','NT$150'),
   'flow': ['Board at Alishan Station','Zhushan Station 2,451 m','Sunrise platform','Shouzhen Temple · descend'],
   'elev_label': 'Zhushan Station 2,451 m', 'elev_peak': (740, 60),
   'elev_path': 'M20 170 C180 160, 340 130, 500 100 S660 72, 740 60',
   'desc': 'The course for Alishan\'s signature sea-of-clouds sunrise. Before dawn, board the Zhushan line at Alishan Station (about 25 minutes, NT$150) up to Zhushan Station at 2,451 m, and watch the sun rise over the cloud sea from the viewing platform. Add Shouzhen Temple and nature trails on the way back for a half-day plan.',
   'segs': [
     ('Start','Board at Alishan Station','0 km','~1 h before sunrise','Departure times shift daily with sunrise. Confirm the next morning\'s time at the station or online the day before, and buy tickets early.','12','warn','Sunrise train tickets sell out fast in peak season — book ahead or arrive very early.'),
     ('1','Zhushan Station → platform','~0.3 km','10–15 min','A short climb from the station to the viewing platform. It is dark before dawn — bring a headlamp or phone light.','50','tip','Keep your warm layer on until the sun appears; it is near freezing before dawn.'),
     ('2','Sunrise viewing','—','30–60 min','The sun rises over the sea of clouds. Mornings after rain give the best chance of cloud seas.','80','tip','After sunrise, enjoy the silhouette of the Datashan ridge across the valley.'),
     ('Return','Shouzhen Temple · back','~1 km','40–60 min','Walk down from Zhushan visiting Shouzhen Temple, then return to Alishan Station by branch train (Shenmu or Zhaoping line) or on foot.','35','tip','Branch trains (NT$100) save your knees for the rest of the day.'),
   ],
   'tips': [
     ('backpack','Gear',['Warm coat & hat','Headlamp','Hot drink','Cash for train tickets']),
     ('book','Fares',['Zhushan line one-way NT$150','Branch lines one-way NT$100','Entry NT$300 separate']),
     ('warning','Cautions',['Pre-dawn temperature drop','Tickets sell out','No sunrise in fog']),
   ],
   'map_note': 'Pre-dawn sunrise special', 'map_start': 'Alishan Station 2,216 m', 'map_end': 'Zhushan platform 2,451 m',
   'map_path': 'M110 330 C240 310, 360 260, 470 210 S620 110, 690 70',
   'map_nodes': [(110,330,10),(470,210,8),(690,70,12)],
   'cps': [
     ('Alishan Station','Starting Point','badge-trailhead','2,216 m','0 km','Station · ticket office'),
     ('Zhushan Station','Arrival','badge-trailhead','2,451 m','~25 min by train','To the platform'),
     ('Zhushan sunrise platform','Attraction','badge-landmark','~2,450 m','~10 min walk','Pavilion · viewpoint'),
     ('Shouzhen Temple','Temple','badge-temple','~2,180 m','~30 min walk down','Shrine · shop'),
     ('Back at Alishan Station','End','badge-trailhead','2,216 m','Branch train or on foot','Restaurant row'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': 'Advanced',
   'name': 'Datashan Summit Hike',
   'sub': 'Zhaoping → Datashan summit 2,663 m round trip · about 7.2 km · 4–5 hours',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Round trip','~7.2 km') + pill('clock','Time','4–5 h') + pill('location','Datashan','2,663 m') + pill_meter('Difficulty',3,'medium') + pill('star','Start','07:00–08:00') + pill('location','Entry','NT$300'),
   'flow': ['Depart Zhaoping','Stairway climbs','Datashan 2,663 m','Descend to start'],
   'elev_label': 'Datashan 2,663 m', 'elev_peak': (740, 44),
   'elev_path': 'M20 180 C170 172, 300 150, 430 116 S600 66, 740 44',
   'desc': 'The only true summit hike in Alishan, to Datashan (2,663 m), the highest peak of the Alishan Range. From Zhaoping, roughly 3.6 km one way of stairs and dirt paths climb steadily to a summit observation deck with sweeping views over the Yushan and Taro Ridge lines. Short but concentrated ascent — pace yourself.',
   'segs': [
     ('Start','Zhaoping → trailhead','~0.5 km','15–20 min','Start from the trailhead beside Zhaoping Park. A 07:00–08:00 start is safest; fog and afternoon thunderstorms are common.','12','tip','Refill water at the Zhaoping shops — there is no resupply on the trail.'),
     ('1','Trailhead → ridge fork','~1.8 km','1–1.5 h','Stairs alternate with dirt paths climbing steadily through dense forest with limited views.','42','warn','After rain the path turns muddy and slippery — poles help more than crampons here.'),
     ('2','Ridge fork → summit','~1.8 km','1–1.5 h','Follow the uneven root-strewn ridge to the rocky section just below the summit observation deck.','80','warn','Wind picks up near the summit — keep your windbreaker and hat handy.'),
     ('Return','Summit → Zhaoping','~3.6 km','1.5–2 h','Descend the same way. The stairs punish the knees — use trekking poles.','30','tip','Don\'t linger too late; respect the descending deadline.'),
   ],
   'tips': [
     ('backpack','Gear',['Anti-slip hiking shoes','Poles & knee braces','1.5 L+ water','Windproof jacket']),
     ('book','Entry',['Entry NT$300','No climbing permit needed','Check descent deadline']),
     ('warning','Cautions',['Afternoon fog & storms','Stair descent is hard on knees','No resupply on trail']),
   ],
   'map_note': 'Alishan Range summit hike', 'map_start': 'Zhaoping trailhead', 'map_end': 'Datashan 2,663 m',
   'map_path': 'M100 340 C220 325, 330 290, 440 240 S620 100, 700 56',
   'map_nodes': [(100,340,10),(440,240,8),(700,56,12)],
   'cps': [
     ('Zhaoping trailhead','Starting Point','badge-trailhead','~2,180 m','0 km','Shops · restrooms'),
     ('Midway rest point','Rest','badge-shelter','~2,350 m','~1.8 km','Bench'),
     ('Ridge fork','Junction','badge-trailhead','~2,500 m','~3.6 km','Signpost'),
     ('Rocky section below summit','Summit push','badge-summit','~2,600 m','~3.4 km','Rope handrail'),
     ('Datashan observation deck','Summit','badge-summit','2,663 m','~3.6 km','Viewing deck'),
   ],
  },
 ],
}

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'ko'
    html = build(which)
    out = pathlib.Path('alishan-playbook.html') if which == 'ko' else pathlib.Path('en/alishan-playbook.html')
    out.write_text(html, encoding='utf-8')
    print(f'wrote {out} ({len(html.splitlines())} lines)')
