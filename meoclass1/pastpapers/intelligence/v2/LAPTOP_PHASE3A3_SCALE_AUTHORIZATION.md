# Laptop independent review — Question Intelligence V2, Phase 3A.3

**Reviewed** 2026-08-18 · **Verdict: GO — Phase 3B authorised**

| | |
|---|---|
| Canonical repo | `F:\Marine-Intelligence-Weekly` |
| `origin/main` | `3b55bfb` (clean, untouched) |
| Research tip reviewed | `53a04ee` |
| Delta base | `b16cf18` (the Phase-3A.2 HOLD state) |
| Prior review | `6a6b6a4` (`review/question-intelligence-v2-phase3a2`) |
| This review | `review/question-intelligence-v2-phase3a3` |
| Worktree | **C:** drive — a genuinely different drive letter from the canonical **F:** repo |

Every figure below was recomputed on the Laptop in a clean worktree. No Desktop
output was accepted as evidence of itself.

---

## 1. Delta scope — clean

Three commits, exactly as reported, and no more:

```
fd69c17 fix(qi-v2): anchor instrument reference suppression
79bfb0a fix(qi-v2): make the adversarial harness Windows-console safe
53a04ee test(qi-v2): guard technical magnitudes against substring suppression
```

Four files, all inside `intelligence/v2/`:

| File | Change |
|---|---|
| `tools/qi_similarity.py` | +22/−3 — the regex, and its reasoning |
| `tools/adversarial_controls.py` | +236 — new controls, cp1252 safety |
| `PHASE3A3_REPAIR_REGISTER.md` | new |
| `README.md` | control counts 52→66, 21→41 |

**No contamination.** Nothing touched in pastpaper specs, solvedQP, oralnotes,
commercial, payments, refunds, entitlements, homepage, magazine, source bank
data, source manifest or question-family data.

---

## 2. The old defect — reproduced from the old commit, on fresh stems

The `b16cf18` expression was rebuilt in isolation and run against ten
Laptop-authored stems that appear nowhere in Desktop's control file. Six lost a
technical magnitude outright:

| Stem | Should read | `b16cf18` read |
|---|---|---|
| the regulating valve opens at 6.5 bar | 6.5 bar | **nothing** |
| the trip mechanism operates at 7.5 bar | 7.5 bar | **nothing** |
| normal alarm level is 80 ppm | 80 ppm | **nothing** |
| filter shall not be coarser than 40 microns | 40 microns | **nothing** |
| there is no more than 25 microns clearance | 25 microns | **nothing** |
| the register is updated at 1000 kW load | 1000 kW | **nothing** |

Three further stems (`nozzle`, `regular`, `registration`) survived `b16cf18` only
because the offending fragment sat more than 24 characters from the number.
They were saved by the window, not by the expression — which is the clearest
statement of why the defect was real and why its measured incidence was zero.

**A second defect, not previously reported, was found in the same expression.**
Under `b16cf18` the genuine reference `Reg. 14` was *not* suppressed and leaked
as `COUNT 14`, because `reg` was followed by `\s*` and the period blocked the
match. So the old form was wrong in **both** directions — it erased quantities
that mattered and admitted designators that did not. The adopted `\b…\b\.?`
closes both with one change.

---

## 3. The adopted regex

```python
_INSTRUMENT_NUM = re.compile(
    r'(?:\b(?:solas|marpol|stcw|colreg|load\s*line|tonnage|ilo|mlc|isps|ism|'
    r'annex|chapter|regulation|reg|convention|protocol|amendment)\b\.?'
    r'|\bno\.)\s*[^.;]{0,24}$', re.I)
```

Boundaries on **both** sides of every ordinary lexical token; `no` alone carries
a **required** period, because bare `no` is a negation and negations sit in front
of exactly the magnitudes that matter. The reasoning is correct, and it is
written down in the file.

## 4. Fresh false-trigger tests — 10/10 survive

`nozzle` · `regular` · `regulating` · `registration` · `mechanism` ·
`isometric` · `normal` · `not` · bare `no` · `register` — every technical
magnitude survives parsing under `53a04ee`. Zero failures.

