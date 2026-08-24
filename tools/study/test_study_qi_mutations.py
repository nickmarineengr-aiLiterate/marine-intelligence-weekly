#!/usr/bin/env python3
"""Mutation tests for the QI -> study integration gate.

A gate that has never rejected anything has not been shown to work. Each
mutation below breaks the integration in a specific, plausible way -- the ways
this integration could actually go wrong -- and the gate must catch it.

Every mutation is applied to an in-memory copy of the gate's input bundle. The
files on disk are never written, and the suite fingerprints them before and
after to prove it.

    python tools/study/test_study_qi_mutations.py
"""

import copy
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import study_qi_adapter as A
import validate_study_qi as V

REPO = A.REPO
DOC = A.DOC

#: Artefacts that must be byte-identical after the suite runs.
WATCHED = [
    os.path.join(DOC, 'study_qi.json'),
    os.path.join(DOC, 'modern_qi_baseline.json'),
    os.path.join(DOC, 'study_spine.json'),
    os.path.join(DOC, 'study_progress.json'),
    os.path.join(REPO, 'tools', 'study', 'study_qi_holds.json'),
    os.path.join(REPO, 'SQ', 'study-roadmap.html'),
]


# --------------------------------------------------------------------------
# Mutations. Each takes the context bundle and returns the rule it must trip.
# --------------------------------------------------------------------------

def mut_1_modern_repeat_relationship_removed(ctx):
    """A modern question quietly loses its host_recurrence_hint and reused_from
    -- the single most damaging thing this integration could do."""
    victim = ctx['baseline']['questions_with_repeat_intelligence'][0]
    ctx['modern']['authored'][victim]['host_recurrence_hint'] = []
    ctx['modern']['authored'][victim]['reused_from'] = None
    return 'R-MODERN-KEEP'


def mut_2_modern_family_silently_regrouped(ctx):
    """A modern repeated question is remapped into a canonical family that
    conflicts with its modern grouping, and the conflict is not held."""
    row = next(r for r in ctx['doc']['reconciliation']['rows']
               if r['verdict'] == 'CONFLICT')
    row.pop('hold_id', None)
    return 'R-CONF-HELD'


def mut_2b_modern_family_members_dropped(ctx):
    """A modern multi-member family loses a member with no migration record."""
    fam = next(r for r in ctx['modern']['derived_families'] if r['size'] > 2)
    fam['members'] = fam['members'][:-1]
    return 'R-MODERN-EDGE'


def mut_3_recurrence_counted_twice(ctx):
    """The roadmap input grows a second recurrence quantity, so a modern repeat
    tag and its canonical family each vote."""
    ctx['doc']['roadmap_recurrence_input']['modern_repeat_families_by_topic'] = {
        'D01': 39}
    return 'R-WEIGHT-ONE'


def mut_3b_weight_source_switched(ctx):
    """The weight is taken from the modern layer instead of the one governed
    source, which would silently change what the score means."""
    ctx['doc']['roadmap_recurrence_input']['source'] = 'MODERN_SIXYEAR_FAMILY'
    return 'R-WEIGHT-SRC'


def mut_4_historical_variant_multiplied(ctx):
    """One family's recurrence is credited to a second question as well, so an
    eight-member family votes twice."""
    donor = next(r for r in ctx['doc']['families']
                 if r['canonical_current_question'] and r['historical_variants'])
    twin = copy.deepcopy(donor)
    twin['family_id'] = donor['family_id'] + '-DUP'
    ctx['doc']['families'].append(twin)
    return 'R-VARIANT-1'


def mut_4b_topic_counts_inflated(ctx):
    """A family is counted under two topics -- the exact multiplication the
    bearer rule exists to prevent."""
    did = next(d for d, t in ctx['doc']['topics'].items()
               if t['mapped_families'] > 0)
    ctx['doc']['topics'][did]['mapped_families'] += 1
    return 'R-VARIANT-2'


def mut_5_limb_promoted_to_whole_question(ctx):
    """A question keeps a family whose unit is a limb but reports it as a
    whole-question relationship, so a limb's sitting count becomes the whole
    question's."""
    row = next(r for r in ctx['doc']['questions'] if r['canonical_family_ids']
               and r['family_unit'])
    row['family_unit'] = ['WHOLE_QUESTION']
    fid = row['canonical_family_ids'][0]
    fam = next(f for f in ctx['doc']['families'] if f['family_id'] == fid)
    fam['unit'] = 'LIMB'
    return 'R-LIMB-CARRY'


