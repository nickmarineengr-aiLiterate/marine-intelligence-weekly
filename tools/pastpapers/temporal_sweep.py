#!/usr/bin/env python3
"""Date-aware future-contamination and donor cross-reference sweep. DETECTION ONLY.

Usage:
  python tools/pastpapers/temporal_sweep.py [SPEC ...] [--self-test] [--json] [-v]

Part of the Production Intelligence Layer (PIL). PIL FLAGS; CLAUDE ADJUDICATES.

Two mechanical sweeps over the CANDIDATE-FACING authored fields of every solved
spec:

  A. POST-SITTING DATE CANDIDATES. The paper's sitting month/year comes from the
     spec. Every date token in a candidate-facing field is parsed and compared
     against the end of the sitting month. Anything later is reported.

  C. INTERNAL Q-REFERENCE CANDIDATES. Bounded PROSE forms -- "See Q8",
     "Q1 of this paper", "refer to Q5" -- which is how a donor's own internal
     numbering has repeatedly been inherited into a target paper that numbers
     its questions differently. Structured ``cross_links`` are NOT swept: a
     canonical link legitimately carries a Q id.

  B. RESOLUTION / ASSEMBLY SESSION DATES ARE DELIBERATELY NOT AUTOMATED. Turning
     an identifier such as ``A.1207(34)`` into an adoption date requires knowing
     when the 34th Assembly sat, which is source knowledge, not string handling.
     Building that table would make this tool assert regulatory facts. It does
     not. In practice the surrounding prose carries the date token anyway, which
     sweep A catches -- that is exactly how the QP2509 A.1207(34) defect reads.

WHAT THIS TOOL NEVER DECIDES
    Whether a flag is an error. A future date can be entirely correct for its
    sitting -- "not yet in force; expected December 2027" was true and knowable
    in September 2025. The output is CANDIDATE, never ERROR. Suppressing a flag
    because the prose says "expected" or "not yet" would be a semantic guess, so
    no such suppression exists. Noise is controlled by FIELD TARGETING only.

WHY FIELD TARGETING, AND WHY THESE FIELDS
    Provenance fields -- ``sources``, ``verification_status``,
    ``reverify_before_publication``, ``temporal_review``, ``decomposition_gate``,
    ``reuse_evidence`` -- carry post-sitting dates BY CONSTRUCTION: they record
    when the authoring and verification happened, which is always after the
    sitting. Sweeping them would guarantee a flag on every paper forever.
    Worse, they are where a REMOVED defect is written down: QP2509 Q2 records
    'Three "See Q8" pointers inherited from the donor were removed'. A sweep
    over that text would flag the audit trail proving the fix. This is the same
    self-trip that ``known_traps_check.py`` guards with EXEMPT_PATHS.

    So the scope is the authored answer layer a candidate actually reads.

Exit code is 0 when the sweep runs. Flags are reported, not failed on -- whether
a particular flag blocks READY is Claude's judgement under
TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md. --self-test exits non-zero if a
positive control fails.
"""
import argparse, calendar, glob, io, json, os, re, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import is_intake  # noqa: E402

REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
PP = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')

# ---------------------------------------------------------------- field scope

# Authored answer-layer fields a candidate reads. Sweeping starts at these keys
# on a question object and descends through whatever structure they hold.
CANDIDATE_FACING = (
    'model_answer',
    'study_notes',
    'quick_revision',
    'memory_cue',
    'understand_first',
    'retrieval_cards',
    'answer_route',
    'regulations',
    'short_title',
)

# NOT swept at all. A cross-link label names ANOTHER paper -- "QP2602 Q4 -
# February 2026" -- so it carries that paper's sitting month by construction,
# and every forward link would flag forever. It is a navigational label, not
# authored answer content, and its Q id is canonical rather than prose. Both
# sweeps therefore exclude it, for the same mechanical reason.
CROSS_LINKS = 'cross_links'

# Named here so the exclusion is a decision on the record rather than an
# accident of which keys were listed above. See the module docstring.
EXCLUDED_INTERNAL = (
    'sources', 'verification_status', 'reverify_before_publication',
    'temporal_review', 'decomposition_gate', 'reuse_evidence', 'unresolved',
    'question_delta', 'provenance_summary', 'text_verbatim', 'decomposition',
)

# --------------------------------------------------------------- date parsing

MONTHS = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}
MONTHS.update({m.lower(): i for i, m in enumerate(calendar.month_abbr) if m})

_MONTH_RE = '|'.join(sorted(MONTHS, key=len, reverse=True))

