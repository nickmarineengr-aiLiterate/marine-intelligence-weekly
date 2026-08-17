# -*- coding: utf-8 -*-
"""Deterministic integrity checks for the Question Intelligence v2 research layer.

Run:
    python meoclass1/pastpapers/intelligence/v2/tools/validate_families.py
    python .../validate_families.py --mutate     # self-test: prove each check can fail

Exit code 0 = all checks pass. Non-zero = at least one check failed.

The checks exist because Phase 1 shipped FAMILY-EM-0004 declaring frequency_known 5
against a single occurrence record. Every count a family states is now required to be
derivable from its own occurrence list, and the derivation is tested here rather than
trusted.
"""
from __future__ import unicode_literals

import argparse
import copy
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
PASTPAPERS = os.path.dirname(os.path.dirname(V2))
SPECS = os.path.join(PASTPAPERS, 'specs')
HIST = os.path.join(PASTPAPERS, 'intelligence', 'historical_qp_intelligence.json')

FAMILIES = os.path.join(V2, 'QUESTION_FAMILIES.json')
OCCURRENCES = os.path.join(V2, 'QUESTION_OCCURRENCES.jsonl')
MANIFEST = os.path.join(V2, 'SOURCE_MANIFEST.json')
BANK = os.path.join(V2, 'OFFICIAL_BANK_ITEMS.json')

MONTHS = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
          'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

# An authoring scaffold is an MIW construct. It describes how the ANSWER is laid out,
# not how the SOURCE PAPER divided the question, and may never key a recurrence.
SCAFFOLD_TOKENS = {
    'framing', 'intro', 'main', 'closing', 'all', 'head', 'report', 'cause',
    'permanent', 'temporary', 'judgement', 'comparison', 'qualification',
    'importance', 'framework', 'survey', 'wider field',
}

LIMB_KINDS = {'SOURCE_LIMB_CONFIRMED', 'SOURCE_LIMB_ASSERTED',
              'ANALYTICAL_SEGMENT', 'AUTHORING_SCAFFOLD', 'WHOLE_QUESTION'}

CONF = {'HIGH', 'MEDIUM', 'LOW', 'NONE', 'UNSCOREABLE_SHORT_STEM'}

SIMILARITY = {'EXACT_REPEAT', 'NEAR_VERBATIM', 'SAME_CORE_ASK',
              'TOPIC_ONLY', 'NO_MEANINGFUL_MATCH'}

# Publication lifecycle. A claim advances one step at a time.
STATUS_ORDER = ['RESEARCH_HYPOTHESIS', 'TEXT_VERIFIED', 'DATE_VERIFIED',
                'LAPTOP_VERIFIED', 'FOUNDER_APPROVED', 'CANDIDATE_PUBLISHED']


def load_json(path):
    with io.open(path, encoding='utf-8-sig') as fh:
        return json.load(fh)


def load_occurrences(path):
    header, rows = None, []
    with io.open(path, encoding='utf-8-sig') as fh:
        for ln, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            obj = json.loads(raw)
            if header is None and 'occurrence_id' not in obj:
                header = obj
                continue
            obj['_line'] = ln
            rows.append(obj)
    return header, rows


def ym(occ):
    m = MONTHS.get((occ.get('source_month') or '').upper()[:3])
    y = occ.get('source_year')
    if not m or not y:
        return None
    return '%04d-%02d' % (y, m)


class Report(object):
    def __init__(self):
        self.failures = []
        self.checks = []

    def check(self, name, ok, detail=''):
        self.checks.append((name, ok))
        if not ok:
            self.failures.append('%s: %s' % (name, detail))
        return ok


