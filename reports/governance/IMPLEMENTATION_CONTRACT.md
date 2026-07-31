# IMPLEMENTATION_CONTRACT.md
**Status:** Approved (Founder decision, 2026-07-31)
**Governs:** Execution of PKG-1 through PKG-13 (MIW Repository Engineering Bootstrap)
**Does not describe:** Repository structure or architecture (see `docs/ARCHITECTURE.md` once created) or governance rationale (see governance review). This document defines **how** work is executed, not **what** exists.

---

## 1. Project Execution Philosophy

These are binding, not aspirational:

1. Every package is small enough to review in one sitting.
2. Every commit is small enough to understand at a glance.
3. Every package leaves the repository in a working state — no package may depend on a future package to not be broken.
4. Nothing is implemented before it is reviewed as a plan.
5. Nothing is committed before it is validated.
6. Governance is never bypassed for convenience, schedule, or Claude's own judgement of what's "obviously fine."
7. Silence is not consent. Ambiguity is resolved by asking, not assuming.
8. The repository, not the conversation, is what future sessions will trust. Every package must leave the repository able to explain itself without this conversation.

---

## 2. Package Execution Lifecycle

Every package — no exceptions — follows the same eight-stage lifecycle.

```
   Planning
      │
      ▼
 Implementation
      │
      ▼
  Validation
      │
      ▼
 Founder Review
      │
      ▼
  ┌───┴────┐
  │Revision │──── (loops back to Validation if changes made)
  │required?│
  └───┬────┘
      │ no
      ▼
   Commit
      │
      ▼
 Verification
      │
      ▼
   Report
      │
      ▼
 Next Package
```

**Stage definitions:**

- **Planning** — Restate the package's Purpose/Scope/Deliverables from the approved roadmap. Flag anything discovered since the roadmap was written that changes scope. No file is touched yet.
- **Implementation** — Build exactly what Planning specified. Nothing extra. Discoveries outside scope are logged as candidate future packages (Section 10), not absorbed silently.
- **Validation** — Run every relevant validation tool available at that point in the bootstrap (Section 5). Before `tools/validate_html.py`/`validate_json.py` exist (early packages), validation means manual review against the package's own checklist.
- **Founder Review** — Nixon reviews the actual diff/output, not a summary of it. Approval, rejection, or revision request.
- **Revision (if required)** — Address feedback, return to Validation. This loop has no iteration limit — it runs until Founder Review passes.
- **Commit** — Per the commit policy in Section 4. Only after Founder Review passes.
- **Verification** — Confirm the committed state matches what was reviewed (cache-busted fetch, `git log`/`git diff` check, or equivalent). Catches any last-mile drift between what was approved and what actually landed.
- **Report** — One short note: what shipped, what deviated from plan (if anything), what's now available for the next package to depend on.

No stage may be skipped. No stage may be merged with another to save time.

---

## 3. Definition of Done

A package is not complete until **every** item below is true:

- [ ] Documentation for the package's deliverables is complete and matches what was actually built (not what was planned, if the two diverged)
- [ ] All applicable validation tools have been run and passed
- [ ] Manual smoke tests (or automated tests, once `tools/tests/` exists) have been run for anything executable
- [ ] No temporary, scratch, or debug files remain in the repository (bash-tool scratch work stays in `/home/claude`, never committed)
- [ ] No content duplicates existing documentation (checked explicitly against the single-responsibility principle from `ENGINEERING_PRINCIPLES.md`)
- [ ] `git status` is clean — no untracked cruft, no partial edits
- [ ] The commit (or commit series) is pushed and matches what Founder Review approved
- [ ] Verification step (Section 2) has confirmed the live/remote state
- [ ] The package report (Section 2, final stage) has been delivered to the Founder

A package with any box unchecked is **not done**, regardless of how much of it is finished.

---

## 4. Commit Policy

