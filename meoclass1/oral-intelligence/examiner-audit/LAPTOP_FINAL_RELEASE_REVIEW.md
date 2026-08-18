# Laptop independent final release review — oral examiner intelligence

**Review branch:** `review/oral-examiner-intelligence-v1-final-release`, cut from
`research/oral-examiner-intelligence-v1-phase2a-iii` @ `d767158`.
**Method:** cross-drive worktree on `C:` against a repository on `F:`. Every gate re-run,
every headline count recomputed from records, no live product file touched.

**Verdict: GO**, with Release A reduced from 136 to **134** and four bounded pre-flight
conditions that land inside Stream A.

---

## A. Repo truth — the brief and the Desktop report are both stale

| Ref | Expected | Actual |
|---|---|---|
| `origin/research/...phase2a-iii` | `d767158` | **`d767158`** ✓ |
| `...phase2a-ii` / `-i` | `f9c5a12` / `85035ba` | ✓ / ✓ |
| `...reconcile` | `de6d3f2` | ✓ |
| `review/...phase2` | `c78a228` | ✓ |
| **`origin/main`** | `88bd1a6` (Desktop) | **`e3cb47a`** |

Main moved **again** after the Desktop wrote its report. The delta is `3b55bfb..e3cb47a`,
five commits, eight files. `88bd1a6` is an ancestor, not the tip.

## B. Gates reproduced independently — all green

| Gate | Reported | Reproduced |
|---|---|---|
| `validate_phase2.py` | 91 / 0 | **91 PASS / 0 FAIL** |
| `test_oral_controls.py` | 315 / 0 | **315 / 0** |
| `test_notes_controls.py` | — | **106 / 0** |
| `mutate_phase2.py` | 33 / 0 escapes | **33 / 0 escapes** |
| `check_determinism.py` | 26 / 0 | **26 / 0 at seeds 0, 1, 524287** |

Mutations fail **semantically**, not by crashing: each reports a control/validator failure
count (M11 → 51 control failures, M10 → 14, M25/M26 → 90 PASS / 1 FAIL), never a traceback.
Determinism holds **cross-drive**, which independently confirms the
`ORAL_NOTES_INVENTORY.json` `st_size` → LF-normalised-bytes portability fix.

## C. Data accounting — every headline number reproduces exactly

- **788** source occurrences → **788** dispositioned rows, a strict bijection: no duplicate
  ids, no dropped records, no added records. John 129 / Simon 256 / Nair 300 / Paul 103.
- **681** canonical questions (unique ids), **992** Notes units, **731** source families.
- Dispositions: EXACT 22 · NEAR 40 · SAME_CORE 24 · PARTIAL 369 · MISSING 218 · AMBIGUOUS 115.
- Notes support: COMPLETE 153 · STRONG 83 · PARTIAL 320 · TOPIC 177 · NONE 55.
- Movement: 135 disposition-changed + 208 target-only + 445 unchanged = 788. 343 moved.
- Human review: 115 = 74 two-target + 41 terse.
- Every final target resolves — **zero orphan references**.

**One presentational caveat:** the reason ladder (SAME_CORE_FLOOR 51 … HUMAN_ADJUDICATION 3)
sums to **135** and explains the disposition changes only — not all 343 moved rows. The
report's table placement invites reading it as explaining 343.

**OTHER_EXPLAINED sampled (21/21):** every one keeps the *same* target and moves on score
alone. Nothing is hidden in that bucket. **EXACT/NEAR target changes: 0** — no
high-confidence pair was silently re-pointed.

**Designator repair re-proved on full stems (8/8):** ME-GI≠ME-GA, ME-GI≠ME-LGI, III/1≠III/2,
Form A≠Form B, D-1≠D-2, G8≠G9 all conflict; Annex VI≡Annex 6 and ME-GI≡itself do not.

## D. Release A — 136 proposed, 134 approved, 2 held

All 136 validated structurally by an independent checker: unique pairs, targets in the 681,
**anchors verified present in the live HTML**, examiners resolve, no ambiguous/SAME_CORE/
MISSING-only row admitted. Composition confirmed: PRIMARY_TRACKER 84 / EXTERNAL 52; Simon 59,
Nair 39, Paul 16, John 11, Rajappan 9, Senthil 1, Srivastava 1.

### D1. Traceability defect — `evidence_ids` is empty on **all 136** rows

Two validator checks — *"every Release-A evidence id resolves"* and, for 76 rows, *"every
Release-A source occurrence resolves"* — therefore pass **vacuously**. The evidence is real; I
traced all 136 by hand to `EXAMINER_EVIDENCE_LEDGER.jsonl` / `READY_CONNECTIONS_V2.json` /
the 788. But the release artefact cannot be audited standalone, and Stream A is supposed to
generate the published index *from it*. **Repair before generation: populate the pointers.**

