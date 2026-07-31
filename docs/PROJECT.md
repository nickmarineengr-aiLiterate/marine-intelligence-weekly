# Project

**Status:** Draft (v0.1) — pending Founder review. Describes current, factual repository state; intended to be updated as that state changes (unlike `docs/BOOTSTRAP_BASELINE.md`, which is a frozen historical snapshot).
**Governs:** Nothing — this document informs, it does not bind. Governance lives in `docs/ENGINEERING_PRINCIPLES.md` and `reports/governance/IMPLEMENTATION_CONTRACT.md`.
**Date:** 2026-07-31
**Audience:** Every future engineer's or collaborator's first read — per `docs/ENGINEERING_PRINCIPLES.md` P7 (Repository Independence), this document plus `docs/ARCHITECTURE.md` should let a new reader understand the system without asking anyone a clarifying question.

---

## Why This Repository Exists

Marine Intelligence Weekly (MIW) is a maritime newsletter and subscription platform (`README.md`: "Weekly newsletter for marine engineers tracking AI, IMO compliance, classification updates and operational impact"), centered on an MEO Class 1 oral exam preparation product (`meoclass1/`), with associated content — a timeline, an ecosystem map, an issue archive, and GHG/decarbonisation tracking (`GHGDecarb/`). This repository is both the newsletter's published website and the exam-prep product's content and delivery system.

Separately, this repository also hosts the engineering discipline that makes the above maintainable: a governance foundation (`docs/ENGINEERING_PRINCIPLES.md`, `reports/governance/IMPLEMENTATION_CONTRACT.md`) built during a 2026-07 bootstrap, and an operational Correction Workflow (`docs/CORRECTION_WORKFLOW.md`) for keeping the published content accurate over time.

---

## What Problem It Solves

Two distinct problems, evidenced by two distinct parts of this repository:

1. **For MEO Class 1 candidates:** structured, examiner-pattern-aware oral exam preparation content — question banks (`meoclass1/QB1`–`QB10`, per `reports/audit/2026-07-30_repo_audit.md`: 89 distinct HTML files by direct count), cheat sheets, and oral-exam notes (`meoclass1/oralnotes/`) — gated behind a paid subscription (`package.json`: `miw-razorpay-backend`, a "Payment & Auth Backend" using Razorpay, Upstash Redis, and Nodemailer).
2. **For this repository's own maintainers:** the problem the 2026-07 bootstrap was built to solve — that engineering knowledge (why the architecture is shaped this way, how corrections should be processed, what "good" looks like for a new document) was "trapped in conversation" rather than committed and citable (`reports/governance/MIW_Bootstrap_Governance_Review.md` §1). `docs/ENGINEERING_PRINCIPLES.md` P1 states the resulting standing rule directly: the repository, not any conversation, is the source of truth.

---

## Repository Philosophy

Stated in full in `docs/ENGINEERING_PRINCIPLES.md` (currently Draft v0.2, 7 principles) — summarized, not restated, here per that document's own P2 (Single Responsibility):

- **Repository First (P1):** the repository is the source of truth; nothing is decided until it's committed.
- **Single Responsibility (P2):** one responsibility per document, one responsibility per tool — this is why `PROJECT.md` and `ARCHITECTURE.md` exist as two documents rather than one, and why neither restates governance already stated elsewhere.
- **Mechanical vs. Judgment Boundary (P3):** deterministic tasks go to tools; engineering/regulatory/correctness judgment is never automated.
- **Verify Before Trust (P4):** no content correction is applied without primary-source verification — the operating rule behind `docs/CORRECTION_WORKFLOW.md`.
- **No Speculative Structure (P5):** new documents, directories, or tools are built only when a real, demonstrated need exists.
- **Code Executes Written Specs (P6):** automated/mechanical execution works from committed specifications, not inferred history.
- **Repository Independence (P7):** a human must be able to understand this repository with zero AI assistance.

For the full statements, rationale, and ADR relationships, see `docs/ENGINEERING_PRINCIPLES.md` directly.

---

## Intended Users

- **MEO Class 1 exam candidates** — the paying subscriber base for `meoclass1/`'s content, referenced directly in the content itself (e.g. `meoclass1/known_traps.md` records corrections "flagged by a candidate").
- **Newsletter readers** — the broader marine-engineer audience for the weekly issues, timeline, and ecosystem content.
- **Future engineers and collaborators maintaining this repository** — the audience this document and `docs/ARCHITECTURE.md` are written for directly, per P7 above.
- **Future AI sessions** (Claude Chat and, per `reports/governance/IMPLEMENTATION_CONTRACT.md` §7, eventually Claude Code) — expected to work from this repository's committed documents rather than rediscovering context from conversation history, per P1 and P6.

---

## Current Maturity

As of this document's authoring (2026-07-31), more current than `docs/BOOTSTRAP_BASELINE.md`'s snapshot (also 2026-07-31, but frozen at an earlier point the same day — see that document's own "not amended to track future state" note):

- **Governance foundation:** established. `reports/governance/MIW_Bootstrap_Governance_Review.md`, `MIW_Architecture_Freeze_Review.md`, and `IMPLEMENTATION_CONTRACT.md` are all committed and Approved.
- **Engineering Principles:** `docs/ENGINEERING_PRINCIPLES.md` exists at Draft v0.2 (7 principles) — not yet Approved. Reasons are stated in the document's own "Why This Remains Draft" section.
- **Architecture Decision Records:** six topics reserved (`ADR-0001`–`ADR-0006`); none drafted.
- **Operational documentation:** `docs/CORRECTION_WORKFLOW.md` (PKG-5) is committed — the first operational, non-governance document produced under this bootstrap. This document and `docs/ARCHITECTURE.md` (PKG-2) are the second and third.
- **Bootstrap's own stated Mandatory tier** (`reports/governance/MIW_Bootstrap_Governance_Review.md` §9: PKG-1, PKG-1.5, PKG-5, PKG-11a): three of four items now done (PKG-1, PKG-5, and PKG-1.5 partially — governance approvals complete, Principles still Draft). PKG-11a (`corrections/` ledger format spec) has not started.
- **Content maintenance infrastructure:** one active automation (`.github/workflows/qb-health-check.yml`, daily), one known unresolved technical-debt item at Critical severity (duplicate Notes manifests, `reports/audit/2026-07-30_repo_audit.md`), tracked as PKG-1.8, not yet started.
- **`skills/`, `templates/`, `corrections/`, `tools/`** — frozen in the target architecture (`MIW_Architecture_Freeze_Review.md` §6), not yet built, consistent with P5.

---

## What This Document Does Not Cover

Per `docs/ENGINEERING_PRINCIPLES.md` P2, technical/business architecture (payment flow, hosting, environment variables, auth mechanism) belongs in `docs/ARCHITECTURE.md` or a future dedicated document — not duplicated here. As of this package, that specific technical detail (Razorpay/Redis/Brevo flow, hosting provider, auth gate mechanism) remains undocumented in either `PROJECT.md` or `ARCHITECTURE.md`; both currently describe the repository's engineering/governance shape, not its payment/hosting technical stack. Flagged here rather than silently left implicit.
