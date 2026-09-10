#!/usr/bin/env python3
"""CORR-REL-BJ-CHEATSHEET-20260909 -- the propagated Bulk Jupiter sibling.

WHAT THIS IS
------------
CORR-REL-BJ-ATTRIBUTION-20260908 and CORR-REL-BJ-FOUNDERING-20260908 corrected
QB8_A#q4 and QB5_A#q11 so that neither asserts a settled cause for the loss of
`Bulk Jupiter`: the Bahamas Maritime Authority, as flag State, records that there
is no physical evidence of cause and concludes only that liquefaction OR a
free-surface effect is most probable. QB10_B was brought into line in the same
release.

`meoclass1/QB2_B_CheatSheet.html` was not. Its Key Numbers block still read

    Casualties: MV Bulk Jupiter (2015) - bauxite liquefaction sinking

which states the rejected proposition -- liquefaction, as established fact --
in the most memorisation-weighted surface the corpus has. A cheat sheet is what
a candidate reads on the morning of the oral, so a settled-cause claim here
outranks the qualified wording on the long cards it summarises.

This is a same-proposition propagation omission, not a new finding. No new
casualty research was done and no new source was read: the replacement wording
is the governed language of the two September 8 records.

HOW IT SURVIVED THE ORIGINAL GATE
---------------------------------
`validate_correction_bulkjupiter.py` asserts the cause-strength proposition per
site on QB8_A#q4, QB5_A#q11 and both QB10_B sites. For this file it asserted
only presence -- `"Bulk Jupiter" in sheet` -- so the sentence could say anything
at all. Its closed-world negative, `no_page_asserts_the_cause_as_settled`, is
documented as running over the deployed bank but matches two literal strings
taken from QB10_B's own prior wording ("was lost to bauxite liquefaction"). The
cheat sheet says "bauxite liquefaction sinking", which neither pattern reaches.
A guard keyed to the phrasing of the site it was written from is blind to the
same proposition spelled differently. The gate is extended alongside this edit.

THE EDIT
--------
One exact-string replacement, required to match exactly once. Nothing else on
the page is touched -- not the TML rule, not the angle-of-repose marker, not the
Group A/B/C block above it, not the Trap below it. Read and write both use
newline="" so the file's own line endings survive byte for byte.
"""
from __future__ import annotations

import pathlib
import sys

QB = pathlib.Path(__file__).resolve().parents[2] / "meoclass1"

FILE = "QB2_B_CheatSheet.html"

BEFORE = (
    "<li>Casualties: <em>MV Bulk Jupiter (2015)</em> — bauxite liquefaction "
    "sinking</li>"
)

# The modal verb and both mechanisms are the flag State's own, carried across
# verbatim in substance from the two governed records. Kept to one cheat-sheet
# line: a bullet a candidate cannot hold is a bullet that gets replaced by the
# wrong one they already remember.
AFTER = (
    "<li>Casualties: <em>MV Bulk Jupiter (2015)</em> — bauxite; most probably "
    "liquefaction or a free-surface effect (flag State found no physical evidence "
    "of cause)</li>"
)


def main() -> int:
    path = QB / FILE
    with open(path, "r", encoding="utf-8", newline="") as fh:
        src = fh.read()

    n = src.count(BEFORE)
    if n != 1:
        print("FAIL %s: pre-edit string matched %d times, expected exactly 1" % (FILE, n))
        return 2
    if AFTER in src:
        print("SKIP %s: already corrected" % FILE)
        return 0

    out = src.replace(BEFORE, AFTER)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)
    print("applied CORR-REL-BJ-CHEATSHEET-20260909 to %s (1 replacement)" % FILE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
