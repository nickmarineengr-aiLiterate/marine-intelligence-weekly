# DESKTOP QP PRODUCTION PLAYBOOK

**Machine-independent production instruction for a second Claude Code team.**
Written 2026-08-11 on the laptop, in the parallel-production baseline session.

This file exists so that a **fresh Claude Code session on the desktop PC** can reproduce the
answer-production method this laptop team developed, without the Founder explaining it again.

If you are that session: read this file completely before you touch a spec.

---

## 0. STATUS BLOCK — read these values first

| | |
|---|---|
| **MIW remote** | `https://github.com/nickmarineengr-aiLiterate/marine-intelligence-weekly.git` — **PUBLIC** |
| **Desktop parallel baseline commit** | **`9c97359`** — see §16. **Immutable for all six papers** |
| **Corpus remote** | `https://github.com/nickmarineengr-aiLiterate/RulesApp-Local-Input.git` — **PRIVATE** |
| **Required corpus commit** | recorded in §16 |
| **Allocation** | [`DESKTOP_QP_ALLOCATION_2024.md`](DESKTOP_QP_ALLOCATION_2024.md) — exactly six 2024 papers |
| **Written product deployment** | **NOT DEPLOYED.** See §17. This does not block QP authoring |
| **Laptop QP production** | **PAUSED.** The laptop authors no paper while these six are open |

---

## 1. PURPOSE

Produce **Founder-review-quality MEO Class I Written solved papers** using the canonical MIW
workflow — the same method, the same structure and the same standard of proof as the thirteen
papers already built.

You are not inventing a method. You are executing one that is written down and has been
cross-validated over thirteen papers and 117 questions.

---

## 2. AUTHORITY — where truth lives

**One canonical repository.** The GitHub remote above is the only truth store for MIW. The laptop
clone and the desktop clone are both *working copies*. Neither becomes a second source of truth.

**One canonical corpus.** `RulesApp-Local-Input` **GitHub main** is the only True Source state you
may consume. Not a laptop folder, not a copy, not uncommitted producer work.

Work reaches the other machine only by `push` and `fetch`. Never by USB, ZIP, hand-copied specs or
a "desktop version" of the repository.

> **This repository is PUBLIC.** Everything you push is published, on any branch, `noindex` or not.
> Source PDFs and `LOCAL_SOURCE_PROVENANCE.md` are git-ignored and must stay that way. Your clone
> will therefore **not** contain the source PDFs — that is correct, not a fault. The Founder
> supplies source copies out of band. See §5.

---

## 3. REQUIRED READ ORDER

Read in this order, before authoring anything:

1. [`PRODUCTION_PROTOCOL_INDEX.md`](PRODUCTION_PROTOCOL_INDEX.md) — precedence and routing. **This wins over this playbook** wherever they appear to differ.
2. [`PASTPAPER_PRODUCTION_PROTOCOL.md`](PASTPAPER_PRODUCTION_PROTOCOL.md) — the mandatory production protocol.
3. [`TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md`](TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md)
4. [`EXECUTION_EFFICIENCY_POLICY.md`](EXECUTION_EFFICIENCY_POLICY.md)
5. [`QA_AND_HANDOVER_PROTOCOL.md`](QA_AND_HANDOVER_PROTOCOL.md)
6. [`CURRENT_STATUS.md`](CURRENT_STATUS.md) — state only.
7. The **relevant** [`WORKFLOW_LESSONS.md`](WORKFLOW_LESSONS.md) entries — targeted reads by category.
8. **This file.**
9. [`DESKTOP_QP_ALLOCATION_2024.md`](DESKTOP_QP_ALLOCATION_2024.md) — your board.

Then, for the specific paper only: its `QP####_TRUE_SOURCE_DEMAND_MAP.md` if one exists, and its
donor rows in [`2024_2026_RECURRENCE_AND_REUSE_MAP.md`](2024_2026_RECURRENCE_AND_REUSE_MAP.md).

**Do not load `history/SESSION_HISTORY.md` broadly.** It is large. Read a specific `§N` only when
you need the record of how one decision arose.

---

## 4. THE STANDING PRODUCTION RULE

> # AUTOMATE REPETITION.
> # CLAUDE ADJUDICATES MEANING.

**Tool-driven — never done by hand:** validation, building, index regeneration, reuse-map
computation, temporal sweeps, contamination sweeps, determinism checks, HTML rendering, counts.

**Claude's own effort — never delegated to a tool:** question interpretation, donor selection,
technical and regulatory distinctions, temporal truth, learning design, final verification.

