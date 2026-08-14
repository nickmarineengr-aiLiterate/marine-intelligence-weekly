# QP2309 — SEPTEMBER 2023 — TEMPORAL AND DONOR ANCHOR

**Paper:** QP2309 · September 2023 · printed serial `2309 EM` · MEO Class I · Engineering Management
**Branch:** `pastpapers/qp2309-founder-review`
**Built from:** `bf5b53301e2a949867aa2ea864d7ae2596d5b1d2` (`origin/main` at session start)
**Corpus commit consumed:** `319524c24d11b2f89f33672c384b56e9ae1ab7db` (`RulesApp-Local-Input` `origin/main`, 0 ahead / 0 behind, tracked tree clean)
**Written before canonical assembly**, as the protocol requires. Nothing in Q1–Q9 was authored until this file existed.

---

## 0. BASELINE DECISION — why this branch is NOT on `18a272c`

The Batch 4 working baseline had been `18a272c`, and QP2312 and QP2304 both branch from it. **This paper does
not**, and the reason is recorded here rather than assumed.

Between QP2304 and this session `origin/main` advanced by three commits:

| Commit | What it did |
|---|---|
| `161c2b1` | Search + Updates architecture — rebuilt the matcher and the maintenance ledger across all paper pages |
| `dcd7826` | Two analysis documents. **No learning content changed** |
| `bf5b533` | **Integrated QP2301 onto `main`** and corrected three answers at the canonical spec |

The standing rule is to retain the fixed batch baseline **unless new integrated paper content changes
production truth.** That condition is met, and specifically:

1. **`bf5b533` is new integrated paper content.** January 2023 is now in the corpus, so the solved set is no
   longer 2024–2026. The allocation's §2 systemic fact — *every donor available to a 2023 question is later
   than the sitting* — has its **first exception**, and QP2301 is a same-year donor that a branch cut from
   `18a272c` cannot see at all.
2. **`bf5b533` changed answers at source.** QP2301 Q4, Q6 and Q7 were corrected. A baseline that predates
   those corrections would let a superseded statement be read as current donor truth.
3. **`161c2b1` changed the page build.** QP2309.html built on `18a272c` would be a pre-Search-architecture
   page landing in a post-Search-architecture `main`. `bf5b533`'s own message records that merging the
   QP2301 branch would have reverted live infrastructure and that path extraction was needed instead.

Integration is unaffected either way — the laptop integrates desktop branches by path extraction and never
by merge — so this choice costs nothing at integration and buys correct donor visibility.

**Branch point proved before any file was written:** `HEAD` = `merge-base(HEAD, origin/main)` = `origin/main`
= `bf5b533`.

### Donors that are pushed but NOT integrated

QP2312 and QP2304 are on their own remote branches and are **not** on `main`. They were read as donor
candidates because they are same-year and same-batch, and every use of them is labelled
**FOUNDER-REVIEW-PENDING** in the map below. No claim in this paper rests on an unintegrated paper alone.

---

## 1. SOURCE RECONCILIATION

| Checked | Result |
|---|---|
| Local file | `meoclass1/pastpapers/docs/SEPTEMBER 2023.pdf` — git-ignored, never committed |
| SHA-256 | `71240652cd655dea5ea9ce9283bef973ee50fb68319d03f9e83a679d8d38e42b` |
| Pages | **2** |
| Printed month / year | **SEPTEMBER 2023** |
| Printed serial | **`2309 EM`** — number first, no `Sr. No.` prefix, no dash. The reversed 2023 convention of allocation §1.1, recorded exactly as printed |
| Examination | `EXAMINATION OF MARINE ENGINEER OFFICER` |
| Function | `Marine Engineering Management at Management Level` |
| Subject | `ENGINEERING MANAGEMENT` |
| Class | `M.E.O CLASS – I` |
| Time | 3 hours |
| Rubric | *Answer SIX questions only* · *All questions carry equal marks* · `Total Marks – 100` |
| Region note | `(India 2023)` |
| **Question count** | **NINE — Q1 to Q9** |

**Method.** The text layer is born-digital and was extracted with PyMuPDF. **Both pages were then rendered
and read as images**, and the rendered text was reconciled line by line against the extraction. They agree
completely; no glyph is present in the image that the text layer lost, and no text-layer artefact is absent
from the page. Two encoding artefacts appear in the extraction only (`M.E.O CLASS �  I` for the en-dash, and
`development�s` for the curly apostrophe); the rendered page shows the correct characters and the spec
records the rendered form.

### 1.1 The question count was established by reading, not by the extractor

The allocation records that an automated extractor under-reads some 2023 papers, and the instruction for this
session is that **automated question count is not authority**. Both printed pages were read in full and the
nine stems were listed by hand before any recurrence tool was run.

