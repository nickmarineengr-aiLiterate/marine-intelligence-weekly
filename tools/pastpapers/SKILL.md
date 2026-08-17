---
name: miw-solvedqp-correction-enrichment
version: 1.0
updated: 2026-08-16
description: >
  Decision-first workflow for correcting or enriching an ALREADY-PUBLISHED solvedQP answer.
  Load whenever the task is to fix a solved answer, add material to one, compare candidate or
  coaching notes against the corpus, act on a defect found during unrelated work, or decide
  whether something learned from a later paper belongs in an earlier one.
  This skill decides WHETHER and WHAT to change before anything is edited. It does NOT author
  new papers. New-paper written-QP production is governed by the protocol set indexed at
  meoclass1/pastpapers/docs/PRODUCTION_PROTOCOL_INDEX.md — start there, not here.
---

# SolvedQP Correction & Enrichment Review — Skill v1

## 0. What this skill is for

An existing, published solved answer is already correct enough to have shipped. The default
outcome of a review is therefore **`NO_CHANGE`**, and every other outcome has to be argued for.

This is a **decision skill first, editing skill second**. Most of it runs before a single file is
opened. Its job is to stop five specific failure modes this corpus has actually experienced:

| Failure mode | What it looks like |
|---|---|
| Uncontrolled answer growth | Every review adds prose; nothing is ever cross-linked or declined |
| False enrichment | Material added because it exists, not because the stem asks for it |
| Temporal contamination | Today's law retrofitted into a paper sat before it |
| Recurrence error | Two same-numbered questions assumed identical when the examiner widened one |
| Provenance error | "We hold no licensed copy" used to mean "we have not verified the text" |

## 1. Trigger

Invoke when asked to:

- correct or enrich an existing solvedQP answer
- compare candidate / coaching / third-party notes against solved answers
- apply new true-source material to a solved answer
- decide whether material from a later paper should propagate to an earlier one
- act on a factual or regulatory defect noticed during some other task

Do **not** invoke for authoring a new paper. That is a different, heavier workflow.

## 2. Governance this sits under

This skill does not restate governance. Read the owner document when its subject applies:

| Subject | Authority |
|---|---|
| **Producing a NEW written paper** (not this skill) | `meoclass1/pastpapers/docs/PRODUCTION_PROTOCOL_INDEX.md` and the protocol set it indexes |
| Learning architecture — five modes, Exam Plan, `answer_route`, subpart marks | `meoclass1/pastpapers/docs/PASTPAPER_PRODUCTION_PROTOCOL.md` §6 |
| What a correction is, how it moves, Founder gates, commit policy | `docs/CORRECTION_WORKFLOW.md` |
| Engineering principles (esp. P4 Verify Before Trust) | `docs/ENGINEERING_PRINCIPLES.md` |
| Product state, open items, restart instructions | `meoclass1/pastpapers/docs/CURRENT_STATUS.md` |
| QA and handover expectations | `meoclass1/pastpapers/docs/QA_AND_HANDOVER_PROTOCOL.md` |
| True-source build priorities | `docs/TRUE_SOURCE_PRIORITY_BACKLOG.md` |
| Learning-quality triage | `docs/SOLVEDQP_LEARNING_QUALITY_TRIAGE.md` |

**Never hard-code the build command from memory.** Read `CURRENT_STATUS.md` for the current
canonical publish command. At the time of writing it is `python tools/pastpapers/run_toolchain.py
--publish`, and a bare/default build is **not** the pre-commit gate — it produces an unpublished
variant. Confirm before relying on it.

## 3. Mandatory read order — before comparing any prose

Read, in this order, and do not skip to the answer text:

1. the question stem, **verbatim**
2. every subpart
3. marks / weighting
4. the complete existing answer
5. `question_delta`
6. `recurrence_adjudication`
7. donor relationships (`reused_from`, `reuse_evidence`, `reuse_tier`)
8. `cross_links`
9. temporal metadata (sitting date, any reverify flags)
10. `sources`, `unresolved`, `provenance_summary`

> **A recurrence hit is not proof that two questions ask the same thing.**
> Two papers can carry the same question number and near-identical opening words while one
> deliberately widens a limb. The recurrence metadata records that; the prose does not. A review
> that compares answer text before reading `recurrence_adjudication` and `question_delta` will
> conclude the answers should match, and will be wrong.

