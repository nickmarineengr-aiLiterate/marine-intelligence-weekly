/* MIW Past Papers - paper page behaviour.
   Plain ES5-compatible DOM code. No framework, no dependencies, no network.

   Design notes:
   - Search reads data-search (generated from the spec), never innerText, so it
     matches while cards are collapsed and can match metadata that is never shown.
   - Bookmarks and progress are keyed by stable question_id (QP2607-Q1), never by
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

__STICKY_SYNC__

__LS_MIGRATE__

  var bookmarks = load(LS_BM);
  var progress = load(LS_PR);

  // Study state saved before the QP rename is carried forward, not discarded.
  if (migrateLegacyKeys(bookmarks)) save(LS_BM, bookmarks);
  if (migrateLegacyKeys(progress)) save(LS_PR, progress);

  // ---- elements ------------------------------------------------------------
  var cards = Array.prototype.slice.call(document.querySelectorAll('.q-card[data-qid]'));
  var input = document.getElementById('search-input');
  var clearBtn = document.getElementById('search-clear');
  var countLabel = document.getElementById('count-label');
  var noResults = document.getElementById('no-results');
  var filterBtns = Array.prototype.slice.call(document.querySelectorAll('.filter-btn[data-filter]'));
  var activeFilter = 'all';

  // ---- corpus search (the escape hatch out of this one paper) --------------
__CORPUS_SEARCH__

  var mcWrap = document.getElementById('mc-wrap');
  var mcSum = document.getElementById('mc-sum');
  var mcNote = document.getElementById('mc-note');
  var mcRes = document.getElementById('mc-res');
  var mcOffer = document.getElementById('mc-offer');
  var mcOfferBtn = document.getElementById('mc-offer-btn');
  // This paper's own id, so corpus results never repeat what is already on
  // screen. Read from the body's data attribute rather than parsed out of the
  // URL: a renamed file would silently stop excluding itself.
  var THIS_PAPER = document.body.getAttribute('data-paper-id') || '';
  var mcShown = '';   // the query whose corpus results are currently rendered

  function mcHide() {
    if (mcWrap) mcWrap.hidden = true;
    if (mcOffer) mcOffer.hidden = true;
    mcShown = '';
  }

  // Render corpus hits for `q`, excluding this paper. `reason` distinguishes
  // the two ways a reader gets here, because the wording is not the same:
  // 'empty'  -- nothing matched locally, we broadened for them
  // 'chose'  -- they had local results and asked for more anyway
  function mcRender(q, reason) {
    if (!mcWrap || !mcRes) return;
    if (mcShown === q + '|' + reason) return;      // idempotent per keystroke
    MIWCorpus.load().then(function (idx) {
      if (!idx) { mcHide(); return; }
      // The query may have moved on while the payload was in flight.
      if (input && input.value.trim() !== q) return;
      var res = MIWCorpus.match(q, { excludePaper: THIS_PAPER });
      if (!res.questions) {
        // Genuinely nothing anywhere. Leave the local dead-end message
        // standing and say nothing more -- an empty broadened panel is worse
        // than no panel.
        mcWrap.hidden = true;
        if (mcOffer) mcOffer.hidden = true;
        mcShown = q + '|' + reason;
        return;
      }
      // We found the reader an answer, so the local "no question matches that
      // search" line is now actively wrong -- it sits directly above a panel
      // listing real matches. Retract it.
      if (reason === 'empty' && noResults) noResults.style.display = 'none';
      mcSum.innerHTML = MIWCorpus.summary(res);
      mcNote.textContent = reason === 'empty'
        ? 'Nothing in this paper — these are from other sittings.'
        : 'Also covered in other sittings.';
      mcRes.innerHTML = MIWCorpus.renderGroups(res);
      mcWrap.hidden = false;
      if (mcOffer) mcOffer.hidden = true;
      mcShown = q + '|' + reason;
    });
  }

  // Called after every local filter pass. `vis` is what the reader can see.
  function mcUpdate(q, vis) {
    if (!mcWrap) return;                       // review build: no corpus panel
    if (!q) { mcHide(); if (noResults) noResults.removeAttribute('data-corpus'); return; }
    if (vis === 0) {
      // Stuck. Broaden without being asked -- a dead end is not a result.
      if (mcOffer) mcOffer.hidden = true;
      mcRender(q, 'empty');
    } else {
      // They have results. Offer more rather than pushing a second list at
      // them, and do not fetch 800KB until they actually want it.
      mcWrap.hidden = true;
      mcShown = '';
      if (mcOffer && mcOfferBtn) {
        mcOfferBtn.textContent = 'Search all solved papers for “' + q + '”';
        mcOffer.hidden = false;
      }
    }
  }

  if (mcOfferBtn) mcOfferBtn.addEventListener('click', function () {
    var q = (input && input.value ? input.value : '').trim();
    if (q) mcRender(q, 'chose');
  });

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
    mcUpdate(q, vis);
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

  // ---- learner modes -------------------------------------------------------
  // The sections are rendered UNHIDDEN. Hiding only happens here, so if this
  // script never runs the whole card still reads top to bottom and the model
  // answer is reachable. The learning layer must never be able to hide the answer.
  function showMode(card, mode) {
    Array.prototype.forEach.call(card.querySelectorAll('.mode'), function (m) {
      m.hidden = m.getAttribute('data-mode') !== mode;
    });
    Array.prototype.forEach.call(card.querySelectorAll('.learn-btn'), function (b) {
      b.setAttribute('aria-selected', b.getAttribute('data-mode') === mode ? 'true' : 'false');
    });
  }

  cards.forEach(function (card) {
    var bar = card.querySelector('.learn-bar');
    if (!bar) return;
    showMode(card, 'answer');
    Array.prototype.forEach.call(card.querySelectorAll('.learn-btn'), function (b) {
      b.addEventListener('click', function () {
        showMode(card, b.getAttribute('data-mode'));
      });
    });
  });

  // ---- knowledge map: branches hidden so the map can be used as recall ------
  Array.prototype.forEach.call(document.querySelectorAll('.kmap-toggle'), function (btn) {
    btn.addEventListener('click', function () {
      var map = btn.closest('.kmap');
      var hidden = map.classList.toggle('branches-hidden');
      btn.setAttribute('aria-pressed', hidden ? 'true' : 'false');
      btn.textContent = hidden ? 'Show branches' : 'Hide branches';
    });
  });

  // ---- blank skeleton recall ----------------------------------------------
  Array.prototype.forEach.call(document.querySelectorAll('.recall-toggle'), function (btn) {
    btn.addEventListener('click', function () {
      var sec = btn.closest('.recall');
      var list = sec.querySelector('.recall-list');
      var show = list.getAttribute('data-state') === 'hidden';
      list.setAttribute('data-state', show ? 'shown' : 'hidden');
      Array.prototype.forEach.call(sec.querySelectorAll('.recall-answer'), function (a) {
        a.hidden = !show;
      });
      Array.prototype.forEach.call(sec.querySelectorAll('.recall-blank'), function (a) {
        a.hidden = show;
      });
      btn.setAttribute('aria-expanded', show ? 'true' : 'false');
      btn.textContent = show ? 'Hide the structure' : 'Reveal the structure';
    });
  });

  // ---- flashcards ----------------------------------------------------------
  Array.prototype.forEach.call(document.querySelectorAll('.card-q'), function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      var ans = document.getElementById(btn.getAttribute('aria-controls'));
      if (ans) ans.hidden = !open;
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
