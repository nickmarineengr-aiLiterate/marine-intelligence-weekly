#!/usr/bin/env python3
"""M01..M23 -- the mutation harness for the OPEN-G1-014 definition gate.

    python tools/current_answers/test_open_g1_014_mutations.py

A gate that has never rejected anything is not evidence of anything. Each
mutation below reintroduces ONE of the defects OPEN-G1-014 recorded, or removes
ONE of the propositions the correction added, and the harness proves four
things per mutation:

    no-op    the mutation actually changed target bytes (digest moved)
    reject   the INTENDED guard failed
    escape   the intended guard did not silently pass
    crash    the gate ran to completion rather than raising

The third column is the one that matters most, and it is the reason the harness
credits a mutation ONLY when the guard it was aimed at fails. A mutation that
happens to trip some other guard proves nothing about the guard under test --
that is a digest failure wearing a semantic guard's name, and it is exactly how
a suite ends up green while the rule it advertises is dead. Collateral failures
are printed, never credited.

The harness runs entirely in memory over a copied bundle. It never writes to
the spec, the rendered page or the registry.
"""
import copy
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import validate_open_g1_014 as G  # noqa: E402


# --------------------------------------------------------------------------
# Mutation primitives.
# --------------------------------------------------------------------------

def _spec_sub(b, pattern, repl=''):
    """Rewrite the spec by round-tripping its JSON text.

    Editing the serialised form rather than walking the tree means a phrase is
    removed everywhere it occurs -- recall, answer blocks, comparison table,
    study guide, keywords -- which is the point: a guard must not be
    satisfiable by one surviving copy in a corner of the spec.
    """
    b['spec'] = json.loads(re.sub(pattern, repl, json.dumps(b['spec']), flags=re.I))


def _page_sub(b, pattern, repl=''):
    b['page'] = re.sub(pattern, repl, b['page'], flags=re.I)


def _both_sub(b, pattern, repl=''):
    _spec_sub(b, pattern, repl)
    _page_sub(b, pattern, repl)


def _inject_answer(b, text):
    b['spec']['answer']['blocks'].append({'p': text})


def _inject_study(b, text):
    b['spec']['study_guide']['blocks'].append({'p': text})


def _set_registry_version(b, value):
    """Walk the registry and stale the CA-EM-0003 row's version."""
    def walk(node):
        if isinstance(node, dict):
            if node.get('current_answer_id') == G.CA_ID:
                node['answer_version'] = value
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(b['registry'])


