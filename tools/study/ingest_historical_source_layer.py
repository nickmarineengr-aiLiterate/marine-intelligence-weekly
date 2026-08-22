#!/usr/bin/env python3
"""Ingest the ADOPTED source layer of the 2010-2020 historical Written recovery.

    origin/research/historical-written-qi-2010-2020   (RESEARCH, never merged)
        PAPER_INVENTORY_2010_2020.json  +  DATE_CERTAINTY.json
                          |
                          |  this tool -- provenance fields ONLY
                          v
    docs/study/historical_source_layer.json           (GOVERNED)

WHAT WAS ADOPTED, AND WHAT WAS NOT
----------------------------------
The Laptop adjudication of 2026-08-23 adopted the SOURCE LAYER only: the
identity, provenance, hash and claimed sitting date of 115 archived pages.
It did NOT adopt the occurrence layer (question stems) and did NOT adopt the
recurrence joins. This tool therefore refuses to copy question text, and the
validator below refuses an artefact that contains any.

Three claims were separated, and they are NOT the same claim:

  A  QUESTION TEXT     "this wording existed on the archived source page"
                       CORROBORATED. Every page is hashed and re-obtainable,
                       and 8 of the 9 official DG Shipping Question Bank items
                       committed to the phase3b research branch match an
                       archived stem (5 of them exactly). The wording is
                       authentic MEO Class I examinable wording.

  B  SITTING DATE      "this question belonged to the YYYY-MM sitting"
                       SECONDARY CLAIM ONLY. Every one of the 115 papers is
                       MONTH_YEAR_CLAIMED_BY_SECONDARY_SOURCE. Nothing
                       official dates any of it.

  C  OFFICIAL          "DG Shipping administered this exact question then"
     OCCURRENCE        NOT ESTABLISHED. The DGS result lists prove only that
                       sittings occurred, in 7 named months, and they date no
                       question at all.

Because B is a secondary claim, this artefact may feed INTERNAL recurrence
analysis and may never, by itself, license a public dated claim. That
threshold split is enforced in code by evidence_model.date_certainty_gate().

Usage:
    python tools/study/ingest_historical_source_layer.py           # write
    python tools/study/ingest_historical_source_layer.py --check   # fail if stale
"""
import argparse, io, json, os, subprocess, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

OUT = os.path.join(ROOT, 'docs', 'study', 'historical_source_layer.json')

SCHEMA = 'miw.study.historical_source_layer.v1'

# The research commit this layer was adjudicated against. Pinned, not floating:
# a later research commit must be re-adjudicated, not silently absorbed.
RESEARCH_REF = '2b22cd4636ed2c3d61d99efc982bd1c966357771'
RESEARCH_BRANCH = 'research/historical-written-qi-2010-2020'
RESEARCH_DIR = 'research/historical-written-qi'

EXPECTED_PAPERS = 115
EXPECTED_STEMS = 1026
EXPECTED_ENTITIES = 256

# Provenance fields only. Every field here describes the PAGE, never a
# question. If a field name that could carry wording ever appears in this
# list, validate() must start failing.
CARRY = ('source_id', 'set_id', 'sitting_date_claim', 'date_certainty',
         'source_class', 'provider', 'original_url', 'archive_url',
         'archive_timestamp', 'sha256', 'bytes', 'questions_stated',
         'questions_extracted', 'completeness', 'answers_recoverable',
         'verification_status')

# Fields that would mean question content had leaked into the source layer.
FORBIDDEN = ('raw_wording', 'normalized_wording', 'text', 'text_verbatim',
             'questions', 'occurrences', 'limb_labels_detected',
             'source_asserted_recurrences', 'family_joins',
             'modern_corpus_joins')


def read_research(name):
    """Read one research artefact from the pinned commit WITHOUT checking it out."""
    path = f'{RESEARCH_DIR}/{name}.json'
    try:
        blob = subprocess.run(['git', 'show', f'{RESEARCH_REF}:{path}'],
                              cwd=ROOT, capture_output=True, check=True).stdout
    except subprocess.CalledProcessError:
        raise SystemExit(
            f'FAIL R-HSL-SOURCE: cannot read {path} at {RESEARCH_REF[:7]}. '
            f'Fetch the research branch first:\n'
            f'    git fetch origin {RESEARCH_BRANCH}')
    return json.loads(blob.decode('utf-8'))


