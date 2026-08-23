# Study spine & syllabus mapping — integration contract

The layer that joins every MIW question to one canonical topic, so that Oral,
Written, study packs, question intelligence and any future audio/flashcard
mode all resolve through the **same** identity chain:

```
canonical_question_id  ->  topic_id  ->  syllabus_node_id
   QB1_A#q1 / QP2301-Q1     D01..D10     (null until an official DGMA
                                          instrument is ingested)
```

**Read `docs/study/SYLLABUS_SOURCE_STATUS.md` first.** No official DGMA
syllabus exists in this repository. This spine is MIW-DERIVED and must never
be described to a candidate as "the DGMA syllabus".

## Files

| Path | Role |
|---|---|
| `tools/study/study_spine.py` | **Registry.** Domains, prerequisites, oral file→domain map, question cues, priority weights. Edit this to change the taxonomy. |
| `tools/study/mapping_engine.py` | **Library.** One mapper, two adapters. Every consumer calls this — nobody parses mapping JSON directly. |
| `tools/study/build_study_mappings.py` | **Only writer** of the mapping store. Incremental by default. |
| `tools/study/build_study_spine.py` | Aggregates the store into per-domain intelligence. Reads the store; never re-derives mappings. |
| `tools/study/validate_study_spine.py` | The gate. Fails closed. |
| `tools/study/test_mapping_engine.py` | Acceptance tests, synthetic fixtures only. |
| `tools/study/test_d01_priority_cohort.py` | Gates the Topic 01 A/B/C/review partition against the live corpus. Parses the cohorts back out of the pack — there is no second store of cohort membership. |
| `docs/study/study_mappings.json` | Governed mapping records (generated). |
| `docs/study/mapping_review_queue.json` | Ambiguous mappings awaiting adjudication (generated). |
| `docs/study/study_spine.json` | Per-domain aggregation (generated). |

All of these are under `tools/` and `docs/`, both **deploy-excluded** in
`.vercelignore`. Changing them deploys nothing.

## The library API

```python
import mapping_engine as ME

ME.map_question(item, 'ORAL',    file_name='QB1_A.html')   # -> record
ME.map_question(item, 'WRITTEN', paper_id='QP2301')        # -> record
ME.resolve_topic('D01')                                    # -> domain record
ME.validate_mapping(record)                                # -> [] if valid
ME.get_question_topic(qid, store)                          # -> 'D01' | None
ME.get_topic_questions('D01', store, content_type='ORAL')  # -> [ids]
ME.review_queue(store)                                     # -> adjudication items
ME.incremental_update(store, items, force=False)           # -> (store, stats)
ME.classify_against_taxonomy(store)                        # -> drift report
ME.taxonomy_version()                                      # -> digest
```

## Confidence and status — the rule that matters

**Two fields, two questions.** `mapping_evidence` says *what was read*;
`mapping_confidence` says *what was decided*. They are not the same question
and the schema keeps them apart on purpose. A strong source does not imply a
confident decision — that conflation is exactly what produced the D02
over-capture corrected on 2026-08-23, where a QB file title minted
HIGH-confidence mappings for questions that were not about that topic at all.
`mapping_confidence` is **always** confidence in the mapping, never confidence
that the file title was read correctly.

| `mapping_evidence` | Meaning | Confidence | Status | Published? |
|---|---|---|---|---|
| `GOVERNED_FIELD` | Written spec `primary_category` | HIGH | `VALID_MAPPED` | yes |
| `FILE_TITLE` | Oral file names one domain; question text silent | HIGH | `VALID_MAPPED` | yes |
| `FILE_TITLE_CORROBORATED` | ...and the question's own cue agrees | HIGH | `VALID_MAPPED` | yes |
| `FILE_TITLE_CONTRADICTED` | ...but the question's own cue points elsewhere | MEDIUM | `REVIEW_PENDING` | **no** |
| `TEXT_CUE` | Domain cue matched text inside a **mixed** file | MEDIUM | `REVIEW_PENDING` | **no** |
| `HUMAN_ADJUDICATION` | A named reviewer decided, with a written note | HIGH | `VALID_MAPPED` | yes |
| `NONE` | Nothing matched | UNRESOLVED | `ACCIDENTALLY_UNMAPPED` | **no — gate fails** |

