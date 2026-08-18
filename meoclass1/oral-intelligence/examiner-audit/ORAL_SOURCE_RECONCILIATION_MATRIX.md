# Oral Source Reconciliation Matrix

**Date:** 18 August 2026 · **Branch:** `research/oral-examiner-intelligence-v1-audit`

Five sources were compared. None is canonical for everything; each is canonical for something.

---

## 1. The five sources side by side

| | **LIVE QB HTML** | **qb_content_index.json** | **MASTER XLSX** | **JULY XLSX** | **EXAMINER INDEX** |
|---|---|---|---|---|---|
| **Path** | `meoclass1/QB*.html` (86 files) | `meoclass1/qb_content_index.json` | `docs/MIW-master-Question-bank/MEO_QB_master_v26.xlsx` *(git-ignored)* | `…/MIW_July2026_QuestionBank_SHARE.xlsx` *(git-ignored)* | `meoclass1/examiner-index.html` |
| **Purpose** | The product. Candidate-facing questions + answers | Search / updates manifest | Candidate-report tracker + build ledger | Subscriber share workbook | Examiner→question navigation |
| **Question count** | **681** numbered q-cards | 683 declared | 702 tracker rows (occurrences) | 683 in `All Questions` | 863 rows / 651 distinct questions |
| **Examiner evidence** | **880 in-prose mentions** across 627 questions; **0 structured attributes** | none | **624** attributed rows + 78 non-examiner | 828 per-examiner rows + 171 raw new-question rows | 863 tagged rows |
| **Granularity of link** | n/a (is the target) | file + `qnum` | **file only** — no anchor | **file only** — no anchor | **file + `#qN`** |
| **Strengths** | Only source of current wording, answer text and live anchors | Fast whole-corpus view; drives search | Only source of raw candidate wording, sitting dates, attempt no., vessel, pass/fail | Cleanest examiner→canonical-question listing; carries the July intake | Only artefact in MIW holding question-level examiner precision |
| **Known weaknesses** | Attribution is prose, unqueryable; two markup generations (`q-text` with and without `itemprop`) | 11 files drifted; QB1_A counts 2 non-question "map" cards as questions; lists 5 cheat-sheet files that do not exist | 132 rows unresolved; 134 fuzzy matches fail re-verification; Summary frozen at 30 Jun 2026 | **Not independent evidence** — see §3 | Header/mini-nav stale; 35 blank rows; 2 invalid tier literals; no generator |
| **Staleness** | Current (is truth) | **2026-08-13, partially stale** | **30 Jun 2026** cut | **31 Jul 2026** cut | Frozen at an unrecorded pass, hand-patched since |
| **Canonical for** | question text · anchors · URLs · answer existence · gating | *nothing* — derived | raw source wording · sitting date · attempt · vessel · result · examiner attribution | July intake wording + examiner | *nothing* — should become derived |

---

## 2. `qb_content_index.json` — classification: **DERIVED_BUT_STALE**

Headline figures look right (683 questions / 91 files, and both internal sums agree). The detail does not.

| Finding | Count |
|---|---|
| Files declared in JSON but **absent from the repo** | **5** — `QB1_K_CheatSheet.html`, `QB2_I_CheatSheet.html`, `QB4_J_CheatSheet.html`, `QB8_H_CheatSheet.html`, `QB9_H_CheatSheet.html` |
| Live QB files missing from JSON | 0 ✅ |
| File-level question-count mismatches | 1 — `QB1_A.html` claims 32, has 30 |
| Questions in JSON with no matching q-card | 2 — `QB1_A` q31/q32 are the "Convention Family Trees" and "Dependency Graph" **map cards**, not questions |
| Question-text mismatches | **99** (62 below 0.7 similarity) |
| Duplicate question identifiers | 0 ✅ |

The 683 headline is therefore **681 real questions + 2 navigational map cards**.

### Two distinct text-drift defects

