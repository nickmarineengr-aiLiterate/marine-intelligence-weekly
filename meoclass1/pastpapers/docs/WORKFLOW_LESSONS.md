# WORKFLOW LESSONS — Past Written Papers

**Governed by `PRODUCTION_PROTOCOL_INDEX.md`. Read only the entries relevant to the task in
hand. Do not load this whole file by reflex.**

This is the Production Intelligence Layer's memory. Same format and discipline as
`known_traps.md`, and for the same reason: a thing this project learned the expensive way,
written down once, so the next session does not pay for it again.

**`known_traps.md` holds facts about the SUBJECT.** A regulation we drafted wrong.

**This file holds facts about the WORK.** A way of working that failed, or that was proven
and should be repeated.

No entry here states a regulatory, legal or technical fact. If a lesson needs one, it belongs
in `known_traps.md` or in a verification record instead.

---

## HOW TO READ AN ENTRY

Each entry carries trailers:

```
EVIDENCE:  what actually happened, with the paper/commit/file it happened in
CATEGORY:  one of the categories below
STATUS:    CANDIDATE | PROVEN | PROMOTED_TO_TOOL | PROMOTED_TO_POLICY | REJECTED | SUPERSEDED
SEEN:      how many separate production events support it — real counts only, never inflated
OWNER:     the tool or protocol file that now enforces it, or NONE
REVISIT:   the condition under which this conclusion should be reopened
```

`REVISIT:` is mandatory on every REJECTED and every CANDIDATE entry. A rejection with no
reopening condition is dogma, and dogma is how a decision that was right on one machine, or
one corpus size, quietly becomes wrong.

**Categories:** `PROCESS_LIFECYCLE`, `SOURCE_HANDLING`, `DONOR_ADAPTATION`,
`TEMPORAL_VERIFICATION`, `BUILD_QA`, `STATE_HANDOVER`, `SURFACE_IMPACT`, `AUTOMATION`,
`REJECTED`.

---

# PART 1 — PROVEN LESSONS

---

### 1. Future-contamination checks must be DATE-granular, not year-granular

A contamination sweep that compares only the **year** cannot see the failure that actually
happened. The dangerous case is same-calendar-year: an instrument adopted in December of the
sitting's own year, cited in a paper sat in September of that year.

QP2509 Q9 (September 2025) inherited from its donor QP2606-Q8 (June 2026) the claim that
resolution **A.1207(34)** was the operative HSSC Survey Guidelines. That resolution was
adopted **3 December 2025** — three months *after* the sitting, in the *same calendar year*.
The correct edition at the sitting was A.1186(33). The defect had reached **fourteen
surfaces** of the question before it was caught.

The same Assembly session is a standing boundary for every 2025 sitting, and it recurred:
QP2510 carries A.1208(34) from the same 34th Assembly.

Compare against the **sitting month**, at minimum.

```
EVIDENCE:  QP2509 Q9 — A.1207(34)/3 Dec 2025 in a Sept 2025 paper, reversed on 14 surfaces
           (spec Q9 temporal_review notes 1-3). QP2510 — A.1208(34), same Assembly boundary.
CATEGORY:  TEMPORAL_VERIFICATION
STATUS:    PROVEN → PROMOTED_TO_TOOL
SEEN:      2
OWNER:     tools/pastpapers/temporal_sweep.py (POST_SITTING_DATE_CANDIDATE)
REVISIT:   if a spec ever records an exact exam DAY, tighten the comparison from month to day.
```

---

### 2. Donor adaptation must sweep for internal Q-references in prose

A donor's prose refers to the donor's **own** question numbering. Copied forward, it points at
a question in the target paper that is about something else entirely — and it reads perfectly.

QP2509 Q2 inherited three `See Q8` pointers from donor QP2508 Q2. QP2508's Q8 was the
Net-Zero Framework question. QP2509's Q8 is the human element. The pointers survived on
`major_trap`, the study-guide instrument comparison, and the regulation and source map — all
candidate-facing.

