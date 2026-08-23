#!/usr/bin/env python3
"""The ONE study-intelligence adapter.

Two question-intelligence layers exist in this repository and they are
complementary, not rival:

    MODERN QUESTION-LEVEL QI          2021 -> August 2026
        authored in the paper specs (host_recurrence_hint, recurrence_class,
        reuse_tier / reused_from / question_delta / cross_links) and clustered
        into `meoclass1/pastpapers/intelligence/derived/sixyear_families.json`.
        High precision: it names WHICH modern questions relate, and how.

    CANONICAL LONGITUDINAL QI         2010 -> August 2026
        `docs/study/qi/*`, one adjudicated family layer with recurrence
        windows, currentness triage and a Phase-2 queue.
        Long range: it says how far back a concept goes and whether it is
        persistent, rising, dormant or re-emerging.

This module joins them and is the ONLY place a study consumer may obtain a
recurrence number. Topics, roadmap, cohorts, workbook and the internal study
page all read it. Nothing downstream may re-parse question text, re-infer a
family, or keep a private recurrence table.

    modern QI  +  canonical QI  +  study mappings
                        |
                 study_qi_adapter          <- you are here
                        |
        question projection / topic projection / roadmap input


The five rules this module exists to enforce
--------------------------------------------

1.  NO MODERN INTELLIGENCE IS LOST.  Every modern record leaves this module
    carrying a disposition: PRESERVED_AS_IS, MAPPED_INTO_UNIFIED_MODEL,
    SUPERSEDED_WITH_EXPLICIT_MIGRATION, DUPLICATE_PROJECTION_CONFIRMED or
    CONFLICT_REQUIRES_REVIEW. Silence is not a disposition.

2.  NO DOUBLE WEIGHTING.  A modern repeat tag and a canonical family very often
    describe the SAME evidence stream seen twice. They are one vote. The
    adapter therefore emits exactly ONE recurrence quantity per topic, sourced
    from the canonical family layer, and the modern layer contributes
    precision fields that carry no weight. See RECURRENCE_WEIGHT_SOURCE.

3.  QUESTION IS NOT LIMB.  A family whose unit is a limb never projects as a
    whole-question repeat, and a modern relationship recorded against one limb
    is not widened by a broader family.

4.  HISTORICAL VARIANTS DO NOT MULTIPLY.  A family's recurrence attaches to one
    canonical current question, not to every member that ever stated it.

5.  RECURRENCE IS NOT READINESS.  A twelve-time repeat carrying a currentness
    risk is high importance AND blocked. It may never read as ready to study.
"""

import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import qi_model as M
import study_spine as SP

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(REPO, 'docs', 'study')
QI_DIR = os.path.join(DOC, 'qi')
SPEC_GLOB = os.path.join(REPO, 'meoclass1', 'pastpapers', 'specs', '*.json')
SIXYEAR = os.path.join(REPO, 'meoclass1', 'pastpapers', 'intelligence', 'derived',
                       'sixyear_families.json')
SIXYEAR_WATCH = os.path.join(REPO, 'meoclass1', 'pastpapers', 'intelligence', 'derived',
                             'sixyear_temporal_watch.json')
PHASE2_STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'qi_phase2_adjudications.json')

SCHEMA_VERSION = '1.0'

# --------------------------------------------------------------------------
# VOCABULARY
# --------------------------------------------------------------------------

#: Where a recurrence WEIGHT may come from. Exactly one source, by design.
#: The modern layer is precision, not a second vote (rule 2).
RECURRENCE_WEIGHT_SOURCE = 'CANONICAL_QI_FAMILY'

#: What happened to each existing modern-QI record (rule 1).
MODERN_DISPOSITIONS = {
    'PRESERVED_AS_IS':
        'The record is carried through unchanged and still readable at its '
        'original address.',
    'MAPPED_INTO_UNIFIED_MODEL':
        'The record is preserved AND joined to a canonical family, which '
        'extends it backward without altering what it says.',
    'SUPERSEDED_WITH_EXPLICIT_MIGRATION':
        'A governed migration record names the replacement. Never implicit.',
    'DUPLICATE_PROJECTION_CONFIRMED':
        'The record restates evidence held elsewhere; it carries no weight of '
        'its own but is not deleted.',
    'CONFLICT_REQUIRES_REVIEW':
        'Modern and canonical layers disagree materially. Held, not resolved.',
}

#: How a modern relationship compares with the canonical family layer.
RECONCILIATION_VERDICTS = {
    'AGREES':
        'Every member the canonical layer knows sits in one shared family, and '
        'that family adds no other modern member.',
    'MODERN_MORE_SPECIFIC':
        'The modern layer names members the canonical layer has not yet seen. '
        'The modern relationship is the finer statement and survives.',
    'FAMILY_MORE_SPECIFIC':
        'The canonical family reaches modern members the modern layer missed. '
        'It extends, it does not overwrite.',
    'LEGITIMATE_WHOLE_VS_LIMB':
        'The split is explained by a governed WHOLE_VS_LIMB_RELATION join. Not '
        'a disagreement -- a preserved distinction.',
    'LEGITIMATE_MULTI_RELATION':
        'One modern question legitimately participates in more than one family.',
    'CONFLICT':
        'The layers place the same modern questions in incompatible families '
        'and no governed join explains it.',
    'UNMAPPED':
        'No canonical family has seen any member of this modern relationship.',
}

