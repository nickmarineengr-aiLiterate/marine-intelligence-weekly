#!/usr/bin/env python3
"""Mutation tests for the 2021-2022 wording archive.

A gate that has never rejected anything has not been shown to work, and this
gate guards the one thing the archive could plausibly do wrong: look like the
paid product. Every mutation below is a specific, plausible way that could
happen -- a copied heading, an inherited link, a year page built one year too
far back -- not arbitrary corruption.

Unlike the Phase-2 suite these tests must touch DISK, because the checker's
whole point is that it reads shipped bytes. Each mutation is therefore written
to a real file, checked, and rolled back, and the suite sha256-fingerprints
every artefact before and after to prove nothing survived. A failure to restore
is reported as loudly as a failure to catch.

    python tools/pastpapers/questions_year_archive_mutations.py
"""
import glob
import hashlib
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import REPO_ROOT

PP_DIR = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')
SQ_DIR = os.path.join(REPO_ROOT, 'solvedQP')
CHECK = os.path.join(HERE, 'questions_year_check.py')

A2021 = os.path.join(PP_DIR, 'questions-2021.html')
A2022 = os.path.join(PP_DIR, 'questions-2022.html')
S2021 = os.path.join(SQ_DIR, 'questions-2021.html')
SOLVED_SHEET = os.path.join(PP_DIR, 'questions-2026.html')
FAKE_2020 = os.path.join(PP_DIR, 'questions-2020.html')
HOME = os.path.join(SQ_DIR, 'index.html')

#: Everything that must be byte-identical when the suite finishes.
WATCHED = sorted(
    glob.glob(os.path.join(PP_DIR, 'questions-*.html'))
    + glob.glob(os.path.join(SQ_DIR, 'questions-*.html'))
    + [HOME])


#: BOTH gates that stand over these bytes. questions_year_check owns the
#: archive's own rules; validate_qi_projection owns the modern-tag census and
#: the closed label vocabulary across every candidate surface. Running only the
#: first would let a mutation that damages the SOLVED sheets pass a suite whose
#: whole subject is a change to those sheets' neighbours.
GATES = (CHECK, os.path.join(REPO_ROOT, 'tools', 'study',
                             'validate_qi_projection.py'))


def run_check():
    """Both gates, as subprocesses. Returns the rule codes they raised.

    Subprocesses rather than imports because the checkers read the filesystem
    at module scope in places, and a stale module cache would let a mutation
    pass by not being seen.
    """
    rules, out = set(), ''
    for gate in GATES:
        p = subprocess.run([sys.executable, gate], capture_output=True,
                           text=True, cwd=REPO_ROOT)
        out += p.stdout + p.stderr
        for line in (p.stdout + p.stderr).splitlines():
            t = line.strip()
            if t.startswith('FAIL '):
                rules.add(t.split()[1])
    return rules, out


def swap(path, old, new):
    """Replace `old` with `new` in `path`; returns a restore callable."""
    original = io.open(path, encoding='utf-8', newline='').read()
    if old not in original:
        raise AssertionError('mutation anchor not found in %s: %r' % (path, old[:60]))
    io.open(path, 'w', encoding='utf-8', newline='').write(
        original.replace(old, new, 1))
    return lambda: io.open(path, 'w', encoding='utf-8', newline='').write(original)


def create(path, text):
    io.open(path, 'w', encoding='utf-8', newline='').write(text)
    return lambda: os.remove(path)


# --------------------------------------------------------------------------
# Mutations. Each returns (restore, expected_rule_prefix).
# --------------------------------------------------------------------------

def mut_01_unsolved_item_marked_solved():
    """The archive sheet copies the solved sheet's month heading.

    This is the likeliest single failure, because the two generators sit in one
    file and the heading is one string apart."""
    return swap(A2021, 'Question wording held', 'Solved paper available'), 'ARCHIVE-D'


def mut_02_fake_solved_answer_link():
    """A 2021 question grows an "open the solved answer" button.

    There is no answer behind it. The reader clicks into the paid product and
    lands on a paper that does not contain their question."""
    return swap(A2021, '<main id="qy-main"',
                '<div class="btn-row"><a class="nav-btn" href="/solvedQP/QP2407.html#q7">'
                'Open the solved answer &rarr;</a></div><main id="qy-main"'), 'ARCHIVE-E'


def mut_03_pre_floor_year_in_navigation():
    """2020 is added to the year navigation on the paid home.

    A link is a claim that the page exists and that its dates are as good as
    the others'. Neither is true below the floor."""
    return swap(HOME, '/solvedQP/questions-2021.html',
                '/solvedQP/questions-2020.html'), 'ARCHIVE-BOUNDARY'


def mut_04_pre_floor_year_page_created():
    """questions-2020.html is built.

    Unlinked, so no navigation test would see it -- and it is still published,
    still indexable in publish mode, and still a dated claim on every 2020
    question it prints from SECONDARY_CLAIMED evidence."""
    return create(FAKE_2020, '<!DOCTYPE html><html><body><h1>2020</h1></body></html>'), \
        'ARCHIVE-BOUNDARY'


def mut_05_host_annotation_republished():
    """The source copy publisher's own recurrence annotation is printed.

    `host_recurrence_hint` sits on every archive record and renders in one
    line of code. It is a third party's analysis, it is directional, and the
    2026 set proved it wrong in both directions."""
    return swap(A2021, '<main id="qy-main"',
                '<main id="qy-main"><p>Previously set: 2011/SR2, 2018/AUG.</p>'), \
        'ARCHIVE-H'