**September 2023 is numerically well behaved** — unlike January and February. Every question is printed
`Q1.` through `Q9.` with the `Q` prefix and a full stop. There are **no bare numerals**, no skipped limb
letters, and no gap in the sequence. Q4 is the only question that spans the page break, its limb (a) closing
page 1 and limb (b) opening page 2; it is one question, not two.

### 1.2 Marks and subparts, as printed

| Q | Printed marks | Limb structure as printed |
|---|---|---|
| Q1 | (16) on the stem | `a.` `b.` `c.` — lower case, full stop, **no per-limb marks** |
| Q2 | (16) | none |
| Q3 | (16) | none |
| Q4 | (8) + (8) | `(a)` `(b)` — parenthesised lower case |
| Q5 | (16) | none |
| Q6 | (5) + (5) + (6) | `A.` `B.` `C.` — **upper case**, full stop |
| Q7 | (4) + (2+2+2+2) + (4) | `(a)` `(b)` with `(i)`–`(iv)` · `(c)` |
| Q8 | (6) + (2×5) | `(a)` `(b)` with `(i)`–`(v)` |
| Q9 | (16) | `(i)` `(ii)` `(iii)` run inline in the stem, no per-limb marks |

Every question totals **16**, and each limb-carrying question's limbs sum to 16 exactly.

### 1.3 Printed anomalies — preserved, never corrected

1. **The paper cannot reach its own printed total.** Instruction 1 requires six questions, instruction 2 says
   all carry equal marks, every question prints **(16)**, and the header prints **`Total Marks – 100`**.
   Six sixteens are **96**. The arithmetic does not close. Recorded as printed on both sides; the spec keeps
   `total_marks: 100` from the header and 16 per question from the stems, and states the discrepancy.
2. **Three different limb conventions in one paper** — `a.` (Q1), `(a)` (Q4, Q7, Q8), `A.` (Q6). Preserved.
3. **Q3 prints "and" twice** — *"the technical and operational **and** market-based measures"*.
4. **Q7 spells the same term two ways in adjacent limbs** — *"major non conformity"* at (b)(i), then
   *"nonconformities"* at (b)(ii).
5. **Q7(c) capitalises mid-sentence** — *"Under **W**hat circumstances"*.
6. **Q1's opening is not a grammatical sentence.** The SDG 5 title is quoted without quotation marks, giving
   *"Achieve gender equality and empower all women and girls **is** one of the sustainable development's
   goals"*. Preserved — a candidate sitting the paper read exactly this.
7. **Q6 uses straight double quotes** around *"conditions of assignment"* where the rest of the paper uses
   curly punctuation.
8. **Q8(b)(ii) ends on a comma** where its siblings end on a semicolon or nothing.

### 1.4 Editorial and host insertions — identified and excluded

The source copy is a third-party-hosted reproduction and carries material the examiner did not print:

- a page header and footer, and a diagonal watermark, on both pages;
- a **boxed advertisement** between the rubric and Q1, and a second advertisement block after Q9;
- a **per-question recurrence annotation table** under every question.

None of this is examination text. None of it is transcribed into `text_verbatim`. **The host is not named in
this file, in the spec, in any verification record or on any built page** — allocation §6.1 and known trap 14.

The recurrence annotations are recorded once per question in `host_recurrence_hint` and adjudicated as
**discovery-only**. They are the host's own backward-looking claim, they are not MIW truth, they create no
family edge, and they reach no candidate-facing surface. They are also demonstrably incomplete in the
directional sense the playbook §7.3 describes: Q6 carries eight prior sittings and Q7 three, while Q1 and Q4
carry none at all despite this paper reproducing earlier MIW-held stems word for word.

---

## 2. THE SEPTEMBER 2023 TEMPORAL LINE

September 2023 is **not** January/April 2023, and the difference is decided by one date.

### 2.1 The mid-year boundary — resolved, and resolved favourably

> **MEPC 80 adopted the 2023 IMO Strategy on Reduction of GHG Emissions from Ships on 7 July 2023
> (resolution MEPC.377(80)).**

The allocation splits the batch on this date: January–June sit under the **Initial Strategy of 2018**;
**August–December sit under the 2023 Strategy**; July alone is undecidable because the paper prints no day.

**September is unambiguously after it.** No day-granularity reasoning is needed and trap 17 does not arise
for this boundary. The 2023 Strategy is **adopted and operative as the Organization's strategy** at this
sitting — two months and some days old, and the freshest thing on the paper.

This is the single most important difference between QP2309 and QP2301/QP2304, and it is what makes Q3
answerable in the terms the examiner asked.

### 2.2 Operative at September 2023

