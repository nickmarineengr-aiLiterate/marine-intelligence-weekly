# MEO Class I — study roadmap

Built 2026-08-22 from main `906e8a4`. Generated evidence:
`study_spine.json`, `study_mappings.json`, `mapping_review_queue.json`.

> **Grounded in the official syllabus.** DGMA EAC Branch Circular **No.49 of
> 2026** (15-Aug-2026), **Annexure III** — the MEO Class I preparatory course
> syllabus, 25 items — has been obtained from the issuer, read and ingested.
> See `SYLLABUS_SOURCE_STATUS.md`.
>
> The official layer states **scope**. The topic spine below remains
> MIW-derived and is the durable **study/join** layer, built from what MIW's
> own corpora prove is examined: 721 oral questions and 360 solved written
> questions across 40 papers. The two are crosswalked, not merged, and MIW
> headings are **not** DGMA headings.
>
> **Adopted, not yet in force.** The revised syllabus takes effect on
> **2027-01-01**. Nothing here presents it as governing a 2026 sitting.

## Source-of-truth chain

```
meoclass1/qb_content_index.json   (721 oral, canonical id = file#anchor)
meoclass1/pastpapers/specs/*.json (360 written, canonical id = PAPER-Qn)
        |
        v   tools/study/mapping_engine.py   (ONE mapper, two adapters)
        |   + tools/study/adjudications.json (human review stamps)
        v
docs/study/study_mappings.json    <- governed mapping records
docs/study/mapping_review_queue.json
        |
        v   tools/study/build_study_spine.py
        v
docs/study/study_spine.json       <- per-domain intelligence
        |
        v
docs/study/TOPIC_nn_*.md          <- candidate-facing study packs
```

`tools/pastpapers/topic_taxonomy.py` remains the owner of the **Written**
study-topic projection that the Solved QP product depends on. This layer does
not reclassify it; it adopts it and adds the Oral join that never existed.
There is no second taxonomy.

## Priority model

Transparent and additive — no opaque score. Weights in
`tools/study/study_spine.py`:

| Component | Weight |
|---|---|
| Oral question breadth | 0.26 |
| Examiner evidence | 0.22 |
| Written question load | 0.17 |
| Written recurrence families | 0.13 |
| Official scope (PRIMARY Annexure III items owned) | 0.13 |
| Foundation (domains depending on it) | 0.09 |

Each component is min-max normalised against the strongest domain. **The
score is an input, not the decision** — study *order* also honours
prerequisites and topic continuity, which is why Topic 01 is the 2nd-ranked
domain (see below).

`official_scope` was added once the circular was ingested; the five original
weights were scaled down proportionally rather than re-tuned. It moved D01
from 3rd to 2nd, because owning six PRIMARY official items is a priority
signal that corpus counts alone cannot see.

## The domains

| # | ID | Domain | Oral | Written | Papers | Examiner Qs | Official items | Score | Prereqs |
|---|---|---|---|---|---|---|---|---|---|
| 1 | D03 | Human Element, ISM & Management | 210 | 69 | 38 | 190 | 8 (+3) | 0.8053 | D01 |
| 2 | D01 | Statutory Framework, Survey & Classification | 46 | 96 | 39 | 39 | 6 (+5) | 0.5897 | — |
| 3 | D02 | Marine Insurance & Commercial Law | 134 | 70 | 38 | 127 | 2 | 0.5782 | D01 |
| 4 | D05 | Alternative Fuels, GHG & Decarbonisation | 60 | 50 | 35 | 55 | 2 (+1) | 0.3403 | D01, D04 |
| 5 | D04 | Pollution Prevention & Response | 60 | 43 | 28 | 51 | 1 (+3) | 0.3183 | D01 |
| 6 | D07 | Cargo Operations & Bulk Carriage | 98 | 13 | 11 | 94 | 0 | 0.2856 | D01 |
| 7 | D06 | Indian Maritime Legislation | 0 | 19 | 15 | 0 | 2 | 0.1067 | D01, D02 |
| 8 | D09 | Machinery, Electrical & Automation | 21 | 0 | 0 | 17 | 3 (+4) | 0.0945 | D01 |
| 9 | D10 | Ship Construction, Stability & Naval Architecture | 26 | 0 | 0 | 22 | 1 (+1) | 0.074 | — |
| 10 | D08 | Fire Safety, LSA & FSS | 27 | 0 | 0 | 22 | 0 (+1) | 0.0589 | D01 |

