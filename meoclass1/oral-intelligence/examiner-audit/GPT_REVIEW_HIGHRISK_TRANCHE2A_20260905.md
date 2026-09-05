# GPT High-Risk Content Review — Tranche 2A

**Date:** 5 September 2026
**Baseline:** `419f3c6` (11 ahead of `origin/main` `9e26f02`, nothing pushed)
**Origin:** Founder / GPT independent review of the Tranche 2 adjudication packet
**Scope:** four authorised items only. No broad rewrite, no Tranche-3 review, no push, no
deploy, no Excel distribution, no full release suite.

This is the authorisation record named by three correction manifests:

| Family | Correction ID | Subject |
|---|---|---|
| A + B | `CORR-GPT-T2A-GRAIN-20260905` | QB2_A#q27 Grain Code criterion, and the `known_traps.md` authoring propagation |
| C | `CORR-GPT-T2A-QB5CB-20260905` | QB5_C_B#q5 reg-box: STCW Table A-III/2 → ISM Code §9 |
| D | `CORR-GPT-T2A-IMSBC-20260905` | QB2_B#q15 On My Vessel: containerised cargo and flexitanks are not IMSBC scope |

**Why three records and not four.** The brief asked for A, B, C and D separated "where
current architecture requires distinct records". The architecture answers it directly:
`oral_manifest.audit_correction_manifest` requires `cards_present` and
`exactly_one_primary_correction`, and a card requires `file`, `anchor` and two digests.
`known_traps.md` has no card, so it **cannot** be a correction record without pretending it
is one — which is precisely what the brief forbade. The closed field table already carries
the two fields built for this case: `known_traps_entries` (the trap number) and `artefacts`
("files this correction touched that carry no q-card and that no release guard pins,
deliberately carrying NO digest"). B therefore rides on A as a separately-classified,
separately-gated event, and the validator asserts it on its own checks.

---

## 1. Family A — QB2_A#q27, the Grain Code residual-area criterion

### 1.1 What was published

One site carried the criterion, in the *Risk Mitigations* body list:

> **For Grain Shift Risks:** … ensuring the calculated heel angle from an assumed shift
> stays under **12°**, keeping the net residual area **under the GZ curve** above
> **0.075 meter-radians**, and maintaining an initial GM of at least **0.30 meters**.

A second site, *Numbers to Memorise*, carried the 12° limb alone:

> **12°:** The maximum allowable final calculated angle of heel due to a dynamic grain shift.

This card was already known. `CORR-GPT-T1-GRAIN-20260904` found it in its scope pass and
recorded it under `propagation.found_and_not_swept` as "incomplete, not wrong … left alone
under the review's no-broad-rewrite instruction and REPORTED". Tranche 2A is the
authorisation that closes it. **No prior record owns q27** — this is the first governed
edit to that card, so the manifest declares no supersession ancestry.

### 1.2 The source, re-read

**IMO resolution MSC.23(59)**, International Grain Code as adopted, held at
`F:/RulesApp-Local-Input/true-source/03-imo-instruments/Grain-Code/_base-and-amendments/IMO_resolution_MSC.23-59_grain_code_as_adopted.pdf`,
sha256 `5b2107d304bcfd8ad6c5cc080c33a94a9d168b5aaa3895277c61134e6cad8678`, registered
`SRC-GRAINCODE-MSC23-59`. The hash was re-verified before the read. 31 pages. **Page 5**
was read through the OCR text layer and then against the page image, because the layer
carries visible artefacts (`betveen` for *between*, `40·` for *40°*).

**A 7.1.1** —

> ".1 the angle of heel due to the shift of grain shall not be greater than 12° or in the
> case of ships constructed on or after 1 January 1994 the angle at which the deck edge is
> immersed, whichever is the lesser"

**A 7.1.2** —

> ".2 in the statical stability diagram, the net or residual area between the heeling arm
> curve and the righting arm curve up to the angle of heel of maximum difference between
> the ordinates of the two curves, or 40° or the angle of flooding (θf), whichever is the
> least, shall in all conditions of loading be not less than 0.075 metre-radians"

**A 7.1.3** —

> ".3 the initial metacentric height, after correction for the free surface effects of
> liquids in tanks, shall be not less than 0.30 m"

### 1.3 The lower bound is NOT clause text, and is recorded as such

The brief required the corrected card to teach the area as measured **from the angle of
equilibrium**. That is correct, and it is what the Code depicts — but it is **not** in the
words of A 7.1.2, which state only the upper bound. The word *equilibrium* appears
**nowhere** in the Code as adopted; a full-text search of all 31 pages returns zero hits.

The lower bound comes from **figure A7**, on the same page, which was read as a rendered
page image rather than through the text layer. The shaded region is labelled **"residual
dynamic stability"** and begins at the **first intersection of the heeling arm line AB with
the righting arm curve** — the vertical the figure annotates **"angle of heel due to grain
shift"**. That intersection is the angle of static equilibrium. The figure's notes define
λ₀ = assumed volumetric heeling moment due to transverse shift ÷ (stowage factor ×
displacement), λ₄₀ = 0.8 × λ₀, and require the righting arm curve to be derived from
cross-curves including 12° and 40°.

So: **upper limits are quoted; the lower bound is derived from figure A7 of the same
instrument.** The card teaches it and names the figure. Asserting it as A 7.1.2 clause text
would be the same class of error this correction exists to fix.

### 1.4 Verdict and corrections

**UPHELD ON BOTH SITES.** Two defects, distinct:

1. **"the area under the GZ curve"** is the wrong object. A 7.1.2 measures the area
   *between two curves* — the residual after the grain heeling arm is subtracted. "Area
   under the GZ curve" names the whole-ship dynamic-stability integral of a different
   criterion family and points a candidate at the wrong integral entirely.
2. **No upper limit was stated at all.** Tranche 1 corrected q11 and q33 from a *one-limb*
   form ("up to 40°"); q27 was worse — it named no bound, so it is not merely incomplete
   but unbounded, and a candidate reading it has nothing to integrate to.

The body criterion now states A 7.1.1, A 7.1.2 and A 7.1.3 in full, with the
between-the-curves formulation, the angle of equilibrium as lower bound with its figure-A7
provenance, all three upper limits enumerated as **the least of**, and an explicit
instruction against both rejected forms. *Numbers to Memorise* gains the A 7.1.2 entry it
never had, and its 12° entry gains the deck-edge limb A 7.1.1 supplies — the same repair
tranche 1 made on q11's equivalent entry, left inconsistent across the file until now.

**Deliberately unchanged on q27:** the 15-second and 60-second answers, which state no
criterion figure and so carry nothing to correct (15s: "maintaining robust stability
margins"; 60s: "keeping the ship's initial GM well above statutory limits"); the
three-mechanism comparison table; the failure-matrix diagram; the CE Oral Tip; the Casualty
Link; and the On My Vessel block, none of which state the criterion.

**q26 is byte-identical**, before and after, digest
`adfa6bbde6599be1dcfccef569cb4ef3c8c3ff982546697f41614ef8507fa567`. Pass 2 found it clean
and this correction does not touch it. Its only hit in the criterion vocabulary sweep is a
Timber Code CE tip about the righting lever curve at large angles — a correct statement
about a different instrument.

### 1.5 The sweep, and what it found

Nine-pattern sweep over `meoclass1/QB2_A.html`, every occurrence mapped to its owning card
by document position: `0.075`, `40°`, *residual area*, `GZ`, *righting arm*, *heeling arm*,
*flooding angle*, *maximum difference*, *equilibrium*.

* **q27**: one criterion site (the body bullet) plus the Numbers block. **The brief's
  premise that these were two *additional* incomplete forms of the 0.075 proposition does
  not hold in the current tree** — there is exactly one 0.075 statement in q27, and the
  Numbers block carried no 0.075 at all. Both named sites are corrected; there is no third.
* **q11, q33**: governed by `CORR-GPT-T1-GRAIN-20260904`, both digests unmoved.
* **q13, q20, q26**: unrelated hits (flooding angle in a different context, GZ in
  free-surface and timber material).

**Reported, not swept (out of Tranche 2A authorisation):**

* **q11's body heading still reads "Net Residual Area on GZ Curve (A 7.1.2)"** while the
  text beneath it is fully correct and says *between the heeling arm curve and the righting
  arm curve*. The heading is the rejected terminology surviving as a label. It is a
  tranche-1-governed card and is not one of the four authorised items. **Referred to GPT.**
* **Neither q11 nor q33 teaches the lower bound** (angle of equilibrium). q27 now does. The
  corpus is therefore inconsistent in the other direction until GPT authorises. **Referred
  to GPT.**

---

## 2. Family B — `known_traps.md`, the authoring propagation

`meoclass1/known_traps.md` line 1321, inside trap **§55** (the MSC.552(108) third grain
compartment configuration):

> **What did NOT change.** The three intact-stability criteria are untouched — **12°**
> maximum heel, **0.075 m·rad** residual area **to 40°**, **0.30 m** minimum corrected GM …

**Verdict: UPHELD, and correctly classified by the brief.** `known_traps.md` is excluded
from Vercel deployment, so this is **not** a candidate-facing release defect. It is worse in
a different way: it is the **authoring source** of the short form, sitting in the file
authors consult while writing grain cards, and it is capable of reintroducing into a new
card exactly the defect three cards have now been corrected for.

Corrected to state A 7.1.1 to A 7.1.3 in full, with the between-the-curves formulation, the
angle of equilibrium and all three upper limits — and followed by a standing **AUTHORING
RULE** naming the short form, saying why it is wrong twice over, and recording that it is
the authoring source of the defect in q11, q27 and q33.

**No unrelated historical trap was rewritten.** Only the `What did NOT change` bullet of
§55 changed; the authoring rule is appended as a new bullet in the same trap. §56 and
everything else in the file are untouched.

Recorded on `CORR-GPT-T2A-GRAIN-20260905` as `known_traps_entries: [55]` and
`artefacts: ["meoclass1/known_traps.md"]`, and asserted by that record's own content
validator. It carries **no digest**, by the architecture's own rule: a pin on an unguarded
file expires on the next unrelated edit to it.

---

## 3. Family C — QB5_C_B#q5, the casualty-investigation reg-box

### 3.1 What was published

The reg-box carried four rows: Casualty Investigation Code (MSC.255(84)), MLC 2006
Regulation 4.3, SOLAS chapter XI-2 / ISPS, and:

> **STCW Code, Table A-III/2** — Minimum standard of competence for chief engineer officers
> … It is a competence standard, not an investigation provision.

Tranche 1 had already narrowed this row's description to a self-qualifying form and recorded
it as remaining, in its own report-only list.

### 3.2 Verdict

**UPHELD.** STCW Table A-III/2 is the management-level competence specification for chief
engineer officers and second engineer officers on ships powered by main propulsion machinery
of 3,000 kW propulsion power or more. It is not a casualty-investigation provision, and the
row said so about itself — a row whose description has to explain that it does not govern
the question is a row that does not belong in that box.

Meanwhile **ISM Code §9 is load-bearing in this card and absent from the box**: it appears
in the 15-second answer, the 60-second answer, the Numbers/Regs block and the CE Oral Tip.
The brief's caution against adding a regulation merely to preserve four rows does not bite
here — §9 is already the proposition the card teaches.

### 3.3 The correction

A-III/2 is removed. The slot takes:

> **ISM Code §9** — Reports and analysis of non-conformities, accidents and hazardous
> occurrences — the Company's SMS procedures for reporting, investigating and analysing
> them, with corrective action under §9.2. This is the **company SMS investigation and
> learning** limb, run through the Master and the Designated Person Ashore. It is **not**
> the flag State's statutory **marine safety investigation**, which is conducted by that
> State's marine safety investigation Authority under the Casualty Investigation Code
> (MSC.255(84)) in the first row above.

The two-layer distinction the brief required is carried **inside the new row**, contrasting
against the MSC.255(84) row, which is left **byte-unchanged** and remains the statutory
investigation reference. Nothing in the new wording implies §9 governs the flag-State marine
safety investigation; it says the opposite, in terms.

---

## 4. Family D — QB2_B#q15, IMSBC scope in On My Vessel

### 4.1 The contradiction

The card's own Trap Question is **correct**:

> **IMDG** covers hazardous materials carried in *packaged form* (drums, cylinders, or
> containers), whereas the **IMSBC Code** governs loose, un-packaged hazardous materials
> loaded directly into the ship's bulk cargo holds.

Its *On My Vessel* block then contradicted it:

> Applied in Maersk container routing when handling containerized bulk shipments, ensuring
> **flexitanks** or solid bulk liners inside standard boxes comply with equivalent weight
> and distribution limits.

### 4.2 The source

**IMSBC Code as adopted, resolution MSC.268(85)**, held at
`F:/RulesApp-Local-Input/true-source/03-imo-instruments/IMSBC-Code/_base-and-amendments/MSC.268(85).pdf`,
sha256 `690a9dae8ffce1b00d695a4e839d60c3e1bd7c1d10bab3d33f96de85a116d9a5`, 372 pages. The
resolution reproduces the governing SOLAS regulations.

**SOLAS VI/1-1.2** (page 9) —

> "2 Solid bulk cargo means any cargo, other than liquid or gas, consisting of a combination
> of particles, granules or any larger pieces of material generally uniform in composition,
> which is loaded directly into the cargo spaces of a ship **without any intermediate form
> of containment**."

**IMSBC 1.4.1** (page 7) —

> "The provisions contained in this Code apply to all ships to which the SOLAS Convention, as
> amended, applies and that are carrying solid bulk cargoes **as defined in regulation 1-1
> of part A of chapter VI** of the Convention."

### 4.3 Verdict

**UPHELD, and settled by a definition rather than by a prohibition** — which is what makes
the gate a fact rather than a judgement. Two independent limbs each exclude the published
claim:

* a **freight container is an intermediate form of containment**, so containerised cargo
  falls outside the definition however bulk-like the commodity is; and
* a **flexitank is liquid**, so it is outside "other than liquid or gas" as well. It is
  excluded twice over.

The block now states the definition, applies both limbs, and points to what actually does
govern a cellular containership: the IMDG Code for dangerous goods in packaged form
including in containers, the applicable container / CTU framework, and the approved Cargo
Securing Manual. **No Maersk-specific procedure is invented** — the block asserts only the
regimes that apply to the ship type and says the answer comes from the Code rather than from
bulk-carrier practice the writer does not have.

**The main answer was not rewritten.** It is correct as it stands, and the Trap Question
that already draws the IMSBC/IMDG line is preserved verbatim.

### 4.4 Propagation

Corpus-wide sweep for `flexitank` and for containerised-cargo-under-IMSBC across
`meoclass1/` and `SQ/`:

* **QB2_B#q15 On My Vessel** — the only site placing containerised cargo or flexitanks
  inside IMSBC scope. Corrected. **No duplicate copies of that proposition exist.**
* **QB1_F.html** (4 sites) — flexitanks under **CSC Annex II** structural controls and
  container stack loading. Correctly framed under the container framework, never under
  IMSBC. Not the same proposition; untouched.
* **QB2_A#q27 On My Vessel** — "any specialized dry bulk charters … require the vessel's
  loading computer to be configured with approved IMSBC and Grain modules". This is about
  dry bulk charters, not containerised cargo, so it is not the corrected proposition. It is
  also not within the criterion scope authorised for q27. **Untouched, and reported.**
* **`meoclass1/oralnotes/miw-notes-mgmt-p14.html`** — "Container tonnage does not carry
  IMSBC bulk cargoes". Already correct and consistent with this correction.

---

## 5. SOLAS VI vs VII — READ-ONLY ADJUDICATION, NOT IMPLEMENTED

### 5.1 The brief's premise does not match the tree

The brief recorded that q15's 15-second answer cites **SOLAS VI** and its 60-second answer
cites **SOLAS VII**. **In the current tree both short layers cite chapter VII**, in
materially the same words:

* 15-second: "The IMSBC Code provides a mandatory framework under **SOLAS Chapter VII** to
  manage the risks of transporting solid bulk cargo."
* 60-second: "…is a mandatory framework under **SOLAS Chapter VII** designed to ensure the
  safe stowage and carriage of solid bulk materials, excluding grain."

Chapter VI appears elsewhere in the card, correctly: the Key Numbers block gives "**SOLAS
Chapter VI, Part B:** the underlying international regulation for loading and stowing
general bulk cargoes", and the reg-box carries **both** chapters — VII/7-1 and VI/2.

So the finding is not "VI in one layer, VII in the other". It is that **the two short layers
attribute the whole Code's mandatory basis to chapter VII alone**, while the deeper material
in the same card has it right. The card is internally inconsistent, not split between two
defensible readings.

### 5.2 What the source says

**IMSBC Code foreword, page 3** —

> "The International Convention for the Safety of Life at Sea, 1974 (SOLAS Convention), as
> amended … contains, in **parts A and B of chapter VI** and **part A-1 of chapter VII**,
> the mandatory provisions governing **the carriage of solid bulk cargoes** and **the
> carriage of dangerous goods in solid form in bulk**, respectively."

**Resolution MSC.268(85), operative recitals** — notes MSC.269(85), "by which it adopted
amendments to **chapters VI and VII**" of SOLAS "to make the provisions of the … IMSBC Code
mandatory under the Convention".

**SOLAS VI/1-2.1** (page 9) — "The carriage of solid bulk cargoes other than grain shall be
in compliance with the relevant provisions of the IMSBC Code."

**SOLAS VII/7-1.1** (page 13) — "this part applies to the carriage of **dangerous goods in
solid form in bulk**".

**IMSBC 1.4.1** anchors the Code's own application clause to **regulation 1-1 of part A of
chapter VI**.

### 5.3 Adjudication

**Both chapters are load-bearing and they carry different subjects, so both citations can be
correct — but not for the claim the short layers are making.** Chapter VI parts A and B
carry the general solid-bulk mandate and are the Code's own application anchor; chapter VII
part A-1 covers only the dangerous-goods-in-solid-form-in-bulk subset, which in the card's
own taxonomy is the Group B / MHB limb. Attributing the **whole Code's** mandatory basis to
chapter VII alone, as both short layers do, is wrong on the primary anchor.

### 5.4 NOT IMPLEMENTED

The brief authorised implementation of this limb only if the evidence is unambiguous **and**
the correction is a direct consequence of the authorised IMSBC-scope correction. The
evidence is now unambiguous; the second condition **fails**. Which SOLAS chapter makes the
Code mandatory is a separate proposition from whether containerised cargo and flexitanks
fall inside the Code's scope, and correcting it would touch the 15-second and 60-second
answers — layers the authorised correction does not reach.

**REPORTED ONLY. Awaiting GPT authorisation.** The source texts above are quoted in full so
the decision needs no further reading.

---

## 6. Source currentness

**Grain Code.** MSC.23(59) is the Code as adopted. The 2026 amendment layer, MSC.552(108)
(adopted 23 May 2024, in force 1 January 2026), is governed by
`CORR-GRAIN-MSC552-20260831` and expressly did **not** change the A 7 criteria — which is
what §55 of `known_traps.md` records and what this correction preserves.

**IMSBC Code.** MSC.268(85) is the base Code; the corpus holds amendments through
MSC.500(105). **Amendment 08-25 (MSC.575(110)) is not held**, and its status — voluntary
application from 1 January 2026, envisaged entry into force **1 January 2027** — is already
recorded in `known_traps.md` §55. It is **deliberately not introduced** into any corrected
card: the proposition written into QB2_B#q15 is the **base-Code scope definition** at SOLAS
VI/1-1.2, which no amendment in the held chain alters. **Nothing in this tranche teaches a
2027 amendment as mandatory in September 2026**, and nothing relies on amendment-specific
text.

---

## 7. Deferred — remaining Tranche 2 findings, NOT implemented

Untouched and still under GPT review: QB7_D#q14 purge/asphyxiation enrichment; the remaining
P1 findings; the nine external-verification propositions; the 17 empty declared 15-second
layers; the 10 no-layer architecture cards; other On My Vessel Class-C blocks; other casualty
links; release-gate registration debt.

Added to that queue by this tranche: q11's "on GZ Curve" heading label (§1.5); the absent
lower bound on q11 and q33 (§1.5); q27's On My Vessel dry-bulk-charter claim (§4.4); and the
SOLAS VI/VII short-layer attribution (§5).

---

## 8. Governance, and two things the architecture required that the brief did not

**Commits.** `77fc842` carried the four content corrections; `44e7d2c` carried the
quoting fix and the two new authoring traps. Both are named in every record's
`governing_commits`, in order, because `validate_corrections.py` requires the
LAST governing commit to have produced the pinned post-state.

**Traps 74 and 75 were added because the architecture requires them.** Thirty-six
of the thirty-eight correction records on disk declare `known_traps_entries`, and
`validate_corrections.py` asserts the declared entries exist. The two new records
were the only omissions. That is not a formality: a correction is finished when
the authoring file records why the wrong version was plausible, which is exactly
what family B is about in the other direction. **74** closes the STCW Table
A-III/2 row that trap 73 had recorded as found-but-not-authorised, and states the
general rule — a reference row whose description has to say what it is *not* is
answering a question the card did not ask. **75** records that the IMSBC Code
excludes a container by *definition* rather than by prohibition, with both limbs,
and carries the 08-25 currency caution so the next author does not reach for an
amendment to answer a scope question. Both carry `GREP: SKIP` notes, because both
corrected cards now legitimately contain the words a keyword sweep looks for.

**The `unquoted()` guard is a span relation, not character adjacency.** The
tranche-1 gate exempted a rejected phrase only when a quote sat within two
characters either side. q27 quotes *"the area under the GZ curve up to 40°"*, so
the opening quote is four characters early and the closing one nine late, and
adjacency called a taught-against phrase an assertion. Containment inside a paired
quote span is what "directly quotes" means. The card text was also written so that
both rejected forms are quoted — the guard was made sound by making the product
honest, not the other way round.

**The correction-log entry is OWED and deliberately not written.** Tranche 1 added
a `recently_updated` entry; this tranche did not. A log entry is candidate-facing
published editorial content, and the brief authorised no deploy, no Excel
distribution and no hub-date change — `meoclass1/index.html` still reads *Last
Updated: 2 Sep 2026*. Writing the log now would announce a change candidates
cannot see. It is recorded in all three records' `content_index_effect` as a
decision rather than an omission, and gated by
`content_log_entry_deferred_on_the_record`.

`meoclass1/qb_content_index.json` was regenerated from the live HTML and came back
**byte-identical**: 761 canonical questions across 86 question-bearing files.