| Item | Position at the sitting |
|---|---|
| **Merchant Shipping Act, 1958** | The governing Indian statute. The MS Act 2025 commenced **15 March 2026** — thirty months later. Standing statute trap for the whole batch |
| **2023 IMO GHG Strategy** (`MEPC.377(80)`) | **Adopted 7 July 2023.** Operative as strategy. Sets the basket of candidate mid-term measures and the 2025-adoption / 2027-entry-into-force indicative timeline |
| **LCA Guidelines** (`MEPC.376(80)`) | Adopted 7 July 2023 — operative |
| **EEXI and operational CII** | In force **1 January 2023**; the first CII reporting year is running at this sitting. `MEPC.328(76)` is the governing Annex VI revision |
| **2022 SEEMP Guidelines** (`MEPC.346(78)`) | Operative |
| **32nd IMO Assembly set** — see §2.4 | `A.1155(32)` PSC Procedures · `A.1156(32)` HSSC Survey Guidelines · `A.1157(32)` III obligations list. **All three operative** |
| **`A.1118(30)`** | Revised Guidelines on implementation of the ISM Code by Administrations, 2017. **Operative** |
| **IMO Council** | **40 Members.** `A.1152(32)` would enlarge it to 52 but requires acceptance by two thirds of Members and was **not in force** |
| **ISM Code** | As amended through `MSC.353(92)`, in force 1 January 2015. No later amendment to the Code text |
| **RO Code** | `MSC.349(92)` / `MEPC.237(65)`, mandatory from 1 January 2015 via SOLAS XI-1/1, MARPOL Annexes I and II, and the 1988 Load Line Protocol |
| **III Code** | `A.1070(28)`, mandatory 1 January 2016; IMO Member State Audit Scheme running |
| **Load Lines** | ICLL 1966 as modified by the 1988 Protocol, with the 2003 revised Annex B in force 1 January 2005 |
| **International Grain Code** | `MSC.23(59)`, mandatory under SOLAS chapter VI regulation 9 |
| **UNCLOS** | 1982, in force 16 November 1994. Unamended |
| **MLC 2006** | As amended through the **2018** set. The 2022 amendments enter force **23 December 2024** — future |
| **AFS 2001** | Cybutryne controls applied from 1 January 2023 |
| **Sulphur** | 0.50 % m/m global limit |

### 2.3 Future at September 2023 — PROHIBITED

| Item | Date | Why it bites on this paper |
|---|---|---|
| **33rd Assembly — the entire `A.118x(33)` set** | adopted **6 December 2023** | Three months after the sitting. Hits Q2, Q4, Q7 and Q9 |
| `A.1185(33)` PSC Procedures 2023 | 6 Dec 2023 | **Q9** — revoked `A.1155(32)` |
| `A.1186(33)` HSSC Survey Guidelines 2023 | 6 Dec 2023 | **Q4** — the donor uses it as its worked example of a resolution |
| `A.1187(33)` III obligations list | 6 Dec 2023 | **Q2** — the donor cites it |
| `A.1188(33)` ISM implementation guidelines | 6 Dec 2023 | **Q7** — revoked `A.1118(30)`. See §4 |
| **MEPC 81** | March 2024 | **Q3** — the MBM donor is built on it |
| **EU ETS applied to maritime** | 1 January 2024 | **Q3** |
| **FuelEU Maritime**, Reg. (EU) 2023/1805 | adopted 13 Sept 2023 | **Q3** — falls *inside* the sitting month. See §2.5 |
| **BBNJ Agreement** opened for signature | 20 September 2023 | **Q8** — falls *inside* the sitting month. See §2.5 |
| MEPC 82 / 83 | 2024–2025 | Q3 |
| IMO Net-Zero Framework / GFI | October 2025 | Q3 |
| Hong Kong Convention in force | 26 June 2025 | trap 5 family |
| SOLAS Consolidated Edition 2024 | 1 July 2024 | |
| MLC 2022 amendments in force | 23 December 2024 | Q1 |
| **Merchant Shipping Act, 2025** | commenced 15 March 2026 | whole paper — trap 11 |
| 34th Assembly `A.12xx(34)` | 3 December 2025 | Q4, Q9 |

### 2.4 The 32nd Assembly set — the finding that decides four questions

The 33rd Assembly resolutions **each revoked a 32nd Assembly predecessor**, and the whole solved corpus is
written for sittings *after* 6 December 2023. For September 2023 every one of those pairs inverts:

| Operative at this sitting | Revoked it, 6 Dec 2023 | Question |
|---|---|---|
| `A.1155(32)` — Procedures for Port State Control, 2021 | `A.1185(33)` | **Q9** |
| `A.1156(32)` — Survey Guidelines under the HSSC, 2021 | `A.1186(33)` | Q4, Q7 |
| `A.1157(32)` — non-exhaustive list of obligations | `A.1187(33)` | **Q2** |
| `A.1118(30)` — ISM implementation guidelines, 2017 | `A.1188(33)` | **Q7** |

