# QI Phase 1 — session acceptance report

**Founder-facing return for the session of 2026-08-23 (Laptop, Opus 5).**
Answers the A–DG schedule set in the session brief, in order.

The engineering account — how the layer is built, why each rule exists, the
Top-25 with reasons — is [`QI_PHASE1_REPORT.md`](QI_PHASE1_REPORT.md).
This file is the acceptance checklist against that work.

---

## A–G · Boundaries

| | |
|---|---|
| **A. Start main SHA** | `cb234e7` — matched the expected neighbourhood exactly; main had not moved |
| **B. Final main SHA** | `1c826fb` — pushed fast-forward, working tree clean |
| **C. Lower QI boundary** | **2010** ✓ |
| **D. Upper QI boundary** | **2026-08** ✓ |
| **E. Pre-2010 search performed** | **NO** |
| **F. Pre-2010 data ingested** | **0** |
| **G. Pre-2010 backlog created** | **0** |

The horizon is enforced in code, not remembered. `qi_model.QI_LOWER_BOUNDARY`
and `QI_UPPER_BOUNDARY` gate the builder, and invariants 01 and 16 fail the
build if either is crossed.

---

## H–O · 2010–2020 source layer

| | |
|---|---|
| **H. Source pages / sets** | 115 archived pages |
| **I. Raw occurrence records** | 1,026 |
| **J. Distinct source entities** | 256 |
| **K. Question-text claim** | `CORROBORATED` |
| **L. Sitting-date claim** | `SECONDARY_CLAIMED` — 1,026 of 1,026 |
| **M. Official-occurrence claim** | `NOT_ESTABLISHED` |

The three claims are stored on three separate fields and are never collapsed
into `verified = true`.

**N. Source entity normalisation.** Entities key on the source's own question
id. Wording is modelled as **entity-level** — the source publishes one wording
per entity and reuses it on every set page — while what each archived page
evidences per sitting is **membership and ordinal**. Manufacturing per-sitting
full-text provenance out of a reused wording would have been the easy mistake.

**O. Duplicate / inflation corrections — two.**

1. The research layer's own `occurrence_id` is **not unique**. Three ids
   collide (`HOCC-2012-JUN-02`, `HOCC-2012-NOV-03`, `HOCC-2017-JUL-06`) because
   they key on a scraped `page_ordinal` and two distinct entities can land on
   one index. Governed identity keys on `printed_qno` and is unique in 1,584 of
   1,584.
2. The research join counts are occurrence-level, restating one entity-level
   decision once per asserted sitting. Re-derived at entity granularity:
   **1,873 modern join pairs → 285**, and **1,026 occurrences → 256 entities**.

---

## P–T · 2021–2026

| | |
|---|---|
| **P. 2021–2023 papers** | 30 held |
| **Q. 2021–2023 questions** | 270 held — **198 unique**, see below |
| **R. 2023–2026-08 papers** | 40 solved |
| **S. 2023–2026-08 questions** | 360 |
| **T. Latest included sitting** | **2026-08** — nothing later exists in the repository |

**The 72-question overlap.** Eight of the 30 wording-only papers — `QP2302`,
`QP2303`, `QP2306`–`QP2311` — are **also** in the solved corpus, under the same
question ids. Emitting both would have counted 72 questions twice and inflated
every 2023 recurrence measure in the model. The builder suppresses the
wording-only copy, records which 72 and why, and mutation M proves the gate
rejects a rebuild that reintroduces them.

**The two bands cannot be added.** Unique contribution of the wording-only band
is **22 papers / 198 occurrences**.

---

## U–Y · Entity / limb model

| | |
|---|---|
| **U. Total governed source entities** | **814** — 256 historical, 198 wording-only, 360 solved |
| **V. Total governed occurrences** | **1,584** |
| **W. Governed limb occurrences** | **698** `GOVERNED_LIMB` records — stored, addressable, **not counted** |
| **X. Whole-question-only occurrences** | 1,052 |
| **Y. Limb adjudication holds** | **272** — 171 historical, 101 wording-only |