## 4. Classification — choose exactly one

| Outcome | Meaning |
|---|---|
| **`CORRECTION`** | Factually, technically or legally wrong; stale **for the sitting date**; internally contradictory; wrong instrument, edition or unit; or misleading enough to cost marks or teach the wrong concept. Normally high priority. |
| **`ENRICHMENT`** | Not wrong, but missing material that materially improves scoring, coverage, understanding, sequence, recall, CE relevance, or the ability to complete a limb the stem actually asks for. **Must earn its place.** |
| **`CROSS_LINK_ONLY`** | Another solved answer already carries the concept properly. Duplicating it would bloat the target. Prefer discoverability over duplication. |
| **`REVIEW`** | Value is plausible but stem relevance, jurisdiction, authority, recurrence relationship or exam value is unclear, or the answer is already large. Do **not** implement automatically. |
| **`NO_CHANGE`** | Already correct, sufficiently complete, historically right for its sitting, and properly scoped. **This is the default.** |

"More information exists" is never sufficient for `ENRICHMENT`.

## 5. Hard gates

Each gate can independently stop the change.

### 5.1 Temporal integrity

Ask: **what was correct on the examination sitting date?**

Later law, amendments, code editions, circulars or industry practice are **not** retrofitted into
an older paper. Typical traps: a statute enacted but not commenced; a transition such as SIRE 2.0;
a later IMO amendment; a changed interest benchmark; a convention entering into force afterwards.

Label deliberately:

- **`HISTORICAL_CURRENT`** — correct for the sitting
- **`CURRENT_NOW`** — correct today

An answer may legitimately carry both **if clearly labelled**. `CURRENT_NOW` must never silently
overwrite `HISTORICAL_CURRENT`. Some traps also run *backwards* — an answer can be wrong by citing
something too old for its sitting.

### 5.2 Source authority

| Rank | Source |
|---|---|
| 1 | MIW true-source object already carrying primary verification |
| 2 | Official instrument / issuing body |
| 3 | Authoritative national administration or official implementation source |
| 4 | Authoritative reproduction where primary access is unavailable |
| 5 | High-quality secondary source |
| 6 | Candidate / coaching notes — **discovery leads only** |

**Candidate notes are never authority.** Another solvedQP is never authority by itself: a donor
answer is evidence of corpus *intent*, not evidence that the proposition is *true*.

### 5.3 True-source first

For any significant regulation, convention, code, legal, numeric or edition/version correction,
check MIW true-source first.

If solvedQP would carry a verified correction that true-source does not yet encode, record a
**`TRUE_SOURCE_GAP`**. The downstream layer must not become permanently more authoritative than
the source layer.

But do **not** block an urgent downstream factual correction because a true-source package is
incomplete, once primary authority is established. Instead: correct downstream safely → register
the true-source repair → close the gap promptly.

### 5.4 Keyword collision

A text hit is a **hypothesis, not corroboration**. The same term routinely denotes different
institutions, instruments or contexts. Before treating a match as support: read the whole matched
question, inspect surrounding context, establish jurisdiction and instrument, and confirm the same
concept is actually meant. Crude keyword sweeps invent false ancestry.

### 5.5 Stem relevance and exam value

Every `ENRICHMENT` candidate must pass all of:

- **Scoring** — a realistic additional mark, or protection against losing one
- **Understanding** — explains a causal, technical or legal relationship the candidate needs
- **Recall** — improves ability to reproduce the answer under exam conditions
- **Stem fit** — the question actually asks for it
- **Exam time** — the candidate can realistically write it
- **Duplication** — not already adequately covered in the same answer
- **Cross-link alternative** — linking would not serve better than more prose

Reject anything whose justification is only: *interesting, current, related, more detailed, or
found in another answer*.

### 5.6 Provenance and source-holdings discipline

Never collapse these into one another:

| State | Means |
|---|---|
| `SOURCE_HELD` / `SOURCE_NOT_HELD` | Whether a copy is in our possession |
| `PRIMARY_TEXT_VERIFIED` / `PRIMARY_TEXT_NOT_VERIFIED` | Whether the wording was actually read and checked |
| `SECONDARY_REPRODUCTION_VERIFIED` | Verified via an authoritative reproduction |
| `REPRODUCTION_RIGHTS_ESTABLISHED` / `..._NOT_ESTABLISHED` | Whether we may republish it |

