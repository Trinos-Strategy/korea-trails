# -*- coding: utf-8 -*-
"""한국 100대 명산 1차(10산) 빌더 — 팩트 테이블 + 표준 문장 생성기.

사실 근거: 산림청 100대 명산 목록 포함 확인(forest.go.kr PDF × 나무위키, 2026-09
세션 검색). 표고·산 이름·대표 코스 구성은 공용 안정 사실. 버스 번호 등 변동 품목은
「이용 전 확인」 일반화. 갤러리 사진은 실산 미보유로 경험 중심 일반 사진 대체
(CREDITS.md 명시).
"""
import pathlib, re, sys

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

if __name__ == '__main__':
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    import importlib
    content = importlib.import_module('k100_content')
    CONTENT = content.CONTENT
    COURSES = content.COURSES
    mountain, lang = sys.argv[1], sys.argv[2]
    html = build(mountain, lang)
    out = pathlib.Path(f'{mountain}-playbook.html') if lang == 'ko' else pathlib.Path(f'en/{mountain}-playbook.html')
    out.write_text(html, encoding='utf-8')
    print(f'wrote {out} ({len(html.splitlines())} lines)')
