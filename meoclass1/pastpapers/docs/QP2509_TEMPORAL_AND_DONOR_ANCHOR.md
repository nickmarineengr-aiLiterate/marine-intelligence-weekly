# QP2509 — SEPTEMBER 2025 — TEMPORAL AND DONOR ANCHOR

**Status: PRE-AUTHORING. No answer has been authored. `specs/QP2509.json` is untouched
intake.**

This document is the verified input to the QP2509 authoring session. It exists because the
temporal research and the donor adjudication are separable from, and must precede, the
authoring — and because a session that runs out of budget mid-paper must leave behind
something complete rather than a half-authored spec (`PASTPAPER_PRODUCTION_PROTOCOL.md` §3).

Governed by `PRODUCTION_PROTOCOL_INDEX.md`. Read with
`TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md`.

---

## 1. SOURCE VERIFICATION — COMPLETE, PASS

Printed copy `meoclass1/pastpapers/docs/SEPTEMBER 2025.pdf`, 2 pages, extracted with PyMuPDF
and compared field-by-field against `specs/QP2509.json`.

| Check | Printed | Spec | Result |
|---|---|---|---|
| Serial | `Sr. No. EM – 2509` | `EM - 2509` | match |
| Sitting | `SEPTEMBER 2025` | September 2025 | match |
| Authority | `EXAMINATION OF MARINE ENGINEER OFFICER` | same | match |
| Function | Marine Engineering Management at Management Level | same | match |
| Class / subject | `M.E.O CLASS – I` / `ENGINEERING MANAGEMENT` | same | match |
| Time / marks | `3 HOURS` / `Total Marks – 100` | same | match |
| Region note | `(India 2025)` | same | match |
| Instructions | 4 printed (NB 1–4) | 4 | match |
| Questions | Q1–Q9 | 9 | match |
| Stems | — | — | **9 / 9 verbatim, 0 mismatches** |
| Marks | all 16 under instruction 2 | 16 | match |
| `printed_marks_absent` | Q1, Q6, Q8 print no allocation | flagged on Q1, Q6, Q8 | match |

**No source correction is required before authoring.**

### 1.1 Printed anomalies — reproduce, do not fix

- **Q9** prints `SOLAS ch.ll-1` — lowercase L twice, where the instrument is chapter **II-1**.
  The spec reproduces the printed form. The answer must address chapter II-1 while the
  verbatim stem keeps the printed error.
- **Q8** prints a capital `B).` for its second limb against a lowercase `a)` for the first.
- **Q1, Q6, Q8** print no marks allocation at all; recorded at 16 under printed instruction 2.
- **Q6** carries an unusually long host annotation block spanning 2018–2022 sittings.

### 1.2 Provenance boundary

The printed copy is a third-party scan. **The host is not named here**: this repository is
public, and host identity is recorded only in the git-ignored local file. Two classes of
content on the scan are **discovery-only** and must not reach any shipped surface:

- host branding — the page header and footer marks, an app promotion and two book-purchase
  blocks;
- the host's printed recurrence annotation on every question, held as `host_recurrence_hint`.

`recurrence_check.py` and `health_check.py` enforce both, and `known_traps_check.py` trap 14
sweeps the whole repository — **including this `docs/` tree** — for host branding. An earlier
draft of this file named the host while describing the rule and was correctly rejected by that
trap. Source PDFs are never committed.

---

## 2. DONOR MAP — RECOMPUTED FROM CURRENT SOLVED STATE

Computed with the corrected derivation committed at `0d7f872`
(`recurrence_model.donor_readiness`), **not** from the stored `reuse_tier` field.

Corpus at computation: **252 questions / 90 solved / 162 unsolved**, 10 fully solved papers.

