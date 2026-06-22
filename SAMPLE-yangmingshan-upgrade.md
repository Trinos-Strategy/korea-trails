# 샘플 파일럿 — 양명산: 실사 인터랙티브 지도 + 상세 대중교통 안내

> **성격** — `ORCHESTRATION-UPGRADE.md`(마스터 설계서)의 **신규 재사용 역량 2종을 단일 산(양명산)에 먼저 적용**해 검증하는 파일럿.
> **이 문서가 도입하는 두 역량** — ① **A‑MAP**(SVG 개념도 → Leaflet 실사 인터랙티브 지도) ② **A‑TRANSIT**(타이베이 출발 상세 대중교통 안내).
> **런타임** — Claude Code 서브에이전트(Task spawn). **산출물** — 프롬프팅 설계만(실행은 별도).
> **검증되면** — 두 역량을 마스터 DAG의 P5(구현) 단계에 정식 편입해 26개 산으로 확장.

---

## 1. 샘플 개요 — 왜 양명산인가

양명산은 파일럿에 최적이다.
- **대중교통 산행의 전형** — 자가용 없이 MRT+버스+공원 셔틀(108)로 들머리·하산지가 달라지는 환승형. 교통 안내의 가치가 가장 큰 산.
- **지도 업그레이드 효과 큼** — 현재 코스 개념도가 추상 SVG. 화산 지형·분기공·초원 등 실제 위성/지형이 결정적.
- **데이터가 이미 풍부** — 체크포인트 표·구간·고도가 3개 코스(초급/중급/고급)별로 정비됨 → 마커·폴리라인 변환 소스로 즉시 활용 가능.

**이 샘플이 증명할 것**: (a) 빌드리스로 실사 지도가 다크모드·반응형·성능 예산 안에서 동작하는가, (b) 교통 리서치가 출처 검증된 실용 정보로 구조화되는가, (c) **템플릿이 산마다 달라도** 에이전트가 견고하게 적응하는가.

---

## 2. ⚠️ 사전 발견 — 템플릿 분기(에이전트 필수 인지)

**양명산 플레이북은 다른 플레이북(예: seoraksan)과 마크업이 다르다.**

| 항목 | seoraksan류 | yangmingshan |
|---|---|---|
| 코스 컨테이너 | 탭형 `course-*` | `tabpane[data-pane]` |
| 지도 | `map-svg` | `div.card.map > svg[viewbox="0 0 760 420"]` |
| 토큰 | `--color-*` | `--surface2`/`--muted`/`--transition` |
| 테마 버튼 | `[data-theme-toggle]` | `#themeBtn` |
| 코스 수 | 3 탭 | **3개 독립 섹션**(초급/중급/고급) 각각 map 패널 보유 |
| 본문 잔재 | 없음 | `[web:553]` 류 인용 마커 잔존(정리 대상) |

➡ **전역 규칙**: 모든 에이전트는 **대상 파일을 먼저 정독해 실제 구조를 파악**한 뒤 작업한다. 다른 산의 클래스명을 가정하지 않는다. 이는 26개 확장 시에도 동일하게 적용되는 핵심 원칙이다(템플릿 다양성 내성).

---

## 3. 공통 불변 제약 (마스터 §3 상속 + 본 샘플 추가)

마스터 설계서 §3을 그대로 상속하되 다음을 추가한다:

- **지도 라이브러리는 CDN만** — Leaflet `unpkg`/`cdnjs` `<script>`/`<link>`. npm·번들 금지.
- **타일 API 키 불필요 소스 우선** — 키 없는 무료 타일 사용, 제공자 **attribution 표기 의무**.
- **JS 비활성/오프라인 폴백** — 지도 로드 실패 시 기존 SVG 개념도 또는 정적 안내가 보이도록 graceful degradation.
- **교통 정보는 출처 검증 필수** — 노선·요금·배차·막차는 변동. 공식 출처(양명산국립공원/타이베이시 공공운수) 우선, 갱신일 표기.
- **양명산 본문 `[web:xxx]` 잔재 제거**(A‑TRANSIT가 교통 섹션 신설 시 함께 정리, 단 사실 변경 금지).

