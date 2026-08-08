# QP2603 (March 2026) — dedup, source plan and the March temporal check

Written 2026-08-08, at the close of the QP2603 production session. Fourth paper of the six
available 2026 sittings.

---

## 1. Source transcription

| | |
|---|---|
| Source copy | `meoclass1/pastpapers/docs/03 - MARCH - 2026.pdf` — 2 pages, git-ignored |
| Printed serial | `EM – 2603` — preserved here and in the local provenance record; canonical `sr_no` is `QP-2603` |
| Method | PyMuPDF text extraction, then both pages rendered at 170 dpi and read visually against the extraction |
| Result | **No wording corrections required.** Extraction matched the rendered pages on both pages. |

**Printed marks — March breaks both earlier 2026 patterns.** Only **three of nine**
questions print any allocation at all:

| Question | Printed marks |
|---|---|
| Q1 | `(16)` — whole question |
| Q8 | `a) (10)` and `b) (6)` — the only per-limb split on the paper |
| Q9 | `(16)` — whole question |
| Q2, Q3, Q4, Q5, Q6, Q7 | **none printed** |

Four of those six unmarked questions are nevertheless divided into lettered limbs (Q2, Q3,
Q5, Q6). **No split was invented for any of them.** Across the set: January printed
per-limb marks on 2 of 9, February on 6 of 9, March on 1 of 9. There is no series
convention.

**The 96-vs-100 discrepancy is present again — now 4/4.** "Answer SIX questions only", "All
questions carry equal marks", printed "Total Marks – 100". 6 × 16 = 96. Recorded as-is.

**Printed limb labels are internally inconsistent again**, and are preserved: Q2 `i)/ii)`,
Q3 and Q8 `a)/b)`, Q5 `a. b. c. d.`, Q6 `a)/b)/c)`. Q1, Q4, Q7 and Q9 are undivided.

**Printed grammatical oddities, transcribed as printed:** Q1's question mark inside a
"Discuss" instruction and its misplaced comma in "For a convention of important technical
nature state,"; Q2's "it's content"; Q5's opening sentence fragment; Q6's three different
capitalisations of "Enhanced Survey Program" across its three limbs.

---

## 2. THE MARCH TEMPORAL CHECK — the headline issue of this sitting

**The Merchant Shipping Act, 2025 commenced on 15 March 2026** — mid-month, inside this
sitting. The brief correctly flagged that a March paper cannot be assumed to sit wholly
before or wholly after commencement.

### The sitting date cannot be established

- **No examination date is printed on the paper.** Only "MARCH 2026" and "(India 2026)".
- **The source copy's PDF metadata does not help.** It records a creation date of
  **20 April 2026** — and the same date, within minutes, for *all six* 2026 files. That is
  when the third-party host batch-generated the copies, which is after every sitting.
- No other date-bearing artefact exists in the source.

**Conclusion: the exact March sitting date is NOT establishable from the source.** This is
recorded honestly rather than guessed.

### Why that does not block the paper

The brief's rule is that an unestablished sitting date becomes `A_BLOCKING` **only if a
statutory answer turns on 15 March**. Every question was therefore checked individually:

| Q | Subject | Turns on 15 March 2026? | Basis |
|---|---|---|---|
| Q1 | Entry into force of an IMO convention | **No** | Answer's only Indian reference is to "the Merchant Shipping Act and rules made under it", deliberately **unnumbered**, and recorded as context not as a scoring claim. Correct either side of commencement. |
| Q2 | Container cargo securing | **No** | Wholly international — SOLAS VI/VII, CSS Code, IMO circulars. |
| Q3 | War risk cover | **No** | Marine Insurance Act **1963**, which s.324(1) does not repeal. |
| Q4 | WHO, disease vectors, ship health certificates | **No** | Regulation list contains **no Merchant Shipping Act at all**. Rests on IHR 2005 and the **Indian Port Health Rules 1955**, made under the **Indian Ports Act 1908**. Full-text scan for "Merchant Shipping", "MSA" and "1958" returns **zero** hits. |
| Q5 | LNG bunkering | **No** | Wholly international and operational — IGF Code, ISO 20519. |
| Q6 | ESP vs CAP | **No** | International survey regime — SOLAS XI-1/2, ESP Code, class rules. |
| Q7 | Propeller crack in dry dock | **No** — *and drafted to stay clear* | The flag-State reporting limb is expressed as a **conditional test** tied to cause and seaworthiness, deliberately **not** tied to a named national instrument. |
| Q8 | FSA and lithium batteries | **No** | Wholly international. The four "MSA" matches in the inherited February object are the substring inside **EMSA** (European Maritime Safety Agency). |
| Q9 | Hong Kong Convention and India | **No** — *and this is the one that could have* | India's recycling law is the **Recycling of Ships Act, 2019**, separate legislation. **s.324(1) of the MS Act 2025 repeals the MS Act 1958 and the Coasting Vessels Act 1838 only** — a closed list that does not reach the 2019 Act. The 2025 Act touches recycling at **s.17** alone. |

