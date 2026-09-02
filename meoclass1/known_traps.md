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

Scope note (2026-08-13): the narrow grep above only catches content that
spells out "1958" — it missed QB5_C_B Q5, which cited "Merchant Shipping
Act (India), Section 358" and "DG Shipping" without the year, both stale.
Fixed there (v1.2): reg citation updated to "Merchant Shipping Act, 2025
(India)" with a caveat to verify the exact 2025 section number before
citing verbatim (not independently confirmed — search did not surface
the 2025 Act's renumbered casualty-investigation section), and both
"DG Shipping" mentions updated to "DGMA". A repo-wide content search for
bare "DG Shipping" (no "1958" nearby) returned ~678 hits across ~68
meoclass1 files — too broad and context-dependent for a safe auto-GREP
(many may be legitimate historical references to pre-March-2026
circulars/orders issued under the old name). This needs a dedicated
manual audit pass, not a blanket find-replace — flagged for a future
session, not yet actioned beyond QB5_C_B Q5.

Follow-up (2026-08-13, same day): Nixon requested the full repo-wide
audit be scoped and actioned. Classified all 508 "DG Shipping" mentions
(88 files) into three buckets: (a) 266 hits in point-in-time historical
exam-paper content (pastpapers/, solved-qp/written-sample files) —
correctly left as-is, since "DG Shipping" was the accurate name during
those exam sittings; (b) 36 hits that are dated, named historical
circulars/notices/orders (e.g. "DG Shipping Engineering Circular 02 of
2021", "DGS Order 06/2020") — correctly left as-is, since that was the
real issuer name at time of publication and renaming would misquote the
document title; (c) 175 genuinely stale present-tense/generic-authority
references across 55 files — fixed to "DGMA". Repo-wide count dropped
508 -> 317 (remaining 317 = buckets a+b, both intentional).
Also found and fixed 12 hyperlinks/text references pointing to
`https://dgshipping.gov.in`, which independent sources confirm was
**permanently shut down 31 March 2026** (dead domain, returns errors) —
updated to `https://dgma.gov.in`. Left 4 deep-linked
`dgshipping.gov.in/WriteReadData/userfiles/...` document URLs in
simon-notes-p3.html untouched — those specific documents' new location
on dgma.gov.in was not verified, so no replacement URL was guessed;
flagged as broken links needing Nixon's attention.
All 65 touched files (64 in the main batch + QB4_H caught in a follow-up
pass after a batch-script gap) pass HTML tag-balance validation.
GREP: SKIP (context-dependent by design; do not blanket-scan)

**Two open questions surfaced, not resolved by Claude — need Nixon's
call:**
1. ~~Full-form naming~~ — **RESOLVED 2026-08-13, confirmed by Nixon:
   "Directorate General of Maritime Administration" is correct.** The
   two "...Maritime Affairs" instances in
   `oralnotes/miw-notes-mgmt-p15.html` (both paired with "DGMA" in the
   same sentence) have been corrected to "...Administration".
2. Rename date precision: known_traps Entry 6 and ~20 files state
   "DG Shipping renamed DGMA" in the same breath as "15 March 2026" (the
   MS Act 2025 commencement date). Manorama Yearbook (July 2026) states
   the actual DGS->DGMA rename specifically took effect **in June 2026**
   under Section 7 of the Act, with the DG "assuming charge as DGMA on
   June 23" — a separate, later event from the Act's broader 15 March
   commencement. Not corrected anywhere this session; would require a
   dated, per-file review across ~20 files to distinguish "Act in force"
   claims (correctly 15 March) from "renamed to DGMA" claims (possibly
   should read June 2026 / 23 June 2026).

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

### 20. Health-check negation-marker gap — grammatical variants of supersession language ("superseding", active-voice "replaced", "re-enacted as") were missed

While closing out the Rathesh correction session (1 Aug 2026), a full health-check run surfaced ~40 "KNOWN TRAP resurfaced" hits across many QB and notes files for "A.1185(33)", "Merchant Shipping Act, 1958", and "FAL Form 8" — none flagged in this session's own edits. Root cause: `NEGATION_MARKERS` in `qb_health_check.py` only listed exact phrases ("supersedes", "replaced by", "repealed") and missed other grammatical forms of the same correction language actually used in the content — "superseding" (present participle), active-voice "replaced the... Act" (no "by"), and "has already been replaced". Fixed in two passes: (1) added "re-enacted as"/"re-enacted"/"now in force as" variants, which cleared the SQ/QB1_A.html false positive; (2) broadened to word-stem markers ("supersed", "replac", "repeal", "revok", "carried into"/"carried from"/"carried forward into") to catch every grammatical form at once rather than chasing exact phrases — this is safe because a stem hit only *downgrades* a flag to `[REVIEW]`, never suppresses it. This cut hard-error resurfaced-trap flags from ~40 to 15 across the whole repo.

The remaining 15 were individually spot-checked (QB4_A_CheatSheet.html, oralnotes/WA3-LIEN2.html, oralnotes/miw-notes-mgmt-p7/p10/p14/p15.html) by reading the actual surrounding text — every one is correctly-framed content (the supersession/correction marker is present in the same paragraph, just not always inside the checker's simple sentence-boundary window, or the file has multiple mentions in one dense reference table/paragraph where only one mention sits next to the marker). No genuine resurfaced content error was found among them. This residual gap is a sentence-splitter granularity limitation (the checker's own `_split_sentences()` is a "cheap splitter", not linguistically precise, per its own docstring) rather than a marker-vocabulary gap, and is lower priority than the marker-vocabulary fix above — logged here rather than chased further to avoid open-ended regex tuning.
GREP: SKIP

### 21. Admiralty Act 2017, Section 9 — maritime lien priority order was inverted (Salvage shown 1st, Wages 2nd)

Candidate correction (2 Aug 2026, screenshot of a MIW page forwarded to Nixon, with a link to the Act text on indiacode.nic.in). Verified against the primary source: Section 9(1) of the Admiralty (Jurisdiction and Settlement of Maritime Claims) Act, 2017 (Act No. 22 of 2017). The correct inter se priority of maritime liens is: (a) wages and other sums due to master/officers/crew — 1st; (b) loss of life or personal injury — 2nd; (c) salvage reward — 3rd; (d) port/canal/waterway/pilotage dues — 4th; (e) tort claims for loss/damage caused by the vessel — 5th. All affected content had wages and salvage swapped — Salvage was listed 1st and Wages described as "second-highest priority" — inverting the true order on the two highest-ranking items. This also directly contradicts the MLM Convention 1993 Article 4 order (wages first), which is already stated correctly elsewhere in the same files — the two lists were internally inconsistent.

Affected and now fixed: `SQ/QB1_A.html` (Q7 CE Oral Tip, Numbers to Memorise, mental-map; Q8 ordered priority list, CE Oral Tip, Numbers to Memorise, mental-map — 7 instances total; versions bumped Q7 v1.1→v1.2, Q8 v1.4→v1.5), `meoclass1/QB1_A.html` (identical mirrored duplicate, same 7 instances and version bumps), `meoclass1/oralnotes/WA3-LIEN1.html` (same 5-item list, plus a fabricated editorial claim that "under Indian law, salvage is placed ahead of wages... unlike the 1993 Convention's Article 4" — this claimed divergence does not exist, since both lists rank wages first; rewrote the paragraph to correctly explain the real nuance, which is Article 5(2)'s salvage queue-jump rule over liens that pre-date the salvage operation, not a change to the fixed first-place ranking; version bumped v1.0→v1.1). Scoped repo-wide search of `meoclass1/` and `SQ/` for "Admiralty" + "Section 9"/"Salvage costs" found 19 total hits across 9 files; the remaining 6 files (`QB9_A.html`, `QB9_D.html`, `QB9_F.html`, `QB9_G.html`, `miw-notes-mgmt-p15.html`, `simon-notes-p7.html`) reference the Act/Section 9 without asserting a specific priority order and required no changes — `QB9_G.html` in particular already correctly distinguishes S.9 (lien inter se ranking) from S.10 (broader claims-vs-mortgages ranking) and was used as the reference point for phrasing the fix.

GREP: Salvage costs</li>
            <li><strong>Wages and other sums due to master, officers, and crew</strong>

---

### 22. HSSC Survey Guidelines — A.1140(31) is three revisions stale; current is A.1207(34)
The Survey Guidelines under the Harmonized System of Survey and Certification (HSSC) are revised roughly every two years at the IMO Assembly. Chain: A.1140(31) [2019] → A.1156(32) [2021] → A.1186(33) [2023] → **A.1207(34) [2025, current]**. A.1140(31) was found cited as the live HSSC reference in the July 2026 batch (QB2_I.html Q5, QB3_J.html Q3) and, on a wider repo check, in several pre-existing files too: `QB4_F.html`, `QB4_H.html`, `QB1_I.html`, and `oralnotes/miw-notes-mgmt-p3.html`. Easily confused with the separate, similarly-numbered Procedures for Port State Control resolution chain (Entry 5: A.1185(33) → A.1206(34)) — both instruments are revised at the same biennial Assembly, one resolution number apart, which is exactly what causes the mix-up; check which instrument (HSSC survey guidelines vs. PSC procedures) before citing either number. Corrected in QB2_I.html and QB3_J.html during the July 2026 batch review (Claude, 4 Aug 2026); the four pre-existing files (QB4_F.html, QB4_H.html, QB1_I.html, oralnotes/miw-notes-mgmt-p3.html) corrected in a follow-up cleanup pass same day (Claude, 4 Aug 2026) — 9 further instances fixed across those 4 files, all verified re-negated (no raw unguarded A.1140(31) mentions remain anywhere in the repo as of this pass). Process note: the initial manual review fix only caught the REG-BOX citation in each file; a second, unguarded mention in QB3_J.html's 60-Second Answer prose ("under the HSSC survey system (Resolution A.1140(31) survey guidelines)") was missed and only caught by qb_health_check.py's post-push KNOWN TRAP scan flagging it as a hard "resurfaced" hit (not a [REVIEW] negation-context hit, since it carried no correction language) — fixed same session. Worth remembering: a single citation fix inside one card can still miss sibling mentions of the same fact in prose elsewhere on the same card; the automated scan is a real backstop, not just a formality.
GREP: A.1140(31)

### 23. QB2_I.html `&lt;title&gt;` tag mismatch — read "QB3_J" instead of "QB2_I"
Isolated copy-paste artifact from adjacent file creation during the July 2026 batch build: the browser-tab `&lt;title&gt;` element read "QB3_J — MARPOL Annexes, ORB &amp; Environmental," while the actual page content (h1, badge, all cards) correctly read QB2_I throughout. Affects SEO/tab display only, not visible page content. Checked all 8 files in the batch for the same mistake — isolated to this one file. Corrected (Claude, 4 Aug 2026).
GREP: SKIP

### 24. Places of Refuge — IMO Resolution A.949(23) is stale; current is A.1184(33)
A.949(23) (2003) "Guidelines on Places of Refuge for Ships in Need of Assistance" was revoked and updated by **A.1184(33), adopted 6 December 2023**, at the 33rd Assembly. Do not confuse with the separate, still-current **A.950(23)** (Maritime Assistance Services, MAS) — the two resolutions were adopted together in 2003 and are frequently cited side-by-side in this content, which is exactly why the stale one slipped through repeatedly: fixing A.949(23) must never touch A.950(23) mentions in the same sentence/reg-box. Found in QB9_F.html Q2 (candidate flagged this via the general "port of refuge" topic; file was misidentified as "QB1" in the report but content match was exact), oralnotes/simon-notes-p5.html, and oralnotes/miw-notes-mgmt-p12.html Topic 4 — the latter's own `verify-note` had explicitly (and incorrectly) asserted A.949(23) was "checked against the IMO's published regulation summaries and are correctly cited," which is itself now corrected. 7 total instances fixed across the 3 files (Claude, 5 Aug 2026; edited directly against the local clone at F:\marine-intelligence-weekly, manifest and this entry updated in the same pass).
GREP: SKIP — corrected sentences legitimately retain "A.949(23)" in historical/negation context ("revoked A.949(23)", "IMO adopts Res. A.949(23) and A.950(23)" timeline entries), so a bare-phrase auto-scan would false-positive; manual verification-pass only.

### 25. Bills of Lading Act, 2025 (India) — supersedes the 1856 Act
The Indian **Bills of Lading Act, 2025** received Presidential assent on **24 July 2025** and repeals the **Indian Bills of Lading Act, 1856**. Source drafts commonly lag this and either cite "the Bills of Lading Bill, 2025" (still pending) or the 1856 Act as current law. Corrected across Notes Part 19.
GREP: SKIP — "Indian Bills of Lading Act, 1856" and "Bills of Lading Bill, 2025" both appear legitimately in historical/negation context ("assent... repeals the Indian Bills of Lading Act, 1856"); manual verification-pass only.

### 26. Carriage of Goods by Sea Act, 2025 (India) — supersedes the 1925 Act; India now Hague-Visby basis
The Indian **Carriage of Goods by Sea Act, 2025 (Act No. 19 of 2025)** received assent **8 August 2025** and commenced **10 September 2025**, repealing the **Indian Carriage of Goods by Sea Act, 1925**. Its Schedule applies the Hague Rules as amended by the 1968 and 1979 Protocols — India is therefore now on a **Hague-Visby basis with SDR limits (666.67 SDR/package or 2 SDR/kg, whichever higher)**, not the old 1925 Act's Hague/gold-value basis. Corrected across Notes Parts 19–20.
GREP: SKIP — "Carriage of Goods by Sea Act, 1925" legitimately appears in historical/negation context; manual verification-pass only.

### 27. BARECON — no "BARECON C" exists
BIMCO's 1974 bareboat forms were **BARECON A** (commissioned vessels, with or without an existing mortgage) and **BARECON B** (newbuildings financed by mortgage) — amalgamated into BARECON 89, revised as BARECON 2001, current form BARECON 2017. The A/B split was about the *subject vessel and financing structure*, not insurance-premium allocation. A fabricated "BARECON C" (and an invented insurance-premium A/B/C scheme) appeared in a source draft and was removed. Found in Notes Part 19 Topic 3.
GREP: BARECON C

### 28. Volumetric weight ratios — express as volume per tonne, not weight per volume
Industry convention states volumetric charging as **CBM per tonne**: ocean 1 CBM/tonne, road 3 CBM/tonne, air 6 CBM/tonne (IATA divisor 6,000 cm³/kg ⇒ 1 CBM ≈ 167 kg). A source draft inverted this for air freight ("1 CBM = 6 tonnes" for air cargo), which is physically absurd — it would mean bulky, light cargo is charged *less*, the opposite of the actual penalty. Corrected in Notes Part 19 Topic 4.
GREP: SKIP — the specific wrong phrasing varies too much (numbers/units differ by draft) to safely auto-scan; manual verification-pass only.

### 29. ESP Code — correct citation is resolution A.1049(27), not "ESP Code 2017"
The Enhanced Survey Programme instrument is the **International Code on the Enhanced Programme of Inspections during Surveys of Bulk Carriers and Oil Tankers, 2011 (2011 ESP Code)**, adopted by **resolution A.1049(27)** on 30 November 2011, made mandatory via SOLAS XI-1/2 (resolution MSC.325(90)) from 1 January 2014. "ESP Code 2017" is not a recognised designation. Corrected in Notes Part 21 Topic 2.
GREP: ESP Code 2017

### 30. IMO Net-Zero Framework adoption status is a moving target — always re-verify the current MEPC session outcome before stating a date
The Framework was approved at MEPC 83 (April 2025), submitted for adoption at MEPC/ES.2 (14–17 October 2025) which adjourned it for one year (57/49/21 vote), discussed again at MEPC 84 (27 April – 1 May 2026) which also reached no final agreement, with the next scheduled decision point a resumed MEPC/ES.2 on **4 December 2026** (immediately after MEPC 85, 30 Nov–3 Dec 2026). Every one of those dates has already superseded an earlier one in this content's own history — found stale in Notes Part 2 Topic 9 (said "rescheduled to November 2026," corrected to 4 December 2026 across 6 occurrences) and in Notes Part 22 Topic 3 (said "reconvenes October 2026," same correction). **Never state this Framework as adopted, in force, or on a fixed future date without a fresh web search against the current MEPC session** — the underlying regulatory position changes roughly every 6 months.
GREP: SKIP — the specific stale date varies with each drafting session (this is a recurring-currency trap, not a fixed wrong phrase); manual verification-pass only, but treat any date associated with NZF adoption as suspect until re-checked.

### 31. QB3_A_CheatSheet.html GZ curve diagram — Angle of Loll marker was plotted at the curve's trough, not the GZ=0 crossing; proportions and "tender" label also wrong
Two-pass correction (both Nixon-flagged screenshot review, same session).

**Pass 1**: In the "GZ Curve & Angle of Loll — The Three GM States" diagram, the angle-of-loll marker and label ("GZ=0, ship sits here at rest") were positioned at the negative-GM curve's most-negative point (the trough), which is not where GZ=0 — a self-contradiction, since the label claimed GZ=0 at a point clearly below the GZ=0 line. Moved the marker circle and drop-line to the curve's actual zero-crossing point on the SVG path. v1.0 → v1.1.

**Pass 2**: Nixon correctly identified the shape was still wrong even after Pass 1 — the negative-stability span (0°→loll) was drawn wider than the positive-stability span (loll→AVS), backwards from reality. Rebuilt using the exact proportions of a documented worked example (Ship Stability for Masters and Mates, Fig 17.5): loll = 18°, range of stability 18°→90°, AVS = 90°. The negative-GM curve is now drawn in two colours split exactly at the loll angle — red (0°→18°, GZ negative, capsizing moment per Fig 6.5(a)) and green (18°→90°, GZ positive but restoring toward the LOLL angle, not upright, per Fig 6.5(c)) — so the positive-stability segment visibly starts at the loll angle rather than at 0°. Separately, the orange "Zero GM — Neutral / 'Tender'" curve conflated two distinct textbook concepts: **tender** = small POSITIVE GM (Ch. 40: 0.16–0.20 m, 25–35 s roll period) vs **zero GM / neutral equilibrium** = GM exactly 0 (Fig 6.4: no righting or capsizing moment at all). Relabelled to "Zero GM — Neutral Equilibrium" with an explicit note distinguishing it from "tender," and flattened the curve shape to match the neutral-equilibrium definition. The unrelated teal "Positive GM — Stable" comparison curve (a separate healthy vessel) was dropped per Nixon's instruction, since it risked reading as a continuation of the same ship's story; section retitled "Zero GM vs Negative GM" and a range-of-stability bracket added (measured from the loll angle, not 0°, per the explicit textbook note in Fig 9.9). v1.1 → v1.2.
GREP: SKIP — SVG coordinate/diagram error and terminology/proportion error, not a fixed text phrase; repo-wide grep for "ship sits here at rest" confirmed this diagram is not duplicated elsewhere.

### 32. LLMC 2012 Amendments wrongly cited as Resolution LEG.3(91) — should be LEG.5(99)
**LEG.3(91)** is "Guidelines on fair treatment of seafarers in the event of a maritime
accident," adopted by the Legal Committee at its 91st session on 27 April 2006 — an
entirely unrelated instrument (also adopted by the ILO Governing Body, 296th session,
12 June 2006). It has nothing to do with LLMC or limitation of liability.

The correct citation for the **2012 Amendments to the Protocol of 1996 to amend the
LLMC Convention 1976** is **Resolution LEG.5(99)**, adopted by the Legal Committee at
its 99th session, raising the Article 3 limits by 51% (verified against IMO's own
resolution text, uploaded by candidate). It entered into force 8 June 2015 via tacit
acceptance. `meoclass1/oralnotes/miw-notes-mgmt-p9.html` already carried the correct
LEG.5(99) citation before this fix — used as a cross-check confirming which number
was right.

Fixed in `QB1_A.html`: 4 instances in the Q3 LLMC card (intro paragraph, limits
subheading, Indian-context paragraph, reg-box) and 1 cross-reference instance in the
Q5 CLC card's parenthetical remark. q-version bumped Q3 v1.1→v1.2, Q5 v1.1→v1.2.
Repo-wide scoped search (`meoclass1/` tree) confirmed no other file carried this
conflation.
GREP: SKIP — "LEG.3(91)" is a real, correctly-usable resolution number in a different
context (fair treatment of seafarers guidelines); an exact-phrase auto-scan would
false-positive against any future correct usage. Manual verification-pass only: check
that any "LEG.3(91)" hit is actually about seafarer fair-treatment guidelines, not
misattributed to LLMC.

---

### 33. CSR scope quoted without contract date — and CSR/GBS applicability conflated
Two linked failures, both examiner-grade.

**(a) Scope stated as ship type + length only.** IACS Common Structural Rules
applicability has **three** components that must always be given together:
ship type, length threshold, **and the applicable construction-contract date**.
Quoting "bulk carriers 90 m+, double-hull oil tankers 150 m+" without a date is
incomplete and collapses against the standard follow-up ("my 200 m bulker was
built 2003 — was it CSR?" — answer: **no**).

- **Harmonised CSR BC & OT** — bulk carriers of unrestricted service, single or
  double side skin, **90 m and above**; **double-hull** oil tankers of
  unrestricted service, **150 m and above**; contracted for construction **on or
  after 1 July 2015**.
- **Earlier separate CSR-BC / CSR-OT** — adopted by IACS Council December 2005,
  applicable to ships contracted for construction **on or after 1 April 2006**.
- The Rules point to **IACS PR No. 29** for the meaning of "contracted for
  construction".
- CSR excludes ore carriers and combination carriers from its bulk-carrier
  definition; oil tanker scope is **double hull only**.

**(b) Do not equate CSR applicability with SOLAS II-1 Reg. 3-10 (GBS)
applicability.** They are two separate tests with different thresholds,
carve-outs and trigger dates. GBS (Res. MSC.290(87), in force 1 Jan 2012)
applies to oil tankers **150 m and above** and bulk carriers **150 m and above**
constructed with single deck, top-side tanks and hopper side tanks in cargo
spaces, **excluding ore carriers and combination carriers**, for which the
building contract is placed on or after **1 July 2016**; or absent a contract,
keel laid or similar stage on or after **1 July 2017**; or delivery on or after
**1 July 2020**. Consequence: a **120 m bulk carrier can be a CSR ship but not a
Reg. 3-10 ship**.

Related standing errors to watch in the same breath: "IACS made CSR mandatory"
and "SOLAS makes CSR mandatory" are both wrong — SOLAS II-1/3-10 operates on the
structural rules of a Recognized Organization or the Administration and does not
name CSR; IACS's claim that CSR are the only Rules complying with GBS must be
attributed to IACS, not stated as a SOLAS requirement.

Verified against the CSR for Bulk Carriers (January 2006) rule-text application
clause, ClassNK's CSR page, IACS's CSR page, Res. MSC.290(87)/MSC.287(87) and
MSC 96. Reference implementation: QB1_K.html Q8.
GREP: SKIP — the defect is an *omission* (missing contract date) and a *conflation*
of two applicability tests; neither is a fixed wrong phrase, and "Common Structural
Rules" is a correct term appearing 105 times across 25 live files (including the
reference answer itself), so a bare-phrase auto-scan would false-positive on every
correct usage. Manual verification-pass only: wherever CSR scope is asserted, check
ship type + length + contract date are all present, and that CSR scope has not been
equated with SOLAS II-1/3-10 GBS scope.

### 34. "PSA" left undefined, and PSSA mis-filed under MARPOL

QB3_H.html Q1 ("What are a PSA and a PSSA? Give an example of each." — Simon)
originally declared that "'PSA' is not a formal IMO term", told the candidate not
to invent a definition, and then answered only the PSSA half. That is a half
answer to a two-part question.

**Correct position.** The intended counterpart is the **MPA — Marine Protected
Area** (candidates also write MPA/MPSA). It is a real, answerable concept:

- **UNCLOS neither defines nor mentions MPAs.** Art. 194(5) is only the general
  obligation to protect rare or fragile ecosystems and the habitat of depleted,
  threatened or endangered species. Do not say "MPA is defined under UNCLOS".
- **CBD** Art. 2 (protected area definition) and Art. 8(a) (obligation to
  establish them) supply the working definition.
- **BBNJ Agreement Art. 1(9)** gives the first treaty definition of an MPA and
  the route to high-seas MPAs. **In force 17 January 2026** (60th ratification
  19 September 2025) — a current-affairs follow-up an examiner may reach for.
- Designated by coastal States, regional bodies (CCAMLR, OSPAR), and now the
  BBNJ COP. Regulates **all activities**, not just shipping.

**Second error in the same answer.** The answer framed PSSA within a MARPOL
context. **PSSA is not a MARPOL instrument.** It is an IMO Assembly resolution
— **A.982(24), as amended by resolution MEPC.267(68)** (2015); submission
guidance MEPC.1/Circ.510. The original answer cited A.982(24) without the
amendment.

**Three-way distinction to hold separate:** MPA (conservation, all activities,
UNCLOS/CBD/BBNJ + national law) / PSSA (shipping impact, IMO, legal force comes
only from the attached APM) / MARPOL Special Area (discharge and emission
criteria, MARPOL Annexes I, II, IV, V, VI). They may overlap geographically
without merging legal effects — Papahānaumokuākea is both an MPA and a PSSA.

Flagged by a candidate via Nixon (WhatsApp screenshot, 19 August 2026). The
candidate's own note needed two corrections in the reply: the expansion is
"Marine Protected **Area**", not "Marine Protected Sea Area"; and PSSA is not
MARPOL.

Fixed in: QB3_H.html Q1 → v1.2 (both halves answered, three-way distinction
added, citation completed, `unclos` tag added).

**Open scope, not yet actioned:** `A.982(24)` is cited **without** the
MEPC.267(68) amendment in QB1_B.html, QB3_E.html, QB3_F.html,
QB1_B_CheatSheet.html, oralnotes/miw-notes-mgmt-p10.html and
oralnotes/simon-notes-p1.html. Incomplete rather than wrong; the pastpapers /
solvedQP files already carry the amended form. Separate cleanup pass.

GREP: SKIP — the corrected text necessarily contains both "PSA" (inside "PSSA")
and "MPA", and "A.982(24)" is a correct citation in ~10 files. Manual
verification-pass only: wherever PSSA is defined, check (a) it is attributed to
an IMO Assembly resolution and not to MARPOL, (b) A.982(24) carries "as amended
by MEPC.267(68)", and (c) any "PSA" wording is resolved to MPA rather than
refused.

---

### 35. PSSA count stated as a hard "17", and A.982(24) cited without its amendment

Two currency defects found while fixing Entry 34, both repo-wide rather than
confined to the flagged file.

**(a) "There are currently 17 designated PSSAs globally."** Stale. The most
recent designation is **Nusa Penida / Gili Matra, Lombok Strait**
(**resolution MEPC.396(82)**, October 2024), preceded by the **North-Western
Mediterranean** (**resolution MEPC.380(80)**, 2023). That puts the total at
roughly **19**.

Do not quote a hard number. Published counts genuinely disagree — 18 or 19
depending on whether Great Barrier Reef and Torres Strait are counted as one
PSSA or two — so an examiner who has a different figure in mind is not
necessarily wrong. Correct oral form: "around nineteen, sir; the most recent is
the Lombok Strait designation in October 2024." Then move on. The count is not
the answerable part of a PSSA question; the three-element test and the APM are.

Corrected in QB1_B.html (2 places) and QB1_B_CheatSheet.html (1 place), now
phrased as approximate with a direction to verify the live list on imo.org.

**(b) `A.982(24)` cited bare.** The Revised PSSA Guidelines were **amended by
resolution MEPC.267(68)** in 2015. Citing the 2005 resolution number alone is
incomplete, and IMO's own circulars always give the amended form. Completed in
QB1_B.html (3), QB3_E.html (4), QB3_F.html (7), QB1_B_CheatSheet.html (3),
oralnotes/miw-notes-mgmt-p10.html (3) and oralnotes/simon-notes-p1.html (2),
plus the public teaser copy at SQ/simon-notes-p1.html (1). This closes the open
scope logged in Entry 34.

The p10 historical timeline was also split into separate 2005 (adoption) and
2015 (amendment) rows and extended with the 2023 and 2024 designations, so the
amendment no longer appears anachronistically on the 2005 row.

**Checked and found correct, no change:** QB3_E cites
**MEPC.1/Circ.778/Rev.5** for the Special Areas / ECA list — Rev.5 (9 May 2025)
is the current revision.

GREP: SKIP — "17" is far too generic to auto-scan, and "A.982(24)" is a correct
citation wherever the amendment now follows it. Manual verification-pass only:
any new PSSA content must give A.982(24) with the MEPC.267(68) amendment, and
must not quote a hard PSSA count.

---

### 36. Public teaser copy carried a non-existent circular revision

`SQ/simon-notes-p1.html` cited **MSC.1/Circ.1405/Rev.3**. There is no Rev.3 of
that circular. **MSC.1/Circ.1405/Rev.2** (25 May 2012) is the final revision —
Revised interim guidance to shipowners, ship operators and shipmasters on the
use of privately contracted armed security personnel (PCASP) in the High Risk
Area. Confirmed against IMO's Private Armed Security page and MSC.1/Circ.1443,
which reads Rev.2 as the operative guidance.

**The conflation:** Rev.3 belongs to the *companion flag-State* circular,
**MSC.1/Circ.1406/Rev.3** (June 2015). The pair runs 1405 (shipowners, Rev.2) /
1406 (flag States, Rev.3) / 1408 (port and coastal States, Rev.1) / 1443 (PMSC).
Different final revision numbers on adjacent circulars is exactly the shape that
invites a wrong citation.

**Why it survived:** the *gated* copy at `oralnotes/simon-notes-p1.html` was
corrected in an earlier session and carries an inline note saying so. The public
SQ teaser copy was not updated in the same pass. SQ files are hand-duplicated
with no automated sync, so the error stayed live in the free sample — the copy a
prospective subscriber reads *first* — for as long as it took someone to compare
the two by hand. Nobody did.

**Standing rule:** any correction to a file that has an SQ teaser counterpart
must be applied to **both copies in the same session**, before commit. Check for
a counterpart before considering any notes/QB correction complete.

GREP: SKIP — now covered by automation instead. See the meta-corrections section
below: `check_sq_file()` gained a citation-contradiction check that compares the
revision/session numbers cited by each copy and fails on genuine disagreement.

---

### 37. File-header version badge was decorative and always stale

Five QB files carried a version segment in the page-header badge
(`QB3_H · Backlog · v1.0`). In **every one of the five** the badge disagreed with
the file's own content: QB1_I (highest question v1.2), QB2_H (v1.1), QB3_H
(v1.2), QB4_I (v1.3), QB7_H (v1.1). The badge was frozen at v1.0 at build time
and never bumped by any correction pass. The other ~120 QB files never had one.

**Resolution: the version segment is removed, not maintained.** A second version
number that nobody updates is worse than none — it looks authoritative and is
always wrong. The badge now reads `QB3_H · Backlog`, matching the majority
convention already present in QB1_H, QB3_G and QB4_H.

**The per-question `q-version` footer is the single source of version truth.**
It is bumped on every correction, it names what changed and when, and it sits
next to the content it describes. Do not reintroduce a file-level version badge.

GREP: SKIP — a bare version string is far too generic to auto-scan. Manual rule:
when building a new QB file, the header badge is `<code>ID · Backlog</code>` or
`<code>ID</code>` only; no version segment.

### 38. Fair Treatment of Seafarers — fabricated MLC "Regulation 5.2.7", fabricated LEG 110/111 VDR guidance, and A.987(24) wrongly described as becoming mandatory

Candidate correction via Nixon (WhatsApp, 21 August 2026) on **QB1_A Q25**
("Fair Treatment of Seafarers — Where is it mentioned?", asked by Nair
immediately after a casualty-investigation question). The candidate's point was
that the answer omitted the Casualty Investigation Code, which was correct and
was the principal defect. His own placement — "included in CIC Recommended
Practices (Under Part III)" — is not right, and was corrected in the reply.

**(a) The Code placement.** Verified against the full text of resolution
MSC.255(84). There is no chapter in Part III titled or citing fair treatment.
The express citation of the Guidelines sits in the **preamble** ("CONSIDERING
ALSO the Guidelines on fair treatment of seafarers in the event of a maritime
accident (resolution A.987(24))") and in the **Foreword, paragraph 6**, under
the standing heading **"Treatment of Seafarers"**. The operative
seafarer-protection obligations are **Part II, Chapter 12 — Obtaining evidence
from seafarers**, which is mandatory under SOLAS XI-1/6.1 (12.1 evidence at the
earliest practical opportunity, return to ship or repatriation at the earliest
possible opportunity, "the seafarers human rights shall, at all times, be
upheld"; 12.2 informed of the nature and basis, access to legal advice on
self-incrimination and the right to remain silent). The nearest Part III
provision is **Chapter 24 — Protection for witnesses and involved parties**
(24.1 compelled self-incriminating evidence inadmissible so far as national law
allows; 24.2 extends 12.2 to any person), supported by Ch 23 (confidentiality of
marine safety records), Ch 25.4 (report inadmissibility) and Ch 21.2.5 (take
account of IMO/ILO instruments). Answering "Part III" concedes non-mandatory
status when the mandatory answer was available.

**(b) MLC Regulation 5.2.7 / Standard A5.2.7 does not exist.** The live answer
cited it four times as the port-State fair-treatment duty. MLC Title 5, Part 5.2
runs only to **Regulation 5.2.1** (port State inspections) and **Regulation
5.2.2** (onshore seafarer complaint-handling procedures). The correct hooks are
**Guideline B4.4.6, paragraph 2** (seafarers detained in a foreign port dealt
with promptly under due process of law and with appropriate consular protection)
and **Regulation 5.1.6** (flag State official inquiry into any serious marine
casualty causing injury or loss of life). Cite *Regulation* 5.1.6, not Standard
A5.1.6: the 2025 amendments *add* new paragraphs 1 and 2 to A5.1.6, meaning it
carries none until they are in force.

**(c) Fabricated Legal Committee guidance.** The answer claimed "recent sessions
of the IMO Legal Committee (LEG 110 / LEG 111 outputs) have updated these
guidelines — extending protections to cover automated data, VDR recordings, and
digital tracking records". No source supports this. **A.987(24) has never been
amended.** LEG 110 (2023) adopted the seafarer-abandonment guidelines
(**LEG.6(110)**); LEG 111 (April 2024) finalised the *draft* detained-seafarers
guidelines. The real current instrument is the **ILO/IMO Guidelines on Fair
Treatment of Seafarers Detained in Connection with Alleged Crimes**, adopted at
JTWG-3 (Geneva, 26–28 November 2024) and by the Legal Committee as **resolution
LEG.7(112) on 28 March 2025**. Removed entirely per the standing rule that
fabricated content is deleted, not softened.

**(d) A.987(24) status — standing phrasing rule.** Do not write that the
Guidelines "become mandatory" through the Code. **A.987(24) remains
recommendatory and was never elevated.** The Casualty Investigation Code is a
separate instrument that contains its own mandatory seafarer-protection
requirements through SOLAS XI-1/6. Two instruments, not one instrument changing
status. (Nixon's precision instruction, 21 August 2026 — use this phrasing
wherever the pair is described.)

**(e) Hebei Spirit chronology inverted.** The answer called Hebei Spirit "a
direct driver for strengthening fair treatment guidelines at IMO" and "the
central case driving fair-treatment guideline reforms". The collision was
**7 December 2007**; the Guidelines were adopted December 2005 and promulgated
1 July 2006. The case cannot have driven them. It exposed that they were
unenforceable, feeding **A.1056(27)** (30 November 2011, promotion of widest
possible application) and ultimately LEG.7(112). Pre-2006 drivers were the
detentions following Erika (1999), Prestige (2002) and Tasman Spirit (2003).

**Time-sensitive material quarantined.** The **2025 amendments to the MLC Code**
(STC-5, Geneva 7–11 April 2025; approved by the 113th International Labour
Conference 6 June 2025; notified to Members 23 June 2025; formal-disagreement
period ends 23 June 2027; **expected entry into force 23 December 2027**) amend
Guideline B4.4.6(2) to require due account of the detained-seafarers Guidelines
and add paragraphs 1 and 2 to Standard A5.1.6. Placed in a new `verify-note`
box, not in the memorisation answer.

**Cross-reference to Entry 32:** LEG.3(91) is the Legal Committee's own adoption
of these same 2006 Guidelines (27 April 2006; ILO Governing Body 296th session,
12 June 2006) — it is *this* instrument, not an LLMC one. Now stated explicitly
on the card so the two never re-converge.

Also fixed on the same card, same defect cluster: Q24's related-question strip
labelled Q25 as "Wreck/Nairobi" and Q26 as "MLC" (Q25 is Fair Treatment, Q26 is
the Wreck Convention), and the dependency-graph card repeated "MLC 5.2.7" in
both `meoclass1/QB1_A.html` and the public teaser `SQ/QB1_A.html` — the Entry 36
standing rule (SQ counterpart corrected in the same session) applied. Q25 v1.0 →
v1.1; file v1.9 → v2.0.

**Refinement, same day.** The first pass of this fix described the Guidelines as "adopted by the IMO Assembly, resolution A.987(24)". Checked against the resolution text itself: **A.987(24) (adopted 1 December 2005) does not contain the Guidelines**. It urges States to respect seafarers' human rights, to investigate expeditiously and to allow prompt repatriation or re-embarkation; it records that recommendatory guidelines are the appropriate means; and it *authorises* the Legal Committee and the ILO Governing Body to promulgate the Guidelines once the Joint IMO/ILO Ad Hoc Expert Working Group finalised them. The Guidelines text was adopted by **LEG.3(91) on 27 April 2006** and by the **ILO Governing Body, 296th session, 12 June 2006**, and promulgated **1 July 2006**. The Casualty Investigation Code's own Foreword uses the loose form ("adopted... through resolution A.987(24)"), which is how the error propagates — quote the chain, not the shorthand. Also added from the resolution's recitals: **UNCLOS Article 230** (pollution offences beyond the territorial sea attract monetary penalties only, with the recognized rights of the accused observed) alongside Article 292, and the **MARPOL Annex I Reg 11 / Annex II Reg 6** damage-exception, which is the CE's substantive defence after an accidental discharge. Q25 v1.1 → v1.2.

GREP: Regulation 5.2.7
GREP: Standard A5.2.7
GREP: LEG 110 / LEG 111 outputs

Note: the corrected card intentionally retains the phrase "Standard 5.2.7" once,
inside the Examiner Trap block ("There is no MLC Regulation or Standard 5.2.7"),
and retains "Part III" throughout while correctly explaining its recommended
status. Both are negation-context hits per the pattern above — check the
surrounding sentence before treating either as resurfaced.
### 39. CII guidelines G1/G4 mis-numbered as MEPC.337(76)/MEPC.338(76) in the public teaser copies

The gated `oralnotes/simon-notes-p1.html` and `oralnotes/simon-notes-p2.html` were
corrected in an earlier session to the right resolution numbers and each carries an
inline "(corrected from MEPC.337(76)...)" note. The public SQ teaser copies were not
updated in the same pass and were still citing the wrong ones — the Entry 36 class of
error again, on the free sample a prospective subscriber reads first.

**Correct mapping** (verified against the primary text of MEPC.338(76) itself, whose
paragraph 1.2 names G1 and G2 by resolution number, and corroborated by ClassNK, IRClass
and BKI circulars):

| Guideline | Resolution | Subject |
|---|---|---|
| G1 | **MEPC.336(76)** | Operational carbon intensity indicators and the calculation methods |
| G2 | **MEPC.337(76)** | Reference lines for use with operational CII |
| G3 | **MEPC.338(76)** | Operational CII reduction factors relative to reference lines |
| G4 | **MEPC.339(76)** | Operational carbon intensity rating of ships (A–E boundaries) |

**Why this one keeps recurring.** Pre-adoption briefs written immediately after MEPC 76
(June 2021) circulated the set as **335/336/337/338** — one number low across the board.
ABS's own MEPC 76 brief lists "G1 = MEPC.335(76), G2 = MEPC.336(76), G3 = MEPC.337(76),
G4 = MEPC.338(76)". Any secondary source of that vintage is off by one, and drafting from
it reproduces the error silently because the numbers look plausible. Always take this
quartet from the adopted resolution text, never from a session brief.

Fixed: `SQ/simon-notes-p1.html` (the C<sub>F</sub>/rating reg-item cited MEPC.338(76) for
both the CF values and the A–E boundaries — neither is G3; split into MEPC.336(76) for the
calculation method, with C<sub>F</sub> values themselves noted as tabulated in MARPOL
Annex VI Appendix IX, and MEPC.339(76) for the rating boundaries) and
`SQ/simon-notes-p2.html` (MEPC.337(76)/MEPC.338(76) cited as the indicator and rating
guidelines; corrected to MEPC.336(76)/MEPC.339(76), with an explicit note that 337 is G2
and 338 is G3 so the pair is not re-quoted for calculation or rating).

GREP: SKIP — MEPC.337(76) and MEPC.338(76) are correct citations for G2 and G3 and appear
legitimately (including inside the corrected sentences, which name them in order to
exclude them). Manual verification-pass only: wherever a CII guideline is cited, check the
G-number against the resolution number using the table above.

### 40. Casualty Investigation Code described as "incorporating" the fair-treatment Guidelines, plus an unverifiable interrogation-conditions claim

Found in `QB1_B.html` Q15 while scoping Entry 38 across the repo. Two problems in one
paragraph.

**(a) Framing.** The card read "The Code, incorporating the ILO/IMO Guidelines on the Fair
Treatment of Seafarers, provides basic guardrails during state interrogations". The Code
does not incorporate the Guidelines. It cites them in its preamble and in Foreword
paragraph 6, and separately carries its own mandatory protections in Part II Chapter 12.
The Guidelines remain recommendatory throughout — see Entry 38(d) for the standing
phrasing rule.

**(b) Fabricated condition.** The card asserted that "medical fitness and fatigue states
must be assessed before prolonged interrogation occurs". No such requirement appears in
Chapter 12, in Chapter 24, or in A.987(24). Removed rather than softened. The two
surviving points were re-attributed correctly: language and consular access are not
Chapter 12 obligations either — consular access rests on **VCCR 1963 Article 36** and
**MLC Guideline B4.4.6(2)**, and the Chapter 12.2 entitlement is to be informed of the
nature and basis of the investigation and to be given access to **legal advice** on
self-incrimination and the right to silence. Paragraph rewritten around the actual
Chapter 12.1/12.2 and Chapter 24 text, with a pointer to QB1_A Q25 for the full answer.
Q15 v1.1 → v1.2.

GREP: Medical fitness and fatigue states

### 41. MLC Regulation 2.7 is Manning Levels, not Recreational Facilities

`QB5_A.html` Q4 (Maslow's hierarchy mapped to MLC/ISM/STCW) cited "MLC Reg. 2.7
(Recreational Facilities)" against the Social/Belonging level. Regulation 2.7 of the MLC
is **Manning levels**. Accommodation and recreational facilities are **Regulation 3.1**.
Corrected. The adjacent citation in the same cell, MLC Reg. 4.4 (shore-based welfare
facilities), was already right and is unchanged. Q4 v1.0 → v1.1.

Worth holding the Title 2 list straight, since it is a cheap examiner catch: 2.1 seafarers'
employment agreements · 2.2 wages · 2.3 hours of work and rest · 2.4 entitlement to leave ·
2.5 repatriation · 2.6 compensation for the ship's loss or foundering · 2.7 manning levels ·
2.8 career and skill development.

GREP: Reg. 2.7 (Recreational Facilities)
---

### 42. MSC.535(107) lifeboat ventilation described as new-build-only, using a "keel laid" test the resolution never uses

`QB2_F.html` Q6 (ventilation of totally enclosed lifeboats) got the two dates right but
the **application rule** wrong. Seven places on the card reduced *installed on or after
1 January 2029* to a newbuilding test — "contracted/keel-laid", "building contract is
dated (or keel laid, if no contract)", "new-build application only, not retrofit",
"next-generation newbuild".

MSC.535(107) paragraph 4 **defines the expression itself**, in two limbs:

- **(a)** for ships for which the building contract is placed on or after 1 January 2029,
  or in the absence of the contract **constructed** on or after that date — any
  installation date on the ship; or
- **(b)** for ships **other than** those in (a), a contractual delivery date for the
  equipment or, in the absence of one, the actual delivery date of the equipment to the
  ship, on or after 1 January 2029.

Two errors follow. First, the resolution says **constructed**, not *keel laid* — a
formulation imported from other IMO instruments and not used here. Second, and worse,
dropping limb (b) made the card assert the **opposite** of the rule for the entire
existing fleet: a replacement lifeboat contracted for or delivered to in-service tonnage
on or after 1 January 2029 **is** caught. What the amendment does not do is force
retrofit of lifeboats already installed — which is a narrower statement than
"new-builds only".

Everything else on the card was rechecked against the primary text and is correct:
5 m³/h per person for the number of persons the lifeboat is permitted to accommodate,
not less than 24 hours, operable from inside, no stratification or unventilated pockets,
powered source not the radio batteries of 4.4.6.11, engine-driven ventilation fuelled per
4.4.6.8, adoption 8 June 2023, entry into force 1 January 2026, the MSC.81(70) ventilation
performance test with entrances and hatches closed, and MSC.559(108) adding "ventilation
system, where fitted" to the MSC.402(96) annual thorough examination. The 15-second
answer already said "installed on/after 1 Jan 2029" and was left alone.

Scope pass: `index22.html`, `archive/issue22.html` ("installations on/after 1 January
2029") and `QB2_I.html` (MSC.535 listed under the 1 Jan 2026 entry-into-force wave) were
checked and are **correct** — not changed. Q6 v1.0 → v1.1.

GREP: SKIP — the corrected text deliberately contains "keel laid" and "new-build" while
saying they are wrong.
---


### 43. "main boilers" listed as a Continuous Machinery Survey item — the boiler is not on the CSM clock

`QB1_G.html` Q40 (CSM survey) listed **"main boilers"** among the *Vital Auxiliary
Systems* assessed under Continuous Machinery Survey, alongside main air compressors,
steering gear pumps, emergency fire pumps and heat exchangers — in an answer that also
states every CSM item is examined at least once in five years and that the interval
between examinations of any item must not exceed five years.

A boiler is not on that clock. **IACS UR Z18 (Survey of Machinery)** keeps the two
regimes in separate sections with separate intervals:

- **§1.3 Continuous Surveys** — special surveys of machinery may be carried out on a
  continuous survey basis; the interval between consecutive examinations of *each item*
  is not to exceed **five years**.
- **§2.1 Survey of Steam Boilers** — water tube boilers for main propulsion including
  reheat boilers, all other boilers of essential service, and boilers of non-essential
  service above 0.35 N/mm² working pressure and 4.5 m² heating surface are to be
  surveyed **internally**, with a **minimum of two internal examinations during each
  5-year special survey period** and the interval between any two such examinations
  **not to exceed 36 months**. Boilers, superheaters and economizers are examined on
  both the water-steam side and the fire side; mountings and safety valves are examined
  at each survey.
- **§2.2** — an **annual** external survey with testing of safety and protective devices
  and of the safety valve using its relieving gear.

So the defect was not a loose category. Reading the boiler as an ordinary CSM item
stretches its internal examination interval from **36 months to five years**.

The **ClassNK Guidance on Continuous Machinery Survey (CMS), Ver.4, June 2025** shows the
same boundary from the applicability side. Its enumeration of machinery applicable to the
CMS system (items ①–⑱) contains **no boiler**, but does contain boiler *auxiliaries*:
Forced Draft Fans for Boiler, Boiler Burning Pumps, Boiler Water Circulating Pumps, Feed
Water Pumps, and F.O. Tanks for Boilers; the Appendix D CMS Reference Table carries a
`Boiler F.D. Fan` row and no boiler row.

The card now names those auxiliaries instead, states that boilers, superheaters and
economizers are **not** CSM items and carry their own **Boiler Survey**, and gives the
36-month figure and the annual external survey.

Second defect on the same card: the reg-box cited **IACS Procedural Requirements PR 1C**
as the "framework for continuous class verification". PR 1C is the *Procedure for
Suspension and Reinstatement or Withdrawal of Class in Case of Surveys or Conditions of
Class Going Overdue* and says nothing about continuous survey. It is replaced by **IACS
UR Z18** with the two sections actually relied on.

Scope pass: the rest of the machinery list was checked item by item against the ClassNK
CMS enumeration and is **correct** — crank pins, main bearings, crossheads and
turbochargers (item ①), auxiliary generator engines (③), main and auxiliary starting air
compressors (④), steering gears (⑯), bilge/ballast/GS/fire pumps and heat exchangers,
coolers and condensers (Reference Table). `QB1_supplementary.html` and `QB1_F.html`
already state the boiler exclusion correctly and were **not changed** — the former says
CMS "explicitly excludes statutory items with their own independent regimes … pressure
vessels such as auxiliary boilers", the latter carries the trap answered "No. Boilers and
pressure vessels are strictly surveyor-only items." `QB4_J.html` already writes
"CSM/boiler/shaft surveys" as distinct engagements. Q40 v1.0 → v1.1.

Two open items recorded, not actioned: this card's question stem expands CSM as
"Condition Survey Method" (CSM is the **Continuous Survey of Machinery**, which the
answer body itself uses), and `QB1_supplementary.html` cites **UR Z7/Z7.1** as governing
CMS where the machinery survey requirement is **Z18**.

GREP: main boilers

---


### 44. CSM/boiler answer built on IACS and ClassNK with no Indian authority in the chain

Follow-up to Entry 43. That correction was right to take the boiler out of the CSM
machinery list, but it reached the answer through **IACS UR Z18** and a **ClassNK**
equipment list. For an MEO Class I candidate sitting before a DG Shipping examiner the
authority order is wrong, and the ClassNK list read as though it were *the* list.

Checked against the Indian sources, which do not merely re-order the answer — **they
change part of it**:

- **IRS Guidelines on Continuous Surveys of Machinery (IRS-G-SUR-02, March 2022)** draws
  its boiler line as a **Chief Engineer credit** boundary, not a CSM eligibility
  boundary. Section 4 is *"Typical List of Machinery Items not acceptable for Survey by
  Chief Engineers"*, and **4.1.1(d) "Boilers and all other pressure vessels"** are *"to be
  surveyed by IRS Surveyors"*. That is a different proposition from "boilers are not CSM
  items", and for an IRS-classed ship the flat version is too strong. The card now makes
  the narrower claim every source supports: the boiler's **pressure boundary** is not on
  the 5-year CSM item interval, because the boiler survey regime governs its internal
  examination.
- The base correction's auxiliary list was **ClassNK's, not IRS's**. IRS **3.1.1(w)**
  forced or induced draught fans and **3.1.1(aa)** adjustment of exhaust-gas boiler safety
  valves under steam are Chief-Engineer-surveyable; IRS does **not** name boiler burning
  pumps or feed water pumps, and **4.1.1(e)** puts boiler fuel oil heaters above 6.9 bar
  out of the CE's reach. Those two pump types are removed from the card.
- **IRS Main Rules Part 1, Ch 2, §8.2** is CSM proper — Special Survey of machinery
  completed within 5 years, item interval not exceeding 5 years, ~⅕ of items a year;
  **§1.4** allows certain items under CE supervision subject to confirmatory survey.
- The Indian **statutory** vocabulary is *"running survey"* — under Rule 274 of the MS
  (Construction and Survey of Passenger Ships) Rules 2026 the hull and machinery are
  opened up and surveyed within 5 years on a schedule the owner draws and the
  Administration approves, with the RO keeping a parallel *Continuous Survey of Hull &
  Machinery* cycle and the Principal Officer specifying MMD attendance. A candidate who
  only knows the word "CSM" is answering in the class register alone.
- On **intervals the three layers coincide** and the card now says so: IACS UR Z18 §2.1,
  the IRS regime and the Indian statutory requirement all give ≥2 internal examinations
  per 5-year special survey cycle, no two more than **36 months** apart.

**Status care:** the draft *Merchant Shipping (Survey, Audit and Certification) Rules,
2026* opens `DRAFT … NOTIFICATION … New Delhi, the____________ 2026 … G.S.R. ______ (E)`
— blank date, blank GSR number. Consultation ran 12.12.2025–11.01.2026. It is cited for
terminology and interval, and the card states it is **not yet notified**. It is not quoted
as binding.

**ClassNK is demoted** from evidence to *implementation example only*, labelled as such in
the reference box, retained solely to show that the detailed equipment list differs
between IACS member societies. IACS is described as a **unified class baseline, not a
statutory authority**.

Entry 43 is **not reopened**: "main boilers" stays out of the machinery list and the false
IACS PR 1C citation stays removed. Q40 v1.1 → v1.2.

Recorded, not actioned: the CE Oral Tip says the CE cannot credit *"the Boiler Safety
Valves"*, right as a general statement under IRS 4.1.1(d), but IRS 3.1.1(aa) and UR Z18
§2.2 both let the CE set **exhaust-gas** boiler safety valves at sea where steam cannot be
raised in port. Editing examiner-voice CE-tip prose is a separate editorial act.

GREP: boiler burning pumps and feed water pumps

---


### 45. "DG Shipping / DGMA" written as a live pair, reviving a retired name

Entry 44 introduced the string **"DG Shipping / DGMA"** twice on `QB1_G.html` Q40 — once
in the authority-order bullet, once as the reg-box code. Presenting a retired name and its
successor as alternatives implies the old one is still current. It also regressed a
convention this repository had already settled: the **Entry 6 follow-up** audit converted
191 references across 65 files from "DG Shipping" to "DGMA", and the corpus expands the
name as **"Directorate General of Maritime Administration"** in 31 places with no competing
form. `QB1_G` itself already carried the house pattern on another card — *"the DGMA
(Directorate General of Maritime Administration, formerly DG Shipping)"*.

Q40 now reads *"The **Directorate General of Maritime Administration** (formerly DG
Shipping) prescribes the statutory survey requirement"*, with **DGMA** as the short form
thereafter including the reg-box code. The gloss is kept deliberately: a candidate reading
older circulars needs to connect the two names.

**Scope held to Q40.** `QB1_G` carries about a dozen other "DG Shipping" strings and they
were checked and **left unchanged**, because they are *document titles* — "DG Shipping
Engineering Circular 02 of 2024", "DG Shipping MS Notice 08 of 2022", "DG Shipping Merchant
Shipping Notice 14 of 2020". A circular's title is its identity at time of issue; renaming
it would make it uncitable and an examiner would not recognise the renamed form. Confirmed
with the Founder before editing.

**Recorded, not swept:** ten further candidate-facing files still contain "DG Shipping" —
`QB3_G`, `QB4_D`, `QB4_E`, `QB9_E`, `QB9_E_CheatSheet` and `oralnotes/miw-notes-mgmt-p1`,
`p5`, `p14`, `p15`, `p16`. They mix document titles with possible live-authority references
and need reading occurrence by occurrence. A blind global replace would rename circular
titles, which is exactly the failure this entry guards against.

No technical claim, citation, interval or authority-hierarchy statement changed. Entries 43
and 44 are not reopened. Q40 v1.2 → v1.3.

GREP: DG Shipping / DGMA

---


## Meta-corrections to `qb_health_check.py` itself (non-content fixes, logged here for continuity)

- 2026-08-01: Fixed a Windows-console `UnicodeEncodeError` crash in the Brevo-fallback print path when SMTP credentials aren't set locally (was crashing on ⚠/✅ glyphs; also fixed a related bug where the fallback path's temporary `TextIOWrapper` around `sys.stdout.buffer` closed the underlying buffer on garbage collection, breaking all later prints in the same run).
- 2026-08-01: Fixed the "QB file(s) on disk but missing from manifest" orphan check to exclude `SQ/` — those are public teaser copies intentionally outside the gated `meoclass1/` manifest scope, not orphaned builds.
- 2026-08-01: Broadened `NEGATION_MARKERS` per Entry 20 above.
- 2026-08-19: Added `extract_citations()` and `citation_bases()`, and rebuilt the
  SQ-teaser drift check in `check_sq_file()`. The previous check compared file
  sizes with a 15% tolerance, which cannot see a one-character revision-number
  correction — the failure that let Entry 36 stay live. The new check works in
  two tiers: (1) **contradiction** — the same instrument cited at *disjoint*
  revision/session numbers in the gated and teaser copies, which is
  truncation-proof because it only compares instruments appearing in both files,
  and subset-tolerant so citing both Rev.1 and Rev.2 in one copy and only Rev.2
  in the other is not flagged; (2) **omission** — citations present in the gated
  copy but absent from the teaser, gated on the teaser being ≥85% the size of
  the original, so deliberately truncated samples like `SQ/QB1_A.html` do not
  generate dozens of false positives. Regression-tested against the Entry 36
  defect: the pre-fix text trips the contradiction check, the corrected text
  passes.

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


### 46. The rescue boat's 5-knot figure belongs to LAUNCHING, not to recovery

`QB2_E.html` Q1 and Q3 both attached the **5 knots of ship headway** to the *recovery*
of a rescue boat. SOLAS III has two separate requirements and they are easy to fuse:

* **Reg. 17.3** — the rescue boat must be capable of being **launched**, where necessary
  using painters, with the ship making headway at speeds up to **5 knots in calm water**.
* **Reg. 17.4** — **recovery** time shall be **not more than 5 minutes** in moderate sea
  conditions, loaded with its full complement of persons and equipment.

Recovery is governed by a *time*, not by a ship speed. A candidate who says "recovered at
up to five knots" has merged two regulations and can be taken apart on either.

The correction pass itself taught the second half of this entry. A first attempt fixed the
prose and the regulatory reference box and left the defect **verbatim in the Numbers block,
in an SVG diagram label and in the page meta description** — the summary lines being
precisely what a candidate memorises. It also mis-cited the sub-paragraphs as 17.1 and
17.3. **When correcting a card, sweep the bullets, the Numbers block, diagram labels and
page metadata, not only the prose.**

### 47. MARPOL Annex VI Regulations 21 and 22 are not EEDI and SEEMP any more

`QB1_C.html` Q9 cited **"MARPOL Annex VI, Reg. 21 & 22 — EEDI and SEEMP"**. That is the
pre-2021 numbering. **MEPC.328(76)**, the revised Annex VI in force **1 November 2022**,
renumbered Chapter 4:

| Reg. | Subject |
|---|---|
| 20 | Goal |
| **21** | **Functional requirements** |
| **22** | **Attained EEDI** |
| 23 | Attained EEXI |
| **24** | **Required EEDI** |
| 25 | Required EEXI |
| **26** | **SEEMP** |
| 27 | Collection and reporting of fuel oil consumption data |
| **28** | **Operational carbon intensity** (the CII rating) |

Any answer still saying "Reg. 21 is EEDI, Reg. 22 is SEEMP" is quoting a numbering that
was superseded four years ago. Related: the same card understated **SOLAS II-1/3-10**
(Goal-Based Standards) as applying to "bulk carriers and oil tankers" — the scope is oil
tankers and bulk carriers of **150 m in length and above** with a building contract placed
**on or after 1 July 2016**. See also Entry 33, where CSR applicability was wrongly
equated with GBS applicability.

### 48. The Baltic Dry Index has had no Handysize component since 1 March 2018

`QB8_A.html` Q3 described the BDI as built from **Capesize, Panamax, Supramax and
Handysize** sub-indices. Baltic Exchange Circular 08/18 removed the Handysize timecharter
average from the BDI on **1 March 2018**. Since then the index is weighted **40% Capesize,
30% Panamax, 30% Supramax**. The **Baltic Handysize Index (BHSI)** already existed and
continues to be published separately — it was not created by that change. The equal
four-way split is the pre-2018 arrangement.

### 49. TML is 90% of the Flow Moisture Point — except for the cargo you are most likely to be asked about

`QB2_A.html` Q31 stated flatly that **TML = 90% of FMP** and, in an adjacent bullet, that
iron ore fines uses the **modified Proctor/Fagerberg** test. Those two statements are
mutually exclusive, and the cargo in question is the one that sinks ships.

* Where the **Flow Moisture Point is measured** — the flow-table and penetration tests —
  **TML is 90% of the FMP**.
* Where the **Proctor/Fagerberg** test is used, TML is read directly off the compaction
  curve as the critical moisture content at a stated **degree of saturation**: **70%** for
  the general test, and **80%** for **iron ore fines** under the modified procedure in
  **IMSBC Appendix 2**. Iron ore fines therefore **has no FMP at all**.

A candidate who recites "TML is 90% of FMP" and is then asked "and for iron ore fines?"
is caught. Related, and found in the same pass: **Group A** is no longer just "cargoes
which may liquefy" — since the 05-19 / 06-21 amendments the definition is cargoes which
may **liquefy or undergo dynamic separation**.

| 2026-07-16 | Initial 10 entries | Compiled from Claude memory / prior correction sessions |
| 2026-07-18 | Entry 11: IMO GFI vs FuelEU Maritime baseline | Candidate (Rathesh) annotated-screenshot correction on QB6_E |
| 2026-07-19 | Entry 12: CLC scope — mineral oil only (whale oil trap) | Candidate (Vivek) screenshot correction on QB1_A |
| 2026-07-25 | Entry 13: GRB threshold now 100 GT, not 400 GT (MEPC.360(79)) | Nixon screenshot correction on QB3_C |
| 2026-07-27 | Entry 15: IMO convention adoption quorum is 1/3, not 2/3 | Candidate screenshot correction on simon-notes-p3 |
| 2026-07-29 | Entry 16: Pipe-delimited markdown tables → real `<table>` markup (formatting standard, not a fact error); added `check_pipe_table_format()` to health check | Candidate screenshot correction on QB2_A, repo-wide grep found 4 more affected files |
| 2026-07-30 | Entry 17: Form E does not list fire-fighting equipment (QB3_A, cheat sheets, QB8_A, QB8_B) | Nixon correction (SEQ Q15 review) |
| 2026-08-01 | Entry 18: BMP5 already covers weapon-of-war threats via safe muster point (distinct from citadel) — added to QB4_H Q2 + cheat sheet | Candidate (Rathesh) via Nixon |
| 2026-08-01 | Entry 19: QB4_H Q2 expanded — Hormuz routing dispute (Iran redrawn TSS), hardening purpose split, AIS/coastal-state clarification | Candidate (Rathesh) via Nixon |
| 2026-08-02 | Entry 21: Admiralty Act 2017 S.9 maritime lien priority order inverted (Salvage 1st/Wages 2nd → corrected to Wages 1st) — QB1_A.html (SQ + meoclass1) and WA3-LIEN1.html | Candidate correction via Nixon (indiacode.nic.in source link) |
| 2026-08-04 | Entry 22: HSSC Survey Guidelines A.1140(31) three revisions stale, current A.1207(34) | Claude Chat verification pass on July 2026 batch; also found in 4 pre-existing files, flagged for separate cleanup |
| 2026-08-04 | Entry 23: QB2_I.html title-tag mismatch (read "QB3_J") | Claude Chat verification pass on July 2026 batch |
| 2026-08-05 | Entry 24: Places of Refuge A.949(23) stale, current A.1184(33) | Candidate correction via Nixon |
| 2026-08-05 | Entries 25–30: Bills of Lading Act 2025, COGSA 2025 (India now Hague-Visby), fabricated "BARECON C", inverted air-freight volumetric ratio, ESP Code citation (A.1049(27)), IMO NZF adoption-status currency reminder — all found while building Notes Parts 19–22 and cross-checking against Parts 1–18 (Part 2 T9 and Part 22 T3 both had a stale NZF date, corrected in the same pass) | Claude Chat, building Notes Parts 19–22 (Uday Sankar S. source, pp. 451–550) |
| 2026-08-07 | Entry 31: QB3_A_CheatSheet.html GZ curve diagram, two-pass — trough-vs-zero-crossing marker error, then negative/positive span proportions and "tender" mislabel, per full redraw against a documented textbook worked example | Nixon Antony (screenshot review, iterative) |
| 2026-08-08 | Entry 32: LLMC 2012 Amendments wrongly cited as LEG.3(91) (fair treatment of seafarers guidelines) instead of LEG.5(99) — QB1_A.html Q3 (4 instances) and Q5 cross-reference (1 instance) | Candidate correction via Nixon (IMO resolution PDF attached) |
| 2026-08-13 | Entry 6 scope note: QB5_C_B Q5 (True Confidence 2024 casualty link, "3 Indian crew died" question) — corrected False casualty-nationality implication (True Confidence fatalities were 2 Filipino + 1 Vietnamese, not Indian), updated "DG Shipping"→"DGMA" (×2), updated MS Act 1958 Section 358 citation to MS Act 2025 (exact section not independently verified) → v1.2. Repo-wide "DG Shipping" bare-mention scope (~678 hits/68 files) flagged, not yet actioned. | Candidate correction request via Nixon (screenshot) |
| 2026-08-13 | Entry 6 follow-up: full repo-wide DG Shipping→DGMA audit, 65 files touched, 191 references corrected (175 naming + 16 missed-in-first-pass QB4_H items), 12 dead dgshipping.gov.in links fixed to dgma.gov.in. Two open questions flagged (Affairs vs Administration naming; March vs June rename date) — see Entry 6 for detail. | Nixon-requested follow-up, same session |
| 2026-08-18 | Entry 33: CSR scope quoted without contract date (ship type + length + contract date must be given together; harmonised CSR BC & OT 1 Jul 2015 vs original CSR-BC/CSR-OT 1 Apr 2006), and CSR applicability wrongly equated with SOLAS II-1/3-10 GBS applicability (GBS is 150 m+ both types, contract 1 Jul 2016 / keel 1 Jul 2017 / delivery 1 Jul 2020, ore and combination carriers excluded) | Candidate report via Nixon (Vivek, WhatsApp); verified against IACS/ClassNK rule text and IMO resolutions while building QB1_K Q8 |
| 2026-08-19 | Entry 34: QB3_H Q1 — "PSA" resolved to MPA (Marine Protected Area) and the MPA half of the answer written; UNCLOS Art. 194(5) / CBD Art. 8(a) / BBNJ Art. 1(9), in force 17 Jan 2026, legal basis stated; PSSA corrected from a MARPOL framing to IMO Assembly res. A.982(24) as amended by MEPC.267(68); MPA vs PSSA vs MARPOL Special Area three-way distinction added → v1.2. Six further files cite A.982(24) without the amendment — logged, not actioned. | Candidate report via Nixon (WhatsApp screenshot) |
| 2026-08-19 | Entry 35: PSSA count stated as a hard "17" — stale, now ~19 following the NW Mediterranean (MEPC.380(80), 2023) and Nusa Penida / Gili Matra Lombok Strait (MEPC.396(82), 2024) designations, and rephrased as approximate because published counts vary 18–19; A.982(24) completed with its MEPC.267(68) amendment across 7 files (23 citations), closing the open scope from Entry 34. MEPC.1/Circ.778/Rev.5 checked and current. | Found during the Entry 34 correction pass |
| 2026-08-19 | Entries 36–37: SQ teaser cited a non-existent MSC.1/Circ.1405/Rev.3 (correct is Rev.2, 25 May 2012; Rev.3 belongs to the companion flag-State circular MSC.1/Circ.1406) while the gated copy had already been corrected — teaser-drift class of error, now covered by a new citation-contradiction check in the health script; and the decorative file-header version badge, stale in all 5 files carrying it, removed in favour of the per-question q-version footer as sole version truth. | Found by a repo-wide teaser/gated citation comparison |
| 2026-08-21 | Entry 38: QB1_A Q25 (Fair Treatment of Seafarers) — Casualty Investigation Code omitted entirely (correct placement: preamble + Foreword para 6, mandatory Part II Ch 12 via SOLAS XI-1/6, recommended Part III Ch 24 — not "Part III" as the candidate had it); fabricated MLC "Regulation 5.2.7/Standard A5.2.7" replaced with Guideline B4.4.6(2) and Regulation 5.1.6; fabricated "LEG 110/111 outputs" on VDR/automated data removed (real instrument is LEG.7(112), 28 Mar 2025); Hebei Spirit chronology inverted; A.987(24) restated as remaining recommendatory, with MSC.255(84) Part II Ch 12 as a separate mandatory instrument. Q25 v1.0→v1.1, file v1.9→v2.0; SQ teaser fixed in the same session. | Candidate correction via Nixon (WhatsApp screenshot) |
| 2026-08-21 | Entry 38 refinement: A.987(24) does not itself contain the Guidelines — it is the Assembly resolution (1 Dec 2005) urging States and authorising promulgation; the Guidelines text was adopted by LEG.3(91) (27 Apr 2006) and the ILO Governing Body (296th session, 12 Jun 2006), promulgated 1 Jul 2006. UNCLOS Art. 230 and the MARPOL Annex I Reg 11 / Annex II Reg 6 damage-exception added from the resolution's recitals. Q25 v1.1→v1.2. | Verification against the A.987(24) resolution text |
| 2026-08-21 | Entry 39: SQ teaser copies of simon-notes-p1 and p2 cited MEPC.337(76)/MEPC.338(76) as the CII calculation and rating guidelines; correct are MEPC.336(76) (G1) and MEPC.339(76) (G4), with 337 = G2 reference lines and 338 = G3 reduction factors. Gated copies were already correct — teaser drift, Entry 36 class. Root cause noted: post-MEPC 76 session briefs circulated the quartet one number low. | Repo-wide scope pass following Entry 38; verified against the MEPC.338(76) primary text |
| 2026-08-21 | Entries 40–41: QB1_B Q15 said the Casualty Investigation Code "incorporates" the fair-treatment Guidelines (it cites them; its own mandatory protections are Part II Ch 12) and asserted an unverifiable requirement to assess medical fitness and fatigue before prolonged interrogation (removed); QB5_A Q4 cited MLC Reg. 2.7 as Recreational Facilities — 2.7 is Manning Levels, recreational facilities are Reg. 3.1. Q15 v1.1→v1.2, Q4 v1.0→v1.1. | Repo-wide scope pass following Entry 38 |
| 2026-08-22 | Entry 42: MSC.535(107) lifeboat ventilation — application rule was new-build-only with a "keel laid" test; resolution defines "installed" in two limbs and limb (b) catches existing ships | Candidate (Vivek) screenshot correction on QB2_F |
| 2026-08-23 | Entry 43: "main boilers" listed as a Vital Auxiliary System assessed under Continuous Machinery Survey (QB1_G Q40) - the boiler itself is not a CSM item and is not on the 5-year CSM interval; IACS UR Z18 §2 requires two internal examinations per 5-year period at a maximum 36-month interval, plus the §2.2 annual external survey, while §1.3 governs the CSM item cycle. Boiler auxiliaries (FD fans, burning pumps, feed water pumps) ARE in the class-approved CMS list per ClassNK Guidance on CMS Ver.4 (June 2025). The card's IACS PR 1C citation was also unsupported - PR 1C is suspension/withdrawal of class for overdue surveys - and was replaced with UR Z18. QB1_supplementary and QB1_F already state the boiler exclusion correctly and were not changed. | Candidate report via Nixon (WhatsApp screenshot) |
| 2026-08-23 | Entry 44: CSM/boiler answer re-framed in the Indian authority order — DG Shipping/DGMA statutory ("running survey", Rule 274), IRS class implementation (Main Rules Pt.1 Ch.2 §8.2/§1.4 and IRS-G-SUR-02), IACS UR Z18 as unified class baseline not a statutory authority, ClassNK demoted to implementation example. IRS 4.1.1(d) shows the real line is Chief Engineer CREDIT, not CSM eligibility, so the claim is narrowed to the boiler's pressure boundary being off the 5-year CSM interval; two ClassNK-derived pump types removed from the card. | Founder review following Entry 43 |
| 2026-08-23 | Entry 45: "DG Shipping / DGMA" written as a live pair on QB1_G Q40 — the authority is the Directorate General of Maritime Administration, named in full on first mention with "formerly DG Shipping" as a historical gloss and DGMA as the short form. Document titles carrying the old name ("DG Shipping Engineering Circular 02 of 2024" etc.) deliberately left unchanged; ten further files recorded for a separate scoped pass. | Founder correction following Entry 44 |
| 2026-08-24 | Entries 46-49: found by an INDEPENDENT clean-context review of the batch-G1 cards, and by a second independent pass over its own fixes. Rescue-boat 5-knot figure attached to recovery instead of launching (QB2_E Q1 and Q3, seven places including an SVG label and the page meta); MARPOL Annex VI Chapter 4 cited in pre-2021 numbering and GBS scope understated (QB1_C Q9); Baltic Dry Index described with a Handysize component eight years after its removal (QB8_A Q3); "TML = 90% of FMP" applied to iron ore fines, which has no FMP, plus a stale Group A definition (QB2_A Q31). Also corrected in the same pass: a revoked VTS resolution A.857(20) and SOLAS V/19-1 mislabelled as AIS (QB9_E Q9, QB3_G Q2), and the Pablo casualty described as producing an oil slick when she was in ballast. | Independent clean-context review, then a second independent pass over the fixes |
| 2026-08-24 | Entries 50-51: `QB1_G` Q32 carried a truncated Merchant Shipping Notice citation, "1 of 202" -- verified against the DGMA Nautical Wing source as **MS Notice 01 of 2026** (15 Jan 2026, empanelment and retention of salvors, s.255 MS Act 2025) rather than reconstructed from the truncation; and `QB8_A` Q3 shipped raw draft scaffolding to candidates, where two of the four `[cite: 1]` markers turned out to be inside the REAL reg-box rather than the `<pre>` duplicate, so deleting the obvious artefact alone would have left them live. Class-wide artefact scope enumerated and registered as OPEN-G1-008. | OPEN-G1-006 and OPEN-G1-007, closed from the August intake open-items register |
| 2026-08-25 | Entry 52: `QB2_F` Q3 credited the ro-ro / vehicle / special-category fire-safety package to **MSC.532(107)** across three blocks; the package is **MSC.550(108)** with FSS Code amendments in **MSC.555(108)**, and `QB10_B` Q1 already had it right, so two paid cards disagreed. Root cause is a shared 1 Jan 2026 entry-into-force date, not carelessness - identify a package by the regulation it AMENDS. Two further defects found in the same card: the 10 mg/kg PFOS threshold is MSC.1/Circ.1694, not SOLAS (II-2/10.11.2 is an unqualified prohibition); and SOLAS II-2/20 states application in each section chapeau, so summarising the requirements gave cargo ships the entire passenger-ship package. The last of these was found only by independent clean-context review. | OPEN-G1-010, and the AUG-0015 ro-ro ask it was blocking |
| 2026-08-25 | Entry 53: `QB9_G` Q6 taught a legal hierarchy Treaty → Convention → Protocol that international law does not recognise (VCLT Art.2(1)(a): a treaty “whatever its particular designation”), defined a Protocol as only an amendment, claimed every Protocol needs its own ratification (disproved by MARPOL Protocol of 1978 Art.IV(1)) and dismissed an IMO Resolution as committee guidance (SOLAS Art.VIII(b) amendments are adopted BY MSC resolution). Q3’s instrument ladder carried the same resolution defect. All three `QB9_G_CheatSheet` copies reconciled. Definition-source rule recorded once at `Claude skill/miw-correction-workflow_SKILL.md` §2a. | Founder review while studying from the MIW study roadmap |
| 2026-09-02 | Entry 64: three cards taught a consequence their instrument does not carry. `QB5_I` Q8 said ISM 10.3 *drives*/*derives* the critical-spares list and that an unobtainable spare *is* an ISM 9 non-conformity, and had filed 10.3's reliability and stand-by-testing limbs under 10.4 - corrected against A.741(18) as amended by MSC.273(85), with ISM 9 made conditional on ISM 1.1.9. `QB2_A` Q11 and Q33 said the Document of Authorisation is *invalid* without the booklet - corrected to Grain Code A 3.1/3.2/3.5 and A 6.1, closing the H6 terminology limitation. `QB9_H` Q10 shipped five candidate-visible editorial placeholders - removed by RETRIEVING the MS Act 2025 corrigenda (three typographical fixes, no renumbering) and citing Part V s.63/64/83(1)/94(1) from the Act itself. Raised by GPT content review of the H6 packet; the 10.3/10.4 mis-citation and the Q33 sibling were found by the scope pass, not reported. | H6 terminology limitation on the grain loading booklet |

### 50. A truncated citation is worse than no citation

`QB1_G.html` Q32 asked about the empanelment of salvors and carried its authority in the
question stem as **"( ms notice 1 of 202)"**. **202 is not a year.** The card body never
states the number anywhere else -- it refers only to "the relevant Director General of
Shipping (DGS) Merchant Shipping Notice" -- so the truncated string was the whole of the
citation a candidate could take into the room.

The instrument is **MS Notice No. 01 of 2026, dated 15 January 2026**, prescribing the
checklist for **empanelment and retention of salvors** under **Section 255 of the Merchant
Shipping Act 2025**, with applications commencing **01 March 2026**.

Two lessons, and the second is the general one.

* The missing digit was **read from the DGMA source, not inferred from the truncation**.
  "202" is equally consistent with 2020, 2021, 2022 and 2026, and a plausible guess in a
  citation is indistinguishable to a candidate from a verified one.
* A question stem is **not decoration**. It is emitted into the page JSON-LD, into the cheat
  sheet cue and into the generated examiner index, so a defect there is reproduced on every
  derived surface -- and correcting it moves display text that several generated files pin.

### 51. Draft scaffolding shipped to candidates, and the copy that survives the cleanup

`QB8_A.html` Q3 -- a paid card -- shipped its own authoring scaffolding live: four
`[cite: 1]` markers, an ASCII **REGULATORY REFERENCE BOX** inside a `<pre>` duplicating the
real reg-box, a second copy of the CE Oral Tip, ten literal markdown `---` rules rendered as
visible paragraphs, the word "arrow" where a glyph belonged, and a draft footer reading
**QB8 Q16 v1.0** inside a card whose real footer reads **QB8 Q3 v1.1**.

The trap is in the repair, not the defect. **Two of the four `[cite: 1]` markers were inside
the REAL reg-box**, not the duplicate. Deleting the obvious artefact -- the `<pre>` block --
would have removed two markers, looked complete, and left two live on the page. This is the
same shape as fixing prose and leaving the summary, the SVG label or the meta description
stale: **after any repair, search the whole card for the pattern, not the block you were
looking at.**

Second lesson: **verify redundancy before deleting**. Each removal here was checked against
the surviving copy first -- the ASCII box's four references are all carried by the real
reg-box, which holds a fifth besides, and the duplicated tip matched word for word. A
"duplicate" that is not actually a duplicate is content loss dressed as tidying.

Scope: these artefact classes are **not confined to that card**. `[cite: N]` appears 65
times across 4 files, `<p>---</p>` 251 times across 10, and the ASCII box and draft footer
22 times each across 3. Recorded as OPEN-G1-008 rather than swept.

### 52. Resolutions adopted into the same entry-into-force tranche are not interchangeable — identify a package by what it AMENDS

`QB2_F.html` Q3 credited the ro-ro, vehicle and special-category-space fire-safety
requirements to **MSC.532(107)**, in its 15-Second block, its 60-Second block and its body.
That package is **MSC.550(108)**, with the FSS Code amendments in **MSC.555(108)**.
`QB10_B.html` Q1 had it right, so two paid cards in the bank contradicted each other, and
`QB10_B`'s own CE Oral Tip says Nair asks for the resolution number verbatim.

The confusion is structural, not careless. **MSC.532(107) and MSC.550(108) share an
entry-into-force date of 1 January 2026** and both amend SOLAS chapter II-2, so a
session brief that lists the 2026 tranche puts them side by side. They are different
packages adopted a year apart:

* **MSC.532(107)**, adopted **8 June 2023** — II-2/10.11 PFOS prohibition (and II-2/1.2.10
  for existing ships), new II-1/3-13 lifting appliances and anchor handling winches,
  V/19.2.12 electronic inclinometers, and the chapter XIV Polar Code extension to
  non-SOLAS ships. It **never touches II-2/20 or II-2/7**.
* **MSC.550(108)**, adopted **23 May 2024** — II-2/20 rewritten for vehicle, special
  category, open and closed ro-ro spaces and weather decks intended for vehicles;
  II-2/7.5.2 and 7.5.5 detection; II-2/4.2.1.9 oil-fuel quality; plus chapter V/31 and
  V/32 container-loss reporting.
* **MSC.555(108)**, adopted 23 May 2024 — FSS Code chapters 7 and 9.

**The rule: identify an amendment package by the regulation it amends, not by the
resolution number nearest to it in a tranche list.** Open the annex and read which
chapter and regulation headings it contains. A one-minute check of the resolution's own
table of amended regulations settles it; a plausible neighbouring number does not.

Two further defects were found in the same card while correcting it, and both are their
own reusable lesson:

* **A threshold can be attributed to the wrong instrument even when the number is right.**
  The card said MSC.532(107) prohibits PFOS media "above 10 mg/kg". The regulation text is
  an unqualified prohibition — *"use or storage of extinguishing media containing
  perfluorooctane sulfonic acid (PFOS) shall be prohibited"*. The **10 mg/kg (0.001% by
  weight)** figure is the unified interpretation in **MSC.1/Circ.1694** (4 July 2025),
  mirrored by IACS UI SC309. Quoting a UI figure as if it were treaty text is a citation
  error even though the number is correct.
* **Application lives in the chapeau, not in the requirement.** SOLAS II-2/20 states which
  ships each section catches in the *introductory paragraph* of that section, not beside
  the requirement. Reading the requirements and summarising them produced a card that gave
  cargo ships the entire passenger-ship package: 20.4.1's chapeau confines 20.4.1.1–.1.4
  to passenger ships and gives cargo ships only 20.4.1.5, and video monitoring (20.4.4),
  weather-deck monitors (20.6.2), structural fire protection (20.5) and decision-making
  signage (20.7) are all passenger-ship duties. This was found by an **independent
  clean-context review**, not by the producing pass, which had read the same PDF.

### 53. An instrument’s TITLE is not a legal rank — and “resolution” is not a synonym for “non-binding”

`QB9_G.html` Q6 answered “Convention vs Protocol vs Treaty” with a hierarchy it printed under
its own heading: **Treaty → Convention → Protocol**. International law recognises no such
ladder. **VCLT 1969, Art.2(1)(a)** defines a treaty as *“an international agreement concluded
between States in written form and governed by international law, whether embodied in a
single instrument or in two or more related instruments and whatever its particular
designation”*. That closing phrase is the whole point: “Convention” and “Protocol” are **titles
reflecting treaty practice**, not tiers. A Convention is a treaty; a Protocol is a treaty.

Four defects travelled with the hierarchy, all in the same card, and three of them were
also in `QB9_G_CheatSheet.html` — the diagram caption, the Convention-vs-Protocol confusable
box and the Q554 flip-card answer. **Candidates memorise the cheat sheet first, so a
corrected answer beside a stale mnemonic still fails.**

* **A Protocol is not by definition an amendment.** The UN Treaty Collection records
  protocols of signature, optional protocols, protocols based on a framework treaty,
  protocols to amend, and protocols as a supplementary treaty. “Major structural
  add-on/update” was MIW shorthand presented as terminology.
* **“A Protocol requires its own separate ratification” is false as a universal.** VCLT
  Art.11 allows consent by signature, exchange of instruments, ratification, acceptance,
  approval, accession, *or any other means if so agreed*, and the **instrument’s own final
  clauses** decide which. The card’s own flagship example disproves it: **MARPOL Protocol
  of 1978, Art.IV(1)** lets a State become a Party by signature without reservation as to
  ratification, by signature followed by ratification/acceptance/approval, **or by
  accession**.
* **There is no universal rule that the parent Convention must be ratified first.** The
  card said “generally no”. Compare, inside one regime: the **1978 Protocol** is open to
  States generally and its Art.I(1) binds Parties to give effect to the 1973 Convention as
  modified, while the **1997 Protocol, Art.5(1)** provides that *only* Contracting States
  to the 1978 Protocol may become Parties to it. Same convention, opposite answers —
  read the final clauses.
* **“An IMO Resolution is committee guidance without independent treaty force” is wrong.**
  A resolution is a formal decision of an IMO organ and the word alone settles nothing.
  Amendments to the SOLAS annex are **adopted by MSC resolution** under **SOLAS
  Art.VIII(b)** and bind Contracting Governments through tacit acceptance; **MSC.48(66)**
  adopted the LSA Code and **MSC.47(66)** adopted the SOLAS chapter III amendments that
  made it mandatory on or after 1 July 1998. Only *some* resolutions stay recommendatory —
  `QB1_A` Q25 (A.987(24)) and `QB2_G` Q1 (A.1048(27)) already scoped that correctly and
  were **not** changed.

The same wrong rung was live in `QB9_G.html` **Q3**, whose instrument ladder read
“Guideline, circular or resolution — recommendatory”. Q3 and Q6 are now consistent, and Q3
states explicitly that its ladder ranks instruments by *what makes them binding on you*,
not by legal class.

**The governing rule this produced** is recorded once, at
`Claude skill/miw-correction-workflow_SKILL.md` §2a: official definition first, MIW
explanation second, clearly labelled as MIW’s own wording, never universalised beyond the
instrument’s scope. Q6 v1.0→v1.1, Q3 v1.0→v1.1.

GREP: SKIP — the corrected text deliberately quotes the wording it rejects
(“Treaty → Convention → Protocol”, “always requires ratification”, “resolution” beside
“recommendatory”) so a phrase scan can only ever fire on the fix. Verify by reading the
sentence: every mention must be **negated or quoted**.

### 54. Naming BMP5 as the current security guidance — and the currency question that cannot find a second edition

Five live cards taught **BMP5** as the standard in force. It is not. **BMP Maritime Security
(BMP MS)** was published on **31 March 2025** by **BIMCO, ICS, IMCA, INTERCARGO, INTERTANKO and
OCIMF**, and it states that it **replaces all the existing versions of the BMP** — BMP5, the
Global Counter Piracy Guidance and BMP West Africa. A **second edition followed in 2026**. An
examiner who asks “what do you follow for a Red Sea transit?” in a 2026 oral is asking about a
publication that has now superseded its own first edition twice over the guidance the card named.

* **Say the supersession before the technique.** BMP5's hardening, citadel, lookout and
  reporting content is still examinable and is still correct as technique — it is the
  **edition label** that fails you. Answer “BMP Maritime Security, which replaced BMP5 in 2025;
  the measures are…”, never “BMP5 says…”.
* **Do not re-region-lock it.** BMP5 was scoped to the Red Sea, Gulf of Aden, Indian Ocean and
  Arabian Sea; BMP West Africa to the Gulf of Guinea. BMP MS is **deliberately global** and
  covers **state and non-state threats** — missile, drone and sea-mine attack as well as piracy
  and armed robbery. “Which High Risk Area does it apply in?” is a question built on the model it
  replaced. It is **voluntary industry guidance**; **SOLAS Ch. XI-2 and the ISPS Code** are the
  mandatory instruments it helps you discharge.
* **The trap behind the trap — a currency check that cannot fail correctly.** The first version
  of this correction taught the **2025 first edition** as current, because the currency record
  behind it asked only *“does BMP MS supersede BMP5?”*. That question answers **yes**, truthfully,
  and is **structurally incapable** of revealing a later edition of BMP MS itself. The question
  that finds it is *“what has the authoritative publisher said MOST RECENTLY about this subject?”*
  The rule is recorded at `docs/sources/MIW_SOURCE_REGISTRY.json` under `query_discipline`, and it
  is why that registry exists.

GREP: SKIP — every corrected card still names BMP5 on purpose, as the predecessor. A phrase scan
for “BMP5” fires on the fix. Verify by reading the sentence: each mention must be **labelled as
superseded** or **scoped to technique**, never presented as the guidance in force.

### 55. The Grain Code has THREE loading configurations since 1 January 2026, not two

Every Grain Code answer built before 2026 teaches two compartment configurations —
**filled** and **partly filled** — each with its own assumed volumetric heeling moment.
**Resolution MSC.552(108)**, adopted **23 May 2024** and in force **1 January 2026** for
**new and existing ships alike**, added a third:

> **“specially suitable compartment, partly filled in way of the hatch opening, with ends
> untrimmed”** — new definition **A 2.8**.

* **What it permits.** New **A 10.4**: the hold is filled to a level **equal with or above the
  bottom edge of the hatch end beams**, but the grain **outside the periphery of the hatch
  opening may lie at its natural angle of repose** — so **dispensation may be granted from
  trimming the ends**. Amended **A 10.7** then requires only the surface **in way of the hatch
  opening** to be level. The commercial driver is the cost, time and confined-space exposure of
  end-trimming a hold.
* **What it costs.** The relief is bought with harsher assumed geometry, not with a lower pass
  mark. New **B 1.1.5**: after loading, the surface is assumed to slope in all directions at
  **30°** from the lower edge of the hatch end beam. New **Part B section 4**: after shifting,
  the surfaces are assumed at **25°** to the horizontal. **B 1.5** carries the
  **1.12 × transverse heeling moment** vertical-shift factor into the new category.
* **What did NOT change.** The three intact-stability criteria are untouched — **12°** maximum
  heel, **0.075 m·rad** residual area to 40°, **0.30 m** minimum corrected GM — and so is the
  Document of Authorisation regime. A candidate who says the criteria were relaxed has inverted
  the amendment.
* **The attribution trap inside the trap.** It is widely and correctly said that an owner using
  the new option must have the **approved grain loading manual updated** — the ship can only be
  loaded to a condition its booklet covers. That is **class-society and P&I guidance**, and it is
  **not in the text of MSC.552(108)**. Give the point, but label it.
* **Do not confuse it with the IMSBC Code.** **MSC.575(110)**, IMSBC amendment 08-25, is a
  different code on a different timetable — voluntary from 1 January 2026, envisaged entry into
  force 1 January 2027.

GREP: SKIP — the corrected card deliberately names both old configurations while adding the
third, so a phrase scan for “filled” or “partly filled” fires on the fix. Verify by reading the
sentence: wherever the configurations are enumerated, **all three** must appear.

### 56. “Freedom of navigation” has a condition, and it is the words *due regard*

A 31 August 2026 candidate was asked for **freedom of navigation** and then, as the follow-up,
for the **condition of** freedom of navigation. Most candidates answer the first and stall on the
second, because the freedom is taught as though it were unqualified. It is not.

* **In the EEZ — Article 58(3).** A State exercising its Article 58 freedoms *“shall have due
  regard to the rights and duties of the coastal State and shall comply with the laws and
  regulations adopted by the coastal State”* in accordance with the Convention.
* **On the high seas — Article 87(2).** The Article 87 freedoms *“shall be exercised…with due
  regard for the interests of other States in their exercise of the freedom of the high seas”*.

**Say “due regard” and give both articles.** That single phrase is the answer to the condition
limb in both zones, and a candidate who produces it has visibly read the Convention rather than a
summary of it.

**Do not confuse the freedom with innocent passage.** They are different rights in different
zones under different articles: innocent passage (Arts. 17–19) operates in the **territorial
sea**, is subject to the passage being continuous, expeditious and not prejudicial, and can be
lost; freedom of navigation operates in the **EEZ and high seas** and is qualified by due regard,
not by innocence. Answering “freedom of navigation is innocent passage” collapses two regimes and
is the single commonest error on this question.

GREP: SKIP — the corrected card names innocent passage deliberately, in order to distinguish it.
Verify by reading the sentence: every mention must be drawing the distinction, never equating the
two.

### 57. The Oil Record Book section letters never changed — the section *wording* did, in 2011

Every Oil Record Book answer written before 2011 still **looks** right, because the letters are
the same. **Resolution MEPC.187(59)**, in force **1 January 2011**, replaced **Part I sections
(A) to (H)** in their entirety and **Part II section (J)**. Section **(I)** was not replaced.

* **(C)** became **“Collection, *transfer* and disposal of oil residues (sludge)”**, and gained an
  item recording the **quantity collected by manual operation**.
* **(D)** and **(E)** changed from *“non-automatic / automatic **discharge** overboard or disposal
  otherwise”* to *“non-automatic / automatic **starting of** discharge, **transfer** or disposal
  otherwise”*.
* The same resolution replaced the word “sludge” with the defined term **“oil residue (sludge)”**
  in regs 12.2, 13, **17.2.3**, 38.2 and 38.7, and **deleted “and other oil residues”** from
  reg. 17.2.3.

**The thread running through all of it is *internal transfer*.** Moving oily water or sludge
between tanks was not expressly recordable before 2011, and unrecorded internal transfers were how
quantities were made to disappear between the tanks and the book. A candidate who says “(C) is
collection and disposal of sludge” is giving the pre-2011 answer.

**Two more that get answered wrongly by habit:**

* **Part I is not “all ships”.** Reg. 17.1: **oil tankers of 150 GT and above** *and* **other ships
  of 400 GT and above**. Two different thresholds.
* **The master signs the page, the officer in charge signs the operation** (reg. 17.4). A Chief
  Engineer countersignature is common company practice and is **not** a MARPOL requirement — do not
  present it as one.

**And an electronic ORB must be *approved*.** Reg. 1.39, added by **MEPC.314(74)** in force
**1 October 2020**, defines an Electronic Record Book as one *“approved by the Administration”*.
An unapproved software log is not an ORB.

GREP: SKIP meoclass1/QB3_F.html#q10, meoclass1/QB1_F.html#q2, meoclass1/QB5_A.html#q20 — these three
deliberately state the superseded wording in order to reject it, and only these three.

**The skip is deliberately narrow, and here is the reason.** `QB1_supplementary.html#q6` is the one
card that prints the section letters as a list to be **memorised**, not rejected. When this trap was
first written its skip was blanket, which would have disarmed the guard over precisely the card
most able to teach the wrong answer — it carried the pre-2011 headings for (B), (C), (D), (E) and
(F) under the instruction “know all ORB code letters by memory”. It has been corrected to the MEPC.187(59)
wording; the guard must stay armed over it so that a future edit cannot quietly restore the old
list. A blanket skip on a currency trap protects the defect it was written to catch.

### 58. IACS UR Z7 is HULL. Machinery surveys are Z18, and the PMS alternative is Z20

The Oral bank stated in four places that Continuous Machinery Survey is governed by
**"IACS UR Z7/Z7.1"**. It is not. From IACS's own consolidated Unified Requirements Z contents
page:

* **Z7** — *Hull classification surveys*
* **Z18** — *Survey of machinery* (1.3 continuous surveys, 1.5 planned maintenance scheme,
  1.6 condition monitoring / CBM)
* **Z19** — *Calibration of measuring equipment*
* **Z20** — *Planned maintenance scheme (PMS) for machinery*
* **Z27** — *Condition Monitoring and Condition Based Maintenance*

**And the certificate has a name.** UR Z20 2.3.1: *"When the PMS is approved a 'Certificate of
Approval for Planned Maintenance Scheme' is issued. However, other equivalent certification or
class notation may be issued according to the procedure in use in each individual Member Society.
In any case, the certification is to be kept on board."* It is a **class** document. There is no
statutory or IMO PMS certificate — ISM section 10 requires the maintenance system and certifies
nothing.

**How the error survived.** The corpus area for class material held only a notes file. A note
asserting what a Unified Requirement says is not evidence of what it says, and an unsourced area of
a corpus does not announce its own errors — the mistake surfaced only when a new card needed the
real citation and the publisher's document was finally acquired.

GREP: `UR Z7` — the only legitimate uses are statements that Z7 is hull classification surveys.
Any sentence pairing Z7 with machinery, CMS, CSM or continuous survey is wrong.

### 59. MEPC.328(76) entered into force 1 November 2022 — not 2023

The revised MARPOL Annex VI adopted by **resolution MEPC.328(76)** was **deemed accepted 1 May
2022** and **entered into force 1 November 2022**, per the resolution's own operative paragraphs 2
and 3. **Secondary summaries circulate with the year wrong, giving 1 November 2023**, and a card in
this batch inherited that wrong year.

**It was inherited from our own corpus, which is the point.** The MARPOL Annex VI canonical layer
in the shared true-source corpus records the entry into force as `2023-11-01`, and the card author
trusted that record rather than the resolution. This is the *"an index row is not evidence"* rule
biting from an unexpected direction: the derived record was ours, it was carefully built, it was
frozen and qualified — and it was still wrong on a date that the underlying PDF states in one line.
A corpus record is a pointer to a source, never a substitute for it, **including when the corpus is
your own**.

**A second wrong variant, and why this entry did not catch it.** This trap was registered during
the H series with a GREP naming one spelling: `1 November 2023`. QB7_A and its cheat sheet carried
a *different* wrong value for the same fact — **1 January 2023** — in six places, and the guard was
blind to all six. The shared corpus independently hit a third form, `EIF 2023-01-01`, in its own
amendment register. One fact, three wrong renderings, and a guard written for one of them.

`1 January 2023` is the more dangerous variant because it is a REAL date in this subject: it is
when the CII and SEEMP Part III **obligations apply** — the first data-collection year. So the card
was not inventing a date, it was **collapsing two limbs into one**, exactly as the MSC.535(107)
ventilation card did. State them as two things:

* **1 November 2022** — MEPC.328(76) enters into force (adopted 17 June 2021, deemed accepted
  1 May 2022).
* **1 January 2023** — the first year the CII and SEEMP Part III obligations apply.

**The rule.** A banned-phrase guard protects against the spelling you happened to see, not against
the fact you got wrong. Where a date is the subject, assert the PROPOSITION — this instrument
entered into force on this date — and let the guard fail on any other value, rather than listing
the wrong ones.

GREP: `1 November 2023` — legitimate only where an instrument genuinely entered into force on that
date. Paired with MEPC.328(76) or with "Annex VI", it is wrong. Likewise any entry-into-force or
"effective" claim for MEPC.328(76) that gives **1 January 2023**: that is the application date of
the obligations, never the entry into force of the amendments. GREP: SKIP for this entry's own
prose, which quotes both wrong forms in order to reject them.

### 60. MEPC.333(76) is EEXI. The CII guidelines are the 336-339 series

The Oral bank stated in four places on one card, and once on its cheat sheet, that the required
CII reference values and the **A-E rating bands** come from **MEPC.333(76)**. They do not. From
IMO's own published resolution, first page:

> *RESOLUTION MEPC.333(76) (adopted on 17 June 2021) 2021 GUIDELINES ON THE METHOD OF CALCULATION
> OF THE ATTAINED ENERGY EFFICIENCY EXISTING SHIP INDEX (EEXI)*

It is an **EEXI** instrument. The operational carbon intensity guidelines adopted at the same
session are a different run of numbers:

* **MEPC.336(76)** - CII Guidelines, **G1** (calculation methods)
* **MEPC.337(76)** - CII **Reference Lines** Guidelines, **G2**
* **MEPC.338(76)** - CII **Reduction Factors** Guidelines, **G3**
* **MEPC.339(76)** - CII **Rating** Guidelines, **G4** - the A-E bands
* **MEPC.364(79)** - the carbon conversion factors C_F (HFO 3.114, MDO/MGO 3.206, LNG 2.750,
  methanol 1.375)

**Why this one was expensive.** The wrong number was not a passing citation. It sat in that card's
*Numbers & Regulations to Memorise* list **and** in its *Common CE Failures* list, as the
distinction a candidate must be able to draw against MEPC.364(79) - so the corpus was drilling it.
The same card's CE Oral Tip records that Nair asks for these numbers verbatim. And the card
separately, and correctly, warns against *"confusing EEXI (one-time, technical) with CII (annual,
operational)"* - which is precisely the error it was making one paragraph away.

**How it survived.** It was found only because a new card on CII-improvement technologies needed
the reference-line and rating instruments by name, inherited the citation from the corpus, and an
independent reviewer checked it at IMO rather than against the bank. A number repeated confidently
in three places on the same page reads as verified; repetition is not corroboration.

GREP: `MEPC.333(76)` - legitimate only where the subject is **EEXI calculation**. Paired with CII,
with rating bands, or with reference lines, it is wrong.


### 61. A membership count is a dated claim, and ours disagreed with itself three ways

Three Oral cards carry MACN. Before this correction they said, between them, **"150+ member
companies"**, **"200+ member companies, >50% of global tonnage, active in 50+ countries"**, and no
figure at all. MACN's own site says **"Over 225"** members across **"Over 45"** countries. A
candidate who revised from two of our pages would have walked in with two different numbers for one
organisation, and a share-of-global-tonnage figure that **MACN does not state anywhere we could
find** - it comes from secondary maritime reporting.

**The rule for any organisation-scale number.** Quote the issuer's own figure, **say the date you
read it**, and stop. *"Over 225 members across more than 45 countries, as of my last reading"* is a
better answer than a confident bare number, because the examiner asking about a network's scale is
usually testing whether you know it moves.

**And the currency question this sits under.** *"MACN, latest outcome?"* is not an identity
question. MACN is a private network - it issues no certificates and adopts no instruments, so there
is no resolution to cite. Date your answer and name a development you can actually stand behind.

**How the corpus's own hedge went wrong.** Production first recorded "which annual report is
current" as **unverifiable**, having read MACN's front page (still leading on the 2024 report) and
its news listing (which names no report at all). The issuer's **publications index** answers
outright: *MACN 2025 Annual Report*, posted May 2026. Two surfaces of a publisher disagreeing is
not evidence that the publisher is silent - go to its index. This is the same failure that, in the
same batch, had a DGS notice recorded as unretrievable while a scan of it sat in the repository.

GREP: `150+ member` / `200+ member` / `% of global tonnage` - all wrong for MACN.

### 62. SOLAS II-2/10.7.3 has TWO triggers, and both directions of the error have now been made

Regulation 10.7.3 applies to ships **constructed on or after 1 January 2016** designed to carry
containers on or above the weather deck. Inside it are two different requirements with two
different conditions:

* **10.7.3.1 — water mist lance.** Every such ship carries **at least one**. The only condition is
  the build date.
* **10.7.3.2 — mobile water monitors.** Only ships **designed to carry five or more tiers on or
  above the weather deck** carry them as well: at least two if breadth is under 30 m, at least
  four if breadth is 30 m or more.

**Both directions of this error have been made in this corpus, a year apart.** An earlier version
of the QB2_A container-fire card told candidates that lances and monitors were *company practice
rather than SOLAS* — understating a live requirement. The CE Oral Tip written for that same card in
September 2026 then made the opposite error, sweeping the monitors under the lance's build-date
condition and dropping the five-tier precondition entirely. An independent reviewer caught it
before it shipped.

The two failures look like opposites and are the same failure: **a compound regulation summarised
down to one condition**. When a regulation carries more than one trigger, a summary that keeps only
the trigger you happened to be thinking about is not a shorter answer, it is a different rule.

**And keep the third boundary separate.** The firefighting equipment above is *in force*. What is
still **draft** is the separate IMO workstream on enhanced **detection and control** of container
fires. Sweeping the in-force equipment into the draft bucket is the failure the earlier card made;
answering *"not mandatory"* to a live SOLAS requirement is the version of it a panel will punish
hardest.

GREP: SKIP for this entry's own prose, which states the wrong readings in order to reject them.
Elsewhere: mobile water monitors asserted without the five-tier condition, or 10.7.3 cited as a
single undifferentiated requirement, is wrong.

### 63. An intake CLASSIFICATION is not a production DISPOSITION

`AUGUST2026_INTAKE_ADJUDICATIONS.json` records, per occurrence, a
`classification` such as `GENUINE_NEW_QUESTION`. That field is frozen at intake
and answers exactly one question: **did a matching card exist when this ask was
first scored?** It is not, and was never, the decision about what gets built.

The decision lives somewhere else — in
`AUGUST2026_PRODUCTION_QUEUE.json` under `production_outcomes`, written after
the reuse-first pass and after independent review. Three August occurrences make
the gap concrete. AUG-0095 (freedom of navigation), AUG-0140 (crew entitlements
onboard) and AUG-0148 (grain loading booklet) are all `GENUINE_NEW_QUESTION` in
the adjudication file **and all three were disposed without a new card**:
`QB1_A#q19` already carried the UNCLOS zones and, after
`CORR-UNCLOS-FREEDOM-20260831`, the Art. 58(3)/87(2) "due regard" condition;
`QB9_H#q10` carried the SEA under Std A2.1; `QB2_A#q11` carried the Grain
Stability Booklet and its Document of Authorisation.

**A reader who takes `classification` as the work order will commission
duplicate roots against live cards** — and, in the AUG-0095 case, against a
correction that had already shipped to answer the very limb being re-asked. A
production brief written from the adjudication file alone did exactly that on
2026-09-02, scoping five cards where two were owed.

GREP: SKIP for this entry's own prose, which quotes the superseded readings in
order to reject them. Elsewhere: citing an occurrence's `classification` as
authority to build, without reading its `production_outcomes` disposition, is
wrong.


### 64. What a regulation REQUIRES, what an SMS DERIVES from it, and what a candidate is told is mandatory

Three cards taught a consequence their governing instrument does not carry. The
shape is identical in all three, and it is not carelessness: each began from a
true proposition and then travelled one step further than the text supports.

**`QB5_I#q8` - ISM Code 10.3.** The card said the critical-equipment list under
10.3 *drives* the critical-spares list, that the spares list is *derived* from
it, and that an unobtainable critical spare *is* a non-conformity under ISM 9.
Read from resolution A.741(18) as amended by MSC.273(85) item 7, 10.3 says only
this: the Company should **identify** equipment whose sudden operational failure
may result in hazardous situations; the SMS **should provide for specific
measures** aimed at promoting the reliability of that equipment; those measures
**should include the regular testing of stand-by arrangements** and equipment not
in continuous use. There is no statutory spares list, no minimum stock and no
reorder point in it. The correct hierarchy is
**10.3 identifies -> the SMS and PMS translate -> the CE manages stock**, and the
spares list is *informed by* 10.3 and then built from maker recommendations,
class and statutory requirements, PMS scope, failure consequence, redundancy,
lead time, consumption and trading pattern.

ISM 9 is the reporting and analysis route for non-conformities, accidents and
hazardous occurrences. Whether procurement failure produces one is answered by
**ISM 1.1.9** - objective evidence of the non-fulfilment of a *specified*
requirement - not by the fact that the spare is missing. The defensible oral
answer is conditional: assess against the SMS and the critical-equipment
requirements, weigh redundancy and operational risk, escalate, impose an
operational limitation or repair plan, and report under ISM 9 where the
condition meets the company's own definition.

**The same card also mis-filed the Code.** 10.3's second and third limbs - the
reliability measures and the stand-by testing - were attributed to **10.4** in
the body, the reg-box, the Casualty-Link deep-dive and the page cheat sheet,
while 10.4's actual content (*the 10.2 inspections and the 10.3 measures are
integrated in the ship's operational maintenance routine*) appeared nowhere.
Nobody reported that; the scope pass found it. **An overstatement and a
mis-citation travel together**, because both come from paraphrasing an
instrument instead of reading it.

**`QB2_A#q11` and `#q33` - International Grain Code.** The card said *"The DoA is
invalid unless accompanied by an approved Grain Stability Booklet"*. The Code
attaches no such invalidity. **A 3.2**: the document *"shall accompany or be
incorporated into the grain loading manual"*. **A 6.1**: the information is
provided *"in printed booklet form"*. **A 3.5** handles the no-document case - the
ship *shall not load grain* until the master demonstrates compliance to the
Administration or the port-State Contracting Government. **A 3.1** gives the
document's real effect: it *"shall be accepted as evidence that the ship is
capable of complying"*. Four terms, four different jobs: *grain loading manual*
is the Code's term for the document, *printed booklet form* is the required
format, *grain loading booklet* is acceptable shorthand, and the *Document of
Authorization* is separate authorisation evidence. Naming the consequence
("invalid") is what a candidate repeats to a panel, so it is the part that must
match the instrument.

**`QB9_H#q10` - a placeholder is not a caveat.** The live paid card carried
*"[cite the 2025 Act at Part level; the 1958 sections must not be quoted as
current]"* - an instruction addressed to the author - inside the 60-second
answer, plus four *"[Part-level, sections pending verification]"* instances. The
hold behind them was real and recorded: `SRC-MSACT-2025` said section numbers
outside s.4 and s.5 were not established until the 30 September 2025 corrigenda
was held. **The fix was to close the hold, not to soften the wording.** The
corrigenda was retrieved from DGMA and is three typographical corrections with
no renumbering, so Part V could be read directly: s.63 (agreement with
seafarers, copy to the shipping master, examine-and-advise before signing),
s.64 (wages, monthly account), s.83(1) (disputes), s.94(1).

**Distinguish the two things that look alike.** An imperative addressed to the
author is scaffolding and must never ship. *"(exact 2025 section pending
verification)"* is an honest candidate-facing currentness caveat and is a
legitimate shippable state - the same principle as `CURRENTNESS_UNVERIFIED` in
the source registry. The corpus carries 22 further instances of the second kind
and they are reported for sizing, not swept.

Files affected: `meoclass1/QB5_I.html` (q8 and the page cheat sheet),
`meoclass1/QB2_A.html` (q11 and q33), `meoclass1/QB9_H.html` (q10). Governed by
`CORR-ISM-SPARES-20260902`, `CORR-GRAIN-TERMINOLOGY-20260902` and
`CORR-MSACT-SEA-20260902`, each declaring supersession from the record that
previously pinned the card rather than rebaselining it.

**And the reason a digest pin did not catch any of it:** H6's pin on `QB5_I#q8`
and `CORR-GRAIN-MSC552-20260831`'s pin on `QB2_A#q11` were both green
throughout. A pin answers *"are these the bytes we authorised?"*, never *"is what
we authorised correct?"* - SKILL.md section 8.2a, now demonstrated on a card the
same session had just shipped.

GREP: SKIP. This entry quotes every rejected formulation - "drives", "derived
from", "invalid unless accompanied", "pending verification" - in order to reject
them, so a phrase scan matches the correction itself.
