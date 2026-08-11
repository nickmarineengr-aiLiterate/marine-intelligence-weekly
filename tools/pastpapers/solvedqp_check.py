#!/usr/bin/env python3
"""Guard the paid Solved QP delivery surface at /solvedQP/.

Checks the SHIPPED BYTES, not the intent:

  completeness   every spec has a delivery page; index and year sheet exist
  indexing       paid pages are noindex and carry no JSON-LD
  review leakage no Founder-review banner or production metadata block
  third party    no source-copy recurrence annotation reaches a candidate,
                 in visible text OR in the invisible search payload
  authoring      no recurrence_class verdict reaches a candidate
  navigation     no link out of /solvedQP/ into the Oral product, which a
                 Written-only customer cannot open
  substance      the answers a customer paid for are actually present

--self-test proves each guard can FAIL by running it against a synthetic
page carrying every defect. A check that cannot fail is not a check.

Exit non-zero on any failure.
"""
import argparse, glob, io, json, os, re, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import REPO_ROOT

SQP = os.path.join(REPO_ROOT, 'solvedQP')
SPEC_GLOB = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers', 'specs', '*.json')

# Third-party source-copy recurrence annotations. These name sittings MIW has
# never read; the specs' own recurrence_note says so. Discovery evidence only.
THIRD_PARTY = [
    (re.compile(r'\b(19|20)\d{2}/(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|SR)', re.I),
     'source-copy recurrence annotation'),
    (re.compile(r'Recurrence recorded on the source paper', re.I),
     'source-copy recurrence sentence'),
    (re.compile(r'\d+\s+prior sitting', re.I),
     'source-copy prior-sitting count'),
]

# Authoring verdicts that must never face a candidate.
AUTHORING = [
    (re.compile(r'\b(Exact repeat|Near repeat|Topic recurs)\b'), 'recurrence_class label'),
    (re.compile(r'\b(exact_recurrence|near_recurrence|topic_recurrence)\b'), 'recurrence_class value'),
    (re.compile(r'Founder review copy'), 'review banner'),
    (re.compile(r'Production metadata \(review build only\)'), 'production metadata block'),
]

FAILS = []
CHECKS = [0]


def fail(where, msg):
    FAILS.append('%s: %s' % (where, msg))


def check_page(path, text, is_paper):
    name = os.path.basename(path)
    CHECKS[0] += 1

    if 'noindex' not in text:
        fail(name, 'paid page is not noindex')
    if 'application/ld+json' in text:
        fail(name, 'paid page carries JSON-LD structured data')
    if '/solvedQP/' not in text:
        fail(name, 'no canonical/self reference to /solvedQP/')

    for rx, label in THIRD_PARTY:
        m = rx.search(text)
        if m:
            fail(name, 'THIRD-PARTY LEAK (%s): %r' % (label, m.group(0)[:40]))
    for rx, label in AUTHORING:
        m = rx.search(text)
        if m:
            fail(name, 'authoring field leaked (%s): %r' % (label, m.group(0)[:40]))

    # A Written-only customer must never be sent into the Oral product.
    for href in re.findall(r'href="(/meoclass1/[^"]*)"', text):
        fail(name, 'links into the Oral product: %s' % href)

    if is_paper and 'Model written answer' not in text:
        fail(name, 'no model answer present — customer paid for answers')


def run():
    spec_paths = sorted(glob.glob(SPEC_GLOB))
    if not spec_paths:
        fail('specs', 'no specs found')
        return
    specs = []
    for sp in spec_paths:
        with open(sp, encoding='utf-8') as fh:
            specs.append(json.load(fh))

    check_storefront(specs)
    check_oral_promo(specs)
    check_year_nav(specs)

    expected = []
    total_q = 0
    years = set()
    for d in specs:
        if not any(q.get('model_answer') for q in d['questions']):
            continue
        expected.append('%s.html' % d['paper_id'])
        total_q += len(d['questions'])
        years.add(d['year'])

    for y in sorted(years):
        expected.append('questions-%d.html' % y)
    expected.append('index.html')

    for name in expected:
        path = os.path.join(SQP, name)
        if not os.path.exists(path):
            fail(name, 'MISSING from the delivery surface')
            continue
        with open(path, encoding='utf-8', newline='') as fh:
            text = fh.read()
        check_page(path, text, is_paper=bool(re.match(r'^QP\d+\.html$', name)))

    # Question count across the delivered papers must match the specs.
    delivered = 0
    for name in expected:
        if not re.match(r'^QP\d+\.html$', name):
            continue
        path = os.path.join(SQP, name)
        if os.path.exists(path):
            with open(path, encoding='utf-8', newline='') as fh:
                delivered += len(re.findall(r'class="q-num"', fh.read()))
    if delivered != total_q:
        fail('delivery', 'question count %d does not match specs %d' % (delivered, total_q))
    else:
        print('[ OK  ] %d questions delivered across %d papers'
              % (delivered, sum(1 for e in expected if re.match(r'^QP\d+\.html$', e))))


