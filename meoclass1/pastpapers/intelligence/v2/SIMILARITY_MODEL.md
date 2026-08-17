# Similarity model — Phase 1

**Research only.** `current_as_of: 2026-08-17`

## Classes (one primary class per comparison)

| Class | Definition | Candidate-facing? |
|---|---|---|
| `EXACT_REPEAT` | Identical stem but for punctuation/formatting/trivial wording | yes, at HIGH |
| `NEAR_VERBATIM` | Same question; small wording, scenario or marks changes | yes, at HIGH |
| `SAME_CORE_ASK` | Wording materially changed; substantially the same answer required | yes, at HIGH |
| `TOPIC_ONLY` | Same subject area, different examination task | **never as "repeated"** |
| `NO_MEANINGFUL_MATCH` | No defensible recurrence | n/a |

`TOPIC_ONLY` is not a repeat and must never be surfaced as one. It is the class
that inflates recurrence statistics if allowed to drift.

## Confidence

| Label | Requires |
|---|---|
| `HIGH` | Both stems read as text, from sources of known identity and date |
| `MEDIUM` | Stems compared but one side's date or source authority is soft |
| `LOW` | Assertion only — a recurrence table, a recollection, a topic argument |

Candidate-facing recurrence eventually requires `HIGH`. Phase 1 retains `MEDIUM`
for review. `LOW` stays research-only.

## Provenance tier — kept separate from confidence

| Tier | Meaning |
|---|---|
| `MIW_TEXT_VERIFIED_RECURRENCE` | Both stems held by MIW, compared as text |
| `EXTERNAL_TEXT_VERIFIED_RECURRENCE` | Historical stem read as text from an external source |
| `DIESELSHIP_ASSERTED_RECURRENCE` | Host metadata only. Never published. |
| `CANDIDATE_ASSERTED_RECURRENCE` | Group/candidate recollection. Never published alone. |

A recurrence table is **not** equivalent to a text comparison. The existing
`host_recurrence_hint` field is tier 3 by construction and the repo already
declines to publish it; v2 keeps that and adds tier 4 for the present feedback.

---

## The main Phase 1 modelling finding: recurrence is often **limb-level**

Question-level classification is the wrong granularity for this paper. Three of
the strongest recurrences in QP2608 are recurrences of a **limb**, not a question:

1. **QP2608-Q8(b)** reproduces one sentence of QP2512-Q4 **word for word** — but
   QP2512-Q4's Maslow limb is absent and the marks fall 16 → 6. Question-level,
   this is not a repeat. Limb-level, it is an `EXACT_REPEAT`.
2. **QP2608-Q2** opens with a near-verbatim reproduction of the July 2012
   dry-dock stem, then adds two limbs (delegation, undocking) that have no
   ancestor. Question-level it looks new; limb-level its first third is old.
3. **QP2608-Q4(b)** (warranties) recurs against QP2312-Q3(b) and QP2606-Q3(b)
   while limbs (a), (c), (d) have no ancestor anywhere in MIW's holdings.

**Recommendation for Phase 2:** the occurrence object must key on
`(question_id, limb_label)`, not `question_id`. A question-level-only model will
simultaneously *under*-report (missing Q8(b), Q4(b)) and *over*-report (calling
Q2 a repeat when two thirds of it is new). Both failures are candidate-visible
and both are avoidable.

A consequence for marks: a limb recurrence carries only its own marks. Q8(b) is
6 marks of a 16-mark question. Telling a candidate "Q8 is a repeat" would be
false in the way that matters — most of Q8 is not.

---

## Matching method

Deterministic normalization → token overlap → key-phrase match → adjudication.
Embedding similarity is **not** permitted to decide a class on its own.

Normalization for fingerprinting only (never overwrites `raw_stem`):
lowercase; collapse whitespace; strip punctuation; British/American spelling
folded (`co-ordination`→`coordination`, `enlist`→`list`); honorifics and role
titles folded (`chief engineer officer`→`chief engineer`); marks annotations
stripped.

**Command verbs are load-bearing and are compared separately.** `state`,
`explain`, `discuss`, `compare`, `evaluate`, `draw`, `prepare`, `analyse` and
`draft` set different tasks. Same topic + different verb is the canonical
`TOPIC_ONLY` signature, and `draft` in particular (QP2608-Q9) demands a
constructed document that `explain` does not.

---

## Negative controls

Required by §45 — for each strong match, a same-topic question that must **not**
classify as a repeat. All three behave correctly.

| # | Modern question | Same-topic distractor | Correct class | Model result |
|---|---|---|---|---|
| NC-1 | QP2608-Q5 — main propulsion stops at sea, full ahead; causes + calm/heavy weather response | QP2403-Q8 / QP2510-Q8 — engines fail to respond to bridge control approaching dock gates | `TOPIC_ONLY` | `TOPIC_ONLY` ✓ |
| NC-2 | QP2608-Q3(b) — when is **cargo** abandoned, and who is liable | QP2104-Q9 / QP2109-Q8 / QP2207-Q3 — abandonment of the **ship** as wreck | `TOPIC_ONLY` | `TOPIC_ONLY` ✓ |
| NC-3 | QP2608-Q9 — **draft** the corrective action plan under MARPOL VI reg. 28.8 | QP2401-Q3 / QP2504-Q6 — explain CII rating and measures to improve it | `TOPIC_ONLY` | `TOPIC_ONLY` ✓ |

NC-1 separates two engine-failure questions by **scenario and demanded limbs**
(control failure under pilotage vs. stopped engine at sea). NC-2 separates two
abandonment questions by **legal object** — cargo under carriage law vs. ship
under the Merchant Shipping Act; a bag-of-words matcher fails this one, which is
why token overlap alone is insufficient. NC-3 separates by **command verb**
alone: identical regulation, identical topic, and `draft` vs `explain` is the
whole difference.

NC-2 and NC-3 are the two that a naive embedding model would most likely get
wrong, and they are the reason adjudication remains mandatory.

---

## Revival score — recommendation

**Do not build a numeric revival score.** A score combining similarity,
frequency, dormancy and return would manufacture false precision on a corpus
whose pre-2021 evidence is almost entirely absent. Any denominator would be
wrong, because "number of known sittings" currently means "number of sittings
MIW happens to hold", which is 2021+.

Use the categorical dormancy classes instead (see `QUESTION_FAMILIES.json`), and
revisit only if the pre-2021 window is ever genuinely acquired.
