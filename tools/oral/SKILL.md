---
name: miw-oral-batch-production
version: 1.0
updated: 2026-08-21
description: >
  Release-engineering workflow for the Marine Intelligence Weekly MEO Class 1 Oral
  question bank (meoclass1/QB*.html) — how an authorised batch of card edits is
  produced, validated, mutation-tested, released and handed off. Load this whenever
  Nixon mentions an Oral batch, an enrichment or follow-up batch, "E1".."E6", a batch
  manifest, a validator or mutator under tools/oral/, the release gates, the QB health
  check, or a FINAL_ORAL_* handoff. Covers process and invocation only.
  For QB CONTENT authoring (HTML structure, answer format, reg-box, CE Oral Tip) use
  the miw-qb-production skill. For manifest/index discoverability use
  docs/miw-qb-index-linkage_SKILL.md.
---

# MIW Oral — Batch Production & Release Skill v1

## 0. What this skill is, and what it is not

This is the **third member of an existing in-repo family**: `tools/notes/SKILL.md`
(Notes series), `tools/pastpapers/SKILL.md` (Solved QP), and this file (Oral QB
batches). Each lives beside the toolchain it drives.

It does **not** duplicate `miw-qb-production`, which governs what a QB card *says* and
how its HTML is shaped. This file governs how a **batch of authorised edits** gets from
an authorisation record to a pushed release without a false green.

It is deliberately thin. Implementation lives in code; this file carries workflow,
policy and invocation. If you find yourself wanting to paste a validator in here, put
the behaviour in a shared module instead.

---

## 1. TL;DR for a new session

```bash
cd /f/Marine-Intelligence-Weekly
git status --porcelain && git fetch origin --prune
git rev-parse HEAD origin/main                    # must match, tree must be clean

python tools/oral/run_oral_release.py --plan      # the exact gate sequence
python tools/oral/run_oral_release.py --full      # THE full release, one command
```

**Do not reconstruct the release suite.** It is committed. `--plan` prints the exact
sequence without executing anything; `--full` runs it. Everything below explains what
the runner does and why — it is not a script to retype.

Narrower invocations while building a batch:

```bash
python tools/oral/oral_manifest.py --quiet                 # manifest schema contract
python tools/oral/test_oral_release_infra.py               # shared-module controls
python tools/oral/test_oral_release_runner.py              # runner/registry controls
python tools/oral/run_oral_release.py --gate validate_batch_<id>
python tools/oral/run_oral_release.py --category batch --read-only
```

**Read the repository, not your memory of it.** Three separate batches were mis-planned
because a consolidation record, a coverage score or a handoff was believed over the
files. Grep before you claim.

---

## 2. The shared modules

| Module | Owns |
|---|---|
| `tools/oral/oral_bytes.py` | control-byte scanning, explicit UTF-8 I/O, the EOL normalisation contract |
| `tools/oral/oral_mutation.py` | mutation preflight (dry-run), the normalised result contract, the summary parser |
| `tools/oral/oral_manifest.py` | manifest field classification and schema assertions |
| `tools/oral/test_oral_release_infra.py` | controls for all three, plus health-check source non-vacuity |

Historical per-batch validators and mutators (`validate_batch_*.py`, `mutate_batch_*.py`)
are **release evidence**. They stay runnable and are not rewritten for elegance. New
behaviour goes in the shared modules and is enforced repo-wide from there.

---

## 3. Batch workflow

### 3.1 Derive the authorised batch
The authorisation record is the **only** source of the action set. For enrichment it is
`FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json` on
`origin/research/oral-final-enrichment-consolidation` — deliberately not on `main`,
because it is an authoring input, not a product surface.

Select the batch **through the manifest's own `authorisation_batch_key`**, never through
a hardcoded literal. Compare both of the record's independent representations
(`batches[].action_ids` and `production_actions[].batch`) and require them to agree in
order.

**The consolidation has been wrong about content in at least three batches.** Treat
`missing_limb` as *which limb*, never as *what to write*. Verify every claim against the
live card and a primary source.

