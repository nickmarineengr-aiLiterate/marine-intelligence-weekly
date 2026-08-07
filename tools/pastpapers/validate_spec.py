#!/usr/bin/env python3
"""Validate a past-paper content spec before it is rendered.

Usage: python validate_spec.py <spec.json>

Checks structure, marks arithmetic, id uniqueness, provenance honesty and the
answer/verification state machine. Reports model-answer word counts against the
marks-to-length bands, as WARN only -- the brief is explicit that completeness
and exam usability override word count.

Exit code 1 if any ERROR is raised. WARNs never fail the build.

Design rule, same as tools/notes/validate_spec.py: this validator knows nothing
about HTML. It validates content. Rendering correctness is audit_paper.py's job.
"""
import io, json, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TOP = [
    'schema_version', 'paper_id', 'sr_no', 'month', 'year', 'function', 'subject',
    'class', 'time_allowed', 'total_marks', 'instructions', 'source_copy_path',
    'source_copy_provenance', 'official_source_verified', 'transcription_verified',
    'build_state', 'review_state', 'version', 'created', 'updated', 'questions',
]

QUESTION = [
    'q_no', 'anchor', 'text_verbatim', 'subparts', 'total_marks', 'topic_tags',
    'recurrence', 'command_verbs', 'decomposition', 'reuse_tier', 'reuse_evidence',
    'reused_from', 'question_delta', 'answer_status', 'verification_status',
    'sources', 'unresolved', 'cross_links', 'model_answer', 'study_notes',
]

BUILD_STATES = ['Intake Complete', 'Dedup Assessed', 'Pilot In Progress',
                'Pilot Review Ready', 'Founder Approved', 'Complete']
ANSWER_STATES = ['Not Built', 'Drafting', 'Pilot Review Ready', 'Founder Approved', 'Built']
TIERS = ['A', 'B', 'C', 'D', None]

# Marks -> (min words, max words). From the build brief section 8.
BANDS = {4: (80, 120), 5: (110, 180), 6: (110, 180), 8: (180, 280),
         10: (240, 340), 16: (450, 650)}

# schema 1.1 -- the decomposition gate. Fields already carried elsewhere in the
# question object (command verbs, required components, internal reuse map) are
# deliberately NOT repeated here; see decomposition_gate.note.
GATE_KEYS = ['question_intent', 'mark_allocation', 'examiner_expectation',
             'primary_source_plan', 'freshness_risk', 'jurisdiction_risk',
             'technical_ambiguities', 'target_answer_shape']

PROV_CLASSES = ['P1_PRIMARY_VERIFIED', 'P2_AUTHORITATIVE_SECONDARY',
                'P3_INDUSTRY_GUIDANCE', 'INTERNAL_REUSE_VERIFIED',
                'ENGINEERING_JUDGEMENT', 'UNRESOLVED', 'TIME_SENSITIVE_REVERIFY']

RISK = ('LOW', 'MEDIUM', 'HIGH')

errs, warns = [], []
total_reverify = [0]


def err(m):
    errs.append(m)


def warn(m):
    warns.append(m)


BLOCK_KEYS = {'h', 'p', 'ul', 'ol', 'table'}


def check_blocks(blocks, label):
    """Every block must carry exactly one recognised content key.

    A block with two (e.g. both 'p' and 'ul', from an index-based patch that
    added rather than replaced) renders only the first branch the renderer
    tests -- silently dropping the other. That is a content-loss bug the page
    itself cannot reveal, so it is caught here.
    """
    for i, b in enumerate(blocks.get('blocks', [])):
        found = set(b) & BLOCK_KEYS
        if len(found) != 1:
            err('%s: block %d carries %s content key(s) %s -- exactly one required'
                % (label, i, len(found), sorted(found) or '(none)'))


def words(blocks):
    """Count words in a rendered-text sense: strip inline tags, join all text."""
    if not blocks:
        return 0
    buf = []
    for b in blocks.get('blocks', []):
        for k in ('h', 'p'):
            if k in b:
                buf.append(b[k])
        for k in ('ul', 'ol'):
            if k in b:
                buf.extend(b[k])
        # Table cells are content the candidate writes -- count them, or an
        # answer that carries its substance in a table measures as near-empty.
        if 'table' in b:
            buf.extend(b['table'].get('headers', []))
            for row in b['table'].get('rows', []):
                buf.extend(row)
    text = ' '.join(buf)
    text = re.sub(r'<[^>]+>', ' ', text)
    return len(text.split())


