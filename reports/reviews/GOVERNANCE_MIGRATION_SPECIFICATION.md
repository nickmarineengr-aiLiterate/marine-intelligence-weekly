# Governance Migration Specification

**Package:** PKG-2.0 — Governance Migration Preparation
**Purpose:** Define the implementation guide for a future migration package. This document moves nothing itself.
**Status:** Specification only. No files moved, modified, or committed.
**Date:** 2026-07-31
**Built on:** `GOVERNANCE_ARCHITECTURE_DECISION.md` (PKG-1.9)

---

## 0. How This Specification Uses the Prior Decision

`GOVERNANCE_ARCHITECTURE_DECISION.md` left five items as open Founder decisions rather than settled facts. This specification treats "the Governance Architecture Decision has been accepted" as adopting that document's own **recommended** answer to each — not as a separately-confirmed line-item sign-off. Each place a recommendation is being relied on as a working assumption is marked **[ASSUMED]** below. If any assumption is wrong, only that assumption's downstream steps need to change — the rest of this specification stands.

| # | Open question (from PKG-1.9) | Assumption this spec uses |
|---|---|---|
| 1 | Does `IMPLEMENTATION_CONTRACT.md` move to `docs/`? | **Yes** — reclassified as permanent governance |
| 2 | Keep or rename `reports/governance/`? | **Rename** to `reports/bootstrap-archive/` — the recommended option, since "governance/" stops being an accurate name once the one actively-governing document leaves it |
| 3 | Resolve the Amendment document's approval status now? | **No** — stays deferred, moves with the rest of the archive, status unchanged |
| 4 | Commit the three (now four, including PKG-1.9's own output) loose review artifacts? | **Yes**, as part of this migration — their standalone continuity risk was flagged as urgent in PKG-1.9 §6 |
| 5 | Migration trigger — wait for `docs/` to exist naturally, or create it now? | **Wait** — migration does not begin until `docs/ENGINEERING_PRINCIPLES.md` exists |

---

## 1. Final Repository Layout

```
marine-intelligence-weekly/
├── docs/
│   ├── ENGINEERING_PRINCIPLES.md          ← PKG-1.5R output (precondition for this migration)
│   ├── IMPLEMENTATION_CONTRACT.md         ← migrates here from reports/governance/
│   └── adr/                               ← future, not created by this migration
│
├── reports/
│   ├── audit/
│   │   └── 2026-07-30_repo_audit.md       ← unchanged
│   ├── packages/
│   │   └── PKG-1_COMPLETION_SUMMARY.md    ← unchanged
│   ├── reviews/                           ← NEW folder, created by this migration
│   │   ├── ONBOARDING_VERIFICATION_REPORT.md
│   │   ├── BOOTSTRAP_CONSOLIDATION_PLAN.md
│   │   ├── ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md
│   │   ├── GOVERNANCE_ARCHITECTURE_DECISION.md
│   │   └── GOVERNANCE_MIGRATION_SPECIFICATION.md   ← this document, once committed
│   └── bootstrap-archive/                 ← renamed from reports/governance/
│       ├── MIW_Bootstrap_Blueprint.md
│       ├── MIW_Bootstrap_Governance_Review.md
│       ├── MIW_Architecture_Freeze_Review.md
│       └── Bootstrap_Architecture_Amendment_LocalFirst.md
│
├── AI_SESSION_HANDOVER.md                 ← stays at root (see §1a)
├── .gitignore, README.md, CNAME, package.json, robots.txt   ← unaffected
└── [all existing content unchanged: meoclass1/, SQ/, GHGDecarb/, archive/,
     articles/, assets/, RulesApp/, youtube/, api/, index*.html, .github/]
```

### 1a. Special case: `AI_SESSION_HANDOVER.md`

Not part of this migration's file-move set. It self-describes as bridging content, "superseded by `docs/CLAUDE.md` once that package is reached" — meaning its natural end-of-life is retirement into the archive when PKG-12 lands, not relocation now. It remains at root, actively maintained, until that trigger. Flagged here as a recommendation for a future package, not a decision this specification is making.

---

## 2. Permanent Governance Location

**`docs/`** — and only `docs/`. Per the frozen architecture (`MIW_Architecture_Freeze_Review.md`, approved), this is the single governance home. After this migration, it holds `ENGINEERING_PRINCIPLES.md` and `IMPLEMENTATION_CONTRACT.md`; `docs/adr/0001–0005` join later, under separate packages, not created by this migration.

**Rule going forward:** a document belongs in `docs/` if and only if it is currently binding on every package's execution and is actively maintained (amended in place when it changes, not superseded by a dated snapshot). `IMPLEMENTATION_CONTRACT.md` qualifies under **[ASSUMED]** decision 1 above.

---

## 3. Historical Report Location

**`reports/`**, three subfolders, each with a distinct rule:

- **`reports/audit/`** — point-in-time repository audits. Never edited after the fact.
- **`reports/packages/`** — per-package completion reports (the pattern PKG-1 set). **Gap noted, not fixed by this migration:** PKG-1.6, PKG-1.7, and PKG-1.5R never produced a file here — their reports were delivered in chat only. Backfilling those is a separate, optional future item, explicitly out of scope for this migration (see §6, Package Boundaries).
- **`reports/reviews/`** (new) — review/analysis output that isn't tied to one specific package number: onboarding reviews, consolidation plans, evidence analyses, architecture decisions, migration specifications. This is where the four currently-uncommitted documents land, plus this document once it is committed.

Everything under `reports/` is written once and read for its findings — never maintained to "stay current." This is the dividing line against `docs/`.

---

## 4. Bootstrap Archive Location

**`reports/bootstrap-archive/`** (renamed from `reports/governance/` — **[ASSUMED]** decision 2).

Holds exactly the four documents whose value is provenance, not ongoing compliance: `MIW_Bootstrap_Blueprint.md`, `MIW_Bootstrap_Governance_Review.md`, `MIW_Architecture_Freeze_Review.md`, `Bootstrap_Architecture_Amendment_LocalFirst.md`. Kept permanently — never deleted, matching the repository's own stated practice for superseded ADRs (`MIW_Bootstrap_Governance_Review.md` §2: "Never delete an ADR, even if superseded — supersession is itself a valuable record"). This is the same discipline applied one level up, to the pre-ADR governance record itself.

**Rule going forward:** a document belongs here if it recorded a decision-in-progress or the reasoning behind a now-settled decision, and nothing currently checks compliance against it directly (compliance is checked against whatever `docs/` document eventually captured its conclusion — an ADR, `ENGINEERING_PRINCIPLES.md`, or the frozen architecture itself).

The Amendment document's approval status is **not** resolved by moving it here — **[ASSUMED]** decision 3. It moves with its siblings, unchanged, still reading "Proposed... pending Founder approval."

---

## 5. Migration Order

**Precondition (blocks Step 1):** `docs/ENGINEERING_PRINCIPLES.md` exists — i.e., PKG-1.5R has completed and its output is committed. This migration does not create `docs/` for its own sake — **[ASSUMED]** decision 5.

1. **Snapshot.** Record the pre-migration commit hash and a file-by-file checksum of everything about to move (§7 list). This is the rollback baseline (§9).
2. **Move `IMPLEMENTATION_CONTRACT.md`.** `git mv reports/governance/IMPLEMENTATION_CONTRACT.md docs/IMPLEMENTATION_CONTRACT.md`. Diff before/after — must be byte-identical.
3. **Rename the archive folder.** `git mv reports/governance reports/bootstrap-archive` (single directory rename; git preserves individual file history for all four remaining files).
4. **Create `reports/reviews/` and add the four loose documents.** These are currently untracked (not a `git mv`, a fresh `git add` at the new path) — `ONBOARDING_VERIFICATION_REPORT.md`, `BOOTSTRAP_CONSOLIDATION_PLAN.md`, `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md`, `GOVERNANCE_ARCHITECTURE_DECISION.md`.
5. **Cross-reference scan.** Grep every already-committed file for the literal old paths (`reports/governance/`) to catch any internal link that would now be broken. (At the time of writing, no committed file links to these paths — this step exists to catch drift between now and when the migration actually runs.)
6. **Validate** per §8.
7. **Commit** — recommend splitting into logically complete units per `IMPLEMENTATION_CONTRACT.md` §4 ("prefer many small, reviewable changes"): one commit for the Contract's move to `docs/`, one for the archive rename, one for populating `reports/reviews/`. A single combined commit is defensible too (it's a pure reorganization, zero content change) — either satisfies the policy; three is the more granular, more easily-reverted option.
8. **Push**, then **verify** (Contract §2 Verification stage — `git log`/`git diff` confirms pushed state matches validated state).
9. **Report** — per the standing package pattern used throughout this bootstrap.

