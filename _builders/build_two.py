#!/usr/bin/env python3
"""타테야마(일본) + 황산(중국) 플레이북 빌더 — yushan 스켈레톤 변환.

사실 게이트 (2026-09 세션 2소스 검증):
- 타테야마: 알펜루트 공식(alpen-route.com) × Nerd Nomads/Japan Alps Adventures —
  운행 4/15~11/30, 무로도 2,450m, 오야마 3,003m(6월 중순까지 잔설), 무로도산장.
- 황산: chinadiscovery × 인민일보/여유중국 — 입장료 190위안(성수기)/150위안(동절기),
  3일 유효, 케이블카 옥병 90/운곡 80, 연화봉-천도봉 교대 휴면(2025 천도봉 개방·실명예약).
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
    return t

# ═══════════ 타테야마 콘텐츠 ═══════════
TATEYAMA = {
 'ko': {
  'title': '타테야마 등산 플레이북',
  'meta': '일본 북알프스 타테야마 가이드. 초급 무로도 고원 산책, 중급 오야마(3,003m) 등반, 고급 츠루기다케(2,999m) 도전 코스의 상세 경로, 실사 지도 및 팁을 제공합니다.',
  'h1_card': '타테야마',
  'p_card': 'Tateyama · 북알프스의 성산 3,003m · 무로도 2,450m 고원 기점',
  'hero_alt': '타테야마 산맥의 웅장한 능선과 고원 풍경',
  'badge': '타테야마 플레이북',
  'h1': '타테야마 등산 플레이북',
  'hero_desc': '일본 북알프스의 성산 타테야마 가이드. 운행 기간 4월 15일~11월 30일의 알펜루트를 따라 무로도(2,450m)에서 오야마(3,003m) 등반, 그리고 츠루기다케 도전까지의 상세 경로와 팁을 제공합니다.',
  'btn1': '초급: 무로도 고원 산책', 'btn2': '중급: 오야마 등반', 'btn3': '고급: 츠루기다케 도전',
  'hero_photographer': 'Zion C', 'hero_url': 'https://unsplash.com/photos/mIUWj_1zKUM',
  'gal_title': '타테야마의 사계 &amp; 명소',
  'lb_zoom': '크게 보기',
  'gallery': [
   ('g1', '무로도 고원 능선', "Photo by &lt;a href='https://unsplash.com/photos/pm7eXo5vB6o' target='_blank' rel='noopener'&gt;Zion C&lt;/a&gt; on Unsplash"),
   ('g2', '설벽 시즌의 산맥', "Photo by &lt;a href='https://unsplash.com/photos/C-ndB1hDD0M' target='_blank' rel='noopener'&gt;Zhixin LIU&lt;/a&gt; on Unsplash"),
   ('g3', '미쿠리가이켜 호수', "Photo by &lt;a href='https://unsplash.com/photos/zP1gZG-B0lU' target='_blank' rel='noopener'&gt;Zion C&lt;/a&gt; on Unsplash"),
   ('g4', '호수와 안개의 산맥', "Photo by &lt;a href='https://unsplash.com/photos/bTF3D36H-1w' target='_blank' rel='noopener'&gt;Shigeki Hasegawa&lt;/a&gt; on Unsplash"),
  ],
 },
 'en': {
  'title': 'Tateyama Hiking Playbook',
  'meta': 'Guide to Mt. Tateyama in Japan\'s Northern Alps. Detailed routes, real maps and tips for the Murodo plateau walk, the Oyama (3,003 m) climb, and the Tsurugi-dake (2,999 m) challenge.',
  'h1_card': 'Tateyama',
  'p_card': 'Tateyama · Sacred peak of the Northern Alps, 3,003 m · Base at Murodo 2,450 m',
  'hero_alt': 'The majestic ridgelines and highland scenery of the Tateyama range',
  'badge': 'Tateyama Playbook',
  'h1': 'Tateyama Hiking Playbook',
  'hero_desc': 'A guide to the sacred Mt. Tateyama in the Northern Alps. Ride the Alpine Route (open April 15 – November 30) up to Murodo at 2,450 m, climb Oyama (3,003 m), and take on the chained ridges of Tsurugi-dake.',
  'btn1': 'Beginner: Murodo Plateau Walk', 'btn2': 'Intermediate: Oyama Climb', 'btn3': 'Advanced: Tsurugi-dake',
  'hero_photographer': 'Zion C', 'hero_url': 'https://unsplash.com/photos/mIUWj_1zKUM',
  'gal_title': 'Tateyama Four Seasons &amp; Attractions',
  'lb_zoom': 'View larger',
  'gallery': [
   ('g1', 'Murodo plateau ridgeline', "Photo by &lt;a href='https://unsplash.com/photos/pm7eXo5vB6o' target='_blank' rel='noopener'&gt;Zion C&lt;/a&gt; on Unsplash"),
   ('g2', 'Snow-wall season peaks', "Photo by &lt;a href='https://unsplash.com/photos/C-ndB1hDD0M' target='_blank' rel='noopener'&gt;Zhixin LIU&lt;/a&gt; on Unsplash"),
   ('g3', 'Mikurigaike pond', "Photo by &lt;a href='https://unsplash.com/photos/zP1gZG-B0lU' target='_blank' rel='noopener'&gt;Zion C&lt;/a&gt; on Unsplash"),
   ('g4', 'Misty mountains over a lake', "Photo by &lt;a href='https://unsplash.com/photos/bTF3D36H-1w' target='_blank' rel='noopener'&gt;Shigeki Hasegawa&lt;/a&gt; on Unsplash"),
  ],
 },
}

TATEYAMA_COURSES = {
 'ko': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': '초급',
   'name': '무로도 고원 산책 코스',
   'sub': '무로도 → 미쿠리가이켜 → 지고쿠다니 · 약 2km · 1~2시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','거리','약 2km') + pill('clock','소요 시간','1~2h') + pill('location','무로도','2,450m') + pill_meter('난이도',2,'medium') + pill('star','운행 기간','4/15~11/30') + pill('location','기점','알펜루트'),
   'flow': ['무로도 터미널','미쿠리가이켜','지고쿠다니 분화구','원점'],
   'elev_label': '고원 순환 능선', 'elev_peak': (620, 84),
   'elev_path': 'M20 155 C160 150, 300 132, 450 112 S580 94, 620 84',
   'desc': '알펜루트의 최고 지점 무로도(2,450m)에서 고원의 하이라이트를 도는 산책 코스입니다. 화산 활동이 이어지는 지고쿠다니(지옥곡)의 김이 오르는 절경과 청색의 미쿠리가이켜 호수를 감상합니다. 겨울을 제외한 운행 기간이라면 누구나 걷기 좋습니다.',
   'segs': [
     ('출','무로도 터미널 출발','0km','10분','버스·로프웨이가 도착하는 무로도 터미널에서 출발합니다. 해발 2,450m라 평지보다 숨이 찹니다. 천천히 걸으세요.','15','tip','터미널 건물에 화장실·매점·휴게 공간이 있습니다.'),
     ('1','미쿠리가이켜 호수','약 0.8km','30분','고원의 상징인 화산호 미쿠리가이켜. 맑은 날에는 호수에 오야마의 역궁(倒立)이 비칩니다.','50','tip','아침이 잔물결이 없어 가장 아름답습니다.'),
     ('2','지고쿠다니 분기공','약 0.6km','30분','김이 치솟는 화산 분기공 지대입니다. 목도길을 벗어나지 말고 황화수소 가스 경보에 따르세요.','85','warn','분기공 인근은 가스 농도에 따라 통제될 수 있습니다. 안내에 반드시 따릅니다.'),
     ('하','원점 복귀','약 0.6km','20분','고원 둑길을 따라 무로도로 돌아옵니다.','30','tip','여유가 되면 라이초자와 온천(도보 약 20분)의 야외욕까지 추가할 수 있습니다.'),
   ],
   'tips': [
     ('backpack','준비물',['방풍 겉옷(고원 강풍)','선크림·모자','물·간식','현금(시설 이용)']),
     ('book','운행·숙박',['알펜루트 운행 4/15~11/30','무로도산장 예약(공식·야마텐)','성수기 숙박 조기 마감']),
     ('warning','주의',['고산 기후(연중 최저 5°C 내외)','화산 가스 통제','눈 녹기 전 잔설(6월 중순까지)']),
   ],
   'map_note': '무로도 고원 하이라이트 루프', 'map_start': '무로도 터미널', 'map_end': '지고쿠다니',
   'map_path': 'M120 320 C250 300, 360 250, 460 205 S610 140, 670 110',
   'map_nodes': [(120,320,10),(460,205,8),(670,110,12)],
   'cps': [
     ('무로도 터미널','출발점','badge-trailhead','해발 2,450m','누적 0km','터미널·매점·숙소'),
     ('미쿠리가이켜','호수','badge-landmark','해발 약 2,430m','누적 약 0.8km','산장·음수대'),
     ('지고쿠다니 분기공','명소','badge-landmark','해발 약 2,400m','누적 약 1.4km','목도·통제 게이트'),
     ('라이초자와 온천 방면','선택','badge-shelter','해발 약 2,300m','편도 약 20분','야외욕·산장'),
     ('원점(무로도)','종점','badge-trailhead','해발 2,450m','누적 약 2km','식당'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': '중급',
   'name': '오야마 등반 코스',
   'sub': '무로도 → 오야마 산정 3,003m 왕복 · 약 6km · 3~4시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','왕복 거리','약 6km') + pill('clock','소요 시간','3~4h') + pill('location','오야마','3,003m') + pill_meter('난이도',3,'medium') + pill('star','최적 시즌','7월~10월') + pill('location','기점','무로도 2,450m'),
   'flow': ['무로도 출발','일출·일몰 능선','오야마 산정 신사 3,003m','원점 하산'],
   'elev_label': '오야마 3,003m', 'elev_peak': (740, 46),
   'elev_path': 'M20 178 C170 170, 320 140, 470 108 S640 66, 740 46',
   'desc': '타테야마 3봉의 주봉 오야마(雄山, 3,003m)를 목표로 하는 표준 등반 코스입니다. 무로도에서 약 550m를 오르며, 정상에는 오야마 신사가 있어 등산과 신앙이 함께하는 산입니다. 6월 중순까지는 정상부에 잔설이 남아 아이젠이 필요할 수 있습니다.',
   'segs': [
     ('출','무로도 → 등산로 입구','0.3km','10분','무로도산장 뒤편 등산로 입구에서 시작합니다. 오전 출발이 날씨 여유 면에서 안전합니다.','10','tip','알펜루트 측 등산로는 정비가 잘 되어 있지만 고도 차가 큽니다.'),
     ('1','입구 → 중산합(나카노야마)','약 2.4km','1~1.5시간','완만한 암석파티오 길이 이어지며 시야가 점점 열립니다. 중간에 중산합 산장이 있습니다.','45','tip','약한 체력이라 중산합에서 되돌아오는 것도 좋은 선택입니다.'),
     ('2','중산합 → 오야마 산정','약 0.3km','30~40분','사다리와 쇠사슬이 있는 암릉을 오르면 정상의 오야마 신사(3,003m)입니다. 날씨가 좋으면 하쿠바산맥까지 조망됩니다.','85','warn','정상 직전 암릉은 쇠사슬 구간입니다. 장갑이 있으면 유용합니다.'),
     ('하','정상 → 무로도 하산','약 3km','1.5시간','같은 길로 하산합니다. 잔설 시즌(6월 중순까지)에는 아이젠을 착용하세요.','30','warn','6월 중순까지 정상부 잔설이 있습니다. 아이젠과 아이스액스(필요시)를 준비하세요.'),
   ],
   'tips': [
     ('backpack','준비물',['트레킹화','방풍·방한 겉옷','헤드랜턴','장갑(쇠사슬 구간)']),
     ('book','숙박',['무로도산장(무로도)','라이초자와 온천산장','예약은 공식 사이트·야마텐']),
     ('warning','주의',['6월 중순까지 잔설','오후 뇌우·강풍','암릉 쇠사슬 구간']),
   ],
   'map_note': '오야마 표준 등반 루트', 'map_start': '무로도 2,450m', 'map_end': '오야마 3,003m',
   'map_path': 'M110 335 C240 315, 350 265, 460 210 S630 90, 700 55',
   'map_nodes': [(110,335,10),(460,210,8),(700,55,12)],
   'cps': [
     ('무로도 등산로 입구','출발점','badge-trailhead','해발 2,450m','누적 0km','산장·매점'),
     ('중산합(나카노야마)','산장','badge-shelter','해발 약 2,698m','누적 약 2.4km','산장·음수대'),
     ('오야마 산정 신사','봉우리','badge-summit','해발 3,003m','누적 약 3km','신사·전망대'),
     ('하산 중 휴게','휴게','badge-shelter','해발 약 2,700m','하산 1km','벤치'),
     ('무로도 복귀','종점','badge-trailhead','해발 2,450m','왕복 약 6km','터미널'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': '고급',
   'name': '츠루기다케(劍岳) 도전 코스',
   'sub': '무로도 → 검악 2,999m 왕복 · 약 5km · 5~7시간 · 쇠사슬·사다리 구간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','왕복 거리','약 5km') + pill('clock','소요 시간','5~7h') + pill('location','츠루기다케','2,999m') + pill_meter('난이도',5,'hard') + pill('star','최적 시즌','7월~10월 초') + pill('location','난이도','전문가'),
   'flow': ['무로도 출발','쓰루기사와 오르막','쇠사슬·사다리 암릉','검악 2,999m'],
   'elev_label': '츠루기다케 2,999m', 'elev_peak': (740, 40),
   'elev_path': 'M20 185 C170 180, 300 160, 430 128 S620 68, 740 40',
   'desc': '일본에서 가장 험한 암봉으로 불리는 츠루기다케(劍岳, 2,999m) 도전 코스입니다. 쇠사슬·사다리·릿지(철제 디딤판)가 이어지는 본격 암릉 등반으로, 등산 경험이 풍부한 등반가만 고려해야 합니다. 악천후에는 즉시 포기하는 판단이 필수입니다.',
   'segs': [
     ('출','무로도 → 쓰루기사와 분기','약 0.7km','20분','오야마 코스와 갈라지는 쓰루기사와 분기까지 접근합니다. 오전 5~6시 출발이 표준입니다.','8','tip','하산 마감 시간을 역산해 출발 시각을 정하세요. 늦으면 하산이 어두워집니다.'),
     ('1','쓰루기사와 → 검악산장','약 1.3km','1.5~2시간','거친 암설 사면을 오릅니다. 검악산장(정상 직하)이 마지막 보급지입니다.','35','warn','퇴각 판단 지점입니다. 날씨가 나쁘면 여기서 포기합니다.'),
     ('2','검악산장 → 정상','약 0.3km','1~1.5시간','쇠사슬·사다리·릿지가 연속되는 핵심 암릉 구간입니다. 헬멧 착용이 권장됩니다.','88','warn','초보자 절대 금지. 암릉 경험자만 진입하고, 정체 시 역방향을 양보합니다.'),
     ('하','정상 → 무로도 하산','약 2.5km','2~3시간','암릉 하산은 등반보다 사고 위험이 높습니다. 여유를 갖고 내려옵니다.','28','warn','하산 중 쇠사슬 구간에서는 등반과 같은 집중이 필요합니다.'),
   ],
   'tips': [
     ('backpack','준비물',['헬멧·하네스(권장)','등산용 장갑','방풍·방한 의류','헤드랜턴·비상식량']),
     ('book','숙박',['검악산장(정상 직하)','무로도산장(전일 예약)','성수기 몇 달 전 예약']),
     ('warning','주의',['암릉 전문 등반 코스','악천후 즉시 포기','하산 시간 엄수']),
   ],
   'map_note': '일본 최고 난이도 암릉 등반', 'map_start': '무로도 2,450m', 'map_end': '츠루기다케 2,999m',
   'map_path': 'M90 345 C210 330, 320 300, 430 255 S630 95, 705 52',
   'map_nodes': [(90,345,10),(430,255,8),(705,52,12)],
   'cps': [
     ('무로도 출발','출발점','badge-trailhead','해발 2,450m','누적 0km','산장·터미널'),
     ('쓰루기사와 분기','분기','badge-trailhead','해발 약 2,500m','누적 약 0.7km','안내판'),
     ('검악산장','산장','badge-shelter','해발 약 2,930m','누적 약 2km','산장·취사'),
     ('암릉 쇠사슬 구간','핵심','badge-summit','해발 약 2,950m','누적 약 2.3km','쇠사슬·사다리'),
     ('검악 정상','봉우리','badge-summit','해발 2,999m','누적 약 2.5km','삼각점'),
   ],
  },
 ],
 'en': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': 'Beginner',
   'name': 'Murodo Plateau Walk',
   'sub': 'Murodo → Mikurigaike → Jigokudani · about 2 km · 1–2 hours',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Distance','~2 km') + pill('clock','Time','1–2 h') + pill('location','Murodo','2,450 m') + pill_meter('Difficulty',2,'medium') + pill('star','Season','Apr 15–Nov 30') + pill('location','Base','Alpine Route'),
   'flow': ['Murodo terminal','Mikurigaike pond','Jigokudani vents','Back to start'],
   'elev_label': 'Plateau loop ridge', 'elev_peak': (620, 84),
   'elev_path': 'M20 155 C160 150, 300 132, 450 112 S580 94, 620 84',
   'desc': 'A walk covering the highlights of the Murodo plateau (2,450 m), the highest point on the Alpine Route. See the steaming volcanic vents of Jigokudani ("Hell Valley") and the vividly blue crater lake Mikurigaike. Easy walking for anyone during the operating season.',
   'segs': [
     ('Start','Depart Murodo terminal','0 km','10 min','Start from the Murodo terminal where buses and the ropeway arrive. At 2,450 m the air is thin — walk slowly.','15','tip','Restrooms, shops, and lounge space are inside the terminal building.'),
     ('1','Mikurigaike pond','~0.8 km','30 min','The plateau\'s iconic crater lake. On clear days Oyama reflects upside down in its surface.','50','tip','Mornings are calmest and most photogenic.'),
     ('2','Jigokudani vents','~0.6 km','30 min','Steaming volcanic fumaroles. Stay on the boardwalk and follow any hydrogen-sulfide alerts.','85','warn','Sections may close depending on gas levels — obey all notices.'),
     ('Return','Back to Murodo','~0.6 km','20 min','Return along the plateau path.','30','tip','With extra time, add a soak at Raichozawa Onsen (about 20 minutes on foot).'),
   ],
   'tips': [
     ('backpack','Gear',['Windproof layer (plateau wind)','Sunscreen & hat','Water & snacks','Cash for facilities']),
     ('book','Season & lodging',['Alpine Route open Apr 15 – Nov 30','Murodo Sanso reservations (official/Yamaten)','Peak-season beds sell out early']),
     ('warning','Cautions',['Alpine climate (year-round lows near 5°C)','Volcanic gas closures','Snow on the summit until mid-June']),
   ],
   'map_note': 'Murodo plateau highlights loop', 'map_start': 'Murodo terminal', 'map_end': 'Jigokudani',
   'map_path': 'M120 320 C250 300, 360 250, 460 205 S610 140, 670 110',
   'map_nodes': [(120,320,10),(460,205,8),(670,110,12)],
   'cps': [
     ('Murodo terminal','Starting Point','badge-trailhead','2,450 m','0 km','Terminal · shops · lodging'),
     ('Mikurigaike','Lake','badge-landmark','~2,430 m','~0.8 km','Hut · water'),
     ('Jigokudani vents','Attraction','badge-landmark','~2,400 m','~1.4 km','Boardwalk · gates'),
     ('Raichozawa Onsen (optional)','Optional','badge-shelter','~2,300 m','~20 min one way','Open-air bath · hut'),
     ('Back at Murodo','End','badge-trailhead','2,450 m','~2 km','Restaurants'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': 'Intermediate',
   'name': 'Oyama Summit Climb',
   'sub': 'Murodo → Oyama summit 3,003 m round trip · about 6 km · 3–4 hours',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Round trip','~6 km') + pill('clock','Time','3–4 h') + pill('location','Oyama','3,003 m') + pill_meter('Difficulty',3,'medium') + pill('star','Best season','Jul–Oct') + pill('location','Base','Murodo 2,450 m'),
   'flow': ['Depart Murodo','Sunlight ridgeline','Oyama summit shrine 3,003 m','Descend'],
   'elev_label': 'Oyama 3,003 m', 'elev_peak': (740, 46),
   'elev_path': 'M20 178 C170 170, 320 140, 470 108 S640 66, 740 46',
   'desc': 'The standard climb to Oyama (雄山, 3,003 m), the main peak of the Tateyama three. Gain about 550 m from Murodo to reach the summit shrine — a mountain where climbing and worship have always gone together. Snow lingers on the summit until mid-June; crampons may be needed.',
   'segs': [
     ('Start','Murodo → trailhead','0.3 km','10 min','The trail starts behind Murodo Sanso. A morning start leaves weather margin.','10','tip','The Alpine-Route-side trail is well maintained but the altitude gain is real.'),
     ('1','Trailhead → Nakano-yama','~2.4 km','1–1.5 h','Gentle rocky paths with ever-widening views. The Nakano-yama hut sits mid-route.','45','tip','If energy runs low, turning back at Nakano-yama is a fine choice.'),
     ('2','Nakano-yama → summit','~0.3 km','30–40 min','Chains and ladders on a short rocky ridge lead to Oyama Shrine at 3,003 m; the Hakuba range appears on clear days.','85','warn','The final ridge has chain sections — gloves help.'),
     ('Return','Summit → Murodo','~3 km','1.5 h','Descend the same way. Through mid-June wear crampons on lingering snow.','30','warn','Snow remains on the summit until mid-June — bring crampons (and an ice axe if needed).'),
   ],
   'tips': [
     ('backpack','Gear',['Hiking boots','Windproof & insulated layers','Headlamp','Gloves for chains']),
     ('book','Lodging',['Murodo Sanso (at Murodo)','Raichozawa Onsen hut','Book via official site / Yamaten']),
     ('warning','Cautions',['Snow until mid-June','Afternoon storms & wind','Chain sections on the ridge']),
   ],
   'map_note': 'Standard Oyama ascent', 'map_start': 'Murodo 2,450 m', 'map_end': 'Oyama 3,003 m',
   'map_path': 'M110 335 C240 315, 350 265, 460 210 S630 90, 700 55',
   'map_nodes': [(110,335,10),(460,210,8),(700,55,12)],
   'cps': [
     ('Murodo trailhead','Starting Point','badge-trailhead','2,450 m','0 km','Hut · shop'),
     ('Nakano-yama','Hut','badge-shelter','~2,698 m','~2.4 km','Hut · water'),
     ('Oyama summit shrine','Summit','badge-summit','3,003 m','~3 km','Shrine · viewpoint'),
     ('Descent rest point','Rest','badge-shelter','~2,700 m','1 km down','Bench'),
     ('Back at Murodo','End','badge-trailhead','2,450 m','~6 km round trip','Terminal'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': 'Advanced',
   'name': 'Tsurugi-dake Challenge',
   'sub': 'Murodo → Tsurugi-gozen 2,999 m round trip · about 5 km · 5–7 hours · chains & ladders',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Round trip','~5 km') + pill('clock','Time','5–7 h') + pill('location','Tsurugi-dake','2,999 m') + pill_meter('Difficulty',5,'hard') + pill('star','Best season','Jul–early Oct') + pill('location','Level','Expert'),
   'flow': ['Depart Murodo','Tsurugi-sawa climb','Chain & ladder ridge','Tsurugi-gozen 2,999 m'],
   'elev_label': 'Tsurugi-dake 2,999 m', 'elev_peak': (740, 40),
   'elev_path': 'M20 185 C170 180, 300 160, 430 128 S620 68, 740 40',
   'desc': 'A route up Tsurugi-dake (劍岳, 2,999 m), called Japan\'s most formidable rock peak. Continuous chains, ladders, and iron rungs make this genuine alpine scrambling — only for highly experienced mountaineers, and turning back in bad weather is mandatory judgment.',
   'segs': [
     ('Start','Murodo → Tsurugi-sawa fork','~0.7 km','20 min','Approach to the Tsurugi-sawa junction where the route splits from the Oyama course. The standard start is 05:00–06:00.','8','tip','Work backwards from your descent deadline when choosing a start time.'),
     ('1','Tsurugi-sawa → Tsurugigozen hut','~1.3 km','1.5–2 h','A rough ascent over rock and scree. Tsurugigozen hut just below the summit is the last resupply.','35','warn','This is the turn-back decision point. In bad weather, give up here.'),
     ('2','Hut → summit','~0.3 km','1–1.5 h','The core ridge: continuous chains, ladders, and iron rungs. Helmet recommended.','88','warn','Absolutely not for beginners. Only experienced scramblers; yield to oncoming climbers.'),
     ('Return','Summit → Murodo','~2.5 km','2–3 h','Descending the ridge carries higher accident risk than the ascent — take your time.','28','warn','Full concentration is required on chains even while descending.'),
   ],
   'tips': [
     ('backpack','Gear',['Helmet & harness (recommended)','Climbing gloves','Windproof & insulated clothing','Headlamp & emergency food']),
     ('book','Lodging',['Tsurugigozen hut (just below summit)','Murodo Sanso (night before)','Book months ahead in peak season']),
     ('warning','Cautions',['Dedicated alpine scramble','Turn back immediately in bad weather','Strict descent deadline']),
   ],
   'map_note': 'Japan\'s toughest ridge scramble', 'map_start': 'Murodo 2,450 m', 'map_end': 'Tsurugi-dake 2,999 m',
   'map_path': 'M90 345 C210 330, 320 300, 430 255 S630 95, 705 52',
   'map_nodes': [(90,345,10),(430,255,8),(705,52,12)],
   'cps': [
     ('Depart Murodo','Starting Point','badge-trailhead','2,450 m','0 km','Hut · terminal'),
     ('Tsurugi-sawa fork','Junction','badge-trailhead','~2,500 m','~0.7 km','Signpost'),
     ('Tsurugigozen hut','Hut','badge-shelter','~2,930 m','~2 km','Hut · cooking'),
     ('Chain & ladder ridge','Key section','badge-summit','~2,950 m','~2.3 km','Chains · ladders'),
     ('Tsurugi-gozen summit','Summit','badge-summit','2,999 m','~2.5 km','Triangulation point'),
   ],
  },
 ],
}

# ═══════════ 황산 콘텐츠 ═══════════
HUANGSHAN = {
 'ko': {
  'title': '황산 등산 플레이북',
  'meta': '중국 안후이 황산(黃山) 가이드. 초급 운곡 케이블카+시신봉 루프, 중급 광명정(1,860m) 일출 코스, 고급 천도봉(1,829m) 등반 코스의 상세 경로, 실사 지도 및 팁을 제공합니다.',
  'h1_card': '황산',
  'p_card': 'Huangshan · 기암·소나무·운해의 명산 · 최고봉 연화봉 1,864m',
  'hero_alt': '화강암 기봉과 소나무, 운해가 어우러진 황산의 절경',
  'badge': '황산 플레이북',
  'h1': '황산 등산 플레이북',
  'hero_desc': '중국 최고의 명산 황산 가이드. 기암괴석과 송나무, 운해의 절경 — 케이블카를 활용한 초급 루프부터 광명정 일출, 천도봉 등반까지의 상세 경로와 팁을 제공합니다.',
  'btn1': '초급: 케이블카+시신봉 루프', 'btn2': '중급: 광명정 일출 코스', 'btn3': '고급: 천도봉 등반',
  'hero_photographer': 'Eric xu', 'hero_url': 'https://unsplash.com/photos/Pw2cEiZamVM',
  'gal_title': '황산의 사계 &amp; 명소',
  'lb_zoom': '크게 보기',
  'gallery': [
   ('g1', '화강암 기봉과 소나무', "Photo by &lt;a href='https://unsplash.com/photos/qjtfK5Mp9vk' target='_blank' rel='noopener'&gt;Eric xu&lt;/a&gt; on Unsplash"),
   ('g2', '운해에 잠긴 산봉우리', "Photo by &lt;a href='https://unsplash.com/photos/R6mcsVqh1P8' target='_blank' rel='noopener'&gt;Wei Pan&lt;/a&gt; on Unsplash"),
   ('g3', '절벽 위의 고목', "Photo by &lt;a href='https://unsplash.com/photos/dH4QBMugdjE' target='_blank' rel='noopener'&gt;David Magalhães&lt;/a&gt; on Unsplash"),
   ('g4', '급경사 돌계단', "Photo by &lt;a href='https://unsplash.com/photos/UKBkp-ubSws' target='_blank' rel='noopener'&gt;Joshua Earle&lt;/a&gt; on Unsplash"),
  ],
 },
 'en': {
  'title': 'Huangshan Hiking Playbook',
  'meta': 'Guide to Huangshan (Yellow Mountain), Anhui, China. Detailed routes, real maps and tips for the Yungu cable-car loop, the Guangmingding (1,860 m) sunrise course, and the Tiandu Feng (1,829 m) summit climb.',
  'h1_card': 'Huangshan',
  'p_card': 'Huangshan · Granite pinnacles, pines & cloud seas · Highest peak 1,864 m',
  'hero_alt': 'Jagged granite pinnacles with pines and a sea of clouds in Huangshan',
  'badge': 'Huangshan Playbook',
  'h1': 'Huangshan Hiking Playbook',
  'hero_desc': 'A guide to China\'s most celebrated mountain — granite pinnacles, twisted pines, and seas of clouds. Routes from an easy cable-car loop to the Guangmingding sunrise and the Tiandu Feng summit climb.',
  'btn1': 'Beginner: Cable Car + Shixin Loop', 'btn2': 'Intermediate: Guangmingding Sunrise', 'btn3': 'Advanced: Tiandu Feng Climb',
  'hero_photographer': 'Eric xu', 'hero_url': 'https://unsplash.com/photos/Pw2cEiZamVM',
  'gal_title': 'Huangshan Four Seasons &amp; Attractions',
  'lb_zoom': 'View larger',
  'gallery': [
   ('g1', 'Granite pinnacles & pines', "Photo by &lt;a href='https://unsplash.com/photos/qjtfK5Mp9vk' target='_blank' rel='noopener'&gt;Eric xu&lt;/a&gt; on Unsplash"),
   ('g2', 'Peaks in the cloud sea', "Photo by &lt;a href='https://unsplash.com/photos/R6mcsVqh1P8' target='_blank' rel='noopener'&gt;Wei Pan&lt;/a&gt; on Unsplash"),
   ('g3', 'Lone tree on the cliff', "Photo by &lt;a href='https://unsplash.com/photos/dH4QBMugdjE' target='_blank' rel='noopener'&gt;David Magalhães&lt;/a&gt; on Unsplash"),
   ('g4', 'Steep stone stairs', "Photo by &lt;a href='https://unsplash.com/photos/UKBkp-ubSws' target='_blank' rel='noopener'&gt;Joshua Earle&lt;/a&gt; on Unsplash"),
  ],
 },
}

HUANGSHAN_COURSES = {
 'ko': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': '초급',
   'name': '운곡 케이블카 + 시신봉 루프',
   'sub': '운곡 케이블카 → 시신봉 → 북해·서해 산책 · 약 4km · 3~4시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','산내 도보','약 4km') + pill('clock','소요 시간','3~4h') + pill('location','산상 해발','약 1,700m') + pill_meter('난이도',2,'medium') + pill('star','입장료','190위안') + pill('location','케이블카','80위안'),
   'flow': ['운곡 케이블카','시신봉 1,683m','북해·서해 전망','원점'],
   'elev_label': '시신봉 전망대', 'elev_peak': (560, 72),
   'elev_path': 'M20 150 C160 142, 300 120, 440 95 S540 80, 560 72',
   'desc': '케이블카로 산상까지 올라 황산의 대표 절경을 도는 가장 효율적인 코스입니다. 시신봉(始信峰)의 기암과 소나무, 북해·서해 전망대의 운해를 감상합니다. 완만한 돌계단 위주라 누구나 즐길 수 있습니다.',
   'segs': [
     ('출','운곡사 → 운곡 케이블카','약 0.5km','15~20분','탕구(湯口)에서 구간버스로 운곡사 정류장에 도착합니다. 케이블카(편도 80위안)로 약 8분 만에 산상(약 1,670m)에 도착합니다.','15','tip','성수기 케이블카 줄이 깁니다. 개장 시간(보통 07:00)에 맞춰 일찍 도착하세요.'),
     ('1','케이블카역 → 시신봉','약 1.5km','1~1.5시간','소나무와 기암 사이 돌계단을 걸어 시신봉(始信峰, 1,683m) 전망대에 오릅니다. 「황산에 오르면 천하의 산은 그만이다」는 말의 시작점입니다.','55','tip','흑호송(黑虎松)·연리송(連理松) 등 명송을 감상하며 걷습니다.'),
     ('2','시신봉 → 북해·서해 전망','약 2.0km','1.5~2시간','북해빈관 방면 전망대에서 사자봉·운해를 감상합니다. 서해대협곡 입구까지 갔다가 되돌아올 수 있습니다.','90','warn','서해대협곡은 동절기(12월~3월경) 폐쇄됩니다. 방문 전 개방 여부를 확인하세요.'),
     ('하','원점 복귀','약 0.5km','30분','같은 길로 케이블카역으로 돌아옵니다.','30','tip','일정이 남으면 산상 숙박 후 일출 코스로 연결할 수 있습니다.'),
   ],
   'tips': [
     ('backpack','준비물',['편한 워킹화','우비(산내 날씨 급변)','물·간식','여권(실명 입장 확인용)']),
     ('book','입장·요금',['입장료 190위안(성수기)·150위안(동절기)','입장권 3일 유효','케이블카 운곡 80위안(편도)']),
     ('warning','주의',['성수기 인파·대기','서해대협곡 동절기 폐쇄','안개 시 전망 불가']),
   ],
   'map_note': '케이블카 활용 초급 루프', 'map_start': '운곡 케이블카역', 'map_end': '시신봉 1,683m',
   'map_path': 'M110 330 C240 310, 360 260, 470 210 S620 120, 680 85',
   'map_nodes': [(110,330,10),(470,210,8),(680,85,12)],
   'cps': [
     ('운곡 케이블카역','출발점','badge-trailhead','해발 약 1,670m','누적 0km','역사·매점'),
     ('시신봉','봉우리','badge-summit','해발 1,683m','누적 약 1.5km','전망대'),
     ('북해 전망대','전망','badge-landmark','해발 약 1,700m','누적 약 2.5km','호텔·식당'),
     ('서해대협곡 입구','명소','badge-landmark','해발 약 1,650m','누적 약 3.5km','동절기 폐쇄'),
     ('원점(운곡역)','종점','badge-trailhead','해발 약 1,670m','누적 약 4km','케이블카'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': '중급',
   'name': '광명정(1,860m) 일출 코스',
   'sub': '산상 1박 → 광명정 일출 → 연화봉 방면 산책 · 약 8km · 6~8시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','산내 도보','약 8km') + pill('clock','소요 시간','6~8h') + pill('location','광명정','1,860m') + pill_meter('난이도',3,'medium') + pill('star','일출 시각','계절별 확인') + pill('location','숙박','산상 호텔'),
   'flow': ['케이블카 상산','산상 1박','광명정 일출 1,860m','옥병루 하산'],
   'elev_label': '광명정 1,860m', 'elev_peak': (700, 48),
   'elev_path': 'M20 165 C170 155, 320 120, 470 95 S620 60, 700 48',
   'desc': '황산의 정수인 일출을 광명정(光明頂, 1,860m)에서 감상하는 1박 2일 코스입니다. 첫날 옥병 또는 운곡 케이블카로 상산해 산상 호텔(북해·서해·백운 등)에 1박하고, 다음 날 새벽 광명정에서 일출을 본 뒤 옥병루 방면 명송을 감상하며 하산합니다.',
   'segs': [
     ('출','상산 (케이블카)','—','오전','케이블카와 도보를 조합해 산상으로 올라옵니다. 산상 호텔에 짐을 맡기고 오후에 인근 봉우리를 산책합니다.','20','tip','산상 숙박은 성수기 몇 주 전 예약이 필요합니다. 가격이 높으니 여유 예산을 준비하세요.'),
     ('1','산상 오후 산책','약 3km','2~3시간','비래석·배송(迎客松) 등 황산의 상징을 오후 빛으로 감상합니다.','50','tip','구름이 낮게 깔린 날이 운해 확률이 높습니다.'),
     ('2','광명정 일출','약 1km','새벽 1~1.5시간','숙소에서 광명정(1,860m)까지 새벽 이동합니다. 인파가 많으니 일출 40~50분 전 도착을 권장합니다.','85','warn','새벽 산상은 매우 춥고 어둡습니다. 헤드랜턴과 방한 의류가 필수입니다.'),
     ('하','옥병루 하산','약 4km','2.5~3.5시간','배송과 옥병루(迎客松)를 지나 옥병 케이블카(편도 90위안) 또는 도보로 하산합니다.','30','tip','옥병루 계단은 급합니다. 무릎 보호대·스틱을 권장합니다.'),
   ],
   'tips': [
     ('backpack','준비물',['헤드랜턴','방한 의류(새벽 한랭)','무릎 보호대','여권']),
     ('book','숙박·요금',['산상 호텔(북해·서해·백운 등)','입장료 190위안·3일 유효','케이블카 옥병 90·운곡 80위안']),
     ('warning','주의',['일출 명소 혼잡','산상 물가高','동절기 협곡·봉우리 폐쇄']),
   ],
   'map_note': '산상 1박 일출 표준 코스', 'map_start': '운곡/옥병 케이블카', 'map_end': '광명정 1,860m',
   'map_path': 'M100 335 C230 320, 340 275, 450 220 S620 95, 695 55',
   'map_nodes': [(100,335,10),(450,220,8),(695,55,12)],
   'cps': [
     ('케이블카역','출발점','badge-trailhead','해발 약 1,670m','누적 0km','역사'),
     ('산상 호텔','숙박','badge-shelter','해발 약 1,700m','누적 약 2km','북해·서해·백운 등'),
     ('비래석·배송','명소','badge-landmark','해발 약 1,680m','누적 약 4km','전망대'),
     ('광명정','봉우리','badge-summit','해발 1,860m','누적 약 5km','일출 명소'),
     ('옥병루·배송 하산','종점','badge-trailhead','해발 약 1,600m','누적 약 8km','옥병 케이블카'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': '고급',
   'name': '천도봉(1,829m) 등반 코스',
   'sub': '옥병루 → 천도봉 정상 왕복 · 약 5km · 4~5시간 · 급계단 암릉',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','왕복 거리','약 5km') + pill('clock','소요 시간','4~5h') + pill('location','천도봉','1,829m') + pill_meter('난이도',4,'hard') + pill('star','개방','연화봉과 교대') + pill('location','예약','실명 예약'),
   'flow': ['옥병루 출발','급계단 등반','천도봉 1,829m','원점 하산'],
   'elev_label': '천도봉 1,829m', 'elev_peak': (740, 50),
   'elev_path': 'M20 175 C170 165, 320 135, 470 100 S640 65, 740 50',
   'desc': '황산에서 가장 험준한 봉우리로 불리는 천도봉(天都峰, 1,829m)을 오르는 코스입니다. 「잉객송(배송)」 위쪽의 급계단을 80도에 가깝게 오르는 구간이 유명합니다. 생태 보호를 위해 연화봉과 교대로 개방되며, 실명 예약이 필요합니다. 심장·고소공포가 있다면 피하세요.',
   'segs': [
     ('출','옥병루 → 천도봉 등산로 입구','약 0.5km','20분','배송(迎客松) 근처 등산로 입구에서 시작합니다. 오전 조기 입장이 대기 없이 등반하는 핵심입니다.','12','tip','실명 예약 정보를 미리 확인하고 여권을 지참하세요.'),
     ('1','등산로 입구 → 천도석(天都石)','약 1.5km','1~1.5시간','가파른 돌계단이 연속됩니다. 난간을 잡고 천천히 오릅니다.','50','warn','경사가 매우 급합니다. 고소공포증이 있으면 진입하지 마세요.'),
     ('2','천도석 → 정상','약 0.3km','30~40분','「등천도(登天都)」라 불리는 최후 구간입니다. 정상에서는 전망이 360도로 열립니다.','88','warn','바람이 강한 날은 정상 체류를 짧게 하세요.'),
     ('하','정상 → 옥병루 하산','약 2.5km','1.5~2시간','같은 계단으로 하산합니다. 하산 사고가 많은 구간이므로 옆모습 자세로 천천히.','30','warn','하산 시 계단 미끄럼 사고가 잦습니다. 스틱을 접고 난간을 잡고 내려오세요.'),
   ],
   'tips': [
     ('backpack','준비물',['트레킹화(미끄럼 방지)','장갑','무릎 보호대','물 1L 이상']),
     ('book','예약·요금',['실명 예약 필수(공식 미니프로그램)','입장료 190위안','연화봉과 교대 개방 확인']),
     ('warning','주의',['80도 급계단','고소공포증 진입 금지','우천 시 폐쇄될 수 있음']),
   ],
   'map_note': '황산 최험 봉우리 등반', 'map_start': '옥병루 출발', 'map_end': '천도봉 1,829m',
   'map_path': 'M95 340 C215 325, 330 285, 440 235 S625 100, 700 58',
   'map_nodes': [(95,340,10),(440,235,8),(700,58,12)],
   'cps': [
     ('옥병루 등산로 입구','출발점','badge-trailhead','해발 약 1,600m','누적 0km','배송·매점'),
     ('급계단 구간 시작','핵심','badge-summit','해발 약 1,680m','누적 약 1km','난간'),
     ('천도석','휴게','badge-landmark','해발 약 1,780m','누적 약 2.5km','전망'),
     ('천도봉 정상','봉우리','badge-summit','해발 1,829m','누적 약 2.8km','360도 전망'),
     ('옥병루 복귀','종점','badge-trailhead','해발 약 1,600m','왕복 약 5km','케이블카 연계'),
   ],
  },
 ],
 'en': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': 'Beginner',
   'name': 'Yungu Cable Car + Shixin Loop',
   'sub': 'Yungu cable car → Shixin Peak → Beihai/Xihai lookouts · about 4 km · 3–4 hours',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','On-mountain walk','~4 km') + pill('clock','Time','3–4 h') + pill('location','Elevation','~1,700 m') + pill_meter('Difficulty',2,'medium') + pill('star','Entry','190 RMB') + pill('location','Cable car','80 RMB'),
   'flow': ['Yungu cable car','Shixin Peak 1,683 m','Beihai/Xihai lookouts','Back to start'],
   'elev_label': 'Shixin Peak platform', 'elev_peak': (560, 72),
   'elev_path': 'M20 150 C160 142, 300 120, 440 95 S540 80, 560 72',
   'desc': 'The most efficient course: ride the cable car to the summit plateau and loop Huangshan\'s signature scenery — the pinnacles and pines of Shixin Peak and the cloud-sea lookouts of Beihai and Xihai. Gentle stone stairs throughout.',
   'segs': [
     ('Start','Yungu Temple → cable car','~0.5 km','15–20 min','Take the shuttle from Tangkou to Yungu Temple, then the cable car (80 RMB one way) — about 8 minutes to the plateau (~1,670 m).','15','tip','Queues get long in peak season — arrive near opening time (usually 07:00).'),
     ('1','Cable-car station → Shixin Peak','~1.5 km','1–1.5 h','Stone stairs wind among pines and pinnacles to the Shixin Peak platform (1,683 m) — the origin of "after Huangshan, no other mountain matters."','55','tip','Admire famous pines like Black Tiger and Lianli on the way.'),
     ('2','Shixin → Beihai/Xihai lookouts','~2.0 km','1.5–2 h','View the Lion Peak cloud seas from the Beihai Hotel terraces; you can extend to the West Sea Grand Canyon entrance and back.','90','warn','The West Sea Grand Canyon closes in winter (roughly December–March) — check before visiting.'),
     ('Return','Back to start','~0.5 km','30 min','Return the same way to the cable-car station.','30','tip','With time to spare, stay overnight and connect to the sunrise course.'),
   ],
   'tips': [
     ('backpack','Gear',['Comfortable walking shoes','Rain shell (fast-changing weather)','Water & snacks','Passport (real-name entry check)']),
     ('book','Entry & fees',['Entry 190 RMB peak / 150 RMB winter','Ticket valid 3 consecutive days','Yungu cable car 80 RMB one way']),
     ('warning','Cautions',['Peak-season crowds & queues','West Sea Canyon closed in winter','Fog can hide all views']),
   ],
   'map_note': 'Beginner loop via cable car', 'map_start': 'Yungu cable-car station', 'map_end': 'Shixin Peak 1,683 m',
   'map_path': 'M110 330 C240 310, 360 260, 470 210 S620 120, 680 85',
   'map_nodes': [(110,330,10),(470,210,8),(680,85,12)],
   'cps': [
     ('Yungu cable-car station','Starting Point','badge-trailhead','~1,670 m','0 km','Station · shop'),
     ('Shixin Peak','Summit','badge-summit','1,683 m','~1.5 km','Viewing platform'),
     ('Beihai lookout','Viewpoint','badge-landmark','~1,700 m','~2.5 km','Hotels · restaurants'),
     ('West Sea Canyon entrance','Attraction','badge-landmark','~1,650 m','~3.5 km','Closed in winter'),
     ('Back at Yungu station','End','badge-trailhead','~1,670 m','~4 km','Cable car'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': 'Intermediate',
   'name': 'Guangmingding Sunrise Course',
   'sub': 'Summit overnight → Guangmingding sunrise → Yuping descent · about 8 km · 6–8 hours',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','On-mountain walk','~8 km') + pill('clock','Time','6–8 h') + pill('location','Guangmingding','1,860 m') + pill_meter('Difficulty',3,'medium') + pill('star','Sunrise','Check by season') + pill('location','Lodging','Summit hotels'),
   'flow': ['Cable car up','Summit night','Guangmingding sunrise 1,860 m','Descend via Yuping'],
   'elev_label': 'Guangmingding 1,860 m', 'elev_peak': (700, 48),
   'elev_path': 'M20 165 C170 155, 320 120, 470 95 S620 60, 700 48',
   'desc': 'A 2-day course for Huangshan\'s essence: the sunrise. Ride a cable car up, overnight at a summit hotel (Beihai, Xihai, Baiyun…), watch dawn from Guangmingding (Bright Summit, 1,860 m), then descend via Yuping past the famous Greeting Pine.',
   'segs': [
     ('Start','Ascend by cable car','—','Morning','Combine cable car and walking to reach the plateau; drop your bags at the hotel and explore nearby peaks in the afternoon.','20','tip','Summit hotels need booking weeks ahead in peak season and are pricey — budget accordingly.'),
     ('1','Afternoon summit walk','~3 km','2–3 h','See Feilai Stone (Rock Flown From Afar) and the Greeting Pine in afternoon light.','50','tip','Low-hanging clouds raise the odds of a cloud sea the next morning.'),
     ('2','Guangmingding sunrise','~1 km','1–1.5 h before dawn','Walk from the hotel to Guangmingding (1,860 m) in the dark. Aim to arrive 40–50 minutes before sunrise — the crowds are large.','85','warn','It is very cold and dark — headlamp and warm layers are essential.'),
     ('Return','Descent via Yuping','~4 km','2.5–3.5 h','Descend past the Greeting Pine to Yuping cable car (90 RMB one way) or on foot.','30','tip','Yuping stairs are steep — knee braces and poles are recommended.'),
   ],
   'tips': [
     ('backpack','Gear',['Headlamp','Warm layers (freezing dawn)','Knee braces','Passport']),
     ('book','Lodging & fees',['Summit hotels (Beihai/Xihai/Baiyun…)','Entry 190 RMB · valid 3 days','Yuping 90 / Yungu 80 RMB one way']),
     ('warning','Cautions',['Sunrise spots are packed','Summit prices are high','Winter closures for canyons & peaks']),
   ],
   'map_note': 'Overnight sunrise standard course', 'map_start': 'Yungu/Yuping cable car', 'map_end': 'Guangmingding 1,860 m',
   'map_path': 'M100 335 C230 320, 340 275, 450 220 S620 95, 695 55',
   'map_nodes': [(100,335,10),(450,220,8),(695,55,12)],
   'cps': [
     ('Cable-car station','Starting Point','badge-trailhead','~1,670 m','0 km','Station'),
     ('Summit hotel','Lodging','badge-shelter','~1,700 m','~2 km','Beihai/Xihai/Baiyun etc.'),
     ('Feilai Stone & Greeting Pine','Attraction','badge-landmark','~1,680 m','~4 km','Viewpoints'),
     ('Guangmingding','Summit','badge-summit','1,860 m','~5 km','Sunrise spot'),
     ('Yuping descent','End','badge-trailhead','~1,600 m','~8 km','Yuping cable car'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': 'Advanced',
   'name': 'Tiandu Feng Summit Climb',
   'sub': 'Yuping trail → Tiandu Feng round trip · about 5 km · 4–5 hours · steep stair scramble',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Round trip','~5 km') + pill('clock','Time','4–5 h') + pill('location','Tiandu Feng','1,829 m') + pill_meter('Difficulty',4,'hard') + pill('star','Openings','Alternates with Lotus Peak') + pill('location','Booking','Real-name reservation'),
   'flow': ['Depart Yuping trail','Steep stair climb','Tiandu Feng 1,829 m','Descend to start'],
   'elev_label': 'Tiandu Feng 1,829 m', 'elev_peak': (740, 50),
   'elev_path': 'M20 175 C170 165, 320 135, 470 100 S640 65, 740 50',
   'desc': 'The climb up Tiandu Feng (Celestial Capital Peak, 1,829 m), Huangshan\'s most vertiginous summit — famous for near-80-degree stairways above the Greeting Pine. For ecological rest the peak alternates opening periods with Lotus Peak, and a real-name reservation is required. Not for those with heart conditions or fear of heights.',
   'segs': [
     ('Start','Yuping trail → Tiandu trailhead','~0.5 km','20 min','Start near the Greeting Pine. Early entry is the key to climbing without crowds.','12','tip','Check your reservation details and carry your passport.'),
     ('1','Trailhead → Tiandu Stone','~1.5 km','1–1.5 h','Relentless steep stone stairs with handrails. Go slowly, holding the rails.','50','warn','The gradient is extreme — do not enter if you have vertigo.'),
     ('2','Tiandu Stone → summit','~0.3 km','30–40 min','The final "ascending-to-heaven" section. The summit opens up to a 360-degree panorama.','88','warn','Wind is strong — keep summit time short on gusty days.'),
     ('Return','Summit → Yuping trail','~2.5 km','1.5–2 h','Descend the same stairs — this stretch sees many slips. Face the slope and go slowly.','30','warn','Descending slips are common here: stow your poles and hold the rails.'),
   ],
   'tips': [
     ('backpack','Gear',['Anti-slip hiking shoes','Gloves','Knee braces','1 L+ water']),
     ('book','Reservation & fees',['Real-name reservation required (official mini-program)','Entry 190 RMB','Check which of Tiandu/Lotus is open']),
     ('warning','Cautions',['Near-vertical stairways','Off-limits with vertigo','May close in rain']),
   ],
   'map_note': 'Huangshan\'s most daring summit', 'map_start': 'Yuping trailhead', 'map_end': 'Tiandu Feng 1,829 m',
   'map_path': 'M95 340 C215 325, 330 285, 440 235 S625 100, 700 58',
   'map_nodes': [(95,340,10),(440,235,8),(700,58,12)],
   'cps': [
     ('Yuping trailhead','Starting Point','badge-trailhead','~1,600 m','0 km','Greeting Pine · shop'),
     ('Steep stairs begin','Key section','badge-summit','~1,680 m','~1 km','Handrails'),
     ('Tiandu Stone','Rest','badge-landmark','~1,780 m','~2.5 km','View'),
     ('Tiandu Feng summit','Summit','badge-summit','1,829 m','~2.8 km','360° panorama'),
     ('Back at Yuping','End','badge-trailhead','~1,600 m','~5 km round trip','Cable car link'),
   ],
  },
 ],
}

CONTENT = {
  'tateyama': TATEYAMA,
  'huangshan': HUANGSHAN,
}
COURSES = {
  'tateyama': TATEYAMA_COURSES,
  'huangshan': HUANGSHAN_COURSES,
}

if __name__ == '__main__':
    mountain, lang = sys.argv[1], sys.argv[2]
    html = build(mountain, lang)
    out = pathlib.Path(f'{mountain}-playbook.html') if lang == 'ko' else pathlib.Path(f'en/{mountain}-playbook.html')
    out.write_text(html, encoding='utf-8')
    print(f'wrote {out} ({len(html.splitlines())} lines)')
