# MIW Repository — Final Architecture Review: `engineering/` Wrapper Proposal
**Role:** Chief Software Architect (pre-freeze review)
**Status:** Final structural decision before PKG-1
**Date:** 2026-07-30

---

## Starting Position

I will not accept or reject this by instinct. The proposal deserves a real test: does wrapping `docs/governance/adr/skills/templates/reports` under `engineering/` produce a **measurable** improvement, or is it reorganisation for its own sake? Notably, the proposal itself already makes one judgement call worth scrutinising: it keeps `tools/` and `corrections/` *outside* `engineering/`, splitting "engineering knowledge" from "engineering execution" and "engineering history." That asymmetry is the first thing to test — if it doesn't hold up, the whole premise weakens.

---

## 1. Architecture Comparison Table

| Criterion | Architecture A (flat, current blueprint) | Architecture B (`engineering/` wrapper) | Winner |
|---|---|---|---|
| 1. Long-term maintainability | Each dir independently named and scoped; no dependency on a parent grouping being "correct" | Adds one more structural decision (what belongs inside `engineering/` vs. not) that must stay correct forever | **A** |
| 2. Repository discoverability | `docs/`, `skills/`, `tools/` etc. are self-evidently meta by name alone — no collision risk with `meoclass1/`, `SQ/`, `GHGDecarb/` | Marginally clearer *if* root is already crowded, but content dirs already have unambiguous product-specific names, so the grouping solves a problem that doesn't exist | **A** (see Section 2 detail) |
| 3. Claude Code usability | Shorter paths on the directories touched most often (`tools/`, `corrections/`) | Same tools/corrections paths (proposal keeps them shallow) — but `docs/`, `skills/` now one hop deeper for every reference | **A**, marginal |
| 4. Claude Chat usability | Same reasoning as #3 — path length compounds over thousands of tool calls across years | Same marginal cost as #3 | **A**, marginal |
| 5. Onboarding a future contributor | Six flat, clearly-named directories — a `ls` at repo root tells the whole story in one screen | Requires understanding *why* the split exists (why is `tools/` not "engineering" but `skills/` is?) — the asymmetry itself needs explaining | **A** |
| 6. Repository scalability | New meta-categories (if ever needed) just become new top-level dirs with clear names — no risk of running out of root "slots" | Scales slightly better *only* if root becomes genuinely crowded with dozens of dirs — not close to true today | **Tie**, B has theoretical edge only |
| 7. Documentation clarity | ADRs live at `docs/adr/` (already decided in governance review) — one governance home | B reintroduces a *second* governance home (`engineering/governance/` + `engineering/adr/`) — this is the same fragmentation the governance review explicitly rejected when it killed `DECISION_LOG.md` | **A**, clearly |
| 8. Risk of future clutter | Low — each dir has one job | Low-to-medium — `engineering/` itself becomes a second root that can clutter internally, and the tools/corrections exclusion needs continuous justification as it grows | **A** |
| 9. Engineering discipline | Matches "avoid unnecessary hierarchy," "one responsibility per document" | Adds hierarchy whose responsibility ("things that aren't tools or corrections but are meta") is fuzzier than any individual directory's | **A** |
| 10. Consistency with this governance review's own philosophy | Directly consistent — Section 3 of the governance review already rejected adding governance homes beyond `docs/adr/` and `ENGINEERING_PRINCIPLES.md` | Directly inconsistent — reopens a decision already closed one review ago | **A** |

**Score: Architecture A wins or ties on all 10 criteria. Architecture B wins outright on none.**

---

## 2. Pros and Cons

### Architecture A (flat)

**Pros**
- Zero new structural decisions — every directory's purpose is legible from its name alone
- Shortest paths for the highest-frequency operations (`tools/*.py`, `corrections/*.md`)
- Fully consistent with the governance review just completed (ADRs at `docs/adr/`, no separate governance home)
- Nothing to migrate — this is what PKG-1 through PKG-13 are already planned against

**Cons**
- If the repository eventually accumulates many more meta-categories (beyond the current 6), root could get crowded — but this is a five-years-from-now hypothetical, not a current or near-term reality
- No single glance answers "which directories are repo-engineering vs. product content" — you have to know the names

### Architecture B (`engineering/` wrapper)

**Pros**
- One-glance separation of "meta" vs. "product" content at root, if root ever becomes genuinely crowded
- If MIW ever spawns sibling repositories (a real possibility given the multi-property nature of your work — ecosystem, timeline, archive, RulesApp-adjacent tooling), `engineering/` as a *convention* could theoretically be replicated across repos for consistency

