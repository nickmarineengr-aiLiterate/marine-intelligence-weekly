# Strong CE-tip held-relationship review — ten pairs, item by item

**Branch:** `review/oral-strong-ce-tip-held-relationships` from `origin/main @ 689c0d6`
(verified: clean tree, `main == origin/main`, no intervening commit touched the
relationship datasets, evidence ledgers, generator or the ten canonical targets).
**Decision artefact:** `STRONG_CE_TIP_REVIEW_DECISIONS.json` (machine-readable, one
record per pair; this file is the narrative only).
**Gate:** `tools/oral/validate_ce_tip_review.py` · **Mutations:** `tools/oral/mutate_ce_tip_review.py`.

## What "the ten" are

There is no labelled artefact. The set is the intersection of `RELEASE_A_HELD.json`
(33 rows) with `READY_CONNECTIONS_V2.json` rows whose `phase1_strength` is
`STRONG_CE_TIP_ASSERTION`: exactly **10**, all held `HOLD_EVIDENCE_BELOW_FLOOR` because
`finalize_release_a.py` ranks `CE_TIP` (2) under the release floor (3). Their research tier
read `PRIMARY_TRACKER`, but that came from a readiness status stamped on page-prose pairs
— the very defect the finalize step corrected. The honest starting provenance is CE tip.

