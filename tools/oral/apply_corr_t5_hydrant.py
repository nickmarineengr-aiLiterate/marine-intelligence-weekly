"""Apply CORR-T5-HYDRANT-20260906: the fire-hydrant minimum-pressure family.

The family. A hard number is presented to the candidate under regulatory
wording - "minimum", "required", "mandatory" - for a quantity SOLAS actually
fixes, and the number is not SOLAS's. Tranche 4 found an invented 6 bar;
Tranche 5's N-3 found "4 to 6 Bar ... minimum ... required at the furthest
hydrant". The corpus-wide census found a third site asserting a "4.0 bar
minimum required at the highest hydrant", and a fourth stating the correct
figure with only one of its two limbs.

The governing text, held: SOLAS II-2/10.2.1.6 fixes the minimum pressure at the
hydrants with the two required pumps delivering simultaneously. For CARGO ships
that is 0.27 N/mm2 at 6,000 GT and upwards and 0.25 N/mm2 below 6,000 GT.
QB9_B#q5 already teaches exactly this, corrected 6 September 2026 - so the three
sites below did not merely lack support, they CONTRADICTED a corrected sibling
card in the same corpus. Internal contradiction against held source is what
promoted these out of the census and into a correction; a number that merely
looks large is not.

Scope discipline. The instruction is explicit that the card must not become a
new pressure lecture. Each edit states the governing figure, its scope and its
provision, and stops. The 6,000 GT limb is stated in both directions because a
single-limb version of a two-limb rule does not blur it - it is simply wrong for
every ship on the other side of the threshold, which is the same shape as the
MSC.535(107) lifeboat-ventilation defect.

The passenger-ship figures are deliberately NOT introduced. These are container
and cargo cards; importing a limb the card never addressed would be authoring,
not correcting.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
QB_ROOT = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import read_text  # noqa: E402

#: The one sentence every edit in this record has to make true.
GOVERNING = ("SOLAS II-2/10.2.1.6 minimum pressure at the hydrants with the two "
             "required pumps delivering simultaneously &mdash; for cargo ships "
             "<strong>0.27 N/mm&sup2;</strong> at 6,000 GT and upwards and "
             "<strong>0.25 N/mm&sup2;</strong> below")

EDITS = [
    # ---- N-3, authorised -------------------------------------------------
    dict(
        id="N-3",
        file="QB2_A.html",
        anchor="q8",
        count=1,
        old='<li><strong>4 to 6 Bar:</strong> Typical minimum operational pressure '
            'range required at the furthest hydrant to ensure effective deck '
            'monitor throw heights.</li>',
        new='<li><strong>0.27 / 0.25 N/mm&sup2;:</strong> ' + GOVERNING +
            '. A higher pressure quoted for deck-monitor throw is a design or '
            'operational target, not a SOLAS minimum.</li>',
        was='a 4-6 bar range asserted as the required minimum at the furthest '
            'hydrant - roughly double the SOLAS floor, and unsourced',
    ),
    # ---- the same false proposition, a card the finding never named -------
    dict(
        id="E-2",
        file="QB2_H.html",
        anchor="q2",
        count=1,
        old='deplete the fire main pressure below the 4.0 bar minimum required at '
            'the highest hydrant.',
        new='deplete the fire main below the ' + GOVERNING + '.',
        was='a 4.0 bar "minimum required at the highest hydrant", contradicting '
            'the corrected QB9_B#q5',
    ),
    # ---- correct figure, one limb missing --------------------------------
    dict(
        id="E-3",
        file="QB2_B.html",
        anchor="q18",
        count=1,
        old='<li><strong>0.27 N/mm²:</strong> The mandatory minimum pressure that '
            'must be maintained at the highest deck hydrants while monitors are '
            'running.</li>',
        new='<li><strong>0.27 / 0.25 N/mm&sup2;:</strong> ' + GOVERNING +
            '. Quoting 0.27 alone is wrong for a ship under 6,000 GT.</li>',
        was='the 6,000 GT threshold was absent, so the figure was stated as if '
            'it governed every cargo ship',
    ),
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    problems = []
    for e in EDITS:
        path = QB_ROOT / e["file"]
        text = read_text(path)
        n = text.count(e["old"])
        if n != e["count"]:
            if text.count(e["new"]) > 0:
                print("  %-5s %-14s %-4s ALREADY APPLIED" % (e["id"], e["file"],
                                                             e["anchor"]))
                continue
            problems.append("%s: expected %d occurrence(s) in %s, found %d"
                            % (e["id"], e["count"], e["file"], n))
            continue
        print("  %-5s %-14s %-4s was: %s" % (e["id"], e["file"], e["anchor"],
                                             e["was"]))
        if args.apply:
            text = text.replace(e["old"], e["new"])
            path.write_bytes(text.encode("utf-8").replace(b"\r\n", b"\n"))

    if problems:
        print("\nREFUSED:")
        for p in problems:
            print("  " + p)
        return 1
    print("\n%s: %d numeric-standard corrections"
          % ("APPLIED" if args.apply else "DRY RUN", len(EDITS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
