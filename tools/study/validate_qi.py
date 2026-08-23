#!/usr/bin/env python3
"""The QI gate. Fails closed.

Sixteen invariants. Each one exists because breaking it would let a number be
wrong in a way nobody would notice from the outside -- a limb's sitting count
read as a whole question's, a catalogue entry counted as an exam, a month of
silence counted as a month with no questions.

    python tools/study/validate_qi.py            # gate
    python tools/study/validate_qi.py --verbose  # gate, and say what passed
"""

import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qi_model as M

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QI_DIR = os.path.join(REPO, 'docs', 'study', 'qi')

FILES = [
    'qi_source_entities.json', 'qi_occurrences.json', 'qi_families.json',
    'qi_family_joins.json', 'qi_coverage_matrix.json',
    'qi_time_window_metrics.json', 'qi_currentness.json',
    'qi_phase2_action_queue.json',
]


def load(name, qi_dir=None):
    with open(os.path.join(qi_dir or QI_DIR, name), encoding='utf-8') as fh:
        return json.load(fh)


def validate(qi_dir=None):
    """Return (failures, checks_run). A failure is a (code, detail) pair."""
    fail = []
    checks = []

    def check(code, ok, detail):
        checks.append(code)
        if not ok:
            fail.append((code, detail))

    ent_doc = load('qi_source_entities.json', qi_dir)
    occ_doc = load('qi_occurrences.json', qi_dir)
    fam_doc = load('qi_families.json', qi_dir)
    join_doc = load('qi_family_joins.json', qi_dir)
    cov_doc = load('qi_coverage_matrix.json', qi_dir)
    met_doc = load('qi_time_window_metrics.json', qi_dir)
    cur_doc = load('qi_currentness.json', qi_dir)
    q_doc = load('qi_phase2_action_queue.json', qi_dir)

    entities = {e['entity_id']: e for e in ent_doc['entities']}
    records = occ_doc['occurrences']
    counted = [o for o in records if o['counts_toward_recurrence']]
    families = fam_doc['families']
    metrics = {m['family_id']: m for m in met_doc['families']}
    queue = {r['family_id']: r for r in q_doc['queue']}
    currentness = {c['family_id']: c for c in cur_doc['families']}

    # 1 -- no governed pre-2010 occurrence, and nothing past the ceiling.
    bad = [o['occurrence_id'] for o in records if o['sitting'] < M.QI_LOWER_BOUNDARY]
    check('INV01_NO_PRE_2010_GOVERNED_OCCURRENCE', not bad,
          'pre-2010 occurrences: %s' % bad[:5])

    # 16 -- upper bound cannot exceed 2026-08 for this Phase-1 release.
    bad = [o['occurrence_id'] for o in records if o['sitting'] > M.QI_UPPER_BOUNDARY]
    check('INV16_NO_OCCURRENCE_AFTER_UPPER_BOUNDARY', not bad,
          'occurrences after %s: %s' % (M.QI_UPPER_BOUNDARY, bad[:5]))

    # 2 -- source entity ids unique.
    dupes = [k for k, v in Counter(e['entity_id'] for e in ent_doc['entities']).items() if v > 1]
    check('INV02_SOURCE_ENTITY_IDS_UNIQUE', not dupes, 'duplicate entity ids: %s' % dupes[:5])

    # 3 -- occurrence ids unique.
    dupes = [k for k, v in Counter(o['occurrence_id'] for o in records).items() if v > 1]
    check('INV03_OCCURRENCE_IDS_UNIQUE', not dupes, 'duplicate occurrence ids: %s' % dupes[:5])

    # 4 -- one entity is not accidentally counted twice in one sitting.
    seen = Counter((o['entity_id'], o['sitting'], o['limb']) for o in records)
    dupes = [k for k, v in seen.items() if v > 1]
    check('INV04_ENTITY_NOT_DOUBLE_COUNTED_IN_A_SITTING', not dupes,
          'entity counted twice in one sitting: %s' % dupes[:5])

    # 5 -- one occurrence cannot count twice inside one family, and cannot
    #      belong to two families at once (which would double it globally).
    bad = []
    owner = {}
    for f in families:
        if len(f['occurrence_ids']) != len(set(f['occurrence_ids'])):
            bad.append('%s repeats an occurrence' % f['family_id'])
        for oid in f['occurrence_ids']:
            if oid in owner:
                bad.append('%s in both %s and %s' % (oid, owner[oid], f['family_id']))
            owner[oid] = f['family_id']
    check('INV05_OCCURRENCE_COUNTED_ONCE_PER_FAMILY', not bad, '; '.join(bad[:5]))

    # 6 -- limb recurrence cannot silently become whole-question recurrence.
    bad = []
    for f in families:
        units = {next((o for o in records if o['occurrence_id'] == oid), {}).get('limb')
                 for oid in f['occurrence_ids']}
        if len(units) > 1:
            bad.append('%s mixes limb and whole-question occurrences' % f['family_id'])
    limb_records = [o for o in records if o['limb']]
    leaked = [o['occurrence_id'] for o in limb_records if o['counts_toward_recurrence']
              and o['occurrence_id'] not in owner]
    if leaked:
        bad.append('%d limb records counted with no limb family' % len(leaked))
    for j in join_doc['joins']:
        if j['verdict'] == 'WHOLE_VS_LIMB_RELATION' and j.get('transfers_occurrences'):
            bad.append('%s transfers occurrences across a whole/limb relation' % j['join_id'])
    check('INV06_LIMB_RECURRENCE_IS_NOT_WHOLE_QUESTION_RECURRENCE', not bad, '; '.join(bad[:5]))

    # 7 -- family ids unique and stable in shape.
    fids = [f['family_id'] for f in families]
    check('INV07_FAMILY_IDS_UNIQUE', len(fids) == len(set(fids)),
          'duplicate family ids')

    # 8 -- every family join points at real governed objects.
    known = set(fids)
    bad = [j['join_id'] for j in join_doc['joins']
           if j['family_a'] not in known or j['family_b'] not in known
           or j['family_a'] == j['family_b']]
    check('INV08_FAMILY_JOINS_RESOLVE', not bad, 'broken joins: %s' % bad[:5])

    bad = [f['family_id'] for f in families
           for e in f['member_entities'] if e not in entities]
    if bad:
        fail.append(('INV08_FAMILY_JOINS_RESOLVE', 'family members not in entity layer: %s' % bad[:5]))

    bad = [oid for f in families for oid in f['occurrence_ids']
           if oid not in {o['occurrence_id'] for o in records}]
    if bad:
        fail.append(('INV08_FAMILY_JOINS_RESOLVE', 'family occurrences not in occurrence layer: %s' % bad[:5]))

    # 9 -- provenance populated on every occurrence.
    bad = [o['occurrence_id'] for o in records
           if not o.get('source_class') or o.get('provenance') is None]
    check('INV09_PROVENANCE_POPULATED', not bad, 'missing provenance: %s' % bad[:5])

    # 10 -- sitting and date confidence populated, from the closed vocabulary.
    bad = [o['occurrence_id'] for o in records
           if o.get('date_certainty') not in M.DATE_CERTAINTY or not o.get('sitting')]
    check('INV10_DATE_CONFIDENCE_POPULATED', not bad, 'missing/unknown date certainty: %s' % bad[:5])

    # 11 -- official question-bank records never count as exam occurrences.
    banned = {'DGS_OFFICIAL_QUESTION_BANK', 'HOST_RECURRENCE_ANNOTATION',
              'OFFICIAL_QUESTION_BANK', 'QUESTION_BANK'}
    bad = [o['occurrence_id'] for o in records if o.get('source_class') in banned]
    check('INV11_QUESTION_BANK_IS_NOT_AN_OCCURRENCE', not bad,
          'question-bank/annotation records counted as occurrences: %s' % bad[:5])

    for key, spec in M.NON_OCCURRENCE_EVIDENCE.items():
        if spec['counts_toward_recurrence']:
            fail.append(('INV11_QUESTION_BANK_IS_NOT_AN_OCCURRENCE',
                         '%s is declared to count toward recurrence' % key))

    # 12 -- modern canonical questions are not duplicated across bands.
    native = defaultdict(set)
    for e in ent_doc['entities']:
        if e['evidence_band'] != 'HISTORICAL_SECONDARY_ARCHIVE':
            native[e['native_id']].add(e['evidence_band'])
    dupes = [k for k, v in native.items() if len(v) > 1]
    check('INV12_MODERN_QUESTIONS_NOT_DUPLICATED', not dupes,
          'question ids present in more than one modern band: %s' % dupes[:5])

    # 13 -- every window count derives from the occurrence layer.
    by_id = {o['occurrence_id']: o for o in records}
    bad = []
    for f in families:
        m = metrics.get(f['family_id'])
        if not m:
            bad.append('%s has no metrics row' % f['family_id'])
            continue
        occ = [by_id[i] for i in f['occurrence_ids']]
        if m['total_occurrences'] != len(occ):
            bad.append('%s total %d != %d occurrences' % (f['family_id'], m['total_occurrences'], len(occ)))
        if m['distinct_sittings'] != len({o['sitting'] for o in occ}):
            bad.append('%s distinct_sittings drifted' % f['family_id'])
        for win, field in (('RECENT_3Y', 'count_3y'), ('RECENT_5Y', 'count_5y'),
                           ('MEDIUM_10Y', 'count_10y'), ('FULL_HORIZON', 'count_full_horizon')):
            expect = sum(1 for o in occ if M.in_window(o['sitting'], win))
            if m[field] != expect:
                bad.append('%s %s %d != %d' % (f['family_id'], field, m[field], expect))
        if m['evidence_breakdown'] != dict(Counter(o['evidence_band'] for o in occ)):
            bad.append('%s evidence breakdown drifted' % f['family_id'])
    check('INV13_WINDOW_COUNTS_DERIVE_FROM_OCCURRENCES', not bad, '; '.join(bad[:5]))

    # 14 -- currentness cannot change a recurrence count.
    bad = [c['family_id'] for c in cur_doc['families'] if c.get('affects_recurrence_count')]
    check('INV14_CURRENTNESS_DOES_NOT_MOVE_RECURRENCE', not bad,
          'currentness rows claiming to affect recurrence: %s' % bad[:5])

    # 15 -- every materially recurrent currentness-risk family is in the queue.
    RISKY = {'CURRENTNESS_REVIEW_REQUIRED', 'CURRENT_FRAMEWORK_CHANGED',
             'CURRENT_WITH_AMENDMENT', 'LIKELY_SUPERSEDED'}
    missing = []
    for f in families:
        m = metrics[f['family_id']]
        material = (m['total_occurrences'] >= M.MATERIALLY_RECURRENT_MIN_OCCURRENCES
                    and m['distinct_sittings'] >= M.MATERIALLY_RECURRENT_MIN_SITTINGS)
        risky = currentness[f['family_id']]['currentness_status'] in RISKY
        if material and risky and f['family_id'] not in queue:
            missing.append(f['family_id'])
    check('INV15_RISKY_RECURRENT_FAMILIES_ARE_QUEUED', not missing,
          'materially recurrent currentness-risk families missing from the queue: %s' % missing[:5])

    # Every family reaches the queue with an action, not only the risky ones.
    unqueued = [f['family_id'] for f in families if f['family_id'] not in queue]
    if unqueued:
        fail.append(('INV15_RISKY_RECURRENT_FAMILIES_ARE_QUEUED',
                     'families with no Phase-2 action: %s' % unqueued[:5]))
    bad_action = [r['family_id'] for r in q_doc['queue']
                  if r['phase2_action'] not in M.PHASE2_ACTIONS]
    if bad_action:
        fail.append(('INV15_RISKY_RECURRENT_FAMILIES_ARE_QUEUED',
                     'unknown Phase-2 action: %s' % bad_action[:5]))

    # Coverage: silence is never a confirmed zero.
    bad = [r['sitting'] for r in cov_doc['per_month']
           if r['counts_as_zero_question_sitting']
           and r['coverage_state'] != 'NO_EXAM_OFFICIALLY_EVIDENCED']
    check('INV17_SILENCE_IS_NOT_A_CONFIRMED_ZERO', not bad,
          'months treated as zero-question without official evidence: %s' % bad[:5])

    # Time-relative language must never lose its flag. This is the risk an
    # instrument-name trigger cannot see: a stem that asks for "the latest" or
    # "ongoing developments" names no convention, so nothing about it looks
    # dated -- and its correct answer changes every year regardless.
    bad = []
    for f in families:
        stems = ' '.join(entities[e]['stem'] for e in f['member_entities']).lower()
        expect = sorted({t for t in M.TIME_RELATIVE_TRIGGERS if t in stems})
        got = sorted(currentness[f['family_id']]['time_relative_flags'])
        if expect != got:
            bad.append('%s flags %s, stems carry %s' % (f['family_id'], got, expect))
        if expect and currentness[f['family_id']]['currentness_status'] != 'CURRENTNESS_REVIEW_REQUIRED':
            bad.append('%s carries time-relative language but is %s'
                       % (f['family_id'], currentness[f['family_id']]['currentness_status']))
    check('INV19_TIME_RELATIVE_STEMS_STAY_FLAGGED', not bad, '; '.join(bad[:5]))

    # Public claim: a dated public claim needs OFFICIAL_DATED, never coverage.
    hist_dated = {o['date_certainty'] for o in counted
                  if o['evidence_band'] == 'HISTORICAL_SECONDARY_ARCHIVE'}
    check('INV18_PUBLIC_DATED_CLAIM_STAYS_BARRED',
          hist_dated == {'SECONDARY_CLAIMED'},
          'historical date certainty is %s -- if this ever becomes OFFICIAL_DATED the '
          'public claim policy must be re-decided by the Founder, not by a builder'
          % sorted(hist_dated))

    return fail, checks


def main(argv):
    verbose = '--verbose' in argv
    missing = [f for f in FILES if not os.path.exists(os.path.join(QI_DIR, f))]
    if missing:
        print('MISSING QI PROJECTIONS: %s' % ', '.join(missing), file=sys.stderr)
        print('Run: python tools/study/build_qi.py', file=sys.stderr)
        return 2

    fail, checks = validate()
    if verbose:
        for c in checks:
            print('  %-58s %s' % (c, 'FAIL' if any(f[0] == c for f in fail) else 'ok'))
    if fail:
        print('QI GATE FAILED (%d of %d)' % (len(fail), len(checks)), file=sys.stderr)
        for code, detail in fail:
            print('  %s: %s' % (code, detail), file=sys.stderr)
        return 1
    print('QI gate: %d invariants hold.' % len(checks))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
