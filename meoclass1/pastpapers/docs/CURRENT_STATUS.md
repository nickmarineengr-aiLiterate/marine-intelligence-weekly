# CURRENT STATUS — MEO Class I Written Questions

**Canonical restart document for the Past Written Papers product. State only.**
Last updated: 2026-08-11, after the state/history split.

This file answers four questions and nothing else: *where are we now, what was completed,
what is next, what is blocked.*

- **Policy** lives in the governed protocol files — start at [`PRODUCTION_PROTOCOL_INDEX.md`](PRODUCTION_PROTOCOL_INDEX.md).
  Where this file appears to restate a rule, the protocol file wins.
- **History** lives in [`history/SESSION_HISTORY.md`](history/SESSION_HISTORY.md) — every session
  narrative, checkpoint and superseded snapshot, verbatim. Read it only when you need the record
  of how a decision arose.
- **Workflow lessons** live in [`WORKFLOW_LESSONS.md`](WORKFLOW_LESSONS.md) — targeted reads by
  category, never the whole file.

---

## 1. Repository / branch state

| | |
|---|---|
| Path | `F:\Marine-Intelligence-Weekly` |
| Remote | `https://github.com/nickmarineengr-aiLiterate/marine-intelligence-weekly.git` |
| **Visibility** | **PUBLIC** — anything committed here is published, on any branch, `noindex` or not |
| `main` | `0766d00` — nothing from the pastpapers line has been merged into it |
| Content head | `a5f2551` on `pastpapers/qp2509-founder-review` — the newest solved-paper state |
| Tooling head | `850bdde` on `workflow/pil-v1` — content head plus the Production Intelligence Layer |
| This branch | `pastpapers/qp2404-founder-review`, cut from `c612a02` — QP2404 reverse-hint adjudication; authoring **stopped at 4/9 and staged** |

All git commands in this repository need `-c safe.directory=*`.

---

## 2. Corpus state

Derived from `health_check.py` and `build_reuse_map.py --check` at `850bdde`, not carried forward
from a previous handover.

| | |
|---|---|
| **Corpus** | **252 questions / 99 solved / 153 unsolved** |
| **Papers** | 28 — **11 solved**, 17 answerless intake |
| **Years** | 2024 (11 papers), 2025 (11), 2026 (6). May is absent from the source set in all three years |
| **Tier D (derived)** | **22** of the 153 unsolved carry a verified donor — was 20; `QP2404-Q4` and `QP2409-Q9` were unlocked by one adjudicated reverse-hint edge to `QP2506-Q1` |
| **Toolchain** | ALL STAGES PASS · `health_check.py` **0 errors, 0 warnings** · reuse map current |

---

## 3. Latest completed papers

| Paper | Sitting | State | Branch |
|---|---|---|---|
| **QP2509** | September 2025 | **COMPLETE 9/9 — newest. Founder review.** | `pastpapers/qp2509-founder-review` @ `a5f2551` |
| QP2506 | June 2025 | complete 9/9 | `pastpapers/qp2506-founder-review` @ `0d7f872` |
| QP2510 | October 2025 | complete 9/9 | `pastpapers/qp2510-founder-review` @ `8fa4f5f` |
| QP2508 | August 2025 | complete 9/9 | `pastpapers/qp2508-founder-review` @ `dedce2c` |
| QP2403 | March 2024 | complete 9/9 | `pastpapers/qp2403-founder-review` @ `e7d8bc0` |
| QP2601–QP2604, QP2606, QP2607 | 2026 set | complete, 6 of 6 available sittings | one review branch each |

Full solved set: QP2403 · QP2506 · QP2508 · QP2509 · QP2510 · QP2601 · QP2602 · QP2603 ·
QP2604 · QP2606 · QP2607.

---

## 4. Current architecture

Settled. Do not redesign without test evidence of a defect — see §7 below and the stop conditions.

| Concern | Where it lives |
|---|---|
| Source of truth | `meoclass1/pastpapers/specs/QP####.json` — everything else is generated |
| Generated product | `QP####.html`, `index.html`, `questions-####.html`, `topics-####.html`, `pastpapers_content_index.json` |
| Learning layer | `answer_route` is the spine; map, recall, flashcards and cheat sheet all derive from it |
| Template | `MIW WRITTEN QUESTIONS — V1`, frozen at `b2535d8`, cross-validated over six papers |
| Build / check tooling | `tools/pastpapers/` — `run_toolchain.py` is the entry point |
| Verification evidence | `meoclass1/pastpapers/verification/QP####/` |
| Local provenance | `verification/LOCAL_SOURCE_PROVENANCE.md` — git-ignored, local only |

