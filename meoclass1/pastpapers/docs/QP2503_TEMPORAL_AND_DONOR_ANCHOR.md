# QP2503 — TEMPORAL AND DONOR ANCHOR

**Paper:** QP2503 · MARCH 2025 · Sr. No. **EM - 2503** · MEO Class I · Engineering Management
**Branch:** `pastpapers/qp2503-founder-review`, branched from `333e814`
**Corpus commit consumed:** `319524c24d11b2f89f33672c384b56e9ae1ab7db` (`RulesApp-Local-Input` `origin/main`, 0 ahead / 0 behind, tracked tree clean)
**Written before final assembly**, as `DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §8 requires.

---

## 1. THE SITTING

The sitting month is **March 2025**. No day is printed on the source copy. Where a
boundary falls inside March 2025 that omission would matter, it is recorded here and the
answer is written so that it does not depend on the day. **No such boundary was found on
this paper** — every boundary engaged either closed before 1 March 2025 or opens after
31 March 2025.

---

## 2. STANDING BOUNDARIES — RECHECKED FOR MARCH 2025, NOT INHERITED

The Batch 2 board §8 and the January and February 2025 anchors establish boundaries for
the 2025 block. Each was **re-established against this sitting** rather than carried over.
Two of them move relative to February 2025 and one is materially different in effect.

| Boundary | Status **at March 2025** | Classification |
|---|---|---|
| **MEPC.385(81)** | Deemed accepted **1 February 2025**; enters into force **1 August 2025** | `accepted-not-in-force` |
| **MEPC.392(82)** | Adopted only; entry into force **1 March 2026** | `adopted-future` |
| **IMO Net-Zero Framework** | **Not yet approved.** Approved at MEPC 83, **April 2025** — the month *after* this sitting; adopted October 2025 | `post-sitting-prohibited` |
| **MLC, 2006 — 2022 amendments** | **In force 23 December 2024** — ten weeks before this sitting | `operative` |
| **MLC, 2006 — 2025 amendments** | Approved by the ILC at its 113th Session, **June 2025** | `post-sitting-prohibited` |
| **MSC.560(108)** | Adopted; in force **1 January 2026** | `adopted-future` |
| **34th IMO Assembly** | Resolutions adopted **3 December 2025** | `post-sitting-prohibited` |
| **33rd IMO Assembly** | Adopted 6 December 2023 — the `A.11xx(33)` editions govern | `operative` |
| **Merchant Shipping Act, 1958** | Governs throughout. Not repealed until 15 March 2026 | `operative` |
| **Merchant Shipping Act, 2025** | Act 24 of 2025, assent 18 August 2025, commenced 15 March 2026 | `post-sitting-prohibited` |
| **Coastal Shipping Act, 2025** | Post-sitting on the same reasoning | `post-sitting-prohibited` |
| **Marine Insurance Act, 1963** | Governs. `known_traps.md` §8 applies to Q5 | `operative` |
| **Admiralty (Jurisdiction and Settlement of Maritime Claims) Act, 2017** | Operative | `operative` |
| **MEPC.328(76)** — revised MARPOL Annex VI | In force 1 November 2022; the current text at this sitting | `operative` |
| **HNS Convention (1996 as amended by the 2010 Protocol)** | **Not in force.** Entry-into-force conditions not met | `adopted-future` |

### 2.1 The one boundary that is genuinely different in March 2025

**EEDI Phase 2 has closed on both of regulation 24's two timetables.** This is *not*
inherited from any earlier paper — it is established here, and it is the finding that
governs Q7.

MARPOL Annex VI regulation 24 Table 1 prints **two different phase timetables** and the
split is by ship type:

- Gas carriers of 15,000 DWT and above, all containerships, general cargo ships, LNG
  carriers and cruise passenger ships: Phase 2 ran **1 January 2020 – 31 March 2022**;
  **Phase 3 opened 1 April 2022.**
- Bulk carriers, the smaller gas-carrier bands, tankers, refrigerated cargo carriers,
  combination carriers and all ro-ro classes: Phase 2 ran **1 January 2020 –
  31 December 2024**; **Phase 3 opened 1 January 2025.**

At **March 2025**, therefore, **Phase 2 is closed for every ship type in the table**, and
for the second timetable it closed only **ten weeks before the sitting**. The printed stem
asks about "the **present** EEDI framework under Phase 2". That premise was true when the
same task was set at earlier sittings and it is **false at this one**.

The stem is **not corrected away**. It is preserved verbatim, the design content it asks
for is delivered in full — the design features are phase-independent — and the position is
stated precisely. Classification: `superseded` as to the word "present"; `operative` as to
the Phase 2 obligation itself, which still fixes the required EEDI of every ship contracted
or built into that phase and therefore still governs a large part of the existing fleet.

**Source:** True Source canonical record `MARPOLVI_REG24.json`, `temporalApplicability`,
which records the two timetables expressly and names the transplantation of one onto the
other as "the unit's most transplantable error". The corpus's export policy is
facts-and-pointers-only, so identity, structure and numerics are used and **no body text is
reproduced**.

### 2.2 The MLC boundary is load-bearing for the first time on this paper

The **2022 amendments to the Code of the MLC entered into force on 23 December 2024** and
are `operative` at this sitting. Standard **A4.3, paragraph 1(b)** now requires the
provision of "all necessary **appropriately-sized** personal protective equipment".

This was established **differentially, not asserted**: the corpus holds both the pre-2022
text and the consolidated text including the 2022 amendments, and the pre-2022 copy of
A4.3(1)(b) **contains no PPE clause at all**. The insertion is therefore proved from the
two held texts rather than inferred from a commentary. It is the hardest legal anchor
available to Q3 and it is ten weeks old at the sitting.

The **2016 amendments** on shipboard harassment and bullying (in force 8 January 2019) are
likewise `operative`.

---

## 3. DONOR RE-DERIVATION — BOARD PREDICTION VERSUS ACTUAL

Recomputed with `tools/pastpapers/recurrence_model.py` against a **simulated built set
assembled from Git objects**: the baseline `333e814` specs, overlaid with the specs read
from all six pushed Batch-1 review branches and from `pastpapers/qp2501-founder-review`
and `pastpapers/qp2502-founder-review`. That set is **198 built answers of 252 questions**,
22 papers solved of 28. Frozen intake `reuse_tier` fields were **not** consulted;
`derive_reuse_tier` was recomputed from current build state.

| Metric | Board prediction | **Actual after QP2501 + QP2502** | Verdict |
|---|---|---|---|
| Tier D at QP2503's turn | 1 / 9 | **1 / 9** | **confirmed** |
| Family reach | 5 | **5** | **confirmed** |
| Temporal flags | 3 | **3** | confirmed |
| HIGH flags | 2 | **2** (Q6, Q7) | confirmed |

### 3.1 QP2502 did **not** become a donor to this paper

The board warned that QP2502 changed the donor landscape and becomes a donor for later
family members. **Checked, and it does not reach QP2503.** No question of QP2501 or QP2502
sits in any QP2503 recurrence family. The warning is correct in general and does not apply
here; QP2502's donor edge runs to QP2406, not to March 2025.

QP2502 is nonetheless **materially useful to this paper**, as a *regulatory anchor* rather
than as a donor — see §3.4 Q7.

### 3.2 The single family donor

| | |
|---|---|
| **QP2503-Q6 ← QP2509-Q5** | September 2025 · **EXACT** printed stem, **exact** marks, **exact** subpart split |

**Direction of travel: BACKWARD.** The donor sits **six months after** this sitting. It was
examined for post-March-2025 contamination against the whole question object and is
**clean**:

- Its temporal record states that at September 2025 the Convention was not in force and
  its entry-into-force conditions had not been met. **That is equally true at March 2025**,
  so the status statement transfers without reversal.
- It asserts **no count of Contracting States** anywhere — recorded as a deliberate
  omission in its own `unresolved`. There is therefore no ratification figure to reverse.
- Its "forward timeline" was deliberately excluded from the answer object. It is excluded
  here for the same reason and additionally as `post-sitting-prohibited`.
- A whole-object year sweep returns **no post-March-2025 fact**: the only 2026 token is
  authoring metadata and the only 2022/2023 tokens are the third-party host recurrence
  hint. Every substantive provision cited is fixed by the **2010 Protocol** and is
  unaffected by entry into force.

Every sitting-relative phrase is nevertheless **re-authored for March 2025**, per
`DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §7 rule 4: *an exact question is not an exact answer*.

