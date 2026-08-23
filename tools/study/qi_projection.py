#!/usr/bin/env python3
"""The ONE candidate-safe projection of question intelligence.

    study_qi.json  (+ the governed QI occurrence layer)
            |
            v   qi_projection.py          <- you are here
            |
    safe_qi_projection.json
            |
    year pages / solved paper pages / topic pages / roadmap / workbook


WHY A PROJECTION LAYER EXISTS AT ALL
------------------------------------
Before this module the backend knew a great deal that no candidate could see,
and the two page generators that DID show recurrence each decided for
themselves what to say. That is how a product ends up asserting different
things about the same question on two pages, and how an internal number
reaches a public one by accident.

So: generators render, they do not decide. Every candidate-facing question
intelligence string in the repository is chosen here, once, and written to a
generated artefact the generators read.


THE THREE LAYERS, AND WHY THEY MUST NOT BE MERGED
-------------------------------------------------
LAYER 1 -- MODERN QUESTION RECURRENCE.
    "Within the sittings MIW has transcribed, has this exact examiner task
    come back?"  Owned by ``tools/pastpapers/recurrence_model.py`` and derived
    from the CALENDAR. This module does not compute it, does not restate it
    and does not override it.

    In particular it is NOT ``study_qi.json``'s ``modern_recurrence_class``.
    That field is the AUTHORING vocabulary and recurrence_model.py records
    three questions in the 2026 set where the two say opposite things --
    QP2607-Q1 is stored ``new`` although the same task was set five months
    earlier, because July was built first. Sourcing a candidate-facing tag
    from it would state the reverse of the truth. The consequence is worth
    naming: because Layer 1 is untouched by this module, "no modern tag was
    lost" is true by construction, not by test.

LAYER 2 -- LONGITUDINAL FAMILY SIGNAL.
    "Over MIW's governed 2010->Aug-2026 question intelligence, how persistent
    is this concept?"  Qualitative only. No dates, no counts, no family ids.

LAYER 3 -- ANSWER READINESS.
    "Is MIW's current answer safe to study TODAY?"  Owned by the Phase-2
    present-day layer. It is not a recurrence statement and never modifies
    one.

A candidate may see all three. Each says only what its own evidence supports.


THE RULE THAT SHAPES LAYER 2: A LABEL MUST SURVIVE ITS OWN EVIDENCE
-------------------------------------------------------------------
The 2010-2020 evidence band is ``SECONDARY_CLAIMED``: MIW holds the questions
but no official document saying when they were set. ``qi_model`` bars a dated
public claim on that band, and the bar is on date certainty, never on
coverage.

A qualitative label can smuggle the same claim through. ``RE_EMERGING`` means
"absent a long time, then set again" -- it is a statement about WHEN, wearing
an adjective. QIF-EM-0220 is the worked case: 2010-04 (claimed) plus 2026-08
(printed) earns RECENTLY_ACTIVE and RE_EMERGING, and the entire support for
RE_EMERGING is the claimed date.

So every family is labelled TWICE by the same engine
(``qi_model.intelligence_labels``), over two populations:

    all governed occurrences        -> ``labels_all_evidence``   (INTERNAL)
    printed-on-source-copy only     -> ``labels_printed_only``   (candidate)

A label is candidate-safe only if it survives on printed evidence alone.
Anything MIW knows beyond that is not thrown away and not asserted either: the
family carries ``WIDER_RECURRENCE_HELD``, which says MIW's governed
intelligence reaches further back without saying how far or when.

That is a real product signal and an honest one. It is also the reason this
module re-runs the label engine instead of reading the stored labels: reading
them would publish the claimed-date shape.


AUDIENCES
---------
PUBLIC    the discovery surfaces. Longitudinal signal only, no readiness --
          answer readiness is a statement about the paid product's contents.
GATED     the paid candidate surfaces. Longitudinal signal, currentness
          warning and answer readiness, all qualitative.
INTERNAL  the workbook and governance. Exact counts, family ids, Phase-2
          action, both label sets, and the evidence basis for each.

There is no "render everything and hope the page filters it". A tier is a
field whitelist applied here, so a field added to the internal record is
absent from the others until someone deliberately adds it.
"""