**Production Intelligence Layer (PIL) V1** exists on `workflow/pil-v1` and is **Founder-review
only** — not merged, not on the content branch. It is two detectors wired into `run_toolchain.py`:
`temporal_sweep.py` (post-sitting dates and inherited donor Q-references) and `surface_impact.py`
(which public / free / paid / commercial / security surfaces a session moved). Both **detect and
report; they do not gate** — `PIL FLAGS; CLAUDE ADJUDICATES`. For what each owns and why, read
[`QA_AND_HANDOVER_PROTOCOL.md`](QA_AND_HANDOVER_PROTOCOL.md) §1 and the PIL entries in
[`WORKFLOW_LESSONS.md`](WORKFLOW_LESSONS.md).

---

## 5. Open review branches

Nothing is merged to `main`. All pages are `noindex` and ungated.

| Branch | Head | Holds |
|---|---|---|
| `workflow/pil-v1` | `850bdde` | PIL V1 — Founder review |
| `workflow/state-history-hygiene` | this branch | the state/history split — Founder review |
| `pastpapers/qp2509-founder-review` | `a5f2551` | QP2509, the newest paper |
| `pastpapers/qp2506-founder-review` | `0d7f872` | QP2506 |
| `pastpapers/qp2510-founder-review` | `8fa4f5f` | QP2510 |
| `pastpapers/qp2508-founder-review` | `dedce2c` | QP2508 |
| `pastpapers/qp2403-founder-review` | `e7d8bc0` | QP2403 |
| `pastpapers/qp2601…qp2606-founder-review` | see `git branch -vv` | the 2026 set, one branch per paper |
| `pastpapers/em2607-founder-review` | `4230a83` | QP2607 — branch name keeps the historical wording deliberately |
| `pastpapers/2024-question-intake` | `7ca36b6` | 2024–2026 intake |
| `pastpapers/2025-question-intake` | `3a4aa14` | 2025 intake |
| `pastpapers/2026-v1-product-review` | `217fbba` | the 2026 V1 product review |
| `commerce/solvedqp-security-v2` | `eaedfda` | frozen; do not reopen without a Founder decision |

---

## 6. Current blockers / Founder decisions

### Blocking publication

1. **The commerce stack cannot carry a paid product as it stands.** Paid content is publicly
   readable (no `vercel.json`, no `middleware.js`), the **client sets the price**
   (`api/create-order.js`), and there is **no entitlement model**. Detail in
   `SOLVED_QP_COMMERCIAL_ARCHITECTURE.md` §2.
2. **The third-party host recurrence annotation ships to students.** `build_paper.py` and
   `build_index.py` render it outside the `if not publish:` guard, and the 2026 set measured it
   wrong in both directions. Fixing it alters six approved pages.

### Awaiting a decision, not blocking

3. **Answer-length band.** Correlation against printed limbs 0.103, core points **0.827**.
   Recommendation: retire 450–650 words and warn outside 20–36 words per core point.
   Validator change is a Founder decision; **not made**.
4. **Solved QP price** — `PRICE_TBD`; `sample_check.py` fails the build if any rupee value renders.
5. **Free/paid placement of the ONLY QUESTIONS year sheet** — MIW recommends free and indexable.
6. **Search payload split** — deferred to a measured UX trigger; no observable problem.
### Known open defects

7. **Q9 / QB9_C cross-link** — known, repair deferred.
8. **The reverse-hint queue is partly adjudicated.** The three `QP2404` rows were ruled on
   2026-08-11 by reading both printed stems — **all three accepted as the same examiner task**, and
   the edges are landed. The remaining rows are still **unadjudicated** and are **not** donors:
   only an author who has read both questions may write `reused_from`. This is a queue, not a
   finding.

### Closed in the pre-QP2404 hardening session — detail in `history/SESSION_HISTORY.md` §32

- **PIL V1.1 is IMPLEMENTED.** `CANDIDATE_FACING_PAID` escalates when it is not the target;
  the V1 advisory NOTE is gone. Detection and reporting only — nothing blocks.
- **The donor model was never directional.** `build_families` has always traversed adjudicated
  edges both ways; it was not changed. The blind spot was in *discovery* — the host annotation
  cannot point forward (819 tokens, zero forward) — and is now inverted into the queue above.
- **`validate_antipatterns.py` does not exist and never had a hook entry.** No `hooks` key in
  any settings file, no such file on disk. The entry was stale; struck rather than carried.

---

## 7. Next production target

**QP2404 — April 2024. IN PROGRESS, STOPPED AT 4 / 9 AND STAGED.** Resume this paper before
starting any other.

| Paper | Tier D | Family reach | Temporal flags |
|---|---|---|---|
| **QP2404** | **4 / 9** | **6** | **1** |
| QP2511 | 3 / 9 | 4 | 2 |
| QP2401 | 3 / 9 | 3 | 2 |
| QP2507 | 0 / 9 | 8 | 2 |

