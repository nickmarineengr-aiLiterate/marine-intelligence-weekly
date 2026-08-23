#!/usr/bin/env python3
"""D01 study-priority cohort gate.

The Topic 01 pack sorts every mapped D01 oral question into exactly one of
four cohorts -- A, B, C, or the review bucket. That partition is a *claim
about the corpus*, and a claim in a Markdown document rots the moment the
taxonomy moves. It has already rotted once: the pack shipped an A/B/C cohort
summing to 53 after adjudication had grown D01 to 72.

So the cohorts are parsed back out of the pack and checked against
``study_mappings.json``. Two rules carry the weight:

* **The partition is total and disjoint.** A + B + C + REVIEW is exactly the
  governed D01 oral universe -- no duplicates, nothing missing.
* **A-priority is gated on settled evidence.** Only ``VALID_MAPPED`` records
  may be A. "Know this cold" must not be said about a mapping nobody has
  adjudicated.

There is no second store of cohort membership. The pack is the single truth
and this file reads it, so the two cannot disagree.
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK = os.path.join(ROOT, 'docs', 'study', 'TOPIC_01_STATUTORY_SURVEYS_AND_CLASS.md')
STORE = os.path.join(ROOT, 'docs', 'study', 'study_mappings.json')
SESSIONS = os.path.join(ROOT, 'docs', 'study', 'study_sessions.json')

# A-priority is a compression set. These bounds are a deliberate design
# constraint, not a measurement: if the corpus doubles, A must not.
A_MIN, A_MAX = 12, 20

QID = re.compile(r'`([A-Za-z0-9_]+#q\d+)`')

# heading -> (start marker, end marker). The end marker keeps each cohort's
# ids away from the prose that follows it, so a question mentioned in a note
# can never be miscounted as a cohort member.
SECTIONS = [
    ('A',      '## A-PRIORITY ORAL QUESTIONS (',  '### B-PRIORITY ORAL QUESTIONS ('),
    ('B',      '### B-PRIORITY ORAL QUESTIONS (', '### C-PRIORITY ORAL QUESTIONS ('),
    ('C',      '### C-PRIORITY ORAL QUESTIONS (', '### REVIEW — MAPPED, STUDIABLE, NOT YET PRIORITISED ('),
    ('REVIEW', '### REVIEW — MAPPED, STUDIABLE, NOT YET PRIORITISED (',
               '**How this bucket empties.**'),
]


def parse_cohorts(text):
    """-> {cohort: [ids]}, {cohort: declared count in the heading}."""
    out, declared = {}, {}
    for name, start, end in SECTIONS:
        i = text.find(start)
        if i < 0:
            raise AssertionError('cohort section not found: %s' % start)
        j = text.find(end, i + len(start))
        if j < 0:
            raise AssertionError('cohort end marker not found: %s' % end)
        block = text[i:j]
        head = block[len(start):block.index(')')]
        declared[name] = int(head)
        out[name] = QID.findall(block)
    return out, declared


def universe():
    """-> {qid: record} for every governed D01 oral question."""
    store = json.load(io.open(STORE, encoding='utf-8'))['mappings']
    return {r['canonical_question_id']: r for r in store.values()
            if r.get('topic_id') == 'D01' and r['content_type'] == 'ORAL'}


def check(text, qs):
    """-> list of failure strings. Empty means the pack is coherent."""
    fails = []
    try:
        cohorts, declared = parse_cohorts(text)
    except AssertionError as exc:
        return [str(exc)]

    flat = [q for c in ('A', 'B', 'C', 'REVIEW') for q in cohorts[c]]

    dups = sorted({q for q in flat if flat.count(q) > 1})
    if dups:
        fails.append('question in more than one cohort: %s' % dups)

    missing = sorted(set(qs) - set(flat))
    if missing:
        fails.append('%d D01 question(s) in no cohort: %s'
                     % (len(missing), missing[:5]))

    extra = sorted(set(flat) - set(qs))
    if extra:
        fails.append('%d cohort id(s) not in the D01 oral universe: %s'
                     % (len(extra), extra[:5]))

    for name in ('A', 'B', 'C', 'REVIEW'):
        if len(cohorts[name]) != declared[name]:
            fails.append('%s heading declares %d, lists %d'
                         % (name, declared[name], len(cohorts[name])))

    # The A gate. An unadjudicated mapping must never be called core.
    unsettled_a = [q for q in cohorts['A']
                   if qs.get(q, {}).get('mapping_status') != 'VALID_MAPPED']
    if unsettled_a:
        fails.append('A-priority contains unsettled mapping(s): %s' % unsettled_a)

    # B and C are also settled-only; the review bucket is exactly the rest.
    for name in ('B', 'C'):
        bad = [q for q in cohorts[name]
               if qs.get(q, {}).get('mapping_status') != 'VALID_MAPPED']
        if bad:
            fails.append('%s-priority contains unsettled mapping(s): %s' % (name, bad))
    settled_in_review = [q for q in cohorts['REVIEW']
                         if qs.get(q, {}).get('mapping_status') == 'VALID_MAPPED']
    if settled_in_review:
        fails.append('review bucket holds settled mapping(s) that should carry '
                     'a letter: %s' % settled_in_review)

    if not (A_MIN <= len(cohorts['A']) <= A_MAX):
        fails.append('A-priority is %d, outside the %d-%d compression band'
                     % (len(cohorts['A']), A_MIN, A_MAX))

    # The arithmetic table a human reads must agree with the lists.
    for name, label in (('A', 'A-priority'), ('B', 'B-priority'),
                        ('C', 'C-priority'),
                        ('REVIEW', 'Review — not yet prioritised')):
        row = re.search(r'\|\s*%s\s*\|\s*(\d+)\s*\|' % re.escape(label), text)
        if not row:
            fails.append('cohort arithmetic table has no %s row' % label)
        elif int(row.group(1)) != len(cohorts[name]):
            fails.append('arithmetic table says %s = %s, lists show %d'
                         % (label, row.group(1), len(cohorts[name])))
    total = re.search(r'\|\s*\*\*Total\*\*\s*\|\s*\*\*(\d+)\*\*', text)
    if not total:
        fails.append('cohort arithmetic table has no Total row')
    elif int(total.group(1)) != len(qs):
        fails.append('arithmetic table total is %s, universe is %d'
                     % (total.group(1), len(qs)))
    return fails


def check_sessions(qs):
    """Every D01 session task that names an oral must name a real D01 one."""
    fails = []
    doc = json.load(io.open(SESSIONS, encoding='utf-8'))
    seen = set()
    for s in doc['sessions']:
        if s['topic_id'] != 'D01':
            continue
        for t in s['tasks']:
            qid = t.get('question_id')
            if qid and '#q' in qid:
                seen.add(qid)
                if qid not in qs:
                    fails.append('%s step %d cites %s, which is not a D01 oral'
                                 % (s['session_id'], t['step'], qid))
    return fails, seen


def main():
    text = io.open(PACK, encoding='utf-8', newline='').read()
    qs = universe()
    checks = 0
    fails = check(text, qs)
    checks += 12
    sess_fails, cited = check_sessions(qs)
    fails += sess_fails
    checks += 1

    # Every A-priority question must be reachable through some session, or the
    # plan says "know this cold" about something it never asks you to open.
    cohorts, _ = parse_cohorts(text)
    orphan_a = sorted(set(cohorts['A']) - cited)
    if orphan_a:
        fails.append('A-priority question(s) no session reaches: %s' % orphan_a)
    checks += 1

    # ---- mutation controls -------------------------------------------------
    # A test that only ever sees a passing corpus proves nothing. Each mutation
    # below is a defect this gate exists to catch; each must fail.
    mutations = [
        ('duplicate across cohorts',
         lambda t: t.replace('| `QB3_B#q1` | What is a hull survey',
                             '| `QB1_H#q3` | What is a hull survey')),
        ('unsettled question promoted to A',
         lambda t: t.replace('| 5 | 5 Class | `QB1_K#q2` |',
                             '| 5 | 5 Class | `QB1_F#q15` |')),
        ('a question dropped from every cohort',
         lambda t: t.replace('`QB1_F#q16`, ', '')),
        ('heading count left stale',
         lambda t: t.replace('## A-PRIORITY ORAL QUESTIONS (18)',
                             '## A-PRIORITY ORAL QUESTIONS (14)')),
        ('arithmetic table left stale',
         lambda t: t.replace('| A-priority | 18 |', '| A-priority | 14 |')),
    ]
    escapes = []
    for label, mutate in mutations:
        mutated = mutate(text)
        if mutated == text:
            escapes.append('%s -- mutation did not apply (anchor moved)' % label)
        elif not check(mutated, qs):
            escapes.append('%s -- mutation NOT caught' % label)
        checks += 1

    print('D01 priority cohort gate -- %d checks' % checks)
    for f in fails:
        print('  FAIL: %s' % f)
    for e in escapes:
        print('  MUTATION ESCAPE: %s' % e)
    if fails or escapes:
        return 1
    cohorts, _ = parse_cohorts(text)
    print('  A=%d B=%d C=%d REVIEW=%d  total=%d  universe=%d'
          % (len(cohorts['A']), len(cohorts['B']), len(cohorts['C']),
             len(cohorts['REVIEW']),
             sum(len(cohorts[k]) for k in ('A', 'B', 'C', 'REVIEW')), len(qs)))
    print('  all PASS (5 mutations caught)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
