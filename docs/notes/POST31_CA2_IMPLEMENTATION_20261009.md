# POST31-CA2 — Published Uday Corrections, Provenance Resolver and Status Cores

**Date:** 9 October 2026 · **Lane:** POST-PART31 (published Uday Engineering Management Notes) · **Status:** LOCAL CANDIDATE — not pushed, not deployed.

**Record location.** No `docs/notes/` directory existed, and the repository has no other records folder for Notes. This record follows the established `docs/<lane>/` pattern used by `docs/study/` (for example `ORAL_TOPIC_ROADMAP_PHASE2A_IMPLEMENTATION_20261008.md`), and `docs/notes/` is the location the CA2 brief names.

## 1. Founder approvals

| Ref | Decision |
|---|---|
| R-CA2-1 | APPROVED. CA2 = CA2-A (three published-Uday corrections) + CA2-B (Layer 1 provenance resolver data + Layer 3 status-core data). |
| R-CA2-2 | APPROVED. Repository location `tools/notes/canonical/`. No LOHAN rows, and no `MERGE-###` / `PCT-*` / `CAND-*` subject IDs, enter production. |
| R-CA2-3 | CONFIRMED. The LOHAN branch's non-Uday CB-1/CB-2 edits (QB, Simon, SQ twins, WA2/WA3, notes-master-index, oralnotes hub) are unlanded proposals. None was cherry-picked. |
| R-CA2-4 | APPROVED. Net-Zero Framework status teaching hub = `miw-notes-mgmt-p22.html#topic-p22-3`. P2 `#topic-9` is the GHG / pricing / policy-mechanics specialisation. |
| R-CA2-5 | ACKNOWLEDGED. CA3 status-consumer conversion is time-sensitive before MEPC 85 / the resumed MEPC/ES.2. No CA3 work is done here. |

## 2. Baseline

`git fetch origin` on 9 Oct 2026 gave origin/main **`b667997e1441fcd019942c2a5cdc413936087f4c`**, unchanged since POST31-CA1 closed, with no intervening commits. Work was done in a fresh worktree `wt-post31-ca2` on branch `feat/post31-ca2-corrections-resolver-status-20261009`, created from origin/main. The LOHAN worktree, the old Uday batch worktrees and the quarantined `b911dd3` checkout were not used. LOHAN commits `335a4a5` and `08a4ba0` were **not** cherry-picked. All three corrections were regenerated on current main.

## 3. Primary-source freshness checks (9 Oct 2026)

