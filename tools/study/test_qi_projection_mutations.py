#!/usr/bin/env python3
"""Mutation tests for the candidate-safe QI projection gate.

    python tools/study/test_qi_projection_mutations.py

A gate that has never rejected anything has not been shown to work. Each
mutation below is a specific, plausible way this projection could ship a claim
the evidence does not support, and the gate must catch every one.

WHY THESE MUTATIONS TOUCH DISK
------------------------------
Half of what this gate asserts is about RENDERED BYTES, not about the
projection artefact -- a page that says more than the model does is precisely
the failure mode, and an in-memory mutation of the model cannot reach it. So
the suite writes, and it therefore has to prove it put everything back.

Every file a mutation touches is snapshotted BYTE-FOR-BYTE before the write and
restored in a finally clause, and the whole watched set is fingerprinted before
the first mutation and after the last. Restoration is from the in-memory
snapshot, never from git: a `git checkout -- <path>` here would discard any
uncommitted work in the tree, which has already destroyed edits in this
repository once.
"""

import hashlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import qi_projection as QIP
import validate_qi_projection as V

PROJ = QIP.OUT
YEAR26 = os.path.join(ROOT, 'solvedQP', 'questions-2026.html')
PAPER = os.path.join(ROOT, 'solvedQP', 'QP2608.html')
TOPICS = os.path.join(ROOT, 'meoclass1', 'topics.html')
PUBLIC = os.path.join(ROOT, 'SQ', 'study-roadmap.html')

#: Every artefact that must be byte-identical when the suite finishes.
WATCHED = [PROJ, YEAR26, PAPER, TOPICS, PUBLIC,
           os.path.join(ROOT, 'docs', 'study', 'study_qi.json'),
           os.path.join(ROOT, 'docs', 'study', 'qi', 'qi_families.json'),
           os.path.join(ROOT, 'docs', 'study', 'qi', 'qi_occurrences.json'),
           os.path.join(HERE, 'qi_phase2_adjudications.json')]


def _read(p):
    return io.open(p, encoding='utf-8', newline='').read()