A sweep **flags**; you **adjudicate**. `PIL FLAGS; CLAUDE ADJUDICATES` is the same rule stated for
the Production Intelligence Layer. A zero-result sweep is a claim that must itself be controlled —
see §9.

---

## 5. ONE PAPER AT A TIME — non-negotiable

Six papers are allocated. **Work one.**

Finish, in order, for paper *N* before paper *N+1* begins:

```
source verification → Q1…Q9 → verification records → paper QA → commit → push → handover
```

**Do not run six Claude authoring sessions concurrently.** The reasons are concrete:

- **Cores and disk**, not RAM, are the binding constraint on a typical machine; concurrent Python,
  Node and browser jobs contend for the same queue and finish later than one sequential pass.
- **Context.** A paper needs its sitting anchor, its donors and its nine stems held together. Two
  papers in one context is how a donor from the wrong sitting gets used.
- **Source quality.** Each paper has its own source verification. Interleaving them is how a
  question from the wrong PDF is authored.
- **Branch hygiene.** One open paper branch at a time cannot collide with itself.

At most **two** Claude Code sessions should be live on one machine, and only one of them authoring.

---

## 6. SOURCE FIRST

Before any question is authored, for every paper:

- Verify the **source PDF/text** actually in front of you is the paper you think it is.
- Verify **paper ID**, **month**, **year** and **serial** (`EM-####`) — the serial is the strongest
  identity check and has caught a mislabelled intake before.
- Verify **Q1–Q9** exist, and each question's **limbs** and **marks**.
- Record **printed anomalies** exactly as printed.

**Preserve examiner and source errors. Never silently normalise printed truth.** If the paper
prints a wrong resolution number, an odd mark split or a malformed limb, the spec records what was
printed and the anomaly is noted — it is not corrected into what the examiner "meant".

> **The most dangerous error in this workflow is a wrong-edition source.** A paper that is really a
> reprint of another sitting, or a file named for the wrong month, poisons every downstream
> judgement. October 2025 was found to be March 2024 reprinted whole. Check the serial.

**Notes supplied by third-party publishers are not authority.** Where a `Notes-for-written-answers/`
style note exists, it is error-seeded and must never be cited as a source.

---

## 7. REUSE / DONOR WORKFLOW

For **every** question, derive and record:

| Field | Meaning |
|---|---|
| **Tier** | the reuse classification, **derived**, not read from a frozen field |
| **Preferred donor** | the specific solved `QP####-Q#` you are reusing, if any |
| **EXACT / NEAR** | whether the printed stems are identical or merely close |
| **Question delta** | what changed in the wording |
| **Marks delta** | what changed in the mark allocation |
| **Temporal delta** | what changed in the law between the two sittings |
| **Fresh-research requirement** | what this question needs that the donor cannot supply |

### Four rules that have each already caught a real defect

1. **Never trust a stored `reuse_tier` blindly.** Tiers are derived from the *currently built* set.
   A frozen field goes stale the moment another paper is solved. Use `derived_reuse_tier`.
2. **Reverse hints are for discovery only.** The reverse-hint queue surfaces *candidate* pairs. A
   row in that queue is **not** a donor. Only an author who has read **both printed stems** may
   write `reused_from`.
3. **Host recurrence hints are not MIW truth.** Third-party host annotations are directional — they
   point backwards only — so they systematically under-report readiness and must never leak to a
   candidate-facing surface.
