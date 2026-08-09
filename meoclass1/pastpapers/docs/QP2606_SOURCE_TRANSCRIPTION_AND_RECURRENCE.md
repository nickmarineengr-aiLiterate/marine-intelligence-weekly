# QP2606 — JUNE 2026 · SOURCE TRANSCRIPTION AND RECURRENCE ANALYSIS

**Status: PRODUCTION IN PROGRESS — transcription and recurrence COMPLETE, authoring INCOMPLETE.**
Opened 2026-08-09 on branch `pastpapers/qp2606-founder-review`, created from `5744143` (QP2604 completion).

> This document is the durable, resumable record of the June session's completed phases.
> **QP2606 is NOT built.** No `specs/QP2606.json` exists, no page is generated, and the
> toolchain still reports five papers. §7 states precisely where a following session resumes.

---

## 1. Source copy

| | |
|---|---|
| File | `meoclass1/pastpapers/docs/06- JUNE - 2026.pdf` (git-ignored, local only) |
| Filename anomaly | **`06- JUNE - 2026.pdf`** — no space after `06`. Every other file in the set uses `NN - MONTH - 2026.pdf`. Recorded, not renamed. |
| Pages | 2 |
| Size | 303,840 bytes — sized like July (303,258), not like Jan–Apr (~200–208 KB) |
| Printed serial | `Sr. No. EM – 2606-1` (en dash U+2013; **carries the `-1` suffix**, as April does) |
| Transcription verified | **Yes** — extracted with PyMuPDF and checked character-by-character against both pages rendered at 150 dpi |

### 1a. CORRECTION TO A PREVIOUSLY RECORDED FACT — PDF generation dates

`CURRENT_STATUS.md` §2d and the March session record state that the source copies' PDF metadata
records **"only 20 April 2026 — the date the third-party host batch-generated *all six* 2026 files"**.

**That is wrong.** Measured this session across all six files:

| File | PDF creationDate |
|---|---|
| 01 - JANUARY - 2026.pdf | 2026-04-20 17:19:38 +05:30 |
| 02 - FEBRUARY - 2026.pdf | 2026-04-20 17:15:29 +05:30 |
| 03 - MARCH - 2026.pdf | 2026-04-20 17:15:46 +05:30 |
| 04 - APRIL - 2026.pdf | 2026-04-20 17:14:44 +05:30 |
| **06- JUNE - 2026.pdf** | **2026-06-18 17:51:55 +05:30** |
| **07 - JULY - 2026.pdf** | **2026-07-21 13:14:55 +05:30** |

The 20 April 2026 batch covers **four** files, not six. June and July were each generated
separately, within weeks of their own sittings.

**Why this matters, and why it is not more than it looks.** The host generation date is an
*upper bound* on the sitting date, not the sitting date. It establishes only that the June paper
existed in the host's hands by **18 June 2026**. It does **not** establish when the examination
was sat, and no examination date is printed on the copy. The March conclusion — that the sitting
date cannot be established from the copy — **still stands for January to April**. For June and
July the upper bound is materially tighter than the March note implied.

Found by measuring rather than by carrying the previous statement forward. This is the second
stale figure the register has produced (April found the QP2607 word-count row), and the same
lesson applies: **derive, do not transcribe.**

---

## 2. Paper-level transcription

| Field | Value as printed |
|---|---|
| Month/year | JUNE 2026 |
| Serial | `EM – 2606-1` |
| Examination | EXAMINATION OF MARINE ENGINEER OFFICER |
| Function | Marine Engineering Management at Management Level |
| Subject | ENGINEERING MANAGEMENT |
| Class | `M.E.O CLASS – I` |
| Time allowed | `TIME ALLOWED - 3 HOURS` (plain hyphen here; en dash elsewhere) |
| Total marks | `Total Marks – 100` |
| Region note | `(India 2026)` |
| Questions offered | 9 |
| Questions to answer | 6 |

**NB, verbatim, four items:**

```
1. Answer SIX questions only.
2. All questions carry equal marks.
3. Neatness in handwriting and clarity in expression carries weightage
4. Blank pages if any, to be struck by (X) at the end of each question.
```

