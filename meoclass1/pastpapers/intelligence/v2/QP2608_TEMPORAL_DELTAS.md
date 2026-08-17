# QP2608 temporal answer deltas — pilots

**RESEARCH ONLY.** `current_as_of: 2026-08-17` · comparison target **August 2026**

> If this old question is asked today, what changes in the answer?

Three pilots. Two are required by §46 to prove the model separates the cases:
one repeated question whose answer is **substantially unchanged**, and one whose
answer has **materially changed** because of regulation.

**No third-party answer was consulted.** Deltas are stated against MIW's own
verified corpus, and anything MIW could not establish is marked
`UNCERTAIN_NEEDS_PRIMARY` rather than filled in.

### Prior art in the repo

This layer is not a new idea for MIW — it generalises something the corpus
already does per-question. QP2304 carries an explicit instruction that the 10%
indicative moisture limit from CCC.1/Circ.2 (20 October 2015) **must not be
quoted as current**, because CCC.1/Circ.2/Rev.1 (20 September 2017) supersedes it
and carries no such limit. That is exactly a `do_not_write_today` entry. v2's
contribution is to lift this from one question's notes to a **family-level layer**
that travels with a recurrence.

---

## PILOT A — the substantially UNCHANGED answer

### FAMILY-EM-0003 · QP2608-Q8(b) · motivation, attitude, competitiveness

**Answer impact: `NONE`**

**Asked before** — earliest MIW-attested March 2021 (QP2103-Q7); also April 2022
(QP2204-Q4); most recently **December 2025** (QP2512-Q4, solved).
**Current recurrence:** August 2026 Q8(b). **Similarity:** `EXACT_REPEAT` (limb).
**Dormancy:** 8 months — `ACTIVE_RECURRENCE`.

**What still stands today**
- The whole answer. This is a human-factors question about motivation,
  attitude and competitiveness aboard, and nothing in its content is
  regulation-dated.
- The verified answer behind QP2512-Q4 transfers directly.

**What changed** — nothing in the answer. Two things changed in the **question**:
- The Maslow limb that preceded it in every earlier appearance is **absent**.
- Marks fall **16 → 6**.

**Do NOT write today**
- Do **not** open with Maslow's hierarchy. It is not asked in August 2026, and
  at 6 marks it would crowd out what is.

**State today** — the same management substance as December 2025, compressed to
6 marks' worth.

**Why this pilot matters:** it proves the model can return "nothing changed".
A temporal engine that finds a delta in every old question is broken, and would
teach candidates to distrust it.

> ⚠ The one real risk here is not legal drift but **mark drift**: the recurrence
> is 6 of Q8's 16 marks. Limb (a) — PSC failures, multinational crew
> communication, shore instructions — carries 10 marks and is **not** a repeat.

---

## PILOT B — the MATERIALLY CHANGED answer

### FAMILY-EM-0002 · QP2608-Q2 · dry dock, coordination with the Master

**Answer impact: `MODERATE`**

**Asked before** — July 2012 (`SRC-SCRIBD-106245627`).
**Current recurrence:** August 2026 Q2. **Similarity:** `SAME_CORE_ASK`
(limb 1 `NEAR_VERBATIM`). **Dormancy:** ~14 years to the previous *known*
appearance — `LONG_DORMANT_REVIVAL`, with the evidence caveat in
`QUESTION_FAMILIES.json`.

**What still stands today**
- The coordination itself: docking plan and block layout, docking drafts and
  trim, stability and free-surface condition, tank soundings and residues,
  bottom-plug and sea-suction arrangements.
- The Master/Chief Engineer interface: agreed docking condition, ballast plan,
  timing, who signs what, shore-side services on landing (power, fire main,
  gangway, communications), hot-work control, mooring and yard interface.
- Engineering substance of the undocking checks: flooding-up sequence, sea
  connections, tightness, running-up of machinery.
- None of this is regulation-dated, and a good July 2012 answer would still
  score for all of it.

**What changed since July 2012**

