# Korea Trails 전면 업그레이드 — 멀티에이전트 오케스트레이션 설계서

> **목적** — `Dokyung KimK/korea-trails` 정적 사이트(index + 플레이북 22개, 명산 26개)의 디자인·UX·UI·그래픽을 전면 업그레이드하고, 모든 산에 **실제 사진(무료 스톡 API)** 을 도입한다.
> **실행 런타임** — Claude Code 서브에이전트(Task 도구 병렬 spawn).
> **범위** — 전체 26개 산 + index 랜딩.
> **이 문서의 사용법** — §11의 "마스터 킥오프 프롬프트"를 오케스트레이터(리드 Claude)에게 그대로 전달하면 된다. §7의 에이전트 프롬프트는 각 서브에이전트 spawn 시 `prompt` 인자로 복붙한다.

---

## 1. 미션 & 노스스타(North Star)

**한 문장 미션**: "방문자가 첫 화면에서 '이 산에 가고 싶다'고 느끼고, 플레이북 한 페이지로 실제 산행을 계획할 수 있는, 사진 중심의 프리미엄 등산 가이드로 격상한다."

**성공의 정의(측정 가능)**:

| 지표 | 현재(추정) | 목표 |
|---|---|---|
| 실제 사진 수 | 0장 | 산당 히어로 1 + 갤러리 3~5장 (총 130장+) |
| Lighthouse Performance (모바일) | 미측정 | ≥ 90 |
| Lighthouse Accessibility | 미측정 | ≥ 95 |
| 페이지당 이미지 전송량 | 0 | ≤ 1.2MB (lazy 제외 above-the-fold ≤ 400KB) |
| 라이선스 출처 기록 | 없음 | 100% (`CREDITS.md` + per-image manifest) |
| 깨진 링크 / 콘솔 에러 | 미상 | 0 |
| 다크/라이트·반응형 정합 | 유지 | 무손상 유지 |

---

## 2. 현황 스냅샷 (자동 감사 결과)

- **스택**: 순수 HTML/CSS/JS, 빌드 도구 없음, GitHub Pages 배포. → **빌드 파이프라인 도입 금지**가 핵심 제약.
- **디자인 시스템 존재**: `:root` CSS 변수(OKLCH 컬러, `--color-*`, `--space-*`, `--radius-*`, `--text-*` clamp 타이포), 라이트/다크 테마 토글, Fontshare(Satoshi·Cabinet Grotesk).
- **플레이북 템플릿 일관성 높음**: `hero`(badge+h1+p+course-selector) → 탭형 코스(beginner/intermediate/advanced) → SVG 맵(`map-svg`) → 고도/난이도 바 → 아코디언 → stat/tip 카드 → flow 노드.
- **사진 부재**: `<img>` 0개. 모든 시각요소가 SVG 그라디언트(`#advGrad`,`#begGrad`,`#intGrad`)로 생성됨.
- **index.html**: `MOUNTAINS[]` 배열(JS)로 카드 렌더. 한국 23 + 대만 3(위산·설산·양명산). `done:true` 16개.

> ⚠️ 리포지토리 표기 불일치 주의: 사용자가 준 URL은 `Trinos-Strategy/korea-trails`이나, 로컬 git remote는 `Dokyung KimK/korea-trails`. **배포 에이전트(A8)는 작업 시작 전 실제 remote/Pages 대상을 반드시 재확인**한다.

---

## 3. 불변 제약(Invariants) & 가드레일

모든 에이전트가 위반 금지하는 전역 규칙:

1. **빌드리스 유지** — npm/webpack/번들러 도입 금지. 결과물은 브라우저에서 파일 그대로 실행 가능해야 함.
2. **디자인 토큰 우선** — 신규 색·간격·폰트는 기존 `--color-*`/`--space-*` 토큰 재사용. 신규 토큰 추가 시 라이트+다크 양쪽 정의 필수.
3. **다크모드 무손상** — 모든 사진은 다크/라이트에서 가독성 확보(오버레이 그라디언트, 보더). 이미지 위 텍스트는 대비 AA 충족.
4. **사진 진위(authenticity)** — "그 산의 실제 사진"이어야 함. 검증 게이트(§8.4) 통과 전 배치 금지. 동명이산·외국 풍경 오삽입 금지.
5. **라이선스 컴플라이언스** — Unsplash/Pexels API TOS 준수. hotlink 금지(다운로드 후 셀프호스팅), 출처·작가·URL 기록, Unsplash는 download endpoint 트리거.
6. **성능 예산** — 반응형 이미지(`srcset`/`sizes`), `loading="lazy"`(히어로 제외), `decoding="async"`, WebP/AVIF 우선 + JPG 폴백, 적정 해상도 리사이즈.
7. **접근성** — 모든 이미지 의미 있는 `alt`(한/영), 키보드 포커스 유지, 모션 `prefers-reduced-motion` 존중.
8. **무회귀(no regression)** — 기존 작동 플레이북의 기능(탭·아코디언·테마토글)을 깨지 않는다. 변경은 **브랜치 + PR**로만.
9. **원자적 커밋** — 산 1개 = 의미 단위 1커밋. 대량 일괄 푸시 금지(롤백성 확보).

