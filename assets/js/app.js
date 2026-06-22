/* -------------------------------------------------------------
   KOREA TRAILS — SHARED CLIENT LOGIC (app.js)
   ------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Unified Theme Management
  const themeBtn = document.getElementById('themeBtn');
  const docEl = document.documentElement;
  
  // Read theme from localStorage or system preferences
  let currentTheme = localStorage.getItem('theme');
  if (!currentTheme) {
    currentTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  docEl.setAttribute('data-theme', currentTheme);
  
  function updateThemeIcon() {
    if (!themeBtn) return;
    themeBtn.innerHTML = currentTheme === 'dark'
      ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`
      : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
  }
  
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
      docEl.setAttribute('data-theme', currentTheme);
      localStorage.setItem('theme', currentTheme);
      updateThemeIcon();
    });
  }
  updateThemeIcon();

  // 2. Playbook Tab Navigation & Accordion Setup
  // Global initializer for playbooks using the unified design system classes
  function initPlaybookComponents() {
    // Tabs
    document.querySelectorAll('.tabs').forEach(tablist => {
      const tabs = tablist.querySelectorAll('.tab');
      const panel = tablist.closest('.panel') || document.body;
      
      tabs.forEach(tab => {
        tab.addEventListener('click', () => {
          tabs.forEach(t => {
            t.classList.remove('active');
            t.setAttribute('aria-selected', 'false');
          });
          
          tab.classList.add('active');
          tab.setAttribute('aria-selected', 'true');
          
          const targetPaneId = tab.dataset.tab;
          panel.querySelectorAll('.tabpane').forEach(pane => {
            if (pane.dataset.pane === targetPaneId) {
              pane.classList.add('active');
            } else {
              pane.classList.remove('active');
            }
          });
        });
      });
    });

    // Accordions (Segments)
    document.querySelectorAll('.accordion').forEach(acc => {
      const header = acc.querySelector('.accordion-header');
      if (header) {
        header.addEventListener('click', () => {
          const isOpen = acc.classList.toggle('open');
          header.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
          const content = acc.querySelector('.accordion-content');
          if (content) {
            content.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
          }
        });
      }
    });
  }
  initPlaybookComponents();

  // 3. Search, Filters, and Sorting (Only for index.html)
  const gridContainer = document.getElementById('mountainGrid');
  if (gridContainer && window.MOUNTAINS) {
    const searchInput = document.getElementById('searchInput');
    const regionSelect = document.getElementById('regionSelect');
    const diffSelect = document.getElementById('diffSelect');
    const doneSelect = document.getElementById('doneSelect');
    const sortSelect = document.getElementById('sortSelect');
    const resultsCount = document.getElementById('resultsCount');

    const DIFF_LABEL = { easy: '초급', medium: '중급', hard: '고급', expert: '전문가' };
    const DIFF_CLASS = { easy: 'diff-easy', medium: 'diff-medium', hard: 'diff-hard', expert: 'diff-expert' };

    // Function to parse integer elevation (e.g. "1,708m" -> 1708)
    function parseElevation(altStr) {
      return parseInt(altStr.replace(/,/g, '').replace('m', ''), 10) || 0;
    }

    // Function to map difficulty to sortable weight
    function getDifficultyWeight(diff) {
      const weights = { easy: 1, medium: 2, hard: 3, expert: 4 };
      return weights[diff] || 0;
    }

    function renderFilteredGrid() {
      const query = (searchInput?.value || '').toLowerCase().trim();
      const region = regionSelect?.value || 'all';
      const difficulty = diffSelect?.value || 'all';
      const status = doneSelect?.value || 'all';
      const sort = sortSelect?.value || 'elevation-desc';

      // Apply Filters
      let filtered = window.MOUNTAINS.filter(m => {
        // Search query match
        const matchesQuery = m.name.toLowerCase().includes(query) || 
                             m.alt.toLowerCase().includes(query) || 
                             m.region.toLowerCase().includes(query) || 
                             m.desc.toLowerCase().includes(query);
        
        // Region filter
        const matchesRegion = region === 'all' || m.region === region || (region === 'korea' && m.region !== '대만');
        
        // Difficulty filter
        const matchesDiff = difficulty === 'all' || m.diff === difficulty;
        
        // Status filter
        const matchesStatus = status === 'all' || 
                              (status === 'done' && m.done) || 
                              (status === 'pending' && !m.done);

        return matchesQuery && matchesRegion && matchesDiff && matchesStatus;
      });

      // Apply Sorting
      filtered.sort((a, b) => {
        if (sort === 'elevation-desc') {
          return parseElevation(b.alt) - parseElevation(a.alt);
        } else if (sort === 'elevation-asc') {
          return parseElevation(a.alt) - parseElevation(b.alt);
        } else if (sort === 'name-asc') {
          return a.name.localeCompare(b.name, 'ko');
        } else if (sort === 'difficulty-asc') {
          return getDifficultyWeight(a.diff) - getDifficultyWeight(b.diff);
        } else if (sort === 'difficulty-desc') {
          return getDifficultyWeight(b.diff) - getDifficultyWeight(a.diff);
        }
        return 0;
      });

      // Update Results Counter
      if (resultsCount) {
        resultsCount.textContent = `검색 결과: ${filtered.length}개`;
      }

      // Handle Empty State
      if (filtered.length === 0) {
        gridContainer.innerHTML = `
          <div style="grid-column: 1/-1; text-align: center; padding: var(--space-12) 0; color: var(--muted);">
            <div style="font-size: 3rem; margin-bottom: var(--space-4);">🏔️</div>
            <h3 style="font-size: var(--text-lg); font-weight: 800; margin-bottom: var(--space-2); color: var(--text);">검색 조건에 맞는 산이 없습니다</h3>
            <p style="font-size: var(--text-sm); color: var(--muted);">다른 검색어나 필터 조건을 시도해보세요.</p>
          </div>
        `;
        return;
      }

      // Render Grid Cards
      gridContainer.innerHTML = filtered.map(m => `
        <article class="card card-hoverable mountain-card" style="padding: 0; overflow: hidden; display: flex; flex-direction: column;">
          <div class="card-thumbnail-wrap" style="position: relative; width: 100%; height: 180px; overflow: hidden; background-color: var(--surface2);">
            <picture>
              <source srcset="assets/img/${m.id}/g1-640.webp" type="image/webp">
              <img 
                src="assets/img/${m.id}/g1-640.jpg" 
                alt="${m.name} 등산로 전경" 
                class="card-thumbnail" 
                style="width: 100%; height: 100%; object-fit: cover; transition: transform var(--transition);" 
                loading="lazy" 
                decoding="async">
            </picture>
            <div style="position: absolute; top: var(--space-3); right: var(--space-3);">
              <span class="diff-badge ${DIFF_CLASS[m.diff]}">${DIFF_LABEL[m.diff]}</span>
            </div>
          </div>
          
          <div style="padding: var(--space-5); display: flex; flex-direction: column; flex-grow: 1;">
            <div style="display: flex; align-items: baseline; justify-content: space-between; margin-bottom: var(--space-2);">
              <h2 style="font-size: var(--text-lg); font-weight: 800; color: var(--text);">${m.name}</h2>
              <span style="font-size: 1.15rem; font-weight: 800; color: var(--primary); font-family: var(--font-display);">${m.alt}</span>
            </div>
            
            <div style="font-size: var(--text-xs); color: var(--muted); font-weight: 700; text-transform: uppercase; margin-bottom: var(--space-3);">
              📍 ${m.region}
            </div>
            
            <p style="font-size: var(--text-sm); color: var(--muted); margin-bottom: var(--space-4); line-height: 1.5; flex-grow: 1; word-break: keep-all;">
              ${m.desc}
            </p>
 
            <div style="display: flex; gap: var(--space-4); border-top: 1px solid var(--border); padding-top: var(--space-4); margin-bottom: var(--space-4);">
              <div style="flex: 1;">
                <div style="font-size: 10px; color: var(--muted); text-transform: uppercase; font-weight: 800;">거리</div>
                <div style="font-weight: 700; font-size: var(--text-sm); color: var(--text); margin-top: 2px;">🥾 ${m.dist}</div>
              </div>
              <div style="flex: 1;">
                <div style="font-size: 10px; color: var(--muted); text-transform: uppercase; font-weight: 800;">시간</div>
                <div style="font-weight: 700; font-size: var(--text-sm); color: var(--text); margin-top: 2px;">⏱ ${m.time}</div>
              </div>
            </div>

            <div>
              ${m.done
                ? `<a href="${m.url}" class="btn btn-primary" style="width: 100%; text-decoration: none;">🗺 플레이북 보기</a>`
                : `<div class="btn btn-secondary" style="width: 100%; cursor: not-allowed; opacity: 0.6;">⏳ 플레이북 준비 중</div>`
              }
            </div>
          </div>
        </article>
      `).join('');
    }

    // Bind event listeners
    [searchInput, regionSelect, diffSelect, doneSelect, sortSelect].forEach(element => {
      if (!element) return;
      element.addEventListener('change', () => {
        saveStateToUrl();
        renderFilteredGrid();
      });
    });

    if (searchInput) {
      // Debounced search for smoother user experience
      let debounceTimeout;
      searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
          saveStateToUrl();
          renderFilteredGrid();
        }, 150);
      });
    }

    // URL State management
    function saveStateToUrl() {
      const params = new URLSearchParams();
      if (searchInput?.value) params.set('q', searchInput.value);
      if (regionSelect?.value && regionSelect.value !== 'all') params.set('r', regionSelect.value);
      if (diffSelect?.value && diffSelect.value !== 'all') params.set('d', diffSelect.value);
      if (doneSelect?.value && doneSelect.value !== 'all') params.set('s', doneSelect.value);
      if (sortSelect?.value && sortSelect.value !== 'elevation-desc') params.set('sort', sortSelect.value);
      
      const newUrl = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
      window.history.replaceState({}, '', newUrl);
    }

    function loadStateFromUrl() {
      const params = new URLSearchParams(window.location.search);
      if (params.has('q') && searchInput) searchInput.value = params.get('q');
      if (params.has('r') && regionSelect) regionSelect.value = params.get('r');
      if (params.has('d') && diffSelect) diffSelect.value = params.get('d');
      if (params.has('s') && doneSelect) doneSelect.value = params.get('s');
      if (params.has('sort') && sortSelect) sortSelect.value = params.get('sort');
    }

    // Initial render
    loadStateFromUrl();
    renderFilteredGrid();
  }
});
