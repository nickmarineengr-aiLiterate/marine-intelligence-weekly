# QB2_C q1 — candidate-visible "⚠CORRECTED" marker cleanup

Post-Release-A fast-follow, 2026-08-19. Closes the debt left open by
`QB2C_CANDIDATE_TEXT_REPAIR.md` §"Left alone" (answer-body production markers).

## Repo truth

Started from `origin/main` `e6c94ce` (moved from the briefed `3de74d4` by three
commits — QB3_H PSA/PSSA fix, PSSA currency pass, teaser circular fix — none of
which touched `QB2_C.html`, the content-index generator or the examiner
generator). Branch `fix/oral-qb2c-q1-corrected-marker-cleanup`.

## Marker inventory (all four occurrences were the same token)

| # | location in q1 | rendered text | technical statement underneath | marker value | action |
|---|---|---|---|---|---|
| 1 | 15-Second Answer | `MSC.520(106) and ⚠CORRECTED: MSC.532(107), entering into force 1 January 2026` | both resolutions in force 1 Jan 2026 | none | REMOVE_MARKER |
| 2 | 60-Second Answer | `Resolution ⚠CORRECTED: MSC.532(107) enforces a complete ban ... PFOS` | PFOS ban is MSC.532(107) | none | REMOVE_MARKER |
| 3 | h5 "2. Prohibition of PFOS-Based Firefighting Media" | `(Resolution ⚠CORRECTED: MSC.532(107))` | same | none | REMOVE_MARKER |
| 4 | reg-box `reg-code` | `Resolution ⚠CORRECTED: MSC.532(107)` | reg-desc: global ban / carriage prohibition of PFOS foams | none | REMOVE_MARKER |

The marker carried no contrast or exam point — only the fact that a number had
been substituted upstream (it is present in the very first upload `30b866f`,
so it predates the repo). It was replaced by the plain number in all four
places. No label was added because the surrounding prose already carries the
distinction (MSC.520(106) = flashpoint declaration / BDN; MSC.532(107) = PFOS).

## Technical verification

Corpus record `Knowledge Central/FSS/FSS_CODE_CORPUS/amendments/2026-01-01_CHANGES.md`
(verified via UK MGN 713(M), DNV, KR): MSC.532(107) → SOLAS II-2/1.2.10 and
10.11, PFOS > 10 mg/kg prohibited, new ships on delivery, existing ships by
first survey on/after 2026-01-01, media landed ashore; MSC.520(106) → SOLAS
II-2/3.59–3.61, 4.2.1.6–4.2.1.8, flashpoint declaration before bunkering, BDN
states measured value or ≥ 70°C. Both in force 1 January 2026. Five other live
QB pages (QB1_K, QB2_F, QB2_I, QB10_B) attribute PFOS to MSC.532(107) the same
way. The card's framing stays aligned to the repaired question (asks about
MSC.520(106) and entry into force; answer leads with MSC.520(106) and names
MSC.532(107) as the concurrent PFOS instrument, never conflating them).

## Contract proven

- q1 question text byte-identical; anchor `q1`; `data-tags` unchanged.
- q2/q3/q4 full-card sha256 identical before/after.
- Semantic diff of the q1 answer region = exactly four deletions of the token
  `⚠CORRECTED:`; nothing else.
- q1 answer hash re-pinned in `tools/oral/test_qb_question_text.py`
  (`5740f51f…` → `44003998…`), stated in the commit.
- New controls: no production/editorial marker in any QB2_C answer region
  (`MARKER` regex, visible text); q1 keeps MSC.520(106), MSC.532(107),
  1 January 2026, PFOS, 60°C, 70°C. Mutations H–K added (marker back, editorial
  note in answer, corrected statement deleted, q2 modified): 11 run, 0 escapes.
  Pre-edit QB2_C fails the new control (`found '⚠CORRECTED'`).

## Gates

q-text gate 7157/0 · content index `--check` matches disk, validator 24/0,
mutations 26 run / 2 escapes (S, U — **pre-existing on origin/main**, verified
in a clean worktree) · examiner build (full write) zero diff on
`examiner-index.html`, `SQ/examiner-index.html`, `SQ/index.html`, snapshot;
validator 52/0 · oral controls 315/0 · notes controls 106/0 ·
check_determinism 26/0 (dirties ORAL_NOTES_IMPACT.md — reverted) ·
deploy_surface 92/92 · link_integrity 20/20 · qb_health_check 181 findings on
both branch and origin/main (baseline-identical). No SQ file changed.

UI (chrome-devtools, `file://` with the client `miw_auth` gate stubbed):
desktop 1280 and emulated 375×812 — no marker, no card/answer/reg-box
overflow, all four cards direct children of `#q-feed`.

## Marker sweep elsewhere (report only, not fixed)

- `QB2_B.html` + `QB2_B_CheatSheet.html`: `⚠ Q10 corrected: water monitor
  flow = 400 L/min` banners (header, sidebar note, footer, cheat-sheet alert).
- `QB6.html` q3/q4/q5: `<span class="tag-correction">CORRECTED: …</span>` in
  q-version and inside one answer.
- `QB4_E.html`: answer prose "Fixed in Legal Framework para, Numbers/Regs box…"
  (a production note inside candidate text).

## Left alone

10 held STRONG_CE_TIP pairs · 27 changelog gaps · 43 tier literals · reverse
Asked-by · Last Updated · QB_GROUPS drift · legacy client cookie gate ·
master XLSX v26/July SHARE (→ v27 / August SHARE later).
