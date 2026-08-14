# QP2303 — MARCH 2023 — TEMPORAL AND DONOR ANCHOR

**Paper:** QP2303 · March 2023 · printed serial `2303 EM` · MEO Class I · Engineering Management
**Branch:** `pastpapers/qp2303-founder-review`
**Built from:** `d6d95e8dbb51ba03fd8eaded864c79427a22cbba` (`origin/main` at session start)
**Corpus commit consumed:** `319524c24d11b2f89f33672c384b56e9ae1ab7db` (`RulesApp-Local-Input` `origin/main`, tracked tree clean)
**Written before canonical assembly**, as the protocol requires. Nothing in Q1–Q9 was authored until this file existed.

---

## 0. BASELINE DECISION — why this branch is on `d6d95e8` and not on `bf5b533`

Batch 4's recorded baseline is `57b9342` (`DESKTOP_QP_ALLOCATION_2023.md` §0.1). No paper in this
batch has used it unchanged since QP2301. The standing rule, established by QP2309 §0, is to retain
the fixed batch baseline **unless newly integrated paper content changes donor truth**. That
condition is met again here.

Between QP2309 and this session `origin/main` advanced by two commits:

| Commit | What it did |
|---|---|
| `7da7daa` | Locked the Solved QP home as a projection and gated delivery on Git. **No learning content changed** |
| `d6d95e8` | **Integrated QP2312 (December 2023) onto `main`** — 30 papers, 270 questions |

`d6d95e8` is new integrated paper content, and it matters to this paper specifically:

1. **QP2312 is a same-year donor.** December 2023 is now on `main`. Two of its questions bear on
   this paper — `QP2312-Q3` (types of loss in marine insurance, York-Antwerp) reaches Q3, and
   `QP2312-Q2` (PSC legal framework and appeal against detention) reaches Q7. A branch cut from
   `bf5b533` cannot see either.
2. **The laptop changed QP2312 at integration.** `origin/main:specs/QP2312.json` is blob
   `30a3995`; the pushed branch tip is blob `584909d`. **They are not the same file.** A branch cut
   before `d6d95e8` would read the desktop's pre-review QP2312 as donor truth and would miss every
   correction the laptop made. This is the decisive reason, and it generalises: *an integrated
   paper and its review branch are different documents, and only the integrated one is truth.*
3. **`bf5b533`'s QP2301 corrections are inherited either way**, since `d6d95e8` descends from it.

Integration is unaffected — the laptop integrates desktop branches by path extraction and never by
merge — so this choice costs nothing at integration and buys correct donor visibility.

**Branch point proved before any file was written:**
`HEAD` = `merge-base(HEAD, origin/main)` = `origin/main` = `d6d95e8`.
No review branch is an ancestor of `HEAD`; this paper is not built on QP2309 or on any other
paper branch.

### Donors that are pushed but NOT integrated

**QP2304** (April 2023) and **QP2309** (September 2023) are on their own remote branches and are
**not** on `main`. They were read as donor candidates because they are same-year and same-batch,
and every use of them below is labelled **FOUNDER-REVIEW-PENDING**. No claim in this paper rests on
an unintegrated paper alone.

---

## 1. SOURCE RECONCILIATION

| Checked | Result |
|---|---|
| Local file | `meoclass1/pastpapers/docs/MARCH 2023.pdf` — git-ignored, never committed |
| SHA-256 | `05089dbf046714fef6d9c2c79b662c07b5c5e87f07c254611beb44dd3a303c55` |
| Printed month/year | **MARCH 2023** — matches the intended sitting |
| Printed serial | **`2303 EM`** — number first, no `Sr. No.` prefix, the reversed 2023 convention of allocation §1.1 |
| Printed authority | `EXAMINATION OF MARINE ENGINEER OFFICER` |
| Function | `Marine Engineering Management at Management Level` |
| Subject | `ENGINEERING MANAGEMENT` |
| Class | `M.E.O CLASS – I` |
| Time / marks | `TIME ALLOWED - 3 HOURS`, `Total Marks – 100` |
| Region note | `(India 2023)` |
| Pages | **2** |
| Questions | **9**, established by reading — see §1.1 |
| Wrong-edition check | **Passed.** The serial `2303` is unique in the batch and consistent with MARCH; no reprint of another sitting |

### 1.1 The question count was established by reading, not by the extractor

Both pages were extracted from the born-digital text layer with PyMuPDF **and then rendered as
images at 170 dpi and read in full**, and the two were reconciled character by character. They
agree.

March 2023 prints **`Q1.` through `Q9.` uniformly** — every question carries the `Q` prefix and a
following period. **QP2303 therefore does NOT carry the numbering anomaly that allocation §1.3
records for January and February.** That anomaly is real, and it was re-confirmed in this session
against `FEBRUARY 2023.pdf` for the recomputation in §7 — February genuinely prints bare `4.` and
`5.` — but it does not touch this paper. A pattern-count extractor under-reads February; it reads
March correctly. The manual count is nevertheless the authority, and the manual count is **nine**.

### 1.2 Marks and subparts, as printed

**Marks are largely unprinted on this paper.** This is itself the paper's most significant printed
characteristic and is recorded rather than repaired.

| Q | Limbs as printed | Marks as printed | Printed total |
|---|---|---|---|
| Q1 | `A.` `B.` | none | — |
| Q2 | none (continuous prose) | none | — |
| Q3 | none (two paragraphs) | none | — |
| Q4 | `A.` `B.` | **`(8)` on A only; B unmarked** | 8 |
| Q5 | `A.` `B).` | none | — |
| Q6 | `(a)` `(b)` | `(8)` `(8)` | 16 |
| Q7 | `a)` `b)` | `(8)` `(8)` | 16 |
| Q8 | `a)` `b)` | none | — |
| Q9 | `A)` `B)` `C)` `D)` | none | — |

Only **Q6 and Q7** print a complete 16. **Q4 prints 8 against two limbs** — limb A carries `(8)`
and limb B carries nothing. Six questions print no marks at all.

`total_marks` is therefore carried as **16 per question by rubric, not by print**: instruction 2
states all questions carry equal marks, six answered questions are required, and the paper prints
`Total Marks – 100`. Six equal questions against 100 gives 16.67, and every question in the corpus
that does print a figure prints `(16)`. The derived 16 is recorded as derived, and the printed
absence is recorded as printed absence. **Six answered questions at 16 total 96 against a printed
100** — the same arithmetic discrepancy carried by every paper in this batch, printed on the source
and reproduced rather than corrected.

