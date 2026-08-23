#!/usr/bin/env python3
"""Build the unified study-intelligence projection. The ONLY writer of
`docs/study/study_qi.json` and `docs/study/modern_qi_baseline.json`.

    existing modern QI (specs + sixyear derived)
    canonical longitudinal QI (docs/study/qi/*)
    governed study mappings
    hand-recorded holds (study_qi_holds.json)
                    |
            study_qi_adapter
                    |
            docs/study/study_qi.json      <- every consumer reads this

The baseline file is the regression guard. It records what modern
question-level intelligence existed BEFORE the longitudinal layer was allowed
anywhere near the study engine, so that a later change cannot quietly drop a
repeat tag, a related-question edge or a modern family and have nobody notice.
It is regenerated from the same sources every build, which is the point: if the
sources really did lose a record, the baseline shrinks and the validator --
which compares against the FROZEN copy committed alongside -- fails.

Usage
    python tools/study/build_study_qi.py            # write
    python tools/study/build_study_qi.py --check    # fail if disk is stale
"""

import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import study_qi_adapter as A
import study_spine as SP

REPO = A.REPO
DOC = A.DOC
OUT = os.path.join(DOC, 'study_qi.json')
BASELINE = os.path.join(DOC, 'modern_qi_baseline.json')
HOLDS = os.path.join(REPO, 'tools', 'study', 'study_qi_holds.json')

#: Files this builder must never write. Progress is durable user state and
#: priority work may not touch it (contract section 46).
PROTECTED = [
    'study_progress.json', 'study_sessions.json', 'study_mappings.json',
    'coverage_matrix.json',
]


class BuildError(Exception):
    pass