### D2. Provenance of the 76 source-less rows — sound

45 carry `MASTER_TRACKER_PRIMARY`, 31 carry a corroborating 788 occurrence **of the same
examiner** (zero examiner mismatches). **Zero rows rest on page-declared CE-tip prose alone.**

I initially read the 16 `JULY-NEW`-evidenced rows as a page scrape (their `Full Answer` column
reads "Read Full Answer →"). The ledger settles it: they are
`MIW_July2026_QuestionBank_SHARE.xlsx#New Questions (July 2026)`, classed
`PRIMARY_CANDIDATE_RECORD`. The *per-examiner* July sheets are separately and correctly classed
`DERIVED_PRODUCT_SURFACE` (828 rows). The tier claim is defensible.

**What does survive:** the July sheet links at **file level** (`QB1_K.html`, no anchor), so for
7 rows the *anchor* is inferred. Five are unambiguous (near-verbatim wording match). Two are not:

| Pair | Examiner ask | Chosen target | Verdict |
|---|---|---|---|
| `RELA-SIMON-QB9_H-q11` | "What is Act, Merchant shipping act?" | *Definitions of casualty as per the MS Act* | **HOLD_TARGET** — only MS Act question on the page, but the demand differs; studying casualty definitions does not prepare "what is the Act" |
| `RELA-NAIR-QB1_K-q5` | "difference between type 1 and type 2?" | *Difference between DP-1 and DP-2* | **HOLD_TARGET** — "type 1/2" is not "DP-1/2"; this is the terse-fragment shape Phase 2A-i refused to force elsewhere |

**Authorised Release A = 134.**

## E. P0 — all 9 reviewed, all 9 approved as classified

Absence claims re-tested against the corpus, scanning **answers** as well as question text:

- **No canonical question** covers BWM / BWTS / D-2 / G8 / G9 (only two ballast-*tank-inspection*
  questions). `G9` appears **nowhere** in 124 QB files. → **P0-0016** and **P0-0410** are real.
- `QB5_B`'s apparent "D-2" hits are **false positives** — Situational Leadership *D2 development
  level*. `QB9_E`'s BWTS mention is incidental (Blue Economy prose). Neither answers D-2 onboard
  verification.
- **GIRDING** appears in no canonical question; `simon-notes-p2.html#n9` exists and the series
  carries "Tug Girding". → promotion approved.
- `QB3_C#q3` **is** *"Hong Kong Convention — IHM three parts and CE role?"* → **GAP-0494 is NOT A
  GAP**; the Desktop's correction of the prior Laptop review is upheld.
- `QB7_I#q2` **does** cover *both* the ME-GI and ME-GA families → **GAP-0409 = enrichment**.
- `QB5_B#q4` **is** *"CE as Leader — Leadership Theories"* and contains **zero** occurrences of
  "assertive" (empathy appears only as a Goleman EI competency) → **GAP-0043 enrichment limb
  confirmed: assertiveness, plus empathy as a CE quality.**
- `QB6#q10` is dual-fuel; **"trifuel" appears nowhere in the corpus** → **GAP-0034** limb confirmed.
- `QB1_supplementary#q20` **is** *"Tail Shaft Survey"* → the prior review's reuse pointer was
  wrong, as the Desktop states.

**One condition on P0-0016.** `QB1_A#q30` ("MEPC 84 Outcomes") already carries substantial BWM
material — Regulation D-2.3, E-1.4.3, the 2016 G8 / BWMS Code unified interpretation, D-3. The
new answer is still justified (that card is a regulatory-update surface, not a Convention content
answer, and G7/G9 are absent), but Stream B **must cross-link `QB1_A#q30` rather than restate
MEPC 84**.

## F. Retiering — approved

2 invalid-literal repairs (`cetip` → `ce_tip`) · 195 proposals · **31 demotions from `confirmed`**
(28 → `ce_tip`, 3 → `inferred`), each resting on a derived sibling with `primary_evidence_count: 0`
· **29 promotions to `confirmed`, every one with `PRIMARY_CONFIRMED` provenance and ≥1 primary
record** · **0 unsupported promotions.** The M5 escape class is closed. `oral_provenance.py` is
correctly designed — `PRIMARY_TRACKER` admits only `{PRIMARY_TRACKER, MASTER_TRACKER}`, and the
July sheets are explicitly derived.

**Authorise the honest re-tiering including all 31 demotions.** The live index over-claims on
those rows; truth over historical counts.

