#!/usr/bin/env python3
"""QP2404 Q3, Q6, Q7 - the three donor-backed questions whose stems are IDENTICAL.

All three donors are LATER sittings pulled BACKWARDS to April 2024.
Also closes Q4's verification_status.
"""
import copy, json, sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qpio import load, q, save

CLONE = ('decomposition', 'model_answer', 'study_notes', 'sources', 'unresolved',
         'regulations', 'search_aliases', 'understand_first', 'memory_cue',
         'decomposition_gate', 'provenance_summary', 'reverify_before_publication',
         'quick_revision', 'answer_route', 'retrieval_cards')

tgt = load('QP2404')


def adapt(qno, donor_paper, donor_qid):
    D = q(load(donor_paper), donor_qid)
    Q = q(tgt, 'QP2404-' + qno)
    for k in CLONE:
        if k in D:
            Q[k] = copy.deepcopy(D[k])
    for i, c in enumerate(Q['retrieval_cards']):
        c['id'] = 'QP2404-%s-C%d' % (qno, i + 1)
    Q['answer_status'] = 'Pilot Review Ready'
    Q['verification_file'] = 'verification/QP2404/%s.md' % qno
    Q['reuse_tier'] = 'D'
    Q['reused_from'] = donor_qid
    Q['recurrence_class'] = 'exact_recurrence'
    return Q


def repl(obj, old, new):
    """Replace inside every string, and prove the target existed."""
    hits = [0]

    def walk(o):
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v) for v in o]
        if isinstance(o, str) and old in o:
            hits[0] += 1
            return o.replace(old, new)
        return o
    out = walk(obj)
    if not hits[0]:
        raise SystemExit('PATCH MISS: %r' % old[:70])
    return out


# ===================================================================== Q3
Q3 = adapt('Q3', 'QP2509', 'QP2509-Q4')
Q3['question_delta'] = (
    'Printed stem IDENTICAL to QP2509-Q4 (September 2025), word for word including the '
    'single printed (16). Marks delta NIL. Temporal delta NIL: the 1993 Convention entered '
    'into force 5 September 2004 and the Admiralty Act, 2017 received assent 9 August 2017 - '
    'both long before April 2024, and neither was amended between this sitting and the '
    "donor's. All three deltas are genuinely nil and are recorded as nil rather than implied.")
Q3['reuse_evidence'] = [
    'VERIFIED ANSWER DONOR: QP2509-Q4 (September 2025). Adjudicated family edge already '
    'existed by exact stem equality; this was Tier D before this session and did not depend '
    'on the reverse-hint queue.',
    'DIRECTION: April 2024 is the EARLIER sitting. The donor is a later answer pulled '
    'backwards, so any currency statement written for September 2025 had to be reversed, '
    'not inherited.',
    'RE-ANCHORED: the sourcing paragraph and the whole temporal review. The donor had to '
    'reason about the Merchant Shipping Act 2025 boundary; at April 2024 that Act did not '
    'exist, so the reasoning is different even though the conclusion is the same.',
]
# the donor's sourcing paragraph names its own sitting
Q3['study_notes'] = repl(Q3['study_notes'],
                         'Nothing in this answer moved near September 2025',
                         'Nothing in this answer moved near April 2024')
Q3['temporal_review'] = {
    'state': 'TEMPORAL REVIEW COMPLETE',
    'risk': 'LOW',
    'sitting': 'April 2024',
    'classes': [],
    'notes': [
        'NOTHING IN THIS ANSWER MOVED NEAR THE SITTING. The International Convention on '
        'Maritime Liens and Mortgages was adopted at Geneva on 6 May 1993 and entered into '
        'force on 5 September 2004, nearly twenty years before this examination. The '
        'Admiralty (Jurisdiction and Settlement of Maritime Claims) Act, 2017 received '
        'assent on 9 August 2017, six and a half years before it.',
        'THE MERCHANT SHIPPING ACT BOUNDARY IS NOT ENGAGED, AND AT THIS SITTING IT DID NOT '
        'YET EXIST. The Indian statute governing maritime liens and admiralty jurisdiction '
        'is the Admiralty Act 2017, a separate enactment. The Merchant Shipping Act 2025 was '
        'not enacted until well after this paper and commenced 15 March 2026; it repealed '
        'the Merchant Shipping Act, 1958, not the Admiralty Act. Recorded because the donor '
        'answer was written at a sitting where that boundary had to be reasoned about, and '
        'the reasoning must not be inherited as though it applied here.',
        'CHECKED IN THE BACKWARD DIRECTION TOO. Nothing relied on in this answer was '
        'superseded between April 2024 and the donor sitting, so the donor text is safe to '
        'carry once the currency sentences are re-anchored.',
        'THE RISK ON THIS QUESTION IS JURISDICTIONAL, NOT TEMPORAL. The live hazard is '
        "asserting India's status as a party to the 1993 Convention, which was not "
        'established. Handled by answering at convention level and giving the Indian statute '
        'separately; recorded in unresolved.',
    ],
}

