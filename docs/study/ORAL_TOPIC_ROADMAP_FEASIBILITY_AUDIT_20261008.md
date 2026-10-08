> **Provenance (added on repository adoption, 2026-10-08).** Findings below are
> unchanged from the reviewed audit file
> `J:\AI-Sandbox\MIW\ORAL-Topic-Roadmap-Audit\ORAL_TOPIC_ROADMAP_FEASIBILITY_AUDIT_20261008.md`
> (sha256 `8a3342950a3ec170a09505103caa5168e2794052c5a207a3095eb41b1844d491`). The audit read `origin/main` `6ce00b5`; this
> copy enters the repository in the Phase 0/1 candidate based on `8083e59`
> (Notes Part 26 only in between). Founder decisions FD-ROADMAP-1..7 and the
> Phase 0/1 outcome are in `ORAL_TOPIC_ROADMAP_PHASE01_IMPLEMENTATION_20261008.md`.

# ORAL Q&A TOPIC ROADMAP — FEASIBILITY AUDIT (2026-10-08)

**Status:** AUDIT ONLY — no implementation, no canonical content touched, no gate changed, nothing published.
**Lane:** MIW MEO Class I Oral Q&A / Oral Release (read-only use).
**Audited state:** `nickmarineengr-aiLiterate/marine-intelligence-weekly` — `origin/main` **`6ce00b5b8f4b74ae2a9f543959b128cfede3573d`** (2026-10-08 02:25 IST, "Add Engineering Management Notes Part 25"), extracted read-only via `git archive` to `J:\AI-Sandbox\MIW\ORAL-Topic-Roadmap-Audit\snapshot\`.

> **Why not the local checkout.** The local working tree at
> `J:\Projects\Marine-Intelligence-Weekly\reconciliation-candidate-2026-09-19\marine-intelligence-weekly`
> sits on branch `audit/india-oilspill-regulatory-cleanup-20260917` at HEAD
> `b911dd3cc901fe065e60ab94ac318936acc0486a` — the `sim <sim@sim>` "TEST SIMULATION approvals
> (scratch clone only)" commit that the project-status record classifies **QUARANTINED / NO
> AUTHORITY**. It is 22 commits behind `origin/main`; working tree has one untracked file
> (`reports/audit/RAZORPAY_SSL_ROTATION_AUDIT_20261005.md`). This audit therefore reads the
> governed `origin/main`, not the quarantined HEAD. The checkout was not modified (only
> `git fetch origin main` was run).

**Documentation location.** `docs/oral/` does **not** exist on `origin/main` and was not created.
The governed home for study-architecture documents is **`docs/study/`** (STUDY_ROADMAP.md,
SYLLABUS_SOURCE_STATUS.md, TOPIC_0n packs, QI reports). Proposed repository path, for a later
authorised commit: **`docs/study/ORAL_TOPIC_ROADMAP_FEASIBILITY_AUDIT_20261008.md`**. This copy
lives in the sandbox per the workstream-hygiene rule.

Note: `docs/study/SYLLABUS_INTEGRATION_STATE.md`, named in the brief, **does not exist**; the
nearest equivalent is `docs/study/SYLLABUS_SOURCE_STATUS.md`.

---

## 1. Executive verdict

### **FEASIBLE — EXISTING SPINE + BOUNDED ORAL SUBTOPIC LAYER**

* The D01–D10 spine already carries the Oral corpus: **719 of 761** canonical Oral questions
  hold a governed D-topic, and a generated, gated **Oral-by-topic page already exists**
  (`meoclass1/topics.html`, built by `tools/study/build_topic_pages.py`, protected by release
  gate `study_pages_check`). Option A is, in substance, **already shipped**.
* What does not exist is what makes it a *roadmap*: a within-topic structure and a learning
  order. `subtopic_id` is a declared schema slot in every mapping record and is **null on all
  1,121 records**; within a topic, `topics.html` lists questions in **lexicographic id order**
  (`QB1_B#q16` before `QB1_B#q5`). No existing Oral metadata can generate a pedagogical order.
* No new taxonomy is needed. A **bounded subordinate subtopic layer** under D01–D10 is
  needed for the three large domains (D03 203, D02 116, D07 104 questions), and its vocabulary
  should be **reused** from the governed Written study-topic leaves (`topic_taxonomy.py`,
  75 leaves) and the Annexure III crosswalk — not invented.
* Two genuine curation debts gate a full Option B: (a) the open mapping queue (**42
  unmapped + 66 review-pending = 108**, of which D10 alone has 26 of 33 pending), and (b)
  **editorial adjudication** of subtopic + sequence position per question (proposals can be
  machine-cued, decisions cannot).

---

## 2. Current architecture — exact source-of-truth chain (as on `6ce00b5`)