| Q | Short title | Tier | Preferred donor | Wording | Other donors | Family (unsolved) |
|---|---|---|---|---|---|---|
| Q1 | Bauxite casualties and safe carriage | **C** | — | — | — | singleton |
| Q2 | CII — commercial impact and shortcomings | **D** | `QP2508-Q2` | EXACT | `QP2602-Q2` | — |
| Q3 | Particular and general average, adjusters | **D** | `QP2607-Q5` | EXACT | `QP2601-Q3`, `QP2604-Q3` | — |
| Q4 | Maritime lien, in rem and in personam | **C** | — | — | — | `QP2404-Q3`, `QP2512-Q9` |
| Q5 | HNS Convention — scope and certification | **C** | — | — | — | `QP2503-Q6` |
| Q6 | Communication, barriers, decarb hazards | **C** | — | — | — | singleton |
| Q7 | Bunker Convention 2001 vs CLC 92 | **C** | — | — | — | singleton |
| Q8 | IMO/ILO human element, fatigue guidance | **C** | — | — | — | singleton |
| Q9 | Classification societies, survey types | **D** | `QP2606-Q8` | EXACT | — | `QP2412-Q4` |

**Tier D: 3 / 9.** Unchanged by the derivation fix — QP2509 was 3/9 under the stored field and
is 3/9 derived. The fix moved five *other* questions (§5.1 of the reuse map); none is in this
paper.

### 2.1 The QP2506 report's expectation is NOT borne out

The QP2506 handover suggested QP2509 was likely stronger than the stored map showed, with
useful existing coverage for Q7 (Bunker / CLC 92) and Q8 (human element). **Measured against
donor readiness, it is not.** Q7 and Q8 are both **family singletons** — no other sitting in
the transcribed corpus set either task, so there is no donor at any tier.

That is not the same as saying there is no leverage, and the distinction is the one the
protocol insists on: **a recurrence family is not a research neighbourhood.** Q8 in particular
has substantial *topical* leverage in already-verified material — the fatigue limb overlaps
verification records for `QP2602-Q4`, `QP2601-Q9`, `QP2604-Q9`, `QP2506-Q8` and `QP2508-Q4`,
which between them read `MSC.1/Circ.1598` in full text, and the Manila-amended `A-VIII/1`
rest-hour figures against a competent-authority restatement after rejecting a pre-Manila IMO
copy. That is reusable **research**, not a donor, and it must be re-read and re-anchored
rather than transplanted.

Promotion of Q7 or Q8 to tier **B** would be a legitimate outcome of the authoring session —
but only from a session that has actually read the candidate objects. It cannot be asserted
here.

### 2.2 Donor deltas — the three the protocol requires

Direction: for all three tier-D questions the donor is a **later** sitting pulled backwards, so
any currency correction made for the donor's sitting must be **reversed**, not inherited.

**Q2 ← `QP2508-Q2` (August 2025).**
- *Question delta:* nil. Marks-normalised stems identical.
- *Marks delta:* nil. 10 / 6 both sittings.
- *Temporal delta:* **one month.** This is the closest donor pair anywhere in the corpus.
  Nothing in the CII regime changed between August and September 2025 — see §3.2 — so the
  regulatory truth is stable across the gap. The second donor `QP2602-Q2` (February 2026) is
  five months the *other* side of the October 2025 extraordinary session and must not be used
  without reversing that.

**Q3 ← `QP2607-Q5` (July 2026).**
- *Question delta:* nil against `QP2607-Q5` (EXACT). `QP2601-Q3` and `QP2604-Q3` are reworded
  and are why `QP2607-Q5` is preferred despite being further away.
- *Marks delta:* nil, 16 both.
- *Temporal delta:* **ten months backwards, and it crosses the Merchant Shipping Act 2025
  commencement of 15 March 2026.** General average itself is contractual (York-Antwerp Rules)
  and unaffected, but any Indian statutory limb must be re-anchored — see §3.7.

**Q9 ← `QP2606-Q8` (June 2026).**
- *Question delta:* nil (EXACT).
- *Marks delta:* nil, 10 / 6 both.
- *Temporal delta:* **nine months backwards, crossing 15 March 2026.** The class-rule and
  SOLAS II-1 limbs are stable; the Indian statutory survey limb is not. `QP2412-Q4`
  (December 2024) is the unsolved third family member — solving Q9 converts it.

---

## 3. TEMPORAL SWEEP — SEPTEMBER 2025

Sitting date: **September 2025**. The printed copy gives the month only; **no day is
printed**. Where a day-level boundary could matter, that is stated explicitly below rather
than assumed away.

Legend: **VERIFIED** — established this session against a source named in the row.
**TO VERIFY** — must be read at source during authoring; the risk is identified, the answer
is not yet established.

### 3.1 Q1 — Bauxite, IMSBC Code · VERIFIED (edition) · residual TO VERIFY