---

## 6. Package Boundaries

**In scope for the future migration package:**
- The exact `git mv` / `git add` operations listed in §5, steps 2–4.
- Updating any internal cross-reference broken by the move (§5 step 5) — required by `IMPLEMENTATION_CONTRACT.md` §5 ("every cross-reference... must resolve to something that actually exists at commit time. A broken link is a validation failure").
- Creating the two new folders (`reports/reviews/`, and `reports/bootstrap-archive/` via rename) as a direct consequence of the moves — not a separate structural decision.

**Explicitly out of scope:**
- Drafting any new content (ADRs, further principles work).
- Resolving the Amendment document's approval status (§4 — separate decision, separate package).
- Backfilling the missing PKG-1.6 / PKG-1.7 / PKG-1.5R / PKG-1.9 report files under `reports/packages/` (§3 gap) — a distinct, optional future item.
- Any change to file *content* beyond what's mechanically required to fix a cross-reference path — no rewording, no status-line changes beyond what was already done in PKG-1.5.
- Deciding `docs/adr/`'s contents — that's PKG-1.5R's ADR follow-on work, unrelated to this reorganization.

---

## 7. Files That Will Eventually Move

| # | File | From | To |
|---|---|---|---|
| 1 | `IMPLEMENTATION_CONTRACT.md` | `reports/governance/` | `docs/` |
| 2 | `MIW_Bootstrap_Blueprint.md` | `reports/governance/` | `reports/bootstrap-archive/` |
| 3 | `MIW_Bootstrap_Governance_Review.md` | `reports/governance/` | `reports/bootstrap-archive/` |
| 4 | `MIW_Architecture_Freeze_Review.md` | `reports/governance/` | `reports/bootstrap-archive/` |
| 5 | `Bootstrap_Architecture_Amendment_LocalFirst.md` | `reports/governance/` | `reports/bootstrap-archive/` |
| 6 | `ONBOARDING_VERIFICATION_REPORT.md` | repo root (uncommitted) | `reports/reviews/` |
| 7 | `BOOTSTRAP_CONSOLIDATION_PLAN.md` | repo root (uncommitted) | `reports/reviews/` |
| 8 | `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` | repo root (uncommitted) | `reports/reviews/` |
| 9 | `GOVERNANCE_ARCHITECTURE_DECISION.md` | repo root (uncommitted) | `reports/reviews/` |
| 10 | `GOVERNANCE_MIGRATION_SPECIFICATION.md` (this document) | repo root (uncommitted) | `reports/reviews/` |

