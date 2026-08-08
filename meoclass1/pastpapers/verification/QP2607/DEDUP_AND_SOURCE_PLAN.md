# QP2607 — Dedup and source plan (Q1–Q9)

Paper: QP-2607, July 2026, Engineering Management, MEO Class I.
Assessed: 2026-08-07. Status: **Dedup Assessed**.

Reuse tiers per the brief:
**A** canonical deep-dive reuse · **B** partial repository reuse, synthesis required ·
**C** new production · **D** existing past-paper answer reuse.

---

## 0. Findings that apply to the whole paper

**No question can be Tier D.** `meoclass1/pastpapers/` has never contained a built paper — only
`docs/`. There is no prior past-paper answer to recur from, for any question, regardless of what the
recurrence table shows. Tier D first becomes available once a second paper is built.

**Recurrence metadata is not evidence of semantic equivalence** and has not been treated as such. Q3,
Q5 and Q9 carry prior-sitting codes; none of those sittings exists on the platform, so the codes tell
us only that the topic is a repeat favourite.

**`Notes-for-written-answers/` is scope evidence only, never a source.** 45 PDFs, 767 pages, audited
in full. Two distinct HATC coaching sets: a machine-readable *Additional Set October 2024* (325 pages)
and an image-only *June 2025* set. Every one of the 325 text pages carries the publisher's own line,
"Certain statements/figures have been intentionally made wrong; same will be corrected in class"
(occurrence count verified: 325/325). It is also third-party copyright material and watermarked.

Its genuine value is structural: the June 2025 set is organised **by past-paper question**, so it maps
questions to topics. Example: its Casualty Investigation page reproduces the QP2601 Q8 stem verbatim.
Use it to know what is examined. Never to know what is true.

One exception in that folder: `DOC-20251125-WA0009.pdf` is **IRS Guidelines on Ballast Water
Management 2018 (IRS-G-ENV-01)** — genuine classification-society material, and citable. Irrelevant to
this paper; recorded so it is not lost.

**Notes coverage of this paper's topics is thin.** Searching all 325 machine-readable pages:
`iron ore`, `pellet`, `IMSBC`, `liquefaction`, `moisture limit`, `dynamic separation`, `bunker
overflow`, `Merchant Shipping Act 2025`, `green ammonia`, `average adjuster`, `Uberrimae` → **zero
hits each**. `SOPEP` 9, `Oil Record Book` 9, `formal safety assessment` 2, `fuel cell` 14.

**Marks.** Every question is 16 marks (8+8 for Q1, Q3, Q8). Six answered × 16 = 96 against a printed
"Total Marks – 100". The discrepancy is on the paper. Recorded as printed; not normalised.

---

## Q1 — Formal safety assessment; iron ore pellets loading and carriage

**Exact topic.** (a) application of FSA to loading/carriage of iron ore pellets in bulk (8);
(b) specific carriage and voyage monitoring requirements for iron ore pellets (8).

**Command verbs and required components.** *Discuss* — FSA methodology, its actual locus of
application, and how it reaches this cargo. *What are* — an enumerable list of carriage and
voyage-monitoring requirements, cargo-specific.

**Repository files actually inspected (content read, not tag-matched):**
`meoclass1/QB8_A.html`, `QB8_E.html`, `QB2_A.html`, `QB2_B.html`, `QB5_I.html`,
`meoclass1/oralnotes/miw-notes-mgmt-p14.html`, plus grep across all `meoclass1/**/*.html`.

**Usable canonical content.** IMSBC Group A/B/C/MHB framework is well established in `QB8_A`
(60-second answer on groups, cargo schedules, hold bilge tracking) and `QB8_E` (IMSBC vs BLU Code vs
Grain Code distinction — directly reusable). `QB2_A` carries Group A/B/C definitions with examples.
FSA is named in `QB2_B` and `QB5_I` but not developed.

