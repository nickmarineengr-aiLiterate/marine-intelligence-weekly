# QP2606 — TRUE SOURCE DEMAND MAP

**June 2026, Engineering Management, MEO Class I.**
Written 2026-08-09 at the close of QP2606 production. Companion to the QP2607, QP2601, QP2602,
QP2603 and QP2604 maps, **none of which is modified by this document**.

This is the handoff contract to the corpus-production track: what QP2606 actually needed in order
to be verified, how strong the evidence was, and what acquiring a source would unblock.

> **`reference_shelf` is empty on every QP2606 question, by design.** No corpus object was
> fabricated, no object id invented, no PDF page cited. See `MIW_TRUE_SOURCE_CONTRACT.md` §3 and
> §5. This map records *demand*, not mappings.

> **June completes the 2026 set.** §3 therefore carries the six-paper aggregate rather than the
> five-paper one, and it is the input the post-six-paper corpus priority review should use.

---

## 1. Classification used

Unchanged from the five earlier maps, so all six are directly comparable.

| Code | Meaning |
|---|---|
| **P** | PRIMARY — the answer's correctness rests on this instrument. Without it the claim is unverified. |
| **S** | SUPPORTING — cited to establish authority or context; the answer would survive its absence with a narrower claim. |
| **C** | CONTEXT — mentioned for orientation; carries no load-bearing claim. |

| Recommendation | Meaning |
|---|---|
| **FULL_CORPUS** | Worth holding as consolidated, structured corpus content with section-level destinations. |
| **REFERENCE_PACK** | Worth holding as a controlled document set; section-level structuring not yet justified. |
| **EXISTING_OBJECT** | An id already exists under the convention in §4 of the contract; needs mapping, not acquisition. |

---

## 2. Demand by question

### Q1 — Goal-based ship construction standards
| Instrument | Class | Note |
|---|---|---|
| **Resolution MSC.287(87)** | **P** | **READ IN FULL AT SOURCE.** New demand. A corpus object must resolve to **section level** — §1.5 and §3 say different things about the tier count, and the answer turns on holding both. Tier II must resolve to the **individual functional requirement** (II.1 … II.15). `FULL_CORPUS`. |
| **SOLAS regulation II-1/3-10** and **II-1/2.28** | **P** | Established from the adopting resolution MSC.290(87) and authoritative secondary reproduction. Licensed consolidated SOLAS **NOT HELD**. `C_ACCEPTED_LIMITATION`. |
| **Resolution MSC.454(100)** | **P** | The operative verification guidelines. Identified but **not read at source**; recorded `B_CURRENCY_CHECK`. `REFERENCE_PACK`. |
| MSC.1/Circ.1343 (Ship Construction File) | S | Content guidance; not read at source. `REFERENCE_PACK`. |
| IACS Common Structural Rules | S | The Tier IV instrument. Licence-gated. `REFERENCE_PACK`. |
| SOLAS regulation XI-1/1 | S | Recognition. Shared with Q8. |

### Q2 — Port State Control and the right of appeal
| Instrument | Class | Note |
|---|---|---|
| **Resolution A.1206(34)** | **P** | **READ AT SOURCE, 173 pp.** New demand, and **highly perishable** — re-adopted roughly every two years and only six months old at this sitting. A corpus object must carry the **revocation chain**, because the failure mode is citing A.1185(33). Must resolve to §1.4, §1.5.1, §2.3.11, §2.4, §2.5, ch. 3 and ch. 5. `FULL_CORPUS`. |
| **MARPOL article 7(2)**; **SOLAS regulation I/19** | **P** | Undue delay and compensation. Read through the Procedures and authoritative secondary reproduction, not licensed text. `C_ACCEPTED_LIMITATION`. |
| SOLAS IX/6.2, XI-1/4, XI-2/9; LL art. 21; STCW art. X; TONNAGE art. 12; AFS art. 11; BWM art. 9 | S | The §1.4 list. Demand at **article** level for six separate conventions. |
| Indian Ocean MoU | S | Regional arrangement; the Indian practical route. `REFERENCE_PACK`. |
| Merchant Shipping Act, 2025 | C | Whether it carries its own detention/appeal route is **unestablished**; no claim made. |

