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
    REUSE MAP     build_reuse_map.py --check  cross-year map + source inventory current
    RECURRENCE    recurrence_check.py   provenance boundary: no host or authoring
                                        recurrence on any shipped surface, plus the
                                        marks-safe stem normalisation cases
    KNOWN TRAPS   known_traps_check.py  traps we have already been caught by
    TEMPORAL      temporal_sweep.py     post-sitting dates and donor prose Q-refs,
                                        reported as CANDIDATES for adjudication
    HEALTH        health_check.py       product coherence, links, safety, review state
    AUDIT         audit_paper.py        each page faithful to its spec
    HOME CONTRACT solvedqp_home_contract_test.py
                                        /solvedQP/index.html owns layout and owns
                                        no product truth: counts, chips, cards,
                                        year links and update rows are recomputed
                                        from the specs and must match the bytes
    DELIVERY      delivery_gate.py      every artefact the specs imply exists AND
                                        is tracked by Git. Runs last, and is the
                                        only stage that consults the index rather
                                        than the working tree -- an untracked
                                        generated page keeps every other stage
                                        green while never reaching the deploy.

    SURFACE       surface_impact.py     only when --base <ref> is given: which
                                        public / paid / commercial surfaces this
                                        change moved. A finalisation report.

Exit code is non-zero if any stage fails. Warnings stay warnings.

TEMPORAL does not fail the build. A post-sitting date can be correct for its
sitting, so its output is a candidate list, and whether any given flag blocks
READY is Claude's judgement under TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md.
SURFACE never runs without an explicit --base: there is no safe default ref, and
guessing one would be exactly the invisible Git assumption it exists to prevent.

