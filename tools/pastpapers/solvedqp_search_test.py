#!/usr/bin/env python3
"""Deterministic tests for the Solved QP topic search.

Usage: python tools/pastpapers/solvedqp_search_test.py

WHAT IS UNDER TEST
------------------
The search that ships is twelve lines of JavaScript over the manifest's
precomputed `search_text`. Almost all of its behaviour is therefore a property
of the MANIFEST, not of the browser: which questions are findable, what they
are folded to, and what is deliberately absent. That is what these tests
assert, in Python, against the real generated file -- no browser, no fixture
corpus, no second copy of the data.

The one thing they cannot assert is that the browser wires the box to the
payload. That is covered by the live UI review, and by the health check's
search-integrity block which proves every result target resolves.

Terms are chosen from the actual solved corpus, not invented, so a term that
stops matching is a real product regression rather than a stale fixture.

Exit 1 on any failure.
"""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
MANIFEST = os.path.join(REPO_ROOT, 'solvedQP', 'solvedqp_content_index.json')

fails = []
PASSED = [0]


def check(name, cond, detail=''):
    print('  [ %-4s ] %s%s' % ('OK' if cond else 'FAIL', name,
                               ('  -- %s' % detail) if detail else ''))
    if cond:
        PASSED[0] += 1
    else:
        fails.append(name)


def fold(s):
    """The browser's fold(), reimplemented exactly.

    Kept deliberately tiny and identical to the JavaScript in
    build_solvedqp_home.SEARCH_JS. The heavy normalisation lives once, in
    build_solvedqp_manifest.norm_search, and is baked into search_text -- so
    this only has to agree about case, punctuation and whitespace.
    """
    return re.sub(r'\s+', ' ', re.sub(r"[^a-z0-9'&]+", ' ', s.lower())).strip()


def search(m, q):
    """Same matching rule as the page: every term must appear in search_text."""
    terms = [t for t in fold(q).split(' ') if t]
    if not terms:
        return []
    hits = []
    for p in m['papers']:
        if p['status'] != 'AVAILABLE':
            continue
        for x in p['questions']:
            t = x.get('search_text') or ''
            if all(w in t for w in terms):
                hits.append((p['paper_id'], p['sitting'], x['question_number'], x['href']))
    return hits


