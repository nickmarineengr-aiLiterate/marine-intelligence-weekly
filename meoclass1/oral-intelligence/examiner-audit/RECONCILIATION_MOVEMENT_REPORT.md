# Movement from the Phase-2 baseline

Baseline `de6d3f2`. A row that keeps its disposition but changes target has still moved and is counted separately.

- disposition changed: **135**
- target changed only: **208**
- unchanged: **445**

## Reasons

| Reason | Rows |
|---|---|
| DESIGNATOR_CONFLICT_FIX | 5 |
| HUMAN_ADJUDICATION | 3 |
| OTHER_EXPLAINED | 21 |
| SAME_CORE_FLOOR | 51 |
| SPELL_REPAIR_SAFETY | 42 |
| TARGET_RESELECTION | 13 |

## Transitions

| From → to | Rows |
|---|---|
| PARTIAL_COVERAGE -> MISSING | 29 |
| SAME_CORE_ASK -> AMBIGUOUS | 28 |
| SAME_CORE_ASK -> PARTIAL_COVERAGE | 22 |
| MISSING -> PARTIAL_COVERAGE | 17 |
| PARTIAL_COVERAGE -> AMBIGUOUS | 15 |
| AMBIGUOUS -> PARTIAL_COVERAGE | 11 |
| AMBIGUOUS -> MISSING | 3 |
| AMBIGUOUS -> SAME_CORE_ASK | 3 |
| MISSING -> AMBIGUOUS | 2 |
| PARTIAL_COVERAGE -> SAME_CORE_ASK | 2 |
| EXACT_MATCH -> SAME_CORE_ASK | 1 |
| NEAR_MATCH -> PARTIAL_COVERAGE | 1 |
| SAME_CORE_ASK -> MISSING | 1 |
