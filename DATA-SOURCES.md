# DATA-SOURCES.md — 데이터 출처·라이선스 정본

MT Trails의 모든 외부 데이터는 이 문서에 출처·라이선스·갱신 방식을 남긴다. 사실 게이트
(SOP 2소스 원칙)와 마찬가지로, 데이터 게시에도 출처 표기가 기본이다.

## 1. 실시간 동적 데이터 (브라우저 직접 호출)

| 데이터 | 출처 | 라이선스 | 방식 |
|---|---|---|---|
| 산악 날씨·3일 예보·일출/일몰 | [Open-Meteo](https://open-meteo.com) | CC BY 4.0 | 플레이북 페이지에서 브라우저가 직접 호출(키 불필요). 정상 좌표+고도 파라미터. 실패 시 카드 조용히 미표출 |

- 호출 위치: `assets/js/deep-info.js` `initWeather()`
- 표시: deep-info 밴드 「산악 날씨」 카드 + 하단 `Open-Meteo (CC BY 4.0)` 속성

## 2. 실측 등산로 지도·고도 (사전 수집, 정적 서빙)

| 데이터 | 출처 | 라이선스 | 방식 |
|---|---|---|---|
| 등산로 트랙(경로·거리) | OpenStreetMap `route=hiking` relation | © OpenStreetMap contributors, **ODbL** | Overpass API로 정점 반경 8km(해외 15km) relation 수집 → 실측 geometry 거리 계산(하버사인) → ≤260점 단순화 → `assets/data/tracks/<id>.json` |
| 고도 프로파일 | Open-Meteo Elevation API (Copernicus DEM) | CC BY 4.0(데이터) | 트랙 경로 샘플 좌표의 표고 조회 → `profile` 배열로 트랙 JSON에 첨부 |
| 산 정점 좌표 QA | DEM 표고 교차검증 | — | 좌표 지점의 DEM 표고가 게시 표고와 ±250m 이상 차이 나면 좌표 재검증(2026-09-27 22산 적발) |

- 수집 스크립트: `scratch/ov_combined.py`(Overpass) · `scratch/wk_b_osm_tracks.py`
- 표시: deep-info 밴드 「실측 등산로 지도」 카드 + 하단 `© OpenStreetMap contributors (ODbL)` 속성
- 갱신: 필요 시 수집 스크립트 재실행(자동 갱신 없음 — 정적 사이트)

## 3. 코스 실측 데이터 (알레, 2026-09-27 수집)

| 데이터 | 출처 | 라이선스 | 방식 |
|---|---|---|---|
| 코스 목록·거리·소요·레벨·보행수·태그·주의 문구 | [alle.co.kr](https://www.alle.co.kr/mb/) 공개 페이지/AJAX | 사이트 이용약관 준수(비상업적 인용·출처 링크) | 14산·66코스 수집 → deep-info 「코스 실측」 섹션(13산, 본 사이트 보유 산만) |
| 코스 기점 GPS | 알레 코스 길찾기용 네이버 지도 경로 URL | — | URL 내 구면 Web Mercator 좌표를 WGS84로 디코딩(41코스) |

- 수집 스크립트: `scratch/alle_collect.py` · 데이터: `scratch/alle_data.json`
- 표시: 각 산 deep-info 출처 행에 알레 산 페이지 링크

## 4. 좌표·표고 정본 (2소스 교차검증)

| 데이터 | 출처 | 비고 |
|---|---|---|
| 산 정점 좌표(46산, 2026-09-27) | 위키백과 인포박스 DMS × Wikidata P625/en 위키 교차, 나무위키 좌표(노인봉·비로봉·가지산), OSM `natural=peak` 노드 | DEM 표고 QA 통과 좌표만 확정 |
| 표고 | 기존 게시값 + Wikidata P2044 교차 | 신불산 1,159→1,209m 정정(wd+문헌 2소스) |
| 검증 스크립트 | `scratch/coords_verify.py` · `scratch/elev_qa.json` | 재검증 가능 |

## 5. 기존 콘텐츠 출처 (요약)

- **심화 밴드(예약·교통·숙박·안전)**: 공공기관 공식 안내(국립공원공단 예약시스템·지자체·대만 林業署 등) — 각 산 엔트리의 sources 링크 참조
- **코스 설명**: 세션 리서치 2소스(공공기관 × 실측 기록) — QUALITY-UPGRADE.md §4~§7
- **사진**: Unsplash(+크레딧 표기), 실산 미보유 산은 PHOTO-ACCURACY.md 추적
- **지도 타일(트랙 카드)**: © OpenStreetMap contributors

## 6. 속성(attribution) 규칙

1. Open-Meteo: 카드 하단 `Open-Meteo (CC BY 4.0)` — 렌더러 자동
2. OpenStreetMap: 카드 하단 `© OpenStreetMap contributors (ODbL)` — 트랙 JSON attribution 필드(렌더러 자동)
3. 알레: deep-info sources 행 링크
4. 사진: 페이지 크레딧 + CREDITS.md
