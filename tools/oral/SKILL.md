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
| `tools/oral/oral_mutation.py` | mutation preflight (dry-run), the normalised result contract, the summary parser, the derived-worktree baseline and the baseline-aware control precondition (§7.4a) |
| `tools/oral/oral_manifest.py` | manifest field classification and schema assertions |
| `tools/oral/oral_supersession.py` | historical digest supersession — does a later authorised card state validly descend from an earlier pin? (§7.5) |
| `tools/oral/test_oral_release_infra.py` | controls for the byte/mutation/manifest modules, plus health-check source non-vacuity |
| `tools/oral/test_oral_supersession.py` | the chain algebra, then the same contract through the real E1 and F1 validators |

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
| **YOUR OWN WRITER CREATES THE CRLF** | On Windows, `pathlib.write_text()` / `open(..., 'w')` translate `\n` to `\r\n`. Every product file written that way in H2 flipped to CRLF, `validate_examiner_index` went red on *SQ home is LF-only*, and **E1–E5 went red with it** through their transitive `examiner_relationship_delta_zero` gate — nine reds from one writer. **Digests were unaffected**, because `card_digests` normalises, which is exactly why it stayed invisible until the full sweep. Write product files as `p.write_bytes(s.encode('utf-8').replace(b'\r\n', b'\n'))`, and audit EOL across every file you touched before running the suite. |
| **Windows path separators** | `glob` returns backslashes; `git show origin/main:meoclass1\QB1_A.html` fails for every file, every baseline loads empty, and the whole corpus reads as new. A baseline that silently fails to load reports catastrophe rather than breakage. |
| **cp1252 decoding** | Always `encoding="utf-8"`. `subprocess(text=True)` once manufactured 450 false diffs. |
| **Counting `.q-card` divs** | Gives 723 against a canonical 721. Use the canonical extractor. |
| **Guards that expire** | A guard pinning "the corpus total is 721" or "batches A–D digests" passes vacuously on the next batch. This has happened at least four times. Pin identities, not totals. |
| **Reading the wrong exit code** | `cmd \| tail; echo $?` reports `tail`'s status. Use `${PIPESTATUS[0]}`. |
| **`validate_corrections.py` is not the manifest auditor** | They audit different things. `validate_corrections.py` checks CORRECTION records against the live corpus; **`python tools/oral/oral_manifest.py` with no arguments audits every manifest on disk, batch and correction alike** (417 checks). H1 ran the first and not the second and shipped a batch manifest that was red on two counts. Run the bare auditor before every ship — it is one command and it covers records you are not thinking about. |
| **Fixtures harvested from live state** | A self-test that reads the live corpus stops testing anything the moment the corpus changes. Build the fixture — or, where the point is to drive the shipped validator, DERIVE its inputs (§7.5b). |
| **A killed mutating gate leaves product bytes** | `test_oral_supersession.py` and every `mutate_batch_*.py` restore in a `finally:`, which does **not** run when the process is killed by a timeout. Run them through `run_oral_release.py`, which owns a byte snapshot and an exact-path restore. Invoked bare and killed at 2 minutes, the supersession control left `QB1_A.html` mutated on disk and `validate_batch_e1.py` red — a "failure" that was purely the leftover. Check `git status` before believing a validator that suddenly went red. |
| **Never run two gates concurrently** | The runner enforces serial ownership for a reason. A validator run while a mutating control was live in the background read a transiently-probed `QB3_I.html` and reported a card as changed that was byte-identical to `HEAD`. |
| **`process.exit()` after a fetch** | Crashes libuv on Windows (0xC0000409). |
| **A currency check that cannot find the next edition** | Asking *"does X supersede Y?"* answers **yes**, truthfully, and is structurally blind to a later edition of X. The card shipped teaching a first edition that was already a year stale. Ask the publisher-anchored form instead — *"what has the authoritative publisher said MOST RECENTLY about this subject?"* — and record the answer in the source registry (§8.2b). |

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

