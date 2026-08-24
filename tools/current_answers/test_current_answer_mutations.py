#!/usr/bin/env python3
"""Prove the current-answer gate actually bites.

    python tools/current_answers/test_current_answer_mutations.py

A validator nobody has attacked is a validator that passes. Each mutation below
corrupts an in-memory COPY of the gate's bundle in one specific way, runs the
gate over it, and requires the NAMED rule to fail. Nothing is written to disk,
so a crash mid-suite cannot leave a mutation behind -- and the suite proves that
too by re-running the gate clean at the end and requiring zero residue.

The list is the fourteen mutations the Founder brief specified, plus seven the
architecture made possible and that would otherwise be untested: untyped library
ownership, whole-and-limb ownership at once, a limb answer promoted to a
whole-question owner, a page that drops its own disclaimer, an entry that grows
a sitting field, a marks band with no basis, and a library owner that is not
verified and therefore has no page to route to.
"""

import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import validate_current_answers as V     # noqa: E402


def _entry(B, i='CA-EM-0001'):
    return B['entries'][i]


def _fam(B, fid):
    for r in B['fams']:
        if r['family_id'] == fid:
            return r
    raise KeyError(fid)


# Each mutation: (id, description, rule that must fail, mutate(B))
MUTATIONS = [
    # ---------------------------------------------------------------- 1 - 5
    (1, 'duplicate current-answer id on disk', 'R-CA-ID-UNIQUE',
     lambda B: B['filed'].append(('CA-EM-0002.json', 'CA-EM-0001'))),

    (2, 'a current answer given a past-paper id', 'R-CA-ID-GRAMMAR',
     lambda B: B['entries'].__setitem__('QP2101-Q4',
                                        B['entries'].pop('CA-EM-0001'))),

    (3, 'a current answer linked to no QI family', 'R-CA-FAMILY',
     lambda B: _entry(B).__setitem__('family_ids', [])),

    (4, 'a verified answer with its authority removed', 'R-CA-AUTHORITY',
     lambda B: _entry(B).__setitem__('authority_sources', [])),

    (5, 'a verified answer with no independent review', 'R-CA-REVIEW',
     lambda B: _entry(B).__setitem__('review_record', {})),

    # ---------------------------------------------------------------- 6 - 7
    # The two that would corrupt the product's central claim: that every
    # recurrence number is a count of what examiners actually set.
    (6, 'a current answer counted as a recurrence occurrence',
     'R-CA-NO-RECURRENCE',
     lambda B: B['qi_occ']['occurrences'].append(
         {'occurrence_id': 'CA-EM-0001', 'sitting': '2026-08'})),

    (7, 'a current answer entered as examiner evidence', 'R-CA-NO-EXAMINER',
     lambda B: B['examiner'].__setitem__(
         'meoclass1/qb_content_index.json',
         '{"examiner": "CA-EM-0001"}')),

    # ---------------------------------------------------------------- 8 - 9
    (8, 'a family naming a library entry that does not exist',
     'R-CA-OWNER-RESOLVES',
     lambda B: _fam(B, 'QIF-EM-0014')['canonical_current_answer']
     .__setitem__('owner_id', 'CA-EM-9999')),

    (9, 'one verified limb promoted to answer the whole question',
     'R-CA-LIMB-SLOT',
     lambda B: _fam(B, 'QIF-EM-0052').__setitem__(
         'canonical_current_answer',
         {'owner_type': 'CURRENT_LIBRARY', 'owner_id': 'CA-EM-0002'})),

    # --------------------------------------------------------------- 10 - 11
    (10, 'the archive calling a current answer a solved answer',
     'R-CA-ARCHIVE-LABEL',
     lambda B: B['archive_pages'].__setitem__(
         'meoclass1/pastpapers/questions-2021.html',
         B['archive_pages']['meoclass1/pastpapers/questions-2021.html']
         .replace('Current framework answer &rarr;', 'Solved answer &rarr;'))),

    (11, 'the gated route dropped from the middleware matcher',
     'R-CA-GATED-MATCHER',
     lambda B: B.__setitem__('middleware',
                             B['middleware'].replace('/solvedQP/:path*', ''))),

    # --------------------------------------------------------------- 12 - 14
    (12, 'a sitting-anchored past-paper answer modernised to cite a current '
         'answer', 'R-CA-SPEC-ANSWER-CLEAN',
     lambda B: B['specs']['QP2304']['questions'][0]
     .__setitem__('model_answer',
                  {'blocks': [{'p': 'See CA-EM-0001 for the current position.'}]})),

    (13, 'the registry left stale after a current answer was created',
     'R-CA-REGISTRY-FRESH',
     lambda B: B['registry']['entries'].pop()),

    (14, 'a current answer stripped of its version history', 'R-CA-VERSION',
     lambda B: _entry(B).__setitem__('version_history', [])),

    # --------------------------------------------------------------- 15 - 21
    # Not in the brief. Reachable only because typed, limb-level ownership
    # exists, so untested is exactly what they would otherwise be.
    (15, 'a library owner written in the untyped legacy shape',
     'R-CA-OWNER-TYPED',
     lambda B: _fam(B, 'QIF-EM-0014').__setitem__(
         'canonical_current_answer', {'question_id': 'CA-EM-0001'})),

    (16, 'a family owned whole AND limb by limb at the same time',
     'R-CA-OWNERSHIP-EXCLUSIVE',
     lambda B: _fam(B, 'QIF-EM-0052').__setitem__(
         'canonical_current_answer',
         {'owner_type': 'CURRENT_LIBRARY', 'owner_id': 'CA-EM-0003'})),

    (17, 'a page that drops its own not-a-past-paper statement',
     'R-CA-PAGE-DISCLAIMS',
     lambda B: B['pages'].__setitem__(
         'CA-EM-0001',
         B['pages']['CA-EM-0001'].replace('not a past-paper question', 'x'))),

    (18, 'a page that claims to be a solved paper', 'R-CA-NO-FAKE-SITTING',
     lambda B: B['pages'].__setitem__(
         'CA-EM-0001', B['pages']['CA-EM-0001'] + '<a>Open the solved answer</a>')),

    (19, 'an entry that grows a sitting field', 'R-CA-NO-SITTING',
     lambda B: _entry(B).__setitem__('month_year', 'August 2026')),

    (20, 'a marks band presented as a printed mark', 'R-CA-MARKS-BASIS',
     lambda B: _entry(B)['recommended_exam_depth']
     .__setitem__('basis', 'PRINTED_ON_SOURCE_COPY')),

    (21, 'a family routing to a library entry that was never verified',
     'R-CA-OWNER-RENDERABLE',
     lambda B: _entry(B).__setitem__('review_status', 'DRAFT')),

    (22, 'a rendered page named like a past-paper question', 'R-CA-ID-NOT-QP',
     lambda B: B['pages'].__setitem__('QP2101-Q4', B['pages']['CA-EM-0001'])),
]


