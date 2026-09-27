# -*- coding: utf-8 -*-
"""deep-info 패치 (PR #36 2트랙).

1) EN 파일 한국어 누출 수리 — h 67건 + ansan body 1건 (KO 항목 갱신 시 EN 미동기화 결함)
2) 「코스 실측」 섹션 신설 — alle.co.kr 실측(2026-09-27 수집) 13산 × KO/EN
   · 코스명·거리·소요·레벨·한 줄 성격·기점 GPS(네이버 지도 경로 기준 디코딩)
3) sources에 알레 산 페이지 링크 추가
"""
import json, pathlib, re

ROOT = pathlib.Path('/Users/mac/korea-trails')
KO_F = ROOT / 'assets/js/deep-info-data.js'
EN_F = ROOT / 'assets/js/deep-info-data-en.js'

# ── 1) EN h 필드 누출 수리 (유일 한글 문자열 → 전역 치환, EN 파일 내에 정당한 한글 h 없음) ──
H_FIX = {
    '입산 자유': 'Open access',
    '성곽 구간 통제': 'Fortress-wall closures',
    '지하철 접근': 'Subway access',
    '자가용': 'By car',
    '도심 산행': 'Urban hike',
    '비상 연락': 'Emergency call',
    '결빙 주의': 'Icy sections',
    '석남터널 들머리': 'Seoknam-tunnel trailhead',
    '통도사 권역': 'Tongdosa side',
    '양산·울산': 'Yangsan & Ulsan',
    '우천 주의': 'Wet-rock caution',
    '창녕 접근': 'Access from Changnyeong',
    '축제기 혼잡': 'Festival crowds',
    '부곡온천': 'Bugok Hot Springs',
    '군락 보호': 'Protect the colonies',
    '들머리 3종': 'Three trailheads',
    '고개 주차': 'Pass parking',
    '진안·완주': 'Jinan & Wanju',
    '겨울 결빙': 'Winter ice',
    '축제기 교통': 'Festival transit',
    '여수': 'Yeosu',
    '유가사 들머리': 'Yugasa trailhead',
    '주말 혼잡': 'Weekend crowds',
    '대구·달성': 'Daegu & Dalseong',
    '암반 하산': 'Rocky descent',
    '봉화 접근': 'Access from Bonghwa',
    '청량사 주차': 'Cheongnyangsa parking',
    '봉화·안동': 'Bonghwa & Andong',
    '기암 낙석': 'Rockfall caution',
    '지하철 최적': 'Subway is best',
    '무장애 자락길': 'Barrier-free trail',
    '야간 조명': 'Night lighting',
    '국립공원 구역': 'National park zone',
    '백양사·구암사': 'Baekyangsa & Guamsa',
    '대중교통': 'Public transit',
    '백양사·내장산': 'Baekyangsa & Naejangsan',
    '단풍철 혼잡': 'Autumn-foliage crowds',
    '용문사 관광단지': 'Yongmunsa tourist area',
    '용문·양평': 'Yongmun & Yangpyeong',
    '암능 주의': 'Exposed-ridge caution',
    '휴양림 요금': 'Recreational-forest fees',
    '휴양림 들머리': 'Recreational-forest trailhead',
    '휴양림·가평': 'Recreation forest & Gapyeong',
    '계곡 수위': 'Valley water levels',
}
BODY_FIX = {
    '서울 도심 어디서나 당일 산행입니다.': 'A same-day hike from anywhere in central Seoul.',
}

