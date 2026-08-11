# DESKTOP QP ALLOCATION — 2024

**The production board for the second (desktop) team.**
Created 2026-08-11 in the parallel-production baseline session.

Six **unsolved 2024** papers are allocated here. Not 2025. Not 2026.

Read [`DESKTOP_QP_PRODUCTION_PLAYBOOK.md`](DESKTOP_QP_PRODUCTION_PLAYBOOK.md) first — it is the
method. This file is the board: *which papers, in what order, with what warnings.*

This board fills the deliberately-empty allocation table in
[`PARALLEL_PRODUCTION_BOARD.md`](PARALLEL_PRODUCTION_BOARD.md) §5. Where the two differ on
branch model or repository rules, the **PARALLEL_PRODUCTION_BOARD wins**.

---

## 1. CORPUS TRUTH AT ALLOCATION

Verified, not carried forward, on 2026-08-11:

| | |
|---|---|
| Corpus | **252 questions / 117 solved / 135 unsolved** |
| Papers | 28 — **13 solved**, 15 answerless intake |
| **2024** | 11 papers — **2 solved** (QP2403, QP2404), **9 unsolved** |
| Reuse map | **current** — `build_reuse_map.py --check` reports "reuse map and source inventory are current" |

May is absent from the source set in all three years. There is no `QP2405`.

---

## 2. COMMON DESKTOP BASELINE — immutable for all six

| | |
|---|---|
| **MIW baseline commit** | `PENDING — recorded by the follow-up metadata commit; see §2.1` |
| Baseline branch | `workflow/corpus-consumer-integration` |
| Baseline contents | corpus consumer seam · honest product coverage · 252/117/135 · 13 papers delivered · toolchain green |
| **Required corpus commit** | `64977b86ed9c601e273f1d0cb55abb0461835811` |
| Corpus branch | `RulesApp-Local-Input` `origin/main` — 0 ahead / 0 behind, tracked tree clean |
| MIW remote | `github.com/nickmarineengr-aiLiterate/marine-intelligence-weekly` — **PUBLIC** |
| Corpus remote | `github.com/nickmarineengr-aiLiterate/RulesApp-Local-Input` — **PRIVATE** |

**All six branches start from that one commit.** Not from six historic paper heads.

### 2.1 How the baseline hash is recorded

The baseline is **the commit that introduces this file and the playbook**. Its hash cannot be
written inside itself, so it is recorded by a small follow-up metadata commit that names its own
parent. Until that commit exists, the row above reads `PENDING`.

**Verify before you branch** — the value in §2 must equal:

```bash
git -c safe.directory=* log --oneline -2 workflow/corpus-consumer-integration
# the metadata commit's PARENT is the baseline
```

If §2 still says `PENDING` in the copy you cloned, **fetch again** — you are behind the metadata
commit. Do not guess a hash and do not branch from a hash that is not written here.

If the corpus team lands FSS or MARPOL work after this baseline, **do not move the desktop branches
onto a newer corpus commit.** Record the commit you consumed; the laptop enriches at integration.

---

## 3. THE SIX ALLOCATED PAPERS

Branch name for each: `pastpapers/qp####-founder-review`, branched from §2.

| # | Paper | Sitting | Branch | Tier D | Family reach | Temporal flags | Dependency |
|---|---|---|---|---|---|---|---|
| **1** | **QP2401** | January 2024 | `pastpapers/qp2401-founder-review` | **3 / 9** | 3 | 2 | — |
| **2** | **QP2412** | December 2024 | `pastpapers/qp2412-founder-review` | 2 / 9 | 1 | **0** | **shares Q9 donor set with #1** |
| **3** | **QP2402** | February 2024 | `pastpapers/qp2402-founder-review` | 1 / 9 | 3 | 2 | early-2024 line from #1 |
| **4** | **QP2409** | September 2024 | `pastpapers/qp2409-founder-review` | 2 / 9 | 1 | 2 | — |
| **5** | **QP2411** | November 2024 | `pastpapers/qp2411-founder-review` | 1 / 9 | 0 | 2 | bracketed by #4 and #2 |
| **6** | **QP2410** | October 2024 | `pastpapers/qp2410-founder-review` | 3 / 9 | 0 | **4** | **highest risk — see §6** |

**Owner (all six):** `DESKTOP CORPUS/QP TEAM`
**Status (all six):** `ALLOCATED — NOT STARTED`
**Corpus dependency (all six):** none blocking. No 2024 question requires FSS or MARPOL Annex VI
provision *text*; citation-level reference is sufficient and available.
**Last push / Founder review status (all six):** `—`

### Not allocated, and why

