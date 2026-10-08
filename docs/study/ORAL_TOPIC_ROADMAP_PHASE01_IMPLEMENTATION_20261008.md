# ORAL TOPIC ROADMAP — PHASE 0 + PHASE 1 IMPLEMENTATION RECORD (2026-10-08)

**Status:** IMPLEMENTATION CANDIDATE — local commits only, push disabled, NOT published, NOT deployed.
**Authority:** Founder instruction "PHASE 0 + PHASE 1 CONTROLLED IMPLEMENTATION" (FD-ROADMAP-1..7) and the Notes-deferral note, both 2026-10-08.
**Audit this implements:** `docs/study/ORAL_TOPIC_ROADMAP_FEASIBILITY_AUDIT_20261008.md`.
**Out of scope and not started:** Phase 2 (mapping adjudication), Phase 3 (subtopics), Phase 4 (relationships / families), Phase 5 (sequence / public expansion).

---

## 1. Starting commit and workspace

| Item | Value |
|---|---|
| Repository | `nickmarineengr-aiLiterate/marine-intelligence-weekly` |
| Audit base | `6ce00b5b8f4b74ae2a9f543959b128cfede3573d` |
| `origin/main` at start (fetched 2026-10-08) | **`8083e590f17d2817b90dfa62e30fbda1e6c77cfc`** — moved by exactly one commit, "Add Engineering Management Notes Part 26" (Notes files + `tools/notes/specs/p26.json` only; no Oral, study or QB file) |
| Implementation clone | `J:\AI-Sandbox\MIW\ORAL-Topic-Roadmap-Phase01\repo`, fresh `git clone` from GitHub, branch `oral-roadmap-phase01-20261008` |
| Push | disabled: `remote.origin.pushurl = DISABLED_NO_PUSH` |
| Quarantined checkout | `…\reconciliation-candidate-2026-09-19\marine-intelligence-weekly` @ `b911dd3` — not developed on; only `git fetch` run there |
| Comparison worktree | `J:\AI-Sandbox\MIW\ORAL-Topic-Roadmap-Phase01\base` (detached `8083e59`) used to classify every failure as pre-existing or new |

Baseline at `8083e59` before any change: release gates `study_mapping_check` **FAIL** (store stale) and `study_spine_validate` **FAIL** (R-GRAN-CORPUS-STABLE 1121≠1130; R-GAP-NO-NEW-QUESTIONS 360≠369) — both caused by the QP2609 staleness the audit found.

## 2. Current corpus counts (candidate HEAD)

| Measure | Value |
|---|---|
| Canonical Oral questions / files | **761 / 86** (unchanged; `build_qb_content_index.py --check` current) |
| Oral mapping: VALID_MAPPED / REVIEW_PENDING / ACCIDENTALLY_UNMAPPED | **653 / 66 / 42** (unchanged) |
| Mapping review queue | **108** (94 unadjudicated, 14 human-held) — unchanged |
| Written questions / papers | **369 / 41** (was 360 / 40 in the study layer) |
| Mapping store | **1,130** records (was 1,121) |
| Examiner pairs (study input) | **958** pairs / **671** questions / **7** examiners |
| Official nodes / crosswalk edges / domains | 25 / 43 / 10 (unchanged) |

## 3. Phase 0 actions

1. `build_study_mappings.py` (incremental, unchanged tool) → QP2609 Q1–Q9 added (§5).
2. Examiner source reconciled and the study layer moved onto one contract (§4).
3. Notes artefacts measured, not regenerated (§6).
4. Stale counts classified; one study-lane comment corrected (§7).
5. Study chain rebuilt with committed tools in the SKILL order:
   `reconcile_official_mappings` → `build_study_spine` → `build_coverage_matrix` → `build_evidence_horizon` → `build_syllabus_gap_register` → `build_topic_pages` → `build_public_study_roadmap`.
   The spine needs the gitignored Written derived layer; it was produced locally with the governed `tools/pastpapers/build_sixyear_intelligence.py` and `sixyear_temporal_and_topics.py` (output gitignored, not committed).
