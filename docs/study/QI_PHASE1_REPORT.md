# Question Intelligence — Phase 1

**Governed longitudinal Written QI, January 2010 → August 2026.**
Built 2026-08-23 on the Laptop. Nothing public changed. Nothing Nixon studies changed.

| | |
|---|---|
| Lower boundary | **2010-01** — permanent, Founder decision |
| Upper boundary | **2026-08** — the ceiling of this release |
| Horizon | 200 months. Say *"2010 through August 2026"*, never *"16 years"* |
| Pre-2010 search this session | **none** |
| Pre-2010 data ingested | **0** |
| Pre-2010 backlog created | **0** |
| Public claim changed | **no** — and still barred |
| Study weights changed | **no** |
| Product answers changed | **no** |

Phase 1 asked one question: **what has recurred from 2010 through August 2026?**
It does not ask what the answer should be today. That is Phase 2, and this
report ends by handing it a queue.

---

## 1. What was built

Eight generated projections under `docs/study/qi/`, one deterministic builder,
one gate, one mutation suite. Every file is regenerable; none is hand-editable.

```
governed inputs  +  hand adjudications  +  pinned research ref
                          |
                 tools/study/build_qi.py
                          |
    entities -> occurrences -> families -> joins
             -> coverage -> windows -> currentness -> Phase-2 queue
                          |
                 tools/study/validate_qi.py   (19 invariants)
                 tools/study/test_qi_mutations.py  (14 mutations)
```

**One QI brain.** There is no `historical_qi_final.json`, no `modern_qi_final.json`.
Three evidence bands resolve through one occurrence layer, and each band keeps
its own provenance strength inside it.

---

## 2. The three claims, kept apart

This is the invariant everything else rests on. For any historical record:

| | Claim | 2010–2020 | 2021–2022 | 2023–2026 |
|---|---|---|---|---|
| **A** | the source carries this wording | CORROBORATED | HELD_SOURCE_COPY | GOVERNED_CANONICAL |
| **B** | it belongs to this sitting month | SECONDARY_CLAIMED | PRINTED_ON_SOURCE_COPY | PRINTED_ON_SOURCE_COPY |
| **C** | DGMA officially set it in that sitting | **NOT_ESTABLISHED** | NOT_INDEPENDENTLY_VERIFIED | NOT_INDEPENDENTLY_VERIFIED |

They are never collapsed into `verified = true`. A 2010–2020 record can be
strong on A, weak on B and empty on C simultaneously — which is enough for
internal recurrence and never enough for a public dated claim.

**No occurrence in the entire layer carries `date_certainty: OFFICIAL_DATED`.**
Invariant 18 fails the build if one ever appears without a Founder decision
behind it.

---

## 3. Evidence bands

| Band | Window | Papers / pages | Occurrences | Entities |
|---|---|---|---|---|
| `HISTORICAL_SECONDARY_ARCHIVE` | 2010-01 … 2020-12 | 115 archived pages | **1,026** | 256 |
| `MIW_WORDING_ONLY` | 2021-01 … 2022-12 | 22 held papers | **198** | 198 |
| `MIW_SOLVED_CANONICAL` | 2023-01 … 2026-08 | 40 solved papers | **360** | 360 |
| | | **177 sets** | **1,584** | **814** |

Plus **698 governed limb records** from the printed subparts of solved papers.
They are stored, addressable and **not counted** in any whole-question total.

### The 72-question double count that would have happened

MIW's 2021–2023 wording-only store holds 30 papers. Eight of them — `QP2302`,
`QP2303`, `QP2306`–`QP2311` — are **also** in the solved corpus, under the same
question ids. Emitting both would have counted 72 questions twice and inflated
every 2023 recurrence measure in the model.

The builder suppresses the wording-only copy and records which 72 and why.
Mutation M re-introduces the duplication and the gate catches it.

So the honest figures are: **30 papers / 270 questions held** for 2021–2023, of
which **22 papers / 198 questions** are unique to that band.

### What is evidence, and what only looks like it

Two things corroborate wording and are structurally barred from ever counting
as an occurrence:

- **The DGS/DGMA official Question Bank.** It is undated throughout. It can
  prove a wording is official; it can never date a sitting. Counting a bank
  item would manufacture recurrence out of a catalogue.
