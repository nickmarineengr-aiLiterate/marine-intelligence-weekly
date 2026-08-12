# QP2507 — SESSION CHECKPOINT

**Paper:** QP2507 · JULY 2025 · Sr. No. `EM – 2507`
**Branch:** `pastpapers/qp2507-founder-review`, branched from `333e814`
**Corpus commit consumed:** `319524c24d11b2f89f33672c384b56e9ae1ab7db`
**Checkpoint written:** 2026-08-13

---

## 1. STATE — READ THIS FIRST

> # QP2507 IS **NOT** SOLVED. 0 / 9 ANSWERS AUTHORED.
>
> **`specs/QP2507.json` is UNTOUCHED and remains in its `Intake Complete` / answerless state.**
> That is correct and deliberate: `DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §12 forbids a
> half-authored canonical spec. Nothing was partially promoted.

This session completed the **whole pre-authoring gate** and stopped at the boundary between
adjudication and authoring. What it produced is the foundation all nine answers rest on, not any
of the answers.

**Batch 2 remains 4 / 6.** QP2507 is IN PRODUCTION, not READY.

---

## 2. WHAT IS COMPLETE — and may be relied on without redoing it

| Item | State | Where |
|---|---|---|
| Persistence gate (Batch 1 ×6, Batch 2 ×4 on `origin`) | **PASS** | handover |
| Governed baseline `333e814` verified canonical | **PASS** | handover |
| Machine preflight | **PASS** | handover |
| **Source gate** — PDF identity, 3/3 pages read back visually | **PASS** | §3 |
| **Intake reconciliation** — all 9 stems, limbs, marks, anomalies | **PASS, 0 corrections** | §3 |
| **Donor re-derivation** — 8/9 tier D, both stems read on all 8 pairs | **COMPLETE** | anchor §7 |
| **Donor direction analysis** — all 8 backward, 0 refusals | **COMPLETE** | anchor §7.3 |
| **Temporal anchor for July 2025** | **COMPLETE** | `docs/QP2507_TEMPORAL_AND_DONOR_ANCHOR.md` |
| **Corpus gap analysis** — 5 of 9 centrally gapped | **COMPLETE** | anchor §4 |
| **New `TRUE_SOURCE_CORRECTION_REQUEST`** (MEPC.376(80) revoked) | **RAISED, corpus not modified** | anchor §4.1 |
| Q1–Q9 answers | **NOT STARTED** | — |
| Verification records `verification/QP2507/` | **NOT STARTED** | — |
| Build, validation, sweeps, determinism, UI | **NOT STARTED** | — |

**Read `docs/QP2507_TEMPORAL_AND_DONOR_ANCHOR.md` in full before authoring.** It is the governing
document for every one of the nine questions and it was written before any donor was adapted.

---

## 3. SOURCE TRUTH — verified, do not re-verify

| | |
|---|---|
| Source copy | `meoclass1/pastpapers/docs/JULY 2025.pdf` (git-ignored, local only) |
| SHA-256 | `182c86484d3830620a86979e24d682292fd1631502a513bc788d79d730515163` |
| MD5 | `b38de69be0c5ed7da7c047a3c4c496f6` |
| Size / pages | 225,320 bytes · **3 pages** |
| Printed serial | **`Sr. No. EM – 2507`** (en dash on the source; spec normalises to `EM - 2507`) |
| Printed sitting | **`JULY 2025`** · `(India 2025)` |
| Time / marks | 3 hours · **`Total Marks – 100`** |
| Read-back | **3 of 3 pages** rendered at 150 dpi and read against the text layer. **No discrepancy.** This closes the residual risk the intake spec declared at `transcription_verified.residual_risk` (it recorded 2 of 3) |

**Marks anomaly — confirmed present and reproduced, not corrected.** Every question is 16 marks;
six answered questions total **96** against the printed **100**. The intake `marks_note` states
this correctly.

**Printed anomalies confirmed and preserved:** `Charter's Liability Insurance` (for *Charterer's*);
`a ship is classes by two classification societies` (for *classed*); `the international Maritime
Organization` (lower-case *international*); mixed limb markers `(a)` with `b) c) d)` in Q3;
`Q4.a)` set without a space; the host `- - PROVIOUSLY ASKED - - -` editorial block under Q9.

**Intake reconciliation result: ZERO transcription corrections required.** Every stem, limb ref,
mark value and anomaly note in `specs/QP2507.json` matches the printed source.

**Not a reprint.** Five questions come from March 2025 and three from January 2025, but the order
is permuted (Mar Q1→Jul Q8, Q2→Q7, Q3→Q6), Q3 is fresh and Q9 is materially reworded. A reprint
preserves order. Chronology is fixed and correct.

---

## 4. THE NINE QUESTIONS — donor, tier, and what each still needs

Derived from a simulated built set of **24 papers / 216 built answers**, assembled from Git objects.
`derive_reuse_tier` recomputed; frozen intake `reuse_tier` **not** consulted.

