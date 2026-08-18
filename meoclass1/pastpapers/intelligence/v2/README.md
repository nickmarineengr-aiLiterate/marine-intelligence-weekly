# Question Intelligence v2 — research layer

**RESEARCH ONLY. NOTHING HERE IS CANDIDATE-FACING.**
`current_as_of: 2026-08-17` · exam target **AUGUST 2026 SITTING**
Phase 2 (Desktop) · retrieval window 2026-08-17 into 2026-08-18

Nothing in this directory renders on a candidate page, gates, prices, feeds an Exam
Plan bullet, appears in a Study Guide, or counts toward solved inventory. The Bullet
Exam Plan architecture is final and was not touched. The Laptop reviews before any
integration.

---

## What this layer answers

Two questions, deliberately kept apart:

1. **Has this question or limb been asked before?**
   → `QUESTION_FAMILIES.json`, `QUESTION_OCCURRENCES.jsonl`, `OFFICIAL_BANK_ITEMS.json`
2. **If it is asked now, what must the candidate write differently?**
   → `TEMPORAL_DELTA_SCHEMA.json`, `QP2608_TEMPORAL_DELTAS.md`

A repeated question is not necessarily a repeated answer. Product placement follows:
**Exam Plan** carries what to write now; **Study Guide** carries what was asked
before and what changed for today.

---

## Phase 2 headline

**The Directorate General of Shipping publishes its own question bank**, and it is
the source a large part of this corpus is drawn from.

`Question Bank MEO CL-I` — 185 items — was recovered from the Internet Archive after
the DGS domain refused connections for a second phase running. **63 questions across
the 40-paper solved corpus match a bank item strongly**, spread over 21 papers.

It overturned two Phase-1 findings and roughly doubled QP2608's verified recurrence,
from ~25/144 marks estimated to **48/144 verified**. It dates nothing at all — the
bank is undated — which is why every date claim in H1–H5 still fails.

See `OFFICIAL_QUESTION_BANK.md`.

---

## Files

### Evidence
| File | Holds |
|---|---|
| `SOURCE_MANIFEST.json` | 42 sources, with preservation state, text availability and separated confidences |
| `OFFICIAL_BANK_ITEMS.json` | the cited items of the official bank — **ancestors, not sittings** |
| `QUESTION_OCCURRENCES.jsonl` | one record per occurrence **at a sitting** |
| `QUESTION_FAMILIES.json` | 7 families; `frequency_known` always equals `known_occurrences.length` |
| `HISTORICAL_COVERAGE_MATRIX.md` | what MIW can read and reproduce, per sitting |

### Models
| File | Defines |
|---|---|
| `SIMILARITY_MODEL.md` | the five classes, normalisation, bidirectional containment, the short-stem guard, six negative controls |
| `LIMB_MODEL.md` | source limb vs analytical segment vs authoring scaffold |
| `PUBLICATION_STATUS_MODEL.md` | the lifecycle, and why a claim can be certain and unpublishable |
| `TEMPORAL_DELTA_SCHEMA.json` | delta categories, answer impact, exam relevance |
| `TEMPORAL_CONTEXT_BOUNDARY.md` | the Exam Plan / Study Guide rule |

