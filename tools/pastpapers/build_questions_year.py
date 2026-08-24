#!/usr/bin/env python3
"""Generate the ONLY QUESTIONS year sheet: questions-<year>.html.

    specs/*.json  -->  recurrence_model  -->  questions-<year>.html

Generic by construction. The year is data, the months are data, and the absent
sittings are data. Adding specs/QP2503.json produces questions-2025.html with
no change to this file, exactly as topics-<year>.html already behaves.

What this page is
-----------------
Every printed examination question for one year, month by month, with marks,
category and honest recurrence intelligence -- and NO answer content of any
kind. It is the discovery surface: it answers "what does this examination
actually ask?" and hands the candidate to the solved paper for "how do I
answer it?".

Three rules it must not break
-----------------------------
1. NO ANSWER CONTENT. Not the model answer, not the study guide, not the route,
   not the retrieval cards, not the quick-revision keywords -- and not in the
   search tokens either, where it would be invisible but still shipped.
2. NO THIRD-PARTY RECURRENCE. The ``recurrence`` list on each question is the
   source copy host's own annotation. Policy classes it discovery-only, the
   2026 set proved it wrong in both directions, and republishing another
   party's analysis on a public page is a separate problem again. Canonical
   recurrence is computed in recurrence_model.py from MIW's own transcriptions.
3. NO CHRONOLOGICAL LIES. Status comes from the calendar, never from the
   authoring field ``recurrence_class`` -- see recurrence_model.py for the three
   questions in the 2026 set where the two disagree.
"""
import argparse
import glob
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import (REPO_ROOT, esc, esc_attr, strip_tags, read_css,
                           topbar, head_meta, footer, GATE_STUB, delivery_links,
                           CORPUS_SEARCH_JS, corpus_fallback_block)
import recurrence_model as RM

# The candidate-safe QI projection lives in the study layer because that is
# where both intelligence layers are joined. This page RENDERS it and decides
# nothing: which longitudinal label a candidate may see, and in what words, is
# settled in tools/study/qi_projection.py so that this page, the solved paper
# page and the topic page cannot disagree about the same question.
sys.path.insert(0, os.path.join(REPO_ROOT, 'tools', 'study'))
import qi_projection as QIP

PP_DIR = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')
SPEC_GLOB = os.path.join(PP_DIR, 'specs', '*.json')

# Sittings that are known NOT to exist, with the evidence for saying so. This is
# a much stronger statement than "we have not built it yet", and the two must
# never render the same way: one is a fact about the examination, the other is a
# fact about MIW's backlog. Keyed (year, month_number).
# May now reads the same way in SIX consecutive years. That is strong evidence, but it
# remains an inference from the source set: a DGMA / DG Shipping examination calendar
# stating that no May sitting is held was searched for on 2026-08-14 and could NOT be
# located. The wording below therefore states the evidence rather than asserting a rule.
#
# June 2021 is deliberately NOT filed with May, because it is a different thing.
KNOWN_ABSENT = {
    (2026, 5): 'No May sitting appears in the MIW source set, and the printed serial numbering '
               'skips it in every year MIW holds &mdash; 2021 runs &hellip;2104, 2107&hellip;, '
               '2022 runs &hellip;2204, 2206&hellip;, and 2023 to 2025 run &hellip;2304, '
               '2306&hellip;, &hellip;2404, 2406&hellip; and &hellip;2504, 2506&hellip;.',
    (2025, 5): 'No May sitting. The printed serial numbering runs &hellip;2504, 2506&hellip; '
               'with nothing at 2505.',
    (2024, 5): 'No May sitting. The printed serial numbering runs &hellip;2404, 2406&hellip; '
               'with nothing at 2405.',
    (2023, 5): 'No May sitting. The printed serial numbering runs &hellip;2304, 2306&hellip; '
               'with nothing at 2305.',
    (2022, 5): 'No May sitting. The printed serial numbering runs &hellip;2204, 2206&hellip; '
               'with nothing at 2205.',
    (2021, 5): 'No May sitting. The printed serial numbering runs &hellip;2104, 2107&hellip; '
               'with nothing at 2105.',
    # A one-off, and the reason is visible in the source set rather than assumed.
    (2021, 6): 'No June paper was numbered &mdash; the printed serials run &hellip;2104, '
               '2107&hellip;. This is not the standing May pattern. 2020 holds only six papers, '
               'with April to September absent, and July 2021 carries TWO papers of which the '
               'second prints no serial at all &mdash; the only paper in 2021 or 2022 that does '
               'not. The reading that fits all three is a June sitting deferred into July.',
}


# The two filter rows scroll sideways instead of wrapping.
#
# Measured before this rule: twelve filter buttons wrapped onto four lines at
# 375px, the controls bar grew to 346px and the sticky chrome took 56.3% of the
# viewport -- the same proportion already recorded as a pre-existing complaint
# against the paper pages. A brand new page should not ship with a defect that
# is already on the review list, and unlike the paper chrome this markup is
# ours to fix. One line each, scrollable, keeps every filter reachable.
YEAR_CSS = """
.qy-filters{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;
  scrollbar-width:thin;padding-top:0}
.qy-filters .filter-btn{flex:0 0 auto}
.qy-legend .cov-row{align-items:flex-start}
"""


def load_specs():
    return [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(SPEC_GLOB))]


