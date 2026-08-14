# QP2306 — JUNE 2023 — TEMPORAL AND DONOR ANCHOR

**Paper:** QP2306 · June 2023 · printed serial `2306 EM` · `(India 2023)`
**Branch:** `pastpapers/qp2306-founder-review`
**Baseline:** `e41772e2534138d0ecf8319c6fa3ac93e2ad754f` (`origin/main` at session start)
**Corpus consumed:** `RulesApp-Local-Input` working state at `D:\RulesApp-Local-Input`, READ ONLY
**Authority for method:** `DESKTOP_QP_PRODUCTION_PLAYBOOK.md`, `DESKTOP_QP_ALLOCATION_2023.md` §3

---

## 1. SOURCE RECONCILIATION

Read directly from `meoclass1/pastpapers/docs/JUNE 2023.pdf` (git-ignored, local only), both pages,
text layer extracted and read back. **The printed paper is the authority. No automated 2023
extraction count was trusted; all nine questions were identified by reading.**

| Checked | Found |
|---|---|
| Printed serial | **`2306 EM`** — number first, no `Sr. No.` prefix, no dash. The 2023 convention (allocation §1.1), **not** the 2024 `Sr. No. EM – 2406` shape |
| Month / year printed | `JUNE 2023` — **month only, no day** |
| Region note | `(India 2023)` |
| Function | `Marine Engineering Management at Management Level` |
| Subject | `ENGINEERING MANAGEMENT` |
| Class | `M.E.O CLASS – I` (printed with an en-dash, and **without** the full stops the 2024 papers print as `M.E.O.`) |
| Time / marks | `TIME ALLOWED - 3 HOURS`; `Total Marks – 100` |
| Pages | **2** |
| Questions | **9**, `Q1`–`Q9`, each printed with the `Q` prefix — this paper does **not** carry the bare-number numbering variants that January and February 2023 do |
| Serial gap | `2304 → 2306`, nothing at `2305`. Consistent with **May 2023 = `NO SITTING`** on serial-gap evidence, as recorded for May 2024 and May 2025 |

### 1.1 Printed marks — recorded exactly as printed

Marks are printed on **four questions only**:

| Question | Printed marks |
|---|---|
| Q3 | `(8)` on limb a), `(8)` on limb b) |
| Q4 | `(16)` |
| Q7 | `(16)` |
| Q8 | `(8)` on limb a), `(8)` on limb b) |
| Q1, Q2, Q5, Q6, Q9 | **no printed marks at all** |

Instruction 2 prints *"All questions carry equal marks"* against `Total Marks – 100` with
*"Answer SIX questions only"*. Every question is therefore recorded at **16 marks**, which is the
figure the paper itself prints on Q4 and Q7 — so six answered questions total **96 against the
printed 100**. **The discrepancy is printed on the source and is not corrected.** `printed_marks_absent`
is `true` on Q1, Q2, Q5, Q6 and Q9.

### 1.2 Printed anomalies — preserved, never normalised

| Where | What is printed | Disposition |
|---|---|---|
| **Q5 limb (iii)** | **`(Ill)`** — capital I followed by two lower-case L's, in place of the roman numeral `(iii)` | **Preserved verbatim.** The same corruption appears in the January 2023 printing of the identical limb (`QP2301-Q2`); the September 2024 printing (`QP2409-Q8`) prints `(iii)` correctly. This is a printing defect that recurs across 2023, not a transcription error |
| **Q1** | Limbs lettered `A.` and `B.` — both upper case | Preserved |
| **Q2** | Limbs lettered **`a)` then `B.`** — case and style change inside one question | Preserved; noted as a numbering anomaly |
| **Q6** | Limbs lettered `A.` `B.` `C.` `D.` `E.` — five limbs, no marks split | Preserved |
| **Q4** | *"Underline the **Importance** of..."* — capitalised mid-sentence | Preserved |
| **Q5** | *"(Ill) Hybrid TBT free paint"* — no hyphen in "TBT free" | Preserved |
| **Q8** | *"What **defense** is available"* — US spelling | Preserved. The December 2024 printing of the identical stem prints *"defence"* |
| **Q9** | *"Micro bubbles"* — printed as two words | Preserved |
| Header | `M.E.O CLASS – I`, `Total Marks – 100` — en-dashes; `M.E.O` without a trailing stop | Preserved |

### 1.3 Host and editorial furniture — excluded from every committed artefact

