# Phase 2A-iii — final 788 recompute, Release A and P0

**Branch:** `research/oral-examiner-intelligence-v1-phase2a-iii`, continuing from the
bounded designator repair at `88c83be`
**Answers:** `LAPTOP_PHASE2_INDEPENDENT_REVIEW.md` @ `c78a228` (HOLD), and the three
phase reports it produced.
**Scope:** the recompute and the release/production datasets. The matcher is frozen:
no tokenisation, no admission floor, no conflict rule and no Notes threshold was
changed. Nothing is published. No live product file was touched.

The governing rule of this phase, in four lines the code now enforces:

> 788 occurrences in, 788 dispositioned out, every movement explained.
> Release A is only what we can defend. P0 is only what a candidate still cannot answer.
> Notes are what MIW knows; the QB is what MIW asks; neither is the other.

---

## A. What the recompute is, and what it replaces

The committed reconciliation stops being the Phase-2 one. This is the first run of the
Phase 2A-i safe matcher, the Phase 2A-ii Notes layer and the Phase 2A-iii designator
repair together, against every source occurrence.

| | Phase 2 (`de6d3f2`) | Phase 2A-iii |
|---|---|---|
| EXACT_MATCH | 23 | **22** |
| NEAR_MATCH | 41 | **40** |
| SAME_CORE_ASK | 69 | **24** |
| PARTIAL_COVERAGE | 364 | **369** |
| MISSING | 204 | **218** |
| AMBIGUOUS | 87 | **115** |
| **total** | **788** | **788** |

Source accounting reproduced rather than asserted: **788** occurrences, John 129,
Simon 256, Nair 300, Paul 103, against **681** canonical QB questions and **992** note
units. Every occurrence carries exactly one content disposition, exactly one Notes
support tier and exactly one production action, and the validator fails if any of the
three is missing, duplicated or drawn from the wrong vocabulary.

`PHASE2_BASELINE_SNAPSHOT.json` records the Phase-2 dispositions and targets as a
committed file, so the movement report is reproducible from the tree alone and needs no
git access when it runs.

## B. Movement — 343 rows moved, and 208 of them silently

**135 rows change disposition. A further 208 keep their disposition and change target.**
That second number is the one a summary table cannot show: a row that stays
PARTIAL_COVERAGE while moving to the right question has still moved, and a review that
only diffs class totals would call it unchanged.

| Reason | Rows |
|---|---|
| `SAME_CORE_FLOOR` | 51 |
| `SPELL_REPAIR_SAFETY` | 42 |
| `OTHER_EXPLAINED` | 21 |
| `TARGET_RESELECTION` | 13 |
| `DESIGNATOR_CONFLICT_FIX` | 5 |
| `HUMAN_ADJUDICATION` | 3 |

The reason ladder is ordered by specificity and derived from the record, not narrated:
a demotion out of SAME_CORE is explained by the admission floor whatever else is true of
the row, and only a row no earlier rung explains reaches `OTHER_EXPLAINED`.

**The class totals happen to match the Phase 2A-i temporary figures exactly.** That is
not evidence the Notes layer and the designator repair did nothing — 343 rows moved
underneath them. It means the demotions and promotions those layers caused net out at
class level, which is precisely why movement is tracked per row.

## C. The designator repair, on real data

The four ME-Gx occurrences scored `0.00` against a corpus holding 27 ME-GI, 46 ME-GA and
43 ME-LGI mentions. They now reach `QB7_I` at 0.43–0.47, and — the point of the repair —
an ME-GI ask is not awarded an ME-GA question. All nine full-sentence designator
behaviours were re-proved through the real `mtokens → designator_conflict → classify`
path before the recompute ran: ME-GI/ME-GA, ME-GI/ME-LGI, III/1 vs III/2 with and
without a keyword slot, Form A vs Form B, D-1 vs D-2 all conflict; Annex VI vs Annex 6,
ME-GI vs itself, and a bare family head against a member all correctly do not.

## D. Notes support, and the row that matters

