# QP2401 — TEMPORAL AND DONOR ANCHOR

**Paper:** QP2401, **January 2024**, MEO Class I, Engineering Management
**Printed serial:** `EM – 24117-1` · 2 pages · 9 questions · 16 marks each
**Branch:** `pastpapers/qp2401-founder-review`, from baseline `9c973596edb04db32c7bf4feb3cb5898b162662a`
**Corpus consumed (read-only):** `RulesApp-Local-Input` `main` = `319524c24d11b2f89f33672c384b56e9ae1ab7db`
**Built:** 2026-08-12, before any answer was authored

Governed by `TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md` and
`DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §8. This file is the sitting anchor: it is built **before**
the answers and every answer is written against it.

---

## 0. THE CORPUS COMMIT ACTUALLY USED — a deliberate departure from the recorded baseline

`DESKTOP_QP_PRODUCTION_PLAYBOOK.md` §16 records the required corpus commit as
`64977b86ed9c601e273f1d0cb55abb0461835811`. The corpus checkout on this machine has legitimately
advanced past that pin to `319524c`, and the session instruction directs that it **not** be reset
backwards. It was verified `main == origin/main`, tracked tree clean, and treated as **read-only**
throughout. No corpus file was written, moved or corrected by this session.

The consequence for this paper is nil. Every corpus object consumed here — the CII guideline
resolutions, the 2021 revised MARPOL Annex VI, the RO Code and the four 33rd-Assembly resolutions —
is identical in both states. Nothing QP2401 depends on moved between `64977b8` and `319524c`.

The known FSS consumer-adapter count mismatch that arises from the newer corpus state is **not a
QP2401 input** and was not touched. See §7.

---

## 1. THE SITTING DATE AND WHAT IT DECIDES

**January 2024.** Three boundaries govern this paper, and each one has a question sitting on it.

### 1.1 The 33rd IMO Assembly — adopted 6 December 2023

The 33rd Assembly adopted its resolutions on **6 December 2023**, one month before this sitting.
The `A.11xx(33)` editions are therefore the operative Assembly instruments for QP2401. An Assembly
boundary is the **adoption date**, not the meeting month.

Four of them are held in the corpus and three are load-bearing here:

| Resolution | Title | Revokes | Used by |
|---|---|---|---|
| `A.1185(33)` | Procedures for Port State Control, 2023 | `A.1155(32)` | Q9 (port State limb) |
| `A.1186(33)` | Survey Guidelines under the HSSC, 2023 | `A.1156(32)` | **Q4** |
| `A.1187(33)` | 2023 Non-exhaustive list of obligations relevant to the III Code | `A.1157(32)` | **Q9** |
| `A.1184(33)` | Guidelines on places of refuge | — | not used |

`A.1186(33)` carries its own currency statement in the annex header: the Guidelines *take into
account relevant IMO mandatory instruments and amendments thereto entering into force before or on
**31 December 2023***. That is a near-exact fit to this sitting and is quoted in Q4.

**The 34th Assembly (adopted 3 December 2025) is after this sitting and must not appear anywhere in
this paper.** No `A.12xx(34)` instrument is cited in any QP2401 answer.

### 1.2 The FAL single-window boundary — 1 January 2024

Resolution **`FAL.14(46)`**, adopted 13 May 2022, **entered into force on 1 January 2024** — days
before this sitting. It is the amendment that makes maritime single window systems **mandatory**.

This is the single most valuable temporal fact on the paper and Q2 is built on it. A candidate
sitting in January 2024 is sitting in the first month of the mandatory single window.

The **next** FAL amendment, `FAL.15(47)`, was adopted 17 March 2023 but **entered into force on
1 January 2025** — *after* this sitting. At January 2024 it was **adopted but not in force**. Q2
states that distinction explicitly rather than eliding it.

### 1.3 The Indian statute boundary

The **Merchant Shipping Act 1958** governs throughout. The **Merchant Shipping Act 2025** commenced
**15 March 2026** and does not exist for this paper. The corpus holds `MS_Act_2025_A2025-24.pdf`;
it was deliberately **not** consulted for any answer.

For Q1 the operative statute is the **Marine Insurance Act, 1963**, not the UK Marine Insurance Act
1906 and not the UK Insurance Act 2015.

---

## 2. THE SYSTEMIC RISK — every donor is pulled BACKWARDS

Every donor available to QP2401 is a **later** answer. The direction of correction is therefore
always subtractive: *what did the donor's author add because their sitting was later than mine?*

| Target | Donor | Donor sitting | Gap | Direction |
|---|---|---|---|---|
| `QP2401-Q1` | `QP2607-Q9` | July 2026 | 30 months later | strip forward |
| `QP2401-Q5` | `QP2607-Q3` | July 2026 | 30 months later | strip forward |
| `QP2401-Q9` | `QP2403-Q7` | March 2024 | **2 months later** | near-neutral |

---

## 3. DONOR ADJUDICATION — three deltas each, computed not inherited

### 3.1 `QP2401-Q1` ← `QP2607-Q9` — Uberrimae Fidei

Both printed stems were read. **EXACT.**

| Delta | Finding |
|---|---|
| **Question delta** | **NIL.** Character-identical, including the four internal questions and the `(16)`. |
| **Marks delta** | **NIL.** 16 marks, unlimbed, at both sittings. |
| **Temporal delta** | **NIL on the operative law.** The Marine Insurance Act, 1963 sections 19, 20, 21 and 22 are unamended between January 2024 and July 2026. The donor's UK Insurance Act 2015 material is already confined to the study notes as *contrast* and is expressly not applied to Indian law, so it needs no reversal — it was never applied forward. |

**Carried:** the statutory spine and the four `s.20(3)` exceptions.
**Re-authored:** the route, all study-guide prose, all cards. The donor object was **not** copied.
**Removed:** the donor's cross-link to `QB9_E.html` and its `unresolved` entry about `QB9_C.html`
link hygiene — both are internal-corpus housekeeping specific to the QP2607 build, not facts about
January 2024.

### 3.2 `QP2401-Q5` ← `QP2607-Q3` — IACS structure and the RO Code

Both printed stems were read. **EXACT** (the donor stores the limb break as a newline where QP2401
stores a space; no word differs).

| Delta | Finding |
|---|---|
| **Question delta** | **NIL.** |
| **Marks delta** | **NIL.** 8 + 8 at both sittings. |
| **Temporal delta** | **NIL on the RO Code. REAL on the IACS panel structure.** |

The RO Code limb is stable: adopted by `MSC.349(92)` (21 June 2013) and `MEPC.237(65)`, mandatory
from **1 January 2015** under `MSC.350(92)`, `MSC.356(92)` and `MEPC.238(65)`. Unchanged at both
sittings. Verified against the corpus copy of the Code rather than inherited.

The IACS limb needed correction. The donor lists a **seven-panel** structure including the **Safe
Decarbonisation Panel** and the **Safe Digital Transformation Panel**. The SDTP was constituted in
**January 2024** — *at* this sitting, not before it. An answer written for July 2026 can present
seven settled panels; an answer written for January 2024 cannot present the newest of them as
established practice. **QP2401-Q5 therefore describes the standing structure — Council, GPG,
technical Panels and Expert Groups, Permanent Secretariat, Quality Committee — and does not recite
a fixed panel count.** This is a genuine backward correction and is the reason Q5 is not a copy.

The donor's other discipline is **kept**: no IACS membership count is stated at either sitting.
A count is volatile and gains no mark.

### 3.3 `QP2401-Q9` ← `QP2403-Q7` — III Code

Both printed stems were read. **EXACT**, including the mark split.

| Delta | Finding |
|---|---|
| **Question delta** | **NIL.** Word-for-word identical, including the printed `Which all IMO instruments covered in the code`. |
| **Marks delta** | **NIL.** `6 + 4 + 6` at both sittings. |
| **Temporal delta** | **NIL.** `A.1070(28)` (4 December 2013) is unamended at both dates. `A.1187(33)` (6 December 2023) is the current obligations list at both dates. |

**The alternate donor `QP2510-Q7` is NEAR, not EXACT, and was not used.** October 2025 prints the
same words at **`6 + 5 + 5`**. A different mark split is a different expected depth, and it is a
later sitting on top of that. Recorded and rejected.

`QP2403-Q7` is the strongest donor on the paper: same examination year, two months later, identical
marks, and a companion instrument that had already settled before both sittings. The **one**
re-anchor required is the donor's sentence that `A.1187(33)` was adopted *"three months before this
sitting"*. For January 2024 it is **one month** before the sitting. That sentence was re-derived,
not copied — and it is a sharper point at this sitting than at the donor's.

The intake spec froze `QP2401-Q9` at **tier C**, *"no family member with a built answer"*. That is
**stale**: `QP2403` was solved after the intake was written. The derived tier is **D** and the
recurrence-and-reuse map already records it as `C → **D**` with donors `QP2403-Q7, QP2510-Q7`. The
derived tier governs. This is the standing rule against trusting a frozen `reuse_tier` doing exactly
what it exists to do.

---

## 4. PER-QUESTION SITTING POSITION

### Q1 — Uberrimae Fidei · **STABLE / LOW**
Marine Insurance Act, 1963 unamended in ss.19–22. No date in the answer falls near the sitting.
Jurisdiction risk is HIGH and is a *jurisdiction* risk, not a temporal one.

### Q2 — FAL Convention · **CONFIRMED / HIGH → resolved**
Intake recorded no flag. **The intake was wrong.** This is the most date-sensitive question on the
paper and the sitting falls inside the first month of a new mandatory regime.

- FAL 1965 adopted **9 April 1965**, in force **5 March 1967**.
- `FAL.14(46)` adopted **13 May 2022**, **in force 1 January 2024** — mandatory single window;
  COVID-19/PHEIC provisions; the anti-corruption approach to the ship–shore interface.
- `FAL.15(47)` adopted **17 March 2023**, **in force 1 January 2025** — **NOT in force at this
  sitting**. Recommended Practice 7.11, illicit activities in national facilitation programmes.
- The 2016 amendments (in force **1 January 2018**) made electronic exchange of information
  mandatory from **9 April 2019**; that is the predecessor step the 2022 amendments build on.

An answer that says "the single window will become mandatory" is wrong at this sitting. So is one
that presents `FAL.15(47)` as operative.

### Q3 — CII / AER / EEOI · **CONFIRMED / MEDIUM**
Intake flagged `IMO INSTRUMENT IN FLUX`. The flag is **real** and resolves to a precise position.

| Fact at January 2024 | Source |
|---|---|
| CII is regulation **28** of MARPOL Annex VI, as revised by `MEPC.328(76)`, in force **1 November 2022** | corpus |
| First calculation year is **2023**; the first attained CII is reported **within three months after the end of 2023** — i.e. by **31 March 2024** | reg 28.1, 28.2 |
| **No ship had yet been assigned a CII rating at this sitting.** 2023 is the first data year and ratings follow verification | reg 28.6 |
| Reduction factor **Z** relative to the 2019 reference line: **2023 = 5%, 2024 = 7%, 2025 = 9%, 2026 = 11%** | `MEPC.338(76)` table 1 |
| **Z for 2027–2030 was not yet set** — "to be further strengthened and developed" | `MEPC.338(76)` note ** |
| Guidelines in force: **G1** `MEPC.352(78)`, **G2** `MEPC.353(78)`, **G3** `MEPC.338(76)`, **G4** `MEPC.354(78)`, **G5** `MEPC.355(78)` | corpus |
| The mandatory review of the measure must complete **by 1 January 2026** | reg 28.11 |
| SEEMP **Part III** and the `MEPC.346(78)` SEEMP guidelines are operative | corpus |
| The **2023 IMO GHG Strategy**, `MEPC.377(80)`, adopted **7 July 2023**, is the standing strategy | — |

**Explicitly excluded as post-sitting:** `MEPC.384(81)` and `MEPC.385(81)` (MEPC 81, March 2024),
`MEPC.392(82)` and `MEPC.395(82)` (MEPC 82, October 2024). All are in the corpus and none is cited.
A donor written for any 2025 or 2026 sitting would carry the outcome of the reg 28.11 review; at
January 2024 that review had **not** reported.

### Q4 — Preventive maintenance, survey and the SMS · **CONFIRMED / LOW**
`A.1186(33)`, adopted 6 December 2023, is the operative HSSC Survey Guidelines edition and states
its own currency cut-off as 31 December 2023. It revoked `A.1156(32)`. The ISM Code element on
maintenance is stable. Nothing else on this question is date-sensitive.

### Q5 — IACS and the RO Code · **CONFIRMED / LOW after correction**
See §3.2. RO Code stable; IACS panel structure corrected backwards; no membership count stated.

### Q6 — Tribology · **CONFIRMED / MEDIUM**
"Latest developments" is inherently sitting-relative. The answer is anchored to what was current in
**January 2024** and, per `PASTPAPER_PRODUCTION_PROTOCOL.md` §2.1, declares engineering judgement
where no instrument prescribes the answer. The one hard regulatory anchor is the **0.50 % m/m global
sulphur limit in force since 1 January 2020** (MARPOL Annex VI reg 14) and its consequences for
cylinder lubrication. **No efficiency, saving or wear-rate percentage is quoted anywhere** — §2.1
forbids vendor-sourced precision.

### Q7 — Vetting inspections · **CONFIRMED / HIGH → resolved**
Intake flagged `GUIDELINE EDITION`. The flag is **real and the most easily failed on the paper**.

**At January 2024:**
- **VIQ7 was still the operative SIRE inspection tool.** SIRE 2.0 had **not** replaced it.
- SIRE 2.0 was in its **phase 3 unlimited beta / transition**, which commenced towards the end of
  Q4 2023 — the phase immediately before launch.
- **SIRE 2.0 launched, and VIQ7 was withdrawn, on 2 September 2024 — eight months AFTER this
  sitting.**

So SIRE 2.0 is correctly answered here as the **emerging** regime — which is precisely what limb (b)
asks for — and must **not** be written as the regime in force. Any donor written for a 2025 or 2026
sitting would say the opposite and would be wrong for January 2024. TMSA 3 is the operative TMSA
edition.

### Q8 — Fault Tree Analysis · **STABLE / LOW**
Method, not regulation. Dominant provenance is engineering judgement over standard reliability
practice, declared as such.

### Q9 — III Code · **CONFIRMED / LOW**
`A.1070(28)` unamended. `A.1187(33)` adopted 6 December 2023 — **one month** before this sitting —
is the current obligations list and had revoked `A.1157(32)`. Material citing the 2021 list is
superseded at this sitting.

---

## 5. THE THREE MANDATORY SWEEPS

Recorded here; results in the session report and in `verification/QP2401/`.

1. **Assembled-answer sweep** — every answer read end to end as a candidate would.
2. **Donor contamination sweep** — searched for any sentence true only of the donor's sitting:
   July-2026 currency in Q1/Q5, March-2024 currency in Q9.
3. **Future contamination sweep** — searched for anything in force only after January 2024:
   34th Assembly, MS Act 2025, MEPC 81/82, SIRE 2.0 as the operative regime, `FAL.15(47)` as in
   force, the reg 28.11 review outcome.

A zero-result sweep is controlled by seeding a known positive before the result is believed.

---

## 6. WHAT THIS PAPER DOES **NOT** DEPEND ON

Confirmed against the allocation: **no QP2401 question requires FSS Code or MARPOL Annex VI
provision *text***. Q3 needs regulation 28 and the CII guideline resolutions, which are held as
official source documents in the corpus and were read directly. Citation-level reference is
sufficient and available. The paper was not blocked on, and did not wait for, the MARPOL/FSS
text-layer derivative work.

## 7. NOT A QP2401 MATTER

The FSS consumer-adapter count mismatch (the pinned-corpus 60/58 question) is **out of scope for
this paper** and was not investigated, corrected or committed here. It is neither an input to nor an
output of QP2401.

---

## 8. STANDING TRAPS FOR THE REVIEWER TO CHECK

If exactly one thing is spot-checked in Founder review, check these five:

1. **Q2** — is the single window written as **already mandatory**, and is `FAL.15(47)` written as
   adopted-but-not-yet-in-force?
2. **Q7** — is VIQ7 the operative tool and SIRE 2.0 the emerging one, not the reverse?
3. **Q3** — is Z for 2024 given as **7 %**, and are the 2027–2030 factors left open?
4. **Q5** — is any IACS panel count or membership count asserted? It should not be.
5. **Q9** — is `A.1187(33)` described as **one** month before the sitting, not three?