import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import qi_model as M

ROOT = os.path.dirname(os.path.dirname(HERE))
DOC = os.path.join(ROOT, 'docs', 'study')
QI_DIR = os.path.join(DOC, 'qi')
STUDY_QI = os.path.join(DOC, 'study_qi.json')
OUT = os.path.join(DOC, 'safe_qi_projection.json')

SCHEMA = 'miw.study.safe_qi_projection.v1'
SCHEMA_VERSION = '1.0'

AUDIENCES = ('PUBLIC', 'GATED', 'INTERNAL')

#: The date-certainty classes a candidate-facing longitudinal label may rest
#: on. Deliberately a whitelist: a new band added to the QI layer is excluded
#: until someone argues it in.
CANDIDATE_SAFE_DATE_CERTAINTY = {'PRINTED_ON_SOURCE_COPY', 'OFFICIAL_DATED'}

#: Layer-2 label -> the exact string a candidate sees. Anything not in this
#: map renders nothing at all; silence is the safe default and an unmapped
#: label must never fall through to its raw governance token.
LONGITUDINAL_TEXT = {
    'PERSISTENT': 'Persistent topic',
    'RECENTLY_ACTIVE': 'Active in recent papers',
    'RE_EMERGING': 'Re-emerging topic',
    'RISING': 'Rising topic',
    'NEW_EMERGING': 'Newly recurring topic',
    'DORMANT': 'Not set in recent papers',
}

#: Labels that are governance-only. HISTORICAL_ONLY names the secondary band
#: in all but name; INSUFFICIENT_HISTORY is an absence, and rendering an
#: absence as a badge tells a candidate something MIW did not measure.
LONGITUDINAL_INTERNAL_ONLY = {'HISTORICAL_ONLY', 'INSUFFICIENT_HISTORY'}

#: The honest statement for a family whose extra reach is secondary-claimed.
#: It asserts that MIW holds more, and nothing about when.
WIDER_RECURRENCE = 'WIDER_RECURRENCE_HELD'
WIDER_RECURRENCE_TEXT = 'Recurs beyond MIW&rsquo;s solved set'

#: Why a question carries no Layer-2 signal. Reported internally so the gap is
#: visible; never rendered.
NO_LONGITUDINAL_REASONS = {
    'LONGITUDINAL_FAMILY_NOT_YET_GOVERNED':
        'No canonical family reaches this question. Its modern recurrence tag '
        'stands alone. Not a defect and not a licence to invent a family.',
    'NO_CANDIDATE_SAFE_LABEL':
        'The family is governed but every label it earns is internal-only or '
        'rests on secondary-claimed dates, and it holds no wider reach to '
        'report either.',
}

#: Answer readiness -> the exact string a candidate sees.
#: NEW_ANSWER_REQUIRED and MODERNISE_REQUIRED share wording on purpose: the
#: difference between them is a production fact about MIW, not a fact the
#: candidate can act on. Both mean "do not treat what is here as current".
READINESS_TEXT = {
    'VERIFY_CURRENT_ANSWER': 'Currentness check pending',
    'NEW_ANSWER_REQUIRED': 'Current-framework answer in preparation',
    'MODERNISE_REQUIRED': 'Current-framework answer in preparation',
    'CURRENTNESS_HOLD': 'Answer under currentness review',
}
READINESS_INTERNAL_ONLY = {'HISTORICAL_ONLY'}

