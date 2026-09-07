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
Global Counter Piracy Guidance and BMP West Africa. It remains the **1st Edition (2025)**,
updated during 2026 with the activist-boarding guidance; **the publishers label no second
edition**, so “the 2026 edition” is itself a trap — see entry 80. An examiner who asks “what do you
follow for a Red Sea transit?” in a 2026 oral is asking about a publication that superseded the
guidance the card named.

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
* **What did NOT change.** The three intact-stability criteria are untouched — **A 7.1.1**, heel
  due to the assumed shift not greater than **12°**, or the deck-edge immersion angle for ships
  constructed on or after 1 January 1994, whichever is the lesser; **A 7.1.2**, the net or residual
  area **between the heeling arm curve and the righting arm curve**, taken from the **angle of
  equilibrium** up to the **least** of the maximum-difference angle, **40°** and the angle of
  flooding, not less than **0.075 m·rad**; and **A 7.1.3**, **0.30 m** minimum corrected GM — and
  so is the Document of Authorisation regime. A candidate who says the criteria were relaxed has
  inverted the amendment.
* **AUTHORING RULE — never write the A 7.1.2 criterion in the short form.** “0.075 m·rad residual
  area to 40°” is wrong twice over: **40° is one of three upper limits** and commonly not the
  governing one, and the area is **between two curves**, not “under the GZ curve”. That short form
  is the authoring source of the defect corrected in **QB2_A q11, q27 and q33**. Whenever this
  criterion is written into any card, all three limits and the between-the-curves formulation go
  with it.
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

### 65. "Consolidated" is not the C in CIC — and the copy that had been right all along was the one nobody read

`QB8_C.html#q4` asked the candidate to explain CIC and expanded it in the question
stem as **"Consolidated Inspection Campaign"**. There is no such thing. The port
State control term is the **Concentrated Inspection Campaign**, and the Paris MoU
and Tokyo MOU name it themselves in their joint press release of 3 August 2026:
*"The Member Authorities of the Tokyo MOU and Paris MoU will undertake a
Concentrated Inspection Campaign (CIC) on Cargo Securing of Cargo Units and Cargo
Transport Units. This CIC will be conducted from 1 September to 30 November 2026."*

**The card's own answer body was already correct.** Its second heading reads
"CIC Type 2: PSC Concentrated Inspection Campaign (Tokyo MOU / Paris MOU)", and
the three-month window it teaches is the window the press release states. So the
page contradicted itself, and the wrong half was the half a candidate reads first
and the half every generated surface copies.

Three lessons.

* **A card can disagree with itself, and a self-consistency check would have found
  this in a second.** Nothing in the release suite compares a stem against its own
  body. The defect survived a clean 77-gate qualification because every gate asked
  whether the bytes were the authorised bytes, never whether the two halves of one
  card agree — SKILL.md section 8.2a, again.
* **It was found by reading a candidate report, not by a sweep.** A candidate wrote
  only "Cic code." Adjudicating that three-word ask against the card is what put a
  human eye on the stem. Intake is a content-review surface, not just a coverage
  surface.
* **The rest of the corpus already knew.** Every other candidate-facing MIW page —
  the solved written papers, the oral notes, the past-paper pages — says
  "concentrated". A term that is wrong in exactly one place and right in twenty is
  a defect a corpus-wide vocabulary check finds trivially, and we did not have one.

**And a derived store can stay stale after its correction shipped.** Regenerating
`docs/study/study_mappings.json` for this fix required `--force`, because that
store's incremental cache key is the taxonomy digest and a question-text change
does not move it. The forced re-derive also picked up `QB1_G#q32`, still carrying
the truncated **"( ms notice 1 of 202)"** stem that entry 50 corrected on the card
— the card was fixed, the mapping store was never re-derived, and nothing failed.
**A generator with a cache key narrower than its inputs will silently serve the
old value forever.**

GREP: SKIP. This entry quotes the rejected expansion "Consolidated Inspection
Campaign" and the truncated citation in order to reject them, so a phrase scan
matches the correction itself.

### 66. An absolute consequence is a different claim from a conditional one, and three cards had made the swap

An independent GPT review of the published corpus at `9e26f02` accepted the
substance of three P0 cards and rejected the **strength** of one proposition in
each. None of the three was a wrong fact. All three were a conditional rule
taught as an absolute one, which is the shape that survives every gate this
toolchain has, because a digest pin is equally happy with "may" and with "must".

**`QB5_J#q2` — NOx.** The card said that going outside the components and
settings identified in the NOx Technical File *"invalidates the EIAPP
certificate"*. The held instrument says otherwise, and says it twice. NTC 2008
**2.4.1.2** requires the technical file to identify *"the full range of allowable
adjustments or alternatives for the components of the engine"* — so an adjustment
inside that range is expressly contemplated, and cannot invalidate anything. NTC
2008 **6.2.1.1.2** then makes engines *"that have undergone modifications or
adjustments to the designated engine components and adjustable features since
they were last surveyed"* **eligible for the engine parameter check method**, and
**6.2.1.2** explains why: the limit *"may, however, be contravened by adjustments
or modification to the engine. Therefore, an engine parameter check method shall
be used to verify whether the engine is still within the applicable NOx emission
limit."* The consequence of departure is **verification against the limit at
survey**, not automatic loss of the certificate. Teaching the absolute version
tells a candidate the wrong thing about what a surveyor will actually do.

**`QB5_J#q2` — ISO 19030.** The card called it *"the standard method for
separating hull fouling from engine deterioration"*. It is not a method for
assessing engine condition at all. It measures **changes in hull and propeller
performance**; the separation only exists when that measurement is read against
corrected engine-performance data. Naming one input as the whole method quietly
promotes a standard beyond its own scope.

**`QB1_D#q7` — Bonjean.** The 60-second answer said that the moment the waterline
is not parallel to the baseline, the hydrostatic tables *"stop being valid"*.
Tabulated hydrostatics do not become invalid; they were computed upright and on
even keel and are simply **not sufficient by themselves** for an arbitrary
inclined or trimmed waterline, because every station is then at a different
draught. The distinction matters in the room: an examiner who hears "invalid"
hears a candidate who does not know what the tables are.

**`QB5_I#q8` — the universal list.** Entry 64 corrected this card's claim that
ISM 10.3 *derives* the critical-spares list. What entry 64 did not catch is that
the card then printed a list of critical equipment and critical spares in a way
that read as though the Code prescribes it. The regulatory logic was right and
the presentation smuggled the old error back in one layer down.

Two lessons worth more than the four fixes.

* **Check the modality, not only the fact.** Every one of these cards would pass a
  fact check. "Invalidates" versus "can render non-compliant", "the standard
  method" versus "a framework", "stop being valid" versus "are not sufficient by
  themselves", "critical equipment is X" versus "a company's SMS may designate X"
  — the noun is identical in each pair and the claim is not. A corpus that only
  ever asks *is this true?* cannot see the difference.
* **Correcting the rule does not correct the illustration.** `QB5_I#q8` had
  already been through a full correction that fixed its ISM reasoning. The example
  list underneath survived untouched and carried the same over-claim in concrete
  form. After correcting a proposition, read the examples that follow it — they
  are where the corrected-away version hides.

**A held file is not a legible source.** The NOx Technical Code was recorded as
held, and it is: 535 pages of it. Every page is an image with **no text layer at
all**, so the instrument that decided this entry could not be read by any tool
that had ever "checked" it. It took an OCR pass to get to 2.4.1 and 6.2. This is
the sibling of section 8.2c's rule that an index row is not evidence — a
*filename* is not evidence either, and neither is a `sha256`.

GREP: SKIP. This entry quotes the rejected wordings — "invalidates the EIAPP
certificate", "the standard method for separating hull fouling from engine
deterioration" and "stop being valid" — in order to reject them, so a flat phrase
scan matches the correction itself rather than the defect.

### 67. A repealed statute's vocabulary outlives it, and the caveat that admits this is the one nobody removes

GPT review pass 2B mapped the **Merchant Shipping Act 2025** against the held
Gazette text and found two distinct failures on the same subject, neither of
which any existing gate could see.

**The stale word.** Twelve candidate-facing places taught the Indian casualty
machinery as *report → preliminary inquiry → formal investigation before a court
with assessors*. That is the **1958** structure. The expression "formal
investigation" occurs **zero times** in the 2025 Act. Part XI is two sections —
notice within twenty-four hours (`s.231(2)`), preliminary inquiry
(`s.231(3)-(4)`), **marine safety investigation** (`s.231(5)-(6)`), administrative
action or proceedings (`s.232`) — and the certificate power the old "formal
investigation" carried now sits separately at `s.312`. One page called the change
a *"2025 renumbering"*. It is a **restructure**: a limb was dropped, not
renumbered. Never describe a consolidating statute as a renumbering unless the
limbs actually survive.

**The caveat that became furniture.** Twenty places carried
*"sections pending verification"* or *"cite at Part level"*. Written honestly, it
is the right thing to publish while evidence is missing. But a caveat is a
**debt**, and this one had been silently rolled forward until a cheat sheet was
instructing candidates, as house doctrine, to cite the Act at Part level forever.
An unverified claim that announces itself is safe; an unverified claim that has
been **institutionalised as a style rule** is not. Any placeholder of this shape
needs an owner and a due date, or it becomes the standard.

**Three things the mapping caught that a summary would not have.**

* **`s.324(1)` is narrower than "except Part XIV".** The text is *"except Part XIV
  **but not including section 411A therein**"* — the saving is Part XIV **minus**
  s.411A. Every card stating the saving must carry that limb.
* **The Act names "very serious marine casualty" exactly once, and does not define
  it.** It appears only inside the `s.224(a)` inclusion list for *marine incident*.
  A card saying "the Act defines it" is wrong; a card saying "the term does not
  appear" is also wrong. The true claim is narrower than either, and only reading
  the provision produces it.
* **A wrong locator can carry a right proposition for weeks.** The source registry
  had the shipping-master definition at `s.93(c)`. s.93 has no clause (c) — the
  definition is in the **Explanation to s.91, clause (c)**. Nothing candidate-facing
  was wrong, so nothing candidate-facing could ever have flagged it. Registry
  locators need the same re-read as the claims they carry.

**An extraction hazard that under-reports silently.** The Act's PDF separates a
section number from its text with a `0x03` control byte as well as with a space.
A `^[0-9]+[.]\s` scan therefore misses sections — `s.319` was reported "NOT FOUND"
on the first pass and is present. The `s.281(2)` penalty table also renumbers its
rows `1..N`, so a naive scan resolves "section 15" to a table row about s.139.
**A negative result from a text scan is only evidence once the scan is proved
able to find a positive.** This is the same family as entry 66's image-only scan:
a file you hold is not a file you have read, and a scan that returns nothing may
simply be blind.

GREP: SKIP. This entry quotes the rejected wording — "formal investigation",
"sections pending verification", "2025 renumbering" — in order to reject it, so a
flat phrase scan matches the correction rather than the defect.
### 68. The Code's own term, and the fact that the investigation is not yours

`QB5_C_B#q5` told the candidate that once the ship is secure he *"transitions to
the formal investigation phase under the IMO Casualty Investigation Code"*, under
a heading reading *"Formal Investigation & Evidence Preservation Procedure"*.
Entry 67 removed that expression wherever it was attributed to the **Merchant
Shipping Act 2025**. This is the same word attributed to a different
instrument, and it is wrong there too.

**The term.** MSC.255(84) para **2.11** defines **marine safety investigation**:
*"an investigation or inquiry (however referred to by a State), into a marine
casualty or marine incident, conducted with the objective of preventing marine
casualties and marine incidents in the future"*. The expression "formal
investigation" occurs **zero times** anywhere in the Code, while "marine safety
investigation" is its term throughout. The parenthesis *"however referred to by a
State"* is permission for a **State** to name its own procedure differently. It
is not licence to attribute a different name to the Code.

**The larger half.** Swapping the term alone would have left a worse claim
standing. A Chief Engineer does not conduct a marine safety investigation at
all: para **2.13** gives it to a *"marine safety investigation Authority"* —
*"an Authority in a State"* — and paras 6.1 and 6.2 place the duty on the flag
State. What the CE actually does is **preserve evidence for** that investigation
and run the **company's** investigation under **ISM Code §9**. In the room, a
candidate who says he will "conduct the formal investigation" has claimed a
statutory function that is not his, which is a worse error than the vocabulary.