**The limb labelling is inconsistent across the paper** — `A./B.`, `A./B).`, `(a)/(b)`, `a)/b)`,
`A)/B)/C)/D)` all appear. Each question's own printed form is preserved in `subparts[].ref`.

### 1.3 Printed anomalies — preserved, never corrected

The house rule is unchanged: printed errors are preserved and recorded. A candidate sitting this
paper saw exactly this.

| Where | What is printed | Adjudication |
|---|---|---|
| Q2 | *"short term, mid-term and long **tern** goals"* | Typo for "long term". **Preserved.** |
| Q1 B | *"In each case elaborate **one** who is responsible for payment"* | "one" for "on". **Preserved.** |
| Q4 | Limb A carries `(8)`; limb B carries **no marks** | Asymmetric mark print. **Preserved**; see §1.2 |
| Q4 A | *"vis-a-vis"* unaccented, and the limb ends `measures; (8)` | **Preserved** |
| Q5 | Limb labels run `A.` then **`B).`** — bracket and period together | **Preserved** |
| Q6 (a) | *"It is common statement that **'**80% of accidents are caused due to human errors,"* — the opening single quote is **never closed** | Unbalanced quotation. **Preserved.** The donor `QP2411-Q8` prints this correctly closed as *'…human error.'* — a real printed divergence, not a transcription slip |
| Q6 (a) | *"It is common statement"* — no article | **Preserved** |
| Q6 (a) | *"referred to here **of** a complex hierarchical socio-technical system"* | Governs awkwardly. **Preserved** |
| Q7 b) | *"difference between 'corrective action' and **'**preventive action."* — opening quote unclosed, and the interrogative ends in a full stop | **Preserved** |
| Q9 | *"employed for the **condition** of L.O"* | The donor `QP2406-Q9` prints *"condition **analysis** of L.O"*. A genuine one-word divergence between two otherwise identical stems. **Preserved**, and recorded as the question delta in §3.1 |

### 1.4 Editorial and host insertions — identified and excluded

The source copy is a third-party scan and carries host furniture that is **not examination text**
and appears nowhere in the spec:

- a page watermark and a running header/footer;
- a promotional box offering an app and books;
- a closing promotional paragraph;
- **red recurrence-hint tables under every question** (`2015/AUG`, `2021/APR/Q2`, `2023/MAR/Q1` …).

Those tables are the host's own recurrence annotation. Per playbook §7.3 they are **directional —
they point backwards only** — and they are **not MIW truth**. They are recorded in
`host_recurrence_hint` as intake evidence and **must never reach a candidate-facing surface**. They
were used in this session only as a discovery prompt, never as a donor claim. Two are worth noting
as intake evidence and nothing more:

- Q2's table carries `2023/FEB/Q2`. February 2023 Q2 is in fact the **III Code** question, not a
  decarbonisation question. **The host hint is wrong**, and it is rejected on the printed stems.
- Q1's table carries `2022/OCT/Q9` and Q9's carries `2022/MAR/Q2`. Those sittings are **not in the
  MIW solved corpus** and cannot be donors regardless.

---

## 2. THE MARCH 2023 TEMPORAL LINE

March 2023 is the **third month of the batch year** and sits in the most tightly bounded position of
any paper allocated so far.

### 2.1 The boundaries that define this sitting

| Boundary | Date | Side March 2023 falls on |
|---|---|---|
| EEXI and CII requirements apply | **1 January 2023** | **AFTER** — operative, by ten weeks |
| Cybutryne (AFS) controls apply | **1 January 2023** | **AFTER** — operative |
| **2023 IMO GHG Strategy** (MEPC 80) | **7 July 2023** | **BEFORE** — future |
| **33rd IMO Assembly** | **6 December 2023** | **BEFORE** — future |
| MLC 2022 amendments in force | 23 December 2024 | **BEFORE** — future |
| EU ETS extended to maritime | 1 January 2024 | **BEFORE** — future |
| Hong Kong Convention in force | 26 June 2025 | **BEFORE** — future |
| Merchant Shipping Act, 2025 commenced | 15 March 2026 | **BEFORE** — future by three years |

**There is no day-granularity problem on this paper.** Unlike July 2023, none of the boundaries above
falls inside March 2023, so every one of them is resolvable from the month alone. The paper prints
`MARCH 2023` and no day, and no claim in this paper depends on the day. Trap 17 is satisfied by
construction, not by argument.

### 2.2 Operative at March 2023

- **Merchant Shipping Act, 1958.** The standing statute trap for the whole batch.
- **Initial IMO Strategy on reduction of GHG emissions from ships — `MEPC.304(72)`, 2018.** This is
  the operative IMO policy instrument on decarbonisation at the sitting, and it decides Q2.
- **32nd IMO Assembly** (December 2021). `A.1155(32)` is the operative PSC procedures resolution.
- **MARPOL Annex VI as revised by `MEPC.328(76)`** — see §2.3, which corrects the corpus on this.
- **`MEPC.346(78)`** 2022 SEEMP development guidelines — operative. **`MEPC.395(82)` (2024) is
  future** and must not be cited.
- **CII guideline set `G1`–`G5`** — `MEPC.352(78)`, `MEPC.353(78)`, `MEPC.338(76)`, `MEPC.354(78)`,
  `MEPC.355(78)`. All 2021–2022; all sitting-correct.
- **ISM Code** as amended through `MSC.353(92)`.
- **RO Code** — `MSC.349(92)` + `MEPC.237(65)`, mandatory since 1 January 2015.
- **UNCLOS 1982**, unamended.
- **CLC 1992, FUND 1992 and the Supplementary Fund Protocol 2003** — all in force.
- **NOx Technical Code 2008**; MARPOL Annex VI regulation 13 Tier I/II/III.
- 0.50 % m/m global sulphur limit.

### 2.3 A corpus defect found at source — MEPC.328(76) entry into force

**This is a `TRUE_SOURCE_CORRECTION_REQUEST` and it is raised, not applied.** QP production never
edits True Source.

`true-source/03-imo-instruments/MARPOL-Annex-VI/amendment-register.json` records the baseline as:

```
"resolution": "MEPC.328(76)", "adopted": "2021-06-17", "entryIntoForce": "2023-11-01"
```

That register's own `authorityNote` states that adoption and entry-into-force facts are *read from
each resolution's own operative paragraphs*. **They were not, in this record.** The held resolution
PDF was opened and its operative paragraphs read directly in this session:

- operative paragraph **2** determines the amendments *"shall be deemed to have been accepted on
  **1 May 2022**"*;
- operative paragraph **3** invites Parties to note that they *"shall enter into force on
  **1 November 2022**"*.

The register is wrong by **one year**. The correct entry into force is **1 November 2022**.

**Why this had to be settled before authoring.** Taken at face value the register would place the
Revised Annex VI *eight months after this sitting*, which would make EEXI and CII inapplicable in
March 2023 and would contradict `DESKTOP_QP_ALLOCATION_2023.md` §3, which records EEXI and CII as
in force from 1 January 2023 and operative for the whole year. The allocation record is right and
the corpus register is wrong. Chapter 4 was in force from 1 November 2022 and the EEXI and CII
requirements applied from 1 January 2023, so **both are squarely operative at this sitting** and Q2
and Q4 are authored on that footing.

**Nothing was written back to the corpus.** The defect is reported to the Founder in the session
handover for the producer team to correct under its own governance.

### 2.4 A second finding from the same read — the primary anchor for Q2

The same resolution's preamble **RECALLS FURTHER** that the Committee *"at its seventy-second
session, adopted resolution **MEPC.304(72)** on the Initial IMO Strategy on reduction of GHG
emissions from ships"*.

This is the strongest possible temporal anchor for Q2, and it is a **primary** one: the instrument
that created the two short-term measures the question asks about names the Initial Strategy as the
policy frame it sits under. At March 2023 that relationship is current. Q2 is authored on it.

### 2.5 Future at March 2023 — PROHIBITED

| Item | Date | Note |
|---|---|---|
| **2023 IMO GHG Strategy `MEPC.377(80)`** | 7 Jul 2023 | **Held in the corpus. Must not be used.** The single sharpest trap on this paper |
| `MEPC.376(80)` LCA guidelines | 7 Jul 2023 | Future |
| 33rd Assembly `A.1185(33)` PSC procedures | 6 Dec 2023 | **Held in the corpus. Must not be used** for Q7 |
| `A.1186(33)`, `A.1187(33)`, `A.1188(33)` | 6 Dec 2023 | Future |
| `MEPC.395(82)` 2024 SEEMP guidelines | 2024 | Future — supersedes the operative `MEPC.346(78)` |
| MEPC 81 / 82 / 83 and all their resolutions | 2024–2025 | Future |
| `MEPC.361(79)`, `MEPC.362(79)` in force | 1 May 2024 | Adopted Dec 2022, **not in force** at the sitting |
| SOLAS Consolidated Edition 2024 | 1 Jul 2024 | Future |
| MLC 2022 amendments | 23 Dec 2024 | Adopted, **not in force** |
| Hong Kong Convention | 26 Jun 2025 | **Not in force anywhere in 2023** |
| IMO Net-Zero Framework / GFI | Oct 2025 | Future — and still not adopted |
| 34th Assembly `A.12xx(34)` | 3 Dec 2025 | Future |
| **Merchant Shipping Act, 2025** | 15 Mar 2026 | Future by three years |

**The corpus register inversion is at its worst on this paper.** The corpus is maintained for the
present, so it holds `MEPC.377(80)` and `A.1185(33)` as current and marks `MEPC.346(78)` as
*superseded*. For a March 2023 sitting that is exactly inverted: the superseded instrument is the
operative one and the current instruments are future. Direction was checked on every consumption.

### 2.6 What changed between January 2023 (QP2301) and this sitting

QP2301's anchor cannot simply be inherited, so the two-month window was checked directly. **Nothing
of regulatory consequence to this paper changed between January and March 2023.** No IMO body met
in the window — MEPC 79 closed in December 2022 and MEPC 80 did not sit until July 2023 — no
amendment entered into force, and no Assembly session fell in it. The January anchor is therefore
sound for March **on the instruments it covers**, but it is *silent* on the instruments this paper
actually turns on: it carries no finding on the GHG strategy layer, on PSC procedures or on the RO
Code. Those were established here from source and not assumed.

---

## 3. DONOR MAP — derived by reading printed stems, not by score

Discovery used a lexical and topical sweep over **288 solved questions across 32 papers** — the 30
papers integrated on `main` at `d6d95e8` plus QP2304 and QP2309 read from their pushed branches.

**The sweep was controlled before it was trusted.** A first pass returned zero on all eighteen
stems; the cause was a wrong field name, not an absence of donors. The corrected sweep was then
seeded with a known positive — `QP2312-Q1` against `QP2606-Q1`, recorded in the corpus as
character-identical — and returned **1.000**. Only then were its results read. A zero from the
first pass would have been a broken filter reported as a clean paper.

Every pair below was then adjudicated by **reading both printed stems in full**. Scores prompted;
they did not decide.

### 3.1 Per-question derivation

