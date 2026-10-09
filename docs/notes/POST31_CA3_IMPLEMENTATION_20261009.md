# POST31-CA3 — Shared Status Consumers and Bounded Currentness Corrections

**Date:** 9 October 2026 · **Lane:** POST-PART31 (published Uday Engineering Management Notes) · **Status:** LOCAL CANDIDATE — not pushed, not deployed.

CA3 is the first live consumer package for the CA2 status-core architecture. Selected published Uday topics now carry a static, dated status line that agrees with the Layer 3 record, and they link to that subject's teaching node. CA3 also corrects the bounded adjacent currentness defects listed in the CA2 handoff. It is **not** a canonical subject-ID implementation, LOHAN publication, Notes consolidation, syllabus mapping, gap-note production, SolvedQP integration or QB correction.

## 1. Base

`git fetch origin` on 9 Oct 2026 gave origin/main **`48131c9b9453653e2df15b81447d0adb7efd4a50`** (POST31-CA2), unchanged from the expected baseline, with no intervening commits, so no overlap classification was needed. Work was done in a fresh worktree `wt-post31-ca3` on branch `feat/post31-ca3-status-consumers-20261009`, created from origin/main. The LOHAN worktree, the CA2 worktree and the quarantined `b911dd3` checkout were not used. Baseline gates were run in a separate pristine detached worktree at the same SHA.

## 2. Primary-source freshness (9 Oct 2026, before any edit)

| Core | Sources | Result |
|---|---|---|
| STATUS-NZF | IMO NZF FAQs; IMO meeting schedule; IMO MEPC 84 summary; imo.org news search | **Unchanged.** Approved at MEPC 83, not adopted, not in force. ISWG-GHG 23–27 Nov, MEPC 85 30 Nov–3 Dec, MEPC.ES/2 4 Dec "[subject to confirmation by MEPC 85]". Entry into force expected 16 months after any adoption. No later IMO decision was found. |
| STATUS-HNS2010 | IMO press briefing 1 Jun 2026; Status of Treaties 2026 Vol. II as at 30 Sep 2026, p. 338 | **Unchanged.** Conditions met 29 May 2026; entry into force 29 Nov 2027; 12 Contracting States; not yet in force. |
| STATUS-BWM (narrow) | Status of Treaties Vol. II pp. 360–365; IMO MEPC 84 summary | **Unchanged.** Entry into force 8 Sep 2017. Art. 18(1): not less than **thirty** States with ≥35% of tonnage. **102** Contracting States; India not listed. MEPC 84 approved (did not adopt) an amendment package and adopted revised G4 guidelines. |

No label, `as_of`, history, next trigger or entry-into-force fact changed. The only status-JSON edits are consumer metadata and one NZF review trigger (§7).

## 3. Real consumer set

Every consumer was read from the current status records, resolved through `source_nodes.csv`, and confirmed as a rendered topic-block: 11 consumers, all resolved. A sweep of all 118 Uday topic-blocks for each subject found four further mentions. None of them is a status consumer:

- **P22 `#topic-p22-2`**: the October 2025 adjournment, a dated historical fact (already excluded by STATUS-NZF).
- **P23 `#topic-p23-5`**: "FuelEU/GFI are well-to-wake", an accounting-basis line with no status claim.
- **P3 `#topic-15`**: uses "HNS" as a cargo class, not the liability instrument.
- **P9 `#topic-40`**: covers the OPRC-HNS Protocol 2000, a different instrument outside the record's scope.

## 4. Consumer action matrix

