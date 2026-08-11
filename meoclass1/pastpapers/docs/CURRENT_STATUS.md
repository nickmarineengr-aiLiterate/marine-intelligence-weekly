# CURRENT STATUS — MEO Class I Written Questions

**Canonical restart document for the Past Written Papers product. State only.**
Last updated: 2026-08-11, after the **pre-corpus-sync hygiene and freeze** session.

> # QP PRODUCTION IS PAUSED AFTER QP2511.
>
> **Do not start another paper. Not QP2512, not QP2507, not any other.**
> The queue in §7 remains recorded and is **PAUSED — DO NOT START UNTIL THE FOUNDER RESUMES**.
>
> Paused for: repository hygiene · MARPOL Annex VI corpus synchronisation ·
> corpus-consumption integration · online product testing · parallel desktop production setup.
>
> **The next Founder action is the corpus sync**, not a paper — see
> [`CORPUS_SYNC_AND_CONSUMPTION_PLAN.md`](CORPUS_SYNC_AND_CONSUMPTION_PLAN.md) §3.

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
| This branch | `pastpapers/qp2511-founder-review` — **QP2511 COMPLETE 9/9, built and delivered.** Branched from `commerce/solvedqp-recovery` @ `462cfbc`. `staging/` has been retired |
| **Head** | `fddae20` — verified this session. Tracked tree was clean before the freeze commits |
| **Freeze baseline** | `fddae20` is the **proposed PARALLEL PRODUCTION BASELINE COMMIT**, awaiting Founder nomination — see [`PARALLEL_PRODUCTION_BOARD.md`](PARALLEL_PRODUCTION_BOARD.md) §2 |

All git commands in this repository need `-c safe.directory=*`.

---

## 2. Corpus state

Derived from `health_check.py` and `build_reuse_map.py --check` at `850bdde`, not carried forward
from a previous handover.