#: READY_TO_STUDY_NOW is TWO different statements and they must not share a
#: sentence.
#:
#: 82 families are ready. TEN of them carry a Phase-2 governed record: current
#: primary authority read and dated, an independent reviewer who passed it, and
#: a named canonical answer. The other seventy-odd are ready because Phase-1
#: TRIAGE fired no currentness risk against them -- which is the absence of a
#: signal, not the presence of a check. ``qi_model`` already says it in terms:
#: UNKNOWN is not CURRENT, it means nobody looked.
#:
#: Printing "Current answer verified" over all 82 would take a genuine, expensive
#: verification claim and spend it on questions nobody has verified. That is the
#: precise failure the Phase-2 contract exists to prevent -- it does not look
#: like a bug, it looks like a confident, current, wrong answer. So the basis
#: chooses the wording, and only a governed review earns the word "verified".
READINESS_BASIS = {
    'PHASE2_GOVERNED_REVIEW':
        'A Phase-2 record names THIS question as the canonical current answer, '
        'carries dated current primary authority and passed independent review.',
    'TRIAGE_NO_RISK_SIGNAL':
        'Phase-1 triage fired no currentness risk. Nobody has verified the '
        'answer against present-day authority.',
}
READY_TEXT_BY_BASIS = {
    'PHASE2_GOVERNED_REVIEW': 'Current answer verified',
    'TRIAGE_NO_RISK_SIGNAL': 'No currentness risk flagged',
}

#: Currentness -> the warning a candidate sees. CURRENT and UNKNOWN render
#: nothing: UNKNOWN means nobody checked, and a badge saying so would read as
#: a finding.
CURRENTNESS_TEXT = {
    'CURRENT_WITH_AMENDMENT': 'Framework since amended',
    'CURRENT_FRAMEWORK_CHANGED': 'Framework has since moved',
    'LIKELY_SUPERSEDED': 'Framework since superseded',
    'CURRENTNESS_REVIEW_REQUIRED': 'Currentness review required',
    'HISTORICAL_ONLY': 'Historical framework',
}

#: Currentness classes under which "Current answer verified" may never render,
#: whatever readiness says. Mirrors study_qi_adapter.UNSAFE_CURRENTNESS; the
#: validator proves the two agree rather than trusting the copy.
UNSAFE_CURRENTNESS = {
    'CURRENT_FRAMEWORK_CHANGED', 'LIKELY_SUPERSEDED',
    'CURRENTNESS_REVIEW_REQUIRED', 'HISTORICAL_ONLY',
}

#: Field whitelists. A tier shows exactly these keys and no others.
QUESTION_FIELDS = {
    'PUBLIC': ('question_id', 'longitudinal_signal', 'longitudinal_text'),
    'GATED': ('question_id', 'longitudinal_signal', 'longitudinal_text',
              'currentness_signal', 'currentness_text',
              'readiness_signal', 'readiness_text', 'readiness_basis',
              'successor_question_id'),
    'INTERNAL': None,   # everything
}

TOPIC_FIELDS = {
    'PUBLIC': ('topic_id', 'ready_now', 'total_families'),
    'GATED': ('topic_id', 'ready_now', 'under_review', 'in_preparation',
              'total_families', 'phase2_verified_answers', 'readiness_text'),
    'INTERNAL': None,
}


def _load(path):
    return json.load(open(path, encoding='utf-8'))


# --------------------------------------------------------------------------
# EVIDENCE PARTITION
# --------------------------------------------------------------------------

def family_evidence(families_doc, occurrences_doc):
    """Per family: all recurrence-bearing sittings, and the printed subset.

    Keyed by occurrence, not by sitting, because the label engine counts
    occurrences in the recent windows and distinct sittings for span.
    """
    by_occ = {o['occurrence_id']: o for o in occurrences_doc['occurrences']}
    out = {}
    for f in families_doc['families']:
        all_s, printed_s = [], []
        for oid in f['occurrence_ids']:
            o = by_occ.get(oid)
            if not o or not o.get('counts_toward_recurrence'):
                continue
            all_s.append(o['sitting'])
            if o.get('date_certainty') in CANDIDATE_SAFE_DATE_CERTAINTY:
                printed_s.append(o['sitting'])
        out[f['family_id']] = {
            'all_sittings': sorted(all_s),
            'printed_sittings': sorted(printed_s),
            'secondary_occurrences': len(all_s) - len(printed_s),
        }
    return out


