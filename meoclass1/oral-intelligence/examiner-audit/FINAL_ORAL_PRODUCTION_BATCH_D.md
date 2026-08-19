# Final Oral Production — Batch D

Nine laptop-authorised notes-based new canonical Q&A cards, built, verified and
integrated. This closes the brand-new-answer workload: **32 of 32** authorised
new cards are now live — 23 from the gap set (Batches A, B and C) and 9 promoted
from the Oral Notes.

Corpus **711 → 720** canonical questions across an unchanged **86**
question-bearing files, derived from the live HTML and independently reproduced
before and after.

## Authorisation — and why the set is nine, not ten

`FINAL_ORAL_PRODUCTION_AUTHORIZATION.json` on the laptop review branch
(`review/oral-final-gap-decision-laptop`, tip `fef45eb`). Unlike the gap
batches, this set has **no `batches.*` array**. The nine are selected by
`laptop_decision == NOTES_TO_QB_PROMOTION`.

The adjudicated total is **10**; the authorised total is **9**. The difference is
**GAP-0065**, adjudicated as a notes promotion and then *downgraded* by the
laptop review to `ALREADY_COVERED`.

Batch C was caught by `laptop_review_status` being an **audit** field rather than
an authorisation one. Here the same trap runs in the opposite direction: all nine
authorised families happen to read `LAPTOP_CONFIRMED`, so a naive status filter
would have returned the right answer *for the wrong reason*, and would have
silently admitted GAP-0065 the moment its status changed. Selection is on
`laptop_decision`.

Four independent witnesses agree on nine:

* `families[].laptop_decision == NOTES_TO_QB_PROMOTION` → 9;
* `authorised.AUTHORISED_NEW_CARD_NOTES_PROMOTIONS` = 9;
* `production_actions` of kind `NEW_CARD_FROM_NOTES` → 9 (**not**
  `NOTES_TO_QB_PROMOTION`, which returns zero — the action record uses a
  different vocabulary from the disposition record);
* `workload.NOTES_BASED_ANSWER_PROMOTIONS` = 9.

`validate_batch_d.py` asserts both halves — that all nine are present, and that
GAP-0065 specifically is absent and still reads `ALREADY_COVERED`.

## Homes

Nine promotions, nine different destination files. No two share a page, so no
sequential-anchor allocation was needed.

| family | action | home | topic |
|---|---|---|---|
| GAP-0151 | PROMNEW-001 | `QB9_A.html#q10` | COFR against the P&I Blue Card |
| GAP-0180 | PROMNEW-002 | `QB9_B.html#q9`  | Intervention Convention 1969 and its dispute machinery |
| GAP-0218 | PROMNEW-003 | `QB2_I.html#q8`  | free-fall lifeboat — certificate, height, seating, liferafts |
| GAP-0231 | PROMNEW-004 | `QB1_D.html#q7`  | Bonjean curves |
| GAP-0334 | PROMNEW-005 | `QB5_C_A.html#q11` | great circle voyage |
| GAP-0342 | PROMNEW-006 | `QB3_B.html#q21` | galvanic corrosion, the galvanic series and anodes |
| GAP-0355 | PROMNEW-007 | `QB5_B.html#q17` | embrittlement and caustic embrittlement in boilers |
| GAP-0534 | PROMNEW-008 | `QB4_H.html#q12` | Seafarer's Identity Document against the CDC |
| GAP-0621 | PROMNEW-009 | `QB9_H.html#q16` | Incoterms 2020 |

Homes were derived from topic taxonomy and the *live* QB structure, not from the
authorisation's `target` field — which holds the **Notes source**, not a QB
destination. Two choices are worth recording: `QB5_B` is titled for management
but is in fact the corpus's boiler cluster (42 boiler mentions, three dedicated
boiler-control cards), so the caustic-embrittlement card sits with its nearest
technical neighbours; and `QB5_C_A` was chosen for the great circle because its
Q3 already owns voyage performance, there being no navigation file in the corpus.

## The Notes targets were wrong for three of the nine

`target` was populated by the same automated matcher that produced this
workstream's earlier false "zero hits corpus-wide" claims. It records a page
that scored highly, not a verified section. Read section-by-section:

| family | authorisation `target` | what is actually there | section used |
|---|---|---|---|
| GAP-0334 | `miw-notes-mgmt-p13#topic-p13-3` | **the Polar Code** | `simon-notes-p4#n3` (dedicated great-circle section) |
| GAP-0231 | `miw-notes-mgmt-p16#topic-p16-6` | GZ curve / IS Code | `simon-notes-p5#n1` (dedicated Bonjean section) |
| GAP-0151 | `miw-notes-mgmt-p8#topic-36` | CLC 1992 & FUND | `miw-notes-mgmt-p21#topic-p21-1` (certificate typology) |

Promoting GAP-0334 from its recorded target would have published Polar Code
material under a great-circle question. The other six targets resolved to the
right material.

## The Notes were wrong on substance in four places

This is the half of the job that "promotion" understates. Notes are draft
evidence; every technical claim was re-verified, and four were wrong.

1. **"Blue Card = Certificate of Financial Responsibility."** Stated in
   `simon-notes-p2#n19` and `simon-notes-p3#n20` — both live, paid pages. They
   are different documents: the Blue Card goes from the club to the **flag
   State** so that State can issue the CLC or Bunkers certificate; the COFR is a
   **United States** instrument under OPA 90 (33 U.S.C. §2716, 33 CFR Part 138)
   issued by the **USCG National Pollution Funds Center**, and International
   Group Clubs **decline to act as COFR guarantors**. Only
   `miw-notes-mgmt-p21#topic-p21-1` has it right, listing them as separate
   examples. The corpus therefore contradicts itself on a live page. The new card
   states the correct position; the Notes were **not** rewritten (this is a
   promotion, not a Notes edit). Recorded as debt.
   The same Notes also give CLC's threshold as "oil tankers ≥2,000 GT"; CLC 1992
   Article VII bites on ships carrying **more than 2,000 tonnes of persistent oil
   in bulk as cargo** — a cargo quantity, not a ship tonnage.
2. **The free-fall height rule was quoted from deleted text.** The Notes give
   "Free-Fall Stowage Height ≤ Free-Fall Tube Certification Height", with
   certification height "measured … in lightest seagoing condition". That
   conflates two Code terms, and the lightest-seagoing-condition clause belonged
   to **`required free-fall height`** (LSA Code 1.1.8) — which, together with
   paragraph **4.7.3.3**, was **deleted by resolution MSC.218(82)**, in force
   1 July 2008. Current 4.7.3 has only `.1` and `.2`. Confirmed from the
   MSC.48(66) and MSC.218(82) resolution texts read directly, and cross-checked
   against a current consolidated rules service. **LSA Code 1.1.4** —
   certification height, measured from the still water surface to the lowest
   point on the lifeboat in the launch configuration — stands and is what the
   card uses.
3. **Caustic embrittlement described as "massive metal loss."** That is
   **caustic gouging**. Caustic **cracking**, which is embrittlement, is
   intergranular with little or no metal loss, which is exactly why it is not
   found by measuring thickness. The Notes' prevention ("ideal pH 8.5–10.5") is
   also the wrong control and looks like a feed-water band; the real control is a
   treatment that leaves **no free hydroxide** — coordinated phosphate/pH
   control — with **sodium nitrate** as the classical inhibitor for
   lower-pressure boilers. The Notes' own regulatory reference flags itself as
   unverified and cites **SOLAS II-1 Reg 26**; the boiler regulation is
   **Reg 32**, which requires two safety valves, two feedwater systems where the
   service is essential, and means to supervise feedwater quality.
4. **Two errors in the Bonjean section.** It lists the **centre of flotation**
   as a use — LCF comes from the waterplane half-breadth curve, not from
   sectional areas — and labels **IACS UR S1** the longitudinal strength
   standard. **UR S11** is the strength standard; **UR S1** covers loading
   conditions, manuals and instruments. Both corrected in the card.

## Re-adjudication against the current live corpus

The corpus grew 688 → 711 between adjudication and production, so every ask was
swept again with word boundaries and the **neighbouring answer bodies read**, not
scored. All nine survived as new cards; three had to be scoped down.

