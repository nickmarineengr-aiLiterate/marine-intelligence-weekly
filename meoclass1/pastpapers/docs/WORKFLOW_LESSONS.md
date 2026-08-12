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

**Corollary, learned the hard way on the follow-up: searching for the string you happened to
find is not the same as searching for the defect.** The first pass grepped `"August 2026"` — the
literal text of the instance in hand — and reported two candidate-facing leaks. A proper scan,
testing `as at <month> <year>` as a pattern, found **six across five papers**, two of which said
**February 2026** and were invisible to the original search. It also corrected a mis-identified
question id that came from reading a line number rather than a parsed object. Derive the pattern
from the defect class; never from the one example you are looking at.

```
EVIDENCE:  QP2404 session, 2026-08-11, commits 9916744 and caf5020. "as at <month> 2026" found in
           QP2601-Q9 study_notes (candidate-facing, corrected), QP2601-Q9 unresolved[1] and
           QP2601-Q7 reverify_before_publication[0].why (review-only, deliberately kept).
           The Founder-authorised follow-up scan then found SIX candidate-facing instances, not
           two - QP2506-Q5, QP2508-Q1, QP2601-Q1, QP2602-Q4, QP2602-Q8, QP2607-Q7 - five fixed and
           QP2602-Q8 kept as a labelled quarantined warning under lesson 14. Verified against
           shipped bytes by stripping prod-meta and review-banner blocks from the built pages,
           which also confirmed the field-class model empirically: exactly one hit survived.
CATEGORY:  TEMPORAL_VERIFICATION
STATUS:    PROVEN
SEEN:      2
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

### 15. A three-way comparison PROVES a port is safe; reading the diffs only guesses

Before porting anything off a long-unmerged branch, compare every overlapping file three
ways: fork point, the branch, and current.

In the Solved QP recovery all six overlapping files -- the four money paths, `SQ/pay.html`,
`SQ/index.html` -- hashed **identical between the fork point and current**. This lineage had
never touched them after the branch was cut, so there was no later fix to preserve and
taking the branch version was a port, not a regression.

That is a *proof*, produced by six `git rev-parse` calls. No amount of reading the diffs
establishes it, because reading tells you what the branch changed and never tells you what
current changed underneath it. Run the comparison first; it also decides how much care the
rest of the port needs.

```
EVIDENCE:  commerce/solvedqp-recovery, 2026-08-11. fork 217fbba == HEAD for all six
           overlapping files; the four delivery-tooling files diverged on BOTH sides and
           needed a genuine hand-port.
CATEGORY:  BUILD_QA
STATUS:    PROVEN
SEEN:      1
OWNER:     NONE -- a session practice, not yet a tool
REVISIT:   if a port is ever attempted without it and lands clean anyway.
```

---

### 16. When two branches solve one problem differently, port the PLUMBING, not the POLICY

A long-lived branch and the trunk will often have fixed the same hazard in different ways.
Applying both is not belt-and-braces -- it can *undo* the better fix.

The commerce branch kept `recurrence_class` and the host's recurrence annotation away from
candidates by **gating them behind `publish`**. Current had since **deleted both**:
`search_tokens` drops them in every mode and the card renders `corpus_relations()` instead.
Porting the gating would have reintroduced exactly the fields current removed.

Test the two rules against each other rather than merging them. Here the delivery checker
settled it independently: current's labels ("Once in this set", "Repeated -- reworded") do
not match the forbidden-label list at all, so the stronger rule already satisfied the
weaker gate. Only the delivery plumbing was taken.

```
EVIDENCE:  commerce/solvedqp-recovery, 2026-08-11. build_paper.py --deliver ported;
           the commerce publish-gating of recurrence_class/prior_sittings/recurrence
           deliberately not.
CATEGORY:  BUILD_QA
STATUS:    PROVEN
SEEN:      1
OWNER:     tools/pastpapers/solvedqp_check.py -- the guard that adjudicates
REVISIT:   if a case appears where both rules are needed together.
```

---

### 17. A number written into prose is frozen at its authoring date and no test will notice

`SQ/index.html` advertised "Six complete solved sittings -- 54 questions". True when the
commerce branch was cut; the product is now twelve sittings and 108 questions. The month
list was 2026-only. Restoring the file verbatim would have under-described a **paid
product on a public page**.

Nothing catches this. Every test passed, the page rendered, the links worked. The delivery
checker guards `data-newest-sitting` because it is a *marker*, and markers can be checked;
the sentence beside it could not be, because it is prose.

The generated surfaces already derive their counts -- the product home computes twelve
sittings and 108 questions from the specs. The hand-written storefront is where frozen
claims survive. Treat every number in hand-written commercial copy as stale until re-derived,
and prefer a checked marker over a sentence wherever the fact is really derived.

```
EVIDENCE:  commerce/solvedqp-recovery, 2026-08-11. Corrected 6->12 sittings and
           54->108 questions from the canonical specs during the storefront port.
CATEGORY:  SURFACE_IMPACT
STATUS:    PROVEN
SEEN:      1
OWNER:     tools/pastpapers/solvedqp_check.py (markers only; prose remains unguarded)
REVISIT:   when storefront counts are generated rather than typed.
```

---

### 18. A relative link is a claim about where the page LIVES, and a projection moves it

`cross_links` are authored relative to the review location `/meoclass1/pastpapers/`, so
`../QB10_B.html` resolves correctly there. The delivery projection serves the same content
from `/solvedQP/`, where that link resolves to a non-existent root path.

The guard did not catch it: it matches absolute `href="/meoclass1/..."`, and these links
never say `meoclass1`. They would have shipped as silent dead ends inside a paid page --
no error, no console warning, nothing to see unless clicked.

Whenever the same content is projected to a second base path, relative links are the first
thing to re-examine, and a guard written for absolute paths does not cover them.

```
EVIDENCE:  commerce/solvedqp-recovery, 2026-08-11. Delivery now keeps only sibling
           QP links whose target is actually delivered.
CATEGORY:  BUILD_QA
STATUS:    PROVEN
SEEN:      1
OWNER:     tools/pastpapers/build_paper.py (deliver-mode cross-link filter)
REVISIT:   if cross_links ever become absolute in the specs, which would retire this.
```

---

### 19. Fix a defect that breaks nothing, then GUARD it -- that is the class that returns

Delivery navigation carried one hard-coded link to `questions-2026.html`. Correct while
2026 was the only solved year. Once 2024 and 2025 were solved, a reader of a 2024 paper was
offered the 2026 sheet and had no route to their own.

Nothing failed. The link resolved, the page existed, every check passed. A defect with no
failure signal has nothing to stop it being reintroduced by the next person who needs "a
link to the questions page" -- so the fix was paired with a guard, and the guard proved by
mutation: a synthetic 2024 page offering only the 2026 sheet must be rejected, and is.

The general rule: when a defect is found by reading rather than by failing, the guard is
the deliverable, not the fix.

```
EVIDENCE:  commerce/solvedqp-recovery, 2026-08-11. delivery_links(year=...) plus
           check_year_nav() and its mutation control in solvedqp_check.py --self-test.
