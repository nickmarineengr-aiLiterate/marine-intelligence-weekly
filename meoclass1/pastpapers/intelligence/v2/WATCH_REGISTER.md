# Watch register — Phase 2 queue

**RESEARCH ONLY.** `current_as_of: 2026-08-17`

---

## A. Current-answer correction candidates

**Evidence only. Nothing patched. Laptop adjudicates.**
Recorded under §48 — Desktop must not modify a current answer on this branch.

### CAC-001 — QP2608-Q2 (and Q1): no antifouling / AFS content

**Severity: MEDIUM–HIGH · Confidence: HIGH that the omission exists**

**Evidence.** The authored QP2608 Q1 and Q2 objects were searched for
`antifoul`, `AFS`, `cybutryne` and `biofoul`. **Zero occurrences in either.**
(`ballast` appears 9 times in Q2, but in the trim/stability sense — the ballast
plan and docking condition — not the BWM sense.)

**Why it matters.** A dry dock is where antifouling is applied and where the AFS
documentation is renewed. MIW's own verified corpus establishes that **two**
controls are in force — organotins, and **cybutryne from 1 January 2023**
(QP2301). An examiner asking about dry-docking preparations and yard
co-operation can reasonably expect antifouling to appear.

**What is NOT claimed.** That the answer is wrong. It is a possible **omission**
in scope. Q2 asks about coordination, delegation and undocking, and an
examiner may not expect antifouling within those limbs. This needs a judgement
about the question's demands, which is Laptop's call.

**Weaker sibling.** Whether the **BWM Convention** belongs in Q1/Q2 is more
arguable — ballast for docking is primarily a stability matter. Recorded at
**LOW–MEDIUM** confidence; do not treat it as equivalent to the AFS point.

**Do not patch on this branch.**

---

## B. Coverage gaps — content MIW does not hold

| ID | Gap | Where it bites |
|---|---|---|
| GAP-001 | **Charterers Contribution Clause** — no verified MIW material at all | QP2608-Q4(d). Least-supported limb in the paper. |
| GAP-002 | **War Risk Clause** under the Marine Insurance Act — no ancestor | QP2608-Q4(c) |
| GAP-003 | **Deviation** under the Marine Insurance Act — no ancestor | QP2608-Q4(a) |
| GAP-004 | **Laid-up notation** vs intermediate/annual/special survey cycle — no ancestor | QP2608-Q1(b), 6 marks |
| GAP-005 | **HV/LV switchboard, isolation, permit to work, power restoration** — nothing in the corpus 2021–2026 sets a switchboard or HV question | QP2608-Q7, entire 16 marks |
| GAP-006 | **Cargo abandonment** (as distinct from abandonment of the ship as wreck) | QP2608-Q3(b) |

GAP-005 is the largest single hole: a whole question with no corpus ancestor.

---

## C. Instrument identities to establish

| ID | Item | Status |
|---|---|---|
| INS-001 | Enclosed-space entry and rescue drill requirements — controlling instrument | MIW deliberately refers **descriptively, not by number** (QP2311) because identity could not be established from a held source. **Do not supply a number until it is.** |
| INS-002 | Biofouling / in-water hull cleaning discharge controls — instrument and status | MIW holds biofouling material but the controlling instrument was not verified this session |

---

## D. Acquisition to retry

| ID | Target | Why | Status |
|---|---|---|---|
| ACQ-001 | **DG Shipping question bank** `SRC-DGS-QBANK` | Official tier; would replace the user-upload source under H1/H2/H3 | `ECONNREFUSED` all session — retry |
| ACQ-002 | Re-source the **July 2012** attestation | H1/H2/H3 currently rest on one third-party upload that direct HTTP cannot even retrieve (3 KB stub) | open |
| ACQ-003 | DG Shipping **live notice archive** | Settle the NTA verdict against the primary archive | unreachable — retry |
| ACQ-004 | 2010 papers specifically | **Warning:** DieselShip 2010 sets hold only 10–25 questions across 7 categories vs 52–66 for 2011–2012. Buying access may **not** resolve 2010. Verify before any spend. | advisory |

---

## E. Model work for Phase 2

1. **Re-key occurrences on `(question_id, limb_label)`.** Question-level keys
   both under- and over-report on this paper. This is the single most important
   change.
2. **Always report recurrence mark-weighted as well as question-wise.**
   4/9 questions vs ~17% of marks describe the same paper very differently.
3. **Do not build a numeric revival score.** See `SIMILARITY_MODEL.md`.
4. **Keep the four provenance tiers.** The distinction between a text comparison
   and a recollection is what this whole layer rests on.
5. Decide placement of the temporal block — Study Guide vs Exam Plan
   (see `BULLET_CONNECTION_PILOT.md`).

---

## F. Standing cautions

- **MIW's evidence floor is January 2021.** Any statement of the form "asked
  since 2010" is unsupported today, whoever says it.
- **Dormancy is partly an artefact.** "Not seen for 14 years" means "not seen in
  the window MIW can see". Never publish it as an examining fact.
- **`TOPIC_ONLY` is not a repeat.** It is the class that inflates statistics.
- **DieselShip is a historical source, never MIW's answer authority.**
