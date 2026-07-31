# Bootstrap Consolidation Plan

**Prepared by:** AI session (Claude Code), consolidating findings from `ONBOARDING_VERIFICATION_REPORT.md`
**Date:** 2026-07-31
**Status:** Planning only. No repository files modified. No commits made. Awaiting Founder approval.
**Inputs reviewed:** `ONBOARDING_VERIFICATION_REPORT.md`, `AI_SESSION_HANDOVER.md`, `reports/audit/2026-07-30_repo_audit.md`, `reports/packages/PKG-1_COMPLETION_SUMMARY.md`, live `git status`/`git log`, live repository directory structure (re-verified this session — no drift from the onboarding review).

---

## Executive Summary

19 distinct issues were identified across the onboarding review and its source documents. None are content-corrupting or actively harmful today, but one — the four governance documents living only as untracked local files — is a genuine continuity risk that should be closed before any further implementation work, regardless of package sequence. Two items (the PKG-1.5 path conflict and principle sign-off) are pure Founder decisions blocking an otherwise-ready package. The remainder is contained, known technical debt that the audit already scoped correctly; this plan's main contribution is sequencing it and deciding what becomes a package versus what gets folded into existing package scope versus what gets explicitly deferred.

Recommended posture: **do not treat this as "ready to fan out into parallel implementation."** Close the two Critical repository-safety items first (both cheap, both non-controversial), get the two blocking Founder decisions, commit PKG-1.5, then resume the numbered sequence with several existing packages (PKG-2, PKG-3) absorbing documentation debt the audit already assigned to them.

---

## Repository Health