| Delta | Was (Jul 2012) | Is now | In force | Source | Tier | Conf. |
|---|---|---|---|---|---|---|
| `NEW_REQUIRED_POINT` — ballast water | BWM Convention 2004 adopted but **not in force**; ballast handling for docking was operational only | Ballast operations sit under a **certificated regime** — approved BWM Plan, International BWM Certificate, treatment system surveyed | **8 September 2017** | MIW verified corpus (QP2308, QP2412): "Ballast Water Management Convention 2004 (adopted 13 February 2004, in force 8 September 2017)" | 1 | HIGH |
| `NEW_REQUIRED_POINT` — antifouling | Organotin control only | **Cybutryne** also controlled; antifouling selection and the AFS declaration/certificate at repaint must reflect it | **1 January 2023** | MIW verified corpus (QP2301): "the two controls in force — organotins, and cybutryne from 1 January 2023" | 1 | HIGH |
| `UPDATED_OPERATIONAL_PRACTICE` — enclosed space | Entry into tanks/voids during docking governed by SMS procedure | Entry and rescue drill requirements have since been tightened | not established | MIW refers to the Organization's enclosed-space recommendations **descriptively and not by resolution number**, because the current instrument identity could not be established from a held source (QP2311). That discipline is inherited here. | — | `UNCERTAIN_NEEDS_PRIMARY` |
| `UPDATED_OPERATIONAL_PRACTICE` — hull cleaning / biofouling | Not a discharge question | Biofouling and in-water/hull-cleaning discharge controls now bear on the docking and cleaning plan, with local port restrictions | not established | MIW holds biofouling material (QP2301, QP2306, QP2307, QP2412) but the controlling instrument and its status were **not** verified this session | — | `UNCERTAIN_NEEDS_PRIMARY` |

**Do NOT write today**
- Do **not** describe ballast exchange/discharge for docking as a purely
  operational matter with no certificate behind it. That was true in July 2012
  and has been wrong since 8 September 2017.
- Do **not** present antifouling compliance as organotin-only. Since
  1 January 2023 that answer is incomplete.

**State today**
- Ballast handling for the docking condition is planned against the **approved
  BWM Plan**, with the **International BWM Certificate** and treatment system
  part of the yard/survey interface.
- Antifouling specified at repaint must satisfy **both** controls in force —
  organotins **and cybutryne (from 1 January 2023)** — with the AFS
  documentation updated accordingly.
- Enclosed-space entry during docking follows the ship's SMS and the
  Organization's current recommendations. **State the practice, not a resolution
  number**, until the instrument identity is established from a held source.

**Why MODERATE and not MAJOR:** the answer's *structure* is unchanged and the
bulk of a July 2012 answer still scores. What has changed is additive — two
compliance limbs that did not exist and that a candidate working from an old
answer would simply omit. That is lost marks, not a wrong answer.

---

## PILOT C — FAMILY-EM-0001 · QP2608-Q1 · lay-up reactivation

**Answer impact: `MINOR`** (limb (a)); limb (b) is **not a temporal question**

**What still stands** — the engineering core is intact: de-preservation, tank
and sea-suction inspection, lubrication and turning gear, insulation resistance
and drying out, sea trials and running-up, statutory and class surveys ranged
before offering the ship.

**What changed** — same BWM and AFS deltas as Pilot B where the reactivation
involves ballast systems and repainting; both HIGH-confidence and tier 1.

**Do NOT write today** — as Pilot B.

**Note on limb (b):** how a laid-up notation affects the intermediate, annual
and special survey cycle has **no historical ancestor**, so there is nothing to
compare it against. It is a **coverage gap**, not a delta, and belongs in
`WATCH_REGISTER.md`.

---

## Summary

| Family | Question | Impact |
|---|---|---|
| FAMILY-EM-0003 | Q8(b) motivation | **NONE** |
| FAMILY-EM-0001 | Q1(a) lay-up reactivation | **MINOR** |
| FAMILY-EM-0002 | Q2 dry dock | **MODERATE** |
| FAMILY-EM-0004 | Q4(b) warranties | not analysed — Phase 2 |

Counts: **NONE 1 · MINOR 1 · MODERATE 1 · MAJOR 0.**

No `MAJOR` appears among the confirmed families, and that is an honest result
rather than a gap in the method. The questions in this paper that *would* score
`MAJOR` — Q6 (scrubbers, discharge zones, VLSFO economics) and Q9 (CII corrective
action plan) — rest on regulation that **did not exist in 2010–2012**, so they
cannot be historical recurrences at all. The temporal engine has nothing to
compare them to, which is itself the finding: **the most regulation-volatile
questions in the paper are the newest ones.**
