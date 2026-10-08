# ORAL TOPIC ROADMAP: PHASE 2A IMPLEMENTATION RECORD (2026-10-08)

**Tranche:** 2A, D10 mapping-queue adjudication (26 items).
**Status at record time:** `ORAL ROADMAP PHASE 2A QUALIFIED — D10 MAPPING QUEUE ADJUDICATED (26/26 RULED, 0 FRESH IN D10, HOLDS VISIBLE) — READY FOR FOUNDER LANDING REVIEW`
**Local only:** two local commits on branch `oral-roadmap-phase2a-20261008` in the governed sandbox clone `J:\AI-Sandbox\MIW\ORAL-Topic-Roadmap-Phase2A\apply\candidate` (`remote.origin.pushurl = DISABLED_NO_PUSH`). Not pushed, not deployed.

## 1. Authority

- Founder / Lane A, 2026-10-08: "Phase 2A.1 proposal is ACCEPTED. Phase 2A.2 APPLY is now AUTHORISED."
- Approved proposal package: `ORAL_ROADMAP_PHASE2A_PROPOSAL_REVIEW_PACK_20261008.zip`, sha256 `a7b80e83dba8c2e706897e68fb461b0d5b0f9c06f5c555430361e84a968931a8` (re-verified before apply).
- Decisions in force: FD-P2-1 (Phase 2 = Oral mapping-queue adjudication in tranches 2A → 2B → 2C; 14 existing holds untouched); FD-P2-2 (reviewer `Nixon Antony`); FD-P2-3 (the three D10 sample swaps listed in §7 APPROVED; no other public stem change); FD-P2-4 (deferred; 2A has no D01 effect); FD-P2-5 (the 26 rulings in §3); FD-P2-6 (post-commit `validate_study_spine` must be ALL PASS); FD-P2-7 (applier-side gates A–D mandatory).
- Basis: `docs/study/ORAL_TOPIC_ROADMAP_FEASIBILITY_AUDIT_20261008.md` §19 (Phase 2 = "Adjudicate the 108-item queue, D10 first, through `adjudications.json`"); `tools/study/SKILL.md` adjudication contract.

## 2. Base

| Item | Value |
|---|---|
| `origin/main` at preflight (fetched 2026-10-08) | `78fa986085681f05eaa6f489270c7542a12982fa` (Notes Parts 27–29, 2026-10-08 18:48 +0530) |
| Moved since the 2A.1 proposal? | **No.** `78fa986..origin/main` empty |
| H7 on main | **No** (`tools/oral/batch_h7_manifest.json` absent) |
| Queue re-derivation | byte-identical to `PHASE2_QUEUE_BASELINE_78fa986_rederived.csv` and to the readiness `PHASE2_QUEUE_BASELINE_3b2075e.csv` (sha256 `45916b96…c688`): 0 drift in the 26 ids, card text, `mapper_topic_id` (D10) or queue state (AWAITING_ADJUDICATION) |
| Written derived layer | gitignored `sixyear_*.json` rebuilt with the governed tools; byte-identical to the 2A.1 copies |

## 3. The 26 Founder rulings

reviewer `Nixon Antony`, `last_reviewed` `2026-10-08`, `mapper_topic_id` `D10` (restated, per the guard). AFFIRM notes = the approved 2A.1 rationales verbatim; HOLD notes = the Founder's notes verbatim.

| # | canonical id | decision | topic / candidates |
|---|---|---|---|
| 1–5 | `QB1_C#q1`, `q2`, `q3`, `q4`, `q5` | AFFIRM | D10 |
| 6–8 | `QB1_D#q1`, `q6`, `q7` | AFFIRM | D10 |
| 9 | `QB1_E#q2` | AFFIRM | D10 |
| 10–11 | `QB1_G#q35`, `q39` | AFFIRM | D10 |
| 12 | `QB1_I#q3` | AFFIRM | D10 |
| 13 | `QB1_K#q3` | AFFIRM | D10 |
| 14–24 | `QB1_supplementary#q2`, `q9`, `q10`, `q11`, `q12`, `q13`, `q14`, `q15`, `q17`, `q18`, `q19` | AFFIRM | D10 |
| 25 | `QB1_C#q7` | **HOLD_REVIEW** | [D01, D03, D10]: "Structural damage assessment is D10, while reporting spans statutory/class and management obligations. No single domain safely dominates the whole question. Hold pending later evidence/refinement." |
| 26 | `QB3_B#q21` | **HOLD_REVIEW** | [D09, D10]: "Galvanic-corrosion theory and hull anodes support D10, while the seawater pump-anode limb is machinery-facing D09. Neither domain safely dominates the complete question. Hold pending later evidence/refinement." |

