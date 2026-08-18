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
import hashlib
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qi_paths                                                   # noqa: E402
import qi_similarity as qs                                        # noqa: E402

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

# The manifest entry that declares the extract's bytes and sha256.
BANK_SOURCE_ID = 'SRC-DGS-QBANK-ARCHIVED'

# Every check downstream of the extract says exactly this and nothing else, so
# one missing file produces one explanation rather than six rival ones.
UNAVAILABLE = 'unavailable - C46 REQUIRED_SOURCE_MISSING'

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
    """The 185-item extract, and the reason it is unusable if it is.

    Returns ``(items, problem)``. ``problem`` is None when the extract loaded;
    otherwise it is a one-line statement of what is wrong with the file, and
    ``items`` is None.

    Phase 3A returned a bare None here and every caller read it as "this
    machine has no intake directory", which was true then: the extract lived
    outside the repository. Phase 3A.1 committed it, and that inverted the
    meaning of absence without anyone revisiting this function. The Laptop
    review measured the consequence - deleting one tracked file switched off
    C32, C33 and the whole C40-C42 ancestor guard, dropped the check count from
    200 to 170, and the validator reported success. Absence is now a checkout
    or tampering failure, and the distinction is the caller's to enforce.
    """
    if not os.path.exists(EXTRACTED_BANK):
        return None, 'file does not exist'
    try:
        raw = load_json(EXTRACTED_BANK)
    except Exception as exc:                                      # noqa: BLE001
        return None, 'file is not readable as JSON (%s)' % exc
    if not isinstance(raw, dict) or not isinstance(raw.get('items'), dict):
        return None, 'file has no "items" object'
    try:
        items = {int(k): v for k, v in raw['items'].items()}
    except (TypeError, ValueError) as exc:
        return None, 'item numbers are not integers (%s)' % exc
    if any(not isinstance(v, type(u'')) or not v.strip()
           for v in items.values()):
        return None, 'one or more items carry no text'
    return items, None


def extract_integrity(manifest, rep):
    """C46/C47: the required source is present, and it is the required bytes.

    C46 is the ROOT check. Everything C32-C34 and C40-C42 assert is downstream
    of it, so when C46 fails those report as unavailable rather than each
    inventing its own explanation of the same single fact.

    C47 verifies the manifest's recorded sha256 against the bytes actually
    checked out, not against a remembered value. The manifest has carried
    `extracted_json_sha256` since Phase 3A.1 and nothing read it, so the
    extract could be edited freely as long as the edit kept 185 well-formed
    items. Hashing the raw bytes also holds the line on the CRLF trap:
    `.gitattributes` pins *.json to LF, and if that pin were ever lost this
    check is what notices.
    """
    items, problem = load_extracted_bank()
    ok = rep.check('C46 the required DGS bank extract is present and loadable',
                   problem is None,
                   'REQUIRED_SOURCE_MISSING: %s - %s'
                   % (EXTRACTED_BANK, problem))
    if not ok:
        return None

    blob = io.open(EXTRACTED_BANK, 'rb').read()
    got = hashlib.sha256(blob).hexdigest().upper()
    want, want_bytes = None, None
    for src in manifest.get('sources', []):
        if src.get('source_id') == BANK_SOURCE_ID:
            want = (src.get('extracted_json_sha256') or '').upper()
            want_bytes = src.get('extracted_json_bytes')
    detail = ('extract is %d bytes sha256 %s; the manifest declares %s bytes '
              'sha256 %s' % (len(blob), got, want_bytes, want))
    rep.check('C47 the bank extract is the bytes the manifest declares',
              bool(want) and got == want and len(blob) == want_bytes, detail)
    return items


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
             extracted=None, documents=None, filenames=None):
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
        for name in ('C32 curated bank text matches the 185-item extract',
                     'C33 the (Oct-05) annotation is derived, not remembered',
                     'C34 the extract still holds all 185 items'):
            rep.check(name, False, UNAVAILABLE)
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

    bank_ancestor_semantics(fam_doc, occ_by_id, specs, extracted, rep)
    occurrence_stem_fidelity(occ_rows, specs, rep)
    family_month_fidelity(fam_doc, occ_by_id,
                          load_documents() if documents is None else documents,
                          rep)

    src_by_id = {s['source_id']: s for s in manifest.get('sources', [])}

    evidence_filename_dates(
        occ_rows, src_by_id,
        verification_filenames() if filenames is None else filenames, rep)

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

    phase3b_inventory(occ_rows, rep)

    return rep


