# POST31-CA4W — P2 Topic 9: 2023 GHG Strategy Resolution and Adopted CII Z Factors

**Date:** 9 October 2026 · **Lane:** POST-PART31 (published Uday Engineering Management Notes) · **Status:** LOCAL CANDIDATE — not pushed, not deployed.

CA4W corrects one published Uday topic: P2 `#topic-9` (`miw-notes-mgmt-p2.html#topic-9`). It changes two facts:

- **W1:** the 2023 IMO GHG Strategy was cited as the wrong resolution;
- **W2:** the 2027–2030 CII reduction (Z) factors were taught as draft and approximate, although they are adopted.

The wording authority is the CA4W readiness sheet (`POST31_CA4W_IMPLEMENTATION_READINESS_20261009.md`, items W1.1–W1.3 and W2.1–W2.16). CA4W is not a canonical subject-ID implementation, a LOHAN publication, a Notes consolidation or an NZF status refresh.

## 1. Founder decisions

| ID | Decision |
|---|---|
| D-CA4-1 | **APPROVED.** CA4W scope is exactly P2 `#topic-9`: the Strategy resolution and the 2027–2030 Z-factor treatment. 4 paths. |
| D-CA4-2 | **No extensions.** P1-T2, P1-T6 and the oralnotes index PSC card are excluded and belong to later packages. |
| D-CA4-3 | **Keep the P2-T9 title as-is**, including "(MEPC-83)". Anchor, title, `data-kw`, `source_nodes.csv` and `display_aliases.csv` are unchanged. |
| D-CA4-4 | Later sequencing noted: CA5-LIAB → CA5-TECH → CA5-GHG → remaining MSA / pointer / UI work. No authority for those packages is created here. |
| D-CA4-5 | CB-T stays after the substantive CB correction families. It is not started in parallel. |
| D-CA4-6 | Current Topics corrections (S-6, BB-Q3, H-08) stay with the existing Oral / Current-Topics correction lane. They are not implemented here. |

## 2. Base

`git fetch origin` on 9 Oct 2026 gave origin/main **`b82017d6cd09b3a2dcce213e865cb472392ecd9f`** (POST31-CA3), equal to the CA4 baseline. There were no intervening commits, so no overlap classification was needed.

- Work was done in a fresh worktree `wt-post31-ca4w`, on branch `feat/post31-ca4w-p2-ghg-cii-20261009`, created from origin/main.
- The CA3/CA4, LOHAN and quarantined `b911dd3` checkouts were not used.
- Pristine copies of the three edited files were taken before any edit:

| File | SHA-256 |
|---|---|
| P2 | `1a7a7cdd…` |
| manifest | `17b23503…` |
| inbound baseline | `3503501d…` |

- Baseline gates ran on the same worktree before the first edit.

## 3. Primary-source gate (9 Oct 2026, before any edit)

| Fact | Source | Result |
|---|---|---|
| 2023 IMO GHG Strategy = **resolution MEPC.377(80), adopted 7 July 2023** | IMO resolution text, two IMO-hosted copies: the CA4-held press-briefing PDF (SHA-256 `721c9599…`) and a fresh download from the IMO Index of Resolutions, `MEPCDocuments/MEPC.377(80).pdf` (SHA-256 `45a6d4dd…`). Text was re-extracted independently. | **Confirmed.** "RESOLUTION MEPC.377(80) — Adopted on 7 July 2023". "MEPC.385" does not appear. |
| MEPC.385 is a real, different resolution | Corpus P23 `#topic-p23-4` reference list: MEPC.385(81), 22 March 2024, the DCS Appendix IX amendments | Explanatory only. The page does not call MEPC.385 fictitious. |
| 2027–2030 CII Z factors = **resolution MEPC.400(83), adopted 11 April 2025**, amending G3 (MEPC.338(76)) | MEPC 83/17/Add.1 annex 4: CA4-held copy (SHA-256 `aa2a3ce8…`) and a fresh IMO Index download, `MEPCDocuments/MEPC.400(83).pdf` (SHA-256 `0c1c4d3f…`) | **Confirmed.** Table 1, relative to the 2019 reference line: 2023 5% · 2024 7% · 2025 9% · 2026 11% · **2027 13.625% · 2028 16.250% · 2029 18.875% · 2030 21.500%** |
| Z factors are separate from the Net-Zero Framework | MEPC.400(83) amends the CII G3 guidelines under MARPOL Annex VI reg. 28. The NZF is the draft Chapter 5 (GFI / pricing). | **Distinct.** Z factors are adopted; NZF pricing tiers stay draft and illustrative. |

