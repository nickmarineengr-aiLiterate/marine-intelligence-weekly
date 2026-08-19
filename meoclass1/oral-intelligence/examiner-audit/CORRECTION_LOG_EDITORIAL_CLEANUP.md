# Oral hub correction log — candidate-facing editorial cleanup (19 August 2026)

Bounded fast-follow to `CORRECTION_LOG_SCHEMA_REPAIR.md` (debt items 2 and 3).
Once the schema repair made all 33 governed rows render, the pre-existing
production vocabulary in the notes became visible to paying candidates on the
`/meoclass1/` hub. This pass rewrote the human-readable `note` of every row so
the public log says **what changed** — not who told us, which chat, which
commit, which internal file, which AI — and added a fail-closed hygiene guard so
the vocabulary cannot come back through the generator.

Not a schema change. Not a technical-truth change. Not a UI change.

## Governing principle

Preserve the correction. Remove the workflow.

## What was in the 33 rows before (regex census, `correction_hygiene_violations` on `ca881c4`)

126 hits on 31 of 33 rows:

| class | hits | examples |
|---|---|---|
| person: Nixon / "via Nixon" | 20 + 8 | "Nixon-flagged", "via Nixon", "for Nixon", "Nixon's review" |
| person: candidate first name | 6 | two candidate first names as correction sources |
| chat: WhatsApp / screenshot | 3 + 3 | "WhatsApp transcripts", "screenshot review" |
| repo: known_traps.md / Entry n | 15 + 14 | "See known_traps.md Entry 32" |
| repo: source file (.md/.json/.py/.xlsx) | 17 | ledger json path, tool names |
| repo: commit SHA / "commits" / GitHub / local drive path | 1 + 2 + 3 + 1 | "commits 7044e4b, 30fb6f5", `F:\RulesApp-Local-Input`, "GitHub raw fetch" |
| workflow: auth gate / gated / health-checked / node --check / manifest entry / ledger / GREP tag / Formspree id / HOLD-nn | 11 + 4 + 3 + 7 + 1 + 4 + 1 + 1 | production-status narration |

Two rows (16, 20) had no regex hit but were still tightened for style
consistency (reporter attribution "following candidate feedback", vendor
source names). Every row was reviewed individually — none sampled.

## Review matrix (all 33)

Action key: EDIT = note rewritten, date/files/order preserved. No row was
KEPT verbatim, none REMOVED (row count must stay 33), none HELD.

