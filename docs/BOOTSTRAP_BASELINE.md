# Bootstrap Baseline

**Status:** Historical reference point — describes the repository as it existed at bootstrap closure. Not a living document; not amended to track future state.
**Date:** 2026-07-31
**Purpose:** A single authoritative record of the repository immediately after the engineering bootstrap phase, for future sessions and collaborators to orient against. Describes what exists today only — proposes no new architecture, no new packages, no new principles.
**Source discipline:** Every statement below cites a committed repository document (file content or `git log` commit message). No claim is drawn from conversation memory alone.

---

## Bootstrap Objectives

Per `reports/governance/MIW_Bootstrap_Blueprint.md` and `reports/governance/MIW_Bootstrap_Governance_Review.md` §1, the bootstrap's objective was to stop the repository's governing knowledge — architecture rationale, workflow rules, engineering values — from living only in conversation, and instead make the repository itself "the source of truth" (`MIW_Bootstrap_Governance_Review.md` §1). Concretely: establish a `docs/`/`skills/`/`tools/`/`templates/`/`reports/`/`corrections/` structure (`MIW_Architecture_Freeze_Review.md` §6, frozen), a package execution lifecycle with explicit gates (`reports/governance/IMPLEMENTATION_CONTRACT.md`), and a governance baseline (Engineering Principles, ADRs) that future packages are checked against.

---

## Bootstrap Scope

**In scope, per `MIW_Bootstrap_Blueprint.md` Open Questions §4 and `MIW_Bootstrap_Governance_Review.md` §10 (Sign-off checklist):** infrastructure and governance only. Explicitly and by design, **no package in this bootstrap touched a live QB/Notes/WA content file** — confirmed in both documents as an intentional constraint so the bootstrap "can be reviewed and merged without any content-correctness risk" (`MIW_Bootstrap_Blueprint.md`, Open Questions §4).

**Out of scope:** MEO Class 1 content authoring/correction, payment/auth backend changes, the `RulesApp/` co-located product (`reports/audit/2026-07-30_repo_audit.md`, Findings: "RulesApp is co-located, not external" — confirmed as a separate, pre-existing product sharing this repository, not part of this bootstrap).

**Numbered package sequence** (`MIW_Bootstrap_Governance_Review.md` §4, §9, revising `MIW_Bootstrap_Blueprint.md` §4): PKG-0 through PKG-13, with PKG-1.5 (Governance Docs) inserted before PKG-2, PKG-9 merged into PKG-8, and PKG-11 split into PKG-11a/11b.

