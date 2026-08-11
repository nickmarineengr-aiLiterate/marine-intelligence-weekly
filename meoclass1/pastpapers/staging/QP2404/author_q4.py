#!/usr/bin/env python3
"""QP2404-Q4 - rudder-efficiency devices.

Tier D by REVERSE-HINT ADJUDICATION. Donor QP2506-Q1 (June 2025), whose printed
stem differs from this one by two words after normalisation ('to'->'in',
'improvements'->'improvement'). MIW adjudicated the pair as the SAME examiner
task this session; the exact-equality family rule could not see it.

Direction: the donor is a LATER sitting pulled BACKWARDS to April 2024.
"""
import copy, json, io, sys

SPECS = 'F:/Marine-Intelligence-Weekly/meoclass1/pastpapers/specs/'
tgt = json.load(io.open(SPECS + 'QP2404.json', encoding='utf-8'))
don = json.load(io.open(SPECS + 'QP2506.json', encoding='utf-8'))

D = [q for q in don['questions'] if q['question_id'] == 'QP2506-Q1'][0]
Q = [q for q in tgt['questions'] if q['question_id'] == 'QP2404-Q4'][0]

# ---- clone the verified structure (route, answer, learning layer) ------------
CLONE = ('decomposition', 'model_answer', 'study_notes', 'sources', 'unresolved',
         'regulations', 'search_aliases', 'understand_first', 'memory_cue',
         'decomposition_gate', 'provenance_summary', 'reverify_before_publication',
         'quick_revision', 'answer_route', 'retrieval_cards')
for k in CLONE:
    if k in D:
        Q[k] = copy.deepcopy(D[k])

# ---- re-anchor identity -----------------------------------------------------
for i, c in enumerate(Q['retrieval_cards']):
    c['id'] = 'QP2404-Q4-C%d' % (i + 1)

Q['answer_status'] = 'Pilot Review Ready'
Q['verification_file'] = 'verification/QP2404/Q4.md'
Q['recurrence_class'] = 'near_recurrence'

# ---- the donor relationship, recorded ---------------------------------------
Q['reuse_tier'] = 'D'
Q['reused_from'] = 'QP2506-Q1'
Q['question_delta'] = (
    'Printed stem identical to QP2506-Q1 (June 2025) except two words: this sitting '
    'prints "contribute to improving" where the donor prints "contribute in improving", '
    'and "rudder-efficiency improvements devices" where the donor prints "improvement '
    'devices". Neither touches the examiner demand. Marks delta NIL - both print '
    '4 + 4 + 4 + 4 = 16 over the same four named devices. Temporal delta NIL on the '
    'hydrodynamics and NIL on the regulatory framing: EEXI and the operational carbon '
    'intensity rating applied from 1 January 2023, before both sittings.')
Q['reuse_evidence'] = [
    'DONOR BY REVERSE-HINT ADJUDICATION. The host annotation on the June 2025 copy '
    'names this April 2024 sitting, but a host hint points only backwards, so the link '
    'was invisible from this question. It was surfaced by REVERSE_HINT_CANDIDATES.md and '
    'adjudicated this session by reading both printed stems.',
    'WHY THE FAMILY MODEL COULD NOT SEE IT. A family edge forms on reused_from or on '
    'EXACT equality of the normalised stem. These two stems differ by two words, so no '
    'edge existed and this question derived as tier C with no donor - a full fresh-research '
    'question - when a verified answer to the same task already existed.',
    'WHAT WAS REUSED: the six-step route and the verified mechanism of each of the four '
    'devices. WHAT WAS REWRITTEN: the corpus-position claim (the donor called itself the '
    'first naval-architecture question in the solved set, which is no longer true), the '
    'cross-link, the temporal note and the regulatory framing, all re-derived for April 2024.',
]

# ---- April 2024 temporal re-anchoring ---------------------------------------
Q['temporal_review'] = {
    'state': 'TEMPORAL REVIEW COMPLETE',
    'risk': 'LOW',
    'classes': [],
    'notes': [
        'CHECKED, NO TEMPORAL ISSUE ON THE TECHNICAL CONTENT. Hydrodynamics is not dated '
        'law. All four devices predate this sitting by decades - the vane wheel was '
        'patented by Grim in 1966 - and nothing in the physics turns on the sitting date.',
        'THE REGULATORY FRAMING IN STEP 6 WAS RE-DERIVED, NOT INHERITED. The Energy '
        'Efficiency Existing Ship Index and the operational carbon intensity rating under '
        'MARPOL Annex VI chapter 4 applied from 1 January 2023, so both were operative at '
        'this sitting and are correctly cited as the retrofit driver. The 2023 IMO GHG '
        'Strategy (MEPC 80, July 2023) was also already adopted.',
        'DELIBERATELY ABSENT. The IMO Net-Zero Framework is not mentioned - it is far later '
        'than this sitting. FuelEU Maritime is not mentioned as applying: Regulation (EU) '
        '2023/1805 was adopted in September 2023 but applies only from 1 January 2025, after '
        'this paper. The EU Emissions Trading System had been extended to maritime transport '
        'from 1 January 2024 and so WAS in force at this sitting, but it is not asserted here '
        'because the donor did not rely on it and this answer does not need it.',
    ],
    'sitting': 'April 2024',
}
Q['decomposition_gate']['freshness_risk'] = (
    'LOW - hydrodynamics is not dated law and all four devices predate this sitting by '
    'decades. The only dated material is the regulatory framing, which is confined to '
    'instruments applying from 1 January 2023, before April 2024.')

# ---- the donor's cross-link does not exist on this paper ---------------------
# QP2506 Q2 was "why an approved IMO measure may not yet bind the ship". QP2404 Q2
# is ammonia as a marine fuel, and at THIS sitting the live example of exactly that
# distinction is that no IMO instrument yet governed ammonia as fuel. Re-pointed
# deliberately, not renumbered by accident.
Q['cross_links'] = [{
    'label': 'QP2404 Q2 - a fuel the IMO framework had not yet reached at this sitting',
    'href': 'QP2404.html#q2',
}]

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qpio import save
save(tgt)
print('QP2404-Q4 authored from QP2506-Q1; cards:', len(Q['retrieval_cards']),
      '; route steps:', len(Q['answer_route']['steps']))