| Notes support | Occurrences |
|---|---|
| `NOTES_COMPLETE_SUPPORT` | 153 |
| `NOTES_STRONG_SUPPORT` | 83 |
| `NOTES_PARTIAL_SUPPORT` | 320 |
| `NOTES_TOPIC_SUPPORT` | 177 |
| `NO_NOTES_SUPPORT` | 55 |

Against the canonical dimension:

| Canonical | complete | strong | partial | topic | none |
|---|---|---|---|---|---|
| **MISSING** (218) | 9 | 2 | 78 | 84 | 45 |
| **PARTIAL_COVERAGE** (369) | 45 | 60 | 204 | 53 | 7 |
| **SAME_CORE_ASK** (24) | 9 | 7 | 7 | 1 | 0 |

**MISSING + NOTES_COMPLETE is never EXACT.** It is a canonical gap over material MIW
already holds, and its production action is a promotion. A validator check enforces
exactly that, and mutation M26 proves the check bites.

## E. Release A — 136 pairs

Connection-only. No answer depends on it. A pair enters on two conditions together:
the examiner provenance is defensible and the canonical target is defensible.

| Strongest evidence tier | Pairs |
|---|---|
| `PRIMARY_TRACKER` | 84 |
| `EXTERNAL_SOURCE_CONFIRMED` | 52 |

Per examiner: Simon 59, Nair 39, Paul 16, John 11, Rajappan 9, Senthil 1, Srivastava 1.

Held out, each with its reason recorded rather than dropped: 369 PARTIAL targets, 205
weak-prose pairs, 183 MISSING targets, 115 AMBIGUOUS targets, 81 CE-tip-only pairs, and
**24 SAME_CORE targets**. The review measured SAME_CORE at 60% precision and held its 37
dependent pairs; the admission floor has since removed most of that class, and the rest
is still held. Nothing was padded to reach a number.

**The Notes route contributed nothing, and that is a finding rather than an omission.**
All 19 `NOTE_CREATES_NEW_EXPLICIT_CONNECTION` rows carry a null canonical target: an
explicit examiner cue exists in a note, but there is no canonical question to attach it
to. Those 19 are candidates for promotion, not for publication.

## F. P0 — 9 items

Not "everything missing" — 218 rows are MISSING. P0 is what a candidate on 24 August
still cannot answer from the existing QB answer plus the relevant Oral Notes.

| Action | Items |
|---|---|
| `P0_NEW_ANSWER` | GAP-0016, GAP-0042, GAP-0044, GAP-0048, GAP-0410 |
| `P0_ENRICH_EXISTING_QB` | GAP-0034, GAP-0043, GAP-0409 |
| `P0_NOTES_TO_QB_PROMOTION` | GAP-0002 |

Human adjudications live in `P0_ADJUDICATIONS.json` as a committed input the builder
reads, so a judgement is auditable as a judgement and never arrives as an edited count.
Four gaps were adjudicated out and one merged:

- **GAP-0494 (HKC / IHM parts) — not a P0 gap, and the matcher is wrong about it twice.**
  `QB3_C#q3` is literally *"Hong Kong Convention — IHM three parts and CE role?"*, and
  `oralnotes/WA1-HKC1.html` carries the IHM Part I/II/III block. The record scores it
  0.298 canonical and `NO_NOTES_SUPPORT` because the candidate wrote "HKG" where MIW
  writes "HKC". The review's `NOT_A_GAP` was right; the residual limb is who performs
  the initial survey, which is an enrichment.
- **GAP-0409 (ME-GA) — enrichment, not a new answer.** The adjudication the designator
  repair existed to unblock. `QB7_I#q2` covers the ME-GI and ME-GA families and
  `QB7_I#q3` compares ME-GA methane slip.
- **GAP-0009 ("STCW 7, 8" / "STCW 5, 6") — human review.** Terse designator fragments
  with no chapter, part or subject. Phase 2A-i withdrew the repair that rewrote `stcw5`
  to `stcw15` and manufactured a target; inventing one here repeats that defect.
