# PASTPAPER PRODUCTION PROTOCOL

**Governed by `PRODUCTION_PROTOCOL_INDEX.md`. Read every paper-production session.**

Stable rules only. No paper-specific facts, no current targets, no branch names, no counts —
those belong in `CURRENT_STATUS.md` and the session prompt.

---

## 1. REPOSITORY-FIRST

The repository is the source of truth for what exists. Before asserting that something is
missing, absent, unbuilt or unsolved, **check the repository**. Intake specs, manifests,
verification records and demand maps already encode most of what a session needs.

Never re-derive from memory what the manifest can answer.

---

## 2. SOURCE AUTHORITY

1. **Primary instruments** — the convention, code, resolution, circular or statute itself.
2. **The examination paper as printed at its sitting** — for what was asked and for how many
   marks.
3. **Official/administration guidance** — where it interprets the primary instrument.
4. **Everything else is not authority.** Search snippets, summaries, forum posts, coaching
   notes and secondary compilations may point you at a source; they may never *be* the source.

Hard rules:

- **Never fabricate a regulation, section, resolution, circular or amendment number.** If it
  cannot be verified, say so in the record rather than inventing precision.
- **Third-party coaching notes are not citable.** Some circulating note sets are known to be
  error-seeded by their publishers. They may be used to understand what a question is driving
  at; they must never appear as authority.
- **Source PDFs are never committed.** This repository is public. Source papers live outside
  version control.

### 2.1 Technical claims with no regulatory source

The ladder above is the authority ladder for a **legal, regulatory or official** claim. Where
such a claim has an applicable primary source, that source is **mandatory**. Nothing below
relaxes that.

But engineering explanation does not require a regulation to exist. Where a question asks how
something works, why it fails, or how it is operated, and **no instrument prescribes the
answer**, acceptable authority for those limbs includes:

- manufacturer manuals and maker's technical documentation;
- classification-society technical material;
- recognised engineering references and standard textbooks;
- authoritative technical papers.

Three rules bound this, and none is negotiable:

- **Never manufacture an IMO, class or statutory rule to satisfy a "primary source"
  checkbox.** An invented regulation number is a far worse defect than an openly declared
  engineering-judgement answer. If no instrument prescribes the answer, record that fact.
- **The relaxation is limb-by-limb, not question-by-question.** A question mixing an
  engineering limb with a regulatory limb still requires primary verification of the
  regulatory limb, and the two must be distinguishable in the verification record.
- **An unverifiable quantity is omitted, not quoted.** Vendor-sourced or installation-specific
  figures — efficiency gains, consumption savings, percentage improvements — are left out
  rather than given false precision.

A technical answer is verified when its mechanism is sound, its provenance class is **stated
rather than disguised**, and the boundary of what could not be verified is written down.
`QP2506-Q1` is the worked precedent. It asks for the common **rudder-efficiency improvement
devices** — thrust fins, asymmetric rudders, rudder bulbs and Grim vane wheels. No instrument
prescribes any of them, so the answer declares engineering judgement as its dominant provenance
class and explains the hydrodynamics mechanistically. On quantities it does the thing rule three
requires: it **refuses to quote a saving as a hard number for any hull**, gives only the
conditioned ranges attributed to industry literature, names the variables the range depends on
(hull form, block coefficient, propeller loading, draught, service speed), states that
model-scale results need a scale-effect correction, and carries those ranges in
`reverify_before_publication` rather than presenting them as settled. Note what this precedent
does *not* license: a range is admissible because it is attributed, conditioned and declared —
not because a percentage is harmless.

---

## 3. ONE PAPER PER FOUNDER-REVIEW BRANCH

- Branch from the current reviewed head, named `pastpapers/qp####-founder-review`.
- **One paper per branch.** Do not fold two sittings into one branch.
- **No merge to `main`, and no launch, without explicit Founder approval.**
- There is **no valid half-authored-paper state**. Either the paper is complete and internally
  consistent, or the session stops and records exactly where it stopped and why.

---

## 4. CANONICAL SPEC → GENERATED HTML

The spec is the source; the page is a build artefact.