Item 3 has no terminating full stop, and reads "carries weightage" against the plural subject
"Neatness … and clarity". Preserved as printed.

### 2a. THE 96-VERSUS-100 DISCREPANCY — now 6/6

Six questions × 16 marks = **96**, against a printed **Total Marks – 100**, with instruction 2
stating all questions carry equal marks. **Present, and recorded as printed, not normalised.**

**At 6/6 this is a settled property of the paper series across the whole available 2026 set.**

### 2b. PRINTED MARKS — a fifth distinct pattern, and the cleanest in the set

| Q | Printed allocation | Sum |
|---|---|---|
| Q1 | a) (8) · b) (8) | 16 |
| Q2 | a) (8) · b) (8) | 16 |
| Q3 | a) (8) · b) (8) | 16 |
| Q4 | a) (8) · b) (8) | 16 |
| Q5 | a) (8) · b) (8) | 16 |
| Q6 | (16) against the whole question, no limbs | 16 |
| Q7 | a) (8) · b) (8) | 16 |
| **Q8** | **a) (10) · b) (6)** | **16** |
| Q9 | (16) against the whole question, no limbs | 16 |

**All nine questions print a mark allocation, and all nine sum to exactly 16.**

This is a **new pattern class**. The series to date:

| Paper | Questions printing an allocation | Internal arithmetic |
|---|---|---|
| QP2607 | most | consistent |
| QP2601 | 2 of 9 | consistent |
| QP2602 | 6 of 9 | consistent |
| QP2603 | 3 of 9 | consistent |
| QP2604 | **9 of 9** | **Q6 prints 5+5+5+5 = 20 against a 16-mark question** |
| **QP2606** | **9 of 9** | **all nine sum to 16 — no anomaly** |

June is the **only paper in the set that prints marks on every question AND has no internal
arithmetic conflict.** April printed marks on every question but contradicted itself on Q6.

**Q8's 10 + 6 is the only unequal two-limb split in the June paper**, and the only 10/6 split
in the set outside the FSA/lithium-battery question (QP2602 Q3, QP2603 Q8, QP2604 Q2).

The register's standing conclusion — *"there is no series convention for printed marks; read
them off the rendered page every time"* — is unchanged and now rests on 6/6.

### 2c. Grammar, spelling and typographic anomalies — preserved, not corrected

| Q | Anomaly as printed | Note |
|---|---|---|
| Q2 b) | "What are **the right to appeal** available to you" | Ungrammatical; singular "right" against "are"/"available" |
| Q3 a) | "**York Antwerp** Rules 1994" | No hyphen. The instrument is the **York-Antwerp Rules**. |
| Q3 a) | "Define **General Average Act** as per York Antwerp Rules 1994?" | Declarative task punctuated as a question |
| Q3 a) | `“General Average”` | **Curly** quotes (U+201C/U+201D) |
| Q7 a) | `"Lakshadweep islands"` … `"Andaman and Nicobar Islands'` | **Straight** double quote opens, **straight apostrophe** closes (U+0022 … U+0027) — mismatched. Also lowercase `islands` against capitalised `Islands`. |
| Q7 b) | `"Particularly Sensitive Sea Area"` | Straight doubles (U+0022) |
| Q8 a) | "SOLAS **ch.ll-1**" | **Two lowercase L's** (U+006C U+006C), not Roman numeral II. Confirmed by codepoint inspection and on the render. The intended reference is **SOLAS chapter II-1**. |
| Q1, Q4 | "emphasizing", "decarbonization", "optimizing" | -ize spellings |
| Q6 | "Chief Engineer’s" | Curly apostrophe (U+2019) |

**Two different quotation conventions appear on the same paper** — curly in Q3, straight in Q7.

> **STANDING RULE, unchanged.** These are recorded as printed. A future session must not
> "fix" `ch.ll-1`, the missing hyphen in York-Antwerp, or the mismatched quote in Q7.

---