Each identity and each revocation is taken from MIW's own read-at-source records, not inferred: the QP2404
verification record states that `A.1188(33)` was read at source *"including the adoption date and the
revoking paragraph"*, and QP2404, QP2401 and QP2402 each record the corresponding `(32)` predecessor by name.

### 2.5 Two boundaries that fall inside the sitting month — trap 17

The paper prints **SEPTEMBER 2023** and no day. Two relevant events fall inside that month:

- **FuelEU Maritime** (Regulation (EU) 2023/1805) was adopted **13 September 2023**;
- the **BBNJ Agreement** opened for signature **20 September 2023**.

**No day-dependent claim is made about either.** Neither is needed to answer any question on this paper:
Q3 is expressly about developments *at IMO*, and Q8 is expressly about UNCLOS itself. Both are therefore
handled by anchoring on material unaffected by the boundary, which is what trap 17 requires, and neither is
asserted to be in force, adopted-and-applicable, or signed at the sitting.

### 2.6 What changed between April 2023 (QP2304) and this sitting

The instruction not to reuse the April anchor blindly is well founded. Searched and found:

| Change | Date | Effect here |
|---|---|---|
| **2023 IMO GHG Strategy adopted** | 7 July 2023 | **Decisive.** April sits under the Initial Strategy 2018; September does not |
| **LCA Guidelines adopted** | 7 July 2023 | Newly available |
| MEPC 80 concluded | 3–7 July 2023 | Its whole output moves from future to operative |

Nothing else material to these nine questions moved between April and September 2023. The 33rd Assembly,
MEPC 81, EU ETS and the MLC 2022 amendments are future for **both** sittings, so the April anchor is correct
on those and is carried; it is the GHG boundary alone that must not be inherited.

---

## 3. DONOR MAP — derived by reading printed stems, not by score

The recomputation after QP2304 predicted **QP2309 — 5 strong candidates**, treated here as a lower bound.
Each of the nine stems was searched lexically and topically across all 279 solved questions (261 on `main`
plus the 18 on the two pushed 2023 branches), every plausible donor stem was read in full, and the
classification below is the result.

**Actual: seven of nine carry a donor** — three EXACT, three NEAR, one LIMB-LEVEL — and two are fresh
research. The prediction understated the paper.

| Q | Class | Donor | Sitting | Distance | Basis |
|---|---|---|---|---|---|
| **Q1** | **EXACT** | `QP2407-Q1` | July 2024 | **+10 m** | Stem identical word for word, same three limbs, same (16) |
| **Q2** | **LIMB-LEVEL EXACT** | `QP2401-Q5(b)` | January 2024 | **+4 m** | The 8-mark limb (b) is this 16-mark stem verbatim |
| **Q3** | **NEAR** | `QP2402-Q5` | February 2024 | **+5 m** | Identical but for the added *market-based* measures |
| **Q4** | **EXACT** | `QP2402-Q1` | February 2024 | **+5 m** | Both limbs identical word for word, same (8)+(8) |
| **Q5** | **NO DONOR** | — | — | — | Fresh research |
| **Q6** | **NO DONOR** | — | — | — | Fresh research |
| **Q7** | **NEAR** | `QP2404-Q8` | April 2024 | **+7 m** | Same stem; marks redistributed |
| **Q8** | **NEAR** | `QP2404-Q9` | April 2024 | **+7 m** | Same stem; marks redistributed |
| **Q9** | **LIMB-LEVEL** | `QP2312-Q2` §4 | December 2023 | **+3 m** | One step of the donor route is this whole question |

### 3.1 Per-question derivation

**Q1 — gender equality. EXACT, `QP2407-Q1` (July 2024).**
The printed stems are the same sentence, the same three limbs in the same order, and the same (16). Nothing
in the wording differs. Also read and classified: `QP2503-Q3` and `QP2507-Q6` (March 2025 / July 2025) print
the *same subject* on a different skeleton — an (8)+(8) split that asks for challenges faced by women and
drops the Chief Engineer limb entirely. **NEAR, family, not preferred** — reusing their route would answer a
question this examiner did not ask. `QP2412-Q1` (SDGs generally, December 2024) is **topical-only, rejected**:
it asks the candidate to choose any two SDGs, which is a different task.

