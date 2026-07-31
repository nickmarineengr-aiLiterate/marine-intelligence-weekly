# Corrections Ledger

**Status:** Operational repository standard — binding on every correction from this point forward, not a discussion draft.
**Governs:** The format, location, and lifecycle of every file in `corrections/`.
**Date:** 2026-07-31
**Package:** PKG-11a — Repository Corrections Ledger (format specification only; backfilling historical entries is PKG-11b, deferred).

---

## Purpose

`corrections/` is the durable, greppable record of what was corrected in this repository, when, and why — independent of any single content file's own footer and independent of `meoclass1/known_traps.md`'s changelog. Its purpose, stated directly in `reports/governance/MIW_Bootstrap_Blueprint.md` §1, is to answer a question no other artifact in this repository can answer on its own: *has this exact class of error been seen before, anywhere in the repository?* — without re-deriving the answer from `git log` archaeology every time.

---

## Repository Philosophy

`corrections/` exists because of `docs/ENGINEERING_PRINCIPLES.md` P1 (Repository First): a correction that isn't recorded here didn't happen, as far as any future session is concerned. It complements, and does not duplicate, `meoclass1/known_traps.md` — per P2 (Single Responsibility), `known_traps.md` owns *current-state reference* (what to check for before publishing new content), and `corrections/` owns *historical ledger* (what happened and when). A future engineer or Claude session should never have to guess which of the two to consult; this document states the split explicitly so neither drifts into the other's job.

---

## Why Corrections Are Preserved Instead of Overwritten

A correction record, once committed, is **never deleted and never rewritten** — even after the error it describes is fixed, even if a later correction supersedes it. Three reasons, each already established elsewhere in this repository's governance rather than invented here:

1. **`reports/governance/IMPLEMENTATION_CONTRACT.md` §4** prohibits force-push and history rewriting without exception: "If a commit needs correcting, commit a correction on top. History is not rewritten." The same discipline applies to the *record* of a correction as to the *code* — a corrections entry is corrected forward (a new, dated entry noting the earlier one was incomplete or wrong), never edited in place to read as if it were always right.
2. **`reports/governance/MIW_Bootstrap_Governance_Review.md` §2** states the same principle for ADRs: "Never delete an ADR, even if superseded — supersession is itself a valuable record." A corrections entry is the same kind of artifact — its value is partly in existing at all, as evidence a class of error occurred and was caught.
3. **The ledger's stated purpose (above) requires persistence.** "Has this exact class of error been seen before" cannot be answered by a ledger that quietly removes old entries once they're no longer current.

---

## Directory Structure

Flat, by design, for now:

```
corrections/
├── README.md          (this file — the standard)
├── TEMPLATE.md         (placeholder-only template — see below)
└── YYYY-MM-DD_<short-slug>.md   (one file per correction)
```

`reports/governance/MIW_Bootstrap_Governance_Review.md` §7 already anticipated that a flat directory "will eventually want date-based subdirectories (`corrections/2027/`) or an index" at high volume, and explicitly declined to build that now: "Not worth solving now — flag as a known future refactor, don't build it preemptively." Per `docs/ENGINEERING_PRINCIPLES.md` P5 (No Speculative Structure), this document does the same — flat structure stands until a real volume of entries demonstrates the need for subdirectories.

---

## Naming Convention

`corrections/YYYY-MM-DD_<short-slug>.md`

- `YYYY-MM-DD` — the date the correction was **committed**, not the date the underlying error was originally introduced (which may be unknown or irrelevant).
- `<short-slug>` — kebab-case, a few words, matching the descriptive-filename convention already used elsewhere in this repository (e.g. `reports/audit/2026-07-30_repo_audit.md`).
- One file per correction. A correction touching multiple content files is still one ledger entry, listing every file affected in its metadata (below).

---

## Required Metadata

Every entry opens with the following fields, in this order. Fields marked *(content only)* apply only to content corrections (see Classification, below) and are omitted for repository or governance corrections.

