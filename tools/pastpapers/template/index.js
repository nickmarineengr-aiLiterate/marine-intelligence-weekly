/* MIW Past Papers - index page behaviour.
   ROWS is emitted immediately above this script by build_index.py: one row per
   question across every paper, each carrying a pre-built search blob. That is
   what makes "search every question without knowing which paper" work.

   Bookmarks and progress are read from the same localStorage keys the paper page
   writes, so "My bookmarks" here reflects what was starred there. */
(function () {
  'use strict';

  var LS_BM = '__LS_BOOKMARKS__';
  var LS_PR = '__LS_PROGRESS__';

  function load(key) {
    try {
      var raw = window.localStorage.getItem(key);
      if (!raw) return {};
      var v = JSON.parse(raw);
      return (v && typeof v === 'object' && !Array.isArray(v)) ? v : {};
    } catch (e) { return {}; }
  }

  var bookmarks = load(LS_BM);
  var progress = load(LS_PR);

  var input = document.getElementById('q-search');
  var clearBtn = document.getElementById('q-clear');
  var results = document.getElementById('idx-results');
  var empty = document.getElementById('idx-empty');
  var hint = document.getElementById('idx-hint');
  var count = document.getElementById('idx-count');
  var papers = Array.prototype.slice.call(document.querySelectorAll('.paper-card'));
  var btns = Array.prototype.slice.call(document.querySelectorAll('.filter-btn[data-f]'));
  var filter = 'all';

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function passes(r) {
    if (filter === 'all') return true;
    if (filter === 'bookmarked') return !!bookmarks[r.qid];
    if (filter === 'unstudied') return progress[r.qid] !== 'studied';
    if (filter.indexOf('y:') === 0) return String(r.y) === filter.slice(2);
    if (filter.indexOf('s:') === 0) {
      return r.sub.join(' ').toLowerCase().indexOf(filter.slice(2)) !== -1;
    }
    return true;
  }

  function render() {
    var q = (input && input.value ? input.value : '').toLowerCase().trim();
    var terms = q ? q.split(/\s+/) : [];
    var searching = terms.length > 0 || filter !== 'all';

    var hits = ROWS.filter(function (r) {
      if (!passes(r)) return false;
      return terms.every(function (t) { return r.s.indexOf(t) !== -1; });
    });

    // paper cards follow the same filter so the two halves agree
    papers.forEach(function (card) {
      var pid = card.getAttribute('data-paper');
      var any = hits.some(function (r) { return r.p === pid; });
      card.hidden = searching && !any;
    });

    if (!searching) {
      results.innerHTML = '';
      if (hint) hint.hidden = false;
      if (empty) empty.style.display = 'none';
      if (count) {
        var saved = Object.keys(bookmarks).length;
        count.textContent = ROWS.length + ' questions' + (saved ? ' · ' + saved + ' bookmarked' : '');
      }
      return;
    }
    if (hint) hint.hidden = true;

    var html = hits.map(function (r) {
      var marks = [];
      if (bookmarks[r.qid]) marks.push('<span class="q-tag rec">&#9733; bookmarked</span>');
      if (progress[r.qid] === 'studied') marks.push('<span class="q-tag">&#10003; studied</span>');
      if (!r.built) marks.push('<span class="q-tag sub">answer not built</span>');
      return '<div class="hit">' +
        '<div class="hit-top">' + esc(r.my) + ' &middot; ' + esc(r.n) + ' &middot; ' + r.mk + ' marks</div>' +
        '<div class="hit-title"><a href="' + esc(r.u) + '">' + esc(r.t) + '</a></div>' +
        '<div class="hit-stem">' + esc(r.st) + '&hellip;</div>' +
        (marks.length ? '<div class="pc-topics" style="margin-top:6px;">' + marks.join('') + '</div>' : '') +
        '</div>';
    }).join('');

    results.innerHTML = html;
    if (empty) empty.style.display = hits.length ? 'none' : 'block';
    if (count) count.textContent = 'Showing ' + hits.length + ' of ' + ROWS.length + ' questions';
  }

  if (input) input.addEventListener('input', render);
  if (clearBtn) clearBtn.addEventListener('click', function () {
    if (input) { input.value = ''; input.focus(); }
    render();
  });
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      filter = b.getAttribute('data-f');
      btns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      render();
    });
  });

  render();
})();
