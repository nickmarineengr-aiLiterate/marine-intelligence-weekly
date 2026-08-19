# Final Oral Production — Batch A

Eight laptop-authorised P1-A new canonical Q&A cards, built, verified and integrated.

## Authorisation

`FINAL_ORAL_PRODUCTION_AUTHORIZATION.json` → `batches.P1-A`, on the laptop review branch.
All eight family records carry `adjudicated_decision = NEW_CANONICAL_QA`,
`laptop_decision = NEW_CANONICAL_QA`, `laptop_review_status = LAPTOP_CONFIRMED`,
`priority = P1-A`, `confidence = HIGH`, and a production action of kind
`NEW_CARD_FROM_GAP`. No examiner-relationship action is authorised for any of them,
so the Examiner Index receives no relationship delta in this batch.

## Homes

| family | production action | home | topic |
|---|---|---|---|
| GAP-0080 | NEW-001 | `QB1_C.html#q8`  | verifying welding after a side shell plate renewal |
| GAP-0225 | NEW-008 | `QB2_E.html#q2`  | the forward liferaft and why it may carry no HRU |
| GAP-0262 | NEW-009 | `QB6_D.html#q4`  | NOx formation and onboard compliance verification |
| GAP-0378 | NEW-012 | `QB3_B.html#q20` | SOLAS II-1/29 steering gear capability and redundancy |
| GAP-0415 | NEW-014 | `QB10_B.html#q9` | autonomous ships and the MASS Code |
| GAP-0465 | NEW-017 | `QB3_F.html#q7`  | bunker ordering, disputes, samples and retention |
| GAP-0478 | NEW-018 | `QB4_G.html#q10` | SAR notification, COSPAS-SARSAT and INDSAR |
| GAP-0619 | NEW-022 | `QB9_B.html#q8`  | medical evacuation, diversion and who bears the cost |

Corpus **688 → 696** canonical questions across an unchanged **86** files.

## Duplicate-home control

Every ask was swept against the live QB HTML before authoring, not against the derived
manifest. Two sweeps had to be re-run: `HRU` and `MASS ` matched inside `through` and
`mass flow`, inflating 1 real hit to 49 and 26 to 161. With word boundaries applied:

* float-free / HRU vocabulary — **1** hit corpus-wide, in the SEQ survey checklist.
* MASS / autonomous — **26** hits, all inside amendment-overview cards; no owning card.
* Bunker delivery note — `QB4_I#q2` owns BDN and MARPOL sample tracking, but only inside
  an ISM-audit frame. Ordering, disputes and the sample set are unowned. Cross-linked.
* Medevac / telemedical — **4** hits corpus-wide.

### GAP-0378 scope

The authorisation record's stated reason ("three weak hits") is wrong: *steering gear*
occurs **111 times across 45 cards**. But **no q-text anywhere in the corpus mentions
steering**, so every one of those hits is incidental answer-body prose. Reading the stems
confirmed the record's substance and its correction: the pre-departure test limb is
genuinely housed in `QB1_K#q9` (SOLAS V/26 — test within 12 hours before departure,
second power unit in restricted waters) and the drill limb in `QB4_C#q9` (3-monthly
emergency steering drill). The new card is therefore scoped to the **II-1/29 capability
and redundancy requirements only**, and cross-links both other cards rather than
repeating them. A keyword census measures vocabulary spread, not topical ownership.

## Primary authority

