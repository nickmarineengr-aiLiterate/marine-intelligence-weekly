# Oral Examiner Intelligence — Existing MIW Truth Audit (Phase 0/1)

**Date:** 18 August 2026 · **Next MEO Class 1 orals: 24 August 2026 (6 days)**
**Repo:** `F:\Marine-Intelligence-Weekly` · **Branch:** `research/oral-examiner-intelligence-v1-audit`
**Baseline:** `main` @ `3b55bfb` (clean, `origin/main` identical)
**Scope:** audit / inventory / reconciliation / connection analysis. **No answer authoring, no index edit, no 788-question ingestion.**

---

## Headline

MIW's existing Oral work is in **better shape than the count layers suggest and worse shape than the
tier badges claim.**

- Every one of the **863** examiner→question links on the live index **resolves correctly**. Zero broken
  links, zero wrong destinations.
- But the page's own header says **791** and its mini-nav sums to **809**. Three of the four count layers
  are stale.
- And only **406 of 862** unique pairs have a primary candidate record behind them. The word "confirmed"
  on that page does not currently mean what a candidate would take it to mean.
- The fastest safe win before 24 August is **not** authoring: **100 examiner→question connections are
  already asserted in MIW's own page prose and are missing from the index**, plus **49** more evidenced by
  the master tracker. That is ~149 new candidate-facing connections with **no new answers written**.

---

## 4. Entity definitions used throughout

These are counted separately everywhere in this audit and must never be compared as equivalents.

| Entity | Definition | Current value |
|---|---|---|
| **A. Unique live QB question** | One numbered `q-card` on a live QB page | **681** |
| **B. Source question occurrence** | One candidate/surveyor report row in a tracker or source document | **873** primary records |
| **C. Examiner↔question pair** | One canonical question connected to one examiner | **862** in the index; **455** evidenced |
| **D. Examiner evidence record** | One source row supporting a pair; many may support one pair | **1,701** ledger rows |
| **E. Source variant** | Different wording / follow-up around the same core ask | 227 in `LEGACY_MATCH_REVIEW.csv` |
| **F. Genuine question gap** | A source ask not substantively covered by any current MIW answer | *deferred to Phase 2* |

> Worked example of the distinction: three records saying Simon asked the same underlying question produce
> **one** canonical question, **one** Simon↔question pair, and **three** evidence records. Never three cards.

---

## Report

### A. Repo truth
`main` @ `3b55bfb5ac60875945490de97a9365d8dec74bbb`, identical to `origin/main`, working tree clean apart
from the untracked `docs/MIW-master-Question-bank/` inputs. `git fetch` succeeded; a `commit-graph`
rename warning appeared and is cosmetic (Windows file-lock), no ref was affected.

### B. Branch
`research/oral-examiner-intelligence-v1-audit`, cut from clean `main`. The Written QI branches
(`research/question-intelligence-v2-*`, `review/QI-v2-*`) were **not touched** — Desktop is working there.

### C. Input availability — all present

| Input | Status |
|---|---|
| `MEO_QB_master_v26.xlsx` | ✅ `docs/MIW-master-Question-bank/` (138,740 B) — **git-ignored** by `.gitignore:76` |
| `MIW_July2026_QuestionBank_SHARE.xlsx` | ✅ same folder (139,044 B) — git-ignored |
| `All Surveyors Class1 Oral Questions.docx` | ✅ same folder (65,614 B) — **deliberately not opened this session** |
| `qb_content_index.json` | ✅ `meoclass1/` |
| `examiner-index.html` | ✅ `meoclass1/` (277,881 B) — plus a second sales copy at `SQ/` |
| Live QB pages | ✅ 86 files, 681 questions |

Nothing was missing. The repo is **public**, so the two workbooks and the DOCX must stay git-ignored.

### D. Current examiner-index generation truth
**(E) Stale output whose generator does not exist in this repository.** Both original commits are
"Add files via upload"; every later change is a hand patch. See `EXAMINER_INDEX_REPRODUCTION_REPORT.md` §1.

