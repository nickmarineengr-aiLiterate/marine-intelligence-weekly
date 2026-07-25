// Loads the repository's generated index/*.json artifacts and exposes a
// small, synchronous-feeling API over them. This is the ONLY place app/
// touches repository/index/** — render.js, search.js and the view modules
// never fetch directly. Fully offline: every fetch is to a local relative path.
window.RulesDB = (function () {
  const BASE = '../repository/index/';
  const REPO_BASE = '../repository/';

  let repoData = null; // {organizations, standards:[{meta,nodes}], definitions, engineeringObjects, extensions}
  let crossrefGraph = null;
  let synonyms = null;
  let statusTimeline = null;
  let manifest = null;
  let searchIndex = null;
  let coverage = null;
  let healthCheck = null;
  let changelog = null;
  let workflowStatus = null;
  let integrityReport = null;
  let performanceReport = null;
  let diffManifest = null;
  let expansionManager = null;
  let coverageMatrix = null;
  let amendmentTracker = null;
  let metricsHistory = null;

  // flat lookup maps, built once data lands
  let standardById = {};
  let nodeById = {};
  let nodeParentStandardId = {};
  let eoByTargetId = {}; // reverse index: node/standard id -> [{eo, relationship}]
  let packageByStandardId = {};
  let referenceFrequency = null; // cached, built lazily

  async function load() {
    const [rd, cg, syn, tl, mf, si, cov, hc, cl, ws, ir, pr, dm, em, cm, at, mh] = await Promise.all([
      fetch(BASE + 'repo-data.json').then((r) => r.json()),
      fetch(BASE + 'crossref-graph.json').then((r) => r.json()),
      fetch(BASE + 'synonyms.json').then((r) => r.json()),
      fetch(BASE + 'status-timeline.json').then((r) => r.json()),
      fetch(BASE + 'manifest.json').then((r) => r.json()),
      fetch(BASE + 'search-index.json').then((r) => r.json()),
      fetch(BASE + 'coverage.json').then((r) => r.json()),
      fetch(BASE + 'health-check.json').then((r) => r.json()),
      fetch(REPO_BASE + 'CHANGELOG.json').then((r) => r.json()).catch(() => []),
      fetch(BASE + 'workflow-status.json').then((r) => r.json()).catch(() => null),
      fetch(BASE + 'integrity-report.json').then((r) => r.json()).catch(() => null),
      fetch(BASE + 'performance-report.json').then((r) => r.json()).catch(() => null),
      fetch(BASE + 'diffs/manifest.json').then((r) => r.json()).catch(() => []),
      fetch(BASE + 'expansion-manager.json').then((r) => r.json()).catch(() => null),
      fetch(BASE + 'coverage-matrix.json').then((r) => r.json()).catch(() => null),
      fetch(BASE + 'amendment-tracker.json').then((r) => r.json()).catch(() => null),
      fetch(BASE + 'metrics-history.json').then((r) => r.json()).catch(() => null),
    ]);
    repoData = rd;
    crossrefGraph = cg;
    synonyms = syn;
    statusTimeline = tl;
    manifest = mf;
    searchIndex = si;
    coverage = cov;
    healthCheck = hc;
    changelog = cl;
    workflowStatus = ws;
    integrityReport = ir;
    performanceReport = pr;
    diffManifest = dm;
    expansionManager = em;
    coverageMatrix = cm;
    amendmentTracker = at;
    metricsHistory = mh;

    repoData.standards.forEach((s) => {
      standardById[s.meta.id] = s;
      (s.nodes || []).forEach((n) => {
        nodeById[n.id] = n;
        nodeParentStandardId[n.id] = s.meta.id;
      });
    });

    (repoData.engineeringObjects || []).forEach((k) => {
      (k.relatedNodes || []).forEach((rn) => {
        (eoByTargetId[rn.targetId] = eoByTargetId[rn.targetId] || []).push({ eo: k, relationship: rn.relationship });
      });
    });

    Object.keys(coverage.packages || {}).forEach((pkgName) => {
      coverage.packages[pkgName].forEach((row) => { packageByStandardId[row.id] = pkgName; });
    });

    return manifest;
  }

  function getStandard(id) { return standardById[id] || null; }
  function getNode(id) { return nodeById[id] || null; }
  function getOwningStandardId(nodeId) { return nodeParentStandardId[nodeId] || null; }
  function getOrganization(id) { return (repoData.organizations || {})[id] || null; }
  function getOrganizations() { return repoData.organizations || {}; }
  function getEdges(id) { return crossrefGraph[id] || { outgoing: [], incoming: [] }; }
  function getDefinitions() { return repoData.definitions || []; }
  function getDefinition(id) { return (repoData.definitions || []).find((d) => d.id === id) || null; }
  function getEngineeringObjects() { return repoData.engineeringObjects || []; }
  function getEngineeringObject(id) { return (repoData.engineeringObjects || []).find((k) => k.id === id) || null; }
  function getEngineeringObjectsFor(targetId) { return eoByTargetId[targetId] || []; }
  function getIllustrations() { return repoData.illustrations || []; }
  function getIllustration(id) { return (repoData.illustrations || []).find((i) => i.id === id) || null; }
  function getExtensionsFor(targetNodeId) {
    return (repoData.extensions || []).filter((e) => (e.targetNodeId || e.targetId) === targetNodeId);
  }
  function getAllStandards() { return repoData.standards; }
  function getTimeline() { return statusTimeline || []; }
  function getSynonyms() { return synonyms || {}; }
  function getSearchIndex() { return searchIndex || []; }
  function getManifest() { return manifest; }
  function getCoverage() { return coverage; }
  function getHealthCheck() { return healthCheck; }
  function getPackageOf(standardId) { return packageByStandardId[standardId] || 'Unassigned'; }

  // Children of a node/standard, in tree order (for hierarchy browsing).
  // Reconstructed on demand from parentId, since flattenTree() only kept the
  // flat array (children[] was stripped when flattening in lib.js).
  function getChildren(parentId, standardId) {
    const std = standardById[standardId];
    if (!std) return [];
    return std.nodes.filter((n) => n.parentId === parentId);
  }
  function getTopLevelNodes(standardId) {
    const std = standardById[standardId];
    if (!std) return [];
    return std.nodes.filter((n) => n.parentId === null);
  }

  // "Show current consolidated version": the edition with effectiveTo:null
  // (falls back to the last edition if none is marked open-ended).
  function getCurrentEdition(standardMeta) {
    const editions = standardMeta.editions || [];
    return editions.find((e) => e.effectiveTo === null) || editions[editions.length - 1] || null;
  }

  // Follows depends_on edges outward from a starting id, breadth-first,
  // capped so a cyclic graph (shouldn't happen, but never trust data blindly)
  // can't hang the UI.
  function getDependencyChain(startId, maxDepth) {
    maxDepth = maxDepth || 6;
    const chain = [];
    const seen = new Set([startId]);
    let frontier = [startId];
    let depth = 0;
    while (frontier.length && depth < maxDepth) {
      const next = [];
      frontier.forEach((id) => {
        const edges = getEdges(id).outgoing.filter((e) => e.type === 'depends_on');
        edges.forEach((e) => {
          if (!seen.has(e.targetId)) {
            seen.add(e.targetId);
            chain.push({ from: id, to: e.targetId, note: e.note || null });
            next.push(e.targetId);
          }
        });
      });
      frontier = next;
      depth++;
    }
    return chain;
  }

  // Every id ever seen as a relationship target, ranked by how many incoming
  // edges point at it — "most frequently referenced" for Study Mode. Built
  // once, lazily, from the same crossref-graph the detail views already read.
  function getReferenceFrequency() {
    if (referenceFrequency) return referenceFrequency;
    referenceFrequency = Object.keys(crossrefGraph)
      .map((id) => ({ id, count: (crossrefGraph[id].incoming || []).length }))
      .filter((r) => r.count > 0)
      .sort((a, b) => b.count - a.count);
    return referenceFrequency;
  }

  // Extracts a trailing 4-digit year from an inconsistently-formatted date
  // string ("2026-01-01", "1968/2000", "1958") so timeline entries can be
  // sorted/ranked without assuming a strict ISO format everywhere.
  function yearOf(dateStr) {
    if (!dateStr) return null;
    const matches = String(dateStr).match(/\d{4}/g);
    if (!matches) return null;
    return parseInt(matches[matches.length - 1], 10);
  }

  // Most recent version-effective timeline entries (amendments), newest
  // first, capped at n. Used by Study Mode's "recently amended" panel.
  function getRecentAmendments(n) {
    n = n || 15;
    return (statusTimeline || [])
      .filter((t) => t.action === 'version-effective')
      .map((t) => ({ ...t, year: yearOf(t.date) }))
      .filter((t) => t.year !== null)
      .sort((a, b) => b.year - a.year || (b.date > a.date ? 1 : -1))
      .slice(0, n);
  }

  function getTimelineForStandard(standardId) {
    return (statusTimeline || []).filter((t) => t.standardId === standardId);
  }

  // ---------- Stage 2B: editorial workflow, change tracking, QA reports ----------
  function getChangelog() { return changelog || []; }
  function getWorkflowStatus(id) { return workflowStatus && workflowStatus.byId ? (workflowStatus.byId[id] || null) : null; }
  function getWorkflowCounts() { return workflowStatus ? workflowStatus.counts : {}; }
  function getIntegrityReport() { return integrityReport; }
  function getPerformanceReport() { return performanceReport; }
  function getDiffManifest() { return diffManifest || []; }
  function fetchDiffReport(fileName) { return fetch(BASE + 'diffs/' + fileName).then((r) => r.json()); }

  // "Recently modified" for the Editorial Dashboard: changelog entries,
  // newest first, with the standard ids they touched resolved from
  // filesChanged paths (repository/standards/**/<segment>/...).
  function getRecentChanges(n) {
    n = n || 20;
    return (changelog || [])
      .slice()
      .sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0))
      .slice(0, n)
      .map((entry) => {
        const touchedStandardIds = new Set();
        (entry.filesChanged || []).forEach((f) => {
          const m = f.match(/^repository\/standards\/[^/]+\/([^/]+)\//);
          if (m) touchedStandardIds.add(m[1]);
        });
        return { ...entry, touchedStandardIds: Array.from(touchedStandardIds) };
      });
  }

  // ---------- Stage 3: Expansion Manager, Coverage Matrix, Amendment Tracker, Metrics ----------
  function getExpansionManager() { return expansionManager; }
  function getCoverageMatrix() { return coverageMatrix; }
  function getAmendmentTracker() { return amendmentTracker; }
  function getMetricsHistory() { return metricsHistory; }

  function getContextView(targetId, mode) {
    mode = mode || 'node';
    const n = getNode(targetId);
    const s = getStandard(targetId);
    const standardId = n ? getOwningStandardId(targetId) : (s ? s.meta.id : null);
    const std = standardId ? getStandard(standardId) : null;

    if (!n && !std) return null;

    if (mode === 'node') {
      return { mode: 'node', targetId, node: n, standard: std };
    }

    if (mode === 'regulation') {
      let regNode = n;
      if (n && n.level !== 'regulation') {
        let cur = n;
        while (cur && cur.parentId) {
          const parent = getNode(cur.parentId);
          if (parent && parent.level === 'regulation') {
            regNode = parent;
            break;
          }
          cur = parent;
        }
      }

      if (!regNode && std) {
        const top = getTopLevelNodes(std.meta.id);
        const findReg = (list) => {
          for (let item of list) {
            if (item.level === 'regulation') return item;
            const subs = getChildren(item.id, std.meta.id);
            const found = findReg(subs);
            if (found) return found;
          }
          return null;
        };
        regNode = findReg(top);
      }

      if (!regNode) regNode = n;

      const nodes = [];
      const collect = (item) => {
        if (!item) return;
        nodes.push(item);
        const children = getChildren(item.id, standardId);
        children.forEach(collect);
      };
      if (regNode) collect(regNode);

      return {
        mode: 'regulation',
        targetId: regNode ? regNode.id : targetId,
        title: regNode ? `${regNode.level} ${regNode.label} — ${regNode.title}` : (std ? std.meta.title : targetId),
        standard: std,
        regNode: regNode,
        nodes: nodes
      };
    }

    if (mode === 'chapter') {
      let chNode = n;
      if (n && n.level !== 'chapter' && n.level !== 'part') {
        let cur = n;
        while (cur && cur.parentId) {
          const parent = getNode(cur.parentId);
          if (parent && (parent.level === 'chapter' || parent.level === 'part')) {
            chNode = parent;
            break;
          }
          cur = parent;
        }
      }

      if (!chNode && std) {
        const top = getTopLevelNodes(std.meta.id);
        chNode = top.length > 0 ? top[0] : null;
      }

      if (!chNode) chNode = n;

      const nodes = [];
      const collect = (item) => {
        if (!item) return;
        nodes.push(item);
        const children = getChildren(item.id, standardId);
        children.forEach(collect);
      };
      if (chNode) collect(chNode);

      return {
        mode: 'chapter',
        targetId: chNode ? chNode.id : targetId,
        title: chNode ? `${chNode.level} ${chNode.label} — ${chNode.title}` : (std ? std.meta.title : targetId),
        standard: std,
        chapterNode: chNode,
        nodes: nodes
      };
    }

    if (mode === 'document') {
      const top = std ? getTopLevelNodes(std.meta.id) : [];
      const nodes = [];
      const collect = (item) => {
        if (!item) return;
        nodes.push(item);
        const children = getChildren(item.id, standardId);
        children.forEach(collect);
      };
      top.forEach(collect);

      return {
        mode: 'document',
        targetId: std ? std.meta.id : targetId,
        title: std ? (std.meta.abbreviation || std.meta.title) : targetId,
        standard: std,
        nodes: nodes
      };
    }

    return null;
  }

  return {
    load, getStandard, getNode, getOwningStandardId, getOrganization, getOrganizations, getEdges,
    getDefinitions, getDefinition, getEngineeringObjects, getEngineeringObject, getEngineeringObjectsFor,
    getIllustrations, getIllustration,
    getExtensionsFor, getAllStandards, getTimeline, getSynonyms, getSearchIndex,
    getChildren, getTopLevelNodes, getCurrentEdition, getDependencyChain,
    getManifest, getCoverage, getHealthCheck, getPackageOf,
    getReferenceFrequency, getRecentAmendments, getTimelineForStandard, yearOf,
    getChangelog, getWorkflowStatus, getWorkflowCounts, getIntegrityReport, getPerformanceReport,
    getDiffManifest, fetchDiffReport, getRecentChanges,
    getExpansionManager, getCoverageMatrix, getAmendmentTracker, getMetricsHistory,
    getContextView
  };
})();
