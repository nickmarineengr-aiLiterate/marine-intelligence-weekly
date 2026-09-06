# PASS 1 TERMINAL CLOSURE — 7 September 2026

**Record id:** `P1TERM-20260907`
**Baseline:** `ac61228` · **Predecessor:** `P1GUARD-20260906`
**Product bytes changed: ZERO.**

## The chain

```
CORR-T5-DDCASCADE / -REACH / -HYDRANT      the original Pass 1
  └─> CORR-P1REPAIR-20260906               its two P0 escapes
        └─> CORR-P1CLOSE-20260906          the repair's three P1 escapes
              └─> P1GUARD-20260906         the guard weaknesses that survived all three
                    └─> P1TERM-20260907    E1-E4 + generated-surface provenance
```

Nothing earlier is rewritten. `P1GUARD-20260906` recorded four escapes as OPEN and
declined to claim closure over them; this record closes exactly those four and the
generated-surface question they exposed, and nothing else.

## What was closed

| id | The escape | How it is closed |
|---|---|---|
| **E1** | A denial clause silenced a live claim coordinated with it: *"BMP5 replaced BMP4 **and** remains the current industry standard"*. | **Bounded clause segmentation**: a coordinator splits where BOTH SIDES CARRY A FINITE VERB. Two verbs is two predications; a noun list predicates once and is left intact. And **subject inheritance**, for the shared-subject form where the live clause never names BMP5 — judged only on an explicit currency assertion, because an inherited subject is an inference. |
| **E2** | `BMP-5` was invisible, and `normalise` folds every unicode dash toward that unmatched ASCII form — normalisation and matcher pulled opposite ways. | One publication, three ordinary spellings: `BMP5`, `BMP 5`, `BMP-5`. Detection only; no card's spelling is rewritten. |
| **E3** | A governing figure with no modal — `Hydrant pressure - 0.27 N/mm²` — was undetectable at any unit. | The default is **INVERTED**, as it already is for BMP5. 0.27 and 0.25 MPa are not arbitrary quantities: they ARE the two limbs SOLAS II-2/10.2.1.6 fixes, so a fire-main sentence stating one is asserting the regulation whether or not it says "minimum". It is a claim unless it reads as an **observation** (on trials, measured, logged, typically). Every MUST-NOT-CATCH in the contract carries an UNGOVERNED figure and is refused long before this test. |
| **E4** | The subject in a preceding sibling block — `<h4>Fire main</h4><li>Minimum 0.27 MPa</li>` — defeated the detector. | A structural label reaches the block beneath it, bounded by **element identity** and by a segment count. Not a character window: the ±220-character window is the defect this replaces. |
| **generated surfaces** | `topics.html` carried four BMP5 mentions the gate never examined, because the whole surface was skipped. | The surface is now swept, and status is decided **item by item from provenance**. |

## Generated-surface policy

A generated page gets **no blanket exemption**. Its status is inherited from the
provenance of each item:

- a **question-stem echo** — a row that is entirely the text of a link into a question
  card — is the examiner's wording and takes the historical policy, exactly as it does
  on the card it quotes;
- a **label or description the generator authors itself** is teaching, and takes the
  currentness policy like any other teaching text;
- **navigation** inherits the semantics of what it points at.

The distinction is structural, so it cannot be satisfied by adding a class to a
template: a stem echo is recognised by the `href` that names the card it quotes. One
test asserts both directions on the same page, same class, same element — opposite
verdicts decided by provenance alone.

### The four `topics.html` mentions, adjudicated

All four are **A / C — HISTORICAL EXAMINER WORDING, echoed as navigation — KEEP**.
Each traces to a `q-text` question stem in a question-bank card, and each is emitted by
`tools/study/build_topic_pages.py` as `<li><a href="QBx.html#qN">` inside
`<ul class="q-list">`:

| row | owning stem |
|---|---|
| "What are the Best Management Practices (BMP5) for piracy prevention…" | `QB4_B.html#q16` |
| "Describe the key content and operational phases of BMP5…" | `QB4_H.html#q11` |
| "…BMP5 measures." | `QB9_A.html#q9` |
| "War risk / vessel hardening / BMP5 — provide detailed…" | `QB9_B.html#q5` |

No source correction is required and no generated HTML was hand-edited. The earlier
report's guess that two of the four were generator-authored topic labels was **wrong**:
both are sentences of an examiner's stem, and the second is the whole stem.

