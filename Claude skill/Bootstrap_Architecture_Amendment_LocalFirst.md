# Bootstrap Architecture Amendment — Local-First Repository Workflow
**Status:** Proposed amendment, pending Founder approval
**Trigger:** Confirmed, reproducible GitHub connector write failure (403) during PKG-1 Commit stage; local Git and Claude Desktop filesystem writes confirmed healthy
**Scope:** Execution model only — does not touch repository structure, governance principles, or ADR-0001 through ADR-0005

---

## 1. Recommendation

**Yes — formally adopt the Local-First Repository Workflow.**

This is not a workaround adopted reluctantly under a broken tool. On engineering merits alone, Local-First is the stronger architecture for this bootstrap, and the current failure is simply what surfaced the fact that the original design leaned on a weaker path when a stronger one was already available.

**Reasoning:**

- **Fewer moving parts in the critical path.** `create_or_update_file` via the GitHub connector introduces a dependency on a third-party integration layer (the connector's own auth, its permission scope, its request translation to GitHub's REST API) sitting between "Founder approves" and "change lands in the repository." Local Git → `git push` removes that intermediate layer entirely: Claude Desktop writes to a filesystem it already has verified write access to, Git (a tool with decades of stability, already proven healthy per your own `git status`/remote checks) handles versioning, and `git push` is the single well-understood network operation — using the same credential path you already use for every manual push described in `docs/GIT_WORKFLOW.md`.
- **Consistency with already-adopted practice.** Your own memory record states corrections/edits made from Claude Desktop should happen via the local clone (`F:\marine-intelligence-weekly`), synced locally, then pushed — specifically to save tokens versus fetching over network. Local-First isn't a new pattern being introduced for this bootstrap; it's the bootstrap catching up to a workflow you'd already established elsewhere.
- **Governance and auditability are equal or better, not worse.** The Implementation Contract's lifecycle (Planning → Implementation → Validation → Founder Review → Commit → Verification → Report) doesn't reference *how* the commit happens, only that it happens after Founder Review and is verified afterward. A local `git commit` followed by `git push origin main` produces the exact same auditable commit history, hash, message, and diff as a connector-mediated write — Git doesn't distinguish "how" a commit was authored when you inspect `git log` later. Founder control is arguably *tighter* under Local-First, since Nixon's own machine executes or directly supervises the final `git push`, rather than trusting a remote connector's write scope.
- **Failure mode is more diagnosable.** The GitHub connector's 403 was, by my own analysis in the prior task, irreducibly ambiguous — I could not determine from available tooling whether it was a GitHub-side permission problem or a connector-side capability limitation. A local `git push` failure, by contrast, produces standard Git/SSH/HTTPS error output that is directly diagnosable (auth failure, network issue, rejected non-fast-forward, etc.) without a black-box intermediary.
- **Long-term maintenance.** The GitHub connector's permission model is now confirmed to be at least one source of fragility. Depending on it as the *sole* write path for 13 packages' worth of commits means every package inherits this same unresolved risk until (and unless) the connector's permissions are fixed. Local-First removes this as a dependency for the bootstrap's own progress, without requiring you to abandon the connector — it remains available for read operations (which work reliably) and can be revisited for writes later if desired.

**One caveat, stated plainly:** Local-First shifts the actual `git push` execution to Claude Desktop or to Nixon directly, not to this Claude Chat session. Claude Chat cannot itself touch the local filesystem or execute `git push` — that capability belongs to Claude Desktop/Claude Code. This has a direct consequence for the Migration Plan and PKG-1 Recommendation below.

---

## 2. Architecture Impact

Only documents genuinely affected by a change in *execution mechanism* — not structure, not governance:

- **`IMPLEMENTATION_CONTRACT.md`** — **Must update.** Section 4 (Commit Policy) and Section 7 (Claude Code Responsibilities) currently describe "push authority" abstractly ("Claude never pushes without explicit session-level authorization") without specifying *which* Claude surface performs the push or by what mechanism. This needs an explicit statement: commits are written and pushed via local Git through Claude Desktop/Claude Code (or Nixon directly), not via the GitHub connector's write API. The push-authorization principle itself doesn't change — only the mechanism is named.
- **`docs/GIT_WORKFLOW.md` (once it exists, PKG-4)** — **Must reflect this when written.** Since this document doesn't exist yet, there's no existing content to amend — but PKG-4 must now be planned to document Local-First as the canonical mechanism from the start, rather than documenting connector-based writes and later needing a correction.
- **`MIW_Bootstrap_Blueprint.md` (the original roadmap)** — **Minor update.** PKG-4's description implicitly assumed *some* push mechanism without specifying connector vs. local; no scope change to PKG-4 itself, but its "Deliverables" checklist item about cache-busting/tarball-fallback commands should note these remain valid for *verification* (confirming a push landed) regardless of which mechanism performed the push.

