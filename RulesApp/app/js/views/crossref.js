// Cross Reference Explorer: an interactive drill-down over the typed
// relationship graph (repository/index/crossref-graph.json), rooted at any
// standard, node, definition, or engineering object. Uses native <details>
// for expand/collapse so nesting stays cheap and accessible. A cycle guard
// (the `path` set) stops the graph from recursing into an ancestor already
// shown on the current branch.
window.RulesCrossref = (function () {
  const DB = window.RulesDB;
  const R = window.RulesRender;
  const MAX_DEPTH = 4;

  const INVERSE_LABEL = {
    amends: 'amended by', interprets: 'interpreted by', supersedes: 'superseded by',
    supersededBy: 'supersedes', implements: 'implemented by', cites: 'cited by',
    relatedTo: 'related to', depends_on: 'required by',
  };

  function edgeLabel(e) { return e.dir === 'out' ? e.type : (INVERSE_LABEL[e.type] || ('incoming ' + e.type)); }

  function buildEdgeList(id) {
    const edges = DB.getEdges(id);
    return (edges.outgoing || []).map((e) => ({ type: e.type, note: e.note, dir: 'out', otherId: e.targetId }))
      .concat((edges.incoming || []).map((e) => ({ type: e.type, note: e.note, dir: 'in', otherId: e.fromId })));
  }

  function renderBranch(id, depth, path) {
    const edges = buildEdgeList(id);
    const eoReverse = DB.getEngineeringObjectsFor(id);
    if (!edges.length && !eoReverse.length) return '<p class="muted">No outgoing or incoming relationships recorded for this item.</p>';

    const edgeItems = edges.map((e) => {
      if (path.has(e.otherId)) {
        return `<li class="xr-cycle"><span class="xr-edge-type">${R.esc(edgeLabel(e))}</span> <span class="xr-title">${R.esc(R.titleOf(e.otherId) || e.otherId)}</span> <span class="muted">(already shown higher up this branch)</span></li>`;
      }
      const canExpand = depth < MAX_DEPTH;
      const newPath = new Set(path); newPath.add(id);
      return `<li>
        <details${depth < 1 ? ' open' : ''}>
          <summary><span class="xr-edge-type">${R.esc(edgeLabel(e))}</span> <span class="xr-title">${R.esc(R.titleOf(e.otherId) || e.otherId)}</span> ${R.kindBadge(R.resolveKind(e.otherId))}${e.note ? ' <span class="xr-note">— ' + R.esc(e.note) + '</span>' : ''} <button type="button" class="xr-focus" data-id="${R.esc(e.otherId)}">Focus here</button></summary>
          ${canExpand ? renderBranch(e.otherId, depth + 1, newPath) : '<p class="muted">Maximum depth reached — click "Focus here" to re-root the explorer.</p>'}
        </details>
      </li>`;
    }).join('');

    const eoItems = eoReverse.map((r) => `
      <li><span class="xr-edge-type">engineering object</span> <a href="#" class="xref eo-focus" data-id="${R.esc(r.eo.id)}">${R.esc(r.eo.title)}</a> ${R.kindBadge('engineering-object')} <span class="xr-note">— ${R.esc(r.relationship)}</span></li>`).join('');

    return `<ul class="xr-list">${edgeItems}${eoItems}</ul>`;
  }

  function renderRoot(id) {
    const container = document.getElementById('crossref-graph');
    if (!container) return;
    const title = R.titleOf(id) || id;
    const kind = R.resolveKind(id);
    if (kind === 'unknown') {
      container.innerHTML = `<p class="muted">No item found for "${R.esc(id)}". Use the search box above to pick a regulation, code, circular, definition, or engineering object.</p>`;
      return;
    }
    container.innerHTML = `
      <div class="xr-root-card">
        <div class="xr-root-title">${R.kindBadge(kind)} <strong>${R.esc(title)}</strong></div>
        ${renderBranch(id, 0, new Set([id]))}
      </div>`;
    container.querySelectorAll('.xr-focus, .eo-focus').forEach((btn) => btn.addEventListener('click', (e) => {
      e.preventDefault();
      renderRoot(btn.dataset.id);
      container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }));
  }

  function renderSuggestions(query) {
    const box = document.getElementById('crossref-suggestions');
    if (!box) return;
    if (!query || !query.trim()) { box.innerHTML = ''; box.classList.remove('open'); return; }
    const results = window.RulesSearch.search(query).slice(0, 12);
    if (!results.length) { box.innerHTML = '<div class="suggest-empty">No matches</div>'; box.classList.add('open'); return; }
    box.innerHTML = results.map((r) => `<div class="suggest-row" data-id="${R.esc(r.id)}">${R.kindBadge(r.kind)} <span>${R.esc(r.title)}</span></div>`).join('');
    box.classList.add('open');
    box.querySelectorAll('.suggest-row').forEach((row) => row.addEventListener('click', () => {
      renderRoot(row.dataset.id);
      box.innerHTML = ''; box.classList.remove('open');
      document.getElementById('crossref-search').value = '';
    }));
  }

  function init() {
    const input = document.getElementById('crossref-search');
    if (!input || input._wired) return;
    input._wired = true;
    input.addEventListener('input', () => renderSuggestions(input.value));
    document.addEventListener('click', (e) => {
      if (!e.target.closest('#crossref-search') && !e.target.closest('#crossref-suggestions')) {
        const box = document.getElementById('crossref-suggestions');
        if (box) { box.innerHTML = ''; box.classList.remove('open'); }
      }
    });
    // Default root: SOLAS II-2/10 if present (fire fighting — heavily
    // cross-referenced across the FSS Code, MSC circulars and Engineering
    // Objects), else the first standard in the repository.
    const defaultId = DB.getNode('SOLAS-II2-10') ? 'SOLAS-II2-10' : (DB.getAllStandards()[0] && DB.getAllStandards()[0].meta.id);
    if (defaultId) renderRoot(defaultId);
  }

  return { init, renderRoot };
})();