Past papers, and any table headed as the 1958 structure, keep "formal
investigation" and are correct: those sittings predate the 2025 Act's
commencement, and a present-day term must never be written into a
sitting-anchored answer.

GREP: SKIP. This entry quotes the rejected wording — "formal investigation
phase under the IMO Casualty Investigation Code" — in order to reject it, so a
flat phrase scan matches the correction rather than the defect.

### 69. ISM section 5 belongs to the Master, and a reg-box row is not an analogy

`QB5_B#q1`'s Regulatory References box cited **ISM Code §5 — Master's
Responsibility and Authority** and described it as *"CE assuming CE role must
review and understand the vessel's SMS immediately"*. The cheat sheet's
pre-arrival row carried the same hook.

**What §5 says.** Read from A.741(18) with every held amendment resolution
re-scanned for sections 5 to 7: §5.1 requires the **Company** to define and
document **the master's** responsibility, and §5.1.5 — *"periodically reviewing
the SMS and reporting its deficiencies to the shore based management"*, the word
"periodically" added by MSC.273(85) — is the **Master's** SMS-review limb. The
section does not mention the chief engineer, a handover, or a takeover. The card
had transposed the Master's duty onto the incoming CE.

**Why "it is only an analogy" does not survive contact with the format.** The row
sits inside a box headed *Regulatory References*: the `reg-code` cell names the
clause and the `reg-desc` cell states a CE duty in the imperative. In that
position the pairing asserts §5 as the regulatory **basis** for the duty. A
citation format carries a claim the prose around it does not get to withdraw.

**And do not over-correct.** ISM **§6.3** — familiarisation for *"personnel
transferred to new assignments"*, unamended — and **§7**, replaced by
MSC.273(85) as *"SHIPBOARD OPERATIONS"*, are what actually support a CE takeover,
together with the **Company's own SMS handover procedure**. But **no ISM clause
prescribes a CE takeover certificate**: "handover", "takeover", "taking over" and
"chief engineer" occur zero times in the Code. Replacing a false §5 hook with a
false §6.3 hook is the same error with a better number.

GREP: SKIP. This entry quotes the rejected wording — "ISM Code §5" as a CE
handover basis — in order to reject it, so a flat phrase scan matches the
correction rather than the defect.


### 70. A criterion with three limits is not the same criterion with one

`QB2_A#q11` and `#q33` taught the Grain Code residual-area criterion as, in
substance, **"the area up to 40°"**. Read from the Code as adopted, in the annex
to **MSC.23(59)**, **A 7.1.2** takes that area *"up to the angle of heel of
maximum difference between the ordinates of the two curves, or 40° or the angle
of flooding (θf), **whichever is the least**"*.

**Why dropping two limbs is not a rounding error.** The three limits are joined
by *whichever is the least*, so the required area is the **smallest** of the
three — and on a great many grain loading conditions the governing limit is the
**maximum-difference angle**, which falls well before 40°. A candidate taught the
short form integrates too far and gets a number that passes when the ship does
not. This is entry 66's family — a claim's **shape** carries meaning the numbers
in it do not — but it is a distinct case, because here no word was absolute or
conditional: an enumeration simply lost two of its three members.

**The same card, the same day, in the opposite direction.** `#q11` also described
the shifted grain surface as *"an angle matching the rolling amplitude"*. Part B
never models the roll. It prescribes an **assumed** surface after shifting, and
the value depends on the compartment: **15°** filled and trimmed (B 2.3); **25°**
partly filled and unsecured (B 5.1); **25°, but 15° in sections where the void
area is small enough**, filled and untrimmed under A 10.3.1 (B 3.2.1); and
**15° abreast, 25° in the ends** under A 10.3.2 (B 3.3). Two of those live inside
one compartment. So the failure mode is not just "wrong angle" — it is believing
there is **one** angle to be right about.

**The instrument was on disk the whole time.** `SRC-GRAINCODE-MSC23-59` was
registered on 4 September 2026 by the previous pass, and both defects are visible
on pages 5, 24, 27 and 28 of it. Nothing was inferred, and nothing needed to be:
the correction cost one PDF read. Register a source and then actually open it.

GREP: SKIP. This entry quotes the rejected wording in order to reject it.


### 71. Two mechanisms, one agent, and an unsafe conclusion in between

`QB2_A#q7` told the candidate the answer *"must be: **No, CO₂ will not extinguish
a Li-ion thermal runaway**"*, and that releasing it *"can waste your fixed
extinguishing agent"*.

**Half of that was right, and the half that was right is what made the rest
persuasive.** CO₂ genuinely does not remove heat from the cells, does not stop
the internal electrochemical self-heating, and cannot by itself prevent
propagation or re-ignition. From that true premise the card drew a conclusion
about a **different** mechanism: flaming combustion in an enclosed space is
oxygen-dependent, and suppressing it is exactly what a fixed gaseous installation
in a protected space is for.

**The operational conclusion is the dangerous part, not the chemistry.** A card
that tells a Chief Engineer to hold back an installed fixed system because
lithium is involved is not making an academic error — it is advice he may one day
act on. The release decision belongs to the **Master** under the ship's fire
control plan, and it turns on the location and accessibility of the fire, whether
the space is enclosed and sealable, whether anybody is unaccounted for inside,
and what is actually installed. Not on the cargo's chemistry.

**A universal sequence is its own defect.** The old 60-second answer gave one
fixed action list with no reference to any of those variables. Correcting the CO₂
proposition while leaving that intact would have left the card teaching the same
shape of error.

**And a circular can be cited at the wrong scope while being perfectly real.**
The same reg-box carried **MSC.1/Circ.1615** described as *"Guidelines for
preventing and mitigating lithium battery fires"*. The circular exists, it is
IMO's, and it does carry material on alternatively powered vehicles — but it is
the *Interim guidelines for minimizing the incidence and consequences of fires in
ro-ro spaces and special category spaces of new and existing **ro-ro passenger
ships***. A wrong-scope citation survives every check that asks "does this
instrument exist?" and fails only the one that asks "does it govern *this*?".

GREP: SKIP. This entry quotes the rejected wording in order to reject it.


### 72. Correcting the rule does not correct the illustration — twice, in the same card, one day apart

Entry 66 recorded that `CORR-GPT-PASS1-20260904` corrected three cards which had
stated conditional rules absolutely, and that a scope pass has to reach the
**illustration** as well as the rule. `QB5_J#q2` was one of those cards.

Twenty-four hours later, the next independent review found that its **Deep-Dive
Trap Questions** block still read: *"Q: Can you advance the timing to recover
performance? **A: Only within the NOx Technical File — outside it the EIAPP is
invalidated.**"* The body Trap point and the REG-BOX had both been corrected. The
worked example underneath them had not.

**What makes this worth its own entry rather than a footnote to 66.** Pass 1
*knew* the lesson — it is the entry Pass 1 itself wrote — and the sweep still
missed the site, because the surviving text does not repeat the phrase the sweep
was built around. It is a **question-and-answer pair**, in a collapsed deep-dive,
phrased as dialogue rather than as a rule. A grep shaped like the rule finds the
rule.

**The cheap defence.** After a modality correction, enumerate every block in the
card by name — short answers, body, numbers, reg-box, CE tip, each deep-dive
block — and read the ones a phrase sweep would not match. There are usually eight
or nine, and the whole exercise is minutes.

GREP: SKIP. This entry quotes the rejected wording in order to reject it.


### 73. A defect found in one card is a defect measured in one card

`QB5_C_B#q5`'s 15-second answer was reported empty, and it was. The obvious fix
is a whole-file string replace of the empty block. That replace would have
matched **eight** times: seven other cards in the same file carry the identical
empty block, and none of them was authorised by anything.

**So the edit was card-scoped by balanced-div extraction**, with an assertion that
each replacement matches exactly once *inside the q5 block*. The seven others are
recorded in the manifest's `found_and_not_swept` and reported, not fixed.

**The same shape, in the other direction, in the same card.** The reg-box was
reported malformed — four `reg-desc` cells with no `reg-code`. Repairing it
surfaced a second defect nobody had reported: **STCW Table A-III/2** sitting in a
casualty-investigation reference box, a competence standard supporting no
proposition the card makes. That is the same class as the **SOLAS V/14** hook
deleted from the `QB5_B` cheat-sheet pre-arrival row in the same pass. One was
authorised and one was not, so one was fixed and one was described accurately and
reported. **Finding an eighth defect while fixing seven is not authorisation to
fix the eighth.**

**And an empty block is a scope trap of its own.** A blank answer has no wording
to sweep for, no digest that looks wrong and no proposition to contradict. It is
invisible to every content gate in the toolchain and visible to any candidate who
opens the card.


### 74. A reference box row that has to explain it does not govern the question

`QB5_C_B#q5`'s casualty-investigation reg-box carried **STCW Code, Table A-III/2**
with the description *"the competence behind the technical account the
investigation relies on. It is a competence standard, not an investigation
provision."* Trap 73 records that this eighth defect was found while fixing seven
others and deliberately **reported rather than fixed**, because finding a defect is
not authorisation to correct it. It has now been authorised and closed.

* **The tell is in the row itself.** A-III/2 is the management-level competence
  specification for chief engineer and second engineer officers on ships of
  **3,000 kW propulsion power or more**. It confers no investigatory function on
  anyone and contains no provision on the conduct, reporting or analysis of a
  casualty. **When a reference row's own description has to say what it is not,
  the row is answering a question the card did not ask.** Narrowing the wording,
  as the previous pass did, made the defect legible; it did not fix it.
* **What was missing was already load-bearing.** **ISM Code §9** — reports and
  analysis of non-conformities, accidents and hazardous occurrences, with
  corrective action under **§9.2** — appears in that card's 15-second answer, its
  60-second answer, its Numbers/Regs block and its CE Oral Tip, and was **absent
  from the reg-box entirely**. A replacement is only safe when the incoming
  instrument is a proposition the answer already rests on. Never add a regulation
  to keep a box at four rows.
* **TWO INVESTIGATIONS, AND THEY MUST NOT MERGE.** The **marine safety
  investigation** is conducted by the **flag State's** marine safety investigation
  Authority under the **Casualty Investigation Code, MSC.255(84)**. The **company**
  investigation and learning runs under **ISM §9**, through the Master and the
  **DPA**. A candidate who answers as though ISM §9 were the statutory regime has
  merged them, and so has any reference box that lists §9 without saying which one
  it is.

GREP: SKIP — the corrected row names MSC.255(84) while denying that §9 is the
statutory regime, so a phrase scan for the resolution number fires on the fix.
Verify by reading the row that carries the resolution in its **reg-code**, not by
counting mentions in the box.

### 75. The IMSBC Code excludes a container by DEFINITION, not by a prohibition

`QB2_B#q15` drew the IMSBC / IMDG line correctly in its own trap question and then
contradicted itself in *On My Vessel*, which put **containerised bulk shipments**
and **flexitanks** inside IMSBC scope. Nothing prohibits it in the Code, because
nothing needs to: the definition never reaches them.

* **SOLAS VI/1-1.2**: a **solid bulk cargo** is any cargo, *other than liquid or
  gas*, consisting of a combination of particles, granules or larger pieces
  generally uniform in composition, *"which is loaded **directly into the cargo
  spaces** of a ship **without any intermediate form of containment**"*. **IMSBC
  1.4.1** anchors the Code's own application to that regulation.
* **TWO INDEPENDENT LIMBS, EITHER ONE SUFFICIENT.** A **freight container is an
  intermediate form of containment**, so containerised cargo is outside the Code
  however bulk-like the commodity looks. A **flexitank is liquid**, so it also
  fails *other than liquid or gas* — it is excluded **twice over**. This is why
  the point is a fact and not a judgement call: it is settled by reading a
  definition, not by weighing a practice.
* **The regimes that do apply**: **IMDG** for dangerous goods in packaged form,
  containers included; the applicable **container / CTU** framework; and the
  approved **Cargo Securing Manual**.
