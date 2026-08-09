#!/usr/bin/env python3
"""One command to build and check the whole Written Questions product.

Usage:
  python tools/pastpapers/run_toolchain.py [--publish] [--self-test] [--gated]

Runs, in dependency order:
    SPEC          validate_spec.py      every spec under specs/
    PAPER BUILD   build_paper.py        one interactive page per paper
    INDEX BUILD   build_index.py        manifest + index.html + topics-<year>.html
    UI BEHAVIOUR  ui_behaviour_test.cjs search/bookmarks/progress (skipped if no node)
    QYEAR BUILD   build_questions_year.py   questions-<year>.html, answers excluded
    QYEAR CHECK   questions_year_check.py   54-question integrity + answer-leak sweep
    SAMPLE BUILD  build_sample.py           free conversion sample from a projection
    SAMPLE CHECK  sample_check.py           withheld content absent from shipped bytes
    KNOWN TRAPS   known_traps_check.py  traps we have already been caught by
    HEALTH        health_check.py       product coherence, links, safety, review state
    AUDIT         audit_paper.py        each page faithful to its spec

Exit code is non-zero if any stage fails. Warnings stay warnings.

This is the command a future production agent runs. Keep its output stable.
"""
import argparse, glob, io, json, os, subprocess, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
PP = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')
PY = sys.executable