def main():
    if not os.path.exists(MANIFEST):
        print('manifest missing -- run build_solvedqp_manifest.py first')
        return 1
    m = json.loads(io.open(MANIFEST, encoding='utf-8').read())
    print('SOLVEDQP SEARCH TESTS  (%d question(s) across %d solved sitting(s))'
          % (m['available_questions'], m['available_papers']))

    # --- multi-paper topic: the Founder's worked example --------------------
    psc = search(m, 'Port State Control')
    check('"Port State Control" spans several sittings',
          len({h[0] for h in psc}) >= 3, '%d paper(s), %d question(s)'
          % (len({h[0] for h in psc}), len(psc)))
    check('"Port State Control" finds the December 2025 detention question',
          ('QP2512', 'December 2025', 'Q8', '/solvedQP/QP2512.html#q8') in psc)

    # --- case and punctuation ----------------------------------------------
    check('search is case-insensitive',
          search(m, 'PORT STATE CONTROL') == psc)
    check('punctuation and spacing are ignored',
          search(m, '  port-state,  control ') == psc)

    # --- a second real multi-paper topic ------------------------------------
    ga = search(m, 'general average')
    check('"general average" is a multi-paper family',
          len({h[0] for h in ga}) >= 3, '%d paper(s)' % len({h[0] for h in ga}))

    # --- alias / tag reach, not just the printed stem -----------------------
    # MLC is carried in tags and aliases; the printed stems mostly spell it out.
    mlc = search(m, 'MLC')
    check('an abbreviation in the tag layer still matches', len(mlc) >= 2,
          '%d question(s)' % len(mlc))

    # --- single result -------------------------------------------------------
    singles = [q for p in m['papers'] if p['status'] == 'AVAILABLE'
               for q in p['questions']]
    uniq = None
    for q in singles:
        term = q['short_title']
        if len(search(m, term)) == 1:
            uniq = (term, q['question_id'])
            break
    check('a specific title returns exactly one question', uniq is not None,
          '%s -> %s' % uniq if uniq else 'no single-hit title found')

    # --- no result -----------------------------------------------------------
    check('a term with no match returns nothing',
          search(m, 'zzzqqq nonexistent topic') == [])

    # --- paper / year terms --------------------------------------------------
    check('paper metadata is NOT in the question payload',
          search(m, 'QP2512') == [],
          'sitting is a grouping, not a search term -- results are grouped by '
          'paper in the UI')

    # --- THE BOUNDARY TESTS --------------------------------------------------
    planned_ids = {p['paper_id'] for p in m['papers'] if p['status'] == 'PLANNED_SOON'}
    all_hits = set()
    for term in ('port state control', 'general average', 'marpol', 'insurance',
                 'ism', 'stcw', 'survey', 'a', 'e'):
        all_hits |= {h[0] for h in search(m, term)}
    # This assertion is only meaningful while an unsolved sitting exists. The
    # 2024-2026 corpus is now fully solved, so on today's data it passes
    # VACUOUSLY -- there is nothing for it to catch. Saying so is the point:
    # a green line that tests nothing is how a suite quietly stops protecting
    # the thing it was written for. The property itself stays under test on the
    # synthetic fixture below, which owns a PLANNED_SOON paper permanently.
    if planned_ids:
        check('no unsolved sitting can ever appear in a result',
              not (all_hits & planned_ids),
              'checked %d planned paper(s) against 9 broad terms' % len(planned_ids))
    else:
        print('  [ n/a  ] no unsolved sitting can ever appear in a result  -- '
              'VACUOUS on live data (0 PLANNED_SOON sittings); the property is '
              'held by the synthetic fixture instead')

    blob = io.open(MANIFEST, encoding='utf-8').read()
    check('the search payload contains no worked-answer field',
          not any('"%s"' % k in blob for k in
                  ('model_answer', 'study_notes', 'quick_revision', 'answer_route',
                   'retrieval_cards', 'memory_cue')))
    check('the search payload contains no authoring field',
          not any('"%s"' % k in blob for k in
                  ('recurrence_class', 'host_recurrence_hint', 'reuse_tier',
                   'verification_status')))

    # --- every hit is reachable ---------------------------------------------
    bad = [h for h in psc + ga
           if not os.path.exists(os.path.join(
               REPO_ROOT, h[3].lstrip('/').split('#')[0].replace('/', os.sep)))]
    check('every result links to a file that exists', not bad, str(bad[:2]))

    corpus_fallback_tests(m)
    updates_tests(m)
    wiring_tests()

    print('%d passed, %d failed' % (PASSED[0], len(fails)))
    return 1 if fails else 0