REASSIGN: **none** (none authorised). Every entry carries an explicit `decision` field.

## 4. Append proof and mandatory applier gates (FD-P2-7)

Pre-edit snapshot: 150 entries, file sha256 `3de2a13ea8f901b6a88ccfce03bda412fc76e29f39c2900c2cec55efb0f450ff`; per-entry canonical sha256 list kept with the package. Post-edit file sha256 `5e4ed19bae26b1377a89c60f71041f154776da3d79d855f58e6f94fa611efdc5` (blob `97a1961e`). Textually a pure append: no pre-existing line changed.

| Gate | Result |
|---|---|
| **A** append proof | **PASS**: 150 original entries deep-equal and canonical-hash-equal; key set +26 = exactly the ruled ids; 0 extra keys; top-level `note` / `schema_version` unchanged |
| **B** refusal scan | **PASS**: 0 × `REFUSED ADJUDICATION` in the complete `build_study_mappings` log (`adjudications: applied 160, reassigned 82, held 16, refused_topic_moved 0, refused_unknown_id 0`) |
| **C** schema | **PASS**: 26/26 new entries carry `decision`, `mapper_topic_id`, `reviewer`, `last_reviewed`, `note`; both HOLDs carry non-empty `candidate_topic_ids`; every entry equals the Founder ruling |
| **D** acceptance (rebuilt store/queue) | **PASS**: 24/24 AFFIRM ids VALID_MAPPED in D10 and out of the queue; `QB1_C#q7`, `QB3_B#q21` HELD_PENDING_EVIDENCE; fresh D10 = 0 |

## 5. BASE_REGEN_CATCHUP (current main, not Phase 2A)

The SKILL.md chain was run with unmodified builders on a disposable, unmodified `78fa986` copy. Its entire diff:

```
docs/study/study_spine.json   sources.notes_files  35 -> 38
```

Nothing else drifted. Cause: `78fa986` raised `meoclass1/oralnotes/notes_content_index.json` `total_files` without regenerating the spine, which records it as a resource counter; on main, `build_study_spine --check` is STALE for this reason. The candidate's `study_spine.json` is **byte-identical** to the base-regen spine, so Phase 2A contributes **nothing** to the spine. This one line is attributed to `78fa986`.

## 6. Before / after

| Metric | Before (`78fa986`) | After (candidate) |
|---|---|---|
| Queue total / fresh / held | 108 / 94 / 14 | **84 / 68 / 16** |
| D10 fresh | 26 | **0** |
| Oral placed (VALID_MAPPED; listed under a topic on `topics.html`) | 653 | **677** |
| D10 placed | 7 | **31** |
| D10 REVIEW_PENDING | 26 | 2 (the two holds; listed under "not yet placed") |
| `topics.html` rows / unique `oq-` ids / non-VALID listed under a topic | 761 / 761 / 0 | 761 / 761 / 0 |
| D01 membership | 77 | 77 (identical ids and statuses) |
| Priority ranks / study order | D03 1, D01 2, D02 3, D05 4, D04 5, D07 6, D09 7, D06 8, D10 9, D08 10 | **unchanged** |
| Gap register, gap production queue, C49-A3-04 (NODE_EVIDENCED_NO_GOVERNED_ANSWER; oral resolved 33) | — | **byte-identical** |
| `coverage_matrix.json`, `written_evidence_horizon.json`, `meoclass1/study.html`, `study_qi.json` | — | **byte-identical** |

Oral store footprint: exactly 26 records changed (= the ruled ids); changed fields ⊆ {mapping_status, last_reviewed, reviewed_by, review_note, mapping_basis, review_hold, adjudicated_candidate_topic_ids}; 0 `topic_id` changes; 1,130 records before and after.

## 7. Public sample swaps (FD-P2-3 approved)

