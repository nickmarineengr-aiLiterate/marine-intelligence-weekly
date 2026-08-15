#!/usr/bin/env python3
"""Enforce the recurrence provenance boundary.

Usage:
  python recurrence_check.py [--self-test]

There are three recurrence signals in this product and only ONE of them may
ever reach a candidate. This module is where that line is enforced, because the
line was crossed silently once already: the source copy host's printed
annotation was being rendered on every solved paper page, folded into the
`data-search` attribute of every question card, and published in the public
content manifest.

    CANONICAL          recurrence_model.py, computed from (year, month) over
                       MIW's own transcriptions. The only signal that may be
                       rendered, searched, badged or published.

    DISCOVERY ONLY     `host_recurrence_hint` -- the third-party host's printed
                       "previously asked" table. Useful for proposing candidate
                       relationships to a human, worthless as evidence: the 2026
                       set proved it over-claims and under-claims in both
                       directions, and its bare-month tokens (2019/OCT) link
                       wholly unrelated questions. Never rendered.

    AUTHORING ONLY     `recurrence_class` -- what was true of the MIW corpus at
                       the moment the question was built. Production order is not
                       sitting order, so for three questions in the 2026 set this
                       field states the OPPOSITE of the chronological truth.
                       Never rendered.

Layers:

  1. SCHEMA     no spec may carry the retired `recurrence` / `prior_sittings`
                keys, and every question must carry `host_recurrence_hint`.
  2. LEAK       no generated candidate-facing artefact may contain a host
                sitting token (2018/APR, 2025/SEP/Q6, 2011/SR4) or an authoring
                recurrence_class value.
  3. NORMALISE  deterministic cases for the marks-safe stem normalisation, which
                decides EXACT versus NEAR for every pair in the corpus.

--self-test positive-controls every layer: a guard that cannot fail is not a
guard. Exit 1 on any failure.
"""
import argparse, glob, io, json, os, re, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import REPO_ROOT                              # noqa: E402
import recurrence_model as RM                                    # noqa: E402

PP = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')

# A host sitting token as the source copies print them:
#   2018/APR   2025/SEP/Q6   2022/MAR/1   2011/SR4   2021/JULY(M)/Q7   2016/JAN2
HOST_TOKEN = re.compile(r'\b(?:19|20)\d{2}/(?:[A-Z]{3,5}\d?(?:\(M\))?|SR\d{1,2})\b')

# The authoring vocabulary. Rendering any of these to a candidate states
# production order as though it were sitting order.
AUTHORING_CLASSES = ('topic_recurrence', 'near_recurrence', 'exact_recurrence')

# `recurrence_note` held two different things under one name: boilerplate on the
# intake specs, and, on 62 questions, a real hand-written adjudication of two
# printed stems. The name is retired because it did not distinguish them; the
# reasoning survives under `recurrence_adjudication`, which says whose reading it
# is. Neither is rendered.
RETIRED_KEYS = ('recurrence', 'prior_sittings', 'recurrence_note')


def candidate_facing():
    """Every generated artefact a candidate can fetch.

    Specs are NOT in this list: the hint is allowed to live in the spec, which
    is the whole point of keeping a provenance field. What must never happen is
    the hint reaching a page, an attribute, or the manifest.
    """
    out = sorted(glob.glob(os.path.join(PP, '*.html')))
    out.append(os.path.join(PP, 'pastpapers_content_index.json'))
    out += sorted(glob.glob(os.path.join(PP, 'sample', '*.html')))
    return [p for p in out if os.path.exists(p)]


def schema_layer(specs):
    fails = []
    for d in specs:
        pid = d['paper_id']
        for q in d['questions']:
            for k in RETIRED_KEYS:
                if k in q:
                    fails.append(
                        '%s %s: carries retired key %r. The host annotation lives in '
                        '`host_recurrence_hint` and nowhere else; `prior_sittings` was a COUNT '
                        'of host claims presented as MIW truth and is gone.' % (pid, q['q_no'], k))
            if 'host_recurrence_hint' not in q:
                fails.append('%s %s: no host_recurrence_hint (use [] when the source copy '
                             'prints no annotation)' % (pid, q['q_no']))
    return fails


def leak_layer(extra=None):
    """No host token and no authoring class in anything we ship."""
    fails = []
    files = [(os.path.relpath(p, REPO_ROOT).replace('\\', '/'),
              io.open(p, encoding='utf-8', errors='replace').read())
             for p in candidate_facing()]
    if extra is not None:
        files.append(('<injected>', extra))
    for name, body in files:
        m = HOST_TOKEN.search(body)
        if m:
            i = m.start()
            fails.append('THIRD-PARTY RECURRENCE LEAK: %s carries host sitting token %r '
                         '(context: %r). Host claims are provenance, never canonical '
                         'recurrence.' % (name, m.group(0), body[max(0, i - 60):i + 20]))
        for cls in AUTHORING_CLASSES:
            if cls in body:
                fails.append('AUTHORING RECURRENCE LEAK: %s carries %r. recurrence_class is '
                             'recorded in production order and is not chronology.' % (name, cls))
    return fails


