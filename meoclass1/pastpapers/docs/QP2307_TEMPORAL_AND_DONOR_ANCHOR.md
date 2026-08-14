# QP2307 — JULY 2023 — TEMPORAL AND DONOR ANCHOR

**Paper:** QP2307 · July 2023 · printed serial `2307 EM`
**Branch:** `pastpapers/qp2307-founder-review`
**Baseline:** `a633e97e3291d7de0f8e934d07b524f24a3b549c` (`origin/main` at session start; merge-base proven)
**Corpus commit consumed:** `319524c` (`RulesApp-Local-Input` `origin/main`)
**Authored:** 2026-08-14, desktop (`Dani-Desktop`)

Authority for method is `DESKTOP_QP_PRODUCTION_PLAYBOOK.md`; year-level authority is
`DESKTOP_QP_ALLOCATION_2023.md` §3. This file records only what is specific to July 2023.

---

## 1. SOURCE IDENTITY — established from the printed copy

| Field | Printed |
|---|---|
| Month / year | `JULY 2023` |
| Serial | **`2307 EM`** — number first, no `Sr. No.` prefix, no dash (the reversed 2023 convention) |
| Authority | `EXAMINATION OF MARINE ENGINEER OFFICER` |
| Function | Marine Engineering Management at Management Level |
| Subject | `ENGINEERING MANAGEMENT` |
| Class | `M.E.O CLASS – I` |
| Time | `TIME ALLOWED - 3 HOURS` |
| Total | `Total Marks – 100` |
| Region | `(India 2023)` |
| Pages | **2** |
| Questions | **9**, counted by reading both pages, not by pattern match |

**Serial check passes.** `2307` is consistent with July 2023 and with the eleven-paper 2023 intake
in which `2305` is absent. This is not a reprint of another sitting: no question on this paper
reproduces a whole other paper, and the four same-year relations found (Q3, Q4, Q6, Q8) are
single-question recurrences.

### 1.1 The under-read is explained, and it is a numbering variant

The 2023 intake named this paper as one an automated extractor under-reads. **The cause was located
and it is `Q3):`.** Every other question prints `Q<n>.`; Q3 alone prints a closing parenthesis and a
colon. A pattern anchored on `Q\d+\.` therefore finds eight questions, not nine, and the one it
drops is the NOx question.

**All nine were established by reading both printed pages before any count was consulted.** The
nine `text_verbatim` strings were then proved substring-exact against the extracted printed layer
after whitespace normalisation and host-furniture removal — a mechanical proof, recorded here
because "I read it" is not evidence a later session can re-run.

### 1.2 Printed anomalies — preserved, not normalised

Fifteen are recorded in `printed_anomalies`. The load-bearing ones:

| Where | Printed | Class |
|---|---|---|
| **Q3** | **`Q3):`** | **numbering — this is the extractor trap** |
| Q1 stem | `the salvor has a right to award` — missing article | grammar |
| Q1 c) | `discuss when is the Convention applicable` — interrogative order in a statement | grammar |
| Q3 b) | `vis-a-vis` — unaccented | spelling |
| Q3 d) | `Scavenge Air Moisturizing` — the industry term is *moistening* (SAM) | spelling |
| Q3 d) | `for ME` where March and October 2023 print `for main engine` | abbreviation |
| **Q4 b)** | **`Complaint Procedures`** — see §4 | **this sitting is the correct one** |
| Q4 stem | `discuss a)` — no colon, where February 2023 prints `discuss:` | punctuation |
| Q5 stem | `explain following.` — missing article, terminal full stop | grammar |
| Q7 (a) | `(a) Hull Roughness Management` — no terminal full stop | punctuation |
| **Q9** | **`“Unseaworthy ships"`** — U+201C closed by a straight U+0022 | punctuation |
| Q9 | `& "Unsafe ships"` where every later recurrence prints `and` | punctuation |
| Q9 | `with respect seaworthiness` — missing preposition | grammar |
| **Q6, Q7, Q8, Q9** | **no mark figure at all** | **marks** |

**Four of nine questions print no marks.** That is the highest count in the 2023 intake. Each is
recorded at 16 on the printed equal-marks rubric with `printed_marks_absent`, and **no limb split is
inferred**. This bites hardest at Q7, whose March 2025 recurrence prints `(6) (5) (5)`: those
figures are deliberately **not** imported, because importing them would manufacture a printed fact.

---

