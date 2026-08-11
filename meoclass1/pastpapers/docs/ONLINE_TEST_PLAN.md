# ONLINE TESTING PLAN — CONTROLLED FOUNDER TEST OF THE PARTIAL WRITTEN PRODUCT

**Status: DESIGN ONLY. Nothing was deployed, no secret was set, no payment was tested.**
Written 2026-08-11, in the pre-corpus-sync freeze session.

**This is not a marketing launch.** It is controlled Founder / tester validation of the product
as it stands, with 13 of 28 sittings solved. The launch blockers in
[`CURRENT_STATUS.md`](CURRENT_STATUS.md) §6 are unchanged and none of them is waived here.

---

## 1. Founder decision being implemented

Test now; do not wait for the library to be complete. A partial library is testable provided
the product is **honest about what is missing** — which is a generation problem, not a copy
problem, and is largely already solved (§3).

---

## 2. Desired year behaviour

Derived from the specs this session, not carried forward:

| Year | Sittings in set | Solved | Intake (not built) | Absent |
|---|---|---|---|---|
| 2026 | 6 | **6** | 0 | May, and Aug–Dec have not sat yet |
| 2025 | 11 | **5** — Jun, Aug, Sep, Oct, Nov | 6 — Jan, Feb, Mar, Apr, Jul, Dec | May |
| 2024 | 11 | **2** — Mar, Apr | 9 | May |
| | **28** | **13** | **15** | |

Three student-facing states, and they must never collapse into two:

| State | Control | Wording |
|---|---|---|
| **SOLVED / READY** | clickable paper card | month + year, opens the paper |
| **INTAKE / NOT BUILT** | non-clicking card | *"Not yet in the MIW set"* — a statement about **MIW's coverage**, not about whether the examination was held |
| **NO SITTING / NO SOURCE** | distinct label | *"No sitting"* + *"No examination paper exists for this month"*, with the reason |

> **Do not invent a paper.** May is absent in **all three years** and the evidence is the
> printed serial numbering itself — the serials run …2404, 2406… and …2504, 2506… with nothing
> at 2405 or 2505. That proof is already recorded in code and must stay in the student-facing
> text, because "no sitting" is a claim that has to be defensible.

---

## 3. Planned-soon generation — MOSTLY ALREADY BUILT

**Finding: the three-state model is not a new design. It exists, it is generated from canonical
state, and two checkers guard it.** No placeholder is hand-maintained anywhere.

Already implemented and already shipping in the delivery build:

| Mechanism | Where | What it does |
|---|---|---|
| `KNOWN_ABSENT` | `build_questions_year.py:52` | governed no-sitting truth for (2024,5), (2025,5), (2026,5), each with its serial-numbering reason |
| three-state month sections | `build_questions_year.py:320–329` | renders available / *No sitting* / *Not yet in the MIW set* |
| `paper_status()` | `build_index.py:57` | `'available'` only when `answers_built > 0` — **a source PDF in a folder can never make a paper look solved** |
| `SERIES_YEARS` + auto-include | `build_index.py:46–54` | unbuilt months come from configuration, never from placeholder spec files |
| navigator guard | `health_check.py:390–415` | every advertised year renders; available-cell count must equal the manifest's |
| absence guard | `questions_year_check.py:109–124` | all twelve months must appear; a known-absent month **must say why** |

So `solvedQP/questions-2024.html`, `-2025` and `-2026` **already** show Planned-soon and
No-sitting correctly today.

### 3.1 The actual remaining delta — one function

`solvedQP/index.html` is the only surface that still shows solved sittings **only**:

```python
# tools/pastpapers/build_solvedqp_home.py:80
def solved_sittings(specs):
    solved = [d for d in specs if any(q.get('model_answer') for q in d['questions'])]
```

Intake papers are filtered out and never reach the page, so the home currently implies the
library is 13 papers rather than 13 of 28. The change is small and deterministic:

1. add a sibling selector for intake sittings (specs exist for all 15 — no new data needed);
2. render them as **non-clicking** cards under the existing per-year grouping, reusing the year
   sheets' wording verbatim so the two surfaces cannot drift;
