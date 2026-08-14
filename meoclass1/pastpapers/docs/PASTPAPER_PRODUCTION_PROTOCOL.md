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

---

## 5. IDENTITY AND NAMING

One identity everywhere: the QP id used in the spec filename, the manifest, the page, the
anchors, the deep links and the verification record must be the same string. Anchors must
resolve; deep links must resolve; ids must be unique across papers and questions.

---

## 6. THE LEARNING ARCHITECTURE — SINGLE SPINE

**`answer_route` is the one canonical sequence for a question. It is authored once.**

Every other learning surface is *derived* from it:

- the study guide / Understand view
- the Map
- Recall (blanks)
- Rapid Revision / cheat-sheet
- retrieval flashcards

Binding consequences:

- **Never author a route twice.** If two surfaces disagree, the route is right and the
  derived surface is a defect.
- **A derived surface must never be more categorical than the verified answer.** If the answer
  is qualified ("generally", "where the administration permits"), the flashcard may not
  flatten it into an absolute. This has already caught a real regression.
- Answers render **unhidden**; the learning layer must remain coherent across map, recall and
  flashcards. `health_check.py` verifies this.

### Question-specific routes and the core-point principle

A route is specific to its question. Do not reuse a generic route because two questions share
a topic. The route carries the **core points the examiner is actually testing** — the marks
live there, not in surrounding narrative.

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