def run_gate(B):
    """Run the gate over a bundle and return {rule: ok}."""
    V.RESULTS = []
    V.run_checks(B)
    return {r: ok for r, ok, _d in V.RESULTS}


def main():
    base = V.load_bundle()

    clean = run_gate(copy.deepcopy(base))
    failed_clean = sorted(r for r, ok in clean.items() if not ok)
    if failed_clean:
        print('ABORT: the gate does not pass before any mutation: %s'
              % failed_clean)
        return 1
    print('baseline: %d invariants, all clean\n' % len(clean))

    caught, escaped = 0, []
    for mid, desc, rule, mutate in MUTATIONS:
        B = copy.deepcopy(base)
        try:
            mutate(B)
        except Exception as exc:                       # pragma: no cover
            print('  ERROR    %-2d %-52s -> mutation itself failed: %s'
                  % (mid, desc[:52], exc))
            escaped.append((mid, rule))
            continue
        res = run_gate(B)
        if res.get(rule) is False:
            caught += 1
            print('  CAUGHT   %-2d %-52s -> %s' % (mid, desc[:52], rule))
        else:
            escaped.append((mid, rule))
            state = ('PASSED' if res.get(rule) else 'RULE ABSENT')
            print('  ESCAPED  %-2d %-52s -> %s %s'
                  % (mid, desc[:52], rule, state))

    # RESIDUE. The suite mutates copies, so disk should be untouched -- but
    # "should be" is what a residue check is for. Re-read from disk and require
    # the gate clean again.
    after = run_gate(V.load_bundle())
    residue = sorted(r for r, ok in after.items() if not ok)

    print('\ncaught %d / %d   escaped %d   residue %d'
          % (caught, len(MUTATIONS), len(escaped), len(residue)))
    if escaped:
        print('ESCAPED: %s' % escaped)
    if residue:
        print('RESIDUE: %s' % residue)
    if escaped or residue:
        return 1
    print('all mutations caught, zero escapes, zero residue.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
