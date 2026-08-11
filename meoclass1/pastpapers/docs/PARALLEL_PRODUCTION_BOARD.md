# PARALLEL PRODUCTION BOARD — DESKTOP / LAPTOP PAPER ALLOCATION

**Status: DESIGN + EMPTY BOARD. No paper is allocated. No branch was created.**
Written 2026-08-11, in the pre-corpus-sync freeze session.

The allocation table in §5 is **deliberately empty**. It exists so that the moment the Founder
approves an allocation there is one governed place that answers *who owns which paper* — and so
that no paper is ever worked from two workstations at once.

---

## 1. One canonical repository. No exceptions.

```
        github.com/nickmarineengr-aiLiterate/marine-intelligence-weekly   (PUBLIC)
                            ▲                        ▲
                  push named branches        push named branches
                            │                        │
                   LAPTOP clone              DESKTOP clone
                   F:\Marine-Intelligence-Weekly
```

The laptop clone and the desktop clone are **working copies**. Neither is a truth store.

**Never:**

- copy finished specs between machines by hand, USB or ZIP;
- maintain a second repository, fork or "desktop version";
- work the same paper branch from both machines;
- push to `main`, or merge anything into `main`.

**Always:** every unit of work reaches the other machine only by `push` and `fetch` against that
one remote.

> This repository is **public**. Everything the desktop team pushes is published, on any branch,
> `noindex` or not. The source PDFs and `LOCAL_SOURCE_PROVENANCE.md` are git-ignored and must
> stay that way — a desktop clone will not receive them, and **that is correct**. A desktop
> producer needs the Founder to supply source copies out of band.

---

## 2. Branch model

Each assigned paper gets exactly one branch, named as the existing convention already does:

```
pastpapers/qpXXXX-founder-review
```

**All desktop branches start from ONE shared baseline commit**, nominated by the Founder, not
from six different historic heads. Branching six papers from six ancestors is what makes
integration a merge archaeology exercise instead of a review.

### PARALLEL PRODUCTION BASELINE COMMIT — proposed, awaiting Founder nomination

```
workflow/corpus-consumer-integration   -- HEAD at Founder approval
                                          935428d at the time of writing
```

Deliberately named as **the branch head, not a frozen hash**: this branch is under Founder review
and any review correction would move the hash, leaving a nominated commit that is no longer the
state anyone reviewed. The Founder nominates the head as approved.

**Supersedes the earlier `fddae20` proposal.** That commit was the newest state in which the
corpus, the toolchain, the delivery product and the recovered security stack were simultaneously
green — 252/117/135, 13 papers delivered, `health_check.py` 0/0, security 62/62. `541c5e4`
descends from the freeze head that carries all of it and adds the two things every future paper
branch should inherit rather than reinvent: the **True Source consumer seam**
(`tools/corpus/consumer_adapter.py`, the widened `REF_ID_RE`, the pilot shelf pattern) and the
**honest coverage** rendering.

The earlier note said the baseline should instead be "the commit that lands the corpus sync". That
condition is now satisfied differently and better: **the corpus is not synced into MIW at all.** It
is consumed read-only from its own private repository, so there is no corpus projection inside a
paper branch to go stale.

### REQUIRED CORPUS COMMIT FOR PARALLEL WORK

```
64977b86ed9c601e273f1d0cb55abb0461835811
nickmarineengr-aiLiterate/RulesApp-Local-Input   (PRIVATE)   origin/main
```

Every desktop or laptop paper branch must consume **this** corpus state.

- **Do not copy a corpus snapshot into a QP branch.** The consumer adapter reads the corpus from
  `MIW_TRUE_SOURCE_ROOT` (defaulting to `F:\RulesApp-Local-Input`) and degrades to
  `CORPUS_UNAVAILABLE` when it is absent, so nothing in the build depends on its presence.
- **Record the pair.** A paper's provenance is the MIW commit **and** the corpus commit. Only that
  pair makes its references reproducible.
- The corpus is **PRIVATE** and this repository is **PUBLIC**. No corpus file, source PDF or
  provision text may ever be committed here.

---

## 3. The global-derived-artefact conflict, and the rule that avoids it

This is the part that will actually break if it is not decided up front.

A paper branch legitimately produces two very different kinds of change:

| Class | Examples | Conflict behaviour |
|---|---|---|
| **Paper-local** | `specs/QPxxxx.json`, `verification/QPxxxx/*`, that paper's anchor doc | disjoint per paper — **never conflicts** |
| **Global derived** | reuse map, recurrence surfaces, search index, `pastpapers_content_index.json`, year sheets, `solvedQP/*`, `CURRENT_STATUS.md`, `SESSION_HISTORY.md`, `WORKFLOW_LESSONS.md` | **every branch rewrites the same files** — six branches conflict six ways |

The global artefacts are **regenerated wholesale from all specs**. Two branches that each
regenerate them produce two full-file rewrites of the same generated bytes. Git cannot merge
that meaningfully, and — worse — a textual merge that *succeeds* yields an index describing a
corpus state that never existed.

### RULE — paper branches do not commit global derived artefacts

```
PAPER BRANCH  owns:  specs/QPxxxx.json
                     verification/QPxxxx/**
                     docs/QPxxxx_TEMPORAL_AND_DONOR_ANCHOR.md

INTEGRATION   owns:  the reuse map, recurrence surfaces, search index,
                     year sheets, solvedQP/**, CURRENT_STATUS, SESSION_HISTORY,
                     WORKFLOW_LESSONS  -- regenerated ONCE, from all specs
```

A desktop producer still **runs** the full toolchain — that is how the paper is validated — but
commits only the paper-local paths. The regenerated global files stay in the working tree,
proving green, and are discarded.

**Verify this against the tooling before the first desktop paper is assigned.** The design rests
on the claim that every global artefact is fully derivable from the specs. `health_check.py`
already asserts *"every generated file reproduces exactly from its source"*, which is strong
evidence for that claim, but it has not been tested against a deliberately partial commit. That
test is one of the acceptance items in §6.

---

## 4. Two-stage model

### STAGE A — paper production (desktop)

Produce spec, verification records, temporal/donor anchor, paper-local evidence. Run the full
toolchain to prove green. Commit **paper-local paths only**. Push the branch. Stop.

### STAGE B — integration (laptop, one paper at a time)

Merge or cherry-pick one paper's local paths, then regenerate everything global **once**:
recurrence, reuse map, search index, year sheets, `solvedQP/`, PIL surfaces, delivery. Run
`run_toolchain.py`, `solvedqp_check.py` and the security suites. Then take the next paper.

**One at a time is not a throughput compromise, it is the correctness requirement.** Solving a
paper changes the derived readiness of *other* papers — proven twice in this corpus: the stored
Tier D field counts 8 over the unsolved set while the derived value counts 20, and solving
QP2511 unlocked six replacement donors. Integrating two papers in one regeneration pass hides
which one caused which change.

---

## 5. ALLOCATION TABLE — EMPTY. Founder approval required.

| paper_id | owner / workstation | branch | starting_commit | status | started_at | dependencies | reverse_hint_candidates | temporal_risk | last_push | review_status |
|---|---|---|---|---|---|---|---|---|---|---|
| *(none allocated)* | | | | | | | | | | |

**Status vocabulary:** `UNALLOCATED` · `ALLOCATED` · `IN PRODUCTION` · `PUSHED` · `INTEGRATING` ·
`INTEGRATED` · `BLOCKED`.

A paper may appear on this board **once**. Two rows for one paper is the failure this file
exists to prevent.

---

## 6. Acceptance before the first desktop paper starts

1. Founder nominates the baseline commit (§2).
2. Desktop clone verified: clone, `run_toolchain.py` green, `solvedqp_check.py` green,
   security 62/62 — on a machine that has **never** built this repository.
3. Prove the §3 rule: commit a paper-local-only change on a scratch branch, integrate it on the
   laptop, confirm the regenerated global artefacts are byte-identical to a full-tree build.
4. Source copies supplied to the desktop out of band (they are git-ignored by design).
5. Allocation approved and written into §5.

---

## 7. PROPOSED DESKTOP PAPER SET — candidates only. DO NOT START.

Derived this session from the 20 Tier D rows and the volatility column of
`2024_2026_RECURRENCE_AND_REUSE_MAP.md`. **This is a proposal for Founder/GPT approval after the
corpus sync, not an allocation.**

