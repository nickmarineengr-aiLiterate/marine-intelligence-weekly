#!/usr/bin/env python3
"""OPEN-G1-014 definition-integrity gate for CA-EM-0003. Fails closed.

    python tools/current_answers/validate_open_g1_014.py

WHAT THIS GATE IS DEFENDING
---------------------------
CA-EM-0003 is the designated CURRENT FRAMEWORK answer on Treaty / Convention /
Protocol, and six candidate-facing year-page routes resolve to it. Version 1.0
taught a legal HIERARCHY that does not exist: it ranked a protocol below a
convention by reason of its title, extended the ladder to a fourth rung for the
codes, and collapsed consent to be bound into four named acts as though they
were the only routes. OPEN-G1-014 records the verified line inventory.

The generic library gate (validate_current_answers.py) is a STRUCTURAL gate: it
proves an entry is well-formed, owned, routed and reviewed. It cannot see a
false legal proposition. This gate is the SEMANTIC complement, and it is
deliberately narrow -- it asserts the specific propositions the correction
turned on, across the canonical spec AND every generated surface, so that a
regression cannot reach a candidate by way of either one.

Two design rules, both learned from the surrounding suite:

1.  Every content guard reads BOTH the canonical spec and the rendered page.
    A guard that reads only the spec cannot see a stale projection; a guard
    that reads only the page cannot see a spec that will re-render the error on
    the next build. The pair is the invariant, not either half.

2.  No guard is tied to a live corpus total. Counts move for reasons that have
    nothing to do with this finding, and a guard that moves with them is a
    guard that gets disabled the first time it is inconvenient.

The bundle is loaded once and the checks run over it, rather than each check
going to disk, so that the mutation harness
(test_open_g1_014_mutations.py) can corrupt the bundle and prove each guard
actually rejects what it claims to reject.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

CA_ID = 'CA-EM-0003'
SPEC = os.path.join(REPO, 'meoclass1', 'current-answers', 'specs', CA_ID + '.json')
PAGE = os.path.join(REPO, 'solvedQP', 'current', CA_ID + '.html')
REGISTRY = os.path.join(REPO, 'meoclass1', 'current-answers', 'registry.json')

#: The five candidate-facing LINK-OWNER files named in the OPEN-G1-014
#: inventory. These are the pages that CARRY a link to this entry; the sixth
#: logical route in that inventory is the DESTINATION page itself,
#: solvedQP/current/CA-EM-0003.html, which is held in PAGE above rather than
#: here. Five link owners plus one destination page is what makes the inventory
#: six logical routes, and the tuple below is deliberately five entries long.
#:
#: A raw href hit count is NOT the route count either: the two 2021 owners each
#: carry two links, so a textual sweep of these five files returns seven hits
#: for six logical routes.
ROUTE_OWNERS = (
    'meoclass1/pastpapers/questions-2021.html',
    'meoclass1/pastpapers/questions-2022.html',
    'solvedQP/questions-2021.html',
    'solvedQP/questions-2022.html',
    'solvedQP/current/CA-EM-0002.html',
)


def _read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def load_bundle():
    """Read every surface this finding owns, once."""
    routes = {}
    for rel in ROUTE_OWNERS:
        p = os.path.join(REPO, rel.replace('/', os.sep))
        routes[rel] = _read(p) if os.path.exists(p) else ''
    return {
        'spec': json.loads(_read(SPEC)),
        'page': _read(PAGE),
        'registry': json.loads(_read(REGISTRY)),
        'routes': routes,
    }


# --------------------------------------------------------------------------
# Text projections of the canonical spec.
# --------------------------------------------------------------------------

def _blocks_text(blocks):
    out = []
    for b in blocks or []:
        for key in ('h', 'p'):
            if b.get(key):
                out.append(str(b[key]))
        for item in b.get('ul') or []:
            out.append(str(item))
        tbl = b.get('table')
        if tbl:
            out.extend(str(x) for x in tbl.get('headers') or [])
            for row in tbl.get('rows') or []:
                out.extend(str(x) for x in row)
    return out


#: The fields of a version_history row that build_current_answers.py PROJECTS
#: into the rendered "Version and review record" section. These four reach a
#: candidate's eyes and are held to the same discipline as the answer body.
RENDERED_HISTORY_FIELDS = ('version', 'date', 'reason', 'authority')

#: The fields of a version_history row that are NEVER rendered. This is where
#: internal governance provenance legitimately lives -- the fix labels, the
#: authority hold, the versioning rationale, the outstanding-review disclosure.
#: The distinction is the point: provenance is not deleted, it is placed where
#: a candidate cannot read it. The full withdrawn-wording inventory is held in
#: the governance correction record under corrections/.
INTERNAL_ONLY_HISTORY_FIELDS = (
    'independent_review', 'authority_hold', 'version_rule', 'review_trigger',
    'supersedes', 'currentness_as_of',
)


def rendered_history_text(spec):
    """The version-history text a candidate actually reads, spec-side.

    This is the projection build_current_answers.py emits, reconstructed from
    the canonical source so that a leak can be caught in the spec BEFORE it is
    rendered as well as on the page after.
    """
    parts = []
    for row in spec.get('version_history') or []:
        for key in RENDERED_HISTORY_FIELDS:
            if row.get(key):
                parts.append(str(row[key]))
    return '\n'.join(parts)


def candidate_text(spec):
    """Everything in the spec that a candidate can end up reading.

    INCLUDES the rendered fields of version_history. An earlier form of this
    gate excluded version_history wholesale on the reasoning that it is
    provenance -- but four of its fields are PROJECTED onto the page, so a
    candidate who reads the version table has read whatever they contain,
    whatever the surrounding sentence says about it. Provenance that must name
    a withdrawn proposition in its own words belongs in the internal-only
    fields listed above, or in the governance correction record.
    """
    parts = [
        str(spec.get('present_day_examinable_core') or ''),
        str(spec.get('understand_first') or ''),
        rendered_history_text(spec),
    ]
    parts += _blocks_text((spec.get('answer') or {}).get('blocks'))
    parts += _blocks_text((spec.get('study_guide') or {}).get('blocks'))
    qr = spec.get('quick_revision') or {}
    parts.append(str(qr.get('recall_15s') or ''))
    parts.append(str(qr.get('critical_regulation') or ''))
    parts.append(str(qr.get('major_trap') or ''))
    parts.extend(str(k) for k in qr.get('keywords') or [])
    parts.extend(str(k) for k in qr.get('critical_numbers') or [])
    return '\n'.join(parts)


def _strip_tags(html):
    return re.sub(r'<[^>]+>', ' ', html)


#: The rendered page carries a "Version and review record" section, class
#: "layer ca-ver", that PROJECTS version_history. It is CANDIDATE-FACING: it
#: sits in the same document, under the same routes, with nothing gating it.
#: page_body() therefore returns the WHOLE page. It exists as a named function
#: because the earlier form of this gate truncated the page here, and the
#: truncation is the defect this guard set now forbids.
_VER_SECTION = 'layer ca-ver'


def page_body(html):
    """The candidate-facing part of the rendered page.

    That is all of it, including the version and review record. Anything that
    genuinely must not be read by a candidate does not belong on the page at
    all -- it belongs in an internal-only spec field or the correction record.
    """
    return _strip_tags(html)


#: Internal workflow vocabulary. None of this may reach a rendered surface:
#: fix labels, finding ids, correction-record ids, review-envelope shorthand.
#: A candidate reading "FIX-A removes the unsourced list (SOLAS 1974, ...)"
#: has read the unsourced list, whatever the verb in front of it was.
_INTERNAL_VOCAB = re.compile(
    r'\bFIX-(?:\d{2}|[A-Z])\b'
    r'|\bOPEN-G1-\d+\b'
    r'|\bCORR-[A-Z0-9-]+\b'
    r'|\bPASS_WITH_FIX\b'
    r'|\bSources?\s+A-F\b'
    r'|\bfrozen\s+(?:review\s+)?envelope\b'
    r'|\bsource\s+pack\b')


#: Sentence-ish split, scoping a claim to the clause that makes it. The
#: lookarounds keep a decimal intact: splitting naively on '.' cut
#: "removed at version 2.0, that a protocol always requires ratification"
#: into a fragment that had lost its own negating verb, and the guard then
#: read MIW's record of the withdrawn claim as MIW asserting it.
_SENT_SPLIT = re.compile(r'(?<!\d)[.;](?!\d)')

#: Words that mark a sentence as WARNING about a claim rather than making it.
_NEGATED = re.compile(
    r'\bno\b|\bnot\b|\bnever\b|trap|myth|wrong|incorrect|universal claim'
    r'|withdraw|removed|superseded', re.I)


def _asserts_universal_ratification(text):
    """Sentences that state a blanket 'a protocol must be ratified' rule.

    Scoped to the sentence, and skipped where the sentence is negating or
    flagging the claim -- the corrected answer names this exact error as a
    trap, and a guard that cannot tell a warning from an assertion would make
    the correct answer unshippable.
    """
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not re.search(r'protocol', s, re.I):
            continue
        if not re.search(r'(must|always|shall|requires?)\s+(be\s+)?ratif', s, re.I):
            continue
        if _NEGATED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


#: FIX-A. The five IMO instruments the version 2.1 text named as familiar
#: examples of the designation Convention. Only MARPOL is in Sources A-F, so
#: MARPOL is deliberately NOT in this list -- it is the worked example and must
#: stay. The other four were never read at source for this entry.
_UNSOURCED_INSTRUMENTS = re.compile(
    r'\bSOLAS\b|\bSTCW\b|\bCOLREGs?\b|\bLoad\s+Lines\b', re.I)


def _asserts_general_convention_operation(text):
    """FIX-B. Sentences making entry into force / amendment a property that a
    convention has BY BEING one, rather than a property of its own terms."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not re.search(r'convention', s, re.I):
            continue
        if not re.search(r'\b(each|every|its|their)\s+(own\s+)?'
                         r'|\bown\s+', s, re.I):
            continue
        if not re.search(r'entry[-\s]into[-\s]force|amendment\s+provision'
                         r'|enters?\s+into\s+force', s, re.I):
            continue
        if _NEGATED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


