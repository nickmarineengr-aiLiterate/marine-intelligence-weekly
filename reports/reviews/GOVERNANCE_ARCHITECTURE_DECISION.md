# Governance Architecture Decision

**Package:** PKG-1.9 — Governance Architecture Consolidation
**Purpose:** Determine, before any new permanent governance document is created, a single authoritative information architecture for governance content — what's permanent, what's historical, what's a report, and where each should live.
**Status:** Architectural decision package. No files moved, renamed, modified, or committed.
**Date:** 2026-07-31

---

## 1. Current State

**Committed, inside `reports/governance/` (created in PKG-1.7):**

| File | Approval status | What it actually is |
|---|---|---|
| `MIW_Bootstrap_Blueprint.md` | Not approved (self-describes: "Draft for Founder Architecture Review") | Origin roadmap draft, superseded in particulars by the two reviews below |
| `MIW_Bootstrap_Governance_Review.md` | **Approved** (2026-07-31) | Decision record: governance/ADR scoping, package reordering, the 10-item principles seed |
| `MIW_Architecture_Freeze_Review.md` | **Approved** (2026-07-31) | Decision record: rejects the `engineering/` wrapper, freezes the flat structure |
| `Bootstrap_Architecture_Amendment_LocalFirst.md` | Not approved (self-describes: "Proposed amendment, pending Founder approval") | Standing rule proposal (git/push mechanism) — still unresolved; its required edit to `IMPLEMENTATION_CONTRACT.md` §4/§7 was never applied |
| `IMPLEMENTATION_CONTRACT.md` | **Approved** (2026-07-31) | Actively-governing execution rulebook — invoked by every package this session, including this one |

**Committed, elsewhere:**

| File | What it is |
|---|---|
| `AI_SESSION_HANDOVER.md` (root) | Self-describes: "Bridges active bootstrap work between AI sessions. **Not permanent governance.** Superseded by `docs/CLAUDE.md` once that package is reached." |
| `reports/audit/2026-07-30_repo_audit.md` | Point-in-time audit report |
| `reports/packages/PKG-1_COMPLETION_SUMMARY.md` | Point-in-time package completion report |

**Not committed (untracked, sitting at repository root):**

| File | What it is |
|---|---|
| `ONBOARDING_VERIFICATION_REPORT.md` | Point-in-time review report (this session) |
| `BOOTSTRAP_CONSOLIDATION_PLAN.md` | Point-in-time planning report (this session) |
| `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` | Point-in-time evidence report (this session, PKG-1.5R) |
| `Claude skill/` (local only, not in git at all) | Leftover local directory — 5 of its 6 files were copied into `reports/governance/` in PKG-1.7; the 6th (`miw-correction-workflow_SKILL.md`, a skill draft) and a superseded local audit draft remain, deliberately excluded from any commit so far |

**Not yet created:** `docs/` does not exist anywhere in the repository. `docs/ENGINEERING_PRINCIPLES.md` (path decided by the Founder) has no content yet — PKG-1.5R is still in the evidence-gathering stage, drafting has not started.

**The core problem this package addresses:** governance-adjacent content is currently split across four locations (`reports/governance/`, repository root committed, repository root uncommitted, and a local-only directory) with no explicit rule distinguishing which category each file belongs to. `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` §7 already flagged the sharpest instance of this: the frozen architecture calls for governance to have "a single home" in `docs/`, but the three currently-approved governance documents live in `reports/governance/`, a location chosen provisionally in PKG-1.7 specifically because `docs/` didn't exist yet.

---

## 2. Desired End State

A repository where the category of a document is recoverable from its location alone, without having to open the file and read its Status line:

- **`docs/`** — standing, currently-in-force rules and reference material. If it's in `docs/`, it binds every future package until formally amended. Nothing point-in-time, nothing superseded-but-kept-for-record.
- **A historical/decision-record archive** — the reasoning and drafts that produced what's now in `docs/`. Kept permanently (not disposable), but explicitly not authoritative going forward — read for provenance, not compliance.
- **`reports/`** — point-in-time output: audits, package completion reports, review/analysis artifacts like the three uncommitted documents above. Generated once, not maintained afterward, per the Blueprint's own original design intent (§1: "`reports/` is generated output, not documentation... disposable/regenerable").