**Q2 — Recognized Organizations. LIMB-LEVEL EXACT, `QP2401-Q5(b)` (January 2024).**
`QP2401-Q5(b)` prints *"What is a Recognized organization? What are the salient features of the R.O. Code?
How do Administrations monitor R.O.s?"* — this paper's entire Q2 stem, word for word, **as an 8-mark limb**.
`QP2607-Q3(b)` (July 2026) is the identical limb again at +34 months. The route transfers; **the depth does
not**. This examiner allots sixteen marks to what January 2024 allotted eight, so the answer must carry
roughly twice the scoring propositions, and the donor cannot supply the second half.
`QP2408-Q1` (August 2024, +11 m) is the **depth donor**: a full 16-mark RO Code question split (8) approval
requirements / (8) oversight mechanisms, which is exactly the material the extra eight marks need.
Two donors, different jobs, both recorded. Rejected: `QP2312-Q8`, `QP2304-Q9`, `QP2412-Q4` and `QP2606-Q8`
are classification-society *survey* questions that mention ROs in passing — **topical-only**.

**Q3 — GHG measures. NEAR, `QP2402-Q5` (February 2024).**
`QP2402-Q5` prints *"…with respect to the technical and operational measures…"*. This paper prints
*"…the technical and operational **and market-based** measures…"*. One clause added; everything else is the
same sentence and the same (16). **Question delta: a third measure class is now examinable.**
The MBM material exists at `QP2408-Q4` (August 2024) — but it is built on **MEPC 81, March 2024**, which is
six months *after* this sitting. `QP2408-Q4` is therefore **read for structure and rejected for content**:
the shape of an MBM answer transfers, its every factual anchor is reversed in §4.
Also read: `QP2407-Q4`, `QP2409-Q3`, `QP2411-Q7` — all revised-GHG-Strategy questions, **NEAR family**,
useful for the Strategy's own architecture and used only for that.

**Q4 — IMO structure and instrument hierarchy. EXACT, `QP2402-Q1` (February 2024).**
Three donors print this stem verbatim, both limbs, same (8)+(8): `QP2402-Q1` (Feb 2024, **+5 m**),
`QP2407-Q3` (July 2024, +10 m) and `QP2502-Q1` (Feb 2025, +17 m). The allocation's known-relations table
named `QP2502-Q1`; **`QP2402-Q1` is preferred because it is the nearest later sitting**, which minimises the
amount of the donor's sitting-relative prose that has to be reversed. The other two are recorded and read.

**Q5 — grain shift and grain stability criteria. NO DONOR. Fresh research.**
Swept for `grain`, `statical stability`, `heel`, `righting`, `metacentric`, `free surface`, `bulk cargo`,
`liquefaction`, `IMSBC` across all 279 questions. **Nothing on grain stability exists in the corpus.**
The nearest neighbours were read and rejected: `QP2501-Q9` / `QP2507-Q4` (liquefaction of solid bulk cargo)
turn on a *different physical mechanism* — a cargo behaving as a liquid, not a dry cargo surface shifting to
a new angle of repose — and `QP2501-Q8` (parametric rolling) is a seakeeping question. A low similarity score
here is not a wording difference; **the question is genuinely new to MIW.**

**Q6 — conditions of assignment. NO DONOR. Fresh research.**
Swept for `load line`, `freeboard`, `assignment`, `watertight`, `weathertight`, `hatch cover`, `deck line`,
`draught mark`. **One hit in 279 questions** — `QP2511-Q1`, and only because it mentions hatch covers while
discussing bulk carrier losses under SOLAS chapter XII. The Load Line Convention has never been the subject
of an MIW question. **This is the freshest question on the paper**, and it is the one where the corpus helps
most (§5).

**Q7 — audit versus survey, RO action on ISM certificates. NEAR, `QP2404-Q8` (April 2024).**
Same question, limb for limb. Two deltas:
*Marks* — QP2404 prints (a) **2**, (b) **8** as one block, (c) **6**; this paper prints (a) **4**,
(b) **2+2+2+2**, (c) **4**. The audit/survey distinction is worth **double**, each of the four scenarios is
now separately weighted, and the invalidation limb is worth **less**. The answer is re-balanced accordingly;
the donor's proportions would lose marks here.
*Wording* — QP2404 prints "major nonconformity", this paper "major non conformity".
**And one reversal that changes the citation entirely — see §4.** Also read: `QP2406-Q5` (June 2024), a
different ISM question about functional requirements and internal audit — **topical-only, rejected**.

**Q8 — UNCLOS. NEAR, `QP2404-Q9` (April 2024).**
Stem materially identical, including the same five zones in the same order. **Marks delta is the whole
difference**: QP2404 prints (a) **8** / (b) **8**; this paper prints (a) **6** / (b) **2 each = 10**. The
environmental-protection limb is worth *less* and the five zone definitions are worth *more* and are now
individually weighted. The donor's balance is wrong for this paper and is rebuilt.
Rejected: `QP2508-Q9` / `QP2602-Q9` share the zones vocabulary but ask a **different question** — sovereign
rights and jurisdiction plus a missing-cadet scenario. **Topical-only.** `QP2604-Q7` / `QP2601-Q7` are flag
State duties. Rejected.

