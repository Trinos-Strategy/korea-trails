# Korea Trails — UX & Typography Critique Report

This report presents an objective evaluation of the scannability, information hierarchy, and visual density of representative pages in the **Korea Trails** project. Headless Chrome was used to render each page under both Desktop (1440x900) and Mobile (375x812) viewports.

---

## 📊 Summary Scorecard

The pages were evaluated on a scale of **1 (Poor)** to **5 (Excellent)** across the following 6 specific criteria:
1. **Core course stats** (Scannability & horizontal layout vs. vertical pile)
2. **Segment difficulty** (Horizontal bar/meter vs. vertical list)
3. **Section navigation tabs** (Clear horizontal tab bar vs. text run/unstyled buttons)
4. **Icon uniformity** (Unified SVGs vs. raw emojis)
5. **Video grid layout** (Responsive horizontal grid vs. vertical 1-column stack)
6. **General typography and hierarchy** (Contrast, margins, line lengths, headings)

| Representative Page | Core Stats | Segment Difficulty | Navigation Tabs | Icon Uniformity | Video Grid | Typography & Hierarchy | **Average Score** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. index.html** (Home) | N/A | N/A | N/A | 5.0 | N/A | 4.5 | **4.75 / 5.0** |
| **2. seoraksan-playbook.html** | 4.0 | 5.0 | 1.0 | 2.0 | N/A | 4.0 | **3.20 / 5.0** |
| **3. en/seoraksan-playbook.html** | 4.0 | 5.0 | 1.0 | 2.0 | N/A | 4.0 | **3.20 / 5.0** |
| **4. bukhansan-playbook.html** | 3.5 | 4.0 | 1.0 | 2.0 | 1.0 | 3.5 | **2.50 / 5.0** |
| **5. dobongsan-playbook.html** | 3.5 | 4.0 | 1.0 | 2.0 | 1.0 | 3.0 | **2.42 / 5.0** |
| **6. soyosan-playbook.html** | 3.5 | 4.0 | 1.0 | 2.0 | 5.0 | 4.0 | **3.25 / 5.0** |

---

## 🔍 Detailed Page-by-Page Evaluation

### 1. index.html (Main Home Page)
* **Desktop Screenshot:** ![Index Desktop](/Users/mac/.gemini/antigravity/brain/c45f32ec-0ee9-4156-a062-5e46518c5616/index_desktop.png)
* **Mobile Screenshot:** ![Index Mobile](/Users/mac/.gemini/antigravity/brain/c45f32ec-0ee9-4156-a062-5e46518c5616/index_mobile.png)

* **Core Course Stats:** **N/A** (Landing page lists mountains, does not display detailed course stats).
* **Segment Difficulty:** **N/A**.
* **Section Navigation Tabs:** **N/A**.
* **Icon Uniformity:** **5.0/5.0**. The index page uses unified SVG icons (`#icon-mountain`, `#icon-location`, `#icon-lightning`, `#icon-book`) retrieved from the unified system asset `assets/icons/icons.svg`. No raw emojis are used.
* **Video Grid Layout:** **N/A**.
* **Typography & Hierarchy:** **4.5/5.0**. Uses Satoshi and Cabinet Grotesk fonts correctly. Strong typographic contrast (dark background hero overlay, clean light background grids). Responsive grids wrap nicely. Hero input has proper focus styles and fallback themes.

---

### 2. seoraksan-playbook.html (KR Pilot)
* **Desktop Screenshot:** ![Seoraksan Desktop](/Users/mac/.gemini/antigravity/brain/c45f32ec-0ee9-4156-a062-5e46518c5616/seoraksan_desktop.png)
* **Mobile Screenshot:** ![Seoraksan Mobile](/Users/mac/.gemini/antigravity/brain/c45f32ec-0ee9-4156-a062-5e46518c5616/seoraksan_mobile.png)

* **Core Course Stats:** **4.0/5.0**. Course distance, duration, elevation, calories, season, and difficulty are rendered horizontally in a flex container (`.course-stats-summary`) using `.stat-pill` classes. Highly scannable on desktop and mobile. However, Transit details are not integrated into this block and are placed vertically in a separate "Transportation Information" card under the Tips tab.
* **Segment Difficulty:** **5.0/5.0**. Renders as a clear, responsive horizontal segment difficulty meter (`.difficulty-meter`) with 5 colored segments indicating level (e.g. green for Easy, gold for Medium).
* **Section Navigation Tabs:** **1.0/5.0**. On desktop viewports (>= 1280px), tabs are hidden (`display: none !important`), and all sections (Overview, Route, Map, Tips) display sequentially. However, on mobile/tablet viewports (< 1280px), the `.tab-bar` and `.tab-btn` elements are rendered. There is **no CSS styling** in `design-system.css` or the file itself for these components. The tab bar renders as a raw, browser-default unstyled list of grey buttons.
* **Icon Uniformity:** **2.0/5.0**. Mixes SVG icons with raw emojis. The stats pills use raw emojis (📏, ⏱, 📈, 🔥, ⭐, 🍂) instead of unified SVGs. Meanwhile, the tab buttons and other sections use the unified SVG icon system.
* **Video Grid Layout:** **N/A** (Nae-Oeseorak Playbook does not contain a trekking video grid).
* **Typography & Hierarchy:** **4.0/5.0**. Strong vertical reading flow, excellent responsive grid columns for the Tips block. The 2-column split layout on desktop works well, though sequentially rendering all tabs makes the page length extremely long.

