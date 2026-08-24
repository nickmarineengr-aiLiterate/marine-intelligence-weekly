#!/usr/bin/env python3
"""The current-answer library -- schema, identity, and the ownership resolver.

WHY THIS EXISTS
---------------
MIW written answers are SITTING-ANCHORED: an answer to a February 2024 paper
must be true as at February 2024, and `TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL`
governs that. Phase 2 then asks a different question -- "what should a candidate
write NEXT month?" -- and until now the only place an answer to THAT question
could live was inside a past-paper spec. Which meant it could not live anywhere:
writing a present-day answer into a 2021 paper would make that paper cite law
that did not govern it.

Tranche 002 hit the wall six times and recorded it as
HOLD_NO_CURRENT_ANSWER_OWNER -- "the research closed and the PRODUCT is
missing". This module is the container that was missing.

    AN EXAM QUESTION HAS A DATE.  A CURRENT ANSWER HAS A REVIEW DATE.
    They are different objects. QI connects them.

WHAT THIS IS NOT
----------------
Not a past paper. A record here has no sitting, no printed serial, no printed
marks and no examiner. It is never evidence that anybody was ever asked this
wording, so it contributes ZERO recurrence and ZERO examiner evidence -- see
`validate_current_answers.R-CA-NO-RECURRENCE` and `R-CA-NO-EXAMINER`, which
prove that rather than asserting it.
"""

import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
LIB_DIR = os.path.join(REPO, 'meoclass1', 'current-answers')
SPEC_DIR = os.path.join(LIB_DIR, 'specs')
REGISTRY = os.path.join(LIB_DIR, 'registry.json')
PAGE_DIR = os.path.join(REPO, 'solvedQP', 'current')

SCHEMA = 'miw.current_answers.entry.v1'
REGISTRY_SCHEMA = 'miw.current_answers.registry.v1'

#: The id grammar. Deliberately NOT sitting-derived: a current answer outlives
#: every sitting that evidenced it, and the 2010-2020 concept archive -- when it
#: is built -- must be able to point at these same ids without inventing a year.
#: `EM` is the Engineering Management stream, the same stream letter the QI
#: family ids use (QIF-EM-xxxx), so the two id spaces read as siblings.
CA_ID = re.compile(r'^CA-EM-\d{4}$')

#: A past-paper question id. Present here for ONE reason: to be refused. The
#: single most dangerous thing this library could do is name itself like a
#: sitting, because every downstream consumer -- the recurrence model, the
#: examiner layer, the year sheets -- keys on that shape.
QP_ID = re.compile(r'^QP\d{4}-Q\d+$')


def page_path(caid):
    """Where the rendered page is written.

    Under /solvedQP/ because `middleware.js` matches
    ["/meoclass1/:path*", "/solvedQP/:path*"] and middleware is NEVER invoked
    off-matcher -- a page outside those two prefixes is public whatever its
    headers say. This is not a routing preference, it is the gate.
    """
    return os.path.join(PAGE_DIR, '%s.html' % caid)


def page_url(caid):
    return '/solvedQP/current/%s.html' % caid


#: Scope of one entry. LIMB means the entry answers ONE independently
#: examinable concept inside a multi-concept family -- not "the stem had a
#: bracket in it". See the semantic-split rule in CURRENT_ANSWER_LIBRARY.md.
SCOPES = {'WHOLE_QUESTION', 'LIMB'}

#: Typed ownership. The Phase-2 store used to name an answer with a bare
#: `question_id`, which worked only because there was exactly one kind of owner.
#: There are now four, and deciding between them by inspecting the STRING would
#: put a parsing rule on the critical path of a readiness grant.
OWNER_TYPES = {
    'SOLVED_PAPER': 'A whole solved past-paper question answers this family.',
    'SOLVED_PAPER_LIMB': 'A limb of a solved past-paper question answers ONE '
                         'limb of this family.',
    'CURRENT_LIBRARY': 'A current-answer library entry answers this family.',
    'CURRENT_LIBRARY_LIMB': 'A current-answer library entry answers ONE limb '
                            'of this family.',
}
LIBRARY_OWNER_TYPES = {'CURRENT_LIBRARY', 'CURRENT_LIBRARY_LIMB'}
PAPER_OWNER_TYPES = {'SOLVED_PAPER', 'SOLVED_PAPER_LIMB'}
LIMB_OWNER_TYPES = {'SOLVED_PAPER_LIMB', 'CURRENT_LIBRARY_LIMB'}

