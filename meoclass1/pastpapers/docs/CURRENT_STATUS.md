# CURRENT STATUS — MEO Class I Written Questions

**Canonical restart document for the Past Written Papers product. State only.**
Last updated: 2026-08-12, after **QP2512 was completed to 9 / 9 and pushed for Founder review**.
See §7a for the QP2512 state and §1a for the security and deployment state.

> # QP2512 IS COMPLETE — 9 / 9 — AND AWAITS FOUNDER REVIEW.
>
> **The Founder lifted the pause on 2026-08-12 and authorised QP2512 — December 2025 — as the sole
> laptop production object. It is now finished.** All nine questions are authored, verified,
> assembled into the canonical spec, built on both surfaces and swept. `specs/QP2512.json` reads
> `build_state: Pilot Review Ready`, `review_state: Awaiting Founder Review - complete paper`,
> `version 1.0`. `staging/QP2512/` has been **retired**.
>
> **The branch `pastpapers/qp2512-founder-review` is pushed and NOT merged.** No merge to `main`
> and no deployment. QP2512 enters production only on Founder approval.
>
> **Nothing else is authorised.** Do not start another laptop paper without the Founder, and in
> particular do not touch the six desktop-allocated 2024 papers (`QP2401`, `QP2412`, `QP2402`,
> `QP2409`, `QP2411`, `QP2410`).
>
> Corpus consumption remains integrated (§2a) and read-only. **The Founder decisions in §6 are
> still open and did not block QP2512** — it cites none of the three corpora, so its
> `reference_shelf` is empty on all nine questions, which is the correct outcome and not a gap.

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
| **`main`** | **`2f38586` — LIVE IN PRODUCTION.** The Written product, Security V2 and the whole pastpapers line were merged to `main` and deployed 2026-08-12. `main` is no longer a stale pre-product branch; it is what customers are served |
| Content head | `a5f2551` on `pastpapers/qp2509-founder-review` — the newest solved-paper state |
| Tooling head | `850bdde` on `workflow/pil-v1` — content head plus the Production Intelligence Layer |
| Release branch | `release/written-live-test-v1` — the reconciliation branch the cutover was assembled on. Fast-forwarded into `main`; kept as the release lineage |
| **Desktop baseline** | **`9c97359` — UNCHANGED and immutable.** The six 2024 paper branches were allocated from it and are unaffected by everything below. Do NOT tell the desktop team to rebase because `main` moved |
| **Consumer branch** | `workflow/corpus-consumer-integration` @ `d2e09a4` — now fully contained in `main` |

All git commands in this repository need `-c safe.directory=*`.

---

## 1a. Security and deployment state — 2026-08-12

**The product is LIVE for controlled testing.** Four blockers were closed in one session; two of
them were discovered during the work, not inherited.

| | |
|---|---|
| Production commit | `2f38586` |
| Public URL | https://marineintelligenceweekly.com |
| **Credential exposure** | **CLOSED.** 100 accounts rotated to random 16-character credentials, stored as salted hashes. Audit: 100 legacy plaintext → **0**. 100 notified, 0 failures |
| **Affected count** | **100, not 28.** 28 was the size of the leaked git blob; the removed `api/check-db.js` disclosed any stored credential to an unauthenticated GET, so the exposure was never limited to it |
| **Legacy plaintext auth** | **REMOVED**, not disabled. `verifyPassword` accepts `sha256$salt$digest` only |
| **`MIW_SESSION_SECRET`** | CONFIGURED, Production and Preview. 14/14 Production variables present |
| **Edge gate** | LIVE and enforcing. A forged `miw_auth=1` now grants nothing |
| **Entitlements** | 100 back-filled to `ORAL_QB_NOTES`. `SOLVED_QP` granted to **one** account only |
| **Subscriber ceiling** | **REMOVED.** `QB_PASSWORD_POOL` no longer gates sign-ups; credentials are generated per sale |
| **Password reset** | Self-service, live. Issues a NEW credential — the old one is unrecoverable by design |
| Test suites | **121 green** — 38 security, 32 sessions, 22 rotation, 29 reset |