**Q9 — port State control provisions. LIMB-LEVEL, `QP2312-Q2` (December 2023).**
No corpus question asks this. What exists is **one step inside two donor routes**: `QP2312-Q2` step 4 and
`QP2606-Q2` step 3, both headed *No more favourable treatment*, each covering non-Party ships and below-size
ships in a handful of bullets — and each worth perhaps two of its paper's sixteen marks. **This paper makes
that step the entire question and adds a third limb** (what a port State does with a certificate issued by a
non-Party to its own ships), which neither donor addresses at all.
So the classification is **limb-level, not near**: the donors seed roughly one sixth of the answer and the
rest is fresh. `QP2312-Q2` is the nearest in time (+3 months, same year) and is **FOUNDER-REVIEW-PENDING**;
`QP2606-Q2` (June 2026, integrated) supplies the treaty citations for the no-more-favourable-treatment
principle and is used for that. Rejected as donors: `QP2504-Q2`, `QP2406-Q3`, `QP2512-Q8` — clear grounds,
detainable deficiencies and detention review are all a **different** part of the PSC regime.

### 3.2 Same-year relations

The batch rule is to prefer same-year donors where genuinely equivalent, because they minimise temporal
reversal. On this paper the rule produces **one** preference and no more:

- **Q9 → `QP2312-Q2` (December 2023, +3 months)** — the closest donor available to any question on this
  paper, and the only same-year relation that is genuinely on point.
- **QP2301 (January 2023), now integrated, donates nothing.** Its nine questions were read; none is on any
  subject this paper examines. Its value to this session was the *baseline decision* (§0), not a donor.
- **QP2304 (April 2023) donates nothing.** Read; no overlap.

Same-year proximity was **not** allowed to override task equivalence anywhere. Where a same-year paper was
merely adjacent — `QP2312-Q8` on classification societies against this Q2, `QP2304-Q4` against this Q9 — it
was rejected in favour of a later donor that actually asks the same question.

### 3.3 Donor direction — every donor is later

| Donor | Distance | Direction |
|---|---|---|
| `QP2312-Q2` | +3 months | later |
| `QP2401-Q5` | +4 months | later |
| `QP2402-Q1`, `QP2402-Q5` | +5 months | later |
| `QP2404-Q8`, `QP2404-Q9` | +7 months | later |
| `QP2407-Q1` | +10 months | later |
| `QP2408-Q1`, `QP2408-Q4` | +11 months | later |
| `QP2606-Q2` | +34 months | later |

**No donor pre-dates this sitting.** The standing batch rule therefore applies without exception:

> No donor statement is inherited. Every sitting-relative statement is re-derived from the September 2023
> position, and the re-derivation is recorded in that question's `temporal_review`.

A donor is a route. Not one sentence of donor prose carrying a date, an edition, a status or a "current"
is reused.

---

## 4. LATER-STATE REVERSALS — question by question

These are the specific statements that are **true in the donor and false at this sitting**. Each is reversed
in the authored answer and recorded in that question's `temporal_review`.

### Q7 — the sharpest reversal on the paper

`QP2404-Q8` is built on **`A.1188(33)`, the 2023 Guidelines on implementation of the ISM Code by
Administrations, adopted 6 December 2023**, and its paragraph references — 1.3.1, 1.3.2, 4.4.2, 4.5.1,
4.13.2, 4.13.3, 4.14.1, 4.14.2, 4.14.3 — are that resolution's numbering. It is correct for April 2024.

**At September 2023 `A.1188(33)` does not exist.** The operative instrument is **`A.1118(30)`**, which
`A.1188(33)` revoked *three months after this sitting*. The QP2404 record puts the same point in the opposite
direction, warning that *"citing A.1118(30) here is a wrong-edition error"* — for September 2023 the polarity
inverts exactly, and citing `A.1188(33)` would be the wrong-edition error.

**MIW holds no copy of `A.1118(30)` and it has not been read at source.** So the answer is built the honest
way: its substance rests on **ISM Code section 13**, which *is* held in the corpus, *is* mandatory, and has
been unamended since `MSC.353(92)`, together with **MSC/Circ.1059–MEPC/Circ.401** (16 December 2002) on
observed major non-conformities. `A.1118(30)` is cited **by identity only**, as the operative guidelines
edition at the sitting. **No paragraph number from `A.1188(33)` is carried across**, because the paragraph
numbering of `A.1118(30)` is not known to MIW and inventing a cross-walk would be fabrication.

