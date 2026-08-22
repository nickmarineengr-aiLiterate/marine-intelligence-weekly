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
showing this pattern. It is regenerated every build, so it cannot rot. The engine **never** copies a "similar" question's
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