Full record, including the four open non-blocking defects and the classification of the
historical git exposure, is in
[`WRITTEN_PRODUCT_LIVE_TEST_STATUS.md`](WRITTEN_PRODUCT_LIVE_TEST_STATUS.md) §10–§20.

**Outstanding and NOT closed by that session:** the Upstash REST token, the Brevo SMTP key and a
Brevo account password were pasted into a chat transcript during the work and must be rotated at
source. That is independent of the git-history incident.

---

## 2. Corpus state

Recomputed from the specs, `build_reuse_map.py` and `solvedqp_check.py` after QP2512 was solved on
2026-08-12. Not carried forward from a previous handover.

| | |
|---|---|
| **Corpus** | **252 questions / 126 solved / 126 unsolved** — the halfway point |
| **Papers** | 28 — **14 solved**, 14 answerless intake |
| **Years** | 2024 (11 papers), 2025 (11), 2026 (6). May is absent from the source set in all three years |
| **Tier D (derived)** | **17** of the 126 unsolved carry a verified donor, down from 20. QP2512 consumed three of its own (`Q1`, `Q2`, `Q9`) and, unlike QP2511, **unlocked none** — its six tier-C questions produced no new donor edge, because six of the nine were adjudicated as fresh or limb-supported rather than family-linked |
| **Delivery** | `solvedQP/` — **14 papers, 126 questions, 3 year sheets, 1 index** |
| **Toolchain** | ALL STAGES PASS · `--self-test` PASS · double-build **byte-identical across 91 artefacts** |
| **Security (offline)** | **62/62 pass** — `security.test.mjs` 34, `sessions.test.mjs` 28. Architecture recovered and proven offline; **nothing deployed, no secret set** |
| **Corpus projection (legacy)** | `RulesApp/repository/index/` is a **2026-07-25 snapshot at 788 nodes** of the `RulesApp` repository. **This is NOT the True Source corpus** — see §2a. It remains 218 nodes behind its own master and is no longer the resolver target |

---

## 2a. True Source consumer integration

The True Source corpus is a **separate private repository**, not the `RulesApp` tree §2 describes.
Consuming it is integrated, tested and **read-only**.

| | |
|---|---|
| **Corpus repository** | `nickmarineengr-aiLiterate/RulesApp-Local-Input` (**PRIVATE**), checkout `F:\RulesApp-Local-Input` |
| **Corpus commit consumed** | **`64977b86ed9c601e273f1d0cb55abb0461835811`** = `origin/main`, 0 ahead / 0 behind, tracked tree clean |
| **Rights** | `FD-RIGHTS-1`, status **ACTIVE**. Read live from `true-source/source-rights-register.json` at every call — never hard-coded, because the clearance is revocable |
| **Open reservations** | `FD-RIGHTS-1-R1` (FSS, Digitrace licence) and `FD-RIGHTS-1-R2` (all three, IMO copyright) — both **OPEN, disclosed, not discharged**. Neither blocks citation or reference use |
| **Consumer seam** | `tools/corpus/consumer_adapter.py`, read-only, degrades to `CORPUS_UNAVAILABLE` when the private corpus is absent so no build depends on it |
| **Schema change** | **NONE.** `reference_shelf`'s five fields were sufficient. Only `validate_spec.py::REF_ID_RE` widened, to admit dotted ids such as `LSA-1.1.1` |
| **Consumer tests** | `tools/corpus/consumer_adapter_test.py` — **60 checks, 0 failures**, positive and negative controls, deterministic. Skips cleanly when the corpus is absent |

### Instrument readiness — three different shapes

**RIGHT TO QUOTE and TEXT AVAILABLE TO QUOTE are different fields.** No two of these agree.