# Phase 3B ---------------------------------------------------------------------

INVENTORY = os.path.join(V2, 'PHASE3B_SOURCE_INVENTORY.json')

ORIGIN_CONFIDENCE = ('AUTHENTIC_OFFICIAL_ARCHIVE',
                     'OFFICIAL_ORIGIN_HIGH_CONFIDENCE',
                     'LIKELY_OFFICIAL', 'UNVERIFIED')
DATE_STATUS = ('MONTH_AND_YEAR_PRINTED', 'YEAR_PRINTED_MONTH_UNKNOWN',
               'NO_DATE_PRINTED', 'SAMPLE_PAPER_NOT_A_SITTING',
               'NOT_A_QUESTION_PAPER')
DOC_TYPE = ('QUESTION_PAPER', 'SAMPLE_QUESTION_PAPER', 'EXAM_RESULT_LIST')


def phase3b_inventory(occ_rows, rep):
    """C48-C52: the archived-source inventory may not assert a date it cannot
    print, and nothing that is not a dated question paper may become history.

    Phase 3B acquisition found two traps that these checks freeze shut. The
    first is a whole population of official DGS files that look like Class I
    papers by name and by path and are actually candidate result lists carrying
    no question text at all. The second is an official Management-level paper
    that prints "SAMPLE PAPER" and was nevertheless carried as a dated sitting.
    Both would have become dated history on the strength of a filename.
    """
    if not os.path.exists(INVENTORY):
        rep.check('C48 the Phase-3B source inventory is present and loadable',
                  False, 'missing: %s' % INVENTORY)
        return
    try:
        with io.open(INVENTORY, encoding='utf-8-sig') as fh:
            inv = json.load(fh)
        srcs = inv['sources']
    except Exception as exc:                                      # noqa: BLE001
        rep.check('C48 the Phase-3B source inventory is present and loadable',
                  False, 'unreadable: %s' % exc)
        return
    rep.check('C48 the Phase-3B source inventory is present and loadable',
              bool(srcs), 'sources: %d' % len(srcs))

    bad = [s.get('source_id') for s in srcs
           if s.get('document_type') not in DOC_TYPE
           or s.get('paper_date_status') not in DATE_STATUS
           or s.get('official_origin_confidence') not in ORIGIN_CONFIDENCE]
    rep.check('C49 every archived source uses the governed enums',
              not bad, 'off-enum: %s' % bad[:8])

    # A month may exist ONLY where the paper printed a month.
    month_no_evidence = [
        s.get('source_id') for s in srcs
        if s.get('sitting_month') is not None
        and s.get('paper_date_status') != 'MONTH_AND_YEAR_PRINTED']
    rep.check('C50 no archived source carries a month it did not print',
              not month_no_evidence, 'asserted: %s' % month_no_evidence[:8])

    # A sample paper and a result list are not sittings, ever.
    not_sittings = [
        s.get('source_id') for s in srcs
        if s.get('document_type') in ('SAMPLE_QUESTION_PAPER', 'EXAM_RESULT_LIST')
        and (s.get('sitting_month') is not None
             or s.get('paper_date_status') == 'MONTH_AND_YEAR_PRINTED')]
    rep.check('C51 no sample paper or result list is dated as a sitting',
              not not_sittings, 'dated: %s' % not_sittings[:8])

    # Forward guard: if an occurrence ever cites an archived source, that source
    # must be a question paper that printed its own month.
    ok_ids = set(s.get('source_id') for s in srcs
                 if s.get('document_type') == 'QUESTION_PAPER'
                 and s.get('paper_date_status') == 'MONTH_AND_YEAR_PRINTED')
    all_ids = set(s.get('source_id') for s in srcs)
    illegal = []
    for o in occ_rows:
        for sid in (o.get('source_ids') or []):
            if sid in all_ids and sid not in ok_ids:
                illegal.append((o.get('occurrence_id'), sid))
    rep.check('C52 no occurrence rests on an undated or non-paper archived source',
              not illegal, 'illegal: %s' % illegal[:8])


# Classes that count as a family genuinely descending from a bank item.
ANCESTOR_FIT = ('EXACT_REPEAT', 'NEAR_VERBATIM', 'SAME_CORE_ASK')