`EVIDENCE_NEVER_HIGH` enforces the governing invariant: **file-level evidence
must not suppress obvious question-level contradictory evidence.** A
contradicted mapping keeps the file's topic as a placeholder — emptying a
topic on a suspicion would be worse than the error being fixed — but it loses
the *claim* to being settled, so it lands in the review queue instead of being
published. That makes the demotion **count-neutral**: `build_study_spine.py`
aggregates by `topic_id`, not by status, so only a human reassignment moves a
topic count.

A MEDIUM/LOW mapping can only become `VALID_MAPPED` by acquiring a
`last_reviewed` stamp from a human adjudication. The validator rejects the
promotion otherwise.

### `adjudications.json` — three decisions, one guard

| `decision` | Does what |
|---|---|
| `AFFIRM` (default) | The mapper is right. Stamp it `VALID_MAPPED`. |
| `REASSIGN` | The mapper is wrong. Move the question to `topic_id`, relabel evidence `HUMAN_ADJUDICATION`, and recompute the official-syllabus join. Requires `mapper_topic_id`. |
| `HOLD_REVIEW` | The evidence does not settle it. Force `REVIEW_PENDING` and record `candidate_topic_ids`. Never published — **do not force a topic merely to empty the queue.** |

The guard is the same for all three: the entry must restate what the mapper
currently says (`mapper_topic_id`, defaulting to `topic_id`). If the taxonomy
has since moved the question, the entry is **refused** rather than
rubber-stamping a stale decision. `REASSIGN` records
`adjudicated_from_topic_id` so re-application is idempotent while a genuine
taxonomy move is still caught.

`docs/study/mapping_review_queue.json` carries a derived
`file_title_contradictions` block: the standing inventory of files still
showing this pattern. It is regenerated every build, so it cannot rot.

**HELD is not UNADJUDICATED, and no summary may sum them.** Every counter in
that file — top-level `queue_states` and per-file alike — splits
`fresh_unadjudicated` (nobody has read it) from `held_adjudicated` (a named
human read it and recorded why the evidence does not settle it). They were a
single `unadjudicated` number until 2026-08-23, when `QB4_H.html` was found
reporting one outstanding question that was in fact `QB4_H#q9`, carrying a
written HOLD. Reporting finished governance work as backlog is pressure to
clear a hold, and forcing a topic to empty the queue is the one move this
contract forbids. `mapping_engine.queue_summary()` is the only place the split
is computed; `R-QUEUE-*` in the validator gates it, and a held item must still
appear in the queue — uncertainty stays visible, it just stops being counted
as work nobody has done. The engine **never** copies a "similar" question's
mapping: the oral follow-up work already proved similarity scoring picks
semantically wrong parents.

## Routine commands

```bash
python tools/study/ingest_official_syllabus.py        # official Annexure III
python tools/study/build_official_crosswalk.py        # official node -> topic
python tools/study/build_study_mappings.py            # incremental map
python tools/study/reconcile_official_mappings.py     # attach official join
python tools/study/build_study_spine.py               # aggregate
python tools/study/build_coverage_matrix.py           # coverage per official node
python tools/study/build_evidence_horizon.py          # what the numbers rest on
python tools/study/export_roadmap_xlsx.py             # roadmap workbook
python tools/study/build_topic_pages.py               # topics.html + study.html (GATED)
python tools/study/build_public_study_roadmap.py      # SQ/study-roadmap.html (PUBLIC)
python tools/study/validate_study_spine.py            # gate
python tools/study/test_mapping_engine.py             # acceptance
python tools/study/test_study_expandability.py        # expandability controls
python tools/study/test_d01_priority_cohort.py        # D01 A/B/C partition gate
```

Each builder also takes `--check`, which fails if its artefact is stale. The
gate sequence for a study change is the `--check` of every builder plus the
validator and the acceptance suite.

The source PDF is **not committed** (`docs/study/sources/*.pdf` is ignored in
both `.gitignore` and `.vercelignore`). To restore it:

```bash
python tools/study/ingest_official_syllabus.py --download
```

That verifies the pinned SHA-256 and **fails closed** on any mismatch — and
names the superseded July draft specifically if it is handed that instead.

After editing `study_spine.py` (a taxonomy change) the digest moves, so run:

```bash
python tools/study/build_study_mappings.py --force
```

Every prior mapping is then reported `STALE` and re-derived. Human review
stamps survive re-derivation; a mapping that lands on a different topic is
marked with `previous_topic_id` and counted as `migrated`.

## Integration points for future production

### Oral QB production (`tools/oral/`)

