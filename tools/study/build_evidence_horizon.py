#!/usr/bin/env python3
"""Build docs/study/written_evidence_horizon.json.

One place answers "what evidence does a roadmap number actually rest on?".
Two layers, kept apart:

  CURRENT_SOLVED_WRITTEN    derived by counting the specs. Grows by itself.
  HISTORICAL_WRITTEN_QI     declared, deliberately unpopulated.

`discovered_assets` is an INVENTORY, not coverage. Listing an asset here does
not add a single question to any count -- it tells the recovery session where
to look. Nothing consumes it as evidence, which is why an asset can be
recorded honestly as RESEARCH_ONLY without inflating a public claim.

Determinism: no clock. `generated_from` is the corpus's own newest `updated`.

Usage:
    python tools/study/build_evidence_horizon.py            # write
    python tools/study/build_evidence_horizon.py --check    # fail if stale
"""
import argparse, glob, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import evidence_model as EM
import mapping_engine as ME

SPECS = os.path.join(ROOT, 'meoclass1', 'pastpapers', 'specs', '*.json')
OUT = os.path.join(ROOT, 'docs', 'study', 'written_evidence_horizon.json')

# Bounded inventory, 2026-08-22. Recorded so the recovery session does not
# repeat the search -- and so nobody concludes from silence that the work
# never existed.
DISCOVERED_ASSETS = [
    {
        'asset': 'meoclass1/pastpapers/intelligence/historical_qp_intelligence.json',
        'location': 'main (committed)',
        'classification': 'FOUND_AND_CURRENT',
        'schema': 'miw.pastpapers.historical_qp_intelligence.v2',
        'status': 'INTELLIGENCE_ONLY',
        'papers': 30,
        'questions': 270,
        'coverage': '2021-2023 sittings',
        'note': ('Printed question wording and rubric only -- no model answer, '
                 'and none may be authored without a Founder decision. Already '
                 'regenerable via tools/pastpapers/extract_historical_questions.py.'),
    },
    {
        'asset': 'meoclass1/pastpapers/intelligence/v2/QUESTION_FAMILIES.json',
        'location': 'origin/research/question-intelligence-v2-phase3b (UNMERGED)',
        'classification': 'FOUND_PARTIAL',
        'schema': 'miw.pastpapers.qi_v2.families.v2',
        'status': 'RESEARCH_ONLY',
        'families': 9,
        'families_counted': 7,
        'excluded_from_families': 7,
        'coverage': '2021-02 to 2026-08 (occurrence-verified)',
        'note': ('Carries the dormancy vocabulary this evidence model adopts. '
                 'Families key on (question_id, limb_label) because recurrence '
                 'is observed at LIMB level, not whole-question level.'),
    },
    {
        'asset': 'meoclass1/pastpapers/intelligence/v2/QUESTION_OCCURRENCES.jsonl',
        'location': 'origin/research/question-intelligence-v2-phase3b (UNMERGED)',
        'classification': 'FOUND_PARTIAL',
        'schema': 'miw.pastpapers.qi_v2.occurrence.v2',
        'status': 'RESEARCH_ONLY',
        'occurrence_records': 25,
        'coverage': '2021-2026',
        'note': ('raw_stem preserves historical wording exactly; '
                 'normalized_stem is for fingerprinting only. Sittings are '
                 'never collapsed into one another.'),
    },
    {
        'asset': 'meoclass1/pastpapers/intelligence/v2/PHASE3B_SOURCE_INVENTORY.json',
        'location': 'origin/research/question-intelligence-v2-phase3b (UNMERGED)',
        'classification': 'FOUND_PARTIAL',
        'status': 'RESEARCH_ONLY',
        'objects': 98,
        'question_papers': 80,
        'coverage': '1999-2005 archived DG Shipping papers',
        'note': ('The single largest untapped source: 80 archived DGS MEO '
                 'Class I question papers, 17 of them Engineering Management. '
                 'But 58 print a YEAR ONLY (mostly 2001) and 17 print no date '
                 'at all, so sitting-level dating is unresolved for most.'),
    },
    {
        'asset': 'meoclass1/pastpapers/intelligence/v2/OFFICIAL_BANK_ITEMS.json',
        'location': 'origin/research/question-intelligence-v2-phase3b (UNMERGED)',
        'classification': 'FOUND_PARTIAL',
        'status': 'RESEARCH_ONLY',
        'items': 185,
        'coverage': 'undated',
        'note': ("The DG Shipping's own published 'Question Bank MEO CL-I'. "
                 'Bank ancestry proves a question EXISTS officially; it dates '
                 'nothing.'),
    },
    {
        'asset': 'docs/study/historical_source_layer.json',
        'location': 'main (committed)',
        'classification': 'FOUND_AND_ADOPTED_AS_SOURCE_LAYER',
        'schema': 'miw.study.historical_source_layer.v1',
        'status': 'ADOPTED_SOURCE_LAYER_ONLY',
        'papers': 115,
        'questions': 0,
        'coverage': '2010-2020 archived source pages (provenance only)',
        'note': ('Adjudicated 2026-08-23. Identity, hash and CLAIMED sitting '
                 'month of 115 archived pages; 1,026 stems are VISIBLE on '
                 'those pages and NONE is ingested as a MIW question, which '
                 'is why questions is 0. Question text is corroborated -- 8 '
                 'of the 9 official DGS Question Bank items held on the '
                 'phase3b branch match an archived stem -- but every sitting '
                 'DATE is MONTH_YEAR_CLAIMED_BY_SECONDARY_SOURCE. Feeds '
                 'internal recurrence work only; licenses no public claim.'),
    },
    {
        'asset': 'research/historical-written-qi/ (occurrences + joins)',
        'location': ('origin/research/historical-written-qi-2010-2020 '
                     '@ 2b22cd4 (UNMERGED)'),
        'classification': 'FOUND_NOT_ADOPTED',
        'status': 'RESEARCH_ONLY',
        'papers': 115,
        'questions': 1026,
        'coverage': '2010-2020 question stems and recurrence candidates',
        'note': ('The occurrence and join layers were reviewed and NOT '
                 'adopted. Joins are counted per occurrence, which restates '
                 'one entity-level decision once per asserted sitting: 83 '
                 'family joins collapse to 18 entity-family decisions, 1,873 '
                 'modern join pairs to 287, and 895 asserted-link checks to '
                 '147, with 11 of the 12 HIGH_CONFIDENCE family joins being '
                 'one and the same question. The evidence is sound and the '
                 'COUNT is inflated, so it is re-adjudicated at entity '
                 'granularity before it may move any number.'),
    },
    {
        'asset': 'MEO Class I written papers for sittings 2006-2009',
        'location': 'not acquired',
        'classification': 'NOT_FOUND_ON_ACCESSIBLE_LAPTOP_STATE',
        'status': 'ABSENT',
        'coverage': 'none',
        'note': ('Sets for 2006-2009 exist on the secondary source index but '
                 'were deliberately left unacquired. CORRECTION 2026-08-23: '
                 'this entry previously read "2006-2020 ... nowhere reachable '
                 'from this machine". That was true of the laptop state when '
                 'written and is now false -- the Desktop found a route to '
                 '2010-2020. The genuinely missing band is 2006-2009, plus '
                 'the 1999-2005 papers which are a different subject family.'),
    },
]