| Topic / slot | OLD | NEW |
|---|---|---|
| D10 / 1 | `QB1_C#q9`: "A new ship is being designed and developed for your company. As Chief Engineer, what requirements would you ask the company to consider?" | `QB1_C#q1`: "Reserve buoyancy and the GZ curve?" |
| D10 / 2 | `QB1_D#q5`: "Load line — what is Fresh Water Allowance, how is it derived, and how do you apply it when loading in dock water?" | `QB1_C#q2`: "Static vs dynamic stability?" |
| D10 / 3 | `QB1_J#q1`: "Explain the procedure for hull paint coating inspection during drydock." | `QB1_C#q3`: "Tender vs stiff ship — problems of excessive stiffness?" |

Assertion: the swaps equal the approved set exactly; 1 topic changed; the other 27 stems unchanged. The word-level diff of `SQ/study-roadmap.html` = these six stems only; **0 count changes**; 0 changed tags. Public safety: `build_public_study_roadmap --check` (runs `assert_public_safe`) PASS; 0 `/meoclass1`, 0 `/solvedQP`, 0 public→gated links, 0 `answer-body`, 0 `q-answer`, 0 ce-tip / CE Oral Tip, 0 examiner names, 0 tier labels. Roadmap destinations: all 13 link rows on the page (the canonical self-link, `index.html`, `SQ/index.html`, `SQ/examiner-index.html`, `SQ/solved-qp-sample-january-2026.html`, `SQ/trial.html` ×2, `SQ/QB1_A.html`, `terms.html`, `privacy.html`, plus the analytics loader) resolve in the tree, with hrefs unchanged. Live 200/302 verification belongs to landing.

## 8. Gate matrix (compared with CURRENT MAIN `78fa986`)

| Gate | main | candidate pre-commit | candidate post-commit | Class |
|---|---|---|---|---|
| `build_study_mappings --check` | PASS | PASS | PASS | — |
| `reconcile_official_mappings --check` | PASS | PASS | PASS | — |
| `build_study_spine --check` | **STALE** | PASS | PASS | BASE_REGEN_CATCHUP (cleared) |
| `build_coverage_matrix --check` | PASS | PASS | PASS | — |
| `build_evidence_horizon --check` | PASS | PASS | PASS | — |
| `build_topic_pages --check` | PASS | PASS | PASS | — |
| `build_public_study_roadmap --check` | PASS | PASS | PASS | — |
| `validate_study_spine` (1,311 checks) | ALL PASS | 2 FAIL = `R-ORAL-NONMUT-FIELDS` (50 values) + `-ONLY-GRANULARITY-ADDED`, flagged set **exactly** the approved footprint, every other rule PASS | **ALL PASS** (NONMUT fields_changed 0) | authorised pre-commit condition → cleared post-commit (FD-P2-6) |
| `test_mapping_engine` | 132 PASS | 132 PASS | 132 PASS | — |
| `test_syllabus_fanout` | 24 PASS | PASS | PASS | — |
| `test_study_expandability` | 2 FAIL | identical | identical | PRE_EXISTING_CURRENT_MAIN |
| `test_d01_priority_cohort` | 2 FAIL (`QB1_F#q23`, `QB1_K#q10`; 75 vs 77) | identical | identical | PRE_EXISTING_CURRENT_MAIN |
| `test_roadmap_cockpit` | 3 FAIL / 18 | identical | identical | PRE_EXISTING_CURRENT_MAIN (suite rewrites the roadmap xlsx; restored to HEAD after every run; never committed) |
| `build_qi --check` | exit 2, QP2609 POST_UPPER_BOUNDARY | identical | identical | PRE_EXISTING_CURRENT_MAIN |
| `build_study_qi --check` | STALE `study_qi.json`, `modern_qi_baseline.json` | identical | identical | PRE_EXISTING_CURRENT_MAIN |
| `build_qi_projection --check` | PASS (558 Q / 270 families) | PASS | PASS | — |
| `report_examiner_source_reconciliation --check` | current | current | current | — |
| `build_examiner_index --check` / `validate_examiner_index` | PASS / 54 PASS | same | same | — |
| `build_qb_content_index --check` | current (761 / 86) | current | current | — |
| Oral release categories content-index + examiner + security + health | 13 PASS / 1 FAIL / 1 UNAVAILABLE | — | **14 PASS / 1 FAIL**; 3 mutation suites, 56 mutations, 0 escapes | see below |