def _asserts_generic_protocol_relation(text):
    """FIX-C. Sentences stating what a protocol is related to AS A CLASS. The
    approved narrow form names the 1978/1973 MARPOL instruments, so a sentence
    that names them is scoped to the example and is not a taxonomy claim."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not re.search(r'protocol', s, re.I):
            continue
        if not re.search(r'related\s+to\s+another\s+instrument'
                         r'|\b(normally|generally|usually|typically|as\s+a\s+rule)\b'
                         r'[^,]{0,60}\brelated\b', s, re.I):
            continue
        if re.search(r'1978|1973|MARPOL', s, re.I):
            continue
        if _NEGATED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


def _asserts_generic_party_status(text):
    """FIX-D. The general claim about a State's party status to a convention
    as against a protocol relating to it."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not re.search(r'part(y|ies)\s+to\s+a\s+convention', s, re.I):
            continue
        if not re.search(r'without\s+being\s+part(y|ies)|\bprotocol\b', s, re.I):
            continue
        if _NEGATED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


# --------------------------------------------------------------------------
# FINAL FIX 1..5 -- the authority-boundary corrections made at version 2.3.
#
# The third independent review found the central legal correction SOUND against
# the primary instruments and left five residual overreaches. Each is guarded
# below by a detector aimed at THAT formulation and no other, so that the
# mutation harness can prove each guard independently non-vacuous.
#
# Every detector reads the CANDIDATE-FACING projection only. The withdrawn
# wording is legitimately named, in its own words, inside the internal-only
# version_history fields and the governance correction record under
# corrections/ -- a guard that rejected it THERE would be pushing provenance
# out of the one place it is supposed to live, which is the opposite of the
# discipline these gates exist to enforce.
# --------------------------------------------------------------------------

#: The designation nouns the withdrawn version 2.2 sentence enumerated. Source
#: A establishes only that the definition applies 'whatever its particular
#: designation'; it does NOT enumerate which titles qualify, and none of the
#: listed instruments was read at source for this entry.
_DESIGNATION_NOUNS = (
    r'convention', r'protocol', r'agreement', r'charter', r'covenant',
    r'pact', r'accord', r'declaration', r'statute',
)


#: An ENUMERATION of designations, matched by its grammatical SHAPE rather
#: than by counting nouns in a window: three or more designation nouns strung
#: into a comma list closed by 'or'/'and'. Shape is what separates asserting a
#: list of titles from merely discussing titles -- the corrected answer does a
#: great deal of the latter ("Convention and protocol are designations given to
#: instruments...") and a noun-counting detector made that unshippable.
_DESIGNATION_ENUM = re.compile(
    r'(?:%(n)s)\s*(?:</?b>\s*)*,\s*(?:</?b>\s*)*(?:%(n)s)'
    r'(?:\s*(?:</?b>\s*)*,\s*(?:</?b>\s*)*(?:%(n)s))*'
    r'\s*(?:</?b>\s*)*,?\s*(?:or|and)\s+(?:</?b>\s*)*(?:%(n)s)'
    % {'n': '|'.join(_DESIGNATION_NOUNS)}, re.I)


def _asserts_designation_example_list(text):
    """FINAL FIX 1. Sentences that ENUMERATE designations said to be treaties.

    Scoped to a genuine enumeration so that the source-safe sentences naming
    convention and protocol as the two designations this limb is about are not
    caught. The replacement quotes Article 2(1)(a)'s own words -- 'whatever its
    particular designation' -- instead of listing which titles qualify, because
    Source A establishes the phrase and not the list.
    """
    bad = []
    for s in _SENT_SPLIT.split(text):
        m = _DESIGNATION_ENUM.search(s)
        if not m:
            continue
        if _NEGATED.search(s):
            continue
        bad.append(m.group(0).strip()[:160])
    return bad


#: A NARROWER negation test, for the three FINAL FIX detectors below.
#:
#: _NEGATED skips any sentence containing 'no'/'not'/'never', on the theory
#: that a sentence warning about a claim reads differently from one making it.
#: That theory fails for these three formulations, because each of them IS a
#: contrastive negative: "decided by its own final clauses, NOT by its title",
#: "one of function, NOT of rank". Using _NEGATED here made all three guards
#: vacuous -- the mutation harness caught it, which is what it is for.
#: _FLAGGED therefore matches only words that mark a claim as WITHDRAWN or
#: WRONG, and ordinary contrastive negation no longer buys an exemption.
_FLAGGED = re.compile(
    r'trap|myth|wrong|incorrect|universal claim|withdraw|removed'
    r'|superseded|no longer|must not', re.I)


#: The withdrawn 'own final clauses' formulation. Source D (VCLT Article 11)
#: says the listed means are available where the instrument or the States
#: concerned so agree -- which is narrower than a general rule that an
#: instrument's concluding provisions FIX which means are available.
_FINAL_CLAUSES = re.compile(r'final\s+clauses', re.I)


def _asserts_final_clauses_consent_rule(text):
    """FINAL FIX 2. The Article 11 / means-of-consent sentence specifically."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not _FINAL_CLAUSES.search(s):
            continue
        if not re.search(r'article\s+11|means\s+of\s+(expressing\s+)?consent'
                         r'|means\s+is\s+|means\s+are\s+', s, re.I):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


def _asserts_final_clauses_protocol_rule(text):
    """FINAL FIX 3. The protocol paragraph / comparison-table formulation."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not _FINAL_CLAUSES.search(s):
            continue
        if not re.search(r'\bprotocol\b|\bpart(y|ies)\b|becomes?\s+bound'
                         r'|consent\s+to\s+be\s+bound', s, re.I):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


def _asserts_functional_taxonomy(text):
    """FINAL FIX 4. The general 'the difference is one of function' claim.

    Sources A-F establish the ABSENCE of hierarchy between the designations.
    They do not establish an affirmative functional taxonomy that says what
    each designation is FOR, so that taxonomy is withdrawn rather than
    qualified.
    """
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not re.search(r'\bdistinction\b|\bdifference\b|\bseparates\b'
                         r'|\bdistinguish', s, re.I):
            continue
        if not re.search(r'one\s+of\s+function|of\s+function\s*,?\s*not'
                         r'|\bjob\s+(the|that|an?)\s+instrument\s+does'
                         r'|\bfunction\b[^.]{0,40}\bnot\b[^.]{0,20}\brank\b'
                         r'|\bby\s+function\b', s, re.I):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


#: FINAL FIX 5. The single recall sentence corrected at 2.3, and the exact
#: formulation it replaced. The rest of the recall is unchanged word for word,
#: which is why this guard names ONE sentence rather than digesting the whole.
#: Re-pointed at version 2.5. The sentence required here from 2.3 was itself a
#: means-available-depends formulation and was withdrawn at 2.5 (it is now
#: forbidden by G32). The WITHDRAWN pattern below is unchanged -- the 2.3
#: regression stays guarded -- and what the recall must now carry is the
#: narrower Article 11 inference that replaced it.
_RECALL_REQUIRED = 'ratification is not the only means it lists'
_RECALL_WITHDRAWN = re.compile(
    r"How\s+a\s+State\s+becomes\s+bound\s+is\s+decided\s+by\s+the\s+"
    r"instrument's\s+OWN\s+FINAL\s+CLAUSES", re.I)


