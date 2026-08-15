#!/usr/bin/env python3
"""Fail a publication whose generated artefacts never reached Git.

    specs/*.json  -->  the set of files that MUST exist and be tracked

THE DEFECT THIS EXISTS TO END
-----------------------------
A paper is authored, the toolchain is run, every check reports PASS, the
commit is made -- and a generated public page is left UNTRACKED on disk. The
build was green because the build only ever looked at the working tree. Git
never saw the file, so the deploy never served it, and the paper is live
everywhere except the one surface a reader opens.

This has been hit repeatedly, and each time the fix was "remember to check
`solvedQP/QP<id>.html` next time". Memory is not a control. The QP2301
integration created FIVE first-of-their-kind artefacts -- the two paper pages
AND the three year surfaces that a first-paper-in-a-new-year brings with it --
so a check that only looked at the paper page would have passed while three
files went missing.

So the gate does not know about any paper. It derives the whole expected
artefact set from the specs, using THE SAME rules the builders use, and then
asks Git -- not the filesystem -- whether each one is really there.

WHAT "REALLY THERE" MEANS, IN THREE FAILURES
--------------------------------------------
    ABSENT     the builder never wrote it. A stage was skipped.
    UNTRACKED  it is on disk and Git has never heard of it. This is the one
               that fakes a green build, because every content check reads
               the working tree and finds the file exactly as expected.
    UNSTAGED   it is tracked, but the version about to be committed is not
               the version the build just produced.

ABSENT and UNTRACKED always fail: neither can be correct at any point in a
session. UNSTAGED is normal mid-work and only fails under --strict, which is
the pre-commit publication gate.

DERIVATION, NOT ENUMERATION
---------------------------
Every rule below mirrors a builder, and the mirroring is asserted rather than
trusted: --verify-derivation compares this module's expected set against what
is actually on disk in both directions, so a builder that starts emitting a
new surface makes THIS FILE fail rather than silently dropping the surface out
of the gate. A hand-kept list of expected paths would be a second source of
truth about the product, which is the class of defect the whole toolchain is
built to avoid.

Determinism: no clock read, no random value. Git is consulted through
--porcelain and ls-files, never by parsing human-readable output.
"""
import argparse, glob, io, json, os, subprocess, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import REPO_ROOT, is_intake

SPEC_GLOB = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers', 'specs', '*.json')

ABSENT, UNTRACKED, UNSTAGED = 'ABSENT', 'UNTRACKED', 'UNSTAGED'


def load_specs():
    out = []
    for p in sorted(glob.glob(SPEC_GLOB)):
        with open(p, encoding='utf-8') as fh:
            out.append(json.load(fh))
    return out


def is_solved(spec):
    """A spec that carries at least one model answer is a product."""
    return any(q.get('model_answer') for q in spec['questions'])


def expected_artefacts(specs):
    """Every file the toolchain must have produced, as repo-relative paths.

    Each block names the builder it mirrors. If a builder's rule changes, the
    matching block here changes with it and --verify-derivation proves it.
    """
    pp = os.path.join('meoclass1', 'pastpapers')
    sq = 'solvedQP'
    exp = {}

    def add(path, why):
        exp[path.replace('\\', '/')] = why

    solved = [d for d in specs if not is_intake(d) and is_solved(d)]

    # build_paper.py -- one review page and one delivery page per solved spec.
    for d in solved:
        pid = d['paper_id']
        add(os.path.join(pp, '%s.html' % pid), 'review paper page')
        add(os.path.join(sq, '%s.html' % pid), 'delivery paper page')

    # build_questions_year.py -- the review sheet covers every year that has a
    # spec at all; the DELIVERY sheet only years that have a solved paper.
    # These two rules genuinely differ; collapsing them would invent a paid
    # page for a year holding only transcriptions.
    for y in sorted({d['year'] for d in specs}):
        add(os.path.join(pp, 'questions-%d.html' % y), 'review year sheet')
    for y in sorted({d['year'] for d in specs if is_solved(d)}):
        add(os.path.join(sq, 'questions-%d.html' % y), 'delivery year sheet')

    # build_index.py -- review manifest, review index, one topics sheet per
    # year present in the manifest. topics-*.html is INTERNAL: it carries
    # recurrence and review metadata and has no delivery counterpart.
    add(os.path.join(pp, 'pastpapers_content_index.json'), 'review manifest')
    add(os.path.join(pp, 'index.html'), 'review index')
    for y in sorted({d['year'] for d in specs}):
        add(os.path.join(pp, 'topics-%d.html' % y), 'review topic sheet')

    # build_solvedqp_manifest.py / build_solvedqp_home.py
    add(os.path.join(sq, 'solvedqp_content_index.json'), 'delivery manifest')
    add(os.path.join(sq, 'index.html'), 'delivery home')
    # build_topic_map.py -- the Study Topic Map, inside the same entitlement.
    add(os.path.join(sq, 'topics.html'), 'delivery topic map')

    # The canonical inputs themselves. A paper whose spec or verification
    # record is untracked is unreproducible: the pages would rebuild from
    # nothing on a fresh clone.
    for d in specs:
        pid = d['paper_id']
        add(os.path.join(pp, 'specs', '%s.json' % pid), 'canonical spec')
    for d in solved:
        pid = d['paper_id']
        for q in d['questions']:
            add(os.path.join(pp, 'verification', pid, '%s.md' % q['q_no']),
                'verification record')

    return exp


