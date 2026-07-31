# MIW Repository Bootstrap — Governance Review
**Role:** Senior Software Architect (review only — no implementation, no documentation created)
**Status:** Approved (Founder decision, 2026-07-31) — Pre-PKG-1 gate review
**Date:** 2026-07-30

---

## 1. Repository Philosophy — Should It Be Formally Stated?

**Yes.** Right now the philosophy is scattered across the original bootstrap brief, your userPreferences, and my blueprint's prose. That's exactly the "trapped in conversation" problem this whole project exists to fix. If the philosophy itself isn't written down as a single artifact, everything downstream (docs, skills, tools) is built on an assumption, not a reference.

But it needs to be **short**. A philosophy document that takes 10 minutes to read gets read once and ignored. A philosophy document that fits on one screen gets re-read every session. Target: 8–12 principles, one line each, no elaboration in the same file.

Proposed principles (subject to your edit):

1. The repository is the source of truth; conversations are disposable.
2. Documentation is authoritative — if it's not written down, it doesn't count as decided.
3. One responsibility per document, one responsibility per tool.
4. Deterministic tooling is preferred over repeated AI reasoning wherever the task is mechanical.
5. Engineering judgement is never automated — tools validate and apply, they do not decide.
6. Corrections are never applied without verification against a primary source.
7. Mutation is opt-in and reversible by default (dry-run first).
8. Prefer many small, reviewable changes over large, unreviewable ones.
9. New structure is created only when a real, demonstrated need exists — not speculatively.
10. Claude Code executes against written specs; it does not rediscover conventions from history.

This maps directly onto your existing userPreferences ("Repository first, Application second, AI third" from RulesApp) — it's the same governance instinct, just not yet transplanted into this repo. That's a good sign: you're not inventing new philosophy, you're porting a proven one.

**Verdict: formalize this, but as Review Area 3 (governance doc), not folded into ARCHITECTURE.md or CLAUDE.md.**

---

## 2. Architecture Decision Records — Recommended

**Yes, adopt ADRs, but scoped tightly.** ADRs are valuable exactly when: (a) a decision was non-obvious, (b) reversing it later would be expensive, and (c) someone will eventually ask "why did we do it this way?" Not every choice qualifies. Your blueprint currently has ~5 decisions that meet that bar; the rest are just implementation detail that belongs in `docs/`, not in an ADR.

**Recommended ADR set (structure only — do not write these yet):**

| ADR | Decision | Why it needs to be an ADR, not just a doc |
|---|---|---|
| ADR-0001 | Repository-first philosophy (repo is source of truth; app/AI are interfaces to it) | This is a stance that could plausibly be challenged later ("why not just let Claude's memory be the source of truth?") — the record of *why* matters more than the *what* |
| ADR-0002 | Claude Chat vs. Claude Code division of responsibility | This will get questioned every time Claude Code gains new capability — the ADR is what stops the boundary from silently eroding |
| ADR-0003 | Documentation hierarchy (docs = what/why, skills = how/when, tools = mechanical execution) | Prevents future duplication drift — the single riskiest maintenance failure mode identified in the prior blueprint |
| ADR-0004 | Correction philosophy (verify-before-apply, never trust external AI review blindly, dry-run-first mutation) | This is a safety-critical decision with real consequences if reversed carelessly |
| ADR-0005 | Git/push authority model (Claude never pushes without explicit session-level authorization) | Also safety-critical; also exactly the kind of thing a future, less-cautious session might accidentally loosen without knowing why it was tight |

**What should NOT become an ADR:** QB HTML structure, manifest schema, cheat-sheet placement rules, examiner-tip conventions — these are *content standards*, not *architectural decisions*. They change more often and don't need the ceremony of an ADR (immutable, numbered, rationale-preserving record). Putting them in ADR format would make the ADR set noisy and devalue the ones that matter.

