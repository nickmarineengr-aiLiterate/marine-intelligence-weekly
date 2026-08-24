#!/usr/bin/env python3
"""The Phase-2 gate. Fails closed.

Phase 1 answers "what keeps coming back". Phase 2 answers "what is true now,
and may a candidate study this today". The second question is the dangerous
one, because getting it wrong does not look like a bug -- it looks like a
confident, current, wrong answer.

So every route to READY runs through here.

What this gate is really defending
----------------------------------
Three things, in order of how badly they would hurt:

1.  A family reading READY because somebody wrote READY. Readiness is not a
    field an author sets; it is a CONSEQUENCE of having done the work. This
    gate re-derives it from the evidence and refuses any state the evidence
    does not support (R-P2-EARNED, R-P2-AUTHORITY, R-P2-REVIEW, R-P2-ANSWER).

2.  Phase 2 quietly editing Phase 1. Recurrence is an INPUT here. The tranche
    manifest pins every count it selected on, and this gate compares the pins
    with the live layer, so any drift underneath the work is caught rather
    than inherited (R-P2-PIN-*).

3.  Phase 2 destroying modern question intelligence while "improving" a
    family. The modern repeat metadata is pinned the same way (R-P2-MODERN).

Run:
    python tools/study/validate_phase2_tranche.py
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import study_qi_adapter as A

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'current_answers'))
import ca_model as CA

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(REPO, 'docs', 'study')
QI_DIR = os.path.join(DOC, 'qi')
STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     'qi_phase2_adjudications.json')
SPEC_DIR = os.path.join(REPO, 'meoclass1', 'pastpapers', 'specs')

#: Authority classes that can satisfy the primary-authority gate. Every one of
#: them is a source somebody can go and read. "A model recalled it" is not on
#: the list and never will be.
ACCEPTED_AUTHORITY = {
    'PRIMARY_IMO', 'PRIMARY_TREATY', 'PRIMARY_INDIAN_STATUTE',
    'PRIMARY_INDIAN_SUBORDINATE', 'COMPETENT_AUTHORITY_RESTATEMENT',
    'CLASSIFICATION_SOCIETY_SUMMARY', 'ENGINEERING_JUDGEMENT',
}

PASSING_REVIEW = {'PASS', 'PASS_WITH_MINOR_FIX'}

#: States that mean "a candidate may study this now".
SAFE = A.PHASE2_SAFE_STATES
BLOCKED = A.PHASE2_BLOCKED_STATES
ALL_FINAL = SAFE | BLOCKED | {'HISTORICAL_ONLY'}

#: Historical-count claims that must never reach a public surface. Phase 2
#: touching a family is not a reason for the public page to start quoting a
#: 2010-based number.
FORBIDDEN_PUBLIC = ('since 2010', 'asked 1', 'official since')

RESULTS = []


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def check(rule, ok, detail=''):
    RESULTS.append((rule, bool(ok), detail))


def spec_question_ids():
    """Every canonical Written question id that actually exists on disk."""
    ids = set()
    for name in sorted(os.listdir(SPEC_DIR)):
        if not name.endswith('.json'):
            continue
        for q in load(os.path.join(SPEC_DIR, name)).get('questions', []):
            if q.get('question_id'):
                ids.add(q['question_id'])
    return ids


def load_bundle():
    """Everything the gate reads, in one dict.

    Separated from the checks so the mutation suite can corrupt a COPY of this
    bundle in memory and prove each rule bites, without writing to disk.
    """
    store = load(STORE)
    return {
        'store': store,
        'fams': store['families'],
        'questions': {q['question_id']: q
                      for q in load(os.path.join(DOC, 'study_qi.json'))['questions']},
        'projected': {r['family_id']: r
                      for r in load(os.path.join(DOC, 'study_qi.json'))['families']},
        'queue': {r['family_id']: r for r in
                  load(os.path.join(QI_DIR, 'qi_phase2_action_queue.json'))['queue']},
        'qi_fams': load(os.path.join(QI_DIR, 'qi_families.json')),
        'qi_occ': load(os.path.join(QI_DIR, 'qi_occurrences.json'))['counts'],
        'metrics': {m['family_id']: m for m in
                    load(os.path.join(QI_DIR,
                                      'qi_time_window_metrics.json'))['families']},
        'holds': load(os.path.join(os.path.dirname(STORE), 'study_qi_holds.json')),
        'real_qids': spec_question_ids(),
        # The other set of nameable answers. Until this existed,
        # `spec_question_ids()` WAS the set of things a present-day answer could
        # be, which is why tranche 002 held six families it had fully researched:
        # the only container available was a past paper, and putting a 2026
        # answer inside a 2021 paper would have made that paper cite law that did
        # not govern it.
        'lib_entries': CA.load_entries(),
        'public_html': read_public(),
    }


def read_public():
    public = os.path.join(REPO, 'SQ', 'study-roadmap.html')
    if not os.path.exists(public):
        return None
    with open(public, encoding='utf-8') as f:
        return f.read().lower()


def run_checks(B):
    store = B['store']
    fams = B['fams']
    by_id = {r['family_id']: r for r in fams}
    projected = B['projected']
    queue = B['queue']
    qi_fams = B['qi_fams']
    qi_occ = B['qi_occ']
    metrics = B['metrics']
    holds = B['holds']
    real_qids = B['real_qids']
    lib_entries = B.get('lib_entries') or {}
    questions = B.get('questions') or {}

    # ------------------------------------------------------------------ A
    # The tranche is a closed set. Every family it claims must be present,
    # exactly once, and the manifest must not have quietly lost one.
    for tid, tr in store['tranches'].items():
        declared = tr['family_ids']
        present = [f for f in declared if f in by_id]
        check('R-P2-TRANCHE-COMPLETE', len(present) == len(declared),
              '%s: manifest declares %d families but %d have records: missing %s'
              % (tid, len(declared), len(present),
                 sorted(set(declared) - set(by_id))))
        check('R-P2-TRANCHE-CLOSED',
              sorted(declared) == sorted(r['family_id'] for r in fams
                                         if r.get('tranche_id') == tid),
              '%s: a family record claims this tranche but the manifest does '
              'not list it, or vice versa' % tid)
        check('R-P2-TRANCHE-UNIQUE', len(set(declared)) == len(declared),
              '%s: a family is declared twice' % tid)
        check('R-P2-TRANCHE-REAL',
              all(f in queue for f in declared),
              '%s: declares a family that does not exist in the QI queue: %s'
              % (tid, sorted(set(declared) - set(queue))))

        # A tranche may declare that it deliberately weighted itself toward
        # new-answer families, and if it does, the weighting is checked. This
        # exists because the cheap way to make a tranche look productive is to
        # fill it with EXISTING_CURRENT_ANSWER_VERIFY families, which convert
        # readily, and quietly drop the NEW_MODERN_ANSWER_REQUIRED ones, which
        # are where the product is actually missing. The declaration is
        # honoured against the ACTION PINNED AT SELECTION, so a family cannot
        # be counted toward the bias by being reclassified afterwards.
        bias = tr.get('new_answer_bias')
        if bias:
            want = min(bias.get('minimum', 0),
                       bias.get('qualifying_pool_at_selection', 0))
            got = sum(1 for f in declared
                      if ((by_id.get(f) or {}).get('pinned_at_selection') or {})
                      .get('phase2_action') == 'NEW_MODERN_ANSWER_REQUIRED')
            check('R-P2-NEW-ANSWER-BIAS', got >= want,
                  '%s declares a minimum of %d new-answer families and the '
                  'queue offered %d, but only %d were selected. A tranche may '
                  'not quietly retreat to the families that convert easily.'
                  % (tid, bias.get('minimum', 0),
                     bias.get('qualifying_pool_at_selection', 0), got))

    # ------------------------------------------------------------------ B
    # Every family finishes in exactly one governed final state. There is no
    # generic REVIEWED, and there is no blank.
    bad_state = [r['family_id'] for r in fams if r.get('final_state') not in ALL_FINAL]
    check('R-P2-FINAL-STATE', not bad_state,
          'family(ies) with a missing or unrecognised final_state: %s' % bad_state)

    # A hold is FINISHED WORK, not backlog -- the same rule the mapping review
    # queue runs on. What makes it finished is that somebody wrote down what
    # stopped it. A blocked state with no stated reason is indistinguishable
    # from a family nobody got to, and the next tranche cannot tell whether it
    # is looking at a decision or at a gap in the record.
    no_reason = [r['family_id'] for r in fams
                 if r['final_state'] in BLOCKED and not r.get('hold_reason')]
    check('R-P2-HOLD-REASON', not no_reason,
          'held family(ies) carrying no hold_reason. A hold without a reason '
          'is backlog wearing a hold\'s clothes: %s' % no_reason)

    # ------------------------------------------------------------------ C/D/E
    # A safe state must be EARNED. Three independent legs, checked separately
    # so a failure names which leg gave way.
    no_auth, bad_auth, no_date, no_review, bad_review, no_answer, ghost_answer = \
        [], [], [], [], [], [], []
    for r in fams:
        if r['final_state'] not in SAFE:
            continue
        fid = r['family_id']
        auth = r.get('primary_authority') or []
        if not auth:
            no_auth.append(fid)
        elif not any(a.get('class') in ACCEPTED_AUTHORITY for a in auth):
            bad_auth.append(fid)
        if not r.get('authority_currentness_date'):
            no_date.append(fid)
        rev = r.get('independent_review') or {}
        if not rev.get('reviewer') or not rev.get('verdict'):
            no_review.append(fid)
        elif rev['verdict'] not in PASSING_REVIEW:
            bad_review.append(fid)
        # OWNERSHIP, TYPED. A resolved family must name something a candidate
        # can be sent to. Since the current-answer library exists there are two
        # kinds of thing and two shapes of ownership, and BOTH have to be read
        # here -- reading only `canonical_current_answer` would report every
        # multi-limb family as answering nothing, which is the same failure as
        # naming an answer that does not exist, arriving from the other side.
        owners = CA.owner_ids(r)
        if not owners:
            no_answer.append(fid)
        for otype, oid in owners:
            if otype in CA.LIBRARY_OWNER_TYPES:
                if oid not in lib_entries:
                    ghost_answer.append('%s -> %s (library entry absent)'
                                        % (fid, oid))
                elif lib_entries[oid].get('review_status') not in CA.RENDERABLE:
                    ghost_answer.append('%s -> %s (library entry not verified, '
                                        'so it has no page)' % (fid, oid))
            elif oid not in real_qids:
                ghost_answer.append('%s -> %s' % (fid, oid))

    check('R-P2-AUTHORITY', not no_auth,
          'verified family(ies) carrying NO primary authority: %s' % no_auth)
    check('R-P2-AUTHORITY-CLASS', not bad_auth,
          'verified family(ies) whose authority is of no accepted class: %s' % bad_auth)
    check('R-P2-AUTHORITY-DATE', not no_date,
          'verified family(ies) with no authority_currentness_date -- an '
          'undated currency check is not a currency check: %s' % no_date)
    check('R-P2-REVIEW', not no_review,
          'verified family(ies) with no independent review: %s' % no_review)
    check('R-P2-REVIEW-PASS', not bad_review,
          'verified family(ies) whose review did NOT pass: %s' % bad_review)
    check('R-P2-ANSWER', not no_answer,
          'verified family(ies) naming no canonical current answer: %s' % no_answer)
    check('R-P2-ANSWER-REAL', not ghost_answer,
          'verified family(ies) pointing at an answer that does not exist: %s'
          % ghost_answer)

    # ------------------------------------------------------- typed ownership
    # A library owner MUST be written in the typed form. Section 17: prefer
    # typed ownership, do not overload string interpretation.
    #
    # This is not tidiness. `resolve_owner` maps the legacy untyped shape to
    # SOLVED_PAPER, because when that shape was written a solved past-paper
    # question was the only nameable answer in existence. If a library id were
    # allowed to arrive in that shape it would be resolved as a past-paper
    # question, fail to appear in the spec set, and surface as "points at a
    # question that does not exist" -- a confusing failure a long way from its
    # cause. Refuse it at the shape instead.
    untyped, cross_shaped = [], []
    for r in fams:
        for obj in ([r.get('canonical_current_answer')]
                    + list(r.get('family_current_answers') or [])):
            if not isinstance(obj, dict):
                continue
            otype, oid = CA.resolve_owner(obj)
            if CA.is_ca_id(oid) and not obj.get('owner_type'):
                untyped.append('%s -> %s' % (r['family_id'], oid))
            if otype in CA.LIBRARY_OWNER_TYPES and CA.is_qp_id(oid):
                cross_shaped.append('%s: %s names %s' % (r['family_id'], otype, oid))
            if otype in CA.PAPER_OWNER_TYPES and CA.is_ca_id(oid):
                cross_shaped.append('%s: %s names %s' % (r['family_id'], otype, oid))
    check('R-P2-OWNER-TYPED', not untyped,
          'family(ies) naming a current-answer library entry without an '
          'explicit owner_type: %s' % untyped)
    check('R-P2-OWNER-SHAPE', not cross_shaped,
          'family(ies) whose owner_type and owner_id disagree about what kind '
          'of answer is being named: %s' % cross_shaped)

    # A family is owned WHOLE or LIMB BY LIMB, never both. Two answers to
    # "where does this candidate go" is one answer too many, and the two drift.
    both = [r['family_id'] for r in fams
            if r.get('family_current_answers') and r.get('canonical_current_answer')]
    check('R-P2-OWNER-EXCLUSIVE', not both,
          'family(ies) claiming both a whole-question owner and limb owners: %s'
          % both)

    # AND THE SLOT MUST MATCH THE TYPE'S SCOPE. R-P2-OWNER-SHAPE above checks
    # the owner_id against the STORE the type names; this checks the type
    # against the SCOPE of the slot it was written into. They are different
    # mistakes: `SOLVED_PAPER_LIMB -> QP2606-Q8` is perfectly well shaped and
    # perfectly resolvable, and is still wrong in `canonical_current_answer`,
    # because that field means the whole family is answered and a limb owner
    # says only that one of its limbs is.
    wrong_scope = []
    for r in fams:
        t, i = CA.resolve_owner(r.get('canonical_current_answer'))
        if i and t in CA.OWNER_TYPES and t not in CA.WHOLE_OWNER_TYPES:
            wrong_scope.append('%s: whole-question slot carries %s'
                               % (r['family_id'], t))
        for l in r.get('family_current_answers') or []:
            t, i = CA.resolve_owner(l)
            if i and t in CA.OWNER_TYPES and t not in CA.LIMB_OWNER_TYPES:
                wrong_scope.append('%s.%s: limb slot carries %s'
                                   % (r['family_id'], l.get('limb_id'), t))
    check('R-P2-OWNER-SLOT', not wrong_scope,
          'ownership slot and owner_type disagree about scope: %s' % wrong_scope)

    # A SYNTHETIC QUESTION IS NOT A SITTING. The library record carries the
    # present-day question text; the Phase-2 record must not restate it as
    # though the family had acquired a new member. Sections 27 and 28.
    fake_member = []
    for r in fams:
        members = (projected.get(r['family_id']) or {}).get('modern_members') or []
        for m in members:
            if CA.is_ca_id(m):
                fake_member.append('%s: %s' % (r['family_id'], m))
    check('R-P2-NO-SYNTHETIC-MEMBER', not fake_member,
          'a current-answer id appears as a MEMBER of a recurrence family. A '
          'present-day answer is not evidence that anybody was asked it, and a '
          'family that counts one is partly counting MIW: %s' % fake_member)

    # Changed answers specifically: a CORRECTION must name the file it changed.
    changed_no_file = [r['family_id'] for r in fams
                       if r.get('correction_or_modernisation') == 'CORRECTION'
                       and not r.get('written_source_edited')]
    check('R-P2-CORRECTION-FILE', not changed_no_file,
          'family(ies) recorded as a CORRECTION without naming the canonical '
          'source edited: %s' % changed_no_file)

    # A modernisation must NOT claim to have edited a sitting-anchored answer.
    # That is the invariant the whole product rests on.
    mod_edited = [r['family_id'] for r in fams
                  if r.get('correction_or_modernisation') == 'MODERNISATION'
                  and r.get('written_source_edited')]
    check('R-P2-MODERNISATION-NOEDIT', not mod_edited,
          'family(ies) recorded as a MODERNISATION that edited a past-paper '
          'answer. A framework change AFTER a sitting may never be written '
          'into that sitting: %s' % mod_edited)

    # A modernisation has to actually say what the present-day position IS,
    # otherwise it is a status change dressed as research.
    mod_empty = [r['family_id'] for r in fams
                 if r.get('correction_or_modernisation') == 'MODERNISATION'
                 and not (r.get('present_day_position')
                          or r.get('present_day_provision_map'))]
    check('R-P2-MODERNISATION-CONTENT', not mod_empty,
          'family(ies) modernised without recording a present-day position: %s'
          % mod_empty)

    # ------------------------------------------------------------------ scope
    # A Phase-2 grant reaches ONE answer, not a whole family.
    #
    # This rule exists because the first propagation of this tranche got it
    # wrong: resolving QIF-EM-0017 made QP2402-Q5 read READY -- a February 2024
    # answer to a question about "ongoing developments", whose own record says
    # it must never be reused at a later sitting -- while the successor it was
    # superseded BY still read VERIFY. A family being sorted out is not the
    # same as every sitting inside it being safe to study.
    # Every question id a governed record blesses, whole or limb. A library id
    # never appears here and that is the point: a family answered by the current
    # library has blessed NO sitting, so every one of its members stays exactly
    # as unsafe to study as it was. MIW now answers the CONCEPT; it still has
    # not answered the 2021 paper.
    named = {oid for r in fams if r['final_state'] in SAFE
             for otype, oid in CA.owner_ids(r) if otype in CA.PAPER_OWNER_TYPES}
    over_reach = []
    for r in fams:
        if r['final_state'] not in SAFE:
            continue
        fid = r['family_id']
        for member in (projected.get(fid) or {}).get('modern_members') or []:
            if member in named:
                continue
            q = questions.get(member) or {}
            # Only judge members whose sole family is this one; a question in
            # two families may legitimately be ready through the other.
            if (q.get('canonical_family_ids') or []) != [fid]:
                continue
            if 'READY_TO_STUDY_NOW' in (q.get('readiness') or []):
                over_reach.append('%s: %s reads READY but is not the named '
                                  'canonical answer' % (fid, member))
    check('R-P2-ANSWER-SCOPE', not over_reach,
          'a Phase-2 resolution blessed a historical variant it never '
          'verified: %s' % over_reach)

    # ...and the same rule in the other direction, which tranche 002 found
    # missing. R-P2-ANSWER-SCOPE stops a RESOLUTION spreading. Nothing stopped a
    # HOLD from failing to spread, and that is the more dangerous of the two: a
    # held family means somebody looked and could not clear it, so a member
    # carrying a SOLVED answer must not go on reading "currentness check
    # pending", which says nobody has looked yet. QIF-EM-0058 is the case --
    # its answers cite Merchant Shipping Act 1958 sections repealed eight
    # months after the sitting.
    #
    # Members with no answer are exempt: NEW_ANSWER_REQUIRED already says more
    # than a currentness hold does, and demoting it would imply an answer
    # exists.
    soft = []
    for r in fams:
        if r['final_state'] not in BLOCKED:
            continue
        for member in (projected.get(r['family_id']) or {}).get('modern_members') or []:
            if member not in real_qids:
                continue
            states = (questions.get(member) or {}).get('readiness') or []
            if states and 'CURRENTNESS_HOLD' not in states:
                soft.append('%s: %s is held but reads %s'
                            % (r['family_id'], member, states))
    check('R-P2-HOLD-REACHES-ANSWERS', not soft,
          'a Phase-2 HOLD did not reach a solved answer inside the held '
          'family, so a finding is showing as an absence of one: %s' % soft)

    # ------------------------------------------------------------------ future
    # ADOPTED IS NOT IN FORCE. If a present-day position names a year later
    # than the date the authority was checked, the record must also declare
    # that item under future_not_in_force. Without this, "enters into force on
    # 29 November 2027" sits in a block headed "the position now" and reads as
    # current law to anyone skimming.
    undeclared = []
    for r in fams:
        checked = (r.get('authority_currentness_date') or '')[:4]
        if not checked.isdigit():
            continue
        now_text = json.dumps(
            [r.get('present_day_position') or [],
             r.get('present_day_provision_map') or []], ensure_ascii=False)
        future_text = json.dumps(r.get('future_not_in_force') or [],
                                 ensure_ascii=False)
        for yr in sorted(set(re.findall(r'\b(20[2-9][0-9])\b', now_text))):
            if int(yr) > int(checked) and yr not in future_text:
                undeclared.append('%s: present-day text names %s but no '
                                  'future_not_in_force entry mentions it'
                                  % (r['family_id'], yr))
    check('R-P2-FUTURE-DECLARED', not undeclared,
          'a future-dated element is presented as the current position: %s'
          % undeclared)

    # ------------------------------------------------------------------ F/I
    # Readiness must agree with the governed state, in BOTH directions.
    ready_unsafe, safe_unready = [], []
    for r in fams:
        fid = r['family_id']
        proj = projected.get(fid) or {}
        actual = proj.get('readiness')
        if r['final_state'] in SAFE and actual != 'READY_TO_STUDY_NOW':
            safe_unready.append('%s: verified but reads %s' % (fid, actual))
        if r['final_state'] in BLOCKED and actual == 'READY_TO_STUDY_NOW':
            ready_unsafe.append('%s: HELD but reads READY' % fid)
    check('R-P2-READY-AGREES', not safe_unready,
          'governed-verified family(ies) not reading as ready: %s' % safe_unready)
    check('R-P2-HOLD-BLOCKS', not ready_unsafe,
          'held family(ies) reading as ready: %s' % ready_unsafe)

    # And the declared readiness_after must be what the adapter actually
    # produced -- a record may not assert an outcome it did not cause.
    drift = ['%s: record says %s, adapter says %s'
             % (r['family_id'], r.get('readiness_after'),
                (projected.get(r['family_id']) or {}).get('readiness'))
             for r in fams
             if r.get('readiness_after')
             != (projected.get(r['family_id']) or {}).get('readiness')]
    check('R-P2-READY-DECLARED', not drift,
          'record readiness_after disagrees with the adapter: %s' % drift)

    # ------------------------------------------------------------------ G
    # Phase 1 is an INPUT. The pins prove it did not move underneath the work.
    pin_drift, pin_missing = [], []
    for r in fams:
        fid = r['family_id']
        pin = r.get('pinned_at_selection') or {}
        if not pin:
            pin_missing.append(fid)
            continue
        met = metrics.get(fid) or {}
        for key in ('count_3y', 'count_5y', 'count_10y', 'count_full_horizon',
                    'distinct_years'):
            if key in pin and key in met and pin[key] != met[key]:
                pin_drift.append('%s.%s pinned=%s live=%s'
                                 % (fid, key, pin[key], met[key]))
        q = queue.get(fid) or {}
        for key, qkey in (('phase2_rank', 'phase2_rank'),
                          ('unit', 'unit'),
                          ('first_sitting', 'first_sitting'),
                          ('last_sitting', 'last_sitting')):
            if key in pin and qkey in q and pin[key] != q[qkey]:
                pin_drift.append('%s.%s pinned=%s live=%s'
                                 % (fid, key, pin[key], q[qkey]))
    check('R-P2-PIN-PRESENT', not pin_missing,
          'family(ies) with no pinned_at_selection block, so Phase-1 drift '
          'could not be detected: %s' % pin_missing)
    check('R-P2-PIN-RECURRENCE', not pin_drift,
          'RECURRENCE MOVED DURING PHASE 2. Phase 2 consumes recurrence and '
          'never rewrites it: %s' % pin_drift)

    # The corpus-level counts are pinned too, so a family-level pin cannot be
    # "fixed" by moving the whole layer.
    check('R-P2-QI-FAMILIES', qi_fams['counts']['families'] == 270,
          'canonical family count moved: %s' % qi_fams['counts']['families'])
    check('R-P2-QI-OCCURRENCES', qi_occ['recurrence_bearing'] == 1584,
          'recurrence-bearing occurrence count moved: %s'
          % qi_occ['recurrence_bearing'])

    # ------------------------------------------------------------------ H
    # Modern question intelligence must survive Phase 2 untouched.
    modern_lost = []
    for r in fams:
        fid = r['family_id']
        pin = r.get('pinned_at_selection') or {}
        proj = projected.get(fid) or {}
        for key in ('modern_members', 'modern_family_ids',
                    'modern_recurrence_classes', 'historical_variants'):
            if key in pin and key in proj and sorted(pin[key]) != sorted(proj[key]):
                modern_lost.append('%s.%s pinned=%s live=%s'
                                   % (fid, key, pin[key], proj[key]))
    check('R-P2-MODERN', not modern_lost,
          'MODERN REPEAT INTELLIGENCE CHANGED during Phase 2: %s' % modern_lost)

    # ------------------------------------------------------------------ J
    # The adapter must actually be carrying the governed state. A Phase-2
    # decision that the study layer has not seen is a decision nobody acts on.
    stale = [r['family_id'] for r in fams
             if ((projected.get(r['family_id']) or {}).get('phase2_resolution')
                 or {}).get('final_state') != r['final_state']]
    check('R-P2-ADAPTER-FRESH', not stale,
          'the study adapter does not reflect the governed Phase-2 state -- '
          'rebuild with build_study_qi.py: %s' % stale)

    # ------------------------------------------------------------------ conflicts
    # Only holds this tranche actually adjudicated may have moved.
    adjudicated_here = {a['conflict_adjudication']['hold_id']
                        for a in fams if a.get('conflict_adjudication')}
    moved = {h['hold_id'] for h in holds['conflict_holds']
             if h['state'] != 'HOLD_RECONCILIATION'}
    check('R-P2-CONFLICT-SCOPE', moved <= adjudicated_here,
          'a conflict hold was resolved that this tranche did not adjudicate: '
          '%s' % sorted(moved - adjudicated_here))
    check('R-P2-CONFLICT-HUMAN',
          all(h.get('adjudicated_by') for h in holds['conflict_holds']
              if h['state'] != 'HOLD_RECONCILIATION'),
          'a conflict hold was resolved with no named adjudicator')
    check('R-P2-CONFLICT-COUNT', len(holds['conflict_holds']) == 7,
          'the conflict-hold population changed; holds are recorded, never '
          'deleted: %d' % len(holds['conflict_holds']))

    # ------------------------------------------------------------------ K
    # Phase 2 may not widen what the public page claims.
    body = B.get('public_html')
    leaked = [t for t in FORBIDDEN_PUBLIC if body and t in body]
    check('R-P2-PUBLIC-SAFE', not leaked,
          'the public roadmap gained a historical-count claim: %s' % leaked)



def report():
    width = max(len(r) for r, _, _ in RESULTS)
    for rule, ok, detail in RESULTS:
        print('  %s %s' % ('PASS' if ok else 'FAIL', rule.ljust(width)))
    fails = [(r, d) for r, ok, d in RESULTS if not ok]
    if fails:
        print('\nFAILURES')
        for rule, detail in fails:
            print('  %-24s %s' % (rule, detail))
        return 1
    print('\nPhase-2 gate: %d invariants hold.' % len(RESULTS))
    return 0


def main():
    if not os.path.exists(STORE):
        print('no Phase-2 store; nothing to gate')
        return 0
    run_checks(load_bundle())
    return report()


if __name__ == '__main__':
    sys.exit(main())