# ===================================================================== Q6
# STRUCTURAL DONOR is QP2506-Q6, but reused_from MUST REMAIN QP2602-Q6.
# QP2506-Q6 and QP2508-Q6 join this family by EXACT stem equality on their own.
# QP2602-Q6 does NOT - it differs by the inserted word "proper" - so the explicit
# edge is the only thing holding it in. Overwriting this field with the structural
# donor would drop QP2602-Q6 out of the family and regress that already-built page
# to "Once in this set". recurrence_model treats reused_from as an UNDIRECTED
# same-task edge, so recording the adjudicated pair here is the correct use.
Q6 = adapt('Q6', 'QP2506', 'QP2506-Q6')
Q6['reused_from'] = 'QP2602-Q6'
Q6['question_delta'] = (
    'Printed stem IDENTICAL to QP2506-Q6 (June 2025), word for word including the marks. '
    'Marks delta NIL. Temporal delta NIL: the York-Antwerp Rules 2016 were the current CMI '
    'text at April 2024 and Rule VII is materially unchanged from the 1994 and 2004 versions, '
    'so an older incorporated version would not alter the answer. All three deltas are nil. '
    'What changed is the SURROUNDINGS: the donor paper carried an LLMC question at Q5 and '
    'cross-referred to it. THIS PAPER HAS NO LLMC QUESTION, so the cross-reference is DROPPED '
    'rather than renumbered - on QP2404, Q5 is antifouling paint and Q1 is IoT.')
Q6['reuse_evidence'] = [
    'VERIFIED ANSWER DONOR: QP2506-Q6 (June 2025), printed stem raw-identical. QP2508-Q6 '
    '(August 2025) is a second identical donor and was consulted; the two are deliberately '
    'kept identical objects.',
    'THIRD DONOR ADDED BY REVERSE-HINT ADJUDICATION THIS SESSION: QP2602-Q6 (February 2026). '
    'Its stem differs from this one by a single inserted word ("give PROPER justification"), '
    'so no exact-equality family edge existed and it sat outside the family while being the '
    'same examiner task. It did not change this question\'s readiness - Q6 was already Tier D '
    '- but the adjudication corrects QP2602-Q6, which until now rendered "Once in this set".',
    'DIRECTION: April 2024 is the EARLIEST sitting in the family. Every donor is a later '
    'answer pulled backwards.',
    'PIL CAUGHT THIS BEFORE ADAPTATION: temporal_sweep.py flagged INTERNAL_QREF on both '
    'QP2506-Q6 and QP2508-Q6 ("See Q5 of this paper", "See Q1 of this paper"). Copying the '
    "donor's study notes unchanged would have pointed a candidate at the wrong question.",
]
# THE PIL FLAG, ACTIONED: drop the cross-reference, do not renumber it.
Q6['study_notes'] = repl(
    Q6['study_notes'],
    '<b>LLMC 1976 Article 3</b> - general average contribution is excepted from '
    'limitation. See Q5 of this paper.',
    '<b>LLMC 1976 Article 3</b> - general average contribution is excepted from '
    'limitation. (This paper sets no limitation question, so the point is given here '
    'in full rather than cross-referred.)')
Q6['study_notes'] = repl(
    Q6['study_notes'],
    'This is the most securely sourced question on the paper and the only one researched '
    'from scratch. Every proposition',
    'This is among the most securely sourced questions on the paper. Every proposition')
Q6['study_notes'] = repl(
    Q6['study_notes'],
    'the Rules were unchanged between this sitting and today',
    'the Rules were unchanged between this sitting and the build date')