| Q | Subject | Preferred donor | Class | Basis |
|---|---|---|---|---|
| **Q1** | UNCLOS pollution definition and coastal-State obligations; the three compensation tiers | `QP2309-Q8` **(same-year)** + `QP2404-Q9` | **LIMB-LEVEL** | Limb A only. Both donors ask UNCLOS marine-environment protection; neither *defines pollution* nor treats *coastal-State* obligations as such, and neither reaches limb B at all |
| **Q2** | Decarbonisation; IMO ambitions; the two short-term measures | `QP2411-Q7` | **NEAR** | Stems align from *"Briefly discuss…"* onward. QP2303 adds an opening *"What is Decarbonisation in shipping?"* and prints *"long tern"*. Task-equivalent; **heaviest temporal reversal on the paper** |
| **Q3** | Perils of the sea; due diligence | `QP2503-Q5` | **EXACT** | Character-identical but for the printed quotation marks around *"due diligence"*. Second donor `QP2507-Q5`. Same-year support from `QP2301-Q3` and `QP2312-Q3` |
| **Q4** | Primary vs secondary NOx reduction; SAM and EGR | `QP2407-Q9` | **TOPICAL-ONLY** | The donor is a four-part short-note question (Tier II/III, emulsion, SCR, NOx Technical File). It supplies secondary-measure substance but neither the primary-vs-secondary framing nor SAM. Route is **not** reusable |
| **Q5** | Power transformation stages; sea trial manoeuvres | **none** | **FRESH** | No donor anywhere in 288. Best score 0.189 against an unrelated tribology question — noise. Authored from first principles |
| **Q6** | Human error, human element, human factors | `QP2411-Q8` | **NEAR** | Same two limbs in the same order. **Marks differ: 8/8 printed here against 6/10 in the donor**, so the depth balance is re-cut. Printed quotation differs (§1.3) |
| **Q7** | PSC clear grounds; corrective vs preventive action | `QP2406-Q3` (limb a) + `QP2312-Q2` **(same-year)** | **LIMB-LEVEL** | Limb a is a genuine match on clear grounds. **Limb b has no donor** — corrective vs preventive action is an ISM/quality-system distinction that no solved question asks. Half fresh |
| **Q8** | IACS structure, UI/UR/PR; RO Code | `QP2401-Q5` | **EXACT** | Both limbs align; `QP2607-Q3` is a second exact donor. **`QP2309-Q2` is a verbatim same-year donor for limb b** — see §3.2 |
| **Q9** | Lubricating oil analysis techniques | `QP2406-Q9` | **EXACT** | Identical but for *"condition of L.O"* against *"condition analysis of L.O"* (§1.3). Second donor `QP2411-Q9` |

**Derived readiness: 3 EXACT · 2 NEAR · 2 LIMB-LEVEL · 1 TOPICAL-ONLY · 1 FRESH = 8 of 9 with a
donor.** Allocation §4 recorded 5 exact/near and 6/9 against a 234-question corpus. Recomputed
against 288 the paper is **stronger** than the frozen table, exactly as §0.3 predicted.

### 3.2 Same-year relations — the finding that most changes this paper

The allocation's §2 systemic fact — every donor to a 2023 question is later than its sitting — now
has **four exceptions in the corpus and one that runs backwards**.

| This paper | Same-year donor | Sitting | Direction | Value |
|---|---|---|---|---|
| **Q8 limb b** | **`QP2309-Q2`** | Sep 2023 | +6 months | **Verbatim identical stem.** *"What is a Recognized organization? What are the salient features of the R.O. Code? How do Administrations monitor R.O.s?"* — word for word. The single most valuable donor on this paper: same year, same regulatory position, near-zero reversal |
| Q1 limb A | `QP2309-Q8` | Sep 2023 | +6 months | UNCLOS marine environment. Preferred over `QP2404-Q9` (+13 months) on the same-year rule |
| Q7 limb a | `QP2312-Q2` | Dec 2023 | +9 months | PSC legal framework. Newly visible only because of the `d6d95e8` baseline |
| Q7 limb a | `QP2309-Q9` | Sep 2023 | +6 months | PSC non-party certificates, no-more-favourable-treatment |
| Q2 | `QP2309-Q3` | Sep 2023 | +6 months | GHG measures — **but Sept 2023 sits AFTER 7 July.** Same-year and still requires the full strategy reversal. Route only |
| **Q3** | **`QP2301-Q3`** | **Jan 2023** | **−2 months** | **The first backward-running donor in the batch.** Marine insurance policy types. An earlier donor structurally cannot drag later law backwards |
| Q8 limb a | `QP2304-Q9`, `QP2312-Q8` | Apr / Dec 2023 | +1 / +9 months | Classification societies in rule formation — adjacent to IACS structure |
| Q3 | `QP2312-Q3` | Dec 2023 | +9 months | Types of loss, York-Antwerp |

`QP2301-Q3` deserves the emphasis. **It is the first donor in Batch 4 that pre-dates its
recipient**, and it is the normal MIW case that allocation §2 said would not occur anywhere in this
batch until a 2023 paper was solved. It has now occurred. The batch's standing rule still holds for
the other eight questions.

**The prompt's anticipated same-year subjects were tested against printed stems and only partly
confirmed.** RO Code and PSC do occur in QP2303 and their same-year donors are real. **IMO
structure does not occur in this paper** — `QP2309-Q4` (IMO structure and instrument hierarchy) has
no counterpart in March 2023 and is **rejected**, not stretched to fit Q8. Likewise **ISM
certification** does not occur: `QP2309-Q7` (audit versus survey, RO action on ISM certificates)
touches Q8's RO material only obliquely and Q7's limb b not at all.

### 3.3 Rejected donors — recorded so the rejection is auditable

| Candidate | For | Why rejected |
|---|---|---|
| `QP2309-Q4` IMO structure and hierarchy | Q8 | **Subject does not occur.** Q8 asks IACS structure and the RO Code, not IMO organs. Rejected on the printed stem despite being flagged in advance |
| `QP2309-Q7` audit versus survey, ISM certificates | Q7, Q8 | Adjacent only. Q7 limb b asks corrective vs preventive action, which the donor does not treat |
| `QP2404-Q9` UNCLOS zones | Q1 | Not rejected outright but **demoted** below `QP2309-Q8` on the same-year rule; its limb (b) on maritime zones is not asked here |
| `QP2304-Q7`, `QP2509-Q7`, `QP2402-Q2`, `QP2409-Q6` Bunker/CLC | Q1 limb B | **Rejected as donors.** All compare Bunker 2001 with CLC 92. Q1 B asks the **three-tier compensation structure** — CLC / FUND / Supplementary Fund — which is a different question. Read, and not used |
| `QP2401-Q6` marine tribology | Q1, Q5, Q7, Q9 | Recurring high-scoring noise across four unrelated stems. Pure lexical artefact; rejected everywhere |
| `QP2602-Q4`, `QP2601-Q9`, `QP2508-Q4` human element in STCW | Q4, Q6 | Scored on the word "human" against Q6 and on nothing at all against Q4. Rejected; the real Q6 donor is `QP2411-Q8` |
| Host hint `2023/FEB/Q2` | Q2 | **Host hint is factually wrong** — February 2023 Q2 is the III Code question. Rejected on the printed stem |

---

## 4. LATER-STATE REVERSALS — question by question

Every donor except `QP2301-Q3` is later than this sitting. A donor is a **route**, not prose.

### Q2 — the sharpest reversal on the paper

`QP2411-Q7` is a **November 2024** answer. Between it and March 2023 lie MEPC 80, MEPC 81 and
MEPC 82. Everything below must be reversed:

| Donor state (Nov 2024) | March 2023 state |
|---|---|
| **2023 IMO GHG Strategy** `MEPC.377(80)` is the operative ambition set | **Future by four months.** The operative instrument is the **Initial Strategy `MEPC.304(72)` of 2018** |
| Net-zero "by or around 2050"; 20/30 % by 2030; 70/80 % by 2040 checkpoints | **None of these exist.** The Initial Strategy's levels are: carbon intensity **−40 % by 2030**, pursuing **−70 % by 2050**, and **total annual GHG at least −50 % by 2050** against 2008 |
| "Indicative checkpoints" is live vocabulary | **Not yet coined.** Do not use the word |
| Mid-term measures under development post-MEPC 80 basket | Mid-term measures are **candidate measures under the Initial Strategy's programme of follow-up actions** |
| `MEPC.395(82)` SEEMP guidelines | **`MEPC.346(78)`** 2022 SEEMP guidelines |
| LCA guidelines `MEPC.376(80)` available | Future |

**The two short-term measures are unchanged and are the stable core of this answer** — EEXI and
CII, introduced by `MEPC.328(76)`, in force 1 November 2022, applying from 1 January 2023, with
guidelines `G1`–`G5` all sitting-correct. The answer is anchored there and the ambition layer is
re-derived onto the Initial Strategy.

### Q6

`QP2411-Q8` is November 2024 but the subject — human error in a socio-technical system, and the
element/error/factors distinction — is **conceptual and essentially time-invariant**. The reversal
burden is near zero. The real delta is **marks**: 8/8 printed here against 6/10 in the donor, so
limb (a) is expanded and limb (b) trimmed relative to the donor's balance. Any reference to
post-2023 human-element instruments is removed.

### Q7

Limb a: `QP2406-Q3` is June 2024. The PSC procedures resolution it may rest on is **`A.1155(32)`**,
not `A.1185(33)` — the latter is 6 December 2023 and future. See §5 for the evidence consequence.
Limb b is fresh and is authored on the ISM Code as amended through `MSC.353(92)`, which is
sitting-correct.

### Q8

`QP2401-Q5` is January 2024 and `QP2607-Q3` is July 2026. The RO Code has not been amended between
March 2023 and either donor, and IACS's UI/UR/PR instrument classes are stable, so the reversal
burden is low. **Limb b is taken from `QP2309-Q2` instead** — same year, verbatim stem, six months
later, no strategy or Assembly boundary crossed between them. Any reference to a 33rd-Assembly
instrument in the later donors is removed.

### Q9

`QP2406-Q9` is June 2024. The subject is **engineering, not regulation** — spectrometric analysis,
FTIR, particle count, BN against AN. It is temporally neutral; no regulatory statement is inherited
and none is needed. Lowest reversal burden on the paper.

### Q3

`QP2503-Q5` is March 2025, +24 months. Marine insurance rests on the Marine Insurance Act 1963
(India) and settled common-law doctrine, neither of which moved in the window. The donor was still
audited for sitting-relative phrasing. **`QP2301-Q3` runs backwards and is structurally safe.**

### Q1

Limb A rests on **UNCLOS 1982, unamended** — the ideal case, where the held text *is* the sitting
text. Limb B's tier structure — CLC 1992, FUND 1992, Supplementary Fund 2003 — was fully in force
well before the sitting. **Monetary limits are the live risk**: the FUND and Supplementary Fund
limits and the CLC tonnage bands are amended by tacit acceptance over time, and a later donor's
figures cannot be carried. See §5.

### Q4 and Q5

Q4 rests on MARPOL Annex VI regulation 13 and the NOx Technical Code 2008, both operative and
unchanged in substance at the sitting; `MEPC.385(81)`'s reg 13.2.2 replacement is 2024 and is
excluded. Q5 is naval architecture and machinery performance with no regulatory content and no
donor; nothing to reverse.

---

## 5. CORPUS USE — what was consumed, and what could not be

Corpus commit **`319524c`**, read-only. **No corpus modification was made from this branch.**

| Instrument | Held? | Used for | Status |
|---|---|---|---|
| **UNCLOS** — `05-un-and-treaty-law/UNCLOS/_base/` | **yes**, official text | Q1 A | **Primary. Unamended since 1982 — the held text is the sitting text** |
| **MARPOL Annex VI** `MEPC.328(76)` — `_base-and-amendments/` | **yes**, official resolution | Q2, Q4 | **Read at source for its operative paragraphs** (§2.3). Instrument is `citation-ready` only under the 2026-08-11 freeze — **resolved to identity and provenance, never quoted as regulation text** |
| **CII guidelines `G1`–`G5`** — `GHG-instruments/` | **yes** | Q2 | **Sitting-correct** (2021–2022). Cited by identity |
| **`MEPC.346(78)`** 2022 SEEMP guidelines | **yes**, marked *superseded* in the corpus | Q2 | **Operative at this sitting.** The corpus marking is inverted for 2023 — see §2.5 |
| **`MEPC.304(72)`** Initial GHG Strategy | **not held as a document** | Q2 | **Identity and content established from `MEPC.328(76)`'s own preamble** (§2.4), which recalls it. Substantive levels graded P2 — see §5.2 |
| **ISM Code** chain — `A.741(18)` → `MSC.353(92)` | **yes**, official chain | Q7 b | **Primary.** `MSC.353(92)` is the last amendment; the held text is the March 2023 text |
| **RO Code** — `RO_code.pdf` | **yes** | Q8 b | Usable, **evidence downgraded**: `RQ-25` leaves edition and completeness unverified |
| **PSC procedures** | held, but **wrong edition** | Q7 a | **NOT CONSUMED.** Only `A.1185/1186/1187(33)` are held, all 6 December 2023 and future. **`A.1155(32)` is not held** |
| **CLC 92 / FUND 92 / Supplementary Fund 2003** | **no text** — status placeholders only | Q1 B | **NOT QUOTED.** The family log holds verified status facts and explicitly declines to assert SDR limits |
| **NOx Technical Code 2008** | held with Annex VI | Q4 | Cited by identity |
| **IACS** — `07-iacs-and-class/` | notes only | Q8 a | `CLASS_AND_SURVEY_NOTES.md` only; no IACS procedural documents held |
| **Merchant Shipping Act, 1958** | **no** — corpus holds the **2025** Act | — | **Structurally inverted.** The corpus holds only the statute that commenced three years *after* this sitting. Not consumed |

