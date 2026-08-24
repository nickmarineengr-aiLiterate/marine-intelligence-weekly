# The current-answer library — a present-day answer with nowhere to live

**Status: RATIFIED (Founder decision, 2026-08-24).**
`meoclass1/current-answers/` is the governed owner of MIW's present-day
canonical questions and answers. It is not a past paper, it is not a second
copy of one, and nothing in it is evidence that any examiner asked anything.

---

## The sentence the whole layer rests on

> **AN EXAM QUESTION HAS A DATE. A CURRENT ANSWER HAS A REVIEW DATE.**
> They are different objects. QI connects them.
> The past paper preserves what was asked. The library preserves what should
> be answered today.

## Why it had to exist

`PHASE2_PRESENT_DAY_LAYER.md` established that MIW written answers are
**sitting-anchored**, and that a family-level present-day record therefore has
to carry its own review date. Phase-2 tranche 002 then discovered the hole in
that arrangement, six times, and named it `HOLD_NO_CURRENT_ANSWER_OWNER`.

The wall was structural, not editorial. The research closed perfectly well; the
product had nowhere to put the result:

- every member of every one of those families is a **2021 or 2022
  wording-only** record;
- `validate_phase2_tranche.spec_question_ids()` drew the set of nameable
  answers **solely** from `meoclass1/pastpapers/specs/*.json`, the solved
  2023–2026 set;
- so a present-day answer could only be named **by inventing a question inside
  a past paper**, which would make that paper cite law that did not govern it.

Two of the six were blocked a **second, independent** way: `QIF-EM-0024` and
`QIF-EM-0052` are term-list questions whose limbs are answered by several
different solved questions, and `canonical_current_answer` names exactly one
question **by design** — the rule that stops a family resolution blessing every
sitting inside it. A four-limb family had no expressible owner at all.

This layer fixes both, and it fixes the second one without relaxing the first.

## What was built

| Path | Role |
|---|---|
| `meoclass1/current-answers/specs/CA-EM-*.json` | **Hand-authored, canonical.** One present-day question and answer per entry. |
| `meoclass1/current-answers/registry.json` | Generated index. Never hand-edited. |
| `solvedQP/current/CA-EM-*.html` | The gated candidate page. |
| `tools/current_answers/ca_model.py` | Schema, id grammar, and the ownership resolver. |
| `tools/current_answers/build_current_answers.py` | Only writer of the registry and the pages. `--check` proves disk matches inputs. |
| `tools/current_answers/validate_current_answers.py` | The gate. 51 invariants, fails closed. |
| `tools/current_answers/test_current_answer_mutations.py` | 22 mutations, all must be caught, zero residue. |

```bash
python tools/current_answers/build_current_answers.py
python tools/current_answers/build_current_answers.py --check
python tools/current_answers/validate_current_answers.py
python tools/current_answers/test_current_answer_mutations.py
```

## Identity

`CA-EM-nnnn`. `EM` is the Engineering Management stream, the same stream letter
the QI family ids use, so the two id spaces read as siblings.

The id is **sitting-independent on purpose**, and that is load-bearing rather
than tidy. A current answer outlives every sitting that evidenced it, and the
2010–2020 concept archive — when it is built — must be able to point at these
same ids without inventing a year for them. `R-CA-ID-NOT-QP` refuses a
QP-shaped id anywhere in the library: in an entry, in a filename, or in a
rendered page name. Every consumer in this repo — the recurrence model, the
examiner layer, the year sheets — keys on that shape.

## Ownership is TYPED

A Phase-2 family record names its answer through one of four owner types:

| `owner_type` | Means |
|---|---|
| `SOLVED_PAPER` | A whole solved past-paper question answers this family. |
| `SOLVED_PAPER_LIMB` | A limb of a solved question answers ONE limb of this family. |
| `CURRENT_LIBRARY` | A library entry answers this family. |
| `CURRENT_LIBRARY_LIMB` | A library entry answers ONE limb of this family. |

`ca_model.resolve_owner()` is the single place that normalises, and it accepts
the two legacy shapes (`{question_id: ...}` and a bare string) as
`SOLVED_PAPER` — because when they were written, a solved past-paper question
was the only nameable answer in existence. Those shapes are **not extended**:
`R-P2-OWNER-TYPED` and `R-CA-OWNER-TYPED` refuse a library owner written
untyped. Without that refusal a library id would be resolved as a past-paper
question, fail to appear in the spec set, and surface as "points at a question
that does not exist" — a confusing failure a long way from its cause.

A family is owned **whole** (`canonical_current_answer`) or **limb by limb**
(`family_current_answers`), **never both** — two answers to "where does this
candidate go" is one too many, and the two will drift. `R-P2-OWNER-EXCLUSIVE`
and `R-CA-OWNERSHIP-EXCLUSIVE` refuse it from each side.