Q6['cross_links'] = [
    {'label': 'QP2506 Q6 - the same question at the June 2025 sitting',
     'href': 'QP2506.html#q6'},
    {'label': 'QP2508 Q6 - the same question at the August 2025 sitting',
     'href': 'QP2508.html#q6'},
    {'label': 'QP2602 Q6 - the same question at the February 2026 sitting',
     'href': 'QP2602.html#q6'},
]
Q6['temporal_review'] = {
    'state': 'TEMPORAL REVIEW COMPLETE',
    'risk': 'LOW',
    'sitting': 'April 2024',
    'classes': [],
    'notes': [
        'THE YORK-ANTWERP RULES BIND BY CONTRACTUAL INCORPORATION, NOT AS LAW. The 2016 '
        'Rules were the current CMI text at this sitting. Rule VII is materially unchanged '
        'from the 1994 and 2004 versions, so an older incorporated version would not alter '
        'the answer to limb (b).',
        'CHECKED IN BOTH DIRECTIONS AND CLEAR. General average is among the most stable '
        'doctrines in maritime law. Nothing relied on entered force between April 2024 and '
        'the donor sittings, and nothing relied on was superseded before April 2024.',
        'DONOR CROSS-REFERENCE REMOVED, NOT RENUMBERED. Flagged prospectively by '
        'temporal_sweep.py as INTERNAL_QREF. The donors point at their own papers\' '
        'limitation question; this paper has none.',
    ],
}

# ===================================================================== Q7
Q7 = adapt('Q7', 'QP2508', 'QP2508-Q4')
Q7['question_delta'] = (
    'Printed stem IDENTICAL in demand to QP2508-Q4 (August 2025): both print limb A "How is '
    'Human Element issue addressed in STCW code (8)" and limb B "Discuss the IMO guidance on '
    'fatigue mitigation and management on board ships (8)". This sitting prints the limb '
    'labels as "A)." and "B)." against the donor\'s "A)" and "B)"; punctuation only. Marks '
    'delta NIL at 8 + 8 = 16. Temporal delta NIL on the operative regime - the Manila '
    'amendments have been in force since 1 January 2012 and MSC.1/Circ.1598 since 24 January '
    '2019, both long settled at this sitting. ONLY THE CURRENCY PARAGRAPH ON THE STCW '
    'COMPREHENSIVE REVIEW WAS RE-ANCHORED, and it is sharper here than in the donor: HTW 10 '
    'sat 5-9 February 2024, two months before this examination.')
Q7['reuse_evidence'] = [
    'VERIFIED ANSWER DONOR: QP2508-Q4 (August 2025). QP2601-Q9, QP2602-Q4, QP2604-Q9 and '
    'QP2506-Q8 are word-for-word identical objects in the same family and were consulted; '
    'the set is deliberately kept identical, so a correction to any one must be applied to all.',
    'DIRECTION: April 2024 is the EARLIEST sitting in this family. Every donor is a later '
    'answer pulled backwards.',
    'RE-ANCHORED: the currency note on the STCW comprehensive review. The donor writes it as '
    'at its own sitting and its relatives write it "as at August 2026" - an authoring-date '
    'statement that must not travel backwards. PIL flagged both prospectively.',
    'CARRIED FORWARD DELIBERATELY: the wrong-edition warning. MIW holds no licensed copy of '
    'the STCW Convention and Code, so the A-VIII/1 figures rest on a competent-authority '
    'restatement. The hazard is identical at this sitting.',
    'FIELD CHANGED: reused_from moves from the stored QP2601-Q9 to QP2508-Q4, the donor '
    'actually adapted. Both sit in the same family, so the recurrence model is unaffected.',
]
Q7['study_notes'] = repl(
    Q7['study_notes'],
    'A <b>comprehensive review</b> of the STCW Convention and Code has been under way '
    'through the HTW Sub-Committee with completion targeted around 2027, one of the '
    'acknowledged gaps being the treatment of hours of rest. <b>Nothing had been adopted '
    'at the date of this paper.</b>',
    'A <b>comprehensive review</b> of the STCW Convention and Code is under way through the '
    'HTW Sub-Committee: <b>HTW 10 met 5-9 February 2024, two months before this examination</b>, '
    'and agreed the roadmap, the methodology and the list of areas to be reviewed, with '
    'adoption targeted for <b>2027</b>. One of the acknowledged gaps is the treatment of hours '
    'of rest. <b>Nothing had been adopted at the date of this paper.</b>')