def family_labels(evidence):
    """Both label sets, from the ONE engine, over two populations."""
    all_l = M.intelligence_labels(evidence['all_sittings']) if evidence['all_sittings'] else []
    printed_l = (M.intelligence_labels(evidence['printed_sittings'])
                 if evidence['printed_sittings'] else [])
    safe = [l for l in printed_l if l in LONGITUDINAL_TEXT]
    # MIW knows more than it may assert. Say that it knows more; say nothing
    # about when. A label that is internal-only over ALL evidence is not a
    # reach worth reporting either -- INSUFFICIENT_HISTORY over everything
    # means there is no wider recurrence to hold.
    wider = bool(set(all_l) - set(printed_l)
                 and evidence['secondary_occurrences'] > 0
                 and set(all_l) - {'INSUFFICIENT_HISTORY'})
    if wider:
        safe = safe + [WIDER_RECURRENCE]
    return {
        'labels_all_evidence': all_l,
        'labels_printed_only': printed_l,
        'candidate_labels': sorted(set(safe)),
        'secondary_occurrences': evidence['secondary_occurrences'],
        'evidence_basis': ('GOVERNED_PRINTED_ONLY' if not evidence['secondary_occurrences']
                           else 'INCLUDES_SECONDARY_CLAIMED'),
    }


# --------------------------------------------------------------------------
# QUESTION PROJECTION
# --------------------------------------------------------------------------

def _first(states, order):
    """The most cautious state present. Order is worst-first."""
    for s in order:
        if s in states:
            return s
    return None


CURRENTNESS_ORDER = ('LIKELY_SUPERSEDED', 'HISTORICAL_ONLY',
                     'CURRENTNESS_REVIEW_REQUIRED', 'CURRENT_FRAMEWORK_CHANGED',
                     'CURRENT_WITH_AMENDMENT', 'UNKNOWN', 'CURRENT')

READINESS_ORDER = ('CURRENTNESS_HOLD', 'NEW_ANSWER_REQUIRED',
                   'MODERNISE_REQUIRED', 'VERIFY_CURRENT_ANSWER',
                   'HISTORICAL_ONLY', 'READY_TO_STUDY_NOW')


def _named_answer(p2):
    """The ONE question a Phase-2 record names as its canonical current answer.

    The field is a dict in the governed store and the older prose writes it as
    a bare id, so both shapes are read. A record that names nothing returns
    None and can therefore never grant readiness to anything.
    """
    v = p2.get('canonical_current_answer')
    if isinstance(v, dict):
        return v.get('question_id')
    return v


