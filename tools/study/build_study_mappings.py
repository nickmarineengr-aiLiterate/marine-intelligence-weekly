#!/usr/bin/env python3
"""Build docs/study/study_mappings.json -- the governed mapping store.

    qb_content_index.json  --(ORAL adapter)----.
                                                >-- mapping_engine --> store
    pastpapers/specs/*.json --(WRITTEN adapter)-'

This is the ONLY writer of the mapping store. build_study_spine.py reads it;
nothing re-derives mappings independently.

Incremental by default (40G): a question whose mapping already carries the
current taxonomy digest is skipped, so adding one paper does not reprocess the
whole corpus. `--force` re-derives everything, and is what you run after
changing study_spine.py.

Usage:
    python tools/study/build_study_mappings.py           # incremental
    python tools/study/build_study_mappings.py --force   # full re-derive
    python tools/study/build_study_mappings.py --check   # fail if stale
    python tools/study/build_study_mappings.py --status  # taxonomy drift report
"""
import argparse, glob, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import mapping_engine as ME
import reconcile_official_mappings as RO

QB     = os.path.join(ROOT, 'meoclass1', 'qb_content_index.json')
SPECS  = os.path.join(ROOT, 'meoclass1', 'pastpapers', 'specs', '*.json')
ADJ    = os.path.join(HERE, 'adjudications.json')
STORE  = os.path.join(ROOT, 'docs', 'study', 'study_mappings.json')
QUEUE  = os.path.join(ROOT, 'docs', 'study', 'mapping_review_queue.json')


def corpus_items():
    """Yield (item, content_type, kwargs) for every canonical question."""
    idx = json.load(open(QB, encoding='utf-8'))
    for fname, f in sorted(idx['files'].items()):
        for q in f['questions']:
            yield q, 'ORAL', {'file_name': fname}
    for p in sorted(glob.glob(SPECS)):
        spec = json.load(open(p, encoding='utf-8'))
        for q in spec['questions']:
            yield q, 'WRITTEN', {'paper_id': spec['paper_id']}