## 5. Genuine instrument references — 10/10 still suppressed

`reg 14` · `Reg. 14` · `regulation 28` · `ISM 9` · `annex 6` · `chapter 5` ·
`SOLAS 74` · `No. 4` · `MARPOL 73` · `amendment 12` — all correctly read as
designators, none reaching magnitude logic. The repair does not regress the
suppression purpose; it extends it.

## 6. Paired classifier consequence — the fix has real effect

| Pair | `b16cf18` | `53a04ee` |
|---|---|---|
| filter "not coarser than" **40 vs 20 microns** | `EXACT_REPEAT` ✗ | `SAME_CORE_ASK` ✓ |
| nozzle opening pressure **320 vs 250 bar** | `NEAR_VERBATIM` ✗ | `SAME_CORE_ASK` ✓ |
| **320 vs 320 bar** (control) | `EXACT_REPEAT` | `EXACT_REPEAT` ✓ |
| regulating valve **6.5 vs 6.5 bar** (control) | `EXACT_REPEAT` | `EXACT_REPEAT` ✓ |
| **Reg. 14 vs Reg. 28**, same ask | `SAME_CORE_ASK` (false conflict) ✗ | `EXACT_REPEAT` ✓ |

Load-bearing values now separate; identical values stay compatible; differing
*designators* over an identical ask no longer manufacture a conflict.

## 7. The Laptop's own 3A.2 proposal fails — Desktop improved the repair

The leading-boundary-only form this review proposed at Phase 3A.2 was rebuilt
and tested independently. It **still** loses `regulating` (and
`regular`/`registration` whenever they fall inside the 24-character window), and
it still leaks `Reg. 14`. Desktop did not deviate from the review; it corrected
it.

## 8. Regex mutation harness — 3 mutations, 0 escapes

Each defective form breaks at least one permanent control, reproduced
independently:

| Mutation | Breaks |
|---|---|
| unanchored substring (the 3A.2 defect) | 16 controls |
| leading boundary only (the Laptop proposal) | 5 controls |
| period dropped from `no.` | 2 controls |

## 9. Windows console — crash closed

| | exit | result |
|---|---|---|
| `b16cf18` harness, `PYTHONIOENCODING=cp1252` | **1** | `UnicodeEncodeError: '\u03bc'` |
| `53a04ee` harness, `PYTHONIOENCODING=cp1252` | **0** | clean |

Output under cp1252 and utf-8 is **byte-identical**, not merely semantically
equal.

## 10. Suites — clean worktree, different drive, no Desktop inputs

| Suite | Reported | Reproduced |
|---|---|---|
| validator checks / skips / failures | 202 / 0 / 0 | **202 / 0 / 0** ✓ |
| validator mutations / escapes | 48 / 0 | **48 / 0** ✓ |
| classifier controls / failures | 66 / 0 | **66 / 0** ✓ |
| parser cases / failures | 41 / 0 | **41 / 0** ✓ |
| classifier mutations / escapes | 15 / 0 | **15 / 0** ✓ |
| regex mutations / escapes | 3 / 0 | **3 / 0** ✓ |

Counts rose only where 3A.3 added test-only coverage (52→66 controls, 21→41
parser cases). No decrease anywhere.

## 11. Required bank extract — still fails closed

| | exit | |
|---|---|---|
| present | 0 | 202 checks, 185 items |
| **deleted** | **1** | C46 `REQUIRED_SOURCE_MISSING`; C32/C33/C34/C40/C41/C42 report **`unavailable`**, not skipped |
| restored | 0 | 202 checks, 0 failures |

C46/C47 semantics intact. Paths resolved correctly from a **C:** worktree — the
`D:` hardcoding defect of Phase 3A.1 stays closed under a real drive change.

## 12. Numeric, range and mark regression — 22/22

`70 N` vs `100 N` · `25` vs `10 microns` · `180` vs `380 cSt` · `3` vs `12 NM` ·
`440` vs `1000 V` · `5` vs `10 bar` · `15` vs `5 ppm` · `0.50%` vs `0.10%` ·
`2` vs `3 years` — all load-bearing. `(4)` vs `(6)` correctly excluded as mark
allocations. Magnitudes read at 1, 9, 10, 21, 25, 70, 100, 999, 1000, 2500 and
0.5 alike: **the small-number gate has not returned.**