### 3.2 Current-live recheck
Before authoring anything, read the live card. Actions get reduced or dropped because
the limb is already there. A "gap" carries the date of the corpus it was scored against.

### 3.3 Build the manifest
`python tools/oral/oral_manifest.py <manifest>` must pass before the batch validator is
written. Every field must be classified in `FIELD_CLASSES` as `LOAD_BEARING` or
`INFORMATIONAL`; an unclassified field fails the audit by design.

### 3.4 Validate
Write `validate_batch_<id>.py`. It must fail **closed**: if the authorisation record is
unavailable, report `unavailable` and return non-zero — never skip.

Performance is a correctness property. E6's first validator called `git show` 172 times
and took 91 seconds; the mutation suite runs it 35 times, making a 50-minute run. One
`git archive` of the tree took it to 39 seconds. A slow guard is a guard people skip.

### 3.5 Preflight the mutations — always, before the suite
```python
from oral_mutation import replace_spec, preflight_or_die
preflight_or_die(SPECS, root=REPO)     # first statement of main()
```
Reports `mutation_id / target / applied / pre_size / post_size / byte_delta`. **If any
mutation changes no bytes, the suite must not launch.** Two mutations (E5's C, E6's H)
matched nothing, wrote nothing and exercised nothing; E6 spent 22 minutes finding it.
Preflight finds it in seconds.

### 3.6 Run the suite and parse it with the shared parser
```python
from oral_mutation import parse_summary, aggregate
summary = parse_summary(log_text)      # never a hand-rolled regex
```
Fifteen harnesses print six dialects. A loose `(\d+)\s*escape` reads the **8** in
`mutations=8 escapes=0` as the escape count, and `fails=2 crash=False` donates a phantom
crash. Parse each suite separately, then `aggregate()`.

A mutation caught only because an unrelated digest changed has not proved its guard.
Record `intended_reason` and compare it to the actual failing check.

---

## 4. Release gates — run through the committed runner

**The gate list is no longer prose. `tools/oral/oral_release_gates.py` is the
authoritative registry and `tools/oral/run_oral_release.py` executes it.** Do not rebuild
a scratch runner; do not maintain a second copy of the gate list anywhere, including in
this file.

```bash
python tools/oral/run_oral_release.py --plan     # inspect the sequence
python tools/oral/run_oral_release.py --full     # 43 gates + determinism
```

**Two flags, not one.** `historical_39` is *provenance* — it records which gates were in
the suite E6 actually ran, and it is what keeps the count of 39 checkable forever.
`separate_phase` decides what the runner holds back until asked (determinism only).
Selecting on `historical_39` would silently exclude every gate added after E6.

**39 historical gates**, derived from repository evidence rather than memory. E1's handoff §17
enumerates its 37 by name (Node counted as three records); E5 reports 37 with Node
collapsed to one plus the two E5 gates; E6 reports 39 — E5 plus `validate_batch_e6` and
`batch_e6_mutate`. Adding a batch adds exactly those two gates and nothing else.
Determinism is registered separately because all three handoffs report it outside the
gate count. **Four post-E6 gates** bring a default run to 43. None is part of the
historical 39 and none is held back:

* `validate_corrections` / `corrections_mutate` — a release must never ship an
  unverified correction. Adding a *correction* adds no gates at all: both iterate every
  `correction_*_manifest.json` on disk.
* `validate_followup_register` / `followup_register_mutate` — the register pins the
  anchor and question text of 35 parent cards, and its validator reads the **live**
  corpus. So a release that moves or rewords one of those cards turns this gate red at
  the moment the drift happens, instead of months later when a follow-up batch tries to
  author against a parent that no longer says what was recorded. It guards no shipped
  bytes; it is a standing target-drift detector.

The post-E6 set is **enumerated by name** in `test_oral_release_runner.py`
(`POST_E6_GATES`), and the expected totals are derived from that list. Registering a new
gate therefore means editing one reviewable line — and a hardcoded total can never
expire out from under the control.

The runner owns these behaviours so no future session has to remember them:

- **Node gets explicit files.** The glob is expanded in Python and never reaches a
  shell. Node 24 resolves `--test <dir>` as a module and fails with `Cannot find module`
  — E5's runner did exactly that and the gate exited 1 in 0.4s.
- **`check_determinism.py` is invoked bare.** It has no argv parser, so `--help` would
  *run the whole chain*. Seeds `0 / 1 / 524287` are hardcoded inside it.
- **Serial ownership** is enforced structurally: one gate at a time, and the runner
  raises if a mutating gate has not released the worktree.
- **Restore is from the runner's own byte snapshot, by exact path.** It never runs
  `git checkout -- .`, `git restore .`, or any blanket reset — and never restores from
  git at all, because `git checkout <ref> -- <file>` destroys uncommitted branch edits.
  It snapshots `VALIDATION_RESULTS.json`, `PHASE2_VALIDATION_RESULTS.json` and
  `ORAL_NOTES_IMPACT.md`, restores them, and verifies the restore.
- **Health compares LOCAL against a clean ref** — never remote main against itself —
  as multisets, after normalising the transport.
- **Audit is semantic.** `validate_audit.py` exits **0** while reporting
  `passed 12 / failed 1`. The runner derives the baseline by running the same tool in a
  temporary detached worktree of `origin/main` and classifies `PASS`,
  `PRE_EXISTING_BASELINE`, `FAIL_CURRENT` or `UNAVAILABLE`. The baseline is never
  hardcoded — a hardcoded baseline silently absorbs the next real regression.
- **Validator summaries have five dialects** and in `107 PASS / 0 FAIL` the leading
  number is *passes*, not a total. Only the second number is trusted.
- **A `FAIL:` line inside a mutator log is caught-evidence, not a failure.** Only the
  harness summary line carries the verdict, and it is read by the shared parser.

Every historical guard runs on every release. `PROPOSED_OPTIMISATIONS` in the registry
records a runtime saving and the reason it has **not** been applied: guard expiry is a
confirmed defect class here, and a historical mutator is exactly what detects it.

---

## 5. Health checks — read this before citing one as evidence

`meoclass1/qb_health_check.py` scans **remote `main` by default**, because that is what
the daily GitHub Action needs. Since 21 August 2026 it takes an explicit source:

```bash
python meoclass1/qb_health_check.py --source local --no-email          # PRE-merge
python meoclass1/qb_health_check.py --source ref --ref origin/main --no-email
python meoclass1/qb_health_check.py                                    # remote, as CI runs it
```

Every run prints `source_type`, `source`, `commit`, `files` and `findings`, so a result
cannot be misread. `--json PATH` writes the same machine-readably.

### The evidence contract
* **PRE-MERGE:** compare `--source local` (the branch, uncommitted edits included)
  against `--source ref --ref origin/main` (a clean baseline). Compare finding **sets**,
  not counts — there are ~369 standing findings, which is why the tool exits 0 on
  findings unless you pass `--fail-on-findings`.
* **POST-PUSH:** a remote-main run is an optional confirmation. It is **not** a
  substitute for local pre-merge regression detection.

### Historical health evidence is not load-bearing
Before this change the checker had one source: it downloaded a tarball of remote `main`
and never read local disk. Several handoffs recorded *"N findings on the branch and N on
a clean origin/main — 0 new, 0 gone"* as **pre-merge** proof. Both runs read the same
remote `main`; neither could see the change under test. E6 proved it by corrupting five
`q-card` tags in a clean tree and getting a byte-identical finding set.

**The underlying releases are not thereby defective** — the validators, mutation suites,
digests and determinism gates did the real work. Only that specific comparison was
vacuous, and it should not be cited as proof of local branch health.

`test_oral_release_infra.py` section 6 pins the fix: a scratch git repo with an
uncommitted corruption, where local mode must see it and ref mode must not.

---

## 6. Traps that have fired more than once