# --------------------------------------------------------------------------
# FINAL FIX A..D -- the source-boundary corrections made at version 2.4.
#
# The fourth independent review again found the central legal correction SOUND
# against the primary instruments and left four residual source-boundary
# overreaches, one of which carried two distinct propositions -- so five
# formulations are withdrawn and five detectors are defined here.
#
# Same two disciplines as the block above. Each detector is aimed at ONE
# formulation so the mutation harness can prove it independently non-vacuous,
# and each reads the CANDIDATE-FACING projection only: the withdrawn wording is
# legitimately named, in its own words, inside the internal-only
# version_history fields (authority_hold at 2.4 inventories all five) and in
# the governance correction record under corrections/.
# --------------------------------------------------------------------------

#: FINAL FIX A. The unsourced second limb of the consent sentence. Sources A-F
#: carry Articles 2(1)(a), 2(1)(b), 3 and 11; they do NOT carry Article 9
#: (adoption of the text), so the proposition about what adoption does not by
#: itself establish is withdrawn rather than qualified. Matched on the
#: adoption/consent pairing rather than on the word 'adopt' alone, because the
#: MARPOL history legitimately says the 1973 Convention was ADOPTED on a date
#: and the 1978 Protocol was ADOPTED after the tanker accidents.
_ADOPTION_CONSENT = re.compile(
    r'adopt\w*[^.;]{0,80}\b(?:consent\s+to\s+be\s+bound|bound\s+by\s+it)'
    r'|\b(?:consent\s+to\s+be\s+bound)[^.;]{0,80}\badopt\w*\s+(?:the\s+)?'
    r'(?:treaty\s+)?text', re.I)


def _asserts_adoption_not_consent(text):
    """FINAL FIX A. Sentences tying ADOPTION of the text to consent to be bound.

    The retained sentence says only that a treaty binds those States that have
    expressed consent to be bound; it never reaches adoption, so it does not
    match. A sentence that reintroduces the adoption limb does.
    """
    bad = []
    for s in _SENT_SPLIT.split(text):
        m = _ADOPTION_CONSENT.search(s)
        if not m:
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


#: FINAL FIX B. The broad legal-effect/operation formulation. Sources A-F
#: establish that a title creates no rank; they do not establish a general
#: theory of how an instrument's terms govern its legal effect and operation.
_LEGAL_EFFECT_OPERATION = re.compile(
    r'legal\s+effect\s+and\s+operation|effect\s+and\s+operation\s+of', re.I)


def _asserts_legal_effect_operation(text):
    """FINAL FIX B. The withdrawn Convention legal-effect/operation claim."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not _LEGAL_EFFECT_OPERATION.search(s):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


#: FINAL FIX C. The protocol ABSOLUTE about legal force. The narrowed
#: replacement speaks to inferiority/subordination, which Sources A-F do
#: establish; the absolute reached the instrument's legal force at large,
#: which they do not.
_PROTOCOL_LEGAL_FORCE = re.compile(
    r'\bprotocol\b[^.;]{0,120}\b(?:tells\s+you\s+nothing|says\s+nothing|'
    r'reveals\s+nothing|tells\s+us\s+nothing)[^.;]{0,60}\blegal\s+force\b'
    r'|\b(?:tells\s+you\s+nothing|says\s+nothing)[^.;]{0,60}\blegal\s+force\b',
    re.I)


def _asserts_protocol_legal_force_absolute(text):
    """FINAL FIX C. The withdrawn 'tells you nothing about legal force'."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not _PROTOCOL_LEGAL_FORCE.search(s):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


#: FINAL FIX D, first limb. Source F carries the dated MARPOL history but not
#: the characterisation that the 1978 Protocol ABSORBED the parent instrument.
_MARPOL_ABSORB = re.compile(
    r'\babsorb\w*\b[^.;]{0,80}\b(?:convention|parent|it)\b'
    r'|\b(?:convention|instrument)\b[^.;]{0,60}\bwas\s+absorbed\b'
    r'|\babsorbed\s+into\b', re.I)


def _asserts_marpol_absorption(text):
    """FINAL FIX D(i). The withdrawn absorption characterisation."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not _MARPOL_ABSORB.search(s):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


#: FINAL FIX D, second limb. Source F carries no NAMING-PRACTICE proposition,
#: so the claim about what the combined regime is commonly called -- and the
#: short form itself, which exists on the page only to carry that claim -- are
#: both withdrawn.
_MARPOL_NAMING = re.compile(
    r'MARPOL\s*73\s*/\s*78'
    r'|commonly\s+(?:referred\s+to|called|known)[^.;]{0,80}\bMARPOL\b'
    r'|\bMARPOL\b[^.;]{0,60}\brather\s+than\s+as\s+MARPOL\b', re.I)


def _asserts_marpol_naming_practice(text):
    """FINAL FIX D(ii). The withdrawn naming-practice proposition."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not _MARPOL_NAMING.search(s):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


# --------------------------------------------------------------------------
# EXTERNAL FIX 1..5 -- the source-boundary contractions made at version 2.5.
#
# The fifth independent review again found the central legal core SOUND against
# the primary instruments and found no primary-source conflict, leaving five
# bounded contractions. Same two disciplines as every block above: one detector
# per withdrawn formulation so the mutation harness can prove each guard
# independently non-vacuous, and every detector reads the CANDIDATE-FACING
# projection only. The withdrawn wording is legitimately named, in its own
# words, inside the internal-only version_history fields (authority_hold at 2.5
# inventories all of it) and in the governance correction record under
# corrections/ -- a guard that rejected it THERE would push provenance out of
# its one legitimate home.
# --------------------------------------------------------------------------

#: EXTERNAL FIX 1. The general-term / binding-agreement opening. Source A
#: defines a treaty FOR THE PURPOSES OF THE CONVENTION; it does not establish a
#: general-term proposition standing outside that definition. The paragraph now
#: opens from Article 2(1)(a) itself and no replacement proposition was added.
_GENERAL_TERM_INTRO = re.compile(
    r'general\s+term\s+in\s+international\s+law'
    r'|\bbinding\s+agreement\s+between\s+States\b'
    r'|\bgeneral\s+term\b[^.;]{0,80}\bbinding\s+agreement\b', re.I)


def _asserts_general_term_intro(text):
    """EXTERNAL FIX 1. The withdrawn general-term/binding-agreement intro."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not _GENERAL_TERM_INTRO.search(s):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


#: EXTERNAL FIX 2, first limb. The general binding rule. Sources A-F carry
#: Articles 2(1)(a), 2(1)(b), 3 and 11; none of them states that a treaty binds
#: only those States that have expressed consent. That is VCLT Articles 26 and
#: 34 territory and neither is in the frozen set.
_BINDS_ONLY_CONSENT = re.compile(
    r'binds\s+only\s+those\s+States'
    r'|\bbinding\s+only\s+on\s+those\s+States\b'
    r'|\bbound\s+only\s+those\s+States\b', re.I)


def _asserts_general_binding_rule(text):
    """EXTERNAL FIX 2(i). The withdrawn general binds-only-those-States rule."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not _BINDS_ONLY_CONSENT.search(s):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


#: EXTERNAL FIX 2, second limb. The means-available-depends theory. Source D
#: lists the means and closes with 'or by any other means if so agreed', which
#: does NOT establish a general theory of which means an instrument makes
#: available. Matched on the depends-on-what-is-agreed-for-that shape rather
#: than on 'agreed' alone, because the retained sentence quotes Article 11's own
#: closing words and must stay shippable.
_MEANS_AVAILABLE_DEPENDS = re.compile(
    r'\bdepends?\s+on\s+what\s+is\s+agreed\s+for\s+that\b'
    r'|\bwhich\s+of\s+the[^.;]{0,60}\bmeans\b[^.;]{0,80}\bis\s+available\b'
    r'|\bmeans\b[^.;]{0,40}\bavailable\b[^.;]{0,80}\bdepends?\s+on\s+what\s+is'
    r'\s+agreed\b', re.I)


def _asserts_means_available_depends(text):
    """EXTERNAL FIX 2(ii). The withdrawn means-available-depends formulation."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not _MEANS_AVAILABLE_DEPENDS.search(s):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


#: EXTERNAL FIX 3, first limb. The Treaty row's withdrawn 'What it does' cell.
_CLASS_NOT_INSTRUMENT = re.compile(
    r'\bit\s+is\s+the\s+class\s*,\s*not\s+an\s+instrument\b'
    r'|\bnothing\s+on\s+its\s+own\b[^.;]{0,80}\bclass\b', re.I)


def _asserts_class_not_instrument(text):
    """EXTERNAL FIX 3(i). The withdrawn class-not-an-instrument table cell."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not _CLASS_NOT_INSTRUMENT.search(s):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


#: EXTERNAL FIX 3, second limb. The Protocol row's generic 'Whatever the terms
#: of that particular instrument provide' claim. Sources A-F establish no
#: general theory of what an instrument's terms provide.
_WHATEVER_THE_TERMS = re.compile(
    r'whatever\s+the\s+terms\s+of\s+that\s+particular\s+instrument'
    r'|whatever\s+the\s+terms\s+of\s+the\s+instrument\s+provide', re.I)