Drift is concentrated in 11 files, and it is not one problem:

**(a) Stale earlier wording — same core ask.** `QB10_A` (6/6), `QB1_supplementary`, `QB6_F`:

| JSON | Live HTML |
|---|---|
| "Sagarmala in detail" | "Explain the Sagarmala Programme in detail." |
| "Amrit kal vision details" | "Explain the Maritime Amrit Kaal Vision 2047." |

The JSON preserved **raw candidate wording** that the page has since re-authored. Recoverable, low risk.

**(b) Off-by-one numbering shift — the dangerous one.** `QB2_B` (17/19) and `QB1_B` (16/21):

| qnum | JSON text | Live HTML text |
|---|---|---|
| 2 | IMDG marking/labelling requirements | container securing arrangement |
| 3 | IMDG Code overview | IMDG marking/labelling requirements |
| 4 | wrongly-labelled container fire | IMDG Code overview |

A question was inserted at position 2 and the JSON never renumbered. **Anything resolving a question by
`qnum` through this JSON is one question off from q2 onward in those files.**

**The examiner index did not inherit this.** Tested directly: of 828 non-blank index rows, **823 match the
live HTML at their anchor and only 2 match the stale JSON**. Commit `3256684` re-based the anchors on
reality. This is the single most important negative finding of the audit — the shift exists, and it did
*not* contaminate the index.

**Do not use `qb_content_index.json` as the question inventory for any Oral work.** Use the live HTML.

---

## 3. `MIW_July2026_QuestionBank_SHARE.xlsx` — **a sibling of the index, not a witness to it**

The July per-examiner sheets (Nair 329, Simon 231, Rajappan 93, Srivastava 90, Senthil 66, Paul 19) look
like the strongest examiner evidence in MIW. They are not evidence at all.

Two proofs:

1. **Their text is canonical MIW wording**, not candidate wording — "P&I Club — What is Protection &
   Indemnity? How does it differ from other marine insurance?" is the live `QB1_A#q1` verbatim.
2. **Overlap with the index is total.** Measured per source:

| Source | Matched rows | Already present in examiner-index | Overlap |
|---|---|---|---|
| July `Nair` sheet | 329 | 329 | **100%** |
| July `Simon` sheet | 231 | 231 | **100%** |
| July `Paul` sheet | 19 | 19 | **100%** |
| July `New Questions` (raw wording) | 171 | 113 | 66% |
| Master `All Questions` (raw wording) | 558 | 470 | 84% |

A genuinely independent source lands in the 60–85% band. A 100% match across three sheets of very
different sizes means one artefact was generated from the other. **Counting these as confirmation would be
circular** — the same defect as a self-test that harvests live state as its fixture.

They are classified `DERIVED_PRODUCT_SURFACE` and are excluded from all evidence counts in this audit.
What they *are* good for: they are a second, independently-published record of the same pairs, useful for
detecting whether a regeneration silently dropped anything.