def question_search_tokens(node, spec_q, status_label):
    """Deterministic search string for the questions-only page.

    This is the SAME mechanism as the index -- generated data-search attributes
    filtered client-side, never innerText, so a collapsed or scrolled-away card
    still matches. It is NOT a second search engine.

    The token set is deliberately narrower than render_common.search_tokens():
    that one folds in model-answer headings, study-guide headings and
    quick-revision keywords, which are answer content. On a questions-only page
    those would be invisible on screen and still present in the shipped HTML,
    which is precisely the leak this product is supposed to avoid. `regulations`
    is excluded for the same reason -- which instruments a question turns on is
    part of what the solved product sells.
    """
    parts = [node['q_no'], node['question_id'], node['paper_id'], node['month'],
             str(node['year']), node['month_year'], node['short_title'],
             strip_tags(node['text_verbatim']), '%s marks' % node['marks'],
             node['primary_category'] or '', strip_tags(status_label)]
    parts += node['subject_tags']
    parts += node['topic_tags']
    # Aliases are topic synonyms ("poseidon principles", "bfrb") and are what
    # makes search work on a term the printed stem never uses. They are NOT
    # withheld: an experiment filtering every alias that also occurs in the
    # answer layer removed 118 of them -- "formal safety assessment",
    # "Casualty Investigation Code", "Merchant Shipping Act 2025" -- because an
    # answer about a concept naturally names it. That protected nothing (the
    # only phrase it was built for turned out to be a quotation of the printed
    # stem) and would have crippled the page's search. The real guard is the
    # leak sweep in questions_year_check.py, which compares shipped bytes
    # against the answer layer and adjudicates stem overlap.
    parts += spec_q.get('search_aliases') or []
    seen, out = set(), []
    for p in parts:
        t = strip_tags(p).lower()
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return ' '.join(out)


def _page_js():
    """Filter + search. Plain DOM work over generated attributes.

    The corpus matcher is injected from render_common so this page, the paper
    page and the home page fold and match a query identically -- the same words
    must give the same answer wherever they are typed.
    """
    return CORPUS_SEARCH_JS + """
  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-qsearch]'));
  var input = document.getElementById('qy-search');
  var clear = document.getElementById('qy-clear');
  var count = document.getElementById('qy-count');
  var state = { q: '', rec: 'all', cat: 'all' };

  function apply() {
    var shown = 0;
    cards.forEach(function (c) {
      var okQ = !state.q || c.getAttribute('data-qsearch').indexOf(state.q) !== -1;
      var okR = state.rec === 'all' || c.getAttribute('data-rec') === state.rec;
      var okC = state.cat === 'all' || c.getAttribute('data-cat') === state.cat;
      var ok = okQ && okR && okC;
      c.hidden = !ok;
      if (ok) shown++;
    });
    // A month heading with nothing under it is noise, so hide the whole block --
    // but only when a filter is active, so the "no paper in this month" notes
    // stay visible in the default view where they are the point.
    var filtering = state.q || state.rec !== 'all' || state.cat !== 'all';
    Array.prototype.forEach.call(document.querySelectorAll('[data-month-block]'), function (b) {
      var any = b.querySelector('[data-qsearch]:not([hidden])');
      b.hidden = filtering && !any;
    });
    count.textContent = filtering
      ? shown + ' of ' + cards.length + ' questions'
      : cards.length + ' questions';
    mcUpdate(state.q, shown);
  }

  // ---- corpus escape hatch ------------------------------------------------
  // A year sheet is correctly scoped to its year. On its own that means a
  // reader looking for a topic this year's examiners did not set is told it
  // does not exist. The same shared matcher the home page and paper pages use
  // answers "and what about the other years?".
  var mcWrap = document.getElementById('mc-wrap');
  var mcSum = document.getElementById('mc-sum');
  var mcNote = document.getElementById('mc-note');
  var mcRes = document.getElementById('mc-res');
  var mcOffer = document.getElementById('mc-offer');
  var mcOfferBtn = document.getElementById('mc-offer-btn');
  var THIS_YEAR = parseInt(document.body.getAttribute('data-year') || '0', 10);
  var mcShown = '';

  function mcRender(q, reason) {
    if (!mcWrap) return;
    if (mcShown === q + '|' + reason) return;
    MIWCorpus.load().then(function (idx) {
      if (!idx) { mcWrap.hidden = true; return; }
      if (input && input.value.trim().toLowerCase() !== q) return;
      var res = MIWCorpus.match(q, { excludeYear: THIS_YEAR });
      if (!res.questions) {
        mcWrap.hidden = true;
        if (mcOffer) mcOffer.hidden = true;
        mcShown = q + '|' + reason;
        return;
      }
      mcSum.innerHTML = MIWCorpus.summary(res);
      mcNote.textContent = reason === 'empty'
        ? 'Nothing in ' + THIS_YEAR + ' — these are from other years.'
        : 'Also set in other years.';
      mcRes.innerHTML = MIWCorpus.renderGroups(res);
      mcWrap.hidden = false;
      if (mcOffer) mcOffer.hidden = true;
      mcShown = q + '|' + reason;
    });
  }

  function mcUpdate(q, shown) {
    if (!mcWrap) return;
    if (!q) { mcWrap.hidden = true; if (mcOffer) mcOffer.hidden = true; mcShown = ''; return; }
    if (shown === 0) {
      if (mcOffer) mcOffer.hidden = true;
      mcRender(q, 'empty');
    } else {
      mcWrap.hidden = true; mcShown = '';
      if (mcOffer && mcOfferBtn) {
        mcOfferBtn.textContent = 'Search all solved papers for “' + q + '”';
        mcOffer.hidden = false;
      }
    }
  }

  if (mcOfferBtn) mcOfferBtn.addEventListener('click', function () {
    var q = (input && input.value ? input.value : '').trim().toLowerCase();
    if (q) mcRender(q, 'chose');
  });

  if (input) {
    input.addEventListener('input', function () {
      state.q = input.value.trim().toLowerCase();
      apply();
    });
  }
  if (clear) {
    clear.addEventListener('click', function () {
      input.value = ''; state.q = ''; apply(); input.focus();
    });
  }
  Array.prototype.forEach.call(document.querySelectorAll('[data-filter]'), function (b) {
    b.addEventListener('click', function () {
      var group = b.getAttribute('data-filter');
      var val = b.getAttribute('data-value');
      state[group] = val;
      Array.prototype.forEach.call(
        document.querySelectorAll('[data-filter="' + group + '"]'), function (o) {
          o.classList.toggle('active', o === b);
          o.setAttribute('aria-pressed', o === b ? 'true' : 'false');
        });
      apply();
    });
  });
  apply();
"""


