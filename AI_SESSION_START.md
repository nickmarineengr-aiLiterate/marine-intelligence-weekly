# AI Session Start

> ## ⚠ Repository Identity Banner — read before doing anything
> | | |
> |---|---|
> | **Repository** | Marine Intelligence Weekly |
> | **Local path** | `F:\Marine-Intelligence-Weekly` |
> | **Branch** | `main` |
> | **Remote** | `nickmarineengr-aiLiterate/marine-intelligence-weekly` |
>
> **This repository is NOT RulesApp.** A separate, similarly-pathed repository (`nickmarineengr-aiLiterate/RulesApp`) exists elsewhere on this machine and has caused real onboarding confusion before. **Always run `git remote -v` before beginning any work** to confirm you are in the correct repository.

**Status:** Authoritative onboarding entry point for any new AI session (GPT or Claude) with zero prior context on this repository. This is the single entry point — do not create another one alongside it.
**Relationship to `AI_SESSION_HANDOVER.md` (root):** this document is now the authoritative entry point going forward. `AI_SESSION_HANDOVER.md` is intentionally left in place, unmodified, pending validation of this document across several fresh AI sessions — its retirement is a separate, future Founder-approved cleanup package, not part of this one. Prefer this document; do not treat that one as authoritative in the meantime.
**Date:** 2026-07-31
**Target reading time:** Under 5 minutes. Everything below is a summary with a pointer to the owning document — do not restate governance text back into this file when updating it; edit the owning document instead and update the summary here only if the summary itself becomes wrong.

---

## Repository Read Strategy

1. **Read this document first, in full.** Nothing else, not yet.
2. **Understand the specific task you've been asked to do.**
3. **Read only the one additional document that task genuinely requires** — Section 7 ("Read Order") below tells you which, per task type.
4. **Do not read the entire repository.** Requesting every document "to be thorough" wastes time and contradicts this repository's own No Speculative Structure discipline (P5) — read only what the task in front of you actually needs.

---

## 1. Repository Identity

