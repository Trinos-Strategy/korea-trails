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
assets/js/deep-info-data.js   ← 산별 데이터 (window.DEEP_INFO[id], 출처 주석 포함)
assets/js/deep-info.js        ← 공유 렌더러 (마운트 div를 찾아 섹션 생성, 템플릿 패밀리 무관 자체 스타일)
<플레이북>.html               ← ① 사진 갤러리 앞에 <div id="deep-info-root" data-mountain="<id>"></div>
                                ② </body> 앞에 deep-info-data.js + deep-info.js 스크립트 2줄
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
5. en/ 30페이지: 확정된 데이터 번역 라운드로 일괄 동기화.

## 5. 브랜딩 규칙 (2026-09 리브랜딩)

- 서비스명: **MT Trails** · 태그라인: **한국·아시아 명산 탐방 플레이북 / Korea & Asia Mountain Playbooks**
- 정본 도메인: `https://mttrails.trinos.group` (CNAME). `og:url`·sitemap·README에 정본 도메인 사용.
- 저장소명 `korea-trails`는 유지(링크·배포 경로 무변경). 로고 워드마크만 `MT TRAILS`로 교체.
- 이력 문서(`ORCHESTRATION-UPGRADE.md` 등)는 과거 기록이므로 소급 수정하지 않는다.
