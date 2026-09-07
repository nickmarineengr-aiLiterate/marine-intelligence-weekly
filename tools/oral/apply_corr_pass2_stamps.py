#!/usr/bin/env python3
"""Version-stamp provenance for the six cards the Pass-2 batch corrected.

Run AFTER apply_corr_pass2.py.  The stamp is the candidate-facing record that
the teaching changed and why, so it is written as part of the correction rather
than left to the manifest alone -- a reader on the page can see what moved.

Each stamp advances the minor version and names the instrument that settled the
point, because the recurring failure on this card set was a confident claim with
no instrument behind it.

Anchors are asserted to occur exactly once; a drifted anchor aborts the run
before any file is written.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
QB = HERE.parent.parent / "meoclass1"

STAMPS = [
    ("QB4_E.html",
     "QB4_E · Q12 · v1.1 — corrected 5 Sep 2026: UR Z7 was given as the example UR &ldquo;for the Enhanced Survey Programme&rdquo;. UR Z7 is Hull Classification Surveys; the enhanced hull surveys of bulk carriers and oil tankers are the UR Z10 series (Z7 Rev.29 Corr.1, §1.1.3).",
     "QB4_E · Q12 · v1.2 — corrected 7 Sep 2026: the card taught eleven IACS Members in the 15-second answer, the 60-second answer and the CE tip, and hedged &ldquo;11 or 12 depending on&rdquo; Türk Loydu, while its own detail list below already carried all twelve. The Korean Register (KR) was missing from the 60-second list. IACS has 12 Members; TL was admitted 1 November 2023. A live authoring scaffold (&ldquo;Below are Q13-Q15 drafted in the exact required chat-ready format&rdquo;) and its rule were removed from the CE tip. · v1.1, 5 Sep 2026: UR Z7 was given as the example UR &ldquo;for the Enhanced Survey Programme&rdquo;. UR Z7 is Hull Classification Surveys; the enhanced hull surveys of bulk carriers and oil tankers are the UR Z10 series (Z7 Rev.29 Corr.1, §1.1.3)."),

    ("QB4_C.html",
     "QB4_C · Q5 · v1.1 — corrected 15 Jul 2026: class-suspension criminal penalty citation updated from MS Act 1958 Sec 334 to MS Act 2025, Part VI (Sec 125, 127)",
     "QB4_C · Q5 · v1.2 — corrected 7 Sep 2026: rebuilt on IACS PR1C Rev.7 (Nov 2024, applies from 1 January 2026), read this pass. Three defects closed. (1) The card blended the two suspension triggers: an overdue periodical survey suspends class automatically (A.1.1&ndash;A.1.3), whereas an overdue condition of class or continuous survey item is only &ldquo;subject to a suspension procedure&rdquo; (A.2.1, A.1.4). (2) &ldquo;All statutory certificates invalid&rdquo; overstated B.1.3, which says <em>certain</em> statutory certificates are implicitly invalidated, and omitted the B.1.1 written notification to Owner and Flag State. (3) Insurance was taught as universally void; PR1C contains no insurance provision at all, and the correct framing is breach of the policy&rsquo;s class warranty. The governing instrument was cited as IACS UR Z15, which is Hull, Structure, Equipment and Machinery Surveys of Mobile Offshore Drilling Units &mdash; a different subject; replaced by PR1C, and the A.4.1 six-month withdrawal rule added. · v1.1, 15 Jul 2026: class-suspension criminal penalty citation updated from MS Act 1958 Sec 334 to MS Act 2025, Part VI (Sec 125, 127)"),

    ("QB8_A.html",
     "QB8 · Q3 · v1.1 &mdash; 24 Aug 2026: added the freight-rate SOURCES limb (Baltic Exchange, container indices, Worldscale, brokers), asked at the Aug 2026 Kochi sitting",
     "QB8 · Q3 · v1.2 &mdash; corrected 7 Sep 2026: alliance currentness. The card named 2M and THE Alliance as current examples of a liner consortium. 2M ended in January 2025 and MSC now operates standalone; Hapag-Lloyd left THE Alliance in February 2025 to form Gemini Cooperation with Maersk, and the remainder (ONE, HMM, Yang Ming) rebranded as Premier Alliance. Ocean Alliance is the only pre-2025 grouping still intact. Regulation 906/2009 (the Consortia Block Exemption) was described as merely &ldquo;historical&rdquo;; it expired on 25 April 2024 and was not renewed, which is the fact an examiner can test. Three unsupported BAF claims removed: that the surcharge is &ldquo;managed by the engineering department&rsquo;s fuel tracking&rdquo;, that engine-room efficiency keeps costs &ldquo;within the baseline projections managed by the commercial BAF framework&rdquo;, and the Ever Given / SCFI record causal claim. · v1.1, 24 Aug 2026: added the freight-rate SOURCES limb (Baltic Exchange, container indices, Worldscale, brokers), asked at the Aug 2026 Kochi sitting"),

    ("QB5_A.html",
     "QB5_A · Q4 · v1.1",
     "QB5_A · Q4 · v1.2 &mdash; corrected 7 Sep 2026: the Numbers to Memorise block had lost the only two numbers it exists to teach &mdash; the list items rendered as &ldquo;&mdash; Maslow theory published&rdquo; and &ldquo;levels (pyramid sequence)&rdquo; with the 1943 and the 5 absent from the markup. Both restored. MLC Reg. 1.4 was cited as &ldquo;Recruitment / Fair Treatment&rdquo;; Reg. 1.4 is Recruitment and placement, and recognition and appraisal have no MLC hook. Maslow was described as &ldquo;strictly upward progression&rdquo;, which Maslow himself did not claim. The On My Vessel block was a fabricated first-person anecdote with invented timings (a 10-day port stay, 24 hours off every third day, morale recovering in 48 hours) resting on a non-existent &ldquo;Maslow Level 1&rarr;3 restoration effect&rdquo;; replaced with guidance to answer from the candidate&rsquo;s own ship."),

    ("QB3_A.html",
     "QB3 · Q5 · v1.1",
     "QB3 · Q5 · v1.2 &mdash; corrected 7 Sep 2026: the annual close-up survey of cargo hold side shell frames was taught as applying to bulk carriers and oil tankers generally, and cited to a tier-6 blog rendered to the candidate as &ldquo;[reference]&rdquo; &mdash; the only such placeholder in the corpus. The requirement belongs to single side skin bulk carriers under IACS UR Z10.2; double side skin bulk carriers sit under UR Z10.5 and oil tankers under UR Z10.1/Z10.4. Same proposition and same correction as QB3_B Q1."),

    ("QB10_B.html",
     "QB10_B · Q1 · v1.0",
     "QB10_B · Q1 · v1.1 &mdash; corrected 7 Sep 2026, verified propositions only. The lowering-speed figures were taught as &ldquo;min 1.0 m/s, max 1.3 m/s &mdash; replaces the old S = 0.4 + 0.02H formula&rdquo;. Resolution MSC.554(108), read this pass, does not replace the formula: LSA Code 6.1.2.8 as amended reads &ldquo;not less than &hellip; S = 0.4 + 0.02H, or 1.0, whichever is less&rdquo;, and 6.1.2.10 sets a 1.3 m/s maximum subject to the Administration accepting another. Corrected in both the formula block and Numbers to Memorise. The free-fall row said SOLAS III/33 &ldquo;removed the 5-knot headway test-launch requirement for ships &ge;20,000 GT&rdquo;; MSC.482(103) narrowed III/33.2 to <em>davit-launched</em> lifeboats on <em>cargo</em> ships of 20,000 GT and upwards, which still carry it. A raw &lt; in &ldquo;(e.g. &lt;150 GT&rdquo; was escaped to &amp;lt; as correct markup hygiene; nothing was being lost, and an earlier draft of this note claimed otherwise in error. MSC.559(108) is amendments to MSC.402(96), not the ventilation requirement itself, which is MSC.535(107); both now cited alongside MSC.554(108). MSC.482(103) added to the reference box. A self-dating &ldquo;it is now mid-2026&rdquo; replaced by the instrument date."),
]


def main() -> int:
    pages: dict[str, str] = {}
    for name, _, _ in STAMPS:
        if name not in pages:
            pages[name] = (QB / name).read_text(encoding="utf-8", newline="")

    errors, applied = [], 0
    for name, old, new in STAMPS:
        text = pages[name]
        n = text.count(old)
        if n != 1:
            errors.append("%s: stamp anchor occurs %d times, expected 1" % (name, n))
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
    print("Stamped %d cards." % applied)
    return 0


if __name__ == "__main__":
    sys.exit(main())
