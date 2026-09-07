#!/usr/bin/env python3
"""Apply the Pass-2 known-defect remediation batch.

Six declared defect families, each closed against a source read in this pass:

  P2-IACS      QB4_E#q12   IACS membership is 12, not "11 or 12"; KR restored
  P2-PR1C      QB4_C#q5    suspension/withdrawal rebuilt on IACS PR1C Rev.7
  P2-ALLIANCE  QB8_A#q3    2M/THE Alliance retired; BAF ownership corrected
  P2-HUMAN     QB5_A#q4    lost numbers restored; MLC 1.4 misattribution closed
  P2-CLOSEUP   QB3_A#q5    blog citation removed; UR Z10.2 scope propagated
  P2-AMEND     QB10_B#q1   lowering speed, III/33.2, MSC.559 custody, unescaped <

Every replacement is asserted to occur EXACTLY ONCE in its target file.  A
replacement whose anchor has drifted aborts the whole run before any file is
written, so a partial batch cannot reach disk.

Line endings are preserved per file: QB4_E.html is CRLF, the rest are LF, and
the two multi-line replacements are built against each file's own EOL.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
QB = REPO / "meoclass1"

# ---------------------------------------------------------------------------
# P2-IACS -- QB4_E#q12
#   Source: IACS is a 12-Member association (ABS BV CCS CRS DNV IRClass KR LR
#   ClassNK PRS RINA TL).  The card's own detail list already carried all
#   twelve including KR, while its 15s, 60s and CE tip taught eleven -- the
#   card contradicted itself on its single load-bearing fact.
# ---------------------------------------------------------------------------
IACS = [
    ("IACS (International Association of Classification Societies) currently consists of 11 full member societies.  The major ones include Lloyd's Register (LR), Bureau Veritas (BV), DNV, American Bureau of Shipping (ABS), ClassNK, RINA, and the Indian Register of Shipping (IRClass).  Note: The Russian Maritime Register (RMRS) was expelled, and IACS now has 11 or 12 members depending on the inclusion of the newest member, Türk Loydu (TL).",
     "IACS (International Association of Classification Societies) has <strong>12</strong> full Member societies: ABS, BV, CCS, CRS, DNV, IRClass, <strong>KR</strong>, LR, ClassNK, PRS, RINA and Türk Loydu (TL).  Türk Loydu was admitted on 1 November 2023 as the twelfth Member; the Russian Maritime Register of Shipping (RMRS) had its membership terminated in March 2022 and is not a Member.  There is no “11 or 12” to hedge over — the current figure is twelve."),

    ("As of 2026, the members are: American Bureau of Shipping (ABS), Bureau Veritas (BV), China Classification Society (CCS), Croatian Register of Shipping (CRS), DNV (Norway), Indian Register of Shipping (IRClass), Lloyd's Register (LR), Nippon Kaiji Kyokai (ClassNK), Polski Rejestr Statków (PRS), Registro Italiano Navale (RINA), and Türk Loydu (TL).",
     "The <strong>12</strong> Members are: American Bureau of Shipping (ABS), Bureau Veritas (BV), China Classification Society (CCS), Croatian Register of Shipping (CRS), DNV (Norway), Indian Register of Shipping (IRClass), <strong>Korean Register (KR)</strong>, Lloyd's Register (LR), Nippon Kaiji Kyokai (ClassNK), Polski Rejestr Statków (PRS), Registro Italiano Navale (RINA), and Türk Loydu (TL) — count them off and you should reach twelve."),

    ("<h4>TL – Türk Loydu (Turkey - admitted recently)</h4>",
     "<h4>TL – Türk Loydu (Turkey — admitted 1 November 2023, the twelfth and most recent Member)</h4>"),

    ("\"Sir, noting recent updates, Russian Maritime Register (RMRS) was expelled, and Türk Loydu (TL) has been admitted, bringing the list to 11 current members.\"",
     "\"Sir, the Russian Maritime Register of Shipping had its membership terminated in March 2022 and Türk Loydu was admitted in November 2023, so IACS stands at twelve Members today.\" The one candidates drop is the Korean Register."),
]

#: Live authoring scaffold and its trailing rule, left in the candidate-facing
#: CE tip.  Matched with the file's own EOL -- QB4_E.html is CRLF.
IACS_SCAFFOLD_OLD = (
    "This proves you read current maritime news.</p>{E}"
    "          <p>------------------------</p>{E}"
    "          <p>Below are Q13-Q15 drafted in the exact required chat-ready format, using quote blocks and collapsible sections.</p></div>"
)
IACS_SCAFFOLD_NEW = "This proves you read current maritime news.</p></div>"

# ---------------------------------------------------------------------------
# P2-PR1C -- QB4_C#q5
#   Source: IACS PR1C Rev.7 (Nov 2024), read this pass from IACS's own hosting.
#   A.1.1-A.1.3 automatic suspension on overdue periodical surveys; A.1.4 and
#   A.2.1 a suspension PROCEDURE for continuous survey items and conditions of
#   class; A.4.1 withdrawal after six months; B.1.1-B.1.3 written notification
#   to Owner and Flag State stating that CERTAIN statutory certificates are
#   implicitly invalidated.  PR1C contains no insurance provision at all.
#   UR Z15 is Mobile Offshore Drilling Unit surveys, not this subject.
# ---------------------------------------------------------------------------
PR1C = [
    ("Both invalidate statutory certificates and void insurance.",
     "Under IACS PR1C the Society confirms either in writing to the Owner and the Flag State, and for SOLAS ships that letter states that <em>certain</em> statutory certificates are implicitly invalidated — not all of them. PR1C says nothing whatever about insurance."),

    ("<strong>Suspension of class</strong> occurs when a vessel fails to rectify a Condition of Class within the specified window or misses a mandatory survey. The class certificate is paused, automatically rendering all statutory certificates invalid and voiding insurance cover under standard class warranties. Class is reinstated once a satisfactory survey is completed.",
     "<strong>Suspension of class</strong> is governed by IACS PR1C, and its two triggers do not work the same way. An <em>overdue periodical survey</em> — Special (Renewal), Annual or Intermediate — makes the Class Certificate invalid and suspends classification <strong>automatically</strong> (PR1C A.1.1–A.1.3). An <em>overdue condition of class</em>, and an overdue continuous survey item, instead make the vessel <strong>subject to a suspension procedure</strong> (A.2.1, A.1.4) — that is not automatic, and blending the two is the commonest error on this question. The Society must confirm the suspension in writing to the Owner and to the Flag State (B.1.1), and for SOLAS ships that letter states that <em>certain</em> statutory certificates are implicitly invalidated (B.1.3) — PR1C does not say all of them are, and it makes no statement about insurance at all. Class is reinstated on satisfactory completion of the overdue survey, but the vessel is disclassed from the date of suspension until the date of reinstatement."),

    ("<li>Statutory certificates issued by the Recognized Organisation (RO) on behalf of the flag state automatically become invalid.</li>",
     "<li>PR1C B.1.3: for vessels to which SOLAS applies, the Society&#x27;s notification letter to Owner and Flag State is to state that <strong>certain</strong> statutory certificates are implicitly invalidated by the suspension or withdrawal. Which ones depends on the certificate and on the flag Administration. Do not tell an examiner that every statutory certificate falls at once — PR1C deliberately says &quot;certain&quot;.</li>"),

    ("<li>Protection and Indemnity (P&amp;I) and Hull &amp; Machinery (H\\&amp;M) insurance underwriters will freeze or void coverage due to a breach of the mandatory class warranty.</li>",
     "<li>Insurance: PR1C contains no insurance provision at all, and there is no universal rule that cover becomes void. What is true is that Hull &amp; Machinery and P&amp;I cover is normally written subject to a <em>class warranty</em> — an express policy term that the vessel is and remains in class — so loss of class is typically a breach of that warranty, and the consequence is whatever the policy and its governing law provide. Say &quot;our class warranty is breached and cover may be prejudiced&quot;, not &quot;insurance is void&quot;.</li>"),

    ("<li><strong>Triggers:</strong> Operating a vessel under suspension beyond the allowed time limits without resolving the defects; failing to pay class fees; shifting to another classification society; or when a ship is structurally compromised beyond repair or sent for recycling.</li>",
     "<li><strong>Triggers:</strong> PR1C A.4.1 gives the hard rule — when class has been suspended for <strong>six (6) months</strong> because of overdue surveys and/or conditions of class, the class <em>is to be withdrawn</em>. A longer suspension period may be granted where the vessel is not trading: lay-up, awaiting disposition after a casualty, or under attendance for reinstatement. Withdrawal also follows on transfer to another society, non-payment of class fees, or where the ship is compromised beyond repair or sent for recycling.</li>"),

    ("<span class=\"reg-code\">IACS UR Z15</span><span class=\"reg-desc\">Outlines standardized international procedures for class suspension and withdrawal.</span>",
     "<span class=\"reg-code\">IACS PR1C, Rev.7 (Nov 2024)</span><span class=\"reg-desc\">Procedure for Suspension and Reinstatement or Withdrawal of Class in Case of Surveys or Conditions of Class Going Overdue — the instrument that actually governs this answer. A.1.1–A.1.3 automatic suspension for overdue periodical surveys; A.1.4 and A.2.1 a suspension <em>procedure</em> for overdue continuous survey items and conditions of class; A.4.1 withdrawal after six months suspended; B.1.1–B.1.3 written notification to Owner and Flag State stating that certain statutory certificates are implicitly invalidated. Rev.7 applies from 1 January 2026 and the clause lettering is unchanged from Rev.6. <strong>Not UR Z15</strong> — that is Hull, Structure, Equipment and Machinery Surveys of Mobile Offshore Drilling Units, a different subject entirely.</span>"),

    ("<p>IACS UR Z15:** Defines the harmonized procedural requirements for the suspension and withdrawal of class. · Merchant Shipping Act, 2025, Sec 125/127 (Part VI):** Establishes severe personal criminal penalties",
     "<p><strong>IACS PR1C Rev.7</strong> (Nov 2024, applies from 1 January 2026): the harmonised procedural requirements for suspension, reinstatement and withdrawal of class — A.1 automatic suspension on overdue periodical surveys, A.2.1 a suspension procedure on an overdue condition of class, A.4.1 withdrawal after six months, B.1 notification to Owner and Flag State. · <strong>Merchant Shipping Act, 2025, Sec 125/127 (Part VI):</strong> Establishes severe personal criminal penalties"),

    ("<strong>Answer:</strong> No, sir. The moment class is suspended, the statutory certificates are legally invalidated, and insurance cover may be voided. The Master must immediately notify the Flag Administration and the coastal state authorities to arrange for safe routing or emergency anchorage at the nearest convenient port of refuge where repairs can be surveyed.",
     "<strong>Answer:</strong> No, sir — but let me take the trigger first. If this is an overdue periodical survey the suspension is automatic under PR1C A.1; an overdue condition of class instead puts us into a suspension procedure under A.2.1. Once class is suspended, the Society confirms it in writing to the Owner and the Flag State, and under B.1.3 that letter states that certain statutory certificates are implicitly invalidated — so I would not assume we can complete the voyage on the strength of the certificates in the folder. The Master must notify the Flag Administration and the coastal State, and we would seek the nearest convenient port where the overdue item can be surveyed. On insurance I would say our class warranty is breached and cover may be prejudiced, rather than claiming that cover is void."),

    ("resulting in the automatic invalidation of their statutory certificates and leaving the crew exposed on structurally compromised hulls.",
     "putting them into suspension and, under PR1C B.1.3, implicitly invalidating certain of their statutory certificates — leaving the crew exposed on structurally compromised hulls."),
]

# ---------------------------------------------------------------------------
# P2-ALLIANCE -- QB8_A#q3
#   The alliance landscape changed in Jan/Feb 2025: 2M ended, Hapag-Lloyd left
#   THE Alliance for Gemini with Maersk, and the remainder rebranded Premier.
#   CBER 906/2009 expired 25 April 2024 and was not renewed.
# ---------------------------------------------------------------------------
ALLIANCE = [
    ("A <strong>liner consortium</strong> is a modern operational alliance (e.g., 2M, Ocean Alliance)",
     "A <strong>liner consortium</strong> is a modern operational alliance (as at 2026: Gemini Cooperation, Ocean Alliance, Premier Alliance)"),

    ("<p>A liner consortium (or mega-alliance, such as the Ocean Alliance or THE Alliance) is a modern structure for global liner operations.</p>",
     "<p>A liner consortium (or mega-alliance) is a modern structure for global liner operations. Know the <em>current</em> line-up, because it changed in February 2025 and a stale name is an easy mark to lose: <strong>Gemini Cooperation</strong> (Maersk and Hapag-Lloyd, run as a hub-and-spoke network), <strong>Ocean Alliance</strong> (CMA CGM, COSCO, Evergreen, OOCL — the only pre-2025 grouping still intact, and extended to 2032) and <strong>Premier Alliance</strong> (ONE, HMM, Yang Ming — the rebranded remainder of THE Alliance after Hapag-Lloyd left for Gemini). <strong>2M no longer exists</strong>: the Maersk/MSC vessel-sharing agreement ended in January 2025, and MSC now operates standalone. Naming 2M or THE Alliance as current dates you by more than a year.</p>"),

    ("<li><strong>BAF:</strong> The standard abbreviation for the Bunker Adjustment Factor, the fuel cost surcharge managed by the engineering department&#x27;s fuel tracking.</li>",
     "<li><strong>BAF:</strong> Bunker Adjustment Factor — a commercial surcharge levied on the shipper to pass through movement in bunker <em>prices</em>. It is set and administered by the carrier&#x27;s commercial department on the carrier&#x27;s own published formula; there is no IMO or industry-standard BAF formula, and the engine department neither sets nor manages it. What the engine room supplies is the consumption data, not the surcharge.</li>"),

    ("<li><strong>Regulation 906/2009:</strong> The historical EU antitrust block exemption that permitted operational container consortia to share space, provided their combined market share remained within strict limits.</li>",
     "<li><strong>Regulation 906/2009 — the Consortia Block Exemption Regulation (CBER):</strong> the EU antitrust block exemption that permitted operational container consortia to share space provided their combined market share stayed within defined limits. The European Commission decided in October 2023 not to renew it, and it <strong>expired on 25 April 2024</strong>. Consortia serving EU trades are now self-assessed under the general Article 101 rules, with no dedicated exemption. Quote it as lapsed, not as current law.</li>"),

    ("This helps keep voyage costs within the baseline projections managed by the commercial BAF framework.&quot;</em>",
     "That protects the fuel budget the commercial department is working to.&quot;</em> Do not go further and claim the engine room influences the BAF: the BAF is a surcharge the commercial side sets from bunker prices, not a cost baseline the engine room manages."),

    ("This extra fuel use cuts directly into the carrier&#x27;s margins, as it cannot be recovered retrospectively through the standard BAF surcharge, impacting operational efficiency.",
     "That extra fuel is a cost to the carrier, and a BAF does not recover it: the BAF passes through movement in bunker <em>prices</em>, not extra consumption caused by the ship&#x27;s own schedule recovery."),

    ("The sudden restriction in available vessel space across major alliances led to an unprecedented increase in container spot rates, with the SCFI index hitting historic highs.",
     "The blockage took effective capacity out of the market for weeks, and spot rates rose sharply. Be careful with the causal claim, because an examiner may press it: container spot rates were already at extraordinary levels through 2021 on pandemic demand and port congestion, and the SCFI&#x27;s all-time peak came in early 2022. Suez was one contributor to an already stretched market, not the sole cause of the record."),
]

# ---------------------------------------------------------------------------
# P2-HUMAN -- QB5_A#q4
#   The two numbers this card exists to teach had been lost from the HTML: the
#   list items read "- Maslow theory published" and "- levels (pyramid
#   sequence)" with the 1943 and the 5 gone.  MLC Reg. 1.4 is Recruitment and
#   placement, not fair treatment.  The "On My Vessel" block was a fabricated
#   first-person anecdote with invented timings and an invented "Maslow
#   restoration effect".
# ---------------------------------------------------------------------------
HUMAN_NUMBERS_OLD = (
    "<h5>Numbers to Memorise</h5><ul>{E}"
    "<li>— Maslow theory published</li>{E}"
    "</ul>{E}"
    "<ul>{E}"
    "<li>levels (pyramid sequence — bottom to top)</li>{E}"
    "</ul>"
)
HUMAN_NUMBERS_NEW = (
    "<h5>Numbers to Memorise</h5><ul>{E}"
    "<li><strong>1943</strong> — Maslow&#x27;s paper &quot;A Theory of Human Motivation&quot;, in which the five-level model was set out</li>{E}"
    "<li><strong>5</strong> levels, bottom to top — Physiological → Safety → Social/Belonging → Esteem → Self-Actualisation</li>{E}"
    "</ul>"
)

HUMAN = [
    ("<td>STCW (competency recognition), MLC Reg. 1.4 (Recruitment / Fair Treatment)</td>",
     "<td>STCW (competency recognition and certification). <strong>No MLC hook here</strong> — MLC Reg. 1.4 is <em>Recruitment and placement</em>, not fair treatment, and recognition, appraisal and promotion are management practice rather than an MLC requirement</td>"),

    ("Maslow&#x27;s model is strictly upward progression.</p>",
     "Alderfer builds regression into the model explicitly. Put it that way round rather than claiming Maslow is a strictly upward progression: Maslow himself wrote that the hierarchy is not rigid, that needs are partially rather than wholly satisfied, and that the order can reverse in individual cases — and the pyramid drawing is a later teaching device, not Maslow&#x27;s own.</p>"),

    ("<p>On my Maersk vessel, the clearest Maslow application I observed was during a prolonged port stay (10 days) with continuous cargo operations in a tropical port. The engine team was on reduced manning, minimal shore leave, and high workload. Morale dropped visibly. Applying Maslow: Levels 1 (rest) and 3 (social contact) were being denied. My response was to restructure the duty roster to give each officer 24 hours&#x27; off-duty every third day, arrange a team meal ashore, and communicate an end-date to the intensive work period. Motivation recovered within 48 hours — entirely consistent with Maslow&#x27;s Level 1→3 restoration effect.</p>",
     "<p>Answer this from your own ship, and keep it to what you actually did. A usable shape: name a period when the engine team&#x27;s rest or shore contact was genuinely squeezed — a long cargo port stay, a heavy repair window, reduced manning — identify which Maslow level that pressed on, say what you changed within your own authority (the duty roster, the order of work, getting an end-date communicated to the team), and say how you checked whether it had worked. Do not invent figures: any number of days off-duty or recovery time you quote must be one from your own ship that you can defend under follow-up. And there is no &quot;Maslow restoration effect&quot; in the literature to appeal to — the model diagnoses where the unmet need sits, it does not predict how quickly morale returns.</p>"),
]

# ---------------------------------------------------------------------------
# P2-CLOSEUP -- QB3_A#q5
#   The same proposition D01-S02 corrected on QB3_B#q1, propagated here and
#   still resting on a tier-6 blog link rendered to the candidate as
#   "[reference]" -- the only such placeholder in the corpus.
# ---------------------------------------------------------------------------
CLOSEUP = [
    ("<li>Annual Survey Close-Up Extension (bulk carriers/oil tankers) — a close-up examination of at least 25% of cargo hold side shell frames (forward hold + one other selected hold) is mandated at the annual survey itself, not just at special survey; worth flagging to the yard/surveyor if it falls due during a drydock window. <a href=\"https://marinegyaan.com/checklist-for-annual-and-intermediate-surveys-of-ships/\" target=\"_blank\" rel=\"noopener\">[reference]</a></li>",
     "<li>Annual close-up survey of cargo hold side shell frames — <strong>single side skin bulk carriers only</strong>, under IACS UR Z10.2. On those ships the annual survey itself includes close-up examination of cargo hold side shell frames and their end attachments, so it is not held over to the special survey. It is <strong>not</strong> a general bulk carrier requirement and it is <strong>not</strong> an oil tanker requirement: double side skin bulk carriers sit under UR Z10.5, and oil tankers under UR Z10.1/Z10.4. Worth flagging to the yard and the attending surveyor if it falls due inside a drydock window.</li>"),
]

# ---------------------------------------------------------------------------
# P2-AMEND -- QB10_B#q1
#   Verified families only.  Sources read this pass: MSC.482(103) (SOLAS
#   III/33.2 and II-1/25-1, eff. 1 Jan 2024), MSC.554(108) (LSA 6.1.2.8 and
#   6.1.2.10 lowering speed, eff. 1 Jan 2026) and MSC.559(108) (amendments to
#   MSC.402(96), ventilation testing, eff. 1 Jan 2026).
# ---------------------------------------------------------------------------
AMEND = [
    ("SOLAS III/33 removed the 5-knot headway test-launch requirement for ships ≥20,000 GT. <em>Why:</em> studies showed the test added no meaningful data on dynamic loads at that speed while adding real risk to crew during drills — removing an unnecessary hazard.",
     "resolution MSC.482(103) replaced SOLAS III/33.2, which now reads that <em>on cargo ships of 20,000 gross tonnage and upwards, <strong>davit-launched</strong> lifeboats shall be capable of being launched, utilizing painters where necessary, with the ship making headway at speeds up to 5 knots in calm water</em>. The effect is to confine the 5-knot headway launch capability to davit-launched lifeboats, so free-fall lifeboats on those ships no longer carry it. State it that way round — the requirement was <strong>narrowed, not abolished</strong>: a davit-launched boat on a 25,000 GT bulker still has it. The same resolution added SOLAS II-1/25-1, the water level detectors above."),

    ("(e.g. <150 GT, fishing vessels)",
     "(e.g. &lt;150 GT, fishing vessels)"),

    ("<p class=\"formula\"><strong>Lifeboat lowering speed (post-2026): min 1.0 m/s, max 1.3 m/s</strong> — replaces the old S = 0.4 + 0.02H formula (H = davit head to lightest seagoing draft), which varied unhelpfully with loading condition.</p>",
     "<p class=\"formula\"><strong>Lifeboat lowering speed — LSA Code 6.1.2.8 and 6.1.2.10, as replaced by resolution MSC.554(108):</strong> the speed at which a fully loaded survival craft or rescue boat is lowered to the water shall not be less than <em>S</em> = 0.4 + 0.02<em>H</em>, <strong>or 1.0 m/s, whichever is less</strong> (<em>S</em> in metres per second; <em>H</em> the height in metres from the davit head to the waterline with the ship at the lightest sea-going condition). The maximum lowering speed shall be <strong>1.3 m/s</strong>, and the Administration may accept a maximum other than 1.3 m/s having regard to the design of the craft, the protection of its occupants from excessive forces, and the strength of the launching arrangements. In force 1 January 2026, applying to life-saving appliances installed on or after that date. <strong>The formula is not abolished</strong> — 1.0 m/s is a ceiling on the formula-derived minimum, not a replacement for it, and &quot;the formula is gone&quot; is the trap here.</p>"),

    ("<li><strong>1.0–1.3 m/s:</strong> new lifeboat lowering speed range (replacing the old H-dependent formula).</li>",
     "<li><strong>Lowering speed — MSC.554(108), LSA Code 6.1.2.8 / 6.1.2.10:</strong> minimum is <em>S</em> = 0.4 + 0.02<em>H</em> or 1.0 m/s, whichever is less; maximum 1.3 m/s unless the Administration accepts another. The formula still stands.</li>"),

    ("<div class=\"reg-item\"><span class=\"reg-code\">MSC.559(108) / MSC.560(108)</span><span class=\"reg-desc\">Lifeboat ventilation testing regime; STCW SASH training (Table A-VI/1-4) — eff. 1 Jan 2026.</span></div>",
     "<div class=\"reg-item\"><span class=\"reg-code\">MSC.482(103)</span><span class=\"reg-desc\">SOLAS II-1/25-1 water level detectors on multiple-hold cargo ships, and the replacement of SOLAS III/33.2 confining the 5-knot headway launch capability to davit-launched lifeboats — adopted 13 May 2021, eff. 1 Jan 2024.</span></div><div class=\"reg-item\"><span class=\"reg-code\">MSC.535(107) / MSC.554(108) / MSC.559(108) / MSC.560(108)</span><span class=\"reg-desc\">Four separate instruments that candidates blur together. <strong>MSC.535(107)</strong> — LSA Code ventilation means, ventilation openings and their means of closing for totally enclosed lifeboats. <strong>MSC.554(108)</strong> — LSA Code amendments including release-gear reset and the lowering-speed paragraphs 6.1.2.8/6.1.2.10. <strong>MSC.559(108)</strong> — amendments to the Requirements for maintenance, thorough examination, operational testing, overhaul and repair of lifeboats and rescue boats, launching appliances and release gear (resolution MSC.402(96)), adding the annual thorough examination and operational testing of the ventilation system that MSC.535(107) introduced. <strong>MSC.560(108)</strong> — STCW SASH training, Table A-VI/1-4. All eff. 1 Jan 2026.</span></div>"),

    ("it is now mid-2026 and that entire package is already in force",
     "that package entered into force on 1 January 2026 and has been in force ever since, so date it from the instrument rather than from your own sense of what is recent"),
]

# ---------------------------------------------------------------------------

FAMILIES = [
    ("P2-IACS", "QB4_E.html", IACS),
    ("P2-PR1C", "QB4_C.html", PR1C),
    ("P2-ALLIANCE", "QB8_A.html", ALLIANCE),
    ("P2-HUMAN", "QB5_A.html", HUMAN),
    ("P2-CLOSEUP", "QB3_A.html", CLOSEUP),
    ("P2-AMEND", "QB10_B.html", AMEND),
]

#: Multi-line replacements, built against each file's own EOL.
EOL_FAMILIES = [
    ("P2-IACS", "QB4_E.html", IACS_SCAFFOLD_OLD, IACS_SCAFFOLD_NEW),
    ("P2-HUMAN", "QB5_A.html", HUMAN_NUMBERS_OLD, HUMAN_NUMBERS_NEW),
]


def eol_of(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def main() -> int:
    pages: dict[str, str] = {}
    for name in {f[1] for f in FAMILIES}:
        pages[name] = (QB / name).read_text(encoding="utf-8", newline="")

    errors: list[str] = []
    applied = 0

    for family, page, pairs in FAMILIES:
        text = pages[page]
        for old, new in pairs:
            n = text.count(old)
            if n != 1:
                errors.append("%s %s: anchor occurs %d times, expected 1: %.90s"
                              % (family, page, n, old))
                continue
            text = text.replace(old, new, 1)
            applied += 1
        pages[page] = text

    for family, page, old_t, new_t in EOL_FAMILIES:
        text = pages[page]
        e = eol_of(text)
        old = old_t.replace("{E}", e)
        new = new_t.replace("{E}", e)
        n = text.count(old)
        if n != 1:
            errors.append("%s %s: EOL anchor occurs %d times, expected 1" % (family, page, n))
            continue
        pages[page] = text.replace(old, new, 1)
        applied += 1

    if errors:
        print("ABORTED - nothing written. %d anchor failure(s):" % len(errors))
        for e in errors:
            print("  " + e)
        return 1

    for name, text in pages.items():
        (QB / name).write_text(text, encoding="utf-8", newline="")

    print("Applied %d replacements across %d files." % (applied, len(pages)))
    for name in sorted(pages):
        print("  meoclass1/%s" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