# --------------------------------------------------------------------------
# The twelve mutations, each naming the single guard it is aimed at.
# --------------------------------------------------------------------------
MUTATIONS = [
    ('M01', 'the withdrawn claim that a protocol is subordinate to a parent '
            'convention is put back into the answer',
     'G01-NO-TITLE-SUBORDINATION',
     lambda b: _inject_answer(b, 'A protocol is itself a treaty, subordinate '
                                 'to a parent convention.')),

    ('M02', 'the fourth rung is rebuilt under the codes, restoring the ladder '
            'Treaty > Convention > Protocol > Code',
     'G02-NO-FOUR-LEVEL-LADDER',
     lambda b: _inject_answer(b, 'Below all three sit the codes.')),

    ('M03', 'the study guide again tells the candidate to open on the hierarchy',
     'G03-NO-HIERARCHY-OPENING',
     lambda b: _inject_study(b, 'Open with the hierarchy in one sentence.')),

    ('M04', 'the positive claim that a protocol is itself a treaty is deleted',
     'G04-PROTOCOL-IS-ITSELF-A-TREATY',
     lambda b: _both_sub(b, r'is\s+itself\s+a\s+treaty', 'is an instrument')),

    ('M05', "VCLT Art.2(1)(a)'s operative words are deleted, which is what "
            'made rank-by-title arguable in version 1.0',
     'G05-DESIGNATION-PHRASE',
     lambda b: _both_sub(b, r'whatever its particular designation',
                         'in written form')),

    ('M06', 'a blanket protocol-ratification rule is asserted as fact',
     'G06-NO-UNIVERSAL-RATIFICATION',
     lambda b: _inject_answer(b, 'A protocol must always be ratified before '
                                 'it can bind a State.')),

    ('M07', 'the Article 2(1)(b) attribution is stripped, collapsing the '
            'definition of the named acts into the means of consent',
     'G07-ART-2-1-B-DEFINES-ACTS',
     lambda b: _both_sub(b, r'2\(1\)\(b\)', 'the Convention')),

    ('M08', 'the Article 11 attribution is stripped, leaving consent to be '
            'bound with no stated source of its means',
     'G08-ART-11-MEANS-OF-CONSENT',
     lambda b: _both_sub(b, r'article\s+11', 'the Convention')),

    ('M09', 'the MARPOL Protocol 1978 Art.IV(1) worked example is deleted, '
            'unanchoring the instrument-specific consent point',
     'G09-MARPOL-PROT-IV-1-EXAMPLE',
     lambda b: _both_sub(b, r'article\s+iv\(1\)', 'its final clauses')),

    ('M10', 'the Article 3 scope qualification is deleted, so Art.2(1)(a) '
            'reads as exhaustive',
     'G10-ART-3-SCOPE-QUALIFICATION',
     lambda b: _both_sub(b, r'article\s+3\b', 'the Convention')),

    ('M11', 'the MIW voice is promoted: its secondary labelling is removed and '
            'the explanation stands as the definition',
     'G11-MIW-LABELLED-SECONDARY',
     lambda b: _spec_sub(b, r'MIW EXPLANATION|MIW GUIDANCE', 'The rule')),

    ('M12', 'the registry row is left on the superseded version while the '
            'spec has moved, i.e. a stale projection',
     'G12-REGISTRY-ROUTE-INTEGRITY',
     lambda b: _set_registry_version(b, '1.0')),

    # ---- version 2.2: the four withdrawn authority-discipline claims -------
    # Each is injected into the ANSWER BLOCKS, i.e. the candidate-facing body,
    # because that is the most obvious surface the guard defends. M19..M23
    # below then inject the SAME defects through the rendered version-history
    # projection, which is the surface an earlier form of this gate excluded.
    ('M13', 'the unsourced IMO example list is put back into the Convention '
            'block, re-asserting instruments never read at source',
     'G13-NO-UNSOURCED-IMO-EXAMPLE-LIST',
     lambda b: _inject_answer(b, 'The familiar instruments so titled include '
                                 'SOLAS 1974, STCW 1978, Load Lines 1966 and '
                                 'COLREG 1972.')),

    ('M14', 'entry into force and amendment are again asserted as things a '
            'convention has by being one, rather than as its own terms',
     'G14-NO-GENERAL-CONVENTION-OPERATION-CLAIM',
     lambda b: _inject_answer(b, 'Each convention carries its own '
                                 'entry-into-force conditions and its own '
                                 'amendment provisions.')),

    ('M15', 'the generic protocol-relation taxonomy is restored above the '
            'single sourced MARPOL example',
     'G15-NO-GENERIC-PROTOCOL-RELATION-TAXONOMY',
     lambda b: _inject_answer(b, 'A protocol is normally related to another '
                                 'instrument or regime.')),

    ('M16', 'the general party-status claim is restored',
     'G16-NO-GENERIC-PARTY-STATUS-CLAIM',
     lambda b: _inject_answer(b, 'A State may be party to a convention '
                                 'without being party to a protocol relating '
                                 'to it.')),

    # ---- the review-claim invariant ---------------------------------------
    # Retargeted once version 2.7 earned a real external PASS. The prior
    # fixture mutated the scope note alone, which stopped building a dishonest
    # state the moment the current version genuinely had a review of its own --
    # G17 was right not to fire. The mutation now also withdraws that PASS, so
    # the entry again claims a current-version review it does not have. The
    # withdrawn value still discloses the shortfall, so G18 stays satisfied and
    # the failure isolates to G17.
    ('M17', 'an older review is re-presented as covering the CURRENT answer '
            'version while that version carries no independent PASS of its '
            'own, i.e. a review claimed but not held',
     'G17-REVIEW-CLAIM-HONESTY',
     lambda b: (
         b['spec']['review_record'].__setitem__(
             'scope_of_this_review',
             'THIS REVIEW COVERS VERSION %s and the verdict PASS recorded in '
             'this record belongs to the text now rendered.'
             % b['spec']['answer_version']),
         _set_current_independent_review(
             b, 'OUTSTANDING - NOT YET OBTAINED FOR THIS VERSION.'))),

    ('M18', 'the current version stops disclosing that its independent review '
            'is outstanding, leaving non-eligibility to be inferred',
     'G18-NON-ELIGIBILITY-DISCLOSED',
     lambda b: _set_current_independent_review(
         b, 'The correction has been applied in full and the entry is '
            'complete.')),

    # ---- leakage through the RENDERED VERSION-HISTORY projection ------------
    # build_current_answers.py projects version, date, reason and authority of
    # every history row into the candidate-facing "Version and review record".
    # A defect delivered through that field reaches a candidate's eyes exactly
    # as an answer-block defect does. These five prove the guards read it. The
    # internal-only fields (independent_review, authority_hold, version_rule,
    # ...) are NOT injected here, because that is where this provenance is
    # supposed to live and a guard that rejected it there would be wrong.
    ('M19', 'internal fix labels and finding ids are written into the rendered '
            'version-history reason, leaking workflow vocabulary to candidates',
     'G19-NO-INTERNAL-VOCAB-IN-RENDERED-SURFACE',
     lambda b: _append_current_reason(
         b, ' FIX-A and FIX-B were applied under OPEN-G1-014, registered by '
            'CORR-DEFN-TREATY-20260825, verdict PASS_WITH_FIX against '
            'Sources A-F.')),

    ('M20', 'the unsourced IMO example list is re-stated inside the rendered '
            'version-history reason instead of the answer body',
     'G13-NO-UNSOURCED-IMO-EXAMPLE-LIST',
     lambda b: _append_current_reason(
         b, ' The familiar instruments so titled include SOLAS 1974, STCW '
            '1978, Load Lines 1966 and COLREG 1972.')),

    ('M21', 'the withdrawn general convention-operation claim is re-asserted '
            'through the rendered version-history reason',
     'G14-NO-GENERAL-CONVENTION-OPERATION-CLAIM',
     lambda b: _append_current_reason(
         b, ' Each convention carries its own entry-into-force conditions and '
            'its own amendment provisions.')),

    ('M22', 'the withdrawn generic protocol-relation taxonomy is re-asserted '
            'through the rendered version-history reason',
     'G15-NO-GENERIC-PROTOCOL-RELATION-TAXONOMY',
     lambda b: _append_current_reason(
         b, ' A protocol is normally related to another instrument or '
            'regime.')),

    ('M23', 'the withdrawn general party-status claim is re-asserted through '
            'the rendered version-history authority field',
     'G16-NO-GENERIC-PARTY-STATUS-CLAIM',
     lambda b: _append_current_authority(
         b, ' A State may be party to a convention without being party to a '
            'protocol relating to it.')),

    # ---- version 2.3: the five withdrawn authority-boundary formulations ----
    # Each mutation reinstates ONE of the exact sentences the third independent
    # review required to be withdrawn, on the candidate-facing surface that
    # sentence actually occupied, and names the single guard aimed at it. The
    # two 'final clauses' mutations (M25, M26) are deliberately distinguished
    # by the sentence they sit in rather than by the phrase they share: if both
    # tripped the same guard, FINAL FIX 2 and FINAL FIX 3 would be one guard
    # wearing two names, and one of the two regressions could return unseen.
    ('M24', 'the unsourced designation example list is put back, enumerating '
            'titles that Source A never enumerates',
     'G20-NO-DESIGNATION-EXAMPLE-LIST',
     lambda b: _inject_answer(b, 'An instrument titled convention, protocol, '
                                 'agreement, charter or covenant is a treaty '
                                 'if it meets those criteria.')),

    ('M25', "the Article 11 means-of-consent sentence again makes availability "
            "a matter of the instrument's own final clauses",
     'G21-ART-11-CONSENT-DEPENDS-ON-WHAT-IS-AGREED',
     lambda b: _inject_answer(b, 'Which of the Article 11 means is actually '
                                 'available for any given instrument is '
                                 "decided by that instrument's own final "
                                 'clauses.')),

    ('M26', 'the protocol paragraph again generalises how a State becomes '
            "party to the protocol's own final clauses",
     'G22-PROTOCOL-CONSENT-NOT-GENERALISED',
     lambda b: _inject_answer(b, 'How a State becomes party to a protocol is '
                                 "decided by that instrument's own final "
                                 'clauses and not by its title.')),

    ('M27', 'the general functional taxonomy is restored above the '
            'no-hierarchy statement the sources actually establish',
     'G23-NO-FUNCTIONAL-TAXONOMY',
     lambda b: _inject_answer(b, 'The distinction between the three is one of '
                                 'function, not of rank.')),

    ('M28', 'the withdrawn OWN FINAL CLAUSES sentence is put back into the '
            '15-second recall, leaving the rest of the recall untouched',
     'G24-RECALL-CONSENT-SENTENCE-CORRECTED',
     # Re-pointed at 2.5: the 2.3 sentence this used to overwrite was itself
     # withdrawn at 2.5, so the replacement now targets the narrower Article 11
     # inference that took its place. Same defect, same guard, live target.
     lambda b: _set_recall(
         b, b['spec']['quick_revision']['recall_15s'].replace(
             'so ratification is not the only means it lists.',
             "How a State becomes bound is decided by the instrument's OWN "
             'FINAL CLAUSES, not by what the instrument is called.'))),

    # ---- version 2.4: the five withdrawn source-boundary formulations -------
    # Four corrections, five propositions: FINAL FIX D withdrew two distinct
    # claims from the MARPOL paragraph, so it gets two guards and two
    # mutations. Each mutation reinstates ONE withdrawn sentence in its own
    # words on a CANDIDATE-FACING surface, and the surfaces are varied
    # deliberately -- answer block, comparison table, rendered version-history
    # reason, critical numbers -- so that no guard can be satisfied by watching
    # the answer body alone. None of them touches the internal-only history
    # fields or the corrections/ record, because that is where the withdrawn
    # wording is SUPPOSED to live: a guard that rejected it there would be
    # pushing provenance out of its one legitimate home.
    ('M29', 'the unsourced adoption limb is put back on the consent sentence, '
            're-asserting what adoption of the treaty text does not establish',
     'G25-NO-UNSOURCED-ADOPTION-CONSENT-CLAIM',
     lambda b: _inject_answer(b, 'Adoption of the treaty text does not by '
                                 "itself establish a State's consent to be "
                                 'bound.')),

    ('M30', 'the broad legal-effect-and-operation claim is restored to the '
            'comparison table, where it sat as the Convention "What it does" '
            'cell rather than in the answer body',
     'G26-NO-CONVENTION-LEGAL-EFFECT-CLAIM',
     lambda b: _set_table_cell(
         b, 'convention',
         'Its legal effect and operation do not follow merely from the '
         'title')),

    ('M31', 'the withdrawn absolute about what being called a protocol tells '
            "you about the instrument's legal force is put back",
     'G27-PROTOCOL-TITLE-CLAIM-NOT-ABSOLUTE',
     lambda b: _inject_answer(b, 'Being called a protocol tells you nothing '
                                 "about the instrument's legal force.")),

    ('M32', 'the withdrawn absorption characterisation is re-asserted through '
            'the rendered version-history reason rather than the answer body',
     'G28-NO-MARPOL-ABSORPTION-CLAIM',
     lambda b: _append_current_reason(
         b, ' The 1978 Protocol absorbed the parent Convention.')),

    ('M33', 'the withdrawn naming-practice proposition is re-asserted through '
            'the critical numbers, a candidate-facing surface outside the '
            'answer blocks entirely',
     'G29-NO-MARPOL-NAMING-PRACTICE-CLAIM',
     lambda b: _inject_critical_number(
         b, 'The combined regime is commonly referred to here as MARPOL 73/78 '
            'rather than as MARPOL 1973')),

    # ---- version 2.5: the seven withdrawn source-boundary formulations ------
    # Five contractions, seven propositions: EXTERNAL FIX 2 withdrew two
    # distinct formulations and EXTERNAL FIX 3 withdrew two distinct table
    # cells, so each of those gets two guards and two mutations. The surfaces
    # are varied deliberately -- answer block, comparison table, answer heading,
    # rendered version-history reason -- so that no guard can be satisfied by
    # watching the answer body alone. None touches the internal-only history
    # fields or the corrections/ record, because that is where the withdrawn
    # wording is SUPPOSED to live.
    ('M34', 'the withdrawn general-term / binding-agreement opening is put '
            'back in front of the Article 2(1)(a) definition',
     'G30-NO-GENERAL-TERM-TREATY-INTRO',
     lambda b: _inject_answer(b, 'A treaty is the general term in '
                                 'international law for a binding agreement '
                                 'between States.')),

    ('M35', 'the withdrawn general binding rule is restored, re-asserting a '
            'proposition no Article in the frozen set carries',
     'G31-NO-GENERAL-BINDS-ONLY-CONSENT-CLAIM',
     lambda b: _inject_answer(b, 'A treaty binds only those States that have '
                                 'expressed consent to be bound by it.')),

    ('M36', 'the withdrawn means-available-depends theory is restored above '
            "Article 11's own listing of the means",
     'G32-NO-MEANS-AVAILABLE-DEPENDS-CLAIM',
     lambda b: _inject_answer(b, 'Which of the Article 11 means of expressing '
                                 'consent is available for a particular '
                                 'instrument depends on what is agreed for '
                                 'that instrument.')),

    ('M37', 'the withdrawn Treaty cell is put back into the comparison table, '
            'a surface outside the answer prose entirely',
     'G33-NO-CLASS-NOT-AN-INSTRUMENT-CELL',
     lambda b: _set_table_cell(
         b, 'treaty', 'Nothing on its own - it is the class, not an '
                      'instrument')),

    ('M38', 'the withdrawn generic whatever-the-terms claim is put back into '
            'the Protocol row of the comparison table',
     'G34-NO-GENERIC-WHATEVER-THE-TERMS-CLAIM',
     lambda b: _set_table_cell(
         b, 'protocol', 'Whatever the terms of that particular instrument '
                        'provide.')),

    # RETARGETED. The earlier form of this mutation asserted the superseded
    # contract: it restored the BARE absolute and was rejected by a guard that
    # simultaneously REQUIRED the residue phrase on the page. Under the
    # corrected contract the residue phrase is banned from the candidate-facing
    # Protocol heading outright, so the mutation that matters is the one the
    # old guard would have WAVED THROUGH -- the residue with the Article
    # 2(1)(a) qualifier still trailing it, which is precisely the heading the
    # old guard locked in.
    ('M39', 'the withdrawn absolute (a treaty in its own right) is '
            'reintroduced into the candidate-facing Protocol heading with the '
            'Article 2(1)(a) qualifier still trailing it -- the exact residue '
            'the superseded guard required rather than rejected',
     'G35-PROTOCOL-HEADING-CONDITIONAL',
     lambda b: _set_protocol_heading(b, 'Protocol - a treaty in its own '
                                        'right where it meets Article '
                                        '2(1)(a)')),

    ('M39B', 'the Article 2(1)(a) qualification is dropped from the '
             'candidate-facing Protocol heading, leaving the status asserted '
             'unconditionally where Source A makes it conditional',
     'G35-PROTOCOL-HEADING-CONDITIONAL',
     lambda b: _set_protocol_heading(b, 'Protocol - a treaty')),

    # ADDED with the restoration of the stronger G35 contract. M39 and M39B
    # both corrupt the RENDERED projection, so between them they prove only
    # that G35 reads the page. G35 now reads the candidate-facing CANONICAL
    # authoring surface as well, and a guard limb that no mutation exercises is
    # a guard limb nobody has evidence for. This mutation corrupts the SPEC
    # heading and leaves the projection untouched, so the ONLY way the target
    # can fail is by G35 having actually read the authoring surface. Under the
    # superseded page-only contract this mutation would have scored an ESCAPE.
    ('M39C', 'the withdrawn absolute (a treaty in its own right) is '
             'reintroduced into the candidate-facing SPEC Protocol heading, '
             'with the Article 2(1)(a) qualifier still trailing it and the '
             'rendered projection left clean -- so only a guard that reads the '
             'canonical authoring surface can catch it',
     'G35-PROTOCOL-HEADING-CONDITIONAL',
     lambda b: _set_spec_protocol_heading(
         b, 'Protocol - a treaty in its own right where it meets Article '
            '2(1)(a)')),

    ('M40', 'the withdrawn evaluative clause on the MARPOL history is '
            're-asserted through the rendered version-history reason',
     'G36-NO-HISTORY-IS-UNUSUAL-CLAIM',
     lambda b: _append_current_reason(b, ' This history is unusual.')),

    # ---- version 2.6: the four withdrawn rank formulations ------------------
    # ONE mutation, because the four contractions are one defect in four
    # sentences and are guarded by one detector. It is delivered through the
    # COMPARISON TABLE rather than the answer prose, so the guard cannot be
    # satisfied by watching the paragraphs alone, and it reintroduces the
    # withdrawn rank language into a block EXT-02 actually contracted. It does
    # not touch the internal-only history fields or the corrections/ record,
    # which is where that wording is SUPPOSED to live.
    ('M41', 'the withdrawn rank language is put back into the Convention row '
            'of the comparison table, re-asserting a law of legal rank that '
            'the frozen source set does not establish',
     'G37-NO-WITHDRAWN-RANK-FORMULATION',
     lambda b: _set_table_cell(
         b, 'convention', 'A designation. The title Convention confers no '
                          'legal rank and does not itself create a legal '
                          'rank')),

    # ---- version 2.7: the three withdrawn hierarchy formulations ------------
    # ONE mutation, matching the ONE guard: the three contractions are one
    # defect in three sentences. It is delivered through the COMPARISON TABLE
    # rather than the answer prose, so the guard cannot be satisfied by
    # watching the paragraphs alone, and it reintroduces the EXT-2.6-02 clause
    # verbatim into a row the contraction did not touch -- proving the guard
    # sweeps the whole candidate-facing teaching surface rather than the three
    # corrected blocks. It does not touch the internal-only history fields or
    # the corrections/ record, which is where that wording is SUPPOSED to live.
    ('M42', 'the withdrawn hierarchy clause is put back into the Protocol row '
            'of the comparison table, re-asserting a proposition about legal '
            'hierarchy that the frozen source set does not establish in '
            'either direction',
     'G38-NO-WITHDRAWN-HIERARCHY-FORMULATION',
     lambda b: _set_table_cell(
         b, 'protocol', 'An instrument titled Protocol is related to the '
                        'convention it relates to, but that relationship does '
                        'not create a legal hierarchy merely from the '
                        'titles')),
]