## The ten domains reviewed against Annexure III

Every domain was re-examined against the official syllabus. A domain was
**not** kept merely because code already referenced it, and **not** dropped
merely because DGMA uses a different heading.

| ID | Verdict | Reasoning |
|---|---|---|
| D01 Statutory & Class | `SUPPORTED_BY_OFFICIAL_SCOPE` | Owns items 3, 6, 7, 9, 10, 24. The largest official footprint after D03. |
| D02 Insurance & Commercial | `SUPPORTED_BY_OFFICIAL_SCOPE` | Item 11 is D02 almost verbatim; item 19 (budgeting) adjudicated to it. |
| D03 Human Element & ISM | `SUPPORTED_BY_OFFICIAL_SCOPE` | Owns 8 items (2, 8, 12–17). The syllabus is management-heavy at Class I. |
| D04 Pollution Prevention | `SUPPORTED_BY_OFFICIAL_SCOPE` | Owns item 25 outright; supports 6, 17, 22 through MARPOL. |
| D05 GHG & Alternative Fuels | `SUPPORTED_BY_OFFICIAL_SCOPE` | Items 18 and 22; also the alternative-fuel limb of 21. |
| D06 Indian Maritime Legislation | `SUPPORTED_BY_OFFICIAL_SCOPE` | Items 1 and 5. Strengthened by the final circular, which names the Merchant Shipping Act **2025** and the Registration of Indian Ships Rules **2026**. |
| **D07 Cargo & Bulk Carriage** | **`MIW_CROSS_CUTTING_DOMAIN`** | **Zero Annexure III edges of any role.** Verified, not assumed: "cargo" appears in Annexure III only incidentally — as a P&I cover type (item 11), a voyage cost line (19) and a blockchain example (23) — never as a subject. It is a Class **II** subject (Annexure II). **Kept anyway**: 98 oral questions and 94 examiner-evidenced questions prove examiners ask it at Class I orals regardless. Dropping it because DGMA files it elsewhere would fail the candidate. |
| D08 Fire Safety, LSA & FSS | `SUPPORTED_BY_OFFICIAL_SCOPE` (supporting only) | No PRIMARY item, but a real supporting edge to item 12 (emergency systems, fire main, drainage). Recorded as `SUPPORTING_ONLY`, deliberately **not** as orphaned. |
| D09 Machinery, Electrical & Automation | `SUPPORTED_BY_OFFICIAL_SCOPE` | Owns items 20, 21, 23 — and gains scope in the final circular (dual-fuel, sensor technology, cyber-risk). |
| D10 Construction, Stability & NA | `SUPPORTED_BY_OFFICIAL_SCOPE` | Item 4 (stability, 2008 IS Code); supports item 25 (hull form for noise). |

**No domain needed a split, a merge, or was found misaligned.** The
ten-domain model survives contact with the official syllabus intact — which
is the strongest available evidence that it was derived from the same
examinable reality the circular describes.

### What the official layer adds that the corpus did not have

- **D07 is now visibly out-of-syllabus-scope but in-examination-scope.** That
  tension was invisible before and is worth knowing when budgeting time.
- **Two subjects are newly examinable and barely covered:** casualty
  investigation (item 24, well covered) and **underwater noise** (item 25,
  1 written question, 0 oral). Item 25 did not exist in the July draft.
- **Classification societies' duty of care** (added to item 3) has **zero**
  corpus coverage. See `TOPIC_01` note **N6**.

## The 01-Jan-2027 transition

Question identity never changes across the transition. `canonical_question_id`
is stable; only the alignment fields move.

| State | Meaning |
|---|---|
| `CROSSWALK_ALIGNED` | 904 mappings — topic has PRIMARY official item(s) |
| `SUPPORTING_ONLY` | 27 mappings (all D08) — official home, secondary role |
| `ORPHANED_IN_ADOPTED_SYLLABUS` | 111 mappings (all D07) — no official edge |
| `UNRESOLVED` | 39 mappings — the pre-existing unmapped oral set |

On 2027-01-01 `MIW-DERIVED-1.0` stops being the operative version and
`DGMA-C49-2026-ANNEX3` starts. Because both versions are already carried on
every record, that is a status flip, not a re-derivation.

## Study order (dependency- and continuity-optimised)

Deliberately **not** the score order. Minimises topic switching and forward
references.