CATEGORY:  BUILD_QA
STATUS:    PROVEN
SEEN:      1
OWNER:     tools/pastpapers/solvedqp_check.py
REVISIT:   never -- guarding a silent defect has no downside worth reopening.
```

### 20. Read the ARTIFACT, not the document that describes the artifact

Three governing documents -- the consumer handover, the Founder rights decision `FD-RIGHTS-1`
and the founder aim -- agreed that the FSS corpus was cleared and text-bearing, and that the
required non-official-status statement was "already built into the LSA and FSS consolidations".
Every one of them was written in good faith by a session that had the corpus in front of it.

The file disagreed. The FSS derivative's own embedded disclaimer -- identical in BUILD-1 and
BUILD-2, so not a stray string -- declares its wording a "verified summary, NOT the official
text", INTERNAL USE ONLY, "never for redistribution". The measurements agreed with the file:
35 of 421 provisions carry no text, and 22 of the 386 that do are labels such as "Section" and
"sea inlet to pump". The sibling corpus is the control -- LSA carries 292 of 292 with
per-provision `textSource: official-base-ocr(...) page-verified` and a 65-character minimum.

A consumer that had trusted the contract would have shipped MIW summaries to candidates as
regulation text. The cost of checking was one file read; the cost of not checking was a
correctness failure on the exact surface the whole corpus exists to serve.

The general rule: a contract states an INTENTION about an artifact. Before building on a
property the contract asserts -- text exists, text is verbatim, a field is populated, a
statement is embedded -- open the artifact and confirm it. Where they disagree, the artifact
wins and the disagreement is REPORTED, never silently absorbed.

```
EVIDENCE:  workflow/corpus-consumer-integration, 2026-08-11. TSCR-1 in
           TRUE_SOURCE_CORRECTION_REQUESTS.md; TEXT_NATURE and its guard test in
           tools/corpus/consumer_adapter.py and consumer_adapter_test.py.
CATEGORY:  SOURCE_HANDLING
STATUS:    PROVEN
SEEN:      1
OWNER:     tools/corpus/consumer_adapter.py -- the guard test asserts the FSS disclaimer still
           says "NOT the official text", so a wording-bearing rebuild reopens the question
           instead of leaving a stale block in place.
REVISIT:   never -- but note the guard is the durable part, not the classification.
```

---

### 21. A validator pattern encodes the example it was written against

`REF_ID_RE` admitted `^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+$` -- hyphen-separated segments only. It was
written when `MARPOL-VI-14-146` was the sole worked example, and it was correct for it. It
therefore silently rejected `LSA-1.1.1`: the identity of the one corpus that is frozen,
text-bearing AND quotation-cleared, and the only one on which the flagship feature could have been
built.

Nothing failed, because no spec had ever carried an LSA reference. The pattern would have failed
the first person to write one, at the moment they were least able to tell an accidental assumption
from a deliberate rule -- the comment above it described the convention, not the constraint.

The general rule: when a validator is written against one worked example, record which parts of
the pattern are RULE and which are ARTEFACT OF THE EXAMPLE. Re-derive it the first time a second
real instance arrives, and prove the widening with negative controls -- `LSA-1..1`, `LSA-`,
`-LSA-1` must all still be rejected -- so "more permissive" does not quietly become "unvalidated".

```
EVIDENCE:  workflow/corpus-consumer-integration, 2026-08-11. REF_ID_RE in
           tools/pastpapers/validate_spec.py, widened to admit dotted segments with eight
           positive and eight negative controls.
CATEGORY:  BUILD_QA
STATUS:    PROVEN
SEEN:      1
OWNER:     tools/pastpapers/validate_spec.py
REVISIT:   if a third corpus arrives with an identity shape neither dotted nor hyphenated.
```

---

## NOT recorded this session -- "corpus availability is not sitting applicability"

Deliberately **not** promoted to a lesson, although it was the outcome most expected in advance.

The pilot was the natural place to prove it: `QP2508-Q3` sits in August 2025 and cites
MSC.555(108), whose entry into force is 1 January 2026. The trap was fully loaded. It did not
fire -- the answer already recorded the amendments as adopted but not yet in force at that
sitting, and the corpus **confirmed** the very date the answer had taken from a class-society
notice. No QP correction was required by any of the three pilot questions.

A lesson recorded from an event that did not happen is indistinguishable from a lesson recorded
from one that did, and this file is read as evidence. The principle is already stated as policy in
`CORPUS_SYNC_AND_CONSUMPTION_PLAN.md` section 5, which is the correct home for a rule that has been
reasoned but not yet paid for.

```
EVIDENCE:  workflow/corpus-consumer-integration, 2026-08-11. Pilot questions QP2508-Q3,
           QP2602-Q3, QP2607-Q4 -- corpus AGREED with all three.
CATEGORY:  TEMPORAL_VERIFICATION
STATUS:    CANDIDATE
SEEN:      0
OWNER:     CORPUS_SYNC_AND_CONSUMPTION_PLAN.md section 5 (as policy, not as a proven lesson)
REVISIT:   promote the first time a corpus lookup actually contradicts a verified answer's
           sitting-relative handling.
```

---

## An Assembly boundary is fixed by the ADOPTION date, not by the session's opening month

The QP2509 incident produced the working rule *"the 34th Assembly is December 2025, so it
postdates any earlier sitting"*. That rule gives the right answer for the wrong reason, and the
reason matters as soon as a November sitting is worked.

**The 34th Assembly sat 24 November to 3 December 2025.** It *convened inside November* — the
sitting month of `QP2511` — and adopted its resolutions at the **close** of the session.
`A.1207(34)` is dated **3 December 2025**. A session that reasons from "which month did the
Assembly meet in" reaches an ambiguous answer for a November paper; a session that reasons from
the adoption date reaches a clean one.

The same shape recurs: the 33rd Assembly's `A.1187(33)` is dated **6 December 2023**, which is
why the 33rd Assembly editions are the operative ones for any sitting up to that date.

**The practical consequence is a whole family of instruments, not one resolution.** Assembly
sessions re-issue the HSSC Survey Guidelines, the Procedures for Port State Control and the III
Code obligations list on a biennial cycle. A donor from a later sitting may legitimately cite the
newer edition of any of them, and that citation is a future instrument for the earlier target.
On `QP2511` this lands on Q5, whose March 2026 donor may cite the 2025 HSSC guidelines where the
sitting requires the 2023 ones — a defect no downstream check would catch, because the donor was
correct for the donor.

```
EVIDENCE:  QP2511 session, 2026-08-11. Assembly 34 dates verified against IMO's own meeting
           summary; A.1187(33) of 6 December 2023 already primary-verified in QP2403-Q7.
           Recorded in docs/QP2511_TEMPORAL_AND_DONOR_ANCHOR.md section 2.
