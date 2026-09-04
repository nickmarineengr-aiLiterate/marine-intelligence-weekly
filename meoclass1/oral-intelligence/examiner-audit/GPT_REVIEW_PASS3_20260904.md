# GPT REVIEW PASS 3 — AUTHORISATION RECORD

**Date:** 4 September 2026
**Origin:** `gpt_content_review`
**Baseline:** `c4420f8` (HEAD at the time this review opened; origin/main at `9e26f02`, 5 ahead)
**Scope:** bounded. Two shared-governance audits, one interruption-safety
implementation, and exactly two residual candidate-facing content items.
Everything else discovered in passing is REPORTED, not acted on.

---

## PART C — QB5_C_B#q5: IMO Casualty Investigation Code terminology

### What was reported

Pass 2B left two candidate-facing surfaces on this card that attribute the
expression **"formal investigation"** to the IMO Casualty Investigation Code:

1. 60-second answer: *"Once the vessel is secure, I transition to the formal
   investigation phase under the **IMO Casualty Investigation Code** and the
   ISM Code."*
2. Body heading: *"Formal Investigation & Evidence Preservation Procedure"*.

### The source, read directly

**Instrument:** IMO resolution **MSC.255(84)** — *Code of the International
Standards and Recommended Practices for a Safety Investigation into a Marine
Casualty or Marine Incident (Casualty Investigation Code)*, adopted
16 May 2008, in force 1 January 2010, mandatory through SOLAS XI-1/6
(inserted by MSC.257(84)); Part III amended by MSC.390(94).

**How read:** the structured extraction of the Code held in the
`casualty-investigation` package — `CASUALTY_DEFINITIONS.json`
(`verification_status: VERIFIED (all 22 captured from official IMO PDF)`,
each definition carrying its own page locator into the MSC.255(84) annex),
`CASUALTY_PROVISION_MATRIX.md` and `CASUALTY_INSTRUMENT_REGISTER.md`. The
package's definitions and provision matrix were both read, not the index rows
alone.

**The operative term (CIC 2.11, Annex Part I ch.2 p.8), verbatim:**

> *marine safety investigation* — "an investigation or inquiry (however
> referred to by a State), into a marine casualty or marine incident,
> conducted with the objective of preventing marine casualties and marine
> incidents in the future; includes collection and analysis of evidence,
> identification of causal factors and making of safety recommendations as
> necessary"

**Who conducts it (CIC 2.13):** a *marine safety investigation Authority* —
"an Authority in a State, responsible for conducting investigations in
accordance with this Code". **Not** a ship's officer.

**The negative:** the expression **"formal investigation" occurs ZERO times**
anywhere in the held casualty-investigation package — definitions,
provision matrix, instrument register and relationship objects — while
"marine safety investigation" occurs 106 times. The Code's own 2.11 wording
"however referred to by a State" is a permission for a STATE to name its
procedure differently; it is not licence to attribute a different name to the
Code.

### Two findings, not one

The stale term is the reported defect. Reading the source surfaced a second,
larger one on the same sentence: **a Chief Engineer does not conduct a marine
safety investigation at all.** Under the Code that is the flag State's
Authority's function (CIC 2.13, 6.1, 6.2). What the CE actually does is
preserve evidence for that investigation and run the **company's** internal
investigation under **ISM Code §9**. The corrected wording therefore fixes
the attribution as well as the term, because a narrow term-swap
("marine safety investigation phase, which I conduct") would have left a
worse claim standing than the one it replaced.

### Authorised edits — exactly two sites

| # | Surface | From | To |
|---|---|---|---|
| 1 | 60-second | "I transition to the formal investigation phase under the **IMO Casualty Investigation Code** and the ISM Code" | "I move to evidence preservation for the flag State's **marine safety investigation** under the IMO Casualty Investigation Code — that investigation is the flag State's Authority's, not mine — and to the company's own investigation under **ISM Code §9**" |
| 2 | Body `<h5>` | "Formal Investigation &amp; Evidence Preservation Procedure" | "Evidence Preservation &amp; Company Investigation Procedure" |

### Surfaces checked and NOT changed on this card

* **15-second block** — present but **empty** on this card. Reported below; not
  filled, because the review bars adding 15/60 layers.
* **Numbers / Regs** — "IMO Resolution MSC.255(84): Casualty Investigation Code
  (Mandatory standard for marine safety investigations)" — already correct.
* **Numbers / Regs, MS Act bullet** — already corrected by
  `CORR-MSACT2B-CASUALTY-20260904`; ends "The 2025 Act does not use 'formal
  investigation' for this machinery". Correct, untouched.
* **REG-BOX** — carries no casualty-code terminology. (Its `ISM Code Section 5`
  row is reported below as an out-of-scope finding.)
* **CE Oral Tip, Trap Warning, Examiner Chain, Casualty Link, On My Vessel** —
  no occurrence of the stale term.
