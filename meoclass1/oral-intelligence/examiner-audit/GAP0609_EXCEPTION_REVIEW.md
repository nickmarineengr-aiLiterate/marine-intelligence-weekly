# GAP-0609 — post-collision Chief Engineer response

Bounded exception review. One family, one decision, one card.

Date: 2026-08-20 · Branch: `prod/oral-gap0609-post-collision` · Base: `origin/main` at `0efe3b5`

---

## Why this session existed

The final enrichment consolidation disposed of every family except one. GAP-0609
was parked as `NEW_CARD_REVIEW_REQUIRED` because its authorised enrichment
target did not own the topic, and new-card production had already been declared
closed at 32/32. The consolidation was explicit that this meant the final
authorisation had missed a genuine new-card need, and left it for adjudication
rather than forcing it into a card that could not hold it.

This review verified that finding independently against the live corpus rather
than accepting it.

## Source ask

One occurrence, `ASC-0645`, examiner Nair, source page 49:

> Collision happened between your ship and another vessel. He wants to know wat
> all will u check? like water tight integrity and how reporting will be done?
> wat all documents n records will u submit? told VDR. he wanted to know more,
> couldnt say. Asked about who pays for the Insurance for ship. Told him about
> 3 by 4 clause, he asked who pays 3/4th and who pays the remaining 1/4th.

The candidate answered "VDR" and could not continue. That is the shape of the
gap: the examiner wanted the record set, and the corpus had no card that listed
it under a collision.

## What the record said, and what was actually true

| Claim in the record | Verified? |
|---|---|
| Authorised target `QB5_B#q9` is "the collision card" | **No.** `QB5_B#q9` is CBDR — collision *avoidance* under COLREGS Rule 7. Its only post-collision text is a passing clause. It owns none of the ask. |
| `notes_support: NO_NOTES_SUPPORT`, `notes_units: []` | **No.** `oralnotes/miw-notes-mgmt-p15.html` Oral Q&A Q1 asks the CE's data-preservation duty *after a collision in Indian waters* and who must be notified — on a page carrying a Nair CE Oral Tip, the same examiner. |
| No post-collision response card exists | **Yes.** Confirmed by canonical q-text sweep over all 720 plus semantic reads. |

The Notes error is the reconciliation failure mode already on record: the matcher
scored the ask against the question bank only, so the examiner-organised Notes
were invisible to it. Notes support does not dissolve this gap — it supplies
verified material for it, and a promotion of that unit creates a card rather
than enriching one.

## Coverage actually found

Read in full: `QB5_B#q9`, `QB4_G#q7`, `QB4_G#q6`, `QB9_H#q2`, `QB9_H#q3`,
`QB1_supplementary#q18`, `QB1_supplementary#q16`, `QB5_I#q3`, `QB5_C_A#q8`,
`QB5_C_B#q5`, `QB1_F#q1`.

- **Technical damage response** — `QB4_G#q7` (hull damage or oil pollution) is
  strong: soundings, watertight doors, bilge and ballast, emergency bilge
  suction, damage control kit.
- **Reporting and investigation** — `QB9_H#q2` is strong: DPA, flag, coastal
  State, class, P&I, and the flag State safety investigation.
- **The record set** — `QB5_C_B#q5` carries a full evidence-preservation
  procedure, but under a war-zone fatality stem.
- **Insurance 3/4 vs 1/4** — heavily covered across QB9_A/B/C/D and QB1_A/B.
  Cross-linked, deliberately not restated, per the consolidation overlap note
  against ENR-003 / GAP-0616.

So the material largely exists — scattered across five cards and two Notes
pages, under stems a candidate searching "collision" will never reach. Searching
collision returns collision avoidance, the collision bulkhead and the liability
clauses.

**Collision bulkhead is not collision response.** `QB1_supplementary#q18` is a
SOLAS II-1/12 design requirement — position from the forward perpendicular,
height, permitted openings. It was not counted as casualty-response coverage.

## Candidate-failure test

> Studying the current 720-question QB plus the Oral Notes, can a candidate give
> a coherent CE response to "your ship has collided, what do you do now"?

**Materially no.** Only by knowing in advance to merge a hull-damage-and-pollution
card, a generic flag-State casualty card, a war-zone fatality investigation card,
an emergency-contacts card and an Indian-waters Notes Q&A. Nothing routes the
word collision to any of them, and the ask is one flowing examiner chain.

## Decision

Last-resort test A–D all **NO**, E **NO** → **NEW_CANONICAL_QA**.

