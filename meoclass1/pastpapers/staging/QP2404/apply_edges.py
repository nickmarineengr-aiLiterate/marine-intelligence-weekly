#!/usr/bin/env python3
"""Land the three adjudicated QP2404 reverse-hint edges as DATA ONLY.

No answers are written. Each edge records an MIW ruling that two printed stems
set the SAME examiner task, made by reading both stems this session. The stored
reuse_tier is INTAKE metadata and is deliberately left alone - donor readiness is
derived, never stored.

Effect: QP2404-Q4 gains a verified donor (C -> D derived); QP2506-Q1 and
QP2602-Q6 stop rendering "Once in this set", which they were doing wrongly.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qpio import load, q, save

spec = load('QP2404')

EDGES = {
    'Q4': dict(
        donor='QP2506-Q1',
        delta=(
            'ADJUDICATED SAME EXAMINER TASK. Normalised stems differ by two words: this '
            'sitting prints "contribute to improving" and "improvements devices" where '
            'QP2506-Q1 (June 2025) prints "contribute in improving" and "improvement '
            'devices". Neither touches the demand. Marks delta NIL - both print '
            '4 + 4 + 4 + 4 = 16 over the same four named devices. No answer has been '
            'authored on this question yet; this field records the equivalence only.'),
        evidence=[
            'REVERSE-HINT ADJUDICATION, this session. Surfaced by REVERSE_HINT_CANDIDATES.md '
            'and ruled on by reading both printed stems. A host hint points only backwards, '
            'so this link was invisible from this question.',
            'WHY THE FAMILY MODEL COULD NOT SEE IT: a family edge forms on reused_from or on '
            'EXACT equality of the normalised stem, and these two differ by two words. The '
            'question therefore derived as tier C with no donor while a verified answer to '
            'the same task already existed on QP2506-Q1.',
            'CONSEQUENCE: derived readiness moves C -> D. This is the first donor the '
            'reverse-hint queue has created.',
        ]),
    'Q6': dict(
        donor='QP2602-Q6',
        delta=(
            'ADJUDICATED SAME EXAMINER TASK. Normalised stems differ by one inserted word: '
            'QP2602-Q6 (February 2026) prints "give PROPER justification" where this sitting '
            'prints "give justification". Marks delta NIL at 8 + 8. No answer has been '
            'authored on this question yet; this field records the equivalence only.'),
        evidence=[
            'REVERSE-HINT ADJUDICATION, this session, by reading both printed stems.',
            'READINESS UNCHANGED: this question was already tier D through QP2506-Q6 and '
            'QP2508-Q6, whose stems are exactly equal to this one. The edge adds a third '
            'donor, not a new capability.',
            'THE REAL EFFECT IS ON THE COUNTERPART. One inserted word kept QP2602-Q6 outside '
            'the general-average family, so an already-built page rendered "Once in this set" '
            'for a question this corpus holds at five sittings. The edge corrects that.',
        ]),
    'Q5': dict(
        donor='QP2409-Q8',
        delta=(
            'ADJUDICATED SAME EXAMINER TASK. Normalised stems differ by one scanning '
            'artifact: the source copy of THIS paper prints the roman numeral "(iii)" as '
            '"(Ill)", which survives normalisation as the word "ill". QP2409-Q8 (September '
            '2024) prints "(iii)". Marks delta NIL at 8 + 8. No answer has been authored on '
            'this question yet; this field records the equivalence only.'),
        evidence=[
            'REVERSE-HINT ADJUDICATION, this session, by reading both printed stems.',
            'NO DONOR VALUE YET: QP2409-Q8 is unbuilt, so this question stays tier C and '
            'still requires full fresh research. The edge is recorded now because the '
            'equivalence is a fact about the two papers, and because whichever of the two is '
            'solved first becomes the donor for the other.',
            'AN OCR ARTIFACT IS ENOUGH TO HIDE A RECURRENCE. Recorded as evidence for the '
            'reverse-hint mechanism: exact-stem equality cannot see through a scanning error, '
            'and nothing else in the pipeline was looking.',
        ]),
}

for qno, e in EDGES.items():
    Q = q(spec, 'QP2404-' + qno)
    assert Q['reused_from'] is None, 'unexpected existing edge on %s' % qno
    assert not Q.get('model_answer'), 'this script must not touch answered questions'
    Q['reused_from'] = e['donor']
    Q['question_delta'] = e['delta']
    Q['reuse_evidence'] = e['evidence'] + (Q.get('reuse_evidence') or [])

save(spec)
print('landed edges:', {k: v['donor'] for k, v in EDGES.items()})
