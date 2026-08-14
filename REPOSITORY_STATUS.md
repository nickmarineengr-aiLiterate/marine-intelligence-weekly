# Repository Status

**Audience:** The Founder and future human maintainers. **Not an AI onboarding document** — AI sessions should read `AI_SESSION_START.md` instead. This document is the executive-summary companion to it: read this to understand *where things stand and why*; read `AI_SESSION_START.md`/`docs/PROJECT.md` for the operational and technical detail this document deliberately doesn't repeat.
**Date:** 2026-07-31
**Status:** Point-in-time closeout summary, written at the end of the engineering bootstrap. Not a living document — if you're reading this more than a few months after 2026-07-31, verify its claims against live repository state (`git log`, `docs/`, `reports/`) before trusting them.

---

## 1. Repository Overview

Marine Intelligence Weekly (MIW) is a maritime newsletter and subscription platform, built around an MEO Class 1 oral-exam preparation product (`meoclass1/`), plus a timeline, ecosystem map, issue archive, and GHG/decarbonisation tracking. It also co-hosts an unrelated, pre-existing product, `RulesApp/`, as a sibling directory. Intended users: MEO Class 1 exam candidates (the paying subscriber base), newsletter readers, and future engineers/maintainers of the repository itself. Full detail: `docs/PROJECT.md`.

## 2. Current Repository Maturity

**Post-governance-bootstrap.** Before 2026-07-30, engineering knowledge about this repository — why it's structured the way it is, how corrections should be handled, what "good" looks like — lived only in conversation. A dedicated bootstrap (PKG-1 through the present) fixed that: the repository now has a committed audit, a frozen architecture, a binding execution contract, a first draft of engineering values, an operational correction workflow, and an AI onboarding entry point. The bootstrap has **not** fully closed against its own defined completion bar — two mandatory items remain open (Section 6).

## 3. Engineering Milestones Completed

- **PKG-1 — Repository Audit.** Surfaced real, evidence-based findings (non-functional `.gitignore`, duplicate Notes manifests, co-located `RulesApp/`, and others).
- **Architecture Freeze.** A proposed `engineering/` wrapper directory was reviewed and rejected on ten criteria; the flat structure (`docs/`, `skills/`, `templates/`, `reports/`, `corrections/`, `tools/`) is now the Approved, frozen top-level layout.
- **Implementation Contract.** The binding 8-stage package lifecycle (Planning → Implementation → Validation → Founder Review → Commit → Verification → Report) and the Claude Chat/Code responsibility split — both Approved.
- **Engineering Principles.** Drafted (v0.1, 10 principles), independently reviewed, revised to v0.2 (7 principles: Repository First, Single Responsibility, Mechanical vs. Judgment Boundary, Verify Before Trust, No Speculative Structure, Code Executes Written Specs, Repository Independence).
- **PKG-2 — Core Docs.** `docs/PROJECT.md` and `docs/ARCHITECTURE.md` committed.
- **PKG-5 — Correction Workflow.** `docs/CORRECTION_WORKFLOW.md` — the first operational (non-governance) document, defining how content/repository/governance corrections are classified, verified, and committed.
- **PKG-11a — Corrections Ledger spec.** `corrections/README.md` + `TEMPLATE.md` — the format standard for a durable, per-correction record (backfilling historical entries is separately scoped as PKG-11b).
- **AI Onboarding.** `AI_SESSION_START.md` — the single authoritative entry point for any new AI session — drafted, refined per Founder feedback, approved, committed (`2c0fd8b`), and pushed.

## 4. Governance Status

Four layers, each Approved/committed except one:

| Layer | Document | Status |
|---|---|---|
| Architecture | `reports/governance/MIW_Architecture_Freeze_Review.md` | **Approved** |
| Process | `reports/governance/IMPLEMENTATION_CONTRACT.md` | **Approved** |
| Values | `docs/ENGINEERING_PRINCIPLES.md` | **Draft v0.2 — not yet Approved** |
| Operational procedure | `docs/CORRECTION_WORKFLOW.md`, `corrections/README.md` | **Operational** |

