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
| AMBIGUOUS | 2 | 31 | 30 | 8 | 44 |
| EXACT_MATCH | 0 | 2 | 0 | 0 | 20 |
| MISSING | 45 | 84 | 78 | 2 | 9 |
| NEAR_MATCH | 1 | 6 | 1 | 6 | 26 |
| PARTIAL_COVERAGE | 7 | 53 | 204 | 60 | 45 |
| SAME_CORE_ASK | 0 | 1 | 7 | 7 | 9 |

**236** occurrences have strong or complete Notes support; **55** have no Notes support at all.

## Old P0 gaps against the Notes

| Gap | Examiner | Ask | Canonical | Notes | Likely future disposition |
|---|---|---|---|---|---|
| GAP-0002 | Simon | What is "GIRDING"? | MISSING | COMPLETE | NOTES_TO_QB_PROMOTION_CANDIDATE |
| GAP-0009 | John | STCW 7, 8 | PARTIAL_COVERAGE | NO | NOTES_DO_NOT_CHANGE_GAP |
| GAP-0016 | John | Convention present condition, CONVENTION AND ITS CON | MISSING | PARTIAL | ENRICH_EXISTING_CANDIDATE |
| GAP-0034 | Simon | What is Dual Fuel Engine and Trifuel engine? Cross q | MISSING | TOPIC | NEW_ANSWER_CANDIDATE |
| GAP-0042 | Nair | How as CE to resolve on-board conflict including bul | MISSING | NO | NEW_ANSWER_CANDIDATE |
| GAP-0043 | Nair | Qualities of CE, explain assertiveness, empathy. | PARTIAL_COVERAGE | NO | NOTES_DO_NOT_CHANGE_GAP |
| GAP-0044 | Nair | STCW. To bcm second engineer to chief engineer what  | MISSING | TOPIC | NEW_ANSWER_CANDIDATE |
| GAP-0048 | Nair | If RO is already there, why a shipowner May want to  | MISSING | TOPIC | NEW_ANSWER_CANDIDATE |
| GAP-0069 | John | TIO2 APPLICATION | MISSING | PARTIAL | ENRICH_EXISTING_CANDIDATE |
| GAP-0093 | John | Latest change in medical certificate apart transgend | MISSING | TOPIC | NEW_ANSWER_CANDIDATE |
| GAP-0409 | Nair | Latest technology - ME GA engine explanation, how wi | MISSING | TOPIC | NEW_ANSWER_CANDIDATE |
| GAP-0454 | Nair | UV-Asked few details of the D2 standards and he want | MISSING | TOPIC | NEW_ANSWER_CANDIDATE |
| GAP-0494 | Nair | HKG-Initial Survey done by whom, what all parts in I | MISSING | NO | NEW_ANSWER_CANDIDATE |

- **ENRICH_EXISTING_CANDIDATE**: 2
- **NEW_ANSWER_CANDIDATE**: 8
- **NOTES_DO_NOT_CHANGE_GAP**: 2
- **NOTES_TO_QB_PROMOTION_CANDIDATE**: 1

## Reverse connection value

| Class | Rows |
|---|---|
| ALREADY_HAS_STRONGER_EVIDENCE | 172 |
| NOTE_ADDS_SUPPORT | 196 |
| NOTE_CREATES_NEW_EXPLICIT_CONNECTION | 19 |
| NOTE_UNRESOLVED | 49 |

Nothing here is published. Every row is a candidate for Phase 2A-iii.