- **The publisher's own cross-set recurrence annotation** — carried on both the
  archived 2010–2020 pages and MIW's 2021–2023 copies. It is a claim *about*
  occurrences with no page behind it. The page carrying it evidences only its
  own sitting.

Both are declared `counts_toward_recurrence: false` in `qi_model.py`, and
invariant 11 fails the build if either declaration flips or if a record carrying
one of those source classes appears in the occurrence layer.

---

## 4. Normalisation: what the entity model fixed

The prior research reported **1,873 modern join pairs** and **83 family joins**.
Those are occurrence-level counts, which restate one entity-level decision once
for every sitting the source asserts. Re-derived at entity granularity:

| Reported by research | Actually distinct |
|---|---|
| 1,873 modern join pairs | **285** historical→modern candidate pairs |
| 83 family joins | **37** historical→historical candidate pairs |
| 1,026 occurrences | **256** distinct source entities |

The prior adoption decision predicted 287 and 18. The recomputation here lands
at 285 and 37 — the modern figure confirms that analysis almost exactly; the
historical figure differs because it is measured over a different pairing rule.

### Two defects found in the research occurrence layer

1. **`occurrence_id` is not unique.** Three ids collide — `HOCC-2012-JUN-02`,
   `HOCC-2012-NOV-03`, `HOCC-2017-JUL-06` — because they are built from
   `page_ordinal`, and two distinct entities can be scraped at one index. The
   governed layer keys on `printed_qno` instead and is unique in 1,584 of 1,584.
2. **Encoding damage.** The archived wording carries U+FFFD replacement
   characters from a lossy scrape. Family *labels* are therefore sourced from
   the cleanest available member rather than the anchor; the archived text is
   preserved verbatim and never repaired, because repairing a source is worse
   than showing it damaged.

---

## 5. Family formation — proposed by code, decided by hand

`qi_similarity.py` proposes. It never decides.

The threshold that matters is applied to **containment_low**, not high. A pair
that is 0.95 contained one way and 0.30 the other is not a repeat — it is a
**limb**, and merging on the high side is exactly how a limb's sitting count
gets read as a whole question's.

**1,025 proposals** — 734 merge-strength, 291 relation-strength — closed into
**180 groups**. Every group was read in full. Two audits ran over all of them:

- **Rare-token divergence.** Tokens present in some members and absent from
  others, ranked by corpus document frequency. This is the detector for the one
  failure mode containment cannot see.
- **Chain audit.** The weakest *direct* containment between any two members.
  **Zero** groups scored below 0.60, so no group owes its existence to
  transitivity alone.

### Five splits made against the proposal

| Split | What the algorithm wanted to merge | Why it is wrong |
|---|---|---|
| SPLIT-001 | Hydrogen ↔ Ammonia as a marine fuel | One framing sentence, one different noun. Nitrogen slip and toxicity versus cryogenics and volumetric energy density. |
| SPLIT-002 | EEXI ↔ EEDI design features | Two instruments. EEDI: new builds, 2013. EEXI: existing vessels, 2023. |
| SPLIT-003 | Blockchain ↔ 3D Printing | The examiner's template, not the answer. |
| SPLIT-004 | Charter-survey limb ↔ whole Bill of Lading question | The limb holds **8** occurrences of its own. Merged, those eight sittings would read as eight sittings of the whole question. |
| SPLIT-005 | 2-limb ↔ 4-limb exhaust-emission bundle | The short form requires neither Tier II/III limits nor SCR — half the preparation. |

Three of the five are the *same* failure: an identical framing sentence wrapped
around a different subject. That is now a named, tested detector rather than a
thing someone happened to notice.

The **limb-coverage rule** is written down so the judgement does not drift:
shared limbs as a fraction of the larger limb set, ≥ 0.60 merges as a variant,
below 0.60 splits into two related families. Without a stated fraction this
drifts, and it always drifts toward merging — the direction that inflates.

### Result

