# MSA 2025 QB RE-BASING — PACKAGE REPORT

Date: 2026-08-03. First corpus-backed correction package after true-source acceptance (ACCEPTED_WITH_DISCLOSED_GAPS).

## Starting repository state
`F:\Marine-Intelligence-Weekly`, branch main @ f75c20f (= origin/main after fetch). Pre-existing local state preserved untouched: unstaged deletions of `meoclass1/known_traps.md` + `meoclass1/qb_content_index.json` (Founder intent unconfirmed — HOLD-04) and 4 untracked Founder files.

## Corpus evidence and legal verification
- MS Act 2025 (Act 24 of 2025): corpus-held text (PRS Gazette reproduction, hash-registered; RQ-32), **in force 2026-03-15** (S.O. 1244(E), verified online 2026-08-03).
- **s.324 verified from the Act text**: 1958 repealed except Part XIV; **s.411A excluded from the saving (repealed), substance re-enacted as s.323**; subordinate rules continue (s.324(2)(a)); documents construed (s.324(2)(c)).
- Bounded extraction (118 pp) verified: s.63 employment agreements, s.112 official logbook, s.127 unseaworthy, Part XI ss.231–232 casualty, wreck/wages ranges.
- **New legal-landscape finding**: Coastal Shipping Act, 2025 (Act 20 of 2025) replaces 1958 Part XIV coasting-trade licensing (QB10 already reflected this; the true-source corpus record was stale and has been corrected — corpus RQ-43 opened for the CSA text + commencement).

## Key discovery
The Founder had already executed a substantial re-basing pass on **15 Jul 2026** (v1.1/v1.2 card footers across QB1_A, QB1_I, QB4_C/D, QB5_A/B/G, QB9_A/D/E/F/G, oralnotes p14–p16, simon-notes-p3, QB10). This package therefore audited that pass and corrected **residual defects only** — 24 corrections in 14 files (ledger RB-001…RB-012), the most significant being the **inverted s.411A claim in QB9_F** (said "excepted from repeal and continues"; the Act says repealed, substance re-enacted as s.323).

## Validation
- Post-edit adversarial sweep: zero remaining 1958-as-current claims (all 243 remaining "1958" hits are historical/transition framing, sampled).
- `qb_health_check.py`: all edited files clean; remaining flags are pre-existing documented REVIEW-class items.
- Part XIV references NOT removed; no 2025 section invented (unverified sections cited Act/Part-level with explicit "pending verification").

## Artefacts
- Ledger: `production-system/verification/merchant-shipping-act-2025-rebasing-ledger.json`
- Crosswalk: `production-system/verification/merchant-shipping-act-2025-crosswalk.md`
- Pipeline export: `production-system/verification/merchant-shipping-act-2025-pipeline-export.json`

## Backlog (non-July, follow-up)
Historic 1958 structural references retained as labelled legacy (simon-notes-p6 key-section list); exact-section verification pass for HOLD-01 topics; SQ/ mirror files (staging duplicates of oralnotes/QB1_A — same corrections apply if SQ is published surface — **not edited this package**, flagged for Founder).

## Rollback
All changes are ordinary commits on main; revert by `git revert <commit>`. No history rewritten, no Founder files touched.

## Candidate-facing summary (draft for Founder approval)
"QB statutory citations have been re-verified against the Merchant Shipping Act, 2025 (in force 15 March 2026). Where the exact 2025 section number is still being confirmed, answers cite the Act and Part with a 'pending verification' note rather than a guessed section. Cabotage questions: 1958 Part XIV was saved at repeal and its licensing role has passed to the Coastal Shipping Act, 2025."
