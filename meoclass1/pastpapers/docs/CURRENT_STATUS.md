# CURRENT STATUS — MEO Class I Written Questions

**Canonical restart document for the Past Written Papers product. State only.**
Last updated: 2026-08-15, after the **pre-launch consolidation** — deploy-surface minimisation,
H1 and P1 hygiene integrated, full access-matrix regression (see §1b and `history/SESSION_HISTORY.md`
§35) — on top of **QP2311 (November 2023) closing the 2023 year** (§40).
Previous entries: **QP2306** (June 2023) (§7r), **QP2308** (August 2023) at `1d55812` (§7q) and
**QP2307** (July 2023) at `569d2d2` (§7p), all 2026-08-15.
Previous entries: QP2302 (February 2023) at `734c03f` and the Annex VI dating correction at
`85fb58e`, both 2026-08-15; **QP2310** (October 2023) at §7o and **QP2303** (March 2023) at §7n,
both 2026-08-14.
See §7j for QP2406, §7h for QP2507, §7g for QP2504, §7f for QP2503, §7e for QP2501 and QP2502,
§7a for QP2512, §7b for the derived layer, §7c for the desktop batches, §1a for security.

> # QP2512 IS LIVE. THE SOLVEDQP DERIVED LAYER IS BUILT.
>
> **DESKTOP BATCH 1 IS 6/6 REVIEWED AND LIVE.** `QP2401`, `QP2412`, `QP2402`, `QP2409`, `QP2411`
> and `QP2410` were each reviewed, integrated and published **one at a time**, every one by path
> extraction onto current `main` rather than by merging its stale branch. All six desktop branches
> are **retained** as provenance evidence and were not deleted.
>
> **DESKTOP BATCH 3 IS 2/2 REVIEWED AND LIVE.** `QP2407` and `QP2408` were reviewed, integrated
> and published on 2026-08-13, both by path extraction onto current `main`. QP2408's desktop branch
> was based on `e5843b1`, which pre-dates the 2023 intake commit `e099711` — merging it would have
> silently reverted `DESKTOP_QP_ALLOCATION_2023.md`, `DESKTOP_QP_HANDOVER_BATCH3.md` and 15 lines of
> this file. Both desktop branches are **retained** as provenance evidence.
>
> **Product: 39 available papers · 351 published questions · 351 in the corpus.**
>
> # THE 2023 YEAR IS CLOSED. QP2311 (NOVEMBER 2023) IS LIVE.
>
> **QP2311 was laptop-reviewed and published 2026-08-15 (§40).** All **eleven** observed 2023
> sittings are solved — January, February, March, April, June, July, August, September, October,
> **November** and December — **99 questions**. May is `NO SITTING` on serial-gap evidence
> (printed serials run `2304 EM` → `2306 EM`, nothing at `2305`); no May sitting was invented to
> round the calendar. **2023, 2024 and 2025 are now all complete years at 11 of 11. 2026 stands at
> 6 of 11.** There is no paper left in the 2023 queue.
>
> **THE PAPER HAD NO LIVE ANSWER DONOR — 0 of 9 — AND ITS LAW AND ENGINEERING STILL HELD.** Five
> questions passed and four were corrected, and **not one correction was to the substance of an
> answer**. Every one was to what the paper said about *itself*.
>
> **`A.1184(33)` IS NOT THE ISM GUIDANCE, AND THE ERROR CAME FROM THE CORPUS.** The paper cited it
> ten times as the Administrations' implementation guidance. It is **Guidelines on places of refuge
> for ships in need of assistance**. The ISM instrument is **`A.1188(33)`** (6 December 2023),
> revoking **`A.1118(30)`** (6 December 2017) — all three read from the Organization's own published
> resolutions. `AMENDMENT_REGISTER.md` line 69 carries the wrong number, so the defect was
> **inherited**: raised as `TS-REFERRAL-QP2311-3`, corpus untouched. Because both resolutions are
> 6 December 2023, the instrument stayed one month future either way and **no legal outcome moved**.
> **A blind find-and-replace would have broken five correct papers** — corpus-wide the number is
> used *correctly* for places of refuge in 63 places (QP2304, QP2402, QP2503, QP2506, QP2507) and
> *incorrectly* as ISM guidance in 35 places (QP2306, QP2309, QP2312, QP2406, QP2502 and this
> paper). **Only this paper was corrected. The other five are OPEN — see `NEXT PROJECT` below.**
>
> **THE FALSE-HOLDINGS CLASS RECURRED FOR THE THIRD TIME, AND THIS TIME IT HID AN EXACT REPEAT.**
> Q5 said the host pointed at "a September 2022 sitting MIW does not hold and cannot read".
> **MIW holds it**: `QP2209-Q5` prints Q5 word for word, preamble and all three limbs, and
> normalises IDENTICAL. Q8 was worse — the host printed *no* hint at all, the paper said no
> transcribed MIW paper sets slow steaming, and `QP2204-Q3` (April 2022) sets the same task
> nineteen months earlier in near-identical printed words. **Only the six-year layer could see it.**
> Both are wording ancestry only; `reused_from` stays null on both because an intelligence-only
> paper carries no answer.
>
> **A `UNIQUE` misclassification that SELF-RESOLVED on graduation.** `normalise_stem` strips a
> printed `(6)` only when it matches a **declared** mark, and an intelligence-only node declares
> none — so the marked 2023 print and the unmarked 2022 print compared unequal. Graduation supplied
> the metadata and the `QP2209-Q5 + QP2311-Q5` family formed as `EXACT_REPEAT`. **Never loosen
> normalisation for this symptom**: the input was asymmetric, not the rule.
>
> **A new guard ships as a DETECTOR, not a gate.** `recurrence_check.py` gains `holdings_layer`,
> which fires only where a denial in `recurrence_adjudication` collides with a host token resolving
> to a paper MIW holds. It reported **22 hits across six already published papers** on its first
> run, so it REPORTS rather than fails — blocking would have forced a six-paper rewrite inside a
> one-paper review, or a weakened rule. It follows the PIL contract: *it flags; Claude adjudicates*.
> Proved at 1 hit against the uncorrected spec and 0 against the corrected one.
>
> **The storefront month-list guard caught its THIRD real defect**, and the 2023 line now reads
> *complete year, all 11 sittings*.
>
> **THE CORRECTION WAS THE PAPER'S ACCOUNT OF WHAT MIW HOLDS, NOT ITS LAW.** Five host recurrence
> chips were recorded as "cannot be checked, MIW holds no paper for that sitting". MIW holds every
> one of them: the six-year layer carries the complete 2021 and 2022 sittings as intelligence-only.
> `QP2212-Q1` and `QP2212-Q9` print Q1 and Q2 word for word from **December 2022**; `QP2201-Q7` and
> `QP2209-Q7` print Q3 from **January 2022**; `QP2102-Q5` prints Q8 word for word from **February
> 2021**; `QP2104-Q1` sets Q4's task in **April 2021**. Q1's earliest appearance is December 2022,
> not April 2024, and Q8 is an **exact recurrence**, not a family member.
>
> **No answer content and no tier moved**, because all of it is *wording ancestry* and none of it is
> an *answer donor* — an intelligence-only paper carries no answer. The derived six-year layer had
> already computed every edge correctly; only the authored prose was behind, which is the argument
> for computing lineage rather than asserting it. `recurrence_class` was deliberately **not** touched
> and Q4 stays `UNIQUE`: its closing words genuinely differ from `QP2104-Q1`, and normalisation is
> never loosened to force a family.
>
> **Three candidate-facing defects, all found in the RENDERED BYTES and none visible to the spec.**
> Q1 told candidates the corpus register carried `MEPC.328(76)` entry into force as `2023-11-01`
> "which is wrong" — a **`TSCR-3` disclosure that went stale mid-review** when the corpus closed the
> defect at `7441cc0`, hours after the branch was pushed. `TSCR-4` closed in the same commit. Q1 also
> carried *"re-check before publication"* and Q8 *"no MIW donor at all"* — review vocabulary
> addressed to a paying candidate. **Trap 18 fired for the third paper running**: `ISM Code
> regulation 10` at three sites; the Code has **elements and paragraphs**.
>
> **The III Code content was HELD, not corrected** — and this is the finding worth keeping. Q9 was
> authored from the **unreviewed** `QP2302-Q2` branch, before that paper's own laptop review, and
> still states the **four parts** and the correct *develop · monitor · review* strategy cycle. It
> matches the corrected live donor on every marker and the pre-review version on none.
>
> **The storefront month-list guard fired for the second time** — August solved while the 2023
> coverage line still advertised eight sittings. See §7q.
>
> **QP2307 (July 2023) IS LIVE — laptop-reviewed and published 2026-08-15 (§7p).** Eight 2023
> sittings are now solved: January, February, March, April, **July**, September, October and
> December. Three remain: June, August and November.
>
> **QP2310 (October 2023) IS LIVE — laptop-reviewed and published 2026-08-14 (§7o).** Six 2023
> sittings are now solved: January, March, April, September, **October** and December. Seven
> questions passed and **two were corrected**. Neither correction was temporal: the paper's
> handling of the **33rd Assembly boundary** — October sits two months *before* the 6 December 2023
> adoption, so Q3 rests on `A.1155(32)` and not `A.1185(33)` — was independently confirmed rather
> than repaired, and every future instrument on the paper appears only inside an exclusion warning.
>
> **The two corrections were a wrong citation UNIT and a production word.** Q9 cited the ISM Code
> as *"regulation 9"*; the ISM Code has **elements and paragraphs**, and *regulation* is SOLAS's
> unit — which the same answer uses correctly for `SOLAS XI-1/6` twelve times. Across the corpus the
> house forms outnumber it 209 to 29, **and all 29 wrong uses are in this paper (16) and `QP2412`
> (13), which is this question's own donor.** The defect was inherited with the answer. **`QP2412`
> is LIVE and still carries it** — referred, not fixed, because this session is one paper. Q7 called
> 1958 *"the standing statute trap for the whole 2023 batch"* on a rendered flashcard; **"batch" is
> a production word**, found by sweeping the rendered bytes rather than the field list.
>
> **Three claims were checked and HELD rather than corrected**, which is worth as much as the
> corrections: the **interleaved Annex VI chapter 4 numbering** (attained EEDI/EEXI at 22/23,
> required at 24/25, CII at 28) is counter-intuitive and **right**, confirmed against the corpus's
> own `mepc-328-76` nodes; the **corpus-holdings claim is accurate, not understated** — all 56
> Annex VI nodes carry controlled paraphrase and none carries `exact_text_excerpt`, so
> "citation-ready but not quotation-ready" is true, **breaking a four-review run of understatement**;
> and Q5's declared dependency on an unreviewed branch was **discharged** when QP2303 went live
> earlier the same day.
>
> **The storefront month-list guard added this session caught its first real defect on its first
> real publication** — October solved while the 2023 coverage line still advertised five sittings.
> See §7o.
>
> **QP2303 (March 2023) IS LIVE — laptop-reviewed and published 2026-08-14 (§7n).** Five 2023 sittings
> are now solved: January, March, April, September and December. The paper was judged against the
> six-year window, which found that **four of its nine questions were first printed BEFORE this
> sitting** — Q1 in April 2021, Q2 and Q3 in August 2022, Q9 in July 2021. Two questions were
> corrected: a **misdescribed CII guideline G5** on Q2 and a **misattributed UNCLOS article** on Q1.
>
> **A live defect in the historical extractor was found through this paper and fixed.** 58 stems
> across 24 papers still carried the host's own code; `HOST_HINT_RX` fixed the month at exactly
> three letters and so matched `2023/MAR/4` but neither `2021/JULY/Q1` nor `2023/JUNE/Q1`. Because
> `normalise_stem` compares printed stems for equality, `QP2306-Q1` — the verbatim reprint of this
> paper's Q1 — compared **UNEQUAL** and the April 2021 root was invisible. 71 stems are now clean,
> **0 gained any text**, and all 270 ids are preserved. See §7n.
> **THE CORPUS HAS NO UNSOLVED QUESTION LEFT.**
>
> **QP2309 (September 2023) IS LIVE — laptop-reviewed and published 2026-08-14 (§7m).** Four 2023
> sittings are now solved: January, April, September and December. The **six-year intelligence
> window** (2021–2026, 61 papers / 549 questions) was used to re-derive ancestry for the first time.
> It corrected the earliest known appearance of two questions — one of which runs **backward** past
> the sitting — and **confirmed** the paper's two "fresh research" findings against 549 questions
> rather than 279.
>
> **BATCH 4 IS OPEN AND QP2301 IS ITS FIRST PAPER — laptop-reviewed 2026-08-14, awaiting the
> Founder's publication authorisation (§7l).** It is the **first 2023 paper MIW has solved** and the
> first paper of any year to go through the Search + Updates architecture as a new arrival. The
> **2023 year surface now exists** across the product and populated itself from the manifest.
>
> **THE 2024 EXAMINATION YEAR IS COMPLETE**, and so is 2025, and so is every 2026 sitting MIW
> holds. All eleven 2024 sittings are solved and live. May is recorded as `NO SITTING` on evidence
> in all three years, not absence: the printed serial numbering runs …2504, 2506… with nothing at
> 2505.
>
> **Completion broke three gates that harvested a live example rather than building one** — the
> last `PLANNED_SOON` row and the last unsolved question both vanished. All three are fixed to
> synthesise their fixtures. See `WORKFLOW_LESSONS.md` L-B3-1.
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