| | |
|---|---|
| Governed recurrence families | **270** |
| Entities inside a family | 629 |
| Entities with no recurrence value | 185 |
| Entities in more than one family | **0** |
| Families spanning historical **and** modern bands | **88** |
| Historical entities gaining modern ancestry | 90 |
| Family joins (relations) | **31** — 23 `WHOLE_VS_LIMB_RELATION`, 8 `RELATED_BUT_DISTINCT` |
| Occurrences transferred by any join | **0** |

All 270 families are materially recurrent: ≥ 2 occurrences across ≥ 2 distinct
sittings. None is a single-sitting artefact.

---

## 6. Coverage — 200 months, and what silence means

| Coverage state | Months |
|---|---|
| `SOURCE_PRESENT` | **176** |
| `NO_SOURCE_PAGE_FOUND` | 23 |
| `NO_ARCHIVE_CAPTURE` | 1 — 2010-09, the only pure acquisition gap |
| `NO_EXAM_OFFICIALLY_EVIDENCED` | **0** |

**Not one month is treated as a confirmed zero-question sitting.** That state
requires an official instrument saying no examination was held, and none is
held. Every other absence is UNKNOWN and is excluded from denominators rather
than counted as a zero. Mutation L flips one and the gate catches it.

### A finding worth having

**May is absent in all 17 years of the horizon.** Not one May sitting appears in
any band.

For 2010–2019 that rested on one secondary index's silence, and the prior
adoption decision was right to refuse to promote it. But 2021–2026 is different
evidence entirely: MIW holds its own source copy of every other month and none
for May. Two independent lines now agree, one of them MIW's own.

It is recorded as `CORROBORATED_INFERENCE_NOT_OFFICIAL_EVIDENCE`. The months
stay UNKNOWN. Corroboration is not an official instrument.

### Per year

| Year | Sets | Occurrences | Entities | Absent months |
|---|---|---|---|---|
| 2010 | 10 | 88 | 56 | 2 (May, Sep) |
| 2011–2019 | 11 each | 97–99 each | 47–76 | 1 each (May) |
| 2020 | 6 | 54 | 44 | 6 (Apr–Sep) |
| 2021 | 11 | 99 | 99 | 2 (May, Jun) |
| 2022–2025 | 11 each | 99 each | 99 each | 1 each (May) |
| 2026 | 7 | 63 | 63 | 1 (May), horizon ends Aug |

---

## 7. Recurrence windows

Measured back from the ceiling. Raw counts first; no composite score is stored
in this layer.

| Window | Span | Families with activity |
|---|---|---|
| `RECENT_3Y` | 2023-09 → 2026-08 | **121** |
| `RECENT_5Y` | 2021-09 → 2026-08 | **164** |
| `MEDIUM_10Y` | 2016-09 → 2026-08 | **222** |
| `FULL_HORIZON` | 2010-01 → 2026-08 | **270** |

### Intelligence labels — multidimensional on purpose

| Label | Families |
|---|---|
| `PERSISTENT` | 76 |
| `RECENTLY_ACTIVE` | 121 |
| `DORMANT` | 149 |
| `RE_EMERGING` | 54 |
| `RISING` | 57 |
| `NEW_EMERGING` | 78 |
| `HISTORICAL_ONLY` | 96 |
| `INSUFFICIENT_HISTORY` | 0 |

A family carries every label it earns. `QIF-EM-0002` — the time-charter
influence question — is `PERSISTENT` **and** `RECENTLY_ACTIVE` **and**
`RE_EMERGING` at once: 22 occurrences across 10 years, set continuously
2010–2022, then absent for 45 months, then set again in 2025. Forcing one
mutually exclusive label onto that would throw away everything interesting
about it.

### Re-emergence is about the shape of the return

`RE_EMERGING` keys on the **latest** gap only. Any long-lived family accumulates
a long gap somewhere; that is history, not re-emergence. Re-emergence is
"absent for three years or more, then set again", so the meaningful gap has to
be the one immediately before the most recent sitting.

This was wrong in the first build — it fired on any historical gap and reported
91 families. Corrected, it reports 54.

---

## 8. Currentness — a different question from recurrence

**Currentness never changes a recurrence count.** They come from different
inputs and live in different files. Invariant 14 enforces it.