CATEGORY:  TEMPORAL_VERIFICATION
STATUS:    PROVEN
SEEN:      2   (QP2509 realised defect; QP2511 prospective catch)
OWNER:     NONE -- adjudication, not detection. temporal_sweep.py flags a post-sitting date but
           cannot know that a re-issued Assembly instrument has an earlier operative edition.
REVISIT:   if an Assembly ever adopts at the opening of a session rather than at its close, or
           if a per-paper Assembly-edition table is built that a tool could check against.
```

---

## When the adoption date is ambiguous, the resolution's ISSUE date settles it

The Assembly-boundary lesson above resolves a sitting by **adoption** date. That works for every
month except the one the adoption falls in. `QP2512` is that month: the 34th Assembly adopted on
**3 December 2025** and the source copy prints `DECEMBER 2025` with **no day**, so a December
sitting can fall on either side of the boundary and the governed fallback — exclude when the date
cannot be established — leaves the question merely *defaulted* rather than answered.

**A second date closes it.** An IMO resolution carries a **document date** as well as an adoption
date, and the document date is later. `A 34/Res.1206` reads *"adopted on 3 December 2025"* on a
cover dated **5 December 2025**. The Organization had not circulated the text until then, so no
sitting anywhere in the month could be examined against it. The exclusion becomes **reasoned rather
than defaulted**, and it does not depend on pinning the examination to a day.

**How to apply.** When a sitting month contains the adoption date, read the resolution's cover for
its document date before falling back on "cannot establish, therefore exclude". The fallback reaches
the same answer; the document date tells you *why*, which is what a verification record has to
carry. The gap is small — two days here — but it is the difference between a defensible finding and
an admitted unknown.

```
EVIDENCE:  QP2512 session, 2026-08-12. A 34/Res.1206 obtained from the IMO resolutions CDN and its
           cover read directly: "A 34/Res.1206, 5 December 2025 ... adopted on 3 December 2025".
           Recorded in docs/QP2512_TEMPORAL_AND_DONOR_ANCHOR.md section 2.
CATEGORY:  TEMPORAL_VERIFICATION
STATUS:    PROVEN
SEEN:      1
OWNER:     NONE -- adjudication, not detection. R7 rejected teaching the sweep resolution dates and
           that rejection stands; this is a reading instruction for the author, not a table.
REVISIT:   if a sitting is ever found whose month contains BOTH the adoption and the document date,
           at which point neither settles it and the examination date must be established directly.
```

---

## A re-issued instrument may have an edition you have never seen between the two you know

The Assembly-boundary lesson predicts that a later donor cites a newer edition of a re-issued
instrument. It leaves implicit a two-edition mental model — *the donor's* and *the one before it* —
and that model is wrong often enough to matter.

The Procedures for Port State Control have **three** editions in play across this corpus:

```
A.1155(32)   Procedures for PSC, 2021    adopted 15 December 2021
A.1185(33)   Procedures for PSC, 2023    adopted  6 December 2023   revokes A.1155(32)
A.1206(34)   Procedures for PSC, 2025    adopted  3 December 2025   revokes A.1185(33)
```

A session re-anchoring `QP2606-Q2` (June 2026, built entirely on `A.1206(34)`) back onto a December
2025 sitting has to land on `A.1185(33)`. The intuitive move — *"before the 2025 Procedures came the
2021 Procedures"* — **skips an entire edition and reaches an instrument that had been revoked for
two years.** Nothing downstream catches it: the citation is real, the resolution exists, the content
is close, and the answer reads correctly.

**How to apply.** Never infer the predecessor edition. Open the donor's own resolution and read
operative paragraph 4 — an IMO resolution that supersedes another **names what it revokes**, and its
preamble recites the chain before that. Two reads give the whole lineage from the document you
already have. Note also that **section numbering does not carry across editions**: `QP2606-Q2` cites
`A.1206(34)` §2.3.11 for the right of appeal, and the equivalent in `A.1185(33)` must be located,
not assumed.

```
EVIDENCE:  QP2512 session, 2026-08-12. A 34-Res.1206 and A 33-Res.1185 both obtained from the IMO
           resolutions CDN and their operative paragraph 4 and preambles read directly.
           Recorded in docs/QP2512_TEMPORAL_AND_DONOR_ANCHOR.md section 2.1.
CATEGORY:  TEMPORAL_VERIFICATION
STATUS:    PROVEN
SEEN:      1   (prospective catch on QP2512-Q8; no defect shipped)
OWNER:     NONE -- adjudication. No tool holds a resolution lineage table and R7 declined to give
           one to the sweep.
REVISIT:   if a per-instrument edition ledger is ever built, this becomes a lookup rather than a
           reading instruction. The HSSC Survey Guidelines and the III Code obligations list are on
           the same biennial cycle and will have the same three-edition shape.
```

---

## The contaminated donor was the FORWARD one, not the backward ones

`QP2511` is a backwards-pull paper: five of its six donors are 2026 answers dragged back to a
November 2025 sitting, and the whole session was set up to reverse *their* currency corrections.

The internal `Q`-reference defect — the QP2509 defect class, where a donor's "see Q8" silently
re-points at an unrelated question on the new paper — was found in **`QP2508-Q7`, the one donor
pushed forward** from an earlier sitting. It carries *"see Q8"*, *"Q8 of this paper"* and
*"Q5 of this paper"*; on `QP2511` those numbers mean the Hong Kong Convention and the Enhanced
Survey Programme.

The lesson is that **direction of pull predicts *which* contamination class to expect, and a
session that has correctly identified itself as a backwards-pull paper is primed to look the
wrong way.** Post-sitting dates travel backwards; internal cross-references travel in **both**
directions, because they are relative to the donor's own paper and not to any date at all.

Sweep every donor for internal `Q`-references regardless of direction. The date sweep may be
directional; the reference sweep never is.

```
EVIDENCE:  QP2511 session, 2026-08-11. Donor scan against the target sitting found the
           POST_SITTING_DATE flags concentrated in the 2026 donors as expected, and the
           INTERNAL_QREF flags concentrated in QP2508-Q7. Recorded in verification/QP2511/Q9.md.
