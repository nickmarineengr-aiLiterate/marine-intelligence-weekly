# Phase 2 Handoff — Oral 788-Question Reconciliation

**From:** Desktop Claude (Opus 5), 18 August 2026
**To:** Laptop Claude — independent review and pre-24-August release authorisation
**Branch:** `research/oral-examiner-intelligence-v1-reconcile`
**Base:** Phase 0/1 audit @ `d8ed9e6` (not `main`)
**Orals begin:** 24 August 2026

---

## What changed since Phase 1

Phase 1 found that the 863 question-level examiner pairings existed in exactly one hand-uploaded HTML
file with no generator and no upstream source. **That fragility is closed.** The pairings are now
data, and the 788 external occurrences are reconciled against them.

| Layer | Count |
|---|---|
| Examiner relationships recovered to data | **862** (from 863 rendered rows; 1 duplicate) |
| Index-recovery evidence records | 863 |
| External source occurrences ingested | **788** (matches the document's own declared total) |
| Normalised source families | 731 |
| Live Oral QB questions compared against | 681 |
| Validation | **35 PASS / 0 FAIL** |

## What you can rely on

- **Every one of the 788 occurrences carries exactly one content disposition and one examiner
  mapping status**, and every one traces back to surveyor, topic, page, question number and raw
  wording. There is no opaque fuzzy-match output.
- **The parse is verified against the document itself**: 129 John / 256 Simon / 300 Nair / 103 Paul,
  57 topics, grand total 788 — parsed counts equal the document's declared counts on every line.
- **No live candidate page was edited.** The only files touched are new tools under `tools/oral/`
  and new records under `meoclass1/oral-intelligence/examiner-audit/`.

## The headline results

| | |
|---|---|
| Already answered (exact / near / same-core) | **133** occurrences |
| Partially covered | **364** |
| Genuinely missing | **204** |
| Ambiguous, needs human judgement | **87** |
| Unique **new** examiner→question pairs proposed | **291** |
| Already-linked pairs corroborated by the external source | **127** |
| Genuine gap families | 196 (**15 at P0**) |
| Material-partial families | 115 |

The single most valuable finding is the middle column of that table: **291 new examiner connections
need no new answers written.** MIW already answers those questions; it never connected the examiner.

## Six things to check first

1. **The 15 P0 gaps** (`ORAL_P0_GAPS.md`). Every one carries its source wording, examiner, page and a
   reuse candidate. Adjudicate whether each genuinely needs a new card — the creation rule is
   applied by tooling, but it is a judgement call at the margin.
2. **The 87-item human review queue** (`HUMAN_REVIEW_QUEUE.md`). Two reasons only: 62 cases with two
   plausible targets where neither fully covers the ask, and 25 source prompts too terse to decide
   from wording alone ("Imposex", "GMDSS").
3. **The 46 `READY_VERIFIED_MULTI_SOURCE` connections** — Phase 1 ready connections now independently
   corroborated by the external compilation. These are the safest thing MIW can publish before
   24 August.
4. **Paul.** 103 external occurrences against 19 published pairs. Only **13** are genuinely missing;
   55 are partially covered, 24 are already answered outright, and **66 new pairs** are proposed
   against just 3 already-linked. Paul is a connection problem far more than a content problem — the
   opposite of what the raw count gap suggests, and he carries **no P0 gap at all**.
5. **John.** Entirely new: 129 occurrences, zero MIW-native evidence, **77 proposed new pairs**, zero
   already-linked, 28 genuine gaps and 3 at P0. **Adjudicate the person before creating an examiner
   section.** Every John relationship rests on `EXTERNAL_SURVEYOR_COMPILATION` alone.
6. **The re-tiering.** 197 of 862 published relationships would change tier under honest evidence
   rules. 406 have a primary record behind them; 203 rest on CE-tip prose; 213 on inference alone.
   Nothing on the live page was changed — this is research data awaiting your decision.

## Traps this phase hit, so you don't

1. **The audit's general tokeniser drops the domain's own designators.** `A-60`, `D-1/D-2`, `Tier
   III`, `Annex 6` all vanish (a bare `60` is under the length floor, `A-60` splits into two dead
   tokens). An ask about A-60 bulkheads could not match a question about A-60 bulkheads. `mtokens()`
   in `reconcile_788.py` fixes this; `oral_lib.tokens` is unchanged so Phase 1 outputs still
   reproduce.
2. **Topic tags must never decide a match.** Including `data-tags` in the coverage denominator gave
   `GMDSS` a perfect score against a question about MMSI, and `IG system` a perfect score against
   "MIS vs data". Tags are recorded as `matched_on_topic_tag`, never scored.
3. **Corpus-wide answer coverage over-rescues.** Taking the best answer match across all 681 cards
   turned real gaps into false coverage. The creation rule is applied through the **matched
   question's own answer**; the corpus-wide best is kept only as a reuse pointer.
4. **The source is candidate-typed and misspells domain words.** "JOHRI WINDOW" is Johari Window,
   which MIW answers. 65 occurrences needed a spelling repair; every repair is recorded on the
   record in `source_spelling_repairs`, never applied silently.
5. **A tie between two targets is not automatically ambiguity.** When both candidates fully cover the
   ask it is a duplicate target, resolved on similarity and recorded as
   `alternative_target_question_id` (34 cases). Treating every tie as ambiguous put 351 of 788 items
   into human review — useless.
6. **The July per-examiner sheets remain excluded.** Confirmed independently this phase: they overlap
   the recovered relationships on **824 of 862** pairs. Counting them as a second confirmation
   inflates every "confirmed" number. Phase 1's `DERIVED_PRODUCT_SURFACE` classification stands.

## Reproduce anything

```bash
PYTHONIOENCODING=utf-8 python tools/oral/recover_relationships.py
```

```bash
PYTHONIOENCODING=utf-8 python tools/oral/ingest_all_surveyors.py --docx "<path to All Surveyors .docx>"
```

```bash
PYTHONIOENCODING=utf-8 python tools/oral/reconcile_788.py
```

```bash
PYTHONIOENCODING=utf-8 python tools/oral/report_phase2.py
```

```bash
PYTHONIOENCODING=utf-8 python tools/oral/validate_phase2.py
```

Expected validation state: **35 PASS / 0 FAIL**. A single new failure means something regressed —
stop rather than proceed. `PYTHONIOENCODING=utf-8` is still mandatory (Windows console is cp1252).
No drive letter, username or temporary path appears in any committed file; the workbooks and the
DOCX are CLI arguments and remain git-ignored on a public repository.

## Fastest pre-24-August release package — proposed, not published

Four bounded releases, smallest risk first. Counts are derived from the records; nothing here is
published and nothing is authored.

| Release | Content | Items | New answers needed |
|---|---|---|---|
| **A** | Verified new connections only — 84 Phase-1 ready connections (46 now multi-source corroborated, 38 tracker-verified) plus **78** new pairs where the external ask is an exact/near/same-core match to an existing answer | **162 pairs** | none |
| **B** | P0 genuine gap answers | **15 questions** | 15 |
| **C** | Follow-up / expected-detail enrichment on existing cards (examiner-specific limbs, regulation-number demands, cross-questions) | **158 pairs** | none — enrichment only |
| **D** | Full regenerated Examiner Index V2 from `EXAMINER_INDEX_V2_GENERATOR_SPEC.md`, including the 35 blank rows, 2 filter-invisible rows, 1 duplicate and the three stale count layers | whole index | none |

A further **213** new pairs rest on partial coverage. They are real connections but a candidate
following one could meet a limb the existing answer does not reach, so they belong after Release C,
not in Release A.

Release A is the largest candidate-visible gain available before 24 August and requires no authoring
at all. It cannot ship until the generator exists (Release D's tooling), because hand-patching the
index is what produced the current three stale count layers.

## Still not done, deliberately

No answers written · no live page edited · no `SQ/` correction · no "Asked By" UI · no generator
built · no tier badge changed · no inferred relationship deleted. The generator contract is
specified in `EXAMINER_INDEX_V2_GENERATOR_SPEC.md` and awaits authorisation.

## Next action — exactly one

> **LAPTOP CLAUDE — INDEPENDENTLY REVIEW THE ORAL 788-QUESTION RECONCILIATION, VERIFY THE PROPOSED
> NEW EXAMINER CONNECTIONS, ADJUDICATE THE HUMAN-REVIEW QUEUE AND AUTHORISE THE FIRST
> PRE-24-AUGUST CONNECTION RELEASE PLUS P0 GAP-ANSWER PRODUCTION.**
