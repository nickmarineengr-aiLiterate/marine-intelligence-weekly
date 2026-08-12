#!/usr/bin/env python3
"""Daily health check for the Solved QP delivery product.

Usage:
  python tools/pastpapers/solvedqp_health_check.py            # remote: main via tarball
  python tools/pastpapers/solvedqp_health_check.py --local    # this working tree
  python tools/pastpapers/solvedqp_health_check.py --self-test
  python tools/pastpapers/solvedqp_health_check.py --no-email

WHAT IT IS FOR
--------------
Everything else in tools/pastpapers/ runs at build time against the working
tree, where a mistake is caught before it ships. This one runs on a schedule
against what is ACTUALLY ON main, which is what customers are served, and it
emails the result. It is the only check that can notice that a page went
missing, that a count drifted, or that a link died after the build that made it.

Modelled on meoclass1/qb_health_check.py -- same tarball fetch, same Brevo
relay, same "clean run still sends a report" discipline -- and deliberately NOT
merged into it. That checker knows about q-cards, CE Oral tips and the Oral
trap ledger; none of that exists in a Written paper, and a Written paper has
a sitting date, which changes what counts as an error (see TEMPORAL below).

INVENTORY AUTHORITY
-------------------
Every count comes from solvedQP/solvedqp_content_index.json. This checker
builds no inventory of its own -- it asserts that the manifest, the delivery
HTML, the year sheets and the home page all agree with it. A third opinion
about how many papers exist is exactly what it is here to prevent.

TEMPORAL -- THE RULE THAT MAKES THIS CHECKER DIFFERENT
------------------------------------------------------
A Written paper answers the examination AS SAT. Current-law trap rules must
therefore never be applied to it blindly:

    A.1185(33) is WRONG as current 2026 law -- A.1206(34) superseded it --
    but it is RIGHT for QP2512, sat in December 2025.

    "Merchant Shipping Act, 1958" is WRONG as current law -- the 2025 Act
    commenced 15 March 2026 -- but it is RIGHT for every 2024 and 2025 sitting,
    which is twenty-two of the twenty-eight papers in the corpus.

The Oral ledger at meoclass1/known_traps.md greps for both of those phrases.
Pointing this checker at that ledger would raise roughly a hundred findings on
correct content, every morning, for ever -- and a report that is wrong every
day is a report nobody reads. So:

  * the Oral ledger is NOT used here. The Written ledger at
    meoclass1/pastpapers/known_traps.md is, and it already resolves this by
    marking time-sensitive entries `GREP: SKIP` (entry 11) so they are
    human-reviewed rather than auto-flagged.

  * forward contamination IS checked, deterministically and in one direction
    only: an instrument may not be asserted as OPERATIVE in a paper that was
    sat before that instrument existed. That test is safe because it needs no
    judgement -- only the sitting date and the instrument's own date.

  * where the sitting month EQUALS the boundary month, the finding is REVIEW,
    never ERROR. A December 2025 sitting and a 3 December 2025 adoption cannot
    be ordered from a month alone, and a checker that guesses would be
    manufacturing a verdict.

No AI judgement runs in CI. Every check here is deterministic.

Exit 1 on ERROR. WARN and REVIEW never fail the job.
"""
import argparse, io, json, os, re, smtplib, ssl, sys, tarfile, urllib.request
from email.mime.text import MIMEText

if __name__ == '__main__':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:                                            # pragma: no cover
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

GITHUB_REPO = 'nickmarineengr-aiLiterate/marine-intelligence-weekly'
GITHUB_BRANCH = 'main'
MANIFEST_PATH = 'solvedQP/solvedqp_content_index.json'
DELIVERY_PREFIX = 'solvedQP/'
WRITTEN_TRAPS = 'meoclass1/pastpapers/known_traps.md'
WANTED_PREFIXES = (DELIVERY_PREFIX, 'meoclass1/pastpapers/known_traps.md')

# Brevo, exactly as the QB checker uses it. No second mail provider, and no
# credential is ever written down here.
EMAIL_TO = os.environ.get('SOLVEDQP_HEALTH_EMAIL_TO',
                          os.environ.get('QB_HEALTH_EMAIL_TO',
                                         'contactus@marineintelligenceweekly.com'))
SMTP_LOGIN = os.environ.get('BREVO_SMTP_LOGIN', '')
EMAIL_FROM = os.environ.get('BREVO_SENDER_EMAIL', 'contactus@marineintelligenceweekly.com')
SMTP_HOST = 'smtp-relay.brevo.com'
SMTP_PORT = 587