## 1b. Pre-launch consolidation — deploy surface, H1, P1, access matrix — 2026-08-15

Not a paper review: a product-boundary hardening session on top of the A.1184 patch. Full record in
`history/SESSION_HISTORY.md` §35.

| | |
|---|---|
| **Deploy surface** | **CLOSED.** `.vercelignore` added. Repository root is the web root and the build is a no-op, so every tracked file was a URL. Now excluded: `specs/`, `verification/`, `docs/`, `intelligence/`, `sample/`, `known_traps.md`, the review manifest, `meoclass1/known_traps.md`, `qb_health_check.py`, `tools/`, root `docs/`, `reports/`, `engineering-reports/`, `production-system/`, `corrections/`, `.github/`, `.claude/`, `Claude skill/`, root `*.md`. **1,051 → 455 files, 143.4 → 109.5 MB.** The review tree `meoclass1/pastpapers/*.html` is still shipped on purpose (H2 pending) |
| **CLI safety** | The Vercel CLI (`getVercelIgnore`, v58.11.0) reads `.vercelignore` + fixed defaults and **never `.gitignore`** — so a workstation deploy was already uploading git-ignored classes. `.vercelignore` now carries every `.gitignore` pattern verbatim; `tools/security/deploy_surface.test.mjs` fails if the two drift and plants a synthetic sentinel in each ignored class. 86/86; cross-checked once against the real `ignore` library over 1,071 paths, 0 disagreements |
| **H1** | Consumed desktop `prelaunch/pastpapers-index-hygiene` (`9ae7075`) — three builder files as authored, manifest regenerated from current specs. Served manifest is now an **allowlisted projection**; internal-field hits 3,749 → 25 (policy prose + "foundering"); 3.72 → 2.47 MB. Self-test 10/10 incl. future-field negative control |
| **P1** | Consumed desktop `prelaunch/p1-hygiene-remediation` (`d5f0dc8`) — 40 authored files applied cleanly, 26 generated pages regenerated. Completed the same classes where the branch stopped: 5 rendered `known_traps.md` / protocol filenames and 3 `regulations[]` TSCR-3 entries. Delivery output now **0** for `known_traps.md`, TSCR, `.md`/spec-`.json` filenames, verification paths, commit hashes |
| **Access matrix** | 284/284 (198 + 86). Oral-only **denied** on `/meoclass1/pastpapers/` and `/solvedQP/`; Written-only denied on Oral; lapsed → `expired`; live trial allows, expired trial denies, paid beats expired trial; evicted, forged `miw_auth`, store-down all deny. Live probes: case-variant paths 404, traversal normalised and gated |
| **Invariants** | 39 papers / 351 questions, 2023 11/11, prices ₹1,499 / ₹899 / ₹1,500, Terms, trials, entitlement code **byte-identical** (`routes.js`, `middleware.js`, `products.js`, `entitlements.js`, `trial.js`, `session.js`) |
| **Determinism** | 149 artefacts byte-identical across two full publish builds; toolchain ALL STAGES PASS; `delivery_gate --strict --verify-derivation` PASS |

**Open, recorded, not fixed here:** H2 (39 review pages render `UNGATED REVIEW COPY` to
SOLVED_QP holders) and H3 (the Oral-gated Written sample renders the same tag) — desktop's
review-tree measurement had not landed, so no retirement; the 44 delivery pages carry an invisible
`<!-- GATE SCRIPT STRIPPED FOR REVIEW COPY -->` comment (template, P3); two HTML/JS comments on
`SQ/index.html` and `SQ/trial.html` say "Founder" (P3); `surface_impact.py` route classifier
disagrees with route policy on some surfaces (P3 governance debt); the Oral `qb_health_check`
reports 66 files with pre-existing errors, unchanged by P1.

---

## 2. Corpus state

Recomputed from the generated manifest `solvedQP/solvedqp_content_index.json` after QP2407 and
QP2408 were reviewed and published on 2026-08-13. Not carried forward from a previous handover.

| | |
|---|---|
| **Corpus** | **252 questions / 252 solved / 0 unsolved** — **100 per cent solved** |
| **Papers** | 28 — **28 solved**, 0 answerless intake |
| **Years** | 2024 (11 papers), 2025 (11), 2026 (6). May is absent from the source set in all three years |
| **Tier D (frozen intake field)** | **3** of the 72 unsolved, down from 17. Batch 1 consumed most of the pool. **Do not plan from this number** — it is the frozen intake field, and Batch 1 proved again that it goes stale: `QP2401-Q9` was frozen at tier C and derived to D, and `QP2410`'s board was wrong in both directions. The derived tier from `build_reuse_map.py` governs, and it is what makes the Batch 2 ordering constraint (`QP2507` after `QP2501` and `QP2503`) real |
| **Delivery** | `solvedQP/` — **28 papers, 252 questions, 3 year sheets, 1 index** |
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
| `pastpapers/qp2308-founder-review` | `7bad669` | QP2308 — **integrated to `main` by path extraction 2026-08-15; retained as provenance, never merged** |
| `pastpapers/qp2306-founder-review` | `4811f3d` | **QP2306 (June 2023) — NEXT IN THE QUEUE**, unreviewed |
| `pastpapers/qp2311-founder-review` | `9e2019a` | QP2311 (November 2023) — unreviewed; the last 2023 sitting |
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

## 7s. A.1184(33) ISM-guidance correction — **A LIVE CORRECTNESS PATCH ACROSS FIVE PAPERS, NOT A PAPER REVIEW**

**Published 2026-08-15. No paper, question, coverage, price, Terms or trial state moved: 39 papers /
351 questions, 2023 complete at 11/11, combined universe 61 papers / 549 questions — all unchanged
and proved unchanged, the six-year build, the reuse map and the solvedQP home all byte-identical to
`origin/main`.**

