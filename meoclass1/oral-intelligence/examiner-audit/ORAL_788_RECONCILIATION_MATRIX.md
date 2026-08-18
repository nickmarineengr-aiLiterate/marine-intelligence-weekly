# Oral 788-Question Reconciliation Matrix (Phase 2)

**Date:** 18 August 2026 · **MEO Class 1 orals: 24 August 2026**  
**Branch:** `research/oral-examiner-intelligence-v1-reconcile`  
**Baseline:** Phase 0/1 audit @ `d8ed9e6`

Every number here is derived from the records in this folder. None is typed by hand.

---

## 1. Global reconciliation

| Layer | Count |
|---|---|
| Raw source occurrences ingested | 788 |
| Normalised source families | 731 |
| Live Oral QB questions compared against | 681 |
| Examiner relationships recovered from the index | 862 |
| Source occurrences dispositioned | 788 |
| Cross-examiner families | 26 |
| Gap families (genuine + material partial) | 311 |
| Human review queue | 87 |

## 2. Content coverage of the 788

| Disposition | Occurrences |
|---|---|
| EXACT_MATCH | 23 |
| NEAR_MATCH | 41 |
| SAME_CORE_ASK | 69 |
| PARTIAL_COVERAGE | 364 |
| MISSING | 204 |
| AMBIGUOUS | 87 |

## 3. Examiner mapping (independent of content)

| Status | Occurrences |
|---|---|
| ALREADY_LINKED | 161 |
| NEW_LINK | 336 |
| CONFLICTING_LINK | 0 |
| UNMAPPED | 87 |
| NOT_APPLICABLE | 204 |

Unique new examiner→question pairs proposed: **291**. Already-linked pairs confirmed by the external source: **127**.

## 4. Surveyor-by-surveyor matrix

| Examiner | Raw occ. | Families | Exact | Near | Same core | Partial | Missing | Ambiguous | Already linked | New links | Conflicts | P0 gaps |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| John | 129 | 127 | 6 | 6 | 10 | 60 | 28 | 19 | 0 | 77 | 0 | 3 |
| Simon | 256 | 241 | 5 | 18 | 21 | 119 | 57 | 36 | 64 | 85 | 0 | 3 |
| Nair | 300 | 292 | 6 | 10 | 27 | 130 | 106 | 21 | 94 | 63 | 0 | 9 |
| Paul | 103 | 99 | 6 | 7 | 11 | 55 | 13 | 11 | 3 | 66 | 0 | 0 |
| **Total** | 788 | 731 | 23 | 41 | 69 | 364 | 204 | 87 | 161 | 291 | 0 | 15 |

## 5. Relationship types

| Type | Occurrences |
|---|---|
| PRIMARY_ASK | 610 |
| FOLLOW_UP | 172 |
| EXPECTED_DETAIL | 6 |

## 6. Gap candidates

| Priority | Genuine gap | Material partial |
|---|---|---|
| P0 | 15 | 0 |
| P1 | 62 | 0 |
| P2 | 119 | 10 |
| P3 | 0 | 105 |

## 7. Ready connections, re-verified

| Status | Pairs |
|---|---|
| NEEDS_REVIEW_WEAK_PROSE | 205 |
| READY_BUT_CE_TIP_ONLY | 81 |
| READY_VERIFIED_MULTI_SOURCE | 46 |
| READY_VERIFIED | 38 |

## 8. Inference-only relationships

| Disposition | Pairs |
|---|---|
| STILL_INFERRED | 267 |
| PROMOTED_BY_EVIDENCE | 42 |

`CONFLICTED` is deliberately zero: the external compilation can corroborate an inference, but its silence about a pair is absence of evidence, not contradiction.

## 9. Recovered index defects

| Defect | Count | Resolution |
|---|---|---|
| Blank display rows | 35 | question text recovered from live HTML into the relationship ledger |
| Invalid `cetip` tier literals | 2 | intended tier `ce_tip` recorded in `repaired_tier` |
| Duplicate relationship | 1 | one relationship, two index rows, both kept as evidence |
| Display-text drift rows | 12 | live text is canonical; index wording kept as a historical variant |

## 10. July workbook status

The July per-examiner sheets overlap the recovered relationships on **824** of **862** pairs. They are carried as `DERIVED_PRODUCT_SURFACE` and are excluded from every evidence-strength calculation in this phase. Counting them would be circular.