**Missing content — and the trap.** The corpus consistently uses **iron ore *fines*** as its Group A
worked example. The question asks about **pellets**, which are **Group C**. There is zero
pellet-specific content anywhere on the platform. A tag-level dedup would score this "covered" and
produce a wrong answer. Additionally, `DIRECT REDUCED IRON (B) — lumps, **pellets**, cold-moulded
briquettes` is a Group B schedule, so the word "pellets" alone is ambiguous — the BCSN governs.

**Verification sources needed / used.** MSC-MEPC.2/Circ.12/Rev.2 (obtained, read in full); IMO Bulk
Carrier Safety and the *Derbyshire*→MSC 76→SOLAS XII chain; SOLAS XII/11 and XII/12; IMSBC via SOLAS
VI/VII; ISM 1.2.2.2; amendment currency 07-23 vs 08-25.

**Regulatory freshness risk: MEDIUM.** Amendment 08-25 is voluntary from 1 Jan 2026, mandatory
1 Jan 2027 — i.e. it straddles this sitting. Both states and dates are given in the answer.

**Reuse tier: B.** **Recommendation:** build in the pilot. Done.

---

## Q2 — Bunker overflow in foreign waters; Chief Engineer's response

**Exact topic.** Chronological CE response across containment, documentation, mandatory local
reporting, cooperation with investigators, and liability exposure.

**Command verbs.** *State in systematic detail* — this is an ordered-procedure question. Marks follow
sequence and completeness, not depth on any one item.

**Repository files actually inspected.** `meoclass1/QB9_E.html` (the single `bunker overflow` hit in
the entire corpus — a CLC/Bunkers aside inside a liability card), `QB4_G.html`, `QB9_A.html`,
`QB3_C.html`, `QB3_G.html`, `QB4_B.html`.

**Usable canonical content.** Verified components exist and are reusable as facts: SOPEP references,
ORB discipline, Bunker Delivery Note, CLC exemptions, P&I involvement, coastal-State concepts. `QB9_E`
already makes the correct point that logbooks, bunkering checklists and sounding logs get legally
sequestered.

**Missing content.** No consolidated chronological incident-response answer exists. The pieces are
scattered across nine files in oral-card format, which does not translate to a 16-mark written
sequence. Synthesis is the whole job here.

**Verification sources needed / used.** MARPOL Annex I regs 17 and 37 + appendix III code letters
(obtained verbatim); MARPOL art. 8 / Protocol I; res. A.851(20); MARPOL Annex VI reg 18; Bunkers
Convention 2001 (IMO primary); Casualty Investigation Code MSC.255(84); fair-treatment res. LEG.3(91)
and A.1056(27); OPRC 1990; ISM 8 and 9.

**Regulatory freshness risk: LOW.** All instruments are long in force and stable.

**Reuse tier: B, at the C boundary.** **Recommendation:** build in the pilot. Done.

---

## Q3 — IACS structure; UI/UR/PR; Recognized Organizations and the RO Code

**Command verbs.** *Enumerate* (structure), *explain difference* (UI vs UR vs PR), *does it have
significance* (a judgement call requiring a reasoned yes), *what is / what are / how do* (RO Code).

**Overlaps found.** Strongest reuse in the paper. `IACS` in 94 files; `Recognized Organization` 36;
`RO Code` 24 (incl. `QB4_C`, `QB1_B_CheatSheet`); `Unified Requirement` 32. Oral notes
`miw-notes-mgmt-p7.html` is titled *Port State Control, Classification Societies & IACS*.

**Missing.** The precise UI/UR/PR distinction needs care — these are routinely conflated. Needs
IACS-primary confirmation, plus the RO Code's dual MSC/MEPC adoption and its Part 1/2/3 structure.

**Freshness: LOW.** **Tier B (strong).** Production order: **2nd**.

---

## Q4 — ECA entry; fuel changeover for boilers and engines; statutes

**Command verbs.** *Explain with justification* (the justification carries marks — thermal shock,
viscosity control, changeover time/volume calculation), *enumerate the statutes*.

