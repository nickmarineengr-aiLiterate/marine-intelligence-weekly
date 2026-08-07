/* GENERATED from src/app.js by build_qso.py@1.0.0 -- do not edit. build d1de03ab7e86 */
/* Study Mode — Question Study Objects.
   Reads only window.QSO_DATA (generated). Renders no content of its own:
   every string shown is a generated label or a verbatim preview carrying its
   own source selector. No network request is ever made. */
(function () {
  'use strict';

  var DATA = window.QSO_DATA || { manifest: { questions: [] }, questions: {} };
  var STATE_KEY = 'miw.study.v1';
  var $ = function (id) { return document.getElementById(id); };

  /* ---- local state: namespaced by QSO id + state schema version -------- */
  var State = {
    all: function () {
      try { return JSON.parse(localStorage.getItem(STATE_KEY)) || {}; }
      catch (e) { return {}; }
    },
    get: function (id) {
      var s = this.all()[id];
      return { status: (s && s.status) || 'not-started', flagged: !!(s && s.flagged) };
    },
    set: function (id, patch) {
      var all = this.all();
      all[id] = Object.assign({ stateSchemaVersion: 1 }, all[id], patch);
      try { localStorage.setItem(STATE_KEY, JSON.stringify(all)); } catch (e) { /* quota */ }
    }
  };

  /* ---- appearance preferences ------------------------------------------
     Two independent dimensions, deliberately not one "theme": a reader who
     wants dark may still want the branch colours, and a reader who wants
     neutral branches may still read in daylight. Collapsing them would force
     a choice neither of them made.

     Presentation only. Nothing here touches the route, the open card, the
     Study Card face, scroll, focus or any QSO datum -- and the storage
     payload below is the proof, because it has room for nothing else.

     The whole feature rests on normalisePrefs(). Every consumer -- the root
     attributes, the CSS selectors, the radios' checked state, the value
     written back to storage -- is derived from its output, so if it can only
     emit controlled values, no malformed stored object can reach any of them.
     That makes "unknown fields do not survive" a property of the data flow
     rather than a rule each call site has to remember. */
  var PREFS_KEY = 'rulesapp.study.preferences.v1';
  var APPEARANCES = ['light', 'dark'];
  var COLOURS = ['multicolour', 'monochrome'];

  /* System preference is consulted only when the reader has never chosen.
     Read at resolve time rather than cached, but NOT subscribed to: once a
     choice is stored it is authoritative, and an OS change must not quietly
     overrule a decision the reader made on purpose. */
  function defaultAppearance() {
    try {
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
      }
    } catch (e) { /* matchMedia unavailable: light is the safe floor */ }
    return 'light';
  }

  /* Total function: every input shape -- null, a string, an array, a number,
     a partial object, an object carrying fields we never asked for -- maps to
     exactly two controlled keys. The input is never mutated and never
     consulted again, so an unknown field cannot be read back out later. */
  function normalisePrefs(raw) {
    var src = (raw && typeof raw === 'object' && !Array.isArray(raw)) ? raw : {};
    return {
      appearance: APPEARANCES.indexOf(src.appearance) >= 0 ? src.appearance : defaultAppearance(),
      colour: COLOURS.indexOf(src.colour) >= 0 ? src.colour : 'multicolour'
    };
  }

  /* Storage is treated as hostile: it may be absent, it may throw on access
     (Safari private mode, a file:// origin, a locked-down profile), and what
     it returns may be anything at all. None of those may stop the
     application starting, so every failure resolves to the defaults. */
  function readPrefs() {
    var raw = null;
    try {
      raw = window.localStorage ? window.localStorage.getItem(PREFS_KEY) : null;
    } catch (e) { return normalisePrefs(null); }        // getter threw
    if (typeof raw !== 'string') return normalisePrefs(null);
    var parsed;
    try { parsed = JSON.parse(raw); }
    catch (e) { return normalisePrefs(null); }           // malformed JSON
    return normalisePrefs(parsed);                       // primitive/array/object all handled
  }

  /* Writes the normalised pair and nothing else, so an unknown field that
     arrived in storage is dropped rather than echoed back. A failed write is
     swallowed: the reader's current selection is already applied to the page
     and must not be undone because persistence was unavailable. */
  function writePrefs(prefs) {
    var clean = normalisePrefs(prefs);
    try {
      if (window.localStorage) window.localStorage.setItem(PREFS_KEY, JSON.stringify(clean));
    } catch (e) { /* quota, security, or no storage: the page is still correct */ }
    return clean;
  }

  /* The document root carries the state. One canonical representation, read
     by the stylesheet and by tests alike; no per-card inline styles, nothing
     that depends on which route rendered. */
  function applyPrefs(prefs) {
    var clean = normalisePrefs(prefs);
    var root = document.documentElement;
    root.setAttribute('data-appearance', clean.appearance);
    root.setAttribute('data-colour', clean.colour);
    return clean;
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function show(view) {
    ['view-home', 'view-question', 'view-cards', 'view-map'].forEach(function (v) {
      $(v).hidden = (v !== view);
    });
  }

  /* ---- navigation primitives ------------------------------------------
     Read the motion preference at call time, not once at load: a reader who
     turns reduction on mid-session must be honoured without a reload. */
  function reducedMotion() {
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  var HIGHLIGHT_MS = 1600;
  var highlightTimer = null;

  /* Bring a destination into view, move focus to it, and mark it briefly so
     the eye can find where the jump landed. Focus is the accessible half of
     that pair and the highlight is the visual half; neither replaces the
     other. The timer is single-shot and shared, so rapid navigation never
     leaves two elements highlighted at once. */
  function land(el) {
    if (!el) return false;
    Array.prototype.forEach.call(document.querySelectorAll('.nav-target'), function (p) {
      p.classList.remove('nav-target');
    });
    if (highlightTimer) { clearTimeout(highlightTimer); highlightTimer = null; }

    el.scrollIntoView({ behavior: reducedMotion() ? 'auto' : 'smooth', block: 'start' });
    if (el.hasAttribute && !el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1');
    try { el.focus({ preventScroll: true }); } catch (e) { el.focus(); }

    el.classList.add('nav-target');
    highlightTimer = setTimeout(function () {
      el.classList.remove('nav-target');
      highlightTimer = null;
    }, HIGHLIGHT_MS);
    return true;
  }

  var KIND = {
    'answer-oral-delivery': 'Oral delivery', 'answer-answer-section': 'Answer section',
    'regulation': 'Regulation', 'answer-ce-tip': 'CE tip',
    'answer-ce-relevance': 'CE relevance', 'answer-trap-question': 'Trap question',
    'answer-common-failure': 'Common failure', 'answer-numbers': 'Numbers',
    'answer-casualty-link': 'Casualty link', 'answer-examiner-chain': 'Examiner chain',
    'answer-on-my-vessel': 'On my vessel', 'answer-deep-dive': 'Deep dive',
    'oral-note': 'Oral note', 'written-note': 'Written note', 'cheat-sheet': 'Cheat sheet',
    'related-question': 'Related question', 'manual': 'Manual', 'illustration': 'Illustration'
  };

  /* ---- home ------------------------------------------------------------ */
  function renderHome() {
    var q = ($('q-search').value || '').toLowerCase();
    var list = DATA.manifest.questions.filter(function (x) {
      return !q || x.canonicalQuestion.toLowerCase().indexOf(q) >= 0 ||
             (x.focusedTopic || '').toLowerCase().indexOf(q) >= 0;
    });
    $('q-list').innerHTML = list.map(function (x) {
      return '<li><a href="#/q/' + esc(x.id) + '"><span>' + esc(x.canonicalQuestion) + '</span>' +
        '<span class="meta">' + x.confirmedRecurrence + '× confirmed · ' +
        x.cards + ' cards</span></a></li>';
    }).join('') || '<li><span class="muted">No question matches.</span></li>';
    $('home-note').textContent = DATA.manifest.questions.length + ' question(s) built ' +
      (DATA.manifest.builtAt || '') + '.';
  }

  /* ---- cards -----------------------------------------------------------
     Every card is an accordion: a real <button> header controlling a panel.
     The card's identity is its generated sectionId -- a stable editorial slug
     derived from the curated answer's own heading, not its position in an
     array. Reordering or inserting a section therefore cannot repoint a
     bookmarked card route.

     Ids are PREFIXED (cb-/cp-) rather than used bare. Two sectionIds begin
     with a digit ('15-second-answer'); a leading digit is a valid DOM id but
     an INVALID CSS selector -- exactly the id="3" defect Milestone 2 found
     live. The prefix makes every id selector-safe by construction.

     The panel carries no role="region": the ARIA practices advise against it
     past roughly six panels, and there are fourteen here. Landmark noise on
     that scale costs a screen-reader user more than it gives them. The
     button's aria-expanded/aria-controls pair is the contract that matters. */
  function cardBtnId(c) { return 'cb-' + c.sectionId; }
  function cardPanelId(c) { return 'cp-' + c.sectionId; }
  /* Face container ids follow the same prefix discipline for the same reason:
     two sectionIds begin with a digit, and a bare leading digit is a valid DOM
     id but an invalid CSS selector. */
  function cardFrontId(c) { return 'cff-' + c.sectionId; }
  function cardBackId(c) { return 'cfb-' + c.sectionId; }

  /* The branch a card sits under is the one piece of identity the accordion
     header does NOT already carry, so it is what the front face adds. Read
     from the generated map nodes -- no label is authored here. */
  function branchLabel(q, n) {
    var nd = q.map.nodes.filter(function (x) { return String(x.n) === String(n); })[0];
    return nd ? nd.label : '';
  }

  /* ---- resources (Resource Card only) ------------------------------------
     A citation and a target are not the same thing, and the card says so. The
     citation code and its description are the answer's own words and are shown
     whether or not anything can be opened -- a citation does not stop being
     true because RulesApp has not built the instrument. Availability is stated
     next to it rather than implied by the absence of a link.

     Every attribute below is decided by the BUILDER: linkKind is generated and
     validated there, so the renderer cannot invent a target, cannot promote a
     relative path to an external one, and cannot be talked into an unsafe
     scheme by the data. If linkKind is 'none' no anchor is emitted at all --
     never a disabled or dead one, which would read as "broken" rather than
     "not held". */
  var STATUS_TEXT = {
    'not-in-corpus': {
      flag: 'Not held',
      text: 'Full text is not held in the accepted RulesApp corpus.'
    },
    'no-single-target': {
      flag: 'No single document',
      text: 'This citation does not identify one specific source document.'
    },
    'accepted': {
      flag: 'In corpus',
      text: 'Held in the accepted RulesApp corpus.'
    }
  };
  /* The action names the thing being opened, so a reader knows where they are
     going before they go. "Open", "More" and "Click here" all describe the
     click rather than the destination. */
  var RESOURCE_ACTION = {
    'unified-requirement': 'Open Unified Requirement',
    'regulation': 'Open regulation',
    'class-rule': 'Open class rule',
    'administrative-arrangement': 'Open source'
  };

  function resourceLinkHTML(r) {
    if (r.linkKind === 'none' || !r.href) return '';
    var label = esc(RESOURCE_ACTION[r.resourceClass] || 'Open source');
    if (r.linkKind === 'external') {
      // The new-tab warning is part of the ACCESSIBLE NAME, not an icon. An
      // icon alone cannot be read out, and a reader who cannot see it would
      // lose their place in the app without being told why.
      return '<a class="cnav res-link" href="' + esc(r.href) +
        '" target="_blank" rel="noopener noreferrer">' + label +
        '<span class="sr-only"> — opens in a new tab</span></a>';
    }
    return '<a class="cnav res-link" href="' + esc(r.href) + '">' + label + '</a>';
  }

  function resourceHTML(r) {
    var st = STATUS_TEXT[r.corpusStatus] ||
             { flag: 'Unknown', text: 'Availability has not been reviewed.' };
    var meta = [r.resourceClassLabel, r.issuerName].filter(Boolean)
      .map(esc).join(' <span aria-hidden="true">&middot;</span> ');
    return '<li class="res" id="' + esc(r.resourceId) +
      '" data-status="' + esc(r.corpusStatus) + '">' +
      '<p class="res-code">' + esc(r.citationCode) + '</p>' +
      (meta ? '<p class="res-meta">' + meta + '</p>' : '') +
      '<p class="res-desc">' + esc(r.description) + '</p>' +
      '<p class="res-status"><span class="res-flag">' + esc(st.flag) + '</span> ' +
      esc(st.text) + '</p>' +
      '<p class="res-evidence">' + esc(r.evidence) + '</p>' +
      resourceLinkHTML(r) + '</li>';
  }

  function cardHTML(q, c) {
    var role = c.cardRole === 'resource' ? 'Resource' : 'Study';
    // The accessible name comes from the button's own contents, so the visible
    // label is always contained in it (WCAG 2.5.3). No aria-label override.
    /* The single spaces between the spans are deliberate. The accessible name
       is computed from the button's contents, and whether a UA inserts a
       separator between adjacent inline boxes depends on how it blockifies
       flex items -- reading the live tree gave
       "Answer sectionDeformations and BucklingStudy", run together. Explicit
       whitespace makes the name correct without depending on that. It costs
       nothing visually: a flex container does not render whitespace-only
       anonymous items.

       The card sits in an <h3> so screen-reader users get a navigable list of
       cards rather than fourteen unlabelled buttons in a flat run. */
    var head = '<h3 class="card-h"><button type="button" class="card-btn" ' +
      'id="' + cardBtnId(c) + '" aria-expanded="false" aria-controls="' + cardPanelId(c) + '">' +
      '<span class="kind">' + esc(KIND[c.type] || c.type) + '</span> ' +
      '<span class="card-title">' + esc(c.title) + '</span> ' +
      '<span class="card-role">' + role + '</span>' +
      '<span class="card-chev" aria-hidden="true"></span></button></h3>';

    /* A reviewed resource list supersedes the flat citation list AND the
       preview. On this card the preview is only the citation codes joined by
       semicolons, so keeping it would print every code twice -- once as noise
       above the list that states it properly. The preview is suppressed only
       where a resource list replaces it; every other card keeps its verbatim
       extract untouched. */
    var hasResources = !!(c.resources && c.resources.length);
    var body = (c.preview && !hasResources) ? '<div class="extract">' + esc(c.preview) + '</div>' : '';

    if (hasResources) {
      body += '<ul class="res-list">' + c.resources.map(resourceHTML).join('') + '</ul>';
    } else if (c.citations) {
      body += '<div class="extract">' + c.citations.map(function (r) {
        return '<div><strong>' + esc(r.code) + '</strong> — ' + esc(r.description) + '</div>';
      }).join('') + '</div>';
    }
    if (c.pairs) {
      body += c.pairs.map(function (p) {
        return '<div class="extract"><em>' + esc(p.question) + '</em><br>' + esc(p.answer) + '</div>';
      }).join('');
    }

    /* The CSS selector the extractor used is build provenance, not something a
       candidate can act on -- it names a div in someone else's HTML. It stays
       in the generated provenance, where it is auditable, and is dropped from
       the face of the card that now states its sources properly. Every other
       card is untouched: harmonising the whole set is a Milestone 7 question,
       and changing a Study Card's foot here would be an unreviewed edit to
       work that is already verified.

       The QB answer link is a REPOSITORY-SOURCE link, not an external one: a
       relative path that resolves inside the deployed site and works offline.
       It gets no target and no rel, because both would be wrong -- and it is
       named for what it opens rather than the generic "Open source". */
    /* Every card's foot names the same thing the same way, decided at
       Milestone 7 after seeing the two side by side.

       Both links point at ONE target -- the curated answer at QB3_B.html#q2 --
       so two labels for one destination was an inconsistency rather than a
       distinction, and "Open source answer" says what actually opens.

       The extractor's CSS selector is gone from every card, not just the
       Resource Card. It named a tag in someone else's HTML, a candidate could
       not act on it, and it did not even discriminate -- almost every section
       is an h4 or an h5. Milestone 5 reached that judgement for one card and
       scoped the change to avoid editing verified work; the reasoning was
       never card-specific. It remains in the generated JSON as
       `sourceSelector` and `provenance.selector`, which is where an auditor
       checks provenance and where the tests read it.

       The source PATH stays: `meoclass1/QB3_B.html` tells a candidate which
       Question Bank file the answer came from, which is provenance they can
       actually use, and it is relative rather than an absolute local path. */
    var foot = [];
    if (c.provenance && c.provenance.sourcePath) foot.push(esc(c.provenance.sourcePath));
    if (c.href) foot.push('<a href="' + esc(c.href) + '">Open source answer &rarr;</a>');

    /* data-face is the panel's readable state. Resource cards never carry it --
       they do not flip, ever -- so the attribute's presence is also the test
       for "is this card allowed a face at all". */
    var face = c.cardRole === 'resource' ? '' : ' data-face="front"';

    var answer = '<div class="card-body">' + body +
      '<div class="card-foot">' + foot.join('<span>&middot;</span>') + '</div></div>';

    /* Study Cards get two faces; a Resource Card gets the answer directly, with
       no face containers, no reveal control and nothing to reset. Previous,
       Next and Return to Map sit OUTSIDE both faces in the one shared nav row,
       so they are present in either state without being duplicated -- one set
       of controls, one set of ids, nothing stale left in a hidden face.

       The whole answer -- extract, citations, pairs AND the provenance foot --
       lives on the back. The foot is not decoration: it holds the only link in
       the card body, and a focusable control inside a hidden face is exactly
       what must not exist. Putting it on the back keeps that true by
       construction rather than by a rule someone has to remember. */
    var inner = c.cardRole === 'resource' ? answer : (
      '<div class="card-face card-front" id="' + cardFrontId(c) + '">' +
        '<p class="face-context">Branch ' + c.n + ' &middot; ' +
          esc(branchLabel(q, c.n)) + '</p>' +
        /* One prompt template for every Study Card, parameterised only by the
           card's own generated title. No per-type prose and no authored
           engineering content: the QSO has no recall-prompt field, and adding
           one to make a better flashcard would be writing knowledge into the
           application instead of citing it. */
        '<p class="face-prompt">Recall <strong>' + esc(c.title) +
          '</strong> from memory, then show the answer to check yourself.</p>' +
        faceBtnHTML('back', 'Show answer', cardBackId(c)) +
      '</div>' +
      /* The return control comes FIRST on the back and the reveal control LAST
         on the front. That is not symmetry for its own sake: a "proceed"
         affordance belongs after the prompt it acts on, a "return" affordance
         belongs at the start of what it leaves. It also happens to put the two
         buttons within a line or so of each other, so a face switch moves
         focus without moving the page. */
      '<div class="card-face card-back" id="' + cardBackId(c) + '" hidden>' +
        faceBtnHTML('front', 'Show question', cardFrontId(c)) + answer +
      '</div>'
    );

    var panel = '<div class="card-panel" id="' + cardPanelId(c) + '"' + face + ' hidden>' +
      inner + cardNavHTML(q, c) + '</div>';

    return '<article class="card cat-' + esc(c.category || 'resource') +
      '" data-card="' + esc(c.sectionId) + '" data-branch="' + c.n +
      '" data-role="' + (c.cardRole === 'resource' ? 'resource' : 'study') + '">' +
      head + panel + '</article>';
  }

  /* Previous / Next / Return to Map, rendered inside every panel so the
     controls travel with the card the reader is actually in.

     Previous and Next are BUTTONS, not links, because the boundary state is
     `disabled` and there is no honest disabled state for an anchor -- an
     aria-disabled link still navigates. Return to Map is a link, because it
     goes somewhere and the browser should own that history entry.

     Boundaries are computed from the branch's own card list, so navigation
     cannot cross a branch: the first card has no Previous and the last has no
     Next, and neither silently continues into the neighbouring section. */
  function branchCards(q, n) {
    return q.cards.filter(function (c) { return String(c.n) === String(n); });
  }

  /* The reveal pair. Real <button> elements, never a clickable div, so Enter
     and Space activate them natively and nothing here has to reimplement that.

     The label IS the accessible name -- computed from the button's own
     contents, with no aria-label override -- so the two can never drift apart.
     "Show answer" / "Show question" is one consistent pair naming the actual
     result; "Flip" and "Turn" name a motion instead, which is exactly what a
     candidate cannot act on.

     Thirteen Study Cards produce thirteen identically named pairs, but at most
     one panel is un-hidden at a time and a hidden panel is out of the
     accessibility tree, so exactly one of each is ever present to be confused.

     They reuse .cnav for styling: the 2.75rem touch target and the focus ring
     are already correct there, and a second set of button rules would drift.
     They are NOT in the .card-nav row -- they change a face, not a location. */
  function faceBtnHTML(to, label, controls) {
    return '<button type="button" class="cnav cnav-face" data-face-to="' + to +
      '" aria-controls="' + controls + '">' + label + '</button>';
  }

  function cardNavHTML(q, c) {
    var sibs = branchCards(q, c.n), i = -1, k;
    for (k = 0; k < sibs.length; k++) if (sibs[k].sectionId === c.sectionId) i = k;
    var prev = i > 0 ? sibs[i - 1] : null;
    var next = (i >= 0 && i < sibs.length - 1) ? sibs[i + 1] : null;

    function btn(dir, label, target) {
      return '<button type="button" class="cnav cnav-' + dir + '"' +
        (target ? ' data-go="' + esc(target.sectionId) + '"' : ' disabled') +
        '>' + label + '</button>';
    }

    return '<div class="card-nav">' +
      btn('prev', '&larr; Previous', prev) +
      btn('next', 'Next &rarr;', next) +
      '<a class="cnav cnav-map" href="#/q/' + esc(q.id) + '/map/' + c.n +
      '" aria-label="Return to branch ' + c.n + ' on the Knowledge Map">Return to Map</a>' +
      '</div>';
  }

  function gapHTML(g) {
    return '<div class="card gap"><div class="card-top"><span class="kind">Gap</span>' +
      '<span class="card-title">No ' + esc(g.kind.replace('-', ' ')) + ' available</span></div>' +
      '<div class="extract">' + esc(g.reason) + '</div>' +
      (g.futureSource ? '<div class="card-foot">Future: ' + esc(g.futureSource) + '</div>' : '') +
      '</div>';
  }

  function renderCards(q) {
    var byBranch = {};
    q.cards.forEach(function (c) { (byBranch[c.n] = byBranch[c.n] || []).push(c); });

    // The branch number is the return path to the map, so it is a real link,
    // not a decorative badge: it works with the keyboard, with middle-click,
    // and with Back, because the browser owns hash history. The gaps section
    // below keeps a plain span -- it has no map node, and pretending it did
    // would be a dead control.
    var html = q.map.nodes.map(function (node) {
      // id="branch-3", never id="3": a bare number is a valid DOM id but an
      // INVALID CSS selector (#3), so any future rule or querySelector aimed
      // at a branch would fail in a way getElementById never reveals.
      return '<section class="branch cat-' + esc(node.category) +
        (node.emphasis === 'secondary' ? ' secondary' : '') + '" id="branch-' + node.n +
        '" tabindex="-1">' +
        '<div class="branch-h"><a class="bnum" href="#/q/' + esc(q.id) + '/map/' + node.n +
        '" aria-label="Show branch ' + node.n + ', ' + esc(node.label) +
        ', on the Knowledge Map">' + node.n + '</a><h2>' +
        esc(node.label) + '</h2></div>' +
        (byBranch[node.n] || []).map(function (c) { return cardHTML(q, c); }).join('') +
        '</section>';
    }).join('');

    if (q.declaredGaps.length) {
      html += '<section class="branch" id="gaps"><div class="branch-h">' +
        '<span class="bnum">—</span><h2>Declared source gaps</h2></div>' +
        q.declaredGaps.map(gapHTML).join('') + '</section>';
    }
    $('cards-root').innerHTML = html;

    var st = State.get(q.id);
    $('status-select').value = st.status;
    $('flag-revision').checked = st.flagged;

    var primary = q.answers.filter(function (a) { return a.role === 'primary'; })[0];
    $('side-answer').innerHTML = primary
      ? '<a href="' + esc(primary.href) + '">' + esc(primary.file) + '#' + esc(primary.anchor) + '</a>' +
        '<div class="muted">' + esc(primary.answerVersion || '') + '</div>' +
        (q.answers.length > 1 ? '<div class="muted">' + (q.answers.length - 1) + ' parallel answer(s)</div>' : '')
      : '<span class="muted">None.</span>';

    var cheat = q.cards.filter(function (c) { return c.type === 'cheat-sheet'; });
    $('side-cheat').innerHTML = cheat.length
      ? cheat.map(function (c) { return '<a href="' + esc(c.href) + '">' + esc(c.title) + '</a>'; }).join('<br>')
      : '<span class="muted">None — declared as a gap.</span>';

    // Workbook and examiner-index evidence are shown as SEPARATE streams.
    var r = q.recurrence, ev = q.evidence;
    $('side-exam').innerHTML =
      '<div><strong>Workbook</strong> — ' + r.confirmed + ' confirmed, ' + r.possible + ' possible</div>' +
      ev.workbook.occurrences.map(function (o) {
        return '<div>· ' + esc(o.examiner) + ' <span class="muted">(' + esc(o.matchTier) + ')</span></div>';
      }).join('') +
      '<div style="margin-top:.4rem"><strong>Examiner index</strong> — ' +
        (ev.examinerIndex.questionRefs || []).length + ' ref(s)</div>' +
      '<div class="muted" style="margin-top:.3rem">Streams are separate and not reconciled.</div>';

    $('side-prov').innerHTML =
      'Built ' + esc(q.build.builtAt) + '<br>' + esc(q.build.generator) +
      '<br>Answer ' + esc(q.build.answerVersion || 'unversioned') +
      '<br>Review: ' + esc(q.review.state) +
      '<br>' + q.counts.citations + ' citation(s) · ' + q.counts.withheldAssociations + ' withheld';
  }

  /* ---- accordion ---------------------------------------------------------
     The URL is the open-card state. There is no module variable holding "the
     open card" and nothing is written to localStorage: the route names at most
     one card, so "at most one card open" is structural rather than something
     the code has to keep remembering to enforce. A render pass always closes
     everything first and then opens the one the route names, so even a bug
     that opened two cards would be corrected by the next route.

     Nothing here writes to history. Only a deliberate user action -- pressing
     a header, Previous, Next, or Return to Map -- assigns location.hash, so
     render-time normalisation can never manufacture a duplicate history entry
     the reader then has to press Back through. */
  function cardsRoot() { return $('cards-root'); }

  /* ---- card face ---------------------------------------------------------
     The ONE writer of card-face state. Everything that can change a face goes
     through here, so `data-face` and the two `hidden` attributes cannot
     disagree -- a face that says "front" while the back is on screen would
     hand the reader the answer they were about to recall.

     Face state is deliberately EPHEMERAL: not in the route, not in
     localStorage, not in the QSO schema. It does not need to be, and the
     reason is structural rather than a promise. Every route pass runs
     applyCardState(), which closes every card, and closing resets the face. So
     a direct card URL, a reload, Back, Forward, Previous, Next and Map ->
     Cards all arrive on the front by construction. Adding a /back segment
     would buy nothing and would make a bookmarked answer outlive the recall
     step it exists to protect. */
  function showFace(panel, face) {
    if (!panel || !panel.hasAttribute('data-face')) return null;   // resource card
    panel.setAttribute('data-face', face);
    var front = panel.querySelector('.card-front');
    var back = panel.querySelector('.card-back');
    // `hidden` and not a class: an inactive face must leave the accessibility
    // tree and the find-in-page text, not merely stop being visible. Its
    // buttons and its "Open source" link go with it, so nothing focusable is
    // ever stranded in a face the reader cannot see.
    if (front) front.hidden = (face !== 'front');
    if (back) back.hidden = (face !== 'back');
    return face === 'back' ? back : front;
  }

  function closeCard(article) {
    var btn = article.querySelector('.card-btn');
    var panel = article.querySelector('.card-panel');
    if (btn) btn.setAttribute('aria-expanded', 'false');
    if (panel) {
      panel.hidden = true;
      // Return the card to its front face, so a closed card is never left
      // showing a back face it would silently reopen on. This is also what
      // makes every route boundary a reset: applyCardState() closes every
      // card on every pass.
      showFace(panel, 'front');
    }
    article.classList.remove('open');
  }

  function openCard(article) {
    var btn = article.querySelector('.card-btn');
    var panel = article.querySelector('.card-panel');
    if (btn) btn.setAttribute('aria-expanded', 'true');
    if (panel) panel.hidden = false;
    article.classList.add('open');
  }

  /* Close every card, then open the one the route names. Returns the opened
     article, or null -- a route naming a card this question does not have
     falls back to the branch view with nothing open rather than fabricating
     a destination, exactly as an unknown branch already does. */
  function applyCardState(cardId) {
    var opened = null;
    Array.prototype.forEach.call(cardsRoot().querySelectorAll('.card'), function (a) {
      if (cardId && a.dataset.card === cardId) { openCard(a); opened = a; }
      else closeCard(a);
    });
    return opened;
  }

  /* Leaving the Cards view closes whatever was open. Found live: after
     Return to Map the card stayed aria-expanded with a visible panel inside
     the now-hidden view. Nothing was user-visible and the next Cards route
     corrected it, but the design claim is that the DOM always matches the URL,
     and a route with no card in it must not leave one open behind the scenes.
     Milestone 4's face state would inherit that staleness. */
  function closeAllCards() {
    if (cardsShowing === null) return;
    Array.prototype.forEach.call(cardsRoot().querySelectorAll('.card'), closeCard);
  }

  /* A card route is honoured only when the card really does belong to the
     branch the URL names. Found live: #/cards/99/ce-relevance opened a real
     card under a branch that does not exist, and #/cards/3/ce-relevance would
     have opened it under the wrong one -- in both cases the card's Previous
     and Next came from its true branch while the URL claimed another, which
     is precisely the fabricated relationship an unknown branch is supposed to
     never produce. A mismatched pair now falls back to the branch view with
     nothing open. */
  function resolveCard(q, branch, cardId) {
    if (!cardId) return null;
    var ok = q.cards.some(function (c) {
      return c.sectionId === cardId && String(c.n) === String(branch);
    });
    return ok ? cardId : null;
  }

  /* Scroll only when the destination is not already adequately visible, and
     never above the sticky header. Instant when motion is reduced. */
  var STICKY_TOP = 70;
  function inView(el) {
    var r = el.getBoundingClientRect();
    return r.top >= STICKY_TOP && r.top <= (window.innerHeight || document.documentElement.clientHeight);
  }
  function bringIntoView(el) {
    if (!el || inView(el)) return;
    el.scrollIntoView({ behavior: reducedMotion() ? 'auto' : 'smooth', block: 'start' });
  }

  /* One focus rule, applied everywhere: move focus to the destination unless
     it is already there.

     That single guard covers every case correctly. Pressing a card header
     already focused it, so opening or closing by click causes no jump. Going
     via Previous or Next leaves focus on a control that is about to be
     hidden, so focus moves. Arriving from a direct URL, a reload, Back or
     Forward moves focus, because otherwise it is stranded outside the card
     the URL is about. And because the rule is idempotent, re-running a route
     can never focus in a loop. */
  function focusTarget(el, scrollEl) {
    if (!el) return false;
    if (document.activeElement === el) return true;
    bringIntoView(scrollEl || el);
    try { el.focus({ preventScroll: true }); } catch (e) { el.focus(); }
    return true;
  }
  function focusCard(article) {
    return focusTarget(article.querySelector('.card-btn'), article);
  }
  /* Focus already inside the branch means the reader is there: landing again
     would take focus off the control they just used. */
  function focusWithin(el) {
    var a = document.activeElement;
    return !!(el && a && (el === a || el.contains(a)));
  }

  /* Delegated once, on a container that outlives every render, so re-rendering
     the cards can never leave a dead or a doubled listener behind. */
  cardsRoot().addEventListener('click', function (e) {
    var q = currentQuestion();
    if (!q) return;

    var head = e.target.closest ? e.target.closest('.card-btn') : null;
    if (head) {
      var art = head.closest('.card');
      var isOpen = head.getAttribute('aria-expanded') === 'true';
      // Toggling is a route change, not a DOM change: set the hash and let the
      // router be the only thing that opens or closes a card.
      location.hash = isOpen
        ? cardsRoute(q, art.dataset.branch)
        : cardsRoute(q, art.dataset.branch, art.dataset.card);
      return;
    }

    /* A face change is NOT a navigation. It assigns no hash, so it creates no
       history entry, does not close the accordion and does not move the card
       the URL names -- Back still steps through cards, never through faces.
       Focus moves to the equivalent control in the face that just appeared,
       because the button just pressed is now `hidden` and focus would
       otherwise fall to <body>. The label it lands on has changed, and that
       label change IS the state announcement: no live region, nothing to
       announce on every render. */
    var faceCtl = e.target.closest ? e.target.closest('.cnav-face') : null;
    if (faceCtl) {
      var shown = showFace(faceCtl.closest('.card-panel'), faceCtl.dataset.faceTo);
      if (shown) focusTarget(shown.querySelector('.cnav-face'));
      return;
    }

    var nav = e.target.closest ? e.target.closest('.cnav-prev, .cnav-next') : null;
    if (nav && !nav.disabled && nav.dataset.go) {
      var from = nav.closest('.card');
      location.hash = cardsRoute(q, from.dataset.branch, nav.dataset.go);
    }
    // .cnav-map is a real link on the existing #/q/<id>/map/<n> route: the
    // browser navigates it and landOnBranch does the focus, highlight and
    // scroll. No parallel implementation, no click handler needed.
  });

  function cardsRoute(q, n, cardId) {
    return '#/q/' + q.id + '/cards' + (n ? '/' + n : '') + (cardId ? '/' + cardId : '');
  }
  function currentQuestion() {
    var m = (location.hash || '').match(/^#\/q\/([a-z0-9-]+)/);
    return m ? DATA.questions[m[1]] : null;
  }

  /* ---- map: deterministic ORGANIC layout -------------------------------
     Positions come from a fixed named-position table, overridable per branch
     via the QSO's mapPresentation. Nothing is random: the same QSO renders
     identically every load. The asymmetry is authored, not generated. */
  var POSITIONS = {
    'upper-right': [0.78, -0.62], 'right': [1.02, -0.02], 'lower-right': [0.74, 0.60],
    'lower': [0.06, 0.94], 'lower-left': [-0.72, 0.64], 'left': [-1.00, 0.06],
    'upper-left': [-0.76, -0.60], 'upper': [-0.04, -0.94]
  };
  var RING = ['upper-right', 'right', 'lower-right', 'lower', 'lower-left', 'left', 'upper-left', 'upper'];

  /* Softly irregular rounded shape: a circle whose radius varies by a fixed,
     seed-derived amount. Deterministic — the seed is the branch index. */
  function blob(cx, cy, r, seed, cls) {
    var pts = [], N = 7, i;
    for (i = 0; i < N; i++) {
      var a = (2 * Math.PI * i / N) - Math.PI / 2;
      var vary = 1 + (((seed * 13 + i * 29) % 7) - 3) * 0.02;
      pts.push([cx + Math.cos(a) * r * vary, cy + Math.sin(a) * r * vary]);
    }
    var d = 'M' + ((pts[0][0] + pts[1][0]) / 2).toFixed(1) + ',' + ((pts[0][1] + pts[1][1]) / 2).toFixed(1);
    for (i = 1; i <= N; i++) {
      var p = pts[i % N], nx = pts[(i + 1) % N];
      d += ' Q' + p[0].toFixed(1) + ',' + p[1].toFixed(1) + ' ' +
           ((p[0] + nx[0]) / 2).toFixed(1) + ',' + ((p[1] + nx[1]) / 2).toFixed(1);
    }
    return '<path class="' + (cls || 'blob') + '" d="' + d + ' Z"/>';
  }

  function renderMap(q) {
    // Fixed viewBox: label sizes are absolute px against it, so the map
    // scales as a whole and text keeps a predictable relative size.
    var nodes = q.map.nodes, W = 1080, H = 760, cx = W / 2, cy = H / 2;
    // The wrapper is a group, NOT an image. An image role makes the whole
    // subtree presentational, which silently hid all seven branch links from
    // assistive technology even though each carried role/tabindex/aria-label.
    // Confirmed against the live accessibility tree, not inferred from source.
    var out = ['<svg viewBox="0 0 ' + W + ' ' + H + '" role="group" ' +
               'aria-label="Knowledge map for this question">'];
    var links = [], blobs = [];

    nodes.forEach(function (nd, i) {
      var pos = POSITIONS[nd.position] || POSITIONS[RING[i % RING.length]];
      // Different branch lengths: primary sits closer and reads stronger.
      // Increased reach separates branches 1-3, which previously crowded
      // together on the right and let labels run into connectors.
      var reach = (nd.emphasis === 'secondary' ? 388 : 330);
      var wob = ((i * 37) % 11 - 5) * 3.4;          // deterministic asymmetry
      var x = cx + pos[0] * reach + wob;
      var y = cy + pos[1] * (reach * 0.74) + wob * 0.5;
      var cls = 'cat-' + nd.category + (nd.emphasis === 'secondary' ? ' secondary' : '');
      var r = nd.emphasis === 'secondary' ? 34 : 42;

      // Curved connector: control point pushed perpendicular to the chord so
      // the link bows instead of running straight.
      var mx = (cx + x) / 2, my = (cy + y) / 2;
      var dx = x - cx, dy = y - cy, len = Math.sqrt(dx * dx + dy * dy) || 1;
      var bow = (i % 2 ? 1 : -1) * Math.min(52, len * 0.22);
      links.push('<path class="link ' + (nd.emphasis === 'secondary' ? 'secondary ' : 'primary ') + cls +
        '" d="M' + cx + ',' + cy + ' Q' + (mx + (-dy / len) * bow).toFixed(1) + ',' +
        (my + (dx / len) * bow).toFixed(1) + ' ' + x.toFixed(1) + ',' + y.toFixed(1) + '"/>');

      blobs.push('<g class="qnode ' + cls + '" data-n="' + nd.n + '" tabindex="0" role="link" ' +
        'aria-label="Branch ' + nd.n + ', ' + esc(nd.label) + '">' +
        blob(x, y, r, i + 1) +
        '<text class="nnum" x="' + x.toFixed(1) + '" y="' + (y + 7).toFixed(1) + '">' + nd.n + '</text>' +
        wrap(nd.label, x, y + r + 24, 17, 'nlabel', 20) + '</g>');
    });

    out.push(links.join(''));
    // Centre stays dominant: bigger than any branch, question wrapped over
    // several lines with room beneath for QB ref and focused topic, so the
    // two never collide.
    out.push('<g class="hub">' + blob(cx, cy, 148, 4, 'hubshape') +
      wrap(q.map.centre.question, cx, cy - 26, 21, 'hubq', 22) +
      '<text class="hubmeta" x="' + cx + '" y="' + (cy + 74) + '">' + esc(q.map.centre.qbRef) + '</text>' +
      '<text class="hubmeta" x="' + cx + '" y="' + (cy + 92) + '">' + esc(q.map.centre.focusedTopic) + '</text>' +
      '</g>');
    out.push(blobs.join(''), '</svg>');

    var cats = {};
    nodes.forEach(function (nd) { cats[nd.category] = true; });
    $('map-root').innerHTML = out.join('') + '<div class="map-legend">' +
      Object.keys(cats).map(function (c) {
        return '<span class="cat-' + c + '"><i></i>' + esc(c.replace(/-/g, ' ')) + '</span>';
      }).join('') + '</div>';
    $('map-title').textContent = q.canonicalQuestion;

    // One hash assignment, one history entry, and the router does the rest.
    // The previous version set the hash and then scrolled from a timeout,
    // which meant Back returned to a Cards view scrolled somewhere else.
    Array.prototype.forEach.call($('map-root').querySelectorAll('.qnode'), function (g) {
      function go() { location.hash = '#/q/' + q.id + '/cards/' + g.dataset.n; }
      g.addEventListener('click', go);
      g.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); }
      });
    });
  }

  function wrap(text, x, y, size, cls, width) {
    var words = String(text).split(' '), lines = [], cur = '', max = width || 17;
    words.forEach(function (w) {
      if ((cur + ' ' + w).trim().length > max) { lines.push(cur.trim()); cur = w; }
      else cur += ' ' + w;
    });
    if (cur.trim()) lines.push(cur.trim());
    var top = y - ((lines.length - 1) * size) / 2;
    return lines.map(function (l, i) {
      return '<text' + (cls ? ' class="' + cls + '"' : '') + ' x="' + x.toFixed(1) +
        '" y="' + (top + i * size).toFixed(1) + '">' + esc(l) + '</text>';
    }).join('');
  }

  /* Land on branch n in whichever view is showing. Returns false for a branch
     the QSO does not have, so the router can fall back rather than pretend. */
  function landOnBranch(q, mode, n) {
    var known = q.map.nodes.some(function (nd) { return String(nd.n) === String(n); });
    if (!known) return false;
    return land(mode === 'map'
      ? $('map-root').querySelector('.qnode[data-n="' + n + '"]')
      : $('branch-' + n));
  }

  /* ---- router ---------------------------------------------------------- */
  /* ---- router ----------------------------------------------------------
     #/q/<id>                       question overview
     #/q/<id>/cards                 all branches
     #/q/<id>/cards/<n>             cards, landed on branch n
     #/q/<id>/cards/<n>/<card>      cards, with that one card open
     #/q/<id>/map                   the map
     #/q/<id>/map/<n>               the map, landed on branch n

     <card> is the card's generated sectionId -- a stable editorial slug, not
     an array index, so inserting or reordering an answer section cannot
     repoint a route the reader saved. Reloading a direct card URL reopens the
     card because the state is IN the URL; nothing is persisted, so the same
     card does not reappear in a later study session.

     Readable, deterministic, and hash-only so it works from file:// with no
     server and no history API -- pushState/replaceState throw on a file://
     document, so canonicalising the URL at render time is not available and is
     not attempted. Fallbacks are deliberate rather than silent: an unknown
     question falls back to home, an unknown mode to the question overview, an
     unknown branch renders the view without landing on anything, and an
     unknown card renders the branch's cards with nothing open. Never a blank
     screen, never a fabricated destination, and never a rewritten URL. */
  var cardsShowing = null;

  function route() {
    var h = location.hash || '#/';
    var m = h.match(/^#\/q\/([a-z0-9-]+)(?:\/(cards|map)(?:\/(\d+)(?:\/([a-z0-9-]+))?)?)?/);
    if (!m || !DATA.questions[m[1]]) {
      // Home is a route with no card in it, so it must leave no card open --
      // the same rule the map and question-overview branches below already
      // follow. Found by the Milestone 7 route matrix: this was the one exit
      // of the three that never closed, so leaving to home (or to an unknown
      // question) left a card aria-expanded, its panel un-hidden and its face
      // still on 'back' inside the now-hidden Cards view. Nothing was visible,
      // but the claim that the DOM always matches the URL was not true here,
      // and Milestone 4's face state inherited the staleness exactly as that
      // milestone predicted it would.
      show('view-home'); closeAllCards(); $('modes').hidden = true;
      $('crumb-q').textContent = ''; $('crumb-sep').hidden = true;
      renderHome(); return;
    }
    var q = DATA.questions[m[1]], mode = m[2], branch = m[3];
    // A card segment is only meaningful in the Cards view. The map has no
    // cards, so a card named on a map route is dropped, not honoured.
    var card = mode === 'cards' ? m[4] : undefined;
    $('crumb-q').textContent = q.focusedTopic;
    $('crumb-sep').hidden = false;
    $('modes').hidden = !mode;
    // Switching view keeps the branch you were reading, so Map and Cards are
    // two ways of looking at the same place rather than two separate trips.
    // An unrecognised branch is dropped here, not propagated.
    var keep = q.map.nodes.some(function (nd) { return String(nd.n) === String(branch); })
      ? '/' + branch : '';
    $('mode-cards').href = '#/q/' + q.id + '/cards' + keep;
    $('mode-map').href = '#/q/' + q.id + '/map' + keep;
    $('mode-cards').classList.toggle('active', mode === 'cards');
    $('mode-map').classList.toggle('active', mode === 'map');
    $('sidebar-toggle').hidden = (mode !== 'cards');

    if (mode === 'cards') {
      show('view-cards');
      // Built once per question. Re-rendering on every toggle would destroy
      // the very button the reader just pressed -- taking their focus with it
      // -- so the route opens and closes elements that already exist.
      if (cardsShowing !== q.id) { renderCards(q); cardsShowing = q.id; }

      var opened = applyCardState(resolveCard(q, branch, card));
      if (opened) {
        focusCard(opened);
      } else if (branch) {
        // With no card open the branch is the destination, exactly as in
        // Milestone 2 -- unless the reader is already inside it, in which case
        // landing would pull focus off the control they just used to close a
        // card. This is the same "already there, do not jump" rule as focus.
        if (!focusWithin($('branch-' + branch))) landOnBranch(q, 'cards', branch);
      }
    } else if (mode === 'map') {
      show('view-map'); closeAllCards(); renderMap(q);
      if (branch) landOnBranch(q, 'map', branch);
    } else {
      show('view-question'); closeAllCards();
      $('q-topic').textContent = q.focusedTopic;
      $('q-canonical').textContent = q.canonicalQuestion;
      var c = q.counts, r = q.recurrence;
      $('q-counts').textContent =
        r.confirmed + ' confirmed occurrence(s) · ' + r.distinctNamedExaminers +
        ' named examiner(s) · ' + c.cards + ' cards across ' + c.branches +
        ' sections · ' + c.declaredGaps + ' declared gap(s)';
      $('go-cards').href = '#/q/' + q.id + '/cards';
      $('go-map').href = '#/q/' + q.id + '/map';
    }
  }

  /* ---- preference controls ----------------------------------------------
     Two native radio groups, not one toggle. A single button labelled with
     the state it is in or the state it would move to is ambiguous either way;
     a radio group shows both options and which one is live, and the browser
     gives arrow-key navigation, the checked state and the group name for
     free.

     Rendered into a container in the header that is NEVER hidden. #modes is
     hidden on the Overview view, so a control placed there would vanish from
     the one screen a first-time reader sees. */
  function prefControlHTML(prefs) {
    function group(legend, name, options, current) {
      return '<fieldset class="pref-set"><legend>' + esc(legend) + '</legend>' +
        options.map(function (o) {
          return '<label class="pref-opt"><input type="radio" name="' + esc(name) +
            '" value="' + esc(o.value) + '"' + (o.value === current ? ' checked' : '') +
            '><span>' + esc(o.label) + '</span></label>';
        }).join('') + '</fieldset>';
    }
    return group('Appearance', 'appearance', [
      { value: 'light', label: 'Light' }, { value: 'dark', label: 'Dark' }
    ], prefs.appearance) +
    group('Colour', 'colour', [
      { value: 'multicolour', label: 'Multicolour' }, { value: 'monochrome', label: 'Monochrome' }
    ], prefs.colour);
  }

  function renderPrefs(prefs) {
    var host = $('prefs');
    if (host) host.innerHTML = prefControlHTML(prefs);
  }

  /* A preference change repaints and persists. That is all it does: it
     assigns no hash, so there is no history entry and no route change; it
     does not re-render the cards, so the open card, its face, the scroll
     position and the focused control all survive untouched. The radio the
     reader just pressed keeps focus because nothing replaces it. */
  function bindPrefs() {
    var host = $('prefs');
    if (!host) return;
    host.addEventListener('change', function (e) {
      var input = e.target;
      if (!input || input.type !== 'radio') return;
      var patch = readPrefs();
      // Only the dimension that changed moves; the other is carried through.
      if (input.name === 'appearance' && APPEARANCES.indexOf(input.value) >= 0) {
        patch.appearance = input.value;
      } else if (input.name === 'colour' && COLOURS.indexOf(input.value) >= 0) {
        patch.colour = input.value;
      } else {
        return;                       // an unknown name or value changes nothing
      }
      applyPrefs(writePrefs(patch));
    });
  }

  window.addEventListener('hashchange', route);
  $('q-search').addEventListener('input', renderHome);
  $('sidebar-toggle').addEventListener('click', function () {
    $('sidebar').hidden = !$('sidebar').hidden;
  });
  $('status-select').addEventListener('change', function () {
    var id = (location.hash.match(/#\/q\/([a-z0-9-]+)/) || [])[1];
    if (id) State.set(id, { status: this.value });
  });
  $('flag-revision').addEventListener('change', function () {
    var id = (location.hash.match(/#\/q\/([a-z0-9-]+)/) || [])[1];
    if (id) State.set(id, { flagged: this.checked });
  });

  /* Preferences settle BEFORE the first route runs, so the very first paint
     the reader sees is already the one they chose. The inline bootstrap in
     index.html has usually stamped the same two attributes a moment earlier;
     this call is what makes them authoritative, and it agrees with the
     bootstrap by construction because both read the same key and accept the
     same controlled values. */
  var PREFS = applyPrefs(readPrefs());
  renderPrefs(PREFS);
  bindPrefs();

  route();
})();
