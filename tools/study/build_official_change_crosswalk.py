#!/usr/bin/env python3
"""Build docs/study/official_change_crosswalk.json -- draft(23) to final(25).

THIS IS NOT docs/study/official_crosswalk.json
----------------------------------------------
`official_crosswalk.json` is the official-node -> MIW-topic layer, 43 edges,
hand-adjudicated, source-verified on both sides. It is unaffected by this file.

THIS file is the draft-to-final RELATIONSHIP layer: how the 28-Jul-2026 draft
Annexure III (23 items) relates to the 15-Aug-2026 final Annexure III (25
items).

WHY EVERY RECORD HERE IS UNVERIFIED
-----------------------------------
The draft PDF is NOT in this repository. Its digest, URL, date and item count
are pinned -- and that is all. No draft text has been extracted, so no
item-to-item comparison has been performed by any tool. The only account of
the difference is a NARRATIVE TABLE written by a human in
docs/study/SYLLABUS_SOURCE_STATUS.md section 3.

A narrative is not a derivation. So every record here carries
provenance NARRATIVE_UNVERIFIED, classification AMBIGUOUS and
review_required true, and the file says so in its own authority field. When
the draft is acquired, this builder is where the real comparison goes; until
then no consumer may treat any record here as a settled relationship.

The narrative's own arithmetic is reported, not repaired: 8 unchanged + 5 minor
+ 12 substantive = 25, and 2 new are listed on top of that, which cannot be
reconciled against 23 draft items and 25 final items. Whether the 2 new are
inside the 25 or additional to it is exactly the kind of question only the
draft source can answer.

Determinism: no clock is read.

Usage:
    python tools/study/build_official_change_crosswalk.py
"""
import io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import mapping_engine as ME

OFFICIAL = os.path.join(ROOT, 'docs', 'study', 'official_syllabus.json')
OUT = os.path.join(ROOT, 'docs', 'study', 'official_change_crosswalk.json')
STATUS_DOC = 'docs/study/SYLLABUS_SOURCE_STATUS.md'

DRAFT_DIGEST = ('b6365d2205428f34283b9e259c8a130b4b4dfd2072f52cd1d96141348a2'
                '1d09c')
DRAFT_DATE = '2026-07-28'
DRAFT_ITEMS = 23
FINAL_DIGEST = ('07170f572c99064fad25eedb0fe985886248a81a49b4eb5d4711fd38d18'
                '6f44d')

# The narrative counts, quoted from SYLLABUS_SOURCE_STATUS.md section 3.
# Reproduced, not adopted: nothing in this repository can currently confirm or
# contradict them.
NARRATIVE_COUNTS = {'unchanged': 8, 'minor_text_change': 5,
                    'substantively_changed': 12, 'new_in_final': 2}

# What the narrative says about specific final items, keyed by official number.
# These are the narrative's own words about that item, carried so a later
# reviewer can check them against the draft when it is acquired. They do NOT
# classify the record: every classification below stays AMBIGUOUS.
NARRATIVE_NOTES = {
    3:  'narrative names the RO Code and classification societies\' duty of '
        'care as a final-only addition to this item',
    8:  'narrative names the Universal Declaration of Human Rights and the '
        'ICCPR as final-only additions to the MLC/ILO item',
    9:  'narrative names detention review panels and appeal procedures as '
        'final-only additions to this item',
    16: 'narrative names sensor-technology fundamentals as a final-only '
        'addition to this item',
    21: 'narrative names dual-fuel engines and alternative-fuel supervisory '
        'competence as final-only additions to this item',
    22: 'narrative names EU-waters GHG restrictions as a final-only addition '
        'to this item',
    23: 'narrative names management-level cyber-risk oversight under the ISM '
        'Code as a final-only addition to this item',
    24: 'narrative names this item (casualty investigation) as NEW in the '
        'final',
    25: 'narrative names this item (underwater noise) as NEW in the final',
}

CLASSIFICATION_VOCABULARY = [
    'UNCHANGED', 'RENAMED', 'MOVED', 'MERGED', 'SPLIT', 'EXPANDED', 'REDUCED',
    'NEW', 'REMOVED', 'AMBIGUOUS',
]


