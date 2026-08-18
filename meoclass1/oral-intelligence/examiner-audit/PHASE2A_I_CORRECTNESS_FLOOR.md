# Phase 2A-i — Oral matcher correctness floor

**Branch:** `research/oral-examiner-intelligence-v1-phase2a-i`, from
`research/oral-examiner-intelligence-v1-reconcile` @ `de6d3f2`
**Answers:** `review/oral-examiner-intelligence-v1-phase2` @ `c78a228` (Laptop, HOLD)
**Scope:** the matching and evidence floor only. No Oral Note was read, no P0 gap was
re-adjudicated, no connection was published, no live product file was touched, and the
committed reconciliation baseline remains the Phase 2 one.

The governing rule of this phase, in four lines the code now enforces:

> An unknown token is not a typo. ATTENDED is not UNATTENDED. ME-GI is not ME-GA.
> CURRENT_INDEX_RECOVERY is not PRIMARY_TRACKER. Same topic is not same core ask.

---

## A. Unsafe spell repair — removed

`repair()` replaced any token of five or more characters absent from the **QB** vocabulary
with its nearest corpus spelling at a 0.86 difflib cutoff. The QB corpus is 681 questions;
treating it as a dictionary of valid English and valid maritime terminology is what produced,
alongside 20-odd genuine fixes, all of the following — every one reproduced in this session
before anything was changed:

| Repair | What it destroyed |
|---|---|
| `attended -> unattended` (×2) | semantic inversion, fatal around UMS |
| `convinced -> convicted` | a different legal fact |
| `provident -> provide` (×2) | breaks Provident Fund |
| `biased -> based` (×2) | the ask was about bias |
| `conciliation -> reconciliation` | a different dispute-resolution mechanism |
| `and92 -> and9` | destroys the CLC 1992 Protocol reference |
| `stcw5 -> stcw15` | a different STCW regulation |
| `iii16 -> iii6` | a different STCW chapter III regulation |
| `whats -> hats`, `strees -> trees`, `shale -> sale` | noise |

**Policy chosen: Option A plus a narrow Option B.** The speculative nearest-corpus-token
engine is gone. Repair is now a 22-entry curated map (`oral_text.SOURCE_TYPO_MAP`) of source
misspellings that are not words in this domain and whose intended spelling is unambiguous —
`johri -> johari`, `ammendment -> amendment`, `deligation -> delegation`, `personm -> personam`
and so on. The curated map is also *more* correct than the engine it replaces: the speculative
version produced `approvel -> approve` (should be *approval*) and `diffence -> diffrence`
(itself a misspelling).

Cost, stated plainly: 14 rows that were PARTIAL_COVERAGE become MISSING, because their
coverage was manufactured by a repair. `STCW 5, 6` only matched STCW III/15 because
`stcw5` had been rewritten to `stcw15`. Withdrawing false coverage is the point.

## B. Load-bearing token guard

`oral_text.is_load_bearing()` is a general rule, not a list. A token is load-bearing when it
carries a digit, is a roman numeral, is a designator token, or is any non-purely-alphabetic
identifier. Repair refuses to touch one, and the controls assert the guard both ways — it must
cover `and92`, `stcw15`, `iii16`, `a60`, `ii`, `vi`, `me-gi`, and it must *not* over-reach onto
ordinary words like `amendment` or `survey`. Every key and value of the curated map is asserted
non-load-bearing, so the map cannot grow into the guard.

## C. Designator tokenisation

Before, `_DESIGNATOR` required a digit, so letter-suffix designators died:

| | Before | After |
|---|---|---|
| `ME-GI` | *(empty)* | `dsg:me-gi`, `dsg:megi` |
| `ME-GA` | *(empty)* | `dsg:me-ga`, `dsg:mega` |
| `ME-LGI` | `lgi` | `dsg:me-lgi`, `dsg:melgi`, `lgi` |
| `Annex I` | `annex` | `annex`, `dsg:annex-1` |
| `Annex VI` / `Annex 6` | `annex`+`vi` / `annex`+`6` — never met | both carry `dsg:annex-6` |
| `Form A` / `Form B` | `form` / `form` | `dsg:form-a` / `dsg:form-b` |
| `G8` / `G9` | `g8` / `g9` | plus `dsg:g-8` / `dsg:g-9`, so they share a family |

Three general rules do this, none of them a hard-coded example list:

1. **An ALL-CAPS hyphen or slash group is a technical designator; a lower-case one is ordinary
   English.** That single distinction is what lets `ME-GI` survive while `well-founded`,
   `state-of-the-art` and `risk-based` tokenise as prose — asserted in both directions.
2. **A keyword designator slot** (`Annex`, `Form`, `Part`, `Chapter`, `Tier`, `Reg`, …) makes a
   bare `I`, `A` or `6` a designator rather than a pronoun, an article or a loose number, and
   maps roman to arabic *inside the slot only* — a bare "v" in prose is still not the number five.
3. **A bare alphanumeric identifier** (`G8`, `A60`) is emitted in the same shape as its
   hyphenated spelling, so `A60` meets `A-60` and `G8` reads as a conflict against `G9`.

Designator tokens carry a `dsg:` prefix so they can never collide with prose. This is not
cosmetic: MIW's corpus contains 46 `ME-GA` mentions *and* 11 uses of "mega-" as an English
prefix (mega-ports, mega-vessels, mega-casualties). An unprefixed token would have matched
ME-GA questions against port-capacity answers.

`designator_conflict()` reports a conflict only when both sides name the **same family with a
different value** — `D-1` against `D-2`, `Annex I` against `Annex VI`, `ME-GI` against `ME-GA`.
Silence is never conflict. A conflict blocks promotion above PARTIAL_COVERAGE in `classify()`,
so an ME-GI ask can no longer be awarded an ME-GA question.

**Effect on the gap set.** The three ME-GI/ME-GA occurrences scored `best_answer_coverage 0.00`
against a corpus holding 27 ME-GI, 46 ME-GA and 43 ME-LGI mentions. They now reach 0.47 and
0.43 against `QB7_I#q1` and `QB7_I#q2`. GAP-0409 rested on a tokeniser artefact, exactly as the
review said; it is not re-adjudicated here, because adjudication belongs after Notes coverage.

## D. SAME_CORE_ASK admission floor

**Root cause.** `classify()` applies a similarity floor to EXACT (`sim >= 0.55`) and to NEAR
(`sim >= 0.30`), and applied none to SAME_CORE. Its two SAME_CORE rungs test coverage only —
`qcov >= 0.75`, or `qcov >= 0.5` with a complete target answer. Coverage is the IDF-weighted
fraction of the *source's* tokens present in the target, so a one-word prompt whose single
token happens to appear anywhere in a long question stem reaches `qcov = 1.00` and is awarded
the same substantive relationship as a genuine restatement. The terse-prompt quarantine that
should have caught these fired only for `0.5 <= cov < 0.95` — that is, everywhere except at the
full coverage a one-word prompt reliably produces. Measured on the committed rows: 52% of
SAME_CORE below `sim 0.25`, 50 of 69 with reverse coverage below 0.35, median similarity 0.222
against 0.667 for EXACT.

**The floor.** `same_core_admissible()` requires, as the smallest defensible criterion:

- **substantive mass** — at least 3 scored source tokens; a one- or two-token prompt is a
  label, not an ask, and is routed to the human review queue at any coverage;
- **bidirectional evidence** — `sim >= 0.30`, or `sim >= 0.20` with reverse coverage `>= 0.35`;
- **no contradictory load-bearing designator**.

A row that fails the floor falls to PARTIAL_COVERAGE, never to MISSING: under-crediting a
covered ask costs an enrichment task, it never misleads a candidate.

Seven of the eight false SAME_CORE matches the review named are eliminated — five demoted to
PARTIAL (shipping master → VGM, LSA Code → Polar Code, LLMC → HNS, CII compliance → shore
power, MLC → assessor) and two quarantined (MRCC, GA PA YA). Median SAME_CORE similarity moves
0.222 → 0.333, and no SAME_CORE row now sits below `sim 0.25`.

**One named false match survives, and no similarity floor can catch it:** *International
Convention on Registration of Ships* → *Fraudulent Registration of Ships*, at `sim 0.40` and
reverse coverage 0.61. Both scores are healthy; the discriminator is the word "Fraudulent",
which is an entity distinction rather than a designator one. Recorded, not papered over.

**A cost, stated.** Two rows leave the strong classes: `UNCLOS FS duties` NEAR → PARTIAL, which
is the wrong-target row the review itself flagged, and `MS Act Welfare for seafarer` EXACT →
SAME_CORE. EXACT and NEAR otherwise hold at 22 and 40 against 23 and 41.

## E. Evidence provenance