Today the oral toolchain does **not** call this layer. The intended contract,
to be wired when the follow-up batches close:

```
new canonical oral question authored
  -> build_qb_content_index.py regenerates meoclass1/qb_content_index.json
  -> build_study_mappings.py            (picks up the new id incrementally)
  -> validate_study_spine.py            (fails if the new question is unmapped
                                         and not in the review queue)
  -> build_study_spine.py               (refresh topic aggregation)
```

**TODO (bounded, not done in this session):** add the two `build_study_*`
calls plus the validator to the oral release runner, so a new oral question
cannot ship `ACCIDENTALLY_UNMAPPED`. Scope: runner wiring only — the mapping
code already exists and is tested. Deliberately deferred here to avoid
touching the release harness mid follow-up production.

### Written QP production (`tools/pastpapers/`)

```
new paper spec authored (primary_category + subject_tags set)
  -> build_study_mappings.py    (HIGH-confidence, no review needed)
  -> validate_study_spine.py
  -> build_study_spine.py
```

Written mapping is HIGH-confidence by construction because `primary_category`
is an authored, governed field. **A new paper only needs its
`primary_category` to be one of the registered categories** — if an author
invents a new one, `R-CAT-CLAIMED` fails loudly rather than dropping the
question.

### Future XLSX export (`tools/oral/export_xlsx.py`)

The exporter stays **downstream** and gains no syllabus logic of its own:

```
mapping_engine  ->  study_mappings.json  ->  export_xlsx.py
```

When an approved workbook is to carry syllabus columns, it reads the already
governed fields — `topic_id`, `official_syllabus_node_id` (or its candidate
set), `official_alignment_status`, `official_mapping_confidence` — and prints
them. **Do not classify anything inside the Excel tooling.** A second
classifier in the exporter would be a second taxonomy by the back door.

Note for whoever wires this: 111 questions are `ORPHANED_IN_ADOPTED_SYLLABUS`
(all D07 cargo). A column that renders that as blank will read as a data
defect. Render the status, not an empty cell.

### Study packs / QI / future audio, flashcards, examiner simulation

All must resolve through `get_topic_questions()` / `get_question_topic()`.
One canonical question identity drives every mode. Do not build a second
lookup.

## The expandable evidence layer

Stable identity and growing evidence are separated on purpose:

| Stable (never migrated by evidence growth) | Expandable |
|---|---|
| `topic_id` D01–D10, `official_syllabus_node_id`, `canonical_question_id`, `paper_id`, `family_id`, examiner identity | oral/written question evidence, examiner relationships, Written QI, recurrence families, historical coverage, recency and trend, marks, resources, study status, future syllabus versions |

`tools/study/evidence_model.py` owns the vocabulary; `written_evidence_horizon.json`
records what every roadmap number actually rests on. Rules:

1. **No corpus size is ever hardcoded.** Counts derive from the horizon, so a
   new paper widens the numbers by itself.
2. **Public copy is generated.** `public_evidence_claim()` computes the
   strongest sentence the *stored* evidence supports. It cannot produce a
   "since 2010" claim while the historical layer is `NOT_STARTED`.
3. **Fake completeness fails closed.** `assert_honest()` rejects a
   `COMPLETE` claim that carries known gaps, a `VALIDATED_RANGE` with no
   evidence, an inverted span, or a `NOT_STARTED` layer carrying counts.
4. **Historical frequency is not current relevance.** `dormancy` and
   `relevance` are separate axes; a long-running family under a superseded
   instrument must be able to say `SUPERSEDED`.
5. **Progress is an input, never an output.** `study_progress.json` is
   hand-maintained; no generator writes it, and a topic missing from it
   defaults to `NOT_STARTED` rather than erroring.

The historical Written QI socket is declared and deliberately empty. See
`docs/study/HISTORICAL_WRITTEN_QI_RECOVERY_BRIEF.md`.

## Candidate surfaces

Three generated pages, two audiences, one model.

| Page | Audience | Gate |
|---|---|---|
| `meoclass1/topics.html` | paid — Oral by Topic | `/meoclass1/:path*` matcher |
| `meoclass1/study.html` | paid — study roadmap landing | `/meoclass1/:path*` matcher |
| `SQ/study-roadmap.html` | **public** — discovery teaser | none: `/SQ/` is off the matcher |

All three are **generated** — never hand-edited.

