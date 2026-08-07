/* MIW Past Papers - paper page behaviour.
   Plain ES5-compatible DOM code. No framework, no dependencies, no network.

   Design notes:
   - Search reads data-search (generated from the spec), never innerText, so it
     matches while cards are collapsed and can match metadata that is never shown.
   - Bookmarks and progress are keyed by stable question_id (EM2607-Q1), never by
     DOM order, so future papers and reordering cannot corrupt saved state.
   - If localStorage is unavailable (private mode, disabled storage), every read
     returns empty and every write is a no-op; the page still works.
*/
(function () {
  'use strict';

  var LS_BM = '__LS_BOOKMARKS__';
  var LS_PR = '__LS_PROGRESS__';

  // ---- storage, defensively ------------------------------------------------
  function storageOK() {
    try {
      var k = '__miw_t__';
      window.localStorage.setItem(k, '1');
      window.localStorage.removeItem(k);
      return true;
    } catch (e) { return false; }
  }
  var HAS_LS = storageOK();

  function load(key) {
    if (!HAS_LS) return {};
    try {
      var raw = window.localStorage.getItem(key);
      if (!raw) return {};
      var v = JSON.parse(raw);
      return (v && typeof v === 'object' && !Array.isArray(v)) ? v : {};
    } catch (e) { return {}; }
  }
  function save(key, obj) {
    if (!HAS_LS) return;
    try { window.localStorage.setItem(key, JSON.stringify(obj)); } catch (e) { /* quota */ }
  }

  var bookmarks = load(LS_BM);
  var progress = load(LS_PR);

  // ---- elements ------------------------------------------------------------
  var cards = Array.prototype.slice.call(document.querySelectorAll('.q-card[data-qid]'));
  var input = document.getElementById('search-input');
  var clearBtn = document.getElementById('search-clear');
  var countLabel = document.getElementById('count-label');
  var noResults = document.getElementById('no-results');
  var filterBtns = Array.prototype.slice.call(document.querySelectorAll('.filter-btn[data-filter]'));
  var activeFilter = 'all';

  // ---- card open/close -----------------------------------------------------
  function setOpen(card, open) {
    card.classList.toggle('open', open);
    var btn = card.querySelector('.q-toggle');
    if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    var body = card.querySelector('.q-body');
    if (body) body.hidden = !open;
  }

  cards.forEach(function (card) {
    var btn = card.querySelector('.q-toggle');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var open = !card.classList.contains('open');
      setOpen(card, open);
      if (open && history.replaceState) {
        history.replaceState(null, '', '#' + card.id);
      }
    });
  });

  // ---- bookmark / studied --------------------------------------------------
  function paint(card) {
    var qid = card.getAttribute('data-qid');
    var bm = !!bookmarks[qid];
    var st = progress[qid] === 'studied';
    var b = card.querySelector('.icon-btn.bm');
    var s = card.querySelector('.icon-btn.st');
    if (b) {
      b.setAttribute('aria-pressed', bm ? 'true' : 'false');
      b.setAttribute('aria-label', (bm ? 'Remove bookmark from ' : 'Bookmark ') + qid);
      b.title = bm ? 'Bookmarked - click to remove' : 'Bookmark this question';
    }
    if (s) {
      s.setAttribute('aria-pressed', st ? 'true' : 'false');
      s.setAttribute('aria-label', (st ? 'Mark ' + qid + ' as not studied' : 'Mark ' + qid + ' as studied'));
      s.title = st ? 'Studied - click to clear' : 'Mark as studied';
    }
    card.setAttribute('data-bm', bm ? '1' : '0');
    card.setAttribute('data-st', st ? 'studied' : 'new');
  }

  cards.forEach(function (card) {
    var qid = card.getAttribute('data-qid');
    var b = card.querySelector('.icon-btn.bm');
    var s = card.querySelector('.icon-btn.st');
    if (b) b.addEventListener('click', function (ev) {
      ev.stopPropagation();
      if (bookmarks[qid]) { delete bookmarks[qid]; } else { bookmarks[qid] = 1; }
      save(LS_BM, bookmarks); paint(card); applyFilters();
    });
    if (s) s.addEventListener('click', function (ev) {
      ev.stopPropagation();
      if (progress[qid] === 'studied') { delete progress[qid]; } else { progress[qid] = 'studied'; }
      save(LS_PR, progress); paint(card); applyFilters();
    });
    paint(card);
  });

  var resetBtn = document.getElementById('reset-progress');
  if (resetBtn) resetBtn.addEventListener('click', function () {
    if (!window.confirm('Clear all bookmarks and studied marks for every paper on this device?')) return;
    bookmarks = {}; progress = {};
    save(LS_BM, bookmarks); save(LS_PR, progress);
    cards.forEach(paint); applyFilters();
  });

  // ---- filters + search ----------------------------------------------------
  function matchesFilter(card) {
    if (activeFilter === 'all') return true;
    if (activeFilter === 'bookmarked') return card.getAttribute('data-bm') === '1';
    if (activeFilter === 'unstudied') return card.getAttribute('data-st') !== 'studied';
    if (activeFilter === 'studied') return card.getAttribute('data-st') === 'studied';
    // subject tag filters
    return (card.getAttribute('data-subjects') || '').indexOf(activeFilter) !== -1;
  }

  function applyFilters() {
    var q = (input && input.value ? input.value : '').toLowerCase().trim();
    var terms = q ? q.split(/\s+/) : [];
    var vis = 0;
    cards.forEach(function (card) {
      var hay = card.getAttribute('data-search') || '';
      var hit = terms.every(function (t) { return hay.indexOf(t) !== -1; });
      var show = hit && matchesFilter(card);
      card.hidden = !show;
      if (show) vis++;
    });
    if (countLabel) {
      var saved = Object.keys(bookmarks).length;
      countLabel.textContent = 'Showing ' + vis + ' of ' + cards.length +
        (saved ? ' · ' + saved + ' bookmarked' : '');
    }
    if (noResults) noResults.style.display = vis === 0 ? 'block' : 'none';
    // keep the side index in step with what is actually visible
    document.querySelectorAll('.toc-link[data-qid]').forEach(function (a) {
      var c = document.querySelector('.q-card[data-qid="' + a.getAttribute('data-qid') + '"]');
      a.hidden = !!(c && c.hidden);
    });
  }

  if (input) input.addEventListener('input', applyFilters);
  if (clearBtn) clearBtn.addEventListener('click', function () {
    if (input) { input.value = ''; input.focus(); }
    applyFilters();
  });
  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      activeFilter = btn.getAttribute('data-filter');
      filterBtns.forEach(function (b) {
        b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
      });
      applyFilters();
    });
  });

  // ---- side index: active state while scrolling ----------------------------
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var id = e.target.id;
        document.querySelectorAll('.toc-link').forEach(function (a) {
          a.classList.toggle('active', a.getAttribute('href') === '#' + id);
        });
      });
    }, { rootMargin: '-100px 0px -60% 0px', threshold: 0 });
    cards.forEach(function (c) { if (c.id) obs.observe(c); });
  }

  // ---- deep links: #q4 opens Q4 -------------------------------------------
  function openFromHash() {
    var h = (window.location.hash || '').replace('#', '');
    if (!h) return;
    var card = document.getElementById(h);
    if (card && card.classList.contains('q-card')) {
      card.hidden = false;
      setOpen(card, true);
      card.scrollIntoView({ block: 'start' });
      var btn = card.querySelector('.q-toggle');
      if (btn) btn.focus({ preventScroll: true });
    }
  }
  window.addEventListener('hashchange', openFromHash);

  document.querySelectorAll('a[href^="#q"]').forEach(function (a) {
    a.addEventListener('click', function () {
      var card = document.getElementById(a.getAttribute('href').slice(1));
      if (card && card.classList.contains('q-card')) { card.hidden = false; setOpen(card, true); }
    });
  });

  // ---- init ----------------------------------------------------------------
  cards.forEach(function (c) { setOpen(c, false); });
  applyFilters();
  openFromHash();

  if (!HAS_LS) {
    var warn = document.getElementById('ls-warning');
    if (warn) warn.hidden = false;
  }
})();
