# Oral follow-up authorisation register

**Status:** committed and validated. Follow-up production (F1 onward) has not started.
**Register:** `tools/oral/oral_followup_register.json` — 35 actions, `FUP-001`..`FUP-035`.

This document explains where the register came from and how to read it. The operational
workflow lives in `tools/oral/SKILL.md` §7.

---

## 1. Why it exists

The 35 follow-up actions were produced on a research branch and never reached `main`. A
repo-wide grep of the working tree found **zero** `FUP` identifiers, so the workload
appeared to survive only in handoff prose.

That reading was half wrong, and the correction matters: the identifiers **were**
committed — as `production_action_id` inside
`FINAL_ORAL_PRODUCTION_AUTHORIZATION.json` on
`origin/review/oral-final-gap-decision-laptop`. They were invisible because a working-tree
grep only ever sees the checked-out branch. `git grep <pattern> <ref>` finds them.

So this was never a reconstruction from memory. It is a **promotion**: machine-readable
authorisation data that existed only where nobody would look has been re-derived,
enriched with a confidence model, and committed to `main` where production will start.

---

## 2. Sources, pinned by blob SHA

Branches move; blobs do not. Each source is addressed by content hash, so the generator
cannot silently re-derive against a different record.

| Role | Blob | Record |
|---|---|---|
| authorisation | `b3f3a97` | `FINAL_ORAL_PRODUCTION_AUTHORIZATION.json` |
| evidence | `5170fbe` | `FINAL_REMAINING_ORAL_PRODUCTION_DECISIONS.json` |
| colocation | `d4571ac` | `FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json` |

The authorisation blob is byte-identical on both
`origin/review/oral-final-gap-decision-laptop` and
`origin/research/oral-final-enrichment-consolidation` — one record, two branches.

---

## 3. The 39 → 35 proof

```
39 source families dispositioned FOLLOWUP_ONLY
   grouped by parent canonical question id
35 distinct parent cards
35 FOLLOWUP_INSERTION actions
```

Group sizes: **32 singletons + 2 pairs + 1 triple** = 39 families, 35 actions.
The three multi-family groups are `FUP-001` (`QB10_B#q1`, 3 families), `FUP-004`
(`QB1_A#q30`, 2) and `FUP-008` (`QB1_E#q1`, 2).

**Four independent representations agree**, and the generator refuses to write unless
they do:

1. `authorisation.families[]` where `adjudicated_decision = FOLLOWUP_ONLY` → 39
2. `authorisation.production_actions[]` where `kind = FOLLOWUP_INSERTION` → 35
3. `decisions.families[]` where `decision = FOLLOWUP_ONLY` → 39
4. `enrichment.followup_colocation[]` → 9 families, all a subset of the 39

The prose record agrees too: *"Follow-up source families: 39. Unique insertion groups:
35."*

### Stable identifiers are derived, not trusted

`build_production_authorization.py` assigned `FUP-NNN` by numbering the grouped targets
in **ascending lexicographic order of the parent canonical id**. The generator re-derives
the numbering from the family table alone and compares it to the committed identifiers.
It matches exactly, for all 35. Nothing was preserved on faith.

**Old handoff IDs vs reconstructed IDs: 35 / 35 MATCH, 0 mismatch.**

---

## 4. Target confidence — the significant finding

All 39 families are `LAPTOP_CONFIRMED`. That confirms the **disposition** — this is a
follow-up rather than a new card — and says nothing about the parent card it points at.

**Only 4 of 39 had their parent chosen by hand** (`decision_basis: "hand adjudication
against current answer bodies"`). The other 35 carry `"rule: material partial
dispositioned by recurrence"`, and their `decision_target` is literally
`current_best_answer_question_id` — an IDF coverage score.

That is the mechanical explanation for the "weak topical match" the closing handoff
flagged. `FUP-005` pairs a parent on Admiralty Law with an ask reading *"International
chamber of commerce?"*; `FUP-011` pairs *"All marpol related documents"* with *"DGCOMM
CONTACT DETAILS"*. A score put them there.

| `target_confidence` | rule | n |
|---|---|---|
| HIGH | hand-adjudicated parent | 4 |
| MEDIUM | score-chosen, score still selects it, coverage ≥ 0.60 | 12 |
| LOW | score-chosen and drifted, or coverage < 0.60 | 19 |

| `target_review_status` | n |
|---|---|
| `CONFIRMED` | 3 |
| `METADATA_ONLY_CANDIDATE` | 1 |
| `REQUIRES_LIVE_ADJUDICATION` | 29 |
| `RETARGET_REQUIRED` | 2 |

`RETARGET_REQUIRED` is **score drift**: `FUP-031` (`GAP-0267`, `QB7_B#q1`) and
`FUP-009` (`GAP-0523`, `QB1_F#q12`) were assigned a target that the current coverage
computation no longer selects. Neither has a hand adjudication to justify the override.

---

## 5. Relationship model

Types come from the governed vocabulary, single-sourced from
`validate_phase2.RELATIONSHIP_TYPES` so the register can never carry a type the phase-2
gate rejects.

