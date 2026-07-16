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