def project_question(q, lab_by_fid, phase2_by_fid):
    """One candidate-safe record for one question.

    Worst-case aggregation throughout. A question reached by two families
    takes the more cautious reading of each axis, because the alternative is a
    page that reassures on the strength of the safer half.
    """
    fids = q.get('canonical_family_ids') or []
    labs = [lab_by_fid[f] for f in fids if f in lab_by_fid]
    cand = sorted({l for x in labs for l in x['candidate_labels']})

    reason = None
    if not fids:
        reason = 'LONGITUDINAL_FAMILY_NOT_YET_GOVERNED'
    elif not cand:
        reason = 'NO_CANDIDATE_SAFE_LABEL'

    curr = _first(set(q.get('currentness_status') or ()), CURRENTNESS_ORDER)
    ready = _first(set(q.get('readiness') or ()), READINESS_ORDER)

    # A successor is shown only where a governed record NAMES one and it is a
    # different question. Never inferred from family membership.
    successor = None
    phase2_names_this = False
    for f in fids:
        p2 = phase2_by_fid.get(f) or {}
        nid = _named_answer(p2)
        if nid == q['question_id']:
            phase2_names_this = True
        if p2.get('final_state') == 'SUPERSEDED_WITH_SUCCESSOR' and nid                 and nid != q['question_id']:
            successor = nid

    # PHASE-1 TRIAGE IS AN INPUT, NOT A VETO OVER PHASE 2.
    #
    # A question can legitimately read READY_TO_STUDY_NOW while its family's
    # currentness triage still says CURRENTNESS_REVIEW_REQUIRED, and three of
    # the ten tranche-001 answers do exactly that. The triage value in
    # qi_currentness.json is DELIBERATELY never rewritten -- Phase 1 is an
    # input here -- so it still records the risk that prompted the Phase-2
    # work, not the finding that closed it.
    #
    # An unconditional "unsafe currentness beats ready" rule therefore reverts
    # every grant Phase 2 earned, which is worse than the staleness it guards
    # against: it hides finished verification behind a stale warning. The
    # exemption is narrow and it is the same one R-READY-SAFE honours -- a
    # governed record that NAMES THIS QUESTION as the canonical current answer.
    # For every other question, including the other members of a resolved
    # family, the guard bites as written.
    if ready == 'READY_TO_STUDY_NOW' and curr in UNSAFE_CURRENTNESS             and not phase2_names_this:
        ready = 'CURRENTNESS_HOLD'

    # ...and for the same reason the stale triage warning is suppressed on the
    # named answer only. Printing "Currentness review required" beside
    # "Current answer verified" would put the page in contradiction with
    # itself on the one question where MIW actually did the work.
    if phase2_names_this:
        curr = None

    # Section 22, at the point of rendering. A family being sorted out is not
    # the same as every sitting inside it being safe, and "verified" is a claim
    # about THIS answer.
    basis = None
    ready_text = READINESS_TEXT.get(ready)
    if ready == 'READY_TO_STUDY_NOW':
        basis = ('PHASE2_GOVERNED_REVIEW' if phase2_names_this
                 else 'TRIAGE_NO_RISK_SIGNAL')
        ready_text = READY_TEXT_BY_BASIS[basis]

    return {
        'question_id': q['question_id'],
        'topic_id': q.get('topic_id'),
        # ---- LAYER 2, candidate-facing -----------------------------------
        'longitudinal_signal': cand,
        'longitudinal_text': [LONGITUDINAL_TEXT.get(l, WIDER_RECURRENCE_TEXT)
                              for l in cand],
        'no_longitudinal_reason': reason,
        # ---- LAYER 3, candidate-facing -----------------------------------
        'currentness_signal': curr if curr in CURRENTNESS_TEXT else None,
        'currentness_text': CURRENTNESS_TEXT.get(curr),
        'readiness_signal': ready if ready_text else None,
        'readiness_text': ready_text,
        'readiness_basis': basis,
        'successor_question_id': successor,
        # ---- INTERNAL ONLY -------------------------------------------------
        'canonical_family_ids': fids,
        'count_3y': q.get('count_3y', 0),
        'count_5y': q.get('count_5y', 0),
        'count_10y': q.get('count_10y', 0),
        'count_full_horizon': q.get('count_full_horizon', 0),
        'labels_all_evidence': sorted({l for x in labs
                                       for l in x['labels_all_evidence']}),
        'labels_printed_only': sorted({l for x in labs
                                       for l in x['labels_printed_only']}),
        'evidence_basis': ('INCLUDES_SECONDARY_CLAIMED'
                           if any(x['evidence_basis'] == 'INCLUDES_SECONDARY_CLAIMED'
                                  for x in labs)
                           else 'GOVERNED_PRINTED_ONLY' if labs else None),
        'raw_currentness': sorted(q.get('currentness_status') or ()),
        'raw_readiness': sorted(q.get('readiness') or ()),
        'phase2_action': sorted(q.get('phase2_action') or ()),
        'is_historical_variant': q.get('is_historical_variant', False),
        'bears_family_weight_for': q.get('bears_family_weight_for') or [],
    }


