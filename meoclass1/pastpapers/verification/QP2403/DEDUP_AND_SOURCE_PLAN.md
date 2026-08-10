# QP2403 — March 2024 — planning, reuse classification, QP2510 pair map and temporal sweep

**Branch:** `pastpapers/qp2403-founder-review`, cut from `dedce2c` (the QP2508 completion).
**Date:** 2026-08-10.
**Scope of this record:** everything established *before and independently of* answer authoring —
source verification, the Q1–Q9 plan, the reuse tier decisions, the QP2510 relationship audit and
the mandatory sitting-date sweep across **all nine** questions.

---

## 0. Source verification — full visual re-read

The complete March 2024 source paper was re-read in full despite the 2024 intake already
recording 100% visual verification, per the standing production rule.

**Method.** Text extracted with PyMuPDF from the born-digital text layer; all **3 of 3** pages
rendered at 150 dpi and read back against the extraction and against
`specs/QP2403.json.text_verbatim`.

**Result: no discrepancy. No transcription correction was required.** Every stem, every limb,
every printed mark allocation, the instructions, the serial and the region note match the spec
exactly.

Anomalies confirmed as printed, not as transcription loss:

| Feature | Confirmed |
|---|---|
| Printed serial | `Sr. No. EM – 18324-1` |
| Printed total | `Total Marks – 100` against six questions at 16 = 96 |
| **Four questions print NO marks** | Q4, Q5, Q6, Q8 |
| Q1 line break and capital | `maritime sector,` / `Such as shipping operations` |
| Q8 double space | after `dock wall.` — normalised to one space in `text_verbatim` |
| Q5 spacing | `MSC. FAL.1/Circ.3` printed with a space after `MSC.` |
| Q9 apostrophe | `seafarers’` uses a right single quotation mark |
| Page-straddling questions | Q2 (p1→p2) and Q7 (p2→p3) |
| Host editorial furniture | two marketing panels and a per-question recurrence table — **not transcribed, not rendered** |

**New provenance fact, not previously recorded.** The source PDF's own metadata gives
`creationDate: 2024-04-01 17:04:22 +05:30`. The host generated this file **on 1 April 2024**,
days after the sitting — unlike the six 2026 files, which were all batch-generated on 20 April
2026 after every sitting. **This bounds the sitting to on or before 1 April 2024**, which is a
tighter anchor than any 2026 paper has. No temporal claim in this paper turns on a date *inside*
March 2024, so the bound is sufficient.

---

## 1. Q1–Q9 planning table

| Q | Topic | Marks | Limbs | Archetype | Primary category | Tier | Temporal (after sweep) |
|---|---|---|---|---|---|---|---|
| Q1 | Big data in the maritime sector | 16 | (A) 8, (B) 8 | evaluate | Human Element & Management | **C** | STABLE + live instrument |
| Q2 | Bill of lading — definition, types, obligations | 16 | a) 3, b) 5, c) 8 | legal | Marine Insurance & Commercial Law | **C** | **CORRECTED — HIGH** |
| Q3 | General average — principles and contribution | 16 | a) 8, b) 8 | legal | Marine Insurance & Commercial Law | **B** | STABLE |
| Q4 | High-efficiency propellers (any three of four) | 16 | a)–d), none printed | compare | Alternative Fuels & Decarbonisation | **C** | STABLE |
| Q5 | Maritime cyber risk management Guidelines | 16 | (A)–(D), none printed | explain | Human Element & Management | **C** | **CORRECTED — HIGH** |
| Q6 | Electronic record books under MARPOL | 16 | a)–c), none printed | explain | Pollution Prevention & Response | **C** | STABLE (confirmed) |
| Q7 | IMO Instruments Implementation Code | 16 | a) 6, b) 4, c) 6 | explain | Statutory Framework & Class | **B** | STABLE + list updated |
| Q8 | Main engine failure to respond to bridge control | 16 | none, single stem | procedure | Statutory Framework & Class | **C** | STABLE |
| Q9 | MLC 2006 — provisions and enforcement | 16 | a) 8, b) 8 | evaluate | Human Element & Management | **C** | **CORRECTED — HIGH** |

`primary_category` values are the **intake values, deliberately unchanged**, per the §24.8
precedent — an answer build must not move a question on `topics-2024.html`. Two are worth a
Founder note: **Q4** (high-efficiency propellers) sits under *Alternative Fuels &
Decarbonisation* and **Q8** (a bridge-control failure report) under *Statutory Framework &
Class*. Both are defensible — Q4's stem is explicitly framed on ship energy efficiency — but
neither is the obvious choice. **Reported, not changed.**

---

