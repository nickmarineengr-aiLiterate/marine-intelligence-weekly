# Candidate Study-Guide block — prototypes

**RESEARCH ONLY. NOTHING HERE IS IMPLEMENTED, AND NOTHING HERE IS PUBLISHED.**
`current_as_of: 2026-08-17`

These are drafts of what a candidate would eventually read. They are **not** wired
into `solvedQP` pages, not into any spec, and not into the Exam Plan. The Exam Plan
architecture is final and untouched.

Placement is fixed: this block lives in **STUDY GUIDE**. Exam Plan carries current
points to write and nothing else.

---

## Prototype 1 — a family that can carry a date (Pilot C)

> ### ASKED BEFORE — WHAT CHANGED FOR TODAY?
>
> **Earlier verified appearances** July 2023, October 2024, June 2025,
> August 2025, February 2026
> **Similarity** exact repeat of the question as set
>
> **WHAT STILL STANDS**
> - What makes a ship unseaworthy, and how that differs from an unsafe ship
> - The owner's obligations to the crew in respect of seaworthiness
> - The shape of the answer you have already learnt
>
> **WHAT CHANGED**
> - The **Merchant Shipping Act, 2025 (Act 24 of 2025)** came into force on
>   **15 March 2026**
> - It repeals the **Merchant Shipping Act, 1958** at section 324(1)
>
> **DO NOT WRITE TODAY**
> - Do not write that the Merchant Shipping Act, **1958 is** the operative Indian
>   statute. It was repealed on 15 March 2026.
> - Do not cite a section of the 1958 Act as current law without saying it is
>   repealed.
>
> **STATE TODAY**
> - Answer the concept as the question asks it
> - Then state that the 1958 Act stands repealed from 15 March 2026, and that the
>   2025 Act is the operative statute
> - Give the date. “The Act has been replaced” scores less than the instrument and
>   the date
>
> **ANSWER IMPACT — MODERATE**
> Most of your answer still scores. The statute it hangs from has changed.

---

## Prototype 2 — a family where nothing changed (Pilot A)

> ### ASKED BEFORE — WHAT CHANGED FOR TODAY?
>
> **Earlier verified appearances** March 2021, April 2022, December 2025
> **Similarity** exact repeat
>
> **WHAT STILL STANDS**
> - All of it. This is human-element management, not a regulated subject, and
>   nothing in the answer has moved.
>
> **WHAT CHANGED**
> - Nothing in the law or the practice.
> - **The question got smaller.** Every earlier appearance paired this with
>   *“Explain Abraham Maslow's theory of motivation”* and the pair carried
>   16 marks. Here it stands alone and carries **6**.
>
> **DO NOT WRITE TODAY**
> - *(nothing)*
>
> **STATE TODAY**
> - The same answer, written to 6 marks.
> - Do not spend the paper on Maslow. He is not asked here.
>
> **ANSWER IMPACT — NONE**

Prototype 2 matters more than it looks. A block that only ever appears when
something changed teaches candidates that its absence means “not checked”. `NONE`
must be a visible, ordinary outcome.

Note also what it does **not** say: nothing about Q8(a). Q8(a) is a different family
at 10 marks and gets its own treatment or none.

---

## Prototype 3 — a real repeat whose date cannot be shown (Pilot D)

> ### ASKED BEFORE — WHAT CHANGED FOR TODAY?
>
> **Status** This question appears in the Directorate General of Shipping's own
> published question bank for MEO Class I, in these words.
> **Similarity** exact repeat
>
> **WHAT STILL STANDS**
> - Reactivation survey and trials practice is stable. The answer you have learnt
>   still applies.
>
> **WHAT CHANGED**
> - Nothing we can demonstrate.
>
> **DO NOT WRITE TODAY**
> - *(nothing)*
>
> **STATE TODAY**
> - The current answer, unchanged.
>
> **ANSWER IMPACT — NONE IDENTIFIED**

**What Prototype 3 must never say.** There is no *“Earlier verified appearance”*
line, and no year anywhere — not “2012”, not “around 2012”, not “over a decade
ago”. The question's official pedigree is real and worth telling a candidate. Its
date is unknown, and the block simply does not have that field.

This is the prototype the Laptop should attack hardest. It is the one where a
plausible-sounding line — *“a long-standing question, last seen some years ago”* —
would be a fabrication.

---

## Design rules the prototypes encode

1. **`DO NOT WRITE TODAY` must name the obsolete thing.** *“Do not write that the
   1958 Act is operative”* is usable. *“Check the latest amendments”* is not, and is
   forbidden.
2. **No date unless `date_confidence` is HIGH.** The field is absent, not hedged.
   A hedge is still a claim.
3. **`ANSWER IMPACT` is exam consequence, not legal significance.** Prototype 2
   reads `NONE` even though the question changed shape.
4. **Source confidence is not shown to candidates.** It governs whether the block
   renders at all. Candidates get the conclusion; the evidence lives here.
5. **Never state a mark or a limb the paper does not print.**
6. **The block never restates the answer.** It qualifies it. The canonical answer
   and the Exam Plan bullets remain the only place points to write appear.

---

## Not yet decided — for the Founder

- Whether Prototype 3's shape is publishable at all. *“Official examinable item,
  date unknown”* is honest and might still read to a candidate as *“this is due to
  come round again”*, which is not a claim the evidence supports.
- Whether `ANSWER IMPACT` is shown as a word, or only implied by the content.
- Whether earlier-appearance dates are listed in full, or summarised as a count.
