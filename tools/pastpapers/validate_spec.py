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

# The publication register. Every re-verification flag must say what kind of
# obligation it creates, because "re-verify before publication" on its own does
# not tell a future session whether the paper can ship.
#
#   A  blocks publication until resolved
#   B  ships, but the fact is date-driven and must be re-checked immediately
#      before publication and before each new sitting
#   C  ships as-is: a known, accepted limit on the evidence (typically an
#      authoritative-secondary source where the primary is not held). Recording
#      it as C is NOT a promotion to primary -- it is a decision to publish with
#      the limitation stated in the answer.
#
# A flag that is no longer needed is DELETED, not downgraded to a fourth class.
REVERIFY_CLASSES = ('A_BLOCKING', 'B_CURRENCY_CHECK', 'C_ACCEPTED_LIMITATION')

errs, warns = [], []
total_reverify = [0]
blocking = [0]


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


# ---------------------------------------------------------------- template
# The canonical Written Answer template, derived from the nine QP2607 answers
# rather than invented. Every built question already satisfies it; enforcing it
# here is what stops the next eleven papers from each drifting a little.
#
# The spine is fixed so a student meets the same shape in every answer and a
# future extractor can rely on it. The question-specific analysis sections in
# between are deliberately NOT constrained -- that is where the thinking lives,
# and forcing irrelevant sections into every answer is exactly what the brief
# rules out.
STUDY_GUIDE_SPINE = (
    'Why this structure scores',
    'Common mistakes',
    'Examiner traps',
    'Likely oral follow-up',
    'Memory framework',
    'Regulation and source map',
)

# Every built answer also discloses what is uncertain, but the tail of the
# heading is question-specific ("Uncertainty and jurisdiction notes",
# "Uncertainty and currency", ...). Match the prefix, not the whole string:
# requiring one exact wording would force a dishonest heading onto a question
# whose uncertainty is of a different kind.
STUDY_GUIDE_PREFIXES = ('Uncertainty',)

# 'skeleton' is deliberately absent: the answer route lives in answer_route and
# nowhere else, so quick revision renders the route rather than storing a second
# copy of it. See docs/MIW_LEARNING_METHOD_DESIGN.md section 5.
QUICK_REVISION_FIELDS = ('recall_15s', 'keywords',
                         'critical_numbers', 'critical_regulation', 'major_trap')

# --- learning layer -------------------------------------------------------
ARCHETYPES = ('procedure', 'explain', 'compare', 'legal', 'evaluate')
CARD_TYPES = ('definition', 'distinction', 'procedure', 'regulation',
              'number', 'trap', 'structure')
ROUTE_MIN, ROUTE_MAX = 4, 9      # chunking; outside this range is a warning
CARDS_MIN = 4


def check_answer_route(q, qn):
    """The route is the one canonical sequence every other view derives from.

    The correspondence check below is the load-bearing one. If a route step and
    its model-answer heading can drift apart, the candidate is taught one order
    and shown another, and every derived view (map, recall blanks, exam plan,
    rapid revision) inherits the inconsistency.
    """
    r = q.get('answer_route')
    if not isinstance(r, dict) or not isinstance(r.get('steps'), list) or not r['steps']:
        err('%s: built answer with no answer_route. The route is required -- the '
            'map, recall test, exam plan and rapid revision are all derived from it.' % qn)
        return
    if r.get('archetype') not in ARCHETYPES:
        err('%s: answer_route.archetype %r not one of %s'
            % (qn, r.get('archetype'), list(ARCHETYPES)))

    steps = r['steps']
    if not (ROUTE_MIN <= len(steps) <= ROUTE_MAX):
        warn('%s: answer_route has %d steps, outside the %d-%d chunking range'
             % (qn, len(steps), ROUTE_MIN, ROUTE_MAX))

    for i, s in enumerate(steps, start=1):
        if s.get('n') != i:
            err('%s: answer_route step %d is numbered %r -- steps must run 1..N '
                'with no gaps, because the numbers are what the candidate memorises'
                % (qn, i, s.get('n')))
        if not (s.get('title') or '').strip():
            err('%s: answer_route step %d has no title' % (qn, i))
        if not (s.get('points') or []):
            err('%s: answer_route step %d has no core points' % (qn, i))

    # correspondence with the model answer
    heads = _headings(q.get('model_answer'))
    want = ['%d. %s' % (s['n'], s['title']) for s in steps]
    for w in want:
        if w not in heads:
            err('%s: answer_route step has no matching model-answer heading: %r. '
                'The principal headings of the model answer ARE the route.' % (qn, w))
    for h in heads:
        if h in want:
            continue
        if re.match(r'^\([a-z]\)', h):
            continue        # limb heading, mirrors the printed question
        err('%s: model answer has principal heading %r which is not a route step '
            'and is not a question limb. Every principal heading must be one or '
            'the other, or the answer and the route have drifted.' % (qn, h))