def _asserts_whatever_the_terms(text):
    """EXTERNAL FIX 3(ii). The withdrawn generic whatever-the-terms claim."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not _WHATEVER_THE_TERMS.search(s):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


#: EXTERNAL FIX 4, as corrected. Source A makes a protocol's status as a
#: treaty CONDITIONAL on the Article 2(1)(a) criteria, so the candidate-facing
#: Protocol heading must carry that qualification.
#:
#: The earlier form of this guard is the defect this form replaces. It banned
#: only the bare absolute 'Protocol - a treaty in its own right' with an
#: end-anchored match, and then REQUIRED the literal string 'a treaty in its
#: own right where it meets Article 2(1)(a)' on the page. That is a guard
#: written against a particular fix rather than against the rule: it accepted
#: the absolute assertion whenever a qualifier happened to follow it, and it
#: actively LOCKED the residue phrase in, so the contraction could not be
#: completed without the guard failing. Both clauses are gone.
#:
#: What is asserted now is the rule itself, in two parts:
#:   (i) NO candidate-facing Protocol heading may contain 'a treaty in its own
#:       right' at all -- searched, not end-anchored, so a trailing qualifier
#:       does not rescue it; and
#:  (ii) EVERY candidate-facing Protocol heading must carry the Article
#:       2(1)(a) qualification, in whatever words, and at least one must exist
#:       on each surface.
#:
#: THE INPUT BOUNDARY. Both parts are evaluated over TWO candidate-facing
#: surfaces and no others:
#:
#:   SPEC INPUT -- the `h` fields of the candidate-facing heading blocks of the
#:       canonical authoring surface,
#:       meoclass1/current-answers/specs/CA-EM-0003.json: answer.blocks[*].h
#:       and study_guide.blocks[*].h. Both are projected onto the rendered page
#:       by build_current_answers.py, so both are candidate-facing.
#:
#:   PAGE INPUT -- the <h1>..<h6> heading elements of the rendered
#:       candidate-facing projection, solvedQP/current/CA-EM-0003.html.
#:
#: This restores the pairing rule stated at the top of this module: every
#: content guard reads BOTH the canonical spec and the rendered page, because a
#: guard that reads only the spec cannot see a stale projection, and a guard
#: that reads only the page cannot see a spec that will re-render the error on
#: the next build. An earlier form of this guard read the projection ALONE and
#: reasoned that the build would carry any spec regression through to the page.
#: That reasoning made the guard depend on a separate freshness proof for its
#: own soundness, and it detected the authoring defect one whole build LATER
#: than the surrounding suite does. Reading the authoring surface directly is
#: the stronger contract and is what is asserted here.
#:
#: What is STILL outside the boundary, and deliberately so: version_history
#: (rendered or internal-only), review_record, the governance correction record
#: under corrections/, authority_hold, and every other repository path. This is
#: NOT a whole-repository phrase ban and it must never become one. The
#: withdrawn wording is legitimately named, in its own words, inside internal
#: provenance in order to record that it WAS withdrawn; a guard that rejected
#: it there would push provenance out of its one legitimate home.
#:
#: The body paragraph beneath the heading is likewise out of scope on both
#: surfaces -- headings are read off heading BLOCKS and heading ELEMENTS, never
#: off flattened text -- so prose that states the conditional proposition in
#: sentences is untouched.
_RESIDUE_IN_OWN_RIGHT = re.compile(
    r'a\s+treaty\s+in\s+its\s+own\s+right', re.I)
_IS_PROTOCOL_HEADING = re.compile(r'^\s*Protocol\s*[-–—]', re.I)
_CONDITIONAL_PROTOCOL_HEADING = re.compile(
    r'\bArticle\s+2\(1\)\(a\)', re.I)


def _page_headings(html):
    """The heading ELEMENTS of the rendered projection.

    Read off <h1>..<h6> specifically rather than off the flattened page text,
    because the paragraph beneath the heading legitimately states the
    conditional proposition in prose and a whole-page detector could not tell
    the heading from the body.
    """
    return [_strip_tags(m).strip() for m in
            re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html, re.I | re.S)]


def protocol_headings(html):
    """Every candidate-facing Protocol heading on the RENDERED PAGE surface."""
    return [h for h in _page_headings(html) if _IS_PROTOCOL_HEADING.match(h)]


def _spec_headings(spec):
    """The heading BLOCKS of the candidate-facing canonical authoring surface.

    Read off the `h` field of answer.blocks and study_guide.blocks specifically
    -- never off a flattened projection of the spec -- so that the paragraph
    blocks beneath a heading, which legitimately state the conditional
    proposition in prose, are not mistaken for headings. version_history,
    review_record and every other spec field are NOT consulted: see the
    input-boundary note above.
    """
    out = []
    for section in ('answer', 'study_guide'):
        for b in (spec.get(section) or {}).get('blocks') or []:
            if b.get('h'):
                out.append(str(b['h']).strip())
    return out


def spec_protocol_headings(spec):
    """Every candidate-facing Protocol heading on the SPEC surface."""
    return [h for h in _spec_headings(spec) if _IS_PROTOCOL_HEADING.match(h)]


#: EXTERNAL FIX 5. The evaluative clause on the MARPOL history. Source F
#: carries the dated history but no evaluation of how typical it is.
_HISTORY_IS_UNUSUAL = re.compile(
    r'\bthis\s+history\s+is\s+unusual\b'
    r'|\bhistory\s+is\s+unusual\b'
    r'|\bunusual\b[^.;]{0,40}\bhistory\b'
    r'|\bhistory\b[^.;]{0,40}\bis\s+unusual\b', re.I)


def _asserts_history_is_unusual(text):
    """EXTERNAL FIX 5. The withdrawn 'This history is unusual' evaluation."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        if not _HISTORY_IS_UNUSUAL.search(s):
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(s.strip()[:160])
    return bad


# --------------------------------------------------------------------------
# EXT-01..EXT-04 -- the rank-language contractions made at version 2.6.
#
# The sixth independent review found the central legal direction SOUND -- VCLT
# Article 2(1)(a) makes treaty status independent of an instrument's particular
# designation -- but held that Sources A-F establish no general law of legal
# RANK and no hierarchy between instruments in either direction. Four bounded
# formulations were withdrawn, and because all four are the same defect wearing
# four sentences, ONE guard is added rather than four: G37. Adding four
# near-identical detectors would have been guard proliferation, and the
# mutation harness would have proved the same thing four times.
#
# THE INPUT BOUNDARY, stated as narrowly as G35's:
#
#   SPEC INPUT -- the candidate-facing ANSWER and STUDY GUIDE blocks and the
#       quick_revision fields of meoclass1/current-answers/specs/CA-EM-0003.json.
#
#   PAGE INPUT -- solvedQP/current/CA-EM-0003.html with the "Version and review
#       record" section removed.
#
# DELIBERATELY OUTSIDE the boundary: version_history (rendered or internal-only),
# review_record, authority_hold, the governance correction record under
# corrections/, and every other repository path. This is NOT a whole-repository
# phrase ban and must never become one -- the withdrawn wording is legitimately
# named, in its own words, inside internal provenance in order to record that it
# WAS withdrawn, and a guard that rejected it there would push provenance out of
# its one legitimate home.
# --------------------------------------------------------------------------

#: The withdrawn rank formulations, by their own words. Each was carried by a
#: candidate-facing surface at version 2.5 and was contracted at 2.6.
_WITHDRAWN_RANK = re.compile(
    r'confers?\s+no\s+(?:legal\s+)?rank'                    # EXT-01, EXT-02
    r'|\bno\s+legal\s+rank\b'                               # EXT-02
    r'|creat\w*\s+a\s+legal\s+rank'                          # EXT-02 table cell
    r'|legally\s+inferior\s+class'                           # EXT-03
    r'|subordinate\s+to\s+a\s+convention'                    # EXT-03
    r'|\bno\s+ladder\b'                                      # EXT-04
    r'|Article\s+2\(1\)\(a\)\s+settles',                     # EXT-04
    re.I)


def _page_answer_body(html):
    """The rendered page WITHOUT the version and review record.

    _version_block in build_current_answers.py opens the projected version
    history with exactly this container, and nothing else on the page uses it,
    so splitting on it is an exact cut rather than a heuristic one. The cut is
    what keeps this guard off provenance: the rendered history legitimately
    recites what was withdrawn.
    """
    marker = '<div class="%s">' % _VER_SECTION
    return _strip_tags(html.split(marker)[0])


