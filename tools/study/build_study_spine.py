#!/usr/bin/env python3
"""Build docs/study/study_spine.json -- the MEO Class I study spine.

    specs/*.json            --(topic_taxonomy)-->  written mappings
    qb_content_index.json   --(study_spine)---->   oral mappings
    CURRENT_EXAMINER_RELATIONSHIPS.jsonl -------->  examiner intelligence
    notes_content_index.json -------------------->  resource inventory

Every count on the output is recomputed here. Nothing is hand-maintained.

Determinism: no clock is read. `generated_from` records the newest spec
`updated` value, the same convention as the delivery manifest and the topic
map, so two runs over the same corpus are byte-identical.

Usage:
    python tools/study/build_study_spine.py            # write
    python tools/study/build_study_spine.py --check    # fail if stale
"""
import argparse, collections, glob, io, json, os, re, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'tools', 'pastpapers'))

import study_spine as SP
import mapping_engine as ME
import topic_taxonomy as TT

SPECS_GLOB = os.path.join(ROOT, 'meoclass1', 'pastpapers', 'specs', '*.json')
QB_INDEX   = os.path.join(ROOT, 'meoclass1', 'qb_content_index.json')
EXAMINERS  = os.path.join(ROOT, 'meoclass1', 'oral-intelligence',
                          'examiner-audit', 'CURRENT_EXAMINER_RELATIONSHIPS.jsonl')
NOTES      = os.path.join(ROOT, 'meoclass1', 'oralnotes', 'notes_content_index.json')
STORE      = os.path.join(ROOT, 'docs', 'study', 'study_mappings.json')
OUT        = os.path.join(ROOT, 'docs', 'study', 'study_spine.json')


def load_specs():
    return [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(SPECS_GLOB))]


def map_written(specs, store):
    """Read the WRITTEN half of the governed store; enrich with study topics.

    The mapping DECISION belongs to mapping_engine. This function only joins
    it back to the spec fields the spine needs to aggregate.
    """
    allq = [q for s in specs for q in s['questions']]
    norm = TT.make_normaliser(allq)
    rows, unmapped = [], []
    for s in specs:
        for q in s['questions']:
            qid = f"{s['paper_id']}-{q['q_no']}"
            m = store['mappings'][qid]
            rec = {
                'paper_id': s['paper_id'], 'month_year': s['month_year'],
                'year': s['year'], 'q_no': q['q_no'],
                'marks': q.get('total_marks'),
                'short_title': q['short_title'].strip(),
                'primary_category': (q.get('primary_category') or '').strip(),
                'study_topics': TT.study_topics_for(q, norm),
                'domain_id': m['topic_id'],
                'confidence': m['mapping_confidence'],
                'basis': m['mapping_basis'],
            }
            (rows if m['topic_id'] else unmapped).append(rec)
    return rows, unmapped