```
CANONICAL (hand-authored, governed)
  meoclass1/QB*.html (86 files)                       Oral cards; identity = file#anchor
  meoclass1/pastpapers/specs/QPyymm.json (41 papers)  Written; identity = PAPER-Qn
  docs/study/official_syllabus.json (25 nodes)        ingested verbatim, DGMA C49/2026 Annex III
  docs/study/official_crosswalk.json (43 edges)       hand-adjudicated D-topic -> node
  tools/study/study_spine.py                          D01–D10 registry, weights, prerequisites
  tools/study/adjudications.json                      human mapping stamps
  examiner-audit/EXAMINER_ALIAS_REGISTER.json         examiner identity (7)
  tools/oral/oral_followup_register.json              35 typed follow-up actions
  docs/study/study_sessions.json, study_progress.json, TOPIC_0n_*.md   hand study plans
        |
DERIVED INDEXES
  meoclass1/qb_content_index.json  (build_qb_content_index.py)        761 Q / 86 files
  examiner-audit/CURRENT_EXAMINER_RELATIONSHIPS.jsonl                  860 rels / 649 Q
  examiner-audit/EXAMINER_INDEX_SNAPSHOT.json -> examiner-index.html   958 pairs / 671 Q
  examiner-audit/ORAL_NOTES_UNITS.jsonl / ORAL_NOTES_COVERAGE.jsonl    992 note units
  examiner-audit/AUGUST2026_INTAKE_*                                   283 recent occurrences
        |
        v  tools/study/mapping_engine.py (ONE mapper, ORAL + WRITTEN adapters)
  docs/study/study_mappings.json (1,121) + mapping_review_queue.json (108)
        |
        v  build_study_spine.py / build_coverage_matrix.py / build_syllabus_gap_register.py
  docs/study/study_spine.json, coverage_matrix.json, syllabus_gap_register.json
        |
        v  export_roadmap_xlsx.py / build_topic_pages.py / build_public_study_roadmap.py
  MIW_MEO_Class1_Study_Roadmap.xlsx | meoclass1/study.html | meoclass1/topics.html (gated)
  | SQ/study-roadmap.html (public whitelist)
```

`docs/study/STUDY_ROADMAP.md` is formally **DEPRECATED (2026-08-23)** — its prose numbers
(721) are history, not state.

---

## 3. Written roadmap model (what to reuse)

| Aspect | How the Written side works | Reuse for Oral? |
|---|---|---|
| A. Source | Paper specs carry governed `primary_category`, `subject_tags`, `recurrence_class`, `model_answer` | Oral cards carry **no** governed subject field — the gap |
| B. Hierarchy | `topic_taxonomy.py`: 7 categories -> alias-normalised `subject_tags` -> **75 study-topic leaves** (threshold ≥3 Q, "Other" bucket). Spine adopts categories as D01–D07 verbatim | **Reuse the 75-leaf vocabulary** as candidate Oral subtopics for D01–D07 |
| C. Recurrence | L1 calendar tag (`recurrence_model.py`), internal six-year EXACT/NEAR, **270 canonical QI families** (`docs/study/qi/qi_families.json`), audience-split `safe_qi_projection.json` (558 Q, **0 Oral**) | Reuse the *pattern* (family ↔ members ↔ occurrences; PUBLIC/GATED/INTERNAL field split), not the Written engine |
| D. Order | Transparent additive priority (`study_spine.py:271-278`: oral .26, examiner .22, written .17, recurrence .13, official .13, foundation .09), min-max scaled; study order = prerequisite-respecting greedy over score | Already Oral-aware at domain level (48% of weight is Oral). No within-topic order exists on either side |
| E. Syllabus | category -> D-topic -> crosswalk -> node; `evidence_granularity` NODE/TOPIC/AMBIGUOUS | Identical join already applies to Oral |
| F. Navigation | `solvedQP/topics.html` -> `?topic=&domain=` -> `QPxxxx.html#…`; every QP page links back to topics | Oral has forward links only; **no back-link** from any QB card |
| G. Update | `tools/pastpapers/run_toolchain.py` runs **no** study step; study layer rebuilt by hand | Same weakness applies — see §11 |
| H. Governance | `generated_by` / `hand_editable:false` on every derived file; `--check` on every builder; `validate_study_spine.py` (~200 R-rules) | Reuse as-is |

**Observed drift (Written):** QP2609 (spec updated 2026-09-23, 9 questions) has **no record
in `study_mappings.json`**; the spine still says "40 papers / 360 written". `build_study_spine.py`
reads `store['mappings'][qid]` with no fallback, so a rebuild fails until mappings are rerun.
Not an Oral defect, but it proves the update chain is manual.

**WRITTEN ROADMAP ARCHITECTURE (compact)**
```
specs (canonical) -> topic_taxonomy (7 x 75 leaves, product view)
                  -> mapping_engine GOVERNED_FIELD -> study_mappings -> study_spine
recurrence: qi_families (270) -> study_qi_adapter -> one weight per topic
candidate:  solvedQP/topics.html <-> QP pages (gated SOLVED_QP); public SQ projection
```

---

## 4. Oral corpus audit

### 4.1 Counts (all derived from files at `6ce00b5`)