| Status | Families |
|---|---|
| `CURRENTNESS_REVIEW_REQUIRED` | **25** |
| `CURRENT_WITH_AMENDMENT` | 42 |
| `CURRENT_FRAMEWORK_CHANGED` | 49 |
| `HISTORICAL_ONLY` | 62 |
| `UNKNOWN` | 92 |
| `LIKELY_SUPERSEDED` | 0 — requires research Phase 1 does not do |

`UNKNOWN` is never read as `CURRENT`. It means nobody has checked.

### The time-relative trigger

The instrument-name trigger inherited from the research layer is blind to the
risk that actually bites. A stem asking for *"the ongoing developments at IMO"*
names no convention at all — so nothing about it looks dated, and its correct
answer changes every year regardless.

**25 families** carry time-relative language. Among them `QIF-EM-0017`:

> *"What are the ongoing developments at IMO with respect to the technical and
> operational measures to be invoked on board ships for combating greenhouse gas
> emissions from ships?"*

13 occurrences, 2010-11 through 2024-02, across 9 distinct years. A 2010 answer
and a 2026 answer to that stem describe different regulatory worlds. It ranks
**14th** in the Phase-2 queue and it is the single most currentness-dangerous
item in the corpus.

Invariant 19 recomputes every flag from the stems and fails if one goes missing.
Mutation H strips one and is caught.

---

## 9. Phase-2 action queue

Every one of the 270 families leaves Phase 1 with an action.

| Action | Families |
|---|---|
| `CURRENT_AND_SOLVED` | 72 |
| `EXISTING_CURRENT_ANSWER_VERIFY` | 59 |
| `NEW_MODERN_ANSWER_REQUIRED` | 37 |
| `CURRENTNESS_RESEARCH_REQUIRED` | 8 |
| `HISTORICAL_ANSWER_REQUIRES_MODERNISATION` | 3 |
| `LOW_PRIORITY_HISTORICAL_ONLY` | 91 |
| `SUPERSEDED_MODERN_REPLACEMENT_REQUIRED` | 0 |
| `AMBIGUOUS_FAMILY_REVIEW` | 0 |
| **Total** | **270** |

### Existing MIW answer coverage (read-only)

| Status | Families |
|---|---|
| `HISTORICAL_ONLY` | 96 |
| `SOLVED_BUT_CURRENTNESS_UNVERIFIED` | 62 |
| `MULTIPLE_CANDIDATE_ANSWERS` | 41 |
| `NO_CURRENT_SOLVED_ANSWER` | 40 |
| `SOLVED_CURRENT_CANDIDATE` | 31 |

### Modern canonical question action

| Action | Families |
|---|---|
| `USE_EXISTING_CANONICAL_QUESTION` | 98 |
| `HISTORICAL_ONLY_NO_MODERN_QUESTION` | 91 |
| `MERGE_VARIANTS` | 41 |
| `CREATE_NEW_CURRENT_CANONICAL_QUESTION` | 37 |
| `MODERNISE_CANONICAL_QUESTION` | 3 |
| `SPLIT_LIMB_FAMILY` | 0 |

### Priority model

Recency and current examinability outrank historical bulk, deliberately: a
family that is old, frequent and obsolete must never outrank one that is recent,
recurrent and still set. `HISTORICAL_ONLY` carries a −14 penalty and `DORMANT`
a −5, against +6 per recent-3Y occurrence and +9 for a currentness-review flag.

---

## 10. Top 25 for Founder review

**Internal. Not a public list.**

