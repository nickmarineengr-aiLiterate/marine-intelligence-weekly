#!/usr/bin/env python3
"""Focused regression: topic-level evidence must never become node evidence.

THE DEFECT THIS PINS
--------------------
`mapping_engine.attach_official` resolves a question to one Annexure III node
only when its MIW topic maps to exactly one node. Where the topic maps to
several, the question is honestly aligned to the candidate SET at MEDIUM with
`official_syllabus_node_id = None`. That rule is correct and is unchanged.

The defect was never in the rule. It was in every downstream reader that
folded a candidate SET into per-node counts by looping over the candidates and
crediting each one with a whole unit of evidence. One topic-level question then
appears as seven node-level claims. That is why Annexure III nodes 02, 08, 13,
14, 15, 16 and 17 all reported oral=197 / written=69: all seven sit under D03,
so all seven inherited D03's entire question count. The numbers were identical
because they were literally the same number, counted seven times.

WHAT THIS TEST DOES
-------------------
It builds a topic carrying several candidate official nodes and exactly ONE
topic-level Oral evidence record drawn from the spoken-examination corpus, then
asserts:

  * every candidate node's NODE-LEVEL tally stays at zero, and
  * the TOPIC-LEVEL (candidate-set) tally of every candidate node rises by one.

PROVING THE REGRESSION BITES
----------------------------
A regression that has never failed proves nothing. Rather than mutate the
repository to reproduce the old behaviour, this file carries the pre-change
derivation itself, as `legacy_fanout_tally` -- the fold that was in use before
this job: `for node in candidates: tally[node] += 1`, with no granularity
distinction. `test_pre_change_derivation_fails` runs the SAME assertion against
that derivation and requires it to raise AssertionError. If the old fold ever
stopped inflating, this test fails, so the two halves cannot silently agree.

Usage:  python tools/study/test_syllabus_fanout.py
"""
import io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import mapping_engine as ME

STORE = os.path.join(ROOT, 'docs', 'study', 'study_mappings.json')

# The topic the live corpus actually fans out through. Chosen from the data,
# not invented: D03 carries seven PRIMARY Annexure III nodes.
FANOUT_TOPIC = 'D03'

passed, failed = 0, 0


def ok(name, condition, detail=''):
    global passed, failed
    if condition:
        passed += 1
        print(f'  PASS {name}')
    else:
        failed += 1
        print(f'  FAIL {name}: {detail}')


# --------------------------------------------------------------------------- #
# The pre-change derivation, preserved verbatim in behaviour
# --------------------------------------------------------------------------- #
def legacy_fanout_tally(contributions, node_ids):
    """How per-node coverage was folded BEFORE this job.

    It reads `official_syllabus_node_candidates` and credits every candidate
    with one unit of evidence, with no notion of granularity. This is the
    function whose output made seven nodes report one topic's count each.
    """
    tally = {n: 0 for n in node_ids}
    for c in contributions:
        nodes = ([c['resolved_official_node_id']]
                 if c['resolved_official_node_id']
                 else c['candidate_official_node_ids'])
        for n in nodes:
            tally[n] += 1
    return tally


def one_topic_level_oral_record():
    """One REAL topic-level Oral record from the spoken-examination corpus.

    Real, not synthetic: the point of the test is that the live corpus fans
    out, so it reads the live corpus. Falls back to constructing the record
    through the engine's own adapter if the store holds no such question,
    which would itself be a finding worth seeing.
    """
    store = json.load(open(STORE, encoding='utf-8'))['mappings']
    for qid in sorted(store):
        r = store[qid]
        if (r.get('content_type') == 'ORAL'
                and r.get('topic_id') == FANOUT_TOPIC
                and len(r.get('official_syllabus_node_candidates') or []) > 1):
            return qid, r
    raise SystemExit('FAIL: the corpus holds no topic-level Oral record for '
                     f'{FANOUT_TOPIC}; this test has nothing to pin')


def main():
    candidates = ME.official_nodes_for_topic(FANOUT_TOPIC)
    print(f'topic {FANOUT_TOPIC} carries {len(candidates)} candidate official '
          f'nodes: {candidates}')
    ok('T-FANOUT-SEVERAL-CANDIDATES', len(candidates) > 1,
       f'{FANOUT_TOPIC} does not fan out; nothing to pin')

    qid, rec = one_topic_level_oral_record()
    print(f'topic-level Oral evidence record: {qid}')

    # ---- the granularity the engine stamped --------------------------------
    ok('T-FANOUT-GRANULARITY', rec.get('evidence_granularity') == 'TOPIC_LEVEL',
       f"record granularity is {rec.get('evidence_granularity')!r}")
    ok('T-FANOUT-NOT-PINPOINTED', rec.get('official_syllabus_node_id') is None,
       'a fanned-out record must carry no resolved node id')
    ok('T-FANOUT-SET-COMPLETE',
       list(rec.get('official_syllabus_node_candidates') or []) == candidates,
       'the candidate set is not the topic\'s complete node set')
    ok('T-FANOUT-MEDIUM',
       rec.get('official_mapping_confidence') == 'MEDIUM',
       'a candidate-set record must stay at MEDIUM confidence')

    contribution = ME.coverage_contribution(rec)
    tallies = ME.tally_contributions([contribution], candidates)

    # ---- THE PROPERTY ------------------------------------------------------
    for node in candidates:
        t = tallies['by_node'][node]
        ok(f'T-FANOUT-NODE-ZERO/{node}', t['resolved'] == 0,
           f"node-level tally rose to {t['resolved']} on topic-level evidence")
        ok(f'T-FANOUT-TOPIC-RISES/{node}', t['topic_level'] == 1,
           f"topic-level tally is {t['topic_level']}, expected 1")

    ok('T-FANOUT-TOTALS',
       tallies['totals'] == {'resolved': 0, 'topic_level': 1, 'ambiguous': 0},
       f"totals are {tallies['totals']}")

    # ---- the regression is proved to bite ----------------------------------
    legacy = legacy_fanout_tally([contribution], candidates)
    inflated = sorted(n for n, v in legacy.items() if v > 0)
    print('\npre-change derivation (legacy_fanout_tally), same single record:')
    print(f'  credited {len(inflated)} nodes with node-level evidence: '
          f'{inflated}')
    try:
        for node in candidates:
            assert legacy[node] == 0, (
                f'{node} node-level tally rose to {legacy[node]} on a single '
                f'topic-level record')
        raise SystemExit('FAIL T-FANOUT-BITES: the pre-change derivation did '
                         'not inflate, so this regression proves nothing')
    except AssertionError as exc:
        print(f'  AssertionError: {exc}')
        ok('T-FANOUT-BITES', True)
    ok('T-FANOUT-LEGACY-INFLATES', len(inflated) == len(candidates),
       f'legacy fold credited {len(inflated)} of {len(candidates)} nodes')

    print(f'\nsyllabus fan-out regression -- {passed + failed} assertions')
    if failed:
        print(f'{failed} FAILED')
        return 1
    print('  all PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
