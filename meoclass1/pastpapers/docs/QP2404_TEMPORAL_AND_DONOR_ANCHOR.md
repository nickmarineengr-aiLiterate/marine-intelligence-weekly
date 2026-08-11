# QP2404 — TEMPORAL AND DONOR ANCHOR

**Paper:** QP2404, April 2024. Serial `EM-2404`. **Sitting date governs every answer.**

Written before authoring, from primary and authoritative sources read this session. Governed by
[`TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md`](TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md).

---

## 1. THE APRIL 2024 LINE

Everything below was **already true** at the sitting and may be written as operative:

| Instrument | State at April 2024 | Established from |
|---|---|---|
| STCW 1978 as amended, **Manila amendments** | in force **1 January 2012** | settled |
| **MSC.1/Circ.1598** (fatigue guidelines) | issued **January 2019** | settled |
| **HTW 10** agreed the STCW comprehensive-review roadmap, methodology and 22 review areas, adoption targeted **autumn 2027** | met **5–9 February 2024** — two months before the sitting | IMO HTW 10 meeting summary |
| **EU ETS** extended to maritime transport | applies from **1 January 2024**; 40 % of 2024 emissions surrendered | EU legislation |
| **2023 IMO GHG Strategy** | adopted MEPC 80, **July 2023** | settled |
| **IGF Code** (MSC.391(95)) | in force 1 Jan 2017; detailed provisions for **natural gas only** | settled |
| **SOLAS II-1/55** alternative design and arrangements | the operative route for a fuel the IGF Code does not prescribe | settled |
| **AFS Convention 2001** | in force 17 September 2008 | settled |
| **UNCLOS 1982** | in force 16 November 1994 | settled |
| **ISM Code**, **MSC-MEPC.7/Circ.8** guidance on ISM certification | settled well before the sitting | settled |

## 2. THE LINE ITSELF — what must NOT enter any answer

| Item | Actual date | Why it is out |
|---|---|---|
| **MSC.1/Circ.1687 — Interim guidelines for the safety of ships using ammonia as fuel** | circular dated **26 February 2025**; approved at **MSC 109, 2–6 December 2024** | **Eight months after the sitting.** The single most dangerous item on this paper. |
| MSC 108 endorsement of the IGF Code alternative-fuel working plan | MSC 108, **May 2024** | one month after the sitting |
| CCC 10 finalisation of the ammonia interim guidelines | **September 2024** | after the sitting |
| **FuelEU Maritime** (Reg. (EU) 2023/1805) **applying** | applies **1 January 2025**; monitoring plans 31 August 2024 | adopted Sept 2023 and may be named as **adopted and upcoming**; must NOT be written as applying |
| IMO Net-Zero Framework | later still | out entirely |
| "as at August 2026" style statements inherited from donors | authoring-date statements | out entirely |

**Q2 is the flagged question and the flag is REAL.** At April 2024 there was **no IMO instrument or
circular governing ammonia as a marine fuel**. The draft interim guidelines were under development
at CCC (fundamental principles on toxicity agreed at **CCC 9, 20–29 September 2023**), with an
intersessional group set for September 2024. An ammonia-fuelled ship at this sitting was approved
by **SOLAS II-1/55 alternative design**, read with the IGF Code's goal and functional requirements
and classification-society rules. Ammonia **carriage as cargo** under the IGC Code is settled and
is a different matter — do not merge the two.

## 3. REVERSE-HINT ADJUDICATION — MIW ruling

Three `REVERSE_HINT_CANDIDATES.md` rows touch this paper. **All three were adjudicated by reading
both printed stems.** A host hint is discovery only; the ruling below is MIW's.

Diffs are on the **normalised** stem (`recurrence_model.normalise_stem`), so case, punctuation and
printed marks are already discounted.

| Pair | Normalised difference | Ruling | Donor consequence |
|---|---|---|---|
| `QP2404-Q4` ← `QP2506-Q1` | two words: `to`→`in`, `improvements`→`improvement` | **EXACT — same examiner task** | **NEW donor. Tier C → D.** |
| `QP2404-Q6` ← `QP2602-Q6` | one inserted word: `proper` | **EXACT — same examiner task** | already Tier D; adds a **third** donor |
| `QP2404-Q5` ← `QP2409-Q8` | one OCR artifact: `(Ill)` → `(iii)` | **EXACT — same examiner task** | **none** — counterpart is unbuilt |

**Why the queue found what the family model could not.** A family edge forms on `reused_from` or on
**exact equality** of the normalised stem. Each pair above is the same examiner task and misses
exact equality by one or two words — in Q5's case by a scanning artifact, where the source copy
prints the roman numeral `(iii)` as `(Ill)`. The exact-equality rule is deliberate and correct; the
reverse-hint queue is what reaches the cases sitting just outside it.

**Two already-built pages carry a candidate-facing statement these edges correct.** Before
adjudication `QP2506-Q1` and `QP2602-Q6` each rendered **"Once in this set"**. Both are repeats.
See the surface-impact report — this is a derived, non-target public-surface change and is reported,
not hidden.

## 4. PIL TEMPORAL SWEEP — RUN PROSPECTIVELY, BEFORE ADAPTATION

`temporal_sweep.py` was run over the donor and support specs **before** any answer was adapted.
13 findings fall on this paper's donor set. Adjudication:

| Finding | Count | Ruling |
|---|---|---|
| `INTERNAL_QREF` — `QP2506-Q6` "See Q5 of this paper"; `QP2508-Q6` "See Q1 of this paper" | 4 | **REAL RISK. Cross-reference must be DROPPED, not renumbered** — it points at an LLMC limitation question, and QP2404 has none. On QP2404 those numbers are antifouling paint and IoT. |
| `POST_SITTING` `2027` — STCW comprehensive review, on the Q7 donor family | 5 | **LEGITIMATE and sitting-known.** HTW 10 agreed the roadmap 5–9 February 2024, targeting autumn 2027. Citable at this sitting as work in progress with nothing adopted. |
| `POST_SITTING` `August 2026` — "nothing had been adopted as at August 2026" | 2 | **REAL RISK.** An authoring-date statement. Must not be carried into an April 2024 answer. |
| `2026` — "identical to three built 2026 objects" | 2 | **FALSE POSITIVE** as a temporal flag: internal corpus provenance, not a regulatory date. Rewritten anyway because the count changes. |

**Nothing was suppressed to produce a clean list.**

## 5. DONOR MAP AS AUTHORED

Derived from current build state, not from stored intake tiers.

| Q | Topic | Tier | Preferred donor | Wording | Fresh research |
|---|---|---|---|---|---|
| Q1 | IoT in the maritime industry | C | — | — | full |
| Q2 | Ammonia as a marine fuel | C | — | — | full, **temporal-critical** |
| Q3 | Maritime lien, in rem / in personam | **D** | `QP2509-Q4` | identical | re-anchor only |
| Q4 | Rudder-efficiency devices | **D** | `QP2506-Q1` | 2-word variant | re-anchor only — **via reverse hint** |
| Q5 | AFS Convention and tin-free paints | C | — | — | full |
| Q6 | General average + refloating damage | **D** | `QP2506-Q6` | identical | re-anchor, **drop the Q-reference** |
| Q7 | Human element in STCW; fatigue | **D** | `QP2508-Q4` | identical | re-anchor to April 2024 |
| Q8 | Audit vs survey; RO action on ISM certificates | C | — | — | full |
| Q9 | UNCLOS environment and maritime zones | C | — | — | full |

**4 / 9 Tier D** after adjudication, against 3 / 9 before. The gain is Q4.