CATEGORY:  DONOR_ADAPTATION
STATUS:    PROVEN
SEEN:      1
OWNER:     tools/pastpapers/temporal_sweep.py detects INTERNAL_QREF_CANDIDATE, but only on
           solved specs against their own sitting -- it cannot sweep a donor against a target.
REVISIT:   if temporal_sweep.py gains a --target-sitting mode, this becomes tool-enforced and
           the entry should be reclassified PROMOTED_TO_TOOL.
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

---

## A right conclusion reached through a PREMATURE premise

**Status: PROVEN.** Evidence: `QP2511-Q8`, 2026-08-11.

The known backwards-donor failure is a *wrong answer* inherited from a later sitting. This is the
harder variant: the donor's **conclusion is correct at both sittings** and only its **reasoning** is
impossible at the earlier one.

`QP2603-Q9` (March 2026) says India's ship recycling law survives *"because s.324(1) of the Merchant
Shipping Act, 2025 repeals only the 1958 Act and the Coasting Vessels Act 1838"*. At November 2025 the
2025 Act had **assent but not commencement**. The conclusion — the Recycling of Ships Act, 2019
governs — is right at both sittings, because that Act is separate legislation either way. The premise
is not: it asserts the effect of a repeal provision that had not yet taken effect.

**Why nothing catches it.** The sentence is internally coherent, names the right statute, and reaches
the right answer. A date sweep flags `15 March 2026` — but a reviewer who checks *"is the conclusion
correct?"* answers yes and moves on. Only asking **"could this REASON have been given at this
sitting?"** exposes it.

**How to apply.** On any backwards donor, check the *premise* separately from the *conclusion*. Where
a donor explains **why** something is so by reference to an instrument, confirm that instrument was
operative at the target sitting — even when the conclusion is unarguable. A correct answer supported
by a premature reason is still a defect, and it is the one most likely to survive review.

---

## Investigating a predicted regression and finding NOTHING is a completed piece of work

**Status: PROVEN.** Evidence: `QP2511-Q5` and `QP2511-Q3`, 2026-08-11.

`QP2511_TEMPORAL_AND_DONOR_ANCHOR.md` named three questions where a backwards donor would bite. **One
was real. Two were not** — the Q5 donor cites no HSSC guidelines and no `A.12xx(34)` resolution at
all, and the Q3 donor contains **zero** occurrences of "Merchant Shipping" in any field.

Both negatives are recorded in `reuse_evidence` and `temporal_review` as findings, not omitted.

**Why it matters.** An anchor prediction is a **question, not a verdict** — the same principle as
`PIL FLAGS; CLAUDE ADJUDICATES`, applied to the paper's own forecast. Treating the prediction as
established invites the opposite error to the one feared: **deleting a correct citation that was never
there**, or "restoring" an earlier edition into an answer that never cited one.

**How to apply.** Sweep for the predicted token family explicitly, and write the result **either way**.
A recorded negative is reusable — the Q5 result establishes that the ESP family does not touch
Assembly-level survey instruments at all, so the 33rd/34th Assembly boundary can be cleared cheaply for
any future member rather than re-investigated.

---

## A token sweep prompts a look; it never delivers a verdict — the false-positive case

**Status: PROVEN.** Evidence: `QP2511-Q6`, 2026-08-11.

The Q6 donor sweep returned **fourteen hits and all fourteen were false positives**. Eleven were the
word `current` inside the technical terms **`eddy current`** and **`impressed current`**. One was the
host recurrence annotation, one an authoring date, and one the word `now` inside a hypothetical
(*"the blade geometry may now be outside tolerance"* — narrative sequence after grinding, not a claim
about the sitting date).

**The cost of getting this wrong is concrete.** Treating the flags as findings would have stripped the
answer's NDT method selection and its cathodic-protection failure mechanism — both correct, both
central to the question.

**How to apply.** `eddy current` and `impressed current` are permanent false positives for any
`current` rule; expect them on machinery questions rather than re-adjudicating from scratch. More
generally, record the false-positive adjudication on the object, so the next session does not repeat
the analysis or, worse, reach a different conclusion.

---

## The staged-object assembler should assert against INTAKE, not against the donor

**Status: PROVEN for the guard; CANDIDATE for promotion to `tools/`.**
Evidence: `QP2511-Q9`, 2026-08-11.

A paper stopped part-finished is staged outside the canonical spec. On resumption, assembly asserted —
for all nine questions, **before writing anything** — identity, printed stem **against the intake
spec**, marks, `printed_marks_absent`, answer state, verification-file existence, `temporal_review`
sitting and state, and retrieval-card id prefixes.

**It blocked, on a real defect.** The Q9 object staged by the previous session carried the **donor's**
`host_recurrence_hint` (seven entries, copied wholesale from `QP2508-Q7`) and had lost this paper's own
`2025/NOV/Q9`. The field is authoring-only and never rendered, so nothing candidate-facing was
affected — but the donor's annotation would have entered the recurrence intelligence as though it were
this paper's.

**The rule.** *Printed truth comes from the intake spec and is re-asserted LAST*, after both donor
inheritance and authored patches. Anything a donor supplies for a printed-truth field is presumptively
wrong, because the donor's printed truth is a different paper's.

**What would reopen promotion to `tools/`.** One observed staged-paper workflow is not enough to
justify a new governed tool. If a paper is stopped part-finished again, promote the assertion set —
**not** the paper-specific payload — to `tools/pastpapers/`.

---

## A compressed stem is a CHANGED TASK, not a shorter one

**Status: PROVEN.** Evidence: `QP2511-Q3` against `QP2601-Q6`, 2026-08-11.

The November 2025 stem folds the January 2026 stem's two separate demands into one, and in doing so
**deletes a qualifier**: *"certificates issued to a vessel **for maintenance of the ship in good
health**"* becomes *"the different certificates **in India**"*.

That qualifier was doing real work. The donor's own `decomposition_gate` records the ambiguity —
whether crew medical certificates are in scope — and resolves it **as ship-only precisely because of
the qualifier the target does not print**. Meanwhile the target's first sentence names *"the ship
**and the crew**"*. The compressed stem is therefore **wider**, not narrower, and a sixth route step
was authored to answer it.

**How to apply.** When a NEAR donor differs by compression, diff the stems **word by word** and ask
what each removed word was doing. Read the donor's own recorded ambiguities: where a donor says *"I
resolved this narrowly because the stem says X"*, and the target does **not** say X, that resolution
does not transfer. Then hedge structurally rather than in prose — answer the narrow reading first and
at greater length, so a marker taking it loses nothing.

---

## Deriving a teaching point from `host_recurrence_hint` leaks it to the candidate

**Status: PROVEN.** Evidence: `QP2511-Q8`, 2026-08-11, caught and removed before build.

