# Architecture

**Status:** Draft (v0.1) — pending Founder review. Describes current, factual repository structure; intended to be updated as that structure changes.
**Governs:** Nothing new — this document describes what `MIW_Architecture_Freeze_Review.md` (Approved) already froze and what `reports/governance/IMPLEMENTATION_CONTRACT.md` (Approved) already binds. Any conflict between this document and those two is an error in this document, not a change to them.
**Date:** 2026-07-31
**Companion document:** `docs/PROJECT.md` — that document answers *why* this repository exists; this one answers *how* it is built and maintained.

---

## Repository Layout

The frozen top-level structure (`MIW_Architecture_Freeze_Review.md` §6, Approved):

```
marine-intelligence-weekly/
├── docs/            (incl. docs/adr/)
├── skills/
├── templates/
├── reports/
├── corrections/
├── tools/           (incl. tools/_lib/)
├── meoclass1/, SQ/, GHGDecarb/, archive/, ecosystem.html, timeline.html  (existing content, unchanged)
└── .github/         (existing, unchanged)
```

**Actual current state**, verified directly rather than assumed from the frozen plan:

| Directory | State |
|---|---|
| `docs/` | Populated — `ENGINEERING_PRINCIPLES.md`, `CORRECTION_WORKFLOW.md`, `BOOTSTRAP_BASELINE.md`, `PROJECT.md`, this document |
| `reports/` | Populated — `audit/`, `governance/`, `packages/`, `reviews/` |
| `skills/`, `templates/`, `corrections/`, `tools/` | Frozen in plan, **not yet built** — per `docs/ENGINEERING_PRINCIPLES.md` P5 (No Speculative Structure), created only when a package genuinely needs them |
| `meoclass1/`, `SQ/`, `GHGDecarb/`, `archive/`, `articles/`, `assets/`, `api/`, root content HTML | Pre-existing, unchanged by the bootstrap |
| `RulesApp/` | Co-located, separate product — confirmed by `reports/audit/2026-07-30_repo_audit.md` to be a subdirectory of this same repository, not external |
| `.github/workflows/` | One workflow, `qb-health-check.yml` — daily automated content health check |

---

## Package Workflow

Every unit of work in this repository is a **package**, executed under the eight-stage lifecycle defined in full in `reports/governance/IMPLEMENTATION_CONTRACT.md` §2 (summarized, not restated, per `docs/ENGINEERING_PRINCIPLES.md` P2):

```
Planning → Implementation → Validation → Founder Review
   → (Revision loop, if needed) → Commit → Verification → Report → Next Package
```

No stage may be skipped or merged. Full stage definitions, the Definition of Done (§3), Commit Policy (§4), Validation Policy (§5), Chat/Code responsibilities (§6–7), and Escalation Policy (§8) live in the Contract itself — this document does not duplicate them.

