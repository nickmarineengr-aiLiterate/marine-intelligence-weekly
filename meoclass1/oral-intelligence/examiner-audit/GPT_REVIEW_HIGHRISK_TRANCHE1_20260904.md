# GPT High-Risk Content Review — Tranche 1

**Date:** 4 September 2026
**Baseline:** `e0fc2aa` (9 ahead of `origin/main` `9e26f02`, nothing pushed)
**Origin:** Founder / GPT independent review of the published corpus, high-risk content pass
**Scope:** bounded surgical correction. No broad rewrite, no push, no deploy, no Excel
distribution, no full release suite.

This is the authorisation record named by four correction manifests:

| Family | Correction ID | Subject |
|---|---|---|
| A | `CORR-GPT-T1-GRAIN-20260904` | Grain Code stability criterion and Part B shift assumptions |
| B | `CORR-GPT-T1-LIION-20260904` | Li-ion battery fire, CO₂, and a wrong-scope IMO circular |
| C | `CORR-GPT-T1-EIAPP-20260904` | surviving EIAPP-invalidation propagation site |
| D | `CORR-GPT-T1-QB5CB-20260904` | QB5_C_B#q5 bounded quality repair, and one unsupported cheat-sheet hook |

---

## 1. Family A — Grain Code (QB2_A#q11, #q33)

### A.1 The residual-area criterion was reduced to one of its three limits

**Reported:** the cards taught the residual-area criterion as, in substance, *"area up
to 40°"*.

**Verdict: UPHELD, and read from the instrument.** The Grain Code as adopted is held in
the corpus as the annex to resolution **MSC.23(59)**, registered as
`SRC-GRAINCODE-MSC23-59` (sha256 `5b2107d3…`, 31 pages). Page 5 carries **A 7.1.2**:

> ".2 in the statical stability diagram, the net or residual area between the heeling
> arm curve and the righting arm curve up to the angle of heel of maximum difference
> between the ordinates of the two curves, or 40° or the angle of flooding (θf),
> whichever is the least, shall in all conditions of loading be not less than 0.075
> metre-radians"

Three limbs, joined by **whichever is the least**. The card kept only the second. This
is not pedantry: on a great many grain loading conditions the **maximum-difference
angle** governs, well before 40°, so a candidate who states the criterion the old way
computes the wrong area.

Corrected in the 60-second answer, the body criterion list, Key Numbers, Common CE
Failures and Numbers to Memorise on **q11**, and in both the body and the Numbers block
on **q33**. The 15-second answer on q11 was examined and left alone: it never stated the
limit at all, so there was nothing there to correct.

### A.2 The 15°/25° assumption was described as the ship's roll

**Reported:** the shift angle was described as *"an angle matching the rolling
amplitude"*.

**Verdict: UPHELD.** Part B prescribes an **assumed grain surface after shifting**; it
does not model the ship's roll. Read from the same instrument:

| Provision | Configuration | Assumed surface after shifting |
|---|---|---|
| **B 2.3** (p.24) | filled compartment, trimmed | **15°** to the horizontal |
| **B 3.2.1** (p.27) | filled, untrimmed, exempt from trimming outside the hatchway periphery (A 10.3.1) | **25°**, but **15°** in any section whose mean transverse void area ≤ that from B 1.1 |
| **B 3.3** (p.28) | filled, untrimmed, exempt from trimming in the ends (A 10.3.2) | **15°** abreast of the hatchway, **25°** in the ends |
| **B 4** note (p.28) | trunks, wing spaces not properly trimmed | **25°** |
| **B 5.1** (p.28) | partly filled, free surface not secured under A 16 / A 17 / A 18 | **25°** to the horizontal |

Vertical-shift factors, same instrument: **1.06 ×** the calculated transverse heeling
moment where the Administration allows underdeck voids to be taken into account in a
filled, trimmed compartment (**B 1.3**, p.23), and **1.12 ×** in a partly filled
compartment (**B 1.5**, p.23).

The 2026 layer is unchanged and already correct on q33: **MSC.552(108)**'s new Part B
section takes the B 2 provisions except that the surfaces after shifting are assumed at
**25°** (`SRC-GRAINCODE-MSC552-2026`).

A new body section states all of this, the CE Oral Tip's filled/partly-filled
distinction now carries B 2.3 and B 5.1 by clause, and both the card body and Common CE
Failures say in terms that these are **calculation assumptions, not roll angles**.