### The three resolutions, read at source

| Resolution | Subject | Adopted | Revokes |
|---|---|---|---|
| `A.1184(33)` | Guidelines on places of refuge for ships in need of assistance | 6 Dec 2023 | `A.949(23)` (op. para 4) |
| `A.1188(33)` | **2023** Guidelines on implementation of the ISM Code by Administrations | 6 Dec 2023 | `A.1118(30)` (op. para 5) |
| `A.1118(30)` | **Revised** Guidelines on the implementation of the ISM Code by Administrations | 6 Dec 2017 | `A.1071(28)` (op. para 5) |

The title the corpus attaches to `A.1184(33)` — *Revised guidelines on implementation of the ISM
Code by Administrations* — is **`A.1118(30)`'s title**. A correction that changes only the number
leaves the title wrong, which is why every corrected site was re-authored rather than swapped.

### The reported scope was wrong in composition, and re-deriving it was the whole job

The brief reported 35 incorrect uses across `QP2306`, `QP2309`, `QP2312`, `QP2406` and `QP2502`, and
63 correct uses elsewhere. Classifying all **115 canonical occurrences** by context gave a different
picture:

| Class | Sites | Papers |
|---|---|---|
| **Correct** — places of refuge, untouched | 76 | `QP2304` `QP2402` `QP2503` `QP2506` `QP2507` |
| **Correct** — naming the corpus defect, untouched | 8 | `QP2311` (3) `QP2312` (4) and one in `QP2309` |
| **Wrong** — consumed as ISM guidance | 27 | `QP2406`-Q5 (5) · `QP2502`-Q1 (8) and -Q3 (14) |
| **Stale** — a settled question still framed as unresolved | 4 | `QP2309`-Q7 |
| **Wrong by implication** — "an ISM-related 33rd Assembly resolution" | 1 | `QP2306`-Q4 |

**`QP2312` needed no change at all** — every statement in it already matched primary source, and it
is left alone. `QP2309` had the law right and only the framing stale. **Only two papers ever shipped
the wrong citation to a customer.**

### Temporal correctness came before the citation

`A.1188(33)` is operative only from 6 December 2023, so a blind number swap would have
forward-contaminated every 2023 paper. Per sitting:

| Paper | Sitting | Was | Correct as at sitting | Later instrument | Sites |
|---|---|---|---|---|---|
| `QP2306`-Q4 | June 2023 | "an ISM-related 33rd Assembly resolution" = `A.1184(33)` | **`A.1118(30)`** (6 Dec 2017) | `A.1188(33)`, six months future | 1 |
| `QP2309`-Q7 | Sept 2023 | law right, framing stale | **`A.1118(30)`** | `A.1188(33)`, three months future | 4 |
| `QP2312`-Q5 | Dec 2023 | already correct | n/a — not cited | n/a | 0 |
| `QP2406`-Q5 | June 2024 | `A.1184(33)` as ISM guidance | **`A.1188(33)`** (operative 6 months) | — | 5 |
| `QP2502`-Q1/Q3 | Feb 2025 | `A.1184(33)` as ISM guidance | **`A.1188(33)`** (operative 14 months) | — | 22 |

**32 canonical field edits. Rendered: 26 sites on the paid pages, plus one search-payload token.**
`QP2306` and `QP2312` render nothing — their occurrences are in `temporal_review` and
`verification_status`, which are review-facing by design.

### `QP2502`-Q3 was also over-claiming its holdings

Its `sources` recorded a **P1 PRIMARY VERIFIED (corpus holding)** citing the corpus path
`03-imo-instruments/ISM-Code/_base-and-amendments/A.1184(33).pdf`. That PDF is the places-of-refuge
resolution, so the claim was wrong twice over, and the path was internal vocabulary on a paid page.
The corpus holds **neither** `A.1188(33)` nor `A.1118(30)`; the answer now says so.

### The corpus is not corrected, and the referral named the wrong surface

Inspected at corpus `origin/main` `7441cc0`: both `AMENDMENT_REGISTER.md` line 69 **and**
`ISM-Code/INSTRUMENT_LOG.md` line 19 still carry the wrong attribution.
**`TS-REFERRAL-QP2311-3` named only the register.** The instrument log is the surface `QP2502`-Q3
actually consumed. Promoted to **`TSCR-9`** in `TRUE_SOURCE_CORRECTION_REQUESTS.md` naming all three
objects, including the misfiled PDF. **Status OPEN.**

### Trap 19, and two probes that could never fail

`known_traps.md` trap 19 is `GREP: SKIP` because no phrase match is safe in either direction — the
citation is correct in five papers and the sentences correcting it must name the ISM Code to deny
it. The structural guard in `known_traps_check.py` reads context: an ISM marker within 300
characters, with no places-of-refuge marker to disarm it. **Positive control: `QP2502`-Q3's shipped
wording. Negative control: `QP2507`-Q9's correct citation and a correcting sentence.** Both hold.

Correcting `QP2502`-Q3's search alias made the `QP2404` fixture probe `a.1188(33)` non-unique, and
checking that exposed `a.1184(33)` → `QP2506-Q3` as **never** having been unique — four cards carry
it. Both re-scoped to unique token-AND pairs and proved against the real payloads.

---

## 7r. QP2306 (June 2023) — laptop-reviewed and published — **THE SAME DEFECT, THE SECOND PAPER RUNNING**

**Published 2026-08-15 at `3962292`, on top of the QP2407 Rule VI correction at `1230f43`.**
Printed serial `2306 EM` · `(India 2023)` · 2 pages · 9 questions · marks printed on Q3, Q4, Q7 and
Q8 only, so six answered questions total **96 against the printed 100**, recorded and not repaired.
**Q2, Q3, Q5, Q6 and Q8 PASS. Q1, Q4, Q7 and Q9 CORRECTED.**

**Product: 38 papers / 342 questions. Graduation proved: solved 37 → 38, intelligence-only 24 → 23,
combined universe 61 papers / 549 questions UNCHANGED.** 2023 reaches ten sittings of eleven;
**only November remains.**

### The source work needed nothing

The `(Ill)` misprint in Q5 limb (iii) — capital I, two lower-case L's — is preserved in
`text_verbatim` *and* named in the subpart. Q4's stem is correctly rejoined across the page break
with the host's intervening marketing block excluded. Both halves were traced to the source text
layer independently. **This is the QP2303-Q5 lesson applied before it was asked for.**

### Three of the four corrections are ONE defect, and it is now a two-paper streak

§7q recorded five host chips wrongly marked *"MIW holds no paper for that sitting"*. **QP2306
carried three more of the same class.**

| Q | Asserted | Truth |
|---|---|---|
| **Q9** | host hint `2022/OCT/Q7` points at "a paper MIW **DOES NOT HOLD AND HAS NEVER TRANSCRIBED**" | `QP2210-Q7` is held, transcribed, and **verbatim identical**. The governed classifier independently returns **`EXACT_REPEAT`**, `first_seen` **October 2022**. `recurrence_class` was `topical_family`; it is now `exact_recurrence` |
| **Q1** | "**only** the March 2023 entry corresponds to a question MIW has transcribed" | **Three do.** `QP2104-Q2` (April 2021) and `QP2210-Q9` (October 2022) are both held and verbatim identical. The family is **six members rooted at April 2021**, not one at March 2023 |
| **Q4** | "MIW holds no licensed SOLAS text" — at **7 sites, live in candidate-facing `study_notes`** | **SOLAS 2024 is held**: three official PDFs, **555 of 556 pages with an extractable text layer**. The authoring choice was right; the reason was false. Corrected to the real limitation — **the held edition post-dates a June 2023 sitting** |

**No answer content moved on any of them, and no tier moved.** `reused_from` stays `null` on Q9
because `QP2210` is unsolved and carries no answer to inherit. That makes QP2306 the corpus's
sharpest illustration of the distinction: **an exact printed recurrence whose answer had to be
authored from nothing.**

### Both misses were mechanical, so both root causes are on the record

**Q9 — a search-scope error, and the more general one.** Five targeted searches were run on
*air cavity*, *microbubble*, *micro bubble*, *skin friction* and *texturing*, and all five came back
empty. They were run over the **solved answer corpus** and not the **six-year intelligence layer**.
**An empty result there means the subject has no built ANSWER. It never means the subject has no
PRECEDENT.**

**Q1 — a transcription artefact that hid the evidence.** `host_recurrence_hint` had been recorded
across the source's line breaks with the tokens shifted by one — `"2015"`, `"AUG 2015"`, `"NOV 2017"`,
`"OCT 2021/APR/Q2"` — so two held ancestors were buried inside a token no reader could resolve.
Re-parsed to the printed tokens.

### Q7 was the hardest question and its law was already right

Stem **verbatim identical** to `QP2412-Q8` (December 2024), across eighteen months, and four
statements reverse: guidelines edition, GHG strategy, CII rating experience, and the state of the
short-term-measure review. All four are correctly reversed. `MEPC.377(80)` (7 July 2023, **one month
future**) appears **only as an exclusion**; the SEEMP sits at **regulation 26** from **1 November
2022**; the guidelines are **`MEPC.346(78)`**; **no ship has been rated**. Q8, from the *same*
December 2024 paper, needed **no** reversal at all — the pair is the argument for computing a
temporal delta rather than inferring it from how settled a subject feels.

### A True Source referral is perishable — verify it at review time, not authoring time