6. **Roadmap workbook NOT committed.** `export_roadmap_xlsx.py` ran (exit 0), but its pack hyperlinks are absolute machine-local `file:///` paths by design (`study_links.py:161`, "Nixon's local study pack"). The committed workbook carries `file:///F:/Marine-Intelligence-Weekly/…`; a sandbox build would replace that with a sandbox path. The workbook was restored to its base bytes and must be regenerated on the owner machine (`python tools/study/export_roadmap_xlsx.py`). No release gate covers it.

Priority rank and study order: **unchanged for all ten domains** (D03 #1, D01 #2, D02 #3 … D08 #10). Scores moved in the third decimal.

## 4. Examiner reconciliation outcome (FD-ROADMAP-4)

### 4.1 What each artefact is (from committed code)

| Artefact | Generator | What it is |
|---|---|---|
| `CURRENT_EXAMINER_RELATIONSHIPS.jsonl` (860 pairs, 649 Q) | `tools/oral/recover_relationships.py` — one-time "Phase 2 step 1" recovery of the then hand-uploaded `examiner-index.html` into a ledger (last written 2026-08-23, 721-question corpus) | The **recovery ledger**; carries `research_best_tier` per pair |
| `EXAMINER_INDEX_SNAPSHOT.json` (958 pairs, 671 Q) | `tools/oral/build_examiner_index.py` (gate `examiner_check`, validator `validate_examiner_index`, 54 checks) | The **resolved product snapshot**: the ledger + `QCARD` card attributions + `RELEASE_A` publication + `CE_TIP_REVIEW` decisions; both `meoclass1/examiner-index.html` and `SQ/examiner-index.html` render from it |

Why the counts differ: the snapshot is built **from** the ledger and adds governed evidence the ledger predates. Re-running `recover_relationships.py` against today's generated index would be circular (it would recover the product back into its own input), so the ledger is **not regenerated**; it remains the upstream record.

### 4.2 Reconciliation (`docs/study/ORAL_EXAMINER_SOURCE_RECONCILIATION_20261008.json`, generated by `tools/study/report_examiner_source_reconciliation.py`, `--check` current)

One row per (canonical_id, examiner) with provenance, evidence tier, ledger tier, presence in each source and disposition.

| Disposition | Pairs |
|---|---|
| CARRIED_FORWARD (in both, same tier) | 854 |
| CARRIED_FORWARD_RETIERED (Release A evidence moved the tier) | 6 |
| ADDED_BY_RELEASE_A | 84 |
| ADDED_BY_QCARD | 8 |
| ADDED_BY_CE_TIP_REVIEW | 6 |
| DROPPED (ledger pair missing from snapshot — fails the report) | **0** |

Pairs by tier (snapshot): **confirmed 459 · reported 44 · ce_tip 214 · header 30 · inferred 211**.
Questions by strongest tier: confirmed 435 · reported 13 · ce_tip 150 · header 0 · inferred 73; **90** canonical questions have no pair.

Per examiner (pairs: confirmed / reported / ce_tip / header / inferred):
Nair 354 (168/8/93/7/78) · Simon 284 (176/14/59/5/30) · Srivastava 104 (15/0/8/5/76) · Rajappan 103 (55/0/30/6/12) · Senthil 67 (27/0/20/5/15) · Paul 33 (18/10/3/2/0) · John 13 (0/12/1/0/0).

The snapshot contains **no August-2026 intake and no panel-level attribution** (0 `AUG-` references in Release A); panel evidence was not merged into any tier.

### 4.3 Unresolved portion (fails closed, not synthesised)

The **40 cards added since the 721 corpus** (2026-08-24 → 09-02, H-series production) have **no examiner pair in either source**. Their examiner provenance exists only in the August intake, which is governed as an isolated lane (`isolated_from_historical_788: true`) and is 271/283 panel-level. No pair was inferred for them. They are among the 90 questions with no examiner record, and the topic page says so per topic.

### 4.4 The contract

`tools/study/examiner_source.py` is the only examiner loader in `tools/study`. It reads the snapshot, keeps tiers distinct, takes labels/meanings from `tools/oral/examiner_index_config.json` (the Examiner Index's own vocabulary), and **fails closed** if the snapshot was not built over the live corpus, names a non-live question, repeats a pair, or carries an unknown tier. `build_study_spine`, `build_coverage_matrix`, `export_roadmap_xlsx` and `build_topic_pages` read through it (their old fail-open `os.path.exists` fallbacks are removed). Topic → examiner → question (study) and examiner → topic → question (Examiner Index) are now projections of the same rows. The spine's `oral_questions_with_evidence` keeps its documented any-tier denominator for the priority weight and now sits beside `oral_questions_by_strongest_tier`. `validate_study_spine` R-ORAL-NONMUT also pins the snapshot.

## 5. Written mapping refresh outcome

`build_study_mappings.py` (incremental): `added 9, skipped 1121`. QP2609 Q1–Q9 → D01, D02, D05, D03, D01, D06, D03, D03, D05; all **VALID_MAPPED / HIGH / GOVERNED_FIELD**, TOPIC_LEVEL, CROSSWALK_ALIGNED. None entered review. No Oral record moved. `build_study_mappings.py --check`: current.

## 6. Notes freshness (FD Notes-deferral)

| | Value |
|---|---|
| Live Notes extent on main | Engineering Management Notes Parts 1–26 (`notes_content_index.json` total_files 35); Simon Notes p1–p8; WA series; Current Topics p1 |
| Frozen `ORAL_NOTES_UNITS.jsonl` | **992** units, 35 files, last written 2026-08-18 |
| Live units (same governed builder `oral_notes.build_units()`, run in memory, nothing written) | **1,095** units, 39 files |
| Delta | **+103 units, all from `miw-notes-mgmt-p23…p26`**; 0 units removed; no existing file's unit count changed |
| Oral↔Notes coverage (frozen) | 788 source asks; notes support for 373 canonical questions |

**Not regenerated, by governance.** `tools/oral/correction_corr_india_oilspill_regulatory_audit_20260917_manifest.json` records `ORAL_NOTES_UNITS.jsonl` as "a frozen audit snapshot … left as history per the 7b22475 precedent", and its generator `ingest_oral_notes.py` feeds `reconcile_788` → `report_notes_impact` → the Phase 2A-iii final package (Release A, P0, movement) that the published Examiner Index reads, under the `determinism` gate. Regenerating it is an Oral-release action, not Phase 0 freshness. Per the Notes-deferral note, current coverage is not treated as final.

Impossible without the later consolidated Notes layer: Notes → D-topic placement (all 992/1,095 units are AMBIGUOUS in the gap register), topic-level "related Notes", and any Notes coverage figure for Parts 23–26 or Lohan Notes. Deferred until LOHAN COMPLETE + UDAY COMPLETE + DGMA/NOTES GAP AUDIT COMPLETE + MIW GAP NOTES PRODUCED.

## 7. Stale-count disposition (721 / 862)

No global replace. Generated current-state outputs were regenerated (no generated study output now carries 721 or 860/862).

| Location | Class | Action |
|---|---|---|
| `tools/study/build_public_study_roadmap.py:100` "30 stems of 721" | COMMENT ONLY (study lane) | corrected to "30 stems across 10 topics" |
| `tools/study/mapping_engine.py:657` "does not reprocess 721" | COMMENT ONLY (illustrative) | kept |
| `tools/oral/oral_release_gates.py:215` note "86 files / 721 questions" | GATE DESCRIPTION (91+1 registry) | **reported, not edited** — registry is not modified by this work |
| `tools/oral/build_examiner_index.py:21` "the 862 published relationships" | COMMENT ONLY (Oral lane) | reported, not edited |
| `tools/oral/SKILL.md:1034` "Canonical Oral questions **721**" | CURRENT-STATE CLAIM (Oral-lane operational doc) | reported for the Oral lane owner |
| `tools/oral/SKILL.md:260-261, 868, 1072` | HISTORICAL — KEEP (lessons / dated figures) | kept |
| `docs/study/STUDY_ROADMAP.md` (721, 862) | DEPRECATED DOCUMENT | kept |
| `docs/ORAL_FOLLOWUP_REGISTER.md:151, 235` | HISTORICAL — KEEP (register pinned to source blobs) | kept |
| `examiner-audit/*` batch/enrichment/intake records, `tools/oral/batch_*`/`correction_*` manifests, `validate_*`/`mutate_*` comments, test fixtures | HISTORICAL — KEEP | kept |

## 8. Phase 1 UI / data changes (`meoclass1/topics.html`, gated)

All generated by `tools/study/build_topic_pages.py`; D01–D10 remains the only top level; no `subtopic_id`, no sequence field, no new taxonomy, no curated list.

* **Placement disclosure (5.1).** Summary bar: "761 oral questions in the bank · 653 placed in a topic · 108 still being placed". Only VALID_MAPPED questions are listed under a topic. A topic with questions under review shows only a count ("+N awaiting confirmation" and "N more question(s) may belong here …"), never the questions. The 66 under review and 42 unassigned are listed once, together, in a topic-free section **"Not yet placed in a topic"** ("in the question bank and answered in full — their study topic is still being confirmed"; 66 being reviewed / 42 not yet assigned). No internal status names appear. An unknown mapping status fails the build. Verified: **0** uncertain questions listed under a topic.
* **Examiner evidence by tier (5.2).** Every examiner name carries its own tier label, e.g. "Nair (Confirmed), Simon (Inferred)", with the tier's meaning as a tooltip; a legend states all five meanings verbatim from the Examiner Index config. Each topic shows: "Examiner records for the N placed questions, counted once per question by its strongest record: 46 Confirmed · 2 Reported · 14 CE Tip · 13 Inferred · 1 with no examiner record" (D01 example). Denominator stated in the footer. No recency claim.
* **Natural identity order (5.4).** Within each list: file by `natural_file_key` (reused from `build_examiner_index.py`: QB1 < QB2 < QB10), then question number (q1 < q2 < q10). D01 now opens `QB1_A#q19 … QB1_A#q23, QB1_B#q5, QB1_B#q7, QB1_B#q16` (previously q16 before q5). Footer: "question-bank order … not a ranking or a suggested learning sequence".
* **Return anchors (5.3, generated half only).** Every list row carries `id="oq-<file>-<qN>"` (761 unique ids, highlighted on `:target`) so a future card link can land on the exact row.
* `study.html` changes only by the shared stylesheet; `SQ/study-roadmap.html` changes only in numbers (§9).

### 8.1 Card → topic backlink — STOPPED for review (5.3)

QB pages share no script or stylesheet (only the GA4 loader); every QB page is a hand-authored canonical card file, no generator writes inside them, the release runner protects them as `PRODUCT_GUARDED_GLOBS` (`meoclass1/QB*.html`), and the H7 lane edits them. A backlink therefore cannot be generated without modifying 86 canonical cards. **Not done.** Minimum alternative for Founder review:

1. `build_topic_pages.py` additionally emits one gated generated file, e.g. `meoclass1/study-topic-map.js`: `canonical_id → {topic_id, topic_name, return anchor}` for VALID_MAPPED questions only (REVIEW_PENDING / unmapped absent, so no topic is asserted), covered by the existing `study_pages_check` `--check` (no new gate).
2. A one-time governed applier adds **one identical `<script src="study-topic-map.js" defer>` line** to each QB page, executed under the Oral correction/manifest regime **after H7 lands**, with a validator that the line is the only diff per file.
3. The script inserts "Study topic: Dnn — name" into each card header, linking to `topics.html#oq-<file>-<qN>` (the anchors this candidate already ships).

This is a new generated artefact and a card-template change; both need Founder authorisation before any release-registry discussion.

## 9. Files changed (`8083e59..HEAD`)

| File | Kind |
|---|---|
| `docs/study/study_mappings.json` | generated (`build_study_mappings`) |
| `docs/study/study_spine.json` | generated |
| `docs/study/coverage_matrix.json` | generated |
| `docs/study/written_evidence_horizon.json` | generated |
| `docs/study/syllabus_gap_register.json`, `docs/study/gap_production_queue.json` | generated |
| `meoclass1/topics.html`, `meoclass1/study.html` | generated (gated) |
| `SQ/study-roadmap.html` | generated (public) — numbers only |
| `docs/study/ORAL_EXAMINER_SOURCE_RECONCILIATION_20261008.json` | generated dated record (new) |
| `tools/study/examiner_source.py` | new code — examiner contract |
| `tools/study/report_examiner_source_reconciliation.py` | new code — reconciliation report (`--check`) |
| `tools/study/build_study_spine.py`, `build_coverage_matrix.py`, `export_roadmap_xlsx.py`, `build_topic_pages.py` | code |
| `tools/study/validate_study_spine.py` | code — one more pinned non-mutation source |
| `tools/study/build_public_study_roadmap.py` | comment only |
| `docs/study/ORAL_TOPIC_ROADMAP_FEASIBILITY_AUDIT_20261008.md` | adopted audit (provenance header only) |
| `docs/study/ORAL_TOPIC_ROADMAP_PHASE01_IMPLEMENTATION_20261008.md` | this record |

Not changed: any `meoclass1/QB*.html`, `qb_content_index.json`, examiner-audit inputs, `CURRENT_EXAMINER_RELATIONSHIPS.jsonl`, `EXAMINER_INDEX_SNAPSHOT.json`, `examiner-index.html`, follow-up register, `oral_release_gates.py`, `run_oral_release.py`, middleware/api/vercel config, Notes, H7/H8/H9 material, `MIW_MEO_Class1_Study_Roadmap.xlsx`.

### Public semantic scope (FD-ROADMAP-6)

`SQ/study-roadmap.html` diff is numeric only: Written 360→369, papers 40→41, date 2026-08-24→2026-09-23, per-topic written/paper counts, examiner-evidenced Oral counts and distinct examiners from the reconciled source, two recurrence-label multiplicities. Field whitelist (`PUBLIC_TOPIC_FIELDS`), the 3-stem/topic sample (30 stems) and `assert_public_safe` are untouched; `study_public_roadmap_check` PASS. Known limitation for the Founder (not changed, FD-6): the public sentence "tied to a named examiner by recorded evidence" counts questions at any tier, including Inferred.

## 10. Tests and gates

All in the implementation clone at candidate HEAD unless marked BASE (`8083e59` worktree).

| Command | Exit | Result |
|---|---|---|
| `python tools/study/validate_study_spine.py` | 0 | all PASS (BASE: 1, 4 FAILED) |
| `python tools/study/test_mapping_engine.py` | 0 | all 132 PASS |
| `python tools/study/test_syllabus_fanout.py` | 0 | all PASS |
| `python tools/study/build_study_mappings.py --check` | 0 | current (BASE: 1, STALE) |
| `python tools/study/build_topic_pages.py --check` | 0 | 2 pages up to date |
| `python tools/study/build_public_study_roadmap.py --check` | 0 | up to date, 30 stems |
| `python tools/study/report_examiner_source_reconciliation.py --check` | 0 | current |
| link integrity (script over `topics.html`) | — | 761 rows, 761 unique ids, **0** broken card links |
| `python tools/study/test_study_expandability.py` | 1 | **PRE-EXISTING** (BASE 1): literal `1081 mappings` and summary checks fail at base; one further literal now fails, `papers_total == 40 and questions_total == 360` — invalidated by mapping QP2609, not edited |
| `python tools/study/test_roadmap_cockpit.py` | 1 | **PRE-EXISTING** (BASE 1): D01 `STALE_PACK_CHANGED` sessions vs TOPIC_01 pack; base also fails on the machine-local `F:/` workbook links |
| `python tools/study/test_d01_priority_cohort.py` | 1 | **PRE-EXISTING**, identical at BASE: QB1_F#q23, QB1_K#q10 in no D01 cohort |
| `build_qi.py --check` / `build_study_qi.py --check` | 2 / 1 | **PRE-EXISTING**, identical at BASE: QI fails closed on QP2609 (`POST_UPPER_BOUNDARY_OCCURRENCE`, 2026-09 beyond the QI window). Window change is a QI governance decision — not done |
| `build_qi_projection.py --check` | 0 | current (558 Q, 270 families) |
| `run_oral_release.py --plan` | 0 | **91 gates** + determinism phase = 92 rows; 39 of historical 39 |
| `run_oral_release.py --category content-index --category examiner --category security --category health --keep-going` | 1 | 15 gates: **13 PASS, 1 FAIL, 1 UNAVAILABLE** (log `oral_release_20261008T071557Z`) |
| — `content_index_check` / `_validate` (24 checks) / `_mutate` | | PASS / PASS / PASS **26 mutations caught, 0 escapes** |
| — `study_mapping_check`, `study_spine_validate`, `study_pages_check`, `study_public_roadmap_check` | | PASS ×4 |
| — `examiner_check`, `validate_examiner_index` (54), `test_examiner_check` (10), `validate_ce_tip_review` (28) | | PASS ×4 |
| — `ce_tip_mutate` | | PASS **17 caught, 0 escapes** |
| — `examiner_mutate` | | UNAVAILABLE in the runner (also at BASE): mutation H writes into `docs/MIW-master-Question-bank/`, a local-only folder absent from a fresh clone. Re-run with that empty folder created then removed: **PASS, 13 caught, 0 escapes** |
| — `node_security_tests` (`node --test tools/security/*.test.mjs`) | | FAIL **PRE-EXISTING**, identical at BASE: 623/625 pass; `regulatory_facts.test.mjs` — Notes Parts 24/25 state a superseded MEPC ES.2 resumption ("October 2026"). Notes lane. All entitlement / deploy-surface tests pass |
| — `qb_health_check` | | PASS (363 findings = baseline 363, NEW 0) |
| determinism phase, batch/correction categories | — | **NOT RUN** (no input of theirs changed); not counted as PASS |

## 11. Remaining mapping debt (Phase 2, not started)

42 ACCIDENTALLY_UNMAPPED + 66 REVIEW_PENDING = 108 queue items (94 unadjudicated, 14 held); D10 has 26 of 33 under review; 25 FILE_TITLE_CONTRADICTED records; 490 TOPIC_LEVEL / 146 AMBIGUOUS granularity.

## 12. Known limitations

* No card → topic link yet (§8.1). Return from a card is via browser back or the topic page.
* 90 questions (incl. all 40 post-721 cards) show no examiner record; August intake evidence is not admitted (§4.3).
* Workbook not regenerated in the candidate (§3.6).
* Public examiner sentence counts all tiers (§9).
* Pre-existing failing tests above remain failing; Notes regulatory-facts failure belongs to the Notes lane.
* `tools/oral/SKILL.md` and the gate note still say 721 (Oral lane).

## 13. H7 interaction (FD-ROADMAP-7)

No canonical Oral card, content index, examiner input, manifest or release-registry file is touched, so the candidate cannot conflict with H7 card edits. If H7 lands first: rebase this branch on the new `main`, then rerun `build_qb_content_index.py --check`, `build_examiner_index.py` (via its owning lane), and the §3 study chain, and re-run §10 before declaring the candidate current. Expect `study_mapping_check` to report new H7 questions until `build_study_mappings.py` runs; new cards will appear under "Not yet placed" or their topic by mapping status, with no manual list edit.

## 14. Rollback

* Whole candidate: discard branch `oral-roadmap-phase01-20261008` (never pushed), or `git reset --hard 8083e59` in the clone.
* Phase 1 only: `git revert <phase-1 commit>` (topic page renderer + `topics.html`/`study.html`), keeping Phase 0.
* Phase 0 examiner contract only: revert the Phase 0 contract commit; the QP2609 mapping commit is independent and can stand alone.
* After any revert: `python tools/study/build_topic_pages.py --check` and `build_public_study_roadmap.py --check` must pass.
