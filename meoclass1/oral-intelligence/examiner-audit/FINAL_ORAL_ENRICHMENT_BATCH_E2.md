# Final Oral Enrichment — Batch E2 (Class, Survey, Structure and Statutory Certification)

Ten authorised existing-answer enrichment edits. **No canonical card was created,
removed, re-anchored or re-homed.** Corpus stays at **721** questions / 86 files.

Baseline commit `3696019`. Consolidation `eb586ed`
(`research/oral-final-enrichment-consolidation`).

---

## 1. The action set — both representations agree

The session brief named E2 as `ENRICH-A011`–`A020`. The consolidation agrees on
**both** of its independent representations: the `batches[]` entry for `E2`
lists exactly those ten ids, and the `batch` field on each production action
assigns exactly those ten to E2. Count 10, no reconciliation needed.

Checking both rather than one remains the point — `batches[].action_ids` is a
denormalised roll-up and `production_actions[].batch` is the per-record truth.
That cross-check is now a validator check in its own right
(`batch_membership_representations_agree`), so a future brief cannot quietly
disagree with the data the way E4's did.

## 2. Action matrix

| Action | Band | Verify class | Target | Family | Status |
|---|---|---|---|---|---|
| ENRICH-A011 | **E-P1** | CLASS_RULE | `QB1_F.html#q7` | GAP-0004 | IMPLEMENTED |
| ENRICH-A012 | E-P2 | CURRENT_REG | `QB1_E.html#q1` | GAP-0672 | IMPLEMENTED |
| ENRICH-A013 | E-P2 | CLASS_RULE | `QB1_F.html#q8` | GAP-0075 | REDUCED SCOPE |
| ENRICH-A014 | E-P2 | PRIMARY_AUTHORITY | `QB3_A.html#q6` | GAP-0574 | REDUCED SCOPE |
| ENRICH-A015 | E-P2 | PRIMARY_AUTHORITY | `QB1_B.html#q7` | GAP-0668 | IMPLEMENTED |
| ENRICH-A016 | E-P2 | MIW_CORPUS_SUFFICIENT | `QB1_H.html#q5` | GAP-0108 | IMPLEMENTED |
| ENRICH-A017 | E-P2 | PRIMARY_AUTHORITY | `QB2_A.html#q15` | GAP-0384 | REDUCED SCOPE |
| ENRICH-A018 | E-P2 | PRIMARY_AUTHORITY | `QB3_H.html#q6` | GAP-0690 | IMPLEMENTED |
| ENRICH-A019 | **E-P1** | PRIMARY_AUTHORITY | `QB3_A.html#q8` | GAP-0490 | IMPLEMENTED |
| ENRICH-A020 | E-P3 | TECHNICAL_REASONING | `QB1_supplementary.html#q3` | GAP-0646 | IMPLEMENTED |

`ENRICH-A012` is the batch's one retarget — the consolidation had already moved
it from `QB10_B#q1` (the 2024–2028 amendment overview, which owns no LSA repair
control) to the SEQ survey card. That retarget was verified against the live
card and adopted.

**Current-live recheck.** All ten cards were opened in full against the live
721-question corpus before any edit. Every target is still the correct home and
no limb had been absorbed by E3, E4, GAP-0609 or Batch D. **Zero actions were
held and zero were downgraded to already-covered** — but three were reduced in
scope on primary evidence (§3), which is a different thing and is recorded as
such.

**Follow-up overlap: two of ten.** `QB1_E#q1` (GAP-0172, GAP-0282) and
`QB3_H#q6` (GAP-0385) both appear in the consolidation's 9
`followup_colocation` records. In each case the follow-up ask is a *different*
limb from the authorised enrichment — FSS Code functional requirements and
statutory certificate validity on the first, IBC annual-versus-intermediate
survey scope on the second — so neither was implemented here. Both remain open
follow-up work and the count of 35 groups is unchanged.

## 3. The authorisation record was wrong four more times

E4 recorded that its consolidation entry attributed a carbon-factor difference
to "asphaltenes", which is chemically backwards. E3 met the same problem twice.
E2 met it four times. The pattern is now settled well enough to state as a rule:
**the consolidation authorises which limb to add; it does not establish what the
limb says, and it is not a reliable description of the card's current state
either.**

### A013 — vocabulary the governing guideline does not use

The consolidation named the deformation vocabulary as "buckling, **set-in/
dishing** of plating, **tripping** of stiffeners and **permanent set**".

Only buckling survives. Searched against IACS Recommendation No. 84, the
guideline that actually governs hull survey on this ship type:

| Term | Occurrences in IACS Rec. 84 |
|---|---|
| `tripping` | **0** |
| `set-in` | **0** |
| `dishing` | **0** |
| `permanent set` | **0** |
| `permanent buckling` | 1 |
| `elastic buckling` | 1 |

These are real shipyard words, but they are not the vocabulary of the class
guideline a surveyor applies, and publishing them to a candidate as though they
were class terminology would be teaching the wrong register for an oral. The
limb was implemented with the taxonomy IACS does use — **local against global
deformation**, **buckling** as defined, and **permanent against elastic**
buckling — and the four unverified terms were dropped rather than reproduced.

