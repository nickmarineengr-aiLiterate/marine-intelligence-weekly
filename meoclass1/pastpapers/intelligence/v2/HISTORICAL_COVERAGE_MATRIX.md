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
| **India (2005) Morning Paper, Management Level** — `SRC-DGS-2005-MGMT` | **`OFFICIAL_FULL_PAPER`** | The only official dated sitting paper either phase has obtained. Nine stems plus the printed rubric. Year 2005 HIGH (printed on the paper); month February MEDIUM (DGS filename token `0205` and the OLE creation date agree — neither is printed). |

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
