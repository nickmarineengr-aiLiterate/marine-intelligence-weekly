# CURRENT STATUS — MEO Class I Written Questions

**Canonical restart document for the Past Written Papers product. State only.**
Last updated: 2026-08-13, after **QP2406 (June 2024) was laptop-reviewed and published to
`main`**, taking the product to 26 papers / 234 questions and **closing Batch 2 at 6/6**.
See §7j for QP2406, §7h for QP2507, §7g for QP2504, §7f for QP2503, §7e for QP2501 and QP2502,
§7a for QP2512, §7b for the derived layer, §7c for the desktop batches, §1a for security.

> # QP2512 IS LIVE. THE SOLVEDQP DERIVED LAYER IS BUILT.
>
> **DESKTOP BATCH 1 IS 6/6 REVIEWED AND LIVE.** `QP2401`, `QP2412`, `QP2402`, `QP2409`, `QP2411`
> and `QP2410` were each reviewed, integrated and published **one at a time**, every one by path
> extraction onto current `main` rather than by merging its stale branch. All six desktop branches
> are **retained** as provenance evidence and were not deleted.
>
> **Product: 26 available papers · 234 published questions · 252 in the corpus.**
> 18 unsolved questions remain across 2 unsolved papers — `QP2407` and `QP2408`, both July and
> August 2024, and **both still at 0/9 with no branch on `origin`**.
>
> **THE 2025 EXAMINATION YEAR IS COMPLETE.** All eleven 2025 sittings MIW holds are solved and
> live. May 2025 is recorded as `NO SITTING` on evidence, not absence: the printed serial numbering
> runs …2504, 2506… with nothing at 2505. Every unsolved paper left in the corpus is a 2024 sitting.
>
> **Three defects were corrected, two of them on already-live papers.** The referred
> `QP2402-Q3` regulation-21 defect was confirmed against the corpus copy of `MEPC.328(76)` and
> fixed — and generalising the referral instead of applying it to the named question alone found
> the same defect in `QP2402-Q5` and `QP2402-Q6`, a live EEXI mislabel on `QP2601-Q1`, and the
> false Hong Kong Convention source state on `QP2511-Q8` and `QP2603-Q9`. See §7d.
>
> **One generated inventory now serves the whole delivery product.**
> `solvedQP/solvedqp_content_index.json` is the single source for the home counts, the coverage
> grid, the topic search, the latest-updates strip and the daily health report. Nobody hand-edits
> it; nobody keeps a second list. See [`SOLVEDQP_DERIVED_LAYER.md`](SOLVEDQP_DERIVED_LAYER.md).
> Every one of the six papers was absorbed by it automatically — availability is derived from the
> presence of model answers, so no status was ever edited by hand.
>
> **Nothing is authorised for laptop authoring.** Do not start a paper without the Founder.
> Batch 1 is closed. **BATCH 2 IS 6/6 LIVE AND CLOSED** — QP2501, QP2502 (§7e), QP2503 (§7f),
> QP2504 (§7g), QP2507 (§7h) and QP2406 (§7j), each authored by the desktop, laptop-reviewed and
> published one at a time, every one by path extraction onto current `main`. All six desktop
> branches are **retained** as provenance and were never merged.
>
> **THE 2023 INTAKE IS ACQUIRED AND AUDITED — it is the FINAL set to be solved.** Eleven MEO
> Class I Engineering Management papers, all 9 questions, all audited 2026-08-13. **May 2023 does
> not exist** and the serials prove it (2304 → 2306, nothing at 2305) — May is now absent in
> **2023, 2024 and 2025**. The 2023 serial convention is **reversed**: `2301 EM`, not
> `Sr. No. EM – 2406`. Source PDFs are on disk and **git-ignored**; hashes and host filenames are
> in the git-ignored `verification/LOCAL_SOURCE_PROVENANCE.md`.
>
> Two desktop handovers are written and are the authority on what comes next:
> **[`DESKTOP_QP_HANDOVER_BATCH3.md`](DESKTOP_QP_HANDOVER_BATCH3.md)** — QP2407 then QP2408, in
> that order on recomputed donor readiness (5/9 against 3/9) — and
> **[`DESKTOP_QP_ALLOCATION_2023.md`](DESKTOP_QP_ALLOCATION_2023.md)** — six 2023 papers
> (QP2312 · QP2304 · QP2301 · QP2303 · QP2309 · QP2302), **not to be started until QP2407 and
> QP2408 are live**. Every 2023 paper pre-dates the whole solved corpus, so **every donor in that
> batch runs backwards** — the QP2406 situation applied eleven times over.
>
> **QP2407 and QP2408 have NOT been started.** No `pastpapers/qp2407-founder-review` or
> `qp2408-founder-review` branch exists on `origin`, and both specs remain `Intake Complete` at
> 0/9 built. A session brief asserting that the desktop had completed them was checked against
> `git ls-remote` and was **not correct** — see §7j. The laptop waits for a complete 9/9 desktop
> push before reviewing either.
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
| **`main`** | **`0816f3d` — LIVE IN PRODUCTION.** The Written product, Security V2 and the whole pastpapers line were merged to `main` and deployed 2026-08-12. `main` is no longer a stale pre-product branch; it is what customers are served |
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
| Production commit | `0816f3d` |
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