# =====================================================================
# CORPUS FALLBACK -- tested on a SYNTHETIC fixture, on purpose
# =====================================================================
#
# The behaviour under test is "a scope with no hits must still reach the hits
# that exist elsewhere". Asserting that against the live corpus would mean
# picking a term that happens to be absent from one real paper today -- and the
# moment someone solves a paper containing it, the test either breaks or, worse,
# passes vacuously because the scoped search now finds something.
#
# That is the exact failure this repository has already had: fixtures harvested
# from live corpus state stopped testing anything when PLANNED_SOON disappeared
# and when the last unsolved question was solved. So the fixture below is built
# by hand, is not derived from any spec, and cannot be invalidated by production.
FIXTURE = {
    'available_questions': 4, 'available_papers': 2,
    'papers': [
        {'paper_id': 'QPX001', 'sitting': 'January 2099', 'sr_no': 'QP-X001',
         'year': 2099, 'status': 'AVAILABLE', 'href': '/solvedQP/QPX001.html',
         'questions': [
             {'question_id': 'QPX001-Q1', 'question_number': 'Q1', 'anchor': 'q1',
              'href': '/solvedQP/QPX001.html#q1', 'short_title': 'Widget survey',
              'search_text': 'widget survey annual', 'topic_tags': ['Widgets'],
              'primary_category': 'Widgets'},
             {'question_id': 'QPX001-Q2', 'question_number': 'Q2', 'anchor': 'q2',
              'href': '/solvedQP/QPX001.html#q2', 'short_title': 'Widget records',
              'search_text': 'widget records', 'topic_tags': ['Widgets'],
              'primary_category': 'Widgets'}]},
        {'paper_id': 'QPX002', 'sitting': 'February 2099', 'sr_no': 'QP-X002',
         'year': 2099, 'status': 'AVAILABLE', 'href': '/solvedQP/QPX002.html',
         'questions': [
             {'question_id': 'QPX002-Q1', 'question_number': 'Q1', 'anchor': 'q1',
              'href': '/solvedQP/QPX002.html#q1', 'short_title': 'Sprocket limits',
              'search_text': 'sprocket limitation fund', 'topic_tags': ['Sprockets'],
              'primary_category': 'Sprockets'}]},
        {'paper_id': 'QPX003', 'sitting': 'March 2099', 'sr_no': 'QP-X003',
         'year': 2098, 'status': 'PLANNED_SOON', 'question_count': 9,
         'questions': []},
    ],
}


def fixture_match(m, q, exclude_paper=None, exclude_year=None):
    """MIWCorpus.match(), reimplemented. Same AND-over-folded-terms rule."""
    terms = [t for t in fold(q).split(' ') if t]
    groups = []
    for p in m['papers']:
        if p['status'] != 'AVAILABLE' or not p['questions']:
            continue
        if exclude_paper and p['paper_id'] == exclude_paper:
            continue
        if exclude_year is not None and p.get('year') == exclude_year:
            continue
        hits = [x for x in p['questions']
                if terms and all(w in (x.get('search_text') or '') for w in terms)]
        if hits:
            groups.append((p, hits))
    return groups


def corpus_fallback_tests(live):
    print('\nCORPUS FALLBACK  (synthetic fixture -- immune to corpus growth)')
    f = FIXTURE

    # THE critical journey, stated as a property rather than as today's data:
    # a term absent from the paper the reader is in, present elsewhere.
    scoped = fixture_match(f, 'sprocket', exclude_paper=None)
    in_paper = [g for g in scoped if g[0]['paper_id'] == 'QPX001']
    broadened = fixture_match(f, 'sprocket', exclude_paper='QPX001')
    check('scoped search finds nothing in the reader\'s own paper', not in_paper)
    check('broadening from that paper finds the real matches elsewhere',
          sum(len(h) for _, h in broadened) == 1,
          '%d hit(s) in %d paper(s)' % (sum(len(h) for _, h in broadened),
                                        len(broadened)))
    check('the reader\'s own paper is excluded from the broadened results',
          all(g[0]['paper_id'] != 'QPX001' for g in broadened))

    # Year sheet: same property on the year axis.
    y = fixture_match(f, 'widget', exclude_year=2099)
    check('excluding the reader\'s year removes that year\'s hits', not y)
    check('without the year exclusion the same term does match',
          sum(len(h) for _, h in fixture_match(f, 'widget')) == 2)

    # Multi-term AND, order independent -- the property the whole matcher rests on.
    check('all terms must match (AND, not OR)',
          not fixture_match(f, 'widget sprocket'))
    check('term order does not matter',
          [g[0]['paper_id'] for g in fixture_match(f, 'fund limitation')] ==
          [g[0]['paper_id'] for g in fixture_match(f, 'limitation fund')])

    # NEGATIVE CONTROL, synthetic: a planned sitting is in the fixture with
    # questions:[] and must stay unreachable however broad the term.
    allhits = set()
    for t in ('widget', 'sprocket', 'a', 'survey', 'fund'):
        allhits |= {g[0]['paper_id'] for g in fixture_match(f, t)}
    check('a PLANNED_SOON sitting is unreachable from any term',
          'QPX003' not in allhits)

    # Deep-link construction, asserted as a rule and then against live data.
    check('fixture hrefs are paper + anchor',
          all(x['href'] == '/solvedQP/%s.html#%s' % (p['paper_id'], x['anchor'])
              for p in f['papers'] for x in p['questions']))
    live_bad = [x for p in live['papers'] for x in p['questions']
                if x['href'] != '/solvedQP/%s.html#%s' % (x['paper_id'], x['anchor'])]
    check('every live result deep-links to a question anchor, never a storefront',
          not live_bad, str(live_bad[:1]))


