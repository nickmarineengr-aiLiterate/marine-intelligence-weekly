# Prototypes — dated sitting versus bank ancestor

**RESEARCH ONLY. NOTHING HERE IS PUBLISHED.** `current_as_of: 2026-08-18`

Laptop's finding on Prototype 3 was right and goes further than it first looks.
Removing the year is not enough. A block headed **ASKED BEFORE** carrying
*exact repeat* still tells a candidate there was a previous sitting. For an
official bank item with no verified date, that is a claim MIW cannot make —
the words do the leaking, not the number.

So there are two evidence classes and they need two different blocks. The
distinction is the whole point of the layer.

---

## TYPE A — verified sitting

Requires a **dated occurrence** resolving to a date-bearing source
(`C36`–`C38`). A question-bank ancestor can never satisfy this.

```
ASKED BEFORE

  This question has appeared before.
    March 2023      full question, 16 marks
    July 2023       full question, 16 marks
    February 2024   grounding and abandonment variant
    March 2025      oil spill added
    July 2025       oil spill added

  Most recent appearance: July 2025.
```

Permitted here, because each is evidenced: the month and year, the count, "most
recent", and the marks. Frequency is derived from the occurrence records, never
typed.

---

## TYPE B — official question-bank ancestor, no sitting date

The bank fixes official wording. It carries no date and proves no sitting.

```
IN THE OFFICIAL QUESTION BANK

  This question appears in the Directorate General of Shipping's own
  published Question Bank for MEO Class I, in almost the same words.

  What that means: the Directorate has set this wording as an examinable
  item.

  What it does not mean: we cannot say when, or whether, it has been set
  at a sitting.
```

Recommended heading: **IN THE OFFICIAL QUESTION BANK**. It is the plainest
true statement, and it survives a candidate reading it literally.

**Forbidden in Type B** — every one of these implies a sitting:

| Forbidden | Why |
|---|---|
| "Asked before" | asserts a prior sitting |
| any year or month | there is none |
| "asked N times", "frequency" | counts sittings |
| "due again", "overdue", "expect it" | predicts from a frequency that does not exist |
| "revival", "returns", "dormant", "not asked since" | all presuppose a timeline |
| "last seen" | asserts a sitting and a date |

The saying-nothing-about-timing is the feature.

---

## Both together

When a family has **both** a dated sitting and a bank ancestor — as
`FAMILY-EM-0009` does — show Type A and add one line of Type B beneath it. Do
not merge them into a single count. Five sittings plus one bank item is not
six of anything.

---

## Answer impact — internal enum, candidate translation

`answer_impact` stays internal. The candidate sees a consequence, never a grade.

| Internal | Candidate wording |
|---|---|
| `NONE` | *No material change — the established answer still holds.* |
| `MINOR` | *The core answer still stands. One current-law point needs updating.* |
| `MODERATE` | *Keep the structure, but important current-law content has changed.* |
| `MAJOR` | *Do not rely on an older answer without substantial updating.* |

Never show the enum, and never show a numeric similarity score. The five
similarity classes stay internal too: a candidate is told *what to do*, not
which bucket the classifier chose.

---

## Worked example — FAMILY-EM-0009, not for publication

> **Corrected in Phase 3A.1.** This example was captioned `FAMILY-EM-0008`
> while listing `FAMILY-EM-0009`'s five casualty sittings. EM-0008 is the
> unseaworthy-vessels family — ancestor BANK-160, sittings July 2023, October
> 2024, June 2025, August 2025, February 2026 — and its months are not these.
> Validator check `C44` now refuses a section that cites months its own named
> family never sat.

```
ASKED BEFORE
  March 2023 · July 2023 · February 2024 · March 2025 · July 2025
  Most recent appearance: July 2025.

IN THE OFFICIAL QUESTION BANK
  This question also appears in the Directorate's published MEO Class I
  question bank.

BEFORE YOU USE AN OLDER ANSWER
  Do not rely on an older answer without substantial updating.
  The Merchant Shipping Act, 2025 came into force on 15 March 2026 and
  replaced the 1958 Act for this topic.
```

**This must not be published**, and not because the wording is wrong. The
mapping from the 1958 Act's casualty and inquiry provisions to their 2025
counterparts has not been done, so the third block cannot yet tell a candidate
what to write *instead*. Telling someone their answer is wrong without telling
them the right one is worse than silence. See
`MERCHANT_SHIPPING_ACT_AUTHORITY.md` §5.