Gating is by PATH, and the guarantee runs in the right direction: Edge
Middleware is not invoked off its matcher, so `/SQ/` is public because the gate
never runs, not because a rule inside the gate permits it.

Cross-product links go to the **storefront** (`/SQ/`), never to
`/solvedQP/…`. `render_common.delivery_links()` records why in the other
direction: ORAL_QB_NOTES and SOLVED_QP are separate entitlements, so linking
one paid surface from the other bounces a customer to login inside their own
product.

### The public page has a harder contract than the gated ones

`build_public_study_roadmap.py` projects the same governed model through a
**field whitelist** (`PUBLIC_TOPIC_FIELDS`), so study progress, priority
scores, diagnostic coverage bands and hand-recorded topic gaps are dropped by
default rather than excluded by name. `assert_public_safe()` then runs over the
**rendered bytes** — a gated link, an answer marker, an internal governance
token, an over-wide evidence claim or a sample-quota overrun fails the build,
and `study_public_roadmap_check` runs it again at release time.

Sample question stems are capped at `SAMPLES_PER_TOPIC` (3) and restricted to
`VALID_MAPPED` records, so nothing still in adjudication is advertised. Written
records carry no text, so no Written stem is ever published — the public
Written signal is recurrence family names and counts.

The public evidence sentence is recomputed by
`evidence_model.public_evidence_claim()` and compared with the stored
`derived_sentence`; a mismatch means the horizon artefact is stale and the
build stops rather than publishing either wording.

## The official syllabus layer

```
DGMA Circular 49 of 2026, Annexure III   (25 official items, SHA-256 pinned)
        |  build_official_crosswalk.py   (hand-adjudicated, 43 edges)
        v
canonical MIW topics  (10 domains -- the durable study/join layer)
        |  mapping_engine.attach_official()  (STRUCTURAL, never text similarity)
        v
1081 governed question mappings
```

Rules that must not be relaxed:

1. **Official wording is quoted, never paraphrased.** It lives only in
   `official_syllabus.json`. MIW topic headings are *not* DGMA headings and
   the spine must keep saying so (`R-AUTHORITY`).
2. **Two syllabus versions, never merged.** `syllabus_version`
   (`MIW-DERIVED-1.0`) is what is operative today; `official_syllabus_version`
   (`DGMA-C49-2026-ANNEX3`) is adopted and takes effect **2027-01-01**. No
   public surface may present the 2027 syllabus as in force before then.
3. **`syllabus_node_id` is not `official_syllabus_node_id`.** The operative
   version defines no node ids at all, so the former must stay null; the
   validator rejects an official node smuggled into it.
4. **A pinpointed official node must be earned.** It may only be set when the
   candidate set contains exactly one node. Otherwise the record aligns to the
   set and says so.
5. **The coverage matrix is diagnostic, never a mapping.** Its probe terms
   must never be used to decide a question's topic or node.

## Question Intelligence — one brain, 2010 to August 2026

**Do not build a second recurrence model.** Everything about what recurs lives
in `docs/study/qi/`, generated by one builder from three inputs. If you need a
recurrence number, read it from there; if it is missing, extend that layer.

| Path | Role |
|---|---|
| `tools/study/qi_model.py` | **Vocabulary and guards.** Evidence bands, the three claims, limb states, join verdicts, horizon. Read this first. |
| `tools/study/qi_similarity.py` | **Proposes only.** Candidate pairs. It never decides a family. |
| `tools/study/qi_phase1_adjudications.json` | **Hand-maintained.** The semantic decisions, in entity ids. |
| `tools/study/build_qi.py` | **Only writer** of `docs/study/qi/*`. `--check` proves disk matches inputs. |
| `tools/study/validate_qi.py` | The gate. 19 invariants, fails closed. |
| `tools/study/test_qi_mutations.py` | 14 mutations, all must be caught. |
| `tools/study/preview_qi_study_impact.py` | Read-only study preview. Asserts it writes no study file. |

```bash
python tools/study/build_qi.py            # rebuild
python tools/study/build_qi.py --check    # is the layer stale?
python tools/study/validate_qi.py         # the gate
python tools/study/test_qi_mutations.py   # prove the gate still bites
```

### The four rules that are easy to break

1. **The horizon is 2010-01 to 2026-08.** 2010 is a permanent Founder floor.
   Do not search for, ingest, or plan pre-2010 material. Invariant 01 and 16
   fail the build if either boundary is crossed.