| Measure | Value | Source |
|---|---|---|
| Canonical Oral questions | **761** | `qb_content_index.json total_questions`; independently = 761 `id="qN"` anchors in the 86 QB HTML files (0 mismatches) |
| Question-bearing files | **86** (+ cheatsheets, not question-bearing) | same |
| Oral mapping records | **761** (1:1 with index, 0 orphans either way) | `study_mappings.json` |
| — VALID_MAPPED / REVIEW_PENDING / ACCIDENTALLY_UNMAPPED | 653 / 66 / 42 | same |
| — HIGH / MEDIUM / UNRESOLVED confidence | 599 / 120 / 42 | same |
| — NODE_LEVEL / TOPIC_LEVEL / AMBIGUOUS granularity | 125 / 490 / 146 | same |
| Mapped to a D-topic | **719** | same; = `study_spine.totals.oral_questions_mapped` |
| Examiner relationships (study input) | **860** rows, **649** questions | `CURRENT_EXAMINER_RELATIONSHIPS.jsonl` |
| Examiner index pairs (product) | **958** pairs, **671** questions | `EXAMINER_INDEX_SNAPSHOT.json` / `examiner-index.html` |
| Examiners | **7** (Nair 332, Simon 246, Srivastava 103, Rajappan 93, Senthil 66, Paul 19, John 1 rels) | alias register + relationships |
| Written mapping records | 360 (all VALID, HIGH, GOVERNED_FIELD) — **369** exist in specs | `study_mappings.json` vs specs |
| D01–D10 domains | 10 | `study_spine.json` |
| Official syllabus nodes | 25 | `official_syllabus.json` |
| Crosswalk edges | 43 (D07 has none) | `official_crosswalk.json` |
| Mapping review queue | **108** (94 AWAITING_ADJUDICATION, 14 HELD_PENDING_EVIDENCE; all Oral) | `mapping_review_queue.json` |
| Oral release gate registry | 91 gates + 1 determinism = **92** | `tools/oral/oral_release_gates.py` |

### 4.2 Why earlier material says 721 / 738

`git log origin/main -- meoclass1/qb_content_index.json` shows the corpus grew in governed steps:

| Corpus | Period | Commit evidence |
|---|---|---|
| 721 | 2026-08-20 → 08-23 | `4272ad6` … `e046790` (GAP-0609 close, CSM/boiler fixes) |
| 725 / 727 | 2026-08-24 | `30c70a4`, `69a35fc` |
| 738 | 2026-08-25 | `018318b` "regenerate the derived surfaces for 738" |
| 739 → 759 | 2026-08-31 → 09-01 | BMP MS, H2, H3A, ORB, H3B-1/2, H4 |
| **761** | **2026-09-02 → now** | `0730c9a` "content index 759 -> 761"; study layer propagated in `3babafa` |

All are legitimate snapshots of one canonical corpus. 721 survives only in **stale prose**:
`docs/study/STUDY_ROADMAP.md` (deprecated), `docs/ORAL_FOLLOWUP_REGISTER.md:235`, the
`content_index_check` gate note, and a code comment in `build_public_study_roadmap.py`
("30 of 721"). `CURRENT_EXAMINER_RELATIONSHIPS.jsonl` was last regenerated **2026-08-23**
(721 corpus) — see gap G3. No September/H7 intake is on `origin/main`; 761 is the post-H6
count. A later H7 landing will change it, and every generated view must regenerate with it.

### 4.3 Card schema variants (verified per card, 761 parsed)

| Section | Cards | Notes |
|---|---|---|
| Question stem (`q-text`), answer (`answer-body`), CE Oral Tip (`ce-tip`), reg box | 761 / 761 / 761 / 761 | universal |
| `reg-item` entries | 747 cards | 2,595 distinct free-text reg codes — **not normalised** |
| Deep-dive family (any `dd-*` / deep-dive block) | 631 | heterogeneous across files |
| Practice block | 465 | |
| Trap content (`trap-box`/`dd-trap`/`trap-q`) | 295 | |
| Numbers (`numbers-box`/`dd-numbers`) | 221 | |
| Casualty (`casualty-box`/`dd-casualty`) | 201 | |
| Examiner chain (`dd-chain`/`examiner-chain`) | 177 | HTML only, not data |
| Formula | 160 | |
| CE-relevance / common failures / vessel (`dd-relevance`/`dd-fail`/`dd-vessel`) | 118 / 137 / 137 | enriched-schema files only (~10 files) |
| Oral-box (15/60 s) | 108 | |
| Card→card links | 317 links from 118 cards (270 same-file), **0 broken** | HTML only |
| Extra block | 57 | |

Feature density varies by **file schema generation, not by topic** (e.g. D10 54% chain vs D03 2%).
Topic pages therefore cannot promise "traps/numbers/casualty" uniformly per topic.

### 4.4 Existing in-card classification signals (candidate subtopic sources)