def _declared_ancestors(fam):
    """A family may declare a primary and a secondary bank ancestor.

    FAMILY-EM-0004 is the live case and it is deliberate: the warranties limb
    recurs against BANK-085 in 2021 and 2022, while its CURRENT recurrence is
    limb (b) of QP2608-Q4, whose parent is BANK-072. Both are real ancestry and
    the schema records both, so an integrity check that knew only about the
    primary would report a defect where there is none.
    """
    return [fam[k] for k in ('official_bank_ancestor', 'secondary_bank_ancestor')
            if fam.get(k)]


def _ancestor_number(anc):
    try:
        return int(str(anc).split('-')[-1])
    except (ValueError, TypeError):
        return None


def _family_fit(fam, bank_stem, occ_by_id, specs, stem_cache):
    """Best class any of the family's own occurrences reaches against a stem.

    A one-word limb such as `Warranties` is UNSCOREABLE_SHORT_STEM on its own
    and inherits from its parent question, which is the rule LIMB_MODEL.md
    already states. Max over occurrences is right: a family legitimately holds
    narrowed and absorbed variants alongside its representative.
    """
    best = -1
    for oid in fam.get('known_occurrences') or []:
        o = occ_by_id.get(oid)
        if not o:
            continue
        key = ('occ', oid)
        if key not in stem_cache:
            stem_cache[key] = qs.Stem(o.get('raw_stem') or '')
        r = qs.classify(stem_cache[key], bank_stem)
        if r.cls == 'UNSCOREABLE_SHORT_STEM':
            parent = (specs.get(o.get('question_id')) or {}).get('text') or ''
            if parent:
                pkey = ('q', o.get('question_id'))
                if pkey not in stem_cache:
                    stem_cache[pkey] = qs.Stem(parent)
                r = qs.classify(stem_cache[pkey], bank_stem)
        best = max(best, qs._RANK.get(r.cls, -1))
    return best


MONTH_NAMES = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5,
               'june': 6, 'july': 7, 'august': 8, 'september': 9,
               'october': 10, 'november': 11, 'december': 12}

# `15 March 2026` is a commencement date, not a sitting: a day number in front
# of the month means the text is dating an event, not naming a paper.
_MONTH_YEAR = re.compile(
    r'(?<!\d\s)\b(%s)\s+(\d{4})\b' % '|'.join(MONTH_NAMES), re.I)
_FAMILY_ID = re.compile(r'FAMILY-EM-\d{4}')


def load_documents():
    """Every markdown file in the layer, read once."""
    out = {}
    for fn in sorted(os.listdir(V2)):
        if fn.endswith('.md'):
            out[fn] = io.open(os.path.join(V2, fn), encoding='utf-8').read()
    return out


# A date token inside a filename: `JUN2010`, `2010-06`, or a bare year.
# `QP2608` is a paper id in MIW's own YYMM form, not a year, and does not match.
_FILENAME_DATE = re.compile(
    r'(?:(%s)[_-]?((?:19|20)\d{2}))|(?<![0-9A-Za-z])((?:19|20)\d{2})(?![0-9])'
    % '|'.join(MONTHS), re.I)


def evidence_filename_dates(occ_rows, src_by_id, filenames, rep):
    """C45: a canonical evidence filename may not claim a date it cannot prove.

    Laptop's original Phase-2 defect L-3, unrepaired through Phase 3A. The five
    files under verification/ were named H1_QP2608_Q1_JUN2010.md through
    H5_QP2608_Q8B_MAR2010.md. Their bodies were careful — each framed its date
    as the claim under adjudication — but a filename is the part that gets
    indexed, linked and quoted out of context, and these asserted five sittings
    the layer has never evidenced.

    The rule is not "no dates in filenames". It is the same rule the rest of
    the layer runs on: a date must come from a dated source. A filename may
    carry a date the occurrence records can actually derive, and no other.
    """
    supported = set()
    for o in occ_rows:
        if not date_evidence(o, src_by_id):
            continue
        y, m = o.get('source_year'), o.get('source_month')
        if y and m and str(m).upper()[:3] in MONTHS:
            supported.add((int(y), MONTHS[str(m).upper()[:3]]))

    problems = []
    for path in sorted(filenames):
        base = os.path.basename(path)
        for mon, yr1, yr2 in _FILENAME_DATE.findall(base):
            if mon:
                pair = (int(yr1), MONTHS[mon.upper()[:3]])
                shown = '%s%s' % (mon, yr1)
            else:
                # A bare year cannot be evidenced by a month-precise record,
                # so it is refused outright in an evidence filename.
                problems.append('%s encodes the year %s, which no dated source '
                                'supports' % (base, yr2))
                continue
            if pair not in supported:
                problems.append('%s encodes %s, which no dated source supports'
                                % (base, shown))

    rep.check('C45 no evidence filename encodes an unevidenced date',
              not problems, '; '.join(problems))