def mut_06_modern_recurrence_relationship_lost():
    """A solved sheet loses a Layer-1 recurrence tag while the archive is built.

    The archive must not touch the calendar model. If it ever did, this is what
    it would look like from outside: the 2026 sheet quietly disagreeing with
    the recurrence model that produced it."""
    return swap(SOLVED_SHEET, '<span class="q-tag rec">Repeated',
                '<span class="q-tag rec">Set once'), 'R-PROJ-A'


def mut_07_longitudinal_tag_bypasses_projection():
    """A longitudinal chip is written straight into the page.

    "Persistent topic" is in the closed vocabulary, so a vocabulary check would
    wave it through. It is not the tag the projection gives THIS question, and
    that is the test that matters."""
    return swap(A2022, '<main id="qy-main"',
                '<main id="qy-main"><div class="hit" data-qsearch="x" id="QP2201-Q1">'
                '<span class="q-tag">Persistent topic</span></div>'), 'ARCHIVE-B'


def mut_08_readiness_implies_the_old_sitting_was_solved():
    """"Current answer verified" appears on a 2021 sheet.

    A governed Phase-2 record can name a CURRENT answer for a concept a 2021
    question raised. That is not the same as the 2021 question having been
    answered, and this is the wording that collapses the two."""
    # The CHIP, not the legend entry. The legend names this vocabulary in
    # order to explain it, and mutating the explanation would prove nothing.
    return swap(A2021,
                '<span class="q-tag ready">Current-framework answer in preparation</span>',
                '<span class="q-tag ready">Current answer verified</span>'), 'ARCHIVE-D'


def mut_09_question_count_disagrees_with_source():
    """The header count is edited without the questions changing."""
    return swap(A2021, '<span>99 questions</span>',
                '<span>108 questions</span>'), 'ARCHIVE-J'


def mut_10_search_mixes_archive_and_solved():
    """The solved-corpus escape hatch is added to an archive sheet.

    It answers "and what about the other years?" by searching the SOLVED
    manifest. On this sheet the answer arrives under a heading that says these
    questions are not solved, and the two statuses land in one result list."""
    return swap(S2021, '<main id="qy-main"',
                '<main id="qy-main"><div id="mc-wrap" hidden></div>'), 'ARCHIVE-L'


def mut_11_readiness_scope_sentence_removed():
    """The legend loses the sentence saying whose answer the readiness chips
    describe.

    Fifty-five of these 198 questions inherit READY_TO_STUDY_NOW from their
    recurrence family and render "No currentness risk flagged". The answer that
    clears them sits on a solved paper from a later year. Without the sentence,
    an all-clear chip sits under a header that says MIW has not solved these
    papers, and the page contradicts itself in the reader's favour -- which is
    the direction that costs a candidate marks."""
    return swap(A2021, 'never this 2021 question', 'about this question'), 'ARCHIVE-M'


MUTATIONS = [
    ('unsolved item marked solved', mut_01_unsolved_item_marked_solved),
    ('fake solved-answer link', mut_02_fake_solved_answer_link),
    ('pre-floor year in navigation', mut_03_pre_floor_year_in_navigation),
    ('pre-floor year page created', mut_04_pre_floor_year_page_created),
    ('host annotation republished', mut_05_host_annotation_republished),
    ('modern recurrence relationship lost', mut_06_modern_recurrence_relationship_lost),
    ('longitudinal tag bypasses projection', mut_07_longitudinal_tag_bypasses_projection),
    ('readiness implies old sitting solved', mut_08_readiness_implies_the_old_sitting_was_solved),
    ('question count differs from source', mut_09_question_count_disagrees_with_source),
    ('search mixes archive and solved', mut_10_search_mixes_archive_and_solved),
    ('readiness scope sentence removed', mut_11_readiness_scope_sentence_removed),
]


def fingerprint():
    out = {}
    for path in WATCHED:
        if os.path.exists(path):
            with open(path, 'rb') as fh:
                out[path] = hashlib.sha256(fh.read()).hexdigest()
    return out


def main():
    before = fingerprint()
    baseline, out = run_check()
    if baseline:
        print('ABORT: the gate does not pass on the unmutated tree -- %s'
              % ', '.join(sorted(baseline)))
        print(out)
        return 1

    caught = escaped = 0
    for i, (name, mut) in enumerate(MUTATIONS, 1):
        restore, want = mut()
        try:
            fails, _ = run_check()
        finally:
            restore()
        if fails and (want is None or any(f.startswith(want) for f in fails)):
            print('  CAUGHT   %02d  %-38s -> %s'
                  % (i, name, sorted(fails)[0]))
            caught += 1
        else:
            print('  ESCAPED  %02d  %-38s (wanted %s, got %s)'
                  % (i, name, want, sorted(fails) or 'nothing'))
            escaped += 1

    after = fingerprint()
    residue = sorted(set(before) ^ set(after)) + \
        [p for p in before if p in after and before[p] != after[p]]
    print('\ncaught %d / escaped %d / residue %d'
          % (caught, escaped, len(residue)))
    for p in residue:
        print('  RESIDUE  %s' % os.path.relpath(p, REPO_ROOT))
    if escaped or residue:
        return 1
    print('all mutations caught, zero escapes, zero residue.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