## 3. Host-printed recurrence table — DISCOVERY ONLY

Captured verbatim as metadata. **It is not evidence of semantic equivalence** (standing rule,
5/5 before this paper; see §5b for how it performed on June).

| Q | Host entries |
|---|---|
| Q1 | 2023/DEC/Q1 |
| Q2 | 2023/DEC/Q2 |
| Q3 | 2023/DEC/Q3 |
| Q4 | 2023/DEC/Q4 |
| Q5 | 2023/DEC/Q5 · 2024/AUG/Q9 |
| **Q6** | **2015/FEB · 2016/AUG · 2016/SEP · 2016/NOV · 2017/JAN · 2017/JAN · 2017/SEP · 2018/SR09 · 2018/OCT · 2018/DEC · 2019/FEB · 2019/APR · 2021/FEB/Q1 · 2022/FEB/Q2 · 2023/DEC/Q6 · 2024/FEB/Q6** |
| Q7 | 2017/AUG · 2023/DEC/Q7 · 2025/FEB/Q9 |
| Q8 | 2022/OCT/Q5 · 2023/APR/Q9 · 2023/DEC/Q8 · 2024/DEC/Q4 · 2025/SEP/Q9 |
| Q9 | 2022/APR/Q7 · 2022/AUG/Q9 · 2023/JUL/Q6 · 2023/DEC/Q9 |

(Each row also carries its own `2026/JUN/Qn` self-reference, omitted above.)

**Two observations, both descriptive.**

1. **The host claims every one of the nine June questions repeats the December 2023 paper at the
   same question number** — Q1↔Q1, Q2↔Q2 … Q9↔Q9. If true this would make June a systematic
   re-issue of 2023/DEC, structurally the same phenomenon April showed against January. **It is
   unverifiable here**: the December 2023 paper is not in the source set, so this is recorded and
   left alone. It is *not* used to classify anything.
2. **Q6 carries 16 prior sittings back to February 2015 — the most-repeated question in the whole
   source set**, by a wide margin. And yet (see §5) it has **no relationship whatever to any of
   the 45 questions already built.** High historical repetition and 2026-set recurrence are
   independent properties.

---

## 4. Verbatim stems

Transcribed with limbs joined by a single space, printed limb refs and printed marks preserved
exactly, wrapped lines joined with a single space. These are the strings used for §5.

- **Q1** — Goal-based ship construction standards (GBS) for bulk carriers and oil tankers:
  concept and significance (8); implementation process and stakeholder involvement (8).
- **Q2** — Port State Control: the concept with focus on the legal framework (8); right of
  appeal available to the Chief Engineer or the Company on an unreasonable/unfair detention (8).
- **Q3** — Types of losses in marine insurance; General Average Act per York Antwerp Rules 1994;
  circumstances for declaring General Average (8); express versus implied warranties in a hull
  and machinery policy (8).
- **Q4** — Need to upskill and train seafarers in the decarbonization scenario (8); effective
  communications as a causal factor in maritime accidents, in present-day crewing (8).
- **Q5** — Role of the SMS in implementing the ISM Code, components and continuous improvement
  (8); evolution of the ISM Code against technological advancement, cyber risk and environmental
  sustainability (8).
- **Q6** — Capital, voyage and operating costs; the Chief Engineer's role in optimizing them;
  modern management principles used in inventory control (16).
- **Q7** — How the Lakshadweep and Andaman & Nicobar islands could be protected from marine
  pollution (8); the term "Particularly Sensitive Sea Area" and the criteria for identification
  and designation of a PSSA (8).
- **Q8** — Role of classification societies in structural, mechanical and electrical rule
  formation and implementation, and why compliance with Class rules is now mentioned in SOLAS
  ch.ll-1 (10); difference and relevance of annual versus periodical surveys towards the
  harmonized survey and certification system (6).
- **Q9** — Formal Safety Assessment: objectives, characteristics and processes, with specific
  explanation of Hazard Identification, Risk Analysis and Cost Benefit Assessment (16).

