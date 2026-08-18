# Phase 3B — verified historical ingestion

**RESEARCH ONLY. NOTHING HERE IS CANDIDATE-FACING.**
`current_as_of: 2026-08-18` · Desktop · branch `research/question-intelligence-v2-phase3b`
Base: `53a04ee`, the Phase-3A.3 tip the Laptop scale-authorised at `cb7a8ed`.

---

## The short version

Phase 3B was sent to convert an identified set of official archived DG Shipping
MEO Class I files into verified dated sitting history.

**That set does not contain question papers.** It contains candidate result
lists. The finding is not a parsing difficulty or a retrieval failure — the
documents are exactly what DGS published, and what DGS published there is
pass/fail tables.

A different and much larger population of official DGS papers *was* found,
verified and extracted: **81 MEO Class I question papers, 1999–2005**. They are
genuine, they are official, and they are a **different examination** from the
one MIW's corpus is built on. Measured against the official bank and against
MIW's own corpus with the unmodified Phase-3A.3 classifier, they yield almost
no signal.

**Verified dated Engineering Management sitting history obtainable from this
archive: zero.** No occurrence record was created, and none should have been.

---

## 1. The target set is result lists, not papers

Phase 3A recorded "12 MEO Class I files, roughly October 2013 – September 2015"
as the Phase-3B acquisition target. Re-enumerating the Wayback CDX index for
`dgshipping.gov.in` (47,227 collapsed rows, 833 mentioning MEO) reproduces that
population and finds **15** distinct Class I filenames, not 12 — the extra three
are 2017–2018 files outside the stated window.

Every one of them sits under `/writereaddata/**ExamResult**/`.

Two were retrieved and **rendered to image and read**, because a path name is
not evidence:

| File | What it actually is |
|---|---|
| `meoclassI_mum_oct13_wo.pdf` | "MEO CL. I / OCTOBER 2013 (MUMBAI) / SECOND COPY" — a scanned table of candidates: application no., EXN 45 no., rotation no., name, pre-sea institute, attempts, Written result, Orals result, function passed, certificate yes/no |
| `MEOCLIAPRIL.pdf` | "MEO CL. I / APRIL - 2017 (KOLKATA)" — the same table, signed by the Examiner of Engineers and the Chief Examiner |

Both are scans from an office MFP (`TOSHIBA e-STUDIO`), landscape, no text
layer. Both carry **zero question text**. They are Class I, they are official,
they are dated — and they evidence *who passed*, not *what was asked*.

They are recorded in `PHASE3B_SOURCE_INVENTORY.json` as
`document_type: EXAM_RESULT_LIST`, `content_status: NOT_QUESTION_PAPER`, and
they are barred from ever becoming dated history by check `C51`.

**Consequence.** The route Phase 3A identified as "twelve more dated sittings
than the layer has outside MIW's own holdings" does not exist. Chasing the
remaining thirteen would produce thirteen more result lists.

These files also contain the names of real candidates. Nothing beyond document
type was extracted from them, and no candidate data is recorded anywhere in this
layer.

## 2. What the archive does hold — 81 official Class I papers

The MEO material is concentrated somewhere else entirely:
`/WriteReadData/userfiles/file/`, holding **686** distinct official DGS `.doc`
files under a systematic `meo<subject><class>_<token>.doc` convention. **81 are
Class I.** All 81 were retrieved and extracted.

Their official origin is not merely "hosted by the Internet Archive". The Word
originals carry DGS's own authoring metadata — `Author: DG SHIPPING`,
`EXAMSERVER`, `ENGEXAM`, `Last Saved By: EXAM`, printed on DGS's own exam
server. All 81 are classed `AUTHENTIC_OFFICIAL_ARCHIVE`.

| Subject | Papers |
|---|---|
| Engineering Knowledge (General) | 17 |
| Electrotechnology | 17 |
| Naval Architecture | 16 |
| Heat Engines | 10 |
| Applied Mechanics | 8 |
| Engineering Knowledge (Motor) | 7 |
| Engineering Knowledge (Steam) | 4 |
| Heat Transfer | 1 |
| **Engineering Management** | **1** (and it is a sample — §4) |