# Semantic-integrity guards.
#
# Structural consistency is not semantic consistency. A route point, a flashcard
# or a cheat-sheet line is a DERIVED representation, and the failure mode is that
# it flattens a conditional verified statement into a categorical one. The model
# answer said "carried as Group C ... but establish that from the declared BCSN
# and its current individual schedule"; three derived layers had reduced that to
# "pellets are Group C", which is the exact error earlier red-teaming rejected.
#
# These are deliberately narrow, known-issue guards. There is no general truth
# validator here and there should not be: subjective educational quality stays a
# human review. Each entry is (name, pattern, hedge words, where to look).
SEMANTIC_GUARDS = [
    (
        'unconditional IMSBC group',
        # "X is/are Group A" with no reference to the schedule or declaration
        re.compile(r'\b(?:is|are|=)\s*Group\s*[ABC]\b', re.I),
        ('schedule', 'declar', 'bcsn'),
        'IMSBC classification and carriage requirements follow the declared BCSN '
        'and its current individual schedule, not the commodity name used in the '
        'question. State the group only alongside that qualification.',
    ),
]


def _derived_texts(q):
    """Every place a verified statement gets re-expressed for learning.

    The model answer and study guide are the SOURCE and are excluded: they are
    allowed to carry the full conditional sentence. These are the short forms.
    """
    out = []
    for s in (q.get('answer_route') or {}).get('steps') or []:
        out.append(('route step %s title' % s.get('n'), s.get('title', '')))
        for p in s.get('points') or []:
            out.append(('route step %s core point' % s.get('n'), p))
    qr = q.get('quick_revision') or {}
    for k in ('recall_15s', 'major_trap', 'critical_regulation'):
        out.append(('quick_revision.%s' % k, qr.get(k) or ''))
    for n in qr.get('critical_numbers') or []:
        out.append(('quick_revision.critical_numbers', n))
    for c in q.get('retrieval_cards') or []:
        out.append(('card %s prompt' % c.get('id'), c.get('prompt') or ''))
        out.append(('card %s answer' % c.get('id'), c.get('answer') or ''))
    if q.get('memory_cue'):
        out.append(('memory_cue', q['memory_cue']))
    return out


# --- MIW True Source reference contract -----------------------------------
# A question points at a CORPUS OBJECT. It never points at a document, an
# edition, a bookmark or a page. The corpus resolver owns all of that, so the
# question survives PDF regeneration, re-pagination, consolidated amendments and
# replacement editions without being touched. See docs/MIW_TRUE_SOURCE_CONTRACT.md.
#
# object_id follows the node-id convention ALREADY established in the MIW
# reference repository (RulesApp/repository/index/repo-data.json): an instrument
# token followed by hyphen-separated structural tokens, e.g. SOLAS-II2-10,
# MARPOL-VI-14, FSSCode-9-2, BunkerConvention2001-Articles-7.
REF_RELATIONSHIPS = ('PRIMARY_RULE', 'SUPPORTING_RULE', 'DEFINITION', 'PROCEDURE',
                     'LEGAL_BASIS', 'NUMERIC_SOURCE', 'CONTEXT')
REF_STATES = ('REFERENCE_AVAILABLE', 'REFERENCE_PENDING', 'NO_CORPUS_OBJECT_YET')
REF_ID_RE = re.compile(r'^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+$')

# Frozen architectural rule. Enforced from the outset, before any reference
# exists, because the cheap moment to forbid page coupling is before the first
# one is written.
PDF_PAGE_RE = re.compile(r'\.pdf\s*#\s*page\s*=|pdf-page-\d|#page=\d|\bpage\s*=\s*\d{1,4}\b', re.I)


def check_primary_category(q, qn):
    """Exactly one primary category, from the topic tree.

    Imported from build_index so there is a single list of categories. A second
    hand-maintained copy here would drift, and the first symptom would be a
    question quietly vanishing from the topic page.
    """
    try:
        from build_index import TOPIC_TREE
    except Exception as e:                       # pragma: no cover
        warn('%s: could not import TOPIC_TREE to validate primary_category (%s)' % (qn, e))
        return
    cats = [c for c, _ in TOPIC_TREE]
    pc = q.get('primary_category')
    if pc not in cats:
        err('%s: primary_category %r is not one of the topic-tree categories %s. '
            'The topic page renders each question once, under this category.'
            % (qn, pc, cats))