Recomputed from the generated manifest `solvedQP/solvedqp_content_index.json` after QP2407 was
reviewed and published on 2026-08-13. Not carried forward from a previous handover.

| | |
|---|---|
| **Corpus** | **252 questions / 243 solved / 9 unsolved** — 96.4 per cent solved |
| **Papers** | 28 — **27 solved**, 1 answerless intake |
| **Years** | 2024 (11 papers), 2025 (11), 2026 (6). May is absent from the source set in all three years |
| **Tier D (frozen intake field)** | **3** of the 72 unsolved, down from 17. Batch 1 consumed most of the pool. **Do not plan from this number** — it is the frozen intake field, and Batch 1 proved again that it goes stale: `QP2401-Q9` was frozen at tier C and derived to D, and `QP2410`'s board was wrong in both directions. The derived tier from `build_reuse_map.py` governs, and it is what makes the Batch 2 ordering constraint (`QP2507` after `QP2501` and `QP2503`) real |
| **Delivery** | `solvedQP/` — **27 papers, 243 questions, 3 year sheets, 1 index** |
| **Toolchain** | ALL STAGES PASS · `--self-test` PASS · double-build **byte-identical across 265 artefacts** |
| **Security (offline)** | **121/121 pass** — `security.test.mjs` 38, `sessions.test.mjs` 32, `rotation.test.mjs` 22, `reset.test.mjs` 29. Re-run unchanged after all six integrations; no security surface was touched |
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
| `pastpapers/qp2507-founder-review` | `3f37176` | QP2507 — **integrated to `main` by path extraction; retained as provenance, never merged** |
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

## 7k. QP2407 (July 2024) — laptop-reviewed against the NEW True Source repository — **FIRST CONTROLLED USE**

```text
TRUE SOURCE REPO:      F:\miw-true-source  (workstation path — cite object IDs, never this path)
                       https://github.com/nixonvantony/miw-true-source
TRUE SOURCE HEAD:      7f8c9fb743854bdc8d5838184d314a956a110ecd  (main, clean, 0 local changes)
WRITTEN REPO:          F:\Marine-Intelligence-Weekly
WRITTEN BRANCH:        integration/qp2407-laptop-review  (from origin/main e099711)
QP2407:                PUBLISHED — 9/9 built, desktop build 7e71066 reviewed not rebuilt
REVIEW:                COMPLETE — 8 accepted as-is, 1 major amendment (Q8)
VALIDATION:            ALL STAGES PASS · validate_spec 0 errors · UI 66/66 · audit clean
TRUE SOURCE GAPS:      1 (TS-GAP-1, non-blocking) + 4 corpus defects TSCR-5..TSCR-8
NEXT ACTION:           Founder review. Do NOT start another True Source paper until
                       TSCR-5 (duplicate object_ids) and TSCR-6 (TRAP-RULE-D-FAULT) are
                       adjudicated. Next recommended paper is QP2501, on subject fit.
```

**The corpus is marine law; QP2407 is a technical/IMO-regulatory paper.** One question of nine
intersected. That single question was nevertheless the right one: Q8 was the only question on the
paper carrying **zero `P1_PRIMARY_VERIFIED` claims**, and it is now at five.

| Measure | Before | After |
|---|---|---|
| `validate_spec` errors | 0 | 0 |
| `validate_spec` warnings | 11 | **10** |
| Q8 primary-verified claims | **0** | **5** |

**Q8 — what was added,** each anchored to a corpus object and folded into existing sections so no
section was renumbered (`memory_cue`, `answer_route` numbering and retrieval card `C1` stay valid):

1. **`YAR-D` — Rule D.** Absent from the desktop build entirely, and the doctrinal hinge of limb (a):
   rights to contribution are not affected by fault, **but that does not prejudice remedies or
   defences**. That residue is exactly what the New Jason Clause was written to close.
2. `TRAP-GA-PA` — general average vs particular average.
3. `YAR-C` — only direct consequences; delay and market loss excluded.
4. `YAR-VI` — salvage, including Art. 14 / SCOPIC, is a particular charge, outside the adjustment.
5. `YAR-XVII` — contributory values; answers the printed limb "implications for cargo owners".

Plus edition control in the answer body: the York-Antwerp Rules are a **contractual code of the CMI
with no entry into force of their own**, 2016 current, 1994 still live.

**Declared limitations all stand.** MIW still holds no wording of the New Jason Clause, the 3/4ths
Collision Clause or any Institute clause set; no section of the Marine Insurance Act, 1963 is cited.

**A corpus trap was itself wrong.** `TRAP-RULE-D-FAULT` asserts the Rule Paramount bars GA on fault.
The Rule Paramount is a **reasonableness** gate, and no definition object in the package supports the
claim. Q8 was written from the verbatim `YAR-D` text instead. Had the gloss been followed the answer
would have said fault bars contribution outright — the opposite of Rule D, and it would have
destroyed the explanation of why the clause exists. Raised as **TSCR-6**.

Full record: [`QP2407_TRUE_SOURCE_REVIEW.md`](QP2407_TRUE_SOURCE_REVIEW.md).
Corpus defects: [`TRUE_SOURCE_CORRECTION_REQUESTS.md`](TRUE_SOURCE_CORRECTION_REQUESTS.md) TSCR-5..8.