| Item | Source | Confirmed |
|---|---|---|
| 2010 HNS Protocol | IMO Status of Treaties 2026 Vol. II, **as at 30 Sep 2026** (HNS PROT 2010, pp. 338–340); IMO press briefing 1 Jun 2026 | Conditions for entry into force met **29 May 2026**. Entry into force **29 Nov 2027** (Art. 21: 18 months). 12 Contracting States. India is not a Party. **Not yet in force.** |
| A.1206(34) | A 34/Res.1206 (full text) | Adopted **3 Dec 2025**. Operative para. 4 **revokes A.1185(33)**. The text contains **no** effective date ("1 January 2026" does not occur). |
| A.1188(33) | A 33/Res.1188 (full text) | 2023 Guidelines on implementation of the ISM Code by Administrations, adopted **6 Dec 2023**. Operative para. 5 **revokes A.1118(30)**. |
| BWM | Status Book Vol. II as at 30 Sep 2026; MEPC.297(72) reg. B-3.8; IMO MEPC 84 summary | EIF 8 Sep 2017. **102** Contracting States (CA1's "95" is not carried forward). India is not a Party. Existing ships D-2 by 8 Sep 2024 at the latest. MEPC 84 **approved** (did not adopt) an amendment package and **adopted** revised G4 guidelines. |
| Net-Zero Framework | IMO MEPC 84 summary; IMO meeting schedule; IMO NZF FAQs | Approved at MEPC 83, **not adopted, not in force**. ISWG-GHG 22 (1–4 Sep) completed. Next: ISWG-GHG 23–27 Nov, MEPC 85 30 Nov–3 Dec, resumed MEPC/ES.2 4 Dec 2026 "[subject to confirmation by MEPC 85]". Entry into force about 16 months after any adoption. No later IMO decision was found. |

Facts held in CA1 or LOHAN drafts that were not re-verified at a primary source today are left out of the status records. Those are BWM tonnage %, e-BWRB / BWRB-form dates, the G4 resolution number and the ES.2 2025 vote count.

## 4. CA2-A — exact corrections

Each correction follows the house convention for published Uday pages: a dated `Correction, 9 October 2026` sentence in the topic's verification note, a topic version bump v1.0 → v1.1, and a newest-first `generated_by` entry in `notes_content_index.json` (plus the existing P21 `editorial_note`). The 8 Oct P2-T9 correction used a plain version stamp, and this package does the same. The older P12-T4 style, which put the explanation inside the stamp, was not used.

**A1 — `miw-notes-mgmt-p4.html#topic-16` (HNS; HTML-only Part)**

| Location | Before | After |
|---|---|---|
| Timeline | `2021 → 2010 HNS Protocol entered into force after reaching ratification threshold` | `2026 → 29 May 2026: conditions for entry into force of the 2010 HNS Protocol met (IMO) — NOT YET IN FORCE` / `2027 → 2010 HNS Protocol scheduled to enter into force on 29 November 2027 (IMO Status of Treaties)` |
| Reg box | `Two-tier liability & compensation regime; entered into force 2021` | `Two-tier liability & compensation regime; NOT YET IN FORCE — conditions for entry into force met 29 May 2026, scheduled to enter into force 29 November 2027` |
| Verification note | — | dated correction sentence appended |
| Version | `Notes-p4 · T16 · v1.0` | `v1.1` |

There is no other in-force claim in topic-16, and no other HNS content was rewritten.

**A2 — `miw-notes-mgmt-p7.html#topic-30` (A.1206(34); HTML-only Part).** All six "effective / took effect 1 Jan 2026" statements were removed. No replacement date was invented.

| # | Location | Change |
|---|---|---|
| 1 | Verification note | "…revokes A.1185(33) and took effect from 1 January 2026." → "…revokes A.1185(33)." (+ dated correction sentence) |
| 2 | Timeline | "(revokes A.1185(33)), effective 1 Jan 2026 — current instrument" → "(revokes A.1185(33)) — current instrument" |
| 3 | Reg box, A.1206(34) | "adopted 3 Dec 2025, effective 1 Jan 2026, revokes A.1185(33)" → "adopted 3 Dec 2025, revokes A.1185(33)" |
| 4 | Reg box, A.1185(33) | "historical instrument, superseded 1 Jan 2026" → "historical instrument, revoked by A.1206(34) (adopted 3 Dec 2025)" |
| 5 | Q&A Q2 | "adopted 3 December 2025 and effective from 1 January 2026." → "adopted 3 December 2025." |
| 6 | Memory box | "2025 resolution (eff. 1 Jan 2026) revokes the 2023 one" → "2025 resolution (adopted 3 Dec 2025) revokes the 2023 one" |
| — | Version | `Notes-p7 · T30 · v1.0` → `v1.1` |

The supersession chain is kept as history. *Recorded, not changed (outside the approved correction):* the same verification note's "A.1185(33) (adopted 6 December 2023, effective 1 January 2024)" and its "2026 transition period" phrasing.

**A3 — `miw-notes-mgmt-p21.html#topic-p21-3` (spec-driven).** Only `tools/notes/specs/p21.json` was edited, at three leaves in topic 3:

- `refs[2]`: "Resolution A.1118(30) — Revised Guidelines…" → "Resolution A.1188(33) — 2023 Guidelines on implementation of the International Safety Management (ISM) Code by Administrations (adopted 6 December 2023; revokes A.1118(30))"
- `verify`: a dated correction sentence appended
- `"version": "1.1"` added

The page was rebuilt with `build_part.py --gated`. The HTML diff is exactly the three corresponding lines, and the generated HTML was not hand-edited. Before the edit, the unmodified spec reproduced the committed P21 HTML byte for byte.

**Manifest:** `generated` is set to 2026-10-09, there is a new `generated_by` entry, and one dated sentence is appended to P21's `editorial_note`. MAN-1 was not repaired: no `topic_count`, `topics[]` or `status` fill, and no reformatting.

**known_traps.md:** this file was not changed. Standing entries already cover both trap families: entry 5 (A.1185(33) superseded by A.1206(34)) and the CLC/HNS entry (2010 HNS Protocol not yet in force; EIF 29 Nov 2027).

## 5. CA2-B — Layer 1 resolver (data)

All files are in `tools/notes/canonical/` and were derived from the candidate tree (b667997 + CA2-A).

| File | Rows | Schema |
|---|---|---|
| `source_nodes.csv` | **118** (31 Parts) | `source_node_key,series,file,anchor,part,ordinal_in_part,title,anchor_scheme,publication_status,source_commit` |
| `display_aliases.csv` | **472** (118 × badge/toc/version/phase1a_key) | `source_node_key,alias_type,alias_value,source` |
| `inbound_baseline.csv` | **449** rows = **4,000** references from **20** referrer files, **0 broken**. Of these, 3,995 come from the 19 pre-existing referrers and are unchanged from CA1; 5 come from this record. | `referrer_file,target_source_node_key,count,source_commit` |

- **Identity:** `source_node_key` = `file#anchor` exactly as published, e.g. `meoclass1/oralnotes/miw-notes-mgmt-p12.html#topic-51`.
- **`anchor_scheme`:** `GLOBAL` (P1–P11), `GLOBAL_ANCHOR_LOCAL_LABELS` (P12) or `PART_LOCAL` (P13–P31).
- **`publication_status`:** `PUBLISHED_LIVE`, meaning the node is present on origin/main.
- **`source_commit`:** the base commit (`b667997…`) at which the node identity was established. CA2-A changes no file, anchor, title or ordinal, and the validator re-checks every row against the rendered page.
- **P12 mismatch, recorded explicitly.** The anchors are `#topic-50…54`. The badge reads "Part 12 · Topic 1…5", the TOC "T1…T5", and the version stamp "P12-T1…T5". The Phase 1A key is `U-P12-T01…05`. All of these resolve to the real global anchor `#topic-(49+n)`.
- **Alias scope.** badge/toc/version aliases are page-scoped, with lookup on (file, type, value). `phase1a_key` is global. No alias is a key.
- **Inbound method.** The scan covers every tracked file except `tools/notes/canonical/` and counts every `miw-notes-mgmt-pN.html#anchor` occurrence. It uses the same method as CA1. The pre-existing referrers give exactly 3,995 references, equal to CA1's measurement on b667997, so CA2-A added and removed no references. The baseline was regenerated from the staged index, so it describes the landing commit, including the 5 references in this record.

## 6. CA2-B — Layer 3 status cores (data only; not rendered)

| Core | Label (as_of 2026-10-09) | Consumers (`file#anchor`) |
|---|---|---|
| `STATUS-HNS2010` | SCHEDULED — NOT YET IN FORCE | P4 `#topic-16` (teaching), P8 `#topic-36` (status-dependent: presents the HNS Convention as governing; for CA3) |
| `STATUS-BWM` | IN FORCE — D-2 SCHEDULE COMPLETE — MEPC 84 PACKAGE APPROVED, NOT ADOPTED | P12 `#topic-51` |
| `STATUS-NZF` | APPROVED (MEPC 83) — NOT ADOPTED — NOT IN FORCE | **hub P22 `#topic-p22-3`**; P2 `#topic-9` (specialisation); P24 `#topic-p24-1`, P28 `#topic-p28-3`, P29 `#topic-p29-3`, P31 `#topic-p31-1` (status prose); P25 `#topic-p25-1`, P23 `#topic-p23-3` (pointers; P23 still points to P2, CA-A03). P22 `#topic-p22-2` is excluded as a historical fact. |

Every core holds `status_id`, `subject`, `label`, `as_of`, `authority`, `authority_url_or_reference`, `history`, `next_decision_or_trigger`, `review_trigger` and `consumers` (objects whose `source_node_key` is a Layer 1 key), plus compact `status_detail`. Consumers were found by scanning the current Uday topic bodies. They were not copied from CA1. No learner page was converted.

## 7. Validator and mutation tests

`tools/notes/canonical/validate_canonical.py` fails closed: a missing file, wrong header, bad row or any rule failure gives exit 1. It checks:

- every rendered topic-block id is registered, and every key resolves to a rendered topic
- keys have both a file and an anchor (anchor-only keys are rejected), and keys are unique
- part, ordinal, title and scheme match the page
- aliases resolve to exactly one node, are actually rendered for that node, are complete, and never have key or anchor form
- P12 local labels resolve to `#topic-(49+n)`
- baseline targets resolve, and a **live re-scan** of tracked files finds 0 broken
- status cores are only the three approved ones, with required fields, and every consumer resolves
- no `MERGE-###`/`PCT-*`/`CAND-*` and no LOHAN page appears anywhere in the data

Duplicate anchor strings in different files are allowed.

`tools/notes/canonical/test_validate_canonical.py` runs **23/23 PASS**. Each case mutates in-memory copies of the real data, proves its condition was false before and true after, and **requires** the rule's own error code:

| Case | Mutation | Required error code |
|---|---|---|
| M1 / M1b | anchor-only key / `#anchor` | `KEY_WITHOUT_FILE` |
| M2 | duplicate key | `DUPLICATE_KEY` |
| M3 / M3b | alias resolves to two nodes (global / page-scoped) | `ALIAS_AMBIGUOUS` |
| M4 | nonexistent anchor | `KEY_NOT_RENDERED` |
| M5 | rendered topic removed | `RENDERED_NOT_REGISTERED` |
| M6 / M6b | P12 "P12-T2" / "U-P12-T02" → real node `p1#topic-2` | `P12_LOCAL_TO_WRONG_ANCHOR` |
| M7 / M7b | broken baseline / live inbound target | `INBOUND_BROKEN` / `LIVE_INBOUND_BROKEN` |
| **M8** | **unmutated control** | **PASS, 0 errors** |

Additional cases M9–M17 cover: alias used as a key, MERGE id, LOHAN row, new unregistered topic, unapproved core, unresolved consumer, alias equal to an anchor, P12 badge rewritten, and a missing required field. **R8+** is a positive test: the same anchor string in two files passes.

As an anti-vacuity check, I ran the harness against a stub validator that reports nothing. All 21 mutation cases then FAIL, and only the control and the positive case pass.

## 8. Gate results (candidate vs pristine baseline b667997)

| Gate | Baseline | Candidate |
|---|---|---|
| P21 `validate_spec` / `build_part --gated` / `health_check --require-gate` | OK / — / 0 errors | OK / built / **0 errors** |
| P4 / P7 `health_check` (legacy format, DISC-004) | 11 / 7 errors | **11 / 7, identical messages** |
| P4 / P7 structural (tag balance, topic ids, section heads) | 0 balance errors | **0**. Topic ids and heads unchanged. Tag delta is only the added `<strong>`/timeline `<span>`. |
| Determinism P19–P31 `--gated` → scratch, byte-compare | 13/13 identical (P21 = control) | **13/13 identical** (P21 compared with its new committed output) |
| `test_notes_root_resolution.py` | PASS | **PASS** |
| `test_spec_parts_discovery.py` | PASS | PASS |
| `check_master_index.py` (balance report) | 0 errors | identical |
| Legacy manifest-name guard | OK | OK |
| Oral `test_notes_controls.py` | 106 / 1 failure | **106 / 1, the same failure** |
| Oral `test_oral_controls.py` | 341 / 1 failure | **341 / 1, the same failure** |
| Oral `validate_correction_pass2.py` (pins P7 content) | — | 133 checks, 0 FAIL |
| `tools/security/regulatory_facts.test.mjs` | 20/20 | **20/20** |
| `git diff --check` | clean | clean |
| `validate_canonical.py` | — | **PASS** |

**Pre-existing failure, not fixed here:** the Oral control "no Oral Note text exercises the ME-GI / ME-GA family" (CQ-ORAL-1) fails in the same way on baseline and candidate. CA2 introduces no new Oral failure.

## 9. Rollback

This is a single local commit. To reject it before landing, delete the branch, or `git revert <sha>` after landing. Reverting restores P4/P7/P21 v1.0 (including the stale statements) and removes `tools/notes/canonical/`. Nothing else depends on the new data, because no page renders it.

## 10. Boundaries and claims

- **No canonical-ID claim.** The resolver is Layer 1 provenance only. No subject or canonical topic ID, no `MERGE-###`/`PCT-*`/`CAND-*`, and no LOHAN row is in the repository. D-L4 remains open.
- There is no cross-reference block, no index/crossref/relationship change, no UI-1/UI-2 cleanup and no MAN-1 repair.
- P2, P22, P23, P24, P25, P28, P29 and P31 are unedited. STATUS-NZF consumer conversion is CA3.
- For CA3: the P8 `#topic-36` HNS wording, the P23 `#topic-p23-3` pointer, the A.1185(33) "effective 1 January 2024" line in P7, and the remaining CB-3…CB-6 items.