| Trap | Rule |
|---|---|
| **Backslashes through a heredoc** | Author anything containing a backslash with a **file writer**, never a shell heredoc. E1 lost `\b` to 0x08, E5 lost `\1` to 0x01, and E6's handoff reproduced *both bytes* in the sentence describing them. Scan prose artefacts too: `python tools/oral/oral_bytes.py <paths>`. |
| **Working-copy CRLF vs LF blob** | `.gitattributes` pins `*.html text eol=lf`. A freshly written file may hold CRLF until the next checkout normalises it. Normalise before comparing text; keep exact bytes only where the digest is the subject. **Never pin working-copy EOL in a manifest** — see debt item 1. |
| **Windows path separators** | `glob` returns backslashes; `git show origin/main:meoclass1\QB1_A.html` fails for every file, every baseline loads empty, and the whole corpus reads as new. A baseline that silently fails to load reports catastrophe rather than breakage. |
| **cp1252 decoding** | Always `encoding="utf-8"`. `subprocess(text=True)` once manufactured 450 false diffs. |
| **Counting `.q-card` divs** | Gives 723 against a canonical 721. Use the canonical extractor. |
| **Guards that expire** | A guard pinning "the corpus total is 721" or "batches A–D digests" passes vacuously on the next batch. This has happened at least four times. Pin identities, not totals. |
| **Reading the wrong exit code** | `cmd \| tail; echo $?` reports `tail`'s status. Use `${PIPESTATUS[0]}`. |
| **Fixtures harvested from live state** | A self-test that reads the live corpus stops testing anything the moment the corpus changes. Build the fixture. |
| **`process.exit()` after a fetch** | Crashes libuv on Windows (0xC0000409). |

---

## 7. Follow-up production mode

### 7.1 Production starts from the committed register — never from prose

**`tools/oral/oral_followup_register.json` is the source of truth for all 35 follow-up
actions `FUP-001`..`FUP-035`.** A new session must **not** reconstruct them from a
handoff, a reconciliation record or chat memory. Read the register.

```bash
python tools/oral/build_followup_register.py --check   # is it current?
python tools/oral/validate_followup_register.py        # 32 checks
python tools/oral/mutate_followup_register.py          # 12 mutations
```

The register is **generated**, not hand-written. `build_followup_register.py` re-derives
it from three sources pinned by **blob SHA** (branches move; blobs do not), regroups the
39 follow-up source families by parent card, re-derives the `FUP-NNN` identifiers and
refuses to write if they disagree with the committed ones. Never hand-edit the JSON —
`register_is_byte_current_with_its_generator` fails immediately, and every mutation in
the suite has to trip its *own* named check to count as caught, precisely so that
byte-currency check cannot be the only thing holding the guard up.

**Register ≠ batch manifest.** The register says what is **authorised**; a
`batch_f*_manifest.json` says what a run **implemented**. Do not collapse them — the
register names 35 parent cards it has never edited, so admitting it to
`authorisation_manifest_paths()` would exempt all 35 from every historical guard.
`test_oral_release_infra.py` pins that separation.

### 7.2 A confirmed disposition is not a confirmed target

All 39 source families are `LAPTOP_CONFIRMED`. That confirms the **disposition**
(this is a follow-up, not a card), and nothing about the parent it points at.

**Only 4 of 39 had their parent card chosen by hand.** The other 35 carry
`decision_basis: "rule: material partial dispositioned by recurrence"`, and their
`decision_target` is literally `current_best_answer_question_id` — an IDF coverage
score. That is why several look like weak topical matches: the score picked the card,
not a person. Two have since **drifted** — the score no longer selects the target it
assigned.

So every action carries `target_confidence` (HIGH / MEDIUM / LOW) and
`target_review_status`:

| status | meaning |
|---|---|
| `CONFIRMED` | hand-adjudicated parent; produce against it |
| `REQUIRES_LIVE_ADJUDICATION` | score-chosen; read the live answer body first |
| `RETARGET_REQUIRED` | the score no longer selects this parent; re-home it |
| `METADATA_ONLY_CANDIDATE` | the source says it is *not an answer* — likely a trap |