### Q3 — Types of loss, general average, warranties
| Instrument | Class | Note |
|---|---|---|
| **York-Antwerp Rules 1994 AND 2016** | **P** | **Read in the CMI's own tabular comparison**, not in the published Rules. MIW holds **no licensed copy of either edition**. `C_ACCEPTED_LIMITATION`. **A corpus object must be EDITION-KEYED**: this question proves the point, because the examiner named a 1994 edition in a 2026 paper and older contracts still incorporate it. `FULL_CORPUS`. |
| **Marine Insurance Act, 1963 (India)** | **P** | ss.35–43 (warranties) and ss.55–66 (losses). **Only s.66 has ever been verified against primary statutory text** in MIW work. `C_ACCEPTED_LIMITATION`. **Priority acquisition — this is the third paper to depend on it.** `FULL_CORPUS`. |
| Insurance Act 2015 (United Kingdom) | S | Recorded as a **jurisdictional contrast** and expressly not applied. `REFERENCE_PACK`. |

> **NEW STRUCTURAL REQUIREMENT FOR THE CORPUS — the edition axis is load-bearing, not metadata.**
> Every prior paper needed the *current* edition of an instrument. Q3 needs **two editions of the
> same instrument simultaneously**, and needs to state that Rule A is identical between them while
> Rules VI, XX, XXI and XXIII are not. A corpus that stores "the York-Antwerp Rules" with the
> current text and an edition tag **cannot answer this question**. It must store editions as
> first-class objects with a diff relationship between them.

### Q4 — Upskilling for decarbonisation; communication
| Instrument | Class | Note |
|---|---|---|
| **HTW 12 outcome (23–27 February 2026)** | **P** | Draft interim training guidelines for methyl/ethyl alcohol and for ammonia; comprehensive STCW review. **A meeting outcome, not an instrument** — see §4. `REFERENCE_PACK`. |
| **STCW regulation V/3 and Code section A-V/3** | **P** | The boundary of the mandatory framework. Licensed consolidated STCW **NOT HELD**. `C_ACCEPTED_LIMITATION`. `FULL_CORPUS`. |
| **ISM Code 1.4.2, 6.6, 6.7** | **P** | Communication requirements. Shared with Q5. |
| SOLAS regulation V/14; STCW Code A-VIII/2; resolution A.918(22) | S | Working language, resource management, SMCP. |
| MARPOL Annex VI regs 25 and 28 | S | Shared with Q6. **Existing demand** from QP2607 Q4. `EXISTING_OBJECT` candidate. |
| IMO Net-Zero Framework | C | **Approved, NOT adopted** at this sitting. No corpus object should exist for an unadopted instrument except as a status record. |

### Q5 — The ISM Code and the safety management system
| Instrument | Class | Note |
|---|---|---|
| **ISM Code** — 1.2, 1.4, sections 9, 10.3, 12 | **P** | Read in authoritative reproductions. **Licensed consolidated ISM Code NOT HELD.** `C_ACCEPTED_LIMITATION`. **Now demanded by two questions on this paper and implicated in a third (Q6).** `FULL_CORPUS`, high priority. |
| **MSC-FAL.1/Circ.3/Rev.3 (4 April 2025)** | **P** | **READ AT SOURCE.** New demand, and **perishable — three revisions so far**. The corpus object must carry the revision, because Rev.2 and Rev.3 differ in the number of functional elements. `REFERENCE_PACK`. |
| Resolution MSC.428(98) | **P** | The mechanism by which cyber entered the SMS. Not read at source. `REFERENCE_PACK`. |
| Resolution A.741(18); SOLAS chapter IX; resolution MSC.353(92) | S | Adoption, mandatory hook, latest amendment. MSC.353(92) content **not established**. |

### Q6 — Ship costs and inventory control
| Instrument | Class | Note |
|---|---|---|
| **ISM Code 10.3** | **P** | The only genuine regulatory constraint in the question. Shared with Q5. |
| MARPOL Annex VI regs 25 and 28 | S | Efficiency as compliance. Shared with Q4. |
| — | — | **NOTHING ELSE.** See the note below. |

> **THIS QUESTION IS A DELIBERATE ZERO-DEMAND CASE, AND IT IS WORTH RECORDING AS SUCH.**
> The cost taxonomy and every inventory-control technique in the answer are accepted
> shipping-economics and operations-management practice. **No IMO, statutory or class instrument
> covers them, and none was invented to fill the gap.** The corpus track should NOT attempt to
> manufacture an object for this content. If MIW ever wants to support it, the correct answer is a
> **separately governed reference layer of engineering and management practice**, explicitly not
> presented as regulatory authority — not a corpus object.