# Each pattern yields a (year, month) pair. Day precision is parsed where it is
# printed but the comparison is month-granular, because the spec records the
# sitting month, not the exam day.
DATE_PATTERNS = [
    # 3 December 2025 / 03 December 2025 / 3rd December 2025
    ('DMY_TEXT', re.compile(
        r'\b(\d{1,2})(?:st|nd|rd|th)?\s+(%s)\.?,?\s+(\d{4})\b' % _MONTH_RE, re.I),
     lambda m: (int(m.group(3)), MONTHS[m.group(2).lower()])),
    # December 3, 2025 / December 3 2025
    ('MDY_TEXT', re.compile(
        r'\b(%s)\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b' % _MONTH_RE, re.I),
     lambda m: (int(m.group(3)), MONTHS[m.group(1).lower()])),
    # December 2025
    ('MONTH_YEAR', re.compile(
        r'\b(%s)\.?\s+(\d{4})\b' % _MONTH_RE, re.I),
     lambda m: (int(m.group(2)), MONTHS[m.group(1).lower()])),
    # 2025-12-03
    ('ISO', re.compile(r'\b(\d{4})-(\d{2})-(\d{2})\b'),
     lambda m: (int(m.group(1)), int(m.group(2)))),
    # 03-12-2025 / 03/12/2025 -- read day-first, the convention of this series'
    # source papers. Where day-first gives an impossible month the month-first
    # reading is taken instead, so a US-formatted date is still parsed rather
    # than silently dropped.
    ('NUMERIC', re.compile(r'\b(\d{1,2})[-/](\d{1,2})[-/](\d{4})\b'),
     lambda m: (int(m.group(3)),
                int(m.group(2)) if 1 <= int(m.group(2)) <= 12 else int(m.group(1)))),
]

# A bare year later than the sitting year. Kept separate and lower-confidence:
# it is the form that carries "in force from 2027" with no month attached.
BARE_YEAR = re.compile(r'\b(19|20)\d{2}\b')

# --------------------------------------------------- internal prose Q-refs

# Bounded prose forms only. Each is anchored so that an explicit CROSS-PAPER
# reference -- "see QP2508 Q8" -- does not match: that names its paper and is
# therefore controlled, which is the opposite of the defect being hunted.
_NOT_QUALIFIED = r'(?<!QP\d{4} )(?<!QP\d{4})'
QREF_PATTERNS = [
    re.compile(r'\b(?:see|refer to|as discussed in|as in|per)\s+' + _NOT_QUALIFIED
               + r'Q(\d{1,2})\b', re.I),
    re.compile(r'\bQ(\d{1,2})\s+of\s+(?:this|the)\s+(?:same\s+)?paper\b', re.I),
    re.compile(r'\bQ(\d{1,2})\s+of\s+this\s+same\s+paper\b', re.I),
]


def sitting_of(spec):
    """(year, month) of the sitting, from canonical spec metadata."""
    y = int(spec['year'])
    m = MONTHS.get(str(spec.get('month', '')).strip().lower())
    if not m:
        raise ValueError('spec %s has no parsable month: %r'
                         % (spec.get('paper_id'), spec.get('month')))
    return y, m


