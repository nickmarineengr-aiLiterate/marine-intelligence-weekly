#!/usr/bin/env python3
"""Question Intelligence -- the governed vocabulary, identity rules and horizon guards.

ONE QI BRAIN. Every evidence band -- archived 2010-2020 secondary pages, MIW's
2021-2022 wording-only papers and the 2023-2026 solved corpus -- resolves through
the identity chain in this module. There is no second recurrence model.

The three claims a historical record can make are kept apart FOREVER:

    QUESTION_TEXT_CLAIM         the source page carries this wording
    SITTING_DATE_CLAIM          the source associates it with this month
    OFFICIAL_OCCURRENCE_CLAIM   DGMA/DG Shipping evidence proves it was set then

They are never collapsed into `verified = true`. A 2010-2020 record may be
CORROBORATED / SECONDARY_CLAIMED / NOT_ESTABLISHED at the same time, which is
enough for INTERNAL recurrence and never enough for a public dated claim.
"""

# --------------------------------------------------------------------------
# HORIZON. Founder decision 2026-08-23: 2010 is the permanent floor.
# --------------------------------------------------------------------------

QI_LOWER_BOUNDARY = '2010-01'
QI_UPPER_BOUNDARY = '2026-08'

QI_HORIZON_RATIONALE = (
    'Founder decision. 2010 is the permanent lower boundary of MIW Question '
    'Intelligence and 2026-08 the ceiling of this Phase-1 release. Pre-2010 '
    'material already held in the repository is ARCHIVE CONTEXT ONLY and may '
    'never enter governed recurrence. No pre-2010 acquisition backlog exists '
    'or may be created.'
)


def in_horizon(sitting):
    """True when a YYYY-MM sitting lies inside the governed QI horizon."""
    return sitting is not None and QI_LOWER_BOUNDARY <= sitting <= QI_UPPER_BOUNDARY


def horizon_violation(sitting):
    """Return a violation code for a sitting outside the horizon, else None."""
    if sitting is None:
        return 'SITTING_MISSING'
    if sitting < QI_LOWER_BOUNDARY:
        return 'PRE_2010_GOVERNED_OCCURRENCE'
    if sitting > QI_UPPER_BOUNDARY:
        return 'POST_UPPER_BOUNDARY_OCCURRENCE'
    return None


# --------------------------------------------------------------------------
# EVIDENCE BANDS -- provenance strength is preserved, never averaged away.
# --------------------------------------------------------------------------

EVIDENCE_BANDS = {
    'HISTORICAL_SECONDARY_ARCHIVE': {
        'window': '2010-01..2020-12',
        'what': 'An archived page of a secondary commercial repository listing '
                'this question entity in this sitting, at this ordinal.',
        'source_class': 'SECONDARY_REPOSITORY_VIA_ARCHIVE',
        'question_text_claim': 'CORROBORATED',
        'sitting_date_claim': 'SECONDARY_CLAIMED',
        'official_occurrence_claim': 'NOT_ESTABLISHED',
        'counts_toward_recurrence': True,
        'licenses_public_dated_claim': False,
    },
    'MIW_WORDING_ONLY': {
        'window': '2021-01..2022-12',
        'what': 'A paper MIW holds a source copy of, carrying printed question '
                'wording and printed rubric. No model answer.',
        'source_class': 'MIW_HELD_SOURCE_COPY',
        'question_text_claim': 'HELD_SOURCE_COPY',
        'sitting_date_claim': 'PRINTED_ON_SOURCE_COPY',
        'official_occurrence_claim': 'NOT_INDEPENDENTLY_VERIFIED',
        'counts_toward_recurrence': True,
        'licenses_public_dated_claim': False,
    },
    'MIW_SOLVED_CANONICAL': {
        'window': '2023-01..2026-08',
        'what': 'A governed, solved MIW paper spec: canonical question, printed '
                'limbs and marks, and a published model answer.',
        'source_class': 'MIW_GOVERNED_SPEC',
        'question_text_claim': 'GOVERNED_CANONICAL',
        'sitting_date_claim': 'PRINTED_ON_SOURCE_COPY',
        'official_occurrence_claim': 'NOT_INDEPENDENTLY_VERIFIED',
        'counts_toward_recurrence': True,
        'licenses_public_dated_claim': False,
    },
}