### The one-answer rule is not relaxed. It moves down a level.

Limb ownership does not reopen the hole tranche 001 fell into. The rule that a
grant reaches exactly ONE answer now holds **per limb**: each limb names one
owner, each owner is reviewed on its own evidence, and `R-CA-LIMB-SLOT` refuses
a `LIMB`-scope entry claimed as a whole-question owner or vice versa. A sibling
limb can only be reached through its own slot, so verifying one can never
verify another.

### The slot has a scope, and so does the type

The two rules above govern *which store* an owner names and *whether* a family
mixes whole and limb ownership. Neither governs the pairing between them: the
whole slot means "this answers the family" and a limb type means "this answers
one limb of it", so `SOLVED_PAPER_LIMB` written into `canonical_current_answer`
is well-typed, well-shaped, resolvable — and says the opposite of what it means.
`R-CA-OWNER-SLOT` and `R-P2-OWNER-SLOT` refuse the pairing from both sides:
the whole slot takes only `SOLVED_PAPER` or `CURRENT_LIBRARY`, the limb list
only the two `_LIMB` types.

This matters because a limb owner carries a **real question id**, so any reader
that matches on the id alone hands it the whole question. Three did.

## The owner-reader contract

**A consumer MUST NOT parse Phase-2 ownership ad hoc.** It either resolves
through `ca_model` — `resolve_owner`, `owner_ids`, `library_owner_ids`,
`paper_owner_ids`, `entry_url_for` — or it states in its own docstring which
single owner class it consumes and why. Reading `canonical_current_answer` for
an id and comparing that id to something is not resolution; it is the parsing
rule the typed model was introduced to remove.

Three consequences, and they are the whole contract:

1. **Scope is decided by the type, never by the id.** `_named_answer` tests
   `== 'SOLVED_PAPER'`, not `in PAPER_OWNER_TYPES`, because the second admits
   `SOLVED_PAPER_LIMB` — and a limb answer is not an answer to the question.
2. **Unknown owner types fail closed.** An `owner_type` the repository does not
   recognise grants nothing, routes nowhere, and is refused by
   `R-CA-OWNER-TYPE-KNOWN`. It is never read as the legacy solved-paper shape.
3. **A whole-only reader is legitimate — if it says so.** Not every surface
   should widen to accept limb owners; some must not. What is forbidden is
   being whole-only *by accident*, which is what a bare id comparison is.

`tools/current_answers/test_owner_reader_contract.py` asserts this against the
readers themselves, on constructed records rather than on whichever families
happen to be owned which way today. It is deliberately separate from the gate
suites: the gates refuse a bad record, and this refuses a good record read
badly — which is the failure that has actually happened, twice.

## The reuse order, and the evidence that it does work

For each family, in order:

1. a valid existing **solved-paper answer**;
2. a valid existing **solved-paper limb**;
3. a **library entry**;
4. several **library limb entries**;
5. **HOLD**.

Never create a library answer merely because one would be convenient.

`QIF-EM-0052` is the worked case and it is worth reading before planning a
tranche, because the reuse order **changed the output**. The obvious plan was
four library answers for a four-limb question. Reading the four candidate
solved owners in full reduced it to two:

| Limb | Owner | Type |
|---|---|---|
| A. Lloyd's Open Form | `CA-EM-0002` | `CURRENT_LIBRARY_LIMB` |
| B. General and Particular Average | `QP2304-Q3` | `SOLVED_PAPER_LIMB` |
| C. Bill of Lading | `QP2510-Q2` | `SOLVED_PAPER_LIMB` |
| D. Treaty, Convention and Protocol | `CA-EM-0003` | `CURRENT_LIBRARY_LIMB` |

The two **rejections** were tested against the standard tranche 002 set when it
refused `QP2406-Q8`: does the candidate owner answer THIS examinable task, or a
neighbouring one? `QP2406-Q8` answers the principles of salvage law and never
says what Lloyd's Open Form is. `QP2308-Q7` answers the four stages of
adoption, not the instrument taxonomy — and it fails a second way besides: it
carries **no canonical QI family at all**, so routing to it would send a
candidate to a question the readiness layer knows nothing about.

## A library answer blesses NO sitting

This is the property that makes the whole thing safe, and it falls out of the
type rather than being enforced by a special case.

`study_qi_adapter.question_readiness()` grants Phase-2 readiness only to the
question a record NAMES. A library-owned family names a `CA-EM-nnnn`, which
matches no question id, so **no member question is blessed**. MIW now answers
the CONCEPT and has still not answered the 2021 sitting — and
`questions-2021.html` still says so in its header.