| Signal | State | Usable as governed subtopic? |
|---|---|---|
| `q-tag` chips | 507 distinct values; inconsistent case (`SURVEY`/`Survey`/`survey`), 102 empty, single-letter extraction artefacts | **No** — ungoverned display chips |
| `section-head` in QB files | 132 distinct headings, nearly all unique per file, incl. "Additional Questions — Q1–Q20" | **No** — per-file editorial layout |
| `mapping.subtopic_id` | schema slot exists, validated as a field, **0 / 1,121 populated** | **Yes — the intended slot** |
| Written `topic_taxonomy` leaves | 75 governed leaves under 7 categories (alias table, threshold rule) | **Yes as vocabulary** for D01–D07; none for D08–D10 |
| Annexure III nodes via crosswalk | 25 nodes; 125 Oral records node-resolved | Partial — scope, not a teaching structure |
| Notes units | 992 units, 39 files, **0 mapped to a D-topic** (all AMBIGUOUS in gap register); units file last regenerated 2026-08-18 (Parts 23–25 absent) | Not yet |

---

## 5. D01–D10 readiness matrix

"Examiner evidence" = questions with ≥1 relationship (rels / confirmed-tier questions / distinct examiners).
"Follow-up/variant density" = cards with an examiner-chain or card→card link block (HTML) — there is **no typed relationship data** for this (§7).

| Domain | Oral Q (valid / review) | Mapping confidence H / M | Examiner evidence | Follow-up/variant density | Official syllabus relationship | August-2026 recency (distinct Q) | Oral roadmap readiness |
|---|---|---|---|---|---|---|---|
| D01 Statutory & Class | 77 (76 / 1) | 42 / 35 | 71 Q, 103 rels, 40 confirmed, 6 ex | chain 23, links 14 | 6 primary + 5 supporting nodes; TOPIC_LEVEL | 22 | **READY_WITH_REVIEW** (45% medium-confidence; pack + sessions exist) |
| D02 Commercial Law | 116 (104 / 12) | 103 / 13 | 104 Q, 130 rels, 59 confirmed, 6 ex | chain 14, links 27 | 2 primary nodes; TOPIC_LEVEL | 37 | **READY_WITH_REVIEW** (12 pending; size needs subtopics) |
| D03 Human Element | 203 (198 / 5) | 190 / 13 | 177 Q, 235 rels, 110 confirmed, 6 ex | chain 5, links 21 | 8 primary + 3 supporting; TOPIC_LEVEL | 50 | **READY_WITH_REVIEW** (largest; unusable as one flat list) |
| D04 MARPOL | 65 (60 / 5) | 59 / 6 | 44 Q, 62 rels, 29 confirmed, 5 ex | chain 13, links 20 | 1 primary node (C49-A3-25) → NODE_LEVEL, but that node's probe coverage is **WEAK** | 17 | **READY_WITH_REVIEW** (node-level claim vs weak probe needs a look) |
| D05 GHG & Fuels | 67 (66 / 1) | 62 / 5 | 59 Q, 66 rels, 32 confirmed, 6 ex | chain 23, links 6 | 2 primary + 1 supporting; TOPIC_LEVEL | 19 | **READY** |
| D06 Indian Law | 4 (4 / 0) | 4 / 0 | 3 Q, 3 rels, 2 ex | none | 2 primary; TOPIC_LEVEL | 2 | **PARTIAL** (Oral-thin; topic is Written-led, 19 W) |
| D07 Cargo | 104 (89 / 15) | 88 / 16 | 94 Q, 134 rels, 66 confirmed, 6 ex | chain 56, links 5 | **none** — no crosswalk edge; all 104 AMBIGUOUS | 37 | **READY_WITH_REVIEW** (strong Oral evidence; must say "no official item"; 15 pending) |
| D08 Fire & LSA | 27 (27 / 0) | 27 / 0 | 21 Q, 29 rels, 12 confirmed, 4 ex | chain 5, links 5 | 1 supporting node only → NODE_LEVEL | 4 | **READY** (small) |
| D09 Machinery | 23 (22 / 1) | 18 / 5 | 18 Q, 18 rels, 13 confirmed, 4 ex | chain 1 | 3 primary + 4 supporting; TOPIC_LEVEL | 3 | **READY_WITH_REVIEW** (thin) |
| D10 Construction & Stability | 33 (**7 / 26**) | 6 / 27 | 24 Q, 39 rels, 10 confirmed, 5 ex | chain 18, links 15 | 1 primary (C49-A3-04, P1 gap lane) → NODE_LEVEL | 7 | **PARTIAL** (79% review-pending) |
| (no domain) | 42 unmapped | — | 34 Q have examiner evidence (41 rels) | chain 19 | UNRESOLVED | 9 | **NOT_READY** |

---

## 6. Mapping / gap statistics (quantified, not fixed)