# ── 2) 코스 실측 섹션 (alle.co.kr 실측, 2026-09-27) ──
# (mid, mount_seq, [ (name_ko, name_en, km, time_ko, time_en, lvl_ko, lvl_en, desc_ko, desc_en, gps|None) ])
L = {'쉬움': 'Easy', '보통': 'Moderate', '약간 어려움': 'Moderate-hard', '어려움': 'Hard'}
COURSES = {
    'gwanaksan': (2, [
        ('사당역 사당능선', 'Sadang Station · Sadang ridge', '6.6km', '3시간 20분', '3 h 20 m', '보통',
         '사당역에서 연주대로 이어지는 시티뷰 능선 종주 — 초입 암릉 구간 주의, 주말 혼잡.',
         'City-view ridgeline from Sadang Station to Yeonjudaek — rocky start, busy on weekends.',
         (37.4749, 126.9815)),
        ('과천향교', 'Gwacheon Hyanggyo', '7.1km', '3시간 30분', '3 h 30 m', '보통',
         '과천향교에서 계곡을 따라 오르는 한적한 코스.',
         'A quieter valley-side ascent starting at Gwacheon Hyanggyo.',
         (37.4282, 126.9907)),
    ]),
    'bulsan': (4, [
        ('상계역', 'Sanggye Station', '4.4km', '2시간 20분', '2 h 20 m', '보통',
         '상계역에서 바로 시작하는 지하철 접근 코스.',
         'A subway-accessible course starting right at Sanggye Station.',
         (37.6609, 127.0738)),
        ('공릉동', 'Gungneung-dong', '6.3km', '3시간', '3 h', '보통',
         '한적한 둘레길을 걸어 정상을 도는 코스.',
         'A quiet loop trail that circles up to the summit.',
         (37.6609, 127.0738)),
        ('불암사', 'Bulamsa temple', '4.3km', '2시간 10분', '2 h 10 m', '보통',
         '불암사에서 정상까지 가장 빠른 최단 코스.',
         'The fastest short route to the summit from Bulamsa temple.',
         (37.6495, 127.1071)),
    ]),
    'suraksan': (5, [
        ('수락산역', 'Suraksan Station', '8km', '4시간', '4 h', '보통',
         '수락산역에서 바로 시작하는 접근성 최고 코스.',
         'The most accessible course, starting right at Suraksan Station.',
         (37.7005, 127.0551)),
        ('불암산역', 'Bulamsan Station', '7.6km', '4시간', '4 h', '보통',
         '4호선 불암산역에서 시작하는 코스.',
         'A course starting at Bulamsan Station on line 4.',
         (37.6712, 127.0798)),
    ]),
    'dobongsan': (6, [
        ('신선대', 'Seonsondae', '6.1km', '3시간', '3 h', '보통',
         '도봉산 대표 코스로 정상까지 가장 무난한 루트.',
         'Dobongsan\'s classic route — the most straightforward way up.',
         (37.6861, 127.0362)),
        ('우이암', 'Uiam rock', '5.4km', '2시간 40분', '2 h 40 m', '보통',
         '우이암 바위를 지나는 짧은 코스.',
         'A shorter course passing the Uiam rock formation.',
         (37.6753, 127.0252)),
        ('종주', 'Ridge traverse', '9.3km', '5시간', '5 h', '약간 어려움',
         '도봉팔봉을 도는 대표 종주 코스.',
         'The signature traverse over the eight Dobong peaks.',
         (37.7232, 127.0362)),
    ]),
    'bukhansan': (7, [
        ('백운대', 'Baegundae', '4.5km', '2시간 30분', '2 h 30 m', '보통',
         '북한산 최고봉 백운대로 가는 최단 코스.',
         'The shortest route to Baegundae, the highest point of Bukhansan.',
         (37.6582, 126.9911)),
        ('우이령길', 'Uiryeong-gil', '8.1km', '3시간 30분', '3 h 30 m', '쉬움',
         '한적하고 완만한 둘레길형 코스.',
         'A quiet, gentle valley-loop walk.',
         (37.6631, 127.0124)),
        ('의상능선', 'Uisang ridge', '9.5km', '5시간 30분', '5 h 30 m', '어려움',
         '암릉이 이어지는 대표 난코스.',
         'A signature hard route with continuous rocky ridgelines.',
         (37.6551, 126.9493)),
    ]),
    'achasan': (8, [
        ('광나루역', 'Gwangnaru Station', '6.5km', '3시간', '3 h', '쉬움',
         '하단·광나루 방면에서 오르는 입문 코스.',
         'An entry-level ascent from the Hadan–Gwangnaru side.',
         (37.5456, 127.1034)),
        ('용마산-아차산 종주', 'Yongmasan–Achasan traverse', '5.7km', '3시간', '3 h', '보통',
         '용마산을 거쳐 아차산으로 이어지는 도시뷰 종주.',
         'A city-view traverse from Yongmasan over to Achasan.',
         (37.5738, 127.0868)),
    ]),
    'inwangsan': (9, [
        ('기차바위', 'Gicha bawi (Train Rock)', '3.7km', '1시간 40분', '1 h 40 m', '보통',
         '인왕산 북쪽 기차바위를 도는 짧은 코스.',
         'A short loop around Train Rock on Inwangsan\'s north side.',
         (37.5756, 126.9656)),
        ('경복궁역', 'Gyeongbokgung Station', '4.2km', '2시간', '2 h', '보통',
         '야경으로 유명한 인왕산 대표 코스.',
         'The classic Inwangsan course, famed for its night views.',
         (37.5762, 126.9721)),
        ('인왕-북악 종주', 'Inwang–Bukak traverse', '8km', '3시간', '3 h', '약간 어려움',
         '인왕산에서 북악산으로 이어지는 능선 종주.',
         'A ridgeline traverse linking Inwangsan to Bukaksan.',
         (37.5776, 126.9612)),
    ]),
    'jirisan': (10, [
        ('바래봉', 'Baraebong', '13.7km', '6시간', '6 h', '보통',
         '천왕봉 서쪽 바래봉 방면 산행.',
         'A hike toward Baraebong, west of Cheonwangbong.',
         (35.4329, 127.5449)),
        ('성삼재-노고단-반야봉', 'Seongsamjae–Nogodan–Banyabong', '16.8km', '8시간 30분', '8 h 30 m', '약간 어려움',
         '노고단에서 반야봉까지 이어지는 능선 코스.',
         'A ridgeline walk from Nogodan on to Banyabong.',
         None),
        ('화엄사-대원사 종주', 'Hwaeomsa–Daeheungsa traverse', '17.8km', '9시간', '9 h', '어려움',
         '화엄사에서 대원사로 이어지는 남부 종주(화대종주).',
         'The southern traverse from Hwaeomsa to Daeheungsa temple.',
         None),
    ]),
    'seoraksan': (11, [
        ('울산바위', 'Ulsanbawi', '8km', '8시간', '8 h', '쉬움',
         '울산바위 탐방로를 도는 대표 코스.',
         'The classic loop taking in the Ulsanbawi trail.',
         (38.1727, 128.4949)),
        ('소공원-공룡능선', 'Small-park–Dinosaur ridge', '11.3km', '6시간 30분', '6 h 30 m', '약간 어려움',
         '공룡능선을 넘는 대표 능선 코스.',
         'The signature ridgeline crossing over Dinosaur Ridge.',
         (38.1727, 128.4948)),
        ('귀때기청봉', 'Gwittoegi–Cheongbong', '7.6km', '5시간', '5 h', '어려움',
         '설악 서북능선의 바윗길.',
         'Rocky terrain on Seorak\'s northwestern ridgeline.',
         (38.0974, 128.4063)),
    ]),
    'sobaeksan': (12, [
        ('어의곡-천동', 'Eoeegok–Cheondong', '12km', '6시간', '6 h', '어려움',
         '어의곡에서 천동으로 이어지는 대표 코스.',
         'The main course linking Eoeegok valley to Cheondong.',
         None),
        ('초암사-국망봉', 'Choamsa–Gukmangbong', '14.6km', '7시간 30분', '7 h 30 m', '어려움',
         '비로봉·국망봉을 잇는 코스.',
         'A course linking Birobong with Gukmangbong.',
         None),
        ('희방사-어의곡 종주', 'Hoibangsa–Eoeegok traverse', '17.8km', '9시간 30분', '9 h 30 m', '어려움',
         '희방사에서 어의곡으로 이어지는 종주.',
         'A long traverse from Hoibangsa temple down to Eoeegok.',
         None),
    ]),
    'songnisan': (13, [
        ('세조길', 'Sejo-gil', '8km', '3시간', '3 h', '쉬움',
         '세조가 걸었다는 치유의 숲길.',
         'A healing forest path said to have been walked by King Sejo.',
         None),
        ('법주사-문장대', 'Beopjusa–Munjangdae', '13.3km', '6시간', '6 h', '보통',
         '법주사에서 문장대로 오르는 대표 코스.',
         'The classic ascent from Beopjusa temple to Munjangdae.',
         None),
        ('화북-천왕봉', 'Habuk–Cheonwangbong', '13km', '7시간', '7 h', '어려움',
         '천왕봉까지 이어지는 능선 산행.',
         'A ridgeline hike continuing to Cheonwangbong.',
         None),
    ]),
    'odaesan': (14, [
        ('선재길', 'Seonjae-gil', '10.7km', '3시간', '3 h', '쉬움',
         '사계절 편하게 걷는 산림욕장형 코스.',
         'An easy, all-season forest-walk course.',
         None),
        ('노인봉', 'Noinbong', '7.7km', '3시간 30분', '3 h 30 m', '보통',
         '진고개 기점 노인봉 왕복 — 소금강 연계 최단 코스.',
         'A round trip to Noinbong from Jingogae — the shortest Sogeumgang-linked course.',
         None),
        ('비로봉', 'Birobong', '11.6km', '5시간 30분', '5 h 30 m', '보통',
         '사찰을 지나 오대산 최고봉 비로봉까지.',
         'Past mountain temples to Birobong, the highest peak of Odaesan.',
         None),
    ]),
    'mudeungsan': (15, [
        ('무등산옛길-증심사', 'Old Mudeung path–Jeungsimsa', '9.8km', '5시간 30분', '5 h 30 m', '보통',
         '옛길 정취를 걷는 코스.',
         'A course following the atmosphere of the old mountain path.',
         None),
        ('증심사-중봉', 'Jeungsimsa–Jungbong', '11.4km', '6시간', '6 h', '약간 어려움',
         '증심사에서 중봉 방면 대표 코스.',
         'The main route from Jeungsimsa temple toward Jungbong.',
         None),
        ('안양산-백마능선', 'Anyangsan–Baekma ridge', '12.7km', '7시간', '7 h', '어려움',
         '백마능선을 타는 도전형 코스.',
         'A demanding ride along the Baekma ridgeline.',
         None),
    ]),
}


