# Historical coverage matrix

**RESEARCH ONLY.** `current_as_of: 2026-08-17`
Retrieval window 2026-08-17 into 2026-08-18. Exam target: **August 2026 sitting**.

Coverage is stated as what MIW can **read and reproduce**, not what MIW has once
seen. Nothing here is inflated.

---

## Classification

| Class | Meaning |
|---|---|
| `OFFICIAL_FULL_PAPER` | a complete official sitting paper, preserved |
| `FULL_PAPER_THIRD_PARTY` | a complete paper from a non-official source, preserved |
| `PARTIAL_PAPER` | some questions of a sitting |
| `QUESTION_TEXT_ONLY` | question wording held, no rubric or marks |
| `RECURRENCE_METADATA_ONLY` | a provider asserts a sitting exists; no text seen |
| `SOURCE_REFERENCED_BUT_NOT_PRESERVED` | a reading was taken; nothing MIW holds reproduces it |
| `OFFICIAL_QUESTION_BANK` | official question wording, **no sitting, no date** — new in Phase 2 |
| `MISSING` | nothing at all |

---

## Priority A — 2010, 2011, 2012 Engineering Management

**This is the window Phase 2 was sent to attack, and it did not fall.**

| Year | Sittings | Class | Evidence |
|---|---|---|---|
| 2010 | Jan–Dec | `RECURRENCE_METADATA_ONLY` | DieselShip set index confirms month-level sets exist and gives per-set question counts. **No stem is publicly rendered.** |
| 2011 | Jan–Dec | `RECURRENCE_METADATA_ONLY` | as 2010 |
| 2012 | Jan–Dec | `RECURRENCE_METADATA_ONLY` | as 2010 |
| 2012 | July | `SOURCE_REFERENCED_BUT_NOT_PRESERVED` | `SRC-SCRIBD-106245627` — two stems read in Phase 1; only a 3,043-byte stub preserved, and the recorded sha256 hashes that stub |

**Readable full papers for 2010–2012: zero. Unchanged from Phase 1.**

The 33 preserved DieselShip set pages give counts and set identity only. They can
corroborate that a sitting happened. They cannot evidence a single question.

---

## What Phase 2 *did* recover

Neither entry falls in the priority window. Both are official, and one reshaped the
whole layer.

| Source | Class | Notes |
|---|---|---|
| **Question Bank MEO CL-I** — `SRC-DGS-QBANK-ARCHIVED` | **`OFFICIAL_QUESTION_BANK`** | 185 items, 100% extracted, `PRESERVED_RAW`, sha256 pinned. **Undated.** Not a sitting, and never counted as one. |
| **India (2005) Morning Paper, Management Level** — `SRC-DGS-2005-MGMT` | **`OFFICIAL_SAMPLE_PAPER`** | **Reclassified in Phase 3B.** Clean re-extraction shows the document is headed **`SAMPLE PAPER`**. It is an official DGS specimen, not a sitting, so it dates nothing and the February month is withdrawn — that month rested only on the filename token `0205` and the OLE creation date, neither of which is printed. Its nine stems are bank items **57–64** (contiguous) plus 126, so the bank already holds the paper verbatim. See `PHASE3B_REPORT.md` §4. |

The bank is by far the more valuable — it supplied official ancestors for five of
QP2608's limbs and matched 63 questions across the corpus — but it is worth being
exact about what it does to *coverage*: **nothing.** It adds no sitting. Coverage of
2010–2012 is precisely what it was.

---

## MIW's own holdings, for contrast

| Window | Class | Holdings |
|---|---|---|
| 2021-01 → 2023-12 | `QUESTION_TEXT_ONLY` | 30 papers, 270 questions, intelligence-only |
| 2023 → 2026 | `OFFICIAL_FULL_PAPER` + solved | 40 papers, 360 questions |

MIW's sitting evidence floor is **January 2021**. Every dormancy statement in this
layer is bounded by it.

---

## Routes attempted in Phase 2

| Route | Outcome |
|---|---|
| `dgshipping.gov.in` question bank PDF (direct) | **ECONNREFUSED** `164.100.60.201:443` — retried, still blocked |
| `www.dgshipping.gov.in` root | **ECONNREFUSED** — whole domain unreachable |
| `betadgs.dgshipping.gov.in` model question papers — **new host, found in Phase 2** | **ECONNREFUSED** |
| `dgshipping.gov.in` exam module page (direct) | **ECONNREFUSED** |
| Internet Archive — question bank PDF | **SUCCESS** — official PDF, 314,710 bytes |
| Internet Archive — exam module page | **SUCCESS** — full document index recovered |
| Internet Archive — `meomemI_0205_I.doc` | **SUCCESS** — official 2005 Management paper |
| Wayback CDX index for `dgshipping.gov.in` | **SUCCESS** — 12,130 archived URLs enumerated, 830 mentioning MEO |
| DG Shipping MEO result lists, 2013–2014 | Located, **not pursued** — pass lists, no question text |
| `marinenotes.blogspot.com` MMD papers | Fetched. Class I subjects listed; **no Engineering Management, no 2010–2012** |
| `meoexamz.co.in` | Fetched. One Engineering Management page; **no dated 2010–2012 papers** |
| `marineengineeringonline.com` | **Not retried.** Phase 1 recorded HTTP 403; re-attempting an explicit refusal with nothing changed would be pressing a block |
| DieselShip set **contents** | **Not attempted** — subscription-gated. No login; the site warns a wrong login bans the IP |

