#!/usr/bin/env python3
"""Pass-2 remediation round 3 -- the sweep, done properly this time.

Three rounds have now failed the same way: a sweep is run in the vocabulary of
the card being fixed, its result is written into a record as a completeness
claim, and nothing verifies the claim. Round 3's review found four more live
sites, one of them a P0 - the DERIVED CHEAT SHEET of the card round 2 had just
corrected, still teaching the opposite. It escaped every previous sweep because
it abbreviates "certificates" to "certs", which no search term covered.

So this round does two things. It corrects the sites, and it replaces the prose
claim with a generated artefact: sweep_pr1c_family.py enumerates every page from
disk, reads RENDERED text, and searches on token variants. The record cites its
output instead of asserting a conclusion.

Corrections, all against IACS primary text read this pass:

  QB4_A_CheatSheet  P0. Three sites teaching "CoC = suspension if missed",
                    "ALL RO-issued statutory certs invalid simultaneously" and
                    "P&I cover typically void". The derived surface of QB4_A#q9.

  QB4_A#q9          The notation TABLE row still said "Class suspended if not
                    met by due date" - untouched by round 2, and the card's most
                    memorisable layer. The Numbers line generalised the
                    three-month window to A.1; it belongs to A.1.2 and A.1.3
                    only, because A.1.1 suspends from the certificate expiry
                    date. PR No.1 is Deleted and PR No.3 is Transparency of
                    Classification and Statutory Information - the instrument
                    the card described is PR 35, "Procedure for Imposing and
                    Clearing Recommendations/Conditions of Class". All four
                    verified from IACS's own PR index by positional extraction;
                    the earlier record's claim that the index "could not be read
                    cleanly" was a failure of method, not of the source.

  QB1_C#q6          All three propositions in one sentence, plus the H-backslash escape
                    artefact, plus a self-contradiction with its own preceding
                    paragraph.

  QB4_E#q13         Unqualified statutory-certificate invalidation, in the same
                    file as declared card q12.

  QB1_F#q7          "automatically invalidating the ship's insurance policies
                    cover", twice. The PR1C record cited this FILE as already
                    correct on the strength of its section 4, which is - and
                    that is the same reasoning error as the sweep claim.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
QB = HERE.parent.parent / "meoclass1"

EDITS = [
    # ---- P0: the derived cheat sheet -------------------------------------
    ("QB4_A_CheatSheet.html",
     "<li><strong>CoC</strong> = binding, due date, suspension if missed</li>",
     "<li><strong>CoC</strong> = binding, due date; if missed, PR1C A.2.1 puts the ship "
     "into a <strong>suspension procedure</strong> — not automatic. Automatic suspension "
     "(A.1.1–A.1.3) is for overdue periodical surveys.</li>", 1),

    ("QB4_A_CheatSheet.html",
     "Suspension → ALL RO-issued statutory certs invalid simultaneously + P&amp;I cover "
     "typically void",
     "Suspension → PR1C B.1.1 letter to Owner + Flag State; B.1.3 says <strong>certain</strong> "
     "statutory certs implicitly invalidated (not all). Class warranty breached, so cover "
     "may be prejudiced — PR1C says nothing about insurance", 1),

    ("QB4_A_CheatSheet.html",
     "ALL RO-issued statutory certs invalid simultaneously</span>",
     "PR1C B.1.3 — <strong>certain</strong> statutory certs implicitly invalidated, not "
     "all of them</span>", 1),

    # ---- P1: QB4_A#q9 notation table -------------------------------------
    ("QB4_A.html",
     "<td>Condition of Class (CoC)</td><td>YES — specific due date</td>"
     "<td>Class suspended if not met by due date</td>",
     "<td>Condition of Class (CoC)</td><td>YES — specific due date</td>"
     "<td><strong>Suspension procedure</strong> under PR1C A.2.1 if not met or postponed "
     "by agreement — not automatic</td>", 1),

    ("QB4_A.html",
     "Recommendation (Memo)</td><td>No — advisory</td><td>No class consequence; action as "
     "practical",
     "Recommendation (Memo)</td><td>Advisory</td><td>No due date attached, so no immediate "
     "class consequence — but PR1C covers <em>recommendations</em> going overdue as well as "
     "conditions of class, so do not call it consequence-free",
     1),

    # ---- P1: QB4_A#q9 Numbers, three-month window -------------------------
    ("QB4_A.html",
     "IACS PR1C — A.1 automatic suspension on overdue periodical surveys (three months, "
     "and not while under attendance),",
     "IACS PR1C — A.1 automatic suspension on overdue periodical surveys: A.1.1 Special "
     "(Renewal) from the certificate expiry date, A.1.2 Annual and A.1.3 Intermediate at "
     "three months past due and not while under attendance;", 1),

    # ---- P1: QB4_A#q9 false PR citations ---------------------------------
    ("QB4_A.html",
     "<span class=\"reg-code\">IACS PR No.1</span><span class=\"reg-desc\">Classification "
     "procedures; framework for survey and class maintenance</span>",
     "<span class=\"reg-code\">IACS PR 35</span><span class=\"reg-desc\">Procedure for "
     "Imposing and Clearing Recommendations/Conditions of Class — the instrument that "
     "governs how a CoC is imposed and cleared. <strong>Not PR No.1</strong>, which is "
     "Deleted in the IACS PR index.</span>", 1),

    ("QB4_A.html",
     "<span class=\"reg-code\">IACS PR No.3</span><span class=\"reg-desc\">Conditions of "
     "Class: types, imposition, timescales, suspension</span>",
     "<span class=\"reg-code\">IACS PR1A / PR1B</span><span class=\"reg-desc\">Transfer of "
     "class, and double or dual class — the neighbouring procedures in the PR1 family. "
     "<strong>Not PR No.3</strong>, which is Transparency of Classification and Statutory "
     "Information, a different subject.</span>", 1),

    ("QB4_A.html",
     "<li>The ship cannot legally trade internationally.</li>",
     "<li>The ship cannot trade: the certificates the flag Administration and port States "
     "rely on are affected, and no operator will move a vessel that is out of class. Say "
     "it that way rather than claiming every certificate has fallen.</li>", 1),

    # ---- P1: QB1_C#q6 ------------------------------------------------------
    ("QB1_C.html",
     "Failure to rectify the defect within the designated timeframe results in the "
     "automatic <strong>Suspension of Class</strong>, which invalidates the "
     "ship&#x27;s statutory certificates and voids hull and machinery "
     "(H\\&amp;M) insurance cover.",
     "If the defect is not rectified by the due date, or postponed by agreement, IACS PR1C "
     "A.2.1 makes the vessel&#x27;s class <strong>subject to a suspension procedure</strong> "
     "— it is not automatic, which is consistent with the point above that a Condition of "
     "Class does not itself warrant immediate suspension. Once class is suspended, the "
     "Society confirms it in writing to the Owner and the Flag State (B.1.1) and, for SOLAS "
     "ships, states that <em>certain</em> statutory certificates are implicitly invalidated "
     "(B.1.3). Hull &amp; Machinery and P&amp;I cover is written subject to a class "
     "warranty, so loss of class breaches it and cover may be prejudiced — PR1C contains no "
     "insurance provision, and cover is not automatically void.", 1),

    # ---- P2: QB4_E#q13 -----------------------------------------------------
    ("QB4_E.html",
     "If the ship loses its class certification due to an engine room defect, the statutory "
     "certificates are invalidated, effectively paralyzing the ship's legal standing to "
     "operate.",
     "If the ship loses class because of an engine room defect, IACS PR1C B.1.3 has the "
     "Society tell the Owner and the Flag State that <em>certain</em> statutory "
     "certificates are implicitly invalidated — enough to paralyse the ship's legal "
     "standing to operate, without claiming that every certificate falls at once.", 1),

    # ---- P2: QB1_F#q7, both copies ----------------------------------------
    ("QB1_F.html",
     "can lead to the withdrawal of the vessel's class notation, automatically invalidating "
     "the ship's insurance policies cover and giving Port State Control full legal grounds "
     "to detain the ship.",
     "can lead to suspension and ultimately, after six months under PR1C A.4.1, withdrawal "
     "of class — which breaches the class warranty in the ship's cover, so cover may be "
     "prejudiced, and gives Port State Control legal grounds to detain. See section 4 of "
     "this card for the full ladder; cover is not automatically void.", 2),
]


def main() -> int:
    pages: dict[str, str] = {}
    for name, _, _, _ in EDITS:
        if name not in pages:
            pages[name] = (QB / name).read_text(encoding="utf-8", newline="")

    errors, applied = [], 0
    for name, old, new, expect in EDITS:
        text = pages[name]
        n = text.count(old)
        if n != expect:
            errors.append("%s: anchor occurs %d times, expected %d: %.70s"
                          % (name, n, expect, old))
            continue
        pages[name] = text.replace(old, new)
        applied += n

    if errors:
        print("ABORTED - nothing written.")
        for e in errors:
            print("  " + e)
        return 1

    for name, text in pages.items():
        (QB / name).write_text(text, encoding="utf-8", newline="")
    print("Applied %d replacements across %d files." % (applied, len(pages)))
    for n in sorted(pages):
        print("  meoclass1/%s" % n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