## 2. TEMPORAL POSITION — JULY 2023

Year-level boundaries are in `DESKTOP_QP_ALLOCATION_2023.md` §3 and are not restated. What this
sitting adds:

| Item | Position at July 2023 |
|---|---|
| Merchant Shipping Act, **1958** | **governs.** The 2025 Act commenced 15 March 2026 — future by ~32 months |
| 32nd IMO Assembly (Dec 2021) | **operative.** `A.1155(32)` PSC procedures |
| 33rd IMO Assembly | adopted **6 Dec 2023** — **future by ~5 months.** `A.118x(33)` prohibited |
| EEXI / CII | **operative** since 1 Jan 2023 |
| `MEPC.328(76)` (2021 revised Annex VI) | **in force 1 Nov 2022** — operative. TSCR-3 carried; the corpus register's date for it is erroneous and is ignored |
| MLC 2006 | **as amended through the 2018 set** |
| **MLC 2022 amendments** | **adopted, NOT in force** — EIF 23 Dec 2024, ~17 months future |
| Salvage Convention 1989 | in force 1996, **unamended** — no edition question |
| Hong Kong Convention | **not in force anywhere in 2023** (EIF 26 June 2025) |
| EU ETS, maritime scope | **future** — 1 Jan 2024 |
| Anti-Fouling Convention | cybutryne controls applied from 1 Jan 2023 |

---

## 3. THE JULY 2023 BOUNDARY — ASSESSED IN FULL, AND THE ANSWER IS MORE INTERESTING THAN "NO"

> **MEPC 80 sat 3–7 July 2023.** It adopted the **2023 IMO GHG Strategy on 7 July 2023**, and it
> **revised the IMO biofouling guidance** during the same session.
> The paper prints `JULY 2023` and **no day**. The sitting cannot be placed on either side.

This is why the allocation deferred QP2307 out of Batch 4. The finding has three parts.

**First: the recomputation was right that no question asks about the GHG Strategy.** No stem on this
paper concerns greenhouse gas ambition, decarbonisation targets or market-based measures.

**Second: the boundary is not therefore irrelevant.** It touches this paper at **two** points, and
neither is the Strategy itself. Both were found during authoring rather than at intake, and both are
neutralised **by structuring the answer so that correctness does not depend on the day** — the
allocation's own preferred remedy under trap 17 — rather than by hedging in prose.

| Question | Subject | Does the boundary bite? |
|---|---|---|
| Q1 | Salvage Convention, Article 13, LOF 2000 | No — unamended treaty and a commercial contract |
| Q2 | Passenger-ship joining inspection | No — SOLAS II-1, II-2, III and the ISM Code |
| **Q3** | **NOx: Tier II/III, primary/secondary, SCR, SAM, EGR** | **The CURRENCY STATEMENT only — see §3.1** |
| Q4 | MLC 2006 | No — an ILO instrument |
| Q5 | Collision at maritime law | No — private law on a 1910 treaty |
| Q6 | Formal Safety Assessment | No — a rule-making method, not a rule |
| **Q7** | **Hull and propeller maintenance for energy efficiency** | **YES, via the BIOFOULING GUIDANCE EDITION — see §3.2** |
| Q8 | Collision under the MS Act | No — Indian statute and a safety code |
| Q9 | Unseaworthy and unsafe ships | No — Indian statute |

### 3.1 Q3 — the boundary reaches the currency statement, not the substance

Regulation 13 is the **NOx** regime and the GHG Strategy governs neither tier limits nor SCR, so the
*substance* of Q3 is untouched. But **any claim about "the most recent MEPC session" would be
day-dependent**: MEPC 79 sat in December 2022 and MEPC 80 from 3 to 7 July 2023.

**The answer makes no such claim.** It states the operative instrument — the revised Annex VI
introduced by `MEPC.328(76)`, in force **1 November 2022** — which is true on both sides of 7 July,
and relies on the separately established fact that **MEPC 80 amended nothing in regulation 13**.

### 3.2 Q7 — the boundary genuinely bites, on the edition of the biofouling guidance

Q7 opens *"with the recent high stress on the energy efficiency of ships"*, which invites a
GHG-policy paragraph. That invitation is declined: **the IMO GHG Strategy is not named in the answer
at all, in either edition**, and the answer is anchored instead on the **SEEMP** and the
**operational carbon intensity** regime — both in force from 1 January 2023 and both unaffected by
7 July.