---

## 4. A‑MAP — 실사 인터랙티브 지도 기술 스펙

### 4.1 기술 선택
- **Leaflet 1.9.x** (CDN). 경량·무빌드·모바일 제스처 지원.
- **베이스 레이어(키 불필요, 토글 제공)**:
  - 위성: **Esri World Imagery** (`https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`) — attribution: "Esri, Maxar, Earthstar Geographics".
  - 지형: **OpenTopoMap** (`https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png`) — attribution: "© OpenTopoMap (CC‑BY‑SA), © OpenStreetMap contributors".
  - 기본 표시는 **위성**(실사 요구), 레이어 컨트롤로 지형 전환.
- **오버레이**: 체크포인트 = `L.marker`/`circleMarker`(코스 색상), 경로 = `L.polyline`(코스별 색: 초급 `#4f7d4a`·중급 `#326f95`·고급 `#9d4f36` — 기존 SVG 색 계승), 정상·온천·버스정류장 아이콘 구분.
- **상호작용**: 마커 클릭 시 팝업(지점명·고도·특징 = 기존 체크포인트 표 데이터), `fitBounds`로 코스 전체 자동 프레이밍, 스크롤줌은 `scrollWheelZoom:false`+포커스 시 활성(페이지 스크롤 충돌 방지).

### 4.2 다크모드·반응형·성능·접근성
- 다크: 컨테이너 보더/그림자 토큰화, 지형 레이어에 약한 필터(선택), 위성은 그대로(가독 양호). 컨트롤 버튼 대비 AA.
- 반응형: 높이 `clamp(280px, 50vh, 460px)`, 모바일 단일 손가락 드래그 허용·핀치줌.
- 성능: Leaflet CSS/JS `defer`, 지도는 **해당 탭/섹션이 보일 때 init**(IntersectionObserver lazy), 타일 과요청 방지.
- 접근성: 지도 컨테이너 `role="application"` + `aria-label`, 마커 키보드 포커스, **지도 외 동등 정보(체크포인트 표) 유지**(지도는 보강이지 대체 아님), `prefers-reduced-motion` 시 팬 애니메이션 축소.

### 4.3 양명산 적용(3개 코스 각각)
초급(소유갱↔칠성산 주봉 왕복), 중급(+동봉→냉수갱), 고급(+몽환호→칭티엔강). 각 섹션의 `div.card.map`을 Leaflet 컨테이너로 교체하되 **기존 SVG는 `<noscript>`/폴백으로 보존**.

### 4.4 좌표 계약 — `map-config`(에이전트가 검증·확정)
각 체크포인트의 실제 위경도를 확정해 JSON으로 박는다(아래는 **시드 추정치, A‑MAP이 공식 지도로 검증**):
```json
{
  "mountain_id": "yangmingshan",
  "default_layer": "satellite",
  "points": {
    "xiaoyoukeng_소유갱":   {"lat": 25.1710, "lng": 121.5565, "alt_m": 805, "type": "trailhead/bus"},
    "qixing_main_주봉":     {"lat": 25.1762, "lng": 121.5645, "alt_m": 1120, "type": "summit"},
    "qixing_east_동봉":     {"lat": 25.1748, "lng": 121.5672, "alt_m": 1107, "type": "summit"},
    "menghuanchi_몽환호":   {"lat": 25.1715, "lng": 121.5708, "alt_m": 880, "type": "lake"},
    "lengshuikeng_냉수갱":  {"lat": 25.1620, "lng": 121.5730, "alt_m": 740, "type": "hotspring/bus"},
    "qingtiangang_칭티엔강":{"lat": 25.1680, "lng": 121.5665, "alt_m": 760, "type": "grassland/bus"}
  },
  "routes": {
    "beginner":     ["xiaoyoukeng_소유갱","qixing_main_주봉","xiaoyoukeng_소유갱"],
    "intermediate": ["xiaoyoukeng_소유갱","qixing_main_주봉","qixing_east_동봉","lengshuikeng_냉수갱"],
    "advanced":     ["xiaoyoukeng_소유갱","qixing_main_주봉","qixing_east_동봉","menghuanchi_몽환호","lengshuikeng_냉수갱","qingtiangang_칭티엔강"]
  }
}
```