**`TSCR-3` and `TSCR-4` are both CLOSED**, corrected upstream at corpus commit **`7441cc0`** on
2026-08-15. The register now reads **`2022-11-01`**. QP2306 shipped *"TSCR-3 remains OPEN and is
re-reported, not repaired"* — accurate when the branch was pushed, stale when it was reviewed.
**Second consecutive paper on which a referral went stale mid-flight.** The substance never moved:
the date came from `MEPC.328(76)` operative paragraph 3, not from the register. Both are now marked
closed in `TRUE_SOURCE_CORRECTION_REQUESTS.md`, with two facts kept: the wrong value had been
**denormalised across 60 files and 251 occurrences** including the resolver layer QP tooling
consumes, and `2023-11-01` is the legitimate *deemed-acceptance* date of `MEPC.361(79)` and
`MEPC.362(79)`, which **must never be swept into a find-and-replace on that date**. `TSCR-4`'s log
entry is fixed but **`MEPC.391(81)` is still not held**, so LCA is citation-ready and not
quotation-ready.

**"Held" is not one fact.** Q7's Annex VI limitation survives with better words: the **MARPOL
consolidated 2022 edition and Annex VI 5th ed. 2023 ARE held**, but both are **image-only with zero
text layer**, so held is not quotation-ready. Measured, not assumed.

### A defect the builders caught and `validate_spec` does not

QP2306's `source_copy_provenance` was missing `pages` and `printed_serial`, which **crashed
`build_reuse_map.py`** with `KeyError: 'pages'`. It is the **same intake omission previously recorded
on QP2303**, and `validate_spec` requires neither field. Restored from the source: 2 pages,
`2306 EM`.

### Main moved mid-review, and the donor was wrong while the recipient was right

`main` advanced `d17fcca → 1230f43` during the review — the **York-Antwerp Rules 2016 Rule VI**
salvage correction on `QP2407-Q8`, which is one of QP2306-Q3's two donors. That commit's sweep could
not have covered QP2306, so Q3 was re-checked against it: it carries **no** "particular charge", no
SCOPIC misplacement, treats **salvage as allowable in general average**, and names all three YAR
editions while insisting the contract selects. **Q3 had not inherited the donor's defect and
independently corroborates the correction.** Rebased and every generated artefact regenerated;
generated conflicts were resolved by **regeneration, never hand-merging**.

### Gates

Publish-mode toolchain **ALL STAGES PASS** · `delivery_gate --verify-derivation --strict` **PASS** ·
`known_traps` **314 checks, 0 failures**, no ISM "regulation" defect in any form · `health_check
--publish` **0 errors** while the bare invocation reports **81**, which is the **proof of build
mode** and not a regression · double publish build **byte-identical across 111 artefacts** ·
UI fixture authored, **66 assertions pass** · storefront guard caught the counts **and** the 2023
month list, page updated not checker, **pricing unchanged** · delivery bytes swept clean (the 87
`branch` hits are the knowledge-map CSS classes `kmap-branch`/`branches-hidden`) · paid route 302s
anonymously with **zero paid prose**, and because that 302 is path-agnostic the deploy was proved
from the **public** surfaces instead: `data-solvedqp-papers="38"`, `342`, June in the live 2023 list.

**Untouched papers are byte-identical to `main`.** Exactly six moved — `QP2301`, `QP2303`, `QP2309`,
`QP2404`, `QP2409`, `QP2412` — and every one shares a family QP2306 joined. `QP2412-Q7` moved from
*"Once in this set"* to *"Repeated — reworded"*, the model independently confirming the Q8 recurrence.

### Reported, not rebuilt — and now worth building

`recurrence_check.py` guards the **host-token provenance boundary** and passes cleanly. It does
**not** reconcile a spec's authored `recurrence_class` against the class the governed model computes,
which is exactly why Q9 could ship as `topical_family` while the model said `EXACT_REPEAT`. With the
false-not-held claim now on **two consecutive papers**, a narrow deterministic guard is warranted:
**assert that no spec asserts non-holding of a paper present in the intelligence layer, and that an
authored `recurrence_class` does not contradict the derived family class.** Not built here, per
invariant 7 — the paper is fixed and the checker belongs to the session that owns it.

---

## 7q. QP2308 (August 2023) — laptop-reviewed and published — **THE ANCESTRY THE CORPUS COULD SEE ALL ALONG**

Published to `main` at `1d55812`, 2026-08-15. **37 papers · 333 questions.** Integrated by path
extraction of 12 paper-owned files onto current `main`; the branch was cut from `bc1be86` and
predates four integrated papers, so a merge would have presented them as deletions.

**Source.** `2308 EM`, August 2023, two pages, nine questions, SHA-256 `9082fed7…` re-verified.
**No printed marks anywhere** — like January and February 2023, unlike September. Eleven printed
anomalies preserved, including the lowercase-L `loT` glyph, Q5's first clause with no main verb, and
three different limb conventions on one paper.

**Q1–Q9: nine PASS, three corrected in candidate-facing text.** No question's law changed.

### The under-read, and why it matters more than a wrong citation would

Five times the branch recorded a host recurrence chip as *"cannot be checked — MIW holds no paper for
that sitting"*. **MIW holds every one of them.** The six-year layer carries the complete 2021 and
2022 sittings as `INTELLIGENCE_ONLY`:

| Q | Chip dismissed | Actually held | Result |
|---|---|---|---|
| Q1 | `2022/DEC/Q1` | `QP2212-Q1` | word for word — earliest is **December 2022**, not April 2024 |
| Q2 | `2022/DEC/Q9` | `QP2212-Q9` | word for word — earliest is December 2022 |
| Q3 | `2022/JAN/Q7`, `2022/SEP/Q7` | `QP2201-Q7`, `QP2209-Q7` | word for word — earliest **January 2022** |
| Q4 | `2021/APR/Q1` | `QP2104-Q1` | same task, closing words differ — **not new** |
| Q8 | `2021/FEB/Q5` | `QP2102-Q5` | word for word — **EXACT recurrence** from February 2021 |

**Nothing downstream moved, and that is the point.** Every edge is *wording ancestry*; none is an
*answer donor*, because an intelligence-only paper carries no answer. Q4 stays tier A, Q8 tier C.
**The derived layer had already computed all of it** — `EXACT_REPEAT` first seen February 2021 for
Q8, December 2022 for Q1 and Q2, `NEAR_REPEAT` January 2022 for Q3. Only the prose was behind.

`recurrence_class` was deliberately **not** changed: it records authoring-time corpus state, is never
rendered, and rewriting it would misstate what was true when the question was built. **Q4 remains
`UNIQUE` in the six-year layer and that is correct** — it ends *"the salient points and trend
analysis"* against `QP2104-Q1`'s *"the salient points, which will enable trend analysis"*. A genuine
examiner rewrite. Normalisation was not loosened to force a family.

### Three candidate-facing corrections, all found in the rendered bytes

1. **A disclosure that went stale mid-review.** Q1 told candidates the corpus register recorded
   `MEPC.328(76)` entry into force as `2023-11-01` *"which is wrong (a defect we have raised against
   our own source register)"*. The corpus **closed that defect at `7441cc0`** on 2026-08-15, hours
   after this branch was pushed — 251 occurrences across 60 files, including the resolver layer QP
   tooling consumes. Rewritten to the settled position: **in force 1 November 2022**, deemed accepted
   1 May 2022, from operative paragraph 3. **The date used in the answer never changed.** `TSCR-4`
   closed in the same commit and does not bite an August 2023 sitting, where `MEPC.376(80)` genuinely
   *is* current. **A referral is a perishable claim: it must be re-checked at integration, not
   carried.**
2. **Review vocabulary addressed to a paying candidate.** *"re-check before publication"* (Q1) and
   *"no MIW donor at all … the least internal corroboration"* (Q8). Substance kept word for word;
   only the nouns moved. The branch's own sweep reported *"zero occurrences"* — it swept the field
   list, not the rendered page.
3. **Trap 18, for the third paper running.** `ISM Code regulation 10` at three sites. The ISM Code
   has **elements and paragraphs**; *regulation* is SOLAS's unit. Corrected in the spec, the
   verification record and the anchor.

### Held rather than corrected — worth as much as the corrections

- **The III Code content is right, and it was derived independently.** Q9 was authored from the
  **unreviewed** `QP2302-Q2` branch, *before* that paper's laptop review corrected it, and
  nonetheless states the **four parts** and the correct **develop · monitor · review** strategy
  cycle with promulgation kept separate. It matches the corrected live donor on every marker and the
  pre-review version on none. **A donor's status is evidence, not authority — and here the producer
  beat its own donor.**
- **The 33rd Assembly reversal is intact.** `A.1185(33)`, `A.1186(33)`, `A.1187(33)` and
  `A.1188(33)` appear **only** inside exclusion or trap frames; `A.1155(32)`, `A.1156(32)`,
  `A.1157(32)` and `A.1118(30)` are used throughout.
- **Q7 keeps the Hong Kong Convention live and unresolved** — conditions satisfied June 2023, the
  twenty-four-month clock running, *"It is not in force today."* Donors 22 months later did not leak.
- **Q6's delta from `QP2303-Q5` was settled at source.** March 2023 genuinely prints *"the ship
  transformed"* without *is*, so `NEAR` is right.
- **The producer's own mobile fixes were confirmed by measurement**, not accepted: Q4's chart 287px
  and Q5's table 283px inside a 347px card at 375px, zero clipping.

### Gates

Toolchain **ALL STAGES PASS in publish mode** · delivery gate `--verify-derivation --strict` **PASS**
· `health_check --publish` **0 errors** · double build **byte-identical across 94 artefacts** ·
UI fixture authored, nine probes **proved unique** against the real card payloads under the search's
own token-AND semantics, **64 assertions pass** · zero internal-vocabulary leaks in the shipped bytes
· paid route bounces anonymous access to `/SQ/pay.html` with no paid prose served.