The 272 holds carry limb markers detected lexically and never semantically
adjudicated. They are recorded as whole-question occurrences with their markers
preserved, and **no limb family is built on any of them**, so none inflates
anything.

---

## Z–AK · Family adjudication

| | |
|---|---|
| **Z. Entity→modern candidate pairs** | **285** (prior estimate 287 — confirmed) |
| **AA. Entity→family candidate pairs** | **37** historical×historical |
| **AB. Exact/high joins reviewed** | **1,025 proposals → 180 groups, every group read in full** |
| **AC. `SAME_FAMILY`** | 90 |
| **AD. `SAME_FAMILY_VARIANT`** | 180 |
| **AE. `SAME_LIMB_FAMILY`** | 0 |
| **AF. `WHOLE_VS_LIMB_RELATION`** | 23 |
| **AG. `RELATED_BUT_DISTINCT`** | 8 |
| **AH. `DISTINCT`** | the remaining proposals, not recorded as joins |
| **AI. `AMBIGUOUS_HOLD`** | **0** |
| **AJ. New families created** | 270 (the layer did not exist before) |
| **AK. Total governed recurrence families** | **270** |

No score decided anything. Every merge threshold is applied to
**containment_low**, and 0 entities sit in more than one family.

### Five splits made against the algorithm

| Split | Proposed merge | Why it is wrong |
|---|---|---|
| SPLIT-001 | Hydrogen ↔ Ammonia as a marine fuel | Same framing sentence, different chemistry |
| SPLIT-002 | EEXI ↔ EEDI | Two instruments: existing vessels 2023 vs new builds 2013 |
| SPLIT-003 | Blockchain ↔ 3D Printing | The examiner's template, not the answer |
| SPLIT-004 | Charter-survey limb ↔ whole Bill of Lading question | The limb holds **8** occurrences of its own |
| SPLIT-005 | 2-limb ↔ 4-limb exhaust-emission bundle | Short form needs neither Tier II/III nor SCR |

Three of five are the same failure — an identical framing sentence wrapped
around a different subject noun. That is now a named, tested detector (rare-token
divergence audit) rather than something someone happened to notice.

### A defect in my own method, found and fixed

The first similarity probe reused the **blocked** overlap count as the score.
Blocking skips high-frequency tokens, so every pair built from common
vocabulary was deflated — two byte-identical stems scored 0.70. Blocking finds
candidate pairs; scoring must be recomputed on full token sets. All figures
above are post-fix.

---

## AL–AQ · Coverage

| | |
|---|---|
| **AL. Distinct years represented** | **17** (2010–2026) |
| **AM. Distinct sittings represented** | **176** months with a source, of 200 in the horizon |
| **AN. Year coverage matrix** | `docs/study/qi/qi_coverage_matrix.json`, per-month and per-year |
| **AO. Source gaps** | 1 — `2010-09`, `NO_ARCHIVE_CAPTURE`, the only pure acquisition gap |
| **AP. Unknown sittings / months** | **24** |
| **AQ. Confirmed no-exam periods** | **0** |

`NO_EXAM_OFFICIALLY_EVIDENCED` requires an official instrument stating no
examination was held. None is held, so **not one month** is treated as a
confirmed zero-question sitting. Every other absence stays UNKNOWN and is
excluded from denominators rather than counted as a zero. Mutation L flips one
and the gate catches it.

### Finding: May is absent in all 17 years

For 2010–2019 that rested on one secondary index's silence, and the earlier
adoption decision was right to refuse to promote it. But 2021–2026 is different
evidence entirely: MIW holds its own source copy of every other month and none
for May. Two independent lines now agree, one of them MIW's own.

Recorded as `CORROBORATED_INFERENCE_NOT_OFFICIAL_EVIDENCE`. The months stay
UNKNOWN — corroboration is not an official instrument.

---

## AR–BC · Recurrence

