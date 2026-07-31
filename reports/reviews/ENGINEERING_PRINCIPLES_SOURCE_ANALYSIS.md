# Engineering Principles — Source Analysis

**Package:** PKG-1.5R — Engineering Principles Redevelopment
**Purpose:** Evidence base only. No principles are drafted in this document. Every observation below is traceable to a surviving repository document by name and location.
**Status:** Evidence-gathering. Awaiting Founder review before any drafting begins.
**Date:** 2026-07-31

---

## 0. What This Document Is Not

This is not a draft of Engineering Principles. It does not propose wording, numbering, or a final principle count. It does not resolve the two near-overlap pairs the lost draft was reported to contain. Its only job is to lay out what survives, organized so the next drafting session can see the whole evidence base at once instead of re-deriving it document by document.

---

## 1. Sources Reviewed

| Source | Role | Status |
|---|---|---|
| `reports/governance/MIW_Bootstrap_Blueprint.md` | Original roadmap draft (2026-07-30) | Committed, unchanged since commit |
| `reports/governance/MIW_Bootstrap_Governance_Review.md` | Revises the Blueprint — governance, ADRs, package reordering | Committed, **Approved** (2026-07-31) |
| `reports/governance/MIW_Architecture_Freeze_Review.md` | Rejects the `engineering/` wrapper, freezes flat structure | Committed, **Approved** (2026-07-31) |
| `reports/governance/IMPLEMENTATION_CONTRACT.md` | Package execution lifecycle, commit policy, quality gates | Committed, **Approved** (2026-07-31) |
| `AI_SESSION_HANDOVER.md` | Bridges bootstrap work between AI sessions | Committed |
| `BOOTSTRAP_CONSOLIDATION_PLAN.md` | This session's issue consolidation | Uncommitted (review artifact) |
| `ONBOARDING_VERIFICATION_REPORT.md` | This session's onboarding review | Uncommitted (review artifact) |

**One source added beyond the Founder's minimum list:**

| Source | Role | Status | Why included |
|---|---|---|---|
| `reports/governance/Bootstrap_Architecture_Amendment_LocalFirst.md` | Adopts Local-First git workflow after the GitHub connector's write path failed | Committed (PKG-1.7), **not** in the Founder's approved-status list — status unchanged, still reads "Proposed amendment, pending Founder approval" | It is a surviving, committed governance document bearing directly on workflow rules (git/push mechanism, Commit-stage responsibility) — the same category of content as the other five. Excluding it would leave a real gap in the workflow-philosophy evidence base. Flagged separately throughout since its approval status is unresolved, unlike the other five.

`MIW_Bootstrap_Blueprint.md` and the Amendment document were **not** part of the Founder's most recent approval decision (only the Governance Review, Architecture Freeze Review, and Implementation Contract were approved) — both are treated below as surviving evidence, not as pre-approved authority.

---

## 2. Extraction Method

Each source was re-read in full (not re-summarized from memory). Every statement below is either a direct quote or a close paraphrase, with a document + section/line citation. Where a statement appears in more than one source, every occurrence is listed under "Duplicated Ideas" (Section 4) rather than only the first one found.

---

## 3. Extracted Statements, Grouped by Theme

### Theme A — Repository as Source of Truth

- Blueprint: "`docs/` must stay 100% authoritative and hand-curated." (§1, "Changes from your proposal")
- Governance Review §1, proposed principle 1: *"The repository is the source of truth; conversations are disposable."*
- Governance Review §1, proposed principle 2: *"Documentation is authoritative — if it's not written down, it doesn't count as decided."*
- Implementation Contract §1, item 8: *"The repository, not the conversation, is what future sessions will trust. Every package must leave the repository able to explain itself without this conversation."*
- Handover §4: *"per Principle 1 (Repository First, itself still in draft), nothing is truly 'decided' until it's in the repository."*
- Handover §9 (closing note): *"Nothing above should be treated as settled until you find it committed in the repository."*
- Handover §9: *"Before creating any new document, check whether an existing one already owns the concern — this repository's own audit found real, costly duplication from skipping that check historically."*

### Theme B — Judgement vs. Mechanical Execution (Chat / Code / Tools boundary)

