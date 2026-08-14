# QP2302 — FEBRUARY 2023 — TEMPORAL AND DONOR ANCHOR

**Paper:** MEO Class I, Engineering Management, **February 2023** (India), printed serial `2302 EM`
**Branch:** `pastpapers/qp2302-founder-review`
**Branch baseline:** `124dfbec4db992f1abb3c46bdc65e04ea87b8e6c`
**Corpus commit consumed:** `319524c24d11b2f89f33672c384b56e9ae1ab7db` (`RulesApp-Local-Input` `origin/main`)
**Source SHA-256:** `5e16dca72cb492f70db244a61600f521d2d2fc4a997f6ba0d459da71752187a1`

This file is the paper's temporal and donor authority. It was completed **before** final canonical
assembly and revised at §7 once the nine answers were written.

---

## 0. BASELINE DECISION — why this branch is on `124dfbe` and not on `d6d95e8`

QP2303 branched from `d6d95e8` (the QP2312 integration). Since then `origin/main` advanced twice:

| Commit | What it is | Class |
|---|---|---|
| `7019445` | **Integrate QP2304 (April 2023)** — 31 papers, 279 questions | **learning content** |
| `124dfbe` | Fix SolvedQP health-check email recipient (`.github/workflows/`) | infrastructure only |

The 2023 desktop precedent is to refresh a paper baseline when newly integrated learning content
**materially changes donor truth**, and not for infrastructure-only movement. Both tests were applied
and the first one fires:

> **`QP2304-Q7` (April 2023) is a Bunker-Convention-against-CLC-92 question, and it is the closest
> donor in time available to this paper anywhere in the corpus — `+2 months`.** Before `7019445` the
> nearest donor for `QP2302-Q9` was `QP2402-Q2` at `+12 months` or `QP2409-Q6` at `+19 months`. That
> is a material change to donor truth on this paper, not a global-artefact change.

The branch therefore takes the current `origin/main` tip. `124dfbe` is carried because it sits on top
of `7019445` and is a CI workflow file that touches nothing this paper reads. Merge-base was proved
equal to `origin/main` before authoring began.

**Not branched from QP2303 or from any other review branch**, per the allocation's branch rules.

### Donors that are pushed but NOT integrated

`QP2309` (`9631b2e`) and `QP2303` (`2eed92e`) are complete and pushed but are not yet on `main`. Both
were read **from their pushed branches** for donor derivation, exactly as QP2303 read QP2304 and
QP2309 from theirs. The derivation pool is therefore **33 papers · 297 questions**, not the 279 that
`main` alone carries.

---

## 1. SOURCE RECONCILIATION

| | |
|---|---|
| Source copy | `meoclass1/pastpapers/docs/FEBRUARY 2023.pdf` — **git-ignored, never committed** |
| Host | Third-party. Recorded only in the git-ignored `verification/LOCAL_SOURCE_PROVENANCE.md`. **Never named in this public repository** |
| Pages | 2 |
| Printed serial | **`2302 EM`** — number first, no `Sr. No.` prefix, no dash. Recorded exactly as printed and deliberately **not** normalised to the 2024 `Sr. No. EM – 2406` shape |
| Printed month/year | `FEBRUARY 2023`, `(India 2023)` |
| Subject | `ENGINEERING MANAGEMENT`, Function: Marine Engineering Management at Management Level, `M.E.O CLASS – I` |
| Rubric | `Answer SIX questions only`; `All questions carry equal marks`; `Total Marks – 100`; `TIME ALLOWED - 3 HOURS` |
| Questions | **NINE** |

### 1.1 The question count was established by reading, not by the extractor

The allocation file records that an automated extractor **under-reads** the 2023 papers, and February
is the worst case in the year. Both pages were rendered at 200 dpi and read as images, and the nine
printed questions were counted off the page before any text was trusted.

A naive `^Q\d` pattern finds **seven** questions on this paper and silently drops two. A naive
`^\d\.` pattern collides with the four-item `NB:` rubric and shifts every question by three. Both
failure modes were reproduced deliberately during intake so that the count could not be taken on
trust; the count of nine comes from the rendered pages.

### 1.2 The printed numbering is inconsistent — preserved exactly

| Printed as | Question |
|---|---|
| `Q1.` `Q2.` `Q3.` | Q1, Q2, Q3 |
| **`4.`** — bare, and with **no space** after the point (`4.State the difference…`) | Q4 |
| **`5.`** — bare | Q5 |
| `Q6.` `Q7.` `Q8.` `Q9.` | Q6, Q7, Q8, Q9 |

This matches `DESKTOP_QP_ALLOCATION_2023.md` §1.3 exactly and confirms the intake audit. **The bare
numbering is not normalised.** A candidate sitting this paper saw `4.` and `5.` without the `Q`.

### 1.3 Marks and subparts, as printed

> **NO MARK FIGURE IS PRINTED ANYWHERE ON THIS PAPER** — not against a question, not against a limb.

This is a stronger statement than QP2303 could make (which printed a complete 16 against two
questions). Every mark figure carried in the spec is therefore **derived from the rubric, not read
from the page**, and the derivation is recorded rather than concealed:

- instruction 2 states all questions carry equal marks;
- six answered questions are required;
- the paper prints `Total Marks – 100`;
- six equal questions against 100 gives **16.67**, and every question in the solved corpus that does
  print a figure for this format prints `(16)`.

