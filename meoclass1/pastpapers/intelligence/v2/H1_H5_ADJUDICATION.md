# H1–H5 — Phase 2 adjudication

**RESEARCH ONLY.** `current_as_of: 2026-08-17`

Each hypothesis pairs a **recurrence** claim with a **date** claim. Phase 2 keeps
them apart, and the two moved in opposite directions: **recurrence got much
stronger, every date stayed unsupported.**

The individual Phase-1 files under `verification/` are retained unedited as the
record of what was known then. This file supersedes their verdicts.

---

## Summary

| | Claim | Recurrence | Date | Source | Status |
|---|---|---|---|---|---|
| **H1** | `QP2608-Q1` ↔ June 2010 | **HIGH** ↑ | **NONE** | **HIGH** ↑ | recurrence upheld, **date rejected** |
| **H2** | `QP2608-Q2` ↔ December 2011 | **HIGH** ↑↑ | **NONE** | **HIGH** ↑ | recurrence upheld and **widened**, **date rejected** |
| **H3** | `QP2608-Q2` ↔ October 2012 | **HIGH** ↑↑ | **NONE** | **HIGH** ↑ | same family as H2, **date rejected** |
| **H4** | `QP2608-Q4` ↔ April 2010 | **HIGH** ↑↑↑ | **NONE** | **HIGH** ↑↑↑ | **reversed** — ancestor found, **date rejected** |
| **H5** | `QP2608-Q8(b)` ↔ March 2010 | **HIGH** | **NONE** | **HIGH** ↑ | recurrence upheld, **date rejected** |

Arrows are movement since Phase 1.

**Not one date claim was supported. Every recurrence claim was.** That is the
cleanest possible vindication of keeping the two confidences apart — a single
`confidence` field would have had to average these into something false.

---

## H1 — `QP2608-Q1(a)`, lay-up reactivation, claimed June 2010

**Recurrence: HIGH.** `BANK-015` is the stem, word for word, containment
1.00 / 1.00. Upgraded from Phase 1's `MEDIUM` — the evidence is now the
Directorate's own publication instead of an unpreserved third-party upload.

**Date: NONE.** The bank is undated. Phase 1's alternative July 2012 evidence rests
on `SRC-SCRIBD-106245627`, now marked `UNVERIFIABLE_FROM_REPOSITORY`. There is no
proven earlier sitting **at all** — not June 2010, not July 2012.

**Adjudication.** The recurrence is among the best-evidenced in the corpus and the
date is among the worst. `FAMILY-EM-0001`, `TEXT_VERIFIED`, blocked from
`DATE_VERIFIED` by check `C21`. Temporal Delta pilot D.

---

## H2 / H3 — `QP2608-Q2`, dry dock, claimed December 2011 and October 2012

**Recurrence: HIGH, and materially wider than Phase 1 thought.** Phase 1 found the
recurrence real *at one limb*, with roughly two thirds of the 16 marks unaccounted
for. `BANK-018` carries **all three limbs** — Master coordination, preparations and
delegation to the engineers, and undocking inspections — matching the whole question
at 1.00 / 1.00.

The Phase-1 understatement is explained: the third-party excerpt carried only the
first sentence. The method was sound; the source was truncated.

**Date: NONE.** Neither December 2011 nor October 2012 has any evidence. The
July 2012 alternative is unverifiable. The bank supplies no date.

**Adjudication.** H2 and H3 are the same family (`FAMILY-EM-0002`). The recurrence
is upheld and **strengthened from `SAME_CORE_ASK` to `EXACT_REPEAT`**. Both dates
are rejected. Temporal Delta pilot B.

---

## H4 — `QP2608-Q4`, marine insurance short notes, claimed April 2010

**Phase 1: `SOURCE NOT FOUND`. Phase 2 reverses this.**

`BANK-072` reads: *“As per the Marine Insurance Act, write short notes on the
following: (a) Deviation (b) Warranties (c) War Risk Clause (d) Charterers
Contribution Clause.”* That is `QP2608-Q4` in full — all four limbs, in that order —
at containment 0.93 / 1.00.

This overturns the sharpest negative finding in Phase 1, which held that limbs (a),
(c) and (d) had *“NO ancestor anywhere in MIW's holdings”* and that (d) was
*“the least-supported limb in the whole paper”*. **All 16 marks have an official
ancestor.** `BANK-085` separately covers the warranties limb.

**Date: NONE.** April 2010 remains entirely unsupported. The bank is undated.

**Adjudication.** The largest single evidential swing in Phase 2 — and it changes
only the recurrence. `FAMILY-EM-0007` (whole question) and `FAMILY-EM-0004` (the
warranties limb across five verified sittings).

**The lesson worth keeping:** Phase 1's `SOURCE NOT FOUND` was a statement about
Phase 1's *sources*, and it was correctly recorded as such rather than as
“this question is new”. Had it been written as a finding about the question, Phase 2
would have had to overturn a published claim instead of extending a search.

---

## H5 — `QP2608-Q8(b)`, motivation, claimed March 2010

**Recurrence: HIGH, and independently proven** — four verified MIW sittings from
March 2021, plus `BANK-054` at 1.00 / 1.00. Unchanged from Phase 1, which already
had this right.

`BANK-054` adds something Phase 1 could not see: the bank item is the motivation
sentence **alone**, with no Maslow limb and with the same *“on board”* spacing
August 2026 uses. So August 2026 is not a truncation of MIW's 2021–2025 form — it is
a return to the official primitive, which MIW's earlier occurrences had *extended*.

**Date: NONE for March 2010.** Nothing supports it. MIW's evidence floor is
January 2021.

One piece of **negative** evidence is worth recording. MIW's historical intelligence
layer carries `host_recurrence_hint` values — third-party month-level assertions —
and for this family (`QP2103-Q7`, `QP2204-Q4`) they read: `2018/MAR`, `2019/MAR`,
`2019/SEP`, `2019/NOV`, `2020/JAN`. **No 2010 entry appears.** That is a
third-party assertion and proves nothing on its own; it is recorded because it
points away from March 2010 rather than towards it, and Phase 3 should not treat
March 2010 as merely untested.

**Adjudication.** Recurrence upheld at the highest confidence in the corpus, date
rejected. `FAMILY-EM-0003`. Temporal Delta pilot A, answer impact `NONE`.

---

## What the bank does and does not settle

It **settles ancestry** for H1, H2/H3, H4 and H5 — all at official-source tier.

It **settles no date whatsoever**, and it explains why the dates were always going
to be hard: if the Directorate sets papers substantially from a standing published
bank, then a question recurring across fifteen years needs no particular sitting to
explain it. The recurrence has a mundane official mechanism. The specific years in
H1–H5 were never more than recollection, and Phase 2 found nothing to convert any of
them into evidence.

**A candidate must never see a year for any of these five.**
