// Editorial Dashboard (Stage 2B, item 1) + Repository QA Reports (item 2).
// Purely a read/aggregate view over index/health-check.json,
// index/workflow-status.json, index/integrity-report.json, index/coverage.json,
// and repository/CHANGELOG.json — computes nothing that isn't already true of
// the last build; "recently modified" is the one panel that couldn't exist
// without Change Tracking (item 3), since a static offline app has no other
// way to know what changed when.
window.RulesEditorial = (function () {
  const DB = window.RulesDB;
  const R = window.RulesRender;

  function cap(list, n) {
    n = n || 30;
    const shown = list.slice(0, n);
    return { shown, truncated: list.length > n, total: list.length };
  }

  function listSection(title, items, formatter, emptyMsg) {
    if (!items || !items.length) return `<div class="ed-card"><h4>${R.esc(title)} <span class="ed-count">0</span></h4><p class="muted">${R.esc(emptyMsg || 'None found.')}</p></div>`;
    const { shown, truncated, total } = cap(items);
    return `<div class="ed-card"><h4>${R.esc(title)} <span class="ed-count">${total}</span></h4>
      <div class="reg-box">${shown.map(formatter).join('')}</div>
      ${truncated ? `<p class="muted">Showing ${shown.length} of ${total} — see the full list in the exported JSON report.</p>` : ''}
    </div>`;
  }

  function idLink(id) { return `<a href="#" class="xref ed-link" data-id="${R.esc(id)}">${R.esc(R.titleOf(id) || id)}</a>`; }

  // ---------- Editorial Dashboard ----------
  function renderDashboard() {
    const container = document.getElementById('editorial-dashboard');
    if (!container) return;
    const health = DB.getHealthCheck();
    const changes = DB.getRecentChanges(15);
    const wfCounts = DB.getWorkflowCounts();
    const eoCount = DB.getEngineeringObjects().length;

    const recentHtml = changes.length ? changes.map((c) => `
      <div class="reg-item"><span class="reg-code">${R.esc(c.date.slice(0, 10))}</span>
        <span>${R.esc(c.author)} — ${R.esc(c.reason)}</span>
        <span class="ed-tag">${R.esc(c.package)}</span>
        <span class="ed-tag ${c.validation && c.validation.passed ? 'ed-pass' : 'ed-fail'}">${c.validation && c.validation.passed ? 'validated' : 'validation failed'}</span>
        ${c.touchedStandardIds.length ? '<span class="ed-touched">' + c.touchedStandardIds.slice(0, 6).map(idLink).join(', ') + '</span>' : ''}
      </div>`).join('') : '<p class="muted">No changelog entries yet.</p>';

    container.innerHTML = `
      <div class="ed-card ed-card-wide"><h4>Recently modified <span class="ed-count">${DB.getChangelog().length} total change(s) logged</span></h4>${recentHtml}</div>

      <div class="ed-card ed-card-wide"><h4>Editorial workflow state distribution</h4>
        <div class="bar-list">${Object.keys(wfCounts).map((k) => `<div class="bar-row"><div class="bar-label">${R.esc(k)}</div><div class="bar-track"><div class="bar-fill" style="width:${Math.round((wfCounts[k] / Math.max(1, Object.values(wfCounts).reduce((a, b) => a + b, 0))) * 100)}%"></div></div><div class="bar-count">${wfCounts[k]}</div></div>`).join('')}</div>
      </div>

      ${listSection('Standards & nodes awaiting verification', health.awaitingVerification.sample, idLink)}
      ${listSection('AI-drafted summaries awaiting human review', health.aiAwaitingReview.sample, idLink)}
      ${listSection('Missing / invalid provenance', health.invalidProvenance, (x) => `<div class="reg-item"><span>${R.esc(x.owner)}</span><span class="reg-desc">${R.esc(x.issue)}</span></div>`)}
      <div class="ed-card"><h4>Missing validity metadata <span class="ed-count">${health.missingValidity.standards + health.missingValidity.nodes}</span></h4>
        <p class="muted">${health.missingValidity.standards}/${health.missingValidity.standardsTotal} standards and ${health.missingValidity.nodes}/${health.missingValidity.nodesTotal} nodes have no structured validity metadata yet.</p></div>
      ${listSection('"Definitions" nodes not yet mined into the definitions registry', health.definitionsGapNodes, (x) => `<div class="reg-item">${idLink(x.nodeId)}<span class="reg-desc">in ${R.esc(x.standardId)}</span></div>`)}
      <div class="ed-card"><h4>Missing engineering objects <span class="ed-count">${eoCount} defined</span></h4>
        <p class="muted">Detecting which real-world equipment concepts SHOULD have an Engineering Object but don't requires editorial judgment, not just data — there is no ground-truth list to check against, so this is a qualitative note rather than an automatic list. Currently ${eoCount} engineering object(s) are defined against 78 standards; expanding this set is ordinary future content work, not a bug.</p></div>
      ${listSection('Missing relationships (no outgoing or incoming edges)', health.unconnectedItems, idLink, 'Every item has at least one relationship.')}
      ${listSection('Asymmetric Engineering Object relationships (node points at an EO the EO does not reciprocate)', health.asymmetricEORelationships, (x) => `<div class="reg-item">${idLink(x.nodeId)}<span class="reg-desc">${R.esc(x.nodeTitle)} -- not yet in ${R.esc(x.eoId)}'s relatedNodes</span></div>`, 'Every node that relates to an Engineering Object is reciprocated in that object relatedNodes list.')}
      ${listSection('Unresolved declared extensions (relatedExtensions entry whose file targets a node not in relatedNodes -- will silently never render, TD-5)', health.unresolvedDeclaredExtensions, (x) => `<div class="reg-item">${idLink(x.eoId)}<span class="reg-desc">${R.esc(x.declaredExtension)} targets ${idLink(x.targetNodeId)}, not yet in relatedNodes</span></div>`, 'Every declared extension resolves via relatedNodes.')}
      ${listSection('Orphan nodes (parentId does not resolve)', health.orphanNodes, (x) => `<div class="reg-item">${idLink(x.nodeId)}<span class="reg-desc">missing parent ${R.esc(x.missingParent)}</span></div>`)}
      ${listSection('Broken citations (missing doc/ref)', health.brokenCitations, (x) => `<div class="reg-item"><span>${R.esc(x.owner)}</span><span class="reg-desc">${R.esc(x.issue)}</span></div>`)}
      ${listSection('Duplicate citations', health.duplicateCitations, (x) => `<div class="reg-item"><span>${R.esc(x.owner)}</span><span class="reg-desc">${R.esc(x.citation)} ×${x.count}</span></div>`)}
      ${listSection('Duplicate engineering objects', health.duplicateEngineeringObjects, (x) => `<div class="reg-item"><span>${R.esc(x.match)}</span><span class="reg-desc">${x.ids.map(idLink).join(', ')}${x.viaAlias ? ' (shared alias)' : ''}</span></div>`)}
      ${listSection('Duplicate definitions', health.duplicateDefinitions, (x) => `<div class="reg-item"><span>${R.esc(x.match)}</span><span class="reg-desc">${x.ids.map(idLink).join(', ')}${x.viaAlias ? ' (shared alias)' : ''}</span></div>`)}
      ${listSection('Unresolved TODO/FIXME markers', health.todoMarkers, (x) => `<div class="reg-item">${idLink(x.owner)}<span class="reg-desc">${R.esc(x.field)}: ${R.esc(x.match)}</span></div>`)}
    `;
    container.querySelectorAll('.ed-link').forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault(); window.RulesNav.showTab('search'); R.showDetail(a.dataset.id);
    }));
  }

  // ---------- QA Reports ----------
  function norm(s) { return String(s || '').trim().toLowerCase(); }

  function buildCitationReport() {
    const rows = [];
    let total = 0, withCitation = 0;
    DB.getAllStandards().forEach((s) => {
      total++; if ((s.meta.citations || []).length) withCitation++;
      s.nodes.forEach((n) => { total++; if ((n.citations || []).length) withCitation++; });
    });
    const health = DB.getHealthCheck();
    return { generatedAt: health.generatedAt, totalItems: total, itemsWithCitations: withCitation, coveragePct: Math.round((withCitation / total) * 1000) / 10, duplicateCitations: health.duplicateCitations, brokenCitations: health.brokenCitations };
  }
  function buildRelationshipReport() {
    const counts = {}; let total = 0;
    DB.getAllStandards().forEach((s) => {
      (s.meta.relationships || []).forEach((r) => { counts[r.type] = (counts[r.type] || 0) + 1; total++; });
      s.nodes.forEach((n) => (n.relationships || []).forEach((r) => { counts[r.type] = (counts[r.type] || 0) + 1; total++; }));
    });
    return { generatedAt: DB.getHealthCheck().generatedAt, totalRelationships: total, byType: counts, brokenRelationships: DB.getHealthCheck().brokenRelationships, disconnectedItems: DB.getHealthCheck().unconnectedItems.length };
  }
  function buildDefinitionReport() {
    const defs = DB.getDefinitions();
    return { generatedAt: DB.getHealthCheck().generatedAt, count: defs.length, terms: defs.map((d) => ({ id: d.id, term: d.term, instrumentCount: d.definitions.length, aliasCount: (d.aliases || []).length })), duplicates: DB.getHealthCheck().duplicateDefinitions };
  }
  function buildEngineeringObjectReport() {
    const eos = DB.getEngineeringObjects();
    return { generatedAt: DB.getHealthCheck().generatedAt, count: eos.length, objects: eos.map((k) => ({ id: k.id, title: k.title, kind: k.kind, relatedNodeCount: (k.relatedNodes || []).length, aliasCount: (k.aliases || []).length })), duplicates: DB.getHealthCheck().duplicateEngineeringObjects, unused: DB.getHealthCheck().unusedEngineeringObjects };
  }
  function buildPackageReport() {
    const cov = DB.getCoverage();
    const rows = Object.keys(cov.packages || {}).map((pkg) => {
      const list = cov.packages[pkg];
      return { package: pkg, standardCount: list.length, avgCoverage: Math.round(list.reduce((a, r) => a + r.coverage, 0) / list.length), statuses: list.reduce((acc, r) => { acc[r.status] = (acc[r.status] || 0) + 1; return acc; }, {}) };
    });
    return { generatedAt: cov.generatedAt, packages: rows };
  }

  const REPORTS = [
    { key: 'coverage', title: 'Coverage Report', build: () => DB.getCoverage() },
    { key: 'integrity', title: 'Integrity Report', build: () => DB.getIntegrityReport() },
    { key: 'citation', title: 'Citation Report', build: buildCitationReport },
    { key: 'relationship', title: 'Relationship Report', build: buildRelationshipReport },
    { key: 'definition', title: 'Definition Report', build: buildDefinitionReport },
    { key: 'engineering-object', title: 'Engineering Object Report', build: buildEngineeringObjectReport },
    { key: 'package', title: 'Package Report', build: buildPackageReport },
    { key: 'health', title: 'Repository Health Report', build: () => DB.getHealthCheck() },
  ];

  function download(filename, content, mime) {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
  }

  function reportToHtml(title, data) {
    return `<!doctype html><html><head><meta charset="utf-8"><title>${title} — RulesApp</title>
      <style>body{font-family:system-ui,sans-serif;max-width:900px;margin:32px auto;padding:0 16px;color:#0f172a;}
      h1{font-size:20px;border-bottom:2px solid #0d9488;padding-bottom:8px;} pre{background:#f1f5f9;padding:16px;border-radius:8px;overflow-x:auto;font-size:12px;white-space:pre-wrap;word-break:break-word;}
      .meta{color:#64748b;font-size:12px;margin-bottom:16px;}</style></head><body>
      <h1>${title}</h1><div class="meta">Generated by RulesApp from the current repository build. Exported ${new Date().toISOString().slice(0, 10)}.</div>
      <pre>${R.esc(JSON.stringify(data, null, 2))}</pre></body></html>`;
  }

  function renderReports() {
    const container = document.getElementById('qa-reports');
    if (!container) return;
    container.innerHTML = REPORTS.map((r) => `
      <div class="qa-card" data-key="${r.key}">
        <h4>${R.esc(r.title)}</h4>
        <div class="qa-summary" id="qa-summary-${r.key}"></div>
        <div class="qa-actions">
          <button type="button" class="chrome-btn qa-export-json" data-key="${r.key}">Export JSON</button>
          <button type="button" class="chrome-btn qa-export-html" data-key="${r.key}">Export HTML</button>
        </div>
      </div>`).join('');

    REPORTS.forEach((r) => {
      const data = r.build();
      const el = document.getElementById(`qa-summary-${r.key}`);
      if (!data) { el.innerHTML = '<p class="muted">Not available — run the corresponding build script.</p>'; return; }
      const keys = Object.keys(data).filter((k) => typeof data[k] !== 'object');
      el.innerHTML = `<div class="reg-box">${keys.map((k) => `<div class="reg-item"><span class="reg-code">${R.esc(k)}</span><span>${R.esc(String(data[k]))}</span></div>`).join('') || '<div class="reg-item muted">See exported JSON for full detail.</div>'}</div>`;
    });

    container.querySelectorAll('.qa-export-json').forEach((btn) => btn.addEventListener('click', () => {
      const r = REPORTS.find((x) => x.key === btn.dataset.key);
      download(`${r.key}-report.json`, JSON.stringify(r.build(), null, 2), 'application/json');
    }));
    container.querySelectorAll('.qa-export-html').forEach((btn) => btn.addEventListener('click', () => {
      const r = REPORTS.find((x) => x.key === btn.dataset.key);
      download(`${r.key}-report.html`, reportToHtml(r.title, r.build()), 'text/html');
    }));
  }

  function init() {
    renderDashboard();
    renderReports();
  }

  return { init };
})();