**The harder point, and the one that was not visible at intake:** the answer must mention the
biofouling management plan and record book, and **MEPC 80 revised the biofouling guidance inside the
sitting window**. Which edition was current on the examination day cannot be determined.

**The answer therefore names no edition, no year and no resolution number for that guidance.** Every
statement made about it — the management plan, the record book, the attention to niche areas, and
its status as *guidance and not law* — is true of it on either side of 7 July. Notably the March 2025
donor had adopted exactly this discipline for a different reason (against staleness); here it does
the work of day-independence.

### 3.3 What was NOT done

**No 7 July problem was manufactured.** No question was re-read looking for a way to make the
boundary relevant; no answer carries a "before or after 7 July" hedge; the boundary appears on no
candidate-facing surface; and where it does not bite, that is recorded as assessed and clear rather
than passed over in silence.

---

## 4. THE `Compliant` / `Complaint` PAIR — VERIFIED AGAINST SOURCE

The Founder flagged a relation between `QP2307-Q4` and `QP2302-Q8`. **Both printed stems were read
and the flag is confirmed, with the direction as stated.**

| | February 2023 (`QP2302-Q8`) | **July 2023 (`QP2307-Q4`)** |
|---|---|---|
| Limb b) | `On-board & On-shore **Compliant** Procedures.` | `On-board & On-shore **Complaint** Procedures.` |
| Stem | `discuss:` | `discuss` — no colon |
| Marks | **none printed** | **`(4) (4) (4) (4)`** |

**February prints a misprint that inverts the meaning** — *compliant* procedures and *complaint*
procedures are different things, and only one of them exists in MLC Title 5. **July prints the
intended word.** Neither is normalised: each sitting carries what it printed, and neither anomaly is
propagated to the other. The July answer therefore addresses **complaint** procedures without
qualification, where the February answer had to adjudicate the misprint first.

This is the cleanest illustration in the batch of the house rule that printed error is preserved:
the same examiner question, five months apart, with one word different and the correct one printed
second.

---

## 5. Q1–Q9 DONOR MAP

Derived at this baseline against **279 built questions across 31 papers** on `origin/main`, plus the
**36 questions on the four pushed 2023 review branches** (`QP2302`, `QP2303`, `QP2309`, `QP2310`) —
315 in total. Not read from any frozen field. Every donor named below was adjudicated by **reading
both printed stems in full**.

| Q | Subject | Tier | Preferred donor | Sitting | Distance | Class |
|---|---|---|---|---|---|---|
| **Q1** | Salvage, Article 13, LOF 2000 | **D** | `QP2408-Q7` | Aug 2024 | **+13 mo** | **NEAR — marks and word order differ** |
| **Q2** | Passenger-ship joining inspection | **—** | *none* | — | — | **FRESH** |
| **Q3** | NOx: Tier II/III, primary/secondary, SCR, SAM, EGR | **C** | `QP2303-Q4` + `QP2407-Q9` | Mar 2023 / Jul 2024 | −4 mo / +12 mo | **LIMB — a composite superset** |
| **Q4** | MLC: responsibilities, complaints, detention, redressal | **D** | `QP2302-Q8` | Feb 2023 | **−5 mo** | **NEAR — the misprint is the delta** |
| **Q5** | Collision: apportionment, fault, liabilities, presumptions | **—** | *none* | — | — | **FRESH** |
| **Q6** | Formal Safety Assessment | **D** | `QP2312-Q9` | Dec 2023 | **+5 mo** | **EXACT — character-identical** |
| **Q7** | Hull and propeller maintenance | **D** | `QP2503-Q8` | Mar 2025 | +20 mo | **EXACT stem, marks absent here** |
| **Q8** | Collision under the MS Act | **D** | `QP2304-Q4` | **Apr 2023** | **−3 mo** | **EXACT — 320 chars, character-identical** |
| **Q9** | Unseaworthy and unsafe ships | **D** | `QP2506-Q9` | Jun 2025 | +23 mo | **NEAR — punctuation and citation form** |

### 5.1 Q3 is a superset, and that is the interesting finding

QP2307-Q3 prints **four** limbs. They are the **union of two different donor questions**:

```
a) Tier 2 and 3 emission regulation on main engine     <- QP2407-Q9 limb A  (July 2024)
b) Primary NOx reduction vis-a-vis secondary           <- QP2303-Q4 limb A  (March 2023)
c) SCR for NOx Emission Reduction                      <- QP2407-Q9 limb C  (July 2024)
d) Scavenge Air Moisturizing & EGR for ME              <- QP2303-Q4 limb B  (March 2023)
```

The opening sentence — *"Exhaust emission control is a major global issue and under serious
consideration by world shipping. In this context, comment on the following: -"* — is
**character-identical to QP2303-Q4 and QP2310-Q5**. So the examiner took the March 2023 two-limb
question, kept its stem and both its limbs, and interleaved two limbs that later appear in July
2024. **No single donor covers this question**; the tier is C because the composite requires
adjudication, not mechanical reuse, and the four limbs are re-marked at 4 each where the donors
carry 8+8 and 4+4+4+4 respectively.

### 5.2 Q8 is the first FORWARD-in-time donor in the whole 2023 batch

`QP2304-Q4` sat in **April 2023, three months BEFORE this sitting**. Every other 2023 question so
far has had to reach forward to a later paper and strip later law. This one reaches **backwards**,
which is the normal MIW case and the safe direction: an earlier donor **cannot** import later law.
The two printed stems are **320 characters, character-identical** — proved by comparison, not by
similarity score.

The consequence for authoring is specific: QP2304-Q4's temporal reasoning is **directly reusable**
because both sittings are under the same statute, the same Assembly and the same casualty code, with
nothing entering force between April and July 2023 that touches the answer. What is **not** reused
is any sitting-relative prose; it is re-anchored to July, as the standing batch rule requires.

### 5.3 Donors on pushed branches, not on `main`

`QP2302-Q8` (Q4's donor) and `QP2303-Q4` (Q3's donor) are authored and pushed but **not yet
integrated on `main`**. They are consumed here on the precedent set by `QP2310-Q5`, which claimed
`QP2303-Q4` the same way: **both printed stems read in full, the branch and commit recorded, and the
claim adjudicated by an author rather than taken from a queue.** If the laptop review returns either
donor for correction, Q3 and Q4 must be re-checked against the corrected version.

### 5.4 Host recurrence annotations — discovery only

The source copy prints its own recurrence table under every question, including `2023/APR/Q4` under
Q8 and `2023/JUL/Q<n>` under all nine. Those rows **independently pointed at the QP2304 pair**, and
that was **discovery only**: the pair was adjudicated by reading the two printed stems. Host rows are
carried in `host_recurrence_hint` as provenance and **must not reach any candidate-facing surface**.

---

## 6. TRUE SOURCE — WHAT WAS CONSUMED, AND WHAT IS MISSING

Corpus commit `319524c`, read-only. Consumed by identity; nothing quoted.

| Instrument | Held? | Used for |
|---|---|---|
| **MLC 2006** — base text, Compendium 4th rev., 2022 amendments | **YES** | **Q4** — the strongest corpus support on this paper |
| **MARPOL Annex VI** — base + NOx Technical Code 2008 (5th ed. 2023), `MEPC.328(76)` | **YES**, citation-ready | **Q3** — instrument identity and provenance only, never text |
| SOLAS 1974 | **PARTIAL** — `MSC.532(107)` for II-1, reg 10 only for II-2 | **Q2** — base chapters II-1 and II-2 **not held** |
| ISM Code, LSA Code, FSS Code | held | Q2, background |
| **Salvage Convention 1989** | **NO** | **Q1** — the family log covers HNS, Nairobi, LLMC, CLC/FUND/Bunkers and **not** Salvage |
| **Merchant Shipping Act, 1958** | **NO** — the corpus holds the **2025** Act | **Q8, Q9** — the standing register inversion |
| Collision Convention 1910 | **NO** | **Q5** |
| FSA Guidelines (`MSC-MEPC.2/Circ.12`) | **NO** | **Q6** |

### 6.1 Limitations recorded, and referrals raised

Five questions rest on authoritative-secondary evidence where the primary is not held. Each is
recorded on the question as `C_ACCEPTED_LIMITATION` — a decision to publish with the limitation
stated, **not** a promotion to primary:

1. **Q1 — Salvage Convention 1989 not held.** Article identities and effects are given by
   authoritative secondary, carried through `QP2408-Q7` and `QP2411-Q5`. **No article is quoted.**