- Blueprint §2, "Responsibility Model": Chat owns judgement calls, planning, review gates, ambiguous/domain-reasoning corrections; Code (post-handover) owns mechanical/repeatable/spec-driven work and "should NOT make unreviewed engineering judgement calls about regulatory correctness"; Python utilities are "deterministic, testable, zero-judgement operations."
- Governance Review §1, proposed principle 5: *"Engineering judgement is never automated — tools validate and apply, they do not decide."*
- Governance Review §1, proposed principle 10: *"Claude Code executes against written specs; it does not rediscover conventions from history."*
- Implementation Contract §6: Chat's exclusive responsibilities — architecture/structural decisions, engineering judgement, verification of external corrections, Founder discussions, drafting anything that "encodes a standing rule or principle," and surfacing (not making) Founder-only decisions.
- Implementation Contract §7: Code's responsibilities and explicit prohibitions — "Claude Code never: Decides whether a regulatory claim is correct... Decides whether a correction should be applied at all... Creates new architectural structure, new skills, or new standing documentation without a Chat-drafted, Founder-approved plan behind it."

*Note: the Contract (§6–7) is a formal, binding restatement of the same boundary the Blueprint described informally (§2) — see Section 4, Duplicated Ideas.*

### Theme C — Deterministic Tooling Over Repeated AI Reasoning

- Governance Review §1, proposed principle 4: *"Deterministic tooling is preferred over repeated AI reasoning wherever the task is mechanical."*
- Governance Review §6: recommends a shared `tools/_lib/` module specifically so "the 10 scripts don't silently drift into 10 slightly-different implementations of the same HTML parser" — modularity framed as a design principle, not just a convenience.
- Governance Review §6: merges `correction_summary.py` and `known_traps_update.py` into one tool to prevent "a correction logged in one but not the other."

### Theme D — Verify Before Trust

- Governance Review §1, proposed principle 6: *"Corrections are never applied without verification against a primary source."*
- Implementation Contract §6: Chat is responsible for "Verification of external corrections (Gemini/Perplexity or any other source) against primary sources before acceptance."
- Blueprint §7 (Risk Register): "Claude Code operates without the judgement guardrails currently applied manually in Chat (e.g. 'never blindly apply external AI review corrections')" — flagged as a risk requiring these guardrails to become "explicit, machine-readable statements," not left as "tacit Chat-only knowledge."

### Theme E — Reversible, Opt-In Mutation

- Governance Review §1, proposed principle 7: *"Mutation is opt-in and reversible by default (dry-run first)."*
- Blueprint §4, PKG-8 scope: "mandatory `--dry-run` default (mutation requires explicit `--apply`)."
- Blueprint §7 (Risk Register): mutation-tier risk mitigation — "Mandatory dry-run default (PKG-8), `validate_html.py`/`validate_json.py` run automatically post-mutation, never auto-push."
- Implementation Contract §4: "Granular history required for: Anything in the Mutation tier (PKG-8) and anything touching `corrections/` or `known_traps.md`... Never squash these."

### Theme F — Small, Reviewable Units of Work

- Governance Review §1, proposed principle 8: *"Prefer many small, reviewable changes over large, unreviewable ones."*
- Implementation Contract §1, items 1–2: "Every package is small enough to review in one sitting. Every commit is small enough to understand at a glance."
- Implementation Contract §4: "One commit per logically complete unit of work within a package... prefer this over one large commit."

### Theme G — No Speculative Structure (Anti-Over-Engineering)

- Governance Review §1, proposed principle 9: *"New structure is created only when a real, demonstrated need exists — not speculatively."*
- Blueprint §1: `automation/` — "flag but don't over-build... If Phase 5 finds no second automation need beyond the existing health check, skip creating this directory — do not create structure speculatively."
- Blueprint §7 (Risk Register): over-engineering risk — "10 skills + 10 tools built... before real usage proves they're needed."
- Architecture Freeze Review §3: "build structure when a demonstrated need exists, not speculatively"; "Cheap migration doesn't make a worse architecture worth adopting."
- Governance Review §3: `STYLE_GUIDE.md` — "Defer, don't reject... Creating it now would be exactly the 'speculative structure' over-engineering risk flagged previously."
- Governance Review §7: `corrections/` ledger date-subdirectory refactor — "Not worth solving now — flag as a known future refactor, don't build it preemptively (this is exactly the over-engineering trap the blueprint already warns against)."
- Governance Review §9: entire Mandatory/Recommended/Optional/Future tiering is built around this discipline; on `CLAUDE.md` specifically — "building it early just produces a document full of broken links."

