# Final Oral gap adjudication — record

Session of 2026-08-19, branch `research/oral-final-gap-adjudication-v1`,
from `origin/main` at `66c919b`. No live product was touched.

## What this session answers

One question: **how many additional canonical Q&A cards do we actually still
need?** Not how many source questions went unmatched, and not how many rows say
MISSING. A new card is the last resort; an existing answer, an enrichment, a
Notes promotion, a follow-up or a merge is tried first, in that order.

## The answer

**ADDITIONAL_NEW_CANONICAL_QA_COUNT = 22.**

Six new canonical questions were already created by the P0 batch, so the corpus
reaches **688 + 22 = 710** canonical questions once the approved batch is
produced — 28 new cards in total across both batches.

## The three findings that changed the count

### 1. The frozen reconciliation was stale by construction

`FINAL_ORAL_GAP_CANDIDATES.json` and its siblings were all imported in a single
commit that predates the P0 batch going live. Six families in it are answered
today. `GAP-0337` ("G7, G8, G9") scores **1.00** question coverage and **1.00**
answer coverage against `QB1_A#q31`; it was a genuine gap right up until the P0
batch published, and would have been written twice.

The corollary is a standing rule: **a gap dataset carries the date of the corpus
it was computed against, not the date it was read.** Re-score before counting.

### 2. Question-title matching had been hiding whole cards

Reading answer *bodies* rather than question stems overturned 47 families to
ALREADY_COVERED. The matcher never found:

| family | ask | card it missed |
| --- | --- | --- |
| GAP-0235 | Subrogation in detail and types | `QB1_B#q20` and `QB1_A#q28`, 27 and 25 mentions |
| GAP-0329 | BMP, BMP 4 and 5 | `QB4_B#q16`, `QB4_H#q2`, `QB4_H#q11` |
| GAP-0420 | Engine room resource management | `QB5_A#q2`, `QB5_C_B#q6` |
| GAP-0463 | Mentoring, and its difference from training | `QB5_A#q15` (51 mentions), `QB5_C_B#q1` |
| GAP-0460 | Appraisal report for a junior engineer | `QB5_A#q13` (43 mentions), `QB9_H#q5` |

Every one of these had been ranked a GENUINE_GAP. The cause is structural: the
matcher scores the examiner's wording against the question stem, and a stem like
"What is subrogation in the context of marine insurance/P&I claims?" shares
almost no vocabulary with "Subrogation in detail AND TYPES" once stopwords go.
Answer-body coverage is the signal that survives paraphrase.

Three of these also override a Notes verdict in the opposite direction from the
usual one: `GAP-0352`, `GAP-0590` and `GAP-0708` were graded NOTES_COMPLETE or
NOTES_STRONG, but the **QB already asks them**. Strong Notes support argues
against writing from zero; it does not establish that the QB is silent.

### 3. Two live duplicate homes, surfaced by families that looked like gaps

Neither is a content gap. Both are the same ask answered twice, which is why a
gap candidate pointed at them:

| pair | ask | surfaced by |
| --- | --- | --- |
| `QB3_A#q13` + `QB3_B#q3` | What do you check during a ballast water tank inspection? | GAP-0547 |
| `QB2_C#q4` + `QB2_F#q5` | Water mist lance and mobile water monitor | GAP-0599 |

This is separate debt, logged in the dataset under `duplicate_home_debt`, and
must not be counted as missing content. It joins the known `QB6_E#q2`/`#q3`
duplicate.

## How the 301 families were dispositioned

155 by hand, against current answer bodies and section-level Notes; 146 by rule.
The rule covers MATERIAL_PARTIAL families only, where the matcher had already
established that an existing answer covers part of the ask — so the only open
question is whether the missing limb is material, and recurrence answers that
without re-reading.

