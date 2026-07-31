# Engineering Principles

**Status:** Draft (v0.2) — pending Founder review. **Not promoted to Approved this pass — see "Why This Remains Draft" below.**
**Governs:** All packages, all documents, all tools produced under this repository's engineering bootstrap and beyond
**Date:** 2026-07-31
**Replaces:** The original Engineering Principles document, confirmed unrecoverable (see `reports/reviews/ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md`). This is a new document, authored from surviving repository evidence only — not a reconstruction of the original.
**Revision history:** v0.1 (10 principles) received independent critical review (`ENGINEERING_PRINCIPLES_REVIEW.md`). v0.2 (this version) addresses every accepted finding: two overlapping pairs merged, two Contract-duplicative principles converted to references, one identified gap closed, one new ADR reserved. Net: 7 principles.

---

## Purpose

This document is the single compliance reference every package's output is checked against. It is not a philosophy essay to be read once — `IMPLEMENTATION_CONTRACT.md` §9 makes it operational: the Governance Gate checks every package's output against this document and the ADR set on every single package, and §3's Definition of Done already names "the single-responsibility principle from `ENGINEERING_PRINCIPLES.md`" as a live compliance check. Write for a reader — human or AI — with no access to the conversation that produced this document.

---

## Principles

### P1. Repository First — `repository-first`
**Statement:** The repository is the source of truth; conversations, chat history, and session memory are disposable and carry no authority once a session ends. If a decision is not written down in the repository, it is not decided — regardless of what was discussed or agreed elsewhere. A document in Draft status is written down and citable, but not yet binding; binding status requires the document's own Status line to read Approved.
**Rationale:** `MIW_Bootstrap_Governance_Review.md` §1 states both halves of this as separate proposed principles: "The repository is the source of truth; conversations are disposable" and "Documentation is authoritative — if it's not written down, it doesn't count as decided." `IMPLEMENTATION_CONTRACT.md` §1 item 8 restates the combined rule as binding: "The repository, not the conversation, is what future sessions will trust."
**Merge note (v0.2):** Combines v0.1's P1 (Repository First) and P2 (Documentation Is Authoritative), per `ENGINEERING_PRINCIPLES_REVIEW.md` Overlap Analysis — the two were evidenced as the same idea at two granularities (the repository as a whole vs. its documentation specifically) rather than independently load-bearing. Also resolves the review's flagged Draft-status ambiguity directly, in the third sentence above.
**Relationships:** Foundational — P6 (formerly P10) applies this principle directly to Claude Code's execution model; P7 (Repository Independence, new) extends it from "the repo is truth" to "the repo must be comprehensible truth."
**ADR:** Reserved — `ADR-0001` (repository-first philosophy), named in `MIW_Bootstrap_Governance_Review.md` §2. Not yet drafted.

### P2. Single Responsibility — `single-responsibility`
**Statement:** Each document and each tool owns exactly one responsibility. Content is not duplicated across documents; behavior is not duplicated across tools. This principle itself intentionally governs two artifact types (documents and tools) under one entry — the same underlying rule applied twice, not two different rules.
**Rationale:** `IMPLEMENTATION_CONTRACT.md` §3 already checks every package's output against this principle by name. `MIW_Architecture_Freeze_Review.md`'s comparison table (criterion 9) cites the same rule as already-decided when rejecting the `engineering/` wrapper proposal.
**Relationships:** Governs P5 (No Speculative Structure) from the artifact-scope side — this principle constrains what an artifact covers once it exists; P5 constrains whether it should exist at all. Directly justifies converting v0.1's P7/P8 into references rather than standalone principles (see "Reserved for the Implementation Contract," below) — restating Contract-owned rules here would itself violate this principle.
**ADR:** Reserved — `ADR-0003` (documentation hierarchy: docs = what/why, skills = how/when, tools = mechanical execution), named in `MIW_Bootstrap_Governance_Review.md` §2. Not yet drafted.

