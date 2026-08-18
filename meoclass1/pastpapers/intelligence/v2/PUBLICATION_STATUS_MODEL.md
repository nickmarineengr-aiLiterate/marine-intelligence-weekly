# Publication status model

**RESEARCH ONLY.** `current_as_of: 2026-08-17`

---

## 1. The lifecycle

```
RESEARCH_HYPOTHESIS
      ↓   the two stems are read as text and classified
TEXT_VERIFIED
      ↓   the earlier SITTING and its date are evidenced
DATE_VERIFIED
      ↓   the Laptop independently reproduces the finding
LAPTOP_VERIFIED
      ↓   the Founder approves what a candidate will see
FOUNDER_APPROVED
      ↓   the claim reaches a candidate-facing page
CANDIDATE_PUBLISHED
```

**One step at a time.** A claim may not jump from `RESEARCH_HYPOTHESIS` to
`CANDIDATE_PUBLISHED`.

---

## 2. Gates, and what enforces them

| Gate | Requirement | Check |
|---|---|---|
| → `TEXT_VERIFIED` | `text_similarity_confidence == HIGH` | `C22` |
| → `DATE_VERIFIED` | `date_confidence == HIGH` | `C21` |
| → `LAPTOP_VERIFIED` | independent Laptop reproduction | manual |
| → `FOUNDER_APPROVED` | Founder decision on candidate wording | manual |
| → `CANDIDATE_PUBLISHED` | all of the above, no unresolved source conflict | `C23` |
| Phase 2 ceiling | **nothing may be `CANDIDATE_PUBLISHED`** | `C23` |

`C23` currently fails any family marked `CANDIDATE_PUBLISHED`, unconditionally. That
is the Phase-2 instruction expressed as code rather than as a promise.

---

## 3. The point of the model

**A claim can be certain and unpublishable at the same time.**

`FAMILY-EM-0001` — the lay-up question — is the worked example:

| | |
|---|---|
| `text_similarity_confidence` | **HIGH** — containment 1.00/1.00 against `BANK-015` |
| `source_confidence` | **HIGH** — the Directorate's own published question bank |
| `date_confidence` | **NONE** — the bank is undated; no sitting is proven |
| `publication_status` | `TEXT_VERIFIED` — and it stops there |

The recurrence is as well evidenced as anything in this corpus. The candidate may
still never be shown a date, because there is no date. `C21` makes the ceiling
mechanical: `DATE_VERIFIED` is unreachable while `date_confidence` is anything but
`HIGH`.

This is the structural answer to the H1–H5 problem. Phase 1's difficulty was that a
single `confidence` field forced a choice between overstating the date and
understating the recurrence. It no longer does.

---

## 4. Current status of every family

| Family | Subject | Text | Date | Source | Status |
|---|---|---|---|---|---|
| `FAMILY-EM-0001` | lay-up reactivation | HIGH | **NONE** | HIGH | `TEXT_VERIFIED` |
| `FAMILY-EM-0002` | dry dock coordination | HIGH | **NONE** | HIGH | `TEXT_VERIFIED` |
| `FAMILY-EM-0003` | motivation / human element | HIGH | HIGH | HIGH | `TEXT_VERIFIED` |
| `FAMILY-EM-0004` | marine insurance warranties | HIGH | HIGH | HIGH | `TEXT_VERIFIED` |
| `FAMILY-EM-0005` | information flow, multinational crew | MEDIUM | NONE | HIGH | `RESEARCH_HYPOTHESIS` |
| `FAMILY-EM-0006` | IMO GHG developments | HIGH | HIGH | HIGH | `TEXT_VERIFIED` |
| `FAMILY-EM-0007` | marine insurance, four-limb short notes | HIGH | **NONE** | HIGH | `TEXT_VERIFIED` |

**Nothing is `CANDIDATE_PUBLISHED`.** For the seven families above, nothing reaches
`DATE_VERIFIED` either — because `DATE_VERIFIED` means the *earlier* sitting is
dated, and for `EM-0003`, `EM-0004` and `EM-0006` the earlier sittings are MIW-held
papers whose dates are anchored, while the *deeper* history behind them is not.

Two families added after this table was written, `FAMILY-EM-0008` and
`FAMILY-EM-0009`, **do** reach `DATE_VERIFIED`: each rests on five MIW-held sittings
whose dates are anchored, and `C21` passes on both. Reaching `DATE_VERIFIED` clears
the date gate alone; it is not a candidate-publication threshold, which §5 below
still governs.

---

## 5. Candidate threshold

Before any recurrence claim reaches a candidate, **all** of:

1. HIGH similarity confidence
2. historical text available and readable
3. historical **sitting and date** verified
4. Laptop verification
5. no unresolved source conflict
6. Founder approval

A temporal delta additionally requires:

7. verified **current** authority — MIW True Source or a primary instrument
8. material usefulness to the candidate
9. candidate-safe wording

Item 3 is the one that currently stops everything with an interesting history, and
it should keep stopping it until a dated official sitting paper is in hand.

---

## 6. Where a claim may appear before it is published

`RESEARCH_HYPOTHESIS` and `TEXT_VERIFIED` claims live in this directory and nowhere
else. They may inform internal review. They may not render on a candidate page, feed
a Study Guide block, or appear in an Exam Plan bullet.