- **Name:** `marine-intelligence-weekly`
- **Remote:** `https://github.com/nickmarineengr-aiLiterate/marine-intelligence-weekly.git`
- **Branch:** `main`
- **Local path (Founder's machine):** `F:\Marine-Intelligence-Weekly`
- **Note:** A *different* repository, `nickmarineengr-aiLiterate/RulesApp`, is sometimes checked out at a visually similar path (`F:\RulesApp\...`). Verify `git remote -v` before trusting any path — a prior session lost time to this exact confusion (`reports/reviews/ONBOARDING_VERIFICATION_REPORT.md`).

## 2. Repository Purpose

Marine Intelligence Weekly (MIW) is a maritime newsletter and subscription platform, centered on an MEO Class 1 oral-exam preparation product (`meoclass1/`), plus a timeline, ecosystem map, issue archive, and GHG/decarbonisation tracking (`GHGDecarb/`). It also co-hosts an unrelated, pre-existing product, `RulesApp/`, as a sibling directory — out of scope for this bootstrap. Full detail: `docs/PROJECT.md`.

## 3. Current Repository Status

This document intentionally does not name a specific "latest commit" — that fact goes stale the moment the next commit lands. **Always run `git log -1` and `git status` yourself** to get the true current state; treat anything below as background, not as live fact.

- As of this document's last edit, the working tree was clean except a small number of untracked, pre-existing items unrelated to any active package (e.g. a local `Claude skill/` directory duplicating already-committed `reports/governance/` content, and two supporting documents cited by name inside `docs/ENGINEERING_PRINCIPLES.md` but never committed). Confirm with `git status` whether this is still accurate.
- Live state always outranks any document, including this one.

## 4. Current Development Stage

**Post-governance-bootstrap, pre-Mandatory-tier-completion.** The engineering bootstrap established a governance foundation (audit → architecture freeze → implementation contract → engineering principles → correction workflow → corrections ledger spec), but has not yet finished the bootstrap's own defined completion bar (Section 9, below). No package has touched live subscriber content yet.

## 5. Governance Hierarchy (summary only — see `docs/ARCHITECTURE.md` § Governance Hierarchy for the full statement)

Four layers, none duplicating another:

1. **Architecture** — `reports/governance/MIW_Architecture_Freeze_Review.md` (**Approved**). Frozen flat top-level structure: `docs/`, `skills/`, `templates/`, `reports/`, `corrections/`, `tools/`, plus unchanged existing content dirs. Changes require a new ADR.
2. **Process** — `reports/governance/IMPLEMENTATION_CONTRACT.md` (**Approved**). The binding 8-stage package lifecycle (Section 10, below) and Chat/Code responsibility split.
3. **Values** — `docs/ENGINEERING_PRINCIPLES.md` (**Draft v0.2**, not yet Approved). 7 principles; 6 ADR topics reserved (`ADR-0001`–`ADR-0006`), none drafted yet.
4. **Operational procedure** — `docs/CORRECTION_WORKFLOW.md` + `corrections/README.md` (both committed/operational). How corrections specifically move through layers 2–3.

## 6. Repository Philosophy

Full statements and rationale: `docs/ENGINEERING_PRINCIPLES.md`. One line each:

- **P1 Repository First** — the repository is truth; an undecided-in-writing thing isn't decided.
- **P2 Single Responsibility** — one job per document, one job per tool; never duplicate.
- **P3 Mechanical vs. Judgment Boundary** — deterministic work goes to tools; engineering/regulatory judgment is never automated.
- **P4 Verify Before Trust** — no correction applied without primary-source verification; never trust external AI review on its own.
- **P5 No Speculative Structure** — build only when a current, real package demonstrates the need.
- **P6 Code Executes Written Specs** — Claude Code works from committed specs, never from inferred conversation history.
- **P7 Repository Independence** — a human must be able to understand this repository with zero AI assistance.

## 7. Read Order (only if you're about to do something this document doesn't cover)

Don't read all of these up front — request only what the specific task requires:

| If you are about to… | Read |
|---|---|
| Execute, validate, or commit any package | `reports/governance/IMPLEMENTATION_CONTRACT.md` in full (this document only summarizes it) |
| Judge whether output complies with governance | `docs/ENGINEERING_PRINCIPLES.md` in full |
| Process a content/repository/governance correction | `docs/CORRECTION_WORKFLOW.md`, then `corrections/README.md` |
| Fix MEO Class 1 content specifically | `meoclass1/known_traps.md` (existing entry format + prior errors) |
| Understand repository structure/directory roles | `docs/ARCHITECTURE.md` |
| Need pre-2026-07-31 historical context | `docs/BOOTSTRAP_BASELINE.md` (frozen snapshot, never updated) |

## 8. Current Engineering Focus

Closing the bootstrap's own Mandatory tier (Section 9) and clearing two concrete blockers:
1. **`docs/ENGINEERING_PRINCIPLES.md` is Draft v0.2, not Approved** — needs explicit Founder sign-off on this specific committed diff (never shown to the Founder in this form before).
2. **Six reserved ADRs (`ADR-0001`–`ADR-0006`) are undrafted** — the Governance Gate (`IMPLEMENTATION_CONTRACT.md` §9) checks every package against "Principles and relevant ADRs" as a pair; the ADR half doesn't exist yet.

Two defensible next packages exist in the committed record (`docs/BOOTSTRAP_BASELINE.md`, "Recommended Starting Point"): **PKG-1.8** (Notes Manifest Resolution — small, mostly a Founder decision) or continuing Mandatory-tier closure. Do not pick unilaterally — ask, or follow whichever the Founder most recently directed.

## 9. Current Roadmap Status

Numbered sequence `PKG-0`–`PKG-13` (`reports/governance/MIW_Bootstrap_Governance_Review.md` §4/§9), plus interstitial sub-packages actually executed (`PKG-1.6` through `PKG-1.10`, `PKG-1.5R`).

**Bootstrap's own Mandatory tier** (§9): PKG-1 ✅ complete · PKG-1.5 ⚠️ partial (governance approvals done, Principles still Draft, ADRs undrafted) · PKG-5 ✅ complete · PKG-11a ✅ complete (ledger spec only; backfill is PKG-11b, deferred). **The bootstrap is not yet complete against its own defined bar** — do not describe it as fully done.

**Also complete:** PKG-2 (`docs/PROJECT.md`, `docs/ARCHITECTURE.md`).
**Not started:** PKG-1.8 (Notes Manifest Resolution), PKG-3 (Content Standards Docs), PKG-4 (Git/Release Workflow Docs), PKG-6–13 (Python tooling tiers, remaining skills, PKG-11b ledger backfill, `docs/CLAUDE.md`, retrospective), the 6 reserved ADRs, and the planned governance-doc migration (`reports/governance/` → partially into `docs/`, per `reports/reviews/GOVERNANCE_MIGRATION_SPECIFICATION.md` — precondition met, not yet executed).

## 10. Rules Every AI Session Must Follow

1. **The repository outranks this conversation and this document.** Verify live state before trusting any claim (P1).
2. **Follow the 8-stage package lifecycle exactly**, no skipping or merging stages: Planning → Implementation → Validation → Founder Review → (Revision loop) → Commit → Verification → Report (`IMPLEMENTATION_CONTRACT.md` §2).
3. **Never commit or push without explicit, session-level Founder authorization** — every time, not just once. The GitHub connector's write path is confirmed non-functional (403); Local-First (`git commit` + `git push origin main`) is the only approved mechanism.
4. **Never add, remove, or rename a top-level directory**, or reintroduce a rejected structure, without a new ADR (`IMPLEMENTATION_CONTRACT.md` §11).
5. **No speculative structure (P5)** — build only what the current package genuinely needs.
6. **Content corrections require primary-source verification first (P4)** — never apply an external AI review or unverified report on trust alone.
7. **Escalate uncertainty; never guess** — state the uncertainty, lay out options, wait for an explicit Founder decision (`IMPLEMENTATION_CONTRACT.md` §8).
8. **`RulesApp/` is a separate, out-of-scope, co-located product** — do not touch it under this bootstrap's work.
9. **Chat vs. Code boundary**: engineering/regulatory judgment, architecture decisions, and anything encoding a standing rule stay in Claude Chat; Claude Code (once handed over) executes only already-approved, written plans (`IMPLEMENTATION_CONTRACT.md` §6–7).
10. **One package at a time**, small enough to review in one sitting; do not silently absorb out-of-scope discoveries — log them as candidate future packages.

---

# GPT / Claude Session Handover

Copy everything below into a brand-new GPT or Claude session with no prior context:

```
You are picking up work on the "marine-intelligence-weekly" repository
(F:\Marine-Intelligence-Weekly, remote: github.com/nickmarineengr-aiLiterate/marine-intelligence-weekly,
branch: main). Assume you know nothing about this project beyond what's in the repository.

Before anything else, read AI_SESSION_START.md at the repository root in full — it is the
single authoritative onboarding document. A separate file, AI_SESSION_HANDOVER.md, also
exists at the root; it is not authoritative — prefer AI_SESSION_START.md whenever the two
would conflict. It tells you the repository's purpose, current status, governance hierarchy,
philosophy, and the rules you must follow.

Do not read every other document up front. AI_SESSION_START.md Section 7 ("Read Order")
tells you exactly which additional document to request based on what you're about to do —
request only that one, when you actually need it.

Standing rules, non-negotiable regardless of task:
- The repository is truth, not this conversation. Verify live state (git log/git status/
  direct file reads) before trusting any claim, including AI_SESSION_START.md itself.
- Never commit or push without explicit, session-level authorization from the Founder,
  even if a prior turn already authorized a different action.
- Follow the 8-stage package lifecycle exactly (Planning -> Implementation -> Validation ->
  Founder Review -> Revision if needed -> Commit -> Verification -> Report). No skipping,
  no merging stages, no exceptions for "this one's simple."
- If anything is ambiguous - Founder intent, regulatory correctness, architectural fit -
  stop and ask. Do not guess.
- Do not create new documents, directories, or tools speculatively. Build only what the
  current task demonstrably needs.

Once you've read AI_SESSION_START.md, tell me what you understand the current engineering
focus and next viable package to be, and ask me anything you still need clarified before
we begin.
```