*This is the single most-reinforced idea in the surviving corpus — seven distinct occurrences across three documents.*

### Theme H — Single Responsibility / No Duplication

- Governance Review §1, proposed principle 3: *"One responsibility per document, one responsibility per tool."*
- Architecture Freeze Review, comparison table criterion 9: "Matches 'avoid unnecessary hierarchy,' 'one responsibility per document'" (direct echo of the above, cited as already-decided).
- Blueprint §7 (Risk Register): documentation/skill drift risk — mitigation "docs = what/why, skills = how/when, one line stating this rule at top of every doc/skill."
- Implementation Contract §3, Definition of Done: *"No content duplicates existing documentation (checked explicitly against the single-responsibility principle from `ENGINEERING_PRINCIPLES.md`)."*
- Handover §9: "Before creating any new document, check whether an existing one already owns the concern — this repository's own audit found real, costly duplication from skipping that check historically."

**This theme carries unusual weight**: Implementation Contract §3 — already Founder-approved — names "the single-responsibility principle from `ENGINEERING_PRINCIPLES.md`" directly. This is a forward reference from an approved document into the not-yet-written one, and it constrains the eventual redraft: whatever replaces the lost document should contain a principle nameable as "single-responsibility," or the Contract's own Definition of Done becomes a dangling reference.

### Theme I — Governance Process Integrity

- Implementation Contract §1, item 6: *"Governance is never bypassed for convenience, schedule, or Claude's own judgement of what's 'obviously fine.'"*
- Implementation Contract §1, item 7: *"Silence is not consent. Ambiguity is resolved by asking, not assuming."*
- Implementation Contract §8, Escalation Policy: "Stop. Do not proceed on a best guess... Do not guess at Founder intent, regulatory correctness, or architectural fit... Request Founder review. Wait for an explicit decision before resuming."
- Implementation Contract §11, Repository Freeze Policy: implementation may not add/remove/rename top-level directories, reintroduce rejected structure, change the Chat/Code boundary, or change package sequence without Founder approval — "Any of the above requires a new ADR proposal."
- Governance Review §10, Founder Acceptance Checklist: explicit multi-category sign-off gate (architecture, governance, skills, tools, scope, Claude Code transition, risk) before PKG-1 begins.

### Theme J — Documentation Hierarchy (docs / skills / tools)

- Blueprint §2: "`docs/` — Source of truth for 'how things work'... `skills/` — Source of truth for 'how to execute a specific recurring task'... reusable across QB/Notes/WA/Timeline where the pattern genuinely repeats... NOT duplicated per content type unless the workflow materially differs."
- Governance Review §2, ADR-0003 candidate: *"Documentation hierarchy (docs = what/why, skills = how/when, tools = mechanical execution) — Prevents future duplication drift — the single riskiest maintenance failure mode identified in the prior blueprint."*
- Blueprint §7 (Risk Register): same "docs = what/why, skills = how/when" phrase repeated as the named mitigation for documentation drift.

### Theme K — Frozen Flat Architecture

- Architecture Freeze Review, full document: ten-criterion comparison rejects the `engineering/` wrapper; "Architecture A wins or ties on all 10 criteria. Architecture B wins outright on none" (§1); final frozen tree recorded in §6.
- Architecture Freeze Review §4: rejecting the wrapper preserves "a single home" for governance (`docs/adr/` + `ENGINEERING_PRINCIPLES.md`) rather than reopening a fragmentation question the Governance Review had already closed.
- Implementation Contract §11: "Architecture is frozen. (Approved: `MIW_Architecture_Freeze_Review.md`)... Implementation may not: Add, remove, or rename top-level directories... [or] Reintroduce a rejected structure."

### Theme L — RulesApp-Derived Lessons