- **GAP-0069 (TIO2) and GAP-0093 (medical certificate) — P1.** Single occurrence each,
  and GAP-0069 is a two-word label rather than an ask.
- **GAP-0454 merges into GAP-0410.** One Nair ask in two formulations.

**The BWTS adjudication resolves as two distinct asks, not one merge.** Phase 2A-ii
observed that GAP-0016, GAP-0069 and GAP-0410 share a best note unit. Read at source,
GAP-0016 is John on the BWM Convention's status and guidelines G7/G8/G9, GAP-0410 is
Nair on verifying D-2 compliance onboard, and GAP-0069 is not BWTS at all. A scan of all
681 canonical questions returns no question mentioning BWM, BWTS, G8, G9 or D-2, so both
survive as genuine gaps.

**One correction to the review, recorded so it is not carried into production:** its
reuse pointer for GAP-0016, `QB1_supplementary#q20`, is *"Tail Shaft Survey"*.

## G. Human review residue — 115

74 two-target, 41 terse. Resolved automatically only where the repaired model makes the
target clear; a terse acronym is never forced, because an unresolved row costs a review
and a wrongly resolved one costs a candidate.

## H. Retiering — research only, and two things kept apart

| | Count |
|---|---|
| invalid literal repairs (`cetip` → `ce_tip`) | **2** |
| proposed tier changes | **195** |
| proposed promotions to `confirmed` with no primary evidence | **0** |

The two are separated because conflating them turns "197 pairs would change tier" into a
claim nobody can check. The repairs are rows whose published tier is not a valid literal
at all, so they have no filter toggle and vanish the first time a filter is used. The
proposals are rows whose tier is valid but is not what the evidence supports — and **31
of them are demotions** (28 `confirmed` → `ce_tip`, 3 `confirmed` → `inferred`), meaning
the live index currently over-claims on those rows. The M5 escape class is closed: no
proposed promotion to `confirmed` lacks primary evidence.

## I. Display text — 9 candidates, one the review did not report

The eight `QB5_C_B` rows the review found, plus **`QB7_B#q2`, whose live
candidate-facing question text is `Examiner context:** Rajappan (2026) — hydrogen colour
taxonomy…`** — unrendered production markup, not a question at all. It is marked for
authoring rather than given a proposed replacement, because stripping the name leaves
prose that still is not an ask. No live file was modified.

## J. Other examiners preserved

The compilation names four surveyors; the index holds six. Every relationship and note
evidence record for the other three survives the recompute: Rajappan 93 relationships,
Srivastava 103, Senthil 66 — 862 relationships in total, unchanged. The external
compilation is additive evidence, not the whole examiner universe.

## K. Gates

| Gate | Phase 2A-iii start | Now |
|---|---|---|
| `validate_phase2.py` | 66 PASS / 0 FAIL | **91 PASS / 0 FAIL** (+25) |
| `test_oral_controls.py` | 315 / 0 | **315 / 0** |
| `mutate_phase2.py` | 26 / 0 escapes | **33 / 0 escapes** (+7) |
| `check_determinism.py` | 10 artefacts / 0 | **26 artefacts / 0** (seeds 0, 1, 524287) |

No check was removed, weakened or renamed. The seven new mutations each fail
semantically rather than by crashing: M20 drops a source occurrence, M21 gives one
occurrence two dispositions, M22 admits an inferred-only pair, M23 admits a pair whose
only external row is SAME_CORE, M24 breaks a target anchor, M25 duplicates a P0 family,
M26 relabels the GIRDING promotion as research from zero.

## L. Reproducibility, and the defect the cross-drive gate found

`check_determinism.py` covers 26 artefacts across five generators. `GENERATORS` became an
ordered sequence rather than a mapping, because the final package reads what the earlier
generators write and alphabetical order ran the consumers before the producers.