# --------------------------------------------------------------- normalisation
# Case A  same wording, one prints its marks and one does not  -> equal
# Case B  a number that is part of the examiner's demand       -> preserved
# Case C  different demand that happens to share a marks token -> still unequal
NORM_CASES = [
    ('A: printed total present vs absent',
     ('Explain the concept of CII rating and its metrics. (16)', 16, []),
     ('Explain the concept of CII rating and its metrics.', 16, []),
     True),
    ('A: differing limb split, identical wording',
     ('a) Objectives of the code. (6) b) Key performance indicators. (4) '
      'c) Flag, coastal and port state responsibilities. (6)', 16,
      [{'marks': 6}, {'marks': 4}, {'marks': 6}]),
     ('a) Objectives of the code. (6) b) Key performance indicators. (5) '
      'c) Flag, coastal and port state responsibilities. (5)', 16,
      [{'marks': 6}, {'marks': 5}, {'marks': 5}]),
     True),
    # The load-bearing case. Two questions about DIFFERENT resolutions of the
    # same instrument differ by nothing except the parenthesised session number.
    # An over-broad normaliser that strips every numeric parenthetical merges
    # them, and the corpus really does set MEPC.312(74) and MEPC.203(62).
    ('B: resolution session number attached to its instrument survives',
     ('Guidelines are laid down in resolution MEPC.312(74), elaborate. (16)', 16, []),
     ('Guidelines are laid down in resolution MEPC.312(62), elaborate. (16)', 16, []),
     False),
    ('B: a declared-marks value inside the demand, but attached',
     ('Explain Phase 2 (of 20% - 30% reduction) under EEXI. (16)', 16, []),
     ('Explain Phase 2 (of 20% - 40% reduction) under EEXI. (16)', 16, []),
     False),
    ('B: bracketed limb enumerators are not marks and are not declared',
     ('Explain (i) accession and (ii) ratification. (16)', 16, []),
     ('Explain (i) accession and (ii) approval. (16)', 16, []),
     False),
    ('C: different demand, same marks token',
     ('Discuss the scope of Indian Admiralty Law. (16)', 16, []),
     ('Discuss the CII rating of a bulk carrier. (16)', 16, []),
     False),
]


def normalise_layer(mutate=None):
    """mutate=='strip_all' installs a deliberately over-broad normaliser, which
    must break case B. That is the positive control."""
    fails = []
    fn = RM.normalise_stem
    if mutate == 'strip_all':
        def fn(text, marks=None, subparts=None):
            return RM.normalise_stem(re.sub(r'\(\d+\)', ' ', text or ''), marks, subparts)
    for label, a, b, want_equal in NORM_CASES:
        got = fn(*a) == fn(*b)
        if got != want_equal:
            fails.append('normalisation case %r: expected %s, got %s'
                         % (label, 'EQUAL' if want_equal else 'DIFFERENT',
                            'EQUAL' if got else 'DIFFERENT'))
    return fails


