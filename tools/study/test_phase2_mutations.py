#!/usr/bin/env python3
"""Mutation tests for the Phase-2 gate.

A gate that has never rejected anything has not been shown to work.

Each mutation below is a specific, plausible way Phase-2 answer work could go
wrong -- not arbitrary corruption. They are the failures that would ship a
confident, current, WRONG answer to a candidate, or that would let Phase 2
quietly rewrite the recurrence layer it is supposed to consume.

Every mutation is applied to an in-memory copy of the gate's input bundle.
Nothing is written to disk, and the suite fingerprints the governed artefacts
before and after to prove it.

    python tools/study/test_phase2_mutations.py
"""

import copy
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import validate_phase2_tranche as V

REPO = V.REPO
DOC = V.DOC

#: Artefacts that must be byte-identical after the suite runs.
WATCHED = [
    V.STORE,
    os.path.join(DOC, 'study_qi.json'),
    os.path.join(DOC, 'qi', 'qi_families.json'),
    os.path.join(DOC, 'qi', 'qi_occurrences.json'),
    os.path.join(DOC, 'qi', 'qi_phase2_action_queue.json'),
    os.path.join(REPO, 'tools', 'study', 'study_qi_holds.json'),
    os.path.join(REPO, 'meoclass1', 'pastpapers', 'specs', 'QP2602.json'),
]

VERIFIED = 'QIF-EM-0082'      # CURRENT_AND_VERIFIED
CORRECTED = 'QIF-EM-0036'     # UPDATED_AND_VERIFIED, the one edited answer
MODERNISED = 'QIF-EM-0129'    # MODERNISED_AND_VERIFIED, carries a future date


def rec(B, fid):
    return next(r for r in B['fams'] if r['family_id'] == fid)


# --------------------------------------------------------------------------
# Mutations. Each mutates the bundle and returns the rule it must trip.
# --------------------------------------------------------------------------

def mut_01_unverified_family_reads_ready(B):
    """A family nobody could verify is held -- and something marks it ready
    anyway. This is the failure that puts a candidate in an exam with an
    answer MIW could not stand behind."""
    r = rec(B, VERIFIED)
    r['final_state'] = 'HOLD_FOR_AUTHORITY'
    r['readiness_after'] = 'READY_TO_STUDY_NOW'
    B['projected'][VERIFIED]['readiness'] = 'READY_TO_STUDY_NOW'
    B['projected'][VERIFIED]['phase2_resolution']['final_state'] = 'HOLD_FOR_AUTHORITY'
    return 'R-P2-HOLD-BLOCKS'


def mut_02_authority_removed(B):
    """A verified family loses its primary authority. The conclusion survives;
    the reason it was believed does not."""
    rec(B, VERIFIED)['primary_authority'] = []
    return 'R-P2-AUTHORITY'


def mut_03_review_removed_from_changed_answer(B):
    """The one family whose ANSWER was edited loses its independent review.
    A changed answer with no second pair of eyes is exactly what the review
    requirement exists to stop."""
    rec(B, CORRECTED)['independent_review'] = {}
    return 'R-P2-REVIEW'


def mut_04_future_requirement_presented_as_current(B):
    """The HNS Convention enters into force on 29 November 2027. Someone drops
    the not-yet-in-force declaration and leaves the date sitting in the block
    headed 'the position now'. Adopted is not in force."""
    rec(B, MODERNISED)['future_not_in_force'] = []
    return 'R-P2-FUTURE-DECLARED'


def mut_05_answer_points_nowhere(B):
    """A verified family names a canonical answer that does not exist. The
    family reads ready and the candidate lands on nothing."""
    rec(B, VERIFIED)['canonical_current_answer']['question_id'] = 'QP2699-Q9'
    return 'R-P2-ANSWER-REAL'


def mut_06_recurrence_count_altered(B):
    """Phase 2 edits a recurrence count. Phase 2 CONSUMES recurrence; the day
    it starts producing it, the two layers stop being independent evidence."""
    B['metrics'][VERIFIED]['count_10y'] += 3
    return 'R-P2-PIN-RECURRENCE'


def mut_07_modern_repeat_metadata_removed(B):
    """A family is 'tidied' during answer work and loses its modern repeat
    relationships -- the highest-precision intelligence in the corpus, and the
    hardest to reconstruct."""
    B['projected'][VERIFIED]['modern_members'] = \
        B['projected'][VERIFIED]['modern_members'][:2]
    return 'R-P2-MODERN'


def mut_08_adapter_left_stale(B):
    """A Phase-2 decision is recorded but the study layer was never rebuilt,
    so nothing downstream acts on it. A decision nobody can see is not a
    decision."""
    B['projected'][MODERNISED]['phase2_resolution']['final_state'] = \
        'HOLD_FOR_AUTHORITY'
    return 'R-P2-ADAPTER-FRESH'


