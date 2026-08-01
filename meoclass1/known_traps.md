# Known Traps & Standing Corrections — Marine Intelligence Weekly

Master reference of verified-correct facts that have previously been drafted wrong
(by Gemini, by source material, or by first-pass Claude verification). Every new
QB/notes batch should be checked against this list before HTML is built — not
just recalled from memory.

Each entry has a `GREP:` line. The health check script only auto-scans entries
where `GREP:` gives an exact wrong phrase that is unambiguous out of context
(safe to flag anywhere it appears). Entries where the "wrong" version is a
general term that's also legitimately used correctly are marked `GREP: SKIP` —
those stay manual-review-only, checked during the verification pass, not by
the automated scanner.

---

### 1. FAL Form 8
FAL Convention has exactly **7 numbered forms**. "FAL Form 8" is a common
examiner trap referring to the **IHR 2005 Maritime Declaration of Health**,
which is not a FAL form at all.
GREP: FAL Form 8

### 2. PSC detention action code
**Action code 30 = detention.** "Action code 15" for detention is wrong.
GREP: action code 15

### 3. IOPC 1992 Fund limit — incomplete figure
Standard limit is 203 million SDR; conditional step-up under Art. 4(4)(b)
raises it to 300.74 million SDR. Needs a manual read to catch (context-
dependent), not a clean grep target.
GREP: SKIP

### 4. AECS definition
AECS = "Assessment, Examination and Certification of Seafarers" (IMO Model
Course 3.12), aimed at MMD examiners / RO surveyors — NOT a seafarer
simulator/assessment course.
GREP: SKIP

### 5. Resolution currency
Never cite a resolution number without checking whether it has been
superseded. Known case: A.1185(33) is superseded by A.1206(34) for PSC
procedures.
GREP: A.1185(33)

### 6. Merchant Shipping Act — superseded
Merchant Shipping Act 2025 (Act No. 24 of 2025) came into force 15 March
2026, repealing the 1958 Act. DG Shipping renamed DGMA. Flag content that
cites "Merchant Shipping Act, 1958" as current law.
GREP: Merchant Shipping Act, 1958

### 7. ME-GA engine line — discontinued
MAN Energy Solutions discontinued the ME-GA line in November 2024. Flag if
described as an active/current product line.
GREP: SKIP

### 8. MASS Code dates
Adopted MSC 111 (May 2026); effective 1 July 2026. Do not confuse adoption
date with entry-into-force date.
GREP: SKIP

### 9. IMO Net-Zero Framework status
Adoption was postponed at the October 2025 extraordinary MEPC session; next
expected at MEPC 85 (Oct/Nov 2026). Flag if stated as already adopted.
GREP: Net-Zero Framework has been adopted

### 10. Canadian Arctic + Norwegian Sea ECA sulphur date
0.10% sulphur limit takes effect 1 March 2027, not earlier.
GREP: SKIP

### 11. IMO GFI reference value vs FuelEU Maritime baseline — cross-track contamination
The IMO GFI (GHG Fuel Intensity, MEPC 83 / MARPOL Annex VI Chapter 5) reference
value is 93.3 gCO2eq/MJ (2008 fleet-average, well-to-wake). FuelEU Maritime
(EU Regulation 2023/1805) is a separate regulation using the same units and
WtW logic but its own 91.16 gCO2eq/MJ baseline (2020 reference). These are
two distinct regulatory tracks (IMO global vs EU regional) that share
terminology ("GFI"/"GHG intensity") and units, making them easy to conflate.
Caught in QB6_E (Q2, Q3): the file used 91.16 as if it were the IMO GFI
reference and computed reduction targets (2%/6%/14.5%) off the wrong
baseline — those percentages are actually FuelEU's own schedule, not IMO's.
Flagged by a candidate (Rathesh) via annotated screenshot correction.
GREP: SKIP (91.16 is legitimate when correctly attributed to FuelEU Maritime;
the trap is only when it's presented as the IMO GFI reference — needs manual
context check, not a safe auto-grep)