### 5.1 Referrals carried, not consumed

- **`A.1155(32)` PSC procedures — NOT HELD.** The corpus holds only the 33rd-Assembly set, which is
  future for this sitting. Q7 limb a therefore cites the PSC procedures regime by **identity and
  concept**, not by quoted paragraph, and its evidence is graded accordingly. This is the same
  referral QP2309 carried at §5.1 and it is unchanged — a standing 2023-batch gap, not a new one.
- **`RQ-25` RO Code edition/completeness — CARRIED.** Q8 limb b rests on a held file whose edition
  is unverified. The answer is authored from it and the grade reflects the open check.
- **`RQ-31` FSA circular placeholder** — noted, not reached by this paper.

### 5.2 Evidence gaps recorded honestly

1. **The Initial GHG Strategy is not held as a document.** Its *identity* is primary-verified from
   `MEPC.328(76)`'s preamble. Its *substantive levels* — the −40 % by 2030 carbon-intensity level,
   the −70 % pursuit, the at-least −50 % total-GHG level by 2050, all against a 2008 baseline — are
   graded **P2 authoritative secondary** and are flagged in `reverify_before_publication` on Q2.
   They are stated as the Initial Strategy's levels of ambition and are not attributed to a quoted
   paragraph.
2. **No compensation-convention text is held.** Q1 limb B's three-tier structure is authored from
   the corpus's status-verified facts plus settled convention architecture. **No SDR figure is
   asserted numerically**, following the corpus's own explicit retrieval instruction. The tier
   ceilings are flagged for verification against official IOPC tables before publication.
3. **`A.1155(32)` unavailable** — see §5.1.
4. **IACS holds no procedural documents.** Q8 limb a's account of UI, UR and PR is authored from
   engineering and industry knowledge and graded **P3 industry guidance**, not primary.
5. **Q5 has no corpus dependency and no donor.** It is graded on engineering reasoning throughout.
6. **MEPC.328(76) is citation-ready, not quotation-ready.** Under `MPVI-FREEZE-2026-08-11` the
   instrument resolves to identity and provenance only. Q2 and Q4 cite it; neither quotes Annex VI
   regulation text. The operative-paragraph read in §2.3 is a read of the **resolution's own
   preamble and operative clauses**, which are not the Annex text and are not subject to that
   restriction.

---

## 6. SUMMARY OF THE ANCHOR

| | |
|---|---|
| Sitting | **March 2023** — after EEXI/CII application, before the 2023 GHG Strategy and the 33rd Assembly |
| Day dependence | **None.** No boundary falls inside the sitting month |
| Printed questions | **9**, established by reading both rendered pages; uniform `Q1.`–`Q9.` |
| Printed marks | **Largely absent** — only Q6 and Q7 print a full 16; Q4 prints 8 against two limbs |
| Statute | **Merchant Shipping Act, 1958** |
| GHG policy frame | **Initial Strategy `MEPC.304(72)` 2018** — the 2023 Strategy is future |
| Assembly set | **32nd (2021)** — `A.1155(32)`, not `A.1185(33)` |
| Donor readiness | **8 / 9** — 3 EXACT, 2 NEAR, 2 LIMB-LEVEL, 1 TOPICAL-ONLY, 1 FRESH |
| Same-year donors | **8 relations across 5 questions**, including one **verbatim** (`QP2309-Q2` → Q8 b) and one that runs **backwards** (`QP2301-Q3` → Q3) |
| Corpus commit | `319524c` — read-only, unmodified |
| Corrections raised | **1** — `MEPC.328(76)` entry-into-force year in `amendment-register.json` (§2.3) |

---

## 7. FINALISED AT AUTHORING — what changed when the nine answers were written

**Written after Q1–Q9 were authored and promoted.** Nothing above was rewritten; this section records what
authoring found, so that the difference between the pre-authoring adjudication and the finished paper is
visible rather than silently absorbed.

### 7.1 The adjudication held. Four things were corrected.

| # | Finding | Where it is recorded |
|---|---|---|
| 1 | **§3.1 misdescribes the Q3 divergence.** It records the difference from `QP2503-Q5` as lying in the printed quotation marks around *"due diligence"*. A word-by-word re-diff of both `text_verbatim` fields at authoring time shows **the quotation marks are identical in both papers**, and that the **sole** divergence is the donor's printed `(16)`, which this paper does not carry. | `Q3.question_delta`, `Q3.unresolved`, `Q3.reverify_before_publication`, `verification/QP2303/Q3.md` |
| 2 | **The spec's `source_copy_provenance` omitted `pages` and `printed_serial`.** Every other spec in the corpus carries both, and `build_reuse_map.py` fails without `pages`. The values — **2 pages** and **`2303 EM`** — were established at intake and are recorded at §1 of this anchor; they were **restored, not changed**. | `specs/QP2303.json`, `source_copy_provenance.printed_serial_note` |
| 3 | **The `A.1157(32)` reversal is required on TWO questions, not one.** §2.2 records it as the operative PSC procedures resolution for Q7. Authoring found that **Q8's monitoring limb needs the identical reversal**, because its January 2024 donor closes on the obligations list at `A.1187(33)` — adopted 6 December 2023, nine months after this sitting. The correction was made on both questions **independently from the adoption dates**, not inherited from either. | `Q7.temporal_review`, `Q8.temporal_review`, `Q8.question_delta` |
| 4 | **A second IACS forward trap was closed on Q8.** The Safe Digital Transformation Panel was constituted in **January 2024**, ten months after this sitting. No panel constituted after March 2023 is named and **no panel count and no membership count is asserted**. | `Q8.unresolved`, `Q8.temporal_review` |

### 7.2 The two findings §2.3 and §2.4 turned on both held

- **The `MEPC.328(76)` correction is load-bearing on two questions and it held.** Entry into force is
  **1 November 2022**, from the resolution's own operative paragraph 3. Q2 and Q4 are both authored on it. Had
  the register's `2023-11-01` been consumed, Q4's regulatory frame would have been inapplicable and **Q2 would
  have been unanswerable**. The corpus was **not edited from this branch** and the
  `TRUE_SOURCE_CORRECTION_REQUEST` stands.