* **GAP-0180 nearly died on a keyword count.** `OPRC` returns 37 hits in QB3_J
  and 15 in QB9_B, and **QB9_B#q2** is literally titled around "an oil pollution
  incident in the high seas". Reading it shows it owns OPRC, SOPEP/SMPEP, the
  master's reporting duty and the CLC Blue Card — the **shipowner's duty to
  report**. The Intervention Convention is the opposite limb: the **coastal
  State's right to act** against a foreign ship it has no ordinary jurisdiction
  over, plus the Article VIII conciliation-and-arbitration machinery, which is
  the absorbed GAP-0241 limb and appears nowhere in the corpus. The card is
  scoped to intervention and dispute settlement and **cross-links** q2 for OPRC
  rather than restating it.
* **GAP-0342's stated evidence was wrong while its decision was right.** The
  authorisation says the QB carries galvanic material "only inside the in-water
  survey card". In fact it is spread across ballast-tank inspection
  (`QB3_A#q13`, `QB3_B#q3`), cold ironing (`QB6#q12`, `QB7_I#q9`), the Ship
  Construction File and drydock cards. None explains the galvanic series, anode
  selection, or the pump. Scoped accordingly.
* **GAP-0534 has one live near-neighbour the authorisation never named.**
  `QB1_F#q19` mentions the Biometric Seafarer Identity Document and ILO 185 in a
  single bullet inside "India government contribution in shipping". It does not
  answer why an SID is needed when a CDC exists. Scoped to the discrimination.
* **GAP-0355's stated evidence was also imprecise** — "every QB embrittlement hit
  is a hydrogen-fuel card". Two of the four are **cryogenic** (LPG in QB2_B, IGF
  in QB7_E). Zero are caustic. Decision right, evidence wrong. That is now the
  fourth time in this workstream a stated-evidence claim has proved false on
  inspection while the decision stood.

Nothing merged, nothing downgraded to enrichment or follow-up, nothing found
already covered. **Actual new-card count = 9**, equal to the initial
authorisation.

## Nine destinations, nine different card contracts

Batch C found three contracts across three files. With nine destinations there
are nine, and a universal template would have been wrong nearly everywhere:

* **EOL** — `QB2_I` and `QB4_H` are CRLF in the working tree; the other seven LF.
* **Timed blocks** — `.practice-block` + `span.pb-label` (QB9_A, QB9_B, QB5_C_A);
  `.practice-block` + **`div`**`.pb-label` (QB5_B); `.practice-block` +
  `<strong>15-Second Answer:</strong>` (QB4_H); `.practice-block practice-15` +
  `span.practice-label`, content in curly quotes (QB1_D); `<h4>` + `p.formula`
  (QB2_I, QB9_H); and inside `.answer-body` on QB3_B but a sibling of it
  elsewhere.
* **Nesting** — `.reg-box`/`.ce-tip` sit *inside* `.answer-body` on QB9_A,
  QB9_B, QB5_C_A and QB3_B, but are *siblings* of it on QB2_I, QB1_D, QB4_H and
  QB9_H.
* **Tags** — `tag-*` modifier classes on some pages, bare `<span class="q-tag">`
  on QB2_I and QB9_H, lowercase text on QB4_H.
* **Footers** — short mailto (QB9_A, QB9_B, QB5_C_A, QB1_D, QB5_B); long mailto
  with the "Subject / Rank, Company, LinkedIn" tail (QB3_B, QB4_H);
  `button.correction-btn` calling `openComment()` (QB2_I, QB9_H).
* **Version prefix** — `QB3_B`'s cards are versioned **`QB3B`**, without the
  underscore.
* **Deep dives** — one `details.deep-dive` (QB9_A, QB9_B, QB5_C_A, QB3_B,
  QB4_H); several sibling `details.dd` (QB2_I, QB9_H); none at all (QB1_D,
  QB5_B).
* **TOC labels** — `Q10. Topic`, `Q7 · Topic`, and bare `16. Topic`.

Every card was cloned from a current card in its own file, and the render review
confirms **every CSS class used by every new card already exists in that page's
own stylesheet**.

