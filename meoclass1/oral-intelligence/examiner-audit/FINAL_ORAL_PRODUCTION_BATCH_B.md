# Final Oral Production — Batch B

Ten laptop-authorised P1-B new canonical Q&A cards, built, verified and integrated.

## Authorisation

`FINAL_ORAL_PRODUCTION_AUTHORIZATION.json` → `batches.P1-B`, on the laptop review branch
(`review/oral-final-gap-decision-laptop`, tip `fef45eb`). The manifest set matches that
batch exactly — ten families, none extra, none missing. All ten carry
`adjudicated_decision = NEW_CANONICAL_QA`, `laptop_decision = NEW_CANONICAL_QA`,
`laptop_review_status = LAPTOP_CONFIRMED`, `priority = P1-B`, `confidence = HIGH`, and a
production action of kind `NEW_CARD_FROM_GAP`. No relationship-kind action exists for any
of them anywhere in the record, so the Examiner Index receives **no relationship delta**.

## Homes

| family | action | home | topic |
|---|---|---|---|
| GAP-0083 | NEW-002 | `QB8_A.html#q7`  | P/V breaker and mast riser — the tank venting chain |
| GAP-0113 | NEW-003 | `QB1_D.html#q5`  | Fresh Water Allowance and Dock Water Allowance |
| GAP-0728 | NEW-023 | `QB1_D.html#q6`  | Type B-60 and B-100 freeboard reduction |
| GAP-0120 | NEW-004 | `QB7_C.html#q2`  | Miller cycle against Otto and Diesel |
| GAP-0128 | NEW-006 | `QB7_C.html#q3`  | adaptive cylinder oil control against fuel sulphur |
| GAP-0124 | NEW-005 | `QB2_H.html#q3`  | why the flammability diagram air line slopes |
| GAP-0365 | NEW-010 | `QB6_D.html#q5`  | cavitation in a centrifugal pump and on a propeller |
| GAP-0412 | NEW-013 | `QB7_D.html#q12` | wake equalising duct and the owner's case |
| GAP-0418 | NEW-015 | `QB6_H.html#q3`  | electric shock from V = IR and its effect on the body |
| GAP-0442 | NEW-016 | `QB5_A.html#q21` | behaviour-based safety |

Corpus **696 → 706** canonical questions across an unchanged **86** files, derived from the
live HTML and independently reproduced before and after.

## Duplicate-home control

Every ask was swept against the live QB HTML with word boundaries, and the nearest
neighbours were read rather than scored. Nothing had to be stopped. Three findings:

* **`ESD` is an acronym collision.** All ten "energy saving device" hits were *Emergency
  Shut Down*. Zero cards own energy-saving devices. This is the `HRU`-inside-`through`
  class from Batch A, now in acronym form.
* **GAP-0728 needed re-scoping, not rejecting.** `QB1_G#q37` genuinely owns "why tankers
  have less freeboard" — that is Type A assignment under a different regulation limb. The
  B-60/B-100 *reduction regime* is unowned. The new card is scoped to the reduction and
  its damage standard, and cross-links q37 rather than restating it. Same pattern as
  GAP-0378 in Batch A.
* **The two flagged false neighbours were confirmed noise.** `QB1_F#q9` is generic
  fuel-consumption prose, not cylinder-oil dosing; the IMSBC/TML pointer for
  behaviour-based safety did not even appear in a word-boundary sweep. The real
  near-neighbour for GAP-0128 is `QB6_G#q1`, which mentions BN and feed rate in a single
  clause inside a teething-problems card — cross-linked, not duplicated.

## Primary authority

No card is sourced from True Source: `Knowledge Central/` in this clone holds only the FSS
and casualty-investigation packages, with **zero hits on all ten topics**. All ten were
verified against primary sources — among them ICLL Annex I Regulations 27, 26, 25, 24, 16
and 40 with **IACS UI LL72 (Sept 2005)** read verbatim; SOLAS II-2/4.5.3, 4.5.3.3,
4.5.3.4.1.3, 4.5.5, 11.6 and 11.6.3.2 with FSS Code Chapter 15; MARPOL Annex VI
regulations 13, 14, 23, 25, 26 and 28 with the NOx Technical Code 2008; **MEPC.1/Circ.896**;
**MAN B&W service letter SL2009-507**; **IEC 60479-1** and IEC 60092; ISM Code 1.2.2, 5, 6,
7 and 9; IMO resolution **A.947(23)**; and STCW Table A-III/2.

Two currency catches worth carrying:

* **MEPC.1/Circ.815 is superseded by MEPC.1/Circ.896 (2021)**, which extends the innovative
  energy-efficiency framework from EEDI to EEXI. Citing 815 in 2026 would have been a
  dated-but-plausible reference — the hardest class to catch on review. Mutation H exists
  precisely to stop that regressing.
* **Annex VI Chapter 4 numbering was verified locally, and the summarising model was wrong
  about it.** The current text is 19 Application, 20 Goal, **21 Functional requirements**,
  22 Attained EEDI, 23 Attained EEXI, 24 Required EEDI, 25 Required EEXI, 26 SEEMP,
  27 fuel oil consumption data, 28 Operational carbon intensity. Regulation 21 is *not*
  EEDI. A fetched summary asserted otherwise; only extracting the resolution PDF caught it.