No paywall bypassed, no authentication attempted, no CAPTCHA encountered, no
user-agent substitution, no paid answers acquired.

One retrieval detail worth keeping: the plain Wayback URL returns the archive's HTML
toolbar wrapper; only the raw `id_` variant returns the underlying file. Phase 2
first downloaded 12,882 bytes of `<!DOCTYPE html>` named `.pdf`, and had to notice.

---

## Honest summary

**The 2010–2012 gap is unchanged.** Phase 2 recovered a lot of official material and
none of it dates a sitting in the priority window.

What changed is that the *recurrence* claims no longer need that window — they rest
on the Directorate's own published question bank. What still needs it, and remains
blocked, is every **date** claim: H1 through H5, and any candidate-facing
“asked before in …” line.

The most promising remaining route is the DG Shipping domain becoming reachable. The
CDX index shows the Directorate has published a great deal of examination material
over the years; Phase 2 enumerated 830 archived MEO URLs and sampled a handful.
**That enumeration is itself an asset for Phase 3.**

---

# Phase 3B — the archive route, worked and closed

`current_as_of: 2026-08-18`

Phase 3B worked the archived MEO enumeration to its end. Full evidence in
`PHASE3B_REPORT.md`; inventory in `PHASE3B_SOURCE_INVENTORY.json`.

## The 2013–2015 Class I files are result lists

The 12 files Phase 3A identified as the Phase-3B acquisition target — re-derived
here as **15** distinct filenames — all sit under `/writereaddata/ExamResult/`.
Two were rendered and read: they are scanned candidate pass/fail tables
(application no., name, Written result, Orals result, certificate yes/no) with
**no question text of any kind**.

| Window | Class | Evidence |
|---|---|---|
| 2013-08 → 2015-09, MEO Class I | **`METADATA_ONLY`** | 15 official dated result lists. They evidence that sittings happened and who passed. They cannot evidence one question. |

**This route yields no question text and is closed.**

## The 1999–2005 Class I papers are real, and are a different exam

`/WriteReadData/userfiles/file/` holds 686 official DGS `.doc` files, of which
**81 are Class I**. All 81 were retrieved, verified official by DGS's own Word
authoring metadata, and extracted — 727 questions, 1,784 comparable units.

| Year | Sittings | Class | Evidence |
|---|---|---|---|
| 1999-06 | EKG, EKM | **`OFFICIAL_FULL_PAPER`** | month and year printed on the paper |
| 1999-07 | EKG, ET | **`OFFICIAL_FULL_PAPER`** | month and year printed |
| 1999-07 | NA | **`OFFICIAL_PARTIAL`** | month printed; questions render inside Word tables and only 2 parse |
| 2001 (12 serial sets) | AM, EKG, EKM, EKS, ET, HE, HT, NA | **`QUESTION_TEXT_ONLY`** | 58 papers printing `INDIA (2001)` and a **serial number**, never a month. A year is not a sitting. |
| 2000 and undated | EKG, EKM, ET, NA | **`QUESTION_TEXT_ONLY`** | 17 papers printing no date at all |
| 2005-??  Engineering Management | **`OFFICIAL_SAMPLE_PAPER`** | one specimen paper, undated, already inside the bank |

**Subject, not volume, is the limit.** These are Applied Mechanics, Naval
Architecture, Electrotechnology, Heat Engines and Engineering Knowledge papers —
the pre-2010 Class I structure. MIW's corpus and the official bank are both
**Engineering Management**. Swept with the unmodified Phase-3A.3 classifier,
1,784 archived units produce **27** reportable rows, **9** strong — and 8 of
those 9 are the 2005 sample paper matching the bank it is already part of.
Strong matches against MIW's own corpus: **zero**.

## Dated coverage of Engineering Management — unchanged

| Window | Class |
|---|---|
| 1999–2000 | `MISSING` for Engineering Management (the subject did not exist in this form) |
| 2001–2012 | `MISSING` |
| 2013–2015 | `METADATA_ONLY` — result lists only |
| 2016–2020 | `MISSING` |
| 2021-01 → 2026-08 | `QUESTION_TEXT_ONLY` / `OFFICIAL_FULL_PAPER` — MIW's own 70 papers |

**MIW's dated evidence floor remains January 2021.** The official bank still
supplies undated ancestry and is not counted as coverage.