A study-notes block drafted for Q8 taught the entry-into-force boundary by **naming the sittings at
which the question has appeared**. The enumeration was derived from `host_recurrence_hint` — an
authoring field — and `study_notes` **is rendered**.

This is the guarded provider-recurrence leak arriving by a new route: not through a field that leaks,
but through an author **reading** an authoring field and writing its content into prose.

**How to apply.** The teaching point almost never needs the sittings. The block was rewritten to say
*"check whether your notes predate 26 June 2025"* — identical pedagogy, no disclosure. Verify by
scanning candidate-facing fields for sitting patterns after drafting, not only before.

Confirmed by inspection of `build_paper.py` that `subpart_marks_note`, `recurrence_adjudication`,
`host_recurrence_hint`, `reuse_evidence` and `question_delta` are **not rendered at all** — recurrence
reasoning recorded in those fields is safe. `sources` and `unresolved` **are** rendered.

---

## SECURITY, DEPLOYMENT AND DATA-MIGRATION LESSONS — 2026-08-12

Added after the credential remediation and the first production cutover of Security V2. These are
the reusable ones; the narrative is in `history/SESSION_HISTORY.md`.

### A gate and the data it reads must be verified together

The single most expensive lesson of the session. `middleware.js` was correct, well tested and
enforced exactly the right rule. `miw:ent:*` was empty for all 100 accounts because the back-fill
had never been run. Deploying the correct gate over absent data locked out every paying customer.

**A correct gate over absent data fails exactly as hard as a broken gate, and it fails silently
until a real user arrives.** Before deploying any authorisation layer, count the records it will
read — not just the rules it will apply. The check is one SCAN and it would have taken a minute.

### A silent build step is a security control that never runs

`middleware.js` had imported `@vercel/edge` without declaring it since the day it was written. The
build script is `echo 'Build successful'`, so nothing resolved the import until the Edge bundler
tried — which had never happened, because the middleware had never deployed. The whole security
boundary silently did not ship, and the visible symptom was a *public content exposure*, which
looks nothing like a dependency error.

**If a build step cannot fail, it is not verifying anything.** Where a security control depends on
a build succeeding, prove the control is live by probing the deployed artefact, never by observing
that the push succeeded.

### Measure production; never carry a hypothesis forward as a fact

Two sessions carried "the affected count is 28" and "some accounts will have been hash-upgraded by
now". Both were wrong: 100 and zero. Neither had been measured, and both were plausible enough to
survive review.

**Any claim about production state that has not been measured this session is a hypothesis.** Write
the read-only audit tool first. It is usually an hour, it is reusable, and it is the only thing
that converts a briefing number into a fact.

### Order remediation so that the fix cannot re-arm the vulnerability

Setting `MIW_SESSION_SECRET` was the briefed fix for LAUNCH-BLOCK-2. Doing it first would have
restored the login path and made 100 leaked passwords usable again — the missing secret was, by
accident, the thing keeping them inert. The correct order was rotate, then remove the legacy
verifier, then set the secret, then deploy.

**Before fixing a broken-but-protective failure, ask what it is currently preventing.** A
misconfiguration that fails closed is a control until you fix it.

### Delete a compatibility path; do not disable it

The legacy plaintext verifier was removed outright rather than flagged off, and the `legacy` return
field was deleted so no caller could branch on the stored form. A second accepted representation of
a credential is precisely how the original exposure stayed live for as long as it did.

**Two accepted forms of a secret is one form too many.** Remove the branch, delete the flag it
returned, and invert the test that asserted the old behaviour — in place, with a comment saying it
was inverted and why.

### Put the retry where the irreversible step is

A rotation replaces the credential, then revokes sessions, then emails. The email is last because
it is the only unrecoverable step: by the time it runs, the old password is dead and the new one
exists nowhere else. A transient relay throttle at message 60 of 100 would have permanently locked
out 60 paying customers.

**Retry belongs inside the last call before the point of no return**, not around the whole
operation. And authenticate the relay once, before the first record is touched — a bad key found
at message 1 costs nothing.

### For an unauthenticated endpoint, uniform responses are not enough — the timing must be uniform too

The password-reset endpoint claims its throttle slot *before* checking whether the account exists.
The other order returns "no such account" without a Redis write, making it measurably faster than
"throttled", so the clock becomes the enumeration oracle that the identical response text was
written to close.

**A constant response string does not make an endpoint non-enumerable.** Make the work uniform, not
just the words. The same applies to client-side error handling: a distinguishable network-failure
message leaks what the server refused to.

### A finite resource in a payment path is an outage with a delay on it

`QB_PASSWORD_POOL` capped how many customers the product could ever take, and the throw happened
*after* Razorpay captured the payment and after the fulfilment lock was claimed: money taken, no
entitlement, no email, a webhook retrying the identical failure forever, and no alert.

**Audit payment paths for anything that can run out.** If the resource has no reason to be
pre-agreed — a credential does not — generate it instead of drawing it from a list.

### Concurrency between agents is a real hazard on customer-impacting work

Two sessions were committing to the same release branch. A merge reported "Already up to date"
because another session had performed it seconds earlier. Two concurrent `rotate --confirm` runs
would have rotated and emailed every customer twice, the first password dead on arrival.

**Before any irreversible customer-facing batch, confirm no other session is running it.** Design
the tool so a second run is a no-op — scoping rotation to unhashed records made a double run
structurally safe, which mattered more than the process check that was skipped.

### Secrets belong in a file, never in a conversation

A git-ignored file was prepared precisely so operator credentials would not enter the transcript.
They were pasted into the chat anyway, and had to be treated as exposed and scheduled for rotation
— a second incident opened while closing the first. A live enumeration probe was then run against
the Founder's real address, resetting their password unnecessarily.

**Use throwaway addresses for probes against live endpoints**, and when a secure channel has been
prepared, say plainly that using the insecure one creates new work rather than saving time.

---

## STOREFRONT, SAMPLE AND MEASUREMENT LESSONS — 2026-08-12 (second session)

### Publish state belongs to the artefact, never to the invocation

`--publish` was a command-line flag, so it lived only in the memory of whoever last typed the
command. `run_toolchain.py` rebuilds samples with no arguments, so every routine build silently
reverted a published page to a review copy — telling customers "not published, not indexable" with
a `PRICE_TBD` placeholder, on the page the whole funnel pointed at. Nothing failed and nothing
warned.

**If a property must survive the next rebuild by someone who does not know about it, it belongs in
the config, not in the command.** The test is simple and worth running: rebuild with no arguments
and see whether the artefact is still what you published.

### A public directory publishes whatever is put in it