### 7.4a Mutation controls compare against a BASELINE, not against zero

A mutation suite proves a **validator** catches corruption, so its control state
must carry no failure the mutations did not cause. That is **not** the same as
carrying no failure at all, and spelling it that way cost the E6 suite its
ability to run.

`validate_batch_e6` is permanently non-green from the line-ending evidence debt
(§11.1). Every E-series harness demanded an absolutely green control:

```python
code, failed = run_validator()
if code != 0:
    return 2            # <- unrunnable forever, once any debt exists
```

so `batch_e6_mutate` exited 2, the runner reported `UNAVAILABLE`, and
`UNAVAILABLE` is release-critical — a default `--full` run stopped at gate 28 of
46 and never reached health, audit, determinism or any later batch. **A guard
that cannot run has silently expired**, which is a confirmed defect class here.

**The rule.** The precondition is *no NEW failures*, never *no failures*:

```
baseline = the validator's failing checks on BASELINE_REF, clean worktree
control  = the validator's failing checks on the current worktree
runnable iff  control ⊆ baseline
```

Four properties that are not optional:

* **Identity, never count.** baseline `{A}` vs control `{B}` is the same size
  and is a regression. baseline `{A,B}` vs control `{A}` is strictly fewer and
  is an improvement. Counting gets the first case wrong.
* **Derived, never declared.** A hardcoded list of "known failures" absorbs the
  next real regression the moment someone forgets to prune it — the same reason
  `classify_audit` derives its baseline.
* **Derived only when needed.** A green control skips the derivation entirely,
  so the eleven clean validators cost exactly what they always did.
* **Fail closed.** An underivable baseline is *not* permission to run.

Once a control legitimately carries a failure the validator never exits 0, so
`code == 0` also stops working as the per-mutation escape test — every mutation
would read as caught. `oral_mutation.mutation_verdict()` asks instead whether a
**new** failing check appeared and whether it is the intended one. With an empty
baseline that is byte-for-byte the original semantics.

Shared implementation, used by every harness and by the runner's own gate
baselines: `oral_mutation.require_control_baseline()`,
`derive_validator_baseline()`, `mutation_verdict()`. Do not re-derive a baseline
locally — a runner and a mutator that computed "the baseline" two different ways
could disagree about what the baseline *is*, which is the ambiguity a derived
baseline exists to remove.

### 7.5 Historical digest supersession — a pin descends, it never expires

**Anchor-level delegation does not cover a digest pin.** Every generation-2
validator pins its cards with `digest16(live) == post_edit_digest`. That check
had **no delegation path in any of the eleven batch validators** — unlike
`only_authorised_cards_changed` immediately above it, which does — so a
follow-up landing on an already-enriched card turned that enrichment's validator
red. Proved on `QB1_A#q9`: a scratch insert took `validate_batch_e1.py` to
*25 checks, 1 FAIL*, failing exactly `manifest_digests_match` and nothing else.

That blocked **8 colocated actions** (FUP-003, 006, 008, 009, 013, 017, 025,
034) behind two wrong options: ship a red historical guard, or rebaseline a
historical manifest.

**The contract, in one line: do not make old evidence disappear — make new
authorised states descend from it.**

The historical pin is never rewritten. The LATER record declares, per card,
which earlier pinned state it descends from:

```json
"pre_edit_digest":  "a1deaf3445bc1c88",
"post_edit_digest": "<new state>",
"supersedes": {
  "manifest": "batch_e1_enrichment_manifest.json",
  "action_id": "ENRICH-A003",
  "post_edit_digest": "a1deaf3445bc1c88"
}
```

and the earlier validator's claim becomes strictly **stronger**: not "my state
is live" but "my state is the ancestor of what is live". `H1 → H2 → H3` is
provable to any depth; an unmanifested `Hx` still fails.

`oral_supersession.resolve_authorised_card_state()` is the single
implementation. Every validator that pins a live post-edit digest calls it, and
folds the result into its existing digest check — **no validator gained a check,
so no check count moved.**