The source copy is a **third-party scan** carrying the host's own branding, an app advertisement, a
purchase solicitation, page numbers and a repeated footer. **None of it is transcribed.** The host
also prints its own recurrence annotations beneath each question (`2023/JUNE/Q1`, `2013/SR02`,
`2022/OCT/Q7`, and so on). These are recorded in `host_recurrence_hint` as **discovery-only
provenance**; they create no family edge, they are not MIW truth, and they reach no candidate-facing
surface. Note that the host's own annotation is internally inconsistent — `2023/JUNE/` on Q1–Q5 and
Q7–Q8 but `2023/JUN/` on Q6 and Q9 — which is one more reason it is not treated as data.

Host identity is recorded only in the git-ignored `verification/LOCAL_SOURCE_PROVENANCE.md`. **This
repository is public.**

---

## 2. JUNE 2023 TEMPORAL STATE

June 2023 is the **last sitting of the year that stands wholly before the MEPC 80 boundary**. That
single fact governs more of this paper than any other.

### 2.1 Operative at this sitting

| Instrument | Position in June 2023 |
|---|---|
| **Merchant Shipping Act, 1958** | **Governs.** The Merchant Shipping Act 2025 commenced 15 March 2026 — **thirty-three months future** |
| **Initial IMO GHG Strategy 2018** (`MEPC.304(72)`) | **OPERATIVE.** See §2.2 |
| **`MEPC.328(76)`** — 2021 revised MARPOL Annex VI | **IN FORCE since 1 November 2022.** See §4 — this is where True Source is wrong |
| **EEXI and CII** | **In force 1 January 2023.** Five to six months old at this sitting. 2023 is the **first CII data year and it is still running**; **no CII rating has yet been issued to any ship** |
| **`MEPC.346(78)`** — 2022 SEEMP Guidelines, adopted 10 June 2022 | **OPERATIVE.** Revoked `MEPC.282(70)`, the 2016 Guidelines |
| **`MEPC.352(78)`** G1 CII guidelines, **`MEPC.355(78)`** G5 correction factors | Operative — the 2022 set |
| **AFS Convention 2001 as amended** | In force; the **cybutryne** controls introduced by `MEPC.331(76)` applied from **1 January 2023** — five months old |
| **ISM Code** as amended through **`MSC.353(92)`** | Operative |
| **Casualty Investigation Code, `MSC.255(84)`** (16 May 2008) | Operative; mandatory through **SOLAS XI-1/6** from 1 January 2010 |
| **III Code, `A.1070(28)`** (4 December 2013) | Operative; **mandatory from 1 January 2016**; the audit standard for IMSAS |
| **32nd Assembly instruments** | Operative — **`A.1155(32)`** PSC Procedures 2021, **`A.1157(32)`** non-exhaustive list of obligations |
| **CLC 1992 · Fund 1992 · Supplementary Fund Protocol 2003** | All in force. India is a Party to CLC 92 and Fund 92 |
| **Hague-Visby Rules** | Operative in India through the **Indian Carriage of Goods by Sea Act, 1925 as amended in 1993**. **Hamburg Rules 1978** in force internationally since 1992 |
| **Marine Insurance Act, 1963** (India) | Operative |
| **MLC 2006** as amended through the **2018** amendments | Operative |

### 2.2 THE MEPC 80 BOUNDARY — the governing temporal fact for this paper

> **MEPC 80 sat 3–7 July 2023 and adopted the 2023 IMO GHG Strategy, resolution `MEPC.377(80)`, on
> 7 July 2023.**
>
> **June 2023 stands entirely before it.** The operative strategy at this sitting is the
> **Initial IMO GHG Strategy of 2018**, with its 2050 target of at least a **50% reduction in total
> annual GHG emissions** against 2008 and a **40% carbon-intensity reduction by 2030**.

This is not a marginal call. Unlike July 2023 — which prints a month with no day and therefore
straddles the boundary irresolvably — **June 2023 is unambiguous**: the whole month precedes
3 July. No day-level reasoning is needed and none is used.

**Consequence for donors.** Every donor available to Q7 and Q9 is a 2024, 2025 or 2026 object and
every one of them carries `MEPC.377(80)` as the operative strategy. **That statement is future here
and is not inherited.** The reversal is recorded per question.

### 2.3 Future at this sitting — PROHIBITED