**727 questions / 1,784 comparable units** extracted, 76 papers `PARSED`,
4 `PARTIAL`, 1 `UNREADABLE` (the last five render their questions inside Word
tables, which the extractor reports rather than silently under-counts).

## 3. Only five papers print a date

This is the finding that governs everything downstream.

| Date evidence | Papers |
|---|---|
| `MONTH_AND_YEAR_PRINTED` | **5** |
| `YEAR_PRINTED_MONTH_UNKNOWN` | 58 |
| `NO_DATE_PRINTED` | 17 |
| `SAMPLE_PAPER_NOT_A_SITTING` | 1 |

The five that print a month:

| Sitting | Subject | Questions |
|---|---|---|
| June 1999 | Engineering Knowledge (General) | 14 offered, attempt TEN |
| June 1999 | Engineering Knowledge (Motor) | 9 |
| July 1999 | Engineering Knowledge (General) | 14 |
| July 1999 | Electrotechnology | 9 |
| July 1999 | Naval Architecture | 2 parsed of a table-rendered paper (`PARTIAL`) |

The 58 "year-only" papers print `INDIA (2001)` and a serial number — set 1
through set 12 — and no month at all. **The filename token is not a date.**
`meoekgI_2001.doc` is serial set 2, not February. Every one of those tokens is
carried as `filename_date_token` and never as a sitting month; `C50` fails the
build if a month ever appears without printed evidence.

### A date that was not there

The first extractor run reported a **July 1986** sitting. It was false. The
paper prints no year; the phrase came out of question 2's own text — *"ships
whose keel was laid before 1st July 1986"* — which a fixed-size header window
swallowed. The header region now ends at the rubric or the first question,
whichever comes first. A regulation's application date is not a sitting date,
and this is precisely how a fabricated year enters a corpus.

## 4. The 2005 Management paper — a correction to the existing layer

`SRC-DGS-2005-MGMT` was carried by Phase 2 as `OFFICIAL_SITTING_PAPER`, dated
**FEB 2005**, and the coverage matrix called it *"the only official dated sitting
paper either phase has obtained"*.

Clean re-extraction shows the document is headed **`SAMPLE PAPER`**.

It is an official DGS specimen paper. It records no sitting, so it evidences no
date, and month FEB is withdrawn — that month rested only on the filename token
`0205` and the OLE creation date, **neither of which is printed**. This is the
same failure mode as §3's phantom 1986, reached by a different road.

A second finding removes its independent value entirely. Swept against the
official bank under the unmodified classifier, its questions are bank items
**57–64, a contiguous block**:

| Sample paper | Bank item | Class |
|---|---|---|
| Q1 | 57 | `EXACT_REPEAT` |
| Q2 | 58 | `EXACT_REPEAT` |
| Q3 | 59 | `EXACT_REPEAT` |
| Q4 | 60 | `EXACT_REPEAT` |
| Q5 | 61 | `NEAR_VERBATIM` |
| Q6 | 62 | `EXACT_REPEAT` |
| Q7 | 126 | `SAME_CORE_ASK` |
| Q8 | 63 | `EXACT_REPEAT` |
| Q9 | 64 | `EXACT_REPEAT` |

**The 185-item bank already contains this paper verbatim.** It adds no question
text MIW does not hold and no date. Phase 3A had already established that it
keys no occurrence and leaks no date into any family, so the blast radius of the
original misclassification is the manifest and the coverage matrix — both
corrected on this branch.

## 5. The measurement — the papers carry almost no signal

All 1,784 units were swept against the 185-item official bank and against MIW's
40-paper solved corpus, using `qi_similarity.py` **unchanged**. No threshold was
touched. A sweep that had to loosen the classifier would be measuring the
loosening.

| | Result |
|---|---|
| Units swept | 1,784 |
| Reportable rows | **27** |
| Strong (exact/near) | **9** |
| — of which from the 2005 sample paper | **8** |
| Strong rows from the 80 genuine papers | **1** |
| Strong rows vs MIW's own corpus | **0** |

The single strong row outside the sample paper is `meoekmI_101.doc` Q8 against
bank item 183 at `NEAR_VERBATIM`. Against MIW's corpus, the best any archived
paper achieves anywhere is `SAME_CORE_ASK`.