Sweep for the bounded prose forms: `See Qn`, `Qn of this paper`, `Qn of the same paper`,
`refer to Qn`, `as discussed in Qn`. A **structured** `cross_links` entry is not this defect —
it names its paper and is controlled.

```
EVIDENCE:  QP2509 Q2 — three inherited "See Q8" pointers removed (spec Q2 reuse_evidence[5],
           temporal_review/notes[2]).
CATEGORY:  DONOR_ADAPTATION
STATUS:    PROVEN → PROMOTED_TO_TOOL
SEEN:      1
OWNER:     tools/pastpapers/temporal_sweep.py (INTERNAL_QREF_CANDIDATE / _OUT_OF_RANGE)
REVISIT:   if a target ever legitimately needs a same-paper prose pointer, the sweep stays and
           the hit is adjudicated — do not weaken the pattern to make one paper quiet.
```

---

### 3. Derived readiness must never be frozen as intake truth

`reuse_tier` in a spec records what was true when the spec was written. Building a *later*
paper can turn an earlier paper's tier C into a tier D without any spec being touched, because
a donor that did not exist then exists now.

Reading the stored field as current truth misclassified six questions across five papers;
five moved C→D once the tier was derived from the built set instead.

The general form: **anything downstream of "what exists now" must be derived at read time, not
stored at write time.**

```
EVIDENCE:  reuse-tier classification defect, 2026-08-11 — 6 questions misclassified, 5 C→D.
CATEGORY:  AUTOMATION
STATUS:    PROMOTED_TO_TOOL
SEEN:      1
OWNER:     tools/pastpapers/recurrence_model.py :: derive_reuse_tier()
REVISIT:   if another stored field is found being read as current state, this entry generalises
           and should be restated as a rule rather than a single fix.
```

---

### 4. A partially authored paper is not a valid canonical build state

A session that cannot finish a paper must not leave half its questions in the canonical spec.
The build rejects it, the corpus counts lie, and the next session inherits an object that is
neither intake nor product.

QP2403 stopped at 2/9 and QP2509 reached 3/9; both required the incomplete work to be moved
out of the spec. QP2509 used a governed staging area outside `specs/` and applied it back in
one asserted step when the paper was complete.

Stage outside the canonical spec. Finish, then land.

```
EVIDENCE:  QP2403 stopped 2/9 (2026-08-10). QP2509 3/9 violated PASTPAPER_PRODUCTION_PROTOCOL
           §3; staged under meoclass1/pastpapers/staging/QP2509/ and applied at completion.
CATEGORY:  PROCESS_LIFECYCLE
STATUS:    PROMOTED_TO_POLICY
SEEN:      2
OWNER:     PASTPAPER_PRODUCTION_PROTOCOL.md
REVISIT:   NONE expected — but if staging itself is ever found drifting from the spec, the
           staging mechanism needs its own equality check.
```

---

### 5. Prefer exact asserted substitution to broad blind replacement

For a high-risk structured edit, an applier that **asserts the exact expected old value** and
fails loudly when it does not match is worth far more than a substitution that quietly matches
more than intended.

The QP2509 staging applier worked this way, and re-running it was idempotent rather than
destructive.

```
EVIDENCE:  meoclass1/pastpapers/staging/QP2509/apply_staged.py (in history at 25e049f;
           retired at a5f2551 once applied).
CATEGORY:  BUILD_QA
STATUS:    PROMOTED_TO_POLICY
SEEN:      1
OWNER:     QA_AND_HANDOVER_PROTOCOL.md
REVISIT:   NONE expected.
```

---

### 6. A guard that has never been demonstrated to fail is not proven

A check that has only ever passed is indistinguishable from a check that cannot fail. Several
in this toolchain have been caught in exactly that state: a glob matching nothing sums to
return code 0 and prints PASS, deleting a whole stage while reporting success.

Every guard carries a positive control that **mutates the input and asserts the guard fires**.
This is why `--self-test` exists on the validators, and why the QP2509 QA pass deliberately
broke `health_check` to confirm it was caught.