| | |
|---|---|
| **Corpus** | **252 questions / 117 solved / 135 unsolved** |
| **Papers** | 28 — **13 solved**, 15 answerless intake |
| **Years** | 2024 (11 papers), 2025 (11), 2026 (6). May is absent from the source set in all three years |
| **Tier D (derived)** | **20** of the 135 unsolved carry a verified donor. Unchanged in total by QP2511: its own six left the unsolved set when it was solved, and solving it unlocked six replacements — most usefully `QP2512-Q1` (from `QP2511-Q3`) and `QP2512-Q2` (from `QP2511-Q4`), the adjacent December 2025 sitting |
| **Delivery** | `solvedQP/` — **13 papers, 117 questions, 3 year sheets, 1 index** |
| **Toolchain** | ALL STAGES PASS · `health_check.py` **0 errors, 0 warnings** · reuse map current |
| **Security (offline)** | **62/62 pass** — `security.test.mjs` 34, `sessions.test.mjs` 28. Architecture recovered and proven offline; **nothing deployed, no secret set** |
| **Corpus projection** | `RulesApp/repository/index/` is a **2026-07-25 snapshot at 788 nodes**. The canonical corpus at `F:\RulesApp\repository\` holds **1,006**, and `provision-truth-aliases.json` is **absent** from the MIW copy. **218 nodes behind** — this is the sync gap |

---

## 3. Latest completed papers

| Paper | Sitting | State | Branch |
|---|---|---|---|
| **QP2511** | November 2025 | **COMPLETE 9/9 — newest. Founder review.** | `pastpapers/qp2511-founder-review` |
| QP2404 | April 2024 | complete 9/9 | `pastpapers/qp2404-founder-review` @ `84fee6f` |
| QP2509 | September 2025 | complete 9/9 | `pastpapers/qp2509-founder-review` @ `a5f2551` |
| QP2506 | June 2025 | complete 9/9 | `pastpapers/qp2506-founder-review` @ `0d7f872` |
| QP2510 | October 2025 | complete 9/9 | `pastpapers/qp2510-founder-review` @ `8fa4f5f` |
| QP2508 | August 2025 | complete 9/9 | `pastpapers/qp2508-founder-review` @ `dedce2c` |
| QP2403 | March 2024 | complete 9/9 | `pastpapers/qp2403-founder-review` @ `e7d8bc0` |
| QP2601–QP2604, QP2606, QP2607 | 2026 set | complete, 6 of 6 available sittings | one review branch each |

Full solved set: QP2403 · QP2404 · QP2506 · QP2508 · QP2509 · QP2510 · **QP2511** · QP2601 ·
QP2602 · QP2603 · QP2604 · QP2606 · QP2607.

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
| **Delivery projection** | `solvedQP/` — the paid customer copy, built from the same specs by `build_paper.py --deliver`. **Projection, not source.** Never hand-edit it |
| **Route authorization** | `api/_lib/routes.js` — the single definition of which URL needs which entitlement. `middleware.js` enforces it; nothing else may decide |
| **Price** | `api/_lib/products.js` — the only place an amount is decided. The browser may display a price, never choose one |

`meoclass1/pastpapers/` is the **review** build of the specs; `solvedQP/` is the **delivery**
build of the same specs. Two views, one source. Both are gated by `SOLVED_QP`.

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
| `pastpapers/qp2404-founder-review` | `84fee6f` | QP2404 |
| `pastpapers/qp2509-founder-review` | `a5f2551` | QP2509 |
| `pastpapers/qp2506-founder-review` | `0d7f872` | QP2506 |
| `pastpapers/qp2510-founder-review` | `8fa4f5f` | QP2510 |
| `pastpapers/qp2508-founder-review` | `dedce2c` | QP2508 |
| `pastpapers/qp2403-founder-review` | `e7d8bc0` | QP2403 |
| `pastpapers/qp2601…qp2606-founder-review` | see `git branch -vv` | the 2026 set, one branch per paper |
| `pastpapers/em2607-founder-review` | `4230a83` | QP2607 — branch name keeps the historical wording deliberately |
| `pastpapers/2024-question-intake` | `7ca36b6` | 2024–2026 intake |
| `pastpapers/2025-question-intake` | `3a4aa14` | 2025 intake |
| `pastpapers/2026-v1-product-review` | `217fbba` | the 2026 V1 product review |
| `pastpapers/qp2511-founder-review` | this branch | **QP2511, COMPLETE 9/9 — the newest paper.** Branched from `commerce/solvedqp-recovery` @ `462cfbc`; built, delivered, `staging/` retired |
| `commerce/solvedqp-recovery` | `462cfbc` | **the Solved QP delivery product and the offline security stack** — Founder review. Branched from `bf87b1a`; inert, nothing deployed |
| `commerce/solvedqp-security-v2` | `eaedfda` | frozen. **Do not merge.** Its content was selectively recovered onto `commerce/solvedqp-recovery`; its stale `solvedQP/` HTML was deliberately not |

---

## 6. Current blockers / Founder decisions

### Blocking publication

1. **Customer passwords have not been confirmed rotated.** The Security V2 incident record
   requires rotation for the existing customer base after two unauthenticated endpoints were
   found reachable in production. No evidence of completion exists anywhere in this repository.
   Treat as **UNCONFIRMED**. This blocks launch, not further engineering.
2. **The recovered security stack is inert.** `commerce/solvedqp-recovery` holds `middleware.js`,
   `vercel.json`, `api/session.js` and `api/_lib/*`, all proven offline, but **nothing is
   deployed and no secret is set**. Until `MIW_SESSION_SECRET`, `KV_REST_API_URL` and
   `KV_REST_API_TOKEN` exist in the Vercel project and the branch is deployed, production paid
   content remains as exposed as before. Middleware fails closed, so a half-configured deploy
   denies rather than leaks — but it denies *everyone*, including paying customers.
3. **`BUNDLE` has no approved price** and `create-order` refuses it. A bundle cannot be sold
   until the Founder sets an amount. None was invented.

*Resolved by the recovery session, 2026-08-11 — architecture only, not activation:* the client
no longer sets the price (`api/create-order.js` reads `api/_lib/products.js` and discards any
amount in the body); an entitlement model exists and is enforced by a single route policy
(`api/_lib/routes.js`); and `/meoclass1/pastpapers/` now requires `SOLVED_QP`, so the Written
library is not handed to Oral customers. The third-party host recurrence annotation blocker was
already closed earlier in this lineage — `search_tokens` drops it in every mode and the card
renders `corpus_relations()` instead — and the delivery checker now guards that boundary.

### Awaiting a decision, not blocking

3. **Answer-length band.** Correlation against printed limbs 0.103, core points **0.827**.
   Recommendation: retire 450–650 words and warn outside 20–36 words per core point.
   Validator change is a Founder decision; **not made**.
4. **Solved QP price** — `PRICE_TBD`; `sample_check.py` fails the build if any rupee value renders.
5. **Free/paid placement of the ONLY QUESTIONS year sheet** — MIW recommends free and indexable.
6. **Search payload split** — deferred to a measured UX trigger; no observable problem.
### Raised and CLOSED by the QP2404 session, 2026-08-11

Both were reported at the end of the QP2404 production run and the Founder authorised both.
Fixed in `caf5020`.

9. **Candidate-facing authoring-date leaks — CLOSED.** A field-class-aware scan of the whole
   corpus found **six**, not the two originally reported: `QP2506-Q5`, `QP2508-Q1`, `QP2601-Q1`,
   `QP2602-Q4` (not Q2 — the earlier id came from a line-number grep), `QP2602-Q8` and
   `QP2607-Q7`. Two of them said **February 2026**, which the first grep never looked for.
   **Five were corrected**, each judged individually rather than blind-replaced.
   **One was deliberately kept:** `QP2602-Q8` carries an explicitly labelled, quarantined
   *"Currency warning for anyone revising this after August 2026"* which protects the sitting
   answer rather than competing with it — the one case the governing rule permits to remain.
   Verified against **shipped bytes**, not just specs: the built pages stripped of `prod-meta`
   and review-banner blocks contain exactly that one hit corpus-wide.
10. **`QP2509` stale paper-level state — CLOSED.** Now `Pilot Review Ready` /
    *"Awaiting Founder Review — complete paper"*, version 1.0. All 28 papers now check
    consistent: solved → `Pilot Review Ready`, intake → `Intake Complete`.
    Correction to the original report: these fields are **not** unread downstream. The two HTML
    renderings are publish-guarded, but `build_index.py` writes both into
    `pastpapers_content_index.json` **unconditionally**, and that manifest is classified
    `PUBLIC_FREE` — so the stale value was in a public artefact.

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

## 7. Production queue — **PAUSED**

> **PAUSED — DO NOT START UNTIL THE FOUNDER RESUMES.**
> Everything below is the queue **as recorded**, not work that is authorised. QP2512 is **not**
> the next immediate work; the corpus sync is. The queue is kept intact so that no donor
> intelligence is lost across the pause.

**QP2511 — November 2025 — IS COMPLETE 9/9, BUILT AND DELIVERED.** Awaiting Founder review.

Its temporal foundation is recorded in
[`QP2511_TEMPORAL_AND_DONOR_ANCHOR.md`](QP2511_TEMPORAL_AND_DONOR_ANCHOR.md), and the nine
verification records are at `verification/QP2511/`. The `staging/` directory has been **retired**.

### Recommended next paper: **QP2512 — December 2025**

| Paper | Tier D | Family reach | Temporal flags |
|---|---|---|---|
| **QP2512** | **3 / 9** | 0 | 2 |
| QP2401 | 3 / 9 | 3 | 2 |
| QP2410 | 3 / 9 | 0 | 4 |
| QP2507 | 0 / 9 | **8** | 2 |

QP2507 still holds the highest *family reach* in the corpus, and on that measure alone it leads. It
is nevertheless **not** the recommendation, for the same reason it was not the recommendation before
QP2511: it starts from **zero** verified donors, so every one of its nine questions is fresh research.

**QP2512 is recommended because the research just completed transfers to it almost whole.** It is the
sitting immediately after QP2511, so the entire November 2025 line — the 34th Assembly boundary, the
Merchant Shipping Act 1958 position, the Net-Zero Framework as approved-but-not-adopted, the FAL
amendment position, the Hong Kong Convention in force — applies with **one** adjustment rather than
being rebuilt. Two of its questions now have direct donors from QP2511 itself (`QP2512-Q1` from
`QP2511-Q3`, `QP2512-Q2` from `QP2511-Q4`).

> **The one adjustment, and it is sharp.** The **34th IMO Assembly sat 24 November – 3 December 2025
> and adopted its resolutions at the close of that session**. A December 2025 sitting may therefore
> fall on **either side** of that boundary, where a November one cannot. Establishing the December
> examination date against 3 December 2025 is the **first** task of that session, and if it cannot be
> established the `A.12xx(34)` family must be treated as excluded rather than assumed available.

**Do not start a new paper. Production is paused — see the banner at the top of this file.**

### Planned work while production is paused

| Workstream | State | Plan |
|---|---|---|
| **MARPOL Annex VI corpus sync** | **NEXT — Founder action** | [`CORPUS_SYNC_AND_CONSUMPTION_PLAN.md`](CORPUS_SYNC_AND_CONSUMPTION_PLAN.md) |
| Online product testing | planned, **not deployed** | [`ONLINE_TEST_PLAN.md`](ONLINE_TEST_PLAN.md) |
| Parallel desktop production | designed, **not started, no branch created, no paper allocated** | [`PARALLEL_PRODUCTION_BOARD.md`](PARALLEL_PRODUCTION_BOARD.md) |

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
| **Corpus sync destination, consumption, pilot** | [`CORPUS_SYNC_AND_CONSUMPTION_PLAN.md`](CORPUS_SYNC_AND_CONSUMPTION_PLAN.md) |
| **Online test plan / Planned-soon design** | [`ONLINE_TEST_PLAN.md`](ONLINE_TEST_PLAN.md) |
| **Parallel desktop production / paper ownership** | [`PARALLEL_PRODUCTION_BOARD.md`](PARALLEL_PRODUCTION_BOARD.md) |
| Learning architecture (frozen) | [`MIW_LEARNING_METHOD_DESIGN.md`](MIW_LEARNING_METHOD_DESIGN.md) |

### Where the old `§N` sections went

Other documents cite `CURRENT_STATUS.md §N`. Every one of those sections now lives in
[`history/SESSION_HISTORY.md`](history/SESSION_HISTORY.md), under the same number:

| Citation | Now at |
|---|---|
| `§1`–`§21` (including `§2a`–`§2f`) | `history/SESSION_HISTORY.md`, the `§1–§21` master section |
| `§22`–`§31` | `history/SESSION_HISTORY.md`, same heading, same number |
| the old duplicate `§31` partial checkpoint | renumbered `§30.6`, marked superseded |