| Field | Description |
|---|---|
| **Date** | `YYYY-MM-DD`, matches the filename |
| **Classification** | `Content` / `Repository` / `Governance` — the same three-way classification defined in `docs/CORRECTION_WORKFLOW.md` |
| **Severity** | `Critical` / `Moderate` / `Low` — the same scale already used in `reports/audit/2026-07-30_repo_audit.md`'s Technical Debt table, not a new one |
| **Summary** | One line, imperative or descriptive, naming what was wrong |
| **What Was Wrong** | The actual error, stated plainly |
| **Correct Position** | What is actually true, or what the repository now does instead |
| **Primary Source** *(content only)* | The source verified against, per `docs/ENGINEERING_PRINCIPLES.md` P4 (Verify Before Trust) |
| **Files Affected** | Every file touched by the fix |
| **Related `known_traps.md` Entry** *(content only)* | Cross-reference to the corresponding numbered entry |
| **Related Manifest Update** *(content only)* | Whether/how `meoclass1/qb_content_index.json` (or equivalent) was updated |
| **Flagged By** | Which entry point surfaced this (per `docs/CORRECTION_WORKFLOW.md`'s Entry Points: subscriber/candidate, automated health-check, audit/review finding, or discovered during unrelated work) |
| **Commit** | The git commit hash that applied the fix |

---

## Severity Classification

Reused, not redefined, from `reports/audit/2026-07-30_repo_audit.md`'s Technical Debt table:

- **Critical** — actively wrong information live to subscribers, or a repository-integrity issue with immediate risk (e.g. the kind of finding that produced the `.gitignore` fix, PKG-1.6).
- **Moderate** — an error or inconsistency with real but bounded impact, not urgent.
- **Low** — a documentation or clarity gap, no functional or factual impact.

---

## Lifecycle of a Correction

Maps directly onto `docs/CORRECTION_WORKFLOW.md`'s Implementation Process — this section states only what happens to the *ledger entry itself* at each stage, not the whole workflow:

1. **Planning / Implementation** — the ledger entry is drafted alongside the fix, not after it.
2. **Validation** — per `docs/CORRECTION_WORKFLOW.md`'s Validation Process; the entry's metadata is checked against this document's Required Metadata table before proceeding.
3. **Founder Review** — the ledger entry is reviewed as part of the correction, not separately.
4. **Commit** — the ledger entry, the content fix (if any), the `known_traps.md` update (if any), and the manifest update (if any) land **in the same commit**, per `docs/CORRECTION_WORKFLOW.md`'s Commit Policy and its real precedent, commit `b942de9`.
5. **Verification / Report** — as in `docs/CORRECTION_WORKFLOW.md`.

Once committed, an entry is permanent (see "Why Corrections Are Preserved," above) — there is no further lifecycle stage that edits it.

---

## Relationship to Governing Documents

Per `docs/ENGINEERING_PRINCIPLES.md` P2, this section states the relationship, not the content, of each governing document:

- **`docs/ENGINEERING_PRINCIPLES.md`** — P1 (Repository First) is why this ledger exists at all; P4 (Verify Before Trust) is why content corrections require a Primary Source field; P2 (Single Responsibility) is why this ledger and `known_traps.md` have distinct, non-overlapping jobs (see Repository Philosophy, above).
- **`docs/CORRECTION_WORKFLOW.md`** — defines the process this ledger's entries are a byproduct of: Classification (reused directly here), Evidence Requirements (the source of the Primary Source field), Entry Points (the source of the Flagged By field), and Audit Trail, which named `corrections/` as "Not yet available" and a known forward dependency — this document is that dependency, now fulfilled.
- **`reports/governance/IMPLEMENTATION_CONTRACT.md`** — §4's granular-history and no-squash requirement already names `corrections/` explicitly; §4's force-push/history-rewriting prohibition is the direct basis for "Why Corrections Are Preserved," above.

---

## Examples of Correction Records

Illustrative only — not real historical entries. Real backfilled entries are PKG-11b's deliverable (`reports/governance/MIW_Bootstrap_Governance_Review.md` §4: "gated behind PKG-8"), not created by this package.

**Example — Content correction** (`corrections/2026-08-01_example-content-correction.md`):

```markdown
**Date:** 2026-08-01
**Classification:** Content
**Severity:** Moderate
**Summary:** [Example] QB2_A cited a superseded resolution number.
**What Was Wrong:** [Example] Text cited Resolution A.1185(33) as current.
**Correct Position:** [Example] A.1185(33) is superseded by A.1206(34) for PSC procedures.
**Primary Source:** [Example] IMO resolution text, cross-checked against known_traps.md Entry 5.
**Files Affected:** [Example] meoclass1/QB2_A.html
**Related known_traps.md Entry:** [Example] Entry 5
**Related Manifest Update:** [Example] meoclass1/qb_content_index.json, recently_updated
**Flagged By:** [Example] Automated health-check scan
**Commit:** [Example] <commit-hash>
```

**Example — Repository correction** (`corrections/2026-08-01_example-repository-correction.md`):

```markdown
**Date:** 2026-08-01
**Classification:** Repository
**Severity:** Low
**Summary:** [Example] Duplicate SQ/ file pair confirmed identical, unprefixed copy removed.
**What Was Wrong:** [Example] SQ/index.html and SQ/SQ_index.html were byte-identical duplicates.
**Correct Position:** [Example] Single canonical file retained; duplicate removed.
**Files Affected:** [Example] SQ/index.html, SQ/SQ_index.html
**Flagged By:** [Example] Audit/review finding
**Commit:** [Example] <commit-hash>
```

---

## Archival Policy

Entries are never deleted (see "Why Corrections Are Preserved," above). The directory remains flat until a real volume of entries makes date-based subdirectories necessary — a known, explicitly deferred future refactor (`MIW_Bootstrap_Governance_Review.md` §7), not built speculatively now, per `docs/ENGINEERING_PRINCIPLES.md` P5.

---

## Validation Requirements

Before any correction entry is committed:

- Filename matches the naming convention exactly.
- Every applicable Required Metadata field is present (all fields for content corrections; the non-*(content only)* fields for repository/governance corrections).
- Severity uses one of the three established values — no new severity term.
- Classification uses one of the three values defined in `docs/CORRECTION_WORKFLOW.md`.
- Every cross-reference (`known_traps.md` entry, manifest update, commit hash) resolves to something that actually exists — a broken cross-reference is a validation failure, not a follow-up item, per `reports/governance/IMPLEMENTATION_CONTRACT.md` §5.
- The entry is committed in the same commit as the correction it records, per Lifecycle, above.

---

## Not Yet In Scope

Backfilling entries for corrections that predate this ledger (e.g. the corrections already recorded in `meoclass1/known_traps.md`'s 11 existing entries) is **PKG-11b**, explicitly deferred and gated behind PKG-8 (`reports/governance/MIW_Bootstrap_Governance_Review.md` §4). This package creates the standard only.