```
EVIDENCE:  UI BEHAVIOUR stage rewritten to derive pages from specs after a glob-matches-nothing
           PASS was identified (run_toolchain.py). QP2509 QA: health_check broken on purpose,
           correctly caught (2026-08-11).
CATEGORY:  BUILD_QA
STATUS:    PROMOTED_TO_TOOL and PROMOTED_TO_POLICY
SEEN:      2
OWNER:     run_toolchain.py --self-test; every *_check.py and the two PIL tools
REVISIT:   NONE. A new guard without a positive control is not acceptable.
```

---

### 7. A valid internal change can move public, free and paid surfaces indirectly

Solving one paper regenerates derived artefacts across the whole product. Those artefacts
include **public, free and commercial** pages that were not the target of the session.

Solving QP2509 changed the public free January 2026 sample, the public index, both questions
year sheets, both topic pages, the shipped search payload — and `QP2601.html`, a *paid* page.
Every guard passed, correctly. Nothing surfaced that a free page and a paid page had moved.

Measured retrospectively, this is not a one-off: the QP2506 range moved five public surfaces
including the same free sample. It has been happening on every paper build.

Regeneration is *permitted* to do this. Doing it *invisibly* is not.

```
EVIDENCE:  c5e85f2^..a5f2551 (QP2509) — 7 public-free changes + 1 non-target paid page.
           f610818^..6a790b2 (QP2506) — 5 public-free changes. Both measured 2026-08-11.
CATEGORY:  SURFACE_IMPACT
STATUS:    PROVEN → PROMOTED_TO_TOOL
SEEN:      2
OWNER:     tools/pastpapers/surface_impact.py
REVISIT:   if a non-target PAID page change is judged to warrant the same escalation as a
           public one, widen the escalation set — that is a Founder decision, and the tool
           currently reports it as a separate NOTE rather than deciding.
```

---

### 8. PIL flags; Claude adjudicates

The two sweeps above report **candidates**, never errors. A post-sitting date can be entirely
correct for its sitting: QP2509 Q9's study guide deliberately tells the candidate that
A.1207(34) was adopted after their exam, and QP2509 Q8's "expected December 2027" for the MLC
2025 amendments is derivable from MLC Article XV and was published by IMO in April 2025 —
before the sitting.

A tool that suppressed those would be making a legal judgement from a string. So no
suppression on `not yet` / `expected` / `future` exists, and none should be added. Noise is
controlled by **field targeting**, which is mechanical, not by guessing at meaning.

```
EVIDENCE:  QP2509 Q8 forward date verified correct against MLC Art XV(6) and XV(8), 2026-08-11.
           QP2509 Q9 candidate-facing warning text legitimately contains 3 December 2025.
CATEGORY:  AUTOMATION
STATUS:    PROMOTED_TO_POLICY
SEEN:      2
OWNER:     temporal_sweep.py; EXECUTION_EFFICIENCY_POLICY.md rule 9
REVISIT:   NONE. If a suppression is ever proposed it must be proven mechanically safe first.
```

---

### 9. Provenance fields must stay outside a contamination sweep

`sources`, `verification_status`, `reverify_before_publication`, `temporal_review`,
`decomposition_gate` and `reuse_evidence` carry post-sitting dates **by construction** — they
record when the work was done, which is always after the sitting.

Worse, they are where a *removed* defect is written down. QP2509 Q2 records that three
`See Q8` pointers were removed; QP2509 Q9 records the full A.1207(34) reversal. A sweep over
those fields flags the audit trail that proves the fix, which is the same self-trip
`known_traps_check.py` already guards with `EXEMPT_PATHS`.

Scope a contamination sweep to what a candidate reads.

```
EVIDENCE:  found while building temporal_sweep.py, 2026-08-11 — the only surviving "See Q8"
           strings in QP2509 are in the records describing their own removal.
CATEGORY:  AUTOMATION
STATUS:    PROVEN → PROMOTED_TO_TOOL
SEEN:      1
OWNER:     temporal_sweep.py :: CANDIDATE_FACING / EXCLUDED_INTERNAL
REVISIT:   if a provenance field ever starts being rendered to candidates in publish mode,
           this exclusion must be re-argued.
```

---