def build():
    inv = read_research('PAPER_INVENTORY_2010_2020')
    gaps = read_research('GAP_REPORT')

    papers = []
    for p in sorted(inv['papers'], key=lambda x: x['set_id']):
        papers.append({k: p[k] for k in CARRY if k in p})

    years = sorted({p['sitting_date_claim'][:4] for p in papers})
    by_year = {}
    for p in papers:
        by_year[p['sitting_date_claim'][:4]] = \
            by_year.get(p['sitting_date_claim'][:4], 0) + 1

    return {
        'schema': SCHEMA,
        'generated_by': 'tools/study/ingest_historical_source_layer.py',
        'status': 'ADOPTED_SOURCE_LAYER_ONLY',
        'adopted_on': '2026-08-23',
        'adopted_by': 'laptop-adjudication',
        'what_this_is': (
            'The identity, provenance, hash and CLAIMED sitting date of 115 '
            'archived pages carrying MEO Class I Engineering Management '
            'question stems for 2010-2020. Each record is a re-obtainable '
            'recipe: archive_url + sha256.'),
        'what_this_is_not': (
            'NOT question text, NOT answers, NOT occurrences, NOT recurrence '
            'joins, and NOT proof that any question was officially set in the '
            'month claimed. It adds no question to any MIW count and licenses '
            'no public dated claim on its own.'),
        'claim_separation': {
            'A_question_text_existed_on_the_page': 'CORROBORATED',
            'A_basis': (
                '115 pages hashed and re-obtainable; 8 of the 9 official DG '
                'Shipping Question Bank items committed on the phase3b '
                'research branch match an archived stem, 5 of them exactly. '
                'The wording is authentic MEO Class I examinable wording.'),
            'B_question_belonged_to_that_sitting': 'CLAIMED_BY_SECONDARY_SOURCE',
            'B_basis': (
                'DieselShip set identity only. Zero papers reach '
                'MONTH_YEAR_CERTAIN. The per-sitting stem was additionally '
                'never captured separately: the research layer stores the '
                "source ENTITY's canonical wording once and replicates it "
                'across every sitting it asserts, so 1,026 occurrence records '
                'carry only 263 distinct wordings.'),
            'C_officially_administered_in_that_sitting': 'NOT_ESTABLISHED',
            'C_basis': (
                'The DGS archive yields result lists, not question papers. '
                'They name 7 distinct sitting months (2013-08, 2013-10, '
                '2013-11, 2014-01, 2014-04, 2015-01, 2015-09) inside a '
                '2013-08..2015-09 envelope, are recorded as DISCOVERED with '
                'no sha256 -- referenced, not retrieved -- and they date no '
                'question text whatsoever.'),
        },
        'internal_use_policy': (
            'PERMITTED. Secondary-claimed sitting dates are sufficient for '
            'INTERNAL recurrence and dormancy analysis, because an internal '
            'model that is wrong about a month costs a study-priority nudge. '
            'They are not sufficient for a public dated claim, where being '
            'wrong costs the corpus its credibility. The two thresholds are '
            'deliberately different and are enforced separately.'),
        'public_use_policy': (
            'FORBIDDEN. No public surface may state or imply a dated '
            'historical span on the strength of this layer. See '
            'evidence_model.date_certainty_gate(): a coverage status can '
            'never license a public dated claim while the underlying dates '
            'are secondary-claimed.'),
        'recurrence_joins_status': (
            'NOT ADOPTED. The research layer counts joins per OCCURRENCE, '
            'which restates one entity-level decision once per asserted '
            'sitting: 83 family joins collapse to 18 entity-family decisions, '
            '1,873 modern join pairs to 287, and 895 asserted-link checks to '
            '147. Eleven of the twelve HIGH_CONFIDENCE family joins are the '
            'same single question. The joins are sound evidence and an '
            'inflated count; they are re-adjudicated at entity granularity '
            'before any of them may move a roadmap number.'),
        'research_provenance': {
            'branch': RESEARCH_BRANCH,
            'commit': RESEARCH_REF,
            'directory': RESEARCH_DIR,
            'merged_into_main': False,
            'note': ('The research branch is NOT merged. This artefact is '
                     'derived from a PINNED commit, so a later research '
                     'commit must be re-adjudicated rather than silently '
                     'absorbed.'),
        },
        'coverage': {
            'window': '2010-01 .. 2020-12',
            'papers_total': len(papers),
            'stems_evidenced_on_pages': sum(p['questions_extracted']
                                            for p in papers),
            'distinct_source_entities': EXPECTED_ENTITIES,
            'papers_by_year': dict(sorted(by_year.items())),
            'earliest_year': int(years[0]),
            'latest_year': int(years[-1]),
            'note': ('stems_evidenced_on_pages counts stems VISIBLE on the '
                     'archived pages. None of them is ingested as a MIW '
                     'question and none is counted anywhere else.'),
        },
        'month_gaps': [
            {'months': 'MAY 2010-2019 (10 months)',
             'classification': 'NO_SOURCE_PAGE',
             'no_sitting_evidence': 'INFERRED_NOT_EVIDENCED',
             'detail': ("No May set appears on the source's own index for any "
                        'year 2010-2019, which is consistent with an '
                        '~11-sittings-per-year calendar. That is an inference '
                        'from one secondary index, not evidence that no '
                        'examination was held. Recorded as UNKNOWN.')},
            {'months': '2020-04 .. 2020-09 (6 months)',
             'classification': 'NO_SOURCE_PAGE',
             'no_sitting_evidence': 'EXTERNALLY_PLAUSIBLE_NOT_EVIDENCED',
             'detail': ('Absent from the source index. The COVID suspension '
                        'is externally well known but is not evidenced by any '
                        'artefact held in this repository.')},
            {'months': '2010-09 (1 month)',
             'classification': 'NO_ARCHIVE_CAPTURE',
             'no_sitting_evidence': 'SITTING_SOURCE_PAGE_KNOWN_TO_EXIST',
             'detail': ('The set exists on the live source index; no HTTP-200 '
                        'archive capture exists. This is the only one of the '
                        '17 absent months that is a pure acquisition gap.')},
        ],
        'gap_report_from_research': gaps['gaps'],
        'papers': papers,
    }