---

## 7a. QP2512 — December 2025 — **LIVE ON MAIN**

Authored on `pastpapers/qp2512-founder-review` from `7e51b97`; **published 2026-08-12**.

**Integration was a reconciliation, not a merge.** `main` had moved three commits ahead of the
branch base while the paper was being written, and one of them fixed a live defect the branch would
have reverted:

| Commit | Class | Preserved |
|---|---|---|
| `a3a3003` | SECURITY / product leakage — public QB trimmed 94.7% → 50.2% | yes |
| `2f38586` | **PUBLISH-STATE** — `--publish` moved from a flag into the projection config | yes |
| `e86d26d` | DOCUMENTATION | yes |

The file that mattered was `SQ/solved-qp-sample-january-2026.html`: the branch's copy carried two
review/`noindex`/`PRICE_TBD` markers, `main`'s carried none. Integrated, it carries none **and**
gains QP2512's content delta (13 → 14 sittings). The guard is not the merge — it is that
`run_toolchain.py` was then run with **no arguments**, the exact invocation that caused the original
regression, and both sample pages stayed published.

| | |
|---|---|
| **Authored** | **All nine**, each with a verification record at `verification/QP2512/` |
| **Canonical spec** | `specs/QP2512.json` — `Pilot Review Ready`, *"Awaiting Founder Review - complete paper"*, `version 1.0` |
| **Validation** | **0 errors.** 9 warnings, all the deferred 450–650 word band (§6 item 3). **0 blocking** re-verification flags |
| **Build** | `meoclass1/pastpapers/QP2512.html` (review, `noindex`) and `solvedQP/QP2512.html` (delivery, no review banner) |
| **Determinism** | double-build **byte-identical across 91 generated artefacts** |
| **Delivery surface** | QP2512 now renders **Available** on `solvedQP/index.html`, transitioned automatically by the generated surface — no manual status edit |
| **Staging** | **RETIRED.** `staging/QP2512/` removed; its content lives in the canonical spec |
| **Merge / deploy** | **MERGED to `main` and deployed.** Founder authorised publication 2026-08-12 |
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

## 7b. SolvedQP derived layer — **ACTIVE**

Built 2026-08-12. Full architecture: [`SOLVEDQP_DERIVED_LAYER.md`](SOLVEDQP_DERIVED_LAYER.md).

| Component | Path | State |
|---|---|---|
| **Manifest** | `solvedQP/solvedqp_content_index.json` | **ACTIVE** — 28 papers, 23 available, 207 published questions, 5 planned, 3 known-absent |
| Generator | `tools/pastpapers/build_solvedqp_manifest.py` | in the toolchain, `--check` and `--self-test` |
| **Topic search** | `solvedQP/index.html`, over the manifest | **ACTIVE** — question-level, grouped by sitting, links to the anchor |
| Search tests | `tools/pastpapers/solvedqp_search_test.py` | 13 / 13 |
| **Latest updates** | `solvedQP/index.html`, from `recently_updated` | **ACTIVE** — generated; never hand-edited |
| **Daily health** | `tools/pastpapers/solvedqp_health_check.py` | **ACTIVE LOCALLY · CONFIGURED REMOTELY** — see below |
| Workflow | `.github/workflows/solvedqp-health-check.yml` | daily 03:30 UTC / 09:00 IST + `workflow_dispatch` |

**Daily email is CONFIGURED, not yet CONFIRMED.** The workflow reuses the existing Brevo secrets
`BREVO_SMTP_LOGIN` and `BREVO_SMTP_KEY`, and takes the recipient from
`SOLVEDQP_HEALTH_EMAIL_TO`, falling back to `QB_HEALTH_EMAIL_TO`, falling back to
`contactus@marineintelligenceweekly.com`. **No new secret is required for it to start reporting**,
but the first scheduled or manual run is what proves delivery. Nothing here holds a credential.

**Inventory authority.** The manifest is the only inventory. The home page, the year sheets, the
search and the health checker all assert against it; none of them builds a second list.

**Paid-text boundary.** The manifest carries printed question stems, topic labels and sitting
metadata only. `assert_no_paid_text()` fails the build on any banned key *and* on any 60-character
run of answer prose beyond the published stems. Unsolved sittings carry **no** question text, so
topic search cannot make a planned paper look solved.

> **The boundary the manifest does NOT fix.** The repository is public, so `solvedQP/QP2601.html`
> — 389 KB of paid answers — is readable unauthenticated at `raw.githubusercontent.com`. The
> middleware gates the site, not the source. This is pre-existing and unchanged by this session;
> the manifest contains strictly less than the pages already committed beside it. Recorded in
> `WRITTEN_PRODUCT_LIVE_TEST_STATUS.md`.

**Temporal handling.** The health check applies the **Written** trap ledger only. The Oral ledger
greps `A.1185(33)` and `Merchant Shipping Act, 1958`, both of which are *correct* on historical
papers; applying it would produce about a hundred false findings every morning. Forward
contamination is checked instead — answer panes only, negation-aware, and REVIEW rather than ERROR
when the sitting and the boundary share a month.

---

## 7c. Desktop batches