### 10. Separate the LAYER a defect lives in from the layer it is noticed in

The QP2509 miss was recorded for three sessions as "host recurrence edges are directional in the
**donor derivation**", and the recorded fix was "symmetrise the edges". Both were wrong about the
layer, and acting on either would have damaged the model.

The donor derivation was **already symmetric**. `build_families` unions `reused_from` as an
undirected edge, so an edge recorded on *either* side traverses *both* ways — a synthetic
one-sided fixture proves it in both directions. There was nothing there to fix, and
"symmetrising" it would have meant inventing edges.

The directionality was one layer **up**, in discovery. The third-party host prints a *cumulative*
table: measured over this corpus, **819 tokens — 551 backward, 252 self, zero forward**. It is
structurally incapable of naming a later sitting. MIW produces newest-paper-first. So the only
machine-readable trace of a relationship always sat on the paper MIW had *already* solved,
pointing at the paper it had not — invisible in the direction of travel.

Naming the layer correctly also dissolved the blocker. R4 deferred the fix because symmetrising
edges "needs a semantic equivalence oracle". Inverting an *annotation* into a queue for a human
needs no oracle at all: the tool moves visibility, the author still makes every judgement.

**Before fixing a defect, reproduce it and confirm which layer it is actually in.** A defect
recorded against the wrong layer proposes a dangerous fix and looks unfixable.

```
EVIDENCE:  pre-QP2404 hardening session, 2026-08-11. Pre-authoring rewind reproduced QP2509-Q6
           deriving tier C with QP2601-Q2 already built; one-sided synthetic fixtures proved
           build_families was never directional; 819-token direction census.
CATEGORY:  DONOR_ADAPTATION
STATUS:    PROVEN → PROMOTED_TO_TOOL
SEEN:      1
OWNER:     recurrence_model.reverse_hint_candidates + build_reuse_map self-test cases 8-11
REVISIT:   if a host source ever prints a forward-looking annotation, the census premise breaks
           and the inversion must be re-derived rather than assumed.
```

---

### 12. A filter that returns nothing is a claim, not a result

The prospective PIL sweep over QP2404's donor specs was filtered down to the donor questions with
a one-line comprehension keyed on `question_id`. It printed **"TOTAL findings 411 | ON MY DONORS:
0"** — a clean bill of health for exactly the material about to be adapted.

The field is called `question`. Every row failed the test, so the filter could only ever return
zero. Re-run with the right key it returned **13** findings, four of which were real defects that
would have been copied into the target paper — the donor cross-references that point at an LLMC
question this paper does not have.

The dangerous property is that the false clean is **indistinguishable from success** and arrives
in the shape you were hoping for. A sweep that reports nothing is the single easiest result to
accept without reading.

**When a filter, query or sweep returns zero, prove the zero before believing it** — dump one raw
record and check the keys, or assert that a known-positive row survives the filter. This costs one
command. The protocol already says the sweeps are what clear a paper; a sweep silently filtered to
nothing clears nothing while appearing to.

```
EVIDENCE:  QP2404 session, 2026-08-11. Scratch filter on temporal_sweep.py --json keyed on
           'question_id' where the field is 'question'; reported 0 findings on the donor set,
           actual 13, of which 4 were real INTERNAL_QREF defects in QP2506-Q6 / QP2508-Q6.
CATEGORY:  BUILD_QA
STATUS:    PROVEN
SEEN:      1
OWNER:     NONE - this is an operator discipline, not a tool behaviour. temporal_sweep.py itself
           was correct throughout and reported all 411 findings.
REVISIT:   if scratch querying of tool JSON becomes frequent enough to justify it, give the
           sweeps a --question filter so the key is never retyped by hand.
```

---

### 13. An authoring-date leak is a FIELD-CLASS defect, not a string defect

`QP2601-Q9` carried *"nothing had been adopted as at August 2026"* on a **January 2026** paper.
The obvious reaction is to purge the string. That would have been wrong in both directions.

A corpus-wide scan found the same string in three different kinds of field:

| Where | Renders to a candidate? | Verdict |
|---|---|---|
| `study_notes` | **YES** — Study guide mode | **DEFECT.** Dates the product and is not a statement about the sitting. |
| `unresolved` | NO — inside `if not publish:` | **CORRECT.** Honest authoring context, properly quarantined. |
| `reverify_before_publication[].why` | NO — inside `if not publish:` | **CORRECT.** This is exactly where an authoring date belongs. |

Purging the string globally would have destroyed the audit trail that says *when this was checked
and against what*. Leaving it globally ships the authoring month to a paying candidate. **The same
sentence is right in one field and wrong in another, and only the render path distinguishes them.**

So the test is not "does this string appear?" but **"does this string reach a candidate?"** —
which means reading `build_paper.py` to establish which fields sit inside the `if not publish:`
guard before deciding anything. This is the same shape as lesson 9, which kept provenance fields
out of a contamination sweep, and it generalises: **a sweep over a spec must be field-class-aware
or it will produce confident answers to the wrong question.**

```
EVIDENCE:  QP2404 session, 2026-08-11, commit 9916744. "as at August 2026" found in
           QP2601-Q9 study_notes (candidate-facing, corrected), QP2601-Q9 unresolved[1] and
           QP2601-Q7 reverify_before_publication[0].why (review-only, deliberately kept).
           Two further candidate-facing instances on QP2601-Q1 and QP2602-Q2 reported for a
           Founder decision rather than fixed, being outside the authorised scope.
CATEGORY:  TEMPORAL_VERIFICATION
STATUS:    PROVEN
SEEN:      1
OWNER:     NONE. temporal_sweep.py reports the token; it does not classify the field by render
           path, and the adjudication is Claude's under lesson 8.
REVISIT:   if authoring-date leakage is found a second time on a shipped page, give
           temporal_sweep.py a candidate-facing / review-only column derived from build_paper.py
           so the classification stops being manual.
```

---

### 14. A post-sitting date inside an EXCLUSION statement is the guard, not the contamination

Every one of the four `temporal_sweep.py` candidates on the finished QP2404 was a post-sitting
date, and **all four were kept**. Three of them read, in substance, *"X is dated 4 April 2025 and
is EXCLUDED"* and *"they were approved in December 2024 and issued in February 2025 — AFTER this
sitting"*.

These are the sentences that **prevent** the wrong-edition error. They name the later instrument
precisely so the candidate can recognise it and rule it out. Deleting them to reach a clean sweep
would have removed the warning while leaving the trap, and produced a paper that scores better on
the detector and worse for the reader.

The distinction is not the date. It is **what the sentence does with the date**:

- **asserts** it as applicable at the sitting → contamination, remove;
- **excludes** it, or marks it as later context → the guard, keep;
- **states it as sitting-known future work** ("targeted for 2027", agreed at a meeting two months
  before the paper) → legitimate, keep.

The fourth flag, `2027` on Q7, is the third kind: HTW 10 sat 5–9 February 2024 and set that target,
so it was knowable at the sitting.

This is the practical edge of lesson 8. `PIL FLAGS; CLAUDE ADJUDICATES` is easy to agree with and
easy to abandon under pressure to show a zero. **A sweep result of "4 candidates, 4 legitimate" is
a better outcome than "0 candidates", and the report should say so rather than quietly engineering
the count down.**

```
EVIDENCE:  QP2404 session, 2026-08-11. temporal_sweep.py returned 4 candidates on the completed
           paper: '4 April 2025' (Q1, MSC-FAL.1/Circ.3/Rev.3 named in order to exclude it),
           'December 2024' and 'February 2025' (Q2 quick_revision.major_trap, naming MSC 109 and
           MSC.1/Circ.1687 in order to exclude them), '2027' (Q7, STCW review target agreed at
           HTW 10 two months before the sitting). All four adjudicated KEEP.
CATEGORY:  TEMPORAL_VERIFICATION
STATUS:    PROVEN
SEEN:      2 - the same adjudication class was reached prospectively on the donor set in §33,
           where 5 of 13 findings were legitimate sitting-known 2027 references.
OWNER:     NONE - operator adjudication under lesson 8.
REVISIT:   if exclusion-sentence flags become a large share of every sweep, consider a spec-level
           convention marking a field as deliberately-excluding so the sweep can report them
           separately - but NOT suppress them, or the guard becomes unauditable.
```