| | Rights operative today | Addressing | Provision text | Consumer readiness |
|---|---|---|---|---|
| **LSA Code** | **YES** | native `provisionId` — `LSA-1.1.1` | **292/292 verbatim**, page-verified, shortest 65 chars | **Quotation-ready.** The only corpus a verbatim view can be built on |
| **FSS Code** | YES, with `R1` | chapter **+** number — `FSSCode-9-2.5.1.3`; chapter is part of the identity | **Summary, not wording** — the derivative self-declares it. 35/421 have no text, 22/386 are labels | **Evidence-ready, NOT quotation-ready** — see [`TRUE_SOURCE_CORRECTION_REQUESTS.md`](TRUE_SOURCE_CORRECTION_REQUESTS.md) TSCR-1 |
| **MARPOL Annex VI** | **NO** — `operativeToday: false` | resolver, 320 entries — `MARPOL-VI-14-146` | **NONE.** `finalDerivativeBuildId: null` | **Citation-ready only.** Resolves to identity, citation and provenance; never to text |

**MARPOL identity is not split.** All 320 resolver entries are canonical `MARPOL-VI-*`;
`MEPC32876-*` appears only among the 527 aliases and resolves **in**, never out. The dual-vocabulary
problem recorded in `CORPUS_SYNC_AND_CONSUMPTION_PLAN.md` §2.1 is a property of the **legacy
`RulesApp` projection** (56 nodes, 36 `MEPC32876` / 20 `MARPOL-VI`), not of True Source. It is
therefore **not a blocker** to writing Annex VI references.

### Pilot — already-solved questions only

`QP2508-Q3`, `QP2602-Q3`, `QP2607-Q4`. Six shelf entries, **no answer wording changed**. All
`REFERENCE_PENDING`, because no viewer route can land on a provision for any corpus yet, so the
paid publish build is byte-unchanged and **no dead "Verify source" control is emitted**.

### Blocked

The **candidate-facing verbatim provision view is not implemented.** Of the three corpora, the one
with real demand from solved answers (MARPOL Annex VI) has no text, the one with text and demand
(FSS) carries summaries rather than wording, and the one that is fully quotation-ready (LSA) is
**cited by none of the 117 solved questions**. See §6.

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

### Blocking the candidate-facing provision view

**A. No corpus can currently carry a verbatim provision view to a solved candidate.** Not one
blocker but three, one per instrument, and each needs a different action:

| Corpus | Why it cannot be shown today | What would unblock it |
|---|---|---|
| **MARPOL Annex VI** | No derivative exists; `FD-RIGHTS-1` records `operativeToday: false` | Producer-team **MARPOL Annex VI derivative build** carrying provision text. New engineering, not a build step — the derivative engine has adapters for FSS and LSA only |
| **FSS Code** | The derivative declares its wording a *"verified summary, NOT the official text"* | Founder/producer resolution of **TSCR-1** — amend the rights record, or build a wording-bearing FSS derivative |
| **LSA Code** | Nothing technical. **No solved question cites the LSA Code**, so there is nothing to attach a view to | A Founder decision on whether to author LSA-dependent questions, or accept the view lands with future papers |

**B. Publication boundary — Founder decision required.** This repository is **PUBLIC**. Rendering
provision text into `solvedQP/` commits corpus text to a world-readable repository, which is not
the same permission as `FD-RIGHTS-1`'s candidate-facing quotation clearance and sits directly
against its prohibition on *"any surface from which the corpus text can be reassembled wholesale"*.
This compounds the known commerce-stack exposure in the items below. **No corpus text was
committed.** The viewer must be decided together with where its text is served from.

**C. No ID→anchor deep link exists for any corpus** (TSCR-2). `reference_href()` can address an
object; nothing can land on the exact section. Every pilot entry is therefore `REFERENCE_PENDING`.

### Blocking publication