The workbook's other sheets **are** primary: `New Questions (July 2026)` (171 rows, raw wording, examiner,
ship type) and the `Oral Notes Index` (Simon's 8-part notes series, 200 pages).

---

## 4. `MEO_QB_master_v26.xlsx` — schema report

11 sheets. `All Questions` is the tracker; everything else is input or log.

| Sheet | Rows | Columns | Semantics |
|---|---|---|---|
| `Summary` | 6 | Examiner, Question Count | Frozen **30 Jun 2026**: Nair 189, Simon 204, Rajappan 81, Srivastava 19, Senthil 27, Paul 9, **TOTAL 529** |
| `Nair` | 189 | No., Question, Attempt, Vessel, Result, Date | Raw WhatsApp candidate reports, per examiner |
| `Simon` | 204 | *(same)* | " |
| `Rajappan` | 81 | *(same)* | " |
| `Senthil` | 27 | *(same)* | " |
| `Srivastava` | 19 | *(same)* | " |
| `Paul` | 9 | *(same)* | " — **the whole of Paul's original evidence base** |
| `New Questions (Jun 2026)` | 206 | No., Examiner, Question, Vessel Type, Date, QB Topic | June intake, pre-build |
| `New Questions (Jul 2026)` | 54 | *(same)* | July intake, pre-build |
| `Jul 2026 - Duplicate Log` | 108 | Session, Examiner, Candidate Question, Status, Matched Existing Content | **The no-duplication principle already applied once** — a July ask judged already covered |
| **`All Questions`** | **702** | No., Examiner, Question, Attempt, Vessel, Result, Date, QB Topic, **Build_Status**, **Live_File**, **Match_Confidence**, **Live_Q_Text (matched)** | The tracker |

### The tracker's own confidence vocabulary is uncontrolled

`Match_Confidence` is free text: `0.83`, `manual`, `High (100% fuzzy match)`, `Built (Claude-verified — reconciliation pass 5 Jul)`.
Numeric scores, human labels and provenance notes share one column. It cannot be sorted, thresholded or
compared. Any future ledger must use a closed literal set.

### `Live_File` has no anchor

702 rows, **0 carrying `#q`**. The tracker can say *which page* answers a candidate's ask; it has never
been able to say *which question*. That is why the index's question-level precision has no upstream source.

---

## 5. Field-level precedence — verified, not assumed

| Field | Canonical source | Why |
|---|---|---|
| Current question text | **LIVE HTML** | Only source that is by definition current; JSON drifted on 99 questions, index display text on 38 |
| Question inventory (what exists) | **LIVE HTML** | JSON over-counts by 2 map cards and names 5 non-existent files |
| Canonical question id / anchor / URL | **LIVE HTML** | Anchors are the only identifier every surface agrees on after `3256684` |
| Answer existence, gating | **LIVE HTML** | 681/681 have answers; 86/86 files carry the `miw_auth` gate |
| Historical candidate wording | **MASTER XLSX** `All Questions.Question` | The only place raw asks survive; the HTML re-authored them |
| Sitting date, attempt number, vessel, result | **MASTER XLSX** | Exists nowhere else. 9 Paul records dated 29/06/2026 all marked "Pass" |
| July-intake wording + examiner | **JULY XLSX** `New Questions (July 2026)` | Raw wording, post-dates the master cut |
| Examiner attribution (primary) | **MASTER XLSX** + **JULY New Questions** | The only sources tying a named examiner to a raw candidate report |
| Examiner attribution (page-declared) | **LIVE HTML CE Oral Tip prose** | 45 `ce_tip` rows reproduce at 100%; 880 mentions across 627 questions |
| Examiner→question pair at question granularity | **EXAMINER INDEX** *(sole holder — extract urgently)* | No workbook carries an anchor |
| Tier / confidence label | **none — must be recomputed** | Current literals do not correspond to the evidence behind them |
| Headline counts | **none — must be derived** | Every count layer on the index except the section headings is stale |

---

## 6. Source classifications

| Source | Classification |
|---|---|
| Live QB HTML | **CANONICAL** (question text, inventory, anchors, URLs, gating) |
| `qb_content_index.json` | **DERIVED_BUT_STALE** — unsafe as a question inventory or as a `qnum` resolver |
| `MEO_QB_master_v26.xlsx` | **CANONICAL** for historical candidate evidence; **PARTIAL** as a live map (file-level only, 132 rows unresolved) |
| `MIW_July2026_QuestionBank_SHARE.xlsx` — per-examiner sheets | **DERIVED_PRODUCT_SURFACE** — never independent confirmation |
| `MIW_July2026_QuestionBank_SHARE.xlsx` — New Questions | **CANONICAL** for the July intake |
| `examiner-index.html` | **UNSAFE_AS_CANONICAL** as a count source; **sole holder** of question-level pairing — extract before any repair |