4. **An exact question is not an exact answer.** Where a stem recurs verbatim, the *answer* must
   still be re-anchored to the new sitting. Sitting-relative prose ("recently adopted", "not yet in
   force", "the current edition") is re-authored on every reuse, never copied.

---

## 8. TEMPORAL VERIFICATION

**Every paper is anchored to its own sitting date.** Build the anchor before the answers.

- A **later** solved donor does **not** transfer later law backwards.
- An **earlier** solved donor does **not** automatically contain later amendments.

For every regulatory or legal claim, distinguish — and say which one you mean:

```
adopted · approved · entered into force · operative · superseded · revoked · proposed · future
```

**Adopted ≠ approved ≠ in force.** These have been confused in real papers and are the single most
common source of a wrong answer.

### Standing boundary for all six allocated papers

> The **33rd IMO Assembly** adopted its resolutions on **6 December 2023**. Every 2024 sitting
> therefore falls *after* that boundary, and the `A.11xx(33)` editions are the operative Assembly
> instruments for all six allocated papers.

This is the 2024 analogue of the 34th Assembly boundary that governs 2025 sittings. Note the shape
of the rule that generalises: **an Assembly boundary is the adoption date, not the meeting month.**

The **Merchant Shipping Act 2025 commenced 15 March 2026**, so every 2024 sitting sits wholly under
the **Merchant Shipping Act 1958**. Do not import MS Act 2025 provisions into a 2024 answer.

Run the temporal sweep. **A zero-result sweep must be controlled** — prove the filter can fire by
seeding a known positive, or the zero means "the sweep is broken", not "the paper is clean".

---

## 9. TRUE SOURCE / CORPUS USE

Consume the **same private corpus main state** recorded in §16. **Record the exact corpus commit
used for every paper** in that paper's handover.

| Corpus | Current standing position |
|---|---|
| **LSA Code** | **Consumer-ready where applicable** — quotation-ready, 292/292 verbatim, native `LSA-1.1.1` addressing |
| **FSS Code** | Producer team is **resolving the derivative/status issue**. Evidence-ready, **not** quotation-ready |
| **MARPOL Annex VI** | Producer team is **resolving the derivative**. **Citation-ready only** — resolves to identity and provenance, never to text |

**Do not wait for enrichment.** If the paper can be correctly verified from the governed
primary-source workflow, author it. Corpus enrichment is not a launch or production blocker.

**Do not fabricate corpus references.** A missing corpus object is recorded as
`REFERENCE_PENDING` (or the appropriate pending status) — never invented, never guessed.

**Corpus truth flows outward. QP production never edits True Source.** If you find a corpus defect,
raise a `TRUE_SOURCE_CORRECTION_REQUEST` and notify the Founder. Do not fix it locally.

If the private corpus is absent, the consumer adapter degrades to `CORPUS_UNAVAILABLE` and no build
depends on it. That is designed behaviour.

---

## 10. LEARNING ARCHITECTURE — the frozen MIW model

Every answer carries five parts, in this order:

```
Understand → Exam Plan → Answer → Study Guide → Recall
```

| Part | What it is |
|---|---|
| **Understand** | the conceptual map — what this question is really about |
| **Exam Plan** | how the candidate *writes* the answer, in the room, against the clock |
| **Answer** | the exam-ready structured answer itself |
| **Study Guide** | deeper technical and regulatory understanding behind the answer |
| **Recall** | the retrieval skeleton and flashcards |

**One question-specific spine.** `answer_route` is the single canonical sequence; the map, recall,
flashcards and cheat sheet all **derive** from it. Never author a route twice.

**A derived layer must never be more categorical than the verified answer.** If the answer says
"generally required", the flashcard does not say "always required". This has caught a real
regression.

**No generic template masquerading as question-specific structure.** If the Understand section
would read the same for any question in the family, it is not finished.

---

## 11. MIW EXAM-ANSWER STYLE

The style exists to solve **real candidate failure modes**:

- cannot complete the paper in time;
- answer too short;
- too few scoring propositions;
- weak underlying understanding;
- cannot remember it under pressure;
- cannot sequence the answer.

Therefore every answer uses:

- **numbered, sequenced scoring propositions** — countable marks, not prose;
- **clear subheadings**;
- an **explicit starting point**;
- a **logical writing order**;
- a **memory route**;
- **expandable detail** — a short version that scores and a longer version that scores more.

The candidate must finish knowing:

> **START HERE → WRITE THIS NEXT → CONTINUE IN THIS ORDER.**

---

## 12. IF A PAPER DOES NOT FINISH IN ONE SESSION

**There is no valid half-authored-paper state in a canonical spec.** Never leave `specs/QP####.json`
partly solved — the build rejects it and the product would misreport coverage.

Use the proven staging mechanism instead:

```
meoclass1/pastpapers/staging/QP####/
```

- Verified question objects live **outside** the canonical spec, in staging.
- The canonical spec stays in its **intake** state until 9/9 exist.
- Write `staging/QP####/CHECKPOINT.md` recording: completed questions · sources · donors ·
  temporal findings · verification state · **exact resume instructions**.

The next fresh session resumes on the **same branch**. When 9/9 are complete:

```
guarded mechanical assembly → validate → build → retire staging
```

The assembly step is mechanical and guarded — it moves verified objects in, it does not author.

---

## 13. BRANCHES AND OWNERSHIP

Each allocated paper gets exactly one branch:

```
pastpapers/qp####-founder-review
```

**Every desktop branch starts from the ONE shared baseline commit in §16.** Not from six different
historic paper heads — branching six papers from six ancestors turns integration into merge
archaeology instead of review.

The desktop workstation **owns that paper branch until completion**. The laptop will not
independently author the same paper.

### 13.1 What a paper branch MAY commit

- `meoclass1/pastpapers/specs/QP####.json`
- `meoclass1/pastpapers/verification/QP####/…`
- that paper's anchor and checkpoint evidence
- `meoclass1/pastpapers/QP####.html` — the **review** build (see §13.3)
- a paper-specific test or fixture, **only** where genuinely required

### 13.2 What a paper branch MUST NOT own — critical for six parallel papers

Do **not** commit independently regenerated **global** artefacts:

- the global reuse map · the reverse-hint global queue · global recurrence indexes
- the site-wide content index (`pastpapers_content_index.json`)
- `questions-YYYY.html` · `topics-YYYY.html`
- `solvedQP/index.html` · `solvedQP/questions-YYYY.html`
- **any other paper's** regenerated HTML
- `CURRENT_STATUS.md` · `history/SESSION_HISTORY.md`
- shared product inventory · shared public sample counts

Normal tooling **will** regenerate several of these during QA. That is fine and expected:

> **Use them to validate, then restore the global derived files before you commit.**

`git status` before every commit, and revert what you do not own. **The final laptop integration
stage owns global regeneration** — one paper at a time, so six branches never fight over the same
derived files.

### 13.3 Paper review HTML

The Founder wants six reviewable solved-QP HTML files. So every completed desktop paper **does**
produce its own `meoclass1/pastpapers/QP####.html` — the review build.

But do **not** commit its final `solvedQP/QP####.html` customer projection as integrated product
truth. If existing tooling makes a paper-specific projection unavoidable during testing, classify
it explicitly as **review output** and do not modify the global delivery inventory.

**Laptop integration creates the final customer-facing projection.**

---

## 14. QA REQUIRED FOR EVERY PAPER

### 14.1 Question QA

- 9/9 authored
- 9/9 verification records
- `validate_spec` — **0 errors**
- temporal sweep
- donor contamination sweep
- internal Q-reference sweep
- authoring-date sweep

> **The authoring-date sweep must be field-class-aware and run against shipped bytes**, not only
> against specs. A line-number grep has produced a wrong question id before, and a naive scan
> missed two hits because it never searched for the second month name.

### 14.2 Paper QA

Run the relevant paper-level toolchain checks:

```bash
python tools/pastpapers/run_toolchain.py
```

If the full toolchain produces global derived changes, **validate them, then revert the
non-owned global outputs before committing** (§13.2).

**Do not weaken a test to make it pass.** If a validator fails, the spec is wrong until proven
otherwise — and twice already the defect has instead been in the *test harness*, which is a finding
to report, not to silently patch around.

### 14.3 UI review

Serve over **HTTP** — `file://` pages cannot be inspected by the browser tooling and a passing
toolchain has hidden four real visual defects that only an HTTP review caught.

Check at **1280 desktop** and **375 mobile**:

- 9 cards · 5 modes · **Answer** mode default
- search · deep links
- no horizontal overflow · no console errors
- **no provider leakage** (no third-party host recurrence annotation on any surface)

**Kill the server explicitly**, in the same command that starts it:

```bash
python -m http.server 8731 --bind 127.0.0.1 >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null' EXIT
sleep 1
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8731/meoclass1/pastpapers/QP2401.html
kill $SRV
```

Never use `( … &)` — a detached subshell cannot be reaped, and an abandoned server on a reused port
can silently serve a **stale directory** to your next verification. That is a correctness risk, not
just a memory one.

### 14.4 Determinism

Build the paper-specific output **twice**. Require **byte identity**.

Write specs with **LF** line endings. CRLF corrupts content-hashed assets.

---

## 15. GIT HYGIENE

### Before each paper

```bash
git -c safe.directory=* fetch origin --prune
git -c safe.directory=* status          # clean tree
git -c safe.directory=* log --oneline -1 # verify you are on the §16 baseline
```

Verify: common baseline · branch name · clean tree · corpus commit · machine cleanup done.

### Commits

- **Explicit staging only.** Name every path.
- **Never `git add .`**
- **Never force push.**
- **Never commit:** source PDFs · private corpus contents · credentials · customer data ·
  temporary downloads · `__pycache__` · `node_modules` · `.vercel` · scratch output.

### After paper completion

Push the branch, then write a concise branch handover recording:

```
paper · branch · base commit · head commit · 9/9 state · donors used ·
temporal issues · corpus commit consumed · QA results · known exceptions ·
files committed · global files deliberately excluded
```

Then **stop**. Start the next allocated paper only after the previous branch is completely pushed
and its tree is clean.

Use the standard report schema in `QA_AND_HANDOVER_PROTOCOL.md` §8.

---

## 16. BASELINE — the immutable starting state

| | |
|---|---|
| **MIW baseline commit** | **`9c973596edb04db32c7bf4feb3cb5898b162662a`** (`9c97359`) on `workflow/corpus-consumer-integration` |
| **Required corpus commit** | `64977b86ed9c601e273f1d0cb55abb0461835811` (`RulesApp-Local-Input` `origin/main`) |
| **Corpus verification** | 0 ahead / 0 behind `origin/main`, tracked tree clean, at time of baseline |

**This baseline is immutable for all six papers.** If the corpus producer team lands FSS or MARPOL
work after the baseline, **do not silently move desktop branches to a new corpus commit.** Record
the commit you used. Later laptop integration enriches and reverifies where needed.

---

## 17. DESKTOP CLONE INSTRUCTION

```bash
# 1. Clone the SAME MIW repository. Do NOT copy the laptop folder.
git clone https://github.com/nickmarineengr-aiLiterate/marine-intelligence-weekly.git
cd marine-intelligence-weekly
git -c safe.directory=* fetch origin --prune

# 2. Check out the recorded baseline
git -c safe.directory=* checkout 9c973596edb04db32c7bf4feb3cb5898b162662a

# 3. Clone the private corpus SEPARATELY, alongside — never inside MIW.
git clone https://github.com/nickmarineengr-aiLiterate/RulesApp-Local-Input.git
git -c safe.directory=* -C RulesApp-Local-Input rev-parse HEAD   # must equal §16

# 4. Read this file and DESKTOP_QP_ALLOCATION_2024.md. Then start paper #1 only.
```

Set line endings to **LF** before checkout (`core.autocrlf=false`) — CRLF corrupts content-hashed
assets.

Every git command in these repositories needs `-c safe.directory=*`.

**The Founder must supply the six source PDFs out of band.** They are git-ignored by design and
your clone will not contain them.

### What is NOT deployed, and why it does not block you

The MIW Written product is **not live**. Deployment is held behind a security matter recorded in
`CURRENT_STATUS.md` and `WRITTEN_PRODUCT_LIVE_TEST_STATUS.md`. **QP authoring is unaffected** — you
are producing specs and review builds on branches, none of which is published to customers.

**Do not attempt to deploy, and do not treat deployment as a prerequisite.**

---

## 18. THE SIX-PAPER STOP GATE

When all six allocated papers are complete and pushed:

> # STOP DESKTOP PRODUCTION.

- **Do not select another paper.**
- **Do not merge to `main` or to any integration branch.**
- Hand the six pushed Founder-review branches back to the **laptop team**.

The laptop then reviews each paper one at a time — source truth, Q1–Q9, temporal decisions, corpus
use, full verification — approves or returns corrections, and only then integrates. After each
approved integration the laptop regenerates the global layer (reuse intelligence, recurrence,
reverse-hint queue, indexes, year pages, topics, `solvedQP/`, public samples, product counts) —
**one paper at a time**.

That sequencing is the whole reason for §13.2. Respect it and six parallel papers integrate
cleanly; ignore it and they collide in the derived files.

---

## 19. THINGS THAT ARE DEFERRED — do not build them

- **The verbatim regulation provision viewer.** Founder decision: deferred. Keep the consumer
  adapter and `reference_shelf` work intact; add no viewer engineering.
- **The autonomous production agent.**
- **Any change to the frozen V1 template** or the settled architecture, without test evidence of a
  defect.
- **Populating `reference_shelf`** before a real resolvable corpus object exists.
- **A purchasable BUNDLE SKU** — the bundle price is unapproved.

---

## 20. WHEN TO STOP AND ASK

Stop and report to the Founder rather than deciding alone when you meet:

- a **wrong-edition or mislabelled source**;
- a corpus defect (raise a `TRUE_SOURCE_CORRECTION_REQUEST`);
- a temporal boundary you cannot establish from primary sources;
- a donor whose two printed stems you cannot obtain;
- a validator failure you can only pass by weakening the test;
- anything that would require committing a source PDF, a credential or corpus text to this
  **public** repository.

A blocked paper reported honestly is worth more than a finished paper built on an assumption.
