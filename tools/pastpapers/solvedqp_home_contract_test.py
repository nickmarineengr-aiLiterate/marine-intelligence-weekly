#!/usr/bin/env python3
"""Prove /solvedQP/index.html owns layout, and owns no product truth.

    specs/*.json --> manifest --> index.html

The home page is a PROJECTION. Every mutable fact on it -- the sitting count,
the question count, the newest sitting, the topic chips, the paper inventory,
the year inventory and the Latest Updates ledger -- must be reproducible from
the canonical specs, and must agree with the manifest the browser fetches for
search and for the full update history.

WHY THIS TEST EXISTS
--------------------
`build_solvedqp_home.py` already derives all of that, and re-running it on an
unchanged tree is byte-identical. But "is currently generated" and "cannot
become hand-maintained" are different guarantees, and only the second one
survives a future session. The failure this forecloses is small and entirely
plausible: someone edits a count, a chip or an update row directly into the
generated HTML to ship a fix quickly. The page then looks right and every
other check still passes, because no other check compares the page's numbers
with the specs. From that moment the product has two sources of truth and the
next build silently reverts the fix.

So each assertion below reads the SHIPPED BYTES and recomputes the same fact
from canonical data. A hand-edit fails the build.

A NOTE ON WHAT IS **NOT** ASSERTED
----------------------------------
This does not require the Latest Updates preview to be fetched client-side.
The preview is rendered server-side ON PURPOSE: it is readable with no
JavaScript, it cannot flash empty on a slow connection, and it survives a
manifest fetch failure, which matters on the landing page of a paid product.
What matters is not WHERE the rows are rendered but WHETHER they are derived,
and that is what is checked -- every rendered row must exist in the manifest,
with the same date, sitting and kind. Server-side rendering of derived data is
not duplication; a second hand-kept copy would be, and rule 6 below is what
tells the two apart.

--self-test mutates a copy of the real page in memory and asserts each guard
FAILS. A contract test that has never been seen to fail is a contract test
that proves nothing.
"""
import argparse, glob, io, json, os, re, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import REPO_ROOT
import build_solvedqp_home as HOME
from build_solvedqp_manifest import recently_updated

INDEX = os.path.join(REPO_ROOT, 'solvedQP', 'index.html')
MANIFEST = os.path.join(REPO_ROOT, 'solvedQP', 'solvedqp_content_index.json')


def unesc(s):
    """Undo the few HTML entities the builder emits in visible text."""
    return (s.replace('&amp;', '&').replace('&mdash;', '—')
             .replace('&middot;', '·').replace('&rsquo;', '’')
             .replace('&lt;', '<').replace('&gt;', '>'))


# ---- the six rules ---------------------------------------------------------

def rule_counts(html, specs, man, fail):
    """1. Hero counts and the newest sitting are derived, and agree with the
    manifest the browser will fetch. Two representations of one number are
    fine; two SOURCES for it are not."""
    sittings = HOME.solved_sittings(specs)
    n_sit = len(sittings)
    n_q = sum(len(d['questions']) for d in sittings)

    m = re.search(r'<div><b>(\d+)</b><span>solved sittings</span></div>', html)
    if not m or int(m.group(1)) != n_sit:
        fail('hero "solved sittings" is %s, specs say %d'
             % (m.group(1) if m else 'ABSENT', n_sit))
    m = re.search(r'<div><b>(\d+)</b><span>questions</span></div>', html)
    if not m or int(m.group(1)) != n_q:
        fail('hero "questions" is %s, specs say %d'
             % (m.group(1) if m else 'ABSENT', n_q))

    newest = HOME.newest_sitting(specs)
    m = re.search(r'<div><b>([^<]+)</b><span>newest solved sitting</span></div>', html)
    if not m or unesc(m.group(1)) != newest['month_year']:
        fail('hero "newest solved sitting" is %s, specs say %s'
             % (m.group(1) if m else 'ABSENT', newest['month_year']))

    # Manifest agreement. If these ever diverge the browser and the page are
    # telling a customer two different things about the same collection.
    if man['available_papers'] != n_sit:
        fail('manifest available_papers %d != specs %d'
             % (man['available_papers'], n_sit))
    if man['available_questions'] != n_q:
        fail('manifest available_questions %d != specs %d'
             % (man['available_questions'], n_q))

    # The hero stat block is the ONE place these two numbers are stated in
    # prose. The search hint used to restate them, which made it a third copy of
    # the same fact for a reader who had just read it two sections above; the
    # redesign removed that duplication. The rule follows: it now pins the hero,
    # so the numbers are still derived and still checked, just not repeated.
    m = re.search(r'<div><b>(\d+)</b><span>solved sittings</span></div>\s*'
                  r'<div><b>(\d+)</b><span>questions</span></div>', html)
    if not m or (int(m.group(1)), int(m.group(2))) != (n_sit, n_q):
        fail('hero stats say %s, specs say (%d sittings, %d questions)'
             % (m.groups() if m else 'ABSENT', n_sit, n_q))