Two claims were **removed rather than guessed**: a 30 m/s high-velocity vent efflux figure
that would not verify, and any single fuel-saving percentage for a wake equalising duct —
the card says instead that the benefit must be established for the specific hull by model
test and sea trial, as MEPC.1/Circ.896 requires.

## Timed blocks

Measured with balanced-tag extraction, against a live corpus norm of 56 words (15s) and
124 (60s):

| card | 15s | 60s | | card | 15s | 60s |
|---|---|---|---|---|---|---|
| QB8_A#q7 | 55 | 136 | | QB6_D#q5  | 59 | 143 |
| QB1_D#q5 | 52 | 149 | | QB7_D#q12 | 57 | 150 |
| QB1_D#q6 | 57 | 141 | | QB6_H#q3  | 58 | 141 |
| QB7_C#q2 | 57 | 146 | | QB5_A#q21 | 56 | 144 |
| QB7_C#q3 | 54 | 150 | | QB2_H#q3  | 57 | 147 |

All twenty inside the 45–60 / 110–150 band. Three 60s blocks were cut after first
measurement. `QB6_H` has no `.practice-block` at all — that page renders timed answers as
`<h4>` plus `<p class="formula">`, and the new card follows its own page.

## Destination template variance

Eight destinations, eight different card contracts. Every card was cloned from a current
card in its own file:

* `.reg-box` inside `.answer-body` on QB8_A, QB7_C, QB6_D, QB7_D; outside it on QB1_D,
  QB2_H, QB6_H, QB5_A.
* `.q-footer` nested **inside** `.q-answer` on QB6_D and QB7_D, a sibling elsewhere.
* Footer control is `span.correction-link` on most, a bare `span` on QB8_A, and a
  `button.correction-btn` calling `openComment()` on QB6_H.
* Timed blocks are `span.pb-label`, `span.practice-label`, a `div.pb-label` inside
  `.answer-body` (QB5_A), a bare `<strong>` (QB2_H), or absent (QB6_H).
* Deep dive is a native `<details>`, a `div.deep-dive` driven by a button, or several
  sibling `<details class="dd">`. QB2_H has **no chevron SVG** at all.

A single universal template would have produced eight broken cards.

## Verification

| gate | result |
|---|---|
| `validate_batch_b.py` (new) | 16 PASS / 0 FAIL |
| `mutate_batch_b.py` (new) | 10 mutations, 0 escapes, 0 not applied, 0 crashes, byte-identical restore |
| pre-existing card regression | 50 pinned + all 51 on-page cards byte-identical vs `origin/main` |
| `validate_batch_a.py` | 11 PASS / 0 FAIL (after the fix below) |
| `mutate_batch_a.py` | 8 mutations, 0 escapes |
| `build_qb_content_index.py --check` | outputs match the live derivation |
| `validate_qb_content_index.py` | 24 checks, 0 FAIL |
| `mutate_qb_content_index.py` | 26 mutations, 0 escapes, 0 crashes |
| `build_examiner_index.py --check` | PASS, 4/4 artefacts current |
| `validate_examiner_index.py` | 52 PASS / 0 FAIL |
| `mutate_examiner_index.py` | 13 mutations, 0 escapes |
| `validate_ce_tip_review.py` | 28 PASS / 0 FAIL |
| `mutate_ce_tip_review.py` | 17 mutations, 0 escapes |
| `validate_phase2.py` | 107 PASS / 0 FAIL |
| `mutate_phase2.py` | 33 mutations, 0 escapes |
| `test_qb_question_text.py` | 7337 controls / 0 failures over 86 pages |
| `test_oral_controls.py` | 315 controls / 0 failures |
| `test_notes_controls.py` | 106 controls / 0 failures |
| `deploy_surface.test.mjs` | 92 pass / 0 fail |
| `regulatory_facts.test.mjs` | 16 pass / 0 fail |
| `link_integrity.mjs` | 276 pages, 8017 refs, 0 broken, 0 dead fragments |
| DOM (bs4/lxml) | all 8 destinations pass; no stray card, no duplicate id |
| determinism | 26 audit artefacts + 6 Batch-B artefacts byte-identical under `PYTHONHASHSEED` 0, 1, 524287 |

Mutation suites were run **serially**, never concurrently with a generator.

## The Batch A guard had expired, and was repaired

`validate_batch_a.py` failed the moment Batch B landed, for two reasons that are the same
mistake twice — a guard that assumes it is the last batch ever written:

* `canonical_total` pinned the corpus at exactly **696**. Replaced with
  `canonical_total_not_regressed`, which asserts Batch A's contribution has never been lost.
* `no_ninth_card` flagged **any** card in a Batch-A destination beyond its own manifest, so
  the authorised `QB6_D#q5` read as unauthorised. It now unions the anchors of every sibling
  `batch_*_manifest.json`, so "unauthorised" means "authorised by no manifest".