def _write(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


def _fingerprint():
    h = {}
    for p in WATCHED:
        h[p] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    return h


def _patch_json(path, fn):
    """Load, mutate through fn, write back. Returns the original bytes."""
    orig = _read(path)
    doc = json.loads(orig)
    fn(doc)
    _write(path, json.dumps(doc, indent=1, ensure_ascii=False) + '\n')
    return orig


# --------------------------------------------------------------------------
# MUTATIONS. Each yields (description, expected_rule, undo_callable).
# --------------------------------------------------------------------------

def mut_1_label_an_unmapped_question():
    """Give an August question with no governed family a "Persistent" chip.

    The most tempting defect in the whole design: the page looks better with a
    badge on every card, and QP2608-Q1 has no family to earn one.
    """
    orig = _read(YEAR26)
    card = 'id="QP2608-Q1"'
    i = orig.index(card)
    j = orig.index('</div>', orig.index('rec-note', i)) + 6
    inject = ('\n    <div class="qy-long"><span class="qy-long-k">Longer-term signal'
              '</span><span class="q-tag">Persistent topic</span></div>')
    _write(YEAR26, orig[:j] + inject + orig[j:])
    return 'R-PROJ-C', lambda: _write(YEAR26, orig)


def mut_2_leak_a_secondary_dated_claim():
    """Print "asked 12 times since 2010" on a gated page, from the secondary
    band. This is the claim the whole date-certainty regime exists to bar."""
    orig = _read(YEAR26)
    new = orig.replace('<span class="q-tag">Recurs beyond MIW&rsquo;s solved set</span>',
                       '<span class="q-tag">Asked 12 times since 2010</span>', 1)
    assert new != orig, 'fixture drifted: no wider-recurrence chip on the 2026 sheet'
    _write(YEAR26, new)
    return 'R-PROJ-D', lambda: _write(YEAR26, orig)


def mut_3_remove_a_modern_repeat_tag():
    """Strip a modern recurrence tag from a card. The existing layer is the one
    thing this session was forbidden to damage."""
    orig = _read(YEAR26)
    m = re.search(r'<span class="q-tag rec">[^<]*</span>', orig)
    _write(YEAR26, orig[:m.start()] + orig[m.end():])
    return 'R-PROJ-H', lambda: _write(YEAR26, orig)


def mut_4_bless_a_stale_answer_from_its_successor():
    """Mark a question CURRENT ANSWER VERIFIED although no governed record names
    it -- the tranche-001 defect, reintroduced at the projection layer."""
    def f(doc):
        victim = next(r for r in doc['questions']
                      if not r['readiness_basis'] and r['canonical_family_ids'])
        victim['readiness_basis'] = 'PHASE2_GOVERNED_REVIEW'
        victim['readiness_signal'] = 'READY_TO_STUDY_NOW'
        victim['readiness_text'] = QIP.READY_TEXT_BY_BASIS['PHASE2_GOVERNED_REVIEW']
    orig = _patch_json(PROJ, f)
    return 'R-PROJ-E', lambda: _write(PROJ, orig)


def mut_5_remove_a_currentness_warning():
    """Strip a rendered currentness warning off a card, leaving a page that
    implies a moved framework is still current.

    Deliberately a PAGE mutation, not a model one. Editing the projection is
    caught by the freshness rule, which proves nothing about whether the
    renderer can drop a warning on its way to the page -- and a warning that
    exists in the model and not on the card is the failure a candidate would
    actually meet.
    """
    orig = _read(YEAR26)
    m = re.search(r'<span class="q-tag warn">[^<]*</span>', orig)
    assert m, 'fixture drifted: no currentness warning rendered on the 2026 sheet'
    _write(YEAR26, orig[:m.start()] + orig[m.end():])
    return 'R-PROJ-B', lambda: _write(YEAR26, orig)


def mut_6_change_a_recurrence_count_in_projection():
    """Edit a recurrence count while projecting. Phase 1 is an input here and
    projection work may never move it."""
    def f(doc):
        doc['counts']['families'] = doc['counts']['families'] + 1
    orig = _patch_json(os.path.join(ROOT, 'docs', 'study', 'qi', 'qi_families.json'), f)
    return 'R-PROJ-L', lambda: _write(
        os.path.join(ROOT, 'docs', 'study', 'qi', 'qi_families.json'), orig)


def mut_7_stale_workbook_copy():
    """Return the workbook to saying the historical QI layer is not integrated,
    while it is in fact feeding the roadmap."""
    p = os.path.join(HERE, 'export_roadmap_xlsx.py')
    orig = _read(p)
    _write(p, orig.replace("            'status': 'LIVE',",
                           "            'status': 'NOT YET INTEGRATED',", 1))
    return 'R-PROJ-J', lambda: _write(p, orig)


def mut_8_topic_readiness_diverges_from_adapter():
    """The topics page reports a readiness count the adapter does not hold."""
    orig = _read(TOPICS)
    m = re.search(r'<span class="chip ready">(\d+) ready to study</span>', orig)
    new = orig[:m.start()] + ('<span class="chip ready">%d ready to study</span>'
                              % (int(m.group(1)) + 7)) + orig[m.end():]
    _write(TOPICS, new)
    return 'R-PROJ-K', lambda: _write(TOPICS, orig)


def mut_9_seo_churn_on_a_page_builder():
    """A page builder quietly flips its robots policy. Not this gate's rule --
    it is asserted here because section 34's hazard was a page generator
    changing SEO as a side effect of unrelated work, and the assertion has to
    live somewhere that runs."""
    orig = _read(YEAR26)
    new = orig.replace('noindex', 'index, follow', 1)
    _write(YEAR26, new)
    return 'R-PROJ-SEO', lambda: _write(YEAR26, orig)


def mut_10_drop_an_august_question():
    """One of the nine August 2026 questions disappears from the projection."""
    def f(doc):
        doc['questions'] = [r for r in doc['questions']
                            if r['question_id'] != 'QP2608-Q4']
    orig = _patch_json(PROJ, f)
    return 'R-PROJ-I', lambda: _write(PROJ, orig)


def mut_11_readiness_on_a_public_surface():
    """Answer readiness reaches a page off the middleware matcher."""
    orig = _read(PUBLIC)
    _write(PUBLIC, orig.replace('</body>',
                                '<p>Current answer verified</p></body>', 1))
    return 'R-PROJ-PUB', lambda: _write(PUBLIC, orig)


def mut_12_paper_page_contradicts_year_sheet():
    """The solved paper prints a longitudinal chip the year sheet does not.
    Two surfaces, one question, two different claims."""
    orig = _read(PAPER)
    new = orig.replace('<span class="q-tag">Recurs beyond MIW&rsquo;s solved set</span>',
                       '<span class="q-tag">Persistent topic</span>', 1)
    assert new != orig, 'fixture drifted: QP2608 carries no wider-recurrence chip'
    _write(PAPER, new)
    return 'R-PROJ-B', lambda: _write(PAPER, orig)


MUTATIONS = [
    ('label an unmapped August question "Persistent"', mut_1_label_an_unmapped_question),
    ('leak "asked 12 times since 2010" onto a gated surface',
     mut_2_leak_a_secondary_dated_claim),
    ('remove an existing modern repeat tag', mut_3_remove_a_modern_repeat_tag),
    ('mark a stale answer CURRENT ANSWER VERIFIED',
     mut_4_bless_a_stale_answer_from_its_successor),
    ('remove a currentness warning', mut_5_remove_a_currentness_warning),
    ('modify a recurrence count during projection',
     mut_6_change_a_recurrence_count_in_projection),
    ('workbook says historical QI is NOT YET INTEGRATED', mut_7_stale_workbook_copy),
    ('topics page readiness differs from the adapter',
     mut_8_topic_readiness_diverges_from_adapter),
    ('a page builder changes its robots policy', mut_9_seo_churn_on_a_page_builder),
    ('one QP2608 question disappears from the projection', mut_10_drop_an_august_question),
    ('answer readiness reaches a public surface', mut_11_readiness_on_a_public_surface),
    ('the solved paper contradicts the year sheet',
     mut_12_paper_page_contradicts_year_sheet),
]


def seo_probe():
    """R-PROJ-SEO. Not part of the gate's twelve, because it is not a claim
    about question intelligence -- it is the no-churn guard the projection work
    had to respect. Asserted over the same rendered bytes."""
    bad = []
    for p in (YEAR26, PAPER):
        head = _read(p)[:6000]
        if 'noindex' not in head:
            bad.append(os.path.relpath(p, ROOT))
    return ['R-PROJ-SEO'] if bad else []


def gate():
    V.QUIET = True
    return V.run() + seo_probe()


def main():
    before = _fingerprint()

    baseline = gate()
    if baseline:
        print('ABORT: the gate does not pass on the unmutated tree -- %s'
              % ', '.join(baseline))
        sys.exit(1)
    print('baseline: gate passes on the unmutated tree')
    print('-' * 68)

    caught, escaped = 0, []
    for desc, fn in MUTATIONS:
        undo = None
        try:
            expected, undo = fn()
            failed = gate()
            hit = expected in failed
            print('  %-4s %-58s %s' % ('OK' if hit else 'MISS', desc,
                                       expected if hit else
                                       ('caught by %s' % ','.join(failed) if failed
                                        else 'NOT CAUGHT')))
            if hit:
                caught += 1
            else:
                escaped.append(desc)
        finally:
            if undo:
                undo()
            QIP._CACHE.clear()

    print('-' * 68)
    after = _fingerprint()
    residue = sorted(os.path.relpath(p, ROOT) for p in WATCHED
                     if before[p] != after[p])

    final = gate()
    print('caught %d / %d   escaped %d   residue %d   gate after restore: %s'
          % (caught, len(MUTATIONS), len(escaped), len(residue),
             'CLEAN' if not final else ', '.join(final)))
    if escaped:
        print('ESCAPED: %s' % '; '.join(escaped))
    if residue:
        print('RESIDUE: %s' % ', '.join(residue))
    if escaped or residue or final:
        sys.exit(1)
    print('All %d mutations caught. Zero escapes, zero residue.' % len(MUTATIONS))


if __name__ == '__main__':
    main()
