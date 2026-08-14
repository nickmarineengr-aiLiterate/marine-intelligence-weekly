# QP2312 — TEMPORAL AND DONOR ANCHOR

**Paper:** QP2312 · December 2023 · printed serial `2312 EM` · MEO Class I · Engineering Management
**Branch:** `pastpapers/qp2312-founder-review`
**Baseline:** `18a272c7295f366b1719584eff1fe51e69966243` — current `main` (see §0)
**Built set at the baseline:** 252 questions across 28 papers, plus `QP2301` (9) on its own branch
**Corpus commit consumed:** `319524c24d11b2f89f33672c384b56e9ae1ab7db` (`RulesApp-Local-Input` `main`)
**Written:** 2026-08-13, before any answer was authored. Donor counts in §5 derived from the §6
detail table **last**, not first.

This is the second 2023 paper MIW has solved, and the first December sitting in the batch.

---

## 0. BASELINE — why this paper does NOT sit on the Batch 4 baseline

`QP2301` was cut from the recorded Batch 4 baseline `57b9342`. **This paper is cut from current
`main` at `18a272c` instead.** That is a governance decision, not a drift, and the reasoning is
recorded here because an unrecorded baseline change becomes an undocumented precedent.

`DESKTOP_QP_ALLOCATION_2023.md` §0.1 (on `pastpapers/batch4-baseline`) states the rule that
decides this: *do not reuse an older batch baseline, because a branch cut from it would compute
donor readiness against a corpus one whole paper short.* Between `57b9342` and `18a272c`:

| What changed on `main` | Why it binds this paper |
|---|---|
| **`f3fa210` integrated QP2408 and closed 2024** | `57b9342` is now itself **one paper short**. The corpus at that commit is 243 questions across 27 papers; at `18a272c` it is **252 across 28** |
| The header gate *"do not start this batch until QP2407 **and** QP2408 are live"* | At `57b9342` it was satisfied only in part, and §0.2 recorded a Founder override releasing it for QP2301 alone — expressly noting *"the QP2408 donors are therefore unavailable to **this paper**"*. That override was scoped to QP2301. The gate is now satisfied in full |
| **`QP2408-Q9` is a character-identical donor for this paper's Q5** | It exists only after `f3fa210`. Cutting from `57b9342` would have hidden the **August 2024** donor and forced Q5 onto the June 2026 one — a 30-month pull instead of an 8-month one |
| `f6b9cdf`, `d3f2cd5`, `b49ab3e`, `18a272c` — the repo-wide DG Shipping → DGMA audit | Settles the terminology question for this paper. See §7 |

**QP2301 remains rooted at `57b9342` and is not disturbed.** Integration onto `main` is by path
extraction, not merge — `f3fa210` records the concrete harm a stale base caused at QP2408's
integration — so a branch cut from current `main` is the safer input to that process, not a riskier
one.

**Referred to the Founder for ratification:** whether `18a272c` now becomes the recorded Batch 4
baseline for the four remaining allocated 2023 papers, or whether each is cut from `main` as it
opens. This paper does not decide that; it records what it did and why.

---

## 1. THE SITTING, AND THE FACT THAT GOVERNS EVERY DONOR

> **Every donor available to this paper is LATER than this paper.**

The solved corpus runs January 2023 (QP2301, on its branch) and then April 2024 → July 2026. This
sitting is December 2023. The usual MIW protection — that an earlier donor cannot drag later law
backwards — **does not exist on any question here.**

The standing batch rule was applied to all nine:

> **No donor statement is inherited. A donor supplies a ROUTE — the shape, the limbs, the order.
> Every sitting-relative statement is re-derived from the December 2023 position, and the
> re-derivation is recorded in that question's `temporal_review`.**

### 1.1 This paper is a whole-paper recurrence, and that is the headline donor fact

**All nine printed stems recur in `QP2606` (June 2026), question for question, in the same order.**
Seven are character-identical; Q7 and Q8 differ in wording and Q8 also in mark split (§6.1). The
December 2023 paper was set again, essentially unchanged, thirty months later.