def verification_filenames():
    d = os.path.join(V2, 'verification')
    if not os.path.isdir(d):
        return []
    return [os.path.join(d, f) for f in sorted(os.listdir(d))
            if f.endswith('.md')]


def _blocks(text):
    """Split a markdown document into blank-line separated blocks."""
    out, cur = [], []
    for line in text.split('\n'):
        if line.strip():
            cur.append(line)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def family_month_fidelity(fam_doc, occ_by_id, documents, rep):
    """C44: a prose section headed by one family may not cite another's months.

    This is the guard for the defect the Laptop review found live in two
    write-ups. `MERCHANT_SHIPPING_ACT_AUTHORITY.md` was headed *Temporal delta
    for FAMILY-EM-0008* and then described five casualty sittings from March
    2023 to July 2025 — FAMILY-EM-0009's data exactly — and
    `PROTOTYPE_EVIDENCE_CLASSES.md` repeated the mistake in its worked example.
    Both are prose, so no schema check could have caught them, and the
    consequence was real: the Part XII mapping gate ended up attached to the
    wrong family, leaving the casualty family ungated.

    A heading naming exactly one family binds the section that follows. Every
    sitting month the section then names must be one that family actually sat.
    A line that names some other family releases the binding for that line,
    because cross-references are legitimate and common.
    """
    months = {}
    for fam in fam_doc['families']:
        got = set()
        for oid in fam.get('known_occurrences') or []:
            o = occ_by_id.get(oid)
            if not o:
                continue
            y, m = o.get('source_year'), o.get('source_month')
            if y and m and str(m).upper()[:3] in MONTHS:
                got.add((int(y), MONTHS[str(m).upper()[:3]]))
        # A month the family itself records as ASSERTED BUT NOT COUNTED is a
        # legitimate thing for its own write-up to discuss — that is the whole
        # point of keeping the assertion visible rather than deleting it.
        for u in fam.get('unverified_asserted_occurrences') or []:
            for name, year in _MONTH_YEAR.findall(json.dumps(u)):
                got.add((int(year), MONTH_NAMES[name.lower()]))
        months[fam['family_id']] = got

    problems = []
    for fn in sorted(k for k in documents if not k.startswith('__')):
        bound, header = None, None
        # A blank line ends a block. The binding is released for a whole block
        # that names another family, not merely for the line that names it:
        # a correction note explaining that EM-0009's data was once filed under
        # EM-0008 must be free to give EM-0008's months in its own sentences.
        for block in _blocks(documents[fn]):
            head = [l for l in block if l.startswith('#')]
            if head:
                ids = set(_FAMILY_ID.findall(head[-1]))
                bound = sorted(ids)[0] if len(ids) == 1 else None
                header = head[-1].strip()[:60]
            if not bound or not months.get(bound):
                continue
            body = '\n'.join(l for l in block if not l.startswith('#'))
            if set(_FAMILY_ID.findall(body)) - {bound}:
                continue
            for name, year in _MONTH_YEAR.findall(body):
                pair = (int(year), MONTH_NAMES[name.lower()])
                if pair not in months[bound]:
                    problems.append(
                        '%s: section %r cites %s %s, which %s never sat'
                        % (fn, header, name, year, bound))

    rep.check('C44 a section headed by a family cites only its own sittings',
              not problems, '; '.join(sorted(set(problems))))