| Gap | Count | Evidence |
|---|---|---|
| Oral questions with no D-topic | **42** (34 of them examiner-evidenced; 3 are post-721 cards) | `mapping_status = ACCIDENTALLY_UNMAPPED` |
| Ambiguous / review-pending mappings | **66** REVIEW_PENDING; queue 108 (52 "cue inside mixed file", 42 "no cue", 14 held with written reasons e.g. SUA, FAL, CIC, MEPC 84) | `mapping_review_queue.json` |
| File-title contradictions | 25 records (`FILE_TITLE_CONTRADICTED`), 6 files flagged | queue `file_title_contradictions` |
| Mapped only at topic level | **490** TOPIC_LEVEL; 146 AMBIGUOUS; 125 NODE_LEVEL | granularity |
| Mapped by file title alone (no text corroboration) | 274 `FILE_TITLE` | `mapping_evidence` |
| Human-adjudicated Oral mappings | 82 (`HUMAN_ADJUDICATION`); `last_reviewed` set on 136 | |
| Stale mappings | Oral: none (index ↔ mappings 1:1). Written: QP2609 (9 Q) missing | |
| Orphan questions / broken anchors | **0 / 0** (index, mappings, relationships, card links all resolve) | |
| Examiner evidence but no study mapping | **34** | join |
| Study mapping but no examiner relationship | **104** mapped questions (incl. all 40 post-721 cards) | join |
| Post-721 cards with zero study-layer examiner rows | **40 / 40** (relationships file frozen 2026-08-23) | join vs `e046790` index |
| Topic areas with no Oral content | none at domain level; D06 has 4 | |
| Official nodes with weak/no Oral evidence | C49-A3-25 (0 oral probe hits, WEAK), C49-A3-05 (1, WEAK), C49-A3-17 (1, PARTIAL), C49-A3-20 (2, PARTIAL), C49-A3-15 / -18 / -19 (2 each) | `coverage_matrix.json` |
| Gap-register node states | 22 nodes AMBIGUOUS_MAPPING / TOPIC_LEVEL_EVIDENCE_ONLY; 3 NODE_EVIDENCED_NO_GOVERNED_ANSWER (P1) | `syllabus_gap_register.json` |
| Duplicate/conflicting topic labels | `q-tag` 507 variants; 132 per-file section heads; two examiner denominators (860 vs 958) | |
| Families not representable | follow-up/variant typing absent from relationships (860 UNSPECIFIED) | §7 |
| Relationship data present but not surfaced | 317 card→card links; 177 examiner-chain blocks; 26 cross-examiner families; 35 follow-up actions; 207 August-matched questions; notes coverage for 373 questions | §7–9 |
| Reciprocal navigation | **0 / 86** QB files link to `topics.html`; 3 QB files link to Notes | |

---

## 7. Oral question-family assessment

What already exists:

* **Canonical card = the family anchor.** The 788-row reconciliation already sorted every historical examiner ask against a card (EXACT_MATCH 22, SAME_CORE_ASK 24, NEAR_MATCH 40, PARTIAL_COVERAGE 369, AMBIGUOUS 115, MISSING 218) — i.e. "variant wording → canonical card" is already governed evidence.
* **CROSS_EXAMINER_FAMILIES.json** — 26 untyped families (34 canonical ids), explicitly "no probability derived".
* **oral_followup_register.json** — 35 typed actions keyed by `parent_canonical_id` with edge `EXAMINER_FOLLOW_UP` (31 are TOPIC_INFERENCE_ONLY, 29 require live adjudication; 3 produced).
* **August 2026 intake** — 283 occurrences with typed classification (FOLLOWUP 27, PARAPHRASE_EXISTING 119, EXACT_EXISTING 62, GENUINE_NEW 44 …) and **`parent_occurrence_id` chains** (30 adjudications).
* HTML-only: 177 examiner-chain blocks, 317 card→card links.

What is missing: the study-layer relationship file types **all 860 rows `UNSPECIFIED`**; none of the above is joined into one relationship view keyed by canonical id.

**Recommendation:** an ORAL QUESTION FAMILY should be **the existing canonical card plus a *generated* relationship projection** (variants from the 788/August adjudications, follow-ups from the register + `parent_occurrence_id`, cross-examiner from ASF families). It should **not** be a new governed entity type and must not be produced by semantic clustering. The only governed addition that may eventually be needed is a typed `relationship_type` vocabulary on rows that already exist (the follow-up register already defines one: `EXAMINER_FOLLOW_UP`, `CROSS_QUESTION`, `PRIMARY_ASK`, `UNSPECIFIED`). HTML chain/link blocks should be read as display, not promoted to data, unless adjudicated.

---

## 8. Examiner-intelligence assessment

