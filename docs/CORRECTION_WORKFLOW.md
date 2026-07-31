# Correction Workflow

**Status:** Draft (v0.1) — pending Founder review
**Governs:** How corrections, defects, engineering improvements, repository inconsistencies, and future user feedback are processed, from the point they're identified to the point they're verified live.
**Date:** 2026-07-31
**Package:** PKG-5 — the first operational (non-governance) document produced under this bootstrap.

---

## Purpose and Relationship to Governance

This document operationalizes `docs/ENGINEERING_PRINCIPLES.md` P4 (Verify Before Trust) and connects to the mutation-safety rules already stated in `reports/governance/IMPLEMENTATION_CONTRACT.md` §4 ("Reserved for the Implementation Contract" in the Principles document, since those rules are Contract-owned, not restated there). It does not restate the Contract's package lifecycle (§2) or its Chat/Code responsibility boundary (§6–7) — it applies them to one specific, recurring kind of work: corrections. Per P2 (Single Responsibility), this document owns *what a correction is and how it moves through the repository*; the Contract continues to own *how any package, including a correction, is executed and committed*.

---

## Scope

**In scope:** factual/content corrections to any live repository content (MEO Class 1 QB/oralnotes material, articles, and similar), repository inconsistencies and technical debt (of the kind catalogued in `reports/audit/2026-07-30_repo_audit.md`), governance-document inconsistencies (of the kind resolved during PKG-1.5, committed as `00d093c`), and future user/subscriber feedback.