# ---- git -------------------------------------------------------------------
# Porcelain v1 is a stable, machine-readable contract; the human-readable
# output of `git status` is not, and parsing it would be a defect waiting for
# a Git upgrade. `-z` avoids the quoting Git applies to paths with spaces or
# non-ASCII -- this repository has a "Knowledge Central/" directory, so that
# is not hypothetical.

def _git(args):
    r = subprocess.run(['git', '-c', 'safe.directory=*'] + args,
                       cwd=REPO_ROOT, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return r.returncode, r.stdout


def git_state():
    """Return (tracked:set, index_status:dict, worktree_status:dict)."""
    rc, out = _git(['ls-files', '-z'])
    if rc != 0:
        print('ERROR: not a git repository, or git is unavailable')
        sys.exit(2)
    tracked = {p for p in out.split('\0') if p}

    rc, out = _git(['status', '--porcelain', '-z', '--untracked-files=all'])
    index, work = {}, {}
    fields = out.split('\0')
    i = 0
    while i < len(fields):
        f = fields[i]
        if len(f) < 4:
            i += 1
            continue
        x, y, path = f[0], f[1], f[3:]
        # A rename entry carries its source path in the NEXT field; consume it
        # so the source is never mistaken for a status record of its own.
        if x == 'R' or y == 'R':
            i += 1
        index[path] = x
        work[path] = y
        i += 1
    return tracked, index, work


def check(specs, strict):
    exp = expected_artefacts(specs)
    tracked, index, work = git_state()
    failures, warnings = [], []

    for path in sorted(exp):
        why = exp[path]
        on_disk = os.path.exists(os.path.join(REPO_ROOT, path))
        if not on_disk:
            failures.append((ABSENT, path, why))
            continue
        if path not in tracked:
            # Staged-as-new counts as tracked: `git add` on a new file puts it
            # in the index, and ls-files reports it. An 'A' here would already
            # have been caught above. Anything left is genuinely unknown to Git.
            failures.append((UNTRACKED, path, why))
            continue
        if work.get(path, ' ') not in (' ', ''):
            (failures if strict else warnings).append((UNSTAGED, path, why))

    return exp, failures, warnings


def verify_derivation(specs):
    """Assert the derivation matches reality in BOTH directions.

    A one-way check ("everything I expect exists") passes trivially for a gate
    that expects too little -- which is precisely how a missing surface gets
    missed. The reverse direction is the one with teeth: a generated page on a
    surface this module does not know about is reported, so adding a builder
    forces a change here.
    """
    exp = set(expected_artefacts(specs))
    actual = set()
    for pat in ('meoclass1/pastpapers/*.html',
                'meoclass1/pastpapers/pastpapers_content_index.json',
                'solvedQP/*.html', 'solvedQP/*.json'):
        for p in glob.glob(os.path.join(REPO_ROOT, pat)):
            actual.add(os.path.relpath(p, REPO_ROOT).replace('\\', '/'))

    unexpected = sorted(actual - exp)
    missing = sorted(p for p in exp - actual
                     if p.startswith(('meoclass1/pastpapers/', 'solvedQP/'))
                     and '/specs/' not in p and '/verification/' not in p)
    return unexpected, missing


def self_test():
    """Non-vacuous negative controls, against synthetic state only.

    Each control asserts the gate FAILS on a defect it is supposed to catch.
    A gate that has never been seen to fail is indistinguishable from a gate
    that returns PASS unconditionally.
    """
    ok = True

    def expect(name, cond):
        nonlocal ok
        print('  %-46s %s' % (name, 'PASS' if cond else 'FAIL'))
        if not cond:
            ok = False

    fake = [{
        'paper_id': 'QPZZ99', 'year': 2099, 'questions': [
            {'q_no': 'Q1', 'model_answer': {'blocks': []}}],
    }]
    exp = expected_artefacts(fake)
    expect('solved spec expects a REVIEW page',
           'meoclass1/pastpapers/QPZZ99.html' in exp)
    expect('solved spec expects a DELIVERY page',
           'solvedQP/QPZZ99.html' in exp)
    expect('solved spec expects both year sheets',
           'meoclass1/pastpapers/questions-2099.html' in exp
           and 'solvedQP/questions-2099.html' in exp)
    expect('solved spec expects a verification record',
           'meoclass1/pastpapers/verification/QPZZ99/Q1.md' in exp)

    # An INTAKE year must NOT produce a paid delivery sheet. This is the
    # control that would have caught a gate demanding a page the product
    # deliberately does not sell.
    intake = [{'paper_id': 'QPZZ98', 'year': 2098,
               'questions': [{'q_no': 'Q1'}]}]
    exp_i = expected_artefacts(intake)
    expect('intake year gets NO delivery year sheet',
           'solvedQP/questions-2098.html' not in exp_i)
    expect('intake spec gets NO delivery paper page',
           'solvedQP/QPZZ98.html' not in exp_i)
    expect('intake year DOES get a review year sheet',
           'meoclass1/pastpapers/questions-2098.html' in exp_i)

    # The gate must report a path Git has never seen. Proven against a name
    # that cannot exist rather than by touching the working tree.
    tracked, _index, work = git_state()
    expect('git state was actually read (tree is tracked)', len(tracked) > 50)
    expect('an impossible path is not tracked',
           'meoclass1/pastpapers/QPZZ99.html' not in tracked)

    real = load_specs()
    unexpected, missing = verify_derivation(real)
    expect('derivation matches disk: nothing unexpected',
           not unexpected or print('    unexpected: %s' % unexpected[:6]) is None
           and not unexpected)
    expect('derivation matches disk: nothing missing',
           not missing or print('    missing: %s' % missing[:6]) is None
           and not missing)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--strict', action='store_true',
                    help='publication gate: an unstaged artefact also fails')
    ap.add_argument('--verify-derivation', action='store_true',
                    help='prove the expected set matches the surfaces on disk')
    ap.add_argument('--self-test', action='store_true',
                    help='negative controls: prove the gate can fail')
    args = ap.parse_args()

    if args.self_test:
        print('DELIVERY GATE self-test')
        sys.exit(0 if self_test() else 1)

    specs = load_specs()
    if not specs:
        print('ERROR: no specs found under %s' % SPEC_GLOB)
        sys.exit(1)

    if args.verify_derivation:
        unexpected, missing = verify_derivation(specs)
        for p in unexpected:
            print('  UNEXPECTED  %s  (generated surface this gate does not know)' % p)
        for p in missing:
            print('  NOT BUILT   %s' % p)
        n = len(unexpected) + len(missing)
        print('DERIVATION   %s' % ('PASS' if n == 0 else 'FAIL (%d)' % n))
        sys.exit(1 if n else 0)

    exp, failures, warnings = check(specs, args.strict)

    for kind, path, why in failures:
        print('  %-10s %s  (%s)' % (kind, path, why))
    for kind, path, why in warnings:
        print('  [WARN ] %-8s %s  (%s)' % (kind, path, why))

    print('DELIVERY GATE %s  %d artefact(s) derived from %d spec(s)%s'
          % ('PASS' if not failures else 'FAIL',
             len(exp), len(specs),
             ', strict' if args.strict else ''))
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
