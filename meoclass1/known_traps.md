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

## Meta-corrections to `qb_health_check.py` itself (non-content fixes, logged here for continuity)

- 2026-08-01: Fixed a Windows-console `UnicodeEncodeError` crash in the Brevo-fallback print path when SMTP credentials aren't set locally (was crashing on ⚠/✅ glyphs; also fixed a related bug where the fallback path's temporary `TextIOWrapper` around `sys.stdout.buffer` closed the underlying buffer on garbage collection, breaking all later prints in the same run).
- 2026-08-01: Fixed the "QB file(s) on disk but missing from manifest" orphan check to exclude `SQ/` — those are public teaser copies intentionally outside the gated `meoclass1/` manifest scope, not orphaned builds.
- 2026-08-01: Broadened `NEGATION_MARKERS` per Entry 20 above.

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
