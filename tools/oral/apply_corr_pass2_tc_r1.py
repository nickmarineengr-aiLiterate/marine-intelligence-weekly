#!/usr/bin/env python3
"""Terminal closure, remediation round 1 -- the fifth review's three P1s.

All three sit in QB10_B#q1 and all three were introduced or left standing by
the terminal-closure pass itself. Each is confirmed against primary text read
this pass.

P1-1  Polar Code chapters SWAPPED. MSC.538(107), adopted 8 June 2023, inserts
      "Chapter 9-1 / Safety of navigation for fishing vessels of 24 metres in
      length overall and above..." and "Chapter 11-1 / Voyage planning for
      fishing vessels...". The card had 9-1 as voyage planning and 11-1 as
      safety of navigation, and called them regulations. The sibling QB2_I#q?
      has had them the right way round throughout.

P1-2  STCW-F "the 2022 amendments" does not exist. The instruments are
      MSC.561(108), the revised annex to the 1995 STCW-F Convention, and
      MSC.562(108), the STCW-F Code -- both adopted 23 May 2024, in force
      1 January 2026.

P1-3  The withdrawn Polar citation IS verifiable, so the source gap this pass
      declared was false. MSC.538(107) was retrieved and read in full. Worse,
      the card contradicted itself: the reg box at the other end of the same
      card still asserted MSC.532(107) for this amendment, and QB2_I plus its
      cheat sheet teach the pairing with detail. Restoring the citation is the
      correction; the previous round removed a correct number on a source gap
      it had not actually tested.
"""
from __future__ import annotations

import pathlib
import sys

QB = pathlib.Path(__file__).resolve().parents[2] / "meoclass1"

EDITS = [
    # ---- P1-1 + P1-3: chapters, subjects, and the restored citation --------
    ("<strong>Polar Code extension to non-SOLAS ships &mdash; SOLAS Ch. XIV / Polar Code "
     "Part I-A:</strong>",
     "<strong>Polar Code extension to non-SOLAS ships &mdash; SOLAS Ch. XIV / Polar Code "
     "Part I-A, MSC.532(107) and MSC.538(107):</strong>", 1),

    ("New regulations 9-1 (voyage planning) and 11-1 (safety of navigation) of Polar Code "
     "Part I-A apply.",
     "MSC.538(107), adopted 8 June 2023, inserts two new <strong>chapters</strong> into "
     "Polar Code Part I-A &mdash; <strong>9-1, Safety of navigation</strong>, and "
     "<strong>11-1, Voyage planning</strong>. They are chapters, not regulations, and the "
     "subjects are the way round an examiner will check: 9 is navigation in the parent Code, "
     "so 9-1 is navigation.", 1),

    ("<em>The adopting resolution is not stated here</em>: the MSC.532(107)/MSC.538(107) "
     "pairing this card previously carried could not be verified, and an unverified number "
     "is worse than none.",
     "The adopting resolutions are stated, and a previous revision of this card was wrong to "
     "withdraw them: MSC.538(107) amends the Polar Code and MSC.532(107) carries the parallel "
     "SOLAS Chapter XIV amendments. Both are verifiable, and QB2_I teaches the same pairing.",
     1),

    # ---- P1-2: the STCW-F instruments -------------------------------------
    ("<strong>STCW-F &mdash; the 2022 amendments and the new STCW-F Code:</strong>",
     "<strong>STCW-F &mdash; MSC.561(108), the revised annex to the 1995 Convention, and "
     "MSC.562(108), the new STCW-F Code, both adopted 23 May 2024:</strong>", 1),
]


def main() -> int:
    p = QB / "QB10_B.html"
    text = p.read_text(encoding="utf-8", newline="")
    errors, applied = [], 0
    for old, new, expect in EDITS:
        if text.count(old) != expect:
            for a, b in (("&mdash;", "—"), ("—", "&mdash;")):
                cand = old.replace(a, b)
                if text.count(cand) == expect:
                    old = cand
                    break
        n = text.count(old)
        if n != expect:
            errors.append("anchor occurs %d times, expected %d: %.70s" % (n, expect, old))
            continue
        text = text.replace(old, new, expect)
        applied += expect
    if errors:
        print("ABORTED - nothing written.")
        for e in errors:
            print("  " + e)
        return 1
    p.write_text(text, encoding="utf-8", newline="")
    print("Applied %d edits to QB10_B.html" % applied)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