## Insertion method

Cards are appended immediately after the **last existing canonical card's**
matching close, located by walking `<div>` depth. Anchoring to the `#q-feed`
close would have been wrong on three pages: `QB1_D`, `QB3_B` and `QB5_B` nest
`#no-results` (and on two, `</main>`) *inside* the feed container, so an
insertion at the container close would have placed the card after the
no-results block. No `rfind('</div>')`, no marker guessing.

## Primary authority

No card is sourced from True Source: `Knowledge Central/` in this clone holds
only the FSS and casualty-investigation packages, with **zero hits on all nine
topics**. Verified against primary or authoritative sources, among them:

* **LSA Code** 1.1.4, 4.7.2, 4.7.3, 4.7.4, 4.7.5, 4.7.6, 4.7.7 read verbatim from
  the **MSC.48(66)** resolution text, with **MSC.218(82)** read for the
  deletions; **SOLAS III/31** and **III/19.3.3.4** for the liferaft and drill
  regime.
* **CLC 1992 Article VII** (>2,000 tonnes persistent oil cargo); **Bunkers
  Convention 2001 Article 7** (>1,000 GT, in force 21 November 2008);
  **OPA 90 / 33 U.S.C. §2716**; **33 CFR Part 138 Subpart A**; USCG **NPFC**.
* **Intervention Convention 1969** — adopted 29 November 1969, in force 6 May
  1975; Articles I, III, V, VI and **VIII** with its Annex, including the rule
  that exhaustion of local remedies is no ground to refuse conciliation or
  arbitration; **1973 Protocol** in force 1983; **UNCLOS Article 221**.
* **ILO C185** (2003, revising C108 of 1958) with the **2016** annex amendments
  aligning the SID to the ICAO machine-readable travel document standard.
* **ICC Incoterms® 2020**, eighth revision, in force 1 January 2020, **eleven**
  rules; DAT **renamed** DPU; CIP at Institute Cargo Clauses (A), CIF at (C).
* **DNV-RP-B401** — −0.80 V Ag/AgCl protective potential, −0.90 V anaerobic,
  −0.80 to −1.10 V working range.
* **IACS UR S11** and **UR S1**; **SOLAS II-1** Regs 3-2, 5, 32, 33; **SOLAS
  XII/11**; **SOLAS V** Regs 19, 27, 34 with **A.893(21)** confirmed still in
  force; **MEPC** Annex VI Reg 28; **MSC.215(82)**; **MSC.267(85)**.

## Numbers removed rather than guessed

* **The 1973 Protocol's exact entry-into-force day.** IMO confirms the year
  (1983); a national administration page gives 30.3.87. The card states the year
  only.
* **India's ratification of the 1969 Convention.** Could not be confirmed
  independently; the card says only that India has not ratified the **1973
  Protocol**, which the national administration's own published position
  supports, and tells the candidate to check the coastal State concerned.
* **A single boiler-water pH band.** The Notes' 8.5–10.5 looks like a feed-water
  figure. The card gives "commonly in the region of pH 10.5–11.5" and says
  explicitly that the maker's and treatment supplier's limits govern — and that
  the control is the absence of free caustic, not a pH reading.
* **A shipbroker-style commission or fixed free-fall height** were never
  asserted; there is no universal free-fall height, it is whatever is on the
  certificate.

## Timed blocks

House range 15s 48–67 words, 60s 106–153:

| card | 15s | 60s |
|---|---|---|
| QB9_A#q10 | 63 | 134 |
| QB9_B#q9 | 59 | 127 |
| QB2_I#q8 | 61 | 132 |
| QB1_D#q7 | 55 | 127 |
| QB5_C_A#q11 | 59 | 134 |
| QB3_B#q21 | 59 | 134 |
| QB5_B#q17 | 63 | 134 |
| QB4_H#q12 | 58 | 139 |
| QB9_H#q16 | 54 | 133 |

All eighteen inside band.

## Examiner relationships — structurally zero