Measured, not argued: resolving `QIF-EM-0014` and `QIF-EM-0052` moved question
readiness for **zero** questions in `safe_qi_projection.json`.

## What a candidate sees

Nine archive questions gained a route. What they did **not** gain is a
readiness change.

- A whole-question owner renders one chip: **Current framework answer →**,
  linking to `/solvedQP/current/CA-EM-nnnn.html`.
- A multi-limb family renders **one chip per limb**, so a partly-covered
  question shows its coverage honestly instead of hiding a gap behind one
  reassuring link.
- `Current-framework answer in preparation` is **suppressed** where a route
  exists. Once the answer is published that chip is false, and false in the
  direction that costs a customer something: it tells them to wait for work
  that is already done and already paid for.

The chip is a **link**, unlike the successor pointer, which stays a sentence.
The difference is that a library URL is deterministic and `R-CA-PAGE-EXISTS`
guarantees a verified entry has a page, whereas a successor may sit on a paper
the reading surface does not carry.

A link is louder than a chip, so the archive legend states what is on the other
side **before** offering it — `R-CA-ARCHIVE-LABEL` reads the shipped bytes
around every library id and refuses the word "solved".

## Gating

The gate is the **middleware matcher**, not a header and not a meta tag.
`middleware.js` matches `["/meoclass1/:path*", "/solvedQP/:path*"]` and
middleware is **never invoked off-matcher** — a page one directory outside
those prefixes is public whatever its headers say. That is why current-answer
pages live at `/solvedQP/current/`, and `R-CA-GATED-MATCHER` fails the build if
the matcher stops covering them.

The public roadmap is unchanged by this layer and `R-CA-PUBLIC-ROADMAP` proves
it: `SQ/study-roadmap.html` rebuilt **byte-identical**. The `PUBLIC` tier
whitelist in `qi_projection` does not carry the route fields, so a paid URL
cannot reach the public surface by accident.

## Versioning and review

A current answer may change when a past-paper answer may not, so it carries
what a past-paper answer does not need:

- `answer_version` and a `version_history` row per material change, each
  recording version, date, reason and the authority that moved
  (`R-CA-VERSION`, `R-CA-VERSION-FIELDS`);
- `authority_review_date` and `currentness_as_of`;
- `next_review_trigger` — the event that should reopen it, not just a date.
  `CA-EM-0002` is on twelve months because LOF editions and SCOPIC revisions
  move; `CA-EM-0003` is on twenty-four because completed treaty events do not,
  and the record says why rather than leaving the difference to look like an
  oversight.

`CURRENT_ANSWER_VERIFIED` is earned by dated primary authority **and** an
independent review that passed. Nothing else is rendered at all — a `DRAFT`
that merely lacks a badge is still an answer a candidate can read and write in
an exam.

## Zero recurrence, zero examiner evidence

A present-day canonical question was set by **nobody**. MIW's whole recurrence
product rests on "this was actually set, on this date, and here is the printed
copy", so if a synthetic question ever leaked into the occurrence layer, every
count MIW publishes would become a number partly about itself.

Proved by sweep, not asserted: `R-CA-NO-RECURRENCE` scans the occurrence,
family and entity stores for the id shape; `R-CA-NO-EXAMINER` scans the oral
and examiner layer; `R-P2-NO-SYNTHETIC-MEMBER` refuses a library id appearing
as a family member; and `R-CA-NOT-AN-OCCURRENCE` catches the inverse — an entry
quietly growing occurrence-layer fields.

`R-CA-NO-SITTING` refuses a sitting field on an entry outright. A field cannot
be "mostly absent": the moment one appears, some consumer will read it.

## Recommended depth is not a printed mark

An entry may carry a `recommended_exam_depth`, and it must declare
`basis: RECOMMENDED_NOT_PRINTED` (`R-CA-MARKS-BASIS`). The sittings that
evidence these families print a **paper total only**, with no per-question
split. "Prepare to 16-mark depth" is a recommendation MIW makes about the
format a candidate now sits. "This was a 16-mark question" would be a claim
about a printed paper, and it would be false.

## Two things this layer does NOT yet do

Recorded here rather than discovered later:

1. **The workbook shows no per-family current-answer ownership.** Both
   acceptance families are topic-**unmapped**, so neither reaches the
   topic-driven `STUDY QUEUE` sheet. Adding owner columns to a sheet the
   samples do not appear on would be untestable decoration. What the workbook
   does reflect is the corpus-level movement, on `WRITTEN QI`: families ready
   to study now, 88 → 90. Mapping was **not** invented to improve that number.
2. **`export_roadmap_xlsx.py` is not byte-deterministic** — the workbook
   rebuilds differently from identical inputs, so no byte gate can cover it.
   Pre-existing, and noted because every other artefact in this chain is
   determinism-checked and the workbook silently is not.
