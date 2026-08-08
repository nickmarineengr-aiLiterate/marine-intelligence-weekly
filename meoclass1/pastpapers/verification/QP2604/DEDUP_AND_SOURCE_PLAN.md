# QP2604 — DEDUP AND SOURCE PLAN

**April 2026, Engineering Management, MEO Class I.**
Written 2026-08-09, before authoring, and completed at the close of production.

---

## 1. Method

Every April stem was compared against **all 36 previously built stems** — not only the
obvious topic matches — using two measures:

- **byte equality** of the raw transcribed stems, which is what an EXACT claim requires;
- **`difflib` normalised similarity** on a case-, whitespace- and punctuation-folded form,
  which is what a NEAR claim rests on.

**The host recurrence table printed on the source copy was never used to establish a
classification.** It is discovery evidence only. April is the paper that proves why — see §3.

---

## 2. Result of the sweep

**324 pairwise comparisons. ZERO byte-exact matches.**

**April is the first paper in the set containing no exact repeat of any previously built
question.** March contained three.

| April Q | Best normalised match | Score | Class | Tier |
|---|---|---|---|---|
| Q1 | (none — best 0.271 was noise) | 0.2710 | **TOPIC** | C |
| Q2 | QP2602 Q3 / QP2603 Q8 | 0.6409 | **NEAR** | D |
| Q3 | QP2601 Q3 | 0.8656 | **NEAR** | D |
| Q4 | QP2601 Q4 | **0.9946** | **NEAR** | D |
| Q5 | (none — best 0.248 was noise) | 0.2483 | **NONE** | C |
| Q6 | QP2601 Q6 / QP2603 Q4 | 0.1527 | **NEAR** | D |
| Q7 | QP2601 Q7 | 0.1880 | **NEAR** | D |
| Q8 | QP2601 Q8 | 0.9177 | **NEAR** | D |
| Q9 | QP2601 Q9 / QP2602 Q4 | 0.4382 | **NEAR** | D |

**EXACT 0 · NEAR 7 · TOPIC 1 · NONE 1.**

### March's "no middle ground" finding did not survive

March recorded that a question is *"either identical to a prior one or clearly unrelated in
wording"* — exactly three pairs above 0.5, all at 1.0000. April produces a genuine
**gradient**: 0.995, 0.918, 0.866, 0.641, 0.641, 0.438. The finding was true of March and is
not a property of the series.

### The similarity ratio is length-sensitive and must not be used alone

**Q6 scores 0.1527 against a question whose four tasks map one-to-one**, because April runs to
764 characters against January's 453. **Q7 scores 0.1880 on the same three limbs.** Both were
classified on a **task-by-task comparison**, not on the ratio. A session that ranked by score
alone would have called both of them NONE and re-authored two answers from scratch.

---

## 3. The two host-table findings, in opposite directions

| | What the host table says | What string comparison shows |
|---|---|---|
| **Q2** | lists `2026/FEB/Q3` and `2026/MAR/Q8` — implying a third instance of a known **exact** pair | **NEAR, 0.6409.** Limb a) re-punctuated; limb b) rewritten to a broader task |
| **Q6** | lists **only this sitting** | **NEAR** against QP2601 Q6 and QP2603 Q4 — a relationship the table omits entirely |

**The table over-claimed on one question and under-claimed on another, on the same paper.**
This is the strongest evidence in the five-paper set for the standing rule that a host
recurrence annotation establishes topic recurrence at most.

---

## 4. Dedup tiers

| Tier | Meaning | April |
|---|---|---|
| **A** | existing deep MIW answer reusable as-is | **0** |
| **B** | partial overlap; propositions reused, answer synthesised | **0** |
| **C** | new to the corpus | **2** — Q1, Q5 |
| **D** | prior past-paper reuse after delta and currency review | **7** — Q2, Q3, Q4, Q6, Q7, Q8, Q9 |

**Tier D does not mean copy.** Every Tier D question here answers a question whose printed
wording differs from its source, and two of them (Q7, Q9) required a limb to be re-authored.

### Where the reuse comes from

**Six of April's nine questions map onto the January paper, at the same question number** —
Q3↔Jan Q3, Q4↔Jan Q4, Q6↔Jan Q6, Q7↔Jan Q7, Q8↔Jan Q8, Q9↔Jan Q9. April reads as a
systematic re-issue of January with limbs and marks made explicit and several limbs widened.

---

## 5. Source plan by question

| Q | Primary sources actually read | Licence gate |
|---|---|---|
| Q1 | **MARPOL Article 16 (1)–(9) in full** | No licensed IMO consolidated MARPOL — edition state recorded as `C` |
| Q2 | Reuse. FSA Guidelines, MSC.550(108), MSC.555(108) re-checked | SOLAS II-2, FSS Code, IMDG — all still gated |
| Q3 | Reuse. Salvage Convention 1989, MIA 1963 s.66, YAR re-checked | York-Antwerp Rules are a copyright contractual code |
| Q4 | Reuse + statute re-anchor. CLC/Fund/Bunkers/LLMC/Nairobi, MIA 1963 | Convention texts gated |
| Q5 | **MEPC.378(80) in full** — operative clauses, s.2, s.10, s.11 | None — freely published |
| Q6 | Reuse. IHR 2005 as amended, Annex 3 models, Art 39 | Indian Port Health Rules 1955 — restatement only |
| Q7 | **UN treaty status record**; Constitution of India by effect; MS Act 2025 via QP2607 Gazette work | None blocking |
| Q8 | **MSC.255(84) re-read at source** | SOLAS XI-1/6 and I/21 texts gated |
| Q9 | Reuse. MSC.1/Circ.1598, STCW VIII/1 and A-VIII/1, MLC 2006 | Licensed STCW Code still not held |

---

## 6. Errors caught before they entered the paper

1. **Q8 — a fabricated numeric threshold.** A search summary asserted that *"severe damage to
   the environment means a discharge of 50MT or more of pollutant."* The Code says nothing of
   the kind: paragraph **2.19** defines it as damage which, as evaluated by the State(s)
   affected or the flag State, produces a **major deleterious effect upon the environment** —
   an evaluative test, not a tonnage threshold. Caught by opening the instrument. The January
   answer was checked and is clean.
2. **Q1 — a wrong threshold in circulation.** Several published summaries give the objection
   threshold for a tacit MARPOL amendment as *two thirds*. Article 16(2)(f)(iii) says **one
   third of the Parties, or Parties holding 50 per cent of world tonnage, whichever is
   fulfilled**.
3. **Q7 — a missed re-anchor.** The hand-built patch list re-anchored the model answer, study
   guide, recall line, major trap, route point and retrieval card onto the Merchant Shipping
   Act 2025, and **missed the Regulation and source map**, which still asserted the 1958 Act
   was operative. Caught only by the sweep of the assembled spec. This is March's finding
   reproducing exactly.
4. **Vocabulary drift.** April Q5 was initially recorded as `no_recurrence`; the corpus already
   uses **`new`** for this class, including for March Q2, the set's first NONE. Corrected.

---

## 7. What was deliberately NOT done

- No source object id was invented. **`reference_shelf` is empty on all nine questions.**
- No fuel- or resistance-penalty percentage was quoted for biofouling.
- No national biofouling arrival standard was reproduced.
- No clause numbers were cited from any instrument MIW does not hold.
- Q6's printed limb marks were **not** normalised to make them sum to 16.