---

### 11. A broken non-blocking hook trains the operator to ignore errors

`validate_antipatterns.py` was carried in `CURRENT_STATUS.md` as an open defect across several
sessions — "errors on every file write, blocks nothing". This session verified it does not exist:
**no `hooks` key in any settings file**, and **no such file anywhere on disk**. It was transient
environment noise, and `SESSION_HISTORY.md` §2901 had already said so. The state document and the
history document had been contradicting each other, and the state document lost.

Two things worth keeping. First: a hook that errors without blocking is worse than no hook, because
it teaches the operator that a red line in the transcript is normal — either repair it so it can
actually fail, or remove it. Second, and the one that cost the sessions: **a defect that has been
disproved must be struck from the state document, not merely discussed in the history.** Otherwise
every future session re-investigates it. The evidence belongs in history; the *entry* belongs
deleted.

```
EVIDENCE:  pre-QP2404 hardening session, 2026-08-11. CURRENT_STATUS.md item 10 vs
           SESSION_HISTORY.md §2901; filesystem and settings sweep found neither hook nor config.
CATEGORY:  STATE_HANDOVER
STATUS:    PROVEN → PROMOTED_TO_POLICY
SEEN:      1
OWNER:     QA_AND_HANDOVER_PROTOCOL.md — state carries what is TRUE NOW, history carries why
REVISIT:   if a hook is ever adopted deliberately, it must positive-control like every other
           governed checker; a hook that can only exit 0 is not a guard.
```

---

# PART 2 — REJECTED AND DEFERRED

Recorded so they are not re-litigated for free, and reopened when their premise changes.

---

### R1. Parallelising heavy build / PDF / browser work — REJECTED on this machine

Logically independent work is not free to run concurrently. Python, Node, browser and
PDF-render jobs contend for the same cores and the same disk queue, so the parallel run
finishes later than the sequential one.

```
EVIDENCE:  EXECUTION_EFFICIENCY_POLICY.md, "Resource-aware execution — binding on this machine".
CATEGORY:  REJECTED
STATUS:    REJECTED
SEEN:      1
OWNER:     EXECUTION_EFFICIENCY_POLICY.md
REVISIT:   on a material change to CORE COUNT or DISK. Note that the 2026-08-11 RAM upgrade did
           NOT reopen this: the constraint is cores and the single disk queue, not memory.
           Cheap read-only work may still be batched.
```

---

### R2. Duplicating machine RAM / concurrency numbers into repository policy — REJECTED

A machine number written into product policy is a second copy of a truth that lives elsewhere,
and it goes stale silently. `EXECUTION_EFFICIENCY_POLICY.md` previously restated a 7.87 GB
figure that became false the moment the laptop was upgraded.

Machine facts live in `CLAUDE_MACHINE_OPERATING_POLICY.md`, outside this repository.

```
EVIDENCE:  the stale 7.87 GB figure, removed from EXECUTION_EFFICIENCY_POLICY.md.
CATEGORY:  REJECTED
STATUS:    REJECTED
SEEN:      1
OWNER:     PRODUCTION_PROTOCOL_INDEX.md §4
REVISIT:   only if the product ever ships on managed infrastructure whose specification is
           genuinely part of the product.
```

---

### R3. Re-litigating the model-answer word-count warning — DEFERRED

The band is `450–650 words` for 16 marks. **91 of the 99 solved model answers fall outside it**
(measured 2026-08-11). A warning that fires on 92% of the corpus carries no information: it is
neither enforced nor believed, and it trains readers to skip warnings generally.

The answer is not to raise the ceiling until it stops complaining. The band was derived for a
single undivided 16-mark answer and is being applied to answers printed as `10+6`, `6+5+5` and
`4+4+4+4`. **Re-derive it per printed limb**, then re-measure.