| # | date | old chars | new chars | internal/privacy classes found | action |
|---|---|---|---|---|---|
| 0 | 2026-08-18 | 2939 | 1800 | chat: WhatsApp/Telegram; person: Nixon; person: candidate name; workflow: auth gate; workflow: node --check; workflow: via <person> | EDIT |
| 1 | 2026-08-13 | 1093 | 811 | person: Nixon; repo: Entry n; repo: commit word; repo: known_traps; repo: source file | EDIT (+files) |
| 2 | 2026-08-13 | 951 | 680 | chat: screenshot; person: Nixon; repo: Entry n; repo: known_traps; repo: source file; workflow: via <person> | EDIT |
| 3 | 2026-08-08 | 724 | 522 | person: Nixon; repo: Entry n; repo: known_traps; repo: source file; workflow: via <person> | EDIT |
| 4 | 2026-08-07 | 1053 | 992 | person: Nixon; repo: Entry n; repo: known_traps; repo: source file | EDIT |
| 5 | 2026-08-07 | 455 | 396 | chat: screenshot; person: Nixon; repo: Entry n; repo: known_traps; repo: source file | EDIT |
| 6 | 2026-08-05 | 589 | 436 | repo: Entry n; repo: known_traps; repo: source file | EDIT |
| 7 | 2026-08-04 | 505 | 372 | repo: Entry n; repo: known_traps; repo: source file | EDIT |
| 8 | 2026-08-04 | 1007 | 713 | chat: WhatsApp/Telegram; repo: Entry n; repo: known_traps; repo: local path; repo: source file; workflow: Formspree; workflow: auth gate | EDIT |
| 9 | 2026-08-03 | 806 | 731 | repo: commit word; repo: commit/SHA; repo: source file; ticket: GAP-/P0-/HOLD-; workflow: ledger | EDIT |
| 10 | 2026-08-02 | 1413 | 1046 | person: Nixon; repo: Entry n; repo: known_traps; repo: source file; workflow: GREP/SKIP tag; workflow: via <person> | EDIT |
| 11 | 2026-08-01 | 1325 | 1231 | person: Nixon; person: candidate name; repo: Entry n; repo: known_traps; repo: source file; workflow: GREP/SKIP tag; workflow: via <person> | EDIT |
| 12 | 2026-08-01 | 910 | 772 | person: Nixon; person: candidate name; repo: Entry n; repo: known_traps; repo: source file; workflow: GREP/SKIP tag; workflow: via <person> | EDIT |
| 13 | 2026-07-30 | 1023 | 786 | person: Nixon; repo: Entry n; repo: known_traps; repo: source file; workflow: GREP/SKIP tag | EDIT |
| 14 | 2026-07-29 | 2176 | 1048 | workflow: auth gate; workflow: manifest entry; workflow: node --check | EDIT |
| 15 | 2026-07-29 | 2464 | 1873 | workflow: auth gate; workflow: node --check | EDIT |
| 16 | 2026-07-29 | 1827 | 1340 | (none by regex; reporter attribution + vendor names) | EDIT |
| 17 | 2026-07-29 | 1144 | 571 | chat: screenshot; person: Nixon; repo: Entry n; repo: known_traps; repo: source file; workflow: via <person> | EDIT |
| 18 | 2026-07-18 | 1036 | 854 | person: Nixon; workflow: manifest entry; workflow: reporter attribution | EDIT |
| 19 | 2026-07-18 | 1060 | 793 | person: Nixon; person: candidate name; workflow: health-check; workflow: manifest entry; workflow: via <person> | EDIT |
| 20 | 2026-07-17 | 300 | 315 | (none by regex; abbreviations expanded) | EDIT |
| 21 | 2026-07-16 | 2035 | 1206 | person: candidate name; repo: known_traps; repo: source file; workflow: health-check; workflow: manifest entry | EDIT |
| 22 | 2026-07-16 | 1409 | 1300 | workflow: auth gate | EDIT |
| 23 | 2026-07-15 | 719 | 557 | person: candidate name; workflow: auth gate; workflow: health-check | EDIT |
| 24 | 2026-07-15 | 910 | 788 | person: Nixon; workflow: auth gate; workflow: health-check; workflow: manifest entry | EDIT |
| 25 | 2026-07-14 | 762 | 480 | person: Nixon; repo: GitHub; workflow: auth gate | EDIT |
| 26 | 2026-07-13 | 341 | 274 | workflow: auth gate | EDIT |
| 27 | 2026-07-13 | 591 | 341 | person: Nixon; repo: GitHub; workflow: manifest entry | EDIT |
| 28 | 2026-07-13 | 641 | 322 | chat: WhatsApp/Telegram; person: Nixon; repo: GitHub; workflow: auth gate | EDIT |
| 29 | 2026-07-05 | 285 | 304 | person: Nixon; workflow: auth gate | EDIT |
| 30 | 2026-07-06 | 281 | 180 | person: Nixon; workflow: manifest entry | EDIT |
| 31 | 2026-07-11 | 902 | 811 | person: Nixon | EDIT |
| 32 | 2026-07-11 | 623 | 333 | repo: source file | EDIT (+files) |

Total note text 34,299 → 24,978 chars. Old and new notes for every row are in
git (`git diff ca881c4 -- tools/oral/qb_content_index_governed.json`); this doc
does not duplicate them.

## Editing rules applied

Kept: what was corrected, which QB page/question, the old and new
regulation/citation/value, why it matters to the candidate, version bumps,
supersession cross-references between rows, examiner surnames where the row is
about the public examiner index (public product context).