* **The authoring lesson.** *On My Vessel* blocks are where a container-ship
  writer is most tempted to make a bulk-carrier regime apply to his own ship. The
  honest move is to say the regime does **not** govern the ship and explain why
  from the instrument. **A card that teaches a rule and then breaks it two blocks
  later is worse than one that never taught the rule.**
* **Currency, kept off the card.** IMSBC amendment **08-25 (MSC.575(110))** is
  voluntary from **1 January 2026** and envisaged into force **1 January 2027**.
  The scope definition above is base-Code and amendment-independent, so **do not
  reach for 08-25 to answer a scope question** — see trap 55.

GREP: SKIP — the corrected block names flexitanks and containers repeatedly while
placing them **outside** the Code, so a keyword scan fires on the fix. Verify at
sentence level: every flexitank sentence must carry *not*, *excluded* or
*outside*.


### 76. A capability asserted at fleet scale from a position that cannot know it

Two *On My Vessel* blocks claimed things nothing in the corpus establishes, and
both read as authoritative because they were specific.

* `QB5_C_B#q5` said *"I maintain an automated, remote cloud-sync backup for our
  critical machinery logs via our fleet telemetry"*, and that this preserved
  records **"for international maritime tribunals"**. That is TWO claims: a
  company IT estate, and an evidentiary standing for its output. A Chief
  Engineer is in no position to warrant either.
* `QB2_A#q27` inferred a universal requirement from a corporate profile — *any*
  specialised dry bulk charter *requires* the loading computer to carry approved
  IMSBC and Grain modules. No instrument says so.
* **THE FIX IS NOT A BETTER-SOURCED SYSTEM.** Neither claim was replaced with
  another invented company arrangement. q5 now promises only what is in the
  CE's own hands — preserve the **originals** unaltered, protect them against
  alteration, back-dating or loss, secure them under the **Master's authority**
  and the **SMS procedure** with a documented **chain of custody**, and release
  them through the Master to the flag State, the port State and the **marine
  safety investigation Authority**. Shore replication, where a ship has it, is
  **system-specific** and **never a substitute for the originals**.
* **The authoring lesson.** *On My Vessel* is the block where a writer is most
  tempted to make his employer's scale answer the question. The candidate's
  authority ends at his own ship: say what you do, say what you do not know, and
  let the instrument carry the rest.

GREP: `cloud-sync`, `fleet telemetry`, `maritime tribunal`, `dry bulk charter`,
`loading computer.{0,120}module`. All five must return zero.

### 77. The purge medium is not the cargo, so a cargo-shaped danger list has no slot for it

`QB7_D#q14` taught purge and inert as *procedure*, cryogenic, vapour cloud, RPT
and rollover as *dangers*, and PPE and essential-personnel as *controls* — and
never taught that the purge medium itself kills.

* **THE OMISSION WAS STRUCTURAL, NOT CARELESS.** Every entry on that list was a
  property of the LNG: it goes cryogenic, it expands 600-fold, it flashes on
  water, it stratifies. Nitrogen is not the cargo, so a list organised on that
  principle has nowhere to put it.
* **The physics, stated as physics.** **Nitrogen** used for purging and inerting,
  and **LNG vapour** itself, are **simple asphyxiants**: neither is toxic at the
  concentrations that matter, and both kill by **displacing air**. An
  oxygen-deficient atmosphere gives **no useful warning**. That is what separates
  it from the vapour-cloud entry above it, where the hazard is flammability and
  the control is dispersion.
* **Controls that had lost their hazard.** 18.4.3 gas detection, 18.4.6
  essential personnel in PPE and the upwind rule were all already on the card as
  REQUIREMENTS. Naming the hazard is what turns a list of controls into an
  explanation of them.
* **DO NOT IMPORT ENCLOSED-SPACE ENTRY.** Bunkering is an open-deck operation
  and involves no entry. A permit-to-work, a stand-by man and a rescue team are
  a different regime answering a question nobody asked, and reaching for them is
  the over-correction this trap exists to prevent.

GREP: SKIP a keyword scan for `nitrogen` — the card is full of legitimate
procedural nitrogen. Verify instead that the DANGERS list carries an
asphyxiation entry, and that `enclosed space`, `permit to work`, `confined
space` and `rescue team` all return zero.

### 78. A heading is a claim, and it outlives the sentence beneath it

`QB2_A#q11` had its criterion text corrected to *"the net or residual area
**between** the heeling arm curve and the righting arm curve"* — and kept the
heading **"Net Residual Area on GZ Curve (A 7.1.2)"** above it.

* **The card taught the right proposition under the wrong label.** A heading is
  what a candidate reads for structure and carries away as the name of the
  thing. Correcting the body and leaving the label is a half-correction that
  looks complete in a diff.
* **A 7.1.2 STATES ONLY THE UPPER BOUND.** The lower bound is **figure A7**,
  which shades the *"residual dynamic stability"* area from the **first
  intersection** of the heeling arm line with the righting arm curve. The word
  **"equilibrium" appears NOWHERE in the Code as adopted** — a full-text search
  of all 31 pages of MSC.23(59) returns zero hits.
* **So the card must state the limit of its own evidence.** It teaches the lower
  bound, names figure A7 as where it comes from, and says in terms that *"from
  the angle of equilibrium"* must **not** be offered as clause text. A corpus
  that quietly upgrades a figure to a quotation has acquired a citation the
  instrument does not contain — which is the same class of error as the wording
  it was fixing.
* **q33 is ACCEPTED on this issue and was deliberately NOT equalised.** Symmetry
  is not a reason to open a card an authorisation does not name.

GREP: SKIP `area under the GZ curve` — q11 and q27 both QUOTE it to teach
against it. Test whether it is ASSERTED, by checking containment inside a paired
quote span. See trap 70.

### 79. Chapter VII is a subset, not the basis — and the short layer had the wrong one

`QB2_B#q15` cited **SOLAS chapter VII** for the IMSBC Code generally, in BOTH
the 15-second and the 60-second layers, while its own deep-dive body cited
**chapter VI part B** correctly.

* **SOLAS chapter VI** — *Carriage of cargoes and oil fuels* — is the general
  mandatory basis for solid bulk cargoes.
* **SOLAS chapter VII part A-1** — *Carriage of dangerous goods in solid form in
  bulk* — is the SUBSET regime. Real, and named, but it does not carry the whole
  Code.
* **THE CARD CONTRADICTED ITSELF, AND THE MEMORISED LAYER WAS THE WRONG ONE.**
  That is the worst possible distribution of an attribution error: a candidate
  studies the deep dive once and recites the 15-second layer in the room.
* **The authoring lesson.** When a Code sits under two chapters, the short layer
  must anchor to the one that makes it mandatory *generally*, and name the other
  as what it actually governs. Deleting chapter VII would have been the opposite
  error.

GREP: `mandatory framework under SOLAS Chapter VII` must return zero. Both short
layers must contain `Chapter VI` and `Part A-1`.

### 80. A currency claim that carries no date cannot be seen to have aged

Four cards carried claims about what is CURRENT. Three were TRUE WHEN WRITTEN,
which is exactly why nothing in the corpus would ever have flagged them.

* **`QB5_E#q4`** called Maersk **"a founding MACN member"**. Maersk's own
  publication says only that it **helped establish** MACN in 2011 — participation
  in establishment, not a status. **The claim was live in TWO blocks**, On My
  Vessel and the CE Oral Tip, and the first sweep found only one because it read
  a **truncated listing** of the card's hits. *A sweep you have not seen the end
  of is not a sweep.*
* **`QB4_H#q13`** called BMP Maritime Security **"the 2026 edition"** at nine
  sites. OCIMF labels it **1st Edition, 2025**, updated during 2026. **There is
  no second edition.** One *Common CE Failures* entry — "Teaching BMP5, **or the
  2025 first edition**, as current" — was FALSIFIED BY THE CORRECTION ITSELF and
  had to be rewritten in the same act. The label was **also wrong at nine sites across the
  five cards outside q13** (`QB4_H#q2`, `QB4_H#q11`, `QB4_B#q16`,
  `QB9_A#q9`, `QB9_B#q5`); that was REPORTED, not swept, and the sweep was
  carried out on **5 September 2026** under `CORR-BMP-EDITION-PROP-20260905`.
  *A report of a defect is not a repair of it, and the gap between the two is
  where a corpus contradicts itself.* See trap 54.
* **`QB7_D#q15`** cited **ISO 23306:2020** with no currency statement at all —
  not a false claim, a claim with no date-of-check. It is still the **CURRENT
  PUBLISHED** standard as at September 2026, but ISO has flagged it *"to be
  revised"* and **ISO/AWI 23306** edition 2 is **UNDER DEVELOPMENT**, registered
  3 August 2026. **An AWI is a work item, not a published standard.**
* **`QB3_C#q7`** said regulation 16 is *"unamended ... in the held in-force
  chain"* — properly scoped to its evidence, and **undated**. It now says *as at
  September 2026*, and names what the recent amendments DO concern.
* **The authoring lesson.** Prefer the publisher's own label over a year you
  inferred; distinguish **CURRENT PUBLISHED** from **UNDER DEVELOPMENT**; and
  give every negative a **date and a scope**, because an exhaustive negative you
  cannot re-run is a claim you cannot maintain. See traps 50, 52 and 61.

GREP: SKIP `the 2026 edition` — q13 QUOTES it to teach against it. Test for
assertion outside a quote span.

### 81. A closure claim is only as good as the corpus behind it — and the count is the part that rots first

`QB7_D#q15` told the candidate that **"the five IGF amendments in force or
adopted were each opened and read"** and then listed five. **The chain has six.**
The missing one was **`MSC.458(101)`** — in force since 1 January 2024, and sitting
in the shared true-source corpus since 3 August 2026. *The omission was in the
reading, not in the holding.*

* **The count was wrong first and the list was edited to agree with it.** The
  sibling card `QB7_D#q14` says "All five IGF amendments" and then lists **six**,
  because its five counts the five then **IN FORCE** and adds `MSC.567(109)` with
  "plus" — defensible in isolation. q15 inherited that **count word** into a
  sentence scoped "in force **or adopted**", where six is the only right answer,
  and dropped a resolution to make the list match the number. **When a number and
  a list disagree, find out which one was written first.**
* **This footer had already been corrected once, and was still wrong.** An earlier
  version claimed closure over **four**; independent review found that
  `MSC.475(102)` and `MSC.524(106)` had never been looked for, and the count went
  to five. It should have gone to six. *A correction that moves a number without
  re-deriving the set has not checked the set.*
* **Name the base separately.** `MSC.391(95)` **adopts** the IGF Code and is not
  one of the six amendments. Counting it gives seven, and that is the error a
  reader correcting "five" in a hurry will make next. Both footers now say so.
* **Hold what you cite.** A footer naming six resolutions the corpus does not hold
  is no more reproducible than one naming five — which is exactly how the
  four-to-five correction passed, with two of the five named but unheld. All six
  are now held with recorded SHA-256 digests and registered in
  `docs/sources/MIW_SOURCE_REGISTRY.json`.
* **The substantive conclusion survived.** No IGF amendment amends the annex to
  part C-1, the LNG Bunker Delivery Note — re-established by reading all six end
  to end, including the omitted one. *An enumeration can be wrong while the
  proposition it supports is right; that is why the enumeration needs its own
  check.* See traps 54 and 80.

GREP: SKIP `five IGF amendments` — the version stamps and this entry QUOTE the
wrong claim in order to record it. Test the ENUMERATION, not the whole footer:
q15 legitimately names `MSC.458(101)` three times outside the list.

### 82. CII is per CAPACITY-nautical-mile, and the capacity measure is ship-type specific

Nine layers of `QB6#q1` taught **`gCO₂/DWT·nm`** as the CII unit, and one layer of
`QB7_I#q10` said **"per DWT-mile"** while its own body said "capacity times distance".
Both are wrong for a whole class of ships, not merely imprecise.

**The rule.** MARPOL Annex VI reg. 28.1 requires the attained annual operational CII to be
calculated taking the **G1 Guidelines** into account. G1 section 4.2 — replaced by
**MEPC.412(84)**, adopted **1 May 2026** — defines supply-based transport work as
`Ws = C × Dt`, where **C is the ship's capacity** and:

* **DWT** — bulk carriers, tankers, container ships, gas carriers, LNG carriers, general
  cargo ships, refrigerated cargo carrier, combination carriers;