The exact strings are held in
`<scratchpad>/june_stems.py` for the authoring session and must be re-transcribed into
`specs/QP2606.json` `text_verbatim` unchanged.

---

## 5. RECURRENCE — June against all 45 previously built questions

Method, following the standing rule that **the similarity ratio surfaces candidates and a
task-by-task comparison classifies them**:

1. `difflib.SequenceMatcher` ratio of each June stem against all 45 built `text_verbatim` strings.
2. A concept-level term scan of all 45 stems for each June question's subject vocabulary.
3. Human adjudication of examiner demand, limb by limb.

### 5a. Result

**EXACT 0 · NEAR 0 · TOPIC 4 · NONE 5.**

| June Q | Class | Related to | Evidence and reasoning |
|---|---|---|---|
| Q1 GBS | `new` | — | Best ratio 0.2543 (structural noise). **No prior stem contains "goal-based", "GBS" or "common structural".** Adjacent to QP2607 Q3 on class rule-making, but no shared examiner task. |
| Q2 PSC | `new` | — | Best ratio 0.2537. **No prior stem contains "port State control", "detention", "detained" or "deficienc-".** |
| Q3 losses / GA / warranties | `topic_recurrence` | **QP2607 Q5** (primary); QP2602 Q6; QP2601 Q3 / QP2604 Q3; QP2607 Q9 | See 5c — the ratio ranked the **wrong** neighbour. |
| Q4 training / communications | `topic_recurrence` | QP2601 Q2; QP2607 Q8; QP2602 Q8 | See 5d — contains a **homonym trap**. |
| Q5 ISM / SMS | `new` | — | The only prior "ISM"/"SMS" hits are the substrings inside **"mechanism"** and **"mechanisms"** in QP2601 Q7 and QP2604 Q7. **Zero genuine relationship.** |
| Q6 costs / inventory | `new` | — | Ship economics and inventory control are absent from the corpus. The only term hits are the words "voyage" and "operating" used in unrelated senses. |
| Q7 PSSA / Indian islands | `new` | — | No prior PSSA or area-designation question. QP2607 Q4 concerns an **Emission Control Area** but sets an operational fuel-changeover task, not designation criteria. |
| Q8 class societies / surveys | `topic_recurrence` | **QP2607 Q3** (primary); QP2603 Q6 | Shares class rule-making and the RO; adds SOLAS II-1/3-1 and the HSSC survey types. |
| Q9 FSA method | `topic_recurrence` | QP2602 Q3 / QP2603 Q8 / QP2604 Q2; QP2607 Q1 | Four prior FSA questions, **all of them applications**; June asks for the **method itself**. |

### 5b. A THIRD DISTINCT RECURRENCE PROFILE

| Paper | EXACT | NEAR | TOPIC | NONE |
|---|---|---|---|---|
| QP2603 March | 3 | 0 | 5 | 1 |
| QP2604 April | 0 | 7 | 1 | 1 |
| **QP2606 June** | **0** | **0** | **4** | **5** |

**June is the first paper in the set with neither an exact nor a near recurrence**, and it carries
**five genuinely new questions — more than the previous five papers produced between them** (the
set held nine `new` across 45 questions before June, and no single paper contributed more than one
`NONE`).

Consequence for production: **June has ZERO Tier D reuse.** Every prior paper since February
carried at least one. The dedup tiers are **C ×5 (Q1, Q2, Q5, Q6, Q7) and B ×4 (Q3, Q4, Q8, Q9)**,
with **no Tier A and no Tier D**. This makes June the most expensive paper in the set to author
and is the principal reason it is not complete in one session.

**The host table's 2026 silence was correct for the first time** — it lists no other 2026 sitting
against any June question, and independent comparison agrees there is no exact or near repeat
within the 2026 set. It remains **under-claiming** on the topic relationships (it records nothing
of Q3↔QP2607 Q5 or Q9↔the three FSA questions), so the standing rule is unchanged: the host table
establishes topic recurrence only, and here it did not even do that.

### 5c. NEW FAILURE MODE — the ratio ranked the wrong neighbour