## 2. Reuse classification — and no false donor was manufactured

All 63 built answers across the seven solved papers were listed and reviewed by examiner demand,
not by lexical match. **Zero Tier D.** Two Tier B. Seven Tier C.

### Tier B ×2 — meaningful partial canonical coverage, read not matched

**Q3 — general average.** Five built objects touch general average: `QP2607-Q5` (particular vs
general average and average adjusters), `QP2602-Q6` and `QP2508-Q6` (essential features, and a
refloating claim), `QP2606-Q3` (types of loss, GA under YAR 1994, when GA may be declared),
`QP2601-Q3` and `QP2604-Q3` (salvage law and GA). Between them they materially cover the
*concept*, the *essential features* and the *circumstances of declaration*. They do **not** cover
what QP2403-Q3 asks as its own weight: **contribution among the parties** — contributory values,
the general average bond and guarantee, and the adjustment process — nor limb (b)'s demand for
**worked examples** and criteria "in modern maritime commerce". **Tier B, not D:** no built
question is this examiner's task.

**Q7 — III Code.** `QP2601-Q7` and `QP2604-Q7` (UNCLOS flag State duties and India's mechanism)
carry a route step on how flag State performance is itself checked, and `QP2606-Q2` (port State
control) covers the port State limb of (c) at depth. They do **not** cover the Code's own
objective, its recommended strategy, the instruments it applies to, or the performance
indicators at paragraphs 42–44 — which are limbs (a) and (b), ten of the sixteen marks.
**Tier B, not D.**

### The near-miss that was rejected, and why it matters

**Q5 — cyber.** `QP2606-Q5` (June 2026, the ISM Code and the evolution of the SMS) contains a
route step headed *Cyber risk*. A lexical reuse search would have offered it. It was rejected on
**two independent grounds**, either sufficient:

1. **Demand.** It is one step of seven in a question about the ISM Code. Per the QP2602-Q3 /
   QP2607-Q1 precedent, shared framework is *supporting reuse*, not an answer donor.
2. **Temporal incompatibility, and it is fatal.** That step states the functional elements as
   **six**, correctly for June 2026, because it is written on **MSC-FAL.1/Circ.3/Rev.3 of 4 April
   2025**. At the March 2024 sitting the operative edition is **Rev.2 of 7 June 2022** and there
   are **five**. Importing the step would have put a **non-existent functional element** into a
   March 2024 answer.

> **Recorded as supporting reuse. `reused_from` remains null on all nine questions.**

---

## 3. QP2403 ↔ QP2510 pair audit — verified directly, not inherited

Every pair was compared by **string comparison of the two transcribed stems**, not taken from the
previous session's report. **All nine map one-to-one, Q1→Q1 through Q9→Q9.** The claim holds.

| QP2403 | QP2510 | Ratio | Class | Question delta | Marks delta | **Temporal delta** |
|---|---|---|---|---|---|---|
| Q1 | Q1 | 1.0000 | **EXACT** | none | none | **Material** — see §4 Q1 |
| Q2 | Q2 | 1.0000 | **EXACT** | none | none | **MATERIAL — statute repealed between sittings** |
| Q3 | Q3 | 1.0000 | **EXACT** | none | none | none identified |
| Q4 | Q4 | 1.0000 | **EXACT** | none | none | none identified |
| Q5 | Q5 | 0.9947 | **NEAR — marks token only** | printed `(16)` inserted after "elaborate following:" | none (both 16) | **MATERIAL — Rev.2 → Rev.3, five elements → six** |
| Q6 | Q6 | 1.0000 | **EXACT** | none | none | **none — the cleanest donor on the paper** |
| Q7 | Q7 | 0.9926 | **NEAR — limb marks only** | none in wording | **6+4+6 → 6+5+5** | minor — obligations list re-issued |
| Q8 | Q8 | 1.0000 | **EXACT** | none | none | none identified |
| Q9 | Q9 | 1.0000 | **EXACT** | none | none | **MATERIAL — MLC 2022 amendments in force between sittings** |

**Seven EXACT, two NEAR — and both NEAR pairs differ only in a printed marks token.** Q5 is the
QP2604-Q4 sub-class again: *NEAR by punctuation alone*, with no semantic difference at all. Q7 is
a new sub-class: **NEAR by limb-mark redistribution** — identical words, 6+4+6 against 6+5+5.
Neither is licence to re-author the question; both are licence to re-weight the answer.

> **The headline is not that the paper repeats. It is that four of the nine carry a temporal
> delta across the nineteen months, and three of those four are material.** "The same paper set
> twice" is true of the *questions* and false of the *answers*. A future session that treats
> QP2510 as a copy job will ship three legal errors.

---

## 4. Mandatory sitting-date sweep — all nine

Run per §14 of the production brief, on every question, regardless of what the intake flag said.
**The intake recorded `STABLE / LOW` on all nine with no classes and no notes. Three of those
nine are wrong.**

### Q1 — Big data. `STABLE`, with a live instrument the answer must use.

Nothing in the topic becomes false. But the **FAL Convention amendments making the Maritime Single
Window mandatory** for public authorities — adopted at FAL 46 (May 2022) — **entered into force
1 January 2024, two months before this sitting**. That is directly on limb (A)'s "port management"
and limb (B)'s integration barriers, and it is the single most citable dated fact available to the
question. An answer written without it is weaker but not wrong. *Not a flag correction; a research
instruction.*

### Q2 — Bill of lading. **`CORRECTED` — HIGH — Indian statute boundary.**

At the March 2024 sitting the governing Indian statutes are the **Indian Bills of Lading Act,
1856** and the **Indian Carriage of Goods by Sea Act, 1925**, the latter amended in 1993 to give
effect to the **Hague-Visby Rules**. Limb (c) asks the candidate to cite "relevant maritime laws
and conventions", so these are load-bearing.

**Both were repealed between the two sittings:**

| Repealing Act | Assent | Repeals |
|---|---|---|
| **Bills of Lading Act, 2025** (Act 18 of 2025) | **24 July 2025** | Indian Bills of Lading Act, 1856 |
| **Carriage of Goods by Sea Act, 2025** | **8 August 2025** | Indian Carriage of Goods by Sea Act, 1925 |

> **This is a NEW statutory boundary for the corpus.** Every Indian-statute finding so far has
> concerned the Merchant Shipping Act 1958 → 2025 boundary of 15 March 2026. This is a
> *different* pair of Acts crossing a *different* boundary in mid-2025 — and it sits **between**
> QP2403 and QP2510. The corpus-wide assumption that "every available 2024 and 2025 sitting
> predates 15 March 2026, so reuse runs backwards across one boundary" is **incomplete**.
> Commencement dates of the two 2025 Acts were not established and must be, before QP2510-Q2 is
> answered — assent is not commencement, as QP2508-Q5 established.

### Q3 — General average. `STABLE`.

The **York-Antwerp Rules 2016** are the current edition at both sittings, and which edition
applies is in any event a matter of contract, not of date. The **Marine Insurance Act, 1963** is
in force throughout. No instrument governing general average changed between March 2024 and
October 2025.

### Q4 — High-efficiency propellers. `STABLE`.

Pure engineering. The regulatory framing the stem uses — improving ship energy efficiency — rests
on EEXI and CII, in force **1 November 2022** and applying from **1 January 2023**, both before
this sitting. No propulsion-related instrument changed between the sittings.

### Q5 — Cyber risk. **`CORRECTED` — HIGH — guideline edition.** *(authored; see `Q5.md`)*

`MSC-FAL.1/Circ.3` has three editions and **the number of functional elements changes between
them**: Rev.2 (7 June 2022) has **five**; Rev.3 (4 April 2025) adds **Govern** for **six**.
Rev.2 governs this sitting. Separately, **IACS UR E26 and E27 were NOT in application** — the
original 1 January 2024 date was withdrawn and the revised requirements apply to ships contracted
for construction **on or after 1 July 2024**, four months after this paper.

### Q6 — Electronic record books. `STABLE`, confirmed not assumed. *(authored; see `Q6.md`)*

MEPC.312(74) is unrevised since 17 May 2019; the enabling MARPOL amendments have been in force
since **1 October 2020**. One residual `B_CURRENCY_CHECK`: Annex VI was revised by MEPC.328(76)
after the resolution was adopted, so the Annex VI regulation numbers are stated as the resolution
prints them.

### Q7 — III Code. `STABLE`, with an associated list re-issued three months before the sitting.

**A.1070(28) is unamended and is the Code at both sittings.** But the companion instrument moved:
**resolution A.1187(33), adopted 6 December 2023**, adopted the **2023 Non-exhaustive List of
Obligations under Instruments Relevant to the III Code**, replacing the 2021 version — **three
months before this sitting**. Material citing the 2021 list is superseded. The Code's own
paragraphs, which are what limbs (a) and (b) turn on, are unchanged.

### Q8 — Bridge control failure. `STABLE`.

An engineering and management scenario. The relevant SOLAS chapter II-1 machinery and
bridge-control provisions did not change between the sittings.

### Q9 — MLC 2006. **`CORRECTED` — HIGH — convention amendment in force between the sittings.**

At **March 2024** the amendments in force are:

| Amendments | In force | Subject |
|---|---|---|
| 2014 | 18 January 2017 | financial security — abandonment, death, long-term disability |
| 2016 | 8 January 2019 | harassment and bullying; validity of certificates |
| 2018 | 26 December 2020 | continued wages during captivity |

The **2022 amendments**, approved **6 June 2022** at the 110th session of the International
Labour Conference, **entered into force 23 December 2024 — nine months AFTER this sitting.**

> **Consequence for the model answer:** at March 2024, **social connectivity and internet access
> on board and in port, appropriately sized personal protective equipment, financial-security
> certificates in the name of the registered owner, and the obligation to investigate, record and
> report seafarer fatalities to the ILO are NOT MLC requirements.** They are approved amendments
> awaiting entry into force. Almost all currently available MLC material describes them as live.
>
> **Consequence for QP2510:** they **are** in force at the October 2025 sitting. This donor needs
> a **substantive legal update, not a re-anchor** — the QP2604-Q7 category, where the underlying
> law itself differs between the two sittings.

### Sweep summary

| Result | Questions |
|---|---|
| **Intake flag WRONG, corrected** | **Q2, Q5, Q9** |
| Stable, confirmed with a recorded reason | Q3, Q4, Q6, Q8 |
| Stable, but a dated instrument the answer must use | Q1, Q7 |

> **The intake temporal model is now 4 for 4 in failing to catch a real currency problem on a
> question it labelled `STABLE / LOW`** — QP2508-Q3, and now QP2403-Q2, Q5 and Q9. Three of the
> four were caught only because the sweep is mandatory. **The `temporal_review` field as
> populated at intake should be treated as unevaluated, not as evidence.** This is a
> corpus-level finding and belongs in the next Founder review.

---

## 5. Source-demand map — what each question needs

| Q | Demand classes | Primary authorities identified |
|---|---|---|
| Q1 | definition; sectoral application; evaluation of barriers | FAL Convention amendments (MSW, in force 1 Jan 2024); IMO e-navigation material; MSC-FAL.1/Circ.3/Rev.2 for the data-exposure counterpart; industry/ classification material for analytics practice — largely **outside the regulatory corpus**, expect `C_ACCEPTED_LIMITATION` |
| Q2 | definition; classification; legal obligation and citation | Hague-Visby Rules; Indian Carriage of Goods by Sea Act 1925 as amended 1993; Indian Bills of Lading Act 1856; Hamburg Rules and Rotterdam Rules for status only; Indian Sale of Goods Act 1930 for document-of-title effect |
| Q3 | principle; criteria; worked application | York-Antwerp Rules 2016 (Rules A, C, D, E, VI, X, XI, XVII, XX, XXII); Marine Insurance Act 1963; **Tier B support** from QP2607-Q5, QP2602-Q6, QP2606-Q3 |
| Q4 | engineering explanation; comparative merits | Authoritative technical/class material on ducted, Kappel, contra-rotating and azimuth propulsion; MARPOL Annex VI regs 22–28 (EEXI/CII) for the framing only. Expect **ENGINEERING_JUDGEMENT** to be the dominant class — no instrument prescribes propeller type |
| Q5 | enumeration; definition; evaluation; distinction | **MSC-FAL.1/Circ.3/Rev.2 — read in full**; MSC.428(98) — **DONE** |
| Q6 | enumeration; compliance mechanism; security | **MEPC.312(74) — read in full** — **DONE** |
| Q7 | objective; strategy; scope; performance indicators; tri-partite responsibilities | **A.1070(28) — read in full** (paras 1, 3, 6, 7, 15–17, 42–44, 45–51, 52–63); A.1187(33) for the obligations list; IMSAS mandatory 1 January 2016 |
| Q8 | fault diagnosis; temporary measure; permanent measure; CE report format | SOLAS II-1 machinery and bridge-control provisions; ISM Code 10 (maintenance) and 9 (non-conformity reporting); class survey requirements; engineering judgement on remote-control system failure modes |
| Q9 | provisions by Title; enforcement mechanism; critical evaluation | MLC 2006 Titles 1–5 as amended to **2018 only**; DMLC Parts I and II; Title 5 enforcement; MLC Regulation 5.2.1 port State inspection; ILO/IMO material on enforcement gaps |

---

## 6. Research-once record for the QP2510 handover

For each authored question, the reusable base and the boundary are recorded in the question's own
verification file (`Q5.md` §5, `Q6.md` §6) rather than in a duplicate answer object, per §35 of
the production brief. **The QP2403 canonical object itself is the future donor.**

**Do not mark QP2510 built.** A donor is not a solved target.