# ---------------------------------------------------------------------------
# Layer 4: HOLDINGS. A denial that the governed record can disprove.
#
# Three consecutive reviews (QP2308, QP2306, QP2311) shipped an adjudication
# saying MIW could not check a sitting the host pointed at, when MIW held that
# sitting all along in the six-year historical intelligence layer. On QP2311 the
# denied sitting turned out to carry the SAME QUESTION WORD FOR WORD.
#
# This layer fires only on an EXACT, MACHINE-PROVABLE contradiction and is kept
# deliberately narrow, because a guard that guesses is worse than no guard:
#
#   * only `recurrence_adjudication` is read. That field exists to adjudicate the
#     host's printed pointer, so a denial in it is unambiguously about a SITTING.
#     Denials elsewhere are usually about an INSTRUMENT the True Source corpus
#     does not hold ("the corpus does not hold the unified requirements"), which
#     is a different and usually true claim;
#   * only tokens carrying a resolvable month are considered. Bare `SR` tokens
#     (2011/SR02) and out-of-window years resolve to nothing and are ignored --
#     a denial about those is correct and must stay silent;
#   * a token resolving to the question's OWN paper is ignored. Every source copy
#     prints a self-referential pointer.
#
# Where a BLANKET denial points at several sittings and only some are held, the
# guard still fires. That is intended: a blanket denial is unsafe once any
# pointed-at sitting is held, and the fix is to make the sentence specific.
#
# SENTENCE SCOPING. A denial that has ALREADY been made specific is read on its
# own terms: if the sentence carrying the denial names sitting tokens itself,
# the denial is adjudicated against THOSE tokens and not against every token on
# the question. This is what "make the sentence specific" was asking for, so
# the guard has to recognise the fix when it sees it -- otherwise a question
# that correctly says "2017/FEB and 2017/DEC are sittings MIW does not hold"
# would flag forever merely because a DIFFERENT, correctly-described token on
# the same question is held. A denial naming no token is still blanket and is
# still checked against everything. The rule is purely positional -- which
# tokens appear inside the sentence -- and involves no reading of meaning.
#
# THIS LAYER DETECTS; IT DOES NOT GATE -- and that is a deliberate choice, not a
# softened guard. Run for the first time it reported 22 hits across six already
# published papers. Making it blocking would have forced one of two bad moves:
# rewriting six papers inside a one-paper review, or loosening the rule until the
# corpus passed. Both are forbidden. What the layer can prove on its own is that
# a denial COLLIDES with the holdings record; whether the sentence is wrong needs
# the two printed stems read side by side, which is Claude's job and not a
# checker's. So it follows the Production Intelligence Layer contract already
# used by temporal_sweep and surface_impact: IT FLAGS; CLAUDE ADJUDICATES.
MONTHS = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUNE': 6,
          'JUL': 7, 'JULY': 7, 'AUG': 8, 'SEP': 9, 'SEPT': 9, 'OCT': 10,
          'NOV': 11, 'DEC': 12}

# Closed list. Each says "MIW cannot check this", which the holdings record can
# contradict outright. Phrases asserting novelty ("no donor", "first set here")
# are deliberately NOT here -- they are claims about the SOLVED set and can be
# true while the sitting is held.
DENIALS = ('does not hold', 'do not hold', 'not held', 'cannot read',
           'cannot be read', 'never transcribed', 'no paper for that sitting',
           'holds no paper', 'cannot be checked', 'does not have')

TOKEN_MONTH = re.compile(r'\b((?:19|20)\d{2})/([A-Z]{3,5})(?:\(M\))?(?:/\S+)?')


def held_papers(specs, intel_path=None):
    """Every paper id MIW can read a printed stem for: solved specs plus the
    six-year historical intelligence store."""
    ids = {d['paper_id'] for d in specs}
    p = intel_path or os.path.join(PP, 'intelligence', 'historical_qp_intelligence.json')
    if os.path.exists(p):
        ids |= {q['paper_id'] for q in json.load(io.open(p, encoding='utf-8'))['papers']}
    return ids


def resolve_token(tok):
    """'2022/SEP/Q5' -> 'QP2209'. Returns None when the token carries no month
    this project can resolve, which is the common case for bare SR tokens."""
    m = TOKEN_MONTH.match(tok)
    if not m:
        return None
    mon = MONTHS.get(m.group(2).upper())
    return None if mon is None else 'QP%s%02d' % (m.group(1)[2:], mon)


SENTENCE = re.compile(r'(?<=[.;:])\s+')


def denial_scopes(adj, hints):
    """Every (denial phrase, tokens it is made about) pair in an adjudication.

    A denial sentence that names sitting tokens is scoped to those tokens; one
    that names none is blanket and is scoped to every hint on the question.
    """
    scopes = []
    for sentence in SENTENCE.split(adj):
        hit = [w for w in DENIALS if w in sentence.lower()]
        if not hit:
            continue
        named = [m.group(0).rstrip('.,;:') for m in TOKEN_MONTH.finditer(sentence)]
        scopes.append((hit[0], named or list(hints)))
    return scopes