**Package numbering**, per current practice: a package maps to an already-defined roadmap item (the original PKG-0–PKG-13 sequence in `reports/governance/MIW_Bootstrap_Blueprint.md` §4 as revised by `MIW_Bootstrap_Governance_Review.md` §4, or a subsequently-identified item recorded in `docs/BOOTSTRAP_BASELINE.md`'s Remaining Open Packages). A genuinely new package that doesn't map to an existing roadmap item requires a documented roadmap amendment before implementation begins, not an improvised number.

---

## Governance Hierarchy

Four layers, each with a distinct scope, none duplicating another (`docs/ENGINEERING_PRINCIPLES.md` P2):

1. **Architecture** (`MIW_Architecture_Freeze_Review.md`, Approved) — the frozen structural decision: what top-level directories exist and why. Changes require a new ADR (`IMPLEMENTATION_CONTRACT.md` §11).
2. **Process** (`IMPLEMENTATION_CONTRACT.md`, Approved) — how any package is executed, validated, committed, and verified. Governs execution, not content.
3. **Values** (`docs/ENGINEERING_PRINCIPLES.md`, Draft v0.2) — what "good" looks like at each process stage requiring judgment. Six ADR topics (`ADR-0001`–`ADR-0006`) are reserved under this layer for decisions needing deeper, case-specific reasoning than a one-line principle can carry; none are drafted yet.
4. **Operational procedure** (e.g. `docs/CORRECTION_WORKFLOW.md`) — how one specific, recurring category of work (corrections) applies layers 2 and 3 in practice. Future operational documents (`docs/GIT_WORKFLOW.md`, `docs/RELEASE_WORKFLOW.md`, per the roadmap) will sit at this same layer.

`reports/governance/MIW_Bootstrap_Blueprint.md` sits outside this hierarchy — it is the original, never-independently-approved planning draft that layers 1–2 above superseded in particulars; kept as historical record, not consulted for current authority.

---

## Document Relationships

| Location | Role | Amended over time? |
|---|---|---|
| `docs/` | Authoritative, currently-binding reference (governance and operational) | Yes — `docs/ENGINEERING_PRINCIPLES.md` has an explicit Amendment Policy; this document and `docs/PROJECT.md` update as repository state changes |
| `reports/audit/`, `reports/packages/` | Point-in-time audit and package-completion reports | No — written once, never edited after the fact |
| `reports/reviews/` | Point-in-time review/analysis/planning artifacts not tied to one package number | No |
| `reports/governance/` | Historical decision-record archive (`MIW_Bootstrap_Blueprint.md`, `MIW_Bootstrap_Governance_Review.md`, `MIW_Architecture_Freeze_Review.md`, `Bootstrap_Architecture_Amendment_LocalFirst.md`) **and**, currently, `IMPLEMENTATION_CONTRACT.md` (actively-governing, per a planned-but-not-yet-executed relocation to `docs/` — see `reports/reviews/GOVERNANCE_MIGRATION_SPECIFICATION.md`) | Historical portion: no. `IMPLEMENTATION_CONTRACT.md`: yes, but rarely, and only through the Contract's own governed amendment path |
| `docs/BOOTSTRAP_BASELINE.md` | Frozen historical snapshot of repository state at bootstrap governance closure | No — explicitly not amended, by its own text |
| `AI_SESSION_HANDOVER.md` (root) | Session-bridging status document | Self-describes as superseded once `docs/CLAUDE.md` (PKG-12) exists; currently stale relative to actual repository state (`docs/BOOTSTRAP_BASELINE.md` Known Limitations) |

---

## Repository Lifecycle

A change enters the repository through one of the entry points already named in `docs/CORRECTION_WORKFLOW.md` (for corrections) or as a new roadmap package (for everything else), moves through the Package Workflow above, and — once committed — becomes part of the permanent, git-tracked record per `docs/ENGINEERING_PRINCIPLES.md` P1. Nothing is removed from history; a wrong decision is corrected going forward (a new commit, or a superseding document), never rewritten in place (`IMPLEMENTATION_CONTRACT.md` §4: force-push and history rewriting are prohibited without exception).

Documents follow the same never-delete convention already established for ADRs (`MIW_Bootstrap_Governance_Review.md` §2: "Never delete an ADR, even if superseded — supersession is itself a valuable record") and applied one level up to governance itself in `reports/reviews/GOVERNANCE_MIGRATION_SPECIFICATION.md` §4's archive design.

---

## Future Expansion

Per `docs/ENGINEERING_PRINCIPLES.md` P5, nothing below is built speculatively — it is already-scoped, committed roadmap, listed here as reference, not proposed fresh by this document:

- **Remaining frozen-but-unbuilt structure:** `skills/`, `templates/`, `corrections/`, `tools/` (`MIW_Architecture_Freeze_Review.md` §6) — each created only when a package genuinely needs it.
- **Remaining roadmap packages** (`docs/BOOTSTRAP_BASELINE.md`, Remaining Open Packages): PKG-1.8 (Notes Manifest Resolution), PKG-3 (Content Standards Docs), PKG-4 (Git & Release Workflow Docs), PKG-6 through PKG-13 (Python utility tiers, remaining skills, corrections ledger, `docs/CLAUDE.md`, retrospective).
- **Six reserved ADRs** (`docs/ENGINEERING_PRINCIPLES.md`, Reserved for ADR table) — none drafted.
- **Governance migration** (`reports/reviews/GOVERNANCE_MIGRATION_SPECIFICATION.md`): moving `IMPLEMENTATION_CONTRACT.md` into `docs/` and renaming `reports/governance/` — precondition (`docs/` existing) now met, migration itself not yet executed.

Any expansion beyond this already-scoped list requires the roadmap-amendment step described under Package Workflow, above — not an ad hoc addition to this document.