| # | Family | 3Y | 5Y | 10Y | Full | Yrs | Currentness | Action |
|---|---|---|---|---|---|---|---|---|
| 1 | `QIF-EM-0082` Classification societies in rule formation; annual vs periodical surveys | 4 | 6 | 6 | 6 | 5 | REVIEW_REQUIRED | VERIFY |
| 2 | `QIF-EM-0001` Bunker Oil Pollution Damage Convention 2001 vs CLC 92 | 4 | 7 | 23 | **25** | 10 | UNKNOWN | CURRENT_AND_SOLVED |
| 3 | `QIF-EM-0036` Human Element in STCW; IMO fatigue guidance | **6** | 7 | 9 | 10 | 7 | WITH_AMENDMENT | VERIFY |
| 4 | `QIF-EM-0007` Flag-state casualty investigation; very serious marine casualty | 4 | 5 | 9 | 17 | **13** | WITH_AMENDMENT | VERIFY |
| 5 | `QIF-EM-0012` Unseaworthy vessels under MS Act 1958 | 4 | 5 | 7 | 14 | 9 | WITH_AMENDMENT | VERIFY |
| 6 | `QIF-EM-0038` Entry into force of an IMO convention | 5 | 5 | 10 | 10 | 4 | UNKNOWN | CURRENT_AND_SOLVED |
| 7 | `QIF-EM-0084` General average — essential features | 5 | 6 | 6 | 6 | 4 | UNKNOWN | CURRENT_AND_SOLVED |
| 8 | `QIF-EM-0104` High-efficiency propellers | 3 | 5 | 5 | 5 | 4 | REVIEW_REQUIRED | VERIFY |
| 9 | `QIF-EM-0005` Capital, voyage and operating costs; C/E role | 3 | 4 | 14 | 17 | 10 | UNKNOWN | CURRENT_AND_SOLVED |
| 10 | `QIF-EM-0009` Modern salvage law and general average | 3 | 4 | 13 | 15 | 9 | UNKNOWN | CURRENT_AND_SOLVED |
| 11 | `QIF-EM-0085` IMO Instruments Implementation Code | 4 | 6 | 6 | 6 | 3 | UNKNOWN | CURRENT_AND_SOLVED |
| 12 | `QIF-EM-0076` Rudder efficiency devices | 3 | 7 | 7 | 7 | 4 | UNKNOWN | CURRENT_AND_SOLVED |
| 13 | `QIF-EM-0083` Maritime lien; in rem and in personam | 3 | 6 | 6 | 6 | 4 | UNKNOWN | CURRENT_AND_SOLVED |
| 14 | `QIF-EM-0017` **IMO ongoing developments on GHG** | 2 | 2 | 4 | 13 | 9 | **REVIEW_REQUIRED** | VERIFY |
| 15 | `QIF-EM-0002` Charter influence on machinery operation | 1 | 3 | 13 | **22** | 10 | UNKNOWN | CURRENT_AND_SOLVED |
| 16 | `QIF-EM-0131` Structure of IMO; amendment procedures | 4 | 4 | 4 | 4 | 3 | UNKNOWN | CURRENT_AND_SOLVED |
| 17 | `QIF-EM-0132` Disease vectors; WHO; ship health certificates | 4 | 4 | 4 | 4 | 2 | UNKNOWN | CURRENT_AND_SOLVED |
| 18 | `QIF-EM-0129` HNS Convention | 2 | 4 | 4 | 4 | 3 | **REVIEW_REQUIRED** | VERIFY |
| 19 | `QIF-EM-0013` Communication; barriers; decarbonisation hazard | 2 | 3 | 13 | 13 | 6 | WITH_AMENDMENT | VERIFY |
| 20 | `QIF-EM-0006` P&I clubs — funding and cover | 1 | 3 | 10 | 17 | 11 | UNKNOWN | CURRENT_AND_SOLVED |
| 21 | `QIF-EM-0128` Maritime cyber risk management | 3 | 4 | 4 | 4 | 3 | WITH_AMENDMENT | VERIFY |
| 22 | `QIF-EM-0130` Hull-form optimisation | 3 | 4 | 4 | 4 | 3 | UNKNOWN | CURRENT_AND_SOLVED |
| 23 | `QIF-EM-0116` Lakshadweep / A&N islands; PSSA | 3 | 3 | 4 | 4 | 4 | UNKNOWN | CURRENT_AND_SOLVED |
| 24 | `QIF-EM-0023` UNCLOS flag-state registration and control | 1 | 3 | 11 | 11 | 6 | WITH_AMENDMENT | VERIFY |
| 25 | `QIF-EM-0031` Modern turbocharging methods | 1 | 1 | 4 | 11 | 6 | **REVIEW_REQUIRED** | VERIFY |

**Where the risk is.** Four kinds of item are on this list:

- **Live, solved, low risk** (2, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 20, 22, 23)
  — recurrence is real and the answer is stable. Phase 2 verifies, it does not rewrite.