| Window | Families with activity |
|---|---|
| **AR.** 3Y (2023-09 → 2026-08) | **121** |
| **AS.** 5Y (2021-09 → 2026-08) | **164** |
| **AT.** 10Y (2016-09 → 2026-08) | **222** |
| **AU.** Full horizon | **270** |

| Label | Families |
|---|---|
| **AV.** `PERSISTENT` | 76 |
| **AW.** `RECENTLY_ACTIVE` | 121 |
| **AX.** `RISING` | 57 |
| **AY.** `RE_EMERGING` | 54 |
| **AZ.** `DORMANT` | 149 |
| **BA.** `HISTORICAL_ONLY` | 96 |
| **BB.** `NEW_EMERGING` | 78 |
| **BC.** `INSUFFICIENT_HISTORY` | 0 |

Labels are multidimensional. `QIF-EM-0002` is `PERSISTENT` **and**
`RECENTLY_ACTIVE` **and** `RE_EMERGING` at once — 22 occurrences across ten
years, set continuously to 2022, absent 45 months, set again in 2025.

`RE_EMERGING` was wrong in the first build: it fired on any meaningful gap
anywhere in a family's history and reported 91. Re-emergence is about the shape
of the *return*, so it keys on the latest gap only. Corrected figure: 54.

---

## BD–BK · Currentness

| Class | Families |
|---|---|
| **BD.** `CURRENT` | 0 — requires research Phase 1 does not do |
| **BE.** `CURRENT_WITH_AMENDMENT` | 42 |
| **BF.** `CURRENT_FRAMEWORK_CHANGED` | 49 |
| **BG.** `LIKELY_SUPERSEDED` | 0 |
| **BH.** `HISTORICAL_ONLY` | 62 |
| **BI.** `CURRENTNESS_REVIEW_REQUIRED` | **25** |
| **BJ.** `UNKNOWN` | 92 |
| **BK.** Time-relative language flags | **25 families** |

`UNKNOWN` is never read as `CURRENT`. It means nobody has checked.

The time-relative trigger catches the risk an instrument-name check is blind
to: a stem asking for *"the ongoing developments at IMO"* names no convention,
so nothing about it looks dated while its correct answer changes every year.
Leading case `QIF-EM-0017` — 13 occurrences, nine distinct years, 2010-11 →
2024-02. Invariant 19 recomputes every flag from the stems; mutation H strips
one and is caught.

**Currentness never moves a recurrence count.** Different inputs, different
files, enforced by invariant 14.

---

## BL–BV · Phase 2

| Action | Families |
|---|---|
| **BL.** `CURRENT_AND_SOLVED` | 72 |
| **BM.** `EXISTING_CURRENT_ANSWER_VERIFY` | 59 |
| **BN.** `NEW_MODERN_ANSWER_REQUIRED` | 37 |
| **BO.** `HISTORICAL_ANSWER_REQUIRES_MODERNISATION` | 3 |
| **BP.** `SUPERSEDED_MODERN_REPLACEMENT_REQUIRED` | 0 |
| **BQ.** `CURRENTNESS_RESEARCH_REQUIRED` | 8 |
| **BR.** `LOW_PRIORITY_HISTORICAL_ONLY` | 91 |
| **BS.** `AMBIGUOUS_FAMILY_REVIEW` | 0 |
| **BT. Total action queue** | **270 — every family, none unclassified** |

**BU. Top 25 Phase-2 families** — with counts, currentness, action and reason:
[`QI_PHASE1_REPORT.md` §10](QI_PHASE1_REPORT.md). Machine-readable at
`docs/study/qi/qi_phase2_action_queue.json`, ranked.

**BV. Modern canonical question action counts**

| Action | Families |
|---|---|
| `USE_EXISTING_CANONICAL_QUESTION` | 98 |
| `HISTORICAL_ONLY_NO_MODERN_QUESTION` | 91 |
| `MERGE_VARIANTS` | 41 |
| `CREATE_NEW_CURRENT_CANONICAL_QUESTION` | 37 |
| `MODERNISE_CANONICAL_QUESTION` | 3 |
| `SPLIT_LIMB_FAMILY` | 0 |