`STRONG_CE_TIP_ASSERTION` is a **regex flag** (`prose_evidence.py`: an assertive verb within a
~360-character window around the examiner's name inside a CE Oral Tip block). It is not a
read. This session read every tip and every card.

## Standard applied

Two separate dimensions, never collapsed:

* **CE provenance class** — is the card's tie of examiner to *this question* declarative
  (asks / typically asks / expects you to / wants / opens with / will pivot to) or merely
  conditional (`If Nair asks …`, `If asked by Simon …`) or a style remark? Conditional-only
  = `CE_STRONG_BUT_NONEXPLICIT`, on the brief's own scale ("Likely asked by …" is weaker).
* **Target correctness** — does *this* card answer what the tip says the examiner asks?

A conditional tie was allowed to reach CE Tip **only** when an independent same-examiner
record on the same target answered the "whether" (§18 C). Corroboration was searched inside
the governed evidence only (master ledger, 788 dispositions, Notes evidence, reverse
connections); the July per-examiner sheets were treated as derived and never counted; the
historical index was not consulted as evidence of an ask.

## Ten-item matrix

| # | relation | examiner | target | tip wording (pinned) | CE class | target | corroboration found | decision | tier |
|---|---|---|---|---|---|---|---|---|---|
| 1 | RELA-NAIR-QB10_B-q7 | Nair | NZF status / NE-Atlantic ECA | "If Nair asks 'when does the Net-Zero Framework come into force'…" | STRONG_BUT_NONEXPLICIT | correct | ASC-0672 (Nair, *SOx/NOx/GHG compliance* — off-demand, PARTIAL); Notes name **Simon** as the GHG examiner | **HOLD_WEAK_ASSERTION** | — |
| 2 | RELA-NAIR-QB2_A-q25 | Nair | Persistent floater | "If Examiner Nair asks you: 'Does … palm oil … Type 2 chemical tanker require a mandatory pre-wash … Kochi?'" | STRONG_BUT_NONEXPLICIT | correct | **ASC-0400 Nair "Persistent floaters, prewash criteria" → this target (PARTIAL)**; NOTEV-0237 (Nair topic tag) | **APPROVE_CE_TIP** | ce_tip |
| 3 | RELA-SIMON-QB10_B-q1 | Simon | SOLAS/MARPOL amendments 2024–28 | "Simon will pivot straight to what applies to YOUR ship: as a container vessel…" | EXPLICIT_FOLLOWUP | correct (CE Relevance answers it) | ASC-0192/0316 Simon "Container fire fighting latest amendment" → this target (PARTIAL); Simon Confirmed on sibling latest-amendments cards (MASTER-AQ-0178 → QB1_F#q20, -0455 → QB4_E#q4) | **APPROVE_CE_TIP** (FOLLOW_UP) | ce_tip |
| 4 | RELA-SIMON-QB1_F-q3 | Simon | VGM — who issues/verifies | "Examiner Simon expects you to state clearly that the shipper — not the carrier — carries the VGM obligation" | EXPLICIT_EXPECTED_DETAIL | correct | NOTEV-0475 Simon Notes "Simon Sir / Rajappan typically ask: What is VGM and the two methods?"; MASTER-AQ-0228 Simon "VGM, who decide the weight" (VERIFIED, on sibling QB2_B#q11) | **APPROVE_CE_TIP** | ce_tip |
| 5 | RELA-SIMON-QB2_A-q4 | Simon | Container tracking / ISO 6346 | "If Examiner Simon asks you: 'What is the practical purpose of the Check Digit…'" | STRONG_BUT_NONEXPLICIT | correct | ASC-0191/0369 Simon "prevent loading of undeclared cargo" (off-demand, PARTIAL); card's chain and tracker (MASTER-AQ-0012) give this question to **Nair** | **HOLD_WEAK_ASSERTION** | — |
| 6 | RELA-SIMON-QB3_B-q1 | Simon | Hull survey | "If asked by Simon, lead with watertight integrity and load line compliance" | STRONG_BUT_NONEXPLICIT | correct | none for Simon (hull/class-survey tracker asks are Nair's) | **HOLD_WEAK_ASSERTION** | — |
| 7 | RELA-SIMON-QB6_E-q2 | Simon | GFI Calculation & Unit | "If he asks for the 'GFI calculation unit,' give the unit immediately" | STRONG_BUT_NONEXPLICIT | **ambiguous** — QB6_E#q3 is titled *"GFI Calculation and Unit (Duplicate/Deepened Focus)"* and already carries Simon **Confirmed** | MASTER-AQ-0180/0202 Simon "GFI calculation unit" — governed-mapped to **q3** | **HOLD_TARGET_AMBIGUOUS** | — |
| 8 | RELA-SIMON-QB6_F-q4 | Simon | MMSI | "Simon opens with the structure/definition, then a reflagging scenario, then checks whether you know MMSI changes require technician-level access" | EXPLICIT_PRIMARY_ASK | correct (only MMSI card) | NOTEV-0367 "Simon Sir typically asks 'What is MMSI and when must it change?'" (reverse-connected to this pair); ASC-0338 Simon "MMSI" → this target (AMBIGUOUS = terse, single candidate, coverage 1.0); MASTER-AQ-0240 Simon "mmsi" UNRESOLVED | **APPROVE_CE_TIP** | ce_tip |
| 9 | RELA-SIMON-QB9_F-q11 | Simon | Official Number | "Examiner Simon wants a precise differentiation between the Official Number and the IMO number" | EXPLICIT_EXPECTED_DETAIL | correct (only Official Number card) | MASTER-AQ-0242 Simon "official number" — legacy mapping UNRESOLVED, parked on QB4_H#q1 (AECS course; plainly wrong) | **APPROVE_CE_TIP** | ce_tip |
| 10 | RELA-SIMON-QB9_F-q8 | Simon | FOC / Open Registry | "Examiner Simon wants a direct answer on India’s status" | EXPLICIT_EXPECTED_DETAIL | correct | **MASTER-AQ-0080 Simon "foc.open registry.does india have open registry." → this target, PARTIAL_MATCH (score 0.429 vs a terse title)** | **APPROVE_CE_TIP** | ce_tip |

**Tally:** APPROVE_CE_TIP 6 · APPROVE_REPORTED 0 · APPROVE_CONFIRMED 0 · HOLD 4 (3 weak, 1
target-ambiguous) · REJECT 0. Relationship types: PRIMARY_ASK 5 of the 6 approved,
FOLLOW_UP 1 (#3). No pair involves John.

## Why nothing went above CE Tip

Three approved pairs (#8, #9, #10) have a **primary tracker record naming the same examiner
and the same ask**, and one (#7, held) has two. None is governed-admissible for Confirmed:
`MASTER-AQ-0080` is `PARTIAL_MATCH`, `-0240` and `-0242` are `UNRESOLVED`, `-0180/-0202` are
mapped to the duplicate sibling. Re-adjudicating a legacy mapping is a ledger decision, not a
relationship-review decision, so the tier stays CE Tip and the records are carried as
`corroboration_ids` / `evidence_ids` with the mapping status stated. The path to Confirmed is
named in each record's `next_action`. Likewise `ASC-0400`, `-0192`, `-0316` are PARTIAL and
`ASC-0338` terse-AMBIGUOUS, so nothing is Reported; the 788 was not reopened.

## The "Kochi MMD Focus" question

The heading sits on every card of `QB9_F` and `QB1_F`, which looked like page-level
attribution (§9). It is not: the examiner named inside it varies per card (QB9_F: q1–q2 Nair,
q4–q6/q8–q11 Simon; QB1_F: 12 Nair, 5 Simon), and siblings with the identical formula are
tracker-Confirmed for Simon (QB9_F#q6, #q10; QB1_F#q13–15, #q20). Two of the three Simon
"Kochi" cards under review turned out to have primary Simon records for the same ask. Per-card
authoring, apparently from tracker records — not a template rotation.

## How approvals reach the index

`build_examiner_index.py` gains a fourth input route, `CE_TIP_REVIEW`: it reads the decision
artefact, publishes only `APPROVE_*` rows, at exactly the tier the outcome permits, and refuses
the build (not skips) on an unknown outcome, a tier the outcome does not permit, an approved
row without evidence ids, a held row carrying a tier, a duplicate relation, or a target that
does not name its own relation id. `RELEASE_A_PUBLICATION.json`, `RELEASE_A_HELD.json` (still 33)
and every evidence ledger are untouched — the governed Release-A gates in `validate_phase2.py`
(floor ≥ NOTE_EXPLICIT, tier derivable from evidence ids) keep proving Release A itself, and
these six render with source `CE_TIP_REVIEW`, never `RELEASE_A`.

Evidence-id conventions: `PROSE:<examiner>:<qid>` resolves to the `PROSE_EXAMINER_EVIDENCE.csv`
row (`in_ce_tip_block` true) and is pinned by `reviewed_ce_tip_wording`, which the gate requires
to remain on the live card (mutation G2 edits the card; caught). `ASC-*` must have this question
as its governed target; `MASTER-*` this question as `canonical_question_id`; `NOTEV-*` must be
reverse-connected to this pair. `corroboration_ids` need only resolve and name the examiner.

## Counts (all from the generated snapshot)

| | before | after |
|---|---|---|
| relationships | 954 | **960** |
| ce_tip / confirmed / reported / header / inferred | 208 / 453 / 43 / 39 / 211 | **214** / 453 / 43 / 39 / 211 |
| Nair | 360 (92 ce_tip) | **361** (93) |
| Simon | 275 (54 ce_tip) | **280** (59) |
| others | unchanged | unchanged |

Publication delta = exactly the six approved pairs; nothing removed, nothing re-tiered.

## Gates

`validate_ce_tip_review.py` 28/0 · `mutate_ce_tip_review.py` 17/0 escapes (A1 A2 B1 B2 B3 C
D1 D2 E F1 F2 G1 G2 H I J K, all semantic, artefacts and `QB9_F.html` restored byte-for-byte) ·
`validate_examiner_index.py` 52/0 · `mutate_examiner_index.py` 13/0 · `validate_phase2.py` 107/0
· determinism byte-identical at `PYTHONHASHSEED` 0 / 1 / 524287 · clean regeneration zero diff ·
`build_qb_content_index.py --check` clean · oral controls 315/0 · notes controls 106/0 ·
question-text gate 7157/0 · deploy-surface 92/92 · link integrity 20/20 · QB health baseline
identical (91 files / 181 pre-existing findings before and after). No `QB*.html` changed.

## Newly discovered debt (max 3)

1. **Three primary Simon records are mis-mapped or unresolved against the only card that
   answers them**: `MASTER-AQ-0080` (FOC/India, PARTIAL on QB9_F#q8), `MASTER-AQ-0242`
   ("official number", UNRESOLVED, parked on an AECS card), `MASTER-AQ-0240` ("mmsi",
   UNRESOLVED). A bounded governed mapping re-adjudication would lift #8/#9/#10 to Confirmed.
2. **`QB6_E#q2` / `#q3` are a live duplicate pair** — q3's own title says so — with Simon
   Confirmed on the duplicate. Content dedup decision needed before any index change there.
3. `ASC-0338` (Simon "MMSI") sits in the terse human-review queue with a single candidate at
   coverage 1.0; the Simon Notes give the disambiguating context. Belongs to the P1/P2 queue.

## Left alone (per brief)

788 reconciliation · matcher · QB answers · new P0 · changelog gaps · 43 tier literals ·
reverse Asked-by · Written QI · magazine · payments · master XLSX v26 / July SHARE (v27 /
August SHARE deferred until approved oral updates are stable) · the other 27 held pairs (still
held) · the two review-held pairs (still held; mutation H proves they cannot re-enter here).
