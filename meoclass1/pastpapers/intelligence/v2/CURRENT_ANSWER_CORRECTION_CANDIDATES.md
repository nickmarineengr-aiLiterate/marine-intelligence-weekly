# Current answer correction candidates

**RESEARCH ONLY. NO CANDIDATE-FACING ANSWER WAS PATCHED ON DESKTOP.**
`current_as_of: 2026-08-17`

A correction candidate is raised where temporal comparison shows a **current** MIW
answer carries obsolete law, a superseded regulation, a wrong status, or is missing
an essential current scoring point. The Laptop adjudicates. Desktop only reports.

---

## Result

# NONE

No correction candidate arose from Phase 2.

---

## What was checked, and how

### 1. Exam Plan bullet leak sweep

All **40 papers**, all `answer_route.steps[].points`, against three probes drawn
from the Phase-2 temporal findings:

| Probe | Becomes wrong from |
|---|---|
| Merchant Shipping Act, 1958 presented as the operative statute | 15 March 2026 |
| The 2018 Initial IMO GHG Strategy presented as the current ambition | July 2023 (MEPC 80) |
| The IMO Net-Zero Framework presented as adopted or in force | April 2025 (approved, not adopted) |

The sweep is **sitting-aware**. MIW answers are written *as at the sitting*, so
naming the 1958 Act as operative is **correct** for any sitting before 15 March 2026
and is only a defect at or after it. A naive sweep flags 42 bullets; every one
before its cutover is right.

| | |
|---|---|
| Bullets flagged before applying the sitting rule | 42 |
| Bullets flagged **at or after** their cutover | **2** |
| Confirmed leaks after reading the surrounding step | **0** |

Both survivors were false positives, and both were false for the same reason — the
probe reads one bullet at a time while a candidate reads the step:

- **`QP2511-Q9` step 6 pt 1** — *“the Net-Zero Framework circulated 11 April 2025”*.
  Point 2 records the October 2025 extraordinary session adjourning, and point 3
  states *“circulated but not adopted, so binding nobody at this sitting”*. The
  status is handled two bullets later.
- **`QP2602-Q8` step 3 pt 4** — *“the two together became the Net-Zero Framework”*.
  This describes what the mid-term basket is called, not whether it is in force.

**Method note for reuse:** any future leak probe must evaluate at **step** level, not
point level. A bullet that looks bare in isolation is routinely qualified by its
neighbour, and a point-level probe will keep producing these two.

### 2. The families carrying a real temporal delta

- **Pilot C — Merchant Shipping Act.** All five held occurrences of `BANK-160`
  already state the repeal, and increasingly thoroughly as commencement approached:
  mentions run **2 → 6 → 14 → 15 → 16** across July 2023, October 2024, June 2025,
  August 2025 and February 2026. Correct at every sitting.
- **`FAMILY-EM-0006` — IMO GHG developments.** Both `QP2309-Q3` (September 2023) and
  `QP2402-Q5` (February 2024) carry the **2023** IMO GHG Strategy and net-zero, not
  the superseded 2018 Initial Strategy. Correct.
- **`QP2608-Q9` — CII corrective action.** States the regulation 28.11 review as
  opened but not concluded, and the Net-Zero Framework as approved at MEPC 83 in
  April 2025 but **not adopted**, the October 2025 extraordinary session having
  adjourned. Matches MIW's verified position exactly.
- **Pilot B — `QP2608-Q2`.** Mentions neither BWM nor AFS/cybutryne. **Not a
  defect.** Both are `USEFUL_CURRENT_ENRICHMENT`; the stem asks about coordination,
  delegation and undocking inspections, not environmental compliance. A missing
  enrichment is not a missing essential point, and raising it as a correction would
  be exactly the answer-bloat the model is built to prevent.

---

## Scope and limits of this finding

“NONE” means: **the three probes, applied across the whole corpus, found nothing.**
It does not mean the corpus is free of obsolete law. The probes were derived from
the temporal deltas Phase 2 actually built, and Phase 2 built four. A broader sweep
needs a broader set of dated cutover facts, which is Phase 3 work.

What the result does support is narrower and still worth having: **on every point
where Phase 2's temporal analysis had something to say, MIW's current answers were
already right.** The temporal layer's value here is for the candidate studying from
older material — not as a defect finder against MIW's own answers.

---

## If one is ever raised

Record: question · claim · current text · problem · authority · severity ·
recommended correction. Then stop. Desktop does not patch candidate-facing answers.