No card in this batch is sourced from the True Source corpus: the packages reachable from
this clone hold amendment PDFs, not consolidated instrument text, for every topic here.
All eight were verified directly against IMO, IACS, ILO, class and flag-administration
publications — among them SOLAS II-1/29 paragraphs 3, 4, 6.1, 7, 11–16 (MSC.1/Circ.1398
and MSC.365(93)); SOLAS III/31.1.4 with MSC.1/Circ.1490/Rev.1; LSA Code 4.1.3.2, 4.1.6.2
and 4.1.6.3; IACS Rec. No. 47 Part B and UR S14, W28, W32, W33, W35, Z13; the NOx
Technical Code chapter 6 with MARPOL Annex VI regulation 13; MARPOL Annex VI regulations
14, 14.8 and 18 with MEPC.324(75), MEPC.182(59) and MEPC.1/Circ.875; the IMO MASS Code
adoption briefing; the Indian National Maritime SAR Plan and ISRO's COSPAS-SARSAT
description; and MLC 2006 Regulations 2.5, 4.1 and 4.2.

## Verification

| gate | result |
|---|---|
| `validate_batch_a.py` | 11 PASS / 0 FAIL |
| `mutate_batch_a.py` | 8 mutations, 0 escapes, 0 not applied, byte-identical restore |
| `validate_qb_content_index.py` | 24 checks, 0 FAIL |
| `mutate_qb_content_index.py` | 26 mutations, 0 escapes |
| `validate_examiner_index.py` | 52 PASS / 0 FAIL |
| `build_examiner_index.py --check` | PASS, 4/4 artefacts current |
| `mutate_examiner_index.py` | 13 mutations, 0 escapes |
| `validate_phase2.py` | 107 PASS / 0 FAIL |
| `validate_ce_tip_review.py` | 28 PASS / 0 FAIL |
| `test_qb_question_text.py` | 7237 controls / 0 failures over 86 pages |
| `test_oral_controls.py` | 315 controls / 0 failures |
| `test_notes_controls.py` | 106 controls / 0 failures |
| `deploy_surface.test.mjs` | 92 pass / 0 fail |
| QB health check | 181 advisories, identical to the pre-change baseline |
| determinism | derived artefacts byte-identical under `PYTHONHASHSEED` 0, 1 and 524287 |
| existing cards | all 60 pre-existing cards on the eight pages byte-identical |

`validate_batch_a.py` and `mutate_batch_a.py` are new and committed with the batch.
The mutation harness reports a mutation that changes no bytes as **NOT APPLIED** rather
than counting it as caught, and proves the restore by digest.

## Two findings worth carrying forward

**Inline markup inside a q-text desynchronises two governed extractors.** `NO<sub>x</sub>`
in a question made the content-index builder emit `NO x` while the validator's live reader
emitted `NOx`, failing the text-drift check. The corpus convention is already plain `NOx`
in q-text, so the card was fixed rather than the tooling — but any inline tag in a q-text
will reproduce this.

**The 15/60-second blocks had to be cut roughly in half.** As first drafted they averaged
108 and 200 words against a corpus norm of 51 and 115 — a "15-second answer" no candidate
could deliver in fifteen seconds. They now sit at 57 and 137. The cards remain longer than
the corpus median because several of these asks are genuinely three- and four-limbed.

## Deliberately not done

* **No examiner relationships added.** The authorised action is `NEW_CARD_FROM_GAP` only;
  no relationship action exists for these ids. All unrelated holds remain held.
* **No cheat sheets updated.** None of the destination cheat sheets is generated from a
  question inventory, so none is governed to track a new question. Recorded as debt.
* **No workbook sync.** The master spreadsheets remain frozen until the approved new
  cards, notes promotions and enrichments are all stable.
* **No neighbouring answer rewritten**, including several pre-existing defects found in
  passing on the destination pages. They are recorded as debt, not silently repaired.

## Remaining authorised workload

Brand-new answer builds: **32 authorised, 8 complete, 24 remaining** — batch P1-B
(GAP-0083, 0113, 0120, 0124, 0128, 0365, 0412, 0418, 0442, 0728) and batch P2
(GAP-0159, 0376, 0516, 0558, 0562), plus the notes-based promotions.
Alongside them: 9 notes-based answer promotions, 63 existing-answer enrichments and
35 follow-up insertions. Projected final canonical count remains **720**.