def _load(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def _dump(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=False) + '\n'


def build():
    modern = A.load_modern_qi()
    canonical = A.load_canonical_qi()
    mappings = _load(os.path.join(DOC, 'study_mappings.json'))['mappings']
    holds = _load(HOLDS)

    recon = A.reconcile(modern, canonical)
    corrob = A.authored_corroboration(modern, canonical)
    fam_rows = A.project_families(modern, canonical, mappings)
    q_rows = A.project_questions(modern, canonical, mappings, fam_rows)
    topics = A.project_topics(fam_rows, q_rows)
    roadmap = A.roadmap_recurrence(topics)

    # ---- apply the hand-recorded holds --------------------------------------
    conflict_holds = {h['modern_family_id']: h for h in holds['conflict_holds']}
    for row in recon:
        if row['verdict'] != 'CONFLICT':
            continue
        h = conflict_holds.get(row['modern_family_id'])
        if not h:
            raise BuildError(
                'CONFLICT on modern family %s carries no governed hold. Add one '
                'to tools/study/study_qi_holds.json -- a conflict that nobody '
                'has read must never be allowed to pass silently into the study '
                'engine.' % row['modern_family_id'])
        row['hold_id'] = h['hold_id']
        row['hold_state'] = h['state']
        row['hold_note'] = h['note']

    topic_holds = {h['family_id']: h for h in holds['topic_mapping_holds']}
    for row in fam_rows:
        if row['topic_reach'] == 'MODERN_MEMBER_PRESENT_BUT_UNMAPPED':
            h = topic_holds.get(row['family_id'])
            if not h:
                raise BuildError(
                    'family %s has a modern member and reaches no topic, and no '
                    'governed hold explains it.' % row['family_id'])
            row['topic_mapping_hold'] = h['state']
            row['topic_mapping_hold_id'] = h['hold_id']

    # ---- the regression baseline --------------------------------------------
    baseline = {
        'schema': 'miw.study.modern_qi_baseline.v1',
        'schema_version': A.SCHEMA_VERSION,
        'generated_by': 'tools/study/build_study_qi.py',
        'hand_editable': False,
        'what_this_is': (
            'The inventory of MIW existing 2021 -> August 2026 question-level '
            'question intelligence, as it stood when the 2010 -> August 2026 '
            'longitudinal layer was joined to the study engine. The validator '
            'compares the live corpus against this frozen record. A modern '
            'repeat tag, a related-question edge or a modern family that '
            'disappears without an explicit migration fails the gate.'),
        'horizon': '2021 through August 2026',
        'sources': {
            'authored': 'meoclass1/pastpapers/specs/*.json',
            'derived': 'meoclass1/pastpapers/intelligence/derived/sixyear_families.json',
        },
        'counts': modern['counts'],
        'questions_with_repeat_intelligence': sorted(
            qid for qid, a in modern['authored'].items()
            if a['host_recurrence_hint'] or a['reused_from']),
        'modern_multi_member_families': {
            r['modern_family_id']: {
                'class': r['modern_class'],
                'evidence': r['modern_evidence_class'],
                'members': r['members'],
            }
            for r in modern['derived_families'] if r['size'] > 1
        },
    }

    verdicts = Counter(r['verdict'] for r in recon)
    dispositions = Counter(r['disposition'] for r in recon)
    reach = Counter(r['topic_reach'] for r in fam_rows)
    readiness = Counter(r['readiness'] for r in fam_rows)

    doc = {
        'schema': 'miw.study.study_qi.v1',
        'schema_version': A.SCHEMA_VERSION,
        'generated_by': 'tools/study/build_study_qi.py',
        'hand_editable': False,
        'what_this_is': (
            'One governed study-intelligence projection. The existing modern '
            'question-level QI and the canonical longitudinal family QI, joined '
            'through a single adapter and read by topics, roadmap, cohorts, the '
            'workbook and the internal study page. Nothing downstream may '
            're-derive a recurrence number.'),
        'what_this_is_not': (
            'A second recurrence engine. It computes no families of its own and '
            'proposes no merges. It reads two governed layers and reports how '
            'they relate.'),
        'recurrence_weight_source': A.RECURRENCE_WEIGHT_SOURCE,
        'precedence_rule': A.PRECEDENCE_RULE,
        'dimensions': A.DIMENSIONS,
        'vocabulary': {
            'modern_dispositions': A.MODERN_DISPOSITIONS,
            'reconciliation_verdicts': A.RECONCILIATION_VERDICTS,
            'modern_evidence_classes': A.MODERN_EVIDENCE_CLASSES,
            'readiness_states': A.READINESS_STATES,
            'action_to_readiness': A.ACTION_READINESS,
        },
        'inputs': {
            'modern_qi': modern['counts'],
            'canonical_qi': canonical['counts'],
            'governed_mappings': len(mappings),
        },
        'reconciliation': {
            'compared': len(recon),
            'by_verdict': dict(sorted(verdicts.items())),
            'by_disposition': dict(sorted(dispositions.items())),
            'deterministic_conflicts': sum(
                1 for r in recon if r['verdict'] == 'CONFLICT'
                and r['modern_evidence_class'] == 'DETERMINISTIC'),
            'records_lost': 0,
            'rows': recon,
        },
        'authored_backward_claims': {
            'what_this_is': (
                'The authored host_recurrence_hint reaches back to 2013 in '
                'places. Those are the modern layer own historical claims, and '
                'the canonical layer can now say which of them governed '
                'evidence supports. Neither side is discarded.'),
            'questions_making_claims': len(corrob),
            'claims_pre_2021': sum(len(c['claimed_pre_2021']) for c in corrob),
            'corroborated_sittings': sum(len(c['corroborated']) for c in corrob),
            'uncorroborated_sittings': sum(len(c['uncorroborated']) for c in corrob),
            'rows': corrob,
        },
        'family_topic_coverage': {
            'total_families': len(fam_rows),
            'by_reach': dict(sorted(reach.items())),
            'holds': {h['family_id']: h['state'] for h in holds['topic_mapping_holds']},
        },
        'readiness': {
            'by_state': dict(sorted(readiness.items())),
            'blocked_families': sum(1 for r in fam_rows if r['blocked']),
        },
        'roadmap_recurrence_input': roadmap,
        'topics': topics,
        'families': fam_rows,
        'questions': q_rows,
    }
    return doc, baseline


def main():
    check = '--check' in sys.argv
    before = {}
    for name in PROTECTED:
        p = os.path.join(DOC, name)
        if os.path.exists(p):
            with open(p, 'rb') as fh:
                before[name] = fh.read()

    doc, baseline = build()
    payloads = [(OUT, _dump(doc)), (BASELINE, _dump(baseline))]

    stale = []
    for path, text in payloads:
        current = None
        if os.path.exists(path):
            with open(path, encoding='utf-8') as fh:
                current = fh.read()
        if current != text:
            stale.append(os.path.relpath(path, REPO))

    if check:
        for name, blob in before.items():
            with open(os.path.join(DOC, name), 'rb') as fh:
                if fh.read() != blob:
                    print('FAIL a --check run modified %s' % name)
                    return 1
        if stale:
            print('STALE %s' % ', '.join(stale))
            print('  run: python tools/study/build_study_qi.py')
            return 1
        print('OK study_qi.json and modern_qi_baseline.json match their inputs')
        return 0

    for path, text in payloads:
        with open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)

    for name, blob in before.items():
        with open(os.path.join(DOC, name), 'rb') as fh:
            if fh.read() != blob:
                raise BuildError('this builder modified %s, which it must never '
                                 'do' % name)

    r = doc['reconciliation']
    print('study_qi.json written')
    print('  modern questions with repeat intelligence : %d'
          % doc['inputs']['modern_qi']['questions_with_repeat_intelligence'])
    print('  modern multi-member families reconciled   : %d' % r['compared'])
    for v, n in sorted(r['by_verdict'].items()):
        print('      %-28s %d' % (v, n))
    print('  canonical families                        : %d' % len(doc['families']))
    print('  family -> topic reach                     : %s'
          % ', '.join('%s=%d' % kv for kv in doc['family_topic_coverage']['by_reach'].items()))
    print('  readiness                                 : %s'
          % ', '.join('%s=%d' % kv for kv in doc['readiness']['by_state'].items()))
    print('  roadmap recurrence source                 : %s'
          % doc['roadmap_recurrence_input']['source'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