1. **`LAUNCH-BLOCK-1` — published customer credentials still authenticate. CONFIRMED, not merely
   unconfirmed.** Upgraded from *"rotation UNCONFIRMED"* on 2026-08-11 after direct verification.
   **28 real customer email/plaintext-password pairs are published in this PUBLIC repository's
   history** (reachable at `0766d00^:api/migrate-users.js`; `0766d00` is `origin/main`), and
   `verifyPassword` still accepts legacy plaintext, so every one of them **authenticates today**.
   Removing the files in `0766d00` stopped the live endpoints but could not remove the blobs from
   published history — `git ls-tree HEAD` reporting ABSENT proves *"not in the tree"*, not
   *"no longer disclosed"*. **This blocks live deployment of any paid surface.** It does not block
   QP authoring or further engineering. Full record, evidence and the five required Founder actions:
   [`WRITTEN_PRODUCT_LIVE_TEST_STATUS.md`](WRITTEN_PRODUCT_LIVE_TEST_STATUS.md) §1–§2.
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

## 7a. QP2512 — December 2025 — **COMPLETE 9 / 9, READY FOR FOUNDER REVIEW**

Branch `pastpapers/qp2512-founder-review`, based on `7e51b97`. Completed 2026-08-12.

| | |
|---|---|
| **Authored** | **All nine**, each with a verification record at `verification/QP2512/` |
| **Canonical spec** | `specs/QP2512.json` — `Pilot Review Ready`, *"Awaiting Founder Review - complete paper"*, `version 1.0` |
| **Validation** | **0 errors.** 9 warnings, all the deferred 450–650 word band (§6 item 3). **0 blocking** re-verification flags |
| **Build** | `meoclass1/pastpapers/QP2512.html` (review, `noindex`) and `solvedQP/QP2512.html` (delivery, no review banner) |
| **Determinism** | double-build **byte-identical across 91 generated artefacts** |
| **Delivery surface** | QP2512 now renders **Available** on `solvedQP/index.html`, transitioned automatically by the generated surface — no manual status edit |
| **Staging** | **RETIRED.** `staging/QP2512/` removed; its content lives in the canonical spec |
| **Merge / deploy** | **NOT merged, NOT deployed.** Founder review only |
| **Read first** | [`QP2512_TEMPORAL_AND_DONOR_ANCHOR.md`](QP2512_TEMPORAL_AND_DONOR_ANCHOR.md) |

**Reuse as built:** tier **D on Q1, Q2, Q9** (donors `QP2511-Q3`, `QP2511-Q4`, `QP2509-Q4`); tier
**C on Q3–Q8**, of which Q3, Q5 and Q8 carry adjudicated limb-level support and Q4, Q6 and Q7 are
fresh. `reference_shelf` is **empty on all nine** — the paper cites none of the three corpora.

**The two findings that governed the paper, both confirmed at source:**

1. **The whole `A.12xx(34)` family is excluded**, and the reason is a *document* date rather than an
   adoption date. The source prints `DECEMBER 2025` with **no day**, but `A 34/Res.1206` was adopted
   3 December 2025 and **issued 5 December 2025**, so the exclusion holds without pinning the sitting.
   **No `A.12xx(34)` resolution appears in any candidate-facing field of any question.**
2. **The Procedures for Port State Control have three editions, not two.** **`A.1185(33)` of
   6 December 2023 is operative** — `A.1155(32)` was revoked in 2023 and the 2025 edition had not
   been issued. `A.1185(33)` was re-obtained and read at source for Q8, and its operative paragraph 4
   confirms the revocation. Its natural support `QP2606-Q2` is built entirely on the 2025 edition and
   was therefore **not cloned**: Q8 was authored fresh so the excluded edition could not enter.

**The known dependency is closed.** `Q1`'s cross-link to `QP2512.html#q8` now resolves; all nine
anchors and all seven internal cross-links resolve in the built page.

---

## 7. Production queue — QP2512 complete, nothing else authorised

> **QP2512 is finished and awaiting Founder review (§7a). Everything below remains the queue as
> recorded, not work that is authorised.** Do not nominate another laptop paper without the Founder.

