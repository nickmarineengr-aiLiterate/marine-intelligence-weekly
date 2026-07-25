// Engineering Object Explorer: dedicated pages for real-world equipment/
// systems (repository/engineering-objects/*.json), grouping every related
// provision by document category (conventions/codes/IRS rules/circulars),
// plus definitions, MIW notes, cross-referenced engineering objects that
// share a provision, and study dependencies pulled via the depends_on graph.
window.RulesEngineering = (function () {
  const DB = window.RulesDB;
  const R = window.RulesRender;

  function standardTypeOf(targetId) {
    const n = DB.getNode(targetId);
    const standardId = n ? DB.getOwningStandardId(targetId) : targetId;
    const std = DB.getStandard(standardId);
    return std ? std.meta.standardType : null;
  }

  function groupRelatedNodes(relatedNodes) {
    const groups = { convention: [], code: [], rule: [], circular: [], other: [] };
    (relatedNodes || []).forEach((r) => {
      const std = DB.getStandard(DB.getNode(r.targetId) ? DB.getOwningStandardId(r.targetId) : r.targetId);
      const t = std ? std.meta.standardType : null;
      if (t === 'convention') groups.convention.push(r);
      else if (t === 'code') groups.code.push(r);
      else if (t === 'rule') groups.rule.push(r);
      else if (t === 'circular') groups.circular.push(r);
      else groups.other.push(r);
    });
    return groups;
  }

  function renderRelGroup(title, items) {
    if (!items.length) return '';
    return `<h4>${R.esc(title)}</h4><div class="reg-box">${items.map((r) => `
      <div class="reg-item"><a href="#" class="xref reg-code" data-id="${R.esc(r.targetId)}">${R.esc(R.titleOf(r.targetId) || r.targetId)}</a><span class="reg-desc">${R.esc(r.relationship)}</span></div>`).join('')}</div>`;
  }

  function findCrossReferencedEOs(eo) {
    const myTargets = new Set((eo.relatedNodes || []).map((r) => r.targetId));
    const shared = [];
    DB.getEngineeringObjects().forEach((other) => {
      if (other.id === eo.id) return;
      const overlap = (other.relatedNodes || []).filter((r) => myTargets.has(r.targetId));
      if (overlap.length) shared.push({ eo: other, overlap });
    });
    return shared;
  }

  function studyDependencies(eo) {
    const seen = new Set();
    const chain = [];
    (eo.relatedNodes || []).forEach((r) => {
      DB.getDependencyChain(r.targetId).forEach((e) => {
        const key = e.from + '>' + e.to;
        if (!seen.has(key)) { seen.add(key); chain.push(e); }
      });
    });
    return chain;
  }

  // Every extension note attached to any of this object's related nodes,
  // deduped -- same data renderNotes() always used, just not yet grouped.
  function allNotes(eo) {
    const seen = new Set();
    const notes = [];
    (eo.relatedNodes || []).forEach((r) => {
      DB.getExtensionsFor(r.targetId).forEach((note) => {
        const key = note.type + '|' + note.text;
        if (!seen.has(key)) { seen.add(key); notes.push(note); }
      });
    });
    return notes;
  }

  // Presentation grouping only -- no new data, no new authoring convention.
  // Maps the extension `type` values already in use (Package 2's SOLAS Reg.
  // 10 pilot, Package 4's MIW references) onto the section headings a
  // marine engineer actually thinks in, so "everything about this concept"
  // reads as a workspace instead of an undifferentiated note dump.
  //
  // Each entry also carries the four-cluster grouping
  // (MIW_INTELLIGENCE_PRODUCT_SPECIFICATION.md §7): 'overview' ("what is
  // this"), 'understanding' ("how do I work with it"), 'study' ("what will
  // I be tested on"). 'explore' has no note types of its own -- it renders
  // Cross References/Recommended Reading Order directly in renderDetail().
  //
  // 'regulatory-lineage' is deliberately excluded here -- it renders inside
  // renderAmendmentKnowledge() below, combined with citation-derived amendment
  // data under one heading, per §9's confirmed "Amendment Knowledge renders
  // twice" finding. 'ai-knowledge' is folded into the same section as
  // 'practical-guidance' (one heading, both types) per §8's terminology
  // guidance -- "AI Knowledge" describes how a note was authored, not what
  // it contains, so it should not be its own subscriber-facing heading.
  const NOTE_SECTIONS = [
    { types: ['components'], title: 'Components', cluster: 'overview' },
    { types: ['engineering-context'], title: 'Engineering Context', cluster: 'understanding' },
    { types: ['practical-guidance', 'ai-knowledge'], title: 'Practical Guidance', cluster: 'understanding' },
    { types: ['inspection-guidance'], title: 'Inspection Guidance', cluster: 'understanding' },
    { types: ['maintenance-guidance'], title: 'Maintenance Guidance', cluster: 'understanding' },
    { types: ['failure-modes'], title: 'Failure Modes', cluster: 'understanding' },
    { types: ['qb-reference'], title: 'Question Bank References (MIW)', cluster: 'study' },
    { types: ['oral-notes-reference'], title: 'Oral Notes (MIW)', cluster: 'study' },
    { types: ['wa-reference'], title: 'Written Answers (MIW)', cluster: 'study' },
    { types: ['ce-relevance'], title: 'Examination Knowledge', cluster: 'study' },
  ];

  const CLUSTERS = [
    { id: 'overview', title: 'Overview' },
    { id: 'understanding', title: 'Understanding It' },
    { id: 'study', title: 'Study & Exam Prep' },
    { id: 'explore', title: 'Explore Further' },
  ];

  // A note's own provenance, not the section it lands in, decides the (MIW)
  // badge -- so the badge stays correct even where an MIW-sourced and an
  // AI-authored note ever share one heading, rather than relying on a fixed
  // per-section title string (see §9's "extend consistent MIW badging").
  function isMiwSourced(note) {
    return !!(note.provenance && note.provenance.sourceType === 'miw_original');
  }

  function renderNoteSection(title, notes) {
    if (!notes.length) return '';
    return `<h4>${R.esc(title)}</h4>${notes.map((note) => `<div class="ce-tip">${isMiwSourced(note) ? '<span class="miw-badge">MIW</span>' : ''}${R.esc(note.text)}</div>`).join('')}`;
  }

  // Renders only the note sections belonging to one cluster. Any note type
  // not yet mapped to a NOTE_SECTIONS entry (future-proofing, not a case
  // that exists in this repository today) surfaces under "Other Notes" in
  // the 'understanding' cluster rather than being silently dropped.
  function renderNotesGrouped(eo, clusterId) {
    const notes = allNotes(eo).filter((n) => n.type !== 'regulatory-lineage');
    const used = new Set();
    let html = '';
    NOTE_SECTIONS.filter((s) => s.cluster === clusterId).forEach((section) => {
      const matched = notes.filter((n) => section.types.includes(n.type));
      matched.forEach((n) => used.add(n));
      html += renderNoteSection(section.title, matched);
    });
    if (clusterId === 'understanding') {
      const knownTypes = new Set(NOTE_SECTIONS.flatMap((s) => s.types));
      const leftover = notes.filter((n) => !used.has(n) && !knownTypes.has(n.type));
      html += renderNoteSection('Other Notes', leftover);
    }
    return html;
  }

  // Counts feeding both the Workspace's own quick-jump nav (below) and the
  // Unified Search EO cluster card (render.js's renderList()) -- one shared
  // computation so the two never drift out of sync with each other. No new
  // data: every count is derived from fields the Workspace detail view
  // already reads (relatedNodes/relatedExtensions/relatedDefinitions,
  // extension notes, and the crossref/dependency graphs).
  function clusterCounts(eo) {
    const notes = allNotes(eo).filter((n) => n.type !== 'regulatory-lineage');
    const countForCluster = (clusterId) => notes.filter((n) =>
      NOTE_SECTIONS.some((s) => s.cluster === clusterId && s.types.includes(n.type))
    ).length;
    return {
      overview: countForCluster('overview'),
      understanding: countForCluster('understanding'),
      study: countForCluster('study'),
      relatedObjects: findCrossReferencedEOs(eo).length,
      readingOrder: studyDependencies(eo).length,
      definitions: (eo.relatedDefinitions || []).map((r) => DB.getDefinition(r.targetId)).filter(Boolean).length,
    };
  }

  // Citations that carry a resolution/amendment/entryIntoForce -- i.e.
  // genuine amendment history, distinct from a node's base "which document"
  // citation -- across every node this object relates to. Existing
  // citation.schema.json fields, not new data; just never surfaced here
  // before.
  function amendmentCitations(eo) {
    const seen = new Set();
    const items = [];
    (eo.relatedNodes || []).forEach((r) => {
      const n = DB.getNode(r.targetId);
      (n && n.citations || []).forEach((c) => {
        if (!c.resolution && !c.amendment) return;
        const key = r.targetId + '|' + (c.resolution || c.amendment);
        if (seen.has(key)) return;
        seen.add(key);
        items.push({ targetId: r.targetId, citation: c });
      });
    });
    return items;
  }

  // Combines both of this repository's amendment-history data sources under
  // ONE heading: citation-level resolution/amendment fields (amendmentCitations,
  // above) and 'regulatory-lineage' extension notes (prose amendment research).
  // Previously these rendered as two separately-titled sections ("Amendment
  // Knowledge" and "Amendment Knowledge (from Engineering Intelligence)") --
  // a confirmed, concrete duplicate-rendering bug
  // (MIW_INTELLIGENCE_PRODUCT_SPECIFICATION.md §9) rather than two distinct
  // concepts a subscriber needs to see separately.
  function renderAmendmentKnowledge(eo) {
    const items = amendmentCitations(eo);
    const notes = allNotes(eo).filter((n) => n.type === 'regulatory-lineage');
    if (!items.length && !notes.length) return '';
    const citationsHtml = items.length ? `<div class="reg-box">${items.map(({ targetId, citation }) => `
      <div class="reg-item">
        <a href="#" class="xref reg-code" data-id="${R.esc(targetId)}">${R.esc(R.titleOf(targetId) || targetId)}</a>
        <span class="reg-desc">${R.esc(citation.doc)}${citation.resolution ? ' · Res. ' + R.esc(citation.resolution) : ''}${citation.entryIntoForce ? ' · EIF ' + R.esc(citation.entryIntoForce) : ''}</span>
      </div>`).join('')}</div>` : '';
    const notesHtml = notes.map((note) => `<div class="ce-tip">${isMiwSourced(note) ? '<span class="miw-badge">MIW</span>' : ''}${R.esc(note.text)}</div>`).join('');
    return `<h4>Amendment Knowledge</h4>${citationsHtml}${notesHtml}`;
  }

  // Quick-jump nav: one pill per cluster, count badge from the same
  // clusterCounts() the search card uses, smooth-scrolls to that cluster's
  // <section> inside this same panel -- no page navigation, no new
  // mechanism, just an anchor-scroll wired after the panel is in the DOM.
  function renderJumpNav(counts) {
    const countFor = (id) => {
      if (id === 'overview') return counts.overview + counts.definitions;
      if (id === 'understanding') return counts.understanding;
      if (id === 'study') return counts.study;
      if (id === 'explore') return counts.relatedObjects + (counts.readingOrder ? 1 : 0);
      return 0;
    };
    return `<nav class="workspace-jumpnav">${CLUSTERS.map((c) => `
      <a href="#" class="workspace-jump-btn" data-cluster="${c.id}">${R.esc(c.title)}${countFor(c.id) ? ` <span class="workspace-jump-count">${countFor(c.id)}</span>` : ''}</a>`).join('')}</nav>`;
  }

  function renderDetail(id) {
    const eo = DB.getEngineeringObject(id);
    const panel = document.getElementById('eo-detail');
    if (!panel) return;
    if (!eo) { panel.innerHTML = '<p class="muted">Select an engineering object above.</p>'; return; }

    const groups = groupRelatedNodes(eo.relatedNodes);
    const defs = (eo.relatedDefinitions || []).map((r) => DB.getDefinition(r.targetId)).filter(Boolean);
    const crossRefs = findCrossReferencedEOs(eo);
    const deps = studyDependencies(eo);
    const counts = clusterCounts(eo);

    const componentsHtml = renderNotesGrouped(eo, 'overview');
    const amendmentHtml = renderAmendmentKnowledge(eo);
    const understandingHtml = renderNotesGrouped(eo, 'understanding');
    const studyHtml = renderNotesGrouped(eo, 'study');

    panel.innerHTML = `
      <div class="detail-head"><h2>${R.esc(eo.title)} <span class="kind-badge bd-eo">${R.esc(eo.kind)}</span></h2>
        ${eo.aliases && eo.aliases.length ? '<div class="detail-meta"><span>Also known as: ' + eo.aliases.map(R.esc).join(', ') + '</span></div>' : ''}
      </div>

      ${renderJumpNav(counts)}

      <section id="cluster-overview" class="workspace-cluster">
        <h3>Overview</h3>
        <h4>Engineering Overview</h4>
        <p class="summary-text">${R.esc(eo.description)}</p>
        <h4>Official Context</h4>
        ${renderRelGroup('Applicable conventions', groups.convention)}
        ${renderRelGroup('Applicable codes', groups.code)}
        ${renderRelGroup('IRS rules', groups.rule)}
        ${renderRelGroup('Circulars', groups.circular)}
        ${renderRelGroup('Other related standards', groups.other)}
        ${defs.length ? '<h4>Definitions</h4><div class="reg-box">' + defs.map((d) => `<div class="reg-item"><a href="#" class="xref reg-code" data-id="${R.esc(d.id)}">${R.esc(d.term)}</a></div>`).join('') + '</div>' : ''}
        ${amendmentHtml}
        ${componentsHtml}
      </section>

      <section id="cluster-understanding" class="workspace-cluster">
        <h3>Understanding It</h3>
        ${understandingHtml.trim().length ? understandingHtml : '<p class="muted">Engineering guidance for this system is still being developed.</p>'}
      </section>

      <section id="cluster-study" class="workspace-cluster">
        <h3>Study &amp; Exam Prep</h3>
        ${studyHtml.trim().length ? studyHtml : '<p class="muted">No Marine Intelligence Weekly exam-preparation references have been identified for this system yet.</p>'}
      </section>

      <section id="cluster-explore" class="workspace-cluster">
        <h3>Explore Further</h3>
        <h4>Related Engineering Objects</h4>
        ${crossRefs.length
          ? `<div class="reg-box">${crossRefs.map((c) => `<div class="reg-item"><a href="#" class="xref reg-code eo-switch" data-id="${R.esc(c.eo.id)}">${R.esc(c.eo.title)}</a><span class="reg-desc">shares ${c.overlap.length} provision(s): ${c.overlap.map((o) => R.esc(o.targetId)).join(', ')}</span></div>`).join('')}</div>`
          : '<p class="muted">No other engineering object in the repository currently shares a provision with this one.</p>'}
        <h4>Recommended Reading Order</h4>
        ${deps.length
          ? `<div class="dep-chain">${deps.map((e) => `<a href="#" class="xref dep-link" data-id="${R.esc(e.to)}">${R.esc(e.to)}</a>`).join(' <span class="dep-arrow">→</span> ')}</div>`
          : '<p class="muted">No recommended reading order recorded for this object\'s related provisions.</p>'}
      </section>
    `;
    panel.querySelectorAll('.xref[data-id]:not(.eo-switch)').forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault();
      window.RulesNav.showTab('search');
      R.showDetail(a.dataset.id);
    }));
    panel.querySelectorAll('.eo-switch').forEach((a) => a.addEventListener('click', (e) => { e.preventDefault(); selectCard(a.dataset.id); }));
    panel.querySelectorAll('.workspace-jump-btn').forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.getElementById('cluster-' + a.dataset.cluster);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }));
  }

  function selectCard(id) {
    document.querySelectorAll('#eo-grid .eo-card').forEach((c) => c.classList.toggle('active', c.dataset.id === id));
    renderDetail(id);
    const panel = document.getElementById('eo-detail');
    if (panel) panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function renderGrid() {
    const grid = document.getElementById('eo-grid');
    if (!grid) return;
    const items = DB.getEngineeringObjects();
    if (!items.length) { grid.innerHTML = '<p class="muted">No engineering objects in the repository yet.</p>'; return; }
    grid.innerHTML = items.map((eo) => `
      <div class="eo-card" data-id="${R.esc(eo.id)}">
        <div class="eo-card-title">${R.esc(eo.title)}</div>
        <div class="eo-card-kind">${R.esc(eo.kind)}</div>
        <div class="eo-card-desc">${R.esc((eo.description || '').slice(0, 140))}${(eo.description || '').length > 140 ? '…' : ''}</div>
        <div class="eo-card-count">${(eo.relatedNodes || []).length} related provision(s)</div>
      </div>`).join('');
    grid.querySelectorAll('.eo-card').forEach((card) => card.addEventListener('click', () => selectCard(card.dataset.id)));
  }

  function init() {
    renderGrid();
    const items = DB.getEngineeringObjects();
    if (items.length) selectCard(items[0].id);
  }

  // selectCard is exported so any other entry point (Search, Cross
  // References, Study Mode, Timeline, Stats, Editorial Dashboard, Diff
  // Viewer, Expansion Manager, Coverage Matrix, the Browse tree) can open an
  // Engineering Object through this same Workspace instead of maintaining a
  // second renderer -- see render.js's showDetail() router and TD-13's
  // resolution in TECHNICAL_DEBT.md.
  // clusterCounts is exported so the Unified Search result card
  // (render.js's renderList()) can preview the same four-cluster counts the
  // Workspace's own quick-jump nav shows -- one shared computation, not a
  // second one that could drift out of sync.
  return { init, selectCard, clusterCounts };
})();