2. **Never collapse the three claims.** Wording, sitting date and official
   occurrence are separate and stay separate. No 2010-2020 record carries
   `OFFICIAL_DATED`, and a public dated claim is gated on that field, never on
   coverage. A layer can be fully covered and still barred.

3. **Question is not limb.** The merge threshold is applied to
   `containment_low`. A pair high one way and low the other is a subset, and
   merging on the high side is how a limb's sitting count becomes a whole
   question's. Families joined by `WHOLE_VS_LIMB_RELATION` share no occurrence.

4. **Recurrence is not currentness.** A twelve-time repeat can be obsolete.
   They are computed from different inputs and currentness may never move a
   count. `UNKNOWN` is not `CURRENT`; it means nobody checked.

### If you change the corpus

Adding or editing a question changes the candidate proposals, which breaks the
pinned `reviewed_proposal_digest` and stops the build. That is deliberate: a
changed proposal set means the recorded semantic review no longer describes
what would be merged. Re-review the affected groups, then re-pin.

The full Phase-1 account, including the Top-25 Founder list, is
`docs/study/QI_PHASE1_REPORT.md`.

## QI -> study: one adapter, two layers, one weight

MIW holds **two** question-intelligence layers and they are complementary. The
integration mistake to avoid is not "which one wins" -- it is letting both
vote.

| Layer | Horizon | What it is good at | Where it lives |
|---|---|---|---|
| **Modern question-level QI** | 2021 -> Aug 2026 | *Which* modern questions relate, and how. High precision, limb-aware. | `meoclass1/pastpapers/specs/*.json` (`host_recurrence_hint`, `recurrence_class`, `reuse_tier`, `reused_from`, `question_delta`, `cross_links`) and `meoclass1/pastpapers/intelligence/derived/sixyear_families.json` |
| **Canonical longitudinal QI** | 2010 -> Aug 2026 | *How far back* a concept goes, and whether it is persistent, rising, dormant or re-emerging. | `docs/study/qi/*` |

```
modern QI  +  canonical QI  +  study mappings
                   |
        tools/study/study_qi_adapter.py        <- the ONLY join
                   |
        docs/study/study_qi.json
                   |
   topics / roadmap / cohorts / workbook / internal study page
```

| Path | Role |
|---|---|
| `tools/study/study_qi_adapter.py` | **The library.** Loads both layers, reconciles them, projects questions/topics/roadmap input. Read its docstring first. |
| `tools/study/build_study_qi.py` | **Only writer** of `study_qi.json` and `modern_qi_baseline.json`. `--check` proves disk matches inputs. |
| `tools/study/study_qi_holds.json` | **Hand-maintained.** Governed holds: modern/canonical conflicts, wording-only topic gaps, known authored-edge defects. |
| `tools/study/validate_study_qi.py` | The gate. 35 checks, fails closed. |
| `tools/study/test_study_qi_mutations.py` | 19 mutations, all must be caught, zero residue. |

```bash
python tools/study/build_study_qi.py            # rebuild
python tools/study/build_study_qi.py --check    # stale?
python tools/study/validate_study_qi.py         # the gate
python tools/study/test_study_qi_mutations.py   # prove the gate bites
```

### The five rules that are easy to break

1. **One weight, two views.** A modern repeat tag and a canonical family are
   usually the *same evidence stream seen twice*. The adapter emits exactly
   ONE recurrence quantity per topic (`RECURRENCE_WEIGHT_SOURCE =
   CANONICAL_QI_FAMILY`); the modern layer contributes precision fields that
   carry no weight. `roadmap_recurrence_by_topic()` is the only entry point a
   priority model may call, deliberately, so there is no way to reach in and
   add a second quantity. `R-WEIGHT-*` gates it.

2. **Precedence is earned, not assumed.** Modern evidence is `AUTHORED`
   (a human wrote it into a spec), `DETERMINISTIC` (identical normalised
   stems), or `INFERRED` (a similarity threshold nobody adjudicated). Modern
   wins for modern question identity where its evidence is authored or
   deterministic. Canonical adjudication wins over `INFERRED`. That asymmetry
   holds only because **every** deterministic modern family agrees with the
   canonical layer and every disagreement observed is inferred. `R-PRECEDENCE`
   fails the build the day that stops being true -- re-argue the rule then,
   do not relax the gate.

3. **A family votes once, through one question.** `canonical_current_question`
   picks the most recent solved modern member as the bearer; every other
   member is a `historical_variant` carrying zero weight. Without this an
   eight-member family votes eight times and historical bulk drowns current
   relevance. This is why production order differs from the Phase-1 preview --
   see the deprecation notice in `preview_qi_study_impact.py`.