**Cons**
- Introduces exactly the asymmetry the governance review has spent two rounds eliminating elsewhere: why are `tools/` (executable knowledge) and `corrections/` (historical knowledge) *not* "engineering," but `docs/` and `skills/` are? This isn't a rhetorical gotcha — a future contributor or a future Claude session will genuinely ask this and there's no clean answer, because the split is organisational taste, not a real category boundary
- Recreates the `governance/` + `adr/` fragmentation that Section 3 of the governance review explicitly closed one review ago — adopting it now would be reopening a decision without new evidence, which the review process itself exists to prevent
- Adds path depth to `docs/` and `skills/`, the second- and third-most-referenced directories after `tools/` and `corrections/` — the cost lands exactly where frequency is highest among the "knowledge" tier
- No measurable problem it solves today — root currently has ~6 planned meta-directories against ~6 existing content directories/files (`meoclass1/`, `SQ/`, `GHGDecarb/`, `archive/`, `ecosystem.html`, `timeline.html`); this is not a crowded root by any reasonable standard

---

## 3. Repository Growth Test (Five-Year Horizon)

Assume: more Python tools, more docs, more automation, more standards, possibly additional repositories.

**Architecture A ages fine.** The failure mode for flat structures is *too many top-level entries with ambiguous or overlapping names*. That's not what's happening here — `docs/`, `skills/`, `tools/`, `templates/`, `reports/`, `corrections/` are semantically distinct and non-overlapping by construction (this was already enforced in the prior governance review: `reports/` split from `docs/` specifically to avoid ambiguity, `corrections/` given a distinct purpose from `known_traps.md`). Adding a 7th or 8th meta-directory in five years costs nothing — it's just another clearly-named sibling.

**Architecture B's theoretical advantage — multi-repository consistency — doesn't actually require adopting it now.** If MIW does spawn sibling repositories in the future, the decision to standardise a shared `engineering/` convention across repos can be made *at that time*, with real evidence of the problem it's solving. Pre-adopting it today based on a five-year hypothetical is the same over-engineering pattern the governance review already flagged and rejected for `automation/` and `STYLE_GUIDE.md` — build structure when a demonstrated need exists, not speculatively.

**Migration cost either way is currently zero** — no package has run yet, nothing exists under any of these paths. This is worth being honest about: normally "no migration cost yet" would be a point *in favor* of adopting the more elaborate structure while it's cheap. But that argument only holds if B were otherwise equal or better on the 10 criteria above. It isn't — B loses or ties on every one. Cheap migration doesn't make a worse architecture worth adopting.

**Verdict: Architecture A ages better**, not because change is inherently bad, but because A's flat structure has no latent inconsistency that will need explaining or unwinding later, and B's does (the tools/corrections exclusion, and the governance fragmentation).

---

## 4. Recommendation

**Reject Architecture B. Retain Architecture A (the current blueprint's flat structure) without modification.**

This is not a "both are fine, pick your preference" outcome. Architecture B introduces a specific, identifiable regression: it reopens the governance-home fragmentation question (`governance/` + `adr/` as two homes) that this project's own governance review already resolved in favor of a single home (`docs/adr/` + `ENGINEERING_PRINCIPLES.md`). Adopting B now would mean the governance review contradicts itself one document later, which is a worse outcome for long-term maintainability than any organisational tidiness B might offer.

The one genuine idea worth preserving from the proposal — a clear "this is repo-engineering, not product content" grouping — is **already achieved by naming alone** (`docs/`, `skills/`, `tools/` etc. don't need a wrapper to be recognisable as non-content, and none of them collide semantically with `meoclass1/`, `SQ/`, or any other content directory).

---

## 5. Migration Impact

**If adopted:** Zero cost today (nothing built yet), but locks in a structural inconsistency that PKG-1.5 (governance docs) and PKG-2–4 (core docs) would then need to justify or work around from their first commit — effectively exporting today's unresolved design question into every subsequent package's file paths.

**If rejected (recommended):** Zero cost, zero change. The blueprint and governance review proceed exactly as already approved. `docs/adr/` remains the single governance home per Section 3 of the governance review; `PKG-1.5` through `PKG-13` require no path changes.

---

## 6. Final Decision

**Reject Architecture B entirely. Do not adopt before PKG-1. No amendment to the blueprint or governance review is required.**

The existing blueprint's flat structure (Architecture A) is already superior across every reviewed criterion, and adopting the `engineering/` wrapper would silently contradict a decision this same review process made one round earlier. The correct engineering response to "should we add a layer of hierarchy" is not "it's free right now so why not" — it's "does it solve a real, current problem without creating a new one." Here it doesn't, and it does.

**Architecture is now frozen as:**
```
marine-intelligence-weekly/
├── docs/            (incl. docs/adr/)
├── skills/
├── templates/
├── reports/
├── corrections/
├── tools/           (incl. tools/_lib/)
├── meoclass1/, SQ/, GHGDecarb/, archive/, ecosystem.html, timeline.html  (existing content, unchanged)
└── .github/         (existing, unchanged)
```

The Founder Acceptance Checklist from the governance review stands as written — no line item requires revision as a result of this review. **PKG-1 is clear to begin on your sign-off.**
