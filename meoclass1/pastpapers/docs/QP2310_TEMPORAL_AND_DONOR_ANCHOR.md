# QP2310 — OCTOBER 2023 — TEMPORAL AND DONOR ANCHOR

**Paper:** QP2310 · October 2023 · printed serial `2310 EM`
**Branch:** `pastpapers/qp2310-founder-review`
**Baseline:** `149a10f8b1fc81788522724d2432be61979ed9f5` (`origin/main` at session start; merge-base proven)
**Authored:** 2026-08-14, desktop (`Dani-Desktop`)

Authority for method is `DESKTOP_QP_PRODUCTION_PLAYBOOK.md`; year-level authority is
`DESKTOP_QP_ALLOCATION_2023.md` §3. This file records only what is specific to October 2023.

---

## 1. SOURCE IDENTITY — established from the printed copy

| Field | Printed |
|---|---|
| Month / year | `OCTOBER 2023` |
| Serial | **`2310 EM`** — number first, no `Sr. No.` prefix, no dash (the reversed 2023 convention) |
| Authority | `EXAMINATION OF MARINE ENGINEER OFFICER` |
| Function | Marine Engineering Management at Management Level |
| Subject | `ENGINEERING MANAGEMENT` |
| Class | `M.E.O CLASS – I` |
| Time | `TIME ALLOWED - 3 HOURS` |
| Total | `Total Marks – 100` |
| Region | `(India 2023)` |
| Pages | **2** |
| Questions | **9**, counted by reading both pages, not by pattern match |

**Serial check passes.** `2310` is consistent with October 2023 and with the eleven-paper 2023
intake in which `2305` is absent. This is not a reprint of another sitting: no question on this
paper reproduces a whole other 2023 paper, and the three same-year relations found (Q5, Q6, Q7)
are single-question recurrences, not a wholesale reprint.

### 1.1 Numbering — uniform, unlike January and February 2023

October prints `Q1.` through `Q9.` consistently. It does **not** carry the January `Q8)` / bare
`9.` variants or the February bare `4.` / `5.` variants recorded in the allocation §1.3. The
extractor risk for this paper is therefore low, but the nine questions were still counted by
reading, as required.

### 1.2 Printed anomalies — preserved, not normalised

| Where | Printed | Class |
|---|---|---|
| Q1 | `hull Forms` — capital F mid-sentence | capitalisation |
| Q1 | `energy efficiency of ship :(i)` — space before colon, none after | spacing |
| Q1 | `(i) Forebody optimization` but `(ii) Aftbody Optimization` | inconsistent casing |
| Q3 | `Port State control` then `port State control` in the same question | inconsistent casing |
| **Q4** | opens **`A.`** and never prints a `B.` — an orphan lettered part | **structure** |
| Q5 | `vis-a-vis` — unaccented | spelling |
| Q5 | `Scavenge Air Moisturizing` — the industry term is *moistening* (SAM) | spelling |
| **Q5** | limb A `(8)`, limb B `(16)` — **sum 24 against an equal-marks rubric** | **marks** |
| Q8 | `other similar Convention such as CLC’92` — singular where plural is meant | grammar |
| **Q9** | **no mark figure at all**, neither total nor limb — the only such question | **marks** |
| Q9 | `‘active failures’ and ‘latent failures.` — opening quote never closed | punctuation |

The two marks anomalies are the load-bearing ones and are handled as follows.

- **Q5.** The printed `(8)` and `(16)` cannot be an arithmetic split of an equal-marks question.
  Sub-part marks are left **null** rather than repaired to `8+8` or the total inflated to 24.
  Both printed figures survive inside `text_verbatim`. This is the same treatment QP2303-Q4 gave
  the same question when *its* limb B printed no figure at all — the printed asymmetry is a
  standing feature of this stem across sittings, not a scan defect.
- **Q9.** `printed_marks_absent: true`; recorded at 16 under printed instruction 2.

### 1.3 Editorial and host furniture — excluded from the transcription

The copy carries a page watermark, running headers and footers, two promotional blocks, and a row
of the host's own backward-looking sitting references beneath every question. None of it is
examination content. The recurrence rows are captured per question in `host_recurrence_hint` as
**discovery-only** provenance; everything else is dropped. **The host is not named in this
repository.**

---

## 2. OCTOBER 2023 TEMPORAL LINE