def project_topic(tid, trow, q_rows):
    """Topic readiness, from the adapter's own topic projection.

    The counts are the adapter's; this adds only the candidate wording. A
    topic page that recomputed readiness from its questions would be a second
    readiness model and would drift the first time a family was resolved.
    """
    ready = trow.get('ready_to_study_now', 0)
    verify = trow.get('verify_current_answer', 0)
    prep = trow.get('new_answer_required', 0) + trow.get('modernise_required', 0)
    hold = trow.get('currentness_hold', 0)
    hist = trow.get('historical_only', 0)
    total = trow.get('mapped_families', 0)

    # Governed verification is counted separately from triage clearance, for
    # the reason set out at READINESS_BASIS: "ready" and "verified" are two
    # different claims and a topic summary is exactly where they would silently
    # merge into the stronger one.
    verified = sum(1 for r in q_rows
                   if r['topic_id'] == tid
                   and r.get('readiness_basis') == 'PHASE2_GOVERNED_REVIEW')

    # One short sentence a candidate can act on. Section 17: a high-recurrence
    # topic whose answers are under review must not read as safe as one whose
    # answers are ready.
    if not total:
        text = 'No longitudinal families mapped yet'
    elif ready == total:
        text = 'Every mapped family is ready to study'
    elif ready:
        text = '%d of %d mapped families are ready to study' % (ready, total)
    else:
        text = 'No mapped family is ready to study yet'
    if verified:
        text += '; %d %s independently verified against current authority' % (
            verified, 'answer' if verified == 1 else 'answers')

    return {
        'topic_id': tid,
        'total_families': total,
        'ready_now': ready,
        'phase2_verified_answers': verified,
        'under_review': verify + hold,
        'in_preparation': prep,
        'historical_only': hist,
        'currentness_hold': hold,
        'verify_current_answer': verify,
        'new_answer_required': trow.get('new_answer_required', 0),
        'modernise_required': trow.get('modernise_required', 0),
        'readiness_pct': trow.get('readiness_pct', 0.0),
        'readiness_text': text,
    }


# --------------------------------------------------------------------------
# BUILD
# --------------------------------------------------------------------------