Enrichment into `QB4_G#q7` was rejected specifically: it is stemmed to hull
damage or oil pollution, built as a two-branch structure, and absorbing this ask
means adding collision-specific action, the statutory casualty reporting chain
and the full submitted record set — four substantive limbs, leaving the stem
inaccurate and the topic still undiscoverable.

## The card

`QB4_G.html#q13` — *"Your ship has been in a collision with another vessel — as
CE what will you check, how is the reporting done, and what documents and
records must be preserved and submitted?"*

Home chosen because QB4_G already holds the CE operational casualty
neighbourhood: Q7 the hull damage response, Q6 the casualty investigation, Q10
informing authorities after a rescue. QB9_H was rejected as the home — it is the
legal and liability file — and is cross-linked instead.

Structure: check → contain → report → preserve → follow up. 15s 60 words, 60s
125 words. Cross-links to `QB4_G#q7`, `QB4_G#q6`, `QB9_H#q2`,
`QB1_supplementary#q16` and `QB9_A#q3`.

### Authority

Every instrument verified; nothing carried across unchecked.

- Casualty Investigation Code, Res. MSC.255(84), mandatory via SOLAS XI-1/6
- SOLAS Ch. V, Reg. 20 — VDR carriage
- Res. MSC.333(90) — capsules at least **48 hours**, long-term medium **30 days**,
  VDRs installed on or after **1 July 2014**
- MSC/Circ.1024 — VDR ownership and recovery; the owner is responsible for
  timely preservation after a casualty
- ISM Code Sections 8 and 9
- SOLAS Ch. II-1, Reg. 19 — damage control information
- Collision Convention 1910, Art. 8 — duty to assist and exchange particulars

Deliberately omitted: any Note of Protest hour figure (jurisdiction dependent),
and the superseded A.861(20) VDR retention figure.

## Corpus debt found, not fixed

`oralnotes/simon-notes-p5.html` tells the candidate to answer VDR retention as
"48 hours primary loop, **12 hours protected capsule**, 30 days long-term
medium". Under Res. MSC.333(90) the protected fixed and float-free capsules
retain **at least 48 hours**; the 12-hour figure belongs to the superseded
A.861(20) standard. As printed, the answer would be marked wrong. Out of scope
for this bounded session — **reported, not fixed**.

## Guards repaired

Adding a card past a closed batch tripped three guards, all the expiring-guard
defect class rather than real findings:

- `validate_batch_a` `no_ninth_card` and `validate_batch_c` `no_sixth_card` read
  `QB4_G#q13` as unauthorised. Both already discover legitimate later additions
  by globbing sibling `batch_*_manifest.json`, so
  `tools/oral/batch_e_gap0609_manifest.json` was added to carry the
  authorisation. No code change.
- `validate_batch_d` `count_reconciles` pinned the live total to
  `baseline + n`, which expires on the next authorised card. Relaxed to `>=`,
  the same reasoning already applied to `canonical_total_not_regressed`. Check
  counts did not fall: A 11, B 16, C 16, D 22, all 0 FAIL.

## Verification

- Canonical corpus **720 → 721**, files 86, 721 unique file#anchor, 0 duplicates.
- All 12 pre-existing `QB4_G` cards byte-identical, digests embedded in the
  review record so the assertion is re-run rather than trusted.
- `validate_gap0609_exception.py` 59 checks / 0 FAIL.
- `mutate_gap0609_exception.py` 8 mutations / 0 escapes / 0 no-ops / 0 crashes.
- Product gates all green; `qb_health_check` identical to `origin/main` (76/20/3),
  `QB4_G.html` clean.
- Examiner relationships unchanged at 960 / 7; delta 0 — the exception review
  carries no examiner relationship authorisation.
- **NOT BROWSER VERIFIED** — the repo sits outside the pane's project folder and
  renders as a static snapshot with no scripting. Substituted: DOM balance
  (345/345 file, 28/28 card), q13 inside `#q-feed`, every class matched against
  the file's own conventions, toggle/filter/observer contracts checked against
  the file's own JS, no tables, images or overflow tokens beyond the standard
  footer email which `.correction-link` already breaks.

## State after this session

- Brand-new answer builds **33/33** — the final new-card inventory is closed.
- Canonical corpus **721**.
- Enrichment consolidation still **50 unique existing-answer edit actions** —
  unchanged. ENR-049 was never one of the 50: it was the single family the
  consolidation excluded as `NEW_CARD_REVIEW_REQUIRED`, and it is now closed as
  a new card instead.
- Follow-up work still **35 groups** — unchanged.
- Master XLSX **deferred**.