Rules a successor must obey, all enforced, all fail-closed:

| Requirement | Failure status |
|---|---|
| the predecessor still pins what you say it pins | `PREDECESSOR_PIN_ALTERED` |
| your `pre_edit_digest` == the predecessor's `post_edit_digest` | `CHAIN_BREAK` |
| the terminal state is the live card | `TERMINAL_NOT_LIVE` |
| the predecessor exists | `ORPHAN_SUCCESSOR` |
| the predecessor owns the SAME card | `WRONG_CARD` |
| one successor per predecessor | `CHAIN_FORK` |
| no cycles, one root, one terminal | `CHAIN_CYCLE` / `AMBIGUOUS_*` |
| same digest convention throughout the chain | `DIGEST_CONVENTION_MISMATCH` |

Three things to know before you write one:

* **Dormant by default.** A target with no `supersedes` anywhere resolves by the
  original `pin == live` comparison and builds no chain. That is why adopting
  this changed nothing for the ten manifests already on main.
* **Conventions are not interchangeable.** Three coexist: `sha256(text)[:16]`
  (E1–E5, F1), full `sha256(text)` (E6), and full `sha256` of a balanced-tag
  block (corrections). A chain must stay in the ROOT's convention — if you
  supersede an E1 pin you record that card the way E1 records it. Mixed widths
  are reported as their own failure rather than compared as strings.
* **This is NOT the `authorised elsewhere` mechanism, and does not replace it.**
  `authorisation_manifest_paths()` answers *"is this later edit authorised?"*;
  the chain answers *"does the later authorised state validly descend from my
  pinned state?"*. Both are required. Ownership delegation alone would exempt a
  card forever; the chain alone would not know the successor was allowed to
  exist.

Controls: `tools/oral/test_oral_supersession.py` — the algebra in memory, then
the same contract driven through the real E1 and F1 validators against the live
corpus, with every card restored byte-exactly.

### 7.5a Discharging a hold — `discharges_hold`

**Batch F1b, 22 August 2026, is the first production chain on main:**
`batch_e1_enrichment_manifest.json/ENRICH-A003` (`a1deaf3445bc1c88`) →
`batch_f1b_manifest.json/FUP-006` (`46defd301a1f56a3`), which is live. E1 stayed
at 25 checks / 0 FAIL throughout and was neither rebaselined nor relaxed.

A hold is closed by the batch that does the work, **never** by editing the batch
that declared it. `discharges_hold` is the mirror of `held_actions` and is
`LOAD_BEARING`, asserted by `audit_manifest`:

| Assertion | Prevents |
|---|---|
| `discharged_holds_well_formed` | a discharge with no id, holder or reason |
| `discharged_holds_are_actually_produced` | claiming a discharge the batch never implemented |
| `discharged_holds_name_a_real_hold` | pointing at a manifest that never held it — or whose hold has since been deleted |

So F1's manifest still says FUP-006 was `HELD_GOVERNANCE` with
`work_still_owed: true`, permanently and truthfully, because that is what F1
did. "Is it still owed?" is answered by **searching for a discharge**, not by
arithmetic over handoffs. `validate_batch_f1b.py` asserts both halves, and its
mutations O, P, Q and R attack the history rather than the product — laundering
a hold is invisible to every digest check in the toolchain.

### 7.5b A guard expires in BOTH directions

Guard expiry is a confirmed defect class here, and F1b hit it twice in one
session — once in each direction. Both were caused by a *legitimate* change.

* **Starts failing.** `validate_batch_f1.py`'s `held_action_target_untouched`
  asserted the held card was byte-unchanged. Correct while held; wrong the
  instant the hold was discharged.
* **Keeps passing while meaning nothing.** `test_oral_supersession.py` asserted
  *"no supersession is declared on main today"* — true on the day the mechanism
  landed, and guaranteed to go stale the first time it was used. This is the
  more dangerous shape: nothing goes red, the guard just stops describing the
  repository.

