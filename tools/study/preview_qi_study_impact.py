#!/usr/bin/env python3
"""SUPERSEDED. The QI study preview is now production.

WHAT THIS WAS
-------------
A read-only preview of what the governed 2010 -> August 2026 QI layer WOULD do
to study priorities if its recurrence were fed into the study-priority model.
It existed because moving a candidate's study order mid-preparation is a
Founder decision, not a build side-effect.

WHAT HAPPENED
-------------
The Founder authorised the integration. `written_recurrence` is now fed from
`tools/study/study_qi_adapter.py`, which joins the existing modern
question-level QI to the canonical longitudinal family layer, and
`build_study_spine.py` reads it. The preview has nothing left to preview.

WHY IT IS NOT SIMPLY RE-RUN
---------------------------
It would now be self-referential. It compared "current" against "QI-informed"
by reading the live spine's `written_recurrence` as the current value -- and
that value IS the QI-informed one today. Re-running it would report a delta of
zero and read as confirmation, which is worse than reporting nothing.

WHY ITS RECORDED ORDER DIFFERS FROM PRODUCTION -- read this before trusting
the frozen artefact
--------------------------------------------------------------------------
The preview predicted:

    D03 > D01 > D02 > D05 > D07 > D04 > D09 > D06 > D10 > D08

Production produced:

    D03 > D01 > D02 > D05 > D04 > D07 > D09 > D06 > D10 > D08

D04 and D07 are the other way round, and the preview was the wrong one. It
credited a family to EVERY topic any of its modern members reached, so a family
whose members span two topics voted twice, and D07 -- a small topic with 13
Written questions -- gained most from the inflation. The adapter attaches a
family's recurrence to ONE canonical current question, so a historical variant
cannot multiply a topic score. The preview's own numbers show it: it reported
42 families for D01 and 27 for D03 where the adapter reports 39 and 25.

That is not a scoring disagreement. It is the preview double-counting, and it
is exactly the failure the adapter's R-VARIANT rules now gate against.

`docs/study/qi/qi_study_preview.json` is kept as the frozen record of what was
shown to the Founder at the decision point, stamped with its supersession. Do
not regenerate it and do not cite its order as current.

    Read instead:  docs/study/study_qi.json
                   tools/study/study_qi_adapter.py
    Gate:          python tools/study/validate_study_qi.py
"""

import sys

SUPERSEDED_BY = 'tools/study/study_qi_adapter.py'
FROZEN_ARTEFACT = 'docs/study/qi/qi_study_preview.json'


def main():
    print(__doc__.strip())
    print('')
    print('This tool is superseded and does nothing. It exits non-zero so that '
          'a script still calling it fails loudly rather than silently '
          'producing no preview.')
    return 2


if __name__ == '__main__':
    sys.exit(main())