| Status | Consumer (`file#anchor`) | Role | Mode | Action |
|---|---|---|---|---|
| NZF | `miw-notes-mgmt-p22.html#topic-p22-3` | TEACHING_HUB | spec | KEEP_HUB (+ dated hub line) |
| NZF | `miw-notes-mgmt-p2.html#topic-9` | SPECIALISATION_STATUS_PROSE | legacy | SHORT_SUMMARY_PLUS_HUB |
| NZF | `miw-notes-mgmt-p23.html#topic-p23-3` | POINTER | spec | REPLACE_STATUS_WITH_HUB_POINTER |
| NZF | `miw-notes-mgmt-p24.html#topic-p24-1` | STATUS_PROSE | spec | SHORT_SUMMARY_PLUS_HUB |
| NZF | `miw-notes-mgmt-p25.html#topic-p25-1` | POINTER | spec | REPLACE_STATUS_WITH_HUB_POINTER (link) |
| NZF | `miw-notes-mgmt-p28.html#topic-p28-3` | STATUS_PROSE | spec | SHORT_SUMMARY_PLUS_HUB |
| NZF | `miw-notes-mgmt-p29.html#topic-p29-3` | STATUS_PROSE | spec | SHORT_SUMMARY_PLUS_HUB |
| NZF | `miw-notes-mgmt-p31.html#topic-p31-1` | STATUS_PROSE | spec | SHORT_SUMMARY_PLUS_HUB |
| HNS2010 | `miw-notes-mgmt-p4.html#topic-16` | TEACHING_NODE | legacy | NO_CHANGE (pointer target) |
| HNS2010 | `miw-notes-mgmt-p8.html#topic-36` | STATUS_DEPENDENT | legacy | CORRECT_STATUS_PLUS_HUB |
| BWM | `miw-notes-mgmt-p12.html#topic-51` | TEACHING_NODE | legacy | CORRECT_STATUS_PLUS_HUB (self) |

The full matrix, with the pre-CA3 status text of each consumer, is `CA3_STATUS_CONSUMER_MATRIX_20261009.csv` in the review pack. Authoring mode was taken from the current repository: P19–P31 have specs, while P2, P4, P7, P8 and P12 are HTML-only. No spec was invented for a legacy Part.

## 5. Presentation pattern and hub decisions

Each consumer that states status now carries exactly one **static marker**:

```
<div|span class="status-current" data-status-id="STATUS-NZF" data-as-of="2026-10-09" …>
  CURRENT STATUS · As of 9 October 2026: IMO Net-Zero Framework — APPROVED (MEPC 83) — NOT ADOPTED — NOT IN FORCE.
  Full current treatment, including the next decision point: <a href="miw-notes-mgmt-p22.html#topic-p22-3">Part 22 · Topic 3</a>.
</div|span>
```

- The label is copied verbatim from the status record, and the date equals the record's `as_of`.
- Pages never fetch `tools/notes/canonical/status/*.json`. Those files are repository-only and are not public routes.
- Markers use inline style rather than a new CSS class. The spec-driven Parts share an extracted shell, and a new class there would change every rebuilt Part.
- Links use the existing Part `file#anchor`. No new identifier appears on any page.

**One status source.** The forward meeting schedule (MEPC 85 / resumed MEPC/ES.2) is stated **only in the hub** (P22-T3). Outside the hub, undated forward-looking schedule lines became hub pointers. Dated past facts were kept as history: MEPC 83, the October 2025 adjournment, MEPC 84, and the dated "8 Oct 2026" one-liners in P31. Topic-specific engineering, CII, fuel, pricing and exam content is unchanged.

- **NZF hub:** P22 `#topic-p22-3` (Founder R-CA2-4). P2 `#topic-9` stays the pricing / policy-mechanics specialisation and is explicitly labelled as not the status reference.
- **HNS / BWM:** no hub designation was made. That would be a new architecture decision, so the records keep `TEACHING_NODE`, and there is no `teaching_hub` field. P8 points to the fuller HNS treatment in P4 `#topic-16` through a declared `requires_pointer_to`. P12 is the only BWM node, so its marker has no pointer.

## 6. Exact content changes