| Batch | Papers | Status |
|---|---|---|
| **1** | QP2401 · QP2412 · QP2402 · QP2409 · QP2411 · QP2410 | **CLOSED — 6/6 reviewed, integrated and LIVE.** Branches retained as provenance, not deleted |
| **2** | ~~QP2501~~ · ~~QP2502~~ · **QP2503** · QP2504 · QP2507 · QP2406 | **2/6 LIVE.** QP2501 and QP2502 published 2026-08-12 (§7e). QP2503 is the next desktop paper |
| **3** | QP2407 · QP2408 | held back — two papers, not three |

Board: [`DESKTOP_QP_ALLOCATION_BOARD.md`](DESKTOP_QP_ALLOCATION_BOARD.md). Batch 1's own board,
[`DESKTOP_QP_ALLOCATION_2024.md`](DESKTOP_QP_ALLOCATION_2024.md), is preserved unchanged.

**Batch 2 baseline: `main` at the QP2512 publication commit** — not `9c97359`, which predates the
publish-state fix and the whole derived layer.

Batch 2 order is fixed and one constraint is hard: **QP2507 must follow QP2501 and QP2503**, which
supply all eight of its family edges and take it from 0/9 to 8/9. The order yields 18 of 54
questions donor-ready, the proven maximum over all 720 orderings.

**Batch 1 is closed, so that gate is now open.** The desktop may start Batch 2 in the governed
order. Batch 2 branches must be cut from current `main`, which is far ahead of `9c97359`.

---

## 7d. Batch 1 corrections — what the laptop changed, and where

Every correction was made at the canonical structured layer (spec plus verification record) and the
HTML regenerated. No generated page was hand-edited.

| Question | Defect | Evidence | Status |
|---|---|---|---|
| `QP2402-Q3` | EEDI mapped to Annex VI **regulation 21**, which is *Functional requirements* | `MEPC.328(76)` chapter 4 headings read directly from the corpus copy | **fixed** — EEDI is regs 22 and 24 |
| `QP2402-Q5` | same mis-numbering, five claims | as above | **fixed** — *not in the referral* |
| `QP2402-Q6` | EEXI cited as reg 25 alone | as above | **fixed** — EEXI is regs 23 and 25 |
| `QP2601-Q1` | reg 25 labelled *Attained EEXI*; reg 25 is *Required EEXI* | as above | **fixed on a LIVE paper**, incl. the public free sample |
| `QP2511-Q8` | "MIW holds no licensed copy of the Hong Kong Convention"; scope given as *500 GT on international voyages* | `official-sources/HONGKONG_CONVENTION.pdf`, 47 pp, Article 3.3 and Article 17 read verbatim | **fixed on a LIVE paper** |
| `QP2603-Q9` | identical pair | as above | **fixed on a LIVE paper** |

**The referral was worth more than the question it named.** It named `QP2402-Q3` only. Turning it
into a corpus-wide scan for the same *class* of claim found five further defects, three of them
already published. Treat every future referral that way.

**What was deliberately NOT changed.** `QP2412-Q8`'s `regulation 22 SEEMP` search alias is correct
by design — it catches candidates searching the superseded pre-2021 numbering, and `QP2402-Q5`
teaches against exactly that. `QP2410-Q4`'s references to the wrong scope are its own warnings
against it. `QP2406`-era audit prose in `QP2402-Q6.md` describing what donor `QP2606-Q6` cites is
left verbatim: it is an audit record of another paper, and rewriting it would falsify the trail.
The remaining "MIW holds no licensed copy" statements about SOLAS, the ESP Code and ISO 484 are
untouched and unverified — they concern other instruments.

---

## 7e. Batch 2 papers 1 and 2 — QP2501 and QP2502 — **LIVE ON MAIN**

Published 2026-08-12. Desktop authored both on their own branches; the laptop reviewed each as
**candidate input** and integrated by controlled path extraction from
`origin/pastpapers/qp250{1,2}-founder-review` rather than by merging the branches, so no stale global
artefact could ride along. Desktop branches are left untouched.

| | QP2501 | QP2502 |
|---|---|---|
| Sitting | January 2025 | February 2025 |
| Desktop tip | `fb2796f` | `c04b402` |
| Publish commit | `eb3a1c5` | `a1cc735` |
| Printed serial | EM - 2501, 3 pages | EM - 2502, 2 pages |
| text_verbatim vs PDF | 9/9 faithful | 9/9 faithful |
| validate_spec | 0 errors, 0 blocking | 0 errors, 0 blocking |
| Understand reconstruction test | 9/9 pass | 9/9 pass |