def build_year_page(specs, year, publish, deliver=False):
    # deliver = the copy served inside the paid /solvedQP/ product. Same
    # generator, same specs, same recurrence model -- only the canonical URL
    # and the navigation change. There is deliberately no second,
    # hand-maintained question list anywhere in the system.
    year_specs = [d for d in specs if d['year'] == year]
    nodes = RM.load_nodes(specs)          # all years: families must cross years
    relations = RM.build_families(nodes)

    spec_q = {}
    for d in specs:
        for q in d['questions']:
            spec_q[q['question_id']] = q

    by_month = {}
    solved_months = set()
    for d in year_specs:
        mn = RM.MONTH_NUM[d['month']]
        by_month[mn] = d
        if any(q.get('model_answer') for q in d['questions']):
            solved_months.add(mn)

    year_nodes = [n for n in nodes.values() if n['year'] == year]
    total_q = len(year_nodes)
    cats = sorted({n['primary_category'] for n in year_nodes if n['primary_category']})

    o = []
    a = o.append
    title = ('MEO Class I Written Examination Questions &mdash; %d | Marine Intelligence Weekly'
             % year)
    desc = ('Every MEO Class I Engineering Management written examination question set in %d, '
            'month by month, with printed marks, topic and recurrence history. Questions only.'
            % year)
    canonical = (('/solvedQP/questions-%d.html' % year) if deliver
                 else ('/meoclass1/pastpapers/questions-%d.html' % year))
    o.extend(head_meta(strip_tags(title), strip_tags(desc), canonical, publish))
    a('<style>')
    a(read_css())
    a(YEAR_CSS)
    a('</style>')
    a('</head>')
    # data-year lets the corpus fallback exclude the year already on screen.
    a('<body data-year="%d">' % year)
    a(GATE_STUB)
    a('<a class="skip" href="#qy-main">Skip to content</a>')
    # A delivered year sheet navigates within /solvedQP/ and links to its
    # OWN year, not to a single hard-coded one.
    o.extend(topbar('Questions by year' if deliver else '',
                    links=delivery_links(year=year) if deliver else None))
    a('<header class="page-header"><div class="wrap">')
    a('  <span class="badge">MEO Class I &middot; Engineering Management</span>')
    a('  <h1>%d &mdash; every written question</h1>' % year)
    a('  <p class="sub">The complete printed question paper for each %d sitting MIW has '
      'transcribed, with marks, topic and recurrence. Questions only &mdash; no answers on '
      'this page.</p>' % year)
    a('  <div class="header-meta"><span>%d question%s</span><span>%d sitting%s</span>'
      '<span>%d of 12 months</span></div>'
      % (total_q, '' if total_q == 1 else 's',
         len(year_specs), '' if len(year_specs) == 1 else 's', len(year_specs)))
    a('</div></header>')
    # The delivery copy is a paying customer's page, so it gets no review
    # banner -- same rule as the papers. It stays noindex via publish=False.
    if not publish and not deliver:
        a('<div class="review-banner"><strong>Founder review copy.</strong> Generated by '
          '<code>tools/pastpapers/build_questions_year.py</code> from the canonical specs. '
          'Not indexable. Regenerates automatically as papers are added.</div>')

    # ---- controls -------------------------------------------------------
    a('<div class="controls-bar"><div class="controls-inner">')
    a('  <label class="search-wrap"><span aria-hidden="true">&#128269;</span>')
    a('    <input id="qy-search" type="search" autocomplete="off" '
      'placeholder="Search every %d question &mdash; e.g. general average, fatigue, MARPOL" '
      'aria-label="Search every %d written question">' % (year, year))
    a('    <button id="qy-clear" class="icon-btn" type="button" aria-label="Clear search">'
      '&times;</button>')
    a('  </label>')
    a('  <span class="count-label" id="qy-count" role="status" aria-live="polite"></span>')
    a('</div>')
    a('<div class="controls-inner qy-filters" style="gap:6px;">')
    for val, label in (('all', 'All questions'), ('repeated', 'Repeated'),
                       ('first', 'First in set'), ('single', 'Set once')):
        a('  <button class="filter-btn%s" type="button" data-filter="rec" data-value="%s" '
          'aria-pressed="%s">%s</button>'
          % (' active' if val == 'all' else '', val,
             'true' if val == 'all' else 'false', esc(label)))
    a('</div>')
    a('<div class="controls-inner qy-filters" style="gap:6px;">')
    a('  <button class="filter-btn active" type="button" data-filter="cat" data-value="all" '
      'aria-pressed="true">All topics</button>')
    for c in cats:
        a('  <button class="filter-btn" type="button" data-filter="cat" data-value="%s" '
          'aria-pressed="false">%s</button>' % (esc_attr(c), esc(c)))
    a('</div>')
    a('</div>')

    a('<main id="qy-main" style="max-width:1000px;margin:0 auto;padding:20px;">')

    # Corpus escape hatch. Delivery only -- it reads the /solvedQP/ manifest,
    # which the review copy under /meoclass1/pastpapers/ must not reach into.
    if deliver:
        o.extend(corpus_fallback_block(str(year)))

    # Recurrence legend. The vocabulary is candidate-facing and its scope limit
    # is stated on the page rather than assumed -- "set once" means once in what
    # MIW has transcribed, and a candidate must not read it as "never asked".
    a('<section class="topic-group qy-legend">')
    a('  <h3>How to read the recurrence tags</h3>')
    a('  <div class="tg-sub">Worked out by comparing the printed questions MIW has '
      'transcribed, not taken from any third party&rsquo;s recurrence table.</div>')
    a('  <div class="cov-row"><span class="cov-k">First in set</span>'
      '<span class="cov-v">The earliest sitting MIW holds for this examiner task. It comes '
      'back later in the year.</span></div>')
    a('  <div class="cov-row"><span class="cov-k">Repeated</span>'
      '<span class="cov-v">The same examiner task has already been set at an earlier sitting '
      '&mdash; either in the same words, or reworded.</span></div>')
    a('  <div class="cov-row"><span class="cov-k">Once in MIW&rsquo;s transcribed set</span>'
      '<span class="cov-v">Set once across the sittings MIW has transcribed &mdash; %s so far. '
      '<b>That is not the same as never asked before.</b> It is a statement about this '
      'comparison set only, and the longer-term signal below may still show the concept '
      'recurring outside it.</span></div>'
      % esc(_scope_phrase(specs)))
    a('</section>')
    # The second layer gets its own legend block, because the mistake this page
    # has to prevent is a reader treating the two vocabularies as one scale.
    a('<section class="topic-group qy-legend">')
    a('  <h3>How to read the longer-term signal</h3>')
    a('  <div class="tg-sub">A second, separate layer. The tags above compare printed '
      'questions <i>within</i> the set MIW has transcribed. These compare the underlying '
      'examinable concept against MIW&rsquo;s governed question intelligence, which reaches '
      'further back than the solved papers do.</div>')
    a('  <div class="cov-row"><span class="cov-k">Persistent &middot; Rising &middot; '
      'Re-emerging &middot; Active in recent papers</span>'
      '<span class="cov-v">How the concept behaves over the longer horizon. These are '
      'qualitative on purpose: MIW does not publish sitting dates it cannot evidence from a '
      'source copy, so no count and no year is claimed here.</span></div>')
    a('  <div class="cov-row"><span class="cov-k">Recurs beyond MIW&rsquo;s solved set</span>'
      '<span class="cov-v">MIW&rsquo;s question intelligence holds earlier occurrences of this '
      'concept whose sitting dates rest on secondary sources. The recurrence is reported; the '
      'dates are not, and are not counted.</span></div>')
    a('  <div class="cov-row"><span class="cov-k">Current answer verified</span>'
      '<span class="cov-v">MIW has checked this answer against current primary authority and '
      'an independent reviewer passed it. <i>No currentness risk flagged</i> is weaker: '
      'nothing suggests the framework has moved, but no verification has been done.</span></div>')
    a('  <div class="cov-row"><span class="cov-k">Currentness check pending &middot; '
      'Answer under currentness review</span>'
      '<span class="cov-v">The framework behind this answer may have moved since the sitting. '
      'The answer is still correct <i>for its own sitting</i> &mdash; every MIW written answer '
      'is anchored to the date of its examination &mdash; but do not rely on it as a statement '
      'of the law today.</span></div>')
    a('</section>')

    for mn in range(1, 13):
        month = RM.MONTHS[mn - 1]
        a('<section class="topic-group" data-month-block="%d">' % mn)
        if mn in by_month:
            d = by_month[mn]
            qs = sorted([n for n in year_nodes if n['month_num'] == mn],
                        key=lambda n: int(''.join(ch for ch in n['q_no'] if ch.isdigit())))
            solved = mn in solved_months
            a('  <h3>%s %d <span class="q-tag%s">%s</span></h3>'
              % (esc(month), year, '' if solved else ' sub',
                 'Solved paper available' if solved else 'Questions transcribed'))
            a('  <div class="tg-sub">%s &middot; %s &middot; %s &middot; %d question%s printed'
              % (esc(d['subject']), esc(d['class']), esc(d['time_allowed']),
                 len(qs), '' if len(qs) == 1 else 's'))
            if solved:
                a('    &middot; <a href="%s.html">Open the solved paper</a>' % esc_attr(d['paper_id']))
            a('  </div>')
            if d.get('marks_note'):
                a('  <div class="rec-note">%s</div>' % esc(d['marks_note']))
            for n in qs:
                _render_question(a, n, relations, nodes, spec_q, solved)
        elif (year, mn) in KNOWN_ABSENT:
            a('  <h3>%s %d <span class="q-tag sub">No sitting</span></h3>' % (esc(month), year))
            a('  <div class="rec-note"><strong>No examination paper exists for this month.</strong> %s</div>'
              % KNOWN_ABSENT[(year, mn)])
        else:
            a('  <h3>%s %d <span class="q-tag sub">Not yet in the MIW set</span></h3>'
              % (esc(month), year))
            a('  <div class="rec-note">This sitting is not yet in the MIW canonical dataset. '
              'That is a statement about MIW&rsquo;s coverage, not about whether the '
              'examination was held.</div>')
        a('</section>')

    a('</main>')
    a('<script>')
    a(_page_js())
    a('</script>')
    o.extend(footer(publish or deliver))
    a('</body>')
    a('</html>')
    return '\n'.join(o) + '\n'