That is a gift and a hazard in the same object. It means 9/9 donor coverage is real. It also means
the *nearest* donor for four questions is **thirty months later than the sitting** — the longest
pull in the batch so far — and June 2026 prose carries the 34th Assembly, the Merchant Shipping Act
2025, the DGMA rename, the Hong Kong Convention in force, MEPC 82/83/84 and the Net-Zero Framework,
none of which exists in December 2023. **QP2606 was therefore used as a route on every question and
as prose on none.** Where a closer donor existed it was preferred over the exact one (§6).

---

## 2. THE DECEMBER 2023 REGULATORY LINE

### 2.1 Operative at the sitting

| Instrument | Position at December 2023 |
|---|---|
| **Merchant Shipping Act, 1958** | The Indian statute in force. The **MS Act 2025 commenced 15 March 2026 — 27 months later** |
| **Directorate General of Shipping (DG Shipping)** | The correct name of the Indian maritime administration at this sitting. **DGMA is future** — see §7 |
| **32nd IMO Assembly** (adopted 6 December 2021) | The Assembly session whose instruments were in circulation for all or almost all of this month. `A.1155(32)` PSC procedures; `A.1156(32)` HSSC survey guidelines — **but see §3, this is the paper's live boundary** |
| **SOLAS II-1/3-1** — structural, mechanical and electrical requirements | Long settled and unamended. Read verbatim from the corpus copy of SOLAS. Bears on **Q8** |
| **SOLAS II-1/3-10** — goal-based ship construction standards | In force 1 January 2012 (`MSC.290(87)`); applies to bulk carriers and oil tankers ≥150 m contracted on/after 1 July 2016. Bears on **Q1** |
| **`MSC.287(87)`** International GBS for bulk carriers and oil tankers | The adopted standards. Operative |
| **`MSC.454(100)`** Revised GBS verification guidelines | Adopted December 2018 — the operative verification guidelines at this sitting |
| **`MSC.1/Circ.1343`** Ship Construction File guidelines | Operative |
| **ISM Code** as amended through **`MSC.353(92)`** (in force 1 January 2015) | The operative text. **No later amendment to the Code itself.** Bears on **Q5** |
| **`MSC.428(98)`** cyber risk in the SMS | Adopted 2017; addressed in the SMS no later than the first annual DOC verification after 1 January 2021 — so **already a mature requirement** at this sitting. Bears on **Q5** |
| **2023 IMO GHG Strategy — `MEPC.377(80)`, adopted 7 July 2023** | **Adopted and operative as policy five months before this sitting.** Bears on **Q4** |
| **`MEPC.376(80)`** 2023 LCA guidelines on life-cycle GHG intensity of marine fuels | Adopted July 2023 — operative |
| **`MEPC.346(78)`** 2022 SEEMP guidelines | Operative. `MEPC.395(82)` is 2024 and is **future** |
| **EEXI and operational CII**, MARPOL Annex VI ch. 4 as revised by `MEPC.328(76)` | Applicable since **1 January 2023** — operative for the whole of 2023. 2023 is the first CII data year, so the **first ratings are assigned in 2024** |
| **STCW 1978 as amended**, incl. `MSC.486/487(103)` (in force 1 January 2023) | Operative. The comprehensive STCW review is not adopted and is not law |
| **IGF Code** and STCW **reg. V/3** training for ships using low-flashpoint fuels | Operative. Bears on **Q4** |
| **PSSA guidelines `A.982(24)`** as amended by **`MEPC.267(68)`** | The operative PSSA identification and designation guidelines. Bears on **Q7** |
| **MARPOL** special areas, Annexes I–VI; **UNCLOS** Part XII | Operative. Bears on **Q7** |
| **`MSC-MEPC.2/Circ.12/Rev.2`** Revised FSA guidelines (2018) | The operative FSA guidelines. Bears on **Q9** |
| **York-Antwerp Rules 1994** | Named in the printed stem of **Q3**. YAR 2016 also exists; both bind only by contractual incorporation, never as law |
| **Marine Insurance Act, 1963 (India)**; Marine Insurance Act 1906 (UK) | Operative |
| **Indian Ocean MOU on Port State Control** | The regional PSC regime India belongs to. Bears on **Q2** |
| **MEPC 80 (3–7 July 2023)** | **The most recent MEPC session at this sitting** |
| **MSC 107 (31 May – 9 June 2023)** | **The most recent MSC session at this sitting** |

