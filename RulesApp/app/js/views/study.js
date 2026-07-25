// Study Mode: an optional study interface layered entirely on existing
// repository data — no new content is authored to support this view.
// Per-document prerequisites/reading order come from the depends_on graph;
// "recently amended" and "most referenced" are repository-wide facts computed
// from status-timeline.json and crossref-graph.json respectively.
window.RulesStudy = (function () {
  const DB = window.RulesDB;
  const R = window.RulesRender;

  // Post-order DFS over depends_on edges: prerequisites get pushed before the
  // node that depends on them, so the resulting array reads prerequisite-
  // first, target-document-last — a usable "suggested reading order".
  function topoOrder(rootId) {
    const order = [];
    const visiting = new Set();
    (function visit(id) {
      if (visiting.has(id)) return;
      visiting.add(id);
      DB.getEdges(id).outgoing.filter((e) => e.type === 'depends_on').forEach((e) => visit(e.targetId));
      order.push(id);
    })(rootId);
    return order;
  }

  function relatedEngineeringObjects(standardId) {
    const std = DB.getStandard(standardId);
    if (!std) return [];
    const ids = [standardId, ...std.nodes.map((n) => n.id)];
    const seen = new Set();
    const out = [];
    ids.forEach((id) => DB.getEngineeringObjectsFor(id).forEach((r) => {
      if (!seen.has(r.eo.id)) { seen.add(r.eo.id); out.push(r.eo); }
    }));
    return out;
  }

  function renderGlobalPanels() {
    const recent = DB.getRecentAmendments(10);
    const freq = DB.getReferenceFrequency().slice(0, 12);
    const defs = DB.getDefinitions();

    document.getElementById('study-recent').innerHTML = recent.length ? recent.map((t) => {
      const std = DB.getStandard(t.standardId);
      return `<div class="reg-item"><span class="reg-code">${R.esc(t.date)}</span><a href="#" class="xref reg-desc" data-id="${R.esc(t.standardId)}">${R.esc(std ? (std.meta.abbreviation || std.meta.title) : t.standardId)}</a>${t.summary ? ' — ' + R.esc(t.summary) : ''}</div>`;
    }).join('') : '<p class="muted">No dated amendments recorded.</p>';

    document.getElementById('study-frequent').innerHTML = freq.length ? freq.map((f) => `
      <div class="reg-item"><span class="reg-code">${f.count} reference(s)</span><a href="#" class="xref reg-desc" data-id="${R.esc(f.id)}">${R.esc(R.titleOf(f.id) || f.id)}</a></div>`).join('') : '<p class="muted">No relationship data yet.</p>';

    document.getElementById('study-definitions').innerHTML = defs.length ? defs.map((d) => `
      <div class="reg-item"><a href="#" class="xref reg-code" data-id="${R.esc(d.id)}">${R.esc(d.term)}</a><span class="reg-desc">defined in ${d.definitions.length} instrument(s)</span></div>`).join('') : '<p class="muted">No definitions in the repository yet.</p>';

    document.querySelectorAll('#screen-study .xref[data-id]').forEach(wireXref);
  }

  function wireXref(a) {
    if (a._wired) return;
    a._wired = true;
    a.addEventListener('click', (e) => { e.preventDefault(); window.RulesNav.showTab('search'); R.showDetail(a.dataset.id); });
  }

  function renderPlan(standardId) {
    const std = DB.getStandard(standardId);
    const planBox = document.getElementById('study-plan');
    if (!planBox) return;
    if (!std) { planBox.innerHTML = '<p class="muted">Select a document above to generate a study plan.</p>'; return; }

    const order = topoOrder(standardId);
    const prereqs = order.filter((id) => id !== standardId);
    const eos = relatedEngineeringObjects(standardId);

    planBox.innerHTML = `
      <h4>Required prerequisite documents</h4>
      ${prereqs.length
        ? `<div class="reg-box">${prereqs.map((id) => `<div class="reg-item"><a href="#" class="xref reg-code" data-id="${R.esc(id)}">${R.esc(R.titleOf(id) || id)}</a></div>`).join('')}</div>`
        : '<p class="muted">No depends_on prerequisites recorded for this document.</p>'}

      <h4>Suggested reading order</h4>
      <div class="dep-chain">${order.map((id) => `<a href="#" class="xref dep-link" data-id="${R.esc(id)}">${R.esc(R.titleOf(id) || id)}</a>`).join(' <span class="dep-arrow">→</span> ')}</div>

      <h4>Related engineering objects</h4>
      ${eos.length
        ? `<div class="reg-box">${eos.map((eo) => `<div class="reg-item"><a href="#" class="xref reg-code" data-id="${R.esc(eo.id)}">${R.esc(eo.title)}</a></div>`).join('')}</div>`
        : '<p class="muted">No engineering objects reference this document\'s provisions yet.</p>'}
    `;
    planBox.querySelectorAll('.xref[data-id]').forEach(wireXref);
  }

  function populateSelect() {
    const sel = document.getElementById('study-standard-select');
    if (!sel || sel._populated) return;
    sel._populated = true;
    const standards = DB.getAllStandards().slice().sort((a, b) => (a.meta.abbreviation || a.meta.title).localeCompare(b.meta.abbreviation || b.meta.title));
    sel.innerHTML = '<option value="">— Select a document —</option>' + standards.map((s) =>
      `<option value="${R.esc(s.meta.id)}">${R.esc(s.meta.abbreviation || s.meta.title)}</option>`).join('');
    sel.addEventListener('change', () => renderPlan(sel.value));
  }

  function init() {
    populateSelect();
    renderGlobalPanels();
    const sel = document.getElementById('study-standard-select');
    const defaultId = DB.getStandard('igf-code') ? 'igf-code' : (DB.getAllStandards()[0] && DB.getAllStandards()[0].meta.id);
    if (defaultId && sel) { sel.value = defaultId; renderPlan(defaultId); }
  }

  return { init };
})();