4. **Recurrence is not readiness.** A twelve-time repeat carrying a currentness
   risk is high importance AND blocked. `UNSAFE_CURRENTNESS` overrides a
   cheerful Phase-2 action, never the reverse. `R-READY-SAFE`.

5. **`recurring_families` and `largest_families` are different populations.**
   In `study_spine.json`, `recurring_families` is the canonical 2010-2026
   weight; `largest_families` holds MIW short-title labels over the SOLVED
   corpus only, and those strings are **printed on the public page**. They may
   never be merged: QI family labels are raw question stems carrying
   secondary-claimed dates, and the public card already says "96 solved
   Written questions across 39 papers" beside them. Two denominators under one
   heading is the defect. `current_written_recurrence_families` in the
   workbook model is the public-safe, solved-corpus figure;
   `longitudinal_recurrence_families` is the internal one.

### Holds are finished work, not backlog

Same rule as the mapping review queue. A `HOLD_RECONCILIATION` means a human
read a modern/canonical disagreement and recorded that the evidence does not
settle it. Resolving one changes what a recurrence relationship *means*, so no
build may do it: `R-CONF-HELD` refuses a conflict with no hold, and
`R-CONF-HUMAN` refuses a resolution with no named adjudicator.

`known_authored_edge_defects` is an allowlist of individually named broken
`host_recurrence_hint` references -- pre-existing corpus defects, recorded so
the dangling-edge gate stays sharp for new breakage instead of being switched
off. `R-EDGE-ALLOW` fails if an allowance outlives the defect it excuses.

### Do not build a fourth recurrence engine

Before this integration the repository had **three**: `build_study_spine.py`
grouped by exact `short_title`, `build_sixyear_intelligence.py` clustered
2021-2026 stems, and `build_qi.py` adjudicated 2010-2026 families. They
disagreed, and the roadmap read the weakest of the three. If you need a
recurrence number, call the adapter. If the number you need is missing, extend
the adapter -- do not compute it where you stand.

## Phase 2 -- from "what recurs" to "what is true now"

Phase 1 says what keeps coming back. Phase 2 says whether a candidate can
safely study it **today**, and that is the dangerous question: getting it
wrong does not look like a bug, it looks like a confident, current, wrong
answer.

| Path | Role |
|---|---|
| `tools/study/qi_phase2_adjudications.json` | **Hand-maintained, and the RATIFIED owner of present-day family decisions.** One record per family. Same family id space as `qi_phase1_adjudications.json` and `study_qi_holds.json`. Full ownership statement: `docs/study/PHASE2_PRESENT_DAY_LAYER.md`. |
| `tools/study/validate_phase2_tranche.py` | The gate. 37 invariants, fails closed. |
| `tools/study/test_phase2_mutations.py` | 16 mutations, all must be caught, zero residue. |

### A new answer has nowhere to live -- read this before planning a tranche

Tranche 002 was weighted six-of-twelve toward `NEW_MODERN_ANSWER_REQUIRED` to
price the creation of a present-day answer. **One of the six resolved.** The
other five could not be, at any price, and the reason is structural:

- all 37 `NEW_MODERN_ANSWER_REQUIRED` families have their newest member in
  **2021 or 2022**, and those are WORDING-ONLY records;
- `spec_question_ids()` builds the nameable-answer set **only** from
  `meoclass1/pastpapers/specs/*.json`, which is the SOLVED 2023-2026 set;
- `historical_qp_intelligence.json` forbids authoring an answer for those
  sittings without a separate Founder decision.

So do not plan a tranche around converting new-answer families until a Founder
decision and an answer container exist. The families that CAN convert are the
ones a governed `WHOLE_VS_LIMB` join already points at a solved successor --
check `qi_family_joins.json` before selecting.