# =====================================================================
# UPDATES -- the maintenance ledger
# =====================================================================

def updates_tests(m):
    print('\nUPDATES LEDGER')
    sys.path.insert(0, HERE)
    from build_solvedqp_manifest import VALID_KINDS, KIND_LABEL
    from build_solvedqp_home import preview_updates, UPDATES_SHOWN

    ru = m.get('recently_updated') or []
    check('the manifest carries a change ledger', bool(ru), '%d record(s)' % len(ru))
    check('every record uses the controlled vocabulary',
          all(r['kind'] in VALID_KINDS for r in ru),
          str(sorted({r['kind'] for r in ru} - set(VALID_KINDS))))
    check('every kind has a candidate-facing label',
          all(r['kind'] in KIND_LABEL for r in ru))

    keys = [(r['date'], r['paper_id']) for r in ru]
    check('the ledger is newest-first and totally ordered',
          keys == sorted(keys, reverse=True))
    check('every record carries a date, a sitting and a summary',
          all(re.fullmatch(r'\d{4}-\d{2}-\d{2}', r['date']) and r['sitting']
              and r['summary'].strip() for r in ru))

    # The whole point of the backfill: a ledger that only ever says "added" is
    # a release feed. This asserts the product property, not a specific count.
    maint = [r for r in ru if r['kind'] != 'added']
    check('the ledger records maintenance, not only new sittings',
          len(maint) > 0, '%d maintenance record(s) of %d' % (len(maint), len(ru)))
    check('corrections name the questions they touched',
          all(r['questions'] for r in ru if r['kind'] == 'corrected'))

    # Preview selection: a single integration batch must not be able to fill
    # every slot and hide the corrections underneath.
    prev = preview_updates(ru)
    check('the preview shows at most the configured number of rows',
          len(prev) <= UPDATES_SHOWN, '%d row(s)' % len(prev))
    check('the preview is still in date order',
          [(r['date'], r['paper_id']) for r in prev] ==
          sorted([(r['date'], r['paper_id']) for r in prev], reverse=True))
    if maint:
        check('the preview is not monopolised by "added"',
              any(r['kind'] != 'added' for r in prev),
              str(sorted({r['kind'] for r in prev})))
    check('every previewed record is a real record from the ledger',
          all(p in ru for p in prev))

    # EMPTY STATE, synthetic -- a corpus with no changes must not crash the
    # selector or invent a row.
    check('an empty ledger previews as nothing', preview_updates([]) == [])
    only_added = [r for r in ru if r['kind'] == 'added'][:3]
    check('a ledger with only additions still previews',
          len(preview_updates(only_added)) == len(only_added))

    # No internal vocabulary may reach a candidate-facing summary.
    banned = ('commit', 'branch', 'Founder', 'Claude', 'main', 'merge', 'spec ',
              'toolchain', 'QP2', 'defect', 'referral', 'batch')
    leaks = [(r['paper_id'], w) for r in ru for w in banned
             if w.lower() in r['summary'].lower()]
    check('no summary leaks internal production vocabulary', not leaks,
          str(leaks[:3]))


# =====================================================================
# WIRING -- the built pages actually carry the behaviour
# =====================================================================