**A trap worth recording for the guard, not just the answer.** The obvious way
to protect this decision is a negative-token check on the four dropped terms.
Done naively it fails immediately: `tripping` occurs inside `s-tripping`, and
the baseline card legitimately says "Emptying, **stripping**, washing" in its
tank-cleaning bullet. The guard is therefore anchored `\btripping\b`. This is
the same substring-collision class that has bitten instrument-number matching in
this repo before, and the general lesson is that **a negative guard must be
tested against the baseline card, not only against the edited one** — otherwise
it fires on text nobody wrote today.

### A014 — a limb that was already three-quarters answered

The consolidation stated the regulatory citation "is the one part of this
four-part ask the card does not answer". That is not accurate about the live
card. `SOLAS Ch XI-1, Reg 2` and `IMO Res. A.1049(27)` already appear in the
reg-box, in the 60-second block and in the Numbers block.

What *is* genuinely absent is narrower and the family record's own `why` field
states it correctly: the answer body opens "a mandatory survey regime under
SOLAS" **without naming the chapter**, and the string `ESP Code` occurs **zero
times anywhere on the card** — the Code is never named as an instrument, only
its adopting resolution number appears. The action was implemented as that prose
completion. Reported as reduced scope rather than claimed as a missing citation,
because the difference matters to anyone reading this record later.

### A017 — two of three elements were already on the card

The consolidation asked for "the ship type assignment, the tank-by-tank record
of the containment and handling equipment fitted, and the carriage conditions
each listed cargo depends on". The live card already states the **Type 1/2/3
assignment** explicitly and already says the product list carries "specific
**tank-by-tank loading restrictions**".

The middle element is also not quite what the instrument does: the IBC model
form does not enumerate handling equipment tank by tank. It keys **conditions of
carriage** to tank numbers which are then resolved by **attachment 2, a signed
and dated tank plan**. The action was implemented as the genuinely absent part —
the model form's anatomy — rather than as a restatement of what the card had.

### A011 — a trigger the instrument does not carry

The consolidation listed "unreported casualty" among the triggers of class
suspension, alongside overdue survey and unrectified Condition of Class.

IACS **PR 1C** does not carry it. The instrument is expressly confined to
"Surveys or Conditions of Class Going Overdue" and lists no casualty-reporting
ground anywhere in Section A. The verified obligation is an insurance one:
**Institute Time Clauses – Hulls 1/11/95 clause 4.3** requires that "Any
incident condition or damage in respect of which the Vessel's Classification
Society might make recommendations as to repairs or other action ... must be
promptly reported to the Classification Society."

So the reporting duty is real and worth teaching, but it is not a PR 1C
suspension trigger. It was written as a reporting duty whose breach bites
through the insurance conditions, not as a third suspension ground.

## 4. Missing limbs, and what was added

### ENRICH-A011 — `QB1_F#q7` — the batch's highest-recurrence ask

*The current answer lacks the class-status ladder — suspension against
withdrawal, what triggers each, whether it is automatic, and the consequence
chain to statutory certificates, insurance cover and trading.*

Three examiners asked this, the highest recurrence in the enrichment set. The
card defined Conditions of Class and Memoranda but never mentioned suspension,
and mentioned withdrawal only in passing in CE-relevance prose.

Added, from **IACS PR 1C Rev.7 (Nov 2024, applying from 1 January 2026)**:

- **Automatic suspension** — from the certificate expiry date if the Special
  (Renewal) Survey is not completed by its due date (A.1.1); and the Class
  Certificate becomes invalid with class automatically suspended if the
  **Annual** (A.1.2) or **Intermediate** (A.1.3) survey is not completed within
  **3 months** of its due date, unless the ship is under attendance.
- **Suspension by procedure** — an overdue **Condition of Class** makes class
  *subject to a suspension procedure* (A.2.1), which is deliberately not the
  same thing. This is the distinction the limb asked for and it is the one a
  candidate most often flattens.
- **Withdrawal** — after **6 months** suspended for overdue surveys and/or
  Conditions of Class, class **is to be withdrawn** (A.4.1); longer suspension
  only where the ship is not trading.
- **Reinstatement** — credited from the date originally due, but the ship is
  **disclassed for the whole period from suspension to reinstatement**;
  "Disclassed" is PR 1C's defined term covering both states.
- **Consequence chain** — **B.1.3** requires the Society's letters to Owner and
  Flag State to state that *certain statutory certificates are implicitly
  invalidated*. On insurance, **ITC-Hulls cl. 4.1.1/4.1.2** impose the duty to
  keep class maintained and comply by the Society's dates, and **cl. 5.1**
  terminates the insurance **automatically** on change, suspension,
  discontinuance, withdrawal or expiry of class — deferred until the next port
  if the ship is at sea. Trading follows both.

### ENRICH-A012 — `QB1_E#q1`

*The current answer lacks the pre-release control on sending an LSA item ashore
— who may lawfully do the work, what that authorisation rests on, and what
evidence returns with the item.*

The card covered launching-appliance and release-gear preparation but the tokens
`402(96)`, `service provider` and `authoris/authoriz` each occurred **zero**
times.

Added, from **Resolution MSC.402(96)** (adopted 19 May 2016, effective
**1 January 2020** with the SOLAS III/3 and III/20 amendments in MSC.404(96)):