**Overlaps found.** `changeover` 31 files, `fuel changeover` 15, `Emission Control Area` 12,
`Annex VI` 76. `QB3_E`, `QB3_F`, `QB4_C`, `QB4_E` carry the operational content.

**Missing.** Boiler-specific changeover guidance is thinner than engine-side. The "statutes" limb needs
MARPOL Annex VI reg 14 plus the written changeover procedure and record-keeping obligation, and any
regional overlay must be flagged as regional rather than IMO.

**Freshness: LOW–MEDIUM.** **Tier B.** Production order: **5th**.

---

## Q5 — Particular Average, General Average, declaration, average adjusters

**Command verbs.** *Explain the concepts*, *what are the circumstances*, *who are / what is their
role*.

**Overlaps found.** `General Average` 21 files, `Particular Average` 7, `York-Antwerp` 19,
`average adjuster` 9 — `QB9_A`, `QB9_C` + CheatSheet, `QB1_B`, `QB9_F`. Oral notes
`miw-notes-mgmt-p12.html` covers Salvage/LOF/SCOPIC, Port of Refuge and GA. HATC notes: `General
Average` 12, `Particular Average` 11.

**Missing.** Which York-Antwerp Rules edition to cite, and the Rule A definition of a general average
act. Recurs from 2023/APR/Q3 and 2025/SEP/Q3 — neither built.

**Freshness: LOW.** **Tier B (strong) — the closest thing to Tier A in this paper.**
Production order: **1st.**

---

## Q6 — Green ammonia as a zero-carbon fuel; ICE versus fuel cells

**Command verbs.** *Evaluate* (requires a balanced judgement, not a description), *what are the
primary challenges* across safety, storage and combustion, with an explicit ICE-vs-fuel-cell contrast.

**Overlaps found.** `ammonia` 32 files, `green ammonia` 10 (`QB5_G`, `QB6`, `QB7_D`), `IGF Code` 24.

**Missing.** `fuel cell` appears in only 2 HTML files — the comparative half of the question is the
weak side. Needs the IGF Code / interim ammonia-fuel guidelines position, toxicity and
N₂O slip.

**Freshness: HIGH.** Ammonia-fuel regulation is actively developing; legal stage must be stated
explicitly for anything not yet in force. **Tier B.** Production order: **6th**.

---

## Q7 — Merchant Shipping Act 2025

**Command verbs.** *Explain the significance*, specifically as to trade and tonnage expansion, foreign
investment, and India's maritime standing.

**Overlaps found.** `Merchant Shipping Act, 2025` 28 files, `MS Act` 44, `DGMA` 38 — already tracked
in project memory as a live transition.

**Missing.** HATC notes have **zero** hits for the 2025 Act — they predate it entirely, so the usual
scope signal is absent for this question. Every consequential claim needs current primary
verification: commencement status, which provisions are notified, whether DGMA is constituted.

**Freshness: 🔴 HIGHEST IN THE PAPER.** **Tier B, but treat the verification as if Tier C.**
Production order: **9th — last, and re-verify immediately before publication.**

---

## Q8 — Competence versus performance; automation and the human element

**Command verbs.** *Explain the difference*, *discuss the role of* training and drills, *discuss
positive and negative effects* — the (b) limb explicitly demands both sides.

**Overlaps found.** `human element` 27 files, `competence` 39, `drills` 62, `automation` 44. `QB5_I`
is tagged `human-element`; `QB5_A/B/C/D/E` are the Management, Leadership & Human Element series. HATC
notes: `human element` 18, `competence` 17.

**Missing.** The competence-versus-performance distinction itself is conceptual and largely absent as
a named contrast; STCW competence tables plus ISM 6 (resources and personnel) supply the frame.

**Freshness: LOW.** **Tier B.** Production order: **4th**.

---

## Q9 — Uberrimae Fidei; disclosure; consequences of non-disclosure

**Command verbs.** *Explain the principle*, *what are the different disclosures*, *list the
circumstances which need not be disclosed*, *what happens to the contract*.