### 12. CLC 1992 scope — mineral oil only, not animal/vegetable oil
CLC 1992 (Civil Liability Convention) applies only to **persistent
hydrocarbon mineral oil** — crude oil, heavy fuel oil, lubricating oil.
It does NOT cover non-mineral oils such as whale oil or other animal/
vegetable oils, regardless of persistence — those are classed as
hazardous and noxious substances and fall under the **HNS Convention
1996, as revised by the 2010 HNS Protocol**, instead. Note the 2010 HNS
Protocol is not yet in force (confirmed entry into force 29 November
2027); until then such incidents fall back on national law, LLMC
limitation, and P&I cover — not a CLC/Fund-style regime. Caught in QB1_A
(Q5, CLC), which listed "whale oil" alongside crude/HFO/lube oil as if
covered by CLC. Flagged by a candidate (Vivek) via screenshot correction.
GREP: lubricating oil, whale oil

---

### 13. Garbage Record Book threshold — 400 GT is obsolete, now 100 GT
MARPOL Annex V Regulation 10.3 was amended by **Resolution MEPC.360(79)**
(adopted 16 Dec 2022, in force **1 May 2024**), lowering the Garbage
Record Book (GRB) threshold from ≥ 400 GT to **≥ 100 GT** — converging
it with the existing Garbage Management Plan (GMP) threshold, which was
already ≥ 100 GT and is unchanged. Any content stating the GRB applies
only to ships ≥ 400 GT, or explicitly separating GMP-at-100GT from
GRB-at-400GT as two different thresholds, is citing the pre-2024
position. The 400 GT GRB figure should only appear with clear historical
framing (e.g. "formerly 400 GT, now 100 GT since 1 May 2024"). GRB
document format itself is unaffected and remains per Resolution
MEPC.277(70). Caught in QB3_C (Q1, MARPOL Annex V garbage amendments) —
error appeared in the 15-Second Answer, 60-Second Answer, comparison
table, CE Oral Tip, and Common CE Failures (the failures line had it
fully inverted, flagging the correct 100 GT answer as the candidate
error). Flagged by Nixon via screenshot correction.
GREP: Garbage Record Book tracking is required at 400, Record Book for ships ≥ 400 GT, Record Book (Parts I and II) for all ships ≥ 400 GT

---