| Topic | Change | Version |
|---|---|---|
| P22 T3 (hub) | Dated hub marker at the top of "The Net-Zero Framework — Current Status"; dated status-check sentence in the verify note | 1.1 → 1.2 |
| P2 T9 | Marker + P22 link after the verify note. The undated forward lines become hub pointers: timeline "4 Dec 2026 …" row → "Next → current status and next decision point: Part 22 · Topic 3"; reg box; Q1 tail; memory line; revision-table "Formal adoption" row. A dated update sentence was added. This also adds the missing P2 → P22 link (CA1 CA-A09). | 1.1 → 1.2 |
| P23 T3 | Verify-note pointer "Part 2 Topic 9 covers the draft Net-Zero Framework …" → status in **Part 22 · Topic 3** (link); P2-T9 named for pricing mechanics only (CA1 CA-A03) | 1.0 → 1.1 |
| P24 T1 | Marker inside the draft-GFI box (the existing paragraph is unchanged; it is a pinned clean control in `regulatory_facts.test.mjs`) | 1.0 → 1.1 |
| P25 T1 | "see Part 22 Topic 3" becomes a link | 1.0 → 1.1 |
| P28 T3 | ESG-table line → inline marker + link | 1.0 → 1.1 |
| P29 T3 | Reg-box entry → inline marker + link; the meeting schedule is removed | 1.0 → 1.1 |
| P31 T1 | Timeline "30 Nov–4 Dec 2026 (scheduled)" row → "Next → … Part 22 · Topic 3"; the paragraph's schedule clause is removed and a marker added | 1.1 → 1.2 |
| **P8 T36 (HNS)** | Six statements that presented the HNS Convention as the regime that currently governs non-persistent oil spills are corrected: why-it-matters, reg box ("Governs …" → **NOT YET IN FORCE**, scheduled 29 Nov 2027; once in force it will cover …), comparison table (national law until entry into force), CE Oral Tip, Q1 and memory line. Dated correction note, marker + link to P4 `#topic-16`. CLC/FUND figures are unchanged. | 1.0 → 1.1 |
| **P12 T2 (`#topic-51`, BWM)** | Art. 18 threshold "35 states / 35%" → **30 States / 35%** (verify note and timeline). Timeline gains "8 Sept 2024 — phase-in complete (reg. B-3, MEPC.297(72))" and "2026 — MEPC 84 approves (does not adopt) a package of amendments; revised G4 adopted". "No corrections were required" is replaced by a dated correction note. A dated marker gives 102 Contracting States (as at 30 Sep 2026) and says India is not a Party. No new BWM note; LOHAN text was not used. | 1.0 → 1.1 |
| **P7 T30** | See §8 | 1.1 → 1.2 |

Every corrected topic has a dated verify-note sentence, following the CA2 convention. `notes_content_index.json` gets only a new newest-first `generated_by` entry (`generated` was already 2026-10-09). MAN-1 was not repaired, and no topic arrays or counts were filled.

## 7. Status-core changes

The three cores and their IDs are unchanged, and no status ID was added. In `consumers[]`, each entry gained:

- `marker` (true/false): whether the topic-block must carry a marker;
- `requires_pointer_to`: for NZF, always the hub; for P8, P4 `#topic-16`;
- an updated `note`.

STATUS-NZF `review_trigger`: the completed "CA3 must complete before MEPC 85" item was replaced with the maintenance rule. On any change, update the record, the hub prose and every marker. The validator enforces that each marker's as-of equals the record's `as_of`.

## 8. P7 residual adjudication (A.1185(33))

| Wording | Primary source | Verdict |
|---|---|---|
| "A.1185(33) (adopted 6 December 2023, **effective 1 January 2024**)" | A 33/Res.1185: adopted 6 Dec 2023; operative paras 1–4 (ADOPTS, INVITES, REQUESTS, **REVOKES A.1155(32)**); no effective date anywhere in the resolution. "2 January 2024" is the document's issue date. | **CORRECTED**: "effective 1 January 2024" removed |
| "accepted orally at Kochi MMD during the **2026 transition period**" | Neither A.1185(33) nor A.1206(34) (CA2-held text) contains "transition" or defines a transition period | **REMOVE**: the phrase and the unverifiable acceptance claim were removed. Sentence now: "Candidates may still meet A.1185(33) in older study material and appeal documents, but should lead with A.1206(34) as the current instrument." |

The six A.1206(34) corrections from CA2 were not reopened.

## 9. BWM adjudication

The current status was verified at primary source (§2). On P12, three stale or missing facts were fixed: the threshold, the phase-in completion and the MEPC 84 package. Facts not re-verified today were left out of the page, as in CA2: the tonnage %, e-BWRB / BWRB-form dates, the G4 resolution number, and Indian notification details. The P12 teaching content is unchanged: the D-1/D-2 standards, the B-4 distances, the BWRB-vs-logger PSC check, and the Q&A.

## 10. Validator design — `tools/notes/canonical/validate_status_consumers.py`

This is a new, bounded validator. Page semantics are kept out of `validate_canonical.py`, which it imports only for shared loaders. It is a pure `validate(status, node_keys, pages)`, fails closed and makes no internet access.

