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


def check(name, cond, detail=''):
    print('  [ %-4s ] %s%s' % ('OK' if cond else 'FAIL', name,
                               ('  -- %s' % detail) if detail else ''))
    if not cond:
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
    check('no unsolved sitting can ever appear in a result',
          not (all_hits & planned_ids),
          'checked %d planned paper(s) against 9 broad terms' % len(planned_ids))

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

    print('%d/%d' % (13 - len(fails), 13))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