- **2.2.6** — "Repair" means any activity requiring **disassembly**, or outside
  the on-board maintenance and emergency-repair instructions. Sending a davit to
  a shore workshop is therefore repair, not maintenance, and that classification
  is what pulls in everything else.
- **4.3** — repair, any overhaul and the five-yearly thorough examination must be
  done by certified personnel of **the manufacturer or a service provider
  authorised by the Administration** (**2.2.1**, **3.1**); **7.2** — the
  Administration makes that list available.
- **7.1** — the authorisation rests on personnel certified for that make and
  type, the manufacturer's specialised tools, parts access, the manufacturer's
  instructions for disassembly of on-load release gear and davit winches, and a
  documented certified quality system.
- **5.1 / 5.2** — reports and checklists **signed by the person who did the work
  and countersigned by the Company's representative or the Master**, and records
  **filed on board for the service life of the equipment** — which is exactly
  what the SEQ surveyor asks to see.

### ENRICH-A013 — `QB1_F#q8`

*The current answer lacks the deformation vocabulary a surveyor actually uses,
how it is assessed, and what makes a deformation a Condition of Class.*

Added, from **IACS Rec. No. 84 §3.3.4 and §3.4**: local against global
deformation; **buckling** defined as the case where a small increase in in-plane
load produces a large deformation; plate buckling between stiffeners where
compressive stress runs perpendicular to the stiffening, which on a container
ship means where deck longitudinals terminate forward and in the cross-deck
strips; **permanent** buckling from overloading, corrosion or contact against
**elastic** buckling which "will not normally be directly obvious but may be
detected by evidence of coating damage, stress lines or shedding of scale";
buckling in the webs of web frames and floors; and the contact-damage warning
that shell damage looking slight from outboard often conceals heavily damaged
internal members.

On assessment, the card now says what the guideline says and no more:
**§3.4.2** "Any damage to ships structures that is considered to affect the
ship's Classification is to be repaired"; **§3.4.4** crop and renew at
permissible minimum thickness, with **doubler plates not permitted to compensate
wasted plate**; **§3.4.5** renewal below the renewal thickness under the net
scantling approach (**UR S11A**, **UR S21A**).

**No universal percentage was stated, deliberately.** Rec. 84 carries no single
allowable-deformation figure, and the batch brief specifically forbids inventing
a 10% or 20% rule. The card now says so explicitly — that the extent is assessed
against the individual Society's acceptance criteria — and a validator qualifier
guards the denial so a later "helpful" simplification cannot quietly install a
number.

### ENRICH-A014 — `QB3_A#q6`

*The current answer lacks the chapter in the defining prose and the Code by
name.*

Added one paragraph inside the existing "What ESP Is" section, quoting
**SOLAS XI-1/2**: bulk carriers as defined in **IX/1.6** and oil tankers as
defined in **II-1/2.22** shall be subject to an enhanced programme of
inspections in accordance with the **International Code on the Enhanced
Programme of Inspections during Surveys of Bulk Carriers and Oil Tankers, 2011
(2011 ESP Code)**, adopted by **A.1049(27)**. Closed with the contrast that
cargo ships *not* subject to the ESP Code are handled under **XI-1/2-1**.

### ENRICH-A015 — `QB1_B#q7`

*The current answer lacks the boundary of RO authority — that classification
needs no delegation, while statutory certification runs only as far as a
particular flag has delegated it in writing.*

Added, from the **RO Code (MSC.349(92))**:

- **1.3** defines statutory certification and services as certificates issued on
  the authority of a sovereign State's laws — so classification, which is the
  society's own product, sits outside the delegated scope entirely.
- **8.1** — under SOLAS I/6 and XI-1/1, LL article 13, MARPOL Annex I reg 6 and
  Annex II reg 8, a flag State may authorise an RO **only for ships entitled to
  fly its flag**.
- **8.2 / 8.3** — the **formal written agreement** is the legal basis, and "the
  flag State shall specify the scope of authorization granted to an RO" across
  ship types and sizes, which conventions and national legislation apply,
  drawing and equipment approval, surveys, **issuance, endorsement and renewal
  of certificates**, corrective actions, reporting, and **withdrawal or
  cancellation of certificates**.
- **8.5** — flag standards may go beyond convention requirements.

So the answer to "what can this society alone do?" is *it depends on the flag*,
and the RO agreement is the document that settles it.

**Source note.** The consolidation warned the True Source RO Code holding is an
image-only scan. Confirmed the hard way: **both** local copies — the
`true-source` one and the `official-sources` one — extract to **61 bytes** of
text, i.e. no text layer at all. The primary fetch from the IMO CDN was
necessary, and it worked.

### ENRICH-A016 — `QB1_H#q5`

*The current answer lacks the objectives half of the ask — why GBS was needed at
all, and why Tier III audit replaces IMO rule-writing.*

The card explained the five tiers, the scope and the SCF precisely, and the ask
puts OBJECTIVES, WHY NEEDED in capitals. A one-line rationale did exist, but
only inside the deep-dive Casualty Link — which is not the answer the candidate
gives.