def check_reference_shelf(q, qn):
    """OPTIONAL. A question with no shelf is valid: answers and corpus objects
    are produced on parallel tracks, and a missing object must never block a
    paper build or force a fabricated reference."""
    shelf = q.get('reference_shelf')
    if shelf is None:
        return
    if not isinstance(shelf, list):
        err('%s: reference_shelf must be a list' % qn)
        return
    seen = set()
    for i, r in enumerate(shelf):
        oid = (r.get('object_id') or '').strip()
        if not oid:
            err('%s reference_shelf[%d]: no object_id' % (qn, i))
            continue
        if not REF_ID_RE.match(oid):
            err('%s reference_shelf[%d]: object_id %r is not a corpus node id. '
                'Expected the established convention, e.g. MARPOL-VI-14.' % (qn, i, oid))
        if oid in seen:
            err('%s reference_shelf[%d]: duplicate object_id %r' % (qn, i, oid))
        seen.add(oid)
        if r.get('relationship') not in REF_RELATIONSHIPS:
            err('%s reference_shelf[%d]: relationship %r not one of %s'
                % (qn, i, r.get('relationship'), list(REF_RELATIONSHIPS)))
        if r.get('state') not in REF_STATES:
            err('%s reference_shelf[%d]: state %r not one of %s'
                % (qn, i, r.get('state'), list(REF_STATES)))
        if not (r.get('label') or '').strip():
            err('%s reference_shelf[%d]: no label' % (qn, i))


def check_no_pdf_coupling(d, path):
    """No part of a question spec may bind a claim to a PDF page.

    Page numbers move. The corpus may record them in its own provenance; the
    question must not, or every re-pagination silently invalidates the product.
    """
    blob = json.dumps(d, ensure_ascii=False)
    for m in PDF_PAGE_RE.finditer(blob):
        err('%s: a PDF page reference appears in the spec (%r). Questions must '
            'reference corpus OBJECT ids, never documents or pages.'
            % (os.path.basename(path), blob[max(0, m.start() - 50):m.end() + 30]))


def check_semantic_integrity(q, qn):
    for name, rx, hedges, why in SEMANTIC_GUARDS:
        for where, text in _derived_texts(q):
            plain = re.sub(r'<[^>]+>', '', str(text))
            m = rx.search(plain)
            if not m:
                continue
            if any(h in plain.lower() for h in hedges):
                continue
            err('%s %s: %s -- %r. %s'
                % (qn, where, name, plain[max(0, m.start() - 40):m.end() + 40], why))


def check_memory_cue(q, qn):
    """A cue may support the canonical route. It must not become a second route.

    If a cue enumerates its own anchors, the candidate ends up holding two
    sequences of different lengths and has to reconcile them under exam
    pressure -- which is the opposite of the point.
    """
    cue = q.get('memory_cue')
    if not cue:
        return
    steps = (q.get('answer_route') or {}).get('steps') or []
    anchors = re.findall(r'\b[A-Z]{3,}(?:\s+[A-Z]{3,})*\b', re.sub(r'<[^>]+>', '', cue))
    anchors = [a for a in anchors if a not in ('MIW', 'IMO', 'BCSN', 'TML', 'ISM')]
    if len(anchors) < 2:
        return              # prose cue, nothing to reconcile
    if not re.search(r'\(\d', cue):
        err('%s memory_cue enumerates %d anchor(s) but maps none of them to a route '
            'step number. A cue must point AT the canonical route, not create a '
            'second sequence. Add step numbers, or drop the cue.'
            % (qn, len(anchors)))


def check_retrieval_cards(q, qn):
    cards = q.get('retrieval_cards')
    if not isinstance(cards, list) or len(cards) < CARDS_MIN:
        err('%s: needs at least %d retrieval_cards (has %s)'
            % (qn, CARDS_MIN, len(cards) if isinstance(cards, list) else 'none'))
        return
    seen_id, seen_prompt = set(), set()
    for c in cards:
        cid = c.get('id')
        if not cid or not cid.startswith(q['question_id'] + '-C'):
            err('%s: card id %r must start with %s-C so a future scheduling layer '
                'can attach to a stable key' % (qn, cid, q['question_id']))
        if cid in seen_id:
            err('%s: duplicate card id %r' % (qn, cid))
        seen_id.add(cid)
        if c.get('type') not in CARD_TYPES:
            err('%s: card %s type %r not one of %s' % (qn, cid, c.get('type'), list(CARD_TYPES)))
        p, a = (c.get('prompt') or '').strip(), (c.get('answer') or '').strip()
        if not p or not a:
            err('%s: card %s has an empty prompt or answer' % (qn, cid))
            continue
        key = p.lower()
        if key in seen_prompt:
            err('%s: duplicate card prompt %r' % (qn, p[:50]))
        seen_prompt.add(key)
        if len(a.split()) > 90:
            warn('%s: card %s answer is %d words -- a flashcard answer that long '
                 'is being read, not retrieved' % (qn, cid, len(a.split())))


def _headings(blocks):
    """Heading text with inline markup removed, so <b>/<i> cannot defeat a match."""
    return [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', b['h'])).strip()
            for b in (blocks or {}).get('blocks', []) if 'h' in b]