def check_oral_promo(specs):
    """The complete January paper shown to existing ORAL subscribers.

    Two things must hold at once, and they pull in opposite directions:
      * it must be COMPLETE — every question, every answer, nothing held
        back, because a half-sample would misrepresent the product;
      * it must not tell an Oral subscriber they own the Written library.
    """
    CHECKS[0] += 1
    path = os.path.join(REPO_ROOT, 'meoclass1', 'oralnotes',
                        'written-sample-january-2026.html')
    if not os.path.exists(path):
        fail('oral promo', 'January Written promo is missing')
        return
    with open(path, encoding='utf-8', newline='') as fh:
        html = fh.read()

    jan = next((d for d in specs if d['paper_id'] == 'QP2601'), None)
    if jan:
        n = len(re.findall(r'class="q-num"', html))
        if n != len(jan['questions']):
            fail('oral promo', 'has %d questions, the January spec has %d'
                 % (n, len(jan['questions'])))
        if 'Model written answer' not in html:
            fail('oral promo', 'no model answers — the promo must be complete')

    if 'noindex' not in html:
        fail('oral promo', 'must be noindex — it is inside the paid Oral product')
    if 'Unlock the full Solved QP' not in html:
        fail('oral promo', 'header CTA missing')
    if 'Get Solved QP Access' not in html:
        fail('oral promo', 'footer CTA missing')

    # The newest sitting in the closing CTA is derived; guard the claim.
    solved = [d for d in specs if any(q.get('model_answer') for q in d['questions'])]
    if solved:
        import recurrence_model as _RM
        newest = sorted(solved, key=lambda d: (d['year'], _RM.MONTH_NUM[d['month']]))[-1]
        if newest['month_year'] not in html:
            fail('oral promo', 'closing CTA does not name the newest sitting %r'
                 % newest['month_year'])

    # Must not imply the Oral subscriber already owns the Written library.
    for rx, why in [
        (re.compile(r'you (?:now )?own the (?:full|complete)', re.I), 'claims ownership'),
        (re.compile(r'included (?:with|in) your (?:Oral )?subscription', re.I),
         'implies the library is included'),
    ]:
        if rx.search(html):
            fail('oral promo', 'copy %s of the Solved QP library' % why)

    for rx, label in THIRD_PARTY + AUTHORING[:2]:
        m = rx.search(html)
        if m:
            fail('oral promo', 'leak (%s): %r' % (label, m.group(0)[:40]))

    print('[ OK  ] oral promo complete and correctly scoped')