Six ADR topics are reserved (`ADR-0001`–`ADR-0006`, covering repository-first philosophy, Chat/Code division, doc hierarchy, correction philosophy, git/push authority, and no-speculative-structure); none are drafted yet. One further governance item, `Bootstrap_Architecture_Amendment_LocalFirst.md`, remains an unresolved `Proposed` amendment. None of this is new or a regression — it's the same disclosed gap the bootstrap has carried since its own baseline.

## 5. AI Onboarding Status

`AI_SESSION_START.md` is the single authoritative AI onboarding entry point, committed and pushed. It carries a repository-identity banner (to prevent confusion with the separate `RulesApp` repository), a read-strategy that discourages reading the whole repository up front, and a rules section every AI session must follow. `AI_SESSION_HANDOVER.md` (the prior bridge document) is deliberately left in place, unmodified, pending validation of `AI_SESSION_START.md` across several real future sessions — see Section 6.

## 6. Current Open Items

**Mandatory** (the bootstrap's own defined completion bar is not met without these):
- Founder approval of `docs/ENGINEERING_PRINCIPLES.md` (currently Draft v0.2).
- Drafting the six reserved ADRs (`ADR-0001`–`ADR-0006`).

**Optional** (scoped, not urgent):
- PKG-1.8 (Notes Manifest Resolution — two competing manifest files, unresolved since PKG-1).
- PKG-3 (Content Standards Docs), PKG-4 (Git/Release Workflow Docs), PKG-6–13 (Python tooling tiers, remaining skills, PKG-11b ledger backfill, `docs/CLAUDE.md`, retrospective).
- Governance-doc migration (`reports/governance/` → partially into `docs/`).
- Resolution of `Bootstrap_Architecture_Amendment_LocalFirst.md`.

**Deferred** (explicitly, by Founder decision, not forgotten):
- Retiring `AI_SESSION_HANDOVER.md` — held until `AI_SESSION_START.md` has been validated across several fresh AI onboarding sessions.

## 7. Current Repository Mode

**Maintenance Mode.**

The repository is in a stable, internally consistent state: git is synced with `origin/main`, no broken references exist, and the governance foundation — while not 100% closed against its own bar — is solid enough that the repository can sit untouched indefinitely without risk (per `IMPLEMENTATION_CONTRACT.md`'s own package-end checklist: "confirmed in a working, complete state — safe to stop here indefinitely if needed"). Development paused not because of a problem, but because the Founder made a deliberate call to redirect attention to `RulesApp` as the primary engineering focus. Nothing here is blocking, urgent, or decaying by being left alone.

## 8. When Development Should Resume

Pick this back up when any of the following actually happens — not speculatively (per Engineering Principle P5):

- A new editorial capability or content type is needed for MIW.
- A concrete governance change is demonstrated necessary by a real implementation need (not a stylistic improvement).
- A workflow improvement is discovered mid-package, elsewhere, that's worth adopting deliberately (per `IMPLEMENTATION_CONTRACT.md` §10).
- Major content expansion is planned for `meoclass1/` or related products.
- Validation across several fresh AI sessions shows `AI_SESSION_START.md` needs revision, or shows it's safe to retire `AI_SESSION_HANDOVER.md`.
- The Founder is ready to close the two Mandatory items (Section 6) and formally complete the bootstrap.

## 9. Founder Notes

A note to my future self: this repository reached a genuinely solid governance foundation — audited, frozen architecture, a binding execution contract, a values draft, an operational correction workflow, and a single AI onboarding document I trust to orient a new session correctly. It is not *finished* by the bootstrap's own bar (Engineering Principles is still Draft, six ADRs are still unwritten), but it is *safe* — nothing is broken, nothing is drifting, and picking it back up costs nothing but reading this document and `AI_SESSION_START.md`. I paused here deliberately, not because MIW stalled or hit a problem, but because `RulesApp` became the more pressing engineering priority. When I come back, the two Mandatory items are the honest starting point — everything else is genuinely optional until a real need names it.

---

*This document does not duplicate `AI_SESSION_START.md` or `docs/PROJECT.md` — for AI-session operating rules see the former; for the repository's technical purpose and structure see the latter and `docs/ARCHITECTURE.md`.*
