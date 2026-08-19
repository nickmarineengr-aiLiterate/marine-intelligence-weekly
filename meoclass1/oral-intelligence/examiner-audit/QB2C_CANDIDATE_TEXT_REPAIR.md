# QB2_C candidate-question text repair — 2026-08-19

Post-Release-A fast-follow. Closes the first item of the P0 fast-follow debt
list (`P0_LAPTOP_REVIEW_RECORD.md` §8.1, `P1_FOLLOWUP_CANDIDATES.md` §C):
four live `QB2_C` cards whose candidate-facing question text was answer
scaffolding rather than a question. Display-text-only. No answer, anchor,
examiner adjudication or held pair was touched.

## Defect

`meoclass1/QB2_C.html` has exactly four q-cards and all four were defective
from the file's first commit (`30b866f`, 25 Jun 2026 "Add files via upload");
no clean wording ever existed in git history.

| Anchor | Text as shipped | Class |
|---|---|---|
| q1 | `EDITORIAL CORRECTION:** MSC.520(106) covers SOLAS Ch II-2 fire safety for container ships (water mist lance, portable wa` | PRODUCTION_METADATA — a truncated (120-char) editorial note with a stray markdown `**` |
| q2 | `15-Second Answer (Elevator Pitch)**` | ANSWER_SCAFFOLDING — the practice-block label of the source note |
| q3 | `15-Second Answer (Elevator Pitch)**` | ANSWER_SCAFFOLDING |
| q4 | `15-Second Answer (Elevator Pitch)**` | ANSWER_SCAFFOLDING |

Because live HTML is the truth, the same four strings had propagated into
`qb_content_index.json`, the hub `Q_INDEX` (search), the Examiner Index V2
snapshot / `examiner-index.html` (8 rows: Simon ×4, Senthil ×4) and the SQ
teaser build.

## Evidence used to recover the intended question (in the governed order)

1. **The card's own answer** — every card opens with a 15-second block that
   restates the ask (q1: MSC.520(106) amendments in force 1 Jan 2026; q2: "My
   approach as Chief Engineer" to an undeclared-DG container fire; q3: fighting
   a container fire with unknown cargo; q4: water mist lance + portable monitor
   construction / working / SOLAS II-2/10.7.3.1).
2. **Sidebar TOC** (already clean): "SOLAS Ch II-2 Latest Amendments
   (MSC.520(106))", "Undeclared DG Fire — CE Approach", "Container Fire —
   Unknown Cargo", "Water Mist Lance & Portable Water Monitor"; and the
   page sub-description listing the same four topics.
3. **Sibling artefact from the same production run** —
   `QB2_C_CheatSheet.html` carries short question forms for the same four
   cards ("Undeclared DG fire — CE approach?", "Container fire, unknown cargo —
   how to fight it?", "Water mist lance and portable water monitor?").
4. Examiner records — `EXAMINER_INDEX_SNAPSHOT.json` ties all four to Simon
   (ce_tip) and Senthil; the CE tips name Nair as the asker. No text there is
   independent of the live page.
5. Tracker — `All Surveyors Class1 Oral Questions.docx` has "Container fire
   fighting latest amendment" and "Container fire fitting, mobile water monitor,
   working, design … water mist lance"; the two master XLSX files carry no
   QB2_C rows.
6. Git history — never clean (see above).

## Repairs applied (all HIGH confidence, 4/4)

| Anchor | New candidate-facing text |
|---|---|
| q1 | What are the latest amendments to SOLAS Chapter II-2 under MSC.520(106), and when do they enter into force? |
| q2 | How would you, as Chief Engineer, approach a fire in a container carrying undeclared dangerous goods? |
| q3 | How would you fight a container fire when the cargo inside is unknown? |
| q4 | Explain the water mist lance and portable water monitor — their construction, working, and the SOLAS carriage requirements. |

Answer regions (`q-answer` … `q-footer`) are byte-identical before and after
(sha256 pinned in `tools/oral/test_qb_question_text.py`); the "card minus
q-text" hash was also identical for all four. Anchors q1–q4, ids, tags,
examiner metadata, TOC and footers unchanged. The QB2_C diff is 4 lines.

## Derived surfaces regenerated (generator only, no hand edits)

- `tools/oral/build_qb_content_index.py` → `qb_content_index.json` (4 text
  records) and `index.html` `Q_INDEX` line. 688 questions / 86 files unchanged.
- `tools/oral/build_examiner_index.py` → `EXAMINER_INDEX_SNAPSHOT.json` and
  `examiner-index.html` (8 rows). SQ files: no byte change (the teaser does not
  carry these rows).

## Permanent controls added

- `build_qb_content_index.LEAK` now also rejects `N-Second Answer`,
  `Elevator Pitch`, `EDITORIAL CORRECTION`, `Full Answer`, `CE Tip`, `REG-BOX`,
  `Why this matters`, `On my vessel`, `P0-n` and markdown `**` in any live
  q-text (the generator FAILS, it does not scrub). Corpus sweep before adding:
  the four QB2_C cards were the only hits in 688 q-texts.
- New gate `tools/oral/test_qb_question_text.py` (7,147 controls over 86
  pages, 0 failures): scaffolding-free q-text (its own regex, independent of
  LEAK), no dangling `**`, QB2_C approved wording pinned, the four old strings
  may not return anywhere, QB2_C answer hashes pinned, unique ids/anchors,
  and a **real `html.parser` DOM walk** — every q-card must be a direct child
  of `div#q-feed` (never the sidebar), own one `q-header` + one `q-answer` as
  direct children and contain a `q-footer` (two live templates put the footer
  either directly in the card or at the end of `q-answer`).
  `--mutate` runs 7 mutations on scratch copies (restore old text, inject
  "Examiner context", edit answer body, change anchor, duplicate id, close
  `#q-feed` early, editorial-note prefix) — 7/7 caught, none by crash. Run
  against the pre-repair file from `origin/main`: 20 failures.
- `mutate_qb_content_index.py` mutation R (restore the scaffolding text in the
  manifest + Q_INDEX) → caught by `leak` / `text`. 18/18 mutations caught.

## Gates run on the branch

validate_qb_content_index 22/0 · mutate_qb_content_index 18 run / 0 escapes ·
validate_examiner_index 52/0 · mutate_examiner_index 13/0 · build_*
`--check` clean · test_oral_controls 315/0 · test_notes_controls 106/0 ·
check_determinism 26 artefacts identical (seeds 0/1/524287) · content index
byte-identical under PYTHONHASHSEED 0/1/524287 · deploy_surface.test.mjs 92/92
· 970 fragment links checked, 0 broken · qb_health_check (local-tree harness)
identical to `origin/main` after sort — same 27 changelog gaps · validate_audit
still reports the pre-existing 43 invalid tier literals only.

Mobile (375 px): the four headings wrap cleanly, no q-text/card overflow, all
cards under `#q-feed`; the topbar `<nav>` still overflows 375 px by ~23 px —
pre-existing template chrome, untouched.

## Left alone (separate debts, unchanged)

Answer bodies including the `⚠CORRECTED: MSC.532(107)` production markers
inside the q1 answer/reg-box (candidate-visible, answer content, out of this
scope); the 10 held STRONG_CE_TIP pairs; reverse Asked-by; correction-log
prose; 27 changelog gaps; QB_GROUPS drift; Last Updated; 43 tier literals;
master XLSX (v26 / July SHARE) — regenerate later as v27 / August SHARE.
