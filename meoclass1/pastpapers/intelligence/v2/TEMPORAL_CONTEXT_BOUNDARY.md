# Temporal-context boundary — Exam Plan or Study Guide?

**RESEARCH ONLY.** `current_as_of: 2026-08-17`
Boundary test only. **No corpus cleaning was performed and none is proposed here.**

The Laptop's sweep found fewer than ten route points across 40 papers that read as
state-of-law *context* rather than executable answer points, and named four
questions to inspect. Phase 2 inspected exactly those four and derived a rule.

---

## What was inspected

`QP2304-Q8`, `QP2403-Q9`, `QP2510-Q9`, `QP2501-Q4` — 29 route steps between them,
filtered for status language (*not yet in force*, *adjourned*, *pending*, *at this
sitting*, *superseded*, …).

| Where | Point | Verdict |
|---|---|---|
| `QP2304-Q8` step 5, limb `a)` | “the 2022 amendments are **adopted but not yet in force** — social connectivity, appropriately-sized PPE, repatriation of the body or ashes” | **EXAM PLAN** |
| `QP2403-Q9` step 2, limb `(a)` | “Std A2.5.2 — financial security for abandonment, a 2014 amendment in force at this sitting” | **EXAM PLAN** |
| `QP2501-Q4` step 0, limb `null` | “So at this sitting the control is in force but its transition is still running” | **EXAM PLAN** |
| `QP2403-Q9` step 0, limb **`framing`** | “at this sitting the operative text is the Convention as amended in 2014, 2016 and 2018” | **STUDY GUIDE** |
| `QP2510-Q9` step 0, limb **`framing`** | “at this sitting the operative text is the Convention as amended in 2014, 2016, 2018 **and 2022**” | **STUDY GUIDE** |

Two of 29 cross the line. That is consistent with the Laptop's “fewer than ten”
across the corpus, and it means the boundary is a **rule to apply going forward**,
not a cleanup backlog.

---

## The rule

> **EXAM PLAN** — anything the candidate writes on the script: a requirement, an
> action, a named instrument with its content, **or a status that qualifies a
> requirement the candidate is stating**.
>
> **STUDY GUIDE** — anything that exists to tell the *author* which version of the
> law to answer from, or that narrates how the law arrived here or where it is
> going, without adding anything the examiner scores.

### The operational test

**Does removing this point change what the candidate writes?**

- Changes the script → **Exam Plan**
- Changes only which sources the *author* consulted → **Study Guide**

Applied to the two borderline cases: *“the operative text is the Convention as
amended in 2014, 2016 and 2018”* is an **edition-selection note**. It tells the
author which MLC text to answer from. A candidate who never writes that sentence
loses nothing, because the amendments' *content* is already carried by the points
that follow. It is Study Guide.

By contrast, *“the 2022 amendments are adopted but not yet in force”* **is** the
scoring point — status is part of the correct legal statement, and a candidate who
presents an unentered amendment as binding law is wrong.

### A useful mechanical signal, not a rule

Both Study Guide cases sit on step 0 with `limb: "framing"` — an authoring scaffold
(see `LIMB_MODEL.md`). Both Exam Plan cases sit on real source limbs, mid-route.

Scaffold-limb + edition-selection language is a **strong flag for review**. It is
not the test — `QP2501-Q4`'s point sits at step 0 too and is correctly Exam Plan,
because it states the status of a control the candidate must describe.

---

## Where temporal deltas land

This settles the placement question the temporal layer raised:

| Material | Destination |
|---|---|
| A requirement, and its current status | Exam Plan |
| “Do not write X, it was repealed” | **Study Guide** |
| “This was asked before” | **Study Guide** |
| Which edition the answer was written against | **Study Guide** |
| Supersession narrative, pending changes, future status | **Study Guide** |
| A new point the examiner now expects | Exam Plan |

The last row is the one to watch. A temporal delta may legitimately produce an
Exam Plan bullet — but only through `exam_relevance: ESSENTIAL_CURRENT_POINT`, and
only as a point, never as history. `USEFUL_CURRENT_ENRICHMENT` and below stay in
Study Guide.

That gate matters at this corpus's scale: route points already run to a median of
41, a p90 of 61 and a maximum of 80, with 39 questions above 60. Temporal
Intelligence has no headroom to spend and must not dump history into Exam Plan.

---

## Not done here, deliberately

- No route point was edited.
- No spec was touched.
- The remaining ~5 corpus-wide candidates were not hunted down.

The deliverable was a deterministic rule for future authoring. That rule is above.