#: The other axis. Not a fifth and sixth owner type -- the same four, grouped by
#: SCOPE rather than by where the answer lives, exactly as the three sets above
#: group them by store. It exists because the two ownership SLOTS are scoped:
#: `canonical_current_answer` answers the whole family and
#: `family_current_answers` answers it limb by limb, and until a consumer can
#: name that distinction it has to infer scope from the id -- which is the
#: parsing rule this module was written to remove.
WHOLE_OWNER_TYPES = {'SOLVED_PAPER', 'CURRENT_LIBRARY'}

#: Which owner types each slot may carry. A LIMB owner in the whole slot is the
#: dangerous direction: it says "one of the four things this family asks has
#: been answered" in the field that means "all of them have", and a consumer
#: that reads only the owner ID cannot tell the two apart. See
#: `validate_current_answers.R-CA-OWNER-SLOT`, which refuses the shape, and
#: `study_qi_adapter.question_readiness`, which refuses to act on it even if
#: the shape ever got past the gate.
SLOT_OWNER_TYPES = {
    'canonical_current_answer': WHOLE_OWNER_TYPES,
    'family_current_answers': LIMB_OWNER_TYPES,
}

#: Review status. CURRENT_ANSWER_VERIFIED is the ONLY value that may reach a
#: candidate as a verification claim, and it is earned by authority + an
#: independent review that passed. Section 16.
REVIEW_STATUSES = {
    'DRAFT': 'Authored, not reviewed. Never rendered.',
    'AUTHORITY_ESTABLISHED': 'Primary authority read and dated; no independent '
                             'review yet. Never rendered.',
    'CURRENT_ANSWER_VERIFIED': 'Dated primary authority AND an independent '
                               'review that passed.',
    'SUPERSEDED': 'Replaced by a later version or by another entry.',
}
RENDERABLE = {'CURRENT_ANSWER_VERIFIED'}

#: Reused verbatim from the Phase-2 store rather than re-declared. Section 15:
#: do not invent a parallel citation universe. If a class satisfies the Phase-2
#: authority gate it satisfies this one, and `R-CA-AUTHORITY-VOCAB` proves the
#: two lists have not drifted apart.
ACCEPTED_AUTHORITY = {
    'PRIMARY_IMO', 'PRIMARY_TREATY', 'PRIMARY_INDIAN_STATUTE',
    'PRIMARY_INDIAN_SUBORDINATE', 'COMPETENT_AUTHORITY_RESTATEMENT',
    'CLASSIFICATION_SOCIETY_SUMMARY', 'ENGINEERING_JUDGEMENT',
}
PASSING_REVIEW = {'PASS', 'PASS_WITH_MINOR_FIX'}

#: Every entry is gated. Section 39: current answers are the paid Written
#: product. The public roadmap is unchanged by this layer and `R-CA-PUBLIC`
#: proves it over the shipped bytes.
VISIBILITY = {'GATED'}

#: How a page may describe exam format. `marks_band` is a RECOMMENDATION
#: derived from how the concept has been set, never a printed mark. Section 22:
#: never fabricate "this was a 16-mark exam question".
DEPTH_BASIS = {'RECOMMENDED_NOT_PRINTED'}

#: Where the canonical question text came from. There is no value here meaning
#: "printed on a source copy", because if it were printed on a source copy it
#: would be a past-paper question and would belong in a spec.
QUESTION_ORIGINS = {
    'SYNTHESISED_FROM_FAMILY_WORDING':
        'Written from the recurring wording of the QI family, brought to the '
        'present-day framework. Not a transcription of any one sitting.',
    'SYNTHESISED_FROM_LIMB_WORDING':
        'Written from one limb of the recurring family wording.',
    'AUTHORED_FOR_CURRENT_FRAMEWORK':
        'Written to examine a present-day framework the printed wording '
        'predates.',
}

REQUIRED = (
    'schema', 'current_answer_id', 'title', 'canonical_question',
    'question_origin', 'family_ids', 'scope', 'present_day_examinable_core',
    'answer', 'authority_sources', 'authority_review_date', 'currentness_as_of',
    'review_status', 'answer_version', 'version_history', 'candidate_visibility',
)

