#!/usr/bin/env python3
"""Build the governed 2010 -> August 2026 Question Intelligence layer.

    governed inputs  +  hand adjudications  +  pinned research source ref
                              |
                      deterministic builder
                              |
                     generated QI projections
                              |
                        validate_qi.py

Nothing below is hand-editable. Every file this writes is regenerable from the
same three inputs, and `--check` proves that the files on disk are what those
inputs produce.

Inputs
    origin/research/historical-written-qi-2010-2020 (PINNED, read-only)
        the 2010-2020 archived secondary source layer. Read through `git show`.
        Raw research stays on its own branch; only the governed derivation lands.
    meoclass1/pastpapers/intelligence/historical_qp_intelligence.json
        the 2021-2023 papers MIW holds a source copy of, wording only.
    meoclass1/pastpapers/specs/*.json
        the solved 2023-2026 corpus. The canonical modern question.
    tools/study/qi_phase1_adjudications.json
        the semantic decisions.

Usage
    python tools/study/build_qi.py            # write
    python tools/study/build_qi.py --check    # fail if disk differs from inputs
"""

import glob
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import qi_model as M
import qi_similarity as S

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(REPO, 'docs', 'study', 'qi')
ADJ_PATH = os.path.join(REPO, 'tools', 'study', 'qi_phase1_adjudications.json')

RESEARCH_REF = 'origin/research/historical-written-qi-2010-2020'
RESEARCH_SHA = '2b22cd4'
RESEARCH_OCCURRENCES = 'research/historical-written-qi/EXTRACTED_OCCURRENCES.json'
RESEARCH_SOURCE_MAP = 'research/historical-written-qi/SOURCE_MAP_2010_2020.json'

MONTHS = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11,
    'December': 12,
}


class BuildError(Exception):
    pass


