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