`validate_batch_b.py` is built so it cannot repeat this: it pins its own ten cards, unions
sibling manifests, and asserts a floor rather than an equality on the corpus total.

## Two findings worth carrying forward

**Line endings differ per file, and they broke a verifier before they broke a page.**
`.gitattributes` pins `*.html` to LF in the object store, but `core.autocrlf=true` leaves
some pages CRLF in the working tree — QB2_H, QB6_H and QB5_A are CRLF, the other five LF.
The first regression run reported *every* card on those three pages as changed, because it
compared `git show` output (normalised LF) against a CRLF working tree. Nothing was wrong
with the pages. Any tool comparing store bytes to working-tree bytes must normalise first.
Note that `mutate_batch_a.py` reads with universal newlines and writes with `newline=""`,
so on a CRLF page it would silently rewrite the file to LF while still reporting
"byte-identical" — its eight destinations happen to all be LF, so it has never bitten.
`mutate_batch_b.py` reads and writes with `newline=""` throughout.

**A gate can pass by inspecting nothing.** `tools/notes/health_check.py` takes filenames as
arguments; run with none it reports `TOTAL ERRORS: 0` and exits 0. That is a vacuous green,
not a pass. Run against `oralnotes/` it reports 349 errors — but that directory holds
`WA*-*.html`, not the "Part" files the tool is written for, and an **unmodified**
`origin/main` copy of the same file already errors. It is not a Batch-B regression and not
a valid Batch-B gate; `test_notes_controls.py` is the governed notes gate and passes 106/0.

## Deliberately not done

* **No examiner relationships added.** The authorised action is `NEW_CARD_FROM_GAP` only.
  The Examiner Index stayed at **960 relationships across 7 examiners**, and
  `build_examiner_index.py --check` passes with 4/4 artefacts current. All existing holds —
  CE-tip, ambiguous, SAME_CORE, inferred-only, human-review — remain held.
* **No cheat sheets updated.** Only three of the eight destinations have one, and no
  generator writes a cheat sheet — the build only records its filename. Hand-maintained,
  recorded as debt.
* **No neighbouring answer rewritten.** Pre-existing defects found in passing are recorded
  below, not silently repaired.
* **No workbook sync.** The master spreadsheets remain frozen.
* **`ORAL_NOTES_IMPACT.md` and `PHASE2_VALIDATION_RESULTS.json` reverted.** Running the
  oral gates re-derives both. They are harness by-products outside this batch's scope.
  Worth noting for whoever owns them: the notes-impact report now shows MISSING dropping
  42 → 38, because Batch B answers four of the asks it counts, and
  `PHASE2_VALIDATION_RESULTS.json` still records **682** canonical questions — it was
  already two batches stale before this one.

## Render

**Not verified in a real browser, and not claimed.** The Browser pane refuses `file://` and
denies `localhost`; no Chrome extension is connected; the Control-Chrome surface is
macOS-only. Substituted, per the static route: DOM validation with a real parser,
CSS-class existence checks per destination, fixed-width and image scans, long-token scans,
and table-overflow analysis. No new card uses a table, so the unstyled `.comp-table`
problem below is untouched by this batch.

## New debt

1. **`.comp-table` is used but never styled on four pages** — QB6_D, QB7_D, QB7_E, QB8_C
   render `<table class="comp-table">` with zero matching CSS, while four other pages style
   it properly. `QB6_D#q4` is a **Batch A** card, so Batch A introduced one instance.
2. **QB2_H carries internal workflow text to candidates** — its q2 version string reads
   `v1.0 · Finalised — pending Nixon final sign-off before gating`, and its correction
   mailto subject is malformed (`QQ2`). Its `<details class="deep-dive">` is also empty.
3. **QB2_H styles none of `extra-block`, `source-note`, `examiner-tag`** — its q1 and q2
   already use all three undefined, so those blocks render unstyled. The new q3 clones the
   local template and adds **no** new undefined class (a `deep-dive-body` wrapper was
   removed for exactly that reason). Its `data-tags` are also still the tokenised
   `10 / ch / code / ii-2/10` set.
4. **QB8_A#q6 leaks `[cite: 1]` artefacts** into candidate-visible reg-box text, duplicates
   its reg box inside a `<pre>` in the deep dive, carries a stray
   `CORRECTION FOOTER: QB8 · Q19 · v1.0` marker with the wrong question number, and splits
   `SOLAS Regulation II` / `2/19` across reg-code and reg-desc.
5. **QB7_D#q11 has an empty reg-desc (`—`)** and cites `SEEMP Part 2 (Reg 26A)`; Annex VI
   Regulation 26 is the SEEMP regulation and there is no 26A in the consolidated text.

## Remaining authorised workload

Brand-new answer builds: **32 authorised, 18 complete, 14 remaining** — batch P2
(GAP-0159, 0376, 0516, 0558, 0562) and the 9 notes-based promotions. Alongside them:
63 existing-answer enrichments and 35 follow-up insertions. Projected final canonical count
remains **720** (706 + 5 + 9). The master spreadsheet sync stays deferred.