An evidence record carries both what it claims (`evidence_tier`) and where it came from
(`source_type`). Nothing validated the two against each other, so mutation M5 — relabelling a
`CURRENT_INDEX_RECOVERY` record, which the ledger itself annotates *"Not independent
evidence"*, as `PRIMARY_TRACKER` — passed at 35 PASS / 0 FAIL. Reproduced here before the fix.

`oral_provenance.py` states a tier↔source compatibility matrix and one hard rule: **a primary
tier admits only provenance that points at the primary tracker structure.** The published
index, the July sheets, a topic inference, a page CE tip and an examiner cue in an Oral Note
are each real evidence of something; none of them is the tracker. Three validator checks now
enforce it, and every one of the five promotions fails.

`NOTE_EXPLICIT` is defined now, ahead of Phase 2A-ii, as the tier for an explicit examiner cue
found in an MIW Oral Note. It is neither `PRIMARY_TRACKER` nor `TOPIC_INFERRED`, and the gate
already refuses to promote it. No Oral Note was read in this phase.

## F. Determinism

**Root cause.** `source_spelling_repairs` was appended while iterating `raw_stoks`, a **set**,
so the list order followed string hash randomisation. Reproduced: two runs under different
`PYTHONHASHSEED` values differed on 2 records, with no disposition, target or coverage change.

Four sources were closed, all on the Phase-2A-i path: repair notes are now built from a sorted
iteration and sorted on emission; the candidate loop iterates `sorted(q_tok)`; both candidate
sorts carry an explicit canonical-id tiebreak so equal scores never fall back on insertion
order; gap families are built and emitted in a stable order. `weighted_coverage` also sums over
a sorted token list, because float addition is not associative and the score itself would
otherwise depend on the seed.

`check_determinism.py` runs the generation three times under deliberately different seeds and
requires the four generated artefacts to be byte-identical. It restores whatever was on disk
before it ran, so it can never become a way of silently re-baselining.

## G. Gates

| Gate | Result |
|---|---|
| `validate_phase2.py` | **38 PASS / 0 FAIL** (35 preserved, 3 provenance checks added; none removed) |
| `test_oral_controls.py` | **181 controls / 0 failures** |
| `mutate_phase2.py` | **16 mutations / 0 escapes** |
| `check_determinism.py` | **4 artefacts / 0 non-reproducible** |

Mutations M1–M9 are the Laptop's nine reproduced. M5 is the escape, now caught. M5a/M5b/M5c and
M13 extend it to July-derived, topic-inferred, CE-tip and Note-explicit promotions. M10 removes
the SAME_CORE floor, M11 collapses ME-GI/ME-GA tokenisation, M12 re-enables speculative repair —
each fails 12, 15 and 6 controls respectively. M14 (Notes-coverage deletion) is deliberately
absent: no Notes coverage layer exists yet.

## H. Regression signal — NOT a baseline

Run once after repair. **Not committed.** The committed reconciliation remains the Phase 2 one
until Phase 2A-iii, because the gap set cannot be re-derived before the Notes are in the
coverage universe.

| Class | Phase 2 | Post-2A-i (temporary) | Why |
|---|---|---|---|
| EXACT_MATCH | 23 | 22 | one row demoted by added designator mass |
| NEAR_MATCH | 41 | 40 | the review's own wrong-target UNCLOS row |
| SAME_CORE_ASK | 69 | 24 | admission floor; the rest demoted or quarantined |
| PARTIAL_COVERAGE | 364 | 369 | the conservative sink absorbing failed SAME_CORE |
| MISSING | 204 | 218 | false coverage manufactured by spell repair, withdrawn |
| AMBIGUOUS | 87 | 115 | terse prompts quarantined at any coverage |

MISSING rising is expected and is *not* evidence against the review's finding that MISSING is
over-reported: that over-reporting is caused by the Notes exclusion, which Phase 2A-ii closes.

## I. Deliberately not done

Oral Notes not ingested · P0 not recomputed · Release A not built · examiner-index V2 generator
not built · SQ untouched · no live QB, index, notes, payments, homepage, Written QI or magazine
file modified · reconciliation source datasets unchanged · governance items (research tree
location, `.vercelignore`, public raw wording) reported by the Laptop and left to the Founder.

## J. Next

**Phase 2A-ii** — ingest `meoclass1/oralnotes/` as a secondary coverage and examiner-evidence
layer, harvesting explicit examiner cues at `NOTE_EXPLICIT` provenance, without changing the
681 canonical QB questions. Then, and only then, **Phase 2A-iii**: full 788 recompute, release
set, P0 recomputation.