def _set_table_cell(b, term, value):
    """Rewrite the LAST cell of the named row of the comparison table.

    Indexed from the end rather than at a fixed column, because EXTERNAL FIX 3
    replaced the four-column table with a two-column one and a hardcoded row[2]
    would raise on the new shape -- a crash, not a rejection, and the harness
    would have credited neither.
    """
    for blk in b['spec']['answer']['blocks']:
        tbl = blk.get('table')
        if not tbl:
            continue
        for row in tbl.get('rows') or []:
            if row and str(row[0]).strip().lower() == term:
                row[-1] = value


def _set_protocol_heading(b, value):
    """Rewrite the Protocol heading ELEMENT of the rendered projection.

    This is the PAGE half of G35's input boundary, used by M39 and M39B. The
    SPEC half is exercised separately by M39C through
    _set_spec_protocol_heading below. Two surfaces, two mutations: corrupting
    only one of them must still fail the guard, and that is what the pair
    proves.
    """
    def repl(m):
        if re.match(r'\s*Protocol\s*[-–—]', G._strip_tags(m.group(2)).strip(),
                    re.I):
            return m.group(1) + value + m.group(3)
        return m.group(0)

    b['page'] = re.sub(r'(<h[1-6][^>]*>)(.*?)(</h[1-6]>)', repl, b['page'],
                       flags=re.I | re.S)