**10 files total.** Items 6–10 are "moves" only in the sense that they are committed for the first time directly at their final path — they have no prior committed location to move from.

## 7a. Files That Will Remain Where They Are

- `AI_SESSION_HANDOVER.md` — root (see §1a: future retirement at PKG-12, not a migration move)
- `reports/audit/2026-07-30_repo_audit.md` — unchanged
- `reports/packages/PKG-1_COMPLETION_SUMMARY.md` — unchanged
- `.gitignore`, `README.md`, `CNAME`, `package.json`, `robots.txt` — unaffected, unrelated to governance
- Every content file and directory: `meoclass1/`, `SQ/`, `GHGDecarb/`, `archive/`, `articles/`, `assets/`, `RulesApp/`, `youtube/`, `api/`, `index*.html`, `.github/workflows/` — entirely out of scope
- `Claude skill/` (local only, never committed) — untouched; its remaining two files (a skill draft and a superseded local audit copy) stay excluded from any commit, as decided in PKG-1.7

---

## 8. Validation Strategy

Before any commit in the future migration package:

1. **Pre-move baseline.** `git ls-files` snapshot plus a checksum (or line/byte count, matching the method already used in PKG-1.6/1.7) for every file in §7.
2. **`git mv` only, never manual copy+delete**, for files already tracked (items 1–5) — preserves rename history and guarantees byte-identical content by construction.
3. **Post-move content diff.** For every moved file, confirm `git diff --stat` shows a pure rename with zero insertions/deletions (or, for items 6–10, confirm the newly-committed content is byte-identical to the working-tree source that existed before this migration).
4. **Cross-reference scan.** Grep the full repository for every old path string before considering the migration complete — per `IMPLEMENTATION_CONTRACT.md` §5's validation policy, a broken cross-reference is a validation failure, not a follow-up item.
5. **Layout check.** Confirm the resulting `git ls-files` output matches §1 (Final Repository Layout) exactly — no missing file, no stray extra file.
6. **`git status` clean** before each commit — no uncommitted or untracked cruft left behind, matching `IMPLEMENTATION_CONTRACT.md` §3 Definition of Done.
7. **Post-push verification.** `git log`/`git diff` (or cache-busted fetch) confirms the pushed remote state matches what was validated locally — Contract §2 Verification stage.

---

## 9. Rollback Strategy

- **Force-push and history rewriting are prohibited without exception** (`IMPLEMENTATION_CONTRACT.md` §4) — this applies to rollback exactly as it applies to any other commit. A migration mistake is fixed going forward, never by rewriting what's already pushed.
- **If caught before push** (still local, uncommitted or committed-but-unpushed): safe to `git reset` locally and redo — this doesn't touch shared/pushed history, so the force-push prohibition doesn't apply.
- **If caught after push:** fix with `git revert` (a new commit undoing the change), never `git reset --hard` + force-push. Because `git mv` preserves rename history, `git log --follow` keeps every file traceable through the revert.
- **Smallest reasonable commit granularity** (§5, step 7 recommends up to three separate commits) directly serves rollback: a wrong destination path for `IMPLEMENTATION_CONTRACT.md` can be reverted without touching the archive rename or the reviews-folder population, if those two were correct.
- **Baseline recorded in Step 1** (§5) — the pre-migration commit hash — means "what did the repository look like immediately before this" never requires archaeology; it's one `git show <hash>` away.

---

## 10. Closing Note

This specification moves nothing. It is a plan for a future package, built on the accepted `GOVERNANCE_ARCHITECTURE_DECISION.md`, with every place that document left a decision open now marked as an explicit, individually-correctable assumption (§0) rather than silently resolved. No repository file was moved, renamed, modified, or committed in producing this document. Submitted for Founder review.
