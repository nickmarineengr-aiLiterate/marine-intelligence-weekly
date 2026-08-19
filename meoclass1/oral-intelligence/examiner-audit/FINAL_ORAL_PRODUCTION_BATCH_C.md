# Final Oral Production — Batch C

Five laptop-authorised P2 new canonical Q&A cards, built, verified and integrated.
This closes the gap-based new-card workload: 23 of 23 authorised NEW_CANONICAL_QA
cards are now live.

## Authorisation — and a reconciliation worth recording

`FINAL_ORAL_PRODUCTION_AUTHORIZATION.json` → `batches.P2`, on the laptop review branch
(`review/oral-final-gap-decision-laptop`, tip `fef45eb`). The five are **GAP-0159,
GAP-0376, GAP-0516, GAP-0558, GAP-0562**.

Deriving that set by the literal filter *(decision = NEW_CANONICAL_QA, status =
LAPTOP_CONFIRMED, confidence = HIGH, priority = P2)* returns **four, not five**.
GAP-0516 carries `laptop_review_status = LAPTOP_CHANGED`.

That is a field-semantics trap, not a missing authorisation. `laptop_review_status` is an
**audit-trail** field — *did this row change?* — not an **authorisation** field — *is this
row approved?* For GAP-0516 the change was a **promotion**: it was held as
medium-confidence and left uncounted, and the laptop review raised it to HIGH/P2/NEW
because it is the only medium candidate carrying multi-family mass, absorbing GAP-0517
(cost estimation) and GAP-0519 (drydock frequency and job scope).

Three independent witnesses agree the batch is five:

* the authorisation's own `batches.P2` array lists five;
* `authorised.AUTHORISED_NEW_CANONICAL_QA = 23`, which reconciles only as 8 + 10 + **5**;
* the Batch B handoff names the same five as the remaining P2 work.

`validate_batch_c.py` does **not** resolve this by relaxing the check to "any status".
The manifest records the expected `laptop_review_status` per family and the validator
asserts an exact match, so the guard is strictly tighter than Batch B's blanket equality:
a silent change to any one of the five dispositions, in either direction, fails the build.

All five carry a production action of kind `NEW_CARD_FROM_GAP`. No relationship-kind
action exists for any of them, so the Examiner Index receives **no relationship delta**.

## Homes

| family | action | home | topic |
|---|---|---|---|
| GAP-0376 | NEW-011 | `QB4_G.html#q11` | attempted stowaway — definition, cost, action on discovery |
| GAP-0516 | NEW-019 | `QB4_G.html#q12` | dry dock budgeting and job prioritisation |
| GAP-0159 | NEW-007 | `QB9_H.html#q14` | capital, voyage and operating cost, and who pays under which charter |
| GAP-0562 | NEW-021 | `QB9_H.html#q15` | what a ship broker is |
| GAP-0558 | NEW-020 | `QB5_I.html#q7`  | motor ship against steam turbine — the owner's case |

GAP-0516 arrived with `target: null` — no home was proposed. It was placed at `QB4_G#q12`
because QB4_G already owns the drydock cluster (`q4` manpower, `q5` preparation and
interval), so the three cross-links are same-page anchors.

Corpus **706 → 711** canonical questions across an unchanged **86** question-bearing
files, derived from the live HTML and independently reproduced before and after.

## The count trap in this corpus

The corpus holds **716 `.q-card` blocks but 711 canonical questions** — five cards are not
questions (two named study aids in QB1_A, three with an empty `id`). Before this batch the
figures were 711 blocks against 706 questions, so a validator counting raw `.q-card`
elements would have read **711** *before a single card was written* and passed vacuously,
reporting success for work never done. Every count in this batch is gated on
`id="q<N>"`, never on the class alone.

## Duplicate-home control

Every ask was swept against the live QB HTML with word boundaries, and the nearest
neighbours were read rather than scored. Nothing had to be stopped. Four findings:

* **"Ship broker returns zero hits corpus-wide" is false as stated, and right as decided.**
  The sweep found **6 occurrences across 3 cards** — NVOCC "space brokering" in QB2_B#q7,
  "bunker brokers" in QB1_F#q6, "unverified brokers" in QB1_G#q32. All three are
  incidental; no card defines the chartering intermediary, so the decision stands while
  its stated evidence does not. This is the third time a "zero hits corpus-wide" claim in
  this workstream has proved false on inspection.
