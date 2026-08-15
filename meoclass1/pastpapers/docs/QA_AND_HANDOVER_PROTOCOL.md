# QA AND HANDOVER PROTOCOL

**Governed by `PRODUCTION_PROTOCOL_INDEX.md`.**
**Read this BEFORE FINALISING a paper — not while authoring.** Loading it during authoring
wastes context.

---

## 1. VALIDATION SEQUENCE

Run in this order. Each must pass before the next is meaningful.

| Step | Tool | Proves |
|---|---|---|
| 1 | `validate_spec.py` | the spec is structurally valid |
| 2 | `build_paper.py` (+ index / year sheet as applicable) | the artefacts generate |
| 3 | `audit_paper.py` | the paper's content is internally coherent |
| 4 | `recurrence_check.py`, `known_traps_check.py` | recurrence and known-trap handling |
| 5 | `health_check.py` | **the whole-repository gate** |
| 6 | `ui_behaviour_test.cjs` | interactive behaviour |
| 7 | visual check over HTTP | what the candidate actually sees |
| 8 | `temporal_sweep.py` | post-sitting dates and inherited donor prose Q-references |
| 9 | `surface_impact.py --base <ref>` | **which public / paid / commercial surfaces moved** |

Steps 1–7 are gates: they pass or the paper does not ship. **Steps 8 and 9 are not gates.**
They are the Production Intelligence Layer, and they detect rather than decide —
`PIL FLAGS; CLAUDE ADJUDICATES`. A post-sitting date can be perfectly correct for its sitting,
so the sweep reports candidates and Claude rules on each under
`TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md`. Both run inside `run_toolchain.py`; step 9 only
when a `--base` ref is supplied, because there is no safe default to compare against.

**Step 9 is mandatory at finalisation.** A change to a public, free, commercial or
security-sensitive surface that was *not* the target of the session must be reported to the
Founder even when every gate passes — regeneration is allowed to move those surfaces, but not
silently. See `WORKFLOW_LESSONS.md` lesson 7.

`health_check.py` must end **0 errors, 0 warnings** — *in the mode the tree is actually built in*.
Among other things it verifies id uniqueness, spec/page correspondence, that every built question
carries a study guide, quick revision, answer route and retrieval cards, that all links and anchors
resolve, that build state matches the requested mode, that there is no path leakage or third-party
branding, and that **every generated file reproduces exactly from its source**.

**The build-state assertion is mode-symmetric**: bare, it requires every page to be `noindex` and
ungated; under `--publish` it requires the opposite. The two are exact complements, so one of the
two invocations returns 0 errors for *any* tree, and a green result on its own proves only that the
tree matches the mode you asked about. Pass the flag that matches the build the tree holds — and at
finalisation, that is the build `main` commits, reached via `run_toolchain.py --publish`. See
`LAPTOP_REVIEW_AND_INTEGRATION_PROTOCOL.md` §3.M.

## 2. DETERMINISM

A rebuild from an unchanged spec must produce byte-identical output. If it does not, stop and
find out why before doing anything else — non-determinism invalidates every downstream check.

**Line endings matter.** CRLF/`autocrlf` corrupts content-hashed assets on checkout. If hashes
move without a content change, suspect this first.

## 3. POSITIVE CONTROLS

A check that has never failed has not been shown to work. Where a validator is load-bearing,
confirm at least once that it *fails* on a deliberately broken input. Two defects have
previously been found in the harness rather than the content — a passing suite is not
self-validating.

`run_toolchain.py --self-test` exercises every positive control, including the PIL sweeps.
**A new guard without a positive control is not acceptable.** Each PIL tool additionally
carries a mutation control that disables its own detection and asserts the control stops
firing, then restores it and asserts detection returns.

## 4. UI VERIFICATION

- Serve over HTTP on localhost. **`file://` cannot be inspected properly** and has hidden real
  defects that the passing toolchain could not see.
- Start one server, reuse it, and **kill it when done** — see `EXECUTION_EFFICIENCY_POLICY.md`.
  A stale server from a previous session can serve the wrong directory and silently invalidate
  the check.
- Check desktop and mobile viewports in one batched pass.

## 5. GENERATED ARTEFACTS

Before committing, confirm the working tree contains exactly the artefacts the build should
have produced — no scratch output, no stray render, no leftover temporary file.

## 6. GIT

- **Stage explicit paths. Never `git add .`** — it sweeps in scratch, caches and untracked
  experiments.
- **MANDATORY PUBLICATION GATE — name `solvedQP/QP####.html` explicitly.** When a paper becomes
  available its customer-facing delivery page is **generated**, so git reports it as `??`
  untracked and staging by explicit path silently omits it. Shipping that state publishes a
  manifest advertising the paper as Available while the paid page 404s. Before every integration
  commit: run `git status`, confirm the delivery page exists, and confirm it appears in
  `git diff --cached --name-only`. This has now arisen on **three consecutive papers** — QP2501,
  QP2502 and QP2503 — and was caught by this check each time. Generated never means tracked.
- One coherent commit per logical change.
- Source PDFs are never committed. This repository is public.
- Push to the paper's own `pastpapers/qp####-founder-review` branch.
- **No merge to `main` without Founder approval.**
- Finish with a clean tracked tree and state the branch and commit in the report.

## 7. STATE, HISTORY AND LESSONS — three files, three owners

At finalisation you update up to three files, and each takes a different kind of writing. Do not
put the session narrative in `CURRENT_STATUS.md`; that is what made it 200 KB.

| File | What you write | How |
|---|---|---|
| `CURRENT_STATUS.md` | **current-state delta only** — new corpus totals, the new latest paper, the new next target, blockers opened or closed | **edit in place.** Replace the superseded rows. It must stay small and scannable |
| `history/SESSION_HISTORY.md` | the **session narrative** — what you did, what you found, what you rejected and why | **append** a new `§NN` section using the schema at the top of that file. Never renumber or rewrite an existing section |
| `WORKFLOW_LESSONS.md` | only when a **reusable** lesson or rejection genuinely changed | edit the relevant entry |

Three rules that are easy to get wrong:

- **Do not add policy to `CURRENT_STATUS.md`** — policy belongs in the protocol files.
- **Do not correct history to match current state.** Old counts, old decisions and old mistakes are
  evidence. If a historical section is superseded, say so in a new section; do not edit the old one.
- **A session with no reusable lesson writes nothing to `WORKFLOW_LESSONS.md`.** Padding it
  devalues the entries that are load-bearing.

## 8. STANDARD REPORT SCHEMA

Default to these sections. The session prompt may request more; do not pad by default.

```
# VERDICT               complete / blocked
# WHAT WAS PRODUCED     paper, question count, artefacts
# SOURCE VERIFICATION   what was checked against what
# TEMPORAL REVIEW       flags examined, findings, sweeps run
# DONOR REUSE           donors used, three deltas per donor
# QA                    each validator and its result
# UI CHECK              what was viewed and how
# GIT                   branch, commit, push, tree state
# OPEN QUESTIONS        anything needing a Founder decision
# NEXT                  the delta for the following session
```

A thirty-section report is not a quality signal. Say what happened, show the evidence, stop.

## 9. HANDOVER / NEXT_SESSION

Carries **delta only**:

- target paper
- starting branch and commit
- specific donors and their known deltas
- specific known temporal risks
- specific source blockers
- expected counts
- the stop boundary

It must **not** restate stable policy — that is what the governed protocol files are for.