# Evidence that corroborates WORDING but can never become an exam occurrence.
NON_OCCURRENCE_EVIDENCE = {
    'DGS_OFFICIAL_QUESTION_BANK': {
        'what': 'The Directorate published Question Bank MEO CL-I.',
        'why_not_an_occurrence': (
            'A question bank is question-bank evidence, not exam-occurrence '
            'evidence. It is undated throughout, so it can corroborate that a '
            'wording is official and can never establish that the question was '
            'set in any sitting. Admitting a bank item as an occurrence would '
            'manufacture recurrence out of a catalogue.'
        ),
        'counts_toward_recurrence': False,
        'may_corroborate_wording': True,
    },
    'HOST_RECURRENCE_ANNOTATION': {
        'what': 'The source publisher own cross-set "this also appeared in" '
                'annotation, carried on both the 2010-2020 archived pages and '
                'the 2021-2023 held copies.',
        'why_not_an_occurrence': (
            'It is a claim ABOUT occurrences with no page behind it. The page '
            'that carries the annotation evidences only its own sitting. '
            'Counting the annotation would double-count every sitting it names '
            'and would import the publisher errors as MIW recurrence.'
        ),
        'counts_toward_recurrence': False,
        'may_corroborate_wording': True,
    },
}

# --------------------------------------------------------------------------
# DATE CERTAINTY -- an axis of its own. Coverage never licenses a dated claim.
# --------------------------------------------------------------------------

DATE_CERTAINTY = {
    'OFFICIAL_DATED': 'An official instrument dates this sitting.',
    'PRINTED_ON_SOURCE_COPY': 'The month and year are printed on the source copy MIW holds.',
    'SECONDARY_CLAIMED': 'A secondary repository asserts the month and year. Nothing official confirms it.',
    'NONE': 'No date evidence at all.',
}

PUBLIC_DATED_CLAIM_REQUIRES = 'OFFICIAL_DATED'

# --------------------------------------------------------------------------
# LIMB MODEL -- QUESTION != LIMB. Recurrence is observed at the unit adjudicated.
# --------------------------------------------------------------------------

LIMB_STATES = {
    'WHOLE_QUESTION_ONLY': 'The question carries no printed subparts; the whole question is the unit.',
    'GOVERNED_LIMB': 'A printed subpart, adjudicated, tracked as its own recurrence unit.',
    'STRUCTURAL_LIMB_ONLY': 'A printed subpart that exists structurally but is not tracked as an independent unit; it recurs only with its parent.',
    'REQUIRES_LIMB_ADJUDICATION': 'Limb markers were detected lexically and have NOT been semantically adjudicated. Never a recurrence key.',
}

LIMB_RULE = (
    'A limb occurrence may never be counted as a whole-question occurrence, and '
    'a whole-question occurrence may never be counted as a limb occurrence. Two '
    'families related by WHOLE_VS_LIMB_RELATION share no occurrence.'
)

# --------------------------------------------------------------------------
# FAMILY JOIN VERDICTS -- Opus adjudicates; a score never decides.
# --------------------------------------------------------------------------

JOIN_VERDICTS = {
    'SAME_FAMILY': 'Same examinable answer core, same ask. One family.',
    'SAME_FAMILY_VARIANT': 'Same answer core; wording, limb count or framing differs. One family, variant recorded.',
    'SAME_LIMB_FAMILY': 'Two limbs that ask the same thing across sittings. One limb family.',
    'WHOLE_VS_LIMB_RELATION': 'One is a limb of the other. TWO families, related, sharing no occurrence.',
    'RELATED_BUT_DISTINCT': 'Same topic, different examinable answer core. Two families, related.',
    'DISTINCT': 'Not the same question. No relation recorded.',
    'CURRENT_FRAMEWORK_CHANGED': 'Same ask, but the governing framework moved so far that the answer core is no longer the same.',
    'AMBIGUOUS_HOLD': 'Cannot be settled on held evidence. No join is made and the pair stays visible.',
}