### P3. Mechanical vs. Judgment Boundary — `mechanical-vs-judgment`
**Statement:** Wherever a task is mechanical and its outcome is fully determined by explicit rules, it is performed by a deterministic tool, not by repeated AI reasoning. Conversely, engineering, regulatory, and correctness judgment is never automated — tools validate and apply decisions already made, they do not decide.
**Rationale:** `MIW_Bootstrap_Governance_Review.md` §1 proposed both halves as separate principles ("Deterministic tooling is preferred..." and "Engineering judgement is never automated..."); §6 gives the concrete cost of getting this wrong — independently-implemented logic "silently drift[ing] into slightly-different implementations" of the same operation. `IMPLEMENTATION_CONTRACT.md` §7 binds the judgment half specifically on Claude Code: it "never decides whether a regulatory claim is correct" and "never decides whether a correction should be applied at all." §6 reserves judgment exclusively for Chat.
**Merge note (v0.2):** Combines v0.1's P4 (Deterministic Tooling) and P5 (Judgment Is Never Automated), per `ENGINEERING_PRINCIPLES_REVIEW.md` — v0.1's own Relationships field already described them as "one boundary from opposite sides" without merging them; this version acts on that finding.
**Relationships:** Defines the Chat/Code responsibility boundary set out in `IMPLEMENTATION_CONTRACT.md` §6–7. Distinct from P6 (Code Executes Written Specs): this principle governs *who decides* (tool vs. Chat judgment); P6 governs *where Code's instructions come from* (written spec vs. inferred history) — a different axis, not a restatement.
**ADR:** Reserved — `ADR-0002` (Claude Chat vs. Claude Code division of responsibility), named in `MIW_Bootstrap_Governance_Review.md` §2. Not yet drafted.

### P4. Verify Before Trust — `verify-before-trust`
**Statement:** No correction is applied to any content until it has been verified against a primary source. External AI-generated review or suggestions are never applied on trust alone.
**Rationale:** `IMPLEMENTATION_CONTRACT.md` §6 assigns this to Chat as a standing responsibility: "Verification of external corrections (Gemini/Perplexity or any other source) against primary sources before acceptance."
**Relationships:** Supports P3 — verifying against a primary source is itself a judgment task, which is why it cannot be delegated to a tool. Connects to the mutation-safety topic now referenced under "Reserved for the Implementation Contract," below, since both share `ADR-0004`.
**ADR:** Reserved — `ADR-0004` (correction philosophy: verify-before-apply, never trust external AI review blindly, dry-run-first mutation), named in `MIW_Bootstrap_Governance_Review.md` §2. Not yet drafted.

