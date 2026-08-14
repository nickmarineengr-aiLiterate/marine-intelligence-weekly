# Engineering Principles — Critical Review

**Reviewing:** `docs/ENGINEERING_PRINCIPLES.md`, Draft v0.1 (commit `5b28190`)
**Reviewer stance:** Independent senior engineer, first exposure to this document, no authorship stake in it.
**Status:** Review only. `docs/ENGINEERING_PRINCIPLES.md` not modified. No v0.2 created. Nothing committed.
**Date:** 2026-07-31

---

## Executive Summary

Draft 1 is a competent, evidence-disciplined first pass — every claim is traceable to a cited repository document, nothing is invented, and the document is honest about its own incompleteness. But it has three real engineering problems, not just polish items: **two of the four near-overlap pairs its own predecessor evidence document (`ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` §5) flagged for resolution were carried into Draft 1 unresolved** (P1/P2, P4/P5); **two principles (P7, P8) are close enough to verbatim restatements of `IMPLEMENTATION_CONTRACT.md` rules that they arguably violate the document's own single-responsibility principle (P3) by existing at all**; and **one gap the evidence-gathering stage already identified and flagged for attention — the "repository must remain useful without Claude in the loop" concept — was not picked up during drafting**, despite being available in the same evidence base Draft 1 was built from. None of these are fatal. All three are fixable in a v0.2 without touching the document's underlying evidence discipline, which is sound and should be preserved.

---

## Overall Assessment

**Strengths:**
- Every principle traces to an actual quote or citation, not paraphrase-from-memory — this document does what it claims to do (evidence-only authoring) and does not smuggle in inferred content.
- The "Known Incompleteness" section is good engineering practice — it would have been easy to quietly present 10 principles as "the" replacement; instead the document states plainly that it falls short of the historical 14 and does not know what it's missing.
- Internal cross-referencing (Relationships fields, the document-level Relationships summary) is mostly accurate on inspection — see Overlap Analysis for the two places it understates rather than overstates the relationship.
- The Amendment Policy citing P9 against itself ("this is P9 applied to the document itself") is a genuinely good design choice — the document practices its own no-speculative-growth rule.

**Weaknesses:**
- Two evidenced-but-unresolved overlaps were carried forward rather than decided (see Overlap Analysis).
- Two principles (P7, P8) sit uncomfortably close to being restatements of Contract rules rather than distinct values — see Principle-by-Principle Review.
- One previously-flagged gap wasn't closed (see Gap Analysis).
- A real ambiguity in P2 was introduced by this document's own Draft status, unaddressed anywhere in the text (see P2 review and Special Attention Q1).

---

## Principle-by-Principle Review

### P1. Repository First — **KEEP**
Clear, foundational, directly evidenced (`MIW_Bootstrap_Governance_Review.md` §1, `IMPLEMENTATION_CONTRACT.md` §1 item 8). Weakness: it is not directly enforceable the way P3, P6, or P7 are — there's no concrete check a reviewer can run against "the repository is the source of truth." That's acceptable for a foundational principle (not every principle needs to be a gate check), but worth naming honestly rather than implying uniform enforceability across all 10.

### P2. Documentation Is Authoritative — **REVISE**
The underlying claim is well-evidenced elsewhere (Governance Review §1 states it directly), but the rationale actually written for it is weak: it cites only this document's own loss as justification — self-referential evidence, one data point — when the source analysis had at least six independent occurrences of this general idea to draw on (Theme A). More importantly, **P2 is functionally a corollary of P1**, not a separately load-bearing rule (see Overlap Analysis). Recommend either strengthening P2's independent rationale with non-self-referential evidence, or merging it into P1 as a second sentence.

### P3. Single Responsibility — **KEEP** (with a self-consistency note)
Well-evidenced, directly enforceable (Contract already checks it by name), correctly distinguished from P9. One structural irony worth flagging: P3 itself governs *two* categories in one statement — "documents" and "tools." A principle that states "one responsibility per document" arguably should not itself be a two-responsibility principle. Minor, not worth blocking on, but a clean v0.2 edit.

### P4. Deterministic Tooling — **MERGE** (with P5)
Clearly evidenced, but this is exactly the pair the source analysis flagged (§5, item 2) as "plausibly two faces of one principle." Draft 1's own Relationships field admits as much ("together they define one boundary from opposite sides") without acting on it. Recommend consolidating into a single principle stating the boundary both ways: mechanical work goes to tools, judgment stays with Chat.