`currentness_required` is a **floor, not a ceiling**: it is derived by conservative
pattern match over the candidate's ask, so a perishable fact with no date word in it
will not be flagged. The batch confirms currentness; the register only pre-warns.

`verification_class` is `UNCLASSIFIED_PENDING_BATCH_SCOPING` for all 35 — the source
records carry an empty `technical_verification_scope` for every follow-up family, so
assigning a governed class in the register would have been invention. The producing
batch assigns the real class.

### 7.3 The workflow

```
follow-up register  (committed, validated)
  -> select a bounded batch          (by target_review_status, not by id order)
  -> current-live target adjudication
  -> authority / currentness review
  -> bounded product edit
  -> relationship metadata
  -> batch production manifest (oral_manifest.py)
  -> validator (fails closed)
  -> mutation preflight
  -> mutation suite (parse with the shared parser)
  -> full release gates
  -> handoff
```

**Relationship metadata.** The register already records the directed edge
`parent_question -> EXAMINER_FOLLOW_UP -> answer_home`, so a later examiner simulator
can walk it. Carry it into the batch manifest unchanged. Do **not** build a Study Engine
now; just do not re-represent the relationship in a way that would need re-authoring.

`creates_new_cards` may be **true** for a follow-up batch. Do not assume the
enrichment-only invariant of "0 cards added"; assert whatever the manifest declares.
Every action in the register is currently `creates_new_card: false`, and the validator
enforces that against an explicitly empty exception list.

**Colocation.** Nine follow-ups land on a card a shipped enrichment already edited
(`colocated_enrichment_actions`). Read the live card before adding a limb — the
enrichment may already have said it. `FUP-034` is the known case: `QB9_G#q3`, already
touched by E6's `A046`. Keep `FUP-034`/`FUP-035` out of the first batch.

---

### 7.4 Registering a follow-up batch — what F1 had to change

A follow-up batch is an ordinary batch on the release surface, but it is the
first thing to be added *after* the historical 39 were fixed, so two counters
had to stop being hardcoded:

* `_batch_pair()` takes `historical_39` and a post-E6 batch **must** pass
  `False`. Defaulting True is right for every batch that existed when the count
  was fixed and wrong for every batch after it.
* Its two gate ids go in `POST_E6_GATES` and, for the mutator,
  `POST_E6_MUTATION_SUITES` in `test_oral_release_runner.py`. The totals derive
  from those lists, so this is one reviewable line each.
* `test_oral_release_infra.py` asserted `len(manifests) == 11`. **F1 turned that
  red simply by existing** — guard-expiry inverted. It is now the enumerated
  `EXPECTED_BATCH_MANIFESTS`, matched both ways.

A batch may also HOLD an action it was authorised to produce. **Record the hold
as structure, never as prose:** `held_actions` is `LOAD_BEARING` in
`FIELD_CLASSES` and asserted by `audit_manifest`, and carries the id, a governed
`HELD_STATUSES` value, the target, the blocker, the empirical proof and
`work_still_owed`. A held action has no `cards[]` entry, so without that record
"we were never asked to do it" is indistinguishable from "we held it and said
so". `HELD_GOVERNANCE` is **not** `REJECTED`, `RETARGET_REQUIRED` or
`ALREADY_COVERED` — those erase the fact that the work is still owed.

**A held action must be as guarded as an implemented one.** Six mutations exist
only for it: edit its parent card, drop its declaration, restate it as a
rejection, mark the work no longer owed, strip its proof, point it at the wrong
target — and one more edits the **register** to say the action was produced,
because the register is an authorisation record, not a status board, and
disguising a hold there would hide outstanding work from every future session.

### 7.4a A non-green validator can make its mutator unrunnable

`mutate_batch_e6.py` aborts with **exit 2** unless its control validator is
green, which is correct — mutating against an already-failing validator proves
nothing. But `validate_batch_e6` is permanently non-green from the line-ending
evidence debt, so **the E6 mutator can never run**, the runner reports
`UNAVAILABLE`, and `UNAVAILABLE` is release-critical: a default `--full` run
stops at gate 28 of 46 and never reaches health, audit, determinism or any later
batch.