`specs/QP2404.json` on this branch is **intake plus three adjudicated recurrence edges and nothing
else — it carries no answers.** Q3, Q4, Q6 and Q7 were authored and are staged at
`staging/QP2404/`, whose `CHECKPOINT.md` carries the resume command, the banked primary-source
research for Q1/Q2/Q5/Q8/Q9, and one trap that must not be tidied away. The resume is mechanical and
was verified by running it.

Its one flag, `QP2404-Q2` **GUIDELINE EDITION**, was investigated and is **REAL**: `MSC.1/Circ.1687`
postdates the sitting by eight months. A second, unflagged wrong-edition trap was found on `Q8`
(`A.1188(33)` revoked `A.1118(30)` four months before the sitting). Both are written up in
`QP2404_TEMPORAL_AND_DONOR_ANCHOR.md`.

### Standing stop conditions

- **No merge to `main`. No Solved QP launch. No removal of `noindex` or gating.**
- **Never commit or delete the source PDFs.** This repository is public.
- Do not reopen `commerce/solvedqp-security-v2`.
- Do not build the autonomous production agent.
- Do not change the frozen V1 template or the settled architecture without evidence of a defect.
- Do not populate `reference_shelf` before a real resolvable corpus object exists.
- Do not build any part of the viewer or resolver — `reference_href()` stays a seam.
- `QP2504-Q9` must not be answered from either cyber donor until the April 2025 examination date is
  established against the 4 April 2025 issue date of Rev.3.

---

## 8. Restart instructions

```bash
cd F:\Marine-Intelligence-Weekly
git -c safe.directory=* status
python tools/pastpapers/run_toolchain.py
```

Then, in order:

1. Read [`PRODUCTION_PROTOCOL_INDEX.md`](PRODUCTION_PROTOCOL_INDEX.md) — precedence and routing.
2. Read the protocol files it makes mandatory for the kind of session you are in.
3. Read **this file** for state.
4. Read `history/SESSION_HISTORY.md` **only** for the specific section you need.

For a paper production session, also read that paper's
`QP####_TRUE_SOURCE_DEMAND_MAP.md` and the donor rows for it in
`2024_2026_RECURRENCE_AND_REUSE_MAP.md`.

Environment notes: `package.json` sets `"type": "module"`, so Node test files must be `.cjs`.
`file://` pages cannot be inspected by the browser tooling — serve over HTTP for visual review.
Write specs with LF line endings; CRLF corrupts content-hashed assets.

---

## 9. Canonical pointers

| Need | File |
|---|---|
| Precedence and routing | [`PRODUCTION_PROTOCOL_INDEX.md`](PRODUCTION_PROTOCOL_INDEX.md) |
| How a paper is produced | [`PASTPAPER_PRODUCTION_PROTOCOL.md`](PASTPAPER_PRODUCTION_PROTOCOL.md) |
| Sitting-date and donor truth | [`TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md`](TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md) |
| Validation, determinism, Git, report schema | [`QA_AND_HANDOVER_PROTOCOL.md`](QA_AND_HANDOVER_PROTOCOL.md) |
| How to execute work here | [`EXECUTION_EFFICIENCY_POLICY.md`](EXECUTION_EFFICIENCY_POLICY.md) |
| Proven and rejected workflow lessons | [`WORKFLOW_LESSONS.md`](WORKFLOW_LESSONS.md) |
| **Session history, checkpoints, superseded state** | [`history/SESSION_HISTORY.md`](history/SESSION_HISTORY.md) |
| Donor / recurrence map (generated) | [`2024_2026_RECURRENCE_AND_REUSE_MAP.md`](2024_2026_RECURRENCE_AND_REUSE_MAP.md) |
| Source inventory | [`SOURCE_INVENTORY.md`](SOURCE_INVENTORY.md) |
| Commercial and access architecture | [`SOLVED_QP_COMMERCIAL_ARCHITECTURE.md`](SOLVED_QP_COMMERCIAL_ARCHITECTURE.md) |
| Corpus object reference contract | [`MIW_TRUE_SOURCE_CONTRACT.md`](MIW_TRUE_SOURCE_CONTRACT.md) |
| Learning architecture (frozen) | [`MIW_LEARNING_METHOD_DESIGN.md`](MIW_LEARNING_METHOD_DESIGN.md) |

### Where the old `§N` sections went

Other documents cite `CURRENT_STATUS.md §N`. Every one of those sections now lives in
[`history/SESSION_HISTORY.md`](history/SESSION_HISTORY.md), under the same number:

| Citation | Now at |
|---|---|
| `§1`–`§21` (including `§2a`–`§2f`) | `history/SESSION_HISTORY.md`, the `§1–§21` master section |
| `§22`–`§31` | `history/SESSION_HISTORY.md`, same heading, same number |
| the old duplicate `§31` partial checkpoint | renumbered `§30.6`, marked superseded |
