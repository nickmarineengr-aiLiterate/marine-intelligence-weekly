# CANDIDATE FEEDBACK AUDIT — 2026-08-12

**Trigger.** Two pieces of real candidate feedback.

1. *Understand mode* — "in the 'understand' column, the use of more accessible/friendly language
   would enhance comprehension. This would allow candidates to write effectively even if they forget
   the technical terms."
2. *Handwritten notes* — a second candidate supplied study notes and said some MIW answers may be
   missing important points.

**Verdict: FEEDBACK PARTIALLY VALIDATED — TARGETED IMPROVEMENTS PUBLISHED.**

**Starting main** `4a3f102` · corpus verified at 20 available papers, 180 published questions,
72 unsolved, 8 unsolved papers.

---

## 1. Scope and method

The notes were treated as a **discovery aid only**. No claim was copied into MIW because a candidate
wrote it. Every proposed addition was independently verified against primary source; every rejected
claim was checked before rejection, so the Founder can say *"we checked it"* rather than *"we did not
use it"*.

The transcription supplied is a 19-fragment JSON array — one fragment per note image, unordered. The
original images sit alongside it. It was read in full; the images were not re-OCR'd, because the
transcription was internally consistent enough to adjudicate every proposition against MIW.

Route followed: candidate feedback → discovery → current MIW content → question relevance → primary
verification → adjudication → targeted improvement.

---

## 2. The notes map onto the live corpus almost exactly

This is the single most useful structural finding. The candidate is studying the **same question
set** MIW has built. Four of the five note clusters reproduce a printed MIW question near-verbatim:

| Note fragment | MIW question |
|---|---|
| "Explain the provisions under UNCLOS that mandates…" | **QP2604 Q7** (and QP2601 Q7) |
| "state the applicable regulations of SOLAS and MARPOL…" | **QP2601 Q8 / QP2604 Q8 / QP2506 Q7** |
| "Maritime industries have taken several initiatives…" | **QP2403 Q1 / QP2510 Q1** |
| "Q8. What are the principles of modern salvage law" | **QP2601 Q3 / QP2604 Q3** |
| "Q2. a) Define wreck as per the wreck convention…" | **QP2501 Q1 / QP2507 Q1** — *not yet solved* |

A keyword sweep of all 252 questions matched **49** on the note topics, of which **35 are solved and
live**. The last row is worth noting on its own: the candidate is revising a wreck-convention
question that sits in Batch 2 and has not been authored yet. That is demand evidence, not a defect.

---

## 3. Coverage matrix — 68 propositions extracted from the notes

| Class | Count | Meaning |
|---|---|---|
| **A** already covered clearly | 52 | MIW states it, in the right question |
| **B** covered but buried | 3 | present in a sibling question, not the one the note came from |
| **C** partially covered | 1 | substance present, a named cut missing |
| **D** useful missing exam point | **1** | genuinely absent, verified, added |
| **E** valid but outside target question | 3 | correct, but does not answer the printed limb |
| **G** duplicative / low value | 1 | true, earns no marks |
| **H** incorrect | 8 | rejected on primary evidence |
| **I** unverified / insufficient evidence | 1 | could not be substantiated; not used |
| **J** transcription uncertain | 3 | note internally inconsistent |

The headline: **out of 68 candidate propositions, exactly one was a genuine missing scoring point.**
MIW's content is in strong shape. Eight propositions were positively wrong.

---

## 4. The one genuine content gap — SOLAS regulation I/21(b)

**Candidate proposition.** "This report to the IMO should be in the anonymous form and should not
disclose identity or nationality of the ships concerned or fix a responsibility upon any ship or
person."

**Current MIW state.** All three CIC questions stated regulation I/21 **paragraph (a) only** — the
Administration's undertaking to investigate. Paragraph (b) was absent. MIW's own verification record
confirms why: MSC.255(84) was read in full, but I/21 had only ever been reached *through* the Code's
cross-reference in chapter 7, never read in its own text.

**Primary verification.** SOLAS Consolidated Edition 2018, chapter I part C regulation 21, read
verbatim:

> **(b)** "Each Contracting Government undertakes to supply the Organization with pertinent
> information concerning the findings of such investigations. No reports or recommendations **of the
> Organization** based upon such information shall disclose the identity or nationality of the ships
> concerned or in any manner fix or imply responsibility upon any ship or person."

**Adjudication.** The candidate was **right that the provision exists and that MIW had missed it**.
He was **wrong about who it binds**. The non-disclosure duty falls on **IMO's own reports and
recommendations** — not on the investigating Administration's report. His formulation would have a
flag State anonymising its own findings, which regulation 21 does not require.

**Action.** Added to **QP2601 Q8, QP2604 Q8, QP2506 Q7**, stated correctly, with an explicit line
locating the duty. Sources, `regulations`, and search aliases updated; `P1_PRIMARY_VERIFIED`
incremented; a verification addendum written to all three records.

**Where MIW was already ahead of the notes.** All three answers already carry **SOLAS XI-1/6** — the
provision that actually makes casualty investigation *mandatory* — and already distinguish it from
I/21's discretionary undertaking. The notes miss XI-1/6 entirely and treat I/21 as the mandatory
hook. A candidate relying on the notes alone would answer limb (a) wrongly.

---

## 5. The partial gap — big-data classification

The printed question says *"Define the concept of big data"*. MIW covered the five Vs and the
data-versus-information distinction, but never named the **structured / semi-structured /
unstructured** cut, which the notes do. Substance was present under *Variety*; the named taxonomy was
not. Added as one clause inside the existing definition of **QP2403 Q1** and **QP2510 Q1** — not as a
new section, because it is worth about a line.

---

## 6. Rejected note points — with the evidence

These matter most for the reply to the candidate.

| # | Candidate claim | Verdict | Evidence |
|---|---|---|---|
| 1 | "The York-Antwerp Rules **2018**" | **Incorrect** | No 2018 edition exists. Editions are 1994, 2004, 2016. MIW cites **YAR 2016** 107 times and 1994 22 times, and never 2018. |
| 2 | Article 14 uplift is "**25 ~ 100%**" | **Incorrect** | Article 14(2): increase up to **30%** of expenses, and a tribunal may go to a maximum of **100%**. The 25% he is thinking of is **SCOPIC's** tariff bonus — a different, contractual instrument. MIW states 30/100 correctly and keeps SCOPIC's 25% bonus and 25% discount separate. |
| 3 | "Shipping contributes **85%** of the world's GHG emissions" | **Incorrect, by roughly thirty times** | Fourth IMO GHG Study 2020, via MEPC.377(80) §1.8: shipping was some **2.89%** of global anthropogenic GHG in 2018. MIW already carries the correct figure on QP2409 Q3. 85% is close to the share of *world trade by volume* carried by sea — two different facts collided. |
| 4 | The report to IMO must be anonymised by the flag State | **Incorrect attribution** | See §4. The duty binds the Organization's output. |
| 5 | "**Rule B** — no GA contributions if ship and cargo are totally lost" | **Incorrect** | YAR Rule B concerns a common maritime adventure between vessels towing or pushing. |
| 6 | "**Rule D** — adjustment carried out … *without due regard to fault*" | **Incorrect / garbled** | Rule D preserves contribution rights *notwithstanding* fault, leaving remedies intact. The note inverts the sense. |
| 7 | Constitution **Article 51(c)** "directs the individual state governments" | **Incorrect** | Article 51 binds "the State" in the Article 12 sense — principally the Union. MIW's QP2604 Q7 is clean on this. |
| 8 | "No cure, no pay — compensated if the operation is **partially successful**" | **Loose to the point of wrong** | The test is a **useful result**. MIW states it correctly. |
| 9 | India registration threshold "**15 tonne or less**" | **Unverified** | Could not be substantiated to a current primary source within scope; the MS Act 2025 changed this area. Not used. MIW does not rely on a tonnage threshold anywhere. |

**Transcription uncertainties (not counted against the candidate).** Rule C is given text identical
to Rule A; "M.S act, 2025 aligns with M.S act 2025" is a duplication; "This will be artificial as big
data analysis is carried out in real time" is almost certainly "beneficial". None affected the
outcome.