Release detail: `node_security_tests` FAILs on main and candidate with the **identical** failing test and assertion payload (`regulatory_facts.test.mjs`, "no current-facing page states a superseded mepc-es2-resumption"; 623/625 pass; Notes-lane pages p24/p25/p28/p29). Class: PRE_EXISTING_CURRENT_MAIN. `qb_health_check` was UNAVAILABLE in the main measurement only because that clone-of-a-clone had no `origin/main` ref (`baseline_exit 1`). On the candidate it ran against `origin/main`: 369 findings vs 369, 0 new → PASS. Not a regression. `study_spine_validate`, `study_pages_check` and `study_public_roadmap_check` all PASS post-commit (not skipped).

**NEW_REGRESSION: 0.**

## 9. Mutation qualification (M1–M8, scratch clones only)

Harness `run_mutations_2a2.py`, two disposable clones, destroyed after capture. **APPLY** context: from `78fa986`, Founder rulings appended, chain run (the 2A.2 path); `validate_study_spine` counted without the authorised pre-commit NONMUT condition. **POST-COMMIT** context: on top of commit 1, full validator. The four applier gates A–D are part of the catcher set.

| ID | Mutation | APPLY verdict (catchers fired) | POST-COMMIT verdict (catchers fired) |
|---|---|---|---|
| M1 | `QB1_C#q1` AFFIRM restates `mapper_topic_id` D09 (from main) | APPLIER_GATE_CAUGHT (B refusal, C schema, D acceptance) | — |
| M1 (store already promoted) | same edit over a store carrying the promotion | APPLIER_GATE_CAUGHT (B, C) | APPLIER_GATE_CAUGHT (B, C) |
| M2 | HOLD `QB3_B#q21` without `candidate_topic_ids` | APPLIER_GATE_CAUGHT (C) | GOVERNED_TOOLCHAIN_CAUGHT (validator NONMUT; also C) |
| M3 | entry for `QB3_A#q19` (H7-only id) | APPLIER_GATE_CAUGHT (A append, B refusal) | APPLIER_GATE_CAUGHT (A, B) |
| M4a | `last_reviewed` removed | GOVERNED_TOOLCHAIN_CAUGHT (`build_study_mappings` exits 1, `--check`; also C) | GOVERNED_TOOLCHAIN_CAUGHT (same) |
| M4b | `reviewer` removed | APPLIER_GATE_CAUGHT (C) | GOVERNED_TOOLCHAIN_CAUGHT (validator NONMUT; also C) |
| M5 | held item relabelled fresh in the on-disk queue | GOVERNED_TOOLCHAIN_CAUGHT (`build_study_mappings --check`; also D) | GOVERNED_TOOLCHAIN_CAUGHT (same) |
| M6 | REVIEW_PENDING stem injected into public samples | GOVERNED_TOOLCHAIN_CAUGHT (`build_public_study_roadmap --check`) | GOVERNED_TOOLCHAIN_CAUGHT |
| M7 | `/meoclass1/` link injected on the public roadmap | GOVERNED_TOOLCHAIN_CAUGHT (`build_public_study_roadmap --check`) | GOVERNED_TOOLCHAIN_CAUGHT |
| M8 | pre-existing entry `QB1_A#q17` altered | APPLIER_GATE_CAUGHT (A) | GOVERNED_TOOLCHAIN_CAUGHT (validator NONMUT; also A) |

**Escapes: 0 in both contexts.** At apply time (the path a tranche actually takes), the governed toolchain alone catches M4a, M5, M6, M7. M1, M2, M3, M4b and M8 are caught only by the applier gates, which is why A–D are qualification gates. After commit, `R-ORAL-NONMUT` turns M2, M4b and M8 into governed catches, because they move committed Oral records.

**Clean-rebuild control (both contexts):** `build_study_mappings.py --force` re-derives all 1,130 records from scratch, then re-applies the adjudications. The result is byte-identical to the incremental build, with gates A–D PASS. The acceptance result therefore does not depend on store state.

## 10. Exact changed paths

Commit 1 `68c1bfd26937100e07b136ddd427cd38aa1aca20` (`study: adjudicate Phase 2A D10 mapping queue`), vs `78fa986`:

| Path | Class | Lines |
|---|---|---|
| `tools/study/adjudications.json` | ALLOWED (hand input, append-only) | +217 / −0 |
| `docs/study/study_mappings.json` | DERIVED (26 records: status/stamp fields) | +141 / −78 |
| `docs/study/mapping_review_queue.json` | DERIVED (24 items leave; 2 become HELD; counters) | +11 / −368 |
| `docs/study/study_spine.json` | DERIVED (BASE_REGEN_CATCHUP only) | +1 / −1 |
| `meoclass1/topics.html` | DERIVED (gated; counts + 24 rows placed under D10) | +2 / −2 (long lines) |
| `SQ/study-roadmap.html` | DERIVED (public; 3 approved stems) | +1 / −1 (single-line page) |