def show(ref, path):
    try:
        raw = subprocess.check_output(
            ['git', 'show', '%s:%s' % (ref, path)], cwd=REPO, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:
        raise BuildError(
            'cannot read %s from %s.\n'
            'The historical source layer lives on a pinned research ref and is '
            'never merged. Run `git fetch origin --prune` and retry.\n%s'
            % (path, ref, exc.stderr.decode('utf-8', 'replace')[:400]))
    return json.loads(raw.decode('utf-8'))


# --------------------------------------------------------------------------
# 1. SOURCE ENTITIES and OCCURRENCES -- one unified layer, three bands.
# --------------------------------------------------------------------------

def load_historical():
    """2010-2020. The source's own question id is the entity; the archived page
    for a month evidences that entity's MEMBERSHIP of that sitting at that
    ordinal. Wording is entity-level and is NOT per-sitting evidence."""
    doc = show(RESEARCH_REF, RESEARCH_OCCURRENCES)
    rows = doc['occurrences']
    entities, occurrences = {}, []

    by_entity = defaultdict(list)
    for r in rows:
        by_entity[r['ds_question_id']].append(r)

    for native, rs in sorted(by_entity.items()):
        eid = M.entity_id('HISTORICAL_SECONDARY_ARCHIVE', native)
        # The entity's canonical wording. 250 of 256 entities carry exactly one
        # wording across every sitting; where several exist the fullest is the
        # entity text and the rest are recorded as variants.
        wordings = sorted({r['raw_wording'] for r in rs}, key=lambda w: (-len(w), w))
        entities[eid] = {
            'entity_id': eid,
            'evidence_band': 'HISTORICAL_SECONDARY_ARCHIVE',
            'native_id': native,
            'stem': wordings[0],
            'stem_variants': wordings[1:],
            'stem_scope': 'ENTITY_LEVEL',
            'stem_scope_note': (
                'The source publishes one wording per question entity and reuses '
                'it on every set page. This text is the entity wording, NOT the '
                'text as printed in any particular sitting. Per-sitting evidence '
                'is membership and ordinal only.'),
            'question_text_claim': 'CORROBORATED',
            'sitting_date_claim': 'SECONDARY_CLAIMED',
            'official_occurrence_claim': 'NOT_ESTABLISHED',
        }
        for r in sorted(rs, key=lambda x: (x['sitting_date_claim'], x['printed_qno'])):
            sitting = r['sitting_date_claim']
            # Identity comes from governed attributes. printed_qno, not
            # page_ordinal: the research layer's page_ordinal collides three
            # times, because two entities can be scraped at one index.
            oid = M.occurrence_id(eid, r['set_id'], r['printed_qno'])
            occurrences.append({
                'occurrence_id': oid,
                'entity_id': eid,
                'evidence_band': 'HISTORICAL_SECONDARY_ARCHIVE',
                'sitting': sitting,
                'set_id': r['set_id'],
                'ordinal': r['printed_qno'],
                'limb': None,
                'limb_state': ('REQUIRES_LIMB_ADJUDICATION'
                               if r.get('limb_labels_detected') else 'WHOLE_QUESTION_ONLY'),
                'limb_markers_detected': r.get('limb_labels_detected') or [],
                'date_certainty': 'SECONDARY_CLAIMED',
                'source_class': 'SECONDARY_REPOSITORY_VIA_ARCHIVE',
                'provenance': {
                    'source_id': r['source_id'],
                    'research_ref': RESEARCH_REF,
                    'research_sha': RESEARCH_SHA,
                    'native_occurrence_id': r['occurrence_id'],
                },
                'counts_toward_recurrence': True,
            })
    return entities, occurrences


def load_wording_only(solved_ids):
    """2021-2023 held source copies. Questions already solved are NOT re-emitted:
    the same sitting and the same question is one occurrence, not two."""
    path = os.path.join(REPO, 'meoclass1', 'pastpapers', 'intelligence',
                        'historical_qp_intelligence.json')
    with open(path, encoding='utf-8') as fh:
        doc = json.load(fh)
    entities, occurrences, suppressed = {}, [], []
    for p in doc['papers']:
        sitting = '%d-%02d' % (p['year'], p['month_num'])
        for q in p['questions']:
            qid = q['question_id']
            if qid in solved_ids:
                suppressed.append(qid)
                continue
            eid = M.entity_id('MIW_WORDING_ONLY', qid)
            entities[eid] = {
                'entity_id': eid,
                'evidence_band': 'MIW_WORDING_ONLY',
                'native_id': qid,
                'stem': q['text_verbatim'],
                'stem_variants': [],
                'stem_scope': 'AS_PRINTED_IN_THIS_SITTING',
                'question_text_claim': 'HELD_SOURCE_COPY',
                'sitting_date_claim': 'PRINTED_ON_SOURCE_COPY',
                'official_occurrence_claim': 'NOT_INDEPENDENTLY_VERIFIED',
                'host_recurrence_annotation': q.get('host_recurrence_hint') or [],
            }
            occurrences.append({
                'occurrence_id': M.occurrence_id(eid, p['paper_id'], q['q_no']),
                'entity_id': eid,
                'evidence_band': 'MIW_WORDING_ONLY',
                'sitting': sitting,
                'set_id': p['paper_id'],
                'ordinal': q['q_no'],
                'limb': None,
                'limb_state': ('REQUIRES_LIMB_ADJUDICATION'
                               if q.get('printed_limbs') else 'WHOLE_QUESTION_ONLY'),
                'limb_markers_detected': q.get('printed_limbs') or [],
                'date_certainty': 'PRINTED_ON_SOURCE_COPY',
                'source_class': 'MIW_HELD_SOURCE_COPY',
                'provenance': {'held_source_pages': p.get('source_pages')},
                'counts_toward_recurrence': True,
            })
    return entities, occurrences, sorted(suppressed)


def load_solved():
    """2023-2026 governed specs. Printed subparts are real limbs and are recorded
    as GOVERNED_LIMB occurrences alongside the whole-question occurrence -- two
    records against one question, never one record counted twice."""
    entities, occurrences, limb_occ = {}, [], []
    for path in sorted(glob.glob(os.path.join(REPO, 'meoclass1', 'pastpapers', 'specs', '*.json'))):
        with open(path, encoding='utf-8') as fh:
            spec = json.load(fh)
        sitting = '%d-%02d' % (spec['year'], MONTHS[spec['month']])
        for q in spec['questions']:
            qid = '%s-%s' % (spec['paper_id'], q['q_no'])
            eid = M.entity_id('MIW_SOLVED_CANONICAL', qid)
            # Spec schema drift: papers authored before schema 1.3 label a
            # subpart with `ref`, later ones with `label`. Reading only one of
            # them silently drops 249 of the 260 questions that print limbs, so
            # the limb layer would look empty rather than broken.
            subparts = [dict(sp, label=(sp.get('label') or sp.get('ref')))
                        for sp in (q.get('subparts') or [])]
            entities[eid] = {
                'entity_id': eid,
                'evidence_band': 'MIW_SOLVED_CANONICAL',
                'native_id': qid,
                'stem': q['text_verbatim'],
                'stem_variants': [],
                'stem_scope': 'AS_PRINTED_IN_THIS_SITTING',
                'question_text_claim': 'GOVERNED_CANONICAL',
                'sitting_date_claim': 'PRINTED_ON_SOURCE_COPY',
                'official_occurrence_claim': 'NOT_INDEPENDENTLY_VERIFIED',
                'total_marks': q.get('total_marks'),
                'topic_tags': q.get('topic_tags') or [],
                'printed_limbs': [sp.get('label') for sp in subparts],
                'host_recurrence_annotation': q.get('host_recurrence_hint') or [],
                'has_model_answer': True,
            }
            occurrences.append({
                'occurrence_id': M.occurrence_id(eid, spec['paper_id'], q['q_no']),
                'entity_id': eid,
                'evidence_band': 'MIW_SOLVED_CANONICAL',
                'sitting': sitting,
                'set_id': spec['paper_id'],
                'ordinal': q['q_no'],
                'limb': None,
                'limb_state': 'WHOLE_QUESTION_ONLY' if not subparts else 'STRUCTURAL_LIMB_ONLY',
                'limb_markers_detected': [sp.get('label') for sp in subparts],
                'date_certainty': 'PRINTED_ON_SOURCE_COPY',
                'source_class': 'MIW_GOVERNED_SPEC',
                'provenance': {'spec': os.path.relpath(path, REPO).replace('\\', '/')},
                'counts_toward_recurrence': True,
            })
            for sp in subparts:
                if not sp.get('label'):
                    continue
                limb_occ.append({
                    'occurrence_id': M.occurrence_id(eid, spec['paper_id'], q['q_no'], sp['label']),
                    'entity_id': eid,
                    'evidence_band': 'MIW_SOLVED_CANONICAL',
                    'sitting': sitting,
                    'set_id': spec['paper_id'],
                    'ordinal': q['q_no'],
                    'limb': sp['label'],
                    'limb_state': 'GOVERNED_LIMB',
                    'limb_text': sp.get('text'),
                    'limb_marks': sp.get('marks'),
                    'date_certainty': 'PRINTED_ON_SOURCE_COPY',
                    'source_class': 'MIW_GOVERNED_SPEC',
                    'provenance': {'spec': os.path.relpath(path, REPO).replace('\\', '/')},
                    'counts_toward_recurrence': False,
                    'counts_toward_recurrence_note': (
                        'A printed limb is recorded so that limb-level recurrence '
                        'is expressible, and is NOT counted in whole-question '
                        'totals. It becomes countable only when a limb family is '
                        'adjudicated onto it.'),
                })
    return entities, occurrences, limb_occ


# --------------------------------------------------------------------------
# 2. FAMILIES -- proposals from qi_similarity, decisions from the adjudications.
# --------------------------------------------------------------------------

def build_families(entities, occurrences, adj):
    texts = {eid: e['stem'] for eid, e in entities.items()}
    proposals = S.candidate_pairs(texts)

    digest = hashlib.sha256(json.dumps(
        [[p['a'], p['b'], p['proposal']] for p in proposals],
        sort_keys=True).encode('utf-8')).hexdigest()

    pinned = adj.get('reviewed_proposal_digest')
    if pinned and pinned != digest:
        raise BuildError(
            'proposal digest mismatch.\n'
            '  pinned  %s\n  computed %s\n'
            'The candidate set has changed since the semantic review, so the '
            'adjudications no longer describe what would be merged. Re-review the '
            'groups and re-pin, or revert the corpus change.' % (pinned, digest))

    groups = S.connected_components(proposals)
    grouped = {m for g in groups for m in g}
    for eid in sorted(entities):
        if eid not in grouped:
            groups.append([eid])
    groups.sort(key=lambda g: g[0])

    # Apply the forced splits. Expressed in entity ids so they survive any
    # renumbering of the proposal groups.
    applied = []
    for split in adj.get('forced_splits', []):
        parts = [set(p) for p in split['partitions']]
        members = set().union(*parts)
        hit = [g for g in groups if members & set(g)]
        if not hit:
            raise BuildError(
                '%s names entities that are in no group: %s. A recorded split '
                'that matches nothing means the corpus moved under the review.'
                % (split['split_id'], sorted(members)))
        for g in hit:
            groups.remove(g)
            leftover = [m for m in g if m not in members]
            for part in parts:
                seg = sorted(part & set(g))
                if seg:
                    groups.append(seg)
            if leftover:
                groups.append(sorted(leftover))
        applied.append(split['split_id'])
        groups.sort(key=lambda g: g[0])

    missing = [s['split_id'] for s in adj.get('forced_splits', [])
               if s['split_id'] not in applied]
    if missing:
        raise BuildError('forced splits never applied: %s' % missing)

    occ_by_entity = defaultdict(list)
    for o in occurrences:
        if o['counts_toward_recurrence']:
            occ_by_entity[o['entity_id']].append(o)

    families, no_value = [], []
    seq = 0
    for g in sorted(groups, key=lambda g: (-sum(len(occ_by_entity[m]) for m in g), g[0])):
        occs = [o for m in g for o in occ_by_entity[m]]
        if len(occs) < M.MATERIALLY_RECURRENT_MIN_OCCURRENCES:
            no_value.extend(g)
            continue
        seq += 1
        fid = M.family_id(seq)
        occs.sort(key=lambda o: (o['sitting'], o['occurrence_id']))
        anchor = max(g, key=lambda m: (len(occ_by_entity[m]),
                                       entities[m]['evidence_band'] == 'MIW_SOLVED_CANONICAL',
                                       m))
        # The ANCHOR is the member carrying the most occurrences -- that is a
        # recurrence fact. The LABEL is a display string, and it should come
        # from the cleanest text available: the archived 2010-2020 wording was
        # scraped through a lossy encoding and carries replacement characters,
        # so a modern member's stem reads better while meaning the same thing.
        band_rank = {'MIW_SOLVED_CANONICAL': 0, 'MIW_WORDING_ONLY': 1,
                     'HISTORICAL_SECONDARY_ARCHIVE': 2}
        label_src = min(g, key=lambda m: (band_rank[entities[m]['evidence_band']],
                                          '�' in entities[m]['stem'], m))
        families.append({
            'family_id': fid,
            'label': _label(entities[label_src]['stem']),
            'label_source_entity': label_src,
            'anchor_entity': anchor,
            'member_entities': sorted(g),
            'unit': 'WHOLE_QUESTION',
            'occurrence_ids': [o['occurrence_id'] for o in occs],
            'sittings': sorted({o['sitting'] for o in occs}),
            'evidence_breakdown': dict(Counter(o['evidence_band'] for o in occs)),
            'variant_count': len(g),
            'join_verdict': 'SAME_FAMILY' if len(g) == 1 else 'SAME_FAMILY_VARIANT',
        })
    return families, proposals, digest, sorted(set(no_value))


def _label(stem, limit=110):
    s = ' '.join(stem.split())
    s = s.lstrip('Qq0123456789.) ')
    return s[:limit].rstrip() + ('...' if len(s) > limit else '')


def build_joins(families, proposals, adj, entities):
    """Relations between families. A relation transfers NO occurrence."""
    owner = {}
    for f in families:
        for m in f['member_entities']:
            owner[m] = f['family_id']

    split_pairs = {}
    for split in adj.get('forced_splits', []):
        parts = split['partitions']
        for i in range(len(parts)):
            for j in range(i + 1, len(parts)):
                for a in parts[i]:
                    for b in parts[j]:
                        split_pairs[tuple(sorted((a, b)))] = split

    joins, seen = [], set()
    for p in proposals:
        fa, fb = owner.get(p['a']), owner.get(p['b'])
        if not fa or not fb or fa == fb:
            continue
        key = tuple(sorted((fa, fb)))
        forced = split_pairs.get(tuple(sorted((p['a'], p['b']))))
        if forced:
            verdict = forced['verdict']
            reason = forced['reason']
            source = forced['split_id']
        elif p['containment_low'] >= S.MERGE_THRESHOLD:
            continue  # already merged, or split-handled above
        else:
            verdict = 'WHOLE_VS_LIMB_RELATION' if p['containment_high'] >= 0.75 else 'RELATED_BUT_DISTINCT'
            reason = ('Asymmetric containment: one stem is largely contained in '
                      'the other while the reverse is not. Recorded as a relation '
                      'so the smaller unit can never lend its sitting count to the '
                      'larger.')
            source = 'DERIVED_ASYMMETRY'
        if key in seen:
            continue
        seen.add(key)
        joins.append({
            'join_id': 'QIJ-%04d' % (len(joins) + 1),
            'family_a': key[0],
            'family_b': key[1],
            'verdict': verdict,
            'transfers_occurrences': False,
            'containment_high': p['containment_high'],
            'containment_low': p['containment_low'],
            'adjudication_source': source,
            'reason': reason,
        })
    return joins


# --------------------------------------------------------------------------
# 3. COVERAGE -- absence of a page is never absence of an exam.
# --------------------------------------------------------------------------

def _governed_month_gaps():
    """The 2010-2020 absent months, and what each absence actually means.

    Read from `docs/study/historical_source_layer.json` -- the governed adoption
    record on main -- rather than from the research branch, because the
    classification of an absence is an adjudication and adjudications live on
    main. Three distinct things hide inside "17 months have no paper", and only
    one of them is an acquisition failure.
    """
    path = os.path.join(REPO, 'docs', 'study', 'historical_source_layer.json')
    with open(path, encoding='utf-8') as fh:
        layer = json.load(fh)

    expanded = {}
    mays = ['%d-05' % y for y in range(2010, 2020)]
    covid = ['2020-%02d' % m for m in range(4, 10)]
    spec = [
        (mays, 'NO_SOURCE_PAGE_FOUND', 'INFERRED_NOT_EVIDENCED'),
        (covid, 'NO_SOURCE_PAGE_FOUND', 'EXTERNALLY_PLAUSIBLE_NOT_EVIDENCED'),
        (['2010-09'], 'NO_ARCHIVE_CAPTURE', 'SITTING_SOURCE_PAGE_KNOWN_TO_EXIST'),
    ]
    declared = layer.get('month_gaps') or []
    if len(declared) != len(spec):
        raise BuildError(
            'historical_source_layer.json declares %d month-gap groups, this '
            'builder expands %d. The adjudicated meaning of an absent month has '
            'changed and the coverage matrix must be re-derived against it, not '
            'guessed.' % (len(declared), len(spec)))
    for (months, state, evidence), rec in zip(spec, declared):
        if rec.get('classification') == 'NO_ARCHIVE_CAPTURE' and state != 'NO_ARCHIVE_CAPTURE':
            raise BuildError('month-gap groups reordered in historical_source_layer.json')
        for mo in months:
            expanded[mo] = {
                'coverage_state': state,
                'no_sitting_evidence': evidence,
                'detail': rec.get('detail'),
                'governed_by': 'docs/study/historical_source_layer.json',
            }
    return expanded


def build_coverage(entities, occurrences, adj):
    known_gaps = _governed_month_gaps()

    held = defaultdict(list)
    for o in occurrences:
        if o['counts_toward_recurrence']:
            held[o['sitting']].append(o)

    months = []
    y, m = 2010, 1
    while ('%04d-%02d' % (y, m)) <= M.QI_UPPER_BOUNDARY:
        months.append('%04d-%02d' % (y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1

    rows = []
    for mo in months:
        occ = held.get(mo, [])
        year = int(mo[:4])
        gap = known_gaps.get(mo)
        if occ:
            state = 'SOURCE_PRESENT'
            evidence = None
        elif gap:
            state = gap['coverage_state']
            evidence = gap['no_sitting_evidence']
        else:
            state = 'NO_SOURCE_PAGE_FOUND'
            evidence = 'NOT_ASSESSED'
        rows.append({
            'sitting': mo,
            'year': year,
            'coverage_state': state,
            'no_sitting_evidence': evidence,
            'gap_detail': (gap or {}).get('detail'),
            'counts_as_zero_question_sitting': state == 'NO_EXAM_OFFICIALLY_EVIDENCED',
            'occurrences': len(occ),
            'distinct_entities': len({o['entity_id'] for o in occ}),
            'sets': sorted({o['set_id'] for o in occ}),
            'evidence_bands': sorted({o['evidence_band'] for o in occ}),
        })

    per_year = []
    for year in range(2010, 2027):
        yr = [r for r in rows if r['year'] == year]
        yocc = [o for o in occurrences
                if o['counts_toward_recurrence'] and int(o['sitting'][:4]) == year]
        per_year.append({
            'year': year,
            'months_in_horizon': len(yr),
            'sitting_months_with_source': sum(1 for r in yr if r['coverage_state'] == 'SOURCE_PRESENT'),
            'months_no_source_page_found': sum(1 for r in yr if r['coverage_state'] == 'NO_SOURCE_PAGE_FOUND'),
            'months_no_archive_capture': sum(1 for r in yr if r['coverage_state'] == 'NO_ARCHIVE_CAPTURE'),
            'months_no_exam_officially_evidenced': sum(1 for r in yr if r['coverage_state'] == 'NO_EXAM_OFFICIALLY_EVIDENCED'),
            'sets': sorted({o['set_id'] for o in yocc}),
            'source_pages_or_papers': len({o['set_id'] for o in yocc}),
            'occurrences': len(yocc),
            'distinct_entities': len({o['entity_id'] for o in yocc}),
            'evidence_bands': dict(Counter(o['evidence_band'] for o in yocc)),
            'date_confidence': dict(Counter(o['date_certainty'] for o in yocc)),
            'source_confidence': dict(Counter(o['source_class'] for o in yocc)),
        })
    return rows, per_year


# --------------------------------------------------------------------------
# 4. TIME WINDOWS, LABELS, RE-EMERGENCE.
# --------------------------------------------------------------------------

def _calendar_observation(rows):
    """What the coverage matrix says about the sitting calendar itself.

    The 2010-2020 research inferred "no May sitting exists" from one secondary
    index, and the prior adoption decision correctly refused to promote that
    inference to evidence. The modern bands settle it a different way: MIW holds
    its own source copies for 2021-2026 and there is no May paper among them
    either. Two independent bodies of evidence, one of them MIW's own, now agree.
    That is corroboration, not proof -- and it is why this stays an observation
    rather than becoming NO_EXAM_OFFICIALLY_EVIDENCED.
    """
    by_month = defaultdict(lambda: {'present': 0, 'absent': 0})
    for r in rows:
        key = r['sitting'][5:]
        by_month[key]['present' if r['coverage_state'] == 'SOURCE_PRESENT' else 'absent'] += 1
    never = sorted(k for k, v in by_month.items() if v['present'] == 0)
    return {
        'calendar_months_never_evidenced': never,
        'per_calendar_month': {k: dict(v) for k, v in sorted(by_month.items())},
        'finding': (
            'May is absent in every one of the 17 years in the horizon, across '
            'all three evidence bands. The 2010-2020 absence rests on one '
            'secondary index; the 2021-2026 absence rests on MIW holding its own '
            'source copy of every other month and none for May. Two independent '
            'lines now agree.'),
        'status': 'CORROBORATED_INFERENCE_NOT_OFFICIAL_EVIDENCE',
        'consequence': (
            'These months remain UNKNOWN in the coverage matrix and are excluded '
            'from recurrence denominators. They do NOT become confirmed '
            'zero-question sittings: that would require an official instrument '
            'stating no examination was held, and none is held.'),
    }


def build_metrics(families, occurrences):
    by_id = {o['occurrence_id']: o for o in occurrences}
    out = []
    for f in families:
        occ = [by_id[i] for i in f['occurrence_ids']]
        sits = sorted({o['sitting'] for o in occ})
        years = sorted({int(s[:4]) for s in sits})
        counts = {w: sum(1 for o in occ if M.in_window(o['sitting'], w))
                  for w in M.RECURRENCE_WINDOWS}
        gaps = [M.months_between(sits[i], sits[i + 1]) for i in range(len(sits) - 1)]
        meaningful = [g for g in gaps if g >= M.DORMANCY_GAP_MONTHS]
        span = M.months_between(sits[0], sits[-1])

        # ONE label engine, in qi_model. The projection layer calls the same
        # function over the printed-evidence-only subset; see its docstring.
        labels = M.intelligence_labels([o['sitting'] for o in occ])

        out.append({
            'family_id': f['family_id'],
            'label': f['label'],
            'total_occurrences': len(occ),
            'distinct_sittings': len(sits),
            'distinct_years': len(years),
            'years': years,
            'first_sitting': sits[0],
            'last_sitting': sits[-1],
            'span_months': span,
            'count_3y': counts['RECENT_3Y'],
            'count_5y': counts['RECENT_5Y'],
            'count_10y': counts['MEDIUM_10Y'],
            'count_full_horizon': counts['FULL_HORIZON'],
            'recent_spread_sittings_5y': len({o['sitting'] for o in occ if M.in_window(o['sitting'], 'RECENT_5Y')}),
            'long_term_spread_years': len(years),
            'gaps_months': gaps,
            'meaningful_gaps_months': meaningful,
            'largest_gap_months': max(gaps) if gaps else 0,
            'evidence_breakdown': f['evidence_breakdown'],
            'intelligence_labels': labels,
        })
    out.sort(key=lambda r: (-r['total_occurrences'], r['family_id']))
    return out


# --------------------------------------------------------------------------
# 5. CURRENTNESS TRIAGE -- flags only. Nothing here moves a recurrence count.
# --------------------------------------------------------------------------

def build_currentness(families, entities, metrics):
    mm = {m['family_id']: m for m in metrics}
    out = []
    for f in families:
        stems = ' '.join(entities[e]['stem'] for e in f['member_entities']).lower()
        tr = sorted({t for t in M.TIME_RELATIVE_TRIGGERS if t in stems})
        fw = sorted({t for t in M.FRAMEWORK_CHANGE_TRIGGERS if t in stems})
        m = mm[f['family_id']]

        if tr:
            status = 'CURRENTNESS_REVIEW_REQUIRED'
            why = ('Time-relative language. The stem asks for what is current '
                   'without naming an instrument, so its correct answer moves '
                   'with the calendar and no instrument-name check can see it.')
        elif fw and m['count_3y'] >= 1:
            status = 'CURRENT_WITH_AMENDMENT'
            why = ('Names a framework that moved inside the horizon and was still '
                   'set within the last three years.')
        elif fw:
            status = 'CURRENT_FRAMEWORK_CHANGED'
            why = ('Names a framework that moved inside the horizon and has not '
                   'been set in the last three years.')
        elif 'HISTORICAL_ONLY' in m['intelligence_labels']:
            status = 'HISTORICAL_ONLY'
            why = 'Every occurrence lies in the 2010-2020 band and no framework trigger fires.'
        else:
            status = 'UNKNOWN'
            why = ('No currentness signal fires. UNKNOWN is not CURRENT: it means '
                   'nobody has checked.')

        out.append({
            'family_id': f['family_id'],
            'label': f['label'],
            'currentness_status': status,
            'time_relative_flags': tr,
            'framework_change_flags': fw,
            'reason': why,
            'affects_recurrence_count': False,
            'phase': 'TRIAGE_ONLY -- no authority research performed, no answer rewritten',
        })
    return out


# --------------------------------------------------------------------------
# 6. PHASE-2 ACTION QUEUE.
# --------------------------------------------------------------------------

def build_queue(families, entities, metrics, currentness, occurrences):
    mm = {m['family_id']: m for m in metrics}
    cc = {c['family_id']: c for c in currentness}
    by_id = {o['occurrence_id']: o for o in occurrences}
    rows = []
    for f in families:
        m, c = mm[f['family_id']], cc[f['family_id']]
        solved = [e for e in f['member_entities']
                  if entities[e]['evidence_band'] == 'MIW_SOLVED_CANONICAL']

        if not solved:
            answer = ('HISTORICAL_ONLY' if 'HISTORICAL_ONLY' in m['intelligence_labels']
                      else 'NO_CURRENT_SOLVED_ANSWER')
        elif c['currentness_status'] in ('CURRENT_WITH_AMENDMENT', 'CURRENT_FRAMEWORK_CHANGED',
                                        'CURRENTNESS_REVIEW_REQUIRED'):
            answer = 'SOLVED_BUT_CURRENTNESS_UNVERIFIED'
        elif len(solved) > 1:
            answer = 'MULTIPLE_CANDIDATE_ANSWERS'
        else:
            answer = 'SOLVED_CURRENT_CANDIDATE'

        if c['currentness_status'] == 'CURRENTNESS_REVIEW_REQUIRED':
            action = ('EXISTING_CURRENT_ANSWER_VERIFY' if solved
                      else 'CURRENTNESS_RESEARCH_REQUIRED')
        elif not solved and 'HISTORICAL_ONLY' in m['intelligence_labels']:
            action = 'LOW_PRIORITY_HISTORICAL_ONLY'
        elif not solved:
            action = 'NEW_MODERN_ANSWER_REQUIRED'
        elif c['currentness_status'] == 'CURRENT_FRAMEWORK_CHANGED':
            action = 'HISTORICAL_ANSWER_REQUIRES_MODERNISATION'
        elif c['currentness_status'] == 'CURRENT_WITH_AMENDMENT':
            action = 'EXISTING_CURRENT_ANSWER_VERIFY'
        elif c['currentness_status'] == 'LIKELY_SUPERSEDED':
            action = 'SUPERSEDED_MODERN_REPLACEMENT_REQUIRED'
        else:
            action = 'CURRENT_AND_SOLVED'

        if action == 'NEW_MODERN_ANSWER_REQUIRED':
            mq = 'CREATE_NEW_CURRENT_CANONICAL_QUESTION'
        elif action == 'LOW_PRIORITY_HISTORICAL_ONLY':
            mq = 'HISTORICAL_ONLY_NO_MODERN_QUESTION'
        elif action == 'HISTORICAL_ANSWER_REQUIRES_MODERNISATION':
            mq = 'MODERNISE_CANONICAL_QUESTION'
        elif answer == 'MULTIPLE_CANDIDATE_ANSWERS':
            mq = 'MERGE_VARIANTS'
        else:
            mq = 'USE_EXISTING_CANONICAL_QUESTION'

        # Priority. Recency and current examinability outrank raw historical bulk
        # on purpose: old + frequent + obsolete must never outrank recent +
        # recurrent + live.
        pri = 0.0
        pri += 6.0 * min(m['count_3y'], 4)
        pri += 2.5 * min(m['count_5y'], 6)
        pri += 1.0 * min(m['count_10y'], 8)
        pri += 0.35 * min(m['count_full_horizon'], 20)
        pri += 2.0 * min(m['distinct_years'], 8)
        if 'RE_EMERGING' in m['intelligence_labels']:
            pri += 5.0
        if 'RISING' in m['intelligence_labels']:
            pri += 4.0
        if c['currentness_status'] == 'CURRENTNESS_REVIEW_REQUIRED':
            pri += 9.0
        if answer in ('NO_CURRENT_SOLVED_ANSWER',):
            pri += 7.0
        if 'HISTORICAL_ONLY' in m['intelligence_labels']:
            pri -= 14.0
        if 'DORMANT' in m['intelligence_labels']:
            pri -= 5.0

        topics = sorted({t for e in f['member_entities'] for t in (entities[e].get('topic_tags') or [])})
        limb_members = sorted({by_id[o]['limb'] for o in f['occurrence_ids'] if by_id[o]['limb']})

        rows.append({
            'family_id': f['family_id'],
            'label': f['label'],
            'topic_tags': topics[:8],
            'first_sitting': m['first_sitting'],
            'last_sitting': m['last_sitting'],
            'count_3y': m['count_3y'],
            'count_5y': m['count_5y'],
            'count_10y': m['count_10y'],
            'count_full_horizon': m['count_full_horizon'],
            'distinct_years': m['distinct_years'],
            'distinct_sittings': m['distinct_sittings'],
            'historical_variants': m['evidence_breakdown'].get('HISTORICAL_SECONDARY_ARCHIVE', 0),
            'unit': f['unit'],
            'limb_units_held': limb_members,
            'evidence_strength_breakdown': m['evidence_breakdown'],
            'intelligence_labels': m['intelligence_labels'],
            'currentness_status': c['currentness_status'],
            'time_relative_flags': c['time_relative_flags'],
            'existing_answer_status': answer,
            'modern_question_action': mq,
            'phase2_action': action,
            'phase2_priority': round(pri, 2),
            'reason': _queue_reason(m, c, answer, action),
        })
    rows.sort(key=lambda r: (-r['phase2_priority'], r['family_id']))
    for i, r in enumerate(rows, 1):
        r['phase2_rank'] = i
    return rows


def _queue_reason(m, c, answer, action):
    bits = ['%d occurrences across %d sittings in %d distinct years (%s to %s)'
            % (m['total_occurrences'], m['distinct_sittings'], m['distinct_years'],
               m['first_sitting'], m['last_sitting'])]
    if m['count_3y']:
        bits.append('%d inside the last three years' % m['count_3y'])
    else:
        bits.append('nothing in the last three years')
    if 'RE_EMERGING' in m['intelligence_labels']:
        bits.append('returned after a %d-month gap' % m['largest_gap_months'])
    if c['time_relative_flags']:
        bits.append('time-relative stem (%s)' % ', '.join(c['time_relative_flags'][:3]))
    bits.append(answer.replace('_', ' ').lower())
    return '; '.join(bits) + '.'


# --------------------------------------------------------------------------
# WRITE
# --------------------------------------------------------------------------

def _header(name, what):
    return {
        'schema': 'miw.study.qi.%s.v1' % name,
        'schema_version': M.SCHEMA_VERSION,
        'generated_by': 'tools/study/build_qi.py',
        'hand_editable': False,
        'what_this_is': what,
        'horizon': {
            'lower_boundary': M.QI_LOWER_BOUNDARY,
            'upper_boundary': M.QI_UPPER_BOUNDARY,
            'language': M.HORIZON_LANGUAGE,
            'rationale': M.QI_HORIZON_RATIONALE,
        },
    }


def main(argv):
    check = '--check' in argv
    with open(ADJ_PATH, encoding='utf-8') as fh:
        adj = json.load(fh)

    solved_entities, solved_occ, limb_occ = load_solved()
    solved_ids = {e['native_id'] for e in solved_entities.values()}
    word_entities, word_occ, suppressed = load_wording_only(solved_ids)
    hist_entities, hist_occ = load_historical()

    entities = {}
    entities.update(hist_entities)
    entities.update(word_entities)
    entities.update(solved_entities)
    occurrences = hist_occ + word_occ + solved_occ
    occurrences.sort(key=lambda o: (o['sitting'], o['set_id'], str(o['ordinal']), o['occurrence_id']))
    all_records = occurrences + sorted(limb_occ, key=lambda o: o['occurrence_id'])

    for o in all_records:
        v = M.horizon_violation(o['sitting'])
        if v:
            raise BuildError('%s on %s (%s)' % (v, o['occurrence_id'], o['sitting']))

    families, proposals, digest, no_value = build_families(entities, occurrences, adj)
    joins = build_joins(families, proposals, adj, entities)
    cov_rows, cov_years = build_coverage(entities, occurrences, adj)
    metrics = build_metrics(families, occurrences)
    currentness = build_currentness(families, entities, metrics)
    queue = build_queue(families, entities, metrics, currentness, all_records)

    files = {}

    files['qi_source_entities.json'] = dict(_header(
        'source_entities',
        'Every distinct question entity across all three evidence bands. An '
        'entity is a QUESTION; the sittings it appears in are occurrences and '
        'live in qi_occurrences.json. One entity appearing on nine source pages '
        'is one entity, not nine questions.'), **{
        'counts': {
            'total': len(entities),
            'by_band': dict(Counter(e['evidence_band'] for e in entities.values())),
        },
        'claim_separation': {
            'question_text_claim': dict(Counter(e['question_text_claim'] for e in entities.values())),
            'sitting_date_claim': dict(Counter(e['sitting_date_claim'] for e in entities.values())),
            'official_occurrence_claim': dict(Counter(e['official_occurrence_claim'] for e in entities.values())),
            'rule': 'Never collapsed into verified=true. See qi_model.EVIDENCE_BANDS.',
        },
        'entities': [entities[k] for k in sorted(entities)],
    })

    files['qi_occurrences.json'] = dict(_header(
        'occurrences',
        'One record per (entity, sitting) observation, plus one record per '
        'printed limb of a solved question. Identity is derived from governed '
        'attributes and never from wording: two sittings printing identical '
        'wording are two occurrences.'), **{
        'counts': {
            'recurrence_bearing': len(occurrences),
            'limb_records_not_counted': len(limb_occ),
            'total_records': len(all_records),
            'by_band': dict(Counter(o['evidence_band'] for o in occurrences)),
            'by_date_certainty': dict(Counter(o['date_certainty'] for o in occurrences)),
            'by_limb_state': dict(Counter(o['limb_state'] for o in all_records)),
        },
        'suppressed_duplicate_question_ids': {
            'count': len(suppressed),
            'why': ('These question ids exist in BOTH the 2021-2023 held-copy band '
                    'and the solved band -- the same sitting and the same question, '
                    'held twice. Emitting both would have counted 72 questions '
                    'twice and inflated every 2023 recurrence measure. The solved '
                    'record wins; the wording-only copy is suppressed here.'),
            'question_ids': suppressed,
        },
        'non_occurrence_evidence': M.NON_OCCURRENCE_EVIDENCE,
        'occurrences': all_records,
    })

    files['qi_families.json'] = dict(_header(
        'families',
        'Governed recurrence families. A family is a set of entities sharing one '
        'examinable answer core, carrying at least two governed occurrences.'), **{
        'counts': {
            'families': len(families),
            'entities_in_families': sum(len(f['member_entities']) for f in families),
            'entities_with_no_recurrence_value': len(no_value),
        },
        'formation': {
            'proposed_by': 'tools/study/qi_similarity.py',
            'decided_by': 'tools/study/qi_phase1_adjudications.json',
            'merge_threshold_containment_low': S.MERGE_THRESHOLD,
            'rule': ('The merge threshold is applied to the LOW containment only. '
                     'A pair that is high one way and low the other is a subset -- '
                     'usually a limb -- and is recorded as a relation, never merged.'),
            'proposal_digest': digest,
        },
        'no_recurrence_value_entities': no_value,
        'families': families,
    })

    files['qi_family_joins.json'] = dict(_header(
        'family_joins',
        'Relations BETWEEN families. Every relation transfers zero occurrences. '
        'This is the file that keeps a limb family from lending its sitting '
        'count to the whole question it sits inside.'), **{
        'counts': {
            'joins': len(joins),
            'by_verdict': dict(Counter(j['verdict'] for j in joins)),
        },
        'verdict_vocabulary': M.JOIN_VERDICTS,
        'limb_rule': M.LIMB_RULE,
        'joins': joins,
    })

    files['qi_coverage_matrix.json'] = dict(_header(
        'coverage_matrix',
        'Every month from 2010-01 to 2026-08 and what MIW holds for it. A month '
        'with no source page is UNKNOWN, never a zero-question sitting.'), **{
        'zero_denominator_rule': M.ZERO_DENOMINATOR_RULE,
        'coverage_states': M.COVERAGE_STATES,
        'summary': {
            'months_in_horizon': len(cov_rows),
            'by_state': dict(Counter(r['coverage_state'] for r in cov_rows)),
            'confirmed_no_exam_periods': [r['sitting'] for r in cov_rows
                                          if r['coverage_state'] == 'NO_EXAM_OFFICIALLY_EVIDENCED'],
            'unknown_months': [r['sitting'] for r in cov_rows
                               if r['coverage_state'] in ('NO_SOURCE_PAGE_FOUND', 'NO_ARCHIVE_CAPTURE', 'UNKNOWN')],
        },
        'calendar_observation': _calendar_observation(cov_rows),
        'per_year': cov_years,
        'per_month': cov_rows,
    })

    files['qi_time_window_metrics.json'] = dict(_header(
        'time_window_metrics',
        'Raw recurrence measures per family, before any composite score. 3Y, 5Y, '
        '10Y and full-horizon counts, distinct sittings, distinct years, gaps.'), **{
        'windows': {k: {'from': v[0], 'to': v[1]} for k, v in M.RECURRENCE_WINDOWS.items()},
        'labels': M.INTELLIGENCE_LABELS,
        'multidimensional_rule': M.MULTIDIMENSIONAL_RULE,
        'dormancy_rule': M.DORMANCY_RULE,
        'horizon_language': M.HORIZON_ELAPSED_NOTE,
        'label_totals': dict(Counter(l for m in metrics for l in m['intelligence_labels'])),
        'window_totals': {
            'families_with_3y_activity': sum(1 for m in metrics if m['count_3y']),
            'families_with_5y_activity': sum(1 for m in metrics if m['count_5y']),
            'families_with_10y_activity': sum(1 for m in metrics if m['count_10y']),
            'families_with_full_horizon_activity': sum(1 for m in metrics if m['count_full_horizon']),
        },
        'families': metrics,
    })

    files['qi_currentness.json'] = dict(_header(
        'currentness',
        'Currentness TRIAGE. Whether the answer would still be right today, '
        'which is a different question from whether the question keeps coming '
        'back. No authority research was performed and no answer was rewritten.'), **{
        'invariant': M.CURRENTNESS_INVARIANT,
        'classes': M.CURRENTNESS_CLASSES,
        'time_relative_triggers': M.TIME_RELATIVE_TRIGGERS,
        'totals': dict(Counter(c['currentness_status'] for c in currentness)),
        'time_relative_flagged_families': sum(1 for c in currentness if c['time_relative_flags']),
        'families': currentness,
    })

    files['qi_phase2_action_queue.json'] = dict(_header(
        'phase2_action_queue',
        'The bridge out of Phase 1. Every materially recurrent family leaves '
        'with an action state and a transparent priority.'), **{
        'actions': M.PHASE2_ACTIONS,
        'modern_question_actions': M.MODERN_QUESTION_ACTIONS,
        'answer_coverage_states': M.ANSWER_COVERAGE_STATES,
        'priority_model': {
            'inputs': ['count_3y', 'count_5y', 'count_10y', 'count_full_horizon',
                       'distinct_years', 'RE_EMERGING', 'RISING',
                       'currentness risk', 'answer availability'],
            'rule': ('Recency and current examinability outrank historical bulk. '
                     'A family that is old, frequent and obsolete must never '
                     'outrank one that is recent, recurrent and still set.'),
        },
        'totals': dict(Counter(r['phase2_action'] for r in queue)),
        'modern_question_action_totals': dict(Counter(r['modern_question_action'] for r in queue)),
        'answer_status_totals': dict(Counter(r['existing_answer_status'] for r in queue)),
        'queue': queue,
    })

    os.makedirs(OUT_DIR, exist_ok=True)
    diffs = []
    for name, payload in files.items():
        path = os.path.join(OUT_DIR, name)
        text = json.dumps(payload, indent=1, ensure_ascii=False, sort_keys=False) + '\n'
        if check:
            existing = None
            if os.path.exists(path):
                with open(path, encoding='utf-8') as fh:
                    existing = fh.read()
            if existing != text:
                diffs.append(name)
        else:
            with open(path, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(text)

    if check:
        if diffs:
            print('STALE: %s' % ', '.join(sorted(diffs)))
            return 1
        print('build_qi --check: all %d QI projections match their inputs' % len(files))
        return 0

    if not adj.get('reviewed_proposal_digest'):
        print('NOTE: adjudication digest is UNPINNED. Pin it with:')
        print('      "reviewed_proposal_digest": "%s"' % digest)
    print('entities              %d' % len(entities))
    print('occurrences (counted) %d   (+%d limb records not counted)'
          % (len(occurrences), len(limb_occ)))
    print('families              %d' % len(families))
    print('family joins          %d' % len(joins))
    print('phase-2 queue         %d' % len(queue))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except BuildError as exc:
        print('BUILD FAILED: %s' % exc, file=sys.stderr)
        sys.exit(2)