def main(path):
    raw = open(path, encoding='utf-8').read()
    try:
        d = json.loads(raw)
    except json.JSONDecodeError as e:
        lines = raw.splitlines()
        line = lines[e.lineno - 1] if e.lineno <= len(lines) else ''
        print('JSON ERROR: %s' % e)
        print('  line %d col %d' % (e.lineno, e.colno))
        print('  >> %s' % line[max(0, e.colno - 80):e.colno + 80])
        sys.exit(1)

    for k in TOP:
        if k not in d:
            err('missing top-level key: %s' % k)

    if d.get('build_state') not in BUILD_STATES:
        err('build_state %r not one of %s' % (d.get('build_state'), BUILD_STATES))

    # --- provenance honesty -------------------------------------------------
    prov = d.get('source_copy_provenance') or {}
    if not isinstance(prov, dict) or 'described_as' not in prov:
        err('source_copy_provenance must be an object carrying described_as')
    if d.get('official_source_verified') is not False and \
            not d.get('official_source_verification_note'):
        err('official_source_verified is not False and carries no verification note. '
            'Never claim official verification without recording how it was established.')
    src = d.get('source_copy_path')
    if src:
        full = os.path.join(os.path.dirname(os.path.abspath(path)), '..', '..', '..', src)
        if not os.path.exists(os.path.normpath(full)):
            warn('source_copy_path does not resolve on disk: %s' % src)

    tv = d.get('transcription_verified') or {}
    if tv.get('state') != 'verified':
        warn('transcription_verified.state is %r -- questions have not been '
             'visually checked against the source' % tv.get('state'))

    # --- questions ----------------------------------------------------------
    qs = d.get('questions', [])
    if len(qs) != 9:
        err('expected 9 questions, found %d' % len(qs))

    seen_no, seen_anchor = set(), set()
    for q in qs:
        qn = q.get('q_no', '?')
        for k in QUESTION:
            if k not in q:
                err('%s: missing key %s' % (qn, k))

        if qn in seen_no:
            err('duplicate q_no: %s' % qn)
        seen_no.add(qn)

        a = q.get('anchor')
        if a in seen_anchor:
            err('duplicate anchor: %s' % a)
        seen_anchor.add(a)
        if a != qn.lower():
            err('%s: anchor %r should be %r' % (qn, a, qn.lower()))

        if not (q.get('text_verbatim') or '').strip():
            err('%s: text_verbatim is empty' % qn)

        # marks arithmetic: subparts must sum to the question total when they
        # carry marks at all. Deliberately NOT checking that questions sum to
        # the paper total -- see marks_note in the spec.
        subs = q.get('subparts') or []
        marked = [s for s in subs if s.get('marks') is not None]
        if marked:
            tot = sum(s['marks'] for s in marked)
            if tot != q.get('total_marks'):
                err('%s: subpart marks sum to %s but total_marks is %s'
                    % (qn, tot, q.get('total_marks')))
        elif subs and not q.get('subpart_marks_note'):
            warn('%s: has unmarked subparts and no subpart_marks_note' % qn)

        if q.get('reuse_tier') not in TIERS:
            err('%s: reuse_tier %r not one of A/B/C/D/null' % (qn, q.get('reuse_tier')))
        if q.get('reuse_tier') == 'D' and not q.get('reused_from'):
            err('%s: tier D requires reused_from' % qn)
        if q.get('reuse_tier') == 'D' and not q.get('question_delta'):
            err('%s: tier D requires question_delta -- wholesale copying is not permitted' % qn)

        st = q.get('answer_status')
        if st not in ANSWER_STATES:
            err('%s: answer_status %r not one of %s' % (qn, st, ANSWER_STATES))

        built = st not in ('Not Built', 'Drafting')
        has_ans = bool(q.get('model_answer'))
        has_notes = bool(q.get('study_notes'))

        if built and not has_ans:
            err('%s: answer_status %r but no model_answer' % (qn, st))
        if built and not has_notes:
            err('%s: answer_status %r but no study_notes' % (qn, st))
        if has_ans and not built:
            err('%s: carries a model_answer but answer_status is %r' % (qn, st))
        if built and not q.get('verification_file'):
            err('%s: answer_status %r but no verification_file' % (qn, st))
        if built and q.get('verification_status') in (None, '', 'Not Started'):
            err('%s: answer_status %r but verification_status is %r'
                % (qn, st, q.get('verification_status')))
        if built and not q.get('sources'):
            err('%s: built answer carries no sources' % qn)

        # --- schema 1.1: decomposition gate must precede a built answer -----
        gate = q.get('decomposition_gate')
        if built and not gate:
            err('%s: built answer with no decomposition_gate. The gate must be '
                'completed BEFORE research and drafting.' % qn)
        if gate:
            for k in GATE_KEYS:
                if not gate.get(k):
                    err('%s: decomposition_gate missing or empty: %s' % (qn, k))
            if gate.get('freshness_risk') and \
                    gate['freshness_risk'].split()[0].upper().rstrip('-') not in RISK:
                warn('%s: freshness_risk should start LOW/MEDIUM/HIGH, got %r'
                     % (qn, gate['freshness_risk'][:30]))

        # --- schema 1.1: provenance -----------------------------------------
        prov = q.get('provenance_summary')
        if built and not prov:
            err('%s: built answer with no provenance_summary' % qn)
        if prov:
            bad_cls = [k for k in prov if k not in PROV_CLASSES]
            if bad_cls:
                err('%s: unknown provenance class(es): %s' % (qn, ', '.join(bad_cls)))
            if not prov.get('P1_PRIMARY_VERIFIED'):
                warn('%s: no claims recorded as P1_PRIMARY_VERIFIED' % qn)
            rv = q.get('reverify_before_publication')
            if rv is None:
                err('%s: missing reverify_before_publication (use [] if none)' % qn)
            else:
                for item in rv:
                    print('  [REVFY] %s: %s -- %s'
                          % (qn, item.get('claim', '?'), item.get('why', '')))
                total_reverify[0] += len(rv)

        vf = q.get('verification_file')
        if vf:
            full = os.path.normpath(os.path.join(
                os.path.dirname(os.path.abspath(path)), '..', vf))
            if not os.path.exists(full):
                err('%s: verification_file missing on disk: %s' % (qn, vf))

        # --- word count against the marks band (WARN only) ------------------
        if has_ans:
            check_blocks(q['model_answer'], '%s model_answer' % qn)
        if has_notes:
            check_blocks(q['study_notes'], '%s study_notes' % qn)

        if has_ans:
            n = words(q['model_answer'])
            # Band on TOTAL marks, not on the sum of subpart bands. Writing time
            # in the exam scales with what the question is worth, not with how
            # the examiner split it: a 16-mark question is 16 marks of writing
            # whether it is set as 16 or as 8+8. Summing two 8-mark bands gives
            # 360-560, which is both tighter than and inconsistent with the
            # brief's own 450-650 for 16 marks.
            lo, hi = BANDS.get(q.get('total_marks'), (0, 10 ** 6))
            band = '%s marks' % q.get('total_marks')
            if marked:
                band += ' (set as %s)' % '+'.join(str(s['marks']) for s in marked)
            flag = 'ok' if lo <= n <= hi else ('SHORT' if n < lo else 'LONG')
            line = '  [WORDS] %s model answer: %d words (%s band %d-%d) %s' \
                   % (qn, n, band, lo, hi, flag)
            print(line)
            if flag != 'ok':
                warn('%s: model answer %d words, outside the %d-%d band for %s '
                     '(completeness overrides -- review, do not auto-trim)'
                     % (qn, n, lo, hi, band))
            if has_notes:
                print('  [WORDS] %s study notes : %d words' % (qn, words(q['study_notes'])))

        for u in (q.get('unresolved') or []):
            print('  [OPEN ] %s: %s' % (qn, u))

    # --- report -------------------------------------------------------------
    print()
    for w in warns:
        print('  [WARN ] %s' % w)
    for e in errs:
        print('  [ERROR] %s' % e)
    print()
    print('%s: %d question(s), %d error(s), %d warning(s), %d claim(s) flagged '
          'for re-verification before publication'
          % (d.get('paper_id', '?'), len(qs), len(errs), len(warns), total_reverify[0]))
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
