#!/usr/bin/env python3
"""후지산 플레이북 빌더 — yushan 스켈레톤 변환 (STANDARD-DEEP-INFO.md §4.2 절차).

사실 게이트 준수: 수치·제도는 fujisan-climb.jp(공식) + highway-buses.jp/japan-guide 교차검증값,
스테이션 표고는 공식 루트 페이지의 대표값을 「약」으로 표기. 불확정 항목은 일반화.
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
            f'<circle cx="{px}" cy="{py}" fill="{color}" r="6"></circle><text fill="{color}" font-size="12" x="{px-148}" y="{py-10}">{label}</text></svg>')

def map_svg(color, note, start_label, end_label, path, nodes):
    ns = ''.join(f'<circle cx="{cx}" cy="{cy}" fill="{color}" r="{r}"></circle>' for cx, cy, r in nodes)
    return (f'<svg viewbox="0 0 760 420"><rect fill="var(--surface2)" height="400" rx="22" width="740" x="10" y="10"></rect>'
            f'<path d="{path}" fill="none" stroke="{color}" stroke-linecap="round" stroke-width="6"></path>{ns}'
            f'<text font-size="12" x="{nodes[0][0]-60}" y="{nodes[0][1]+28}">{start_label}</text>'
            f'<text font-size="12" x="{nodes[-1][0]-170}" y="{nodes[-1][1]-18}">{end_label}</text>'
            f'<text fill="var(--muted)" font-size="12" x="34" y="44">{note}</text></svg>')

L = 'ko'

def panels_lang(_title_site, courses):
    out = []
    for i, c in enumerate(courses):
        active = ' active' if i == 0 else ''
        color = c['color']
        # theme hex for svg strokes
        hexc = c['hex']
        flow = '<span class="arr">→</span>'.join(f'<span class="chip">{x}</span>' for x in c['flow'])
        segs = ''.join(seg(*s) for s in c['segs'])
        tips = ''.join(tipcard(*t) for t in c['tips'])
        cps = ''.join(cp(n+1, *x) for n, x in enumerate(c['cps']))
        out.append(f'''<section class="panel {color}{active}" id="{c['id']}"><div class="panel-top"><span class="level"><svg class="icon-svg"><use href="{IC}#icon-season"></use></svg> {c['level']}</span><div><div class="panel-name">{c['name']}</div><div class="panel-sub">{c['sub']}</div></div></div><div class="tabs"><button class="tab active" data-tab="overview"><svg class="icon-svg"><use href="{IC}#icon-prep"></use></svg> {c['tab_overview']}</button><button class="tab" data-tab="route"><svg class="icon-svg"><use href="{IC}#icon-book"></use></svg> {c['tab_route']}</button><button class="tab" data-tab="map"><svg class="icon-svg"><use href="{IC}#icon-location"></use></svg> {c['tab_map']}</button><button class="tab" data-tab="tips"><svg class="icon-svg"><use href="{IC}#icon-tip"></use></svg> {c['tab_tips']}</button></div>
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
    # head
    t = t.replace('<title>위산 등산 플레이북</title>', f'<title>{T["title"]}</title>', 1)
    t = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{T["meta"]}" name="description"/>', t, count=1)
    t = t.replace('assets/img/yushan/og.png', f'{pfx}assets/img/fuji/og.png')
    t = t.replace('hreflang="ko" rel="alternate"/><link href="en/yushan-playbook.html"', 'hreflang="ko" rel="alternate"/><link href="en/fuji-playbook.html"') if lang == 'ko' else t
    t = t.replace('../yushan-playbook.html', '../fuji-playbook.html') if lang == 'en' else t
    t = t.replace('yushan-playbook.html', 'fuji-playbook.html') if lang == 'ko' else t
    t = t.replace('<html data-theme="light" lang="ko">', '<html data-theme="light" lang="en">') if lang == 'en' else t

    # header card
    t = re.sub(r'<h1>위산</h1><p>[^<]*</p>', f'<h1>{T["h1_card"]}</h1><p>{T["p_card"]}</p>', t, count=1)

    # hero section — replace between markers
    hero_start = t.find('<section class="hero hero-bleed">')
    main_marker = '<main class="wrap">'
    main_idx = t.find(main_marker, hero_start)
    hero_html = f'''<section class="hero hero-bleed">
<picture class="hero-picture" id="heroFallbackImage">
<source sizes="100vw" srcset="{pfx}assets/img/fuji/hero-640.avif 640w, {pfx}assets/img/fuji/hero-1024.avif 1024w, {pfx}assets/img/fuji/hero-1600.avif 1600w, {pfx}assets/img/fuji/hero-2400.avif 2400w" type="image/avif"/>
<source sizes="100vw" srcset="{pfx}assets/img/fuji/hero-640.webp 640w, {pfx}assets/img/fuji/hero-1024.webp 1024w, {pfx}assets/img/fuji/hero-1600.webp 1600w, {pfx}assets/img/fuji/hero-2400.webp 2400w" type="image/webp"/>
<img alt="{T['hero_alt']}" class="hero-img" sizes="100vw" src="{pfx}assets/img/fuji/hero-1600.jpg" srcset="{pfx}assets/img/fuji/hero-640.jpg 640w, {pfx}assets/img/fuji/hero-1024.jpg 1024w, {pfx}assets/img/fuji/hero-1600.jpg 1600w, {pfx}assets/img/fuji/hero-2400.jpg 2400w"/>
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
<span class="credit-author">Photo by <a href="https://unsplash.com/photos/YKQKSpKpVZI" rel="noopener" target="_blank">Wren Chai</a></span>
<span class="credit-divider">/</span>
<span class="credit-source"><a href="https://unsplash.com" rel="noopener" target="_blank">Unsplash</a></span>
</div>
</section>
'''
    t = t[:hero_start] + hero_html + t[main_idx:]

    # panels region: from first panel section to </main>
    panels_start = t.find('<section class="panel')
    panels_end = t.find('</main>', panels_start)
    panels = panels_lang(None, COURSES[lang])
    t = t[:panels_start] + panels + '\n' + t[panels_end:]

    # gallery: replace images and credits
    gal_start = t.find('<section class="photo-gallery-section">')
    gal_end = t.find('</section>', gal_start) + len('</section>')
    caps = T['gallery']
    items = []
    for i, (name, title, cap) in enumerate(caps):
        items.append(f'''<button aria-haspopup="dialog" aria-label="{title} {T['lb_zoom']}" class="gallery-item" data-credit="{cap}" data-index="{i}">
<picture class="gallery-picture">
<source srcset="{pfx}assets/img/fuji/{name}.avif" type="image/avif"/>
<source srcset="{pfx}assets/img/fuji/{name}.webp" type="image/webp"/>
<img alt="" class="gallery-img" decoding="async" loading="lazy" src="{pfx}assets/img/fuji/{name}.jpg"/>
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

    # tail: deep-info mount, footer aria texts
    t = t.replace('data-mountain="yushan"', 'data-mountain="fuji"', 1)
    if lang == 'en':
        t = t.replace('../assets/js/', '../assets/js/')  # noop guard
    return t

# ── content (facts: fujisan-climb.jp official × highway-buses.jp × japan-guide) ──
CONTENT = {
  'ko': {
    'title': '후지산 등산 플레이북',
    'meta': '일본 최고봉 후지산(3,776m) 가이드. 초급 요시다 루트 1박 2일 일출 코스, 중급 후지노미야 당일 코스, 고급 고텐바 장거리 코스의 상세 경로, 실사 지도 및 팁을 제공합니다.',
    'h1_card': '후지산',
    'p_card': 'Fuji · 일본 최고봉 3,776m · 표준 1박 2일 요시다 코스',
    'hero_alt': '새벽 하늘 아래 분홍빛으로 물든 후지산의 웅장한 산세',
    'badge': '후지산 플레이북',
    'h1': '후지산 등산 플레이북',
    'hero_desc': '일본 최고봉 3,776m 가이드. 2025년부터 전 루트 통행료 4,000엔·요시다 예약제를 반영한, 초급 요시다 1박 2일부터 고텐바 장거리까지의 상세 경로와 팁을 제공합니다.',
    'btn1': '초급: 요시다 1박 2일 코스', 'btn2': '중급: 후지노미야 당일 코스', 'btn3': '고급: 고텐바 장거리 코스',
    'gal_title': '후지산의 사계 & 명소',
    'lb_zoom': '크게 보기',
    'gallery': [
      ('g1', '후지산 콘봉', "Photo by &lt;a href='https://unsplash.com/photos/xt5xG-fEj0M' target='_blank' rel='noopener'&gt;Alison Pang&lt;/a&gt; on Unsplash"),
      ('g2', '호수 반사 절경', "Photo by &lt;a href='https://unsplash.com/photos/6aV2WKzGJ_4' target='_blank' rel='noopener'&gt;Brian Chen&lt;/a&gt; on Unsplash"),
      ('g3', '오산(五合目) 사원과 후지산', "Photo by &lt;a href='https://unsplash.com/photos/C62Tb_iodQE' target='_blank' rel='noopener'&gt;Filiz Elaerts&lt;/a&gt; on Unsplash"),
      ('g4', '운해 위의 능선', "Photo by &lt;a href='https://unsplash.com/photos/rFX5FfVGeWE' target='_blank' rel='noopener'&gt;Zeke Tucker&lt;/a&gt; on Unsplash"),
    ],
  },
  'en': {
    'title': 'Mount Fuji Hiking Playbook',
    'meta': 'Guide to Mount Fuji (3,776m), the highest peak in Japan. Detailed routes, real maps and tips for the beginner Yoshida 2-day course, the intermediate Fujinomiya day hike, and the advanced Gotemba long haul.',
    'h1_card': 'Mount Fuji',
    'p_card': 'Fuji · Japan\'s highest peak 3,776m · Standard 2-day Yoshida course',
    'hero_alt': 'Mount Fuji glowing pink under a dawn sky',
    'badge': 'Mount Fuji Playbook',
    'h1': 'Mount Fuji Hiking Playbook',
    'hero_desc': 'A guide to Japan\'s highest peak at 3,776m. Reflecting the 2025 fee hike (4,000 yen on all trails) and the Yoshida reservation system, with detailed routes from the 2-day Yoshida climb to the Gotemba long haul.',
    'btn1': 'Beginner: Yoshida 2-Day Course', 'btn2': 'Intermediate: Fujinomiya Day Hike', 'btn3': 'Advanced: Gotemba Long Haul',
    'gal_title': 'Mount Fuji Four Seasons & Attractions',
    'lb_zoom': 'View larger',
    'gallery': [
      ('g1', 'Fuji cone', "Photo by &lt;a href='https://unsplash.com/photos/xt5xG-fEj0M' target='_blank' rel='noopener'&gt;Alison Pang&lt;/a&gt; on Unsplash"),
      ('g2', 'Lake reflection', "Photo by &lt;a href='https://unsplash.com/photos/6aV2WKzGJ_4' target='_blank' rel='noopener'&gt;Brian Chen&lt;/a&gt; on Unsplash"),
      ('g3', 'Temple and Fuji', "Photo by &lt;a href='https://unsplash.com/photos/C62Tb_iodQE' target='_blank' rel='noopener'&gt;Filiz Elaerts&lt;/a&gt; on Unsplash"),
      ('g4', 'Ridge above the clouds', "Photo by &lt;a href='https://unsplash.com/photos/rFX5FfVGeWE' target='_blank' rel='noopener'&gt;Zeke Tucker&lt;/a&gt; on Unsplash"),
    ],
  },
}

COURSES = {
 'ko': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': '초급',
   'name': '요시다 루트 1박 2일 코스',
   'sub': '스바루타 5합목 → 8합 산장 1박 → 새벽 등정 → 스바루타 5합목 · 왕복 약 13.6km · 등산 5~7시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','왕복 거리','약 13.6km') + pill('clock','등산 시간','5~7h') + pill('location','스바루타 5합목','약 2,300m') + pill_meter('난이도',3,'medium') + pill('star','등산기간','7/1~9/10') + pill('location','예약','통행료 4,000엔'),
   'flow': ['스바루타 5합목(약 2,300m)','8합 산장 1박(약 3,400m)','켄가미네 3,776m','원점 하산'],
   'elev_label': '켄가미네 3,776m', 'elev_peak': (740, 48),
   'elev_path': 'M20 190 C160 182, 280 164, 400 132 S580 84, 740 48',
   'desc': '가장 널리 권장되는 표준 코스입니다. 2025년부터 요시다 루트는 공식 사이트에서 온라인 예약·사전 결제(통행료 4,000엔)가 필요하고 하루 4,000명으로 정원이 제한되며, 오후 2시~익일 오전 3시에는 게이트가 폐쇄됩니다(산장 숙박 예약자는 예외). 오후에 들어가 8합 산장에서 1박하고 새벽에 정상에 서는 일정이 표준입니다.',
   'segs': [
     ('출','스바루타 5합목 출발','0km','약 2,300m','후지스바루라인 5합목에서 출발합니다. 예약·통행료 확인 후 게이트를 통과하세요. 오후 2시 이후 입산은 원칙적으로 제한됩니다.','20','tip','직통버스(신주쿠발 약 2시간 25분)는 성수기 예약이 빨리 마감되므로 조기 예약하세요.'),
     ('1','5합목 → 8합 산장','약 4.5km','5~7시간','사토고메야(6합)·태이시칸(7합)을 거쳐 8합 산장대까지 오릅니다. 산장과 매점이 가장 잘 갖춰진 루트입니다.','52','warn','오후 들어오는 산행은 게이트 폐쇄(14:00~익일 03:00)를 반드시 확인하세요.'),
     ('2','산장 1박 → 새벽 등정','약 2.3km','1.5~2.5시간','새벽 2~3시에 헤드랜턴을 켜고 분화구 능선을 따라 켄가미네(3,776m)로 오릅니다. 일출과 호에이(影)를 보고 오쿠미야 신사를 둘러봅니다.','86','tip','정상부는 여름에도 기온이 낮고 바람이 강합니다. 방풍·방한 의류가 필수입니다.'),
     ('하','정상 → 5합목 하산','약 6.8km','3~4시간','하산로(吉田 하산로)를 따라 5합목으로 내려옵니다. 하산길 모래·자갈 구간은 미끄러우니 천천히.','34','tip','하산로와 등산로가 갈라지는 지점을 놓치지 않도록 표지판을 확인하세요.'),
   ],
   'tips': [
     ('backpack','준비물',['방풍·방한 의류','헤드랜턴(여분 배터리)','고칼로리 간식·물 2L','현금(산장 지불용)']),
     ('book','예약·허가',['요시다 통행 예약(공식 사이트)','산장 숙박 예약 필수','통행료 4,000엔 사전 결제']),
     ('warning','주의',['14:00~익일 03:00 게이트 폐쇄','고산 기상 급변·저체온','성수기 인파·산장 혼잡']),
   ],
   'map_note': '표준 1박 2일 일출 코스', 'map_start': '스바루타 5합목', 'map_end': '켄가미네 3,776m',
   'map_path': 'M92 330 C220 300, 330 250, 440 190 S600 100, 696 60',
   'map_nodes': [(92,330,10),(440,190,8),(696,60,12)],
   'cps': [
     ('스바루타 5합목','출발점','badge-trailhead','해발 약 2,300m','누적 0km','버스터미널·매점·화장실'),
     ('6합 사토고메야','휴게','badge-shelter','해발 약 2,390m','누적 약 1.0km','산장·음수대'),
     ('7합 태이시칸','휴게','badge-shelter','해발 약 2,720m','누적 약 2.4km','산장·매점'),
     ('8합 태이칸사','산장 지대','badge-shelter','해발 약 3,020m','누적 약 3.6km','산장군·구급소'),
     ('켄가미네(정상)','봉우리','badge-summit','해발 3,776m','누적 약 6.8km','오쿠미야 신사'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': '중급',
   'name': '후지노미야 루트 당일 왕복 코스',
   'sub': '후지노미야 신5합목 → 정상 왕복 · 약 8.6km · 등산 4~5.5시간',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','왕복 거리','약 8.6km') + pill('clock','등산 시간','4~5.5h') + pill('location','신5합목','약 2,400m') + pill_meter('난이도',3,'medium') + pill('star','등산기간','7/10~9/10') + pill('location','예약','통행료 4,000엔'),
   'flow': ['후지노미야 신5합목(약 2,400m)','정상 3,776m','원점 하산'],
   'elev_label': '정상 3,776m', 'elev_peak': (740, 52),
   'elev_path': 'M20 172 C180 158, 320 128, 480 96 S660 66, 740 52',
   'desc': '가장 짧고 빠른 루트로, 시작 고도(약 2,400m)가 4루트 중 가장 높습니다. 다만 경사가 급하고 노출 구간이 많아 당일 왕복은 체력과 고산 적응이 뒷받침될 때 권장됩니다. 시즈오카 측 루트는 등산기간이 7월 10일~9월 10일이며 통행료는 등산로에서 지불합니다.',
   'segs': [
     ('출','후지노미야 신5합목 출발','0km','약 2,400m','시즈오카 측 후지노미야 루트의 들머리입니다. 아침 일찍 출발해 오후 기상 악화 전에 하산하는 일정을 세웁니다.','18','tip','정상 왕복 8~9시간이면 여유 있는 당일 일정입니다. 막차 시간을 먼저 확인하세요.'),
     ('1','5합목 → 8합','약 3.0km','2.5~3.5시간','완만하게 시작하지만 중반부터 경사가 급해집니다. 화산 자갈 지형에서 발을 보호하는 신발이 중요합니다.','58','warn','경사가 급하고 노출 구간이 있어 비·안개 시에는 하산을 우선합니다.'),
     ('2','8합 → 정상','약 1.3km','1.5~2시간','능선을 따라 정상 부근까지 오릅니다. 오쿠미야 신사(분화구 저변)까지 내려갔다 올라올 수 있습니다.','86','tip','분화구 내부로 내려가는 구간은 시간이 추가되니 하산 시간과 함께 계획하세요.'),
     ('하','정상 → 신5합목 하산','약 4.3km','2~3시간','등산로를 따라 내려옵니다. 무릎 부담이 크므로 스틱이 유용합니다.','30','tip','오후 뇌우가 잦습니다. 정오 전 등정·오후 이른 하산이 안전합니다.'),
   ],
   'tips': [
     ('backpack','준비물',['방풍·방한 의류','헤드랜턴','물 2L 이상','트레킹 스틱']),
     ('book','예약·요금',['통행료 4,000엔(현장 지불)','산장 숙박 시 별도 예약','당일 왕복은 예약 요건 확인']),
     ('warning','주의',['급경사·노출 구간','오후 뇌우·기상 급변','고산 증상(두통·구역)']),
   ],
   'map_note': '최단·최고 시작 고도 루트', 'map_start': '후지노미야 신5합목', 'map_end': '정상 3,776m',
   'map_path': 'M100 336 C230 310, 350 260, 470 200 S640 96, 700 56',
   'map_nodes': [(100,336,10),(470,200,8),(700,56,12)],
   'cps': [
     ('후지노미야 신5합목','출발점','badge-trailhead','해발 약 2,400m','누적 0km','버스·주차장·매점'),
     ('6합','휴게','badge-shelter','해발 약 2,590m','누적 약 1.1km','산장'),
     ('7합','휴게','badge-shelter','해발 약 2,780m','누적 약 1.9km','산장·음수대'),
     ('8합','산장 지대','badge-shelter','해발 약 3,100m','누적 약 2.8km','산장군'),
     ('오쿠미야 신사·정상','봉우리','badge-summit','해발 3,776m','누적 약 4.3km','신사'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': '고급',
   'name': '고텐바 루트 1박 2일 코스',
   'sub': '고텐바 신5합목 → 정상 → 원점 · 등산 약 10.5km · 공식 약 8시간 40분',
   'tab_overview': '개요', 'tab_route': '경로 안내', 'tab_map': '지도', 'tab_tips': '팁 &amp; 주의',
   'h_flow': '코스 흐름', 'h_elev': '고도 프로파일', 'h_route': '구간별 경로 안내', 'h_map': '코스 개념도', 'h_cp': '체크포인트 표',
   'pills': pill('ruler','왕복 거리','약 18.9km') + pill('clock','등산 시간','약 8h40m') + pill('location','신5합목','약 1,440m') + pill_meter('난이도',5,'hard') + pill('star','등산기간','7/10~9/10') + pill('location','예약','통행료 4,000엔'),
   'flow': ['고텐바 신5합목(약 1,440m)','8합 이상 능선','정상 3,776m','원점 하산'],
   'elev_label': '정상 3,776m', 'elev_peak': (740, 40),
   'elev_path': 'M20 200 C170 196, 300 180, 420 150 S600 92, 740 40',
   'desc': '4개 루트 중 가장 길고 표고차가 큰(약 2,300m) 코스입니다. 등산 약 10.5km에 공식 소요 약 8시간 40분, 하산 약 8.4km에 약 3시간 30분으로 안내되며, 넓은 사방(砂防) 지형을 길게 걷는 체력전입니다. 초보자에게는 권장되지 않으며, 1박 2일로 나눠 걷는 것이 표준입니다.',
   'segs': [
     ('출','고텐바 신5합목 출발','0km','약 1,440m','후지산 남동쪽 고텐바 신5합목에서 출발합니다. 시작 고도가 낮아 초반 더위와 장거리에 대비합니다.','12','tip','장거리 루트라 식수·행동식을 넉넉히 준비하고 페이스를 낮게 유지하세요.'),
     ('1','5합목 → 7합','약 4.8km','3~4시간','화산 사방 지형의 긴 직선 구간이 이어집니다. 스바시리 루트와 갈라지는 지점을 확인합니다.','42','warn','거리감이 안 오는 특수한 지형입니다. 시간 배분을 보수적으로 잡으세요.'),
     ('2','7합 → 8합 이상','약 3.2km','3~4시간','지그재그가 시작되며 고도를 크게 올립니다. 8합 위에서 요시다·스바시리 쪽 능선과 이어집니다.','70','warn','고도가 높아지며 증상이 나타나면 즉시 상승을 멈춥니다.'),
     ('하','정상 → 원점 하산','약 8.4km','약 3시간 30분','고텐바 하산로로 내려옵니다. 하산 거리가 길어 무릎 보호대가 사실상 필수입니다.','28','tip','1박 2일 일정이라면 8합 산장 1박 후 새벽 등정 → 오전 하산이 표준입니다.'),
   ],
   'tips': [
     ('backpack','준비물',['방풍·방한 의류','헤드랜턴','물 2.5L 이상+행동식','무릎 보호대·스틱']),
     ('book','예약·요금',['통행료 4,000엔(현장 지불)','산장 숙박 시 별도 예약','하산 버스 막차 확인']),
     ('warning','주의',['최장·최대 표고차 루트','체력 저하 시 이탈 계획','오후 기상 악화']),
   ],
   'map_note': '최장·최대 표고차 체력전 코스', 'map_start': '고텐바 신5합목', 'map_end': '정상 3,776m',
   'map_path': 'M80 350 C200 340, 320 300, 430 240 S620 110, 700 56',
   'map_nodes': [(80,350,10),(430,240,8),(700,56,12)],
   'cps': [
     ('고텐바 신5합목','출발점','badge-trailhead','해발 약 1,440m','누적 0km','주차장·매점·화장실'),
     ('6합','휴게','badge-shelter','해발 약 1,720m','누적 약 2.4km','산장'),
     ('7합','휴게','badge-shelter','해발 약 2,430m','누적 약 4.8km','산장·음수대'),
     ('8합','산장 지대','badge-shelter','해발 약 2,890m','누적 약 7.3km','산장군'),
     ('정상(켄가미네)','봉우리','badge-summit','해발 3,776m','누적 약 10.5km','오쿠미야 신사'),
   ],
  },
 ],
 'en': [
  {
   'id': 'beginner', 'color': 'green', 'hex': '#6a7d4c', 'level': 'Beginner',
   'name': 'Yoshida Trail 2-Day Course',
   'sub': 'Fuji-Subaru Line 5th Station → overnight at an 8th-station hut → dawn summit → back down · about 13.6 km round trip · ascent 5–7 h',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Round trip','~13.6 km') + pill('clock','Ascent time','5–7 h') + pill('location','5th Station','~2,300 m') + pill_meter('Difficulty',3,'medium') + pill('star','Season','Jul 1–Sep 10') + pill('location','Permit','4,000 yen'),
   'flow': ['Fuji-Subaru Line 5th St. (~2,300 m)','Overnight at 8th-station hut (~3,400 m)','Kengamine 3,776 m','Descend to trailhead'],
   'elev_label': 'Kengamine 3,776 m', 'elev_peak': (740, 48),
   'elev_path': 'M20 190 C160 182, 280 164, 400 132 S580 84, 740 48',
   'desc': 'The most recommended standard course. Since 2025 the Yoshida Trail requires an online reservation with prepayment of the 4,000-yen toll on the official site, caps climbers at 4,000 per day, and closes its gate from 2 p.m. to 3 a.m. (hut guests excepted). The standard plan enters in the afternoon, sleeps at an 8th-station hut, and summits before dawn.',
   'segs': [
     ('Start','Fuji-Subaru Line 5th Station','0 km','~2,300 m','Start from the 5th station on the Fuji Subaru Line. Clear the gate after confirming your reservation and toll. Entry after 2 p.m. is in principle restricted.','20','tip','The direct bus from Shinjuku (about 2 h 25 m) books out early in peak season — reserve ahead.'),
     ('1','5th → 8th station','~4.5 km','5–7 h','Climb past Satogomeya (6th) and Taishikan (7th) to the 8th-station hut cluster — the best-equipped trail for huts and shops.','52','warn','Check the gate closure (2 p.m.–3 a.m.) carefully when planning an afternoon entry.'),
     ('2','Hut night → dawn summit','~2.3 km','1.5–2.5 h','Set out at 2–3 a.m. with a headlamp and follow the crater rim to Kengamine (3,776 m) for sunrise, then visit Okumiya Shrine.','86','tip','Even in summer the summit is cold and windy — windproof, insulated layers are essential.'),
     ('Descent','Summit → 5th station','~6.8 km','3–4 h','Follow the Yoshida descent path back to the 5th station; the gravelly sections are slippery — take them slowly.','34','tip','Watch for the point where the ascent and descent trails split.'),
   ],
   'tips': [
     ('backpack','Gear',['Windproof & insulated clothing','Headlamp (spare batteries)','2 L water + high-calorie snacks','Cash for the huts']),
     ('book','Reservations',['Yoshida toll reservation (official site)','Hut booking required','4,000-yen toll prepaid']),
     ('warning','Cautions',['Gate closed 2 p.m.–3 a.m.','Sudden alpine weather / hypothermia','Peak-season crowds']),
   ],
   'map_note': 'Standard 2-day sunrise course', 'map_start': 'Fuji-Subaru Line 5th St.', 'map_end': 'Kengamine 3,776 m',
   'map_path': 'M92 330 C220 300, 330 250, 440 190 S600 100, 696 60',
   'map_nodes': [(92,330,10),(440,190,8),(696,60,12)],
   'cps': [
     ('Fuji-Subaru Line 5th St.','Starting Point','badge-trailhead','~2,300 m','0 km','Bus terminal · shops · restrooms'),
     ('6th St. Satogomeya','Rest','badge-shelter','~2,390 m','~1.0 km','Hut · water'),
     ('7th St. Taishikan','Rest','badge-shelter','~2,720 m','~2.4 km','Hut · shop'),
     ('8th St. Taikansha','Hut cluster','badge-shelter','~3,020 m','~3.6 km','Huts · first-aid'),
     ('Kengamine (summit)','Summit','badge-summit','3,776 m','~6.8 km','Okumiya Shrine'),
   ],
  },
  {
   'id': 'intermediate', 'color': 'blue', 'hex': '#456e96', 'level': 'Intermediate',
   'name': 'Fujinomiya Trail Day Hike',
   'sub': 'Fujinomiya New 5th Station → summit round trip · about 8.6 km · ascent 4–5.5 h',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Round trip','~8.6 km') + pill('clock','Ascent time','4–5.5 h') + pill('location','New 5th St.','~2,400 m') + pill_meter('Difficulty',3,'medium') + pill('star','Season','Jul 10–Sep 10') + pill('location','Permit','4,000 yen'),
   'flow': ['Fujinomiya New 5th St. (~2,400 m)','Summit 3,776 m','Back down'],
   'elev_label': 'Summit 3,776 m', 'elev_peak': (740, 52),
   'elev_path': 'M20 172 C180 158, 320 128, 480 96 S660 66, 740 52',
   'desc': 'The shortest and fastest route, starting higher (about 2,400 m) than any other. The trade-off is a steep, exposed path, so a same-day round trip suits hikers with fitness and acclimatization. The Shizuoka-side trails run July 10 – September 10; the toll is collected on the trail.',
   'segs': [
     ('Start','Fujinomiya New 5th Station','0 km','~2,400 m','Start early from the Shizuoka-side trailhead and plan to descend before afternoon weather deteriorates.','18','tip','Allow 8–9 hours for the full round trip, and check your return bus first.'),
     ('1','5th → 8th station','~3.0 km','2.5–3.5 h','An easy start turns steep from mid-route. Volcanic gravel makes sturdy footwear important.','58','warn','The slope is steep and exposed — in rain or fog, descend rather than push on.'),
     ('2','8th → summit','~1.3 km','1.5–2 h','Follow the ridge to the summit; you can drop into the crater to Okumiya Shrine and climb back out.','86','tip','The crater detour adds time — budget it with your descent schedule.'),
     ('Descent','Summit → New 5th Station','~4.3 km','2–3 h','Descend the same trail; hard on the knees — poles help.','30','tip','Afternoon thunderstorms are common. Summit before noon, descend early.'),
   ],
   'tips': [
     ('backpack','Gear',['Windproof & insulated clothing','Headlamp','2 L+ water','Trekking poles']),
     ('book','Fees',['4,000-yen toll (paid on trail)','Separate hut booking if overnight','Check day-trip requirements']),
     ('warning','Cautions',['Steep, exposed sections','Afternoon storms','Altitude symptoms']),
   ],
   'map_note': 'Shortest trail with the highest start', 'map_start': 'Fujinomiya New 5th St.', 'map_end': 'Summit 3,776 m',
   'map_path': 'M100 336 C230 310, 350 260, 470 200 S640 96, 700 56',
   'map_nodes': [(100,336,10),(470,200,8),(700,56,12)],
   'cps': [
     ('Fujinomiya New 5th St.','Starting Point','badge-trailhead','~2,400 m','0 km','Bus · parking · shops'),
     ('6th Station','Rest','badge-shelter','~2,590 m','~1.1 km','Hut'),
     ('7th Station','Rest','badge-shelter','~2,780 m','~1.9 km','Hut · water'),
     ('8th Station','Hut cluster','badge-shelter','~3,100 m','~2.8 km','Huts'),
     ('Okumiya Shrine · Summit','Summit','badge-summit','3,776 m','~4.3 km','Shrine'),
   ],
  },
  {
   'id': 'advanced', 'color': 'red', 'hex': '#9f5845', 'level': 'Advanced',
   'name': 'Gotemba Trail 2-Day Course',
   'sub': 'Gotemba New 5th Station → summit → back · ascent ~10.5 km · official time ~8 h 40 m',
   'tab_overview': 'Overview', 'tab_route': 'Route', 'tab_map': 'Map', 'tab_tips': 'Tips',
   'h_flow': 'Course Flow', 'h_elev': 'Elevation Profile', 'h_route': 'Route by Section', 'h_map': 'Concept Map', 'h_cp': 'Checkpoints',
   'pills': pill('ruler','Round trip','~18.9 km') + pill('clock','Ascent time','~8 h 40 m') + pill('location','New 5th St.','~1,440 m') + pill_meter('Difficulty',5,'hard') + pill('star','Season','Jul 10–Sep 10') + pill('location','Permit','4,000 yen'),
   'flow': ['Gotemba New 5th St. (~1,440 m)','Ridge above 8th station','Summit 3,776 m','Descend to trailhead'],
   'elev_label': 'Summit 3,776 m', 'elev_peak': (740, 40),
   'elev_path': 'M20 200 C170 196, 300 180, 420 150 S600 92, 740 40',
   'desc': 'The longest route with the largest elevation gain (~2,300 m): an ascent of about 10.5 km in an officially estimated 8 h 40 m, and a descent of about 8.4 km in about 3 h 30 m. It is a long grind across wide volcanic erosion-control terrain — not recommended for beginners, and normally split over two days.',
   'segs': [
     ('Start','Gotemba New 5th Station','0 km','~1,440 m','Start from the southeast-side trailhead; the low starting elevation means preparing for heat and distance.','12','tip','Carry ample water and snacks and keep a low pace — this route rewards patience.'),
     ('1','5th → 7th station','~4.8 km','3–4 h','Long, straight stretches across the erosion-control terrain; note where the trail splits from Subashiri.','42','warn','Distance is deceptive here — budget time conservatively.'),
     ('2','7th → above 8th station','~3.2 km','3–4 h','Switchbacks begin and the grade steepens sharply; above the 8th station the trail merges toward the Yoshida–Subashiri ridges.','70','warn','If altitude symptoms appear, stop ascending immediately.'),
     ('Descent','Summit → trailhead','~8.4 km','~3 h 30 m','Descend the Gotemba descent path — its length makes knee braces practically mandatory.','28','tip','On a 2-day plan, the standard rhythm is a night at an 8th-station hut, a dawn summit, and a morning descent.'),
   ],
   'tips': [
     ('backpack','Gear',['Windproof & insulated clothing','Headlamp','2.5 L+ water + snacks','Knee braces & poles']),
     ('book','Fees',['4,000-yen toll (paid on trail)','Separate hut booking if overnight','Check the last descent bus']),
     ('warning','Cautions',['Longest route, biggest gain','Plan an exit if exhausted','Afternoon weather deterioration']),
   ],
   'map_note': 'Longest route, biggest endurance test', 'map_start': 'Gotemba New 5th St.', 'map_end': 'Summit 3,776 m',
   'map_path': 'M80 350 C200 340, 320 300, 430 240 S620 110, 700 56',
   'map_nodes': [(80,350,10),(430,240,8),(700,56,12)],
   'cps': [
     ('Gotemba New 5th St.','Starting Point','badge-trailhead','~1,440 m','0 km','Parking · shops · restrooms'),
     ('6th Station','Rest','badge-shelter','~1,720 m','~2.4 km','Hut'),
     ('7th Station','Rest','badge-shelter','~2,430 m','~4.8 km','Hut · water'),
     ('8th Station','Hut cluster','badge-shelter','~2,890 m','~7.3 km','Huts'),
     ('Summit (Kengamine)','Summit','badge-summit','3,776 m','~10.5 km','Okumiya Shrine'),
   ],
  },
 ],
}

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'ko'
    html = build(which)
    out = pathlib.Path('fuji-playbook.html') if which == 'ko' else pathlib.Path('en/fuji-playbook.html')
    out.write_text(html, encoding='utf-8')
    print(f'wrote {out} ({len(html.splitlines())} lines)')