**The rule: make the check change SUBJECT, do not stand it down, and never
special-case the action that exposed it.**

```
no discharge declared -> the held card must be UNCHANGED        (original semantics)
discharge declared    -> the held card must be exactly the state
                         the discharging record PINNED
```

Non-vacuous under both regimes, and an arbitrary edit fails it either way —
proved by F1's mutation C, which still trips the same named check. Likewise the
chain audit now asserts *every declared chain resolves* instead of *no chain
exists*: silent when there are none, stronger when there are.

**A live fixture must DERIVE its predecessor, never hardcode one.**
`test_oral_supersession.py` pinned `ENRICH-A003 / a1deaf3445bc1c88` as the state
its scratch successor descended from. F1b legitimately appended a state, so the
scratch became a second successor to one predecessor — reported as `CHAIN_FORK`,
which reads as a broken contract when the only stale thing was the fixture.
`terminal_state_for()` now asks the resolver where the chain currently ends. The
suite went **48 checks → 55**, because the FUP-006 case stopped returning early
and now proves the contract at depth three.

Two smaller traps from the same session, both worth knowing:

* **A resolver failure changes shape once a chain exists.** The same probe that
  reported `PIN_MISMATCH` reports `TERMINAL_NOT_LIVE` once a successor is
  declared. A parser that reads only the first shape silently returns `None`.
* **Registering a batch touches four files, not one:** the gate pair in
  `oral_release_gates.py` (with `historical_39=False`), `POST_E6_GATES` and
  `POST_E6_MUTATION_SUITES` in `test_oral_release_runner.py`, and
  `EXPECTED_BATCH_MANIFESTS` in `test_oral_release_infra.py`. Miss the last and
  the new manifest turns an unrelated control red simply by existing.

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

### 8.2a A digest pin cannot tell you the content is right

Both gates above answer *"are these bytes the ones we authorised?"*. Neither
answers *"is what we authorised actually correct?"* — a pin is perfectly happy
with wrong text, because it pins whatever it is given.

That gap is invisible until a correction turns on a **regulatory proposition** a
later well-meaning edit could quietly drop. `CORR-LSA-LIFEBOAT-VENTILATION-20260822`
is the first that did: MSC.535(107) defines *installed on or after 1 January 2029*
in two limbs, and the card had kept only the newbuilding limb — which does not
blur the rule, it **inverts** it for the whole in-service fleet. Restoring the
missing limb and pinning the result would have left nothing asserting that the
limb must stay.

So a correction of that kind also gets **content gates**, named per correction,
exactly as a production batch gets `validate_batch_<id>`:

```bash
python tools/oral/validate_correction_lsavent.py
python tools/oral/mutate_correction_lsavent.py
```

Two rules learned building the first one:

1. **Every mutation's required check must be a content check, never the digest
   pin.** Any edit to the card trips the pin, so accepting it as the catch would
   prove only that the pin works while the substantive checks rot as dead code.
2. **A correction quotes the wording it rejects**, so a flat banned-phrase grep
   fails on the very sentences carrying the fix — the same reason this entry is
   `GREP: SKIP` in the trap register. Assert that each mention is *negated or
   quoted*, not that it is absent. Run the negation window wide: the tightest
   real case put the denial behind two full quoted phrases.

Naming a correction in the **delegation** path is still bypassing the model.
Naming one in a **content** gate is not — see the MAINTENANCE note in
`oral_release_gates.py`.

---

### 8.2b Currency: ask what the publisher said LAST, not whether a known supersession happened

`CORR-BMP-MS-CURRENCY-20260831` was **rejected by independent review on its first
round**, and the reason is a process defect worth more than the card was.

Five live cards taught **BMP5** as the current maritime-security guidance. The
currency record built to check them asked exactly one question:

> *does BMP MS supersede BMP5?*

