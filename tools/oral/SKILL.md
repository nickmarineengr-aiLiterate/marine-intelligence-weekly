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
python tools/oral/run_oral_release.py --full     # 39 gates + determinism
```

**39 gates**, derived from repository evidence rather than memory. E1's handoff §17
enumerates its 37 by name (Node counted as three records); E5 reports 37 with Node
collapsed to one plus the two E5 gates; E6 reports 39 — E5 plus `validate_batch_e6` and
`batch_e6_mutate`. Adding a batch adds exactly those two gates and nothing else.
Determinism is registered separately because all three handoffs report it outside the
gate count.

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

The next workload is **35 follow-up groups** — examiner follow-up questions attached to
existing cards. The workflow is the enrichment workflow with two extra steps, and the
tooling above is deliberately batch-kind agnostic:

```
follow-up group
  -> resolve canonical home and relationship (which card owns the answer?)
  -> current-live recheck (is it already answered on that card?)
  -> primary verification where the answer is regulatory
  -> bounded product edit
  -> relationship metadata      <-- new
  -> manifest (oral_manifest.py)
  -> validator (fails closed)
  -> mutation preflight
  -> mutation suite (parse with the shared parser)
  -> full release gates
  -> handoff
```

**Relationship metadata.** Record the follow-up as a directed edge:
`question -> examiner follow-up -> next canonical question/answer`. Keep it clean enough
that a later examiner simulator can walk it. Do **not** build a Study Engine now; just
do not represent the relationship in a way that would need re-authoring to consume.

`creates_new_cards` may be **true** for a follow-up batch. Do not assume the
enrichment-only invariant of "0 cards added"; assert whatever the manifest declares.

---

## 8. Sibling-manifest delegation

A later authorised change must be accepted by an older batch's guard, through explicit
delegation to the later manifest. The delegation must be **non-vacuous**: without the
later manifest the older guard fails; with it, it passes. Verify both directions when
you add one — a delegation that passes when the manifest is absent is not a delegation.

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
2. **`authorisation_source` is unread by every batch validator.** It duplicates a
   hardcoded constant. It is now asserted to *resolve* by `oral_manifest.py`, so it is no
   longer decoration, but no validator selects through it.
3. **`index_tier_literals_valid`** fails in `validate_audit.py` on a clean `origin/main`
   (43 invalid literals). Pre-existing baseline, carried since E1.
4. **Stale counters** in `VALIDATION_RESULTS.json` / `PHASE2_VALIDATION_RESULTS.json`
   (`live_questions` 688 vs 721, `headings` 954 vs 960).
5. **RELEASE-BLOCKING — 7 of the 11 batch validators are red on `main` at `1922db1`.**
   The candidate-correction commits `7135a7a` and `1922db1` changed `QB1_A#q24`,
   `QB1_A#q25`, `QB1_B#q15` and `QB5_A#q4` **without a batch manifest**. Verified by
   `run_oral_release.py --category batch --read-only --keep-going`:

   | Validator | Result | Failing check |
   |---|---|---|
   | `validate_batch_a` / `_c` / `_d` / `gap0609` | PASS | — |
   | `validate_batch_b` | **FAIL 1** | `pre_existing_cards_unchanged`, drifted `QB5_A#q4` |
   | `validate_batch_e1`…`e5` | **FAIL 1** each | `only_authorised_cards_changed` |
   | `validate_batch_e6` | **FAIL 2** | the above, plus item 1 |

   **This is the authorisation contract working, not a tooling defect** (§8): a change
   that no manifest declares is exactly what these guards exist to catch, and `batch_b`
   caught it through a digest pin rather than the corpus-wide check. It was invisible
   until now only because no committed runner existed. A full release cannot go green
   until the correction is declared in a manifest the older guards can delegate to, or
   the guards are deliberately reconciled. Product content was deliberately NOT touched
   when this was found.

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