def map_oral(idx, store):
    """Read the ORAL half of the governed store."""
    rows, queue = [], []
    for fname, f in sorted(idx['files'].items()):
        for q in f['questions']:
            m = store['mappings'][q['id']]
            base = {
                'id': q['id'], 'file': fname, 'anchor': q['anchor'],
                'qnum': q['qnum'], 'text': q['text'],
                'qb_group': f['qb_group'], 'file_title': f['title'],
                'domain_id': m['topic_id'],
                'confidence': m['mapping_confidence'],
                'basis': m['mapping_basis'],
            }
            (rows if m['topic_id'] else queue).append(base)
    return rows, queue


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    specs = load_specs()
    idx = json.load(open(QB_INDEX, encoding='utf-8'))
    rels = [json.loads(l) for l in open(EXAMINERS, encoding='utf-8') if l.strip()]
    notes = json.load(open(NOTES, encoding='utf-8'))

    store = ME.load_store(STORE)
    if not store['mappings']:
        print('FAIL: run tools/study/build_study_mappings.py first')
        return 1
    written, w_unmapped = map_written(specs, store)
    oral, o_queue = map_oral(idx, store)

    # ---- examiner intelligence, per oral question id ----------------------
    ex_by_q = collections.defaultdict(set)
    rel_by_q = collections.Counter()
    for r in rels:
        ex_by_q[r['question_id']].add(r['examiner'])
        rel_by_q[r['question_id']] += 1
    oral_dom = {r['id']: r['domain_id'] for r in oral}

    # ---- written recurrence families (exact short_title) ------------------
    fam = collections.defaultdict(list)
    for r in written:
        fam[r['short_title']].append(r)
    recurring = {k: v for k, v in fam.items() if len(v) > 1}

    # ---- per-domain aggregation -------------------------------------------
    domains = []
    for d in SP.DOMAINS:
        did = d['domain_id']
        o = [r for r in oral if r['domain_id'] == did]
        w = [r for r in written if r['domain_id'] == did]
        ex_qs = [r['id'] for r in o if r['id'] in ex_by_q]
        examiners = sorted({e for r in o for e in ex_by_q.get(r['id'], ())})
        w_fam = {k: len(v) for k, v in recurring.items()
                 if v[0]['domain_id'] == did}
        topics = collections.Counter(t for r in w for t in r['study_topics'])
        dependants = [x['domain_id'] for x in SP.DOMAINS
                      if did in x['prerequisites']]
        domains.append({
            'domain_id': did, 'name': d['name'], 'short': d['short'],
            'rationale': d['rationale'],
            'official_syllabus_nodes': [],       # see SYLLABUS_SOURCE_STATUS.md
            'syllabus_status': 'NO_OFFICIAL_SOURCE_IN_REPO',
            'prerequisites': d['prerequisites'],
            'dependants': dependants,
            'written_categories': d['written_categories'],
            'oral': {
                'questions': len(o),
                'high_confidence': sum(1 for r in o if r['confidence'] == 'HIGH'),
                'medium_confidence': sum(1 for r in o if r['confidence'] == 'MEDIUM'),
                'files': sorted({r['file'] for r in o}),
            },
            'written': {
                'questions': len(w),
                'papers': len({r['paper_id'] for r in w}),
                'marks': sum(r['marks'] or 0 for r in w),
                'top_topics': topics.most_common(12),
            },
            'examiner_intelligence': {
                'oral_questions_with_evidence': len(ex_qs),
                'relationship_occurrences': sum(rel_by_q[q] for q in ex_qs),
                'distinct_examiners': len(examiners),
                'examiners': examiners,
            },
            'written_question_intelligence': {
                'recurring_families': len(w_fam),
                'largest_families': sorted(w_fam.items(),
                                           key=lambda kv: (-kv[1], kv[0]))[:8],
            },
        })

    # ---- transparent study-priority score ---------------------------------
    def norm_of(key, vals):
        top = max(vals) or 1
        return [v / top for v in vals]

    raw = {
        'oral_questions':     [d['oral']['questions'] for d in domains],
        'examiner_evidence':  [d['examiner_intelligence']['oral_questions_with_evidence'] for d in domains],
        'written_questions':  [d['written']['questions'] for d in domains],
        'written_recurrence': [d['written_question_intelligence']['recurring_families'] for d in domains],
        'foundation':         [len(d['dependants']) for d in domains],
    }
    scaled = {k: norm_of(k, v) for k, v in raw.items()}
    for i, d in enumerate(domains):
        comps = {k: round(scaled[k][i] * w, 4)
                 for k, w in SP.PRIORITY_WEIGHTS.items()}
        d['study_priority'] = {
            'components': comps,
            'weights': SP.PRIORITY_WEIGHTS,
            'raw': {k: raw[k][i] for k in raw},
            'score': round(sum(comps.values()), 4),
        }
    order = sorted(domains, key=lambda d: -d['study_priority']['score'])
    for rank, d in enumerate(order, 1):
        d['priority_rank'] = rank

    out = {
        'spine_version': '1.0',
        'generated_by': 'tools/study/build_study_spine.py',
        'generated_from': max(s.get('updated', '') for s in specs),
        'authority': 'MIW-DERIVED. Not an official DGMA syllabus. See '
                     'docs/study/SYLLABUS_SOURCE_STATUS.md.',
        'sources': {
            'written_specs': f'{len(specs)} papers',
            'oral_index': f"{idx['total_questions']} questions / {idx['total_files']} files",
            'examiner_relationships': len(rels),
            'notes_files': notes.get('total_files'),
            'mapping_store': f"{len(store['mappings'])} governed mappings @ taxonomy {store.get('taxonomy_version')}",
        },
        'totals': {
            'domains': len(domains),
            'written_questions_mapped': len(written),
            'written_questions_unmapped': len(w_unmapped),
            'oral_questions_mapped': len(oral),
            'oral_questions_unresolved': len(o_queue),
            'oral_questions_total': idx['total_questions'],
            'written_recurring_families': len(recurring),
        },
        'domains': domains,
        'ambiguous_mapping_queue': o_queue,
        'unmapped_written': w_unmapped,
    }

    body = json.dumps(out, indent=2, ensure_ascii=False, sort_keys=False) + '\n'
    if args.check:
        cur = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
        if cur != body:
            print('STALE: docs/study/study_spine.json differs from a fresh build')
            return 1
        print('OK: study spine is current')
        return 0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='') as fh:
        fh.write(body)
    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    print(f"  domains={len(domains)} oral_mapped={len(oral)} "
          f"unresolved={len(o_queue)} written_mapped={len(written)}")
    for d in order:
        print(f"  #{d['priority_rank']} {d['domain_id']} {d['short']:20s} "
              f"score={d['study_priority']['score']:.3f} "
              f"oral={d['oral']['questions']:3d} written={d['written']['questions']:3d} "
              f"exam={d['examiner_intelligence']['oral_questions_with_evidence']:3d}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