**Format recommendation:** Keep each ADR to Context / Decision / Consequences / Status — the standard lightweight format. Store as `docs/adr/0001-repository-first.md` etc. Status field matters: `Proposed → Accepted → (rarely) Superseded`. Never delete an ADR, even if superseded — supersession is itself a valuable record.

---

## 3. Repository Governance — What's Actually Worth Adding

Reviewing your four candidates individually rather than accepting the list wholesale:

- **`PROJECT_PHILOSOPHY.md`** — **Recommend, but merge into `PROJECT.md` (PKG-2) rather than a separate file.** A standalone philosophy doc plus a standalone project doc will overlap heavily (both answer "what is this and why"). One document, two sections, avoids the duplication risk flagged in the original blueprint's own design principles.
- **`ENGINEERING_PRINCIPLES.md`** — **Recommend as standalone.** This is genuinely different content from PROJECT.md (numbered principles list, Section 1 above) and gets referenced by name from CLAUDE.md, skills, and ADRs alike — it earns its own file because it's *pointed to* frequently, not just read once.
- **`DECISION_LOG.md`** — **Reject as a separate document — this is what ADRs are for.** A parallel decision log plus an ADR folder is redundant governance; pick one. ADRs win because they're per-decision (independently linkable, independently supersedable) rather than one growing file that becomes unwieldy and hard to cite precisely.
- **`STYLE_GUIDE.md`** — **Defer, don't reject.** Right now HTML/CSS/answer-format style lives correctly in the QB/Notes skill files (PKG-3/existing skills). A cross-cutting style guide only earns its place once you have 3+ content types with genuinely shared style rules beyond what's already in `CONTENT_GUIDE.md`. Creating it now would be exactly the "speculative structure" over-engineering risk flagged previously. Revisit at PKG-13 retrospective.

**Net governance doc set:** `ENGINEERING_PRINCIPLES.md` (new, standalone) + `docs/adr/` (new, per-decision) + philosophy folded into `PROJECT.md` (no new file). This is smaller than your candidate list of four, deliberately — governance sprawl is itself a maintainability risk.

---

## 4. Package Review — Challenging the Prior Design

Going package-by-package with a genuinely critical eye, not just re-confirming the prior blueprint.

**PKG-2, PKG-3, PKG-4 (docs) — merge candidate rejected, but reorder.** I initially proposed these as parallel/independent. On reflection, PKG-3 (content standards) implicitly depends on ENGINEERING_PRINCIPLES.md existing (principle 3, "one responsibility per document," needs to already be stated before you write four separate one-responsibility documents — otherwise you're applying a principle you haven't yet written down). **Correction: insert a new PKG-1.5 (Governance Docs) before PKG-2.**

**PKG-6/7/8 (Python utility tiers) — the tier split is correct, keep it.** Validation → Scan/Report → Mutation is a genuine risk gradient (read-only, read-only, read-write) and deserves separate review gates. No change.