### Q7 — Protecting the islands; PSSA designation
| Instrument | Class | Note |
|---|---|---|
| **Resolution A.982(24) as amended by MEPC.267(68)** | **P** | The PSSA Guidelines. New demand. The object **must carry the amendment**, since citing A.982(24) alone is incomplete. Must resolve to the criteria groups and the APM requirement. `FULL_CORPUS`. |
| **The IMO register of designated PSSAs** | **P** | **A LIVE EXTERNAL LIST — see §4.** The answer's central claim is a *negative*: no Indian area is designated. That claim decays every MEPC session. |
| **Island Coastal Regulation Zone (ICRZ) Notification, 2019** | **P** | Made under EP Act 1986 s.3; superseded the IPZ Notification 2011. **Exact Gazette citation unsettled** — `B_CURRENCY_CHECK`. `REFERENCE_PACK`, Indian. |
| **Merchant Shipping Act, 2025** | **P** | In force 15 March 2026. **India Code returns HTTP 403.** Only commencement and repeal verified in Gazette. **Fifth paper to depend on this Act.** `FULL_CORPUS`, highest Indian priority. |
| Environment (Protection) Act 1986; Wild Life (Protection) Act 1972; Coast Guard Act 1978; NOS-DCP | S | The Indian domestic layer. `REFERENCE_PACK`. |
| UNCLOS article 211(6); SOLAS V/10, V/11 | S | Legal bases for an APM. UNCLOS is an **existing** demand from QP2601 Q7 and QP2604 Q7. |
| MARPOL Special Areas; Annex VI ECAs | C | Named to establish that India holds none. |

### Q8 — Classification societies, SOLAS II-1/3-1 and surveys
| Instrument | Class | Note |
|---|---|---|
| **Resolution A.1207(34)** | **P** | **READ AT SOURCE, 233 pp.** New demand and **perishable** — re-adopted roughly every two years, revokes A.1186(33), six months old at this sitting. Must resolve to §4.1–§4.7 and to annex 1's certificate mapping, because the periodical survey has **two different frequencies**. `FULL_CORPUS`. |
| **SOLAS regulation II-1/3-1** | **P** | The whole point of limb (a). Authoritative secondary only. `C_ACCEPTED_LIMITATION`. |
| SOLAS XI-1/1; RO Code MSC.349(92) + MEPC.237(65) | **P** | Recognition and the RO Code. `REFERENCE_PACK`. |
| IACS UR / UI / PR; Common Structural Rules | S | Licence-gated. Shared with Q1. |
| IACS membership record | C | **HTTP 403.** No membership count asserted anywhere. |

### Q9 — Formal Safety Assessment, the method itself
| Instrument | Class | Note |
|---|---|---|
| **MSC-MEPC.2/Circ.12/Rev.2 (9 April 2018)** | **P** | **READ IN FULL AT SOURCE, 71 pp.** Existing demand from QP2607 Q1 and the lithium-battery family, but **at a different depth**: those questions APPLIED FSA, this one needs the methodology, so the object must resolve to §1.1.1, §2, §3.1.1.1, §§4–9 and **appendix 7**. `FULL_CORPUS`. |
| Appendix 7 tabulated NCAF/GCAF values | **P** | **Present as a table IMAGE and not extractable as text.** No monetary figure is asserted anywhere in the answer. `C_ACCEPTED_LIMITATION`. **A corpus ingestion pipeline must handle tables-as-images or it will silently lose criterion values.** |

---

## 3. Six-paper aggregate demand — the completed 2026 set

**Counting rule:** an instrument is counted once per paper that raises a load-bearing (P) demand
for it. Reuse-carried demand is not double-counted.

| Instrument | Papers demanding it | Held? | Recommendation |
|---|---|---|---|
| **Licensed consolidated SOLAS** | QP2607, QP2601, QP2602, QP2603, QP2604, **QP2606** — **6 of 6** | **NO** | **FULL_CORPUS — the single highest-value acquisition in the whole set** |
| **Merchant Shipping Act, 2025 (India)** | QP2607, QP2602, QP2603, QP2604, **QP2606** — 5 | Gazette PDF, partial | **FULL_CORPUS — highest Indian priority** |
| **Licensed consolidated MARPOL** | QP2607, QP2602, QP2604, **QP2606** — 4 | **NO** | **FULL_CORPUS** |
| **ISM Code** | **QP2606** (×2 questions), QP2601 | **NO** | **FULL_CORPUS — newly promoted by June** |
| **Marine Insurance Act, 1963 (India)** | QP2607, QP2601/QP2604, **QP2606** — 3 | s.66 only | **FULL_CORPUS** |
| **York-Antwerp Rules, edition-keyed** | QP2607, QP2602, QP2604, **QP2606** — 4 | **NO** | **FULL_CORPUS — edition axis now load-bearing** |
| **IMSBC Code** | QP2607, QP2603 | **NO**, licence-gated | FULL_CORPUS |
| **STCW consolidated** | QP2601, QP2604, **QP2606** — 3 | **NO** | FULL_CORPUS |
| Assembly resolutions re-adopted on a cycle (A.1206(34), A.1207(34)) | **QP2606** ×2 | read at source | **REFERENCE_PACK with a revocation chain** |
| FSA Guidelines MSC-MEPC.2/Circ.12/Rev.2 | QP2607, QP2602, QP2603, QP2604, **QP2606** — 5 | read at source | FULL_CORPUS |