MERGING_VERDICTS = {'SAME_FAMILY', 'SAME_FAMILY_VARIANT', 'SAME_LIMB_FAMILY'}
RELATING_VERDICTS = {'WHOLE_VS_LIMB_RELATION', 'RELATED_BUT_DISTINCT', 'CURRENT_FRAMEWORK_CHANGED'}

ENTITY_DISPOSITIONS = {
    'CONFIDENTLY_FAMILY_OWNED': 'The entity belongs to exactly one governed family.',
    'LEGITIMATE_MULTI_FAMILY_LIMBS': 'The entity belongs to more than one family because its limbs do.',
    'NEW_FAMILY_REQUIRED': 'A real examinable concept with recurrence value and no existing family.',
    'NO_EXISTING_FAMILY': 'No family fits and none is warranted yet.',
    'NO_RECURRENCE_VALUE': 'One governed occurrence, no join. Carries no recurrence signal.',
    'AMBIGUOUS_HOLD': 'Held for evidence.',
}

# --------------------------------------------------------------------------
# COVERAGE STATES -- absence of a page is never absence of an exam.
# --------------------------------------------------------------------------

COVERAGE_STATES = {
    'SOURCE_PRESENT': 'A source page or paper is held for this sitting.',
    'NO_SOURCE_PAGE_FOUND': 'No source page located. Whether a sitting occurred is UNKNOWN.',
    'NO_ARCHIVE_CAPTURE': 'The source page is known to exist and no archive capture of it was obtained.',
    'SITTING_EXISTS_BUT_QUESTION_SOURCE_UNAVAILABLE': 'Independent evidence says a sitting occurred; its questions are not held.',
    'NO_EXAM_OFFICIALLY_EVIDENCED': 'An official instrument states no examination was held. Requires an official citation.',
    'UNKNOWN': 'Not assessed.',
}

ZERO_DENOMINATOR_RULE = (
    'Only NO_EXAM_OFFICIALLY_EVIDENCED may be treated as a confirmed zero-question '
    'sitting. Every other non-present state is UNKNOWN and is excluded from '
    'recurrence denominators rather than counted as a zero.'
)

# --------------------------------------------------------------------------
# RECURRENCE WINDOWS, measured back from the ceiling.
# --------------------------------------------------------------------------

RECURRENCE_WINDOWS = {
    'RECENT_3Y': ('2023-09', QI_UPPER_BOUNDARY),
    'RECENT_5Y': ('2021-09', QI_UPPER_BOUNDARY),
    'MEDIUM_10Y': ('2016-09', QI_UPPER_BOUNDARY),
    'FULL_HORIZON': (QI_LOWER_BOUNDARY, QI_UPPER_BOUNDARY),
}

HORIZON_LANGUAGE = '2010 through August 2026'
HORIZON_ELAPSED_NOTE = (
    'Exactly 200 months of calendar span, 2010-01 to 2026-08 inclusive. Say '
    '"2010 through August 2026". Never round to "16 years", and never say it '
    'publicly at all -- the historical dates are secondary-claimed.'
)

# --------------------------------------------------------------------------
# INTELLIGENCE LABELS -- multidimensional on purpose.
# --------------------------------------------------------------------------