def write(store, path):
    body = json.dumps(store, indent=2, ensure_ascii=False) + '\n'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        fh.write(body)
    return body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--status', action='store_true')
    a = ap.parse_args()

    store = ME.load_store(STORE)

    if a.status:
        cls = ME.classify_against_taxonomy(store)
        print(f'taxonomy_version (current) = {ME.taxonomy_version()}')
        print(f'store taxonomy_version     = {store.get("taxonomy_version")}')
        for k in ('UNCHANGED', 'STALE', 'NEEDS_REVIEW', 'ORPHANED_NODE'):
            print(f'  {k:14s} {len(cls[k]):4d}')
        return 1 if (cls['STALE'] or cls['ORPHANED_NODE']) else 0

    store, stats = ME.incremental_update(store, corpus_items(), force=a.force)
    adj = json.load(open(ADJ, encoding='utf-8'))['adjudications']
    store, astats, refusals = ME.apply_adjudications(store, adj)
    for r in refusals:
        print('  REFUSED ADJUDICATION ' + r)
    store['generated_by'] = 'tools/study/build_study_mappings.py'
    store['authority'] = ('MIW-DERIVED topic structure, crosswalked to the '
                          'official DGMA syllabus. The topic labels are not an '
                          'official DGMA syllabus. See '
                          'docs/study/SYLLABUS_SOURCE_STATUS.md.')

    # Attach the adopted-syllabus join through the SAME code the standalone
    # reconciler uses. Two paths that both write this store would drift, and
    # the drift would surface as a permanently STALE --check that everyone
    # learns to ignore -- which is how a gate stops being a gate.
    _, rec_errors = RO.reconcile(store)
    if rec_errors:
        for line in rec_errors[:10]:
            print('  RECONCILE ERROR ' + line)
        return 1
    counts = {}
    for r in store['mappings'].values():
        counts[r['mapping_status']] = counts.get(r['mapping_status'], 0) + 1
    store['summary'] = {'total': len(store['mappings']), 'by_status': dict(sorted(counts.items()))}
    # keep key order stable for byte-identical rebuilds
    store = {k: store[k] for k in sorted(store) if k != 'mappings'} | {'mappings': store['mappings']}

    queue = ME.review_queue(store)
    # The standing inventory of the file-level over-capture pattern: a QB file
    # whose title names one domain, holding questions whose own text cues a
    # different one. DERIVED, so it can never rot into a stale hand-list -- a
    # file drops off this summary the moment its questions are adjudicated.
    #
    # Every count below splits FRESH from HELD. A single 'unadjudicated'
    # number was wrong in one direction only, but it was wrong on the number
    # a human reads: on 2026-08-23 QB4_H.html reported one unadjudicated
    # question, and that question was QB4_H#q9 -- carrying a written human
    # HOLD. Held work reported as outstanding work is pressure to clear a
    # hold, which is the one thing the adjudication contract forbids.
    contra = {}
    for i in queue:
        rec = store['mappings'][i['canonical_question_id']]
        if rec.get('mapping_evidence') != 'FILE_TITLE_CONTRADICTED':
            continue
        f = contra.setdefault(rec['source_file'],
                              {'file_topic_id': rec['topic_id'],
                               'fresh_unadjudicated': 0,
                               'held_adjudicated': 0, 'questions': []})
        held = i.get('review_status') == ME.HELD_ADJUDICATED
        f['held_adjudicated' if held else 'fresh_unadjudicated'] += 1
        f['questions'].append({
            'canonical_question_id': i['canonical_question_id'],
            'review_status': i.get('review_status'),
            'contradicting_topic_ids': rec.get('contradicting_topic_ids') or []})
    contra_items = [i for i in queue
                    if store['mappings'][i['canonical_question_id']]
                    .get('mapping_evidence') == 'FILE_TITLE_CONTRADICTED']
    qbody = json.dumps({'generated_by': 'tools/study/build_study_mappings.py',
                        'taxonomy_version': ME.taxonomy_version(),
                        'queue_states': {
                            'what': 'HELD is not UNADJUDICATED. A held item '
                                    'was read by a named human who recorded '
                                    'why the evidence does not settle it; a '
                                    'fresh item has been read by nobody. '
                                    'Never sum these into one backlog number.',
                            **ME.queue_summary(queue)},
                        'total': len(queue),
                        'file_title_contradictions': {
                            'what': 'QB files whose title names one domain but '
                                    'which hold questions whose own text cues '
                                    'another. Follow-up inventory for the '
                                    '2026-08-23 over-capture correction.',
                            'files': len(contra),
                            **ME.queue_summary(contra_items),
                            'by_file': dict(sorted(contra.items()))},
                        'items': queue},
                       indent=2, ensure_ascii=False) + '\n'

    body = json.dumps(store, indent=2, ensure_ascii=False) + '\n'
    if a.check:
        cur = open(STORE, encoding='utf-8').read() if os.path.exists(STORE) else ''
        curq = open(QUEUE, encoding='utf-8').read() if os.path.exists(QUEUE) else ''
        if cur != body or curq != qbody:
            print('STALE: mapping store or review queue differs from a fresh build')
            return 1
        print('OK: mapping store and review queue are current')
        return 0

    write(store, STORE)
    with open(QUEUE, 'w', encoding='utf-8', newline='') as fh:
        fh.write(qbody)
    print(f'wrote docs/study/study_mappings.json  ({len(store["mappings"])} mappings)')
    print(f'  {stats}')
    print(f'  adjudications: {astats}')
    print(f'  by status: {store["summary"]["by_status"]}')
    qs = ME.queue_summary(queue)
    print(f'wrote docs/study/mapping_review_queue.json  ({qs["total"]} open: '
          f'{qs["fresh_unadjudicated"]} unadjudicated, '
          f'{qs["held_adjudicated"]} human-held)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
