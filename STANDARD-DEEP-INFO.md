# MT Trails — 플레이북 심화 표준 v1 (Deep Info Band)

> **목적** — 기존 26개 플레이북(한국 23 + 대만 3)을 **동일한 심화 표준**으로 끌어올려, 이후 신규 산(일본·동남아·네팔 등) 확장 시 그대로 복제하는 **정본 템플릿**을 확립한다.
> **브랜드** — 2026-09 리브랜딩: 서비스명 **MT Trails**(커스텀 도메인 `mttrails.trinos.group`과 일치), 기존 Ridge Apex 골드 마크 계승.
> **선행 문서** — `ORCHESTRATION-UPGRADE.md`(마스터) · `MISSING-MOUNTAINS-RESEARCH.md`(사실 검증 게이트) · `SAMPLE-yangmingshan-upgrade.md`(교통 안내 선례).

---

## 1. 표준이 정하는 것

기존 플레이북의 코스·체크포인트·고도·팁 구조는 **그대로 유지**한다. 여기에 아래 **심화 정보 밴드(Deep Info Band)** 1개 섹션을 사진 갤러리 앞에 추가한다. 국산/해외산 모두 동일 4블록 + 국가별 확장 블록.

| 블록 | 한국 산 | 해외 산 |
|---|---|---|
| ① 입산·예약 | 탐방로 예약제·대피소 예약(국립공원공단 예약시스템) | 입산허가(入园/permit)·산장 예약·외국인 쿼터 |
| ② 교통 | 철도·고속버스·시내버스·셔틀, 주차장 | 공항→도시→들머리 3단 국제 이동 동선 |
| ③ 숙박 | 대피소(예약 창구·가격), 인근 숙박지 | 산장(bunk bed)·인근 온천/숙박지 |
| ④ 안전·비상연락 | 119·산악안전공단·통제시간 | 현지 비상전화(경찰/구급)·대사관 연락 권고 |
| ⑤(선택) 시즌·비고 | 개화·단풍·설경 시즌, 통제 구간 | 비자·통신(eSIM)·화폐·현금 사용 등 |

## 2. 사실 게이트 (불변 — `MISSING-MOUNTAINS-RESEARCH.md` §2 상속)

1. 밴드에 들어가는 **모든 수치·제도는 세션 내 2소스 교차검증** 또는 **사이트 기존 게재 사실의 재사용**만 허용한다.
2. 검증 못한 항목은 기재하지 않거나 「이용 전 공식 시간표 확인」 형태로 **명시적으로 일반화**한다.
3. 밴드 하단에 **정보 기준일(예: 2026-09 기준)**과 **출처 링크 목록**을 반드시 표기한다.
4. 노선·배차·요금·예약 창구는 변동 품목 — 연 1회(또는 제보 시) 갱신을 원칙으로 한다.

## 3. 기술 구조 (빌드리스 유지)

```
assets/js/deep-info-data.js     ← 산별 데이터·한국어 (window.DEEP_INFO[id], 출처 주석 포함)
assets/js/deep-info-data-en.js  ← 산별 데이터·영문 (window.DEEP_INFO_EN[id]) — 한국어 항목 갱신 시 같은 라운드에서 함께 갱신
assets/js/deep-info.js          ← 공유 렌더러 (<html lang>을 읽어 KO/EN 표를 자동 선택, 미보유 언어는 반대 표로 폴백)
<플레이북>.html                 ← ① 사진 갤러리 앞에 <div id="deep-info-root" data-mountain="<id>"></div>
                                ② </body> 앞에 deep-info(-data|-data-en).js + deep-info.js 스크립트 2줄
                                   (en/ 페이지는 ../assets/js/ 경로 + -data-en.js)
```

- 렌더러는 다크/라이트·반응형·a11y(figcaption/aria)를 자체 토큰(공용 토큰 없을 시 폴백색)으로 처리한다.
- JS 미로드 시 마운트 div는 빈 채로 남고 본문 코스 정보는 무손상 — graceful degradation.
- **en/ 페이지 동기화는 표준 확정 이후 별도 라운드**(본 표준 §5).

### 데이터 스키마