def check_storefront(specs):
    """The storefront is hand-written HTML. Guard the two facts in it that
    are really derived from elsewhere, so they cannot drift silently:

      * the newest solved sitting  -- derived from the specs
      * the Solved QP price        -- owned by api/_lib/products.js
    """
    CHECKS[0] += 1
    idx = os.path.join(REPO_ROOT, 'SQ', 'index.html')
    if not os.path.exists(idx):
        fail('SQ/index.html', 'storefront missing')
        return
    with open(idx, encoding='utf-8', newline='') as fh:
        html = fh.read()

    # newest solved sitting
    solved = [d for d in specs if any(q.get('model_answer') for q in d['questions'])]
    if solved:
        import recurrence_model as _RM
        newest = sorted(solved, key=lambda d: (d['year'], _RM.MONTH_NUM[d['month']]))[-1]
        m = re.search(r'data-newest-sitting="([^"]+)"', html)
        if not m:
            fail('SQ/index.html', 'Written card has no data-newest-sitting marker')
        elif m.group(1).strip() != newest['month_year']:
            fail('SQ/index.html',
                 'newest sitting claims %r but the specs say %r'
                 % (m.group(1), newest['month_year']))

    # price agreement with the server catalogue
    cat = os.path.join(REPO_ROOT, 'api', '_lib', 'products.js')
    if os.path.exists(cat):
        with open(cat, encoding='utf-8', newline='') as fh:
            src = fh.read()
        m = re.search(r'SOLVED_QP\s*:\s*\{.*?amount:\s*(\d+)', src, re.S)
        if not m:
            fail('products.js', 'could not read the SOLVED_QP amount')
        else:
            paise = int(m.group(1))
            rupees = paise // 100
            shown = '₹%s,%03d' % (rupees // 1000, rupees % 1000) if rupees >= 1000 else '₹%d' % rupees
            if shown not in html:
                fail('SQ/index.html',
                     'storefront does not show the catalogue price %s (%d paise)' % (shown, paise))
            else:
                print('[ OK  ] storefront price %s agrees with the catalogue (%d paise)'
                      % (shown, paise))


def check_year_nav(specs):
    """Every delivered page must offer the year sheet for ITS OWN year.

    The delivery navigation used to carry a single hard-coded link to
    questions-2026.html. That was right only while 2026 was the only solved
    year: once 2024 and 2025 were solved, a reader of a 2024 paper was
    offered the 2026 sheet and had no route to their own. Nothing failed --
    the link resolved, the page existed, and every other guard passed --
    which is exactly why it needs a guard of its own.

    A paper links to its own year. A year sheet links to itself. The home
    covers every solved year, since it belongs to no single one.
    """
    CHECKS[0] += 1
    solved_years = sorted({d['year'] for d in specs
                           if any(q.get('model_answer') for q in d['questions'])})

    def nav_years(text):
        return sorted({int(y) for y in
                       re.findall(r'href="/solvedQP/questions-(\d{4})\.html"', text)})

    for d in specs:
        if not any(q.get('model_answer') for q in d['questions']):
            continue
        path = os.path.join(SQP, '%s.html' % d['paper_id'])
        if not os.path.exists(path):
            continue
        with open(path, encoding='utf-8', newline='') as fh:
            found = nav_years(fh.read())
        if d['year'] not in found:
            fail('%s.html' % d['paper_id'],
                 'year navigation offers %s but this paper is from %d'
                 % (found or 'nothing', d['year']))

    for y in solved_years:
        path = os.path.join(SQP, 'questions-%d.html' % y)
        if not os.path.exists(path):
            continue
        with open(path, encoding='utf-8', newline='') as fh:
            found = nav_years(fh.read())
        if y not in found:
            fail('questions-%d.html' % y,
                 'year sheet does not link to its own year; offers %s' % (found or 'nothing'))

    home = os.path.join(SQP, 'index.html')
    if os.path.exists(home):
        with open(home, encoding='utf-8', newline='') as fh:
            found = nav_years(fh.read())
        missing = [y for y in solved_years if y not in found]
        if missing:
            fail('index.html', 'product home does not reach solved year(s) %s'
                 % ', '.join(str(y) for y in missing))

    print('[ OK  ] year navigation is year-aware across %d solved year(s)'
          % len(solved_years))


def self_test():
    """Positive control: every guard must fire on a page built to trip it."""
    print('-- self-test: a deliberately defective page must be REJECTED --')
    bad = (
        '<html><head><title>x</title>'
        '<script type="application/ld+json">{}</script></head><body>'
        '<a href="/meoclass1/QB1_A.html">oral</a>'
        '<span>Exact repeat</span><span>12 prior sittings</span>'
        '<p>Recurrence recorded on the source paper: 2018/APR, 2019/JUN.</p>'
        '<div>Founder review copy</div>'
        '</body></html>'
    )
    before = len(FAILS)
    check_page(os.path.join(SQP, '__selftest__.html'), bad, is_paper=True)
    fired = FAILS[before:]
    del FAILS[before:]          # discard synthetic failures

    wanted = ['not noindex', 'JSON-LD', 'THIRD-PARTY LEAK', 'authoring field leaked',
              'links into the Oral product', 'no model answer']
    missing = [w for w in wanted
               if not any(w.split()[0].lower() in f.lower() for f in fired)]
    for f in fired:
        print('   fired: %s' % f)
    if missing:
        print('SELF-TEST FAILED — these guards did not fire: %s' % ', '.join(missing))
        return False
    print('   %d guards fired as expected' % len(fired))

    # Year-aware navigation, proved by mutation. A 2024 paper whose nav offers
    # only the 2026 sheet is the exact regression the fix removed, so the guard
    # is asserted against that page rather than against the fixed one.
    before = len(FAILS)
    stale = '<a href="/solvedQP/questions-2026.html">Questions by year</a>'
    fake = [{'year': 2024, 'paper_id': '__selftestyear__',
             'questions': [{'model_answer': {'blocks': []}}]}]
    tmp = os.path.join(SQP, '__selftestyear__.html')
    wrote = False
    try:
        os.makedirs(SQP, exist_ok=True)
        with open(tmp, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(stale)
        wrote = True
        check_year_nav(fake)
    finally:
        if wrote:
            os.remove(tmp)
    year_fired = FAILS[before:]
    del FAILS[before:]
    if not any('2024' in f for f in year_fired):
        print('SELF-TEST FAILED — the year-navigation guard did not fire on a '
              '2024 paper offering only the 2026 sheet')
        return False
    print('   year-navigation guard fired on the stale-2026 regression')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()

    ok = True
    if args.self_test:
        ok = self_test()

    run()

    if FAILS:
        for f in FAILS:
            print('[FAIL ] %s' % f)
        print('solvedqp_check: %d failure(s) across %d page(s)' % (len(FAILS), CHECKS[0]))
        sys.exit(1)
    if not ok:
        sys.exit(1)
    print('[ OK  ] solvedQP delivery clean across %d page(s)' % CHECKS[0])


if __name__ == '__main__':
    main()