*"We hold no licensed copy"* must not be used to mean *"we have not verified the text"* — they are
different claims and can have opposite truth values. A source can be unreadable while held (an
image-only scan), or verified while not retained (read, hashed, not stored).

Provenance statements also **decay**: one that was true when written goes stale when later work
verifies the source. When touching a question, check whether its provenance block still holds.

### 5.7 Source-text / verbatim policy

The principle is **not** "avoid all matching wording". It is: *preserve legal and technical
accuracy while respecting source rights and publication policy.*

Exact wording is appropriate for official titles, defined terms, numerical requirements, units,
benchmarks, dates, short operative phrases, and legal tests where paraphrase weakens meaning. Do
not distort a phrase such as `first banking day` to reduce textual overlap.

Substantial continuous reproduction is a different question and follows the applicable copyright,
licence and public/private evidence policy. Where public verbatim publication is restricted:
preserve exact evidence privately, publish precise MIW-authored propositions, and retain evidence
IDs, hashes and provenance.

MIW may later create authorised consolidated editions where broader reproduction rights exist, so
never encode a permanent assumption that verbatim source text can never be published.

**No word-count threshold is the definition of correctness.** Treat any overlap metric as a review
trigger; classify what it surfaces rather than rewriting to satisfy it.

## 6. Proposal before implementation

Unless correcting a clear high-risk factual defect under an already-authorised maintenance
workflow:

```
DISCOVERY → AUDIT → CLASSIFY → PROPOSAL → FOUNDER REVIEW → IMPLEMENT → VALIDATE
```

Allowed decisions: `APPROVE_CORRECTION`, `APPROVE_ENRICH`, `CROSS_LINK_ONLY`, `REVIEW`,
`NO_CHANGE`.

A proposal states: target QP and question · sitting date · exact stem requirement · the gap or
defect · proposed change · preferred insertion point · authority relied on · temporal constraint ·
recurrence and donor questions checked · cross-link alternative considered · **what NOT to
import** · Founder approval required.

## 7. Implementation — only after approval

### 7.1 Minimal diff

**Correct the defect, not the neighbourhood.** Prefer the smallest technically complete change,
the existing schema, established cross-links, and deterministic generation. Avoid schema
invention, broad rewrites, unrelated modernisation and opportunistic cleanup. Any new out-of-scope
defect found becomes backlog, not scope creep.

### 7.2 Place the fact where candidates meet it

A fact is only useful where the candidate's canonical route leads them. Check, where relevant:
answer body · `answer_route` · scoring points · critical numbers · regulation/source block ·
traps · recall layer · cross-links.

Do not add a fact only to a long model answer the route never reaches — and do not blindly
duplicate it into every layer. Update the **minimum semantic set** needed for consistency. A
derived layer must never be more categorical than the verified answer.

## 8. Validation

If a canonical spec changed, run the publish-mode toolchain named by current governance (§2).
Check, as applicable: JSON parsing · schema · IDs · donors · recurrence relationships ·
cross-links · deterministic artifacts (byte-identical regeneration) · temporal assertions ·
source/provenance consistency · `git diff --check` · generated, public and gated surfaces · **no
unrelated artifact drift**.

Zero artifact drift on a full publish build is also positive evidence that a field never reaches a
shipped surface.

## 9. Final gate before commit

- inspect every changed file; classify each as canonical / generated / report
- prove zero unrelated paths
- **read the whole edited question after patching**, not just the diff
- semantic before/after review: did meaning change as intended, and only as intended?
- fetch before push; no force
- **verify the active credential matches the target repository** — this workstation carries more
  than one GitHub identity, and the wrong active account fails with a 403 that looks like an
  expired login but is not. Never hard-code credentials or tokens.

## 10. Output contract

Report to Founder:

1. **Classification** — one of the §4 outcomes, with reasons
2. **Authority** — what was relied on, and its rank under §5.2
3. **Temporal finding** — `HISTORICAL_CURRENT` / `CURRENT_NOW`, and the sitting-date test
4. **Recurrence check** — which donors and related questions were read
5. **What was deliberately not imported**, and why
6. **Files changed** — or `0`
7. **Validation** — exact results, including honest pre-existing failures
8. **Backlog raised** — any out-of-scope finding, and where it was registered