def _set_spec_protocol_heading(b, value):
    """Rewrite the Protocol heading BLOCK of the canonical authoring surface.

    Touches the spec ONLY. b['page'] is deliberately left alone, so a guard
    that reads the rendered projection alone cannot see this mutation at all
    and would score an ESCAPE against it. That asymmetry is the evidence: it is
    what makes M39C a non-vacuous proof that G35 reads the spec surface.
    """
    for section in ('answer', 'study_guide'):
        for blk in (b['spec'].get(section) or {}).get('blocks') or []:
            if blk.get('h') and re.match(r'\s*Protocol\s*[-–—]',
                                         str(blk['h']), re.I):
                blk['h'] = value


def _inject_critical_number(b, text):
    """Append to quick_revision.critical_numbers, a candidate-facing surface
    that is neither an answer block nor the rendered history."""
    b['spec']['quick_revision'].setdefault('critical_numbers', []).append(text)


def _set_recall(b, value):
    """Rewrite the 15-second recall only. Used by M28 to prove G24 reads the
    recall itself rather than being satisfied by the answer body."""
    b['spec']['quick_revision']['recall_15s'] = value


def _append_current_reason(b, text):
    """Append to the CURRENT version's rendered `reason` field."""
    _append_current_history_field(b, 'reason', text)


