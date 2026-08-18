# P1 follow-up candidates — observed during Oral P0 production

Recorded, **not repaired**. No live QB edit was made for anything on this list; the
P0 batch was held to exactly nine items. Each entry states what was seen and where.

Observed on branch `prod/oral-p0-pre24aug`, cut from `origin/main` @ `0242774`.

---

## A. Consequences of this batch that Laptop must action

These are not defects in the P0 content — they are the mechanical downstream effect
of adding six canonical questions. They are listed in full in
`P0_PRODUCTION_HANDOFF.md` §4 and repeated here only so the debt is visible in one
place.

1. **Examiner index snapshot is stale** against the new anchors — regeneration
   required.
2. **`QB6#q10` and `QB5_B#q4` rendered display text** no longer matches the live
   question text, because both question texts were widened by the approved
   enrichments.
3. **SQ storefront oral-question figure** reads 682; the corpus is now **688**.
   `SQ/index.html` is a forbidden surface for Desktop, so this was deliberately left
   alone. Three of the five `validate_examiner_index.py` failures are this one fact.

---

## B. Pre-existing findings, unrelated to this batch

Confirmed present on `origin/main` before any edit in this session — the baseline
capture showed **104 error groups**, unchanged by this batch.

4. **`QB4_A_CheatSheet.html` — a hard known-trap hit.** The health check reports
   `KNOWN TRAP resurfaced: "A.1185(33)" found in visible text`. Unlike the many
   `[REVIEW]` advisories elsewhere, this one is not flagged as sitting in a
   negation/correction context, so it may be a genuine resurfaced superseded
   reference rather than a correctly framed supersession note. Worth one look
   against `meoclass1/known_traps.md`.

5. **Two `oralnotes/` files are in neither notes manifest.**
   `solved-qp-january-2026-full.html` and `written-sample-january-2026.html` are on
   disk but listed in neither `notes_content_index.json` nor
   `written_content_index.json`. The health check reports them as orphans. They look
   like Written/sample surfaces that landed without a manifest entry.

6. **Widespread changelog gaps in `qb_content_index.json`.** Roughly 90 of the 104
   baseline error groups are of the form *"file X is named in the YYYY-MM-DD
   `recently_updated` summary but has an empty `corrections_applied` array"*. The
   file entries simply have no `corrections_applied` key. Either the checker's
   expectation or the manifest convention has drifted; one of the two should be
   settled, because the volume of advisory noise currently makes a real regression
   easy to miss. This is the reason this session validated by **diffing against a
   captured baseline** rather than by reading a pass/fail result.

7. **`qb_health_check.py` cannot validate a branch.** It only ever fetches
   `codeload.github.com/.../refs/heads/main`, so nothing can be gated before merge.
   A local-tree mode (or a small harness like the one used in this session, which
   imports the real checkers and substitutes only the file source) would let
   production branches be validated before they reach main. Recommended as a
   tooling P1.

---

## C. Explicitly NOT touched — separate known debts

Named in the brief as out of scope and left entirely alone:

- the 10 `STRONG_CE_TIP_ASSERTION` held examiner pairs
- the four `QB2_C` cards carrying answer scaffolding as question text
- research-tree relocation and the `.vercelignore` entry
- the broader 115-item human-review queue
- reverse "Asked by" badges
- Written QI

Also untouched, per the brief: the matcher and evidence architecture
(`tools/oral/*`), `examiner-index.html`, `SQ/`, payments, `pastpapers/`,
`articles/`, magazine, and Release-A data.

---

## D. Items demoted during adjudication — no action taken

Carried forward from `FINAL_P0_PRODUCTION_BATCH.md` for continuity only:
GAP-0009 (terse STCW designator fragments → human review), GAP-0069 (TIO2 — a
label, not an ask), GAP-0093 (single occurrence, topic-level notes only), GAP-0494
(not a gap — `QB3_C#q3` covers it; the residual limb is who performs the initial
survey, an enrichment).
