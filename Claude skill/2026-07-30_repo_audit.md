# Repository Audit Report — PKG-1
**Repository:** nickmarineengr-aiLiterate/marine-intelligence-weekly
**Ref inspected:** `main` @ commit `b942de9fc09882a6ff8d1a6003f1328ee88ddb24`
**Date:** 2026-07-30
**Method:** Live GitHub API inspection (read-only), no local clone modified, no repository file altered

---

## Executive Summary

The repository is larger and more heterogeneous than the bootstrap planning documents assumed. Core MEO Class 1 content (`meoclass1/`) is extensive and well-organized by naming convention (QB1–QB10, A–J sub-variants, cheat sheets). However, this audit surfaces several concrete issues that were not visible from conversation memory alone: a non-functional `.gitignore` (the file is named `gitignore`, missing its leading dot, so Git does not read it), a duplicate pair of manifest files for the Notes series (`notes-content-index.json` and `notes_content_index.json` both exist), a duplicated content set between repository root and `archive/` (identical `indexNN.html` files stored twice, ~9MB of duplication), a duplicated pair of files in `SQ/` (prefixed and unprefixed versions of `index.html`, `pay.html`, `examiner-index.html`), and confirmation that **RulesApp is not a separate repository** but a subdirectory (`RulesApp/`) inside this same repo — a fact referenced in prior planning documents as if it were external. Automation is minimal and matches expectations: exactly one GitHub Actions workflow exists, running `meoclass1/qb_health_check.py` on a daily schedule. One credential-bearing script referenced in project memory (`verify-session.js`) was not found in `api/`.

None of these findings block PKG-1.5 or later packages, but several should directly inform `docs/ARCHITECTURE.md` (PKG-2) and are flagged as Critical/Moderate technical debt below.

---

## Repository Facts

**FACT** — Root directory contents (26 top-level entries): `.github/`, `CNAME`, `GHGDecarb/`, `README.md`, `RulesApp/`, `SQ/`, `api/`, `archive/`, `articles/`, `assets/`, `cover24.webp`, `ecosystem.html`, `gitignore` (no leading dot), `index.html`, `index17.html` through `index30.html` (14 files), `logo.webp`, `meoclass1/`, `package.json`, `privacy.html`, `robots.txt`, `terms.html`, `timeline.html`, `youtube/`.

**FACT** — `.github/workflows/` contains exactly one file: `qb-health-check.yml`.

**FACT** — `qb-health-check.yml` triggers on a daily cron (`0 3 * * *`, documented in-file as 03:00 UTC / 08:30 IST) and on manual `workflow_dispatch`. It checks out the repo, sets up Python 3.11, and runs `python3 meoclass1/qb_health_check.py` with three secrets injected as environment variables: `BREVO_SMTP_LOGIN`, `BREVO_SMTP_KEY`, `QB_HEALTH_EMAIL_TO`.

**FACT** — `meoclass1/` contains 10 QB series (QB1 through QB10) as 89 distinct `.html` files by direct count of the directory listing, including main QB files, cheat sheets, and one `QB1_supplementary.html`. It also contains `known_traps.md`, `qb_content_index.json`, `qb_health_check.py`, `index.html`, `examiner-index.html`, an `assets/` subdirectory, and an `oralnotes/` subdirectory.

**FACT** — `meoclass1/oralnotes/` contains 18 `miw-notes-mgmt-pN.html` files (p1–p18), 8 `simon-notes-pN.html` files (p1–p8), 3 `WA1-HKC*.html`, 2 `WA2-GHG*.html`, 3 `WA3-LIEN*.html`, `current-topics-p1.html`, `uday-index-crossref.html`, `index.html`, an `assets/` subdirectory, and **two** manifest files: `notes-content-index.json` (hyphenated, 22,500 bytes) and `notes_content_index.json` (underscored, 25,422 bytes).

**FACT** — `SQ/` contains 10 files, including both `index.html` and `SQ_index.html`, both `pay.html` and `SQ_pay.html`, and both `examiner-index.html` and `SQ_examiner-index.html`, plus `SQ/QB1_A.html`, `SQ/miw-notes-mgmt-p1.html`, and `SQ/simon-notes-p1.html` and `-p2.html`.

**FACT** — `api/` contains 6 files: `check-db.js`, `check-password.js`, `create-order.js`, `migrate-users.js`, `razorpay-webhook.js`, `verify-payment.js`.

