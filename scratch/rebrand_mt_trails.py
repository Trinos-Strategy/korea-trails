#!/usr/bin/env python3
"""MT Trails 리브랜딩 일괄 적용 (STANDARD-DEEP-INFO.md §5).

- 사이트 HTML(root + en/)·브랜드 SVG의 서비스명 교체: Korea Trails → MT Trails
- 정본 도메인으로 URL 교체: trinos-strategy.github.io/korea-trails → mttrails.trinos.group
- 이력 문서(_*.md, LOGO-*, DESIGN-*, ORCHESTRATION-* 등)는 소급 수정하지 않는다.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

SITE_HTML = sorted(list(ROOT.glob("*.html")) + list(ROOT.glob("en/*.html")))
BRAND_SVGS = [
    ROOT / "assets/brand/logo.svg",
    ROOT / "assets/brand/favicon.svg",
    ROOT / "assets/brand/social-og.svg",
]
SITEMAP = ROOT / "sitemap.xml"

URL_OLD = "https://trinos-strategy.github.io/korea-trails"
URL_NEW = "https://mttrails.trinos.group"

changed = []

def apply(path, rules):
    text = path.read_text(encoding="utf-8")
    orig = text
    for old, new in rules:
        text = text.replace(old, new)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        changed.append(path.relative_to(ROOT).as_posix())

html_rules = [
    ("Korea Trails", "MT Trails"),
    (URL_OLD, URL_NEW),
]
for f in SITE_HTML:
    apply(f, html_rules)

svg_rules = [("Korea Trails", "MT Trails"), ("KOREA TRAILS", "MT TRAILS")]
for f in BRAND_SVGS:
    apply(f, svg_rules)

apply(SITEMAP, [(URL_OLD, URL_NEW)])

# index.html 정정: 스테일 필터 카운트 + 푸터 설명
apply(ROOT / "index.html", [
    ('<option value="done">완성됨 (17)</option>', '<option value="done">완성됨 (26)</option>'),
    ('<option value="pending">준비 중 (9)</option>', '<option value="pending">준비 중 (0)</option>'),
    ("MT Trails — 전국 등산 플레이북", "MT Trails — 한국·아시아 명산 등산 플레이북"),
    ('>경상 / Jeju<', '>경상 / 제주<'),
])

print(f"changed {len(changed)} files")
for c in changed:
    print(" -", c)

# 잔존 확인: 사이트 파일에 브랜드/구도메인 잔존이 없어야 한다
leftovers = []
for f in SITE_HTML + [SITEMAP] + BRAND_SVGS:
    text = f.read_text(encoding="utf-8")
    for needle in ("Korea Trails", "KOREA TRAILS", URL_OLD):
        if needle in text:
            leftovers.append((f.relative_to(ROOT).as_posix(), needle, text.count(needle)))
if leftovers:
    print("LEFTOVERS:")
    for l in leftovers:
        print(" !!", l)
else:
    print("no leftovers — rebrand clean")