This mirrors the distinction the repository already tried to draw between `known_traps.md` (current-state reference) and `corrections/` (historical ledger) — same pattern, applied one level up to governance itself.

---

## 3. Repository Information Architecture

### 3a. What should be considered permanent governance

Content that actively binds every future package's execution, referenced by name from the Quality Gates (`IMPLEMENTATION_CONTRACT.md` §9) or equivalent:

- `ENGINEERING_PRINCIPLES.md` (once drafted) — Founder-decided path: `docs/ENGINEERING_PRINCIPLES.md`. Not in question.
- `docs/adr/0001` through `0005` (once drafted) — topics already scoped in `MIW_Bootstrap_Governance_Review.md` §2; no content exists yet.
- **`IMPLEMENTATION_CONTRACT.md`** — this is the one genuinely open classification question. It is not a record of past reasoning; it is the operative rulebook this very package is being executed under. By function, it belongs with `ENGINEERING_PRINCIPLES.md` and the ADRs as permanent governance, which under the frozen architecture means `docs/`. It currently sits in `reports/governance/` only because that was the fastest safe place to rescue it from being local-only (PKG-1.7). **Recommendation: reclassify as permanent governance, destined for `docs/` — flagged as a Founder decision below, not assumed.**
- Future packages already scope more permanent governance into `docs/` by design: `CORRECTION_WORKFLOW.md` (PKG-5), `GIT_WORKFLOW.md` / `RELEASE_WORKFLOW.md` (PKG-4), `PROJECT.md` / `ARCHITECTURE.md` (PKG-2), content standards docs (PKG-3), `CLAUDE.md` (PKG-12). These are out of this package's scope — noted only so the end-state picture is complete.

### 3b. What should be historical records

Content whose value is in *why a decision was made*, not in being consulted for compliance going forward:

- `MIW_Bootstrap_Blueprint.md` — origin draft, never itself approved, superseded in particulars by the two reviews below. Clearly historical.
- `MIW_Bootstrap_Governance_Review.md` — **approved**, meaning its conclusions are binding, but its *form* is discursive review/recommendation prose, not a standing rule artifact. Once ADR-0001–0005 are drafted, the ADR-track portions of this review become formally captured elsewhere, and this document becomes pure provenance record of the reasoning behind them (and behind the 10-item principles seed, and the package reordering). Its binding conclusions remain in force regardless of where the file sits — reclassifying it as "historical" does not reopen anything.
- `MIW_Architecture_Freeze_Review.md` — same logic. The *fact* of the frozen structure is simple enough to be restated compactly wherever needed (e.g., a future `docs/ARCHITECTURE.md`); the *why* — the ten-criterion comparison against the rejected wrapper proposal — is exactly what a historical decision record is for.

### 3c. What should be implementation reports

Point-in-time output of a specific review, audit, or package's completion — generated once, read for its findings, never edited afterward to "stay current":

- `reports/audit/2026-07-30_repo_audit.md` — already correctly placed.
- `reports/packages/PKG-1_COMPLETION_SUMMARY.md` — already correctly placed. **Gap noted:** PKG-1.6, PKG-1.7, and PKG-1.5R did not produce an equivalent committed report file — their reports were delivered in chat only. This package doesn't resolve that gap, but it's the same category question and worth the Founder's attention alongside this decision.
- `ONBOARDING_VERIFICATION_REPORT.md`, `BOOTSTRAP_CONSOLIDATION_PLAN.md`, `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` — all three are exactly this category (review/analysis output of a specific activity), currently sitting uncommitted at repository root instead of under `reports/`. This is the most direct, immediately-actionable finding in this analysis.

### 3d. What should eventually live under `docs/`

