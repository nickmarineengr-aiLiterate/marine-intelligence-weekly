#!/usr/bin/env python3
"""What the governed QI layer WOULD do to study priorities. Read-only.

Nothing here is applied. It writes one file, `docs/study/qi/qi_study_preview.json`,
which is a QI artefact and not a study artefact: no study weight, no session
file, no cohort and no progress record is touched, and the suite asserts that.

Why a preview at all: the study spine already carries a `written_recurrence`
component, currently fed by 9 research-only families. The governed layer holds
270. Feeding it in would move the order, and moving a candidate's study order
mid-preparation is a Founder decision, not a build side-effect.
"""

import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import study_spine as SP

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOC = os.path.join(REPO, 'docs', 'study')
OUT = os.path.join(DOC, 'qi', 'qi_study_preview.json')

# Files this preview must never modify.
PROTECTED = [
    'study_spine.json', 'study_sessions.json', 'study_progress.json',
    'study_mappings.json', 'coverage_matrix.json',
]


def load(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def main():
    before = {}
    for name in PROTECTED:
        p = os.path.join(DOC, name)
        if os.path.exists(p):
            with open(p, 'rb') as fh:
                before[name] = fh.read()

    spine = load(os.path.join(DOC, 'study_spine.json'))
    mappings = load(os.path.join(DOC, 'study_mappings.json'))['mappings']
    fams = load(os.path.join(DOC, 'qi', 'qi_families.json'))['families']
    metrics = {m['family_id']: m
               for m in load(os.path.join(DOC, 'qi', 'qi_time_window_metrics.json'))['families']}
    ents = {e['entity_id']: e
            for e in load(os.path.join(DOC, 'qi', 'qi_source_entities.json'))['entities']}

    # A family joins a topic through its MODERN member questions, which are the
    # only members the taxonomy has ever seen. A family with no modern member
    # joins no topic -- and that absence is itself a finding, because it means
    # a recurring historical concept has no mapped modern question at all.
    by_topic = defaultdict(list)
    unmapped = defaultdict(list)
    for f in fams:
        topics = set()
        bands = {ents[e]['evidence_band'] for e in f['member_entities']}
        for e in f['member_entities']:
            ent = ents[e]
            if ent['evidence_band'] == 'HISTORICAL_SECONDARY_ARCHIVE':
                continue
            rec = mappings.get(ent['native_id'])
            if rec and rec.get('topic_id'):
                topics.add(rec['topic_id'])
        if not topics:
            # Two very different reasons a family reaches no topic, and lumping
            # them together would misstate the Phase-2 backlog badly.
            if bands == {'HISTORICAL_SECONDARY_ARCHIVE'}:
                reason = 'HISTORICAL_ONLY_NO_MODERN_MEMBER'
            elif 'MIW_SOLVED_CANONICAL' in bands:
                reason = 'SOLVED_MEMBER_PRESENT_BUT_UNMAPPED'
            else:
                reason = 'MODERN_MEMBER_IS_WORDING_ONLY_BAND'
            unmapped[reason].append(f['family_id'])
        for t in topics:
            by_topic[t].append(f['family_id'])

    domains = spine['domains']
    raw = {
        'oral_questions': [d['oral']['questions'] for d in domains],
        'examiner_evidence': [d['examiner_intelligence']['oral_questions_with_evidence'] for d in domains],
        'written_questions': [d['written']['questions'] for d in domains],
        'written_recurrence': [d['written_question_intelligence']['recurring_families'] for d in domains],
        'foundation': [len(d['dependants']) for d in domains],
        'official_scope': [len(d['official_syllabus_nodes']) for d in domains],
    }
    qi_raw = dict(raw)
    qi_raw['written_recurrence'] = [len(by_topic.get(d['domain_id'], [])) for d in domains]

    def scores(rawmap):
        scaled = {k: [v / (max(vals) or 1) for v in vals] for k, vals in rawmap.items()
                  for vals in [rawmap[k]]}
        out = []
        for i, d in enumerate(domains):
            comps = {k: round(scaled[k][i] * w, 4) for k, w in SP.PRIORITY_WEIGHTS.items()}
            out.append((d['domain_id'], d['short'], round(sum(comps.values()), 4), comps))
        return out

    cur = sorted(scores(raw), key=lambda r: -r[2])
    prev = sorted(scores(qi_raw), key=lambda r: -r[2])
    cur_rank = {r[0]: i + 1 for i, r in enumerate(cur)}
    prev_rank = {r[0]: i + 1 for i, r in enumerate(prev)}
    cur_score = {r[0]: r[2] for r in cur}

    deltas = []
    for did, short, sc, _ in prev:
        deltas.append({
            'domain_id': did,
            'short': short,
            'current_rank': cur_rank[did],
            'preview_rank': prev_rank[did],
            'rank_move': cur_rank[did] - prev_rank[did],
            'current_score': cur_score[did],
            'preview_score': sc,
            'score_delta': round(sc - cur_score[did], 4),
            'current_recurring_families': raw['written_recurrence'][
                [d['domain_id'] for d in domains].index(did)],
            'qi_governed_families': len(by_topic.get(did, [])),
        })

    doc = {
        'schema': 'miw.study.qi.study_preview.v1',
        'generated_by': 'tools/study/preview_qi_study_impact.py',
        'status': 'PREVIEW_ONLY_NOT_APPLIED',
        'what_this_is': (
            'The domain order the existing study-priority model would produce if '
            'its written_recurrence component were fed from the governed QI layer '
            'instead of the 9 research-only families it reads today.'),
        'what_this_is_not': (
            'A proposal, a decision, or anything applied. No study weight changed, '
            'no session file changed, no cohort changed and study_progress.json is '
            'untouched. Nixon study front remains D01 -> D03 -> D02 until a Founder '
            'decides otherwise.'),
        'model': {
            'weights': SP.PRIORITY_WEIGHTS,
            'component_changed': 'written_recurrence',
            'component_weight': SP.PRIORITY_WEIGHTS['written_recurrence'],
            'note': ('Only one of six components changes. The other five are read '
                     'from the live spine unchanged, so the delta below isolates '
                     'the effect of governed recurrence and nothing else.'),
        },
        'current_study_order': [r[0] for r in cur],
        'qi_informed_preview_order': [r[0] for r in prev],
        'order_changed': [r[0] for r in cur] != [r[0] for r in prev],
        'active_front_unchanged': ['D01', 'D03', 'D02'],
        'domain_deltas': deltas,
        'families_per_topic': {k: sorted(v) for k, v in sorted(by_topic.items())},
        'families_with_no_mapped_topic': {
            'count': sum(len(v) for v in unmapped.values()),
            'by_reason': {k: len(v) for k, v in sorted(unmapped.items())},
            'why_the_split_matters': (
                'The taxonomy maps MIW oral questions and the 360 SOLVED written '
                'questions. It has never mapped the 2021-2022 wording-only band. '
                'So "no topic" means two different things: a family that lives '
                'only in 2010-2020 and has no modern life at all, and a family '
                'that is alive in 2021-2022 but whose modern member is simply not '
                'a question the taxonomy has ever been asked to map. Reported as '
                'one number, the Phase-2 backlog would be badly overstated.'),
            'family_ids': {k: sorted(v) for k, v in sorted(unmapped.items())},
        },
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write('\n')

    after = {}
    for name in PROTECTED:
        p = os.path.join(DOC, name)
        if os.path.exists(p):
            with open(p, 'rb') as fh:
                after[name] = fh.read()
    touched = sorted(k for k in before if before[k] != after[k])
    if touched:
        print('PREVIEW MUTATED PROTECTED STUDY FILES: %s' % touched, file=sys.stderr)
        return 1

    print('current order : %s' % ' > '.join(doc['current_study_order']))
    print('preview order : %s' % ' > '.join(doc['qi_informed_preview_order']))
    print('order changed : %s' % doc['order_changed'])
    print('protected study files touched: 0')
    for d in deltas:
        arrow = '=' if d['rank_move'] == 0 else ('up %d' % d['rank_move'] if d['rank_move'] > 0 else 'down %d' % -d['rank_move'])
        print('  %s %-26s %2d -> %2d  %-7s  score %+.4f  families %d -> %d'
              % (d['domain_id'], d['short'][:26], d['current_rank'], d['preview_rank'],
                 arrow, d['score_delta'], d['current_recurring_families'], d['qi_governed_families']))
    print('families reaching no topic: %d' % sum(len(v) for v in unmapped.values()))
    for k, v in sorted(unmapped.items()):
        print('    %-40s %d' % (k, len(v)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