def _append_current_authority(b, text):
    """Append to the CURRENT version's rendered `authority` field."""
    _append_current_history_field(b, 'authority', text)


def _append_current_history_field(b, field, text):
    cur = str(b['spec'].get('answer_version'))
    for row in b['spec'].get('version_history') or []:
        if str(row.get('version')) == cur:
            row[field] = str(row.get(field) or '') + text


def _set_current_independent_review(b, value):
    """Rewrite the CURRENT version's history row only."""
    cur = str(b['spec'].get('answer_version'))
    for row in b['spec'].get('version_history') or []:
        if str(row.get('version')) == cur:
            row['independent_review'] = value


def _digest(bundle):
    blob = json.dumps(
        {'spec': bundle['spec'], 'registry': bundle['registry']},
        sort_keys=True, ensure_ascii=False) + bundle['page'] + \
        ''.join(bundle['routes'][k] for k in sorted(bundle['routes']))
    return hashlib.sha256(blob.encode('utf-8')).hexdigest()


def main():
    base = G.load_bundle()
    baseline = G.run(base)
    failing = [r for r, ok, _ in baseline if not ok]
    if failing:
        print('ABORT: the gate does not pass before any mutation: %s' % failing)
        return 1
    known = {r for r, _, _ in baseline}

    print('OPEN-G1-014 MUTATION HARNESS -- %d mutation(s) over %d guard(s)\n'
          % (len(MUTATIONS), len(known)))

    escapes = noops = crashes = miscredit = 0
    for mid, desc, target, apply_ in MUTATIONS:
        if target not in known:
            print('  %s  ERROR   names an unknown guard %s' % (mid, target))
            miscredit += 1
            continue
        b = copy.deepcopy(base)
        before = _digest(b)
        try:
            apply_(b)
        except Exception as exc:  # noqa: BLE001
            print('  %s  CRASH   while mutating: %r' % (mid, exc))
            crashes += 1
            continue
        after = _digest(b)
        if before == after:
            print('  %s  NO-OP   mutation changed no target bytes' % mid)
            noops += 1
            continue
        try:
            res = G.run(b)
        except Exception as exc:  # noqa: BLE001
            print('  %s  CRASH   gate raised on mutated bundle: %r' % (mid, exc))
            crashes += 1
            continue
        broke = [r for r, ok, _ in res if not ok]
        if target not in broke:
            print('  %s  ESCAPE  %s did NOT reject: %s' % (mid, target, desc))
            if broke:
                print('          (only these failed, none of them the target: %s)'
                      % broke)
            escapes += 1
            continue
        collateral = [r for r in broke if r != target]
        note = ''
        if collateral:
            note = '  [collateral, not credited: %s]' % ', '.join(collateral)
        print('  %s  OK      %s rejected%s' % (mid, target, note))
        print('          %s' % desc)

    total = len(MUTATIONS)
    passed = total - escapes - noops - crashes - miscredit
    print('\n%d/%d mutation(s) rejected by the guard they were aimed at.'
          % (passed, total))
    print('escapes=%d no-ops=%d crashes=%d misnamed=%d'
          % (escapes, noops, crashes, miscredit))
    if passed == total:
        print('every OPEN-G1-014 guard is non-vacuous: each one rejected the '
              'specific defect it exists to catch.')
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