```
EVIDENCE:  validate_spec.py:53 — {10: (240,340), 16: (450,650)}; 91/99 outside band.
CATEGORY:  BUILD_QA
STATUS:    CANDIDATE / DEFERRED
SEEN:      1 (corpus-wide measurement)
OWNER:     NONE yet — validate_spec.py owns the current band
REVISIT:   when the band is re-derived per printed limb. Until then do NOT adjust the numbers
           and do NOT silence the warning.
```

---

### R4. Symmetrising host-recurrence donor edges — SUPERSEDED by lesson 10

Deferred on the reasoning that symmetrising edges changes **donor rankings and recurrence
semantics**, and that doing it safely needs an oracle for whether two questions are genuinely the
same — a semantic judgement no deterministic tool may make.

**That reasoning was correct and is retained.** What was wrong was the premise underneath it: the
donor derivation was never directional, so there were no edges to symmetrise. The directionality
was in the host annotation, one layer up. Inverting an annotation into a queue for a human needs
no equivalence oracle, because the tool moves visibility and the author still makes every
judgement — so the blocker that justified the deferral never applied to the fix that was needed.

Full reasoning in lesson 10. **Do not reopen this as an edge-symmetrisation task.**

```
EVIDENCE:  superseded 2026-08-11 in the pre-QP2404 hardening session. build_families proved
           already undirected; recurrence_model.reverse_hint_candidates ships the real fix.
CATEGORY:  DONOR_ADAPTATION
STATUS:    SUPERSEDED
SEEN:      1
OWNER:     lesson 10
REVISIT:   only if someone proposes promoting a host hint to a family edge — the answer is no.
```

---

### R5. Weakening a known trap after one correct hit — REJECTED

QP2601 Q4 tripped the Bunkers "strict liability on the registered owner" trap with a sentence
about the Nairobi Wreck Removal Convention that was **correct**. The trap was left at full
strength and the QP2601 wording was changed instead, so no protection was given up.

One correct hit is not evidence a trap is too broad. It is evidence the trap is live.

```
EVIDENCE:  known_traps.md trap 1, "Scope warning — added during QP2601 production, 2026-08-08".
CATEGORY:  REJECTED
STATUS:    REJECTED
SEEN:      1
OWNER:     known_traps.md
REVISIT:   on a SECOND independent correct-statement hit — at which point the phrase moves to
           GREP: SKIP and the narrower qualified form stays auto-scanned.
```

---

### R6. Limb-level semantic reuse — DEFERRED, not implemented

QP2509 Q8 demonstrated that reuse can be supported at the level of an individual limb rather
than a whole question. The opportunity is recorded; nothing is built.

PIL may one day surface **exact string similarities** for Claude to review, which is mechanical.
Decomposing a question into limbs and judging semantic equivalence is not, and is outside PIL's
authority.

```
EVIDENCE:  QP2509 Q8 limb-level donor support, 2026-08-11.
CATEGORY:  DONOR_ADAPTATION
STATUS:    CANDIDATE / DEFERRED
SEEN:      1
OWNER:     NONE
REVISIT:   when a second paper shows limb-level support, and only as exact-string surfacing for
           human review — never as automated equivalence.
```

---

### R7. Resolution-session date inference in the temporal sweep — REJECTED for V1

Turning `A.1207(34)` into "adopted 3 December 2025" requires knowing when the 34th Assembly
sat. That is source knowledge, and encoding it would make a detection tool assert regulatory
facts.

In practice the surrounding prose carries the date token anyway — which is exactly how the
QP2509 A.1207(34) defect reads, and the retrospective test confirms the date sweep catches it
without any resolution table.

```
EVIDENCE:  temporal_sweep.py --retrospective surfaces the A.1207(34) case via its
           "3 December 2025" token alone, from real donor bytes (QP2606 Q8).
CATEGORY:  REJECTED
STATUS:    REJECTED
SEEN:      1
OWNER:     temporal_sweep.py (documented in the module docstring, sweep B)
REVISIT:   only if a resolution is ever found cited with NO date anywhere in its field — at
           which point the mapping belongs in known_traps.md as a verified fact, not in a tool.
```
