#!/usr/bin/env python3
"""Which surfaces did this change actually touch? DETECTION AND CLASSIFICATION ONLY.

Usage:
  python tools/pastpapers/surface_impact.py --base <ref> [--head <ref>]
                                            [--target QP2509] [--json] [-v]
  python tools/pastpapers/surface_impact.py --self-test

Part of the Production Intelligence Layer (PIL). PIL FLAGS; CLAUDE ADJUDICATES.

WHY THIS EXISTS
    Solving QP2509 legitimately changed the recurrence summary on the PUBLIC,
    FREE January 2026 sample and on QP2601.html -- neither of which was the
    target of that session. Every guard passed, correctly, and nothing surfaced
    that a free and a paid page had moved. Regeneration is allowed to do this;
    it is not allowed to do it invisibly.

TWO INDEPENDENT AXES
    SURFACE  -- who can see this artefact, derived from repository architecture:
                INTERNAL, CANDIDATE_FACING_PAID, PUBLIC_FREE, COMMERCIAL,
                SECURITY_SENSITIVE, UNKNOWN_REVIEW.

    RELATION -- how this artefact relates to the declared target of the session:
                TARGET_DIRECT, DERIVED_NON_TARGET, UNRELATED_OR_UNKNOWN.

    These are kept separate on purpose. An earlier design proposed labelling
    changes EXPECTED or UNEXPECTED. That was dropped: a path can tell you a file
    is the target paper's page, but no path can tell you whether a public
    sample's change is semantically the one you meant. Claiming "expected" from
    a path is exactly the semantic overreach PIL must not commit. RELATION
    states the mechanical fact and stops there.

WHAT GETS ESCALATED
    Any PUBLIC_FREE, COMMERCIAL or SECURITY_SENSITIVE artefact whose relation is
    NOT TARGET_DIRECT, plus everything classified UNKNOWN_REVIEW, is reported as
    FOUNDER REVIEW REQUIRED. That is a request for a human decision, not a
    verdict that the change is wrong.

Exit code is 0 whenever the comparison runs, including when review is required
-- this is a finalisation report, not a build gate. --self-test exits non-zero
if a positive control fails.
"""
import argparse, io, json, os, re, subprocess, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

INTERNAL = 'INTERNAL'
PAID = 'CANDIDATE_FACING_PAID'
FREE = 'PUBLIC_FREE'
COMMERCIAL = 'COMMERCIAL'
SECURITY = 'SECURITY_SENSITIVE'
UNKNOWN = 'UNKNOWN_REVIEW'

ESCALATING = (FREE, COMMERCIAL, SECURITY)

TARGET_DIRECT = 'TARGET_DIRECT'
DERIVED = 'DERIVED_NON_TARGET'
UNRELATED = 'UNRELATED_OR_UNKNOWN'

# Ordered, first match wins. Each rule is (regex, surface, why). The "why" is
# printed in --verbose so a classification can be argued with rather than
# trusted. Anything reaching the end is UNKNOWN_REVIEW, deliberately.
RULES = [
    # --- security and money first: these must never be shadowed by a broader
    #     rule that happens to match the same path.
    (r'^api/(check-password|migrate-users|check-db)\.js$', SECURITY,
     'authentication / user-store endpoint'),
    (r'^api/', SECURITY,
     'server endpoint: payment or auth surface'),
    (r'^robots\.txt$', SECURITY,
     'indexing policy -- controls whether paid content is crawlable'),
    (r'^(vercel|middleware)\.(json|js)$', SECURITY,
     'hosting / request-path configuration'),

    # --- the storefront. The free sample lives inside SQ/ and must be matched
    #     BEFORE the storefront rule, or it would be reported as commercial.
    (r'^SQ/solved-qp-sample-.*\.html$', FREE,
     'free conversion sample -- public, ungated'),
    (r'^SQ/index\.html$', COMMERCIAL,
     'storefront: price and CTA surface'),
    (r'^SQ/', COMMERCIAL,
     'storefront surface'),

    # --- the paid product.
    (r'^meoclass1/pastpapers/QP\d{4}\.html$', PAID,
     'solved paper page -- the paid product'),

    # --- public pages generated from the same specs.
    (r'^meoclass1/pastpapers/(index|questions-\d{4}|topics-\d{4})\.html$', FREE,
     'public index / questions-only year sheet / topic page'),
    (r'^meoclass1/pastpapers/pastpapers_content_index\.json$', FREE,
     'shipped search payload -- reaches the browser'),

    # --- internal production material. Specs and verification records are the
    #     source of the product but are never served.
    (r'^meoclass1/pastpapers/(specs|verification|staging|sample)/', INTERNAL,
     'production input, not served'),
    (r'^meoclass1/pastpapers/docs/', INTERNAL,
     'governed protocol / intelligence document'),
    (r'^meoclass1/pastpapers/known_traps\.md$', INTERNAL,
     'trap registry'),
    (r'^tools/', INTERNAL,
     'build and check tooling'),
    (r'^(docs|reports|engineering-reports|corrections)/', INTERNAL,
     'internal documentation'),
    (r'^\.claude/', INTERNAL,
     'agent configuration'),
]