### P5. Judgment Is Never Automated — **MERGE** (with P4)
Same finding as P4. Strongly evidenced independently (`IMPLEMENTATION_CONTRACT.md` §7's explicit prohibitions are some of the best-grounded citations in the whole document) — the strength of P5's own evidence is a reason to make the merged principle lead with this framing, not a reason to keep two entries.

### P6. Verify Before Trust — **KEEP**
Clear, necessary, directly enforceable (was a primary source cited: yes/no), no overlap with any other principle. No changes recommended.

### P7. Reversible Mutation — **REVISE**
Well-evidenced and genuinely important, but on close reading this principle's entire content is already stated, more precisely, in `IMPLEMENTATION_CONTRACT.md` §4 — and P7's own ADR field admits it ("None reserved — enforced directly through `IMPLEMENTATION_CONTRACT.md`"). If the Contract already fully owns and enforces this rule, restating it as a Principle risks the exact cross-document duplication P3 warns against. Recommend v0.2 either shrink this to a one-line pointer ("see `IMPLEMENTATION_CONTRACT.md` §4") rather than a full restated principle, or keep it but explicitly justify why a Contract-owned rule also deserves Principles-level statement (e.g., because it's a *value* the Contract merely operationalizes — a defensible position, but the current draft doesn't make that argument, it just restates).

### P8. Small, Reviewable Units — **REVISE**
Same issue as P7, same recommendation. Additionally, "small enough to review in one sitting" has no concrete threshold — inherited vagueness from the Contract itself, not introduced here, but worth naming since it limits this principle's enforceability regardless of which document it lives in.

### P9. No Speculative Structure — **KEEP** (flag for a dedicated ADR)
The best-evidenced, most load-bearing principle in the document — it drives this document's own Amendment Policy and is independently reinforced seven times across three sources per the source analysis. Given that weight, and given it currently has *no* reserved ADR (unlike P1, P3, P5/P10, P6/P7), recommend Founder consideration of a sixth ADR topic dedicated to it — the original five-ADR scope (`MIW_Bootstrap_Governance_Review.md` §2) didn't include one, but that scope was set before this principle's outsized influence on the document itself was apparent. Separately: the statement gives no operational test for "real, demonstrated need" — worth a concrete example or threshold in v0.2 to reduce future dispute risk.

### P10. Code Executes Written Specs — **KEEP** (clarify distinction)
Well-evidenced (`IMPLEMENTATION_CONTRACT.md` §7), genuinely non-redundant with P1/P5 on close inspection — P5 governs *who decides* (tool vs. Chat), P10 governs *where Code's instructions come from* (written spec vs. inferred history) — a different axis, not a restatement. But the current rationale doesn't make this distinction explicit, so a reader could reasonably mistake it for overlap. Recommend v0.2 state the P5/P10 distinction directly rather than leaving it implicit.

---

## Overlap Analysis

Of the four overlap pairs `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` §5 flagged as needing a decision, Draft 1 resolved two correctly (by keeping them distinct, with good reasoning) and left two unresolved:

| Pair | Source Analysis flagged it? | Draft 1's treatment | Verdict |
|---|---|---|---|
| P1 (repository-first) / P2 (documentation-authoritative) | Yes (§5, item 1) | Kept both, no resolution attempted | **Unresolved — recommend merge or stronger differentiation** |
| P4 (deterministic-tooling) / P5 (judgment-not-automated) | Yes (§5, item 2) | Kept both, Relationships field admits the overlap without acting on it | **Unresolved — recommend merge** |
| P3 (single-responsibility) / P9 (no-speculative-structure) | Yes (§5, item 3) | Kept both, distinguished as scope-vs-existence | **Correctly resolved — genuinely distinct, keep both** |
| P7 (reversible-mutation) / P8 (small-reviewable-units) | Yes (§5, item 4) | Kept both, distinguished as mutation-specific vs. general | **Correctly resolved as a pair — but see individual REVISE findings above; the more serious issue for both is redundancy with the Contract, not redundancy with each other** |

**New overlap not previously flagged:** P1 and P10 — P10 is described in its own Relationships field as "the direct consequence of P1 and P2." A principle that is explicitly "the consequence of" two other principles is arguably an application, not an independent principle. Reviewed above under P10; recommendation is to keep but sharpen, not merge, since the P5/P10 axis distinction is real.

---

## Gap Analysis

1. **"The repository must remain useful without Claude in the loop"** — flagged in `ENGINEERING_PRINCIPLES_SOURCE_ANALYSIS.md` §6 (Missing Areas) as proposed but never operationalized anywhere in the surviving corpus. Draft 1 had this flag available in its own permitted evidence base and did not close it. This is the clearest concrete gap in the current draft — recommend it become principle 11 in v0.2, or be explicitly declined with reasoning if the Founder judges it out of scope for this document.
2. **Governance process integrity** (`IMPLEMENTATION_CONTRACT.md` §1 items 6–7: "governance never bypassed for convenience," "silence is not consent, ambiguity resolved by asking") — arguably Contract-owned process rather than a Principles-level value, similar to the P7/P8 question above. Flagged, not recommended for inclusion — but worth an explicit Founder decision rather than silent omission, for consistency with how P7/P8 are being questioned.
3. **The three untraceable historical principle names** (`Explicit Relationships`, `Traceability`, `Reproducibility` — source analysis §6) remain exactly as unrecoverable as before. Draft 1 correctly does not guess at them. Not a defect in this draft; restated here only because Special Attention Q3 asks directly.

---

## Recommended Revisions

In priority order:

1. **Resolve P1/P2** — merge into one principle, or add independent (non-self-referential) evidence to P2's rationale and state explicitly why both are needed.
2. **Resolve P4/P5** — merge into one principle stating the mechanical/judgment boundary from both directions.
3. **Reconsider P7 and P8's form** — either reduce to explicit cross-references to `IMPLEMENTATION_CONTRACT.md` §4, or add an explicit argument for why Contract-enforced rules also earn independent Principles-level statement.
4. **Close or explicitly decline the offline-first/no-Claude-in-the-loop gap** — don't leave it silently unaddressed a second time now that this review has surfaced it twice.
5. **Sharpen P10's stated distinction from P1/P5** and **P3's self-referential two-category issue** — minor, low-risk edits.
6. **Add an operational test to P9** for what counts as "real, demonstrated need" — reduces future dispute risk given how much weight this principle carries.
7. **Consider a sixth ADR topic for P9** — Founder decision, not a drafting-stage action.
8. **Address the Draft-status ambiguity in P2's scope** — does an uncommitted/Draft version of a document count as "written down" for P2's own purposes? Worth one clarifying sentence.

---

## Recommendation for Draft v0.2

Do not restart from scratch — the evidence discipline and citation quality in Draft 1 are worth preserving intact. A v0.2 pass should: merge P1/P2 and P4/P5 (net: 8 principles from the current 10, before considering additions), resolve the P7/P8 form question, add or explicitly decline the offline-first gap, and make the P9/P10/P3 clarifications above. If the offline-first gap is added and nothing else grows the count, v0.2 would land at roughly 8–9 principles — fewer than Draft 1, not more, despite closing a real gap, because two merges outweigh one addition. This is worth stating plainly: **shrinking the count while improving coverage is a sign of a healthier document, not a less thorough one.**

---

## Answers to Special Attention Questions

**1. Does this document stand on its own?**
Mostly. Every principle's statement is self-contained, but several rationales lean on section-number citations to `IMPLEMENTATION_CONTRACT.md`, `MIW_Bootstrap_Governance_Review.md`, and `MIW_Architecture_Freeze_Review.md` without enough inline quotation for a reader to grasp the full "why" without opening those files too. This is a defensible tradeoff under P3 (don't duplicate content across documents) but means "stands on its own" is true for *what* the rules are, not always for *why*, without further reading.

