# LOHAN F3 + Node Security-Suite Control Hardening

**Date:** 10 October 2026 · **Lane:** A (LOHAN publication controls) · **Status:** LOCAL CANDIDATE. Not pushed, not deployed.
**Authority:** local validator and test hardening only. This task does **not** authorise D-L4 publication, manifest/index activation, a LOHAN publication-status transition, canonical subject IDs, Uday↔LOHAN relationships, a push or a deployment.

## 1. Base

| Role | Commit |
|---|---|
| Production baseline (origin/main, unchanged at fetch) | `d8b48e8116ba5285969eaa609f91a4aac71cb2f8` |
| Parent of this candidate: POST31 LOHAN source admission | `51c1c07f7f32f95f8cbcfce6d3cd6bf9db353f4b` |
| LOHAN content tip (P12 F1 successor), used for combined qualification only | `0364cea9cb33291710aa76d21fc5a470ea0ccb4a` |
| Oral LOHAN classification, used for combined qualification only | `9d20df08bcc50896525301c8c909afb445ab4d19` |

## 2. F3: reverse-reference isolation

**Gap (independent audit, mutation IM9).** `scan_inbound` matches only `miw-notes-mgmt-pN.html#anchor`, so the live check looks at references whose *target* is a Uday page. A Uday page linking *to* a LOHAN page was never examined. It passed `validate_canonical`, `validate_status_consumers`, the Oral controls and `link_integrity`.

**Decision: a referrer-driven, registration-based rule. No filename ban.**

| Question | Decision | Why |
|---|---|---|
| What is a Uday→LOHAN reference? | Any `lohan-notes-pN.html[#anchor]` occurrence in a **Uday-series source file**: `meoclass1/oralnotes/miw-notes-mgmt-pN.html`, its `SQ/` twin, or `tools/notes/specs/pN.json` | Classified by the referrer's series, derived from its path the same way POST31 derives LOHAN referrers. Records, tools, hub indexes and LOHAN→LOHAN navigation are not series cross-references |
| When is one valid? | When it equals a registered `inbound_baseline.csv` row (referrer → LOHAN `file#anchor`, same count), in both directions | Mirrors `LOHAN_INBOUND_DRIFT` for the opposite direction. Uses the existing registry, so no new file, column or schema |
| May such a row be registered today? | No. `REGISTRABLE_DIRECTIONS = {(LOHAN, UDAY)}`. A Uday→LOHAN row still fails `CROSS_SERIES_REFERENCE` | Governance has authorised no Uday↔LOHAN relationship (POST31 admission, D-L4 open). Authorising later is one reviewed line plus its rows, and the live/registered checks then apply unchanged (proved by the RA cases) |
| Page-level links (no anchor) | Never match a registration, so they fail `CROSS_SERIES_UNREGISTERED` | Layer 1 identity is the exact `file#anchor` (FD-P1-02) |
| Anchor-only registered targets | `KEY_WITHOUT_FILE` (in addition to `INBOUND_BROKEN`) | 35 anchor strings collide across series, so an anchor alone is not an identity |
| Inferred relationships / subject IDs | None. No data row added or changed | Out of scope; `FORBIDDEN_ID_RE` unchanged |

New validator codes:

| Code | Fires when |
|---|---|
| `CROSS_SERIES_UNREGISTERED` | a live Uday→LOHAN reference (node- or page-level) does not equal a registered row |
| `CROSS_SERIES_BAD_IDENTITY` | a live or (authorised) registered target is not a registered node of an admitted LOHAN page: wrong part in the anchor, unadmitted page, unregistered node, Uday-style anchor |
| `CROSS_SERIES_DRIFT` | a registered Uday→LOHAN row is no longer live |
| `KEY_WITHOUT_FILE` (extended) | an inbound target is anchor-only |

`--no-live` skips the cross-series scan along with the live inbound scan, as before.