* **Deep dives / cheat sheets** — this card has no separate deep-dive block, and
  no cheat sheet or `current-answers` file carries the phrase.

### Corpus-wide propagation sweep, and its dispositions

`grep -rn "[Ff]ormal [Ii]nvestigation" meoclass1/` returns matches in seven
further files. Every one is dispositioned rather than assumed:

| Site | Disposition |
|---|---|
| `QB9_H.html` q1/q4/q11, `QB9_H_CheatSheet.html` | Already correct — they teach *marine safety investigation* and state expressly that the 2025 Act does not use "formal investigation". No action. |
| `pastpapers/QP2304, QP2307, QP2503, QP2507, QP2512` | **Sitting-anchored answers to MS Act 1958-era questions.** Historically correct; a present-day term cannot be written into a past paper. Explicitly barred by the review's scope. No action. |
| `oralnotes/miw-notes-mgmt-p15.html` §"Preliminary Inquiry vs. Formal Investigation" | Heading reads *(Historical MS Act, 1958 Structure)*. Explicitly historical and correctly framed. No action. |
| `oralnotes/simon-notes-p6.html` s.359/s.360 list | Introduced as *"1958 numbering, for legacy reference; the current Act is the MS Act 2025"*, and its reg-box states the 2025 Act does not use the term. No action. |
| `QB4_B.html` MV El Faro (2015) | Describes the **US** casualty investigation, not the IMO Code, and attributes nothing to MSC.255(84). Out of this defect's family. **Reported, not changed.** |

So the propagation surface of *this* defect is exactly the two sites listed
above, both on QB5_C_B#q5.

---

## PART D — QB5_B#q1 and QB5_B_CheatSheet: ISM §5 / incoming CE

### What Pass 2B established, and what it deferred

`CORR-MSACT2B-CEHANDOVER-20260904` removed the non-existent MS Act handover
hook and recorded, under `authority.ism_position`, that ISM §5 is the
**Master's** Responsibility and Authority and that **no ISM clause prescribes
a CE takeover certificate**. It then listed the QB5_B#q1 ISM §5 reg-box row
under `deliberately_unchanged`, on the reading that the row "draws an analogy
rather than asserting a CE obligation, so it states nothing false", and
flagged it for review. This record is that review.

### The source, read directly

**Instrument:** ISM Code — resolution **A.741(18)** (adopted 4 November 1993),
as amended. Held at
`F:/RulesApp-Local-Input/true-source/03-imo-instruments/ISM-Code/_base-and-amendments/`,
`SRC-ISMCODE-CONSOLIDATED`. Base text sha256
`4aa9ebfe484f579c05d5cc58ea09bbc15d03f6d6a6a48736fb744854db1c3e9c`.

**How read:** the base resolution's text layer was extracted and read, and then
**every held amendment resolution was re-scanned for sections 5, 6 and 7** —
the registry's own currentness note records that its earlier scan was scoped to
sections 9 and 10 only, so that row could not be relied on for this question.

Amendment findings for §§5–7:

* **MSC.273(85)** item 3 — adds the word *"periodically"* at the beginning of
  **5.1.5**. Section 5 otherwise stands as adopted.
* **MSC.273(85)** item 4 — **replaces the whole of section 7**. Current §7 is
  titled **"SHIPBOARD OPERATIONS"** and reads: *"The Company should establish
  procedures, plans and instructions, including checklists as appropriate, for
  key shipboard operations concerning the safety of the personnel, ship and
  protection of the environment. The various tasks should be defined and
  assigned to qualified personnel."*
* **MSC.353(92)** — replaces **6.2** (manning). **6.3 is unamended.**
* **MSC.104(73)**, **MSC.179(79)**, **MSC.195(80)** — no amendment to §§5–7.

**§5 as it stands — "MASTER'S RESPONSIBILITY AND AUTHORITY":** 5.1 the Company
defines and documents **the master's** responsibility, in five limbs, of which
5.1.5 is "*periodically* reviewing the SMS and reporting its deficiencies to
the shore based management"; 5.2 the master's overriding authority. **The
section does not mention the chief engineer, a handover, or a takeover.**

**§6.3, verbatim and unamended:** "The Company should establish procedures to
ensure that new personnel and personnel transferred to new assignments related
to safety and protection of the environment are given proper familiarization
with their duties. Instructions which are essential to be provided prior to
sailing should be identified, documented and given."

### Every remaining ISM §5 reference in the two files, classified

| # | File | Text | Class | Action |
|---|---|---|---|---|
| 1 | `QB5_B.html` #q1 REG-BOX | `ISM Code §5` / "Master's Responsibility and Authority — **CE assuming CE role must review and understand the vessel's SMS immediately**" | **A** | Corrected |
| 2 | `QB5_B_CheatSheet.html` "Pre-arrival" row | Regulatory Hook `ISM Code §5 / SOLAS V/14` for "Review vessel history, outstanding defect list, SMS documents, previous PSC reports, class certificates validity" | **A** | Corrected (the `§5` token only) |

