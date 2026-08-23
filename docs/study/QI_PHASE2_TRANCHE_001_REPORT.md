# QI Phase 2 — Tranche 001

**Date:** 2026-08-23 · **Baseline:** `5acbb42` · **Scope:** ten families, then stop.

Phase 1 built one governed recurrence brain for 2010→August 2026. It answers
*what keeps coming back*. Phase 2 answers the harder question — *is it safe to
study this today* — and this is the first tranche of that work.

---

## 1. The finding that shaped the tranche

The brief asked for current answers to be written into the canonical Written
source. **That cannot be done to a past-paper answer**, and the reason is in
the product's own governing rule:

> Every answer must be true as at the date of its own examination sitting —
> not as at today.
> — `TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md` §1

Several of the selected answers say so themselves. `QP2402-Q5` records that it
"must never be reused at a later sitting" and that "a reviewer reading it after
2025 must not 'correct' it to the current position". `QP2509-Q5` records that
"the answer must NOT be updated to the current position".

So Phase 2 splits every change in two:

| Situation | Class | Action |
|---|---|---|
| Answer was already wrong **at its own sitting** | `CORRECTION` | Edit `model_answer` — this *restores* sitting-anchoring |
| Framework moved **after** the sitting | `MODERNISATION` | Leave the answer; record the present-day position at family level |

The present-day layer lives in `tools/study/qi_phase2_adjudications.json`,
hand-maintained, the natural next member of the family that already contains
`qi_phase1_adjudications.json` and `study_qi_holds.json`. No new architecture
was invented; `R-P2-MODERNISATION-NOEDIT` enforces the split.

---

## 2. Selection

Actionable pool (not `READY_TO_STUDY_NOW`, action in the four working states):
**107**. Taken in canonical `phase2_rank` order, frozen at ten. `QIF-EM-0031`
was rank 11 and deliberately excluded so the tranche cost is measurable.

| Rank | Family | Topic | 3Y/5Y/10Y/Full | Final state |
|---|---|---|---|---|
| 1 | QIF-EM-0082 Classification societies, survey types | D01 | 4/6/6/6 | CURRENT_AND_VERIFIED |
| 3 | QIF-EM-0036 Human element in STCW; fatigue | D03 | 6/7/9/10 | **UPDATED_AND_VERIFIED** |
| 4 | QIF-EM-0007 Flag-State casualty investigation | D04 | 4/5/9/17 | CURRENT_AND_VERIFIED |
| 5 | QIF-EM-0012 Unseaworthy vessels, MS Act | D06 | 4/5/7/14 | **MODERNISED_AND_VERIFIED** |
| 8 | QIF-EM-0104 High-efficiency propellers | D05 | 3/5/5/5 | CURRENT_AND_VERIFIED |
| 14 | QIF-EM-0017 IMO GHG ongoing developments | D05 | 2/2/4/13 | **SUPERSEDED_WITH_SUCCESSOR** |
| 18 | QIF-EM-0129 HNS Convention | D04 | 2/4/4/4 | **MODERNISED_AND_VERIFIED** |
| 19 | QIF-EM-0013 Communication and its barriers | D03 | 2/3/13/13 | CURRENT_AND_VERIFIED |
| 21 | QIF-EM-0128 Maritime cyber risk management | D03 | 3/4/4/4 | **MODERNISED_AND_VERIFIED** |
| 24 | QIF-EM-0023 UNCLOS flag-State duties | D01 | 1/3/11/11 | **MODERNISED_AND_VERIFIED** |

**Every selected family was `EXISTING_CURRENT_ANSWER_VERIFY`.** Not one was
`NEW_ANSWER_REQUIRED`. The top of the ranking is verification work, not
authoring work — which matters for costing tranche 002.

---

## 3. What current authority actually said

Four families were unchanged. Six had moved.