def holdings_layer(specs, intel_path=None):
    fails = []
    held = held_papers(specs, intel_path)
    for d in specs:
        for q in d.get('questions', []):
            adj = q.get('recurrence_adjudication') or ''
            hints = q.get('host_recurrence_hint') or []
            for phrase, toks in denial_scopes(adj, hints):
                for tok in toks:
                    pid = resolve_token(tok)
                    if not pid or pid == d['paper_id'] or pid not in held:
                        continue
                    fails.append(
                        'FALSE HOLDINGS DENIAL: %s-%s says %r in recurrence_adjudication, '
                        'but its host pointer %r resolves to %s, which MIW HOLDS and can '
                        'read. Adjudicate the pointer against the stem instead of denying '
                        'it.' % (d['paper_id'], q['q_no'], phrase, tok, pid))
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()

    specs = [json.load(io.open(p, encoding='utf-8'))
             for p in sorted(glob.glob(os.path.join(PP, 'specs', '*.json')))]

    fails = schema_layer(specs) + leak_layer() + normalise_layer()
    holdings = holdings_layer(specs)

    nodes = RM.load_nodes(specs)
    rel = RM.build_families(nodes)
    fam = {r['family_id'] for r in rel.values()}

    print('RECURRENCE PROVENANCE BOUNDARY')
    print('  %d spec(s), %d question(s), %d canonical famil(ies)'
          % (len(specs), len(nodes), len(fam)))
    print('  swept %d generated artefact(s) for host sitting tokens'
          % len(candidate_facing()))
    print('  %d deterministic normalisation case(s)' % len(NORM_CASES))
    print('  %d paper(s) readable for a holdings denial check' % len(held_papers(specs)))

    if args.self_test:
        bad = []
        if not leak_layer(extra='<div class="rec-note">Recurrence recorded on the source '
                                'paper: 2018/APR, 2025/SEP/Q6.</div>'):
            bad.append('leak guard did NOT fire on an injected host recurrence block')
        if not leak_layer(extra='<span class="q-meta">exact_recurrence</span>'):
            bad.append('leak guard did NOT fire on an injected authoring recurrence_class')
        import copy
        s2 = copy.deepcopy(specs)
        if s2:
            s2[0]['questions'][0]['prior_sittings'] = 3
            if not any('prior_sittings' in f for f in schema_layer(s2)):
                bad.append('schema guard did NOT fire on a reinstated prior_sittings key')
        if not normalise_layer(mutate='strip_all'):
            bad.append('normalisation guard did NOT fire against an over-broad normaliser '
                       'that strips every numeric parenthetical')

        # Holdings layer. Two controls, because this guard has to stay SILENT on
        # a correct denial as reliably as it fires on a false one -- a guard that
        # fires on everything would push authors to delete true sentences.
        # Both controls are scoped to the probe itself. Asserting on the whole
        # run would silently inherit the corpus's own 22 open hits and the
        # negative control could never pass.
        probe = {'paper_id': 'QP9901', 'questions': [{
            'q_no': 'Q1', 'host_recurrence_hint': ['2022/SEP/Q5'],
            'recurrence_adjudication': 'A September 2022 sitting MIW does not hold.'}]}
        if not [f for f in holdings_layer([probe]) if 'QP9901' in f]:
            bad.append('holdings guard did NOT fire on a denial of a sitting MIW holds')
        # Unresolvable SR token, an out-of-window sitting, and a self-referential
        # pointer -- all three must be ignored.
        quiet = {'paper_id': 'QP2311', 'questions': [{
            'q_no': 'Q1', 'host_recurrence_hint': ['2011/SR02', '1998/APR', '2023/NOV/Q1'],
            'recurrence_adjudication': 'Tokens pointing at sittings MIW does not hold.'}]}
        if holdings_layer([quiet]):
            bad.append('holdings guard FIRED on a correct denial -- it must stay silent '
                       'on unresolvable tokens and on out-of-window sittings')

        # Sentence scoping. The rule only earns its place if it still fires when
        # the NAMED token is the held one, so both directions are controlled.
        scoped_bad = {'paper_id': 'QP9902', 'questions': [{
            'q_no': 'Q1', 'host_recurrence_hint': ['1998/APR', '2022/SEP/Q5'],
            'recurrence_adjudication':
                'The host points at 2022/SEP/Q5, a sitting MIW does not hold. '
                'Nothing else is claimed.'}]}
        if not [f for f in holdings_layer([scoped_bad]) if 'QP9902' in f]:
            bad.append('holdings guard did NOT fire on a denial that NAMES a sitting '
                       'MIW holds -- sentence scoping must not excuse a specific '
                       'denial, only a correctly-specific one')
        scoped_ok = {'paper_id': 'QP9903', 'questions': [{
            'q_no': 'Q1', 'host_recurrence_hint': ['1998/APR', '2022/SEP/Q5'],
            'recurrence_adjudication':
                '1998/APR is a sitting MIW does not hold. 2022/SEP/Q5 resolves to '
                'QP2209, which MIW holds and which was read.'}]}
        if holdings_layer([scoped_ok]):
            bad.append('holdings guard FIRED on a denial scoped to the one token it '
                       'actually denies, while a DIFFERENT token on the same question '
                       'is held and correctly described as held')
        for b in bad:
            print('  [SELFTEST FAIL] %s' % b)
        print('  self-test: %s' % ('FAILED' if bad else 'every guard fired when broken'))
        fails += bad

    print()
    for h in holdings:
        print('  [HOLD ] %s' % h)
    if holdings:
        print('  holdings denials colliding with the record: %d -- REPORT, not a gate. '
              'Read the two printed stems and adjudicate each.' % len(holdings))
    for f in fails:
        print('  [FAIL ] %s' % f)
    print('recurrence boundary: %d failure(s)' % len(fails))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
