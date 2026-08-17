# MIW WRITTEN ANSWER METHOD — design rationale

**Status: ADOPTED.** Written 2026-08-08 as the QP2607 pilot rationale; carried by the whole
solved corpus since. Applies to the Past Written Papers (QP) series.

> **Structurally frozen as the V1 template on 2026-08-08** — five modes, one canonical
> `answer_route`, everything else derived. See `CURRENT_STATUS.md` §2a. **Do not add a sixth
> mode.**
>
> The pilot question this file once carried — *"does the method work?"* — was closed by QP2607
> Founder review and by cross-paper validation from QP2601 onward. The architecture has since
> been applied across the full solved corpus.
>
> **This document is the design *rationale*. It does not bind on its own.** What binds a
> production session is `PASTPAPER_PRODUCTION_PROTOCOL.md` §6, which states the current rules;
> read that first and come here for *why*. Where the two differ, the protocol wins.

This document explains *why* the QP question object has the shape it has. It is the design
rationale a future paper-production session should read before authoring QP2601–QP2612.

---

## 1. The problem we are solving

Founder feedback from real MEO Class I candidates. Five recurring first-attempt failures:

| # | Candidate said | What it actually is |
|---|---|---|
| **F1** | "I could not finish in time" | No execution plan. Time lost deciding what to write. |
| **F2** | "My answer was too short" | No sense of what "enough" looks like. |
| **F3** | "I did not have enough points" | Recalled the topic, not the coverage. |
| **F4** | "I did not understand the topic" | Memorised prose over a hollow mental model. |
| **F5** | "I could not remember it in the exam" | Studied by re-reading, which does not survive pressure. |

A technically correct 650-word essay solves none of these. It is necessary and not
sufficient. **Correctness stays the foundation; execution is the layer being added.**

---

## 2. Evidence review

Compact by design. Only what changed a build decision.