def walk_strings(node, path):
    """Yield (path, string) for every string under node."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_strings(v, '%s/%s' % (path, k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_strings(v, '%s[%d]' % (path, i))
    elif isinstance(node, str):
        yield path, node


def candidate_fields(question):
    """Yield (path, string) over the candidate-facing authored fields only."""
    for k in CANDIDATE_FACING:
        if k in question and question[k] is not None:
            yield from walk_strings(question[k], k)


def scan_dates(text, sitting):
    """Yield (kind, token, (y, m)) for date tokens later than the sitting month."""
    sy, sm = sitting
    seen = []
    for kind, rx, extract in DATE_PATTERNS:
        for m in rx.finditer(text):
            try:
                y, mo = extract(m)
            except (KeyError, ValueError):
                continue
            if not (1 <= mo <= 12):
                continue
            span = m.span()
            # A longer pattern already covering this span wins: "3 December
            # 2025" must not also report as "December 2025".
            if any(span[0] >= a and span[1] <= b for a, b in seen):
                continue
            seen.append(span)
            if (y, mo) > (sy, sm):
                yield kind, m.group(0), (y, mo)
    for m in BARE_YEAR.finditer(text):
        span = m.span()
        if any(span[0] >= a and span[1] <= b for a, b in seen):
            continue
        if int(m.group(0)) > sy:
            yield 'BARE_YEAR', m.group(0), (int(m.group(0)), 0)


def scan_qrefs(text, valid_q_numbers):
    """Yield (token, n, in_range) for bounded prose internal Q-references."""
    hits = []
    for rx in QREF_PATTERNS:
        for m in rx.finditer(text):
            span = m.span()
            if any(span[0] >= a and span[1] <= b for a, b in hits):
                continue
            hits.append(span)
            n = int(m.group(1))
            yield m.group(0), n, n in valid_q_numbers


def sweep_spec(spec):
    """Return a list of flag dicts for one loaded spec. No judgement applied."""
    pid = spec['paper_id']
    sitting = sitting_of(spec)
    sitting_label = spec.get('month_year') or '%s %d' % (spec['month'], spec['year'])
    valid_q = set()
    for q in spec.get('questions', []):
        m = re.match(r'Q(\d+)', str(q.get('q_no', '')))
        if m:
            valid_q.add(int(m.group(1)))

    flags, seen = [], set()

    def add(qid, path, token, reason, form):
        # One row per (question, field, token, reason). The same date repeated
        # inside one paragraph is one thing to adjudicate, not several.
        key = (qid, path, token, reason)
        if key in seen:
            return
        seen.add(key)
        flags.append({'paper': pid, 'question': qid, 'field': path,
                      'token': token, 'sitting': sitting_label,
                      'reason': reason, 'form': form})

    for q in spec.get('questions', []):
        qid = q.get('question_id') or q.get('q_no')
        for path, text in candidate_fields(q):
            for kind, token, _when in scan_dates(text, sitting):
                add(qid, path, token,
                    'POST_SITTING_YEAR_CANDIDATE' if kind == 'BARE_YEAR'
                    else 'POST_SITTING_DATE_CANDIDATE', kind)
            for token, n, in_range in scan_qrefs(text, valid_q):
                add(qid, path, token,
                    'INTERNAL_QREF_CANDIDATE' if in_range
                    else 'INTERNAL_QREF_OUT_OF_RANGE',
                    'Q%d %s' % (n, 'exists in this paper' if in_range
                                else 'DOES NOT EXIST in this paper'))
    return flags


def load_specs(paths):
    out = []
    for p in paths:
        d = json.load(open(p, encoding='utf-8'))
        if is_intake(d):
            continue
        out.append((p, d))
    return out


def report(flags, as_json, stream=sys.stdout):
    if as_json:
        json.dump(flags, stream, indent=2)
        stream.write('\n')
        return
    if not flags:
        stream.write('  no candidates\n')
        return
    order = {'INTERNAL_QREF_OUT_OF_RANGE': 0, 'INTERNAL_QREF_CANDIDATE': 1,
             'POST_SITTING_DATE_CANDIDATE': 2, 'POST_SITTING_YEAR_CANDIDATE': 3}
    for f in sorted(flags, key=lambda f: (order.get(f['reason'], 9), f['paper'],
                                          str(f['question']), f['field'])):
        stream.write('  [%-28s] %-8s %-14s %-42s %r  (sitting %s; %s)\n'
                     % (f['reason'], f['paper'], f['question'], f['field'],
                        f['token'], f['sitting'], f['form']))


# ------------------------------------------------------------------ self-test

def _fixture(month, year, **question_fields):
    q = {'q_no': 'Q1', 'question_id': 'FIX-Q1'}
    q.update(question_fields)
    return {'paper_id': 'FIXTURE', 'month': month, 'year': year,
            'build_state': 'Complete', 'questions': [
                q,
                {'q_no': 'Q2', 'question_id': 'FIX-Q2'},
                {'q_no': 'Q3', 'question_id': 'FIX-Q3'},
            ]}


def self_test():
    """Positive controls. Every guard here has been demonstrated to fire."""
    checks = []

    def expect(name, ok, detail=''):
        checks.append((name, ok, detail))

    # CONTROL 1 -- the real QP2509 defect shape: a December 2025 date inside a
    # September 2025 paper, in a candidate-facing field.
    f = sweep_spec(_fixture('September', 2025, quick_revision={
        'major_trap': 'Resolution A.1207(34) was adopted on 3 December 2025.'}))
    hit = [x for x in f if x['reason'] == 'POST_SITTING_DATE_CANDIDATE']
    expect('C1 post-sitting date (3 December 2025 in Sept 2025)',
           len(hit) == 1 and hit[0]['token'] == '3 December 2025',
           repr([x['token'] for x in f]))

    # CONTROL 2 -- the donor cross-reference shape.
    f = sweep_spec(_fixture('September', 2025, study_notes=[
        {'p': 'CII is in force and enforceable. See Q8 of this paper.'}]))
    hit = [x for x in f if x['reason'].startswith('INTERNAL_QREF')]
    expect('C2 prose "See Q8" flagged', len(hit) >= 1, repr(f))
    expect('C2 out-of-range detected (fixture has 3 questions)',
           any(x['reason'] == 'INTERNAL_QREF_OUT_OF_RANGE' for x in hit), repr(hit))

    # CONTROL 3 -- a pre-sitting date must NOT raise a future-date flag.
    f = sweep_spec(_fixture('September', 2025, quick_revision={
        'critical_numbers': ['MEPC.400(83) was adopted on 11 April 2025.']}))
    expect('C3 pre-sitting date not flagged',
           not [x for x in f if x['reason'] == 'POST_SITTING_DATE_CANDIDATE'], repr(f))

    # CONTROL 4 -- a structured cross_links entry carrying a valid Q id must not
    # raise a PROSE reference flag.
    f = sweep_spec(_fixture('September', 2025, cross_links=[
        {'label': 'QP2602 Q4 - February 2026 - IMSBC groups and BCSN',
         'href': 'QP2602.html#q4'}]))
    expect('C4 structured cross_links not prose-flagged',
           not [x for x in f if x['reason'].startswith('INTERNAL_QREF')], repr(f))
    expect('C4a cross_links label date not flagged (it is another paper\'s sitting)',
           not [x for x in f if x['reason'].startswith('POST_SITTING')], repr(f))
    # ...and an explicitly qualified cross-paper prose reference is controlled.
    f = sweep_spec(_fixture('September', 2025, model_answer=[
        {'p': 'The limitation machinery is worked through in see QP2508 Q8.'}]))
    expect('C4b qualified "QP2508 Q8" not flagged',
           not [x for x in f if x['reason'].startswith('INTERNAL_QREF')], repr(f))

    # CONTROL 5 -- MUTATION: the checker itself must be able to fail. Break the
    # date comparison and assert the controls stop passing. A guard that has
    # never been shown to fail is not proven.
    import copy
    saved = list(DATE_PATTERNS)
    try:
        DATE_PATTERNS[:] = []
        f = sweep_spec(_fixture('September', 2025, quick_revision={
            'major_trap': 'adopted on 3 December 2025.'}))
        expect('C5 mutation: date sweep disabled -> C1 no longer fires',
               not [x for x in f if x['reason'] == 'POST_SITTING_DATE_CANDIDATE'],
               repr(f))
    finally:
        DATE_PATTERNS[:] = saved
    # re-prove C1 after restoring, so the mutation cannot leave the tool blind
    f = sweep_spec(_fixture('September', 2025, quick_revision={
        'major_trap': 'adopted on 3 December 2025.'}))
    expect('C5 mutation reverted -> detection restored',
           any(x['reason'] == 'POST_SITTING_DATE_CANDIDATE' for x in f), repr(f))

    saved_q = list(QREF_PATTERNS)
    try:
        QREF_PATTERNS[:] = []
        f = sweep_spec(_fixture('September', 2025, study_notes=[{'p': 'See Q8.'}]))
        expect('C5 mutation: qref sweep disabled -> C2 no longer fires',
               not [x for x in f if x['reason'].startswith('INTERNAL_QREF')], repr(f))
    finally:
        QREF_PATTERNS[:] = saved_q

    # CONTROL 6 -- field targeting is the noise control, so prove it holds in
    # BOTH directions. An excluded provenance field must be out of scope, and a
    # candidate-facing field must be in scope, for identical text.
    text = 'Verified on 3 December 2025. See Q8 of this paper.'
    f = sweep_spec(_fixture('September', 2025, verification_status=text,
                            temporal_review={'notes': [text]}, reuse_evidence=[text]))
    expect('C6 provenance fields out of scope', not f, repr(f))
    f = sweep_spec(_fixture('September', 2025, memory_cue=text))
    expect('C6 candidate-facing field in scope', len(f) >= 2, repr(f))

    # CONTROL 7 -- numeric and ISO forms.
    f = sweep_spec(_fixture('September', 2025, memory_cue='Due 2025-12-03 and 03/12/2025.'))
    expect('C7 ISO and numeric forms flagged',
           len([x for x in f if x['reason'] == 'POST_SITTING_DATE_CANDIDATE']) == 2, repr(f))

    # CONTROL 8 -- a sitting-known future reference is STILL flagged. The tool
    # must not suppress on "expected"/"not yet"; that would be a semantic guess.
    f = sweep_spec(_fixture('September', 2025, model_answer=[
        {'p': 'Not yet in force; expected December 2027.'}]))
    expect('C8 "not yet / expected" still flagged (no semantic suppression)',
           any(x['reason'] == 'POST_SITTING_DATE_CANDIDATE' for x in f), repr(f))

    width = max(len(n) for n, _, _ in checks)
    failed = 0
    for name, ok, detail in checks:
        print('  %-*s  %s' % (width, name, 'PASS' if ok else 'FAIL'))
        if not ok:
            failed += 1
            print('      got: %s' % detail)
    print('  %d control(s), %d failed' % (len(checks), failed))
    return 1 if failed else 0


# ------------------------------------------------------- retrospective test

# The two defects this sweep exists because of, both from QP2509 production.
# Neither pre-fix spec was ever committed -- both were caught and corrected
# inside the authoring session -- so there are no historical bytes to replay.
# The DONORS are still in the repository, though, and the defect in both cases
# was the donor's own text carried forward unchanged into a September 2025
# sitting. So the fixture is built by transplanting the real donor question
# into the target's sitting, in memory. Real bytes, real defect shape, and
# nothing is written: specs/ is never touched.
RETROSPECTIVE = [
    ('A.1207(34) / 3 December 2025 carried into a September 2025 sitting',
     'QP2606', 'Q8', 'POST_SITTING_DATE_CANDIDATE', '3 December 2025'),
    ('donor internal "See Q8" carried into a September 2025 sitting',
     'QP2508', 'Q2', 'INTERNAL_QREF_CANDIDATE', None),
]


def retrospective():
    """Replay the two known QP2509 defects against the sweep. Read-only."""
    target = json.load(open(os.path.join(PP, 'specs', 'QP2509.json'), encoding='utf-8'))
    failed = 0
    for label, donor_id, donor_q, want_reason, want_token in RETROSPECTIVE:
        donor = json.load(open(os.path.join(PP, 'specs', '%s.json' % donor_id),
                               encoding='utf-8'))
        src = next(q for q in donor['questions'] if q['q_no'] == donor_q)
        fixture = {
            'paper_id': 'RETRO-%s-from-%s' % (target['paper_id'], donor_id),
            'month': target['month'], 'year': target['year'],
            'month_year': target['month_year'], 'build_state': 'Complete',
            # The donor question keeps its own number so the transplant is what
            # it claims to be; the target's full question list is preserved so
            # in-range/out-of-range is judged against the TARGET paper.
            'questions': [dict(src, question_id='RETRO-%s' % src['q_no'])]
            + [{'q_no': q['q_no']} for q in target['questions']
               if q['q_no'] != donor_q],
        }
        flags = sweep_spec(fixture)
        hits = [f for f in flags if f['reason'] == want_reason
                and (want_token is None or f['token'] == want_token)]
        ok = bool(hits)
        print('  %-4s %s' % ('PASS' if ok else 'FAIL', label))
        print('       donor %s %s -> %d flag(s) of %s'
              % (donor_id, donor_q, len(hits), want_reason))
        for h in hits[:4]:
            print('         %-42s %r' % (h['field'], h['token']))
        if not ok:
            failed += 1
            print('       got: %r' % [(f['reason'], f['token']) for f in flags][:12])
    print('  %d retrospective case(s), %d failed' % (len(RETROSPECTIVE), failed))
    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('specs', nargs='*', help='spec paths; default every solved spec')
    ap.add_argument('--self-test', action='store_true')
    ap.add_argument('--retrospective', action='store_true',
                    help='replay the two known QP2509 defects (read-only)')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('-v', '--verbose', action='store_true')
    args = ap.parse_args()

    if args.self_test:
        print('temporal_sweep self-test')
        rc = self_test()
        print('temporal_sweep retrospective (known QP2509 defects)')
        sys.exit(rc or retrospective())

    if args.retrospective:
        print('temporal_sweep retrospective (known QP2509 defects)')
        sys.exit(retrospective())

    paths = args.specs or sorted(glob.glob(os.path.join(PP, 'specs', '*.json')))
    loaded = load_specs(paths)
    all_flags = []
    for p, d in loaded:
        all_flags.extend(sweep_spec(d))

    if args.json:
        report(all_flags, True)
        sys.exit(0)

    by_reason = {}
    for f in all_flags:
        by_reason[f['reason']] = by_reason.get(f['reason'], 0) + 1
    print('temporal sweep: %d solved spec(s), %d candidate(s)'
          % (len(loaded), len(all_flags)))
    for r in sorted(by_reason):
        print('  %-30s %d' % (r, by_reason[r]))
    print('-' * 58)
    report(all_flags, False)
    print('-' * 58)
    print('CANDIDATES ONLY. A post-sitting date may be correct for its sitting.')
    print('Adjudicate under TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md.')
    sys.exit(0)


if __name__ == '__main__':
    main()
