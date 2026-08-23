#!/usr/bin/env python3
"""Mutation tests for the QI gate.

A gate that has never rejected anything has not been shown to work. Each test
below breaks the QI layer in a specific, plausible way and requires the gate to
catch it. Every mutation is applied to a throwaway copy; the real projections
are never touched, and the suite asserts that afterwards.

    python tools/study/test_qi_mutations.py
"""

import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qi_model as M
import validate_qi as V

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QI_DIR = os.path.join(REPO, 'docs', 'study', 'qi')


def read(d, name):
    with open(os.path.join(d, name), encoding='utf-8') as fh:
        return json.load(fh)


def write(d, name, doc):
    with open(os.path.join(d, name), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write('\n')


# --------------------------------------------------------------------------
# Mutations. Each returns the invariant code it must trip.
# --------------------------------------------------------------------------

def mut_a_pre_2010_occurrence(d):
    """A 2009 sitting slips into the governed layer."""
    doc = read(d, 'qi_occurrences.json')
    seed = dict(doc['occurrences'][0])
    seed['occurrence_id'] = seed['occurrence_id'] + '-MUTANT'
    seed['sitting'] = '2009-11'
    doc['occurrences'].append(seed)
    write(d, 'qi_occurrences.json', doc)
    return 'INV01_NO_PRE_2010_GOVERNED_OCCURRENCE'


def mut_b_duplicate_source_entity(d):
    """One source entity is serialised twice, inflating the entity count."""
    doc = read(d, 'qi_source_entities.json')
    doc['entities'].append(dict(doc['entities'][0]))
    write(d, 'qi_source_entities.json', doc)
    return 'INV02_SOURCE_ENTITY_IDS_UNIQUE'


def mut_c_duplicate_occurrence_in_family(d):
    """A family lists one occurrence twice -- a 5-time repeat becomes a 6."""
    doc = read(d, 'qi_families.json')
    fam = next(f for f in doc['families'] if len(f['occurrence_ids']) >= 2)
    fam['occurrence_ids'].append(fam['occurrence_ids'][0])
    write(d, 'qi_families.json', doc)
    return 'INV05_OCCURRENCE_COUNTED_ONCE_PER_FAMILY'


def mut_d_limb_becomes_whole_question(d):
    """A governed limb record is promoted into a whole-question family, so the
    limb's sittings start evidencing the whole question."""
    occ = read(d, 'qi_occurrences.json')
    limb = next(o for o in occ['occurrences'] if o['limb'])
    limb['counts_toward_recurrence'] = True
    write(d, 'qi_occurrences.json', occ)

    fam = read(d, 'qi_families.json')
    target = next(f for f in fam['families'] if len(f['occurrence_ids']) >= 2)
    target['occurrence_ids'].append(limb['occurrence_id'])
    write(d, 'qi_families.json', fam)
    return 'INV06_LIMB_RECURRENCE_IS_NOT_WHOLE_QUESTION_RECURRENCE'


def mut_e_question_bank_as_occurrence(d):
    """An item from the Directorate's undated question bank is admitted as an
    exam occurrence, manufacturing recurrence out of a catalogue."""
    doc = read(d, 'qi_occurrences.json')
    seed = dict(doc['occurrences'][0])
    seed['occurrence_id'] = 'QIO-BANK-MUTANT'
    seed['source_class'] = 'DGS_OFFICIAL_QUESTION_BANK'
    seed['date_certainty'] = 'NONE'
    doc['occurrences'].append(seed)
    write(d, 'qi_occurrences.json', doc)
    return 'INV11_QUESTION_BANK_IS_NOT_AN_OCCURRENCE'


def mut_f_secondary_claim_upgraded_to_official(d):
    """A secondary-source date claim is relabelled OFFICIAL_DATED with no
    official document behind it -- which would unlock the public dated claim."""
    doc = read(d, 'qi_occurrences.json')
    row = next(o for o in doc['occurrences']
               if o['evidence_band'] == 'HISTORICAL_SECONDARY_ARCHIVE')
    row['date_certainty'] = 'OFFICIAL_DATED'
    write(d, 'qi_occurrences.json', doc)
    return 'INV18_PUBLIC_DATED_CLAIM_STAYS_BARRED'


def mut_g_broken_family_join(d):
    """A join points at a family that does not exist."""
    doc = read(d, 'qi_family_joins.json')
    if not doc['joins']:
        raise AssertionError('no joins to break')
    doc['joins'][0]['family_b'] = 'QIF-EM-9999'
    write(d, 'qi_family_joins.json', doc)
    return 'INV08_FAMILY_JOINS_RESOLVE'


def mut_h_currentness_flag_removed(d):
    """The time-relative flag is stripped from a stem that asks for 'the
    ongoing developments' -- the single most dangerous silent failure here."""
    doc = read(d, 'qi_currentness.json')
    row = next(c for c in doc['families'] if c['time_relative_flags'])
    row['time_relative_flags'] = []
    row['currentness_status'] = 'CURRENT'
    write(d, 'qi_currentness.json', doc)
    return 'INV19_TIME_RELATIVE_STEMS_STAY_FLAGGED'


def mut_i_risky_family_dropped_from_queue(d):
    """A materially recurrent, currentness-risk family is dropped from the
    Phase-2 queue, so Phase 2 never learns it needs work."""
    cur = read(d, 'qi_currentness.json')
    met = {m['family_id']: m for m in read(d, 'qi_time_window_metrics.json')['families']}
    risky = next(c['family_id'] for c in cur['families']
                 if c['currentness_status'] in ('CURRENTNESS_REVIEW_REQUIRED',
                                                'CURRENT_FRAMEWORK_CHANGED',
                                                'CURRENT_WITH_AMENDMENT')
                 and met[c['family_id']]['distinct_sittings'] >= 2)
    doc = read(d, 'qi_phase2_action_queue.json')
    doc['queue'] = [r for r in doc['queue'] if r['family_id'] != risky]
    write(d, 'qi_phase2_action_queue.json', doc)
    return 'INV15_RISKY_RECURRENT_FAMILIES_ARE_QUEUED'


def mut_j_occurrence_after_ceiling(d):
    """A 2026-10 sitting appears, breaking the Phase-1 ceiling."""
    doc = read(d, 'qi_occurrences.json')
    seed = dict(doc['occurrences'][-1])
    seed['occurrence_id'] = seed['occurrence_id'] + '-FUTURE'
    seed['sitting'] = '2026-10'
    doc['occurrences'].append(seed)
    write(d, 'qi_occurrences.json', doc)
    return 'INV16_NO_OCCURRENCE_AFTER_UPPER_BOUNDARY'


def mut_k_window_count_hand_edited(d):
    """A recurrence count is edited by hand instead of derived."""
    doc = read(d, 'qi_time_window_metrics.json')
    doc['families'][0]['count_3y'] += 3
    doc['families'][0]['total_occurrences'] += 3
    write(d, 'qi_time_window_metrics.json', doc)
    return 'INV13_WINDOW_COUNTS_DERIVE_FROM_OCCURRENCES'


def mut_l_silence_counted_as_zero(d):
    """A month with no source page is recorded as a confirmed zero-question
    sitting, which would quietly deflate every recurrence denominator."""
    doc = read(d, 'qi_coverage_matrix.json')
    row = next(r for r in doc['per_month'] if r['coverage_state'] == 'NO_SOURCE_PAGE_FOUND')
    row['counts_as_zero_question_sitting'] = True
    write(d, 'qi_coverage_matrix.json', doc)
    return 'INV17_SILENCE_IS_NOT_A_CONFIRMED_ZERO'


def mut_m_modern_question_duplicated(d):
    """A 2023 question is emitted in both the wording-only and solved bands --
    the 72-question double-count this build exists to suppress."""
    doc = read(d, 'qi_source_entities.json')
    solved = next(e for e in doc['entities'] if e['evidence_band'] == 'MIW_SOLVED_CANONICAL')
    clone = dict(solved)
    clone['entity_id'] = solved['entity_id'] + '-DUP'
    clone['evidence_band'] = 'MIW_WORDING_ONLY'
    doc['entities'].append(clone)
    write(d, 'qi_source_entities.json', doc)
    return 'INV12_MODERN_QUESTIONS_NOT_DUPLICATED'


def mut_n_entity_double_counted_in_sitting(d):
    """One entity is recorded twice in the same sitting under two ids."""
    doc = read(d, 'qi_occurrences.json')
    seed = next(o for o in doc['occurrences'] if not o['limb'])
    clone = dict(seed)
    clone['occurrence_id'] = seed['occurrence_id'] + '-TWICE'
    doc['occurrences'].append(clone)
    write(d, 'qi_occurrences.json', doc)
    return 'INV04_ENTITY_NOT_DOUBLE_COUNTED_IN_A_SITTING'


MUTATIONS = [
    ('A  pre-2010 governed occurrence', mut_a_pre_2010_occurrence),
    ('B  duplicated source entity', mut_b_duplicate_source_entity),
    ('C  occurrence counted twice in one family', mut_c_duplicate_occurrence_in_family),
    ('D  limb recurrence promoted to whole-question', mut_d_limb_becomes_whole_question),
    ('E  question-bank item counted as an exam occurrence', mut_e_question_bank_as_occurrence),
    ('F  secondary date claim upgraded to official', mut_f_secondary_claim_upgraded_to_official),
    ('G  broken family join', mut_g_broken_family_join),
    ('H  currentness flag stripped from a time-relative stem', mut_h_currentness_flag_removed),
    ('I  risky recurrent family dropped from the Phase-2 queue', mut_i_risky_family_dropped_from_queue),
    ('J  occurrence after the 2026-08 ceiling', mut_j_occurrence_after_ceiling),
    ('K  recurrence count hand-edited away from the occurrence layer', mut_k_window_count_hand_edited),
    ('L  month of silence counted as a confirmed zero', mut_l_silence_counted_as_zero),
    ('M  modern question duplicated across bands', mut_m_modern_question_duplicated),
    ('N  entity counted twice in one sitting', mut_n_entity_double_counted_in_sitting),
]


def fingerprint():
    out = {}
    for name in V.FILES:
        with open(os.path.join(QI_DIR, name), 'rb') as fh:
            out[name] = fh.read()
    return out


def main():
    before = fingerprint()

    baseline_fail, checks = V.validate(QI_DIR)
    if baseline_fail:
        print('BASELINE IS ALREADY FAILING -- fix the layer before mutating it:',
              file=sys.stderr)
        for c, det in baseline_fail:
            print('  %s: %s' % (c, det), file=sys.stderr)
        return 2
    print('baseline: %d invariants hold\n' % len(checks))

    caught = escaped = 0
    for label, fn in MUTATIONS:
        tmp = tempfile.mkdtemp(prefix='qi-mut-')
        try:
            for name in V.FILES:
                shutil.copy(os.path.join(QI_DIR, name), os.path.join(tmp, name))
            expected = fn(tmp)
            fail, _ = V.validate(tmp)
            codes = {c for c, _ in fail}
            if expected in codes:
                print('  CAUGHT   %-58s -> %s' % (label, expected))
                caught += 1
            elif codes:
                print('  CAUGHT*  %-58s -> %s (expected %s)'
                      % (label, sorted(codes)[0], expected))
                caught += 1
            else:
                print('  ESCAPED  %-58s (expected %s)' % (label, expected))
                escaped += 1
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    after = fingerprint()
    residue = sorted(k for k in before if before[k] != after[k])

    print('\ncaught %d / escaped %d / residue %d'
          % (caught, escaped, len(residue)))
    if residue:
        print('RESIDUE -- a mutation leaked into the real projections: %s' % residue,
              file=sys.stderr)
    if escaped or residue:
        return 1
    print('all mutations caught, zero escapes, zero residue.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
