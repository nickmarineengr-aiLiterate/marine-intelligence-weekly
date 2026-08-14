# Engineering Principles — Authoring Framework

**Package:** PKG-1.5R — Engineering Principles Redevelopment (Framework Stage)
**Purpose:** Define *how* `docs/ENGINEERING_PRINCIPLES.md` will be authored. Contains no principle content.
**Status:** Framework proposal. No principles drafted. No repository file modified. Not committed.
**Date:** 2026-07-31
**Evidence base:** `reports/reviews/ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` and the three approved governance documents (`MIW_Bootstrap_Governance_Review.md`, `MIW_Architecture_Freeze_Review.md`, `IMPLEMENTATION_CONTRACT.md`)

---

## 0. Provenance Convention Used Throughout

Every element below is tagged:
- **[EVIDENCED]** — directly stated or strongly implied by a surviving source, with citation.
- **[RECOMMENDED]** — this framework's own proposal, not found in any surviving source, offered because the task requires a complete authoring framework and the evidence base doesn't specify every operational detail.

This distinction matters because the entire reason PKG-1.5R exists is that the original document was lost and must not be silently reconstructed by inference (per Founder instruction, this package and PKG-1.5R's opening). Keeping "what we know" visibly separate from "what this framework proposes" is the same discipline applied here.

---

## 1. Document Purpose

**[EVIDENCED]** `MIW_Bootstrap_Governance_Review.md` §1: *"Right now the philosophy is scattered across the original bootstrap brief, your userPreferences, and my blueprint's prose. That's exactly the 'trapped in conversation' problem this whole project exists to fix. If the philosophy itself isn't written down as a single artifact, everything downstream (docs, skills, tools) is built on an assumption, not a reference."*

**[EVIDENCED]** `IMPLEMENTATION_CONTRACT.md` §9 (Quality Gates) makes this operational, not just aspirational: the **Governance Gate** checks "Does this package's output comply with `ENGINEERING_PRINCIPLES.md` and relevant ADRs?" on *every* package, forever. §3 (Definition of Done) already names "the single-responsibility principle from `ENGINEERING_PRINCIPLES.md`" as something every package's output is checked against — a live forward reference from an already-approved document.

**Purpose statement for the framework:** `ENGINEERING_PRINCIPLES.md` is not a philosophy essay. It is the single compliance reference every future package's output is checked against, replacing scattered, undocumented assumptions with one citable artifact. Its purpose is to be *checked against*, not merely *read once*.

---

## 2. Intended Audience

**[EVIDENCED]** Two distinct audiences are named across the surviving sources, with different needs:

- **Humans, without AI assistance.** `MIW_Bootstrap_Governance_Review.md` §8: *"the repository must remain useful without Claude in the loop... A human (Nixon, or a future collaborator) should be able to read `docs/` and `known_traps.md` and understand the system with zero AI assistance."*
- **Future AI sessions, without conversation history.** `IMPLEMENTATION_CONTRACT.md` §1, item 8: *"The repository, not the conversation, is what future sessions will trust."* `MIW_Bootstrap_Blueprint.md` §2: Claude Code "executes against `docs/*.md` and `skills/*` as its spec — does not need conversation history to know 'how MIW does things.'"

**[RECOMMENDED]** Design consequence for authoring: every principle must be understandable in isolation, without requiring the reader to have followed the bootstrap conversation, the source analysis, or this framework. Write for a reader — human or AI — encountering the document cold, matching the same standard `AI_SESSION_HANDOVER.md` §6 already applies to itself ("For a new engineer with no conversation history...").

---

## 3. Document Organization

**[EVIDENCED]** Two constraints from surviving sources, currently in tension and both binding:

1. **Format constraint** (`MIW_Bootstrap_Governance_Review.md` §1): *"it needs to be short... Target: 8–12 principles, one line each, no elaboration in the same file... A philosophy document that fits on one screen gets re-read every session."*
2. **Structural constraint** (`AI_SESSION_HANDOVER.md` §4, describing the lost draft): *"Content fully drafted (14 principles, **Purpose, Relationships, Reserved-for-ADR sections**)."*

These aren't actually contradictory — "one line each, no elaboration" describes the *principles themselves*; the three named sections (Purpose, Relationships, Reserved-for-ADR) are framing and cross-reference material around the list, not elaboration of individual principles. A one-screen principles list can still sit inside a slightly longer document that also explains what the list is for and how it connects to ADRs.

**Organization for the framework:**
1. Header/metadata block **[RECOMMENDED — pattern-matched from every sibling governance document]**
2. Purpose section **[EVIDENCED — named explicitly]**
3. The principles list itself — numbered, one line each, no elaboration **[EVIDENCED — explicit format spec]**
4. Relationships section **[EVIDENCED — named explicitly, content unspecified — see §6 caveat below]**
5. Reserved-for-ADR section **[EVIDENCED — named explicitly]**
6. Amendment/Change Policy **[RECOMMENDED — see §8]**

---

## 4. Numbering System

**[EVIDENCED]** No surviving source specifies a formal ID scheme for principles. The only precedent in the surviving corpus is `MIW_Bootstrap_Governance_Review.md` §1's 10-item list, informally numbered 1–10 in prose order, no stable identifiers.

**[EVIDENCED]** The repository's ADR convention is the closest existing pattern: `MIW_Bootstrap_Governance_Review.md` §2 specifies ADRs are "Store[d] as `docs/adr/0001-repository-first.md` etc." — a stable number *and* a descriptive slug, in the filename itself.

**[RECOMMENDED]** Adopt the same two-part convention for principles: a sequential display number (P1, P2, ...) for reading order, plus a short, stable kebab-case name (e.g., `single-responsibility`) for citation. Rationale: `IMPLEMENTATION_CONTRACT.md` §3 already cites "the single-responsibility principle from `ENGINEERING_PRINCIPLES.md`" *by name*, not by number — a numbering-only scheme would leave that citation fragile against future reordering. A stable name survives reordering; a number alone does not.

Example format: `**P3 — single-responsibility:** One responsibility per document, one responsibility per tool.`

---

## 5. Required Sections

| # | Section | Provenance | Content |
|---|---|---|---|
| 1 | Header/metadata | [RECOMMENDED] | Status, Governs/Scope, Date — matching `MIW_Bootstrap_Blueprint.md`, `MIW_Bootstrap_Governance_Review.md`, `MIW_Architecture_Freeze_Review.md`, `IMPLEMENTATION_CONTRACT.md`, all of which open with this exact pattern |
| 2 | Purpose | [EVIDENCED] | Short — why this document exists, who it binds (see §1 above) |
| 3 | Principles List | [EVIDENCED] | Numbered, one line each, no elaboration in-file (§3, §4 above) |
| 4 | Relationships | [EVIDENCED, content unspecified] | How principles relate to *each other* and/or to ADRs and the Contract — see §6 caveat, this is the least-recoverable structural element |
| 5 | Reserved for ADR | [EVIDENCED] | Named pointers to the five ADR topics (`MIW_Bootstrap_Governance_Review.md` §2) — topics too weighty for a one-liner, deliberately not restated here to avoid duplication (Theme H, single-responsibility) |
| 6 | Amendment/Change Policy | [RECOMMENDED] | How and when this document may be amended — see §8 |

**Explicitly not a required section, by design:** elaboration/rationale per principle. That belongs in the corresponding ADR when one exists (§6), or nowhere, if the principle is genuinely self-explanatory. Duplicating rationale here would itself violate the single-responsibility principle this document is meant to state.

---

## 6. Relationship to ADRs

**[EVIDENCED]** `MIW_Bootstrap_Governance_Review.md` §2 draws the line explicitly: ADRs are for decisions that are "(a) non-obvious, (b) reversing it later would be expensive, and (c) someone will eventually ask 'why did we do it this way?'" — five such decisions are already named and scoped (repository-first philosophy, Chat/Code division, documentation hierarchy, correction philosophy, git/push authority), none yet drafted as files. Principles are the short, memorable "what" statements; ADRs are the "why," told once, in depth, per weighty decision — not duplicated in the principles list.

The lost draft's "Reserved-for-ADR" section is direct evidence this handoff mechanism was real and deliberate: rather than compressing a weighty decision into an inadequate one-liner, or expanding a one-liner into unwanted elaboration, the draft apparently pointed at the relevant ADR instead.

**[RECOMMENDED]** Authoring guidance: when drafting begins, for each of the five ADR topics, decide whether it also needs a *short* companion principle statement (in the numbered list) or purely a Reserved-for-ADR pointer (no numbered principle at all, just a named forward reference). This decision should be made per-topic, not as a blanket rule — the surviving evidence doesn't specify which of the five got which treatment in the lost draft, and this framework does not guess.

---

## 7. Relationship to the Implementation Contract

**[EVIDENCED]** The relationship is already load-bearing, not merely descriptive:

- `IMPLEMENTATION_CONTRACT.md` §3 (Definition of Done) cites "the single-responsibility principle from `ENGINEERING_PRINCIPLES.md`" as a literal compliance check on every package.
- `IMPLEMENTATION_CONTRACT.md` §9 (Quality Gates) makes the **Governance Gate** — compliance with `ENGINEERING_PRINCIPLES.md` and ADRs — one of six gates every package must pass before its successor may begin.
- `IMPLEMENTATION_CONTRACT.md` §6 groups drafting/revising `ENGINEERING_PRINCIPLES.md` together with ADRs and `CORRECTION_WORKFLOW.md` as things that "even after Claude Code exists, these are Chat-authored and Chat-revised" — Code never authors or edits this document.
- `MIW_Architecture_Freeze_Review.md` §4/§6 treats `docs/adr/` + `ENGINEERING_PRINCIPLES.md` together as "a single [governance] home" — companion artifacts, not independent ones.

**Division of labor:** the Contract governs *process* — how a package moves through its lifecycle. Principles governs *values* — what "good" looks like at each Contract stage that requires judgment (e.g., the Validation stage's review-for-duplication check has no meaning without a single-responsibility principle to check against). Neither document can enforce anything alone; the Contract's gates are the enforcement mechanism, Principles is what gets enforced.

---

## 8. Relationship to Future Governance

**[EVIDENCED]** `IMPLEMENTATION_CONTRACT.md` §11 (Repository Freeze Policy): governance is frozen; implementation may improve within approved boundaries but "any of the above requires a new ADR proposal... not a mid-implementation adjustment." Once committed, `ENGINEERING_PRINCIPLES.md` becomes part of that frozen baseline — changeable, but not casually.

**[EVIDENCED, this session]** The Founder's own declaration opening this package: *"Bootstrap governance is now frozen. Future governance changes shall be driven only by implementation needs."* This is the binding amendment rule going forward, stated directly rather than inferred, and it is fully consistent with the single most-reinforced idea across the entire surviving evidence base — `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` Theme G, "no speculative structure," documented 7 separate times across three sources.

**[RECOMMENDED]** §5's Amendment/Change Policy section should state this rule explicitly, in the document itself, rather than leaving it only in the Contract and this Founder instruction: *a principle is amended only when a specific, real implementation package demonstrates the need — never speculatively, never as part of a general "cleanup" or "improvement" pass.*

---

## 9. Review and Approval Workflow

**[EVIDENCED]** `IMPLEMENTATION_CONTRACT.md` §2 defines the general eight-stage package lifecycle (Planning → Implementation → Validation → Founder Review → [Revision loop] → Commit → Verification → Report), binding on every package including this one. §1, item 6: "Governance is never bypassed for convenience, schedule, or Claude's own judgement of what's 'obviously fine.'" §6: only Chat drafts/revises principles, never Code.

**[EVIDENCED, direct precedent from this repository's own history]** The original 14-principle draft was, per `AI_SESSION_HANDOVER.md` §4, "fully drafted" and reportedly reached Founder-level discussion — yet it was never committed, and is now confirmed unrecoverable (per this package's background). This is not a hypothetical failure mode; it already happened once, to this exact document.

**[RECOMMENDED]** The redraft's review workflow should follow the Contract's standard lifecycle, with one addition directly targeted at the failure that produced PKG-1.5R in the first place:

1. **Planning** — confirm this framework (the current document) against Founder review before any principle is drafted.
2. **Implementation (drafting)** — Chat drafts the principles list plus Purpose/Relationships/Reserved-for-ADR sections, working only from evidence already gathered (`ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md`) plus fresh Founder input where the evidence has gaps (the untraceable principle names flagged in that document's §6).
3. **Validation** — cross-check every principle against the Contract's existing forward references (e.g., confirm a `single-responsibility`-named principle exists, since §3 of the Contract already depends on one existing) and against the Source Analysis's duplicated-ideas/overlap findings, so known near-overlaps are resolved deliberately, not accidentally re-created.
4. **Founder Review** — as normal.
5. **Commit — promptly, even in an explicitly marked draft state if full sign-off takes more than one session.** This is the one workflow change this framework recommends beyond the Contract's default: the lost draft's failure mode was specifically "approved-in-conversation, never committed." A `docs/ENGINEERING_PRINCIPLES.md` carrying a `**Status:** Draft — pending final Founder sign-off` header is recoverable if a session ends unexpectedly; a document that exists only in chat output is not. This does not weaken Founder Review — final sign-off still gates the Status line changing to `Approved` — it only ensures the *content* survives regardless of when sign-off completes.
6. **Verification / Report** — as normal, per the Contract.

---

## 10. What This Framework Deliberately Does Not Do

- Does not draft, number, name, or word any principle.
- Does not decide the final principle count (the lost draft had 14; the surviving seed has 10; this framework takes no position on the eventual number).
- Does not resolve the untraceable principle names (`Explicit Relationships`, `Traceability`, `Reproducibility`) flagged in `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` §6 — those require fresh Founder input during actual drafting, not inference here.
- Does not decide the Relationships section's actual content — its existence is evidenced, its content is not, and this framework does not guess at it.

---

## 11. Closing Note

This framework defines how `docs/ENGINEERING_PRINCIPLES.md` will be authored, not what it will say. No principle was drafted. No repository file was modified. Nothing was committed. Submitted for Founder review.
