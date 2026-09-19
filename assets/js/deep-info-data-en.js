/* MT Trails — Deep Info Band data, English (STANDARD-DEEP-INFO.md §3 schema)
 *
 * English mirror of deep-info-data.js, for pages with <html lang="en">.
 * Fact gate (STANDARD-DEEP-INFO.md §2) applies unchanged: content is a faithful
 * translation of the Korean entries — same facts, same sources, no new claims.
 * When updating a Korean entry, update this English entry in the same round.
 */
window.DEEP_INFO_EN = window.DEEP_INFO_EN || {};

// ── Pilots ──

window.DEEP_INFO_EN['seoraksan'] = {
  updated: 'As of 2026-09',
  note: 'Korea-standard pilot',
  sections: [
    {
      icon: 'book', title: 'Permits & Reservations',
      items: [
        { h: 'Heullimgol trail reservation', tag: 'Required',
          body: 'The Seorak-dong → Baekundae section (Heullimgol) runs on a 5,000-person-per-day reservation system. Entry is by QR permit delivered via KakaoTalk or SMS.',
          links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
        { h: 'Shelter reservations', tag: 'Required',
          body: 'National-park shelters such as Socheong and Jungcheong require advance booking. Popular sections close out early, so apply with plenty of lead time.' },
        { h: 'Phone reservations & inquiries', tag: 'Note',
          body: 'Reservation call center 1670-9201 (weekdays 09:00–18:00), Seoraksan National Park office +82-33-636-7700.' },
      ],
      links: [{ label: 'Trail reservation information', href: 'https://res.knps.or.kr' }],
    },
    {
      icon: 'bus', title: 'Getting There',
      items: [
        { h: 'Seoul → Sokcho', tag: 'Recommended',
          body: 'Express bus from Dong Seoul Terminal to Sokcho. Trains on the new Donghae line to Sokcho Station are also an option — check the latest timetable before travel.' },
        { h: 'Sokcho → Seorak-dong', tag: 'Note',
          body: 'Local bus 7-1 runs from Sokcho to the Seorak-dong entrance. Roads congest in peak season, so start early.' },
        { h: 'Inner Seorak (Baekdamsa) access', tag: 'Required',
          body: 'Take the paid shuttle from the Yongdae-ri parking lot to Baekdamsa (about 20 minutes). Traverse routes start and finish at different points, so plan transport for both ends.' },
        { h: 'Parking', tag: 'Note',
          body: 'Seorak-dong and Osaek parking lots are paid and often congested in peak season. Public transport is recommended.' },
      ],
    },
    {
      icon: 'tent', title: 'Lodging',
      items: [
        { h: 'Shelters', tag: 'Required',
          body: 'In-mountain shelters such as Socheong operate by reservation; cooking is restricted. Check the rules after booking.' },
        { h: 'Nearby lodging', tag: 'Note',
          body: 'Hotels and restaurants cluster in Seorak-dong and Sokcho city. For a pre-dawn start, stay in Seorak-dong.' },
      ],
    },
    {
      icon: 'shield', title: 'Safety & Emergency',
      items: [
        { h: 'Emergency contact', tag: 'Required',
          body: 'Call 119 for mountain rescue. Aim to descend two hours before sunset.' },
        { h: 'Access cutoff times', tag: 'Required',
          body: 'The Gongnyongneung ridge entrance requires arrival before 13:00 (April–October) or 10:00 in winter. Turn back immediately in bad weather.' },
        { h: 'Weather check', tag: 'Recommended',
          body: 'Check the Korea Meteorological Administration mountain forecast before and during the hike, and carry crampons for icy winter sections.' },
      ],
    },
  ],
  sources: [
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
    { label: 'korea.kr — Heullimgol reservation field report', href: 'https://www.korea.kr/news/reporterView.do?newsId=148906341' },
    { label: 'Details published in this site\'s Seoraksan playbook', href: 'seoraksan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['yushan'] = {
  updated: 'As of 2026-09',
  note: 'International-standard pilot',
  sections: [
    {
      icon: 'book', title: 'Permits',
      items: [
        { h: 'Unified permit application', tag: 'Required',
          body: 'Yushan entry combines the national-park entry permit and the police mountain-entry permit in one application on Taiwan\'s unified hiking portal. Climbing resumes and a planned itinerary with timings must be submitted.',
          links: [{ label: 'hike.taiwan.gov.tw', href: 'https://hike.taiwan.gov.tw' }] },
        { h: 'General application (lottery)', tag: 'Required',
          body: 'Apply roughly 1–2 months before your target date for the lottery draw. Weekends and peak season are highly competitive; unsuccessful applicants can re-apply for remaining slots closer to the date.' },
        { h: 'Foreign-passport priority quota', tag: 'Recommended',
          body: 'A dedicated quota for foreign-passport holders assigns 24 Paiyun Lodge beds per day, first come first served (no lottery). Apply 4 months to 35 days before entry and select "Paiyun Lodge Advanced Application".' },
        { h: 'Paiyun Lodge follow-up', tag: 'Required',
          body: 'After the permit is confirmed, contact the lodge separately to book meals and bedding. Sleeping quarters are shared dormitory bunks.' },
      ],
      links: [
        { label: 'Yushan National Park (official)', href: 'https://www.ysnp.gov.tw' },
        { label: 'Foreigner permit guide', href: 'https://braveontw.com/post/yushan-permit-foreigners' },
      ],
    },
    {
      icon: 'bus', title: 'International Transit',
      items: [
        { h: 'Incheon → Taipei', tag: 'Note',
          body: 'Direct flights from Incheon reach Taipei (Taoyuan or Songshan) in roughly two and a half hours; schedules vary by season.' },
        { h: 'Taipei → trailhead', tag: 'Recommended',
          body: 'Combine the high-speed rail (THSR), intercity buses, and local buses to reach Chiayi or the Lukou/Lugao hot-spring area, then continue to the Tataka trailhead. Timetables change by season — recheck after the permit is confirmed.' },
        { h: 'Trailhead access', tag: 'Note',
          body: 'The lower section of the Tataka trailhead road is private; visitors generally use the tourist shuttle or a chartered vehicle. Arrange transport with your party in advance.' },
      ],
    },
    {
      icon: 'tent', title: 'Lodging',
      items: [
        { h: 'Paiyun Lodge', tag: 'Required',
          body: 'The de-facto required stop for the 2-day main-peak itinerary (about 3,400 m). Beds are allocated together with the permit; meals are booked separately with the lodge.' },
        { h: 'Nearby lodging', tag: 'Note',
          body: 'Plenty of hotels in Chiayi city and the Lugao hot-spring area. A night at each end of the climb is a comfortable rhythm.' },
      ],
    },
    {
      icon: 'shield', title: 'Safety & Emergency',
      items: [
        { h: 'Local emergency numbers', tag: 'Required',
          body: 'Taiwan-wide: police 110, ambulance/fire 119. If altitude symptoms appear (headache, breathlessness), descend rather than push on.' },
        { h: 'Altitude preparation', tag: 'Recommended',
          body: 'The summit stands at 3,952 m — far colder than any Korean mountain. Carry ample insulation layers, water, and snacks, and pace the pre-dawn summit push.' },
        { h: 'Travel preparation', tag: 'Note',
          body: 'Travel insurance and connectivity (eSIM/roaming) are recommended. Share your itinerary with family or companions at home.' },
      ],
    },
  ],
  sources: [
    { label: 'Taiwan unified hiking application site', href: 'https://hike.taiwan.gov.tw' },
    { label: 'Yushan National Park (official)', href: 'https://www.ysnp.gov.tw' },
    { label: 'Paiyun Lodge overview (Wikipedia)', href: 'https://en.wikipedia.org/wiki/Paiyun_Lodge' },
    { label: 'Foreigner permit guide', href: 'https://taiwan-adventures.com/yushan-self-guided-hike-information' },
    { label: 'Details published in this site\'s Yushan playbook', href: 'yushan-playbook.html' },
  ],
};

// ── Gangwon · Gyeonggi ──

window.DEEP_INFO_EN['chiaksan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters and ranger-led programs at Chiaksan National Park are booked through the park service reservation system. Trail-reservation sections change from time to time — check before you go.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
      { h: 'Trail basics', tag: 'Note', body: 'Main routes start from the Guryongsa parking lot. Confirm your course at the visitor center before setting off.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Access', tag: 'Note', body: 'The Guryongsa parking lot is the main starting point. Local buses from Wonju can be infrequent — check routes and times before departure.' },
      { h: 'Parking', tag: 'Note', body: 'Use the Guryongsa parking lot. Arrive early on weekends and in peak season.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Nearby lodging', tag: 'Note', body: 'Hotels and restaurants cluster in Wonju city. For a pre-dawn start, stay in Wonju.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Descend two hours before sunset.' },
      { h: 'Caution sections', tag: 'Recommended', body: 'The Birobong route is steep and sustained. Carry trekking poles and crampons in wet or icy conditions, and never push past your limits.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Chiaksan playbook', href: 'chiaksan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['odaesan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'Woljeongsa temple fee', tag: 'Note', body: 'Routes start from the parking lot in front of Woljeongsa\'s Iljumun gate; an adult temple-visit fee of KRW 4,000 applies. Pick up a map at the visitor center before heading in.' },
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters and ranger-led programs at Odaesan National Park are booked through the park service reservation system.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Sangwonsa shuttle', tag: 'Note', body: 'A shuttle bus links Woljeongsa and Sangwonsa, handy for one-way traverses. If you parked on one side, plan how to retrieve the car.' },
      { h: 'Full-ridge access', tag: 'Recommended', body: 'The Odae five-peak traverse (26 km) requires a 05:00–06:00 start. Decide whether to park at Sangwonsa or Woljeongsa in advance.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Nearby lodging', tag: 'Note', body: 'Lodging is available around Woljeongsa, Sangwonsa, and Jinbu. For early starts, stay near the trailheads.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Long ridge routes demand a strict descent deadline before dark.' },
      { h: 'Weather check', tag: 'Recommended', body: 'Check conditions at the visitor center before entry; ridgelines are exposed to strong wind.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Odaesan playbook', href: 'odaesan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['taebaeksan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters and ranger-led programs at Taebaeksan National Park are booked through the park service reservation system. Check for trail-reservation sections before you go.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
      { h: 'Trail basics', tag: 'Note', body: 'From both Danggol Plaza and the Hyeonbulsa parking lot, confirm weather and closure notices at the visitor center before entry.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Parking', tag: 'Note', body: 'Danggol Plaza parking is paid (KRW 2,000). The Hyeonbulsa parking lot also serves as a trailhead.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Nearby lodging', tag: 'Note', body: 'Taebaek city has hotels. Book early for the popular winter snow-scenery season.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Icy sections form in winter — bring crampons.' },
      { h: 'Weather check', tag: 'Recommended', body: 'High elevation brings low temperatures and strong wind. Check the mountain forecast and wear windproof layers.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Taebaeksan playbook', href: 'taebaeksan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['bukhansan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters and ranger-led programs at Bukhansan National Park are booked through the park service reservation system. Trail-reservation sections change frequently — verify before your visit.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
      { h: 'Stay on marked trails', tag: 'Required', body: 'Unofficial paths exist around Manguydai. Follow signposts and official trails strictly — do not stray.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Access', tag: 'Note', body: 'Excellent access from central Seoul by subway and bus. See the course tabs in the playbook for each trailhead\'s approach.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day hikes are the norm. If you need to stay overnight, look for accommodations near the mountain (Guigidong or Songchu side).' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. The many exposed ridge sections demand full attention in poor weather.' },
      { h: 'Caution sections', tag: 'Recommended', body: 'The narrow ridge before Bibong and the very steep descent from the summit toward Manguydai include sections where you must step down backwards. Take extra care when wet.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Bukhansan playbook', href: 'bukhansan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['dobongsan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'National park', tag: 'Note', body: 'Dobongsan belongs to the Dobong district of Bukhansan National Park. Shelters and programs can be checked on the park service reservation system.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
      { h: 'Visitor center', tag: 'Note', body: 'Check the trail map and use the restrooms at the Obong visitor center before entry.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Subway & bus', tag: 'Recommended', body: 'From Subway Line 3 Gupabal Station, bus 34 reaches Songchu Valley in about 30 minutes; the Obong visitor center is a 5-minute walk from the stop.' },
      { h: 'Parking', tag: 'Note', body: 'Use Songchu parking lots 1 and 2. Arrive before 08:00 on weekends.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day hikes are the norm. The Songchu Valley restaurant strip is a good finish line.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Ridge sections are slippery — children should use the handrails.' },
      { h: 'Y-gok warning', tag: 'Required', body: 'Y-Valley (Ygyegok) is absolutely off-limits to beginners, children, and anyone uncomfortable with exposure. Go only with experienced climbers and never in rain or ice.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Dobongsan playbook', href: 'dobongsan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['myeongseongsan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'The signature route loops from Sangdong parking past Biseon and Deungnyong falls, the silvergrass fields, and Samgakbong to the summit and Sanan Pass — about 14.1 km and six and a half hours.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Parking', tag: 'Note', body: 'Start from Sangdong parking. Traverses may end elsewhere, so plan your car shuttle ahead of time.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day hikes are the norm. Pocheon city offers meals and lodging before or after the climb.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. The long traverse demands both fitness and time management.' },
      { h: 'Seasonal note', tag: 'Recommended', body: 'Autumn silvergrass draws big crowds. Arrive early on weekends.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Myeongseongsan playbook', href: 'myeongseongsan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['soyosan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Entry & fees', tag: 'Note', body: 'Entry is free (since May 2023). The parking lot — KRW 2,000 per day — sits right in front of the Iljumun gate.' },
      { h: 'Inquiries', tag: 'Note', body: 'Call the Soyosan management office at +82-31-865-5043 for closures and information.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Subway access', tag: 'Recommended', body: 'Metro Line 1 to Soyosan Station, Exit 1 — a 15-minute walk to the Iljumun gate (about 70 minutes from Seoul Station). Autumn weekends often fill the lot; the train is the safer bet.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day hikes are the norm. Restaurant rows near the Iljumun gate make an easy finish.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue (Dongducheon fire station). Do not hike after dark.' },
      { h: 'Galbawi warning', tag: 'Required', body: 'The Galbawi (Flag Rock) scramble requires gloves and is off-limits to those with a fear of heights — use the bypass. Never enter it wet or icy.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Soyosan playbook', href: 'soyosan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['unaksan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Choosing a route', tag: 'Note', body: 'The Gapyeong side (via Hyeondeungsa) avoids the exposed ridges and is comparatively safe; the Pocheon side (Mujichi Falls) brings steep staircases and ridge scrambles after the falls toward Seobong.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Parking', tag: 'Note', body: 'Parking is available on both the Gapyeong and Pocheon sides. Start and end points differ by route — plan your car shuttle in advance.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day hikes are the norm. Gapyeong and Pocheon towns offer meals and lodging.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Stay focused on the steep stairs and ridge of the Seobong section.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Unaksan playbook', href: 'unaksan-playbook.html' },
  ],
};

// ── Chungcheong · Jeolla ──

window.DEEP_INFO_EN['sobaeksan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'Entry fee', tag: 'Note', body: 'The Huibangsa district charges an entry fee (KRW 1,600 for adults). Confirm your course at the visitor center before heading in.' },
      { h: 'Access cutoff', tag: 'Required', body: 'The Jukryeong route requires a 06:00–07:00 start, with entry cutoff at 14:00. Respect the cutoff strictly.' },
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters and ranger-led programs at Sobaeksan National Park are booked through the park service reservation system.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Parking & car shuttle', tag: 'Recommended', body: 'For Jukryeong traverses, leave a car at Eouigok or Cheondong, or use a vehicle-transport service. Descending toward Cheondong parking requires a car.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Nearby lodging', tag: 'Note', body: 'Stay in Danyang or Yeongju. For the Jukryeong trailhead, consider lodging the night before for a pre-dawn drive.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. The Eouigok valley freezes in winter — bring crampons.' },
      { h: 'Seasonal note', tag: 'Recommended', body: 'Late-May azalea bloom along Yeonhwabong draws big crowds. Arrive early.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Sobaeksan playbook', href: 'sobaeksan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['gyeryongsan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters and ranger-led programs at Gyeryongsan National Park are booked through the park service reservation system. Check for trail-reservation sections before your visit.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
      { h: 'Route planning', tag: 'Required', body: 'Many routes have separate start and end points. Plan transport in advance and do not leave the marked trails mid-hike.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Access', tag: 'Note', body: 'Gapsa and Donghaksa districts are the main gateways. Access from Daejeon is easy; check shuttle and parking notices in peak season.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day hikes are the norm. Gongju and Daejeon offer lodging and meals.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. The Sambulbong ridge has exposed sections demanding full attention.' },
      { h: 'Caution sections', tag: 'Recommended', body: 'Short but strenuous ridgelines. Leave time for the transport connection at your descent point.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Gyeryongsan playbook', href: 'gyeryongsan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['woraksan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters and ranger-led programs at Woraksan National Park are booked through the park service reservation system. Check for trail-reservation sections before you go.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Access', tag: 'Note', body: 'Trailhead parking differs by course. For traverses, plan your car shuttle in advance.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day hikes are the norm. Jecheon and Chungju offer lodging and meals.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. The constant ups and downs of the ridge punish late-stage fatigue — manage your pace.' },
      { h: 'Caution sections', tag: 'Recommended', body: 'The Yeongbong ridge is exposed. Do not push on in rain or ice.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Woraksan playbook', href: 'woraksan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['sikjangsan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'An easy day-hike mountain on Daejeon\'s doorstep. The rolling ups and downs between peaks are hard on the knees on the way down.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Access', tag: 'Note', body: 'Easy to reach from central Daejeon. Use parking near the trailhead; expect weekend-morning crowds.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day hikes are the norm. Daejeon city has restaurants and hotels.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Refuel with a snack before Doksuribong, then focus on the descent.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Sikjangsan playbook', href: 'sikjangsan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['minjusan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'The mountain splits into two areas: Mulhangye-gok Valley and Domaryeong. The Minjujisan shelter is unmanned.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Rail & bus', tag: 'Recommended', body: 'Alight at Yeongdong Station (Gyeongbu line, KTX or regular trains) and take the rural bus toward Mulhangye-gok (routes 640/642, about 5 departures a day) — about 1 hour 10 minutes to Mulhan-ri.' },
      { h: 'Taxi & car', tag: 'Note', body: 'A taxi from Hwangan Station takes about 25 minutes (around KRW 30,000). Domaryeong has almost no public transport — charter a taxi from Yeongdong or Hwangan station. The Domaryeong and Mulhangye-gok parking lots are far apart by road, so plan a call-taxi pickup if you drive.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day hikes are the norm. Yeongdong town has lodging and meals.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. The rocky section around Seokgibong uses rope-and-cable handrails — mind the fall risk.' },
      { h: 'Winter preparation', tag: 'Required', body: 'A high mountain with heavy snowfall; sudden wind and rapid cooling are common in winter. Insulated clothing plus gaiters and crampons are essential.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Minjujisan playbook', href: 'minjusan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['jirisan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'Nogodan summit reservation', tag: 'Required', body: 'Hiking to the Nogodan summit requires an advance reservation; enter with your QR code.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
      { h: 'Shelter reservations', tag: 'Required', body: 'Shelters require advance booking. Next-month reservations open at 10:00 on the 1st of each month, and weekend slots sell out in seconds. Bring your own sleeping bag (no blankets provided).' },
      { h: 'Vehicle restrictions', tag: 'Recommended', body: 'On weekends and in peak season, the road to Seongsamjae is restricted. Park below and check whether the shuttle is running.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Car retrieval', tag: 'Required', body: 'After finishing the Seongsam–Jungsanri traverse at Jungsan-ri, take the Sancheong intercity bus or a taxi, then retrieve the car at Seongsamjae (a shuttle service is recommended).' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Shelters', tag: 'Required', body: 'Shelters such as Jangteomok, Byeoksoryeong, and Yeonhacheon run on reservations. Aim to reach Byeoksoryeong shelter before 17:00; switch to Yeonhacheon shelter if you run out of steam.' },
      { h: 'Day-two plan', tag: 'Recommended', body: 'For a Cheonwangbong sunrise, set out at 03:00–04:00; a sleeping bag rated for -5 to 0°C is needed.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. A same-day Cheonwangbong round trip requires a 04:00–05:00 start.' },
      { h: 'Descent caution', tag: 'Recommended', body: 'The 7.8 km descent to Jungsan-ri is the biggest cumulative shock to the knees — wear knee braces.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Jirisan playbook', href: 'jirisan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['naejangsan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters and ranger-led programs at Naejangsan National Park are booked through the park service reservation system.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
      { h: 'Peak-season planning', tag: 'Recommended', body: 'During the foliage season, check shuttle and parking-dispersal notices in advance and arrive early.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Jeongeup Station link', tag: 'Note', body: 'Check connections between Jeongeup Station and the parking lots, and plan your return-leg transport in advance. Confirm whether the cable car is running before your visit.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Nearby lodging', tag: 'Note', body: 'Jeongeup city has hotels — book early for the foliage season.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Keep spacing on the crowded leaf-peeping paths in autumn.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Naejangsan playbook', href: 'naejangsan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['deogyusan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters at Deogyusan National Park are booked through the park service reservation system.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
      { h: 'Trail basics', tag: 'Note', body: 'Confirm your course at the Gucheondong visitor center before entry. Parking is paid.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Yukgu traverse retrieval', tag: 'Required', body: 'The Yukgyeong traverse demands a 04:00–05:00 start; reserve onward transport from Yuksip-ryeong toward Jangsu or Jeonju, or plan a car shuttle.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Shelters', tag: 'Note', body: 'You can rest and buy food at Hyangjeokbong shelter; Sakkatjae shelter is a base on the highland ridge traverse.' },
      { h: 'Nearby lodging', tag: 'Note', body: 'Lodging clusters around Gucheondong, Muju. Book early in the winter ski season.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. The open ridgeline is very windy.' },
      { h: 'Seasonal note', tag: 'Recommended', body: 'Winter snowscapes are beautiful but icy — carry crampons and winter gear.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Deogyusan playbook', href: 'deogyusan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['wolchulsan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters and ranger-led programs at Wolchulsan National Park are booked through the park service reservation system.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
      { h: 'Dogapsa hours', tag: 'Note', body: 'Dogapsa temple admits visitors only during opening hours (09:00–18:00).' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Parking', tag: 'Note', body: 'Parking costs about KRW 3,000–4,000 for a passenger car. Pick up a course map at the visitor center.' },
      { h: 'Car retrieval', tag: 'Recommended', body: 'The Cheonhwangbong–Dogap traverse ends far from the start. Plan your car shuttle in advance.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day hikes are the norm. Yeongam town has lodging and meals.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. The rock sections become dangerously slippery in rain — avoid climbing in wet weather.' },
      { h: 'Cloud Bridge control', tag: 'Required', body: 'Gureumdari (Cloud Bridge, 54 m) may be closed temporarily in strong wind, and one-way operation applies at times. If closed, detour via Barampok Falls.' },
      { h: 'Start time', tag: 'Recommended', body: 'Start between 05:00 and 06:00 for the traverse — the 9.5 km full course takes over six and a half hours.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Wolchulsan playbook', href: 'wolchulsan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['mudeungsan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters and ranger-led programs at Mudeungsan National Park are booked through the park service reservation system.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Metro & bus', tag: 'Recommended', body: 'From Gwangju Metro Line 1 Hakdong–Jeungsimsa Station, transfer to buses 09, 50, 51, or 54 — about 10 minutes to the Jeungsimsa district terminus.' },
      { h: 'Wonhyosa access', tag: 'Note', body: 'For the Wonhyosa district, take bus 1187 from Gwangju Station or the intercity bus terminal to the Wonhyosa terminus.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day hikes are the norm. Gwangju city has lodging and meals.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. The loose-rock zone past Dangsannamu is slippery — take care.' },
      { h: 'Winter warning', tag: 'Required', body: 'The Seoseokdae and Ipseokdae columnar-joint area is habitually icy and windy in winter. Winter gear is a must.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Mudeungsan playbook', href: 'mudeungsan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['duryunsan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Cable car', tag: 'Note', body: 'A cable car links the lower station to the upper station (580 m). Confirm operations in strong wind or lightning.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Bus access', tag: 'Recommended', body: 'From Haenam intercity bus terminal, the Daerungsa-bound rural bus (Haenam Traffic) takes about 25 minutes to the Daerungsa terminus by the ticket office; buses run every 30–60 minutes.' },
      { h: 'Oso side', tag: 'Note', body: 'Take the Namchang/Wando county bus toward Oso and alight at Oso Shelter, or use a Haenam taxi.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day hikes are the norm. Haenam town has lodging and meals.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. The Noseungbong–Garyebong ridge has fall and slip hazards.' },
      { h: 'Winter warning', tag: 'Required', body: 'Accidents on the steep iron staircases and rock sections are frequent when icy. Carry crampons and winter gear.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Duryunsan playbook', href: 'duryunsan-playbook.html' },
  ],
};

// ── Gyeongsang · Jeju · Taiwan ──

window.DEEP_INFO_EN['gayasan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'Baegundong reservation', tag: 'Required', body: 'The Baegundong trail (toward Manmulsang) requires advance booking in the September–October peak. At the Chiin side, pay the entry fee and enter the Haeinsa grounds.' },
      { h: 'Haeinsa visit', tag: 'Note', body: 'After paying the entrance fee, you can view the Tripitaka Koreana in the Janggyeong Panjeon hall.' },
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters and ranger-led programs at Gayasan National Park are booked through the park service reservation system.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Parking & retrieval', tag: 'Recommended', body: 'Choose between Chiin parking and Baegundong parking (Seongju, North Gyeongsang). Descending via Tosingol to Chiin requires a taxi or shuttle to retrieve your car.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Nearby lodging', tag: 'Note', body: 'Lodging is available around Haeinsa and in Hapcheon and Seongju. Book early for autumn foliage.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Temperatures drop quickly near Sangwangbong — bring an extra layer.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Gayasan playbook', href: 'gayasan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['juwangsan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'National park reservations', tag: 'Recommended', body: 'Shelters and ranger-led programs at Juwangsan National Park are booked through the park service reservation system.', links: [{ label: 'KNPS Reservation System', href: 'https://reservation.knps.or.kr' }] },
      { h: 'Closure check', tag: 'Required', body: 'After heavy rain, trails close when stream levels rise. Check closures on the national park site (knps.or.kr) before setting out.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Bus access', tag: 'Note', body: 'From Cheongsong bus terminal, the Jusanji-bound bus takes about 20 minutes (KRW 1,300).' },
      { h: 'Car retrieval', tag: 'Recommended', body: 'Place a shuttle car at Sangui parking or take a taxi (Cheongsong, +82-54-874-2222) to retrieve your vehicle.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Nearby lodging', tag: 'Note', body: 'Stay in Cheongsong town or at guesthouses and pensions around Juwangsan.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Before Gamebong, the steep section (about 20% grade) rewards two trekking poles and knee braces.' },
      { h: 'Weather warning', tag: 'Required', body: 'The rock-and-root mix just below the summit is extremely dangerous in rain. Hike on dry days.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Juwangsan playbook', href: 'juwangsan-playbook.html' },
    { label: 'KNPS Reservation System', href: 'https://res.knps.or.kr' },
  ],
};

window.DEEP_INFO_EN['hallasan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits & Reservations', items: [
      { h: 'Advance reservation required', tag: 'Required', body: 'Gwaneumsa and Seongpanak cannot be entered without a reservation. Next-month bookings open at 09:00 on the 1st of each month and sell out fast (popular dates go in minutes). Watch for cancellation penalties.', links: [{ label: 'Hallasan Reservation', href: 'https://visithalla.jeju.go.kr' }] },
      { h: 'Entry cutoffs', tag: 'Required', body: 'Pass the trailhead before the cutoff time (winter 12:00, summer 15:00 — varies by course). The Yeongsil and Eorimok routes are posted as reservation-free. Cutoff inquiries: +82-64-713-9950.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Bus access', tag: 'Recommended', body: 'Bus 181 serves Seongpanak from Jeju city; bus 240 serves Eorimok. From Seogwipo, take city buses toward Yeongsil.' },
      { h: 'Parking', tag: 'Note', body: 'Seongpanak, Yeongsil, and Eorimok lots are paid and congested — arrive early. At Yeongsil, park at the ticket office and walk 40 minutes to the trailhead (shuttle available when running).' },
    ]},
    { icon: 'tent', title: 'Lodging & Supplies', items: [
      { h: 'Witse Oreum shelter', tag: 'Note', body: 'Cup noodles (KRW 1,500) and water are sold here — bring cash. No water sources after Jindallaebat shelter, so refill there.' },
      { h: 'Nearby lodging', tag: 'Note', body: 'The usual pattern is lodging in Jeju city or Seogwipo with a pre-dawn drive to the trailhead.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Summit temperatures hover near 10°C even in summer, with frequent wind and fog.' },
      { h: 'Rules & cutoffs', tag: 'Required', body: 'Start between 05:00 and 06:00; on the Gwaneumsa route, clear the Samgakbong checkpoint on time. Solo hiking is prohibited. Crampons and gaiters are essential in winter.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Hallasan playbook', href: 'hallasan-playbook.html' },
    { label: 'Hallasan Reservation', href: 'https://visithalla.jeju.go.kr' },
  ],
};

window.DEEP_INFO_EN['xueshan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Permits', items: [
      { h: 'Unified permit application', tag: 'Required', body: 'Xueshan entry permits go through the same unified Taiwanese hiking portal as Yushan. Overnight courses that include 369 Lodge are handled together with lodge allocation — check quotas and lottery details on the official site.', links: [{ label: 'hike.taiwan.gov.tw', href: 'https://hike.taiwan.gov.tw' }] },
    ]},
    { icon: 'bus', title: 'International Transit', items: [
      { h: 'Incheon → Taipei', tag: 'Note', body: 'Fly Incheon to Taipei, then combine public and chartered transport to reach the Xueshan trailhead. Timetables change by season — recheck after the permit is confirmed.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: '369 Lodge', tag: 'Required', body: 'The standard 2-day course climbs past Chika Lodge and Dongbong to overnight at 369 Lodge before the dark-forest push to the summit — 10.9 km one way from the trailhead.' },
      { h: 'Nearby lodging', tag: 'Note', body: 'A night in the gateway city at each end of the climb is a comfortable rhythm.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Local emergency numbers', tag: 'Required', body: 'Taiwan-wide: police 110, ambulance/fire 119. If altitude symptoms appear (headache, breathlessness), descend rather than push on.' },
      { h: 'Altitude preparation', tag: 'Recommended', body: 'The summit stands at 3,886 m, with total hiking times of 11–12 hours or more. Pack ample insulation, water, and trail food.' },
    ]},
  ],
  sources: [
    { label: 'Taiwan unified hiking application site', href: 'https://hike.taiwan.gov.tw' },
    { label: 'Details published in this site\'s Xueshan playbook', href: 'xueshan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['yangmingshan'] = {
  updated: 'As of 2026-09',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Descent deadline', tag: 'Required', body: 'Shuttle bus 108 leaves the terminal at 17:30 and ends its loop soon after. To catch it at the Xiaoyoukeng stop you must board by about 16:30 — treat 16:30 as your downhill deadline.' },
    ]},
    { icon: 'bus', title: 'Getting There', items: [
      { h: 'Shuttle & buses', tag: 'Recommended', body: 'From Xiaoyoukeng, take shuttle 108 to Yangmingshan bus terminal, then city buses R5 (紅5) or 260 back into the city.' },
      { h: 'Taipei access', tag: 'Note', body: 'Connections from central Taipei are excellent and day trips are the norm. Check last-shuttle times alongside your flight and hotel plans.' },
    ]},
    { icon: 'tent', title: 'Lodging', items: [
      { h: 'Lodging', tag: 'Note', body: 'Day trips are the norm. Base yourself at a Taipei city hotel.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Local emergency numbers', tag: 'Required', body: 'Taiwan-wide: police 110, ambulance/fire 119. Fog settles often on the volcanic terrain — descend when visibility drops.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Yangmingshan playbook', href: 'yangmingshan-playbook.html' },
  ],
};

// ── Mount Fuji (Japan — first mountain on the expansion standard) ──
// English mirror of the Korean entry — same facts, same sources.

window.DEEP_INFO_EN['fuji'] = {
  updated: 'As of 2026-09',
  note: 'First mountain on the Japan expansion',
  sections: [
    {
      icon: 'book', title: 'Permits & Reservations',
      items: [
        { h: 'Toll & reservation', tag: 'Required',
          body: 'Since May 9, 2025, all trails charge a one-time toll of 4,000 yen per person. The Yoshida Trail requires an online reservation with prepayment on the official site; the Shizuoka-side trails collect the toll on the trail.',
          links: [{ label: 'Official Mt. Fuji climbing site', href: 'https://www.fujisan-climb.jp/en/' }] },
        { h: 'Daily cap & gate', tag: 'Required',
          body: 'The Yoshida Trail caps climbers at 4,000 per day, and its gate closes from 2 p.m. to 3 a.m. to deter "bullet climbs". Hut guests with a confirmed booking may pass during the closure.' },
        { h: 'Climbing season', tag: 'Required',
          body: 'The Yoshida Trail is open July 1 – September 10; the three Shizuoka-side trails (Subashiri, Gotemba, Fujinomiya) run July 10 – September 10. Openings can shift with weather and lingering snow.' },
      ],
    },
    {
      icon: 'bus', title: 'International Transit',
      items: [
        { h: 'Incheon → Tokyo', tag: 'Note',
          body: 'Direct flights from Incheon reach Tokyo (Haneda or Narita) in roughly two and a half hours; schedules vary by season.' },
        { h: 'Tokyo → 5th Station', tag: 'Recommended',
          body: 'A direct bus from Shinjuku to the Fuji-Subaru Line 5th Station takes about 2 h 25 m (4,800 yen). It runs only in summer and books out early in peak season.',
          links: [{ label: 'highway-buses.jp', href: 'https://highway-buses.jp/course/fuji-5th.php' }] },
        { h: 'Via Kawaguchiko', tag: 'Note',
          body: 'Alternatively, take the Shinjuku → Kawaguchiko bus (about 1 h 45 m – 2 h, around 2,200 yen), then a local bus to the 5th Station (about 50 minutes, 3,400 yen round trip).' },
      ],
    },
    {
      icon: 'tent', title: 'Lodging',
      items: [
        { h: '8th-station huts', tag: 'Required',
          body: 'The standard 2-day itinerary overnights at a hut near the 8th station. Huts fill early in peak season — secure them before the toll reservation. No cooking; meals follow the hut\'s booking terms.' },
        { h: 'Nearby lodging', tag: 'Note',
          body: 'Plenty of hotels around Kawaguchiko and Fujisan Station. A night at each end of the climb is a comfortable rhythm.' },
      ],
    },
    {
      icon: 'shield', title: 'Safety & Emergency',
      items: [
        { h: 'Local emergency numbers', tag: 'Required',
          body: 'Japan-wide: police 110, ambulance/fire 119. At 3,776 m prepare for sudden alpine weather and hypothermia risk.' },
        { h: 'Weather & gear', tag: 'Recommended',
          body: 'Even in summer the summit is cold and windy. Carry windproof, insulated clothing and a headlamp, and postpone the climb in bad-weather forecasts.' },
        { h: 'Travel preparation', tag: 'Note',
          body: 'Travel insurance and connectivity (eSIM/roaming) are recommended. Share your itinerary with family or companions at home.' },
      ],
    },
  ],
  sources: [
    { label: 'Official Mt. Fuji climbing site', href: 'https://www.fujisan-climb.jp/en/' },
    { label: 'highway-buses.jp (Shinjuku ↔ 5th Station)', href: 'https://highway-buses.jp/course/fuji-5th.php' },
    { label: 'japan-guide.com — Mt. Fuji', href: 'https://www.japan-guide.com/e/e6901.html' },
    { label: 'Details published in this site\'s Fuji playbook', href: 'fuji-playbook.html' },
  ],
};

// ── Alishan (Taiwan — 4th Taiwan mountain) ──
// English mirror of the Korean entry — same facts, same sources.

window.DEEP_INFO_EN['alishan'] = {
  updated: 'As of 2026-09',
  sections: [
    {
      icon: 'book', title: 'Entry & Fees',
      items: [
        { h: 'Entrance fee', tag: 'Required',
          body: 'Admission to Alishan National Forest Recreation Area is NT$300. A half fare of NT$150 applies to visitors arriving by public bus (show your ticket) and eligible students.',
          links: [{ label: 'Taiwan Forest Recreation (official)', href: 'https://recreation.forest.gov.tw/en/Forest/RA?typ_id=0500001' }] },
        { h: 'Zhushan sunrise train', tag: 'Required',
          body: 'The Zhushan line costs NT$150 one way (about 25 minutes); departure times shift daily with sunrise. It sells out early in peak season — book ahead or arrive early.',
          links: [{ label: 'Alishan Forest Railway (official)', href: 'https://afrch.forest.gov.tw' }] },
        { h: 'Climbing permit', tag: 'Note',
          body: 'No separate hiking permit is needed for trails inside the recreation area (Giant Tree Trail, Datashan, etc.).' },
      ],
    },
    {
      icon: 'bus', title: 'International Transit',
      items: [
        { h: 'Incheon → Taipei', tag: 'Note',
          body: 'Fly Incheon to Taipei, then take the high-speed rail (THSR) to Chiayi.' },
        { h: 'Chiayi → Alishan', tag: 'Recommended',
          body: 'From HSR Chiayi Station, the Taiwan Trip shuttle Route A (7329) takes about 2.5 hours; from TRA Chiayi Station, take Route B (7322). Departures are limited — book ahead.',
          links: [{ label: 'Taiwan Trip shuttle info', href: 'https://www.taiwantrip.com.tw' }] },
        { h: 'Forest Railway main line', tag: 'Note',
          body: 'The Alishan Forest Railway main line also runs from Chiayi to Alishan — check the official timetable for operating days and duration.' },
      ],
    },
    {
      icon: 'tent', title: 'Lodging',
      items: [
        { h: 'Inside the recreation area', tag: 'Note',
          body: 'Staying at hotels or guesthouses inside the area makes the sunrise train easy. Book early in peak season.' },
        { h: 'Chiayi city', tag: 'Note',
          body: 'A same-day round trip by bus from Chiayi is possible, but overnighting inside the area is recommended for sunrise.' },
      ],
    },
    {
      icon: 'shield', title: 'Safety & Emergency',
      items: [
        { h: 'Local emergency numbers', tag: 'Required',
          body: 'Taiwan-wide: police 110, ambulance/fire 119. Temperatures drop before dawn — dress warmly for the sunrise train.' },
        { h: 'Weather & sunrise times', tag: 'Recommended',
          body: 'Sea of clouds is most likely on mornings after rain. Sunrise and train times change daily — confirm the day before.' },
        { h: 'Travel preparation', tag: 'Note',
          body: 'Travel insurance and connectivity (eSIM/roaming) are recommended. Share your itinerary with family or companions at home.' },
      ],
    },
  ],
  sources: [
    { label: 'Alishan Forest Railway (official)', href: 'https://afrch.forest.gov.tw' },
    { label: 'Taiwan Forest Recreation (official)', href: 'https://recreation.forest.gov.tw/en/Forest/RA?typ_id=0500001' },
    { label: 'Taiwan Trip shuttle info', href: 'https://www.taiwantrip.com.tw' },
    { label: 'Details published in this site\'s Alishan playbook', href: 'alishan-playbook.html' },
  ],
};

// ── Tateyama (Japan — 2nd Japan mountain) ──
// English mirror of the Korean entry — same facts, same sources.

window.DEEP_INFO_EN['tateyama'] = {
  updated: 'As of 2026-09',
  sections: [
    {
      icon: 'book', title: 'Permits & Reservations',
      items: [
        { h: 'Alpine Route season', tag: 'Required',
          body: 'The Tateyama–Kurobe Alpine Route operates only April 15 – November 30. It closes entirely in winter, and snow lingers on Oyama\'s summit until mid-June.',
          links: [{ label: 'Alpine Route official site', href: 'https://www.alpen-route.com/en/' }] },
        { h: 'Hut reservations', tag: 'Required',
          body: 'Murodo Sanso is the main lodging at Murodo. Book via the official site or the Yamaten booking service; the snow-wall season and autumn weekends sell out months ahead.',
          links: [{ label: 'Murodo Sanso', href: 'https://www.murodo-sanso.jp/' }] },
        { h: 'Climbing permits', tag: 'Note',
          body: 'No permit is needed for the Oyama climb. Tsurugi-dake is a genuine alpine scramble for experienced mountaineers only.' },
      ],
      links: [{ label: 'Yamaten booking site', href: 'https://yamaten-oyama.com/' }],
    },
    {
      icon: 'bus', title: 'International Transit',
      items: [
        { h: 'Incheon → Tokyo/Osaka', tag: 'Note',
          body: 'Fly Incheon to Tokyo or Osaka, then take the shinkansen toward Toyama or Nagano.' },
        { h: 'Toyama → Murodo', tag: 'Recommended',
          body: 'From Toyama Station: Toyama Chiho railway to Tateyama Station, then cable car → bus → ropeway → Murodo. From the Nagano side, enter via Shinano-Omachi. Segment fares are complex — check the official fare table.' },
        { h: 'Alpine Route passes', tag: 'Note',
          body: 'The route uses six or more transport modes. Round-trip passes and discount tickets are worth comparing on the official site.' },
      ],
    },
    {
      icon: 'tent', title: 'Lodging',
      items: [
        { h: 'Murodo Sanso', tag: 'Required',
          body: 'The standard base for a 2-day climb. Half-board rates are typical — confirm hut rules (slippers, bedding) when booking.' },
        { h: 'Raichozawa Onsen hut', tag: 'Note',
          body: 'An onsen hut about 20 minutes on foot from Murodo; its open-air bath makes it a popular alternative.' },
      ],
    },
    {
      icon: 'shield', title: 'Safety & Emergency',
      items: [
        { h: 'Local emergency numbers', tag: 'Required',
          body: 'Japan-wide: police 110, ambulance/fire 119. At 2,450 m, Murodo is cold with rapidly changing weather.' },
        { h: 'Season & snow', tag: 'Recommended',
          body: 'Crampons may be needed on Oyama until mid-June. Afternoon storms and wind are common — climb in the morning.' },
        { h: 'Travel preparation', tag: 'Note',
          body: 'Travel insurance and connectivity (eSIM/roaming) are recommended. Share your itinerary with family or companions at home.' },
      ],
    },
  ],
  sources: [
    { label: 'Tateyama–Kurobe Alpine Route (official)', href: 'https://www.alpen-route.com/en/' },
    { label: 'Murodo Sanso (official)', href: 'https://www.murodo-sanso.jp/' },
    { label: 'Japan Alps Adventures — Murodo Sanso', href: 'https://jaa.travel/en/mountain-hut/tateyamamurodosanso/' },
    { label: 'Details published in this site\'s Tateyama playbook', href: 'tateyama-playbook.html' },
  ],
};

// ── Huangshan (China — first China mountain) ──
// English mirror of the Korean entry — same facts, same sources.

window.DEEP_INFO_EN['huangshan'] = {
  updated: 'As of 2026-09',
  note: 'First mountain in China',
  sections: [
    {
      icon: 'book', title: 'Entry & Reservations',
      items: [
        { h: 'Entrance fee', tag: 'Required',
          body: 'Entry is 190 RMB in peak season and 150 RMB in winter, with re-entry allowed on 3 consecutive days. It is a real-name system — carry your passport.',
          links: [{ label: 'Huangshan scenic area (official)', href: 'https://www.huangshan.com.cn/' }] },
        { h: 'Rotating peak closures', tag: 'Required',
          body: 'For ecological rest, Lotus Peak (1,864 m) and Tiandu Feng (1,829 m) alternate multi-year closures. Check which summit is open at your travel time; Tiandu Feng requires a real-name reservation.' },
        { h: 'Winter closures', tag: 'Recommended',
          body: 'Sections including the West Sea Grand Canyon close in winter (roughly December–March). Verify open sections before a winter visit.' },
      ],
    },
    {
      icon: 'bus', title: 'International Transit',
      items: [
        { h: 'Incheon → China entry', tag: 'Required',
          body: 'Fly Incheon to Shanghai, Hangzhou, or similar. China entry policy (visa or visa-free) changes over time — check the latest rules before departure.' },
        { h: 'Huangshan North Station → Tangkou', tag: 'Recommended',
          body: 'By high-speed rail reach Huangshan North Station (Tunxi), then about 1 hour by bus to Tangkou town (South Gate transfer center). Shuttles continue to Ciguang Pavilion (Yuping ropeway) or Yungu Temple (Yungu ropeway).' },
        { h: 'Shuttle & cable cars', tag: 'Note',
          body: 'The Tangkou→station shuttle is charged separately. Cable cars are 80 RMB (Yungu) and 90 RMB (Yuping) one way in peak season.' },
      ],
    },
    {
      icon: 'tent', title: 'Lodging',
      items: [
        { h: 'Summit hotels', tag: 'Required',
          body: 'For sunrise, the standard is one night at a summit hotel (Beihai, Xihai, Baiyun…). Book weeks ahead in peak season; prices are high — budget accordingly.' },
        { h: 'Tangkou lodging', tag: 'Note',
          body: 'Plenty of hotels in Tangkou town. A same-day round trip is possible, but an overnight on the summit is recommended for both sunset and sunrise.' },
      ],
    },
    {
      icon: 'shield', title: 'Safety & Emergency',
      items: [
        { h: 'Local emergency numbers', tag: 'Required',
          body: 'China: police 110, ambulance 120, fire 119. Summit stairways become extremely slippery in rain.' },
        { h: 'Weather & crowds', tag: 'Recommended',
          body: 'Summit weather changes fast, and Chinese holiday periods bring extreme crowds. Move early and keep a flexible schedule.' },
        { h: 'Travel preparation', tag: 'Note',
          body: 'Travel insurance and connectivity (eSIM/roaming or a local SIM) are recommended. Share your itinerary with family or companions at home.' },
      ],
    },
  ],
  sources: [
    { label: 'Huangshan scenic area (official)', href: 'https://www.huangshan.com.cn/' },
    { label: 'China Discovery — Huangshan Cable Car', href: 'https://www.chinadiscovery.com/huangshan-tours/transportation/huangshan-cable-car.html' },
    { label: 'People\'s Daily — Lotus/Tiandu rotation', href: 'http://paper.people.com.cn/rmrbhwb/html/2023-12/18/content_26032392.htm' },
    { label: 'Details published in this site\'s Huangshan playbook', href: 'huangshan-playbook.html' },
  ],
};

// ── Fansipan (Vietnam — first Vietnam mountain) ──
window.DEEP_INFO_EN['fansipan'] = {
  updated: 'As of 2026-09',
  note: 'First mountain in Vietnam',
  sections: [
    {
      icon: 'book', title: 'Permits & Fees',
      items: [
        { h: 'Park entry & climbing permit', tag: 'Required',
          body: 'Hoang Lien National Park entry is ~70,000 VND and the Fansipan climbing permit ~300,000 VND. A licensed guide is mandatory for trekking routes and is usually included in tours.',
          links: [{ label: 'Hoang Lien NP information', href: 'https://vinpearl.com/en/hoang-lien-national-park-sapa' }] },
        { h: 'Cable car fare', tag: 'Note',
          body: 'The Sun World Fansipan Legend cable car costs about 700–900k VND round trip (adult). Peak weekends sell out — pay online in advance.' },
      ],
    },
    {
      icon: 'bus', title: 'International Transit',
      items: [
        { h: 'Incheon → Hanoi', tag: 'Note',
          body: 'Direct flights from Incheon reach Hanoi in roughly four and a half hours.' },
        { h: 'Hanoi → Sapa', tag: 'Recommended',
          body: 'Overnight sleeper train (depart Hanoi ~22:00, arrive Lao Cai ~06:00, ~400–450k VND) or an express sleeper bus. Shuttles cover Lao Cai → Sapa in ~30 minutes (~30k VND).' },
      ],
    },
    {
      icon: 'tent', title: 'Lodging',
      items: [
        { h: 'Sapa town', tag: 'Note',
          body: 'Plenty of hotels and guesthouses in Sapa — sufficient for the 1-day trek; the 2-day traverse includes a camp night.' },
        { h: 'Mountain camp (traverse)', tag: 'Recommended',
          body: 'The 2-day tour includes one camp night near the summit; porters prepare tents and meals. Check your sleeping bag — nights are cold.' },
      ],
    },
    {
      icon: 'shield', title: 'Safety & Emergency',
      items: [
        { h: 'Local emergency numbers', tag: 'Required',
          body: 'Vietnam: police 113, fire 114, ambulance 115. The summit is cold year-round and ices over in winter.' },
        { h: 'Rainy season', tag: 'Recommended',
          body: 'Leeches and slippery mud appear May–September. Wear long pants and socks, and plan mornings-first days against afternoon fog.' },
        { h: 'Travel preparation', tag: 'Note',
          body: 'Travel insurance and connectivity (eSIM/roaming) are recommended. Share your itinerary with family or companions at home.' },
      ],
    },
  ],
  sources: [
    { label: 'Sun World cable-car information', href: 'https://sunparadiseland.com/SunParadiseLandSaPa/tin-tuc/fansipan-cable-car-2025-a-guide-to-ticket-prices-and-schedules-for-newbies-6908' },
    { label: 'Hoang Lien NP fee information', href: 'https://vinpearl.com/en/hoang-lien-national-park-sapa' },
    { label: 'Hanoi–Sapa train information', href: 'https://vietnam-railway.com/train/touristtrainstosapa' },
    { label: 'Details published in this site\'s Fansipan playbook', href: 'fansipan-playbook.html' },
  ],
};

// ── Taishan (China — 2nd China mountain) ──
window.DEEP_INFO_EN['taishan'] = {
  updated: 'As of 2026-09',
  sections: [
    {
      icon: 'book', title: 'Entry & Fees',
      items: [
        { h: 'Entrance fee', tag: 'Required',
          body: '115 RMB in peak season (Apr–Oct), 100 RMB off-season. Re-entry is allowed for 3 days after first check-in and the ticket includes Dai Temple. Real-name system — carry your passport.',
          links: [{ label: 'Tai\'an official ticket page', href: 'https://tsgw.taian.gov.cn/art/2025/4/7/art_366039_10321175.html' }] },
        { h: 'Cable car & shuttle', tag: 'Note',
          body: 'The Zhongtianmen–Nantianmen cable car costs 100 RMB one way; the Tianwaicun shuttle is 30 RMB. Combining the cable car on descent protects your knees.' },
        { h: '24-hour access', tag: 'Note',
          body: 'Taishan is open 24 hours year-round, which is why the night-climb-for-sunrise culture thrives. Headlamp and warm layers are mandatory at night.' },
      ],
    },
    {
      icon: 'bus', title: 'International Transit',
      items: [
        { h: 'Incheon → China entry', tag: 'Required',
          body: 'Fly Incheon to Beijing, Shanghai, or similar, then take the Beijing–Shanghai high-speed rail to Tai\'an Station (about 2 hours from Beijing). Check the latest China entry policy before departure.' },
        { h: 'Tai\'an Station → Hongmen', tag: 'Note',
          body: 'A short taxi or bus ride connects Tai\'an Station to the Hongmen trailhead — access is very easy from town.' },
      ],
    },
    {
      icon: 'tent', title: 'Lodging',
      items: [
        { h: 'Summit lodging', tag: 'Note',
          body: 'Overnighting at a summit hotel lets you catch both sunset and sunrise. Peak-season prices are high — book in advance.' },
        { h: 'Tai\'an city', tag: 'Note',
          body: 'For night climbs, the usual pattern is leaving your luggage at a city hotel and climbing light.' },
      ],
    },
    {
      icon: 'shield', title: 'Safety & Emergency',
      items: [
        { h: 'Local emergency numbers', tag: 'Required',
          body: 'China: police 110, ambulance 120, fire 119. Steps ice over in winter — bring crampons.' },
        { h: 'Crowds & weather', tag: 'Recommended',
          body: 'Weekend holiday stairs become extremely crowded, and the pre-dawn summit is cold — full insulation is essential on night climbs.' },
        { h: 'Travel preparation', tag: 'Note',
          body: 'Travel insurance and connectivity (eSIM/roaming or local SIM) are recommended. Share your itinerary with family or companions at home.' },
      ],
    },
  ],
  sources: [
    { label: 'Tai\'an official ticket page', href: 'https://tsgw.taian.gov.cn/art/2025/4/7/art_366039_10321175.html' },
    { label: 'TravelChinaGuide — Mount Tai', href: 'https://www.travelchinaguide.com/attraction/shandong/taian/mt_taishan.htm' },
    { label: 'Details published in this site\'s Taishan playbook', href: 'taishan-playbook.html' },
  ],
};

// ── Kinabalu (Malaysia — first Malaysia mountain) ──
window.DEEP_INFO_EN['kinabalu'] = {
  updated: 'As of 2026-09',
  note: 'First mountain in Malaysia',
  sections: [
    {
      icon: 'book', title: 'Permits & Booking',
      items: [
        { h: 'Summit climb booking', tag: 'Required',
          body: 'Summit climbs are booked only through Sabah Parks and capped at 135 climbers per day. Bookings open about a year ahead and sell out quickly — fix your travel dates first.',
          links: [{ label: 'Sabah Parks (official)', href: 'https://sabahparks.org.my/' }] },
        { h: 'Mandatory guide', tag: 'Required',
          body: 'A licensed guide must accompany all summit climbers (RM 350 per guide, up to 5 climbers). Guides are assigned at Timpohon Gate on climb morning.' },
        { h: 'Permits & fees', tag: 'Required',
          body: 'The climbing permit for foreigners is now RM 400 (raised). The permit lanyard must be worn throughout. Laban Rata lodging and meals are charged separately — packages run RM 1,740–2,180.',
          links: [{ label: 'Summit package information', href: 'https://www.mountkinabalu.com/packages' }] },
      ],
    },
    {
      icon: 'bus', title: 'International Transit',
      items: [
        { h: 'Incheon → Kota Kinabalu', tag: 'Note',
          body: 'Direct flights from Incheon reach Kota Kinabalu (Sabah, Borneo) in about five hours.' },
        { h: 'Kota Kinabalu → Park', tag: 'Recommended',
          body: 'About 2 hours by road to Kinabalu Park. An overnight near the park (Kundasang area) the night before makes the early gate start easier.' },
      ],
    },
    {
      icon: 'tent', title: 'Lodging',
      items: [
        { h: 'Laban Rata', tag: 'Required',
          body: 'The hut at 3,270 m is the de-facto mandatory overnight for the summit push. Bed capacity is tied to the daily quota; meals are included in bookings.' },
        { h: 'Near-park lodging', tag: 'Note',
          body: 'Use park lodges or Kota Kinabalu hotels before and after the climb. The night-before stay near the park suits the early gate start.' },
      ],
    },
    {
      icon: 'shield', title: 'Safety & Emergency',
      items: [
        { h: 'Local emergency numbers', tag: 'Required',
          body: 'Malaysia unified emergency number is 999. If altitude symptoms appear (headache, nausea), stop ascending and tell your guide immediately.' },
        { h: 'Descent deadline', tag: 'Required',
          body: 'The descent deadline is usually 10:30–11:00. Overrunning it triggers rescue procedures — keep summit time short.' },
        { h: 'Travel preparation', tag: 'Note',
          body: 'Travel insurance (check alpine-climb coverage) and connectivity are recommended. Share your itinerary with family or companions at home.' },
      ],
    },
  ],
  sources: [
    { label: 'Sabah Parks (official)', href: 'https://sabahparks.org.my/' },
    { label: 'Mount Kinabalu package information', href: 'https://www.mountkinabalu.com/packages' },
    { label: 'Borneo Dream — cost details', href: 'https://borneodream.com/' },
    { label: 'Details published in this site\'s Kinabalu playbook', href: 'kinabalu-playbook.html' },
  ],
};

// ── Rinjani (Indonesia — first Indonesia mountain) ──
window.DEEP_INFO_EN['rinjani'] = {
  updated: 'As of 2026-09',
  note: 'First mountain in Indonesia',
  sections: [
    {
      icon: 'book', title: 'Permits & Fees',
      items: [
        { h: 'Entry fee restructure', tag: 'Required',
          body: 'From November 3, 2025 the foreign entry fee is about IDR 200–250k per person per day (varies by route class). A 2-day summit trek costs IDR 400–500k in park fees alone.',
          links: [{ label: 'Entry fee update', href: 'https://rinjanitrekkingplanner.com/rinjani-entrance-ticket-fees-2026-update/' }] },
        { h: 'Guide mandatory', tag: 'Required',
          body: 'A licensed guide is mandatory and solo trekking is banned. Guides ~IDR 400–500k/day, porters ~250–350k/day; 2-day summit packages run $130–285.' },
        { h: 'Daily quota & insurance', tag: 'Required',
          body: 'A cap of 240 international trekkers per day sells out in season. The 2025 SOP also requires official registration and trekking insurance.' },
      ],
    },
    {
      icon: 'bus', title: 'International Transit',
      items: [
        { h: 'Incheon → Bali/Lombok', tag: 'Note',
          body: 'Fly to Bali (Denpasar) or Lombok (LOP). From Bali, ferries and fast boats connect to Lombok.' },
        { h: 'Airport → gate', tag: 'Recommended',
          body: 'From Lombok airport, Senaru is about 2.5–3 hours by road and Sembalun about 3–3.5 hours. Tour pickups are standard.' },
      ],
    },
    {
      icon: 'tent', title: 'Lodging',
      items: [
        { h: 'On-mountain camping', tag: 'Required',
          body: 'There are no huts on Rinjani — camping only. Tours include tents, cooking gear, and meals; porters carry the load.' },
        { h: 'Senaru/Sembalun villages', tag: 'Note',
          body: 'Use guesthouses before and after the climb. The night before at a gate-side guesthouse helps the early start.' },
      ],
    },
    {
      icon: 'shield', title: 'Safety & Emergency',
      items: [
        { h: 'Local emergency numbers', tag: 'Required',
          body: 'Indonesia unified emergency number is 112. Strong winds and rapid temperature drops hit the rim and summit.' },
        { h: 'Season rules', tag: 'Required',
          body: 'Trekking is allowed roughly April–December; the park closes in the rainy season (Jan–Mar). Unauthorized entry during closure carries legal penalties.' },
        { h: 'Travel preparation', tag: 'Note',
          body: 'Trekking insurance is required by the SOP. Prepare proof of coverage and share your itinerary with family at home.' },
      ],
    },
  ],
  sources: [
    { label: 'Rinjani entry fee update', href: 'https://rinjanitrekkingplanner.com/rinjani-entrance-ticket-fees-2026-update/' },
    { label: 'Rinjani trekking info (guide/porter)', href: 'https://rinjaniindonesia.com/en/guide/rinjani-trekking-info' },
    { label: 'Rinjani 2025 SOP', href: 'https://rinjanidawnadventures.com/mount-rinjani-national-park-sop-2025/' },
    { label: 'Details published in this site\'s Rinjani playbook', href: 'rinjani-playbook.html' },
  ],
};

// ── Poon Hill (Nepal — first Nepal mountain) ──
window.DEEP_INFO_EN['poonhill'] = {
  updated: 'As of 2026-09',
  note: 'First mountain in Nepal',
  sections: [
    {
      icon: 'book', title: 'Permits',
      items: [
        { h: 'ACAP permit', tag: 'Required',
          body: 'The Annapurna Conservation Area Permit (ACAP) is mandatory — about NPR 3,000 (~$25–30) for foreigners. Issue it at offices in Kathmandu or Pokhara.' },
        { h: 'Guide mandatory', tag: 'Required',
          body: 'Since April 2023 a licensed guide is required for treks in protected areas (~$25–35/day). Solo trekking is officially not permitted.' },
        { h: 'Teahouse booking', tag: 'Note',
          body: 'Teahouse lodging runs $5–10/night with on-site allocation possible, but reserving ahead is safer in peak season (Oct–Nov, Mar–May).' },
      ],
    },
    {
      icon: 'bus', title: 'International Transit',
      items: [
        { h: 'Incheon → Kathmandu', tag: 'Note',
          body: 'Fly Incheon to Kathmandu (about 8–9 hours including connections). Issue the ACAP permit there, then move to Pokhara.' },
        { h: 'Pokhara → Nayapul', tag: 'Recommended',
          body: 'About 1.5–2 hours by road from Pokhara to Nayapul. Local buses, taxis, and shuttles are available; the same transport retrieves you at the trek end.' },
      ],
    },
    {
      icon: 'tent', title: 'Lodging',
      items: [
        { h: 'Teahouses', tag: 'Required',
          body: 'Sleep in teahouses throughout the trek ($5–10/night). Rooms and bathrooms are often shared; early allocation in Ghorepani helps in peak season.' },
        { h: 'Pokhara lodging', tag: 'Note',
          body: 'The standard pattern is staying at Pokhara Lakeside before and after the trek.' },
      ],
    },
    {
      icon: 'shield', title: 'Safety & Emergency',
      items: [
        { h: 'Local emergency numbers', tag: 'Required',
          body: 'Nepal: police 100, ambulance 102, unified 112. Poon Hill sits at 3,210 m with low altitude-sickness risk, but pre-dawn cold is real.' },
        { h: 'Season & flights', tag: 'Recommended',
          body: 'Seasons are March–May and October–November. Monsoon (Jun–Sep) brings flight delays and leeches — keep spare days.' },
        { h: 'Travel preparation', tag: 'Note',
          body: 'Travel insurance (confirm trekking altitude coverage) is recommended. Share your itinerary with family or companions at home.' },
      ],
    },
  ],
  sources: [
    { label: 'Poon Hill cost & itinerary information', href: 'https://www.havenholidaysnepal.com/trips/3-days-poonhill-trek' },
    { label: 'ACAP permit information', href: 'https://ntb.gov.np/' },
    { label: 'Details published in this site\'s Poon Hill playbook', href: 'poonhill-playbook.html' },
  ],
};

// ── Korea 100 Famous Mountains (10 mountains) ──

window.DEEP_INFO_EN['gwanaksan'] = {
  updated: 'As of 2026-09',
  note: 'Korea 100 Famous Mountains expansion',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Gwanaksan is one of Korea\'s 100 Famous Mountains and requires no separate climbing permit. Check trail opening hours and weather before visiting.' },
      { h: 'Transit', tag: 'Recommended', body: 'Public transit is available but schedules may be limited — verify the latest timetable before departure.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Aim to descend two hours before sunset.' },
      { h: 'Wildfire alert', tag: 'Required', body: 'Smoking and cooking are prohibited during wildfire alert periods. Check forest service notices.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Gwanaksan playbook', href: 'gwanaksan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['suraksan'] = {
  updated: 'As of 2026-09',
  note: 'Korea 100 Famous Mountains expansion',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Suraksan is one of Korea\'s 100 Famous Mountains and requires no separate climbing permit. Check trail opening hours and weather before visiting.' },
      { h: 'Transit', tag: 'Recommended', body: 'Public transit is available but schedules may be limited — verify the latest timetable before departure.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Aim to descend two hours before sunset.' },
      { h: 'Wildfire alert', tag: 'Required', body: 'Smoking and cooking are prohibited during wildfire alert periods. Check forest service notices.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Suraksan playbook', href: 'suraksan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['cheonggyesan'] = {
  updated: 'As of 2026-09',
  note: 'Korea 100 Famous Mountains expansion',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Cheonggyesan is one of Korea\'s 100 Famous Mountains and requires no separate climbing permit. Check trail opening hours and weather before visiting.' },
      { h: 'Transit', tag: 'Recommended', body: 'Public transit is available but schedules may be limited — verify the latest timetable before departure.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Aim to descend two hours before sunset.' },
      { h: 'Wildfire alert', tag: 'Required', body: 'Smoking and cooking are prohibited during wildfire alert periods. Check forest service notices.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Cheonggyesan playbook', href: 'cheonggyesan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['achasan'] = {
  updated: 'As of 2026-09',
  note: 'Korea 100 Famous Mountains expansion',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Achasan is one of Korea\'s 100 Famous Mountains and requires no separate climbing permit. Check trail opening hours and weather before visiting.' },
      { h: 'Transit', tag: 'Recommended', body: 'Public transit is available but schedules may be limited — verify the latest timetable before departure.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Aim to descend two hours before sunset.' },
      { h: 'Wildfire alert', tag: 'Required', body: 'Smoking and cooking are prohibited during wildfire alert periods. Check forest service notices.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Achasan playbook', href: 'achasan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['geumjeongsan'] = {
  updated: 'As of 2026-09',
  note: 'Korea 100 Famous Mountains expansion',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Geumjeongsan is one of Korea\'s 100 Famous Mountains and requires no separate climbing permit. Check trail opening hours and weather before visiting.' },
      { h: 'Transit', tag: 'Recommended', body: 'Public transit is available but schedules may be limited — verify the latest timetable before departure.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Aim to descend two hours before sunset.' },
      { h: 'Wildfire alert', tag: 'Required', body: 'Smoking and cooking are prohibited during wildfire alert periods. Check forest service notices.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Geumjeongsan playbook', href: 'geumjeongsan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['palgongsan'] = {
  updated: 'As of 2026-09',
  note: 'Korea 100 Famous Mountains expansion',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Palgongsan is one of Korea\'s 100 Famous Mountains and requires no separate climbing permit. Check trail opening hours and weather before visiting.' },
      { h: 'Transit', tag: 'Recommended', body: 'Public transit is available but schedules may be limited — verify the latest timetable before departure.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Aim to descend two hours before sunset.' },
      { h: 'Wildfire alert', tag: 'Required', body: 'Smoking and cooking are prohibited during wildfire alert periods. Check forest service notices.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Palgongsan playbook', href: 'palgongsan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['unmunsan'] = {
  updated: 'As of 2026-09',
  note: 'Korea 100 Famous Mountains expansion',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Unmunsan is one of Korea\'s 100 Famous Mountains and requires no separate climbing permit. Check trail opening hours and weather before visiting.' },
      { h: 'Transit', tag: 'Recommended', body: 'Public transit is available but schedules may be limited — verify the latest timetable before departure.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Aim to descend two hours before sunset.' },
      { h: 'Wildfire alert', tag: 'Required', body: 'Smoking and cooking are prohibited during wildfire alert periods. Check forest service notices.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Unmunsan playbook', href: 'unmunsan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['songnisan'] = {
  updated: 'As of 2026-09',
  note: 'Korea 100 Famous Mountains expansion',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Songnisan is one of Korea\'s 100 Famous Mountains and requires no separate climbing permit. Check trail opening hours and weather before visiting.' },
      { h: 'Transit', tag: 'Recommended', body: 'Public transit is available but schedules may be limited — verify the latest timetable before departure.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Aim to descend two hours before sunset.' },
      { h: 'Wildfire alert', tag: 'Required', body: 'Smoking and cooking are prohibited during wildfire alert periods. Check forest service notices.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Songnisan playbook', href: 'songnisan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['daedunsan'] = {
  updated: 'As of 2026-09',
  note: 'Korea 100 Famous Mountains expansion',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Daedunsan is one of Korea\'s 100 Famous Mountains and requires no separate climbing permit. Check trail opening hours and weather before visiting.' },
      { h: 'Transit', tag: 'Recommended', body: 'Public transit is available but schedules may be limited — verify the latest timetable before departure.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Aim to descend two hours before sunset.' },
      { h: 'Wildfire alert', tag: 'Required', body: 'Smoking and cooking are prohibited during wildfire alert periods. Check forest service notices.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Daedunsan playbook', href: 'daedunsan-playbook.html' },
  ],
};

window.DEEP_INFO_EN['maisan'] = {
  updated: 'As of 2026-09',
  note: 'Korea 100 Famous Mountains expansion',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Maisan is one of Korea\'s 100 Famous Mountains and requires no separate climbing permit. Check trail opening hours and weather before visiting.' },
      { h: 'Transit', tag: 'Recommended', body: 'Public transit is available but schedules may be limited — verify the latest timetable before departure.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Emergency contact', tag: 'Required', body: 'Call 119 for mountain rescue. Aim to descend two hours before sunset.' },
      { h: 'Wildfire alert', tag: 'Required', body: 'Smoking and cooking are prohibited during wildfire alert periods. Check forest service notices.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s Maisan playbook', href: 'maisan-playbook.html' },
  ],
};

// ── Himalaya category 3 treks ──

window.DEEP_INFO_EN['ebc'] = {
  updated: 'As of 2026-09',
  note: 'Himalaya category',
  sections: [
    { icon: 'book', title: 'Permits', items: [
      { h: 'Trekking permits', tag: 'Required', body: 'Everest Base Camp trekking requires national park entry and municipality permits (~NPR 6,000 total). A guide has been mandatory since 2023.' },
      { h: 'Insurance', tag: 'Required', body: 'Trekking insurance (including helicopter evacuation) is de-facto mandatory — the route includes sections above 5,000 m.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Local emergency numbers', tag: 'Required', body: 'Nepal: police 100, ambulance 102, unified 112. Descend immediately if altitude symptoms appear.' },
      { h: 'Season', tag: 'Recommended', body: 'March–May (spring) and October–November (autumn) are optimal. Winter high-altitude camping is for experts only.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s playbook', href: 'ebc-playbook.html' },
  ],
};

window.DEEP_INFO_EN['act'] = {
  updated: 'As of 2026-09',
  note: 'Himalaya category',
  sections: [
    { icon: 'book', title: 'Permits', items: [
      { h: 'Trekking permits', tag: 'Required', body: 'Annapurna Circuit trekking requires national park entry and municipality permits (~NPR 6,000 total). A guide has been mandatory since 2023.' },
      { h: 'Insurance', tag: 'Required', body: 'Trekking insurance (including helicopter evacuation) is de-facto mandatory — the route includes sections above 5,000 m.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Local emergency numbers', tag: 'Required', body: 'Nepal: police 100, ambulance 102, unified 112. Descend immediately if altitude symptoms appear.' },
      { h: 'Season', tag: 'Recommended', body: 'March–May (spring) and October–November (autumn) are optimal. Winter high-altitude camping is for experts only.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s playbook', href: 'act-playbook.html' },
  ],
};

window.DEEP_INFO_EN['langtang'] = {
  updated: 'As of 2026-09',
  note: 'Himalaya category',
  sections: [
    { icon: 'book', title: 'Permits', items: [
      { h: 'Trekking permits', tag: 'Required', body: 'Langtang Valley trekking requires national park entry and municipality permits (~NPR 6,000 total). A guide has been mandatory since 2023.' },
      { h: 'Insurance', tag: 'Required', body: 'Trekking insurance (including helicopter evacuation) is de-facto mandatory — the route includes sections above 5,000 m.' },
    ]},
    { icon: 'shield', title: 'Safety & Emergency', items: [
      { h: 'Local emergency numbers', tag: 'Required', body: 'Nepal: police 100, ambulance 102, unified 112. Descend immediately if altitude symptoms appear.' },
      { h: 'Season', tag: 'Recommended', body: 'March–May (spring) and October–November (autumn) are optimal. Winter high-altitude camping is for experts only.' },
    ]},
  ],
  sources: [
    { label: 'Details published in this site\'s playbook', href: 'langtang-playbook.html' },
  ],
};

// ── Korea 100 Famous Mountains 2nd batch (7 mountains) ──

window.DEEP_INFO_EN['inwangsan'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 2nd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Inwangsan is one of Korea\'s 100 Famous Mountains. No separate permit needed. Check trail hours before visiting.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue. Descend two hours before sunset.' },
    ]},
  ],
  sources: [{ label: 'Details in this site\'s playbook', href: 'inwangsan-playbook.html' }],
};

window.DEEP_INFO_EN['gajisan'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 2nd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Gajisan is one of Korea\'s 100 Famous Mountains. No separate permit needed. Check trail hours before visiting.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue. Descend two hours before sunset.' },
    ]},
  ],
  sources: [{ label: 'Details in this site\'s playbook', href: 'gajisan-playbook.html' }],
};

window.DEEP_INFO_EN['hwawangsan'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 2nd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Hwawangsan is one of Korea\'s 100 Famous Mountains. No separate permit needed. Check trail hours before visiting.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue. Descend two hours before sunset.' },
    ]},
  ],
  sources: [{ label: 'Details in this site\'s playbook', href: 'hwawangsan-playbook.html' }],
};

window.DEEP_INFO_EN['unjangsan'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 2nd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Unjangsan is one of Korea\'s 100 Famous Mountains. No separate permit needed. Check trail hours before visiting.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue. Descend two hours before sunset.' },
    ]},
  ],
  sources: [{ label: 'Details in this site\'s playbook', href: 'unjangsan-playbook.html' }],
};

window.DEEP_INFO_EN['yeongchwisan'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 2nd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Yeongchwisan is one of Korea\'s 100 Famous Mountains. No separate permit needed. Check trail hours before visiting.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue. Descend two hours before sunset.' },
    ]},
  ],
  sources: [{ label: 'Details in this site\'s playbook', href: 'yeongchwisan-playbook.html' }],
};

