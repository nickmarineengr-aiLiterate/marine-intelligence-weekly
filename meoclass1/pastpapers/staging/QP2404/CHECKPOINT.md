# QP2404 AUTHORING CHECKPOINT — 4 of 9

**Status: STOPPED DELIBERATELY, NOT FAILED.** Governed by
`PASTPAPER_PRODUCTION_PROTOCOL.md` §3 — there is no valid half-authored-paper
state, so the canonical spec was **restored to intake** and the completed work
staged here.

`specs/QP2404.json` on the branch is therefore **intake, plus three adjudicated
recurrence edges and nothing else**. It carries **no answers**. The toolchain is
green in that state.

---

## What is here

| File | What it is |
|---|---|
| `QP2404.authored-4of9.json` | the spec as it stood with Q3, Q4, Q6, Q7 authored — evidence, not the resume path |
| `author_q4.py` | re-authors **Q4** from `QP2506-Q1` |
| `author_q367.py` | re-authors **Q3, Q6, Q7** and closes out Q4's verification_status |
| `apply_edges.py` | the three reverse-hint edges — **already applied and committed**; kept as the record. Re-running it asserts rather than double-applying. |
| `qpio.py` | canonical spec IO (indent=1, LF, trailing newline). Path derived from this file's location, not a drive letter. |

## How to resume

```bash
python meoclass1/pastpapers/staging/QP2404/author_q4.py
python meoclass1/pastpapers/staging/QP2404/author_q367.py
python tools/pastpapers/validate_spec.py meoclass1/pastpapers/specs/QP2404.json
```

**Verified this session**: the two scripts reproduce exactly 4 answered questions
and leave `reused_from` as `QP2509-Q4`, `QP2506-Q1`, `QP2602-Q6`, `QP2508-Q4`.
They are deterministic — they clone the donor objects and apply explicit patches,
so they re-derive rather than carry a copy.

Expect **4 errors** immediately after running: the four verification records under
`verification/QP2404/` do not exist yet. Writing them is the first task on resume.

### The one trap in this checkpoint

`author_q367.py` adapts **Q6** structurally from `QP2506-Q6` but then forces
`reused_from = QP2602-Q6`, and that line must not be "tidied up".
`QP2506-Q6` and `QP2508-Q6` join the general-average family by **exact stem
equality** on their own. `QP2602-Q6` does not — it differs by the single inserted
word *"proper"* — so the explicit edge is the only thing holding it in. Replacing
it with the structural donor drops `QP2602-Q6` out of the family and regresses an
already-built page to **"Once in this set"**. The line carries the same warning.

---

## What remains for 9/9

| Q | Topic | Tier | Work |
|---|---|---|---|
| Q1 | IoT in the maritime industry | C | full fresh research — technical/management, no instrument prescribes it |
| Q2 | Ammonia as a marine fuel | C | full fresh research — **temporal-critical, see below** |
| Q5 | AFS Convention + tin-free paints | C | full fresh research |
| Q8 | Audit vs survey; RO action on ISM certificates | C | full fresh research — **wrong-edition risk, see below** |
| Q9 | UNCLOS environment and maritime zones | C | full fresh research |

Then: 9 verification records, the four mandatory sweeps, build, QA, determinism,
HTTP UI review, surface impact, corpus recomputation.

## Research already banked — do not redo it

All of this was established from primary sources this session and is written up in
`docs/QP2404_TEMPORAL_AND_DONOR_ANCHOR.md`.

- **Q2.** At April 2024 **no IMO instrument governed ammonia as fuel.**
  `MSC.1/Circ.1687` is dated **26 February 2025** and was approved at **MSC 109,
  2–6 December 2024** — read verbatim from the circular. The draft guidelines were
  under development at CCC (principles on toxicity agreed at CCC 9, 20–29 September
  2023). The route at this sitting was **SOLAS II-1/55 alternative design** with the
  IGF Code's goal and functional requirements and class rules. Ammonia *carriage*
  under the IGC Code is a different matter — do not merge them.
- **Q8.** **`A.1188(33)`, adopted 6 December 2023, paragraph 5: "REVOKES resolution
  A.1118(30)."** Read verbatim from the resolution. So at April 2024 the operative
  edition is the **2023 Guidelines**, and A.1118(30) — which stood for six years and
  is the natural default — had been revoked four months before the sitting. Useful
  text already located: 4.4 (annual DOC verification, ±3 months of the anniversary),
  4.14.1–4.14.3 (a major non-conformity affects the validity of the DOC and related
  SMCs; corrective action normally within three months; failure to correct may itself
  be a major non-conformity). Limb (c) is carried by the ISM Code's own paragraph 13
  provisions. **Not yet located**: a single named IMO provision covering the exam's
  "extension of the SMC" and "revision of an entry" scenarios. If none exists, say so
  and attribute those to the RO's/Administration's procedures rather than inventing a
  rule — `PASTPAPER_PRODUCTION_PROTOCOL.md` §2.1.
- **Q5.** Cybutryne controls under **`MEPC.331(76)`** (adopted 17 June 2021) entered
  into force **1 January 2023** and were therefore **in force at this sitting**, with
  the revised IAFS Certificate form. An answer describing only the TBT position is
  wrong for April 2024 — this trap runs **backwards**.
- **EU instruments.** EU ETS extended to maritime **1 January 2024** — in force at the
  sitting. **FuelEU Maritime** (Reg. (EU) 2023/1805) was **adopted** September 2023 but
  applies only from **1 January 2025** — nameable as upcoming, never as applying.

## The generalisable finding

The **33rd IMO Assembly (December 2023) is a standing boundary for every 2024
sitting**, exactly as the 34th Assembly (December 2025) already is for 2025 sittings.
A.1188(33) is the first instance found. Any 2024 paper citing an Assembly-adopted
guideline should be checked against it.