---

## 5. A‑TRANSIT — 상세 대중교통 안내 스펙

### 5.1 출력 정보 구조(필수 포함 계층)
1. **공항→타이베이 시내** — 타오위안 공항 → MRT 공항선/버스 → 시내 환승 거점(타이베이역·젠탄/스린).
2. **시내→공원 진입** — 주 노선: **260**(타이베이역/스린), **紅5(R5)**(젠탄역), **小15**(젠탄역) → **양명산 버스터미널**. 소요·요금·배차.
3. **공원 내 이동(핵심)** — **108 공원 순환 셔틀**: 양명산터미널·방문자센터·소유갱·칠성산·냉수갱·칭티엔강·몽환호 등 정차. 배차(평일 30~40분/주말 20~30분), 요금(1회권/1일권), **막차 시각**.
4. **들머리 접근** — 코스별: 초급/중급/고급 모두 **소유갱(小油坑)** 하차 시작. 108로 소유갱까지.
5. **하산지→귀가** — 코스별 종점 상이: 초급=소유갱 복귀, 중급=냉수갱, 고급=칭티엔강 → 각 지점에서 108로 터미널 복귀 → 260/R5로 시내. **막차·소요 시간 역산 가이드**.
6. **결제·실무 팁** — 悠遊卡(EasyCard) 사용, 환승 할인, 주말 혼잡, 안개·강풍 시 운휴 가능성, 1일권 손익분기.

### 5.2 소스 우선순위(검증 의무)
1. **양명산국립공원 공식**(ymsnp.gov.tw — Bus Routes & Times) ← 1순위
2. 타이베이시 공공운수처/공식 버스 시간표(yunbus 등 실시간)
3. 보조: 여행 가이드(교차검증용, 단독 근거 금지)
→ **노선·요금·배차·막차는 갱신일과 함께 표기**하고, "출발 전 공식 확인" 고지 문구 삽입.

### 5.3 UI 표현
- 신규 섹션 "🚌 대중교통 상세 안내"를 각 코스 `tips` 위 또는 독립 섹션으로 추가(템플릿 클래스 재사용: `card`/`section-title`/`table-wrap`).
- **단계 카드 + 노선 테이블**(노선·구간·소요·요금·배차·막차) + **코스별 귀가 동선 요약** + **타임라인**(예: 09:00 젠탄역 → … → 16:30 막차).
- 기존 팁카드의 빈약한 "버스로 접근" 문구는 신규 섹션으로 대체/링크.

### 5.4 데이터 계약 — `transit.json`
```json
{
  "mountain_id": "yangmingshan",
  "verified_on": "2026-06-22",
  "sources": ["https://www.ymsnp.gov.tw/en/cp.aspx?n=18205", "..."],
  "to_city": [{"from":"Taoyuan Airport","via":"Airport MRT","to":"Taipei Main","time_min":40}],
  "city_to_terminal": [
    {"route":"260","board":"Taipei Main / Shilin","alight":"Yangmingshan Terminal","time_min":40,"fare":"EasyCard"},
    {"route":"紅5(R5)","board":"Jiantan MRT","alight":"Yangmingshan Terminal"},
    {"route":"小15","board":"Jiantan MRT","alight":"Xiaoyoukeng/Lengshuikeng"}
  ],
  "park_shuttle": {"route":"108","loop":true,"fare_single":"NT$15","fare_daypass":"NT$60",
    "headway_weekday":"30-40min","headway_weekend":"20-30min","last_bus":"~17:30(확인)",
    "stops":["Terminal","Visitor Center","Xiaoyoukeng","Qixingshan","Lengshuikeng","Qingtiangang","Menghuanchi"]},
  "return_by_course": {
    "beginner":"소유갱→108→터미널→260/R5→시내",
    "intermediate":"냉수갱→108→터미널→…",
    "advanced":"칭티엔강→108→터미널→…"
  }
}
```

---

