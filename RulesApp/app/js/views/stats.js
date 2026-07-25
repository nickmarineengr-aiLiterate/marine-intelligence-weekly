// Repository Statistics dashboard. Purely a read/aggregate view over
// manifest.json, coverage.json, health-check.json, search-index.json and the
// standards/nodes already loaded by db.js — computes nothing that isn't
// already true of the generated index, just presents it.
window.RulesStats = (function () {
  const DB = window.RulesDB;
  const R = window.RulesRender;

  function allCoverageRows() {
    const cov = DB.getCoverage();
    const rows = [];
    Object.keys(cov.packages || {}).forEach((pkg) => cov.packages[pkg].forEach((r) => rows.push(r)));
    return rows;
  }

  function coverageByOrg() {
    const byOrg = {};
    allCoverageRows().forEach((r) => {
      const std = DB.getStandard(r.id);
      const pub = std ? std.meta.publisher : 'unknown';
      (byOrg[pub] = byOrg[pub] || []).push(r.coverage);
    });
    return Object.keys(byOrg).map((pub) => {
      const org = DB.getOrganization(pub);
      const list = byOrg[pub];
      return { key: pub, name: org ? org.name : pub, count: list.length, avg: Math.round(list.reduce((a, b) => a + b, 0) / list.length) };
    }).sort((a, b) => b.avg - a.avg);
  }

  function coverageByPackage() {
    const cov = DB.getCoverage();
    return Object.keys(cov.packages || {}).map((pkg) => {
      const list = cov.packages[pkg];
      return { key: pkg, count: list.length, avg: Math.round(list.reduce((a, r) => a + r.coverage, 0) / list.length) };
    }).sort((a, b) => b.avg - a.avg);
  }

  function nodesByLevel() {
    const counts = {};
    DB.getAllStandards().forEach((s) => s.nodes.forEach((n) => { counts[n.level] = (counts[n.level] || 0) + 1; }));
    return counts;
  }

  function relationshipCounts() {
    const counts = {};
    let total = 0;
    DB.getAllStandards().forEach((s) => {
      (s.meta.relationships || []).forEach((r) => { counts[r.type] = (counts[r.type] || 0) + 1; total++; });
      s.nodes.forEach((n) => (n.relationships || []).forEach((r) => { counts[r.type] = (counts[r.type] || 0) + 1; total++; }));
    });
    return { counts, total };
  }

  function eoLinkCount() {
    return DB.getEngineeringObjects().reduce((n, k) => n + (k.relatedNodes || []).length, 0);
  }

  function statCard(value, label) {
    return `<div class="stat-card"><div class="stat-value">${R.esc(value)}</div><div class="stat-label">${R.esc(label)}</div></div>`;
  }

  function barRow(label, count, max) {
    const pct = max ? Math.round((count / max) * 100) : 0;
    return `<div class="bar-row"><div class="bar-label">${R.esc(label)}</div><div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div><div class="bar-count">${count}</div></div>`;
  }

  function render() {
    const container = document.getElementById('stats-content');
    if (!container) return;
    const manifest = DB.getManifest();
    const health = DB.getHealthCheck();
    const byLevel = nodesByLevel();
    const rel = relationshipCounts();
    const byOrg = coverageByOrg();
    const byPkg = coverageByPackage();
    const docs = allCoverageRows().sort((a, b) => b.coverage - a.coverage || a.title.localeCompare(b.title));
    const errorCount = (health.duplicateIds || []).length + (health.orphanNodes || []).length + (health.brokenRelationships || []).length
      + (health.duplicateCitations || []).length + (health.invalidProvenance || []).length;
    const maxLevel = Math.max(1, ...Object.values(byLevel));
    const maxRel = Math.max(1, ...Object.values(rel.counts));

    container.innerHTML = `
      <div class="stats-grid">
        ${statCard(manifest.counts.standards, 'Standards')}
        ${statCard(manifest.counts.nodes, 'Total decomposed nodes')}
        ${statCard(byLevel.regulation || 0, 'Regulations (level: regulation)')}
        ${statCard(manifest.counts.engineeringObjects, 'Engineering objects')}
        ${statCard(manifest.counts.definitions, 'Definitions')}
        ${statCard(manifest.counts.organizations, 'Organizations')}
        ${statCard(DB.getSearchIndex().length, 'Search index size')}
        ${statCard(rel.total, 'Authored relationships')}
      </div>

      <h4>Nodes by decomposition level</h4>
      <div class="bar-list">${Object.keys(byLevel).sort((a, b) => byLevel[b] - byLevel[a]).map((lvl) => barRow(lvl, byLevel[lvl], maxLevel)).join('')}</div>

      <h4>Relationship counts by type</h4>
      <div class="bar-list">${Object.keys(rel.counts).sort((a, b) => rel.counts[b] - rel.counts[a]).map((t) => barRow(t, rel.counts[t], maxRel)).join('')}
        ${barRow('engineering-object links (relatedNodes)', eoLinkCount(), maxRel)}</div>

      <h4>Coverage by organization</h4>
      <table class="stats-table"><thead><tr><th>Organization</th><th>Standards</th><th>Avg. coverage</th></tr></thead><tbody>
        ${byOrg.map((o) => `<tr><td>${R.esc(o.name)}</td><td>${o.count}</td><td>${o.avg}%</td></tr>`).join('')}
      </tbody></table>

      <h4>Coverage by package</h4>
      <table class="stats-table"><thead><tr><th>Package</th><th>Standards</th><th>Avg. coverage</th></tr></thead><tbody>
        ${byPkg.map((p) => `<tr><td>${R.esc(p.key)}</td><td>${p.count}</td><td>${p.avg}%</td></tr>`).join('')}
      </tbody></table>

      <h4>Coverage by document (${docs.length})</h4>
      <div class="stats-table-scroll"><table class="stats-table"><thead><tr><th>Document</th><th>Package</th><th>Status</th><th>Nodes</th><th>Coverage</th></tr></thead><tbody>
        ${docs.map((d) => `<tr><td><a href="#" class="xref" data-id="${R.esc(d.id)}">${R.esc(d.title)}</a></td><td>${R.esc(d.package)}</td><td>${R.esc(d.status)}</td><td>${d.nodes}</td><td>${d.coverage}%</td></tr>`).join('')}
      </tbody></table></div>

      <h4>Validation status</h4>
      <div class="prov-box ${errorCount === 0 ? 'validation-pass' : 'validation-fail'}">
        <div><strong>${errorCount === 0 ? 'PASS' : 'FAIL'}</strong> — ${errorCount} objective error(s) as of the last health check (${R.esc(health.generatedAt)})</div>
        <div>Duplicate IDs: ${health.duplicateIds.length} · Orphan nodes: ${health.orphanNodes.length} · Broken relationships: ${health.brokenRelationships.length} · Duplicate citations: ${health.duplicateCitations.length} · Invalid provenance: ${health.invalidProvenance.length}</div>
        <div class="muted">Coverage notes (not errors): ${health.missingValidity.standards}/${health.missingValidity.standardsTotal} standards and ${health.missingValidity.nodes}/${health.missingValidity.nodesTotal} nodes have no structured validity metadata yet; ${health.missingSearchAliases.length} definitions/engineering-objects missing search aliases.</div>
      </div>

      <h4>Repository version</h4>
      <div class="prov-box"><div><strong>Schema version:</strong> ${R.esc(manifest.schemaVersion)}</div><div><strong>Last build:</strong> ${R.esc(manifest.generatedAt)}</div></div>
    `;
    container.querySelectorAll('.xref[data-id]').forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault(); window.RulesNav.showTab('search'); R.showDetail(a.dataset.id);
    }));
  }

  return { render };
})();