**Result: 0 of 9 questions turn on the 15 March 2026 commencement. No `A_BLOCKING` flag
arises from the sitting-date ambiguity.**

The QP2607 Q7 Gazette reading paid for itself a **third** time. Without a verified reading
of s.324(1)'s closed repeal list, Q9 could not have been answered safely at all.

---

## 3. Cross-paper recurrence — established by reading, not by the recurrence table

The source copy prints a table of prior-sitting codes beneath each question. Those are
**host-added annotation**, not examination data, and support **discovery only**. Every
classification below was decided by comparing transcribed wordings directly. A full
similarity sweep was run of all nine March stems against all 27 already-built stems.

| Q | Class | Against | Evidence |
|---|---|---|---|
| **Q1** | **EXACT** | **QP2602 Q7** | String equality, 398 characters |
| **Q4** | **EXACT** | **QP2601 Q6** | String equality, 453 characters |
| **Q8** | **EXACT** | **QP2602 Q3** | String equality, 245 characters |
| Q2 | **NONE** | — | Empty recurrence table; sweep found no match above 0.5 |
| Q3 | TOPIC | QP2607 Q9, QP2601 Q4 | Same category and statute, no shared command or subject |
| Q5 | TOPIC | QP2607 Q6 | Same category and fuel framework, different task entirely |
| Q6 | TOPIC | QP2601 Q5 | Structural condition from the survey side rather than the corrosion side |
| Q7 | TOPIC | QP2607 Q2 | Shared "you as CE, state the steps" shape only — a structural, not topical, relationship |
| Q9 | TOPIC | QP2607 Q7 | Same Indian statutory territory; different Act and objective |

**EXACT 3 · NEAR 0 · TOPIC 5 · NONE 1.**

Q8 additionally carries an inherited **NEAR** against QP2607 Q1(a). A question can hold two
different recurrence relationships against two different papers at once.

### The similarity sweep

Every March stem was compared against all 27 prior stems by sequence-matching ratio. Exactly
three pairs scored above 0.5, and all three scored **1.0000**. There is no middle ground in
this paper: a March question is either word-for-word identical to a prior one or clearly
unrelated in wording. That is itself a finding — February's two NEAR recurrences had no
counterpart here.

---

## 4. THE REUSE FINDING — an exact question is not an exact answer object

**This is the most important architectural outcome of the March session.**

February established the reuse rule: an identical question keeps its verified answer and its
canonical route, because one question has exactly one route. March applied that rule three
times and found what February's single instance did not expose.

> **A verified answer contains sitting-relative prose, and that prose is false at the new
> sitting even when every underlying fact is unchanged.**

**Ten** such statements were found across the three reused questions:

| From | Statement | Why it fails in March |
|---|---|---|
| QP2602 Q7 | *"The Net-Zero Framework in **Q8 of this paper**…"* | February's Q8 **is** the Net-Zero question. March's Q8 is the lithium-battery FSA question. The sentence would have been simply false. |
| QP2602 Q3 (×7) | *"in force 1 January 2026 — **five weeks** before this examination"*, and variants | Correct arithmetic for February; wrong for March. Also *"back onto **February** 2026"*. |
| QP2601 Q6 (×2) | *"**four months** before this sitting"*; *"the **January 2026** position"* | 19 September 2025 is four months before January, six before March. |

Every one was re-anchored by an **asserted patch** in the assembly step: the build fails
loudly if a patch does not fire, and fails again if the old string survives. Silent reuse
was not acceptable, because each of these would have shipped as a confident false statement
inside an otherwise verified answer.