**A checker with a mode flag can report green in the wrong mode.** `health_check.py` asserts *review*
state bare and *publish* state with `--publish`, so whichever build the tree holds, one invocation
always returns 0 errors. A review-mode toolchain run left 37 pages carrying `noindex` and production
metadata while the bare checker reported clean. Only comparing against what `main` actually commits
exposed it. **`run_toolchain.py --publish` is the pre-commit gate; the bare run is not.**

**Graduation:** solved 36 → **37**, intelligence-only 25 → **24**, combined universe **61 papers /
549 questions unchanged**. The thirteen other paper pages that moved are **exactly** the members of
the families QP2308 joined — no collateral drift.

**Storefront:** the month-list guard fired for the second time — August was solved and delivered
while the 2023 coverage line still advertised eight sittings. The page was updated, never the checker.

**Referred, not fixed.** `QP2303-Q5` is **live** and its `subparts` silently repair the printed
grammar twice — *"the ship **is** transformed"* and *"and **the** typical objectives"* — where the
March 2023 copy prints neither. `text_verbatim` is faithful on both sides, so QP2308's lineage is
unaffected. Printed defects are preserved, never silently repaired.

---

## 7p. QP2307 (July 2023) — laptop-reviewed and published — **A PRESERVED MISPRINT, AND THE EDGE THAT BEATS IT**

Desktop branch `pastpapers/qp2307-founder-review` @ `9f8bf0c`, based on `a633e97`, pushed
2026-08-14 17:19 IST. Twelve files, all paper-owned, one commit. Integrated by **path extraction**
onto `main`; the branch was never merged and is retained as provenance. Its tip did not move during
the review. **`main` DID move** — `85fb58e` landed mid-review and is reconciled below.

**Product: 36 available papers · 324 published questions.** July 2023 transitioned to Available
automatically.

### Source — verified independently from the printed copy

`2307 EM`, July 2023, `(India 2023)`, 2 pages, **9 questions counted by reading**, `Total Marks –
100`, `Answer SIX questions only`. **Q3 alone prints `Q3):`** — the closing parenthesis is why an
extractor anchored on a `Q<n>.` pattern under-reads this paper by one. **Four questions print no
mark figure at all** (Q6, Q7, Q8, Q9), the highest count in the 2023 intake; each is recorded at 16
on the equal-marks rubric and **no limb split is inferred** — in particular Q7's `(6)(5)(5)` from
its March 2025 recurrence is deliberately not imported. The printed defects survive in
`text_verbatim`: `vis-a-vis`, `Scavenge Air Moisturizing`, `with respect seaworthiness`, and Q9's
opening curly quotation mark closed by a straight one.

### Q1–Q9 — seven PASS, two CORRECTED

**C1 — Q4, the burden of proof on an undue detention is on the COMPLAINANT.** The answer said it
"rests on the shipowner". **Standard A5.2.1 paragraph 8** was read in the held MLC text: *"If a ship
is found to be unduly detained or delayed, compensation shall be paid for any loss or damage
suffered. The burden of proof in each case shall be on the complainant."* **Standard A5.1.4
paragraph 16** says the same for the wrongful exercise of an inspector's powers. In an answer whose
whole subject is the seafarer's *complaint*, naming the shipowner as the burden-bearer is both
non-textual and confusing.

**C2 — Q4, the Code amendment procedure is Article XV, not Article XIII.** Read at source:
**Article XIII** establishes the committee that keeps the Convention under review — the Special
Tripartite Committee; **Article XIV** is amendment of the Convention; **Article XV** is *"The Code
may be amended either by the procedure set out in Article XIV or … in accordance with the procedure
set out in the present Article."* The substance was right and the article number was wrong — the
"correct citation carrying the wrong content" failure mode. The delivery page now renders
`Article XV`, and no `Article XIII` reaches a candidate surface.

**C3 — Q9 asserted an unverifiable universal negative, across ten sites.** *"The Act that eventually
replaced it did not exist in any form at this date"*, supported by *"the Merchant Shipping Bill,
2024 was not introduced in the Lok Sabha until 10 December 2024"*. **Nothing MIW holds supports
either claim.** The corpus's own instrument log for the 2025 Act records assent **18 August 2025**,
commencement **15 March 2026** — and says nothing about a Bill. All ten sites now state the held
chronology instead: roughly thirty-two months after this sitting. The operative conclusion — the
1958 Act governs — never moved.

### Three internal leaks, found by sweeping the RENDERED BYTES

- **The private corpus commit hash reached sixteen candidate-facing fields.** `319524c` is a git
  identifier of a **private** repository and means nothing to a paying candidate. **No live paper
  carries one**, so this paper would have introduced the class. The disclosure is kept; the hash is
  gone.
- **"the 2023 batch"** — scheduling vocabulary, the same class as the `QP2310-Q7` flashcard. One
  further live instance on another paper is **referred, not fixed**.
- **"not repaired from this branch"** — production vocabulary, twice.

**The nil is a searched nil.** Seeding all three back into the built page makes the sweep fire; the
clean page reports zero on both surfaces.

### The Q4 lineage defect — it resolves itself, and no classifier was touched

The six-year layer classified `QP2307-Q4` **UNIQUE, singleton**, despite nine host-annotated prior
sittings. The mechanism was located, and it is not a classifier fault:

> An **INTELLIGENCE_ONLY** ghost carries no `reused_from` edge, so it can join a family **only** by
> exact normalised-stem equality. This sitting prints `Complaint`; February 2023 preserves the
> misprint `Compliant`. **One letter**, similarity 0.991, and the equality fails.

Once the paper is solved, graduation drops the ghost and the **adjudicated** `reused_from` edge to
`QP2302-Q8` does the work the stem cannot. Proved by building the layer twice:

| | class | size | members |
|---|---|---|---|
| before | `UNIQUE` | 1 | `QP2307-Q4` |
| after | `NEAR_REPEAT` | **4** | `QP2211-Q3` (Nov 2022) · `QP2302-Q8` · `QP2307-Q4` · `QP2407-Q6` |

**No narrow fix was made and none was needed** — which is the right outcome, because any
normalisation loose enough to equate `Complaint` with `Compliant` would risk collapsing genuinely
different families.

> **OPEN, REPORTED NOT FIXED — `QP2201-Q4` (January 2022) is a false `UNIQUE` that does NOT resolve
> itself.** Its stored stem reads *"Detainable deficiencies. **2** d) Grievance Redressal…"* — a
> bare page number swept in **mid-stem** across the page break. The span rules added during the
> QP2303 repair catch that artefact at the **end** of a stem, not in the middle. It will stay a
> singleton until January 2022 is solved. It is intelligence-only, so **no customer sees it**; and
> correcting a historical `text_verbatim` to make classification pass is what the source-fidelity
> rule forbids. The fix belongs in the extractor, as a mid-stem span rule.

### July 2023 and the 7 July GHG boundary — assessed, and it does not bite

**MEPC 80 sat 3–7 July 2023** and adopted the 2023 IMO GHG Strategy on 7 July. The paper prints
`JULY 2023` and **no day**, so the sitting cannot be placed on either side — and it does not need
to be. No stem concerns GHG ambition. The two places the window could have reached were checked:
**Q3**, where any claim about "the most recent MEPC session" would be day-dependent — the answer
makes none, resting on `MEPC.328(76)`, in force 1 November 2022; and **Q7**, where MEPC 80 revised
the biofouling guidance inside the window — the answer names **no edition, no year and no resolution
number** for it, so every statement is true on either side of 7 July. **No hedge was written and no
7 July problem was manufactured.**

### `main` moved mid-review, and it closed a claim this paper was making

`85fb58e` landed during the review and dated the revised Annex VI from `MEPC.328(76)`'s own
operative paragraph, recording that **TSCR-3 was corrected in the corpus** at corpus commit
`7441cc0`. QP2307-Q3 was telling a candidate that the corpus register defect was **live**. The
desktop's own `reverify_before_publication` entry said, in terms, *"BEFORE PUBLICATION, confirm the
register has been corrected or that the declared discrepancy still stands"* — and this is
publication. Seven sites now cite **the resolution** as the authority for 1 November 2022, which is
where the date should have come from, and record the register value as corrected at source. The
substantive date never moved. Rebased onto `85fb58e`; the only conflict was a **generated** file and
it was resolved by regenerating, never by hand-merging.

### UI fixture — authored, eighteen probes proved

QP2307 had none, which failed the suite on both surfaces. Every probe was proved unique against the
real card payloads under the search's **token-AND** semantics before it was written down — the
assertion uses `includes()`, so a probe reaching two cards still reports green. The paper's
collisions are unusually strong: it prints **two** collision questions and **two** Merchant Shipping
Act questions, so `collision` reaches two cards, `detention` three and `merchant shipping act`
**six**. None is used. Aliases were checked against the visible text with **tag boundaries treated
as hard breaks** — an earlier pass reported false positives because the segment began mid-tag and
swept the `data-search` payload back in. `23 december 2024` is the regression sentinel: it guards
the one boundary that can actually be crossed here, because the corpus holds **both** MLC editions
in one folder and the 2022 set is inapplicable at this sitting. **66/66 on both surfaces.**

### The storefront month-list guard fired for the second time

> `2023 coverage omits July -- solved and delivered, but the customer is not told they get it`

The storefront also still advertised **35 papers / 315 answers**, and its `<meta>` description was
staler still at **33 / 297**. All corrected; months are derived from the specs and never typed into
the checker.

### Intelligence graduation — proved, not asserted