### 14. PSCO qualification pipeline — 10 Flag State Inspections, not 60
The PSC Officer qualification pipeline (Simon Sir Notes, Part 3, card n13,
"PSC Officer — Qualification Criteria") stated the candidate must complete
at least **60 Flag State Inspections** as an authorised FSI Officer before
being eligible for supervised PSC inspections. The correct figure per the
DGS Standard Operating Procedure for Port State Control and Flag State
Inspection (referencing Merchant Shipping Notice No. 9 of 2013) is **10
Flag State Inspections** — the same figure as the FSI-officer qualification
threshold itself (card n12), which the PSCO pipeline builds on. The
remainder of the pipeline (6 months as FSI officer, 1 year as flag
surveyor, 10 supervised PSC inspections, 2/year re-qualification) was
already correct and unchanged. Flagged by a candidate (Rathesh) via the
site correction form (Topic 62, "Simon Sir Notes — Pages 51–75", 26 Jul
2026). Verified against primary source:
https://www.dgshipping.gov.in/WriteReadData/userfiles/file/sop_psc__fsi141016.pdf
GREP: 60 Flag State Inspections, 60 FSIs
Note: the corrected page intentionally retains the phrase "60 Flag State
Inspections" once, inside the in-page `.correction-note` block that
describes the old error ("Prior revision incorrectly stated 60 Flag State
Inspections... the correct figure is 10 Flag State Inspections"). This is a
negation-context false positive per the pattern below — do not treat it as
a resurfaced error without checking the surrounding sentence.

---

### 15. IMO convention adoption — quorum is 1/3 present, not 2/3
The "How an IMO Convention Enters into Force — 5 Steps" flow (Simon Sir
Notes, Part 3, card n18, "International Legislation Hierarchy & EIF
Process") stated Step 2 (Adoption) as "Assembly conference: 2/3 quorum
present; 2/3 vote in favour." The quorum figure is wrong. The correct
requirement is a quorum of **at least 1/3 of contracting governments
present** to hold the vote, with **at least 2/3 of those present** voting
in favour for adoption — the same 1/3–2/3 figures already correctly
verified elsewhere in this platform's content (Engineering Management
Notes Part 2, SOLAS Article VIII / MARPOL Article 16 tacit-acceptance
mnemonic). Do not conflate this adoption-quorum figure with the separate
tacit-acceptance objection threshold (1/3 of states or 50% of world
tonnage), which is a different stage of the process. Flagged by a
candidate via screenshot correction, 27 Jul 2026.
GREP: 2/3 quorum present

---

### 16. Pipe-delimited markdown tables leaked into live HTML — formatting standard, not a factual error
Six comparative tables in QB2_A (container thicknesses, tanker types, tonnage
fees, watertight vs weathertight boundaries, inclinometer types, bulk cargo
failure modes) plus 13 more across QB1_B (1), QB1_F (7), QB1_G (10), and
QB3_H (1) were rendered as raw markdown-style pipe rows inside `<p>` tags
(e.g. `| Col A | Col B | | --- | --- | | val | val |`) instead of real
`<table>` markup. This is a legacy artifact from earlier AI-assisted drafting
sessions, not a regulatory/factual error — the content itself was correct.
On mobile (the primary subscriber device) these wrap unpredictably and lose
column alignment entirely, defeating the purpose of a comparison table.
Flagged by a candidate via screenshot, 29 Jul 2026 (Nixon relay). All 19
instances converted to real `<table>` markup with the site's standard
`.answer-body table/th/td` CSS (added to QB1_F and QB1_G, which had no table
CSS at all prior to this fix); QB3_H matched using its own rem-based CSS
convention. Fixed and pushed 2026-07-29.
This is a **formatting standard**, not a wrong-phrase fact — no single GREP
phrase applies. A dedicated automated check (`check_pipe_table_format()`)
was added to `qb_health_check.py` instead, scanning for the separator-row
pattern `\|\s*-{2,}\s*\|` (any dash count/spacing) across all QB files and
Engineering Management Notes/WA files, run in the same daily 03:00 UTC job.
GREP: SKIP

The daily `qb_health_check.py` trap scan (`check_known_traps()`) currently
flags a `GREP:` phrase on any occurrence, including when the surrounding
sentence is correctly citing the old/wrong term in order to supersede,
repeal, or debunk it (e.g. "the old Merchant Shipping Act, 1958... has been
replaced by", "supersedes A.1185(33)", "IMO does not designate it 'FAL Form
8'"). Verified 2026-07-19: every trap hit in that day's run (MS Act 1958 x6
files, A.1185(33) x4 files, FAL Form 8 x1 file) was a false positive of
this kind — correctly-framed corrections, not resurfaced errors.

Before treating a future flag as confirmed, check whether the matched line
also contains a negation/supersession marker, e.g.:
- "superseded by" / "supersedes"
- "replaced by" / "replaces"
- "repealed"
- "not... but" / "not the... but"
- "does not designate" / "is not"
- "formerly" / "now succeeded by" / "since replaced by"

If one of these markers appears in the same sentence as the trap phrase,
treat it as likely-correct usage and verify manually rather than flagging
as an error. `qb_health_check.py` should ideally skip-list lines matching
these markers (or downgrade them to a "review" tier instead of "error") to
cut noise in future runs — this is a suggested script enhancement, not yet
implemented.

---

### 17. Form E (SEQ Certificate supplement) does not list fire-fighting equipment
Form E — “Record of Equipment for Cargo Ship Safety Equipment Certificate,” per the SOLAS 74/78 Appendix — has exactly **three sections**: (1) Details of Life-Saving Appliances, (2) Equivalent Arrangements, and (3) Details of Navigational Systems and Equipment. There is **no fire-fighting equipment section**. Multiple QB answers (QB3_A Q15 and its embedded/standalone cheat sheets, QB8_A, QB8_B) incorrectly stated or implied that Form E itemises fitted fire-fighting equipment (extinguishers, fixed FIFI systems, portable water monitors, etc.) alongside LSA. This conflates the *scope of the SEQ survey* (which does cover FFA, under SOLAS Ch II-2 / FSS Code) with the *content of Form E* (which does not). Correct position: FFA compliance is attested on the certificate's own text; the itemised fitted/quantity/location record for FFA lives in the ship's Fire Control Plan and is maintained through the PMS, not on Form E. Flagged by Nixon, 30 Jul 2026; corrected across QB3_A.html, QB3_A_CheatSheet.html, QB8_A.html, QB8_B.html same session.
GREP: SKIP

This trap is a negation-context minefield for the health checker — the corrected sentences legitimately contain “Form E”, “fire”, and “list/cover/record” together (to correctly state the *exclusion*). A literal GREP for “Form E” + “fire” would flag every corrected sentence as a false positive, so this entry is SKIP-tagged for manual verification-pass review rather than daily auto-scan. If a future auto-scan enhancement is built for this, it should only flag co-occurrence patterns where “Form E” is the stated subject of a listing/inclusion verb applied to fire-fighting equipment (e.g. “Form E ... lists ... fire-fighting”), not sentences containing a negation marker (“NOT”, “does not”, “not part of”) in the same clause.

### 18. BMP5 already addresses weapon-of-war threats (missile/WBIED/mine) via the "safe muster point" provision — it is not piracy-only

A candidate suggested BMP5 has "only addressed piracy" (Gulf of Aden/Red Sea/Arabian Sea/West Africa) and has "not exclusively addressed" state-actor/missile/torpedo/warhead security threats. This is not accurate: BMP5 Section 5 already requires that where the threat/risk assessment identifies a possibility of hull breach on or below the waterline (missile, WBIED, mine), a **safe muster point above the waterline** must be identified and selected with the likely blast path in mind — a provision distinct from, and complementary to, the citadel (which is the correct response to a boarding/hijack threat, not a blast/weapon-of-war threat). This distinction, carried forward into BMP-MS (2025), was present in the QB4_H Q2 answer's citadel-only hardening section but the separate safe-muster-point provision was missing, which is the gap the candidate's question actually points to — not an absence of BMP coverage. The candidate's separate point about a BIMCO-family supplementary document for the Strait of Hormuz is broadly correct in substance (the actual document is the ICS/BIMCO/INTERCARGO/INTERTANKO/IMCA/OCIMF "Industry Guidance on the Safe Management of Vessel Transit through the Strait of Hormuz," May 2026, not literally titled "Supplementary Regional Maritime Security Guidance") and was already cited in QB4_H Q2. Corrected: added the safe-muster-point vs. citadel distinction to QB4_H.html Q2 (answer-body, reg-box, CE tip trap line, deep-dive trap/casualty items, source-confidence note) and to QB4_H_cheatsheet.html rows 2 and 11. Flagged by candidate Rathesh via Nixon, 1 Aug 2026.
GREP: SKIP

This entry's GREP was originally set to "safe muster point" — the CORRECT phrase we added — not an error phrase to detect resurfacing of the candidate's original wrong claim. That misuse of the convention caused the health checker to flag QB4_H.html, QB4_H_cheatsheet.html, and unrelated files that legitimately use the phrase "safe muster point" (QB4_B.html, QB1_FG_CheatSheet.html) as "KNOWN TRAP resurfaced" every run — a false positive on our own fix. Corrected to SKIP on 2026-08-01 during the follow-up pass. There is no single wrong-phrase string to grep for here (the original error was an omission, not a specific incorrect sentence), so SKIP is the correct tag, matching Entry 16/17's precedent for the same underlying issue.

### 19. QB4_H Q2 Hormuz content expanded — routing dispute, hardening purpose split, AIS/coastal-state clarification

Follow-up to Entry 18: after the safe-muster-point correction, the candidate (Rathesh, via Nixon) asked five specific follow-up questions on 1 Aug 2026 — (1) why citadel and safe muster point can't be the same, (2) whether vessel hardening is still required, (3) which authorities to inform, (4) AIS management "as per coastal state requirements," and (5) re-routing on a coastal-state-specified lane. Verification found: (1)/(2)/(3) were already adequately covered or answerable from existing content; (4) the candidate's framing was corrected — AIS policy is Master/company/flag discretion, NOT coastal-state-mandated, and QB4_H Q2 already stated this correctly, so the reg-box AIS line was reinforced with an explicit "Not coastal-state-mandated" note rather than changed; (5) was a genuine, significant content gap — since April 2026 Iran has redrawn the Strait of Hormuz TSS and directs vessels to IRGC-designated corridors only (the "Tehran Toll Booth" near Qeshm/Larak), threatening a "decisive response" against non-compliant vessels; Oman separately announced an IMO-coordinated alternate route which Iran rejected, and a vessel was reportedly struck shortly after using it; IMO's March 2026 position is that transit passage under UNCLOS Part III cannot be unilaterally redirected by a coastal state, which Iran (a non-ratifier of UNCLOS) disputes. QB4_H Q2 did not previously cover this routing dispute at all. Corrected: added a new "Route Selection & the Coastal-State Routing Dispute" subsection to the answer-body, a new orange-box "Route selection — redrawn TSS dispute" live-update item (replacing the now-outdated "both lanes have had incidents" framing), a new UNCLOS Part III reg-box entry, an AIS coastal-state clarification in the During-Transit bullet and orange box, a hardening-purpose split (anti-boarding vs. anti-blast/kinetic, citing ISPS Level 3/sandbagging/ballistic PPE from the May 2026 Industry Guidance), a new trap question, updated Common CE Failures/Numbers/Casualty Link/On My Vessel items, and an updated source-confidence note. Version bumped v1.2 → v1.3.
GREP: SKIP

Same convention fix as Entry 18: "Tehran Toll Booth" is correct content we just added, not a wrong phrase to catch resurfacing — SKIP-tagged for the same reason.

---

## How to use this file

- Before building any new QB batch or notes part, check the drafted answer
  text against every entry above (not just the auto-greppable ones).
- If a Gemini draft or source text contains a flagged wrong phrasing, it is
  removed and corrected — not relabelled or softened.
- This file is a living document. Every time a correction is made post-build
  (caught by Nixon, a subscriber, or a re-verification pass), add a new
  numbered entry here in the same session: what was wrong, the correct
  version, and a `GREP:` line (exact phrase, or `SKIP` if too generic to
  auto-scan safely).
- The QB health check script (`qb_health_check.py`) auto-scans all live QB
  HTML daily for every non-SKIP `GREP:` phrase — see `check_known_traps()`.
  SKIP entries stay in this file as a manual verification-pass checklist.

---

## Change log

| Date | Entry added | Source |
|---|---|---|
| 2026-07-16 | Initial 10 entries | Compiled from Claude memory / prior correction sessions |
| 2026-07-18 | Entry 11: IMO GFI vs FuelEU Maritime baseline | Candidate (Rathesh) annotated-screenshot correction on QB6_E |
| 2026-07-19 | Entry 12: CLC scope — mineral oil only (whale oil trap) | Candidate (Vivek) screenshot correction on QB1_A |
| 2026-07-25 | Entry 13: GRB threshold now 100 GT, not 400 GT (MEPC.360(79)) | Nixon screenshot correction on QB3_C |
| 2026-07-27 | Entry 15: IMO convention adoption quorum is 1/3, not 2/3 | Candidate screenshot correction on simon-notes-p3 |
| 2026-07-29 | Entry 16: Pipe-delimited markdown tables → real `<table>` markup (formatting standard, not a fact error); added `check_pipe_table_format()` to health check | Candidate screenshot correction on QB2_A, repo-wide grep found 4 more affected files |
| 2026-07-30 | Entry 17: Form E does not list fire-fighting equipment (QB3_A, cheat sheets, QB8_A, QB8_B) | Nixon correction (SEQ Q15 review) |
| 2026-08-01 | Entry 18: BMP5 already covers weapon-of-war threats via safe muster point (distinct from citadel) — added to QB4_H Q2 + cheat sheet | Candidate (Rathesh) via Nixon |
| 2026-08-01 | Entry 19: QB4_H Q2 expanded — Hormuz routing dispute (Iran redrawn TSS), hardening purpose split, AIS/coastal-state clarification | Candidate (Rathesh) via Nixon |