| Q | Topic | Tier | Donor | Stem | Direction | Corpus | What it needs |
|---|---|---|---|---|---|---|---|
| **Q1** | Nairobi Wreck Removal Convention | **D** | `QP2501-Q1` | NEAR | ←6 mo | **GAP** (citation-only) | WRC text at P1/P2; India accession date **VERIFY** |
| **Q2** | LCA of fuels; WtW / WtT | **D** | `QP2501-Q7` | **EXACT** | ←6 mo | **P1 this session** | Author on **MEPC.391(81)**; MEPC.376(80) is **REVOKED** |
| **Q3** | Charter parties; charterer's liability | **C** | *none* | *single* | — | **GAP** | **FULL FRESH RESEARCH** — the only one |
| **Q4** | Liquefaction of solid bulk cargo | **D** | `QP2501-Q9` | **EXACT** | ←6 mo | partial | IMSBC **07-23** identity at P2 (not held) |
| **Q5** | Perils of the sea; due diligence | **D** | `QP2503-Q5` | **EXACT** | ←4 mo | **GAP** | Marine Insurance Act 1963 at primary source |
| **Q6** | Gender equality in maritime | **D** | `QP2503-Q3` | **EXACT** | ←4 mo | **GAP** (nothing held) | IMO + Indian initiatives, P2/P3, honestly classed |
| **Q7** | Substantial corrosion; renewal survey | **D** | `QP2503-Q2` | **EXACT** | ←4 mo | **P1** A.1049(27) | re-anchor sitting-relative prose only |
| **Q8** | Classification; dual class | **D** | `QP2503-Q1` | **EXACT** | ←4 mo | **P1** RO Code | re-anchor sitting-relative prose only |
| **Q9** | Collision — coastal State action | **D** | `QP2503-Q9` | **NEAR** | ←4 mo | **GAP + TRAP** | **MS Act 1958**; re-point to coastal State; 8-surface sweep |

**Derived tier D: 8 / 9 — exactly as the board predicted.**
**Family reach: 0, not the predicted 8** — see anchor §7.1; this is the second consecutive paper
where the board's reach arithmetic double-counted. Reported as a workflow finding.

---

## 5. THE THREE THINGS THAT WILL BREAK THIS PAPER IF FORGOTTEN

1. **Q9 — the corpus holds the WRONG Merchant Shipping Act.** There is no MS Act **1958** anywhere
   in the corpus; it holds the **2025** Act, and its own instrument log instructs that 1958 section
   numbers "must be re-based to the 2025 Act". That instruction is correct for the July 2026 orals
   and **wrong for this sitting**, which predates even the 2025 Act's assent (18 August 2025).
   Author on the 1958 Act from official primary source. Sweep all **eight** surface classes.
   → anchor §5.

2. **Q2 — the corpus holds a REVOKED instrument as current.** `MEPC.376(80)` was **revoked** by
   `MEPC.391(81)` ¶5 on 22 March 2024. The corpus holds the revoked one and its log marks it
   `GUIDANCE` with no supersession note. MEPC.391(81) **was read at source this session** (SHA-256
   `f7601f21ad7a52404eff7cfc1d2c4a07d4ae03356be1ab57a26a4f23f0634c5f`), so Q2 may carry it at
   **P1** — an upgrade on the donor, which carried it at P2 marked "NOT read".
   → anchor §4.1.

3. **Q9 is a NARROWING, not a rewording.** July confines the demand to **the coastal State**;
   March was open and is satisfied by flag-State machinery. Reusing March's answer unchanged
   answers a question that was not asked. → anchor §7.4.

---

## 6. EXACT RESUME INSTRUCTIONS

```bash
cd D:\Marine-Intelligence-Weekly
git -c safe.directory=* fetch origin --prune
git -c safe.directory=* checkout pastpapers/qp2507-founder-review
git -c safe.directory=* status            # must be clean
git -c safe.directory=* log --oneline -1  # the checkpoint commit
```

Then, in order:

1. Read `docs/QP2507_TEMPORAL_AND_DONOR_ANCHOR.md` **in full**. Do not re-derive it.
2. Read this checkpoint. **Do not re-run the source gate or the donor re-derivation** — both are
   complete and recorded above with their evidence.
3. Author questions into `staging/QP2507/Q<n>.json`, **one at a time**, in the order
   **Q2 → Q7 → Q8 → Q4 → Q5 → Q6 → Q1 → Q9 → Q3**.

   *Rationale for that order:* Q2 first because its P1 evidence is freshest and its corpus finding
   is this session's; Q7/Q8 next because they are P1-backed EXACT donors and cheapest; Q4/Q5/Q6
   next; **Q1 and Q9 late** because they are the gapped, highest-research pair; **Q3 last** because
   it is the only question with no donor at all and needs the largest uninterrupted block.

4. Write `verification/QP2507/Q<n>.md` **with** each question, never batched afterwards.
5. When 9/9 exist: guarded mechanical assembly into `specs/QP2507.json`, then validate, build,
   sweep, determinism, UI — per `QA_AND_HANDOVER_PROTOCOL.md`.
6. **Retire `staging/QP2507/`** once the canonical spec carries all nine.

### Donor specs are on sibling branches, not on this baseline

`QP2501` and `QP2503` are solved **only on their own review branches**. Read them read-only from
Git objects — **never check them into this branch**:

```bash
git -c safe.directory=* show \
  refs/remotes/origin/pastpapers/qp2501-founder-review:meoclass1/pastpapers/specs/QP2501.json
git -c safe.directory=* show \
  refs/remotes/origin/pastpapers/qp2503-founder-review:meoclass1/pastpapers/specs/QP2503.json
```

---

## 7. PAPER-OWNED FILES COMMITTED BY THIS SESSION

Only these. No global derived artefact was regenerated or committed; the canonical spec was not
touched.

```
meoclass1/pastpapers/docs/QP2507_TEMPORAL_AND_DONOR_ANCHOR.md
meoclass1/pastpapers/staging/QP2507/CHECKPOINT.md
```

---

## 8. STANDING PROHIBITIONS CARRIED FORWARD

- Do not merge to `main`. Do not integrate any Batch-1 or Batch-2 branch.
- Do not regenerate and commit global product state.
- Do not edit the frozen True Source corpus. Both correction requests stay **raised, not fixed**.
- Do not resolve the MEPC.328(76) request; it is referenced at anchor §6 and left open.
- Do not start Batch 2 paper #6 (**QP2406**) until QP2507 is 9/9 and pushed.
