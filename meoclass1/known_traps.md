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

GREP: Regulation 5.2.7
GREP: Standard A5.2.7
GREP: LEG 110 / LEG 111 outputs

Note: the corrected card intentionally retains the phrase "Standard 5.2.7" once,
inside the Examiner Trap block ("There is no MLC Regulation or Standard 5.2.7"),
and retains "Part III" throughout while correctly explaining its recommended
status. Both are negation-context hits per the pattern above — check the
surrounding sentence before treating either as resurfaced.
---

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