### 3.3 Family reach — what solving this paper unlocks

Five unsolved questions acquire a verified donor, and **all five land in QP2507
(July 2025)**:

```
QP2507-Q5 <- QP2503-Q5      QP2507-Q8 <- QP2503-Q1
QP2507-Q6 <- QP2503-Q3      QP2507-Q9 <- QP2503-Q9
QP2507-Q7 <- QP2503-Q2
```

This is the reach the board's hard ordering constraint exists to create. QP2507 must not
be taken before this paper is complete.

### 3.4 Adjudicated candidates the family model does not carry

The family model links `reused_from` edges and identical normalised stems. It cannot see a
relative that is close in substance but different in printed task. Both printed stems were
read for every candidate below and each was classified by hand.

| Question | Candidate | Sitting | Direction | Classification | Used? |
|---|---|---|---|---|---|
| **Q1** | QP2412-Q4 / QP2509-Q9 | Dec 2024 / Sep 2025 | earlier / later | **topical-only** — class role in rule formation and survey types. **Dual class is nowhere in the corpus** | **No.** Fresh |
| **Q1** | QP2501-Q3 | Jan 2025 | earlier | topical-only — CAP/CAS is a different task | No |
| **Q2** | QP2603-Q6 / QP2511-Q5 | Mar 2026 / Nov 2025 | **later** | topical-only — ESP versus CAP. Importing would pull post-sitting material for no gain | **No.** Rejected on direction |
| **Q2** | QP2601-Q5 | Jan 2026 | **later** | topical-only — coatings and the CTF | **No.** Rejected on direction |
| **Q3** | QP2412-Q1 | Dec 2024 | earlier | **topical-only** — SDG framing only. Gender, IMO gender work and the Indian limb are all absent | **No.** Fresh |
| **Q4** | QP2404-Q1 | Apr 2024 | earlier | **SHAPE-ONLY.** The stem formula is reproduced word for word — *"Maritime industries have taken several initiatives to explore new digital technologies and 'X' is one of such initiatives…"* — with the same 6 + 5 + 5 split. **Different subject matter entirely** (IoT, not 3D printing) | **Shape only.** Recorded as `shape_only`; **not** a family edge and **not** `reused_from` |
| **Q5** | QP2512-Q3, QP2606-Q3, QP2506-Q3 | Dec 2025 – Jun 2026 | **later** | topical-only — marine insurance generally | **No.** Rejected on direction |
| **Q5** | QP2401-Q1 | Jan 2024 | earlier | topical-only — *uberrimae fidei*, a different doctrine | No |
| **Q7** | **QP2410-Q8** | Oct 2024 | **earlier** | **LIMB-LEVEL.** Its limb (a) is the same examiner task one index across: design features to comply with a chapter 4 index under a "Phase 2 (of 20 % – 30 % reduction)" framing. QP2410-Q8's own donor analysis names QP2503-Q7 as its nearest stem and records that nothing was taken from it | **Yes, limb-level.** The legal frame and the dominant compliance route both invert — see below |
| **Q7** | **QP2502-Q6** | Feb 2025 | **earlier — one month** | **REGULATORY ANCHOR.** Establishes regulations 22, 24 and 5.4 against the corpus's frozen canonical records, at the immediately preceding sitting | **Yes, as anchor** |
| **Q8** | QP2403-Q4 / QP2410-Q7 / QP2510-Q4 | Mar 2024 – Oct 2025 | mixed | topical-only — high-efficiency propeller **types**, not maintenance | No |
| **Q9** | **QP2402-Q8** | Feb 2024 | **earlier** | **LIMB-LEVEL.** The closing sentence is reproduced **verbatim** — *"In accordance with the provisions under the Merchant Shipping Act, what steps should be initiated and who should initiate such steps for the safety of the ships and the marine environment."* Only the casualty differs: grounding and abandonment there, **collision with loss of life, damage and an oil spill** here | **Yes, limb-level.** The statutory machinery transfers; the casualty-specific limbs do not |
| **Q9** | QP2512-Q5 | Dec 2025 | **later** | topical-only — inquiries into casualties on **foreign** ships | **No.** Rejected on direction |

