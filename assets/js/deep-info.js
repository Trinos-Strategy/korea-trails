/* MT Trails — Deep Info Band 공유 렌더러 (STANDARD-DEEP-INFO.md §3)
 * 마운트: <div id="deep-info-root" data-mountain="<id>"></div>
 * 데이터: <html lang="ko"> → window.DEEP_INFO[<id>] (assets/js/deep-info-data.js)
 *         <html lang="en"> → window.DEEP_INFO_EN[<id>] (assets/js/deep-info-data-en.js)
 *         해당 언어 표가 비어 있으면 반대 언어 표로 폴백한다.
 * 템플릿 패밀리(seoraksan류/양명산류) 무관하게 자체 스코프 스타일로 렌더링한다.
 * JS가 로드되지 않으면 마운트 div가 비어 본문 코스 정보는 무손상이다.
 */
(function () {
  'use strict';

  var mount = document.getElementById('deep-info-root');
  if (!mount) return;

  var id = mount.getAttribute('data-mountain');
  var lang = document.documentElement.getAttribute('lang') === 'en' ? 'en' : 'ko';
  var PFX = location.pathname.indexOf('/en/') >= 0 ? '../' : '';
  function tableFor(l) { return l === 'en' ? window.DEEP_INFO_EN : window.DEEP_INFO; }
  var data = (tableFor(lang) || {})[id];
  if (!data) {
    lang = lang === 'en' ? 'ko' : 'en';
    data = (tableFor(lang) || {})[id];
  }
  if (!data || !data.sections || !data.sections.length) return;

  var L10N = {
    ko: {
      title: '심화 탐방 정보',
      aria: '심화 탐방 정보',
      footer: '노선·요금·예약 창구는 변동될 수 있습니다.',
      tags: { '필수': 'dib-tag-required', '권장': 'dib-tag-warn', '참고': 'dib-tag-neutral' },
    },
    en: {
      title: 'Deep-Dive Trail Info',
      aria: 'Deep-dive trail information',
      footer: 'Schedules, fares, and reservation channels may change.',
      tags: { 'Required': 'dib-tag-required', 'Recommended': 'dib-tag-warn', 'Note': 'dib-tag-neutral' },
    },
  };
  var T = L10N[lang];
  var TAG_CLASS = T.tags;
  var ICONS = { book: 'icon-book', bus: 'icon-bus', tent: 'icon-tent', shield: 'icon-shield',
                phone: 'icon-phone', tip: 'icon-tip', season: 'icon-season',
                mountain: 'icon-mountain', location: 'icon-location' };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function cardHtml(sec) {
    var items = (sec.items || []).map(function (it) {
      var tag = it.tag && TAG_CLASS[it.tag]
        ? '<span class="dib-tag ' + TAG_CLASS[it.tag] + '">' + esc(it.tag) + '</span> ' : '';
      var head = it.h ? '<h3 class="dib-item-h">' + tag + esc(it.h) + '</h3>' : (tag ? '<h3 class="dib-item-h">' + tag.replace(' </span>', '</span>') + '</h3>' : '');
      var links = (it.links || []).map(function (l) {
        return '<a class="dib-link" href="' + esc(l.href) + '" target="_blank" rel="noopener">' + esc(l.label) + ' ↗</a>';
      }).join(' ');
      return '<div class="dib-item">' + head + '<p class="dib-item-body">' + esc(it.body) + (links ? ' ' + links : '') + '</p></div>';
    }).join('');
    var blockLinks = (sec.links || []).map(function (l) {
      return '<a class="dib-link dib-block-link" href="' + esc(l.href) + '" target="_blank" rel="noopener">' + esc(l.label) + ' ↗</a>';
    }).join(' ');
    var iconId = ICONS[sec.icon] || 'icon-book';
    return '' +
      '<div class="dib-card">' +
        '<div class="dib-card-head">' +
          '<svg class="dib-icon" aria-hidden="true"><use href="'+PFX+'assets/icons/icons.svg#' + iconId + '"></use></svg>' +
          '<h2 class="dib-card-title">' + esc(sec.title) + '</h2>' +
        '</div>' +
        items + (blockLinks ? '<div class="dib-links-row">' + blockLinks + '</div>' : '') +
      '</div>';
  }

  function sourceHtml() {
    var links = (data.sources || []).map(function (l) {
      return '<a href="' + esc(l.href) + '" target="_blank" rel="noopener" class="dib-source-link">' + esc(l.label) + '</a>';
    }).join('<span class="dib-source-sep" aria-hidden="true"> · </span>');
    var parts = [];
    if (data.updated) parts.push('<span class="dib-updated">' + esc(data.updated) + '</span>');
    if (links) parts.push('<span class="dib-sources">' + links + '</span>');
    if (!parts.length) return '';
    return '<footer class="dib-footer"><svg class="dib-icon dib-icon-sm" aria-hidden="true"><use href="'+PFX+'assets/icons/icons.svg#icon-tip"></use></svg>' +
           ' ' + esc(T.footer) + ' ' + parts.join(' — ') + '</footer>';
  }

  var root = document.createElement('section');
  root.className = 'deep-info-band';
  root.setAttribute('aria-label', T.aria);
  root.innerHTML =
    '<div class="dib-head">' +
      '<svg class="dib-icon dib-icon-lg" aria-hidden="true"><use href="'+PFX+'assets/icons/icons.svg#icon-book"></use></svg>' +
      '<h2 class="dib-title">' + esc(T.title) + '</h2>' +
      (data.note ? '<span class="dib-note">' + esc(data.note) + '</span>' : '') +
    '</div>' +
    '<div class="dib-grid">' + data.sections.map(cardHtml).join('') + '</div>' +
    sourceHtml();

  var style = document.createElement('style');
  style.textContent =
    '.deep-info-band{--dib-surface:var(--surface,var(--color-surface,#fff));--dib-surface2:var(--surface2,var(--color-surface-offset,#f6f7f9));--dib-border:var(--border,var(--color-border,#e4e7ec));--dib-text:var(--text,var(--color-text,#17181c));--dib-muted:var(--muted,var(--color-text-muted,#5b6472));--dib-primary:var(--primary,var(--color-primary,#0ea5e9));margin:var(--space-8,40px) 0;background:var(--dib-surface2);border:1px solid var(--dib-border);border-radius:16px;padding:clamp(18px,3vw,28px);}' +
    '.dib-head{display:flex;align-items:center;gap:10px;margin-bottom:14px;}' +
    '.dib-title{margin:0;font-family:var(--font-display,inherit);font-size:clamp(1.05rem,2vw,1.3rem);font-weight:800;color:var(--dib-text);letter-spacing:-.01em;}' +
    '.dib-note{font-size:12px;font-weight:700;color:var(--dib-muted);border:1px solid var(--dib-border);border-radius:999px;padding:2px 10px;background:var(--dib-surface);white-space:nowrap;}' +
    '.dib-icon{width:20px;height:20px;fill:none;stroke:var(--dib-primary);stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none;}' +
    '.dib-icon-lg{width:24px;height:24px;}.dib-icon-sm{width:14px;height:14px;}' +
    '.dib-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;}' +
    '@media (min-width:1024px){.dib-grid{grid-template-columns:repeat(2,1fr);}}' +
    '.dib-card{background:var(--dib-surface);border:1px solid var(--dib-border);border-radius:12px;padding:16px 18px;}' +
    '.dib-card-head{display:flex;align-items:center;gap:8px;margin-bottom:10px;}' +
    '.dib-card-title{margin:0;font-size:15px;font-weight:800;color:var(--dib-text);}' +
    '.dib-item+.dib-item{margin-top:10px;padding-top:10px;border-top:1px dashed var(--dib-border);}' +
    '.dib-item-h{margin:0 0 4px;font-size:13px;font-weight:700;color:var(--dib-text);}' +
    '.dib-tag{display:inline-block;font-size:10px;font-weight:800;border-radius:999px;padding:1px 8px;margin-right:6px;vertical-align:1px;}' +
    '.dib-tag-required{background:rgba(239,68,68,.14);color:#b91c1c;}' +
    '.dib-tag-warn{background:rgba(201,162,75,.18);color:#8a6a1f;}' +
    '.dib-tag-neutral{background:rgba(125,135,150,.14);color:var(--dib-muted);}' +
    '.dib-item-body{margin:0;font-size:13px;line-height:1.7;color:var(--dib-muted);}' +
    '.dib-link{color:var(--dib-primary);font-weight:700;text-decoration:none;white-space:nowrap;}' +
    '.dib-link:hover{text-decoration:underline;}' +
    '.dib-links-row{margin-top:10px;padding-top:10px;border-top:1px dashed var(--dib-border);display:flex;flex-wrap:wrap;gap:8px;}' +
    '.dib-block-link{font-size:12px;}' +
    '.dib-footer{margin-top:14px;padding-top:12px;border-top:1px solid var(--dib-border);font-size:11.5px;line-height:1.8;color:var(--dib-muted);display:flex;gap:6px;align-items:flex-start;}' +
    '.dib-source-link{color:var(--dib-primary);text-decoration:none;font-weight:600;}' +
    '.dib-source-link:hover{text-decoration:underline;}' +
    '.dib-source-sep{color:var(--dib-border);}' +
    '.dib-updated{font-weight:700;color:var(--dib-text);}';

  document.head.appendChild(style);

  // 사진 갤러리(가장 가까운 .photo-gallery-section) 앞에 삽입, 없으면 마운트 위치에 그대로 둔다.
  var gallery = document.querySelector('.photo-gallery-section');
  if (gallery && gallery.parentNode) {
    gallery.parentNode.insertBefore(root, gallery);
    mount.parentNode.removeChild(mount);
  } else {
    mount.appendChild(root);
  }

  document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('.deep-info-band')) return;
    var galleryNow = document.querySelector('.photo-gallery-section');
    if (galleryNow && galleryNow.parentNode) {
      galleryNow.parentNode.insertBefore(root, galleryNow);
      if (mount.parentNode) mount.parentNode.removeChild(mount);
    } else {
      mount.appendChild(root);
    }
  });

  /* ── 실시간 산악 날씨 + 실측 등산로 지도 (동적 강화 — 실패 시 조용히 생략) ── */

  var L10N2 = {
    ko: {
      weather: '산악 날씨', weatherSub: '정상 고도 기준 실시간 예보',
      now: '현재', feels: '바람', precip: '강수',
      sunrise: '일출', sunset: '일몰', days: ['오늘', '내일', '모레'],
      track: '실측 등산로 지도', trackSub: 'OpenStreetMap 등산로 실측', measured: '실측',
      start: '입구', elevProfile: '고도 프로파일',
      srcWeather: 'Open-Meteo', srcOsm: '© OpenStreetMap',
      loading: '불러오는 중…',
    },
    en: {
      weather: 'Mountain Weather', weatherSub: 'Live forecast at summit elevation',
      now: 'Now', feels: 'Wind', precip: 'Precip',
      sunrise: 'Sunrise', sunset: 'Sunset', days: ['Today', 'Tomorrow', 'Day 3'],
      track: 'Measured Trail Map', trackSub: 'OpenStreetMap hiking routes', measured: 'measured',
      start: 'Start', elevProfile: 'Elevation profile',
      srcWeather: 'Open-Meteo', srcOsm: '© OpenStreetMap',
      loading: 'Loading…',
    },
  };
  var T2 = L10N2[lang] || L10N2.ko;

  function grid() { return root.querySelector('.dib-grid'); }

  function addCard(iconId, title, sub) {
    var g = grid();
    if (!g) return null;
    var c = document.createElement('div');
    c.className = 'dib-card dib-dyn';
    c.innerHTML = '<div class="dib-card-head"><svg class="dib-icon" aria-hidden="true"><use href="'+PFX+'assets/icons/icons.svg#' + iconId + '"></use></svg>' +
      '<h2 class="dib-card-title">' + esc(title) + '</h2></div>' +
      (sub ? '<p class="dib-dyn-sub">' + esc(sub) + '</p>' : '');
    g.appendChild(c);
    return c;
  }

  function fmtKm(km) { return (km >= 10 ? Math.round(km * 10) / 10 : Math.round(km * 100) / 100) + 'km'; }

  /* 1) 산악 날씨 — Open-Meteo (무료·키 불필요·CC BY 4.0, 브라우저에서 직접 호출) */
  function initWeather(coords) {
    if (!coords || !window.fetch) return;
    var card = addCard('season', T2.weather, T2.weatherSub);
    var body = document.createElement('div');
    body.className = 'dib-weather';
    body.innerHTML = '<span class="dib-loading">' + esc(T2.loading) + '</span>';
    card.appendChild(body);
    var q = 'latitude=' + coords[0] + '&longitude=' + coords[1] +
      '&elevation=' + (coords[2] || 0) +
      '&current=temperature_2m,wind_speed_10m,precipitation' +
      '&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,sunrise,sunset' +
      '&forecast_days=3&timezone=auto';
    fetch('https://api.open-meteo.com/v1/forecast?' + q).then(function (r) { return r.json(); }).then(function (j) {
      if (!j || !j.current || !j.daily) throw new Error('bad payload');
      var c = j.current, d = j.daily;
      var unit = lang === 'en' ? '°F' : '°C';
      var tUnit = function (v) { return Math.round(v) + unit; };
      var windU = (j.current_units && j.current_units.wind_speed_10m) || 'km/h';
      var h = '<div class="dib-w-now"><span class="dib-w-temp">' + tUnit(c.temperature_2m) + '</span>' +
        '<span class="dib-w-meta">' + esc(T2.now) + ' · ' + esc(T2.feels) + ' ' + Math.round(c.wind_speed_10m) + ' ' + esc(windU) +
        ' · ' + esc(T2.precip) + ' ' + (c.precipitation || 0) + 'mm</span></div>';
      h += '<div class="dib-w-days">';
      for (var i = 0; i < 3; i++) {
        h += '<div class="dib-w-day"><span class="dib-w-day-l">' + esc(T2.days[i]) + '</span>' +
          '<span class="dib-w-day-v">' + tUnit(d.temperature_2m_min[i]) + ' ~ ' + tUnit(d.temperature_2m_max[i]) + '</span>' +
          '<span class="dib-w-day-p">' + (d.precipitation_sum[i] || 0) + 'mm</span></div>';
      }
      h += '</div>';
      var sr = (d.sunrise[0] || '').slice(11), ss = (d.sunset[0] || '').slice(11);
      h += '<div class="dib-w-sun">' + esc(T2.sunrise) + ' ' + esc(sr) + ' · ' + esc(T2.sunset) + ' ' + esc(ss) + '</div>';
      h += '<div class="dib-dyn-src">' + esc(T2.srcWeather) + ' (CC BY 4.0)</div>';
      body.innerHTML = h;
    }).catch(function () {
      if (card && card.parentNode) card.parentNode.removeChild(card);
    });
  }

  /* 2) 실측 등산로 지도 — OSM 트랙(사전 수집) + Leaflet 지연 로드 */
  var LEAFLET_CSS = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
  var LEAFLET_JS = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
  var leafletPromise = null;
  function loadLeaflet() {
    if (window.L) return Promise.resolve();
    if (leafletPromise) return leafletPromise;
    leafletPromise = new Promise(function (resolve, reject) {
      var link = document.createElement('link');
      link.rel = 'stylesheet'; link.href = LEAFLET_CSS;
      document.head.appendChild(link);
      var s = document.createElement('script');
      s.src = LEAFLET_JS;
      s.onload = function () { resolve(); };
      s.onerror = function () { leafletPromise = null; reject(new Error('leaflet failed')); };
      document.head.appendChild(s);
    });
    return leafletPromise;
  }

  var ROUTE_COLORS = ['#0ea5e9', '#f59e0b', '#10b981'];

  function initTrackMap(coords) {
    if (!window.fetch) return;
    fetch(PFX + 'assets/data/tracks/' + id + '.json').then(function (r) {
      if (!r.ok) throw new Error('no track');
      return r.json();
    }).then(function (tj) {
      if (!tj || !tj.routes || !tj.routes.length) throw new Error('empty');
      var card = addCard('location', T2.track, T2.trackSub);
      var mapDiv = document.createElement('div');
      mapDiv.className = 'dib-map';
      var leg = '<div class="dib-map-legend">';
      tj.routes.forEach(function (rt, i) {
        leg += '<span class="dib-map-leg"><i style="background:' + ROUTE_COLORS[i % 3] + '"></i>' +
          esc(rt.name) + ' · ' + fmtKm(rt.km) + ' (' + esc(T2.measured) + ')</span>';
      });
      leg += '</div>';
      var prof = '<div class="dib-profile-wrap" hidden></div>';
      card.appendChild(mapDiv);
      card.insertAdjacentHTML('beforeend', leg + prof + '<div class="dib-dyn-src">' + esc(tj.attribution || T2.srcOsm) + '</div>');
      return loadLeaflet().then(function () {
        var map = L.map(mapDiv, { scrollWheelZoom: false, attributionControl: false });
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18 }).addTo(map);
        var bounds = [];
        tj.routes.forEach(function (rt, i) {
          var latlngs = rt.points.map(function (p) { return [p[0], p[1]]; });
          L.polyline(latlngs, { color: ROUTE_COLORS[i % 3], weight: 3.5, opacity: 0.9 }).addTo(map);
          if (latlngs.length) {
            L.circleMarker(latlngs[0], { radius: 5, color: '#17181c', weight: 1.5, fillColor: '#fff', fillOpacity: 1 })
              .bindTooltip(T2.start + ': ' + rt.name).addTo(map);
            bounds = bounds.concat(latlngs);
          }
        });
        if (bounds.length) map.fitBounds(bounds, { padding: [14, 14] });
        renderProfile(card.querySelector('.dib-profile-wrap'), tj);
      });
    }).catch(function () { /* 트랙 없음/오프라인 — 생략 */ });
  }

  /* 3) 실측 고도 프로파일 — 트랙 JSON에 profile(샘플 표고 배열)이 있으면 SVG 렌더 */
  function renderProfile(wrap, tj) {
    if (!wrap) return;
    var series = (tj.routes || []).filter(function (r) { return r.profile && r.profile.length > 4; });
    if (!series.length) return;
    wrap.hidden = false;
    var W = 560, H = 120, pad = 8;
    var html = '<div class="dib-profile-title">' + esc(T2.elevProfile) + '</div>';
    series.forEach(function (r, i) {
      var pts = r.profile;
      var min = Math.min.apply(null, pts), max = Math.max.apply(null, pts);
      var span = Math.max(1, max - min);
      var d = '';
      pts.forEach(function (v, k) {
        var x = pad + (W - 2 * pad) * k / (pts.length - 1);
        var y = H - pad - (H - 2 * pad) * (v - min) / span;
        d += (k ? 'L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1);
      });
      var color = ROUTE_COLORS[i % 3];
      html += '<svg class="dib-profile" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc(r.name) + '">' +
        '<path d="' + d + '" fill="none" stroke="' + color + '" stroke-width="2.5" stroke-linecap="round"/>' +
        '<text x="' + pad + '" y="' + (H - 1) + '" font-size="10" fill="currentColor" opacity=".65">' +
        esc(r.name) + ' · ' + Math.round(min) + '→' + Math.round(max) + 'm</text></svg>';
    });
    wrap.innerHTML = html;
  }

  var coords = (window.DEEP_COORDS || {})[id];
  if (coords) initWeather(coords);
  initTrackMap(coords);

  var style2 = document.createElement('style');
  style2.textContent =
    '.dib-dyn-sub{margin:0 0 10px;font-size:11.5px;font-weight:700;color:var(--dib-muted);}' +
    '.dib-dyn-src{margin-top:8px;font-size:10.5px;color:var(--dib-muted);opacity:.85;}' +
    '.dib-loading{font-size:12px;color:var(--dib-muted);}' +
    '.dib-w-now{display:flex;align-items:baseline;gap:10px;margin-bottom:8px;}' +
    '.dib-w-temp{font-size:26px;font-weight:800;color:var(--dib-text);letter-spacing:-.02em;}' +
    '.dib-w-meta{font-size:12px;color:var(--dib-muted);}' +
    '.dib-w-days{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:8px;}' +
    '.dib-w-day{background:var(--dib-surface2);border:1px solid var(--dib-border);border-radius:8px;padding:6px 8px;display:flex;flex-direction:column;gap:2px;}' +
    '.dib-w-day-l{font-size:10.5px;font-weight:700;color:var(--dib-muted);}' +
    '.dib-w-day-v{font-size:12.5px;font-weight:700;color:var(--dib-text);white-space:nowrap;}' +
    '.dib-w-day-p{font-size:10.5px;color:#0369a1;}' +
    '.dib-w-sun{font-size:11.5px;color:var(--dib-muted);}' +
    '.dib-map{height:240px;border-radius:10px;border:1px solid var(--dib-border);overflow:hidden;background:var(--dib-surface2);z-index:0;}' +
    '.dib-map-legend{margin-top:8px;display:flex;flex-direction:column;gap:3px;}' +
    '.dib-map-leg{font-size:11.5px;color:var(--dib-muted);display:flex;align-items:center;gap:6px;}' +
    '.dib-map-leg i{width:14px;height:3px;border-radius:2px;flex:none;}' +
    '.dib-profile-wrap{margin-top:8px;display:flex;flex-direction:column;gap:4px;}' +
    '.dib-profile-title{font-size:11.5px;font-weight:700;color:var(--dib-muted);}' +
    '.dib-profile{width:100%;height:auto;color:var(--dib-text);display:block;}';
  document.head.appendChild(style2);
})();