**Not affected, explicitly:**
- `MIW_Bootstrap_Governance_Review.md` — governance and structure are unchanged.
- `MIW_Architecture_Freeze_Review.md` — repository directory structure is unchanged; this amendment is purely about the mechanism that writes files into that structure.
- Any ADR (0001–0005) — none of the five encode a GitHub-connector-specific decision; the push-authority principle they support is preserved, just now named a specific mechanism.

---

## 3. Lifecycle Changes

Reviewing each of the Implementation Contract's eight stages against this amendment:

| Stage | Changes? | Detail |
|---|---|---|
| Planning | **Unchanged** | No mechanism dependency |
| Implementation | **Unchanged** | Content/file creation logic is identical regardless of how it's later committed |
| Validation | **Unchanged** | Tools run the same way against local files whether or not they're later pushed via connector or local git |
| Founder Review | **Unchanged** | Review happens before commit either way |
| **Commit** | **Changes** | Mechanism becomes: write file(s) to local working copy (via Claude Desktop/Code) → `git add` → `git commit` with the same message-format policy already defined in Contract §4 → `git push origin main`. The *policy* (message format, granularity, force-push prohibition, squash rules) is unchanged; only *who/what executes the push* changes. |
| **Verification** | **Changes slightly** | Verification already specified cache-busted fetch or `git log`/`git diff` as acceptable methods (Contract §2) — this becomes the primary verification method rather than one option among others, since there's no longer a connector-write-confirmation step to distinguish from repository state |
| Report | **Unchanged** | Report content and format are unaffected |
| Next Package | **Unchanged** | — |

**Net: one stage (Commit) changes its mechanism; one stage (Verification) narrows to its already-existing local-check method; six of eight stages are completely unaffected.**

---

## 4. Package Impact

Reviewing the 13-package roadmap for any package whose *scope* (not just mechanism) must change:

**No package requires a scope change.** Every package's Deliverables, Files created/modified, and Validation checklist are defined in terms of *what* gets created, not *how* it gets pushed. The only adjustment needed:

- **PKG-4 (Git & Release Workflow Docs)** — its Scope already includes documenting the actual push mechanism; this amendment simply determines *which* mechanism it documents (Local-First) rather than requiring new scope. No expansion, no reduction.
- All other packages (PKG-1.5 through PKG-13) — **no change.** They were never written assuming a specific push mechanism; Commit was always "per the approved commit policy," which this amendment refines rather than contradicts.

---

## 5. Migration Plan

**Objective: preserve all completed work, repeat nothing.**

1. **PKG-1's audit report and this session's governance/architecture/contract documents are not lost.** They exist in full in this conversation and can be written to the local filesystem exactly as already drafted — no rework, no re-drafting, no re-review. The content that already passed Founder Review stands as approved; only the delivery mechanism changes.
2. **Handoff point:** Since Claude Chat cannot itself write to the local filesystem or execute `git push`, the actual file-write-and-push step for already-approved content (the PKG-1 audit report, and once approved, this amendment itself) needs to happen via **Claude Desktop or Claude Code**, or **Nixon directly**, using the exact file content and paths already specified in this conversation.
3. **No re-validation needed for already-approved content.** PKG-1's Founder Review already approved the audit report's content; Local-First doesn't reopen that approval, it only changes how the already-approved bytes reach the repository.
4. **Going forward (PKG-1.5 onward):** Claude Chat continues to draft, and Claude Desktop/Code executes the local commit-and-push using the same Implementation Contract lifecycle, with Commit/Verification now explicitly meaning the Local-First mechanism.
5. **Connector left in place for reads.** No migration action needed for read operations — they continue to work and remain useful for verification (e.g., confirming a push landed, without needing a fresh local clone check every time).

**Nothing needs to be reimplemented. Nothing needs to be re-reviewed. Only the delivery step for already-approved content needs to move from "Claude Chat via connector" to "Claude Desktop/Code via local git."**

---

## 6. Recommendation on PKG-1

**A. Commit locally using Git — do not hold PKG-1 pending connector fix.**

Engineering reasoning:

- The content is already Founder-approved (per your own explicit review resolution in the prior task). Holding it hostage to an unrelated connector permission issue serves no purpose — the audit report's value doesn't depend on which mechanism wrote it to disk.
- Local Git is confirmed healthy (`git status`, remote configuration, branch sync all verified working per your own report) — there's no engineering reason to wait on a separate, currently-unresolved GitHub App/PAT permission investigation when a working path exists right now.
- Blocking PKG-1 indefinitely on the connector fix would violate the Implementation Contract's own Principle 4 ("every package leaves the repository in a working state") in spirit, if "working state" is held hostage to a dependency this amendment has just demonstrated isn't actually required.
- This is also directly consistent with your own "Approved → Commit, never leave a package open because of issues that belong elsewhere" principle from the PKG-1 Founder Review — the connector permission problem is exactly the kind of issue that belongs to a separate concern (connector configuration), not to PKG-1's own completion.

**Practical consequence:** the actual `git add / git commit / git push` for the PKG-1 audit report (and, once you approve it, the Package Completion Summary) needs to be executed via Claude Desktop/Code or by you directly — Claude Chat will supply exact file content and commit message, but cannot perform the local write/push itself.
