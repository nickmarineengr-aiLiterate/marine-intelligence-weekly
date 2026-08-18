# Phase 2A-ii — Oral Notes as secondary coverage and examiner evidence

**Branch:** `research/oral-examiner-intelligence-v1-phase2a-ii`, from
`research/oral-examiner-intelligence-v1-phase2a-i` @ `85035ba`
**Answers:** `review/oral-examiner-intelligence-v1-phase2` @ `c78a228` (Laptop)
**Scope:** the Notes layer only. The 681 canonical QB questions are unchanged, the
committed 788 reconciliation is still the Phase 2 one, no Release A was built, no P0
answer was written, no examiner-index V2 was generated, and no live product file was
touched. Every Oral Note was read; none was modified.

The governing rule of this phase, in four lines the code now enforces:

> The QB answers what MIW *asks*. The Notes answer what MIW *knows*.
> A page is not a section. Nairobi is not Nair. A note is never the tracker.

---

## A. What the Notes actually are

`meoclass1/oralnotes/` holds **44 HTML pages, 4.9 MB on disk** (3.79 MB of HTML; the
balance is `assets/` and the two manifests). The Laptop's "43 pages" is the same set
less the series landing page.

The folder is not homogeneous, and treating it as one corpus is the first way to get
this wrong. Two governed manifests already in the folder state what each page is, and
they are **read rather than re-derived**, so a page cannot silently change series:

| Role | Pages | Which |
|---|---|---|
| `SUBSTANTIVE_NOTES` | **39** | Simon Oral Notes ×8, Engineering Management ×22, Current Topics ×1, Written-Answer (WA) series ×8 |
| `NAVIGATION_INDEX` | 3 | `index.html`, `notes-master-index.html`, `uday-index-crossref.html` |
| `OUT_OF_SCOPE_WRITTEN_SAMPLE` | 2 | the January 2026 solved paper and written sample — Written QI product, not Oral Notes |
| `UNCLASSIFIED` | **0** | a page no manifest claims is excluded and reported, never guessed at |

The three navigation pages are excluded on purpose. Their rows are *links into other
pages*; ingesting them would let a table of contents rescue an ask that the page it
points at does not answer.

## B. Section-level, not page-level

This is the whole design. `simon-notes-p2.html` is 116 KB and mentions almost
everything; scored whole, it "covers" every ask put to it. So the unit of retrieval is
a **section**, and the four page dialects each yield one:

| Dialect | Unit | Count |
|---|---|---|
| Simon notes | `note-card` — one topic, one ask | 162 `NOTE_CARD` |
| Engineering Management | `topic-block`, plus its `qa-item` children | 92 `TOPIC` + 342 `QA` |
| WA series | `section-h` run, plus its exam prompts | 96 `TOPIC` |
| Current Topics | one numbered question block | 12 `TOPIC` |
| all | written-exam prompts | 288 `EXAM_Q` |

**992 note units**, 704 of them answer-bearing. Tug Girding is a 1,432-character unit
resolving to `simon-notes-p2.html#n9` — 1/80th of its page. Unit ids are derived from
series, page, authored anchor and title slug (`NOTE-SIMON-P2-N9-NO-009-TUG-GIRDING-…`);
never from array position alone, because Simon pages reuse an anchor id across two
elements. No id is canonical-shaped and none collides with a QB id.

Three parser defects were found and fixed while building this, each of which silently
destroyed content:

1. **Children inherited the parent's whole block** as their cue scope, so every examiner
   cue was counted once per sibling — 158 "Nair" hits on a page holding 17.
2. **The headline written question on every WA page was dropped**, because extraction
   started at the first section heading and that prompt sits above it. Eight prompts,
   the most important one on each page.
3. **WA exam prompts were prefixed with their marks badge**, because the two dialects
   nest the prompt differently.

## C. Notes support — a second, separate dimension

A source occurrence now carries two independent verdicts. They are graded on
**disjoint vocabularies**, and the validator asserts the disjointness:

```
CANONICAL:  EXACT_MATCH  NEAR_MATCH  SAME_CORE_ASK  PARTIAL_COVERAGE  MISSING  AMBIGUOUS
NOTES:      NOTES_COMPLETE_SUPPORT  NOTES_STRONG_SUPPORT  NOTES_PARTIAL_SUPPORT
            NOTES_TOPIC_SUPPORT     NO_NOTES_SUPPORT
```

`QB: MISSING` with `NOTES: COMPLETE_SUPPORT` means MIW holds the knowledge but not as a
canonical answer — a future **NOTES_TO_QB_PROMOTION**, never "an EXACT QB match".

The tiering rests on one distinction that does the real work: **aboutness versus
mention.** Coverage of the ask by a unit's *body* says the words appear somewhere in it.
Coverage by the unit's *title, subtitle and authored keywords* says the unit is **for**
the ask. A generic MARPOL note mentions a discharge limit in passing; a note titled for
that limit answers it. Only the second may reach STRONG or COMPLETE.