window.DEEP_INFO_EN['biseulsan'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 2nd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Biseulsan is one of Korea\'s 100 Famous Mountains. No separate permit needed. Check trail hours before visiting.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue. Descend two hours before sunset.' },
    ]},
  ],
  sources: [{ label: 'Details in this site\'s playbook', href: 'biseulsan-playbook.html' }],
};

window.DEEP_INFO_EN['cheongnyangsan'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 2nd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Cheongnyangsan is one of Korea\'s 100 Famous Mountains. No separate permit needed. Check trail hours before visiting.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue. Descend two hours before sunset.' },
    ]},
  ],
  sources: [{ label: 'Details in this site\'s playbook', href: 'cheongnyangsan-playbook.html' }],
};

// ── Korea 100 Famous Mountains 3rd batch (6 mountains) ──

window.DEEP_INFO_EN['ansan'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 3rd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Ansan is one of Korea\'s 100 Famous Mountains. No separate permit needed.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue.' },
    ]},
  ],
  sources: [{ label: 'Details in playbook', href: 'ansan-playbook.html' }],
};

window.DEEP_INFO_EN['bulsan'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 3rd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Bulsan is one of Korea\'s 100 Famous Mountains. No separate permit needed.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue.' },
    ]},
  ],
  sources: [{ label: 'Details in playbook', href: 'bulsan-playbook.html' }],
};