### Findings
| File | Holds |
|---|---|
| `OFFICIAL_QUESTION_BANK.md` | the Phase-2 headline finding |
| `QP2608_PAPER_DNA.md` | recomputed — count view and mark-weighted view |
| `QP2608_TEMPORAL_DELTAS.md` | four pilots — `NONE`, `MINOR`, `MODERATE`, blocked |
| `PHASE3A1_REPAIR_REGISTER.md` | the Phase-3A.1 register, built from the actual Laptop review at `286c0c5` |
| `H1_H5_ADJUDICATION.md` | supersedes the Phase-1 verdicts in `verification/` |
| `CANDIDATE_BLOCK_PROTOTYPES.md` | drafts of the Study Guide block — **not implemented** |
| `CURRENT_ANSWER_CORRECTION_CANDIDATES.md` | **NONE**, with the sweep that established it |
| `SETTER_HYPOTHESIS.md` | NTA — `NO OFFICIAL EVIDENCE FOUND`, re-checked in Phase 2 |
| `WATCH_REGISTER.md` | what to re-check, and when |
| `BULLET_CONNECTION_PILOT.md` | Phase 1 — how a family reaches the current answer |
| `verification/H1…H5` | Phase 1 files, retained as the record of what was known then. Renamed in Phase 3A.1: the filenames asserted dates (`JUN2010`, `DEC2011`, `OCT2012`, `APR2010`, `MAR2010`) that the model refuses to assert, and a filename is the part that gets indexed, linked and quoted out of context. The dates are unchanged — still unsupported — and are now stated inside the files as the claim under adjudication. See `C45`. |

### Tools
| Tool | Does |
|---|---|
| `tools/validate_families.py` | **202 checks**, 0 skipped; `--mutate` runs 48 corruptions and proves each is caught, 9 of them against the required-source file itself |
| `tools/adversarial_controls.py` | **66 classification controls** and **41 magnitude-parser assertions**; `--mutate` switches off one guard at a time and requires a named control to break, then substitutes 3 weaker forms of the reference-suppression expression and requires each to break something |
| `tools/parse_dgs_question_bank.py` | extracts the official bank PDF — 185/185 items |
| `tools/match_bank_to_corpus.py` | sweeps the bank against all 40 specs, both containment directions |
| `tools/negative_controls.py` | 6 controls the classifier must not fail |

The DGS bank extract at `pastpapers/sources/official/dgshipping/` is REQUIRED
repository evidence, not optional intake. If it is missing, unreadable,
malformed or not the bytes the manifest declares, validation fails and exits
non-zero. It does not skip.

```bash
python meoclass1/pastpapers/intelligence/v2/tools/validate_families.py --mutate
```

---

## The rules this layer holds itself to

- **`frequency_known` counts SITTINGS.** Bank items are ancestors, stored apart so
  they cannot inflate it (`C28`).
- **Three confidences, never one** — text, date, source. `FAMILY-EM-0001` is
  legitimately `HIGH / NONE / HIGH`.
- **No date reaches a candidate unless `date_confidence` is HIGH** (`C21`). No
  hedged year either — the field is absent, because a hedge is still a claim.
- **Authoring scaffolds never key a recurrence** (`C4`, `C5`).
- **Marks are never inferred** (`C8`). Unknown stays unknown.
- **`DO NOT WRITE TODAY` must name the obsolete thing.** “Check the latest
  amendments” is forbidden.
- **A gap in MIW's holdings is not dormancy.** `LONG_GAP_RETURN` needs proven
  sittings at both ends (`C24`).
- **No numerical revival score.** Categorical status only.
- **Nothing is `CANDIDATE_PUBLISHED`** (`C23`, unconditional in Phase 2).

---

## Phase-1 conditions

| Condition | State |
|---|---|
| `FAMILY-EM-0004` counts inconsistent with its records | **REPAIRED.** The four declared ancestors were re-verified and serialised. The declared counts were *correct* and the records were missing, so records were created rather than counts reduced. `C14`–`C17` now enforce the derivation. |
| `SRC-SCRIBD-106245627` overstated | **RESOLVED.** Marked `UNVERIFIABLE_FROM_REPOSITORY`, with an explicit note that its sha256 hashes a 3 KB stub and not the text it was cited for. Superseded for recurrence by the official bank; the July 2012 **date** remains unevidenced and is counted nowhere. |

---

## Status

Nothing is candidate-published. Nothing is even `DATE_VERIFIED`. Every family sits at
`RESEARCH_HYPOTHESIS` or `TEXT_VERIFIED`, awaiting independent Laptop verification.
