# Phase 1 Handoff — Oral Examiner Intelligence

**From:** Laptop Claude (Opus 5), 18 Aug 2026
**To:** Desktop Claude — 788-question All-Surveyors reconciliation
**Branch:** `research/oral-examiner-intelligence-v1-audit` · **Baseline:** `main` @ `3b55bfb`

---

## What you can rely on

| Fact | Value | Where |
|---|---|---|
| Live Oral QB questions | **681** across 86 files | `CURRENT_ORAL_QB_INVENTORY.json` |
| Canonical id convention | `<file-stem>#q<N>`, e.g. `QB1_A#q1` | — |
| Examiner→question pairs currently published | **862** unique (863 rows) | `EXAMINER_INDEX_PAIRS.csv` |
| Broken index links | **0** | validated |
| Evidence records | **1,701**, closed vocabulary | `EXAMINER_EVIDENCE_LEDGER.jsonl` |
| Established examiners | 6 (Nair, Simon, Rajappan, Srivastava, Senthil, Paul) | `EXAMINER_ALIAS_REGISTER.json` |
| John | **no MIW-native evidence whatsoever** | register + audit §V |

Re-run anything with:

```bash
PYTHONIOENCODING=utf-8 python tools/oral/audit_index.py
```

```bash
PYTHONIOENCODING=utf-8 python tools/oral/reconcile_evidence.py --master <master.xlsx> --july <july.xlsx>
```

```bash
PYTHONIOENCODING=utf-8 python tools/oral/validate_audit.py
```

Expected validation state today: **10 PASS / 3 FAIL / 0 UNAVAILABLE**. The three failures are the known
live-page count defects. If a *fourth* appears, something regressed — stop.

---

## Six traps this audit hit, so you don't

1. **`PYTHONIOENCODING=utf-8` is mandatory.** Windows console is cp1252; the first `✅` in the index kills
   an unguarded script.
2. **QB pages have two markup generations.** `<div class="q-text">` *and*
   `<div class="q-text" itemprop="name">`. An exact-attribute regex silently returns empty text for whole
   files and manufactures fake "drift". Always `[^>]*`.
3. **`q-card` is not always a question.** `QB1_A` carries `id="family-trees"` and `id="dependency-graph"`
   map cards. Filter on `id="q<digits>"`, or you inherit `qb_content_index.json`'s 683-vs-681 error.
4. **The July per-examiner sheets are NOT evidence.** They overlap the examiner index 100% (329/329,
   231/231, 19/19). They are a sibling product surface. Counting them as confirmation is circular and will
   inflate every "confirmed" number you produce.
5. **`qb_content_index.json` cannot resolve a question by `qnum`.** `QB2_B` and `QB1_B` carry an
   off-by-one insertion shift — JSON q2 = HTML q3. Resolve against the live HTML, always.
6. **No source outside the index carries an anchor.** All 702 tracker `Live_File` values and all 1,332
   July hyperlinks are file-level. When the 788 source says "Simon asked X", you can find the *page* from
   history but you must derive the *question* yourself.

---

## Your Phase 2 contract

Emit one record per external question, preserving:
`source_id`, `surveyor_raw`, `surveyor_normalized`, `topic`, `source_question_number`,
`raw_question_text`, `source_page`, `source_comment`, `source_type`, `source_provenance`.

Then assign **two independent statuses** — never one merged field:

- **Content coverage:** `EXACT_MATCH` · `NEAR_MATCH` · `SAME_CORE_ASK` · `PARTIAL_COVERAGE` · `MISSING` · `AMBIGUOUS`
- **Examiner mapping:** `ALREADY_LINKED` · `NEW_LINK` · `CONFLICTING_LINK` · `UNMAPPED`

The common and valuable case is `EXACT_MATCH` + `NEW_LINK`: MIW already answers it, we just never
connected that examiner.

### The creation test

> Would a candidate who studied the existing canonical MIW answer be materially unable to answer the
> source examiner ask?

**No → connect / enrich. Yes → potential gap.** New wording alone never earns a new card. The master
workbook's `Jul 2026 - Duplicate Log` (108 rows) is a worked precedent for this judgement.

### Expected shape of your results

- **Paul is the real prize.** MIW holds 46 primary Paul records but resolves only 18 questions, and the
  external source reportedly carries ~103. Expect the largest genuine gap here.
- **John is entirely new.** Zero MIW evidence. Every John question is a new attribution; adjudicate the
  person before creating a section.
- **Simon and Nair are near-saturated** (343 and 276 primary records already). Expect mostly
  `ALREADY_LINKED` and `NEW_LINK`, few genuine gaps.

---

## Do not touch

`main` · `examiner-index.html` · any q-card · `SQ/` · commerce · payments · magazine · Written QI
(`research/question-intelligence-v2-*`, `review/QI-v2-*` — Desktop's other stream) · solvedQP.

Never commit `MEO_QB_master_v26.xlsx`, `MIW_July2026_QuestionBank_SHARE.xlsx` or
`All Surveyors Class1 Oral Questions.docx`. **The repository is public.** They are already covered by
`.gitignore:76` for the workbooks — confirm the DOCX before any `git add`.

---

## Parallel work worth doing first

Extract the 863 pairs from `examiner-index.html` into `EXAMINER_RELATIONSHIPS.jsonl`. That question-level
precision exists in exactly one hand-uploaded HTML file, with no generator and no upstream source. It is
the only genuine fragility this audit found, and `EXAMINER_INDEX_PAIRS.csv` is already 90% of the job.