def _spec_answer_text(spec):
    """The candidate-facing TEACHING surface of the spec, without provenance."""
    parts = _blocks_text((spec.get('answer') or {}).get('blocks'))
    parts += _blocks_text((spec.get('study_guide') or {}).get('blocks'))
    qr = spec.get('quick_revision') or {}
    for key in ('recall_15s', 'critical_regulation', 'major_trap'):
        parts.append(str(qr.get(key) or ''))
    parts.extend(str(k) for k in qr.get('keywords') or [])
    parts.extend(str(k) for k in qr.get('critical_numbers') or [])
    return '\n'.join(parts)


def _asserts_withdrawn_rank(text):
    """EXT-01..EXT-04. Sentences carrying a withdrawn rank formulation."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        m = _WITHDRAWN_RANK.search(s)
        if not m:
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(m.group(0).strip()[:160])
    return bad


# --------------------------------------------------------------------------
# EXT-2.6-01..EXT-2.6-03 -- the hierarchy-language contractions made at
# version 2.7.
#
# The seventh independent review found the version 2.6 answer SUBSTANTIALLY
# CORRECT and accepted its legal core: VCLT Article 2(1)(a) makes treaty status
# independent of an instrument's particular designation. What it did not accept
# was three residual clauses that assert something ABOUT rank or hierarchy --
# 'not a rank' in the Convention heading, 'does not create a legal hierarchy'
# in the protocol paragraph, and 'do not create a hierarchy between these
# instruments' in the closing takeaway. Denying a hierarchy is still a
# proposition about hierarchy, and the frozen source set establishes only that
# the designation does not determine whether the definition is MET.
#
# WHY THIS IS A NEW GUARD RATHER THAN A WIDENED G37. G37 is frozen and is not
# touched here. It is also, demonstrably, blind to these three formulations:
# every one of them was live on a candidate-facing surface at version 2.6 and
# G37 passed over all three. Its alternation list reaches 'confers no rank',
# 'no legal rank', 'create a legal RANK', 'legally inferior class', 'subordinate
# to a convention', 'no ladder' and 'Article 2(1)(a) settles' -- and none of
# those matches 'not a rank' or a HIERARCHY formulation. Leaving the three
# corrections to G37 would have left them unguarded.
#
# ONE guard rather than three, on G37's own reasoning: the three contractions
# are one defect wearing three sentences, and three near-identical detectors
# would be guard proliferation proving the same thing three times.
#
# THE INPUT BOUNDARY is G37's, exactly:
#
#   SPEC INPUT -- the candidate-facing ANSWER and STUDY GUIDE blocks and the
#       quick_revision fields of meoclass1/current-answers/specs/CA-EM-0003.json.
#
#   PAGE INPUT -- solvedQP/current/CA-EM-0003.html with the "Version and review
#       record" section removed.
#
# DELIBERATELY OUTSIDE the boundary: version_history (rendered or internal-only),
# review_record, authority_hold, the governance correction record under
# corrections/, and every other repository path. This is NOT a whole-repository
# phrase ban and must never become one -- the withdrawn wording is named, in its
# own words, in the internal-only authority_hold of the 2.7 row precisely so
# that the record of its withdrawal survives, and a guard that rejected it there
# would push provenance out of its one legitimate home.
# --------------------------------------------------------------------------

#: The withdrawn hierarchy formulations, by their own words.
_WITHDRAWN_HIERARCHY = re.compile(
    r'\bnot\s+a\s+rank\b'                                     # EXT-2.6-01
    r'|creat\w*\s+a\s+legal\s+hierarchy'                      # EXT-2.6-02
    r'|creat\w*\s+a\s+hierarchy\s+between\s+these\s+instruments',  # EXT-2.6-03
    re.I)


def _asserts_withdrawn_hierarchy(text):
    """EXT-2.6-01..EXT-2.6-03. Sentences carrying a withdrawn hierarchy
    formulation. Contraction by REMOVAL: there is no narrower replacement
    proposition about rank or hierarchy, and none may be substituted."""
    bad = []
    for s in _SENT_SPLIT.split(text):
        m = _WITHDRAWN_HIERARCHY.search(s)
        if not m:
            continue
        if _FLAGGED.search(s):
            continue
        bad.append(m.group(0).strip()[:160])
    return bad


# --------------------------------------------------------------------------
# Review-claim predicates.
#
# These are OPEN-G1-014-specific and are deliberately NOT a change to the
# library-wide review architecture: global R-CA-REVIEW-PASS in
# validate_current_answers.py is untouched and unweakened. They exist because
# this entry exposed a distinction that gate does not draw.
#
#   HONESTY / BUILDABLE-FOR-REVIEW  -- may the entry be built and handed to a
#       reviewer? TRUE while the current version's review is explicitly
#       OUTSTANDING, because saying so is honest. FALSE the moment the entry
#       CLAIMS a review it does not have.
#
#   PUBLICATION-ELIGIBLE -- may this reach a candidate as a verified answer?
#       TRUE only when an independent PASS is tied to the CURRENT answer
#       version. An older version's PASS never carries forward.
#
# The two are separate on purpose. Collapsing them is what let a version 1.0
# PASS render over 2.x text in the first place.
# --------------------------------------------------------------------------

_PASS_CLAIM = re.compile(r'\bPASS\b')
_NO_REVIEW = re.compile(r'OUTSTANDING|NOT\s+YET\s+OBTAINED|PASS_WITH_FIX', re.I)


def _history_row(spec, version):
    for row in spec.get('version_history') or []:
        if str(row.get('version')) == str(version):
            return row
    return None


def current_version_has_pass(spec):
    """Is an independent PASS actually tied to the CURRENT answer version?"""
    row = _history_row(spec, spec.get('answer_version'))
    if row is None:
        return False
    ir = str(row.get('independent_review') or '')
    return bool(_PASS_CLAIM.search(ir)) and not _NO_REVIEW.search(ir)


def claims_current_review(spec):
    """Does the entry PRESENT its review_record as covering the current text?

    Two ways to claim it: saying so, or -- the quieter one -- failing to
    disclaim it. A scope note that simply never mentions the current version
    leaves the rendered 'Independent review: PASS' badge standing over it.
    """
    cur = str(spec.get('answer_version') or '')
    scope = str((spec.get('review_record') or {}).get('scope_of_this_review') or '')
    esc = re.escape(cur)
    if re.search(r'covers?\s+version\s+' + esc, scope, re.I):
        return True
    disclaimed = re.search(
        r'(does\s+not|do\s+not|no[t]?\b)[^.]{0,200}\bversion\s+' + esc, scope, re.I) \
        or re.search(r'\bversion\s+' + esc + r'\b[^.]{0,200}\b(has\s+not|no\b|not\b)',
                     scope, re.I)
    return not disclaimed


def honesty_buildable_for_review(spec):
    """(ok, detail). An entry may never claim a review it does not have."""
    if claims_current_review(spec) and not current_version_has_pass(spec):
        return False, ('review_record is presented as covering answer_version '
                       '%s, but version_history[%s].independent_review records '
                       'no independent PASS for it. An entry may not claim a '
                       'review it does not have.'
                       % (spec.get('answer_version'), spec.get('answer_version')))
    return True, ('review scope is stated truthfully against answer_version %s'
                  % spec.get('answer_version'))


def publication_eligible(spec):
    """(ok, detail). Not a gate -- a reported fact. FALSE is a valid state."""
    cur = spec.get('answer_version')
    if not current_version_has_pass(spec):
        return False, ('no independent PASS is tied to answer_version %s; the '
                       'PASS in review_record belongs to an earlier version '
                       'and does not carry forward' % cur)
    return True, 'an independent PASS is tied to answer_version %s' % cur


def discloses_non_eligibility(spec):
    """If the entry is not publication-eligible, it must SAY so, in the
    current version's own history row -- not leave it to be inferred."""
    if publication_eligible(spec)[0]:
        return True
    row = _history_row(spec, spec.get('answer_version'))
    ir = str((row or {}).get('independent_review') or '')
    return bool(_NO_REVIEW.search(ir))


