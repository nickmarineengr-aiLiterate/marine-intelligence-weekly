#!/usr/bin/env python3
"""Prove the six-year intelligence layer is REGENERABLE and counts each sitting once.

    specs/QP*.json  +  intelligence/historical_qp_intelligence.json
        --> build_sixyear_intelligence.py --> families + nodes

WHY THIS TEST EXISTS
--------------------
The builder used to read its historical input from a hard-coded path inside one
Claude session's scratchpad directory. Two things followed, and both actually
happened:

  * the layer could not be rebuilt at all once that directory was cleaned, so
    "regenerate and check" was not an available move; and
  * the scratchpad copy and the committed copy drifted apart with nothing
    watching, because no check ever compared them.

When September 2023 was solved, its record was then deleted from the historical
store BY HAND so the totals would not count the sitting twice -- once as a
solved paper and once as its own intelligence-only ghost. That manual step is
the real hazard. It is invisible, it must be repeated for every future paper,
and forgetting it inflates the corpus in a direction that flatters the product.

So graduation is now a rule in the builder, the store keeps a complete shelf
record, and this file is what stops either from quietly regressing.

WHAT IS ASSERTED
----------------
    1  neither six-year tool depends on a path outside the repository
    2  a double build is byte-identical
    3  a paper with a canonical solved spec is excluded from the historical set
    4  no sitting and no question is counted twice
    5  no 2021/2022 sitting is ever marked SOLVED
    6  node ordering and node identity are stable across builds
    7  every family carries a known class and the families partition the nodes
    8  the reported universe equals the sum of its parts, recomputed

Rule 3 is the one with teeth, so --self-test does not merely re-run it. It
promotes a real intelligence-only paper to SOLVED in a scratch tree and asserts
the historical duplicate disappears; then it disables the rule and asserts the
same sitting is counted TWICE. A guard that has never been seen to fail, and
never been seen to matter, proves nothing.
"""
import argparse
import contextlib
import filecmp
import glob
import io
import json
import os
import re
import shutil
import sys
import tempfile

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_sixyear_intelligence as SY
import recurrence_model as RM

DERIVED = ('sixyear_families.json', 'sixyear_nodes.json')
CLASSES = {'EXACT_REPEAT', 'NEAR_REPEAT', 'UNIQUE'}

# A drive-letter or POSIX absolute path in a tool's source. The point is not to
# ban the character '/', it is to ban a path that exists on ONE machine.
ABSOLUTE_PATH_RX = re.compile(r"""['"](?:[A-Za-z]:[\\/]|/(?:tmp|home|Users|var)/)""")

WATCHED_SOURCES = ('build_sixyear_intelligence.py',
                   'sixyear_temporal_and_topics.py',
                   'extract_historical_questions.py')


def build(out_dir, spec_glob=None, intel_path=None):
    # The builder prints a full internal report. This file reports on the
    # builder, so its own narration is swallowed rather than interleaved.
    with contextlib.redirect_stdout(io.StringIO()):
        SY.main(out_dir,
                spec_glob or SY.SPEC_GLOB,
                intel_path or SY.INTEL_PATH)
    return (json.load(open(os.path.join(out_dir, 'sixyear_families.json'), encoding='utf-8')),
            json.load(open(os.path.join(out_dir, 'sixyear_nodes.json'), encoding='utf-8')))


# --------------------------------------------------------------------------- #
# Rules
# --------------------------------------------------------------------------- #

def rule_no_foreign_paths(_fams, _nodes, fails):
    for name in WATCHED_SOURCES:
        path = os.path.join(HERE, name)
        for i, line in enumerate(open(path, encoding='utf-8'), 1):
            if line.lstrip().startswith('#') or ABSOLUTE_PATH_RX.search(line) is None:
                continue
            fails.append(f'{name}:{i} hard-codes a machine-specific path: {line.strip()[:90]}')