---

## 4. 오케스트레이션 토폴로지

```
                         ┌─────────────────────────────────┐
                         │   ORCHESTRATOR (리드 Claude)      │
                         │   - 계획·DAG·게이트·머지 결정      │
                         │   - 공유 아티팩트 소유            │
                         └───────────────┬─────────────────┘
                                         │
        ┌───────────┬───────────┬────────┼────────┬───────────┬───────────┐
        ▼           ▼           ▼        ▼        ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐┌────────┐┌─────────┐ ┌─────────┐ ┌─────────┐
   │A0 RECON │ │A1 ART   │ │A2 PHOTO ││A3 IMG  ││A4 UI    │ │A5 UX/IA │ │A6 GRAPHIC│
   │ 감사     │ │ 디렉터   │ │ 소싱     ││ 파이프 ││ 구현     │ │ a11y/perf│ │ SVG/로고 │
   └─────────┘ └─────────┘ └─────────┘└────────┘└─────────┘ └─────────┘ └─────────┘
        │           │           │        │        │           │           │
        └───────────┴───────────┴────────┴────────┴───────────┴───────────┘
                                         ▼
                              ┌────────────────────┐      ┌──────────────┐
                              │ A7 QA (적대적 검증) │ ───► │ A8 DEPLOY     │
                              │ 사진진위·a11y·perf  │ FAIL │ git/PR/Pages  │
                              └─────────┬──────────┘ 시   └──────────────┘
                                        │ 재작업 루프(해당 에이전트로 반송)
                                        └──────────────► (A2~A6)
```

**역할 분리 원칙**: 소싱(A2)·가공(A3)·배치(A4)를 분리해 책임 경계를 명확히 하고, 검증(A7)을 **독립 적대적** 에이전트로 두어 생산자와 분리한다(self-review 편향 제거).

---

## 5. 실행 단계 DAG & 게이트

| Phase | 내용 | 담당 | 병렬성 | 통과 게이트(Gate) |
|---|---|---|---|---|
| **P0 정찰** | 코드/토큰/템플릿 감사, 산 26개 인벤토리 작성 | A0 | 단독 | `audit.md` + `inventory.json` 생성 |
| **P1 방향설정** | 비주얼 업그레이드 스펙·아트디렉션·컴포넌트 계약 확정 | A1 (+A6 로고) | A1·A6 병렬 | `design-spec.md` 승인 |
| **P2 소싱** | 산별 사진 후보 검색·라이선스 수집 | A2 | **산 단위 병렬(배치 4~6)** | `photo-candidates.json` (산당 ≥ 8후보) |
| **P3 검증①** | 후보 사진 진위/품질 1차 필터 | A7 | A2와 파이프라인 | 산당 채택 5장 확정 |
| **P4 가공** | 다운로드·리사이즈·WebP·srcset·attribution | A3 | 산 단위 병렬 | `/assets/` 생성 + `image-manifest.json` |
| **P5 구현** | 히어로·갤러리·카드에 사진 통합 + UX/a11y | A4·A5 | 페이지 단위 병렬 | 페이지별 로컬 렌더 OK |
| **P6 검증②+배포** | 적대적 QA → 통과 시 PR·Pages 확인 | A7→A8 | 순차 | QA 리포트 GREEN → 머지 |

**게이트 규칙**: 각 게이트는 오케스트레이터가 산출 아티팩트의 스키마·완결성을 확인한 뒤 다음 Phase를 spawn한다. P3에서 후보 부족(채택 <3) 시 A2로 반송(쿼리 확장).

---

## 6. 공유 아티팩트 / 에이전트 간 계약