def rule_topics(html, specs, fail):
    """2. Every topic chip is derived, and no chip names a topic with no
    solved questions behind it -- the one thing a discovery control must never
    do."""
    want = dict(HOME.topic_counts(HOME.solved_sittings(specs)))
    got = {}
    for label, count in re.findall(
            r'<button type="button" class="sq-chip" data-domain="([^"]+)" '
            r'aria-pressed="false">[^<]*<span class="sq-kbd">(\d+)</span></button>', html):
        got[unesc(label)] = int(count)
    if not got:
        fail('no topic chips found on the page at all')
        return
    for label, n in sorted(got.items()):
        if label not in want:
            fail('chip "%s" names a topic with NO solved questions' % label)
        elif want[label] != n:
            fail('chip "%s" says %d, specs say %d' % (label, n, want[label]))
    for label in sorted(set(want) - set(got)):
        fail('topic "%s" has %d solved questions but no chip' % (label, want[label]))


def rule_inventory(html, specs, fail):
    """3. The solved inventory reachable from the home page is exactly the set of
    solved sittings -- no invented link, no omitted one.

    UPDATED for the redesigned hierarchy. The old rule matched a flat "Solved
    papers" card grid, which has been removed because it listed every sitting a
    second time with no year structure. Coverage by Year is now the primary and
    only route in, so the rule follows the route: it counts the per-month links
    that grid emits. The GUARANTEE is unchanged -- every solved paper must be
    reachable from a server-rendered link, and nothing unsolved may be.
    """
    want = {d['paper_id'] for d in HOME.solved_sittings(specs)}
    got = set(re.findall(r'<a class="cov-m cov-av" href="/solvedQP/([A-Za-z0-9-]+)\.html"', html))
    for pid in sorted(got - want):
        fail('coverage links %s, which is not a solved spec' % pid)
    for pid in sorted(want - got):
        fail('solved spec %s is not reachable from Coverage by year' % pid)


def rule_years(html, specs, fail):
    """4. The year inventory follows the solved set. Adding the first paper of
    a new year must add its sheet with no edit to the page."""
    want = {d['year'] for d in HOME.solved_sittings(specs)}
    got = {int(y) for y in re.findall(r'/solvedQP/questions-(\d{4})\.html', html)}
    for y in sorted(got - want):
        fail('year sheet %d is linked but has no solved paper' % y)
    for y in sorted(want - got):
        fail('year %d has solved papers but no sheet link' % y)


def rule_updates(html, specs, man, fail):
    """5. Every rendered update row exists in the manifest, and the rows are
    exactly what the selection policy picks. This is the rule that makes the
    server-side preview a projection rather than a second ledger."""
    sittings = {d['paper_id'] for d in HOME.solved_sittings(specs)}
    all_ups = recently_updated(specs, sittings)
    picked = HOME.preview_updates(all_ups)

    rows = re.findall(
        r'<li><time datetime="([^"]+)">[^<]*</time><div class="what">'
        r'<b><span class="sq-kind sq-k-([a-z_]+)">[^<]*</span>'
        r'<a href="/solvedQP/([^."]+)\.html">([^<]*)</a></b>', html)
    if not rows:
        fail('no update rows rendered on the page')
        return

    # Manifest membership. A row that names a (date, paper, kind) the manifest
    # does not carry is a hand-authored row by definition.
    known = {(u['date'], u['paper_id'], u['kind']) for u in man['recently_updated']}
    for date, kind, pid, _sitting in rows:
        if (date, pid, kind) not in known:
            fail('update row %s/%s/%s is NOT in the manifest ledger' % (date, pid, kind))

    # Policy agreement: the rendered rows must be precisely the policy's output.
    want = [(u['date'], u['kind'], u['paper_id']) for u in picked]
    got = [(d, k, p) for d, k, p, _s in rows]
    if want != got:
        fail('rendered preview %s != preview_updates() %s' % (got, want))

    # The full ledger must not be duplicated into the page. The panel is an
    # empty div the browser fills from the manifest.
    # Negative lookahead for the CLOSING tag, not merely for non-whitespace:
    # `>\s*\S` also matches the `<` of `</div>`, so it reported an empty div as
    # populated and would have failed the shipped page forever.
    if re.search(r'<div id="sq-upd-all"[^>]*>(?!\s*</div>)', html):
        fail('the full update ledger is materialised into the page')
    if len(man['recently_updated']) > len(picked) \
            and 'id="sq-upd-btn"' not in html:
        fail('ledger is longer than the preview but has no "view all" control')


