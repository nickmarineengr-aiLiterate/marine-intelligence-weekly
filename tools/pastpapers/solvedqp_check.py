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


WARNS = []


def warn(where, msg):
    """Something a human should decide, not a defect.

    Kept out of FAILS on purpose: a warning must never block a delivery,
    or the next person to meet one will be tempted to silence it. The
    price ladder is the case this exists for -- the check can see that a
    step has become due, but only the Founder may move a price.
    """
    WARNS.append('%s: %s' % (where, msg))
    print('[WARN ] %s: %s' % (where, msg))


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


from recurrence_model import MONTHS, MONTH_NUM

# "September" -> "Sep". The card abbreviates; the specs do not.
MONTH_ABBR = {m[:3]: m for m in MONTHS}


def expected_coverage_months(solved, year):
    """The months a year's coverage entry must name, in sitting order.

    Derived from the specs and nothing else. The storefront is hand-written,
    so the moment this list is typed anywhere but here it is a second copy
    of the truth and will drift from the first.
    """
    return [d['month'] for d in
            sorted((d for d in solved if d['year'] == year),
                   key=lambda d: MONTH_NUM[d['month']])]


def coverage_entry(coverage, year):
    """The visible text of one year's entry, and nothing after it.

    Slicing only up to the next `<strong>20dd:</strong>` is not enough for
    the LAST year in the block: everything that follows the list -- the
    closing span, the line break, and the "newest solved sitting: July 2026"
    sentence -- would still be inside it. A month regex over that text
    harvests July as though 2026 advertised a July sitting it might not
    have. Cut at the first structural tag instead.
    """
    m = re.search(r'<strong>%d:</strong>(.*?)(?=<strong>20\d\d:</strong>|$)' % year,
                  coverage, re.S)
    if not m:
        return None
    return re.split(r'</span>|<br\s*/?>', m.group(1))[0]


def check_coverage_months(coverage, solved):
    """Every solved year's entry must name EXACTLY the months delivered.

    THIS IS THE HOLE THE YEAR-SET CHECK LEFT OPEN. On 2026-08-14 the card
    read "2023: Jan, Apr, Dec" while the manifest held five solved 2023
    papers -- January, March, April, September and December. Every guard
    passed: the newest sitting was right, the price was right, the paper
    and question totals were right, and the coverage block did name 2023.
    Only the months inside that entry were stale, and nothing looked at
    them. A customer comparing the card against the product would have
    found two sittings they were never told they had bought.

    The months are read out of the specs, never typed here. Hard-coding
    "Jan, Mar, Apr, Sep, Dec" to make this pass would recreate the defect
    one layer down -- the storefront and the checker would then agree with
    each other and both be wrong the next time a paper lands.

    A year advertised as a complete year states no month list by design;
    the completeness claim itself is checked against the calendar below,
    which is the stronger test.
    """
    for year in sorted({d['year'] for d in solved}):
        entry = coverage_entry(coverage, year)
        if entry is None:
            continue                    # the year-set check above owns this
        if 'complete year' in entry:
            continue

        want = expected_coverage_months(solved, year)
        got = [MONTH_ABBR[a] for a in re.findall(r'\b(%s)\b' % '|'.join(MONTH_ABBR), entry)]

        if not got:
            fail('SQ/index.html',
                 '%d names no sittings and makes no complete-year claim, but the '
                 'corpus delivers %s' % (year, ', '.join(want)))
            continue

        missing = [m for m in want if m not in got]
        extra = [m for m in got if m not in want]
        if missing:
            fail('SQ/index.html',
                 '%d coverage omits %s -- solved and delivered, but the customer '
                 'is not told they get it' % (year, ', '.join(missing)))
        if extra:
            fail('SQ/index.html',
                 '%d coverage advertises %s, which the corpus does not deliver'
                 % (year, ', '.join(extra)))
        if not missing and not extra and got != want:
            fail('SQ/index.html',
                 '%d coverage lists the right sittings out of order: %s, expected %s'
                 % (year, ' · '.join(got), ' · '.join(want)))
        if not missing and not extra and got == want:
            print('[ OK  ] %d coverage names exactly its %d solved sitting(s): %s'
                  % (year, len(want), ' · '.join(m[:3] for m in want)))