def build():
    current = EM.current_written_horizon(SPECS)

    # The socket stays NOT_STARTED on purpose. The 2010-2020 SOURCE layer is
    # adopted (docs/study/historical_source_layer.json) but no question from it
    # is ingested, so the QI coverage layer -- which is what drives counts and
    # the public claim -- genuinely holds nothing yet. Saying PARTIAL here
    # would put a number on a layer that has none.
    historical = EM.empty_qi_socket(
        'NOT_STARTED',
        known_gaps=[
            {'from_year': 2006, 'to_year': 2009,
             'reason': 'no accessible source on this machine'},
            {'from_year': 2010, 'to_year': 2020,
             'reason': ('source layer ADOPTED 2026-08-23 and questions NOT '
                        'ingested; sitting dates are '
                        'MONTH_YEAR_CLAIMED_BY_SECONDARY_SOURCE, so this '
                        'window can never reach VALIDATED_RANGE on the '
                        'present evidence')},
        ],
        source_status='SOURCE_LAYER_ADOPTED_QUESTIONS_NOT_INGESTED',
    )
    errors = EM.assert_honest(historical)
    if errors:
        raise SystemExit('FAIL R-QI-HONEST: ' + '; '.join(errors))

    specs = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(SPECS))]
    generated_from = max(s.get('updated', '') for s in specs)

    return {
        'schema_version': EM.EVIDENCE_MODEL_VERSION,
        'generated_by': 'tools/study/build_evidence_horizon.py',
        'generated_from': generated_from,
        'authority': ('Derived. Every count is computed from the governed '
                      'corpora; none is asserted.'),
        'versions': {
            'evidence_model_version': EM.EVIDENCE_MODEL_VERSION,
            'written_qi_schema_version': EM.WRITTEN_QI_SCHEMA_VERSION,
            'official_syllabus_version': ME.OFFICIAL_VERSION,
            'operative_syllabus_version': ME.SYLLABUS_VERSION,
        },
        'layers': {
            'current_solved_written': current,
            'historical_written_qi': historical,
        },
        'public_claim': {
            'derived_sentence': EM.public_evidence_claim(current, historical),
            'policy': ('Public copy is GENERATED from this file. Until the '
                       'historical layer reaches VALIDATED_RANGE, no surface '
                       'may claim a span wider than the current layer states.'),
            'date_certainty_policy': (
                'A dated public claim is gated on DATE_CERTAINTY, never on '
                'coverage. See evidence_model.date_certainty_gate(): the '
                'historical layer may be COMPLETE and still barred, because '
                'holding the papers is not the same as an official document '
                'saying when they were set. The 2010-2020 layer is '
                'SECONDARY_CLAIMED and is therefore barred indefinitely on '
                'the present evidence, however much coverage it gains.'),
            'forbidden_until_validated': [
                'based on 16 years of papers',
                '2010-2026 analysis',
                'appeared N times since 2010',
                'since 2010',
                'asked since 2010',
                'papers from 2010',
                '16 years of question intelligence',
            ],
        },
        'discovered_assets': DISCOVERED_ASSETS,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    text = json.dumps(build(), indent=2, ensure_ascii=False) + '\n'
    if args.check:
        if not os.path.exists(OUT) or open(OUT, encoding='utf-8').read() != text:
            print('FAIL: docs/study/written_evidence_horizon.json is missing or stale')
            return 1
        print('evidence horizon -- up to date')
        return 0

    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    built = json.loads(text)
    c = built['layers']['current_solved_written']
    h = built['layers']['historical_written_qi']
    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    print(f"  current    {c['papers_total']} papers / {c['questions_total']} questions "
          f"({c['earliest_sitting']} .. {c['latest_sitting']})")
    print(f"  historical {h['status']} -- gaps {h['known_gaps']}")
    print(f"  claim      {built['public_claim']['derived_sentence']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