**QIF-EM-0128 — the bearer predicted its own obsolescence by name.**
`QP2510-Q5` carried a currency flag asking whether a **Rev.4** of the cyber
guidelines had appeared "which a later editor might wrongly back-date".
`MSC-FAL.1/Circ.3/Rev.4` was issued **28 May 2026** (FAL 50, MSC 111) and was
read in full from the IMO CDN. The delta is smaller than the revision number
suggests: the **six** functional elements (Govern first) and the **nine**
vulnerable-system heads both carry over unchanged. The real change is
definitional — the guidance is now built around **Computer Based Systems**,
with IT and OT defined as kinds of CBS and two new definitions added. Both
counts were *counted in the Rev.4 text*, not assumed to have moved; much
published material still says five elements, so working from secondary sources
could have "corrected" a right answer into a wrong one.

**QIF-EM-0012 — the governing statute was replaced entirely.**
`s.324(1)` of the Merchant Shipping Act, 2025 repealed the 1958 Act from
**15 March 2026**. The whole spine of the sitting-anchored answer (1958
ss.334–336) is no longer live law. Full provision map, read verbatim in the
Gazette text:

| 1958 Act | 2025 Act |
|---|---|
| s.334 definition | **s.2(69)** — substantively the same test |
| s.335 sending unseaworthy ship to sea | **s.127** — now liability to **penalty**, not offence |
| s.336 owner's obligation | **s.128(1)** implied obligation; **s.128(2)** survey power |
| detention of unsafe ships | **s.278**, **s.307** (with the "unsafe vessel" Explanation), **s.308** costs |
| seafarer's refusal | **s.98(2)** — reasonable cause, subject to prior complaint |

**QIF-EM-0129 — the premise of the question was overtaken.**
The 2010 HNS Convention's entry-into-force conditions were met on
**29 May 2026**; it enters into force on **29 November 2027**. Twelve
Contracting States, nine above 2 m GT, >40 m tonnes contributing cargo for the
2025 reporting year, 250 m SDR cap. Still **not in force** at August 2026.

**QIF-EM-0017 — thirty months stale, but no new answer was needed.**
The bearer answers February 2024, five weeks before MEPC 81. Present position:
the Net-Zero Framework is **approved, not adopted**; MEPC/ES.2 (14–17 Oct
2025) adjourned; MEPC 84 (27 Apr–1 May 2026) preserved it as the basis for
negotiation; the resumed session is **Friday 4 December 2026**. MIW already
holds a current-facing answer — `QP2602-Q8` (February 2026) — so the study
route was moved rather than a new answer written.

> The date mattered. Widely repeated secondary material still says the session
> resumes "around October 2026", which was all that was knowable in February
> 2026. The date was fixed at MEPC 84 as **4 December 2026**. Taking the older
> wording would have reproduced an error this organisation has already had to
> correct once on a live surface.

**QIF-EM-0023 — the Indian naming has settled.** `s.7(1)` of the 2025 Act
creates the **Director-General of Maritime Administration**, in Chapter II
headed *Maritime Administration*. UNCLOS Articles 91/92/94/217 unchanged.

---

## 4. The one answer that was actually edited

`QP2602-Q4` (February 2026) asks how the human element is addressed in the
STCW Code. **Resolution MSC.560(108)** entered into force on **1 January
2026 — six weeks before that sitting** — adding to STCW Code table A-VI/1-4 a
competence on *contributing to the prevention of and response to violence and
harassment, including sexual harassment, bullying and sexual assault*.

It was absent. That is a defect **at the answer's own sitting date**, not a
later development, so it was added rather than deferred to a study note.
Nothing post-dating February 2026 was introduced and limb (B) is untouched.

Evidence class: `COMPETENT_AUTHORITY_RESTATEMENT` — two national maritime
administrations, MIW holding no licensed STCW Code. This is the same class the
corpus already accepts for the Manila rest-hour figures, and it is labelled as
such rather than claimed as primary.

---

