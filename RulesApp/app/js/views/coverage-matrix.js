// Repository Coverage Matrix (Stage 3, item 2). Purely a read view over
// index/coverage-matrix.json — document/chapter/regulation/paragraph-level
// presence, verification percentage, relationship completeness, and
// Engineering Object coverage, per standard and rolled up per package.
window.RulesCoverageMatrix = (function () {
  const DB = window.RulesDB;
  const R = window.RulesRender;
  let activePackage = '';

  function check(bool) { return bool ? '✓' : '·'; }

  function renderSummary(matrix) {
    const el = document.getElementById('matrix-summary');
    if (!el) return;
    el.innerHTML = matrix.packageSummary.map((p) => `
      <div class="stat-card">
        <div class="stat-value">${p.avgVerificationPct}%</div>
        <div class="stat-label">${R.esc(p.package)} — verification</div>
        <div class="muted" style="margin-top:6px;">${p.standardCount} standards · relationships ${p.avgRelationshipCompletenessPct}% · EO ${p.avgEngineeringObjectCoveragePct}%</div>
      </div>`).join('');
  }

  function renderFilterRow(matrix) {
    const el = document.getElementById('matrix-filter');
    if (!el || el._rendered) return;
    el._rendered = true;
    const packages = matrix.packageSummary.map((p) => p.package);
    el.innerHTML = `<button class="filter-btn active" data-pkg="">All packages</button>` +
      packages.map((p) => `<button class="filter-btn" data-pkg="${R.esc(p)}">${R.esc(p)}</button>`).join('');
    el.querySelectorAll('.filter-btn').forEach((btn) => btn.addEventListener('click', () => {
      el.querySelectorAll('.filter-btn').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      activePackage = btn.dataset.pkg;
      renderTable(matrix);
    }));
  }

  function renderTable(matrix) {
    const el = document.getElementById('matrix-table-wrap');
    if (!el) return;
    const rows = matrix.standards.filter((r) => !activePackage || r.package === activePackage)
      .slice().sort((a, b) => b.verificationPct - a.verificationPct || a.title.localeCompare(b.title));
    el.innerHTML = `<table class="stats-table">
      <thead><tr><th>Standard</th><th>Package</th><th>Doc</th><th>Chapter</th><th>Regulation</th><th>Paragraph</th><th>Verification</th><th>Relationships</th><th>EO coverage</th><th>Definitions</th></tr></thead>
      <tbody>${rows.map((r) => `
        <tr>
          <td><a href="#" class="xref matrix-link" data-id="${R.esc(r.id)}">${R.esc(r.title)}</a></td>
          <td>${R.esc(r.package)}</td>
          <td>${check(r.levels.documentLevel)}</td>
          <td>${check(r.levels.chapterLevel)}</td>
          <td>${check(r.levels.regulationLevel)}</td>
          <td>${check(r.levels.paragraphLevel)}</td>
          <td>${r.verificationPct}%</td>
          <td>${r.relationshipCompletenessPct}%</td>
          <td>${r.engineeringObjectCoveragePct}%</td>
          <td>${r.definitionsSourced}</td>
        </tr>`).join('')}</tbody>
    </table>`;
    el.querySelectorAll('.matrix-link').forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault(); window.RulesNav.showTab('search'); R.showDetail(a.dataset.id);
    }));
  }

  function init() {
    const matrix = DB.getCoverageMatrix();
    if (!matrix) {
      const el = document.getElementById('matrix-table-wrap');
      if (el) el.innerHTML = '<p class="muted">index/coverage-matrix.json not found — run repository/build/coverage-matrix.js.</p>';
      return;
    }
    renderSummary(matrix);
    renderFilterRow(matrix);
    renderTable(matrix);
  }

  return { init };
})();