Sitting date: **October 2023**, month only — **no day is printed**, so no day-dependent claim may
be made and no week-granularity distance may be computed from this sitting.

### 2.1 Operative at the sitting

| Instrument / position | Status at October 2023 |
|---|---|
| **Merchant Shipping Act, 1958** | **The governing Indian statute.** |
| **32nd IMO Assembly** (adopted December 2021) | **Operative.** `A.1155(32)` *Procedures for Port State Control, 2021* is the applicable PSC procedures resolution. |
| **EEXI and CII** | **Operative since 1 January 2023** — the whole year. |
| **MEPC.328(76)**, Revised MARPOL Annex VI | **In force 1 November 2022** — see §2.4. This is the Annex VI text applicable at this sitting. |
| **2023 IMO GHG Strategy** | **Adopted 7 July 2023 at MEPC 80.** October is after that date, so the 2023 Strategy — not the 2018 Initial Strategy — is the operative statement of IMO ambition. |
| Most recent **MEPC** | **MEPC 80**, 3–7 July 2023. |
| Most recent **MSC** | **MSC 107**, May–June 2023. |
| **MEPC.346(78)** 2022 SEEMP guidelines | Operative. |
| Global sulphur limit 0.50 % m/m | Operative since 1 January 2020; 0.10 % m/m in ECAs. |
| **AFS Convention** as amended | Operative; **cybutryne controls applied from 1 January 2023**. |
| **CLC 1992** and the **Bunker Convention 2001** | Both long in force; India is a party to both. |
| **LLMC 1976 / 1996 Protocol**, limits as raised by the 2012 amendments | The raised limits have applied since **8 June 2015**. |
| **MLC 2006** as amended through the **2018** set | Operative. |
| **ISM Code** as amended through `MSC.353(92)` | Operative. |
| **Casualty Investigation Code**, `MSC.255(84)` | Operative. |
| **SOLAS** | The 2020 consolidated edition is the current one. |
| **HSSC guidelines**, `A.1156(32)` | The applicable Assembly survey-guidelines resolution. |

### 2.2 Future at the sitting — PROHIBITED in any answer

| Item | Date | Why it is a trap here |
|---|---|---|
| **33rd IMO Assembly**, `A.11xx(33)` | adopted **6 December 2023** | **Two months after this sitting.** `A.1185(33)` PSC Procedures must **not** be cited on Q3. |
| **MEPC 81 / 82 / 83** | 2024–2025 | Q5 and Q6 both invite drift here. |
| **MEPC.385(81)** major-conversion amendment to Annex VI reg 13.2.2 | adopted March 2024 | Directly contaminates Q5 if the donor's consolidated text is carried. |
| **MSC 108** resolutions | adopted May 2024 | — |
| **SOLAS Consolidated Edition 2024** | 1 July 2024 | — |
| **EU ETS** applied to maritime | 1 January 2024 | Attractive but future on Q5 and Q6. |
| **MLC 2022 amendments** | in force 23 December 2024 | Adopted, **not** in force. |
| **Hong Kong Convention** | in force **26 June 2025** | Its entry-into-force *conditions were met* in June 2023, but it is **not in force** at this sitting. |
| **IMO Net-Zero Framework / GFI** | October 2025 | — |
| **34th Assembly**, `A.12xx(34)` | 3 December 2025 | — |
| **Merchant Shipping Act, 2025** | commenced 15 March 2026 | The standing statute trap for the whole 2023 batch. |

### 2.3 The 7 July 2023 GHG boundary — settled, and *not* ambiguous for this paper

The allocation §3 records 7 July 2023 as the intra-year boundary that splits the batch, and warns
that **July 2023 cannot be resolved** because the paper prints no day. **October is unambiguously
after the boundary.** The 2023 IMO GHG Strategy is available and operative for this sitting. No
day-dependent reasoning is required and none is used.

This does not reach any question on this paper directly — no question asks about GHG ambition —
but it fixes the year-position of Q5 and Q6, which sit in the Annex VI space.

### 2.4 `MEPC.328(76)` entry into force — the corpus register is wrong, and it matters (TSCR-3)

The corpus amendment register records the entry into force of `MEPC.328(76)` as **2023-11-01**.
The resolution's own operative paragraph 3 reads **1 November 2022**, and its operative paragraph 2
records deemed acceptance on 1 May 2022.