`build_examiner_index.py` harvests card-level attributions only from a
`data-examiner` attribute, never from prose. The new cards carry `data-tags`
only, so the delta is zero by construction. Confirmed three ways: the generator
reports **960 relationships across 7 examiners**, unchanged; `--check` passes
4/4 artefacts current; and the only line that moved in
`EXAMINER_INDEX_SNAPSHOT.json` is `canonical_questions: 711 → 720`. Both examiner
HTML pages are byte-identical.

Three cards name an examiner in the CE tip where the local file convention does
so and the evidence supports it (Simon on QB2_I, Nair on QB9_H). The rest use the
un-named form.

## A stale TOC repaired on one page

`QB1_D` listed only Q1–Q4 against six cards, and its `sec-count` and
`q-count-label` both read 4 — Batch B added q5 and q6 without them. Inserting a
seventh entry into that TOC would have produced a visibly broken Q1–Q4, Q7
sequence. TOC entries for **q5, q6 and q7** were added and the two counters
corrected to 7. This is the only pre-existing defect repaired in this batch, and
only because the insertion depended on it.

## Public count

Eight occurrences of the old corpus figure, all in `SQ/index.html`: the meta
description, three prose claims, the `data-oral-questions` attribute and its
visible `stat-num`, a feature-list item, and a payment-confirmation string.
All eight updated 711 → 720 with character-level proof — every changed character
is `1→2` or `1→0`, line count unchanged, no length change, and the 19
occurrences of the price string untouched. `validate_examiner_index.py` then
passes its own "no stale oral figure survives in candidate-visible SQ home text".

## Verification

| gate | result |
|---|---|
| `validate_batch_d.py` (new) | **22 PASS / 0 FAIL** |
| `mutate_batch_d.py` (new) | **12 mutations, 0 escapes, 0 not applied, 0 crashes**, byte-identical restore |
| pre-existing card regression | **102** pinned cards across 9 files byte-identical vs `origin/main`, EOL-normalised |
| `validate_batch_a.py` | 11 PASS / 0 FAIL |
| `mutate_batch_a.py` | 8 mutations, 0 escapes, 0 not applied, 0 crashes |
| `validate_batch_b.py` | 16 PASS / 0 FAIL |
| `mutate_batch_b.py` | 10 mutations, 0 escapes, 0 not applied, 0 crashes |
| `validate_batch_c.py` | 16 PASS / 0 FAIL |
| `mutate_batch_c.py` | 10 mutations, 0 escapes, 0 not applied, 0 crashes |
| `build_qb_content_index.py --check` | matches the live derivation (86 files, 720 questions) |
| `validate_qb_content_index.py` | 24 checks, 0 FAIL |
| `mutate_qb_content_index.py` | 26 mutations, 0 escapes, 0 crashes, live artefacts byte-identical |
| `build_examiner_index.py --check` | PASS, 4/4 artefacts current, 960 relationships |
| `validate_examiner_index.py` | 52 PASS / 0 FAIL |
| `mutate_examiner_index.py` | 13 mutations, 0 escapes |
| `validate_ce_tip_review.py` | 28 PASS / 0 FAIL |
| `mutate_ce_tip_review.py` | 17 mutations, 0 escapes |
| `validate_phase2.py` | 107 PASS / 0 FAIL |
| `mutate_phase2.py` | 33 mutations, 0 escapes |
| `test_qb_question_text.py` | **7477** controls / 0 failures over 86 pages (was 7387) |
| `test_oral_controls.py` | 315 controls / 0 failures |
| `test_notes_controls.py` | 106 controls / 0 failures |
| `test_examiner_check.py` | 10 tests / 0 failures |
| `deploy_surface.test.mjs` | 92 pass / 0 fail |
| `regulatory_facts.test.mjs` | 16 pass / 0 fail |
| `link_integrity.test.mjs` | 20 pass / 0 fail — 0 broken refs, 0 dead fragments |
| `qb_health_check.py` | **identical multiset to the `origin/main` baseline — 0 new findings** |
| DOM | all 9 destinations div-balanced, no duplicate id, no card outside `#q-feed` |
| determinism | 6 generated artefacts byte-identical under `PYTHONHASHSEED` 0, 1, 524287 |

Mutation suites were run **serially**, never in background, never concurrently
with a generator.