* **Topic → Examiners → Questions** is derivable today for 649 questions (and `topics.html` already prints examiner names per question). **Examiner → Topics → Questions** is the existing `examiner-index.html`. Both read the same relationship records — two projections, no duplication — **but they read different files today**: study surfaces read `CURRENT_EXAMINER_RELATIONSHIPS.jsonl` (860 / 649 Q, frozen at 721); the examiner index reads `EXAMINER_INDEX_SNAPSHOT.json` (958 / 671 Q, includes card attributions and CE-tip mentions). A roadmap must pick **one** denominator and label it; the snapshot is the more current.
* **Tiers exist and must be shown honestly:** confirmed 412, inferred 322, header 78, ce_tip 47, reported 1. A topic's "examiner breadth" counted from inferred-only rows would overstate evidence (e.g. D03: 59 questions are inferred-only).
* **Recent frequency:** the historical 788 records have **no dates** (single undated "All Surveyors" compilation). The only dated, recent signal is the **August 2026 intake window** (28 submissions, 283 occurrences, 207 matched canonical questions), and **271 / 283 occurrences are panel-level only** (examiner not individually attributed). The window is `OPEN_EXPECTING_MORE_INPUT`. So "recently asked" is derivable per question **only as "asked in the August 2026 window"**, not per examiner, and should stay internal or gated until the window is closed.

---

## 9. Notes / Written cross-link assessment

| Link | Today | Assessment |
|---|---|---|
| Oral ↔ D-topic ↔ official node | governed (mappings + crosswalk) | reuse |
| Oral ↔ Written (same D-topic) | derivable by shared `topic_id`; `topics.html` deliberately links only to public `/SQ/` because ORAL_QB_NOTES and SOLVED_QP are **separate entitlements** (`build_topic_pages.py:30-38`) | Show counts + storefront link; never a gated cross-product link |
| Oral ↔ Notes | `ORAL_NOTES_COVERAGE.jsonl` gives note units per canonical question for **373** questions (support levels COMPLETE 153 / STRONG 83 / PARTIAL 320 / TOPIC 177 per source ask) | DERIVABLE, but snapshot is from 2026-08-18; Parts 23–25 missing; must be regenerated, not copied |
| Notes ↔ D-topic | **none** (992 units AMBIGUOUS) | NEEDS a mapping pass through the same `mapping_engine` adapter pattern — not a new taxonomy |
| Simon notes | 162 units in the same files; same entitlement (ORAL_QB_NOTES) | permitted on the paid surface, via relationships only |

The principle holds: one knowledge structure, links not copies. No Note text should be duplicated into Oral roadmap pages.

---

## 10. Public / paid projection assessment

* **Paid (ORAL_QB_NOTES):** everything under `/meoclass1/` is gated by `middleware.js` (matcher `/meoclass1/:path*`; HMAC session + Redis entitlement). `topics.html` / `study.html` inherit the gate by path. A full Oral roadmap belongs here.
* **Public:** `SQ/study-roadmap.html` is produced by `build_public_study_roadmap.py` from a **field whitelist** (`PUBLIC_TOPIC_FIELDS`: Oral count, examiner-evidenced count, distinct examiners) plus at most **3 Oral stems per topic** (≤180 chars, first VALID_MAPPED by sorted id — no allowlist file), and `assert_public_safe` refuses any `/meoclass1` or `/solvedQP` link. Public examiner content is separately configured (`examiner_index_config.json`: Paul full, Simon 5-row preview).
* **One model, two projections is already the house pattern** (cf. `safe_qi_projection.json` PUBLIC / GATED / INTERNAL fields). An Oral roadmap model should declare per-field audience the same way; the public builder extends its whitelist, it never reads a second dataset.
* Must stay out of public: answers, CE tips, traps, numbers, examiner names per question beyond the configured teaser, August recency, inferred-tier claims.

---

## 11. Release-gate impact (no change proposed)

Existing gates already protect roadmap inputs:

| Input | Gates (in the 91+1 registry) |
|---|---|
| `qb_content_index.json` | `content_index_check`, `content_index_validate` (23 checks), `content_index_mutate` (26 mutations) |
| Study mappings / spine | `study_mapping_check` ("every canonical oral question must already carry a governed mapping"), `study_spine_validate` |
| Gated topic/study pages | `study_pages_check` (`build_topic_pages.py --check`) |
| Public roadmap | `study_public_roadmap_check` (incl. `assert_public_safe`) |
| Examiner index | `examiner_check`, `validate_examiner_index` (55), `examiner_mutate`, `test_examiner_check` |
| Follow-up register | `validate_followup_register`, `followup_register_mutate`, `followup_closure_controls` |

Observations:
* A roadmap that **extends `build_topic_pages.py` output** inherits `study_pages_check` with no new gate. A **new artefact** (e.g. `docs/study/oral_roadmap.json`, per-topic pages) would need its own `--check` and a validator — those belong in **study validation** first, and are surfaced to release only through the existing pattern of a `--check` gate in the registry. This audit does not authorise adding them.
* Study acceptance/mutation tests (`test_mapping_engine`, `test_syllabus_fanout`, `test_study_expandability`, `test_roadmap_cockpit`, QI mutations) are **not wired into any runner**; they are manual (`tools/study/SKILL.md`).
* No toolchain runs the study chain automatically on intake; the Oral release suite only *detects* staleness. Gate notes still carry stale counts (721, 862).
* H7/H8/H9 interaction: any future intake changes 761 and is caught by `content_index_check` → `study_mapping_check` → `study_pages_check`. A roadmap generated over the same inputs would be re-derived in the same run — no extra coupling, provided it is a pure function of those inputs.