VOID_ELEMENTS = {'br', 'img', 'meta', 'link', 'hr', 'input', 'area', 'base',
                 'col', 'embed', 'source', 'track', 'wbr'}

# The five modes every delivered question must carry.
FIVE_MODES = ('understand', 'plan', 'answer', 'guide', 'recall')

# Strings that must never appear on a page a customer is served.
LEAKAGE = [
    (r'(?i)founder[\s\-]*review', 'Founder-review banner or copy'),
    (r'(?i)\breview copy\b', 'review-copy marker'),
    (r'(?i)dieselship', 'third-party source-host branding'),
    (r'(?i)PRICE_TBD', 'unresolved price sentinel'),
    (r'(?i)\bTODO\b|\bFIXME\b', 'draft marker'),
    (r'(?i)https?://localhost', 'localhost link'),
    (r'(?i)https?://127\.0\.0\.1', 'loopback link'),
    (r'[A-Za-z]:\\\\?(?:Users|RulesApp|Marine-Intelligence)', 'local filesystem path'),
    (r'(?i)RulesApp-Local-Input', 'private corpus path'),
    (r'(?i)/meoclass1/pastpapers/docs/[^"\']*\.pdf', 'source PDF link'),
    (r'(?i)\brecurrence_class\b', 'authoring field recurrence_class'),
    (r'(?i)\bhost_recurrence_hint\b', 'authoring field host_recurrence_hint'),
]

# ---------------------------------------------------------------------------
# Forward-contamination guards.
#
# Each entry: a phrase that asserts an instrument is OPERATIVE, and the date it
# actually became operative. A paper sat strictly BEFORE that date must not
# assert it. Same-month is REVIEW, never ERROR.
#
# Only instruments with an unambiguous, verified operative date belong here.
# Anything needing judgement stays in known_traps.md as GREP: SKIP.
# ---------------------------------------------------------------------------
FORWARD_GUARDS = [
    {
        'id': 'MSA2025',
        'boundary': (2026, 3),
        'label': 'Merchant Shipping Act, 2025 (commenced 15 March 2026)',
        # "the MS Act 2025 governs / is in force / commenced" -- an assertion of
        # current operation, not a mention that it is coming.
        'patterns': [
            r'(?i)merchant shipping act,?\s*2025[^.]{0,80}?\b(?:is in force|in force|commenced|governs|repeal(?:s|ed))',
            r'(?i)\bunder the merchant shipping act,?\s*2025\b',
        ],
    },
    {
        'id': 'A120634',
        'boundary': (2025, 12),
        'label': 'Resolution A.1206(34), adopted 3 December 2025',
        'patterns': [r'A\.1206\(34\)'],
    },
    {
        'id': 'A34',
        'boundary': (2025, 12),
        'label': '34th IMO Assembly resolutions (adopted 24 Nov - 3 December 2025)',
        'patterns': [r'A\.1\d{3}\(34\)'],
    },
    {
        'id': 'A33',
        'boundary': (2023, 12),
        'label': '33rd IMO Assembly resolutions (adopted 6 December 2023)',
        'patterns': [r'A\.1\d{3}\(33\)'],
    },
]

# Current-law trap phrases that this checker MUST NOT flag on a historical
# paper. Named explicitly so the exemption is a decision on the record rather
# than an omission somebody later "fixes".
CURRENT_LAW_TRAPS_NOT_APPLIED = [
    ('A.1185(33)', 'correct for any sitting before December 2025, including QP2512'),
    ('Merchant Shipping Act, 1958', 'correct for every 2024 and 2025 sitting'),
]

findings = []   # (level, area, message); level in ERROR / WARN / REVIEW / OK


def add(level, area, msg):
    findings.append((level, area, msg))


def err(area, msg):
    add('ERROR', area, msg)


def warn(area, msg):
    add('WARN', area, msg)


def review(area, msg):
    add('REVIEW', area, msg)


def ok(area, msg):
    add('OK', area, msg)


# ------------------------------------------------------------------ sources

def fetch_remote():
    """{repo-relative path: bytes} for the delivery surface on main."""
    url = 'https://codeload.github.com/%s/tar.gz/refs/heads/%s' % (GITHUB_REPO, GITHUB_BRANCH)
    req = urllib.request.Request(url, headers={'User-Agent': 'solvedqp-health-check'})
    with urllib.request.urlopen(req, timeout=90) as resp:
        raw = resp.read()
    files = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as tar:
        for m in tar.getmembers():
            if not m.isfile():
                continue
            parts = m.name.split('/', 1)
            if len(parts) != 2:
                continue
            rel = parts[1]
            if rel.startswith(WANTED_PREFIXES):
                f = tar.extractfile(m)
                if f is not None:
                    files[rel] = f.read()
    return files