#: The evidence class of a modern relationship. This drives precedence.
#: The distinction is not cosmetic: AUTHORED and DETERMINISTIC are governed
#: statements, INFERRED is a similarity threshold nobody adjudicated.
MODERN_EVIDENCE_CLASSES = {
    'AUTHORED':
        'A human wrote it into the paper spec (host_recurrence_hint, '
        'reused_from). Governed.',
    'DETERMINISTIC':
        'Identical normalised stems (sixyear EXACT_REPEAT). Reproducible with '
        'no threshold and no judgement.',
    'INFERRED':
        'A similarity clustering (sixyear NEAR_REPEAT). Proposes; it never '
        'decided anything.',
    'SINGLETON':
        'A one-member group. There is no relationship to reconcile.',
}

PRECEDENCE_RULE = (
    'For MODERN QUESTION IDENTITY the modern layer wins where its evidence is '
    'AUTHORED or DETERMINISTIC -- the canonical layer may extend such a '
    'relationship backward but may not silently regroup it. Where the modern '
    'evidence is INFERRED and the canonical layer has an adjudicated split, '
    'the adjudication wins and the inferred cluster is HELD, not deleted. '
    'This asymmetry is earned, not assumed: every DETERMINISTIC modern family '
    'agrees with the canonical layer, and every disagreement observed lies in '
    'the INFERRED band. If that ever stops being true the validator says so.'
)

#: Study readiness, projected from canonical currentness + Phase-2 action.
#: Recurrence never appears here (rule 5).
READINESS_STATES = {
    'READY_TO_STUDY_NOW':
        'A solved answer exists and no currentness risk fires against it.',
    'VERIFY_CURRENT_ANSWER':
        'A solved answer exists and a currentness signal fires. Important, not safe.',
    'NEW_ANSWER_REQUIRED':
        'Materially recurrent and MIW holds no solved answer.',
    'MODERNISE_REQUIRED':
        'A solved answer exists but the framework behind it has moved.',
    'CURRENTNESS_HOLD':
        'Currentness cannot be triaged from held evidence, or the family itself '
        'is held. High importance, explicitly unsafe.',
    'HISTORICAL_ONLY':
        'Recurred only in the historical band and shows no modern life.',
}

#: Phase-2 action -> readiness. The one place the mapping is written down.
ACTION_READINESS = {
    'CURRENT_AND_SOLVED': 'READY_TO_STUDY_NOW',
    'EXISTING_CURRENT_ANSWER_VERIFY': 'VERIFY_CURRENT_ANSWER',
    'NEW_MODERN_ANSWER_REQUIRED': 'NEW_ANSWER_REQUIRED',
    'HISTORICAL_ANSWER_REQUIRES_MODERNISATION': 'MODERNISE_REQUIRED',
    'SUPERSEDED_MODERN_REPLACEMENT_REQUIRED': 'MODERNISE_REQUIRED',
    'CURRENTNESS_RESEARCH_REQUIRED': 'CURRENTNESS_HOLD',
    'LOW_PRIORITY_HISTORICAL_ONLY': 'HISTORICAL_ONLY',
    'AMBIGUOUS_FAMILY_REVIEW': 'CURRENTNESS_HOLD',
}

#: Phase-2 final states that MAY clear a currentness block.
#: Clearing one is not a build decision: it requires a governed record in
#: `qi_phase2_adjudications.json` carrying current primary authority, an
#: independent review verdict and a resolvable canonical answer. The validator
#: enforces all three (R-P2-*). This is the ONLY route out of an unsafe
#: currentness state -- rule 5 still holds, and recurrence still never appears.
PHASE2_SAFE_STATES = {
    'CURRENT_AND_VERIFIED', 'UPDATED_AND_VERIFIED', 'MODERNISED_AND_VERIFIED',
    'NEW_CURRENT_ANSWER_CREATED', 'SUPERSEDED_WITH_SUCCESSOR',
}

#: Phase-2 final states that are explicitly still blocked. A hold is finished
#: work, not backlog -- same rule as the mapping review queue.
#:
#: HOLD_NO_CURRENT_ANSWER_OWNER was added by tranche 002 and it is the state
#: the other two could not express. The first two say the RESEARCH did not
#: close: authority could not be established, or a family relationship has to
#: be settled first. This one says the research closed perfectly well and MIW
#: still has nothing a candidate can be sent to -- the present-day core is
#: understood, and no question in the solved corpus answers it. Filing that as
#: HOLD_FOR_AUTHORITY would blame the sources for a gap in the product, and
#: the gap would then be invisible to anyone reading the store for what to
#: build next.
PHASE2_BLOCKED_STATES = {
    'HOLD_FOR_AUTHORITY', 'HOLD_FAMILY_RECONCILIATION',
    'HOLD_NO_CURRENT_ANSWER_OWNER',
}

