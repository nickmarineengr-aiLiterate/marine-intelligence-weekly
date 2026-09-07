#!/usr/bin/env python3
"""Pass-2 remediation round 2 -- the sibling the first sweep claimed did not exist.

CORR-PASS2-PR1C-SUSPENSION recorded that a corpus search for "all statutory
certificates" left "only the already-corrected QB1_K q2, and past-paper
examiner wording". A second independent review ran that search and found
QB4_A#q9 -- a teaching card, not examiner wording -- carrying all three
propositions the PR1C record exists to correct, in six layers.

So the record's completeness claim was false, and the defect it missed was
live. Both are closed here: the card becomes the eighth declared card of this
batch, and the record's propagation section is rewritten.

Four defects, each verified against PR1C Rev.7 read this pass:

  1. "all statutory certificates ... become simultaneously invalid" - B.1.3
     says CERTAIN statutory certificates are implicitly invalidated.
  2. "P&I cover typically falls away" - PR1C contains no insurance provision.
     The card's own "seaworthy and in class is a fundamental warranty" is the
     accurate half and is kept; the automatic-loss half is not.
  3. "failure to meet the due date results in Suspension of Class" for a
     Condition of Class - A.2.1 makes that a suspension PROCEDURE, not an
     automatic consequence. A.1.1-A.1.3 automatic limb belongs to overdue
     periodical surveys.
  4. "IACS UR Z23" cited three times as the RO-to-Flag-State notification
     instrument. UR Z23 is "Hull Survey for New Construction". This is the
     same defect shape as the UR Z15 misattribution on QB4_C#q5: right issuer,
     right series, wrong document, and invisible to any check that only asks
     whether a citation exists.

NOT touched, and recorded as unverified rather than corrected: the card's
"IACS PR No.1" and "IACS PR No.3" reg-box entries. The IACS PR index could not
be read cleanly this pass, so no replacement number is asserted. PR1C is added
as the entry that IS verified to govern this subject.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
QB = HERE.parent.parent / "meoclass1"

EDITS = [
    # ---- 15-second answer ------------------------------------------------
    ("QB4_A.html",
     "failure to meet the due date results in Suspension of Class. When class is "
     "suspended, all statutory certificates issued by the RO on behalf of the Flag State "
     "become simultaneously invalid — the ship cannot trade, P&amp;I cover typically "
     "falls away, and the Flag State is notified by the RO under IACS UR Z23.",

     "if the due date passes unrectified, IACS PR1C A.2.1 puts the vessel into a "
     "<strong>suspension procedure</strong> — it is not automatic, unlike an overdue "
     "periodical survey, which suspends class automatically under A.1.1–A.1.3. Once "
     "class is suspended the Society confirms it in writing to the Owner and the Flag "
     "State (B.1.1), and for SOLAS ships that letter states that <em>certain</em> "
     "statutory certificates are implicitly invalidated (B.1.3) — not all of them at "
     "once. Our class warranty is breached, so cover may be prejudiced; PR1C itself says "
     "nothing about insurance."),

    # ---- 60-second answer ------------------------------------------------
    ("QB4_A.html",
     "If a Condition expires unresolved, the society suspends class; under IACS UR Z23 "
     "and SOLAS Ch I/Reg 6, the RO must notify the Flag State, and all statutory "
     "certificates issued by that RO on behalf of the Flag State become invalid "
     "simultaneously — not just the class notation.",

     "If a Condition expires unresolved, IACS PR1C A.2.1 provides that the vessel&#x27;s "
     "class becomes <strong>subject to a suspension procedure</strong> — worth saying "
     "precisely, because an overdue Annual, Intermediate or Special survey suspends "
     "class <strong>automatically</strong> under A.1.1–A.1.3, and blending the two is "
     "the commonest error here. On suspension the Society confirms it in writing to the "
     "Owner and to the Flag State (B.1.1–B.1.2), and under B.1.3 that letter states, for "
     "SOLAS ships, that <em>certain</em> statutory certificates are implicitly "
     "invalidated — which is narrower than &ldquo;all of them simultaneously&rdquo;, and "
     "narrower is the defensible answer."),

    # ---- cascade bullets --------------------------------------------------
    ("QB4_A.html",
     "<li>All statutory certificates issued by the RO on the Flag State's behalf become "
     "invalid — SCC, SEC, SRC, IOPP, IAPP, Load Line Certificate.</li>",
     "<li>Under PR1C B.1.3 the Society&#x27;s letter states that <strong>certain</strong> "
     "statutory certificates issued by the RO on the Flag State&#x27;s behalf are "
     "implicitly invalidated. Which ones depends on the certificate and on the flag "
     "Administration, so name the likely ones — SCC, SEC, SRC, IOPP, IAPP, Load Line — "
     "as examples rather than asserting that every certificate falls at once.</li>"),

    ("QB4_A.html",
     "<li>P&amp;I Club cover typically falls away — \"seaworthy and in class\" is a "
     "fundamental warranty under standard P&amp;I Club Rules.</li>",
     "<li>Insurance: &quot;seaworthy and in class&quot; is a fundamental warranty under "
     "standard P&amp;I Club Rules, so loss of class breaches it and cover may be "
     "prejudiced — the consequence is whatever the policy and its governing law provide. "
     "PR1C contains no insurance provision at all, so do not tell an examiner that cover "
     "automatically ends.</li>"),

    ("QB4_A.html",
     "<li>Flag State is notified by the RO under IACS UR Z23 and SOLAS Ch I/Reg 6.</li>",
     "<li>The Society confirms the suspension in writing to the Owner and to the Flag "
     "State — <strong>IACS PR1C B.1.1</strong>, with B.1.2 covering withdrawal. "
     "(Not UR Z23: that is Hull Survey for New Construction.)</li>"),

    # ---- regulatory references -------------------------------------------
    ("QB4_A.html",
     "<div class=\"reg-item\"><span class=\"reg-code\">IACS UR Z23</span>"
     "<span class=\"reg-desc\">Survey status communication from RO to Flag State; "
     "suspension notification</span></div>",
     "<div class=\"reg-item\"><span class=\"reg-code\">IACS PR1C, Rev.7 (Nov 2024)</span>"
     "<span class=\"reg-desc\">Procedure for Suspension and Reinstatement or Withdrawal "
     "of Class in Case of Surveys or Conditions of Class Going Overdue — the instrument "
     "that governs this answer. A.1.1–A.1.3 automatic suspension for overdue periodical "
     "surveys; A.2.1 a suspension <em>procedure</em> for an overdue condition of class; "
     "A.4.1 withdrawal after six months suspended; B.1.1–B.1.3 written notification to "
     "Owner and Flag State stating that certain statutory certificates are implicitly "
     "invalidated. Applies from 1 January 2026. <strong>Not UR Z23</strong>, which is "
     "Hull Survey for New Construction.</span></div>"),

    # ---- CE oral tip -------------------------------------------------------
    ("QB4_A.html",
     "immediately add that all RO-issued statutory certificates become invalid "
     "simultaneously, P&amp;I cover typically falls away, and the ship cannot trade.",
     "immediately add the consequence, and state it precisely: under PR1C B.1.3 the "
     "Society&#x27;s letter to Owner and Flag State says that <em>certain</em> "
     "RO-issued statutory certificates are implicitly invalidated, our class warranty is "
     "breached so cover may be prejudiced, and the ship cannot trade."),

    # ---- trap answer -------------------------------------------------------
    ("QB4_A.html",
     "A: Class is suspended. All statutory certificates issued by the RO on behalf of "
     "the Flag State are invalid. The ship cannot sail.",
     "A: Sir, an overdue Condition of Class puts us into a suspension procedure under "
     "PR1C A.2.1 rather than suspending class automatically — the automatic limb is for "
     "overdue periodical surveys. Once suspended, the Society writes to the Owner and "
     "the Flag State, and that letter states that certain of our RO-issued statutory "
     "certificates are implicitly invalidated. The ship cannot sail."),

    # ---- numbers layer -----------------------------------------------------
    ("QB4_A.html",
     "<p>IACS PR No.1, PR No.3, UR Z23. Three notation types:",
     "<p>IACS PR1C — A.1 automatic suspension on overdue periodical surveys (three "
     "months, and not while under attendance), A.2.1 suspension procedure on an overdue "
     "condition of class, A.4.1 withdrawal after six months, B.1.1–B.1.3 notification to "
     "Owner and Flag State. Three notation types:"),
]


def main() -> int:
    pages: dict[str, str] = {}
    for name, _, _ in EDITS:
        if name not in pages:
            pages[name] = (QB / name).read_text(encoding="utf-8", newline="")

    errors, applied = [], 0
    for name, old, new in EDITS:
        text = pages[name]
        n = text.count(old)
        if n != 1:
            errors.append("%s: anchor occurs %d times, expected 1: %.80s" % (name, n, old))
            continue
        pages[name] = text.replace(old, new, 1)
        applied += 1

    if errors:
        print("ABORTED - nothing written.")
        for e in errors:
            print("  " + e)
        return 1

    for name, text in pages.items():
        (QB / name).write_text(text, encoding="utf-8", newline="")
    print("Applied %d edits to %d file(s)." % (applied, len(pages)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