**Overlaps found.** `Uberrimae` 10 files (`QB9_C` + CheatSheet, `QB9_E`), `utmost good faith` 9,
`Marine Insurance Act` 14. The four-part structure maps cleanly onto existing cards.

**Missing.** Which statute governs — the UK Marine Insurance Act 1906 versus the Indian Marine
Insurance Act 1963 — and whether the UK Insurance Act 2015 reform of the avoidance remedy is to be
mentioned. This must be resolved before drafting; it changes the fourth limb's answer materially.
Recurs from 2022/OCT/Q2 and 2024/JAN/Q1 — neither built.

**Freshness: MEDIUM** (only because of the 2015 reform question). **Tier B (strong).**
Production order: **3rd**.

---

## Recommended production order

| Order | Q | Rationale |
|---|---|---|
| — | Q1, Q2 | Pilot, built |
| 1 | Q5 | Highest reuse, lowest risk, cleanest four-part structure |
| 2 | Q3 | Very high reuse; one precision check (UI/UR/PR) |
| 3 | Q9 | High reuse; resolve governing-statute question first |
| 4 | Q8 | Good reuse; conceptual framing to build |
| 5 | Q4 | Good reuse; boiler-side gap to fill |
| 6 | Q6 | Thin on the fuel-cell half; volatile |
| 7 | Q7 | Most volatile; no notes coverage; verify last and re-verify at publication |

Q1 and Q2 were built first because the brief specified them, not because they were the cheapest. On
reuse economics alone they are among the more expensive questions in the paper — Q1 in particular
required research the corpus could not supply.

---

## Standing recommendation

Acquire a licensed copy of the **IMSBC Code (2023 edition, amendment 07-23)** and of the **2025
edition (08-25)**. Q1 could not be finished to primary-source standard for the individual schedule's
characteristics table, and every future cargo question in this series will hit the same wall.

---

## Production checkpoint — 2026-08-08

All nine questions built. Status: **Pilot Review Ready**, ungated, uncommitted.

| Batch | Q | Tier | Reuse outcome |
|---|---|---|---|
| Pilot (red-teamed) | Q1 | B | IMSBC framework reused; pellet-specific content built new. Group C claim held at P2, not P1 |
| Pilot (red-teamed) | Q2 | B | Components reused as facts; chronological structure built new. Two Critical legal corrections applied |
| A | Q5 | B | Strongest reuse in the paper — Rule A, GA security mechanics and the PA/GA contrast came from QB9_A |
| A | Q9 | B | Conceptual frame reused; **all statutory citations rejected and re-derived** — QB9_C cites the UK 1906 Act |
| A | Q3 | B | Topic well covered internally, but the UR/UI/PR distinction was nowhere stated precisely; verified against IACS |
| B | Q8 | B | Human-element material plentiful; the competence/performance contrast had no internal basis |
| B | Q4 | B | Changeover content reused; boiler-side and reg 14.6 recording verified externally; ECA list newer than the corpus |
| C | Q6 | B | Ammonia covered, but `fuel cell` appeared in only 2 files — the comparative half was built from scratch |
| D | Q7 | B on paper, **verified as Tier C** | Repository explicitly not used as legal authority. Two items remain unresolved |

**Reuse economics, honestly.** Tier B was correct for all nine, but "B" spanned a wide range: Q5
reused substantial verified content, while Q6 and Q7 were effectively new production. Tier D never
became available — no prior sitting exists on the platform. The single most valuable reuse was not
content at all but **structure**: once the pilot's answer shape was fixed, later questions drafted
considerably faster.

**Two internal-content defects found by reuse screening**, both of which would have propagated:
`QB9_C` cites the UK Marine Insurance Act 1906 for an Indian-law topic, and the corpus consistently
teaches iron ore *fines* as the Group A exemplar without noting the conditional Group C route.

**Blocking before publication:** Q7's commencement scope and provision-level citations; Q6's ammonia
regulatory status. Seven claims across the paper carry `reverify_before_publication` flags.