## 6. 에이전트 spawn 프롬프트 (복붙용)

> 두 에이전트는 병렬 가능(서로 다른 산출물). 단 A‑MAP 좌표와 A‑TRANSIT 정류장명은 동일 지명 표기 규약 공유. 공통 헤더로 마스터 §3 + 본 문서 §3을 주입.

### A‑TRANSIT (먼저 또는 병렬)
```
역할: 양명산 대중교통 리서치·구조화 전문 에이전트.
미션: 타이베이 출발~공원 내 이동~코스별 귀가까지 실사용 가능한 대중교통 안내를 만든다.
작업:
1. 양명산국립공원 공식 버스 페이지를 1순위로, 타이베이 공공운수/실시간 시간표를 보조로 조사.
2. §5.1 6계층(공항→시내→공원진입→108셔틀→들머리→귀가)을 모두 채운다.
3. 노선/요금/배차/막차에 갱신일·출처 표기, 변동 가능 고지 삽입.
4. transit.json(§5.4)로 구조화하고, 코스별(초급/냉수갱/칭티엔강) 귀가 동선과 막차 역산 타임라인 작성.
검증: 모든 수치는 ≥2개 출처 교차확인, 단독 블로그 근거 금지. 불확실 항목은 "확인 필요"로 표기.
산출물: _orchestration/transit.json + transit-section.html(삽입용 마크업, 양명산 템플릿 클래스 사용).
금지: 추정 시간표를 확정처럼 단정, [web:xxx] 잔재를 그대로 두기.
```

### A‑MAP (병렬)
```
역할: Leaflet 실사 인터랙티브 지도 구현 에이전트.
미션: 양명산 3개 코스의 SVG 개념도를 위성/지형 실사 지도로 교체한다.
선행: 대상 파일(yangmingshan-playbook.html)을 정독해 실제 구조 확인(§2 템플릿 분기). 클래스명 가정 금지.
작업:
1. 체크포인트 실제 위경도를 공식 지도로 검증해 map-config(§4.4) 확정.
2. Leaflet(CDN) + Esri 위성/OpenTopoMap 지형 레이어 토글, attribution 표기.
3. 코스별 마커(고도·특징 팝업)+폴리라인(기존 색 계승), fitBounds 자동 프레이밍.
4. lazy init(IntersectionObserver), scrollWheelZoom 포커스 활성, 다크/반응형/a11y(§4.2).
5. 기존 SVG는 폴백으로 보존(JS 실패/ noscript 시 표시).
산출물: 수정된 yangmingshan-playbook.html(브랜치 커밋) + _orchestration/map-config.json.
완료기준: 3코스 지도 렌더·반응형·다크 정상, 폴백 동작, 콘솔 에러 0, 기존 탭/테마 무손상.
금지: 빌드 도구 도입, 키 필요한 타일, 체크포인트 표 삭제.
```

### QA 체크(독립 A7 적용)
```
1. 라이선스/Attribution: 타일 제공자 표기 존재, hotlink 정책 위반 없음.
2. 교통 정합: transit.json 6계층 완비, 막차·요금에 출처·갱신일, 코스별 귀가 동선 일치.
3. 지도: 3코스 모두 마커·경로 정확, 좌표가 실제 지형과 부합(스팟체크), 폴백 동작.
4. 성능/a11y: lazy init, CLS<0.1, 지도 aria, 키보드 접근, 대비 AA.
5. 무회귀: 탭/아코디언/테마토글/링크 정상, 콘솔 에러 0, [web:xxx] 잔재 제거 확인.
판정: FAIL 1건이라도 RED → 원인 에이전트 반송. ALL GREEN만 머지 후보.
```

---

## 7. 합격 기준 (샘플 Definition of Done)

- [ ] 양명산 3개 코스 모두 Leaflet 실사 지도(위성 기본+지형 토글), 마커·경로·팝업 정상
- [ ] JS 실패 시 폴백(기존 SVG/정적 안내) 표시, 콘솔 에러 0
- [ ] "🚌 대중교통 상세 안내" 섹션: 공항→시내→공원→108셔틀→들머리→코스별 귀가 전 계층 + 막차 타임라인
- [ ] 모든 교통 수치 출처·갱신일 표기, 공식 출처 1순위 교차검증
- [ ] 다크/라이트·모바일 정상, CLS<0.1, 지도/이미지 a11y 충족
- [ ] 타일 attribution 표기, 빌드리스 유지, 기존 기능 무손상
- [ ] `[web:xxx]` 잔재 제거(사실 불변)