**Frequency:** One commit per logically complete unit of work within a package. A package with multiple deliverables (e.g., PKG-3's four standards docs) may be multiple commits — prefer this over one large commit, consistent with Section 1, Principle 2.

**Message format:** `type(scope): summary`, matching the convention already used throughout the approved roadmap:
- `docs(scope): ...` — documentation
- `tools(scope): ...` — Python utilities
- `skills(scope): ...` — skill packages
- `docs+skill(scope): ...` — packages producing both (e.g., PKG-5)

Summary is imperative mood, under ~72 characters, no trailing period. Body (if needed) explains *why*, not *what* — the diff already shows what.

**Force-push:** Prohibited, without exception, on this repository. If a commit needs correcting, commit a correction on top. History is not rewritten.

**Squash:** Acceptable only for a single package's own commits, only before that package's Founder Review is finalized, and only if the squash doesn't destroy information useful for future debugging (e.g., don't squash across a validation-failure-then-fix pair if the failure itself is instructive — leave it visible).

**Granular history required for:** Anything in the Mutation tier (PKG-8) and anything touching `corrections/` or `known_traps.md` — these are exactly the places where "what changed and why, step by step" has future diagnostic value. Never squash these.

**Push authority:** Per the existing standing rule (`docs/GIT_WORKFLOW.md`), Claude never pushes without explicit session-level authorization from Nixon. This contract does not change that — it applies identically whether the actor is Claude Chat or Claude Code.

---

## 5. Validation Policy

Before any commit, in this order:

1. **Run validation tools** appropriate to the package (once they exist — `validate_html.py`, `validate_json.py`, and later tiers). For packages before those tools exist, validation is manual against the package's own checklist from the roadmap.
2. **Review tool output directly** — not a paraphrase of it. If a tool produces warnings as well as errors, warnings are reviewed too, not dismissed by default.
3. **Review every generated or modified file** in full, not by diff summary alone, for anything touching content or manifests.
4. **Review documentation links** — every cross-reference (`docs/` → `skills/`, `CLAUDE.md` → everything) must resolve to something that actually exists at commit time. A broken link is a validation failure, not a follow-up item.
5. **Review repository consistency** — does this package's output contradict anything already committed (a doc restating a principle differently than `ENGINEERING_PRINCIPLES.md`, a manifest field named inconsistently with `manifest_schema.py`, etc.)?

Any failure at any step returns the package to Implementation. Validation failures are never committed "to fix later."

---

## 6. Claude Chat Responsibilities

Always, without exception, stays in Claude Chat:

- Architecture and structural decisions (frozen per Section 11, but any future proposal is drafted here)
- Engineering judgement — regulatory interpretation, correctness of MEO Class 1 content, examiner-pattern accuracy
- Verification of external corrections (Gemini/Perplexity or any other source) against primary sources before acceptance
- Founder discussions, package reviews, escalations (Section 8)
- Drafting anything that encodes a standing rule or principle (`ENGINEERING_PRINCIPLES.md`, ADRs, `CORRECTION_WORKFLOW.md`) — even after Claude Code exists, these are Chat-authored and Chat-revised
- Any decision this contract requires the Founder to make — Chat surfaces the decision, it does not make it

## 7. Claude Code Responsibilities