QP2404's own read-at-source finding — that the substance of the paragraphs used is *largely unchanged*
between the two editions — is what makes the mandatory-text route safe. It is recorded as the reason, not
used as a licence to cite paragraphs that were not read.

### Q4

The donor's worked example of an Assembly resolution is **`A.1186(33)`** (6 December 2023) — future.
Replaced with **`A.1155(32)`**, Procedures for Port State Control 2021, adopted December 2021 and operative
at this sitting. `A.1152(32)` is carried forward unchanged: the Council is **40 Members**, and the
enlargement to 52 is adopted but **not in force**, which is true at both sittings.

### Q2

The donor cites **`A.1187(33)`** (6 December 2023) — future. Replaced with **`A.1157(32)`**, the
non-exhaustive list of obligations operative at this sitting. The RO Code itself, `MSC.349(92)` /
`MEPC.237(65)` mandatory from 1 January 2015, and the III Code `A.1070(28)` are unchanged and carry across.

### Q3

The donor `QP2402-Q5` cites `MEPC.377(80)`, `MEPC.376(80)` and `MEPC.346(78)`. **All three are adopted before
this sitting and all three survive** — the February 2024 donor is temporally clean on its citations, which is
unusual and is recorded as such.
What must be reversed is everything downstream of **MEPC 81 (March 2024)**, on which the MBM donor
`QP2408-Q4` is entirely built. At September 2023 the correct statement of the market-based position is the
one the 2023 Strategy itself makes: a **basket of candidate mid-term measures** combining a technical element
and an economic element, **under development**, with adoption indicated for 2025 and entry into force for
2027. Nothing is agreed, nothing is adopted, and no MBM instrument exists. **EU ETS (1 January 2024) and
FuelEU Maritime are not brought in**, the latter also for the §2.5 reason.

### Q9

Any statement resting on **`A.1185(33)`** is reversed to **`A.1155(32)`**. The underlying treaty provisions —
the control articles and the no-more-favourable-treatment provisions in SOLAS, MARPOL, Load Lines and STCW —
are unchanged between the two editions and carry across on their own authority.

### Q1

`QP2407-Q1` is checked and **passes without reversal**. Its regulatory spine is MLC 2006 as amended through
the **2018** amendments, which is correct at both sittings — the 2022 amendments enter force 23 December 2024
and are future for July 2024 as well. Its reference to the **G-SMART** programme in the appendix to the 2023
IMO GHG Strategy is likewise safe, that Strategy being adopted 7 July 2023. The Merchant Shipping Act, 1958
governs at both sittings. **This is the cleanest donor on the paper.**

### Q8

`QP2404-Q9` is checked and **passes without reversal**. UNCLOS was concluded in 1982 and entered into force
on 16 November 1994; nothing in Parts II, V, VI, VII or XII changed between April 2024 and September 2023 or
at any point between them. Risk is **LOW**. The only live edge is the BBNJ Agreement (§2.5), which is
excluded.

---

## 5. CORPUS USE — what was consumed, and what could not be

Corpus commit **`319524c`**, read-only. QP production never edits True Source.

| Instrument | Held? | Used for | Status |
|---|---|---|---|
| **UNCLOS** — `05-un-and-treaty-law/UNCLOS/_base/` | **yes**, official text | Q8 | **Primary. Unamended since 1982 — the ideal case: the held text *is* the sitting text** |
| **ISM Code** chain — `A.741(18)` → `MSC.353(92)` | **yes**, official resolution chain | Q7 | **Primary.** `MSC.353(92)` is the last amendment to the Code; the held text is the September 2023 text |
| **RO Code** — `RO_code.pdf` | yes | Q2 | Usable, **evidence downgraded**: `RQ-25` leaves edition and completeness unverified |
| **Load Lines** — `official-sources/load_line_convention_2021_edition.pdf` | **yes**, 46 MB official consolidated edition, **READ AT SOURCE** | Q6 | **Primary, and the best-placed source on the paper** — see §5.3 |
| **PSC procedures** — `A.1185/1186/1187(33)` | held, but **wrong edition** | Q9 | **NOT CONSUMED.** All three are 6 December 2023 — future for this sitting. `A.1155(32)` is **not held** |
| **GHG** — `MEPC.376/377(80)` | held | Q3 | **NOT QUOTED.** `RQ-30` marks title-page identity confirmation as **blocking for citation**. Cited by identity and adoption date only |
| **International Grain Code** `MSC.23(59)` | **no** | Q5 | **Not held.** Evidence downgraded accordingly |
| **Intact Stability Code 2008** | held by reference | Q5 | Adjacent only; grain criteria are not in it |