- **Live and framework-moved** (3, 4, 5, 19, 21, 24) — still set recently, and the
  instrument behind the answer has been amended inside the horizon.
- **Time-relative stems** (1, 8, 14, 18, 25) — the dangerous class. #14 asks for
  "ongoing developments" on GHG and #18 says the HNS Convention "is expected
  shortly to come into force", a sentence that has been printed unchanged for
  years. Their answers rot silently.
- **Deep but quiet** (15, 20) — 22 and 17 occurrences, one recent sitting each.
  High historical weight, and the priority model deliberately does not let that
  alone carry them higher.

---

## 11. Study system — preview only

`docs/study/qi/qi_study_preview.json`. Computed, not applied.

| | Current | QI-informed preview |
|---|---|---|
| Order | D03 > D01 > D02 > D05 > D04 > D07 > D06 > D09 > D10 > D08 | D03 > D01 > D02 > D05 > **D07 > D04** > **D09 > D06** > D10 > D08 |

Only one of six priority components changes — `written_recurrence`, weight 0.13 —
so the delta isolates governed recurrence and nothing else.

**The active front does not move.** D03, D01 and D02 hold ranks 1–3 in both
orders. Two adjacent pairs swap at ranks 5–6 and 7–8. `D01 → D03 → D02` stands
untouched.

Score deltas are small and mostly negative, because the governed layer gives
*every* domain more families and renormalisation compresses the spread:

| Domain | Families now | Families under QI | Δ score | Rank |
|---|---|---|---|---|
| D03 Human Element | 9 | 27 | +0.0105 | 1 → 1 |
| D01 Statutory & Class | 16 | 42 | 0.0000 | 2 → 2 |
| D02 Commercial Law | 12 | 29 | −0.0077 | 3 → 3 |
| D05 GHG & Fuels | 10 | 19 | −0.0225 | 4 → 4 |
| D07 Cargo | 4 | 4 | −0.0201 | 6 → 5 |
| D04 MARPOL | 10 | 14 | −0.0380 | 5 → 6 |
| D09 Machinery | 0 | 0 | 0.0000 | 8 → 7 |
| D06 Indian Law | 5 | 7 | −0.0189 | 7 → 8 |

**136 families reach no topic**, and that number splits into two very different
things:

- **96** are `HISTORICAL_ONLY_NO_MODERN_MEMBER` — they live only in 2010–2020
  and the taxonomy has never had a modern question to map.
- **40** are `MODERN_MEMBER_IS_WORDING_ONLY_BAND` — alive in 2021–2022, but the
  taxonomy maps oral questions and the 360 solved written questions only, and
  has never been asked to map the wording-only band.

Reported as one number the Phase-2 backlog would be badly overstated.

No study weight, session file, cohort or progress record was modified. The
preview tool asserts this itself and fails if it ever touches one.

---

## 12. Public claim policy — unchanged, and still barred

No public surface changed. No marketing changed.

**"Official DGMA questions since 2010" remains NOT PERMITTED**, and this build
does not move it one inch closer. 1,026 of 1,584 occurrences carry
`SECONDARY_CLAIMED` dates and no official document dates any 2010–2020 sitting.
More coverage cannot fix that, because coverage is not the missing thing.

Internal QI may use the secondary-claimed sittings. Being wrong about a month
costs an internal model a study-priority nudge; being wrong in public costs the
corpus its credibility. The two thresholds are different on purpose and are
enforced separately in code.

---

## 13. Validation

**19 invariants**, all holding:

| | |
|---|---|
| 01 | no governed pre-2010 occurrence |
| 02 | source entity ids unique |
| 03 | occurrence ids unique |
| 04 | one entity not double-counted in a sitting |
| 05 | one occurrence counted once per family, and owned by one family |
| 06 | limb recurrence is not whole-question recurrence |
| 07 | family ids unique |
| 08 | every join resolves to real governed objects |
| 09 | provenance populated |
| 10 | date confidence populated from the closed vocabulary |
| 11 | question-bank and host annotation are not occurrences |
| 12 | modern canonical questions not duplicated across bands |
| 13 | window counts derive from the occurrence layer |
| 14 | currentness does not move a recurrence count |
| 15 | every family reaches the Phase-2 queue with a known action |
| 16 | no occurrence after 2026-08 |
| 17 | silence is not a confirmed zero |
| 18 | the public dated claim stays barred |
| 19 | time-relative stems keep their flag |

