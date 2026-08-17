# Question Intelligence v2 — Phase 1 (RESEARCH ONLY)

**Status:** RESEARCH — NOT CANDIDATE-FACING. Nothing in this directory renders,
gates, prices, or reaches a candidate. Laptop reviews before any integration.

**Built:** 2026-08-17 (Desktop)
**Base:** `origin/main` @ `3451558`
**Branch:** `research/question-intelligence-v2-phase1`
**Comparison target date (`current_as_of`):** 2026-08-17

---

## Why this exists

Candidate/group feedback claimed several August 2026 Engineering Management
questions revive 2010–2012 questions. Phase 1 tests those claims and, separately,
builds the engine that answers the harder question behind them:

> A repeated question is not necessarily a repeated answer.
> If this old question is asked today, what must be written differently?

Two linked layers:

1. **Recurrence intelligence** — has this been asked before, and how similar?
2. **Temporal answer intelligence** — what in the answer has changed since?

---

## Relationship to the intelligence that already exists

This directory is **additive**. It does not replace and must not contradict:

| Existing artefact | What it owns | Untouched by v2 |
|---|---|---|
| `intelligence/historical_qp_intelligence.json` | Question-only records, 2021–2023 sittings, schema `...historical_qp_intelligence.v2` | yes |
| `tools/pastpapers/recurrence_model.py` | Canonical recurrence computed chronologically over MIW's **own** corpus | yes |
| `tools/pastpapers/recurrence_check.py` | What may and may not be published about recurrence | yes |
| `specs/*.json` → `recurrence_adjudication` | Per-question human adjudication written at authoring time | yes |

Two conventions inherited from that layer and honoured here:

- `host_recurrence_hint` is **third-party assertion and is never published.**
  v2 keeps that rule and adds an explicit provenance tier so the distinction is
  testable rather than remembered.
- Canonical recurrence is computed from the calendar over MIW's own holdings.
  v2 does **not** write into that model; it records external occurrences
  separately so canonical recurrence stays derivable from MIW-held sources only.

---

## The evidence floor (the single most important fact in Phase 1)

**MIW holds no source copy of any sitting earlier than January 2021.**

- Solved specs: QP2301 → QP2608
- Intelligence-only: QP2101 → QP2311

There is therefore **no MIW-internal route** to text-verify any 2010–2012 claim.
Every such claim depends on external acquisition, and external acquisition in
this session was almost entirely blocked (see `SOURCE_MANIFEST.json`).

## The second most important fact

**The August 2026 source copy carries no recurrence annotation at all.**
Every QP2608 question has an empty `host_recurrence_hint`. The Founder's
2010–2012 dates did not come from the paper, and could not have.

Further, DieselShip's own recurrence vocabulary for 2010–2015 is **month-level
only** (`2010/JUN`, `2011/SR2`) and carries **no question number**; question
numbers only appear from 2020 onward (`2021/JAN/Q1`). So a claim shaped
"QP2608-Q2 ≈ December 2011 Q-something" cannot have come from DieselShip's
question-level data either, because DieselShip does not publish question-level
data for those years. The hypotheses are candidate recollection. That does not
make them false — H1 in fact survives — but it fixes their evidential weight.

---

## Files

| File | What it is |
|---|---|
| `SOURCE_MANIFEST.json` | Every source touched, its access type, what it yielded, SHA256 |
| `HISTORICAL_COVERAGE_MATRIX.md` | 2010–2022 coverage, classified per §8 |
| `SIMILARITY_MODEL.md` | Classes, confidence, the limb-level finding, negative controls |
| `QUESTION_OCCURRENCES.jsonl` | Normalized historical question occurrences |
| `QUESTION_FAMILIES.json` | Recurrence families with dormancy/revival |
| `QP2608_PAPER_DNA.md` | Q1–Q9 classified; paper-level summary |
| `TEMPORAL_DELTA_SCHEMA.json` | Schema for the temporal answer layer |
| `QP2608_TEMPORAL_DELTAS.md` | Temporal pilots, incl. the unchanged/changed pair |
| `SETTER_HYPOTHESIS.md` | NTA rumour, bounded evidence search |
| `WATCH_REGISTER.md` | What Phase 2 must chase |
| `verification/H*.md` | One record per Founder hypothesis |

## Rules honoured

- No DieselShip answer content acquired, quoted, or stored. Questions only.
- No paywall, login, CAPTCHA or app restriction bypassed. Blocked routes were
  abandoned, not worked around, and are recorded as blocked.
- Raw third-party material stays outside git at `D:\MIW-Historical-QP-Intake\`.
- No candidate-facing file modified. No QP2608 artefact modified.
- Historical wording stays historical; normalization is a separate field.
- One canonical current answer. No `answer_2010` / `answer_2026` forks.
