// Offline full-text + keyword + synonym-expanded search over
// RulesDB.getSearchIndex(), plus Advanced Search: field-scoped filters
// (status, publisher/organization, standardType, edition, chapter,
// regulation number, validity presence, dependency-graph reachability) layered
// on top of the same scoring function — a citation-pattern query still always
// outranks everything else regardless of which filters are active.
window.RulesSearch = (function () {
  const DB = window.RulesDB;

  // Recognizes things like "SOLAS II-2/10", "Reg 10", "MSC.1/Circ.1321",
  // "ISM-4", "A.1207(34)" — patterns a user typing an exact reference uses.
  const CITATION_PATTERNS = [
    /\b[A-Z]{2,}(?:-[A-Z0-9]+)+\b/,          // SOLAS-II2-10, ISM-4-1
    /\b[A-Z]{2,3}\.\d+(?:\/Circ\.\d+)?\(?\d*\)?/i, // MSC.1/Circ.1321, MSC.532(107), A.1207(34)
    /\breg(?:ulation)?\.?\s*\d+/i,             // Regulation 10, Reg 10
  ];

  const FIELD_NAMES = ['status', 'publisher', 'organization', 'type', 'standardtype', 'edition', 'chapter', 'regulation', 'validity', 'depends'];

  function isCitationQuery(q) {
    return CITATION_PATTERNS.some((re) => re.test(q));
  }

  function normalizeText(s) {
    if (!s) return '';
    return String(s)
      .toLowerCase()
      .replace(/₂/g, '2')
      .replace(/₃/g, '3')
      .replace(/₄/g, '4')
      .replace(/°/g, ' deg ')
      .replace(/sulphur/g, 'sulfur')
      .replace(/p\/v\s*valve/g, 'pressure vacuum valve')
      .replace(/aux\s+steering/g, 'auxiliary steering gear')
      .replace(/co2\s+cylinder/g, 'carbon dioxide cylinder')
      .replace(/esd\s+space/g, 'esd-protected machinery space')
      .replace(/sox\s+limit/g, 'sulfur oxides')
      .replace(/neca/g, 'nitrogen oxides emission control area')
      .replace(/[\/\\\-_.\(\)]/g, ' ');
  }

  function expandQuery(q) {
    const syn = DB.getSynonyms ? DB.getSynonyms() : {};
    const norm = normalizeText(q);
    const rawLower = q.toLowerCase();
    const terms = new Set(norm.split(/\s+/).filter(Boolean));
    
    // Add un-normalized terms for exact matches
    rawLower.split(/\s+/).filter(Boolean).forEach((t) => terms.add(t));
    
    // Strip hyphens and slashes to form compact reference key
    const compactRef = rawLower.replace(/[^a-z0-9]/g, '');
    if (compactRef) terms.add(compactRef);

    Object.keys(syn).forEach((abbrev) => {
      const normAbbrev = normalizeText(abbrev);
      if (rawLower.includes(abbrev) || norm.includes(normAbbrev)) {
        normalizeText(syn[abbrev]).split(/\s+/).forEach((t) => terms.add(t));
      }
    });
    return Array.from(terms);
  }

  // Splits "fire safety status:current" into { text: "fire safety",
  // filters: { status: "current" } }. Recognized field names only — anything
  // else with a colon (e.g. "MSC.1/Circ.1321") is left in the free-text part.
  function parseAdvanced(rawQuery) {
    const filters = {};
    const words = (rawQuery || '').split(/\s+/);
    const textWords = [];
    words.forEach((w) => {
      const m = w.match(/^([A-Za-z]+):(.+)$/);
      if (m && FIELD_NAMES.includes(m[1].toLowerCase())) {
        let field = m[1].toLowerCase();
        if (field === 'standardtype') field = 'type';
        if (field === 'organization') field = 'publisher';
        filters[field] = m[2].toLowerCase();
      } else if (w) {
        textWords.push(w);
      }
    });
    return { text: textWords.join(' '), filters };
  }

  // Resolves the fields an item's underlying repository record actually
  // carries — the flattened search-index rows are lean, so node-kind items
  // resolve their owning standard for publisher/status/edition.
  function resolveFilterFields(item) {
    if (item.kind === 'standard') {
      const std = DB.getStandard(item.id);
      return {
        status: std && std.meta.status, publisher: std && std.meta.publisher,
        type: std && std.meta.standardType, editions: (std && std.meta.editions || []).map((e) => e.editionId),
        hasValidity: !!(std && std.meta.validity),
      };
    }
    if (item.kind === 'node') {
      const n = DB.getNode(item.id);
      const standardId = DB.getOwningStandardId(item.id);
      const std = DB.getStandard(standardId);
      return {
        status: std && std.meta.status, publisher: std && std.meta.publisher,
        type: std && std.meta.standardType, editions: n ? [n.editionId] : [],
        hasValidity: !!(n && n.validity), level: n && n.level, label: n && n.label,
      };
    }
    return {};
  }

  function matchesFilters(item, filters, dependencySet) {
    if (!Object.keys(filters).length) return true;
    const f = resolveFilterFields(item);
    if (filters.status && (f.status || '').toLowerCase() !== filters.status) return false;
    if (filters.publisher && !(f.publisher || '').toLowerCase().includes(filters.publisher)) return false;
    if (filters.type && (f.type || '').toLowerCase() !== filters.type) return false;
    if (filters.edition && !(f.editions || []).some((e) => (e || '').toLowerCase().includes(filters.edition))) return false;
    if (filters.chapter && !(f.level === 'chapter' && (f.label || '').toLowerCase() === filters.chapter)) return false;
    if (filters.regulation && !(f.level === 'regulation' && (f.label || '').toLowerCase() === filters.regulation)) return false;
    if (filters.validity === 'has' && !f.hasValidity) return false;
    if (filters.validity === 'missing' && f.hasValidity) return false;
    if (dependencySet && !dependencySet.has(item.id)) return false;
    return true;
  }

  // Very small scorer: term-frequency over the pre-flattened `text` field,
  // plus a big flat bonus for an id/title exact-ish match (the citation
  // engine's "always rank the exact reference first" rule).
  function score(item, queryTerms, rawQuery) {
    const hay = (item.text || item.title || '').toLowerCase();
    const normHay = normalizeText(item.text || item.title || '');
    const idLower = (item.id || '').toLowerCase();
    const normId = normalizeText(item.id || '');
    const compactId = idLower.replace(/[^a-z0-9]/g, '');
    const compactRaw = (rawQuery || '').toLowerCase().replace(/[^a-z0-9]/g, '');
    
    let s = 0;
    queryTerms.forEach((t) => {
      if (!t || t.length < 2) return;
      if (hay.includes(t) || normHay.includes(t)) s += 1;
      if (idLower.includes(t) || normId.includes(t)) s += 3;
    });
    
    if (compactRaw && (compactId === compactRaw || compactId.endsWith(compactRaw))) s += 100;
    if (compactRaw && compactId.includes(compactRaw)) s += 20;
    return s;
  }

  function search(rawQuery, opts) {
    opts = opts || {};
    const index = DB.getSearchIndex();
    const parsed = parseAdvanced(rawQuery || '');
    const filters = Object.assign({}, parsed.filters, opts.filters || {});
    const freeText = parsed.text;

    let dependencySet = null;
    if (filters.depends) {
      const root = index.find((i) => (i.id || '').toLowerCase() === filters.depends || (i.title || '').toLowerCase().includes(filters.depends));
      if (root) {
        dependencySet = new Set(DB.getDependencyChain(root.id).map((e) => e.to));
        dependencySet.add(root.id);
      } else {
        dependencySet = new Set(); // no match -> empty result set rather than ignoring the filter
      }
    }

    let base;
    if (!freeText.trim()) {
      base = index.map((item) => ({ item, s: 1 }));
    } else {
      const terms = expandQuery(freeText);
      base = index.map((item) => ({ item, s: score(item, terms, freeText) })).filter((r) => r.s > 0);
    }

    let results = base.filter((r) => matchesFilters(r.item, filters, dependencySet));
    if (opts.kind) results = results.filter((r) => r.item.kind === opts.kind);

    const citationBoost = freeText && isCitationQuery(freeText);
    results.sort((a, b) => {
      if (citationBoost) {
        const norm = freeText.toLowerCase().replace(/[^a-z0-9]/g, '');
        const aIdHit = a.item.id.toLowerCase().replace(/[^a-z0-9]/g, '').includes(norm);
        const bIdHit = b.item.id.toLowerCase().replace(/[^a-z0-9]/g, '').includes(norm);
        if (aIdHit && !bIdHit) return -1;
        if (bIdHit && !aIdHit) return 1;
      }
      return b.s - a.s;
    });
    return results.map((r) => r.item);
  }

  return { search, isCitationQuery, expandQuery, parseAdvanced };
})();