| Paper | Sitting | Tier D | Reach | Why held back |
|---|---|---|---|---|
| QP2406 | June 2024 | 0 / 9 | 2 | zero verified donors — nine fresh researches |
| QP2407 | July 2024 | 0 / 9 | 2 | zero verified donors — nine fresh researches |
| QP2408 | August 2024 | 1 / 9 | 0 | one donor, no family reach |

These three form the **mid-2024 block** and are the natural second batch, once the allocated six
have unlocked further donors. They are the heaviest fresh-research burden per unit of product and
are the worst fit for a team building its first papers.

---

## 4. ALLOCATION RATIONALE

Selection was **not** chronological. It was made against donor readiness, family reach, temporal
complexity, dependency, research burden and safe parallelism.

### 4.1 The six are the six most *ready* papers in 2024

Ranked by verified donors, the nine unsolved 2024 papers order:
`QP2401 (3) · QP2410 (3) · QP2409 (2) · QP2412 (2) · QP2402 (1) · QP2408 (1) · QP2411 (1) ·
QP2406 (0) · QP2407 (0)`.

The allocation takes every paper with **≥ 1 verified donor except QP2408**, and takes none with
zero. That converts the maximum amount of already-verified research into finished product.

### 4.2 They form two contiguous calendar blocks — this is the main finding

```
   JAN  FEB              SEP  OCT  NOV  DEC
   ██   ██               ██   ██   ██   ██
   #1   #3               #4   #6   #5   #2
```

- **Early-2024 block:** QP2401 · QP2402
- **Late-2024 block:** QP2409 · QP2410 · QP2411 · QP2412

Contiguity is worth more than it looks. The regulatory position of a sitting is established once
per *period*, not once per paper: instrument editions in force, amendment entry dates, Indian
statute position and guideline revisions move on their own calendar, not on the exam calendar. A
contiguous block researches that line **once** and re-anchors it per sitting, instead of rebuilding
it from scratch six times.

The three held-back papers are exactly the mid-year gap — a coherent later batch, not an
awkward remainder.

### 4.3 Safe parallelism

The desktop team owns **all six** and works them **one at a time**, so no two papers that share a
donor family are ever in flight simultaneously. The laptop authors **no** 2024 paper while these
are open. That is what makes the shared donor sets in §6 safe rather than dangerous.

### 4.4 What was deliberately not optimised for

**Family reach was not allowed to override donor readiness.** QP2507 (2025) carries the highest
family reach in the whole corpus at 8, and is still not the right paper to start from — it has
**zero** verified donors, so all nine questions are fresh research. The same logic excludes
QP2406/QP2407 here. Reach is only valuable once a paper is finishable.

---

## 5. RECOMMENDED ORDER — 1 → 6

Work them in this order. Every position has a reason.