**Operative edition at the sitting: IMSBC Code amendment 07-23 (2023 edition)** — voluntary
from 1 January 2024, **mandatory from 1 January 2025**, therefore in force in September 2025.

Amendment 07-23 is the edition that carries the *dynamic separation* apparatus — the
definition, and the "cargoes which may undergo dynamic separation" category describing the
formation of a liquid slurry above the solid material producing a free-surface effect. That is
the post-*Bulk Jupiter* (January 2015) response and is central to this question.

TO VERIFY at authoring, in the Code text itself: the exact schedule structure for bauxite
(the Group C `BAUXITE` schedule against the Group A `BAUXITE FINES` schedule), the moisture
and particle-size criteria that separate them, and the TML/moisture-content carriage
requirements. **Do not** state the group classification from secondary summaries — the search
material consulted this session was inconsistent about it.

### 3.2 Q2 — CII · VERIFIED · **the approved/adopted gap**

At September 2025:

- CII regulations have been in force since **1 January 2023**; first ratings issued 2024 on
  2023 data.
- MARPOL Annex VI **regulation 28.11** requires the review of the short-term measure to be
  **completed by 1 January 2026** — so at the sitting the review is *live and incomplete*.
- **MEPC 83 (April 2025) APPROVED** draft amendments to regulations 20, 25 and 28, circulated
  by IMO Circular Letter No. 5005 of 11 April 2025, **with a view to adoption at the
  extraordinary session MEPC/ES.2 in October 2025**.
- MEPC 83 also approved the work plan for **phase 2** of the review.

**The trap.** October 2025 is *after* this sitting. At September 2025 those amendments were
**approved, not adopted, and not in force**. The same is true of the IMO Net-Zero Framework,
which was approved at MEPC 83 for adoption at the same October 2025 extraordinary session.

- The answer must not say the amendments were adopted.
- The answer must not import any MEPC/ES.2 (October 2025) or later outcome.
- The `QP2602-Q2` donor (February 2026) sits *after* that session and will state the
  post-adoption position. **Reversing this is mandatory if that donor is consulted.**
- The `QP2508-Q2` donor (August 2025) sits one month before and is on the correct side.

### 3.3 Q5 — HNS Convention · VERIFIED · **HIGHEST RISK IN THE PAPER**

At September 2025 the 2010 HNS Protocol was **NOT in force**, and its entry-into-force
conditions had **NOT been met**.

The forward timeline, none of which existed at the sitting:

| Event | Date |
|---|---|
| Belgium, Germany, Netherlands, Sweden ratify | April 2026 |
| Article 21 entry-into-force conditions met | **29 May 2026** |
| Convention enters into force | **29 November 2027** |
| Contracting States as at 30 June 2026 | 13 |

**Every one of those facts is unusable for this paper.** A present-day source will volunteer
all of them; an answer that absorbs any of them is wrong for September 2025.

The printed stem's own words — *"The HNS Convention is expected shortly to come into force"* —
are the state of expectation at the sitting and must be **preserved, not corrected**. The
study-guide layer is where the candidate is told what has happened since.

**On the number of Contracting States: do not quote one.** The per-State accession dates could
not be established this session (`hnsconvention.org/status` lists States without dates; the
IMO treaty database was not read). Four of the thirteen are known to post-date the sitting by
seven months, but the September-2025 figure cannot be derived by subtraction without the other
nine dates. Under `PASTPAPER_PRODUCTION_PROTOCOL.md` §2.1 an unverifiable quantity is
**omitted, not quoted**. The three printed limbs — substances covered, types of damage, and
why a products tanker needs CLC + Bunker + HNS certificates — are answerable without a state
count, and limb (c) is the real weight of the question.

TO VERIFY at authoring, in the Protocol/Convention text: the substance categories by reference
to the constituent instruments (MARPOL Annex I/II/III, IBC, IGC, IMSBC/IMDG), the damage heads
including the exclusion boundary against CLC and Bunkers, and the certification architecture.

### 3.4 Q8 — Human element, MLC and fatigue · VERIFIED · **a three-state trap**

This is subtler than "do not import later amendments", and getting it wrong in *either*
direction is an error at this sitting.