def rule_resilience(html, man, fail):
    """6. A manifest fetch failure must degrade, not blank.

    The whole inventory is server-rendered, so the page is useful with the
    fetch dead; and the two client-side surfaces say so instead of showing an
    empty box. Equally important, the inventory must NOT be duplicated into a
    JS fallback -- that would be the second source of truth this whole test
    exists to prevent."""
    for needle, what in (
            ('Search is temporarily unavailable', 'search failure message'),
            ('Could not load the update history', 'update-history failure message')):
        if needle not in html:
            fail('missing graceful %s' % what)

    # Server-rendered inventory: the cards are in the bytes, not injected.
    n_links = html.count('class="cov-m cov-av"')
    if n_links < man['available_papers']:
        fail('paper inventory is not fully server-rendered (%d coverage links, %d papers)'
             % (n_links, man['available_papers']))

    # No inline copy of the manifest. A fallback array of papers or updates
    # embedded in the script would recreate the duplication.
    for pat, what in ((r'recently_updated\s*=\s*\[', 'inline updates array'),
                      (r'var\s+PAPERS\s*=\s*\[', 'inline papers array'),
                      (r'<script[^>]*type="application/json"', 'inline JSON payload')):
        if re.search(pat, html):
            fail('page carries an %s -- second source of truth' % what)


RULES = ('counts', 'topics', 'inventory', 'years', 'updates', 'resilience')


def run(html, specs, man, report):
    fails = []

    def fail(msg):
        fails.append(msg)
    rule_counts(html, specs, man, fail)
    rule_topics(html, specs, fail)
    rule_inventory(html, specs, fail)
    rule_years(html, specs, fail)
    rule_updates(html, specs, man, fail)
    rule_resilience(html, man, fail)
    if report:
        for f in fails:
            print('  %s' % f)
    return fails


def load():
    specs = []
    for p in sorted(glob.glob(os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers',
                                           'specs', '*.json'))):
        with open(p, encoding='utf-8') as fh:
            specs.append(json.load(fh))
    html = open(INDEX, encoding='utf-8').read()
    man = json.load(open(MANIFEST, encoding='utf-8'))
    return html, specs, man


def self_test():
    """Each mutation is a realistic hand-edit. All six rules must bite."""
    html, specs, man = load()
    ok = True

    def probe(name, mutated):
        nonlocal ok
        got = run(mutated, specs, man, report=False)
        print('  %-52s %s' % (name, 'PASS' if got else 'FAIL (not detected)'))
        if not got:
            ok = False

    n_sit = len(HOME.solved_sittings(specs))
    probe('hand-edited sitting count is caught',
          html.replace('<div><b>%d</b><span>solved sittings</span></div>' % n_sit,
                       '<div><b>%d</b><span>solved sittings</span></div>' % (n_sit + 1)))
    probe('hand-added topic chip is caught',
          html.replace('<div class="sq-chips" role="group" aria-label="Browse by topic">',
                       '<div class="sq-chips" role="group" aria-label="Browse by topic">\n'
                       '    <button type="button" class="sq-chip" data-domain="Ballast Water" '
                       'aria-pressed="false">Ballast Water <span class="sq-kbd">7</span></button>'))
    probe('deleted coverage link is caught',
          re.sub(r'<a class="cov-m cov-av" href="/solvedQP/QP2301\.html"', '<a class="x"',
                 html, count=1))
    probe('invented year-sheet link is caught',
          html.replace('/solvedQP/questions-2023.html',
                       '/solvedQP/questions-2019.html', 1))
    probe('hand-authored update row is caught',
          html.replace('<ul class="sq-upd">',
                       '<ul class="sq-upd">\n    <li><time datetime="2026-01-01">1 Jan 2026'
                       '</time><div class="what"><b><span class="sq-kind sq-k-corrected">'
                       'Corrected</span><a href="/solvedQP/QP2301.html">January 2023</a>'
                       '</b><span>hand written</span></div></li>', 1))
    probe('removed graceful-failure message is caught',
          html.replace('Could not load the update history', 'X'))
    probe('inlined manifest payload is caught',
          html.replace('<div id="sq-upd-all" hidden></div>',
                       '<div id="sq-upd-all" hidden>{"recently_updated": []}</div>'))

    # Positive control: the real page must PASS, or every result above is
    # meaningless because the rules would fire on anything.
    real = run(html, specs, man, report=True)
    print('  %-52s %s' % ('the SHIPPED page passes all six rules',
                          'PASS' if not real else 'FAIL'))
    if real:
        ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()

    if args.self_test:
        print('SOLVEDQP HOME CONTRACT self-test')
        sys.exit(0 if self_test() else 1)

    html, specs, man = load()
    fails = run(html, specs, man, report=True)
    print('HOME CONTRACT %s  %d rule(s) over %d spec(s)'
          % ('PASS' if not fails else 'FAIL (%d)' % len(fails), len(RULES), len(specs)))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
