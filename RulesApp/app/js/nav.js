// UI shell: tab router between primary engineering screens and secondary
// maintenance views, dark-mode toggle, print button, and browse tree.
window.RulesNav = (function () {
  const DB = window.RulesDB;
  const R = window.RulesRender;
  const TABS = ['search', 'crossref', 'engineering', 'illustrations', 'study', 'timeline', 'stats', 'editorial', 'diff', 'expansion', 'matrix'];
  const initialized = {};

  function showTab(tab) {
    if (!TABS.includes(tab)) tab = 'search';
    TABS.forEach((t) => {
      const screen = document.getElementById('screen-' + t);
      const btn = document.querySelector(`[data-tab="${t}"]`);
      if (screen) screen.classList.toggle('active', t === tab);
      if (btn) btn.classList.toggle('active', t === tab);
    });
    if (location.hash !== '#tab=' + tab) history.replaceState(null, '', '#tab=' + tab);
    if (!initialized[tab]) {
      initialized[tab] = true;
      if (tab === 'crossref') window.RulesCrossref && window.RulesCrossref.init();
      else if (tab === 'engineering') window.RulesEngineering && window.RulesEngineering.init();
      else if (tab === 'illustrations') window.RulesIllustrations && window.RulesIllustrations.init();
      else if (tab === 'study') window.RulesStudy && window.RulesStudy.init();
      else if (tab === 'timeline') window.RulesTimeline && window.RulesTimeline.init();
      else if (tab === 'stats') window.RulesStats && window.RulesStats.render();
      else if (tab === 'editorial') window.RulesEditorial && window.RulesEditorial.init();
      else if (tab === 'diff') window.RulesDiffViewer && window.RulesDiffViewer.init();
      else if (tab === 'expansion') window.RulesExpansion && window.RulesExpansion.init();
      else if (tab === 'matrix') window.RulesCoverageMatrix && window.RulesCoverageMatrix.init();
    }
    // Close maintenance dropdown if open
    const menu = document.getElementById('maint-menu');
    if (menu) menu.style.display = 'none';
  }

  function updateThemeLabel(theme) {
    const btn = document.getElementById('theme-toggle');
    if (btn) btn.textContent = theme === 'dark' ? '☀ Light mode' : '🌙 Dark mode';
  }

  function initDarkMode() {
    const stored = localStorage.getItem('rulesapp-theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = stored || (prefersDark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
    updateThemeLabel(theme);
    const btn = document.getElementById('theme-toggle');
    if (btn) btn.addEventListener('click', () => {
      const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('rulesapp-theme', next);
      updateThemeLabel(next);
    });
  }

  function initPrint() {
    const btn = document.getElementById('print-btn');
    if (btn) btn.addEventListener('click', () => window.print());
  }

  function initTabs() {
    document.querySelectorAll('[data-tab]').forEach((btn) => btn.addEventListener('click', () => showTab(btn.dataset.tab)));
    
    // Maintenance Dropdown Toggle
    const dropBtn = document.getElementById('maint-dropdown-btn');
    const menu = document.getElementById('maint-menu');
    if (dropBtn && menu) {
      dropBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
      });
      document.addEventListener('click', () => { menu.style.display = 'none'; });
    }

    const m = location.hash.match(/tab=([a-z]+)/);
    showTab(m ? m[1] : 'search');
  }

  function renderBrowseTree() {
    const container = document.getElementById('browse-tree');
    if (!container || container._rendered) return;
    container._rendered = true;
    const cov = DB.getCoverage();
    const pkgNames = Object.keys(cov.packages || {}).sort();
    container.innerHTML = pkgNames.map((pkg) => {
      const rows = cov.packages[pkg].slice().sort((a, b) => a.title.localeCompare(b.title));
      return `<details class="browse-pkg">
        <summary>${R.esc(pkg)} <span class="muted">(${rows.length})</span></summary>
        <ul class="browse-list">${rows.map((r) => `<li><a href="#" class="xref browse-link" data-id="${R.esc(r.id)}">${R.esc(r.title)}</a> ${R.statusBadge(r.status)}</li>`).join('')}</ul>
      </details>`;
    }).join('');
    container.querySelectorAll('.browse-link').forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault();
      R.showDetail(a.dataset.id);
      document.getElementById('detail-panel').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }));
  }

  function initSubtabs() {
    document.querySelectorAll('.subtab-btn').forEach((btn) => btn.addEventListener('click', () => {
      document.querySelectorAll('.subtab-btn').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const mode = btn.dataset.subtab;
      document.getElementById('result-list-wrap').classList.toggle('active', mode === 'search');
      document.getElementById('browse-tree-wrap').classList.toggle('active', mode === 'browse');
      if (mode === 'browse') renderBrowseTree();
    }));
  }

  function init() {
    initDarkMode();
    initPrint();
    initSubtabs();
    initTabs();
  }

  return { init, showTab };
})();
