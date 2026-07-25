// Repository Diff Viewer (Stage 2B, item 4). The diff itself is computed at
// build time by repository/build/diff-report.js (which shells out to git —
// something a static browser app cannot do); this view only lists and
// renders whatever pre-generated diff reports exist under
// repository/index/diffs/*.json.
window.RulesDiffViewer = (function () {
  const DB = window.RulesDB;
  const R = window.RulesRender;
  let currentReport = null;

  function populateSelect() {
    const sel = document.getElementById('diff-select');
    if (!sel || sel._populated) return;
    sel._populated = true;
    const manifest = DB.getDiffManifest();
    if (!manifest.length) {
      sel.innerHTML = '<option value="">No diff reports generated yet</option>';
      return;
    }
    sel.innerHTML = manifest.map((m) => `<option value="${R.esc(m.file)}">${R.esc(m.standardTitle)} — ${R.esc(m.fromRef)} → ${R.esc(m.toRef)}</option>`).join('');
    sel.addEventListener('change', () => loadAndRender(sel.value));
  }

  function nodeRow(n) { return `<div class="reg-item"><span class="reg-code">${R.esc(n.level)} ${R.esc(n.label)}</span><a href="#" class="xref reg-desc diff-link" data-id="${R.esc(n.id)}">${R.esc(n.title)}</a></div>`; }

  function render(report) {
    const container = document.getElementById('diff-content');
    if (!container) return;
    container.innerHTML = `
      <div class="diff-header">
        <div class="diff-flow"><span class="diff-node">${R.esc(report.standardTitle)}</span><span class="diff-arrow">↓</span><span class="diff-node diff-from">${R.esc(report.fromRef)}</span><span class="diff-arrow">↓</span><span class="diff-node diff-to">Current Repository (${R.esc(report.toRef)})</span></div>
        <p class="muted">Generated ${R.esc(report.generatedAt)} by repository/build/diff-report.js. Compares ${R.esc(report.standardId)}'s decomposed tree between the two git refs shown above.</p>
      </div>
      <div class="stats-grid">
        ${['newNodes', 'removedNodes', 'modifiedNodes', 'nodesWithNewRelationships', 'changedDefinitionFiles', 'changedEngineeringObjectFiles'].map((k) => `<div class="stat-card"><div class="stat-value">${report.summary[k]}</div><div class="stat-label">${R.esc(k)}</div></div>`).join('')}
      </div>
      <h4 class="diff-new">New regulations (${report.newNodes.length})</h4>
      <div class="reg-box">${report.newNodes.length ? report.newNodes.map(nodeRow).join('') : '<div class="reg-item muted">None.</div>'}</div>
      <h4 class="diff-removed">Removed regulations (${report.removedNodes.length})</h4>
      <div class="reg-box">${report.removedNodes.length ? report.removedNodes.map(nodeRow).join('') : '<div class="reg-item muted">None.</div>'}</div>
      <h4 class="diff-modified">Modified summaries / citations / provenance / validity (${report.modifiedNodes.length})</h4>
      <div class="reg-box">${report.modifiedNodes.length ? report.modifiedNodes.map((m) => `<div class="reg-item"><a href="#" class="xref reg-code diff-link" data-id="${R.esc(m.id)}">${R.esc(m.title)}</a><span class="reg-desc">changed: ${m.changedFields.map(R.esc).join(', ')}</span></div>`).join('') : '<div class="reg-item muted">None.</div>'}</div>
      <h4 class="diff-new">New relationships (${report.newRelationships.length} node(s) affected)</h4>
      <div class="reg-box">${report.newRelationships.length ? report.newRelationships.map((r) => `<div class="reg-item"><a href="#" class="xref reg-code diff-link" data-id="${R.esc(r.id)}">${R.esc(r.title)}</a><span class="reg-desc">+${r.added.map((a) => a.type + ' → ' + a.targetId).join(', ')}</span></div>`).join('') : '<div class="reg-item muted">None.</div>'}</div>
      <h4 class="diff-new">New/changed definitions referencing this standard (${report.newOrChangedDefinitions.length})</h4>
      <div class="reg-box">${report.newOrChangedDefinitions.length ? report.newOrChangedDefinitions.map((f) => `<div class="reg-item">${R.esc(f)}</div>`).join('') : '<div class="reg-item muted">None.</div>'}</div>
      <h4 class="diff-new">New/changed engineering objects referencing this standard (${report.newOrChangedEngineeringObjects.length})</h4>
      <div class="reg-box">${report.newOrChangedEngineeringObjects.length ? report.newOrChangedEngineeringObjects.map((f) => `<div class="reg-item">${R.esc(f)}</div>`).join('') : '<div class="reg-item muted">None.</div>'}</div>
    `;
    container.querySelectorAll('.diff-link').forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault(); window.RulesNav.showTab('search'); R.showDetail(a.dataset.id);
    }));
  }

  function loadAndRender(fileName) {
    if (!fileName) return;
    const container = document.getElementById('diff-content');
    if (container) container.innerHTML = '<p class="muted">Loading…</p>';
    DB.fetchDiffReport(fileName).then((report) => { currentReport = report; render(report); });
  }

  function init() {
    populateSelect();
    const sel = document.getElementById('diff-select');
    if (sel && sel.value) loadAndRender(sel.value);
  }

  return { init };
})();