Q7['study_notes'] = repl(
    Q7['study_notes'],
    'This question is also substantively identical to three built 2026 objects, and the '
    'four are deliberately kept identical: a correction to any one of them must be applied '
    'to all.',
    'This question is substantively identical to several other built objects in its family, '
    'which are deliberately kept identical: a correction to any one of them must be applied '
    'to all.')
Q7['temporal_review'] = {
    'state': 'TEMPORAL REVIEW COMPLETE',
    'risk': 'LOW',
    'sitting': 'April 2024',
    'classes': [],
    'notes': [
        'THE OPERATIVE REGIME WAS SETTLED LONG BEFORE THIS SITTING. STCW 1978 as amended, '
        'with the Manila amendments in force from 1 January 2012; the rest-hour provisions '
        'of Regulation VIII/1 and Code section A-VIII/1; and MSC.1/Circ.1598 of 24 January '
        '2019 with its six modules. Every one of these was in force at April 2024.',
        'THE CURRENCY PARAGRAPH WAS RE-DERIVED FOR THIS SITTING, NOT INHERITED. HTW 10 sat '
        '5-9 February 2024 - two months before this examination - and agreed the roadmap, '
        'methodology and list of areas for the comprehensive review of the STCW Convention '
        'and Code, with adoption targeted for 2027. So at this sitting the review was under '
        'way and newly framed, and NOTHING had been adopted. Write the Manila regime as '
        'operative and the review as work in progress.',
        'DONOR STATEMENT REJECTED. Relatives of this question carry "nothing had been '
        'adopted as at August 2026". That is an authoring-date statement; it is true but it '
        'is not a statement about this sitting, and it is not carried. PIL flagged it '
        'prospectively as POST_SITTING_DATE.',
    ],
}

# ===================================================================== Q4 close-out
q(tgt, 'QP2404-Q4')['verification_status'] = (
    'Structure and mechanism carried from the verified QP2506-Q1 object, whose four device '
    'mechanisms were established against published naval-architecture and industry sources; '
    'the quoted efficiency ranges remain industry-quoted rather than verified, and no '
    'manufacturer datasheet or model-test report was read. The donor relationship itself was '
    'adjudicated this session by reading both printed stems. Regulatory framing re-derived '
    'for April 2024.')
for qid in ('Q3', 'Q6', 'Q7'):
    QQ = q(tgt, 'QP2404-' + qid)
    QQ['verification_status'] = {
        'Q3': 'Convention-level answer carried from the verified QP2509-Q4 object, sourced '
              'to the certified text of the 1993 Convention (articles 4, 5, 12) and the '
              'Gazette text of the Admiralty Act, 2017. Temporal review re-derived for April '
              "2024; India's party status to the 1993 Convention deliberately not asserted.",
        'Q6': 'Carried from the verified QP2506-Q6 object, every proposition sourced to the '
              'text of the York-Antwerp Rules 2016 (Rule of Interpretation, Rule Paramount, '
              'Rules A-E and Rule VII). Donor internal cross-reference removed after a '
              'prospective PIL INTERNAL_QREF flag. Temporal review re-derived for April 2024.',
        'Q7': 'Carried from the verified QP2508-Q4 object. Regulation VIII/1 quoted at '
              'primary level through MSC.1/Circ.1598, which reproduces it; A-VIII/1 figures '
              'rest on a competent-authority restatement and that limitation is stated. The '
              'STCW comprehensive-review currency paragraph was re-derived for April 2024 '
              'against the HTW 10 outcome of 5-9 February 2024.',
    }[qid]

# ---- guard: no cross-link may still point at a donor's own paper -------------
for qid in ('Q3', 'Q4', 'Q6', 'Q7'):
    for cl in q(tgt, 'QP2404-' + qid).get('cross_links') or []:
        assert not cl['href'].startswith('QP2404.html#') or cl['href'] == 'QP2404.html#q2', cl
        assert 'QP2506.html#q5' != cl['href'], 'stale donor self-reference: %s' % cl

save(tgt)
print('Q3, Q6, Q7 authored; Q4 closed out.')