The Edge gate was correct and enforcing. `SQ/QB1_A.html` still exposed ~95% of the paid Question
Bank, because `/SQ/` is deliberately outside the middleware matcher so login and the storefront
work without a session. No amount of boundary correctness catches a **placement** error.

**Audit the public directory by content, not by route.** For every file under a public prefix, ask
what fraction of a paid artefact it reproduces. The comparison is one script and it found this in
a minute.

### Counting a short string is a hypothesis, not a measurement

Three times in one session a naive count sent the work the wrong way:

- `grep 'Exam Plan'` returned 0 because the label is `Exam plan` — concluded, wrongly, that the
  sample did not demonstrate all five modes.
- 17 "lock" markers looked like a paywall. They were the substring `lock` inside `display:block`
  and `white-space:nowrap`. There was no lock.
- A leak check compared tag-stripped sentences against **raw HTML**, so any sentence containing
  `<strong>` could never match. It reported 2 false leaks and 6 false losses simultaneously.

**Compare like with like, and confirm what a count means before acting on it.** Text belongs
against text, markup against markup. A verification that can fail in both directions at once is
not a verification.

### State the cost from the tool, never from prose

The commercial cost of publishing the January paper in full was described as "February, March,
April and July". The build, asked properly, printed **18 questions across 11 sittings**, one paper
losing six of its nine. The Founder had already decided on the understated figure.

**When a decision has a measurable price, measure it before presenting the choice**, and make the
tool print it on every run so the number cannot drift back into prose. Where the decision was taken
on a wrong figure, say so plainly and give the one-line reversal.

### A guard exception must be honoured everywhere the guard lives

The recurrence guard existed twice: in `build_sample.py` and again in `sample_check.py`. Adding a
legitimate override to one left the other failing 21 times with no way to go green except deleting
something.

**Mirror the exception wherever the rule is mirrored, and make the exception prove itself** — here
the config claims a gate, and the checker verifies that claim against the output path rather than
believing it. A permanently red check trains people to ignore checks, which costs more than the
check ever saved.

### Verify the deployed artefact, and read it, not its status code

The review banner sat live on the public sample through an entire prior session that had verified
the page returned HTTP 200 and leaked no paid links — but never read what it said.

**A 200 is not a verification.** Fetch the live page and assert on its content: the words a customer
sees, the robots tag, the price, and the absence of internal paths.

---

## When an excluded instrument would spread across a whole object, AUTHOR FRESH rather than clone-and-patch

**Status: PROVEN.** Evidence: `QP2512-Q8`, 2026-08-12.

The three-edition lesson above says a re-issued instrument may have an edition you have never seen.
This is the *authoring* consequence of it, and it is a different rule.

`QP2606-Q2` was the natural support for `QP2512-Q8`'s port State control limbs. It is built
**entirely** on the 2025 Procedures for Port State Control, which had not been issued at a December
2025 sitting. The staging harness would happily have cloned it and taken a patch.

**It was not cloned, and the reason is arithmetic rather than caution.** The intake temporal note for
this question predicts an instrument asserted across **eight separate surfaces** of a single question
object — model answer, study guide, `recall_15s`, `major_trap`, a route core point, a retrieval card,
`regulations` and `search_aliases`. Cloning means finding and reversing the excluded edition on all
eight, and being right eight times. Authoring fresh means it **cannot enter at all**, and the donor's
value — its section structure and its sense of what the examiner wants — is not lost, because
structure can be read without copying text.

**The rule.** *Before cloning a donor, ask how many surfaces the contaminant occupies. Where an
instrument, statute or date is excluded at the target sitting and the donor is built on it, author
fresh and record the donor as structural support.* Clone-and-patch is for donors whose contamination
is **local**; it is the wrong tool when the contamination is **pervasive**, because it converts one
structural decision into eight independent chances to miss something.

**What would reopen this.** A donor whose excluded instrument genuinely occupies one or two fields.
Cloning is still cheaper there, and this lesson is not an argument for always authoring fresh.

---

## Solving a paper does not necessarily REPLENISH the derived tier-D pool

**Status: PROVEN.** Evidence: QP2511 versus QP2512, 2026-08-12.

`CURRENT_STATUS.md` recorded, after QP2511, that its derived tier-D total was *"unchanged in total:
its own six left the unsolved set when it was solved, and solving it unlocked six replacements."*
That is a real observation, and it quietly became an expectation.

**QP2512 did not behave that way.** It consumed three tier-D donors of its own and **unlocked none**:
the derived count over the unsolved set fell 20 → 17, by exactly the three it took. Six of its nine
questions were adjudicated as **fresh or limb-supported** rather than family-linked, and a question
with no family produces no edge for anyone else however well it is answered.

**The rule.** *Donor readiness is a property of the corpus's family structure, not a conserved
quantity that solving papers tops up.* A planning session must **recompute** the derived tier-D count
after each paper rather than assume the pool is self-sustaining — and a paper rich in fresh questions
is worth **more** to candidates and **less** to the next session's donor budget at the same time.
Those two facts are not in tension; they are simply different measures.

---

## A newly solved paper needs a UI fixture, and its regulation probe is a free temporal tripwire

**Status: PROVEN.** Evidence: `QP2512`, 2026-08-12.

`ui_behaviour_test.cjs` fails a page whose `paper_id` has no `FIXTURES` entry, deliberately, so a new
paper cannot report a clean run having tested nothing. That gate fired the first time QP2512 was
built, which is the gate working.

Two things were learned in satisfying it.

**Choose the terms by probing the built page, not by intuition.** Every candidate probe, alias,
narrowing phrase and leak token was run against the generated `data-search` attributes before being
written into the fixture. Three intuitive alias candidates turned out to be rendered on the card and
were therefore useless as *alias* probes; the true alias-only terms were found by diffing
`search_aliases` against the rendered text.

**Spend the `regulation` probe on the paper's sharpest temporal anchor.** The slot takes one
regulation term. For QP2512 it is `a.1185(33)` — the operative edition of the Procedures for Port
State Control at that sitting — rather than a SOLAS regulation that could never be wrong. The effect
is a **mechanical tripwire**: if a future edit re-anchors the paper onto a different edition, the
fixture fails on the wrong resolution number, in CI, without anyone having to remember the trap.

**The rule.** *A per-paper UI fixture is not boilerplate. Derive its terms from the built artefact,
and aim its single regulation slot at whatever the paper is most likely to be got wrong about later.*

---

## A GUARD THAT HAS NEVER SUBTRACTED THE ALLOWED SURFACE WILL CONVICT THE PRODUCT OF ITSELF

**Status: PROVEN.** Evidence: `build_solvedqp_manifest.py`, 2026-08-12.