### 2.2 The 2023 GHG Strategy is settled here, and this is the one 2023 paper where it is

`DESKTOP_QP_ALLOCATION_2023.md` §3 makes the 7 July 2023 boundary the batch's headline hazard,
because it splits `QP2307`. **It does not bite here.** December is unambiguously after 7 July, so
the **2023 IMO GHG Strategy is operative** and the Initial Strategy of 2018 is superseded — a
day-independent conclusion, recorded as such rather than assumed. This is stated positively in
**Q4**.

What must NOT follow from it: the 2023 Strategy's indicative checkpoints and its net-zero-by-or-
around-2050 ambition are **policy**, not law. No mid-term measure had been adopted. There is **no
IMO carbon price, no GFI and no Net-Zero Framework** at this sitting; the only carbon price
touching any ship's account is regional, and the EU ETS extension to maritime does not begin until
**1 January 2024** — three weeks to a month *after* this sitting, on any December day.

---

## 3. THE 33rd ASSEMBLY BOUNDARY — the paper's highest-risk issue

> **The 33rd IMO Assembly adopted its resolutions on 6 December 2023. This paper prints
> `DECEMBER 2023` and NO DAY. The sitting may fall on either side of that date and MIW cannot
> establish which.**

### 3.1 What was established from primary text, and what was not

The exam day is **not recoverable**. The source copy prints month and year only; no serial, no
rubric and no host annotation carries a day. **No week-granularity distance is asserted anywhere in
this paper**, and no answer is written so that its correctness depends on the day.

What *was* established, by reading the resolutions themselves from the corpus copies:

| Resolution | Adopted | Document issued | Operative clauses |
|---|---|---|---|
| **`A.1185(33)`** Procedures for Port State Control, 2023 | **6 December 2023** | **2 January 2024**, reissued 5 March 2024 with editorial changes | ADOPTS · **INVITES** Governments to implement · REQUESTS review · **REVOKES `A.1155(32)`** |
| **`A.1186(33)`** Survey Guidelines under the HSSC, 2023 | **6 December 2023** | **11 December 2023** | ADOPTS · **INVITES** Governments to apply · REQUESTS review · **REVOKES `A.1156(32)`** |
| **`A.1184(33)`** Guidelines on Places of Refuge | 6 December 2023 | 11 December 2023 | not engaged by any question on this paper |

**Neither resolution defers its own effect.** There is no "shall take effect on" clause in either.
On the face of the instruments, adoption on 6 December 2023 carries revocation of the predecessor
from that date.

### 3.2 The adjudication — and why it makes both questions day-independent

Two questions touch the boundary: **Q2** (PSC) and **Q8** (annual versus periodical surveys under
the HSSC). Classified as the protocol requires:

| Class | Instrument |
|---|---|
| **Pre-sitting, operative** | `A.1155(32)`, `A.1156(32)` — certainly operative for the first five days of the month and in circulation throughout |
| **Adopted during the sitting window** | `A.1185(33)`, `A.1186(33)` — adopted 6 December 2023, inside the month the paper was sat |
| **Adopted but not yet in circulation** | `A.1185(33)` — **its text was not issued until 2 January 2024**, after every possible December 2023 exam day |
| **Post-sitting, PROHIBITED** | `A.1206(34)`, `A.1207(34)` — 34th Assembly, adopted 3 December 2025 |

Three facts make the day irrelevant to the answer, and all three are recorded in the questions
themselves rather than assumed here:

1. **Both instruments are recommendatory.** Their operative clause is *INVITES Governments* to
   implement or apply. Neither confers nor removes a legal power. **The legal framework for port
   State control, and the legal requirement to survey, are created by the conventions — not by
   these resolutions.** Q2 is therefore anchored on SOLAS I/19, MARPOL articles 5 and 6, LOAD LINES
   article 21, STCW article X and regulation I/4, MLC Title 5.2, TONNAGE article 12, AFS article 11
   and BWM article 9, plus the Indian Ocean MOU and Indian domestic law — none of which turns on
   6 December 2023. Q8 is anchored on SOLAS I/7–I/10 and the 1988 SOLAS and Load Lines Protocols.
2. **The substance did not change across the boundary in anything either question asks.** The
   initial-inspection / clear-grounds / more-detailed-inspection / detention structure, and the
   annual–intermediate–periodical–renewal survey structure, are the same in the 2021 and the 2023
   texts. A candidate answering either from the 2021 edition scores identically.
3. **On the PSC side the 2023 text was not obtainable in December 2023 at all.** It was issued as a
   document on 2 January 2024. No candidate could have been examined on its content and no
   Administration had yet received it.

**How the answers are written.** Q2 and Q8 state that the consolidated IMO procedures/guidelines in
circulation at the sitting were the 32nd Assembly editions, and that the 33rd Assembly adopted
revisions **on 6 December 2023, within the month of this sitting**, expressly declining to assert
which side of that date the paper fell. The answer's marks do not depend on the resolution number,
and the resolution number is never presented as the source of the legal power.

**This is trap 17 applied to a second boundary.** The batch's known day-dependency was the 7 July
GHG date; this paper adds a 6 December one, and it is narrower and sharper because it sits *inside*
the sitting month rather than in a different half of the year.

### 3.3 What is prohibited because of it

`A.1206(34)` (PSC procedures) and `A.1207(34)` (HSSC survey guidelines) are **34th Assembly, adopted
3 December 2025 — two years future.** `known_traps.md` Entries 5 and 22 record both as the *current*
instruments; that register is maintained for the present and is **inverted** for this sitting.
Neither number appears anywhere in this paper. The same inversion applies to `MEPC.395(82)`
(marked current, but 2024) against `MEPC.346(78)` (marked superseded, but operative here).

---

## 4. FUTURE AT THIS SITTING — PROHIBITED

| Item | Date | After the sitting by |
|---|---|---|
| **EU ETS extended to maritime transport** | 1 January 2024 | days to weeks |
| **MEPC 81** | 18–22 March 2024 | ~3 months |
| **MSC 108** and its resolutions | May 2024; in force 1 January 2026 | ~5 months |
| **SOLAS Consolidated Edition 2024** | in effect 1 July 2024 | ~7 months |
| **MLC 2006 — 2022 amendments** | in force **23 December 2024** | ~12 months |
| **MEPC 82** and `MEPC.395(82)` 2024 SEEMP guidelines | Sep–Oct 2024 | ~10 months |
| **Hong Kong Convention** | in force **26 June 2025** | ~18 months |
| **MEPC 83**; the IMO Net-Zero Framework and the GFI | April 2025; adoption deferred at the October 2025 extraordinary session and still not adopted | ~16 months + |
| **34th IMO Assembly** — `A.1206(34)`, `A.1207(34)`, all `A.12xx(34)` | adopted 3 December 2025 | ~24 months |
| **Merchant Shipping Act, 2025** (Act 24 of 2025) | commenced 15 March 2026 | ~27 months |
| **DG Shipping renamed DGMA** | 2026 — see §7 | ~29 months |
| **Bills of Lading Act 2025; Carriage of Goods by Sea Act 2025** | 2025 | ~20 months |
| **MASS Code** | adopted MSC 111, May 2026 | ~29 months |
| **MSC.560(108)** STCW harassment/bullying training | in force 1 January 2026 | ~24 months |

Every one of these appears in this paper **only as a declared exclusion**, never as content.

---

## 5. DONOR STATE — PREDICTED VERSUS ACTUAL

