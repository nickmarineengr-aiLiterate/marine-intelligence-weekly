# Phase 2A-ii - Oral Notes impact on the 788 source occurrences

An analysis, not a baseline. The committed reconciliation is still the
Phase 2 one; Phase 2A-iii performs the definitive recomputation.

## Notes support across all source occurrences

| Notes support | Occurrences |
|---|---|
| NOTES_COMPLETE_SUPPORT | 153 |
| NOTES_STRONG_SUPPORT | 83 |
| NOTES_PARTIAL_SUPPORT | 320 |
| NOTES_TOPIC_SUPPORT | 177 |
| NO_NOTES_SUPPORT | 55 |
| **total** | **788** |

## Notes support against the canonical disposition

The two dimensions are independent. A row that is canonically MISSING
with COMPLETE Notes support is not a gap in MIW's knowledge - it is
knowledge MIW holds outside the canonical question bank.

| canonical \ notes | NO | TOPIC | PARTIAL | STRONG | COMPLETE |
|---|---|---|---|---|---|
| AMBIGUOUS | 3 | 31 | 31 | 8 | 46 |
| EXACT_MATCH | 0 | 2 | 0 | 0 | 20 |
| MISSING | 42 | 80 | 72 | 2 | 6 |
| NEAR_MATCH | 2 | 6 | 1 | 6 | 27 |
| PARTIAL_COVERAGE | 8 | 57 | 208 | 60 | 45 |
| SAME_CORE_ASK | 0 | 1 | 8 | 7 | 9 |

**236** occurrences have strong or complete Notes support; **55** have no Notes support at all.

## Old P0 gaps against the Notes

| Gap | Examiner | Ask | Canonical | Notes | Likely future disposition |
|---|---|---|---|---|---|
| GAP-0009 | John | STCW 7, 8 | PARTIAL_COVERAGE | NO | NOTES_DO_NOT_CHANGE_GAP |
| GAP-0034 | Simon | What is Dual Fuel Engine and Trifuel engine? Cross q | MISSING | TOPIC | NEW_ANSWER_CANDIDATE |
| GAP-0069 | John | TIO2 APPLICATION | MISSING | PARTIAL | ENRICH_EXISTING_CANDIDATE |
| GAP-0093 | John | Latest change in medical certificate apart transgend | MISSING | TOPIC | NEW_ANSWER_CANDIDATE |
| GAP-0454 | Nair | UV-Asked few details of the D2 standards and he want | MISSING | TOPIC | NEW_ANSWER_CANDIDATE |
| GAP-0494 | Nair | HKG-Initial Survey done by whom, what all parts in I | MISSING | NO | NEW_ANSWER_CANDIDATE |

- **ENRICH_EXISTING_CANDIDATE**: 1
- **NEW_ANSWER_CANDIDATE**: 4
- **NOTES_DO_NOT_CHANGE_GAP**: 1

## Reverse connection value

| Class | Rows |
|---|---|
| ALREADY_HAS_STRONGER_EVIDENCE | 163 |
| NOTE_ADDS_SUPPORT | 203 |
| NOTE_CREATES_NEW_EXPLICIT_CONNECTION | 13 |
| NOTE_UNRESOLVED | 57 |

Nothing here is published. Every row is a candidate for Phase 2A-iii.