Commit 2 `(this commit; its SHA is in the final review package)` (`docs: record Oral Roadmap Phase 2A qualification`): this file only. No `tools/study/*.py`, QB card, SQ twin, `qb_content_index.json`, `tools/oral/**`, examiner, official syllabus/crosswalk, QI, Notes, `TOPIC_0n_*.md`, roadmap xlsx, `middleware.js`, `api/**`, `vercel.json` or new generated file is in either commit.

## 11. H7

Not landed on main; not modified; no H7-only id adjudicated (`QB3_A#q19` appears only as the M3 negative control in scratch). Sequencing (readiness §6): whichever of H7 and this tranche lands second rebases and re-runs the study chain from unmodified builders. H7's 5 S-plan entries are disjoint from these 26 keys and must be appended after them, not over them.

## 12. QI

Unchanged. `QI_UPPER_BOUNDARY` not moved; no QI builder run in write mode; `study_qi.json` byte-identical; `build_qi` / `build_study_qi` `--check` payloads identical to main (QP2609 outside the window).

## 13. Notes

Unchanged. `meoclass1/oralnotes/**`, `tools/notes/**` and the frozen `ORAL_NOTES_UNITS.jsonl` were not touched. The only Notes-related effect is the derived `study_spine.json` counter `notes_files 35 → 38` (BASE_REGEN_CATCHUP from `78fa986`, §5).

## 14. Rollback

- Before landing: discard the local branch. Nothing is published.
- After landing: `git revert` the commit-2 record and commit 1 (or reset main to `78fa986` under the landing authority), then run the SKILL.md chain. Reverting commit 1 restores the 108-item queue, the 653 placements and the three previous D10 public samples. It also restores the stale `notes_files 35`; re-running the chain re-applies the catch-up. The deployment rollback target is the production deployment serving `78fa986` at landing time, to be recorded by the landing step.

## 15. Phase 2B handover

- **Scope:** 26 fresh items cued to other domains: recommended D07 15, D04 4, D03 3, D05 1, D02 1, **D01 1 (`QB1_F#q23`)**, D09 1 (readiness §3; `PHASE2_QUEUE_BASELINE_78fa986_rederived.csv` rows tagged `2B-CUED-OTHER`).
- **FD-P2-4 must be decided before 2B.** `QB1_F#q23` is already one of the two `test_d01_priority_cohort` failures. Any 2B ruling into or out of D01 changes that universe and couples to `docs/study/TOPIC_01_STATUTORY_SURVEYS_AND_CLASS.md`.
- **Mandatory for 2B:** the 2A pattern (proposal → Founder rulings → apply), gates A–D, the pre-commit NONMUT footprint proof, post-commit `validate_study_spine` ALL PASS, and re-simulation of public sample cascades (2B moves D07/D04/D03 samples whenever an affirmed id sorts ahead of a current sample).
- **2C remains blocked** on the null-mapper contract test (42 items with `mapper_topic_id = null`).
- Pre-existing toolchain properties recorded in 2A.1 (builder exits 0 on refusal; incremental store keeps stale promotions; null reviewer accepted; empty holds accepted) are unchanged. They are why gates A–D are mandatory.

## 16. Final rebase onto `e0f1606` and requalification (2026-10-08)

Sections 1–15 are the historical qualification on base `78fa986` and are not rewritten. This section records the Founder/Lane A–authorised rebase (Phase 2A implementation accepted in substance; rebase only, no editorial change). Reviewed package: `ORAL_ROADMAP_PHASE2A_FINAL_REVIEW_20261008.zip`, sha256 `d37aba075a226875f20b3ab7375fbca5d93defeeb091540d20252aecab6ca473`.

**Status:** `ORAL ROADMAP PHASE 2A REBASED AND REQUALIFIED — D10 QUEUE CLOSED FOR FRESH ITEMS — READY FOR FOUNDER LANDING APPROVAL`

### 16.1 Base and Notes Parts 30–31