Four ceilings, each stating a reason the raw score cannot mean what it says:

- a contradictory technical designator caps at TOPIC;
- a one- or two-token prompt caps at TOPIC **unless** the unit is titled for the whole
  ask and answers it — a section called "Tug Girding — Capsizing Risk" is a dedicated
  treatment of "What is GIRDING?", not a coincidence of vocabulary;
- a unit that only *poses* a written-exam prompt caps at TOPIC: a question is not an
  answer;
- a missing designator or numeric demand caps below STRONG.

Thresholds are the Notes layer's own. **SAME_CORE admission is untouched**, and the
Phase 2A-i control set proves it.

One Notes-layer matching rule was needed. The source compilation writes ordinary words
in capitals for emphasis — `What is "GIRDING"?` — and the acronym pass turns each into
`dsg:girding` *alongside* the prose `girding`. Ordinary prose can never carry that
alias, so the same word counted twice made a dedicated section unmatchable. A designator
alias is now satisfied when the unit carries the word itself. This does **not** touch
the tokeniser, and conflict is still computed on the raw sets, so ME-GI against ME-GA is
unaffected.

## D. Examiner cues

**528 word-bounded alias occurrences** across the 992 units, from the alias register's
own observed forms — surname resemblance never merges two people.

| Disposition | Count | Evidence? |
|---|---|---|
| `NOTE_EXPLICIT_PRIMARY_ASK` | 473 | yes |
| `NOTE_EXPLICIT_FOLLOWUP` | 16 | yes |
| `NOTE_EXPLICIT_EXPECTED_DETAIL` | 11 | yes |
| `NOTE_WEAK_MENTION` | 27 | no |
| `NON_EXAMINER_NAME` | 1 | no |

**500 explicit cue occurrences → 289 unique examiner↔note-unit relations**
(Simon 173, Nair 60, Senthil 24, Paul 14, Rajappan 12, Srivastava 6). The Laptop's 189
was a page-level count; this is section-level and every row carries file, anchor, unit
id and a quoted excerpt.

Cues arrive by three vehicles, recorded so a reviewer can tell them apart: 280
`STRUCTURED_TIP` ("⚡ Simon Sir typically asks …"), 205 `STRUCTURED_ATTRIBUTION`
(`Examiner: Nair` fields on management topics), 43 `PROSE`.

An ask must be **bound to the name** — the verb has to sit in the short span following
the alias. A page that names an examiner in one sentence and uses the word "asks" three
sentences later is a weak mention, not a cue.

### The false-positive controls

The substring class this phase found is the largest single source of error:
**53 of the 220 literal "Nair" hits inside note units are "Nairobi"** — a wreck-removal
convention, not an examiner. Word-boundary matching removes all 53, and a control pins
it.

Two controls were written wrong first, and both were destroying real evidence:

- **`Examiner: Nair Medium Frequency`** was suppressed as a longer proper name, because
  the following capitalised word looked like a surname. It is a frequency badge. A
  structured examiner field now outranks the negative heuristics — 205 real
  attributions were being discarded.
- **`Bunker Convention 2001 vs. CLC 92`** was read as a legal case. This domain compares
  things constantly: "Audit vs Survey", "Double Class vs Dual Class", "WTW vs TTW".
  Comparison is not litigation, and the case control is now the citation form only.

What survives, and what the permanent controls assert: `John Doe v. The Motor Vessel
Olympic Prometheus` (legal case party — the single suppressed hit in the real corpus),
`John Ziegler` of Ziegler–Nichols (longer proper name), `USS John S. McCain` (ship
name), and author/compiler attributions. **John remains at zero examiner cues in the
Notes**, consistent with the alias register.

Provenance never rises above `NOTE_EXPLICIT` on `ORAL_NOTE_PAGE`. Only the three
explicit dispositions become evidence records; the 27 weak mentions and the 1 suppressed
name are counted in the audit and excluded from the ledger.

## E. What the Notes would move — analysis, not a baseline

| Notes support | Occurrences |
|---|---|
| `NOTES_COMPLETE_SUPPORT` | 153 |
| `NOTES_STRONG_SUPPORT` | 83 |
| `NOTES_PARTIAL_SUPPORT` | 320 |
| `NOTES_TOPIC_SUPPORT` | 177 |
| `NO_NOTES_SUPPORT` | 55 |

Against the canonical dimension, the row that matters is **MISSING (204)**: 10 complete,
3 strong, 72 partial, 81 topic, 38 none.

**This contradicts the Laptop's page-level estimate, and the contradiction is the
finding.** The review reported "12 of the 15 P0 gaps have material in the Notes",
supported by observations of the form "D-2 in 4 Notes pages", "dual-fuel in 3 Notes
pages". Read at section level, most of those are topic-level vocabulary overlap that
answers nothing: the ask about a change to the medical certificate finds its best hit in
the *Nairobi Wreck Removal Convention* topic. Topic support is therefore **not** treated
as material anywhere in this report. Only PARTIAL and above is.