A leak guard scanned the generated manifest for any 60-character run of model-answer prose. It
fired on the very first build, on `QP2403-Q4` — because that answer opens by restating its own
printed question, and the printed question is exactly what the manifest is *for*.

The bug was not the threshold. It was that the guard tested "does paid text appear here?" when the
question it had to answer was "does paid text appear here **beyond what we already publish**?"

**The rule.** *Before a guard can flag an overlap, it must be given the set it is allowed to
overlap with.* Build the allowed corpus from the artefact's own published fields and subtract it.
A guard without that subtraction does not measure leakage — it measures similarity, and a product
is always similar to itself.

---

## AN AUTOMATED SCAN MUST SEE WHAT THE READER SEES, NOT WHAT THE FILE CONTAINS

**Status: PROVEN.** Evidence: `solvedqp_health_check.py`, 2026-08-12.

The first run of the delivery health check reported eighteen errors: every page "contains a
review-copy marker". Every page carries `<!-- GATE SCRIPT STRIPPED FOR REVIEW COPY -->` — a build
comment, invisible to any customer.

Eighteen daily errors about something no reader can see is worse than no check, because it teaches
the reader to skip the report.

**The rule.** *Strip comments, scripts and styles before scanning for anything a human would
"see".* Keep the markup only where the leak itself is markup — a `localhost` href hides in an
attribute, not in prose. The scan surface is a decision per rule, not one global setting.

---

## A HISTORICAL DOCUMENT CANNOT BE CHECKED AGAINST CURRENT LAW — AND THE STUDY GUIDE IS THE PROOF

**Status: PROVEN.** Evidence: `solvedqp_health_check.py` temporal design, 2026-08-12.

Two separate versions of this mistake were made and caught in one session.

**First**, the obvious one: the Oral trap ledger greps for `A.1185(33)` and
`Merchant Shipping Act, 1958`, both wrong as current law. Both are *right* on the papers they
appear in — `A.1185(33)` is the operative PSC edition for a December 2025 sitting, and the 1958 Act
governs all twenty-two 2024 and 2025 sittings. Sharing that ledger would produce roughly a hundred
false findings every morning, for ever.

**Second**, and much less obvious: even a correctly-directional guard — "no instrument may be
asserted as operative before it existed" — raised seven errors on correct content. It was reading
whole pages, and **the Study Guide is required to tell the candidate the law has since changed**.
Forward-looking commentary is the product working, not failing.

The final false positive was `QP2602`'s answer reading *"in force 15 March 2026 — some five weeks
after this paper was sat"*, which is a model piece of temporal honesty and which a naive
`[^.]{0,80}(commenced|in force)` window happily flagged.

**The rule, in three parts.**
1. *Scope the guard to the region where the rule applies* — answer panes, not pages.
2. *Read the sentence, not the match.* An assertion and its negation share every keyword.
3. *Where the evidence cannot order two events — a December sitting and a 3 December adoption —
   emit REVIEW, never ERROR.* A checker that guesses is manufacturing a verdict, and a deterministic
   job in CI has no business doing that.

---

## A SELF-TEST FIXTURE PLACED OUTSIDE THE RULE'S SCOPE TESTS NOTHING

**Status: PROVEN.** Evidence: `solvedqp_health_check.py --self-test`, 2026-08-12.

The future-law fixture injected its defect immediately after `<body>`. It passed while the guard
scanned whole pages, and failed the moment the guard was correctly narrowed to answer panes — 12/13.

That failure was the self-test working. A fixture that survives a *tightening* of the rule it
exercises was never inside the rule to begin with.

**The rule.** *When you narrow a check's scope, re-place every fixture that exercises it.* And read
a self-test failure after a scope change as a question about the fixture before assuming it is a
question about the code.

---

## RECOMPUTE ALLOCATION UNDER THE STATE THAT WILL EXIST, NOT THE STATE THAT DOES

**Status: PROVEN.** Evidence: desktop Batch 2 selection, 2026-08-12.

Batch 2 had to be chosen while Batch 1 was still in flight. Ranking the candidates on *today's*
corpus would have been ranking them on a state that will never be the state they are worked in.

Simulating Batch 1 as complete moved real decisions: QP2502 rose 2/9 → 3/9, QP2504 rose 1/9 → 3/9
and then to 5/9 in sequence, and QP2507 — 0/9 today, and correctly rejected by Batch 1 for exactly
that reason — became **8/9**, because all eight of its family edges land inside two other papers in
the same batch.

It also *demoted* an inherited assumption. The previous board expected the mid-2024 trio to be the
natural next block; simulation showed all three finish at 1/9 with reach 0 whatever the order,
because their donors come from other years. There was no block to protect.

**The rule.** *Plan the next batch against the projected corpus, and record which projection you
used.* The derived tier already refuses to be read from a stored field because stored tiers plan
off the past; planning off the present has the same defect one step later.

---

## L-B1-1 — A referral names a question; treat it as naming a CLASS of claim

**Proven:** 2026-08-12, Desktop Batch 1 integration.

The desktop referred one defect: `QP2402-Q3` maps EEDI to MARPOL Annex VI regulation 21, which is
Functional requirements. Fixing the question named would have been a complete, defensible response
to the referral.

Instead the referral was turned into a scan of **every solved spec** for the same shape of claim —
"EEDI cited near regulation 21", "attained EEXI cited near regulation 25". That found the identical
defect in `QP2402-Q5`, the EEXI half in `QP2402-Q6`, and a live mislabel on `QP2601-Q1` that was
also on the public free sample. A parallel scan of the Hong Kong Convention source-state claim
found two more, both live.

**One referral, six defects, three of them already published.** Five would have survived a
question-scoped fix.

**Do:** when a referral arrives, write the detector before writing the fix, and run it over the
whole corpus. **Do not** assume the reporting session found every instance — it was looking at one
paper.

---

## L-B1-2 — Extract paper-owned paths; never merge a branch cut from an old baseline

**Proven:** 2026-08-12, six papers.

Branches built from `9c973596` predate the manifest, search, health checker and publish-state fix.
Merging one replays its stale global tree over newer work, and the damage is invisible because the
build still passes — it just passes against the wrong inputs.

**Do:** create an integration branch from current `origin/main`, then
`git checkout <desktop-branch> -- <the paper-owned paths only>`.

**Prove it is lossless first**, in one command, before the first extraction:

```
git diff <baseline> origin/main -- <the paper-owned paths>
```

Empty output means main never touched those paths, so extraction and merge would differ *only* in
the globals. Non-empty means the paper's own files have moved on main and a real reconciliation is
needed. Assuming the empty case is how a silent revert happens.

---

## L-B1-3 — Stage from what the build changed, not from a path list you typed

**Cost:** one follow-up commit, 2026-08-12 (`3a19f02`).