**QP2511 — November 2025 — IS COMPLETE 9/9, BUILT AND DELIVERED.** Awaiting Founder review.

Its temporal foundation is recorded in
[`QP2511_TEMPORAL_AND_DONOR_ANCHOR.md`](QP2511_TEMPORAL_AND_DONOR_ANCHOR.md), and the nine
verification records are at `verification/QP2511/`. The `staging/` directory has been **retired**.

**QP2512 — December 2025 — IS ALSO COMPLETE 9/9, BUILT AND DELIVERED.** Awaiting Founder review;
see §7a. Its `staging/` directory has been **retired**. Its temporal foundation is recorded in
[`QP2512_TEMPORAL_AND_DONOR_ANCHOR.md`](QP2512_TEMPORAL_AND_DONOR_ANCHOR.md).

The December adjustment this section previously flagged as *"sharp"* was worked and is now settled:
the sitting date is **not printed on the paper**, and the `A.12xx(34)` exclusion was established from
the resolution's **issue date of 5 December 2025** rather than by pinning the sitting. It also
surfaced a **third** edition of the Procedures for Port State Control that the note did not
anticipate — see §7a.

### Best remaining 2025 candidate — **QP2502, February 2025** — INFORMATION ONLY, NOT AUTHORISED

Recomputed from the derived map after QP2512 was solved, not carried forward as an estimate:

| Paper | Sitting | Tier D | Family reach | Temporal flags |
|---|---|---|---|---|
| **QP2502** | February 2025 | **2 / 9** | 5 | 2 |
| QP2503 | March 2025 | 1 / 9 | 5 | 3 |
| QP2504 | April 2025 | 1 / 9 | 5 | 4 |
| QP2501 | January 2025 | 0 / 9 | 3 | 2 |
| QP2507 | July 2025 | 0 / 9 | **8** | 2 |

**QP2502 leads on verified donors**, which is the measure that has predicted actual session cost
better than family reach on every paper so far. QP2507 still holds the highest family reach in the
corpus and is still **not** the recommendation, for the reason it has never been: it starts from
**zero** verified donors, so all nine questions are fresh research.

> **This is a recomputation for information, not an authorisation.** No laptop paper is authorised.
> The Founder nominates the next one.

### Planned work while production is paused

| Workstream | State | Plan |
|---|---|---|
| **MARPOL Annex VI corpus sync** | **NEXT — Founder action** | [`CORPUS_SYNC_AND_CONSUMPTION_PLAN.md`](CORPUS_SYNC_AND_CONSUMPTION_PLAN.md) |
| Online product testing | **BLOCKED — not deployed.** Release candidate is green; `LAUNCH-BLOCK-1` gates it | [`WRITTEN_PRODUCT_LIVE_TEST_STATUS.md`](WRITTEN_PRODUCT_LIVE_TEST_STATUS.md) |
| **Parallel desktop production** | **SIX 2024 PAPERS ALLOCATED — NOT STARTED.** Playbook and board written; baseline nominated | [`DESKTOP_QP_ALLOCATION_2024.md`](DESKTOP_QP_ALLOCATION_2024.md) · [`DESKTOP_QP_PRODUCTION_PLAYBOOK.md`](DESKTOP_QP_PRODUCTION_PLAYBOOK.md) |

### Written product deployment status — 2026-08-11

**NOT LIVE. NOT DEPLOYED. NO MERGE TO `main` WAS PERFORMED.** The Founder authorised live
deployment for controlled testing; the authorisation was conditioned on no unresolved security
prerequisite, and `LAUNCH-BLOCK-1` above is unresolved. Pre-deploy acceptance is otherwise **green**
— toolchain ALL STAGES PASS, security 62/62, corpus consumer 60/60, coverage and solvedqp
self-tests pass on seeded positives, and a full toolchain run left the tracked tree byte-identical.
**Desktop QP production is unaffected and may start.**

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