#: Currentness classes that can never read as ready, whatever the action says.
UNSAFE_CURRENTNESS = {
    'CURRENT_FRAMEWORK_CHANGED', 'LIKELY_SUPERSEDED',
    'CURRENTNESS_REVIEW_REQUIRED', 'HISTORICAL_ONLY',
}

#: Dimensions kept apart on purpose -- no opaque score (contract section 15).
DIMENSIONS = [
    'modern_repeat_signal', 'recent_3y', 'recent_5y', 'medium_10y',
    'full_horizon', 'persistent', 're_emerging', 'rising',
    'currentness_risk', 'answer_readiness',
]

MONTHS = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUNE': 6,
          'JUL': 7, 'JULY': 7, 'AUG': 8, 'SEP': 9, 'SEPT': 9, 'OCT': 10,
          'NOV': 11, 'DEC': 12}


class AdapterError(Exception):
    pass


def _load(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
# 1. THE EXISTING MODERN QUESTION-LEVEL QI  (2021 -> August 2026)
# --------------------------------------------------------------------------

def normalise_recurrence_class(raw):
    """`recurrence_class` is a free-text authoring field and it shows: the
    corpus carries one idea as 'exact_recurrence', 'EXACT RECURRENCE' and
    'EXACT_RECURRENCE'. Normalising for READING is safe and necessary; the raw
    value is always kept beside it, because this field is an authoring note and
    rewriting forty specs to tidy it is a corpus edit, not an integration step.
    """
    if not raw:
        return None
    return re.sub(r'[^A-Z0-9]+', '_', str(raw).strip().upper()).strip('_')


def parse_hint(ref):
    """'2022/JAN/Q7' -> ('2022-01', 'QP2201-Q7'); '2019/OCT' -> ('2019-10', None).

    The authored hints reach back well before 2021 and frequently name only a
    sitting. That is not a defect: it is the modern layer making its own claim
    of historical depth, and it is precisely what the canonical layer can now
    corroborate or fail to corroborate.
    """
    parts = [p for p in str(ref).split('/') if p]
    if len(parts) < 2:
        return None, None
    year, mon = parts[0].strip(), parts[1].strip().upper()
    if not re.fullmatch(r'\d{4}', year) or mon not in MONTHS:
        return None, None
    sitting = '%s-%02d' % (year, MONTHS[mon])
    qid = None
    if len(parts) > 2:
        m = re.fullmatch(r'Q?(\d+)[a-z)]*', parts[2].strip(), re.I)
        if m:
            qid = 'QP%s%02d-Q%s' % (year[2:], MONTHS[mon], m.group(1))
    return sitting, qid


def month_num(month):
    if isinstance(month, int):
        return month
    key = str(month).strip().upper()
    for name in ('JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY',
                 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'):
        if key.startswith(name[:3]):
            return MONTHS[name[:3]]
    raise AdapterError('unparseable spec month %r' % (month,))


def load_modern_qi():
    """Everything the repository already knew about modern question recurrence,
    read from its own homes and never rewritten."""
    authored = {}
    for path in sorted(glob.glob(SPEC_GLOB)):
        spec = _load(path)
        pid = spec['paper_id']
        for q in spec['questions']:
            qid = '%s-%s' % (pid, q['q_no'])
            hints = list(q.get('host_recurrence_hint') or [])
            resolved, sittings, unresolved = [], [], []
            for h in hints:
                sitting, target = parse_hint(h)
                if sitting is None:
                    unresolved.append(h)
                    continue
                sittings.append(sitting)
                if target:
                    resolved.append(target)
            authored[qid] = {
                'question_id': qid,
                'paper_id': pid,
                'sitting': '%s-%02d' % (spec['year'], month_num(spec['month'])),
                'recurrence_class_raw': q.get('recurrence_class'),
                'recurrence_class': normalise_recurrence_class(q.get('recurrence_class')),
                'host_recurrence_hint': hints,
                # Self excluded: host_recurrence_hint lists every sitting in
                # the lineage INCLUDING this one, which is right for a hint but
                # wrong for a field called "related". Leaving it in made every
                # question its own relation.
                'related_question_ids': sorted(set(resolved) - {qid}),
                'related_sittings': sorted(set(sittings)),
                'unresolved_hints': unresolved,
                'reuse_tier': q.get('reuse_tier'),
                'reused_from': q.get('reused_from') or None,
                'has_question_delta': bool(q.get('question_delta')),
                'cross_links': len(q.get('cross_links') or []),
                'primary_category': q.get('primary_category'),
                'total_marks': q.get('total_marks'),
                'has_model_answer': bool(q.get('model_answer')),
            }

    fams = _load(SIXYEAR)
    watch = {f['family_id'] for f in _load(SIXYEAR_WATCH)}
    derived, member_family = [], {}
    for f in fams:
        ev = ('DETERMINISTIC' if f['class'] == 'EXACT_REPEAT'
              else 'INFERRED' if f['class'] == 'NEAR_REPEAT' else 'SINGLETON')
        rec = {
            'modern_family_id': f['family_id'],
            'modern_class': f['class'],
            'modern_evidence_class': ev,
            'size': f['size'],
            'members': list(f['members']),
            'years': list(f['years']),
            'first_seen': f['first_seen'],
            'last_seen': f['last_seen'],
            'on_temporal_watch': f['family_id'] in watch,
            'statuses': list(f['statuses']),
        }
        derived.append(rec)
        for m in f['members']:
            member_family[m] = f['family_id']

    return {
        'authored': authored,
        'derived_families': derived,
        'member_to_modern_family': member_family,
        'counts': {
            'authored_questions': len(authored),
            'questions_with_repeat_intelligence':
                sum(1 for a in authored.values()
                    if a['host_recurrence_hint'] or a['reused_from']),
            'authored_hint_references':
                sum(len(a['host_recurrence_hint']) for a in authored.values()),
            'authored_related_question_edges':
                sum(len(a['related_question_ids']) for a in authored.values()),
            'reused_from_records':
                sum(1 for a in authored.values() if a['reused_from']),
            'modern_families': len(derived),
            'modern_multi_member_families': sum(1 for r in derived if r['size'] > 1),
            'modern_family_members_in_multi':
                sum(r['size'] for r in derived if r['size'] > 1),
            'modern_families_by_class': dict(Counter(r['modern_class'] for r in derived)),
            'modern_families_by_evidence':
                dict(Counter(r['modern_evidence_class'] for r in derived)),
            'temporal_watch_families': len(watch),
            'recurrence_class_distinct_raw_values':
                len({a['recurrence_class_raw'] for a in authored.values()
                     if a['recurrence_class_raw']}),
            'recurrence_class_distinct_normalised':
                len({a['recurrence_class'] for a in authored.values()
                     if a['recurrence_class']}),
        },
    }


# --------------------------------------------------------------------------
# 2. THE CANONICAL LONGITUDINAL QI  (2010 -> August 2026)
# --------------------------------------------------------------------------

def load_phase2():
    """Governed Phase-2 answer decisions, keyed by family.

    Hand-maintained, like `qi_phase1_adjudications.json` and
    `study_qi_holds.json`. Absent file is not an error: Phase 2 is incremental
    by tranche, and most families have not been worked yet.
    """
    if not os.path.exists(PHASE2_STORE):
        return {}
    store = _load(PHASE2_STORE)
    return {r['family_id']: r for r in store.get('families', [])}


def load_canonical_qi():
    ents = {e['entity_id']: e for e in
            _load(os.path.join(QI_DIR, 'qi_source_entities.json'))['entities']}
    fams = _load(os.path.join(QI_DIR, 'qi_families.json'))['families']
    metrics = {m['family_id']: m for m in
               _load(os.path.join(QI_DIR, 'qi_time_window_metrics.json'))['families']}
    curr = {c['family_id']: c for c in
            _load(os.path.join(QI_DIR, 'qi_currentness.json'))['families']}
    queue = {q['family_id']: q for q in
             _load(os.path.join(QI_DIR, 'qi_phase2_action_queue.json'))['queue']}
    joins = _load(os.path.join(QI_DIR, 'qi_family_joins.json'))['joins']
    # occurrence_id -> sitting, read from the occurrence layer rather than
    # parsed out of the id. The id embeds a SET id ('2016/APR'), not a sitting
    # ('2016-04'); deriving one from the other by string surgery is how a
    # corroboration check silently reports zero matches.
    occ_sitting = {o['occurrence_id']: o['sitting']
                   for o in _load(os.path.join(QI_DIR, 'qi_occurrences.json'))['occurrences']}

    native_to_families = defaultdict(list)
    for f in fams:
        for eid in f['member_entities']:
            ent = ents[eid]
            if ent['evidence_band'] == 'HISTORICAL_SECONDARY_ARCHIVE':
                continue
            native_to_families[ent['native_id']].append(f['family_id'])

    join_index = defaultdict(dict)
    for j in joins:
        join_index[j['family_a']][j['family_b']] = j['verdict']
        join_index[j['family_b']][j['family_a']] = j['verdict']

    return {
        'entities': ents,
        'families': {f['family_id']: f for f in fams},
        'family_list': fams,
        'metrics': metrics,
        'currentness': curr,
        'queue': queue,
        'phase2': load_phase2(),
        'joins': joins,
        'join_index': join_index,
        'occurrence_sitting': occ_sitting,
        'native_to_families': dict(native_to_families),
        'counts': {
            'families': len(fams),
            'entities': len(ents),
            'modern_natives_in_families': len(native_to_families),
        },
    }


# --------------------------------------------------------------------------
# 3. RECONCILIATION  --  neither layer silently wins
# --------------------------------------------------------------------------

def reconcile(modern, canonical):
    """Compare every MULTI-MEMBER modern relationship with the canonical family
    layer. Singletons carry no relationship to reconcile.

    A disagreement is never resolved here. It is classified, and a CONFLICT
    becomes a governed hold that a human adjudicates.
    """
    n2f = canonical['native_to_families']
    fams = canonical['families']
    joins = canonical['join_index']
    rows = []

    for rec in modern['derived_families']:
        if rec['size'] < 2:
            continue
        members = rec['members']
        known = [m for m in members if n2f.get(m)]
        row = {
            'modern_family_id': rec['modern_family_id'],
            'modern_class': rec['modern_class'],
            'modern_evidence_class': rec['modern_evidence_class'],
            'members': members,
            'members_known_to_canonical': known,
            'canonical_families': sorted({q for m in known for q in n2f[m]}),
        }
        if not known:
            row['verdict'] = 'UNMAPPED'
            row['disposition'] = 'PRESERVED_AS_IS'
            row['reason'] = ('No canonical family has seen any member. The modern '
                             'relationship stands alone and is preserved intact.')
            rows.append(row)
            continue

        shared = set.intersection(*[set(n2f[m]) for m in known])
        multi = [m for m in known if len(n2f[m]) > 1]

        if shared:
            extra = set()
            for q in shared:
                for eid in fams[q]['member_entities']:
                    ent = canonical['entities'][eid]
                    if (ent['evidence_band'] != 'HISTORICAL_SECONDARY_ARCHIVE'
                            and ent['native_id'] not in members):
                        extra.add(ent['native_id'])
            if len(known) < len(members):
                row['verdict'] = 'MODERN_MORE_SPECIFIC'
                row['modern_only_members'] = [m for m in members if m not in known]
                row['reason'] = (
                    'The modern layer names %d member(s) the canonical layer has '
                    'not seen. The modern relationship is the finer statement and '
                    'is what a study surface must show.'
                    % (len(members) - len(known)))
            elif extra:
                row['verdict'] = 'FAMILY_MORE_SPECIFIC'
                row['canonical_adds_modern_members'] = sorted(extra)
                row['reason'] = (
                    'The canonical family reaches %d further modern member(s). It '
                    'extends the modern relationship; it replaces nothing.'
                    % len(extra))
            elif multi:
                row['verdict'] = 'LEGITIMATE_MULTI_RELATION'
                row['multi_family_members'] = sorted(multi)
                row['reason'] = ('Members participate in more than one canonical '
                                 'family, which is legal at limb level.')
            else:
                row['verdict'] = 'AGREES'
                row['reason'] = 'Both layers describe one and the same group.'
            row['disposition'] = 'MAPPED_INTO_UNIFIED_MODEL'
            rows.append(row)
            continue

        # No shared family: the canonical layer split this modern group.
        split = row['canonical_families']
        verdicts = {joins[a].get(b) for a in split for b in split if a != b}
        verdicts.discard(None)
        if 'WHOLE_VS_LIMB_RELATION' in verdicts:
            row['verdict'] = 'LEGITIMATE_WHOLE_VS_LIMB'
            row['governing_joins'] = sorted(verdicts)
            row['disposition'] = 'MAPPED_INTO_UNIFIED_MODEL'
            row['reason'] = (
                'The canonical split is explained by a governed '
                'WHOLE_VS_LIMB_RELATION join. Merging it back would turn a limb '
                'sitting count into a whole-question count -- exactly the error '
                'the join exists to record.')
        else:
            row['verdict'] = 'CONFLICT'
            row['disposition'] = 'CONFLICT_REQUIRES_REVIEW'
            row['canonical_split_into'] = split
            row['governing_joins'] = sorted(verdicts)
            row['precedence'] = (
                'MODERN_WINS'
                if rec['modern_evidence_class'] in ('AUTHORED', 'DETERMINISTIC')
                else 'CANONICAL_ADJUDICATION_WINS')
            row['reason'] = (
                'The canonical layer split this %s group into %d families and no '
                'governed join explains it. The modern evidence is %s, so '
                'precedence is %s. The modern grouping is HELD, never deleted.'
                % (rec['modern_class'], len(split), rec['modern_evidence_class'],
                   row['precedence']))
        rows.append(row)

    return rows


def authored_corroboration(modern, canonical):
    """The authored hints make historical claims of their own, many reaching
    back to 2013. Check them against governed occurrences rather than trusting
    or discarding either side."""
    n2f = canonical['native_to_families']
    out = []
    for qid, a in sorted(modern['authored'].items()):
        if not a['related_sittings']:
            continue
        qfams = n2f.get(qid, [])
        governed = set()
        for fid in qfams:
            governed |= family_sittings(canonical, fid)
        claimed = set(a['related_sittings'])
        out.append({
            'question_id': qid,
            'claimed_sittings': sorted(claimed),
            'claimed_pre_2021': sorted(s for s in claimed if s < '2021-01'),
            'canonical_families': qfams,
            'corroborated': sorted(claimed & governed),
            'uncorroborated': sorted(claimed - governed),
            'canonical_only': sorted(governed - claimed),
        })
    return out


def family_sittings(canonical, fid):
    """The YYYY-MM sittings a family actually occupies, from governed records."""
    fam = canonical['families'].get(fid)
    if not fam:
        return set()
    sit = canonical['occurrence_sitting']
    return {sit[oid] for oid in fam.get('occurrence_ids', []) if oid in sit}


# --------------------------------------------------------------------------
# 4. FAMILY -> ONE CANONICAL CURRENT QUESTION   (rule 4)
# --------------------------------------------------------------------------

def canonical_current_question(canonical, fid):
    """A family's recurrence attaches to ONE question, not to every variant that
    ever stated it. Otherwise an eight-member family would contribute eight
    times to its topic and historical bulk would drown current relevance.

    The bearer is the most recent SOLVED modern member; failing that the most
    recent modern member of any band; failing that nothing, and the family is
    historical-only.
    """
    fam = canonical['families'][fid]
    solved, wording = [], []
    for eid in fam['member_entities']:
        ent = canonical['entities'][eid]
        if ent['evidence_band'] == 'MIW_SOLVED_CANONICAL':
            solved.append(ent['native_id'])
        elif ent['evidence_band'] == 'MIW_WORDING_ONLY':
            wording.append(ent['native_id'])
    pool = solved or wording
    if not pool:
        return None, [], 'HISTORICAL_ONLY_NO_MODERN_MEMBER'
    bearer = sorted(pool, key=paper_sort_key)[-1]
    variants = sorted(set(solved + wording) - {bearer})
    return bearer, variants, ('SOLVED_BEARER' if solved else 'WORDING_ONLY_BEARER')


def paper_sort_key(native_id):
    m = re.match(r'QP(\d{2})(\d{2})-Q(\d+)', native_id)
    if not m:
        return (0, 0, 0, native_id)
    return (2000 + int(m.group(1)), int(m.group(2)), int(m.group(3)), native_id)


# --------------------------------------------------------------------------
# 5. READINESS   (rule 5)
# --------------------------------------------------------------------------

def readiness_for(canonical, fid):
    q = canonical['queue'].get(fid) or {}
    c = canonical['currentness'].get(fid) or {}
    action = q.get('phase2_action') or q.get('action')
    status = c.get('currentness_status', 'UNKNOWN')
    state = ACTION_READINESS.get(action, 'CURRENTNESS_HOLD')
    # A currentness risk overrides a cheerful action, never the other way round.
    if status in UNSAFE_CURRENTNESS and state == 'READY_TO_STUDY_NOW':
        state = 'CURRENTNESS_HOLD'

    triage_readiness = state

    # Phase-2 governed resolution. The triage above is only ever a TRIAGE: it
    # says nobody checked, not that the answer is wrong. Where a human has
    # since established current primary authority for this family and a second
    # pass reviewed that work, the block it raised is resolved -- and that is
    # the only thing that resolves it. No count is consulted here.
    p2 = (canonical.get('phase2') or {}).get(fid) or {}
    if p2:
        final = p2.get('final_state')
        if final in PHASE2_SAFE_STATES:
            state = 'READY_TO_STUDY_NOW'
        elif final == 'HISTORICAL_ONLY':
            state = 'HISTORICAL_ONLY'
        else:
            state = 'CURRENTNESS_HOLD'

    return {
        'readiness': state,
        'phase2_action': action,
        'currentness_status': status,
        # The queue writes this field as `existing_answer_status`. It was read
        # here under two names it never had, so it was silently None on every
        # family in the corpus until 2026-08-23.
        'answer_coverage': q.get('existing_answer_status'),
        'modern_question_action': q.get('modern_question_action'),
        'blocked': state not in ('READY_TO_STUDY_NOW', 'HISTORICAL_ONLY'),
        'triage_readiness': triage_readiness,
        'phase2_resolution': ({
            'tranche_id': p2.get('tranche_id'),
            'final_state': p2.get('final_state'),
            'action_taken': p2.get('action_taken'),
            'correction_or_modernisation': p2.get('correction_or_modernisation'),
            'authority_currentness_date': p2.get('authority_currentness_date'),
            'review_verdict': (p2.get('independent_review') or {}).get('verdict'),
            'canonical_current_answer':
                (p2.get('canonical_current_answer') or {}).get('question_id'),
        } if p2 else None),
    }


# --------------------------------------------------------------------------
# 6. PROJECTIONS  --  what every consumer actually reads
# --------------------------------------------------------------------------

def family_labels(canonical, fid):
    m = canonical['metrics'].get(fid) or {}
    return list(m.get('labels') or m.get('intelligence_labels') or [])


def project_families(modern, canonical, mappings):
    """One row per canonical family: its longitudinal metrics, the modern
    intelligence attached to it, the single question that bears its weight, and
    the topic it reaches."""
    rows = []
    for fid, fam in sorted(canonical['families'].items()):
        met = canonical['metrics'].get(fid, {})
        bearer, variants, bearer_kind = canonical_current_question(canonical, fid)
        ready = readiness_for(canonical, fid)
        labels = family_labels(canonical, fid)

        modern_members, modern_families, modern_classes = [], set(), set()
        for eid in fam['member_entities']:
            ent = canonical['entities'][eid]
            if ent['evidence_band'] == 'HISTORICAL_SECONDARY_ARCHIVE':
                continue
            nid = ent['native_id']
            modern_members.append(nid)
            mf = modern['member_to_modern_family'].get(nid)
            if mf:
                modern_families.add(mf)
            a = modern['authored'].get(nid)
            if a and a['recurrence_class']:
                modern_classes.add(a['recurrence_class'])

        topics = sorted({mappings[n]['topic_id'] for n in modern_members
                         if n in mappings and mappings[n].get('topic_id')})
        # A family reaches a topic through the ONE bearer for weighting, but the
        # full topic set is reported so a multi-topic family is visible.
        weight_topic = (mappings.get(bearer) or {}).get('topic_id') if bearer else None

        rows.append({
            'family_id': fid,
            'label': fam.get('label'),
            'unit': fam.get('unit'),
            'count_3y': met.get('count_3y', 0),
            'count_5y': met.get('count_5y', 0),
            'count_10y': met.get('count_10y', 0),
            'count_full_horizon': met.get('count_full_horizon', 0),
            'distinct_years': met.get('distinct_years', 0),
            'first_sitting': met.get('first_sitting'),
            'last_sitting': met.get('last_sitting'),
            'labels': labels,
            'modern_members': sorted(modern_members),
            'modern_family_ids': sorted(modern_families),
            'modern_recurrence_classes': sorted(modern_classes),
            'canonical_current_question': bearer,
            'canonical_bearer_kind': bearer_kind,
            'historical_variants': variants,
            'weight_topic_id': weight_topic,
            'topics_reached': topics,
            'topic_reach': ('MAPPED' if topics else
                            'HISTORICAL_ONLY_NO_MODERN_MEMBER' if not modern_members
                            else 'MODERN_MEMBER_PRESENT_BUT_UNMAPPED'),
            'materially_recurrent': (
                met.get('count_full_horizon', 0) >= M.MATERIALLY_RECURRENT_MIN_OCCURRENCES
                and met.get('distinct_sittings', 0) >= M.MATERIALLY_RECURRENT_MIN_SITTINGS),
            **ready,
        })
    return rows


def question_readiness(fam_row, nid, has_answer=True):
    """The readiness ONE question inherits from ONE family.

    A family can be resolved while most of its members stay unsafe to study.
    They are older sittings whose answers nobody re-checked, and in a
    SUPERSEDED_WITH_SUCCESSOR family the family's own bearer is explicitly the
    thing NOT to study. So a Phase-2 grant reaches only the question the
    governed record actually names as the canonical current answer; every
    other member keeps the triage verdict it already had.

    Without this, resolving a family silently blesses every historical variant
    in it -- which is how a thirty-month-old answer to a question about
    "ongoing developments" comes to read as ready.
    """
    p2 = fam_row.get('phase2_resolution') or {}
    if not p2:
        return fam_row['readiness']
    if p2.get('canonical_current_answer') == nid:
        return fam_row['readiness']

    # The fallback above is asymmetric on purpose, and tranche 002 found the
    # side that had not been thought through.
    #
    # Falling back to TRIAGE is right when the family was RESOLVED: the grant
    # must not spread, so every other member keeps the verdict it already had.
    # It is wrong when the family was HELD, because then the triage verdict is
    # the weaker statement and falling back to it SOFTENS a finding. QIF-EM-0058
    # is the worked case: its answer cites Merchant Shipping Act 1958 sections
    # that were repealed eight months after the sitting, Phase 2 established
    # that and held the family -- and the member still read "Currentness check
    # pending", which says nobody has looked. Somebody had looked. That is the
    # weaker claim beating the stronger one, which is the failure direction this
    # whole layer is built to prevent.
    #
    # A held family therefore pushes its block down to any member that HAS an
    # answer. A member with no answer keeps NEW_ANSWER_REQUIRED, which is not a
    # softening: "MIW has no current-framework answer" is already the more
    # precise statement for a wording-only sitting, and demoting it to "answer
    # under currentness review" would tell a candidate that an answer exists.
    if p2.get('final_state') in PHASE2_BLOCKED_STATES and has_answer:
        return fam_row['readiness']

    return fam_row.get('triage_readiness') or fam_row['readiness']


def project_questions(modern, canonical, mappings, fam_rows):
    """Per modern question: the modern tag AND the family context, side by side.
    Neither field is derived from the other and neither replaces the other."""
    by_fid = {r['family_id']: r for r in fam_rows}
    n2f = canonical['native_to_families']
    rows = []
    natives = set(modern['authored']) | set(n2f) | set(modern['member_to_modern_family'])
    for nid in sorted(natives, key=paper_sort_key):
        a = modern['authored'].get(nid) or {}
        fids = n2f.get(nid, [])
        fr = [by_fid[f] for f in fids if f in by_fid]
        bearer_of = [r['family_id'] for r in fr if r['canonical_current_question'] == nid]
        rows.append({
            'question_id': nid,
            'topic_id': (mappings.get(nid) or {}).get('topic_id'),
            'band': ('MIW_SOLVED_CANONICAL' if nid in modern['authored']
                     else 'MIW_WORDING_ONLY'),
            # ---- the existing modern layer, preserved verbatim --------------
            'modern_recurrence_class': a.get('recurrence_class'),
            'modern_recurrence_class_raw': a.get('recurrence_class_raw'),
            'modern_related_question_ids': a.get('related_question_ids', []),
            'modern_related_sittings': a.get('related_sittings', []),
            'modern_host_recurrence_hint': a.get('host_recurrence_hint', []),
            'modern_reuse_tier': a.get('reuse_tier'),
            'modern_reused_from': a.get('reused_from'),
            'modern_family_id': modern['member_to_modern_family'].get(nid),
            'modern_repeat_signal': bool(
                a.get('host_recurrence_hint') or a.get('reused_from')
                or (modern['member_to_modern_family'].get(nid) and any(
                    d['size'] > 1 and d['modern_family_id']
                    == modern['member_to_modern_family'].get(nid)
                    for d in modern['derived_families']))),
            # ---- the longitudinal layer, extending it -----------------------
            'canonical_family_ids': fids,
            'count_3y': max([r['count_3y'] for r in fr], default=0),
            'count_5y': max([r['count_5y'] for r in fr], default=0),
            'count_10y': max([r['count_10y'] for r in fr], default=0),
            'count_full_horizon': max([r['count_full_horizon'] for r in fr], default=0),
            'recurrence_labels': sorted({l for r in fr for l in r['labels']}),
            'family_unit': sorted({r['unit'] for r in fr if r.get('unit')}),
            'currentness_status': sorted({r['currentness_status'] for r in fr}),
            'readiness': sorted({question_readiness(r, nid, nid in modern['authored'])
                                 for r in fr}),
            'phase2_action': sorted({r['phase2_action'] for r in fr if r['phase2_action']}),
            # ---- weighting (rule 4) -----------------------------------------
            'bears_family_weight_for': bearer_of,
            'is_historical_variant': bool(fr) and not bearer_of,
        })
    return rows


def project_topics(fam_rows, q_rows):
    """Per-domain intelligence. Every dimension stays separate (contract 15)."""
    out = {}
    for d in SP.DOMAINS:
        did = d['domain_id']
        # Weight-bearing families only -- rule 4. A family counts for the topic
        # of its ONE bearer, so historical variants cannot multiply the total.
        fams = [r for r in fam_rows if r['weight_topic_id'] == did]
        recurrent = [r for r in fams if r['materially_recurrent']]
        qs = [r for r in q_rows if r['topic_id'] == did]
        lab = Counter(l for r in recurrent for l in r['labels'])
        ready = Counter(r['readiness'] for r in recurrent)
        n = len(recurrent)
        out[did] = {
            'topic_id': did,
            'modern_repeated_questions': sum(1 for r in qs if r['modern_repeat_signal']),
            'mapped_families': len(fams),
            'materially_recurrent_families': n,
            'active_3y': sum(1 for r in recurrent if r['count_3y'] > 0),
            'active_5y': sum(1 for r in recurrent if r['count_5y'] > 0),
            'active_10y': sum(1 for r in recurrent if r['count_10y'] > 0),
            'persistent': lab.get('PERSISTENT', 0),
            're_emerging': lab.get('RE_EMERGING', 0),
            'rising': lab.get('RISING', 0),
            'dormant': lab.get('DORMANT', 0),
            'currentness_risk': sum(1 for r in recurrent
                                    if r['currentness_status'] in UNSAFE_CURRENTNESS),
            'ready_to_study_now': ready.get('READY_TO_STUDY_NOW', 0),
            'verify_current_answer': ready.get('VERIFY_CURRENT_ANSWER', 0),
            'new_answer_required': ready.get('NEW_ANSWER_REQUIRED', 0),
            'modernise_required': ready.get('MODERNISE_REQUIRED', 0),
            'currentness_hold': ready.get('CURRENTNESS_HOLD', 0),
            'historical_only': ready.get('HISTORICAL_ONLY', 0),
            'readiness_pct': round(100.0 * ready.get('READY_TO_STUDY_NOW', 0) / n, 1) if n else 0.0,
        }
    return out


# --------------------------------------------------------------------------
# 7. THE ROADMAP INPUT  --  exactly one recurrence quantity (rule 2)
# --------------------------------------------------------------------------

def roadmap_recurrence(topic_rows):
    """The single `written_recurrence` raw input per domain.

    This function is the double-weight guard in code rather than in prose: it
    returns ONE number per topic, and that number is computed only from
    canonical families that bear weight. The modern layer already contributed
    to those families' formation, so counting a modern repeat tag again here
    would count one evidence stream twice.
    """
    return {
        'source': RECURRENCE_WEIGHT_SOURCE,
        'measure': 'materially_recurrent_families',
        'double_weight_guard': (
            'Modern repeat tags and canonical families are two views of one '
            'evidence stream. Only the canonical view carries weight; the '
            'modern view carries precision. There is exactly one recurrence '
            'key in this dict and the validator proves it.'),
        'by_topic': {did: t['materially_recurrent_families']
                     for did, t in sorted(topic_rows.items())},
    }


def roadmap_recurrence_by_topic():
    """The one call a priority model makes. Returns {topic_id: count}.

    Deliberately the ONLY convenience entry point: a consumer that wants a
    recurrence number gets this and nothing else, so there is no way to reach
    in and add a second recurrence quantity to the same score.
    """
    modern = load_modern_qi()
    canonical = load_canonical_qi()
    with open(os.path.join(DOC, 'study_mappings.json'), encoding='utf-8') as fh:
        mappings = json.load(fh)['mappings']
    fam_rows = project_families(modern, canonical, mappings)
    q_rows = project_questions(modern, canonical, mappings, fam_rows)
    return roadmap_recurrence(project_topics(fam_rows, q_rows))['by_topic']