| | solved | intelligence-only | combined |
|---|---|---|---|
| before | 35 papers / 315 q | 26 papers / 234 q | **61 / 549** |
| after | **36 / 324** | **25 / 225** | **61 / 549** |

Solved **+1**, intelligence-only **−1**, combined **unchanged**. **No record was hand-deleted.**

### Verification

`validate_spec` **0 errors**, 13 warnings (9 the Founder-deferred word band, 4 `no P1`).
`run_toolchain --publish --strict` **ALL STAGES PASS**. `delivery_gate --verify-derivation --strict`
**PASS**. `health_check --publish` **0 errors, 0 warnings**. Determinism **byte-identical across 94
artefacts** over two full builds, product **and** six-year, re-proved after the rebase. Security
**198/198** across six suites, unchanged. UI **66/66** on both surfaces. Visual at **1280 and 375**:
9 anchors · 5 modes · no horizontal overflow · **no console output** · all four corrections rendered
· zero internal vocabulary in visible text. `solvedQP/QP2307.html` was untracked and was staged by
explicit path.

---

## 7o. QP2310 (October 2023) — laptop-reviewed and published — **A DEFECT INHERITED FROM A LIVE DONOR**

Desktop branch `pastpapers/qp2310-founder-review` @ `ccef3d7`, based on `149a10f`, pushed
2026-08-14 15:48 IST. Twelve files, all paper-owned, one commit. Integrated onto current `main`
(`6dec08a`) by **path extraction**; the branch was never merged and is retained as provenance. Its
tip did not move during the review — the desktop had gone on to QP2307, QP2308 and then QP2306.

**Merging would have been destructive, and measurably so.** The branch diff against `main` showed
**56,047 deletions** — it would have reverted the six-year extractor repair, the QP2303 publication
and the storefront coverage fix, none of which existed when it was cut.

### Source — verified independently from the printed copy

`2310 EM`, October 2023, `(India 2023)`, 2 pages, **9 questions counted by reading**, printed
`Total Marks – 100`. Two printed anomalies are load-bearing and both are **preserved, not repaired**:
**Q5 prints (8) on limb A and (16) on limb B**, which sum to 24 against an equal-marks rubric, so its
sub-part marks are left null; and **Q9 prints no mark figure at all**. The unclosed quotation mark
before `latent failures`, `hull Forms`, `vis-a-vis`, `Scavenge Air Moisturizing` and the singular
`other similar Convention` all survive in `text_verbatim`.

### Q1–Q9 — seven PASS, two CORRECTED

**C1 — Q9, the ISM Code is not divided into regulations (21 strings).** The answer cited the
Company's investigation duties as `ISM Code regulation 9`, `regulation 1.2.2` and `regulation 12`.
Part A of the ISM Code has numbered **elements**, divided into **paragraphs**. *Regulation* belongs
to SOLAS and MARPOL — and this same answer uses `SOLAS regulation XI-1/6` correctly twelve times,
which is what makes it a slip rather than a house style. Corpus-wide the house forms run **element
(142), paragraph (34), section (33) against regulation (29)** — and **all 29 are in this paper (16)
and `QP2412` (13), which is this question's answer donor.** Corrected to *paragraph 1.2.2* and
*elements 9 and 12*, after proving Q9 contains **no MARPOL or Annex VI regulation reference** that
the same substitution would have damaged. `SOLAS XI-1/6` untouched.

> **`QP2412` IS LIVE AND STILL CARRIES THIS DEFECT.** Referred, not fixed — one paper per session.
> Any fix there must repeat the scoping proof, because QP2412's affected questions may contain
> Annex VI references that QP2310's did not.
>
> **CLOSED 14 August 2026 at `594fdcf`.** The scoping proof was repeated: QP2412-Q5 carries no
> MARPOL or Annex VI regulation reference, and all 11 `SOLAS regulation XI-1/6` citations are
> untouched. Scope was **23 tokens, not the 13 referred** — the referral counted only the
> `ISM Code regulation N` form, and Q5 also carried seven **bare** references with the ISM Code as
> the antecedent and two **abbreviated** as `reg`. The correction above was itself incomplete for
> the same reason: `QP2310-Q9`'s recall card still read *"ISM reg 9 ... reg 1.2.2 ... reg 12"* in
> front of customers and is fixed in the same commit. The class is now held by `known_traps.md`
> **trap 18** in both the grep and the structural layer, with positive **and** negative controls.

**C2 — Q7, production vocabulary on a rendered flashcard.** *"The standing statute trap for the
whole 2023 **batch**"*. The desktop's own sweep (§6.1 of the paper anchor) caught eleven uses of
*donor* and one of *laptop-reviewed* but missed this, because it searched the **authoring**
vocabulary and not the **scheduling** vocabulary. Eight further uses of "batch" were found and
**deliberately left**, all in `reuse_evidence`, `question_delta` and `temporal_review` — confirmed
non-rendered by sweeping **the bytes of both built pages**, not by trusting a field list.

### What was checked and HELD

- **Annex VI chapter 4 is interleaved, and the paper has it right.** Attained EEDI **22**, attained
  EEXI **23**, required EEDI **24**, required EEXI **25**, CII **28**. Confirmed against the
  corpus's `mepc-328-76` nodes, which also give regulation **21** as *Functional requirements* —
  consistent with the standing note that **reg 21 is never EEDI**.
- **The corpus-holdings claim is accurate.** "Annex VI is citation-ready but not quotation-ready"
  was tested: all **56** Annex VI nodes carry `text` (controlled paraphrase) and **none** carries
  `exact_text_excerpt`, which the casualty package's nodes do. **Four consecutive reviews found
  understated holdings; this paper does not.**
- **Q9 uses "very serious marine casualty"**, which `MSC.255(84)` para 2.22 defines, and avoids
  "serious marine casualty", which it does not.
- **`MEPC.328(76)` in force 1 November 2022** (TSCR-3 carried, register still wrong at 2023-11-01).

### Q5's donor dependency — discharged, not waived

The anchor declared Q5's donor `QP2303-Q4` as sitting on an **unreviewed branch**. That was true
when written and is **now stale**: QP2303 went live at `604ca40` earlier the same day. Q5 was
re-read against the published version. Both papers state `MEPC.328(76)` in force 1 November 2022
and both exclude `MEPC.385(81)`; the stems are identical, so the EXACT classification holds.

### Intelligence graduation — proved, not asserted

| | 2023 solved | 2023 intel-only | combined |
|---|---|---|---|
| before | 5 | 6 | **61 papers / 549 questions** |
| after | **6** | **5** | **61 papers / 549 questions** |

Solved **+1**, intelligence-only **−1**, combined **unchanged**. Computed by the builder; **no
record was hand-deleted.**

### UI fixture — authored, and two probes rejected on proof

QP2310 had none, which failed the UI suite on both surfaces (43/45, then 66/66). The search is
**token-AND, not substring**, and that rejected two probes that looked obviously safe: `bunker oil`
also matches Q6 (*bunker* delivery note, compliant *fuel oil*), and `Merchant Shipping Act 1958
Part XA` also matches Q8. **A probe matching two cards still passes the assertion and still reports
green**, so uniqueness was proved for all nine. `A.1155(32)` is the sentinel — a break there most
likely means the 33rd-Assembly resolution has been walked back into a paper that predates it.
`MEPC.328(76)` was considered and **rejected**: it reaches four cards and cannot localise.

### The storefront guard caught its first live defect

Phase 0 of this session closed the gap that let *"2023: Jan · Apr · Dec"* ship while five sittings
were solved. On this paper's very first build it fired:

> `2023 coverage omits October -- solved and delivered, but the customer is not told they get it`

The months are **derived from the specs**, never typed into the checker. A negative control asserts
a correct block is **accepted** before any mutation is tested, because a guard that rejects the
truth gets edited until it passes.

### Verification

Full `run_toolchain --publish --strict`: **ALL STAGES PASS**. Delivery gate
`--verify-derivation --strict`: **PASS**. Determinism: **85 artefacts byte-identical across two
full builds** (product and six-year). Security suites: **198/198**, 0 failures. UI: **66/66 on both
the review and delivery pages**. Visual: 1280 and 375, **9 anchors · 5 modes · no overflow · no
console errors · zero internal vocabulary in visible text**.

Published as `3486547`. Live storefront verified at **34 papers / 306 questions** with 2023 reading
**Jan · Mar · Apr · Sep · Oct · Dec**. Existence was **not** proved from the paid route's 302: that
redirect is path-agnostic and `QP9999.html` returns it identically. The evidence used is the
**generated** free-sample page, which enumerates *October 2023* in its month list and states
*34 solved papers · 306 questions*.

---

## 7n. QP2303 (March 2023) — laptop-reviewed and published — **THE SIX-YEAR WINDOW CORRECTED THE PAPER'S OWN ANCESTRY**

Desktop branch `pastpapers/qp2303-founder-review` @ `2eed92e`, based on `d6d95e8`, pushed 2026-08-14
11:52 IST. Twelve files, all paper-owned. Integrated onto current `main` (`e41772e`) by path
extraction on `integration/qp2303-laptop-review`; the desktop branch was **never merged** and is
retained as provenance. Its tip did not move during the review — the desktop had gone on to QP2302,
QP2310, QP2307 and QP2308.

**Merging would have been worse than usual.** The branch base predates the trial system, the
storefront counts, QP2304, QP2309 *and* the six-year repair, so its diff carries
`D api/_lib/trial.js`, `D api/_lib/grants.js`, `D solvedQP/QP2309.html` and
`D tools/pastpapers/sixyear_intelligence_test.py`.

**Product: 33 available papers · 297 published questions.** March 2023 transitioned to Available
automatically.

### Seven of nine accepted. Two corrected, both against a source read in this session