모든 에이전트는 `/_orchestration/` 디렉터리(작업 산출물, 배포 제외)와 `/assets/`(최종 이미지, 배포 포함)를 통해 비동기 협업한다. **에이전트는 서로 직접 대화하지 않고 파일 계약으로만 통신**한다.

```
korea-trails/
├── _orchestration/                 # 작업 메타(배포 시 .gitignore 가능, 단 CREDITS는 루트)
│   ├── audit.md                    # A0
│   ├── inventory.json              # A0 — 산 26개 정규화 메타
│   ├── design-spec.md              # A1 — 비주얼/컴포넌트 스펙
│   ├── photo-candidates.json       # A2 — 후보 풀
│   ├── photo-selected.json         # A7(P3) — 채택 확정
│   ├── image-manifest.json         # A3 — 최종 파일·attribution 매핑
│   └── qa-report.md                # A7(P6)
├── assets/
│   └── img/<mountain-id>/          # hero.webp, hero.jpg, g1..g5.webp, *.jpg
├── CREDITS.md                      # 루트 — 라이선스/작가 출처(배포 포함, 필수)
└── *.html
```

### 핵심 스키마

**`inventory.json`** (A0) — 산 1개 레코드:
```json
{
  "id": "seoraksan",
  "name_ko": "설악산", "name_en": "Seoraksan", "name_hanja": null,
  "region": "강원", "country": "KR",
  "altitude_m": 1708,
  "landmarks": ["대청봉","공룡능선","울산바위","비룡폭포","오색"],
  "search_terms": ["Seoraksan","Seoraksan National Park","대청봉","Ulsanbawi"],
  "file": "seoraksan-playbook.html", "done": true,
  "season_signature": "단풍·설경",
  "hero_present": false
}
```

**`photo-candidates.json`** (A2) — 후보 1개:
```json
{
  "mountain_id": "seoraksan",
  "source": "unsplash",
  "photo_id": "abc123",
  "url_full": "https://images.unsplash.com/...",
  "url_download_trigger": "https://api.unsplash.com/photos/abc123/download",
  "author": "Hong Gil-dong",
  "author_url": "https://unsplash.com/@hong",
  "license": "Unsplash License",
  "width": 4000, "height": 2667,
  "query_used": "Seoraksan National Park autumn",
  "geo_hint": "tagged Sokcho",
  "authenticity_confidence": 0.0
}
```

**`image-manifest.json`** (A3) — 최종 배치 1개:
```json
{
  "mountain_id": "seoraksan",
  "role": "hero",
  "files": {
    "avif": "assets/img/seoraksan/hero.avif",
    "webp": "assets/img/seoraksan/hero.webp",
    "jpg":  "assets/img/seoraksan/hero.jpg"
  },
  "widths": [640,1024,1600,2400],
  "alt_ko": "설악산 대청봉에서 바라본 가을 단풍 능선",
  "alt_en": "Autumn ridgeline viewed from Daecheongbong, Seoraksan",
  "credit": { "author": "Hong Gil-dong", "source": "Unsplash", "url": "https://unsplash.com/photos/abc123" }
}
```

---

## 7. 에이전트별 상세 프롬프트 (spawn용)

> 각 블록을 `Task(subagent_type="general-purpose", prompt=...)` 의 prompt로 사용. 공통 헤더(§3 불변 제약)를 모든 프롬프트 상단에 포함시킨다.

### A0 — RECON / 감사 에이전트
```
역할: Korea Trails 코드베이스 정찰관.
미션: 26개 산 전체의 정규화 메타데이터와 템플릿 구조 지도를 만든다.
작업:
1. index.html의 MOUNTAINS[] 배열을 파싱해 26개 산 레코드 추출.
2. 각 플레이북 HTML을 스캔해 hero/탭/SVG맵/아코디언 등 삽입 지점(anchor)을 식별.
3. 산별 landmark·계절 시그니처·영문/한자명·검색어 후보를 정리.
4. 디자인 토큰(--color-*, --space-*, --text-*) 전체 목록과 라이트/다크 매핑 추출.
산출물: _orchestration/audit.md (템플릿 해부 + 삽입지점 좌표),
        _orchestration/inventory.json (§6 스키마, 26개 전부).
완료기준: 26개 레코드 모두 search_terms ≥ 3개, file 경로 검증 완료, hero_present 플래그 정확.
금지: 파일 수정 금지(읽기/분석 전용).
```