def check_study_guide_spine(q, qn):
    hs = _headings(q.get('study_notes'))
    for want in STUDY_GUIDE_SPINE:
        if want not in hs:
            err('%s study_notes: missing required section %r. The canonical '
                'template is: %s (plus question-specific sections).'
                % (qn, want, ', '.join(STUDY_GUIDE_SPINE)))
    for pre in STUDY_GUIDE_PREFIXES:
        if not any(h.startswith(pre) for h in hs):
            err('%s study_notes: no %r section. Every built answer must state '
                'what is uncertain; the heading tail may be question-specific.'
                % (qn, pre))


def check_quick_revision(q, qn):
    """Quick Revision is generated from the question object, never hand-kept.

    It is also the source of the Exam Approach block and of the paper-level
    Rapid Revision table, so a missing field silently empties two other
    surfaces rather than just this one.
    """
    qr = q.get('quick_revision')
    if not isinstance(qr, dict):
        err('%s: built answer with no quick_revision object' % qn)
        return
    for f in QUICK_REVISION_FIELDS:
        if not qr.get(f):
            err('%s quick_revision: missing or empty %r (required: %s)'
                % (qn, f, ', '.join(QUICK_REVISION_FIELDS)))
    if isinstance(qr.get('skeleton'), list) and len(qr['skeleton']) < 3:
        err('%s quick_revision.skeleton has %d step(s). An answer skeleton with '
            'fewer than 3 is not a usable exam-writing map.'
            % (qn, len(qr['skeleton'])))


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

    check_no_pdf_coupling(d, path)

    for k in TOP:
        if k not in d:
            err('missing top-level key: %s' % k)

    if d.get('build_state') not in BUILD_STATES:
        err('build_state %r not one of %s' % (d.get('build_state'), BUILD_STATES))

    # --- provenance honesty -------------------------------------------------
    # Source-copy classification is NEUTRAL: it records what kind of copy this
    # is, never who hosted it. This repository is public, so a host's name in a
    # spec is a public brand trace. The host identity is kept in a local-only
    # file. Note that this is a separate axis from official_source_verified --
    # deleting a brand name must never promote a scan to an official source.
    SOURCE_COPY_TYPES = ('third_party_scan', 'official_publication', 'candidate_transcript')
    SOURCE_AUTHORITIES = ('unverified', 'verified_official')
    prov = d.get('source_copy_provenance') or {}
    if not isinstance(prov, dict) or 'described_as' not in prov:
        err('source_copy_provenance must be an object carrying described_as')
    else:
        if prov.get('source_copy_type') not in SOURCE_COPY_TYPES:
            err('source_copy_provenance.source_copy_type %r not one of %s'
                % (prov.get('source_copy_type'), list(SOURCE_COPY_TYPES)))
        if prov.get('source_authority') not in SOURCE_AUTHORITIES:
            err('source_copy_provenance.source_authority %r not one of %s'
                % (prov.get('source_authority'), list(SOURCE_AUTHORITIES)))
        if 'host_branding' in prov:
            err('source_copy_provenance carries host_branding. Third-party host '
                'identity must not live in this public repository; record it in '
                'verification/LOCAL_SOURCE_PROVENANCE.md and use source_copy_type.')
        if prov.get('source_authority') == 'verified_official' and \
                d.get('official_source_verified') is not True:
            err('source_authority is verified_official but official_source_verified '
                'is not True. These two must agree.')
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
                    cls = item.get('class')
                    if cls not in REVERIFY_CLASSES:
                        err('%s: reverify class %r not one of %s. Every flag must '
                            'say whether it blocks publication (A), needs a currency '
                            'check first (B), or is an accepted limitation (C).'
                            % (qn, cls, list(REVERIFY_CLASSES)))
                    if not item.get('claim') or not item.get('why'):
                        err('%s: reverify entry needs both claim and why' % qn)
                    print('  [REVFY] %s [%s]: %s -- %s'
                          % (qn, cls, item.get('claim', '?'), item.get('why', '')))
                    if cls == 'A_BLOCKING':
                        blocking[0] += 1
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
            check_study_guide_spine(q, qn)
        if has_ans:
            check_quick_revision(q, qn)
            check_answer_route(q, qn)
            check_retrieval_cards(q, qn)
            check_semantic_integrity(q, qn)
            check_memory_cue(q, qn)
            check_primary_category(q, qn)
        check_reference_shelf(q, qn)

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
          'for re-verification before publication (%d blocking)'
          % (d.get('paper_id', '?'), len(qs), len(errs), len(warns),
             total_reverify[0], blocking[0]))
    if blocking[0]:
        print('  PUBLICATION BLOCKED: %d class A flag(s) outstanding.' % blocking[0])
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