April established that the ratio is **length-sensitive** (a low score can hide a task-for-task
match). June adds a distinct failure:

> **June Q3's highest-scoring prior question (QP2601 Q3, 0.3080) is not its real relative.**

Its actual relative is **QP2607 Q5**, which scores *lower*, but which contains a near-verbatim
shared task:

| | |
|---|---|
| QP2607 Q5 | "What are the **circumstances when a general average can be declared**?" |
| QP2606 Q3 a) | "State the **circumstances under which "General Average" can be declared**?" |

QP2607 Q5 also sets "Particular Average" and "General Average" as concepts, which is what June
Q3 a)'s "types of losses in marine insurance" resolves to. QP2601 Q3 — the top scorer — is a
**salvage law** question that merely contains the phrase "General Average".

**The score was non-zero, confidently ranked, and pointed at the wrong target.** A session
ranking by score alone would have reused salvage content for an averages question.

June Q3 is nonetheless **TOPIC and not NEAR**: only one of its four tasks maps cleanly, limb b)
(express versus implied warranties) is new subject matter, and the average adjusters task is
dropped. **Reuse is available at limb level, not question level.**

### 5d. NEW SUB-CLASS — a shared word that is a homonym

**QP2601 Q2 and QP2606 Q4 both contain "decarbonisation"/"decarbonization" and both contain
"communication". They are not the same subject.**

| | QP2601 Q2 | QP2606 Q4 a) |
|---|---|---|
| "decarbonisation" means | **main engine decarbonisation** — the maintenance job of removing carbon deposits, worked on the cylinder head platform and the bottom platform | **decarbonisation of shipping** — the energy transition, alternative fuels, GHG reduction |
| the task | identify communication-failure hazards in a two-group engine overhaul and mitigate them | discuss the need to upskill and train seafarers, citing anticipated areas of concern |

The genuine overlap between the two questions is **communication** (QP2601 Q2 defines it,
enumerates types and discusses barriers; June Q4 b) treats it as a causal factor in accidents),
plus **training and competence** shared with QP2607 Q8. The decarbonisation token is a false
friend.

> This is AGENT_LESSON 2 — *"tag-level dedup is unsafe; read the matched content"* — reappearing
> at **stem** level rather than tag level. A keyword-driven reuse step would have merged a
> planned-maintenance question with an energy-transition question.

---

## 6. VERIFICATION COMPLETED SO FAR

Primary sources actually opened and read this session. **This covers Q1 and Q2 and the paper-wide
temporal anchors only.** Q3–Q9 are not verified.

### 6a. Sitting-date truth for June 2026

June 2026 falls **after the 15 March 2026 commencement of the Merchant Shipping Act 2025**
(S.O. 1244(E), read in the Gazette during the QP2607 session). Any Indian statutory limb must be
answered on the 2025 Act unless a specialist statute governs — and the standing warning applies
that **not every Indian maritime subject falls under it** (the Recycling of Ships Act 2019 and the
Indian Ports Act 1908 framework both survived on earlier papers). **Q7 is the June question where
this must be worked**, and it is not yet done.

**The IMO Net-Zero Framework was still APPROVED BUT NOT ADOPTED at the June 2026 sitting.**
The extraordinary MEPC session convened in October 2025 adjourned on 17 October 2025 by vote
(57–49, 21 abstentions) and **reconvenes 16–27 November 2026** — five months *after* the June
sitting — with the adoption of the revised Net-Zero Framework and the designation of the
North-East Atlantic as a SOx/PM/NOx ECA both on its agenda. February's headline finding therefore
**holds unchanged at the June sitting**, and this is the fourth paper on which it bites.
**Relevant to Q4 a).** `B_CURRENCY_CHECK` — the November 2026 session may change it.

### 6b. Q1 — Goal-Based Standards · PRIMARY VERIFIED

Read in full: **resolution MSC.287(87)**, *Adoption of the International Goal-based Ship
Construction Standards for Bulk Carriers and Oil Tankers*, adopted 20 May 2010 (9 pp.).