def bank_ancestor_semantics(fam_doc, occ_by_id, specs, extracted, rep):
    """C40-C42: the RIGHT bank ancestor, not merely a valid one.

    The Laptop review's independent corruption LC-3 escaped every Phase-3A
    check: swap two families' ancestors and every id is still real, unique,
    present in the curated file and byte-identical to the official extract.
    Nothing asked whether the item a family points at is the item its own
    questions actually descend from. That is not a hypothetical class of error
    — the EM-0008/EM-0009 mislabel was live in the write-ups at the same time.
    """
    if extracted is None:
        for name in ('C40 occurrence ancestors lie within the family declaration',
                     'C41 the family representative fits its declared ancestor',
                     'C42 no undeclared bank item fits the family better'):
            rep.check(name, False, UNAVAILABLE)
        return

    bank_stems = {}
    for num, text in extracted.items():
        bank_stems[num] = qs.Stem(text)
    stem_cache = {}

    for fam in fam_doc['families']:
        fid = fam['family_id']
        declared = _declared_ancestors(fam)
        if not declared:
            continue
        nums = set()
        bad_num = []
        for a in declared:
            n = _ancestor_number(a)
            if n is None or n not in extracted:
                bad_num.append(a)
            else:
                nums.add(n)

        # C40 -- every ancestor an occurrence declares must be one the family
        # declares. This is the cheapest possible guard on the exact defect
        # class and it is exact, not heuristic.
        seen = set()
        for oid in fam.get('known_occurrences') or []:
            o = occ_by_id.get(oid)
            if o and o.get('official_bank_ancestor'):
                seen.add(o['official_bank_ancestor'])
        undeclared = sorted(seen - set(declared))
        rep.check('C40 %s occurrence ancestors lie within the family declaration'
                  % fid, not undeclared,
                  'occurrences cite %s, family declares %s'
                  % (undeclared, sorted(declared)))

        if bad_num or not nums:
            rep.check('C41 %s the family representative fits its declared '
                      'ancestor' % fid, False,
                      'ancestor(s) %s do not resolve in the extract' % bad_num)
            continue

        # C41 -- the PRIMARY ancestor must actually fit.
        primary = _ancestor_number(fam.get('official_bank_ancestor'))
        pf = _family_fit(fam, bank_stems[primary], occ_by_id, specs, stem_cache)
        rep.check('C41 %s the family representative fits its declared ancestor'
                  % fid, pf >= qs._RANK['SAME_CORE_ASK'],
                  'best occurrence reaches %s against BANK-%03d, which is below '
                  'SAME_CORE_ASK' % (qs._UNRANK.get(pf, pf), primary))

        # C42 -- and no item the family has NOT declared may fit it better.
        # This is what makes a wrong-but-valid substitution fail: the swapped-in
        # item cannot outrank the one the family really descends from.
        best_declared = max(_family_fit(fam, bank_stems[n], occ_by_id, specs,
                                        stem_cache) for n in nums)
        rivals = []
        for num, bs in bank_stems.items():
            if num in nums:
                continue
            if _family_fit(fam, bs, occ_by_id, specs, stem_cache) > best_declared:
                rivals.append('BANK-%03d' % num)
        rep.check('C42 %s no undeclared bank item fits the family better' % fid,
                  not rivals,
                  'undeclared %s outrank the declared ancestor(s) %s at %s'
                  % (rivals, sorted(declared), qs._UNRANK.get(best_declared)))


def occurrence_stem_fidelity(occ_rows, specs, rep):
    """C43: the preserved historical stem must be the stem the paper prints.

    P3A-6. Actor is load-bearing in the classifier now, so an unverified actor
    inside a raw_stem is a real hole: C7/C8 validate the limb label and the
    marks against the spec, but nothing validated the text. Occurrences whose
    paper is not in the solved corpus cannot be checked against it; they are
    listed by name rather than passed over, so the unverifiable set cannot grow
    silently.
    """
    def norm(x):
        return re.sub(r'[^a-z0-9]', '', (x or '').lower())

    mismatched, unverifiable = [], []
    for o in occ_rows:
        oid = o.get('occurrence_id')
        if not oid:
            continue
        spec = specs.get(o.get('question_id'))
        if not spec:
            unverifiable.append('%s (%s not in the solved corpus)'
                                % (oid, o.get('question_id')))
            continue
        stem = norm(o.get('raw_stem'))
        if not stem:
            mismatched.append('%s: empty raw_stem' % oid)
            continue
        candidates = [spec.get('text') or '']
        lab = o.get('limb_label')
        if lab:
            candidates.append((spec.get('subpart_text') or {}).get(lab, ''))
        if not any(stem in norm(c) or (norm(c) and norm(c) in stem)
                   for c in candidates):
            mismatched.append('%s: raw_stem is not the text %s prints'
                              % (oid, o.get('question_id')))

    rep.check('C43 every raw_stem matches the text its own spec prints',
              not mismatched, '; '.join(mismatched))
    rep.check('C43b the unverifiable-stem set is exactly the papers outside '
              'the corpus', len(unverifiable) == UNVERIFIABLE_STEM_BUDGET,
              'expected %d unverifiable, got %d: %s'
              % (UNVERIFIABLE_STEM_BUDGET, len(unverifiable), unverifiable))