def check_storefront(specs):
    """The storefront is hand-written HTML. Guard the facts in it that are
    really derived from elsewhere, so they cannot drift silently:

      * the newest solved sitting  -- derived from the specs
      * the Solved QP price        -- owned by api/_lib/products.js
      * the paper and question COUNTS -- derived from the specs
      * the per-year coverage list -- derived from the specs

    THE COUNTS ARE HERE BECAUSE THEY ALREADY DRIFTED ONCE.

    On 2026-08-14 the card was still advertising "Twelve complete solved
    sittings -- 108 questions" and a coverage line reading "2024: Mar,
    Apr". The corpus had reached 31 papers and 279 worked answers, with
    2024 and 2025 complete. The storefront was selling roughly a third
    of the product, and had been for weeks, because the only facts under
    guard were the newest sitting and the price -- both of which happened
    to stay correct while everything around them went stale.

    A number that a human retypes after every paper is a number that
    will eventually be forgotten. The fix is not to try harder; it is to
    make the omission fail the build.
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

    # ---- paper and question counts ----
    # Every element carrying data-solvedqp-papers / -questions must agree
    # with the corpus, and the same number must appear in the element's
    # visible text -- otherwise the attribute could be updated while the
    # sentence a candidate actually reads stays wrong.
    if solved:
        n_papers = len(solved)
        n_questions = sum(
            len([q for q in d['questions'] if q.get('model_answer')]) for d in solved
        )

        for attr, expected in (('data-solvedqp-papers', n_papers),
                               ('data-solvedqp-questions', n_questions)):
            found = re.findall(attr + r'="(\d+)"', html)
            if not found:
                fail('SQ/index.html',
                     'no element carries %s -- the storefront counts are unguarded, '
                     'which is exactly how "12 papers / 108 questions" survived to '
                     '31 papers / 279 questions' % attr)
                continue
            for claimed in found:
                if int(claimed) != expected:
                    fail('SQ/index.html',
                         '%s claims %s but the corpus has %d' % (attr, claimed, expected))

        # The visible sentence, not just the machine-readable attribute.
        for expected, what in ((n_papers, 'paper count'), (n_questions, 'question count')):
            if not re.search(r'\b%d\b' % expected, html):
                fail('SQ/index.html',
                     'the %s %d appears in no visible text on the storefront'
                     % (what, expected))

        # ---- per-year coverage ----
        # Each year the corpus delivers must be named on the card, and no
        # year may be advertised that the corpus does not have.
        years = sorted({d['year'] for d in solved})
        # Anchored on its own marker. Keying off data-solvedqp-papers
        # instead would match the STATS tile first -- same attribute,
        # different element -- and silently check the wrong text.
        m_cov = re.search(r'data-solvedqp-coverage[^>]*>(.*?)</div>', html, re.S)
        if not m_cov:
            fail('SQ/index.html', 'no element marked data-solvedqp-coverage')
        coverage = m_cov.group(1) if m_cov else ''

        # Look for the year LABEL, not the bare digits. The block also
        # contains prose like "January 2023 to July 2026", so a substring
        # test for "2023" passes even after the 2023 entry is deleted --
        # which is exactly how this check first shipped, and it did not
        # fire when the entry was removed.
        labelled = set(int(y) for y in re.findall(r'<strong>(20\d\d):</strong>', coverage))
        for y in years:
            if y not in labelled:
                fail('SQ/index.html',
                     'coverage block has no "%d:" entry, but the corpus delivers '
                     '%d paper(s) for it' % (y, len([d for d in solved if d['year'] == y])))
        for claimed in labelled - set(years):
            fail('SQ/index.html',
                 'coverage block advertises %d, which the corpus does not deliver' % claimed)

        # ---- per-year MONTH LIST ----
        # Naming the year is not enough. See check_coverage_months.
        check_coverage_months(coverage, solved)

        # A "complete year" claim must be true: every sitting that took
        # place that year is solved.
        #
        # THE DENOMINATOR IS THE WHOLE POINT. Counting specs is useless --
        # every spec in the repo is a solved paper, so specs-for-year
        # always equals solved-for-year and the claim is true by
        # construction. The first version of this check did exactly that
        # and would have certified 2023 (3 sittings of 11) and 2026 (a
        # year still in progress) as complete years.
        #
        # The real denominator is the calendar: twelve months, less the
        # sittings the manifest records as KNOWN_ABSENT. No May sitting
        # occurs in any year MIW holds, which is why a complete year is
        # eleven papers and not twelve.
        absent_by_year = {}
        mpath = os.path.join(REPO_ROOT, 'solvedQP', 'solvedqp_content_index.json')
        if os.path.exists(mpath):
            with open(mpath, encoding='utf-8') as fh:
                for a in json.load(fh).get('known_absent', []):
                    absent_by_year[a['year']] = absent_by_year.get(a['year'], 0) + 1

        for y in sorted(labelled):
            entry = re.search(r'<strong>%d:</strong>(.*?)(?=<strong>20\d\d:|$)' % y,
                              coverage, re.S)
            if not entry or 'complete year' not in entry.group(1):
                continue
            got = len([d for d in solved if d['year'] == y])
            sittings = 12 - absent_by_year.get(y, 0)
            if got != sittings:
                fail('SQ/index.html',
                     'card calls %d a complete year, but only %d of its %d sittings '
                     'are solved' % (y, got, sittings))
            else:
                # "all 11 sittings" is a second, retyped copy of the same
                # number. Guard the digits a candidate reads, not only the
                # claim behind them.
                m_n = re.search(r'all\s+(\d+)\s+sittings', entry.group(1))
                if m_n and int(m_n.group(1)) != sittings:
                    fail('SQ/index.html',
                         '%d is advertised as "all %s sittings" but the year holds %d'
                         % (y, m_n.group(1), sittings))
                else:
                    print('[ OK  ] %d really is a complete year (%d of %d sittings, '
                          'May never sits)' % (y, got, sittings))

        print('[ OK  ] storefront advertises %d papers / %d questions, matching the corpus'
              % (n_papers, n_questions))
        print('[ OK  ] coverage block names exactly the years delivered: %s'
              % ', '.join(str(y) for y in years))

    # ---- price ladder ----
    # Founder decision: SolvedQP is priced at roughly 500 rupees per exam
    # year, stepping when a year completes. NOTHING HERE CHANGES A PRICE.
    # A script that silently re-prices a product is a script that can
    # overcharge a candidate; the amount stays a Founder decision in
    # products.js. What is automated is only the REMINDER, because the
    # step is easy to miss on the day it becomes due -- the same way the
    # paper counts were missed for weeks.
    if solved:
        cat_path = os.path.join(REPO_ROOT, 'api', '_lib', 'products.js')
        if os.path.exists(cat_path):
            with open(cat_path, encoding='utf-8', newline='') as fh:
                cat_src = fh.read()
            m_l = re.search(r'priceLadder:\s*\{[^}]*stepsWhenYearCompletes:\s*(\d+)', cat_src)
            m_n = re.search(r'priceLadder:\s*\{[^}]*nextAmount:\s*(\d+)', cat_src)
            m_a = re.search(r'SOLVED_QP\s*:\s*\{.*?amount:\s*(\d+)', cat_src, re.S)
            if m_l and m_n and m_a:
                step_year, next_amount, current = int(m_l.group(1)), int(m_n.group(1)), int(m_a.group(1))
                got = len([d for d in solved if d['year'] == step_year])
                sittings = 12 - absent_by_year.get(step_year, 0)
                if got >= sittings and current < next_amount:
                    warn('products.js',
                         '%d is now a complete year (%d of %d sittings). The approved price '
                         'ladder steps to %d paise at this point and the catalogue still says '
                         '%d. This is a FOUNDER DECISION -- nothing has been changed.'
                         % (step_year, got, sittings, next_amount, current))
                else:
                    print('[ OK  ] price ladder: %d is at %d of %d sittings, no step due'
                          % (step_year, got, sittings))

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

    # ---- coverage month list, proved by mutation ----
    # Driven with synthetic coverage HTML rather than the shipped card, so
    # the control keeps proving the guard bites after the real storefront
    # changes. A fixture harvested from live state stops being a test the
    # day the thing it harvested moves.
    fake_solved = [
        {'year': 2023, 'month': 'January'}, {'year': 2023, 'month': 'March'},
        {'year': 2023, 'month': 'April'}, {'year': 2023, 'month': 'September'},
        {'year': 2023, 'month': 'December'},
        {'year': 2024, 'month': 'March'}, {'year': 2024, 'month': 'June'},
    ]
    GOOD = ('<strong>2023:</strong> Jan · Mar · Apr · Sep · Dec &nbsp;—&nbsp;'
            '<strong>2024:</strong> Mar · Jun</span><br>'
            'newest solved sitting: <strong>July 2026</strong>')

    # Negative control FIRST: the correct card must be accepted. A guard
    # that rejects the truth is worse than no guard -- the next person will
    # edit the check until it passes, and the real defect walks through.
    before = len(FAILS)
    check_coverage_months(GOOD, fake_solved)
    if FAILS[before:]:
        print('SELF-TEST FAILED — the month-list guard rejected a CORRECT '
              'coverage block: %s' % '; '.join(FAILS[before:]))
        del FAILS[before:]
        return False
    print('   month-list guard accepts a correct coverage block')

    # Positive controls: one mutation per failure mode this guard exists for.
    mutations = [
        ('omitted month  (the 2026-08-14 live defect)',
         GOOD.replace('Jan · Mar · Apr · Sep · Dec', 'Jan · Apr · Dec'), 'omits'),
        ('invented month (sold a sitting that is not solved)',
         GOOD.replace('Jan · Mar · Apr', 'Jan · Feb · Mar · Apr'), 'advertises'),
        ('wrong month    (Sep silently became Oct)',
         GOOD.replace('Sep', 'Oct'), 'omits'),
        ('out of order   (right sittings, misleading sequence)',
         GOOD.replace('Jan · Mar · Apr · Sep · Dec', 'Dec · Jan · Mar · Apr · Sep'),
         'out of order'),
        ('new paper published, card never updated',
         GOOD, 'omits'),
    ]
    for label, mutated, wanted in mutations:
        solved_for = fake_solved
        if wanted == 'omits' and mutated == GOOD:
            # The commonest real failure: the corpus grows, the hand-written
            # card does not. Mutate the CORPUS, not the HTML.
            solved_for = fake_solved + [{'year': 2023, 'month': 'October'}]
        before = len(FAILS)
        check_coverage_months(mutated, solved_for)
        fired = FAILS[before:]
        del FAILS[before:]
        if not any(wanted in f for f in fired):
            print('SELF-TEST FAILED — the month-list guard did not fire on: %s' % label)
            return False
        print('   month-list guard fired on %s' % label)

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