- Governance Review §8: *"Repository first, application second, AI third"* — stated as directly mapping onto MIW's Theme A principles, "proven itself in a sibling project already."
- Governance Review §8: "Offline-first as a discipline, not just a feature... MIW's equivalent... is 'the repository must remain useful without Claude in the loop.' A human (Nixon, or a future collaborator) should be able to read `docs/` and `known_traps.md` and understand the system with zero AI assistance." Explicitly flagged as "a good acceptance test to fold into the Founder Checklist."
- Governance Review §8: Version 1.0 priority discipline ("distinguish what should be built now vs. future vision") — maps onto the §9 tiering (Theme G).
- Governance Review §8: explicit non-adoption — RulesApp's "engineering objects with modeled relationships" data model "does not transplant cleanly" and "should not" be imported into MIW's architecture, "named explicitly so a future session doesn't assume RulesApp's data model should be ported wholesale."

### Theme M — Scope Discipline

- Blueprint §7 (Risk Register): "Each package's 'Scope' section is a hard boundary; anything discovered mid-package that's out of scope gets logged as a new candidate package, not absorbed."
- Implementation Contract §2, Implementation stage: "Build exactly what Planning specified. Nothing extra. Discoveries outside scope are logged as candidate future packages (Section 10), not absorbed silently."
- Implementation Contract §12, checklist: "Any discovered out-of-scope item logged as a candidate package, not absorbed."

### Theme N — Content-Correctness Risk Isolation

- Blueprint, Open Questions §4: "No package in this roadmap touches a live QB/Notes/WA content file. Correct — this is intentional, so the entire bootstrap can be reviewed and merged without any content-correctness risk."
- Governance Review §10, Sign-off checklist: "Explicit acknowledgment: no package in Mandatory or Recommended tiers touches a live content file — content-correctness risk remains zero through this phase."

### Theme O — Push/Commit Mechanism (Local-First)

- Bootstrap_Architecture_Amendment_LocalFirst.md §1: "formally adopt the Local-First Repository Workflow" — reasoning: fewer moving parts, consistency with already-adopted practice, equal-or-better auditability, more diagnosable failure mode.
- Amendment §2: names `IMPLEMENTATION_CONTRACT.md` as needing an explicit update to Sections 4 and 7 to name the specific push mechanism — **this update does not appear to have been made** (see Section 5, Contradictions, below).
- Implementation Contract §4: "Push authority: Per the existing standing rule (`docs/GIT_WORKFLOW.md`), Claude never pushes without explicit session-level authorization from Nixon."

---

## 4. Duplicated Ideas

Ideas stated, near-verbatim or in substance, in three or more places:

| Idea | Occurrences | Sources |
|---|---|---|
| No speculative/premature structure | 7 | Governance Review §1/§3/§7/§9, Blueprint §1/§7, Architecture Freeze Review §3 |
| Repository/documentation is the source of truth | 6 | Blueprint §1, Governance Review §1 (×2 principles), Contract §1, Handover §4/§9 |
| Single responsibility / no duplication | 5 | Governance Review §1, Architecture Freeze Review comparison table, Blueprint §7, Contract §3, Handover §9 |
| Judgement vs. mechanical boundary (Chat/Code/Tools) | 5 | Blueprint §2, Governance Review §1 (×2 principles), Contract §6–7 |
| Verify before trust (primary-source verification) | 3 | Governance Review §1, Contract §6, Blueprint §7 |
| Small, reviewable units of work | 3 | Governance Review §1, Contract §1 (×2 items), Contract §4 |
| Scope discipline (log, don't absorb) | 3 | Blueprint §7, Contract §2, Contract §12 |
| Documentation hierarchy (docs/skills/tools) | 3 | Blueprint §2, Governance Review §2, Blueprint §7 |
| Reversible/opt-in mutation | 4 | Governance Review §1, Blueprint §4/§7, Contract §4 |
| Content-correctness risk isolation | 2 | Blueprint (Open Questions), Governance Review §10 |

**Observation:** Every one of the 10 one-line principles in `MIW_Bootstrap_Governance_Review.md` §1 is independently corroborated elsewhere in the surviving corpus — none of the 10 is a one-off. This is useful signal for a future drafting session: these 10 are not fragile or speculative, they are the most load-bearing ideas across the whole document set.

---

## 5. Overlapping Concepts (Not Identical, But Adjacent)

These are pairs that say related-but-distinct things. A future drafting pass will need to decide whether each pair stays as two principles, merges into one, or gets explicitly differentiated:

1. **"Repository is the source of truth" (P1) vs. "Documentation is authoritative" (P2)** (both Governance Review §1) — P1 is a claim about the *repository as a whole* (vs. conversation); P2 is a narrower claim about *written documentation specifically* (vs. undocumented decisions). Related, not identical — P1 could subsume P2, or P2 could be read as an operational corollary of P1.
2. **"Deterministic tooling preferred" (P4) vs. "Engineering judgement never automated" (P5)** (both Governance Review §1) — two directions of the same boundary: push mechanical work toward tools (P4) and keep judgement out of tools (P5). Plausibly two faces of one principle.
3. **"One responsibility per document/tool" (P3) vs. "New structure only when demonstrated need exists" (P9)** (both Governance Review §1) — P3 governs the *scope* of an artifact once it exists; P9 governs *whether* it should exist at all. Related but operating at different decision points.
4. **"Mutation is opt-in/reversible" (P7) vs. "Prefer many small reviewable changes" (P8)** (both Governance Review §1) — both are risk-containment-through-granularity ideas, but P7 is specifically about mutation tooling while P8 is about commit/package sizing generally.

*Note: these are this analysis's own observations about adjacency in the surviving 10-item list — they are not necessarily the same two pairs the lost 14-principle draft flagged as near-overlaps (see Section 6 below, which found no surviving trace of the lost draft's own named pairs).*