**Existing references unchanged.** Live Uday→LOHAN references: 0 in all 45 Uday source files on the production baseline, the POST31 candidate and the combined tree. LOHAN→Uday stays at 128 references / 57 targets / 0 broken, and Uday rows and the inbound baseline are byte-identical. `referrer_series` now also returns `('UDAY', part)` for Uday-series paths. Previously these paths were `('OTHER', None)`, and no caller distinguished the two.

**Tests.** `test_validate_canonical.py` adds 24 R-series cases (60 → 84). Each R case must report **exactly** its expected codes, a stricter bar than the M/L cases, so a case cannot pass on an unrelated failure. RA cases temporarily authorise UDAY→LOHAN to prove the rule is registration-based (registered + live passes, everything else still fails). R-pos1/R-pos2 prove LOHAN→LOHAN and governance-record mentions are not caught.

## 3. Node security suite in CI

**Finding (audit F1 process note).** `node --test tools/security/*.test.mjs` is a gate in the Oral release runner (`tools/oral/oral_release_gates.py`, `node_security_tests`), but no GitHub workflow runs it. LOHAN qualifications ran neither, so P12's `regulatory_facts` failure went unseen.

**Decision.** Add one job, `node-security-suite`, to the existing `.github/workflows/qb-health-check.yml`. The QB job is unchanged (0 lines removed). The new job shares the workflow's daily schedule and `workflow_dispatch`, so it checks `main` daily and any pushed branch on demand. It needs no secrets.

| Requirement | How |
|---|---|
| Node/runtime | `actions/setup-node@v4`, Node 24 (`package.json` engines `24.x`). Built-in modules only, so no `npm install`. Tests also call `git ls-files` and `python3` (present on `ubuntu-latest`) |
| Regulatory-facts and link-integrity included | The step fails if `regulatory_facts.test.mjs` or `link_integrity.test.mjs` is missing. Every `*.test.mjs` is passed explicitly (never the directory: Node 24 rejects it) |
| Missing Node reported | Explicit `::error::` and exit 1 |
| No skipped suite presented as a pass | Fails on zero executed tests, and on a test file that defines no tests (Node reports such a file as one passing test). Skipped/todo tests become a warning plus the step summary and are never counted as passes |

Locally (Windows or Linux, Node ≥ 21): `node --test "tools/security/*.test.mjs"`. Run it for any change that adds or edits files under `meoclass1/oralnotes/`.

**Not changed:** `tools/oral/**` (the Oral release gate already carries the suite), `package.json`, any other workflow.

## 4. Results

| Tree | canonical | canonical tests | status consumers | status tests | Node security |
|---|---|---|---|---|---|
| A. production `d8b48e8` (reference; candidate not applicable without POST31) | PASS | 23/23 | PASS | 18/18 | 627 pass / 0 fail / 1 skip |
| B. POST31 `51c1c07` before → this candidate | PASS → PASS | 60/60 → 84/84 | PASS → PASS | 18/18 → 18/18 | 627/0/1 → 627/0/1 |
| C. combined (`0364cea` + POST31 + Oral) before → + this candidate | PASS → PASS | 60/60 → 84/84 | PASS → PASS | 18/18 → 18/18 | 627/0/1 → 627/0/1 |

The one skipped Node test is pre-existing on every tree (`templates/issue_shell.html` lives in the factory repo). Full evidence, on-disk mutation proofs and the P12 F1 preservation proof are in the review package `LOHAN_F3_SECURITY_CONTROL_HARDENING_REVIEW_20261010.zip` (J: sandbox, not in Git).

## 5. Not done here (still D-L4 or other lanes)

F4 (ME-GI/ME-GA Oral control; read-only assessment only, Oral lane owns `tools/oral/**`), manifest and index activation (F5/B7), the gated LOHAN rebuild (F8), the LOHAN publication-status transition, the Oral secondary-layer policy (F6/F7) and the study spine (F9).