def mut_5b_whole_vs_limb_join_unlabelled(ctx):
    """A split explained by a governed whole-vs-limb join loses that join, so
    the distinction reads as an accident and invites a merge."""
    row = next(r for r in ctx['doc']['reconciliation']['rows']
               if r['verdict'] == 'LEGITIMATE_WHOLE_VS_LIMB')
    row['governing_joins'] = []
    return 'R-LIMB-LABEL'


def mut_6_currentness_risk_marked_ready(ctx):
    """A family carrying a currentness risk is published as ready to study --
    an unsafe answer presented to a candidate as safe."""
    row = next(r for r in ctx['doc']['families']
               if r['currentness_status'] in A.UNSAFE_CURRENTNESS)
    row['readiness'] = 'READY_TO_STUDY_NOW'
    row['blocked'] = False
    return 'R-READY-SAFE'


def mut_6b_limb_owned_family_ready_with_no_owner(ctx):
    """The LIMB-OWNED half of R-READY-SAFE, untested until Phase-2 tranche 003
    tripped it in production.

    `_phase2_earned` originally read only `canonical_current_answer`, so a
    family owned LIMB BY LIMB looked as though it answered nothing and lost a
    readiness grant it had fully earned. The gap stayed latent because the only
    limb-owned family before tranche 003 carried an UNKNOWN currentness triage,
    and UNKNOWN never reaches this guard. QIF-EM-0061 was the first limb-owned
    family whose triage flagged a real risk.

    Fixing that must not open the other door, so this mutation proves the new
    branch FAILS CLOSED: a limb-owned family carrying a currentness risk, left
    reading READY with no `owner_id` in any limb slot, must still be refused.
    A limb list is not an owner; an owner is.

    The positive control is the baseline itself, which now contains a genuinely
    limb-owned family with an unsafe triage and passes. The condition here is
    CONSTRUCTED onto whichever family carries a Phase-2 resolution rather than
    harvested from whichever family happens to be limb-owned today, so this
    mutation cannot quietly expire when the next tranche changes the corpus.
    """
    row = next(r for r in ctx['doc']['families'] if r.get('phase2_resolution'))
    row['currentness_status'] = 'CURRENT_FRAMEWORK_CHANGED'
    row['readiness'] = 'READY_TO_STUDY_NOW'
    row['blocked'] = False
    p2 = row['phase2_resolution']
    p2['canonical_current_answer'] = None
    p2['family_current_answers'] = [
        {'limb_id': 'L-A', 'scope': 'a limb with nothing in it',
         'owner_type': 'CURRENT_LIBRARY_LIMB', 'owner_id': None}]
    return 'R-READY-SAFE'


def mut_7_phase2_debt_omitted(ctx):
    """A Phase-2 queue family is dropped from the study projection, so answer
    debt stops being visible to the person planning study."""
    victim = ctx['doc']['families'][0]['family_id']
    ctx['doc']['families'] = [r for r in ctx['doc']['families']
                              if r['family_id'] != victim]
    return 'R-DEBT-COVER'


def mut_8_roadmap_recurrence_hand_edited(ctx):
    """The roadmap recurrence is edited away from what the adapter produces --
    a hand-tuned priority wearing a governed label."""
    for did in ctx['doc']['roadmap_recurrence_input']['by_topic']:
        ctx['doc']['roadmap_recurrence_input']['by_topic'][did] += 5
        break
    return 'R-ROADMAP-DERIVE'


def mut_8b_spine_detached_from_adapter(ctx):
    """The spine keeps its own recurrence number instead of reading the
    adapter, quietly restoring a second recurrence brain."""
    ctx['spine']['domains'][0]['study_priority']['raw']['written_recurrence'] = 999
    return 'R-ROADMAP-WIRED'


def mut_9_prerequisite_gating_altered(ctx):
    """A prerequisite edge is dropped, so a dependency-gated study sequence
    silently becomes a raw score ordering."""
    for d in ctx['spine']['domains']:
        if d['prerequisites']:
            d['prerequisites'] = []
            break
    return 'R-PREREQ'


def mut_10_secondary_dated_claim_published(ctx):
    """A secondary-source historical claim reaches the public page."""
    ctx['public_html'] += (
        '<p>Built from official questions since 2010 '
        '(SECONDARY_CLAIMED).</p>')
    return 'R-PUBLIC-LEAK'


def mut_11_deterministic_conflict_ignored(ctx):
    """A DETERMINISTIC modern family conflicts with the canonical layer. The
    precedence rule rests on that never happening, so the gate must refuse
    rather than quietly apply a rule it no longer earns."""
    row = next(r for r in ctx['doc']['reconciliation']['rows']
               if r['verdict'] == 'CONFLICT')
    row['modern_evidence_class'] = 'DETERMINISTIC'
    return 'R-PRECEDENCE'