def build():
    sq = _load(STUDY_QI)
    fams = _load(os.path.join(QI_DIR, 'qi_families.json'))
    occs = _load(os.path.join(QI_DIR, 'qi_occurrences.json'))

    ev = family_evidence(fams, occs)
    lab_by_fid = {fid: family_labels(e) for fid, e in ev.items()}

    p2doc = _load(os.path.join(HERE, 'qi_phase2_adjudications.json'))
    phase2_by_fid = {r['family_id']: r for r in p2doc['families']}

    q_rows = [project_question(q, lab_by_fid, phase2_by_fid) for q in sq['questions']]
    t_rows = {tid: project_topic(tid, tr, q_rows) for tid, tr in sorted(sq['topics'].items())}

    fam_rows = {}
    for fid in sorted(lab_by_fid):
        l = lab_by_fid[fid]
        fam_rows[fid] = {
            'family_id': fid,
            'candidate_labels': l['candidate_labels'],
            'labels_all_evidence': l['labels_all_evidence'],
            'labels_printed_only': l['labels_printed_only'],
            'evidence_basis': l['evidence_basis'],
            'secondary_occurrences': l['secondary_occurrences'],
        }

    counted = [r for r in q_rows if r['longitudinal_signal']]
    return {
        'schema': SCHEMA,
        'schema_version': SCHEMA_VERSION,
        'generated_by': 'tools/study/build_qi_projection.py',
        'hand_editable': False,
        'what_this_is': (
            'The one candidate-safe projection of MIW question intelligence. '
            'Layer 2 (longitudinal family signal) and Layer 3 (present-day '
            'answer readiness), in the exact words a candidate sees.'),
        'what_this_is_not': (
            'Layer 1. The modern repeat tag is computed from the calendar by '
            'tools/pastpapers/recurrence_model.py and is neither restated nor '
            'overridden here. Nothing in this file can remove a modern tag.'),
        'inputs': {
            'study_qi': sq['schema'],
            'qi_families': fams['schema'],
            'qi_occurrences': occs['schema'],
            'phase2_store': p2doc['schema'],
        },
        'label_engine': 'qi_model.intelligence_labels',
        'candidate_safe_date_certainty': sorted(CANDIDATE_SAFE_DATE_CERTAINTY),
        'secondary_claim_rule': (
            'A longitudinal label reaches a candidate only if it survives on '
            'PRINTED_ON_SOURCE_COPY evidence alone. Reach beyond that is '
            'reported as WIDER_RECURRENCE_HELD, which asserts that MIW holds '
            'more and nothing about when.'),
        'audiences': list(AUDIENCES),
        'vocabulary': {
            'longitudinal_text': LONGITUDINAL_TEXT,
            'longitudinal_internal_only': sorted(LONGITUDINAL_INTERNAL_ONLY),
            'wider_recurrence_text': WIDER_RECURRENCE_TEXT,
            'readiness_text': READINESS_TEXT,
            'readiness_basis': READINESS_BASIS,
            'ready_text_by_basis': READY_TEXT_BY_BASIS,
            'currentness_text': CURRENTNESS_TEXT,
            'unsafe_currentness': sorted(UNSAFE_CURRENTNESS),
            'no_longitudinal_reasons': NO_LONGITUDINAL_REASONS,
        },
        'question_fields': {k: (list(v) if v else 'ALL')
                            for k, v in QUESTION_FIELDS.items()},
        'topic_fields': {k: (list(v) if v else 'ALL')
                         for k, v in TOPIC_FIELDS.items()},
        'totals': {
            'questions': len(q_rows),
            'with_longitudinal_signal': len(counted),
            'without_family': sum(
                1 for r in q_rows
                if r['no_longitudinal_reason'] == 'LONGITUDINAL_FAMILY_NOT_YET_GOVERNED'),
            'family_but_no_safe_label': sum(
                1 for r in q_rows
                if r['no_longitudinal_reason'] == 'NO_CANDIDATE_SAFE_LABEL'),
            'with_readiness_signal': sum(1 for r in q_rows if r['readiness_signal']),
            'ready_phase2_verified': sum(
                1 for r in q_rows if r['readiness_basis'] == 'PHASE2_GOVERNED_REVIEW'),
            'ready_triage_only': sum(
                1 for r in q_rows if r['readiness_basis'] == 'TRIAGE_NO_RISK_SIGNAL'),
            'with_currentness_warning': sum(1 for r in q_rows if r['currentness_signal']),
            'families': len(fam_rows),
            'families_labelled_from_printed_only': sum(
                1 for f in fam_rows.values()
                if f['evidence_basis'] == 'GOVERNED_PRINTED_ONLY'),
            'families_downgraded_to_wider_recurrence': sum(
                1 for f in fam_rows.values()
                if WIDER_RECURRENCE in f['candidate_labels']),
        },
        'topics': t_rows,
        'families': fam_rows,
        'questions': q_rows,
    }


# --------------------------------------------------------------------------
# CONSUMER API -- the only way a generator may read this
# --------------------------------------------------------------------------

_CACHE = {}


def load(path=None):
    p = path or OUT
    if p not in _CACHE:
        _CACHE[p] = _load(p)
    return _CACHE[p]