def read_local():
    files = {}
    for rel_root in (DELIVERY_PREFIX.rstrip('/'), 'meoclass1/pastpapers'):
        base = os.path.join(REPO_ROOT, rel_root.replace('/', os.sep))
        for dirpath, _dirs, names in os.walk(base):
            for n in names:
                p = os.path.join(dirpath, n)
                rel = os.path.relpath(p, REPO_ROOT).replace(os.sep, '/')
                if rel.startswith(WANTED_PREFIXES):
                    files[rel] = io.open(p, 'rb').read()
    return files


# ------------------------------------------------------------------- checks

def text_of(b):
    return b.decode('utf-8', 'replace')


def strip_comments(html):
    """Build machinery is not customer-facing copy.

    Every delivered paper carries `<!-- GATE SCRIPT STRIPPED FOR REVIEW COPY -->`.
    Scanning raw HTML for the words "review copy" therefore flagged all eighteen
    pages on the first run -- eighteen daily errors about a comment no reader can
    see. Comments come out before any leakage or trap scan; the markup itself
    stays, because href-shaped leaks (localhost, source PDFs) live in attributes.
    """
    return re.sub(r'(?s)<!--.*?-->', ' ', html)


def visible_text(html):
    s = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', strip_comments(html))
    return re.sub(r'<[^>]+>', ' ', s)


def answer_text(html):
    """Only the ANSWER panes of a paper, as visible text.

    This distinction is the whole of the temporal design. A Written answer is
    written to the law AS SAT, but the STUDY GUIDE is explicitly where the
    candidate is told the law has since changed -- so QP2512's guide is REQUIRED
    to say that the Merchant Shipping Act, 2025 commenced on 15 March 2026,
    after the sitting. Scanning the whole page for later law therefore convicts
    the product of doing exactly what it is supposed to do; the first run raised
    seven such errors. Forward contamination is only a defect inside the answer.
    """
    src = strip_comments(html)
    out = []
    for mm in re.finditer(r'<div class="mode" data-mode="answer"[^>]*>', src):
        i = mm.end()
        depth = 1
        for t in re.finditer(r'<(/?)div\b[^>]*?(/?)>', src[i:]):
            if t.group(2):
                continue
            depth += -1 if t.group(1) else 1
            if depth == 0:
                out.append(src[i:i + t.start()])
                break
    joined = ' '.join(out)
    joined = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', joined)
    return re.sub(r'<[^>]+>', ' ', joined)


# Cues that a sentence is EXCLUDING an instrument rather than relying on it.
# "the 2025 Act had assent but had not commenced at this sitting" is the correct
# thing for a 2025 answer to say, and a guard that cannot tell it apart from
# contamination is a guard that fires on correctness.
NEGATION_CUES = (
    'not commenced', 'had not', 'has not', 'not yet', 'was not', 'is not',
    'not in force', 'after this sitting', 'after the sitting', 'not relied',
    'later than', 'would not', 'did not', 'never', 'no longer',
    'at this sitting the', 'postdates', 'subsequent to',
)

# The same idea where a fixed phrase is too rigid. QP2602's answer reads
# "...in force 15 March 2026 - some five weeks after this paper was sat", which
# is a model piece of temporal honesty and was the last false positive standing.
NEGATION_PATTERNS = (
    r'after (?:this|that|the) (?:sitting|paper|examination|exam|date)',
    r'after (?:this|that|the) paper was sat',
    r'(?:weeks|months|days|years) after',
    r'had (?:not|yet to)\b',
    r'only (?:from|after)\b',
)


def sentence_around(text, pos):
    start = max(text.rfind('.', 0, pos), text.rfind(';', 0, pos)) + 1
    end = text.find('.', pos)
    end = len(text) if end < 0 else end + 1
    return re.sub(r'\s+', ' ', text[start:end]).strip()


def check_manifest_present(files):
    if MANIFEST_PATH not in files:
        err('manifest', 'MISSING: %s -- nothing downstream can be verified' % MANIFEST_PATH)
        return None
    try:
        m = json.loads(text_of(files[MANIFEST_PATH]))
    except Exception as e:
        err('manifest', 'unparseable: %s' % e)
        return None
    ok('manifest', 'manifest present, version %s, generated %s'
       % (m.get('manifest_version'), m.get('generated')))
    return m


