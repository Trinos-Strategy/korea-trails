#!/usr/bin/env python3
"""라위니(인도네시아) + 푼힐(네팔) 플레이북 빌더.

사실 게이트 (2026-09 세션 2소스 검증):
- 라위니: 2025-11-03부터 입장료 개편(외국인 1일 20~25만동), 가이드 필수(솔로 금지),
  외국인 일 240명 한정, 운행 4~12월(1~3월 폐쇄): rinjanitrekkingplanner ×
  rinjaniindonesia × rinjanidawnadventures 교차.
- 푼힐: ACAP 허가 필수(약 3,000루피), 2023-04부터 가이드 의무(솔로 금지),
  4~5일 고레파니 티하우스 트레킹, 시즌 3~5월·10~11월: havenholidaysnepal ×
  공식 허가 안내 교차.
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
    t = t.replace('../../assets/img/', '../assets/img/')
    return t

# ═══ 라위니 ═══
RINJANI = {
 'ko': {
  'title': '라위니 등산 플레이북',
  'meta': '인도네시아 롬복 라위니(3,726m) 가이드. 초급 크레이터 림 트레킹, 중급 2일 1박 정상 등반, 고급 호수 종주 코스의 상세 경로, 실사 지도 및 팁을 제공합니다.',
  'h1_card': '라위니',
  'p_card': 'Rinjani · 롬복의 화산 신 3,726m · 세가라아나크 호수',
  'hero_alt': '라위니 화산의 크레이터 호수와 웅장한 산맥',
  'badge': '라위니 플레이북',
  'h1': '라위니 등산 플레이북',
  'hero_desc': '인도네시아 제2의 화산 라위니(3,726m) 가이드. 크레이터 호수 세가라아나크와 새벽 정상 등반까지 — 허가·가이드 제도를 반영한 상세 경로와 팁을 제공합니다.',
  'btn1': '초급: 센나루 림 트레킹', 'btn2': '중급: 2일 1박 정상 등반', 'btn3': '고급: 호수 종주 코스',
  'hero_photographer': 'Fahrul Razi', 'hero_url': 'https://unsplash.com/photos/OYDPdqZdJY4',
  'gal_title': '라위니의 사계 &amp; 명소',
  'lb_zoom': '크게 보기',
  'gallery': [
   ('g1', '라위니 산맥 전경', "Photo by &lt;a href='https://unsplash.com/photos/4CHdH9cMr0E' target='_blank' rel='noopener'&gt;Aaron Thomas&lt;/a&gt; on Unsplash"),
   ('g2', '암반 능선 등반', "Photo by &lt;a href='https://unsplash.com/photos/1mFzrUgTic8' target='_blank' rel='noopener'&gt;Al ghazali&lt;/a&gt; on Unsplash"),
   ('g3', '운에 가려진 화산', "Photo by &lt;a href='https://unsplash.com/photos/pFBtd8_ynTY' target='_blank' rel='noopener'&gt;Fahrul Razi&lt;/a&gt; on Unsplash"),
   ('g4', '롬복 논과 화산', "Photo by &lt;a href='https://unsplash.com/photos/Qq0Coemj0Ng' target='_blank' rel='noopener'&gt;Maximus Beaumont&lt;/a&gt; on Unsplash"),
  ],
 },
 'en': {
  'title': 'Mount Rinjani Playbook',
  'meta': 'Guide to Mount Rinjani (3,726 m) on Lombok, Indonesia. Detailed routes, real maps and tips for the Senaru crater-rim trek, the 2-day summit climb, and the lake traverse.',
  'h1_card': 'Mount Rinjani',
  'p_card': 'Rinjani · Volcano god of Lombok 3,726 m · Segara Anak lake',
  'hero_alt': 'Rinjani\'s crater lake and mighty ridgelines',
  'badge': 'Mount Rinjani Playbook',
  'h1': 'Mount Rinjani Playbook',
  'hero_desc': 'A guide to Indonesia\'s second-highest volcano, Rinjani (3,726 m) — the Segara Anak crater lake, a pre-dawn summit push, and the permits and guide rules that shape the trek.',
  'btn1': 'Beginner: Senaru Rim Trek', 'btn2': 'Intermediate: 2-Day Summit Climb', 'btn3': 'Advanced: Lake Traverse',
  'hero_photographer': 'Fahrul Razi', 'hero_url': 'https://unsplash.com/photos/OYDPdqZdJY4',
  'gal_title': 'Rinjani Four Seasons &amp; Attractions',
  'lb_zoom': 'View larger',
  'gallery': [
   ('g1', 'Rinjani range panorama', "Photo by &lt;a href='https://unsplash.com/photos/4CHdH9cMr0E' target='_blank' rel='noopener'&gt;Aaron Thomas&lt;/a&gt; on Unsplash"),
   ('g2', 'Rocky ridge scramble', "Photo by &lt;a href='https://unsplash.com/photos/1mFzrUgTic8' target='_blank' rel='noopener'&gt;Al ghazali&lt;/a&gt; on Unsplash"),
   ('g3', 'Volcano in the clouds', "Photo by &lt;a href='https://unsplash.com/photos/pFBtd8_ynTY' target='_blank' rel='noopener'&gt;Fahrul Razi&lt;/a&gt; on Unsplash"),
   ('g4', 'Lombok rice fields & volcano', "Photo by &lt;a href='https://unsplash.com/photos/Qq0Coemj0Ng' target='_blank' rel='noopener'&gt;Maximus Beaumont&lt;/a&gt; on Unsplash"),
  ],
 },
}
RINJANI_COURSES = {
 'ko': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': '초급',
   'name': '센나루 크레이터 림 트레킹',
   'sub': '센나루 → 림 2,641m 왕복 2일 · 약 12km · 야영 1박',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','왕복 거리','약 12km') + pill('clock','일정','2일 1박') + pill('location','림','2,641m') + pill_meter('난이도',3,'medium') + pill('star','가이드','필수') + pill('location','기점','센나루'),
   'flow': ['센나루 게이트','정글 오르막','림 2,641m 야영','하산'],
   'elev_label': '림 2,641m', 'elev_peak': (700, 56),
   'elev_path': 'M20 178 C170 170, 320 142, 470 108 S640 70, 700 56',
   'desc': '세가라아나크 호수와 정상을 내려다보는 크레이터 림(2,641m)까지 오르는 2일 트레킹입니다. 정상 등반보다 완만하지만 고도 상승이 집중되어 체력 관리가 필요하며, 가이드 동반이 의무입니다.',
   'segs': [
     ('1일차','센나루 게이트 → 포지 3','약 6km','5~6시간','열대우림 계단길을 오르며 포지 1~3 휴게지를 거칩니다. 캠프는 림 직하에 설치됩니다.','60','tip','오전 출발로 오후 비를 피하세요. 우기 외 시즌이 안전합니다.'),
     ('1일차 밤','림 야영','—','—','림에서 호수와 정상의 야경을 감상합니다. 밤 기온이 낮습니다.','—','warn','바람이 강하므로 텐트 고정과 보온을 철저히 하세요.'),
     ('2일차','림 → 센나루 하산','약 6km','4~5시간','같은 길로 하산합니다. 내리막 계단이 많아 무릎 보호대가 유용합니다.','30','tip','하산 후 센나루 마을에서 온천으로 회복할 수 있습니다.'),
   ],
   'tips': [
     ('backpack','준비물',['수면배깅','방풍 겉옷','헤드랜턴','우비']),
     ('book','허가·가이드',['입장료 1일 약 20~25만동(외국인)','가이드 동반 의무(솔로 금지)','투어 약 $130~285']),
     ('warning','주의',['1~3월 폐쇄(우기)','림 강풍','거머리·미끄럼']),
   ],
   'map_note': '센나루 림 입문 트레킹', 'map_start': '센나루 게이트', 'map_end': '림 2,641m',
   'map_path': 'M110 335 C240 318, 350 270, 460 215 S620 100, 695 58',
   'map_nodes': [(110,335,10),(460,215,8),(695,58,12)],
   'cps': [
     ('센나루 게이트','출발점','badge-trailhead','해발 약 600m','1일차 0km','허가 확인소'),
     ('포지 1~3','휴게','badge-shelter','해발 약 1,500m','1일차 중간','쉼터'),
     ('림 2,641m','야영','badge-summit','해발 2,641m','1일차 약 6km','캠프·전망'),
     ('하산 시작','하산','badge-trailhead','해발 2,641m','2일차 0km','—'),
     ('센나루 복귀','종점','badge-trailhead','해발 약 600m','2일차 약 6km','마을·온천'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': '중급',
   'name': '2일 1박 정상 등반',
   'sub': '셈발룬 → 림 1박 → 새벽 정상 3,726m → 하산 · 약 22km',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','총 거리','약 22km') + pill('clock','일정','2일 1박') + pill('location','정상','3,726m') + pill_meter('난이도',4,'hard') + pill('star','가이드','필수') + pill('location','기점','셈발룬'),
   'flow': ['셈발룬 게이트','림 1박','새벽 정상 3,726m','하산'],
   'elev_label': '정상 3,726m', 'elev_peak': (740, 40),
   'elev_path': 'M20 190 C170 182, 320 155, 470 118 S640 60, 740 40',
   'desc': '라위니의 표준 정상 등반 코스입니다. 첫날 셈발룬(동쪽)에서 림까지 오르고 1박, 둘째 날 새벽 3시에 화산 잔설 사면을 오라 정상(3,726m)에 서고 세가라아나크 호수의 일출을 맞이합니다. 가파른 화산 자갈 사면이라 하산 발걸림이 많습니다.',
   'segs': [
     ('1일차','셈발룬 게이트 → 림','약 8km','6~8시간','사바나 초원과 화산 자갈 사면을 오릅니다. 림(약 2,800m)에서 1박합니다.','60','warn','오후 강풍이 강합니다. 텐트를 돌바람에 겹치게 치세요.'),
     ('1일차 밤','림 1박','—','—','새벽 등반에 대비해 20~21시 취침이 표준입니다.','—','tip','정상 등반 짐은 가볍게 다시 꾸리세요.'),
     ('2일차','새벽 정상 등반','약 3km','2.5~3.5시간','새벽 3시경 화산 자갈 사면(2걸음 오르면 1걸음 미끄러짐)을 오라 정상에 섭니다. 세가라아나크 호수의 일출이 압권입니다.','92','warn','하산이 더 위험합니다. 자갈에 미끄러지지 않게 발끝으로 딛습니다.'),
     ('2일차','셈발룬 하산','약 8km','4~5시간','같은 길로 내려옵니다. 무릎 보호대가 사실상 필수입니다.','30','tip','하산 후 셈발룬 마을에서 도착 식사를 제공하는 투어가 많습니다.'),
   ],
   'tips': [
     ('backpack','준비물',['수면배깅(5°C 이하)','방한 재킷·장갑','헤드랜턴','마스크(화산 먼지)']),
     ('book','허가·예약',['외국인 일 240명 한정','가이드 필수·투어 $130~285','성수기 몇 주 전 예약']),
     ('warning','주의',['1~3월 폐쇄','자갈 사면 하산 위험','림 강풍']),
   ],
   'map_note': '셈발룬 표준 정상 등반', 'map_start': '셈발룬 게이트', 'map_end': '정상 3,726m',
   'map_path': 'M95 345 C210 332, 320 300, 430 255 S630 90, 705 50',
   'map_nodes': [(95,345,10),(430,255,8),(705,50,12)],
   'cps': [
     ('셈발룬 게이트','출발점','badge-trailhead','해발 약 1,150m','1일차 0km','허가 확인소'),
     ('포지 휴게지','휴게','badge-shelter','해발 약 2,000m','1일차 중간','쉼터'),
     ('림 캠프','야영','badge-summit','해발 약 2,800m','1일차 약 8km','캠프·전망'),
     ('정상 3,726m','봉우리','badge-summit','해발 3,726m','2일차 새벽','호수 일출'),
     ('셈발룬 복귀','종점','badge-trailhead','해발 약 1,150m','2일차 하산','마을'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': '고급',
   'name': '호수 종주 코스',
   'sub': '센나루 → 림 → 세가라아나크 호수 → 정상 → 셈발룬 3~4일',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','총 거리','약 30km+') + pill('clock','일정','3~4일') + pill('location','정상','3,726m') + pill_meter('난이도',5,'hard') + pill('star','구성','호수+정상') + pill('location','형태','가이드+포터'),
   'flow': ['센나루→림','호수 하강','정상 등반','셈발룬 하산'],
   'elev_label': '정상 3,726m', 'elev_peak': (740, 42),
   'elev_path': 'M20 192 C170 185, 300 165, 440 130 S620 66, 740 42',
   'desc': '라위니의 모든 것을 담는 최종 코스입니다. 센나루에서 림을 거쳐 세가라아나크 화산호수로 내려가 온천에 들어가고, 셈발룬 쪽에서 새벽 정상 등반을 마친 뒤 종주합니다. 3~4일 일정에 가이드·포터가 필수입니다.',
   'segs': [
     ('1일차','센나루 → 림','약 6km','5~6시간','초급 코스와 동일하게 림까지 오릅니다. 야영합니다.','25','tip','림에서 호수로 내려가는 길이 가파르니 여유 있게 도착하세요.'),
     ('2일차','림 → 세가라아나크 호수','약 2km','2~3시간','급경사 사면을 내려가 화산호수와 온천에 도착합니다. 호숫가 캠프에서 1박합니다.','50','warn','하강 사면이 가파르고 미끄럽습니다. 서두르지 마세요.'),
     ('3일차','호수 → 셈발룬 림','약 5km','5~6시간','호수를 떠나 셈발룬 쪽 림으로 급상승합니다. 이 일정의 가장 힘든 구간입니다.','75','warn','고도 상승이 집중됩니다. 수분·전해질을 충분히 보충하세요.'),
     ('4일차','새벽 정상 → 셈발룬 하산','약 11km','7~9시간','새벽 정상 등반 후 셈발룬으로 긴 하산을 마칩니다.','95','warn','종주 마지막 날은 체력 안배가 생명입니다. 출발 시각을 엄수하세요.'),
   ],
   'tips': [
     ('backpack','준비물',['수면배깅','4일분 의류·행동식','구급 키트','마스크(화산 먼지)']),
     ('book','투어',['3~4일 패키지 권장','가이드·포터·식사 포함','시즌 초 예약 권장']),
     ('warning','주의',['연속 고도 변화','호수 하강 사면','화산 가스 확인']),
   ],
   'map_note': '호수·정상 완전 종주', 'map_start': '센나루', 'map_end': '셈발룬',
   'map_path': 'M85 350 C200 340, 310 310, 420 262 S620 100, 700 52',
   'map_nodes': [(85,350,10),(430,260,8),(700,52,12)],
   'cps': [
     ('센나루 게이트','출발점','badge-trailhead','해발 약 600m','1일차 0km','허가 확인소'),
     ('센나루 림','야영','badge-summit','해발 2,641m','1일차 약 6km','캠프'),
     ('세가라아나크 호수','명소','badge-landmark','해발 약 2,000m','2일차','온천·캠프'),
     ('정상 3,726m','봉우리','badge-summit','해발 3,726m','4일차 새벽','호수 일출'),
     ('셈발룬 게이트','종점','badge-trailhead','해발 약 1,150m','4일차 하산','마을'),
   ],
  },
 ],
 'en': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': 'Beginner',
   'name': 'Senaru Crater Rim Trek',
   'sub': 'Senaru → rim 2,641 m round trip · 2 days · about 12 km · 1 camp night',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Round trip','~12 km') + pill('clock','Duration','2 days 1 night') + pill('location','Rim','2,641 m') + pill_meter('Difficulty',3,'medium') + pill('star','Guide','Mandatory') + pill('location','Base','Senaru'),
   'flow': ['Senaru gate','Jungle climb','Rim 2,641 m camp','Descend'],
   'elev_label': 'Rim 2,641 m', 'elev_peak': (700, 56),
   'elev_path': 'M20 178 C170 170, 320 142, 470 108 S640 70, 700 56',
   'desc': 'A 2-day trek to the crater rim (2,641 m) overlooking Segara Anak lake and the summit. Gentler than the summit push but with concentrated altitude gain — a mandatory guide applies.',
   'segs': [
     ('Day 1','Senaru gate → Pos 3','~6 km','5–6 h','Climb rainforest stairs past rest points Pos 1–3; camp is set just below the rim.','60','tip','Start in the morning to avoid afternoon rain. Outside the rainy season is safest.'),
     ('Day 1 night','Rim camp','—','—','Watch the lake and summit under the stars. Nights are cold.','—','warn','Wind is strong on the rim — stake tents firmly and insulate well.'),
     ('Day 2','Rim → Senaru descent','~6 km','4–5 h','Descend the same way; many stairs make knee braces useful.','30','tip','Recover in the hot springs at Senaru village afterwards.'),
   ],
   'tips': [
     ('backpack','Gear',['Sleeping bag','Windproof layer','Headlamp','Rain shell']),
     ('book','Permits & guide',['Entry ~IDR 200–250k/day (foreigners)','Guide mandatory (no solo)','Tours ~$130–285']),
     ('warning','Cautions',['Closed Jan–Mar (rainy season)','Rim winds','Leeches & slippery trails']),
   ],
   'map_note': 'Senaru rim entry trek', 'map_start': 'Senaru gate', 'map_end': 'Rim 2,641 m',
   'map_path': 'M110 335 C240 318, 350 270, 460 215 S620 100, 695 58',
   'map_nodes': [(110,335,10),(460,215,8),(695,58,12)],
   'cps': [
     ('Senaru gate','Starting Point','badge-trailhead','~600 m','Day 1 · 0 km','Permit check'),
     ('Pos 1–3','Rest','badge-shelter','~1,500 m','Mid Day 1','Shelters'),
     ('Rim 2,641 m','Camp','badge-summit','2,641 m','~6 km','Camp · views'),
     ('Descent start','Descent','badge-trailhead','2,641 m','Day 2 · 0 km','—'),
     ('Back at Senaru','End','badge-trailhead','~600 m','~6 km','Village · hot springs'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': 'Intermediate',
   'name': '2-Day Summit Climb',
   'sub': 'Sembalun → rim overnight → dawn summit 3,726 m → descend · about 22 km',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Total distance','~22 km') + pill('clock','Duration','2 days 1 night') + pill('location','Summit','3,726 m') + pill_meter('Difficulty',4,'hard') + pill('star','Guide','Mandatory') + pill('location','Base','Sembalun'),
   'flow': ['Sembalun gate','Rim overnight','Dawn summit 3,726 m','Descend'],
   'elev_label': 'Summit 3,726 m', 'elev_peak': (740, 40),
   'elev_path': 'M20 190 C170 182, 320 155, 470 118 S640 60, 740 40',
   'desc': 'Rinjani\'s standard summit course. Day 1 climbs from Sembalun (east) to the rim for the night; Day 2 sets off at 03:00 up the volcanic scree to the summit (3,726 m) for sunrise over Segara Anak. The steep scree makes the descent treacherous.',
   'segs': [
     ('Day 1','Sembalun gate → rim','~8 km','6–8 h','Climb savanna and volcanic scree to the rim (~2,800 m) for the night.','60','warn','Afternoon winds are strong — pitch tents sheltered from crosswind.'),
     ('Day 1 night','Rim overnight','—','—','The standard is lights-out at 19:00–20:00 before the dawn push.','—','tip','Repack a light pack for the summit push.'),
     ('Day 2','Dawn summit push','~3 km','2.5–3.5 h','From 03:00 climb the scree ("two steps up, one slide back") to the summit — sunrise over Segara Anak is spectacular.','92','warn','The descent is riskier — step toe-first and control the scree.'),
     ('Day 2','Sembalun descent','~8 km','4–5 h','Return the same way; knee braces are practically mandatory.','30','tip','Many tours include a post-trek meal at Sembalun village.'),
   ],
   'tips': [
     ('backpack','Gear',['Sleeping bag (sub-5°C)','Insulated jacket & gloves','Headlamp','Dust mask (volcanic ash)']),
     ('book','Permits & booking',['240 international trekkers/day cap','Guide mandatory · tours $130–285','Book weeks ahead in season']),
     ('warning','Cautions',['Closed Jan–Mar','Scree descent hazard','Rim winds']),
   ],
   'map_note': 'Standard Sembalun summit course', 'map_start': 'Sembalun gate', 'map_end': 'Summit 3,726 m',
   'map_path': 'M95 345 C210 332, 320 300, 430 255 S630 90, 705 50',
   'map_nodes': [(95,345,10),(430,255,8),(705,50,12)],
   'cps': [
     ('Sembalun gate','Starting Point','badge-trailhead','~1,150 m','Day 1 · 0 km','Permit check'),
     ('Pos rest points','Rest','badge-shelter','~2,000 m','Mid Day 1','Shelters'),
     ('Rim camp','Camp','badge-summit','~2,800 m','~8 km','Camp · views'),
     ('Summit 3,726 m','Summit','badge-summit','3,726 m','Day 2 dawn','Lake sunrise'),
     ('Back at Sembalun','End','badge-trailhead','~1,150 m','Day 2 descent','Village'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': 'Advanced',
   'name': 'Lake Traverse Course',
   'sub': 'Senaru → rim → Segara Anak lake → summit → Sembalun · 3–4 days',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Total distance','~30 km+') + pill('clock','Duration','3–4 days') + pill('location','Summit','3,726 m') + pill_meter('Difficulty',5,'hard') + pill('star','Format','Lake + summit') + pill('location','Support','Guide + porter'),
   'flow': ['Senaru → rim','Descend to lake','Summit climb','Sembalun descent'],
   'elev_label': 'Summit 3,726 m', 'elev_peak': (740, 42),
   'elev_path': 'M20 192 C170 185, 300 165, 440 130 S620 66, 740 42',
   'desc': 'The complete Rinjani experience: descend from the Senaru rim to the Segara Anak crater lake and its hot springs, then climb the Sembalun side for a dawn summit before traversing out. 3–4 days with guide and porter mandatory.',
   'segs': [
     ('Day 1','Senaru → rim','~6 km','5–6 h','Climb to the rim as on the beginner course; camp overnight.','25','tip','Arrive with time to spare — the lake descent is steep.'),
     ('Day 2','Rim → Segara Anak lake','~2 km','2–3 h','Descend the steep slope to the crater lake and hot springs; camp by the lake.','50','warn','The descent is steep and slippery — take it slowly.'),
     ('Day 3','Lake → Sembalun rim','~5 km','5–6 h','Big climb out of the lake to the Sembalun-side rim — the hardest section of the traverse.','75','warn','Concentrated altitude gain — hydrate and replace electrolytes.'),
     ('Day 4','Dawn summit → Sembalun descent','~11 km','7–9 h','Dawn summit push followed by the long descent to Sembalun.','95','warn','Energy management is everything on the final day — respect start times.'),
   ],
   'tips': [
     ('backpack','Gear',['Sleeping bag','4 days of clothing & trail food','First-aid kit','Dust mask (volcanic ash)']),
     ('book','Tour',['3–4 day packages recommended','Guide, porter, meals included','Book early in the season']),
     ('warning','Cautions',['Continuous altitude swings','Lake descent slope','Check volcanic gas notices']),
   ],
   'map_note': 'Full lake & summit traverse', 'map_start': 'Senaru', 'map_end': 'Sembalun',
   'map_path': 'M85 350 C200 340, 310 310, 420 262 S620 100, 700 52',
   'map_nodes': [(85,350,10),(430,260,8),(700,52,12)],
   'cps': [
     ('Senaru gate','Starting Point','badge-trailhead','~600 m','Day 1 · 0 km','Permit check'),
     ('Senaru rim','Camp','badge-summit','2,641 m','Day 1 · ~6 km','Camp'),
     ('Segara Anak lake','Attraction','badge-landmark','~2,000 m','Day 2','Hot springs · camp'),
     ('Summit 3,726 m','Summit','badge-summit','3,726 m','Day 4 dawn','Lake sunrise'),
     ('Sembalun gate','End','badge-trailhead','~1,150 m','Day 4 descent','Village'),
   ],
  },
 ],
}

# ═══ 푼힐 ═══
POONHILL = {
 'ko': {
  'title': '푼힐 트레킹 플레이북',
  'meta': '네팔 아나푸르나 푼힐(3,210m) 트레킹 가이드. 초급 사라앙곳 전망, 중급 4~5일 고레파니 티하우스 트레킹, 고급 ABC 연장 코스의 상세 경로, 실사 지도 및 팁을 제공합니다.',
  'h1_card': '푼힐',
  'p_card': 'Poon Hill · 아나푸르나 전망대 3,210m · 티하우스 트레킹',
  'hero_alt': '구름 위로 솟은 아나푸르나 산맥의 눈 덮인 봉우리들',
  'badge': '푼힐 플레이북',
  'h1': '푼힐 트레킹 플레이북',
  'hero_desc': '네팔 입문 트레킹의 정석, 푼힐(3,210m) 가이드. 아나푸르나·다울라기리 일출 전망대까지 티하우스 트레킹의 허가·경로·팁을 정리했습니다.',
  'btn1': '초급: 사라앙곳 전망', 'btn2': '중급: 4~5일 푼힐 트레킹', 'btn3': '고급: ABC 연장 코스',
  'hero_photographer': 'Daniel Leone', 'hero_url': 'https://unsplash.com/photos/g30P1zcOzXo',
  'gal_title': '푼힐의 사계 &amp; 명소',
  'lb_zoom': '크게 보기',
  'gallery': [
   ('g1', '눈 덮인 아나푸르나 능선', "Photo by &lt;a href='https://unsplash.com/photos/8NOpqulKiQw' target='_blank' rel='noopener'&gt;titas gurung&lt;/a&gt; on Unsplash"),
   ('g2', '초원 위 등반객', "Photo by &lt;a href='https://unsplash.com/photos/tPfOcBOx2wI' target='_blank' rel='noopener'&gt;Anja Lee Ming Becker&lt;/a&gt; on Unsplash"),
   ('g3', '산을 등진 티하우스', "Photo by &lt;a href='https://unsplash.com/photos/HLi1PjkCEdQ' target='_blank' rel='noopener'&gt;Shrish Shrestha&lt;/a&gt; on Unsplash"),
   ('g4', '운해 너머 봉우리', "Photo by &lt;a href='https://unsplash.com/photos/C3YrTbvNcho' target='_blank' rel='noopener'&gt;Sudip Shrestha&lt;/a&gt; on Unsplash"),
  ],
 },
 'en': {
  'title': 'Poon Hill Trekking Playbook',
  'meta': 'Guide to the Poon Hill (3,210 m) trek in the Annapurnas, Nepal. Detailed routes, real maps and tips for the Sarangkot viewpoint, the 4–5 day Ghorepani teahouse trek, and the ABC extension.',
  'h1_card': 'Poon Hill',
  'p_card': 'Poon Hill · Annapurna viewpoint 3,210 m · Teahouse trek',
  'hero_alt': 'Snow-capped peaks of the Annapurna range rising above clouds',
  'badge': 'Poon Hill Playbook',
  'h1': 'Poon Hill Trekking Playbook',
  'hero_desc': 'The classic introductory Nepal trek to Poon Hill (3,210 m) — permits, teahouse routes, and tips for the sunrise viewpoint over the Annapurna and Dhaulagiri ranges.',
  'btn1': 'Beginner: Sarangkot Viewpoint', 'btn2': 'Intermediate: 4–5 Day Poon Hill Trek', 'btn3': 'Advanced: ABC Extension',
  'hero_photographer': 'Daniel Leone', 'hero_url': 'https://unsplash.com/photos/g30P1zcOzXo',
  'gal_title': 'Poon Hill Four Seasons &amp; Attractions',
  'lb_zoom': 'View larger',
  'gallery': [
   ('g1', 'Snowy Annapurna ridgeline', "Photo by &lt;a href='https://unsplash.com/photos/8NOpqulKiQw' target='_blank' rel='noopener'&gt;titas gurung&lt;/a&gt; on Unsplash"),
   ('g2', 'Hikers on the meadow', "Photo by &lt;a href='https://unsplash.com/photos/tPfOcBOx2wI' target='_blank' rel='noopener'&gt;Anja Lee Ming Becker&lt;/a&gt; on Unsplash"),
   ('g3', 'Teahouse below the peaks', "Photo by &lt;a href='https://unsplash.com/photos/HLi1PjkCEdQ' target='_blank' rel='noopener'&gt;Shrish Shrestha&lt;/a&gt; on Unsplash"),
   ('g4', 'Peaks beyond the clouds', "Photo by &lt;a href='https://unsplash.com/photos/C3YrTbvNcho' target='_blank' rel='noopener'&gt;Sudip Shrestha&lt;/a&gt; on Unsplash"),
  ],
 },
}
POONHILL_COURSES = {
 'ko': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': '초급',
   'name': '사라앙곳 전망 트레일',
   'sub': '포카라 → 사라앙곳 1,592m 왕복 · 약 6km · 3~4시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','왕복 거리','약 6km') + pill('clock','소요 시간','3~4h') + pill('location','사라앙곳','1,592m') + pill_meter('난이도',1,'medium') + pill('star','추천 시간','일출·일몰') + pill('location','기점','포카라'),
   'flow': ['포카라 출발','계단·마을길','사라앙곳 전망대','원점'],
   'elev_label': '사라앙곳 1,592m', 'elev_peak': (660, 88),
   'elev_path': 'M20 148 C160 142, 300 122, 450 104 S580 94, 660 88',
   'desc': '푼힐 트레킹 전에 네팔 히말라야 전망을 맛보는 포카라 인근 코스입니다. 사라앙곳(1,592m) 전망대에서 아나푸르나 남벽과 마차푸차레의 일출·일몰을 감상합니다. 완만한 산길이라 누구나 가능합니다.',
   'segs': [
     ('출','포카라 → 트레일 입구','약 1km','20분','포카라 레이크사이드에서 차량 또는 도보로 트레일 입구까지 이동합니다.','15','tip','일출을 보려면 새벽 4시 30분경 출발이 필요합니다.'),
     ('1','계단길 → 사라앙곳','약 2km','1~1.5시간','마을과 계단길을 지나 사라앙곳 전망대에 오릅니다.','65','tip','전망대 인근 카페에서 커피를 마시며 일출을 기다릴 수 있습니다.'),
     ('2','전망대 감상','—','30~60분','아나푸르나 남벽·마차푸차레(어린 양 정상)·다울라기리가 펼쳐집니다.','90','tip','10~11월 하늘이 가장 맑습니다.'),
     ('하','원점 복귀','약 2km','1시간','같은 길로 포카라로 돌아옵니다.','30','tip','낮에는 패러글라이딩도 인근에서 즐길 수 있습니다.'),
   ],
   'tips': [
     ('backpack','준비물',['가벼운 방한 겉옷','물·간식','선크림','현금(카페)']),
     ('book','입장',['사라앙곳은 별도 허가 불필요','푼힐 트레킹과는 별개','포카라 시내 기점']),
     ('warning','주의',['아침 기온 낮음','우기 운해','계단 미끄럼']),
   ],
   'map_note': '포카라 근교 전망 코스', 'map_start': '포카라 레이크사이드', 'map_end': '사라앙곳 1,592m',
   'map_path': 'M120 320 C250 305, 360 260, 470 215 S600 165, 660 135',
   'map_nodes': [(120,320,10),(470,215,8),(660,135,12)],
   'cps': [
     ('포카라 레이크사이드','출발점','badge-trailhead','해발 약 820m','누적 0km','카페·숙소'),
     ('계단길 시작','트레일','badge-trailhead','해발 약 1,000m','누적 약 1km','마을'),
     ('사라앙곳 전망대','전망','badge-landmark','해발 1,592m','누적 약 3km','카페·전망대'),
     ('원점 복귀','종점','badge-trailhead','해발 약 820m','왕복 약 6km','레이크사이드'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': '중급',
   'name': '4~5일 고레파니 티하우스 트레킹',
   'sub': '나야풀 → 울레리 → 고레파니 → 푼힐 일출 → 간두룩 → 나야풀 · 약 40km',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','총 거리','약 40km') + pill('clock','일정','4~5일') + pill('location','푼힐','3,210m') + pill_meter('난이도',2,'medium') + pill('star','숙박','티하우스') + pill('location','허가','ACAP 필수'),
   'flow': ['나야풀','울레리','고레파니 2,850m','푼힐 일출 3,210m','간두룩','나야풀'],
   'elev_label': '푼힐 3,210m', 'elev_peak': (500, 60),
   'elev_path': 'M20 160 C140 150, 260 118, 380 85 S460 68, 500 60',
   'desc': '네팔 트레킹의 입문 정석. 4~5일간 티하우스(산장)에 숙박하며 계단 마을과 루돌락 숲을 지나 고레파니에서 1박, 새벽 푼힐(3,210m) 전망대에서 아나푸르나·다울라기리 일출을 맞이합니다. 고산 질환 위험이 낮아 누구나 도전할 수 있습니다.',
   'segs': [
     ('1일차','포카라 → 나야풀 → 틱케드퉁가/울레리','약 8km','4~5시간','포카라에서 차량으로 나야풀까지 이동(약 1.5~2시간) 후 트레킹 시작. 울레리까지 3,000개가 넘는 계단이 이어집니다.','40','warn','울레리 계단은 이 코스 최대 난관입니다. 페이스를 낮게 유지하세요.'),
     ('2일차','울레리 → 고레파니 2,850m','약 8km','5~6시간','루돌락(진달래) 숲을 통과하며 고도를 올립니다. 봄철엔 진달래가 만개합니다.','65','tip','고레파니에서 숙소를 정한 뒤 내일 일출 시각을 확인하세요.'),
     ('3일차','푼힐 일출 3,210m','왕복 약 2km','새벽 1~1.5시간','새벽 어스름에 헤드랜턴을 켜고 푼힐 전망대(3,210m)로 오릅니다. 아나푸르나·다울라기리 일출이 압권입니다.','92','warn','새벽엔 영하권이므로 최상위 보온을 착용하세요.'),
     ('3~4일차','타다파니 → 간두룩','약 12km','6~7시간','숲 능선길로 타다파니를 거쳐 구르응 마을 간두룩으로 이동합니다.','70','tip','간두룩의 구르응 문화 박물관도 볼 만합니다.'),
     ('5일차','간두룩 → 나야풀 → 포카라','약 10km','4~5시간','계곡길로 나야풀까지 하산한 뒤 차량으로 포카라에 복귀합니다.','30','tip','일정을 4일로 줄이려면 간두룩을 생략할 수 있습니다.'),
   ],
   'tips': [
     ('backpack','준비물',['헤드랜턴','방한 겉옷(새벽 한랭)','트레킹 스틱','물 정화 태블릿']),
     ('book','허가·가이드',['ACAP 허가 필수(약 3,000루피)','가이드 동반 의무(2023~)','티하우스 $5~10/박']),
     ('warning','주의',['울레리 계단','새벽 한랭','우기 거머리·비행 지연']),
   ],
   'map_note': '티하우스 표준 트레킹', 'map_start': '나야풀', 'map_end': '푼힐 3,210m',
   'map_path': 'M95 345 C210 332, 320 300, 430 255 S630 100, 700 55',
   'map_nodes': [(95,345,10),(430,255,8),(700,55,12)],
   'cps': [
     ('나야풀','출발점','badge-trailhead','해발 약 1,070m','1일차 0km','허가 확인소'),
     ('울레리','마을','badge-shelter','해발 약 1,950m','1일차 약 8km','티하우스'),
     ('고레파니','마을','badge-shelter','해발 2,850m','2일차 약 8km','티하우스·카페'),
     ('푼힐 전망대','전망','badge-summit','해발 3,210m','3일차 새벽','일출 전망대'),
     ('간두룩','마을','badge-shelter','해발 약 1,940m','4일차','박물관·티하우스'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': '고급',
   'name': 'ABC(아나푸르나 베이스캠프) 연장 코스',
   'sub': '푼힐 트레킹 + ABC 4,130m 연장 · 7~10일 · 약 90km+',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','총 거리','약 90km+') + pill('clock','일정','7~10일') + pill('location','ABC','4,130m') + pill_meter('난이도',4,'hard') + pill('star','숙박','티하우스') + pill('location','허가','ACAP 필수'),
   'flow': ['푼힐 트레킹','추모룽 분기','MBC→ABC 4,130m','지노우 온천 하산'],
   'elev_label': 'ABC 4,130m', 'elev_peak': (740, 42),
   'elev_path': 'M20 190 C170 184, 320 158, 470 120 S640 62, 740 42',
   'desc': '푼힐 트레킹에 아나푸르나 베이스캠프(4,130m)를 연장하는 7~10일 코스입니다. 추모룽에서 분기해 마차푸차레 베이스캠프를 지나 ABC에 도달하며, 3,000m 이상 고도 적응이 본격적으로 필요해집니다. 티하우스 트레킹의 완성형입니다.',
   'segs': [
     ('1~3일차','푼힐 트레킹 구간','약 20km','3일','기존 푼힐 코스로 고레파니·푼힐 일출을 마친 뒤 타다파니로 이동합니다.','30','tip','3일차까지는 중급 코스와 동일합니다.'),
     ('4~5일차','추모룽 → MBC(3,700m)','약 12km','6~7시간','추모룽에서 ABC 방면으로 분기해 히말라야 빙하 계곡을 따라 MBC(마차푸차레 베이스캠프)까지 오릅니다.','60','warn','3,000m를 넘으며 고산 증상이 나타날 수 있습니다. 하루 고도 상승을 관리하세요.'),
     ('6일차','MBC → ABC 4,130m','약 2km','2시간','짧은 이동으로 ABC에 도착합니다. 오후 구름 전 오후경 관람 후 조기 취침합니다.','85','warn','ABC 밤 기온은 영하권입니다. 산소 희박에 대비해 무리한 움직임을 피합니다.'),
     ('7일차','ABC 일출 → 지노우 온천 하산','약 12km','6~7시간','ABC 일출을 감상한 뒤 긴 하산을 시작해 지노우 온천에서 회복합니다.','90','tip','지노우 온천(별도 요금)이 하산 피로 회복에 탁월합니다.'),
     ('8~10일차','지노우 → 나야풀 → 포카라','약 12km','5~6시간','온천 마을에서 나야풀까지 하산 후 포카라로 복귀합니다.','30','tip','비행 지연 대비 여유 일정을 하루 이상 두세요.'),
   ],
   'tips': [
     ('backpack','준비물',['수면배깅(티하우스 담요 보조)','방한 의류 세트','고산 약(아세타졸아미드·상담 후)','정화 태블릿']),
     ('book','허가·가이드',['ACAP 허가 필수','가이드 동반 의무','티하우스 예약은 현장 가능(성수기 사전 권장)']),
     ('warning','주의',['고산 질환(하산이 치료)','동절기 협곡 폐쇄','연결 비행 지연']),
   ],
   'map_note': 'ABC 연장 장거리 트레킹', 'map_start': '나야풀', 'map_end': 'ABC 4,130m',
   'map_path': 'M90 348 C200 336, 310 305, 420 258 S630 95, 705 50',
   'map_nodes': [(90,348,10),(420,258,8),(705,50,12)],
   'cps': [
     ('나야풀','출발점','badge-trailhead','해발 약 1,070m','1일차 0km','허가 확인소'),
     ('고레파니','마을','badge-shelter','해발 2,850m','2일차','티하우스'),
     ('추모룽 분기','분기','badge-trailhead','해발 약 2,170m','4일차','ABC 방면'),
     ('MBC','산장','badge-shelter','해발 3,700m','5일차','티하우스'),
     ('ABC 4,130m','목적지','badge-summit','해발 4,130m','6일차','기지캠프 전망'),
   ],
  },
 ],
 'en': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': 'Beginner',
   'name': 'Sarangkot Viewpoint Trail',
   'sub': 'Pokhara → Sarangkot 1,592 m round trip · about 6 km · 3–4 hours',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Round trip','~6 km') + pill('clock','Time','3–4 h') + pill('location','Sarangkot','1,592 m') + pill_meter('Difficulty',1,'medium') + pill('star','Best time','Sunrise/sunset') + pill('location','Base','Pokhara'),
   'flow': ['Depart Pokhara','Stairs & village paths','Sarangkot viewpoint','Back to start'],
   'elev_label': 'Sarangkot 1,592 m', 'elev_peak': (660, 88),
   'elev_path': 'M20 148 C160 142, 300 122, 450 104 S580 94, 660 88',
   'desc': 'A taste of Himalayan viewpoints near Pokhara before committing to the Poon Hill trek. From Sarangkot (1,592 m) watch sunrise and sunset over the Annapurna south wall and Machhapuchhre. Gentle trails suit anyone.',
   'segs': [
     ('Start','Pokhara → trailhead','~1 km','20 min','Move from Lakeside to the trailhead by vehicle or on foot.','15','tip','For sunrise you must leave around 04:30.'),
     ('1','Stairs → Sarangkot','~2 km','1–1.5 h','Village paths and stairs climb to the Sarangkot viewpoint.','65','tip','Summit-area cafes serve coffee while you wait for the sun.'),
     ('2','Viewing time','—','30–60 min','The Annapurna south wall, Machhapuchhre (Fishtail), and Dhaulagiri spread below.','90','tip','October–November skies are clearest.'),
     ('Return','Back to start','~2 km','1 h','Return the same way to Pokhara.','30','tip','Paragliding is popular nearby in the daytime.'),
   ],
   'tips': [
     ('backpack','Gear',['Light warm layer','Water & snacks','Sunscreen','Cash for cafes']),
     ('book','Entry',['No separate permit needed for Sarangkot','Independent of the Poon Hill trek','Starts from Pokhara town']),
     ('warning','Cautions',['Cold mornings','Monsoon haze','Slippery stairs']),
   ],
   'map_note': 'Pokhara-area viewpoint course', 'map_start': 'Pokhara Lakeside', 'map_end': 'Sarangkot 1,592 m',
   'map_path': 'M120 320 C250 305, 360 260, 470 215 S600 165, 660 135',
   'map_nodes': [(120,320,10),(470,215,8),(660,135,12)],
   'cps': [
     ('Pokhara Lakeside','Starting Point','badge-trailhead','~820 m','0 km','Cafes · lodging'),
     ('Stairs begin','Trail','badge-trailhead','~1,000 m','~1 km','Village'),
     ('Sarangkot viewpoint','Viewpoint','badge-landmark','1,592 m','~3 km','Cafe · decks'),
     ('Back at Lakeside','End','badge-trailhead','~820 m','~6 km round trip','Lakeside'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': 'Intermediate',
   'name': '4–5 Day Ghorepani Teahouse Trek',
   'sub': 'Nayapul → Ulleri → Ghorepani → Poon Hill sunrise → Ghandruk → Nayapul · about 40 km',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Total distance','~40 km') + pill('clock','Duration','4–5 days') + pill('location','Poon Hill','3,210 m') + pill_meter('Difficulty',2,'medium') + pill('star','Lodging','Teahouses') + pill('location','Permit','ACAP required'),
   'flow': ['Nayapul','Ulleri','Ghorepani 2,850 m','Poon Hill sunrise 3,210 m','Ghandruk','Nayapul'],
   'elev_label': 'Poon Hill 3,210 m', 'elev_peak': (500, 60),
   'elev_path': 'M20 160 C140 150, 260 118, 380 85 S460 68, 500 60',
   'desc': 'The classic introductory Nepal trek: 4–5 days sleeping in teahouses, climbing stair-villages and rhododendron forests to Ghorepani, then greeting sunrise over the Annapurna and Dhaulagiri ranges from Poon Hill (3,210 m). Low altitude-sickness risk makes it accessible to most hikers.',
   'segs': [
     ('Day 1','Pokhara → Nayapul → Tikhedhunga/Ulleri','~8 km','4–5 h','Drive to Nayapul (1.5–2 h) and start trekking. More than 3,000 steps lead up to Ulleri.','40','warn','The Ulleri stairs are the hardest part — keep the pace low.'),
     ('Day 2','Ulleri → Ghorepani 2,850 m','~8 km','5–6 h','Gain altitude through rhododendron forest — in full bloom in spring.','65','tip','Confirm tomorrow\'s sunrise time once settled in Ghorepani.'),
     ('Day 3','Poon Hill sunrise 3,210 m','~2 km RT','1–1.5 h before dawn','Headlamp up to the Poon Hill platform (3,210 m) — the Annapurna and Dhaulagiri sunrise is unforgettable.','92','warn','It is below freezing before dawn — wear your warmest layers.'),
     ('Day 3–4','Tadapani → Ghandruk','~12 km','6–7 h','Ridge forest trails lead to Tadapani and down to the Gurung village of Ghandruk.','70','tip','Ghandruk\'s Gurung culture museum is worth a visit.'),
     ('Day 5','Ghandruk → Nayapul → Pokhara','~10 km','4–5 h','Descend the valley to Nayapul and drive back to Pokhara.','30','tip','Skipping Ghandruk compresses the trek to 4 days.'),
   ],
   'tips': [
     ('backpack','Gear',['Headlamp','Warm layers (pre-dawn cold)','Trekking poles','Water purification tablets']),
     ('book','Permits & guide',['ACAP permit required (~NPR 3,000)','Guide mandatory (since 2023)','Teahouses $5–10/night']),
     ('warning','Cautions',['Ulleri stairs','Pre-dawn cold','Monsoon leeches & flight delays']),
   ],
   'map_note': 'Standard teahouse trek', 'map_start': 'Nayapul', 'map_end': 'Poon Hill 3,210 m',
   'map_path': 'M95 345 C210 332, 320 300, 430 255 S630 100, 700 55',
   'map_nodes': [(95,345,10),(430,255,8),(700,55,12)],
   'cps': [
     ('Nayapul','Starting Point','badge-trailhead','~1,070 m','Day 1 · 0 km','Permit check'),
     ('Ulleri','Village','badge-shelter','~1,950 m','Day 1 · ~8 km','Teahouses'),
     ('Ghorepani','Village','badge-shelter','2,850 m','Day 2 · ~8 km','Teahouses · cafes'),
     ('Poon Hill viewpoint','Viewpoint','badge-summit','3,210 m','Day 3 dawn','Sunrise deck'),
     ('Ghandruk','Village','badge-shelter','~1,940 m','Day 4','Museum · teahouses'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': 'Advanced',
   'name': 'ABC (Annapurna Base Camp) Extension',
   'sub': 'Poon Hill trek + ABC 4,130 m extension · 7–10 days · about 90 km+',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Total distance','~90 km+') + pill('clock','Duration','7–10 days') + pill('location','ABC','4,130 m') + pill_meter('Difficulty',4,'hard') + pill('star','Lodging','Teahouses') + pill('location','Permit','ACAP required'),
   'flow': ['Poon Hill trek','Chhomrong fork','MBC → ABC 4,130 m','Jhinu hot springs descent'],
   'elev_label': 'ABC 4,130 m', 'elev_peak': (740, 42),
   'elev_path': 'M20 190 C170 184, 320 158, 470 120 S640 62, 740 42',
   'desc': 'Extend the Poon Hill trek to Annapurna Base Camp (4,130 m) over 7–10 days. From Chhomrong the route branches into the glacial valley past Machhapuchhre Base Camp to ABC — proper acclimatization above 3,000 m becomes essential. The complete teahouse-trekking experience.',
   'segs': [
     ('Days 1–3','Poon Hill section','~20 km','3 days','Walk the standard Poon Hill course through Ghorepani and the sunrise, then move toward Tadapani.','30','tip','Identical to the intermediate course through Day 3.'),
     ('Days 4–5','Chhomrong → MBC (3,700 m)','~12 km','6–7 h','Branch toward ABC at Chhomrong and climb the glacial valley past Machhapuchhre Base Camp.','60','warn','Above 3,000 m altitude symptoms appear — manage daily gain carefully.'),
     ('Day 6','MBC → ABC 4,130 m','~2 km','2 h','A short move to Annapurna Base Camp; view the sanctuary in the afternoon light and sleep early.','85','warn','ABC nights are below freezing — move deliberately in the thin air.'),
     ('Day 7','ABC sunrise → Jhinu hot springs','~12 km','6–7 h','Watch the ABC sunrise, then start the long descent, recovering at Jhinu hot springs.','90','tip','Jhinu hot springs (small fee) are superb for post-trek recovery.'),
     ('Days 8–10','Jhinu → Nayapul → Pokhara','~12 km','5–6 h','Descend from the hot-spring village to Nayapul and drive back to Pokhara.','30','tip','Keep at least one spare day for flight delays.'),
   ],
   'tips': [
     ('backpack','Gear',['Sleeping bag (supplement teahouse blankets)','Full warm set','Altitude meds (consult a doctor)','Purification tablets']),
     ('book','Permits & guide',['ACAP permit required','Guide mandatory','Teahouses bookable on site (reserve in peak season)']),
     ('warning','Cautions',['Altitude sickness (descent is the cure)','Winter canyon closures','Connecting flight delays']),
   ],
   'map_note': 'ABC extension long trek', 'map_start': 'Nayapul', 'map_end': 'ABC 4,130 m',
   'map_path': 'M90 348 C200 336, 310 305, 420 258 S630 95, 705 50',
   'map_nodes': [(90,348,10),(420,258,8),(705,50,12)],
   'cps': [
     ('Nayapul','Starting Point','badge-trailhead','~1,070 m','Day 1 · 0 km','Permit check'),
     ('Ghorepani','Village','badge-shelter','2,850 m','Day 2','Teahouses'),
     ('Chhomrong fork','Junction','badge-trailhead','~2,170 m','Day 4','ABC direction'),
     ('MBC','Hut','badge-shelter','3,700 m','Day 5','Teahouse'),
     ('ABC 4,130 m','Destination','badge-summit','4,130 m','Day 6','Base camp views'),
   ],
  },
 ],
}

CONTENT = {
  'rinjani': RINJANI,
  'poonhill': POONHILL,
}
COURSES = {
  'rinjani': RINJANI_COURSES,
  'poonhill': POONHILL_COURSES,
}

if __name__ == '__main__':
    mountain, lang = sys.argv[1], sys.argv[2]
    html = build(mountain, lang)
    out = pathlib.Path(f'{mountain}-playbook.html') if lang == 'ko' else pathlib.Path(f'en/{mountain}-playbook.html')
    out.write_text(html, encoding='utf-8')
    print(f'wrote {out} ({len(html.splitlines())} lines)')