It answers **yes**. It is **true**. And it is **structurally incapable** of
returning the fact that mattered: BMP MS had itself moved to a **2026 second
edition**. A question shaped as *"did the supersession I already suspect exist?"*
can only ever confirm or deny the supersession you named. It cannot see one you
did not.

**The question that finds it** is anchored on the publisher, not on the pair:

> *what has the authoritative publisher said MOST RECENTLY about this subject?*

Rules this produced, all now enforced in
`docs/sources/MIW_SOURCE_REGISTRY.json`:

1. **`SEARCH ONCE → VERIFY → PRESERVE → REUSE → REVALIDATE WHEN DUE`.** A primary
   source that cost a verification pass is registered, not re-found. The registry
   is the reuse surface; a second answer on the same subject starts there.
2. **Every registered source carries a currentness STATE**, not a date alone —
   `CURRENT_VERIFIED`, `HISTORICAL_SUPERSEDED`, `ACCESS_LIMITED`,
   `CURRENTNESS_UNVERIFIED` — plus the trigger that makes it due for
   revalidation. `CURRENTNESS_UNVERIFIED` is a legitimate, shippable state; a
   silently assumed `CURRENT` is not.
3. **A source cited candidate-facing with a date must be registered.** Round 2
   caught MISTO quoted with a date and no registry row; it is now
   `SRC-MISTO-2025-11`.
4. **An access limit is stated, never worked around and never hidden.** The BMP MS
   bytes sit behind an HTTP 403 that was **not** defeated. The card therefore
   asserts **no** chapter, page or phase structure, and says so to the candidate
   in its source-confidence line. Registered `ACCESS_LIMITED`, with the
   co-publisher releases carrying whatever the card does claim.

The wider shape, and why this sits beside §8.2a: a digest pin cannot tell you the
content is right, and a **content** gate cannot tell you the content is still
current. Correctness and currency fail independently, and only a source with a
state and a revalidation trigger catches the second.

---

### 8.2c A source is not one voice — read the status chapter, and ask the issuer's index

§8.2b is about asking the right *question* of an issuer. This is about what to do when the
issuer's own answer is not single. Both H2 blocking defects were this, and neither was a
research failure — the correct text was in a document already held.

**A long document contradicts itself, and the narrative chapter is the one that lies.**
DGMA's decarbonisation framework says, in its narrative chapter, that the Green Tug Transition
Programme began *"with pilot deployments at JNPT and Kochi"*. Its **deployment-status** chapter
says Phase 1 is Deendayal, JNPA, Paradip and V.O. Chidambaranar, work orders placed at all four,
and Cochin waiting until its diesel tug contract expires in 2027. A card was written from the
narrative chapter and then turned that error into *advice* — it told a Kochi MMD candidate to
volunteer "Kochi as a GTTP pilot port" as one of three memorised facts, in front of the one panel
certain to know better.

> **Rule.** In any policy, framework or programme document, find the section that reports **what
> has actually been deployed, tendered, awarded or commissioned**, and prefer it over any
> narrative, executive-summary or context passage. Narrative chapters are written to motivate;
> status chapters are written to account. When they disagree, say in the record that they
> disagree and which one you used — do not silently pick.

IMO does the same thing at instrument level. Its **January 2026 publication supplement** to the
Grain Code omits annex item 6 of MSC.552(108) and carries **no operative clauses at all**, so the
supplement alone cannot establish the adoption route, the deemed-acceptance date, or the absence
of an application clause — the fact that decides whether an amendment binds existing ships.
**A supplement to a sales publication is an editorial aid, not the instrument.** Get the
resolution.

**A "latest event" fact is checked against the issuer's INDEX, not against a document.**
A card recorded the March 2026 National Shipping Board meeting as the latest verified, and hedged
that it might not be latest *"after 31 August 2026"* — while DGMA's own listing had carried the
16–17 April meeting for five months. The hedge was on the wrong side of the date. Worse, the card
said the Board *"meets quarterly"* — the Rules' norm — when that Board had been meeting roughly
monthly, which made a five-month-old answer look one meeting behind instead of four.

