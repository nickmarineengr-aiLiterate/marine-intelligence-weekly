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

`health_check.py` must end **0 errors, 0 warnings**. Among other things it verifies id
uniqueness, spec/page correspondence, that every built question carries a study guide, quick
revision, answer route and retrieval cards, that all links and anchors resolve, that review
state is `noindex` and ungated, that there is no path leakage or third-party branding, and
that **every generated file reproduces exactly from its source**.

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
- One coherent commit per logical change.
- Source PDFs are never committed. This repository is public.
- Push to the paper's own `pastpapers/qp####-founder-review` branch.
- **No merge to `main` without Founder approval.**
- Finish with a clean tracked tree and state the branch and commit in the report.

## 7. CURRENT_STATUS UPDATE

Update `CURRENT_STATUS.md` with **state only**: what now exists, what is next, what is
blocked. Do not add policy to it — policy belongs in the protocol files. Do not rewrite
historical entries; append.

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