Three invariants added with that tranche, and the middle one was catching a
live defect: `R-P2-NEW-ANSWER-BIAS` (a declared new-answer minimum is checked
against the action PINNED at selection), `R-P2-HOLD-REACHES-ANSWERS` (a HOLD
must reach the solved answers inside the held family -- the inverse of
`R-P2-ANSWER-SCOPE`), and `R-P2-HOLD-REASON` (a hold with no reason is backlog
in a hold's clothes).

```bash
python tools/study/validate_phase2_tranche.py
python tools/study/test_phase2_mutations.py
```

### The rule the whole product rests on

**MIW Written answers are SITTING-ANCHORED.** Every answer must be true as at
the date of its own examination sitting, not as at today
(`TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md` s1). That governs what Phase 2
may and may not touch, and the distinction is not a nicety:

| Situation | Class | What you do |
|---|---|---|
| The answer was already wrong **at its own sitting** | `CORRECTION` | Edit `model_answer`. This RESTORES sitting-anchoring. |
| The framework moved **after** the sitting | `MODERNISATION` | Leave the answer alone. Record the present-day position in the family record. |

`R-P2-MODERNISATION-NOEDIT` fails the build if a record classed as a
modernisation also claims to have edited a past paper. Collapsing the two
would make a February 2026 paper cite law that did not govern it, which is
worse than the staleness being fixed.

### Readiness is earned, never asserted

`READY_TO_STUDY_NOW` is a consequence, not a field. A Phase-2 record only
clears a currentness block if it carries **all** of: a safe final state, dated
current primary authority, an independent review that passed, and a canonical
answer that resolves to a real question. Hollow out any one and the grant
evaporates (`R-P2-EARNED` inputs, gated by `R-P2-AUTHORITY*`, `R-P2-REVIEW*`,
`R-P2-ANSWER*`). `validate_study_qi.R-READY-SAFE` honours that exemption and
nothing else -- the triage value in `qi_currentness.json` is never rewritten,
because Phase 1 is an input here.

### A grant reaches ONE answer, not a family

This is the mistake tranche 001 actually made before it was caught. Resolving
`QIF-EM-0017` initially marked `QP2402-Q5` ready -- a February 2024 answer to
a question about *ongoing developments*, whose own record says in terms that
it must never be reused at a later sitting -- while the successor it had been
superseded by still read `VERIFY`. Exactly backwards.

`study_qi_adapter.question_readiness()` therefore grants Phase-2 readiness
only to the question the record NAMES as `canonical_current_answer`; every
other member keeps its triage verdict. `R-P2-ANSWER-SCOPE` gates it. A family
being sorted out is not the same as every sitting inside it being safe.

### Recurrence is an input and the manifest proves it

Each tranche pins the counts it selected on into `pinned_at_selection`, and
the gate compares the pins with the live layer (`R-P2-PIN-*`, `R-P2-MODERN`).
So the manifest is self-policing: altering a recurrence count or dropping
modern repeat metadata during answer work is caught, not inherited.

### Working a tranche

1. Select from `qi_phase2_action_queue.json` in `phase2_rank` order, skipping
   anything already `READY_TO_STUDY_NOW`. Freeze the list.
2. Read the actual question and answer text. Labels lie; the D01 cue and the
   NEAR_REPEAT clusters both prove it.
3. Verify against current primary authority appropriate to the question --
   IMO for a convention, the Gazette for an Indian statute, OEM or naval
   architecture for a machinery concept. Do not put DGMA first reflexively.
4. Classify CORRECTION vs MODERNISATION and act accordingly.
5. Record authority, dates, review verdict and final state.
6. `python tools/study/build_study_qi.py` then the two Phase-2 commands above,
   then the normal study gate sequence.

**Only adjudicate a conflict hold if it blocks a family you selected.** The
other holds are finished work, not backlog.

## Candidate-facing projection -- three layers, one artefact

Backend intelligence that no candidate can see is not a product. But the three
things MIW now knows are answers to three DIFFERENT questions, and the whole
risk of showing them is that they read as one.

| Layer | Question it answers | Owner |
|---|---|---|
| 1 MODERN RECURRENCE | "Within the sittings MIW has transcribed, has this exact examiner task come back?" | `tools/pastpapers/recurrence_model.py` -- from the CALENDAR |
| 2 LONGITUDINAL SIGNAL | "Over 2010->Aug-2026, how persistent is this concept?" | `docs/study/qi/*` via the adapter |
| 3 ANSWER READINESS | "Is MIW's current answer safe to study TODAY?" | the Phase-2 present-day layer |

```
study_qi.json + qi_families/qi_occurrences + phase2 store
                        |
            tools/study/qi_projection.py       <- chooses every candidate string
                        |
            docs/study/safe_qi_projection.json
                        |
   year sheets / solved papers / topics / study / workbook
```

| Path | Role |
|---|---|
| `tools/study/qi_projection.py` | **The library.** Tier whitelists, the closed label vocabulary, and `render_block()` -- the shared markup every candidate surface emits. |
| `tools/study/build_qi_projection.py` | **Only writer** of `safe_qi_projection.json`. `--check` proves disk matches inputs. |
| `tools/study/validate_qi_projection.py` | The gate. 14 invariants over the ARTEFACT and the SHIPPED BYTES. Fails closed. |
| `tools/study/test_qi_projection_mutations.py` | 12 mutations, all must be caught, zero residue. |

```bash
python tools/study/build_qi_projection.py            # rebuild
python tools/study/build_qi_projection.py --check    # stale?
python tools/study/validate_qi_projection.py         # the gate
python tools/study/test_qi_projection_mutations.py   # prove the gate bites
```

### Four rules that are easy to break

1. **Layer 1 is not sourced from here.** The candidate-facing modern tag is
   computed from the calendar by `recurrence_model.py`. It is NOT
   `study_qi.json`'s `modern_recurrence_class`, which is the AUTHORING field --
   `recurrence_model.py` names three questions in the 2026 set where the two
   say opposite things. Because this projection never touches Layer 1, "no
   modern tag was lost" is true by construction, not by test.

2. **A label must survive its own evidence.** The 2010-2020 band is
   `SECONDARY_CLAIMED`. `RE_EMERGING` is a statement about WHEN wearing an
   adjective, so a qualitative label can smuggle a barred dated claim through.
   Every family is therefore labelled TWICE by the SAME engine
   (`qi_model.intelligence_labels`) -- over all governed occurrences, and over
   printed-on-source-copy occurrences alone. Only labels surviving the second
   pass reach a candidate. Reach beyond that renders as
   `WIDER_RECURRENCE_HELD`: MIW holds more, and says nothing about when.
   QIF-EM-0220 is the worked case (2010-04 claimed + 2026-08 printed).

3. **"Ready" is not "verified".** 82 families are ready; ten carry a governed
   Phase-2 record. The rest are ready because triage fired no risk -- an
   absence of signal, not a check. `readiness_basis` chooses the wording and
   only `PHASE2_GOVERNED_REVIEW` earns the word "verified".

4. **Phase-1 triage does not veto Phase 2.** A question may read
   `READY_TO_STUDY_NOW` while its family triage still says
   `CURRENTNESS_REVIEW_REQUIRED`; the triage value is frozen on purpose. The
   unsafe-currentness guard is exempted for -- and only for -- the question a
   governed record NAMES. See `PHASE2_PRESENT_DAY_LAYER.md`.

### Tiers are whitelists, not filters

`PUBLIC` gets the longitudinal signal only; `GATED` adds currentness and
readiness; `INTERNAL` adds counts, family ids, both label sets and the Phase-2
action. A field added to the internal record is absent from the others until
someone deliberately adds it -- which is why `SQ/study-roadmap.html` rebuilt
byte-identical when topic readiness landed: `PUBLIC_TOPIC_FIELDS` dropped the
new fields without anyone naming them.

### Rebuild order

The projection reads `study_qi.json`, so it is built after it and before any
page:

```bash
python tools/study/build_study_qi.py
python tools/study/build_qi_projection.py
python tools/study/export_roadmap_xlsx.py
python tools/study/build_topic_pages.py
python tools/pastpapers/run_toolchain.py --publish     # NOT --gated
python tools/study/validate_qi_projection.py
python tools/study/test_qi_projection_mutations.py
```

**`--publish`, and not `--gated`.** The committed review copies under
`meoclass1/pastpapers/` carry `index, follow` and JSON-LD; rebuilding without
`--publish` silently flips forty papers to `noindex` and strips their
structured data. `--gated` is a separate hazard already recorded. Determine the
mode from the committed bytes, never from habit.

## Fresh-session test

A new Claude Code session can, using only this file:

1. read this contract and `SYLLABUS_SOURCE_STATUS.md`;
2. ingest a new Oral or Written question into its corpus file;
3. run one documented command (`build_study_mappings.py`);
4. obtain the topic candidate and its confidence;
5. see whether review is required — `mapping_review_queue.json`;
6. commit the governed mapping (`study_mappings.json`);
7. regenerate affected indexes (`build_study_spine.py`).

**Answer: YES**, with one known gap — step 3 is not yet *automatically*
invoked by the Oral release runner, so an oral author must run it explicitly
until the TODO above is wired. Nothing else is missing.