def _scope_phrase(specs):
    years = sorted({d['year'] for d in specs})
    n = len(specs)
    if len(years) == 1:
        return '%d %d sitting%s' % (n, years[0], '' if n == 1 else 's')
    return '%d sittings across %s' % (n, '&ndash;'.join(str(y) for y in (years[0], years[-1])))


def _render_question(a, n, relations, nodes, spec_q, solved):
    rel = relations[n['question_id']]
    q = spec_q[n['question_id']]
    # label_plain, not label. An HTML entity inside a data-search attribute is
    # escaped a second time, so the shipped token read "repeated &amp;mdash;
    # reworded" and a candidate searching the words on screen matched nothing.
    # STATUS_LABEL_PLAIN exists for exactly this slot; it was simply never
    # wired to it.
    a('  <div class="hit" data-qsearch="%s" data-rec="%s" data-cat="%s" id="%s">'
      % (esc_attr(question_search_tokens(n, q, rel['label_plain'])),
         esc_attr(rel['filter']), esc_attr(n['primary_category'] or ''),
         esc_attr(n['question_id'])))
    a('    <div class="hit-top">%s <span class="sep">&middot;</span> %s '
      '<span class="sep">&middot;</span> %s marks <span class="sep">&middot;</span> %s</div>'
      % (esc(n['month_year']), esc(n['q_no']), n['marks'],
         esc(n['primary_category'] or 'Uncategorised')))
    # The full printed question, verbatim, including its printed sub-limbs. This
    # is the whole point of the page -- never truncated, unlike the topic page,
    # which shows a 230-character preview because it is a routing surface.
    a('    <div class="hit-title">%s</div>' % esc(n['short_title']))
    for line in n['text_verbatim'].split('\n'):
        a('    <div class="q-stem">%s</div>' % esc(line))
    for sp in n['subparts']:
        # QP2607 spells the limb marker 'label'; the other five spell it 'ref'.
        # Reading only one silently drops every limb marker on five papers.
        label = sp.get('label') or sp.get('ref') or ''
        marks = sp.get('marks')
        a('    <div class="q-stem">%s%s%s</div>'
          % (esc(label + ' ') if label else '', esc(sp.get('text', '')),
             ' <b>(%s)</b>' % marks if marks else ''))
    a('    <div class="pc-topics" style="margin-top:6px;">%s</div>'
      % ''.join('<span class="q-tag sub">%s</span>' % esc(t) for t in n['topic_tags'][:5]))
    # LAYER 1 -- modern recurrence, from the calendar. Unchanged.
    a('    <div class="rec-note"><span class="q-tag rec">%s</span> %s</div>'
      % (rel['label'], RM.family_summary(nodes, relations, n['question_id'])))
    # LAYER 2/3 -- longitudinal signal and answer readiness, from the governed
    # projection. A SEPARATE line: the two layers answer different questions
    # over different horizons and folding them into one sentence is how a
    # "set once" tag comes to contradict a "persistent topic" tag. Renders
    # nothing at all where the projection knows nothing.
    block = QIP.render_block(n['question_id'], audience='GATED')
    if block:
        a('    %s' % block)
    if solved:
        a('    <div class="btn-row"><a class="nav-btn" href="%s.html#%s">'
          'Open the solved answer &rarr;</a></div>'
          % (esc_attr(n['paper_id']), esc_attr(n['anchor'])))
    a('  </div>')