`DESKTOP_QP_ALLOCATION_2023.md` §4 predicted **9 exact/near, 0 family, 9/9 with a donor**, computed
against 234 built questions across 26 papers. That table was recomputed rather than read, as §0.3
requires.

**Recomputed at this baseline against 261 built questions across 29 papers: 9 / 9 with a donor.**
Nine exact or near, zero family-only, zero fresh-research questions. The prediction is confirmed on
count — and understated on quality, because the recomputation found **multiple donors on five
questions** and, on three of those, a donor materially closer to the sitting than the one the
prediction implied.

Derived from the §6 table: **7 character-identical** stems, **2 near** (wording and, on Q8, marks).
**Preferred donor is the exact June 2026 one on only four questions**; on five, a closer sitting was
preferred over an exact-but-distant one.

---

## 6. DONOR DECISIONS — question by question

| Q | Preferred donor | Sitting | Distance | Class | Why this one |
|---|---|---|---|---|---|
| Q1 | `QP2606-Q1` | June 2026 | +30 | **EXACT** | Character-identical. Only exact donor; `QP2409-Q2` (Sep 2024) read as a near/family cross-check |
| Q2 | `QP2606-Q2` | June 2026 | +30 | **EXACT** | Character-identical. `QP2406-Q3` (Jun 2024, +6) and `QP2504-Q2` (Apr 2025) read as closer PSC family and preferred for the inspection-mechanics prose |
| Q3 | `QP2606-Q3` | June 2026 | +30 | **EXACT** | Character-identical. `QP2509-Q3`, `QP2607-Q5`, `QP2506-Q3` read as the average/insurance family |
| Q4 | `QP2606-Q4` | June 2026 | +30 | **EXACT** | Character-identical and the **only** donor. Highest reversal load on the paper — see §6.2 |
| Q5 | **`QP2408-Q9`** | **August 2024** | **+8** | **EXACT** | Character-identical **and 22 months closer** than `QP2606-Q5`, which is equally exact. Closer sitting preferred |
| Q6 | **`QP2402-Q6`** | **February 2024** | **+2** | **EXACT** | Character-identical and **the closest donor relation in the 2023 batch to date**. `QP2606-Q6` also exact but +30 |
| Q7 | **`QP2502-Q9`** | **February 2025** | **+14** | **NEAR** | Same near-variant wording as `QP2606-Q7` but 16 months closer |
| Q8 | **`QP2412-Q4`** | **December 2024** | **+12** | **NEAR** | Same near-variant wording as `QP2509-Q9` and `QP2606-Q8`; closest of the three. **Marks differ — see §6.1** |
| Q9 | `QP2606-Q9` | June 2026 | +30 | **EXACT** | Character-identical. `QP2501-Q5` (Jan 2025) read as the FSA family; `QP2508-Q3` is FSA *applied*, not the method |

### 6.1 The one marks delta on the paper — Q8

QP2312 prints **`(8)` and `(8)`**. Every later sitting of the same question — `QP2412-Q4`,
`QP2509-Q9`, `QP2606-Q8` — prints **`(10)` and `(6)`**. The stem also differs by one character
class: QP2312 prints **`above-referred`** (hyphenated); the later sittings print `above referred`.

**The printed December 2023 split governs this paper.** The two limbs are recorded at 8 and 8, the
answer is built to that weighting, and the donors' 10/6 depth distribution was rebalanced rather
than carried. This is a real examiner change between sittings, not a transcription artefact, and it
is preserved rather than normalised.

### 6.2 Q4 carries the heaviest reversal load, and it has no closer donor

Q4 is decarbonisation upskilling and communication. Its only donor is thirty months later, and
almost everything a June 2026 answer would say about the *regulatory* driver for training —
Net-Zero Framework, GFI, MEPC 83 outcomes, the 2026 STCW review, `MSC.560(108)` — is future here.
What survives the reversal is the **2023 Strategy itself**, the IGF Code and STCW V/3 training
architecture, the ammonia and methanol competence gap as it stood in 2023, and the human-element
material, which carries no amendment boundary. The reversal is itemised in that question's
`temporal_review`.