2. **Q5 — the Collision Convention 1910 not held.** Doctrine stated by identity and effect.
3. **Q6 — the FSA Guidelines not held.** The method is carried through `QP2312-Q9` and `QP2606-Q9`.
4. **Q8, Q9 — the MS Act 1958 not held.** The standing 2023 inversion: the corpus holds the 2025
   Act, which is future by ~32 months at this sitting. Identical to the position already recorded
   for `QP2304-Q4` and `QP2410-Q1`.
5. **Q2 — SOLAS chapters II-1 and II-2 held only as an amendment resolution and one regulation.**

**No corpus defect was found on this paper**, so no `TRUE_SOURCE_CORRECTION_REQUEST` is raised. The
five entries above are **coverage gaps, not defects** — the corpus does not claim to hold these and
is not wrong about them. They are recorded here so the Founder's minimum-True-Source audit, which
runs after all papers are solved, has the demand list without re-deriving it:

> **QP2307 True Source demand:** Salvage Convention 1989 · Merchant Shipping Act 1958 ·
> Collision Convention 1910 · `MSC-MEPC.2/Circ.12` FSA Guidelines · SOLAS chapters II-1 and II-2
> base text.

---

## 7. WHAT IS DELIBERATELY ABSENT FROM EVERY ANSWER

- The **2023 IMO GHG Strategy** and the **Initial Strategy 2018** — §3.1.
- **`A.118x(33)`** and every 33rd Assembly instrument — future by five months.
- The **Merchant Shipping Act, 2025** and **DGMA** — future by ~32 months. `DG Shipping` is correct
  here and carries `GREP: SKIP` under `known_traps.md` Entry 6.
- The **MLC 2022 amendments** as operative law — adopted, in force 23 Dec 2024. Q4 names them only
  as *adopted and not yet in force*, which is the distinction the playbook §8 exists to enforce.
- The **Hong Kong Convention**, **EU ETS**, **MEPC 81/82/83** and the **IMO Net-Zero Framework**.
- Any **week-granularity distance** from a month-only sitting.

---

## 7A. QA RESULT

Run at the end of authoring, with the global layer regenerated to validate and then **reverted**.

| Check | Result |
|---|---|
| `validate_spec` | **0 errors**, 13 warnings (nine word-count LONG, four `no P1` — both match the house norm) |
| `audit_paper` (globals present) | **0 errors, 0 warnings** — all 14 checks pass, including manifest consistency |
| Double deterministic build | **byte-identical**, `d2def0b94758b84b`; LF line endings on spec and HTML |
| `known_traps_check` | 233 checks, **0 failures**; trap 17 swept separately — **0 week/day distances** |
| `recurrence_check` | 288 questions, 161 families, **0 failures** |
| `health_check` (globals present) | **0 errors, 0 warnings** |
| `questions_year_check` | **OK**, 4 years, 0 warnings |
| `temporal_sweep` | 52 QP2307 candidates, **all adjudicated** — every one is a post-sitting date stated as an exclusion, a limitation or the declared corpus-register defect |
| Donor contamination | swept per question; two donors **partially rejected** (`QP2407-Q9` currency statement, `QP2508-Q5` 2025-Act reasoning) |
| Candidate-facing leakage | **1 real defect found and fixed** — the word *donor* had reached `Q8.quick_revision`; re-swept to 0 |
| Host identity in shipped bytes | **0** |
| Positive control on the leakage filter | seeded a known positive → filter fired; the nil is a **searched** nil |
| UI at 1280 and 375 | 9 cards · 5 modes · **Answer default on all nine** · search · 20 deep links all resolve · 16 cross-links all within-paper · **no horizontal overflow** · **no console errors** |

**Two failures are present and neither is caused by this paper.**

1. `solvedqp_check` — the storefront `SQ/index.html` hard-codes 31 papers / 279 questions and is
   stale at 32 / 288. It is **shared product inventory**, listed in playbook §13.2 as not owned by a
   paper branch. The laptop updates it at integration.
2. `coverage_check` — `NO_SITTING` disagrees with `KNOWN_ABSENT` for **2021-05, 2021-06 and
   2022-05**. **This was reproduced on the clean baseline with QP2307 stashed**, so it pre-dates this
   paper entirely and concerns years MIW does not hold. Reported, not fixed.

---

## 8. BRANCH AND ARTEFACT RULES

Unchanged from the batch. This branch commits only its paper-owned files: the spec, the review HTML,
this anchor and the nine verification records. No global derived artefact, no source PDF. Push and
stop; the laptop integrates.