| Instrument | State at September 2025 |
|---|---|
| MLC 2006 **2022 amendments** (ILC 110) | **In force since 23 December 2024** — fully operative |
| MLC 2006 **2025 amendments** (ILC 113) | **ADOPTED 6 June 2025** — three months *before* the sitting — but **not in force**; expected late December 2027 |
| `MSC.1/Circ.1598` fatigue guidelines | Approved MSC 100, 24 January 2019; current at the sitting; supersedes `MSC/Circ.1014` |
| STCW comprehensive review | Ongoing; nothing adopted at the sitting |

**So the September-2025 answer must place the 2025 amendments in the adopted-but-not-in-force
state.** Omitting them entirely is a temporal error, because they were adopted before the
candidate sat the paper. Applying them as operative is the opposite error. This is exactly the
"approved ≠ adopted ≠ in force" rule in `TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md` §1.

TO VERIFY at authoring: the substantive content of the 2025 amendments as adopted, and the
`A-VIII/1` Manila rest-hour figures — the corpus already records that a freely available IMO
copy of `A-VIII/1` was the **superseded pre-Manila text** and was rejected. Do not repeat that
mistake.

### 3.5 Q7 — Bunker Convention 2001 / CLC 92 · TO VERIFY · low risk

Both instruments long in force and stable across the sitting; no amendment boundary near
September 2025 was identified. All four limbs — pollution damage and exclusions, time limits,
shipowner liability and limitation, compulsory insurance and financial security — must be read
in the convention texts at authoring, and the CLC/Bunkers boundary stated precisely rather
than by analogy. Limb (c) of Q5 depends on the same boundary; author the two together.

### 3.6 Q3, Q4 — private maritime law · TO VERIFY · low risk, one statutory limb each

- **Q3 general average.** York-Antwerp Rules apply **by contract**, so the operative version is
  whichever is incorporated — the corpus already records Rule VII as materially identical
  across 1994 / 2004 / 2016, and that the 2016 Rules were read in full for `QP2607-Q5` and
  `QP2601-Q3`. The Indian statutory counterpart is the **Marine Insurance Act 1963** (s.66
  supplies the definition and the right to rateable contribution). Stable across the sitting.
- **Q4 maritime lien.** The convention limb points at the **1993 International Convention on
  Maritime Liens and Mortgages** and its order of settlement. **Verify India's party status
  before asserting it applies to an Indian-flag scenario** — this has not been established and
  must not be assumed from the fact that the question asks about it.

### 3.7 The Merchant Shipping Act boundary · VERIFIED · applies to Q3, Q4, Q9

**The Merchant Shipping Act 2025 commenced 15 March 2026 and repealed the 1958 Act by
s.324(1). September 2025 is six months BEFORE that.**

So for QP2509 the operative Indian statute is the **Merchant Shipping Act 1958**, and this is
a **backwards** trap: two of the three donors (`QP2607-Q5` July 2026, `QP2606-Q8` June 2026)
sit *after* commencement and will state the 2025 Act. Reusing either without reversing the
statute is a **statute regression**.

The corpus records this failure mode concretely: an April 2026 sweep found the 1958 Act
asserted on **eight separate surfaces of a single question object** — model answer, study
guide, `recall_15s`, `major_trap`, an `answer_route` core point, a retrieval card,
`regulations` and `search_aliases`. **Expect eight again, in reverse.**

### 3.8 Indian carriage law, 10 September 2025 · VERIFIED NOT LOAD-BEARING

The Bills of Lading Act 2025 and the Carriage of Goods by Sea Act 2025 both commenced
**10 September 2025** — mid-month, and the printed copy gives no sitting day. That is a
genuine unresolvable ambiguity **if** any question turned on it.

**None does.** Read across all nine printed stems: Q1 is cargo carriage under the IMSBC Code,
not contract of carriage; Q3 is general average under the York-Antwerp Rules and the Marine
Insurance Act 1963; Q4 is maritime lien and arrest, not bills of lading; Q7 is pollution
liability. No question raises a bill of lading, a contract of carriage, or a carrier's
obligations or immunities.

**Therefore the day-level sitting date does not need to be resolved for this paper.** Record
the reasoning; do not silently rely on it. Any future September-2025 question touching
carriage law would make the missing day load-bearing and would need the sitting date
established first.

### 3.9 Instruments explicitly checked and found NOT load-bearing