# --------------------------------------------------------------------------- #
# THE WORDING ARCHIVE  --  2021 and 2022
# --------------------------------------------------------------------------- #
#
# A year sheet above is built from a SOLVED spec. These are built from
# meoclass1/pastpapers/intelligence/historical_qp_intelligence.json, which holds
# printed question wording and printed rubric metadata for sittings MIW has a
# source copy of and has never solved. That file's own governing statement is
# that no model answer for those sittings may be authored without a separate
# Founder decision, so this page can only ever be a wording archive.
#
# Why 2021 and 2022 belong in the candidate's chronology and 2010-2020 do not
# -------------------------------------------------------------------------
# Their SITTING DATES ARE PRINTED ON A SOURCE COPY MIW HOLDS -- the same
# date_certainty as every solved paper (PRINTED_ON_SOURCE_COPY, 558 of the 1,584
# governed occurrences). The 2010-2020 band is SECONDARY_CLAIMED: recovered
# through a secondary repository via a web archive, with dates nobody has
# corroborated against a printed paper. Both are good recurrence evidence and
# only one of them can carry a date in front of a candidate. A year page is a
# dated claim about every question it prints, so this file builds 2021 and 2022
# and REFUSES to build anything earlier -- see ARCHIVE_FLOOR, and the boundary
# guard in questions_year_check.py that proves the refusal.
#
# Three things this page must never do
# ------------------------------------
# 1. LOOK SOLVED. No "Solved paper available", no "Open the solved paper", no
#    "Open the solved answer". The whole difference between this page and the
#    sheet above is that MIW has not answered these questions.
# 2. CARRY A LAYER-1 RECURRENCE TAG. recurrence_model computes those from the
#    SPEC set, so feeding archive papers into it would silently rewrite the
#    modern tags on 2023-2026: a question that reads "first in set" would become
#    "repeated" and the calendar model would stop matching the shipped product.
#    The archive shows the GOVERNED longitudinal projection instead, which
#    already covers all 198 of these questions, and nothing else.
# 3. REPUBLISH THE HOST'S ANNOTATION. `host_recurrence_hint` on these records is
#    the source copy publisher's own recurrence analysis. Rule 2 at the top of
#    this file bars it, and it is directional besides.
ARCHIVE_PATH = os.path.join(PP_DIR, 'intelligence', 'historical_qp_intelligence.json')

#: The earliest year that may appear in the standard question-year chronology.
#: Not a preference. Raising this floor is a separate historical-archive design
#: with its own provenance vocabulary, not an edit here.
ARCHIVE_FLOOR = 2021