**Overall:** Contained and stable. No new issues emerged between the audit (2026-07-30) and this review (2026-07-31) — every re-checked finding (`.gitignore` naming, duplicate manifests, `SQ/` duplicate pairs, missing `verify-session.js`, undocumented `api/` scripts) held exactly as reported. The working tree is clean apart from two untracked items: `Claude skill/` (pre-existing, the governance-document risk discussed below) and `ONBOARDING_VERIFICATION_REPORT.md` (this session's own deliverable).

**Lifecycle discipline:** Good. PKG-1 closed all eight lifecycle stages (Planning → Report) with no shortcuts and explicit Limitations logged rather than silently skipped (`reports/packages/PKG-1_COMPLETION_SUMMARY.md:69-79`). This is the strongest evidence that the bootstrap process itself works, not just that the repository is in acceptable shape.

**Primary risk:** Single point of failure on governance. The Bootstrap Blueprint, Governance Review, Architecture Freeze Review, and Implementation Contract — the documents that define the entire package sequence and decision framework this plan itself relies on — exist in exactly one place: an untracked directory on one local machine. This is the one item in this plan that is not "technical debt" in the ordinary sense; it's an availability risk to the bootstrap's own foundation.

---

## Validated Strengths

- **PKG-1 is a clean, trustworthy baseline.** Full lifecycle closure, evidence-based findings, explicit limitations — nothing overstated or silently assumed.
- **Automation footprint matches expectations exactly.** One GitHub Actions workflow, no hidden automation (audit, confirmed live this session — `.github/workflows/` unchanged).
- **No duplication between repository content and skill-file guidance.** The audit found that PKG-3's planned Content Standards Docs would fill a genuine gap, not restate something already documented elsewhere — a real strength, since it means the documentation backlog is not busywork.
- **Local-First Repository Workflow is proven end-to-end.** PKG-1's commit/push/verify cycle worked without the GitHub connector, and this is now the standing mechanism (`PKG-1_COMPLETION_SUMMARY.md:91-93`).
- **Independent re-verification this session found zero drift** from the audit's findings — the audit's Technical Debt table is still accurate 24 hours later, which is a good sign for its reliability as a planning input.
- **Architecture and governance are conceptually coherent**, even though not yet committed: 14 principles, 5 planned ADRs, a flat top-level structure that (once the `RulesApp/` co-location is documented) has no open structural disputes (`reports/audit/2026-07-30_repo_audit.md:58-59`).

---

## Issues Found

Each issue is tagged with its origin: **[Audit]** = `reports/audit/2026-07-30_repo_audit.md`, **[Handover]** = `AI_SESSION_HANDOVER.md`, **[Onboarding]** = new findings from `ONBOARDING_VERIFICATION_REPORT.md`.

| # | Issue | Origin | Severity |
|---|---|---|---|
| 1 | Governance docs (Blueprint, Governance Review, Architecture Freeze Review, Implementation Contract) exist only as untracked local files — absent from any fresh clone | Onboarding | **Critical** |
| 2 | `.gitignore` committed as `gitignore` (no leading dot) — non-functional since repository creation | Audit | **Critical** |
| 3 | Duplicate Notes manifests (`notes-content-index.json` vs `notes_content_index.json`), diverged, undetermined authority | Audit | **Critical** |
| 4 | PKG-1.5 blocked — target path conflict (`docs/` vs `repository/`) | Handover | **High** |
| 5 | PKG-1.5 blocked — final sign-off on 14 principles, incl. 2 flagged near-overlaps | Handover | **High** |
| 6 | `RulesApp/` co-location not reflected in frozen architecture discussion; naming collision with a separate standalone `RulesApp` repo caused a real onboarding delay | Audit / Onboarding | **High** |
| 7 | `Claude skill/` directory name/location doesn't match frozen `skills/` architecture — an undocumented second source of truth | Onboarding | **High** |
| 8 | Root/`archive/` duplicated legacy issues 17–22 (~9MB), incomplete migration for 23–30 | Audit | Medium |
| 9 | Root-level clutter — 14 unarchived `indexNN.html` files | Audit | Medium |
| 10 | `SQ/` prefixed/unprefixed duplicate file pairs (3 pairs), not content-diffed | Audit | Medium |
| 11 | Handover §8 self-reference drift — describes its own commit as pending; already committed as `b3fc477` | Onboarding | Medium |
| 12 | No structured Founder-Questions ledger — six open questions live only in handover prose | Onboarding | Medium |
| 13 | Undocumented API scripts (`check-db.js`, `migrate-users.js`) | Audit | Low |
| 14 | `api/verify-session.js` referenced in prior project memory, not found in repository | Audit | Low |
| 15 | `package.json` `build`/`test` scripts are placeholder echo statements | Audit | Low |
| 16 | No substantive root `README.md` (two lines, no architecture/workflow/contributor info) | Audit | Low |
| 17 | No `docs/CLAUDE.md` entry point yet | Handover | Low (expected — scheduled for PKG-12) |
| 18 | Six audit Founder Questions bundled as a tracking gap (superset of items 3, 6, 13, 14 plus gitignore history and archive intent) | Audit | Low (tracking, not the underlying issues themselves) |
| 19 | `RulesApp/README.md` and its relationship to the separate `RulesApp` GitHub repository not fully reviewed | Onboarding | Low |

---

## Priority Matrix

| Severity | Issues | Blocking? | Effort to resolve |
|---|---|---|---|
| **Critical** | #1, #2, #3 | #1 and #2 block nothing directly but carry continuity/security-adjacent risk; #3 blocks PKG-8 specifically | Low (all three are small, mechanical fixes or a single commit) |
| **High** | #4, #5, #6, #7 | #4 and #5 directly block PKG-1.5's Commit stage; #6 and #7 block accurate PKG-2 documentation | Low–Medium (Founder decisions are cheap; documentation work is contained) |
| **Medium** | #8, #9, #10, #11, #12 | None block the numbered package sequence | Medium (content diffing, migration work takes real time; #11/#12 are near-trivial) |
| **Low** | #13, #14, #15, #16, #17, #18, #19 | None block anything | Low, but requires Founder input on several (purpose confirmation) before documenting |

---

## Recommended Packages

**New packages (not currently in the PKG-0…PKG-13 sequence):**

- **PKG-1.6 — Repository Hygiene: `.gitignore` Fix.** Resolves #2. Matches the audit's own recommendation (`reports/audit/2026-07-30_repo_audit.md:90`) to handle this as a small, early, dedicated commit before PKG-2's file volume grows further. Trivial scope: rename `gitignore` → `.gitignore`, verify patterns still apply.
- **PKG-1.7 — Governance Foundation Commit.** Resolves #1. Commits the four governance documents (Blueprint, Governance Review, Architecture Freeze Review, Implementation Contract) from `Claude skill/` into the repository — target location depends on the Founder's #4 decision (likely `docs/governance/` or similar, to be confirmed). This is the single highest-priority package in this plan: it protects the bootstrap's own foundation from being local-machine-dependent.
- **PKG-1.8 — Notes Manifest Resolution.** Resolves #3. Determines which of `notes-content-index.json` / `notes_content_index.json` is authoritative, documents the decision, and either deprecates or repurposes the other. Must land before PKG-8 (manifest_update.py) per the audit's own dependency note (`reports/audit/2026-07-30_repo_audit.md:91`).
- **New package under `miw-archive` skill scope (unnumbered, outside the 13-package sequence).** Resolves #8, #9. Already recommended by the audit as separately scheduled work (`reports/audit/2026-07-30_repo_audit.md:92`); this plan concurs it should stay outside the main sequence rather than gate it.
- **Founder-Questions Ledger (lightweight artifact, not a numbered package).** Resolves #12, folds in #18. A simple table under `reports/` tracking the six open audit questions plus any new ones raised by this plan, so they stop living only in handover prose (which has already drifted once — see #11).

**Existing packages that should absorb additional scope:**

- **PKG-2 (Core Docs: PROJECT.md + ARCHITECTURE.md)** — already scheduled by the audit to absorb #6 (`RulesApp/` co-location), #13 (`check-db.js`/`migrate-users.js` purpose), #14 (`verify-session.js` discrepancy). This plan adds: document the `RulesApp/`-vs-`RulesApp`-repository naming disambiguation explicitly (part of #6/#19), since it caused a real, measurable onboarding delay.
- **PKG-3 (Content Standards Docs)** — already scheduled to absorb #10 (`SQ/` duplicate pairs), pending Founder clarification.
- **PKG-1.5 (Engineering Principles)** — not a new package, but cannot proceed to Commit until #4 and #5 are resolved by the Founder.

**Not recommended as packages:**

- #7 (`Claude skill/` relocation) is a direct side-effect of PKG-1.7 landing, not separate work — once the governance docs are committed, the leftover local directory can simply be cleaned up or renamed without needing its own package.
- #11 (handover drift) and #16 (thin root README) are single-paragraph edits, not packages — fold into whichever session next touches the handover / root README respectively.
- #15 (`package.json` placeholders) should wait for real build/test tooling (likely arriving with PKG-6/7, Python Utilities) rather than being fixed prematurely with no functional target yet.
- #17 (`docs/CLAUDE.md` absence) is expected and already scheduled — PKG-12. No action needed now.

---

## Recommended Package Order

1. **PKG-1.6 — `.gitignore` fix.** Zero dependencies, zero controversy, protects every commit made from this point forward. Do this first, immediately.
2. **PKG-1.7 — Governance Foundation Commit.** Highest-priority continuity fix. Should not wait on the Founder's final path decision for PKG-1.5 (#4) — even committing the four documents to a provisional location (e.g., `reports/governance/` as drafts) is strictly better than leaving them local-only, and can be moved later if #4 lands on a different path.
3. **Founder resolves #4 and #5** (PKG-1.5 path + principle sign-off) — pure decision, no implementation dependency, can happen in parallel with steps 1–2.
4. **Commit PKG-1.5** once #4/#5 are resolved.
5. **PKG-1.8 — Notes Manifest Resolution.** Should land before PKG-8 is scheduled; doing it here, early, removes a known blocker well ahead of when it would otherwise bite.
6. **Stand up the Founder-Questions Ledger.** Cheap, and best done before PKG-2/PKG-3 start absorbing documentation questions, so answers have one place to land.
7. **PKG-2 (Core Docs)**, with the expanded scope above (#6, #13, #14, #19).
8. **PKG-3 (Content Standards Docs)**, with the expanded scope above (#10).
9. **Resume the numbered sequence (PKG-4 onward)** per the existing Bootstrap Blueprint.
10. **Deferred track (parallel, non-blocking):** the `miw-archive`-scope package for #8/#9, scheduled whenever Founder bandwidth allows — does not gate any of the above.

---

## Founder Decisions Required

1. **PKG-1.5 target path** — `docs/ENGINEERING_PRINCIPLES.md` vs. `repository/ENGINEERING_PRINCIPLES.md`. (#4)
2. **Final sign-off on the 14 Engineering Principles**, including a ruling on the two flagged near-overlap pairs (Explicit Relationships vs. Traceability; Deterministic Tooling vs. Reproducibility). (#5)
3. **Target commit location for the four governance documents** (PKG-1.7) — a definitive `docs/` path, or an interim `reports/governance/` staging location if the final architecture isn't ready to commit to yet.
4. **Authoritative Notes manifest** — `notes-content-index.json` (hyphen) or `notes_content_index.json` (underscore) — and disposition of the other (deprecate vs. repurpose). (#3)
5. **Root/`archive/` migration intent** — confirm `archive/` as the long-term home, and decide timing for completing the migration of issues 23–30 and removing root-level duplicates for 17–22. (#8, #9)
6. **`SQ/` duplicate-pair purpose** — confirm whether the three prefixed/unprefixed pairs are intentional (e.g., a segmented-audience variant) or migration leftovers, to guide PKG-3. (#10)
7. **`check-db.js` / `migrate-users.js` purpose** and **`api/verify-session.js` status** (never existed / renamed / not yet implemented) — needed before PKG-2 documents the auth/data flow accurately. (#13, #14)
8. **Approval to stand up a Founder-Questions Ledger** as a lightweight tracking artifact — process choice, not content-blocking. (#12)

---

## Transition Recommendation

**Do not move directly into broad implementation.** The two Critical, low-effort fixes (#1 via PKG-1.7, #2 via PKG-1.6) should close first — they are cheap enough that sequencing them ahead of any Founder decision costs nothing, and #1 in particular protects work the Founder has already approved from being lost. In parallel, the Founder should resolve the two items blocking PKG-1.5 (#4, #5), since that package is otherwise done and sitting idle.

Once PKG-1.5 is committed, the manifest resolution (PKG-1.8) should land before touching PKG-8 territory, and the ledger should exist before PKG-2/PKG-3 start generating more open questions than the current handover-prose approach can track cleanly (as evidenced by #11's drift).

The archive-cleanup and SQ-dedup tracks are real but not urgent — they can run on a slower, Founder-convenience timeline without gating the numbered package sequence, consistent with how the audit itself scoped them.

**No files were modified and no commits were made in producing this plan.** Submitted for Founder review and approval before any of the above is implemented.