### 6.3 Rejected donors, and why

| Rejected | For | Why |
|---|---|---|
| `QP2606-Q5` | Q5 | Equally exact but 22 months further away than `QP2408-Q9`. Route cross-checked; prose not used |
| `QP2606-Q6` | Q6 | Equally exact but 28 months further away than `QP2402-Q6` |
| `QP2606-Q7` | Q7 | Same wording variant as `QP2502-Q9` but 16 months further away |
| `QP2509-Q9`, `QP2606-Q8` | Q8 | Same wording variant as `QP2412-Q4` but further away; all three print the 10/6 split this paper does not use |
| `QP2508-Q3` | Q9 | FSA **applied** to lithium batteries in RORO carriage. This question asks for the **method itself**. Family, not donor |
| `QP2503-Q1`, `QP2507-Q8` | Q1, Q8 | Classification *requirements and dual class* — a different question from GBS and from rule formation. Read, not used |
| `QP2402-Q7` | Q8 | HSSC as its own subject rather than the annual/periodical distinction. Read as support for limb b |
| `QP2301-Q3` | Q3 | January 2023 marine-insurance question, but on **types of policy, liabilities and Indian agencies** — not losses, general average or warranties. Same year, wrong question. Recorded because a same-year donor would have been the batch's first, and it was checked and rejected on subject |

**`QP2301` is the only same-year paper in the corpus and it donates nothing to this paper.** That
was tested, not assumed.

---

## 7. TERMINOLOGY — DG Shipping, and why this paper does not use DGMA

`main` absorbed a repo-wide **DG Shipping → DGMA** audit at `f6b9cdf`, `d3f2cd5`, `b49ab3e` and
`18a272c`. That audit is recorded at `meoclass1/known_traps.md` Entry 6, and it **expressly
adjudicated the pastpapers case**: of 508 mentions across 88 files, the 266 in point-in-time
examination-paper content were classified as bucket (a) and **correctly left as `DG Shipping`,
because that was the accurate name at those sittings.** Entry 6 carries `GREP: SKIP — context-
dependent by design; do not blanket-scan`.

**This paper therefore uses `DG Shipping`, and that is now governed rather than merely conventional.**
The rename to the Directorate General of Maritime Administration followed the Merchant Shipping Act
2025 and took effect in 2026 — roughly 29 months after this sitting. `dgshipping.gov.in` was live at
this sitting and is not cited as a present-tense URL anywhere.

**No repo-wide terminology migration was performed from this branch, and no third variant was
invented.** The one item Entry 6 leaves open — whether the rename is correctly dated to 15 March
2026 or to June 2026 — is a *current-law* question that does not touch a December 2023 paper, and it
is left where it is, still referred.

---

## 8. CORPUS USE, EVIDENCE GRADES AND GAPS

**Corpus commit consumed: `319524c`.** Read-only. Nothing in the corpus was modified from this
branch.

| Question | Corpus support | Grade |
|---|---|---|
| Q1 | **SOLAS II-1/3-10 read verbatim** from the corpus copy of SOLAS, including the application thresholds, the goal statement in paragraph 2, the paragraph 3 route through recognized-organization rules and the paragraph 4 Ship Construction File, and the footnotes naming `MSC.287(87)` and `MSC.454(100)` | **P1 PRIMARY VERIFIED** |
| Q2 | **`A.1185(33)` read verbatim** from the corpus copy — adoption date, issue date, reissue note and all four operative clauses. `A.1155(32)` identified by its recital in that resolution | **P1 PRIMARY VERIFIED** for the boundary; the convention PSC articles are cited from the instruments themselves |
| Q3 | **Not held.** No marine-insurance, York-Antwerp or Indian Marine Insurance Act material in the corpus | `REFERENCE_PENDING`; authored from established marine-insurance law and practice, declared as such |
| Q4 | **`MEPC.377(80)` (2023 GHG Strategy) and `MEPC.376(80)` (LCA guidelines) held**; STCW chain held | **P1 / P2** |
| Q5 | **ISM Code chain held** — `A.741(18)` through `MSC.353(92)`; `MSC.428(98)` held | **P1 PRIMARY VERIFIED** |
| Q6 | ISM element 10.3 from the corpus copy of the Code; the rest is shipping economics and operations management, declared as such | **P1** + declared practice |
| Q7 | **Not held.** No PSSA guidelines and no Indian environmental-law material in the corpus | `REFERENCE_PENDING`; authored from the IMO PSSA guidelines and Indian statutory framework, declared as such |
| Q8 | **SOLAS II-1/3-1 read verbatim**; **`A.1186(33)` read verbatim** for the boundary | **P1 PRIMARY VERIFIED** |
| Q9 | **`MSC-MEPC.2/Circ.12/Rev.2` NOT HELD** — recorded in the corpus's own GHG instrument log as placeholder RQ-31 | `REFERENCE_PENDING`; the FSA method authored from the guidelines' established content, declared as such |