def load_archive():
    """Question-only sittings, grouped {year: {month_num: [paper, ...]}}.

    A month can hold MORE THAN ONE paper: July 2021 carries two, and the second
    prints no serial at all. The solved builder keys one spec per month because
    the solved set has never had a double sitting; assuming the same here would
    silently drop nine questions.
    """
    if not os.path.exists(ARCHIVE_PATH):
        return {}
    doc = json.load(open(ARCHIVE_PATH, encoding='utf-8'))
    out = {}
    for p in doc.get('papers', []):
        out.setdefault(p['year'], {}).setdefault(RM.MONTH_NUM[p['month']], []).append(p)
    for months in out.values():
        for papers in months.values():
            papers.sort(key=lambda p: (bool(p.get('second_sitting')),
                                       p.get('printed_serial') or ''))
    return out


def archive_years(specs, archive):
    """Years the archive may publish: at or above the floor, and NOT solved.

    A year holding even one solved spec is served by the solved year sheet, and
    two sheets for one year would be two answers to the same question. The
    intelligence file states this exclusion for its consumers; applying it here
    by rule rather than by dropping the records is what makes it testable.
    """
    solved = {d['year'] for d in specs}
    return sorted(y for y in archive if y >= ARCHIVE_FLOOR and y not in solved)


def _archive_search_tokens(paper, q):
    parts = [q['q_no'], q['question_id'], paper['paper_id'], paper['month'],
             str(paper['year']), paper['sitting'], strip_tags(q['text_verbatim'])]
    seen, out = set(), []
    for p in parts:
        t = strip_tags(p).lower()
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return ' '.join(out)


def _archive_js():
    """Search only. No recurrence or topic filters, because there is no
    governed per-question topic mapping for these years and no Layer-1 tag --
    and a filter control with nothing behind it is itself a claim."""
    return """
  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-qsearch]'));
  var input = document.getElementById('qy-search');
  var clear = document.getElementById('qy-clear');
  var count = document.getElementById('qy-count');
  var q = '';

  function apply() {
    var shown = 0;
    cards.forEach(function (c) {
      var ok = !q || c.getAttribute('data-qsearch').indexOf(q) !== -1;
      c.hidden = !ok;
      if (ok) shown++;
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-month-block]'), function (b) {
      var any = b.querySelector('[data-qsearch]:not([hidden])');
      b.hidden = !!q && !any;
    });
    count.textContent = q ? shown + ' of ' + cards.length + ' questions'
                          : cards.length + ' questions';
  }
  if (input) {
    input.addEventListener('input', function () {
      q = input.value.trim().toLowerCase(); apply();
    });
  }
  if (clear) {
    clear.addEventListener('click', function () {
      input.value = ''; q = ''; apply(); input.focus();
    });
  }
  apply();
"""


