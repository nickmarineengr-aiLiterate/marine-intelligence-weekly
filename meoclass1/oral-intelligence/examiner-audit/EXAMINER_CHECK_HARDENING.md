# Examiner Index generator: `--check` now checks

Tooling-only session, 2026-08-19. Branch `fix/oral-examiner-generator-check-stale-output`
from `6c84b54`. Zero product change: every generated artefact is byte-identical before and
after (`e31458ca…` index, `ff8cb629…` teaser, `9011a03d…` SQ home, `f8bdf3f5…` snapshot).

## The defect

`build_examiner_index.py --check` built the snapshot and pages in memory, printed the counts,
then printed `--check: nothing written` and returned 0. It never compared what it built with
what was on disk and never ran the validator. So a hand-edited `meoclass1/examiner-index.html`,
a stale `EXAMINER_INDEX_SNAPSHOT.json`, a stale `SQ/examiner-index.html`, or a governed input
changed without regeneration all passed `--check`. Reproduced on clean `6c84b54`: Simon's
section count edited 280→281 in the full index, `--check` exit 0.

No earlier report named this explicitly; every prior gate table recorded the honest words
"52/0, nothing written". The sibling `build_qb_content_index.py --check` already exits 3 on
stale disk, so this brings the examiner generator to the same contract.

## The contract now

One build path, one output set:

| function | role |
|---|---|
| `GENERATED_OUTPUTS` | the canonical tuple: `EXAMINER_INDEX_SNAPSHOT.json`, `meoclass1/examiner-index.html`, `SQ/examiner-index.html`, `SQ/index.html` (card only, but the whole file is the artefact) |
| `build_outputs()` | resolve + render + self-checks once → `(snapshot, {Path: bytes})`, LF/UTF-8; writes nothing; refuses if its keys ≠ `GENERATED_OUTPUTS` |
| `write_outputs()` | normal mode: staging file beside the target, fsync, `os.replace()` (was a plain `write_bytes` before — now atomic) |
| `check_outputs()` | `--check`: byte-compare each artefact with disk; reports `STALE OUTPUT` (sha256 + size of both, first differing line clipped to 120 chars), `MISSING OUTPUT`, `EXTRA OUTPUT` (only the generator's own `*.staging` residue — arbitrary orphan scanning is out of scope by design) |
| `run_semantic_validation()` | `--check` also runs `validate_examiner_index.py` as a subprocess (it imports the generator, so in-process would be circular); it reads disk and writes nothing |

Exit codes: **0** current + valid · **1** semantic validation failed · **2** build failure ·
**3** stale / missing / extra generated output. Stale wins over semantic in the exit code; both
are printed. Success prints exactly:

```
EXAMINER INDEX CHECK: PASS
4/4 generated artefacts current
semantic validation PASS
```

`--check` writes nothing under any outcome: proven by hashes and `git status --short` around
every run in the new suite.

## Test suite: `tools/oral/test_examiner_check.py`

Runs the tool as a subprocess; a caught failure must be non-zero, carry
`EXAMINER INDEX CHECK: FAIL`, name the artefact with the right marker, and show no traceback.
Everything restored byte-for-byte under a Guard; restoration itself is asserted.

| | mutation | result |
|---|---|---|
| A | pristine tree | PASS, exit 0 |
| B | full index section count hand-edited | STALE `meoclass1/examiner-index.html`, exit 3 |
| C | snapshot total altered | STALE snapshot, exit 3 |
| D | SQ teaser "Questions Tagged" altered | STALE `SQ/examiner-index.html`, exit 3 |
| E | SQ home card promo count altered | STALE `SQ/index.html`, exit 3 |
| F | `SQ/examiner-index.html` deleted | MISSING OUTPUT, exit 3 |
| G | one Simon `APPROVE_CE_TIP` in `STRONG_CE_TIP_REVIEW_DECISIONS.json` flipped to `HOLD_WEAK_ASSERTION`, nothing regenerated | all four artefacts STALE, exit 3 (a Nair pair would leave `SQ/index.html` current — the card only carries Paul/Simon counts — which is correct, not an escape) |
| H | hashes + `git status` identical around every `--check` | PASS |
| I | normal generation on a current tree | zero byte change (write path == check path) |
| J | `SQ/examiner-index.html.test.staging` left beside the teaser | EXTRA OUTPUT, exit 3 |

10/10, 0 escapes on F:; 10/10 on a disposable C: worktree (`autocrlf=true`, artefacts still
4/4 current — LF is pinned for them); byte-identical `--check` PASS at `PYTHONHASHSEED`
0 / 1 / 524287; no `F:` or user path in either file.

## Gates after the change (all unchanged from the CE-tip review record)

`validate_examiner_index.py` 52/0 · `mutate_examiner_index.py` 13/0 · `validate_phase2.py`
107/0 · `validate_ce_tip_review.py` 28/0 · `mutate_ce_tip_review.py` 17/0 ·
`build_qb_content_index.py --check` clean · oral controls 315/0 · notes controls 106/0 ·
question-text gate 7157/0 · deploy-surface 92/92 · link integrity 20/20 · normal generation
run twice → zero diff · counts 960 total / Nair 361 / Simon 280 / ce_tip 214 (6 review
approvals in, 4 holds out — the check path consumes the same decisions file, test G proves it).

## Left alone (per brief)

`mutate_qb_content_index.py` S/U escapes (still present, next tooling task) · 27 changelog
gaps · 43 invalid tiers · reverse Asked-by · Written QI · magazine · payments · master XLSX
(v27 / August SHARE deferred) · QB content · examiner adjudication.

## Debt noticed (≤3)

1. `mutate_examiner_index.py` and `test_examiner_check.py` each carry their own `Guard`;
   a shared helper in `oral_lib` would remove the duplication (cosmetic).
2. `validate_phase2.py` still rewrites `PHASE2_VALIDATION_RESULTS.json` on every run and must be
   reverted by hand after a gate sweep (pre-existing, unchanged).
3. A cross-drive git worktree needs `safe.directory` (env-scoped `GIT_CONFIG_*` works) before
   the validator's "no raw source tracked by git" check can run; without it `--check` reports a
   semantic FAIL that is environmental, not a product defect.
