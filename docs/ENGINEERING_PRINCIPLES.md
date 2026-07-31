# Engineering Principles

**Status:** Draft (v0.1) — pending Founder review
**Governs:** All packages, all documents, all tools produced under this repository's engineering bootstrap and beyond
**Date:** 2026-07-31
**Replaces:** The original Engineering Principles document, confirmed unrecoverable (see `reports/reviews/ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md`). This is a new document, authored from surviving repository evidence only — not a reconstruction of the original.

---

## Purpose

This document is the single compliance reference every package's output is checked against. It is not a philosophy essay to be read once — `IMPLEMENTATION_CONTRACT.md` §9 makes it operational: the Governance Gate checks every package's output against this document and the ADR set on every single package, and §3's Definition of Done already names "the single-responsibility principle from `ENGINEERING_PRINCIPLES.md`" as a live compliance check. Write for a reader — human or AI — with no access to the conversation that produced this document.

---

## Principles

### P1. Repository First — `repository-first`
**Statement:** The repository is the source of truth. Conversations, chat history, and session memory are disposable and carry no authority once a session ends.
**Rationale:** Without this, "everything downstream (docs, skills, tools) is built on an assumption, not a reference" (`MIW_Bootstrap_Governance_Review.md` §1). `IMPLEMENTATION_CONTRACT.md` §1 item 8 states the same rule as binding: "The repository, not the conversation, is what future sessions will trust."
**Relationships:** Foundational — P2 defines *how* truth gets recorded in the repository; P10 applies this principle directly to Claude Code's execution model.
**ADR:** Reserved — `ADR-0001` (repository-first philosophy), named in `MIW_Bootstrap_Governance_Review.md` §2. Not yet drafted.

### P2. Documentation Is Authoritative — `documentation-authoritative`
**Statement:** If a decision is not written down in the repository, it is not decided — regardless of what was discussed or agreed in conversation.
**Rationale:** This principle's own history is the clearest evidence for why it matters: per `ENGINEERING_PRINCIPLES_AUTHORING_FRAMEWORK.md` §9, the original Engineering Principles were reportedly drafted and discussed but never committed, and are now confirmed unrecoverable.
**Relationships:** Companion to P1. Directly enforced by this document's own authoring workflow — Draft 1 is committed immediately rather than left pending in conversation, per the Authoring Framework's explicit recommendation.
**ADR:** None reserved.

### P3. Single Responsibility — `single-responsibility`
**Statement:** Each document and each tool owns exactly one responsibility. Content is not duplicated across documents; behavior is not duplicated across tools.
**Rationale:** `IMPLEMENTATION_CONTRACT.md` §3 already checks every package's output against this principle by name. `MIW_Architecture_Freeze_Review.md`'s comparison table (criterion 9) cites the same rule as already-decided when rejecting the `engineering/` wrapper proposal.
**Relationships:** Governs P9 from the artifact-scope side — P3 constrains what an artifact covers once it exists; P9 constrains whether it should exist at all.
**ADR:** Reserved — `ADR-0003` (documentation hierarchy: docs = what/why, skills = how/when, tools = mechanical execution), named in `MIW_Bootstrap_Governance_Review.md` §2. Not yet drafted.

### P4. Deterministic Tooling — `deterministic-tooling`
**Statement:** Wherever a task is mechanical and its outcome is fully determined by explicit rules, it is performed by a deterministic tool, not by repeated AI judgment.
**Rationale:** `MIW_Bootstrap_Governance_Review.md` §6: shared, deterministic tooling prevents independently-implemented logic from "silently drift[ing] into slightly-different implementations" of the same operation.
**Relationships:** The mechanical counterpart to P5 — together they define one boundary from opposite sides.
**ADR:** None named directly; underlies the Chat/Code division captured in `ADR-0002` (see P5).

### P5. Judgment Is Never Automated — `judgment-not-automated`
**Statement:** Tools validate and apply decisions already made; they do not make engineering, regulatory, or correctness judgments themselves.
**Rationale:** `IMPLEMENTATION_CONTRACT.md` §7 binds this on Claude Code specifically: it "never decides whether a regulatory claim is correct" and "never decides whether a correction should be applied at all." §6 reserves judgment exclusively for Chat.
**Relationships:** Paired with P4. Defines the Chat/Code responsibility boundary set out in `IMPLEMENTATION_CONTRACT.md` §6–7.
**ADR:** Reserved — `ADR-0002` (Claude Chat vs. Claude Code division of responsibility), named in `MIW_Bootstrap_Governance_Review.md` §2. Not yet drafted.

### P6. Verify Before Trust — `verify-before-trust`
**Statement:** No correction is applied to any content until it has been verified against a primary source. External AI-generated review or suggestions are never applied on trust alone.
**Rationale:** `IMPLEMENTATION_CONTRACT.md` §6 assigns this to Chat as a standing responsibility: "Verification of external corrections (Gemini/Perplexity or any other source) against primary sources before acceptance."
**Relationships:** Supports P5 — verifying against a primary source is itself a judgment task, which is why it cannot be delegated to a tool.
**ADR:** Reserved — `ADR-0004` (correction philosophy: verify-before-apply, never trust external AI review blindly, dry-run-first mutation), named in `MIW_Bootstrap_Governance_Review.md` §2. Shared with P7. Not yet drafted.

### P7. Reversible Mutation — `reversible-mutation`
**Statement:** Any operation that changes committed content is opt-in and reversible by default. Dry-run is the default mode; mutation requires an explicit, separate action to apply.
**Rationale:** `IMPLEMENTATION_CONTRACT.md` §4 extends this into commit discipline directly: mutation-tier work and anything touching `corrections/` or `known_traps.md` requires granular history and is never squashed, because "what changed and why, step by step" has diagnostic value precisely because mutation carries real risk.
**Relationships:** Shares `ADR-0004` with P6. Supports P8 — reversibility and small units of change are complementary risk-containment strategies.
**ADR:** Reserved — `ADR-0004` (shared with P6). Not yet drafted.

