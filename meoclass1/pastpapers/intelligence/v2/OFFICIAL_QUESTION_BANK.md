# The official DG Shipping question bank

**RESEARCH ONLY.** `current_as_of: 2026-08-17`

This is the central finding of Phase 2, and it changes what the recurrence layer
rests on.

---

## What was found

The Directorate General of Shipping publishes its own **`Question Bank MEO CL-I`**
— a 185-item compilation of Engineering Management questions, in the Directorate's
own wording, on the Directorate's own domain.

Phase 1 identified this document as the highest-value unexploited source and could
not reach it: `ECONNREFUSED 164.100.60.201:443`. That block **persists** — in Phase 2
the whole `dgshipping.gov.in` domain refused connections from the shell, from `curl`
and from the harness fetch path, including a beta host (`betadgs.dgshipping.gov.in`)
that Phase 1 did not know about.

The document was obtained instead from the **Internet Archive**, which holds a
snapshot of the official PDF taken 10 January 2026.

| | |
|---|---|
| Source id | `SRC-DGS-QBANK-ARCHIVED` |
| Artefact | `%PDF-1.7`, 314,710 bytes |
| sha256 | `0E0D6BC7A7B738335687B57D6F33364D728D2DAD99BC22ED0E2A5D371438CB51` |
| Preservation | `PRESERVED_RAW` in the raw intake directory |
| Extraction | 185 of 185 items, verified by contiguous numbering 1–185 with no gaps |
| Extraction repair | Item 182 was scrambled in Phase 2. Body lines were ordered by `(page, -y)` alone, so three fragments sharing baseline `y=145.5` on page 16 kept pdfminer's container order rather than reading left to right. `x0` is now part of the sort key; re-extraction changes item 182 and nothing else. |
| Source defect preserved | Item 181 letters its limbs `a, b, d, c`. That is the Directorate's own mislettering, printed in that order, and is kept verbatim. |
| Access | No paywall, no login, no restriction. A public archive of a public official document. |

One retrieval detail matters for reproducibility: the plain Wayback URL returns the
archive's HTML toolbar wrapper, and only the raw `id_` variant returns the genuine
PDF. Phase 2 initially downloaded 12,882 bytes of `<!DOCTYPE html>` and had to
notice.

---

## Why this outranks everything Phase 1 had

Phase 1's recurrence findings rested on `SRC-SCRIBD-106245627` — a third-party user
upload whose full text was never preserved. The bank replaces it **at a strictly
higher provenance tier**: this is the examining authority's own published wording,
not somebody's scan of a paper.

It also fixes a Phase-1 error that the weaker source had caused. The Scribd excerpt
carried only the *first sentence* of the dry dock question, so Phase 1 concluded
that two thirds of `QP2608-Q2` had no ancestor. `BANK-018` carries all three limbs.

---

## What it proves, and what it does not

This is the distinction the whole layer turns on.

**It proves ancestry.** A question in the bank is an official examinable item with
fixed official wording. When a sitting paper reproduces it, that is recurrence, and
the evidence is first-rate.

**It proves no dates at all.** The bank is undated throughout. Exactly one item
(`BANK-3`, the dry-docking welding-fire question) carries an inline `(Oct-05)`,
at the very end of its text. Phase 2's prose attached that annotation to
`BANK-4`; the extractor had it right and only the write-up was wrong. Check
`C33` now reads the annotation back out of the extracted bank, so the claim is
derived rather than remembered. The DGS upload prefix dates *publication*
to 12 February 2018, and item `BANK-144` cites the Manila amendments of 25 June
2010 — so the **document** sits between 2010 and February 2018. That bounds the
document. It dates **no sitting**.

So the bank moves `source_confidence` to HIGH and `text_similarity_confidence` to
HIGH while leaving `date_confidence` exactly where it was: **NONE**. That is the
clearest possible demonstration of why Phase 1 was right to keep the three apart.

Bank items are therefore stored in `OFFICIAL_BANK_ITEMS.json`, **not** in
`QUESTION_OCCURRENCES.jsonl`, and validator check `C28` enforces the separation. If
a bank item were recorded as an occurrence it would inflate `frequency_known`, which
counts sittings and nothing else.

---

## How much of the corpus comes from it

Sweeping all 185 items against all 40 solved papers (360 questions):

- **63 strong matches** across **21 of 40 papers**
- `QP2608` has the most of any paper: **7**
- The most-reused items are `BANK-097` (entry into force of an IMO convention),
  `BANK-160` (unseaworthy vessels under the MS Act 1958), `BANK-162` (casualty
  investigation) and `BANK-048` (P&I clubs) — each appearing across four or more
  sittings

An independently recovered **official sitting paper from 2005**
(`SRC-DGS-2005-MGMT`) prints the same rubric QP2608 prints twenty-one years later —
*Answer SIX Questions only*, *All Questions carry equal marks*, *Total Marks 100* —
and its questions also map onto bank items.

The reasonable reading is that the Directorate sets Engineering Management papers
substantially by drawing on its own standing bank, and sometimes extends an item
with a scenario. That is a **description of the evidence**, not a proven mechanism,
and it is not the basis of any candidate-facing claim.

---

## Consequence for the setter hypothesis

It supplies a mundane, officially documented explanation for the long-run recurrence
that the NTA rumour was invoked to explain. That **strengthens** the existing
`NO OFFICIAL EVIDENCE FOUND` verdict without being causal evidence for anything.
Recurrence is still not proof of who sets the paper. See `SETTER_HYPOTHESIS.md`.

---

## What is stored where

Only the seven items actually cited as ancestors are reproduced in
`OFFICIAL_BANK_ITEMS.json`. The full 185-item extract lives in the raw intake
directory outside git and is reproducible from the preserved PDF via
`tools/parse_dgs_question_bank.py`; the sha256 above pins the artefact the tool was
run against.

**Recommendation for the Laptop:** the PDF is an official public document and is
load-bearing for the whole layer. It currently exists in exactly one place, on one
machine, outside version control. Canonical storage should be decided.