**Why #1 is A and not B.** Pass 2B read it as an analogy. It is not. The row
sits in a box headed *Regulatory References*: the `reg-code` cell names the
clause and the `reg-desc` cell states a **CE duty in the imperative** ("must
review and understand the vessel's SMS immediately"). That duty is 5.1.5 —
the **Master's** SMS-review limb — transposed onto the Chief Engineer. In that
position the pairing does not draw an analogy; it asserts §5 as the regulatory
basis for a CE obligation. It is also **contradicted by the card's own body**,
which says "The ISM Code does not specify a detailed handover procedure, but
ISM Sec. 3, Sec. 6 and Sec. 9 collectively require…" and whose *Numbers to
Memorise* names "ISM Sec. 3, 6, 9, 10" — §5 appears nowhere else in the card.
Under either classification the review directs the same edit, so the
disagreement changes the record, not the outcome.

No occurrence in either file was classified **B** (acceptable analogy) or **C**
(unrelated Master-specific reference). The other `§5` strings in the cheat
sheet are **STCW Reg. VIII/2 §5** (the 0.05 % BAC limit) — a different
instrument entirely, correct, untouched.

### Authorised edits

| # | Surface | From | To |
|---|---|---|---|
| 1 | QB5_B#q1 REG-BOX | `ISM Code §5` — "Master's Responsibility and Authority — CE assuming CE role must review and understand the vessel's SMS immediately" | `ISM Code §6.3` — "Familiarisation on a new assignment — the Company establishes procedures so that personnel transferred to new assignments related to safety and protection of the environment are given proper familiarisation with their duties. That, with §7 (procedures, plans and instructions for key shipboard operations) and the Company's own SMS handover procedure, is what governs a CE takeover. **No ISM clause prescribes a CE takeover certificate**, and §5 is the *Master's* Responsibility and Authority, not the Chief Engineer's." |
| 2 | Cheat sheet "Pre-arrival" hook | `ISM Code §5 / SOLAS V/14` | `Company SMS handover procedure; ISM Code §6.3 (familiarisation on a new assignment) / SOLAS V/14` |

### The boundary this record does NOT cross

The replacement says the Company's procedures **exist** and that
familiarisation is what §6.3 requires. It does **not** say that §6.3 or §7
mandates a CE takeover certificate — that claim would be as false as the one
being removed, and Pass 2B's `ism_position` already records the whole-document
negative behind it (`handover` 0, `takeover` 0, `taking over` 0, `chief
engineer` 0 in the ISM Code; the single "take over" is inside the 1.1.2
definition of *Company*). The governing principle written into both surfaces
is: **Company SMS / handover procedure, supported by ISM familiarisation and
documented operating procedures.**

---

## NEWLY DISCOVERED — REPORTED ONLY, NO ACTION TAKEN

1. **`QB5_C_B.html#q5` has an EMPTY 15-second block.** The `practice-block`
   div carries its `15-Second Answer` label and no content. Candidate-facing
   and visible. Not filled: the review bars adding 15/60 layers.
2. **`QB5_C_B.html#q5` REG-BOX carries a bare `ISM Code Section 5` row** with
   no description, on a casualty-investigation card. Same misattribution
   family as Part D but a different file and outside Part D's stated scope.
3. **`QB5_C_B.html#q5` truncates the Code's own title** — "…for a Safety
   Investigation into a Marine Casualty", omitting "or Marine Incident".
4. **`QB5_B_CheatSheet.html` "Pre-arrival" row still cites SOLAS V/14** for
   reviewing defect lists, PSC reports and certificate validity. V/14 is safe
   manning; it does not support that action cell.
5. **`QB4_B.html` MV El Faro paragraph** says "the formal investigation" of a
   US casualty. Not attributed to the IMO Code, so out of this defect family,
   but worth a currency read.
6. **Two Pass-1/Pass-2B correction validators are not registered as release
   gates.** `validate_correction_gptpass1.py` and
   `validate_correction_msact2b.py` exist and pass, but neither appears in
   `tools/oral/oral_release_gates.py`, so `run_oral_release.py` never runs
   them. The two gates this record ships have the same status and are declared
   here rather than registered, to keep the Pass-2B precedent visible instead
   of silently diverging from it. **This should be closed before publication.**
7. **The interruption-safety defect fixed in `mutate_corrections.py` is a
   defect CLASS.** Thirteen further mutation suites carry their own
   copy-pasted `Snapshot` class with the same `except Exception` shape, and
   none has a journal. Named in the Pass 3 report; not changed, because the
   review scopes Part B to `mutate_corrections.py`.
