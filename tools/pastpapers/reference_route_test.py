#!/usr/bin/env python3
"""Prove the reference shelf never links to a route that does not exist.

    specs/*.json --> build_paper.reference_shelf() --> shipped HTML

WHY THIS TEST EXISTS
--------------------
`REFERENCE_ROUTE_BASE` was '/reference' -- a placeholder written while no
question anywhere carried a REFERENCE_AVAILABLE object, so the constant
rendered nothing and was safe. It stopped being safe the day QP2307 became the
first paper to map its claims onto corpus objects, and nothing announced that
day. Nineteen "Verify source" buttons per copy shipped to candidates, each one
a 404, in both the delivered paper and the review copy.

The defect was not the placeholder. It was that a placeholder could become
live without a single check noticing. So this test asserts the invariant the
constant only implied:

    A reference control is emitted ONLY IF the route it points at is governed.

and it asserts it against the SHIPPED BYTES, not against the builder's
intentions, because the builder is what changed and the bytes are what a
candidate clicks.

THE FOUR RULES
--------------
1. No shipped page emits an href under an ungoverned reference base.
2. The builder fails closed: with no route configured, reference_href()
   returns None and the shelf emits no control -- proved by rendering, not by
   reading the constant.
3. A shelf entry that is NOT available still renders its state in a review
   build. Suppressing the dead link must not have suppressed the pending
   signal production relies on.
4. The evidence itself survives. Every REFERENCE_AVAILABLE object in a spec
   still has its label, relationship and scope on the delivered page. Removing
   a dead button must not quietly remove the citation it sat under.

TURNING THE LINKS ON
--------------------
When the resolver and viewer land, set REFERENCE_ROUTE_BASE to its base path
and add that base to GOVERNED_ROUTES below, in the same commit. Rule 1 then
requires the route to resolve; it does not merely permit the href.

--self-test mutates a copy of the real page in memory and asserts each guard
FAILS. A contract test that has never been seen to fail proves nothing.
"""
import argparse, glob, io, json, os, re, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import REPO_ROOT, esc
import build_paper as BP

SPECS = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers', 'specs', '*.json')

# Reference bases that a page is allowed to link to, each mapped to the
# repository path that must exist for the route to resolve. EMPTY on purpose:
# no public reference viewer has been built. This is the allow-list, so an
# unlisted base is a dead route by definition and needs no separate blocklist.
GOVERNED_ROUTES = {}

# Any href whose path segment looks like a reference viewer. Deliberately wider
# than the one base that shipped: the failure was a placeholder nobody was
# watching, so the guard watches the shape, not the string.
REF_HREF = re.compile(r'href="((/(?:reference|references|source|sources|corpus)'
                      r'(?:/[^"]*)?))"')


def shipped_pages():
    """Every generated HTML page in the repository.

    Not just the deployed ones. A dead control in the review tree is a defect
    production sees too, and the review tree is where the delivered pages are
    proofread -- a reviewer who clicks a dead button there learns the wrong
    thing about the product either way.
    """
    out = []
    for sub in ('solvedQP', 'meoclass1', 'SQ'):
        out.extend(sorted(glob.glob(os.path.join(REPO_ROOT, sub, '**', '*.html'),
                                    recursive=True)))
    return out


def load_specs():
    return [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(SPECS))]


def shelf_entries(spec, state=None):
    for q in spec.get('questions') or []:
        for r in q.get('reference_shelf') or []:
            if state is None or r.get('state') == state:
                yield q, r


# ---- the four rules --------------------------------------------------------

def rule_no_ungoverned_href(fail, pages=None):
    """1. No shipped page links into a reference base that is not governed."""
    for path in (pages if pages is not None else shipped_pages()):
        try:
            rel = os.path.relpath(path, REPO_ROOT).replace('\\', '/')
        except ValueError:
            # --self-test writes its mutated copy to the system temp directory,
            # which on Windows is routinely on another drive. Not an error.
            rel = path.replace('\\', '/')
        html = open(path, encoding='utf-8').read()
        for whole, base_path in REF_HREF.findall(html):
            base = '/' + base_path.strip('/').split('/')[0]
            target = GOVERNED_ROUTES.get(base)
            if target is None:
                fail('%s links to %s, but %s is not a governed reference route'
                     % (rel, whole, base))
            elif not os.path.exists(os.path.join(REPO_ROOT, target)):
                fail('%s links to %s and %s is governed, but %s does not exist'
                     % (rel, whole, base, target))