def check_inventory(m, files):
    """§36 -- manifest, HTML on disk and the manifest's own totals must agree."""
    avail = [p for p in m['papers'] if p['status'] == 'AVAILABLE']
    planned = [p for p in m['papers'] if p['status'] == 'PLANNED_SOON']

    if m['available_papers'] != len(avail):
        err('inventory', 'available_papers=%d but %d papers are marked AVAILABLE'
            % (m['available_papers'], len(avail)))
    if m['planned_papers'] != len(planned):
        err('inventory', 'planned_papers=%d but %d papers are marked PLANNED_SOON'
            % (m['planned_papers'], len(planned)))
    if m['total_papers'] != len(m['papers']):
        err('inventory', 'total_papers=%d but %d paper records exist'
            % (m['total_papers'], len(m['papers'])))

    published = sum(len(p['questions']) for p in avail)
    if m['available_questions'] != published:
        err('inventory', 'available_questions=%d but %d question rows are published'
            % (m['available_questions'], published))

    html_papers = sorted(re.sub(r'^solvedQP/|\.html$', '', k)
                         for k in files
                         if re.fullmatch(r'solvedQP/QP\d{4}\.html', k))
    manifest_avail = sorted(p['paper_id'] for p in avail)
    if html_papers != manifest_avail:
        missing = sorted(set(manifest_avail) - set(html_papers))
        extra = sorted(set(html_papers) - set(manifest_avail))
        if missing:
            err('inventory', 'AVAILABLE in the manifest with no delivery page: %s'
                % ', '.join(missing))
        if extra:
            err('inventory', 'delivery page exists that the manifest does not list '
                'as AVAILABLE: %s' % ', '.join(extra))
    if not findings_have_error('inventory'):
        ok('inventory', '%d available paper(s), %d published question(s), '
           '%d planned, %d month(s) with no sitting -- manifest and files agree'
           % (len(avail), published, len(planned), m['known_absent_sittings']))

    # Home page and year sheets must not carry a different count.
    home = files.get('solvedQP/index.html')
    if home is None:
        err('inventory', 'solvedQP/index.html is missing')
    else:
        h = text_of(home)
        if not re.search(r'<b>%d</b>\s*<span>solved sittings' % len(avail), h):
            err('inventory', 'home page headline does not state %d solved sittings'
                % len(avail))
        if not re.search(r'<b>%d</b>\s*<span>questions' % published, h):
            err('inventory', 'home page headline does not state %d questions' % published)


def findings_have_error(area):
    return any(l == 'ERROR' and a == area for l, a, _ in findings)


def check_status_files(m, files):
    """§37 -- a status is a promise about what exists."""
    bad = 0
    for p in m['papers']:
        path = 'solvedQP/%s.html' % p['paper_id']
        if p['status'] == 'AVAILABLE':
            if path not in files:
                err('status', '%s is AVAILABLE but %s does not exist' % (p['paper_id'], path))
                bad += 1
        else:
            if path in files:
                err('status', '%s is PLANNED_SOON but a delivery page exists at %s'
                    % (p['paper_id'], path))
                bad += 1
            if p.get('href'):
                err('status', '%s is PLANNED_SOON but carries an href' % p['paper_id'])
                bad += 1
            if p.get('questions'):
                err('status', '%s is PLANNED_SOON but publishes %d question stem(s)'
                    % (p['paper_id'], len(p['questions'])))
                bad += 1
    for a in m.get('known_absent', []):
        pid = 'QP%02d%02d' % (a['year'] % 100, a['month_num'])
        if 'solvedQP/%s.html' % pid in files:
            err('status', '%s %d is recorded as KNOWN_ABSENT but a paper page exists'
                % (a['month'], a['year']))
            bad += 1
    if not bad:
        ok('status', 'every AVAILABLE paper has a page; no planned or absent sitting has one')


def check_paper_structure(m, files):
    """§38 -- shape of a delivered paper."""
    bad = 0
    for p in m['papers']:
        if p['status'] != 'AVAILABLE':
            continue
        path = 'solvedQP/%s.html' % p['paper_id']
        if path not in files:
            continue
        h = text_of(files[path])
        if p['question_count'] != 9:
            review('structure', '%s carries %d questions, not the usual 9 -- confirm '
                   'against the printed paper' % (p['paper_id'], p['question_count']))
        ids = re.findall(r'\sid="(q\d+)"', h)
        if len(ids) != len(set(ids)):
            err('structure', '%s has duplicate element ids: %s'
                % (p['paper_id'], ', '.join(sorted({i for i in ids if ids.count(i) > 1}))))
            bad += 1
        for q in p['questions']:
            if ('id="%s"' % q['anchor']) not in h:
                err('structure', '%s: anchor #%s is in the manifest but not in the page'
                    % (q['question_id'], q['anchor']))
                bad += 1
        low = h.lower()
        missing = [mo for mo in FIVE_MODES if ('data-mode="%s"' % mo) not in low
                   and ('>%s<' % mo) not in low]
        if len(missing) == len(FIVE_MODES):
            err('structure', '%s: none of the five modes are detectable on the page'
                % p['paper_id'])
            bad += 1
        d = tag_balance(h)
        if d:
            err('structure', '%s: unbalanced HTML (%s)' % (p['paper_id'], d))
            bad += 1
    if not bad:
        ok('structure', 'every delivered paper has unique ids, live anchors, balanced '
           'HTML and the five modes')