def wiring_tests():
    print('\nPAGE WIRING  (built delivery HTML)')
    def read(rel):
        p = os.path.join(REPO_ROOT, rel.replace('/', os.sep))
        return io.open(p, encoding='utf-8').read() if os.path.exists(p) else ''

    home = read('solvedQP/index.html')
    paper = read('solvedQP/QP2607.html')
    year = read('solvedQP/questions-2026.html')
    review = read('meoclass1/pastpapers/QP2607.html')

    check('home carries the shared matcher', 'window.MIWCorpus' in home)
    check('paper page carries the shared matcher', 'window.MIWCorpus' in paper)
    check('year sheet carries the shared matcher', 'window.MIWCorpus' in year)
    check('paper page carries the corpus fallback panel', 'id="mc-wrap"' in paper)
    check('year sheet carries the corpus fallback panel', 'id="mc-wrap"' in year)
    check('paper page declares its own id so it can exclude itself',
          'data-paper-id="QP2607"' in paper)
    check('year sheet declares its own year', 'data-year="2026"' in year)
    check('home search is sticky', '.sq-find{position:sticky' in home)

    # ---- sticky geometry must not depend on scroll position ----------------
    # The sticky block used to hide its chips and hint and cut its padding once
    # a sentinel crossed the top of the viewport. Because a sticky element
    # keeps its flow box, that shrank the document by 105px, Chrome's scroll
    # anchoring gave the 105px back by moving scrollTop, and the move pushed
    # the sentinel back across the threshold -- so the page oscillated between
    # two scroll positions (measured: 520 -> 415 -> 520) for as long as the
    # reader rested in that band.
    #
    # These four assertions are the shape of the fix, not the symptom: the
    # sticky element must contain only the field and its results, the browse
    # affordances must live outside it, and nothing may recompute a class from
    # a scroll position. Any one of them failing re-opens the feedback loop.
    check('the browse affordances are OUTSIDE the sticky element',
          '<section class="sq-findfoot">' in home
          and home.index('<div class="sq-find">')
              < home.index('<section class="sq-findfoot">'))
    check('the chips and hint sit in the foot, not the sticky block',
          '.sq-findfoot.has-q .sq-chips' in home
          and '.sq-find.has-q' not in home)
    check('no scroll-position class changes the sticky block',
          '.sq-find.is-stuck{' not in home
          and '.sq-find.is-stuck .sq-chips' not in home)
    check('the stuck detector and its sentinel are gone',
          '__miwSyncStuck' not in home and "'is-stuck'" not in home)
    # Exactly one scroll listener may exist: the back-to-top control, which is
    # position:fixed and therefore out of document flow, so nothing it does can
    # move the page under the reader. The count is pinned rather than the
    # behaviour because the danger is not this handler -- it is the NEXT one.
    # A second scroll listener has to be added deliberately, past this line.
    check('the only scroll listener is the out-of-flow back-to-top control',
          home.count("addEventListener('scroll'") == 1
          and 'addEventListener("scroll"' not in home
          and '.sq-top{position:fixed' in home)
    check('home reads a ?q= deep link', "URLSearchParams" in home)
    check('home offers the full update log', 'id="sq-upd-btn"' in home)
    check('home offers topic discovery', 'class="sq-chip"' in home)

    # The review copy under /meoclass1/pastpapers/ must NOT reach into the paid
    # delivery surface -- a reviewer is not a customer and the manifest is not
    # theirs. This is the one place the two builds must differ.
    check('the review copy does NOT carry the delivery corpus panel',
          'id="mc-wrap"' not in review)

    # The payload the fallback fetches is public-by-download, so the boundary
    # is asserted here as well as in the manifest generator's own self-test.
    check('the fallback fetches only the guarded manifest',
          paper.count("'/solvedQP/solvedqp_content_index.json'") >= 1 or
          '/solvedQP/solvedqp_content_index.json' in paper)


if __name__ == '__main__':
    sys.exit(main())