Solving a paper re-classifies recurrence on *other* papers — `QP2402-Q3` became "First in set. The
same task returns at November 2024 Q3" only when `QP2411-Q3` was solved. Those propagated files are
not predictable from the paper being integrated, so a hand-written `git add` list will miss them
and the miss is silent: the commit succeeds and the tree is left inconsistent with `main`.

**Do:** after the final build, read `git status` and stage from it, filtering out the known
unrelated untracked set. Then assert nothing tracked remains unstaged before committing.

---

## L-B1-4 — Adjudicate a temporal sweep by VALUE, not by count

**Proven:** 2026-08-12, ~450 candidates across six papers, zero real defects.

The sweep is detection-only and its raw counts are meaningless — QP2409 alone raised 110. Grouping
the candidates by their literal value collapses them to a dozen distinct facts that can each be
adjudicated once: 2030/2040/2050 are the 2023 GHG Strategy's own checkpoints, `26 June 2025` is the
Hong Kong Convention's known future entry into force, `1 July 2024` is quoted from `A.1187(33)`'s
own annex currency statement.

Three legitimate classes recur, and none is contamination:

1. a **future date stated by an instrument that is itself in force** at the sitting;
2. an **express exclusion** — the paper naming an anachronism precisely to warn the candidate off
   it (`A.1207(34)`, `MSC.560(108)`, FuelEU, the MS Act 2025);
3. a **boundary marker confined to the study surfaces** and kept out of the model answer.

Class 2 is why a keyword hit is not a finding: QP2409's spec contains every instrument its own
contamination list forbids, and each one is correct. **Check the framing, not the presence.**

---

## L-B1-5 — Give a zero-result sweep a positive control, in the same command

**Cost:** one false alarm, 2026-08-12.

A provider-leak sweep reported 19 hits of `HATC` in a shipped page. It was matching `hatc` inside
**hatch cover**. Re-run with `\bHATC\b` it reported zero — and a zero from a pattern that has just
been shown to be wrong is worth nothing.

**Do:** print the control beside the result, so the evidence that the detector works and the
evidence that the surface is clean arrive together:

```
regex \bHATC\b vs 'HATC notes' -> True   vs 'hatch cover' -> False
```

The same discipline applies in reverse: an exact-string replacement script must assert its expected
occurrence count and **write nothing** if any edit misses. That guard fired on the first QP2402 run
— a generic string had consumed the specific ones — and cost nothing but a re-ordering, because the
file was never written. Order replacements longest-first when one is a substring of another.

---

### 22. A self-test that HARVESTS its fixture from the live corpus is a wasting asset

`build_reuse_map.py --self-test` case 1 proves that solving a donor promotes a question C→D. It
found its fixture by scanning for an unsolved question whose recurrence family had **no** built
member, then adding one. That is a real mutation and a good test.

It is also a fixture mined from production state, and production state was being consumed by the
very process the test guards. Five such questions remained before this session — `QP2507-Q5`, `Q6`,
`Q7`, `Q8`, `Q9`. Solving QP2503 gave every one of them a donor, which is precisely what QP2503 was
scheduled to do and what its own anchor document predicted. Case 1 then reported:

```
FAIL case 1 C->D on donor arrival  -- no unsolved question with an unsolved family
```

The corpus had become **more** complete and the suite went red. Worse, it went red in a way that
reads exactly like a content regression on the paper being integrated, at the QA gate, minutes
before publication. The failure would have recurred on every future paper, permanently.

The fix is not to relax the assertion. It is to stop harvesting and start **synthesising**: take a
question that *does* have built donors and un-build them to construct the same starting state. That
is the identical mutation case 2 already relied on, it touches no spec, and so a classifier reading
frozen intake metadata still cannot pass it. The guard's strength is unchanged; only its dependence
on scarce production state is removed.

The general rule: **if a test mines the live corpus for its fixture, ask what happens when the
corpus runs out of that shape.** Anything the pipeline consumes will eventually be exhausted by the
pipeline. A fixture built by mutation from whatever exists is stable; a fixture that requires a
particular residue of unfinished work has a scheduled expiry date nobody wrote down.

```
EVIDENCE:  QP2503 integration, 2026-08-13. build_reuse_map.py case 1 failed at the QA gate with
           "no unsolved question with an unsolved family" after QP2503 supplied donors to the last
           five candidates (QP2507-Q5..Q9). Fixed at build_reuse_map.py by synthesising the
           baseline; case 1 now reports "[synthesised baseline]" and passes.
CATEGORY:  BUILD_QA
STATUS:    PROVEN
SEEN:      1
OWNER:     tools/pastpapers/build_reuse_map.py
REVISIT:   If a future self-test case is written that again scans for a naturally occurring corpus
           shape rather than constructing one, this entry applies to it before it is committed.
```

---

### 23. A tool that rewrites a spec must detect that FILE'S formatting, not the corpus convention

Removing one phrase from `study_notes` across eight specs was done by load / modify / `json.dumps`.
The dump used `indent=1`, which is what the corpus uses — except that `QP2410.json` and
`QP2501.json` are written with `indent=2`. Those two files came back as **6,493 and 5,858 changed
lines** for a four-word edit, burying the real change and destroying the reviewability of the diff.

The same trap had already been hit earlier in the same session on `QP2503.json` itself, from the
opposite direction: a first pass dumped at `indent=2` against an `indent=1` file and rewrote all
7,084 lines.

There is no single house convention to assume, and asserting one would mean reformatting files that
are not otherwise being touched. The discipline is:

1. Read the file, parse it, and **re-serialise it unmodified**; assert the result is byte-identical
   to what was read. That establishes the parameters — indentation, `ensure_ascii`, trailing
   newline, line endings — from the file itself.
2. Only then apply the edit and write with those same parameters.
3. Check `git diff --numstat` before committing. A one-word change that reports thousands of
   changed lines is a formatting accident, not a content edit.

Where the edit is a plain substring with no structural component, skip the round-trip entirely and
patch the raw text, asserting the occurrence count first. That is what was finally done on
`QP2503.json` and `QP2508.json`, and both produced one-line diffs.

```
EVIDENCE:  QP2503 integration, 2026-08-13. Two separate full-file reformats caught by
           `git diff --numstat` before commit: QP2503.json (7,084 lines) and QP2410.json /
           QP2501.json (6,493 / 5,858 lines). Both reverted and redone; final diffs 1-3 lines each.
CATEGORY:  AUTOMATION
STATUS:    PROVEN
SEEN:      2
OWNER:     NONE — no tool enforces this yet
REVISIT:   If a spec-rewriting helper is ever factored out into tools/, this becomes its contract
           and this entry should be promoted to PROMOTED_TO_TOOL.
```