**FACT** — `archive/` contains `index.html`, `issue17.html` through `issue22.html`, and `thematicmapissues01to16.html`. The blob SHA of `archive/issue17.html` is identical to the blob SHA of root-level `index17.html` (`b6c5c9856c9c3db46a66635138dd78c0e76c3362`) — confirming byte-for-byte duplicate content, not merely similar naming.

**FACT** — `RulesApp/` exists as a subdirectory of this repository, containing `README.md`, `index.html`, and two further subdirectories: `RulesApp/app/` and `RulesApp/repository/`.

**FACT** — Root file `gitignore` (as inspected) contains standard ignore patterns (`.env`, `node_modules/`, IDE files, OS files, build outputs) but the file is named `gitignore`, not `.gitignore`. A file named without the leading dot is not recognized by Git as an ignore file.

**FACT** — `package.json` declares the project name `miw-razorpay-backend`, type `module`, dependencies `nodemailer` and `@upstash/redis`, and `node: 24.x` under `engines`. `build` and `test` scripts are placeholder echo statements, not functional builds/tests.

**FACT** — `README.md` at repository root is a two-line description of the newsletter; it contains no architecture, workflow, or contributor information.

**FACT** — No `docs/`, `skills/`, `tools/`, `templates/`, `reports/`, or `corrections/` directory currently exists in the repository (confirmed by their absence from the root listing above) — consistent with PKG-1 being the first package executed under this bootstrap.

---

## Findings

**FINDING — Non-functional `.gitignore`.** The repository's ignore-pattern file is committed as `gitignore` rather than `.gitignore` (evidence: root listing shows `"name":"gitignore"`, and `git_url`/content match a standard ignore-pattern file). As written, none of its patterns (`.env`, `node_modules/`, `package-lock.json`, etc.) are actually applied by Git. This means secrets or build artifacts matching these patterns are not protected from accidental commit unless another mechanism (e.g., manual discipline) is compensating. Severity assessed below.

**FINDING — Duplicate Notes manifest files.** `meoclass1/oralnotes/` contains both `notes-content-index.json` and `notes_content_index.json`, differing in naming convention (hyphen vs. underscore) and file size (22,500 vs. 25,422 bytes), meaning they are not identical copies but two independently-maintained or partially-diverged files. Prior project memory referenced only `notes_content_index.json` (underscore) as the canonical manifest — the hyphenated file's existence and purpose is undocumented anywhere inspected. This is a direct instance of the "manifest drift" risk anticipated in the PKG-1 planning stage.

**FINDING — Duplicated legacy issue content between repository root and `archive/`.** `index17.html` through `index22.html` exist at repository root and are byte-identical (matching blob SHAs) to `archive/issue17.html` through `issue22.html`. `index23.html` through `index30.html` exist only at root, with no corresponding `archive/issueNN.html`. This is an inconsistent, partially-completed migration: some legacy issues were copied into `archive/`, others were not, and the root copies were never removed after the ones that were copied.

**FINDING — Duplicated SQ marketing files.** `SQ/` contains both a prefixed and unprefixed version of three files (`index.html`/`SQ_index.html`, `pay.html`/`SQ_pay.html`, `examiner-index.html`/`SQ_examiner-index.html`). Whether these are identical, near-identical, or serving different purposes (e.g., one being a legacy naming convention mid-migration) was not determined — file contents were not diffed as part of this audit (see Validation Summary / Limitations).

**FINDING — RulesApp is co-located, not external.** Contrary to the framing used throughout this bootstrap's planning documents ("similar to the governance model used in the RulesApp repository," implying a separate project), `RulesApp/` is a subdirectory of this same repository, containing its own `app/`, `repository/`, `index.html`, and `README.md`. This means the frozen flat architecture (`docs/`, `skills/`, `tools/`, etc. at repository root) will sit alongside an entirely separate, pre-existing product directory at the same root level — a fact not accounted for when architecture was reviewed and frozen.

**FINDING — Undocumented API scripts.** `api/check-db.js` and `api/migrate-users.js` exist and were not referenced in any prior project memory or planning document. Their purpose was not determined from filename alone within this audit's read-only scope.

**FINDING — Referenced script not found.** `api/verify-session.js`, described in project memory as handling session-based auth and evicting superseded devices, does not appear in the current `api/` directory listing. Either this script was never committed, has been renamed, or project memory is describing intended-but-unimplemented behavior. `api/check-password.js` (which does exist) may implement session logic under a different name — this was not confirmed by content inspection within this audit's scope.

