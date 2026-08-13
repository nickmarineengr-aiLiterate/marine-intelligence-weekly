# QP2407 — STAGING CHECKPOINT

Written under `DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §12. **There is no valid half-authored
state in a canonical spec**, so `specs/QP2407.json` remains in its **intake** state at 0/9
and every gate cleared so far is recorded here instead.

| | |
|---|---|
| **Paper** | QP2407 — July 2024 — `Sr. No. EM – 2407` |
| **Branch** | `pastpapers/qp2407-founder-review` |
| **Branched from** | **`e5843b1104592ac54bcaba822eab15ac4530cc23`** — the Batch 3 baseline |
| **Canonical spec state** | **`Intake Complete`, 0/9 built — deliberately untouched** |
| **Questions verified into staging** | **0 of 9** |
| **Corpus consumed** | `RulesApp-Local-Input` @ `319524c24d11b2f89f33672c384b56e9ae1ab7db` |

---

## 1. GATES CLEARED — do not repeat these

### 1.1 Preservation gate — PASSED

All twelve Batch 1 and Batch 2 review branches were proven **from remote git objects**, not
from the working tree: branch reachable on `origin`, solved JSON, review HTML, temporal and
donor anchor, `Q1.md`–`Q9.md`, 9/9 questions carrying a model answer, and local ref equal to
remote ref. Matrix in the session handover.

### 1.2 Batch 3 baseline — ESTABLISHED

`e5843b1` on `main` — *"Record QP2406 as live, close Batch 2 at 6/6, and correct the remote's
state"*. Batch 1's `9c97359` and Batch 2's `333e814` are both stale for this batch: `main` has
since absorbed all twelve reviewed papers and the delivery manifest. Recorded on
`pastpapers/batch3-baseline`, whose parent **is** the baseline — the same self-verifying
pattern Batch 1 and Batch 2 used.

Branch point proved before authoring: `HEAD == e5843b1 == merge-base(HEAD, origin/main)`,
0 commits ahead.

### 1.3 Source gate — PASSED, ZERO CORRECTIONS

| | |
|---|---|
| File | `meoclass1/pastpapers/docs/JULY 2024.pdf` — **present** |
| SHA-256 | `0a8b30bf7b151825de9894ce1b93caf3967b682fd8d463dbf948e10a2b3ceefb` |
| Size / pages | 222,344 bytes / **2 pages** |
| Printed serial | **`Sr. No. EM – 2407`** — matches |
| Questions | **Q1–Q9 present** |
| Marks | 16 each; every subpart split reconciles to its question total |
| Verbatim | **9/9 `text_verbatim` stems reconcile to the printed page**, after dehyphenating line breaks only |

**Printed anomalies, preserved as printed — do not normalise:**

1. **Q1** prints its limbs as `a.` `b.` `c.` with **no per-limb marks**; a single `(16)` sits
   at the end of limb c. The intake correctly carries `marks: null` on all three.
2. **Q7** prints its limbs as capital **`A)` `B)`**, unlike every other limbed question on the
   paper.
3. **Q9** prints its limbs as **`A.` `B.` `C.` `D.`**.
4. **Q1** carries a **character-encoding artefact in the source text layer** at
   *"sustainable development�s goals"*. The intake preserves it. It is an extraction artefact
   of the third-party copy, not an examiner error, and it must not be silently repaired in
   `text_verbatim`.
5. The copy is a **third-party host scan** (`source_authority: unverified`). Its recurrence
   annotations are host metadata and must never reach a candidate-facing surface.

### 1.4 Donor and temporal derivation — COMPLETE

Full record in [`docs/QP2407_TEMPORAL_AND_DONOR_ANCHOR.md`](../../docs/QP2407_TEMPORAL_AND_DONOR_ANCHOR.md).
Recomputed against the actual built set at the baseline — **234/252 built, 26 solved
papers** — never read from the frozen `reuse_tier` field.

- **1 tier D: `QP2407-Q3` ← `QP2402-Q1`**, byte-identical stem, nil question delta, nil marks
  delta, and — uniquely for a 2024 paper — the donor **pre-dates** the sitting.
- `QP2502-Q1` rejected as an equally exact but **later** alternate.
- Eight questions are fresh research. `QP2409-Q3` (0.56) and `QP2410-Q3` (0.68) were read and
  rejected as topical and related-but-different respectively.
- **Mid-2024 boundary found and verified at source: SOLAS `MSC.521(106)` in force
  1 July 2024.** June sits before it; July and August sit after it.
- Decisive exclusions: **Q4** must stop at `MEPC.377(80)` (2023) and exclude MEPC 82, MEPC 83,
  the Net-Zero Framework and the GFI; **Q6** must use MLC 2006 as amended through **2018**,
  because the 2022 amendments enter into force 23 December 2024.

### 1.5 Source grades established by test

Each corpus file was tested for an extractable text layer rather than assumed to have one.
**P1 quotation-ready and confirmed:** SOLAS Consolidated Edition 2024 (all three parts),
`MEPC.377(80)`, `A.1049(27)` ESP Code, `MSC.255(84)` Casualty Investigation Code, `mlc-2006`,
`MARPOL_Annex_VI_highlighted`. **Image-only, evidence-only, NOT quotable:** the Annex VI /
NOx Technical Code 5th edition scan, `RO_code.pdf`, STCW 2017, Load Lines 2021, MARPOL
consolidated 2022.

---

## 2. RESUME INSTRUCTIONS

Resume **on this branch**. Do not re-branch and do not re-run §1.

1. Re-read the anchor. It is the authority for the July 2024 line; do not re-derive it.
2. Author Q1–Q9 into `staging/QP2407/Q#.json` — **verified question objects only, outside the
   canonical spec** — using the frozen five-part model (`Understand → Exam Plan → Answer →
   Study Guide → Recall`) and one question-specific `answer_route` from which the map, recall,
   flashcards and cheat sheet all derive.
3. Write `verification/QP2407/Q#.md` as each question completes, discharging anchor §7.
4. At 9/9: guarded mechanical assembly into `specs/QP2407.json`, asserting every frozen intake
   field byte-identical and failing closed if that equality breaks; then `validate_spec`,
   `audit_paper`, `known_traps_check`, `temporal_sweep` with a seeded positive control,
   deterministic double build for byte identity, HTTP UI review at 1280 and 375, leakage
   checks; then retire this staging directory.
5. Regenerate global derived artefacts **only to validate**, then **revert them before
   staging the commit**. Commit paper-owned paths only, named explicitly. Never `git add -A`.

**Suggested authoring order** — establish the instrument line once, then spend it:

> **Q3** (donor, exact, cheapest) → **Q5** (SOLAS XI-1, P1) → **Q6** (MLC, P1) →
> **Q4** (GHG, P1, highest temporal risk) → **Q9** (Annex VI reg 13) → **Q1** → **Q2** →
> **Q7** → **Q8**

Q3, Q5 and Q6 share the SOLAS / instrument-hierarchy line and Q4 and Q9 share the MARPOL
Annex VI line, so each line is read once and re-anchored rather than rebuilt.

## 3. WHAT THIS BRANCH HAS COMMITTED SO FAR

- `meoclass1/pastpapers/docs/QP2407_TEMPORAL_AND_DONOR_ANCHOR.md`
- `meoclass1/pastpapers/staging/QP2407/CHECKPOINT.md` (this file)

**No global derived artefact has been touched.** `specs/QP2407.json` is unmodified from the
baseline and still reports `Intake Complete` at 0/9, which is the correct and required state
until all nine questions exist.