| Item | Date | Distance from sitting |
|---|---|---|
| **2023 IMO GHG Strategy `MEPC.377(80)`** | 7 July 2023 | **~1 month future** |
| **MEPC 80** itself | 3–7 July 2023 | ~1 month future |
| SOLAS Consolidated Edition 2024 | 1 July 2024 | 12 months |
| **MLC 2022 amendments** | in force 23 December 2024 | 18 months — **adopted, not in force** |
| **EU ETS maritime application** | 1 January 2024 | 6 months |
| FuelEU Maritime | 1 January 2025 | 18 months |
| **Hong Kong Convention** | in force 26 June 2025 | 24 months — **not in force anywhere in 2023** |
| **33rd Assembly `A.118x(33)`** | adopted 6 December 2023 | **6 months** — `A.1185(33)`, `A.1187(33)`, `A.1184(33)` all future |
| **`MEPC.388(81)`**, **`MEPC.395(82)`** SEEMP guidelines | 2024 | 10 and 16 months |
| MEPC 81 / 82 / 83 | 2024–2025 | — |
| IMO Net-Zero Framework / GFI | October 2025 | — |
| 34th Assembly `A.12xx(34)` | 3 December 2025 | — |
| **Merchant Shipping Act, 2025** | commenced 15 March 2026 | **33 months** |

### 2.4 One day-dependent fact inside the sitting month — NOT CONSUMED

The **Hong Kong Convention reached its entry-into-force conditions on 26 June 2023**, when Bangladesh
and Liberia acceded, fixing entry into force for 26 June 2025. **That event falls inside the printed
sitting month and the paper prints no day.** In line with the standing rule against week-granularity
reasoning from a month-only sitting, **no claim in this paper depends on which side of 26 June the
examination fell**. The Convention is not in force at this sitting on any reading, and no question
requires more than that.

---

## 3. Q1–Q9 DONOR MAP

Derived by stem-similarity and targeted phrase search across **333 questions in 37 papers** — the
32 built specs on the baseline plus the five pushed, governed 2023 review branches (`qp2302`,
`qp2303`, `qp2307`, `qp2308`, `qp2310`). Every candidate below was chosen after **reading both
printed stems**, never from a similarity score alone.

**The Batch 4 allocation ranked QP2306 at 3/9 with a donor. That figure is stale and was
recomputed, not inherited:** six 2023 papers have been solved since, and two of this paper's three
strongest donors (`QP2303-Q1`, `QP2301-Q2`) are same-year 2023 objects that did not exist when that
table was written.

