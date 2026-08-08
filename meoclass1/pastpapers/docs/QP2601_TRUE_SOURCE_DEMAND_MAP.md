# QP2601 — TRUE SOURCE DEMAND MAP

**January 2026, Engineering Management, MEO Class I.**
Written 2026-08-08 at the close of QP2601 production. Companion to `QP2607_TRUE_SOURCE_DEMAND_MAP.md`,
which is **not** modified by this document.

This is the handoff contract to the corpus-production track: what QP2601 actually needed in order
to be verified, how strong the evidence was, and what acquiring a source would unblock.

> **`reference_shelf` is empty on every QP2601 question, by design.** No corpus object was
> fabricated, no object id invented, no PDF page cited. See `MIW_TRUE_SOURCE_CONTRACT.md` §3 and §5.
> This map records *demand*, not mappings.

---

## 1. Classification used

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

### Q1 — Low-load two-stroke operation
| Instrument | Class | Note |
|---|---|---|
| MARPOL Annex VI reg 25 (EEXI) | **P** | In force 1 Jan 2023. `EXISTING_OBJECT` — Annex VI is already represented. |
| MARPOL Annex VI reg 28 (CII) | **P** | As above. |
| MARPOL Annex VI reg 26 (SEEMP) | S | |
| IMO Net-Zero Framework | C | **Approved, not adopted.** Adoption adjourned at the extraordinary MEPC session, 14–17 Oct 2025. Do not create a corpus object for an unadopted instrument. |
| Engine-designer service guidance | S | Licensed/commercial. `REFERENCE_PACK` at best; may never be redistributable. |

**Caution for the resolver:** the QP2607 map already records that **MARPOL Annex VI is represented
twice** in `repo-data.json` (`MARPOL-VI-14…` and `MEPC32876-3-14…`) with disjoint vocabularies. Q1
needs regs 25, 26 and 28, so the same disambiguation must be settled before any Annex VI mapping.

### Q2 — Communication and the decarbonisation job
| Instrument | Class | Note |
|---|---|---|
| ISM Code elements 6, 7, 8 | **P** | `FULL_CORPUS`. Recurs across both papers. |
| SOLAS V/14.3 (working language) | **P** | `EXISTING_OBJECT` — SOLAS is represented. |
| STCW Code A-VIII/2 | S | See the STCW note at Q9 — licence-gated. |
| Code of Safe Working Practices | C | Industry guidance, not a convention. |

### Q3 — Salvage law and General Average
| Instrument | Class | Note |
|---|---|---|
| Salvage Convention 1989, Arts 8, 12, 13, 14 | **P** | In force 14 Jul 1996. **New demand — no July counterpart.** `FULL_CORPUS`. |
| York-Antwerp Rules (Rule A; YAR 2016) | **P** | Contractual, not statutory. `REFERENCE_PACK`. Also demanded by QP2607 Q5. |
| Marine Insurance Act, 1963 (India) s.66 | **P** | Demanded by QP2607 Q5 and Q9 and by QP2601 Q3 and Q4 — **the most repeatedly demanded Indian instrument in the 2026 set so far.** |
| SCOPIC clause / Lloyd's Open Form | S | Contract forms. `REFERENCE_PACK`. |

### Q4 — VLCC total loss
| Instrument | Class | Note |
|---|---|---|
| CLC Protocol 1992 | **P** | Also QP2607 Q2. `FULL_CORPUS`. |
| Nairobi WRC 2007 | **P** | **New demand.** Territorial-sea application is opt-in — a section-level destination matters here. |
| Fund Protocol 1992 | **P** | |
| Supplementary Fund Protocol 2003 | S | |
| Bunkers Convention 2001 | S | Already demanded by QP2607 Q2; `BunkerConvention2001-Articles-3` and `-7` exist. `EXISTING_OBJECT`. |
| LLMC 1976 and 1996 Protocol | S | **New demand.** |
| UNCLOS Art 2 | S | See Q7. |
| Marine Insurance Act 1963 ss.19–20 | S | Verified in QP2607 Q9. |