### A.3 MV *Leros Strength* removed as a grain casualty

**Verdict: UPHELD, and already on the correction queue.**
`CORR-GRAIN-MSC552-20260831` recorded this as a pre-existing defect it deliberately did
not fix: *"the Casualty Link attributes MV Leros Strength (1997) to grain-related
stability degradation when she was carrying apatite concentrate and was lost to
structural failure"*. Founder/GPT independently reached the same conclusion — she was
laden with approximately 18,000 t of **apatite**, not grain.

**No substitute casualty was invented.** The Casualty Link now says that no specific
casualty is necessary to answer this question, that the Grain Code addresses the
stability hazard created by transverse grain shift, and that a named ship offered as
grain evidence is a mark lost the moment the examiner knows what she was carrying.

### A.4 The false "On My Vessel" claim removed

**Verdict: UPHELD.** The block asserted Maersk *"dual-purpose vessels or geared fleet
configurations carrying agricultural bulk under charter plans"*. That is not established
Founder experience and does not belong in a Maersk container-vessel block. It is
replaced with the truthful container-vessel relevance: bulk grain is not a cargo regime
the Founder operates, the Grain Code does not apply to his ship, and what the
examination expects is the principle — assumed shifted surface → volumetric heeling
moment → residual stability tested against A 7.1 — plus the Document of Authorisation
and grain loading manual regime. **No Maersk cargo practice is invented.**

---

## 2. Family B — Li-ion battery fire (QB2_A#q7)

### B.1 The CO₂ proposition conflated two different things

**Reported:** the card taught *"CO₂ will not extinguish a Li-ion thermal runaway"* and
derived an operational conclusion equivalent to *do not release / do not waste the fixed
CO₂ system*.

**Verdict: UPHELD, and this is the most safety-sensitive item in the tranche.** The old
Examiner Trap told the candidate the answer *"must be: **No, CO₂ will not extinguish a
Li-ion thermal runaway**"*, and that releasing CO₂ *"can waste your fixed extinguishing
agent"*. Two distinct things were run together:

* **Thermal runaway.** CO₂ does not remove heat from the cells, does not stop the
  internal electrochemical self-heating, and cannot by itself prevent propagation or
  re-ignition. Cooling is therefore crucial. *(This limb of the old card was correct.)*
* **Flaming combustion in an enclosed space.** This is oxygen-dependent, and it is
  exactly what a fixed gaseous installation in a protected space addresses. Telling a
  Chief Engineer that CO₂ is categorically useless, and that an installed fixed system
  should be held back because lithium cells are involved, is wrong and unsafe.

The corrected answer states the distinction in the substance the review directed: CO₂
may suppress the external flaming fire but cannot cool the battery or terminate internal
thermal runaway; re-ignition and continued propagation remain possible, so the
fixed-system response must be combined with temperature monitoring, boundary cooling and
the ship's emergency procedure.

The universal action sequence was also conditioned. The 15-second and 60-second answers
now run under the **Master's emergency command and the ship's fire control plan**, and
turn on location, whether the space is enclosed and sealable, accessibility of the cells,
and what is actually installed. A new body bullet, *"The Fixed Installation — and Who
Decides"*, names the release decision as the Master's on the CE's technical advice, and
lists what it turns on — *"not the mere presence of lithium cells"*. Boundary cooling and
direct cell cooling are distinguished explicitly wherever cooling is mentioned: for a
closed container stowed in a hold only the boundary is reachable.

Common CE Failures now names the failure at **both** ends — the candidate who thinks
smothering ends the event, and the candidate who declares CO₂ useless and withholds the
system. The examiner chain's *"Why doesn't CO2 work?"* became *"What will CO₂ do, and
what will it not do? → Who decides to release the fixed system, and on what?"*

### B.2 MSC.1/Circ.1615 was cited at the wrong scope

**Reported:** the REG-BOX cited MSC.1/Circ.1615 as *"Guidelines for preventing and
mitigating lithium battery fires"* — i.e. as IMO guidance governing a containerized
Li-ion battery fire.

**Verdict: UPHELD.** The circular's actual title is **"Interim guidelines for minimizing
the incidence and consequences of fires in ro-ro spaces and special category spaces of
new and existing ro-ro passenger ships"**, approved at MSC 101 and dated 26 June 2019. It
carries material on alternatively powered vehicles; it is **not** generic containership
or containerized-lithium-battery fire guidance.