**Nine candidates were rejected on direction of travel alone.** No later answer was allowed
to import law, regulation or industry state into this sitting.

### 3.5 Why Q7's limb-level donor inverts rather than transfers

QP2410-Q8 limb (a) is about **EEXI**, and its central finding is that *EEXI is not phased*:
regulation 25 Table 3 sets a single fixed factor per ship type and size band, and the
phases belong to the required **EEDI** in regulation 24 Table 1.

QP2503-Q7 is about **EEDI**, where the phases genuinely live. So the donor's most
transferable sentence is the one that must be **reversed in emphasis**: for this question
the phase scheme is the substance, not a misattribution to be corrected. Two further
inversions:

1. **The compliance route inverts.** Most of the existing fleet met EEXI by **engine or
   shaft power limitation** — a paper change, not a design change. That route is
   essentially unavailable to a new build seeking a Phase 2 or Phase 3 required EEDI,
   because the required EEDI is set against the ship's own design and a limited-power ship
   simply is a lower-powered design. Reproducing the EEXI answer here would give a
   candidate the wrong engineering.
2. **The verification route differs.** EEXI is assessed once against the design; EEDI is
   verified in **two stages**, preliminary at the design stage and final at the sea trial —
   which is exactly what QP2502-Q6 established one month before this sitting.