* **GT** — cruise passenger ships, ro-ro cargo ships (vehicle carriers), ro-ro cargo ships,
  ro-ro passenger ships.

`Dt` is the total distance travelled in the calendar year, **under way and not under way**,
as reported under the IMO DCS.

**Why this is not pedantry.** A ro-ro passenger ship's attained CII is not a DWT figure at
all. A candidate taught the universal form answers confidently and wrongly the moment the
panel changes the ship type — which is what a panel does. Say **capacity** first, then name
yours.

**AUTHORING RULE.** Never write `gCO₂/DWT·nm` as *the* CII unit. Write
`gCO₂ per capacity·nm` and state the ship-type split.

**Propagation CLOSED 5 September 2026.** `QB6#q1` and `QB7_I#q10` were corrected first;
`QB6#q2` (five sites) and `QB6_cheatsheet.html` (five sites) followed. For the four hours
between them **`QB6.html` taught two versions of one unit**, which is the real cost of a
card-scoped authorisation and the reason a revision layer must be corrected in the same
breath as its cards — a candidate revising from the cheat sheet gets the uncorrected form.

**Not every DWT occurrence is this defect — read the scope before you edit.** The
following are **CORRECT and must be kept**:

* `QB3_J` — "attained CII = CO₂ emitted ÷ (capacity × distance sailed), in
  `gCO₂/DWT·nm` **for my ship type**" and "CII units **for container ships**". The scope
  clause is what makes it right; a pattern-only sweep would eat the clause and keep the unit.
* `QB1_K` — "the capacity term **C** in the **container-ship** CII". The unit is being used
  as *evidence* in a tonnage-definitions card about what DWT is.
* `QB6#q13` — a worked example opening "**A container vessel** with 12% propeller slip".
  Scoped by the sentence *before* the unit, so it cannot be adjudicated from a grep line.
* `QB7_A` — "gCO₂/DWT·nm **or** gCO₂/GT·nm". Names both measures; the model form.

The EEDI/EEXI reference line `a × DWT^−c` is a **different proposition** and is genuinely
DWT-based. Do not sweep it.

GREP: SKIP `gCO₂/DWT·nm` — this entry and the corrected cards' trap blocks QUOTE the
rejected form in order to reject it. Test that each occurrence is **negated or quoted**,
never that it is absent.


### 83. MARPOL Annex I reg. 34.1.5 has TWO limbs, split on 31 December 1979

Seven candidate-facing sites in `QB3_F` taught the total-quantity limit as a single
universal **1/30,000**, and **`1/15,000` appeared nowhere in the 86-file bank** — so a
candidate revising the whole corpus could never have met the other limb.

**The rule, from MEPC.117(52) reg. 34.1.5.** The total quantity of oil discharged into the
sea shall not exceed, of the total quantity of the particular cargo of which the residue
formed a part:

* tanker **delivered on or before 31 December 1979** (reg. 1.28.1) — **1/15,000**;
* tanker **delivered after 31 December 1979** (reg. 1.28.2) — **1/30,000**.

**AUTHORING RULE.** Never write one number. Where a short or memorisation layer cannot
carry the sentence, use the compact split — `1/15,000 (delivered on or before 31 Dec 1979)
or 1/30,000 (delivered after 31 Dec 1979)` — and keep the boundary **exact**. "Before
1980" is NOT the same rule: it moves every tanker delivered *on* 31 December 1979 into the
wrong limb. The other reg. 34.1 criteria — outside a special area, en route, >50 NM,
≤30 L/NM, ODMCS and slop tank in operation — are correct and must not be altered.

**And count the sites by DOCUMENT POSITION, not by report.** The finding was reported as
"q3 ×5, q11 ×2". q11 owns **one**; the seventh lives in the page's *Rapid Recall*
cheat-grid, **outside every q-card**, where no card digest can reach it.

GREP: SKIP `1/30,000 alone is wrong` — the corrected body bullet quotes the rejected form.


### 84. A vessel specification can be TRUE and still be a provenance failure

`QB6#q1` told candidates its ship had a *MAN B&W 11G90ME-C main engine at ~35,000 kW MCR*;
`QB2_A#q31` described a personal **fine-ore pre-loading routine** on a candidate whose
service is container vessels. Neither was corrected because it was inaccurate.

**The rule.** *"On My Vessel"* asserts the candidate's **own experience**. A ship
specification or fleet fact may be factually true and still be inappropriate there if it is
presented as the candidate's own without grounding. **Source proof does not rescue a
provenance failure**, so the cure is to **delete or genericise** — never to substitute a
sourced replacement, which is the same failure with better footnotes.

The pattern that scores: *"This is not a cargo operation from my container-vessel
experience. In an oral I would say so directly, then answer from the applicable
requirements rather than invent a bulk-carrier routine."* Answering the half you own and
naming the half you do not beats claiming both.

**Corollary — a hedge must span the real disagreement.** The same card hedged the casualty
position as *"230 to 240 nautical miles"* and told the candidate they *"cannot be caught
out"*. **No source supported 240**; the reported spread was 230 to 290. A hedge on the
wrong side of a disagreement is worse than no hedge, because it advertises a safety it does
not have. Same defect class as the National Shipping Board date. See trap 83 for the
document-position rule and `docs/sources/MIW_SOURCE_REGISTRY.json` for the evidence set.

**Corollary — a recent named casualty needs a registered source before release.** Verify
every published fact **individually**. `QB2_A#q31` carried three wrong facts (cargo tonnage,
distance, rescuing vessel) and two unverifiable ones (beam, and an implied destination) in a
card that read as careful. Where no flag-State or coastal-State report exists, say so to the
candidate and name what is therefore **not claimed**.

GREP: SKIP `230 to 240` and `72,100` — this entry quotes the withdrawn figures.


### 85. IACS UR Z7 is Hull Classification Surveys — it is NOT the Enhanced Survey Programme

`QB4_E` taught **"IACS UR Z7: ESP for Bulk Carriers and Tankers"** in seven places across
two cards, and `oralnotes/simon-notes-p3.html` taught the same thing under a *different*
number — **"mandatory under IACS UR Z7.1"**. Both are false.

**The rule, from the instrument itself** (UR Z7 Rev.29 Corr.1, held and hash-pinned at
`docs/sources/IACS-UR-Z7-Rev29-Corr1.pdf`):

* its title is **Hull Classification Surveys**;
* **§1.1.1** — "These requirements apply to **all self-propelled vessels**." It is the
  baseline hull survey requirement for every ship, not a two-ship-type regime;
* **§1.1.3** — the *additional* hull, piping and ballast-tank requirements for tankers,
  bulk carriers, chemical tankers, double-hull tankers and double-side-skin bulk carriers
  are in the **Z10 series**. Z7 itself routes ESP-type work out of Z7;
* **§1.1.5** — **UR Z7.1** is the **water level detector** requirement for single-hold
  cargo ships. Not ESP either.

**ESP's authority is STATUTORY, not class.** The International Code on the Enhanced
Programme of Inspections during Surveys of Bulk Carriers and Oil Tankers, 2011 (**ESP
Code**), **IMO res. A.1049(27)**, made mandatory by **SOLAS Chapter XI-1, Regulation 2**
(MSC.325(90), in force 1 January 2014). A Unified Requirement binds IACS member societies'
own rules; it does not bind a flag State. Citing a UR for why ESP is *mandatory* is a
category error, not a citation slip. `QB1_I#q1` is the model card.

**AUTHORING RULE — do NOT substitute a guessed Z10 sub-number.** Read strictly, Z7 §1.1.3's
"respectively" maps **tankers → Z10.1** and **bulk carriers → Z10.2**, which is the
*opposite* of the widely repeated assumption. Nothing held resolves it and neither
sub-document is in the repository. Write **"the UR Z10 series"** unless an exact sub-number
has been verified at the instrument. Replacing one false citation with a plausible second
one is the same defect with better footnotes.

**A hedge is not a fix.** The `simon-notes-p3` reg box printed the wrong code and appended
*"verify exact UR number before quoting"*. The wrong number was still in the code column
and the verification was handed to the candidate. Verify it, or remove it.

GREP: SKIP `UR Z7` — UR Z7 is a real and correctly cited requirement in its own right, and
this entry plus the corrected cards QUOTE the rejected attribution in order to reject it.
Test that `Z7` is not bound to `ESP` / `Enhanced Survey Programme`, never that `Z7` is absent.

### 86. The Grain Code's Document of Authorisation is **A 3**, not A 7

**A 3** is DOCUMENT OF AUTHORIZATION. **A 6** is INFORMATION REGARDING SHIP'S STABILITY AND
GRAIN LOADING — the printed booklet. **A 7** is STABILITY REQUIREMENTS: the 12° heel, the
0.075 m·rad residual area and the 0.30 m corrected GM. All three read verbatim from
**MSC.23(59)**, the Grain Code as adopted, held locally.

`QB2_A#q33` cited "International Grain Code, A 7" in its reg box for the Document of
Authorisation while, two paragraphs above, correctly citing **A 7.1.2** for the residual-area
criterion. The card contradicted itself on one screen. A prior correction (T1-GRAIN) had
touched the same card and left this untouched — **CORRECTED ≠ REVIEWED**.

**Also in A 7.1.1:** the deck-edge alternative to the 12° limit applies only "in the case of
ships constructed on or after 1 January 1994". Teaching "12°, or deck-edge immersion if less"
without that limb drops an applicability condition.

GREP: test that `A 7` is not bound to `Document of Authorisation`, never that `A 7` is absent
— A 7 is the correct and necessary citation for the stability criteria.

### 87. The current CII G2/G4 pair is **MEPC.353(78) / MEPC.354(78)**, not the 2021 pair

Both 2022 resolutions were retrieved from IMO's own resolutions CDN and their **operative
clause 5** read directly: MEPC.353(78) **REVOKES** the 2021 reference-lines Guidelines
(MEPC.337(76)); MEPC.354(78) **REVOKES** the 2021 rating Guidelines "adopted by resolution
**MEPC.339(76)**". Reduction factors (G3) remain **MEPC.338(76)** — there is no 2022 G3.

The corpus contradicted itself: `QB7_I#q10`, `QB6#q1` and `QB6_cheatsheet.html` taught the
revoked 2021 pair as current while `QB6_E` and `QB7_E` cited MEPC.354(78) for the same thing.

**C_F attribution is a two-step chain, and the one-step version is not simply wrong.**
**MEPC.352(78)** (G1) §4.1 does not tabulate C_F: it defines it "in line with those specified
in the 2018 Guidelines on the method of calculation of the attained EEDI for new ships
(resolution MEPC.308(73)), as may be further amended". So the numbers really are read from the
EEDI guidelines — currently **MEPC.364(79)** — but the **CII authority is G1**. Cite the chain.
Naming the EEDI resolution alone on a card whose own trap section punishes EEDI/CII confusion
is the specific slip to avoid.

GREP: test that `MEPC.337(76)` and `MEPC.339(76)` are not bound to a *current* G2/G4 claim,
never that they are absent — the corrected cards name them in order to reject them.

### 88. BMP: the current publication, and what it actually says about muster, citadels and speed

**BMP Maritime Security, 1st Edition 2025, updated June 2026** — held from OCIMF's own
publication endpoint. Its **version-control table gives the Edition column as "First" for BOTH
the March 2025 and June 2026 rows**, which is primary proof from the document itself that there
is **no second edition**. "The 2026 edition" and "Version 2 (2026)" are both wrong. The June
2026 change is one thing: activist-boarding content in Section 6.

**Two endpoints do not serve the same bytes.** maritimeglobalsecurity.org's
`/media/t4jccjou/bmp-ms_lo-res_s.pdf` serves the **pre-update** March 2025 file with no activist
content. Check the version-control table on any re-acquisition.

**Muster location is chosen BY THREAT** — verbatim: locations "will vary depending on the
threat, i.e. threat from piracy (citadel), threat from WBIED/UAV (above waterline)". A
**security muster point**'s "location should be above the waterline if there's a risk of hull
breach". A **citadel** is where the crew retreat "if intruders board", and "should accommodate
the entire crew and any extra staff for **3-5 days**". A steering-gear-room citadel is a sound
answer for a *boarding*; it is the wrong answer for a missile or WBIED, and the error is
failing to distinguish the threat rather than the space itself.

