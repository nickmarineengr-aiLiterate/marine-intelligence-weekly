# The Phase-2 present-day layer — ownership, and why it exists

**Status: RATIFIED (Founder decision, 2026-08-23).**
`tools/study/qi_phase2_adjudications.json` is the governed owner of present-day
family decisions. It is not a temporary store and it is not to be folded back
into the paper specs.

This document exists because a previous brief asked that no new store be
created, and tranche 001 created one anyway. It was right to. This records why,
so nobody removes it on the strength of the earlier instruction.

---

## The contract the whole product rests on

**MIW written answers are SITTING-ANCHORED.**

A model answer to a February 2024 paper must be true as at the February 2024
sitting. Not as at today. `TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md` §1 is
the governing statement and nothing here weakens it.

That is not a stylistic preference. A candidate reading a 2024 paper is reading
what the examiner set and what a correct answer looked like *then*. Silently
rewriting it to August 2026 law would make the paper cite instruments that did
not govern it — a document that is internally coherent, confidently worded, and
false about its own date.

## The problem that creates

If answers are frozen at their sitting, then over time the corpus accumulates
answers that are correct-for-their-sitting and stale-for-today. Both facts are
true at once, and the candidate needs both:

- *"What was the right answer at that sitting?"* — the past paper answers it.
- *"Is that still the law, and what should I write in next month's exam?"* —
  nothing answered it before Phase 2.

The second question cannot be answered by editing the first. It needs a
**separate record, at family level, carrying its own review date**.

## The two layers, stated plainly

| | PAST-PAPER MODEL ANSWER | PHASE-2 FAMILY PRESENT-DAY RECORD |
|---|---|---|
| Question it answers | What was correct **at this sitting**? | What is correct **now**? |
| Anchored to | the examination date | `authority_currentness_date` |
| Lives in | `meoclass1/pastpapers/specs/*.json` | `tools/study/qi_phase2_adjudications.json` |
| Unit | one question | one recurrence family |
| Changes when | it was **already wrong at its sitting** | current authority moves |

## Fields the Phase-2 store owns

Nothing here is duplicated from elsewhere. Recurrence counts appear only inside
`pinned_at_selection`, and they are pins for the self-policing gate
(`R-P2-PIN-*`), not a second copy of the recurrence layer.

| Field | Role |
|---|---|
| `family_id` | join to Phase 1. Same id space as `qi_phase1_adjudications.json` and `study_qi_holds.json`. |
| `present_day_examinable_core` | what the examiner would be asking today. |
| `existing_answer_owners` | which solved questions currently answer it. |
| `canonical_current_question` | the question a candidate should read today. |
| `canonical_current_answer` | **the ONE answer a readiness grant reaches.** See "a grant reaches one answer" below. |
| `primary_authority` | source, class and what was checked. Dated. |
| `authority_currentness_date` | the date the finding is anchored to. |
| `current_framework_finding` | whether and how the framework moved since the sitting. |
| `future_not_in_force` | adopted but not yet operative — must never read as current. |
| `superseded_elements` | what has been replaced. |
| `correction_or_modernisation` | the classification that decides whether a past paper may be edited. |
| `independent_review` | named reviewer and verdict. |
| `final_state` | the governed outcome. |
| `readiness_after` | the consequence, never asserted directly. |

## The invariant, and where it is enforced

> **A Phase-2 currentness finding must NOT rewrite a sitting-anchored model
> answer, unless that answer was already wrong at its own sitting.**

| Situation | Class | Action |
|---|---|---|
| Wrong **at its own sitting** | `CORRECTION` | Edit `model_answer`. This RESTORES sitting-anchoring. |
| Framework moved **after** the sitting | `MODERNISATION` | Leave the answer alone. Record the present-day position here. |

`UPDATE_2024_ANSWER_TO_2026_LAW` is not an available move. Modernisation lives
in this layer or in a successor answer, never in the historical paper.

Enforced by:

- `validate_phase2_tranche.R-P2-MODERNISATION-NOEDIT` — fails the build if a
  record classed `MODERNISATION` also claims to have edited a past paper.
- `validate_phase2_tranche.R-P2-EARNED` and the `R-P2-AUTHORITY*`,
  `R-P2-REVIEW*`, `R-P2-ANSWER*` inputs — readiness is a consequence of dated
  authority, a passed independent review and a resolvable named answer. Hollow
  out any one and the grant evaporates.
- `validate_study_qi.R-READY-SAFE` — honours that exemption and nothing else.
  The Phase-1 triage value in `qi_currentness.json` is never rewritten.
- `validate_qi_projection.R-PROJ-E/F/G` — the same rules again at the point of
  rendering, over the shipped bytes.

## A grant reaches ONE answer, not a family

Tranche 001 made this mistake before it was caught. Resolving `QIF-EM-0017`
initially marked `QP2402-Q5` ready — a February 2024 answer about *ongoing
developments*, whose own record says it must never be reused at a later sitting
— while the successor that had superseded it still read `VERIFY`. Exactly
backwards.

`study_qi_adapter.question_readiness()` therefore grants Phase-2 readiness only
to the question the record NAMES as `canonical_current_answer`. Every other
member keeps its triage verdict. `R-P2-ANSWER-SCOPE` gates it, and
`R-PROJ-E`/`R-PROJ-G` re-assert it against what actually renders.

## "Ready" is not "verified"

Added 2026-08-23 with the projection layer, and it is the distinction most
likely to be lost again.

82 families are `READY_TO_STUDY_NOW`. **Ten** carry a governed Phase-2 record.
The rest are ready because Phase-1 triage fired no currentness risk — which is
the *absence of a signal*, not the presence of a check. `qi_model` already says
it: `UNKNOWN` is not `CURRENT`, it means nobody looked.

So the candidate-facing wording splits on `readiness_basis`:

| Basis | Wording |
|---|---|
| `PHASE2_GOVERNED_REVIEW` | **Current answer verified** |
| `TRIAGE_NO_RISK_SIGNAL` | **No currentness risk flagged** |

Spending the word "verified" on 82 answers when nine were verified would be the
precise failure this whole layer exists to prevent: it does not look like a bug,
it looks like a confident, current, wrong answer.

## Phase 1 is an input here, and it does not get a veto

A question can legitimately read `READY_TO_STUDY_NOW` while its family's
currentness triage still says `CURRENTNESS_REVIEW_REQUIRED`. Three of the ten
tranche-001 answers do. The triage value is deliberately frozen — it records the
risk that *prompted* the Phase-2 work, not the finding that *closed* it.

An unconditional "unsafe currentness beats ready" rule therefore reverts every
grant Phase 2 earned, and hides finished verification behind a stale warning.
The exemption is narrow: a governed record that names **this** question. For
every other member of a resolved family the guard bites as written.
`qi_projection.project_question()` carries the comment; `R-PROJ-F` gates it.

## Working a tranche

See `tools/study/SKILL.md`, section "Phase 2". Nothing in this document
replaces the working procedure there.