| # | Rule | Code |
|---|---|---|
| 1 | every consumer / pointer target resolves through `source_nodes.csv` and is rendered | SC_CONSUMER_UNRESOLVED |
| 2 | `teaching_hub` present → exactly one TEACHING_HUB, equal to it; absent → no TEACHING_HUB role | SC_HUB_COUNT |
| 3 | STATUS-NZF hub = P22 `#topic-p22-3` | SC_NZF_HUB_WRONG |
| 4 | each consumer with `requires_pointer_to` links to it (inside its marker when it has one); for NZF the target must be the hub | SC_HUB_POINTER_MISSING / SC_POINTER_TARGET_WRONG |
| 5 | no NZF consumer presents P2 `#topic-9` as the status reference (marker link, or a sentence naming P2-T9 with NZF/status and not the hub) | SC_NZF_STATUS_POINTS_TO_P2 |
| 6 | before 29 Nov 2027, no HNS consumer sentence says HNS is in force / governs without a qualifier (dated correction sentences quoting old wording are exempt) | SC_HNS_IN_FORCE_CLAIM |
| 7 | every marker has `data-as-of` and the matching visible "As of D Month YYYY"; it must equal the record `as_of` and carry the record label | SC_MARKER_NO_AS_OF / SC_MARKER_STALE / SC_MARKER_LABEL |
| 8 | no page references `tools/notes/canonical` or `STATUS-*.json` | SC_PRIVATE_PATH |
| 9 | every status id on a page is an approved core | SC_UNKNOWN_STATUS_ID |
| 10 | no MERGE-### / PCT-* / CAND-* / CANON-* on any Uday page | SC_CANONICAL_ID_ON_PAGE |
| + | declared markers exist; undeclared, duplicate or out-of-block markers fail; every Uday `file#anchor` link inside a consumer resolves | SC_MARKER_MISSING / _UNDECLARED / _DUPLICATE, SC_LINK_UNRESOLVED |

Run against the pristine base (48131c9), rules 5 and 6 report exactly the defects CA3 fixes: P23 → P2-T9, and P8 "HNS Convention — Governs …". On the candidate it gives **PASS** (31 pages, 11 consumers, 8 markers).

## 11. Mutation tests — `test_validate_status_consumers.py`

**18/18 PASS.** Each case deep-copies the real candidate data, proves the mutation changed it, and requires the rule's own code.

| Case | Mutation | Required code |
|---|---|---|
| M1 | P24 marker links to P2 `#topic-9` instead of P22 | SC_NZF_STATUS_POINTS_TO_P2 + SC_HUB_POINTER_MISSING |
| M2 | second NZF TEACHING_HUB | SC_HUB_COUNT |
| M3 | "The HNS Convention is in force and governs these claims." on P8 | SC_HNS_IN_FORCE_CLAIM |
| M4 | marker as-of removed | SC_MARKER_NO_AS_OF |
| M5 | P23 link → `#topic-p22-9` (nonexistent) | SC_LINK_UNRESOLVED |
| M6 | link to `/tools/notes/canonical/status/STATUS-NZF.json` | SC_PRIVATE_PATH |
| M7 | "MERGE-072" on P31 | SC_CANONICAL_ID_ON_PAGE |
| M8 | `data-status-id="STATUS-ECA"` | SC_UNKNOWN_STATUS_ID |
| **M9** | **unmutated candidate** | **PASS, 0 errors** |
| M10–M18 | record re-dated / label drift / marker on undeclared node / P23 reverted to CA2 wording / P4 "entered into force in 2021" re-introduced / NZF hub moved to P2 / declared marker removed / pointer to a non-teaching node / unregistered consumer key | SC_MARKER_STALE, SC_MARKER_LABEL, SC_MARKER_UNDECLARED, SC_NZF_STATUS_POINTS_TO_P2, SC_HNS_IN_FORCE_CLAIM, SC_NZF_HUB_WRONG, SC_MARKER_MISSING, SC_POINTER_TARGET_WRONG, SC_CONSUMER_UNRESOLVED |

**Anti-vacuity:** with `validate()` replaced by a stub that reports nothing, all 17 mutation cases FAIL and only M9 passes.