**The register date is wrong by one year.** Taken at face value it would place the Revised Annex VI
*one month after* this October 2023 sitting and would force the answer onto a superseded text.

**Standing position carried, unchanged: `MEPC.328(76)` entered into force 1 November 2022 and is
the Annex VI text applicable at this sitting.** This is `TSCR-3`, already raised by the producer
team; it is **not** repaired from this branch, and QP production never edits True Source.

This finding was established on QP2303 and is *carried*, not re-derived — but it is re-stated here
because Q5 of this paper depends on it exactly as QP2303-Q4 did.

### 2.5 The 33rd Assembly boundary — the sharpest trap on this paper

October 2023 sits **two months before** the 33rd Assembly adopted on 6 December 2023. Q3 is a port
State control question and the single most likely contamination is citing `A.1185(33)` *Procedures
for Port State Control, 2023*. **The applicable resolution at this sitting is `A.1155(32)`, adopted
December 2021.** Every donor available for Q3 sits at or after December 2023 and therefore carries
the 33rd-Assembly text; each was reversed.

Note the shape of the rule the batch has now applied three times: **an Assembly boundary is the
adoption date, not the meeting month.**

---

## 3. DONOR MAP — Q1 to Q9

Every donor below was adjudicated by **reading both printed stems**. Host recurrence rows were used
for discovery only and created no edge.

| Q | Topic | Donor | Donor sitting | Direction | Class |
|---|---|---|---|---|---|
| **Q1** | Hull form optimisation — forebody, aftbody, twin skeg | `QP2402-Q3` | February 2024 | **+4 later** | **EXACT** |
| **Q2** | Annual surveys · items examined · condition of class | `QP2304-Q9`(b) · `QP2402-Q7` | April 2023 · Feb 2024 | −6 earlier · +4 later | **FAMILY** |
| **Q3** | PSC — regional agreements · future · effectiveness | `QP2312-Q2` · `QP2406-Q3` | Dec 2023 · Jun 2024 | +2 · +8 later | **FAMILY** |
| **Q4** | Turbocharging — pulse converter, sequential, 2-stage, VGT | `QP2408-Q8` | August 2024 | **+10 later** | **FAMILY** |
| **Q5** | Primary vs secondary NOx · SAM · EGR | **`QP2303-Q4`** | **March 2023** | **−7 EARLIER** | **EXACT** |
| **Q6** | GISIS aim, function, fuel oil module | **`QP2301-Q9`** | **January 2023** | **−9 EARLIER** | **EXACT** |
| **Q7** | LLMC — purpose, heads of claim, legal terms | **`QP2301-Q5`** | **January 2023** | **−9 EARLIER** | **EXACT** |
| **Q8** | Bunker Convention 2001 vs CLC ’92 | `QP2402-Q2` | February 2024 | **+4 later** | **EXACT** |
| **Q9** | Root cause analysis · active and latent failures | `QP2412-Q5` | December 2024 | **+14 later** | **EXACT** |

**Six exact, three family.** That is materially better than the 5/9 readiness figure the allocation
§4 recorded for this paper on 2026-08-13, and the reason is exactly the one §2 of the allocation
predicted: **three 2023 papers have since been solved and have become this paper's donors.**

### 3.1 The systemic 2023 fact no longer holds universally — record this

Allocation §2 states that *every* donor available to *any* 2023 question is later than the sitting
it donates to. **That is now false for this paper.** Q5, Q6 and Q7 draw on **earlier same-year
sittings** — March 2023 and January 2023 — and Q2's family donor `QP2304-Q9` is April 2023.

This changes the risk profile in a specific way that must not be over-read:

- **An earlier donor cannot drag later law backwards.** For Q5, Q6 and Q7 the *forward* trap is
  therefore closed at source.
- **But an earlier donor does not automatically contain later amendments either.** Between January
  and October 2023 the year moved: **MEPC 80 sat and the 2023 GHG Strategy was adopted on 7 July
  2023.** A January-2023 donor states "the most recent MEPC session is MEPC 79, of December 2022".
  **That statement is false at October 2023 and was reversed forward** on Q6.

Both directions were checked on every question. Neither is assumed.

### 3.2 Donor read from a pushed review branch — declared