### E. Generator / input files
**None exist.** No script in the repo emits `examiner-index.html`, and no surviving source carries a
question anchor — `Live_File` in the master tracker is file-level for all 702 rows (0 with `#q`), and all
1,332 July workbook hyperlinks are file-level. **The 863 question-level pairings exist only inside the
HTML file itself.**

### F. Current unique QB questions
**681** numbered questions across **86** live QB pages (cheat sheets excluded). All 681 have an answer
body; all 86 files carry the legacy `miw_auth` client gate.

### G. `qb_content_index.json` questions
**683 declared** = 681 real questions **+ 2 navigational map cards** (`QB1_A` q31 "Convention Family
Trees", q32 "Dependency Graph") miscounted as questions.

### H. HTML vs JSON drift
| Finding | Count |
|---|---|
| Files in JSON absent from repo | **5** (all `*_CheatSheet.html`) |
| Live files missing from JSON | 0 |
| File count mismatches | 1 (`QB1_A`: 32 vs 30) |
| Question-text mismatches | **99** (62 below 0.7) |
| Duplicate identifiers | 0 |

Two defect classes: **stale earlier wording** (recoverable) and an **off-by-one numbering shift** in
`QB2_B` and `QB1_B` (dangerous). **The index did not inherit the shift** — 823/828 rows align with live
HTML, 2 with the stale JSON. Classification: **DERIVED_BUT_STALE**. Details in the matrix, §2.

### I. Master workbook
11 sheets, `All Questions` is the tracker at **702 rows** / 12 columns. Per-examiner input sheets: Nair
189, Simon 204, Rajappan 81, Senthil 27, Srivastava 19, **Paul 9**. Plus `New Questions (Jun 2026)` 206,
`New Questions (Jul 2026)` 54, and a **`Jul 2026 - Duplicate Log`** of 108 rows — proof the
no-duplication principle has already been applied once by hand. `Summary` is frozen at 30 Jun 2026
(TOTAL 529). Full schema in the matrix, §4.

Two structural weaknesses: `Match_Confidence` is uncontrolled free text (`0.83`, `manual`,
`High (100% fuzzy match)` in one column), and `Live_File` carries no anchor.

### J. July workbook
13 sheets. `All Questions` 683 rows (a July snapshot of the live QB). Six per-examiner sheets totalling
**828** rows. `New Questions (July 2026)` **171** rows (Simon 94, Nair 49, Paul 28 — only three examiners).
Plus `Oral Notes Index` (Simon's 8-part, 200-page notes series) and three marketing sheets.

**Relationship to master: the per-examiner sheets are a *sibling* of the examiner index, not a source for
it.** They restate canonical MIW wording and overlap the index **100%** (329/329, 231/231, 19/19) where
genuinely independent sources land at 66–84%. Classified `DERIVED_PRODUCT_SURFACE` and excluded from all
evidence counts. Only `New Questions (July 2026)` is primary.

### K. Current examiners
Six, exactly as expected: **Nair, Simon, Rajappan, Srivastava, Senthil, Paul**. No seventh section.

### L. Examiner alias register
`EXAMINER_ALIAS_REGISTER.json`. Observed forms are honorific variants only (`Nair` / `Nair Sir` /
`Capt. Nair`); no two people were merged on surname resemblance. Four **non-examiner** attributions are
registered rather than discarded: `UNTRACED - WhatsApp` (50), `Nixon (own notes)` (18), `Not yet assigned`
(9), `Rathesh (WhatsApp report)` (1 — a reporting *candidate*, never to be promoted to examiner).

### M. Current examiner-question pairs
**863 rendered rows → 862 unique pairs** (one duplicate). Per examiner: Nair 339, Simon 243, Srivastava
103, Rajappan 93, Senthil 66, Paul 19.

### N. Evidence tier distribution (reproduced from rows, not furniture)
| Tier | Header claims | Actually rendered |
|---|---|---|
| `confirmed` | 359 | **406** |
| `ce_tip` | 45 | **45** |
| `cetip` *(invalid literal)* | — | **2** |
| `header` | 71 | **87** |
| `inferred` | 316 | **323** |
| **Total** | 791 | **863** |

### O. Broken index links
**Zero.** 863/863 target files exist, 863/863 anchors exist, 863/863 resolve to a numbered q-card.

Presentation defects on otherwise-correct links: **35 blank display rows** (`QB4_G` 18, `QB5_C_A` 6,
`QB5_G` 6, `QB6_E` 3, `QB7_F` 2), **2 invalid `cetip` tier literals** (both `QB7_I`, Simon — these two rows
**vanish permanently the moment a candidate uses any tier filter**, because `filterTier()` has no toggle
for that literal), and **3 same-core text-drift rows**.

### P. Duplicate index relationships
**1 duplicated pair / 2 rows** — Simon → `QB5_C_A#q1`, one copy blank.

### Q. Current QB questions with no examiner
**30 of 681** (4.4%) have no index connection. Only **1** question has no examiner signal anywhere —
neither an index row nor a prose mention.

### R. Multi-examiner questions
**178** questions carry more than one examiner; maximum **4** examiners on a single question.

### S. Legacy tracker matches (702 tracker rows + 171 July new-question rows)
| Classification | Count |
|---|---|
| `VERIFIED_MATCH` | 1,303 |
| `VERIFIED_SAME_CORE` | 98 |
| `PARTIAL_MATCH` | 34 |
| `WRONG_MATCH` | 134 |
| `UNRESOLVED` | 132 |
| `AMBIGUOUS` | 0 |
| `STALE_TARGET` | 0 |
| **Total** | **1,701** |

(`AMBIGUOUS` is a live literal in the vocabulary — the tie-break case where a runner-up scores within 0.05
of the winner — but no row triggered it. `AMBIGUOUS` appears 158 times as a *disposition* instead, applied
to rows whose mapping class carries no stronger reading.)

Dispositions: `ALREADY_CANONICAL_AND_LINKED` 1,273 · `AMBIGUOUS` 158 · `ALREADY_CANONICAL_LINK_MISSING`
**128** · `STALE_SOURCE_RECORD` 66 · `CANONICAL_MATCH_BUT_LEGACY_MAPPING_WRONG` 42 · `PARTIAL_COVERAGE` 34.

**Legacy fuzzy-match defects: 227 rows** in `LEGACY_MATCH_REVIEW.csv`, in two classes —
`SOURCE_ASK_NOT_COVERED_BY_MAPPED_QUESTION` (136: the tracker's claimed live text matches, but the
*original candidate ask* does not) and `MAPPING_UNVERIFIABLE_AGAINST_LIVE_FILE` (91). This is the class the
Founder suspected: keyword overlap survived, examiner demand did not.

### T. READY_CONNECTIONS — the fast win
Two independent channels, both requiring **no new answers**:

| Channel | Ready now | Needs review |
|---|---|---|
| **Page prose** — examiner named in a CE Oral Tip with assertive phrasing, not in the index | **100** | 91 supported + 163 weak |
| **Master tracker / July intake** — primary candidate record, verified match, not in the index | **49** | — |
| **Combined** | **≈149** | |

Prose channel by examiner: Simon 35, Rajappan 25, Nair 15, Senthil 13, Srivastava 9, Paul 3.
Tracker channel by examiner: Simon 23, Nair 11, Rajappan 9, Paul 4, Senthil 1, Srivastava 1.

Sample (verified by hand): `QB10_B#q6` → Rajappan, *"Rajappan will almost certainly…"*; `QB10_B#q1` →
Simon, *"…are the two he asks most"*; `QB10_B#q7` → Nair, *"If Nair asks 'when does the Net-Zero…'"*.

### U. Inferred-only connections
**309** of 862 pairs (36%) rest on topic inference alone with no primary record and no page assertion.
Separately, **196 of 323** `inferred`-tier rows *do* name their examiner in the page prose — the tier is
mislabelled in both directions. `INFERRED_ONLY_CONNECTIONS.csv`.

### V. John status — **NEW_EXTERNAL_ONLY_EXAMINER**
Zero MIW-native evidence, searched exhaustively:

| Where | Result |
|---|---|
| Master workbook (all 11 sheets, every cell) | **0** |
| July workbook (all 13 sheets, every cell) | **0** |
| `examiner-index.html` | **0** |
| QB page metadata / CE Oral Tips | **0** |
| Literal "John" in `meoclass1/*.html` | 4 hits in 3 files — **all false positives**: *"John Doe v. The Motor Vessel Olympic Prometheus"* (an in-rem worked example) and *"John Ziegler"* (Ziegler–Nichols PID tuning) |

The detector found and correctly down-graded both as `WEAK_INCIDENTAL_MENTION`. **Do not add a John
section** until the 788-question compilation is ingested and adjudicated.

### W. Paul status — thin at source, then unresolved
Not a generator omission and not an alias problem. The sequence:

| Stage | Paul records |
|---|---|
| Master per-examiner sheet (cut 30 Jun 2026) | **9** — one sitting, 29/06/2026, all marked "Pass" |
| Master tracker after June/July additions | 18 |
| July `New Questions` intake | **28** |
| **Total primary records now held** | **46** |
| Distinct canonical questions those resolve to | **18** |
| Pairs the index shows | **19** |

So MIW holds 46 primary Paul records but converts them into only 18 questions: **16 are `AMBIGUOUS`, 9
`STALE_SOURCE_RECORD`, 3 `PARTIAL_COVERAGE`, 4 `ALREADY_CANONICAL_LINK_MISSING`**. The cause is
**genuine evidence scarcity in the original tracker compounded by an unresolved July intake** — the July
Paul questions arrived after the last attribution pass and were never matched through.

The external compilation's ~103 Paul questions would therefore be a **genuine and large expansion**, not a
duplicate of hidden MIW work. Paul is the single strongest argument for the 788-question ingestion.

### X. Source reconciliation matrix
`ORAL_SOURCE_RECONCILIATION_MATRIX.md`.

### Y. Existing oral truth model
```
LIVE QB HTML  ── canonical question, text, anchor, URL, answer, gate
     ▲
     │ (anchor-level pairing exists ONLY here)
EXAMINER-INDEX.HTML  ── 863 pairs, no generator, no upstream source
     ▲                        ▲
     │ file-level only        │ page prose (880 mentions / 627 questions)
MASTER XLSX ──────────────────┘
  raw candidate wording · date · attempt · vessel · result
     ▲
JULY XLSX ── New Questions (primary) │ per-examiner sheets (DERIVED, not evidence)
```

### Z. Canonical field precedence
See matrix §5. In short: **live HTML** owns question text, inventory, anchors, URLs and gating;
**master XLSX** owns raw wording, sitting date, attempt, vessel and result; **July New Questions** owns the
July intake; **CE Oral Tip prose** owns page-declared attribution; **the index alone** owns question-level
pairing and must be extracted; **tier labels and every headline count must be recomputed**, never carried
forward.

### AA. Existing connection gaps
`EXISTING_CONNECTION_GAPS.csv` (49 tracker-evidenced) and `PROSE_CONNECTION_GAPS.csv` (354 prose,
graded). Every id in both files resolves to a live question — validated.

### AB. Fastest candidate value before 24 August
| | Metric | Value |
|---|---|---|
| **A** | READY_CONNECTION mappings addable with **no new answers** | **~149** (100 prose + 49 tracker) |
| **B** | Obviously wrong / stale existing mappings | **227** legacy fuzzy-match rows to review; **3** stale display texts |
| **C** | Questions with examiner evidence but missing from the index | **149** pairs across ~140 questions |
| **D** | Broken index links | **0** ✅ |
| **E** | Pairs relying on inference alone | **309** (36%) |
| **F** | Immediate gain by examiner (prose + tracker) | Simon **58**, Rajappan **34**, Nair **26**, Senthil **14**, Srivastava **10**, Paul **7** |

Plus three page defects that are cheap and candidate-visible: 35 blank rows, 2 filter-invisible rows,
1 duplicate row, and the header/mini-nav counts.

### AC. Future 788-comparison contract
The external record must preserve: `source_id`, `surveyor_raw`, `surveyor_normalized`, `topic`,
`source_question_number`, `raw_question_text`, `source_page`, `source_comment`, `source_type`,
`source_provenance`.

**Two orthogonal statuses, never combined into one field:**
- *Content coverage:* `EXACT_MATCH` · `NEAR_MATCH` · `SAME_CORE_ASK` · `PARTIAL_COVERAGE` · `MISSING` · `AMBIGUOUS`
- *Examiner mapping:* `ALREADY_LINKED` · `NEW_LINK` · `CONFLICTING_LINK` · `UNMAPPED`

A question can be `EXACT_MATCH` + `NEW_LINK` (we have the answer, not the connection) or `MISSING` +
`ALREADY_LINKED` (we link the examiner to a near-miss we should not have).

### AD. Gap creation rule (governing rule for Phase 2)
> **Would a candidate who studied the existing canonical MIW answer be materially unable to answer the
> source examiner ask?**
> **No** → connect / enrich. **Yes** → potential gap.

New wording alone never justifies a new question card. The master workbook's own
`Jul 2026 - Duplicate Log` (108 rows) shows this rule already applied by hand — reuse that discipline.

### AE. Examiner follow-up model
Preserve, do not promote to standalone questions. Relationship types: `PRIMARY_ASK` · `CROSS_QUESTION` ·
`FOLLOW_UP` · `EXPECTED_DETAIL` · `TOPIC_INFERENCE_ONLY`. Where a record shows an examiner specifically
wanted a regulation number, a test procedure or a missing point, that is examiner intelligence and belongs
on the existing question. The CE Oral Tip prose is already full of it and is currently unqueryable.

### AF. Index regeneration recommendation
Report first, generator second. **Extract the 863 pairs to data before repairing anything** — they exist
in one HTML file with no backup source. Then re-tier from the evidence ledger, then build
`tools/oral/build_examiner_index.py` deriving every count from the records it writes, gated by
`validate_audit.py`. Do **not** hand-patch the header. Detail in the reproduction report §6.

### AG. Validation results
`tools/oral/validate_audit.py` — **10 PASS / 3 FAIL / 0 UNAVAILABLE**. It fails closed.

PASS: all canonical ids resolve · no duplicate evidence ids · disposition and mapping vocabularies closed ·
every one of 1,701 rows carries an attribution kind (no row silently discarded) · all index links resolve ·
section headings match rendered rows · aliases resolve · both gap files resolve to live questions.

FAIL (all three are genuine live-page defects, not tooling): mini-nav 809 ≠ 863 · header 791 ≠ 863 ·
2 invalid tier literals.

### AH. Portability
No drive letter appears in any committed tool. `oral_lib.REPO` derives from the tool's own location; both
workbooks are **CLI arguments**; outputs are written relative to the repo root. Everything runs unchanged
on Desktop. One environment note: Windows console is cp1252, so these tools must be invoked with
`PYTHONIOENCODING=utf-8` or they crash on the first `✅` — the same trap recorded from the QI-v2 work.

### AI. Files created
Tools (`tools/oral/`): `oral_lib.py`, `audit_index.py`, `audit_sources.py`, `reconcile_evidence.py`,
`verify_tiers.py`, `prose_evidence.py`, `validate_audit.py`.

Audit outputs (`meoclass1/oral-intelligence/examiner-audit/`): `ORAL_EXISTING_TRUTH_AUDIT.md`,
`EXAMINER_INDEX_REPRODUCTION_REPORT.md`, `ORAL_SOURCE_RECONCILIATION_MATRIX.md`, `PHASE1_HANDOFF.md`,
`EXAMINER_ALIAS_REGISTER.json`, `CURRENT_ORAL_QB_INVENTORY.json`, `EXAMINER_EVIDENCE_LEDGER.jsonl`,
`EXAMINER_INDEX_PAIRS.csv`, `EXAMINER_INDEX_REPRODUCTION.json`, `SOURCE_AUDIT.json`,
`RECONCILIATION_SUMMARY.json`, `LEGACY_MATCH_REVIEW.csv`, `EXISTING_CONNECTION_GAPS.csv`,
`INFERRED_ONLY_CONNECTIONS.csv`, `PROSE_EXAMINER_EVIDENCE.csv`, `PROSE_CONNECTION_GAPS.csv`,
`PROSE_EVIDENCE_SUMMARY.json`, `TIER_REPRODUCIBILITY.json`, `TIER_EVIDENCE_ROWS.csv`,
`VALIDATION_RESULTS.json`, `MASTER_TRACKER_ROWS.json`, `MASTER_EXAMINER_SHEETS.json`,
`JULY_EXAMINER_SHEETS.json`, `JULY_NEW_QUESTIONS.json`.

### AJ. Files modified
**One, and it is not a production page: `.gitignore`.**

No candidate production page, no `examiner-index.html`, no q-card, no `SQ/`, no commerce, no payments, no
magazine, no Written QI, no solvedQP. Every other write is a new file under `tools/oral/` or
`meoclass1/oral-intelligence/examiner-audit/`.

The `.gitignore` change closes a real exposure found during the audit. The existing rule at line 76 was
`docs/MIW-master-Question-bank/*.xlsx` — **`.docx` was not covered**, so the 788-question
`All Surveyors Class1 Oral Questions.docx` was staged and committable on a **public** repository. The rule
now also covers `*.docx`, `*.doc` and `*.pdf` in that folder. Confirmed:
`git check-ignore` now matches the DOCX at `.gitignore:80`.

### AK. Git
Branch `research/oral-examiner-intelligence-v1-audit` off clean `main` @ `3b55bfb`. `main` untouched, no
force push. The two workbooks and the DOCX remain git-ignored — the repo is public.

### AL. Founder decisions (5)
1. **Publish the ~149 ready connections before 24 August?** They need no new answers, but the index has no
   generator, so this means building one (recommended) or hand-editing (not recommended).
2. **Accept the graded prose tier?** 100 "strong CE-tip assertion" links are page-declared, not
   tracker-confirmed. Show them as `CE tip` tier, or hold for review?
3. **Re-tier the whole index from evidence?** This will move ~456 pairs out of `confirmed`/`header` into
   an honest inference tier and will *reduce* the apparent confirmed count. Candidate-honest, but the
   headline number gets smaller.
4. **`SQ/examiner-index.html` is a sales page publishing stale numbers** ("791+", "212 Simon",
   "Paul Sir — All 10 Questions" against a live 19, "62+ QB Files" against 86). Outside this session's
   boundary. Authorise a commerce-side correction?
5. **Paul:** 46 primary records held, only 18 questions resolved. Resolve the existing July Paul backlog
   first, or wait and do it inside the 788 ingestion?

### AM. Next action — exactly one
> **DESKTOP CLAUDE — INGEST THE 788-QUESTION ALL-SURVEYORS COMPILATION INTO STRUCTURED SOURCE RECORDS AND
> RECONCILE IT AGAINST THE LAPTOP-VERIFIED EXISTING ORAL TRUTH BASELINE, SEPARATING NEW EXAMINER
> CONNECTIONS FROM PARTIAL COVERAGE AND GENUINE QUESTION GAPS.**

The baseline is sound: zero broken links, a closed-vocabulary ledger of 1,701 evidence records, and a
validation gate that fails closed. No bounded repair needs to precede ingestion — the three validation
failures are display-layer defects that the index regeneration will resolve anyway, and none of them
misdirects a candidate.

**Run in parallel, not before:** extract the 863 pairs to `EXAMINER_RELATIONSHIPS.jsonl`. They exist in
exactly one hand-uploaded HTML file with no upstream source, and that is the only real fragility this
audit found.

### AN. Verdict

> ## GO — EXISTING MIW ORAL TRUTH AUDITED AND READY FOR 788-QUESTION RECONCILIATION
