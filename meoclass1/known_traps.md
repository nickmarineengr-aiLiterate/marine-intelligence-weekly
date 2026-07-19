# Known Traps & Standing Corrections — Marine Intelligence Weekly

Master reference of verified-correct facts that have previously been drafted wrong
(by Gemini, by source material, or by first-pass Claude verification). Every new
QB/notes batch should be checked against this list before HTML is built — not
just recalled from memory.

Each entry has a `GREP:` line. The health check script only auto-scans entries
where `GREP:` gives an exact wrong phrase that is unambiguous out of context
(safe to flag anywhere it appears). Entries where the "wrong" version is a
general term that's also legitimately used correctly are marked `GREP: SKIP` —
those stay manual-review-only, checked during the verification pass, not by
the automated scanner.

---

### 1. FAL Form 8
FAL Convention has exactly **7 numbered forms**. "FAL Form 8" is a common
examiner trap referring to the **IHR 2005 Maritime Declaration of Health**,
which is not a FAL form at all.
GREP: FAL Form 8

### 2. PSC detention action code
**Action code 30 = detention.** "Action code 15" for detention is wrong.
GREP: action code 15

### 3. IOPC 1992 Fund limit — incomplete figure
Standard limit is 203 million SDR; conditional step-up under Art. 4(4)(b)
raises it to 300.74 million SDR. Needs a manual read to catch (context-
dependent), not a clean grep target.
GREP: SKIP

### 4. AECS definition
AECS = "Assessment, Examination and Certification of Seafarers" (IMO Model
Course 3.12), aimed at MMD examiners / RO surveyors — NOT a seafarer
simulator/assessment course.
GREP: SKIP

### 5. Resolution currency
Never cite a resolution number without checking whether it has been
superseded. Known case: A.1185(33) is superseded by A.1206(34) for PSC
procedures.
GREP: A.1185(33)

### 6. Merchant Shipping Act — superseded
Merchant Shipping Act 2025 (Act No. 24 of 2025) came into force 15 March
2026, repealing the 1958 Act. DG Shipping renamed DGMA. Flag content that
cites "Merchant Shipping Act, 1958" as current law.
GREP: Merchant Shipping Act, 1958

### 7. ME-GA engine line — discontinued
MAN Energy Solutions discontinued the ME-GA line in November 2024. Flag if
described as an active/current product line.
GREP: SKIP

### 8. MASS Code dates
Adopted MSC 111 (May 2026); effective 1 July 2026. Do not confuse adoption
date with entry-into-force date.
GREP: SKIP

### 9. IMO Net-Zero Framework status
Adoption was postponed at the October 2025 extraordinary MEPC session; next
expected at MEPC 85 (Oct/Nov 2026). Flag if stated as already adopted.
GREP: Net-Zero Framework has been adopted

### 10. Canadian Arctic + Norwegian Sea ECA sulphur date
0.10% sulphur limit takes effect 1 March 2027, not earlier.
GREP: SKIP

### 11. IMO GFI reference value vs FuelEU Maritime baseline — cross-track contamination
The IMO GFI (GHG Fuel Intensity, MEPC 83 / MARPOL Annex VI Chapter 5) reference
value is 93.3 gCO2eq/MJ (2008 fleet-average, well-to-wake). FuelEU Maritime
(EU Regulation 2023/1805) is a separate regulation using the same units and
WtW logic but its own 91.16 gCO2eq/MJ baseline (2020 reference). These are
two distinct regulatory tracks (IMO global vs EU regional) that share
terminology ("GFI"/"GHG intensity") and units, making them easy to conflate.
Caught in QB6_E (Q2, Q3): the file used 91.16 as if it were the IMO GFI
reference and computed reduction targets (2%/6%/14.5%) off the wrong
baseline — those percentages are actually FuelEU's own schedule, not IMO's.
Flagged by a candidate (Rathesh) via annotated screenshot correction.
GREP: SKIP (91.16 is legitimate when correctly attributed to FuelEU Maritime;
the trap is only when it's presented as the IMO GFI reference — needs manual
context check, not a safe auto-grep)

---

## Health-check grep — negation-context noise

The daily `qb_health_check.py` trap scan (`check_known_traps()`) currently
flags a `GREP:` phrase on any occurrence, including when the surrounding
sentence is correctly citing the old/wrong term in order to supersede,
repeal, or debunk it (e.g. "the old Merchant Shipping Act, 1958... has been
replaced by", "supersedes A.1185(33)", "IMO does not designate it 'FAL Form
8'"). Verified 2026-07-19: every trap hit in that day's run (MS Act 1958 x6
files, A.1185(33) x4 files, FAL Form 8 x1 file) was a false positive of
this kind — correctly-framed corrections, not resurfaced errors.

Before treating a future flag as confirmed, check whether the matched line
also contains a negation/supersession marker, e.g.:
- "superseded by" / "supersedes"
- "replaced by" / "replaces"
- "repealed"
- "not... but" / "not the... but"
- "does not designate" / "is not"
- "formerly" / "now succeeded by" / "since replaced by"

If one of these markers appears in the same sentence as the trap phrase,
treat it as likely-correct usage and verify manually rather than flagging
as an error. `qb_health_check.py` should ideally skip-list lines matching
these markers (or downgrade them to a "review" tier instead of "error") to
cut noise in future runs — this is a suggested script enhancement, not yet
implemented.

---

## How to use this file

- Before building any new QB batch or notes part, check the drafted answer
  text against every entry above (not just the auto-greppable ones).
- If a Gemini draft or source text contains a flagged wrong phrasing, it is
  removed and corrected — not relabelled or softened.
- This file is a living document. Every time a correction is made post-build
  (caught by Nixon, a subscriber, or a re-verification pass), add a new
  numbered entry here in the same session: what was wrong, the correct
  version, and a `GREP:` line (exact phrase, or `SKIP` if too generic to
  auto-scan safely).
- The QB health check script (`qb_health_check.py`) auto-scans all live QB
  HTML daily for every non-SKIP `GREP:` phrase — see `check_known_traps()`.
  SKIP entries stay in this file as a manual verification-pass checklist.

---

## Change log

| Date | Entry added | Source |
|---|---|---|
| 2026-07-16 | Initial 10 entries | Compiled from Claude memory / prior correction sessions |
| 2026-07-18 | Entry 11: IMO GFI vs FuelEU Maritime baseline | Candidate (Rathesh) annotated-screenshot correction on QB6_E |