**The tenth was found only by sweeping the ASSEMBLED spec**, not the source. The patch list
built by reading the three source objects had missed a re-verification note reading *"These
dates were five weeks old at the sitting"* — a different string from the six already caught
in the same question. That is the argument for making the post-assembly sweep mandatory
rather than trusting the patch list.

**Recommendation for QP2604 and QP2606:** treat "scan the reused object for sitting-relative
prose" as a **mandatory step** of Tier D reuse, not as a judgement call. The classes of
phrase to search for are: `this paper`, `this sitting`, `this examination`, `weeks/months
before`, a named month-year, and any cross-reference to another question **by number** on
the same paper.

This does **not** reopen the reuse rule. The verified answer and the canonical route were
reused, exactly as February decided. What changed is confined to re-anchoring, and no
scoring proposition was altered on any of the three.

### Standing consequence

Q1, Q4 and Q8 are deliberately identical in substance to QP2602 Q7, QP2601 Q6 and QP2602 Q3
respectively. **Any correction made to either member of a pair on Founder review must be
applied to the other.** Recorded in each spec's `unresolved` list and in each verification
record. Note that QP2601 Q9 / QP2602 Q4 remain a pair from February, so **four** linked
pairs now exist across the set.

---

## 5. Reuse tier by question

| Q | Tier | Reasoning |
|---|---|---|
| Q1 | **D** | Exact prior past-paper recurrence — QP2602 Q7 |
| Q2 | C | Fresh. No material MIW overlap. |
| Q3 | B | MIA 1963 identification reused from QP2607 Q9; substance fresh |
| Q4 | **D** | Exact prior past-paper recurrence — QP2601 Q6 |
| Q5 | B | IGF Code framing reused from QP2607 Q6; four processes fresh |
| Q6 | B | Coating Technical File from QP2601 Q5; RO relationship from QP2607 Q3 |
| Q7 | B | Incident-response discipline from QP2607 Q2; class relationship from QP2607 Q3 |
| Q8 | **D** | Exact prior past-paper recurrence — QP2602 Q3 |
| Q9 | B | The s.324(1) Gazette reading from QP2607 Q7 is load-bearing here |

**No Tier A.** Nothing in the existing MIW corpus already answered a March question in full.
Tier is a production classification, not a quality score.

---

## 6. Source hierarchy actually achieved

| Question | Strongest source reached |
|---|---|
| Q1 | P1 — IMO treaty-process material (inherited, verified) |
| Q2 | P1 — MSC.1/Circ.1353/Rev.2, MSC.1/Circ.1352/Rev.1, MSC.1/Circ.1627 |
| Q3 | **P1 — Marine Insurance Act 1963 s.2(e), read at source** |
| Q4 | P1 — consolidated IHR text read in full (inherited, verified) |
| Q5 | P1 — ISO 20519 requirements (extracts) |
| Q6 | P1 — IMO resolution record for A.1049(27) |
| Q7 | **P2/P3 only** — procedural; no primary instrument governs the sequence |
| Q8 | P1 — MSC-MEPC.2/Circ.12/Rev.2 (inherited, verified) |
| Q9 | **P1 — IMO press briefings for entry into force and India's accession** |

**Licence-gated instruments blocked a P1 claim again — 4/4 papers.** March's blocked
instruments: SOLAS, the CSS Code, the IGF Code, ISO 20519, the 2011 ESP Code, ISO 484 and
the Hong Kong Convention text. This is the largest licence-gap of any paper so far and is
recorded in the true-source demand map.

---

## 7. What was deliberately NOT asserted

Recorded because a future session may otherwise "fix" these by adding a number.

- **Joint War Committee Listed Areas and war risk premium rates** (Q3) — change continuously.
- **India's share of world ship recycling** (Q9) — published figures differ widely; none verified.
- **Gross tonnage thresholds for ESP application** (Q6) — inconsistent across secondary sources.
- **Gassing-up completion percentages and cooldown rates** (Q5) — ship and containment-system specific.
- **Propeller blade repair zone boundaries** (Q7) — differ between classification societies.
- **ISO 20519 clause numbers** (Q5) — more than one edition exists and none is held.
- **Whether Q7's damage is a reportable casualty or an insured loss** — the question gives no cause.

---

## 8. Result

**Nine questions built. 0 class A blocking flags.** The paper is a Founder review candidate.