### A1 — ART DIRECTOR / 비주얼 디렉터
```
역할: 사진 중심 프리미엄 가이드의 아트 디렉터.
미션: 사진 도입 후의 비주얼 언어와 컴포넌트 계약을 확정한다.
입력: _orchestration/audit.md, inventory.json, 기존 CSS 토큰.
작업:
1. 히어로 리디자인: 풀블리드 사진 + 그라디언트 오버레이(다크/라이트 양쪽 대비 AA) 위에
   기존 hero-badge/h1/course-selector 재배치. 토큰만 사용.
2. 신규 컴포넌트 스펙 정의: (a) 사진 갤러리(반응형 그리드 + 라이트박스, 무JS의존 fallback),
   (b) index 카드 썸네일 영역, (c) 사진 크레딧 캡션 컴포넌트.
3. 사진 처리 규칙: aspect-ratio, object-fit, 오버레이 그라디언트 토큰, 보더/라운드(--radius-*),
   포커스/호버 모션(prefers-reduced-motion 분기).
4. above-the-fold 성능 가이드(히어로 preload, 갤러리 lazy).
산출물: _orchestration/design-spec.md — 각 컴포넌트의 HTML 골격 + CSS(토큰 기반) + 사용예시.
완료기준: 모든 신규 CSS가 기존 토큰만 참조(하드코드 hex 0개), 다크/라이트 대비 명시,
        A4가 추가 결정 없이 복붙 구현 가능한 수준의 구체성.
```

### A2 — PHOTO SOURCING / 사진 소싱 에이전트  *(산 단위 병렬)*
```
역할: 무료 스톡(Unsplash·Pexels) 사진 헌터.
미션: 배정된 산들에 대해 진짜 그 산의 고품질 후보 사진을 모은다.
입력: inventory.json(배정 산 슬라이스), §8 쿼리 매트릭스.
도구: Unsplash API(/search/photos), Pexels API(/v1/search). (키는 환경변수/사용자 제공)
작업:
1. 산별 쿼리 매트릭스(영문 공식명 > 국립공원명 > 랜드마크 > 로마자, 대만은 한자 병행) 순차 실행.
2. 가로형·고해상도(≥1600px) 우선, 인물/광고/지도/일러스트 제외.
3. 산당 후보 ≥ 8장 수집, geo 태그/캡션으로 1차 진위 힌트 기록.
4. Unsplash 채택 시 download endpoint 트리거 의무 기록(가공 단계에서 호출).
산출물: _orchestration/photo-candidates.json (append, §6 스키마).
완료기준: 배정 전 산 후보 ≥ 8(부족 시 쿼리 확장·대체 소스 명시), 라이선스/작가/URL 100% 기록.
금지: hotlink 사용 금지, 임의 이미지 다운로드 금지(후보 메타만), 산과 무관 추정 이미지 제외.
```

### A3 — IMAGE PIPELINE / 가공 에이전트  *(산 단위 병렬)*
```
역할: 이미지 최적화 엔지니어.
미션: 채택 사진을 셀프호스팅용 반응형 자산으로 가공한다.
입력: photo-selected.json(A7 P3 확정분).
도구: bash(ImageMagick/cwebp/avifenc 또는 sharp-cli), 네트워크 다운로드.
작업:
1. 원본 다운로드(Unsplash는 download endpoint 선호출).
2. 리사이즈 폭 [640,1024,1600,2400] 생성, AVIF+WebP+JPG(폴백) 인코딩, 품질 ~80, 메타 strip.
3. 파일 규약 assets/img/<id>/{hero,g1..g5}.{avif,webp,jpg}.
4. alt 텍스트(한/영) 작성, credit과 함께 image-manifest.json 기록.
5. 누적 전송량 예산(§3) 위반 시 폭/품질 재조정.
산출물: assets/img/** , _orchestration/image-manifest.json, CREDITS.md 항목 append.
완료기준: 모든 채택분 3포맷·4폭 생성, manifest 스키마 충족, above-the-fold 히어로 ≤ 400KB.
```

