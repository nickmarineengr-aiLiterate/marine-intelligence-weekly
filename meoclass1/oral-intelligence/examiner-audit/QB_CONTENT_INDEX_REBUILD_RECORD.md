# qb_content_index.json — rebuilt from the live QB HTML (19 August 2026)

Post-release fast-follow after the pre-24-Aug Oral Release A + P0 sprint
(`b7c249e`). Bounded to one job: make the live QB HTML the canonical source of
`meoclass1/qb_content_index.json`, at the generator, not by hand-patching rows.

## What was true before

`qb_content_index.json` had never had a generator. Every version since inception
was hand-written (`generated_by: "Claude (...)"`), keyed by array position, with no
anchor. The hub search on `meoclass1/index.html` reads a **second** hand-written
copy of the same data, the inline `Q_INDEX` array; the JSON is fetched by that page
only for the `recently_updated` correction log.

Measured against the live q-cards at `b7c249e` — **688 canonical / 86 files**, derived
here and matching the P0 review's figure:

| class | records | where |
|---|---|---|
| UNCHANGED | 579 | — |
| ENCODING_ONLY (raw `&mdash;`/`&amp;` stored; rendered double-escaped by `esc()`) | 38 | QB2_A 29, QB2_I 3, six singles |
| ANCHOR_DRIFT (old q-number's text lives at a *different* live anchor) | 37 | QB2_B 17, QB1_B 15, QB1_supplementary 5 |
| TEXT_STALE | 32 | QB5_C_B 8, QB10_B 8, QB10_A 6, QB6_F 5, QB1_supplementary 2, QB1_F/QB4_D/QB1_B 1 each |
| NONQUESTION_RECORD (revision cards counted as questions) | 2 | QB1_A q32 `#family-trees`, q33 `#dependency-graph` |
| NONQUESTION_FILE_ENTRY (cheat-sheet stubs in `files{}`) | 5 | QB1_K/2_I/4_J/8_H/9_H `_CheatSheet.html` |
| METADATA_LEAK | **2** | QB1_K q8 `(Simon sir) …`; **QB7_B q2 `Examiner context:** Rajappan (2026) …`** (not previously reported) |
| MISSING_RECORD / NEW_RECORD | 0 / 0 | — |

Old total 690 vs live 688. The historical "95" was a one-off text-and-position
comparison whose tolerance was not recorded; it does not reproduce to the digit
(exact 111, entity/whitespace-tolerant 79, punctuation-folded 73), but the *class*
reproduces exactly — same drift files, same stale files, same entity file — and
main did not move between the review and this rebuild.

Root cause of ANCHOR_DRIFT: QB1_B, QB2_B and QB1_supplementary carry q-card ids
**out of document order** (QB2_B: q1,q3,q4,q5,q8,q6,q14,…). A positional index
cannot survive that. Anchor is identity; array position is display order.

## What was built

| file | role |
|---|---|
| `tools/oral/build_qb_content_index.py` | generator. Reads live QB pages via `oral_lib.qb_files()/parse_qb_file()` (q-card with `id="q<N>"` = canonical question), the cheat sheets on disk, `QB_GROUPS` membership, and the governed file. Writes the manifest and exactly three regions of `index.html` (the `Q_INDEX` line, each card's `qcount`, the `Questions Live` counter), each anchored by a regex that must match once. Fails closed on duplicate anchor, empty q-text, or examiner/production metadata in q-text. Staging file + `os.replace`. LF, UTF-8. `--check` exits 3 when disk is stale. |
| `tools/oral/qb_content_index_governed.json` | the only hand-maintained input: `recently_updated` (33 entries, verbatim), per-file `corrections_applied` (34 files), `version` fallback for the 57 pages with no `Version:` line, `cheatsheet_overrides` for QB1_FG. No question text. |
| `tools/oral/validate_qb_content_index.py` | 19 named checks; independent html.parser walker, not the generator's regex. |
| `tools/oral/mutate_qb_content_index.py` | 11 mutations, each must fail its *named* check (crash = escape). |
| `docs/miw-qb-index-linkage_SKILL.md` | re-pointed: manifest + `Q_INDEX` are generated; the doc's own `Q_INDEX` example carried the `(Simon sir)` record and the `&amp;` convention. |

## Field audit

| field | class | decision |
|---|---|---|
| `files{}` keys | LIVE-DERIVED | 86 QB pages with cards; the 5 cheat-sheet stubs dropped (`qb_health_check` never required them; cheat sheets attach via the parent's `cheatsheet`) |
| `questions[].text` | LIVE-DERIVED | candidate-facing q-text of the live card, entities decoded |
| `questions[].anchor`, `id`, `order` | LIVE-DERIVED, **new** | `id` = `QB1_K#q8` (the corpus convention); `order` = document position |
| `questions[].qnum` | LIVE-DERIVED | now read from the anchor, kept for `audit_sources.py` compatibility |
| `question_count`, `total_questions`, `total_files` | LIVE-DERIVED | 688 / 86 |
| `title` | LIVE-DERIVED | from `<title>` with the `QBx — ` / ` \| MIW…` trim (49 old values were hand-styled variants; no consumer reads it) |
| `tags` | LIVE-DERIVED | union of card `data-tags` (14 old values stale) |
| `cheatsheet` | LIVE-DERIVED | case-insensitive `<stem>_CheatSheet.html` on disk (39 linked; old JSON linked 9) + QB1_FG override |
| `cheatsheet_inline` | LIVE-DERIVED | true when the page carries an inline cheat block; old flags (QB3_J/5_J/6_H) were on the wrong files — live blocks are on QB6_D/7_E/8_C |
| `version` | LIVE where present (29 pages), else GOVERNED | `version_source` says which |
| `corrections_applied` | GOVERNED | verbatim; read by `qb_health_check` changelog-gap check |
| `recently_updated` | GOVERNED | verbatim; rendered by the hub correction log |
| `qb_group`, `letter` | LIVE-DERIVED | from file name |
| `generated` (date) | OBSOLETE | dropped — non-deterministic; `generated_by`/`source` name the tool |
| `manifest_version` | STATIC | 1.0 → 1.1 (additive) |
| stub `type`/`parent_file` | OBSOLETE | dropped with the stubs |

## Consumers

| consumer | reads | compatible |
|---|---|---|
| `meoclass1/index.html` (hub) | `recently_updated` via fetch; inline `Q_INDEX` for search | yes — `Q_INDEX` regenerated from the same derivation, plain text, +`anchor` |
| `meoclass1/qb_health_check.py` | `files{}` keys, `question_count`, `cheatsheet`, `corrections_applied`, `recently_updated[].summary`; `Q_INDEX` count, card `qcount`, hero counter | yes — run locally against the tree: `check_index_linkage` clean, `check_manifest` shows the same 15 pre-existing changelog-gap errors as clean `origin/main`, 0 new; manifest sum now 688 = disk 688 (was 690 vs 688) |
| `tools/oral/audit_sources.py` | `files{}`, `question_count`, `questions[].qnum/.text` | yes |
| `tools/notes/miw_paths.py` | path only | yes |
| `tools/security/deploy_surface.test.mjs` | path in deploy surface | yes, 92/92 |
| `tools/oral/reconcile_788.py` | does not read it (its docstring records the off-by-one) | n/a |

**Positional q-number resolution:** no consumer resolves "question N" by array
position. `qb_health_check` counts; `audit_sources` keys by `qnum` (now the anchor
number). The hub search links `href="${h.file}"` without an anchor — a UX gap, not
a resolver; the record now carries `anchor` for whenever that link is upgraded.

## Gates

| gate | result |
|---|---|
| `validate_qb_content_index.py` | 19 checks / 0 FAIL (17/19 FAIL against the old artefacts) |
| `mutate_qb_content_index.py` | 11 mutations / 0 escapes |
| determinism | PYTHONHASHSEED 0 / 1 / 524287 → identical sha256 for both outputs, equal to committed |
| cross-drive | HEAD exported to `C:\…\Temp` and run there → identical sha256, 19/0, 11/0 |
| `build_qb_content_index.py --check` after commit | outputs on disk match the live derivation |
| `test_oral_controls.py` / `test_notes_controls.py` | 315/0, 106/0 |
| `validate_examiner_index.py` / `build_examiner_index.py --check` | 52/0, nothing to write |
| `deploy_surface.test.mjs` | 92/92 |
| live QB HTML, `examiner-index.html`, `SQ/`, payments, Written QI, magazine | untouched |

## Debt found, not actioned

1. Hub correction log renders `e.note`; 21 of 33 `recently_updated` entries use `summary`
   (17) or `files_touched` (4) and so display an empty line. Pre-existing UI/data key
   mismatch; the governed file is verbatim, so it is fixable in one place.
2. `qb_health_check` "changelog gap": 15 pre-existing errors (files named in
   `recently_updated` with no `corrections_applied`), identical on `origin/main`.
3. `QB_GROUPS` card `version`/`tags`/`title`/`cheatsheet` are still hand-maintained and
   disagree with the derived manifest on 28/21/1/30 cards. The generator owns only `qcount`.
4. Hub search result links to the file, not `file#anchor`; the record now carries the anchor.
5. `Last Updated` hero stat is hand-entered (still "18 Aug 2026").
