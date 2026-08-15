# LAPTOP REVIEW AND INTEGRATION PROTOCOL

**Governed by `PRODUCTION_PROTOCOL_INDEX.md`. Read every laptop review/integration session.**

Stable method only. No paper-specific facts, no current HEAD, no counts, no queue, no branch
timestamps, no donor readiness, no pricing — those are repo truth or session delta.

This file owns the **LAPTOP** role. It does not restate what the governed set already owns:

| Already owned elsewhere | Read there |
|---|---|
| source authority ladder, spec→HTML, learning architecture, candidate-facing boundary, True Source boundary, what needs Founder approval | `PASTPAPER_PRODUCTION_PROTOCOL.md` |
| sitting-date truth, donor reuse, recurrence, contamination sweeps | `TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md` |
| validation sequence, determinism, positive controls, UI verification, the `solvedQP/QP####.html` staging gate, state/history/lessons ownership | `QA_AND_HANDOVER_PROTOCOL.md` |
| how to execute efficiently, server teardown | `EXECUTION_EFFICIENCY_POLICY.md` |

---

## 1. THE TWO ROLES ARE NOT THE SAME JOB

| | DESKTOP | LAPTOP |
|---|---|---|
| Produces | paper-specific candidate material from donors | nothing new; adjudicates what was produced |
| Authority | proposes | **decides** |
| Output | a `pastpapers/qp####-founder-review` branch | corrected paper integrated on `main`, published, verified live |
| Ends at | branch pushed | one paper LIVE, then **stop** |

**The desktop branch is candidate input, not authority.** Its anchor document is the producer's
own account of its work. Read it — it is usually excellent and will save hours — but every
substantive claim in it is a claim to be tested, not a finding to be accepted.

---

## 2. INVARIANTS

1. **Never merge a founder-review branch wholesale.** It was cut from an older `main` and a merge
   presents everything `main` gained since as a deletion. Extract the **paper-owned files** onto
   current `main` instead: the spec, the paper page, the anchor/review doc, the verification
   records. Prove the extraction list is complete and that nothing else moved.
2. **Repo truth wins over the prompt.** The prompt states expected HEAD, counts and queue as a
   convenience. Verify each. Where they differ, the repository is right and the difference is
   reported, not silently absorbed.
3. **The corpus is the source of truth for what the corpus holds.** Never accept an authored
   sentence about holdings, coverage or absence without checking. Distinguish: official source
   file held · structured object held · exact text available · paraphrase only · citation-ready ·
   quotation-ready. "Held" does not mean "quotable" — an image-only scan is neither.
4. **Never invent a citation.** No regulation, article, resolution, circular, date, threshold or
   percentage may be asserted unless verified. If it cannot be verified, say so and stop if it is
   material. This binds corrections as hard as it binds authoring.
5. **Do not mutate the True Source corpus.** Record defects through the governed referral
   mechanism, verify the answer independently, and carry the referral rather than re-raising it.
6. **One paper. Then stop.** Do not begin the next paper because the tooling is warm.
7. **A review corrects the paper; it does not redesign the system.** Reviewing one paper regularly
   exposes a defect in shared machinery — a classifier, a checker, a corpus-wide vocabulary class,
   a security surface. Those are **reported, not rebuilt**, and the finding is written down with
   enough evidence that the owning session can act. If a genuinely new *repeatable* defect warrants
   a guard, add one narrow deterministic guard with its positive control — never a framework, and
   never a second source of truth inside a checker to make a page pass. Fix the page; the guard
   states the truth.

   The test for acting rather than reporting: the defect is **in this paper**, or shipping this
   paper would newly expose customers to it.

---

## 3. WORKFLOW

### A. Repo truth, before any mutation
`status` · `fetch --prune` · current `main` · every relevant remote branch and its tip · confirm
the target branch is **stable** (not moving under you) · note any branch that appeared since the
prompt was written. Record the starting HEAD; you will report the ending HEAD against it.

### B. Extract, do not merge
Per invariant 1. Confirm each extracted path was previously absent (or diff it deliberately).

### C. Source adjudication
Verify independently from the source copy: serial · sitting month/year · page count · **question
count** · printed marks (and their absence) · rubric · anomalies · typos · malformed subparts.

- **Count questions by reading the rendered pages.** Numbering is inconsistent across sittings and
  a naive pattern both under-reads and collides with the rubric list.
- Prove every `text_verbatim` traces to the source text layer.
- **Printed defects are preserved, never silently repaired** — and a misprint that changes what is
  being asked must be named as such in the answer.
- Where marks are not printed, the derivation must be recorded rather than concealed. A later
  sitting of the same question that *does* print marks is legitimate corroboration.

