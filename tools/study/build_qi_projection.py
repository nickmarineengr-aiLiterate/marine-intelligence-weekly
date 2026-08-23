#!/usr/bin/env python3
"""Only writer of docs/study/safe_qi_projection.json.

    python tools/study/build_qi_projection.py            # write
    python tools/study/build_qi_projection.py --check    # fail if stale

Same shape as every other builder in this layer: the artefact is a pure
function of governed inputs, so --check rebuilding to different bytes means an
input moved and the page generators are about to render a stale claim.
"""
import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import qi_projection as P


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    obj = P.build()
    text = json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=False) + '\n'

    if args.check:
        if not os.path.exists(P.OUT):
            print('STALE: %s does not exist' % os.path.relpath(P.OUT, P.ROOT))
            sys.exit(1)
        cur = open(P.OUT, encoding='utf-8', newline='').read()
        if cur != text:
            print('STALE: safe_qi_projection.json does not match its inputs')
            sys.exit(1)
        print('build_qi_projection --check: projection matches its inputs '
              '(%d questions, %d families)'
              % (obj['totals']['questions'], obj['totals']['families']))
        return

    st = P.write(P.OUT, obj)
    t = obj['totals']
    print('safe_qi_projection.json  %s' % st)
    print('  questions %d   with longitudinal signal %d   with readiness %d'
          % (t['questions'], t['with_longitudinal_signal'], t['with_readiness_signal']))
    print('  families %d   printed-only basis %d   downgraded to wider-recurrence %d'
          % (t['families'], t['families_labelled_from_printed_only'],
             t['families_downgraded_to_wider_recurrence']))


if __name__ == '__main__':
    main()