# Occurrences whose source paper predates the solved corpus, so their stems
# cannot be checked against a spec. Held as an explicit number so that a new
# unverifiable stem is a FAILURE rather than a silent addition to the set.
UNVERIFIABLE_STEM_BUDGET = 4


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
            labels, marks, texts = set(), {}, {}
            for sp in (q.get('subparts') or []):
                if sp.get('label'):
                    labels.add(sp['label'])
                    marks[sp['label']] = sp.get('marks')
                    texts[sp['label']] = sp.get('text') or ''
            specs[q['question_id']] = {'labels': labels, 'marks': marks,
                                       'total_marks': q.get('total_marks'),
                                       'text': q.get('text_verbatim') or '',
                                       'subpart_text': texts}
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

    # -- Phase 3A.1: the Laptop review's LC-3, which escaped Phase 3A --------
    # Every id below stays real, unique, curated and byte-identical to the
    # official extract. Only the ATTACHMENT is wrong.
    ('swap the ancestors of two families (every id stays real)',
     lambda f, o: _swap_ancestors(f), 'C40|C41|C42'),
    ('replace a correct ancestor with a different VALID curated bank item',
     lambda f, o: f['families'][0].update(
         {'official_bank_ancestor': 'BANK-160'}), 'C40|C41|C42'),
    ('corrupt a preserved historical stem (invert the actor)',
     lambda f, o: o[0].update(
         {'raw_stem': (o[0]['raw_stem'] or '').replace(
             'Chief Engineer', 'Port State Control officer')}), 'C43'),
]


def _swap_ancestors(fam_doc):
    a, b = fam_doc['families'][0], fam_doc['families'][1]
    a['official_bank_ancestor'], b['official_bank_ancestor'] = (
        b['official_bank_ancestor'], a['official_bank_ancestor'])

# Document mutations corrupt an in-memory copy of the markdown tree. A
# validator self-test must never write to the tree it is validating, so these
# take the loaded documents rather than touching disk.
DOC_MUTATIONS = [
    ('re-label a family section with another family id (the live defect)',
     lambda d: d.__setitem__(
         'MERCHANT_SHIPPING_ACT_AUTHORITY.md',
         _require_replace(d['MERCHANT_SHIPPING_ACT_AUTHORITY.md'],
                          '## 5. Temporal delta for FAMILY-EM-0009',
                          '## 5. Temporal delta for FAMILY-EM-0008')),
     'C44'),
    ('re-date an evidence filename with an unsupported sitting',
     lambda d: d.__setitem__(
         '__filenames__',
         list(d.get('__filenames__') or [])
         + ['verification/H1_QP2608_Q1_JUN2010.md']), 'C45'),
    ('give a worked example another family\'s sitting months',
     lambda d: d.__setitem__(
         'PROTOTYPE_EVIDENCE_CLASSES.md',
         _require_replace(d['PROTOTYPE_EVIDENCE_CLASSES.md'],
                          '  March 2023 · July 2023',
                          '  October 2024 · July 2023')),
     'C44'),
]


def _require_replace(text, old, new):
    if old not in text:
        raise AssertionError('mutation target %r not present' % old)
    return text.replace(old, new, 1)


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


# Required-source mutations. These corrupt the extract FILE rather than the
# in-memory documents, because the defect the Laptop review found was in how
# the file's absence was interpreted, and no in-memory mutation can reach that.
# Each returns the bytes to write in place of the real extract (None = delete
# the file), plus an optional edit to the manifest entry that declares its hash.
def _drop_item(blob):
    d = json.loads(blob.decode('utf-8'))
    d['items'].pop(sorted(d['items'], key=int)[0])
    return json.dumps(d, ensure_ascii=False, indent=2).encode('utf-8')


def _tamper_item(blob):
    d = json.loads(blob.decode('utf-8'))
    k = sorted(d['items'], key=int)[0]
    d['items'][k] = d['items'][k] + ' and state the penalty.'
    return json.dumps(d, ensure_ascii=False, indent=2).encode('utf-8')


def _to_crlf(blob):
    return blob.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')