| Q | Class | Donor | Sitting | Direction | Note |
|---|---|---|---|---|---|
| **Q1** | **EXACT** | `QP2303-Q1` | March 2023 | **−3 months (earlier)** | Stems **verbatim identical**, including both limb letters. Same year, same temporal regime |
| **Q2** | **LIMB** | `QP2301-Q7` (casualty limb) · `QP2308-Q9` (III Code / audit limb) | Jan 2023 · Aug 2023 | −5 / **+2 months** | Composite. **No donor for the origin-of-IMO and ratification limb** — `QP2506-Q2` family only |
| **Q3** | **LIMB** | `QP2407-Q8(b)` (3/4ths collision clause = the Running Down Clause) · `QP2304-Q3` (general average) | July 2024 · **April 2023** | +13 / **−2 months** | The unrepaired-damage limb is **FRESH** — no corpus question addresses it |
| **Q4** | **FAMILY** | `QP2302-Q5` (effective communication under the ISM Code) | February 2023 | **−4 months** | Emergency-preparedness communication measures are **FRESH** |
| **Q5** | **EXACT (limb donor)** | `QP2301-Q2` limb c) | January 2023 | **−5 months** | The QP2306 question **is** that limb standing alone, **verbatim, including the `(Ill)` misprint** |
| **Q6** | **FRESH** | — | — | — | **No donor anywhere in 336 questions.** Host hint points to 2013/2014 papers MIW does not hold |
| **Q7** | **EXACT** | `QP2412-Q8` | December 2024 | **+18 months** | Verbatim identical. **Carries the paper's largest temporal reversal** — see §5 |
| **Q8** | **EXACT** | `QP2412-Q7` | December 2024 | **+18 months** | Verbatim but for *defense*/*defence* |
| **Q9** | **FAMILY** | `QP2402-Q3` / `QP2310-Q1` (hull-form optimisation) · `QP2503-Q8` / `QP2307-Q7` (hull and propeller maintenance) | 2023–2025 | mixed | The three named technologies — air cavity, surface texturing, microbubbles — are **FRESH**. Host hint `2022/OCT/Q7` is a paper MIW does not hold |

**Totals: 4 EXACT · 2 LIMB · 2 FAMILY · 1 FRESH.**

### 3.1 Same-year donors — the batch has begun to feed itself

Five of this paper's donors are **2023 objects** (`QP2301` ×2, `QP2302`, `QP2303`, `QP2304`,
`QP2308`), of which **three are earlier than June 2023**. This is the first QP2306-class paper in
which the normal MIW situation — a donor that pre-dates its recipient and therefore *cannot* carry
later law backwards — actually occurs. It does not remove the obligation to re-derive: a donor is a
**route**, and every sitting-relative statement is re-derived from the June 2023 position and
recorded in that question's `temporal_review`.

### 3.2 Later-donor reversals applied

| Q | Donor asserts | June 2023 position | Action |
|---|---|---|---|
| **Q7** | `QP2412-Q8`: SEEMP guidelines are **`MEPC.395(82)`** (4 Oct 2024), revoking `MEPC.346(78)`; operative strategy is `MEPC.377(80)`; first CII ratings issued | Guidelines are **`MEPC.346(78)`**, the **2022** Guidelines — `MEPC.395(82)` and `MEPC.388(81)` do not exist. Strategy is the **Initial 2018 Strategy**. **No CII rating has been issued to any ship** | **Three reversals.** Regulation 26 numbering is the one element that transfers unchanged |
| **Q7** | `QP2412-Q8`: MEPC 82 review of the short-term measures in progress | **MEPC 80 has not yet met.** The `MEPC.328(76)` review required by regulations 25.3 and 28.11 to complete by 1 January 2026 is recorded from `MEPC.346(78)` operative paragraph 4 — the only forward-looking statement that *is* available here | Reversed to the 2022 statement |
| **Q8** | `QP2412-Q7`: cargo-convention framework | The Hague-Visby / Hamburg / Rotterdam positions are **unchanged** between the two sittings. Rotterdam Rules not in force at either | **No reversal needed** — recorded as checked, not assumed |
| **Q9** | 2024–2026 energy-efficiency family carries `MEPC.377(80)` and post-2023 CII experience | Initial 2018 Strategy; first CII year running | Reversed |
| **Q3** | `QP2407-Q8` (July 2024) | Institute Time Clauses and the Marine Insurance Act 1963 are unchanged | No reversal; York-Antwerp edition handled per §6 |

---

## 4. TRUE SOURCE — CONSUMPTION, LIMITATIONS AND REFERRALS

Corpus used **READ ONLY**. No corpus file was created, edited or deleted. No corpus construction
was begun.

### 4.1 TSCR-3 IS ENGAGED BY THIS PAPER, AND IT IS DECLINED

`TRUE_SOURCE_CORRECTION_REQUEST` **TSCR-3** is open against
`true-source/03-imo-instruments/MARPOL-Annex-VI/amendment-register.json`, whose `baseline` block
records:

```json
{"resolution": "MEPC.328(76)", "adopted": "2021-06-17", "entryIntoForce": "2023-11-01"}
```

**The entry-into-force date is wrong. The correct date is 1 November 2022.**

**This paper sits inside the window that error corrupts, and Q7 depends on it directly.** Consuming
`2023-11-01` would place a June 2023 sitting *before* the revised Annex VI entered into force. The
answer would then have to say the SEEMP is required by **regulation 22**, that chapter 4 had not been
renumbered, and that **EEXI and CII were not yet applicable** — three wrong statements, one of which
inverts the substance of the question. **The corpus figure is declined and 1 November 2022 is used.**

**It is refuted from inside the corpus, by primary source.** `MEPC.346(78)`, read directly this
session, states in its own preamble:

> the Committee, at its seventy-sixth session, adopted, by resolution MEPC.328(76), the 2021 revised
> MARPOL Annex VI, **which will enter into force on 1 November 2022**

No corpus file was touched. **TSCR-3 remains OPEN and is re-reported, not repaired.** TSCR-4
(`MEPC.376(80)` presented as current) is also MARPOL Annex VI but is **not engaged**: `MEPC.376(80)`
is a July 2023 instrument and is future at this sitting, so no question consumes it.

### 4.2 What the corpus supplied

| Question | Object read directly | Value |
|---|---|---|
| **Q7** | `GHG-instruments/_base-and-amendments/MEPC.346(78).pdf` — resolution and annex sections 1, 2, 3 and 4 in full | **Decisive.** The operative SEEMP Guidelines at this sitting, held complete |
| **Q1** | `05-un-and-treaty-law/UNCLOS/_base/UNCLOS_unclos_e.pdf` | **Decisive.** Article 1(1)(4) definition of pollution read verbatim; Part XII read for the coastal-State obligations |
| **Q2, Q4** | `ISM-Code/_base-and-amendments/` (`A.741(18)` through `MSC.353(92)`), `Casualty-Investigation-Code/_base-and-amendments/MSC.255(84).pdf` | Instrument identity and text confirmed |

### 4.3 Limitations recorded — not worked around

| Limitation | Effect | Class |
|---|---|---|
| **No licensed consolidated MARPOL Annex VI text.** The corpus holds the resolutions, not a consolidated Annex | Regulation numbering and content for regulations 20, 26, 27, 28 are established from the recitals and cross-references **inside `MEPC.346(78)`**, read directly. **No regulation is quoted verbatim** | `C_ACCEPTED_LIMITATION` (Q7) |
| **CLC / Fund / Supplementary Fund texts are not held.** `05-un-and-treaty-law/liability-and-compensation/` is explicitly *"citation/index only + verified status facts"*, and its own log instructs that **SDR limits be verified against official text before citing numerically** | Q1B is authored **without asserting any SDR limit**. The three tiers, the liable party, the funding source and the certification are stated; **the numbers are not** | `C_ACCEPTED_LIMITATION` (Q1) |
| **No copy of any revision of the IMSAS Framework and Procedures.** `A.1067(28)` is cited by identity | Q2's audit-scheme limb is built on the **III Code `A.1070(28)`**, which *is* held and verified, plus the mandating chain. The currency of the Framework resolution is flagged | `C_ACCEPTED_LIMITATION` (Q2) |
| **No Institute Time Clauses, York-Antwerp Rules or Marine Insurance Act 1963 text in the corpus** | Q3 is authored from the governed workflow and from `INTERNAL_REUSE_VERIFIED` donors (`QP2304-Q3`, `QP2407-Q8`) whose provisions were read at their own sittings | `C_ACCEPTED_LIMITATION` (Q3) |
| **No ship-repair contract standard form held** (Q6) and **no naval-architecture reference for skin-friction technologies** (Q9) | Both are authored as engineering and commercial practice, with the evidence class stated honestly on each claim rather than dressed as regulation | `C_ACCEPTED_LIMITATION` (Q6, Q9) |

### 4.4 Correction requests raised by this paper

**TSCR-3 re-reported as engaged and declined** (§4.1). **No new correction request is raised.** No
other corpus defect was found in the objects consumed.

---

## 5. THE PAPER'S HARDEST QUESTION

**Q7.** Its stem is verbatim identical to `QP2412-Q8`, which is one of the most thoroughly built
objects in the corpus — and **almost every regulatory statement in that object is wrong for June
2023**. The guidelines edition, the GHG strategy, the CII rating experience and the state of the
short-term-measure review all reverse. What survives is the structure of the four-step cycle, the
Part I / II / III architecture, and the regulation 26 numbering. **This is the clearest available
demonstration that an exact question is not an exact answer**, and it is recorded as such.

---

## 6. STANDING NOTE ON EDITIONS THE PAPER DOES NOT FIX

Two instruments are contract-selected rather than date-selected, and the paper does not say which
edition applies:

- **York-Antwerp Rules** (Q3). YAR 1994, 2004 and 2016 all exist at this sitting and which applies
  is a matter of the contract of affreightment, not of the sitting date. The answer says so rather
  than asserting one.
- **Institute Time Clauses — Hulls** (Q3). The 1983 and 1995 clause sets and the International Hull
  Clauses 2003 are all in use. The answer identifies the 3/4ths collision liability and unrepaired
  damage provisions by their function and standard numbering and states that the policy wording
  governs.

Both are recorded as `C_ACCEPTED_LIMITATION` rather than resolved by assumption.

---

## 7. PRODUCTION OUTCOME — recorded at 9/9

**Nine of nine authored.** Assembled mechanically from governed staging, which was then retired.
Staged-to-promoted identity proved over **234 authored fields, 0 mismatches**; the frozen intake
fields were protected by the assembler and none moved.

### 7.1 Final donor totals, as authored

| Class | Questions |
|---|---|
| **EXACT** (tier D) | **Q1** `QP2303-Q1` · **Q5** `QP2301-Q2` limb c) · **Q7** `QP2412-Q8` · **Q8** `QP2412-Q7` |
| **LIMB** (tier C) | **Q2**, **Q3** |
| **FAMILY** (tier B) | **Q4**, **Q9** |
| **FRESH** (tier C, no relation of any kind) | **Q6** |

**Five donors are 2023 objects and three of those are earlier than June 2023** — the first paper in
the batch where the normal MIW direction of donation occurs at all.

### 7.2 The two exact recurrences from the same December 2024 paper — the finding worth keeping

`QP2306-Q7` and `QP2306-Q8` are both **verbatim recurrences of questions from the same
December 2024 paper, across the same eighteen-month gap**.

- **Q7 required four separate reversals** — guidelines edition, GHG strategy, CII rating experience
  and the state of the short-term-measure review.
- **Q8 required none.**

> **A temporal delta must be computed, not inferred from how settled a subject feels.** Had the check
> been skipped on Q8 because cargo law moves slowly, that answer would have been right by luck rather
> than by verification. The two questions sit on one paper and make the point better than any
> instruction could.

### 7.3 QA result

| Check | Result |
|---|---|
| `validate_spec` | **0 errors**, 0 blocking. 13 warnings — 9 advisory word-band (every built question in the corpus exceeds that band; corpus median 1461 words) and 4 honest `no P1_PRIMARY_VERIFIED` on Q3, Q6, Q8, Q9 |
| `audit_paper` | **0 errors, 0 warnings** — all 14 checks pass |
| Deterministic double build | **byte-identical** |
| `run_toolchain` | 33 AUDIT **PASS** · 33 SPEC **PASS** · TEMPORAL **PASS** · RECURRENCE **PASS** · HEALTH **PASS**. DELIVERY reports only untracked/unstaged paths |
| `known_traps_check` | **240 checks, 0 failures** |
| `coverage_check` | **PASS** |
| Temporal sweep | 27 candidates on QP2306, **all 27 adjudicated, 0 defects** — every one is an exclusion statement, a provenance note, or a forward deadline set by an instrument in force at the sitting |
| **Seeded positive control** | A deliberate `MEPC.377(80)` contamination was seeded into Q7's model answer; **the sweep fired on it**, and the spec was restored byte-identical. The zero-defect result is therefore controlled |
| Assertion-level scan | Every mention of a future instrument — `MEPC.377(80)`, `MEPC.388(81)`, `MEPC.395(82)`, `A.1185(33)`, `A.1187(33)`, `A.1184(33)`, `MEPC.376(80)`, MS Act 2025, EU ETS, FuelEU, Net-Zero Framework — is an **exclusion**, never an assertion |
| UI, HTTP, 1280 and 375 | 9 cards · 5 modes · **Answer default on all nine** · search discriminates on within-paper-unique probes · 20 internal links resolve, 0 broken · **no horizontal overflow** · 19 tables all in scroll containers · **no console errors** |
| Delivery-surface contamination | **0 hits** after the fix below |

### 7.4 One real defect was found and fixed

The **delivery projection leaked production vocabulary**. `solvedQP/QP2306.html` carried the word
*donor* twice, and the phrase *"direct search … this session"* twice, in candidate-facing
`study_notes` Uncertainty sections on Q3, Q4, Q6 and Q9.

The review build may carry production metadata; **the delivery surface may not**, and this is exactly
the defect the QP2406 review recorded as rule 3. The four sentences were rewritten in candidate-facing
language, the paper was re-promoted and rebuilt, and the delivery surface now scans **completely
clean** — no host name, no host recurrence annotation, no *donor*, no *reverify*, no *before
publication*, no `TSCR`, no verification path, no absolute path, no source-PDF path.

**No scanner was weakened. The content was corrected.**

### 7.5 Global derived artefacts — validated, then reverted

Regenerating the index and the delivery surface produced changes in the global manifests, the year
and topic sheets, `solvedQP/`, and **four other papers' HTML**. That last is worth recording because
it is substantive rather than cosmetic:

> `QP2412-Q7` changed from *"Once in this set"* to **"Repeated — reworded · 2 sittings in this set"**,
> because `QP2306-Q8` is the same question. **The recurrence model independently confirmed the exact
> recurrence adjudicated by reading both printed stems.**

All of it was used to validate and then **reverted before commit**. The branch commits only its
twelve paper-owned files. **`solvedQP/QP2306.html` is deliberately not committed** — laptop
integration owns the customer projection and the global regeneration.