**The cross-drive gate earned its place.** Regenerating everything in a fresh worktree on
`C:` from a repository on `D:` reproduced 25 of 26 byte-identically and moved
`ORAL_NOTES_INVENTORY.json`. Only the recorded sizes differed — every `note_units` count
was identical — but a committed number that differs between two checkouts of the same
commit cannot be reviewed. Cause: the inventory recorded `stat().st_size`, and these
pages are text under `*.html text eol=lf`, so a Windows working tree can hold CRLF while
the blob holds LF. Sizes are now measured on LF-normalised bytes. Both drives report
total 3785706 and substantive 2799197; the previously committed 3791609 was the
CRLF-inflated reading, so the "3.79 MB of HTML" in the Phase 2A-ii report was measuring
this machine rather than the corpus. After the fix, **every artefact reproduces
byte-identically cross-drive and the validators leave the worktree clean.**

A related latent condition is reported and not acted on: 25 committed artefacts sit on
this working tree with CRLF while their blobs hold LF. Git hides it, because the `text`
attribute normalises on comparison, so `git status` is clean. It is harmless to git and
to every gate here, but it means "byte-identical on disk" is only a meaningful claim for
artefacts a generator has rewritten.

**Interrupted-run safety** was confirmed before the recompute: the determinism harness
writes its pre-run snapshot to disk before regenerating anything and restores a stale
snapshot on the next run, which is the defect that clobbered the Phase-2 baseline once.
The committed baseline was additionally copied out before the first generator ran, and
every input remains recoverable from `de6d3f2`.

## M. Governance — reported, unchanged

The research tree still lives at `meoclass1/oral-intelligence/`, inside the deployed web
root, and `.vercelignore` still has no entry for it. Nothing was relocated and no
ignore file was altered, per instruction. **The risk did not change in kind, but it grew
in volume:** this phase adds the final reconciliation, the Release-A set, the P0 batch
and the movement report to that tree. The recommendation stands, and remains a Founder
decision.

## M2. `origin/main` moved during this session — read this before rebasing

Main was reported as `3b55bfb` and was `3b55bfb` when this session established repo
truth. It is now **`88bd1a6`**: three commits landed while this recompute ran, and they
change the inputs this phase measured. The branch itself is unaffected — it forks at
`3b55bfb`, and a diff against that fork point changes nothing outside
`meoclass1/oral-intelligence/`, `tools/oral/`, `.gitignore` and `.gitattributes` — but
the Laptop must not verify these numbers against `main`'s corpus without accounting for
the drift.

| | this branch | `origin/main` now |
|---|---|---|
| canonical QB questions | **681** | **682** |
| `QB1_K.html` questions | 7 | 8 |
| `examiner-index.html` rows | 863 | **864** |

Three consequences, none of them fatal and none of them silent:

1. **The question universe is 682 on main.** Every count in this report is against the
   681 at the fork point. Re-running after a rebase will legitimately move rows.
2. **The live examiner index was hand-edited again** — 863 rows to 864. That is exactly
   the hand-maintenance the V2 generator exists to end, and it means the index and the
   research data have drifted apart once more.
3. **A tenth display-text defect was introduced today.** The new `QB1_K#q8` reads
   `(Simon sir) "What is CSR?" — what does he mean, and what is its scope?`. It is the
   same class as the nine in section I: an examiner name inside candidate-facing text.
   The detector already catches this shape, so a rebase would raise the candidate count
   from 9 to 10 without any change to the rule.

Recorded rather than acted on: rebasing mid-review would invalidate the Laptop's
verification target, and choosing when to rebase is not this session's call.

## N. Deliberately not done

examiner-index V2 generator not built · `SQ/examiner-index.html` untouched · no
connection published · no P0 answer written · no QB, Oral Note, examiner index, SQ,
homepage, payments, Written QI or magazine file modified · matcher architecture not
reopened · the 19 unresolved note-explicit connections not forced to a target.

## O. Next

**Laptop release review.** Independently verify the 788 recomputation, the Release-A set,
the retiering proposal, the human-review residue and every P0 item. If green, authorise
two bounded production streams: deterministic examiner-index V2 and SQ teaser generation
from this same canonical data pass, and only the approved P0 items.