## 12. Inbound baseline (regenerated after final edits)

| | Before (CA2, 48131c9) | After (CA3 candidate) |
|---|---|---|
| referrer files | 20 | 34 |
| rows | 449 | 474 |
| total references | 4,000 | 4,035 |
| broken | 0 | **0** |

The method is CA2's `scan_inbound`: every tracked file, excluding `tools/notes/canonical/`, regenerated from the staged index so that this record is counted. Rows carry `source_commit` = the CA3 base `48131c9…`, following CA2's convention that the baseline records the base it was generated on. This is why the git diff shows every row changed, even though only the rows above changed in content. The +35 references are fully accounted for. 23 are the new learner-facing links: P2 +7, P8 +2 (after its 1 pre-existing), P23/P24/P25/P28/P29 +1 each and P31 +2 in the HTML, plus the same links in specs p23–p31 (+7). The other 12 are mentions in this record. The 14 new referrer files are those pages and specs plus this record. No reference was removed.

`source_nodes.csv` and `display_aliases.csv` are **unchanged**. No anchor, title, topic or ordinal changed, and every version token (P22-T3, T9, …) is unchanged; only the `v1.x` suffix moved, and the alias data does not record it.

## 13. Test results (pristine base 48131c9 vs candidate)

| Gate | Base | Candidate |
|---|---|---|
| `validate_canonical.py` | PASS | **PASS** |
| `test_validate_canonical.py` | 23/23 | **23/23** |
| `validate_status_consumers.py` | (new) | **PASS** |
| `test_validate_status_consumers.py` | (new) | **18/18**; null-validator 1/18 |
| `validate_spec` P22–P25, P28, P29, P31 | OK | **OK** |
| `health_check --require-gate` P22–P25, P28, P29, P31 | 0 errors | **0 errors** |
| Legacy `health_check` P2 / P4 / P7 / P8 / P12 (DISC-004 legacy format) | 10 / 11 / 7 / 9 / 6 | **identical messages** (only the byte-size header differs) |
| Legacy structure P2 / P7 / P8 / P12 | 0 balance errors | **0**; topic ids and section heads unchanged |
| Gate safety, all 11 edited pages | — | `<head>` (robots, GA4, gate) and footer-to-end **byte-identical** |
| Determinism P19–P31 `--gated` | 13/13 identical | **13/13**: P19–P21, P26, P27, P30 byte-identical to base; P22–P25, P28, P29, P31 byte-identical to the new committed HTML |
| `test_notes_root_resolution.py` / `test_spec_parts_discovery.py` | PASS / PASS | PASS / PASS |
| `check_master_index.py` (balance report) | — | identical |
| Legacy manifest guard | OK | OK |
| `validate_correction_pass2.py` | 133, 0 FAIL | 133, 0 FAIL |
| `regulatory_facts.test.mjs` | 20/20 | **20/20** |
| Oral `test_notes_controls.py` / `test_oral_controls.py` | 106/1, 341/1 | **106/1, 341/1**, same failure |
| `git diff --check` | — | clean |

**Known failure, not fixed here:** the Oral control "no Oral Note text exercises the ME-GI / ME-GA family" (CQ-ORAL-1) fails identically on base and candidate.

**Not done:** no rendered visual check. The in-app preview shows local files only as static snapshots. The change is static HTML, verified structurally and by the validators.

## 14. Out of scope, observed

- P2 `#topic-9` still cites the 2023 Strategy as **MEPC.385(80)** (CA1 DSC-01; seven other nodes say MEPC.377(80)), and its draft Z-factor table (DSC-02) is also unchanged. These are not status-consumer items and need their own correction package.
- CB-3…CB-6, CB-T anchor hygiene, the canonical subject-ID freeze and the relationship layer are **not started**. CA3 creates no authority for them.

## 15. Rollback and claims

This is a single local commit. To reject it before landing, delete the branch, or `git revert <sha>` after landing. Reverting restores the CA2 pages and records and removes the new validator and test.

**No canonical-ID claim.** Consumers are still identified by the published `file#anchor`. No MERGE-### / PCT-* / CAND-* / CANON-* identifier and no LOHAN row or text was introduced. No QB, SolvedQP, study-mapping, index, crossref or relationship-registry file was touched.