`total_marks` is carried as **16 per question by rubric**. Six answered at 16 totals 96 against the
printed 100. **That discrepancy is on the source copy and is reproduced, not corrected.**

Limb labelling as printed: `a) b)` on Q1, Q3, Q5, Q7, Q8; `a) b) c)` on Q2; **`(a) (b)`** bracketed on
Q6 alone; no limbs on Q4 and Q9. The inconsistency is preserved.

### 1.4 Printed anomalies — preserved, never corrected

Every one of these is reproduced in `text_verbatim` and recorded here. **None is repaired.**

| Q | Printed | The apparent intention | Handling |
|---|---|---|---|
| Q1 | `''Big Data "` | opening quote is two apostrophes, closing is one double quote | preserved |
| Q1 | `initiatives. with brief introduction` | sentence opens lower-case after a full stop | preserved |
| Q1 | `future transformation **or** the shipping industry` | `of` | preserved; the answer reads it as `of` and says so |
| Q2 | `Which all IMO instruments covered in the code.` | Indian-English elision of *are* | preserved |
| Q3 | `C02` | `CO₂` — a **zero**, not the letter O | preserved |
| Q3 | `Phase 2 ( f 20% - 30% reduction)` | `(of 20% - 30% reduction)` — a stray `f` | preserved; and see §4 Q3, because the *substance* of this parenthesis is also wrong |
| Q4 | `4.State` | missing space | preserved |
| Q4 | `calculated .JS per this form?` | `as per this form` | preserved |
| Q5 | limb `a)` printed with **no `b)`** | a lone labelled limb | preserved; the question is treated as one limb carrying three instructions |
| Q5 | `''Effective communication"` | mixed quotation marks | preserved |
| Q5 | `examples *of*` — the word `of` is set in **italics** | typographic accident | preserved as plain text; noted here |
| Q6 | `a Bill of lading` — lower-case `l` mid-sentence, against `Bill of Lading` elsewhere in the same limb | inconsistent capitalisation | preserved |
| Q7 | `Cortra rotating Propellers.` | **Contra-rotating** propellers | preserved; the answer names the device correctly once and says why |
| Q8 | `On-board & On-shore **Compliant** Procedures` | **Complaint** procedures | preserved. **This is the single most consequential misprint on the paper** — see §4 Q8 |
| Q9 | `Bunker Convention2001` | missing space | preserved |
| Q9 | `0il` | `Oil` — a **zero** | preserved |

### 1.5 Editorial and host insertions — identified and excluded

The source copy carries host furniture that is **not examination text** and is excluded from
`text_verbatim`:

- a page header and footer on both pages, and a diagonal watermark;
- a boxed advertisement between the rubric and Q1, and a closing advertisement after Q9;
- a **red recurrence table printed under every question**.

Those recurrence tables are the host's own **backward-looking** annotation. They are **not MIW truth**,
they create no family edge, and they must never reach a candidate-facing surface. They are retained
per question in `host_recurrence_hint` as intake evidence only. Twenty such cells were captured:

`2023/FEB/Q1`–`Q9` (the host's self-reference on every question), plus `2016/MAR` and `2021/JULY/Q5`
on Q6, `2022/AUG/Q7` on Q7, and on Q8 the longest chain on the paper — `2017/AUG`, `2019/JAN`,
`2019/APR`, `2019/JULY`, `2019/OCT`, `2020/MAR/Q4`, `2022/JAN/Q4`, `2022/NOV/Q3`.

**None of those sittings is in the MIW solved corpus**, so not one of them is usable as a donor. This
is the systematic under-reporting the playbook §7 rule 3 describes, seen from the other side: the
host's annotation is dense on Q8 and empty on Q3, while MIW's real donor coverage is the exact
opposite.

---

## 2. THE FEBRUARY 2023 TEMPORAL LINE

Established independently for this sitting. **No boundary is inherited from any donor.**

### 2.1 The shape of this sitting

February 2023 is an **early-2023 sitting that falls immediately after two major boundaries and long
before three others.** That combination is what makes it high-risk: the law it must apply is *newer
than the corpus register believes*, and the law a later donor would apply is *not yet made*.

### 2.2 Operative at February 2023

| Instrument | Position at the sitting | Basis |
|---|---|---|
| **Revised MARPOL Annex VI**, `MEPC.328(76)` | **IN FORCE since 1 November 2022** — three months old | resolution's own operative ¶3, read at source. **See §2.3** |
| **EEXI and CII** (regs 23, 25, 28) | **APPLICABLE from 1 January 2023** — six weeks old | Annex VI chapter 4 |
| **SEEMP**, `MEPC.346(78)` 2022 Guidelines | operative; the enhanced SEEMP Part III was required on board **from 1 January 2023** | held resolution |
| CII guideline layer G1–G5 (`MEPC.352(78)`–`MEPC.355(78)`), G3 (`MEPC.338(76)`) | operative | held resolutions |
| **Initial IMO GHG Strategy 2018**, `MEPC.304(72)` | **the operative strategy** | held; recited in `MEPC.328(76)`'s own preamble |
| **32nd Assembly**, adopted December 2021 | **the operative Assembly** — `A.1155(32)` PSC procedures, `A.1157(32)` III Code obligations list | see §2.4 |
| **III Code**, `A.1070(28)` | operative and unamended; mandatory under IMSAS since 1 January 2016 | held resolution |
| **MLC 2006 as amended through the 2018 set** | operative | held base text |
| **ISM Code** as amended through `MSC.353(92)` | operative | held |
| **Merchant Shipping Act, 1958** | **the governing Indian statute** | |
| Salvage Convention 1989 | in force since 14 July 1996 | |
| CLC 1992, Fund 1992, Supplementary Fund 2003, Bunkers 2001, LLMC 1976/1996 | all in force | corpus family log |
| 0.50% m/m sulphur limit | operative since 1 January 2020 | |
| AFS cybutryne controls, `MEPC.331(76)` | **in force 1 January 2023** — six weeks old | |

### 2.3 THE DECISIVE CORPUS DEFECT — `MEPC.328(76)` entry into force

> **The corpus register records `entryIntoForce: "2023-11-01"`. The correct date is
> `1 November 2022`. February 2023 is a sitting that this defect decides the wrong way.**

`true-source/03-imo-instruments/MARPOL-Annex-VI/amendment-register.json` → `baseline` carries:

```
"resolution": "MEPC.328(76)", "adopted": "2021-06-17", "entryIntoForce": "2023-11-01"
```

The resolution's own text is **held in the corpus** at
`_agent-run/local-text/MEPC.328(76).pageindex.json` and was **read at source this session**. Its
operative paragraphs say:

- **¶2** — deemed accepted on **1 May 2022** under MARPOL article 16(2)(f)(iii);
- **¶3** — *"shall enter into force on **1 November 2022**"* under article 16(2)(g)(ii).

**Primary beats the register.** The answer layer uses **1 November 2022**.

**This is `TSCR-3`, already open** — raised by the QP2504 session on 2026-08-13, referenced and left
open by QP2507. It is **carried, not re-raised, and the corpus is not modified.** But QP2302 changes
its status in one respect that must be recorded:

> `TSCR-3` predicted that *"any sitting between 1 November 2022 and 1 November 2023 is decided the
> wrong way by it"*. **QP2302 is the first paper MIW has authored that falls inside that window and
> whose answer depends on the date.** QP2504 and QP2507 referenced the defect without depending on
> it. Here, `Q3` cannot be answered at all without resolving it: a February 2023 sitting reading the
> register would conclude the revised Annex VI was **not yet in force**, and would then have to
> explain EEXI and CII — which the paper states are in force — under a superseded Annex. The
> prediction is now demonstrated, not theoretical. **The producer-team action requested in `TSCR-3`
> is unchanged and remains outstanding.**

A likely mechanism for the defect is recorded as an observation, not a finding: the immediately
following register entry, `MEPC.361(79)`, carries `deemedAccepted: "2023-11-01"`. The baseline's
wrong value is that field's value, one row away.

### 2.4 The Assembly boundary, and the sharpest donor trap on this paper

The **33rd Assembly adopted its resolutions on 6 December 2023 — ten months AFTER this sitting.**
Every `A.11xx(33)` instrument is therefore **future and prohibited**.

This matters concretely and not abstractly, because the corpus's own III Code answers rely on one:

> `QP2510-Q7` (October 2025) — the strongest donor for this paper's Q2 — cites
> **`A.1187(33)`**, the *2023 Non-exhaustive list of obligations under instruments relevant to the
> III Code*, adopted **6 December 2023**, which **revokes `A.1157(32)`**.

At February 2023 that revocation has not happened. **`A.1157(32)`, adopted by the 32nd Assembly in
December 2021, is the operative list.** Carrying the donor's citation across would import an
instrument that did not exist for another ten months. This is recorded here and enforced at §4 Q2.

Likewise PSC procedures are **`A.1155(32)`**, not `A.1185(33)`.

### 2.5 Future at February 2023 — PROHIBITED

| Item | Date | Distance from the sitting |
|---|---|---|
| **2023 IMO GHG Strategy**, `MEPC.377(80)` | adopted 7 July 2023 | **+5 months** |
| **33rd Assembly**, `A.11xx(33)` incl. `A.1185(33)`, `A.1187(33)` | adopted 6 December 2023 | **+10 months** |
| **EU ETS extension to maritime** | from 1 January 2024 | +11 months |
| SOLAS Consolidated Edition 2024 | 1 July 2024 | +17 months |
| MSC 108 resolutions | adopted May 2024, in force 1 January 2026 | +15 months |
| **MLC 2022 amendments** | **in force 23 December 2024** | **+22 months** |
| **Hong Kong Convention** | in force 26 June 2025 | +28 months |
| IMO Net-Zero Framework / GFI | October 2025 | +32 months |
| 34th Assembly `A.12xx(34)` | adopted 3 December 2025 | +34 months |
| **Merchant Shipping Act, 2025** | commenced 15 March 2026 | **+37 months** |

Additionally, and specific to this paper: **the first CII ratings did not exist at this sitting.**
Regulation 28 requires the operational carbon intensity to be determined *after the end of calendar
year 2023*. At February 2023 the first rating year was **six weeks old and running**. No ship had been
rated A to E. Any donor sentence describing ships as *having been rated*, or describing the observed
distribution of ratings, is a later-state statement and is excluded. See §4 Q3.

### 2.6 What changed between January 2023 (`QP2301`) and this sitting

Nothing in the regulatory layer. `QP2301` sat one month earlier under the same Annex VI position, the
same Assembly, the same MS Act and the same MLC set. The one-month gap makes `QP2301` the **safest
same-year reference point on the paper** for any Indian institutional or market framing, because an
earlier answer cannot drag later law backwards. It is used that way at §4 Q8.

---

## 3. DONOR MAP — derived by reading printed stems, not by score

**Derived at this baseline against 297 built questions across 33 papers** — the 31 integrated on
`main` at `124dfbe`, plus `QP2309` and `QP2303` read from their pushed branches. Not read from any
frozen field.

A lexical sweep produced candidates; **every candidate above threshold was then adjudicated by
reading both printed stems in full.** The sweep was seeded with a known positive before any result
was trusted, and the parser was rejected and rewritten once, after it silently mis-assigned the `NB:`
rubric items as questions 1 to 4 — the same failure the extractor makes on this paper.

### 3.1 Per-question derivation

| Q | Subject | Tier | Preferred donor | Sitting | Distance | Class |
|---|---|---|---|---|---|---|
| Q1 | Big Data analytics | B | `QP2503-Q4` | Mar 2025 | +25 mo | **frame-exact, subject-fresh** |
| Q2 | III Code | A | `QP2510-Q7` | Oct 2025 | +32 mo | EXACT stem |
| Q3 | EEXI design measures, CII / AER / EEOI | A | `QP2410-Q8` | Oct 2024 | +20 mo | EXACT stem |
| Q4 | Maritime vs contractual salvage, LOF, award | C | `QP2408-Q7` | Aug 2024 | +18 mo | family — partial overlap |
| Q5 | ISM effective communication, ERM | C | `QP2312-Q4` | Dec 2023 | +10 mo | family |
| Q6 | Bill of Lading — function, *to order*, contract | C | `QP2403-Q2` | Mar 2024 | +13 mo | family — different limbs |
| Q7 | High-efficiency propellers | A | `QP2510-Q4` | Oct 2025 | +32 mo | EXACT stem |
| Q8 | MLC 2006 — four limbs | C | `QP2407-Q6` | Jul 2024 | +17 mo | family — **no exact donor exists** |
| Q9 | CLC'92 against Bunkers 2001 | B | **`QP2304-Q7`** | **Apr 2023** | **+2 mo** | near — reversed framing |

**9 of 9 are donor-connected. 3 exact, 2 near, 4 family. No question on this paper is fresh
research, and no Tier D is manufactured.**

This is a better position than the allocation's §4 estimate of `3 exact / 3 family / 6 of 9`, and the
improvement is almost entirely `QP2304-Q7` arriving at `+2 months` on Q9.

### 3.2 Same-year relations

Only one same-year donor exists for this paper, and it is the most valuable relation on it:

- **`QP2304-Q7` (April 2023, `+2 months`) → `Q9`.** The shortest donor distance anywhere in Batch 4.
  Both sittings stand under the identical liability architecture, and the two months carry no
  regulatory movement whatever. Its **evidential discipline is inherited in full** — see §5.

`QP2301-Q3` (January 2023, `−1 month`) is a **backward-running** same-year reference, not a donor. It
donates nothing structurally, but it fixes the Indian statutory and institutional frame at a date one
month *before* this sitting, which no later donor can do. Used at Q8 for the Indian layer only.

### 3.3 What THIS paper will donate — recorded for Batch 5

Two of this paper's questions are **printed identically** on later-2023 papers that are still
unsolved. Building QP2302 creates their first same-year donors:

| This paper | Recurs as | Relation |
|---|---|---|
| **`QP2302-Q2`** III Code | **`QP2308-Q9`** (August 2023, `+6 mo`) | **character-identical stem** |
| **`QP2302-Q8`** MLC four limbs | **`QP2307-Q4`** (July 2023, `+5 mo`) | identical but for the `Compliant`/`Complaint` misprint, which QP2307 prints correctly |

Both were established by reading the printed stems of the August and July papers, not from the host
annotation. This is the concrete production reason QP2302 was kept as the next target — see §6.

### 3.4 Rejected donors — recorded so the rejection is auditable

| Candidate | Score | Rejected because |
|---|---|---|
| `QP2404-Q1` (IoT) for Q1 | 0.35 | Same printed frame, but the technology is different. Reused as **frame**, not as donor; `QP2503-Q4` is the closer frame instance and is preferred |
| `QP2406-Q6` (MLC) for Q8 | 0.26 | Four limbs, but **four different limbs** — minimum requirements, conditions of employment, compliance, abandonment. Not this question |
| `QP2412-Q9`, `QP2403-Q7` for Q2 | 0.88 each | Genuine exact siblings of `QP2510-Q7`; only one preferred donor is carried and the other two are recorded as corroborating instances |
| `QP2403-Q4` for Q7 | 0.88 | Tied with `QP2510-Q4`; the October 2025 instance is preferred because its record is the more recent and more complete |
| `QP2409-Q6`, `QP2402-Q2` for Q9 | 0.11 lexical, high topical | Real siblings, but **both are further away in time than `QP2304-Q7`** and both frame the question from the Bunker side. Read and used as cross-checks only |
| `QP2510-Q2` for Q6 | 0.09 | Bill of Lading, but the limbs are *define / distinguish types / obligations*. This paper asks *main function / why 'to order' / when the B/L becomes the contract*. Family, not donor |

---

## 4. LATER-STATE REVERSALS — question by question

**No donor statement is inherited.** Every sitting-relative statement is re-derived from the February
2023 position. This section records what had to be reversed.

### Q2 — the sharpest reversal on the paper

`QP2510-Q7` sits **thirty-two months later** and cites **`A.1187(33)`** for the list of instruments
the Code covers. That resolution was adopted **6 December 2023, ten months after this sitting**, and
it revokes the instrument that *was* operative. **Reversed to `A.1157(32)`** (32nd Assembly, December
2021). The III Code itself, `A.1070(28)`, is unamended between the two sittings and transfers
without qualification. The donor's paragraph-level reading of the annex — objective at ¶1, strategy at
¶3, subject areas at ¶6, KPIs at ¶42–44, coastal State at ¶45–51, port State at ¶52–63 — is structural
and carries across intact.

### Q3 — three separate reversals, and the paper's hardest question

1. **The corpus register date must be reversed** before the question can be answered at all. §2.3.
2. **The donor sits after the first rating cycle; this sitting sits inside the first rating year.**
   `QP2410-Q8` (October 2024) can describe ships as rated, and can describe the regulation 28.2
   deadline as passed. At February 2023 **no ship had a CII rating** and the first rating year was six
   weeks old. Every such statement is re-authored forward-looking.
3. **The printed parenthesis is substantively wrong, not merely misprinted.** `Phase 2 ( f 20% - 30%
   reduction)` conflates two different schemes: the **phased** Phase 0/1/2/3 structure belongs to the
   *required EEDI* table (reg 24, Table 1) for new ships, while **EEXI** takes its required reduction
   factor from reg 25 Table 3, which is banded by ship type and size and is **not phased**. The answer
   states the framing as printed, then distinguishes the two schemes, because a candidate who simply
   adopts the printed framing will describe the wrong table. The stray `f` is preserved separately as
   a typographic anomaly at §1.4; **this is the substantive defect underneath it.**

Additionally, `MEPC.395(82)` — the SEEMP guideline edition whose date `QP2410-Q8` could not resolve —
is **October 2024 and simply future here**, so that donor's unresolved item does not arise. The
operative SEEMP guidelines are `MEPC.346(78)`.

### Q8 — the misprint that changes what is being asked

The stem prints **`On-board & On-shore Compliant Procedures`**. The word is **`Complaint`**. MLC 2006
regulation 5.1.5 provides **on-board complaint procedures** and regulation 5.2.2 **onshore seafarer
complaint-handling procedures**; there is no MLC instrument called a *compliant procedure*. The
misprint is preserved in `text_verbatim` and the answer names the correct term once, explains that the
paper prints it otherwise, and then answers the question that MLC actually contains. **Answering a
"compliant procedure" would be answering nothing.**

The temporal reversal on this question is the **MLC 2022 amendments**, adopted at the 110th
International Labour Conference in 2022 and **in force 23 December 2024 — twenty-two months after this
sitting.** They are **adopted but not in force** here, and the distinction is stated in those words.
Any later donor's account of the amended Code — in particular anything about repatriation, the
seafarer death-notification provisions, or the amended Code A/B guidance — is excluded.

Limb (d), **grievance redressal for Indian seafarers**, has no donor anywhere in the corpus and no
held Indian source beyond the Merchant Shipping Act, 1958 frame. It is answered to the **statutory and
institutional architecture** — the flag State's obligation under Title 5, the shipping-master and
Directorate route, and the on-board-then-onshore escalation the Convention itself requires — and **no
circular number, no office name and no forum name is asserted**. This is recorded as an evidence gap
at §5.2, not concealed.

### Q9

`QP2304-Q7` is **two months later** and stands under an identical architecture; there is nothing to
reverse. Its record is nevertheless audited line by line, and one thing is *not* carried: the donor
cites the **CLC 1992 limits as raised by the 2000 amendments**. Those took effect in 2003 and were
therefore operative twenty years before this sitting, so the *fact* is safe — but the **figures are
not asserted here** for the reason at §5.2, and the donor's own `unresolved` list makes the same
choice. The reversal of framing is the real work: the donor asks *describe Bunkers and say how it
differs from CLC*; this paper asks *compare CLC and Bunkers* across four named heads. The answer is
rebuilt on the four printed heads and not on the donor's seven-step route.

### Q7

`QP2510-Q4` is thirty-two months later, but hydrodynamics is not dated. The only temporal content is
the regulatory framing — *why* propeller efficiency is being pursued — and that is re-derived: at
February 2023 the driver is **EEXI compliance six weeks old and the CII rating year just begun**, under
the **Initial GHG Strategy of 2018**, not the 2023 Strategy. `Cortra` is answered as **contra-rotating**.

### Q1

The frame recurs exactly; the technology does not. `QP2503-Q4` supplies the printed frame and the
five-part shape a *technology* question in this family takes, and **nothing else**. Big Data is
authored fresh. The temporal content is limb (a)'s *"upcoming regulations"*, which is re-anchored: at
February 2023 the regulations that are *upcoming* are the **CII rating cycle whose first year has just
begun** and the **DCS reporting stream feeding it** — not the EU ETS, not the 2023 Strategy, not the
Net-Zero Framework, all of which a later donor would reach for.

### Q4, Q5, Q6

Doctrinal questions whose governing instruments — the Salvage Convention 1989, the ISM Code as amended
through `MSC.353(92)`, and the Hague/Hague-Visby carriage regime with the Indian Bills of Lading and
Carriage of Goods by Sea legislation — did not move between these sittings and their donors. **LOF is
answered as LOF 2020**, the current form at this sitting, with the point that the arbitration and
`SCOPIC` machinery, not the form's year, is what the question is about. No case authority is cited
anywhere, because none is held.

---

## 5. CORPUS USE

**Corpus commit consumed: `319524c24d11b2f89f33672c384b56e9ae1ab7db`.** Read-only. Nothing was edited.

This is **not** the playbook §16 baseline commit `64977b8`. That pin was written for the 2024 batch;
the 2023 batch has consumed current corpus `main` since QP2312, and QP2303 recorded the same value.
The divergence is recorded rather than silently taken.

### 5.1 What was consumed

| Question | Corpus object | Level |
|---|---|---|
| Q3 | `MEPC.328(76)` resolution text, operative ¶2 and ¶3, read at source | **P1 primary verified** |
| Q3 | `MARPOL-Annex-VI` canonical regulation records — regs 22–28 | P1 |
| Q3 | `MEPC.346(78)` 2022 SEEMP Guidelines | P1 |
| Q2 | `A.1070(28)` III Code — via the MIW verification record that read it in full | internal reuse verified |
| Q8 | MLC 2006 base text, held at `04-ilo-instruments/MLC-2006/_base-and-amendments/mlc-2006.pdf` | P1 |
| Q8 | MLC 2022 amendments, held — read **only** to fix the in-force date | P1 |
| Q5 | ISM Code, held at `03-imo-instruments/ISM-Code/` | P1 |
| Q9 | `05-un-and-treaty-law/liability-and-compensation/INSTRUMENT_LOG.md` | **status facts only** |

### 5.2 Evidence gaps — recorded, not filled by invention

1. **No CLC 1992 or Bunkers 2001 treaty text is held.** The corpus classifies this whole family as
   *citation and index only, with verified status facts*, and its own log says numeric SDR limits are
   *"deliberately NOT asserted"*. Q9 nevertheless prints **"limits of liability"** as one of four
   required heads. It is answered to the **structure** of limitation — that CLC carries its own
   tonnage-banded limit and a compulsory-insurance certificate, while **Bunkers sets no limit of its
   own and refers out** to the applicable national or international regime, in practice LLMC — and
   **no SDR figure, no tonnage band and no currency conversion appears anywhere in the answer.**
   Carried as `B_CURRENCY_CHECK` in `reverify_before_publication`.
2. **No LOF form text is held.** The form is named and its machinery described by substance. **No
   clause is quoted and no clause number is asserted.**
3. **No Indian grievance-redressal instrument is held** beyond the Merchant Shipping Act, 1958 frame.
   Q8(d) is answered to architecture. **No DG Shipping circular number is asserted.**
4. **No bill of lading form or carriage-convention text is held.** Q6 is answered on the settled
   doctrine and the Indian statutory frame, and **no article of the Hague-Visby Rules is asserted by
   number**.
5. **No casualty report is held.** Q5 requires *two examples of near misses or accidents*. They are
   given as **constructed, clearly-labelled illustrative scenarios of the recognised failure classes**,
   not as named real casualties, because no held source supports a named account. This is stated in
   the answer itself so a candidate does not cite them as reported cases.

### 5.3 Referrals carried, not consumed

- **`TSCR-3`** — `MEPC.328(76)` entry into force recorded a year late. **Carried. Status OPEN and
  unchanged.** See §2.3, which records that QP2302 is the first paper to depend on it.

---

## 6. SUMMARY OF THE ANCHOR

1. Baseline refreshed to `124dfbe` because `7019445` integrated QP2304, which gives Q9 a `+2 month`
   donor where the nearest was previously `+12`.
2. **Nine printed questions**, established by reading both rendered pages. Numbering is `Q1 Q2 Q3 4.
   5. Q6 Q7 Q8 Q9` and is preserved.
3. **No marks are printed anywhere.** 16 per question is derived from the rubric and the derivation is
   recorded.
4. Fifteen printed anomalies preserved. The consequential one is Q8's **`Compliant`** for
   **`Complaint`**.
5. **`MEPC.328(76)` entered into force 1 November 2022**, three months before this sitting, on the
   resolution's own operative ¶3. The corpus register's `2023-11-01` is wrong and QP2302 is the first
   paper whose answer depends on the correction. `TSCR-3` carried, corpus untouched.
6. **`A.1157(32)`, not `A.1187(33)`.** The 33rd Assembly is ten months future.
7. **No ship held a CII rating at this sitting.**
8. **MLC 2022 amendments are adopted but not in force** — twenty-two months future.
9. **9 of 9 donor-connected**: 3 exact, 2 near, 4 family. No Tier D manufactured.
10. Building this paper creates the first same-year donors for `QP2308-Q9` and `QP2307-Q4`.

---

## 7. FINALISED AT AUTHORING

*Completed after the nine answers were written, the canonical spec was assembled and the full governed QA
suite had run. Sections 0 to 6 are unchanged: nothing in them was contradicted by authoring. What follows is
what authoring added, and it is deliberately confined to genuinely new findings.*

### 7.1 The donor map held. Nothing in §3 was revised

All nine relations stood as adjudicated. **9 of 9 donor-connected: 3 exact, 2 near, 4 family**, unchanged. No
donor was demoted, no new donor was found, and the rejected candidates at §3.4 stayed rejected. The one thing
worth recording is that the two questions with the weakest donor support — Q8, where no exact donor exists, and
Q6, whose whole limb (b) has no donor at all — produced the two largest objects on the paper, which is the
expected shape and is recorded rather than treated as an anomaly.

### 7.2 Q7's donor audit ran the OPPOSITE way from every other audit in the batch

This is the finding of most general value and it was not predicted at §3.

Both exact instances of the propeller stem — `QP2510-Q4` and `QP2403-Q4` — carry an **empty `regulations` list**,
and each records expressly that MARPOL Annex VI was not read in a licensed consolidated edition, so that **no
regulation number and no date for EEXI or CII is asserted anywhere in either record**. The standing assumption
behind a temporal audit is that a later donor *over*-claims and must be stripped back. Here both donors
**under**-claim.

That restraint was correct on the evidence those sessions held. **It does not bind this paper**, because this
paper holds the primary material for a *different* question: Q3 reads `MEPC.328(76)` at source for its operative
paragraphs and the paper consumes the corpus's canonical Annex VI regulation records for regulations 22 to 28
(§5.1). Q7's regulatory framing is therefore **stated at P1 provenance** where the donors stated nothing.

> **The reusable rule: an audit must ask whether the donor says too little as well as whether it says too much,
> and a donor's evidence limitation is a fact about that session, not a property of the question.**

### 7.3 Q6 — the Indian statute book itself moved, and the contamination risk was not in the preferred donor

Anticipated in outline at §4 but sharper in fact. The **preferred** donor `QP2403-Q2` (March 2024) stands under
the *same* statute book as this sitting and transfers without reversal. The danger is the *second* family
instance `QP2510-Q2` (October 2025), which answers **entirely** on the **Bills of Lading Act 2025** and the
**Carriage of Goods by Sea Act 2025**, both in force 10 September 2025 — **thirty-one months future here**. Its
whole statutory layer is excluded.

**This is the only question in the 2023 batch to date on which the Indian statute book itself was replaced
between the sitting and a corpus donor**, and it is the reason §5.2 item 4's prohibition is substantive rather
than formal: the two donors cite the same provisions under **two different numbering schemes**, because the 2025
re-enactment renumbers. No held source fixes the numbering a February 2023 candidate would have found, so no
Hague-Visby article or rule is asserted by number anywhere in Q6.

### 7.4 Q8 — the `Compliant` reading was confirmed from outside this paper

§4 read the misprint as `Complaint` from the structure of MLC 2006. Authoring confirmed it independently: the
printed stem of **`QP2307-Q4` (July 2023, +5 months) prints the same question with the word spelled correctly**.
That stem was read for the confirmation only; nothing else was taken from it, and QP2307 remains unsolved.

Two smaller Q8 findings:

- The **margin** to the MLC 2022 amendments is the delta from the donor, and it changes the *confidence* rather
  than the conclusion. `QP2407-Q6` excludes them at five months and `QP2410` at two; **here the margin is
  twenty-two months**, before the amendments had completed their acceptance period, so the question whether an
  early-adopting flag might have anticipated them does not arise.
- **`known_traps.md` Entry 6 was applied INVERTED**, exactly as for QP2304: the administration at this sitting is
  the **Directorate General of Shipping**, and the renamed body appears only as the excluded future position.
  §5.2 item 3's prohibition on naming an office was applied as barring **named cells, offices and forums**, while
  the administration and the shipping master — the architecture §4 itself names — are named. That reading is
  recorded here so the next MLC question applies the same one.

### 7.5 Q9 — the exclusion of the CLC figures is an EVIDENCE decision, not a temporal one

§5.2 item 1 is honoured in full: no SDR figure, no tonnage band, no limitation amount, no fund ceiling and no
currency conversion appears anywhere in Q9, notwithstanding that the printed stem names *limits of liability* as
a required head. The head is answered to the **structure** of limitation.

The distinction that authoring adds, and that a later reader could easily get wrong: **the donor's CLC figures
are temporally perfectly safe.** They derive from the 2000 amendments, in force since 2003 — twenty years before
this sitting. They are excluded because **neither treaty text is held**, not because they are out of date. The
classification is recorded in Q9's `reverify_before_publication` as `B_CURRENCY_CHECK`, and the question whether
figures may be restored if the treaties are ever acquired is left to the Founder rather than decided here.

Q9 also returned **zero temporal-sweep candidates**, the only question on the paper to do so, which is consistent
with its LOW risk rather than with an omission.

### 7.6 A paper-wide defect was found by the governed validator and repaired across all nine questions

**This is the most important process finding of the session and it is recorded in full because it is not
flattering.**

The five questions completed in the previous session were validated against the **QP2303 field-name schema**, per
the helper reproduced at CHECKPOINT §4. That helper compares **key names only**. When `validate_spec.py` — the
governed validator — was first run on the assembled paper it returned **363 errors**, and they were distributed
across **all nine questions**, 30 to 38 on each of Q1 to Q5 and 43 to 53 on each of Q6 to Q9. The defect was
therefore **not** introduced by the resuming session; it was latent in the completed work and was inherited.

What was wrong, and what was done:

| Defect | Scope | Repair |
|---|---|---|
| `primary_category` outside the seven topic-tree categories | all 9 | mapped to the tree, each against a donor precedent |
| `answer_route.archetype` outside the closed set | Q1, Q3, Q5 | `technology`, `technical_regulatory`, `management` → `explain` |
| `retrieval_cards[].type` outside the closed set | 101 cards | mapped to the seven permitted types |
| `reverify_before_publication[].class` outside the closed set | 24 flags | `A_TEMPORAL_ANCHOR`, `A_REGULATORY_CORRECTION`, `B_DATE_CHECK` → `B_CURRENCY_CHECK`; `C_EVIDENCE_GAP`, `D_PRESENTATION` → `C_ACCEPTED_LIMITATION` |
| model-answer principal headings not identical to the route steps | 96 headings, 48 steps | route titles adopted **from** the answer headings, so no wording was lost; 44 sub-headings demoted out of the principal sequence; one closing route step added to each of Q8 and Q9 |
| `memory_cue` enumerating anchors without mapping them to route step numbers | 5 questions | a numbered route line prepended |
| the six canonical study-guide sections and the `Uncertainty` section absent | all 9 | **63 sections authored**, preserving every existing question-specific section |
| `verification_file` missing on disk | all 9 | the nine records written |

**No answer content was weakened, thinned or deleted to satisfy the validator.** The heading repair adopted the
richer model-answer wording as the route title rather than truncating the answer to the route, and the study-guide
repair added sections alongside the existing analysis rather than replacing it.

> **The reusable rule: the CHECKPOINT §4 helper proves the field NAMES, not the governed contract.
> `validate_spec.py` must be run before a paper is called complete, and a resuming session must run it against
> the inherited questions and not only its own.**

An **`A_` reverify class was deliberately not used anywhere on this paper.** `A_BLOCKING` means the claim blocks
publication. `TSCR-3` is carried, not re-raised, and the paper ships as Founder-Review Ready, so the temporal
anchors are currency checks and are classed `B_CURRENCY_CHECK`.

### 7.7 One health-check gate failure, and the phrasing gap behind it

`solvedqp_health_check.py` failed once, on Q6, reporting that the answer asserted the **Merchant Shipping Act,
2025** as operative. The assertion was not being made — the cell reads `DOES NOT EXIST - commenced 15 March
2026` — but the checker's `NEGATION_CUES` list contains `is not`, `was not`, `did not` and `has not` and **does
not contain `does not`**, and its sentence window straddles a table row. The exclusion was rephrased to carry the
recognised cue *after this sitting*, which is also the plainer wording. **The checker was not weakened**; the
answer was made unambiguous to it. The cue-list gap is recorded here as an observation for the producer team, not
raised as a correction request.

### 7.8 QA outcome

`validate_spec` **0 errors** on all 32 specs · deterministic **byte-identical double build**
(`6d7548f57d725cd2`) · `audit_paper` **pass** on all 32 · `known_traps_check`, `recurrence_check`,
`temporal_sweep`, `health_check`, `solvedqp_health_check` **pass** · positive controls **pass** ·
`surface_impact` **no non-target public, paid or commercial surface moved**.

**Those results were measured with the global derived artefacts regenerated, and every one of them was then
reverted before staging** (playbook §13.2). With the globals reverted to their committed state,
`audit_paper` reports exactly one residual error on this branch — *manifest has no entry for QP2302* — which is
the expected founder-review-branch condition and is the same state `QP2303` and `QP2309` shipped in: neither
appears in the manifest either. It closes at integration, with §7.10 item 1.

The **temporal sweep returned 118 candidates**, every one of which was adjudicated: each is either a date this
paper deliberately **excludes** (the 2025 Indian Acts, the MS Act 2025, the MLC 2022 amendments, the 2023 GHG
Strategy, the EU ETS, the 33rd Assembly, the Net-Zero Framework), the corpus register value **being corrected**
(`2023-11-01`), or a donor sitting named in authoring metadata. **None asserts post-sitting law as operative.**
`PIL FLAGS; CLAUDE ADJUDICATES` was applied per candidate.

UI reviewed over HTTP at **1280 and 375** with explicit server teardown, Node being absent: nine question
anchors resolve, **Answer is the default pane**, all **five modes** (`understand`, `plan`, `answer`, `guide`,
`recall`) render for all nine questions, search isolates correctly (`Compliant` → Q8 only, `contra-rotating` →
Q7 only), **24 cross-links and 20 internal links all resolve**, **no horizontal overflow at either width**, **no
console output**, and **all eight printed anomalies render exactly as printed**. **No host recurrence annotation
reaches either surface**, and the delivery page carries **zero** production-metadata, host-branding or path
tokens.

### 7.9 What this paper now donates — unchanged from §3.3, and confirmed at authoring

- **`QP2302-Q2`** → **`QP2308-Q9`** (August 2023, +6 months), character-identical stem.
- **`QP2302-Q8`** → **`QP2307-Q4`** (July 2023, +5 months), identical but for the `Compliant`/`Complaint`
  misprint, which QP2307 prints correctly — now confirmed by reading QP2307's printed stem.

**That future reuse influenced no wording here. Printed QP2302 truth remains the authority for these objects.**

### 7.10 Open for the Founder

1. **The delivery page and the manifest entry are deliberately NOT committed on this branch**, following the
   `QP2303` and `QP2309` precedent: neither appears in the manifest and neither committed `solvedQP/QP####.html`.
   The paper is therefore **not advertised as Available** and nothing 404s. The QA protocol §6 publication gate
   applies at **integration**, and the integration session must generate and explicitly stage
   `solvedQP/QP2302.html` together with the manifest entry.
2. **`TSCR-3` remains OPEN and the producer-team action is unchanged.** QP2302 is the first paper whose answer
   *depends* on the correction; the corpus was not modified.
3. **Whether the CLC and Bunkers figures may be restored to Q9** if either treaty text is ever acquired — see
   §7.5.
4. **Whether Hague-Visby article numbering may be restored to Q6** if the 1925 Act's Schedule is ever acquired —
   see §7.3.
</content>
</invoke>