**Interstitial packages** (not part of the original numbered sequence; each executed under a distinct Founder-directed package during the bootstrap, evidenced by commit messages and the `reports/reviews/` documents rather than the original planning documents): PKG-1.6 (`.gitignore` fix — named as a candidate in `reports/audit/2026-07-30_repo_audit.md`, Recommendations item 1), PKG-1.7 (Governance Foundation commit — per `reports/reviews/GOVERNANCE_ARCHITECTURE_DECISION.md` §1), PKG-1.5R and PKG-1.5R(v1.0) (Engineering Principles redevelopment — per `docs/ENGINEERING_PRINCIPLES.md` revision history and commit log), PKG-1.9 (Governance Architecture Consolidation — per `reports/reviews/GOVERNANCE_MIGRATION_SPECIFICATION.md` header), PKG-2.0 (Governance Migration Preparation — per `reports/reviews/GOVERNANCE_MIGRATION_SPECIFICATION.md` header), PKG-2.1 (Bootstrap Closure of review artifacts — per commit `1f7b24f`'s message), and this document's own package, PKG-1.10.

---

## Governance Documents

All currently committed, with status exactly as their own text states:

| Document | Location | Status (as stated in the file) |
|---|---|---|
| `MIW_Bootstrap_Blueprint.md` | `reports/governance/` | "Draft for Founder Architecture Review" — never itself approved; superseded in particulars by the two reviews below |
| `MIW_Bootstrap_Governance_Review.md` | `reports/governance/` | "Approved (Founder decision, 2026-07-31) — Pre-PKG-1 gate review" |
| `MIW_Architecture_Freeze_Review.md` | `reports/governance/` | "Approved (Founder decision, 2026-07-31) — final structural decision, ratified before PKG-1" |
| `IMPLEMENTATION_CONTRACT.md` | `reports/governance/` | "Approved (Founder decision, 2026-07-31)" |
| `Bootstrap_Architecture_Amendment_LocalFirst.md` | `reports/governance/` | "Proposed amendment, pending Founder approval" — unresolved |
| `ENGINEERING_PRINCIPLES.md` | `docs/` | "Draft (v0.2) — pending Founder review. Not promoted to Approved this pass" |
| `AI_SESSION_HANDOVER.md` | repository root | Self-describes: "Not permanent governance. Superseded by `docs/CLAUDE.md` once that package is reached." |

**Supporting review/evidence documents, also committed**, under `reports/reviews/`: `ONBOARDING_VERIFICATION_REPORT.md`, `BOOTSTRAP_CONSOLIDATION_PLAN.md`, `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md`, `GOVERNANCE_ARCHITECTURE_DECISION.md`, `GOVERNANCE_MIGRATION_SPECIFICATION.md`.

**Referenced but not committed:** `docs/ENGINEERING_PRINCIPLES.md` itself cites two supporting documents by name — `ENGINEERING_PRINCIPLES_AUTHORING_FRAMEWORK.md` and `ENGINEERING_PRINCIPLES_REVIEW.md` — neither of which is committed to the repository as of this baseline. See Known Limitations.

---

## Repository Structure

Per direct `git ls-files` inspection at the time of this baseline. Root-level structure:

**Bootstrap-created, present:** `docs/` (contains only `ENGINEERING_PRINCIPLES.md` and, as of this document, `BOOTSTRAP_BASELINE.md`), `reports/` (`audit/`, `governance/`, `packages/`, `reviews/`), `.gitignore` (corrected — see Lessons Learned).

**Frozen architecture, not yet created:** `skills/`, `templates/`, `corrections/`, `tools/` — named in `MIW_Architecture_Freeze_Review.md` §6's frozen tree but not built, because no package to date has required them (`MIW_Architecture_Freeze_Review.md`'s "Architecture ages fine" reasoning, §3: new directories cost nothing to add when a real need exists; none has yet, for these four).

**Pre-existing content, unchanged by this bootstrap:** `meoclass1/` (MEO Class 1 QB/oralnotes content), `SQ/`, `GHGDecarb/`, `archive/`, `articles/`, `assets/`, `api/`, root-level `index.html`/`index17.html`–`index30.html`, `youtube/`, `.github/workflows/` (one workflow, `qb-health-check.yml`, per `reports/audit/2026-07-30_repo_audit.md`).

**Co-located, separate product:** `RulesApp/` — confirmed by audit to be a subdirectory of this repository, not an external project, containing its own `app/`, `repository/`, `README.md`.

---

## Engineering Principles Status

`docs/ENGINEERING_PRINCIPLES.md`, **Status: Draft (v0.2)**. Contains 7 principles (P1–P7), down from an initial 10-principle Draft v0.1 after two merges (P1/P2, P4/P5) and two conversions of Contract-duplicative content into a "Reserved for the Implementation Contract" reference section, plus one addition (P7, Repository Independence) closing a gap identified during evidence-gathering. Six ADR topics are reserved (`ADR-0001` through `ADR-0006`); none are drafted. The document's own "Why This Remains Draft" section states three reasons it has not been promoted to Approved: one principle (P7) is content never previously reviewed before this version; all six referenced ADRs are undrafted; and only one review pass has occurred, which the document states explicitly does not substitute for Founder sign-off on the specific committed diff.

---

## Architecture Status

**Frozen**, per `MIW_Architecture_Freeze_Review.md` §6 (Approved). The flat top-level structure (`docs/`, `skills/`, `templates/`, `reports/`, `corrections/`, `tools/`, alongside unchanged existing content directories and `.github/`) was chosen over an `engineering/`-wrapper alternative, rejected on all ten reviewed criteria (§1). `IMPLEMENTATION_CONTRACT.md` §11 (Repository Freeze Policy) makes this binding: implementation may improve within the frozen boundaries but may not add, remove, or rename top-level directories, or reintroduce a rejected structure, without a new ADR proposal.

Only two of the six frozen top-level meta-directories exist and are populated as of this baseline (`docs/`, `reports/`); the remaining four (`skills/`, `templates/`, `corrections/`, `tools/`) are frozen-but-unbuilt, per the "No Speculative Structure" discipline now stated as `docs/ENGINEERING_PRINCIPLES.md` P5.

---