## The first attempt at E1 and E3 failed, and how

Both were closed once by enumeration and reopened by the independent verifier, inside
their own declared classes — not as new families:

- **E1** was first closed by requiring a coordinated clause to OPEN with its verb, on
  the reasoning that a coordinated predicate shares its subject. True of the shape the
  escape was reported in, and blind to the commoner one, where the live clause states
  its own subject: *"BMP4 was withdrawn **and** BMP5 is the current industry guidance"*.
  The denial then silenced the sentence exactly as before. The repair is clause-shaped
  rather than word-order-shaped: **a verb on each side**.
- **E3** was first closed with a label:value shape plus a numbers-context vocabulary.
  Four trailing words defeated the shape (`Hydrant pressure: 0.27 N/mm2 on cargo ships`
  — the `$` anchor), and ordinary prose defeated the vocabulary (`SOLAS II-2/10.2.1.6
  gives 0.27 N/mm2 at the hydrant for cargo ships`). The reg-box row is the very surface
  three earlier defects in this family were found on. The repair stops enumerating and
  **inverts the default**.

That is the sixth and seventh instance of one lesson: a shape or a vocabulary is an open
set. Both repairs replace one with a property — "two predications" and "a governed limb,
unless observed" — and both were verified against the live corpus, which stayed at zero
under the wider rules.

## Second independent review — four more, all fixed

A second clean-context verifier, given the goal and not the implementation, reproduced
four further guard defects. All four were reproduced here before being accepted, all
four are inside the declared E1/E3/E4 classes or the §11 false-positive duty, and none
was a live content defect:

| # | Finding | Repair |
|---|---|---|
| 1 | **The corpus's own dominant numeric idiom escaped entirely.** `<td>Fire main hydrant pressure</td><td>0.27 N/mm2</td>` lent no subject to its own value, while the identical row with `<th>` was caught — because `th` was a label tag and `td` was not. Two-cell label/value rows appear in **153 of the 224 files**. | The **first cell of a table row labels the rest of that row**, whatever tag it uses, and the scope ends with the row. A markup choice a reader cannot see must not change what a guard sees. |
| 2 | **The pronoun escaped.** *"BMP5 was superseded in 2025, **but it** is still the guidance we apply on board."* `but` is a hard boundary, so the live clause landed in the next sentence group and inheritance stopped there. English prefers the pronoun on second mention, so this is the **more** natural way to write the defect, not a rarer one. | A pronoun subject inherits across **one** sentence boundary, and only on an explicit currency claim. A sentence-initial subordinator (*"Although BMP5 was superseded, it is…"*) now splits at its comma. |
| 3 | **False positive: the fire-main detector had no examiner-stem exemption at all.** It skipped three provenance classes where the BMP5 detector consults the whole excused-class set, so it would have reported an examiner's own stem as a defect — pointing an operator at the one edit the corpus rule forbids, modernising anchored wording. | The two detectors now excuse the same things. The asymmetry was the bug. |
| 4 | **False positive: correct history flagged.** *"Before 2025 the guidance was region-locked — BMP5 for the Red Sea…"* is **verbatim live in `QB4_H.html`** and survived only because its container happened to carry a governing note; on a cheat sheet it read as teaching BMP5 as current. | A **dated frame is a denial**: `before <year>`, `until <year>`, `region-locked`. It puts a sentence in the past as surely as a verb does. |

Verified after all four: the live corpus stayed at **firemain 0 / BMP5 0** across all 173
non-past-paper files, so none of the widenings produced a false positive.

## Third independent review - four more fixed, one deferred as the top debt item

| # | Finding | Disposition |
|---|---|---|
| **E2** | *"BMP5 was superseded in 2025. **Nevertheless, it** remains the guidance we apply."* The pronoun rule was anchored on the bare pronoun, and English almost always fronts an adverbial first - so it missed 10 of 10 natural phrasings. | **FIXED.** Up to two adverbial openers may precede the pronoun. |
| **E3** | `_VERB` listed `governs` but not `governed`, `covered`, `specified`, `mandated`. With no recognised verb on the left the coordinator refused to split, and the left clause's denial silenced the live claim: *"BMP5 governed HRA transits before 2025, and it remains the current industry guidance."* 11 of 12 missed. | **FIXED.** The past-tense forms an author actually reaches for are recognised. |
| **FP2** | The fire-main detector had no question exemption, where the currentness detector has had one from the start. A trap question or practice prompt quoting the figure was reported as teaching it. | **FIXED.** A question is not an assertion - the same rule, one layer down. |
| **FP1b** | The exemption's own container test read **raw HTML** with a literal attribute pattern - the one path that never went through the normalising segmenter. `<div id="q1" class="q-card">`, single quotes, an extra class and `<section>` each broke it, and when it breaks an entire card of correct history is reported as live teaching. | **FIXED.** Attribute order, quote style, extra classes and the three container tags all resolve alike. |
| **E1w** | **The whole-card exemption itself.** A card carrying a supersession banner is exempt in its entirety, so a live claim *inside* it is invisible while the same words one byte outside are reported. | **DEFERRED - the single most serious open item in this record.** |