The health-check baseline was taken by running the tool on a **clean detached
worktree of `origin/main`**, not by reading a committed results file. Its raw
diff shows 32 changed lines, but the two outputs are **multiset-identical** at
470 lines each — `qb_health_check.py` emits its changelog-gap section in
non-deterministic order. Recorded as debt; there are no new findings.

### The predecessor guards did not expire

Batch B's redesign — assert a **floor**, and union the anchors of every sibling
`batch_*_manifest.json` — held again. All three predecessor validators failed
transiently on `no_sixth_card` while `batch_d_manifest.json` did not yet exist,
and all three cleared the moment it was written, with **no change to any of
them**. `validate_batch_d.py` is built the same way and will not expire when the
enrichment work lands.

### One crash, contained

`mutate_examiner_index.py` died with a `UnicodeEncodeError` printing an emoji to
a cp1252 console. Per the crash-safe rule the artefact hashes were re-checked
**immediately**, before anything else touched the tree: unchanged, nothing left
mutated. Re-run under `PYTHONIOENCODING=utf-8` it passed 13/0. This is a console
encoding fault in the harness, not a validation failure, but it is a real
crash-exposure path on Windows.

## Render

**Not verified in a real browser, and not claimed.** The Browser pane is policy
blocked for localhost and for the live site in this environment, and the Chrome
extension surface is not connected. Substituted, per the static route: DOM
validation by balanced-tag walk; **CSS-class existence checked per destination —
every class used by every new card exists in that page's own inline
stylesheet**; and fixed-width, inline-style, long-token, table and image scans on
all nine cards. No new card uses a table or an image, none carries a fixed pixel
width, none carries an inline style, and there are no unbreakable long tokens.

## Deliberately not done

* **No examiner relationships added.** All existing holds remain held.
* **No Notes file edited.** This is a promotion, not a Notes rewrite; the four
  substantive Notes errors above are recorded as debt, not silently patched.
  `test_notes_controls.py` passes and all nine source sections still resolve.
* **No cheat sheets updated.** Seven of the nine destinations have one
  (`QB1_D` and `QB3_B` have none). No generator writes a cheat sheet — the build
  only records the filename. Hand-maintained, recorded as debt.
* **No enrichment or follow-up work started.**
* **`PHASE2_VALIDATION_RESULTS.json` reverted.** Running the oral gates
  re-derives it (682 → 720); it is a harness by-product outside this batch.
* **No workbook sync.** The master spreadsheets remain frozen.

## New debt

1. **Two live paid Notes pages equate the Blue Card with the COFR.**
   `simon-notes-p2#n19` and `simon-notes-p3#n20`. The same sections give CLC's
   threshold as a gross tonnage rather than 2,000 tonnes of persistent oil cargo.
   This is a cross-product contradiction against `miw-notes-mgmt-p21#topic-p21-1`
   and against the new QB9_A card.
2. **`CORRECTION FOOTER:` is candidate-visible on three QB pages** — 22
   occurrences across `QB8_A`, `QB9_A` and `QB9_B`, inside deep-dive blocks. Some
   reg-descs on `QB9_A` also carry `[cite: 1]` residue. Pre-existing; not
   replicated by the new cards.
3. **`QB5_C_A#q10` ships an empty 15-second answer block and an empty
   `reg-desc`.** Pre-existing.
4. **`qb_health_check.py` emits its changelog-gap section in non-deterministic
   order**, which makes a raw baseline diff unreadable and could hide a real
   regression behind reordering noise.
5. **`mutate_examiner_index.py` (and the other emoji-printing harnesses) crash on
   a cp1252 console.** They need `PYTHONIOENCODING=utf-8` or an explicit
   `reconfigure`; a crash mid-run is a mutation-escape exposure.

## Remaining authorised workload

Brand-new answer builds: **32 authorised, 32 complete — closed.** 23 gap-based,
9 notes promotions. Remaining: **63** existing-answer enrichment actions (from 68
source families) and **35** follow-up insertion actions (from 39 source
families). Final projected canonical count for the enrichment and follow-up work
is unchanged at **720**, since neither creates new cards. The master spreadsheet
sync stays deferred until both are done.
