# 🏔 MT Trails — 한국·아시아 명산 탐방 플레이북

한국과 아시아의 명산 코스를 탐색하고, 실전 플레이북으로 산행을 계획하는 **오픈소스 등산 아카이브**입니다.
인터랙티브 지도에서 산을 선택하면 체크포인트·고도 프로필·입산 예약·교통·안전 정보가 담긴 플레이북으로 이동합니다.

🌐 **라이브 사이트** → [https://mttrails.trinos.group](https://mttrails.trinos.group)

> 2026-09 리브랜딩: 기존 "Korea Trails"에서 커스텀 도메인과 일치하는 **MT Trails**로 명칭을 변경했습니다.
> 저장소명(`korea-trails`)은 배포 경로 안정성을 위해 유지합니다. 리브랜딩·심화 표준 전문: [`STANDARD-DEEP-INFO.md`](./STANDARD-DEEP-INFO.md)

---

## ✨ 주요 기능

- 🗺 **인터랙티브 월드 맵** — Leaflet 기반, 한국·대만 명산 마커와 플레이북 바로가기
- 📖 **등산 플레이북 72종** — 코스별 체크포인트, 고도 프로필, 구간 난이도, 실사 지도
- 🧭 **심화 탐방 정보** — 입산·예약(국내 탐방로 예약제/해외 입산허가), 교통, 숙박, 안전·비상연락 (`STANDARD-DEEP-INFO.md` 표준)
- 🔍 **검색·필터·정렬** — 지역/난이도/플레이북 상태 필터와 고도·이름 정렬
- 🌐 **한국어/영어 이중 제공** — 모든 페이지의 `en/` 미러
- 🌙 **라이트/다크 모드** · 📱 모바일 반응형 · ⚡ 빌드리스 정적 사이트

---

## 📂 플레이북 현황 (72산)

| 지역 | 산 |
|---|---|
| 강원 | [설악산](./seoraksan-playbook.html) · [치악산](./chiaksan-playbook.html) · [오대산](./odaesan-playbook.html) · [태백산](./taebaeksan-playbook.html) · [소금강](./sogeumgang-playbook.html) · [계방산](./gyebangsan-playbook.html) · [두타산](./dutasan-playbook.html) | · [대암산](./daeamsan-playbook.html)
| 경기/서울 | [북한산](./bukhansan-playbook.html) · [도봉산](./dobongsan-playbook.html) · [명성산](./myeongseongsan-playbook.html) · [소요산](./soyosan-playbook.html) · [운악산](./unaksan-playbook.html) · [관악산](./gwanaksan-playbook.html) · [수락산](./suraksan-playbook.html) · [청계산](./cheonggyesan-playbook.html) · [아차산](./achasan-playbook.html) · [인왕산](./inwangsan-playbook.html) · [안산](./ansan-playbook.html) · [불알산](./bulsan-playbook.html) · [용문산](./yongmunsan-playbook.html) · [왕관산](./wanggwan-playbook.html) · [유명산](./yumyeongsan-playbook.html) | · [감악산](./gamaksan-playbook.html)
| 충청 | [소백산](./sobaeksan-playbook.html) · [계룡산](./gyeryongsan-playbook.html) · [민주지산](./minjusan-playbook.html) · [식장산](./sikjangsan-playbook.html) · [월악산](./woraksan-playbook.html) · [속리산](./songnisan-playbook.html) · [희양산](./heuiyangsan-playbook.html) · [청태산](./cheongtaesan-playbook.html) |
| 전라 | [지리산](./jirisan-playbook.html) · [내장산](./naejangsan-playbook.html) · [덕유산](./deogyusan-playbook.html) · [월출산](./wolchulsan-playbook.html) · [무등산](./mudeungsan-playbook.html) · [두륜산](./duryunsan-playbook.html) · [대둔산](./daedunsan-playbook.html) · [마이산](./maisan-playbook.html) · [운장산](./unjangsan-playbook.html) · [영취산](./yeongchwisan-playbook.html) · [백암산](./baekamsan-playbook.html) | · [백운산](./baegunsan-playbook.html)
| 경상/제주 | [가야산](./gayasan-playbook.html) · [주왕산](./juwangsan-playbook.html) · [한라산](./hallasan-playbook.html) · [금정산](./geumjeongsan-playbook.html) · [팔공산](./palgongsan-playbook.html) · [운문산](./unmunsan-playbook.html) · [가지산](./gajisan-playbook.html) · [화왕산](./hwawangsan-playbook.html) · [비슬산](./biseulsan-playbook.html) · [청량산](./cheongnyangsan-playbook.html) · [남산(경주)](./namsan-playbook.html) | · [신불산](./sinbulsan-playbook.html)
| 인천 | [마니산](./manisan-playbook.html) |
| 대만 | [위산(玉山, 3,952m)](./yushan-playbook.html) · [설산(雪山, 3,886m)](./xueshan-playbook.html) · [양명산(陽明山)](./yangmingshan-playbook.html) · [아리산(阿里山, 2,663m)](./alishan-playbook.html) |
| 일본 | [후지산(富士山, 3,776m)](./fuji-playbook.html) · [타테야마(立山, 3,003m)](./tateyama-playbook.html) |
| 중국 | [황산(黃山, 1,864m)](./huangshan-playbook.html) · [타이산(泰山, 1,545m)](./taishan-playbook.html) |
| 베트남 | [판시판(3,143m)](./fansipan-playbook.html) |
| 말레이시아 | [킨리산(4,095m)](./kinabalu-playbook.html) |
| 인도네시아 | [라위니(3,726m)](./rinjani-playbook.html) |
| 네팔 | [푼힐(3,210m)](./poonhill-playbook.html) | · [에베레스트 BC](./ebc-playbook.html) · [안나푸르나 서킷](./act-playbook.html) · [랑탕 밸리](./langtang-playbook.html)

테마 페이지: [사이클링 코스](./cycling.html) · [인터랙티브 지도](./map.html) · [사이트맵](./sitemap.html)

**히말라야 카테고리** — 일반인이 도전할 수 있는 히말라야 트레킹(EBC·안나푸르나 서킷·랑탕 밸리)을 추가했습니다.

**로드맵** — 다음 확장 대상: 한국 100대 명산 미소개 산(순차 확장). 표준·확장 절차는 [`STANDARD-DEEP-INFO.md`](./STANDARD-DEEP-INFO.md) §4를 따릅니다.

---

## 🤝 기여 방법

1. 이 저장소를 **Fork**합니다.
2. `your-mountain-playbook.html`을 추가하고(기존 플레이북 구조를 템플릿으로 사용), `index.html`의 `MOUNTAINS` 배열에 데이터를 등록합니다.
3. 사실 기반 정보(거리·고도·교통·허가)는 **2개 이상의 권위 소스로 교차검증**하고, 출처를 `CREDITS.md` 또는 플레이북 심화 정보 출처 목록에 남깁니다.
4. **Pull Request**를 보냅니다. (main 직접 푸시 금지, 산 1개 = 1 PR 권장)

---

## 🛠 기술 스택

- **순수 HTML/CSS/JavaScript** — 빌드 도구 없음, GitHub Pages + 커스텀 도메인 배포
- **Leaflet + Esri 위성 타일** (인터랙티브 맵), Lucide 아이콘
- **Noto Serif/Sans KR** · Satoshi/Cabinet Grotesk (Fontshare)
- 공유 디자인 시스템: `assets/css/design-system.css` + `assets/js/*`

## 📄 라이선스

- 본 사이트의 일부 등산 사진·트래킹 영상은 김도경(Dokyung Kim) 촬영·제작 저작물(CC BY-NC 4.0 준용)
- 스톡 사진·영상 출처는 [CREDITS.md](./CREDITS.md)에 기록

---

Made with ❤️ by [Dokyung Kim](https://youtube.com/@DK2560) · © 2026 MT Trails