def tag_balance(html):
    s = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', html)
    s = re.sub(r'(?s)<!--.*?-->', ' ', s)
    stack = []
    for mm in re.finditer(r'<(/?)([a-zA-Z][\w-]*)([^>]*?)(/?)>', s):
        closing, name, attrs, selfclose = mm.groups()
        name = name.lower()
        if name in VOID_ELEMENTS or selfclose:
            continue
        if closing:
            if not stack:
                return 'stray </%s>' % name
            if stack[-1] != name:
                return '</%s> closes <%s>' % (name, stack[-1])
            stack.pop()
        else:
            stack.append(name)
    return 'unclosed <%s>' % stack[-1] if stack else ''


def check_links(m, files):
    """§39 + §40 -- every candidate-facing link and every search target resolves."""
    bad = 0
    targets = {k for k in files if k.startswith(DELIVERY_PREFIX)}
    for p in m['papers']:
        if p['status'] != 'AVAILABLE':
            continue
        if p['href'].lstrip('/') not in targets:
            err('links', '%s href %s does not resolve' % (p['paper_id'], p['href']))
            bad += 1
        for q in p['questions']:
            base, _, frag = q['href'].partition('#')
            if base.lstrip('/') not in targets:
                err('links', '%s search target %s does not resolve' % (q['question_id'], base))
                bad += 1
            elif ('id="%s"' % frag) not in text_of(files[base.lstrip('/')]):
                err('links', '%s search target anchor #%s does not exist'
                    % (q['question_id'], frag))
                bad += 1
    for name in ('solvedQP/index.html',) + tuple(
            'solvedQP/questions-%d.html' % y for y in m['years']):
        if name not in files:
            err('links', 'missing product page %s' % name)
            bad += 1
            continue
        for href in set(re.findall(r'href="(/solvedQP/[^"#]+)(?:#[^"]*)?"',
                                   text_of(files[name]))):
            if href.lstrip('/') not in targets:
                err('links', '%s links to %s, which does not exist' % (name, href))
                bad += 1
    if not bad:
        ok('links', 'home, year sheets, paper hrefs and every search target resolve')


def check_search_integrity(m):
    """§40 -- the search payload itself."""
    bad = 0
    qids, seen_pairs = set(), set()
    for p in m['papers']:
        for q in p['questions']:
            if p['status'] != 'AVAILABLE':
                err('search', '%s is searchable but its paper is %s'
                    % (q['question_id'], p['status']))
                bad += 1
            if q['question_id'] in qids:
                err('search', 'duplicate question identity %s' % q['question_id'])
                bad += 1
            qids.add(q['question_id'])
            pair = (q['paper_id'], q['question_number'])
            if pair in seen_pairs:
                err('search', 'duplicate %s %s' % pair)
                bad += 1
            seen_pairs.add(pair)
            if not (q.get('search_text') or '').strip():
                err('search', '%s has empty search_text and can never be found'
                    % q['question_id'])
                bad += 1
            if q['paper_id'] != p['paper_id']:
                err('search', '%s is filed under %s' % (q['question_id'], p['paper_id']))
                bad += 1
    if not bad:
        ok('search', '%d searchable question(s), all unique, all on AVAILABLE papers'
           % len(qids))


def check_paid_boundary(m):
    """§41 + §52 -- the manifest must stay metadata."""
    blob = json.dumps(m, ensure_ascii=False)
    banned = ['model_answer', 'study_notes', 'quick_revision', 'answer_route',
              'retrieval_cards', 'memory_cue', 'recurrence_class',
              'host_recurrence_hint', 'reuse_tier', 'verification_status']
    hit = [b for b in banned if '"%s"' % b in blob]
    if hit:
        err('boundary', 'manifest carries paid or authoring field(s): %s' % ', '.join(hit))
    else:
        ok('boundary', 'manifest carries question stems and labels only -- no answer '
           'text, no authoring field')


