# QP2303 — MARCH 2023 — CHECKPOINT

**State:** `Intake Complete` — **0 of 9 authored.**
**Branch:** `pastpapers/qp2303-founder-review`
**Baseline:** `d6d95e8dbb51ba03fd8eaded864c79427a22cbba` (`origin/main` at session start)
**Corpus commit consumed:** `319524c24d11b2f89f33672c384b56e9ae1ab7db` — read-only, unmodified
**Written:** 2026-08-14

---

## 1. WHAT THIS SESSION COMPLETED

Everything upstream of authoring. The adjudication is done and recorded; the answer layer is not.

| Stage | State |
|---|---|
| Fetch, re-ground, machine and remote verification | **DONE** — `Dani-Desktop`, clean tree, no git operation in progress |
| Baseline decision and merge-base proof | **DONE** — anchor §0 |
| Persistence gate on QP2301 / QP2312 / QP2304 / QP2309 | **DONE** — all four intact on `origin`, 9/9, full artefact set |
| QP2303 vs QP2302 recomputation from printed truth | **DONE** — anchor §7 reasoning, summarised in §3 below |
| Source and intake gate, both pages rendered and reconciled | **DONE** — `transcription_verified` in the spec |
| Donor re-derivation across all nine questions | **DONE** — anchor §3, and §2 of every verification record |
| March-2023 temporal anchor | **DONE** — anchor §2 |
| Corpus discipline and evidence grading | **DONE** — anchor §5 |
| **Q1–Q9 authoring** | **NOT STARTED** |
| Paper HTML build | **NOT STARTED** — and must not be built until 9/9 |
| Paper QA, UI review, determinism | **NOT STARTED** |

**Why it stopped here.** A single authored question object in this corpus is roughly **52,000
characters** (`QP2309-Q2` is 52,689). Nine of them plus nine full verification records is on the
order of **470 KB of adjudicated content**. That is a whole authoring session's work in its own
right, and the protocol is explicit that there is no valid half-authored canonical spec: the spec
stays at intake until 9/9 exist. Stopping at a clean, validated, fully-recorded intake is the
governed outcome, not a failure state — and it means the next session starts with every hard
judgement already made and evidenced.

---

## 2. RESUME INSTRUCTIONS

```bash
cd D:/Marine-Intelligence-Weekly
git fetch origin --prune
git checkout pastpapers/qp2303-founder-review
git status                                   # must be clean
python tools/pastpapers/validate_spec.py meoclass1/pastpapers/specs/QP2303.json   # must be 0 errors
```

**Re-ground before authoring, do not assume:**

1. **Check whether `origin/main` has moved.** If a further 2023 paper has been integrated, apply the
   anchor §0 test again: *newly integrated paper content that changes donor truth* justifies
   rebasing this branch onto the new `main`. Nothing here is authored yet, so a rebase is currently
   free — this is the cheapest possible moment to take a newer baseline.
2. **Re-read the anchor before writing anything.**
   `meoclass1/pastpapers/docs/QP2303_TEMPORAL_AND_DONOR_ANCHOR.md`.
3. **Do not re-derive donors from scratch.** They are recorded per question in `reuse_evidence` and
   in §2 of each verification record, with rejections and their reasons. Re-check them only if the
   corpus has gained a paper.

**Then author, one question at a time**, writing each completed question object into
`meoclass1/pastpapers/staging/QP2303/Q<n>.json` — **not** into the canonical spec. When 9/9 exist:
guarded mechanical assembly into `specs/QP2303.json` → `validate_spec` → build → retire staging.

**Suggested order** — cheapest and safest first, so the hardest temporal reasoning is done once the
paper's voice is established:

> **Q9 · Q3 · Q8 · Q6 · Q5 · Q4 · Q7 · Q1 · Q2**

Q9 and Q3 are exact donors on temporally stable subjects. Q8 has a verbatim same-year donor needing
compression. Q2 is last because it carries the whole GHG-strategy reversal.

---

## 3. WHY THIS PAPER AND NOT QP2302 — recomputed this session

Both papers were re-read from their printed sources and re-scored against the **current** 288-question
corpus. Both come out at **8 of 9 with a donor**, so the frozen §4 table (which had them tied at 6/9)
no longer discriminates. Three things do:

| | **QP2303** | **QP2302** |
|---|---|---|
| Strong exact/near donors | **5** (Q3, Q8, Q9 exact; Q2, Q6 near) | **4** (Q2, Q3, Q7 exact; Q9 near) |
| Limb-level or weaker | **3** | **4** |
| Fresh (no donor anywhere) | 1 — Q5 | 1 — Q6, Bill of Lading |
| **Temporal volatility of the strong donors** | **LOW** — marine insurance, lubricating-oil analysis, IACS/RO Code. Q9 is temporally neutral outright | **HIGH** — EEXI/CII six weeks after entry into force, MLC across the 23 Dec 2024 amendment boundary, CLC/Bunker liability limits |
| Printed anomaly load | Moderate — `long tern`, `elaborate one`, unclosed quotes, `B).`, asymmetric Q4 marks | **Heaviest in the batch** — bare `4.` and `5.`, stray `f`, `.JS` for "as", `Cortra rotating`, `C02`, `0il`, `Compliant` for "Complaint", `Convention2001` |
| Same-year support | **5 questions**, incl. one **verbatim** (`QP2309-Q2`) and one **backward-running** (`QP2301-Q3`) | 4 questions |

**QP2302 has not become materially stronger.** Its same-year gains (`QP2304-Q7` for Q9,
`QP2304-Q6` for Q7) are real but its strong donors sit in the four most amendment-sensitive subjects
on the syllabus, which is precisely the wrong exposure for a February 2023 sitting. **QP2303 was
correctly preferred and the margin is wider than the stale table showed.**

---

## 4. THE ONE THING A REVIEWER MUST NOT UNDO

`meoclass1/pastpapers/specs/QP2303.json` models **Q4's subpart marks as unset**, even though limb A
prints `(8)`.

That is deliberate. The examiner printed `(8)` against limb A and **nothing at all** against limb B.
Recording a marked subpart beside an unmarked one fails the validator's arithmetic check, and the
only ways to pass it are to invent `(8)` for limb B — which the examiner did not print — or to leave
both unset and record the printed asymmetry in prose. **The second was chosen.** The printed truth is
preserved in `printed_marks`, `printed_marks_note` and `subpart_marks_note`, and in §1 of
`verification/QP2303/Q4.md`.

**Do not "fix" this by writing 8/8 into Q4's subparts.** It would silently normalise printed truth,
which is the one thing the house rule forbids.

---

## 5. OPEN ITEMS CARRIED INTO AUTHORING

| # | Item | Class |
|---|---|---|
| 1 | **`MEPC.328(76)` entry-into-force year is wrong in the corpus** — `amendment-register.json` says `2023-11-01`; the resolution's own operative paragraph 3 says **1 November 2022**. Raised as a `TRUE_SOURCE_CORRECTION_REQUEST` in anchor §2.3. **Not applied — QP production never edits True Source** | Founder / producer team |
| 2 | CLC / FUND / Supplementary Fund tier ceilings — no text held; **no SDR figure may be asserted numerically** | `B_CURRENCY_CHECK` (Q1) |
| 3 | Initial GHG Strategy `MEPC.304(72)` not held as a document; its levels graded **P2** | `C_ACCEPTED_LIMITATION` (Q2) |
| 4 | `A.1155(32)` PSC procedures **not held**; only the future 33rd-Assembly set is. Standing 2023-batch gap | `C_ACCEPTED_LIMITATION` (Q7) |
| 5 | `RQ-25` — RO Code edition and completeness unverified | `C_ACCEPTED_LIMITATION` (Q8) |
| 6 | No IACS procedural documents held; limb a graded **P3** | `C_ACCEPTED_LIMITATION` (Q8) |

---

## 6. FILES OWNED BY THIS BRANCH

```
meoclass1/pastpapers/specs/QP2303.json
meoclass1/pastpapers/docs/QP2303_TEMPORAL_AND_DONOR_ANCHOR.md
meoclass1/pastpapers/verification/QP2303/Q1.md … Q9.md
meoclass1/pastpapers/staging/QP2303/CHECKPOINT.md
```

**No global derived artefact is committed** — no reuse map, manifest, index, year sheet, topic sheet
or `solvedQP/` page. **No `QP2303.html`**, because the paper is not solved and a review build of an
unsolved paper would misreport coverage. **No source PDF.**