*Evidence tier, stated rather than glossed:* the circular itself is **not held** in the
corpus and IMO's own PDF for it was not reachable (HTTP 404 on the CDN path tried). The
title, date and MSC 101 approval were confirmed against two independent secondary
sources — imorules.com's circular index and Bureau Veritas's MSC 101 report — and agree
with the Founder/GPT independent verification. That is enough to establish that the old
description was wrong; it is **not** relied on for anything the circular says.

**Treatment:** the review permitted removal, or retention *"only if the answer explicitly
and accurately labels its ro-ro-passenger-space scope, which is probably unnecessary
here."* **Retention with an explicit scope label was chosen**, as a `Scope caution` row
that names the real title, says the card itself previously mis-cited it, and states in
terms that it must not be quoted as generic containership guidance. The reasoning: this
is a mis-citation the corpus itself made and candidates repeat, so an inoculation is
worth more than a silent deletion. **No substitute circular was invented.**

**IMDG material kept, and separated.** The REG-BOX now has two distinct rows —
*"IMDG Code — transport classification"* (Class 9, UN 3480 / UN 3481 as applicable,
labelled as governing declaration, packing, marking, stowage and segregation and
explicitly **not** firefighting guidance) and *"IMDG Code — EmS emergency schedules"*
(F-A and S-I, qualified as *"shown against the applicable UN entry in the IMDG amendment
in force"*, with the candidate told to read the entry for the consignment actually
carried rather than a remembered pair). The SOLAS II-2/19 row now names the ship's fire
control plan and who releases a fixed installation.

---

## 3. Family C — QB5_J#q2 propagation

Pass 1 (`CORR-GPT-PASS1-20260904`) corrected the absolute proposition *"going outside
Technical File settings invalidates the EIAPP certificate"* in the body Trap point and
the REG-BOX. Tranche 1 found **one surviving candidate-facing site in the same card**:

> *Deep-Dive: Trap Questions* — "Q: Can you advance the timing to recover performance?
> **A: Only within the NOx Technical File — outside it the EIAPP is invalidated.**"

**Verdict: UPHELD.** It is the same rejected proposition, in the same card, in the
answer to a question the candidate will actually be asked. It is corrected to the
already-governed Pass-1 wording — the full range of adjustments the Technical File
identifies as allowable, the approved route (amendment of the technical file, and
verification at survey by the engine parameter check method), and the conditional
consequence: an unapproved departure **can** leave the engine no longer compliant with
its certified NOx configuration.

The rest of the answer was **not** reopened. The card-scoped sweep result is recorded in
the manifest: after the fix, no candidate-facing positive assertion of automatic EIAPP
invalidation survives anywhere in QB5_J.

---

## 4. Family D — QB5_C_B#q5, bounded quality repair

Each reported finding was verified against the card and the governing source before
anything was changed.

| # | Finding | Verdict | Disposition |
|---|---|---|---|
| A | 15-second answer empty | **CONFIRMED** | written from the card's own verified substance |
| B | bare "ISM Code Section 5" in the REG-BOX | **CONFIRMED** | removed |
| C | four `reg-desc` with no `reg-code` | **CONFIRMED** | structural markup repaired |
| D | truncated Casualty Investigation Code title | **CONFIRMED** | full instrument identity restored |
| E | hostage/piracy CE tip on a casualty-investigation question | **CONFIRMED** | rewritten to the real discriminator |
| F | "seize and lock away the Oil Record Book" | **CONFIRMED** | rewritten as preservation, not impoundment |
| G | "will result in immediate criminal prosecution, cancellation of CoC" | **CONFIRMED** | made conditional |

**B.** ISM Code section **5** is *Master's Responsibility and Authority*. That was
established by `CORR-ISMSEC5-20260904` in Pass 3 and is unchanged here. It is not a
casualty-investigation provision and cannot support anything this card says, so it is
removed rather than re-described.

**D.** The instrument is the *Code of the International Standards and Recommended
Practices for a Safety Investigation into a Marine Casualty **or Marine Incident***
(Casualty Investigation Code), adopted by resolution **MSC.255(84)**. The body had it
truncated at "Marine Casualty".