### The deferred item, stated plainly

`_governing_currentness` grants a **whole-card** exemption. That makes the detector
structurally blind to this corpus's own documented defect shape: `QB4_B.html` records a
correction of 6 Sep 2026 reading *"the body and Numbers layers still taught BMP5 as the
current publication, contradicting this card's own banner"*. The banner is exactly what
buys the immunity.

It is not a parser edge case and it is not being dismissed as one. It is deferred for two
reasons, both stated so a reader can overrule them:

1. **It is outside the E1-E4 + generated-surface contract this record was authorised to
   close**, and that authorisation forbids redesigning the detector architecture again.
2. **Removing it requires that redesign.** The exemption exists because the sentence-level
   rule flags plain past-tense history - *"BMP5 was published in 2018"*, *"BMP5 covered the
   Red Sea"* - at a measured **18 of 18** false positives on real corpus sentences once the
   exemption is neutralised. Dropping the whitelist without first teaching the detector
   that a past-tense predication about a superseded publication is history would trade a
   blind spot for eighteen false alarms on correct text.

The principled repair is a tense-and-aspect rule, not another list. **Recommended as the
first item of a Pass 1.5**, before any new paid surface depends on this guard.

No live content defect follows from it: three independent verifiers, each with their own
enumeration and their own regexes, measured the corpus clean.

## Two defects found while closing, worth as much as the closure

**A committed regex had two dead alternatives.** `oral_currentness.py` carried a literal
`0x08` byte where `\b` was intended, in `PROVENANCE_HINT` (`questions on\b`) and
`CURRENTNESS_MARK` (`replaced\b`) — written that way at `a2c83bd` by a shell heredoc that
ate the backslash. Both alternatives could never match. Both fail **closed** (a lost
excuse makes the detector more suspicious, not less), so no defect escaped through them,
but a named alternative that cannot fire is a check that is not there. Repaired, and a
scan now catches the byte class — and found a **third** instance, in
`tools/oral/validate_tranche4a.py:191`, where `HG1` had become
`HG1`. Repaired; that gate stays 85/85.

**A control passed for the wrong reason.** `E4_label_does_not_leak_across_containers`
used an unrelated heading ("Lifeboat davits"), which is refused by the *subject* test
whether or not the container bound exists — so the bound was never actually proven. The
mutation that removed the bound exposed it. The check now uses the same "Fire main"
label and the same governed figure separated only by a **closed** container, and the
container bound is compared by **element identity**: two sibling `<div>`s both spell
"div", so a tag-name comparison let a label leak across a boundary it was supposed to
stop at.

## Vacuous-check audit (new controls only)

Each new control names a reachable failing state and one mutation reaches it:

| control | mutation that kills it |
|---|---|
| `E1_coordinator_splits_clauses_not_noun_lists` | `E1-E` (two edits — see below) |
| `E1_MUST_CATCH_denial_then_live_claim` | `E1-D` |
| `E2_hyphenated_name_is_the_same_publication` | `E2-D` |
| `E3_MUST_CATCH_modal_free_governing_figure` | `E3-D` |
| `E4_label_does_not_leak_across_containers` | `E4-D` |
| `generated_surface_status_follows_item_provenance` | `G-D` |
| `E4_first_table_cell_labels_its_row` | `E4-T` |
| `E1_pronoun_carries_the_subject_one_sentence` | `E1-P` |
| `firemain_excuses_examiner_wording_like_bmp5_does` | `F-X` |
| `historical_date_framing_is_a_denial` | `H-D` |
| `E1_adverbial_opener_does_not_hide_the_pronoun` | `E1-O` |
| `E1_past_tense_verbs_still_form_a_clause` | `E1-V` |
| `currentness_exemption_survives_markup_variation` | `W-D` |
| `firemain_excuses_a_question_like_bmp5_does` | `F-Q` |