### P8. Small, Reviewable Units — `small-reviewable-units`
**Statement:** Work is delivered as many small, independently reviewable changes rather than large, unreviewable ones.
**Rationale:** `IMPLEMENTATION_CONTRACT.md` §1 items 1–2 make this binding, not aspirational: "Every package is small enough to review in one sitting. Every commit is small enough to understand at a glance." §4 operationalizes it: "One commit per logically complete unit of work."
**Relationships:** Supports P7 (reversible mutation) and P2 (documentation is authoritative) — small units are both easier to revert and safer to commit incrementally, without waiting for a larger batch to feel "finished."
**ADR:** None reserved — enforced directly through `IMPLEMENTATION_CONTRACT.md` rather than deferred to a future ADR.

### P9. No Speculative Structure — `no-speculative-structure`
**Statement:** New documents, directories, tools, or skills are created only when a real, demonstrated need exists — never in anticipation of a need that has not yet materialized.
**Rationale:** The most independently reinforced principle in the surviving evidence base. `MIW_Architecture_Freeze_Review.md`'s entire rejection of the `engineering/` wrapper proposal rests on it: "build structure when a demonstrated need exists, not speculatively... Cheap migration doesn't make a worse architecture worth adopting." Per `ENGINEERING_PRINCIPLES_AUTHORING_FRAMEWORK.md` §8, this same rule now governs governance itself: future governance changes are to be "driven only by implementation needs."
**Relationships:** Governs P3 from the existence side, not the scope side. Directly cited by this document's own Amendment Policy, below.
**ADR:** None named directly — enforced through `IMPLEMENTATION_CONTRACT.md` §11 (Repository Freeze Policy) rather than its own dedicated ADR.

### P10. Code Executes Written Specs — `code-executes-specs`
**Statement:** Claude Code executes against already-written, committed specifications. It does not rediscover conventions by reading conversation history or inferring past practice.
**Rationale:** `IMPLEMENTATION_CONTRACT.md` §7 states this directly and lists what Claude Code never does, including creating new structure without an approved, written plan behind it.
**Relationships:** The direct consequence of P1 and P2 applied specifically to the Chat/Code boundary defined under P5.
**ADR:** Reserved — shares `ADR-0002` with P5.

---

## Relationships (Document-Level Summary)

- **P1 and P2** are foundational — every other principle depends on the repository being trusted (P1) and decisions being written down to be trusted (P2).
- **P4 and P5** define a single boundary — mechanical work to tools, judgment to Chat — from opposite sides.
- **P6 and P7** are the correction/mutation safety pair, sharing `ADR-0004`.
- **P8** governs delivery granularity and supports both P7 (smaller changes are easier to revert) and P2 (smaller changes are safer to commit early).
- **P9** governs when new structure is warranted at all, and constrains this document's own future growth (see Amendment Policy).
- **P3 and P10** both tie back to P1/P2 — P3 to how the repository stays trustworthy at the document/tool level, P10 to how Claude Code stays trustworthy at the execution level.

This section is new synthesis for Draft 1. The original document is known to have contained a "Relationships" section (per `ENGINEERING_PRINCIPLES_AUTHORING_FRAMEWORK.md` §3, citing the historical record), but its actual content was not recoverable — this section does not attempt to reproduce it, only to state the relationships evidenced by the ten principles actually drafted here.

---

## Reserved for ADR

Per `MIW_Bootstrap_Governance_Review.md` §2, five Architecture Decision Records were scoped but never drafted. Each is referenced above by the principle(s) it underlies. None exist as files yet.

| ADR | Topic | Referenced by |
|---|---|---|
| `ADR-0001` | Repository-first philosophy | P1 |
| `ADR-0002` | Claude Chat vs. Claude Code division of responsibility | P5, P10 |
| `ADR-0003` | Documentation hierarchy (docs/skills/tools) | P3 |
| `ADR-0004` | Correction philosophy (verify-before-apply, dry-run-first mutation) | P6, P7 |
| `ADR-0005` | Git/push authority model | Not yet linked to a principle above — `Bootstrap_Architecture_Amendment_LocalFirst.md` bears directly on this topic but is itself still unapproved ("Proposed amendment, pending Founder approval"); no principle here asserts a specific push mechanism until that is resolved |

This document deliberately does not restate ADR-level reasoning inline — per P3, that would duplicate content the ADRs themselves are meant to own.

---

## Amendment Policy

Per `ENGINEERING_PRINCIPLES_AUTHORING_FRAMEWORK.md` §8: **"Bootstrap governance is now frozen. Future governance changes shall be driven only by implementation needs."**

A principle in this document is amended only when a specific, real implementation package demonstrates the need — never speculatively, never as part of a general cleanup or improvement pass. This is P9 applied to the document itself. Amendment follows the standard package lifecycle (`IMPLEMENTATION_CONTRACT.md` §2): drafted in Chat, validated, reviewed by the Founder, committed — never bypassed for convenience (`IMPLEMENTATION_CONTRACT.md` §1 item 6).

---

## Known Incompleteness (Draft 1)

This draft contains **10 principles**, sourced from the one surviving seed list (`MIW_Bootstrap_Governance_Review.md` §1). Per `reports/reviews/ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` §6, the lost original is reported to have contained 14 principles, including at least three named concepts with no surviving definition anywhere (`Explicit Relationships`, `Traceability`, `Reproducibility`). This draft does not invent content to reach 14. Whether additional principles are needed is a question for Founder review, to be answered with fresh input, not inference.