- Author the **spec** (`meoclass1/pastpapers/specs/QP####.json`). Never hand-edit generated
  HTML.
- Build with the governed toolchain in `tools/pastpapers/`.
- **Every generated file must reproduce exactly from its source.** `health_check.py` enforces
  this. A page that does not reproduce is a defect, not a variation.
- Build **only when the paper is complete**. Partial builds create misleading artefacts.

Toolchain (do not reinvent): `run_toolchain.py`, `validate_spec.py`, `build_paper.py`,
`build_index.py`, `build_questions_year.py`, `build_reuse_map.py`, `build_sample.py`,
`audit_paper.py`, `recurrence_check.py`, `known_traps_check.py`, `questions_year_check.py`,
`sample_check.py`, `health_check.py`, `ui_behaviour_test.cjs`.

### 4.1 BUILD MODE IS A DECISION, NOT A DEFAULT

**Establish the build mode before you build, and state which one you used.**

- A **bare** toolchain run produces the **review** build — `noindex`, ungated, carrying
  production metadata. That is correct for a paper under Founder review (§9).
- `run_toolchain.py --publish` produces the build **`main` commits**. That is the pre-commit
  gate for integration.

Three rules, each paid for by a real incident:

1. **Never pick the mode because a checker came back green.** `health_check.py` is
   **mode-symmetric** — it faults a review tree that is not `noindex`, and equally faults a
   publish tree that still carries `noindex`. One of the two invocations returns 0 errors for
   *any* tree. Green proves only that the tree matches the mode you asked about. A bare
   toolchain run once left 37 pages carrying `noindex` and production metadata while the bare
   checker agreed the tree was clean.
2. **Rebuild intentionally, then inspect the generated diff and classify every changed file** —
   canonical / generated / report, and paper-owned / global. Never commit review-banner or
   `noindex` contamination into a published tree.
3. **Prove deterministic regeneration**: build twice from an unchanged spec and require
   byte-identical output, product build **and** intelligence build.

A bare run rewrote the whole review tree once without any gate failing. Mode is therefore
established explicitly against what `main` actually commits — never inferred, never defaulted.
See `LAPTOP_REVIEW_AND_INTEGRATION_PROTOCOL.md` §3.M for the integration-side rule.

---

## 5. IDENTITY AND NAMING

One identity everywhere: the QP id used in the spec filename, the manifest, the page, the
anchors, the deep links and the verification record must be the same string. Anchors must
resolve; deep links must resolve; ids must be unique across papers and questions.

---

## 6. THE LEARNING ARCHITECTURE — FIVE MODES, ONE SPINE

**Frozen. Do not redesign it while producing a paper.** Rationale lives in
`MIW_LEARNING_METHOD_DESIGN.md`; this section states what binds.

### 6.1 Five modes — there is no sixth

```
[ Understand ]  [ Exam Plan ]  [ Answer ]  [ Study Guide ]  [ Recall ]
```

Defined once in `build_paper.py` (`MODES`). **`Answer` is the default open view** — expertise
reversal: a candidate who already knows the topic must reach the model answer without being
walked through scaffolding.

Do not propose a Bullet Answer tab, Summary tab, Cheat Sheet tab, Timeline tab or any other
learning mode. Adding, removing or renaming a mode is a **Founder decision** (§10). Verification
is a *capability*, not a mode: the Reference Shelf sits outside the selector.

Each mode has one job, and they do not borrow each other's:

| Mode | Owns |
|---|---|
| **Understand** | the plain-language mental model, *before* examination phrasing. Conditional — present only where the topic has a genuinely counter-intuitive core. Not a second answer, not a regulation dump, not a mini Study Guide. Must pass the reconstruction test |
| **Exam Plan** | **what the candidate should write in the exam now** — see §6.2 |
| **Answer** | the full verified model answer. Do **not** shorten it because Exam Plan exists |
| **Study Guide** | why the structure scores · distinctions · common mistakes · examiner traps · deeper reasoning · regulatory nuance · currency and temporal context |
| **Recall** | the retrieval / self-test layer — the route with titles blanked, plus flashcards |