def validate(doc):
    """Fail closed. The whole value of this layer is that it under-claims."""
    e = []
    if doc.get('schema') != SCHEMA:
        e.append(f'schema is {doc.get("schema")!r}')
    if doc.get('status') != 'ADOPTED_SOURCE_LAYER_ONLY':
        e.append('status is not ADOPTED_SOURCE_LAYER_ONLY')
    papers = doc.get('papers') or []
    if len(papers) != EXPECTED_PAPERS:
        e.append(f'{len(papers)} papers, expected {EXPECTED_PAPERS}')
    if doc['coverage']['stems_evidenced_on_pages'] != EXPECTED_STEMS:
        e.append('stems_evidenced_on_pages does not match the research layer')

    # No question content may exist anywhere in this artefact.
    blob = json.dumps(doc)
    for f in FORBIDDEN:
        if f'"{f}"' in blob:
            e.append(f'forbidden content field {f!r} leaked into the source layer')

    seen_hash, seen_id = set(), set()
    for p in papers:
        if p.get('date_certainty') != 'MONTH_YEAR_CLAIMED_BY_SECONDARY_SOURCE':
            e.append(f'{p.get("set_id")}: date_certainty overclaims '
                     f'({p.get("date_certainty")})')
        if p.get('source_class') != 'SECONDARY_REPOSITORY_VIA_ARCHIVE':
            e.append(f'{p.get("set_id")}: source_class overclaims')
        if p.get('verification_status') != 'VERIFIED':
            e.append(f'{p.get("set_id")}: not VERIFIED')
        if not p.get('sha256') or not p.get('archive_url'):
            e.append(f'{p.get("set_id")}: not re-obtainable (missing hash/url)')
        if p.get('sha256') in seen_hash:
            e.append(f'{p.get("set_id")}: duplicate sha256 -- two sets cannot '
                     f'be the same page')
        if p.get('set_id') in seen_id:
            e.append(f'{p.get("set_id")}: duplicate set_id')
        if p.get('answers_recoverable'):
            e.append(f'{p.get("set_id")}: claims recoverable answers')
        seen_hash.add(p.get('sha256'))
        seen_id.add(p.get('set_id'))
    return e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    doc = build()
    errors = validate(doc)
    if errors:
        print(f'FAIL R-HSL-VALID -- {len(errors)} error(s)')
        for line in errors[:15]:
            print('  ' + line)
        return 1

    text = json.dumps(doc, indent=2, ensure_ascii=False) + '\n'
    if args.check:
        if not os.path.exists(OUT) or open(OUT, encoding='utf-8').read() != text:
            print('FAIL: docs/study/historical_source_layer.json is missing '
                  'or stale')
            return 1
        print(f'historical source layer -- up to date '
              f'({len(doc["papers"])} papers, adopted source layer only)')
        return 0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    c = doc['coverage']
    print(f'wrote {os.path.relpath(OUT, ROOT)}')
    print(f'  {c["papers_total"]} archived pages, {c["window"]}, all '
          f'MONTH_YEAR_CLAIMED_BY_SECONDARY_SOURCE')
    print(f'  {c["stems_evidenced_on_pages"]} stems visible on those pages -- '
          f'NONE ingested as a MIW question')
    print(f'  question text  {doc["claim_separation"]["A_question_text_existed_on_the_page"]}')
    print(f'  sitting date   {doc["claim_separation"]["B_question_belonged_to_that_sitting"]}')
    print(f'  official occ.  {doc["claim_separation"]["C_officially_administered_in_that_sitting"]}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
