# Examiner Index V2 — Deterministic Generator Contract

**Status: designed, NOT published.** No generator is built in this phase and no live page is
touched. This document is the contract the next phase implements once the Founder authorises
regeneration.

The defect this contract exists to end: `meoclass1/examiner-index.html` is a hand-uploaded page
whose header says **791**, whose mini-nav sums to **809**, and which actually renders **863** rows.
Three of four count layers are stale because every count is typed by hand. A generator that derives
every number from the records it writes cannot drift.

---

## 1. Inputs

All four are records in `meoclass1/oral-intelligence/examiner-audit/`, never a rendered page.

| Input | File | Owns |
|---|---|---|
| Canonical live inventory | rebuilt from live HTML at run time (`oral_lib.build_inventory`) | question text, anchor, file, URL, answer existence |
| Examiner relationships | `CURRENT_EXAMINER_RELATIONSHIPS.jsonl` (+ approved additions) | which examiner is connected to which question |
| Evidence | `EXAMINER_EVIDENCE_LEDGER.jsonl`, `EXAMINER_EVIDENCE_LEDGER_V2.jsonl` | why MIW believes each relationship |
| Source occurrences | `ALL_SURVEYORS_SOURCE_RECORDS.jsonl`, `ORAL_788_RECONCILIATION.jsonl` | reported wording, follow-ups, expected detail |

**The live HTML is re-parsed on every run.** `qb_content_index.json` is never an input: it carries an
off-by-one insertion shift in `QB2_B` and `QB1_B` and five files that no longer exist.

## 2. Output

1. `meoclass1/examiner-index.html` — the full candidate index.
2. Later, from the same pass: `SQ/examiner-index.html` (commerce teaser) and per-question
   "Asked By" metadata on the QB cards.

Both surfaces must be emitted by **one** data pass. The current split is why the sales page still
advertises "791+", "Simon 212" and "Paul Sir — All 10 Questions" against a live 19.

## 3. Derivation rules

- Every count — header total, per-examiner subtotal, mini-nav pill, tier tally — is `len()` of the
  records being rendered. **No literal may be hand-entered anywhere in the template.** Not 791, not
  809, not 863, not any examiner subtotal.
- A relationship renders only if its `question_id` resolves against the live inventory parsed in the
  same run. An unresolvable relationship is a build failure, not a skipped row.
- Display text comes from the **live question**, never from the stored index wording. The 35 blank
  rows and 12 drifted rows in the current page are both consequences of storing display text.
- The tier badge renders `research_best_tier`, mapped to the candidate-facing vocabulary. Every tier
  literal emitted must have a matching toggle in `filterTier()`; a literal without a toggle is a
  build failure. This is what made two `cetip` rows vanish on first filter use.
- A relationship appears once. Multiple evidence records collapse into one row with an evidence
  count, never into duplicate rows.

## 4. Tier mapping

| Research tier | Candidate-facing badge | Meaning |
|---|---|---|
| `MULTI_SOURCE_CONFIRMED` | Confirmed | two or more independent primary records |
| `PRIMARY_CONFIRMED` | Confirmed | one primary candidate record |
| `EXTERNAL_SOURCE_CONFIRMED` | Reported | external surveyor compilation only |
| `CE_TIP` | CE tip | page-declared attribution, not tracker-confirmed |
| `HEADER` | Page metadata | attribution from page header only |
| `INFERRED_ONLY` | Topic inference | no primary record, no page assertion |

`CE_TIP` must never silently render as Confirmed — the Founder's standing decision. The July
per-examiner sheets never raise a tier: they are `DERIVED_PRODUCT_SURFACE` and overlap the index on
824 of 862 pairs, so counting them is circular.

## 5. Build gate

The generator runs only if `validate_phase2.py` passes, and re-runs it against its own output:

- every rendered `question_id` resolves to a live question, file and anchor;
- no duplicate relationship ids and no duplicate rendered rows;
- header total == mini-nav sum == rendered row count == `len(relationships)`;
- every emitted tier literal has a filter toggle;
- no row renders empty display text.

Any failure aborts the build without writing. The page is regenerated, never patched.

## 6. Commerce surface — recorded, deferred

`SQ/examiner-index.html` publishes stale marketing numbers ("791+", "Simon 212", "Paul Sir — All 10
Questions", "62+ QB Files" against a live 86). The Founder has authorised eventual correction but
**not now**: canonical examiner coverage is about to change substantially, so correcting the sales
page before regeneration would produce a second stale number a week later. Correct it in the same
data pass as the index, once.