The primary text agreed with the brief, so there was no stop. LOHAN audit evidence (§5.1 #15, MEPC.385 → 377) agrees, but it is history only and was not used as a source.

## 4. Exact corrections (P2 `#topic-9`, controlled HTML edit)

P2 is a hand-authored legacy Part with no spec, so no spec was created and `build_part.py` was not run. The edits were applied by a script that requires each old string to occur exactly once in the file and inside the `#topic-9` block; otherwise it writes nothing. There were 22 replacements, because W2.9 covers four table cells.

| # | Locus | Change |
|---|---|---|
| W1.1 | timeline 2023 row | `Resolution MEPC.385(80)` → `Resolution MEPC.377(80), adopted 7 July 2023` |
| W1.2 | regulatory references | reg-code `Resolution MEPC.385(80)` → `Resolution MEPC.377(80)` (reg-desc unchanged) |
| W1.3 | quick revision "2023 revision" | `(Resolution MEPC.385(80))` → `(Resolution MEPC.377(80))` |
| W2.1 | verify note, 1st caveat | "and the year-by-year Z-factor percentages" removed; the draft/indicative caveat now covers the NZF tier prices only |
| W2.2 | verify note, 8 Oct sentence | "Treat every number … tier structure and reduction trend" → "Treat every Net-Zero Framework pricing number … tier structure" |
| W2.3 | verify note, appended | dated **Correction, 9 October 2026** sentence (§5) |
| W2.4 | definition | NZF pricing + Fund "(approved in principle, not adopted)"; CII reduction factors 2027–2030 "(adopted, MEPC.400(83))" |
| W2.5 | timeline Apr 2025 row | MEPC-83 approves the NZF in principle **and adopts** the 2027–2030 CII reduction factors (MEPC.400(83), 11 April 2025) |
| W2.6 | section head | "CII Reduction Trajectory (Z-Factors) — Draft Trend, 2027–2030" → "CII Reduction Factors (Z) — Adopted, 2027–2030 (MEPC.400(83))" |
| W2.7 | Z-table header | "Indicative Z-Factor (draft, illustrative)" → "Reduction factor Z, % below the 2019 reference line" |
| W2.8 | 2026 row | "11.0% (confirmed baseline window, current in-force trajectory)" → "11% (MEPC.338(76))" |
| W2.9 | 2027–2030 rows | "~13.1% (draft)" / "~16.2% (draft)" / "~18.8% (draft)" / "~21.5% (draft)" → **13.625% (MEPC.400(83))** / **16.25%** / **18.875%** / **21.5%** |
| W2.10 | paragraph after the table | the "discussed/proposed at MEPC-83 … not immutable law" sentence → adopted factors (G3 as amended by MEPC.400(83)), +2.625 points a year to 21.5% in 2030, separate from the draft NZF GFI targets, pointer to Part 23 · Topic 3. The Required-CII formula sentence is unchanged. |
| W2.11 | Oral Q2 | Q → "What CII reduction factors apply for 2027–2030?"; A → MEPC.400(83) values, 2019 reference line, 5/7/9/11% for 2023–2026, "adopted, not part of the draft NZF; re-verify at each MEPC" |
| W2.12 | 15M written question | "proposed extended CII trajectory (2027–2030)" → "adopted 2027–2030 CII reduction factors (MEPC.400(83))" (rest unchanged) |
| W2.13 | memory box | "2026 = 11.0% confirmed; 2027–2030 figures are draft/indicative only" → "CII Z: 11% (2026) → 13.625 / 16.25 / 18.875 / 21.5% (2027–2030), adopted by MEPC.400(83) — not draft" |
| W2.14 | quick revision | "Confirmed Z-factor / 11.0% for 2026" → "CII Z factors (adopted) / 2026 11%; 2027–2030 13.625 / 16.25 / 18.875 / 21.5% (MEPC.400(83), 11 Apr 2025)" |
| W2.15 | references | two `<li>` added. Both link to the IMO Index of Resolutions PDFs, which already appear in the corpus (`WA2-GHG1.html`) and resolved HTTP 200 on 9 Oct 2026: MEPC.377(80), and MEPC 83/17/Add.1 annex 4, MEPC.400(83). |
| W2.16 | footer version | `Notes-p2 · T9 · v1.2` → `v1.3` |

**Not changed:**

- anchor `#topic-9`, `data-kw`, the title including "(MEPC-83)" (D-CA4-3);
- the STATUS-NZF marker (byte-identical) and all 7 P22 hub pointers;
- the NZF pricing-tier text and caveats ("draft ~$300/t … illustrative", "Exact US-dollar values remain subject to final adoption", "MARPOL Annex VI, Ch.5 (draft)");
- the CE Oral Tip, the Deep Dive and the adjacent-frameworks list;
- every other P2 topic;
- `<head>`, the tail and the gate.

## 5. Historical correction note

The CA2/CA3 convention is followed: old wrong values appear **only** inside one clearly dated sentence that retracts them. That sentence is the "Correction, 9 October 2026:" sentence at the end of the verify note. It records:

- "Resolution MEPC.385(80)" as the earlier wrong citation, and that MEPC.385 is a different instrument, MEPC.385(81);
- the earlier draft values "~13.1 / ~16.2 / ~18.8 / ~21.5 %";
- the adopted MEPC.400(83) values;
- the Part 23 · Topic 3 pointer.

The CA4W string guards mask exactly this sentence out of the "live" teaching text, then require:

- MEPC.385(80) = 0 live (1 in the correction, 0 elsewhere in the file);
- MEPC.377(80) ≥ 3 live (5);
- 13.625 / 16.25 / 18.875 / 21.5 present live;
- "(draft)" = 0 in the Z table;
- "draft/indicative only" = 0;
- the old "~" values and "11.0%" = 0 live.

No separate "pre-adoption draft" table is kept, so the page does not teach superseded numbers.

## 6. P22 hub preservation

CA3 made P22 `miw-notes-mgmt-p22.html#topic-p22-3` the NZF TEACHING_HUB and P2-T9 the pricing / policy-mechanics specialisation. CA4W does not reverse this:

- the STATUS-NZF marker is byte-identical;
- the P22 pointer count is unchanged (7 → 7);
- the counts of "MEPC 85" and "4 December" are unchanged, so no meeting-date maintenance is reintroduced;
- the new pointer goes to the **CII** node (`miw-notes-mgmt-p23.html#topic-p23-3`), not to any NZF status reference.

`validate_status_consumers.py` passes.

## 7. Manifest (`meoclass1/oralnotes/notes_content_index.json`)

The edits are raw text and the JSON is not re-serialised. A JSON tree comparison shows exactly two changed paths:

- `generated_by`: a new newest-first POST31-CA4W entry, with the earlier text kept after "Previous:";
- the P2 `editorial_note`: one appended sentence, "Correction, 9 October 2026 (POST31-CA4W): …". It covers the Strategy resolution correction and the Z-factor correction, and says that the item (3) draft/illustrative caveat now applies to the NZF pricing tiers only, not to the adopted CII Z factors.

`generated` stays `2026-10-09`. It was already the CA4W date, so the value is unchanged. MAN-1 is **not** repaired, and nothing else is reformatted.

## 8. Inbound baseline

`tools/notes/canonical/inbound_baseline.csv` was regenerated with the CA3 method: `validate_canonical.scan_inbound` over all tracked files except `tools/notes/canonical/`, with this record staged so that it is counted, and `source_commit` = the CA4W base `b82017d…`.

| | Before (CA3, b82017d) | After (CA4W candidate) |
|---|---|---|
| referrer files | 34 | 35 |
| rows | 474 | 478 |
| total references | 4,035 | 4,040 |
| broken | 0 | **0** |

Delta: +5 references and +4 rows. `miw-notes-mgmt-p2.html` 7 → 9: the two new links to `#topic-p23-3` (W2.3, W2.10) form one new row. This record adds 3 references in 3 rows (P2-T9, the P22 hub and the P23 CII node), and is the 1 new referrer file. No reference was removed. Every row carries `source_commit` = `b82017d…`, so the git diff shows every row changed, although only these rows changed in content.

`source_nodes.csv`, `display_aliases.csv` and the status cores are **unchanged**. The title, anchor and version alias `T9` are unchanged; only the `v1.x` suffix moved, and the alias data does not record it.

## 9. Exclusions

| Item | Reason |
|---|---|
| P2-T9 retitle (drop "(MEPC-83)") | D-CA4-3: keep |
| P1-T2 / P1-T6 GHG wording and resolution attribution | D-CA4-2 → CA5-GHG |
| oralnotes index PSC card (H-07) | D-CA4-2 → hub/UI package |
| Liability (H-01…H-04), CB-5 technical (B-30, XII/12, OWS 14.7), ECA, MS Act | CA5-LIAB / CA5-TECH / CA6-MSA; not authorised here |
| `known_traps.md` entry for MEPC.377 / MEPC.400 | QB/Oral-governance owned; handed off |
| CE Oral Tip "present MEPC-83 figures as adopted law" | Outside the authorised loci. In context it refers to NZF figures, but since MEPC 83 did adopt the CII factors, a later package may tighten it to "NZF figures". Observation only. |
| Post-MEPC 85 NZF refresh | Time-triggered, after 4 Dec 2026 |
| S-6, BB-Q3, H-08 | Current Topics lane (D-CA4-6) |
| CB-T | After the substantive CB correction families (D-CA4-5) |

## 10. Tests (pristine base b82017d vs candidate)

| Gate | Base | Candidate |
|---|---|---|
| `validate_canonical.py` | PASS | **PASS** (live scan = baseline: 4,040 refs across 35 referrer files) |
| `test_validate_canonical.py` | 23/23 | **23/23** |
| `validate_status_consumers.py` | PASS | **PASS** |
| `test_validate_status_consumers.py` | 18/18; null-validator 1/18 | **18/18**; null-validator **1/18** (anti-vacuity preserved) |
| CA4W string / content guards (42) | 16/42 (anti-vacuity: the guards fail on the unedited page) | **42/42** |
| Legacy `health_check` P2 / P4 / P7 / P8 / P12 | 10 / 11 / 7 / 9 / 6 | **identical messages** (only the P2 byte-size header differs: 67,914 → 69,618) |
| P2 structure | 0 balance errors, 0 unclosed | **0 / 0**. Topic ids unchanged; 37 section heads, of which only W2.6 changed (approved). Tag delta: li +2, a +4, strong +4, em −1, all explained by W2.3/W2.10/W2.15 and W2.2. |
| P2 `<head>` / bytes before `#topic-9` / bytes from `#topic-10` to the end (tail, robots, gate) | — | **byte-identical** |
| Determinism P19–P31 `--gated` | 13/13 identical | **13/13 identical** (untouched by CA4W) |
| `validate_spec` + `health_check --require-gate` P22–P25, P28, P29, P31 | OK / 0 errors | OK / 0 errors |
| `test_notes_root_resolution.py` / `test_spec_parts_discovery.py` | PASS / PASS | PASS / PASS (only a random temp-dir name differs) |
| `check_master_index.py` (balance report) | — | identical |
| Legacy manifest guard | OK | OK |
| `validate_correction_pass2.py` | 133, 0 FAIL | 133, 0 FAIL |
| `regulatory_facts.test.mjs` | 20/20 | **20/20** |
| Oral `test_notes_controls.py` / `test_oral_controls.py` | 106/1, 341/1 | **106/1, 341/1**, same payload |
| `git diff --check` | — | clean |
| Canonical-ID leakage (MERGE-/PCT-/CAND-/CANON-) in the learner-page diff | — | **0** |
| LOHAN paths changed / integration records / D-L4 | — | **0 / 0 / no** |

## 11. Known failures

Oral control CQ-ORAL-1, "no Oral Note text exercises the ME-GI / ME-GA family", fails identically on base and candidate: 106/1 and 341/1, with the same payload. It is not caused by CA4W and is not fixed here.

## 12. LOHAN boundary

CA4W is a Uday-owned correction.

- **Zero** LOHAN files or worktrees were modified.
- No LOHAN patch was cherry-picked.
- No Uday↔LOHAN integration record was created.
- No shared canonical ID was frozen.
- D-L4 was not modified.

The facts rest on IMO primary text alone; LOHAN audit evidence is cited as history only. The learner-page diff introduces no MERGE-, PCT-, CAND- or CANON- identifier.

## 13. Rollback

This is a single local commit.

- **Before landing:** delete the branch `feat/post31-ca4w-p2-ghg-cii-20261009` and the worktree.
- **After landing:** `git revert <sha>` restores P2-T9 v1.2, the manifest and the CA3 inbound baseline, and removes this record. The Vercel rollback target is `dpl_Cx3AHtkpFUZfHkUBqTY4JsjBRhyL` (b82017d).

Nothing else depends on the new text.