| type | n | derived from |
|---|---|---|
| `FOLLOW_UP` | 2 | adjudicator wrote "follow-up on …" |
| `EXPECTED_DETAIL` | 2 | adjudicator wrote "expected detail" |
| `TOPIC_INFERENCE_ONLY` | 31 | target came from a topical score and nothing else |

`TOPIC_INFERENCE_ONLY` is not a placeholder — it is the honest governed value for a
relationship inferred from topical proximity. Live adjudication may promote one to
`FOLLOW_UP` or `EXPECTED_DETAIL`; the register must not pre-empt that.

Direction is explicit on every action, so a later examiner simulator can walk it without
re-authoring:

```json
"relationship_edge": {
  "parent_question": "QB1_A#q9",
  "edge": "EXAMINER_FOLLOW_UP",
  "followup": "FUP-006",
  "answer_home": "QB1_A#q9"
}
```

No Study Engine was built.

---

## 6. Structural target check

All **35 targets resolve** against the live corpus (721 canonical questions, 86
question-bearing files): file exists, anchor exists, anchor is a canonical question, and
the pinned `parent_qtext` matches the live card byte for byte.

`TARGET_MISSING` 0 · `TARGET_DRIFTED` 0 · `TARGET_REVIEW_REQUIRED` 0.

The validator re-runs this on every release, which is why it is registered as a gate: a
release that moves one of those cards turns it red immediately.

---

## 7. Register ≠ batch manifest

The register says what is **authorised**. A `batch_f*_manifest.json` says what a run
**implemented**. They must never be collapsed: the register names 35 parent cards it has
never edited, so admitting it to `authorisation_manifest_paths()` would pre-emptively
exempt all 35 from every historical batch guard. `test_oral_release_infra.py` pins the
separation.

---

## 8. Known limits

* **`verification_class` is `UNCLASSIFIED_PENDING_BATCH_SCOPING` for all 35.** Every
  source record carries an empty `technical_verification_scope` for follow-up families.
  Assigning a governed class here would be invention; the producing batch assigns it.
* **`currentness_required` is a floor, not a ceiling** (4 of 35 flagged). It is a
  conservative pattern match over the candidate's ask, so a perishable fact with no date
  word escapes it — `FUP-029` names COP28 and is not flagged. The batch confirms
  currentness.
* **`primary_authority_hint` is a hint**, extracted from instrument names appearing in
  the ask and parent text. It is not a claim about what any instrument says.
* **Nine actions are colocated** with a shipped enrichment on the same parent card. Read
  the live card before authoring — the enrichment may already have said it.

---

## 9. Recommended first batch (F1) — not started

**`FUP-006`, `FUP-018`, `FUP-033`.**

The historically proposed F1 (`FUP-003/004/005/006/009/010/011`) does **not** survive
the register. Of those seven, only `FUP-006` is `CONFIRMED`; five are LOW confidence, and
`FUP-009` — which the closing handoff called the second-cleanest parent match — is
`RETARGET_REQUIRED`.

| id | parent | confidence | relationship | currentness | colocation |
|---|---|---|---|---|---|
| `FUP-006` | `QB1_A#q9` | HIGH / CONFIRMED | `FOLLOW_UP` | no | `ENRICH-A003` |
| `FUP-018` | `QB3_I#q4` | HIGH / CONFIRMED | `EXPECTED_DETAIL` | no | — |
| `FUP-033` | `QB9_C#q5` | HIGH / CONFIRMED | `FOLLOW_UP` | no | — |

Three actions, three files, three source families. Every one is hand-adjudicated, so F1
tests the *workflow* rather than the targeting. `FUP-006` and `FUP-033` are both Marine
Insurance, giving coherent subject matter; `FUP-018` exercises the second relationship
type. Zero currentness exposure. Exactly one colocation, which rehearses the live-recheck
step without being a messy case.

Excluded deliberately:

* `FUP-028` — the only other HIGH action, but `METADATA_ONLY_CANDIDATE` and
  currentness-bearing (a sitting Secretary-General is the most perishable fact in the
  corpus). It may not be a Q&A limb at all.
* `FUP-034` / `FUP-035` — `FUP-034` targets `QB9_G#q3`, already edited by E6's `A046`
  under `GAP-0481` colocation. Confirmed against the register; kept out of F1.

---

## 10. Controls

| Tool | Result |
|---|---|
| `validate_followup_register.py` | 32 checks, 0 FAIL |
| `mutate_followup_register.py` | 12 mutations, 12 caught, 0 weak / 0 escapes / 0 no-ops / 0 crashes |
| `test_oral_release_infra.py` | 91 checks, 0 FAIL |
| `test_oral_release_runner.py` | 107 checks, 0 FAIL |
| `oral_manifest.py --quiet` | 113 / 113 |
| `build_qb_content_index.py --check` | current — 86 files, 721 questions |

Every mutation must trip its **own** named check. The validator carries a check that
re-derives the register and byte-compares, and that check fires on every edit — so a
harness that only asked "did the validator go red?" would report 12/12 while proving
nothing about the other 31 checks. Mutations caught solely by byte-currency are reported
as `WEAK` and fail the suite.
