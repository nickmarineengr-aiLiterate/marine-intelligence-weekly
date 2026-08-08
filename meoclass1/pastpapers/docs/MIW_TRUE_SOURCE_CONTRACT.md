# MIW QUESTION ↔ TRUE SOURCE REFERENCE CONTRACT

**Status: CONTRACT ONLY. No corpus content is imported, copied or referenced by QP2607.**
Written 2026-08-08. Applies to the Past Written Papers (QP) series.

This document defines how a written question will eventually point at verified source
material, so that the question-and-answer architecture does **not** have to be redesigned
when the Founder supplies corpus mappings.

**Nothing in this document is live.** Every QP2607 question currently carries **zero**
reference entries, by design. The framework renders nothing until objects exist.

---

## 1. The fourth learner question

The five study modes answer three questions — *what does this mean*, *how do I organise it*,
*can I reproduce it*. They do not answer the fourth:

> **Where does this requirement, number or rule actually come from?**

That is a **confidence** question, not a study question. It therefore does **not** become a
sixth study-mode tab. The Reference Shelf sits after the answer content, outside the mode
selector, as evidence.

```
QUESTION → UNDERSTAND → EXAM PLAN → ANSWER → STUDY GUIDE → RECALL     (study cycle)

ANSWER ──► REFERENCE SHELF ──► CORPUS OBJECT ──► RESOLVER ──► VIEWER ──► EXACT SECTION
                                                                          (verification)
```

**Reference Shelf ≠ Related Questions.** The shelf answers *where does the truth come from*.
`cross_links` answers *where else has this been examined*. Different relationships, kept
separate in schema and in UI.

---

## 2. The three-level trust chain

Deliberately three levels, so the answer page stays simple and depth is opt-in:

| Level | Control | Shows |
|---|---|---|
| 1 | the answer | the requirement, as a candidate would write it |
| 2 | **Verify source** | the exact consolidated section that carries it |
| 3 | **Source details** | issuing authority, edition/amendment, current-through date |

Level 3 is where authority is stated precisely. It is not on the answer page.

---

## 3. Questions reference OBJECTS. Never documents, never pages.

**Frozen architectural rule.** A question spec must never contain:

```
marpol.pdf#page=103        pdf-page-144        ?page=77
```

`validate_spec.py` scans every spec and **fails the build** on any of those, and did so
before the first reference was ever written — the cheap moment to forbid page coupling is
before one exists.

**Why.** Page numbers move on PDF regeneration, on consolidated amendments, on replacement
editions and on added bookmarks. A question bound to a page silently becomes wrong. A
question bound to an object stays correct while the resolver absorbs the change.

The corpus *may* record pages in its own provenance. That is the corpus's business.

---

## 4. Object id convention — adopted, not invented

The MIW reference repository at `RulesApp/repository/` **already establishes a node-id
convention**, and this contract adopts it rather than inventing a parallel scheme:

```
<INSTRUMENT>-<STRUCTURAL-TOKENS…>

SOLAS-II2-10                     SOLAS chapter II-2, regulation 10
MARPOL-VI-14                     MARPOL Annex VI, regulation 14
MARPOL-VI-14-144                 …and its sub-paragraph
FSSCode-9-2                      FSS Code chapter 9
BunkerConvention2001-Articles-7   Bunker Convention, article 7
IMSBCCode-4                      IMSBC Code chapter 4
```

Observed in `RulesApp/repository/index/repo-data.json`: 788 nodes across 60+ standards, each
node carrying `id`, `parentId`, `standardId`, `editionId`, `label`, `title`, `citations`,
`provenance` and `officialRequirement`.

**Do not use `::` separators.** The established convention is single hyphens.

---

## 5. Data contract

```jsonc
"reference_shelf": [                     // OPTIONAL. Absent is valid and normal.
  {
    "object_id":    "MARPOL-VI-14",      // corpus node id, section 4 convention
    "label":        "MARPOL Annex VI regulation 14 — Sulphur oxides",
    "relationship": "PRIMARY_RULE",
    "claim_scope":  "The 0.10% ECA limit and the reg 14.6 record requirement",
    "state":        "REFERENCE_PENDING"
  }
]
```

`relationship` — small closed vocabulary, deliberately not a graph schema:
`PRIMARY_RULE` · `SUPPORTING_RULE` · `DEFINITION` · `PROCEDURE` · `LEGAL_BASIS` ·
`NUMERIC_SOURCE` · `CONTEXT`

`state` — `REFERENCE_AVAILABLE` · `REFERENCE_PENDING` · `NO_CORPUS_OBJECT_YET`

Validated: id syntax, no duplicates within a question, closed vocabularies, non-empty label.
**Not required on any question.** No corpus file needs to exist for the build to pass.

### Granularity now, and later

