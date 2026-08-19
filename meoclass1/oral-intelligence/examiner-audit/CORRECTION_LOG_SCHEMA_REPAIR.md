# Oral hub correction log — schema normalised (19 August 2026)

Bounded fast-follow to the content-index rebuild (`ed4e077`), fixing debt item 1
of `QB_CONTENT_INDEX_REBUILD_RECORD.md`: 21 of 33 governed correction records
rendered as a blank line on the live hub.

## Root cause

Not a data typo — two consumers bound to two different keys, and neither ever
validated the key it read:

| when | who | key |
|---|---|---|
| 2026-07-04 | first `recently_updated` records | `note` + `files` |
| 2026-07-15 | hub renderer `toggleCorrectionLog()` in `meoclass1/index.html` | reads `e.note`, `e.files` |
| 2026-07-18 → 08-18 | 21 authored records | `summary` |
| 2026-07-27 | `qb_health_check.check_manifest` changelog-gap check | reads `entry["summary"]` |
| 2026-07-30 → 08-01 | 4 records | `files_touched` instead of `files` |

Shapes at `ed4e077`: `{date,files,summary}`×17, `{date,files_touched,summary}`×4,
`{date,files,note}`×12. Rendered: 33 rows, **21 blank descriptions** (4 of them a
bare date, because `files_touched` is also not the renderer's key).

## Canonical contract (one)

```
date   YYYY-MM-DD                        required
note   human-readable description        required, non-empty
files  list[str], structured metadata    optional — never the description
```

Chosen `note` (not `summary`) because it is the original schema, it is what the
candidate-facing renderer already binds to, and `files` was already 29/33. The
21 `summary` texts are full human descriptions, so migration is a pure key
rename — automated, no hand-editing, no text change.

## What changed

| file | change |
|---|---|
| `tools/oral/qb_content_index_governed.json` | 25 keys renamed (`summary`→`note` ×21, `files_touched`→`files` ×4); key order normalised to `date, note, files`; **order, dates and text verified equal to `origin/main` for all 33**; other sections byte-equal |
| `tools/oral/build_qb_content_index.py` | `check_corrections()` at governed load: refuses `summary`/`files_touched`/unknown keys, blank `note`, non-list `files`, duplicate `(date, note)`. Regeneration cannot re-admit the split. |
| `meoclass1/qb_content_index.json` | regenerated; only the 25 renamed keys moved |
| `meoclass1/qb_health_check.py` | changelog-gap check reads `note` (was `summary`); scan scope unchanged (description only) |
| `tools/oral/validate_qb_content_index.py` | +3 checks: `corrections` (schema/blank/type/dupes, own walk), `renderer` (index.html log block binds to `e.date/e.note/e.files`, no `e.summary`/`files_touched`), `corrections_preserved` (manifest == governed, verbatim, same order; per-file `corrections_applied` carried through) → 22 checks |
| `tools/oral/mutate_qb_content_index.py` | +6 mutations L–Q: blank note, obsolete `summary` key, scalar `files` + `files_touched`, duplicate record, renderer reads `e.summary`, generator drops corrections → 17 mutations |
| `meoclass1/index.html` | **not changed** — the renderer already read the canonical keys |

## Gates

| gate | result |
|---|---|
| `validate_qb_content_index.py` | 22 / 0 FAIL |
| `mutate_qb_content_index.py` | 17 / 0 escapes (all caught by the named check) |
| generator fail-closed on the governed *source* | `summary`, `files_touched`, blank note, duplicate, scalar files → `BUILD FAILURE` (5/5) |
| `build_qb_content_index.py --check` | clean |
| determinism `PYTHONHASHSEED` 0 / 1 / 524287 | identical sha256, equal to committed |
| rendered log (renderer emulated + chrome-devtools on a local origin) | 33 rows, 0 blank, 0 `undefined`, 0 raw arrays, 0 duplicates; desktop and 375×812 mobile: 0 overflowing rows |
| `test_oral_controls.py` / `test_notes_controls.py` | 315/0, 106/0 |
| `validate_examiner_index.py` / `build_examiner_index.py --check` | 52/0, nothing written |
| `deploy_surface.test.mjs` | 92/92 |
| QB*.html, examiner index, SQ, Written QI, magazine, payments | untouched |

## Debt found, not actioned

1. `qb_health_check` changelog-gap count rises 15 → **27** on this tree: the old
   `summary` key silently skipped the 12 `note` records, so 12 more real gaps
   (files named in a correction with an empty `corrections_applied`) now surface.
   Same class as rebuild-record debt 2; nothing new was introduced.
2. Correction-log prose carries internal production vocabulary to candidates
   (candidate first names, "via Nixon, WhatsApp", commit SHAs, `known_traps.md`
   Entry n). Pre-existing on the 12 entries that already rendered; now visible on
   all 33. Editorial, not schema — a candidate-facing wording pass is a separate task.
3. The `files` list is free text in two entries ("65 files across meoclass1/… see
   known_traps.md Entry 6"). Type-valid but not a file list; same wording pass.