`QP2303-Q4` (the Q5 donor) is **not on `main`**. It sits on `origin/pastpapers/qp2303-founder-review`
and has not yet been laptop-reviewed or integrated. It was used because the printed stems are an
exact match and because it is the only **earlier same-year** treatment of this question in
existence, which is worth more here than a later, laptop-reviewed alternative.

**The dependency is declared rather than hidden.** Everything carried from it was re-derived
against the October 2023 line, and the technical substance was re-reasoned rather than copied. It
is recorded as an evidence limitation in §5 and in Q5's verification record. If the laptop returns
corrections on QP2303-Q4, Q5 of this paper should be re-read against them.

`QP2301` (Q6, Q7 donors) and `QP2304` (Q2 donor) **are** on `main`, integrated after laptop review.

---

## 4. NECESSARY REVERSALS — what was changed and why

| Q | Donor statement | Reversed to, at October 2023 |
|---|---|---|
| **Q3** | Donors at and after December 2023 rest on the 33rd Assembly PSC procedures | **`A.1155(32)`, adopted December 2021.** `A.1185(33)` is two months future and is excluded. |
| **Q3** | Donor material framed by post-2023 MoU developments | Regional MoU position stated as at 2023; no post-sitting expansion asserted. |
| **Q5** | Donor cites Annex VI reg 13 **as consolidated to 1 May 2024**, which incorporates `MEPC.385(81)` | **Revised Annex VI as introduced by `MEPC.328(76)`, in force 1 November 2022.** `MEPC.385(81)` excluded entirely. |
| **Q6** | Donor (January 2023) states "the most recent MEPC session is MEPC 79, December 2022" | **MEPC 80, 3–7 July 2023** — a **forward** correction of an earlier donor. |
| **Q6** | Donor's `QP2409` ancestry framed the module at September 2024 | Anchored to the examiner's own October 2023 premise. |
| **Q7** | Later donors (`QP2506-Q5`, `QP2602-Q1`) sit under the 34th Assembly and, for the 2026 one, the MS Act 2025 | **MS Act 1958**; LLMC limits as raised with effect from 8 June 2015; no later instrument. |
| **Q8** | Donor `QP2402-Q2` is February 2024 | Re-anchored; no 2024 instrument used. `QP2304-Q7` (April 2023) cross-checked as the same-year control. |
| **Q9** | Donor is December 2024 | Re-anchored; the Casualty Investigation Code and human-element guidance cited are all pre-2023. |
| **Q2** | `QP2402-Q7` HSSC material is February 2024 | HSSC stated on `A.1156(32)`; no 33rd-Assembly survey guidelines. |
| **Q4** | Donor is August 2024 and treats *different* turbocharger developments | Nothing regulatory carried; the four named methods authored from engineering first principles. |

---

## 5. EVIDENCE LIMITATIONS AND REFERRALS

Recorded honestly and carried into the per-question `reverify_before_publication` register. **None
of these blocks the paper** — they are class B or C.

1. **MARPOL Annex VI is citation-ready but not quotation-ready** in True Source. Q5 and Q6 cite
   Annex VI at **corpus identity level only**; no Annex VI text is quoted and no sub-paragraph is
   reproduced. `C_ACCEPTED_LIMITATION`.
2. **`TSCR-3` remains open.** The corpus amendment register still records `MEPC.328(76)` entry into
   force as 2023-11-01 against the resolution's own 1 November 2022. **Not repaired from this
   branch.** The correct date is used and the discrepancy is declared. Referral: producer team.
3. **The Q5 donor sits on an unreviewed branch** — see §3.2. `C_ACCEPTED_LIMITATION`.
4. **The GISIS module list is administrative** and changes without any instrument being amended; it
   is stated as expressly non-exhaustive. `B_CURRENCY_CHECK`.
5. **Regional PSC MoU membership and coverage figures** are administrative and move; Q3 states the
   framework and names the regimes without asserting a membership count for a date it cannot
   verify. `B_CURRENCY_CHECK`.
6. **"Condition of class"** (Q2 limb C) is a **classification-society** term, not a convention
   term. Its definition and consequences are drawn from settled class practice and the IACS unified
   framework rather than from a statutory instrument, and the answer says so.
   `C_ACCEPTED_LIMITATION`.
7. **The examiner's premise in Q6** — that GISIS had "recently" updated its fuel oil module — is
   accepted as the examiner's framing and anchored to the sitting. No specific release date was
   verified. `C_ACCEPTED_LIMITATION`.
