#!/usr/bin/env python3
"""Terminal closure C -- the seven QB10_B#q1 propositions declared open in Pass 2.

Dispositions, one per proposition, no broad rewrite:

  P1 MASS Code            VERIFIED_PRIMARY   - MSC.595(111) adopted MSC 111 (May
                          2026), non-mandatory, effective 1 Jul 2026, EBP. The
                          card is correct; nothing changed.
  P2 STCW-F               QUALIFY            - the CONVENTION has been in force
                          since 2012. What entered force on 1 Jan 2026 is the
                          2022 amendments and the new STCW-F Code.
  P3 Polar Code extension QUALIFY + SOURCE_GAP - the substance and both dates
                          verify, and the population is wider and more precise
                          than "fishing vessels and pleasure yachts". The
                          resolution PAIRING could not be verified, so it is
                          removed rather than asserted.
  P4 MEPC.392(82)         VERIFIED_PRIMARY + QUALIFY - adopted 4 Oct 2024,
                          in force 1 Mar 2026, SOx/PM enforced 1 Mar 2027. The
                          card's 2027 date is RIGHT; what it lacked was the
                          1 Mar 2026 entry into force, whose absence invites
                          exactly the conflation that nearly caused a wrong
                          "correction" here.
  P5 LRIT                 DEFER_NON_MATERIAL - already correctly hedged as
                          "approved in principle, pending formal adoption";
                          now explicitly as-at dated so it cannot silently rot.
  P6 MSC 112 expectations DEFER_NON_MATERIAL - future events, same treatment.
  P7 Bulk Jupiter         REMOVE_UNSUPPORTED - the causal attribution has no
                          source. Two further errors in the same clause: the
                          ship is BULK JUPITER, and she was lost to bauxite
                          LIQUEFACTION, not a cargo shift.
"""
from __future__ import annotations

import pathlib
import sys

QB = pathlib.Path(__file__).resolve().parents[2] / "meoclass1"

EDITS = [
    # ---- P2 STCW-F ------------------------------------------------------
    ("<strong>STCW-F Convention and Code:</strong> entered force 1 Jan 2026,",
     "<strong>STCW-F &mdash; the 2022 amendments and the new STCW-F Code:</strong> in force "
     "1 Jan 2026. Say it precisely: the <em>Convention</em> itself (STCW-F 1995) has been in "
     "force since 2012; what arrived on 1 Jan 2026 is the amendments and the Code,", 1),

    # ---- P3 Polar Code --------------------------------------------------
    ("<strong>Polar Code extension to non-SOLAS ships &mdash; SOLAS Ch. XIV / Polar Code "
     "Part I-A, MSC.532(107)/MSC.538(107):</strong> fishing vessels and pleasure yachts "
     "operating in polar waters brought under interim safety requirements, retroactive to "
     "existing non-SOLAS ships by 1 Jan 2027.",
     "<strong>Polar Code extension to non-SOLAS ships &mdash; SOLAS Ch. XIV / Polar Code "
     "Part I-A:</strong> the population is wider than &ldquo;fishing vessels and yachts&rdquo; "
     "and worth learning exactly &mdash; fishing vessels of <strong>24 m LOA and above</strong>, "
     "pleasure yachts of <strong>300 GT and above not engaged in trade</strong>, and cargo "
     "ships of <strong>300 GT and above but below 500 GT</strong>. New regulations 9-1 "
     "(voyage planning) and 11-1 (safety of navigation) of Polar Code Part I-A apply. Ships "
     "constructed on or after 1 Jan 2026 comply from the start of polar operation; ships "
     "constructed before that date must comply by <strong>1 Jan 2027</strong>. <em>The "
     "adopting resolution is not stated here</em>: the MSC.532(107)/MSC.538(107) pairing this "
     "card previously carried could not be verified, and an unverified number is worse than "
     "none.", 1),

    # ---- P4 MEPC.392(82) -------------------------------------------------
    ("Canadian Arctic and Norwegian Sea designated (MEPC.392(82)); 0.10% sulphur enforcement "
     "begins 1 March 2027.",
     "Canadian Arctic and Norwegian Sea designated by <strong>MEPC.392(82)</strong>, adopted "
     "4 October 2024 and <strong>in force 1 March 2026</strong>. Keep the two dates apart, "
     "because they are one year and one trap apart: the areas become ECAs on 1 March 2026, "
     "and <strong>SOx/PM &mdash; the 0.10% limit &mdash; is enforced from 1 March 2027</strong>.",
     1),

    # ---- P7 Bulk Jupiter, both layers ------------------------------------
    ("<em>Why:</em> traces directly to the bulk carrier <em>Jupiter</em> bauxite cargo-shift "
     "casualty, where investigators had no recorded roll/stability data to reconstruct events.",
     "<em>Why:</em> the general case for recorded roll data is that a stability casualty is "
     "hard to reconstruct without it &mdash; the loss of the bulk carrier <em>Bulk Jupiter</em> "
     "(2 January 2015, off Vung Tau, 18 of 19 crew lost) is the standard illustration, and "
     "she was lost to bauxite <strong>liquefaction</strong>, not a cargo shift. No source "
     "traces this amendment <em>directly</em> to that casualty, so do not claim the causal "
     "link in an oral.", 1),

    ("The electronic inclinometer/VDR requirement traces directly to the bulk carrier "
     "<em>Jupiter</em> bauxite cargo-shift casualty, where post-incident investigators lacked "
     "recorded roll/stability data to reconstruct the sequence of events &mdash; a gap this "
     "amendment closes.",
     "The <em>Bulk Jupiter</em> (2 January 2015, off Vung Tau; 18 of 19 crew lost) is the "
     "casualty to reach for on recorded stability data. She was lost to bauxite "
     "<strong>liquefaction</strong> &mdash; not a cargo shift &mdash; and the investigation "
     "found an average cargo moisture content of 21.3%. Use her to explain <em>why</em> "
     "recorded roll data matters; do <strong>not</strong> claim the inclinometer amendment "
     "traces directly to her, because no source establishes that.", 1),

    # ---- P5 / P6 as-at dating -------------------------------------------
    ("<p><em>Note &mdash; LRIT free access for coastal States:</em> updated status &mdash;",
     "<p><em>Note &mdash; LRIT free access for coastal States (status as at September 2026 "
     "&mdash; re-check before any sitting, this is a moving item):</em>", 1),

    ("subject to approval at MSC 111 and formal adoption at MSC 112 (December 2026)",
     "subject to formal adoption at MSC 112 (December 2026, still a future session as at "
     "September 2026)", 1),
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