- **The §2.4 primary anchor for Q2 held and is the best evidence on the paper.** `MEPC.328(76)`'s preamble
  *RECALLS FURTHER* the adoption of `MEPC.304(72)`, so the instrument that created EEXI and CII names the
  Initial Strategy as the frame it sits under. `MEPC.304(72)` is still **not held as a document**: its identity
  is primary-verified from that preamble and its **levels of ambition remain graded P2** and flagged.

### 7.3 The donor shape was confirmed unchanged

**3 EXACT · 2 NEAR · 2 LIMB-LEVEL · 1 TOPICAL-ONLY · 1 FRESH = 8 of 9.** No question moved class at authoring.

- **Q5 is genuinely fresh.** Neither limb has any relative in the corpus; the 0.189 best score is noise from
  `QP2401-Q6`, which recurs as a false positive against Q1, Q5, Q7 and Q9 alike.
- **Q7 is half fresh in practice.** Limb a matches `QP2406-Q3` at limb level; **limb b has no donor anywhere**,
  and corrective versus preventive action was authored from first principles.
- **Q1 limb B has no donor and the rejection is the finding.** `QP2304-Q7`, `QP2509-Q7`, `QP2402-Q2` and
  `QP2409-Q6` were each read in full and rejected: they compare Bunkers 2001 with CLC 92, which is a different
  question from the three-tier structure this limb asks for.
- **A same-year donor is not automatically a safe donor.** `QP2309-Q3` (September 2023) sits **after 7 July
  2023**, so it is written on the 2023 Strategy and needed the full reversal itself. Nothing substantive was
  carried from it.

### 7.4 Two new evidence limitations, recorded rather than resolved

1. **The EEXI guideline resolution numbers were not established.** §5 established the CII set `G1`–`G5` by
   number; it did not establish the EEXI set. Those guidelines are therefore cited **by function only** and
   **no resolution number is asserted for any of them**. A number was deliberately not invented to match the
   symmetry of the CII table, and the gap is stated in Q2's own answer.
2. **Q5 has no corpus dependency and cites three IMO instruments by identity only** — the manoeuvrability
   standards, the manoeuvring-information requirement and the steering gear trial. **None was read at source**,
   and **no criterion value is asserted anywhere**.

### 7.5 Production-term leak found and closed

A candidate-facing sweep of `model_answer`, `study_notes`, `quick_revision`, `retrieval_cards`,
`answer_route`, `memory_cue` and `understand_first` found the production term **"donor"** in the closing
uncertainty note of **Q5 and Q8**. Both were rewritten in candidate vocabulary. The delivery surface now
carries **zero** occurrences of `donor`, `founder-review`, `staging`, `RulesApp`, `true-source` or
`reuse_evidence`. The review copy retains them **only** in its own review banner and provenance block, which is
the established behaviour of every review page and is stripped from the delivery build.

### 7.6 One presentational fix from the mobile review

Q8's `UR / UI / PR` table was authored with **four** columns and was the only element on the paper wider than a
375 px viewport. It was folded to **three**, with *how it reaches a ship* carried inside the *what it is* cell.
No content was removed. At 375 px and at 1280 px, with all nine cards open, **zero elements exceed the
viewport** and the document does not scroll horizontally.

---

## 8. SIX-YEAR WORDING ANCESTRY — added at laptop review, 2026-08-14

The desktop derived the donor map at section 3 by reading printed stems **against the MIW solved set**.
That is the right basis for an *answer donor* and it is unchanged. It is not a basis for *wording
ancestry*, because the solved set holds no 2021 or 2022 sitting. This section re-derives ancestry against
the **2021–2026 window — 61 sittings / 549 questions** — as QP2309 was re-derived at its own §7m.

**Three fields, kept apart.** *Wording ancestry* is where a stem was first printed. An *answer donor* is a
solved question whose reasoning may be reused. The *temporal answer basis* is March 2023 regardless of
either. An intelligence-only sitting can establish the first, and can never supply the second.

### 8.1 The result, question by question

| Q | Class | Earliest known printing | Later printings | Direction |
|---|---|---|---|---|
| **Q1** | EXACT_REPEAT | **QP2104-Q2 — April 2021** | QP2210-Q9 (Oct 2022) · QP2306-Q1 (Jun 2023) | **backward, 23 months** |
| **Q2** | EXACT_REPEAT | **QP2208-Q4 — August 2022** | none | **backward, 7 months** |
| **Q3** | EXACT_REPEAT | **QP2208-Q2 — August 2022** | QP2503-Q5 · QP2507-Q5 (2025) | **backward, 7 months** |
| **Q4** | EXACT_REPEAT | **this sitting** | QP2307-Q3 (Jul 2023, 4-limb variant) · QP2310-Q5 (Oct 2023) | forward |
| **Q5** | NEAR_REPEAT | **this sitting** | QP2308-Q6 (Aug 2023) | forward |
| **Q6** | EXACT_REPEAT | **this sitting** | QP2411-Q8 (Nov 2024, marks 6/10 not 8/8) | forward |
| **Q7** | **UNIQUE** | — | nothing above the noise floor in six years | — |
| **Q8** | EXACT_REPEAT | **this sitting** | QP2309-Q2 (Sep 2023, limb b alone) · QP2401-Q5 (Jan 2024) · QP2607-Q3 (Jul 2026) | forward |
| **Q9** | EXACT_REPEAT | **QP2107-S2-Q1 — July 2021** | QP2108-Q2 (Aug 2021) · QP2203-Q2 (Mar 2022) · QP2406-Q9 (Jun 2024) | **backward, 20 months** |

**Four of the nine run backward.** March 2023 originates only Q4, Q5, Q6 and Q8; Q7 is unique; and Q1, Q2,
Q3 and Q9 were all set before this sitting. **No `reused_from` changed** — the intelligence layer holds
printed wording and no answers, so it can correct *where a question was first asked* and can never supply
*what the answer is*.

**The host's own annotations agree independently.** `2021/APR/Q2` and `2022/OCT/Q9` on Q1, `2022/AUG/Q4` on
Q2, `2022/AUG/Q2` on Q3, and `2021/JUL/Q1`, `2021/AUG/Q2`, `2022/MAR/Q2` on Q9 each name exactly the sitting
the six-year scan found. That is a genuine cross-check: the annotation is discovery evidence only and is
never a MIW claim, but two independent methods reaching the same sittings is worth recording.