Added as a new leading section, from IMO's own account: from the 1990s the MSC
recognised that **prescriptive-based regulations were unable to cope with new
ship design challenges**; the shift is to a goal- and performance-oriented
approach *in lieu of* the prescriptive one; IMO sets and audits the goal while
classification societies acting as ROs develop the detailed rules; and **Tier III
is the mechanism** — class construction rules verified by **international GBS
Audit Teams established by IMO's Secretary-General** under the Revised
guidelines for verification of conformity (**MSC.454(100)**, a resolution the
card did not previously carry).

### ENRICH-A017 — `QB2_A#q15`

*The current answer lacks the anatomy of the certificate and its attachments.*

Added, from the **IBC Code model form of the International Certificate of
Fitness** (MSC.176(79)): the three-column entry — **Product / Conditions of
carriage (tank numbers etc.) / Pollution Category**; **attachment 1**, the
continuation sheets which must be **signed and dated**; **attachment 2**, the
**signed and dated tank plan** on which the tank numbers are identified;
**Note 4**'s requirement that Category Z substances not covered by the Code are
listed and identified as **"chapter 18 Category Z"**; **Note 2**'s rule that an
entry of "Type 2" means Type 2 in *all* respects the Code prescribes; and the
exemptions, modifications and loading requirements carried on the face of the
certificate.

### ENRICH-A018 — `QB3_H#q6`

*The current answer lacks the pointer to an actual document — the signed product
list attached to the Certificate of Fitness, read with the P&A Manual, and the
Annex I equivalent.*

Added: under **MARPOL Annex II regulation 7**, a chemical tanker certified under
the IBC Code holds an International Certificate of Fitness, and that certificate
"shall have the same force and receive the same recognition as the certificate
issued under regulation 9" — so the permitted products are the signed, dated
list attached to it. Read with **regulation 14**'s Administration-approved
**Procedures and Arrangements Manual** in the standard format of **appendix 4**,
whose stated purpose is to identify for the ship's officers the physical
arrangements and all operational procedures for cargo handling, tank cleaning,
slops handling and cargo tank ballasting and deballasting. The **Annex I
equivalent** is the **Supplement to the IOPP Certificate** — the Record of
Construction and Equipment, **Form A** for ships other than oil tankers and
**Form B** for oil tankers — permanently attached to the certificate.

### ENRICH-A019 — `QB3_A#q8` — the batch's second E-P1

*The current answer lacks the scope of SOLAS Chapter XII beyond regulation 11,
and the damage stability criteria the loadicator is checking against.*

Two limbs, two sections.

**The chapter, item by item** — all fourteen regulations with their titles, from
the SOLAS 2024 consolidated text: 1 Definitions, 2 Application, 3 Implementation
schedule, 4 Damage stability, 5 Structural strength, 6 Structural and other
requirements, 7 Survey and maintenance, 8 Information on compliance, 9 Ships not
capable of complying with 4.3, 10 Solid bulk cargo density declaration, 11
Loading instrument, 12 Water ingress alarms, 13 Availability of pumping systems,
14 Restrictions from sailing with any hold empty.

**The criteria**, from **regulation XII/4** verbatim: one-hold flooding at the
Summer Load Line for single-side skin ships **150 m and upwards** carrying cargo
of density **1,000 kg/m³ and above** built on or after **1 July 1999**, and for
double-side skin ships built on or after **1 July 2006** where any part of the
longitudinal bulkhead lies within **B/5 or 11.5 m, whichever is less**;
**foremost** hold only for pre-1999 single-side skin ships carrying **1,780
kg/m³ and above**, phased in under regulation 3; the equilibrium condition
itself referred out to the annex to **resolution A.320(IX)** as amended by
**A.514(13)**; and permeability fixed at **0.9** loaded / **0.95** empty.

The family record's `bloat_caution` excluded the ask's ballasting-versus-stress
limb because the card already covers bending moment and shear force. Honoured —
nothing was added on ballasting or hull girder stress.

### ENRICH-A020 — `QB1_supplementary#q3`

*The current answer lacks the reason the margin line sat 76 mm below the
bulkhead deck at side.*

This is the largest target in the set at ~11,500 characters, and the family
record's `bloat_caution` required one or two sentences **inside the existing
Margin Line section**, not a new section. Honoured — a single paragraph was added
in place.

The card already stated the position, the non-submergence rule and the 2009
deletion, so only the principle was added: the bulkhead deck is the deck to
which the transverse watertight bulkheads are carried, so it is the top of the
subdivision; immersion at side lets water run *over* the bulkhead tops
(progressive flooding) and puts the horizontal escape route awash; the **76 mm**
— three inches in the convention's original imperial terms — was a deliberate
**reserve** so margin remained after heel, trim and sinkage. Hence *margin* line,
not limit line.

Verified in passing that the string `margin line` occurs **zero times** in the
SOLAS 2024 consolidated text, which independently confirms the card's existing
claim that the concept was removed.

## 5. Authority — every action primary or class

