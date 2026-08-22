#!/usr/bin/env python3
"""The expandable evidence model: stable identity, growing evidence.

    STABLE IDENTITY                 EXPANDING EVIDENCE
    ---------------                 ------------------
    topic_id (D01..D10)             oral question evidence
    official_syllabus_node_id       written question evidence
    canonical_question_id           examiner relationships
    paper_id                        written question intelligence
    family_id                       recurrence families
    examiner identity               historical paper coverage
                                    recency / trend signals
                                    resources, study status
                                    future syllabus versions

Nothing downstream -- workbook, topic page, study landing -- may hardcode a
corpus size. Every count is derived from an evidence horizon, so that adding
papers changes the numbers and the *wording* without editing a renderer.

WHY THIS EXISTS
---------------
A larger MIW Written Question Intelligence effort covering historical MEO
Class I papers is incomplete. It must later become an additional evidence
layer inside THIS system -- not another taxonomy and not another roadmap. So
the socket is defined now, while the schema is cheap to shape, and left
explicitly empty rather than speculatively filled.

THE ENUMS BELOW ARE ADOPTED, NOT INVENTED
-----------------------------------------
`DORMANCY_CLASSES` is taken verbatim from the existing QI-v2 research schema
(`meoclass1/pastpapers/intelligence/v2/QUESTION_FAMILIES.json`,
`miw.pastpapers.qi_v2.families.v2`). That work already reasoned about long-gap
returns against the MEO Class I sitting calendar. Re-deriving a second, subtly
different vocabulary here would be exactly the duplication this layer exists
to prevent.

PUBLIC CLAIMS ARE DERIVED, NEVER WRITTEN BY HAND
------------------------------------------------
`public_evidence_claim()` computes the strongest sentence the *stored*
evidence supports. Until historical QI is validated, it cannot produce a
"16 years of papers" claim, because the horizon it reads does not contain one.
That is the point: the marketing copy cannot outrun the data, because a
generator -- not an author -- writes it.
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

# --- versioning -----------------------------------------------------------
# Semantic versions, never timestamps. `generated_from` carries the corpus's
# own newest `updated` value so two runs over one corpus are byte-identical.
EVIDENCE_MODEL_VERSION = '1.0'
WRITTEN_QI_SCHEMA_VERSION = '1.0'

# --- integration status of an evidence layer ------------------------------
QI_STATUS = ('NOT_STARTED', 'PARTIAL', 'VALIDATED_RANGE', 'COMPLETE')

# --------------------------------------------------------------------------- #
# COVERAGE AND DATE CERTAINTY ARE TWO AXES.
#
# QI_STATUS answers "how much of the window do we hold?".
# DATE_CERTAINTY answers "who says these papers are from those months?".
#
# They are independent, and conflating them is the specific mistake this pair
# blocks. The 2010-2020 recovery adjudicated on 2026-08-23 is a live example:
# 115 of 132 months are held and every page is hashed -- excellent coverage --
# yet not one sitting date comes from an official document. A future session
# looking only at QI_STATUS would see near-complete coverage and reasonably
# conclude that "papers since 2010" is now sayable in public. It is not.
#
# So the PUBLIC claim is gated on DATE_CERTAINTY, never on coverage alone,
# while INTERNAL recurrence analysis is gated on coverage. Being wrong about a
# month costs an internal model a study-priority nudge; it costs a public
# claim its credibility. Different costs, different thresholds, on purpose.
# --------------------------------------------------------------------------- #
DATE_CERTAINTY = (
    'NONE',               # nothing held
    'SECONDARY_CLAIMED',  # a secondary source asserts the month; no official
    'MIXED',              # some papers officially dated, some not
    'OFFICIAL_DATED',     # an official document ties these papers to months
)

# Only this tier may licence a dated public claim.
PUBLIC_DATED_CLAIM_REQUIRES = 'OFFICIAL_DATED'

# --- how a family behaves over time (adopted from qi_v2 families v2) ------
DORMANCY_CLASSES = ('ACTIVE_RECURRENCE', 'RECENT_RETURN', 'HISTORICAL_RETURN',
                    'LONG_GAP_RETURN', 'ONE_OFF_HISTORICAL',
                    'INSUFFICIENT_HISTORY')

# --- whether a historically asked question still counts today -------------
# Historical frequency is NOT current relevance. A family that recurred for a
# decade under a superseded instrument must be able to say so rather than
# being promoted into the study order by its raw count.
RELEVANCE = ('CURRENT_RELEVANT', 'HISTORICAL_RELEVANT', 'SUPERSEDED',
             'REQUIRES_CURRENTNESS_REVIEW')

# --- recurrence windows ---------------------------------------------------
# Raw counts are stored first; these are transparent derived cuts over them.
# There is no weighting and no opaque score: each window is a plain count of
# occurrences inside a stated span, and a consumer may ignore all of them and
# use the raw occurrence list instead.
RECURRENCE_WINDOWS = (
    ('all_time',           None),
    ('last_10_years',      10),
    ('last_5_years',        5),
    ('last_3_years',        3),
    ('current_syllabus_era', None),   # bounded by syllabus era, not by years
)

TREND = ('INCREASING', 'DECREASING', 'PERSISTENT', 'DORMANT', 'RE_EMERGING',
         'INSUFFICIENT_HISTORY')

_PAPER = re.compile(r'^QP(\d{2})(\d{2})$')


def paper_sitting(paper_id):
    """'QP2304' -> (2023, 4). The id is the sitting; month names do not sort."""
    m = _PAPER.match(paper_id)
    if not m:
        return None
    return (2000 + int(m.group(1)), int(m.group(2)))


def current_written_horizon(spec_glob=None):
    """Derive the CURRENT solved-written evidence horizon from the specs.

    Everything here is counted, never asserted. If a paper is added tomorrow
    the horizon widens by itself and every consumer follows.
    """
    spec_glob = spec_glob or os.path.join(
        ROOT, 'meoclass1', 'pastpapers', 'specs', '*.json')
    papers, questions, sittings = [], 0, []
    for path in sorted(glob.glob(spec_glob)):
        spec = json.load(open(path, encoding='utf-8'))
        pid = spec['paper_id']
        papers.append(pid)
        questions += len(spec['questions'])
        s = paper_sitting(pid)
        if s:
            sittings.append(s)
    if not sittings:
        raise SystemExit('FAIL R-HORIZON: no written specs found')
    earliest, latest = min(sittings), max(sittings)
    return {
        'layer': 'CURRENT_SOLVED_WRITTEN',
        'papers_total': len(papers),
        'questions_total': questions,
        'earliest_year': earliest[0],
        'earliest_sitting': f'{earliest[0]}-{earliest[1]:02d}',
        'latest_year': latest[0],
        'latest_sitting': f'{latest[0]}-{latest[1]:02d}',
        'years_spanned': latest[0] - earliest[0] + 1,
        'corpus_version': EVIDENCE_MODEL_VERSION,
        'completeness': 'VALIDATED_RANGE',
        'source_status': 'SOLVED_AND_GOVERNED',
        'papers': papers,
    }


def empty_qi_socket(status='NOT_STARTED', **known):
    """The historical Written QI layer, declared but not yet populated.

    A socket that says NOT_STARTED honestly is worth more than one that
    guesses. Consumers must tolerate every value below being null: a renderer
    that breaks on an unpopulated socket has not actually been made
    expandable, and the schema test asserts exactly that.
    """
    socket = {
        'layer': 'HISTORICAL_WRITTEN_QI',
        'schema_version': WRITTEN_QI_SCHEMA_VERSION,
        'status': status,
        # Coverage says how much; date_certainty says who vouches for WHEN.
        'date_certainty': 'NONE',
        'papers_total': None,
        'questions_total': None,
        'earliest_year': None,
        'earliest_sitting': None,
        'latest_year': None,
        'latest_sitting': None,
        'years_spanned': None,
        'validated_ranges': [],
        'known_gaps': [],
        'corpus_version': None,
        'completeness': status,
        'source_status': 'NOT_INTEGRATED',
        'family_id_namespace': 'FAMILY-EM-',
        'dormancy_classes': list(DORMANCY_CLASSES),
        'relevance_classes': list(RELEVANCE),
        'recurrence_windows': [w for w, _ in RECURRENCE_WINDOWS],
        'trend_classes': list(TREND),
        'integration_point': ('tools/study/build_study_spine.py reads this '
                              'socket; no renderer interprets QI itself'),
    }
    socket.update(known)
    if status not in QI_STATUS:
        raise SystemExit(f'FAIL R-QI-STATUS: {status!r} not in {QI_STATUS}')
    return socket


def assert_honest(socket):
    """Reject a socket that claims more coverage than it stores.

    The specific lie this blocks: labelling a recovered 2018-2026 slice as
    '2010-2026 complete'. COMPLETE and VALIDATED_RANGE both require a real
    span, and a declared gap contradicts COMPLETE.
    """
    errors = []
    st = socket.get('status')
    if st not in QI_STATUS:
        errors.append(f'status {st!r} invalid')
    if st in ('VALIDATED_RANGE', 'COMPLETE'):
        if not socket.get('validated_ranges'):
            errors.append(f'{st} declared with no validated_ranges')
        for f in ('papers_total', 'questions_total', 'earliest_year', 'latest_year'):
            if socket.get(f) in (None, 0):
                errors.append(f'{st} declared but {f} is empty')
    if st == 'COMPLETE' and socket.get('known_gaps'):
        errors.append('COMPLETE declared while known_gaps are recorded')
    if st == 'NOT_STARTED':
        for f in ('papers_total', 'questions_total'):
            if socket.get(f):
                errors.append(f'NOT_STARTED but {f} is populated')
    dc = socket.get('date_certainty')
    if dc not in DATE_CERTAINTY:
        errors.append(f'date_certainty {dc!r} invalid')
    elif dc == 'NONE' and socket.get('papers_total'):
        errors.append('papers are held but date_certainty is still NONE -- '
                      'say who vouches for the sitting months')
    elif dc != 'NONE' and st == 'NOT_STARTED':
        errors.append(f'NOT_STARTED but date_certainty claims {dc}')
    e, l = socket.get('earliest_year'), socket.get('latest_year')
    if e and l and e > l:
        errors.append('earliest_year is after latest_year')
    return errors


def date_certainty_gate(historical):
    """May the historical layer licence a DATED public claim? -> (bool, why).

    This is the single chokepoint between "we hold the evidence" and "we may
    say so in public". It is deliberately not satisfiable by coverage: a layer
    can be COMPLETE and still be barred, because completeness says nothing
    about who dated the papers.
    """
    dc = historical.get('date_certainty', 'NONE')
    st = historical.get('status')
    if dc != PUBLIC_DATED_CLAIM_REQUIRES:
        return False, (
            f'date_certainty is {dc}; a public dated claim requires '
            f'{PUBLIC_DATED_CLAIM_REQUIRES}. Coverage does not substitute: '
            f'holding the papers is not the same as an official document '
            f'saying when they were set.')
    if st not in ('VALIDATED_RANGE', 'COMPLETE'):
        return False, f'coverage status is {st}'
    if not (historical.get('earliest_year') and historical.get('latest_year')):
        return False, 'no span is stored'
    return True, 'officially dated papers over a validated range'


def public_evidence_claim(current, historical):
    """The strongest sentence the STORED evidence supports. Never hand-written.

    While historical QI is unintegrated this can only describe the current
    governed corpus. Once a validated historical range exists AND those papers
    are officially dated, the same function strengthens the wording
    automatically -- and only then. Coverage alone never unlocks it.
    """
    base = (f"Based on MIW's currently mapped Oral corpus and "
            f"{current['questions_total']} solved Written questions across "
            f"{current['papers_total']} papers "
            f"({current['earliest_sitting']} to {current['latest_sitting']}).")
    allowed, _ = date_certainty_gate(historical)
    if allowed:
        return (f"{base} Recurrence intelligence additionally draws on "
                f"validated historical papers from "
                f"{historical['earliest_year']} to {historical['latest_year']}.")
    return base