---

### 3. en/seoraksan-playbook.html (EN Pilot)
* **Desktop Screenshot:** ![EN Seoraksan Desktop](/Users/mac/.gemini/antigravity/brain/c45f32ec-0ee9-4156-a062-5e46518c5616/seoraksan_en_desktop.png)
* **Mobile Screenshot:** ![EN Seoraksan Mobile](/Users/mac/.gemini/antigravity/brain/c45f32ec-0ee9-4156-a062-5e46518c5616/seoraksan_en_mobile.png)

* **Core Course Stats:** **4.0/5.0**. Same implementation as the Korean pilot.
* **Segment Difficulty:** **5.0/5.0**. Same horizontal segment bar.
* **Section Navigation Tabs:** **1.0/5.0**. Same unstyled `.tab-bar` and `.tab-btn` on mobile.
* **Icon Uniformity:** **2.0/5.0**. Same raw emojis (📏, ⏱, 📈, 🔥, ⭐, 🍂, 🅿) used within stats lists and timeline chips.
* **Video Grid Layout:** **N/A**.
* **Typography & Hierarchy:** **4.0/5.0**. Renders clean Cabinet Grotesk headings. Excellent localized copy lines.

---

### 4. bukhansan-playbook.html (Bukhansan Page)
* **Desktop Screenshot:** ![Bukhansan Desktop](/Users/mac/.gemini/antigravity/brain/c45f32ec-0ee9-4156-a062-5e46518c5616/bukhansan_desktop.png)
* **Mobile Screenshot:** ![Bukhansan Mobile](/Users/mac/.gemini/antigravity/brain/c45f32ec-0ee9-4156-a062-5e46518c5616/bukhansan_mobile.png)

* **Core Course Stats:** **3.5/5.0**. Uses vertical card layout for KPIs (`.kpi-card`) instead of the horizontal `.stat-pill`s. This changes the structural density and is less uniform with the Seoraksan pilot. Transit details are located in tables further down the page.
* **Segment Difficulty:** **4.0/5.0**. The route guide timeline uses text chips with raw emojis (🟢 쉬움, 🟡 보통, 🔴 가파름) instead of the horizontal segment difficulty meter.
* **Section Navigation Tabs:** **1.0/5.0**. Uses `.tabs-nav` and `.tab-btn` classes, which are completely unstyled. On mobile, they render as raw, unaligned grey browser buttons.
* **Icon Uniformity:** **2.0/5.0**. Extensively uses raw emojis (📏, ⏱, 🟢, 🟡, 🔴) inside the KPI lists and timeline items, violating the unified SVG design system.
* **Video Grid Layout:** **1.0/5.0**. The trekking video section uses a container `.video-grid` and items `.video-card`. However, **no CSS styles exist** for these classes in the stylesheet or the file itself. As a result, the videos stack vertically in a single column on both desktop and mobile, leading to massive unused white space on desktop and excessive scrolling.
* **Typography & Hierarchy:** **3.5/5.0**. Header styling and font stack are correct, but because the video grids are not styled, they create a broken visual hierarchy on desktop.

---

### 5. dobongsan-playbook.html (Dobongsan Page)
* **Desktop Screenshot:** ![Dobongsan Desktop](/Users/mac/.gemini/antigravity/brain/c45f32ec-0ee9-4156-a062-5e46518c5616/dobongsan_desktop.png)
* **Mobile Screenshot:** ![Dobongsan Mobile](/Users/mac/.gemini/antigravity/brain/c45f32ec-0ee9-4156-a062-5e46518c5616/dobongsan_mobile.png)