window.DEEP_INFO_EN['sogeumgang'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 3rd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Sogeumgang is one of Korea\'s 100 Famous Mountains. No separate permit needed.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue.' },
    ]},
  ],
  sources: [{ label: 'Details in playbook', href: 'sogeumgang-playbook.html' }],
};

window.DEEP_INFO_EN['heuiyangsan'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 3rd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Heuiyangsan is one of Korea\'s 100 Famous Mountains. No separate permit needed.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue.' },
    ]},
  ],
  sources: [{ label: 'Details in playbook', href: 'heuiyangsan-playbook.html' }],
};

window.DEEP_INFO_EN['cheongtaesan'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 3rd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Cheongtaesan is one of Korea\'s 100 Famous Mountains. No separate permit needed.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue.' },
    ]},
  ],
  sources: [{ label: 'Details in playbook', href: 'cheongtaesan-playbook.html' }],
};

window.DEEP_INFO_EN['baekamsan'] = {
  updated: 'As of 2026-09', note: 'Korea 100 Famous Mountains 3rd batch',
  sections: [
    { icon: 'book', title: 'Trail Basics', items: [
      { h: 'Trail basics', tag: 'Note', body: 'Baekamsan is one of Korea\'s 100 Famous Mountains. No separate permit needed.' },
    ]},
    { icon: 'shield', title: 'Safety', items: [
      { h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain rescue.' },
    ]},
  ],
  sources: [{ label: 'Details in playbook', href: 'baekamsan-playbook.html' }],
};

// ── Korea 100 Famous Mountains 3rd batch ──

window.DEEP_INFO_EN['ansan'] = {updated:'As of 2026-09',note:'Korea 100 Famous Mountains 3rd batch',sections:[{icon:'book',title:'Trail Basics',items:[{h:'Trail basics',tag:'Note',body:'Ansan is one of Korea\'s 100 Famous Mountains. No separate permit needed.'}]},{icon:'shield',title:'Safety',items:[{h:'Emergency',tag:'Required',body:'Call 119 for mountain rescue.'}]}],sources:[{label:'Details in playbook',href:'ansan-playbook.html'}]};

window.DEEP_INFO_EN['bulsan'] = {updated:'As of 2026-09',note:'Korea 100 Famous Mountains 3rd batch',sections:[{icon:'book',title:'Trail Basics',items:[{h:'Trail basics',tag:'Note',body:'Bulsan is one of Korea\'s 100 Famous Mountains. No separate permit needed.'}]},{icon:'shield',title:'Safety',items:[{h:'Emergency',tag:'Required',body:'Call 119 for mountain rescue.'}]}],sources:[{label:'Details in playbook',href:'bulsan-playbook.html'}]};

window.DEEP_INFO_EN['sogeumgang'] = {updated:'As of 2026-09',note:'Korea 100 Famous Mountains 3rd batch',sections:[{icon:'book',title:'Trail Basics',items:[{h:'Trail basics',tag:'Note',body:'Sogeumgang is one of Korea\'s 100 Famous Mountains. No separate permit needed.'}]},{icon:'shield',title:'Safety',items:[{h:'Emergency',tag:'Required',body:'Call 119 for mountain rescue.'}]}],sources:[{label:'Details in playbook',href:'sogeumgang-playbook.html'}]};

window.DEEP_INFO_EN['heuiyangsan'] = {updated:'As of 2026-09',note:'Korea 100 Famous Mountains 3rd batch',sections:[{icon:'book',title:'Trail Basics',items:[{h:'Trail basics',tag:'Note',body:'Heuiyangsan is one of Korea\'s 100 Famous Mountains. No separate permit needed.'}]},{icon:'shield',title:'Safety',items:[{h:'Emergency',tag:'Required',body:'Call 119 for mountain rescue.'}]}],sources:[{label:'Details in playbook',href:'heuiyangsan-playbook.html'}]};

window.DEEP_INFO_EN['cheongtaesan'] = {updated:'As of 2026-09',note:'Korea 100 Famous Mountains 3rd batch',sections:[{icon:'book',title:'Trail Basics',items:[{h:'Trail basics',tag:'Note',body:'Cheongtaesan is one of Korea\'s 100 Famous Mountains. No separate permit needed.'}]},{icon:'shield',title:'Safety',items:[{h:'Emergency',tag:'Required',body:'Call 119 for mountain rescue.'}]}],sources:[{label:'Details in playbook',href:'cheongtaesan-playbook.html'}]};

window.DEEP_INFO_EN['baekamsan'] = {updated:'As of 2026-09',note:'Korea 100 Famous Mountains 3rd batch',sections:[{icon:'book',title:'Trail Basics',items:[{h:'Trail basics',tag:'Note',body:'Baekamsan is one of Korea\'s 100 Famous Mountains. No separate permit needed.'}]},{icon:'shield',title:'Safety',items:[{h:'Emergency',tag:'Required',body:'Call 119 for mountain rescue.'}]}],sources:[{label:'Details in playbook',href:'baekamsan-playbook.html'}]};

// ── Korea 100 Famous Mountains 4th batch ──

window.DEEP_INFO_EN['yongmunsan'] = {updated:'As of 2026-09',note:'Korea 100 Famous Mountains 4th batch',sections:[{icon:'book',title:'Trail Basics',items:[{h:'Trail basics',tag:'Note',body:'Yongmunsan is one of Korea\'s 100 Famous Mountains. No separate permit needed.'}]},{icon:'shield',title:'Safety',items:[{h:'Emergency',tag:'Required',body:'Call 119 for mountain rescue.'}]}],sources:[{label:'Details in playbook',href:'yongmunsan-playbook.html'}]};

window.DEEP_INFO_EN['wanggwan'] = {updated:'As of 2026-09',note:'Korea 100 Famous Mountains 4th batch',sections:[{icon:'book',title:'Trail Basics',items:[{h:'Trail basics',tag:'Note',body:'Wanggwan is one of Korea\'s 100 Famous Mountains. No separate permit needed.'}]},{icon:'shield',title:'Safety',items:[{h:'Emergency',tag:'Required',body:'Call 119 for mountain rescue.'}]}],sources:[{label:'Details in playbook',href:'wanggwan-playbook.html'}]};

window.DEEP_INFO_EN['yumyeongsan'] = {updated:'As of 2026-09',note:'Korea 100 Famous Mountains 4th batch',sections:[{icon:'book',title:'Trail Basics',items:[{h:'Trail basics',tag:'Note',body:'Yumyeongsan is one of Korea\'s 100 Famous Mountains. No separate permit needed.'}]},{icon:'shield',title:'Safety',items:[{h:'Emergency',tag:'Required',body:'Call 119 for mountain rescue.'}]}],sources:[{label:'Details in playbook',href:'yumyeongsan-playbook.html'}]};

/* Korea 100 Famous Mountains, round 5: Namsan (Gyeongju), Gyebangsan, Dutasan, Manisan — KO/EN synced 2026-09. */
window.DEEP_INFO_EN['namsan'] = {updated:'2026-09 기준',note:'Korea 100 Famous Mountains round 5',sections:[{ icon: 'book', title: 'Entry & Booking', items: [{ h: 'No reservation or permit needed', tag: 'Note', body: 'Namsan is open to hikers without any reservation or permit.' }, { h: 'Samneung Trail Center', tag: 'Note', body: 'Information, restrooms and parking are available at the Samneung trail center.' }, { h: 'Heritage protection', tag: 'Required', body: 'The whole mountain is a UNESCO World Heritage zone — never touch or mark the stone Buddhas, pagodas or temple sites.' }] }, { icon: 'bus', title: 'Transport', items: [{ h: 'Rail & bus', tag: 'Note', body: 'Take the KTX-Eum to Gyeongju Station or intercity buses to the Gyeongju Terminal, then city buses toward the Namsan area (Samneung / Tongiljeon). Check routes and schedules before travel.' }, { h: 'By car', tag: 'Note', body: 'The Samneung trail-center lot is the most used trailhead parking — it fills early on peak-season weekends.' }] }, { icon: 'tent', title: 'Lodging', items: [{ h: 'Downtown Gyeongju', tag: 'Note', body: 'Hotels, condos and guesthouses cluster in central Gyeongju — a convenient base. Bomun tourist district is 20–30 minutes by car.' }] }, { icon: 'shield', title: 'Safety & Emergency', items: [{ h: 'Emergency', tag: 'Required', body: 'In case of mountain accidents call 119.' }, { h: 'Ridge hikes', tag: 'Recommended', body: 'The Gowibong-side ridgeline is hard to follow after dark — carry a headlamp and plan to descend before sunset.' }] }],sources:[{ label: 'UNESCO — Gyeongju Historic Areas', href: 'https://whc.unesco.org/en/list/976/' }, { label: 'Gyeongju City', href: 'https://www.gyeongju.go.kr' }]};
window.DEEP_INFO_EN['gyebangsan'] = {updated:'2026-09 기준',note:'Korea 100 Famous Mountains round 5',sections:[{ icon: 'book', title: 'Entry & Booking', items: [{ h: 'Park access', tag: 'Note', body: 'Inside Odaesan National Park — no permit required.' }, { h: 'Check closures', tag: 'Recommended', body: 'Seasonal rest-zone (summer) and fire-season closures may restrict sections — check park and county notices before you go.' }] }, { icon: 'bus', title: 'Transport', items: [{ h: 'By car', tag: 'Note', body: 'The Windunderyeong rest-area lot and the 1100 Highlands lot are the main trailheads — both fill early on weekend mornings.' }, { h: 'Public transport', tag: 'Note', body: 'Regional buses toward Pyeongchang or Hongcheon get you close, but local connections are infrequent — check timetables in advance.' }] }, { icon: 'tent', title: 'Lodging', items: [{ h: 'Jinbu / Yongpyeong area', tag: 'Note', body: 'Yongpyeong Resort and guesthouses around Jinbu are the usual bases before and after the hike.' }] }, { icon: 'shield', title: 'Safety & Emergency', items: [{ h: 'Emergency', tag: 'Required', body: 'In case of mountain accidents call 119.' }, { h: 'Winter hiking', tag: 'Recommended', body: 'Famed for snowscapes — bring crampons/spikes and wind gear, and adjust plans in strong wind or blizzard conditions.' }] }],sources:[{ label: 'Odaesan National Park (KNPS)', href: 'https://www.knps.or.kr' }, { label: 'Visit Korea — Gyebangsan', href: 'https://korean.visitkorea.or.kr' }]};
window.DEEP_INFO_EN['dutasan'] = {updated:'2026-09 기준',note:'Korea 100 Famous Mountains round 5',sections:[{ icon: 'book', title: 'Entry & Booking', items: [{ h: 'No permit needed', tag: 'Note', body: 'Dutasan is open without any reservation or permit.' }, { h: 'Mureung Valley', tag: 'Note', body: 'Mureung is a managed tourist area — fees and parking rules may apply. Check local-government guidance before visiting.' }] }, { icon: 'bus', title: 'Transport', items: [{ h: 'Express bus', tag: 'Note', body: 'Frequent express buses run from Seoul Dong-Seoul Terminal to Donghae; from town, city buses head toward Mureung Valley.' }, { h: 'Datjae rest area', tag: 'Note', body: 'Datjae rest area (680 Duta-ro, Hajang-myeon, Samcheok) is the trailhead for the shortest route — easiest by car.' }] }, { icon: 'tent', title: 'Lodging', items: [{ h: 'Donghae & Samcheok towns', tag: 'Note', body: 'Stay in Donghae or Samcheok, or at guesthouses near Mureung Valley.' }] }, { icon: 'shield', title: 'Safety & Emergency', items: [{ h: 'Emergency', tag: 'Required', body: 'In case of mountain accidents call 119.' }, { h: 'Crag sections', tag: 'Required', body: 'The Byeotul Rock and Macheonru sections are continuous crags. Avoid them in rain, strong wind or ice, and never linger under rockfall zones.' }] }],sources:[{ label: 'Samcheok City Tourism', href: 'https://tour.samcheok.go.kr' }, { label: 'Donghae City', href: 'https://www.dh.go.kr' }]};
window.DEEP_INFO_EN['manisan'] = {updated:'2026-09 기준',note:'Korea 100 Famous Mountains round 5',sections:[{ icon: 'book', title: 'Entry & Booking', items: [{ h: 'Managed tourist site', tag: 'Recommended', body: 'Manisan operates as a public tourist site — check fees, opening hours and whether the Chanseongdan altar is open, with Ganghwa County before your visit.' }] }, { icon: 'bus', title: 'Transport', items: [{ h: 'Getting to Ganghwa', tag: 'Note', body: 'City buses run from Ganghwa Bus Terminal toward Manisan, but services are infrequent — driving is easier.' }, { h: 'By car', tag: 'Note', body: 'From Seoul, the West Coast Expressway reaches Ganghwa Island in roughly 1–1.5 hours.' }] }, { icon: 'tent', title: 'Lodging', items: [{ h: 'Ganghwa town', tag: 'Note', body: 'Hotels and guesthouses in Ganghwa town work well; day trips from Incheon or Seoul are also common.' }] }, { icon: 'shield', title: 'Safety & Emergency', items: [{ h: 'Emergency', tag: 'Required', body: 'In case of mountain accidents call 119.' }, { h: 'Ridge & stairs', tag: 'Recommended', body: 'Avoid the Jeongsusa ridge rocks when icy. The 372-step Dangun-ro descent is hard on the knees — take it slowly.' }] }],sources:[{ label: 'Ganghwa County — Manisan', href: 'https://www.ganghwa.go.kr' }, { label: 'Incheon Tourism', href: 'https://www.incheonfair.go.kr' }]};

/* Korea 100 Famous Mountains round 6: Daeamsan, Baegunsan, Sinbulsan, Gamaksan — KO/EN synced 2026-09. */
window.DEEP_INFO_EN['daeamsan'] = {updated:'2026-09 기준',note:'Korea 100 Famous Mountains round 6',sections:[{ icon: 'book', title: 'Entry & Booking', items: [{ h: 'Yongneup is fully reservation-only', tag: 'Required', body: 'The Yongneup marsh (Natural Monument No. 246) tour is 100% reservation-based: apply at least 10 days ahead and bring photo ID. Inje (sum.inje.go.kr) and Yanggu (yg-eco.kr) use separate portals.' }, { h: 'General ridge trail', tag: 'Note', body: 'The Hyangnobong hiking ridge needs no reservation — but the marsh reserve is off-limits without one.' }, { h: 'Civilian Control Line', tag: 'Required', body: 'The area lies inside the CCL — ID is mandatory and photographing military facilities is prohibited.' }] }, { icon: 'bus', title: 'Transport', items: [{ h: 'Inje Gaari course', tag: 'Note', body: 'Meet at the Gaari center, then a 14 km vehicle transfer to the trail start. Driving or taxi is the practical access.' }, { h: 'Yanggu Seoheung-ri course', tag: 'Note', body: 'Starts at the temporary Yongneup center near Yanggu — check local transit times in advance.' }] }, { icon: 'tent', title: 'Lodging', items: [{ h: 'Yanggu & Inje towns', tag: 'Note', body: 'Motels and pensions in both county seats, or stays near Paroho Lake, make convenient bases.' }] }, { icon: 'shield', title: 'Safety & Emergency', items: [{ h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain accidents.' }, { h: 'Highland weather', tag: 'Recommended', body: 'The 1,280 m moor runs cold even in summer; boardwalks are slippery in rain.' }] }],sources:[{ label: 'Inje County Eco-tourism — Yongneup', href: 'https://sum.inje.go.kr' }, { label: 'Yanggu Yongneup tours', href: 'https://yg-eco.kr' }]};

window.DEEP_INFO_EN['baegunsan'] = {updated:'2026-09 기준',note:'Korea 100 Famous Mountains round 6',sections:[{ icon: 'book', title: 'Entry & Booking', items: [{ h: 'No permit needed', tag: 'Note', body: 'Baegunsan is open without reservation or permit.' }, { h: 'Recreation forest fees', tag: 'Recommended', body: 'The recreation forest section has facility and parking fees — check Gwangyang City notices before visiting.' }] }, { icon: 'bus', title: 'Transport', items: [{ h: 'Public transport', tag: 'Note', body: 'Reach Gwangyang or Gurye by intercity bus, then local transport to the specific trailhead (Naeroe, Nonsil, or the forest) — verify each in advance.' }, { h: 'By car', tag: 'Note', body: 'Azalea-season weekends (late May–early June) bring severe traffic and parking jams.' }] }, { icon: 'tent', title: 'Lodging', items: [{ h: 'Recreation forest & town', tag: 'Note', body: 'Forest cabins or Gwangyang town lodging work well.' }] }, { icon: 'shield', title: 'Safety & Emergency', items: [{ h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain accidents.' }, { h: 'Festival crowds', tag: 'Recommended', body: 'The summit area packs during the Azalea Festival — hike early.' }] }],sources:[{ label: 'Gwangyang City — Recreation Forest', href: 'https://www.gwangyang.go.kr' }, { label: 'Baegunsan Azalea Festival', href: 'https://www.gwangyang.go.kr' }]};

window.DEEP_INFO_EN['sinbulsan'] = {updated:'2026-09 기준',note:'Korea 100 Famous Mountains round 6',sections:[{ icon: 'book', title: 'Entry & Booking', items: [{ h: 'No permit needed', tag: 'Note', body: 'Sinbulsan is open without reservation or permit (not a national park).' }] }, { icon: 'bus', title: 'Transport', items: [{ h: 'Baenae parking', tag: 'Note', body: 'Baenae Lot 2 in Icheon-ri, Sangbuk-myeon, Ulju is the main trailhead lot; use Lot 1 when full.' }, { h: 'Public transport', tag: 'Note', body: 'City buses from Ulsan reach the Baenaegol area but run infrequently — check timetables.' }] }, { icon: 'tent', title: 'Lodging', items: [{ h: 'Ulsan & Eonyang', tag: 'Note', body: 'Town lodging in Ulsan or Eonyang is the practical base.' }] }, { icon: 'shield', title: 'Safety & Emergency', items: [{ h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain accidents.' }, { h: 'Silver-grass season & crags', tag: 'Recommended', body: 'Autumn weekends crowd the trails; the Ganwolsan crags are dangerous in rain.' }] }],sources:[{ label: 'Ulsan Tourism — Yeongnam Alps', href: 'https://tour.ulsan.go.kr' }, { label: 'Ulju County Tourism', href: 'https://www.ulju.go.kr' }]};

window.DEEP_INFO_EN['gamaksan'] = {updated:'2026-09 기준',note:'Korea 100 Famous Mountains round 6',sections:[{ icon: 'book', title: 'Entry & Booking', items: [{ h: 'No permit needed', tag: 'Note', body: 'Gamaksan is open without reservation or permit.' }, { h: 'Bridge hours', tag: 'Recommended', body: 'The suspension bridge has set opening hours — check Paju City notices before you go.' }] }, { icon: 'bus', title: 'Transport', items: [{ h: 'Public transport', tag: 'Note', body: 'Inter-city buses from Seoul/Ilsan reach Paju, then local transport toward Gamaksa or the valley — verify schedules.' }, { h: 'By car', tag: 'Note', body: 'Gamaksa and valley lots; crowded on weekend mornings.' }] }, { icon: 'tent', title: 'Lodging', items: [{ h: 'Paju & Ilsan', tag: 'Note', body: 'A capital-area day trip is standard; overnight options in Paju or Ilsan.' }] }, { icon: 'shield', title: 'Safety & Emergency', items: [{ h: 'Emergency', tag: 'Required', body: 'Call 119 for mountain accidents.' }, { h: 'Crags & bridge', tag: 'Recommended', body: 'Crags around Imkkeokjeongbong are accident-prone when wet; the bridge sways in strong wind.' }] }],sources:[{ label: 'Paju City — Gamaksan', href: 'https://www.paju.go.kr' }, { label: 'Valley & bridge info', href: 'https://www.paju.go.kr' }]};