## 13. Prior hardening — green

`DESCRIBE` vs `CRITICISE`, required vs not-required, the short-stem floor, the
wrong-but-valid bank ancestor, duplicate occurrence ids, the fake historical date
from bank-only evidence, `FAMILY-EM-0008`/`EM-0009`, and the C45 dated-filename
guard are all present and passing inside the green suites.

## 14. Sweep and Paper DNA — coherent, and provably unmoved

Sweep: **45** exact/near · **37** same-core · **82** reportable.

Row movement from `b16cf18` was tested by rebuilding the old extractor in place
and re-running the sweep: the two outputs are **byte-identical — zero rows
moved.**

QP2608 Paper DNA recomputed from the sweep rows:

| Question | Counted as | Marks |
|---|---|---|
| Q1(a) | `EXACT_REPEAT` | 10 |
| Q2 whole | `EXACT_REPEAT` | 16 |
| Q4 whole | `NEAR_VERBATIM` | 16 |
| Q8(b) | `EXACT_REPEAT` | 6 |
| | **48 / 144 = 33.3%** | |
| Q8(a) | `SAME_CORE_ASK` | +10 |
| | **58 / 144 = 40.3%** | |

Double-count suppression verified: Q1 is counted at its limb (10), not the whole
16; Q8 is counted as (a)+(b)=16, never limb *and* whole.

---

## 15. Findings — both non-blocking, record only

**L3A3-1 — plural `Regs` is not recognised as a designator.**
`"Regs 14 and 15 apply"` yields `COUNT 14, COUNT 15`. The error direction is the
**safe** one: a leaked designator manufactures a false conflict and *demotes* a
true repeat, so it under-reports rather than over-reports — the opposite of the
3A.2 defect. Incidence in classifier-visible text is **zero**: 0 hits in the
185-item bank extract, 0 in `QUESTION_OCCURRENCES.jsonl`, and all 43 hits across
the 40 paper specs sit in answer-side fields (`recall_15s`, `points`,
`critical_numbers`) that the classifier never reads. Per the 3A.2 lesson —
*zero incidence today is not zero at scale* — this belongs on the
`WATCH_REGISTER` for Phase 3B ingestion, not in another hardening phase.

**L3A3-2 — `README.md` status prose is stale.**
It states "Nothing is even `DATE_VERIFIED`", but two families now carry
`DATE_VERIFIED`. This pre-dates `b16cf18` and is outside the 3A.3 delta; the data
itself is internally consistent (C21 green). Documentation drift only.

**Accepted limit (§18).** Coordinated modification of an uncited bank item plus
its manifest sha plus its byte count can evade semantic checks until that item
becomes a cited ancestor. Founder has accepted this. Git history protects
repository integrity, the source hash protects normal drift, semantic checks
protect cited ancestors, and Phase 3B naturally expands semantic coverage. **No
new integrity architecture.**

## 16. Product safety

| | |
|---|---|
| QI integrated into the website | **NO** — no candidate-facing page references the layer |
| `CANDIDATE_PUBLISHED` | **none** (0 occurrences) |
| Candidate pages changed | none |
| Bullet Exam Plan | untouched |
| Commercial / payments / refunds / entitlements | untouched |
| Magazine | untouched |
| Research integration | **branch-only** — `53a04ee` is not an ancestor of `origin/main` |
| W-1 / W-2 | left record-only |

---

## Verdict

**GO — QUESTION INTELLIGENCE V2 PHASE 3A.3 INDEPENDENTLY VERIFIED AND PHASE 3B
AUTHORISED.**

The anchored expression passes fresh false-trigger cases, preserves genuine
instrument suppression, catches every defective mutation, no longer crashes a
stock Windows console, keeps the full suite green from a clean cross-drive
worktree, still fails closed when the required bank source is removed, and moves
no sweep row. No further hardening phase is warranted.