* **GAP-0159 needed scoping against a live neighbour the authorisation never named.**
  `QB5_I#q2` carries `capital cost` seven times and `operating cost` five. Reading it
  shows it is **cost-benefit analysis** — FSA, GCAF/ICAF, CAPEX-versus-OPEX as a decision
  tool — and it never decomposes voyage cost at all. Different question. The new card is
  scoped to the cost *taxonomy* and its charter allocation, and cross-links q2.
* **GAP-0516 had to be scoped down, not rejected.** Its absorbed GAP-0519 ("drydock
  frequency and job scope") is **already owned** — `QB4_G#q5` and `QB3_A#q5` both give the
  interval and the work-list scope. What is genuinely unowned is budgeting, cost
  estimation and prioritisation. The card is scoped to those and cross-links the interval
  rather than restating it. Same pattern as GAP-0728 in Batch B.
* **GAP-0558 and GAP-0376 are clean gaps.** "Convince owner / business case" returns
  **zero** cards corpus-wide and no card compares a motor ship to a steam turbine. All ten
  stowaway mentions are one-clause items inside P&I cover lists or ISPS threat lists.

## Primary authority

No card is sourced from True Source: `Knowledge Central/` in this clone holds only the FSS
and casualty-investigation packages, with **zero hits on all five topics**.

The stowaway card is built on primary text extracted from the **FAL 50 resolution
document** rather than on any summary. Verified verbatim:

* **Resolution FAL.20(50)**, adopted **27 March 2026**, allocation of responsibilities to
  apply **as from July 2026** — current as of today.
* Its Annex §2.1 defines **attempted stowaway** as detected on board *"before the ship has
  departed from the port"*, against a stowaway detected after departure, or in cargo while
  unloading at the port of arrival, *and reported as a stowaway by the master*.
* The commercial consequence, which is the half most candidates miss: where the person is
  found before sailing, *"no charge is to be imposed on the shipowner in respect of
  detention or removal costs, and no penalty is to be imposed."*
* Section 4 (Stowaways) was inserted into the FAL Convention annex by **FAL.7(29)**,
  adopted **10 January 2002**, in force **1 May 2003**.
* Lineage of the guidelines: A.871(20) → MSC.312(88) → FAL.11(37) → FAL.13(42) →
  MSC.448(99) → **FAL.20(50)**. ISPS **B/9**, **B/16** and **B/8.9**, and
  **FAL.2/Circ.50/Rev.3** for the reporting format.

**A.871(20) is the dated-but-plausible trap here** — it is what most training material
still quotes, and it is four revisions out of date. The card names it only as superseded,
and **mutation H** downgrades FAL.20(50) to it and requires the validator to notice.

Other cards: BIMCO **GENCON 2022**, **NYPE 2015** and **BARECON 2017** confirmed as the
current forms, with BIMCO's own text confirming the bareboat charterer bears operating
expenses; **Institute of Chartered Shipbrokers**, Royal Charter **1920**; **MLC 2006
Title 2**; **ISM Code sections 3, 9 and 10**; **SOLAS I/10**, **II-1**, **XI-2**;
**MARPOL Annex VI regulations 13, 14 and 28**; **STCW Regulation III/2** at **3,000 kW**.

Two numbers were **removed rather than guessed**, per the no-guessed-numbers rule:

* **A steam-plant thermal efficiency figure.** The ~50% for a modern low-speed two-stroke
  is corroborated independently; the commonly quoted ~30% for a marine steam plant could
  not be sourced to a primary or class authority, and the OEM page carried no figure at
  all. The card states the *direction and cause* of the gap and omits the number.
* **A shipbroker commission percentage.** The customary 1.25% could not be verified —
  the Baltic Exchange site is behind a challenge wall — so the card describes commission
  as a negotiated percentage of freight, hire or price and explicitly warns against
  quoting a rate. The **brokerage versus address commission** distinction is given
  instead, which is the discriminating detail anyway.

## A live corpus inconsistency, deliberately routed around

Several existing cards assert **"Reg 24 for EEXI, not Reg 23/25"** and *"Regulation 24 is
the EEXI regulation number"*. That contradicts the Chapter 4 numbering Batch B verified
from the resolution text (22 Attained EEDI, 23 Attained EEXI, **24 Required EEDI**, 25
Required EEXI, 26 SEEMP, 27 fuel oil consumption data, 28 Operational carbon intensity).

This is pre-existing debt and was **not** repaired — the rule is to baseline unrelated
defects, not silently fix them. But it changed this batch's authoring: GAP-0558 would
naturally have cited EEXI regulation numbers, and doing so would have created a visible
cross-product contradiction. The card is anchored on **regulation 28 (CII)** instead,
which the corpus states consistently. Recorded as debt below.

## Timed blocks

Measured with balanced-tag extraction against the house norm (15s 48–67 words, 60s
106–153):

| card | 15s | 60s |
|---|---|---|
| QB4_G#q11 | 63 | 131 |
| QB4_G#q12 | 64 | 140 |
| QB9_H#q14 | 56 | 113 |
| QB9_H#q15 | 66 | 147 |
| QB5_I#q7  | 65 | 140 |

All ten inside band. `QB4_G#q12`'s 15s measured 68 on first draft and was cut to 64.

## Destination template variance

Three destinations, three different card contracts. Every card was cloned from a current
card in its own file:

* **QB4_G** (LF): timed blocks are `div.snap-box` with a `<b>` label; a `div.ce-relevance`
  block inside `.answer-body`; deep dive is one `details.dd` containing a `.dd-body` of
  `.dd-item` rows; footer is `span.correction-link` with a **short** mailto (no trailing
  "Subject / Rank, Company, LinkedIn" tail); `q-text` carries `itemprop="name"`; three
  `q-tag`s; TOC label style `Q11. Topic`.
* **QB9_H** (CRLF): 15s is `<h4>` + `p.formula`, 60s is `<h4>` + plain `<p>`; several
  sibling `details.dd` each with a bare `<p>`; footer is a **`button.correction-btn`**
  calling `openComment()`, not a mailto link; two uppercase `q-tag`s; no filter buttons;
  TOC label style `14. Topic` with **no** "Q" prefix.
* **QB5_I** (CRLF): same timed-block shape as QB9_H but the footer is the **long**
  `span.correction-link` mailto with the full trailing tail, and the CE tip label is the
  plain `CE Oral Tip:` rather than QB9_H's `CE Oral Tip (Name):`.

A single universal template would have produced three wrong footers and two wrong TOC
labels. The first TOC entry written for QB4_G used `Q11 &middot; …` and was corrected to
the local `Q11. …` form.

## Examiner relationships — structurally zero, not merely asserted

`build_examiner_index.py` harvests card-level attributions **only from a `data-examiner`
attribute**, never from prose. The new cards carry `data-tags` only, so the delta is zero
by construction rather than by inspection. Confirmed three ways: the generator reports
**960 relationships across 7 examiners** unchanged; `--check` passes 4/4 artefacts
current; and the only line that moved in `EXAMINER_INDEX_SNAPSHOT.json` is
`canonical_questions: 706 → 711`. Both examiner HTML pages are byte-identical.

No examiner is named in the two cards whose evidence would not support it — GAP-0159's
recorded examiner has no primary MIW evidence, so its CE tip uses the un-named form even
though QB9_H's local convention names one.

## Verification

| gate | result |
|---|---|
| `validate_batch_c.py` (new) | 16 PASS / 0 FAIL |
| `mutate_batch_c.py` (new) | 10 mutations, 0 escapes, 0 not applied, 0 crashes, byte-identical restore |
| pre-existing card regression | 29 pinned cards byte-identical vs `origin/main`, EOL-normalised |
| `validate_batch_a.py` | 11 PASS / 0 FAIL |
| `mutate_batch_a.py` | 8 mutations, 0 escapes |
| `validate_batch_b.py` | 16 PASS / 0 FAIL |
| `mutate_batch_b.py` | 10 mutations, 0 escapes |
| `build_qb_content_index.py --check` | matches the live derivation (86 files, 711 questions) |
| `validate_qb_content_index.py` | 24 checks, 0 FAIL |
| `mutate_qb_content_index.py` | 26 mutations, 0 escapes, 0 crashes |
| `build_examiner_index.py --check` | PASS, 4/4 artefacts current, 960 relationships |
| `validate_examiner_index.py` | 52 PASS / 0 FAIL |
| `mutate_examiner_index.py` | 13 mutations, 0 escapes |
| `validate_ce_tip_review.py` | 28 PASS / 0 FAIL |
| `mutate_ce_tip_review.py` | 17 mutations, 0 escapes |
| `validate_phase2.py` | 107 PASS / 0 FAIL |
| `mutate_phase2.py` | 33 mutations, 0 escapes |
| `test_qb_question_text.py` | **7387** controls / 0 failures over 86 pages (was 7337) |
| `test_oral_controls.py` | 315 controls / 0 failures |
| `test_notes_controls.py` | 106 controls / 0 failures |
| `test_examiner_check.py` | 10 tests / 0 failures |
| `deploy_surface.test.mjs` | 92 pass / 0 fail |
| `regulatory_facts.test.mjs` | 16 pass / 0 fail |
| `link_integrity.mjs` | 8030 refs, 0 broken, 0 dead fragments |
| `qb_health_check.py` | 189 findings, **identical to the `origin/main` baseline** — 0 new |
| DOM (stdlib parser) | all 3 destinations balanced; no duplicate id; TOC count == card count |
| determinism | 6 generated artefacts byte-identical under `PYTHONHASHSEED` 0, 1, 524287 |

Mutation suites were run **serially**, never concurrently with a generator.

The health-check baseline was taken by running the tool on a **clean detached worktree of
`origin/main`**, not by reading a committed results file — a committed result is not a
baseline.

### The Batch A and B guards did not expire this time

Batch B had to repair Batch A's guard because it hard-pinned the corpus at 696. Batch B's
redesign — assert a **floor**, and union the anchors of every sibling
`batch_*_manifest.json` — meant Batch C required **no change to either predecessor**.
`validate_batch_a.py` did fail once, transiently, before `batch_c_manifest.json` existed;
writing the manifest cleared it, which is the designed behaviour. `validate_batch_c.py`
is built the same way and will not expire when Batch D lands.

## Render

**Not verified in a real browser, and not claimed.** A static server was started from the
committed `miw-static` launch configuration, but the Browser pane denied navigation to
`localhost`, and the Chrome extension surface is not connected. Substituted, per the
static route: DOM validation with a real parser; CSS-class existence checked per
destination; fixed-width, inline-width, long-token, image and table scans on every new
card. No new card uses a table or an image, none carries a fixed width above 340px, and
the only long token is the correction email address — both mailto destinations carry the
`word-break:break-all; min-width:0` rule that exists for exactly that.

## Deliberately not done

* **No examiner relationships added.** All existing holds — CE-tip, ambiguous, SAME_CORE,
  inferred-only, human-review — remain held.
* **No cheat sheets updated.** `QB4_G_CheatSheet.html` and `QB9_H_CheatSheet.html` exist;
  QB5_I has none. No generator writes a cheat sheet — the build only records its filename.
  Hand-maintained, recorded as debt.
* **No neighbouring answer rewritten.** Defects found in passing are recorded below.
* **`PHASE2_VALIDATION_RESULTS.json` reverted.** Running the oral gates re-derives it; it
  is a harness by-product outside this batch's scope. Worth noting for whoever owns it: it
  still records **682** canonical questions and was already three batches stale.
* **No workbook sync.** The master spreadsheets remain frozen.

## New debt

1. **EEXI regulation numbering is wrong on live cards.** At least three assert Reg 24 is
   the EEXI regulation; 24 is *Required EEDI*, and 23/25 are Attained/Required EEXI. This
   is a cross-product contradiction waiting to be quoted at an oral.
2. **`dd-item` and `q-version` are unstyled on QB4_G.** Both already appear ten times on
   `origin/main`, so this is inherited, not introduced; `dd-item` carries an inline
   `margin-bottom` and `q-version` inherits from `.q-footer`, so neither renders badly.
3. **`QB4_G`'s `itemprop="name"` is orphan microdata** — the attribute appears on every
   `q-text` with no enclosing `itemscope`/`itemtype`, so it declares nothing. Cloned
   faithfully into the two new cards to match the local template.
4. **`mutate_ce_tip_review.py` and `mutate_phase2.py` are slow enough to hit a two-minute
   timeout**, and a kill mid-run leaves `STRONG_CE_TIP_REVIEW_DECISIONS.json` mutated on
   disk. The harness restores correctly when allowed to finish, but there is no
   crash-safe restore. A caller that times out must re-check the tree.
5. **Cheat sheets for QB4_G and QB9_H are now one batch behind** their pages and no
   generator owns them.

## Remaining authorised workload

Brand-new answer builds: **32 authorised, 23 complete, 9 remaining** — all of them
notes-based new-card promotions; the gap-based new-card workload is now **closed at 23 of
23**. Alongside them: **63** existing-answer enrichments and **35** follow-up insertions.
Projected final canonical count remains **720** (711 + 9). The master spreadsheet sync
stays deferred.