**14 mutations, 14 caught, 0 escaped, 0 residue.**

```
A pre-2010 occurrence            -> INV01     H currentness flag stripped   -> INV19
B duplicated source entity       -> INV02     I risky family dropped        -> INV15
C occurrence counted twice       -> INV05     J occurrence after ceiling    -> INV16
D limb promoted to whole         -> INV06     K count hand-edited           -> INV13
E question bank as occurrence    -> INV11     L silence counted as zero     -> INV17
F secondary date -> official     -> INV18     M modern question duplicated  -> INV12
G broken family join             -> INV08     N entity twice in one sitting -> INV04
```

The builder also fails closed on its own inputs: a changed proposal set breaks
the pinned adjudication digest, and a recorded split that matches no entity
stops the build rather than shipping an unreviewed family. Both verified.

Existing suites re-run unchanged: **1,187 assertions pass**
(`test_mapping_engine` 132, `test_study_expandability` 339,
`test_historical_qi_inventory` 19, `test_roadmap_cockpit` 18,
`test_d01_priority_cohort` 19, `validate_study_spine` 660).

---

## 14. What Phase 1 did not settle

Non-blocking. None of these can move a material recurrence result.

1. **272 occurrences carry `REQUIRES_LIMB_ADJUDICATION`** — 171 in the archived
   2010–2020 band and 101 in the 2021–2022 held-copy band. Limb markers were
   detected lexically and never semantically adjudicated. They are recorded as
   whole-question occurrences with their markers preserved, and **no limb family
   is built on any of them**, so none inflates anything. Semantic limb
   adjudication of these two bands is Phase-2 work if it is ever wanted. Only
   the solved band carries `GOVERNED_LIMB` records, and those are not counted.
2. **291 relation-strength pairs where one side has no family** are not recorded
   as joins, because a single-occurrence entity is not a family and a relation
   to it carries no recurrence.
3. **The 17 DGS result lists remain references, not evidence** — `sha256: null`,
   never retrieved. Retrieved, they would corroborate seven sitting months and
   would still date no question. Unchanged from the prior adoption decision.
4. **Encoding damage in the archived wording** is preserved as found.

---

## 15. Files

| Path | Role |
|---|---|
| `tools/study/qi_model.py` | Vocabulary, identity, horizon guards |
| `tools/study/qi_similarity.py` | Candidate generation. Proposes only |
| `tools/study/qi_phase1_adjudications.json` | **Hand-maintained.** The semantic decisions |
| `tools/study/build_qi.py` | The only writer of the QI projections |
| `tools/study/validate_qi.py` | The gate. Fails closed |
| `tools/study/test_qi_mutations.py` | 14 mutations |
| `tools/study/preview_qi_study_impact.py` | Read-only study preview |
| `docs/study/qi/qi_source_entities.json` | 814 entities |
| `docs/study/qi/qi_occurrences.json` | 1,584 counted + 698 limb records |
| `docs/study/qi/qi_families.json` | 270 families |
| `docs/study/qi/qi_family_joins.json` | 31 relations, 0 occurrence transfers |
| `docs/study/qi/qi_coverage_matrix.json` | 200 months |
| `docs/study/qi/qi_time_window_metrics.json` | 3Y / 5Y / 10Y / full horizon |
| `docs/study/qi/qi_currentness.json` | Triage only |
| `docs/study/qi/qi_phase2_action_queue.json` | 270 rows |
| `docs/study/qi/qi_study_preview.json` | Preview, not applied |

`tools/` and `docs/` are both deploy-excluded. This build deploys nothing.

---

## 16. Phase 2

**Recurrence-driven present-day question and answer modernisation.**

Phase 1 answered *what kept coming back*. Phase 2 asks: *if it comes back
tomorrow, what should the candidate answer under today's framework?*

Start at the top of the queue and at the 25 time-relative and framework-moved
families in particular. `QIF-EM-0017` — the GHG "ongoing developments" stem, 13
occurrences across 9 years — is where the gap between what recurs and what is
currently true is widest.
