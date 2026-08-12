# QP2409 — TEMPORAL AND DONOR ANCHOR

**Paper:** QP2409 — MEO Class I, Engineering Management, **September 2024** (India)
**Printed serial:** `EM – 2409`
**Branch:** `pastpapers/qp2409-founder-review`
**MIW baseline:** `9c973596edb04db32c7bf4feb3cb5898b162662a`
**Corpus commit consumed:** `319524c24d11b2f89f33672c384b56e9ae1ab7db` (`RulesApp-Local-Input` `main == origin/main`, tracked tree clean)

> **Note on the corpus pin.** `DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §16 records
> `64977b86ed9c601e273f1d0cb55abb0461835811` as the baseline corpus commit. The corpus `main`
> has since advanced. This paper was authored against the **current** corpus state recorded
> above, on explicit Founder instruction not to reset the corpus to an older pin. The commit
> actually consumed is recorded here, which is what §16's own rule requires.

Built **before** any answer was authored, as `TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md`
requires. Nothing below is inherited from intake metadata; every position was established for
**this** sitting.

---

## 1. THE HEADLINE FINDING — ON THIS PAPER THE PULL RUNS *FORWARD*

`DESKTOP_QP_ALLOCATION_2024.md` §6.3 states the standing rule for the whole 2024 batch:

> The unsolved sitting is the **earlier** one. Every donor available to a 2024 paper is a **2025
> or 2026** answer … any currency correction made for the later sitting must be reversed.

**That rule does not describe this paper, and applying it mechanically here would be an error.**

All three verified donors for QP2409 are **earlier 2024 sittings**, solved after the allocation
was written:

| Question | Donor | Donor sitting | Direction | Gap |
|---|---|---|---|---|
| `QP2409-Q6` | `QP2402-Q2` | **February 2024** | **FORWARD** (donor is earlier) | 7 months |
| `QP2409-Q8` | `QP2404-Q5` | **April 2024** | **FORWARD** (donor is earlier) | 5 months |
| `QP2409-Q9` | `QP2404-Q4` | **April 2024** | **FORWARD** (donor is earlier) | 5 months |

The danger therefore **inverts**. It is not that the donor imported something too late; it is
that the donor may **omit something that happened between its sitting and this one**. The
question to ask of every donor on this paper is the opposite of the batch-standard question:

> *What happened between the donor's sitting and September 2024 that the donor's author could
> not have known?*

That window — **February/April 2024 → September 2024** — is audited at §5. It is not assumed
to be empty; it is checked and found to contain **MSC 108** and nothing that touches these
three questions.

### 1.1 The allocation predicted two donors. There are three.

`DESKTOP_QP_ALLOCATION_2024.md` §5 records QP2409 at **2 verified donors**, "both from QP2404
and QP2506". Re-derivation against the **current** solved corpus — including the three completed
desktop papers read from their branch git objects — returns **three**:

- `QP2402-Q2` is a donor **only because this desktop team solved QP2402** as paper #3. It did
  not exist as a donor when the board was written. It is an **EXACT** stem match, the strongest
  relationship on the paper.
- `QP2506-Q1` (June 2025) is **rejected** in favour of `QP2404-Q4` for Q9 — see §4.3.

This is the concrete vindication of the standing rule that a frozen `reuse_tier` goes stale the
moment another paper is solved. The frozen intake recorded **all nine** questions as tier `C`
with **no donor**. That is wrong for three of them.

---

## 2. THE SITTING, AND THE BOUNDARIES AROUND IT

September 2024 is a **late-2024** sitting and the first of the late-2024 block.

| Boundary | Date | Position at this sitting |
|---|---|---|
| 33rd IMO Assembly resolutions adopted | **6 December 2023** | **BEFORE** — the `A.11xx(33)` editions are operative |
| **MEPC 81** | **18–22 March 2024** | **BEFORE** — MEPC 81 output exists and is available |
| **MSC 108** | **2024, first half** | **BEFORE** — see §2.4 |
| **MEPC 82** | **30 September – 4 October 2024** | **AFTER — but only just. The sharpest edge on this paper** |
| MSC 109 | December 2024 | AFTER |
| **MLC 2022 amendments enter into force** | **23 December 2024** | **AFTER** — approved but not yet in force |
| FuelEU Maritime applies | 1 January 2025 | AFTER |
| `MSC.560(108)` enters into force | 1 January 2026 | AFTER (adopted before, in force after) |
| 34th IMO Assembly | 3 December 2025 | AFTER |
| Merchant Shipping Act 2025 commences | 15 March 2026 | AFTER |

The MEPC 81 / MEPC 82 dates are carried as `INTERNAL_REUSE_VERIFIED` from the committed
February-2024 anchor (`QP2402_TEMPORAL_AND_DONOR_ANCHOR.md` §1), which established them from
IMO's published meeting record.

### 2.1 MEPC 82 is the defining temporal fact of this paper

**The most recent MEPC at this sitting is MEPC 81 (March 2024).** MEPC 82 opened on
**30 September 2024** — at or after the very end of the examination month, and certainly after
the paper was set. This single fact governs **Q3** and constrains **Q7**.

Two specific consequences, both of which a careless answer gets wrong:

- **`MEPC.395(82)` — the 2024 SEEMP Guidelines, adopted 4 October 2024 — does not exist at this
  sitting.** The operative SEEMP development guidelines are **`MEPC.346(78)`** (2022). The corpus
  instrument log records `MEPC.346(78)` as "SUPERSEDED by MEPC.395(82) (2024)" — that supersession
  is **after** this paper and must not be read back into it.
- Anything reported as a **MEPC 82 outcome** is unavailable. At this sitting the comprehensive
  impact assessment of the mid-term measures is *awaiting* its finalized report, which
  `MEPC.377(80)` §6.2 schedules **for MEPC 82**.

### 2.2 Indian statute

**The Merchant Shipping Act, 1958 governs throughout.** The Merchant Shipping Act, 2025
(Act No. 24 of 2025, assent 18 August 2025) commenced **15 March 2026** — eighteen months after
this sitting — per notification S.O. 1244(E), as recorded in the corpus instrument log at
`true-source/06-india-law-and-dg-shipping/Merchant-Shipping-Act-2025/INSTRUMENT_LOG.md`. It must
not appear in any answer on this paper. This is a live contamination risk on **Q5(b)**, which
asks squarely about Indian Government initiatives, and a solved donor for the 2025 Act exists in
the corpus (`QP2607-Q7`). That donor is **rejected** for this paper — see §4.4.

The **Coastal Shipping Act 2025** is likewise after this sitting and must not appear.

### 2.3 MLC — approved is not in force

Established from the corpus instrument log at
`true-source/04-ilo-instruments/MLC-2006/INSTRUMENT_LOG.md`, which verifies the amendment chain
against the ILO's own 2026 Compendium:

| Amendment set | Approved | Entry into force | Position at September 2024 |
|---|---|---|---|
| 2014 (financial security — abandonment) | ILC 103rd | in force | **OPERATIVE** |
| 2016 (harassment and bullying) | ILC 105th | **8 January 2019** | **OPERATIVE** |
| 2018 (wages while held captive) | ILC 107th | **26 December 2020** | **OPERATIVE** |
| **2022** | ILC 110th (2022) | **23 December 2024** | **APPROVED BUT NOT IN FORCE — three months after this sitting** |
| 2025 | ILC 113th (June 2025) | expected 2027 | Does not exist |

The Convention itself entered into force **20 August 2013**.

> **`APPROVED ≠ ADOPTED ≠ IN FORCE.`** The 2022 amendments were approved by the International
> Labour Conference in 2022 — before this sitting — and entered into force **after** it. An
> answer that presents them as operative in September 2024 is wrong.

**Controlled check, not an assumption.** The relevant provisions for Q5 are Regulation 4.5 and
Standard A4.5. Their text was extracted from three separate ILO editions held in the corpus —
the pre-2022 copy, the 2022 consolidated text and the 2026 Compendium — and compared
mechanically. **They are character-identical across all three** (the only differences are a
running-header artefact and one line-break hyphen). Standard A4.5 was therefore untouched by the
2014, 2016, 2018 and 2022 sets, and quoting it from the Compendium is safe for a September 2024
sitting. This was verified rather than presumed, because quoting a post-sitting consolidation is
exactly how a temporal error enters an otherwise correct answer.

### 2.4 STCW — the comprehensive review is in progress, not law

Established from the corpus instrument log at
`true-source/03-imo-instruments/STCW/INSTRUMENT_LOG.md`.

The operative instrument at this sitting is the **STCW Convention and Code, 2017 consolidated
edition**, as amended by:

- `MSC.416(97)` / `MSC.417(97)` — in force **1 July 2018** — **OPERATIVE**
- `MSC.486(103)` / `MSC.487(103)` — in force **1 January 2023** — **OPERATIVE**

And **not** by:

- **`MSC.560(108)`** — mandatory minimum training on the prevention of harassment, bullying and
  sexual assault, Table A-VI/1-4. **Adopted 2024, entry into force 1 January 2026.** At this
  sitting it is **adopted but not in force**, and it is in any event Chapter VI, not Chapter VIII.
- **The HTW comprehensive review of STCW.** The corpus log records it as
  *"IN PROGRESS, not adopted — nothing from it may be cited as law."* At September 2024 it is an
  **industry transition underway** and is described as such in Q1, not as a requirement.

### 2.5 GHG — the position at September 2024

Established by reading **`MEPC.377(80)` in full at source** from the corpus
(`true-source/03-imo-instruments/GHG-instruments/_base-and-amendments/MEPC.377(80).pdf`).

| Instrument | Status at September 2024 |
|---|---|
| **`MEPC.377(80)`** — 2023 IMO GHG Strategy, adopted **7 July 2023** | **OPERATIVE.** Revoked the 2018 Initial Strategy from that date (operative paragraph 6) |
| `MEPC.376(80)` — LCA guidelines (well-to-wake) | Operative; referenced by Strategy §3.2 and §4.7 |
| EEXI, operational CII, enhanced SEEMP | **IN FORCE since 1 January 2023** |
| CII guidelines G1–G5 | Operative editions |
| SEEMP development guidelines | **`MEPC.346(78)` (2022)** — `MEPC.395(82)` does not exist yet |
| **Basket of mid-term measures** | **NOTHING ADOPTED.** Architecture agreed — a technical *goal-based marine fuel standard* and an economic *GHG emissions pricing mechanism* (Strategy §4.5) — but approval is scheduled for MEPC 83 (spring 2025) and adoption for an extraordinary MEPC session thereafter |
| **IMO Net-Zero Framework / GFI** | **DOES NOT EXIST AT THIS SITTING.** The name arose at MEPC 83 in April 2025. The corpus records it as **draft, not adopted, not in force** even as at 2026-08-03. It must appear nowhere in this paper |

**Strategy §6.2 gives the examinable timeline, and it places this sitting precisely.** At
September 2024 the candidate stands between the MEPC 81 milestone ("finalization of basket of
measures") and the MEPC 82 milestone ("finalized report" of the comprehensive impact assessment),
with approval at MEPC 83, adoption at an extraordinary session about six months later, and entry
into force **16 months after adoption (2027)**.

### 2.6 The EU measures

- **EU ETS extended to maritime transport from 1 January 2024** — **operative** at this sitting.
- **FuelEU Maritime (Regulation (EU) 2023/1805)** — adopted September 2023, **applies from
  1 January 2025**. **Adopted but future.** It must not be described as applying.

---

## 3. TEMPORAL CLASSIFICATION OF EVERY QUESTION

Required by the work order. Each time-sensitive issue is classified into one of the five states.

| Q | Subject | Classification | Risk |
|---|---|---|---|
| Q1 | STCW Ch VIII fitness for duty | **Operative before sitting** (2017 edition + 2023 amendments). `MSC.560(108)` **adopted but future**. STCW comprehensive review **industry transition underway** | LOW–MEDIUM |
| Q2 | Goal-Based Standards | **Operative before sitting** — SOLAS II-1/3-10 and the GBS framework long predate it | LOW |
| Q3 | Revised IMO GHG Strategy | **Operative before sitting** (`MEPC.377(80)`). Mid-term basket **not yet available**. Net-Zero Framework **not yet available**. FuelEU **adopted but future** | **HIGH** |
| Q4 | IOPC Funds | **Operative before sitting.** 1971 Fund **superseded/wound up before sitting** | LOW–MEDIUM |
| Q5 | MLC social security + India | MLC as amended through **2018** operative; **2022 amendments approved but future**. MS Act 2025 **not yet available** | **HIGH** |
| Q6 | Bunker Convention / CLC 92 | **Operative before sitting** — both long in force | LOW |
| Q7 | GISIS | **Operative before sitting.** MARPOL Annex VI regs 17 and 18 operative | LOW |
| Q8 | AFS Convention | **Operative before sitting** — cybutryne controls in force **1 January 2023**. Certificate transition **still running** at the sitting | MEDIUM |
| Q9 | Rudder efficiency devices | No temporal content — hydrodynamics | LOW |

---

## 4. DONOR ADJUDICATION — DERIVED, NOT INHERITED

The pool was every solved question on this baseline **plus** the three completed desktop papers
read from their branch git objects (`QP2401` @ `37af6d4`, `QP2412` @ `48badc3`, `QP2402` @
`af5a8d9`) — **sixteen solved papers**. Candidates were scored on the normalised printed stem by
both token-overlap and sequence similarity, and every candidate above threshold was adjudicated
by **reading both printed stems**.

### 4.1 `QP2409-Q6` ← `QP2402-Q2` — **EXACT**, accepted

Stem similarity **1.000** on both measures. The two printed stems are **character-identical**,
including the four unmarked lettered limbs and the undifferentiated printed `(16)`.

- **Marks delta:** NIL.
- **Wording delta:** NIL.
- **Temporal delta:** NIL. CLC 92 in force since 1996, the Bunkers Convention since
  21 November 2008. No amendment boundary falls between February and September 2024.
- **Evidence:** `QP2402-Q2` carries its article-level content as `INTERNAL_REUSE_VERIFIED` from
  `verification/QP2509/Q7.md`, which read **both treaty texts in full**. Neither text is held in
  the corpus. That evidence boundary is carried forward unchanged and re-declared.

**An exact question is not an exact answer.** The answer is re-anchored to September 2024 and the
sitting-relative statements re-authored. Because the substance is treaty text unchanged between
the two sittings, the re-anchoring confirms rather than alters — and that was **checked**, which
is the point.

`QP2509-Q7` (September 2025) is a **rejected** alternative: it is a later sitting, and its limb
structure differs materially (it asks for liability and compulsory insurance as printed limbs and
never asks for the definition of *bunker oil*). Using it directly would import a later answer
across thirteen months for no gain, when an exact same-year donor exists.

### 4.2 `QP2409-Q8` ← `QP2404-Q5` — **EXACT** but for one printed character, accepted

Stem similarity **0.995**. The only difference is that the **April 2024** source copy prints the
third alternative as **"(Ill)"** — a capital I and two lower-case Ls — where **this** September
2024 copy prints it correctly as **"(iii)"**. Both are reproduced exactly as printed in their
respective specs.

- **Marks delta:** NIL — 8 + 8 both sittings.
- **Wording delta:** the single enumeration artefact above. The examiner demand is identical.
- **Temporal delta:** NIL, and **checked in the forward direction**. Cybutryne controls under
  `MEPC.331(76)` entered into force **1 January 2023**, before both sittings. Nothing in the AFS
  regime changed between April and September 2024. The certificate transition was still running
  at **both** sittings.
- **Note on direction:** `QP2404-Q5` already records `reused_from: QP2409-Q8` as an *undirected
  recurrence family edge* — at that time QP2409 was an answerless intake object and supplied no
  content. **That direction now reverses.** QP2404-Q5 is built and verified; QP2409-Q8 is not.
  QP2404-Q5 is a genuine **answer donor** here.

### 4.3 `QP2409-Q9` ← `QP2404-Q4` — **EXACT**, accepted; `QP2506-Q1` rejected

Two candidates, and the choice between them matters.

| Candidate | Sitting | Similarity | Verdict |
|---|---|---|---|
| **`QP2404-Q4`** | **April 2024** | **1.000 — character-identical** | **ACCEPTED** |
| `QP2506-Q1` | June 2025 | 0.971 token / 0.717 sequence | **REJECTED** |

`QP2506-Q1` prints "contribute **in** improving" and "rudder-efficiency **improvement** devices"
where both 2024 sittings print "contribute **to** improving" and "**improvements** devices".
`QP2404-Q4` is a **character-identical, same-year, earlier** donor. Preferring a June 2025 donor
over it would pull an answer backwards across nine months for no benefit whatever. Rejected on
the §6.3 principle even though §6.3's usual direction does not apply here.

**Temporal delta:** NIL. Hydrodynamics is not dated law; all four named devices predate both
sittings by decades.

### 4.4 Rejections — donors considered and refused

| Rejected donor | For | Why refused |
|---|---|---|
| `QP2509-Q7` (Sep 2025) | Q6 | Later sitting; different printed limbs; an exact same-year donor exists |
| `QP2506-Q1` (Jun 2025) | Q9 | Later sitting; two-word wording delta; a character-identical same-year donor exists |
| `QP2412-Q6` (Dec 2024) | Q5 | **CONTENT-FAMILY ONLY, NOT A DONOR.** Same convention, different question — it asks for the *structure* of the MLC and *DMLC Parts I and II*. This question asks for **social security** under Title 4 and an **Indian** limb, neither of which the donor addresses. It is also a **later** sitting. Recorded as a cross-link, not as `reused_from` |
| `QP2607-Q7` | Q5(b) | Merchant Shipping Act **2025** — commenced 15 March 2026. Pure contamination risk |
| `QP2506-Q8`, `QP2508-Q4`, `QP2601-Q9`, `QP2602-Q4`, `QP2404-Q7` | Q1 | **NOT DONORS.** All are the *"Human Element in the STCW Code + IMO fatigue guidance"* question. Similarity 0.35–0.41 is generic-prose noise. This question asks for the **criteria for fitness for duty under Chapter VIII** — a different provision and a different demand. Rejected after reading both stems |
| everything scoring ≥ 0.30 for Q2, Q3, Q4, Q7 | — | **NO GENUINE CANDIDATE.** The top scorers are unrelated questions (ship operating costs, CII rating, marine tribology) matching on prose shape alone. These four are **fresh research** |

**Reuse count was not optimised for.** Six of nine questions are fresh research. Correct
September-2024 answers are the objective.

### 4.5 Host recurrence hints — used for discovery only

The source copy carries third-party host annotations (`2023/OCT/Q8 2024/FEB/Q2` on Q6;
`2023/JAN/Q2 2024/APR/Q5` on Q8; five prior sittings on Q9). These are **not MIW truth**, they
point backwards only, and **no `reused_from` was written from them**. In each case the donor was
established independently by stem re-derivation and confirmed by reading both printed stems. They
must not leak to any candidate-facing surface.

---

## 5. THE FORWARD-PULL WINDOW AUDIT — February/April 2024 → September 2024

Because every donor on this paper is **earlier** than the sitting, the window between them is
audited explicitly rather than assumed empty.

| Event in the window | Date | Touches a donor question? |
|---|---|---|
| **MSC 108** | 2024, first half | **NO.** Its STCW output `MSC.560(108)` is Chapter VI training and does not enter into force until 1 January 2026. Nothing in it touches the Bunkers Convention, the AFS Convention or rudder hydrodynamics |
| MEPC 81 | 18–22 March 2024 | **NO** for Q6 and Q9. For Q8, MEPC 81 made no change to the AFS regime. (MEPC 81 is *before* the April donor in any event, so it is inside the donor's own knowledge for Q8 and Q9) |
| Any AFS amendment | — | **NONE** in the window |
| Any Bunkers/CLC amendment | — | **NONE** in the window |

**Conclusion: the forward pull is benign on all three donors.** No proposition in any donor was
rendered incomplete by an event between its sitting and September 2024. This was established by
audit and is recorded, not presumed.

---

## 6. CORPUS USE

| Instrument | Held? | How used on this paper |
|---|---|---|
| **STCW 2017 consolidated edition** | **YES** — `official-sources/STCW-2017.pdf` | **READ AT SOURCE for Q1.** Regulation VIII/1, Regulation VIII/2 and Section A-VIII/1 read in full by page render (the PDF carries no text layer). **P1 PRIMARY VERIFIED** |
| **`MEPC.377(80)`** | **YES** | **READ AT SOURCE for Q3** — vision, levels of ambition, indicative checkpoints, guiding principles, timelines, the mid-term basket and the §6.2 milestone table. **P1 PRIMARY VERIFIED** |
| **MLC 2006** | **YES** — ILO 2026 Compendium + two earlier editions | **READ AT SOURCE for Q5.** Regulation 4.5, Standard A4.5 and Guideline B4.5, plus the three-edition identity check at §2.3. **P1 PRIMARY VERIFIED** |
| **MARPOL Annex VI** | Citation-level only | Regulations **17** (reception facilities) and **18** (fuel oil availability and quality) resolved through the consumer adapter for **Q7**; chapter 4 regulations 22, 23, 26, 27 and 28 for **Q3**. Resolves to identity and provenance, **never to text** — which is all this paper needs |
| LSA Code | Held, quotation-ready | Not required by any question on this paper |
| FSS Code | Held, not quotation-ready | Not required by any question on this paper |
| DG Shipping circulars | **NO** — placeholder collection, acquisition gap RQ-35 | **Q5(b) evidence gap declared.** The Indian limb is written at concept level from the MLC and the MS Act 1958 framework. No circular number is invented |
| AFS Convention, IOPC/Fund/CLC/Bunkers, SOLAS consolidated text, GBS resolutions | **NO** | **Evidence gaps declared** on Q2, Q4, Q6 and Q8. Content is carried as authoritative restatement or as verified internal reuse, and is labelled as such |

**No corpus object was modified.** No `TRUE_SOURCE_CORRECTION_REQUEST` arose from this paper.

---

## 7. SOURCE VERIFICATION

| | |
|---|---|
| Source copy | `meoclass1/pastpapers/docs/SEPTEMBER 2024.pdf` — third-party scan, `source_authority: unverified` |
| **Printed serial** | **`EM – 2409`** — matches the paper identity. The strongest identity check, and it passes |
| Pages | **2**, both read |
| Questions | **9**, Q1–Q9, all present |
| Marks | Every question **16**. Q2, Q5, Q7, Q8 print `8 + 8`; Q9 prints `4 + 4 + 4 + 4`; Q1, Q3, Q4, Q6 print an undifferentiated `(16)` |
| **Transcription reconciliation** | **All nine `text_verbatim` strings were matched mechanically against the born-digital text layer of the PDF. All nine are present verbatim.** No retyping |
| `official_source_verified` | **false** — no DG Shipping / MMD copy has been located. Unchanged |

### 7.1 Printed anomalies — preserved, not corrected

1. **The marks do not sum.** Instruction 2 says all questions carry equal marks and six are to be
   answered, against a printed **Total Marks – 100**. Nine questions at 16 gives six answered
   questions **96**, not 100. Printed on the source; recorded in `marks_note`; not normalised.
2. **Q1 prints "STCW Chapter 8"** in Arabic numerals where the Convention numbers its chapters in
   Roman — **Chapter VIII**. Reproduced as printed and noted.
3. **Q7 limb (a) prints the question mark mid-sentence**, before the parenthetical expansion:
   *"component of GISIS? (Global Integrated Shipping Information System of the IMO) and how it
   facilitates"*. Reproduced as printed.
4. **Q6 prints `(16)` as a whole-question total** with four unmarked lettered items, so sub-part
   marks are null.
5. **Q8 prints "(iii)" correctly** where the April 2024 sitting prints "(Ill)". Both preserved in
   their own specs; the difference is recorded as the entire wording delta between the two.

The **`sr_no` field reads `QP-2409`**, which is the repository's internal identifier convention
applied uniformly across all 28 specs — it is not a transcription of the printed serial. The
printed serial `EM – 2409` is recorded here and in every verification record.

---

## 8. WHAT THIS PAPER DELIBERATELY DOES NOT SAY

A contamination sweep target list, stated positively so it can be checked mechanically.

- **IMO Net-Zero Framework**, **GFI**, draft MARPOL Annex VI chapter 5 — did not exist
- **`MEPC.395(82)`** and every other MEPC 82 output — days too late
- **MLC 2022 amendments presented as in force** — three months too early
- **Merchant Shipping Act 2025**, **Coastal Shipping Act 2025** — eighteen months too early
- **`A.12xx(34)`** and every 34th Assembly instrument — fifteen months too early
- **`MSC.560(108)` presented as in force** — adopted before, in force 1 January 2026
- **FuelEU Maritime presented as applying** — applies 1 January 2025
- **Any outcome of the STCW comprehensive review presented as law** — in progress only
- **Any CLC monetary limitation figure** — amendable by tacit acceptance, and not asked for
- **Any invented DG Shipping circular number** — the collection is an acknowledged gap