### 6.2 EXAM PLAN — the bullet plan is the corpus standard

> **What changed.** Bullet Exam Plan shipped as a QP2608-only pilot behind a `plan_bullets`
> spec flag. It was propagated to the whole solved corpus on 2026-08-17 and **the flag was
> removed deliberately** — it did not disappear by accident. There is now one renderer, no
> opt-in, and no per-paper variation. Do not reintroduce a flag.

**EXAM PLAN = WHAT TO WRITE IN THE EXAM NOW.** The rendering carries:

- source-backed **subpart marks where known** (§6.3);
- **route headings** — the things to write down first;
- the caption `Bullet answer — points to write`;
- **supporting points beneath each heading**;
- the memory cue, where one exists;
- the explicit *Remember N headings · Cover M core points* split.

**Single canonical data source: `answer_route.steps[].points`.**

Never create `bullet_answer`, `short_answer`, `exam_answer`, `bullet_points_v2` or any other
parallel answer corpus. The points the Exam Plan prints are the same points the model answer,
knowledge map and recall test derive from — which is precisely why nothing can drift.

### 6.3 SUBPART MARKS — show them, never guess them

- **If the source paper or spec states subpart marks: show them.**
- **If it does not: do not guess.** Never infer `8+8`, `10+6` or `4+4+4+4` from a total.