### D. Q1–Q9 independent adjudication
For each: read the stem, identify every limb and command verb, determine what a correct MEO Class I
answer requires **before** reading the produced answer, then compare. Check technical substance,
legal/regulatory substance, numbers, dates, limits, terminology, omissions, padding, wrong emphasis,
temporal contamination, stale corpus claims.

Return **PASS** or **CORRECTED** per question, with the substance of each correction.

Three failure modes worth hunting specifically, all observed in production:

- **A wrong premise authored once is then derived coherently everywhere.** When you correct a
  substantive claim, sweep the whole question — model answer, route, understand, study notes,
  recall, cue, cards, regulations, decomposition, unresolved — not just the paragraph you noticed.
  Corrections routinely touch double figures of sites.
- **An audit can introduce a defect, not only inherit one.** The standing assumption is that a
  later donor over-claims and must be stripped back. Check the donor: if the live donor states the
  law correctly and the paper under review does not, the reversal ran the wrong way.
- **A correct citation can carry wrong content.** Verify what the cited paragraph *says*, not that
  the paragraph number is plausible.

### E. Temporal correctness
The Model Answer must be right **as at the sitting date** — see
`TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md`. Two laptop-specific points:

- Sitting-date truth can differ sharply **inside one calendar year**; a same-year donor is not
  automatically safe in either direction.
- Later law may appear only where governed — as trap, later development, current comparison or
  Study Guide context — and never as operative at the sitting.

### F. Lineage
Adjudicate `EXACT` / `NEAR` / `FAMILY` / `RELATED` / `UNIQUE` by **reading historical stems**, never
by score alone. Keep **wording ancestry** separate from **answer donor**: an identical question is
not an identical answer, and historical unsolved questions are intelligence evidence, not answer
authority. Sanity-check the automated classification — a preserved misprint or a print-only
difference can make a genuine recurrence classify as `UNIQUE`.

### G. Learning quality
Five modes, no sixth: Understand · Exam Plan · Answer · Study Guide · Recall. Each has a distinct
job; the architecture is frozen. Understand must pass the **reconstruction test** — strip the formal
terms and the explanation must still let a candidate rebuild what the issue is, how it works and why
the answer is shaped that way (plain idea → mechanism → formal term). Recall must test retrieval,
not reprint the answer. The route must be question-specific and cover every limb.

### H. Candidate-facing hygiene
Sweep the **rendered delivery bytes** — the paid page, not the review page, which carries production
metadata by design. Adjudicate context; do not substring-match. Legitimate technical language that
collides with internal vocabulary stays (e.g. *delivery without production of the bill*, CLC's
*second and third tiers*, CSS comments about desktop breakpoints). Genuine leaks are internal
identifiers, corpus paths, provenance vocabulary and production process words.

### I. Terminology and traps
Run the governed trap suite. Never broad-replace a technical term. A declared correction may still
miss **abbreviated or bare variants** of the same defect, so scope a terminology sweep to every form
of the term, not the form that was reported.

### J. UI fixture
If the paper has no fixture, author one — a page with no fixture must fail rather than pass quietly.
**Prove every probe unique against the real card payloads under the search's own semantics**
(token-AND over the search payload, not substring over the visible text) before writing it down. A
probe matching two cards still passes its assertion and still reports green, which is why uniqueness
is proved rather than assumed. Alias probes must appear **only** in search metadata — check
visibility with tag boundaries treated as hard breaks, because collapsing whitespace joins adjacent
elements and manufactures false matches.

### K. Intelligence graduation
Graduation is a builder rule. **Never hand-delete a historical record.** Prove three things:
solved **+1**, intelligence-only **−1**, combined universe **unchanged**.

### L. Regeneration and public derivation
Regenerate every governed derived artefact from the canonical spec. Never hand-edit generated HTML
where a builder exists.

The storefront is hand-maintained and **guarded**: when the guard reports a mismatch, update the
**page**, never the checker. Verify paper count, question count, the **per-year month list**,
newest sitting, and that pricing did not move. Totals can be correct while a per-year month list is
stale — that is a real defect class the year-level check alone will not catch.

### M. Gates
`validate_spec` · full toolchain · traps · recurrence · temporal · UI behaviour · search · home
contract · coverage · storefront · corpus consumer · security/access · leakage ·
**`delivery_gate.py --verify-derivation --strict`**.

Stage generated artefacts **explicitly** — `git add -u` misses new files, and a generated delivery
page is untracked on the paper's first integration. See `QA_AND_HANDOVER_PROTOCOL.md` §6.

**Build the tree in the mode `main` commits, then check it in that mode.** `main` commits the
**publish** build. `run_toolchain.py --publish` is therefore the pre-commit gate; the bare run is
not. The final integration gate must establish **explicitly that the tree is in the same build
mode `main` commits** — not merely that some checker returned zero errors.

