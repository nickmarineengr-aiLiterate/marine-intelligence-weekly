# AI Session Handover
**Repository:** nickmarineengr-aiLiterate/marine-intelligence-weekly
**Prepared:** 2026-07-30
**Status:** Bridges active bootstrap work between AI sessions. Not permanent governance. Superseded by `docs/CLAUDE.md` once that package is reached.

---

## 1. Repository Overview

**Purpose:** Marine Intelligence Weekly (MIW) — a maritime newsletter and subscription platform (`marineintelligenceweekly.com`), centered on an MEO Class 1 oral exam preparation product (`meoclass1/`), plus associated content (timeline, ecosystem map, archive, GHG/decarbonisation tracking). The repository also co-hosts an unrelated product, `RulesApp/`, as a sibling directory.

**Current development phase:** Pre-implementation infrastructure bootstrap. No `docs/`, `skills/`, `tools/`, `templates/`, or `corrections/` directories exist in the repository yet. The only repository-level engineering artifacts committed so far live under `reports/`.

**Current architectural maturity:** Architecture is frozen (flat top-level structure: `docs/`, `skills/`, `templates/`, `reports/`, `corrections/`, `tools/`, alongside existing content directories, unchanged). Governance is frozen (Engineering Principles + 5 planned ADRs). An Implementation Contract governs execution. None of these four governing documents are yet committed to the repository itself — see Section 4.

---

## 2. Repository Status

- **Branch:** `main`
- **Working tree:** Clean aside from one pre-existing untracked directory, `Claude skill/`, unrelated to this bootstrap.
- **Approved repository documents:** None yet under a formal `docs/` structure. Two reports exist under `reports/`, both committed (see Section 3).
- **Write mechanism:** Local-First Repository Workflow — local `git commit` + `git push origin main` via Claude Desktop/Code. The GitHub connector's write path (`create_or_update_file`) is confirmed non-functional (403, cause undetermined) and is **not** part of the active execution path; it remains available for read-only inspection.

---

## 3. Recently Completed Packages

**PKG-1 — Repository Audit.** Complete, committed, verified.
- `reports/audit/2026-07-30_repo_audit.md` — commit `e8cd853`
- `reports/packages/PKG-1_COMPLETION_SUMMARY.md` — commit `0359cbe`
- Surfaced real, evidence-based findings: non-functional `.gitignore` (missing leading dot), two competing Notes manifests (`notes-content-index.json` vs `notes_content_index.json`), `RulesApp/` confirmed co-located rather than external, duplicated legacy issue content (root vs `archive/`), duplicate `SQ/` file pairs, an undocumented/missing `api/verify-session.js`. Full detail in the audit report itself — not restated here.

No other package has reached Commit.

---

## 4. Draft / Pending Work

**Not yet approved or committed:**

- **PKG-1.5 — Engineering Principles.** Content fully drafted (14 principles, Purpose, Relationships, Reserved-for-ADR sections). **Blocked on two open Founder decisions:** (1) target path — instruction specified `repository/ENGINEERING_PRINCIPLES.md`, frozen architecture specifies `docs/ENGINEERING_PRINCIPLES.md`; (2) final sign-off on the 14 principles as drafted, including two flagged near-overlaps (Explicit Relationships vs. Traceability; Deterministic Tooling vs. Reproducibility).
- **This handover document itself.**
- **Four core governance/planning documents exist only outside the repository** — produced in-session, never committed: the Bootstrap Blueprint, the Governance Review, the Architecture Freeze Review, and the Implementation Contract. This is a real gap worth the next engineer's attention: per Principle 1 (Repository First, itself still in draft), nothing is truly "decided" until it's in the repository — right now these four foundational documents exist only as session output, not as committed fact.

---

## 5. Outstanding Issues

**Technical:**
- `.gitignore` committed without its leading dot — non-functional, ignore patterns not applied.
- Two competing Notes manifest files, undetermined which is authoritative.
- `api/verify-session.js`, referenced in prior project context, not found in current `api/` listing.
- `api/check-db.js` and `api/migrate-users.js` — purpose undocumented.
- Duplicated legacy content between repository root (`index17.html`–`index30.html`) and `archive/` (issues 17–22 only, byte-identical).
- Three duplicate file pairs in `SQ/` (prefixed vs. unprefixed), not yet content-diffed.

**Architectural:**
- None open at the structural level (frozen, no active dispute). The only open architectural item is the PKG-1.5 path discrepancy noted in Section 4, which is a compliance question against the freeze, not a request to reopen it.

**Founder decisions:** see Section 8 — kept separate from the technical/architectural list per your instruction, not duplicated here.

---

## 6. Repository Reading Order

For a new engineer with no conversation history, in this order:

1. `reports/audit/2026-07-30_repo_audit.md` — ground truth on actual repository state.
2. `reports/packages/PKG-1_COMPLETION_SUMMARY.md` — what's actually been completed and verified.
3. This document — current state and immediate priorities.

No `docs/CLAUDE.md` exists yet to serve as the intended long-term entry point (planned for a later package). Until it exists, this handover is the closest equivalent.

---

## 7. Current Priorities

1. Resolve the PKG-1.5 path decision and principle sign-off (Section 4) — blocks that package's Commit.
2. Once resolved: commit PKG-1.5, then produce the recommended ADR Dependency Map before drafting ADR-0001–0005 individually.
3. Decide whether to commit the four outside-repository planning documents (Section 4) into the repository, consistent with Principle 1 once approved.
4. Resume the numbered package sequence (core/content/git docs) once governance foundation work lands.

---

## 8. Founder Decisions Awaiting Review

- PKG-1.5 target path: `docs/ENGINEERING_PRINCIPLES.md` (per frozen architecture) vs. `repository/ENGINEERING_PRINCIPLES.md` (per most recent instruction).
- Final approval of the 14 drafted Engineering Principles, including the two flagged near-overlap pairs.
- Six audit Founder Questions from PKG-1 (gitignore history, manifest authority, SQ duplicate purpose, `verify-session.js` status, `check-db.js`/`migrate-users.js` purpose, `archive/` migration intent) — none blocking, all still open.
- Whether to formally commit the Blueprint, Governance Review, Architecture Freeze Review, and Implementation Contract into the repository itself.
- This handover document's own content and its commit.

---

## 9. Handover Notes

- Do not use the GitHub connector for any write operation — confirmed non-functional, Local-First is the sole approved commit mechanism.
- Follow the Implementation Contract's lifecycle exactly: Founder Review precedes Commit, without exception, for every package.
- Before creating any new document, check whether an existing one already owns the concern — this repository's own audit found real, costly duplication from skipping that check historically.
- Treat `RulesApp/` as a separate, pre-existing product co-located in this repository — not part of this bootstrap's scope.
- Nothing above should be treated as settled until you find it committed in the repository — several foundational documents currently exist only in prior session output, not in `main`.