**Q2 (MAJOR) — guideline G5 was misdescribed on every surface it appeared.** The answer gave
`MEPC.355(78)` as *"corrective action for a poor rating, and incentives for good performance"*. Its
title page reads **2022 INTERIM GUIDELINES ON CORRECTION FACTORS AND VOYAGE ADJUSTMENTS FOR CII
CALCULATIONS (CII GUIDELINES, G5)**. The number was right and the subject was wrong. Corrective
action for a D-or-E rated ship is not a guideline at all — it is MARPOL Annex VI **regulation 28**
and the SEEMP guidelines `MEPC.346(78)`, both of which the answer already stated correctly
elsewhere. The error had propagated to **seven candidate-facing surfaces**. This is a **regression
against MIW's own verified record** — `QP2411`'s anchor already carried G5 correctly, P1, read at
source. The correction also repairs the answer's own argument: section 6 criticises the CII for
penalising a laden ship waiting at anchor, and **G5 is precisely the instrument that answers that
criticism**.

**Q1 (MINOR, precise) — the transfer-of-damage duty is UNCLOS article 195, not article 194.**
Article 194(2) carries the damage-to-other-States duty; **article 195** is a separate article with
its own heading. On a limb whose mark scheme is article-level precision, a reader sent to 194 would
not find it.

### Understated holdings — the FOURTH occurrence of this defect class

| Claim as authored | Reality | Action |
|---|---|---|
| Q1: Part XII safeguards *"their individual articles were not examined"* | **UNCLOS is held**; section 7 is articles 223–233 | **Read at source.** Articles 224, 225, 226, 227, 230, 231, 232 named with substance; graded P1 |
| Q2: CII guideline set graded **P2**, *"established by the corpus review"* | **All five are held** as official IMO resolution texts | **All five title pages read at source**; G1–G5 and the SEEMP guidelines promoted to **P1** |

**Claims checked and found accurate, left alone:** `MEPC.304(72)` is genuinely not held; the EEXI
guideline set is genuinely not held and citing it by function rather than inventing a number is
correct; `A.1155(32)` is genuinely not held — MIW holds only `A.1185(33)`, nine months future for
this sitting; MIW holds no IACS procedural document and no quality-management standard.

### The six-year window moved four of the nine questions' ancestry BACKWARD

The desktop derived its donor map against the **solved set**, which holds no 2021 or 2022 sitting.
Re-derived against **61 sittings / 549 questions**:

| Q | Earliest printing | Direction |
|---|---|---|
| **Q1** | **QP2104-Q2, April 2021** (also QP2210-Q9 Oct 2022; QP2306-Q1 Jun 2023) | **backward 23 months** |
| **Q2** | **QP2208-Q4, August 2022** | **backward 7 months** |
| **Q3** | **QP2208-Q2, August 2022** | **backward 7 months** |
| **Q9** | **QP2107-S2-Q1, July 2021** (also QP2108-Q2, QP2203-Q2) | **backward 20 months** |
| Q4 · Q5 · Q6 · Q8 | **this sitting originates the family** | forward |
| Q7 | **UNIQUE** — nothing above the noise floor in six years | — |

**No `reused_from` changed.** The intelligence layer holds printed wording and no answers, so it can
correct *where a question was first asked* and can never supply *what the answer is*. The host's own
annotations independently name the same sittings, which is a genuine cross-check.

**`QP2303-Q8` to `QP2309-Q2` confirmed by measurement:** limb (b) and the whole of QP2309-Q2
normalise to the **identical string**, differing only by QP2309's printed `(16)`. **`QP2207-Q7` is
NOT a wording ancestor** — similarity **0.053** to QP2303-Q8. The July 2022 premise stays rejected.

### A live extractor defect, found through this paper and fixed

`HOST_HINT_RX` fixed the month at **exactly three letters**, matching `2023/MAR/4` but neither
`2021/JULY/Q1` nor `2023/JUNE/Q1` — after `JUL` the next character is `Y`, the trailing word
boundary failed, and the whole annotation survived. **58 stems across 24 papers** still carried host
code. Because `recurrence_model.normalise_stem` compares printed stems for equality, `QP2306-Q1` —
the verbatim reprint of this paper's Q1 — compared **UNEQUAL**, which is failure mode 1 in the
extractor's own comment block, and it was suppressing QP2303's own Q1 ancestry.

Widened to `[A-Z]{3,9}` with the attached-digit form `2016/JAN2`; two further **span-based** rules
added for the sales footer that wraps after *"organized manner with"* and for the bare page number
left at the end of a stem spanning the page break. A line filter was tried first and reproduced the
exact wrap bug the previous session had already hit — span-based is the rule.

**Proof: 71 stems changed, 0 stems gained any text, all 270 ids preserved, 0 residual host
artefacts of any form.**

### Candidate-facing production vocabulary — 11 rewrites

A sweep of the seven candidate-facing fields found internal machinery reaching a paying reader:
*"flagged for verification … before publication"* (Q1, Q2 — the same class as `QP2501-Q1` and
`QP2309-Q5`), *"MIW's own reference corpus … the corpus amendment register is wrong by one year"*
(Q2, Q4, including `quick_revision`), *"review-queue item RQ-25"* (Q8), *"the corpus records a
modelling defect"* (Q7), and the evidence grades *"primary-verified"* / *"authoritative secondary"*
(Q2). All rewritten in candidate vocabulary, keeping the disclosure and dropping the register.
**The delivery build now carries zero internal-vocabulary terms.**

### Validation

`validate_spec` **0 errors / 0 blocking**, 11 warnings — 9 the Founder-deferred word band, 2 the
`no P1` notes on Q5 and Q9 (both engineering questions where MIW holds no test-method standard).
`run_toolchain` **ALL STAGES PASS**. `delivery_gate.py --verify-derivation --strict` **PASS**.
**Double build byte-identical across 206 artefacts**, product and six-year both. New authored UI
fixture **63/63** — its regulation probe is deliberately `mepc.355(78)`, a regression sentinel for
the G5 correction, because `MEPC.328(76)` reaches Q4 as well and cannot localise a break. Search
**49/49**, home contract **PASS 6 rules**, coverage **PASS**, recurrence **0 failures**, corpus
consumer **PASS**, six-year **PASS 8 rules**, security **198/198** across six suites.
**Zero host or provider tokens in any built artefact** across delivery, public and review surfaces.

### Intelligence graduation — automatic, and proved by removing the spec

| | Before | After |
|---|---|---|
| SOLVED | 32 papers / 288 questions | **33 / 297** |
| INTELLIGENCE-ONLY | 29 sittings / 261 questions | **28 / 252** |
| **Combined six-year universe** | **61 / 549** | **61 / 549 — unchanged** |

Established by building the layer with `QP2303.json` moved aside and again with it in place.
**Nothing was hand-deleted from `historical_qp_intelligence.json`** — it still carries all 30 raw
2021–2023 sittings, and graduation is applied at the derived layer by rule.

---

## 7m. QP2309 (September 2023) — laptop-reviewed and published — **FIRST PAPER JUDGED AGAINST SIX YEARS**

Desktop branch `pastpapers/qp2309-founder-review` @ `9631b2e`, based on `bf5b533`, pushed
2026-08-14 07:25 IST. Twelve files, all paper-owned, no global artefacts. Integrated onto current
`main` (`a633e97`) by path extraction on `integration/qp2309-laptop-review`; the desktop branch was
never merged and is **retained as provenance**. The branch tip did not move during the review.

**Product: 32 available papers · 288 published questions.** September 2023 transitioned to Available
automatically.

**The desktop build was strong and most of it was accepted.** `model_answer` carries **zero**
post-sitting citations on all nine questions, Rule 4 is clean on all nine `understand_first`, and
every post-sitting resolution on the paper sits in a `major_trap` field that warns the candidate
*away* from it. The two sharpest temporal calls — `A.1155(32)` operative for Q9 and `A.1118(30)` for
Q7, both revoked by the 33rd Assembly three months *after* the sitting — were verified and are right.

### The six-year window was applied to a paper for the first time

The intelligence layer was generated at 12:01 IST; this branch was pushed at 07:25. The donor map was
therefore derived against 279 questions and has been re-derived against **549**.

| Q | Earliest appearance as authored | Corrected | Note |
|---|---|---|---|
| **Q2** | QP2401-Q5(b), Jan 2024 | **QP2207-Q7, July 2022** | `QP2303-Q8(b)` (March 2023) prints the whole stem **six months BEFORE** the sitting |
| **Q4** | QP2402-Q1, Feb 2024 | **QP2102-Q2, February 2021** | repeated `QP2109-Q2`, September 2021 — same month, exactly two years earlier |
| Q1 | QP2407-Q1, July 2024 | **this sitting** | nothing earlier in six years; September 2023 *originates* the family |

**Q2 is the first question on any paper whose wording ancestry runs backward.** The anchor's
*"every donor is later"* is true of **answer donors** and is **not** true of lineage. No
`reused_from` changed: the intelligence layer holds printed wording and no answers, so it can correct
where a question was first asked and can never supply what the answer is.

**Both "fresh research" findings survived the wider test**, which was the result most likely to
break. Q5's only six-year hits match *"fine grain"* in an ICCP question; Q6 has none.

### Corrections applied

