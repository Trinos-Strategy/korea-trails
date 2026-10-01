# -*- coding: utf-8 -*-
"""한국 100대 명산 2차(7산) 콘텐츠."""
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

import sys, json as _json, pathlib as _pl
_credits = _json.load(open(_pl.Path(__file__).parent / 'k100v2_credits.json'))
_meta = {list(c.keys())[0]: list(c.values())[0] for c in _credits}
CONTENT = {}
COURSES = {}
F7 = {
 'inwangsan': dict(ko_name='인왕산', en_name='Inwangsan', ko='인왕산', en='Inwangsan', alt='338m', region='경기', en_region='Gyeonggi', lat=37.5839, lng=126.9659,
   intro_ko='도성과 맞닿은 서울의 상징적 산. 인왕산 성곽길과 도심 전망이 압권입니다.',
   intro_en='An iconic Seoul mountain along the old city wall — fortress trail and skyline views.'),
 'gajisan': dict(ko_name='가지산', en_name='Gajisan', ko='가지산', en='Gajisan', alt='1,240m', region='경상', en_region='Gyeongsang', lat=35.3686, lng=129.0758,
   intro_ko='울산 최고봉. 통도사와 간월산 능선이 어우러진 영산입니다.',
   intro_en='Ulsan\'s highest peak — Tongdosa temple and the Ganwolsan ridgeline.'),
 'hwawangsan': dict(ko_name='화왕산', en_name='Hwawangsan', ko='화왕산', en='Hwawangsan', alt='928m', region='경상', en_region='Gyeongsang', lat=35.5983, lng=128.4233,
   intro_ko='영주의 진산. 봄철 진달래 군락과 비로봉 전망이 유명합니다.',
   intro_en='Yeongju\'s guardian mountain — famous for spring azalea colonies and Birobong views.'),
 'unjangsan': dict(ko_name='운장산', en_name='Unjangsan', ko='운장산', en='Unjangsan', alt='1,126m', region='전라', en_region='Jeolla', lat=35.6483, lng=127.2833,
   intro_ko='백두대간의 중요 산. 무등재·교룡산 능선과 천황봉이 연결됩니다.',
   intro_en='A key peak on the Baekdu-daegan — connecting to Gyoryong and the main watershed.'),
 'yeongchwisan': dict(ko_name='영취산', en_name='Yeongchwisan', ko='영취산', alt='1,090m', region='전라', en_region='Jeolla', lat=35.2350, lng=126.9500,
   intro_ko='화순의 진산. 사자봉·일출봉 능선과 수마애 조각이 유명합니다.',
   intro_en='Hwasun\'s guardian mountain — Saja and Ilchul peaks with stone Buddha carvings.'),
 'biseulsan': dict(ko_name='비슬산', en_name='Biseulsan', ko='비슬산', en='Biseulsan', alt='1,084m', region='경상', en_region='Gyeongsang', lat=35.7167, lng=128.5000,
   intro_ko='대구 남서쪽의 명산. 원시림과 아이스크림 도장놀이로 유명합니다.',
   intro_en='Southwest of Daegu — primeval forest and a famous ice-cream stamp tradition.'),
 'cheongnyangsan': dict(ko_name='청량산', en_name='Cheongnyangsan', ko='청량산', en='Cheongnyangsan', alt='1,093m', region='경상', en_region='Gyeongsang', lat=35.6333, lng=129.1167,
   intro_ko='울산·경주 경계의 명산. 청량사와 주능선이 어우러집니다.',
   intro_en='Between Ulsan and Gyeongju — Cheongnyangsa temple and the main ridgeline.'),
}
levels = [
    ('beginner', 'green', '#6a7d4c', 2, '초급' if L=='ko' else 'Beginner'),
    ('intermediate', 'blue', '#456e96', 3, '중급' if L=='ko' else 'Intermediate'),
    ('advanced', 'red', '#9f5845', 4, '고급' if L=='ko' else 'Advanced'),
]
for mid, d in F7.items():
    courses = []
    for i, (cid, color, hexc, meter, level) in enumerate(levels):
        flow = [d['intro_ko'][:6], '중간 지점', d['alt']+' 정상', '하산'] if L=='ko' else [d['intro_en'][:20], 'Midpoint', d['alt']+' summit', 'Descent']
        segs = [((('출' if j==0 else ('하' if j==3 else str(j)))), f'{w}', '—', '—', f'{"에서 출발합니다." if j==0 else "구간을 지나 이동합니다." if j<3 else "산행을 마무리합니다."}' if L=='ko' else ('Start here.' if j==0 else 'Pass through.'), 15+j*30, 'tip', d['intro_ko'][:30] if L=='ko' else d['intro_en'][:30]) for j, w in enumerate(flow)]
        cps = [(w, '출발점' if j==0 else ('종점' if j==3 else '경유'), 'badge-trailhead', '해발 —', '—', '—') for j, w in enumerate(flow)]
        courses.append(dict(id=cid, color=color, hex=hexc, level=level, meter=meter,
            name=(f'{d["ko_name"]} {["완만 코스","대표 코스","능선 종주"][i]}' if L=='ko' else f'{d["en_name"]} {["Easy Course","Main Course","Ridge Traverse"][i]}'),
            sub=f'약 {6+i*3}km · {3+i}시간' if L=='ko' else f'~{6+i*3} km · {3+i} h',
            tabs=['개요','경로 안내','지도','팁 &amp; 주의'] if L=='ko' else ['Overview','Route','Map','Tips'],
            pills=pill('ruler','거리' if L=='ko' else 'Distance',f'약 {6+i*3}km' if L=='ko' else f'~{6+i*3} km')+pill('clock','소요' if L=='ko' else 'Time',f'{3+i}h')+pill('location','정상' if L=='ko' else 'Summit',d['alt'])+pill_meter('난이도' if L=='ko' else 'Difficulty',meter,'medium' if meter<=3 else 'hard')+pill('star','100대 명산' if L=='ko' else '100 Mt. List','✓')+pill('location','허가' if L=='ko' else 'Permit','불필요' if L=='ko' else 'N/A'),
            h_flow='코스 흐름' if L=='ko' else 'Course Flow', h_elev='고도 프로파일' if L=='ko' else 'Elevation Profile',
            h_route='구간별 경로 안내' if L=='ko' else 'Route by Section', h_map='코스 개념도' if L=='ko' else 'Concept Map',
            h_cp='체크포인트 표' if L=='ko' else 'Checkpoints',
            flow=flow, elev_label=d['alt'], elev_path='M20 170 C180 160, 330 130, 480 100 S650 60, 740 46', elev_peak=(740,46),
            desc=d['intro_ko'] if L=='ko' else d['intro_en'],
            segs=segs, tips=[(tipcard('backpack','준비물' if L=='ko' else 'Gear',['트레킹화','물 1L','방풍 겉옷']) if False else ('backpack','준비물' if L=='ko' else 'Gear',['트레킹화','물 1L','방풍 겉옷'])),
                             (tipcard('book','입장' if L=='ko' else 'Entry',['허가 불필요','교통 최신 확인']) if False else ('book','입장' if L=='ko' else 'Entry',['허가 불필요','교통 최신 확인'])),
                             (tipcard('shield','주의' if L=='ko' else 'Cautions',['일몰 전 하산','산불 주의']) if False else ('shield','주의' if L=='ko' else 'Cautions',['일몰 전 하산','산불 주의']))],
            cps=cps, map_note='100대 명산 대표 코스' if L=='ko' else 'Representative course',
            map_start=flow[0], map_end=flow[-1],
            map_path='M110 335 C240 315, 350 265, 460 210 S620 95, 695 55', map_nodes=[(110,335,10),(460,210,8),(695,55,12)]))
    for lang in ('ko','en'):
        ko = lang=='ko'
        name = d['ko_name'] if ko else d['en_name']
        CONTENT.setdefault(mid, {})[lang] = dict(
            title=f'{name} 등산 플레이북' if ko else f'{d["en_name"]} Hiking Playbook',
            meta=(f'100대 명산 {d["ko_name"]}({d["alt"]}) 가이드. ' + d['intro_ko']) if ko else (f'Guide to {d["en_name"]} ({d["alt"]}), one of Korea\'s 100 Famous Mountains. ' + d['intro_en']),
            h1_card=d['ko_name'] if ko else d['en_name'], p_card=f'{name} · 100대 명산 {d["alt"]}' if ko else f'{d["en_name"]} · 100 Famous Mountains {d["alt"]}',
            hero_alt=d['intro_ko'] if ko else d['intro_en'],
            badge=f'{name} 플레이북' if ko else f'{d["en_name"]} Playbook',
            h1=f'{name} 등산 플레이북' if ko else f'{d["en_name"]} Hiking Playbook',
            hero_desc=d['intro_ko'] if ko else d['intro_en'],
            btn1=COURSES.get(mid,{}).get(lang,[{},{}])[0].get('name','') if COURSES.get(mid,{}).get(lang) else '',
            btn2=COURSES.get(mid,{}).get(lang,[{},{},{}])[1].get('name','') if COURSES.get(mid,{}).get(lang) else '',
            btn3=COURSES.get(mid,{}).get(lang,[{},{},{}])[2].get('name','') if COURSES.get(mid,{}).get(lang) else '',
            hero_photographer='', hero_url='',
            gal_title=f'{name}의 사계 &amp; 명소' if ko else f'{d["en_name"]} Four Seasons &amp; Attractions',
            lb_zoom='크게 보기' if ko else 'View larger',
            gallery=[(f'g{i}', f'{name} 풍경 {i}' if ko else f'{d["en_name"]} scenery {i}', 'Unsplash') for i in range(1,5)],
        )
        COURSES.setdefault(mid, {})[lang] = courses

# hero credits 주입
_credits = _json.load(open(_pl.Path(__file__).parent / 'k100v2_credits.json'))
_meta = {list(c.keys())[0]: list(c.values())[0] for c in _credits}
for _mid, _c in _meta.items():
    if _mid in CONTENT:
        for _lang in ('ko','en'):
            CONTENT[_mid][_lang]['hero_photographer'] = _c['hero']['photographer']
            CONTENT[_mid][_lang]['hero_url'] = _c['hero']['url']
            for _i, _g in _c['gallery'].items():
                _cap = f"Photo by &lt;a href='{_g['url']}' target='_blank' rel='noopener'&gt;{_g['photographer']}&lt;/a&gt; on Unsplash"
                _lst = list(CONTENT[_mid][_lang]['gallery'])
                _idx = int(_i[1]) - 1
                if _idx < len(_lst):
                    _lst[_idx] = (_lst[_idx][0], _lst[_idx][1], _cap)
                CONTENT[_mid][_lang]['gallery'] = tuple(_lst)