**Correctly rejected as out of scope, not wrong.** MARPOL **Article 8** (reports on incidents
involving harmful substances) is accurate but answers *reporting*, not *"under which it is mandatory
to conduct an investigation"* — MIW carries it on QP2607 Q2, where it belongs. **Vetting** likewise:
it is not a limb of MIW's printed big-data question, and MIW has three separate vetting questions.

---

## 7. Corpus-wide defect propagation sweep

Because one error class can hide several instances, all ten candidate error classes were swept across
**all 252 questions**, not merely the matched ones.

**Result: clean. Zero of the candidate's errors have propagated into MIW.** No YAR 2018, no 25%
Article 14 uplift, no inflated GHG share, no anonymity misattribution, no Rule B total-loss bar, no
Article 51 misstatement, no "severe marine pollution" in place of the Code's "severe damage to the
environment".

---

## 8. Understand-mode audit

**Reviewed:** all 180 solved questions measured; the 35 note-matched questions read.

### What the measurement actually showed

| Metric | Result |
|---|---|
| Solved questions carrying an Understand section | **167 / 180** |
| Median length | 121 words |
| Median citation density | **0.0 per 100 words** |
| Sections opening on a real numbered citation | **2** (and one is a false positive — "The rule is simple and the engineering is not") |
| Sections addressing *the examiner* rather than the subject | 18 |

**A correction to an earlier reading in this audit.** A first pass suggested 25 sections opened on a
citation. That was an artefact of a loose pattern that counted the ordinary English words "rule" and
"regulation". Measured tightly, the real number is **one**. Understand mode is **not** a regulation
dump, and the "too technical" complaint is not a citation-density problem.

### The three real defect classes

**U1 — the mode was absent (13 questions).** Not a schema breach: `understand_first` is *conditional*
by design, present only where a topic has a counter-intuitive core. But each of these 13 has one —
ECA changeover (the compliant fuel must *already* be burning), FSA (a regulator's tool, not a
shipboard risk assessment), goal-based standards (goal versus prescription), entry into force
(adoption binds nobody), IACS/RO (one body, two legal roles), ship operating costs (bunkers are a
*voyage* cost). Filling them applies the existing rule; it does not change it.

**U2 — examiner-voice substituting for explanation.** The clearest case, and precisely the candidate's
complaint. QP2403 Q1 / QP2510 Q1 opened *"The examiner is not asking what big data is in general"* and
then contained **no explanation of what big data is at all**, despite the printed limb reading "Define
the concept of big data". That section fails the reconstruction test outright: delete the bold terms
and nothing remains to reconstruct from.

**U3 — term-dense and idea-thin.** QP2601 Q7 / QP2604 Q7 named *administrative, technical and social
matters* and *generally accepted international regulations* without ever saying, in ordinary words,
what those cover. The candidate's own handwritten gloss — "administrative = survey, stopping a vessel,
fining; technical = strength, stability; social = MLC" — was **more useful than ours**. The feedback
landed exactly where the measurement says it should.

### Reconstruction test

Applied to the 35 note-matched sections: **29 PASS, 6 FAIL.** All six failures were fixed. Extrapolated
across the corpus the problem is **LOCAL-TO-MODERATE, not systemic** — which is why no blind rewrite
was performed and 161 sections were left untouched.

---

## 9. What changed

**Content (3 questions).** SOLAS I/21(b) added to QP2601 Q8, QP2604 Q8, QP2506 Q7.

**Answer enrichment (2 questions).** Structured/semi-structured/unstructured taxonomy into the big-data
definition, QP2403 Q1 and QP2510 Q1.

**Understand filled — 13 questions** (QP2511 Q8; QP2602 Q3, Q7; QP2603 Q1, Q8, Q9; QP2604 Q2;
QP2606 Q1, Q4, Q6; QP2607 Q2, Q3, Q4).

**Understand rewritten — 6 questions** (QP2403 Q1, Q3; QP2510 Q1, Q3; QP2601 Q7; QP2604 Q7).

**Untouched: 161 of 180 Understand sections.** No Model Answer was rewritten. No route, Exam Plan or
Recall was restructured — the single spine is preserved throughout.

### Representative before / after

**QP2510 Q1 — Big Data.** *Problem:* no explanation of the subject; pure exam strategy plus one dated
fact duplicated from the Answer.