---

## 6. Missing Areas

Gaps where a source explicitly calls for something that never actually materializes anywhere in the surviving corpus:

1. **The lost draft's own named principles are untraceable.** `AI_SESSION_HANDOVER.md` §4 names two flagged near-overlap *pairs* from the lost 14-principle draft: "Explicit Relationships vs. Traceability" and "Deterministic Tooling vs. Reproducibility." Of these four names, only "Deterministic Tooling" has any surviving definition (Governance Review P4, Theme C above). **"Explicit Relationships," "Traceability," and "Reproducibility" do not appear, defined or undefined, anywhere in any surviving source.** This is the clearest direct evidence of what the lost document actually contained that the surviving 10-item seed list does not: at minimum, these three additional named concepts, plus whatever separates 10 items from 14.
2. **"The repository must remain useful without Claude in the loop"** (Governance Review §8, Theme L) is explicitly flagged as something that should be "fold[ed] into the Founder Checklist" — but the actual Founder Acceptance Checklist (Governance Review §10) contains no line item matching this description. The idea was proposed and never operationalized anywhere in the surviving corpus.
3. **No ADR has been drafted.** Five ADR topics are named and scoped (Governance Review §2: repository-first philosophy, Chat/Code division, documentation hierarchy, correction philosophy, git/push authority), and the Implementation Contract (§7) describes ADRs as companion artifacts to `ENGINEERING_PRINCIPLES.md` — but none of the five exist as files anywhere. The principles document and the ADR set were planned together; only the principles' *topic list* (via the 10-item seed) partially survives.
4. **Version 1.0 / MVP-priority discipline** is discussed at length (Governance Review §8, §9) but never phrased as a standalone principle statement anywhere — it exists only as package-tiering practice (Mandatory/Recommended/Optional/Future), not as a principle a document like `ENGINEERING_PRINCIPLES.md` would state directly.

---

## 7. Contradictions and Live Tensions