`E1-E` is **two edits in one mutation**, and that is a finding in itself. The noun-list
rule is defended twice over — the both-sides verb test, and the rule that a verbless
fragment merges forward instead of standing as a proposition. Removing either alone
changed nothing the control could see, and the mutation reported an escape the guard had
not suffered. Redundancy is good design and bad for a mutation suite: crediting a kill
to an edit that left the property standing is exactly the false credit these suites
exist to refuse.

## Evidence

- **Controls:** `tools/oral/test_currentness_detectors.py` — 32 checks, 0 FAIL, over 95
  adversarial cases including 6 E1 MUST-CATCH (both the shared-subject and own-subject
  shapes) with 3 MUST-NOT-CATCH, the 3 E2 spellings, 7 E3 MUST-CATCH with 4
  MUST-NOT-CATCH, and both E4 directions, plus the table-row idiom in both tag spellings,
  five pronoun sentences with two bounds, the examiner-stem symmetry and the dated frame.
  Every case two independent verifiers used to reopen this closure is in the set as a
  case, not as prose.
- **Mutations:** `tools/oral/mutate_correction_p1guard.py` — **38 of 38 behaved as
  required, 0 escapes, 0 crashes**, serial, byte-exact restore. 34 must-catch (product
  and detector) and 4 must-NOT-catch: past-paper wording, a wholly historical
  coordinated sentence, an unrelated heading, and a generated stem echo.
- **Gates:** p1repair 50, struct 23, reach 42, hydrant 35, scope 10, detectors 32,
  tranche4a 85 — 0 FAIL.
- **Live corpus, recursive, 224 files:** fire-main incomplete-scope claims **0**;
  BMP5-as-current **0**, generated surfaces now included.

## Residual release-hardening debt

Declared, not hidden, and outside the closure contract. **The whole-card currentness
exemption (E1w above) is the top item and is P1-grade guard debt, not P2/P3** - it has its
own heading above rather than being buried here. The rest:

- **P2** - `OBSERVATION` is tested before `MANDATORY`, so a hedge beats an explicit
  requirement: *"In practice the minimum hydrant pressure is 0.27 N/mm2"* reads as a
  report. No live instance.
- **P2** - `HEADING_CLASSES` carries seven class names with zero occurrences in this
  corpus and omits the ones it does use (`dd-label`, `cs-label`). Structural label
  detection therefore rests on the tag set, which does cover the live pages.
- **P2** - *"Even though"* and *"Notwithstanding that"* openers are split by the
  subordinator rule before the leading-clause rule sees them.
- **P2** - a correction footnote outside the three provenance classes is judged as
  teaching.

- **P3** — CSS- or JavaScript-generated text, malformed markup beyond the parser's
  recovery, OCR-style corruption, and claims carried only in HTML attribute text.
- **P3** — units outside the eleven in the conversion table, and unit spellings no
  maritime author uses.
- **P3** — `oral_lib.all_anchors()` enumerates top level only. Used by the
  examiner-index and matcher validators, by no closure gate, and its subject (q-card
  anchors) exists only on top-level pages.
- **P2** — clause segmentation is bounded, not a parser. A subject carried across a
  full sentence boundary, or through a construction outside the coordinator set, is not
  inherited. No live instance; a defect of this shape would have to be written
  deliberately.
- **P3** — publication-name forms outside the three ordinary spellings: `BMP.5`,
  `BMP v5`, `BMP 5th edition`. Outside the declared E2 class and unused on this corpus.
- **P3** — a structural label whose heading is wrapped in its own element (so the value
  block is not inside the heading's parent), or a value more than `HEADING_REACH` = 8
  segments after it. Both are the bound working as designed at its edge.
- **KEEP, adjudicated** — `QB4_B.html:1931` lists BMP5 among the publications the bank
  was compiled from. A compilation provenance statement is a historical fact about the
  sources read, not a claim of current authority.

## Closure standard applied

Pass 1 closes when no LIVE P0/P1 content defect remains and no realistic E1–E4-class
guard escape remains. A verifier's sixth, seventh or eighth theoretical parsing edge
case outside the declared contract is release-hardening debt, recorded above — not a
reason to keep Pass 1 open.