### 8.2 QP2303-Q8 → QP2309-Q2 — confirmed by measurement

`QP2303-Q8` limb (b) and the **whole** of `QP2309-Q2` normalise to the **identical string**, differing only
by QP2309's printed `(16)`. March 2023 sets it as one of two limbs; September 2023 promotes the same three
sentences to a standalone sixteen-mark question. **QP2303 is the wording root of that family.**

**`QP2207-Q7` is NOT a wording ancestor and the July 2022 premise stays rejected.** Measured against
`QP2303-Q8` its stem similarity is **0.053**, and against `QP2309-Q2` it is 0.325 — below any family
threshold. It asks for the *limitations* of the RO and the salient *responsibilities* of a class society
authorised as an RO. That is `SAME_CONCEPT_FAMILY` at most. Do not reinstate it as an exact or near
ancestor without printed evidence.

### 8.3 A defect in the historical extractor, found through this paper and fixed

The six-year store carried the host's code **inside 58 stems across 24 papers**, including
`2023/JUNE/Q1` on `QP2306-Q1` — the *exact* reprint of this paper's Q1. Because
`recurrence_model.normalise_stem` compares printed stems for equality, that annotation made a
**verbatim-identical question compare UNEQUAL**, which is failure mode 1 in the extractor's own comment
block. QP2303's Q1 ancestry was being silently suppressed by it.

`HOST_HINT_RX` fixed the month at **exactly three letters**, so it matched `2023/MAR/4` but not
`2021/JULY/Q1` or `2023/JUNE/Q1` — after `JUL` the next character is `Y`, the trailing `\b` failed, and the
whole annotation survived. Widened to `[A-Z]{3,9}` with the attached-digit form `2016/JAN2` admitted. Two
further span-based rules were added for the sales footer that wraps after *"organized manner with"* and for
the bare page number left at the end of a stem spanning the page break.

**Proof:** 71 stems changed, **0 stems gained any text**, all 270 question ids preserved, and **0 residual
host artefacts** of any form. `QP2306-Q1` now compares equal to `QP2303-Q1`, which is what surfaced the
April 2021 root. `sixyear_intelligence_test.py` **PASS on all 8 rules**.

---

## 9. CORRECTIONS APPLIED AT LAPTOP REVIEW, 2026-08-14

Seven of nine questions were accepted as authored. Two were corrected, both at the canonical spec, and the
HTML regenerated. No generated page was hand-edited.

### 9.1 Q2 (MAJOR) — guideline **G5** was misdescribed on every surface it appeared

The answer gave **`MEPC.355(78)`** as *"corrective action for a poor rating, and incentives for good
performance"*. **Read at source in this session**, its title page is:

> RESOLUTION MEPC.355(78) (adopted on 10 June 2022) — 2022 INTERIM GUIDELINES ON CORRECTION FACTORS AND
> VOYAGE ADJUSTMENTS FOR CII CALCULATIONS (CII GUIDELINES, G5)

The resolution **number** was right; the **subject** was wrong. Corrective action for a D-or-E rated ship is
not a guideline at all — it lives in **MARPOL Annex VI regulation 28** and in the **SEEMP guidelines
`MEPC.346(78)`**, both of which this answer already states correctly elsewhere. The error propagated to
**seven candidate-facing surfaces** — the model-answer table, the study notes, quick revision, the answer
route, the memory cue, a retrieval card and the sources block — and all seven are corrected.

**The correction strengthens the answer's own argument.** Section 6 criticises the CII for dividing by
capacity and distance, penalising a laden ship waiting at anchor and short-sea trades. **G5 is precisely the
instrument that addresses that**, by correction factors for certain ship types and voyage adjustments. As
written, the answer raised the criticism and then mislabelled its remedy.

This is a **regression against MIW's own verified record**: `QP2411`'s anchor already carried G5 correctly,
`P1 PRIMARY VERIFIED`, read at source.

### 9.2 Q1 (MINOR, precise) — the transfer-of-damage duty is **article 195**, not article 194

The answer read *"Article 194 carries two further duties … measures taken must not transfer damage or
hazards from one area to another, or transform one type of pollution into another."* **UNCLOS was read at
source**: article 194(2) carries the damage-to-other-States duty, and the transfer duty is **article 195**,
a separate article with its own heading — *Duty not to transfer damage or hazards or transform one type of
pollution into another*. On a limb whose mark scheme is article-level precision, a reader sent to 194 would
not find it. Re-attributed, with 194(2) stated in its own terms.

### 9.3 Understated holdings — the fourth occurrence of a known defect class

Two claims understated what MIW holds, and both were promoted after reading the instrument:

| Claim as authored | Reality | Action |
|---|---|---|
| Q1: Part XII safeguards *"referred to here in general terms; their individual articles were not examined"* | **UNCLOS is held.** Section 7, articles 223–233 | **Read at source.** Articles 224, 225, 226, 227, 230, 231 and 232 now named with their substance; graded `P1` |
| Q2: the CII guideline set graded **`P2` authoritative secondary**, *"established by the corpus review"* | **All five are held** as official IMO resolution texts | **All five title pages read at source.** G1–G5 and the SEEMP guidelines promoted to `P1 PRIMARY` with verified titles and adoption dates |

**Claims that were checked and are accurate, and were left alone:** `MEPC.304(72)` is genuinely **not
held** (Q2); the **EEXI** guideline set is genuinely not held, and citing it by function rather than
inventing a number is correct (Q2); `A.1155(32)` is genuinely **not held** — MIW holds only the
33rd-Assembly `A.1185(33)`, which is nine months future for this sitting (Q7); and MIW holds **no IACS
procedural document** and no quality-management standard (Q8, Q7 limb b).

### 9.4 Temporal result

**All nine questions are correct as at March 2023.** The two sharpest reversals were made by the desktop and
both are verified: the **Initial IMO Strategy `MEPC.304(72)`** governs Q2, with `MEPC.377(80)` of 7 July
2023 absent from the object entirely; and **`A.1155(32)`** governs Q7's procedural layer, with the whole
33rd-Assembly set of 6 December 2023 excluded. `A.1157(32)` over `A.1187(33)` on Q8 is right for the same
reason. `MEPC.385(81)` (2024) is correctly excluded from Q4. **No post-sitting instrument appears in any
candidate-facing field.**