---

## 8. 마스터 킥오프 프롬프트 (샘플 실행용, 오케스트레이터에게 복붙)

```
너는 Korea Trails '양명산 샘플 파일럿'의 ORCHESTRATOR다. 목표는 두 가지 신규 역량
(① Leaflet 실사 인터랙티브 지도, ② 타이베이 출발 상세 대중교통 안내)을 양명산 1개에
먼저 적용해 검증하는 것이다. SAMPLE-yangmingshan-upgrade.md를 단일 진실원천으로 삼는다.

규칙:
1. 모든 서브에이전트 프롬프트 상단에 마스터 §3 + 본 문서 §3 제약을 주입한다.
2. 착수 전 두 에이전트(A-TRANSIT, A-MAP)에게 'yangmingshan-playbook.html을 먼저 정독해
   실제 템플릿 구조를 확인하라'고 명시한다(§2 템플릿 분기 — 다른 산 클래스명 가정 금지).
3. A-TRANSIT와 A-MAP을 병렬 spawn한다(산출물 분리). 각자 transit.json / map-config.json을 남긴다.
4. 두 산출물이 나오면 A4(UI)가 transit-section.html과 Leaflet 코드를 실제 파일에 통합한다
   (브랜치+커밋, main 직접 푸시 금지).
5. 독립 A7로 §6 QA 체크를 돌린다. FAIL 1건이라도 RED면 원인 에이전트로 반송(최대 2라운드).
6. 교통 시간표·요금·막차는 공식 출처 1순위로 교차검증하고 갱신일·"출발 전 확인" 고지를 넣는다.
7. 지도 타일 키가 필요 없는 소스를 쓰되 attribution을 표기하고, JS 폴백을 보장한다.

진행 전, 전체 실행계획(병렬 배치·산출물·게이트)을 1~2문장으로 요약해 승인받아라.
승인되면 A-TRANSIT·A-MAP 병렬 spawn → 통합 → QA → (GREEN 시) PR 생성 순으로 진행하고,
각 단계 종료 시 결과를 짧게 보고하라.
```

---

## 9. 부록 — 검증된 양명산 교통 시드 (A‑TRANSIT 출발점)

> 아래는 공개 출처 기반 **시드 정보**. A‑TRANSIT는 이를 출발점으로 공식 사이트에서 **현행 확인** 후 확정한다(시간표 변동 가능).

- **시내→양명산 터미널**: 타이베이역/스린에서 **260**, 젠탄(Jiantan)역에서 **紅5(R5)** 또는 **小15**. 260 약 40분.
- **공원 셔틀 108**: 터미널 기점 **순환 노선**, 정차에 소유갱·칠성산·냉수갱·칭티엔강·몽환호 등 포함. 배차 평일 30~40분/주말 20~30분, **요금 1회 NT$15·1일권 NT$60**, 터미널 막차 약 17:30대(현행 확인 필요).
- **들머리**: 3개 코스 모두 **소유갱(小油坑)** 시작 → 108로 소유갱 하차.
- **결제**: 悠遊卡(EasyCard) 사용 권장.

**Sources:**
- [양명산국립공원 — Bus Routes & Times (공식)](https://www.ymsnp.gov.tw/en/cp.aspx?n=18205)
- [Route 108 Yangmingshan 시간표 (yunbus)](https://yunbus.tw/lite/en/route.php?id=TPE10822)
- [Taipei to Yangmingshan by Bus (Taiwan Obsessed)](https://www.taiwanobsessed.com/taipei-to-yangmingshan/)

---

*Korea Trails 샘플 파일럿 — 양명산 실사지도+교통 · v1.0 · `ORCHESTRATION-UPGRADE.md` 보조 문서*