### Q5 — Tank corrosion, coatings and the CTF
| Instrument | Class | Note |
|---|---|---|
| IMO res MSC.215(82) — PSPC | **P** | **New demand.** Read in full for this paper. `FULL_CORPUS` — section 3.4 is quoted item by item and is exactly the kind of content a section-level destination serves. |
| SOLAS II-1/3-2 | **P** | `EXISTING_OBJECT`. |
| SOLAS XII/6 | S | |
| ESP Code / res A.744(18) | **P** | ⚠ **NOT HELD.** The PSPC defines only *GOOD*; *FAIR* and *POOR* and the survey consequences come from class restatements and sit at P2. **Acquisition unblocks a class C limitation.** |

### Q6 — WHO, disease vectors and ship health certificates
| Instrument | Class | Note |
|---|---|---|
| International Health Regulations (2005), as amended 2014/2022/2024 | **P** | **New demand, and wholly new subject area for the corpus.** Read in full. `FULL_CORPUS`. Arts 20, 22, 24, 27, 37, 39 and Annexes 3, 5, 8. |
| IHR (2005) **original** text | S | Needed **as a superseded edition** — the Maritime→Ship Declaration of Health rename can only be shown by holding both. A good test of the corpus's edition/amendment model. |
| Indian Port Health Rules, 1955 | S | ⚠ Not read at source. `REFERENCE_PACK`. |
| DG Shipping Order 10 of 2018 (revised) | C | ⚠ Not read at source. |
| MLC 2006 (crew medical fitness) | C | |

### Q7 — UNCLOS flag State duties and India's mechanism
| Instrument | Class | Note |
|---|---|---|
| UNCLOS Arts 91, 92, 94, 217 | **P** | **New demand.** Also serves Q4 (Art 2) and Q8 (Art 94(7)). `FULL_CORPUS` — UNCLOS is demanded by three QP2601 questions. |
| Merchant Shipping Act, **1958** | **P** | ⚠ **The question-date statute.** Repealed 15 Mar 2026. The corpus must be able to serve a **repealed** instrument for papers sat before commencement — see §5. |
| Merchant Shipping Act, 2025 + S.O. 1244(E) | S | Primary-verified in QP2607. `dgma-merchant-shipping-act-2025` is registered with **zero nodes**. |
| RO Code | S | Verified in QP2607 Q3. |
| III Code / IMO Member State Audit Scheme | S | **New demand.** |

### Q8 — Casualty Investigation Code
| Instrument | Class | Note |
|---|---|---|
| IMO res MSC.255(84) — Casualty Investigation Code | **P** | **New demand.** Read in full. `FULL_CORPUS` — the ch.2 definitions are heavily cited and are natural section-level objects. |
| SOLAS XI-1/6 | **P** | `EXISTING_OBJECT`. |
| MARPOL Article 12 | **P** | An **Article of the Convention**, not a regulation in an Annex — the corpus id scheme must distinguish these. |
| SOLAS I/21 | S | |
| UNCLOS Art 94(7) | S | Shared with Q7. |
| IMO res MSC.257(84) | C | The amending resolution. |

### Q9 — Human element in STCW and IMO fatigue guidance
| Instrument | Class | Note |
|---|---|---|
| **STCW Convention and Code (Manila-amended)** | **P** | ⚠ **NOT HELD — highest-value acquisition on this paper.** Reg VIII/1, A-VIII/1, A-VIII/2, Part A competence tables, regs I/6, I/8, I/9, I/11, I/14. See §5 for why this is urgent. |
| MSC.1/Circ.1598 — Guidelines on fatigue | **P** | Read in full. `FULL_CORPUS` or `REFERENCE_PACK`. |
| MSC/Circ.1014 | C | Superseded; useful only as edition history. |
| MLC 2006 Regs 2.3, 2.4, 2.7 | S | |

---

## 3. Aggregate across the 2026 set so far — QP2607 + QP2601

Instrument → papers demanding it. **Two papers is not a trend**; this is a counting exercise to be
re-read when the six-paper set exists.