| Action | Authority |
|---|---|
| A011 | **IACS PR 1C Rev.7** (Nov 2024, applies 1 Jan 2026) §§A.1.1–A.1.3, A.2.1, A.4.1, B.1.3, Definitions — verbatim from the IACS public store; **Institute Time Clauses – Hulls 1/11/95** cl. 4.1.1, 4.1.2, 4.3, 5.1 — verbatim |
| A012 | **IMO Res. MSC.402(96)** §§2.2.1, 2.2.6, 3.1, 4.3, 5.1, 5.2, 7.1, 7.2 — local True Source copy; **MSC.404(96)** / SOLAS III/3, III/20 |
| A013 | **IACS Rec. No. 84 Rev.1** (Nov 2017) §§3.3.4, 3.4.2, 3.4.4, 3.4.5 and section 5 deformation guidance — downloaded from the IACS public store |
| A014 | **SOLAS consolidated 2024, XI-1/2** verbatim (and XI-1/2-1); **A.1049(27)** held locally |
| A015 | **RO Code, Res. MSC.349(92)** §1.3 and Part 2 §§8.1, 8.2, 8.3, 8.5, 8.6.1 — fetched from the IMO CDN |
| A016 | IMO's Goal-Based Standards account; **MSC.287(87)**, **MSC.290(87)**, **MSC.454(100)** |
| A017 | **IBC Code (MSC.176(79))** model form of the ICOF, items 3–6 and Notes 2–4 — local True Source copy |
| A018 | **MARPOL Annex II regs 7 and 14** verbatim — local copy; IBC model form; **IOPP Supplement Forms A/B** |
| A019 | **SOLAS consolidated 2024** chapter XII contents and **regulation XII/4.1–4.4** verbatim |
| A020 | Technical reasoning only, as the family record specifies; SOLAS 2024 checked for the absence of `margin line` |

**Notes used: none.** No E2 family carried Notes support, and no claim was taken
from `oralnotes/`, from neighbouring MIW cards, or from a study website. Where a
claim could not be substantiated it was dropped (§3), not softened.

**On the class-source access gate.** Both `CLASS_RULE_VERIFY_REQUIRED` actions
were gated on reading real class text before editing, and both cleared it. Worth
recording how, because the obstacle was tooling rather than permission: the IACS
resolution pages return **HTTP 403** to a plain fetch, and the PDF bytes are not
parseable by the fetch tool. Driving the real browser and scanning the Vue app's
serialised state for the escaped `/` paths recovers the true S3 URL, and
`pdftotext -layout` turns it into quotable text. `PR 1C` and `Rec. 84` were both
obtained that way.

**One IACS identifier was nearly wrong and was caught by checking.** The obvious
candidate for class suspension is `PR 1A`. **PR 1A is the Procedure for Transfer
of Class.** The suspension/withdrawal instrument is **PR 1C**. This is exactly
the failure the brief warned about after the earlier UR S11-versus-S1 confusion,
and it is one search away from being published.

## 6. Scope of change

```
meoclass1/QB1_B.html             +11 -1
meoclass1/QB1_E.html             +12 -1
meoclass1/QB1_F.html             +27 -2
meoclass1/QB1_H.html             +10 -2
meoclass1/QB1_supplementary.html  +1
meoclass1/QB2_A.html             +13 -1
meoclass1/QB3_A.html             +13
meoclass1/QB3_H.html              +9 -1
```

**The deletions are a line-level artefact, not lost content.** Several reg-boxes
and answer bodies are a single very long line; appending to one shows as a line
removed and a line added. At character level every one of the ten edits is
**purely additive** — `SequenceMatcher` opcodes over each card give `insert`
only, with **zero delete and zero replace ops**:

| Action | insert | delete | replace | chars added |
|---|---|---|---|---|
| A011 | 2 | 0 | 0 | 3,633 |
| A012 | 2 | 0 | 0 | 2,437 |
| A013 | 2 | 0 | 0 | 3,146 |
| A014 | 2 | 0 | 0 | 1,067 |
| A015 | 2 | 0 | 0 | 2,446 |
| A016 | 2 | 0 | 0 | 1,692 |
| A017 | 2 | 0 | 0 | 2,141 |
| A018 | 1 | 0 | 0 | 1,842 |
| A019 | 2 | 0 | 0 | 3,057 |
| A020 | 1 | 0 | 0 | 868 |
| **total** | **18** | **0** | **0** | **22,329** |

**Timed-block delta: zero** — every 15-second and 60-second block is
byte-identical to baseline on all ten cards, and that is now a validator check
(`timed_blocks_unchanged`) with its own mutation, not merely an assertion.

**Zero new CSS classes, zero new inline styles, zero tables, zero images, zero
nested lists, zero fixed widths.** Tags used across all ten additions:
`div, em, h4, li, p, span, strong, ul`.

One responsive defect was found and fixed before commit: the A017 reg-box
initially contained the 37-character unbreakable token
`product/conditions/pollution-category`, which would have risked horizontal
overflow in a narrow reg-desc column. Reworded to
"the product, conditions and pollution category columns"; the card's digest was
re-derived and the edit re-proved insert-only.

## 7. Claim review

Every new numeric, instrument, section and date claim introduced by E2, and how
it was verified:

| Claim | Verified against |
|---|---|
| PR 1C = suspension/withdrawal; **PR 1A is transfer of class** | IACS resolution index + PR 1C title page |
| Rev.7 Nov 2024, **applies from 1 January 2026** | PR 1C Notes, item 8 |
| Special Survey → automatic suspension from expiry | PR 1C A.1.1 |
| Annual / Intermediate → automatic at **3 months** overdue | PR 1C A.1.2, A.1.3 |
| Overdue CoC → **suspension procedure**, not automatic | PR 1C A.2.1 |
| Withdrawal after **6 months** suspended | PR 1C A.4.1 |
| "Disclassed" = suspended or withdrawn | PR 1C Definitions |
| Statutory certificates **implicitly invalidated** | PR 1C B.1.3 |
| Duty to keep class maintained; comply by Society's dates | ITC-Hulls 1/11/95 cl. 4.1.1, 4.1.2 |
| Incident/damage **promptly reported** to the Society | ITC-Hulls cl. 4.3 |
| Cover **terminates automatically**, deferred to next port at sea | ITC-Hulls cl. 5.1 |
| MSC.402(96) effective **1 January 2020**; MSC.404(96) amends III/3, III/20 | MSC.402(96) preamble |
| "Repair" = requiring **disassembly** / outside on-board instructions | MSC.402(96) 2.2.6 |
| Repair, overhaul, 5-yearly by manufacturer **or authorised service provider** | MSC.402(96) 4.3, 2.2.1, 3.1 |
| Reports countersigned by Company rep **or Master** | MSC.402(96) 5.1 |
| Records kept on board for the **service life of the equipment** | MSC.402(96) 5.2 |
| Buckling = small in-plane load increase → large deformation | IACS Rec. 84 §3.3.4 |
| Elastic buckling detected by coating damage, stress lines, scale | IACS Rec. 84 §3.3.4 |
| Damage affecting classification **is to be repaired** | IACS Rec. 84 §3.4.2 |
| **Doubler plates must not** compensate wasted plate | IACS Rec. 84 §3.4.4 |
| Net scantling renewal thickness; **UR S11A / S21A** | IACS Rec. 84 §3.4.5 |
| **No** universal allowable-deformation percentage exists | absence across IACS Rec. 84 |
| SOLAS **XI-1/2**; IX/1.6; II-1/2.22; **2011 ESP Code**; A.1049(27); XI-1/2-1 | SOLAS 2024 verbatim |
| RO authority only for ships **entitled to fly that flag** | RO Code 8.1 |
| Flag State **shall specify the scope**, incl. withdrawal/cancellation | RO Code 8.3 |
| Statutory certification defined as State-authority certificates | RO Code 1.3 |
| Prescriptive rules "unable to cope with new ship design challenges" | IMO GBS account |
| Tier III audited by **GBS Audit Teams**, Secretary-General; **MSC.454(100)** | IMO GBS account |
| ICOF columns Product / Conditions of carriage / Pollution Category | IBC model form item 4 |
| **attachment 1** signed sheets; **attachment 2** signed dated tank plan | IBC model form item 4 |
| **chapter 18 Category Z** listing requirement | IBC model form Note 4 |
| "Type 2" means Type 2 **in all respects** | IBC model form Note 2 |
| Annex II reg 7 — CoF has **same force** as the reg 9 certificate | MARPOL Annex II reg 7 verbatim |
| Reg 14 P&A Manual, **appendix 4** standard format, stated purpose | MARPOL Annex II reg 14 verbatim |
| IOPP Supplement **Form A / Form B**, Record of Construction and Equipment | MARPOL Annex I appendix II |
| SOLAS XII = **fourteen** regulations, titles as listed | SOLAS 2024 chapter XII contents |
| 150 m; 1,000 kg/m³; 1 Jul 1999; 1 Jul 2006; **B/5 or 11.5 m** | SOLAS XII/4.1, 4.2 verbatim |
| 1,780 kg/m³ pre-1999 → **foremost** hold; reg 3 schedule | SOLAS XII/4.3 verbatim |
| Equilibrium per **A.320(IX)** as amended by **A.514(13)** | SOLAS XII/4.4 verbatim |
| Permeability **0.9** loaded / **0.95** empty | SOLAS XII/4.4 verbatim |
| Margin line 76 mm = three inches; deleted from SOLAS | arithmetic; zero hits in SOLAS 2024 |

Four claims from the authorisation record were **rejected** on verification
(§3): the unreported-casualty suspension trigger, three of the four deformation
terms plus "permanent set", the "one part not answered" reading of A014, and the
tank-by-tank equipment enumeration in A017. Nothing unverifiable was retained,
and no section number was guessed.

## 8. Verification

| Property | Result |
|---|---|
| Canonical total | **721 → 721** (equality vs baseline `3696019`) |
| Question-bearing files | 86, unchanged |
| Cards added / removed | **0 / 0** |
| Cards changed corpus-wide | **exactly 10, all authorised, 0 unauthorised** |
| Edits purely additive | **yes** — 18 insert opcodes, 0 delete, 0 replace |
| q-text / anchors | unchanged on every card, corpus-wide |
| DOM | balanced on all ten cards, ids unique, all under `#q-feed`, no nested lists |
| Candidate-visible hygiene | clean — no new leak on any touched card |
| `build_qb_content_index --check` | **CURRENT — no regeneration** (86 files / 721 questions) |
| `build_examiner_index --check` | **960 relationships / 7 examiners — zero delta**, 4/4 artefacts current |
| Public corpus count | **721**, unchanged. Pricing untouched. |
| Determinism | **26 artefacts / 0 non-reproducible** under `PYTHONHASHSEED` 0 / 1 / 524287, every artefact identical to disk — the deterministic *no-change* state |

