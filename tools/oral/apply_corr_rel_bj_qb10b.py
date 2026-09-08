#!/usr/bin/env python3
"""CORR-REL-BJ-ATTRIBUTION-20260908, propagated site: QB10_B#q1.

An independent release verifier found what the first pass of this correction
missed, and the miss is worth stating plainly.

QB8_A#q4 and QB5_A#q11 were corrected to state the cause of the `Bulk Jupiter`
loss at the strength the flag State's report states it: no physical evidence of
cause, and only a most-probable finding of liquefaction OR a free-surface
effect. QB10_B#q1 says twice, as settled fact, that "she was lost to bauxite
liquefaction". So the corpus was left contradicting itself on the one
proposition the correction existed to fix.

Two things made that worse than an oversight:

  * The content gate written FOR this correction carried a check named
    `qb10b_still_denies_the_cargo_shift_reading`, asserting that "not a cargo
    shift" remains present on QB10_B. That check does not merely fail to notice
    the contradiction - it REQUIRES the contradicting sentence to stay. A gate
    that pins the defect it was written to prevent.

  * Both correction records asserted, in `corpus_agreement_checked`, that
    QB10_B "agrees with the corrected wording". It did not. The claim was made
    by checking the crew toll and the 21.3% moisture figure - which do agree -
    and never checking the cause-strength proposition that had just changed.

And known_traps entry 131, written in this same batch, states the rule that was
broken: "Whenever a card reports a finding, quote the report's own modal verb."

What is PRESERVED, because it is correct and was tested rather than assumed:
"not a cargo shift" stays. QB10_B draws that distinction to stop a candidate
reaching for the classic solid-mass-slides answer, and it is the right
distinction. What changes is only the certainty, and only where the card speaks
for the investigation.
"""

from __future__ import annotations

import pathlib

QB = pathlib.Path(__file__).resolve().parents[2] / "meoclass1"

EDITS: list[tuple[str, str, str]] = [
    (
        "QB10_B.html",
        "is the standard illustration, and she was lost to bauxite "
        "<strong>liquefaction</strong>, not a cargo shift.",

        "is the standard illustration. The Bahamas Maritime Authority, as flag "
        "State, found no physical evidence of the cause and concluded only that "
        "it was <strong>most probable</strong> that either "
        "<strong>liquefaction</strong> or a <strong>free-surface effect</strong> "
        "induced the list &mdash; not a cargo shift.",
    ),
    (
        "QB10_B.html",
        "She was lost to bauxite <strong>liquefaction</strong> &mdash; not a "
        "cargo shift &mdash; and the investigation found an average cargo "
        "moisture content of 21.3%.",

        "The <strong>Bahamas Maritime Authority</strong> investigated her as "
        "flag State, and its report is expressly qualified: there is <em>no "
        "physical evidence</em> to confirm what caused the unrecoverable list, "
        "and it is <strong>most probable</strong> that either "
        "<strong>liquefaction</strong> or a <strong>free-surface effect</strong> "
        "induced it &mdash; not a cargo shift. The cargo carried an average "
        "moisture content of <strong>21.3%</strong> against the <strong>10%</strong> "
        "declared. Give the mechanism with that qualification in an oral: an "
        "investigation that says <em>most probable, and it may be either of "
        "two things</em> has not concluded, and a candidate who says it has "
        "cannot defend it.",
    ),
]


def main() -> int:
    bad = 0
    for fname, old, new in EDITS:
        path = QB / fname
        text = path.read_text(encoding="utf-8", newline="")
        n = text.count(old)
        if n != 1:
            print("ABORT %-12s matched %d times: %.70s" % (fname, n, old))
            bad += 1
            continue
        path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")
        print("OK    %-12s %5d -> %5d bytes" % (fname, len(old), len(new)))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