**Numbers BMP MS does NOT support.** There is **no 72-hour** citadel provisioning standard —
it is 3-5 days, and it is guidance. There is **no 18-knot threshold**: the string "18 knots"
appears nowhere in either held file. BMP MS gives an action — "increase to maximum to open the
distance" and "steer straight" — not a speed threshold.

**BMP is not an IMO instrument.** Six industry publishers: BIMCO, ICS, IMCA, INTERCARGO,
INTERTANKO, OCIMF. Listing **IMO** as a publisher misstates the document's authority. BMP
mandates nothing; it binds through the **Ship Security Plan**.

**Adjacent authority slips found in the same family.** **SOLAS XI-2/8** is the *Master's*
discretion against constraint by the Company or charterer — it is not a Chief Engineer's
authority to bypass a protective trip. Machinery-space escape is **SOLAS II-2/13.4.2.1** ("a
steel door capable of being operated from each side"), **not** the LSA Code. Fire-main minima
are **SOLAS II-2/10.2.1.6** at hydrants — cargo ships 0.27 / 0.25 N/mm² — and there is no
6-bar figure and none expressed for deck monitors. The **ISM** master's review is
*periodically* (5.1.5, as amended by MSC.273(85)) with **no** Code interval; internal audits
are 12.1's "intervals not exceeding twelve months", exceedable "by not more than three months".

**The scoping lesson.** The 31 Aug 2026 correction added a supersession banner to four cards
and, by its own declared scope, left "every BMP5 technique block deliberately untouched".
Three of the four then went on teaching BMP5 as the current active edition in the layer
candidates memorise, two screens below a banner saying the opposite. **A banner is not a
migration.**

GREP: test that `BMP5` is not bound to a *current-publication* claim, never that `BMP5` is
absent — the stems, the banners and the replacement history all name it legitimately.

### 89. Authoring artefacts served to candidates, and the guard that flagged its own audit trail

Two classes of machine residue were live in the published corpus: **101 occurrences of exactly
`[cite: 1]`** across four files, and **21 plain-text scaffold blocks** — a `<pre>` "REGULATORY
REFERENCE BOX", a duplicate CE ORAL TIP and a `CORRECTION FOOTER:` stamp — each duplicating
its card's rendered reg box and CE tip. Twelve of those stamps carried a **wrong card's
identity** (every one in `QB9_B.html` said `QB8 · Q…`) and nine carried a stale version.

**Count occurrences, not lines.** The census was quoted per file as 2/15/30/15 from `grep -c`,
which counts *matching lines*; the occurrence counts are 6/24/47/24. Same total, different
denominator.

**Verify duplication before excising.** Each block was checked to duplicate its card's rendered
reg box and CE tip *before* removal, so no unique candidate content was lost; balance and
per-card reg-box/CE-tip counts were re-proved after.

**AUTHORING RULE — a content guard must not read the provenance it creates.** A correction
stamp necessarily quotes the defect it removed ("no longer claims XI-2/8…", "the invented 72
hours…"). Three Tranche 4A gates went red on their own `q-version` audit trail until `flat()`
stripped it. The same lesson as the PIL sweep: **provenance fields sit outside the sweep.**

**AUTHORING RULE — scope a check to its element, not to a character window.** Guards written as
"needle within N chars of keyword" passed mutations because an adjacent bullet supplied the
keyword. Element scoping (the enclosing `<li>`, reg row or paragraph) is what makes them bind;
a wrong **reg-code** likewise hid behind a right **reg-desc** until the code slot was checked
on its own.

GREP: `[cite:` and `REGULATORY REFERENCE BOX` must both be absent from `meoclass1/*.html`.

### 90. The deep-dive suffix cascade — one conversion bug, 146 blocks, 82,736 duplicated bytes

A markdown-to-HTML conversion split each deep-dive blob into typed `dd-block` divs by taking the
tail from every `* <strong>Label:</strong>` marker **onward** instead of the segment **between**
markers. `dd-trap` therefore rendered its own content plus four following sections as raw
markdown, `dd-fail` three, and so on down the card. 146 blocks on 38 cards across `QB1_F` and
`QB1_G`.

**A suffix cascade is repairable mechanically; an arbitrary duplication is not.** Because the
conversion took suffixes, every stray section is byte-identical to the **own body of the later
typed block carrying the same label on the same card**. That was proved for all 146 before a
byte was written, and the applier refuses any block the proof does not cover. Truncation then
deletes only duplication — no content is invented and none is lost.

**Match by LABEL, never by position.** The blocks are not emitted in the markdown's order:
`dd-chain` sits between `dd-casualty` and `dd-vessel`. A positional comparison reported a false
mismatch on every card and made the repair look unprovable.

**A normaliser is part of the key.** The proof recorded labels through `html.unescape`; the
applier first re-derived them without it, and every block labelled `Numbers &amp; Regulations`
silently failed to match and was skipped — 109 of 146 repaired, no error raised. Import the
normaliser; never re-implement it beside its own proof.

### 91. An idempotency check written for replacements is blind to deletions

The reach applier tested "already applied" by looking for its replacement text. One of its eight
edits is a **deletion** — the two proposition-less `MSC.1/Circ.1606` pills — and a deletion has
no replacement text to find, so a perfectly clean re-run reported it as a refusal. The rule for a
deletion is that its anchor is simply gone. Same family as the guard that expires in both
directions: a check has to change **subject** with the edit it guards, not just keep running.

### 92. A generator must not read its own output

`build_t5_correction_records.py` resolves each card's prior authorised pin by walking the
manifest surface — and once its own records were on disk, `build_chain` saw them as states in the
chain and reported `PREDECESSOR_PIN_ALTERED` against the very pins the run was recomputing. The
second run of a generator is not a re-run if the first run changed its input. Exclude the
record's own filename explicitly; do not rely on running it only once.

### 93. Hydrant minimum pressure is **0.27 / 0.25 N/mm²** by SOLAS II-2/10.2.1.6, scoped at 6,000 GT

Three sites taught a bar figure under mandatory wording for a quantity SOLAS fixes: `QB2_A#q8`
gave "4 to 6 Bar" as the "minimum … required at the furthest hydrant", `QB2_H#q2` gave a "4.0 bar
minimum required at the highest hydrant", and `QB2_B#q18` gave the correct 0.27 N/mm² with **no
threshold**, so it read as governing every cargo ship.

For **cargo ships**, with the two required pumps delivering simultaneously: **0.27 N/mm² at 6,000
GT and upwards, 0.25 N/mm² below**. A higher figure quoted for deck-monitor throw is a design or
operational target, not a SOLAS minimum. The passenger-ship limbs are deliberately not imported
into container cards.

**Internal contradiction is a stronger signal than a suspicious number.** The 4.0 bar site was
promoted out of a 1,034-hit numeric census because it contradicted `QB9_B#q5`, corrected to the
governing figures five days earlier. "This number looks invented" cannot be mechanised; "this
number contradicts held source **and** a corrected sibling card" can.

**A single-limb version of a two-limb rule is not a blurred rule.** It is simply wrong for every
ship on the other side of the threshold — the same shape as the MSC.535(107) lifeboat-ventilation
defect, where keeping only the newbuilding limb inverted the rule for the in-service fleet.

### 94. A sweep whose site list comes from a finding's card list will always leave siblings behind

Three BMP corrections ran between 31 August and 6 September, and a corpus-wide census on
6 September still found **three untouched card-layer sites** — including `QB4_H#q6`, in the *same
file* as a card two of those sweeps had corrected — plus a `source-confidence` footer on `QB4_H#q2`
still offering "BMP5 Section 5" as the authority the card had been verified against, five days
after the card's own body removed that citation as unverifiable.

**Derive the site list from the corpus, then classify; never from the finding.** Of 102 corpus
occurrences, **94 are KEEP**: a `q-text`, a `cs-qtitle`, a TOC entry, a `sub-desc` or a generated
index row echoing one is the **examiner's own wording**; `QB4_H#q11` is retained on purpose as the
predecessor record because examiners still ask for BMP5 by name; and a currentness note that
quotes BMP5 in order to deny it is the fix, not the defect. A flat "remove every occurrence" sweep
would have destroyed all of it.

**Emit the SURFACE with every hit.** The same string is a defect in an answer body and correct in
a `q-text`. A census that reports only file and line cannot be adjudicated without reopening every
site by hand.

### 95. A cheat sheet takes no digest pin, so only a content gate can guard it

Revision surfaces (`*_CheatSheet.html`, `*_cheatsheet.html`) carry no `q-card`, so they are
recorded in a correction manifest's `artefacts` **without** a digest — a pin on an unguarded file
would expire on the next unrelated edit to it. That means the manifest cannot prove what they say,
and their propositions have to be asserted by the correction's own content gate instead. Three of
this pass's eight reach sites live only there; without content gates they would have been
completely unguarded while looking recorded.

### 96. A forbidden-proposition check must be case-insensitive, and adding the second spelling is not the fix

`CORR-T5-HYDRANT-20260906` corrected `QB2_H#q2`'s extra-block to the SOLAS
II-2/10.2.1.6 limbs, wrote a version stamp saying the old figure "is not a SOLAS figure", and
left the card's **Key Numbers / Regs** list — four lines above that stamp — still reading
`4.0 Bar: Minimum operational pressure required at the furthest deck hydrant`. The gate reported
PASS. Its negative check was `removed not in flat(teaching)` with `removed = "4.0 bar"`, and the
residue reads `4.0 Bar`.

**Capitalisation is not part of a proposition, so it must not be part of the matcher.** Lower-case
both sides and normalise whitespace. Enumerating `"4.0 bar"` and `"4.0 Bar"` is not a fix — it
moves the same hole to `4.0 BAR`, and the next residue will differ by a non-breaking space or a
line wrap instead.

**A mutation can pass its own suite while the escape stays live.** The suite's mutation B
reinserted the figure using the *lower-case* spelling the check was written against, so the guard
looked proved. A mutation that reproduces the defect **in the exact bytes the corpus actually
carries** is the only one that tests anything; write the mutation from the live residue, not from
the correction's own vocabulary.

### 97. A scope defect is invisible from inside its own scope

Every Pass-1 census and gate enumerated `meoclass1/*.html`. That is **128 files**. The corpus is
**224**: `oralnotes` 44, `pastpapers` 51, `rulesapp` 1. Ninety-six files were outside every claim
of "corpus-wide", and the whole oralnotes study series sat in that gap teaching **BMP5 as current**
with a timeline row dating it to **2024**.

Nothing went red. Every count was internally consistent, every gate was green, and three reports
described a sweep of 57% of the corpus as complete — including the report that added trap entry 94,
*"derive the site list from the corpus, then classify; never from the finding"*.

> **Rule.** "Corpus-wide" resolves through **one** enumeration function, recursive, imported by
> every consumer. A local re-glob is how two definitions drift apart, and the drift is what hides.

**A scope control cannot share the enumeration it tests.** `test_corpus_scope.py` re-walks the tree
with `os.walk` as a second implementation, and **plants a file in a nested directory** and requires
the enumeration to see it. Assert the contract as a live comparison — "the recursive set is strictly
larger than the top-level set, and these N files are what a top-level glob would miss" — so
reverting the glob goes red instead of passing vacuously.

**Recursive scope is not a licence to sweep.** A surface is a POLICY, not a directory.
`pastpapers` is sitting-anchored: modernising an examiner's historical wording is its own defect.
`oralnotes` is current study material by its own titles, so currentness rules apply there exactly
as on a card. Classification must be **total** — a file with no family is a file with no policy.

**And a wider net catches content.** The recursive orphan-bullet scan immediately flagged a lone
`* Day-counts are ...` line in `miw-notes-mgmt-p6` — the **footnote** paired with the `3 days*` /
`7 days*` markers above it. A bullet run is two or more consecutive lines; a single starred line is
a footnote. Widening scope without sharpening the discriminator would have deleted the note saying
those day-counts are not MLC statutory text.

### 98. What a self-written gate cannot tell you, and the four ways these ones lied

The three Pass-1 gates were written by the session that made the edits, and an independent reviewer
found four checks that passed while asserting nothing:

* **A body that is never read.** `every_typed_block_survived_the_repair` compared `(class, label)`
  pairs — `DD_BLOCK` group 3 is the body, and the check never touched it. A repair that replaced
  all 146 bodies with one character would have passed, and so would a block migrating between cards
  in the same file, because the comparison was file-wide rather than per card.
* **A number computed and discarded.** `derived_bytes` was accumulated in the loop and never used;
  the 82,736-byte claim was guarded by `manifest_number > 50000` — the record marking its own
  homework.
* **A check satisfied by the audit trail it was written to exclude.** `N1_footer_agrees_with_its_own_card_body`
  read the whole card, and the word it looked for exists **only in the version stamp**.
* **A check that was the literal `True`.** Honest in its message, still counted in the total.

> **Rule.** Every check must be able to FAIL on some reachable state, and the mutation that reaches
> it must be named. A green gate written beside the edit it guards is evidence of nothing until an
> independent reader has tried to break it.

### 99. Three escapes, one defect: a guard that knows a spelling, a shape or a position

Three independent reviews in a row found the same underlying failure, each time wearing different
clothes:

| escape | the guard recognised | what defeated it |
|---|---|---|
| Pass 1 | the string `"4.0 bar"` | **case** — the corpus carried `4.0 Bar` |
| Pass-1 repair | the string `"0.27 N/mm"`, in `<li>`/`<p>` | **unit and element** — `QB2_F` writes `0.27 MPa` in a `<div>` |
| Pass-1 repair | `<span class="reg-code">` | **HTML class** — the `<td>` cell and CE-tip prose it had just corrected |

Every one of those guards was written correctly against the instance in front of it, and every one
was blind to the next spelling of the same claim.

> **Rule.** Detect the **proposition**, not its rendering. Normalise the units, take the smallest
> enclosing element of **any** candidate-facing tag, and ask whether the sentence asserts the
> forbidden thing. `tools/oral/oral_currentness.py` is the single implementation; a gate that
> re-implements it will drift back into shape-dependence.

**Normalise numerals as well as units.** `0.27 MPa` = `0.27 N/mm²` = `2.7 bar` = `270 kPa`, and
`two pumps` = `2 pumps`. The cheat-card writes the numeral and the card writes the word; the
proposition is identical. The first version of the completeness check missed a site it had *just
corrected* because the card said "2 pumps".

**Unit normalisation is a DETECTOR rule, never an editorial one.** A card may print MPa or N/mm²
as it likes. The guard changed; the card did not.

**The innermost element is usually too small.** In
`<li>Minimum fire-main pressure: <strong>0.27 MPa</strong> at monitors</li>` the innermost element
around the figure is the `<strong>`, whose visible text is `0.27 MPa` — no subject, no modal, and a
detector reading only that sees nothing. Climb outward and take the **smallest element that carries
a complete claim**. That keeps element scoping (entry 89) without depending on where the author put
the emphasis tags.

**A depth counter is not a stack.** The element scanner tracked depth and recorded a start only at
depth 0, so it yielded the **outermost** element of each tag and never a nested one — a `<div>` inside
a cheat card resolved to the whole cheat sheet, and the completeness test was then satisfied by
unrelated text elsewhere on the page. Every open element containing the position is a rung.

**A claim needs all of its parts, or it is a different claim.** A hit requires the subject
(hydrant / fire-main / monitor), a figure, mandatory framing, **and** incomplete scope. Two of the
four is not the defect: figure + subject alone fires on `fire main water (typically 5–7 bar)`, a
HydroPen operating pressure that is correct; figure + modal alone fires on the weathertightness
hose test, a different quantity with no held source.

### 100. Insert by structural identity, never by the first matching anchor

The BMP currentness banner was inserted at the **first occurrence** of `⚓ Why It Matters (CE
Perspective)` in `miw-notes-mgmt-p10.html`. That head appears in every topic, so the banner landed
in the *Marine Environmental Governance (UNCLOS Pt. XII)* topic — about 375 lines and four topics
away from the BMP material it warns about, in a topic that never mentions BMP5. Topic 46 then said
"see the currentness note above", pointing across four unrelated topics, and carried no banner of
its own.

The damage is worse than a no-op: a currentness note **governs its container**, so a misplaced
banner protects text that needs no protection and leaves the real material unguarded. A gate that
asks only "does the banner exist in this file?" passes happily.

> **Rule.** Locate an insertion by the **structural identity of its container** — `id="topic-46"`,
> a card anchor — and bound the search to that block. Never by first-occurrence, global needle, or
> nearest-heading.

**This is the third wrong-occurrence bug in one session.** A mutation replaced a `dd-block` body by
string and hit an earlier duplicate of the same text outside any block, exercising nothing; a
mutation edited a `q-text` stem and hit the JSON-LD copy instead; and this. A `replace()` on text
that appears more than once is a positional guess wearing the costume of an edit.

**Prove locality in both directions.** The control asserts the banner is in the intended topic
**and** in no other, that the intended topic is the one whose subject matches, and that the note
cross-referencing it lives in the same block. "Exists somewhere in the file" is not a location.

### 101. Five rounds, one defect: enumerating renderings never converges

| round | the guard recognised | what defeated it |
|---|---|---|
| 1 | the string `"4.0 bar"` | **case** |
| 2 | `"0.27 N/mm"`, in `<li>`/`<p>` only | **unit and element type** |
| 3 | `<span class="reg-code">` only | **HTML class name** |
| 4 | a figure adjacent to its unit | **number formatting** (`0.27-0.35 MPa`) |
| 5 | 14 operative phrasings | **wording** (`BMP5 is the current industry guidance`) |

Each fix was correct for the instance in front of it, and each was defeated by the next
disguise. An enumeration of renderings is an **open set** — the reviewer always has one more.

> **Rule.** Make the rendering stop mattering. Normalise it away before matching; invert the
> default so an unlisted form fails **closed**; compare **quantities**, not strings. A list is
> acceptable only where the set is closed by nature — inline tags, unit conversions — never
> where it enumerates how an author might phrase or mark up a claim.

**Match on visible text, never on raw HTML.** Entities, `&nbsp;`, unicode dashes, superscripts
and a figure split across tags are all invisible to a reader and must be invisible to the guard.
`0.27&nbsp;MPa`, `<strong>0.27</strong> MPa` and `0.27 <span>MPa</span>` are one string.

**Cover elements by EXCLUSION.** A block-tag allowlist cannot be finished — `<dd>`,
`<figcaption>`, `<caption>` were all missed. The *inline* set is small, standard and closed, so
define blocks as everything else and an unfamiliar tag is segmented correctly for free.

**Scope denial to the proposition.** `BMP5 replaced BMP4, but BMP5 is what we use today` is two
propositions and only the second is a defect. A denial token anywhere in the element silenced
both — the negative image of the phrase list.

**Use a RELATIVE tolerance for converted units.** `2.7538 kg/cm2` and `39.16 psi` are both
0.27 MPa to any practical precision and exact equality sees neither. 1% is safe here because the
two governed limbs differ by 8%.

**Three parser bugs, each of which silently narrowed the guard:** a container stack sampled at
flush time loses every inline ancestor, because an inline end tag pops before the flush; classes
must be unioned over the whole segment, or an inline `<a class="toc-link">` opened mid-run is
invisible and every navigation row reads as teaching; and an em-dash aside is not a proposition
boundary — splitting there severed a historical framing from the clause it governs and reported
the corpus's own supersession card as a defect.

**A schema refusing your record is the schema working.** The guard hardening changed no product
byte, so it could not supply a card, a `PRIMARY_CORRECTION` or a digest pair. Manufacturing one
to fit would have produced the decorative record the schema exists to forbid. It was written as a
chained governance document instead.

### 102. A shell heredoc eats `\b`, and the regex still compiles

`oral_currentness.py` shipped at `a2c83bd` with a literal `0x08` byte where `\b` belonged, in
two alternatives — `questions on\b` and `replaced\b`. Written through a bash heredoc that
consumed one backslash. Nothing failed: the module imported, the pattern compiled, every gate
stayed green, and both alternatives were simply **unreachable** for two days.

**A regex that compiles is not a regex that matches.** The damage is invisible to syntax checks,
to review, and to any test whose input does not need that alternative — which is every test,
because the alternative is what would have made the input pass.

**Both failed CLOSED**, which is why no defect escaped: the dead alternatives were *excuses*, so
losing them made the detector more suspicious rather than blind. That was luck, not design. Had
the byte landed in a MUST-CATCH alternative it would have opened a hole with every gate green.

**Do this:** never write a regex through a heredoc. Use the file-editing tools, and scan for
control bytes (`grep -c $'\x08'`) after any shell-mediated write. Repaired here, and the same
scan found a third instance in the mutation suite before it ran.

### 103. A check can pass for a reason it does not name

`E4_label_does_not_leak_across_containers` asserted that a heading in a CLOSED sibling block
lends no subject to the block after it. It used the heading "Lifeboat davits" — which the
*subject* test refuses whether or not the container bound exists. The bound was never exercised.
Removing the bound entirely did not turn the check red.

**A negative check must fail if the property is removed.** Pick the input that WOULD produce a
hit if the guard were gone: same subject, same governed figure, differing only in the property
under test. Here that is the same `Fire main` heading and the same `0.27 MPa`, separated only by
a closed container.

The mutation suite found this, and it is the argument for detector mutations: the corpus is
clean, so a corpus-only suite tests the guard on the one input where it cannot fail.

### 104. Tag names are not element identity

The same check hid a second defect. A label's reach was bounded by comparing the ancestor **tag
name** path — but two sibling `<div>`s both spell `div`, so a heading's container and the next
container along were indistinguishable and the label leaked across a boundary that looked
enforced. Fixed by giving every open element a serial and comparing those.

**When you bound something by structure, bound it by identity.** A path of tag names is a
description, not an address.

### 105. Redundant defences make a mutation lie

The rule "a coordinator splits clauses, not noun lists" turned out to be upheld three times
over: the left side must carry a finite verb, the right side must open with one, and a verbless
fragment merges forward instead of standing alone. A mutation removing the first reported an
ESCAPE — the control stayed green because the other two still held the property.

**An escape can mean the mutation was too weak, not that the guard is.** Before recording an
escape, check whether the property is defended elsewhere; if it is, the mutation must remove
every defender, or it credits a kill it never made. Defence in depth is worth keeping — the
mutation is what has to change.

### 106. Word order is not clause structure

E1 was closed once by requiring a coordinated clause to OPEN with its verb — sound
reasoning about a coordinated *predicate*, which shares its subject and so begins with the
verb. It caught `BMP5 replaced BMP4 and remains the current standard` and was blind to the
commoner shape, where the live clause states its own subject:

> `BMP4 was withdrawn and BMP5 is the current industry guidance.`

No split, so the denial in the first clause silenced the second — the exact defect, back
under a different word order.

**Count predications, not word positions.** A coordinator joins clauses when BOTH SIDES
CARRY A FINITE VERB. A noun list (`BMP5 and BMP4 are historical predecessors`) predicates
once and is left intact. The rule got shorter and stronger at the same time.

### 107. A `$`-anchored label pattern dies of four extra words

E3 was closed once with a label:value shape (`^subject : figure $`) plus a numbers-context
vocabulary. Both were walked past immediately:

- `Hydrant pressure: 0.27 N/mm2 on cargo ships` — the trailing qualifier broke the anchor;
- `SOLAS II-2/10.2.1.6 gives 0.27 N/mm2 at the hydrant for cargo ships` — prose, so no
  vocabulary hit.

And the reg-box row is the very surface three earlier defects in this family were found on.

**When the FIGURE is the regulation, let the figure do the work.** 0.27 and 0.25 MPa are
the two limbs SOLAS II-2/10.2.1.6 fixes, so a fire-main sentence stating one is asserting
the regulation whether or not it says "minimum". Invert the default: a claim unless it
reads as an observation. Every legitimate case in the contract carries an UNGOVERNED
figure and is refused before the question is reached — which is what makes the inversion
safe, and is worth checking before inverting any default.

Seventh instance of one lesson: a shape and a vocabulary are both open sets.

### 108. A markup choice a reader cannot see must not change what a guard sees

`<th>Fire main hydrant pressure</th><td>0.27 N/mm2</td>` was caught. The identical row
written `<td>…</td><td>…</td>` was **invisible** — `th` was a label tag and `td` was not.

Two-cell label/value rows are this corpus's dominant numeric idiom: **153 of its 224
files**. A guard blind to that shape is blind to the most likely place the next defect
gets typed.

**When a structural rule keys on a tag, ask what the tag means to a reader.** `td` and
`th` are the same thing to a candidate reading a Numbers table. The rule is now positional
— the FIRST cell of a row labels the rest of that row — and the scope ends with the row.

### 109. English prefers the pronoun, so the pronoun is the likelier defect

E1 was closed for `BMP5 … and BMP5 …` and for `BMP5 … and <other subject> …`, then reopened
by the form a person would actually write:

> `BMP5 was superseded in 2025, but it is still the guidance we apply on board.`

`but` is a hard sentence boundary, so the live clause landed in the next group and subject
inheritance stopped at the boundary. The forms the detector caught are the ones a writer is
*least* likely to produce, because repeating a proper noun in the second clause is
unnatural.

**Rank your test cases by how a human would write the sentence, not by how a regex would.**
A pronoun subject now inherits across one boundary, bounded by an explicit currency claim.

### 110. Two detectors for one policy must excuse the same things

`bmp5_current_teaching` consulted a whole excused-class set — examiner stems, navigation,
bibliography. `firemain_scope_defects` skipped three provenance classes and nothing else,
so it would have reported an examiner's own stem, quoting a regulation figure in the
question, as a defect.

**The direction of a false positive matters.** This one points an operator straight at the
edit the corpus rule most forbids: modernising anchored historical wording. A guard that
recommends the prohibited action is worse than a guard that stays quiet.

Also fixed alongside: a dated frame (`Before 2025 the guidance was region-locked — BMP5
for the Red Sea…`) is a denial. That sentence is live in `QB4_H.html` and survived only
because its container happened to carry a governing note; on a cheat sheet the same words
were reported as teaching BMP5 as current. **Correct content must not depend on which
container it was filed in.**

### 111. An exemption is a blind spot, and it is where the last defect hides

`bmp5_current_teaching` exempts an entire card whose banner says the publication was
superseded. So a live claim INSIDE that card — "BMP5 is the current industry guidance" —
is invisible, while the same words one byte outside are reported.

That is precisely this corpus's own documented defect. `QB4_B.html` records: *"the body and
Numbers layers still taught BMP5 as the current publication, contradicting this card's own
banner"*. **The banner is what buys the immunity.**

Worse, the exemption exists to hide a measured **18 of 18 false-positive rate** on real
historical sentences ("BMP5 was published in 2018", "BMP5 covered the Red Sea"). A
whitelist that broad is not a policy; it is a symptom that the rule underneath it does not
discriminate.

**When you add an exemption, measure what it HIDES, not only what it fixes.** Neutralise it
and count the hits: if most are legitimate, the sentence rule is the thing to repair. Here
the honest fix is a tense-and-aspect rule — a past-tense predication about a superseded
publication is history — not a wider whitelist.

And the exemption's own container test read RAW HTML with a literal attribute pattern: the
one path that never went through the normalising segmenter. `<div id="q1" class="q-card">`
broke it, turning a whole card of correct history into reported defects.

**Audit exemption paths to the same standard as detection paths.** They are load-bearing in
the opposite direction, and they are the easiest thing to forget when the detector is what
is under review.

### 112. HSSC is a statutory regime; the class survey cycle is not HSSC

`QB3_B#q9` taught, in both memorisation-weighted layers, that "the Classification
Society survey system operates on a 5-year Harmonized System of Survey and Certification
(HSSC) framework", under a section headed "Survey Types and Periodicity (HSSC)", citing
"IACS HSSC Guidelines". Four sites in the same file repeated the attribution.

**HSSC was introduced by the 1988 SOLAS and Load Line Protocols** and harmonises the
intervals and validity of **statutory certificates**. Its guidelines are IMO Assembly
instruments — A.1207(34), adopted 3 December 2025, revoking A.1186(33) — and they invite
**Governments** carrying out surveys under IMO instruments to apply them. There is no
such thing as an "IACS HSSC Guideline". The class cycle (Annual / Intermediate /
Special) comes from the society's own Rules on the **IACS UR Z series**.

The two are **deliberately aligned in interval** so class and statutory surveys can be
taken on one attendance, and a society acting as an RO does statutory work in a
different legal capacity on the same visit. Alignment and co-location are exactly why
the conflation is easy — and why it is dangerous.

**The bottom survey is the teaching case.** It exists in BOTH regimes on the same
interval — two inspections in any five-year period, max 36 months — statutory under
SOLAS I/10 and class under IACS UR Z3. An overlap is not a merger.

The card's own "Key distinction for exam" bullet had said the right thing four bullets
below the defect. **When a card contradicts itself, the defect is usually in the layer
that gets memorised**, because that is the layer written fastest.

### 113. "Automatic" belongs to overdue SURVEYS, not to an overdue Condition of Class

`QB1_K#q2` taught that missing a CoC deadline suspends class **automatically** and
"collapses the statutory certificates". IACS **PR1C** draws the opposite distinction and
does it with one word:

| Trigger | PR1C wording |
|---|---|
| Special/Renewal survey overdue (A.1.1) | *"classification is **automatically suspended**"* |
| Annual +3 months (A.1.2), Intermediate +3 months (A.1.3) | *"**automatically suspended**"* |
| Continuous survey item overdue (A.1.4) | *"subject to a **suspension procedure**"* |
| **Overdue condition of class (A.2.1)** | *"subject to a **suspension procedure**"* |

"Automatically" runs through A.1 and is **absent from A.2**. And B.1.3 says the letter
states that **"certain statutory certificates are implicitly invalidated"** — *certain*,
not all — with B.1.1/B.1.2 requiring written confirmation to the **Owner and the Flag
State**, which is the mechanism an examiner asks for next.

Two lessons beyond the content. **First: an earlier audit pass had this backwards in
both directions** — it defended "automatic" and asked for the statutory clause to be
softened. Primary evidence reversed both. A finding is not evidence; the instrument is.

**Second: the corpus disagreed with itself.** `QB1_F` already taught the correct
distinction, the six-month withdrawal rule (A.4.1) and "certain statutory certificates".
A defect present in one card and absent from its sibling is not systematic — and
checking the sibling first would have found the answer without any research.

**Currency footnote:** the correction was verified against Rev.6; `QB1_F` cites Rev.7 in
force from 1 January 2026 with the same substance. Recorded in the card, not silently
chosen — PR1C is also a harmonized **floor**, and a society's own Rules may go further.

### 114. A UI is a fallback, and a real instrument cited for the wrong proposition beats any existence check

`QB1_H#q3` said a Unified Interpretation, "once accepted", becomes "the standard by
which Flag States and ROs interpret the convention" — while the same card's trap line
said "a Flag State may reject a UI and issue its own interpretation". The trap line was
right.

A UI addresses provisions that are vaguely worded or **left to the satisfaction of each
Administration**. IACS societies apply it to ships whose flag Administration has **not
issued definite instructions**, in the course of statutory certification on that
Administration's behalf. **It governs silence and yields to instruction.**

The second defect is the more instructive one. The card cited **"PR 1C — transfer of
class"**. PR1C is real; it is the suspension/withdrawal procedure. **A real instrument
attached to the wrong proposition survives every check that only asks whether the
instrument exists** — which is most citation checks, including automated ones.

The correct PR letter for transfer of class was **not** established, so none was
asserted: the card names the concept, says it is not PR 1C, and tells the candidate not
to quote a letter unverified. **An unresolved citation is left unresolved out loud.**
Substituting a plausible number would have reproduced the exact defect being fixed.

### 115. Documenting a trap does not prevent it — only a check does

Entry #102 recorded that a shell heredoc silently turns `\b` into a literal `0x08`, so
the regex still compiles and the alternative can never match. **It then happened twice
more in the same session**, once in `mutate_correction_p1guard.py` and once in a
`hidden`-element guard written minutes after #102 was filed — where it let a live
mutation escape and the gate report PASS.

**A lesson in a register is not a control.** `validate_correction_d01s01.py` now scans
every `tools/**/*.py` for the byte and fails closed.

And the first version of that scan **reported itself**, because its needle was written
as a literal escape and so contained the byte it was hunting. Build the needle with
`chr(8)`. A detector that cannot be written safely in the same language it detects is a
detector that will find itself first.

### 116. The string went away. The proposition did not.

`CORR-D01-HSSC-CLASS-20260907` corrected the class-cycle-is-HSSC defect in `QB3_B#q9`,
swept for propagation, and gated the result with `"IACS HSSC" appears nowhere`. The string
genuinely vanished. The commit message said so, and it was **literally true**.

An independent audit then found the **proposition** alive in six sites, none of which
contained the token:

| where | what it said |
|---|---|
| q1 60-second | "follows the **IACS Harmonized System of Survey and Certification (HSSC)** cycle" |
| q11 15-second | "resets the 5-year **HSSC** clock" |
| q11 60-second | "resets the 5-year **HSSC** cycle" |
| q11 heading | "Post-Renewal **HSSC** Matrix" |
| q11 CE Oral Tip | "the statutory **HSSC** intermediate matrix" |
| q11 Examiner Chain | "Resetting **HSSC** Timeline" |

Both cards were left **contradicting themselves** — a corrected REG-BOX saying HSSC is a
separate statutory regime, and a memorisation-weighted layer saying the class cycle is
HSSC. **A partial correction is worse than none: it gives the defect an alibi.**

This is trap #101 ("enumerating renderings never converges") reproduced one session after
it was written down, by the author of #101.

**Two rules came out of it.** First, gate the PROPOSITION: a matcher that folds the
acronym and the spelled-out name, at sentence scope, with an explicit acquittal for
sentences that draw the distinction. Second, **guard every candidate-facing layer by
name** — a card-wide "is the phrase present somewhere" test cannot tell a corrected
REG-BOX from a defective 15-second answer, which is exactly the state these cards were in.

The proposition-scoped control then found **six further cards** the grep families had
missed: `QB1_F#q8`, `#q13`, `#q14`, `#q16`, `QB1_G#q30`, `#q31`, `QB1_I#q5`. The grep and
the token check both said the corpus was clean. It was not.

### 117. A narrow check and a broad check fail in opposite directions, and both are wrong

Building the proposition matcher took four rounds, alternating between the two failures:

- **Too narrow:** the ESP scope check required the word "ESP" within 140 characters of the
  ship list. Two sites wrote "…the ESP Code. **It applies** to oil tankers, chemical
  tankers…" — the subject in the previous sentence — and walked straight past. Two more
  scope sites were found only after the check was rewritten to read the scope statement
  itself.
- **Too broad:** the same matcher then flagged `QB1_G#q24` ("the Cargo Ship Safety
  Certificate under the **HSSC scheme**") and `QB2_A#q15` ("the ICOF's 5-year **HSSC
  cycle**"). Both are **correct**: those are statutory certificates, and a statutory
  certificate's survey cycle genuinely *is* HSSC.

**The fix was to name what the defect actually is.** HSSC legitimately *is* a framework
and a scheme; what it does not have is a **cycle** or a **clock** that a *class* survey
runs on. Dropping "framework" and "scheme" from the noun list, and keeping "cycle",
"clock", "matrix", "timeline", separated the two.

**Widening a check until it fires on correct content is not thoroughness.** It forces you
to either edit right answers or add exceptions until the check means nothing — and it
drags in unrelated cards the batch was scoped to leave alone.

### 118. A record must declare where its edit LANDED, not where it was aimed

An `A.1156(32)` → `A.1207(34)` fix was written with `count=1` and replaced the **first**
occurrence in the file — which was in `QB1_F#q7`, a card explicitly out of batch, not the
`q14` site it was aimed at. Nothing crashed. The card is better for it. But the record
declared `q14`, and the change to `q7` was **undeclared**.

`every_pinned_state_is_live_or_a_proven_ancestor` caught it as `AMBIGUOUS_ROOT`, and
tracing where the edit had gone turned up a **third** instance in `q13`.

**`count=1` targets a position, not a card.** Anchor a replacement inside the card's own
byte span, or verify afterwards which anchors moved. The edit was declared rather than
reverted — reverting would have restored a stale instrument this pass had already
identified — but the declaration is not optional.

### 119. A later correction must not require its predecessor to rewrite history

Correcting cards that three earlier records had already pinned turned four gates red at
once: `PIN_MISMATCH` on six cards, a typed-block invariant, and a token check reading the
new version stamps — which **quote** the old string in order to record its removal
(trap #89, in the gate written to prevent a related failure).

None of those was a defect in the earlier records. They are what supersession looks like
when it has not been declared. The repository already has the mechanism —
`oral_supersession`, and a `supersedes` claim naming the predecessor manifest, action id
and post-digest — and **the resolver treats a card with no claim as dormant**, which falls
back to a plain pin comparison and fails.

**Ten claims later, every chain resolved.** The lesson is not "add a claim"; it is that a
correction system needs a way for a record to be *superseded without being falsified*, and
if you find yourself editing a predecessor's pins, you have skipped it.

### 120. IACS has twelve Members, and the one that goes missing is the Korean Register

`QB4_E#q12` — the card whose entire job is to list the members — taught **eleven** in its
15-second answer, its 60-second answer and its CE tip, and hedged "11 or 12 members
depending on the inclusion of the newest member, Türk Loydu". Its own detail list
immediately below already carried **twelve**, including **KR**. The card contradicted
itself on its single load-bearing fact, and the 60-second list — the one a candidate
recites — was the layer that had dropped KR.

The membership is: ABS, BV, CCS, CRS, DNV, IRClass, **KR**, LR, ClassNK, PRS, RINA, TL.
Türk Loydu was admitted 1 November 2023 as the twelfth; RMRS was terminated in March 2022.

**A hedge is not caution when the fact is settled.** "11 or 12 depending on" reads as
scholarly care and is simply a wrong answer with a hedge attached — and the hedge told a
candidate to expect ambiguity where an examiner expects a number. The tell that this was
a defect rather than a genuinely open question was inside the card: a list of twelve
sitting under a sentence saying eleven.

### 121. UR Z15 is Mobile Offshore Drilling Units. Suspension and withdrawal of class is PR1C

`QB4_C#q5` cited **IACS UR Z15** as the instrument that "outlines standardized
international procedures for class suspension and withdrawal", in its Regulatory
References box and again in Numbers & Regs. UR Z15 is *Hull, Structure, Equipment and
Machinery Surveys of Mobile Offshore Drilling Units*. It has nothing to do with the
subject.

The instrument is **PR1C**, *Procedure for Suspension and Reinstatement or Withdrawal of
Class in Case of Surveys or Conditions of Class Going Overdue*.

**A citation in the right register is the hardest kind of wrong to see.** "IACS UR Z15"
has the right issuer, the right series and the right shape, so every reader who was
checking that a citation *existed* passed it. Only a reader who opened it would find it
was about drilling units. An existence check cannot catch this class; only reading the
cited text can. (Compare #114 — a real instrument cited for the wrong proposition.)

### 122. MSC.554(108) did not abolish S = 0.4 + 0.02H

`QB10_B#q1` taught "1.0–1.3 m/s: new lifeboat lowering speed range (replacing the old
H-dependent formula)" in a formula block and again in Numbers to Memorise, and this was
carried as a P1 source gap through Pass 1 because a *replacement* claim cannot be
adjudicated from the number alone.

The primary text settles it. LSA Code **6.1.2.8**, as replaced by MSC.554(108): the
lowering speed "shall not be less than that obtained from the formula: **S = 0.4 + 0.02H,
or 1.0, whichever is less**". **6.1.2.10**: the maximum "shall be 1.3 m/s", and the
Administration may accept another. In force 1 January 2026 for appliances installed on or
after that date.

So both numbers in the card are real, and the proposition joining them is false: 1.0 m/s
is a **ceiling on the formula-derived minimum**, not a replacement for the formula, and
1.3 m/s is a default maximum the Administration can vary.

**Two true numbers do not make the sentence between them true.** The figures survived
every numeric check because they are the figures in the instrument. What was wrong was
the verb.

### 123. SOLAS III/33.2 was narrowed to davit-launched lifeboats, not removed

`QB10_B#q1` listed under the 1 January 2024 tranche: "SOLAS III/33 removed the 5-knot
headway test-launch requirement for ships ≥20,000 GT."

**MSC.482(103)** (adopted 13 May 2021, in force 1 January 2024) replaced III/33.2 with:
"On cargo ships of 20,000 gross tonnage and upwards, **davit-launched** lifeboats shall be
capable of being launched, utilizing painters where necessary, with the ship making
headway at speeds up to 5 knots in calm water."

The requirement was not removed. It was confined to davit-launched lifeboats, which is
what releases free-fall lifeboats from it — and it dropped "ships" for "cargo ships". A
candidate reading the card would tell an examiner that a davit-launched boat on a
25,000 GT bulker no longer needs the capability. It does.

**An exemption written as an abolition is a bigger error than the one it corrects.** The
card was right that something changed and right about the date; it inverted which
population kept the rule.

### 124. The container alliances changed in February 2025, and 2M is gone

`QB8_A#q3` offered "2M, Ocean Alliance" and "the Ocean Alliance or THE Alliance" as
current examples of a liner consortium. The 2M vessel-sharing agreement between Maersk and
MSC ended in January 2025; MSC now operates standalone. Hapag-Lloyd left THE Alliance in
February 2025 to form **Gemini Cooperation** with Maersk, and the remainder — ONE, HMM,
Yang Ming — rebranded as **Premier Alliance**. Ocean Alliance (CMA CGM, COSCO, Evergreen,
OOCL) is the only pre-2025 grouping still intact.

The same card called Regulation 906/2009 the "historical" block exemption without saying
what happened to it: the **Consortia Block Exemption Regulation expired on 25 April 2024**
and was not renewed.

**A commercial-currentness card decays on a schedule nothing in the repository tracks.**
Regulatory cards have resolution numbers and entry-into-force dates that a detector can
compare against. An alliance roster has neither — it simply stops being true one Tuesday,
and it reads exactly as authoritative the day after. Cards of this class need a stated
as-at date and a re-verification trigger, not a currentness regex.

### 125. MLC Regulation 1.4 is Recruitment and placement, not fair treatment

`QB5_A#q4` mapped Maslow's esteem level to "MLC Reg. 1.4 (Recruitment / Fair Treatment)"
in its Regulatory Hook column. MLC Reg. 1.4 is **Recruitment and placement** — the
regulation of manning agents. Fair treatment is not its subject, and recognition,
appraisal and promotion prospects have no MLC hook at all: they are management practice.

This is the third occasion a fair-treatment proposition has been attached to an MLC
regulation that does not carry it (see #38, the fabricated "Regulation 5.2.7", and #41,
Reg. 2.7).

**A management-theory card is where legal attributions go unchecked.** Nobody expects a
Maslow answer to contain a false citation, so the regulatory-hook column of a soft-skills
table is read as decoration rather than as a claim. It is a claim, and a candidate will
recite it.

### 126. A regex tag-stripper is not an HTML parser, and the gap between them invented a defect

`QB10_B#q1` contained `(e.g. <150 GT, fishing vessels)`. Extracting the card's visible
text with the toolchain's usual `re.sub(r"<[^>]+>", " ", …)` showed the sentence ending
mid-parenthesis and colliding with the next clause: *"subject to the usual V/1.4 exemptions
(e.g. Why: pilot transfer accidents…"*. About 150 characters were missing, including both
2028 and 2029 compliance dates.

I concluded a browser was eating them, corrected the card, wrote it into the version stamp
as candidate-facing fact, recorded it as a manifest invariant, built a gate check and a
mutation around it, and censused five more "affected" sites as remaining P1 debt.

**All of that was wrong.** An independent review disputed it, and a real browser settles it.
Serving the pre-fix string and reading the rendered text back:

```
exemptions (e.g. <150 GT, fishing vessels). New installations comply
immediately from 1 Jan 2028; existing arrangements by first survey
after 1 Jan 2029. ENDMARKER
```

Nothing was ever lost. HTML5 tokenisation is explicit: in the tag open state, anything
other than an ASCII letter, `!`, `/` or `?` after `<` is a parse error, the `<` is emitted
as a literal character, and the parser reconsumes in the data state. `<1` is text. Only
`<` followed by a **letter** opens a tag — and in the same probe, `unclosed <em comply …`
rendered as the single word `unclosed`, everything after it swallowed.

A corpus census for that genuinely damaging form — `<` plus a letter that is not a real
element name — returns **zero sites across all 224 pages**. The 75 distinct tag-like names
in `meoclass1/` are all real HTML or SVG elements. The defect class does not exist here.

The escaping to `&lt;` was kept, because it is correct markup regardless. Everything
claimed about its effect was withdrawn.

**Three compounding lessons, and the third is the expensive one.**

*The tool disagreed with the browser, and I believed the tool.* `<[^>]+>` is a decent
approximation of tag stripping and a bad model of a parser. It cannot see that `<1` is
text, so it deletes to the next `>` and reports damage that only exists inside itself.

*A gate can encode a fictional failure mode.* `amend_2028_compliance_dates_survive_rendering`
passed, and its mutation was CAUGHT — because the mutation was written against the same
wrong model. A green check and a caught mutation prove the gate is self-consistent, not
that it describes reality. Nothing in a mutation suite can catch this: the suite inherits
the author's model of the defect.

*A false claim in a version stamp is published to candidates.* This one reached the card
footer and a manifest invariant before anyone tested it, and the correction that carried
it was otherwise sound. Verify the MECHANISM, not just the symptom — especially when the
symptom is produced by your own extractor.

**Where the extraction convention is still right:** stripping tags from source is the
correct way to read teaching text, and it is what every content gate in `tools/oral/` does.
The failure was not using it; it was treating its output as evidence about a *browser*.
When a claim is about what a candidate SEES, render it.

### 127. Propagating a proposition means carrying its qualifications, not just its subject

`CORR-PASS2-CLOSEUP-SCOPE` propagated the annual close-up requirement from `QB3_B#q1` to
`QB3_A#q5`, and named that card as its entire authority. The source says:

> The annual survey itself — not just the special survey — **can require** a close-up
> examination of at least **25% of cargo hold side shell frames**, their lower end
> attachments and adjacent shell plating, in a forward cargo hold and one other selected
> hold … The requirement is also **age-conditioned**. This card does not state the age
> band, because it could not be verified against Z10.2 directly.

What arrived on `QB3_A#q5` was:

> On those ships the annual survey itself **includes** close-up examination of cargo hold
> side shell frames and their end attachments, so it is not held over to the special survey.

The population survived. The **extent**, the **hold scope**, the **modality** and the **age
condition** did not — and "can require, age-conditioned" became "includes". The record
claimed it *"deliberately asserts nothing that record did not"*. It asserted an
unconditional rule where its source asserted a conditional one, so a candidate would learn
that a two-year-old bulker gets an annual close-up of its side shell frames.

The 25% was dropped for a reason that sounded like discipline: the figure had entered the
corpus through a tier-6 blog, so restating it looked like laundering a bad source. But
`QB3_B#q1` had already re-attributed that same figure to **UR Z10.2** in the D01-S02 pass.
Deleting it was not conservatism; it was discarding an adjudication that had already been
made, and it left the bullet weaker AND broader than the source it cited.

**Two rules, and the second is the one that bites.**

*A propagation is only faithful if the qualifications travel.* Population, extent, scope,
modality and conditions are one proposition. Carrying the subject and dropping the limits
does not narrow the claim, it widens it — the most dangerous direction, because the
resulting sentence is shorter and reads more confidently.

*Check the sibling before deciding a figure is unsourced.* The question is not "where did
this number originally come from" but "what does the corpus currently attribute it to".
`QB3_B#q1` answered that, and reading it was already required — it was the record's only
authority.

The reverse defect was live in the same pair: `QB3_B#q1`'s own Numbers block still scoped
the 25% to "(bulk carriers/tankers)", contradicting the body and reg-box that D01-S02 had
corrected. One proposition, two cards, and each held a different half of it wrong.

**The gate now asserts the two cards AGREE**, on population, extent and age condition. A
propagation record whose gate cannot see a contradiction it created cannot certify the
propagation — and until this check existed, none of the six Pass-2 checks compared a card
to anything outside itself.
