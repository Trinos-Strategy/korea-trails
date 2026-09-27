# -*- coding: utf-8 -*-
"""MT Trails 전 페이지 렌더 검증 파이프라인 (Playwright).

- 외부 http(s) 요청 차단(폰트 시스템 폴백·지도 타일 공백은 예상 동작) → 행 없음
- 페이지별: title·히어로 이미지 로드·심화 밴드 렌더·갤러리 로드·패널 수·순수 JS 콘솔 에러
- 스크린샷 /tmp/mt_visual/, 보고서 scratch/visual_report.json
실행: /tmp/pwenv/bin/python scratch/visual_pipeline.py
"""
import json, pathlib, re, sys, time
from concurrent.futures import ThreadPoolExecutor

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHOTS = pathlib.Path('/tmp/mt_visual')
SHOTS.mkdir(exist_ok=True)
REPORT = ROOT / 'scratch' / 'visual_report.json'

CHECK_JS = """() => {
  const isPb = location.href.includes('playbook');
  const hero = document.querySelector('img.hero-img, img.hero-bg-img');
  // 렌더러는 마운트 div를 .deep-info-band 섹션으로 치환한다 — 렌더 결과를 검사한다.
  const di = document.querySelector('.deep-info-band');
  const gimgs = [...document.querySelectorAll('.gallery-img')];
  const panels = document.querySelectorAll('.panel, .course-panel').length;
  return {
    title: document.title || '',
    hero: !isPb ? 'skip' : (hero ? (hero.naturalWidth > 0 ? 'loaded' : 'NOT-LOADED') : 'NO-ELEMENT'),
    deepInfo: !isPb ? 'skip' : (di ? 'rendered' : 'NOT-RENDERED'),
    gallery: gimgs.length ? `${gimgs.filter(i => i.naturalWidth > 0).length}/${gimgs.length}` : 'skip',
    panels: isPb ? panels : 'skip',
  };
}"""


def pages():
    out = sorted(ROOT.glob('*.html')) + sorted((ROOT / 'en').glob('*.html'))
    return [p for p in out if p.name != 'index.html' or True], out


def one(browser_ctx_q, page_path):
    ctx = browser_ctx_q()
    pg = ctx.new_page()
    errors = []
    pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' and not re.search(r'net::ERR|Failed to load resource|Unsafe attempt to load URL|URL scheme "file"|Failed to fetch', m.text) else None)
    name = str(page_path.relative_to(ROOT)).replace('/', '_')
    rec = {'page': str(page_path.relative_to(ROOT))}
    t0 = time.time()
    try:
        pg.goto(page_path.resolve().as_uri(), wait_until='domcontentloaded', timeout=30000)
        pg.wait_for_timeout(1200)
        try:
            pg.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            pg.wait_for_timeout(600)
            pg.evaluate('window.scrollTo(0, 0)')
            pg.wait_for_timeout(200)
        except Exception:
            pass
        rec.update(pg.evaluate(CHECK_JS))
        pg.screenshot(path=str(SHOTS / f'{name}.png'), clip={'x': 0, 'y': 0, 'width': 1440, 'height': 2200})
        rec['shot'] = f'/tmp/mt_visual/{name}.png'
    except Exception as e:
        rec['error'] = f'{type(e).__name__}: {str(e)[:120]}'
    rec['js_errors'] = errors[:5]
    rec['secs'] = round(time.time() - t0, 1)
    pg.close()
    return rec


def main():
    _, all_pages = pages()
    print(f'대상 {len(all_pages)}페이지 (순차 실행)')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={'width': 1440, 'height': 2200})
        ctx.route('**/*', lambda route: route.continue_() if route.request.url.startswith('file://') else route.abort())
        holder = {}

        def ctx_q():
            return holder.setdefault('ctx', ctx)

        recs = [one(ctx_q, pp) for pp in all_pages]
        ctx.close()
        browser.close()

    fails = []
    for r in recs:
        why = []
        if r.get('error'):
            why.append(r['error'])
        if r.get('hero') in ('NOT-LOADED', 'NO-ELEMENT'):
            why.append(f"hero={r['hero']}")
        if r.get('deepInfo') == 'NOT-RENDERED':
            why.append('deepInfo=NOT-RENDERED')
        if r.get('js_errors'):
            why.append('js: ' + ' | '.join(r['js_errors']))
        g = str(r.get('gallery', 'skip'))
        if g != 'skip' and not g.startswith('4/'):
            why.append(f'gallery={g}')
        if str(r.get('panels')) not in ('3', 'skip'):
            why.append(f"panels={r.get('panels')}")
        if not r.get('title'):
            why.append('no-title')
        r['verdict'] = 'pass' if not why else 'fail'
        if why:
            fails.append((r['page'], why))
    REPORT.write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'pass {len(recs) - len(fails)} / fail {len(fails)} — 보고서 {REPORT}')
    for pg, why in fails:
        print('FAIL', pg, '|', '; '.join(why))
    print(f'스크린샷 {SHOTS} ({len(list(SHOTS.glob("*.png")))}장)')


if __name__ == '__main__':
    main()
