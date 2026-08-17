# PRODUCTION PROTOCOL INDEX

**Read this first. It is deliberately short and contains no policy of its own.**

Its only job is to tell you which governed files exist, what each one owns, when to read it,
and which instruction wins when two disagree.

---

## 1. PRECEDENCE — which instruction wins

```
SESSION-SPECIFIC TASK        (the prompt you were just given)
        must obey
GOVERNED WORKFLOW PROTOCOL   (the files listed below)
        must obey
REPOSITORY GOVERNANCE        (CLAUDE.md, repo conventions, frozen architecture)
        must obey
MACHINE / ENVIRONMENT SAFETY (outside this repo — see §4)
```

Two consequences that are easy to get wrong:

- **`CURRENT_STATUS.md` describes STATE, not POLICY.** Where it restates a rule that a
  protocol file below also states, the **protocol file wins**. `CURRENT_STATUS` may not
  silently redefine stable policy.
- **`history/SESSION_HISTORY.md` is HISTORY, not state and not policy.** It is append-only
  evidence and was accurate when written. It never overrides `CURRENT_STATUS.md` on state or a
  protocol file on policy, however emphatically an old section is worded.
- **A handover or NEXT_SESSION file carries DELTA only.** It does not override repository
  governance unless the Founder explicitly authorises that in the session prompt.
- **`WORKFLOW_LESSONS.md` is EVIDENCE, not policy.** Where a lesson has been promoted, the
  protocol file or the tool that now owns it is what binds. A lesson still at `CANDIDATE`
  binds nothing — it records what was observed and what would reopen the question.

---

## 2. THE GOVERNED SET

| File | Owns | Read when |
|---|---|---|
| `PRODUCTION_PROTOCOL_INDEX.md` | precedence, routing | **always, first** |
| `PASTPAPER_PRODUCTION_PROTOCOL.md` | how a solved paper is produced: sources, **build mode**, spec→build, the **five-mode learning architecture and Exam Plan**, branch/review rules, the **production sequence**, global side effects, publication proof | **always**, for any paper production |
| `TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md` | sitting-date truth, donor reuse, recurrence, contamination sweeps | **always**, for any paper production |
| `EXECUTION_EFFICIENCY_POLICY.md` | how Claude should execute work on this project | **always** — it is short |
| `QA_AND_HANDOVER_PROTOCOL.md` | validation, determinism, UI check, Git, report schema | **before finalisation** — not needed while authoring |
| `LAPTOP_REVIEW_AND_INTEGRATION_PROTOCOL.md` | the **laptop** role: independent adjudication of a founder-review branch, extraction onto `main`, public/storefront derivation, intelligence graduation, publication and live proof, one-paper stop | **always**, for any review/integration session — and **not** during desktop authoring |
| `CURRENT_STATUS.md` | **current state only**: what exists now, what is next, what is blocked, restart instructions | **always** — it is small on purpose |

There are **two kinds of paper session** and they read different sets.

**Mandatory for a normal solved-paper PRODUCTION session (desktop role):**

1. `PRODUCTION_PROTOCOL_INDEX.md`
2. `PASTPAPER_PRODUCTION_PROTOCOL.md`
3. `TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md`
4. `EXECUTION_EFFICIENCY_POLICY.md`
5. `CURRENT_STATUS.md`

`QA_AND_HANDOVER_PROTOCOL.md` is read **later**, before finalising. Loading it during
authoring wastes context.

**Mandatory for a REVIEW / INTEGRATION session (laptop role):**

1. `PRODUCTION_PROTOCOL_INDEX.md`
2. `LAPTOP_REVIEW_AND_INTEGRATION_PROTOCOL.md`
3. `TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md`
4. `QA_AND_HANDOVER_PROTOCOL.md` — needed **throughout** a review, not only at the end
5. `EXECUTION_EFFICIENCY_POLICY.md`
6. `CURRENT_STATUS.md`

`PASTPAPER_PRODUCTION_PROTOCOL.md` is read by a reviewer **on demand** — it owns the source
authority ladder, the learning architecture and the candidate-facing boundary, which a reviewer
adjudicates against but does not need loaded to begin.

---

## 3. CONDITIONAL READING — do not load these by reflex

| File | Read only when |
|---|---|
| `history/SESSION_HISTORY.md` | you need the historical record — a past session narrative, an old paper checkpoint, a superseded state snapshot, or how a decision arose. **Read the one section you need, never the file.** Other documents cite `CURRENT_STATUS.md §N`; every one of those sections now lives here under the same number, and `CURRENT_STATUS.md` §9 carries the locator table. It is ~200 KB — loading it by reflex costs more context than the whole governed set |
| `WORKFLOW_LESSONS.md` | **read the relevant ENTRIES, never the whole file.** Lessons about how the work is done — proven practices, and rejected or deferred optimisations with the condition for reopening each. Go to it when you are about to adapt a donor, run a temporal sweep, stop a paper part-finished, add a guard, or change a public surface. It is indexed by category so a task-relevant read is cheap; loading all of it is not |
| `2024_2026_RECURRENCE_AND_REUSE_MAP.md` | you need the donor map for the specific paper in hand |
| `QP####_TRUE_SOURCE_DEMAND_MAP.md` | producing that specific paper |
| `MIW_TRUE_SOURCE_CONTRACT.md` | touching corpus object references |
| `MIW_LEARNING_METHOD_DESIGN.md` | you need the **rationale** behind the frozen learning architecture — the evidence base, why there are five modes and no sixth, why `Answer` is the default. It does **not** bind: the rules live in `PASTPAPER_PRODUCTION_PROTOCOL.md` §6 |
| `SOLVED_QP_COMMERCIAL_ARCHITECTURE.md` | commercial/gating questions only |
| `2026_PATTERN_REGISTER.md`, `SOURCE_INVENTORY.md` | intelligence questions, not production |

---

## 4. OUTSIDE THIS REPOSITORY

Machine-specific operating rules (RAM ceiling, session concurrency, stale-process cleanup,
local-server teardown, canonical Python/Node paths) live at:

```
C:\Users\User\PC-Optimization\Claude-Environment\CLAUDE_MACHINE_OPERATING_POLICY.md
```

They are **not** in this repository on purpose — they describe one laptop, not the product.

---

## 5. WHAT THIS ARCHITECTURE REPLACES

Session prompts previously restated stable policy every time: repository grounding, source
authority, Git hygiene, toolchain, determinism, learning architecture, temporal review, donor
reuse, recurrence boundaries, execution efficiency, report structure.

That is now governed here. **A session prompt should carry only the delta**: which paper,
which branch, which donors, which known risks, and where to stop.
