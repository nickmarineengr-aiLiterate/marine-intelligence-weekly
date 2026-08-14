# MIW Repository Engineering Bootstrap — Master Blueprint
**Role:** Project Architect (planning only — no implementation)
**Status:** Draft for Founder Architecture Review
**Date:** 2026-07-30

---

## 0. How This Document Is Organised

1. Recommended repository structure
2. Workflow architecture (Chat / Code / Python / Git / Docs / Skills)
3. Package dependency diagram
4. Execution roadmap — all implementation packages, in order
5. Token optimisation analysis
6. Claude Code readiness & handover point
7. Risk register
8. Founder Architecture Review checklist (the gate before Phase 1 starts)

---

## 1. Recommended Repository Structure

Your proposed layout is sound. Two changes recommended, with reasoning below.

```
marine-intelligence-weekly/
├── docs/                      # Authoritative, stable knowledge — read by humans and Claude
│   ├── PROJECT.md             # What MIW is, who it's for, business model, current state
│   ├── ARCHITECTURE.md        # Repo structure, hosting, payments/auth, data flow
│   ├── CONTENT_GUIDE.md       # Cross-cutting content rules shared by QB/Notes/WA/Timeline etc.
│   ├── QB_STANDARDS.md        # QB-specific HTML/answer format (thin — links to skill for detail)
│   ├── NOTES_STANDARDS.md     # Engineering Management Notes structure
│   ├── CHEATSHEET_STANDARDS.md
│   ├── CORRECTION_WORKFLOW.md # The one true correction SOP (all content types reference this)
│   ├── GIT_WORKFLOW.md        # CLI vs web editor, cache-busting, tarball verification
│   ├── RELEASE_WORKFLOW.md    # Build → gate → validate → manifest → push → verify
│   ├── KNOWN_TRAPS.md         # Pointer/index — actual file stays at meoclass1/known_traps.md
│   └── CLAUDE.md              # Entry point for Claude Code (links out, never inlines content)
│
├── skills/                    # Reusable Skill definitions (Purpose/Inputs/Outputs/Workflow/Validation)
│   ├── repo-correction-protocol/
│   ├── repo-scan/
│   ├── qb-html-editing/
│   ├── notes-editing/
│   ├── engineering-validation/
│   ├── git-workflow/
│   ├── manifest-update/
│   ├── known-traps-update/
│   ├── repo-audit/
│   ├── batch-correction/
│   └── release-preparation/
│
├── tools/                     # Python utilities — one responsibility each
│   ├── repo_scan.py
│   ├── similar_phrase_scan.py
│   ├── replace_engine.py
│   ├── validate_html.py
│   ├── validate_json.py
│   ├── known_traps_update.py
│   ├── manifest_update.py
│   ├── git_commit.py
│   ├── repo_report.py
│   └── correction_summary.py
│
├── templates/                 # Boilerplate for new content (QB skeleton, correction footer, etc.)
│   ├── qb_file_template.html
│   ├── correction_footer_template.html
│   └── manifest_entry_template.json
│
├── reports/                   # Generated, disposable — audit reports, health-check logs, correction summaries
│   ├── audit/
│   ├── health-checks/
│   └── corrections/
│
├── corrections/                # NEW — structured correction records (see reasoning below)
│   └── YYYY-MM-DD_<short-slug>.md
│
└── automation/                 # NEW — CI/scheduled workflows, separated from ad-hoc tools/
    └── .github/workflows/      # (or symlink reference — GH Actions must live at repo root .github/)
```

### Changes from your proposal, with reasoning

**`reports/` is generated output, not documentation — keep it out of `docs/`.**
`docs/` must stay 100% authoritative and hand-curated. If health-check logs or audit reports live in `docs/`, the directory stops being "trustworthy by default" and every future Claude session has to distinguish signal from noise. `reports/` is disposable/regenerable and can be `.gitignore`d or pruned periodically.

**`corrections/` as structured records, not just a workflow doc.**
`CORRECTION_WORKFLOW.md` describes *how* to correct. But you already have a `known_traps.md` changelog pattern that works well — the missing piece is a durable, greppable *record* of what was corrected, when, and why, independent of the QB file's own footer. This is what lets `similar_phrase_scan.py` and future audits answer "has this exact class of error been seen before, anywhere in the repo?" without re-deriving it from git log archaeology. Low cost, high long-term value — this is the single highest-leverage structural addition.