### Gates — every required suite executed

`validate_batch_e2` **23/0** · `validate_batch_e3` 21/0 · `validate_batch_e4`
16/0 · `validate_batch_a` 11/0 · `validate_batch_b` 16/0 · `validate_batch_c`
16/0 · `validate_batch_d` 22/0 · `validate_gap0609_exception` 59/0 ·
`validate_qb_content_index` · `validate_examiner_index` · `validate_phase2` ·
`validate_ce_tip_review` · `validate_audit` (see below) ·
`test_qb_question_text` **7487 controls / 0 failures over 86 pages** ·
`test_oral_controls` 315/0 · `test_notes_controls` 106/0 ·
`test_examiner_check` all caught · Node `deploy_surface`, `regulatory_facts`,
`link_integrity` — all exit 0.

### Mutations — 183 across 12 suites, 0 escapes, 0 no-ops, 0 crashes

`mutate_batch_e2` **18** · `mutate_qb_content_index` 26 · `mutate_phase2` 33 ·
`mutate_ce_tip_review` 17 · `mutate_examiner_index` 13 · `mutate_batch_d` 12 ·
`mutate_batch_e4` 12 · `mutate_batch_b` 10 · `mutate_batch_c` 10 ·
`mutate_batch_a` 8 · `mutate_gap0609_exception` 8 · `mutate_batch_e3` 16.
All restored byte-exact; every harness ended with the tree byte-identical.

The E2 suite breaks each property in turn — omit an action, retarget an action,
touch a card no manifest owns, blank an added limb, inject an internal id, add a
q-card, misstate the canonical total, strip a required class authority, alter
q-text, claim a relationship delta, delete baseline text, revert an authorised
card, declare new-card creation — plus five E2 additions:

- **N** reintroduce an unsubstantiated deformation term → caught
  (`unsubstantiated_claims_absent`)
- **O** flatten the automatic-versus-procedure suspension distinction → caught
  (`required_qualifiers_kept`)
- **P** assert a universal allowable-deformation percentage → caught
  (`required_qualifiers_kept`)
- **Q** falsify a recorded digest → caught (`manifest_digests_match`)
- **R** edit a timed block on an authorised card → caught
  (`timed_blocks_unchanged`)

Mutation **C** deliberately targets `QB1_H#q1`, a card no manifest owns, and the
harness *asserts that fact at run time* before running rather than trusting it.
That is what makes the sibling-manifest delegation an exemption rather than a
hole.

### Audit validator — semantic result, not exit code

`validate_audit` reports `passed 12 / failed 1 / unavailable 0` while exiting
**0**. Run on a **clean `origin/main` worktree** the result is
`passed 12 / failed 1 / unavailable 0` — **identical**. Pre-existing, unrelated
to E2, and already carried as debt from E3 and E4. Reported here rather than
counted as green, because reading the exit code alone would call it a pass.

`qb_health_check`: **477 findings on both the branch and a clean `origin/main`
worktree**, compared as multisets rather than by order — **0 new, 0 gone**.

Gate-generated artefacts (`VALIDATION_RESULTS.json`,
`PHASE2_VALIDATION_RESULTS.json`, `ORAL_NOTES_IMPACT.md`) were dirtied by these
runs and **reverted after proof**.

### Render

**NOT BROWSER VERIFIED.** The preview pane serves files outside the project
folder as static snapshots that execute no JS and expose neither DOM nor page
text; `file:///` navigation on the repo returned a snapshot with no readable
content. No browser claim is made. Substituted: DOM parse and div balance, id
uniqueness, `#q-feed` parentage, CSS-class existence, inline-style count, and
table/image/nested-list/fixed-width/long-token scans over the **added text
only** — all clean after the A017 token fix (§6).

## 9. Guard delegation — the first batch that needed no repair

E3 recorded guard-expiry as a structural defect class: a guard that pins
corpus-wide state fails the moment the next authorised batch lands. Batch B's
guard pinned the corpus total; E4 found the A–D digest pins half-wired; E3
repaired `only_authorised_cards_changed` in E4's validator and, crucially,
**pre-emptively in its own** for batches that did not yet exist.

E2 is the payoff. **No guard needed maintenance.** Because the exemption is
keyed on a glob over `batch_*_manifest.json`, simply creating
`batch_e2_enrichment_manifest.json` before running the older guards was enough:

- `validate_batch_e3` now reports all **ten** E2 cards by name as
  `authorised-elsewhere`;
- `validate_batch_e4` reports **sixteen** (E3's six plus E2's ten);
- A/B/C/D and GAP-0609 pass unchanged.

Not vacuous, and not a weakening: mutation C still fails on a card no manifest
owns, and `CARD ADDED` / `CARD REMOVED` entries carry a suffix that can never
match a plain `file#anchor` exemption.

**Ordering still matters and is worth restating.** The E2 manifest had to exist
*before* those guards ran. In the window before it was written, A–D, GAP-0609,
E3 and E4 would all have reported genuine-looking drift on ten cards that were
legitimately edited — the guards would not have been wrong, the delegation
record simply would not yet have existed.

**Sibling pin delegation: none needed.** No earlier manifest pins any of the ten
E2 targets, checked programmatically against every `batch_*_manifest.json`. E2
required no digest-pin exemption of its own — unlike E3, which needed two.

