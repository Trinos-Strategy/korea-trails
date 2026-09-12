/* MT Trails — Deep Info Band 공유 렌더러 (STANDARD-DEEP-INFO.md §3)
 * 마운트: <div id="deep-info-root" data-mountain="<id>"></div>
 * 데이터: window.DEEP_INFO[<id>] (assets/js/deep-info-data.js)
 * 템플릿 패밀리(seoraksan류/양명산류) 무관하게 자체 스코프 스타일로 렌더링한다.
 * JS가 로드되지 않으면 마운트 div가 비어 본문 코스 정보는 무손상이다.
 */
(function () {
  'use strict';

  var mount = document.getElementById('deep-info-root');
  if (!mount) return;

  var id = mount.getAttribute('data-mountain');
  var data = (window.DEEP_INFO || {})[id];
  if (!data || !data.sections || !data.sections.length) return;

  var TAG_CLASS = { '필수': 'dib-tag-required', '권장': 'dib-tag-warn', '참고': 'dib-tag-neutral' };
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
          '<svg class="dib-icon" aria-hidden="true"><use href="assets/icons/icons.svg#' + iconId + '"></use></svg>' +
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
    return '<footer class="dib-footer"><svg class="dib-icon dib-icon-sm" aria-hidden="true"><use href="assets/icons/icons.svg#icon-tip"></use></svg>' +
           ' 노선·요금·예약 창구는 변동될 수 있습니다. ' + parts.join(' — ') + '</footer>';
  }

  var root = document.createElement('section');
  root.className = 'deep-info-band';
  root.setAttribute('aria-label', '심화 탐방 정보');
  root.innerHTML =
    '<div class="dib-head">' +
      '<svg class="dib-icon dib-icon-lg" aria-hidden="true"><use href="assets/icons/icons.svg#icon-book"></use></svg>' +
      '<h2 class="dib-title">심화 탐방 정보</h2>' +
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
})();