---

## 12. Option comparison

| | A — Simple topic index | B — Oral study roadmap | C — New Oral taxonomy |
|---|---|---|---|
| What it is | D01–D10 → question list | D01–D10 → subtopics → order → questions → examiner/follow-up/regs/notes/written | Independent Oral classification |
| Current state | **Exists** (`topics.html`, gated, gate-protected) | Partially: domain order, examiner names, official items exist; subtopic, sequence, relationships, notes, back-links absent | — |
| Usefulness | Low for D02/D03/D07 (116–203 flat items, id order) | High — answers "what next, in what order" | High short-term |
| Maintainability | Fully generated | Generated, except bounded editorial fields (subtopic, sequence) held in an adjudication store like `adjudications.json` | Two taxonomies to keep in step with spine, crosswalk, Written, Notes |
| Governance risk | Low | Medium — only if subtopic/order become free text; mitigated by vocabulary reuse + `--check` | High — contradicts "There is no second taxonomy" (STUDY_ROADMAP design record) |
| Duplication | None | None if built as a projection | Duplicates spine + crosswalk + Written leaves |

**Recommendation: Option B, built as an extension of the existing study projection.** Option C rejected — the evidence does not show any Oral requirement the spine cannot hold; the missing level is a *subordinate* one the schema already reserves (`subtopic_id`).

---

## 13. Recommended architecture

```
Canonical Oral cards (QB*.html)                 ── unchanged
  + qb_content_index.json                       ── unchanged
  + study_mappings.json  (topic_id, + subtopic_id populated by adjudication)
  + adjudication store for subtopic + sequence  (hand-maintained, like adjudications.json)
  + ONE examiner relationship source            (snapshot-grade, typed where register/intake prove it)
  + official_crosswalk.json                     ── unchanged
  + notes relationships (ORAL_NOTES_COVERAGE, regenerated) + Notes→D-topic mapping (same engine)
  + August-window recency (gated/internal only)
        ↓  one deterministic builder (extension of build_topic_pages / export_roadmap_xlsx)
  oral roadmap model (per-field audience: PUBLIC / GATED / INTERNAL)
        ↓                                  ↓
  meoclass1/topics.html (+ per-topic views)   SQ/study-roadmap.html (whitelist only)
```

Rules: no generated page is a source of truth; no question list is hand-maintained; subtopic vocabulary is drawn from Written leaves (D01–D07) and, for D08–D10 only, a small adjudicated list; every count is `len()` of rendered records (existing house rule in `build_topic_pages.py`).

---

## 14. Candidate UX / navigation model (sketch only)

```
ORAL Q&A
├── Study Roadmap (study.html)           domain order: prerequisites first (exists)
├── Study by Topic (topics.html)         exists — to be deepened
│   └── D03 Human Element, ISM & Management
│        ├── Overview: official items, counts, examiner breadth (tier-labelled)
│        ├── Subtopics (e.g. reused Written leaves) — each with:
│        │    ├── Learn first      (sequence position 1–n, adjudicated)
│        │    ├── Core questions   → QBx.html#qN
│        │    ├── Asked in Aug-2026 window (gated)
│        │    ├── Follow-ups / variants (from register + intake, typed)
│        │    ├── Regulations & numbers (cards with numbers/reg blocks; display-only)
│        │    └── Related Notes (relationship links)
│        ├── Related Written: count + /SQ/ storefront link (entitlement-safe)
│        └── Unmapped / under-review questions disclosed, not hidden
├── Study by Examiner (examiner-index.html)  exists — same relationship data
├── Question Bank (index.html, QB navigation) exists
└── Search                                   exists
Card back-link: "Part of D03 › <subtopic> — see topic" (new, generated)
```

---

## 15. Data / schema changes required

| Class | Change |
|---|---|
| **None** | D01–D10, crosswalk, official syllabus, card HTML schema, release framework, examiner alias register |
| **Generated-only** | deeper `topics.html` (subtopic grouping, tier-labelled examiner counts, disclosed unmapped list); card→topic back-links; Oral↔Notes links from regenerated coverage; August-window recency (gated); public whitelist extension; regenerate stale `ORAL_NOTES_UNITS`, relationships file, Written QP2609 mappings |
| **Relationship / schema extension** | populate existing `subtopic_id` (no new field); typed `relationship_type` values on existing relationship rows using the register's existing vocabulary; Notes records through the `mapping_engine` adapter pattern; per-field audience declaration for the Oral roadmap model; a `sequence` field in an adjudication store (new field, bounded) |
| **Editorial adjudication** | clear the 108-item mapping queue (D10 first); assign subtopic per question (machine-cued via Written aliases, human-decided); sequence position within subtopic; adjudicate the 31 TOPIC_INFERENCE_ONLY follow-up actions before display |

---