**2. Would a new engineer understand how the repository should be engineered?**
Partially, and this should be stated honestly rather than glossed over: this document conveys *values* clearly (repo-first, judgment-vs-mechanical, verify-before-trust, reversible mutation, small units, no speculative structure) but does not convey *process* (the package lifecycle, how to pick up work, what exists today) — that's `IMPLEMENTATION_CONTRACT.md`'s and the future `docs/CLAUDE.md`'s job, and this document correctly avoids duplicating it. A new engineer needs this document plus at least the Contract to actually get oriented; that's a reasonable division of labor, not a flaw, but the document doesn't say so anywhere, and arguably should.

**3. Are any important governance concepts still missing?**
Yes — see Gap Analysis. The offline-first/no-Claude-in-the-loop concept is the clearest miss; governance-process-integrity is a defensible-but-undecided omission.

**4. Are there principles that should become ADRs instead?**
Not "instead" — but P9 is under-supported relative to its actual influence and is a strong candidate for a new, sixth ADR topic (see P9 review above). No principle currently duplicates ADR-level depth, so none needs *demotion* to ADR-only status.

**5. Should the document remain at approximately ten, or grow?**
Neither, precisely — it should get *more accurate*, which in this case means net-shrinking (two merges) while closing one real gap, landing near 8–9 rather than 10 or 14. Growing toward the historical 14 for its own sake would contradict P9, which this document itself states. The right target is "however many principles the evidence and identified gaps actually support," not a specific number.

---

## Final Verdict

**Draft v0.1 is a sound foundation, not a finished document.** Its evidence discipline should be preserved without dilution — nothing in this review found an invented claim, a misquote, or an unsupported historical assertion. Its structural weaknesses are real but narrow and fixable: two unresolved overlaps its own predecessor document already flagged, two principles that may not have earned independent status now that the Contract fully owns their content, and one previously-identified gap that didn't make it into the draft. **Recommend: do not approve Draft v0.1 as final. Approve it as a strong basis for v0.2**, incorporating the revisions above, before this document is treated as the repository's binding Governance Gate reference.