def build():
    official = json.load(open(OFFICIAL, encoding='utf-8'))
    records = []
    for node in sorted(official['nodes'], key=lambda n: n['official_node_id']):
        num = node['official_number']
        records.append({
            'final_official_node_id': node['official_node_id'],
            'final_official_number': num,
            'final_official_label': ' '.join(
                node['official_text'].split())[:160].rstrip() + '...',
            'final_source_page': node.get('source_page'),
            'draft_item_number': None,
            'draft_item_text': None,
            'classification': 'AMBIGUOUS',
            'provenance': 'NARRATIVE_UNVERIFIED',
            'review_required': True,
            'basis': (f'{STATUS_DOC} section 3, narrative table. The draft '
                      f'source is absent from this repository, so no draft '
                      f'text was read and no item-to-item comparison was '
                      f'performed.'),
            'narrative_note': NARRATIVE_NOTES.get(num),
            'source_verified': False,
        })
    return {
        'schema': 'miw.study.official_change_crosswalk.v1',
        'schema_version': '1.0',
        'generated_by': 'tools/study/build_official_change_crosswalk.py',
        'hand_editable': False,
        'authority': (
            'DRAFT SIDE UNVERIFIED AND AWAITING SOURCE ACQUISITION. The '
            '28-Jul-2026 draft circular is ABSENT from this repository: only '
            'its digest, URL, date and item count are pinned. No draft text '
            'has been extracted and no item-to-item comparison has been '
            'performed by any tool. The draft side of every relationship in '
            'this file rests on the narrative table in '
            + STATUS_DOC + ' section 3 and on nothing else. Every record is '
            'therefore classified AMBIGUOUS with provenance '
            'NARRATIVE_UNVERIFIED and review_required true. No record here is '
            'source-verified, and no consumer may treat one as settled. This '
            'file is DISTINCT from docs/study/official_crosswalk.json, which '
            'remains the official-node to MIW-topic layer and is unaffected.'),
        'what_this_is_not': (
            'Not the official-to-MIW-topic crosswalk. Not a derivation from '
            'draft text. Not evidence that any particular final item did or '
            'did not change.'),
        'draft_source': {
            'status': 'ABSENT_FROM_REPOSITORY_AWAITING_ACQUISITION',
            'date': DRAFT_DATE,
            'sha256': DRAFT_DIGEST,
            'item_count': DRAFT_ITEMS,
            'url': ('https://dgma.gov.in/ -- the draft circular listing; the '
                    'file itself is not held here and was not fetched'),
            'text_extracted': False,
        },
        'final_source': {
            'circular': official['source']['circular'],
            'annex': official['annex']['annex_id'],
            'sha256': FINAL_DIGEST,
            'syllabus_version': ME.OFFICIAL_VERSION,
            'item_count': len(official['nodes']),
            'text_extracted': True,
        },
        'narrative_counts': {
            'source': STATUS_DOC + ' section 3',
            'confirmed_by_source_comparison': False,
            **NARRATIVE_COUNTS,
            'arithmetic_observation': (
                'unchanged 8 + minor 5 + substantive 12 = 25, and 2 new are '
                'listed in addition, which reconciles with neither 23 draft '
                'items nor 25 final items. No source-derived comparison was '
                'available to confirm or contradict the narrative counts, so '
                'the discrepancy is reported here rather than reconciled '
                'away.'),
        },
        'classification_vocabulary': CLASSIFICATION_VOCABULARY,
        'classification_note': (
            'The vocabulary is declared so that a later source-derived pass '
            'has somewhere to write. Until the draft is acquired every record '
            'uses AMBIGUOUS.'),
        'counts': {
            'records': len(records),
            'source_verified': 0,
            'narrative_unverified': len(records),
            'review_required': len(records),
        },
        'records': records,
    }


def main():
    payload = build()
    body = json.dumps(payload, indent=2, ensure_ascii=False) + '\n'
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(body)
    print('wrote docs/study/official_change_crosswalk.json '
          f"({payload['counts']['records']} records)")
    print('  every record: classification=AMBIGUOUS provenance='
          'NARRATIVE_UNVERIFIED review_required=true')
    print('  narrative counts (unconfirmed): '
          + json.dumps(NARRATIVE_COUNTS))
    print('  draft source: ABSENT_FROM_REPOSITORY_AWAITING_ACQUISITION')
    return 0


if __name__ == '__main__':
    sys.exit(main())