**`automation/` — flag but don't over-build.**
GitHub Actions *must* physically live at `.github/workflows/` for GitHub to run them — you already have this working (`qb_health_check.py` at 03:00 UTC). Don't move it. `automation/` in the tree above is really just a documentation/reference pointer, not a new functional directory. If Phase 5 finds no second automation need beyond the existing health check, **skip creating this directory** — do not create structure speculatively. This is called out again in the Risk Register (over-engineering risk).

---

## 2. Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         RESPONSIBILITY MODEL                         │
└─────────────────────────────────────────────────────────────────────┘

CLAUDE CHAT (this environment)
  • Judgement calls: engineering accuracy, examiner-pattern fit, editorial voice
  • Planning, package design, review gates (Founder Architecture Review)
  • Reading textbooks/PDFs, drafting new Q&A content, drafting doc prose
  • One-off/ambiguous corrections requiring domain reasoning
  • Should NOT: run large repo-wide mechanical scans token-by-token,
    re-read entire repo every session to "rediscover" conventions

CLAUDE CODE (post-handover, see Section 6)
  • Mechanical, repeatable, spec-driven work: running tools/*.py,
    applying pre-approved correction patterns across many files,
    manifest sync, git operations, validation passes
  • Executes against docs/*.md and skills/* as its spec — does not
    need conversation history to know "how MIW does things"
  • Should NOT: make unreviewed engineering judgement calls about
    regulatory correctness — that's still routed back to Chat/Nixon

PYTHON UTILITIES (tools/)
  • Deterministic, testable, zero-judgement operations:
    tag-balance checks, JS syntax checks, manifest diffing,
    phrase-pattern scanning, JSON schema validation
  • Callable identically from Chat's bash tool or from Claude Code
  • Single responsibility per script — composable, not monolithic

GIT
  • Source of truth for history and diff review
  • CLI required for large files (QB4_A.html >100KB — web editor
    silently truncates); web editor acceptable for small edits only

REPOSITORY DOCUMENTATION (docs/)
  • Source of truth for "how things work" — read by humans, Claude
    Chat, and Claude Code alike
  • Never duplicated into CLAUDE.md; CLAUDE.md links out only

SKILLS (skills/)
  • Source of truth for "how to execute a specific recurring task"
  • Reusable across QB/Notes/WA/Timeline where the pattern genuinely
    repeats (e.g. correction protocol); NOT duplicated per content type
    unless the workflow materially differs

┌─────────────────────────────────────────────────────────────────────┐
│                          DATA FLOW EXAMPLE                            │
│                    "Correct a regulatory error"                      │
└─────────────────────────────────────────────────────────────────────┘

 Nixon reports error
        │
        ▼
 Claude Chat: engineering validation against primary source  ◄── judgement
        │
        ▼
 Claude Chat or Code: tools/repo_scan.py — find all instances ◄── mechanical
        │
        ▼
 Claude Chat: classify severity, decide correction wording    ◄── judgement
        │
        ▼
 Claude Code: apply fix across N files, bump footer version    ◄── mechanical
        │
        ▼
 tools/validate_html.py + validate_json.py                    ◄── mechanical
        │
        ▼
 tools/known_traps_update.py — append GREP anchor + changelog ◄── mechanical
        │
        ▼
 corrections/2026-XX-XX_<slug>.md — durable record             ◄── mechanical
        │
        ▼
 tools/manifest_update.py — sync qb_content_index.json         ◄── mechanical
        │
        ▼
 tools/git_commit.py — commit with structured message          ◄── mechanical
        │
        ▼
 Nixon pushes (or Claude Code pushes if authorised) → verify live
```

---

## 3. Package Dependency Diagram

```
                    ┌───────────────────────┐
                    │  PKG-0 Founder Review  │  (gate — this document)
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │  PKG-1 Repository      │
                    │  Audit                 │
                    └───────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                  │
    ┌─────────▼──────┐ ┌────────▼───────┐ ┌────────▼────────┐
    │ PKG-2 Core Docs │ │ PKG-3 Content  │ │ PKG-4 Git/Release│
    │ (PROJECT,       │ │ Standards Docs │ │ Workflow Docs    │
    │ ARCHITECTURE)   │ │ (QB/Notes/CS)  │ │                  │
    └─────────┬──────┘ └────────┬───────┘ └────────┬────────┘
              │                 │                   │
              └─────────────────┼───────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ PKG-5 Correction        │
                    │ Workflow Doc + Skill    │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ PKG-6 Python Utilities  │
                    │ — Validation tier       │
                    │ (validate_html/json)    │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ PKG-7 Python Utilities  │
                    │ — Scan/Report tier      │
                    │ (repo_scan, phrase_scan,│
                    │  repo_report)           │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ PKG-8 Python Utilities  │
                    │ — Mutation tier         │
                    │ (replace_engine,        │
                    │  manifest_update,       │
                    │  known_traps_update)    │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ PKG-9 Git Automation    │
                    │ (git_commit.py,         │
                    │  correction_summary.py) │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ PKG-10 Remaining Skills │
                    │ (repo-audit, batch-     │
                    │  correction, release-   │
                    │  preparation, etc.)     │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ PKG-11 corrections/     │
                    │ ledger bootstrap        │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ PKG-12 CLAUDE.md +      │
                    │ Claude Code Handover    │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼────────────┐
                    │ PKG-13 Workflow         │
                    │ Optimisation Report     │
                    │ (post-handover review)  │
                    └────────────────────────┘
```

Each package is independently committable — a hard fail or pause at any point leaves the repo in a working state, because no package modifies live QB/content files. Everything through PKG-13 is additive infrastructure.

---

## 4. Execution Roadmap — Implementation Packages

> Format per your spec. Times are Claude-session estimates, not calendar time.

---

### PKG-0 — Founder Architecture Review Gate
**Purpose:** Nixon reviews and approves this blueprint before any repo file is touched.
**Scope:** This document only.
**Deliverables:** Approved/amended blueprint; explicit go-ahead.
**Files created:** `MIW_Bootstrap_Blueprint.md` (this file — kept outside repo, or in `docs/` once approved, your call).
**Files modified:** None.
**Dependencies:** None.
**Validation checklist:**
- [ ] Repository structure approved or amended
- [ ] Package sequence approved or reordered
- [ ] `corrections/` addition accepted or rejected
- [ ] Claude Code handover point (PKG-6, see Section 6) accepted
**Acceptance criteria:** Nixon gives explicit written go-ahead referencing package numbers.
**Complexity:** N/A (review, not build)
**Est. time:** N/A
**Commit message:** N/A (not committed until approved, then commit as `docs: add approved bootstrap blueprint`)

---

### PKG-1 — Repository Audit
**Purpose:** Establish ground truth before writing any documentation, so docs describe what exists, not what we assume exists.
**Scope:** Read-only. Full repo tree, existing `.github/workflows`, existing skill files, manifest files, `known_traps.md`, `qb_health_check.py`.
**Deliverables:** `reports/audit/2026-XX-XX_repo_audit.md` — structure inventory, undocumented workflows, duplication found, technical debt list.
**Files created:** One audit report.
**Files modified:** None.
**Dependencies:** PKG-0 approval.
**Validation checklist:**
- [ ] Every top-level directory accounted for
- [ ] All GitHub Actions workflows listed with trigger/schedule
- [ ] All existing Python scripts inventoried with one-line purpose
- [ ] Every manifest file (`qb_content_index.json`, `notes_content_index.json`, `written_content_index.json`, `MEO_QB_master_v25.xlsx`) cross-checked against actual live files for drift
**Acceptance criteria:** Audit report reviewed by Nixon; no repo file changed.
**Complexity:** Medium (breadth, not difficulty)
**Est. time:** 1 session
**Commit message:** `docs(audit): add repository audit report`

---

### PKG-2 — Core Docs: PROJECT.md + ARCHITECTURE.md
**Purpose:** Single-responsibility top-level docs — what MIW is, and how the system is built.
**Scope:** `PROJECT.md` (business model, subscription tiers, target audience, examiner index concept). `ARCHITECTURE.md` (Razorpay→Redis→Brevo flow, auth gate mechanism, Vercel/Cloudflare hosting, GA4/Formspree IDs).
**Deliverables:** Two docs, cross-linked, no content duplication with skill files (skills own *workflow*, these own *what/why*).
**Files created:** `docs/PROJECT.md`, `docs/ARCHITECTURE.md`
**Files modified:** None.
**Dependencies:** PKG-1 (audit findings feed accuracy).
**Validation checklist:**
- [ ] No regulatory/content-editorial rules leaked into ARCHITECTURE.md (belongs in CONTENT_GUIDE.md, PKG-3)
- [ ] All env var names / service names verified against PKG-1 audit, not memory
- [ ] Cross-links to skills, not duplicated skill content
**Acceptance criteria:** A new Claude Code session reading only these two docs can explain the system without asking Nixon a clarifying question.
**Complexity:** Low
**Est. time:** 1 session
**Commit message:** `docs: add PROJECT.md and ARCHITECTURE.md`

---

### PKG-3 — Content Standards Docs
**Purpose:** Thin, authoritative pointers for QB/Notes/Cheat Sheet structure — detail stays in existing skill files, these docs prevent re-deriving structure from scratch each session.
**Scope:** `CONTENT_GUIDE.md` (shared rules: answer format, citation currency rule, examiner-pattern embedding, SEO/noindex rule). `QB_STANDARDS.md`, `NOTES_STANDARDS.md`, `CHEATSHEET_STANDARDS.md` — each links to its skill for full detail, states only what's cross-cutting or currently undocumented.
**Deliverables:** 4 docs.
**Files created:** `docs/CONTENT_GUIDE.md`, `docs/QB_STANDARDS.md`, `docs/NOTES_STANDARDS.md`, `docs/CHEATSHEET_STANDARDS.md`
**Files modified:** None.
**Dependencies:** PKG-1.
**Validation checklist:**
- [ ] Zero content duplicated verbatim from `miw-qb-production_SKILL_v3.md` etc. — links only
- [ ] Diagram placement rule (cheat sheets only, QB1_C grandfathered) explicitly stated once
- [ ] A/B file split rule (QB1–4 vs QB5+) stated once, in QB_STANDARDS.md only
**Acceptance criteria:** Each doc under ~1 page; a skill file changing its detail doesn't require editing these docs.
**Complexity:** Medium
**Est. time:** 1–2 sessions
**Commit message:** `docs: add content standards (QB, Notes, CheatSheet, shared guide)`

---

### PKG-4 — Git & Release Workflow Docs
**Purpose:** Codify the git/publishing quirks that currently live only in memory/skill prose (CLI-vs-web-editor 100KB limit, cache-busting, tarball fallback, session-based push authority).
**Scope:** `GIT_WORKFLOW.md`, `RELEASE_WORKFLOW.md`.
**Deliverables:** 2 docs.
**Files created:** `docs/GIT_WORKFLOW.md`, `docs/RELEASE_WORKFLOW.md`
**Files modified:** None.
**Dependencies:** PKG-1.
**Validation checklist:**
- [ ] States explicitly: Claude never pushes directly unless Nixon has authorised it for a given session — matches current practice
- [ ] Cache-busting pattern (`?nocache=$(date +%s)`) and tarball fallback documented with exact commands
- [ ] 9-step QB build workflow (ungated→gate→validate→health-check→manifest→index→xlsx→push→verify) captured as canonical sequence
**Acceptance criteria:** Nixon confirms this matches actual practice with zero corrections needed.
**Complexity:** Low
**Est. time:** 1 session
**Commit message:** `docs: add GIT_WORKFLOW.md and RELEASE_WORKFLOW.md`

---

### PKG-5 — Correction Workflow Doc + Skill
**Purpose:** This is the highest-value single document — it's invoked on every correction, currently reconstructed partly from memory each time.
**Scope:** `CORRECTION_WORKFLOW.md` (the 11-step SOP from Phase 6 of your original brief, refined against actual `known_traps.md` practice) + `skills/repo-correction-protocol/`.
**Deliverables:** 1 doc + 1 skill package (Purpose/Inputs/Outputs/Workflow/Validation/Failure conditions/Examples).
**Files created:** `docs/CORRECTION_WORKFLOW.md`, `skills/repo-correction-protocol/SKILL.md`
**Files modified:** None.
**Dependencies:** PKG-1, PKG-3 (needs content standards to reference).
**Validation checklist:**
- [ ] Explicitly encodes: verify against primary source before applying any external AI review correction (Gemini/Perplexity) — standing principle
- [ ] Explicitly encodes: negation-context false-positive pattern for health-checker
- [ ] References `corrections/` ledger (PKG-11) as the durable record destination
- [ ] Failure conditions section covers: str_replace silent failure on whitespace mismatch → Python offset-splice fallback
**Acceptance criteria:** Following this doc alone, a fresh session can execute a correction end-to-end without asking Nixon "what's the process."
**Complexity:** Medium
**Est. time:** 1–2 sessions
**Commit message:** `docs+skill: add correction workflow SOP and skill package`

---

### PKG-6 — Python Utilities: Validation Tier
**Purpose:** Deterministic checks that currently run ad-hoc or only inside `qb_health_check.py` — extract into standalone, composable tools.
**Scope:** `validate_html.py` (tag-balance via `HTMLParser` subclass, void-elements aware — already exists in some form, formalise it), `validate_json.py` (manifest schema/sync validation).
**Deliverables:** 2 scripts with `--help`, exit codes, and a `tests/` smoke test each.
**Files created:** `tools/validate_html.py`, `tools/validate_json.py`, `tools/tests/test_validate_html.py`, `tools/tests/test_validate_json.py`
**Files modified:** Possibly `qb_health_check.py` to import from `tools/` instead of inlining logic — **only if PKG-1 audit shows duplication; otherwise leave untouched** (existing automation is working — don't destabilise it for tidiness alone).
**Dependencies:** PKG-1.
**Validation checklist:**
- [ ] Runs identically from bash_tool (Chat) and from a plain terminal (Code) — no hidden environment assumptions
- [ ] Non-zero exit on failure, machine-parseable output
- [ ] Tested against a known-good and a known-bad QB file
**Acceptance criteria:** `python tools/validate_html.py meoclass1/QB1_A.html` returns pass/fail with line numbers.
**Complexity:** Medium
**Est. time:** 1–2 sessions
**Commit message:** `tools: add validate_html.py and validate_json.py`

> **This is the earliest sensible Claude Code handover point — see Section 6.**

---

### PKG-7 — Python Utilities: Scan/Report Tier
**Purpose:** Read-only repo-wide analysis tools that replace expensive manual tarball-and-grep sessions.
**Scope:** `repo_scan.py` (generic pattern/phrase search across all HTML with file:line output), `similar_phrase_scan.py` (fuzzy dedup — formalises the WhatsApp-question dedup logic already used manually), `repo_report.py` (structure/stats summary, feeds audit reports).
**Deliverables:** 3 scripts.
**Files created:** `tools/repo_scan.py`, `tools/similar_phrase_scan.py`, `tools/repo_report.py`
**Files modified:** None.
**Dependencies:** PKG-6 (shares validation helpers/conventions).
**Validation checklist:**
- [ ] `repo_scan.py` supports the negation-context awareness flagged in `known_traps.md` (regex + context window, not naive grep)
- [ ] `similar_phrase_scan.py` checks against both manifest JSON and xlsx rows, matching existing dedup rule
- [ ] All three tools read-only — no file mutation possible
**Acceptance criteria:** A correction's "repo-wide scan" step (Phase 6, step 3) runs in one tool call instead of a multi-step tarball fetch.
**Complexity:** Medium–High (negation-context logic is the hard part)
**Est. time:** 2 sessions
**Commit message:** `tools: add repo_scan.py, similar_phrase_scan.py, repo_report.py`

---

### PKG-8 — Python Utilities: Mutation Tier
**Purpose:** The only tools permitted to write to content/manifest files — kept separate and reviewed more carefully than read-only tools.
**Scope:** `replace_engine.py` (scoped find/replace with dry-run mode, offset-splice fallback for whitespace-mismatch cases), `manifest_update.py` (syncs `qb_content_index.json`/notes/written manifests), `known_traps_update.py` (appends GREP anchor + changelog entry in the established format).
**Deliverables:** 3 scripts, each with mandatory `--dry-run` default (mutation requires explicit `--apply`).
**Files created:** `tools/replace_engine.py`, `tools/manifest_update.py`, `tools/known_traps_update.py`
**Files modified:** None directly (these tools modify content later, not during this package).
**Dependencies:** PKG-6, PKG-7.
**Validation checklist:**
- [ ] Dry-run is the default mode for all three — mutation is opt-in, never accidental
- [ ] `replace_engine.py` tested against a case that previously triggered `str_replace` silent failure
- [ ] `manifest_update.py` output validated against `validate_json.py` (PKG-6) automatically
**Acceptance criteria:** Running any tool with no flags never modifies a file.
**Complexity:** High (this tier carries real risk — see Risk Register)
**Est. time:** 2–3 sessions
**Commit message:** `tools: add replace_engine.py, manifest_update.py, known_traps_update.py (dry-run default)`

---

### PKG-9 — Git Automation Utilities
**Purpose:** Standardise commit messages and correction summaries so history stays searchable.
**Scope:** `git_commit.py` (structured commit message builder — type(scope): summary, matching this roadmap's own commit-message convention), `correction_summary.py` (generates the `corrections/` ledger entry, PKG-11).
**Deliverables:** 2 scripts.
**Files created:** `tools/git_commit.py`, `tools/correction_summary.py`
**Files modified:** None.
**Dependencies:** PKG-8.
**Validation checklist:**
- [ ] `git_commit.py` never force-pushes, never pushes without explicit flag matching Nixon's session-level authorisation
- [ ] Commit message format matches conventions used throughout this roadmap
**Acceptance criteria:** Generated commit messages require no manual editing for standard corrections.
**Complexity:** Low–Medium
**Est. time:** 1 session
**Commit message:** `tools: add git_commit.py and correction_summary.py`

---

### PKG-10 — Remaining Skills
**Purpose:** Fill out the skill set for the remaining reusable workflows not covered by PKG-5.
**Scope:** `skills/repo-scan/`, `skills/qb-html-editing/`, `skills/notes-editing/`, `skills/engineering-validation/`, `skills/git-workflow/`, `skills/manifest-update/`, `skills/known-traps-update/`, `skills/repo-audit/`, `skills/batch-correction/`, `skills/release-preparation/`.
**Deliverables:** 10 skill packages, each thin — most will primarily reference `docs/` + `tools/`, with the skill layer adding only "when to trigger" and "how to sequence."
**Files created:** 10 `skills/*/SKILL.md` files.
**Files modified:** None.
**Dependencies:** PKG-2 through PKG-9 (skills reference all of them).
**Validation checklist:**
- [ ] No skill duplicates content already in `docs/` — skill = trigger + sequence + tool references only
- [ ] `batch-correction` explicitly builds on `repo-correction-protocol` (PKG-5) rather than re-deriving it
- [ ] Each skill's "reusable across future projects" candidacy noted (per your design principle) — flag which ones are MIW-specific vs genuinely portable
**Acceptance criteria:** Each skill triggers correctly per its own description when tested against a sample request.
**Complexity:** Medium (volume, not difficulty — consider splitting into 2–3 sub-packages if reviewed one at a time)
**Est. time:** 2–3 sessions
**Commit message:** `skills: add remaining repository workflow skills`

---

### PKG-11 — Corrections Ledger Bootstrap
**Purpose:** Backfill a `corrections/` entry for the most significant known corrections already in `known_traps.md`, establishing the format going forward.
**Scope:** `corrections/README.md` (format spec), 2–3 backfilled entries for the highest-value existing traps (e.g. A.1185(33)→A.1206(34), MS Act 1958→2025).
**Deliverables:** README + sample entries.
**Files created:** `corrections/README.md`, `corrections/2025-XX-XX_a1185-superseded.md` (dated per original correction if known, else marked "backfilled").
**Files modified:** None.
**Dependencies:** PKG-5, PKG-8.
**Validation checklist:**
- [ ] Format is greppable by `repo_scan.py`
- [ ] Backfilled entries clearly marked as retrospective, not claiming false historical precision
**Acceptance criteria:** Format approved by Nixon as the going-forward standard.
**Complexity:** Low
**Est. time:** 1 session
**Commit message:** `docs: bootstrap corrections/ ledger with format spec and backfilled entries`

---

### PKG-12 — CLAUDE.md + Claude Code Handover Package
**Purpose:** The actual handover artifact — single entry point, links only, no inlined content.
**Scope:** `docs/CLAUDE.md` per your Phase 8 spec (overview, structure, required docs, skills, tools, workflow order, principles, quality standards — all as links).
**Deliverables:** 1 doc + a short "first Claude Code session checklist."
**Files created:** `docs/CLAUDE.md`
**Files modified:** None.
**Dependencies:** All prior packages (this is the capstone — it links to everything).
**Validation checklist:**
- [ ] Every link resolves to an existing file
- [ ] Zero inlined substantive content — links only, per your explicit instruction
- [ ] A dry-run: hand this single file to a fresh Claude Code session and confirm it can locate everything else unassisted
**Acceptance criteria:** Nixon can open a brand-new Claude Code session, point it at `docs/CLAUDE.md`, and it correctly identifies workflow order without further prompting.
**Complexity:** Low
**Est. time:** 1 session
**Commit message:** `docs: add CLAUDE.md as Claude Code entry point`

---

### PKG-13 — Workflow Optimisation Report (Post-Handover Review)
**Purpose:** Retrospective — now that infrastructure exists, measure actual token/time savings vs. estimates, identify remaining manual work worth automating, decide if anything in this roadmap was over-built.
**Scope:** Review only. No new tools unless a clear, validated gap is found.
**Deliverables:** `reports/audit/2026-XX-XX_workflow_optimisation_review.md`.
**Files created:** 1 report.
**Files modified:** Potentially trims unused skills/tools if PKG-10 over-produced (honest self-audit).
**Dependencies:** All prior packages, plus real usage data (run for a few weeks post-PKG-12 before doing this).
**Validation checklist:**
- [ ] Compares actual vs. estimated token/time savings (Section 5 below) with real session data
- [ ] Flags any skill/tool unused since creation as a candidate for removal
**Acceptance criteria:** Nixon reviews and decides what, if anything, gets pruned or extended.
**Complexity:** Low
**Est. time:** 1 session
**Commit message:** `docs: add workflow optimisation review`

---

## 5. Token Optimisation Analysis

| Repeated cost today | Cause | Fix (package) | Est. saving |
|---|---|---|---|
| Re-deriving QB HTML structure/CSS conventions each session | Convention lives in skill prose, re-read in full each time it's touched | PKG-3 thin docs + existing skills stay as detail tier | Moderate — mainly reduces *ambiguity-driven* re-reads, not base skill load |
| Manual tarball fetch + grep for "has this error appeared elsewhere" | No searchable correction history | PKG-7 (`repo_scan.py`) + PKG-11 (ledger) | High — replaces multi-turn fetch/scan with one tool call |
| Re-explaining git CLI-vs-web-editor 100KB truncation quirk | Not documented, lives in memory | PKG-4 (`GIT_WORKFLOW.md`) | Low per-instance, but eliminates a recurring correction-of-Claude moment |
| `str_replace` silent failures on large whitespace-mismatched blocks, requiring retry | No standard fallback tool | PKG-8 (`replace_engine.py`) | Moderate–High — each failure currently costs a full retry round-trip |
| Manifest drift between `qb_content_index.json` / xlsx / live files | Manual, session-dependent updates | PKG-8 (`manifest_update.py`) + PKG-6 (`validate_json.py`) | High — prevents entire classes of "why doesn't the site match the manifest" debugging sessions |
| Re-deriving "what's the correction SOP" each time | Partial reconstruction from memory each session | PKG-5 (`CORRECTION_WORKFLOW.md`) | High — this is the single most frequently repeated workflow in the project |
| Repo-wide health check duplication logic split between `qb_health_check.py` and ad-hoc Claude checks | Two implementations of similar validation | PKG-6 (shared `validate_html.py`) | Moderate — mainly reduces divergence risk, not raw tokens |

**Honest caveat:** most of these savings are *variance reduction* (fewer failed attempts, fewer clarifying round-trips) rather than raw base-token reduction on a successful first pass. Do not oversell this — measure it properly in PKG-13 rather than assuming the estimates above hold.

---

## 6. Claude Code Readiness & Handover

**Earliest sensible handover point: after PKG-6 (Validation Tier).**

Reasoning:
- Before PKG-1/2, there is no stable spec for Claude Code to execute against — it would be working from conversation memory, defeating the purpose of this whole bootstrap.
- PKG-6 is the first package that produces something *mechanically verifiable by a script*, not requiring engineering judgement. That's the natural boundary between "Chat does this" and "Code can do this."
- PKG-7 and PKG-8 (scan/mutation tiers) are good *early* Claude Code tasks specifically — well-specified, testable, low ambiguity — better suited to Code's execution style than Chat's conversational style.
- PKG-5 (Correction Workflow doc) should still be **drafted in Chat**, because it encodes judgement calls (e.g., "verify against primary source before applying external AI corrections") that need domain reasoning to write correctly, even though *executing* it later can be Code.
- PKG-10 (Skills) is mixed: skill *content* judgement stays in Chat; skill *file scaffolding* could be handed to Code once PKG-6–9 exist as reference patterns.
- PKG-12 (CLAUDE.md) marks full handover readiness — after this, routine corrections and batch work should default to Claude Code, with Chat reserved for: new content authoring, ambiguous engineering judgement, and periodic architecture reviews (PKG-13 and beyond).

**Recommendation:** Run PKG-1 through PKG-6 in Chat. Pilot PKG-7 in Claude Code as a test of handover readiness before committing PKG-8–13 to Code. If the pilot reveals gaps (e.g., Code lacking repo context it needs), fix the gap in `docs/CLAUDE.md` before proceeding, rather than reverting to Chat by default.

---

## 7. Risk Register

| Risk | Category | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| Documentation duplicates skill file content, drifts out of sync over time | Documentation | High | Medium | Enforce "docs = what/why, skills = how/when, one line stating this rule at top of every doc/skill" (already built into PKG-2–PKG-10 checklists) |
| Mutation-tier tools (`replace_engine.py`, `manifest_update.py`) introduce a bug that corrupts a live QB file or manifest | Architectural/Workflow | Medium | High | Mandatory dry-run default (PKG-8), `validate_html.py`/`validate_json.py` run automatically post-mutation, never auto-push — Nixon or explicit `--apply` + `--push` gate |
| Over-engineering: 10 skills + 10 tools built (Phase 4/5 of original brief) before real usage proves they're needed | Over-engineering | Medium | Medium | PKG-13 retrospective explicitly checks for unused artifacts; consider splitting PKG-10 and doing only PKG-5's skill first, deferring the rest until PKG-6–9 tools exist and prove their shape |
| `automation/` directory created speculatively with no second automation need beyond existing health-check Action | Over-engineering | Medium | Low | Explicitly deferred in Section 1 — do not create until a real second automation need is found |
| Claude Code operates without the judgement guardrails currently applied manually in Chat (e.g. "never blindly apply external AI review corrections") | Workflow | Medium | High | These guardrails must be explicit, machine-readable statements in `CORRECTION_WORKFLOW.md` (PKG-5) — not left as tacit Chat-only knowledge |
| `corrections/` ledger becomes a second source of truth that drifts from `known_traps.md` | Maintenance | Medium | Medium | PKG-11 explicitly defines: `known_traps.md` = current-state reference (what to check for), `corrections/` = historical ledger (what happened and when) — different purposes, cross-linked, not duplicated |
| Manifest sync tooling (PKG-8) built against current `qb_content_index.json` schema, breaks silently if schema evolves | Maintenance | Low | Medium | `validate_json.py` (PKG-6) should assert schema shape explicitly, failing loudly rather than silently on drift |
| Large roadmap causes scope creep — packages balloon during implementation despite this plan | Architectural | Medium | Medium | Each package's "Scope" section is a hard boundary; anything discovered mid-package that's out of scope gets logged as a new candidate package, not absorbed |
| Founder Architecture Review (PKG-0) skipped under time pressure, implementation starts on unapproved plan | Workflow | Low (you've explicitly built the gate in) | High | This document exists specifically to prevent that — PKG-1 dependency is hard-gated on PKG-0 sign-off |

---

## 8. Prioritised Implementation Order (Summary)

1. **PKG-0** — Founder Architecture Review *(you are here)*
2. **PKG-1** — Repository Audit
3. **PKG-2, PKG-3, PKG-4** — Core/Content/Git docs (can run in parallel sessions, no interdependency between them)
4. **PKG-5** — Correction Workflow (highest standalone value)
5. **PKG-6** — Validation tools *(Claude Code pilot candidate starts here)*
6. **PKG-7** — Scan/Report tools
7. **PKG-8** — Mutation tools *(highest risk tier — most scrutiny)*
8. **PKG-9** — Git automation
9. **PKG-10** — Remaining skills *(consider splitting into 2–3 sub-packages given volume)*
10. **PKG-11** — Corrections ledger bootstrap
11. **PKG-12** — CLAUDE.md handover artifact
12. **PKG-13** — Workflow optimisation retrospective (run after real usage, not immediately)

---

## Open Questions for Founder Review

1. Should `docs/CLAUDE.md` and this blueprint itself live in the repo (`docs/`) or stay external to it? Recommendation: once approved, commit it — it's exactly the kind of "how we decided to build this" record the repo should retain.
2. PKG-10 is the largest single package by volume (10 skills). Split into sub-packages (e.g., correction-related skills vs. content-editing skills vs. audit/release skills) for easier review, or keep as one?
3. Should `automation/` be dropped from the structure entirely until a second real need appears, rather than listed as planned-but-empty?
4. Confirm: no package in this roadmap touches a live QB/Notes/WA content file. Correct — this is intentional, so the entire bootstrap can be reviewed and merged without any content-correctness risk. Content corrections continue via the existing manual workflow until PKG-5 supersedes it.