def check_leakage(files):
    """§41 -- nothing internal on a page a customer is served."""
    bad = 0
    for name in sorted(files):
        if not name.startswith(DELIVERY_PREFIX) or not name.endswith('.html'):
            continue
        h = strip_comments(text_of(files[name]))
        for pat, what in LEAKAGE:
            if re.search(pat, h):
                err('leakage', '%s contains %s' % (name, what))
                bad += 1
    if not bad:
        ok('leakage', 'no review banner, host branding, local path or draft marker on '
           'any delivered page')


def check_known_traps(m, files):
    """§43 -- the WRITTEN ledger only, and only its greppable entries."""
    raw = files.get(WRITTEN_TRAPS)
    if raw is None:
        warn('traps', 'written trap ledger not in the snapshot -- trap scan skipped')
        return
    text = text_of(raw)
    entries, skipped = [], 0
    for block in re.split(r'\n### ', text)[1:]:
        head = block.splitlines()[0].strip()
        g = re.search(r'^GREP:\s*(.+)$', block, re.M)
        val = g.group(1).strip() if g else None
        if val is None or val.upper() == 'SKIP':
            skipped += 1
            continue
        entries.append((head, val))
    bad = 0
    for name in sorted(files):
        if not name.startswith(DELIVERY_PREFIX) or not name.endswith('.html'):
            continue
        vis = visible_text(text_of(files[name]))
        for head, phrase in entries:
            if phrase.lower() in vis.lower():
                err('traps', '%s contains trap phrase %r (%s)' % (name, phrase, head))
                bad += 1
    if not bad:
        ok('traps', '%d greppable written trap(s) scanned across the delivery surface, '
           '%d manual-review-only. The ORAL ledger is deliberately not applied: %s.'
           % (len(entries), skipped,
              '; '.join('%s is %s' % (p, why) for p, why in CURRENT_LAW_TRAPS_NOT_APPLIED)))


def check_temporal(m, files):
    """§44 -- forward contamination only, judged against each paper's sitting."""
    bad = 0
    for p in m['papers']:
        if p['status'] != 'AVAILABLE':
            continue
        path = 'solvedQP/%s.html' % p['paper_id']
        if path not in files:
            continue
        # ANSWER panes only. See answer_text(): the study guide is required to
        # discuss later law, so scanning the whole page inverts the test.
        ans = answer_text(text_of(files[path]))
        sitting = (p['year'], p['month_num'])
        for guard in FORWARD_GUARDS:
            hit = None
            for pat in guard['patterns']:
                hit = re.search(pat, ans)
                if hit:
                    break
            if not hit:
                continue
            by, bm = guard['boundary']
            if sitting > (by, bm):
                continue                      # sat after it existed -- correct
            sent = sentence_around(ans, hit.start())
            low = sent.lower()
            if (any(c in low for c in NEGATION_CUES)
                    or any(re.search(p2, low) for p2 in NEGATION_PATTERNS)):
                continue                      # the answer is excluding it, correctly
            if sitting == (by, bm):
                review('temporal', '%s (%s) cites %s in its answer, and the boundary '
                       'falls in the same month. A month cannot order these -- confirm '
                       'against the sitting date. Sentence: %s'
                       % (p['paper_id'], p['sitting'], guard['label'], sent[:160]))
                continue
            err('temporal', '%s was sat in %s but its ANSWER asserts %s as operative, '
                'which is later than the sitting. Sentence: %s'
                % (p['paper_id'], p['sitting'], guard['label'], sent[:160]))
            bad += 1
    if not bad:
        ok('temporal', '%d forward-contamination guard(s) applied per sitting; no paper '
           'asserts an instrument that postdates it' % len(FORWARD_GUARDS))


def check_updates(m):
    """§23 -- the latest-updates strip must be honest and internally silent."""
    bad = 0
    ids = {p['paper_id'] for p in m['papers']}
    for u in m.get('recently_updated', []):
        if u['paper_id'] not in ids:
            err('updates', 'update record names unknown paper %s' % u['paper_id'])
            bad += 1
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', u['date']):
            err('updates', 'update record for %s has a malformed date %r'
                % (u['paper_id'], u['date']))
            bad += 1
        if re.search(r'(?i)\b(commit|branch|merge|rebase|toolchain|spec)\b', u['summary']):
            warn('updates', 'update record for %s exposes internal process language: %s'
                 % (u['paper_id'], u['summary'][:80]))
    dates = [u['date'] for u in m.get('recently_updated', [])]
    if dates != sorted(dates, reverse=True):
        err('updates', 'recently_updated is not newest-first')
        bad += 1
    if not bad:
        ok('updates', '%d update record(s), newest first, every one naming a real paper'
           % len(dates))