INTELLIGENCE_LABELS = {
    'PERSISTENT': 'Occurrences in >=4 distinct years and a span of >=60 months.',
    'RECENTLY_ACTIVE': 'At least one occurrence inside RECENT_3Y.',
    'RISING': 'The RECENT_3Y occurrence rate per year is >=2x the earlier rate, on >=2 recent occurrences.',
    'RE_EMERGING': 'A meaningful dormancy gap was closed by a later occurrence.',
    'DORMANT': 'No occurrence inside RECENT_3Y while the family has >=2 occurrences overall.',
    'HISTORICAL_ONLY': 'Every occurrence lies in the 2010-2020 band.',
    'NEW_EMERGING': 'First occurrence inside RECENT_5Y and >=2 occurrences.',
    'INSUFFICIENT_HISTORY': 'Fewer than 2 governed occurrences.',
}

MULTIDIMENSIONAL_RULE = (
    'A family carries every label it earns. LONG_TERM PERSISTENT and '
    'RECENTLY_ACTIVE together is a real and common state; forcing one '
    'mutually exclusive marketing label would destroy the signal.'
)

DORMANCY_GAP_MONTHS = 36
DORMANCY_RULE = (
    'A gap of 36 months or more between consecutive occurrences is a MEANINGFUL '
    'GAP. A family whose history contains a meaningful gap and which has occurred '
    'since is RE_EMERGING -- structurally different from continuous recurrence, '
    'and it must not be reported as a flat total.'
)

# --------------------------------------------------------------------------
# CURRENTNESS -- NOT recurrence. A 12-time repeat can be obsolete.
# --------------------------------------------------------------------------

CURRENTNESS_CLASSES = {
    'CURRENT': 'The framework behind the answer core is unchanged.',
    'CURRENT_WITH_AMENDMENT': 'Still examinable; the instrument has been amended and the answer must reflect it.',
    'CURRENT_FRAMEWORK_CHANGED': 'Still asked, but the governing framework has materially moved.',
    'LIKELY_SUPERSEDED': 'The instrument or practice behind it has been replaced.',
    'HISTORICAL_ONLY': 'No longer examinable under the present framework.',
    'CURRENTNESS_REVIEW_REQUIRED': 'Carries a currentness risk signal and has not been researched.',
    'UNKNOWN': 'Not assessed. Never read as CURRENT.',
}

CURRENTNESS_INVARIANT = (
    'Currentness never changes a recurrence count. Recurrence answers "what kept '
    'coming back"; currentness answers "would the same answer still be right". '
    'They are computed from different inputs and stored in different fields.'
)

# Time-relative language: dangerous precisely because it names no instrument,
# so an instrument-name trigger is blind to it.
TIME_RELATIVE_TRIGGERS = [
    'ongoing development', 'ongoing developments', 'latest', 'recent', 'recently',
    'current status', 'present status', 'present day', 'present-day', 'new generation',
    'new requirement', 'new requirements', 'recent amendment', 'recent amendments',
    'latest amendment', 'latest amendments', 'upcoming', 'forthcoming',
    'expected shortly', 'expected to come into force', 'emerging trend',
    'emerging trends', 'modern methods', 'newly introduced',
    'in recent times', 'presently', 'state of the art', 'new digital technologies',
    'is now mentioned', 'being considered', 'growing means',
]

# Framework-change risk: named instruments and domains that moved inside the horizon.
FRAMEWORK_CHANGE_TRIGGERS = [
    'greenhouse gas', 'ghg', 'decarbonis', 'decarboniz', 'net zero', 'net-zero',
    'eedi', 'eexi', 'cii', 'carbon intensity', 'seemp', 'emission', 'sulphur', 'sulfur',
    'ballast water', 'bwm', 'hong kong convention', 'ship recycling', 'recycling',
    'stcw', 'mlc', 'ism code', 'isps', 'cyber', 'polar code', 'imo 2020',
    'annex vi', 'marpol', 'solas', 'llmc', 'hns', 'wreck removal', 'anti fouling',
    'antifouling', 'af paints', 'r.o. code', 'ro code', 'iacs', 'goal-based', 'gbs',
    'alternative fuel', 'ammonia', 'hydrogen', 'lng', 'methanol', 'biofuel',
    'life cycle analysis', 'well-to-wake', 'market-based', 'enhanced survey',
    'fal convention', 'unclos', 'merchant shipping act', 'nox', 'sox', 'tier',
]