8. **India's LLMC position** (Q7). The Merchant Shipping Act 1958 Part XA gives effect to limitation
   of liability in Indian law. The answer states the Convention scheme and identifies the Indian
   statutory vehicle without asserting a ratification instrument or date that was not read this
   session. `C_ACCEPTED_LIMITATION`.

**No corpus enrichment job was launched from this branch and no True Source file was edited.**

---

## 6. QA RECORD — WHAT THE CHECKS ACTUALLY CAUGHT

The paper passed the governed toolchain, but not on the first pass. Three real defects were
found and fixed, and they are recorded here rather than quietly corrected.

### 6.1 Production vocabulary on a candidate-facing surface

The word **"donor"** reached the rendered page eleven times, and **"laptop-reviewed"** once —
in `verification_status`, `reverify_before_publication` and `unresolved`, all of which the
builder renders. `QP2301.html`, which has been laptop-reviewed and integrated, carries the word
**zero** times. This is the QP2406 review lesson §6.3 exactly: *donor*, *before publication*,
*reverify* and *production protocol* stay out of every candidate-facing field.

All twelve were reworded to candidate-meaningful language — "the later paper", "MIW's own
earlier treatment of the identical question", "not yet integrated into the published corpus".
`reuse_evidence`, `question_delta` and `temporal_review` were **left alone**, having first been
confirmed by string probe *not* to be rendered.

### 6.2 A spec-shape defect that broke a global builder

`build_reuse_map.py` raised `KeyError: 'pages'`. The cause was mine: `pages`, `printed_serial`
and `printed_serial_note` had been written at the top level and inside `transcription_verified`,
where every other spec in the corpus carries them **inside `source_copy_provenance`**. Proved by
controlled test — the reuse map builds cleanly with `QP2310.json` removed and fails with it
present. The fields were moved to the house position; the scanner was **not** weakened.

### 6.3 The temporal sweep was controlled, not merely run

The sweep returned **35 candidates** on QP2310. Every one was adjudicated against its
surrounding text and every one is a **post-sitting date named in order to exclude it** —
`A.1185(33)` at 6 December 2023, `MEPC.385(81)` at March 2024, the MS Act 2025 at 15 March 2026,
and the wrong `2023-11-01` register date. A zero-result sweep would have been the suspicious
outcome here, not a clean one.

The sweep was then **positively controlled**: a deliberate forward contamination was seeded into
Q1 (`the IMO Net-Zero Framework of October 2025 applies to this ship`), the sweep fired on it,
and the seed was removed with the spec restored and the build proved byte-identical to its
pre-seed state.

### 6.4 Everything else

| Check | Result |
|---|---|
| `validate_spec` | **0 errors**, 9 warnings (all model-answer length, the house norm) |
| `audit_paper` | **0 errors, 0 warnings** across all 13 checks |
| Deterministic double build | **byte-identical**, run four times across the session |
| Spec line endings | **LF only**, 0 CRLF |
| `known_traps_check` | 233 checks, **0 failures** |
| `recurrence_check` | **0 failures**; host annotations create no family edge |
| Full `run_toolchain` | every stage **PASS** except the delivery gate |
| HTTP UI, 1280 and 375 | 9 cards · 5 modes · **Answer default** · search · deep links · **no overflow at either width** · **no console errors** |
| Candidate-facing leakage | **zero** — no host name, no host recurrence rows, no paper ids, no production vocabulary |

**The delivery gate fails by design on this branch.** It requires 400 derived artefacts to be
committed; §13.2 forbids exactly that here. Every one of them was regenerated to validate and
then **reverted**, along with `solvedQP/QP2310.html`. The branch carries only its twelve
paper-owned files.

---

## 7. WHAT THIS PAPER ADDS TO THE 2023 BATCH

- **October is the first 2023 paper solved that sits after the 7 July 2023 GHG boundary** and can
  resolve it without ambiguity. That resolution is recorded here for QP2308 and QP2311 to reuse.
- **It is the first 2023 paper with a majority of *backward* same-year donors.** The allocation's
  §2 universal statement should be read as describing the batch at its start, not as a standing
  rule.
- **The 33rd Assembly boundary is now settled in both directions**: QP2312 settled it for a
  December sitting; this paper settles it for the last sitting *before* adoption.