def mut_12_qi_counts_moved(ctx):
    """The integration rebuilds the QI layer instead of reading it."""
    ctx['occurrence_counts']['recurrence_bearing'] = 1600
    return 'R-QI-OCCURRENCES'


def mut_13_disposition_dropped(ctx):
    """A modern relationship passes through with no recorded disposition, so a
    record is neither preserved nor migrated -- it simply vanishes."""
    ctx['doc']['reconciliation']['rows'][0].pop('disposition')
    return 'R-DISPOSITION'


def mut_14_spent_edge_allowance_left(ctx):
    """A recorded broken-edge allowance stays in place after the edge is fixed,
    blunting the gate for the next real defect."""
    real = ctx['doc']['questions'][0]['question_id']
    ctx['holds']['known_authored_edge_defects']['defects'].append(
        {'reference': 'X', 'resolves_to': real, 'state': 'RECORDED_NOT_FIXED'})
    return 'R-EDGE-ALLOW'


MUTATIONS = [
    ('1   modern repeat relationship removed', mut_1_modern_repeat_relationship_removed),
    ('2   modern/canonical conflict left unheld', mut_2_modern_family_silently_regrouped),
    ('2b  modern family loses a member', mut_2b_modern_family_members_dropped),
    ('3   recurrence counted twice in the roadmap', mut_3_recurrence_counted_twice),
    ('3b  recurrence weight source switched', mut_3b_weight_source_switched),
    ('4   historical variant credited twice', mut_4_historical_variant_multiplied),
    ('4b  family counted under two topics', mut_4b_topic_counts_inflated),
    ('5   limb recurrence promoted to whole question', mut_5_limb_promoted_to_whole_question),
    ('5b  whole-vs-limb join stripped', mut_5b_whole_vs_limb_join_unlabelled),
    ('6   currentness-risk family marked ready', mut_6_currentness_risk_marked_ready),
    ('6b  limb-owned family ready with no owner', mut_6b_limb_owned_family_ready_with_no_owner),
    ('7   Phase-2 answer debt omitted', mut_7_phase2_debt_omitted),
    ('8   roadmap recurrence hand-edited', mut_8_roadmap_recurrence_hand_edited),
    ('8b  spine detached from the adapter', mut_8b_spine_detached_from_adapter),
    ('9   prerequisite gating altered', mut_9_prerequisite_gating_altered),
    ('10  secondary dated claim published', mut_10_secondary_dated_claim_published),
    ('11  deterministic conflict ignored', mut_11_deterministic_conflict_ignored),
    ('12  QI occurrence counts moved', mut_12_qi_counts_moved),
    ('13  modern record left with no disposition', mut_13_disposition_dropped),
    ('14  spent broken-edge allowance retained', mut_14_spent_edge_allowance_left),
]


def fingerprint():
    out = {}
    for path in WATCHED:
        if os.path.exists(path):
            with open(path, 'rb') as fh:
                out[path] = hashlib.sha256(fh.read()).hexdigest()
    return out


def main():
    before = fingerprint()

    base_ctx = V.load_context()
    base_ctx['run_determinism'] = False
    failures, checks = V.run_checks(copy.deepcopy(base_ctx))
    if failures:
        print('BASELINE IS ALREADY FAILING -- fix the integration before '
              'mutating it:')
        for f in failures:
            print('  ' + f)
        return 1
    print('baseline clean: %d checks pass' % len(checks))

    caught = escaped = 0
    for label, mutate in MUTATIONS:
        ctx = copy.deepcopy(base_ctx)
        expected = mutate(ctx)
        try:
            fails, _ = V.run_checks(ctx)
        except Exception as exc:                     # noqa: BLE001
            # A mutation that makes the gate blow up is still caught: the gate
            # refused the input. Say which one, so a crash is never mistaken
            # for a clean pass.
            print('  CAUGHT   %-46s -> raised %s' % (label, type(exc).__name__))
            caught += 1
            continue
        tripped = [f.split()[0] for f in fails]
        if expected in tripped:
            print('  CAUGHT   %-46s -> %s' % (label, expected))
            caught += 1
        elif tripped:
            print('  CAUGHT   %-46s -> %s (expected %s)'
                  % (label, tripped[0], expected))
            caught += 1
        else:
            print('  ESCAPED  %-46s -> nothing tripped (expected %s)'
                  % (label, expected))
            escaped += 1

    after = fingerprint()
    residue = sorted(p for p in before if before[p] != after.get(p))
    print('')
    print('caught %d / escaped %d / residue %d'
          % (caught, escaped, len(residue)))
    for p in residue:
        print('  RESIDUE ' + os.path.relpath(p, REPO))
    if escaped or residue:
        return 1
    print('all mutations caught, zero escapes, zero residue.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