Priority lets recency outrank historical bulk deliberately: old + frequent +
obsolete must never outrank recent + recurrent + still-set.

---

## BW–CB · Study preview

| | |
|---|---|
| **BW. Current study domain order** | `D03 > D01 > D02 > D05 > D04 > D07 > D06 > D09 > D10 > D08` |
| **BX. QI-informed preview order** | `D03 > D01 > D02 > D05 > **D07 > D04** > **D09 > D06** > D10 > D08` |
| **BY. Domain score preview deltas** | D03 +0.0105 · D01 0.0000 · D02 −0.0077 · D05 −0.0225 · D07 −0.0201 · D04 −0.0380 · D06 −0.0189 · D09/D10/D08 0.0000 |
| **BZ. Actual study weights changed** | **NO** |
| **CA. Active session files changed** | **0** |
| **CB. `study_progress.json` changed** | **NO** |

**The active front does not move.** D03, D01 and D02 hold ranks 1–3 in both
orders; two adjacent pairs swap at ranks 5–6 and 7–8. **`D01 → D03 → D02`
stands untouched.**

Only one of six priority components changes (`written_recurrence`, weight
0.13), so the delta isolates governed recurrence and nothing else. The preview
tool asserts it writes no study file and fails if it ever does.

Its "136 families reach no topic" splits into **96** historical-only families
the taxonomy has never had a modern question for, and **40** whose modern member
sits in the 2021–2022 wording-only band the taxonomy has never been asked to
map. Reported as one number the Phase-2 backlog would be badly overstated.

---

## CC–CF · Public safety

| | |
|---|---|
| **CC. Internal 2010–Aug-2026 QI status** | **LIVE** — governed, internal use permitted |
| **CD. Public "official since 2010" claim** | **NOT PERMITTED** — unchanged, and this build moves it no closer |
| **CE. Public historical copy diff** | **0** |
| **CF. Marketing diff** | **0** |

1,026 of 1,584 occurrences carry `SECONDARY_CLAIMED` dates and no official
document dates any 2010–2020 sitting. More coverage cannot fix that, because
coverage is not the missing thing. Invariant 18 fails the build if any
historical occurrence is ever relabelled `OFFICIAL_DATED` without a Founder
decision behind it; mutation F proves it.

---

## CG–CR · Validation

| Guard | State |
|---|---|
| **CG.** Pre-2010 | INV01 — holds |
| **CH.** Post-Aug-2026 | INV16 — holds |
| **CI.** Source-entity uniqueness | INV02 — holds |
| **CJ.** Occurrence uniqueness | INV03 — holds |
| **CK.** Duplicate-count guard | INV04, INV05, INV12 — hold |
| **CL.** Limb / whole guard | INV06 — holds |
| **CM.** DGS-bank-not-occurrence guard | INV11 — holds |
| **CN.** Provenance / date-confidence guard | INV09, INV10 — hold |
| **CO.** Broken-join guard | INV08 — holds |
| **CP.** Currentness guard | INV14, INV19 — hold |
| **CQ.** Phase-2 queue coverage guard | INV15 — holds |
| **CR. Mutations** | **14 caught / 0 escaped / 0 residue** |

19 invariants in total (INV07 family-id uniqueness, INV13 counts derive from the
occurrence layer, INV17 silence-is-not-a-zero, INV18 public claim barred).

```
A pre-2010 occurrence            -> INV01     H currentness flag stripped   -> INV19
B duplicated source entity       -> INV02     I risky family dropped        -> INV15
C occurrence counted twice       -> INV05     J occurrence after ceiling    -> INV16
D limb promoted to whole         -> INV06     K count hand-edited           -> INV13
E question bank as occurrence    -> INV11     L silence counted as zero     -> INV17
F secondary date -> official     -> INV18     M modern question duplicated  -> INV12
G broken family join             -> INV08     N entity twice in one sitting -> INV04
```

The builder also fails closed on its own inputs — verified live: a changed
proposal set breaks the pinned adjudication digest, and a recorded split
matching no entity stops the build rather than shipping an unreviewed family.

