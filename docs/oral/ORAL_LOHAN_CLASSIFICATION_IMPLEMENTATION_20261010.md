# Oral Notes - LOHAN source-series classification (implementation record)

Date: 10 October 2026. Status: LOCAL CANDIDATE ONLY. Base: `d8b48e8` (production).
Qualified against: `43441b7` (LOHAN D-L4 post-CA4W candidate, 21 LOHAN pages).

Not authorised and not done: publication, push, deploy, canonical integration,
POST31 source admission, production manifest activation, any learner-page change.

## What changed

| File | Change |
|---|---|
| `tools/oral/oral_notes.py` | `SERIES_LOHAN = "LOHAN_SOURCE_NOTES"`, series code `LOHAN`, manifest key `lohan-notes`, dialect `_lohan_units` (delegates to the management topic-block parser). A manifest series key the model does not know now yields an `UNCLASSIFIED` row instead of a `KeyError` at import. |
| `tools/oral/test_notes_controls.py` | Section 9: 13 new controls (fixture-backed and real-tree). 106 -> 119 controls. |
| `tools/oral/mutate_phase2.py` | Code mutations M30-M32 for LOHAN. The harness now counts a code mutation as caught only when it adds a failing control the unmutated tree does not already have (see "Harness fix"). |

No manifest, learner page, generated artefact or `tools/notes` file is touched.

## Classification design

- Series is manifest-driven, as for every other series: a page is LOHAN if and
  only if `notes_content_index.json` lists it under `lohan-notes`. Until D-L4
  activates that key, the 21 pages stay `UNCLASSIFIED` and the existing
  "every notes page is classified" control reports them. That is correct
  behaviour, not a defect.
- Dialect: LOHAN pages use the management topic-block / `qa-item` / `exam-q`
  markup. Parsing is shared with `_mgmt_units` but dispatched through its own
  entry so identity (code, namespace, manifest key) is LOHAN's alone.
- Independent parser verification (raw HTML counts against parsed units, all 21
  pages): `topic-block` count equals parsed topics on every page; `qa-item` +
  `exam-q` equals parsed children on every page; no unit lacks an anchor or a
  title; no `note-card`, `section-h` or `q-text` structures that another
  dialect would claim. 123 topics + 324 Q&A + 8 exam prompts = 455 units.

## Identity safety

LOHAN unit ids are `NOTE-LOHAN-P<n>-...`. Measured over the full 1,693-unit
universe (scratch, manifest activated): 0 duplicate ids; 0 collisions with the
761 canonical QB ids; 0 canonical-shaped ids; 0 ids carrying a MERGE / PCT /
CAND / CANON token; 0 non-LOHAN ids in the `NOTE-LOHAN-` namespace; all 21 LOHAN
page numbers also exist as management pages (P1-P21) and no id collides.
The 1,238 pre-existing units are byte-identical (per-unit hash) with and without
LOHAN admitted; the only classification change is 21 pages
`UNCLASSIFIED` -> `SUBSTANTIVE_NOTES / LOHAN_SOURCE_NOTES`.

## Known failure: ME-GI / ME-GA

`no Oral Note text exercises the ME-GI / ME-GA family` fails at `d8b48e8`
already, and still fails with LOHAN present. LOHAN P20 does not clear it: it
adds ME-GI text (2 units) and no ME-GA text, and the control is an absence
assertion that Uday P25 and P29 already violate. It is a stale precondition,
not a coverage gap, and was left untouched.

## Harness fix

`mutate_phase2.py` treated "controls exit non-zero" as "mutation caught". With
a standing failure on the baseline every code mutation passed that test
vacuously. It now runs the unmutated copy first and requires a new failing
control. Result on the same code: all 7 pre-existing code mutations stay caught
with 2-51 new failures each.

## Handoffs (other owners; nothing done here)

1. D-L4 / Notes metadata: activation must add `lohan-notes` (21 files) to
   `notes_content_index.json` and set `total_files` 40 -> 61. `qb_health_check`
   is series-agnostic; with the key present its "files on disk but not listed"
   finding for the 21 pages clears (two older, unrelated entries remain).
2. Oral artefacts: after activation the six `ORAL_NOTES_*` artefacts must be
   regenerated with `ingest_oral_notes.py`. They are already stale against the
   generator before LOHAN (explicit cues 500 committed vs 585 regenerated, from
   the Uday parts admitted since). LOHAN itself adds 0 explicit examiner cues
   and changes the Notes support tier of 66 of 788 source asks (secondary
   layer only; no canonical relation changes).
3. Study owner: `build_study_spine.py` reads only the `total_files` scalar, so
   bumping it requires regenerating the spine and the `RulesApp/study/app`
   data bundle. The builder could not be run in a clean checkout (needs an
   untracked `sixyear_families.json`), so this is a static finding.
4. Notes owner: the ME-GI / ME-GA absence control needs a decision (retire or
   restate); out of scope here.
