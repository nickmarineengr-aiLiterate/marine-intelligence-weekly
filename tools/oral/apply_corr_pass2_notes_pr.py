#!/usr/bin/env python3
"""Terminal closure A -- the three IACS PR 1 mis-citations in the Notes pages.

OWNERSHIP, corrected. The Pass-2 report deferred these on the ground that the
Notes series is generated from a JSON content spec by tools/notes and must not
be hand-edited. That is true of the parts AUTHORED with that toolchain --
tools/notes/specs holds p19.json..p22.json -- and false of these three files.
miw-notes-mgmt-p7 and the whole simon-notes series predate the builder and have
no spec: `find` for a spec matching either returns nothing, and build_part.py
only ever emits from tools/notes/specs/p<N>.json. There is nothing to
regenerate, and the HTML body IS the source of record.

The SKILL's rule still binds and is honoured: the head, CSS, watermark, topbar,
sidebar, footer and closing scripts are template-carried and are NOT touched
here. Only body prose changes.

The three claims, against IACS's own PR index (read by coordinate extraction,
which is what settled them in the previous round):

  PR 1   Deleted
  PR 3   Transparency of Classification and Statutory Information
  PR 1C  Procedure for Suspension and Reinstatement or Withdrawal of Class in
         Case of Surveys, Conditions of Class or Recommendations Going Overdue
  PR 35  Procedure for Imposing and Clearing Recommendations/Conditions of Class

p7 carries a second, independent error in the same sentence: PR1C A.4.1's six
months is WITHDRAWAL after six months already suspended, not a trigger that
causes suspension.
"""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
NOTES = REPO / "meoclass1" / "oralnotes"

EDITS = [
    ("miw-notes-mgmt-p7.html",
     "The 6-month automatic-suspension trigger for a lapsed CoC extension request is standard "
     "IACS practice\n    (PR1) and is retained.",
     "The six-month figure is corrected rather than retained: under IACS <strong>PR1C "
     "A.4.1</strong> six months is the point at which class already <em>suspended</em> is to "
     "be <strong>withdrawn</strong> — it is not a trigger that causes suspension, and it is "
     "not &ldquo;PR1&rdquo;, which the IACS PR index records as Deleted. An overdue Condition "
     "of Class puts the ship into a suspension <em>procedure</em> under PR1C A.2.1; only an "
     "overdue periodical survey suspends class automatically (A.1.1&ndash;A.1.3)."),

    ("simon-notes-p2.html",
     '<span class="reg-code">IACS PR 1 / Class Rules</span><span class="reg-desc"><em>"IACS '
     'Procedural Requirement PR1 — Procedural Arrangements for Classification"</em> — '
     'conditions of class, survey requirements, and suspension procedures; verify exact PR '
     'number before quoting</span>',
     '<span class="reg-code">IACS PR1C / PR 35</span><span class="reg-desc"><em>PR1C — '
     '"Procedure for Suspension and Reinstatement or Withdrawal of Class in Case of Surveys '
     'or Conditions of Class Going Overdue"</em>, and <em>PR 35 — "Procedure for Imposing and '
     'Clearing Recommendations/Conditions of Class"</em>. The number is now verified: there '
     'is no "PR 1 — Procedural Arrangements for Classification". The IACS PR index records '
     '<strong>PR 1 as Deleted</strong> and PR 3 as Transparency of Classification and '
     'Statutory Information.</span>'),

    ("simon-notes-p6.html",
     '<span class="reg-code">IACS PR 1</span><span class="reg-desc">IACS procedure for '
     'condition of class — classification survey standards</span>',
     '<span class="reg-code">IACS PR 35 / PR1C</span><span class="reg-desc">PR 35 imposes and '
     'clears Recommendations/Conditions of Class; PR1C governs suspension, reinstatement and '
     'withdrawal when surveys or conditions of class go overdue. <strong>Not PR 1</strong>, '
     'which the IACS PR index records as Deleted.</span>'),
]


def main() -> int:
    pages: dict[str, str] = {}
    for name, _, _ in EDITS:
        pages.setdefault(name, (NOTES / name).read_text(encoding="utf-8", newline=""))

    errors, applied = [], 0
    for name, old, new in EDITS:
        text = pages[name]
        if text.count(old) != 1:
            # These files mix entity and literal dashes; try the literal forms.
            for a, b in (("—", "&mdash;"), ("&mdash;", "—")):
                cand = old.replace(a, b)
                if text.count(cand) == 1:
                    old = cand
                    break
        n = text.count(old)
        if n != 1:
            errors.append("%s: anchor occurs %d times, expected 1: %.70s" % (name, n, old))
            continue
        pages[name] = text.replace(old, new, 1)
        applied += 1

    if errors:
        print("ABORTED - nothing written.")
        for e in errors:
            print("  " + e)
        return 1

    for name, text in pages.items():
        (NOTES / name).write_text(text, encoding="utf-8", newline="")
    print("Applied %d edits across %d Notes page(s)." % (applied, len(pages)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