3. read absence from `KNOWN_ABSENT` rather than re-deriving it;
4. extend `solvedqp_check.py` with the guard that matters — **a Planned-soon card must carry no
   `href` and no deep link**, and the count of clickable paper cards must still equal 13.

**Not implemented in this session.** It changes candidate-facing delivery bytes, and this was a
hygiene and freeze session whose determinism requirement (§32 of the session brief) is that no
product byte moves. It is the first task of the online-test session, not of this one.

### 3.2 One judgement the Founder should make first

Should 2026 August–December — sittings that **have not happened yet**, today being 2026-08-11 —
render as "Planned soon"? They are neither absent nor merely unbuilt. Recommendation: **do not
render future months as Planned soon**; either omit them or label them separately, because
"Planned soon" against a sitting that has not occurred promises something MIW cannot schedule.

---

## 4. Online test scope

Separated by where each item can honestly be proven. **Anything that needs a live secret cannot
be tested offline, and no amount of offline green changes that.**

### 4.1 OFFLINE — provable now, no deployment

| # | Item | Instrument |
|---|---|---|
| Q | recurrence regeneration | `run_toolchain.py`, reuse map `--check` |
| R | Solved QP folder generation | `solvedqp_check.py` + `--self-test` |
| N | year sheets | `questions_year_check.py` |
| O | Planned soon | new guard, §3.1 item 4 |
| P | no-sitting | `questions_year_check.py:114–124` — already green |
| M | search | `health_check.py` search-metadata stage |
| S | public sample | `sample_check.py` |
| T | no provider leakage | `solvedqp_check.py` leak guards — 10 fire on the self-test fixture |
| C/D/E/F | session, entitlement, Oral-only, Written-only | `security.test.mjs` + `sessions.test.mjs` — **62/62 green**, access matrix included |

### 4.2 PREVIEW DEPLOYMENT — needs Founder approval, needs secrets

| # | Item | Why it cannot be offline |
|---|---|---|
| A | storefront | real routing through `middleware.js` |
| B | login | real session issue |
| G | dual-entitlement account | requires a real entitlement record |
| H | direct deep links | middleware must actually intercept |
| I | evicted session | requires the KV store |
| J | logout | requires cookie round-trip |
| K/L | mobile / desktop | real viewport against served CSS |

### 4.3 PRODUCTION — explicitly out of scope

Not until password rotation is confirmed, security is activated and the bundle price is
approved. **No live payment test in preview or production.**

---

## 5. Preview readiness — what would be needed, NOT activated

Determined from the recovered architecture; **nothing here was set**.

| Requirement | State today |
|---|---|
| `MIW_SESSION_SECRET` | **not set** |
| `KV_REST_API_URL` / `KV_REST_API_TOKEN` | **not set** — middleware fails closed, so a half-configured preview denies *everyone* including the Founder |
| Entitlement test accounts | none exist; must be seeded via `tools/security/entitlement_admin.mjs`, never by hand-editing a page |
| Product states to test | `SOLVED_QP` only, `ORAL` only, both, none |
| Payment | **disabled path only.** `BUNDLE` has no approved price and `create-order` refuses it — leave it refusing |
| Access matrix | already encoded in `api/_lib/routes.js`; preview verifies it, does not redefine it |

Two cautions carried from prior evidence, both already learned the hard way:

- **Vercel Deployment Protection SSO makes a gate look like it is passing.** Always probe a
  known-public control on the same deployment, or an SSO redirect will be read as a working
  paywall.
- **Never expose real customer credentials in a test.** Seed synthetic accounts.

---

## 6. Sequence

1. Founder syncs the MARPOL Annex VI corpus (the actual next action — see
   [`CORPUS_SYNC_AND_CONSUMPTION_PLAN.md`](CORPUS_SYNC_AND_CONSUMPTION_PLAN.md)).
2. Implement §3.1 — Planned-soon on the delivery home, plus its guard.
3. Founder approves a preview deployment and sets the three secrets.
4. Run §4.2 against preview with synthetic accounts, payment disabled.
5. Report. **Then** decide about production.

Steps 3–5 need explicit Founder authorisation each time. None is implied by this document.
