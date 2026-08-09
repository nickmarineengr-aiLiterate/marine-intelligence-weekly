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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    args = ap.parse_args()

    specs = [json.load(io.open(p, encoding='utf-8'))
             for p in sorted(glob.glob(os.path.join(PP, 'specs', '*.json')))]

    fails = schema_layer(specs) + leak_layer() + normalise_layer()

    nodes = RM.load_nodes(specs)
    rel = RM.build_families(nodes)
    fam = {r['family_id'] for r in rel.values()}

    print('RECURRENCE PROVENANCE BOUNDARY')
    print('  %d spec(s), %d question(s), %d canonical famil(ies)'
          % (len(specs), len(nodes), len(fam)))
    print('  swept %d generated artefact(s) for host sitting tokens'
          % len(candidate_facing()))
    print('  %d deterministic normalisation case(s)' % len(NORM_CASES))

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
        for b in bad:
            print('  [SELFTEST FAIL] %s' % b)
        print('  self-test: %s' % ('FAILED' if bad else 'every guard fired when broken'))
        fails += bad

    print()
    for f in fails:
        print('  [FAIL ] %s' % f)
    print('recurrence boundary: %d failure(s)' % len(fails))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