> **Before** — "The examiner is not asking what big data is in general - he is asking what it is FOR…
> First, one hard dated fact: the Maritime Single Window became MANDATORY on 1 January 2024…"

> **After** — "Big data is not simply *a lot of data*. What makes it a different kind of problem is
> that it arrives faster than anyone can look at it, in forms that will not sit in neat rows and
> columns, from sources of very uneven trustworthiness - and it is worth nothing at all until
> something turns it into a decision. … A sensor logging a bearing temperature every second has
> produced **data**; a system that notices the trend and has the bearing renewed before it fails has
> produced **value**."

*Why easier to recall:* the five Vs are now derived from an image the candidate can rebuild.
*Accuracy preserved:* the MSW fact was verified as still present in both the Answer and Recall before
removal, so nothing was lost.

**QP2601 Q7 — UNCLOS.** *Problem:* named the formal terms without the plain idea.

> **After** — "…the State has to exercise real control, not merely bank the registration fee. That
> control is described under three heads - the paperwork and enforcement side, the physical condition
> of the ship, and the conditions of the people living and working aboard her - which the Convention
> calls **administrative, technical and social** matters."

*Why easier to recall:* a candidate who forgets the phrase still has three usable headings. This is
the two-layer pattern the feedback asked for.

**QP2403 Q3 — General Average.** *Problem:* strong opening, then examiner-voice for the whole middle.

> **Before** — "The examiner has asked for THREE things in limb (a) … and contribution is the one
> candidates never reach."

> **After** — "The half that gets dropped is **contribution** - who pays, and how much. The logic is
> only proportion: everyone whose property arrived safely owes a share measured by what that property
> was worth on arrival, because that value is the measure of what the sacrifice bought them."

*Why easier to recall:* it now teaches the contribution rule instead of reporting that candidates
forget it.

**QP2607 Q4 — ECA changeover.** *Problem:* Understand absent entirely.

> **New** — "The rule is simple and the engineering is not. At the moment you cross the boundary, the
> fuel *actually burning* must already be inside the limit - not the fuel you have just begun pumping.
> That word **already** is the whole question, because a fuel system is not a tap."

---

## 10. The new Understand-mode standard

