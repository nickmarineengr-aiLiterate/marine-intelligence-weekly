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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qi_paths                                                   # noqa: E402

HERE = qi_paths.TOOLS
V2 = qi_paths.V2
PASTPAPERS = qi_paths.PASTPAPERS
SPECS = qi_paths.SPECS
HIST = qi_paths.HIST

FAMILIES = qi_paths.FAMILIES
OCCURRENCES = qi_paths.OCCURRENCES
MANIFEST = qi_paths.MANIFEST
BANK = qi_paths.BANK
VERIFICATION = qi_paths.VERIFICATION

MONTHS = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
          'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

# The full extracted bank, committed under pastpapers/sources/official so that
# referential integrity is executable on every machine. Phase 3A resolved this
# to the Desktop intake directory, which made C32/C33 skip silently on the
# integration authority's machine and let a tampered-bank-text mutation escape.
# The curated subset in OFFICIAL_BANK_ITEMS.json is checked back against it.
EXTRACTED_BANK = qi_paths.EXTRACTED_BANK

# Which source classes can carry a DATE. A question bank cannot: it is undated
# by construction, and that is the whole point of keeping ancestry and dating
# apart. Phase 2's C21 only checked that the stored date_confidence agreed with
# the stored publication_status, so editing both consistently promoted a family
# with no dated evidence behind it at all. Dates are now derived.
DATE_BEARING_SOURCE_TYPES = {'OFFICIAL_SITTING_PAPER', 'MIW_VERIFIED_CORPUS'}
NEVER_DATE_BEARING = {'OFFICIAL_QUESTION_BANK'}

# The one inline annotation in the whole bank, and the item it belongs to.
# Phase 2's prose attributed it to item 4. Deriving it stops the next write-up
# guessing.
OCT05_ITEM = 3
OCT05_MARK = '(Oct-05)'

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
        self.skipped = []

    def check(self, name, ok, detail=''):
        self.checks.append((name, ok))
        if not ok:
            self.failures.append('%s: %s' % (name, detail))
        return ok

    def skip(self, name, why):
        """A check that could not run. Recorded loudly; never counted as a pass."""
        self.skipped.append('%s: %s' % (name, why))


def load_extracted_bank():
    """The 185-item extract, or None when the raw intake tree is absent."""
    if not os.path.exists(EXTRACTED_BANK):
        return None
    try:
        return {int(k): v for k, v
                in load_json(EXTRACTED_BANK)['items'].items()}
    except (ValueError, KeyError):
        return None


def date_evidence(occ, src_by_id):
    """Why this occurrence does or does not carry a usable date.

    Returns (is_dated, reason). A bank ancestor can never make this true.
    """
    if not ym(occ):
        return False, 'no source_year/source_month'
    sids = occ.get('source_ids') or []
    if not sids:
        return False, 'no source_ids'
    bank_only = True
    for sid in sids:
        st = (src_by_id.get(sid) or {}).get('source_type')
        if st in NEVER_DATE_BEARING:
            continue
        bank_only = False
        if st in DATE_BEARING_SOURCE_TYPES:
            return True, 'dated by %s (%s)' % (sid, st)
    if bank_only:
        return False, 'only question-bank sources, which carry no date'
    return False, 'no source of a date-bearing class: %s' % sids