> **Rule.** For anything with a recurring cadence — meetings, sessions, circulars, editions —
> open the issuer's **listing page** and take the most recent row. Never infer currency from the
> document you happen to hold. And state the **observed** cadence, not the prescribed one: a
> cadence that understates reality hides staleness.

Retrieving the later minutes then produced a better finding than the review had asked for:
**both** the March and April sets are titled the *"31st meeting"*. Where a source is unreliable
about its own identifiers, drop them — that card now gives dates and venues and no ordinals.

**And a corpus index row is a pointer, not evidence — open the artefact.** H3A asked whether
MARPOL Annex I Appendix II had been amended since 2018, searched the shared corpus, read its
`INSTRUMENT_LOG.md` row for `MEPC.359(79)` — *"Annex I ch.6 reg 38 (reception facilities)"* — and
concluded no. The resolution's own title is *"…(Regional reception facilities within Arctic waters
and **Form of IOPP Certificate and Supplements**)"*, and its operative paragraph 3 replaces the
title of Form B section 5. **The file was on disk in the folder that was searched.** A card shipped
telling candidates the Supplement was last amended in 2018 when the answer is 2024, and an
independent reviewer caught it. The log had been written by an earlier run that summarised the
resolution by its headline subject and dropped the second limb. Treat every log row, manifest
entry, register line and `used_by` list the same way: it tells you *where to look*, and it is not
what you cite. This is the sibling of §14b's rule about quoting the card you reject — both say
that a summary is not the thing.

The common shape across all four: **the defect was inside a source already held, and only reading
a second part of it exposed the first.** Independent review found most of them; the rest surfaced
only because the findings were re-verified at source instead of accepted.

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
   `derive_audit_baseline` too. `oral_mutation.worktree_env()` injects the exception
   for exactly the one worktree path, and passes it to the child process. It lives in
   the shared module because the runner's gate baselines and every mutation harness's
   control precondition (§7.4a) must derive *the same* baseline the same way.

   **The mutator blocker this caused is closed.** `batch_e6_mutate` refused to launch
   at all while this debt existed; it is now baseline-aware and runs. The EOL evidence
   debt itself is untouched and still reports `PRE_EXISTING_BASELINE` — repairing it
   would mean rewriting what E6 certified.
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

## 14. Rolling intake — a mutable inbox is not a carrier

`ingest_carriers()` re-walks **every** registered carrier from the first on each run and
reproduces the earlier records byte-for-byte; `M4-BYTE-STABLE` checks exactly that. Identities
are allocated by position in that walk. So a registered carrier that **changes between runs
renumbers identities that have already been issued, adjudicated and published.**

That is fine while carriers arrive complete. It breaks the moment the Founder is collecting
reports *during* the day — which is the normal case, not an edge one. The 31-August inbox stood
at **842 bytes at 16:27** and **2,617 bytes at 19:48**, with more expected. Registering it would
have been registering a file guaranteed to change.

**The contract:**

```
mutable human inbox   →   immutable snapshot carrier   →   governed ingestion
(one file per day,        (_snapshots/<day> - snapshot     (registry order
 grows all day)            NN.txt, hash-pinned)             allocates identities)
```

1. **Never register the inbox.** Copy it to `_snapshots/… - snapshot NN.txt` and register the
   snapshot, with its SHA-256 and byte count.
2. **A later tranche is a NEW snapshot carrying only its own increment** — never a fresh full
   copy of the inbox, or its earlier submissions are ingested twice. Append it after the
   previous snapshot; identities continue and nothing already allocated moves.
3. **Prove it, do not assert it.** `S5-EXISTING-IDS-IMMOVABLE` simulates appending the next
   snapshot and checks that every existing occurrence keeps its id, text and submission;
   `S5-INBOX-NOT-A-CARRIER` checks the inbox is not registered; `S5-SNAPSHOT-IMMUTABLE`
   re-hashes what is.