- **SOLAS regulation II-1/3-10** was adopted by **resolution MSC.290(87)** and, with the
  definition in **II-1/2.28**, entered into force **1 January 2012**. The Standards took effect on
  the same date.
- **Application: bulk carriers and oil tankers of 150 m in length and above, for which the
  building contract is placed on or after 1 July 2016.**
- **THE TIER DISTINCTION — this is the discrimination the question rewards, and secondary
  sources get it wrong.** MSC.287(87) §1.5 records that MSC agreed to use a **five-tier system**
  (I Goals · II Functional requirements · III Verification of conformity · IV Rules and
  regulations for ship design and construction · V Industry practices and standards). But §3
  STRUCTURE states: *"These Standards consist of the following **three** tiers: Tier I, Tier II,
  Tier III."* **The framework is five tiers; the instrument contains three.** Tiers IV and V are
  the class/national rules and industry practice that sit beneath it.
  > **An automated summary of this same PDF asserted a "four-tier hierarchical framework". It is
  > neither five nor three — it is simply wrong.** Sixth consecutive paper on which opening the
  > source caught a substantive error.
- **Tier I goal, exact wording:** *"Ships shall be designed and constructed for a specified design
  life to be safe and environmentally friendly when properly operated and maintained under the
  specified operating and environmental conditions, in intact and specified damage conditions,
  throughout their life."* With .1 safe and environmentally friendly (adequate strength, integrity
  and stability), .2 constructed of materials for **environmentally acceptable recycling**,
  .3 safe access, escape, inspection and proper maintenance, .4 specified operating and
  environmental conditions, .5 specified design life.
- **Tier II — fifteen functional requirements in four lifecycle groups**, which is the natural
  answer skeleton:
  - **DESIGN** — II.1 Design life (**not less than 25 years**) · II.2 Environmental conditions
    (**North Atlantic**) · II.3 Structural strength (II.3.1 general design, II.3.2 deformation and
    failure modes, II.3.3 ultimate strength, II.3.4 safety margins) · II.4 Fatigue life ·
    II.5 Residual strength · II.6 Protection against corrosion (II.6.1 coating life, II.6.2
    corrosion addition) · II.7 Structural redundancy · II.8 Watertight and weathertight integrity ·
    II.9 Human element considerations · II.10 Design transparency
  - **CONSTRUCTION** — II.11 Construction quality procedures · II.12 Survey during construction
  - **IN-SERVICE CONSIDERATIONS** — II.13 Survey and maintenance · II.14 Structural accessibility
  - **RECYCLING CONSIDERATIONS** — II.15 Recycling
- **Tier III §6.1**: the rules of an organization **recognized by an Administration in accordance
  with SOLAS regulation XI-1/1**, or the national rules of an Administration, shall be verified as
  conforming to the goals and functional requirements.
- **SUPERSEDED-EDITION TRAP.** The verification guidelines are **no longer MSC.296(87)** (2010).
  International GBS Audit Teams established by the Secretary-General now evaluate submissions
  against the **Revised guidelines for verification of conformity with goal-based ship
  construction standards, resolution MSC.454(100)**, reporting to MSC for approval.
  **`B_CURRENCY_CHECK`: confirm MSC.454(100) is still the operative revision at publication, and
  establish whether any further revision was adopted after MSC 100.**

**Outstanding for Q1 before it can be authored:** the Ship Construction File requirement
(SOLAS II-1/3-10.2.1 and its MSC.1/Circ.1343 guidelines, including whether a `/Rev.1` is
operative); the IACS Common Structural Rules for Bulk Carriers and Oil Tankers as the Tier IV
instrument and their harmonised-entry date; and the outcome of the initial GBS verification audits.

### 6c. Q2 — Port State Control · PRIMARY VERIFIED

Read: **resolution A.1206(34)**, *Procedures for Port State Control, 2025*, adopted
**3 December 2025** (173 pp.), obtained from the IMO resolutions CDN.