Recorded in `MIW_LEARNING_METHOD_DESIGN.md` §10 (clarification, not an architecture change — the
conditional gate is unchanged) and made mandatory for Batch 2 onward in
`DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §10.1.

Understand answers one question: **can I remember and explain the idea even if I forget the official
term?**

**Acceptance criterion — the reconstruction test.** Delete every bold term. If what remains still lets
a candidate rebuild the shape of a decent answer, it passes.

1. Open on the situation or problem, in ordinary words — never on a citation.
2. Explain the mechanism: cause, effect, what follows from what.
3. Plain idea first, formal term second.
4. No dates, resolution numbers or article numbers — those live in Answer and Recall.
5. Describe limbs conceptually; never address the examiner.
6. Length follows the job: ~120 words typical, ~200 where the question has two unrelated halves.
7. Stay question-specific and keep the same spine as Exam Plan, Answer and Recall.

A useful consequence of rule 4: an Understand section carrying no dates is **sitting-independent** and
transfers unchanged across an exact-recurrence family — the one part of an answer object that may.

---

## 11. Automated checking — assessed, deliberately limited

A "friendly language score" would be noise and was not built. Three checks are deterministic and
worth having; they were run manually here and are recommended as reviewer guidance rather than a
blocking gate:

- **Understand present where a counter-intuitive core exists** — cannot be automated; reviewer judgement.
- **Citation density in Understand** — deterministic and cheap, but the corpus median is already 0.0,
  so a gate would fire on nothing. Not worth wiring.
- **Literal "the examiner" in Understand** — deterministic, precise, and caught the real defect class.
  **Recommended** as a review-time warning, not an error: several uses are legitimate hinges.
- **Understand near-verbatim from Answer** — deterministic (8-gram overlap) and it **found something**.
  Corpus median overlap is **0.0%**, but **QP2410 Q5 (FAL Convention) sits at 32.2%**: its *Answer*
  opens by repeating the Understand section almost word for word. Its exact-recurrence sibling
  **QP2511 Q7 measures 1.4%**, which shows the intended shape and proves this is drift on one
  question, not a class.

  **Left unfixed on purpose, and flagged for a Founder decision.** The redundancy is stylistic, not a
  learning failure — no candidate is misled — and the fix would mean editing a *Model Answer* opening,
  which is the scored artefact. That is a larger risk than the defect, and it sits outside the
  note-driven scope this session verified. Recommend it as a one-line cleanup in the next QP2410 touch.
  **Recommended as a standing check** at a 20% threshold: one real hit, zero false positives.

---

## 12. QA

| Check | Result |
|---|---|
| `run_toolchain.py` | ALL STAGES PASS — 239 warnings (identical to baseline) |
| `run_toolchain.py --self-test` | ALL STAGES PASS |
| solvedqp_check / --self-test | OK across 27 / 29 pages |
| coverage_check / --self-test | PASS |
| health_check | 0 errors, 0 warnings |
| solvedqp_health_check / --self-test | PASS · 13/13 |
| solvedqp_search_test / --self-test | 13/13 |
| sample_check · questions_year_check · recurrence_check · known_traps_check | OK · OK · 0 failures · 205 checks, 0 failures |
| **Security regression** | **121 / 121 pass, 0 fail** — unchanged from baseline |
| **Determinism** | double build, **105 artefacts byte-identical** |
| Gating / publish state | no change — no diff on noindex, gated, paywall or withheld markers |
| UI 1280 and 375 | Understand renders, mode switching works, no horizontal overflow, no broken anchors |

---

## 13. Founder-facing candidate feedback summary

**What we reviewed.** Both pieces of feedback in full. 68 discrete propositions extracted from the
handwritten notes and adjudicated one by one against the live corpus; all 180 solved Understand
sections measured; 35 read in detail.

**What the candidates were right about.**
- *Understand mode.* Right, on a minority of questions, and right about the mechanism — some sections
  named the formal term without ever giving the plain idea, and two contained no explanation of the
  subject at all. Fixed on 19 questions, and the standard is now written down so it cannot drift back.
- *The notes.* Right that something was missing. **SOLAS regulation I/21(b)** was genuinely absent from
  all three casualty-investigation answers, and it is now in, verified against the Convention text.

**What was already covered.** 52 of 68 propositions, including the whole Casualty Investigation Code
chapter structure, all five Vs of big data, the York-Antwerp principles, contribution and adjustment,
the six criticisms of general average, the Salvage Convention's voluntary-service and no-cure-no-pay
tests, Article 13 and Article 14, UNCLOS Article 94 and Article 217, and India's constitutional
mechanism under Articles 253, 297 and 51 with the Union List.

**What we added.** SOLAS I/21(b) to three questions; the structured/semi-structured/unstructured
classification to two.

**What we did not use, and why.** Eight propositions were wrong on primary evidence — the most
consequential being the York-Antwerp "2018" edition (no such edition), the Article 14 uplift as
"25–100%" (it is 30%, then up to 100% — the 25% belongs to SCOPIC), and shipping as "85% of world
GHG" (it is about 2.89%; 85% is roughly the seaborne share of world *trade*). One could not be
verified and was left out. Three were transcription artefacts, not candidate errors.

**One thing worth telling him directly.** On the casualty question his notes treat SOLAS I/21 as the
provision that makes investigation mandatory. It is not — it is discretionary, and **SOLAS XI-1/6** is
the mandatory hook. MIW carries that distinction and it is worth marks on limb (a).

**How future questions benefit.** The Understand standard is now mandatory for Batch 2 onward, with a
worked example and a pass/fail test, so this is fixed at the point of authoring rather than by audit.

---

## 14. Batch 2

**UNCHANGED — NOT STARTED.** QP2501, QP2502, QP2503, QP2504, QP2507, QP2406. No question was
authored in this session.

*Observed during preflight, for the Founder's awareness only:* a branch
`origin/pastpapers/qp2501-founder-review` appeared on the remote during this session's fetch. It was
not created here and was not touched. If desktop has begun QP2501, it should adopt the §10.1 standard
before its Understand sections are written.

---

## 15. Next action

After Founder review of this report, resume desktop Batch 2 with **QP2501** using the refined
Understand-mode standard in `DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §10.1.