A guessed split teaches the candidate a weighting the examiner never published. `limb_marks()`
in `build_paper.py` therefore omits any limb it cannot match, and the caller falls back to the
bare label; `ui_behaviour_test.cjs` guards this ("scaffold limbs and unmarked subparts stay
label-only"). Preserving the source paper's silence is the point.

**Two subpart key conventions coexist** under one `schema_version`: most of the corpus writes
`ref` (`"a)"`), the newest papers write `label` (`"(a)"`). Route `limb` values vary the same way
(`a`, `a)`, `(a)`, `A.`). The renderer reduces both sides to alphanumerics before matching, so
historical records stay compatible. **New authoring should follow the convention the current
schema and neighbouring recent specs use** — but never "normalise" an existing paper as a side
effect of unrelated work.

Where marks are genuinely absent from the print, record the derivation in
`subpart_marks_note` rather than concealing it (`validate_spec.py` warns on its absence).

### 6.4 SOURCE LIMBS ARE NOT AUTHORING SCAFFOLDS

`answer_route.steps[].limb` currently does two different jobs. Real question limbs (`(a)`,
`a)`, `A.`) are examination subparts. Values such as **`framing`, `closing`, `intro`, `main`,
`all`, `d1…d5`, `head 1…head 4`, `qualification`** are **authoring scaffolds** — they are not
subparts and must never be assigned invented marks.

For new production:

- Prefer a clean route structure that expresses the shape **without** a scaffold label.
- Use a scaffold only where authoring genuinely needs it, and never in a way that reads to a
  candidate as a limb that merely lost its marks.
- Never treat an existing scaffold label as evidence that the source paper had that subpart.

Scaffold limbs are candidate-facing today and are a **registered open item** (`CURRENT_STATUS.md`
§6.D). Do not fix them opportunistically inside a paper session — it means editing canonical
spec data corpus-wide.

### 6.5 THE EXAM-PLAN / STUDY-GUIDE BOUNDARY

```
EXAM PLAN    →  what to write NOW
STUDY GUIDE  →  why · traps · nuance · historical and temporal context ·
                "asked before — what changed for today?"
```

**Do not let regulatory history accumulate inside Exam Plan.** A current-law fact belongs in the
Exam Plan only when it is a useful point for the candidate's present answer. Framing such as
*"at this sitting the operative text is …"* is Study Guide material.

This boundary is measured, not assumed: a sweep of all route points found fewer than ten
genuine state-of-law framings corpus-wide (`CURRENT_STATUS.md` §6.G). Keep it that way.

### 6.6 `answer_route` IS LOAD-BEARING — author it deliberately

**`answer_route` is the one canonical sequence for a question. It is authored once**, and every
other surface is *derived* from it: Understand's knowledge map, the model answer's principal
headings, the Exam Plan, Recall's blanks, quick revision, and the structure flashcard.

For every route step:

- **`title`** — a **writable examination heading**. The candidate should be able to put it
  straight on the page.
- **`points`** — the actual scoring and supporting points, authored as short retrieval cues
  (3–8 words), not a second copy of the prose.

Avoid: vague headings · duplicated steps · explanatory essay paragraphs disguised as bullets ·
points that belong only in Study Guide · historical narrative that is not writable in the exam.

Binding consequences:

- **Never author a route twice.** If two surfaces disagree, the route is right and the derived
  surface is a defect.
- **A derived surface must never be more categorical than the verified answer.** If the answer
  is qualified ("generally", "where the administration permits"), the flashcard may not flatten
  it into an absolute. This has already caught a real regression.
- A route is **specific to its question**. Do not reuse a generic route because two questions
  share a topic. The route carries the **core points the examiner is actually testing**.
- A memory cue may point *at* the canonical route; it may never introduce a second sequence of a
  different length.
- Answers render **unhidden**; `health_check.py` verifies learning-layer coherence.

### 6.7 ROUTE SIZE — a warning threshold, not a correctness rule

**There is no bullet cap, and no arbitrary target.** Do not truncate a complex answer to hit a
number, and do not pad a simple one.

Measured across the solved corpus (360 questions, 40 papers, 2026-08-17) — **recompute rather
than trust these figures; they move as the corpus grows**:

| | min | median | p90 | max |
|---|---|---|---|---|
| route headings | 5 | 7 | 9 | 14 |
| core points | 12 | 41 | 61 | 80 |

39 questions carry more than 60 points. `validate_spec.py` warns outside the 4–9 chunking range;
that is a **prompt to look**, not a defect. Eleven questions already sat outside it before the
range was questioned (`CURRENT_STATUS.md` §6.E).

If a new question produces an unusually high heading or point count, **review it for duplication
or poor structure before accepting it** — then accept it deliberately and say so. Route structure
must stay navigable; it must not be trimmed to flatter a statistic.

---

## 7. CANDIDATE-FACING BOUNDARY

Some fields exist for authoring and must **never** face a candidate:

- **`recurrence_class` is an authoring field.** It must never be rendered to a candidate.
- **Provider/host recurrence must not leak.** Which examination provider repeated which
  question is internal intelligence. It has leaked on multiple surfaces before and is now
  guarded — keep it guarded.
- Sample/demo material must be **family singletons**: a demo must not expose a recurrence
  family.

---

## 8. TRUE SOURCE CORPUS BOUNDARY

The True Source corpus is a **separate store**. This repository borrows its **id convention**
only.

- Questions reference corpus **object ids** (e.g. `SOLAS-II2-10`), never PDF page numbers.
- `reference_shelf` stays **empty** until the corpus is actually available here.
- The per-paper demand map is the handoff artefact between the two.

See `MIW_TRUE_SOURCE_CONTRACT.md` only if you are changing this boundary.

---

## 9. REVIEW STATE

While a paper is under Founder review, its pages are **`noindex` and ungated**.
`health_check.py` verifies review state, absence of path leakage, absence of third-party
branding, and correct scoping of production metadata. Do not change gating or indexing as a
side effect of production work.

---

## 10. WHAT REQUIRES FOUNDER APPROVAL

- Merging to `main`.
- Launching or un-gating any paper.
- Changing the frozen V1 template or the learning architecture.
- Changing commercial gating or pricing surfaces.
- Reopening security architecture (frozen — separate scope).
- Deleting or rewriting historical verification records.

When in doubt, produce the work and stop at the boundary with a clear question. Do not cross
it and report afterwards.

---

## 11. THE PRODUCTION SEQUENCE

Nine phases. Desktop owns 1–8; the laptop owns 9 under
`LAPTOP_REVIEW_AND_INTEGRATION_PROTOCOL.md`.

| # | Phase | What it produces |
|---|---|---|
| 1 | **Source intake** | the verified paper: id, month/year, subject, serial, duration, total marks, question count, answer instruction, per-question marks, subpart marks. Stems transcribed **verbatim**. Printed inconsistencies **preserved**, never silently normalised (§11.1) |
| 2 | **Recurrence / donor discovery** | lineage classified against the corpus (§11.2); donors identified cautiously and separately from recurrence (§11.3) |
| 3 | **Current-law research** | every high-risk legal or regulatory claim verified against primary sources for the **sitting date**; temporal changes resolved |
| 4 | **Author** | `understand_first` (where it earns its place) · `answer_route` · full Answer · Study Guide · Recall and flashcards |
| 5 | **Self-review** | marks · limbs · citations · temporal sweeps · donor contamination · currentness |
| 6 | **Build** | in the mode the machine role requires (§4.1) |
| 7 | **Validate** | the governed gate set (§11.4) — 0 failures |
| 8 | **Handoff** | desktop stops; branch pushed; anchor document written |
| 9 | **Laptop integration** | extract paper-owned paths onto **current `main`**, re-review independently, publish build, global gates, deploy if green |

### 11.1 Source truth — preserve the paper, including its errors

**Transcribe the stem verbatim. Preserve printed inconsistencies; never normalise them silently.**

Worked precedent (QP2608): six questions printed at 16 marks each sum to **96**, while the paper's
printed total is **100**. That discrepancy is recorded, not corrected — a spec that quietly makes
the arithmetic work has replaced the source paper with a tidier one that never existed.

**Where the printed premise is wrong, do not rewrite the question.** The answer:

1. states the correct position;
2. briefly corrects the premise;
3. **still performs the task the examiner asked for.**

Worked precedent (QP2608-Q9): the paper posits *two consecutive D ratings*, where the rule is
**three consecutive D, or one E**. The answer names the correction, notes the ship is one year
short of the threshold, and then delivers the requested corrective-action plan. Silently
answering the wrong scenario, and refusing to answer at all, are both failures.

### 11.2 Lineage classification — use the existing vocabulary

Adjudicate lineage by **reading historical stems**, never by score alone, into the five
**production** classes (`LAPTOP_REVIEW_AND_INTEGRATION_PROTOCOL.md` §3.F):

| Class | Means |
|---|---|
| `EXACT` | the same printed task, same wording |
| `NEAR` | materially reworded, same task |
| `FAMILY` | the same core ask, differently framed |
| `RELATED` | same topic only |
| `UNIQUE` | no meaningful match |

This is the vocabulary a **human adjudicates in and a paper records**. Same topic is **not**
automatically recurrence.

#### Three layers, three vocabularies — do not "harmonise" them

Two sibling vocabularies exist by design. They are **not** competing names for the production
classes, and neither is a defect to be cleaned up:

| Layer | Vocabulary | Who assigns it |
|---|---|---|
| **Production adjudication** (this section) | `EXACT` `NEAR` `FAMILY` `RELATED` `UNIQUE` | a human, by reading stems |
| Six-year intelligence classifier (`build_sixyear_intelligence.py`) | `EXACT_REPEAT` `NEAR_REPEAT` `UNIQUE` | computed over historical stems |
| Recurrence display status (`recurrence_model.py`) | `repeat_exact` `repeat_near` | derived, for rendering |

The machine classes are **coarser on purpose** — a classifier cannot separate `FAMILY` from
`RELATED` without reading for intent, which is the adjudicator's job. So a computed
`EXACT_REPEAT` is **evidence for**, not a substitute for, an adjudicated `EXACT`; QP2306-Q1 is
the worked precedent, where the classifier's `EXACT_REPEAT` established wording ancestry to an
unsolved October 2022 root while `reused_from` correctly stayed null.

**Do not add a fourth vocabulary, and do not rename an existing one.** Question Intelligence v2
may use richer research terminology internally, but any future integration must **explicitly map
its research classes onto the five production classes above** rather than silently creating
competing meanings. Renaming or collapsing any of these three is a Founder decision, not
tidying.

**Recurrence can occur at limb level.** Never write *"this entire question repeated"* when only
one 4- or 6-mark limb repeated. Never invent a historic sitting date from group feedback or
coaching material — an unverified date is a fabricated citation.

### 11.3 Donor use — starting point, never copy authority

For every donor: verify the exact question relationship · check current-law currency · remove
donor-only limbs · adjust marks and scope · re-anchor evidence · run the temporal sweep. Record
the three deltas (`TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md` §4).

**Never copy a 16-mark donor into a 6-mark repeated limb.** And never copy an old current-law
claim forward: check for repealed statutes, replacement Acts, IMO amendments, changed
entry-into-force status, new limits, changed terminology, new class/IACS positions and new
practice.

> **An old question does not mean an old answer.**
> Historical sources establish **what was asked**. Current primary and verified authority
> establishes **what should be written now**. The current canonical answer always controls the
> Exam Plan.

### 11.4 Validation baseline

Run the governed checks in the sequence at `QA_AND_HANDOVER_PROTOCOL.md` §1, covering: spec
validation · publish/review build · UI behaviour · question-year · sample · reuse · recurrence ·
known traps · temporal · health · audit · home contract · solvedQP checker · delivery gate ·
strict derivation · determinism.

**Require 0 failures.** Do not hardcode an expected test count into a report — suites grow, and a
frozen number becomes a false assertion.

Every new paper needs its own **UI behaviour fixture**. A missing fixture must fail, not quietly
produce fewer assertions and pass. Prove every search probe **unique under the search's own
semantics** before writing it down; reject ambiguous probes. Mutation-test a relaxed or new guard
where practical.

### 11.5 Exam Plan acceptance — test this explicitly on every new paper

- Can a candidate open **Exam Plan alone** and reconstruct a credible answer without reading the
  full Answer?
- Do subpart marks show **where known**, and are they absent where the source is silent?
- Are the headings **writable** as they stand?
- Are the bullets current for the sitting?
- Do bullet weights roughly respect the marks?
- Are legal and regulatory distinctions preserved, not flattened?
- Are procedural questions sequenced correctly?
- Does it remain usable on mobile (375 px, no horizontal overflow)?

No bullet-count target. Do **not** add a headings-only toggle to Exam Plan — that duplicates
Recall.

### 11.6 Memory cues

Prefer authoring a useful memory cue during production rather than leaving new debt. A cue is
**not** a hard blocker for a new paper unless governance says so elsewhere, and **historical
backfill is out of scope for a paper session** — 20 of 360 questions currently carry none
(`CURRENT_STATUS.md` §6.F).

---

## 12. GLOBAL SIDE EFFECTS — explain every changed file

A new paper legitimately changes existing generated surfaces: recurrence families, reuse maps,
year indexes, counts, storefront counts, latest-sitting metadata.

**Do not assume "a new paper should only add new files."** But **every changed old file must be
explained.** Classify each; where the generated diff is wider than the paper, compare
representative untouched pages byte-for-byte against `origin/main`.

A newly published paper may move paper count, question count, newest sitting and month
availability. Storefront guards must stay green — when a guard reports a mismatch, update the
**page**, never the checker.

**Never change pricing or commercial product scope during ordinary QP production.** Do not touch
Razorpay, refund logic, entitlements or access product definitions unless explicitly tasked.
Written access remains a separate product from Oral. See `SOLVED_QP_COMMERCIAL_ARCHITECTURE.md`.

---

## 13. PUBLICATION PROOF

**HTTP 200 or 302 is not deployment proof.** The access gate is path-agnostic: a redirect that
302s every path also 302s a path that does not exist. Prove deployment from a public surface
whose **content actually moved**, or from the exact deployed commit SHA. Then confirm the paid
route is still protected and that no paid text is served anonymously.

---

## 14. QUESTION INTELLIGENCE v2 — NOT CANDIDATE-FACING

QI-v2 is under separate research governance and is **not** part of paper production.

Historical recurrence intelligence may later surface in **Study Guide**, at whole-question or
limb level. Author `answer_route` and lineage records so they stay compatible with that — but
**do not depend on unfinished research**, and **do not candidate-publish** old sitting dates,
Paper DNA, temporal blocks or setter hypotheses until QI-v2 governance approves them.

Do not start QI-v2 work inside a paper session.