- `origin/main` = **`e0f1606e62d27f8d06993f1c9f7c13066f69e7a4`** ("Complete Engineering Management Notes Parts 30-31", 2026-10-08 20:54 +0530). It changes 9 Notes paths only (`meoclass1/oralnotes/**`, `tools/notes/specs/p29–p31.json`). No H7.
- Effect on the study layer: `notes_content_index.json` `total_files` 38 → 40, read only into `study_spine.json` `sources.notes_files`.
- **Ruling-input identity, `78fa986` vs `e0f1606`:** every one of these is blob-identical: `mapping_review_queue.json`, `study_mappings.json`, `adjudications.json` (pre-Phase-2A, 150 entries, sha256 `3de2a13e…`), `qb_content_index.json`, the 8 QB files holding the 26 items, the examiner snapshot / ledger / config / reconciliation record, `study_spine.py`, `mapping_engine.py`, `official_crosswalk.json`, `official_syllabus.json`, `topics.html`, `study.html`. The whole trees `tools/study`, `docs/study`, `tools/oral`, `meoclass1/oral-intelligence` and `SQ` are identical. The queue re-derived on `e0f1606` is byte-identical: **108 total / 94 fresh / 14 held, D10 fresh 26**, 0 drift.

### 16.2 Old → new commit mapping

| Logical commit | Old (on `78fa986`) | New (on `e0f1606`) | Content delta |
|---|---|---|---|
| 1. `study: adjudicate Phase 2A D10 mapping queue` | `68c1bfd26937100e07b136ddd427cd38aa1aca20` | `0527359ea8797868d9d82812f101fa72b4f3ba10` | `study_spine.json` `notes_files` 38 → 40 only (`git range-diff`). Message: catch-up line updated to 35 → 40, plus a "Rebased onto e0f1606 from 68c1bfd" line |
| 2. `docs: record Oral Roadmap Phase 2A qualification` | `28da9a59a552cc6b7f14e0701a513d19a069d935` | this commit | this §16 appended; §§1–15 byte-identical |

No ruling, reviewer, `last_reviewed`, note, HOLD candidate list, public swap or topic logic changed. `adjudications.json`, `study_mappings.json`, `mapping_review_queue.json`, `topics.html` and `SQ/study-roadmap.html` are byte-identical between old and new commit 1.

### 16.3 BASE_REGEN_CATCHUP (current main)

The SKILL.md chain on a disposable, untouched `e0f1606` copy changes exactly one value: `study_spine.json` `sources.notes_files` **35 → 40** (Parts 27–29 in `78fa986` plus Parts 30–31 in `e0f1606`; main never regenerated the spine). No other drift. The rebased candidate's `study_spine.json` is **byte-identical** to that base-regen spine. Phase 2A contributes nothing to the spine; `notes_files = 40` is current-main catch-up.

### 16.4 Rebuild and mandatory gates A–D (rebased tree, unmodified builders)

Chain: all 8 builders exit 0. `adjudications: applied 160, reassigned 82, held 16, refused 0`. Queue written: 84 open = 68 unadjudicated + 16 human-held. Only `study_spine.json` was re-written relative to the cherry-picked commit.

| Gate | Result |
|---|---|
| A append proof (vs `e0f1606` store) | PASS: 150 deep-equal, +26 exactly the ruled ids, 0 extra, top level unchanged |
| B refusal scan | PASS: 0 × `REFUSED ADJUDICATION` |
| C schema | PASS: 26/26 complete and equal to the Founder rulings; both HOLDs carry candidates |
| D acceptance | PASS: 24/24 AFFIRM VALID_MAPPED in D10; `QB1_C#q7`, `QB3_B#q21` HELD_PENDING_EVIDENCE; fresh D10 = 0 |

### 16.5 Final queue metrics and semantic result

Queue 108 → **84**; fresh 94 → **68**; held 14 → **16**; **D10 fresh 26 → 0**; Oral placed 653 → **677**; D10 placed 7 → **31**. D01 membership unchanged (77; ids and statuses identical); priority ranks and study order unchanged; gap register and gap production queue byte-identical; C49-A3-04 unchanged (`NODE_EVIDENCED_NO_GOVERNED_ANSWER`, oral resolved 33); `written_evidence_horizon.json`, `coverage_matrix.json`, `study.html` and `study_qi.json` byte-identical. Oral store footprint: 26 records = the ruled ids, adjudication fields only, 0 topic changes, 1,130 records.

### 16.6 Final public diff