def check_freshness(m):
    """Manifest age against its own content date."""
    gen = m.get('generated', '')
    newest = max((u['date'] for u in m.get('recently_updated', [])), default=None)
    if newest and gen < newest:
        err('freshness', 'manifest generated %s but carries a %s update -- it is stale'
            % (gen, newest))
    else:
        ok('freshness', 'manifest content date %s is not behind its newest record' % gen)


# --------------------------------------------------------------- self-test

def self_test(files):
    """Inject each defect the checker exists to catch, and require a catch."""
    import copy
    base_m = json.loads(text_of(files[MANIFEST_PATH]))
    results = []

    def run(name, mutate):
        global findings
        saved = findings
        findings = []
        f2 = dict(files)
        m2 = copy.deepcopy(base_m)
        m2 = mutate(m2, f2) or m2
        try:
            check_inventory(m2, f2)
            check_status_files(m2, f2)
            check_paper_structure(m2, f2)
            check_links(m2, f2)
            check_search_integrity(m2)
            check_paid_boundary(m2)
            check_leakage(f2)
            check_known_traps(m2, f2)
            check_temporal(m2, f2)
            check_updates(m2)
            check_freshness(m2)
        except Exception as e:                                   # pragma: no cover
            findings.append(('ERROR', 'self-test', 'raised %r' % e))
        caught = [f for f in findings if f[0] == 'ERROR']
        findings = saved
        results.append((name, bool(caught), caught[0][2][:78] if caught else ''))

    def drop_paper(m, f):
        pid = next(p['paper_id'] for p in m['papers'] if p['status'] == 'AVAILABLE')
        f.pop('solvedQP/%s.html' % pid, None)
    run('missing delivery page for an AVAILABLE paper', drop_paper)

    def wrong_count(m, f):
        m['available_questions'] += 1
    run('manifest question count disagrees with the rows', wrong_count)

    def wrong_papers(m, f):
        m['available_papers'] += 1
    run('manifest paper count disagrees with the rows', wrong_papers)

    def broken_anchor(m, f):
        p = next(p for p in m['papers'] if p['status'] == 'AVAILABLE')
        p['questions'][0]['anchor'] = 'q99'
        p['questions'][0]['href'] = '/solvedQP/%s.html#q99' % p['paper_id']
    run('broken question anchor / missing search target', broken_anchor)

    def planned_live(m, f):
        p = next(p for p in m['papers'] if p['status'] == 'PLANNED_SOON')
        p['href'] = '/solvedQP/%s.html' % p['paper_id']
    run('PLANNED_SOON card carrying a live link', planned_live)

    def planned_stems(m, f):
        p = next(p for p in m['papers'] if p['status'] == 'PLANNED_SOON')
        q = next(x for x in m['papers'] if x['status'] == 'AVAILABLE')['questions'][0]
        p['questions'] = [dict(q, paper_id=p['paper_id'])]
    run('unsolved paper publishing question stems', planned_stems)

    def review_banner(m, f):
        pid = next(p['paper_id'] for p in m['papers'] if p['status'] == 'AVAILABLE')
        k = 'solvedQP/%s.html' % pid
        f[k] = f[k].replace(b'<body>', b'<body><div>Founder review copy</div>', 1)
    run('review banner in a paid delivery page', review_banner)

    def trap_phrase(m, f):
        pid = next(p['paper_id'] for p in m['papers'] if p['status'] == 'AVAILABLE')
        k = 'solvedQP/%s.html' % pid
        f[k] = f[k].replace(
            b'<body>', b'<body><p>CLC 1992 does not apply to a bunker spill.</p>', 1)
    run('known written trap phrase on a delivered page', trap_phrase)

    def future_law(m, f):
        # Injected INSIDE an answer pane on purpose. Dropping it after <body>
        # -- which is what the first version of this fixture did -- proves
        # nothing now that the guard is scoped to answers, and the self-test
        # correctly failed until the fixture was put where the rule applies.
        p = next(p for p in m['papers'] if p['status'] == 'AVAILABLE' and p['year'] <= 2025)
        k = 'solvedQP/%s.html' % p['paper_id']
        marker = b'<div class="mode" data-mode="answer">'
        assert marker in f[k], 'no answer pane in %s' % k
        f[k] = f[k].replace(
            marker,
            marker + b'<p>Liability arises under the Merchant Shipping Act, 2025.</p>', 1)
    run('future statute asserted as operative on an earlier sitting', future_law)

    def paid_text(m, f):
        m['papers'][0]['model_answer'] = 'x'
    run('paid field in the manifest', paid_text)

    def dup_q(m, f):
        p = next(p for p in m['papers'] if p['status'] == 'AVAILABLE')
        p['questions'].append(dict(p['questions'][0]))
    run('duplicate question identity', dup_q)

    def bad_update(m, f):
        m['recently_updated'].insert(0, {'date': '2026-08-13', 'paper_id': 'QP9999',
                                         'sitting': 'x', 'kind': 'added',
                                         'summary': 'x', 'questions': []})
    run('update record naming a paper that does not exist', bad_update)

    # And the one that must NOT fire: current law on a historical paper.
    def historical_ok(m, f):
        p = next(p for p in m['papers'] if p['status'] == 'AVAILABLE' and p['year'] <= 2025)
        k = 'solvedQP/%s.html' % p['paper_id']
        f[k] = f[k].replace(
            b'<body>',
            b'<body><p>PSC procedures follow Resolution A.1185(33), and the Merchant '
            b'Shipping Act, 1958 governs.</p>', 1)
    global findings
    saved = findings
    findings = []
    f2 = dict(files)
    m2 = copy.deepcopy(base_m)
    historical_ok(m2, f2)
    check_known_traps(m2, f2)
    check_temporal(m2, f2)
    quiet = not [f for f in findings if f[0] == 'ERROR']
    findings = saved
    results.append(('current-law phrases on a historical paper stay QUIET', quiet,
                    '' if quiet else 'FALSE POSITIVE'))

    print('SOLVEDQP HEALTH CHECK SELF-TEST')
    failed = 0
    for name, good, detail in results:
        print('  [ %-4s ] %s%s' % ('OK' if good else 'FAIL', name,
                                   ('  -- %s' % detail) if detail and good else ''))
        if not good:
            failed += 1
    print('%d/%d' % (len(results) - failed, len(results)))
    return failed == 0


