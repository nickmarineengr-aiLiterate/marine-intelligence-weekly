// Timeline View: chronological navigation over repository/index/status-
// timeline.json (every edition/version effective-date already flattened by
// build-index.js). Filterable to a single standard or the whole repository.
window.RulesTimeline = (function () {
  const DB = window.RulesDB;
  const R = window.RulesRender;

  // Splits into chronologically-sortable events (a parseable year) and
  // undated ones ("Not specified" etc.) — undated entries have no place on a
  // chronological axis, so they're listed separately rather than sorted to
  // the front as if year 0.
  function eventsFor(standardId) {
    const list = standardId ? DB.getTimelineForStandard(standardId) : DB.getTimeline();
    const withYear = list.map((t) => ({ ...t, year: DB.yearOf(t.date) }));
    const dated = withYear.filter((t) => t.year !== null).sort((a, b) => a.year - b.year || (a.date < b.date ? -1 : a.date > b.date ? 1 : 0));
    const undated = withYear.filter((t) => t.year === null);
    return { dated, undated };
  }

  function renderItem(t) {
    const std = DB.getStandard(t.standardId);
    const label = std ? (std.meta.abbreviation || std.meta.title) : t.standardId;
    const isEdition = t.action === 'edition-effective';
    return { std, label, isEdition };
  }

  function render(standardId) {
    const track = document.getElementById('timeline-track');
    if (!track) return;
    const { dated, undated } = eventsFor(standardId);
    if (!dated.length && !undated.length) { track.innerHTML = '<p class="muted">No events recorded for this selection.</p>'; return; }

    let lastYear = null;
    let html = dated.map((t) => {
      const { label, isEdition } = renderItem(t);
      const yearMarker = t.year !== lastYear ? `<div class="tl-year">${R.esc(t.year)}</div>` : '';
      lastYear = t.year;
      return `${yearMarker}<div class="tl-item ${isEdition ? 'tl-edition' : 'tl-version'}">
        <div class="tl-dot"></div>
        <div class="tl-content">
          <div class="tl-date">${R.esc(t.date)}</div>
          <div class="tl-title"><a href="#" class="xref" data-id="${R.esc(t.standardId)}">${R.esc(label)}</a> ${isEdition ? R.statusBadge(t.status) + ' ' + R.esc(t.label || '') : 'v' + R.esc(t.version || '')}</div>
          ${t.summary ? '<div class="tl-summary">' + R.esc(t.summary) + '</div>' : ''}
          ${t.changeRef ? '<div class="tl-changeref">via <a href="#" class="xref" data-id="' + R.esc(t.changeRef) + '">' + R.esc(t.changeRef) + '</a></div>' : ''}
        </div>
      </div>`;
    }).join('');

    if (undated.length) {
      html += `<div class="tl-year">Undated</div>` + undated.map((t) => {
        const { label, isEdition } = renderItem(t);
        return `<div class="tl-item ${isEdition ? 'tl-edition' : 'tl-version'}">
          <div class="tl-dot"></div>
          <div class="tl-content">
            <div class="tl-date">${R.esc(t.date)}</div>
            <div class="tl-title"><a href="#" class="xref" data-id="${R.esc(t.standardId)}">${R.esc(label)}</a> ${isEdition ? R.statusBadge(t.status) + ' ' + R.esc(t.label || '') : 'v' + R.esc(t.version || '')}</div>
            ${t.summary ? '<div class="tl-summary">' + R.esc(t.summary) + '</div>' : ''}
            ${t.changeRef ? '<div class="tl-changeref">via <a href="#" class="xref" data-id="' + R.esc(t.changeRef) + '">' + R.esc(t.changeRef) + '</a></div>' : ''}
          </div>
        </div>`;
      }).join('');
    }

    track.innerHTML = html;
    track.querySelectorAll('.xref[data-id]').forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault(); window.RulesNav.showTab('search'); R.showDetail(a.dataset.id);
    }));
  }

  function populateSelect() {
    const sel = document.getElementById('timeline-standard-select');
    if (!sel || sel._populated) return;
    sel._populated = true;
    const withEvents = new Set(DB.getTimeline().map((t) => t.standardId));
    const standards = DB.getAllStandards()
      .filter((s) => withEvents.has(s.meta.id))
      .slice().sort((a, b) => (a.meta.abbreviation || a.meta.title).localeCompare(b.meta.abbreviation || b.meta.title));
    sel.innerHTML = '<option value="">All standards (' + DB.getTimeline().length + ' events)</option>' +
      standards.map((s) => `<option value="${R.esc(s.meta.id)}">${R.esc(s.meta.abbreviation || s.meta.title)}</option>`).join('');
    sel.addEventListener('change', () => render(sel.value));
  }

  function init() {
    populateSelect();
    const sel = document.getElementById('timeline-standard-select');
    render(sel ? sel.value : '');
  }

  return { init, render };
})();