def rule_double_build_identical(_fams, _nodes, fails):
    a, b = tempfile.mkdtemp(prefix='sy_a_'), tempfile.mkdtemp(prefix='sy_b_')
    try:
        build(a)
        build(b)
        for name in DERIVED:
            if not filecmp.cmp(os.path.join(a, name), os.path.join(b, name), shallow=False):
                fails.append(f'{name} differs between two builds from identical inputs')
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def rule_solved_papers_graduate(_fams, nodes, fails):
    solved_ids = {os.path.basename(f)[:-5] for f in glob.glob(SY.SPEC_GLOB)}
    for qid, n in nodes.items():
        if n['paper'] in solved_ids and n['status'] != 'SOLVED':
            fails.append(f'{qid}: {n["paper"]} has a canonical solved spec but is carried '
                         f'as {n["status"]}')
    store = json.load(open(SY.INTEL_PATH, encoding='utf-8'))
    graduated = sorted({p['paper_id'] for p in store['papers']} & solved_ids)
    if not graduated:
        fails.append('no paper in the historical store has a solved spec, so rule 3 is '
                     'currently vacuous -- the store has been pruned by hand again')


def rule_no_double_count(_fams, nodes, fails):
    status_of = {}
    for qid, n in nodes.items():
        prev = status_of.setdefault(n['paper'], n['status'])
        if prev != n['status']:
            fails.append(f'{n["paper"]} appears with two statuses: {prev} and {n["status"]}')
    seen = {}
    for qid, n in nodes.items():
        key = (n['paper'], n['q_no'])
        if key in seen:
            fails.append(f'{n["paper"]} {n["q_no"]} appears twice: {seen[key]} and {qid}')
        seen[key] = qid


def rule_no_early_solved(_fams, nodes, fails):
    for qid, n in nodes.items():
        if n['year'] <= 2022 and n['status'] == 'SOLVED':
            fails.append(f'{qid} is a {n["year"]} sitting marked SOLVED -- 2021/2022 are '
                         f'intelligence-only by standing policy')


