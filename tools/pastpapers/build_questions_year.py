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
                           topbar, head_meta, footer, GATE_STUB, DELIVERY_LINKS)
import recurrence_model as RM

PP_DIR = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')
SPEC_GLOB = os.path.join(PP_DIR, 'specs', '*.json')

# Sittings that are known NOT to exist, with the evidence for saying so. This is
# a much stronger statement than "we have not built it yet", and the two must
# never render the same way: one is a fact about the examination, the other is a
# fact about MIW's backlog. Keyed (year, month_number).
KNOWN_ABSENT = {
    (2026, 5): 'No May sitting appears in the MIW source set, and the examiner&rsquo;s own '
               'serial numbering skips it in 2025 as well &mdash; the 2025 serials run '
               '&hellip;2504, 2506&hellip; with nothing at 2505.',
    (2025, 5): 'No May sitting. The examiner&rsquo;s serial numbering runs &hellip;2504, '
               '2506&hellip; with nothing at 2505.',
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
    """Filter + search. Plain DOM work over generated attributes."""
    return """
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
  }

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
    # generator, same specs, same recurrence model — only the canonical
    # URL and the navigation change. There is deliberately no second,
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
    a('<body>')
    a(GATE_STUB)
    a('<a class="skip" href="#qy-main">Skip to content</a>')
    o.extend(topbar('Questions by year' if deliver else '',
                    links=DELIVERY_LINKS if deliver else None))
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
    # banner — same rule as the papers. It stays noindex via publish=False.
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
    a('  <div class="cov-row"><span class="cov-k">Set once</span>'
      '<span class="cov-v">Set once across the sittings MIW has transcribed. That is not the '
      'same as never asked before &mdash; MIW has transcribed %s so far.</span></div>'
      % esc(_scope_phrase(specs)))
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
    a('  <div class="hit" data-qsearch="%s" data-rec="%s" data-cat="%s" id="%s">'
      % (esc_attr(question_search_tokens(n, q, rel['label'])),
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
    a('    <div class="rec-note"><span class="q-tag rec">%s</span> %s</div>'
      % (rel['label'], RM.family_summary(nodes, relations, n['question_id'])))
    if solved:
        a('    <div class="btn-row"><a class="nav-btn" href="%s.html#%s">'
          'Open the solved answer &rarr;</a></div>'
          % (esc_attr(n['paper_id']), esc_attr(n['anchor'])))
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

    years = [args.year] if args.year else sorted({d['year'] for d in specs})
    for year in years:
        if args.deliver:
            path = os.path.join(REPO_ROOT, 'solvedQP', 'questions-%d.html' % year)
            os.makedirs(os.path.dirname(path), exist_ok=True)
        else:
            path = os.path.join(PP_DIR, 'questions-%d.html' % year)
        st = write(path, build_year_page(specs, year, args.publish, deliver=args.deliver))
        print('%squestions-%d.html  %s'
              % ('solvedQP/' if args.deliver else '', year, st))


if __name__ == '__main__':
    main()