- **SUPERSEDED-EDITION TRAP, and a sharp one.** A.1206(34) **revokes resolution A.1185(33)**
  (Procedures for Port State Control, 2023), which had itself followed the successive revocation
  of A.1155(32), A.1138(31), A.1119(30), A.1052(27), A.882(21), A.787(19), A.742(18), A.597(15)
  and A.466(XII). **A.1206(34) was adopted six months before the June sitting and is the operative
  instrument for this paper.** A great deal of published material — including material dated well
  into 2025 — still cites A.1185(33) or A.1155(32). An answer citing either is wrong for June 2026.
- **Legal framework, verbatim from §1.4** — this is precisely what Q2 a) asks for:
  > SOLAS 1974 regulations **I/19, IX/6.2, XI-1/4 and XI-2/9**, as modified by SOLAS PROT 1988;
  > **article 21 of LL 1966**, as modified by LL PROT 1988; **articles 5 and 6, regulation 11 of
  > Annex I, regulation 16.9 of Annex II, regulation 9 of Annex III, regulation 14 of Annex IV,
  > regulation 9 of Annex V and regulation 10 of Annex VI of MARPOL**; **article X of STCW 1978**;
  > **article 12 of TONNAGE 1969**; **article 11 of AFS 2001**; and **article 9 of BWM 2004**.
- **No more favourable treatment (§1.5.1):** SOLAS PROT 1988 art I(3), LL PROT 1988 art I(3),
  MARPOL art 5(4), STCW art X(5), AFS art 3(3), BWM art 3(3).
- **THE RIGHT OF APPEAL — §2.3.11, quoted in full:**
  > *"The company or its representative have a right of appeal against a detention taken by the
  > authority of a port State. **The appeal should not cause the detention to be suspended.** The
  > PSCO should properly inform the master of the right of appeal."*

  Three examinable points fall straight out, and the question's own framing sets up the first:
  1. **The right is the company's (or its representative's) — it is not the Chief Engineer's
     personal right.** Q2 b) asks about "you as the Chief Engineer **or** the Company"; the
     instrument answers the disjunction directly.
  2. **Appealing does not release the ship.** The detention continues while the appeal runs.
  3. The PSCO carries a duty to **inform the master** the right exists.
- **A TRAP WORTH RECORDING.** A.1206(34) **Chapter 5 is titled "REVIEW PROCEDURES"** and a
  candidate — or a careless answer — will reach for it as the appeal route. **It is not.** Chapter 5
  (§5.1 Report of comments) concerns the Organization's periodic evaluation of *summaries of
  deficiency reports* to improve consistency of application. The owner's remedy is §2.3.11, inside
  the general procedural guidelines. **The chapter with the right-sounding name is the wrong one.**
- Also verified as available for the answer: §2.4 Clear grounds · §2.5 More detailed inspections ·
  Chapter 3 Contravention and detention (3.5 Guidance for the detention of ships, 3.7 Rectification
  and release) · §2.3.9 permission to proceed to another port · §2.3.10 detention reports to the
  flag State · Appendix 2 Guidelines for the detention of ships · Appendix 17 Comments by flag
  State on detention report.

**Outstanding for Q2 before it can be authored:** the "undue delay / compensation" provisions in
the parent conventions (**MARPOL article 7(2)**, **SOLAS I/19(f)** and the LL equivalent) read in
their own text rather than through the Procedures; the **Indian Ocean MoU** review/appeal
mechanism and the **DG Shipping** route as the practical Indian answer; and whether the
**Merchant Shipping Act 2025** carries its own detention and appeal provisions, which — June being
after 15 March 2026 — would be the operative Indian statute.

---

## 7. WHERE A FOLLOWING SESSION RESUMES

**Nothing in this document is provisional.** §1–§5 are complete and verified, and §6 records
exactly which claims have been established against primary sources.

**Completed**

- Repository re-grounding; baseline toolchain confirmed at **5 papers, ALL STAGES PASS, 38 warnings**.
- Branch `pastpapers/qp2606-founder-review` created from `5744143`; all five prior branches untouched.
- Source extraction, character-level transcription and **visual verification of both pages**.
- Marks, instructions, anomalies and the 96-vs-100 check — **6/6**.
- Full recurrence classification against all 45 built questions, with dedup tiers.
- Controlled-vocabulary audit (§8 below).
- One stale recorded fact found and corrected (§1a).
- Primary-source verification for **Q1** and **Q2** and the paper-wide temporal anchors.