Per §3a: `ENGINEERING_PRINCIPLES.md`, `docs/adr/0001–0005`, and — pending the Founder's decision — `IMPLEMENTATION_CONTRACT.md`. Beyond this package's scope but part of the same eventual directory: every PKG-2 through PKG-12 documentation deliverable already named in the Blueprint's original layout.

### 3e. What should remain under `reports/`

- `reports/audit/`, `reports/packages/` — as-is, continuing pattern.
- A new subfolder for review/analysis artifacts (e.g., `reports/reviews/`) to hold the three currently-loose documents from §3c, so root stops accumulating ad hoc report files.
- A historical/decision-record archive for the §3b documents. Two placement options, both defensible:
  - **Keep them in `reports/governance/`** — consistent with the Blueprint's original framing of `reports/` as generated/non-authoritative output, and requires no new top-level naming decision.
  - **Rename to something that doesn't read as "current governance"** — e.g. `reports/governance-history/` or `reports/decisions/` — since "governance/" as a name implies active governing, which is misleading once `IMPLEMENTATION_CONTRACT.md` (the one document in that folder that actually *is* active governance) moves out.
  
  This naming ambiguity is itself a finding: right now, a reader who sees `reports/governance/` and doesn't check each file's Status line would reasonably assume everything inside it is currently authoritative. Two of five files are approved-but-historical, one is approved-and-still-actively-governing, and one is unapproved-and-unresolved. The folder name doesn't currently distinguish any of that.

### 3f. Bootstrap_Architecture_Amendment_LocalFirst.md — unresolved, doesn't fit cleanly into any category above

Flagged again here (previously surfaced in the PKG-1.7 report and in `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` §7) because this package's classification exercise makes its in-between status more visible, not less: it is not approved, so it isn't permanent governance; but it describes the *actual mechanism every commit in this session has used*, so it isn't purely historical either. It stays wherever the §3b archive ends up, but its own approval status is a separate, still-open Founder decision this package does not resolve.

---

## 4. Recommended Migration Sequence

**No migration in this package** — per this package's own boundaries. The sequence below is a recommendation for a later package, contingent on the Founder decisions in Section 6.