### P5. No Speculative Structure — `no-speculative-structure`
**Statement:** New documents, directories, tools, or skills are created only when a real, demonstrated need exists — never in anticipation of a need that has not yet materialized. A need is demonstrated when a specific, currently-in-progress package requires it — not a hypothetical future package, and not administrative tidiness.
**Rationale:** The most independently reinforced principle in the surviving evidence base. `MIW_Architecture_Freeze_Review.md`'s entire rejection of the `engineering/` wrapper proposal rests on it: "build structure when a demonstrated need exists, not speculatively... Cheap migration doesn't make a worse architecture worth adopting." Per `ENGINEERING_PRINCIPLES_AUTHORING_FRAMEWORK.md` §8, this same rule now governs governance itself: future governance changes are to be "driven only by implementation needs."
**Revision note (v0.2):** Second sentence (the operational test) added per `ENGINEERING_PRINCIPLES_REVIEW.md`'s finding that the original statement gave no concrete test for "demonstrated need," risking future dispute.
**Relationships:** Governs P2 from the existence side, not the scope side. Directly cited by this document's own Amendment Policy, below.
**ADR:** Reserved — `ADR-0006` (no speculative structure / demonstrated-need discipline). **New in v0.2**, not among the original five ADR topics named in `MIW_Bootstrap_Governance_Review.md` §2. Per `ENGINEERING_PRINCIPLES_REVIEW.md`: this principle carries outsized influence (drives this document's own Amendment Policy, independently reinforced across three sources) without any reserved ADR, and meets the Governance Review §2's own stated ADR bar — "(a) non-obvious, (b) reversing it later would be expensive, (c) someone will eventually ask why." Reserving a sixth ADR topic is itself a structural decision the Founder should confirm; not yet drafted.

### P6. Code Executes Written Specs — `code-executes-specs`
**Statement:** Claude Code executes against already-written, committed specifications. It does not rediscover conventions by reading conversation history or inferring past practice.
**Rationale:** `IMPLEMENTATION_CONTRACT.md` §7 states this directly and lists what Claude Code never does, including creating new structure without an approved, written plan behind it.
**Relationships:** The direct consequence of P1 applied specifically to the Chat/Code boundary defined under P3. See P3's Relationships field for the explicit distinction between the two.
**ADR:** Reserved — shares `ADR-0002` with P3.

### P7. Repository Independence — `repository-independence`
**Statement:** The repository must remain useful and understandable without Claude in the loop. A human reading `docs/` (and `meoclass1/known_traps.md`, where applicable) must be able to understand the system with zero AI assistance.
**Rationale:** `MIW_Bootstrap_Governance_Review.md` §8: "Offline-first as a discipline, not just a feature... MIW's equivalent... is 'the repository must remain useful without Claude in the loop.' A human (Nixon, or a future collaborator) should be able to read `docs/` and `known_traps.md` and understand the system with zero AI assistance." That same section explicitly flagged this as "a good acceptance test to fold into the Founder Checklist" — `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` §6 (Missing Areas) confirmed it was never actually operationalized anywhere in the surviving corpus. This is a new principle in v0.2, addressing that specific, previously-identified gap.
**Relationships:** Extends P1 — not just "the repository is truth," but "the repository's truth must be comprehensible without AI assistance." A stronger bar than P1 alone requires.
**ADR:** None reserved — this is stated as a direct acceptance test, not a structural decision requiring case-by-case justification.

---

## Reserved for the Implementation Contract

Two ideas evidenced in `MIW_Bootstrap_Governance_Review.md` §1 as proposed principles — "mutation is opt-in and reversible by default (dry-run first)" and "prefer many small, reviewable changes over large, unreviewable ones" — are **not** restated here as standalone principles in v0.2. On review (`ENGINEERING_PRINCIPLES_REVIEW.md`), both are already fully stated and enforced directly by `IMPLEMENTATION_CONTRACT.md`:

- **Delivery granularity** — one commit per logically complete unit of work, every package small enough to review in one sitting: `IMPLEMENTATION_CONTRACT.md` §1 items 1–2, §4.
- **Reversible mutation** — dry-run as the default mode, mutation requiring an explicit separate action, granular non-squashed history for mutation-tier and `corrections/`/`known_traps.md` work: `IMPLEMENTATION_CONTRACT.md` §4. Also connects to `ADR-0004` (see P4).

Restating fully-Contract-owned rules here as independent principles would itself violate P2 (single responsibility, no cross-document duplication). This section exists so the underlying ideas remain traceable from this document without re-stating them.

---

## Relationships (Document-Level Summary)

- **P1** is foundational — every other principle depends on the repository being trusted and its record being complete.
- **P3** defines a single boundary — mechanical work to tools, judgment to Chat — stated once, from both directions.
- **P4** is the correction-safety application of P3's judgment half, and connects to the mutation-safety topic now homed in "Reserved for the Implementation Contract."
- **P5** governs when new structure is warranted at all, constrains this document's own future growth (see Amendment Policy), and now carries its own reserved ADR given its outsized influence.
- **P2 and P6** both tie back to P1 — P2 to how the repository stays trustworthy at the document/tool level, P6 to how Claude Code stays trustworthy at the execution level, distinguished explicitly from P3 in P3's own entry.
- **P7** extends P1 with a comprehensibility bar beyond mere existence.

This section was originally new synthesis for Draft 1 and has been updated for v0.2's renumbering and merges. The original lost document is known to have contained a "Relationships" section (per `ENGINEERING_PRINCIPLES_AUTHORING_FRAMEWORK.md` §3, citing the historical record), but its actual content was never recoverable — this section does not attempt to reproduce it, only to state the relationships evidenced by the seven principles actually drafted here.

---

## Reserved for ADR

Six Architecture Decision Records are now reserved (five named in `MIW_Bootstrap_Governance_Review.md` §2, one added in v0.2 — see P5). None exist as files yet.

| ADR | Topic | Referenced by |
|---|---|---|
| `ADR-0001` | Repository-first philosophy | P1 |
| `ADR-0002` | Claude Chat vs. Claude Code division of responsibility | P3, P6 |
| `ADR-0003` | Documentation hierarchy (docs/skills/tools) | P2 |
| `ADR-0004` | Correction philosophy (verify-before-apply, dry-run-first mutation) | P4, and the mutation-safety topic under "Reserved for the Implementation Contract" |
| `ADR-0005` | Git/push authority model | Not yet linked to a principle — `Bootstrap_Architecture_Amendment_LocalFirst.md` bears directly on this topic but is itself still unapproved ("Proposed amendment, pending Founder approval"); no principle here asserts a specific push mechanism until that is resolved |
| `ADR-0006` | No speculative structure / demonstrated-need discipline | P5. **New in v0.2** — Founder confirmation of this as a valid sixth ADR topic is recommended, not assumed. |

This document deliberately does not restate ADR-level reasoning inline — per P2, that would duplicate content the ADRs themselves are meant to own.

---

## Amendment Policy

Per `ENGINEERING_PRINCIPLES_AUTHORING_FRAMEWORK.md` §8: **"Bootstrap governance is now frozen. Future governance changes shall be driven only by implementation needs."**

A principle in this document is amended only when a specific, real implementation package demonstrates the need — never speculatively, never as part of a general cleanup or improvement pass. This is P5 applied to the document itself. Amendment follows the standard package lifecycle (`IMPLEMENTATION_CONTRACT.md` §2): drafted in Chat, validated, reviewed by the Founder, committed — never bypassed for convenience (`IMPLEMENTATION_CONTRACT.md` §1 item 6).

---

## Why This Remains Draft

This version addresses every finding in `ENGINEERING_PRINCIPLES_REVIEW.md` and is not known to contain any unsupported claim, invalid citation, or unresolved duplication. It is **not** being promoted to Approved in this pass, for three specific reasons rather than general caution:

1. **P7 (Repository Independence) is genuinely new content**, introduced in this revision, that has never been shown to the Founder in any form before this document. Every other principle has now been through one review cycle; this one has been through zero.
2. **All six reserved ADRs remain undrafted.** The Governance Gate (`IMPLEMENTATION_CONTRACT.md` §9) checks compliance against "`ENGINEERING_PRINCIPLES.md` and relevant ADRs" as a pair — the ADR half of that pair does not exist yet in any form.
3. **Only one review pass has occurred**, conducted within the same working context that authored the original draft. It was run adversarially and in good faith, but it is not the same as independent Founder sign-off on this specific version's actual diff, which `IMPLEMENTATION_CONTRACT.md` §2 (Founder Review stage) treats as a distinct, required step — not something a passed self-review substitutes for.

None of these block the document from being useful now — it is committed, citable, and already the most complete Engineering Principles artifact this repository has ever had. They are reasons to withhold the specific "Approved" status, not reasons to withhold the content.

---

## Known Incompleteness

This version contains **7 principles** — down from v0.1's 10 (two merges, two conversions to Contract references, one addition), sourced entirely from the surviving seed list in `MIW_Bootstrap_Governance_Review.md` §1 plus the one previously-identified gap closed in P7. Per `reports/reviews/ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` §6, the lost original is reported to have contained 14 principles, including at least three named concepts with no surviving definition anywhere (`Explicit Relationships`, `Traceability`, `Reproducibility`). This document does not invent content to reach 14, and per P5, does not treat "closer to the historical count" as itself a reason to grow. Whether additional principles are needed remains a question for future Founder review, answered only when a real implementation need surfaces one — not by inference now.
