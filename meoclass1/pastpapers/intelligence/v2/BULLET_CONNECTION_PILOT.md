# Bullet connection pilot — how temporal intelligence would reach Exam Plan

**RESEARCH ONLY. NO UI IMPLEMENTED. NO CANDIDATE-FACING FILE TOUCHED.**
`current_as_of: 2026-08-17`

Laptop is piloting "BULLET ANSWER — POINTS TO WRITE" on QP2608. This file shows,
for two confirmed families, how the temporal layer would attach — so Laptop can
decide where it belongs. It changes nothing.

The chain is:

```
OLD REPEAT DETECTED → CURRENT ANSWER DELTA → BULLET POINTS TO WRITE TODAY
```

**The bullet layer must always represent the CURRENT answer.** Bullets are never
generated from the historical question. The temporal layer's only job is to
decorate current bullets with warnings and, where a delta adds a requirement, to
flag that a bullet is **missing**.

---

## Pilot 1 — QP2608-Q2 (dry dock) · FAMILY-EM-0002 · impact MODERATE

**Old question (July 2012):** coordination and information exchange with the
Master for entry to dry dock.

**Current route headings** (from the authored spec, unmodified):

1. The exchange with the Master, and the information the dock requires
2. Condition of the ship for docking — draught, trim, stability and tanks
3. Preparing the machinery and services for shutdown
4. Delegation of responsibilities to the engineers
5. *(undocking steps follow)*

**Mapping to the recurrence**

| Route step | Historical ancestor? |
|---|---|
| 1 | **yes — this is the July 2012 question, near-verbatim** |
| 2, 3 | partial — implied by the old question, not asked |
| 4, 5 | **no ancestor** — new in August 2026 |

**Current bullet points, as authored** (step 1, unchanged):
- give: docking plan, shell expansion, docking draughts and trim, tank plan, work list, defects and Conditions of Class
- take: dock date and tide window, dock entry conditions, passage ballast and trim, cargo and slop position, crew arrangements
- settle jointly: the stability condition on entry

**Temporal warnings the layer would attach**

> ⚠ **Asked before — July 2012, near-verbatim, but only this first limb.**
> Steps 4 and 5 (delegation, undocking) are new. Do not budget your time from
> the old question: roughly two thirds of the 16 marks have no 2012 ancestor.

> ⚠ **Two compliance points post-date the old answer.** Antifouling now carries
> **two** controls in force — organotins **and cybutryne from 1 January 2023**.
> Ballast operations sit under the **BWM Convention 2004, in force 8 September
> 2017**. A candidate writing a 2012-shaped answer omits both.

**A bullet the temporal layer says is MISSING**

The authored answer for Q2 contains **no** mention of antifouling, AFS or
cybutryne (verified: zero occurrences of `antifoul`, `AFS`, `cybutryne`,
`biofoul` in the Q2 object). A dry dock is where antifouling is applied and where
the AFS documentation is renewed. This is recorded as a correction candidate in
`WATCH_REGISTER.md` — **not patched here.**

This is the clearest demonstration of the layer's value: it did not merely
annotate the answer, it **found a gap in it**.

---

## Pilot 2 — QP2608-Q8(b) (motivation) · FAMILY-EM-0003 · impact NONE

**Old question:** the identical sentence, set March 2021, April 2022 and
December 2025 — every time preceded by "Explain Abraham Maslow's theory of
motivation" and carrying 16 marks.

**Current route headings for Q8** (authored spec, unmodified) — note that all of
steps 1–4 serve limb **(a)**:

1. What I establish before I hold the meeting
2. The initial meeting — what is said, and how
3. The flow of information after the meeting
4. Examples of the repeated failures such a ship carries
5. *(limb (b) — the motivation limb)*

**Temporal warnings the layer would attach**

> ✓ **Nothing in this answer has dated.** The December 2025 answer transfers
> intact. No law, limit or terminology has moved.

> ⚠ **But the question moved.** The Maslow limb is **gone** and the marks fall
> **16 → 6**. Do not open with Maslow — it is not asked.

> ⚠ **The repeat is 6 marks of 16.** Limb (a) — PSC failures, multinational
> crew, shore instructions — is **not** a repeat and carries 10 marks. That is
> where the time goes.

---

## What this pilot suggests about placement

Two different signals are in play and they behave differently:

- **"What changed in the law"** is reference material. It is read once, it is
  stable, and it belongs in **Study Guide**.
- **"This limb is a repeat but it is only 6 of 16 marks"** is a time-allocation
  instruction. It is read while planning the answer, and it belongs in the
  **Exam Plan**, beside the bullets it governs.

**Recommendation:** do not build a new learning tab. Put the temporal delta in
**Study Guide**, and put the limb/marks warning inline in **Exam Plan**. A single
combined "ASKED BEFORE" block would force one of the two signals into the wrong
place. Laptop should assess this independently.

**Hard rule carried forward:** never render "bullet points from 2010". Bullets
are current-answer only; history is decoration on top of them, never a source
for them.