```js
window.DEEP_INFO['seoraksan'] = {
  updated: '2026-09 기준',
  sections: [
    { icon: 'book',  title: '입산·예약', items: [{ h: '흘림골 탐방로 예약제', body: '…', tag: '필수' }], links: [{ label: '국립공원공단 예약시스템', href: 'https://reservation.knps.or.kr' }] },
    { icon: 'bus',   title: '교통', items: […] },
    { icon: 'tent',  title: '숙박', items: […] },
    { icon: 'shield', title: '안전·비상연락', items: […] },
  ],
  sources: [{ label: '국립공원공단 예약시스템', href: 'https://res.knps.or.kr' }, …],
};
```

- `icon` 허용값(기존 spritesheet에 존재): `book·bus·tent·shield·phone·tip·season·mountain·location`.
- `tag` 허용값: `필수`(빨강 계열) / `권장`(골드 계열) / `참고`(중립).

## 4. 롤아웃 절차 (나머지 24산)

1. 파일럿 2산(설악산·위산) 렌더·사실 검수 → **표준 확정 게이트(사용자 승인)**.
2. 승인 후 산 1개 = 1커밋/PR. 리서치 데이터 먼저(`_orchestration/deep-<id>.json` 권장), 게이트 통과 후 `deep-info-data.js`에 데이터 추가 → 마운트 div 삽입.
3. 국내 23산은 예약제 대상 구간 유무(예: 지리산·한라산·북한산 등)에 따라 ①블록 내용만 달라지고 구조는 동일.
4. 대만 2산(설산·양명산)은 위산 패턴(허가·산장·국제동선)을 복제.
5. en/ 30페이지: ~~확정된 데이터 번역 라운드로 일괄 동기화~~ **완료 (2026-09)** — 26산 영문 데이터(`deep-info-data-en.js`)를 추가하고 렌더러가 `<html lang>`으로 KO/EN을 자동 선택한다. **운영 규칙: 한국어 항목을 고치면 같은 커밋에서 영문 항목도 고친다.**

## 5. 브랜딩 규칙 (2026-09 리브랜딩)

- 서비스명: **MT Trails** · 태그라인: **한국·아시아 명산 탐방 플레이북 / Korea & Asia Mountain Playbooks**
- 정본 도메인: `https://mttrails.trinos.group` (CNAME). `og:url`·sitemap·README에 정본 도메인 사용.
- 저장소명 `korea-trails`는 유지(링크·배포 경로 무변경). 로고 워드마크만 `MT TRAILS`로 교체.
- 이력 문서(`ORCHESTRATION-UPGRADE.md` 등)는 과거 기록이므로 소급 수정하지 않는다.

## 6. 동적 강화 섹션 (2026-09-27, PR #37)

공유 렌더러(`assets/js/deep-info.js`)가 밴드 삽입 후 두 카드를 **동적으로** 추가한다.
둘 다 실패 시 조용히 생략된다(오프라인·API 장애 무관 동작). 데이터 출처·라이선스는
`DATA-SOURCES.md`가 정본이다.

### 6.1 산악 날씨 카드 (전 플레이북)
- 브라우저가 Open-Meteo에 정상 좌표+고도(`window.DEEP_COORDS`)로 직접 조회(키 불필요, CC BY 4.0).
- 현재 기온·풍속·강수 + 3일 최저/최고/강수 + 일출·일몰. 카드 하단 속성 필수.
- KO/EN 라벨은 렌더러 L10N2가 `<html lang>`으로 선택.

### 6.2 실측 등산로 지도 카드 (트랙 보유 산만)
- `assets/data/tracks/<id>.json`이 존재하면 표출. OSM `route=hiking` relation의 실측
  geometry(≤260점 단순화, 하버사인 거리) + Leaflet 1.9.4 **지연 로드**(unpkg).
- 경로별 실측 km 범례 + 입구 마커 + OSM 타일 + `© OpenStreetMap contributors (ODbL)` 속성.
- 트랙 JSON에 `profile`(Open-Meteo Elevation 샘플 배열)이 있으면 SVG 고도 프로파일 병기.
- 파일 구성: `scratch/ov_batch.py`(수집) → `scratch/wk_d_profiles.py`(프로파일 첨부).

### 6.3 좌표 QA 게이트 (데이터 신규 반영 시)
게시 좌표 지점의 DEM 표고가 게시 표고와 ±250m 이상 차이 나면 좌표 오류 후보다.
OSM `natural=peak` 노드(표고 ±100m 일치)로 확정한다. 2026-09-27 기준 22산 적발·처리 이력은
QUALITY-UPGRADE.md §8 참조.
