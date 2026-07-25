// View rendering: search-result list, and a detail panel that adapts to
// whichever kind of thing was clicked (standard, node, definition,
// engineering object). This is the Citation Viewer: every regulation/standard
// page shows citation, source document, edition, version, status, validity,
// provenance, and relationships categorized into regulations/codes/circulars/
// engineering objects, plus a breadcrumb trail and a collapsible hierarchy.
window.RulesRender = (function () {
  const DB = window.RulesDB;
  const listEl = () => document.getElementById('result-list');
  const detailEl = () => document.getElementById('detail-panel');
  const countEl = () => document.getElementById('result-count');

  function esc(s) { return (s == null ? '' : String(s)).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])); }

  function kindBadge(kind) {
    const map = { standard: 'bd-standard', node: 'bd-node', definition: 'bd-definition', 'engineering-object': 'bd-eo' };
    return `<span class="kind-badge ${map[kind] || ''}">${esc(kind)}</span>`;
  }

  function statusBadge(status) {
    if (!status) return '';
    const cls = status === 'current' ? 'st-current' : status === 'superseded' ? 'st-superseded' : status === 'future-effective' ? 'st-future' : 'st-other';
    return `<span class="status-badge ${cls}">${esc(status)}</span>`;
  }

  // Stage 2B: editorial workflow state — a dimension distinct from the
  // regulatory `status` badge above (see repository/build/workflow-state.js
  // and EDITORIAL_GUIDE.md for the full derivation). Shown on every standard/
  // node detail page per the Stage 2B spec ("repository pages shall clearly
  // display their workflow state").
  const WORKFLOW_CLASS = {
    Draft: 'wf-draft', 'AI Draft': 'wf-ai-draft', 'Pending Human Review': 'wf-pending',
    Verified: 'wf-verified', Published: 'wf-published', Deprecated: 'wf-deprecated', Archive: 'wf-archive',
  };
  function workflowBadge(id) {
    const state = DB.getWorkflowStatus && DB.getWorkflowStatus(id);
    if (!state) return '';
    return `<span class="workflow-badge ${WORKFLOW_CLASS[state] || ''}" title="Editorial workflow state — see Editorial Dashboard">${esc(state)}</span>`;
  }

  // Rich result card for an Engineering Object hit, per
  // MIW_INTELLIGENCE_PRODUCT_SPECIFICATION.md §6: title, Official Context
  // citation, a short Engineering Intelligence snippet, and cluster counts
  // (with short labels) for guidance notes, exam-prep (MIW) references,
  // related objects, and definitions -- "understand the result" before
  // clicking in, not just a title. Every field reused from data the
  // Workspace itself already renders; clusterCounts() is the exact same
  // computation the Workspace's own quick-jump nav uses, via
  // views/engineering.js, so the two can never drift apart. Returns null
  // if the object can't be resolved (falls back to the flat row).
  function renderEOCard(item) {
    const eo = DB.getEngineeringObject(item.id);
    if (!eo || !window.RulesEngineering) return null;
    const counts = window.RulesEngineering.clusterCounts(eo);
    const nodes = eo.relatedNodes || [];
    const context = nodes.length ? titleOf(nodes[0].targetId) || nodes[0].targetId : null;
    const moreContext = nodes.length - 1;
    const desc = eo.description || '';
    const snippet = desc.length > 160 ? desc.slice(0, 160) + '…' : desc;
    const stats = [];
    if (counts.understanding) stats.push(`<span class="eo-card-stat">${counts.understanding} guidance note${counts.understanding === 1 ? '' : 's'}</span>`);
    if (counts.study) stats.push(`<span class="eo-card-stat eo-card-stat-miw">${counts.study} exam reference${counts.study === 1 ? '' : 's'} (MIW)</span>`);
    if (counts.relatedObjects) stats.push(`<span class="eo-card-stat">${counts.relatedObjects} related object${counts.relatedObjects === 1 ? '' : 's'}</span>`);
    if (counts.definitions) stats.push(`<span class="eo-card-stat">${counts.definitions} definition${counts.definitions === 1 ? '' : 's'}</span>`);
    return `
      <div class="result-eo-head">
        <span class="result-title">${esc(eo.title)}</span>
        <span class="kind-badge bd-eo">${esc(eo.kind)}</span>
      </div>
      ${context ? `<div class="result-eo-context">${esc(context)}${moreContext > 0 ? ` <span class="muted">+${moreContext} more</span>` : ''}</div>` : ''}
      ${snippet ? `<div class="result-eo-snippet">${esc(snippet)}</div>` : ''}
      ${stats.length ? `<div class="result-eo-stats">${stats.join('')}</div>` : '<div class="result-eo-stats muted">Engineering Intelligence for this system is still being developed.</div>'}`;
  }

  // ---------- LIST ----------
  function renderList(items) {
    const el = listEl();
    el.innerHTML = '';
    countEl().textContent = items.length + (items.length === 1 ? ' result' : ' results');
    if (!items.length) {
      el.innerHTML = '<div class="empty-state">No matches. Try a different term, or clear the filter.</div>';
      return;
    }
    items.slice(0, 200).forEach((item) => {
      const row = document.createElement('div');
      const eoCardHtml = item.kind === 'engineering-object' ? renderEOCard(item) : null;
      if (eoCardHtml) {
        row.className = 'result-row result-row-eo';
        row.innerHTML = eoCardHtml;
      } else {
        row.className = 'result-row';
        row.innerHTML = `
          <div class="result-main">
            <div class="result-title">${esc(item.title)}</div>
            <div class="result-sub">${kindBadge(item.kind)} ${item.abbreviation ? esc(item.abbreviation) : ''} ${item.label ? '· ' + esc(item.label) : ''}</div>
          </div>
          <div class="result-status">${statusBadge(item.status)}</div>`;
      }
      row.addEventListener('click', () => showDetail(item.id, item.kind));
      el.appendChild(row);
    });
  }

  // ---------- shared: identify + describe any id in the repository ----------
  function resolveKind(id) {
    if (DB.getEngineeringObject(id)) return 'engineering-object';
    if (DB.getDefinition(id)) return 'definition';
    if (DB.getNode(id) && !DB.getStandard(id)) return 'node';
    if (DB.getStandard(id)) return 'standard';
    return 'unknown';
  }

  function titleOf(id) {
    const n = DB.getNode(id); if (n) return `${n.level} ${n.label} — ${n.title}`;
    const s = DB.getStandard(id); if (s) return s.meta.abbreviation ? `${s.meta.abbreviation} — ${s.meta.title}` : s.meta.title;
    const d = DB.getDefinition(id); if (d) return d.term;
    const k = DB.getEngineeringObject(id); if (k) return k.title;
    return null;
  }

  function bucketFor(id) {
    const kind = resolveKind(id);
    if (kind === 'engineering-object') return 'eo';
    if (kind === 'definition') return 'definition';
    if (kind === 'node') return 'regulation';
    if (kind === 'standard') {
      const t = DB.getStandard(id).meta.standardType;
      if (t === 'code') return 'code';
      if (t === 'circular') return 'circular';
      return 'other-standard';
    }
    return 'unknown';
  }

  const BUCKET_LABELS = {
    regulation: 'Related regulations', code: 'Related codes', circular: 'Related circulars',
    eo: 'Related engineering objects', 'other-standard': 'Related standards',
    definition: 'Related definitions', unknown: 'Other references',
  };
  const BUCKET_ORDER = ['regulation', 'code', 'circular', 'eo', 'other-standard', 'definition', 'unknown'];

  // The Citation Viewer's categorized relationship sections. Combines
  // authored relationships[] (both directions, via crossref-graph.json) with
  // the reverse Engineering Object index (EO links are authored on the EO
  // side as relatedNodes[], not as a formal relationship — see db.js).
  function renderCategorizedRelationships(id) {
    const edges = DB.getEdges(id);
    const combined = []
      .concat((edges.outgoing || []).map((e) => ({ type: e.type, note: e.note, dir: 'out', otherId: e.targetId })))
      .concat((edges.incoming || []).map((e) => ({ type: e.type, note: e.note, dir: 'in', otherId: e.fromId })));

    const buckets = {};
    combined.forEach((e) => { (buckets[bucketFor(e.otherId)] = buckets[bucketFor(e.otherId)] || []).push(e); });

    const eoReverse = DB.getEngineeringObjectsFor(id);
    if (eoReverse.length) {
      buckets.eo = (buckets.eo || []).concat(eoReverse.map((r) => ({ type: 'relatedTo', note: r.relationship, dir: 'in', otherId: r.eo.id })));
    }

    return BUCKET_ORDER.filter((b) => buckets[b] && buckets[b].length).map((b) => `
      <h4>${esc(BUCKET_LABELS[b])}</h4>
      <div class="reg-box">${buckets[b].map((e) => {
        const dirLabel = e.dir === 'out' ? esc(e.type) : `← ${esc(e.type)}`;
        return `<div class="reg-item"><span class="reg-code">${dirLabel}</span><a href="#" class="xref reg-desc" data-id="${esc(e.otherId)}">${esc(titleOf(e.otherId) || e.otherId)}</a>${e.note ? ' — ' + esc(e.note) : ''}</div>`;
      }).join('')}</div>`).join('');
  }

  // ---------- shared: breadcrumb trail ----------
  function renderBreadcrumb(id) {
    const parts = [];
    const n = DB.getNode(id) && !DB.getStandard(id) ? DB.getNode(id) : null;
    const standardId = n ? DB.getOwningStandardId(id) : (DB.getStandard(id) ? id : null);
    const std = standardId ? DB.getStandard(standardId) : null;
    const org = std && std.meta ? DB.getOrganization(std.meta.publisher) : null;

    if (org) parts.push({ id: std.meta.id, label: org.abbreviation || org.name, current: true });
    if (std) parts.push({ id: std.meta.id, label: std.meta.abbreviation || std.meta.title, current: !n });

    const chain = [];
    let cur = n;
    while (cur && cur.parentId) {
      cur = DB.getNode(cur.parentId);
      if (cur) chain.unshift({ id: cur.id, label: `${cur.level} ${cur.label}` });
    }
    parts.push(...chain);
    if (n) parts.push({ id: n.id, label: `${n.level} ${n.label}`, current: true });

    if (!parts.length) return '';
    return `<nav class="breadcrumb" style="margin-bottom:12px;font-size:13px;color:#64748b;">${parts.map((p, i) => (i > 0 ? '<span class="crumb-sep" style="margin:0 6px;color:#94a3b8;">›</span>' : '') +
      (p.current ? `<span class="crumb-current" style="font-weight:600;color:#0f172a;">${esc(p.label)}</span>` : `<a href="#" class="xref crumb-link" data-id="${esc(p.id)}" style="color:#0284c7;text-decoration:none;">${esc(p.label)}</a>`)).join('')}</nav>`;
  }

  // ---------- shared: validity ----------
  function renderValidity(validity) {
    if (!validity) {
      return `<h4>Validity</h4><p class="muted">Not yet recorded — structured applicability metadata (ship types, tonnage, build date, voyage type) is a known repository coverage gap; see the Statistics dashboard. This is not a claim that the provision has no applicability limits, only that they have not yet been captured here.</p>`;
    }
    const rows = [];
    if (validity.shipTypes && validity.shipTypes.length) rows.push(`<div><strong>Ship types:</strong> ${validity.shipTypes.map(esc).join(', ')}</div>`);
    if (validity.tonnageThreshold) rows.push(`<div><strong>Tonnage threshold:</strong> ${esc(validity.tonnageThreshold)}</div>`);
    if (validity.buildDateFrom || validity.buildDateTo) rows.push(`<div><strong>Build date:</strong> ${esc(validity.buildDateFrom || '?')} – ${esc(validity.buildDateTo || 'present')}</div>`);
    if (validity.voyageType) rows.push(`<div><strong>Voyage type:</strong> ${esc(validity.voyageType)}</div>`);
    if (validity.note) rows.push(`<div>${esc(validity.note)}</div>`);
    return `<h4>Validity</h4><div class="prov-box">${rows.join('') || '<span class="muted">No structured applicability fields set.</span>'}</div>`;
  }

  // ---------- DETAIL: STANDARD ----------
  function renderStandardDetail(id) {
    const s = DB.getStandard(id);
    if (!s) return `<p>Not found: ${esc(id)}</p>`;
    const m = s.meta;
    const org = DB.getOrganization(m.publisher);
    const cur = DB.getCurrentEdition(m);
    const pkg = DB.getPackageOf(id);

    const editionsHtml = (m.editions || []).map((ed) => `
      <div class="edition-block ${ed.editionId === (cur && cur.editionId) ? 'current-edition' : ''}">
        <div class="edition-head">${esc(ed.label || ed.editionId)} ${statusBadge(ed.status)} ${ed.editionId === (cur && cur.editionId) ? '<span class="current-tag">CURRENT CONSOLIDATED VERSION</span>' : ''}</div>
        <div class="edition-range">${esc(ed.effectiveFrom || '?')} → ${ed.effectiveTo ? esc(ed.effectiveTo) : 'present'}</div>
        ${(ed.versions || []).map((v) => `
          <div class="version-row">
            <div class="version-label">v${esc(v.version)} · ${esc(v.effectiveFrom || '?')}${v.changeRef ? ' · via <a href="#" class="xref" data-id="' + esc(v.changeRef) + '">' + esc(v.changeRef) + '</a>' : ''}</div>
            <div class="version-summary">${esc(v.summary || '')}</div>
          </div>`).join('')}
      </div>`).join('');

    const hierarchyHtml = s.nodes && s.nodes.length
      ? `<div class="tree-header"><h4>Hierarchy (${s.nodes.length} nodes)</h4><div class="tree-controls"><button type="button" class="tree-expand-all">Expand all</button><button type="button" class="tree-collapse-all">Collapse all</button></div></div><div class="tree">${renderTreeLevel(DB.getTopLevelNodes(id), id)}</div>`
      : '<p class="muted">Not yet decomposed below document level.</p>';

    const depChain = DB.getDependencyChain(id);
    const depHtml = depChain.length
      ? `<h4>Study path (depends_on)</h4><div class="dep-chain">${depChain.map((e) => `<a href="#" class="xref dep-link" data-id="${esc(e.to)}">${esc(e.to)}</a>`).join(' <span class="dep-arrow">→</span> ')}</div>`
      : '';

    return `
      ${renderBreadcrumb(id)}
      <div class="detail-head">
        <h2>${esc(m.title)} ${statusBadge(m.status)} ${workflowBadge(id)}</h2>
        <div class="detail-meta">
          <span>${esc(m.standardType)}</span>
          <span>Package: ${esc(pkg)}</span>
          <span>Publisher: <a href="#" class="xref" data-id="${esc(m.publisher)}">${esc(org ? org.name : m.publisher)}</a> (${esc(org && org.orgType)}, ${esc(org && org.jurisdiction && org.jurisdiction.scope)}${org && org.jurisdiction && org.jurisdiction.region ? ' · ' + esc(org.jurisdiction.region) : ''})</span>
          ${m.adoptionDate ? '<span>Adopted: ' + esc(m.adoptionDate) + '</span>' : ''}
          ${m.entryIntoForce ? '<span>In force: ' + esc(m.entryIntoForce) + '</span>' : ''}
        </div>
      </div>
      ${renderViewModeTabs(id, 'node')}
      ${m.summary ? `<p class="summary-text">${esc(m.summary)}</p>` : ''}
      <h4>Editions &amp; Amendment History</h4>
      ${editionsHtml}
      ${depHtml}
      ${renderValidity(m.validity)}
      ${renderCitations(m.citations)}
      ${renderProvenance(m.provenance)}
      ${renderCategorizedRelationships(id)}
      ${hierarchyHtml}
      ${m.sourceUrl ? `<a class="source-link" href="${esc(m.sourceUrl)}" target="_blank" rel="noopener">Official source ↗</a>` : ''}
    `;
  }

  function renderTreeLevel(nodes, standardId, depth) {
    depth = depth || 0;
    if (!nodes.length) return '';
    return '<ul class="tree-level" style="--depth:' + depth + '">' + nodes.map((n) => {
      const children = DB.getChildren(n.id, standardId);
      const hasChildren = children.length > 0;
      return `<li>
        ${hasChildren ? '<button type="button" class="tree-toggle" aria-expanded="true">▾</button>' : '<span class="tree-toggle-spacer"></span>'}
        <a href="#" class="xref tree-node-link" data-id="${esc(n.id)}"><span class="tree-label">${esc(n.level)} ${esc(n.label)}</span> — ${esc(n.title)}</a>
        ${hasChildren ? renderTreeLevel(children, standardId, depth + 1) : ''}
      </li>`;
    }).join('') + '</ul>';
  }

  function renderViewModeTabs(id, activeMode) {
    activeMode = activeMode || 'node';
    return `
      <div class="view-mode-tabs" style="display:flex;gap:6px;margin:12px 0 16px 0;padding:4px;background:#f1f5f9;border-radius:8px;border:1px solid #cbd5e1;">
        <button type="button" class="view-tab ${activeMode==='node'?'active':''}" data-mode="node" data-id="${esc(id)}" style="flex:1;padding:8px 6px;font-size:11px;font-weight:700;border:none;border-radius:6px;cursor:pointer;background:${activeMode==='node'?'#0f172a':'transparent'};color:${activeMode==='node'?'#fff':'#475569'};">🛠 Engineering View</button>
        <button type="button" class="view-tab ${activeMode==='regulation'?'active':''}" data-mode="regulation" data-id="${esc(id)}" style="flex:1;padding:8px 6px;font-size:11px;font-weight:700;border:none;border-radius:6px;cursor:pointer;background:${activeMode==='regulation'?'#0d9488':'transparent'};color:${activeMode==='regulation'?'#fff':'#475569'};">📖 Regulation Reading</button>
        <button type="button" class="view-tab ${activeMode==='chapter'?'active':''}" data-mode="chapter" data-id="${esc(id)}" style="flex:1;padding:8px 6px;font-size:11px;font-weight:700;border:none;border-radius:6px;cursor:pointer;background:${activeMode==='chapter'?'#2563eb':'transparent'};color:${activeMode==='chapter'?'#fff':'#475569'};">📚 Chapter Reading</button>
        <button type="button" class="view-tab ${activeMode==='docinfo'?'active':''}" data-mode="docinfo" data-id="${esc(id)}" style="flex:1;padding:8px 6px;font-size:11px;font-weight:700;border:none;border-radius:6px;cursor:pointer;background:${activeMode==='docinfo'?'#475569':'transparent'};color:${activeMode==='docinfo'?'#fff':'#475569'};">ℹ️ Document Info</button>
      </div>
    `;
  }

  function renderDocumentInfoHTML(id) {
    const n = DB.getNode(id);
    const standardId = n ? DB.getOwningStandardId(id) : id;
    const std = DB.getStandard(standardId);
    if (!std) return `<p style="padding:16px;">No document info available for ${esc(id)}.</p>`;

    const m = std.meta;
    const org = DB.getOrganization(m.publisher);
    const editions = m.editions || [];
    const currentEd = DB.getCurrentEdition(m);

    return `
      ${renderBreadcrumb(id)}
      <div class="detail-head">
        <h2>${esc(m.abbreviation || m.title)} ${statusBadge(m.status)}</h2>
        <div class="detail-meta"><span>${esc(m.title)}</span></div>
      </div>
      ${renderViewModeTabs(id, 'docinfo')}
      <div class="docinfo-container" style="background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;padding:24px;margin-top:16px;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <h3 style="font-size:16px;font-weight:700;color:#0f172a;margin-top:0;margin-bottom:16px;border-bottom:2px solid #475569;padding-bottom:8px;">ℹ️ Document Information &amp; Metadata</h3>
        
        <div class="info-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px;">
          <div style="background:#f8fafc;padding:12px;border-radius:6px;border:1px solid #e2e8f0;">
            <div style="font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;">Convention / Instrument</div>
            <div style="font-size:14px;font-weight:700;color:#0f172a;">${esc(m.title)}</div>
            <div style="font-size:12px;color:#475569;">Publisher: ${esc(org ? org.name : m.publisher)}</div>
          </div>
          <div style="background:#f8fafc;padding:12px;border-radius:6px;border:1px solid #e2e8f0;">
            <div style="font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;">Edition &amp; Status</div>
            <div style="font-size:14px;font-weight:700;color:#0f172a;">${esc(currentEd ? currentEd.label || currentEd.editionId : 'Active')} ${statusBadge(m.status)}</div>
            <div style="font-size:12px;color:#475569;">Adoption: ${esc(m.adoptionDate || 'N/A')} · EIF: ${esc(m.entryIntoForce || 'N/A')}</div>
          </div>
        </div>

        <h4>Repository Coverage &amp; Decomposition</h4>
        <div class="prov-box" style="margin-bottom:20px;">
          <div><strong>Decomposed Nodes:</strong> ${(std.nodes || []).length} nodes in repository</div>
        </div>
        <p class="muted">Requirement-coverage and citation-grounding percentages are not yet computed for this standard — this is a known repository gap, not a claim that decomposition or citation work is incomplete. See the Coverage Matrix tab for the repository's actual computed metrics.</p>

        ${renderCitations(m.citations)}
        ${renderProvenance(m.provenance)}

        <div class="applicability-placeholder" style="background:#f1f5f9;border:1px dashed #94a3b8;border-radius:8px;padding:14px;margin-top:20px;">
          <div style="font-size:11px;font-weight:700;letter-spacing:1px;color:#475569;text-transform:uppercase;margin-bottom:4px;">⚙️ Applicability Engine (Version 2.0 Placeholder)</div>
          <div style="font-size:12px;color:#64748b;">Target keel-laying date, ship type (tanker/bulk/container/passenger), and GT applicability parameters will be evaluated dynamically by the Version 2.0 Statutory Applicability Engine.</div>
        </div>
      </div>
    `;
  }

  function renderContextViewHTML(id, mode) {
    if (mode === 'docinfo') return renderDocumentInfoHTML(id);

    const ctx = DB.getContextView(id, mode);
    if (!ctx || !ctx.nodes || !ctx.nodes.length) {
      return `<p style="padding:16px;">No continuous context view available for ${esc(id)}.</p>`;
    }

    const modeTitle = mode === 'regulation' ? '📖 Regulation Reading View' : (mode === 'chapter' ? '📚 Chapter Reading View' : '📜 Document Reading View');

    // Conservative sibling-gap check: only flags a gap between two entries at
    // the same level, under the same parent, with plain integer labels (e.g.
    // "29" -> "31"). Roman numerals, decimals ("2.2.4"), and alpha-suffixed
    // labels ("42-1") are deliberately left unchecked rather than guessed at -
    // a missed gap is preferable to a wrong one (see repository/governance's
    // Engineering Humility principle).
    function siblingGapNote(prev, next) {
      if (!prev || !next || prev.level !== next.level || prev.parentId !== next.parentId) return '';
      const a = Number(prev.label), b = Number(next.label);
      if (!Number.isInteger(a) || !Number.isInteger(b) || b - a <= 1) return '';
      const missing = b - a === 2 ? String(a + 1) : `${a + 1}–${b - 1}`;
      return `<div class="muted" style="margin:16px 0;padding:10px 14px;border-left:3px solid #cbd5e1;font-size:13px;">
        — a numbering gap follows: this repository does not currently include ${esc(next.level)} ${esc(missing)} between ${esc(prev.label)} and ${esc(next.label)}. This may reflect content not yet decomposed here, or numbers not used in this edition — consult the official source to confirm. —
      </div>`;
    }

    return `
      ${renderBreadcrumb(id)}
      <div class="detail-head">
        <h2>${esc(ctx.title)}</h2>
        <div class="detail-meta">
          <span style="font-weight:700;color:#0d9488;">${esc(modeTitle)}</span>
          <span>Standard: <a href="#" class="xref" data-id="${esc(ctx.standard ? ctx.standard.meta.id : '')}">${esc(ctx.standard ? ctx.standard.meta.title : '')}</a></span>
        </div>
      </div>
      ${renderViewModeTabs(id, mode)}
      <div class="context-view-container" style="background:#ffffff;border:1px solid #cbd5e1;border-radius:10px;padding:24px;margin-top:16px;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:11px;font-weight:700;letter-spacing:1px;color:#0d9488;text-transform:uppercase;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #0d9488;">
          Continuous Reading Mode (${ctx.nodes.length} Decomposed Sub-Provisions) — Engineering Account, No Interpretive Commentary
        </div>
        ${(() => {
          // ctx.nodes is a flattened pre-order walk (a regulation immediately
          // followed by its own children before the next regulation), so the
          // literal previous array entry is often a child, not a sibling.
          // Track the last node actually seen at each level+parent instead.
          const lastAtLevel = {};
          return ctx.nodes.map((n, idx) => {
            const key = n.level + '|' + n.parentId;
            const gapHtml = siblingGapNote(lastAtLevel[key], n);
            lastAtLevel[key] = n;
            return `
          ${gapHtml}
          <div class="context-node-block" id="ctx-node-${esc(n.id)}" style="margin-bottom:24px;padding-bottom:16px;border-bottom:${idx < ctx.nodes.length - 1 ? '1px solid #e2e8f0' : 'none'};">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
              <h3 style="font-size:15px;font-weight:700;color:#0f172a;margin:0;">${esc(n.level)} ${esc(n.label)} — ${esc(n.title)}</h3>
              <a href="#" class="xref" data-id="${esc(n.id)}" style="font-size:11px;color:#0284c7;text-decoration:none;font-weight:600;">Node Card ↗</a>
            </div>
            <div style="font-size:14px;line-height:1.75;color:#1e293b;white-space:pre-wrap;font-family:Inter, system-ui, sans-serif;margin-bottom:12px;">${esc(n.officialRequirement || n.summary)}</div>
            ${renderCitations(n.citations)}
          </div>
        `;
          }).join('');
        })()}
      </div>
    `;
  }

  // ---------- DETAIL: NODE (a decomposed regulation/provision) ----------
  function renderNodeDetail(id, mode) {
    if (mode && mode !== 'node') return renderContextViewHTML(id, mode);

    const n = DB.getNode(id);
    if (!n) return `<p>Not found: ${esc(id)}</p>`;
    const standardId = DB.getOwningStandardId(id);
    const standard = DB.getStandard(standardId);
    const children = DB.getChildren(id, standardId);

    const editions = (standard && standard.meta.editions) || [];
    const edition = editions.find((e) => e.editionId === n.editionId) || DB.getCurrentEdition(standard ? standard.meta : {});
    const latestVersion = edition && edition.versions && edition.versions.length ? edition.versions[edition.versions.length - 1] : null;
    const docContext = standard ? `
      <h4>Document context</h4>
      <div class="prov-box">
        <div><strong>Source document:</strong> <a href="#" class="xref" data-id="${esc(standardId)}">${esc(standard.meta.abbreviation || standard.meta.title)}</a> ${statusBadge(standard.meta.status)}</div>
        ${edition ? '<div><strong>Edition:</strong> ' + esc(edition.label || edition.editionId) + ' ' + statusBadge(edition.status) + '</div>' : ''}
        ${latestVersion ? '<div><strong>Version:</strong> v' + esc(latestVersion.version) + ' · effective ' + esc(latestVersion.effectiveFrom || '?') + (latestVersion.changeRef ? ' · via <a href="#" class="xref" data-id="' + esc(latestVersion.changeRef) + '">' + esc(latestVersion.changeRef) + '</a>' : '') + '</div>' : ''}
      </div>` : '';

    return `
      ${renderBreadcrumb(id)}
      <div class="detail-head">
        <h2>${esc(n.title)} ${workflowBadge(id)}</h2>
        <div class="detail-meta">
          <span>${esc(n.level)} ${esc(n.label)}</span>
          <span>Part of: <a href="#" class="xref" data-id="${esc(standardId)}">${esc(standard ? standard.meta.title : standardId)}</a></span>
        </div>
      </div>
      ${renderViewModeTabs(id, 'node')}
      ${n.officialRequirement ? `
        <div class="official-req-card" style="background:#f8fafc;border:2px solid #0d9488;border-radius:10px;padding:16px;margin:16px 0;">
          <div style="font-size:11px;font-weight:700;letter-spacing:1px;color:#0d9488;text-transform:uppercase;margin-bottom:8px;">🔧 Engineering Summary</div>
          <div class="official-req-body" style="font-size:14px;line-height:1.7;color:#0f172a;white-space:pre-wrap;">${esc(n.officialRequirement)}</div>
        </div>
      ` : `<p class="summary-text">${esc(n.summary)}</p>`}
      ${n.interpretation ? `
        <div class="interp-card" style="background:#fff7ed;border:1px solid #f97316;border-radius:10px;padding:16px;margin:16px 0;">
          <div style="font-size:11px;font-weight:700;letter-spacing:1px;color:#c2410c;text-transform:uppercase;margin-bottom:8px;">🎓 MIW Engineering Interpretation</div>
          <div class="interp-body" style="font-size:13px;line-height:1.6;color:#1e293b;">${esc(n.interpretation.explanation || n.interpretation.oralExamGuidance || 'Reserved for future MIW engineering guidance.')}</div>
        </div>
      ` : ''}
      ${renderValidity(n.validity)}
      ${renderCitations(n.citations)}
      ${renderProvenance(n.provenance)}
      ${renderCategorizedRelationships(id)}
      ${docContext}
      ${children.length ? `<div class="tree-header"><h4>Sub-provisions</h4><div class="tree-controls"><button type="button" class="tree-expand-all">Expand all</button><button type="button" class="tree-collapse-all">Collapse all</button></div></div><div class="tree">${renderTreeLevel(children, standardId)}</div>` : ''}
    `;
  }

  // ---------- DETAIL: DEFINITION ----------
  function renderDefinitionDetail(id) {
    const d = DB.getDefinition(id);
    if (!d) return `<p>Not found: ${esc(id)}</p>`;
    return `
      <div class="detail-head"><h2>${esc(d.term)}</h2>
        ${d.aliases && d.aliases.length ? '<div class="detail-meta"><span>Also known as: ' + d.aliases.map(esc).join(', ') + '</span></div>' : ''}
      </div>
      <h4>Defined across ${d.definitions.length} instrument(s)</h4>
      ${d.definitions.map((x) => `
        <div class="def-instrument-block">
          <div class="def-instrument-name"><a href="#" class="xref" data-id="${esc(x.sourceNodeId)}">${esc(x.instrument)}</a></div>
          <div class="def-text">${esc(x.text)}</div>
        </div>`).join('')}
    `;
  }

  // ---------- shared partials ----------
  function renderCitations(citations) {
    if (!citations || !citations.length) return '';
    return `<h4>Official Citation</h4><div class="citation-box">${citations.map((c) => {
      const parts = [
        c.doc && `<span class="citation-doc">${esc(c.doc)}</span>`,
        c.ref && `<span class="citation-ref">${esc(c.ref)}</span>`,
        c.resolution && `<span class="citation-res">Res. ${esc(c.resolution)}</span>`,
        c.amendment && `<span class="citation-amend">Amend: ${esc(c.amendment)}</span>`,
        c.entryIntoForce && `<span class="citation-eif">EIF: ${esc(c.entryIntoForce)}</span>`,
        c.page && `<span class="citation-page">p.${esc(c.page)}</span>`
      ].filter(Boolean).join(' · ');
      return c.url ? `<div class="citation-item"><a href="${esc(c.url)}" target="_blank" rel="noopener">${parts}</a></div>` : `<div class="citation-item">${parts}</div>`;
    }).join('')}</div>`;
  }

  function renderProvenance(prov) {
    if (!prov) return '';
    return `<h4>Provenance</h4><div class="prov-box">
      <div><strong>Source type:</strong> ${esc(prov.sourceType)}</div>
      ${prov.sourceFile ? '<div><strong>Source file:</strong> ' + esc(prov.sourceFile) + (prov.sourcePages ? ' (p. ' + esc(prov.sourcePages) + ')' : '') + '</div>' : ''}
      ${prov.sourceUrl ? '<div><strong>Source URL:</strong> <a href="' + esc(prov.sourceUrl) + '" target="_blank" rel="noopener">' + esc(prov.sourceUrl) + '</a></div>' : ''}
      ${prov.verifiedBy ? '<div><strong>Verified by:</strong> ' + esc(prov.verifiedBy) + '</div>' : ''}
      ${prov.verifiedMethod ? '<div><strong>Method:</strong> ' + esc(prov.verifiedMethod) + '</div>' : ''}
    </div>`;
  }

  // ---------- tree collapse/expand wiring ----------
  function wireTreeControls(root) {
    root.querySelectorAll('.tree-toggle').forEach((btn) => btn.addEventListener('click', (e) => {
      e.preventDefault();
      const li = btn.closest('li');
      const sublist = li && li.querySelector(':scope > .tree-level');
      if (!sublist) return;
      const collapsed = sublist.classList.toggle('collapsed');
      btn.textContent = collapsed ? '▸' : '▾';
      btn.setAttribute('aria-expanded', String(!collapsed));
    }));
    root.querySelectorAll('.tree-expand-all').forEach((btn) => btn.addEventListener('click', () => {
      root.querySelectorAll('.tree-level.collapsed').forEach((el) => el.classList.remove('collapsed'));
      root.querySelectorAll('.tree-toggle').forEach((b) => { b.textContent = '▾'; b.setAttribute('aria-expanded', 'true'); });
    }));
    root.querySelectorAll('.tree-collapse-all').forEach((btn) => btn.addEventListener('click', () => {
      root.querySelectorAll('.tree-level').forEach((el, i) => { if (i > 0) el.classList.add('collapsed'); });
      root.querySelectorAll('.tree-toggle').forEach((b) => { b.textContent = '▸'; b.setAttribute('aria-expanded', 'false'); });
    }));
  }

  // ---------- router ----------
  // Engineering Objects are deliberately NOT rendered here. Every entry point
  // that resolves to one (Search, Cross References, Study Mode, Timeline,
  // Stats, Editorial Dashboard, Diff Viewer, Expansion Manager, Coverage
  // Matrix, the Browse tree) converges on the single Engineering Workspace
  // renderer (views/engineering.js) instead -- see TD-13's resolution in
  // TECHNICAL_DEBT.md and MIW_INTELLIGENCE_PRODUCT_SPECIFICATION.md §6's
  // "every entry point opens the *same* Engineering Workspace template."
  function showDetail(id, hintedKind, mode) {
    if (hintedKind === 'engineering-object' || DB.getEngineeringObject(id)) {
      window.RulesNav.showTab('engineering');
      window.RulesEngineering.selectCard(id);
      return;
    }
    mode = mode || 'node';
    let html = '';
    if (hintedKind === 'definition' || DB.getDefinition(id)) html = renderDefinitionDetail(id);
    else if (hintedKind === 'node' || (DB.getNode(id) && !DB.getStandard(id))) html = renderNodeDetail(id, mode);
    else if (DB.getStandard(id)) html = mode && mode !== 'node' ? renderContextViewHTML(id, mode) : renderStandardDetail(id);
    else if (DB.getNode(id)) html = renderNodeDetail(id, mode);
    else html = `<p>Nothing found for "${esc(id)}".</p>`;

    detailEl().innerHTML = html;
    detailEl().classList.add('open');
    if (mode === 'chapter') {
      const originAnchor = document.getElementById('ctx-node-' + id);
      if (originAnchor) originAnchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    detailEl().querySelectorAll('.xref[data-id]').forEach((a) =>
      a.addEventListener('click', (e) => { e.preventDefault(); showDetail(a.dataset.id); detailEl().scrollIntoView({ behavior: 'smooth', block: 'start' }); }));
    detailEl().querySelectorAll('.view-tab[data-mode]').forEach((btn) =>
      btn.addEventListener('click', (e) => { e.preventDefault(); showDetail(btn.dataset.id, hintedKind, btn.dataset.mode); detailEl().scrollIntoView({ behavior: 'smooth', block: 'start' }); }));
    wireTreeControls(detailEl());
  }

  function closeDetail() { detailEl().classList.remove('open'); detailEl().innerHTML = ''; }

  return {
    renderList, showDetail, closeDetail,
    esc, kindBadge, statusBadge, workflowBadge, resolveKind, titleOf, renderBreadcrumb, renderValidity,
    renderCitations, renderProvenance, renderCategorizedRelationships, renderTreeLevel, wireTreeControls,
    renderViewModeTabs, renderContextViewHTML
  };
})();