# ------------------------------------------------------------------ report

def build_report(source_label):
    order = {'ERROR': 0, 'REVIEW': 1, 'WARN': 2, 'OK': 3}
    rows = sorted(findings, key=lambda f: (order[f[0]], f[1]))
    n = {k: sum(1 for f in findings if f[0] == k) for k in order}
    clean = n['ERROR'] == 0
    head = ('SOLVEDQP HEALTH: PASS' if clean else 'SOLVEDQP HEALTH: %d ERROR(S)' % n['ERROR'])
    lines = [head, '=' * len(head), '',
             'Source   : %s' % source_label,
             'Errors   : %d' % n['ERROR'],
             'Review   : %d   (needs a human, not a failure)' % n['REVIEW'],
             'Warnings : %d' % n['WARN'],
             'Passed   : %d' % n['OK'], '']
    for level in ('ERROR', 'REVIEW', 'WARN', 'OK'):
        block = [f for f in rows if f[0] == level]
        if not block:
            continue
        lines.append('%s' % level)
        lines.append('-' * len(level))
        for _l, area, msg in block:
            lines.append('  [%-9s] %s' % (area, msg))
        lines.append('')
    return head, '\n'.join(lines)


def send_email(subject, body):
    key = os.environ.get('BREVO_SMTP_KEY')
    if not SMTP_LOGIN or not key:
        print('BREVO_SMTP_LOGIN / BREVO_SMTP_KEY not set -- printing the report instead.')
        print(body)
        return False
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    ctx = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls(context=ctx)
        s.login(SMTP_LOGIN, key)
        s.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
    print('Report emailed to %s' % EMAIL_TO)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--local', action='store_true', help='scan this working tree')
    ap.add_argument('--self-test', action='store_true')
    ap.add_argument('--no-email', action='store_true')
    args = ap.parse_args()

    if args.local or args.self_test:
        files = read_local()
        label = 'local working tree %s' % REPO_ROOT
    else:
        files = fetch_remote()
        label = 'github.com/%s @ %s' % (GITHUB_REPO, GITHUB_BRANCH)

    if args.self_test:
        return 0 if self_test(files) else 1

    m = check_manifest_present(files)
    if m is not None:
        check_inventory(m, files)
        check_status_files(m, files)
        check_paper_structure(m, files)
        check_links(m, files)
        check_search_integrity(m)
        check_paid_boundary(m)
        check_leakage(files)
        check_known_traps(m, files)
        check_temporal(m, files)
        check_updates(m)
        check_freshness(m)

    subject, body = build_report(label)
    if args.no_email:
        print(body)
    else:
        if not send_email('[MIW] %s' % subject, body):
            pass
    return 1 if any(f[0] == 'ERROR' for f in findings) else 0


if __name__ == '__main__':
    sys.exit(main())