**A mode-flagged checker is mode-symmetric, so green proves only that the tree matches the mode
you asked about.** `health_check.py` faults a review tree that is not `noindex` and equally faults
a publish tree that still carries `noindex`. The two assertions are exact complements, so
whichever build the tree holds, one of the two invocations always returns 0 errors. **Never choose
the mode because it comes back green** — choose the mode `main` commits, and make the tree satisfy
it. A review-mode toolchain run once left 37 pages carrying `noindex` and production metadata while
the bare checker agreed the tree was clean; only comparing against what `main` actually commits
exposed it. Where the build state is genuinely ambiguous, resolve it against the current
`origin/main` convention, never against a checker's exit code.

**Generated pages this paper does not own must stay byte-identical to their `main` baseline**,
unless a legitimate global derivation change explains the drift — graduation, family recomputation,
or shared derived data. When the generated diff is wider than the paper, compare representative
untouched pages byte-for-byte against `origin/main`.

Before treating any alarming standalone result as a regression, **prove it against the previous
commit** — if the prior state reports identically, it is pre-existing and it is not yours.

### N. Determinism
Build twice; require byte-identical output. Product build **and** six-year intelligence build. This
is publication proof, not polish.

### O. Visual QA
One batched browser session over HTTP (never `file://`), desktop and mobile widths, explicit
teardown. Verify question anchors, five modes, mode switching, no horizontal overflow, no console
output, corrected text actually **rendered**, and no host/provider residue. Note that hidden panes
return nothing from `innerText`; use `textContent` when asserting presence in a collapsed surface.

### P. Cross-machine safety, immediately before commit
`fetch --prune` again. Re-check `main` and every queue branch. If the target branch moved during
review, **stop and reconcile**.

### Q. Publication
Commit, push, verify deployment.

**A path-agnostic paywall redirect is not existence proof.** A gate that 302s every path 302s a path
that does not exist. Prove the deploy from something that actually changed: a public surface whose
content moved, or the deployed commit SHA. Then confirm the paid route is protected and that no paid
text is served anonymously.

### R. Stop
Recompute queue readiness from actual current branches and recommend **one** next paper.

---

## 4. STOP CONDITIONS

Stop and report rather than proceed if: the target branch is moving · the source is ambiguous · a
donor relationship is not as reported · an authoritative claim cannot be verified · a temporal
question cannot be resolved · graduation breaks or the combined universe changes unexpectedly ·
storefront derivation breaks · a trap regresses · the build is non-deterministic · **the tree's
build mode cannot be established against what `main` commits** · the delivery gate fails · a
security regression appears · a cross-machine collision occurs.

---

## 5. VARIABLE INPUTS — what a session prompt must still supply

Everything else is discovered from repo truth.

**Required**
- target QP id and sitting
- where to stop (normally: one paper, then stop)

**Supply when they exist — these cannot be derived safely**
- paper-specific known risks or source hazards
- known donor dependencies this paper discharges or depends on, and any question flagged as a
  **future donor** (review those hardest — they propagate)
- prior-session corrections, referrals or open items that bear on this paper
- any deviation from the normal flow (a paper to be reviewed but not published, a deliberate
  ordering constraint, a Founder decision already taken)

**Never in the prompt, because it goes stale**
current HEAD · corpus counts · queue membership · branch tips · donor readiness · test counts ·
pricing · campaign state.

---

## 6. REPORT SCHEMA

Sections may say **not applicable**. Do not fabricate content to fill one, and do not pad — a long
report is not a quality signal.

```
A. REPO                  starting HEAD, branch tip, remote movement, ending HEAD
B. SOURCE                serial, sitting, pages, questions, marks, anomalies
C. Q1-Q9 VERDICTS        PASS / CORRECTED, with the substance of each correction
D. LINEAGE / DONORS      classes, roots, what this paper donates and any reuse caveat
E. TEMPORAL / LEGAL      sitting boundary, instruments excluded, primary sources used
F. CORPUS HOLDINGS       stale claims found and corrected
G. LEARNING QUALITY      five modes, routes, reconstruction test
H. TERMINOLOGY / TRAPS   trap suite result, any new terminology defect
I. GRADUATION            solved before/after, intelligence-only, combined universe
J. QA / DETERMINISM / SECURITY
K. PUBLICATION           commits, deployment proof, live totals
L. QUEUE                 current branches and readiness
M. NEXT RECOMMENDATION   exactly one paper
N. DEFERRED / REFERRALS  what was deliberately not done, and why
```

---

## 7. WHAT THIS PROTOCOL DOES NOT COVER

Marketing, campaign copy, social proof, pricing, Terms, trial architecture, the future
2017–2026 Question Intelligence product, Study Compass, the Dual-Time Answer View, and the
Product Security Check are **out of scope for a review session** and are not to be touched as a
side effect of integrating a paper. They are separate roadmap concerns with their own governance.
