#!/usr/bin/env python3
"""Pass-2 remediation round 1 -- closing what the independent review found.

The clean-context verifier returned three P1s inside the declared Pass-2 scope.
All three are upheld; each was checked against evidence rather than accepted.

  R1-A  QB4_C#q5 CE Oral Tip still said "invalidates our statutory
        certificates", unqualified. Every other layer was corrected. The CE tip
        is the sentence the card instructs the candidate to SAY, so this was
        the worst possible layer to miss. Stop-Work bullet and Numbers layer
        corrected with it.

  R1-B  QB3_A#q5 dropped two qualifications the source record makes. QB3_B#q1,
        which CORR-PASS2-CLOSEUP-SCOPE cites as its whole authority, says the
        annual survey "CAN REQUIRE" close-up of "at least 25% of cargo hold
        side shell frames ... in a forward cargo hold and one other selected
        hold", and records that the requirement "is also age-conditioned"
        with the band unverified. The propagation kept the population and lost
        the extent, the hold scope, the modality and the age condition -- and
        the record claimed it "asserts nothing that record did not" while
        asserting an UNCONDITIONAL rule. Restored to match, source gap and all.

  R1-C  QB10_B#q1 published a false claim about its own history: that an
        unescaped "<" had been deleting rendered teaching. It had not. A
        browser emits "<" literally unless the next character is a letter, so
        "<150 GT" always rendered fine. Verified in a real browser engine:
        the pre-fix string renders complete, including both dates. The escaping
        is kept as correct hygiene; the claim goes.

  R1-D  QB3_B#q1's Numbers layer still carried "(bulk carriers/tankers)" --
        the exact over-broad scope that card's own body and reg-box refute.
        Bounded same-defect propagation, and a seventh declared card.

  R1-E  QB10_B#q1's bold lead-in still read "Free-fall lifeboat test-launch
        exemption" over a body that says the requirement was narrowed, not
        abolished. The bold label is the layer a skimming candidate reads.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
QB = HERE.parent.parent / "meoclass1"

EDITS = [
    # ---- R1-A --------------------------------------------------------------
    ("QB4_C.html",
     "Operating under either status invalidates our statutory certificates and "
     "exposes us to direct criminal liability under Part VI of the Merchant Shipping "
     "Act, 2025.",
     "The trigger matters: an overdue survey suspends class automatically, an overdue "
     "condition of class puts us into a suspension procedure. Either way the Society "
     "notifies the Owner and the Flag State in writing, and under PR1C B.1.3 that "
     "letter states that <em>certain</em> statutory certificates are implicitly "
     "invalidated — not all of them — and trading on that basis exposes us to direct "
     "criminal liability under Part VI of the Merchant Shipping Act, 2025."),

    ("QB4_C.html",
     "as operating without valid statutory certificates or insurance exposes the "
     "senior officers to personal prosecution and severe legal penalties.",
     "because trading with statutory certificates that PR1C B.1.3 treats as implicitly "
     "invalidated, and with the class warranty in our H&amp;M and P&amp;I cover "
     "breached, exposes the senior officers to personal prosecution and severe legal "
     "penalties."),

    ("QB4_C.html",
     "A.1 automatic suspension on overdue periodical surveys",
     "A.1 automatic suspension on overdue periodical surveys — and note the windows: "
     "A.1.2 and A.1.3 bite three months past the due date, and not while the vessel is "
     "under attendance for completion",
     ),

    # ---- R1-B --------------------------------------------------------------
    ("QB3_A.html",
     "<li>Annual close-up survey of cargo hold side shell frames — <strong>single side "
     "skin bulk carriers only</strong>, under IACS UR Z10.2. On those ships the annual "
     "survey itself includes close-up examination of cargo hold side shell frames and "
     "their end attachments, so it is not held over to the special survey. It is "
     "<strong>not</strong> a general bulk carrier requirement and it is <strong>not</strong> "
     "an oil tanker requirement: double side skin bulk carriers sit under UR Z10.5, and "
     "oil tankers under UR Z10.1/Z10.4. Worth flagging to the yard and the attending "
     "surveyor if it falls due inside a drydock window.</li>",

     "<li><strong>Annual Survey Close-Up (single side skin bulk carriers):</strong> the "
     "annual survey itself — not just the special survey — <strong>can require</strong> "
     "a close-up examination of at least <strong>25% of cargo hold side shell frames</strong>, "
     "their lower end attachments and adjacent shell plating, in a forward cargo hold "
     "and one other selected hold, with any thickness measurement found necessary "
     "reported. This is an IACS UR Z10.2 requirement, and Z10.2 governs single side "
     "skin bulk carriers — double side skin bulk carriers are Z10.5, oil tankers are "
     "Z10.1/Z10.4 — so it is <strong>not</strong> an oil tanker requirement. The "
     "requirement is also <strong>age-conditioned</strong>; this card does not state "
     "the age band, because it could not be verified against Z10.2 directly — check "
     "the applicable clause before quoting a threshold in an oral. Worth flagging to "
     "the yard and the attending surveyor if it falls due inside a drydock window. "
     "Same requirement, same wording, as QB3_B Q1.</li>"),

    # ---- R1-D --------------------------------------------------------------
    ("QB3_B.html",
     "<strong>25%</strong> — annual close-up survey extent of cargo hold side shell "
     "frames (bulk carriers/tankers), forward hold + one other selected hold.",
     "<strong>25%</strong> — annual close-up survey extent of cargo hold side shell "
     "frames, <strong>single side skin bulk carriers only</strong> (UR Z10.2; not oil "
     "tankers), forward hold + one other selected hold, and age-conditioned."),

    # ---- R1-C --------------------------------------------------------------
    ("QB10_B.html",
     "An unescaped &lt; in &ldquo;(e.g. &lt;150 GT&rdquo; was silently deleting about 150 "
     "characters of rendered teaching, including two entry-into-force dates.",
     "A raw &lt; in &ldquo;(e.g. &lt;150 GT&rdquo; was escaped to &amp;lt; as correct "
     "markup hygiene; nothing was being lost, and an earlier draft of this note claimed "
     "otherwise in error.",
     ),

    # ---- R1-E --------------------------------------------------------------
    ("QB10_B.html",
     "<strong>Free-fall lifeboat test-launch exemption:</strong>",
     "<strong>Free-fall lifeboats released from the 5-knot headway launch requirement "
     "— which davit-launched lifeboats keep:</strong>"),
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
    print("Applied %d remediation edits across %d files." % (applied, len(pages)))
    for n in sorted(pages):
        print("  meoclass1/%s" % n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
