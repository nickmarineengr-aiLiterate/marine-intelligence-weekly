# MEO Class I — study roadmap

Built 2026-08-22 from main `906e8a4`. Generated evidence:
`study_spine.json`, `study_mappings.json`, `mapping_review_queue.json`.

> **MIW-DERIVED, not official.** No DGMA syllabus instrument exists in this
> repository — see `SYLLABUS_SOURCE_STATUS.md`. The spine is built from what
> MIW's own corpora prove is examined: 721 oral questions and 360 solved
> written questions across 40 papers.

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
| Oral question breadth | 0.30 |
| Examiner evidence | 0.25 |
| Written question load | 0.20 |
| Written recurrence families | 0.15 |
| Foundation (domains depending on it) | 0.10 |

Each component is min-max normalised against the strongest domain. **The
score is an input, not the decision** — study *order* also honours
prerequisites and topic continuity, which is why Topic 01 is the 3rd-ranked
domain (see below).

## The domains

| # | ID | Domain | Oral | Written | Papers | Examiner Qs | Score | Prereqs |
|---|---|---|---|---|---|---|---|---|
| 1 | D03 | Human Element, ISM & Management | 210 | 69 | 38 | 190 | 0.778 | D01 |
| 2 | D02 | Marine Insurance & Commercial Law | 134 | 70 | 38 | 127 | 0.629 | D01 |
| 3 | D01 | Statutory Framework, Survey & Classification | 46 | 96 | 39 | 39 | 0.567 | — |
| 4 | D05 | Alternative Fuels, GHG & Decarbonisation | 60 | 50 | 35 | 55 | 0.356 | D01, D04 |
| 5 | D04 | Pollution Prevention & Response | 60 | 43 | 28 | 51 | 0.349 | D01 |
| 6 | D07 | Cargo Operations & Bulk Carriage | 98 | 13 | 11 | 94 | 0.328 | D01 |
| 7 | D06 | Indian Maritime Legislation | 0 | 19 | 15 | 0 | 0.086 | D01, D02 |
| 8 | D08 | Fire Safety, LSA & FSS | 27 | 0 | 0 | 22 | 0.068 | D01 |
| 9 | D10 | Ship Construction, Stability & Naval Architecture | 26 | 0 | 0 | 22 | 0.066 | — |
| 10 | D09 | Machinery, Electrical & Automation | 21 | 0 | 0 | 17 | 0.052 | D01 |

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
6. **D07 — Cargo Operations & Bulk Carriage** — 98 oral, only 13 written.
7. **D08 — Fire Safety, LSA & FSS** — oral-only; pairs naturally with D07.
8. **D10 — Ship Construction, Stability & Naval Architecture** — oral-only.
9. **D09 — Machinery, Electrical & Automation** — oral-only.
10. **D06 — Indian Maritime Legislation** — 19 written questions; small, and
    best late because it leans on D01 and D02. **Note the mapping gap below.**

## Known limitations — read before trusting a number

1. **D06 shows 0 oral questions.** Indian-law orals exist (e.g.
   `QB1_I#q2` ship registration in India, `QB4_E#q13`), but they live inside
   files assigned to other domains, and the mapper assigns one PRIMARY topic
   per question. `SECONDARY` / `CROSS_TOPIC` roles are defined in the schema
   but not yet populated. **D06's oral coverage is understated, not absent.**
2. **39 oral questions are `ACCIDENTALLY_UNMAPPED`** and sit in the review
   queue. Mostly candidate-experience questions ("Any incident on your ship",
   "Describe your last vessel") that legitimately belong to no domain — most
   should probably be reclassified `INTENTIONALLY_UNMAPPED` after review.
3. **82 mappings are `REVIEW_PENDING`** — cue-derived and not individually
   adjudicated. They are excluded from `VALID_MAPPED` topic views by default.
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