def sec_ko(mid, seq, rows):
    items = []
    for (nk, ne, km, tk, te, lk, dk, de, gps) in rows:
        body = f'{km} · {tk} · {lk} — {dk}'
        if gps:
            body += f' 입구: {gps[0]}, {gps[1]}.'
        items.append("{h:'" + js(nk) + "',tag:'참고',body:'" + js(body) + "'}")
    return " {icon:'tip',title:'코스 실측',items:[" + ', '.join(items) + ']}'


def sec_en(mid, seq, rows):
    items = []
    for (nk, ne, km, tk, te, lk, dk, de, gps) in rows:
        body = f'{km} · {te} · {L[lk]} — {de}'
        if gps:
            body += f' Start: {gps[0]}, {gps[1]}.'
        items.append("{h:'" + js(ne) + "',tag:'Note',body:'" + js(body) + "'}")
    return " {icon:'tip',title:'Measured courses',items:[" + ', '.join(items) + ']}'


def js(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


def _entry_span(s, marker):
    i = s.find(marker)
    assert i >= 0, marker
    return i


def _find_bus(s, i):
    m = re.compile(r"\{\s*icon:\s*'bus',\s*title:\s*'(?:교통|Transport|Getting There)'").search(s, i)
    assert m, 'bus section not found after %d' % i
    return m.start()


def _sources_close(s, i):
    k = re.compile(r"sources:\s*\[").search(s, i)
    assert k, 'sources not found'
    d = 0
    for pos in range(s.find('[', k.start()), len(s)):
        c = s[pos]
        if c == '[':
            d += 1
        elif c == ']':
            d -= 1
            if d == 0:
                return pos
    raise AssertionError('unbalanced sources')


def patch_file(path, prefix, sec_fn, src_label):
    s = path.read_text(encoding='utf-8')
    n_sec = n_src = 0
    for mid, (seq, rows) in COURSES.items():
        marker = f"window.DEEP_INFO{'_EN' if prefix else ''}['{mid}']"
        i = _entry_span(s, marker)
        j = _find_bus(s, i)
        sec = sec_fn(mid, seq, rows)
        s = s[:j] + sec + ',' + s[j:]
        n_sec += 1
        e = _sources_close(s, i)
        href = f'https://www.alle.co.kr/mb/content/mount_view?seq={seq}'
        seg = s[s.find('sources', max(0, i - 20)):e]
        if href not in seg:
            s = s[:e] + ",{label:'" + src_label + "',href:'" + href + "'}" + s[e:]
            n_src += 1
    path.write_text(s, encoding='utf-8')
    return n_sec, n_src


def fix_leaks(path):
    s = path.read_text(encoding='utf-8')
    n = 0
    for ko, en in H_FIX.items():
        s2 = s.replace("h:'" + ko + "'", "h:'" + en + "'")
        if s2 != s:
            n += 1
        s = s2
    for ko, en in BODY_FIX.items():
        s2 = s.replace("body:'" + ko + "'", "body:'" + en + "'")
        if s2 != s:
            s = s2
            n += 1
    path.write_text(s, encoding='utf-8')
    return n


def residual_ko_h(path):
    s = path.read_text(encoding='utf-8')
    return [x for x in re.findall(r"h:'([^']*)'", s) if re.search(r'[가-힣]', x)]


def main():
    n_leak = fix_leaks(EN_F)
    print(f'EN 누출 수리: {n_leak} 패턴')
    n1 = patch_file(KO_F, False, sec_ko, '알레 코스 실측')
    n2 = patch_file(EN_F, True, sec_en, 'Alle course data')
    print(f'코스 실측 섹션: KO {n1[0]}산 + 출처 {n1[1]}건 / EN {n2[0]}산 + 출처 {n2[1]}건')
    residual = residual_ko_h(EN_F)
    print(f'EN h 잔존 한글: {len(residual)} {residual[:5]}')


if __name__ == '__main__':
    main()