EXTRACT_MUTATIONS = [
    ('delete the required bank extract',
     lambda blob: (None, None), 'C46'),
    ('leave the extract unparseable as JSON',
     lambda blob: (b'{"items": {1: broken', None), 'C46'),
    ('strip the items object out of the extract',
     lambda blob: (b'{"note": "no items here"}', None), 'C46'),
    ('blank the text of one extract item',
     lambda blob: (json.dumps(
         dict(json.loads(blob.decode('utf-8')),
              items=dict(json.loads(blob.decode('utf-8'))['items'],
                         **{'1': '   '})),
         ensure_ascii=False).encode('utf-8'), None), 'C46'),
    ('remove one of the 185 items',
     lambda blob: (_drop_item(blob), None), 'C34|C47'),
    ('alter the canonical text of one item',
     lambda blob: (_tamper_item(blob), None), 'C32|C47'),
    ('re-encode the extract with CRLF line endings',
     lambda blob: (_to_crlf(blob), None), 'C47'),
    ('change the declared sha256 without touching the file',
     lambda blob: (blob, {'extracted_json_sha256': '0' * 64}), 'C47'),
    ('change the declared byte count without touching the file',
     lambda blob: (blob, {'extracted_json_bytes': 1}), 'C47'),
]


INVENTORY_MUTATIONS = [
    ('give a year-only paper a month it never printed',
     lambda d: _inv_set(d, 'YEAR_PRINTED_MONTH_UNKNOWN', {'sitting_month': 6}),
     'C50'),
    ('date the SAMPLE paper as a February sitting',
     lambda d: _inv_set(d, 'SAMPLE_PAPER_NOT_A_SITTING',
                        {'sitting_month': 2,
                         'paper_date_status': 'MONTH_AND_YEAR_PRINTED'}),
     'C50|C51'),
    ('promote a candidate result list to a dated question paper',
     lambda d: _inv_set(d, 'NOT_A_QUESTION_PAPER',
                        {'paper_date_status': 'MONTH_AND_YEAR_PRINTED',
                         'sitting_month': 10}),
     'C50|C51'),
    ('invent an off-enum provenance class',
     lambda d: _inv_set(d, None, {'official_origin_confidence': 'PROBABLY_FINE'}),
     'C49'),
    ('delete the inventory entirely',
     lambda d: None,
     'C48'),
]


def _inv_set(doc, date_status, patch):
    """Patch the first source matching `date_status` (or the first source)."""
    for src in doc['sources']:
        if date_status is None or src.get('paper_date_status') == date_status:
            src.update(patch)
            return doc
    raise AssertionError('no inventory source with status %s' % date_status)


def run_inventory_mutations(fam, occ, manifest, bank, specs, hist_ids,
                            extracted, documents, filenames):
    """Prove the Phase-3B date guards are load-bearing.

    The real inventory is never modified: each variant is written to a
    temporary directory and the module's INVENTORY pointer is moved onto it.
    """
    import shutil
    import tempfile

    global INVENTORY
    real = INVENTORY
    base = json.load(io.open(real, encoding='utf-8-sig'))
    tmp = tempfile.mkdtemp(prefix='qi-inv-mut-')
    held = 0
    print('')
    print('archived-source mutations - a date may not appear without evidence')
    print('%-64s %-12s %s' % ('MUTATION', 'EXPECT', 'RESULT'))
    print('-' * 104)
    try:
        for name, mutate, expect in INVENTORY_MUTATIONS:
            path = os.path.join(tmp, 'PHASE3B_SOURCE_INVENTORY.json')
            if os.path.exists(path):
                os.remove(path)
            doc = mutate(copy.deepcopy(base))
            if doc is not None:
                io.open(path, 'w', encoding='utf-8').write(
                    json.dumps(doc, indent=1, ensure_ascii=False))
            INVENTORY = path

            r2 = Report()
            validate(copy.deepcopy(fam), copy.deepcopy(occ), manifest,
                     copy.deepcopy(bank), specs, hist_ids, r2, extracted,
                     dict(documents), list(filenames))
            fired = set(fl.split(' ')[0] for fl in r2.failures)
            ok = bool(fired & set(expect.split('|')))
            held += 0 if ok else 1
            print('%-64s %-12s %s'
                  % (name[:64], expect,
                     'caught' if ok else 'ESCAPED (fired: %s)' % sorted(fired)))
    finally:
        INVENTORY = real
        shutil.rmtree(tmp, ignore_errors=True)
    print('-' * 104)
    print('archived-source: %d   escaped: %d' % (len(INVENTORY_MUTATIONS), held))
    return held