### A4 — UI 구현 에이전트  *(페이지 단위 병렬)*
```
역할: 프론트엔드 구현자.
미션: design-spec.md의 컴포넌트를 실제 HTML/CSS에 통합한다.
입력: design-spec.md, image-manifest.json, 대상 플레이북/ index.html.
작업:
1. 각 플레이북 hero에 풀블리드 사진(<picture> avif/webp/jpg + srcset/sizes) + 오버레이 적용.
2. 갤러리 섹션 삽입(코스 섹션 사이 적정 위치), 라이트박스(경량·무외부의존).
3. index 카드에 썸네일 + lazy 로딩 추가, MOUNTAINS[]에 image 경로 필드 확장.
4. 크레딧 캡션 렌더, alt 주입.
산출물: 수정된 *.html (브랜치 커밋, 산 1개=1커밋).
완료기준: 로컬 렌더 시 사진 표시·반응형·다크모드 정상, 기존 탭/아코디언/테마 무손상.
금지: design-spec 외 임의 디자인 변경, 인라인 하드코드 색.
```

### A5 — UX / IA / 성능·접근성 에이전트
```
역할: UX·접근성·성능 가디언.
미션: 사진 도입으로 인한 UX/성능/a11y 영향을 정밀 보정한다.
작업:
1. index 검색/지역필터/난이도필터 UX 점검·개선(키보드·포커스링·aria).
2. 이미지 a11y: alt 적절성, 장식 이미지 alt="" 구분, 라이트박스 포커스 트랩·ESC.
3. 성능: preload/lazy/decoding 속성, CLS 방지(width/height·aspect-ratio), 폰트·이미지 우선순위.
4. prefers-reduced-motion·prefers-color-scheme 정합.
산출물: 패치(커밋) + _orchestration/ux-notes.md(변경·근거).
완료기준: 키보드만으로 전 동선 이동 가능, CLS<0.1 설계, A7 a11y 게이트 사전 충족.
```

### A6 — GRAPHIC / SVG·로고 에이전트  *(A1과 병렬)*
```
역할: 그래픽·아이코노그래피 담당.
미션: 사진과 조화되는 브랜드 그래픽으로 격상.
작업:
1. 로고 리파인(현 산능선 SVG 유지·개선), 파비콘/OG 이미지 생성.
2. SVG 맵·고도프로필·난이도바의 시각 톤을 신규 아트디렉션에 정렬(토큰 색).
3. 산별 OG/소셜 카드 템플릿(사진+제목) 생성 가이드.
산출물: assets/brand/** , 갱신 SVG, design-spec.md에 그래픽 섹션 append.
완료기준: 로고/파비콘/OG 세트 완비, SVG가 다크/라이트 토큰에 반응.
```

### A7 — QA / 적대적 검증 에이전트  *(P3 필터 + P6 최종)*
```
역할: 독립 적대적 검증관. 생산자 편을 들지 않는다. 통과보다 결함 발견이 임무.
P3(사진 진위 필터):
1. 각 후보를 산 랜드마크/지형/계절과 대조. 동명이산·외국풍경·스튜디오/실내·과보정 의심 제거.
2. geo 태그·캡션·시각 단서로 authenticity_confidence 산정, 산당 상위 5장 채택.
산출물: photo-selected.json (confidence·채택사유), 부족 시 A2 반송 지시.
P6(최종 게이트):
1. 라이선스: 모든 이미지가 CREDITS.md·manifest에 출처/작가/URL 기록되었는가, hotlink 없는가.
2. 성능: 페이지별 전송량 예산, 반응형 속성, lazy/preload 정확성(샘플 실측).
3. a11y: alt 유무·적절성, 키보드·대비 AA.
4. 무회귀: 탭/아코디언/테마토글/링크 동작, 콘솔 에러 0.
5. 진위 재확인(스팟체크 6산).
산출물: _orchestration/qa-report.md (항목별 PASS/FAIL + 증거 + 반송 대상 에이전트).
판정: 단 1개 FAIL이라도 전체 GATE=RED → 해당 에이전트 재작업. ALL GREEN만 A8 진행.
```

### A8 — DEPLOY 에이전트
```
역할: 릴리스 매니저.
작업:
1. 시작 시 git remote·GitHub Pages 대상 재확인(§2 불일치 주의).
2. 작업 브랜치 → PR 생성, 변경 요약·스크린샷·CREDITS 링크 첨부.
3. Pages 빌드/배포 후 라이브 URL 스모크 테스트(샘플 6페이지 렌더·이미지 200).
산출물: PR URL, 배포 확인 노트.
완료기준: PR 생성·CI 통과·라이브에서 이미지 정상 로드. main 직접 푸시 금지.
금지: QA GREEN 전 머지 금지.
```

---

## 8. 사진 소싱 파이프라인 상세

