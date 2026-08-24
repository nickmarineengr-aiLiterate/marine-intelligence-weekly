#!/usr/bin/env python3
"""The owner-reader contract: what every consumer of typed ownership must do.

WHY THIS EXISTS
---------------
The gates refuse a badly-scoped ownership record -- `R-CA-OWNER-SLOT` and
`R-P2-OWNER-SLOT` -- so in a healthy repository the shapes exercised below never
reach a reader at all. That is precisely why this file exists. A gate is one
line of defence and it is the line that gets edited; the readers are the line
that gets FORGOTTEN, and twice now a reader has been found quietly misreading a
shape the store had only just learned to hold:

  * tranche 003 found `validate_study_qi.R-READY-SAFE` and the candidate
    projection guards still reading whole-question ownership only, months after
    limb ownership shipped;
  * this suite's own first run found `study_qi_adapter.question_readiness`
    granting a whole question READY_TO_STUDY_NOW from a SOLVED_PAPER_LIMB owner,
    and from an owner_type nothing in the repository recognises.

Neither was caught by a gate, because neither was a bad RECORD -- both were a
good record read badly. So this suite asserts the READER's behaviour directly,
owner type by owner type, on CONSTRUCTED inputs rather than on whichever
families happen to be owned which way today. A test that harvests its fixture
from the live corpus is a wasting asset: it passes for the wrong reason the
moment the corpus moves.

    python tools/current_answers/test_owner_reader_contract.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, 'tools', 'study'))

import ca_model as CA                      # noqa: E402
import study_qi_adapter as A               # noqa: E402
import qi_projection as P                  # noqa: E402
import validate_current_answers as VCA     # noqa: E402
import validate_phase2_tranche as VP2      # noqa: E402

Q = 'QP2606-Q8'          # a real solved question
SIB = 'QP2304-Q3'        # a real solved question, owned as a LIMB elsewhere
LIB = 'CA-EM-0001'       # a real, verified library entry

TRIAGE = 'VERIFY_CURRENT_ANSWER'
RESULTS = []


def check(num, desc, cond, detail=''):
    RESULTS.append((num, desc, bool(cond), detail))
    print('  %-7s %-3s %-58s %s'
          % ('OK' if cond else 'FAILED', num, desc[:58],
             '' if cond else detail))


def fam_row(owner=None, limbs=None):
    """A family row shaped exactly as `study_qi_adapter.family_rows` emits one:
    ownership already normalised to a bare id plus its type."""
    otype, oid = CA.resolve_owner(owner)
    return {'readiness': 'READY_TO_STUDY_NOW', 'triage_readiness': TRIAGE,
            'phase2_resolution': {
                'canonical_current_answer': oid,
                'canonical_current_answer_owner_type': otype,
                'final_state': 'CURRENT_AND_VERIFIED',
                'family_current_answers': [
                    {'limb_id': l.get('limb_id'),
                     'owner_type': CA.resolve_owner(l)[0],
                     'owner_id': CA.resolve_owner(l)[1]}
                    for l in (limbs or [])]}}


def store_rec(owner=None, limbs=None):
    """A Phase-2 STORE record -- the un-normalised shape the projection reads."""
    r = {'family_id': 'QIF-EM-9999', 'final_state': 'CURRENT_AND_VERIFIED'}
    if owner is not None:
        r['canonical_current_answer'] = owner
    if limbs is not None:
        r['family_current_answers'] = limbs
    return r


def gate_rules(mutate):
    """Rule ids that FAIL when `mutate` is applied to both ownership gates.

    Reuses each gate's own loader and check pass, so the rules exercised here
    are the rules that ship -- and, like every other mutation suite in this
    repository, it mutates an in-memory bundle and never touches disk.
    """
    failed = set()
    for V in (VCA, VP2):
        B = V.load_bundle()
        mutate(B['fams'])
        V.RESULTS = []
        V.run_checks(B)
        failed |= {r for r, ok, _d in V.RESULTS if not ok}
    return failed


def owned(fams):
    return next(r for r in fams if r.get('canonical_current_answer'))


def set_owner(value):
    return lambda fams: owned(fams).__setitem__('canonical_current_answer', value)


def main():
    print('OWNER-READER CONTRACT\n')

    lib_owner = {'owner_type': 'CURRENT_LIBRARY', 'owner_id': LIB}
    sp_limb = {'limb_id': 'L-B', 'limb_label': 'B', 'scope': 'one of several',
               'owner_type': 'SOLVED_PAPER_LIMB', 'owner_id': SIB}
    cl_limb = {'limb_id': 'L-A', 'limb_label': 'A', 'scope': 'one of several',
               'owner_type': 'CURRENT_LIBRARY_LIMB', 'owner_id': LIB}

    # ------------------------------------------------------------------ 1
    # A CURRENT_LIBRARY owner where the old reader expected a question id. It
    # must produce a ROUTE and no whole-question grant: a library answer is not
    # an answer to this question, it is an answer to the concept. The readers
    # got this right before only because a CA id could never equal a QP id --
    # id-space luck, not a decision, and luck is what item 5 below broke.
    check(1, 'CURRENT_LIBRARY routes, and grants no question READY',
          P._library_answer(store_rec(lib_owner)) == LIB
          and P._named_answer(store_rec(lib_owner)) is None
          and A.question_readiness(fam_row(lib_owner), Q) == TRIAGE
          and CA.entry_url_for(store_rec(lib_owner)) == CA.page_url(LIB))

    # ------------------------------------------------------------------ 2 / 3
    # A LIMB owner is a limb route and nothing else: it reaches the limb layer
    # with its type and target intact, and no whole-question surface at all.
    # A paper limb has no library page, so it carries a label and no URL; a
    # library limb carries the URL of the entry that answers that one limb.
    paper_routes = P._library_limbs(store_rec(limbs=[sp_limb]))
    check(2, 'SOLVED_PAPER_LIMB reaches the limb layer, with no page URL',
          len(paper_routes) == 1
          and paper_routes[0]['owner_type'] == 'SOLVED_PAPER_LIMB'
          and paper_routes[0]['owner_id'] == SIB
          and paper_routes[0]['url'] is None)

    lib_routes = P._library_limbs(store_rec(limbs=[cl_limb]))
    check(3, 'CURRENT_LIBRARY_LIMB reaches the limb layer, WITH its page URL',
          len(lib_routes) == 1
          and lib_routes[0]['owner_type'] == 'CURRENT_LIBRARY_LIMB'
          and lib_routes[0]['url'] == CA.page_url(LIB))

    # ------------------------------------------------------------------ 4
    # SIBLING ISOLATION. A verified limb says nothing about the limb beside it.
    # A family owned limb by limb grants no question anything -- not a sibling
    # limb's question, and not the question its own limb answer sits on.
    limb_row = fam_row(owner=None, limbs=[sp_limb])
    check(4, 'a limb owner verifies no sibling limb and no sibling question',
          A.question_readiness(limb_row, 'QP2999-Q9') == TRIAGE
          and A.question_readiness(limb_row, SIB) == TRIAGE
          and len(paper_routes) == 1)

    # ------------------------------------------------------------------ 5
    # THE FALSE POSITIVE THIS SUITE WAS WRITTEN FOR. A limb owner carries a REAL
    # question id, so an id-matching reader hands it the whole question. Refused
    # twice over: the gates refuse the record, and the readers refuse to act on
    # it even if the record ever got past them.
    limb_in_whole_slot = {'owner_type': 'SOLVED_PAPER_LIMB', 'owner_id': Q}
    lib_limb_in_whole_slot = {'owner_type': 'CURRENT_LIBRARY_LIMB',
                              'owner_id': LIB}
    check(5, 'a limb owner in the whole slot badges no whole question',
          A.question_readiness(fam_row(limb_in_whole_slot), Q) == TRIAGE
          and P._named_answer(store_rec(limb_in_whole_slot)) is None
          and CA.entry_url_for(store_rec(lib_limb_in_whole_slot)) is None)
    check('5g', 'and both gates refuse to store it',
          {'R-CA-OWNER-SLOT', 'R-P2-OWNER-SLOT'}
          <= gate_rules(set_owner(limb_in_whole_slot)))

    # ------------------------------------------------------------------ 6
    # UNKNOWN OWNER TYPE. Fail closed at the reader, refused at the gate, and
    # never silently read as the legacy solved-paper shape -- which is what an
    # id-matching reader does with it, because the id still looks fine.
    unknown = {'owner_type': 'PODCAST_EPISODE', 'owner_id': Q}
    check(6, 'an unrecognised owner_type grants nothing',
          A.question_readiness(fam_row(unknown), Q) == TRIAGE
          and P._named_answer(store_rec(unknown)) is None
          and P._library_answer(store_rec(unknown)) is None
          and CA.entry_url_for(store_rec(unknown)) is None)
    check('6g', 'and the gate refuses an unrecognised owner_type',
          'R-CA-OWNER-TYPE-KNOWN' in gate_rules(set_owner(unknown)))

    # ------------------------------------------------------------------ 7
    # MISSING OWNER ID. An owner_type with nothing behind it is not an owner,
    # and a resolved family naming nothing must be refused -- otherwise a
    # hollowed-out record buys the readiness grant a real one would.
    empty = {'owner_type': 'SOLVED_PAPER'}
    check(7, 'an owner_type with no owner_id grants nothing',
          A.question_readiness(fam_row(empty), Q) == TRIAGE
          and CA.resolve_owner(empty)[1] is None
          and CA.owner_ids(store_rec(empty)) == [])
    check('7g', 'and the gate refuses a resolved family owning nothing',
          'R-P2-ANSWER' in gate_rules(set_owner(None)))

    # ------------------------------------------------------------------ 8
    # VALID OWNER, MISSING TARGET. Well-typed, well-shaped, and pointing at
    # something that is not there -- on both sides of the store.
    check('8a', 'a library owner naming an absent entry is caught',
          'R-CA-OWNER-RESOLVES' in gate_rules(set_owner(
              {'owner_type': 'CURRENT_LIBRARY', 'owner_id': 'CA-EM-9999'})))
    check('8b', 'a paper owner naming an absent question is caught',
          'R-CA-OWNER-RESOLVES' in gate_rules(set_owner(
              {'owner_type': 'SOLVED_PAPER', 'owner_id': 'QP9999-Q9'})))

    # ------------------------------------------------------------------ 9 / 10
    # THE OPPOSITE FAILURE. Everything above stops a reader claiming too much;
    # these two stop it claiming too little, which is the quieter direction --
    # a family whose research is complete and whose answer is published simply
    # stops being offered, and nothing anywhere goes red. Tranche 003 found
    # exactly that in `R-READY-SAFE`. Asserting the route is PRESENT is what
    # catches a reader that starts dropping it.
    check(9, 'a CURRENT_LIBRARY whole owner does not drop out of the projection',
          P._library_answer(store_rec(lib_owner)) == LIB
          and CA.library_owner_ids(store_rec(lib_owner)) == [LIB])
    check(10, 'a CURRENT_LIBRARY_LIMB owner does not drop out of limb routing',
          [r['url'] for r in lib_routes] == [CA.page_url(LIB)]
          and CA.library_owner_ids(store_rec(limbs=[cl_limb])) == [LIB])

    failed = [r for r in RESULTS if not r[2]]
    print('\n%d/%d reader-contract assertions hold.'
          % (len(RESULTS) - len(failed), len(RESULTS)))
    if failed:
        print('FAILED: %s' % [r[0] for r in failed])
        return 1
    print('every owner type is read as itself, and none is read as more than '
          'itself.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