**F.** No investigation or evidence procedure gives the Chief Engineer a power to seize
statutory records, and the Oil Record Book in particular must remain available for
inspection. The bullet now says: preserve exactly as they stand, nothing altered, erased
or back-dated; secure against alteration or loss on the Master's authority and under the
company's SMS procedure; open a fresh supplementary logbook; *the records are not mine to
impound*; make them available through the Master to those authorised to receive them, and
keep a documented chain of custody. The card's own Trap Warning — refusing to surrender
**originals** to non-statutory local entities while offering certified copies and
escalating — is consistent with this and was left intact.

**G.** No governing law makes prosecution or CoC cancellation automatic. The claim is now
conditional on the facts, the jurisdiction and the authority seized of the case, and says
in terms that what follows *"is decided by the competent authority on the evidence — it
is not automatic"*, without weakening the professional warning.

### D.1 The unsupported SOLAS V/14 hook (`QB5_B_CheatSheet.html`)

The *Taking Over as CE* checklist's **Pre-arrival** row — review vessel history,
outstanding defect list, SMS documents, previous PSC reports, class certificate validity
— carried the hook *"ISM Code §6.3 (familiarisation on a new assignment) / SOLAS V/14"*.
**SOLAS V/14 is *Ships' manning*.** It does not govern the review of a defect list, an
SMS or a PSC history. **The hook is deleted; nothing is substituted.** The ISM §6.3 hook,
which does govern the row, stays.

The **Manning check** row's *"STCW 2010 / SOLAS V/14 / MLC 2006"* was examined and
**deliberately left alone**: manning is precisely what V/14 governs, so it is correctly
cited there.

A cheat sheet carries no q-card, so no release guard pins it and no digest can be taken
over it. It is declared in the family D manifest's `artefacts` and its substance is
asserted instead by the named content gate — the same treatment
`CORR-MSACT2B-CEHANDOVER-20260904` gave the *Formal declaration* row of this same table.

**Why it rides on family D rather than standing alone:** the record schema makes `cards`
load-bearing, and a correction record whose `cards` list is empty passes every
card-oriented check vacuously. Family E is therefore governed as a declared artefact of
the record it is closest to in defect class — an authority attached to a proposition it
does not govern, which is exactly what ISM §5 was doing in D.B.

---

## 5. Accepted cards — untouched

`QB3_F#q8`, `QB7_D#q13`, `QB1_K#q10`, `QB2_A#q34`, `QB5_I#q8`, `QB3_J#q5`, `QB1_D#q6`
and the `QB5_B#q1` Pass-3 correction were **not** edited. No propagation from §§1–4
reached any of them; the sweeps that establish this are recorded per family in the
manifests.

---

## 6. Newly discovered — REPORTED, NOT FIXED

1. **`QB5_C_B.html` has eight empty 15-second answer blocks**, of which q5 was one. The
   other seven (`q1`, `q2`, `q3`, `q4`, `q6`, `q7`, `q8` — see the manifest for the
   verified list) are outside this tranche's authorisation and were left alone. Every
   edit in family D was made card-scoped precisely so a whole-file replace could not
   silently touch them.
2. **`QB5_C_B#q5` REG-BOX still carries STCW Code, Table A-III/2.** It is a competence
   standard, not an investigation provision, so its relevance to this question is thin —
   the same defect class as the SOLAS V/14 hook. It was **not** removed, because it was
   not a reported finding and §H directs that new discoveries be reported. Its
   description is now honest about what it is and is not.
3. **`QB2_A` line ~2993** (the bulk-cargo failure matrix card) states the residual-area
   criterion as *"keeping the net residual area under the GZ curve above 0.075
   meter-radians"*. That is **incomplete but not wrong** — it makes no 40° claim — so it
   was left alone under the no-broad-rewrite instruction.
4. **`SRC-GRAINCODE-MSC23-59`'s text layer** carries OCR artefacts (`HSC.23(S9)`,
   `ahall`, `boa rd`). Every provision quoted in family A was checked against the page
   image. The registry row already records this caveat.

---

## 7. Held back, deliberately

* `meoclass1/index.html` still reads **"Last Updated: 2 Sep 2026"**. Not patched — the
  review directs that the date be reported, not changed, while further tranches may
  still arrive. The value it will eventually need is 4 Sep 2026.
* No Excel distribution, no push, no deploy, no full release suite.
