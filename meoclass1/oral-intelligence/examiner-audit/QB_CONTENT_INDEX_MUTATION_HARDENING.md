# qb_content_index mutation harness hardening — S/U escapes closed

Date 2026-08-19 · branch `fix/oral-qb-content-index-mutation-su` from `ccf7560` ·
Laptop · tooling/validation only. No QB HTML, examiner data, SQ, correction wording,
generator or validator code changed.

## The defect

`tools/oral/mutate_qb_content_index.py` mutations **S** ("via Nixon") and **U** (commit
SHAs) escaped on `ccf7560`: `26 run, 2 escape(s)`, both `observed=[]`.

Root cause — **stale mutations, not a validator or generator gap.**

| | S | U |
|---|---|---|
| target | scratch `qb_content_index.json`, `recently_updated[3].note` | same, `recently_updated[9].note` |
| method | `str.replace("QB1_A:", "QB1_A (candidate-flagged, via Nixon):")` | `str.replace("24 corrections", "24 corrections (commits 7044e4b, 30fb6f5)")` |
| why it escaped | after the editorial cleanup (`3de74d4`) three commits (`156ca93`, `b263d41`, `e6c94ce`) each **prepended** one governed row (33 → 36). Every index shifted by 3: the `QB1_A:` note is now row 6, the `24 corrections` note row 12. `str.replace` on the absent anchor returned the note unchanged → the "mutant" was byte-identical to the baseline → the validator was correctly green. | same |
| harness weakness | it could not tell "mutation never landed" from "validator blind": both print `observed=[]`. | same |

## Both protection lines were proven healthy before any edit

- **Line 1, governed source → generator.** Injected ` Candidate-flagged via Nixon (commits a1b2c3d, 30fb6f5).` into `tools/oral/qb_content_index_governed.json` row 0 → `build_qb_content_index.py --check` → `BUILD FAILURE: recently_updated[0] … hygiene violation - person: Nixon … (4 hit(s))`, rc 2.
- **Line 2, generated manifest → validator.** Same string into `meoclass1/qb_content_index.json` only → `validate_qb_content_index.py` → `hygiene FAIL 4 hit(s): person: Nixon, repo: commit/SHA 'a1b2c3d', repo: commit word, workflow: via <person>` (+ `corrections_preserved`, `determinism`), rc 1.
- All three artefacts restored byte-exactly (sha256 checked). `CORRECTION_FORBIDDEN` (25 patterns) not touched.

## Repair (harness only)

`tools/oral/mutate_qb_content_index.py`
1. S/T/U rewritten through `_append_note()` — a pinned regression fragment is **appended**
   to whatever row sits at the index, so a governed prepend can never no-op them again.
   `REGRESSION_VIA_NIXON = " Re-evaluation request received via Nixon."`,
   `REGRESSION_SHA = " Applied under a1b2c3d and 30fb6f5."` — hex with letters and digits and
   **no "commit" word**, so the constrained SHA regex is proven load-bearing on its own.
2. Mutation-quality gate: the scratch artefacts are SHA-256'd before/after; a mutation that
   leaves them byte-identical is reported `ESCAPE (NOT APPLIED - mutation is a no-op)` and
   never counts as a catch (rerunning the *old* S/U bodies through the new harness prints
   exactly that).
3. Hygiene mutations S T U V W Y assert the `CORRECTION_FORBIDDEN` label that fired
   (`ESCAPE (wrong hygiene label)` otherwise).
4. Per-mutation report: verdict, target, `applied=`, expected checks, observed checks,
   hygiene labels; run summary adds crash count and a live-artefact byte-identity check
   (governed JSON, manifest, index.html hashed before/after; residue → exit 1).
5. Nothing shells to git; strings are pinned in the file.

## After

`26 run, 0 escape(s), 0 crash(es); live artefacts byte-identical: True` —
S → `hygiene` with `person: Nixon`, `workflow: via <person>`; U → `hygiene` with `repo: commit/SHA`.

## Gates

`build_qb_content_index.py --check` clean (86 files / 688 Q) · validator 24/0 ·
determinism `PYTHONHASHSEED` 0/1/524287 → manifest `6396f4f4…`, index `0f7d8c3a…` (= live) ·
normal generation ×2 → zero product diff · examiner `--check` 4/4 current + semantic PASS ·
`validate_examiner_index` 52/0 · `validate_ce_tip_review` 28/0 · `test_examiner_check` 10/10 ·
oral controls 315/0 · notes controls 106/0 · q-text gate 7157/0 · deploy-surface 92/92 ·
link integrity 20/20 · `qb_health_check` 33 ⚠ on branch and on main (identical, pre-existing) ·
cross-drive C: copy: `--check` clean, validator 24/0, mutations 26/0/0 ·
product hashes unchanged: `qb_content_index.json 6396f4f4…`, `index.html 0f7d8c3a…`,
`examiner-index.html e31458ca…`, `SQ/examiner-index.html ff8cb629…`, `SQ/index.html 9011a03d…`.
No audit artefacts dirtied.

## Left alone (per brief)

27/33 changelog gaps · 43 invalid tiers · reverse Asked-by · Written QI · magazine · payments ·
master XLSX (v27 / August SHARE deferred) · QB content · examiner adjudication · P1/P2.

## Debt noticed (≤3)

1. Mutations L M N O W X Z still address rows by fixed index; they are content-independent so
   they cannot no-op, but the harness's `NOT APPLIED` gate is now the only thing that would
   catch a future positional mutation that does.
2. `mutate_examiner_index.py` / `mutate_ce_tip_review.py` do not have the byte-digest
   "applied" gate — the same no-op escape class is possible there.
3. The prior report `CORRECTION_LOG_EDITORIAL_CLEANUP.md` recorded 26/0 truthfully for
   `3de74d4`; the escape appeared three commits later without any tooling change — a mutation
   suite that pins positions is a wasting asset the moment the dataset it targets grows.