### 8.1 쿼리 매트릭스(우선순위)
산별로 다음 순서로 검색, 충분(≥8) 시 조기 종료:
1. `<EnglishName> National Park` (예: "Seoraksan National Park")
2. `<EnglishName> mountain Korea`
3. `<대표 랜드마크 영문/로마자>` (예: "Ulsanbawi", "Daecheongbong")
4. 한국어 원어(`설악산`) — Pexels/Unsplash 한글 인덱스 보조
5. 대만 3산은 **한자 병행**: 위산`玉山 Yushan`, 설산`雪山 Xueshan`, 양명산`陽明山 Yangmingshan`

### 8.2 채택 기준
가로형·≥1600px·풍경(능선/정상/계곡/단풍·설경)·자연광. 제외: 인물 클로즈업, 워터마크, 일러스트/지도, 실내, 과한 HDR.

### 8.3 라이선스·TOS 처리
- **Unsplash**: Unsplash License(무료·상업가능). 채택 시 `/photos/:id/download` **트리거 의무**, 작가 크레딧 권장→본 프로젝트는 필수 기록.
- **Pexels**: Pexels License(무료·상업가능, 크레딧 권장). 출처 기록.
- **공통**: hotlink 금지 → 다운로드 후 `assets/`에 셀프호스팅. `CREDITS.md`에 산별 작가·소스·URL 표기.
- API 키 부재 시 A2는 **사용자에게 키 요청** 후 진행(임의 스크래핑 금지).

### 8.4 진위 검증 게이트(중요)
오삽입(동명이산·외국 풍경)이 최대 리스크. A7 P3가 **랜드마크·지형·계절 시그니처 대조**로 필터. confidence<0.6은 탈락, 산당 신뢰 상위 5장만 채택. 애매하면 보수적으로 제외하고 A2에 재검색 요청.

---

## 9. 리스크 레지스터 & 가드레일

| # | 리스크 | 영향 | 완화 |
|---|---|---|---|
| R1 | 산과 무관한 사진 오삽입 | 신뢰도 치명 | A7 P3 진위게이트, 스팟체크 6산, confidence 임계 |
| R2 | 라이선스 위반/hotlink | 법적·차단 | 셀프호스팅, CREDITS 필수, Unsplash download 트리거 |
| R3 | 성능 회귀(이미지 과중) | 이탈·SEO | 전송량 예산, AVIF/WebP, srcset, lazy, A7 실측 |
| R4 | 다크모드 가독성 저하 | UX 손상 | 오버레이 토큰, 대비 AA, A1 양테마 명시 |
| R5 | 기존 기능 파손 | 회귀 | 브랜치/PR, 산1=커밋1, A7 무회귀 체크 |
| R6 | 리포 대상 혼선(Trinos vs Dokyung KimK) | 잘못 배포 | A8 착수 전 remote/Pages 재확인 |
| R7 | API 키/레이트리밋 | 진행 정체 | 키 사전확보, 배치 4~6 병렬 상한, 백오프 |
| R8 | 서브에이전트 산출 스키마 불일치 | 파이프 단절 | §6 스키마 강제, 게이트에서 검증 |

---

## 10. 검증 루프 & 합격 기준

- **이중 검증**: P3(소싱 직후 진위) + P6(배포 직전 종합). 생산 에이전트와 분리된 A7이 수행.
- **재작업 루프**: FAIL 항목은 원인 에이전트(A2~A6)로 반송, 최대 2라운드. 2라운드 후 잔존 FAIL은 오케스트레이터가 사용자에게 에스컬레이션.
- **최종 합격(Definition of Done)**:
  - [ ] 26산 전부 히어로 사진 + 갤러리 ≥3장, index 썸네일 완비
  - [ ] CREDITS.md·image-manifest.json 100% 정합
  - [ ] Lighthouse Perf≥90 / A11y≥95(샘플 6산 + index)
  - [ ] 콘솔 에러·깨진 링크 0, 다크/라이트·모바일 정상
  - [ ] PR 머지 + 라이브 스모크 통과

---

## 11. 마스터 킥오프 프롬프트 (오케스트레이터에게 복붙)