**Out of scope:** new content authoring (a correction fixes something already published; it does not introduce a new topic), architectural changes (governed by `MIW_Architecture_Freeze_Review.md` and `IMPLEMENTATION_CONTRACT.md` §11 — a correction may not add, remove, or rename a top-level directory), and anything requiring a new ADR (per `docs/ENGINEERING_PRINCIPLES.md`'s Reserved for ADR table — a correction applies an already-settled decision, it does not make a new one).

---

## Entry Points

A correction can be identified through any of the following, each evidenced by how this repository already surfaces problems:

1. **Subscriber/candidate-flagged error.** `meoclass1/known_traps.md`'s existing entries record this pattern directly — e.g., Entry 11: "Flagged by a candidate (Rathesh) via annotated screenshot correction."
2. **Automated health-check scan.** `.github/workflows/qb-health-check.yml` runs `meoclass1/qb_health_check.py` daily (03:00 UTC / 08:30 IST) and on manual dispatch, emailing findings via Brevo SMTP.
3. **Audit or review findings.** `reports/audit/2026-07-30_repo_audit.md`'s Technical Debt table is itself a live list of entry points (e.g., the duplicate Notes manifests, still unresolved as of `docs/BOOTSTRAP_BASELINE.md`).
4. **Discovered during unrelated work.** Per `IMPLEMENTATION_CONTRACT.md` §2 (Implementation stage): "Discoveries outside scope are logged as candidate future packages... not absorbed silently." A correction discovered mid-package becomes its own entry here, not a scope-creep addition to the package that found it.

---

## Classification of Corrections

Three categories, each evidenced by an actual precedent already in this repository:

| Category | Description | Precedent | Requires primary-source verification (P4)? |
|---|---|---|---|
| **Content correction** | A factual, regulatory, or examiner-pattern error in published QB/oralnotes/article material | `meoclass1/known_traps.md`, all 11 current entries; commit `b942de9` (Form E fire-fighting equipment fix) | **Yes, always** |
| **Repository correction** | A structural, technical-debt, or automation issue not tied to a specific factual claim | `reports/audit/2026-07-30_repo_audit.md` Technical Debt table; commit `63e0b3c` (`.gitignore` fix) | No — verified against repository state directly, not a primary source |
| **Governance correction** | An inconsistency inside a governance document itself (a stale status line, a broken cross-reference) | Commit `00d093c` (three governance documents marked Approved) | No — verified against the governing Founder decision, not a primary source |

Severity within any category uses the same vocabulary already established in `reports/audit/2026-07-30_repo_audit.md`'s Technical Debt table — **Critical / Moderate / Low** — rather than a new scale, per P2 (no parallel taxonomies for the same concept).

---

## Validation Process

Follows `IMPLEMENTATION_CONTRACT.md` §5 (Validation Policy) directly, with one addition specific to content corrections:

1. For **content corrections**: verify against a primary source before anything else (P4). `meoclass1/known_traps.md`'s own header states the reference-priority discipline this repository already follows for regulatory content — a claim is not corrected on the strength of an external AI review or a single unverified report.
2. Scope the search: a single wrong claim is rarely isolated. Check whether the same error pattern appears elsewhere in the affected content tree before treating one instance as the whole fix — this repository already builds this expectation into its own health-check mechanism (see Evidence Requirements, below, on the `GREP:` field).
3. Review every modified file in full, not by diff summary alone, for anything touching content or manifests (`IMPLEMENTATION_CONTRACT.md` §5, item 3).
4. Review cross-references — a correction that updates `meoclass1/known_traps.md` or a manifest must leave both internally consistent; a broken cross-reference is a validation failure, not a follow-up item (§5, item 4).
5. Any failure at any step returns the correction to Implementation. Validation failures are never committed "to fix later" (§5).

---

## Evidence Requirements

For a **content correction**, evidence must include:

- The primary source consulted (per the reference-priority order this repository already follows in practice: IMO conventions/codes > SOLAS/MARPOL/STCW > IACS UR/UI > class rules > DG Shipping/DGMA > manufacturer docs > ISO/IEC — reconstructed here from the pattern already visible across `meoclass1/known_traps.md`'s entries, e.g. Entry 6's Merchant Shipping Act 2025 citation, Entry 9's MEPC session citation).
- A `GREP:` classification, matching `meoclass1/known_traps.md`'s existing format exactly: either an exact wrong phrase safe to auto-scan, or `SKIP` when "the wrong version is a general term that's also legitimately used correctly" (`meoclass1/known_traps.md`, header) — this is the repository's own already-evidenced negation-context safeguard; it is not a new mechanism introduced here.
- Every file touched, so the correction's `known_traps.md` entry and manifest update stay traceable to the same evidence.

For **repository** and **governance corrections**, evidence is the cited repository state itself (a `git ls-files`/`git status`/direct file read showing the inconsistency) — no external primary source applies.

---

## Founder Review Gates

Per `IMPLEMENTATION_CONTRACT.md` §6–8:

- Chat verifies content corrections against primary sources before proposing them (§6) — Chat never applies an unverified correction.
- Code, once it exists in this repository's workflow, never decides whether a correction should be applied — only executes one already judged correct in Chat (§7).
- Any uncertainty — about primary-source interpretation, about whether an error is isolated or repository-wide, about severity — stops the correction and escalates per §8 (Escalation Policy): state the uncertainty, lay out the options, request Founder review, wait for an explicit decision. Do not guess.
- Founder Review is a required lifecycle stage (§2) for every correction, without exception, matching every other package type — a correction is not a lesser-scrutiny category of change.

---

## Implementation Process

1. **Planning** — confirm the correction's classification (above) and scope; restate what will change before touching any file (`IMPLEMENTATION_CONTRACT.md` §2).
2. **Implementation** — apply exactly the scoped fix. For content corrections: update the content file(s), then `meoclass1/known_traps.md` (new numbered entry, following the existing 11 entries' style — short title, what was wrong, correct position, files affected, who flagged it and when, a `GREP:` line), then the relevant manifest (`meoclass1/qb_content_index.json`'s `recently_updated` array and `generated`/`generated_by` fields, mirroring the structure already present in that committed file).
3. **Validation** — per the Validation Process above.
4. **Founder Review** — per Founder Review Gates above.
5. **Commit** — per Commit Policy below.
6. **Verification** — per Verification below.
7. **Report** — one short note: what was corrected, what was touched, what's now available for the next package (`IMPLEMENTATION_CONTRACT.md` §2).

---

## Verification

Two layers, both already evidenced in this repository rather than newly proposed:

- **Passive, ongoing:** `.github/workflows/qb-health-check.yml` re-scans daily against every `GREP:`-classified `known_traps.md` entry — a corrected claim that regresses (e.g., via a later, unrelated edit) has a real chance of being caught automatically, not just at correction time.
- **Active, at correction time:** matching the Contract's standard Verification stage as already practiced throughout this bootstrap (`git log`/`git diff` confirming the pushed state matches what was reviewed) — applied here to confirm the content file, the `known_traps.md` entry, and the manifest update all landed together and match what Founder Review approved.

---

## Commit Policy

Follows `IMPLEMENTATION_CONTRACT.md` §4 directly. One real precedent already exists in this repository's history, predating this document: commit `b942de9` ("Fix: Form E does not list fire-fighting equipment (QB3_A Q15 full rewrite + cheat sheet, QB8_A, QB8_B); known_traps.md Entry 17; manifest updated") touched four content files, `known_traps.md`, and the manifest **in one commit** — content fix, standing-record update, and manifest sync landing together, traceably. This workflow adopts that shape as the standard, not a one-off.

`IMPLEMENTATION_CONTRACT.md` §4 additionally requires: granular, non-squashed history specifically for anything touching `corrections/` or `known_traps.md` — "what changed and why, step by step" has diagnostic value here precisely because content corrections carry regulatory-accuracy risk. Message format follows the Contract's `type(scope): summary` convention; a content correction's summary should name what was wrong, matching the descriptive style of `b942de9` rather than a generic "fix content" message.

---

## Audit Trail

Three layers, all already real and committed, not newly introduced:

1. **`meoclass1/known_traps.md`** — the durable, human-readable record of what was wrong and why, in the exact numbered-entry format already used for its current 11 entries.
2. **`meoclass1/qb_content_index.json`'s `recently_updated` field** — a machine-readable, dated record of what changed, confirmed present in the manifest's actual current structure (`manifest_version`, `generated`, `generated_by`, `total_questions`, `total_files`, `recently_updated`, `files`).
3. **Git history itself** — per `docs/ENGINEERING_PRINCIPLES.md` P1 (Repository First), the commit log is the ultimate audit trail; nothing above substitutes for it, each only makes it easier to search for a specific class of prior correction without reading raw diffs.

**Not yet available:** `MIW_Bootstrap_Blueprint.md` §1 and `MIW_Bootstrap_Governance_Review.md` §9 both describe a future `corrections/` directory as a fourth, structured ledger (one dated record per correction, independent of `known_traps.md`'s changelog style) — this is `corrections/` PKG-11a's deliverable, per `docs/BOOTSTRAP_BASELINE.md`'s Remaining Open Packages list, and does not exist yet. This workflow does not reference it as available. Once PKG-11a lands, this document will need a corresponding update — logged here as a known forward dependency, not implemented speculatively now (per P5, No Speculative Structure).

---

## Completion Criteria

A correction is not complete until every item below is true, adapting `IMPLEMENTATION_CONTRACT.md` §3 (Definition of Done) to this specific category of work:

- [ ] For content corrections: verified against a primary source, source cited in the `known_traps.md` entry.
- [ ] All affected files identified and fixed — not just the first instance found (Validation Process, item 2).
- [ ] `meoclass1/known_traps.md` updated, in its existing format, where the correction is a content correction.
- [ ] Manifest (`meoclass1/qb_content_index.json` or the relevant equivalent) updated where content changed.
- [ ] `git status` clean — no scratch or partial files remain.
- [ ] Commit lands as one logically complete unit, per Commit Policy.
- [ ] Verification confirms the pushed state matches what Founder Review approved.
- [ ] Report delivered.

---

## Terminology Note

This document deliberately reuses existing repository vocabulary rather than introducing new terms for the same concepts: "Critical/Moderate/Low" (from the audit's Technical Debt table, not a new severity scale), "Founder Review" and the eight lifecycle stage names (from `IMPLEMENTATION_CONTRACT.md` §2, unchanged), "primary source" and "verify-before-trust" (from `docs/ENGINEERING_PRINCIPLES.md` P4, unchanged), and `GREP:`/`SKIP` (from `meoclass1/known_traps.md`'s own existing format, unchanged). No conflicting or parallel workflow exists elsewhere in the committed repository as of this document's authoring — `docs/BOOTSTRAP_BASELINE.md`'s Repository Structure section confirms `docs/` contained only `ENGINEERING_PRINCIPLES.md` and itself before this document.
