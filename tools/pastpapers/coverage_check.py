#!/usr/bin/env python3
"""Prove the Solved QP home states coverage honestly.

The product is deliberately partial during controlled online testing, so the
home page must distinguish three things and invent a fourth for nobody:

    solved sitting          -> clickable card
    transcribed, unsolved   -> "Planned soon", NO link
    no examination held     -> "No sitting", distinct from the above
    not in the source set   -> ABSENT ENTIRELY, never fabricated

The last one is the reason this file exists. A month grid that renders all
twelve months would silently assert that a sitting exists for every month of the
current year, which is a factual claim about the examination that MIW cannot
make. Coverage is asserted from evidence only.

    python tools/pastpapers/coverage_check.py [--self-test]
"""
import argparse, glob, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_solvedqp_home as H
import recurrence_model as RM

FAILS = []


def fail(msg):
    FAILS.append(msg)
    print('[FAIL] %s' % msg)


def ok(msg):
    print('[ OK  ] %s' % msg)


def load():
    return [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(H.SPEC_GLOB))]


def check(specs, html):
    rows = H.coverage(specs)
    by_state = {}
    for r in rows:
        by_state.setdefault(r[3], []).append(r)

    # -- solved sittings are available and clickable --------------------------
    solved = {(d['year'], RM.MONTH_NUM[d['month']]) for d in specs
              if any(q.get('model_answer') for q in d['questions'])}
    got = {(r[0], r[1]) for r in by_state.get(H.AVAILABLE, [])}
    if got == solved:
        ok('%d solved sitting(s) marked AVAILABLE' % len(got))
    else:
        fail('AVAILABLE set disagrees with the specs: %s' % sorted(got ^ solved))
    for (_y, _m, month, _s, pid) in by_state.get(H.AVAILABLE, []):
        if 'href="/solvedQP/%s.html"' % pid not in html:
            fail('solved sitting %s is not clickable on the home page' % pid)
    ok('every AVAILABLE sitting links to its paper')

    # -- intake papers are Planned soon and carry NO answer link --------------
    intake = {(d['year'], RM.MONTH_NUM[d['month']]) for d in specs
              if not any(q.get('model_answer') for q in d['questions'])}
    got = {(r[0], r[1]) for r in by_state.get(H.PLANNED_SOON, [])}
    if got == intake:
        ok('%d intake sitting(s) marked PLANNED_SOON' % len(got))
    else:
        fail('PLANNED_SOON set disagrees with the specs: %s' % sorted(got ^ intake))
    for (_y, _m, _month, _s, pid) in by_state.get(H.PLANNED_SOON, []):
        if 'href="/solvedQP/%s.html"' % pid in html:
            fail('unsolved paper %s is linked as if an answer page existed' % pid)
    ok('no unsolved paper offers a link')

    # -- known-absent months are distinct from planned soon -------------------
    got = {(r[0], r[1]) for r in by_state.get(H.NO_SITTING, [])}
    # Compare against KNOWN_ABSENT RESTRICTED TO THE YEARS THE GRID RENDERS.
    # The coverage section is the route into a solved paper, so build_solvedqp_home
    # deliberately draws only years that hold a paper in the spec set (see the
    # comment on `years` in its coverage_rows). Extending KNOWN_ABSENT back to 2021
    # to describe the question-only intelligence years therefore added months that
    # the grid must NOT draw -- 2021 would otherwise be a row of nothing but two
    # "No sitting" chips, and 2022 a row of one. Those years belong to the
    # examination-history matrix below the grid, not to coverage. Comparing against
    # the unrestricted set asserted that the builder should render a year it is
    # correct to omit.
    solved_years = {d['year'] for d in specs}
    expect = {k for k in H.KNOWN_ABSENT if k[0] in solved_years}
    if got == expect:
        ok('%d known-absent month(s) marked NO_SITTING across %d rendered year(s)'
           % (len(got), len(solved_years)))
    else:
        fail('NO_SITTING set disagrees with KNOWN_ABSENT: %s' % sorted(got ^ expect))
    # Distinctness can only be asserted where both states actually exist. Every
    # sitting in the set was solved at QP2408, so there is no PLANNED_SOON row
    # left to render and "Planned soon" legitimately disappears from the page.
    # Asserting it unconditionally turned a COMPLETE corpus into a coverage
    # failure. Assert the label that must be there, and assert the other only
    # while something is still unsolved.
    planned = by_state.get(H.PLANNED_SOON, [])
    if 'No sitting' not in html:
        fail('known-absent months are not labelled "No sitting" on the page')
    elif not planned:
        ok('"No sitting" renders; no "Planned soon" state exists (every '
           'evidenced sitting is solved)')
    elif 'Planned soon' in html:
        ok('"No sitting" and "Planned soon" are distinct labels on the page')
    else:
        fail('the two unavailable states are not distinctly labelled')

    # -- nothing is fabricated ------------------------------------------------
    known = ({(d['year'], RM.MONTH_NUM[d['month']]) for d in specs}
             | set(H.KNOWN_ABSENT))
    invented = [(r[0], r[1]) for r in rows if (r[0], r[1]) not in known]
    if invented:
        fail('coverage invented sitting(s) with no source evidence: %s' % invented)
    else:
        ok('no sitting is rendered without a spec or a known-absent record')

    # The sharpest case: the current year must not be filled out to December.
    latest_year = max(y for y, _ in known)
    months_shown = sorted(m for (y, m) in [(r[0], r[1]) for r in rows] if y == latest_year)
    months_known = sorted(m for (y, m) in known if y == latest_year)
    if months_shown == months_known:
        ok('%d shows only its %d evidenced month(s), not a full calendar'
           % (latest_year, len(months_shown)))
    else:
        fail('%d coverage does not match its evidence' % latest_year)

    # -- the headline count still describes SOLVED papers ---------------------
    n_solved = len(H.solved_sittings(specs))
    if '<b>%d</b><span>solved sittings</span>' % n_solved in html:
        ok('headline count describes the %d solved paper(s), not total coverage'
           % n_solved)
    else:
        fail('headline solved-sitting count is wrong or missing')


def self_test(specs, html):
    """Mutate the BUILDER and require the checks to notice.

    Injecting an extra spec would not test anything -- a spec is evidence, so a
    sitting derived from one is legitimate by construction. The failure this
    guards against is the builder emitting a month that no spec and no
    known-absent record supports, so that is what is simulated here.
    """
    print('\n-- self-test: a fabricated sitting must be caught --')
    real = H.coverage

    def lying_coverage(s):
        return real(s) + [(2099, 12, 'December', H.PLANNED_SOON, 'QP9912')]

    before = len(FAILS)
    H.coverage = lying_coverage
    try:
        check(specs, html)
    finally:
        H.coverage = real
    caught = len(FAILS) > before
    del FAILS[before:]          # discard the synthetic failures
    if caught:
        ok('self-test: fabricated sitting was caught')
    else:
        fail('self-test: fabricated sitting was NOT caught')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()

    specs = load()
    home = os.path.join(H.REPO_ROOT, 'solvedQP', 'index.html')
    if not os.path.exists(home):
        print('solvedQP/index.html not built -- run build_solvedqp_home.py first')
        return 1
    with open(home, encoding='utf-8') as fh:
        html = fh.read()

    check(specs, html)
    if args.self_test:
        self_test(specs, html)

    print()
    if FAILS:
        print('COVERAGE CHECK FAIL -- %d problem(s)' % len(FAILS))
        return 1
    print('COVERAGE CHECK PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