def validate(fam_doc, occ_rows, manifest, bank, specs, hist_ids, rep):
    occ_by_id = {}
    # --- C1 no duplicate occurrence ids -------------------------------------
    dupes = []
    for o in occ_rows:
        oid = o.get('occurrence_id')
        if oid in occ_by_id:
            dupes.append(oid)
        occ_by_id[oid] = o
    rep.check('C1 no duplicate occurrence ids', not dupes, 'duplicated: %s' % dupes)

    # --- C2 occurrence shape ------------------------------------------------
    bad_kind = [o['occurrence_id'] for o in occ_rows if o.get('limb_kind') not in LIMB_KINDS]
    rep.check('C2 limb_kind is from the enum', not bad_kind, 'bad: %s' % bad_kind)

    bad_conf = []
    for o in occ_rows:
        for f in ('text_similarity_confidence', 'date_confidence', 'source_confidence'):
            if o.get(f) not in CONF:
                bad_conf.append('%s.%s=%r' % (o['occurrence_id'], f, o.get(f)))
    rep.check('C3 confidences are separate and from the enum', not bad_conf, 'bad: %s' % bad_conf)

    # --- C4 scaffolds never key a recurrence --------------------------------
    scaffolds = []
    for o in occ_rows:
        lab = (o.get('limb_label') or '').strip().lower()
        if not lab:
            continue
        head = re.sub(r'[^a-z ]', '', lab).strip()
        if head in SCAFFOLD_TOKENS or head.split(' ')[0] in SCAFFOLD_TOKENS \
                or re.fullmatch(r'd\d+', lab) or re.fullmatch(r'head \d+', lab):
            if o.get('limb_kind') != 'AUTHORING_SCAFFOLD':
                scaffolds.append('%s limb_label=%r' % (o['occurrence_id'], o.get('limb_label')))
    rep.check('C4 no authoring scaffold used as a source limb', not scaffolds,
              'scaffold-shaped limb labels not marked AUTHORING_SCAFFOLD: %s' % scaffolds)

    used_as_key = [o['occurrence_id'] for o in occ_rows if o.get('limb_kind') == 'AUTHORING_SCAFFOLD']
    rep.check('C5 no occurrence is keyed on an authoring scaffold', not used_as_key,
              'occurrences keyed on a scaffold: %s' % used_as_key)

    # --- C6 question ids valid where MIW-held -------------------------------
    unknown_q = []
    for o in occ_rows:
        qid = o.get('question_id')
        if not qid:
            continue
        if qid not in specs and qid not in hist_ids:
            unknown_q.append(qid)
    rep.check('C6 question ids resolve to a spec or the historical layer',
              not unknown_q, 'unresolved: %s' % sorted(set(unknown_q)))

    # --- C7 limb identifiers valid ------------------------------------------
    bad_limb = []
    for o in occ_rows:
        if o.get('limb_kind') != 'SOURCE_LIMB_CONFIRMED':
            continue
        qid, lab = o.get('question_id'), o.get('limb_label')
        labels = specs.get(qid, {}).get('labels', set())
        if lab not in labels:
            bad_limb.append('%s: limb %r not a printed subpart of %s (printed: %s)'
                            % (o['occurrence_id'], lab, qid, sorted(labels)))
    rep.check('C7 CONFIRMED limbs match a printed subpart label', not bad_limb,
              '; '.join(bad_limb))

    # --- C8 marks are never invented ----------------------------------------
    bad_marks = []
    for o in occ_rows:
        if o.get('limb_kind') != 'SOURCE_LIMB_CONFIRMED':
            continue
        qid, lab, mk = o.get('question_id'), o.get('limb_label'), o.get('marks_if_known')
        printed = specs.get(qid, {}).get('marks', {}).get(lab)
        if mk is not None and printed is not None and mk != printed:
            bad_marks.append('%s: says %s, spec says %s' % (o['occurrence_id'], mk, printed))
        if mk is not None and printed is None:
            bad_marks.append('%s: asserts %s marks where the spec prints none' % (o['occurrence_id'], mk))
    rep.check('C8 marks match the spec and are never inferred', not bad_marks,
              '; '.join(bad_marks))

    # --- C9 source links resolve --------------------------------------------
    src_ids = {s['source_id'] for s in manifest.get('sources', [])}
    bad_src = []
    for o in occ_rows:
        for s in o.get('source_ids') or []:
            if s not in src_ids:
                bad_src.append('%s -> %s' % (o['occurrence_id'], s))
    rep.check('C10 occurrence source_ids resolve to the manifest', not bad_src,
              'unresolved: %s' % bad_src)

    bank_ids = {b['bank_item_id'] for b in bank.get('items', [])}
    bad_bank = [('%s -> %s' % (o['occurrence_id'], o['official_bank_ancestor']))
                for o in occ_rows
                if o.get('official_bank_ancestor') and o['official_bank_ancestor'] not in bank_ids]
    rep.check('C11 official_bank_ancestor resolves to OFFICIAL_BANK_ITEMS.json',
              not bad_bank, 'unresolved: %s' % bad_bank)

    # --- family-level checks -------------------------------------------------
    for fam in fam_doc['families']:
        fid = fam['family_id']
        ids = fam.get('known_occurrences') or []

        missing = [i for i in ids if i not in occ_by_id]
        rep.check('C12 %s occurrence ids exist' % fid, not missing, 'missing: %s' % missing)

        rep.check('C13 %s no duplicate ids within the family' % fid,
                  len(ids) == len(set(ids)), 'duplicates: %s' % ids)

        # THE Phase-1 defect
        rep.check('C14 %s frequency_known == len(known_occurrences)' % fid,
                  fam.get('frequency_known') == len(ids),
                  'declares %r against %d records' % (fam.get('frequency_known'), len(ids)))

        present = sorted(x for x in (ym(occ_by_id[i]) for i in ids if i in occ_by_id) if x)
        if present:
            rep.check('C15 %s earliest_occurrence consistent' % fid,
                      fam.get('earliest_occurrence') == present[0],
                      'declares %r, records give %r' % (fam.get('earliest_occurrence'), present[0]))
            rep.check('C16 %s latest_occurrence consistent' % fid,
                      fam.get('latest_occurrence') == present[-1],
                      'declares %r, records give %r' % (fam.get('latest_occurrence'), present[-1]))
            prev = present[-2] if len(present) > 1 else None
            rep.check('C17 %s previous_before_current consistent' % fid,
                      fam.get('previous_before_current') == prev,
                      'declares %r, records give %r' % (fam.get('previous_before_current'), prev))

        rep.check('C18 %s similarity class is from the enum' % fid,
                  fam.get('similarity_to_current') in SIMILARITY,
                  'got %r' % fam.get('similarity_to_current'))

        for f in ('text_similarity_confidence', 'date_confidence', 'source_confidence'):
            rep.check('C19 %s %s from the enum' % (fid, f), fam.get(f) in CONF,
                      'got %r' % fam.get(f))

        st = fam.get('publication_status')
        rep.check('C20 %s publication_status is from the lifecycle' % fid,
                  st in STATUS_ORDER, 'got %r' % st)

        # --- the rules that keep an unproven claim off a candidate's screen ---
        if st in STATUS_ORDER:
            i = STATUS_ORDER.index(st)
            if i >= STATUS_ORDER.index('DATE_VERIFIED'):
                rep.check('C21 %s DATE_VERIFIED or beyond requires date_confidence HIGH' % fid,
                          fam.get('date_confidence') == 'HIGH',
                          'status %s with date_confidence %r' % (st, fam.get('date_confidence')))
            if i >= STATUS_ORDER.index('TEXT_VERIFIED'):
                rep.check('C22 %s TEXT_VERIFIED or beyond requires text confidence HIGH' % fid,
                          fam.get('text_similarity_confidence') == 'HIGH',
                          'status %s with text_similarity_confidence %r'
                          % (st, fam.get('text_similarity_confidence')))
            rep.check('C23 %s nothing is CANDIDATE_PUBLISHED in Phase 2' % fid,
                      st != 'CANDIDATE_PUBLISHED', 'family is marked CANDIDATE_PUBLISHED')

        # a family may not claim a dormancy gap it cannot evidence at both ends
        if fam.get('dormancy_class') in ('LONG_GAP_RETURN', 'HISTORICAL_RETURN'):
            rep.check('C24 %s long-gap class needs 2+ proven sittings' % fid,
                      len(ids) >= 2, 'class %s with %d occurrence(s)'
                      % (fam.get('dormancy_class'), len(ids)))

        # an unverifiable assertion may never sit in the counted list
        for u in fam.get('unverified_asserted_occurrences') or []:
            rep.check('C25 %s unverified assertion is not counted' % fid,
                      u.get('status') in ('UNVERIFIABLE_FROM_REPOSITORY', 'NOT_PRESERVED'),
                      'status %r' % u.get('status'))

    # --- C26 every occurrence belongs to exactly one family -------------------
    claimed = [i for f in fam_doc['families'] for i in (f.get('known_occurrences') or [])]
    rep.check('C26 no occurrence claimed by two families',
              len(claimed) == len(set(claimed)),
              'claimed twice: %s' % sorted({c for c in claimed if claimed.count(c) > 1}))

    orphans = sorted(set(occ_by_id) - set(claimed))
    rep.check('C27 no orphan occurrence records', not orphans, 'orphans: %s' % orphans)

    # --- C28 bank items are never counted as sittings -------------------------
    bank_as_occ = [o['occurrence_id'] for o in occ_rows
                   if (o.get('occurrence_id') or '').startswith('OCC-BANK')]
    rep.check('C28 no official bank item is recorded as a sitting occurrence',
              not bank_as_occ, 'found: %s' % bank_as_occ)

    return rep