* **Core Course Stats:** **3.5/5.0**. Same vertical KPI grid cards as Bukhansan, deviating from Seoraksan's horizontal scannable pills.
* **Segment Difficulty:** **4.0/5.0**. Uses text-based difficulty tags (🟢 쉬움, 🟡 보통, 🔴 암벽) instead of the visual segment meter.
* **Section Navigation Tabs:** **1.0/5.0**. Same unstyled `.tab-btn` buttons, rendering as unaligned default browser elements on mobile.
* **Icon Uniformity:** **2.0/5.0**. Inconsistent emoji usage (📏, ⏱, 🟢, 🟡, 🔴) mixed with SVGs.
* **Video Grid Layout:** **1.0/5.0**. Same as Bukhansan: Dobongsan features many YouTube Shorts videos, but because **`.video-grid` has no CSS styling**, the videos stack vertically in a single-column layout. On desktop, this makes the page extremely long and renders a single vertical column of giant cards next to wide empty spaces.
* **Typography & Hierarchy:** **3.0/5.0**. Due to the unstyled video elements and the sequential rendering of all tabs, the page length is excessively long, causing major scrolling fatigue.

---

### 6. soyosan-playbook.html (Soyosan Page)
* **Desktop Screenshot:** ![Soyosan Desktop](/Users/mac/.gemini/antigravity/brain/c45f32ec-0ee9-4156-a062-5e46518c5616/soyosan_desktop.png)
* **Mobile Screenshot:** ![Soyosan Mobile](/Users/mac/.gemini/antigravity/brain/c45f32ec-0ee9-4156-a062-5e46518c5616/soyosan_mobile.png)

* **Core Course Stats:** **3.5/5.0**. Same vertical KPI card grid layout.
* **Segment Difficulty:** **4.0/5.0**. Uses text-based emoji chips.
* **Section Navigation Tabs:** **1.0/5.0**. Same unstyled `.tab-btn` on mobile viewports.
* **Icon Uniformity:** **2.0/5.0**. Uses raw emojis instead of SVG icons in the stats block.
* **Video Grid Layout:** **5.0/5.0**. Unlike Dobongsan and Bukhansan, Soyosan has **local `.video-grid` and `.video-card` styling** inside the file. This creates a highly responsive horizontal grid (multiple columns on desktop, 2 columns on mobile), resulting in a compact, highly scannable layout despite having 14 video cards.
* **Typography & Hierarchy:** **4.0/5.0**. The responsive video grid keeps the visual density clean and professional. The 2-column split layout works well.

---

## 🚨 Identified Defects & Action Items

### P0 Defects (Critical / Must Fix)
1. **Unstyled Navigation Tabs on Mobile/Tablet (`.tab-bar` / `.tabs-nav` / `.tab-btn`):**
   * **Impact:** High visual and functional bug. On screens narrower than 1280px, the tabs are shown but appear as unstyled, default browser grey buttons, which ruins the premium aesthetic.
   * **Affected Pages:** `seoraksan-playbook.html`, `en/seoraksan-playbook.html`, `bukhansan-playbook.html`, `dobongsan-playbook.html`, `soyosan-playbook.html`.
   * **Solution:** Implement a unified `.tabs` and `.tab` style in the design system CSS and apply it across all pages to match the standard tab bar design.

2. **Missing CSS for Video Grids in Bukhansan and Dobongsan (`.video-grid`):**
   * **Impact:** Severe layout breakage on desktop. 14 videos on Dobongsan stack vertically in a single column, leading to massive layout imbalance and long scroll lengths.
   * **Affected Pages:** `bukhansan-playbook.html`, `dobongsan-playbook.html`.
   * **Solution:** Port the responsive `.video-grid` CSS rules from `soyosan-playbook.html` or `en/bukhansan-playbook.html` into `design-system.css` so all pages render videos in a responsive horizontal grid.

---

### P1 Defects (Important / Should Fix)
1. **Icon Inconsistency (Raw Emojis vs. SVGs):**
   * **Impact:** Lowers the visual quality. Raw emojis (📏, ⏱, 📈, 🔥, ⭐, 🍂) render differently across OS platforms (Android, iOS, Windows, macOS) and clash with the professional SVG icons.
   * **Affected Pages:** All playbook pages.
   * **Solution:** Replace all raw emojis inside stats boxes, KPI cards, and route chips with unified SVG `<svg><use href="..."></use></svg>` icons pointing to the unified asset file.

2. **Layout Inconsistency in Core Stats Panels:**
   * **Impact:** Poor uniformity across the catalog. Seoraksan uses horizontal pills (`.stat-pill`), whereas Bukhansan, Dobongsan, and Soyosan use vertical `.kpi-card` blocks.
   * **Affected Pages:** `bukhansan-playbook.html`, `dobongsan-playbook.html`, `soyosan-playbook.html`.
   * **Solution:** Standardize on Seoraksan's horizontal `.stat-pill` layout in `design-system.css`.