4. **Say the window is open.** The carrier registry carries `intake_window.status =
   OPEN_EXPECTING_MORE_INPUT`. *A completely adjudicated snapshot is not a closed day*, and
   `intake count == adjudication count` is green while the window stays open. Do not report a
   day's count as final because the validator is green.
5. **Do not pin a day's total in a control.** `M5-ALL-REGISTERED` asserted the registry equalled
   exactly three named carriers and went red the moment a fourth was appended — guard expiry,
   for the sixth time. It now asserts the historical carriers are still the registry's ordered
   **prefix**, which stays true however many snapshots follow.

### 14a. Grammar is per-carrier evidence, never assumed from the last one

Each carrier has arrived with grammar the previous ones did not have, and every time the parser
has **failed silently** — a lost occurrence raises no error, it simply is not counted. 24 August
lost a whole submission to `1.`-only recognition; 27 August lost five starred probes; 31 August
lost **four lettered root asks and one unnumbered question**, and reported `unparsed_blocks: []`
while doing it.

Read the source before ingesting, and add a RED control per defect **before** touching the
parser. What 31 August added: lettered roots (`A.` `B.`) with `Cross questions:` beneath and
numbering restarting under each letter; a question mark as the only signal that an unnumbered
line is a question; `2nd attempt` where `ATTEMPT_RE` expects `Attempt 2`; and honorifics
(`Mr. Simon,`) that the alias register must carry as observed forms rather than the normaliser
guess at.

Two rules that generalise:

* **A structural branch that links a child to a parent needs a fallback.** The starred-probe
  branch takes "the most recent non-starred occurrence" when no explicit parent exists; the
  cross-question branch first shipped without that fallback and orphaned a probe the candidate
  had plainly marked. If one branch has the rule, ask why the other does not.
* **Nothing examinable may reach `context_comments` alone.** Metadata consumed into a field is
  accounted for by the value it produced; a *question* is not. `S4-NO-SILENT-LINE-LOSS` walks
  every non-rule source line and requires each to be an occurrence, a preserved comment, or a
  recognised metadata match.

### 14b. A rejection reason must quote the card it rejects

Adjudication rejects candidate cards by the dozen, and the failure mode is specific: **the card
is returned by the search and then rejected on its TITLE.** Two of six `GENUINE_NEW_QUESTION`
calls on 31 August were wrong that way, and both would have commissioned an answer the bank
already held — `QB3_J#q6` reads as a UV-technology question and carries the full USCG-versus-IMO
approval comparison; `QB9_H#q1` reads as an India-ratification question and carries the Article
253 route by which a convention reaches the Merchant Shipping Act.

So a `negative_search` rejection must quote the body text it is rejecting, and the record must be
**generated from its own pattern** — the same run also produced a `negative_search` whose stated
hit count and reject list matched only by coincidence: five listed ids were not hits at all and
five real hits were missing, one of them the nearest miss in the bank. A hand-picked relevance
list wearing a regex's clothes is worse than no evidence, because it reads as a sweep.

---

## 12. Product invariants (assert, never assume)

| Invariant | Value |
|---|---|
| Canonical Oral questions | **721** |
| Question-bearing files | **86** |
| Examiner relationships / examiners | **960 / 7** |
| Price | **₹1,499, one year** |

A batch that changes any of these without saying so in its manifest is a stop condition.

---

## 13. Candidate workbook export (XLSX) — fast lane, not a release

Every interim/final question-bank spreadsheet comes from repo truth through one
exporter. Never patch a previous workbook by hand; never treat an old workbook as
question identity (the July/v26 files are presentation references only and live
git-ignored under `docs/MIW-master-Question-bank/`, as does every generated one).

```
PYTHONIOENCODING=utf-8 python tools/oral/export_question_bank_xlsx.py --candidate-share --month 2026-08
PYTHONIOENCODING=utf-8 python tools/oral/validate_question_bank_xlsx.py docs/MIW-master-Question-bank/MIW_MEO_Class1_Oral_QuestionBank_August_2026.xlsx --month 2026-08
PYTHONIOENCODING=utf-8 python tools/oral/test_question_bank_xlsx.py
```