def mut_09_public_gains_historical_claim(B):
    """The public roadmap starts advertising a 2010-based recurrence count on
    the strength of Phase-2 work. The historical band is mostly
    secondary-claimed dates; it may inform study, never a public claim."""
    B['public_html'] = (B['public_html'] or '') + \
        '<p>this question has been asked 14 times since 2010.</p>'
    return 'R-P2-PUBLIC-SAFE'


def mut_10_manifest_omits_a_family(B):
    """The tranche manifest quietly drops a family it actually worked. The
    work happened; the accounting says it did not."""
    B['store']['tranches']['QI_PHASE2_TRANCHE_001']['family_ids'].remove(MODERNISED)
    return 'R-P2-TRANCHE-CLOSED'


def mut_11_modernisation_edits_a_past_paper(B):
    """A framework change that happened AFTER a sitting is written into that
    sitting's answer. This is the single most damaging thing Phase 2 could do
    to the Written product, because the result looks more current and is
    historically false."""
    rec(B, MODERNISED)['written_source_edited'] = [
        'meoclass1/pastpapers/specs/QP2509.json :: QP2509-Q5']
    return 'R-P2-MODERNISATION-NOEDIT'


def mut_12_unrelated_conflict_hold_resolved(B):
    """A NEAR_REPEAT hold this tranche never examined is marked resolved --
    scope creep dressed as progress."""
    for h in B['holds']['conflict_holds']:
        if h['hold_id'] == 'SQI-CONF-002':
            h['state'] = 'RESOLVED_MODERN'
            h['adjudicated_by'] = 'nobody in particular'
    return 'R-P2-CONFLICT-SCOPE'


def mut_13_resolution_blesses_a_historical_variant(B):
    """Resolving a family marks every older sitting inside it ready too. The
    real one: QP2402-Q5 answers February 2024 and its own record forbids reuse
    at a later sitting. A family being sorted out does not make every sitting
    in it safe to study."""
    fid = 'QIF-EM-0017'
    for member in B['projected'][fid]['modern_members']:
        q = B['questions'].get(member)
        if q and q.get('canonical_family_ids') == [fid]:
            q['readiness'] = ['READY_TO_STUDY_NOW']
    return 'R-P2-ANSWER-SCOPE'


MUTATIONS = [
    mut_01_unverified_family_reads_ready,
    mut_02_authority_removed,
    mut_03_review_removed_from_changed_answer,
    mut_04_future_requirement_presented_as_current,
    mut_05_answer_points_nowhere,
    mut_06_recurrence_count_altered,
    mut_07_modern_repeat_metadata_removed,
    mut_08_adapter_left_stale,
    mut_09_public_gains_historical_claim,
    mut_10_manifest_omits_a_family,
    mut_11_modernisation_edits_a_past_paper,
    mut_12_unrelated_conflict_hold_resolved,
    mut_13_resolution_blesses_a_historical_variant,
]


def fingerprint():
    out = {}
    for path in WATCHED:
        if os.path.exists(path):
            with open(path, 'rb') as f:
                out[path] = hashlib.sha256(f.read()).hexdigest()
    return out


def failures_for(bundle):
    V.RESULTS = []
    V.run_checks(bundle)
    return {rule for rule, ok, _ in V.RESULTS if not ok}


def main():
    before = fingerprint()
    base = V.load_bundle()

    # The unmutated bundle must be clean, or every "catch" below is noise.
    clean = failures_for(copy.deepcopy(base))
    if clean:
        print('BASELINE IS NOT CLEAN -- fix the gate before trusting it:')
        for r in sorted(clean):
            print('   ', r)
        return 1

    caught, escaped = 0, []
    for mut in MUTATIONS:
        bundle = copy.deepcopy(base)
        expected = mut(bundle)
        fails = failures_for(bundle)
        name = mut.__name__.split('_', 2)[2].replace('_', ' ')
        num = mut.__name__.split('_')[1]
        if expected in fails:
            caught += 1
            print('  CAUGHT   %s  %-44s -> %s' % (num, name[:44], expected))
        else:
            escaped.append((num, name, expected, sorted(fails)))
            print('  ESCAPED  %s  %-44s -> expected %s, got %s'
                  % (num, name[:44], expected, sorted(fails) or 'NOTHING'))

    after = fingerprint()
    residue = [p for p in before if before[p] != after.get(p)]

    print('\ncaught %d / escaped %d / residue %d'
          % (caught, len(escaped), len(residue)))
    if residue:
        print('RESIDUE -- the suite wrote to disk:')
        for p in residue:
            print('   ', p)
    if escaped or residue:
        return 1
    print('all mutations caught, zero escapes, zero residue.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