def run_extract_mutations(fam, occ, manifest, bank, specs, hist_ids,
                          documents, filenames):
    """Prove the required source cannot go missing quietly.

    The real extract is never modified: each mutation writes its variant into a
    temporary directory and repoints the module's EXTRACTED_BANK at it, so a
    crash mid-table cannot leave the repository holding a corrupted file.
    """
    import shutil
    import tempfile

    global EXTRACTED_BANK
    real = EXTRACTED_BANK
    blob = io.open(real, 'rb').read()
    tmp = tempfile.mkdtemp(prefix='qi-extract-mut-')
    held = 0
    print('\nrequired-source mutations - the extract may not go missing quietly')
    print('%-64s %-12s %s' % ('MUTATION', 'EXPECT', 'RESULT'))
    print('-' * 104)
    try:
        for name, mutate, expect in EXTRACT_MUTATIONS:
            new_blob, man_edit = mutate(blob)
            path = os.path.join(tmp, 'dgs_meo_cl1_bank_items.json')
            if os.path.exists(path):
                os.remove(path)
            if new_blob is not None:
                io.open(path, 'wb').write(new_blob)
            EXTRACTED_BANK = path

            m2 = copy.deepcopy(manifest)
            if man_edit:
                for src in m2.get('sources', []):
                    if src.get('source_id') == BANK_SOURCE_ID:
                        src.update(man_edit)

            r2 = Report()
            ext2 = extract_integrity(m2, r2)
            validate(copy.deepcopy(fam), copy.deepcopy(occ), manifest,
                     copy.deepcopy(bank), specs, hist_ids, r2, ext2,
                     dict(documents), list(filenames))
            fired = {fl.split(' ')[0] for fl in r2.failures}
            ok = bool(fired & set(expect.split('|')))
            held += 0 if ok else 1
            print('%-64s %-12s %s'
                  % (name[:64], expect,
                     'caught' if ok else 'ESCAPED (fired: %s)' % sorted(fired)))
    finally:
        EXTRACTED_BANK = real
        shutil.rmtree(tmp, ignore_errors=True)
    print('-' * 104)
    print('required-source: %d   escaped: %d' % (len(EXTRACT_MUTATIONS), held))
    return held


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

    rep0 = Report()
    extracted = extract_integrity(manifest, rep0)
    documents = load_documents()
    filenames = verification_filenames()

    rep = validate(fam, occ, manifest, bank, specs, hist_ids, rep0,
                   extracted, documents, filenames)
    print('QI-v2 family validator')
    print('  families    : %d' % len(fam['families']))
    print('  occurrences : %d' % len(occ))
    print('  bank items  : %d' % len(bank['items']))
    print('  extract     : %s'
          % ('%d items' % len(extracted) if extracted
             else 'UNUSABLE - required source; see C46'))
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
            d2 = dict(documents)
            d2['__filenames__'] = list(filenames)
            try:
                if kind == 'bank':
                    mutate(b2)
                elif kind == 'doc':
                    mutate(d2)
                else:
                    mutate(f2, o2)
            except Exception as exc:                              # noqa: BLE001
                print('%-64s %-12s SETUP ERROR %s' % (name[:64], expect, exc))
                held += 1
                continue
            fn2 = d2.pop('__filenames__', list(filenames))
            r2 = validate(f2, o2, manifest, b2, specs, hist_ids, Report(),
                          extracted, d2, fn2)
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
    bad += run_table('document mutations - the family a write-up NAMES must be '
                     'the family it DESCRIBES', DOC_MUTATIONS, 'doc')
    bad += run_extract_mutations(fam, occ, manifest, bank, specs, hist_ids,
                                 documents, filenames)
    bad += run_inventory_mutations(fam, occ, manifest, bank, specs, hist_ids,
                                   extracted, documents, filenames)

    total = (len(MUTATIONS) + len(BANK_MUTATIONS) + len(DATE_MUTATIONS)
             + len(DOC_MUTATIONS) + len(EXTRACT_MUTATIONS)
             + len(INVENTORY_MUTATIONS))
    print('\nmutations: %d   escaped: %d' % (total, bad))
    return 1 if (rep.failures or bad) else 0


if __name__ == '__main__':
    sys.exit(main())