Two lessons. First, **classifying a validator as `PRE_EXISTING_BASELINE` does
not neutralise its debt** — trace the dependents, because a mutator gated on
that validator fails harder than the validator did. Second, a gate that has not
run since the debt appeared is not evidence of anything; use `--keep-going` to
get the remaining gates and report the blocker separately, rather than quietly
treating a truncated run as a pass.

### 7.5 The post-pin gap — why 8 follow-ups cannot be produced yet

**Anchor-level delegation does not cover a digest pin.** Every generation-2
validator pins its own cards with `digest16(live) == post_edit_digest`, and that
check has **no delegation path in any of the eleven batch validators** — unlike
`only_authorised_cards_changed` immediately above it, which does.

So a follow-up landing on a card a shipped enrichment already edited turns that
enrichment's validator red. Proved on `QB1_A#q9`: a scratch insert took
`validate_batch_e1.py` to *25 checks, 1 FAIL*, failing exactly
`manifest_digests_match ['QB1_A.html#q9 post']` and nothing else.

This blocks the **8 colocated actions** — FUP-003, 006, 008, 009, 013, 017, 025,
034. Do not schedule them until a **post-pin supersession contract** exists:
a later manifest declares `supersedes_post_pins`, the earlier validator consults
it, and it holds only when the superseding record's own pin matches live — so
the live state stays pinned by exactly one record. Build it in
`oral_manifest.py`, the single shared surface, and prove non-vacuity both ways.

Until then a colocated follow-up has exactly two wrong options — ship a red
historical guard, or rebaseline a historical manifest — so the governed answer
is to **hold the action**, as F1 held FUP-006.

## 8. Sibling-manifest delegation

A later authorised change must be accepted by an older batch's guard, through explicit
delegation to the later manifest. The delegation must be **non-vacuous**: without the
later manifest the older guard fails; with it, it passes. Verify both directions when
you add one — a delegation that passes when the manifest is absent is not a delegation.

Every batch validator reads that surface through **one** function,
`oral_manifest.authorisation_manifest_paths()`. Do not re-add a local glob: ten copies
of the same glob is how the two record families drifted apart in the first place.

### 8.1 Two record families

| Family | Filename | Authorises |
|---|---|---|
| Batch | `batch_*_manifest.json` | cards a production or enrichment run created / enriched |
| Correction | `correction_*_manifest.json` | cards repaired **after** a batch shipped |

A batch closes when it publishes and its digests are release evidence — so a
post-release repair is **never** back-dated into a batch it did not belong to.

### 8.2 Post-release corrections carry a manifest — always

**A product correction made outside a production batch is not finished until it has an
authorised correction manifest.** Without one, every historical guard that owns the
corrected card reads it as undeclared drift and goes red — correctly. This is not
theoretical: the fair-treatment candidate correction turned **7 of 11** batch validators
red until `CORR-FAIR-TREATMENT-20260821` was written.

The full loop is owned by the correction workflow skill
(`Claude skill/miw-correction-workflow_SKILL.md`, §7a). Do not duplicate it here.

Delegation is **anchor-level**, which on its own would exempt a corrected card forever.
So a correction also **pins** each card's post-correction digest, and
`validate_corrections.py` compares those pins to the live pages:

| Question | Answered by |
|---|---|
| "was this card legitimately edited?" | the batch validators, via delegation |
| "and is it still exactly what was authorised?" | `validate_corrections.py`, via the pin |

Neither subsumes the other. Run both:

```bash
python tools/oral/validate_corrections.py
python tools/oral/mutate_corrections.py
```

---

## 9. Shared targets

Several action identities may share one canonical card (E1: `A007+A008` on `QB9_H#q9`;
E5: `A036+A037` on `QB4_C#q6`). One post-edit digest then serves several action records,
while each authorised limb stays independently testable.

Two declaration dialects are both valid and both accepted by `oral_manifest.py`:
per-card `shared_target_note` (E1) and top-level `shared_target` (E5, E6). A shared
target that is declared **neither** way fails the audit.