#: Keys that would make this record look like a sitting. Refused outright --
#: `R-CA-NO-SITTING`. A field cannot be "mostly absent": the moment one of
#: these appears, some consumer will read it.
FORBIDDEN_SITTING_KEYS = (
    'paper_id', 'sitting', 'month', 'year', 'month_year', 'q_no',
    'printed_serial', 'printed_authority', 'total_marks', 'examiner',
    'source_copy_path', 'sr_no', 'anchor', 'text_verbatim',
)


def _load(path):
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


def load_entries():
    """Every library entry on disk, keyed by id.

    A missing directory is not an error: the library is incremental and started
    empty, exactly like the Phase-2 store it serves.
    """
    out = {}
    if not os.path.isdir(SPEC_DIR):
        return out
    for name in sorted(os.listdir(SPEC_DIR)):
        if not name.endswith('.json'):
            continue
        e = _load(os.path.join(SPEC_DIR, name))
        out[e.get('current_answer_id') or name] = e
    return out


def load_registry():
    return _load(REGISTRY) if os.path.exists(REGISTRY) else None


def is_ca_id(v):
    return bool(isinstance(v, str) and CA_ID.match(v))


def is_qp_id(v):
    return bool(isinstance(v, str) and QP_ID.match(v))


def resolve_owner(obj):
    """Normalise any ownership pointer to ``(owner_type, owner_id)``.

    Three shapes reach here and only one of them is new::

        {'owner_type': ..., 'owner_id': ...}   the typed form (section 17)
        {'question_id': 'QP2606-Q8', ...}      the tranche-001/002 form
        'QP2606-Q8'                            the oldest prose form

    The legacy shapes normalise to SOLVED_PAPER because that is the only thing
    they could ever have meant -- when they were written, a solved past-paper
    question was the only nameable answer in existence. They are NOT extended:
    `validate_phase2_tranche.R-P2-OWNER-TYPED` refuses a library owner written
    in an untyped shape, so the fallback can never quietly acquire a second
    meaning and no consumer ever has to guess from the string.
    """
    if obj is None:
        return (None, None)
    if isinstance(obj, str):
        return ('SOLVED_PAPER', obj)
    if not isinstance(obj, dict):
        return (None, None)
    if obj.get('owner_type') or obj.get('owner_id'):
        return (obj.get('owner_type'), obj.get('owner_id'))
    qid = obj.get('question_id')
    return ('SOLVED_PAPER', qid) if qid else (None, None)


def owner_ids(record):
    """Every (owner_type, owner_id) a Phase-2 family record names, whole or limb.

    One place, so a consumer can never see half the ownership. A family that
    resolves through limbs has no whole-question owner and vice versa; reading
    only `canonical_current_answer` would silently report a multi-limb family as
    unowned, which is how a resolved family comes to read NEW_ANSWER_REQUIRED.
    """
    out = []
    t, i = resolve_owner(record.get('canonical_current_answer'))
    if i:
        out.append((t, i))
    for limb in record.get('family_current_answers') or []:
        t, i = resolve_owner(limb)
        if i:
            out.append((t, i))
    return out


def library_owner_ids(record):
    return [i for t, i in owner_ids(record) if t in LIBRARY_OWNER_TYPES]


def paper_owner_ids(record):
    return [i for t, i in owner_ids(record) if t in PAPER_OWNER_TYPES]


def entry_url_for(record):
    """The one candidate URL a family record routes to, or None.

    A multi-limb family has no single page by design -- its limbs live in
    different places, some of them on past papers -- so this returns None rather
    than picking one. Picking one is the exact error section 34 forbids.

    WHOLE-QUESTION OWNERSHIP ONLY, and the type is what decides it. This used to
    test `t in LIBRARY_OWNER_TYPES`, which is true of CURRENT_LIBRARY_LIMB too --
    so a limb-typed owner written into the whole slot would have been handed back
    as the family's one URL, sending a candidate asked for four concepts to an
    answer about one. That is the error the docstring above forbids, committed by
    the function that forbids it.
    """
    t, i = resolve_owner(record.get('canonical_current_answer'))
    return page_url(i) if t == 'CURRENT_LIBRARY' and i else None