This is the command a future production agent runs. Keep its output stable.
"""
import argparse, glob, io, json, os, subprocess, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import is_intake  # noqa: E402
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
PP = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')
PY = sys.executable


def run(label, argv, verbose, echo=None):
    """Run a stage. ``echo`` is a predicate over output lines that must be shown
    even on a passing quiet run -- used by the PIL stages, whose whole value is
    the report they print rather than their return code."""
    r = subprocess.run([PY] + argv, cwd=REPO_ROOT, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    out = (r.stdout or '') + (r.stderr or '')
    warns = out.count('[WARN ]')
    status = 'PASS' if r.returncode == 0 else 'FAIL'
    print('%-13s %s%s' % (label, status, '  (%d warning(s))' % warns if warns else ''))
    if verbose or r.returncode != 0:
        for line in out.rstrip('\n').split('\n'):
            print('    %s' % line)
    elif echo:
        for line in out.rstrip('\n').split('\n'):
            if echo(line):
                print('    %s' % line)
    return r.returncode, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--publish', action='store_true',
                    help='build student-facing pages (indexable, no production metadata)')
    ap.add_argument('--gated', action='store_true', help='add the access gate')
    ap.add_argument('--self-test', action='store_true',
                    help='positive-control the health, trap and PIL checks')
    ap.add_argument('--strict', action='store_true',
                    help='publication gate: a generated artefact that is '
                         'unstaged also fails DELIVERY, not just an untracked '
                         'or absent one')
    ap.add_argument('--base', help='base git ref: adds the SURFACE IMPACT '
                                   'finalisation report. No default -- omitted, '
                                   'the stage does not run.')
    ap.add_argument('--target', help='paper id this session was meant to change '
                                     '(SURFACE IMPACT only)')
    ap.add_argument('-v', '--verbose', action='store_true')
    args = ap.parse_args()

    specs = sorted(glob.glob(os.path.join(PP, 'specs', '*.json')))
    if not specs:
        print('ERROR: no specs found under meoclass1/pastpapers/specs/')
        sys.exit(1)

    # The spec is the source of truth for which pages must exist. Every later
    # stage derives its targets from this list rather than from a filename glob.
    #
    # INTAKE specs -- questions transcribed, no answers authored -- are split out
    # here. They are validated and they feed the year sheet and the manifest, but
    # they have no paper page, so building or auditing one is not a thing that
    # can succeed. Splitting once, from the specs, keeps every later stage
    # consistent about which papers are products.
    loaded = [(sp, json.load(open(sp, encoding='utf-8'))) for sp in specs]
    paper_ids = [d['paper_id'] for _, d in loaded]
    solved = [(sp, d) for sp, d in loaded if not is_intake(d)]
    intake = [d['paper_id'] for _, d in loaded if is_intake(d)]

    mode = 'PUBLISH' if args.publish else 'review (noindex)'
    print('MIW Written Questions & Answers -- toolchain')
    print('mode: %s%s   specs: %d%s'
          % (mode, ', gated' if args.gated else '', len(specs),
             '   (%d intake, questions only: %s)' % (len(intake), ', '.join(intake))
             if intake else ''))
    print('-' * 58)

    rc_total, warn_total = 0, 0
    T = os.path.join('tools', 'pastpapers')

    for sp in specs:
        rel = os.path.relpath(sp, REPO_ROOT)
        rc, w = run('SPEC', [os.path.join(T, 'validate_spec.py'), rel], args.verbose)
        rc_total += rc
        warn_total += w

    for sp, _ in solved:
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
        for _, d in solved:
            pid = d['paper_id']
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

    # The cross-year map and the source inventory are DERIVED from the specs.
    # Checking rather than rebuilding here keeps this command read-only over
    # documentation, while still failing the build if either has gone stale --
    # which is what a hand-edit or an unregenerated spec change looks like.
    rc, w = run('REUSE MAP', [os.path.join(T, 'build_reuse_map.py'), '--check'], args.verbose)
    rc_total += rc
    warn_total += w

    # Donor readiness is derived from the current built set, so --check alone
    # only proves the document matches the derivation -- not that the derivation
    # is still live. The self-test mutates the built set and asserts the tier
    # moves with it, which is the property that regressed.
    if args.self_test:
        rc, w = run('REUSE SELFTEST',
                    [os.path.join(T, 'build_reuse_map.py'), '--self-test'], args.verbose)
        rc_total += rc
        warn_total += w

    # The recurrence provenance boundary. Runs after every page exists, because
    # two of its three layers sweep generated bytes rather than specs.
    argv = [os.path.join(T, 'recurrence_check.py')]
    if args.self_test:
        argv.append('--self-test')
    rc, w = run('RECURRENCE', argv, args.verbose)
    rc_total += rc
    warn_total += w

    # ---- paid Solved QP delivery surface -------------------------------
    # The same canonical specs, projected into /solvedQP/ for paying
    # customers. Built and then immediately checked, because the failure that
    # matters here is not a broken page but a page that leaks the third-party
    # source copy's recurrence annotations, an authoring verdict, or the
    # Founder review banner into a product someone paid for.
    #
    # This runs AFTER the review build and its checks, so a spec that cannot
    # produce a sound review page never reaches the delivery surface.
    for sp in specs:
        rel = os.path.relpath(sp, REPO_ROOT)
        rc, w = run('SOLVEDQP BLD',
                    [os.path.join(T, 'build_paper.py'), rel, '--deliver'], args.verbose)
        rc_total += rc
        warn_total += w

    rc, w = run('SOLVEDQP QY',
                [os.path.join(T, 'build_questions_year.py'), '--deliver'], args.verbose)
    rc_total += rc
    warn_total += w

    # The delivery manifest MUST be built before the home page, which renders
    # its "latest updates" strip from the same derivation, and before the
    # search and health checks, which read the file. Ordering it here is what
    # makes the manifest authoritative rather than merely present.
    argv = [os.path.join(T, 'build_solvedqp_manifest.py')]
    rc, w = run('SOLVEDQP MFST', argv, args.verbose)
    rc_total += rc
    warn_total += w

    if args.self_test:
        rc, w = run('SOLVEDQP MFST ST',
                    [os.path.join(T, 'build_solvedqp_manifest.py'), '--self-test'],
                    args.verbose)
        rc_total += rc
        warn_total += w

    rc, w = run('SOLVEDQP HOME', [os.path.join(T, 'build_solvedqp_home.py')], args.verbose)
    rc_total += rc
    warn_total += w

    # The Study Topic Map -- "what should I study?" -- a static projection of
    # the same specs through topic_taxonomy. Built after the manifest because
    # its contract test proves every leaf equals the manifest's structured
    # `?topic=&domain=` filter set exactly.
    rc, w = run('TOPIC MAP', [os.path.join(T, 'build_topic_map.py')], args.verbose)
    rc_total += rc
    warn_total += w

    # Search is a property of the manifest, so it is tested here rather than in
    # a browser. See solvedqp_search_test.py.
    rc, w = run('SOLVEDQP FIND', [os.path.join(T, 'solvedqp_search_test.py')], args.verbose)
    rc_total += rc
    warn_total += w

    # The home page owns layout and owns no product truth. Every count, chip,
    # card, year link and update row on the shipped bytes is recomputed here
    # from the specs and cross-checked against the manifest, so a hand-edit to
    # the generated HTML fails the build instead of surviving until the next
    # rebuild silently reverts it.
    argv = [os.path.join(T, 'solvedqp_home_contract_test.py')]
    if args.self_test:
        argv.append('--self-test')
    rc, w = run('SOLVEDQP HOME CT', argv, args.verbose)
    rc_total += rc
    warn_total += w

    argv = [os.path.join(T, 'topic_map_test.py')]
    if args.self_test:
        argv.append('--self-test')
    rc, w = run('TOPIC MAP CT', argv, args.verbose)
    rc_total += rc
    warn_total += w

    # The six-year lineage layer is INTERNAL and its output is gitignored, so
    # nothing else in this toolchain would notice it rotting. It is checked
    # here because its two inputs ARE committed, and because it once read its
    # historical input from a session scratchpad, which made it unbuildable.
    # The rule with teeth is graduation: a sitting that gains a solved spec
    # must leave the intelligence-only set by rule, not by hand.
    argv = [os.path.join(T, 'sixyear_intelligence_test.py')]
    if args.self_test:
        argv.append('--self-test')
    rc, w = run('SIXYEAR INTEL', argv, args.verbose)
    rc_total += rc
    warn_total += w

    # The complete January paper shown to existing ORAL subscribers. Built
    # from the same canonical spec as the paid product, so it cannot drift
    # from what it is advertising.
    promo_spec = os.path.join(PP, 'specs', 'QP2601.json')
    if os.path.exists(promo_spec):
        rc, w = run('ORALPROMO BLD',
                    [os.path.join(T, 'build_paper.py'),
                     os.path.relpath(promo_spec, REPO_ROOT), '--oral-promo'], args.verbose)
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

    # The delivery health check, run against THIS tree. In production the same
    # script runs daily against main's tarball and emails the result; running
    # it here means a defect it would report tomorrow fails the build today.
    rc, w = run('SOLVEDQP HLTH',
                [os.path.join(T, 'solvedqp_health_check.py'), '--local', '--no-email'],
                args.verbose)
    rc_total += rc
    warn_total += w

    if args.self_test:
        rc, w = run('SOLVEDQP HLTH ST',
                    [os.path.join(T, 'solvedqp_health_check.py'), '--self-test'],
                    args.verbose)
        rc_total += rc
        warn_total += w

    # Production Intelligence Layer. Detection only -- PIL FLAGS, CLAUDE
    # ADJUDICATES -- so the sweep's candidate list never fails the build. What
    # it must do is be impossible to miss, which is why the summary counts and
    # every out-of-range prose Q-reference print on a quiet run too.
    #
    # An out-of-range reference is the one case that is mechanically certain
    # rather than a candidate: the prose points at a question number this paper
    # does not have, which no sitting-date argument can excuse.
    if args.self_test:
        rc, w = run('TEMPORAL ST', [os.path.join(T, 'temporal_sweep.py'), '--self-test'],
                    args.verbose)
        rc_total += rc
        warn_total += w
        rc, w = run('SURFACE ST', [os.path.join(T, 'surface_impact.py'), '--self-test'],
                    args.verbose)
        rc_total += rc
        warn_total += w

    rc, w = run('TEMPORAL', [os.path.join(T, 'temporal_sweep.py')], args.verbose,
                echo=lambda l: (l.startswith('temporal sweep:')
                                or l.strip().startswith(('INTERNAL_QREF',
                                                         'POST_SITTING'))
                                or 'INTERNAL_QREF_OUT_OF_RANGE' in l))
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

    for sp, _ in solved:
        rel = os.path.relpath(sp, REPO_ROOT)
        argv = [os.path.join(T, 'audit_paper.py'), rel]
        if args.gated:
            argv.append('--require-gate')
        if args.publish:
            argv.append('--publish')
        rc, w = run('AUDIT', argv, args.verbose)
        rc_total += rc
        warn_total += w

    # ---- delivery artefact completeness --------------------------------
    # LAST, because it asks whether everything the earlier stages BUILT has
    # actually reached Git. Every check above reads the working tree, so all of
    # them stay green while a generated public page sits untracked and never
    # deploys. This is the only stage that consults the index rather than the
    # filesystem, and it is the reason a paper can no longer go live on every
    # surface except the one a reader opens.
    #
    # --strict (with --publish) is the pre-commit gate: there, an artefact that
    # is tracked but unstaged is also a failure, because the bytes about to be
    # committed are not the bytes just built. Without --strict an unstaged
    # artefact is a warning, since that is the normal state mid-session.
    if args.self_test:
        rc, w = run('DELIVERY ST', [os.path.join(T, 'delivery_gate.py'), '--self-test'],
                    args.verbose)
        rc_total += rc
        warn_total += w
        rc, w = run('DELIVERY DERIV',
                    [os.path.join(T, 'delivery_gate.py'), '--verify-derivation'],
                    args.verbose, echo=lambda l: l.startswith(('  UNEXPECTED', '  NOT BUILT')))
        rc_total += rc
        warn_total += w

    argv = [os.path.join(T, 'delivery_gate.py')]
    if args.strict:
        argv.append('--strict')
    rc, w = run('DELIVERY', argv, args.verbose,
                echo=lambda l: l.lstrip().startswith(('ABSENT', 'UNTRACKED', 'UNSTAGED')))
    rc_total += rc
    warn_total += w

    # Finalisation only, and only against a ref the caller supplied. Its whole
    # report is the point, so it always echoes rather than only on --verbose.
    if args.base:
        argv = [os.path.join(T, 'surface_impact.py'), '--base', args.base]
        if args.target:
            argv += ['--target', args.target]
        rc, w = run('SURFACE', argv, args.verbose, echo=lambda l: True)
        rc_total += rc
        warn_total += w

    print('-' * 58)
    print('%s   %d warning(s)' % ('ALL STAGES PASS' if rc_total == 0 else 'FAILURES PRESENT',
                                  warn_total))
    sys.exit(1 if rc_total else 0)


if __name__ == '__main__':
    main()