def validate(fam_doc, occ_rows, manifest, bank, specs, hist_ids, rep,
             extracted=None):
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

    # --- bank referential integrity (Phase 3A) --------------------------------
    items = bank.get('items', [])

    ids = [b.get('bank_item_id') for b in items]
    rep.check('C29 no duplicate bank_item_id', len(ids) == len(set(ids)),
              'duplicated: %s' % sorted({i for i in ids if ids.count(i) > 1}))

    bad_num = []
    for b in items:
        bid, num = b.get('bank_item_id') or '', b.get('bank_item_number')
        m = re.match(r'^BANK-(\d+)$', bid)
        if not m:
            bad_num.append('%r is not BANK-nnn' % bid)
        elif num != int(m.group(1)):
            bad_num.append('%s declares number %r' % (bid, num))
        elif not (1 <= (num or 0) <= 185):
            bad_num.append('%s number %r out of range 1-185' % (bid, num))
    rep.check('C30 bank_item_id and bank_item_number agree and are in range',
              not bad_num, '; '.join(bad_num))

    empty = [b.get('bank_item_id') for b in items
             if not (b.get('text_verbatim') or '').strip()]
    rep.check('C31 every bank item carries canonical text', not empty,
              'empty: %s' % empty)

    if extracted is None:
        rep.skip('C32 curated bank text matches the 185-item extract',
                 'raw intake tree not present at %s' % EXTRACTED_BANK)
        rep.skip('C33 the (Oct-05) annotation is derived, not remembered',
                 'raw intake tree not present')
    else:
        mismatch = []
        for b in items:
            num = b.get('bank_item_number')
            want = extracted.get(num)
            got = b.get('text_verbatim')
            if want is None:
                mismatch.append('%s: item %r absent from the extract'
                                % (b.get('bank_item_id'), num))
            elif ' '.join((want or '').split()) != ' '.join((got or '').split()):
                mismatch.append('%s: text differs from the extract'
                                % b.get('bank_item_id'))
        rep.check('C32 curated bank text matches the 185-item extract',
                  not mismatch, '; '.join(mismatch))

        carriers = sorted(n for n, t in extracted.items() if OCT05_MARK in t)
        rep.check('C33 the (Oct-05) annotation is derived, not remembered',
                  carriers == [OCT05_ITEM],
                  'expected only item %d to carry %s, extract gives %s'
                  % (OCT05_ITEM, OCT05_MARK, carriers))

        rep.check('C34 the extract still holds all 185 items',
                  len(extracted) == 185 and set(extracted) == set(range(1, 186)),
                  'extract holds %d items' % len(extracted))

    src_by_id = {s['source_id']: s for s in manifest.get('sources', [])}

    bad_bank_src = [b.get('bank_item_id') for b in items
                    if bank.get('source_id') not in src_by_id]
    rep.check('C35 the bank names a source that resolves to the manifest',
              not bad_bank_src,
              'bank source_id %r is not in SOURCE_MANIFEST.json'
              % bank.get('source_id'))

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

        anc = fam.get('official_bank_ancestor')
        rep.check('C39 %s official_bank_ancestor resolves' % fid,
                  not anc or anc in bank_ids,
                  'family cites %r, which is not in OFFICIAL_BANK_ITEMS.json' % anc)

        rep.check('C18 %s similarity class is from the enum' % fid,
                  fam.get('similarity_to_current') in SIMILARITY,
                  'got %r' % fam.get('similarity_to_current'))

        for f in ('text_similarity_confidence', 'date_confidence', 'source_confidence'):
            rep.check('C19 %s %s from the enum' % (fid, f), fam.get(f) in CONF,
                      'got %r' % fam.get(f))

        st = fam.get('publication_status')
        rep.check('C20 %s publication_status is from the lifecycle' % fid,
                  st in STATUS_ORDER, 'got %r' % st)

        # --- dates are DERIVED from evidence, never merely declared ----------
        # Phase 2 checked only that date_confidence agreed with
        # publication_status, so editing the two together promoted a family
        # that had no dated source behind it. The derivation is now the check.
        # date_confidence answers "how sure are we WHEN THE EARLIER one was
        # set?". The current sitting is dated by definition and is not the
        # claim, so it is excluded: a family whose only occurrence is the
        # paper in hand has no historical date evidence at all.
        current = (fam.get('current_recurrence') or '').strip()
        dated = []
        for i_ in ids:
            o = occ_by_id.get(i_)
            if not o:
                continue
            tag = '%s%s' % (o.get('question_id') or '', o.get('limb_label') or '')
            if current and tag == current:
                continue
            ok_, why_ = date_evidence(o, src_by_id)
            if ok_:
                dated.append((i_, why_))
        derived = 'HIGH' if dated else 'NONE'

        rep.check('C36 %s date_confidence is derived from dated evidence' % fid,
                  not (fam.get('date_confidence') == 'HIGH' and derived != 'HIGH'),
                  'declares date_confidence HIGH but no PRIOR occurrence has a '
                  'date-bearing source; a question-bank ancestor never dates a '
                  'sitting, and the current paper is not evidence of an '
                  'earlier one')

        rep.check('C37 %s a claimed earlier sitting needs dated evidence' % fid,
                  not (fam.get('previous_before_current') and not dated),
                  'declares previous_before_current %r with no dated prior '
                  'occurrence' % fam.get('previous_before_current'))

        # --- the rules that keep an unproven claim off a candidate's screen ---
        if st in STATUS_ORDER:
            i = STATUS_ORDER.index(st)
            if i >= STATUS_ORDER.index('DATE_VERIFIED'):
                rep.check('C21 %s DATE_VERIFIED or beyond requires date_confidence HIGH' % fid,
                          fam.get('date_confidence') == 'HIGH',
                          'status %s with date_confidence %r' % (st, fam.get('date_confidence')))
                rep.check('C38 %s DATE_VERIFIED or beyond requires DERIVED dated evidence' % fid,
                          derived == 'HIGH',
                          'status %s but no occurrence carries a date-bearing '
                          'source' % st)
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
    ('point a family at a bank item that does not exist (BANK-15 -> BANK-150)',
     lambda f, o: f['families'][0].update({'official_bank_ancestor': 'BANK-150'}),
     'C39'),
]

# Bank mutations need the bank document, which the family mutations do not
# take. Kept as a separate table rather than widening every lambda above.
BANK_MUTATIONS = [
    ('duplicate a bank_item_id',
     lambda b: b['items'][1].update({'bank_item_id': b['items'][0]['bank_item_id']}),
     'C29'),
    ('renumber a bank item so id and number disagree (BANK-015 -> 150)',
     lambda b: b['items'][0].update({'bank_item_number': 150}), 'C30'),
    ('remove a bank item that a family cites',
     lambda b: b['items'].pop(0), 'C11|C39'),
    ('blank a bank item text',
     lambda b: b['items'][0].update({'text_verbatim': '   '}), 'C31'),
    ('alter a bank item text away from the extract',
     lambda b: b['items'][0].update(
         {'text_verbatim': b['items'][0]['text_verbatim'].replace(
             'Chief Engineer', 'Second Engineer')}), 'C32'),
    ('point the bank at a source the manifest does not hold',
     lambda b: b.update({'source_id': 'SRC-NOT-REAL'}), 'C35'),
]