| disposition | families |
| --- | ---: |
| DEFER_LOW_VALUE | 95 |
| ENRICH_EXISTING_QB | 63 |
| ALREADY_COVERED | 47 |
| FOLLOWUP_ONLY | 39 |
| NEW_CANONICAL_QA | 29 (22 counted, 7 medium-confidence) |
| MERGE_WITH_EXISTING_FAMILY | 10 |
| NOTES_TO_QB_PROMOTION | 10 |
| HUMAN_REVIEW_REQUIRED | 7 |
| NOT_A_GAP | 1 |

## Every approved new card is single-examiner

Cross-examiner recurrence among the 22: **zero**. Every one was asked by exactly
one examiner, once. This is worth stating plainly rather than hiding inside a
priority column — the recurrent, cross-examiner asks were the P0 batch, and they
are done. What remains is breadth, not repetition, which is why the batching
below is argued from the nature of the ask rather than from how often it recurs.

## Batching

- **P1-A (8)** — a current regulation, or a statutory/safety duty a CE is
  expected to hold outright and cannot bluff: MASS/autonomous ships, onboard NOx
  compliance verification, bunker quantity/quality disputes and the sample
  regime, SOLAS steering-gear requirements and pre-departure tests, SAR /
  COSPAS-SARSAT / INDSAR, forward liferaft and HRU, post-renewal weld
  verification, medical evacuation and diversion.
- **P1-B (10)** — solid engineering or commercial asks: Miller cycle,
  flammability-diagram slope, adaptive cylinder-oil control, P/V breaker and
  mast riser, cavitation, wake-equalising duct, electric-shock physiology,
  behaviour-based safety, fresh water allowance, Type B-60 ships.
- **P2 (4)** — long tail: cost decomposition, stowaway handling, motor ship
  against steam turbine, ship broker.

## Human-review queue, recomputed

115 rows in. 42 resolve to an existing answer, 11 become enrichments, and **62
remain genuinely ambiguous**. That residue is deliberate. An ambiguous acronym is
not a question: forcing "FTIR" or "Metos" onto a target costs a candidate a wrong
answer, while leaving it open costs a review. None of the 62 is a confirmed
missing answer, so the residue is safe to carry past a workbook freeze.

Note that 96 of the 115 rows carry best-answer coverage of 0.90 or higher, which
looks like near-total coverage until you see that 41 of them are one- or
two-token prompts. **High coverage on a terse prompt is not evidence of
anything** — a short token set is trivially contained in a long answer. The
recompute therefore requires both coverage and prompt mass before resolving.

## Guard note: token mass is not ask clarity

The validator's first attempt at "a terse prompt cannot justify a new card" used
token mass alone, and immediately flagged `GAP-0562` — "What is a ship broker."
— which tokenises to two content words and is unmistakably a question. The rule
now requires a prompt to be *both* low-mass *and* unformed (no question mark, no
interrogative or imperative verb) before it counts as a bare label. The
interrogatives are all stopwords, so the test has to read the original text: by
the time the prompt is tokenised the evidence is already gone.

## Verification

- 26 validator checks, 0 failures. Every check fails closed.
- 22 mutations, 0 escapes, 0 no-ops, 0 crashes. Each mutation proves it was
  APPLIED by SHA-256 delta and RESTORED by digest, so a silently no-op mutation
  is reported as an escape rather than a pass.
- Determinism: byte-identical output under `PYTHONHASHSEED` 0, 1 and 524287.

The mutation sweep also caught a weakness in the validator itself. "Ambiguous
family promoted to a counted NEW card" was initially caught only by the coverage
check, which fired by luck on that fixture's 0.75 score — a zero-coverage
ambiguous family would have escaped. The mutation now deliberately selects the
*lowest*-coverage ambiguous family, and the catch comes from `C24`, which
requires the dataset to reproduce the authored adjudication table.

## Verdict

**GO** — the true additional new-Q&A count is established at 22.

Master workbook status: **DEFERRED**. `MEO_QB_master_v27.xlsx` and
`MIW_August2026_QuestionBank_SHARE.xlsx` must wait until the approved batch of 22
new cards, 63 enrichments and 10 Notes promotions is produced and published.
