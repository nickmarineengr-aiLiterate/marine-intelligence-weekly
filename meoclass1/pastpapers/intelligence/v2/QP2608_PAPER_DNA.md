# QP2608 Paper DNA — recomputed in Phase 2

**RESEARCH ONLY — these counts must NOT be published.**
`current_as_of: 2026-08-17`
August 2026, Engineering Management, MEO Class I. Printed serial `EM-17826-1`.

> **Phase 2 changed this materially.** Phase 1 estimated roughly **25 of 144 marks
> (~17%)**, with the `Q2` component inferred from a third-party source. Measured
> against the Directorate's own published question bank, the verified figure is
> **48 of 144 marks (33.3%)** — nearly double, and no longer inferred. Two Phase-1
> findings were overturned in the process.

Classification is now against the **official DG Shipping question bank**
(`SRC-DGS-QBANK-ARCHIVED`, 185 items) plus MIW's own holdings — 2021–2026 solved and
2021–2023 intelligence-only. It is still *not* against the 2010–2012 sittings,
because those remain unreadable (see `HISTORICAL_COVERAGE_MATRIX.md`).

---

## 1. The mark base

The paper offers **9 questions × 16 = 144 marks**. Candidates *answer six*, so a
script totals **96**. Both denominators are reported, because they answer different
questions: coverage of the paper *as set* is measured against 144, and what a
candidate actually needs is measured against 96.

Every mark below is **`KNOWN`** — printed on the paper. Nothing is estimated. The
`UNAVAILABLE` figures in these families sit in the historical layer, where MIW holds
question text without printed marks; those stay `UNAVAILABLE` and are never
inferred.

---

## 2. Count view — whole questions

| | Questions | of 9 |
|---|---|---|
| Whole question has an official ancestor | **2** (`Q2`, `Q4`) | 22.2% |
| Partly ancestored, at limb level | **2** (`Q1`, `Q8`) | 22.2% |
| No ancestor located | **5** (`Q3`, `Q5`, `Q6`, `Q7`, `Q9`) | 55.6% |

**The count view is the misleading one and is never published alone.** “4 of 9
questions have an ancestor” is true, and would lead a candidate to over-prepare `Q1`
and `Q8`, where only part of the marks recur.

---

## 3. Mark-weighted view

| Q | Limb | Marks | Ancestor | Class | text / date conf. |
|---|---|---|---|---|---|
| `Q1` | (a) | **10** | `BANK-015` | `EXACT_REPEAT` | HIGH / **NONE** |
| `Q1` | (b) | 6 | — | none located | — |
| `Q2` | whole | **16** | `BANK-018` | `EXACT_REPEAT` | HIGH / **NONE** |
| `Q3` | (a)(b) | 16 | — | none located | — |
| `Q4` | whole | **16** | `BANK-072` | `NEAR_VERBATIM` | HIGH / **NONE** |
| `Q5` | — | 16 | — | none located | — |
| `Q6` | — | 16 | — | none located | — |
| `Q7` | — | 16 | — | none located | — |
| `Q8` | (a) | *10* | `BANK-105` | `SAME_CORE_ASK` | MEDIUM / **NONE** |
| `Q8` | (b) | **6** | `BANK-054` | `EXACT_REPEAT` | HIGH / HIGH |
| `Q9` | — | 16 | — | none located | — |

| Measure | Marks | of 144 |
|---|---|---|
| `EXACT_REPEAT` + `NEAR_VERBATIM` | **48** | **33.3%** |
| plus `SAME_CORE_ASK` (`Q8(a)`) | **58** | **40.3%** |
| No ancestor located | 86 | 59.7% |

Against the 96 marks a script actually carries, the four questions holding an
ancestor (`Q1`, `Q2`, `Q4`, `Q8`) are **64 of those 96** — but only **48 of the 64**
are themselves ancestored. **That gap is the entire reason the mark-weighted view
exists**, and it is exactly what a count-based statistic conceals.

---

## 4. What Phase 2 overturned

**`Q2` — the largest single correction.** Phase 1 held that *“roughly two thirds of
the 16 marks have no ancestor”*, because the only source then available carried the
Master-coordination sentence alone. `BANK-018` carries **all three limbs** —
coordination with the Master, preparations and delegation to the engineers, and
inspections and co-operation for undocking — and matches the whole question at
containment **1.00 / 1.00**. All 16 marks have an official ancestor. The Phase-1
error was caused by the unpreserved third-party excerpt, not by the method.

**`Q4` — three limbs recovered.** Phase 1 recorded limbs (a) Deviation, (c) War Risk
Clause and (d) Charterers Contribution Clause as having *“NO ancestor anywhere in
MIW's holdings”*, and called (d) *“the least-supported limb in the whole paper”*.
`BANK-072` is `Q4` in full — all four limbs, in that order, essentially verbatim.
All 16 marks have an official ancestor.

**`Q8(a)` — an ancestor found by measuring backwards.** Phase 1 recorded no
ancestor. Forward containment is 0.48, so a one-directional test discards it;
**reverse containment is 0.96**. `BANK-105` sits inside the modern limb almost
entirely, and August 2026 then wraps it in a PSC-failure scenario. 10 marks.

---

## 5. Verified versus provisional

**Verified** — official ancestor, `PRESERVED_RAW` artefact, sha256 pinned:
`Q1(a)`, `Q2`, `Q4` (all four limbs), `Q8(a)`, `Q8(b)` — 58 marks.

**Provisional / research-only:**

- `Q8(a)`'s class is `MEDIUM`. The ancestor is certain; the added scenario is
  substantial enough that adjudication could yet move it to `TOPIC_ONLY`.
- **Every date is provisional.** The bank is undated. `Q8(b)` is the only limb whose
  earlier *sittings* are dated, and only back to MIW's March 2021 evidence floor.

**Withdrawn since Phase 1:** the asserted **July 2012** sitting behind `Q1` and `Q2`.
The recurrence survived and strengthened; only the date fell. See
`SRC-SCRIBD-106245627` in `SOURCE_MANIFEST.json`.

---

## 6. What this paper does and does not support

Supported, internally:

- 48 of 144 offered marks reproduce an item of the Directorate's own question bank
- `Q2` and `Q4` reproduce a bank item **in full**
- `Q8` is **not** a repeat: limb (b) is, limb (a) is a different and weaker family,
  and they carry 6 and 10 marks respectively

Not supported by anything:

- that any of these was asked in June 2010, December 2011, October 2012, April 2010,
  March 2010 or July 2012
- that any question was “dormant” for any period
- any numerical revival score

---

## 7. Corpus context — do not generalise from this paper

`QP2608` has **7 strong bank matches, the most of any paper in the corpus**. Across
all 40 solved papers there are **63**, spread over **21** papers; the median matched
paper has 2.

`QP2608` is unusually bank-derived. A candidate-facing framing built on this paper
alone would overstate how much of a normal Engineering Management paper recurs.