### The old 15 P0 against the Notes

| Likely future disposition | Gaps |
|---|---|
| `NOTES_TO_QB_PROMOTION_CANDIDATE` | **1** — GAP-0002 GIRDING |
| `ENRICH_EXISTING_CANDIDATE` | **2** — GAP-0016, GAP-0069 |
| `NEW_ANSWER_CANDIDATE` | **11** |
| `NOTES_DO_NOT_CHANGE_GAP` | **1** — GAP-0043 |

Merge detection is independent of the Laptop's: GAP-0016, GAP-0069 and GAP-0410 all
resolve to the same best unit, *BWTS Type Approval — G8/G9*, and are merge candidates.

### Reverse connection value

436 rows where a Notes unit naming the examiner touches the ask: 177
`ALREADY_HAS_STRONGER_EVIDENCE`, 194 `NOTE_ADDS_SUPPORT`, **14
`NOTE_CREATES_NEW_EXPLICIT_CONNECTION`**, 51 `NOTE_UNRESOLVED`, across 330 unique
examiner↔question pairs. Nothing is published.

## F. Gates

| Gate | Result |
|---|---|
| `validate_phase2.py` | **66 PASS / 0 FAIL** (38 preserved, 28 Notes checks added; none removed) |
| `test_oral_controls.py` | **287 controls / 0 failures** (181 preserved + 106 Notes) |
| `mutate_phase2.py` | **25 mutations / 0 escapes** (16 preserved + 9) |
| `check_determinism.py` | **10 artefacts / 0 non-reproducible** across seeds 0, 1, 524287 |

New mutations: **M14** drops the Notes coverage layer (12 controls fail — the GIRDING
fixture goes first); **M14b** asserts support with no unit under it; **M14c** relabels
Notes support with a canonical disposition; **M14d** matches at page level instead of
section level; **M15** promotes a note cue to `PRIMARY_TRACKER`; **M16** disables the
non-examiner name controls (8 fail); **M17/M17b** point a unit at a missing page and a
missing section; **M18** injects a note unit as a canonical question id.

Two harness defects were found and fixed:

- The code mutations copy `tools/oral` to a scratch directory, so the copied modules
  derived a repo root inside the temp directory, found no data, and every code mutation
  "failed" on a missing file rather than on the injected regression — a caught mutation
  that proved nothing. `ORAL_REPO_ROOT` now states the root explicitly (no path is
  hardcoded), and M10/M11/M12 again report real control failures.
- `check_determinism.py` held its pre-run snapshot **in memory only**. A run killed
  part-way — and this gate is now slow enough to be killed by a timeout — left the
  regenerated artefacts in place with no way back. That happened once during this
  session and clobbered the committed Phase 2 baseline, which was restored from git. The
  snapshot is now written to disk before anything is regenerated and a stale snapshot is
  restored on the next run.

## G. Reported, not fixed — a Phase 2A-i limitation the Notes work surfaced

`designator_conflict` is exercised in production on mixed-case **sentences**, but the
Phase 2A-i controls compare **bare** designators. On a bare `ME-GI` the string is wholly
uppercase and the acronym pass is skipped; in a sentence it additionally emits `dsg:me`
and `dsg:gi`, both sides then share the family `me` with the value `me`, and the
conflict cancels:

```
designator_conflict(mtokens("explain the ME-GI standard"),
                    mtokens("explain the ME-GA standard"))  ->  False
```

**Not reopened here, deliberately.** The tokeniser is Phase 2A-i's, and `ME-GI`, `ME-GA`
and `ME-LGI` occur 27, 46 and 43 times in the QB and **zero** times in the Oral Notes —
no Note text exercises it, so the founder's condition for reopening is not met. A
control pins the present behaviour in both directions so it cannot change silently, and
**Phase 2A-iii must resolve it before adjudicating GAP-0409 (ME-GA)**, whose whole
question is whether an ME-GA ask can be wrongly awarded an ME-GI answer.

## H. Deliberately not done

681 canonical QB questions unchanged · 788 not recomputed or re-committed · Release A
not built · P0 not recomputed and no P0 answer written · examiner-index V2 not generated
· no connection published · no live QB, oralnotes, examiner-index, SQ, payments,
homepage, Written QI or magazine file modified · governance items left to the Founder.

## I. Governance — restated, unchanged

The research artefacts still live at `meoclass1/oral-intelligence/`, inside the deployed
web tree. Nothing was relocated and `.vercelignore` was not altered in this phase, per
instruction. The recommendation stands: this is research data sitting under a public web
root, and it should move out of it or be excluded from deploy before Release A.

## J. Next

**Phase 2A-iii** — combine the Phase 2A-i safe matcher with this secondary layer,
recompute all 788 source occurrences deterministically, produce the final Release-A
connection set and a small repaired P0 batch, with full movement traceability from
Phase 2. Resolve the mixed-case designator-conflict limitation in section G first, since
GAP-0409 depends on it.