def run(label, argv, verbose):
    r = subprocess.run([PY] + argv, cwd=REPO_ROOT, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    out = (r.stdout or '') + (r.stderr or '')
    warns = out.count('[WARN ]')
    status = 'PASS' if r.returncode == 0 else 'FAIL'
    print('%-13s %s%s' % (label, status, '  (%d warning(s))' % warns if warns else ''))
    if verbose or r.returncode != 0:
        for line in out.rstrip('\n').split('\n'):
            print('    %s' % line)
    return r.returncode, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--publish', action='store_true',
                    help='build student-facing pages (indexable, no production metadata)')
    ap.add_argument('--gated', action='store_true', help='add the access gate')
    ap.add_argument('--self-test', action='store_true',
                    help='positive-control the health and trap checks')
    ap.add_argument('-v', '--verbose', action='store_true')
    args = ap.parse_args()

    specs = sorted(glob.glob(os.path.join(PP, 'specs', '*.json')))
    if not specs:
        print('ERROR: no specs found under meoclass1/pastpapers/specs/')
        sys.exit(1)

    # The spec is the source of truth for which pages must exist. Every later
    # stage derives its targets from this list rather than from a filename glob.
    paper_ids = [json.load(open(sp, encoding='utf-8'))['paper_id'] for sp in specs]

    mode = 'PUBLISH' if args.publish else 'review (noindex)'
    print('MIW Written Questions & Answers -- toolchain')
    print('mode: %s%s   specs: %d' % (mode, ', gated' if args.gated else '', len(specs)))
    print('-' * 58)

    rc_total, warn_total = 0, 0
    T = os.path.join('tools', 'pastpapers')

    for sp in specs:
        rel = os.path.relpath(sp, REPO_ROOT)
        rc, w = run('SPEC', [os.path.join(T, 'validate_spec.py'), rel], args.verbose)
        rc_total += rc
        warn_total += w

    for sp in specs:
        rel = os.path.relpath(sp, REPO_ROOT)
        argv = [os.path.join(T, 'build_paper.py'), rel]
        if args.publish:
            argv.append('--publish')
        if args.gated:
            argv.append('--gated')
        rc, w = run('PAPER BUILD', argv, args.verbose)
        rc_total += rc
        warn_total += w

    argv = [os.path.join(T, 'build_index.py')]
    if args.publish:
        argv.append('--publish')
    rc, w = run('INDEX BUILD', argv, args.verbose)
    rc_total += rc
    warn_total += w

    # Optional UI stage: exercises search, bookmarks and progress against the
    # generated page. Skipped cleanly where node is unavailable -- the product
    # itself has no node dependency.
    #
    # The pages under test are derived from the specs, never from a filename
    # glob. A glob that matches nothing sums to a zero return code and reports
    # PASS, so a paper rename would silently delete this entire stage while
    # still printing success. Deriving from the specs makes a missing page a
    # hard failure instead.
    import shutil
    if shutil.which('node'):
        node_rc, tested = 0, 0
        for pid in paper_ids:
            pg = os.path.join(PP, '%s.html' % pid)
            if not os.path.exists(pg):
                print('    MISSING generated page for spec %s: %s'
                      % (pid, os.path.relpath(pg, REPO_ROOT)))
                node_rc += 1
                continue
            r = subprocess.run(['node', os.path.join(T, 'ui_behaviour_test.cjs'),
                                os.path.relpath(pg, REPO_ROOT)],
                               cwd=REPO_ROOT, capture_output=True, text=True,
                               encoding='utf-8', errors='replace')
            node_rc += r.returncode
            tested += 1
            if args.verbose or r.returncode:
                print((r.stdout or '') + (r.stderr or ''))
        if not tested:
            print('    no paper page was exercised -- refusing to report PASS')
            node_rc += 1
        print('%-13s %-5s %d page(s)'
              % ('UI BEHAVIOUR', 'PASS' if node_rc == 0 else 'FAIL', tested))
        rc_total += node_rc
    else:
        print('%-13s SKIP  (node not available; product has no node dependency)'
              % 'UI BEHAVIOUR')

    # Questions-only year sheet and the free conversion sample. Both are
    # generated from the same specs and both are checked immediately after
    # being built, because the thing that can go wrong with them is not a
    # broken page but a page that quietly gives the paid product away.
    argv = [os.path.join(T, 'build_questions_year.py')]
    if args.publish:
        argv.append('--publish')
    rc, w = run('QYEAR BUILD', argv, args.verbose)
    rc_total += rc
    warn_total += w

    rc, w = run('QYEAR CHECK', [os.path.join(T, 'questions_year_check.py')], args.verbose)
    rc_total += rc
    warn_total += w

    if glob.glob(os.path.join(PP, 'sample', '*.sample.json')):
        argv = [os.path.join(T, 'build_sample.py')]
        if args.publish:
            argv.append('--publish')
        rc, w = run('SAMPLE BUILD', argv, args.verbose)
        rc_total += rc
        warn_total += w

        rc, w = run('SAMPLE CHECK', [os.path.join(T, 'sample_check.py')], args.verbose)
        rc_total += rc
        warn_total += w

    # ---- paid Solved QP delivery surface -------------------------------
    # Same specs, projected into /solvedQP/ for paying customers. Built and
    # then immediately checked, because the failure that matters here is not
    # a broken page but a page that leaks the third-party source copy's
    # recurrence annotations, an authoring verdict, or the review banner.
    for sp in specs:
        rel = os.path.relpath(sp, REPO_ROOT)
        rc, w = run('SOLVEDQP BLD', [os.path.join(T, 'build_paper.py'), rel, '--deliver'],
                    args.verbose)
        rc_total += rc
        warn_total += w

    rc, w = run('SOLVEDQP QY', [os.path.join(T, 'build_questions_year.py'), '--deliver'],
                args.verbose)
    rc_total += rc
    warn_total += w

    rc, w = run('SOLVEDQP HOME', [os.path.join(T, 'build_solvedqp_home.py')], args.verbose)
    rc_total += rc
    warn_total += w

    argv = [os.path.join(T, 'solvedqp_check.py')]
    if args.self_test:
        argv.append('--self-test')
    rc, w = run('SOLVEDQP CHK', argv, args.verbose)
    rc_total += rc
    warn_total += w

    argv = [os.path.join(T, 'known_traps_check.py')]
    if args.self_test:
        argv.append('--self-test')
    rc, w = run('KNOWN TRAPS', argv, args.verbose)
    rc_total += rc
    warn_total += w

    argv = [os.path.join(T, 'health_check.py')]
    if args.publish:
        argv.append('--publish')
    if args.self_test:
        argv.append('--self-test')
    rc, w = run('HEALTH', argv, args.verbose)
    rc_total += rc
    warn_total += w

    for sp in specs:
        rel = os.path.relpath(sp, REPO_ROOT)
        argv = [os.path.join(T, 'audit_paper.py'), rel]
        if args.gated:
            argv.append('--require-gate')
        if args.publish:
            argv.append('--publish')
        rc, w = run('AUDIT', argv, args.verbose)
        rc_total += rc
        warn_total += w

    print('-' * 58)
    print('%s   %d warning(s)' % ('ALL STAGES PASS' if rc_total == 0 else 'FAILURES PRESENT',
                                  warn_total))
    sys.exit(1 if rc_total else 0)


if __name__ == '__main__':
    main()