1. **Governance-home location tension.** The Architecture Freeze Review (§4, §6) and Implementation Contract (§11) both state the frozen architecture's single governance home is `docs/adr/` + `ENGINEERING_PRINCIPLES.md` — i.e., `docs/`. The Founder's current decision places the newly-approved `ENGINEERING_PRINCIPLES.md` at `docs/ENGINEERING_PRINCIPLES.md` (correct, matches the frozen architecture) — but the three already-approved governance documents (Governance Review, Architecture Freeze Review, Implementation Contract itself) currently sit at `reports/governance/`, a provisional location chosen in PKG-1.7 specifically because `docs/` didn't exist yet and the path question was still open. Now that `docs/` is about to be created and the path question is resolved for the principles document, the three approved governance documents and the (upcoming) principles document will sit in **two different directories**, despite the frozen architecture describing governance as having "a single home." Not a contradiction between the source documents themselves — a live gap between stated intent and current repository state, worth Founder attention when `docs/` is created.
2. **The Local-First Amendment's required Contract update was never applied.** `Bootstrap_Architecture_Amendment_LocalFirst.md` §2 explicitly states `IMPLEMENTATION_CONTRACT.md` Sections 4 and 7 "must update" to name Local-First as the specific push mechanism, replacing the current abstract language ("Claude never pushes without explicit session-level authorization" — mechanism-agnostic). Checking the now-approved `IMPLEMENTATION_CONTRACT.md`: Section 4's push-authority language is still the original abstract wording; the amendment's specific update was never incorporated. The Amendment document's own status also still reads "Proposed amendment, pending Founder approval" — unresolved, unlike its three sibling documents. This is a real, still-open loose end, separate from the Engineering Principles gap, surfaced here because it was encountered during this source review.
3. **Forward reference to a non-existent document.** `IMPLEMENTATION_CONTRACT.md` §4 cites "the existing standing rule (`docs/GIT_WORKFLOW.md`)" for push authority — but `docs/GIT_WORKFLOW.md` does not exist yet (planned for PKG-4). This is a forward reference to planned content, not a broken link to something that should already exist, but it means the Contract's push-authority rule currently has no committed textual basis anywhere in the repository — it rests entirely on the Contract's own restatement of it.
4. **Sequencing correction, not a contradiction but worth noting for provenance.** The Blueprint's original package dependency diagram (§3) shows PKG-2/3/4 running with no dependency on a governance-docs package, because PKG-1.5 did not exist yet when the Blueprint was written. The Governance Review (§4) explicitly says *"Correction: insert a new PKG-1.5 before PKG-2"* — a self-aware revision, not a conflict requiring resolution, but it means the Blueprint's dependency diagram is stale relative to the Governance Review and should not be read as current without that correction in mind.
5. **Commit-type taxonomy doesn't cover actual practice.** `IMPLEMENTATION_CONTRACT.md` §4 enumerates commit message types (`docs`, `tools`, `skills`, `docs+skill`) but PKG-1.6 and PKG-1.7's actual commits used `fix(repo):` and `docs(governance):` — neither of which is enumerated. Minor, but a real gap between the approved policy text and what has already happened in this repository's history.

---

## 8. Summary Table

| Theme | Occurrences | Status |
|---|---|---|
| A — Repository as Source of Truth | 6 | Consistent, heavily reinforced |
| B — Judgement vs. Mechanical Boundary | 5 | Consistent; Contract formalizes Blueprint's informal version |
| C — Deterministic Tooling | 3 | Consistent |
| D — Verify Before Trust | 3 | Consistent |
| E — Reversible Mutation | 4 | Consistent |
| F — Small Reviewable Units | 3 | Consistent |
| G — No Speculative Structure | 7 | Consistent, most-reinforced idea in the corpus |
| H — Single Responsibility / No Duplication | 5 | Consistent; constrained by a live forward-reference in an approved document |
| I — Governance Process Integrity | 5 | Consistent |
| J — Documentation Hierarchy | 3 | Consistent |
| K — Frozen Flat Architecture | 3 | Consistent, formally approved |
| L — RulesApp-Derived Lessons | 4 | One sub-idea (offline-first-as-discipline) never operationalized — see Missing Areas #2 |
| M — Scope Discipline | 3 | Consistent |
| N — Content-Correctness Risk Isolation | 2 | Consistent |
| O — Push/Commit Mechanism | 3 | **Unresolved** — Amendment still "Proposed," its required Contract update never applied |

---

## 9. Closing Note

No content for `docs/ENGINEERING_PRINCIPLES.md` has been drafted, implied, or suggested in this document. What survives is: a corroborated 10-item seed list (Governance Review §1), strong thematic reinforcement for each of those 10 items from independent sources, clear evidence that the lost draft contained additional named material this analysis cannot recover (Section 6, item 1), and several live process gaps (Section 7) that a drafting session — or a separate small package — may want to resolve alongside or before redrafting.

This document is submitted for Founder review. No repository file was modified. Nothing was committed.