1. **Trigger point:** wait until `docs/` is first created — which will happen naturally when the Engineering Principles redraft (PKG-1.5R's eventual output) lands at `docs/ENGINEERING_PRINCIPLES.md`. Migrating governance-architecture files before `docs/` exists means creating it prematurely for this purpose alone, which is exactly the kind of speculative-structure move the surviving evidence base (`ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` Theme G — the single most-reinforced idea across all sources) argues against.
2. **At that point, in one small package:**
   - `git mv reports/governance/IMPLEMENTATION_CONTRACT.md` → `docs/IMPLEMENTATION_CONTRACT.md` (or `docs/governance/IMPLEMENTATION_CONTRACT.md`, depending on the Founder's answer to whether `docs/` gets its own governance subfolder — not decided here) — **only if** the Founder confirms the §3a reclassification.
   - Decide and apply the §3e naming question for the remaining historical-archive folder (keep `reports/governance/` or rename).
   - Commit the three §3c review artifacts into their new `reports/` subfolder.
   - Resolve (separately, not silently folded in) the Amendment document's approval status per §3f.
3. **Do not** move `MIW_Bootstrap_Blueprint.md`, `MIW_Bootstrap_Governance_Review.md`, or `MIW_Architecture_Freeze_Review.md` out of the historical archive location — under every option considered in §3e, all three stay in the archive; only its name is in question, not whether these three files belong there.

---

## 5. Files Affected (by the future migration this package recommends, not by this package itself)

| File | Current location | Proposed destination | Contingent on |
|---|---|---|---|
| `IMPLEMENTATION_CONTRACT.md` | `reports/governance/` | `docs/` (exact subpath TBD) | Founder decision 1 |
| `MIW_Bootstrap_Blueprint.md` | `reports/governance/` | Same folder, possibly renamed | Founder decision 2 |
| `MIW_Bootstrap_Governance_Review.md` | `reports/governance/` | Same folder, possibly renamed | Founder decision 2 |
| `MIW_Architecture_Freeze_Review.md` | `reports/governance/` | Same folder, possibly renamed | Founder decision 2 |
| `Bootstrap_Architecture_Amendment_LocalFirst.md` | `reports/governance/` | Same folder, possibly renamed | Founder decisions 2 and 3 |
| `ONBOARDING_VERIFICATION_REPORT.md` | repo root, uncommitted | `reports/reviews/` (or similar) | Founder decision 4 |
| `BOOTSTRAP_CONSOLIDATION_PLAN.md` | repo root, uncommitted | `reports/reviews/` (or similar) | Founder decision 4 |
| `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` | repo root, uncommitted | `reports/reviews/` (or similar) | Founder decision 4 |

**Zero files are affected by this package itself** — this table describes a future, separately-authorized migration only.

---

## 6. Risks

- **Moving `IMPLEMENTATION_CONTRACT.md` before `docs/` exists would be premature structure-creation** — directly contrary to the most-reinforced principle in the surviving evidence base (no speculative structure). This is why the recommended sequence gates migration on `docs/` already existing for an unrelated reason (the principles file), not on creating `docs/` specifically to hold the Contract.
- **Continuity risk for the three uncommitted review artifacts is real and ongoing**, independent of which subfolder they eventually land in. They currently share the exact single-point-of-failure risk the governance documents had before PKG-1.7 (local-machine-only, not recoverable from a fresh clone). This package does not resolve that — committing them, even to a provisional location, is arguably more urgent than settling their final subfolder name.
- **Renaming `reports/governance/` (if chosen) touches five files' paths at once** — low technical risk (git tracks renames cleanly), but every existing citation to the current path — including this document, `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md`, and the PKG-1.7 commit message — would describe a path that no longer exists. Not a broken link in the technical sense (nothing in the repository currently hyperlinks to these paths), but a readability cost for anyone cross-referencing past reports against current structure.
- **Deferring the Amendment document's approval status again** (as this package does, deliberately) lets an actively-relied-upon workflow rule (Local-First) continue operating without a fully current textual basis in `IMPLEMENTATION_CONTRACT.md`. Low practical risk today (the workflow is being followed correctly regardless), but it's the third package in a row to note this without resolving it.
- **Over-designing the information architecture itself is a risk this document tries to avoid** — the recommendations above are deliberately minimal (one new subfolder, one possible rename, one file reclassification) rather than a larger restructuring, consistent with the evidence base's own anti-over-engineering theme.

---

## 7. Founder Decisions Required

1. **Should `IMPLEMENTATION_CONTRACT.md` be reclassified as permanent governance and migrate to `docs/`** (recommended in §3a), or does it stay classified alongside the historical decision records in the archive folder? If it moves to `docs/`, does it get its own `docs/governance/` subfolder, or sit directly in `docs/`?
2. **Should the historical-archive folder keep the name `reports/governance/`, or be renamed** (e.g. `reports/governance-history/`, `reports/decisions/`) to stop implying active governance once (or if) `IMPLEMENTATION_CONTRACT.md` moves out of it?
3. **Should `Bootstrap_Architecture_Amendment_LocalFirst.md`'s approval status be resolved now** (approve it and apply its described update to `IMPLEMENTATION_CONTRACT.md` §4/§7), or explicitly deferred again to a later, dedicated package?
4. **Should the three uncommitted review artifacts be committed** (to `reports/reviews/` or wherever is decided), and if so, is that urgent enough to happen before the broader migration in Section 4, given their standalone continuity risk (§6)?
5. **Confirm the migration trigger:** wait for `docs/` to be created naturally by the Engineering Principles redraft (recommended), or execute this migration as its own dedicated package sooner, independent of that trigger?

---

## 8. Closing Note

This document makes no changes to the repository. `MIW_Architecture_Freeze_Review.md`, `IMPLEMENTATION_CONTRACT.md`, `AI_SESSION_HANDOVER.md`, and `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` were reviewed as instructed; current repository structure was verified directly against `git ls-files` rather than assumed from memory. No file was moved, renamed, modified, or committed. Submitted for Founder review.