**Q5 (MAJOR)** — the spec declared *"the corpus SOLAS holding covers chapters II-1, II-2 and III
only"* in three places, and that was the stated reason the question carried **zero
`P1_PRIMARY_VERIFIED` claims**. The corpus holds the **full SOLAS 2024 consolidated edition** with a
working text layer (and the structured corpus also holds chapter V). **SOLAS VI/8 and VI/9 were read
at source**, primary-verifying the Grain Code's identity as `MSC.23(59)`, the statutory definition of
grain, the mandatory hook and the Document of Authorization. Q5 goes **0 → 4 P1**, and the only
non-word-band validator warning on the paper is cleared. Same defect class as `QP2511-Q8`'s "MIW
holds no licensed copy of the Hong Kong Convention"; a corpus-wide sweep found it **contained to
QP2309** — a regression, not an inheritance.

**Q8 (MINOR)** — the continental shelf limb stopped at the 200-mile entitlement. **UNCLOS article 76
was read at source** and paragraph 5's outer cap added: 350 nautical miles from the baselines, or 100
from the 2,500 metre isobath. The omission had been *deliberately* recorded on the ground that
paragraphs 4–6 were unread; reading them removed the ground.

**Q5 study guide (MINOR, candidate-facing)** — told a paying reader a claim was *"flagged for
verification … before publication"*, on a published page. Same class as `QP2501-Q1`. Rewritten to
keep the disclosure and drop the internal register, and pointed at the ship's approved grain loading
manual instead.

**Paper-level (MINOR)** — `marks_note` claimed Q1, **Q6** and Q9 carry limbs with no individual mark.
Q6 prints `A.(5) B.(5) C.(6)` and the spec's own `subparts` record 5/5/6. Corrected to Q1 and Q9.
`printed_marks_absent` was set on two questions and absent on seven; normalised to `false` on all
nine (the paper prints (16) throughout). No derived output changed.

**Donor status** — ten references called `QP2312`/`QP2304` `FOUNDER-REVIEW-PENDING`. Both were
published earlier the same day; corrected across the spec, the anchor and the Q9 record.

### Two failures fixed that QP2309 did not cause

- **`coverage_check.py`** compared the rendered `NO_SITTING` set against the **whole** of
  `KNOWN_ABSENT`. When `KNOWN_ABSENT` was extended back to 2021 for the intelligence years,
  `build_solvedqp_home` was correctly restricted to years holding a paper, and the checker was not.
  It now compares against the years the grid actually renders.
- **`SQ/index.html`** still advertised 31 papers / 279 answers. Data only; the historical commentary
  lines describing the *earlier* count drift were deliberately left verbatim.

### Validation

`validate_spec` **0 errors / 0 blocking**, 9 warnings — all the Founder-deferred word band, down from
10. `run_toolchain` **ALL STAGES PASS**. `delivery_gate.py --verify-derivation --strict` **PASS**.
Double build **byte-identical across 80 generated artefacts**. UI **62/62** on a new authored fixture
(probes chosen against the Q2/Q7 recognized-organization collision, which defeats every obvious
term). Search **49/49**, home contract PASS, coverage PASS, recurrence 0 failures, corpus consumer
**60/60**, security and access **198/198** across six suites. **Zero host recurrence tokens and zero
provider branding in any built artefact.** No paid answer text in the public manifest.

`solvedQP/QP2309.html` was untracked for the **EIGHTH** consecutive paper and was staged by explicit
path.

### Reported, not fixed

`tools/pastpapers/build_sixyear_intelligence.py` reads `hist_raw.json` from **another session's
scratchpad directory**, hard-coded. It is a one-shot analysis script, not a reproducible builder, so
the intelligence layer cannot currently be regenerated. QP2309's own record was removed from it by
hand when the paper became solved (30→29 papers, 270→261 questions; the six-year total holds at
61/549). Rebuilding that script properly is a governed change and is raised rather than done.

---

## 7l. QP2301 (January 2023) — laptop-reviewed — **BATCH 4 OPENS · FIRST 2023 PAPER**

Desktop branch `pastpapers/qp2301-founder-review` @ `6e811d7`, based on `57b9342`, pushed
2026-08-13 21:05 IST. Twelve files, all paper-owned, no global artefacts. Integrated onto current
`main` (`dcd7826`) by path extraction on `integration/qp2301-laptop-review`; the desktop branch was
not merged and is **retained as provenance**.

**Path extraction was load-bearing, not ceremonial.** The branch base `57b9342` is the QP2407
integration commit, which predates the QP2408 publication, the DGMA naming sweep **and the entire
Search + Updates architecture at `161c2b1`**. A merge would have reverted live production
infrastructure.

**Product: 29 available papers · 261 published questions.** January 2023 transitioned to Available
automatically and the **2023 year sheet, topic sheet and nav entry were generated, not authored** —
the first time a whole new examination *year* has been absorbed by the derived layer.

### The session brief was wrong on two premises, and both were checked rather than assumed

1. **"All nine questions currently have zero P1" is false.** The paper carries **100** P1 claims as
   received, 2 to 17 per question. The zero figure was true of the *intake* spec before the answer
   layer existed. **No P1 was manufactured to improve the metric** — exactly one claim was promoted,
   Q7's, and only because MSC.255(84) was read at source. Total is now 101.
2. **The Casualty Investigation Core package does not need building — it already exists.** A
   complete, validated package sits at `Knowledge Central/casualty-investigation/`:
   FOUNDER_REVIEW, 15 sources, 22 definitions, 28/28 Part II standards, 106 verified citations,
   0 failures, and three acceptance tests including one written against the SOLAS I/21 gap. It is
   git-ignored, which is why a repository-wide triage did not see it. **Reclassify from build to
   migration** — it is not in `F:\miw-true-source`, so no consumer seam can address it.

### Three corrections, all at the canonical spec

**Q7 (MAJOR)** — *"serious marine casualty"* was presented as a Code-defined term. MSC.255(84)
chapter 2 defines twenty-two terms, 2.1 to 2.22, and it is not among them; the phrase's only
appearance in the resolution is a preambular recital about the ILO MLC. Re-attributed to the
harmonized reporting procedures. This landed on the one limb where definitional precision is the
mark scheme.

**Q4 (MINOR ×2)** — the SCOPIC on-scene appointee was named *"Shipowner's* Casualty Representative"
in five places and described as attending automatically. Clause 12 defines the ***Special*** Casualty
Representative, whom the owners *"may at their sole option appoint"*. **A regression, not an
inheritance**: a corpus-wide sweep found the wrong expansion in QP2301 alone — the donor QP2506 has
it right — so nothing propagated.

**Q6 (MINOR)** — Rule D carried only *"without prejudice to any remedies"*; the Rule says *"remedies
**or defences** … open **against or to** that party"*. The defences half is the residue the New Jason
Clause closes, the same point QP2407-Q8 turned on.

**The two named corpus warnings did not bite.** `TSCR-6`'s defective `TRAP-RULE-D-FAULT` gloss was
not followed — Q6 independently reached the same conclusion QP2407 did, which should move **TSCR-6
from raised to confirmed**. `TSCR-5` did not arise: no object ID was consumed. **No new TSCR raised.**

### Temporal result — the cleanest paper in the corpus on these measures

Every donor is **later** than this sitting, by 15 to 42 months, so the usual protection that an
earlier donor cannot drag later law backwards does not exist anywhere on the paper. Against that:
**0 future-contamination hits** across 13 instrument classes in candidate-facing fields, and
**0 Rule 4 breaches** in `understand_first` on all nine questions.

### Validation

`validate_spec` **0 errors / 0 blocking**, 9 warnings — all the Founder-deferred 450–650 word band.
`run_toolchain` and `--self-test` both **ALL STAGES PASS**. Double build **byte-identical across 145
generated artefacts**. Search tests **49/49**, coverage PASS, recurrence 0 failures, corpus consumer
**60/60**, security **121/121** unchanged. New UI fixture: **60 passed / 0 failed**, its regulation
probe deliberately `MEPC.331(76)` because cybutryne entering force on 1 January 2023 is this paper's
sharpest live edge.

**Search / Updates regression — QP2301 was its first real production test, and it passed.** Indexed
automatically; deep links resolve to `#q1`…`#q7`; the alias-only term `vsmc`, which is never rendered
on any card, retrieves Q7; the negative control returns a proper no-match citing 261 questions across
29 sittings. Two ledger rows generated: `added` and an `enriched` note naming Q4, Q6 and Q7. **Zero
host recurrence tokens anywhere in any built artefact, attributes included.**

**`solvedQP/QP2301.html` was untracked for the SEVENTH consecutive paper** and was staged by explicit
path. `git add -u` would again have shipped a manifest entry pointing at a page that does not exist.

### Reported, not fixed

`PASTPAPER_PRODUCTION_PROTOCOL.md` §2.1 cites `QP2506-Q1` as its worked precedent for an answer with
no regulatory source, calling it a question where *"no instrument prescribes a propeller type"* whose
answer *"quotes no efficiency percentage anywhere"*. `QP2506-Q1` is the **rudder-device** question and
it quotes four percentages. The rule is sound; only its illustration is false. A protocol file is
governed, so this is raised rather than edited.

Full record: [`QP2301_TEMPORAL_AND_DONOR_ANCHOR.md`](QP2301_TEMPORAL_AND_DONOR_ANCHOR.md) §9 and
[`QP2301_TRUE_SOURCE_GAPS.md`](QP2301_TRUE_SOURCE_GAPS.md).

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
4. `YAR-VI` — ~~salvage, including Art. 14 / SCOPIC, is a particular charge, outside the adjustment.~~
   **CORRECTED 2026-08-15 (TSCR-9)** — that was the **YAR 2004** rule under a **2016** label. YAR 2016
   **Rule VI(a) allows** salvage expenditure incurred to preserve the property from peril, subject to
   VI(b)–(d); only **VI(d)** (Art. 14 special compensation and SCOPIC) is excluded. "Particular charge"
   is in neither edition.
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