def rule_stable_order_and_ids(_fams, nodes, fails):
    d = tempfile.mkdtemp(prefix='sy_o_')
    try:
        _, again = build(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    if list(nodes) != list(again):
        fails.append('node ordering is not stable across builds')
    if set(nodes) != set(again):
        fails.append('node identity is not stable across builds')


def rule_families_partition_nodes(fams, nodes, fails):
    members = []
    for f in fams:
        if f['class'] not in CLASSES:
            fails.append(f'family {f["family_id"]} carries unknown class {f["class"]!r}')
        if f['size'] != len(f['members']):
            fails.append(f'family {f["family_id"]} size {f["size"]} != {len(f["members"])} members')
        members.extend(f['members'])
    if len(members) != len(set(members)):
        fails.append('a question belongs to more than one family')
    if set(members) != set(nodes):
        missing = sorted(set(nodes) - set(members))[:3]
        fails.append(f'families do not cover every node; e.g. {missing}')


def rule_universe_adds_up(_fams, nodes, fails):
    papers = {}
    for n in nodes.values():
        papers[n['paper']] = n['status']
    solved_p = [p for p, s in papers.items() if s == 'SOLVED']
    intel_p = [p for p, s in papers.items() if s != 'SOLVED']
    spec_ct = len(glob.glob(SY.SPEC_GLOB))
    if len(solved_p) != spec_ct:
        fails.append(f'{len(solved_p)} solved papers in the layer but {spec_ct} canonical specs')
    store = json.load(open(SY.INTEL_PATH, encoding='utf-8'))
    expect_intel = len([p for p in store['papers'] if p['paper_id'] not in set(solved_p)])
    if len(intel_p) != expect_intel:
        fails.append(f'{len(intel_p)} intelligence-only papers but the store, after '
                     f'graduation, holds {expect_intel}')
    q_solved = sum(1 for n in nodes.values() if n['status'] == 'SOLVED')
    q_intel = len(nodes) - q_solved
    if q_solved + q_intel != len(nodes):
        fails.append('question totals do not sum to the node count')


RULES = (
    ('no machine-specific path in any six-year tool', rule_no_foreign_paths),
    ('a double build is byte-identical', rule_double_build_identical),
    ('a solved spec supersedes its historical record', rule_solved_papers_graduate),
    ('no sitting and no question is counted twice', rule_no_double_count),
    ('no 2021/2022 sitting is marked SOLVED', rule_no_early_solved),
    ('node ordering and identity are stable', rule_stable_order_and_ids),
    ('families partition the nodes, with known classes', rule_families_partition_nodes),
    ('the universe equals the sum of its parts', rule_universe_adds_up),
)


def run(fams, nodes, report=False):
    all_fails = []
    for label, fn in RULES:
        fails = []
        fn(fams, nodes, fails)
        if report:
            print('  %-52s %s' % (label, 'PASS' if not fails else 'FAIL'))
            for f in fails:
                print('      %s' % f)
        all_fails.extend(fails)
    return all_fails


# --------------------------------------------------------------------------- #
# Negative control
# --------------------------------------------------------------------------- #

def self_test():
    """Promote an intelligence-only paper to solved in a scratch tree.

    The paper must DISAPPEAR from the historical set. Then the rule is disabled
    and the same sitting must be counted TWICE -- which is what makes the rule
    load-bearing rather than decorative.
    """
    ok = True
    store = json.load(open(SY.INTEL_PATH, encoding='utf-8'))
    solved_ids = {os.path.basename(f)[:-5] for f in glob.glob(SY.SPEC_GLOB)}
    victim = next(p['paper_id'] for p in store['papers'] if p['paper_id'] not in solved_ids)

    kept = SY.historical_specs(solved_ids | {victim})
    gone = victim not in {d['paper_id'] for d in kept}
    print('  %-52s %s' % (f'{victim} promoted to solved -> excluded', 'PASS' if gone else 'FAIL'))
    ok &= gone

    base = SY.historical_specs(solved_ids)
    dropped = len(base) - len(kept)
    one = dropped == 1
    print('  %-52s %s' % (f'exactly one paper leaves the historical set ({dropped})',
                          'PASS' if one else 'FAIL'))
    ok &= one

    # Rule disabled: the sitting is now present on both sides at once.
    unguarded = SY.historical_specs(set())
    dupes = sorted({d['paper_id'] for d in unguarded} & solved_ids)
    fires = bool(dupes)
    print('  %-52s %s' % (f'without the rule, {len(dupes)} sitting(s) double-count',
                          'PASS' if fires else 'FAIL'))
    if not fires:
        print('      the store holds no solved sitting, so the guard cannot be shown to bite')
    ok &= fires

    # And a real build must not contain those duplicates.
    d = tempfile.mkdtemp(prefix='sy_s_')
    try:
        _, nodes = build(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    ghosts = sorted({n['paper'] for n in nodes.values()
                     if n['paper'] in dupes and n['status'] != 'SOLVED'})
    clean = not ghosts
    print('  %-52s %s' % ('the real build carries no historical ghost',
                          'PASS' if clean else 'FAIL %s' % ghosts))
    ok &= clean
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()

    if args.self_test:
        print('SIX-YEAR INTELLIGENCE self-test')
        sys.exit(0 if self_test() else 1)

    d = tempfile.mkdtemp(prefix='sy_r_')
    try:
        fams, nodes = build(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)

    fails = run(fams, nodes, report=True)
    papers = {n['paper']: n['status'] for n in nodes.values()}
    print('SIX-YEAR INTELLIGENCE %s  %d rule(s)  %d papers / %d questions  '
          '(%d solved / %d intelligence-only)'
          % ('PASS' if not fails else 'FAIL (%d)' % len(fails), len(RULES),
             len(papers), len(nodes),
             sum(1 for s in papers.values() if s == 'SOLVED'),
             sum(1 for s in papers.values() if s != 'SOLVED')))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