GENERATED = re.compile(
    r'^(meoclass1/pastpapers/(QP\d{4}|index|questions-\d{4}|topics-\d{4})\.html'
    r'|meoclass1/pastpapers/pastpapers_content_index\.json'
    r'|SQ/solved-qp-sample-.*\.html)$')


def classify(path):
    """(surface, why) for one repo-relative path. Never guesses: falls to UNKNOWN."""
    p = path.replace('\\', '/')
    for rx, surface, why in RULES:
        if re.search(rx, p):
            return surface, why
    return UNKNOWN, 'no classification rule matched -- classify it or review it'


def relate(path, target):
    """(relation, why) of one path to the declared target paper id."""
    p = path.replace('\\', '/')
    if target and target.upper() in p.upper():
        return TARGET_DIRECT, 'path names the declared target %s' % target
    if GENERATED.search(p):
        if not target:
            return UNRELATED, 'generated artefact, but no target was declared'
        return DERIVED, 'generated artefact regenerated without naming %s' % target
    return UNRELATED, 'not a generated artefact and does not name the target'


def changed_paths(base, head, cwd=REPO_ROOT):
    """[(status, path)] from git. Fails loudly rather than assuming a range."""
    r = subprocess.run(['git', 'diff', '--name-status', '%s..%s' % (base, head)],
                       cwd=cwd, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    if r.returncode != 0:
        sys.stderr.write('git diff %s..%s failed:\n%s\n' % (base, head, r.stderr))
        sys.exit(2)
    out = []
    for line in r.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split('\t')
        out.append((parts[0], parts[-1]))
    return out


def infer_target(paths):
    """Target paper id, only where exactly one spec changed. Printed, never silent."""
    ids = {m.group(1) for _s, p in paths
           for m in [re.search(r'specs/(QP\d{4})\.json$', p.replace('\\', '/'))] if m}
    return ids.pop() if len(ids) == 1 else None


def analyse(paths, target):
    rows = []
    for status, path in paths:
        surface, swhy = classify(path)
        relation, rwhy = relate(path, target)
        review = (surface in ESCALATING and relation != TARGET_DIRECT) or surface == UNKNOWN
        rows.append({'status': status, 'path': path, 'surface': surface,
                     'relation': relation, 'review_required': review,
                     'surface_why': swhy, 'relation_why': rwhy})
    return rows


# ------------------------------------------------------------------ self-test

# (path, expected surface, expected relation given target QP2509)
FIXTURES = [
    ('meoclass1/pastpapers/QP2509.html', PAID, TARGET_DIRECT),
    ('meoclass1/pastpapers/QP2601.html', PAID, DERIVED),
    ('meoclass1/pastpapers/specs/QP2509.json', INTERNAL, TARGET_DIRECT),
    ('meoclass1/pastpapers/verification/QP2509/Q1.md', INTERNAL, TARGET_DIRECT),
    ('meoclass1/pastpapers/docs/CURRENT_STATUS.md', INTERNAL, UNRELATED),
    ('tools/pastpapers/build_paper.py', INTERNAL, UNRELATED),
    ('SQ/solved-qp-sample-january-2026.html', FREE, DERIVED),
    ('meoclass1/pastpapers/questions-2025.html', FREE, DERIVED),
    ('meoclass1/pastpapers/index.html', FREE, DERIVED),
    ('meoclass1/pastpapers/pastpapers_content_index.json', FREE, DERIVED),
    ('SQ/index.html', COMMERCIAL, UNRELATED),
    ('api/create-order.js', SECURITY, UNRELATED),
    ('api/check-password.js', SECURITY, UNRELATED),
    ('robots.txt', SECURITY, UNRELATED),
    ('some/unmapped/thing.html', UNKNOWN, UNRELATED),
]


def self_test():
    checks = []

    def expect(name, ok, detail=''):
        checks.append((name, ok, detail))

    for path, want_surface, want_relation in FIXTURES:
        got_s, _ = classify(path)
        got_r, _ = relate(path, 'QP2509')
        expect('classify %-52s -> %s' % (path, want_surface),
               got_s == want_surface, 'got %s' % got_s)
        expect('relate   %-52s -> %s' % (path, want_relation),
               got_r == want_relation, 'got %s' % got_r)

    # Escalation policy, both directions.
    rows = analyse([('M', 'SQ/solved-qp-sample-january-2026.html')], 'QP2509')
    expect('free sample changed on a QP2509 session -> FOUNDER REVIEW REQUIRED',
           rows[0]['review_required'], repr(rows[0]))
    rows = analyse([('A', 'meoclass1/pastpapers/QP2509.html')], 'QP2509')
    expect('the target paid page itself -> no review escalation',
           not rows[0]['review_required'], repr(rows[0]))
    rows = analyse([('M', 'tools/pastpapers/build_paper.py')], 'QP2509')
    expect('internal tooling -> no review escalation',
           not rows[0]['review_required'], repr(rows[0]))
    rows = analyse([('M', 'some/unmapped/thing.html')], 'QP2509')
    expect('unclassified path -> review escalation (UNKNOWN is never hidden)',
           rows[0]['review_required'], repr(rows[0]))

    # Ordering: the free sample lives under SQ/, which is otherwise commercial.
    # If the specific rule ever moves below the storefront rule, the free page
    # silently becomes COMMERCIAL and stops being reported as a free-surface
    # change. Prove the ordering, not just the current answer.
    expect('rule ordering: free sample beats the SQ/ storefront rule',
           classify('SQ/solved-qp-sample-january-2026.html')[0] == FREE
           and classify('SQ/anything-else.html')[0] == COMMERCIAL)

    # MUTATION -- the classifier must be able to fail. Drop the paid-page rule
    # and assert a fixture that depends on it stops matching.
    saved = list(RULES)
    try:
        RULES[:] = [r for r in RULES if 'QP' not in r[0]]
        expect('MUTATION: paid-page rule removed -> QP2509.html misclassifies',
               classify('meoclass1/pastpapers/QP2509.html')[0] != PAID,
               'still %s' % classify('meoclass1/pastpapers/QP2509.html')[0])
    finally:
        RULES[:] = saved
    expect('MUTATION reverted -> paid page classifies again',
           classify('meoclass1/pastpapers/QP2509.html')[0] == PAID)

    # MUTATION -- escalation policy itself.
    saved_esc = tuple(ESCALATING)
    try:
        globals()['ESCALATING'] = ()
        rows = analyse([('M', 'SQ/solved-qp-sample-january-2026.html')], 'QP2509')
        expect('MUTATION: escalation disabled -> free sample stops escalating',
               not rows[0]['review_required'], repr(rows[0]))
    finally:
        globals()['ESCALATING'] = saved_esc
    rows = analyse([('M', 'SQ/solved-qp-sample-january-2026.html')], 'QP2509')
    expect('MUTATION reverted -> free sample escalates again',
           rows[0]['review_required'], repr(rows[0]))

    width = max(len(n) for n, _, _ in checks)
    failed = 0
    for name, ok, detail in checks:
        if not ok:
            failed += 1
        print('  %-*s  %s%s' % (width, name, 'PASS' if ok else 'FAIL',
                                '   ' + detail if not ok else ''))
    print('  %d control(s), %d failed' % (len(checks), failed))
    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--base', help='base git ref (required unless --self-test)')
    ap.add_argument('--head', default='HEAD')
    ap.add_argument('--target', help='paper id this session was meant to change')
    ap.add_argument('--self-test', action='store_true')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('-v', '--verbose', action='store_true')
    args = ap.parse_args()

    if args.self_test:
        print('surface_impact self-test')
        sys.exit(self_test())

    # No base ref, no report. Inventing one -- "probably the previous commit" --
    # is the invisible Git-state assumption this tool must not make.
    if not args.base:
        ap.error('--base is required: surface impact is a comparison, and there '
                 'is no safe default ref to compare against')

    paths = changed_paths(args.base, args.head)
    target = args.target or infer_target(paths)
    rows = analyse(paths, target)

    if args.json:
        json.dump({'base': args.base, 'head': args.head, 'target': target,
                   'rows': rows}, sys.stdout, indent=2)
        sys.stdout.write('\n')
        sys.exit(0)

    print('surface impact  %s..%s' % (args.base, args.head))
    if args.target:
        print('target: %s (declared)' % target)
    elif target:
        print('target: %s (INFERRED -- exactly one spec changed)' % target)
    else:
        print('target: NONE DECLARED and none inferable -- every generated '
              'artefact is reported as UNRELATED_OR_UNKNOWN')
    print('%d changed path(s)' % len(rows))
    print('-' * 78)
    for r in sorted(rows, key=lambda r: (not r['review_required'], r['surface'],
                                         r['path'])):
        print('  %s %-21s %-19s %s' % (r['status'], r['surface'], r['relation'],
                                       r['path']))
        if args.verbose:
            print('        surface: %s' % r['surface_why'])
            print('        relation: %s' % r['relation_why'])

    review = [r for r in rows if r['review_required']]
    print('-' * 78)
    if review:
        print('FOUNDER REVIEW REQUIRED -- %d change(s) to a public, commercial, '
              'security-sensitive' % len(review))
        print('or unclassified surface that is NOT the declared target:')
        for r in review:
            print('    %-21s %-19s %s' % (r['surface'], r['relation'], r['path']))
        print('')
        print('This is not a defect finding. Regeneration is permitted to move '
              'these surfaces;')
        print('what is not permitted is moving them without saying so.')
    else:
        print('No public, commercial or security-sensitive non-target change.')

    # Reported separately rather than folded into the escalation set. A paid
    # page that moves without being the target is worth seeing -- QP2601.html
    # did exactly that during QP2509 -- but the escalation set is a governed
    # decision, so widening it is the Founder's call, not this tool's.
    paid = [r for r in rows if r['surface'] == PAID and r['relation'] != TARGET_DIRECT]
    if paid:
        print('')
        print('NOTE -- %d paid page(s) regenerated without being the target:' % len(paid))
        for r in paid:
            print('    %-19s %s' % (r['relation'], r['path']))
    sys.exit(0)


if __name__ == '__main__':
    main()