def rule_builder_fails_closed(fail):
    """2. With no governed route, the builder emits no control -- proved by
    rendering a real available entry, not by reading the constant."""
    if BP.REFERENCE_ROUTE_BASE and BP.REFERENCE_ROUTE_BASE not in GOVERNED_ROUTES:
        fail('REFERENCE_ROUTE_BASE is %r but that base is not in GOVERNED_ROUTES'
             % BP.REFERENCE_ROUTE_BASE)

    spec = _spec_with(state='REFERENCE_AVAILABLE')
    if spec is None:
        return                      # nothing maps a corpus object yet; rule moot
    q, _ = next(shelf_entries(spec, 'REFERENCE_AVAILABLE'))
    out = []
    BP.reference_shelf(q, out, True)
    html = '\n'.join(out)
    if not html:
        fail('an available reference rendered no shelf at all')
        return
    if 'rs-open' in html or REF_HREF.search(html):
        fail('an available reference still emitted a control with no governed route')
    if BP.reference_href('SOLAS-II2-10') is not None and not GOVERNED_ROUTES:
        fail('reference_href() returned a route while GOVERNED_ROUTES is empty')


def rule_pending_still_renders(fail):
    """3. A non-available entry still shows its state in a review build."""
    spec = _spec_with(state=None, non_available=True)
    if spec is None:
        return
    for q, r in shelf_entries(spec):
        if r.get('state') == 'REFERENCE_AVAILABLE':
            continue
        out = []
        BP.reference_shelf(q, out, False)       # review build
        html = '\n'.join(out)
        if 'rs-pending' not in html:
            fail('a %s entry rendered no pending styling in a review build'
                 % r.get('state'))
        if 'rs-state' not in html:
            fail('a %s entry rendered no state line in a review build'
                 % r.get('state'))
        return


def rule_evidence_survives(fail):
    """4. Removing the dead control did not remove the citation under it."""
    for spec in load_specs():
        pid = spec['paper_id']
        page = os.path.join(REPO_ROOT, 'solvedQP', '%s.html' % pid)
        avail = list(shelf_entries(spec, 'REFERENCE_AVAILABLE'))
        if not avail or not os.path.exists(page):
            continue
        html = open(page, encoding='utf-8').read()
        for _, r in avail:
            if esc(r['label']) not in html:
                fail('%s: reference label %r is no longer on the delivered page'
                     % (pid, r['label']))
            if r.get('claim_scope') and esc(r['claim_scope']) not in html:
                fail('%s: claim scope for %r is no longer on the delivered page'
                     % (pid, r['label']))
        if html.count('class="rs-item') != len(avail):
            fail('%s: page renders %d shelf items, spec has %d available objects'
                 % (pid, html.count('class="rs-item'), len(avail)))


RULES = [rule_no_ungoverned_href, rule_builder_fails_closed,
         rule_pending_still_renders, rule_evidence_survives]


def _spec_with(state, non_available=False):
    for spec in load_specs():
        for _, r in shelf_entries(spec):
            if non_available:
                if r.get('state') != 'REFERENCE_AVAILABLE':
                    return spec
            elif r.get('state') == state:
                return spec
    return None


def run(report=True, pages=None):
    fails = []

    def fail(msg):
        fails.append(msg)
        if report:
            print('  FAIL  %s' % msg)

    rule_no_ungoverned_href(fail, pages)
    for r in RULES[1:]:
        r(fail)
    return fails


# ---- self-test -------------------------------------------------------------

def self_test():
    import tempfile
    ok = True
    real = os.path.join(REPO_ROOT, 'solvedQP', 'QP2307.html')
    html = open(real, encoding='utf-8').read()

    def probe(name, mutated):
        nonlocal ok
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'QP2307.html')
            open(p, 'w', encoding='utf-8').write(mutated)
            got = bool(run(report=False, pages=[p]))
        print('  %-56s %s' % (name, 'PASS' if got else 'FAIL (not detected)'))
        if not got:
            ok = False

    # The exact defect this session removed, reintroduced.
    probe('a reinstated /reference/ button is caught',
          html.replace('<div class="rs-label">',
                       '<a class="nav-btn rs-open" href="/reference/SOLAS-II2-10">'
                       'Verify source</a><div class="rs-label">', 1))
    # The same defect wearing a different base.
    probe('a dead /source/ route is caught',
          html.replace('<div class="rs-label">',
                       '<a href="/source/X-1">Verify</a><div class="rs-label">', 1))
    probe('a dead /corpus/ route is caught',
          html.replace('<div class="rs-label">',
                       '<a href="/corpus/X-1">Verify</a><div class="rs-label">', 1))

    # Positive control: the shipped tree must pass, or every result above is
    # meaningless because the rules would fire on anything.
    real_fails = run(report=True)
    print('  %-56s %s' % ('the SHIPPED tree passes all four rules',
                          'PASS' if not real_fails else 'FAIL'))
    if real_fails:
        ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()

    if args.self_test:
        print('REFERENCE ROUTE self-test')
        sys.exit(0 if self_test() else 1)

    fails = run(report=True)
    print('REFERENCE ROUTE %s  %d rule(s) over %d page(s), %d governed route(s)'
          % ('PASS' if not fails else 'FAIL (%d)' % len(fails),
             len(RULES), len(shipped_pages()), len(GOVERNED_ROUTES)))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