## 16. Implementation effort (no time estimates)

| Component | Effort |
|---|---|
| D01–D10 spine, crosswalk, mapper, Oral mappings | ALREADY EXISTS |
| Gated Oral-by-topic page + gate | ALREADY EXISTS |
| Public roadmap with Oral whitelist | ALREADY EXISTS |
| Examiner index (Examiner → Q) | ALREADY EXISTS |
| Card → topic back-links | SMALL |
| Single examiner denominator for study surfaces (adopt snapshot) | SMALL |
| Disclose unmapped/under-review on topic page; tier-labelled examiner counts | SMALL |
| Regenerate stale inputs (relationships, notes units, QP2609 mappings) | SMALL |
| Clear mapping queue (108) | MEDIUM (editorial) |
| Subtopic vocabulary + cue proposals from Written aliases | MEDIUM |
| Subtopic assignment for 761 questions | LARGE (editorial, bounded) |
| Learning-sequence adjudication | LARGE (editorial) — or MEDIUM if limited to D01–D03 first, where packs/sessions already rank cohorts |
| Typed follow-up/variant relationship projection | MEDIUM |
| Notes → D-topic mapping + Oral↔Notes links | MEDIUM |
| Per-field audience model + public whitelist extension | SMALL–MEDIUM |
| New `--check` / validator for a new artefact (if any) | SMALL each |

---

## 17. Risks

1. **Silent staleness** — study chain is manual; already visible (relationships frozen at 721, notes units at 18 Aug, QP2609 unmapped). A richer roadmap multiplies stale surfaces unless it is one builder behind existing `--check` gates.
2. **False precision** — showing node-level syllabus claims for TOPIC_LEVEL/AMBIGUOUS records (636 of 761), or "examiner-asked" for inferred-only rows.
3. **Recency over-reading** — August data is panel-level and the window is open; per-examiner "recently asked" would be unsupported.
4. **Taxonomy creep** — subtopics becoming free-text labels per page; mitigated by reuse of Written leaves and a closed vocabulary.
5. **Entitlement leak** — cross-linking ORAL ↔ SOLVED_QP gated pages, or public projection reading gated fields.
6. **Collision with H7/H8/H9** — any edit to QB cards or index for roadmap purposes would collide with release lanes; roadmap work must be read-only over cards.
7. **Feature-density illusion** — traps/numbers/casualty blocks exist only in some file generations; per-topic sections would look uneven by schema, not by importance.

---

## 18. Founder decisions (genuine product / authority only)

1. **Approve Option B as an extension of the existing study projection** (and reject Option C).
2. **Subtopic vocabulary authority:** adopt Written `topic_taxonomy` leaves as the Oral subtopic vocabulary for D01–D07, with a small adjudicated list for D08–D10 — or decide D01–D10 only (no subtopics) for v1.
3. **Learning sequence:** authorise editorial sequence adjudication (and in which domains first), or accept "priority cohorts" (A/B/C as in TOPIC packs) instead of a strict order.
4. **Examiner denominator:** which examiner source the study surfaces display (snapshot 958 vs relationships 860), and whether inferred-tier rows count toward displayed breadth.
5. **Recency exposure:** whether August-window "asked recently" is shown on the paid surface before the window is closed, and never publicly.
6. **Public discovery scope:** keep the current 3-stem/topic whitelist, or extend it (counts per subtopic only).
7. **Sequencing vs releases:** confirm the roadmap work waits behind (or runs read-only alongside) H7 so that 761 → H7 count changes are absorbed by regeneration.

---

## 19. Proposed implementation phases (none started)

* **Phase 0 — Freshness (generated-only).** Regenerate relationships/examiner source, notes units/coverage, Written QP2609 mappings via existing builders; correct stale count notes. No new artefacts.
* **Phase 1 — Option A+ (generated-only).** Deepen `topics.html`: disclose unmapped/under-review, tier-labelled examiner counts, card → topic back-links. Inherits `study_pages_check`.
* **Phase 2 — Mapping debt (editorial).** Adjudicate the 108-item queue, D10 first, through `adjudications.json`.
* **Phase 3 — Subtopic layer (schema slot + editorial).** Cue proposals from Written aliases; human adjudication fills `subtopic_id`; validator rule added to study validation.
* **Phase 4 — Relationships.** Typed follow-up/variant projection from register + intake + 788 reconciliation; Notes → D-topic mapping.
* **Phase 5 — Sequence + public projection.** Adjudicated sequence (D01–D03 first, seeded from packs/sessions); per-field audience model; public whitelist extension under `study_public_roadmap_check`.

Each phase is regenerated by intake: new report → intake adjudication → canonical relationship → mapper → relationship projection → roadmap rebuild → `--check` gates. The Founder edits adjudication stores only, never topic pages.

---

### Confirmation

No Oral card, content index, mapping, relationship, register, gate, generator, or public/paid page was modified. No commit, push, deploy, or publish occurred. The quarantined local checkout was not altered beyond `git fetch origin main`.