**Not started**

- Primary-source verification for **Q3, Q4, Q5, Q6, Q7, Q8, Q9**, and completion of the
  outstanding items listed for Q1 and Q2.
- `specs/QP2606.json` — **does not exist**. No decomposition gates, model answers, routes,
  study guides, retrieval cards or quick-revision blocks have been authored.
- `verification/QP2606/` records.
- `FIXTURES` entry for QP2606 in `ui_behaviour_test.cjs` (**standing rule — a paper without
  fixtures must fail the harness**).
- Build, UI harness at six pages, visual QA, determinism check, prior-five-paper byte regression.
- `docs/QP2606_TRUE_SOURCE_DEMAND_MAP.md`.
- The six-paper closure work: demand aggregation, corpus priority re-ranking, question families,
  archetype and category distributions, search-payload decision, mobile measurement, the pattern
  register update and the evidence snapshot document.

**The single most useful thing about June, for whoever picks it up:** it is the most expensive
paper in the set. **Five of nine questions are new to the corpus and there is no Tier D reuse at
all**, so almost nothing can be inherited. Budget it as roughly a paper and a half, not as a
sixth iteration of a settled routine.

**Highest-risk items, in order:**

1. **Q7** — sitting-date truth for Indian statutory protection of the island groups, after the
   MS Act 2025 commencement, and whether the islands hold any actual PSSA or special-area status
   (they may hold none, in which case the question is prospective and must be answered as such).
2. **Q3** — the question names the **York Antwerp Rules 1994** specifically, a superseded edition
   (2004 and 2016 exist). The answer must give the 1994 position as asked while stating the
   current editions, and must not silently substitute a later Rule A.
3. **Q6** — largely outside the regulatory corpus. Ship cost structure and inventory-control
   theory rest on textbook and industry material, not primary instruments. Expect a high
   `C_ACCEPTED_LIMITATION` count and **do not manufacture citations to make it look verified**.
4. **Q5** — the ISM cyber-risk position (resolution MSC.428(98) and the current revision of the
   MSC-FAL.1/Circ.3 guidelines) and the current ISM amendment state both need checking.
5. **Q9** — confirm **MSC-MEPC.2/Circ.12/Rev.2** (9 April 2018) is still the operative FSA
   revision at the June sitting. Note the question uses the instrument's own term **"Risk
   Analysis"** for Step 2, which is the correct name; the HATC coaching notes mis-name it
   "assessment of risks" and are, as always, not a verification source.

---

## 8. CONTROLLED VOCABULARY AUDIT — clean

Required by the six-paper closure brief before aggregation. Measured across all 45 built questions:

| Field | Values in use | Verdict |
|---|---|---|
| `recurrence_class` | `topic_recurrence` 22 · `near_recurrence` 10 · `new` 9 · `exact_recurrence` 4 | **No drift, no aliases.** `new` is canonical and is the value June's five NONE questions must carry. **`no_recurrence` appears nowhere.** |
| `reuse_tier` | `B` 23 · `C` 9 · `D` 13 | Clean. **Tier `A` has never been used** in 45 questions — worth recording, since the draft skill defines it. |

**One inconsistency found, and it is in the declaration rather than the data.** The
`controlled_vocabulary` block differs in shape between specs: QP2607 and QP2601 declare
`recurrence_class` / `recurrence_rule` / `primary_category`; QP2602 and QP2603 declare only
`reuse_tiers` and omit any recurrence list; QP2604 declares `archetypes` / `reuse_tiers` /
`recurrence_classes`. QP2604's own note records that the four earlier specs were deliberately not
edited because they are frozen review candidates, and that the index derives from the union.

**No spec was rewritten.** QP2606 should follow **QP2604's shape**, which is the most complete.
The values themselves need no cleanup.