Recorded so a later session does not re-open them (§2 of the temporal protocol: record the
answer either way, including "checked, no temporal issue").

| Raised as a risk | Finding |
|---|---|
| Maritime cyber `MSC-FAL.1/Circ.3/Rev.3` (issued 4 April 2025, six elements) | **Not load-bearing.** No QP2509 question concerns cyber risk management. Rev.3 was operative at the sitting had it been needed. |
| Merchant Shipping Act 2025 back-dating | **Load-bearing — see §3.7.** Must NOT be back-dated. |
| CII review / phase timing | **Load-bearing — see §3.2.** |
| HNS status | **Load-bearing — see §3.3, highest risk.** |
| MLC later amendments | **Load-bearing — see §3.4, and in both directions.** |
| Indian carriage law transition | **Not load-bearing — see §3.8.** |

---

## 4. AUTHORING POSTURE PER QUESTION

| Q | Route | Primary-source burden | Note |
|---|---|---|---|
| Q1 | fresh | IMSBC Code 07-23 schedules read at source | edition verified; classification not |
| Q2 | donor `QP2508-Q2`, re-anchored | MARPOL Annex VI reg 28; MEPC 83 outcome | one-month delta; do not cross October 2025 |
| Q3 | donor `QP2607-Q5`, re-anchored | YAR 2016; MIA 1963 s.66 | reverse MS Act 2025 → 1958 |
| Q4 | fresh | 1993 Liens & Mortgages Convention; MS Act 1958 | verify India's party status |
| Q5 | fresh | 2010 HNS Protocol text | **quote no state count**; preserve "expected shortly" |
| Q6 | fresh | **largely non-regulatory** | see below |
| Q7 | fresh | Bunkers 2001 and CLC 92 texts | author with Q5 limb (c) |
| Q8 | fresh | MLC 2006 as amended; `MSC.1/Circ.1598` | three-state framing mandatory |
| Q9 | donor `QP2606-Q8`, re-anchored | SOLAS II-1; HSSC | reverse MS Act 2025 → 1958 |

**Q6 is the worked case for the newly clarified `PASTPAPER_PRODUCTION_PROTOCOL.md` §2.1.**
Communication theory, communication barriers, and the hazards of a two-platform main-engine
decarbonisation carried out by two groups are **engineering and human-factors** questions. No
instrument prescribes a taxonomy of communication types or a list of decarbonisation
communication hazards. Recognised references, class technical material and sound engineering
reasoning are acceptable authority for those limbs; the provenance class must be **stated
rather than disguised**; and no regulation number may be manufactured to make the question look
primary-sourced. Where the answer does touch governed ground — permit-to-work, risk assessment
and toolbox-talk obligations under the ISM Code — that limb carries the ordinary primary
burden.

---

## 5. WHERE THIS SESSION STOPPED, AND WHY

**Stopped before authoring. Deliberately, and at a clean boundary.**

`PASTPAPER_PRODUCTION_PROTOCOL.md` §3: *"There is no valid half-authored-paper state. Either
the paper is complete and internally consistent, or the session stops and records exactly where
it stopped and why."*

Nine answers at this corpus's standard is not a partial-credit task — the solved specs run
300–500 KB each and every load-bearing limb is read at source and recorded. This session spent
its budget on the machine preflight, the donor-readiness defect and its regression coverage,
the source-authority clarification, source verification and this temporal sweep. Beginning to
author with what remained would have produced exactly the state the protocol forbids.

**`specs/QP2509.json` is therefore untouched.** The corpus is unchanged at 252 / 90 / 162.

The next session starts at §4 above with the temporal work already done and verified.

### Carried forward as TO VERIFY

1. IMSBC Code 07-23 — bauxite schedule structure and group classification, at source (§3.1).
2. 2010 HNS Protocol — substance categories, damage heads, certification (§3.3).
3. MLC 2025 amendments — substantive content as adopted (§3.4).
4. `A-VIII/1` rest hours — competent-authority restatement only; the freely available IMO copy
   is the superseded pre-Manila text (§3.4).
5. Bunkers 2001 and CLC 92 — all four limbs at source (§3.5).
6. India's party status to the 1993 Liens and Mortgages Convention (§3.6).
7. Whether Q7 or Q8 earns promotion to tier **B** once the candidate corpus objects are read
   (§2.1).