def build_spec_index():
    specs, hist_ids = {}, set()
    for fn in os.listdir(SPECS):
        if not fn.endswith('.json'):
            continue
        try:
            d = load_json(os.path.join(SPECS, fn))
        except ValueError:
            continue
        for q in d.get('questions', []):
            labels, marks = set(), {}
            for sp in (q.get('subparts') or []):
                if sp.get('label'):
                    labels.add(sp['label'])
                    marks[sp['label']] = sp.get('marks')
            specs[q['question_id']] = {'labels': labels, 'marks': marks,
                                       'total_marks': q.get('total_marks')}
    if os.path.exists(HIST):
        h = load_json(HIST)
        for p in h.get('papers', []):
            for q in p.get('questions', []):
                hist_ids.add(q['question_id'])
    return specs, hist_ids


MUTATIONS = [
    ('inflate frequency_known (the Phase-1 defect)',
     lambda f, o: f['families'][3].update({'frequency_known': 99}), 'C14'),
    ('drop an occurrence record but keep the count',
     lambda f, o: f['families'][2]['known_occurrences'].pop(), 'C14'),
    ('point a family at a nonexistent occurrence',
     lambda f, o: f['families'][0]['known_occurrences'].append('OCC-DOES-NOT-EXIST'), 'C12'),
    ('duplicate an occurrence id inside a family',
     lambda f, o: f['families'][2]['known_occurrences'].append(
         f['families'][2]['known_occurrences'][0]), 'C13'),
    ('falsify earliest_occurrence',
     lambda f, o: f['families'][3].update({'earliest_occurrence': '2010-03'}), 'C15'),
    ('falsify latest_occurrence',
     lambda f, o: f['families'][3].update({'latest_occurrence': '2099-01'}), 'C16'),
    ('falsify previous_before_current',
     lambda f, o: f['families'][3].update({'previous_before_current': '2010-06'}), 'C17'),
    ('publish a family whose date is unproven',
     lambda f, o: f['families'][0].update({'publication_status': 'DATE_VERIFIED'}), 'C21'),
    ('jump a research hypothesis straight to candidate-published',
     lambda f, o: f['families'][4].update({'publication_status': 'CANDIDATE_PUBLISHED'}), 'C22'),
    ('claim a long gap on a single sitting',
     lambda f, o: f['families'][0].update({'dormancy_class': 'HISTORICAL_RETURN'}), 'C24'),
    ('promote an unverifiable assertion to a counted occurrence',
     lambda f, o: f['families'][0]['unverified_asserted_occurrences'][0].update(
         {'status': 'TEXT_VERIFIED'}), 'C25'),
    ('use an authoring scaffold as a source limb',
     lambda f, o: o[0].update({'limb_label': 'framing'}), 'C4'),
    ('key an occurrence on a scaffold',
     lambda f, o: o[0].update({'limb_kind': 'AUTHORING_SCAFFOLD'}), 'C5'),
    ('invent a limb that the paper does not print',
     lambda f, o: o[0].update({'limb_label': '(z)'}), 'C7'),
    ('invent marks for a limb',
     lambda f, o: o[0].update({'marks_if_known': 99}), 'C8'),
    ('point an occurrence at an unknown source',
     lambda f, o: o[0].update({'source_ids': ['SRC-MADE-UP']}), 'C10'),
    ('point an occurrence at an unknown bank item',
     lambda f, o: o[0].update({'official_bank_ancestor': 'BANK-999'}), 'C11'),
    ('point an occurrence at an unknown question',
     lambda f, o: o[0].update({'question_id': 'QP9999-Q1'}), 'C6'),
    ('collapse a confidence back into one field',
     lambda f, o: o[0].update({'date_confidence': None}), 'C3'),
    ('claim two families own the same occurrence',
     lambda f, o: f['families'][0]['known_occurrences'].append(
         f['families'][2]['known_occurrences'][0]), 'C26'),
    ('orphan an occurrence record',
     lambda f, o: f['families'][2]['known_occurrences'].pop(0), 'C14|C27'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutate', action='store_true',
                    help='self-test: corrupt the data one way at a time and prove a check fires')
    args = ap.parse_args()

    fam = load_json(FAMILIES)
    _, occ = load_occurrences(OCCURRENCES)
    manifest = load_json(MANIFEST)
    bank = load_json(BANK)
    specs, hist_ids = build_spec_index()

    rep = validate(fam, occ, manifest, bank, specs, hist_ids, Report())
    print('QI-v2 family validator')
    print('  families    : %d' % len(fam['families']))
    print('  occurrences : %d' % len(occ))
    print('  bank items  : %d' % len(bank['items']))
    print('  checks run  : %d' % len(rep.checks))
    if rep.failures:
        print('  FAILURES    : %d' % len(rep.failures))
        for f in rep.failures:
            print('    - %s' % f)
    else:
        print('  FAILURES    : 0')

    if not args.mutate:
        return 1 if rep.failures else 0

    print('\nmutation test - each mutation must make a named check fail')
    print('%-58s %-10s %s' % ('MUTATION', 'EXPECT', 'RESULT'))
    print('-' * 92)
    bad = 0
    for name, mutate, expect in MUTATIONS:
        f2, o2 = copy.deepcopy(fam), copy.deepcopy(occ)
        try:
            mutate(f2, o2)
        except Exception as exc:                                  # noqa: BLE001
            print('%-58s %-10s SETUP ERROR %s' % (name[:58], expect, exc))
            bad += 1
            continue
        r2 = validate(f2, o2, manifest, bank, specs, hist_ids, Report())
        fired = {fl.split(' ')[0] for fl in r2.failures}
        wanted = set(expect.split('|'))
        ok = bool(fired & wanted)
        bad += 0 if ok else 1
        print('%-58s %-10s %s' % (name[:58], expect,
                                  'caught' if ok else 'ESCAPED (fired: %s)' % sorted(fired)))
    print('-' * 92)
    print('mutations: %d   escaped: %d' % (len(MUTATIONS), bad))
    return 1 if (rep.failures or bad) else 0


if __name__ == '__main__':
    sys.exit(main())