## Implementation Contract Status

`reports/governance/IMPLEMENTATION_CONTRACT.md`, **Status: Approved (Founder decision, 2026-07-31)**. States it "Governs: Execution of PKG-1 through PKG-13" — its eight-stage lifecycle (Planning → Implementation → Validation → Founder Review → [Revision] → Commit → Verification → Report) was applied in practice to the interstitial packages listed above (PKG-1.6 through PKG-1.10) as well, though the Contract's own text does not explicitly enumerate sub-numbered packages. See Known Limitations.

The Local-First git workflow (`Bootstrap_Architecture_Amendment_LocalFirst.md`) has been the actual commit/push mechanism used throughout — confirmed operational end-to-end per `reports/packages/PKG-1_COMPLETION_SUMMARY.md` §9 — but the Amendment document's own required update to `IMPLEMENTATION_CONTRACT.md` §4/§7 (naming Local-First explicitly rather than describing push authority abstractly) was never applied, and the Amendment itself remains unapproved. See Known Limitations.

---

## Remaining Open Packages

Per the numbered sequence (`MIW_Bootstrap_Governance_Review.md` §4, §9) and this bootstrap's own interstitial work, not yet started:

- **PKG-1.8 — Notes Manifest Resolution.** Named as a candidate in `reports/audit/2026-07-30_repo_audit.md` Recommendations item 2 and `reports/reviews/BOOTSTRAP_CONSOLIDATION_PLAN.md`. Blocks `PKG-8` (manifest tooling) until resolved.
- **PKG-2 — Core Docs** (`PROJECT.md`, `ARCHITECTURE.md`).
- **PKG-3 — Content Standards Docs.**
- **PKG-4 — Git & Release Workflow Docs.**
- **PKG-5 — Correction Workflow Doc + Skill** — named in `MIW_Bootstrap_Governance_Review.md` §9 as part of the Mandatory tier and "the single highest-value artifact in the entire roadmap."
- **PKG-6 through PKG-13** — Python utility tiers, remaining skills, corrections ledger, `CLAUDE.md`, retrospective — none started.
- **Six ADRs** (`ADR-0001`–`ADR-0006`, per `docs/ENGINEERING_PRINCIPLES.md`'s Reserved for ADR table) — none drafted.
- **Governance migration** — per `reports/reviews/GOVERNANCE_MIGRATION_SPECIFICATION.md`: move `IMPLEMENTATION_CONTRACT.md` to `docs/`, rename `reports/governance/` to `reports/bootstrap-archive/`. That document's stated precondition (`docs/ENGINEERING_PRINCIPLES.md` existing) is now met; the migration itself has not been executed.

---

## Deferred Work

Per `reports/audit/2026-07-30_repo_audit.md` Recommendations, explicitly deferred rather than resolved:

- Root/`archive/` duplicated legacy issues (17–22) and incomplete migration (issues 23–30) — recommended as a package "outside this bootstrap's numbered packages," scheduled separately under `miw-archive` skill scope (Recommendation 3).
- `SQ/` prefixed/unprefixed duplicate file pairs — deferred to PKG-3 or a standalone investigation (Recommendation 4).
- `api/check-db.js` / `api/migrate-users.js` purpose — deferred to PKG-2's `ARCHITECTURE.md` (Recommendation 7).
- `api/verify-session.js` discrepancy (referenced in prior project memory, absent from the repository) — deferred to PKG-2/PKG-4 (Recommendation 6).
- `package.json` `build`/`test` placeholder scripts — no committed recommendation resolves this; noted as low-severity in the audit's Technical Debt table.

---

## Known Limitations

1. **`AI_SESSION_HANDOVER.md` is stale.** It describes repository state as of commit `b3fc477` (2026-07-30) and predates every interstitial package from PKG-1.6 onward. It was not updated during this bootstrap.
2. **`docs/ENGINEERING_PRINCIPLES.md` cites two uncommitted supporting documents** (`ENGINEERING_PRINCIPLES_AUTHORING_FRAMEWORK.md`, `ENGINEERING_PRINCIPLES_REVIEW.md`) by name. Neither exists in the repository as of this baseline — a cross-reference that does not yet resolve, of the kind `IMPLEMENTATION_CONTRACT.md` §5 treats as a validation failure.
3. **`Bootstrap_Architecture_Amendment_LocalFirst.md` remains unapproved**, and its own required edit to `IMPLEMENTATION_CONTRACT.md` §4/§7 was never applied, despite Local-First being the mechanism used for every commit in this bootstrap.
4. **Zero ADRs exist.** Six topics are reserved; none are drafted, including the newly-added `ADR-0006` which itself requires Founder confirmation as a valid topic (per `docs/ENGINEERING_PRINCIPLES.md`, P5's ADR field).
5. **Duplicate Notes manifests remain unresolved** (`notes-content-index.json` vs. `notes_content_index.json`) — rated Critical severity in `reports/audit/2026-07-30_repo_audit.md`'s Technical Debt table.
6. **The `.gitignore` fix (PKG-1.6) is not retroactive.** It protects commits made after the fix; whether anything matching its patterns was committed before it was not investigated in this bootstrap.
7. **`reports/governance/` currently mixes document types.** It holds documents at three different approval states (approved, unapproved, and one — `IMPLEMENTATION_CONTRACT.md` — that is itself actively-governing rather than purely historical) under one folder name, per `reports/reviews/GOVERNANCE_ARCHITECTURE_DECISION.md` §3e's finding. The planned migration (see Remaining Open Packages) resolves this but has not run.

---

## Lessons Learned

Per `reports/packages/PKG-1_COMPLETION_SUMMARY.md` §9, and confirmed by subsequent bootstrap work:

- The GitHub connector's write path failed with an irreducibly ambiguous 403 error; this was resolved by testing an alternative (local Git), not by direct diagnosis. Connector-dependent assumptions should be verified early, not assumed reliable by default.
- Local-First (local repository → local git → push) is confirmed operational end-to-end and has been the standing mechanism for every commit in this bootstrap.
- Live repository inspection surfaced real issues (duplicate manifests, non-functional `.gitignore`, co-located `RulesApp`) invisible from project memory alone — direct confirmation of the bootstrap's own founding premise, that the repository, not the conversation, must be the source of truth.
- A document's own Status line can drift from actual practice if nothing revisits it: three governance documents were found, during PKG-1.5, still reading "pending Founder approval" or similar despite being relied upon as settled — see the Governance Documents table above for the state after correction.
- Committing a document immediately in an explicit Draft state, rather than waiting for full sign-off to commit at all, is the direct structural response `docs/ENGINEERING_PRINCIPLES.md` itself records to the loss of the original Engineering Principles document — which was, per that document's own text, drafted and discussed but never committed.

---

## Bootstrap Completion Criteria

`MIW_Bootstrap_Governance_Review.md` §9 defines a "Minimum Viable Bootstrap (Version 1 Scope)" with a **Mandatory tier**: PKG-1 (Repository Audit), PKG-1.5 (Governance Docs), PKG-5 (Correction Workflow doc + skill), and PKG-11a (Corrections ledger format spec only). Against that originally-stated bar:

- PKG-1 — **complete** (`reports/packages/PKG-1_COMPLETION_SUMMARY.md`: all eight lifecycle stages closed).
- PKG-1.5 — **partially complete**: governance document approvals are done; `docs/ENGINEERING_PRINCIPLES.md` exists but is Draft, not Approved.
- PKG-5, PKG-11a — **not started.**

**This baseline therefore marks the completion of the bootstrap's governance foundation** — audit, Contract, architecture freeze, and a first Engineering Principles draft — **not** the completion of the Mandatory tier the bootstrap's own governing documents defined as the actual "Version 1" bar. Describing the bootstrap as fully complete by that standard would contradict `MIW_Bootstrap_Governance_Review.md` §9 directly. What is complete: the repository now has a citable governance baseline to build the remaining Mandatory-tier work against, which it did not have before PKG-1.

---

## Recommended Starting Point for Operational Development

Two defensible options exist in the committed record, not a single obvious answer:

1. **PKG-1.8 (Notes Manifest Resolution)** — smallest remaining item, primarily a Founder decision (which manifest is authoritative) rather than new authoring work, and unblocks `PKG-8` early per the audit's own dependency note.
2. **PKG-5 (Correction Workflow Doc + Skill)** — explicitly named in `MIW_Bootstrap_Governance_Review.md` §9 as "the single highest-value artifact in the entire roadmap" and part of the Mandatory tier this baseline shows is still incomplete.

This document does not resolve which should come first — that is a scheduling judgment for the Founder, not an architectural one, and outside this baseline's remit to decide.
