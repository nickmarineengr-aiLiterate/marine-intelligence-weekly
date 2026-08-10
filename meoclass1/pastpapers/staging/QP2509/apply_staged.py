#!/usr/bin/env python3
"""Apply the staged QP2509 answer objects into specs/QP2509.json.

Usage, from the repository root:

    python meoclass1/pastpapers/staging/QP2509/apply_staged.py [--check]

WHY THIS FILE EXISTS
--------------------
`PASTPAPER_PRODUCTION_PROTOCOL.md` section 3: "There is no valid
half-authored-paper state. Either the paper is complete and internally
consistent, or the session stops and records exactly where it stopped and why."

The toolchain enforces that mechanically. `build_paper.py` selects a paper by the
PRESENCE OF ANSWERS, not by `build_state`, so a spec carrying three answers and
six nulls enters the build pipeline and fails in `render_blocks` on the first
null. A partially authored spec therefore turns the whole branch red - it is not
merely untidy, it is a broken build.

The 2026-08-11 session authored and verified Q2, Q5 and Q7 to the READY standard
but could not reach 9/9. Rather than discard verified work or leave the branch
failing, those three question objects are parked HERE and `specs/QP2509.json` is
left as untouched intake. The toolchain stays green, and the next session applies
this file in one command and continues at Q8.

WHAT IS STAGED
--------------
`authored_questions.json` holds the three complete question objects exactly as
they validated - answer_status "Built", 0 validator errors. Their verification
records are already in the repository at `verification/QP2509/`, because those
are the durable research product and stand on their own.

RESUMING
--------
    python meoclass1/pastpapers/staging/QP2509/apply_staged.py
    python tools/pastpapers/validate_spec.py meoclass1/pastpapers/specs/QP2509.json

Expect 0 errors and 3 word-count warnings. Then author Q8, Q3, Q9, Q4, Q1, Q6,
and only when all nine are Built run the toolchain and build the paper.

This script is idempotent: applying it twice produces the same spec.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
SPEC = os.path.join(ROOT, 'meoclass1', 'pastpapers', 'specs', 'QP2509.json')
STAGED = os.path.join(HERE, 'authored_questions.json')


def main(check_only=False):
    spec = json.load(io.open(SPEC, encoding='utf-8'))
    staged = json.load(io.open(STAGED, encoding='utf-8'))

    by_no = {q['q_no']: i for i, q in enumerate(spec['questions'])}
    applied, already = [], []

    for q_no, obj in staged.items():
        if q_no not in by_no:
            print('ERROR: %s is not a question in the spec' % q_no)
            return 1
        cur = spec['questions'][by_no[q_no]]
        if cur.get('text_verbatim') != obj.get('text_verbatim'):
            print('ERROR: %s printed stem differs between spec and staged object. '
                  'Refusing to apply - the source copy is the authority and a stem '
                  'mismatch means one of them has drifted.' % q_no)
            return 1
        if cur.get('model_answer'):
            already.append(q_no)
            continue
        spec['questions'][by_no[q_no]] = obj
        applied.append(q_no)

    if check_only:
        print('would apply: %s' % (', '.join(applied) or 'nothing'))
        print('already present: %s' % (', '.join(already) or 'none'))
        return 0

    json.dump(spec, io.open(SPEC, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('applied: %s' % (', '.join(applied) or 'nothing'))
    if already:
        print('already present, left untouched: %s' % ', '.join(already))
    built = sum(1 for q in spec['questions'] if q.get('model_answer'))
    print('QP2509 now %d/9 built.' % built)
    if built < 9:
        print('DO NOT BUILD. %d question(s) still unauthored - the paper is not '
              'shippable until 9/9.' % (9 - built))
    return 0


if __name__ == '__main__':
    sys.exit(main(check_only='--check' in sys.argv))