### The headline for the corpus team, now that all six papers exist

1. **A licensed consolidated SOLAS is demanded by every single paper in the 2026 set.** Six of six.
   Nothing else comes close. It would clear `C_ACCEPTED_LIMITATION` flags on all six.
2. **The ISM Code is newly promoted by June** — two questions on this paper depend on it directly
   and a third uses 10.3 as its only regulatory constraint. It is cheap relative to SOLAS.
3. **The York-Antwerp Rules must be modelled edition-first**, not current-text-plus-tag.
4. **Two Assembly resolutions used on this paper are on a re-adoption cycle** and were both six
   months old at the sitting. Any corpus object for them must carry the revocation chain, or the
   corpus will confidently serve a superseded edition.

---

## 4. Corpus temporal model — the live-list pattern reaches a FIFTH instance, and a new sub-class

The pattern first recorded in March, and refined in April: some load-bearing values are not
editions or amendment states but **continuously revised third-party or institutional registers**.

Prior instances: Joint War Committee Listed Areas (Mar Q3); authorised Indian ports for ship
sanitation certificates (Jan Q6); EU-approved recycling facilities (Mar Q9); national biofouling
arrival requirements (Apr Q5).

**Fifth instance — the IMO register of designated Particularly Sensitive Sea Areas (Jun Q7).**

> **NEW SUB-CLASS, AND IT IS THE SHARPEST ONE YET: THE LOAD-BEARING CLAIM IS A NEGATIVE.**
>
> Q7's answer does not depend on *which* areas are designated. It depends on the fact that
> **none of them is Indian**. A live-list object that stores "the current members of the list" can
> serve a positive lookup, but a **negative claim decays silently**: the moment India obtains a
> PSSA designation, an answer that says "no Indian area holds PSSA status" becomes false, and
> nothing in the corpus would flag it, because no object the answer cites has changed.
>
> **A corpus live-list object therefore needs an "absence" relationship**, so that a question can
> assert *X is not in list L as at date D* and be re-checked when L changes — not merely cite the
> members of L.

**A second new pattern, from Q4: a MEETING OUTCOME is not an instrument.** The HTW 12 result —
draft interim training guidelines agreed in February 2026 — is load-bearing for Q4, is
authoritative, and **is not a document with an edition**. It is a state of institutional progress.
The corpus needs either a "work in progress" object type or an explicit decision not to hold such
things, because the alternative is a session inventing a circular number that does not exist.

---

## 5. What acquiring a source would unblock

| Acquire | Unblocks |
|---|---|
| **Licensed consolidated SOLAS** | **All six papers.** On June alone: Q1 (II-1/3-10, II-1/2.28), Q2 (I/19 and the ch. IX / XI hooks), Q4 (V/14), Q8 (II-1/3-1, XI-1/1). |
| **ISM Code (licensed)** | June Q5 in full, June Q4's communication limb, June Q6's only regulatory constraint, and QP2601 Q2. |
| **Marine Insurance Act, 1963** | June Q3 in full, plus QP2607 Q5/Q9 and QP2601 Q3 / QP2604 Q3. |
| **York-Antwerp Rules, 1994 and 2016** | June Q3's edition comparison — currently resting on a CMI comparison document rather than the Rules. |
| **Merchant Shipping Act, 2025 (full Gazette text, section-level)** | June Q7's Indian limb and the standing `B_CURRENCY_CHECK` on five papers. |
| **A table-image-capable ingestion path** | June Q9's appendix 7 criterion values, and any future instrument whose numbers live in a figure. |

---

## 6. Status

**`reference_shelf` remains empty on every question of all six papers.** No object id has been
invented, no PDF page cited, no fake viewer link created. The `reference_href()` seam is untouched
and remains a seam.

The QP track's next involvement is step 8 of the contract's handoff sequence — populating
`reference_shelf` from returned object mappings. **Nothing before then.**

**This map completes the 2026 demand picture.** The six-paper aggregate in §3 is the input the
post-six-paper corpus priority review should work from; it should not be re-derived per paper.