```
너는 Korea Trails 업그레이드 프로젝트의 ORCHESTRATOR다. 목표는 이 정적 사이트
(index + 플레이북, 명산 26개)의 디자인·UX·UI·그래픽을 전면 격상하고, 모든 산에
무료 스톡 API(Unsplash·Pexels)의 실제 사진을 도입하는 것이다. 동봉된
ORCHESTRATION-UPGRADE.md가 마스터 설계서다. 이를 단일 진실원천(SSOT)으로 삼는다.

운영 규칙:
1. §3 불변 제약을 모든 서브에이전트 프롬프트 상단에 항상 주입한다.
2. §5 DAG 순서로 진행하되, 명시된 Phase는 Task 도구로 서브에이전트를 병렬 spawn한다
   (P2/P4/P5는 산·페이지 단위 배치 4~6 병렬).
3. 에이전트 간 통신은 §6 공유 아티팩트 파일로만 한다. 각 Phase 종료 시 산출
   아티팩트의 스키마·완결성을 네가 직접 검증(게이트)한 뒤 다음 Phase를 연다.
4. A7(QA)은 독립 적대적 검증이다. FAIL 1건이라도 RED면 원인 에이전트로 반송한다.
5. 모든 변경은 브랜치+PR. main 직접 푸시 금지. 산 1개=의미커밋 1개.
6. API 키가 없으면 먼저 사용자에게 요청한다. 리포 remote가 모호하면(§2) 배포 전 재확인한다.

지금 P0부터 시작하라:
- 먼저 A0(RECON)을 spawn해 audit.md와 inventory.json을 생성한다.
- 산출물을 검증한 뒤 P1(A1 아트디렉터 + A6 그래픽)을 병렬 spawn한다.
- 이후 §5 표대로 P2→P6까지 게이트를 통과시키며 진행하고, 각 Phase 종료 시
  진행상황·게이트 판정·다음 단계를 1~2문장으로 보고하라.
진행 전, 전체 실행계획(Phase·병렬 배치·예상 산출물)을 먼저 요약해 승인받아라.
```

---

## 12. 부록 — 산별 검색 쿼리 매트릭스 (26)

A2가 그대로 사용. 형식: `id | 1차 쿼리 | 보조 랜드마크 쿼리`.

| id | 1차 쿼리 | 랜드마크/보조 |
|---|---|---|
| seoraksan | Seoraksan National Park | Ulsanbawi, Daecheongbong, autumn ridge |
| hallasan | Hallasan National Park Jeju | Baengnokdam crater, snow |
| jirisan | Jirisan National Park | Cheonwangbong, Nogodan sea of clouds |
| bukhansan | Bukhansan National Park Seoul | Baegundae granite peak |
| sobaeksan | Sobaeksan National Park | Birobong, royal azalea |
| gayasan | Gayasan National Park | Haeinsa, Sangwangbong |
| odaesan | Odaesan National Park | Birobong, Woljeongsa |
| naejangsan | Naejangsan National Park | autumn maple tunnel |
| chiaksan | Chiaksan National Park | Birobong |
| deogyusan | Deogyusan National Park | Hyangjeokbong, winter snow |
| gyeryongsan | Gyeryongsan National Park | Gwaneumbong, Gapsa |
| wolchulsan | Wolchulsan National Park | cloud bridge, rocky peaks |
| mudeungsan | Mudeungsan National Park Gwangju | Seoseokdae columnar joints |
| baekhaksan | Baekhaksan Yeoncheon Korea | ridge |
| duryunsan | Duryunsan Haenam | Garyeonbong, Daeheungsa |
| minjusan | Minjujisan Korea | Samdobong |
| sikjangsan | Sikjangsan Daejeon | city view summit |
| woraksan | Woraksan National Park | Yeongbong, Chungju lake |
| dobongsan | Dobongsan Seoul | Jaunbong, Manjangbong granite |
| soyosan | Soyosan Dongducheon | Jajaeam valley autumn |
| juwangsan | Juwangsan National Park | Jubang valley waterfall |
| myeongseongsan | Myeongseongsan Pocheon | silver grass, Sanjeong lake |
| taebaeksan | Taebaeksan National Park | Cheonjedan, yew trees snow |
| yushan | 玉山 Yushan Taiwan | Yushan main peak sunrise |
| xueshan | 雪山 Xueshan Taiwan | Holy Ridge, glacial cirque |
| yangmingshan | 陽明山 Yangmingshan Taiwan | Qixingshan crater, sulfur |

> 대만 3산은 한자+영문 병행 필수. 한국 산은 영문 공식 로마자 우선, 한글은 보조.

---

*Korea Trails 멀티에이전트 오케스트레이션 설계서 · v1.0*
