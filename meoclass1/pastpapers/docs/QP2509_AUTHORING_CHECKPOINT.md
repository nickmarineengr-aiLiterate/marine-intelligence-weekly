# QP2509 — AUTHORING CHECKPOINT

> # ⚑ CLOSED — 2026-08-11. THIS CHECKPOINT HAS BEEN CONSUMED.
>
> **QP2509 is COMPLETE: 9 of 9 authored, built, toolchain `ALL STAGES PASS`.**
> See **`CURRENT_STATUS.md` §31** and the nine records at `verification/QP2509/`.
>
> The resume command in §3 below **has been executed**; Q2, Q5 and Q7 were restored mechanically
> by the applier and the applier reported them byte-identical to the spec afterwards. The
> **`staging/QP2509/` directory has been deleted** — it is obsolete and its docstring
> ("DO NOT BUILD") is now actively misleading.
>
> **Nothing below has been rewritten.** The §5 substantive findings and the §4 record of the
> authoring order remain accurate and were the input to the completing session. Only this header
> is new. Read §5 for what not to re-derive; ignore §1, §3, §7 and §8, whose "partial" state is
> superseded.

**Status at the time of writing: PARTIAL — 3 of 9 authored. `specs/QP2509.json` was UNTOUCHED
INTAKE and the three authored objects were STAGED, not applied.**

Session 2026-08-11, branch `pastpapers/qp2509-founder-review`, from `c5e85f2`.

Read with `QP2509_TEMPORAL_AND_DONOR_ANCHOR.md`, which remains correct and is the
pre-authoring input. This file records only what the authoring session did, where it
stopped and why, and exactly how to resume.

---

## 1. WHAT WAS COMPLETED

| Q | Topic | Tier | Donor | State |
|---|---|---|---|---|
| **Q2** | CII — commercial impact and shortcomings | D | `QP2508-Q2` EXACT | **READY** |
| **Q5** | HNS Convention — scope and certification | C | none | **READY** |
| **Q7** | Bunker Convention 2001 vs CLC 92 | C | none | **READY** |
| Q1 | Bauxite | C | — | not started |
| Q3 | General average | D | `QP2607-Q5` EXACT | not started |
| Q4 | Maritime lien | C | — | not started |
| Q6 | Communication | C | — | not started |
| Q8 | Human element / MLC | C | — | not started |
| Q9 | Classification societies | D | `QP2606-Q8` EXACT | not started |

All three completed objects validate at **0 errors**, carry full verification records at
`verification/QP2509/`, and were authored in the order the session prompt directed —
highest temporal risk first — with one efficiency deviation recorded in §4.

---

## 2. WHY THE SPEC IS UNTOUCHED, AND THE WORK IS STAGED

`PASTPAPER_PRODUCTION_PROTOCOL.md` §3: *"There is no valid half-authored-paper state."*

**The toolchain enforces that mechanically, and this session proved it.** `build_paper.py`
selects a paper by the **presence of answers**, not by `build_state`. With three answers and six
nulls in the spec, QP2509 entered the build pipeline and the run went red:

```
PAPER BUILD   FAIL     render_blocks on a null model_answer
UI BEHAVIOUR  FAIL
REUSE MAP     FAIL     stale derivation
HEALTH        FAIL     26 errors, QP2509 review build is NOT noindex
AUDIT         FAIL     built page not found
FAILURES PRESENT
```

A partially authored spec is therefore not merely untidy — it is a **broken build on the
branch**. Three outcomes were available and only one is correct:

- **Complete all nine.** Not reachable in this session at the corpus's standard. Each object
  runs to ~40 KB of primary-verified content plus a verification record.
- **Discard the authored work** and leave the branch as found. Throws away three verified
  answers and two full convention readings.
- **Park the objects outside the spec.** Toolchain stays green, nothing verified is lost, and
  the next session resumes with one command. **This is what was done.**

`specs/QP2509.json` was restored from `c5e85f2` and its hash confirmed **byte-identical** to the
committed intake.

---

## 3. HOW TO RESUME — ONE COMMAND

```bash
python meoclass1/pastpapers/staging/QP2509/apply_staged.py
```

Then confirm:

```bash
python tools/pastpapers/validate_spec.py meoclass1/pastpapers/specs/QP2509.json
```

Expect **0 errors, 3 warnings** (model-answer word counts, which are WARN-only and consistent
with the rest of the corpus). Then author **Q8 → Q3 → Q9 → Q4 → Q1 → Q6** and only at 9/9 run
the toolchain and build.

The applier is **idempotent** and refuses to apply if a printed stem has drifted between the
staged object and the spec. Both properties were tested this session: applied twice, second run
a no-op; spec restored to a byte-identical hash afterwards.

**Do not commit an applied spec until 9/9.** Applying it and stopping again recreates exactly
the red-build state this checkpoint exists to avoid.

---

## 4. AUTHORING ORDER — ONE DEVIATION, RECORDED

The prompt directed Q5 → Q2 → Q8 → Q3 → Q9 → Q7 → Q4 → Q1 → Q6, and allowed adjustment where
source availability made another sequence clearly more efficient. Two adjustments were taken:

- **Q2 was authored first**, not second. Its donor object had just been read into context in
  full for the donor adjudication. Authoring it immediately avoided re-reading a 400 KB spec.
- **Q7 was authored third**, not sixth. Q5 limb (c) and the whole of Q7 turn on the same
  CLC 92 / Bunkers 2001 boundary, and the anchor itself directed that the two be authored
  together. The three convention texts were read once and applied to both.

Q8, the third of the front-loaded high-risk questions, was **not reached**. It remains the
correct next question.

---

## 5. SUBSTANTIVE FINDINGS THE NEXT SESSION SHOULD NOT RE-DERIVE

**Q2 — a donor cross-reference defect, found and fixed.** `QP2508-Q2` carried the pointer
**"See Q8"** on three surfaces — `quick_revision.major_trap`, the study-guide instrument
comparison, and the regulation and source map — plus a `cross_links` entry to `QP2508.html#q8`.
QP2508's Q8 was the Net-Zero Framework question; **QP2509's Q8 is the human-element question**.
Copied verbatim, all four would have sent a candidate to an unrelated answer. All four were
rewritten to stand alone. **This defect class carries no date and is invisible to a temporal
sweep** — it must be swept for by name. Expect the same in the Q3 and Q9 donors.

**Q2 — interval arithmetic.** The donor's "four months before this examination" is correct for
August and silently wrong for September. A one-month forward pull imports no facts but breaks
every relative interval.

**Q5 — a widely repeated "exclusion" that is not in the treaty.** Secondary summaries, including
the Convention's own public-facing overview page, state that HNS does not apply to damage
covered by the Bunkers Convention. **That proposition appears nowhere in the Convention**, and a
full-text search confirms the word "bunker" does not occur in it at all. Article 4.3 contains
exactly two exclusions — CLC pollution damage, and class 7 radioactive material. Bunkers fall
outside because **article 1.5(a) covers only substances carried *as cargo***.

**Q5 — the State count was deliberately omitted**, per the session prompt and
`PASTPAPER_PRODUCTION_PROTOCOL.md` §2.1. No figure appears anywhere in the object. Treat the
later appearance of one as a regression, not an improvement.

**Q7 — the Bunkers Convention has no limitation figures at all.** Article 6 fixes none and
refers out to the LLMC 1976 as amended. No LLMC figure is quoted, because the referral itself is
the comparative point.

**Corpus gain, separate from donor gain.** Q5 and Q7 put the **first primary readings of the
2010 HNS, 1992 CLC and 2001 Bunkers texts** into the corpus. Neither creates a donor family —
Q7 is a singleton and Q5's only relative is unsolved — but the research is durable and is
available to any future pollution-liability question. A paper can produce research value and no
donors; the two are tracked separately.

---

## 6. RESEARCH ALREADY DONE FOR UNAUTHORED QUESTIONS

None beyond the anchor. Q8, Q3, Q9, Q4, Q1 and Q6 are at the state
`QP2509_TEMPORAL_AND_DONOR_ANCHOR.md` §4 and §5 left them. The anchor's **carried-forward TO
VERIFY list is still live** for items 1, 3, 4 and 6; items 2 and 5 (the HNS Protocol text, and
the Bunkers/CLC limbs) are now **discharged** by Q5 and Q7. Item 7 — whether Q7 or Q8 earns
promotion to tier B — is **answered for Q7: it does not**, and the reason is recorded in its
verification record. It remains open for Q8.

---

## 7. STATE AT CLOSE

| | |
|---|---|
| Corpus | **252 total / 90 solved / 162 unsolved** — unchanged |
| Fully solved papers | 10 — unchanged |
| `specs/QP2509.json` | untouched intake, hash-identical to `c5e85f2` |
| Toolchain | `ALL STAGES PASS`, 102 warnings — identical to the session baseline |
| `REUSE SELFTEST` | PASS |
| QP2509 built page | **does not exist, correctly** |
| New in the repository | 3 staged question objects, 3 verification records, this checkpoint |

**If the three staged objects were applied, the corpus would read 252 / 93 / 159.** It
deliberately does not, because the paper is not finished.

---

## 8. WHAT WAS NOT DONE, AND MUST NOT BE ASSUMED DONE

- Q1, Q3, Q4, Q6, Q8, Q9 — **not authored**.
- The three **mandatory paper-level sweeps** (assembled-answer, donor-contamination,
  future-contamination) were run **per question** on Q2, Q5 and Q7 and are recorded in their
  verification records. They have **not** been run across the paper, because a paper-level sweep
  of a third of a paper proves nothing.
- **No build.** No `QP2509.html`, no index entry, no sample.
- **No QA pass** — no determinism check, no positive controls beyond the toolchain self-test,
  no HTTP UI review at 1280 px and 375 px. All of that belongs to a completed paper.
- **No corpus or donor-readiness recomputation.** Nothing was solved, so nothing changed.
- **No next-paper recommendation.** The ranking depends on what QP2509 creates, and QP2509 has
  not created it yet.
- **No merge to `main`. No launch. No un-gating.**