This is the empirical statement of the subject problem. The 1999–2005 Class I
examination was a set of technical subject papers — propellers, metallurgy,
steering gear, boiler water treatment. The modern Class I written paper, the one
MIW's corpus and the official bank are both built on, is **Engineering
Management** — lay-up and reactivation, dry docking, the ISM Code, marine
insurance, the Merchant Shipping Act, man management. They are different
examinations. The overlap is not small because the classifier is strict; it is
small because the syllabus changed.

## 6. No occurrence records were created

Per §30, ingestion stopped at the source stage and reported, rather than
scaling through a broken assumption. Nothing was ingested because nothing
qualified:

- the result lists carry no questions;
- the sample paper is not a sitting and is already in the bank;
- the 58 year-only papers cannot date a sitting to a month;
- the 5 genuinely dated 1999 papers are in subjects that connect to neither the
  bank nor MIW's corpus above `SAME_CORE_ASK`, in a single instance.

Creating 727 occurrence records to show volume would have inflated the layer
with a different exam's history. `frequency_known` still counts sittings and
nothing else, and no family moved.

**Occurrences before Phase 3B: 25. After: 25. Families: 9 and 9.**

## 7. L3A3-1 — watched at scale, not triggered

The Laptop's open finding was that plural `Regs` is not recognised as a
designator, so `"Regs 14 and 15 apply"` leaks `COUNT 14, COUNT 15`, with zero
measured incidence in classifier-visible text.

Phase 3B put 1,784 units of genuine historical examination text through the
pattern — 1999–2005, nine subjects, text written by a different generation of
examiners and never seen by the classifier before.

**Zero hits. Not triggered.** No `REAL_PHASE3B_TRIGGER` is recorded and no
repair was made. The entry stays on the watch register with its incidence
evidence strengthened, exactly as §27 requires.

## 8. What was corrected, and what was added

| Change | Why |
|---|---|
| `SOURCE_MANIFEST.json` — `SRC-DGS-2005-MGMT` retyped `OFFICIAL_SAMPLE_PAPER`, month withdrawn | it prints `SAMPLE PAPER` (§4) |
| `README.md` — "Nothing is even `DATE_VERIFIED`" | stale; `EM-0008` and `EM-0009` are (L3A3-2) |
| `PUBLICATION_STATUS_MODEL.md` — same claim | the same staleness, in a second file the Laptop had not flagged |
| `HISTORICAL_COVERAGE_MATRIX.md` | the 2005 row and the archive route restated truthfully |
| `PHASE3B_SOURCE_INVENTORY.json` | new — 98 archived sources with what each turned out to be |
| `C48`–`C52` | new — the date guards, with 5 mutations proving each is load-bearing |

## 9. Suites

| Suite | Before | After |
|---|---|---|
| validator checks / failures | 202 / 0 | **207 / 0** |
| validator mutations / escapes | 48 / 0 | **53 / 0** |
| classifier controls / failures | 66 / 0 | **66 / 0** |
| parser cases / failures | 41 / 0 | **41 / 0** |
| regex mutations / escapes | 3 / 0 | **3 / 0** |
| bank sweep | 45 strong / 37 core / 82 reportable | **unchanged** |

No count fell. The corpus sweep did not move a row.

---

## Assessment — is verified history now materially useful?

**No, and not because too little was found.** 81 official papers were found,
verified and extracted; the acquisition worked. What they show is that the
archive's dated Class I material predates the syllabus MIW examines, and the one
Management-level document in it is a specimen that the bank already contains.

The layer's verified dated history is unchanged: it runs from **January 2021**,
MIW's own evidence floor. The official bank still supplies ancestry without
dates. Phase 3B did not move the boundary between the two — it established, with
evidence rather than assumption, that this particular archive cannot.

That is worth having. The 2013–2015 route is now closed on inspection rather
than on hope, the 2005 date claim is withdrawn before it could be published, and
two ways of inventing a date from a filename are now guarded by tests.

**Verdict: `HOLD` — Phase 3B needs stronger dated source coverage.** The gap is
1999→2021 in Engineering Management, and nothing in `dgshipping.gov.in`'s
archived holdings fills it.