def build_archive_year_page(archive, year, publish, deliver=False):
    months = archive[year]
    papers = [p for ms in months.values() for p in ms]
    total_q = sum(len(p['questions']) for p in papers)

    o = []
    a = o.append
    title = ('MEO Class I Written Examination Questions &mdash; %d (question archive) '
             '| Marine Intelligence Weekly' % year)
    desc = ('The printed MEO Class I Engineering Management written examination questions MIW '
            'holds for %d, month by month. Question wording only &mdash; MIW has not solved '
            'these papers.' % year)
    canonical = (('/solvedQP/questions-%d.html' % year) if deliver
                 else ('/meoclass1/pastpapers/questions-%d.html' % year))
    o.extend(head_meta(strip_tags(title), strip_tags(desc), canonical, publish))
    a('<style>')
    a(read_css())
    a(YEAR_CSS)
    a('</style>')
    a('</head>')
    a('<body data-year="%d" data-archive="1">' % year)
    a(GATE_STUB)
    a('<a class="skip" href="#qy-main">Skip to content</a>')
    o.extend(topbar('Questions by year' if deliver else '',
                    links=delivery_links(year=year) if deliver else None))
    a('<header class="page-header"><div class="wrap">')
    a('  <span class="badge">MEO Class I &middot; Engineering Management</span>')
    a('  <h1>%d &mdash; the question papers MIW holds</h1>' % year)
    a('  <p class="sub"><b>Question wording archive.</b> The printed paper for each %d sitting '
      'MIW holds a source copy of. <b>MIW has not solved these papers</b> &mdash; there is no '
      'model answer, exam plan, study guide or recall content for any question below, and none '
      'is implied by its presence here.</p>' % year)
    a('  <div class="header-meta"><span>%d question%s</span><span>%d sitting%s</span>'
      '<span>0 solved answers</span></div>'
      % (total_q, '' if total_q == 1 else 's',
         len(papers), '' if len(papers) == 1 else 's'))
    a('</div></header>')
    if not publish and not deliver:
        a('<div class="review-banner"><strong>Founder review copy.</strong> Generated by '
          '<code>tools/pastpapers/build_questions_year.py</code> from '
          '<code>intelligence/historical_qp_intelligence.json</code>. Not indexable.</div>')

    a('<div class="controls-bar"><div class="controls-inner">')
    a('  <label class="search-wrap"><span aria-hidden="true">&#128269;</span>')
    a('    <input id="qy-search" type="search" autocomplete="off" '
      'placeholder="Search every %d question &mdash; e.g. general average, lay-up, MARPOL" '
      'aria-label="Search every %d written question">' % (year, year))
    a('    <button id="qy-clear" class="icon-btn" type="button" aria-label="Clear search">'
      '&times;</button>')
    a('  </label>')
    a('  <span class="count-label" id="qy-count" role="status" aria-live="polite"></span>')
    a('</div></div>')

    a('<main id="qy-main" style="max-width:1000px;margin:0 auto;padding:20px;">')

    a('<section class="topic-group qy-legend">')
    a('  <h3>What MIW has, and what it does not</h3>')
    a('  <div class="tg-sub">Stated first, because everything below is question wording and '
      'nothing below is an answer.</div>')
    a('  <div class="cov-row"><span class="cov-k">Held</span>'
      '<span class="cov-v">The printed question paper for %d %s, transcribed from a source '
      'copy: every question in full, with the printed serial, the time allowed and the total '
      'marks exactly as printed.</span></div>'
      % (len(papers), 'sittings' if len(papers) != 1 else 'sitting'))
    a('  <div class="cov-row"><span class="cov-k">Not held</span>'
      '<span class="cov-v"><b>No solved answer for any of these questions.</b> No per-question '
      'mark split either &mdash; these papers print a total only. Where a question carries no '
      'longer-term signal below, that means no governed recurrence family reaches it yet, not '
      'that it has never recurred.</span></div>')
    a('  <div class="cov-row"><span class="cov-k">Dates</span>'
      '<span class="cov-v">Every sitting below is dated from the printed source copy, which is '
      'the same standard as MIW&rsquo;s solved papers. MIW holds recurrence evidence reaching '
      'further back than this, but those dates rest on secondary sources and are therefore '
      'never printed as a year or a count.</span></div>')
    a('</section>')

    a('<section class="topic-group qy-legend">')
    a('  <h3>How to read the longer-term signal</h3>')
    a('  <div class="tg-sub">The same governed projection the solved papers and the other year '
      'sheets use, rendered by the same code. This page computes no recurrence of its '
      'own.</div>')
    a('  <div class="cov-row"><span class="cov-k">Persistent &middot; Rising &middot; '
      'Re-emerging &middot; Active in recent papers</span>'
      '<span class="cov-v">How the underlying examinable concept behaves over MIW&rsquo;s '
      'governed horizon. Qualitative on purpose: no count and no year is claimed.</span></div>')
    # THE SENTENCE THIS PAGE CANNOT SHIP WITHOUT.
    #
    # 55 of these 198 questions read READY_TO_STUDY_NOW and therefore render
    # "No currentness risk flagged". That readiness is inherited from the
    # question's recurrence FAMILY, and the family's answer lives on a solved
    # paper from a later year. On a page whose header says MIW has not solved
    # these papers, an unqualified all-clear chip reads as "this one is fine to
    # study" -- and there is nothing here to study. The chips are correct; what
    # they are ABOUT has to be stated once, plainly, or the page contradicts its
    # own heading. ARCHIVE-M refuses the page without it.
    a('  <div class="cov-row"><span class="cov-k">No currentness risk flagged &middot; '
      'Current answer verified &middot; Currentness check pending &middot; Answer under '
      'currentness review</span>'
      '<span class="cov-v"><b>These describe MIW&rsquo;s answer to the CONCEPT, on a later '
      'solved paper &mdash; never this %d question.</b> None of the questions on this page has '
      'been answered by MIW. A concept that recurred here and was later set again in a year MIW '
      'has solved carries the readiness of THAT answer, which is why an all-clear can appear '
      'beside a question with no answer behind it.</span></div>' % year)
    a('  <div class="cov-row"><span class="cov-k">Current-framework answer in preparation</span>'
      '<span class="cov-v">MIW holds no current answer to this concept yet. That is a '
      'statement about MIW, not about the question.</span></div>')
    a('  <div class="cov-row"><span class="cov-k">Current framework: see &hellip;</span>'
      '<span class="cov-v">A governed review has found that a <i>later</i> solved question '
      'covers what this one asks, and names it. <b>It does not mean this %d question has been '
      'answered.</b> It means the concept has a current home elsewhere in the corpus.</span>'
      '</div>' % year)
    # THE SECOND SENTENCE THIS PAGE CANNOT SHIP WITHOUT, added with the
    # current-answer library on 2026-08-24.
    #
    # A link is louder than a chip. Everything else on this page is a
    # description; this one is a door, and a candidate who walks through it
    # lands on a full model answer. On a page whose header says MIW has not
    # solved these papers, an unexplained door reads as the solution to the
    # question beside it -- so what is on the other side has to be stated
    # before the link is offered. It is NOT this question answered. It is
    # MIW's own present-day answer to the CONCEPT, written to no sitting and
    # carrying a review date instead of an examination date.
    a('  <div class="cov-row"><span class="cov-k">Current framework answer &rarr;</span>'
      '<span class="cov-v">MIW holds a <b>present-day</b> answer to the concept this question '
      'examines, and the link opens it. <b>This %d question has still not been solved.</b> '
      'What is on the other side is not a past paper and never was: it has no sitting, no '
      'printed serial and no printed marks, it was set by no examiner, and it answers '
      '&ldquo;what should I write about this <i>now</i>&rdquo; rather than &ldquo;what was '
      'correct at this sitting&rdquo;. It carries a review date for exactly that reason.</span>'
      '</div>' % year)
    # A multi-part question is not owned by one answer, and pretending otherwise
    # would send a candidate asked for three concepts to an answer about one.
    # Where the parts are answered in different places the chips say so
    # part by part -- which also makes it visible when only SOME parts are
    # covered, instead of a single reassuring link hiding the gap.
    a('  <div class="cov-row"><span class="cov-k">A. &hellip; &middot; B. &hellip; &mdash; one '
      'chip per part</span>'
      '<span class="cov-v">Where a question asks for several independent things, MIW answers '
      'them <i>separately</i> and each part is routed on its own &mdash; some to a current '
      'framework answer, some to a later solved question that covers that part. Read the parts '
      'you are offered: a part with no chip is a part MIW does not yet answer, and the absence '
      'is deliberate rather than an oversight.</span></div>')
    a('</section>')

    for mn in range(1, 13):
        month = RM.MONTHS[mn - 1]
        a('<section class="topic-group" data-month-block="%d">' % mn)
        if mn in months:
            for p in months[mn]:
                a('  <h3>%s <span class="q-tag sub">Question wording held</span></h3>'
                  % esc(p['sitting'] + (' (second sitting)' if p.get('second_sitting') else '')))
                bits = [('printed serial %s' % p['printed_serial']) if p.get('printed_serial')
                        else 'no printed serial on the source copy',
                        p.get('time_allowed') or '',
                        ('%s marks printed as the paper total' % p['total_marks'])
                        if p.get('total_marks') else '',
                        '%d question%s printed' % (len(p['questions']),
                                                   '' if len(p['questions']) == 1 else 's')]
                a('  <div class="tg-sub">%s</div>'
                  % ' &middot; '.join(esc(b) for b in bits if b))
                a('  <div class="rec-note"><b>No solved answer.</b> MIW holds the printed '
                  'wording for this sitting and has not answered it.</div>')
                for q in p['questions']:
                    _render_archive_question(a, p, q)
        elif (year, mn) in KNOWN_ABSENT:
            a('  <h3>%s %d <span class="q-tag sub">No sitting</span></h3>' % (esc(month), year))
            a('  <div class="rec-note"><strong>No examination paper exists for this month.'
              '</strong> %s</div>' % KNOWN_ABSENT[(year, mn)])
        else:
            a('  <h3>%s %d <span class="q-tag sub">Not yet in the MIW set</span></h3>'
              % (esc(month), year))
            a('  <div class="rec-note">MIW holds no source copy for this sitting. That is a '
              'statement about MIW&rsquo;s shelf, not about whether the examination was '
              'held.</div>')
        a('</section>')

    a('</main>')
    a('<script>')
    a(_archive_js())
    a('</script>')
    o.extend(footer(publish or deliver))
    a('</body>')
    a('</html>')
    return '\n'.join(o) + '\n'