# Date-derivation mutations. These are the ones Phase 2 could not catch: the
# fields stay internally consistent and only the evidence is missing.
DATE_MUTATIONS = [
    ('promote a bank-only family to date_confidence HIGH',
     lambda f, o: f['families'][0].update({'date_confidence': 'HIGH'}), 'C36'),
    ('give a bank-only family a date and a HIGH confidence, consistently',
     lambda f, o: f['families'][0].update(
         {'date_confidence': 'HIGH', 'earliest_occurrence': '2010-06',
          'latest_occurrence': '2010-06'}), 'C36|C37'),
    ('advance a bank-only family to DATE_VERIFIED with matching fields',
     lambda f, o: f['families'][0].update(
         {'publication_status': 'DATE_VERIFIED', 'date_confidence': 'HIGH'}),
     'C36|C38'),
    ('rest a PRIOR sitting on the question bank alone',
     lambda f, o: _rest_prior_on_bank(f, o), 'C36|C37|C38'),
    ('strip the dated source from every prior occurrence',
     lambda f, o: _strip_prior_sources(f, o), 'C36|C37|C38'),
]


def _prior_records(fam_doc, occ_rows):
    """Occurrence records that are not the family's current recurrence."""
    currents = {(fm.get('current_recurrence') or '').strip()
                for fm in fam_doc['families']}
    out = []
    for r in occ_rows:
        tag = '%s%s' % (r.get('question_id') or '', r.get('limb_label') or '')
        if tag and tag not in currents:
            out.append(r)
    return out


def _rest_prior_on_bank(fam_doc, occ_rows):
    prior = _prior_records(fam_doc, occ_rows)
    if not prior:
        raise AssertionError('no prior occurrence exists to mutate')
    for r in prior:
        r['source_ids'] = ['SRC-DGS-QBANK-ARCHIVED']


def _strip_prior_sources(fam_doc, occ_rows):
    prior = _prior_records(fam_doc, occ_rows)
    if not prior:
        raise AssertionError('no prior occurrence exists to mutate')
    for r in prior:
        r['source_ids'] = []


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

    extracted = load_extracted_bank()

    rep = validate(fam, occ, manifest, bank, specs, hist_ids, Report(),
                   extracted)
    print('QI-v2 family validator')
    print('  families    : %d' % len(fam['families']))
    print('  occurrences : %d' % len(occ))
    print('  bank items  : %d' % len(bank['items']))
    print('  extract     : %s' % ('%d items' % len(extracted) if extracted
                                  else 'ABSENT - two checks skipped'))
    print('  checks run  : %d' % len(rep.checks))
    if rep.skipped:
        print('  SKIPPED     : %d' % len(rep.skipped))
        for s in rep.skipped:
            print('    ~ %s' % s)
    if rep.failures:
        print('  FAILURES    : %d' % len(rep.failures))
        for f in rep.failures:
            print('    - %s' % f)
    else:
        print('  FAILURES    : 0')

    if not args.mutate:
        return 1 if rep.failures else 0

    bad = 0

    def run_table(title, table, kind):
        held = 0
        print('\n%s' % title)
        print('%-64s %-12s %s' % ('MUTATION', 'EXPECT', 'RESULT'))
        print('-' * 104)
        for name, mutate, expect in table:
            f2, o2, b2 = (copy.deepcopy(fam), copy.deepcopy(occ),
                          copy.deepcopy(bank))
            try:
                if kind == 'bank':
                    mutate(b2)
                else:
                    mutate(f2, o2)
            except Exception as exc:                              # noqa: BLE001
                print('%-64s %-12s SETUP ERROR %s' % (name[:64], expect, exc))
                held += 1
                continue
            r2 = validate(f2, o2, manifest, b2, specs, hist_ids, Report(),
                          extracted)
            fired = {fl.split(' ')[0] for fl in r2.failures}
            ok = bool(fired & set(expect.split('|')))
            held += 0 if ok else 1
            print('%-64s %-12s %s'
                  % (name[:64], expect,
                     'caught' if ok else 'ESCAPED (fired: %s)' % sorted(fired)))
        print('-' * 104)
        print('%s: %d   escaped: %d' % (title.split(' -')[0], len(table), held))
        return held

    bad += run_table('family and occurrence mutations - each must fire a named check',
                     MUTATIONS, 'family')
    bad += run_table('bank referential mutations', BANK_MUTATIONS, 'bank')
    bad += run_table('date-derivation mutations - fields stay consistent, '
                     'only the evidence is missing', DATE_MUTATIONS, 'family')

    total = len(MUTATIONS) + len(BANK_MUTATIONS) + len(DATE_MUTATIONS)
    print('\nmutations: %d   escaped: %d' % (total, bad))
    return 1 if (rep.failures or bad) else 0


if __name__ == '__main__':
    sys.exit(main())