## 10. Two operational traps hit this session

**A killed mutation run leaves the tree mutated.** The E2 mutation suite exceeded
a two-minute command timeout and was killed mid-run; so did the determinism gate
on its first attempt. In both cases the correct response was to inspect
immediately rather than reach for a blanket checkout. The mutation harness's
`finally` had restored its file — all ten card digests verified intact — but the
determinism gate had left **seven** generated artefacts modified and a
`.determinism-snapshot/` directory behind. Those seven were restored
individually, by name, and nothing else was touched. A blanket
`git checkout -- .` at that moment would have destroyed all ten production
edits.

**Long-running gates must be backgrounded from the start.** The full mutation
suite runs ~20 validator invocations, each of which shells out to
`build_examiner_index --check` and does ~170 `git show` calls. That is well past
any interactive timeout. Both later runs were backgrounded and completed cleanly.

## 11. New debt (5)

1. **`QB1_H#q5` carries an authoring-tool name in candidate view.** The card
   says "**The Gemini-drafted answer** did not state that GBS/SOLAS II-1 Reg.
   3-10 is scoped exclusively to..." and closes with "Source confidence: High
   after correction". Both are internal production vocabulary on a paid page.
   Pre-existing, outside the authorised limb, and not caught by the hygiene
   regex because neither string is in the banned set. Same class as the
   `[MS Act 2025 - ... pending verification]` leak recorded as DEBT-E3.
2. **`QB1_F#q8` cites a study website to a candidate.** The reg-box carries a
   live link to `marinegyaan.com` labelled `[reference]`, and the answer body
   carries `[MarineGyaan — Annual/Intermediate Survey Checklist]` inline. A
   third-party study site is exactly the class of source the batch brief forbids
   relying on, and here it is presented to the candidate as a citation.
   Pre-existing; not touched because it is outside the authorised limb.
3. **`QB3_H#q6` `data-tags` carries literal markdown.** Reads
   `"** marpol annex ii nls p&a manual cargo record book"` — a leading `**` from
   an unconverted bold marker, which also surfaces as a visible filter chip
   reading "** marpol annex ii". Same class as the E3 debt item on `QB2_B#q2`.
4. **DEBT-E2 remains open on `QB3_H#q6`** — the "Ship Recycling Sequence" block
   (IHM Parts I–III, Ship Recycling Plan) still sits inside a MARPOL Annex II
   card, while `QB3_H#q5` is the ship-recycling card. Recorded by the
   consolidation, confirmed present, deliberately not repaired here.
5. **`validate_audit` still exits 0 while reporting `failed: 1`.** Carried from
   E4 and E3, still unfixed; a caller trusting the exit code reads a failure as
   a pass. The failing check is `index_tier_literals_valid`.

## 12. Status

- Brand-new answer inventory: **COMPLETE 33/33**, unchanged.
- Canonical corpus: **721**, unchanged. Public count unchanged. Pricing untouched.
- Examiner index: **960 relationships / 7 examiners**, delta zero.
- Enrichment workload: **38 → 28 unique actions remaining** (E2's ten complete).
- Follow-up workload: **35 groups**, unchanged — E2's two colocated follow-ups
  are different limbs and were not resolved.
- Master XLSX: deferred.

## 13. Next batch

**E1 — Marine insurance, liability and commercial** (`ENRICH-A001`–`A010`,
10 actions).

Chosen on current consolidation figures, recomputed rather than inherited:

| Batch | n | E-P1 | Currentness (`CURRENT_REG`) | Dominant authority | Follow-up overlap |
|---|---|---|---|---|---|
| **E1** | **10** | **2 (20%)** | **2 (20%)** | 5 primary-authority, 3 technical-reasoning | 3 |
| E5 | 12 | **0** | 3 (25%) | 5 primary, 4 technical | 3 |
| E6 | 6 | 1 (17%) | **3 (50%)** | current-regulation | 1 |

E1 now carries the **highest remaining E-P1 count** of the three and the lowest
currentness exposure.

**The reason to revisit E1 is specific.** E3 deprioritised it on the grounds that
its authority is "market clause wording rather than convention text, which is the
weakest class for primary verification". E2 incidentally falsified that concern:
A011 needed the hull-insurance consequence of disclassing, and **Institute Time
Clauses – Hulls 1/11/95 proved publicly available and text-extractable**, with
clauses 4.1.1, 4.1.2, 4.3 and 5.1 quoted verbatim. The dominant authority class
for E1 has now been reached and read successfully. Note the distinction E2 also
had to make: the **Institute Classification Clause (CL.354)** is a *cargo*
clause and is not the hull class warranty — an easy and expensive confusion for
an insurance batch.

E6 remains the wrong pick on criteria despite being smallest: half its actions
are `CURRENT_REG_VERIFY_REQUIRED`, the highest temporal exposure of any remaining
batch, and the standing temporal boundaries plus the Coastal Shipping Act 2025 /
MS Act 2025 interactions are live hazards for it. E5 is last on twelve actions
and **zero** E-P1.

## 14. Verdict

**GO** — Final Oral Enrichment Batch E2 complete; all ten authorised
class/survey/structure edits verified and published.