### 5.3 The Load Lines read — a finding about the source, recorded not written back

Q6 is the one question on this paper whose substance was read at a primary source in this session,
and the read produced a finding about the **source** that is worth recording separately.

The corpus publication carries **no text layer** — it is a page-image publication — so Annex I
chapter II was inspected by rendering pages and reading them, which the protocol permits where a
primary source exists only in image form. Read that way, its own foreword states:

- the consolidated text in Part 3 is current **as of 31 December 2021**;
- the amendment chain runs to **resolution MSC.375(93), adopted 22 May 2014**;
- Part 5 is the **Form of record of conditions of assignment of load lines**, which lists each
  fitting individually — deck, number, material, coaming dimensions, height, type and closing
  appliances down to the number of clips.

**Why this matters for this paper.** The consolidation date is **twenty-one months BEFORE the
sitting**. The source is therefore *structurally incapable* of introducing a post-sitting amendment
— the opposite of the corpus's usual problem on this paper, and the reason Q6 carries the lowest
temporal risk of any question here.

**Why it matters beyond this paper.** The corpus records the post-2021 Load Lines chain as
unverified (`RQ-09`). This read **materially narrows** that gap: the edition's own cutoff is now
known, and the residual window is only 1 January 2022 to September 2023. It does **not** close it.

**This is recorded here and is NOT written back to the corpus.** QP production never edits True
Source, and no new `TRUE_SOURCE_CORRECTION_REQUEST` is raised — nothing was found to be *wrong*,
only better bounded than the review queue currently records.

### 5.1 Referrals carried, not consumed

- **`A.1184(33)` corpus mislabel — CARRIED, NOT CONSUMED.** `03-imo-instruments/ISM-Code/INSTRUMENT_LOG.md`
  records `A.1184(33)` as *"Revised guidelines on implementation of the ISM Code by Administrations"*. MIW's
  own read-at-source record identifies `A.1184(33)` as **Guidelines on places of refuge for ships in need of
  assistance** (revoking `A.949(23)`), and identifies the ISM implementation guidelines as **`A.1188(33)`**.
  The two cannot both be right. **This session consumed neither**, because both resolutions are 6 December
  2023 and therefore future for this sitting — the mislabel could not affect this paper even if it were
  resolved. It is re-raised, not re-adjudicated, and **no new TRUE_SOURCE_CORRECTION_REQUEST is opened**.
- **`RQ-25`** (RO Code edition) — carried into Q2's evidence grading.
- **`RQ-09`** (Load Lines post-2021 amendments) — carried into Q6's evidence grading.
- **`RQ-30`** (GHG resolution identity, blocking for citation) — carried into Q3's evidence grading.
- **`RQ-27`** (A.1185/1186/1187(33) identity, blocking for citation) — **moot here**, the whole set being
  future for this sitting.

### 5.2 Evidence gaps recorded honestly

1. **Q5 has no primary source in the corpus.** No Grain Code, and the grain criteria are not in the Intact
   Stability Code. The answer is authored from the settled architecture of the regime — SOLAS chapter VI
   regulation 9 mandating the International Grain Code — and **no numerical criterion is stated as a quotation
   from a text that was not read**. Where a figure is given it is labelled by its status.
2. **`A.1118(30)` is identified but not held** (Q7). Handled as §4 describes.
3. **`A.1155(32)` is not held** (Q9). Cited by identity, adoption session and revocation date, all of which
   are established from MIW's own records; its clause numbering is **not** asserted.
4. **No independently authoritative DG Shipping / MMD copy of this paper exists.** The source copy is a
   third-party reproduction and `official_source_verified` is `false`, as for every paper in the set.

---

## 6. SUMMARY OF THE ANCHOR

| | |
|---|---|
| Sitting | **September 2023** |
| Serial | **`2309 EM`** |
| Manual question count | **9** — read from both printed pages before any tool was run |
| Numbering anomalies | **none in the numbering itself**; three limb conventions, and the 96-versus-100 total |
| Donors | **7 of 9** — 3 EXACT, 3 NEAR, 1 LIMB-LEVEL |
| Fresh research | **Q5, Q6** |
| Prediction | 5 strong candidates — **understated; actual 7** |
| Same-year donors | **1** (`QP2312-Q2`, +3 months, review-pending) |
| Donor direction | **all later**; +3 to +34 months |
| Decisive temporal fact | **2023 GHG Strategy adopted 7 July 2023 — operative** |
| Sharpest reversal | **Q7** — `A.1118(30)`, not `A.1188(33)` |
| Prohibited set | **the entire 33rd Assembly**, MEPC 81 onward, EU ETS, MS Act 2025 |
| Corpus commit | **`319524c`** |
