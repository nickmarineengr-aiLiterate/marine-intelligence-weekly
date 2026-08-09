# QP2606 (June 2026) — dedup assessment and source plan

**Completed 2026-08-09**, across two sessions: transcription and recurrence in the first,
verification and authoring in the second. This document records the dedup decision for every
question and the source plan that followed from it.

---

## 1. Method

Unchanged from the four prior papers, and applied in this order:

1. `difflib.SequenceMatcher` ratio of each June stem against all **45** previously built
   `text_verbatim` strings.
2. A concept-level term scan of all 45 stems for each June question's subject vocabulary.
3. **Human adjudication of examiner demand, limb by limb.**

Step 3 is not optional. April established that the ratio is **length-sensitive**, and June added a
second failure mode (§3 below).

---

## 2. Result

**EXACT 0 · NEAR 0 · TOPIC 4 · NONE 5.**

| Q | Subject | Class | Tier | Related to |
|---|---|---|---|---|
| Q1 | Goal-based ship construction standards | `new` | C | — |
| Q2 | Port State Control and the right of appeal | `new` | C | — |
| Q3 | Types of loss, general average, warranties | `topic_recurrence` | B | **QP2607 Q5** (primary); QP2602 Q6 |
| Q4 | Upskilling for decarbonisation; communication | `topic_recurrence` | B | QP2601 Q2; QP2607 Q8; QP2602 Q8 |
| Q5 | ISM Code and the safety management system | `new` | C | — |
| Q6 | Ship costs and inventory control | `new` | C | — |
| Q7 | Protecting the islands; PSSA designation | `new` | C | — |
| Q8 | Classification societies; annual vs periodical survey | `topic_recurrence` | B | **QP2607 Q3** (primary); QP2603 Q6 |
| Q9 | Formal Safety Assessment — the method itself | `topic_recurrence` | B | QP2607 Q1; QP2602 Q3 / QP2603 Q8 / QP2604 Q2 |

**Tiers: C ×5, B ×4. No Tier A, and — for the first time since January — NO TIER D.**

### Why that matters for production

Tier D reuse is what made February, March and April affordable: a verified answer already existed
and only had to be re-anchored. **June inherits nothing.** Five of its nine questions have no
relationship at all to the 45 already built, and the four that do have only a topic relationship,
so every answer was authored from sources. This is why June was checkpointed rather than rushed,
and it is the single most useful fact about this paper.

---

## 3. Two recurrence failure modes recorded on this paper

### 3a. The similarity ratio ranked the WRONG neighbour

> **June Q3's highest-scoring prior question (QP2601 Q3, ratio 0.3080) is not its real relative.**

Its actual relative is **QP2607 Q5**, which scores *lower* but contains a near-verbatim shared task:

| | |
|---|---|
| QP2607 Q5 | "What are the **circumstances when a general average can be declared**?" |
| QP2606 Q3 a) | "State the **circumstances under which \"General Average\" can be declared**?" |

QP2601 Q3 — the top scorer — is a **salvage law** question that merely contains the phrase
"General Average". **The score was non-zero, confidently ranked, and pointed at the wrong target.**
A session ranking by score alone would have reused salvage content for an averages question.

June Q3 is nonetheless **TOPIC and not NEAR**: only one of its four tasks maps cleanly, limb b)
(express versus implied warranties) is new subject matter, and the average adjusters task is
dropped. **Reuse was taken at limb level, never at question level.**

### 3b. A shared word that is a homonym

**QP2601 Q2 and QP2606 Q4 both contain "decarbonisation" and both contain "communication". They
are not the same subject.**

| | QP2601 Q2 | QP2606 Q4 a) |
|---|---|---|
| "decarbonisation" means | **main engine decarbonisation** — removing carbon deposits | **decarbonisation of shipping** — the energy transition |
| the task | communication-failure hazards in a two-group overhaul | the need to upskill and train seafarers |