## G. Display text — 10, not 9

The 8 `QB5_C_B` rows and `QB7_B#q2` all verify on live main. An independent sweep of all 124 QB
files on `origin/main` confirms the predicted **10th**: `QB1_K#q8`, whose candidate-facing text is
`(Simon sir) "What is CSR?" — what does he mean, and what is its scope?`.

`FINAL_DISPLAY_TEXT_FIX_SET` = the 9 candidates **plus** `QB1_K#q8`. Metadata to preserve
separately: examiner name and confidence (`QB1_K#q8` already carries `data-examiner="Simon"
data-examiner-confidence="confirmed"`). `QB7_B#q2` needs authoring, not stripping — removing the
name leaves prose that is still not an ask.

## H. Current main delta — no material impact on the 788

`3b55bfb..e3cb47a`: `QB1_K.html`, `QB1_K_CheatSheet.html`, `examiner-index.html`, `index.html`,
`qb_content_index.json`, `qb_health_check.py`, `known_traps.md`, `docs/miw-qb-index-linkage_SKILL.md`.

**The 682nd question is `QB1_K#q8` (IACS Common Structural Rules).** Tested against all 788 source
occurrences: **zero** mention CSR or common structural rules. Therefore **no new matches, no changed
targets, no changed dispositions, no Release-A impact, no P0 impact.** → **Decision A.** Do not
re-run the 788. Cherry-pick/rebase during generator integration.

Note the trap for Stream A: `QB1_K#q8` is *IACS CSR*, while `QB5_C_B#q8` is *Continuous Synopsis
Record*. Two different CSRs, one acronym.

### H1. New live defect neither review reported

The hand-edit to `examiner-index.html` raised Simon 243 → 244 and inserted a `confirmed` row, but
**did not update the tier sub-count**:

| Examiner | header | actual rows | header confirmed | actual confirmed |
|---|---|---|---|---|
| **Simon** | 244 | 244 | **148** | **149** ✗ |
| Nair / Rajappan / Srivastava / Senthil / Paul | — | — | — | consistent |

Live, candidate-facing, introduced by `88bd1a6`. The V2 generator fixes this structurally (every
count is `len()`), so it needs no separate repair — but it is one more demonstration that
hand-maintained counts drift. Other examiners preserved and verified intact: **Rajappan 93,
Srivastava 103, Senthil 66** — exactly as reported. Total rendered rows 864.

## I. Governance

**Research tree:** the 76 research files exist **only on the research branch — zero files on
`main`**, so nothing is deployed today. `.vercelignore` has no `oral-intelligence` entry, so the
exposure would be created *by the merge*, not by the current state. Recommendation **A**: add the
`.vercelignore` entry as part of the Stream A integration commit. Not a release blocker.

**Raw source governance:** the committed 788 wording contains **no** emails, phone numbers, URLs,
WhatsApp metadata or candidate identifiers. `vessel` holds 19 generic ship *types* ("Container",
"LNG Carrier"). Risk: **low**.

**But — an unignored raw source file.** `.gitignore` covers `docs/MIW-master-Question-bank/*.xlsx`
and **not `.docx`**, leaving `docs/MIW-master-Question-bank/All Surveyors Class1 Oral Questions.docx`
untracked *and* unignored in a **public** repository. A `git add -A` in a production session commits
a third-party compilation. **Fix the pattern before Stream A or B commits anything.**

## J. Generator spec — approved as written

It already requires everything the brief demands: every count derived by `len()`, no hand-entered
literal, display text taken from the **live question** (which structurally ends the display-text
class), both `meoclass1/` and `SQ/` emitted from **one** data pass, unresolvable relationship =
build failure, tier literal without a filter toggle = build failure, July sheets never raise a tier.
`EXTERNAL_SOURCE_CONFIRMED` maps to **"Reported"** — exactly the treatment John's 11 pairs require.

**Reverse "Asked by" connections: POST-RELEASE FAST FOLLOW.** The spec already names it as a later
output of the same pass; cheap once the pass exists, but not worth risking 24 August.

## K. Pre-flight conditions (all inside Stream A)

1. Drop the 2 held Release-A pairs → publish **134**.
2. Populate `evidence_ids` / `source_occurrence_ids` on Release-A rows before generation.
3. Apply the **10**-item display-text fix set before the index is regenerated.
4. Extend `.gitignore` to `docs/MIW-master-Question-bank/*.docx` before any commit.

## L. Untouched

No QB HTML, Oral Note, `examiner-index.html`, SQ page, payments, homepage, Written QI or magazine
file was modified. `main` was not moved. Nothing was published. No P0 answer was written. The
research branch was not rebased.