def _render_archive_question(a, paper, q):
    a('  <div class="hit" data-qsearch="%s" id="%s">'
      % (esc_attr(_archive_search_tokens(paper, q)), esc_attr(q['question_id'])))
    a('    <div class="hit-top">%s <span class="sep">&middot;</span> %s '
      '<span class="sep">&middot;</span> marks not printed per question</div>'
      % (esc(paper['sitting']), esc(q['q_no'])))
    for line in q['text_verbatim'].split('\n'):
        a('    <div class="q-stem">%s</div>' % esc(line))
    for limb in q.get('printed_limbs') or []:
        a('    <div class="q-stem">%s</div>'
          % esc(limb if isinstance(limb, str)
                else json.dumps(limb, ensure_ascii=False)))
    # The governed projection, and nothing else. No Layer-1 tag: see the note at
    # the top of this section.
    block = QIP.render_block(q['question_id'], audience='GATED')
    if block:
        a('    %s' % block)
    a('  </div>')

def write(path, text):
    prev = open(path, encoding='utf-8', newline='').read() if os.path.exists(path) else None
    with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    return 'IDENTICAL' if prev == text else ('CHANGED' if prev is not None else 'NEW')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--publish', action='store_true')
    ap.add_argument('--year', type=int, default=None,
                    help='Restrict to one year. Default: every year that has a spec.')
    ap.add_argument('--deliver', action='store_true',
                    help='write the paid /solvedQP/ projection instead')
    args = ap.parse_args()

    specs = load_specs()
    if not specs:
        print('ERROR: no specs found under %s' % SPEC_GLOB)
        sys.exit(1)

    archive = load_archive()
    arc_years = archive_years(specs, archive)

    if args.year:
        years = [args.year]
    elif args.deliver:
        # The delivery surface carries a sheet for each year that has a solved
        # paper. A year holding only transcriptions is not part of the paid
        # product, so it gets no delivered sheet. Derived, never listed.
        years = sorted({d['year'] for d in specs
                        if any(q.get('model_answer') for q in d['questions'])})
    else:
        years = sorted({d['year'] for d in specs})

    # The archive years join the SAME chronology. They are not a second product
    # and they are not a separate URL shape: a candidate reading questions-2023
    # should be able to walk back to questions-2022 without learning a new
    # convention. What differs is the page, not the address -- and the page says
    # in its first paragraph that MIW has not solved it.
    #
    # `--year` is honoured for both sets, so a single archive year can be
    # rebuilt on its own. It cannot conjure one: a year absent from the archive
    # store and from the specs simply produces nothing.
    if args.year:
        arc_years = [args.year] if args.year in arc_years else []
        years = [y for y in years if y in {d['year'] for d in specs}]

    for year in years + arc_years:
        is_archive = year in arc_years
        if args.deliver:
            path = os.path.join(REPO_ROOT, 'solvedQP', 'questions-%d.html' % year)
            os.makedirs(os.path.dirname(path), exist_ok=True)
        else:
            path = os.path.join(PP_DIR, 'questions-%d.html' % year)
        text = (build_archive_year_page(archive, year, args.publish, deliver=args.deliver)
                if is_archive
                else build_year_page(specs, year, args.publish, deliver=args.deliver))
        st = write(path, text)
        print('%squestions-%d.html  %s%s'
              % ('solvedQP/' if args.deliver else '', year, st,
                 '  (wording archive)' if is_archive else ''))


if __name__ == '__main__':
    main()