**PKG-9 (Git Automation) — reconsider merging into PKG-8.** `git_commit.py` and `correction_summary.py` are thin wrappers with no mutation risk of their own (they format/commit, they don't decide *what* changed). Splitting them into their own package is more process overhead than the risk warrants. **Recommend merging PKG-9 into PKG-8**, keeping the mutation-tier tools and their git wrapper as one reviewable unit — they're used together every time anyway.

**PKG-10 (10 skills) — split confirmed necessary, not just "consider."** On review, this package as a single unit violates the blueprint's own "many small commits" principle worse than any other package — 10 independent artifacts bundled into one review is a code-smell by the project's own stated design principles. **Split into three:**
- PKG-10a: Correction-related skills (repo-scan, batch-correction, known-traps-update) — builds directly on PKG-5/7/8
- PKG-10b: Content-editing skills (qb-html-editing, notes-editing, engineering-validation) — largely thin pointers to existing skill files
- PKG-10c: Audit/release skills (repo-audit, git-workflow, manifest-update, release-preparation)

**PKG-11 (Corrections ledger) — reorder earlier, dependency was too conservative.** I originally gated this behind PKG-5 and PKG-8. But the ledger's *format* doesn't actually need the mutation tools to exist — only its *population* does. **Recommend splitting PKG-11 into PKG-11a (format spec + README, movable up to right after PKG-5) and PKG-11b (backfilled entries, stays gated behind PKG-8)** so the format is locked in before tools are built against it, not after — tools should target a stable spec, not the reverse.

**PKG-13 — no change, but add an explicit trigger condition.** "Run after real usage" is vague enough to never happen. Recommend a concrete trigger: after 10 real corrections have gone through the new workflow, or 4 weeks post-PKG-12, whichever comes first.

**New package needed: PKG-1.5 — Governance Docs.** Per Section 3, this must land after PKG-1 (audit) and before PKG-2 (it needs audit findings to be accurate, and PKG-2/3 need principles to reference). Deliverables: `ENGINEERING_PRINCIPLES.md`, `docs/adr/0001–0005` (the five identified in Section 2), philosophy section merged into what becomes PKG-2's `PROJECT.md`.

---

## 5. Skills Optimisation Review

Applying your three lenses (merge / templatize / stays-documentation) to each proposed skill:

| Proposed skill | Verdict | Reasoning |
|---|---|---|
| repo-correction-protocol | **Keep as skill** | Genuinely procedural, triggers on real recurring events, sequencing matters |
| repo-scan | **Merge into repo-correction-protocol** | It's a step inside corrections, not an independent workflow with its own trigger — as a standalone skill it would just be "run this one tool," which doesn't need skill ceremony |
| qb-html-editing | **Stays documentation** (already exists as `miw-qb-production` skill) | Redundant to create a second skill covering the same ground — this was already flagged as a duplication risk in Section 1 of the prior blueprint; the review should have caught this the first time |
| notes-editing | **Stays documentation** (already exists as `miw-notes-mgmt` skill) | Same reasoning |
| engineering-validation | **Becomes a checklist template, not a skill** | "Verify against primary source" isn't a workflow with steps to sequence — it's a standing rule best expressed as a checklist item referenced from ENGINEERING_PRINCIPLES.md and CORRECTION_WORKFLOW.md, not a skill with its own trigger conditions |
| git-workflow | **Merge into repo-correction-protocol and release-preparation** | Git actions never happen standalone in this repo — they're always the tail end of either a correction or a release; a bare git-workflow skill would just be documentation with no independent trigger, which is what `GIT_WORKFLOW.md` (PKG-4) is already for |
| manifest-update | **Keep as skill, but thin** | Genuinely reusable across QB/Notes/WA — real trigger conditions (any content addition), real sequencing (validate → update → verify) |
| known-traps-update | **Merge into repo-correction-protocol** | Same reasoning as repo-scan — it's a step, not a standalone workflow |
| repo-audit | **Keep as skill** | Distinct trigger (periodic/on-request), distinct from correction workflow, genuinely reusable pattern (this exact skill is what generated PKG-1 in the first place — it should be formalized from that experience) |
| batch-correction | **Keep as skill, built on repo-correction-protocol** | Genuinely different from single corrections — different risk profile (N files, not 1), worth its own trigger and validation checklist |
| release-preparation | **Keep as skill** | Distinct trigger (publishing a new QB/notes batch), distinct from correction workflow |

**Net result: 5 skills survive as genuinely reusable, standalone workflows** (repo-correction-protocol, manifest-update, repo-audit, batch-correction, release-preparation) — down from 10. Three merge into repo-correction-protocol as internal steps. Two are redundant with existing skills and should not be recreated. One becomes a checklist/template artifact instead of a skill.

This directly resolves the PKG-10 split question from Section 4 — it's no longer 10 skills split into 3 packages, it's **5 skills**, small enough to be one package again (revise PKG-10 back to a single package, now that scope is halved).

---

## 6. Python Utilities Optimisation Review

**Shared helper module — yes, clearly needed.** Reviewing the 10 proposed tools, several depend on identical primitives that would otherwise get reimplemented per-script:

- HTML parsing setup (the `HTMLParser` subclass with void-elements awareness) — needed by `validate_html.py` *and* implicitly by `repo_scan.py` (which must parse HTML to scan it structurally, not just grep text)
- File-path/manifest conventions (where QB files live, naming patterns) — needed by `repo_scan.py`, `manifest_update.py`, `repo_report.py`, `known_traps_update.py`
- Dry-run/apply flag handling — needed identically by every mutation-tier tool
- JSON read/write with the specific manifest schema — needed by `validate_json.py`, `manifest_update.py`, `repo_report.py`

**Recommend a `tools/_lib/` shared module** (underscore-prefixed to signal "not a standalone CLI tool"):
- `tools/_lib/html_parsing.py` — the shared HTMLParser subclass
- `tools/_lib/repo_paths.py` — canonical path/naming conventions, single source of truth for "where does content live"
- `tools/_lib/manifest_schema.py` — schema definitions + read/write helpers
- `tools/_lib/cli_common.py` — shared dry-run/apply argument handling

This directly serves your stated design principle ("Python utilities are modular") — modularity isn't just "one script per responsibility," it's also "shared logic factored out so the 10 scripts don't silently drift into 10 slightly-different implementations of the same HTML parser." Without this, PKG-6/7/8 will produce working but *inconsistent* tools — the classic failure mode where `validate_html.py`'s idea of a "void element" and `repo_scan.py`'s idea disagree after six months of independent small edits.

**Utilities that could actually be one script, not two:** `correction_summary.py` and `known_traps_update.py` overlap significantly — both generate a formatted record of a correction, just targeting different files (`corrections/` ledger vs. `known_traps.md`). **Recommend merging into a single `correction_record.py`** that writes both outputs from one invocation, rather than requiring two tool calls that could drift out of sync with each other (e.g., a correction logged in one but not the other).

**Revised utility count: 8 CLI tools + 1 shared `_lib/` package**, down from 10 flat scripts with implicit duplication.

---

## 7. Future Expansion — Repository at 2x Size

Assuming MIW doubles (more QB series, more content types beyond QB/Notes/WA/Timeline/Ecosystem/Archive, more examiners, more subscribers):

**What holds up well:**
- The docs/skills/tools separation scales fine — adding a new content type means one new thin standards doc (following the QB_STANDARDS.md pattern) and possibly one new skill, not a redesign
- `tools/_lib/` shared module scales well — new tools reuse the same primitives
- ADR set doesn't need to grow proportionally — architectural decisions don't double just because content does

**What creates real scaling risk:**
- **`repo_scan.py` and `similar_phrase_scan.py` performance** — at 2x content volume, naive full-repo grep/fuzzy-match starts costing real tokens/time per invocation. Mitigation: these tools should support scoping (`--path meoclass1/QB5*`) from day one (PKG-7), not bolted on later, so habitual full-repo scans don't become the default expensive path.
- **Manifest drift risk grows non-linearly** — more content types means more manifests (`qb_content_index.json`, `notes_content_index.json`, `written_content_index.json`, plus whatever a new content type needs) that can drift from each other and from `MEO_QB_master_v25.xlsx`. Mitigation: `manifest_schema.py` (Section 6) should define one canonical cross-manifest consistency check in `repo_report.py`, run as part of every release (PKG-4 `RELEASE_WORKFLOW.md`), not just per-manifest validation in isolation.
- **`corrections/` ledger becomes unwieldy as a flat directory at high volume** — fine at current scale, but if correction frequency grows significantly, a flat `corrections/YYYY-MM-DD_*.md` directory will eventually want date-based subdirectories (`corrections/2027/`) or an index. Not worth solving now — flag as a known future refactor, don't build it preemptively (this is exactly the over-engineering trap the blueprint already warns against).
- **Skill trigger overlap** — as more skills exist, ambiguous requests risk triggering the wrong skill (this already shows up in your live skill descriptions, which use fairly aggressive "always trigger" language). Mitigation: keep the 5-skill set from Section 5 lean rather than letting it regrow to 10+ as new content types arrive; prefer extending `repo-correction-protocol` and `release-preparation` to cover new content types over creating parallel per-content-type skills.

**Overall verdict: the architecture scales; the main risk is *tool scoping* and *manifest consistency*, not document/skill structure.** Both are addressed by decisions already made in this review (shared `_lib/`, explicit scoping flags, one canonical cross-manifest check) rather than requiring new structure.

---

## 8. RulesApp Lessons Worth Adapting (Without Copying)

From your stated RulesApp principles, three ideas transplant well, and I'd flag one that does *not* transplant cleanly:

**Transplants well:**
1. **"Repository first, application second, AI third."** Directly maps to "repo is source of truth, docs are authoritative, AI explains rather than replaces" — this is the philosophical backbone of Section 1's principle list, and it's proven itself in a sibling project already.
2. **Offline-first as a discipline, not just a feature.** MIW's equivalent isn't literal offline capability — it's "the repository must remain useful without Claude in the loop." A human (Nixon, or a future collaborator) should be able to read `docs/` and `known_traps.md` and understand the system with zero AI assistance. This is a good acceptance test to fold into the Founder Checklist (Section 10).
3. **Version 1.0 priority discipline** ("distinguish what should be built now vs. future vision, don't let future features delay v1"). This maps directly onto Section 9 below — it's the same discipline RulesApp already applies, just not yet applied to *this* bootstrap.

**Does not transplant cleanly:**
- RulesApp's "engineering objects with modeled relationships" (boiler → regulations → maintenance → alarms, etc.) is a knowledge-graph pattern suited to a rules/reference application. MIW's content (QB Q&A, exam notes) is fundamentally document-and-manifest shaped, not relationship-graph shaped. **Do not import this pattern into MIW's architecture** — it would be solving a problem MIW doesn't have, at real design cost. Worth naming explicitly so a future session doesn't assume RulesApp's data model should be ported wholesale.

---

## 9. Minimum Viable Bootstrap (Version 1 Scope)

Applying real over-engineering discipline — what must exist before implementation is "safe and useful," versus what can wait.

**Mandatory (blocks PKG-1 from being worth doing at all):**
- PKG-1 (Repository Audit)
- PKG-1.5 (Governance Docs: ENGINEERING_PRINCIPLES.md + ADR-0001 through ADR-0005)
- PKG-5 (Correction Workflow doc + skill) — this is the single highest-value artifact in the entire roadmap
- PKG-11a (Corrections ledger format spec only, not backfill)

**Recommended (large value, low risk, do soon after Mandatory):**
- PKG-2, PKG-3, PKG-4 (core/content/git docs)
- PKG-6 (Validation tools) — also the Claude Code pilot trigger
- `tools/_lib/` shared module (Section 6) — do this *as part of* PKG-6, not deferred, since retrofitting shared helpers after 3 tools already exist independently is wasted work

**Optional (real value, but repository functions correctly without them):**
- PKG-7 (Scan/Report tools) — valuable, but manual tarball/grep still works today; this is an efficiency gain, not a capability gap
- PKG-8 (Mutation tools, merged with PKG-9 per Section 4) — high value but high risk; delay until PKG-6/7 have proven the shared-lib pattern works
- PKG-10 (5 skills, per Section 5) — genuinely useful but the underlying workflows already function manually today

**Future (explicitly do not build until a demonstrated need exists):**
- PKG-11b (backfilled correction entries) — historical value only, not blocking
- PKG-12 (CLAUDE.md) — no value until enough of the above exists to link to; building it early just produces a document full of broken links
- PKG-13 (Optimisation retrospective) — by definition needs real usage data first
- `STYLE_GUIDE.md` (Section 3) — explicitly deferred
- `automation/` directory (prior blueprint, Section 1) — explicitly deferred
- Any new ADRs beyond the initial five — write more only when a new decision actually meets the ADR bar (Section 2)

**This reordering has one important consequence: it delays PKG-12 (Claude Code handover artifact) later than the prior blueprint implied**, because CLAUDE.md linking to half-finished infrastructure is worse than not having it yet. Claude Code handover readiness should be re-assessed after the "Recommended" tier is complete, not immediately after PKG-6 in isolation — PKG-6 gives Code *capability*, but CLAUDE.md gives it *findability*, and both need to be ready together.

---

## 10. Founder Acceptance Checklist

To be reviewed and explicitly signed off before PKG-1 begins.

**Architecture**
- [ ] Repository structure (docs/skills/tools/reports/corrections, `automation/` deferred) approved
- [ ] `tools/_lib/` shared module approach approved
- [ ] Merged/split package changes from Section 4 approved (PKG-1.5 added; PKG-9 merged into PKG-8; PKG-11 split into 11a/11b)

**Governance**
- [ ] ENGINEERING_PRINCIPLES.md scope (Section 1, ~10 principles) approved
- [ ] ADR-0001 through ADR-0005 scope (Section 2) approved; confirm no additional decisions belong in this initial set
- [ ] DECISION_LOG.md rejection (superseded by ADRs) accepted
- [ ] STYLE_GUIDE.md deferral accepted

**Skills**
- [ ] Reduced 5-skill set (Section 5) approved, replacing the original 10
- [ ] Confirmation that `qb-html-editing`/`notes-editing` will NOT be recreated as new skills (existing `miw-qb-production`/`miw-notes-mgmt` skills remain authoritative)

**Python Utilities**
- [ ] 8 CLI tools + shared `_lib/` (Section 6) approved, replacing the original 10 flat scripts
- [ ] Merge of `correction_summary.py` + `known_traps_update.py` into `correction_record.py` approved
- [ ] Mandatory dry-run-default policy for all mutation tools reconfirmed

**Scope**
- [ ] Version 1 Bootstrap scope (Section 9: Mandatory + Recommended tiers) approved as the actual implementation target
- [ ] Optional and Future tiers explicitly acknowledged as deferred, not cancelled
- [ ] PKG-12 (CLAUDE.md) re-sequencing — later than original plan — approved

**Claude Code Transition**
- [ ] Handover trigger (capability-ready at PKG-6 + findability-ready when Recommended tier completes) approved
- [ ] PKG-7 pilot-in-Code approach (from prior blueprint, Section 6) still stands, re-scoped to Optional tier timing

**Risk**
- [ ] Risk Register from prior blueprint (Section 7) re-reviewed against this governance review's changes — no new unmitigated risks introduced
- [ ] Explicit acknowledgment: no package in Mandatory or Recommended tiers touches a live content file — content-correctness risk remains zero through this phase

**Sign-off**
- [ ] Nixon Antony approves this governance review and the resulting revised roadmap
- [ ] PKG-1 authorized to begin

---

## Summary of Changes From the Prior Blueprint

| Area | Prior blueprint | This review |
|---|---|---|
| Governance docs | None planned | ENGINEERING_PRINCIPLES.md + 5 ADRs (new PKG-1.5) |
| Package count | 14 (PKG-0–13) | 15 (adds PKG-1.5; merges PKG-9 into PKG-8; splits PKG-11 into 11a/11b) |
| Skills | 10 proposed, 1 package | 5 confirmed reusable, 1 (smaller) package |
| Python tools | 10 flat scripts | 8 CLI tools + shared `_lib/` module |
| corrections/ ledger | One package, gated behind PKG-8 | Format (11a) moved earlier; backfill (11b) stays gated |
| CLAUDE.md timing | After PKG-6 area | Deferred until Recommended tier complete (findability requires substance to link to) |
| New rejected ideas | — | DECISION_LOG.md (redundant with ADRs), premature STYLE_GUIDE.md, premature `automation/` dir, RulesApp's relationship-graph data model |