## 5. Two defects found in this work, and fixed

**`answer_coverage` was `None` on all 270 families.** The adapter read
`answer_coverage_state` / `answer_coverage`; the queue writes
`existing_answer_status`. Neither name ever existed, so the field was silently
empty corpus-wide. A `CORRECTION`.

**A Phase-2 grant was reaching a whole family, not one answer.** On first
propagation, resolving `QIF-EM-0017` marked `QP2402-Q5` **READY** — the very
answer whose record forbids reuse — while its successor still read `VERIFY`.
Exactly backwards. `question_readiness()` now grants readiness only to the
question the record NAMES; `R-P2-ANSWER-SCOPE` gates it and mutation 13 proves
the gate bites. Workbook impact: +9 questions ready, not +37.

---

## 6. Propagation

| | Before | After |
|---|---|---|
| READY_TO_STUDY_NOW | 72 | **82** |
| VERIFY_CURRENT_ANSWER | 59 | **49** |
| Blocked families | 107 | **97** |
| Workbook questions ready | 145 | **154** |

Topic readiness moved in five topics — D01 59.0→64.1%, D03 40.0→52.0%,
D04 28.6→42.9%, D05 26.3→36.8%, D06 33.3→50.0%.

**Roadmap rank and every recurrence score are unchanged.** That is the correct
outcome: recurrence drives priority, readiness drives safety, and Phase 2
moves only the second. QI family count (270) and recurrence-bearing occurrence
count (1,584) are unchanged and gated.

Active study sequence D01 → D03 → D02 untouched; `study_progress.json` is
hand-maintained and no generator writes it.

---

## 7. Conflict hold

`SQI-CONF-004` was the only one of the seven NEAR_REPEAT holds naming a
selected family, so it was adjudicated and no other was touched.
**LEGITIMATE_RELATED_BUT_DISTINCT**: six members ask about the *role* of
classification societies (QIF-EM-0082); `QP2310-Q2` asks the *purpose of annual
surveys* (QIF-EM-0073). The canonical split is right; the inferred cluster
over-reached by one member. No member, occurrence or count moved —
`RESOLVED_CANONICAL` records the decision and releases the block.

---

## 8. Open findings, deliberately not fixed here

1. **`audit_paper.py` check 11 fails on every published paper.** It rebuilds
   in review mode while the committed pages are `--publish` builds. Verified
   identical on untouched `QP2601`. Pre-existing; not mixed into this tranche.
2. **`topics.html` and `study_spine.json` carry no readiness at all.**
   Readiness reaches `study_qi.json` and the workbook but no candidate-facing
   topic page. A product gap, not a regression.
3. **`QP2604-Q8` paragraph-numbering flag left OPEN.** MIW holds no current
   consolidated Casualty Investigation Code, so the numbering cannot be
   positively confirmed. Discharging it would have been the easy, wrong call.
4. **North-East Atlantic ECA effective dates not established** — named, dates
   omitted rather than guessed.

---

## 9. Gates

- `validate_phase2_tranche.py` — **30 invariants**, fails closed
- `test_phase2_mutations.py` — **13 mutations, 13 caught, 0 escaped, 0 residue**
- 4 study validators PASS · 8 acceptance suites PASS · 8 builder `--check` OK
- Oral product diff: **0**

## 10. Cost, and the recommendation for tranche 002

Ten families took one long session. The expensive part was **not** authoring —
nothing needed a new answer. It was obtaining primary authority: India Code was
Akamai-blocked and a guessed Gazette number returned an unrelated Road
Transport notification. What worked was a `CG-DL` identifier recorded in a
*previous* MIW verification record, which reconstructed the eGazette URL.
Provenance metadata written for audit turned out to be a working retrieval key.

**Recommend tranche 002 at 12–15 families**, biased toward the
`NEW_MODERN_ANSWER_REQUIRED` band, which this tranche never touched and whose
cost is therefore still unmeasured.