def question(qid, audience='GATED', doc=None):
    """The tier-filtered record for one question, or None.

    Returning None for an unknown question is deliberate: a generator that
    renders whatever it is handed must render nothing at all for a question
    this layer has never seen, rather than an empty badge.
    """
    doc = doc or load()
    by_id = doc.setdefault('_by_id', {r['question_id']: r for r in doc['questions']})
    row = by_id.get(qid)
    if row is None:
        return None
    return _tier(row, QUESTION_FIELDS[audience])


def topic(tid, audience='GATED', doc=None):
    doc = doc or load()
    row = doc['topics'].get(tid)
    if row is None:
        return None
    return _tier(row, TOPIC_FIELDS[audience])


def _tier(row, fields):
    if fields is None:
        return dict(row)
    return {k: row[k] for k in fields if k in row}


def write(path, obj):
    text = json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=False) + '\n'
    prev = open(path, encoding='utf-8', newline='').read() if os.path.exists(path) else None
    with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    return 'IDENTICAL' if prev == text else ('CHANGED' if prev is not None else 'NEW')


# --------------------------------------------------------------------------
# RENDERING -- one block, every candidate surface
# --------------------------------------------------------------------------

#: Class hints so a surface can style the three kinds differently without
#: parsing the strings back apart.
_KIND_CLASS = {'longitudinal': '', 'currentness': ' warn', 'readiness': ' ready',
               'successor': ' warn'}


def tags_for(qid, audience='GATED', doc=None):
    """The ordered (kind, text) pairs a surface should show for one question.

    Ordered worst-news-last is deliberate. A candidate scanning a page reads
    the last chip on the line, so the readiness state -- the only one of the
    three that changes what they should DO today -- goes at the end.

    Returns [] where the projection knows nothing. A surface must render
    nothing at all in that case: an empty badge row reads as "checked, found
    nothing", and for an ungoverned family the truth is "not looked at yet".
    """
    row = question(qid, audience=audience, doc=doc)
    if not row:
        return []
    out = [('longitudinal', t) for t in row.get('longitudinal_text') or ()]
    # CURRENTNESS_REVIEW_REQUIRED and a readiness of "check pending" / "under
    # review" are the same fact reported twice. Two chips saying it does not
    # make it twice as true; it makes the row look like two findings.
    curr = row.get('currentness_signal')
    ready = row.get('readiness_signal')
    redundant = (curr == 'CURRENTNESS_REVIEW_REQUIRED'
                 and ready in ('VERIFY_CURRENT_ANSWER', 'CURRENTNESS_HOLD'))
    if row.get('currentness_text') and not redundant:
        out.append(('currentness', row['currentness_text']))
    if row.get('readiness_text'):
        out.append(('readiness', row['readiness_text']))
    # Section 23. Named by a governed record, never inferred, and rendered as
    # a statement rather than a link: the successor may sit on a paper this
    # surface does not carry, and a dead link is worse than a sentence.
    if row.get('successor_question_id'):
        out.append(('successor',
                    'Current framework: see %s' % row['successor_question_id']))
    return out


def render_block(qid, audience='GATED', doc=None, label='Longer-term signal'):
    """The shared HTML for Layer 2 + Layer 3. Used by EVERY candidate surface.

    It lives here rather than in either page generator because the year sheet
    and the solved paper page must say the same thing about the same question.
    Two copies of this markup would drift, and the first symptom would be a
    customer seeing one claim on the year sheet and another on the paper.

    The strings are already HTML (they carry entities such as &rsquo;), so they
    are emitted as-is: they come from a closed vocabulary in this module, never
    from corpus text.
    """
    tags = tags_for(qid, audience=audience, doc=doc)
    if not tags:
        return ''
    parts = ['<div class="qy-long"><span class="qy-long-k">%s</span>' % label]
    for kind, text in tags:
        parts.append('<span class="q-tag%s">%s</span>' % (_KIND_CLASS[kind], text))
    parts.append('</div>')
    return ''.join(parts)