`--candidate-share` is the group-facing product; `--candidate-interim` and
`--working-master` still write the internal INTERIM and WORKING copies from the
same model. Regenerate all three together so the on-disk set never disagrees.

Pipeline: `qb_content_index.json` (identity + text, proven fresh by
`build_qb_content_index.py --check`) + `EXAMINER_INDEX_SNAPSHOT.json` (the same
object the examiner page renders from) + live HTML (anchor proof only)
→ `build_export_model()` → `render_workbook()`. The renderer infers nothing.
The model reserves `official_syllabus_version / official_syllabus_node_id /
miw_topic_id / miw_topic_name / objective_id` for the governed syllabus mapper;
they are empty and unrendered until that mapper is production-authorised — the
exporter must never populate them. "Topic / Category" is the current production
QB page title. Examiner cells are names only (tier/evidence stay internal).

Counting semantics (do not mix): 738 canonical questions; 86 question-bearing
pages; 958 examiner relationships = distinct (examiner, question) pairs across
7 examiners; the older 862/6 figure is the pre-Release-A
`CURRENT_EXAMINER_RELATIONSHIPS.jsonl` before John and the 103 Release-A rows.

### 13.1 The monthly "New & Updated" sheet

The share workbook carries a `<Month> <Year> - New & Updated` sheet as sheet 2.
Its rows come from `tools/oral/oral_monthly.py`, never from curation. Three rules
carry all the weight, and each exists because the obvious alternative is wrong:

* **Date the question, not the anchor.** Identity is file+anchor and anchors get
  RENUMBERED, so "first commit carrying this anchor id" invents new cards out of
  renumbered old ones — on August 2026 it claimed 109 new anchors against 50
  governed `NEW_CARD` actions. The module instead reconstructs the corpus from
  the git tree at the last commit BEFORE the month and compares wording.
* **Occupancy beats wording.** A card sitting on an anchor the baseline already
  carried existed then, whatever its text now says, so it is capped at UPDATED.
  This demoted five August cards (the four QB2_C slots whose July q-text was
  answer scaffolding, plus one enriched leadership question just under the
  similarity floor). Over-claiming "new" is the dangerous direction in a
  marketing artefact; this rule can only ever under-claim.
* **Two evidence streams, cross-checked.** Every manifest `NEW_CARD` action must
  land in the wording-derived NEW set or the export FAILS. The manifest regime
  only began 2026-08-19, so a month may legitimately hold new cards no manifest
  governs (the eight QB pages of 2026-08-04) — but never a governed creation the
  wording test disputes.

A manifest action kind that is in neither `CREATE_KINDS` nor `UPDATE_KINDS` is a
hard failure: a new governance word must be classified deliberately, not drop
silently out of the candidate-facing view. Derived-index regeneration, CSS/TOC
repair and validator-only edits are deliberately NOT updates.

`validate_question_bank_xlsx.py --month YYYY-MM` re-derives the projection
INDEPENDENTLY rather than reading the exporter's answer back, and
`test_question_bank_xlsx.py` mutation-proves each month control (deleted row,
flipped status, duplicate, phantom id, wrong link, inflated headline, buried
sheet). August 2026 baseline: `2c0fd8b` (2026-07-31, 627 questions) → 738 today,
111 NEW + 71 UPDATED = 182 rows.

Exporting changes no product content, so it does NOT trigger the full release
runner. The protected names (`MEO_QB_master_v26.xlsx`,
`MIW_July2026_QuestionBank_SHARE.xlsx`, `MEO_QB_master_v27.xlsx`,
`MIW_August2026_QuestionBank_SHARE.xlsx`) are refused by the exporter; the final
two are produced by this same exporter only after the final release sequence
(follow-ups → corpus freeze → 788-occurrence audit → final validation).