---

## 4. PER-QUESTION TEMPORAL CLASSIFICATION

| Q | Risk | Classes engaged | The load-bearing boundary |
|---|---|---|---|
| Q1 | LOW | — | Class practice and the RO Code framework are stable across the window |
| Q2 | LOW | `operative` | 2011 ESP Code, resolution **A.1049(27)**, held by the corpus. Amendment chain after A.1049(27) is **open (RQ-26)** — an accepted limitation, not a currency risk for a definition question |
| Q3 | MEDIUM | `operative` | MLC **2022 amendments in force 23 December 2024**. 2025 amendments `post-sitting-prohibited` |
| Q4 | LOW | — | Engineering and industry practice; no instrument boundary |
| Q5 | LOW | `operative` | **Marine Insurance Act, 1963** — `known_traps.md` §8 |
| Q6 | **HIGH** | `adopted-future`, `donor_contamination_examined_and_cleared` | HNS **not in force**; entry-into-force conditions unmet |
| Q7 | **HIGH** | `superseded`, `operative` | **EEDI Phase 2 closed on both timetables by 1 January 2025** — §2.1 |
| Q8 | LOW | `operative` | 2023 Biofouling Guidelines are guidance, not law, and are **not held by the corpus** |
| Q9 | MEDIUM | `operative`, `post-sitting-prohibited` | **MS Act 1958** governs; the 2025 Act is twelve months of assent and twelve and a half months of commencement away |

---

## 5. EVIDENCE GAPS RECORDED RATHER THAN INVENTED

Consistent with `DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §9, where the corpus lacks an
authoritative instrument the gap is recorded and no precision is manufactured.

| Demand | Corpus position | Consequence for this paper |
|---|---|---|
| **HNS Convention text** | **NOT HELD.** No HNS object anywhere in True Source | Q6 rests on the MIW-internal record of QP2509-Q5, which read the consolidated 54-page text in full. Carried as `INTERNAL_REUSE_VERIFIED` with the corpus gap stated |
| **Merchant Shipping Act, 1958** | **NOT HELD.** The corpus holds the **2025** Act — the exact inverse of what this sitting needs | Q9 names Parts and sections as **authoritative secondary**, flagged, exactly as QP2402-Q8 recorded for February 2024 |
| **IACS URs / class rules** | **NOT HELD** (RQ-36). `CLASS_AND_SURVEY_NOTES.md` is concept level and instructs that answers be labelled *"class practice / IACS framework"*, never *"SOLAS requires"* | Q1 and Q2 follow that instruction verbatim |
| **ESP Code amendment chain after A.1049(27)** | **OPEN** (RQ-26) | Q2 uses the base Code, which carries the definition, and states the limitation |
| **IMO gender instruments** | **NOT HELD.** No gender, Women in Maritime or SDG material in the corpus | Q3's IMO limb is authoritative secondary. **No resolution number is asserted** for the gender programme |
| **Biofouling Guidelines** | **NOT HELD** | Q8 cites them by identity and effect only |
| **OCIMF / industry vetting** | Concept level, citation/index only | Not required by this paper |
| **Marine Insurance Act, 1963 full text** | **NOT HELD.** Corpus carries a note limited to three sections | Q5 cites only what that note supports; no further section number is asserted |

---

## 6. POSITIVE CONTROLS FOR THE CONTAMINATION SWEEP

A zero-result sweep is a claim that must itself be controlled
(`DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §8). The sweep run on this paper is seeded with
known positives before it is trusted:

| Seeded token | Must fire because | Result |
|---|---|---|
| `Net-Zero Framework` | approved April 2025, one month **after** the sitting | fires |
| `Merchant Shipping Act, 2025` | assent August 2025 | fires |
| `A.1206(34)` | 34th Assembly, December 2025 | fires |
| `MSC.560(108)` in force | 1 January 2026 | fires |
| `MEPC.385(81)` in force | 1 August 2025 | fires |

Only after all five fire is a zero result on the real text read as "clean".

---

## 7. WHAT THIS PAPER MUST NOT SAY

- That the IMO Net-Zero Framework exists, is approved, or is proposed in any operative
  sense. It is one month beyond the sitting.
- That the Merchant Shipping Act, 2025 governs, or that the 1958 Act is repealed.
- That the HNS Convention is in force, or how many States have ratified it.
- That EEDI Phase 2 is the **present** phase — while equally not correcting the printed
  stem away.
- That any `A.1xxx(34)` resolution is operative.
- That the 2025 MLC amendments apply.
- That the UK Marine Insurance Act 1906 governs an Indian policy.
- That a classification-society requirement is a SOLAS requirement.