Once handover occurs (per the roadmap's Claude Code Readiness section), Claude Code owns:

- Mechanical repository edits specified by an already-approved plan
- Running Python tools and reporting their output verbatim
- Validation execution (not validation *judgement calls* — a borderline validation result escalates to Chat/Founder, per Section 8)
- Repeatable mechanical refactoring (e.g., applying a pre-approved correction pattern across N files)
- Git operations within the bounds of Section 4
- Repository-wide corrections, once the correction itself has been judged correct in Chat

**Claude Code never:**
- Decides whether a regulatory claim is correct
- Decides whether a correction should be applied at all — only executes an already-approved correction
- Creates new architectural structure, new skills, or new standing documentation without a Chat-drafted, Founder-approved plan behind it
- Pushes without the same session-level authorization required of Chat

---

## 8. Escalation Policy

If uncertainty exists at any stage of any package:

1. **Stop.** Do not proceed on a best guess.
2. **Do not guess** at Founder intent, regulatory correctness, or architectural fit.
3. **Produce options** — state the uncertainty plainly, lay out the realistic paths forward with their tradeoffs (this contract's own predecessor documents are the model: comparison tables, pros/cons, not a single unexplained recommendation).
4. **Request Founder review.** Wait for an explicit decision before resuming.

This applies equally in Claude Chat and Claude Code. Claude Code hitting genuine uncertainty escalates to Chat/Founder exactly as Chat would — it does not attempt to resolve ambiguity by choosing the "most reasonable" interpretation when the ambiguity concerns engineering judgement, architecture, or scope.

---

## 9. Quality Gates

No package may pass a gate it hasn't earned. No gate may be bypassed, combined, or skipped "because this package is simple."

| Gate | Checks | Applies to |
|---|---|---|
| **Architecture Gate** | Does this package's output match the frozen architecture (Section 11)? Any deviation requires a new ADR proposal, not a quiet adjustment. | Every package |
| **Governance Gate** | Does this package's output comply with `ENGINEERING_PRINCIPLES.md` and relevant ADRs? | Every package |
| **Implementation Gate** | Was the package built exactly to its approved Scope — nothing missing, nothing extra absorbed silently? | Every package |
| **Validation Gate** | Section 5 fully executed, all checks passing? | Every package |
| **Founder Acceptance Gate** | Explicit Founder sign-off on the actual diff/output? | Every package |
| **Repository Sync Gate** | Local and remote identical after push; verification step (Section 2) confirms it? | Every package that commits |

A package is only permitted to start its successor once all applicable gates have passed and been recorded in that package's Report.

---

## 10. Continuous Improvement

If, during implementation, a better workflow, tool design, or package sequencing is discovered:

**Do not silently adopt it.** Instead, produce a recommendation containing:
- **Problem** — what's inefficient, risky, or wrong about the current approach
- **Proposed improvement** — the specific change
- **Benefits** — concrete, not hypothetical
- **Risks** — including the risk of changing an already-approved plan mid-stream
- **Affected packages** — which already-completed or upcoming packages this touches

The Founder decides whether to adopt it, defer it (logged for PKG-13's retrospective), or reject it. Implementation does not pause indefinitely for this — the current package continues under the existing plan unless the Founder explicitly redirects it.

---

## 11. Repository Freeze Policy

**Architecture is frozen.** (Approved: MIW_Architecture_Freeze_Review.md)
**Governance is frozen.** (Approved: MIW_Bootstrap_Governance_Review.md)

Implementation may improve *within* these approved boundaries — better prose, better tool ergonomics, better test coverage — without triggering a freeze violation.

Implementation may **not**:
- Add, remove, or rename top-level directories
- Reintroduce a rejected structure (e.g., `engineering/` wrapper, `DECISION_LOG.md`, premature `STYLE_GUIDE.md` or `automation/`)
- Change the Chat/Code responsibility boundary (Sections 6–7)
- Change the package sequence or dependency order without Founder approval

Any of the above requires a new ADR proposal, drafted in Claude Chat, reviewed exactly as the original architecture was — not a mid-implementation adjustment.

---

## 12. Implementation Checklist (One Page)

Use at the **start** and **end** of every package.

**At package start:**
- [ ] Package name and number confirmed against the approved roadmap
- [ ] Purpose, Scope, Deliverables restated and unchanged (or changes flagged to Founder first)
- [ ] Dependencies (prior packages) confirmed complete via their own Reports
- [ ] No architecture/governance freeze violation anticipated

**During execution:**
- [ ] Lifecycle stages (Section 2) followed in order, none skipped
- [ ] Any discovered out-of-scope item logged as a candidate package, not absorbed
- [ ] Any uncertainty escalated per Section 8, not guessed

**At package end:**
- [ ] Definition of Done (Section 3) — all boxes checked
- [ ] All six Quality Gates (Section 9) passed and recorded
- [ ] Commit policy (Section 4) followed exactly
- [ ] Verification step confirms committed state matches approved output
- [ ] Package Report delivered
- [ ] Repository confirmed in a working, complete state — safe to stop here indefinitely if needed

**Only if every box above is checked may the next package begin.**