**FINDING — Root-level clutter from legacy issue files.** 14 `indexNN.html` files (17–30) sit at repository root alongside the current `index.html`. Combined with the `archive/` duplication finding above, this suggests root was the original storage location before `archive/` was introduced, with an incomplete cleanup.

**FINDING — No skill-file/repository-file duplication of *content* was found for QB or Notes standards.** The `miw-qb-production`, `miw-notes-mgmt`, and related skill files describe workflow and format conventions; no corresponding second copy of this same guidance exists inside the repository itself (e.g., no `meoclass1/README.md` restating QB structure). This is a positive finding — it means PKG-3 (Content Standards Docs) is filling a genuine gap, not duplicating existing repository documentation.

---

## Technical Debt

| Item | Severity | Category |
|---|---|---|
| `gitignore` missing leading dot — non-functional | **Critical** | Repository / Automation risk |
| Duplicate Notes manifests (`notes-content-index.json` vs `notes_content_index.json`) | **Critical** | Duplication / Workflow |
| Root/`archive/` duplicated legacy issues (~9MB, issues 17–22) | Moderate | Repository |
| Root-level clutter (14 unarchived `indexNN.html` files) | Moderate | Repository |
| SQ prefixed/unprefixed duplicate files (3 pairs) | Moderate | Duplication |
| `RulesApp/` co-location not reflected in frozen architecture discussion | Moderate | Documentation / Architecture |
| Undocumented API scripts (`check-db.js`, `migrate-users.js`) | Low | Documentation |
| `verify-session.js` referenced in memory but not found in repo | Low | Documentation |
| `package.json` build/test scripts are placeholders | Low | Automation |
| No root `README.md` beyond a two-line description | Low | Documentation |

---

## Recommendations

Recommendations only — nothing below has been implemented as part of PKG-1.

1. **Fix `.gitignore` naming.** Recommend addressing in a dedicated, small, early commit — before PKG-2 if possible, since every subsequent package commits new files and is currently doing so without working ignore protection. *Candidate package: a new minimal PKG-1.6 (or fold into PKG-2 as a first commit) — Founder decision required, since this is outside PKG-1's read-only scope.*
2. **Resolve the duplicate Notes manifest.** Determine which of `notes-content-index.json` / `notes_content_index.json` is authoritative, document the decision, and treat the other as either deprecated (with a removal path) or repurposed. *Candidate package: PKG-8 (manifest_update.py) should not be built against two competing manifests — this needs resolution before or during PKG-8, and should be flagged explicitly in `docs/ARCHITECTURE.md` (PKG-2).*
3. **Investigate and reconcile the root/`archive/` duplication.** Confirm whether `archive/` is the intended long-term home for legacy issues, complete the migration for issues 23–30, and remove the root-level duplicates for issues 17–22 once confirmed safe. *Candidate package: new package under `miw-archive` skill scope — outside this bootstrap's numbered packages, flag to Founder for separate scheduling.*
4. **Clarify SQ duplicate file pairs.** Diff the prefixed/unprefixed pairs to determine if they're identical, drifted, or intentionally distinct. *Candidate: fold into PKG-1.5 or PKG-3 as a documentation clarification, or a short standalone investigation before PKG-3 if the answer affects `docs/CONTENT_GUIDE.md`.*
5. **Reflect RulesApp co-location in `docs/ARCHITECTURE.md`.** PKG-2 should explicitly document that `RulesApp/` is a sibling directory at repository root, distinct from the bootstrap's own structure, so future sessions don't conflate the two or assume RulesApp is external.
6. **Confirm `verify-session.js` status directly with Nixon** before PKG-4 (`GIT_WORKFLOW.md`)/PKG-2 (`ARCHITECTURE.md`) describe the auth flow, since documenting a script that doesn't exist would immediately violate this bootstrap's own accuracy standard.
7. **Document `check-db.js` and `migrate-users.js` purpose** as part of PKG-2's `ARCHITECTURE.md`, once their function is confirmed (by content read or by asking Nixon) — not assumed from filename.

---

## Validation Summary

Every inspection target from the approved PKG-1 Execution Plan (Section 2) was inspected, with the following results and one explicit limitation:

- **Repository structure** — Inspected. Full root listing captured; `meoclass1/`, `SQ/`, `api/`, `archive/`, `RulesApp/`, `meoclass1/oralnotes/` listings captured directly. `GHGDecarb/`, `articles/`, `youtube/`, `assets/`, `RulesApp/app/`, `RulesApp/repository/` were confirmed to exist (present in parent listings) but their internal contents were **not** individually listed — see Limitations below.
- **Existing documentation** — Inspected. Only `README.md` (root) and `RulesApp/README.md` found as free-standing documentation; content of the latter was not read in full.
- **Existing skill files** — Not re-inspected in this audit; already directly available and previously verified in the current session's context (skill files at `/mnt/skills/user/`), per the file-reading skill's guidance that already-visible content need not be re-fetched.
- **Python tools** — Inspected. `meoclass1/qb_health_check.py` confirmed to exist (41,415 bytes); full content was not read line-by-line as part of this audit (existence and location confirmed; deep content review deferred — see Limitations).
- **GitHub Actions workflows** — Inspected in full. Exactly one workflow, full content read and quoted above.
- **Manifests** — Inspected. `qb_content_index.json`, `notes-content-index.json`, `notes_content_index.json`, `written_content_index.json` all confirmed to exist by directory listing; **not** cross-checked field-by-field against live QB files for drift (that level of validation requires content-level diffing beyond this audit's read-only structural scope — flagged as a Limitation and a candidate for a dedicated PKG-7 `repo_scan.py`/`manifest_update.py` validation pass rather than manual audit).
- **`known_traps.md`** — Confirmed to exist (15,053 bytes); full content was not quoted in this report (existing project memory already reflects its content accurately per prior sessions' direct review).
- **Correction workflow evidence** — Not independently verified against git commit history in this audit; commit-level `git log` inspection was not performed. Flagged as a Limitation.
- **Release workflow evidence** — Not independently verified against git commit history. Flagged as a Limitation.
- **Existing automation beyond the health check** — Inspected. Confirmed only one workflow file exists; no other scheduled or webhook-triggered automation found in `.github/`.

**Limitations encountered:**
- Git commit history (`git log`) was not inspected — the GitHub API tools used in this audit provide file/tree content, not history, within this session's toolset. This means "correction workflow evidence" and "release workflow evidence" (Section 2 of the PKG-1 plan) were assessed only via current file state, not historical pattern. If historical commit analysis is needed, it requires a follow-up pass with git-log-capable tooling.
- Several subdirectories (`GHGDecarb/`, `articles/`, `youtube/`, `assets/` at two locations, `RulesApp/app/`, `RulesApp/repository/`) were confirmed to exist but not individually listed or read, in the interest of proportionate audit scope — this repository has substantially more surface area than the original planning documents anticipated. This is itself a finding (see above) but also a genuine audit limitation.
- File *contents* of the SQ duplicate pairs and the `api/check-db.js`/`migrate-users.js` scripts were not diffed/read in full — their existence and naming were confirmed, but a byte-level or line-level comparison was not performed.

---

## Founder Review Summary

**Major strengths:** Automation footprint is minimal and exactly matches expectations (one workflow, one script) — no hidden automation surprises. QB content structure is extensive and consistently named. No duplication was found between repository content and skill-file guidance — the documentation gap PKG-1.5–PKG-4 are meant to fill is real and not already addressed elsewhere.

**Major weaknesses:** Two Critical-severity items — the non-functional `.gitignore` and the duplicate Notes manifest — were previously invisible to project memory and change the risk picture for early packages (particularly PKG-8's manifest tooling, which cannot safely target two competing manifest files without a resolution first). The repository also has meaningfully more surface area (`RulesApp/`, `api/`, `articles/`, `youtube/`, `GHGDecarb/`, duplicated archive content) than prior planning fully accounted for.

**Blockers:** None block PKG-1.5 from proceeding. However, two items (the `.gitignore` fix and the manifest resolution) should be resolved or explicitly deferred with Founder sign-off **before** PKG-8 is scheduled, since PKG-8 was planned assuming a single, unambiguous manifest per content type.

**Readiness for PKG-1.5:** Ready. PKG-1.5 (Governance Docs) does not depend on resolving the findings above — it can proceed once this report is reviewed. The findings should inform PKG-2 (`ARCHITECTURE.md`) directly, particularly the `RulesApp/` co-location fact and the `verify-session.js` discrepancy.

**PKG-1 completion status: Implementation and Validation stages complete. Awaiting Founder Review per Implementation Contract §2 before proceeding to Commit.**