The genuine overlap is **communication**, and only that was reused. This is AGENT_LESSON 2 —
*"tag-level dedup is unsafe; read the matched content"* — reappearing at **stem** level.

---

## 4. The host recurrence table on this paper

The host claims **all nine** June questions repeat **2023/DEC** at the same question number.
**Unverifiable** — the December 2023 paper is not in the source set — and **not used to classify
anything**.

Two observations:

- **June is the first paper on which the host table's 2026 silence was correct.** It lists no other
  2026 sitting against any June question, and independent comparison agrees there is no exact or
  near repeat within the 2026 set.
- It still **under-claims** on topic relationships, recording nothing of Q3↔QP2607 Q5 or
  Q9↔the four prior FSA questions.

Standing rule unchanged: **the host table establishes topic recurrence at most.**

Q6 carries **sixteen** prior sittings back to February 2015 — the most-repeated question in the
whole source set — and has **no relationship whatever** to any of the 45 built questions. **High
historical repetition and corpus recurrence are independent properties.**

---

## 5. Source plan, and what it cost

| Q | Primary instrument actually read | Outcome |
|---|---|---|
| Q1 | Resolution MSC.287(87), in full | Tier count settled; MSC.296(87) found superseded by MSC.454(100) |
| Q2 | Resolution A.1206(34), Procedures for PSC 2025 | Revokes A.1185(33); appeal at §2.3.11 quoted; chapter 5 trap recorded |
| Q3 | CMI tabular comparison of YAR 1994 / 2004 / 2016 | **Rule A identical in 1994 and 2016**; 1994 has no time bar |
| Q4 | HTW 12 outcome (Feb 2026); ISM 1.4.2, 6.6, 6.7 | Mandatory-STCW gap established; Net-Zero re-anchored to the sitting |
| Q5 | MSC-FAL.1/Circ.3/Rev.3 (4 Apr 2025); ISM 1.2, 1.4, 10.3 | **SIX functional elements — Govern added**; Code evolves without amendment |
| Q6 | ISM 10.3; MARPOL Annex VI regs 25 and 28 | **Deliberately thin.** No instrument exists for the rest; none invented |
| Q7 | IMO PSSA designations; A.982(24) as amended by MEPC.267(68) | **No Indian PSSA exists** — question answered in the conditional |
| Q8 | Resolution A.1207(34), HSSC 2025, in full | Revokes A.1186(33); periodical survey has **two** frequencies |
| Q9 | MSC-MEPC.2/Circ.12/Rev.2, in full | **No mandatory cost-per-fatality criterion exists** |

### The single deliberate abstention

**Q6 has no primary authority for its principal content, and none was manufactured.** The cost
taxonomy and every inventory technique are accepted management and shipping-economics practice.
Two genuine constraints — ISM 10.3 and MARPOL Annex VI regs 25 and 28 — are used only where they
actually bite. Recorded as `C_ACCEPTED_LIMITATION`, not disguised.

---

## 6. Mandatory assembled-spec sweep

Run per the standing rule even though June carries **no Tier D reuse** and therefore no inherited
prose to go stale. Sitting-relative statements can be **authored** as easily as inherited.

**~385 hits across ten patterns. ZERO defects.** Every hit was adjudicated by hand and falls into
one of three classes:

- a **deliberate teaching point** that an instrument is superseded (MSC.296(87), A.1185(33),
  A.1186(33), MSC-FAL.1/Circ.3/Rev.2, the Island Protection Zone Notification 2011) or that a
  statute is repealed (the Merchant Shipping Act, 1958);
- a **correctly anchored** sitting-relative statement — the arithmetic was checked: Feb 2026 is
  "four months before", 3 Dec 2025 is "six months before", Nov 2026 is "five months after";
- a **real instrument date**.

`cross-ref by number` returned **0 hits** — no answer refers to another question on this paper by
number, which is the failure March had to patch ten times.