**The Merchant Shipping Act, 1958 is not held in the corpus.** The corpus's India holdings are the
Admiralty Act 2017, the MS Act **2025** and the Coastal Shipping Act 2025 — two of the three being
future at this sitting. Where the 1958 Act is relied on, the evidence grade says so.

### 8.1 CORPUS DEFECT FOUND — referred, not fixed

`true-source/03-imo-instruments/ISM-Code/INSTRUMENT_LOG.md` lists `A.1184(33)` as *"Revised
guidelines on implementation of the ISM Code by Administrations"* and files that PDF in the ISM-Code
folder. **The PDF is not that instrument.** Read directly, `A.1184(33)` is **Guidelines on Places of
Refuge for Ships in Need of Assistance**, adopted 6 December 2023 — which is what MIW's own
`known_traps.md` Entry 24 already records.

Consequences honoured here: **`A.1184(33)` is not cited as an ISM instrument anywhere in Q5**, and
the ISM implementation-guidelines line is not asserted from the corpus at all. Per the playbook this
is raised as a **`TRUE_SOURCE_CORRECTION_REQUEST` and referred to the Founder — it was not fixed
from this branch**, because QP production never edits True Source.

---

## 9. QUESTIONS WHOSE CORRECTNESS DEPENDS ON SITTING-DAY UNCERTAINTY

> **None.**

Two questions **touch** the 6 December 2023 boundary — **Q2** and **Q8** — and both are written so
that the answer is correct whichever day in December the paper was sat (§3.2). Each records the
boundary explicitly in `temporal_review` and states the position without asserting a side.

No other question on this paper has any day-dependency. Q4's boundary (7 July 2023) is five months
before the sitting on any December day and resolves in one direction only.

---

## 10. SOURCE GAPS AND ACCEPTED LIMITATIONS

1. **The exam day is unrecoverable** and is not asserted. No week-granularity distance appears
   anywhere in this paper.
2. **The source copy is a third-party-hosted copy**, not an officially verified DG Shipping / MMD
   original. `official_source_verified` is `false` on this paper as on every other.
3. **Marks: 6 × 16 = 96 against a printed `Total Marks – 100`.** Printed, reproduced, not corrected.
4. **Q3, Q7 and Q9 have no corpus holding.** Their evidence grade is declared in the question rather
   than concealed, and no provision has been invented to give them false authority.
5. **The corpus SOLAS base is the Consolidated Edition 2024**, in effect 1 July 2024 — *after* this
   sitting. II-1/3-1 and II-1/3-10 were checked against the amendment register and **neither was
   amended between December 2023 and 1 July 2024**, so the 2024 text states the December 2023
   position for both. Recorded because the direction of travel must be checked on every consumption.
6. **Printed anomalies preserved** — Q7's mismatched quotation marks (`"Andaman and Nicobar
   Islands'`), Q8's `SOLAS ch.ll-1` for chapter II-1, Q2(b)'s *"What are the right to appeal"*, and
   Q3's *"York Antwerp Rules 1994"* without a comma. Recorded, never corrected.