V1 is **question-level**. `claim_scope` records in prose which part of the answer an object
supports, which is enough to place a shelf item meaningfully without sentence-level citation
clutter. Nothing in the schema blocks attaching a shelf entry to a route step later — the
route steps are already numbered and stable, so `"step": 4` is a purely additive change.

---

## 6. Resolver boundary

```
QP PRODUCT      knows: object_id. Nothing else.
CORPUS RESOLVER knows: object_id → standard → edition → version → document → bookmark
                        → viewer destination → amendment state
VIEWER          knows: how to display authorised source material
```

**The pastpapers builder must not become the regulation corpus engine.** There is exactly one
coupling point in the whole builder — `reference_href()` in `build_paper.py` — which turns an
object id into a route. When the resolver lands, that function changes and nothing else does.

The existing corpus already contains the resolver's raw material: nodes carry `standardId`
and `editionId`, and standards carry `editions[].versions[]` with `effectiveFrom` /
`effectiveTo` / `status`. That is precisely the "current through" state level 3 needs.

---

## 7. Viewer boundary — designed now, deferred as work

**Designed now:** route shape `/reference/<object-id>`, resolved server-side rather than
hard-coded; exact-section landing, never "page 1 of the Annex, go and search"; the
`reference_href()` seam.

**Explicitly deferred:** any renderer, PDF.js or otherwise; authentication; entitlement
checks; contents/outline navigation; document search; watermarking. None of it is built here
and none of it is assumed.

The URL syntax is **not** frozen. It is provisional and internal until a viewer exists.

### On "controlled"

Documentation must not promise impossible protection. Anyone who can read a page can
photograph it. Future controls (no download, no print, entitlement, session tokens,
watermark, rate limiting) reduce **casual** redistribution and nothing more.

**Do not flatten searchable consolidated PDFs into page images to deter copying.** Search and
navigation are the educational value; destroying them to slow a determined copier trades the
product away for nothing.

---

## 8. Availability behaviour

| Corpus state | Review build | Publish build |
|---|---|---|
| Object exists and resolves | shelf item + **Verify source** | shelf item + **Verify source** |
| `REFERENCE_PENDING` | shelf item, muted, internal state shown | **item omitted** |
| No shelf at all | nothing renders | nothing renders |

**A missing corpus object must never** fail a paper build, force a fabricated reference, or
block Founder review. Publish omits what cannot resolve rather than offering a dead control —
a broken "Verify source" button destroys exactly the confidence the feature exists to build.

**Future gate candidate, not enforced:** publication may later require source coverage for
high-risk regulatory claims. Not implemented, because the Founder has not defined it.

---

## 9. Terminology

Recommended student-facing wording:

> **MIW True Source** — consolidated from verified primary sources
> Source: *[issuing authority]* · Current through: *[edition / amendment date]*

**MIW is the consolidation and presentation layer, not the issuing authority.** Never write
"official publication", "official equivalent" or anything implying MIW issues the instrument.

```
PRIMARY OFFICIAL SOURCE   (IMO, Government of India, class society …)
        ↓
MIW CONTROLLED CONSOLIDATION
        ↓
QUESTION / ANSWER RELATION
```

No badge proliferation. The presence of a working **Verify source** control is itself the
signal; a page covered in "SOURCE VERIFIED" chips reads as marketing.

---

## 10. Semantic integrity applies to references too

A shelf `label` or `claim_scope` is a **derived** representation and is bound by the same rule
as every other derived layer: it may not be more categorical than the verified answer. See
`known_traps.md` trap 16 and `SEMANTIC_GUARDS` in `validate_spec.py`.

Concretely: do not label an object in a way that asserts a classification, a threshold or an
applicability the answer itself qualifies.

---

## 11. Cross-paper relation — build once, relate, appear everywhere

When QP2501-Q? and QP2405-Q? also examine ECA changeover, all three point at the **same**
`MARPOL-VI-14`. The corpus object is authored once; questions relate to it. Never duplicate a
corpus reference per paper, and never copy corpus text into a question spec.

---

## 12. Coverage reality as at 2026-08-08

Reported as an architecture finding. **No mapping has been written.**

The existing corpus would already support some QP2607 questions and not others — for example
`MARPOL-VI-14` exists with sub-nodes, `BunkerConvention2001-Articles-3` and `-7` exist (the
exact liability-versus-insurance distinction Q2 turns on), while the IMSBC individual cargo
schedules Q1 needs do not exist (only chapter-level nodes), and
`dgma-merchant-shipping-act-2025` is registered with **zero** nodes.

That mixed state is the normal condition this contract is designed for, and it is why the
availability states in section 8 exist.

**FOUNDER DECISION REQUIRED — one question only:** is `RulesApp/repository/` the intended
resolver for QP references, or is the July corpus a separate store? The contract works either
way; only `reference_href()` and the resolver lookup depend on the answer. Nothing should be
populated until that is settled.