Removed: the Founder's name and "via Nixon", candidate first names, WhatsApp /
screenshot / "candidate-flagged" reporter attribution, commit SHAs and the word
"commit", `known_traps.md` and Entry numbers, ledger/json/xlsx/tool paths, local
drive paths, GitHub-raw-fetch chronology, HOLD-nn ids, auth-gate / gated /
health-checked / node --check / tag-balance production status, "this manifest"
housekeeping narration, Formspree form id, "not yet re-gated pending review",
the same-session repo sweeps that produced no correction (row 0's NZF/CSRD sweep).

Technical meaning: no regulation number, date, value or attribution was changed
or added from memory. Every retained fact is a copy of the pre-existing note.
Two positional cross-references were made order-safe ("the other 16 July entry"
instead of "above/below" where the authoring order and render order disagreed).
Row 22 keeps its historical "120-day window" with an explicit pointer to the
same-day refinement in row 21 (IOMOU 90 days), so a candidate reading the older
row is not left with the superseded figure.

## The two free-text `files` rows

| row | before | decision | after |
|---|---|---|---|
| 1 (2026-08-13 DGMA sweep) | `["65 files across meoclass1/, meoclass1/oralnotes/, meoclass1/rulesapp/ -- see known_traps.md Entry 6 for full file-by-file breakdown"]` | **B — truthful scoped label.** Git resolves the two sweep commits (`f6b9cdf`, `d3f2cd5`) to **66** unique content files, not 65, so a deterministic array was possible but would contradict the note's own count and would put a 66-item "Files:" line in front of candidates. Bounded label chosen; the exact list is recorded below for the internal audit trail. | `["meoclass1/ question-bank pages and cheat sheets", "meoclass1/oralnotes/", "meoclass1/rulesapp/"]` |
| 32 (2026-07-11 examiner index) | `["examiner-index.html (new, /meoclass1/)", "examiner-index.html (new, /SQ/ public teaser)"]` | **A — resolved deterministically**; both paths exist on disk. | `["examiner-index.html", "SQ/examiner-index.html"]` |

Row-1 sweep files (66, from `git show --stat f6b9cdf d3f2cd5`, excluding
known_traps / manifest / tooling): 54 under `meoclass1/` (QB10_A, QB10_B, QB1_A,
QB1_B, QB1_B_CheatSheet, QB1_C, QB1_F, QB1_FG_CheatSheet, QB1_G, QB1_H, QB1_I,
QB1_J, QB1_K, QB1_K_CheatSheet, QB1_supplementary, QB2_A, QB2_G, QB2_H, QB2_I,
QB2_I_CheatSheet, QB3_F, QB3_G, QB3_H, QB3_I, QB3_J, QB4_E, QB4_E_cheatsheet,
QB4_G, QB4_H, QB4_I, QB4_J, QB4_J_CheatSheet, QB5_G, QB5_H, QB5_I, QB5_J, QB6_E,
QB6_F, QB6_G, QB6_H, QB7_F, QB7_G, QB7_H, QB7_I, QB8_F, QB8_G, QB8_H,
QB8_H_CheatSheet, QB9_D, QB9_E, QB9_F, QB9_G, QB9_H, QB9_H_CheatSheet — all
`.html`); 11 under `meoclass1/oralnotes/` (miw-notes-mgmt-p1/p3/p5/p6/p7/p9/p16,
simon-notes-p1/p2/p3/p4); `meoclass1/rulesapp/index.html`.

## Guard added

`tools/oral/build_qb_content_index.py`
: `CORRECTION_FORBIDDEN` (25 labelled patterns) + `correction_hygiene_violations()`;
  `check_corrections()` now fails the build on the first hit in `note` or
  `files` of the governed source (`BUILD FAILURE: … candidate-facing hygiene
  violation - person: Nixon: 'Nixon' (3 hit(s) total …)`). Patterns are
  explicit regression controls from this dataset, not NER: the two candidate
  first names and the Founder's name are literal; SHA regex requires both a
  letter and a digit so plain numbers never match; "branch" and "manifest" are
  deliberately NOT banned (DGMA Maritime Health Branch, cargo manifest);
  examiner surnames are allowed.

`tools/oral/validate_qb_content_index.py`
: +`hygiene` (same function on the rendered manifest, so a generator that
  re-admits a stale note is caught downstream) and +`note_quality` (min 40
  chars and at least one page/regulation/verb token — "Content updated." fails)
  → **24 checks**.

`tools/oral/mutate_qb_content_index.py`
: +S "via Nixon", +T WhatsApp, +U commit SHAs, +V `known_traps.md Entry 6`,
  +W GAP-/P0-, +X blank note, +Y pre-cleanup unsafe note restored verbatim,
  +Z hygienic-but-empty note → **26 mutations, 0 escapes**, each caught by its
  named check, none by crash.

## Gates

| gate | result |
|---|---|
| `validate_qb_content_index.py` | 24 / 0 FAIL |
| `mutate_qb_content_index.py` | 26 run / 0 escapes |
| generator fail-closed on the governed source | BUILD FAILURE (rc 2) on injected "via Nixon, WhatsApp" |
| determinism `PYTHONHASHSEED` 0 / 1 / 524287 | manifest `4a528e06…`, index.html `0f7d8c3a…` identical |
| `meoclass1/index.html` | **byte-unchanged** (log is fetched from the JSON at runtime; `Q_INDEX` untouched → search index logically unchanged, no note is a question result) |
| `qb_health_check.py` changelog-gap set | **27 before, 27 after, same files** — the gap check scans QB filenames in `note` and every rewritten note kept its page references |
| rendered log, chrome-devtools on a local origin | 33 rows, 0 blank, 0 `undefined`, 0 raw arrays, 33 unique, 0 leaks (client regex), 33 "Files:" lines; desktop and emulated 375×812: 0 overflowing rows, no horizontal document scroll |
| `test_oral_controls.py` / `test_notes_controls.py` / `test_qb_question_text.py` | 315/0, 106/0, 7147/0 |
| `validate_examiner_index.py` / `build_examiner_index.py --check` | 52/0, nothing written |
| `deploy_surface.test.mjs` | 92/92 |
| `git diff --name-only origin/main` ∩ `QB*.html` | none |

## Debt found, not actioned (unchanged from prior records)

1. 27 changelog gaps (`qb_health_check`) — unchanged by this pass, by design.
2. Row 0 remains long (1,800 chars) because the CSR/GBS card carries several
   distinct corrections; it wraps inside the log's own scroll container. If a
   shorter public log is wanted, that is a UI/format decision, not editorial.
3. QB2_C q1 answer's visible `⚠CORRECTED` production marker (candidate-visible,
   separate).
4. Held STRONG_CE_TIP pairs, QB_GROUPS drift, Last Updated, tier literals — all
   out of scope here.