# --------------------------------------------------------------------------
# PHASE-2 ACTIONS -- the bridge out of Phase 1.
# --------------------------------------------------------------------------

PHASE2_ACTIONS = {
    'CURRENT_AND_SOLVED': 'A current MIW answer exists and carries no currentness risk signal.',
    'EXISTING_CURRENT_ANSWER_VERIFY': 'A solved answer exists and a currentness risk signal fires against it.',
    'NEW_MODERN_ANSWER_REQUIRED': 'Materially recurrent and MIW holds no solved answer at all.',
    'HISTORICAL_ANSWER_REQUIRES_MODERNISATION': 'Recurrent historically with a solved answer whose framework has moved.',
    'SUPERSEDED_MODERN_REPLACEMENT_REQUIRED': 'The ask survives but the framework behind it has been replaced.',
    'CURRENTNESS_RESEARCH_REQUIRED': 'Currentness cannot be triaged from held evidence.',
    'LOW_PRIORITY_HISTORICAL_ONLY': 'Recurred only in the historical band and shows no modern life.',
    'AMBIGUOUS_FAMILY_REVIEW': 'The family itself is held for adjudication.',
}

MODERN_QUESTION_ACTIONS = {
    'USE_EXISTING_CANONICAL_QUESTION': 'A solved canonical question already states the modern ask.',
    'MODERNISE_CANONICAL_QUESTION': 'The canonical question needs re-framing for the present framework.',
    'CREATE_NEW_CURRENT_CANONICAL_QUESTION': 'No modern canonical question exists for a live recurrence.',
    'SPLIT_LIMB_FAMILY': 'The family mixes limb and whole-question units and must be split in Phase 2.',
    'MERGE_VARIANTS': 'Several canonical questions state one ask and should converge.',
    'HISTORICAL_ONLY_NO_MODERN_QUESTION': 'No modern canonical question is warranted.',
}

ANSWER_COVERAGE_STATES = {
    'SOLVED_CURRENT_CANDIDATE': 'Exactly one solved MIW answer covers the family.',
    'SOLVED_BUT_CURRENTNESS_UNVERIFIED': 'A solved answer exists and its currentness is unverified.',
    'MULTIPLE_CANDIDATE_ANSWERS': 'More than one solved answer covers the family.',
    'NO_CURRENT_SOLVED_ANSWER': 'No solved answer covers the family.',
    'HISTORICAL_ONLY': 'The family lives entirely in the historical band.',
}

MATERIALLY_RECURRENT_MIN_OCCURRENCES = 2
MATERIALLY_RECURRENT_MIN_SITTINGS = 2

# --------------------------------------------------------------------------
# IDENTITY -- derived from governed attributes, never from wording.
# --------------------------------------------------------------------------

def entity_id(band, native_id):
    """Stable source-entity id. One entity may appear in many sittings."""
    prefix = 'QIE-H-' if band == 'HISTORICAL_SECONDARY_ARCHIVE' else 'QIE-M-'
    return prefix + str(native_id)


def occurrence_id(ent_id, set_id, ordinal, limb=None):
    """Stable occurrence id.

    Built from (entity, set, ordinal, limb) -- NEVER from wording. Two sittings
    printing byte-identical wording are two occurrences, and always will be.
    """
    base = '%s@%s#%s' % (ent_id, set_id, ordinal)
    return base + (':' + limb if limb else '')


def family_id(seq):
    return 'QIF-EM-%04d' % seq


def month_index(sitting):
    """YYYY-MM -> integer month ordinal, for gap and window arithmetic."""
    y, m = sitting.split('-')
    return int(y) * 12 + int(m)


def months_between(a, b):
    return month_index(b) - month_index(a)


def in_window(sitting, window):
    lo, hi = RECURRENCE_WINDOWS[window]
    return lo <= sitting <= hi


SCHEMA_VERSION = '1.0'