| Instrument | QP2607 | QP2601 | Count |
|---|---|---|---|
| SOLAS | ✔ | ✔ | **2 / 2** |
| MARPOL Annex VI | ✔ | ✔ | **2 / 2** |
| Marine Insurance Act 1963 (India) | ✔ Q5, Q9 | ✔ Q3, Q4 | **2 / 2** — 4 questions |
| STCW | ✔ Q8 | ✔ Q2, Q9 | **2 / 2** |
| ISM Code | ✔ Q8 | ✔ Q2 | **2 / 2** |
| CLC / Fund / Bunkers | ✔ Q2 | ✔ Q4 | **2 / 2** |
| Merchant Shipping Act (India) | ✔ 2025 | ✔ 1958 *and* 2025 | **2 / 2** |
| RO Code / IACS | ✔ Q3 | ✔ Q7 | **2 / 2** |
| UNCLOS | — | ✔ Q4, Q7, Q8 | 1 / 2 |
| Salvage Convention 1989 | — | ✔ Q3, Q4 | 1 / 2 |
| IHR 2005 | — | ✔ Q6 | 1 / 2 |
| PSPC MSC.215(82) | — | ✔ Q5 | 1 / 2 |
| Casualty Investigation Code | — | ✔ Q8 | 1 / 2 |
| ESP Code | — | ✔ Q5 | 1 / 2 |
| MSC.1/Circ.1598 | — | ✔ Q9 | 1 / 2 |
| IMSBC Code | ✔ Q1 | — | 1 / 2 |
| LSA / FSS Codes | — | — | **0 / 2** |

**Observation, not conclusion:** the instruments demanded by *both* papers are the eight in the top
block. If that holds across the remaining four sittings, those eight are the corpus's core.

---

## 4. Acquisition priority

Ranked by *how much verified answer quality is currently blocked*, not by volume.

1. **STCW Convention and Code (Manila-amended).** Demanded by both papers. During QP2601 Q9 a freely
   available copy of section A-VIII/1 turned out to be the **pre-Manila 1995 text** — 70 hours per
   seven days, no 14-hour interval rule — while a search summary simultaneously asserted the modern
   77-hour figure *citing that same document*. The wrong edition was caught only by reading the PDF.
   This is the single clearest demonstration on either paper of why a controlled, edition-stamped
   corpus is worth building.
2. **ESP Code (res A.744(18) lineage).** Unblocks the Q5 class C limitation on FAIR/POOR.
3. **IMSBC Code (2023 / 2025 editions).** Carried over from the QP2607 map; unchanged.
4. **Marine Insurance Act, 1963.** Most repeatedly demanded Indian instrument across the set.
5. **UNCLOS.** Three QP2601 questions; certain to recur.

Items 1, 2 and 3 are all **licence-gated**. That is the recurring shape of the problem: the gaps are
not obscure instruments, they are the mainstream ones that cost money.

---

## 5. Two findings the corpus design must absorb

**(a) The corpus must serve superseded and repealed instruments, not only current ones.**

QP2601 Q7's correct answer is the **Merchant Shipping Act, 1958** — repealed on 15 March 2026, two
months *after* the sitting. QP2607 Q7's correct answer is the **2025 Act**. Same corpus, same
question topic, two sittings four months apart, opposite answers. Q6 shows the same shape inside a
single instrument: the IHR **as amended** says *Ship Declaration of Health*, the **original 2005**
text says *Maritime Declaration of Health*, and the rename can only be demonstrated by holding both.

A corpus that only holds "what is current" cannot serve a past-papers product at all. The existing
`editions[].versions[]` model with `effectiveFrom` / `effectiveTo` / `status` is the right shape —
this is a note that it is **load-bearing**, not optional.

**(b) Articles and regulations are different structural things.**

Q8 needs **MARPOL Article 12** — an Article of the Convention, not a regulation inside an Annex.
`BunkerConvention2001-Articles-7` shows the convention already handles this. Confirming that
`MARPOL-Articles-12` resolves distinctly from `MARPOL-I-12` should be an explicit test.

---

## 6. Handoff state

- **No `reference_shelf` entry was created.** Every QP2601 question carries none.
- **No object id was invented.** No id in this document should be treated as existing; the
  `EXISTING_OBJECT` markers are *candidates for mapping*, verified only against the identity axis
  recorded in the QP2607 map, not against the True Source store.
- **The corpus axis remains `UNKNOWN`**, exactly as for QP2607. The True Source store is separately
  governed and was not inspected during this session.
- **Next QP-track involvement** is unchanged: populate `reference_shelf` only when real resolvable
  objects are returned. Nothing before then.