def run(bundle):
    """Return [(rule, ok, detail)]. Pure over the bundle: no disk access."""
    spec = bundle['spec']
    spec_text = candidate_text(spec)
    page_text = _strip_tags(bundle['page'])
    both = spec_text + '\n' + page_text
    res = []

    def check(rule, ok, detail=''):
        res.append((rule, bool(ok), detail))

    # ---------------------------------------------------------------- G01-G03
    # The three withdrawn hierarchy teachings, by their own words.
    hits = [p for p in (r'subordinate to a parent convention',
                        r'treaty subordinate to')
            if re.search(p, both, re.I)]
    check('G01-NO-TITLE-SUBORDINATION', not hits,
          'a surface still ranks a protocol below a convention by title: %s'
          % hits)

    check('G02-NO-FOUR-LEVEL-LADDER',
          not re.search(r'below all three sit', both, re.I),
          'the four-level ladder Treaty > Convention > Protocol > Code is back')

    check('G03-NO-HIERARCHY-OPENING',
          not re.search(r'open with the hierarchy', both, re.I),
          'the study guide again tells the candidate to open on the hierarchy')

    # ---------------------------------------------------------------- G04-G05
    # The two propositions that replaced them. Required on BOTH surfaces.
    # POSITIVE anchor re-pointed at version 2.6. The subordination limb this
    # guard used to require ('is not a subordinate class') was ITSELF withdrawn
    # at 2.6 as wider than the sources support, and the withdrawn rank
    # formulations are now forbidden outright by G37. Requiring the withdrawn
    # wording here would have LOCKED IN the residue the sixth external review
    # asked to be removed -- the same defect G35 records and replaced. The
    # positive claim the guard now requires is the narrower one that survived:
    # a protocol meeting the Article 2(1)(a) criteria is itself a treaty, and
    # its TITLE ALONE does not alter that conclusion.
    check('G04-PROTOCOL-IS-ITSELF-A-TREATY',
          re.search(r'is\s+itself\s+a\s+treaty', spec_text, re.I)
          and re.search(r'is\s+itself\s+a\s+treaty', page_text, re.I)
          and re.search(r'alone\s+does\s+not\s+alter\s+that\s+conclusion',
                        both, re.I),
          'the positive claim (a protocol is itself a treaty, and its title '
          'alone does not alter that conclusion) is missing from a surface')

    check('G05-DESIGNATION-PHRASE',
          re.search(r'whatever its particular designation', spec_text, re.I)
          and re.search(r'whatever its particular designation', page_text, re.I),
          "VCLT Art.2(1)(a)'s operative words are missing from a surface")

    # ---------------------------------------------------------------- G06
    bad = _asserts_universal_ratification(both)
    check('G06-NO-UNIVERSAL-RATIFICATION', not bad,
          'a blanket protocol-ratification rule is asserted: %s' % bad)

    # ---------------------------------------------------------------- G07-G08
    # The attribution the correction turned on. 2(1)(b) DEFINES the named acts;
    # 11 supplies the MEANS. Collapsing them is what produced the old error.
    check('G07-ART-2-1-B-DEFINES-ACTS',
          re.search(r'2\(1\)\(b\)[^.]{0,200}defin', both, re.I)
          or re.search(r'defin[^.]{0,200}2\(1\)\(b\)', both, re.I),
          'Article 2(1)(b) is not attributed as the DEFINITION of ratification, '
          'acceptance, approval and accession')

    check('G08-ART-11-MEANS-OF-CONSENT',
          re.search(r'article 11[^.]{0,200}means', both, re.I)
          or re.search(r'means[^.]{0,200}article 11', both, re.I),
          'Article 11 is not attributed as the MEANS of expressing consent')

    # ---------------------------------------------------------------- G09-G10
    check('G09-MARPOL-PROT-IV-1-EXAMPLE',
          re.search(r'article iv\(1\)', both, re.I),
          'the instrument-specific worked example (Protocol of 1978 relating '
          'to MARPOL, Art.IV(1)) is gone, leaving the consent point unanchored')

    check('G10-ART-3-SCOPE-QUALIFICATION',
          re.search(r'article 3', both, re.I),
          'the Article 3 scope qualification is missing, so Art.2(1)(a) reads '
          'as an exhaustive definition of every international agreement')

    # ---------------------------------------------------------------- G11
    # MIW voice must never stand as the legal definition.
    uf = str(spec.get('understand_first') or '')
    sg = ' '.join(_blocks_text((spec.get('study_guide') or {}).get('blocks')))
    check('G11-MIW-LABELLED-SECONDARY',
          re.search(r'MIW EXPLANATION', uf) and re.search(r'secondary', uf, re.I)
          and re.search(r'MIW GUIDANCE', sg) and re.search(r'secondary', sg, re.I),
          'MIW explanation/guidance is no longer labelled secondary to the '
          'legal foundation')

    # ---------------------------------------------------------------- G12
    # Registry and routing properties, without touching a corpus total.
    row = None
    rows = bundle['registry'].get('entries') or bundle['registry'].get('rows') or []
    if isinstance(rows, dict):
        row = rows.get(CA_ID)
    else:
        for r in rows:
            if isinstance(r, dict) and r.get('current_answer_id') == CA_ID:
                row = r
                break
    routed = [rel for rel, txt in bundle['routes'].items() if CA_ID in txt]
    check('G12-REGISTRY-ROUTE-INTEGRITY',
          row is not None
          and row.get('answer_version') == spec.get('answer_version')
          and row.get('renderable') is True
          and len(routed) == len(ROUTE_OWNERS),
          'registry row missing/stale (version must track the spec and the '
          'entry must be renderable), or a route owner stopped resolving: '
          'routed=%s of %s' % (len(routed), len(ROUTE_OWNERS)))

    # ---------------------------------------------------------------- G13-G16
    # The four authority-discipline generalisations withdrawn at version 2.2.
    # Each reads the candidate-facing body of BOTH surfaces and each is scoped
    # so that the provenance record of the withdrawal is not read as the claim.
    body = spec_text + '\n' + page_body(bundle['page'])

    hits = sorted(set(m.group(0) for m in _UNSOURCED_INSTRUMENTS.finditer(body)))
    check('G13-NO-UNSOURCED-IMO-EXAMPLE-LIST', not hits,
          'the candidate-facing text again names IMO instruments that were '
          'never read at source for this entry (Sources A-F carry MARPOL '
          'only): %s' % hits)

    bad = _asserts_general_convention_operation(body)
    check('G14-NO-GENERAL-CONVENTION-OPERATION-CLAIM', not bad,
          "entry into force / amendment is again asserted as something a "
          "convention has by being one, rather than as a matter of that "
          "instrument's own terms: %s" % bad)

    bad = _asserts_generic_protocol_relation(body)
    check('G15-NO-GENERIC-PROTOCOL-RELATION-TAXONOMY', not bad,
          'a general taxonomy claim about what a protocol is related to is '
          'back; only the MARPOL 1978/1973 example is sourced: %s' % bad)

    bad = _asserts_generic_party_status(body)
    check('G16-NO-GENERIC-PARTY-STATUS-CLAIM', not bad,
          'the general claim about party status to a convention as against a '
          'protocol relating to it is back: %s' % bad)

    # ---------------------------------------------------------------- G20-G24
    # The five authority-boundary corrections made at version 2.3. Each guard
    # pairs a NEGATIVE detector (the withdrawn formulation must not return) with
    # a POSITIVE requirement (the narrower replacement must actually be present
    # on both surfaces), because a guard that only forbids can be satisfied by
    # deleting the teaching altogether.
    bad = _asserts_designation_example_list(body)
    check('G20-NO-DESIGNATION-EXAMPLE-LIST',
          not bad
          and re.search(r'whatever its particular designation', spec_text, re.I)
          and re.search(r'whatever its particular designation', page_text, re.I),
          'the candidate-facing text again ENUMERATES designations said to be '
          'treaties, or has lost the Article 2(1)(a) words that replaced the '
          'list. Source A establishes the phrase, not a list of titles: %s'
          % bad)

    bad = _asserts_final_clauses_consent_rule(body)
    check('G21-ART-11-CONSENT-DEPENDS-ON-WHAT-IS-AGREED',
          not bad
          and (re.search(r'article\s+11[^.]{0,300}agreed', spec_text, re.I)
               or re.search(r'agreed[^.]{0,300}article\s+11', spec_text, re.I))
          and (re.search(r'article\s+11[^.]{0,300}agreed', page_text, re.I)
               or re.search(r'agreed[^.]{0,300}article\s+11', page_text, re.I)),
          "the means-of-consent sentence again makes availability a matter of "
          "the instrument's final clauses, or is no longer anchored to Article "
          '11 with availability depending on what is agreed. Source D is '
          'narrower than a general final-clauses rule: %s' % bad)

    bad = _asserts_final_clauses_protocol_rule(body)
    check('G22-PROTOCOL-CONSENT-NOT-GENERALISED',
          not bad
          and re.search(r'article iv\(1\)', body, re.I)
          and re.search(r'without\s+reservation', body, re.I)
          and re.search(r'\baccession\b', body, re.I),
          'the protocol paragraph or the comparison table again generalises '
          "consent or party status to the instrument's final clauses, or the "
          'MARPOL Protocol 1978 Art.IV(1) worked example has lost one of its '
          'three instrument-specific routes: %s' % bad)

    bad = _asserts_functional_taxonomy(body)
    check('G23-NO-FUNCTIONAL-TAXONOMY',
          not bad
          and re.search(r'do not create a hierarchy|no ladder', spec_text, re.I)
          and re.search(r'do not create a hierarchy|no ladder', page_text, re.I),
          'a general Convention/Protocol taxonomy by FUNCTION is back, or the '
          'no-hierarchy statement that replaced it is missing. Sources A-F '
          'establish the absence of a hierarchy, not an affirmative taxonomy '
          'of what each designation is for: %s' % bad)

    recall = str((spec.get('quick_revision') or {}).get('recall_15s') or '')
    check('G24-RECALL-CONSENT-SENTENCE-CORRECTED',
          _RECALL_REQUIRED in recall
          and not _RECALL_WITHDRAWN.search(recall)
          and not _RECALL_WITHDRAWN.search(page_text)
          and _RECALL_REQUIRED.rstrip('.') in _strip_tags(bundle['page']),
          'the 15-second recall no longer carries the corrected consent '
          'sentence, or the withdrawn OWN FINAL CLAUSES formulation is back on '
          'a candidate-facing surface')

    # ---------------------------------------------------------------- G25-G29
    # The four source-boundary corrections made at version 2.4, carrying five
    # withdrawn formulations. Each guard pairs the NEGATIVE detector with the
    # POSITIVE requirement that the narrower replacement is actually present on
    # both surfaces, so that a guard cannot be satisfied by deleting the
    # teaching outright.
    bad = _asserts_adoption_not_consent(body)
    check('G25-NO-UNSOURCED-ADOPTION-CONSENT-CLAIM',
          not bad
          # POSITIVE anchor re-pointed at version 2.5. The sentence this guard
          # used to require ('a treaty binds only those States that have
          # expressed consent to be bound') was ITSELF withdrawn at 2.5 as
          # wider than Sources A-F support, and is now forbidden by G31. The
          # NEGATIVE detector below is unchanged: the adoption limb stays
          # withdrawn. What the guard now requires is the narrower consent
          # statement that survived in its place.
          and re.search(r'Article\s+11[^.]{0,80}means', spec_text, re.I)
          and re.search(r'Article\s+11[^.]{0,80}means', page_text, re.I),
          'the candidate-facing text again ties ADOPTION of the treaty text to '
          'consent to be bound, or has lost the source-supported Article 11 '
          'consent statement that stands alone in its place. Sources A-F carry '
          'Articles 2(1)(a), 2(1)(b), 3 and 11, not the adoption provision: %s'
          % bad)

    bad = _asserts_legal_effect_operation(body)
    check('G26-NO-CONVENTION-LEGAL-EFFECT-CLAIM',
          not bad
          # POSITIVE anchor re-pointed at version 2.6. The replacement this
          # guard used to require was itself a RANK proposition, and the sixth
          # external review withdrew it: Sources A-F make designation
          # irrelevant to whether the Article 2(1)(a) definition is MET, and
          # establish no law of rank in either direction. The anchor is
          # therefore the surviving Convention proposition.
          and re.search(r'titled\s*(?:</?b>\s*)*Convention\s*(?:</?b>\s*)*\s*is'
                        r'\s+a\s+treaty\s+where\s+it\s+meets\s+the\s*'
                        r'(?:</?b>\s*)*Article\s+2\(1\)\(a\)\s*(?:</?b>\s*)*'
                        r'\s*criteria',
                        spec_text, re.I)
          and re.search(r'titled\s*(?:</?b>\s*)*Convention\s*(?:</?b>\s*)*\s*is'
                        r'\s+a\s+treaty\s+where\s+it\s+meets\s+the\s*'
                        r'(?:</?b>\s*)*Article\s+2\(1\)\(a\)\s*(?:</?b>\s*)*'
                        r'\s*criteria',
                        page_text, re.I),
          'the broad legal effect and operation formulation is back, or the '
          'narrower replacement (an instrument titled Convention is a treaty '
          'where it meets the Article 2(1)(a) criteria) is missing from a '
          'surface. Sources A-F establish designation-independence, not a '
          'theory of legal effect and not a law of rank: %s' % bad)

    bad = _asserts_protocol_legal_force_absolute(body)
    check('G27-PROTOCOL-TITLE-CLAIM-NOT-ABSOLUTE',
          not bad
          # POSITIVE anchor re-pointed at version 2.6, for the same reason as
          # G04 and G26: the inferiority/subordination replacement was itself a
          # rank proposition and was withdrawn by the sixth external review. It
          # is now forbidden by G37, so requiring it here would have made the
          # contraction unshippable.
          and re.search(r'alone\s+does\s+not\s+alter\s+that\s+conclusion',
                        spec_text, re.I)
          and re.search(r'alone\s+does\s+not\s+alter\s+that\s+conclusion',
                        page_text, re.I)
          and re.search(r'is\s+itself\s+a\s+treaty', body, re.I),
          'the absolute that being called a protocol tells you nothing about '
          "the instrument's legal force is back, or the narrower replacement "
          '(the title alone does not alter that conclusion) or the retained '
          'Article 2(1)(a) point that such a protocol is itself a treaty is '
          'missing: %s' % bad)

    bad = _asserts_marpol_absorption(body)
    check('G28-NO-MARPOL-ABSORPTION-CLAIM',
          not bad
          and re.search(r'2\s+October\s+1983', spec_text, re.I)
          and re.search(r'2\s+October\s+1983', page_text, re.I),
          'the candidate-facing text again says the 1978 Protocol ABSORBED the '
          'parent Convention, or has lost the dated entry-into-force fact '
          'Source F does carry. Source F carries the history, not the '
          'absorption characterisation: %s' % bad)

    bad = _asserts_marpol_naming_practice(body)
    check('G29-NO-MARPOL-NAMING-PRACTICE-CLAIM',
          not bad
          and re.search(r'2\s+November\s+1973', body, re.I)
          and re.search(r'1976-77', body, re.I)
          and re.search(r'Annex\s+VI', body, re.I),
          'the naming-practice proposition (or the short form that exists only '
          'to carry it) is back on a candidate-facing surface, or the MARPOL '
          'history Source F does carry has been trimmed with it. Retained: '
          '1973 adoption, the 1978 Protocol after the 1976-77 accidents, no '
          'independent entry into force, 2 October 1983, Annex VI: %s' % bad)

    # ---------------------------------------------------------------- G30-G36
    # The five source-boundary contractions made at version 2.5, carrying seven
    # withdrawn formulations. Same pairing discipline: each NEGATIVE detector is
    # backed by the POSITIVE requirement that the narrower replacement really is
    # present on both surfaces, so no guard can be satisfied by deleting the
    # teaching outright.
    bad = _asserts_general_term_intro(body)
    check('G30-NO-GENERAL-TERM-TREATY-INTRO',
          not bad
          and re.search(r'Article\s+2\(1\)\(a\)[^.]{0,120}defines\s+a\s+treaty',
                        spec_text, re.I)
          and re.search(r'Article\s+2\(1\)\(a\)[^.]{0,120}defines\s+a\s+treaty',
                        page_text, re.I),
          'the withdrawn general-term / binding-agreement opening is back, or '
          'the paragraph no longer opens from the Article 2(1)(a) definition '
          'that replaced it. Source A defines a treaty for the purposes of the '
          'Convention and establishes no general-term proposition: %s' % bad)

    bad = _asserts_general_binding_rule(body)
    check('G31-NO-GENERAL-BINDS-ONLY-CONSENT-CLAIM',
          not bad
          and re.search(r'ratification\s+is\s+not\s+the\s+only\s+means\s+it'
                        r'\s+lists', spec_text, re.I)
          and re.search(r'ratification\s+is\s+not\s+the\s+only\s+means\s+it'
                        r'\s+lists', page_text, re.I),
          'the general binds-only-those-States rule is back, or the narrower '
          'Article 11 inference that replaced it is missing from a surface. '
          'Sources A-F carry Articles 2(1)(a), 2(1)(b), 3 and 11, not the '
          'general binding rule: %s' % bad)

    bad = _asserts_means_available_depends(body)
    check('G32-NO-MEANS-AVAILABLE-DEPENDS-CLAIM',
          not bad
          and (re.search(r'article\s+11[^.]{0,300}agreed', spec_text, re.I)
               or re.search(r'agreed[^.]{0,300}article\s+11', spec_text, re.I)),
          'the withdrawn theory that which Article 11 means is AVAILABLE '
          'depends on what is agreed for that instrument is back, or Article '
          "11's own closing words have been lost with it. Source D lists the "
          'means; it establishes no theory of availability: %s' % bad)

    bad = _asserts_class_not_instrument(body)
    check('G33-NO-CLASS-NOT-AN-INSTRUMENT-CELL',
          not bad
          and [b for b in ((spec.get('answer') or {}).get('blocks') or [])
               if (b.get('table') or {}).get('headers')
               == ['Term', 'Source-safe distinction']],
          'the withdrawn Treaty cell (nothing on its own - it is the class, '
          'not an instrument) is back, or the comparison table is no longer '
          "the two-column Term / Source-safe distinction table that replaced "
          'the four-column taxonomy: %s' % bad)

    bad = _asserts_whatever_the_terms(body)
    check('G34-NO-GENERIC-WHATEVER-THE-TERMS-CLAIM',
          not bad
          and re.search(r'article iv\(1\)', body, re.I),
          'the generic claim that a protocol does whatever the terms of that '
          'particular instrument provide is back, or the instrument-specific '
          'Source-E form that replaced it has gone. Sources A-F establish no '
          "general theory of what an instrument's terms provide: %s" % bad)

    spec_ph = spec_protocol_headings(spec)
    page_ph = protocol_headings(bundle['page'])
    residue_spec = [h for h in spec_ph if _RESIDUE_IN_OWN_RIGHT.search(h)]
    residue_page = [h for h in page_ph if _RESIDUE_IN_OWN_RIGHT.search(h)]
    uncond_spec = [h for h in spec_ph
                   if not _CONDITIONAL_PROTOCOL_HEADING.search(h)]
    uncond_page = [h for h in page_ph
                   if not _CONDITIONAL_PROTOCOL_HEADING.search(h)]
    check('G35-PROTOCOL-HEADING-CONDITIONAL',
          not residue_spec and not residue_page
          and not uncond_spec and not uncond_page
          and bool(spec_ph) and bool(page_ph),
          'a candidate-facing Protocol heading asserts the withdrawn absolute '
          '(a treaty in its own right) -- a trailing qualifier does not rescue '
          'it -- or a Protocol heading no longer carries the Article 2(1)(a) '
          'qualification, or no Protocol heading exists at all. Source A makes '
          'that status conditional on the Article 2(1)(a) criteria. Evaluated '
          'over BOTH candidate-facing surfaces: the heading blocks of %s and '
          'the heading elements of %s. '
          'spec: residue=%r unconditional=%r headings=%d | '
          'page: residue=%r unconditional=%r headings=%d'
          % (os.path.relpath(SPEC, REPO).replace(os.sep, '/'),
             os.path.relpath(PAGE, REPO).replace(os.sep, '/'),
             residue_spec, uncond_spec, len(spec_ph),
             residue_page, uncond_page, len(page_ph)))

    bad = _asserts_history_is_unusual(body)
    check('G36-NO-HISTORY-IS-UNUSUAL-CLAIM',
          not bad
          and re.search(r'not\s+as\s+a\s+general\s+rule\s+about\s+what'
                        r'\s+protocols\s+do', spec_text, re.I)
          and re.search(r'not\s+as\s+a\s+general\s+rule\s+about\s+what'
                        r'\s+protocols\s+do', page_text, re.I),
          'the withdrawn evaluative clause (this history is unusual) is back on '
          'a candidate-facing surface, or the boundary statement that this is '
          "MARPOL's own history and not a general rule about what protocols do "
          'has been lost with it. Source F carries the dated history, not an '
          'evaluation of how typical it is: %s' % bad)

    # ---------------------------------------------------------------- G37
    # The four rank-language contractions made at version 2.6. One guard, two
    # candidate-facing surfaces, and the same pairing discipline as every guard
    # above: the NEGATIVE detector is backed by the POSITIVE requirement that
    # the narrower designation-independence propositions really are present, so
    # the guard cannot be satisfied by deleting the teaching outright.
    teaching = _spec_answer_text(spec)
    page_answer = _page_answer_body(bundle['page'])
    bad = _asserts_withdrawn_rank(teaching) + _asserts_withdrawn_rank(page_answer)
    check('G37-NO-WITHDRAWN-RANK-FORMULATION',
          not bad
          and re.search(r'does\s+not\s+determine\s+whether\s+it\s+falls'
                        r'\s+within', teaching, re.I)
          and re.search(r'does\s+not\s+determine\s+whether\s+it\s+falls'
                        r'\s+within', page_answer, re.I)
          and re.search(r'alone\s+does\s+not\s+alter\s+that\s+conclusion',
                        teaching, re.I)
          and re.search(r'alone\s+does\s+not\s+alter\s+that\s+conclusion',
                        page_answer, re.I),
          'a withdrawn rank formulation is back on a candidate-facing teaching '
          'surface, or one of the narrower designation-independence '
          'propositions that replaced them has been lost. Sources A-F make '
          "treaty status independent of an instrument's designation; they "
          'establish no general law of legal rank and no hierarchy between '
          'instruments in either direction. Evaluated over the answer, study '
          'guide and quick_revision of the canonical spec and over the '
          'rendered page with the version and review record removed -- '
          'provenance is deliberately outside the boundary: %s' % bad)

    # ---------------------------------------------------------------- G38
    # The three hierarchy-language contractions made at version 2.7, over
    # G37's input boundary exactly. Same pairing discipline: the NEGATIVE
    # detector is backed by a POSITIVE requirement, so the guard cannot be
    # satisfied by deleting the surrounding teaching outright. The positive
    # limbs are deliberately the SURVIVING source-safe propositions and NOT the
    # exact replacement heading -- requiring a particular fix wording is the
    # defect G35 records, and it would lock the entry out of the bare
    # 'Convention' heading the review expressly allowed.
    bad = (_asserts_withdrawn_hierarchy(teaching)
           + _asserts_withdrawn_hierarchy(page_answer))
    _TITLES_ALONE = r'titles\s+alone\s+do\s+not\s+determine\s+treaty\s+status'
    _MARPOL_RELATION = (r'is\s+related\s+to\s+the\s*(?:</?b>\s*)*1973\s+MARPOL'
                        r'\s+Convention')
    check('G38-NO-WITHDRAWN-HIERARCHY-FORMULATION',
          not bad
          and re.search(_TITLES_ALONE, teaching, re.I)
          and re.search(_TITLES_ALONE, page_answer, re.I)
          and re.search(_MARPOL_RELATION, teaching, re.I)
          and re.search(_MARPOL_RELATION, page_answer, re.I),
          'a withdrawn hierarchy formulation is back on a candidate-facing '
          'teaching surface, or one of the source-safe propositions that '
          'survived the contraction has been lost with it (the takeaway that '
          'titles alone do not determine treaty status, and the relationship '
          'between the 1978 Protocol and the 1973 MARPOL Convention). Denying '
          'a hierarchy is still a proposition ABOUT hierarchy; the frozen '
          'source set establishes only that an instrument\'s designation does '
          'not determine whether the Article 2(1)(a) definition is met, and no '
          'rank or hierarchy proposition may be substituted for a withdrawn '
          'one. Evaluated over the answer, study guide and quick_revision of '
          'the canonical spec and over the rendered page with the version and '
          'review record removed -- provenance is deliberately outside the '
          'boundary: %s' % bad)

    # ---------------------------------------------------------------- G19
    # Internal workflow vocabulary must not reach a rendered surface. Scoped
    # to the CANDIDATE-VISIBLE projection only: the internal-only fields of
    # version_history, and the governance correction record under
    # corrections/, are where this vocabulary is supposed to live, and this
    # guard must not push provenance out of them.
    vocab = sorted(set(m.group(0) for m in _INTERNAL_VOCAB.finditer(body)))
    check('G19-NO-INTERNAL-VOCAB-IN-RENDERED-SURFACE', not vocab,
          'internal workflow vocabulary reached the candidate-visible '
          'projection (the rendered version and review record is part of it): '
          '%s -- this belongs in the internal-only version_history fields %s '
          'or in the governance correction record'
          % (vocab, list(INTERNAL_ONLY_HISTORY_FIELDS)))

    # ---------------------------------------------------------------- G17-G18
    ok, detail = honesty_buildable_for_review(spec)
    check('G17-REVIEW-CLAIM-HONESTY', ok, detail)

    check('G18-NON-ELIGIBILITY-DISCLOSED', discloses_non_eligibility(spec),
          'this entry is not publication-eligible and does not say so in '
          'version_history[%s].independent_review, so the shortfall has to be '
          'inferred rather than read' % spec.get('answer_version'))

    return res


def main():
    try:
        bundle = load_bundle()
    except OSError as exc:
        print('ABORT: cannot read a CA-EM-0003 surface: %s' % exc)
        return 1
    results = run(bundle)
    bad = 0
    for rule, ok, detail in results:
        print('[%s] %s' % ('PASS' if ok else 'FAIL', rule))
        if not ok:
            print('       ' + detail)
            bad += 1
    print('\n%d/%d OPEN-G1-014 definition invariants pass over %s.'
          % (len(results) - bad, len(results), CA_ID))

    # Reported, not gated. PUBLICATION-ELIGIBLE=FALSE is a legitimate state
    # for an entry whose current-version review is honestly outstanding; it is
    # NOT a gate failure, and it is NOT allowed to be silent either.
    spec = bundle['spec']
    h_ok, h_why = honesty_buildable_for_review(spec)
    p_ok, p_why = publication_eligible(spec)
    print('\nanswer_version               %s' % spec.get('answer_version'))
    print('HONESTY / BUILDABLE-FOR-REVIEW  %-5s  %s' % (h_ok, h_why))
    print('PUBLICATION-ELIGIBLE            %-5s  %s' % (p_ok, p_why))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