---

## 10. End-of-batch: the lesson-to-skill review

After every major batch or release, ask explicitly:

> **Did this session discover a reusable operational lesson?**

If yes, classify it and put it in exactly one place:

| Class | Home |
|---|---|
| **CODE** | a shared module, with a control in `test_oral_release_infra.py` |
| **SKILL** | this file — workflow, policy, invocation |
| **DOC** | the batch handoff (`FINAL_ORAL_*.md`) |
| **DEBT** | the handoff's debt section, capped at 5 |

Prefer CODE. **Reading a lesson is not the same as encoding it** — E5 documented the
parser ordering constraint in prose and E6 reproduced the bug anyway. A lesson that
lives only in prose will be relearned.

Do not persist a lesson that is specific to one batch's content.

---

## 11. Standing debt (tooling)

1. **`file_line_endings` in the E6 manifest is not reproducible.** It records `CRLF` for
   `QB4_I.html` and `QB9_G.html`, but `.gitattributes` pins `*.html text eol=lf` and both
   blobs are LF. The value captured a pre-normalisation working copy, so
   `validate_batch_e6.py`'s `line_endings_homogeneous_per_file` check now fails on a
   clean checkout of the very commit it certified. Product bytes are correct; the pin is
   the defect. Future manifests should not pin working-copy EOL.

   **The runner now classifies this, and never as PASS.** `validate_batch_e6` is marked
   `baseline_derivable`, so on failure the runner re-runs that same validator on a clean
   worktree of `origin/main` and compares **failing check names**. Live failures that are
   a subset of the baseline's report as **`PRE_EXISTING_BASELINE`** — its own status,
   which does not block the release and is not green — with `baseline_fixed` naming any
   check the run repaired. A *new* failing check is not a subset and still FAILs.

   The baseline is derived, never declared, for the reason `classify_audit` already
   gives: a hardcoded baseline silently absorbs the next real regression.

   **Derived worktrees need a scoped `safe.directory`.** `F:` does not record filesystem
   ownership, so git refuses to operate in a directory that is not on the allowlist. The
   main clone is on it; a fresh temporary worktree never is. Without the exception every
   git call inside the derived tree dies with *dubious ownership*, and a validator that
   reads its evidence through `git show` reports that evidence as **unavailable** — so
   the "baseline" describes the sandbox, not the commit. This silently affected
   `derive_audit_baseline` too. `run_oral_release.worktree_env()` injects the exception
   for exactly the one worktree path, and passes it to the child process.
2. **`authorisation_source` is unread by every batch validator.** It duplicates a
   hardcoded constant. It is now asserted to *resolve* by `oral_manifest.py`, so it is no
   longer decoration, but no validator selects through it.
3. **`index_tier_literals_valid`** fails in `validate_audit.py` on a clean `origin/main`
   (43 invalid literals). Pre-existing baseline, carried since E1.
4. **Stale counters** in `VALIDATION_RESULTS.json` / `PHASE2_VALIDATION_RESULTS.json`
   (`live_questions` 688 vs 721, `headings` 954 vs 960).
5. ~~RELEASE-BLOCKING — 7 of the 11 batch validators are red from an unmanifested
   candidate correction.~~ **Closed 21 August 2026** — declared as
   `CORR-FAIR-TREATMENT-20260821` (§8.2). The batch sweep went **4 PASS / 7 FAIL →
   10 PASS / 1 FAIL**; no guard was weakened and no batch was rebaselined. The single
   remaining failure is item 1, which is unrelated to the correction.

6. ~~No committed release runner.~~ **Closed 21 August 2026** —
   `tools/oral/run_oral_release.py` + `oral_release_gates.py`.

---

## 12. Product invariants (assert, never assume)

| Invariant | Value |
|---|---|
| Canonical Oral questions | **721** |
| Question-bearing files | **86** |
| Examiner relationships / examiners | **960 / 7** |
| Price | **₹1,499, one year** |

A batch that changes any of these without saying so in its manifest is a stop condition.