1. **D01 — Statutory Framework, Survey & Classification** ← **TOPIC 01**
   Prerequisite of 8 of 9 domains; on 39 of 40 written papers. Everything
   else is enforced through its certificates, surveys and class machinery.
   → `TOPIC_01_STATUTORY_SURVEYS_AND_CLASS.md`
2. **D03 — Human Element, ISM & Management**
   Largest domain by volume (210 oral). Reads far cheaper once D01's audit,
   certification and RO vocabulary is in place. Natural continuity: ISM is
   the management limb of the same statutory regime.
3. **D02 — Marine Insurance & Commercial Law**
   Second-largest, self-contained, no dependants — a clean block. Its
   liability arguments assume the ship's statutory/class status from D01.
4. **D04 — Pollution Prevention & Response**
   MARPOL, sitting on D01's certification regime (IOPP/IAPP).
5. **D05 — Alternative Fuels, GHG & Decarbonisation**
   Straight after D04 (shares Annex VI). Placed late deliberately: the most
   currentness-sensitive domain, so studying it near the exam wastes least.
6. **D07 — Cargo Operations & Bulk Carriage** — 95 oral, only 13 written.
7. **D08 — Fire Safety, LSA & FSS** — oral-only; pairs naturally with D07.
8. **D10 — Ship Construction, Stability & Naval Architecture** — oral-only.
9. **D09 — Machinery, Electrical & Automation** — oral-only.
10. **D06 — Indian Maritime Legislation** — 19 written questions; small, and
    best late because it leans on D01 and D02. **Note the mapping gap below.**

## Known limitations — read before trusting a number

1. **D06 shows 2 oral questions.** It was 1 until 2026-08-23, when
   `QB4_E#q13` (ship registration in India) was adjudicated out of D03 into
   D06 — the first time an Indian-law oral was moved there deliberately.
   Others still exist inside files assigned to other domains (e.g.
   `QB1_I#q2`), and the mapper assigns one PRIMARY topic per question;
   `SECONDARY` / `CROSS_TOPIC` roles are defined in the schema but not yet
   populated. **D06's oral coverage remains understated, not absent.**

   The detector cannot help here: `QUESTION_CUES` in `study_spine.py` has
   **no D06 pattern at all**, so a contradiction on an Indian-law question can
   only ever propose D01. `QB4_E#q13` was flagged D01 and reassigned to D06 by
   hand. Adding a D06 cue is a deliberate engine change and is **not** being
   made to shrink the queue; it is recorded here as a known blind spot.
2. **39 oral questions are `ACCIDENTALLY_UNMAPPED`** and sit in the review
   queue. Mostly candidate-experience questions ("Any incident on your ship",
   "Describe your last vessel") that legitimately belong to no domain — most
   should probably be reclassified `INTENTIONALLY_UNMAPPED` after review.
3. **121 mappings are `REVIEW_PENDING`** — cue-derived or human-held, and in
   either case not settled. They are excluded from `VALID_MAPPED` topic views
   by default. The figure rises as well as falls: the two 2026-08-23
   contradiction tranches *demoted* file-title mappings they did not settle,
   which is the intended behaviour — a contradicted mapping keeps its topic as
   a placeholder but loses the claim to being settled.
4. **Written recurrence uses exact `short_title` matching**, which splits
   families whose titles were worded slightly differently (the III Code
   family reports 3 + 2 instead of 5) and misses thematic families whose
   titles all differ (the 8 PSC questions all count as singletons). Recurrence
   counts are therefore a **floor**, not a total.
5. **Examiner relationship totals** here derive from
   `CURRENT_EXAMINER_RELATIONSHIPS.jsonl`: 862 relationships, 6 examiners,
   651 of 721 questions with evidence. A session brief quoted "960 / 7";
   that figure is not reproducible from this file and was not adopted.
6. **Some QB file `tags` are corrupt** — `QB2_B`, `QB9_E`, `QB9_F`, `QB6_F`,
   `QB3_H`, `QB4_I`, `QB2_H`, `QB10_A` carry junk tokens (`&`,
   `**SECTION:**`, bare numbers). Not used by this layer, which reads titles
   and text — but it is a real defect in the oral index.

## Deferred, untouched this session

Oral F2 and the remaining 32 follow-ups · master XLSX · the 788-occurrence
audit · any oral or written **answer** content · public/deployed surfaces.