---

## CS–CX · Invariants

| | |
|---|---|
| **CS. Oral question-text diff** | **0** |
| **CT. Oral answer diff** | **0** |
| **CU. Written answer diff** | **0** |
| **CV. Examiner relationship diff** | **0** |
| **CW. Study taxonomy diff** | **0** |
| **CX. Study progress preserved** | **YES** |

The change is **purely additive**: 18 new files, **zero existing files
modified**, zero deleted — apart from the one documentation file noted below.

One thing to record: running `test_roadmap_cockpit.py` regenerates
`MIW_MEO_Class1_Study_Roadmap.xlsx` as a side effect, and it was swept into a
commit. Only `docProps/core.xml` differed — the embedded build timestamp, zero
content change. It was restored to its `cb234e7` bytes and the commit amended.
This is the known roadmap byte-reproducibility debt, recorded and not fixed
here.

---

## CY–DC · Delivery

| | |
|---|---|
| **CY. Tests** | QI: 19 invariants + 14 mutations (0 escapes, 0 residue). Existing suites re-run unchanged: **1,187 assertions pass** — `validate_study_spine` 660, `test_study_expandability` 339, `test_mapping_engine` 132, `test_d01_priority_cohort` 19, `test_historical_qi_inventory` 19, `test_roadmap_cockpit` 18 |
| **CZ. Files changed** | 18 added, 1 modified (`tools/study/SKILL.md`), 0 deleted |
| **DA. Commits** | 4 |
| **DB. Push status** | **Pushed fast-forward** `cb234e7..1c826fb`, never forced |
| **DC. Deployment** | **NONE** — `tools/` and `docs/` are both deploy-excluded |

```
504649f  feat(qi): one governed question-intelligence model, 2010 to August 2026
78fd5a8  feat(qi): unify all three evidence bands into one occurrence layer
c51ba73  feat(qi): recurrence windows, currentness triage and the Phase-2 queue
1c826fb  docs(study): point the study contract at the one QI brain
```

---

## DD–DG · Verdict

### DD. Phase-1 status

**`COMPLETE_2010_TO_2026_08`**

### DE. Remaining Phase-1 blockers

**None.** Four non-blocking holds, none of which can affect a material
recurrence result:

1. **272 limb-marker holds** — recorded as whole-question occurrences with
   markers preserved; no limb family is built on any of them, so none inflates
   anything.
2. **291 relation-strength pairs where one side has no family** — a
   single-occurrence entity is not a family and a relation to it carries no
   recurrence.
3. **The 17 DGS result lists remain references, not evidence** (`sha256: null`,
   never retrieved). Retrieved, they would corroborate seven sitting months and
   would still date no question.
4. **Encoding damage in the archived wording** is preserved as found; family
   labels are sourced from the cleanest available member instead.

### DF. Next project

**QI PHASE 2 — RECURRENCE-DRIVEN PRESENT-DAY QUESTION + ANSWER MODERNISATION.**

Start at `docs/study/qi/qi_phase2_action_queue.json`. The 25 time-relative
families are the sharp end, led by `QIF-EM-0017` — the IMO GHG "ongoing
developments" stem, 13 occurrences across nine years, where the gap between
what recurs and what is currently true is widest.

### DG. Verdict

> **GO** — MIW NOW HAS A GOVERNED, PROVENANCE-AWARE, LIMB-AWARE LONGITUDINAL
> QUESTION-INTELLIGENCE LAYER FROM 2010 THROUGH AUGUST 2026, WITH 3-YEAR,
> 5-YEAR, 10-YEAR AND FULL-HORIZON RECURRENCE SIGNALS, CURRENTNESS TRIAGE AND A
> MACHINE-READABLE PHASE-2 QUEUE; NO PRE-2010 RESOURCES WERE USED, NO PRODUCT
> ANSWERS WERE CHANGED AND THE ACTIVE STUDY SYSTEM REMAINS UNTOUCHED.