| Technique | Evidence | Use? | Fixes | Implementation |
|---|---|---|---|---|
| **Retrieval practice / testing effect** | **STRONG** — d ≈ 0.40–0.61 across 7 syntheses, >120,000 students; "high utility" in Dunlosky 2013, replicated by Hattie & Donoghue 2021 (242 studies, n=169,179) | **YES** | F5, F3 | Flashcards + blank-skeleton recall |
| **Complexity caveat on the testing effect** | **STRONG enough to constrain us** — most studies use simple verbal material; the effect *shrinks as material complexity rises* | **YES — as a limit** | F5 | Never test "recall the essay". Test the **route** (5–9 items) and **discrete facts**. See §4. |
| **Pretesting / errorful generation** | **STRONG** — attempting and failing *before* instruction beats studying first; benefit does **not** depend on retrieval success, but the correct answer must follow | **YES** | F5, F4 | Recall test sits **before** the answer, with instant reveal |
| **Distributed practice / spacing** | **STRONG** — joint top rating with practice testing | **PRINCIPLE ONLY** | F5 | Stable card IDs so a scheduler *can* be added later. **No scheduler now** (out of scope). |
| **Chunking** | **STRONG** | **YES** | F1, F5 | Route capped at **5–9 steps**; map branches = route |
| **Concept / knowledge mapping** | **USEFUL, CONTEXT-DEPENDENT** — Karpicke & Blunt (2011) found retrieval beat mapping, but a 2024 re-examination showed that gap was a **methodological artifact** (the mapping group never got a memorisation phase); retrieval-*based* mapping performs well | **YES, as retrieval** | F4, F1 | Map has a **hide/reveal** mode so it is recall, not a picture to read |
| **Worked examples** | **STRONG** for novices | **YES** | F2, F4 | The Model Answer *is* the worked example |
| **Expertise reversal** | **STRONG** — scaffolding that helps a novice *harms* an expert by adding redundant load | **YES — architectural** | all | **Never force the ladder.** Progressive disclosure; the Model Answer is always one click away. See §7. |
| **Elaboration / self-explanation ("why")** | **MODERATE** | **YES** | F4 | Study Guide answers *why*, not *what again* |
| **Interleaving** | **MODERATE, context-dependent** | **NOT NOW** | — | Meaningful only across many papers. Revisit at 3+ papers. |
| Re-reading · highlighting · summarising | **LOW UTILITY** (Dunlosky) | **NO** | — | Deliberately **not** added. No "summary" block. |
| Huberman "gap effect", 10-second micro-breaks, "10× repetitions" | **CONTESTED** — not universally accepted; specific magnitude claims are not established | **NO** | — | Study-session *behaviour*, not content architecture. Out of scope, and we will not repeat unverified magnitude claims. |
| Sung "GRINDE" mapping | **Method, not a study** — its useful parts (4–8 chunks, direction/causality, construct-don't-copy) are the mainstream chunking + generation findings above | **PRINCIPLES ONLY** | F4 | Adopted as chunk limits and relational branches. **No third-party terminology or branding in MIW.** |

**Two findings did the most work here.** The complexity caveat is why we never ask a
candidate to recall prose. Expertise reversal is why the learning scaffolding is optional
rather than a gate.

---

## 3. What MIW deliberately does not build

Spaced-repetition scheduling · SM-2 · Anki clone · XP, streaks, gamification · AI tutor ·
accounts · database · cloud sync · study analytics · dashboards · external mind-map engines
or graph libraries.

Stack is unchanged: **structured JSON → deterministic Python renderer → vanilla HTML/CSS/JS,
`localStorage` only where it earns its place.**

---

## 3a. SEMANTIC INTEGRITY — the rule that outranks the rest

> **Structural consistency is not semantic consistency.**

Every derived representation — route, core points, knowledge map, flashcards, Quick Revision,
Rapid Revision, memory cue, reference label — is a *short form* of a verified answer. The
failure mode is not that it goes out of sync structurally; the toolchain catches that. It is
that a nuanced conditional statement gets **flattened into a categorical one** on the way out.

**A derived layer may never be more categorical than its source.** Every one must preserve:

scope · conditions · uncertainty · jurisdiction · applicability · regulatory status

This was found for real, not hypothetically. Q1's model answer said iron ore pellets are
"carried as Group C … but establish that from the declared BCSN and its current individual
schedule"; a route core point, `recall_15s`, `major_trap` and a flashcard had all reduced it
to **"pellets are Group C"**. `recall_15s` contradicted itself inside a single field. It also
overstated provenance: the group rests on authoritative-secondary sources and is recorded as
a class C limitation.

Enforced by `SEMANTIC_GUARDS` in `validate_spec.py`, which scans the **derived fields only** —
the model answer and study guide are the source and may carry the full conditional sentence.
Guards are narrow and known-issue-specific. There is deliberately **no general truth
validator**; subjective quality stays a human review.

Recorded as `known_traps.md` trap 16.

## 4. The core principle — do not memorise 650 words

A candidate cannot reliably reproduce 650 words of prose under pressure, and the evidence
says testing prose is where the testing effect is weakest. So MIW teaches a **route**:

```
5-9 numbered anchors
      -> each anchor recalls a cluster of core points
            -> candidate reconstructs the explanation in their own words
```

The anchors are what get memorised. The prose is regenerated, not recited.

---

## 5. One canonical sequence

**The single most important structural rule.** One question has exactly **one** numbered
route, and every view is that same route:

```
answer_route  (canonical, authored)
   |
   +-- Start here      route headings, in order
   +-- Model answer    principal sections ARE the route steps
   +-- Knowledge map   first-level branches ARE the route steps
   +-- Recall test     route steps with titles hidden
   +-- Quick revision  route as a one-line trail
   +-- Flashcards      one auto card tests the route; others test its content
```

A candidate learns **one** route, not four competing structures. `validate_spec.py` enforces
that every route step has a matching principal heading in the model answer, so the two
cannot drift.

**Derived, never authored twice:** knowledge map, recall test, start-here block, quick-revision
route line, and the structure flashcard. Changing a route step updates all of them.

---

## 6. Answer archetypes

The nine QP2607 questions fall into five natural shapes. The **schema is identical** for all;
only the route differs. Archetype is recorded so future papers can reuse a known-good shape.

| Archetype | Typical route | QP2607 |
|---|---|---|
| `procedure` | Immediate action → sequence → records → follow-up | Q2, Q4 |
| `explain` | Define → components → how it works → significance | Q1, Q3 |
| `compare` | Define A → Define B → distinctions → application | Q5 |
| `legal` | Principle → statutory basis → requirements → exceptions → consequences | Q7, Q9 |
| `evaluate` | Context → for → against → comparison → judgement | Q6, Q8 |

Five is enough. Do not grow this list without a question that genuinely fits none of them.

---

## 7. The learner journey — a ladder you may skip

```
UNDERSTAND  ->  PLAN  ->  WRITE  ->  RECALL  ->  TEST
```

Rendered as one mode selector inside the already-proven expandable question card:

```
[ Understand ] [ Exam Plan ] [ Answer ] [ Study Guide ] [ Recall ]
```

**Verification is a capability, not a sixth tab.** "Where does this come from?" is a
confidence question, not another way of studying the same answer, so the Reference Shelf sits
after the answer content and outside this selector. See `MIW_TRUE_SOURCE_CONTRACT.md`.

**A memory cue must not create a second route.** A cue may point *at* the canonical route; it
may not introduce its own sequence of a different length. Q2's cue originally listed seven
anchors against a six-step route — the candidate then has to reconcile two structures under
exam pressure, which is the opposite of the point. Cues now carry the step numbers they map
to, and `check_memory_cue()` rejects an enumerated cue that maps to none.

**Remember vs Cover.** The memory target and the coverage target are different sizes, and the
UI now says so explicitly: *Remember 5 route headings · Cover 23 core points beneath them*.
A candidate trying to memorise 23 core points is doing the wrong work.

**`Answer` is the default open view.** Expertise reversal is the reason: a candidate who
already knows the topic must not be walked through scaffolding to reach the model answer,
and a candidate revising for the third time needs less support than on day one. The ladder
is available, never compulsory.

A candidate must never have to wonder *where is the actual answer*.

---

## 8. Numbering style

```
1.  Principal section          <- these are the route steps
    (a) (b) (c)                <- sub-points where the question has limbs
    - bullets                  <- lists within a section
```

No `1.1.1.1`. These are exam answers, not technical standards. For two-part questions
(Q1, Q3, Q8) the route carries a `limb` of `(a)`/`(b)` so the structure mirrors the printed
question. Where numbering would break natural legal or analytical prose, the section keeps
its prose and only the heading is numbered.

---

## 9. Core points — the completeness signal

**Definition.** A core point is *one distinct exam-relevant proposition, action, requirement,
distinction or explanation that materially advances the answer.*

It is **not** a sentence, a bullet, or a clause. Splitting one idea into fragments to inflate
a count is prohibited. "Stop the transfer", "raise the alarm" and "close the valves" are
three genuine operational points. "Stop the transfer immediately" and "stop the transfer at
once" are one.

Core points are authored as **short cues** (3–8 words) attached to their route step — they
are retrieval cues, not a second copy of the prose.

**User-facing wording is `CORE POINTS TO COVER`, never `MARKS`.** We do not know the
examiner's private marking scheme and will not imply a points-to-marks mapping. The number
exists so a candidate can tell when an answer is *probably too thin* — that is all it claims.

---

## 10. Component specifications

**Understand this first** — plain engineering language, the central mental model *before*
examination phrasing. **Conditional by design**: present only where the topic has a genuinely
counter-intuitive core. Adding it to a self-evident question is clutter, and clutter is what
expertise reversal punishes.

*Clarified 2026-08-12 by the candidate-feedback audit (`CANDIDATE_FEEDBACK_AUDIT_2026-08-12.md`).
The conditional gate above is unchanged. What the audit settled is the job the section must do when
it is present, after a candidate reported that the column did not help him write once he had
forgotten the technical term.*

**The purpose test.** Understand exists to answer one question: *can I remember and explain the idea
even if I forget the official term?* It is not a second Model Answer, not a regulation dump, not a
synonym-rewritten Answer, and not a mini Study Guide.

**The reconstruction test — the acceptance criterion.** Delete every bold term from the section. If
what remains would still let a candidate rebuild the shape of a decent answer, it passes. If what
remains is exam advice, or nothing, it fails.

**Seven rules, derived from the sections that measurably passed that test:**

1. Open on the **situation or the problem**, in ordinary words. Never open on a citation.
2. Explain the **mechanism** — what happens, why it matters, what follows from what.
3. **Plain idea first, formal term second.** Write "the paperwork and enforcement side, the physical
   condition of the ship, and the conditions of the people aboard", and *then* name them
   *administrative, technical and social* matters. The concept must survive the term being forgotten.
4. **Carry no dates, resolution numbers or article numbers.** Those belong in Answer and Recall,
   where they are already verified. A number in Understand is a number maintained in two places.
5. **Describe the limbs conceptually; do not address the examiner.** "The examiner has asked for
   three things" teaches nothing and duplicates the Exam Plan. Naming a limb to orient the reader is
   fine; substituting exam strategy for explanation is the defect.
6. **Length follows the job, not a sentence count.** Measured practice across the solved corpus is a
   median of ~120 words, and up to ~200 is right where the question has two unrelated halves. The
   former "2–4 sentences" figure described the QP2607 pilot and had already been overtaken by the
   corpus it was meant to govern.
7. **Stay question-specific**, and keep the same spine as Exam Plan, Answer and Recall. A friendlier
   explanation that reorganises the route is a defect, not an improvement.

Because rule 4 keeps dates and citations out, an Understand section is normally
**sitting-independent** and transfers unchanged across an exact-recurrence family — unlike answer
prose, which must be re-anchored on every Tier D reuse.

**Start here / Exam Plan** — the route headings, and the instruction to write all headings first
and then expand in order. Must be usable in seconds. This is the F1 fix.

*Superseded rendering, recorded so the change is not mistaken for drift.* The original view
printed every route heading **twice** — once as the plan list, and again inside a collapsed
`<details>` — and that duplication is the only reason the core points had to be hidden at all.
The two were merged into **one list with the points shown beneath each heading**, captioned
*Bullet answer — points to write*. A candidate asking for "a bullet version of the answer" is now
given it on arrival instead of having to discover a collapsed control.

This shipped as a QP2608 pilot behind a `plan_bullets` spec flag, was propagated to the whole
corpus on 2026-08-17, and **the flag was then removed deliberately**. There is one renderer and
no opt-in. The points are the same `answer_route.steps[].points` every other view derives from —
no second corpus, nothing authored twice, so nothing can drift. Subpart marks print beside a limb
**only where the source paper stated them**; they are never inferred from a total. See
`PASTPAPER_PRODUCTION_PROTOCOL.md` §6.2–§6.4.

**Knowledge map** — root = topic; first level = route steps (5–9); second level = only
critical children. No paragraphs, no third level. Rendered as a **semantic HTML/CSS tree**
(`<ol>`/`<ul>`), not an SVG island — so it is readable by screen readers and reflows on
mobile for free. Carries a hide/reveal control so it can be used as retrieval.

**Flashcards** — 5–12 per question. Required coverage: at least one `structure` card
(auto-derived from the route), and cards spanning `definition`, `distinction`, `procedure`,
`regulation`, `number`, `trap`. Prompt → reveal short answer → optional why. Prohibited:
prompts that contain their own answer, paragraph-length answers, trivia, duplicates.

**Recall test** — the route with titles blanked, revealed on demand. Pretesting says the
attempt matters more than success, so no typing is required in V1; mental or paper
reconstruction is enough, and the reveal must be immediate.

**Quick revision** — retrieval cues only: route trail, keywords, critical numbers, critical
regulation, biggest trap. A 30–60 second refresh, **not** a miniature answer.

**Study guide** — must fix *understanding*, not restate the answer: central concept, causal
relationships, why the rule exists, misconceptions, connections. Existing six-section spine
is retained.

---

## 11. Schema — required, conditional, optional

Avoiding schema inflation. New fields:

| Field | Status | Why |
|---|---|---|
| `answer_route` (`archetype`, `steps[]` with `n`, `title`, `limb?`, `points[]`) | **REQUIRED** for every built answer | It is the spine every derived view depends on |
| `retrieval_cards[]` (`id`, `type`, `prompt`, `answer`, `why?`) | **REQUIRED**, ≥4 authored | The primary evidence-backed intervention |
| `understand_first` | **CONDITIONAL** — where the topic is counter-intuitive. Where present it must pass the **reconstruction test** in §10 | Forcing it everywhere creates clutter; but where it *is* present and fails the purpose test, the mode silently stops working |
| `memory_cue` | **OPTIONAL** | Only where a cue is genuinely memorable. **No invented acronyms.** |
| `knowledge_map`, recall test, start-here | **DERIVED — never authored** | Single source of truth |

Card IDs are stable (`QP2607-Q5-C3`) so a future spacing layer can attach without re-authoring.

---

## 12. Performance and accessibility

Learning content lives **inside** the paper page, never on the index — the index already
carries every question's search blob and must not also carry ~70 flashcards per paper.

All controls are real `<button>`s with `aria-expanded`, keyboard operable, visible focus.
The map is semantic markup, so it degrades to a readable nested list with CSS off and is
navigable by screen reader. Nothing in the learning layer is required to reach the answer:
with JavaScript disabled the model answer must still render.

---

## 13. QP2607 pilot plan

Apply to all nine July questions — deliberately diverse (technical, scenario, institutional,
operational, conceptual-legal, emerging-tech, legislative, human-element, legal principle).
If a feature only works for Q2 and is absurd for Q9, it must not be mandatory.

Then test against five simulated candidates: **A** cannot finish · **B** writes too little ·
**C** forgets under pressure · **D** cannot understand · **E** needs rapid revision.
Defects are recorded by failure mode, not by "does the HTML look nice".

**Verified technical content is not to be changed to fit the template.** Renumbering headings
is presentational; if any wording changes, regression-check it. All existing verification
metadata and the A/B/C reverify register remain authoritative.
