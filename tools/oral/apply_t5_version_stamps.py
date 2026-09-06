"""Stamp candidate-facing correction provenance on the seven corrected cards.

WHICH CARDS GET A STAMP, AND WHY THE OTHER 44 DO NOT
----------------------------------------------------
A `q-version` stamp is the candidate's record of what changed in the answer
they are reading. The seven cards below had a PROPOSITION change: a superseded
publication taught as current, a footer citing it as verification authority, or
a hydrant pressure that was not SOLAS's.

The 44 cards in CORR-T5-DDCASCADE-20260906 did not. That repair removed
duplicated RENDERING - every proposition a candidate could read before is still
there, exactly once instead of two to five times. Stamping "this card changed"
on 44 cards whose teaching did not change would make the stamp mean less
everywhere it appears, and the instruction is explicit that this pass performs
no cleanup beyond the defect.

QB2_H#q2 is the exception inside the exception: its empty deep-dive promise was
structural, but its 4.0 bar figure was a proposition, so it is stamped for the
latter.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
QB_ROOT = HERE.parent.parent / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import read_text  # noqa: E402

BMP = ("BMP5 taught as the current publication; migrated to <strong>BMP "
       "Maritime Security, 1st Edition (2025) as updated in 2026</strong>, "
       "which replaced BMP5 (2018), BMP West Africa and the Global Counter "
       "Piracy Guidance &mdash; see QB4_H Q13")
HYD = ("SOLAS II-2/10.2.1.6 governs the minimum pressure at the hydrants with "
       "the two required pumps delivering simultaneously: for cargo ships "
       "0.27 N/mm&sup2; at 6,000 GT and upwards and 0.25 N/mm&sup2; below")

STAMPS = [
    ("QB1_F.html", "q10", "QB1_F · Q10 · v1.0",
     "QB1_F &middot; Q10 &middot; v1.1 &mdash; corrected 6 Sep 2026: the "
     "reg-box row read &ldquo;Best Management Practices (BMP5)&rdquo; and "
     "described it as current industry-standard guidance. " + BMP +
     ". This card had never been reached by any earlier BMP sweep."),
    ("QB4_H.html", "q6", "QB4_H · Q6 · v1.0",
     "QB4_H &middot; Q6 &middot; v1.1 &mdash; corrected 6 Sep 2026: the "
     "reg-box row cited BMP5 for electronic signature management in an HRA. "
     + BMP + ". A sibling card in the same file as Q2, which three earlier "
     "BMP sweeps corrected without opening this one."),
    ("QB5_B.html", "q14", "QB5_B · Q14 · v1.0",
     "QB5_B &middot; Q14 &middot; v1.1 &mdash; corrected 6 Sep 2026: the "
     "answer body taught &ldquo;BMP5 engineering measures&rdquo; and the "
     "reg-box row was headed &ldquo;BMP5 / Industry Best Management "
     "Practices&rdquo;. " + BMP + "."),
    ("QB2_A.html", "q8", "QB2_A · Q8 · v2.0",
     "QB2_A &middot; Q8 &middot; v2.1 &mdash; corrected 6 Sep 2026: Numbers to "
     "Memorise gave &ldquo;4 to 6 Bar&rdquo; as the minimum operational "
     "pressure <em>required</em> at the furthest hydrant &mdash; roughly "
     "double the regulatory floor, and carrying no source. " + HYD +
     ". A higher figure quoted for deck-monitor throw is a design or "
     "operational target, not a SOLAS minimum."),
    ("QB2_B.html", "q18", "QB2_B · Q18 · v1.1",
     "QB2_B &middot; Q18 &middot; v1.2 &mdash; corrected 6 Sep 2026: Key "
     "Numbers gave 0.27 N/mm&sup2; as &ldquo;the mandatory minimum "
     "pressure&rdquo; with no tonnage threshold, so it read as governing every "
     "cargo ship. " + HYD + " &mdash; quoting 0.27 alone is wrong for a ship "
     "under 6,000 GT, not merely incomplete."),
    ("QB2_H.html", "q2",
     "v1.0 · Finalised — pending Nixon final sign-off before gating",
     "v1.1 &mdash; corrected 6 Sep 2026: the card warned against depleting the "
     "fire main below a &ldquo;4.0 bar minimum required at the highest "
     "hydrant&rdquo;, which is not a SOLAS figure and contradicted QB9_B Q5. "
     + HYD + ". An empty deep-dive element promising seven sections was also "
     "removed. Prior: v1.0 &middot; Finalised &mdash; pending Nixon final "
     "sign-off before gating"),
]

#: QB4_H#q2 already carries a long, correct v1.5 stamp. It is EXTENDED rather
#: than replaced, because that stamp is the audit trail of four prior
#: corrections and rewriting it would destroy evidence to record evidence.
Q2_TAIL = ("; corrected 6 Sep 2026: the source-confidence footer still offered "
           "&ldquo;BMP5 Section 5 (mscio.eu)&rdquo; as an authority this card "
           "had been verified against, five days after the body removed that "
           "carry-over as unverifiable &mdash; the footer now cites the held "
           "BMP Maritime Security, 1st Edition (2025) as updated June 2026")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    problems = []
    for fname, anchor, old, new in STAMPS:
        path = QB_ROOT / fname
        text = read_text(path)
        if new in text:
            print("  %-14s %-4s ALREADY STAMPED" % (fname, anchor))
            continue
        if text.count(old) != 1:
            problems.append("%s#%s: stamp anchor found %d time(s)"
                            % (fname, anchor, text.count(old)))
            continue
        print("  %-14s %-4s stamped" % (fname, anchor))
        if args.apply:
            path.write_bytes(text.replace(old, new)
                             .encode("utf-8").replace(b"\r\n", b"\n"))

    # QB4_H#q2 - extend, never replace.
    path = QB_ROOT / "QB4_H.html"
    text = read_text(path)
    if Q2_TAIL in text:
        print("  %-14s %-4s ALREADY STAMPED" % ("QB4_H.html", "q2"))
    else:
        marker = "; unsupported named-company security-system claim removed"
        i = text.find(marker)
        if i < 0:
            problems.append("QB4_H#q2: v1.5 stamp anchor not found")
        else:
            end = text.find("</span>", i)
            print("  %-14s %-4s stamp EXTENDED" % ("QB4_H.html", "q2"))
            if args.apply:
                text = text[:end] + Q2_TAIL + text[end:]
                path.write_bytes(text.encode("utf-8").replace(b"\r\n", b"\n"))

    if problems:
        print("\nREFUSED:")
        for p in problems:
            print("  " + p)
        return 1
    print("\n%s: 7 cards" % ("APPLIED" if args.apply else "DRY RUN"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