| # | Paper | Why here |
|---|---|---|
| **1** | **QP2401** | Highest combined readiness in 2024 — 3 verified donors *and* family reach 3. Establishes the early-2024 line and the Q9 donor family that #2 needs. |
| **2** | **QP2412** | Takes the Q9 research from #1 while it is fresh — **identical donor set**. Also the only 2024 paper with **zero** temporal flags, so it is the fastest paper in the set and a clean second run. |
| **3** | **QP2402** | Adjacent to #1. The January line re-anchors to February with one adjustment rather than a rebuild. Family reach 3 pays forward. |
| **4** | **QP2409** | Opens the late-2024 block from the early end. Both donors come from QP2404 and QP2506, which are solved and verified. |
| **5** | **QP2411** | Now **bracketed** — September (#4) and December (#2) are both established, so November re-anchors between two known points. |
| **6** | **QP2410** | **Last deliberately.** Highest temporal risk in the entire 2024 set. By this point September, November and December are all solved and sitting-anchored, so October is bracketed on both sides — the safest possible position for the most dangerous paper. |

---

## 6. DEPENDENCY WARNINGS — recomputed, not inherited

Both warnings carried in the allocation instruction were **recomputed against the current reuse map
and both are confirmed true.** They are not assumptions.

### 6.1 CONFIRMED — QP2401-Q9 and QP2412-Q9 share an identical donor set

| Question | Preferred donor | Wording | Other donors |
|---|---|---|---|
| `QP2401-Q9` | `QP2403-Q7` | identical | `QP2510-Q7` |
| `QP2412-Q9` | `QP2403-Q7` | identical | `QP2510-Q7` |

Same preferred donor, same alternate, same family, both printed stems identical to the donor.

**Action taken:** both papers are allocated to the **same owner** and placed **adjacent** in the
sequence (#1 and #2), so the research is done once and transferred immediately.

**Action still required of the author:** an identical donor set is **not** an identical answer.
January 2024 and December 2024 are eleven months apart. The Q9 answer must be re-anchored to each
sitting independently. Reusing the object wholesale is the specific failure this warning exists to
prevent.

### 6.2 CONFIRMED — QP2410 carries high-volatility donor relationships

QP2410 holds the **only HIGH-volatility donor relationship in the whole 2024 set**, and has **four**
temporal flags — more than any other 2024 paper.

| Question | Donor | Volatility | Flag |
|---|---|---|---|
| `QP2410-Q4` | `QP2511-Q8` (alt `QP2603-Q9`) | **HIGH** | `CONVENTION NOT YET IN FORCE` |
| `QP2410-Q5` | `QP2511-Q7` | **MEDIUM** | `IMO INSTRUMENT IN FLUX` |
| `QP2410-Q9` | `QP2404-Q6` (alts `QP2506-Q6`, `QP2508-Q6`, `QP2602-Q6`) | stable | — |
| `QP2410-Q1` | — | — | `INDIAN STATUTE BOUNDARY` |
| `QP2410-Q8` | — | — | `IMO INSTRUMENT IN FLUX` |

`QP2410-Q4`'s donor is `QP2511-Q8` — a **November 2025** answer being pulled back to an **October
2024** sitting, across thirteen months, on a question flagged `CONVENTION NOT YET IN FORCE`. A
convention that was "not yet in force" at one of those dates may have been in force at the other,
and the donor answer will have been written for the *later* position.

**Required: sitting-date re-anchoring on every one of QP2410's donor questions.** Establish the
October 2024 examination date first, before any donor text is consulted.

### 6.3 SYSTEMIC — every 2024 donor is pulled BACKWARDS

This applies to all six papers and is the single most likely way this batch goes wrong.

> The unsolved sitting is the **earlier** one. Every donor available to a 2024 paper is a **2025 or
> 2026** answer. The donor is a later answer pulled *backwards*, so **any currency correction made
> for the later sitting must be reversed, not inherited.**

Concretely, for every donor you use, ask: *what did the donor's author add or change because their
sitting was later than mine?* — and take it back out.

The standing 2024 anchors:

- **33rd IMO Assembly, resolutions adopted 6 December 2023.** All 2024 sittings fall after it, so
  the `A.11xx(33)` editions are the operative Assembly instruments for all six papers. An Assembly
  boundary is the **adoption date**, not the meeting month.
- **Merchant Shipping Act 1958 governs throughout.** The MS Act 2025 commenced **15 March 2026** and
  must not appear in any 2024 answer.
- Any donor written for a 2025 sitting may carry the **34th Assembly** position (adopted 3 December
  2025). That is **after** every 2024 sitting and must be stripped out.

---

## 7. BRANCH AND ARTEFACT RULES — summary

Full rules in the playbook §13. The two that matter most for six parallel papers:

**A paper branch owns** its spec, its verification records, its anchor/checkpoint evidence and its
**review** HTML (`meoclass1/pastpapers/QP####.html`).

**A paper branch must NOT commit** any global derived artefact: the reuse map, the reverse-hint
queue, recurrence indexes, `pastpapers_content_index.json`, `questions-YYYY.html`,
`topics-YYYY.html`, `solvedQP/*`, any other paper's HTML, `CURRENT_STATUS.md`,
`history/SESSION_HISTORY.md`, or shared product/sample counts.

The toolchain **will** regenerate some of these during QA. Validate with them, then **revert them
before committing**. Global regeneration is laptop-owned, one paper at a time.

---

## 8. THE SIX-PAPER STOP GATE

When all six are complete and pushed:

> # STOP DESKTOP PRODUCTION.

Do not select a seventh paper. Do not merge to `main` or any integration branch. The six pushed
Founder-review branches are handed back to the **laptop team**, which reviews and integrates them
one at a time and owns all global regeneration.

---

## 9. PRODUCTION / DEPLOYMENT STATUS AT ALLOCATION

| | |
|---|---|
| **Written product** | **NOT DEPLOYED.** Live deployment is blocked on a security matter recorded in [`WRITTEN_PRODUCT_LIVE_TEST_STATUS.md`](WRITTEN_PRODUCT_LIVE_TEST_STATUS.md) |
| **Effect on QP authoring** | **NONE.** Authoring produces specs and review builds on branches; nothing reaches a customer |
| **Laptop QP production** | **PAUSED** while these six are open |
| **Provision viewer** | **DEFERRED** by Founder decision — do not build it |
| **FSS / MARPOL enrichment** | producer team resolving — **do not wait** |

**Do not attempt to deploy anything from a desktop paper branch.**
