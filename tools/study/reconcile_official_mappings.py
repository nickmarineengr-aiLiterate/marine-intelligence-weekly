#!/usr/bin/env python3
"""Reconcile the governed mapping store against the official syllabus layer.

This does NOT remap anything. The 1081 existing question->topic decisions were
made from structural evidence and are preserved byte-for-byte; all this adds
is the adopted-syllabus join produced by `mapping_engine.attach_official`, so
that every question resolves upward to Annexure III as well as downward to a
MIW topic.

Reported outcomes:
  unchanged        topic mapping identical to before (expected: all of them)
  reconciled       gained or changed an official-syllabus join
  stale            taxonomy_version no longer matches the live taxonomy
  review_pending   mapping_status was already REVIEW_PENDING
  orphaned         topic has no PRIMARY node in Annexure III

Determinism: no clock is read.

Usage:
    python tools/study/reconcile_official_mappings.py            # write
    python tools/study/reconcile_official_mappings.py --check    # fail if stale
"""
import argparse, collections, copy, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import mapping_engine as ME

STORE = os.path.join(ROOT, 'docs', 'study', 'study_mappings.json')

# Fields that define the question->topic decision. If any of these move, the
# reconciliation has overstepped its remit and must fail rather than publish.
TOPIC_FIELDS = ('canonical_question_id', 'content_type', 'topic_id',
                'subtopic_id', 'mapping_role', 'mapping_confidence',
                'mapping_basis', 'mapping_status', 'last_reviewed')


def reconcile(store):
    live_taxonomy = ME.taxonomy_version()
    counts = collections.Counter()
    errors = []

    for qid, rec in sorted(store['mappings'].items()):
        before = {f: rec.get(f) for f in TOPIC_FIELDS}
        had_official = 'official_alignment_status' in rec
        prior = rec.get('official_alignment_status')

        rec['syllabus_status'] = ME.OFFICIAL_STATUS
        ME.attach_official(rec)

        after = {f: rec.get(f) for f in TOPIC_FIELDS}
        if before != after:
            errors.append(f'{qid}: reconciliation altered the topic mapping')
            continue
        counts['unchanged'] += 1

        if not had_official or prior != rec['official_alignment_status']:
            counts['reconciled'] += 1
        if rec.get('taxonomy_version') != live_taxonomy:
            counts['stale'] += 1
        if rec.get('mapping_status') == 'REVIEW_PENDING':
            counts['review_pending'] += 1
        if rec['official_alignment_status'] == 'ORPHANED_IN_ADOPTED_SYLLABUS':
            counts['orphaned'] += 1
        if rec['official_alignment_status'] == 'UNRESOLVED':
            counts['unresolved'] += 1

        bad = ME.validate_mapping(rec)
        if bad:
            errors.append(f'{qid}: ' + '; '.join(bad))

    by_conf = collections.Counter(
        r.get('official_mapping_confidence') for r in store['mappings'].values())
    by_align = collections.Counter(
        r.get('official_alignment_status') for r in store['mappings'].values())

    store['official_syllabus'] = {
        'syllabus_version': ME.OFFICIAL_VERSION,
        'status': ME.OFFICIAL_STATUS,
        'effective_from': ME.OFFICIAL_EFFECTIVE_FROM,
        'crosswalk': 'docs/study/official_crosswalk.json',
        'source_sha256': ME.official_crosswalk()['official_source']['sha256'],
        'by_official_confidence': dict(sorted(by_conf.items(),
                                              key=lambda kv: str(kv[0]))),
        'by_alignment': dict(sorted(by_align.items(),
                                    key=lambda kv: str(kv[0]))),
    }
    return counts, errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    original = open(STORE, encoding='utf-8').read()
    store = json.loads(original)
    counts, errors = reconcile(store)

    if errors:
        print(f'FAIL -- {len(errors)} reconciliation error(s)')
        for line in errors[:20]:
            print('  ' + line)
        return 1

    text = json.dumps(store, indent=2, ensure_ascii=False) + '\n'
    if args.check:
        if text != original:
            print('FAIL: docs/study/study_mappings.json is stale -- '
                  'run tools/study/reconcile_official_mappings.py')
            return 1
        print('official mapping reconciliation -- up to date')
        return 0

    with open(STORE, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)

    total = len(store['mappings'])
    print(f'reconciled {total} mappings against {ME.OFFICIAL_VERSION}')
    for key in ('unchanged', 'reconciled', 'stale', 'review_pending',
                'orphaned', 'unresolved'):
        print(f'  {key:16s} {counts.get(key, 0)}')
    print('  by alignment    ' + json.dumps(store['official_syllabus']['by_alignment']))
    print('  by confidence   ' + json.dumps(store['official_syllabus']['by_official_confidence']))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