Exactly the three approved D10 swaps: `QB1_C#q9` → `QB1_C#q1` "Reserve buoyancy and the GZ curve?"; `QB1_D#q5` → `QB1_C#q2` "Static vs dynamic stability?"; `QB1_J#q1` → `QB1_C#q3` "Tender vs stiff ship — problems of excessive stiffness?". The word-level diff against `e0f1606` = these six stems only; 0 count changes; 0 changed tags. `build_public_study_roadmap --check` (with `assert_public_safe`) PASS; 0 `/meoclass1`, 0 `/solvedQP`, 0 public→gated links, 0 answer / CE-tip markup, 0 examiner names, 0 tier labels. All 9 internal roadmap destinations (`SQ/study-roadmap.html`, `index.html`, `SQ/index.html`, `SQ/examiner-index.html`, `SQ/solved-qp-sample-january-2026.html`, `SQ/trial.html`, `SQ/QB1_A.html`, `terms.html`, `privacy.html`) resolve in the tree; 5-page link inventory 1,810 rows, 0 broken.

### 16.7 Final validation matrix (rebased commit 1 vs CURRENT MAIN `e0f1606`)

| Gate | `e0f1606` | rebased | Class |
|---|---|---|---|
| `build_study_spine --check` | STALE | current | FIXED_CURRENT_MAIN_STALENESS (via BASE_REGEN_CATCHUP) |
| `validate_study_spine` (1,311) | ALL PASS | **ALL PASS**, incl. `R-ORAL-NONMUT-FIELDS` and `-ONLY-GRANULARITY-ADDED` (fields_changed 0) | — |
| `build_study_mappings`, `reconcile_official_mappings`, `build_coverage_matrix`, `build_evidence_horizon`, `build_topic_pages`, `build_public_study_roadmap` `--check` | PASS | PASS | — |
| `test_mapping_engine` (132), `test_syllabus_fanout` (24) | PASS | PASS | — |
| `test_study_expandability` (2 FAIL), `test_d01_priority_cohort` (2 FAIL), `test_roadmap_cockpit` (3 FAIL), `build_qi --check` (QP2609), `build_study_qi --check` (STALE) | fail | identical payloads | PRE_EXISTING_CURRENT_MAIN |
| `build_qi_projection --check`, examiner reconciliation `--check`, `build_examiner_index --check`, `validate_examiner_index` (54), `build_qb_content_index --check` (761/86) | PASS | PASS | — |
| Oral release: content-index, examiner, security, health | 14 PASS / 1 FAIL | **14 PASS / 1 FAIL**, gate-by-gate identical; 56 mutations, 0 escapes | `node_security_tests`: PRE_EXISTING_CURRENT_MAIN (identical failing test and payload: superseded MEPC ES.2 wording on Notes pages p24/p25/p28/p29) |

**NEW_REGRESSION: 0.**

### 16.8 Mutation sentinels (rebased contract)

The full M1–M8 POST-COMMIT suite was re-run on rebased commit 1 (pre-store reference `e0f1606`): **0 escapes**, with verdicts identical to the pre-rebase POST-COMMIT run. Required sentinels: append proof (A) catches the pre-existing-entry edit (M8); refusal scan (B) catches the mismatched mapper topic (M1); schema (C) catches the malformed HOLD (M2) and missing review fields (M4a/M4b); acceptance (D) catches the wrong final ruled state (M5); public checks catch the REVIEW_PENDING stem (M6) and the gated link (M7). A `--force` clean rebuild is byte-identical, with A–D PASS. The APPLY-context exhaustive result (§9) is reused: the harness inputs differ only by the spine Notes counter, which no mutation reads.

### 16.9 Landing readiness

Local branch `oral-roadmap-phase2a-rebased-20261008` = `e0f1606` + rebased commit 1 + this commit: a **fast-forward of `origin/main`**. Changed paths vs `e0f1606`: `tools/study/adjudications.json`, `docs/study/study_mappings.json`, `docs/study/mapping_review_queue.json`, `docs/study/study_spine.json`, `meoclass1/topics.html`, `SQ/study-roadmap.html`, and this record. Not pushed, not deployed. Landing (push, deploy, live verification of the 9 destinations as 200 and gated pages as 302) needs separate Founder approval. Rollback after landing: revert these two commits, or reset to `e0f1606`, then re-run the chain (which re-applies `notes_files 40`).