Per-paper donor readiness across the 15 unsolved papers:

| Paper | Sitting | Tier D | Volatility on its donors | Parallel verdict |
|---|---|---|---|---|
| **QP2401** | January 2024 | **3 / 9** | stable | **SAFE TO PARALLEL** — but see the Q9 collision |
| **QP2410** | October 2024 | **3 / 9** | **HIGH** (Q4), MEDIUM (Q5) | **SAFE**, with a re-anchor requirement |
| **QP2412** | December 2024 | 2 / 9 | stable | **SAFE TO PARALLEL** — but see the Q9 collision |
| **QP2409** | September 2024 | 2 / 9 | stable | **SAFE TO PARALLEL** |
| **QP2502** | February 2025 | 2 / 9 | stable | **SAFE TO PARALLEL** |
| **QP2411** | November 2024 | 1 / 9 | MEDIUM (Q2) | **SAFE TO PARALLEL** |
| QP2402 | February 2024 | 1 / 9 | stable | safe, thinner |
| QP2408 | August 2024 | 1 / 9 | stable | safe, thinner |
| QP2503 | March 2025 | 1 / 9 | **HIGH** (Q6) | safe, thinner |
| QP2504 | April 2025 | 1 / 9 | stable | **BLOCKED — see below** |
| QP2406, QP2407, QP2501, QP2507 | — | **0 / 9** | — | **BETTER SEQUENTIAL** — all-fresh research |
| QP2512 | December 2025 | **3 / 9** | stable | **KEEP ON THE LAPTOP** — see below |

### The six-paper proposal

**QP2401 · QP2410 · QP2412 · QP2409 · QP2502 · QP2411** — the six best-donor-supported unsolved
papers, five of them 2024, which is exactly the Founder's stated goal of finishing 2024 faster.

### Three constraints that must travel with the allocation

- **QP2401-Q9 and QP2412-Q9 share an identical donor set** (`QP2403-Q7`, `QP2510-Q7`). They are
  not dependent on each other — both donors are already solved — but two owners researching them
  independently will duplicate the work and can produce two divergent answers to the same
  examiner task. **Allocate both papers to the same owner, or sequence them.**
- **QP2410 carries the corpus's only HIGH-volatility donor pair** (Q4 from `QP2511-Q8`, Q5 from
  `QP2511-Q7`). An exact question is **not** an exact answer object: every sitting-relative
  statement must be re-anchored to October 2024, not inherited from November 2025. This is a
  known, twice-proven failure mode and it must be in the work order, not discovered.
- **QP2504 is not free to start.** A standing stop condition forbids answering `QP2504-Q9` from
  either cyber donor until the April 2025 examination date is established against the 4 April
  2025 issue date of Rev.3. **Do not allocate QP2504 to a producer who cannot resolve that.**

### Why QP2512 is excluded despite scoring well

QP2512 is the strongest single next paper (3/9 Tier D, two donors from QP2511 itself, the whole
November 2025 line transferring with one adjustment). That is precisely why it should **not** go
to a parallel producer: its single sharp risk is the 34th Assembly boundary — the Assembly sat
24 November – 3 December 2025 and adopted at the close, so a December sitting can fall on either
side of it. That is a judgement call this lineage has already got wrong once in the other
direction. Keep it where the temporal history lives.

### Why the four zero-donor papers are excluded

QP2406, QP2407, QP2501 and QP2507 start from **zero** verified donors — nine fresh research
questions each. QP2507 additionally holds the corpus's highest family reach (8), which means
solving it changes the derived readiness of many other papers. Running it in parallel wastes
that leverage; running it *first* would improve everything downstream. It is a sequential
laptop paper, not a desktop one.

---

## 8. Standing rules for a desktop producer

- Read `PRODUCTION_PROTOCOL_INDEX.md` first. It governs precedence.
- No merge to `main`. No removal of `noindex`. No gating change. No deployment.
- Never commit or delete a source PDF. This repository is public.
- Never hand-edit `solvedQP/` — it is a projection.
- `recurrence_class` is an **authoring** field and must never face a candidate.
- Write specs with LF endings. CRLF corrupts content-hashed assets.
- Every git command in this repository needs `-c safe.directory=*`.