**Both branched from `333e814`, so both predate the Understand standard** added at `0408d02`
(`MIW_LEARNING_METHOD_DESIGN.md` §10, `DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §10.1). Audited against it
anyway, they largely already conformed — the standard codified what the desktop was doing rather than
correcting it. **QP2503 onwards must be authored against §10.1 directly.**

### Laptop corrections

- **QP2501 Q4 and QP2502 Q4** — Understand reframed off examiner-voice (§10.1 rule 5). Two sentences
  in each; all substantive explanation preserved verbatim. No Model Answer content altered.
- **QP2501 Q1 and Q3 study notes** told a paying reader a claim was *"flagged for confirmation before
  publication"* — on a published page. The disclosure is kept; the internal workflow phrasing is not.
- **UI fixtures added for both papers** in `ui_behaviour_test.cjs`, which fails by design when a paper
  has none. Regulation probes were chosen as each paper's sharpest temporal risk: `MEPC.391(81)` for
  QP2501 (LCA guidelines edition) and `MSC.560(108)` for QP2502 (in force 1 Jan 2026, *after* that
  sitting).

### Two things worth carrying forward

**A new paper's customer-facing delivery page arrives untracked.** `solvedQP/QP####.html` is generated,
so it shows as `??` and is missed by explicit staging unless named. On QP2502 it was caught before the
commit; had it shipped, the paid page would have 404'd while the manifest advertised it. **Name it
explicitly in every future integration.**

**Two integration steps always fail first, by design.** `REUSE MAP` goes stale the moment a paper
becomes solved (re-run `build_reuse_map.py`), and `UI BEHAVIOUR` fails until the paper has a fixture.
Neither is a defect in the paper.

### Verified corpus state after both

**22 available papers · 198 published questions · 54 unsolved across 6 papers**
(QP2406, QP2407, QP2408, QP2503, QP2504, QP2507). Both papers transitioned Planned soon → Available
automatically; no manual index edit. QA at publication: toolchain and self-tests green, 121/121
security, double build byte-identical, clean at 1280 and 375, paid pages gated 302 live.

---

## 7j. QP2406 (June 2024) — laptop-reviewed and published — **BATCH 2 CLOSED 6/6**

Desktop branch `pastpapers/qp2406-founder-review` at `49e31e2`, based on `333e814`, pushed
2026-08-13 07:38 IST. Twelve files, all paper-owned, no global artefacts. Integrated onto current
`main` (`2d9435d`) by path extraction on `integration/qp2406-laptop-review`; the desktop branch was
never merged and is retained as provenance. Published at `c368d5d`.

**Product: 26 available papers · 234 published questions.** June 2024 transitioned
Planned soon → Available; July and August 2024 are the only Planned soon cards left.

**The session brief was wrong about the remote and the check caught it.** It stated the desktop had
completed QP2406, QP2407 and QP2408. `git ls-remote` showed only the QP2406 branch; QP2407 and
QP2408 have no branch and remain `Intake Complete` at 0/9. The brief also gave a stale product
count. **Fetch and derive; do not author from the brief's numbers.**

**This is the earliest sitting in the solved set**, so six of its seven donor relations travel
backward into the paper and only `QP2403-Q9` (March 2024) pre-dates it. Every whole-question donor
is later. All three tier D claims were re-verified against the corpus rather than taken on trust
and each was accurate: `Q7 ← QP2504-Q8` exact with nil delta, `Q8 ← QP2601-Q3` presentational delta
only, `Q9 ← QP2411-Q9` a substantive enlarging delta. Adding the paper made it the earliest member
of the salvage/general-average family, so `QP2601`'s recurrence note correctly re-anchored to
June 2024 Q8 — a derived change on a live page, produced by the toolchain, not by hand.

### Five corrections applied

1. **The source host was named by brand in all nine verification records** — in a public
   repository, while the same spec's `source_copy_provenance` declares host identity *"recorded
   locally only, outside this public repository"*. **No other paper in 25 does this.** A prose
   record contradicted a machine-readable declaration in the same object, and only the declaration
   was validated. Neutralised to "the host"; corpus-wide sweep found no propagation.
2. **Anchor arithmetic.** The header claimed *"8 of 9 relations travel BACKWARD"*; its own donor
   table lists seven (six later, one earlier). Corrected to 6 of 7. Same class as the four
   arithmetic defects found on QP2504 — a summary figure written before the detail was settled.
3. **Production jargon in six candidate-facing study-note blocks** ("donor", "before publication",
   "reverify"). Rewritten in candidate language. **This is the register-only subset of §7i and is
   safe to fix; the provenance-claim subset was left untouched and remains Founder-blocked.**
4. **Rule 4.** `Article 14` (Q8) and `the 2014 amendments` (Q6) removed from `understand_first`.
   `Merchant Shipping Act, 1958` (Q2) was **kept** — the year is part of the statute's name, not a
   citation. The `2014` still visible in Q6's Understand pane is in the **knowledge map**, which is
   derived from `answer_route` and is not governed by Rule 4.
5. **Trap 17, second occurrence.** A `two weeks` distance from the sitting to the SOLAS 2024
   consolidated edition, in four places. The paper prints `JUNE 2024` with no day, so the true
   distance is anywhere from one to thirty days. Restated as "the month after".

### Verification

Source verified against the printed copy independently of the desktop: 3 pages, serial `EM – 2406`,
nine questions, every limb, 16 marks each, `text_verbatim` faithful with printed errors preserved
(*"What is P&I clubs?"*, *"filling a claim"*, *"What is General Average,"*). The printed
**96-versus-100 marks anomaly** — six answered questions at 16 marks against a printed *Total Marks
100* — is recorded, not corrected. Host branding, the `dsguides` promotion, both purchase panels and
the host recurrence annotation are excluded from the transcription; the recurrence leak probes
(`2021/JULY/Q2`, `2010/NOV`, `2022/FEB/Q4`, `2023/MAR/Q9`) all return nothing from the shipped bytes.

`validate_spec` 0 errors / 0 blocking, `known_traps_check` 205/0, all toolchain stages pass with the
five positive-control stages (`REUSE SELFTEST`, `SOLVEDQP MFST ST`, `SOLVEDQP HLTH ST`,
`TEMPORAL ST`, `SURFACE ST`) firing. **120 generated files byte-identical across a double build.**
UI reviewed at 1280 and 375: nine cards, five modes, Answer pre-selected via `aria-selected`, mode
switching and anchors working, no overflow, no console errors, no review banner and no host or
provider leakage on the delivery surface. Live verified on a **public control** — the paywall is
path-agnostic, so a 302 proves nothing; `SQ/solved-qp-sample-january-2026.html` returns 200 and
reads *"26 solved papers · 234 questions"*.

**`solvedQP/QP2406.html` was untracked for the SIXTH consecutive paper** and was staged by explicit
path. `git add -u` would have shipped a manifest entry pointing at a page that does not exist.

Neither open referral is engaged: **TSCR-3 and TSCR-4 are both MARPOL Annex VI**, and no question on
this paper depends on that Annex. No new referral raised.

---

## 7h. QP2507 (July 2025) — laptop-reviewed and published — **2025 YEAR CLOSED**

Desktop branch `pastpapers/qp2507-founder-review` at `3f37176`, based on `333e814`, pushed
2026-08-13 03:58 IST. Twelve files, all paper-owned, no global artefacts. Integrated onto current
`main` by path extraction on `integration/qp2507-laptop-review` at `0a6f685`; the desktop branch
was not merged and is retained as provenance.

**This is the paper the batch order was built to produce.** QP2507 went from 0/9 to 8/9
donor-ready once QP2501 and QP2503 were solved, and the anchor confirmed the board's 8/9 exactly.
Three donors came from QP2501 (Q1 NEAR, Q2 and Q4 EXACT) and five from QP2503 (Q5, Q6, Q7, Q8
EXACT; Q9 NEAR). Q3 is the only question with no donor and was authored fresh. **Every donor is
backward** — three at −6 months, five at −4 — so no donor-direction refusal was required, unlike
QP2504's Q9. Family reach came out at **0, not the board's 8**, for the second time and the same
reason: the eight papers that emit reach are the eight the board required to be solved first.
Reach should be computed against the *unbuilt* set at the paper's turn.

**Temporally this is the easy paper, and it is provable rather than assumed.** No boundary the
paper engages moves inside July 2025. The two nearest sit outside on either side — the Hong Kong
Convention entered into force 26 June 2025, four days before the month opens, and `MEPC.385(81)`
enters into force 1 August 2025, one day after it closes. **The Hong Kong Convention is not
engaged by any of the nine questions**, so the pre-EIF donor contamination that was the flagged
risk on this paper could not arise; the sweep confirms zero occurrences. One genuine donor
re-anchoring was made and is confirmed: the January donor's *"FuelEU Maritime began to apply in
the sitting month itself"* is true of January and false of July, and was re-authored.

**The risk was in the evidence, not the calendar.** Q9's governing statute, the Merchant Shipping
Act **1958**, is not held by True Source — the corpus holds the **2025** Act instead and its own
instrument log instructs that 1958 section numbers be re-based to it. That instruction is right
for the July 2026 orals and wrong for this sitting, which predates even the 2025 Act's assent on
18 August 2025. The eight-surface reverse sweep was run: all nine shipped surfaces carry 1958, and
every mention of the 2025 Act is an explicit exclusion.

**Laptop corrections — 14, all to the canonical spec.** Rule 4: Understand now measures **zero**
regulatory citations on all nine questions, the first Batch 2 paper to do so (QP2501 carried 1,
QP2502 9, QP2503 5, QP2504 3 — the residue on QP2504 being instrument names). Removed
`MEPC.391(81)` from Q2, `SOLAS II-1/3-1` from Q8, a bare `2015` from Q1, an entry-into-force date
from Q6, and — the one that mattered — Q5's `(section 2)` and `(section 3)`, which pointed at
answer sections but sat in a paragraph about the Marine Insurance Act whose own `regulations` list
cites sections 19, 20 and 66. **The knowledge map legitimately keeps its citations on every
paper**; Rule 4 governs the concept-first prose, not the answer skeleton.

Candidate-facing language: *"the production protocol forbids"*, *"before publication"*, *"this
production line"* and the production term *"donor"* removed from study notes and one `regulations`
entry. **The provenance sentences that say what the corpus does and does not hold were left
alone** — that is a corpus-wide class, and rewriting it would change a provenance claim rather
than a phrasing. Reported, not rewritten. See §7i.

**Two True Source referrals were transcribed into the register they claimed to be in.**
`TRUE_SOURCE_CORRECTION_REQUESTS.md` held only TSCR-1 and TSCR-2; the `MEPC.328(76)` entry-into-force
error and the `MEPC.376(80)`-presented-as-current defect existed only in anchors and in this file,
although both anchors state they were *"raised as a `TRUE_SOURCE_CORRECTION_REQUEST`"*. They are
now **TSCR-3** and **TSCR-4**, both OPEN. No corpus file was touched.

**Validation.** `validate_spec` 0 errors / 0 blocking; known traps 205 checks 0 failures;
recurrence 0 failures; `run_toolchain` and `--self-test` both ALL STAGES PASS; double build
byte-identical across 65 generated artefacts; UI behaviour 66 passed / 0 failed on a new QP2507
fixture whose nine probes were derived from the built page and re-tested for within-paper
uniqueness. The delivery surface carries no production metadata, no review banner and no host
branding, with every detector controlled against the review build.

**`solvedQP/QP2507.html` was untracked for the fifth consecutive paper** and was staged
explicitly. `git add -u` would have missed it again.

---

## 7i. OPEN — corpus-provenance vocabulary in candidate-facing study notes

**Reported by the QP2507 review. Not fixed. Needs a Founder decision before any corpus-wide pass.**

Every question's final study-notes section is an *Uncertainty / evidence limits* block, and it
speaks to the candidate in MIW's internal provenance vocabulary. On QP2507 alone there are **30
instances** across all nine questions, in shipped fields:

> *"The MIW True Source corpus does not hold `MEPC.391(81)` … the corpus defect has been raised as
> a correction request rather than fixed."*
> *"The corpus holds no gender material at all."*
> *"P2 — held by the corpus"* (in a rendered table)

**Why it was not swept with the other 14 corrections.** The clearly internal phrases — *"the
production protocol forbids"*, *"before publication"*, *"this production line"*, *"donor"* — are
production jargon a candidate cannot decode, and removing them changes nothing but register. These
are different: *"the corpus holds no class rulebook"* is a **provenance claim**, and rewriting it
alters what is being asserted about the evidence, not merely how it reads. The QP2507 work order
said to report semantic ambiguity rather than rewrite it, and this is the ambiguity.

**It is corpus-wide, not a QP2507 defect.** The same construction runs through the delivery pages
of every solved paper. QP2501-Q1 and Q3 already had the narrower *"flagged for confirmation before
publication"* variant fixed (§7e), so the class is known and partly addressed.

**The question for the Founder is whether the disclosure should survive in candidate voice** —
*"no class rulebook was read for this answer, so no acceptance criterion is quoted"* — or whether
provenance belongs only in the review build. The disclosure itself is valuable and should not be
deleted; only its register is in question. **Do not start a corpus-wide rewrite until that is
decided.**

---

## 7g. QP2504 (April 2025) — laptop-reviewed and published

Desktop branch `pastpapers/qp2504-founder-review` at `aa0d8a6`, based on `333e814`, pushed
2026-08-13 00:14 IST. **Twelve files, all paper-owned, no global artefacts** — the cleanest
handover of Batch 2. Integrated onto current `main` by path extraction on
`integration/qp2504-laptop-review`; the desktop branch was not merged and is retained.

**The paper is the hardest temporal case in the batch.** Three boundaries fall *inside* the
sitting month and no examination day is printed: MEPC.400(83) and the Net-Zero Framework
approval on 11 April 2025, and `MSC-FAL.1/Circ.3/Rev.3` on 4 April 2025. The anchor discharges
all three rather than hedging — MEPC.400(83) is proved immaterial by a differential on the G3
table (the 2023–2026 rows are unchanged, so Z = 9 % governs 2025 on every day of April), the
Net-Zero Framework is prohibited outright, and Q9 is written to be correct under either
revision by naming the edition it answers on. **All three proofs were re-verified at review
against the held primary PDFs and hold.**

**One material defect was found and corrected.** Q6 asserted that the 2024 attained CII "fell
due for reporting by 31 March 2025 — **three weeks before this paper**", on seven shipped
surfaces. That is a distance measured from the examination *day* and it breaches the paper's
own governing rule that no answer may depend on which day in April the candidate sat. All
seven now read "in the month immediately before…". The same class was swept corpus-wide and
one further **live** instance was found and fixed: `QP2510-Q6` described the electronic Ballast
Water Record Book amendments as taking effect "three weeks before this examination" when
1 October 2025 is the *first day of QP2510's own sitting month* — a shipped Study Guide
statement that misclassified an in-month boundary. Recorded as **known trap 17**.

**Understand rule-4 pass.** Citations were removed from Q1 (three regulation numbers), Q4 (one)
and Q5 (two section numbers plus four colonial statute years). Understand now carries **zero**
regulation, section or article numbers across all nine questions — the first paper in Batch 2
to reach that. Four dates survive as necessary and were kept deliberately: SOLAS **1974** and
the **2017** Act name their own instruments, the CII **2019** reference line is the mechanism,
and Q9's **4 April 2025** is the entire point of its section.

**Verdict Q1–Q9:** Understand — 5 PASS, 4 MINOR (all corrected), 0 FAIL. Content completeness —
every printed limb covered, every definition complete. No answer defect was found in any of the
nine model answers.

**Corpus defect confirmed and left open.** `MEPC.328(76)` entry into force is `2022-11-01`,
read from the resolution's own operative paragraph 3 and corroborated by two further held
resolutions. Three canonical True Source records still say `2023-11-01`. The corpus was not
modified; the `TRUE_SOURCE_CORRECTION_REQUEST` stands.

**Delivery-page gate held.** `solvedQP/QP2504.html` was generated **untracked** — the same
failure as the previous three papers — and was caught by the Part 15 gate and staged explicitly
before commit. Root cause: the toolchain writes a *new* file per paper and `git add -u` only
updates tracked paths.


## 7f. Batch 2 paper 3 — QP2503 — **LIVE ON MAIN**

Published 2026-08-13 at `0816f3d` (integration commit `b4f2469`). Desktop authored it at
`2ca4aa4`; the laptop reviewed it as **candidate input** and integrated by controlled path
extraction from `origin/main`. The desktop tip is untouched. Desktop was probed three times
across the session and never moved.

| | QP2503 |
|---|---|
| Sitting | March 2025 · printed serial **EM - 2503**, 2 pages |
| Desktop tip / base | `2ca4aa4`, branched from `333e814` |
| text_verbatim vs PDF | 9/9 faithful, printed anomalies preserved |
| validate_spec | 0 errors, 0 blocking |
| Laptop corrections | 2 (both Understand) |
| Corpus propagation | 1 (QP2508-Q8) |

**The paper's signature finding, verified independently at source.** MARPOL Annex VI
regulation 24 Table 1 prints **two** phase timetables split by ship type. Containerships, gas
carriers ≥15,000 DWT, general cargo ships, LNG carriers and cruise passenger ships entered
Phase 3 on **1 April 2022**; tankers, bulk carriers, reefers, combination carriers and the
ro-ro classes on **1 January 2025**. At March 2025 Phase 2 has therefore closed on **both**
timetables — the second only ten weeks before the paper — so Q7's printed premise, "the
present EEDI framework under Phase 2", is false. The stem is preserved verbatim and
adjudicated, not corrected away. Confirmed against the corpus canonical record
`MARPOLVI_REG24.json`, which names transplanting one timetable onto the other as the unit's
most transplantable error.

### Understand audit — the first paper authored directly under §10.1

**7 PASS · 2 MINOR · 0 FAIL** on the reconstruction test. Two corrections:

- **Q5** carried `(section 2)` and `(section 3)`, referring to answer-route steps but reading
  unavoidably as sections of the **Marine Insurance Act, 1963** — on the one question whose
  verification record deliberately refuses to assert any section beyond 19, 20 and 66. The
  Understand section was manufacturing exactly the false statutory precision the Answer was
  built to avoid. Removed. Corpus sweep: **unique to this question**; QP2502-Q5's section
  numbers are genuine Admiralty Act citations and were left alone.
- **Q3** addressed the examiner as "he" on the paper's *gender-equality* question, and
  substituted exam strategy for explanation (§10 rule 5). Rewritten. The same pronoun defect
  was found in one other live paper, **QP2508-Q8**, and corrected there.

### Did §10.1 actually improve authoring? Partly — and measurably

| | QP2501 | QP2502 | **QP2503** |
|---|---|---|---|
| Understand median words | 205 | 272 | **196** |
| Range | 175–221 | 196–301 | **160–217** |
| Rule-4 breaches (dates / citations) | 4/9 | 6/9 | **5/9** |

Direct authoring under the standard produced **tighter, more consistent length** — QP2502 ran
well over the ~120–200 band the standard sets, QP2503 sits inside it with the narrowest spread
of the three — and a markedly more disciplined single-thesis opening ("one boundary", "one
sentence generates this entire answer", "four legal events happening at once"). All nine pass
the reconstruction test.

**What it did not fix is rule 4.** Dates, regulation and article numbers still appear in 5 of 9
sections, statistically indistinguishable from the two pre-standard papers. Where they are
load-bearing (Q7's temporal adjudication, Q9's commencement date) they are defensible; the rule's
own rationale — a number maintained in two places, and an Understand section that should be
sitting-independent — is nonetheless not being met. **This is the open item for the next paper.**

### Verified corpus state

**23 available papers · 207 published questions · 45 unsolved across 5 papers**
(QP2406, QP2407, QP2408, QP2504, QP2507). QP2503 transitioned Planned soon → Available
automatically. QA at publication: toolchain and both self-tests green, solvedqp_check and
coverage_check green with self-tests, 121/121 security, double build byte-identical across 52
generated files, no console errors, no overflow at 1280 or 375, live search narrows correctly,
no host or provider leakage, paid pages gated 302 live with `reason=nosession`, and the live
public sample is **hash-identical** to the local build.

### Donor readiness after QP2503 — governed model, not Jaccard

| Paper | tier D | Reach |
|---|---|---|
| **QP2507** | **8 / 9** | 0 |
| QP2504 | 5 / 9 | 0 |
| QP2406 | 1 / 9 | 0 |
| QP2407 | 1 / 9 | 0 |
| QP2408 | 1 / 9 | 0 |

**QP2507 has converted 0/9 → 8/9**, the largest readiness conversion in the corpus and exactly
what the Batch 2 board predicted for solving QP2501 then QP2503. **Five of its eight donors are
QP2503 questions** (Q5←Q5, Q6←Q3, Q7←Q2, Q8←Q1, Q9←Q9). The earlier crude Jaccard indication of
3/9 materially understated it. Governed order still puts **QP2504** next; QP2507 is the
strongest by readiness. That ordering call belongs to the Founder, not to this session.

---

## 7. Production queue — QP2512 published, nothing else authorised

> **QP2512 is live (§7a). Everything below remains the queue as recorded, not work that is
> authorised.** Do not nominate another laptop paper without the Founder.

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
