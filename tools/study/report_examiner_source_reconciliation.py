#!/usr/bin/env python3
"""Reconcile the two examiner-relationship files the study layer could read.

    CURRENT_EXAMINER_RELATIONSHIPS.jsonl  Phase-2 recovery ledger (2026-08-23)
    EXAMINER_INDEX_SNAPSHOT.json          resolved product snapshot
                                          (tools/oral/build_examiner_index.py)

Writes one row per (canonical_question_id, examiner) pair found in EITHER file:

    canonical_id, examiner, provenance (snapshot sources), evidence tier,
    ledger tier (research_best_tier), present_in_ledger, present_in_snapshot,
    disposition

Dispositions
    CARRIED_FORWARD            in both; snapshot tier == the ledger's research
                               tier under examiner_index_config's mapping
    CARRIED_FORWARD_RETIERED   in both; Release A evidence merged into the pair
                               moved its tier (the snapshot records why)
    ADDED_BY_<SOURCE>          snapshot only; SOURCE in RELEASE_A, QCARD,
                               CE_TIP_REVIEW
    DROPPED                    ledger only. Any such row FAILS this report:
                               the snapshot may not lose a ledger pair silently.

Read-only over both inputs. Deterministic (sorted, no clock).

    python tools/study/report_examiner_source_reconciliation.py           # write
    python tools/study/report_examiner_source_reconciliation.py --check   # fail if stale
"""
import argparse, collections, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import examiner_source as EXS

EA = os.path.join(ROOT, 'meoclass1', 'oral-intelligence', 'examiner-audit')
LEDGER = os.path.join(EA, 'CURRENT_EXAMINER_RELATIONSHIPS.jsonl')
OUT = os.path.join(ROOT, 'docs', 'study',
                   'ORAL_EXAMINER_SOURCE_RECONCILIATION_20261008.json')


def build():
    r2l = json.load(open(EXS.CONFIG, encoding='utf-8'))['research_tier_to_literal']
    ledger = {}
    for line in open(LEDGER, encoding='utf-8'):
        if line.strip():
            r = json.loads(line)
            ledger[(r['question_id'], r['examiner'])] = r
    snap = {(r['canonical_question_id'], r['examiner']): r for r in EXS.load()}
    idx = json.load(open(EXS.QB_INDEX, encoding='utf-8'))
    live = sorted(q['id'] for f in idx['files'].values() for q in f['questions'])

    rows = []
    for key in sorted(set(ledger) | set(snap)):
        led, sn = ledger.get(key), snap.get(key)
        led_tier = led['research_best_tier'] if led else None
        if led and sn:
            disp = ('CARRIED_FORWARD' if r2l.get(led_tier) == sn['tier']
                    else 'CARRIED_FORWARD_RETIERED')
        elif sn:
            extra = [s for s in sn['sources'] if s != 'INDEX']
            disp = 'ADDED_BY_' + '+'.join(extra or ['UNKNOWN'])
        else:
            disp = 'DROPPED'
        rows.append({
            'canonical_id': key[0], 'examiner': key[1],
            'provenance': sn['sources'] if sn else ['LEDGER_ONLY'],
            'evidence_tier': sn['tier'] if sn else None,
            'ledger_research_tier': led_tier,
            'present_in_ledger': bool(led), 'present_in_snapshot': bool(sn),
            'disposition': disp,
        })

    qs_led = {k[0] for k in ledger}
    qs_snap = {k[0] for k in snap}
    summary = {
        'ledger_pairs': len(ledger), 'snapshot_pairs': len(snap),
        'ledger_questions': len(qs_led), 'snapshot_questions': len(qs_snap),
        'canonical_questions': len(live),
        'questions_with_no_examiner_pair': len(set(live) - qs_snap),
        'by_disposition': dict(sorted(collections.Counter(
            r['disposition'] for r in rows).items())),
        'snapshot_pairs_by_tier': {t: sum(1 for r in snap.values() if r['tier'] == t)
                                   for t in EXS.tier_policy()},
        'snapshot_questions_by_strongest_tier': dict(collections.Counter(
            EXS.strongest_tier({r['tier'] for k, r in snap.items() if k[0] == q})
            for q in sorted(qs_snap))),
    }
    return {
        'schema': 'miw.study.examiner_source_reconciliation.v1',
        'generated_by': 'tools/study/report_examiner_source_reconciliation.py',
        'hand_editable': False,
        'record_class': 'DATED RECONCILIATION RECORD (Phase 0, 2026-10-08)',
        'inputs': {
            'ledger': 'meoclass1/oral-intelligence/examiner-audit/'
                      'CURRENT_EXAMINER_RELATIONSHIPS.jsonl',
            'snapshot': EXS.SNAPSHOT_REL,
        },
        'decision': ('The study layer reads the snapshot through '
                     'tools/study/examiner_source.py. The ledger is not '
                     'regenerated: it is the recovery ledger build_examiner_index '
                     'resolves FROM; regenerating it from the generated index '
                     'would be circular.'),
        'tier_policy': {t: {'label': p['label'], 'meaning': p['meaning']}
                        for t, p in EXS.tier_policy().items()},
        'summary': summary,
        'rows': rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    rec = build()
    if rec['summary']['by_disposition'].get('DROPPED'):
        print(f"FAIL: {rec['summary']['by_disposition']['DROPPED']} ledger pair(s) "
              f"absent from the snapshot")
        return 1
    body = json.dumps(rec, indent=1, ensure_ascii=False) + '\n'
    if args.check:
        cur = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else None
        if cur != body:
            print('STALE: ' + os.path.relpath(OUT, ROOT))
            return 3
        print('examiner source reconciliation -- current')
        return 0
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(body)
    print('wrote ' + os.path.relpath(OUT, ROOT))
    print(json.dumps(rec['summary'], indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
