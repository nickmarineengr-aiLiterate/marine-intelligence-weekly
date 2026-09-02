# GPT REVIEW SET — August 2026 final closure production

**Record class:** independent-review packet
**Date:** 2026-09-02
**Prepared for:** Founder / GPT content review **before** publication authority is given
**Status:** NOT PUSHED. NOT DEPLOYED. NOT PUBLISHED. No workbook distributed.

**Corpus:** 759 → **761** canonical questions across **86** question-bearing files.
**Examiner relationships:** 958 across 7 examiners — **unchanged, tier for tier**.

---

## 0. Read this first — the scope changed, and why

The brief that opened this batch asked for **five** new canonical answers:
AUG-0095, AUG-0140, AUG-0148, AUG-0266, AUG-0268.

Three of those five **already have canonical answers** and were already disposed
of, under governance, without a new card. The brief was reading
`AUGUST2026_INTAKE_ADJUDICATIONS.json → adjudications[].classification`, which is
**frozen at intake** and answers only *"did a matching card exist when this ask
was first scored?"*. The production **disposition** is a different field in a
different file, written later, after the reuse-first pass and after independent
review: `AUGUST2026_PRODUCTION_QUEUE.json → production_outcomes.H3A`.

Each of the three was re-verified here **against the live card body**, not
against the summary. The Founder ruled on 2026-09-02 that the dispositions stand
and that no duplicate standalone roots be created.

This is now recorded as **known_traps entry 63** so the next reader of the
adjudication file does not repeat it.

**So this packet contains three things to review:**

| # | Item | What it is |
|---|---|---|
| A | `QB5_J#q2` | New canonical card — AUG-0266 |
| B | `QB5_I#q8` | New canonical card — AUG-0268 |
| C | `QB1_D#q7` | CE Oral Tip added to an existing published card — H5C-RES-01 |
| D | Annex | Evidence that AUG-0095 / AUG-0140 / AUG-0148 are already answered |

---

# A. QB5_J#q2 — AUG-0266

| Field | Value |
|---|---|
| **Canonical ID** | `QB5_J#q2` |
| **File path** | `meoclass1/QB5_J.html` |
| **Local anchor** | `#q2` |
| **Triggering occurrence** | `AUG-0266` (submission `AUG2026-S027`, Snapshot 03, 31-Aug-2026 LPG carrier) |
| **Candidate's question, as reported** | "As a Chief Engineer, how will you decide your main engine is not performing well?" |
| **Card question text** | "As Chief Engineer, how will you decide that your main engine is not performing well?" |
| **Action ID** | `H6-001` |
| **Post-edit digest** | `9a73504bc93c782676eeb87e38714ec51e15d7b86ac98f00b33105e7a6bd478d` |
| **Commit** | `e910dd3` |

### Why a new canonical root was required

The adjudication ran three body-scoped negative searches and quoted the body of
every card it rejected:

* `main engine.{0,60}(performing|performance)` → 2 hits, both rejected.
  `QB4_B#q17` is confined-water manoeuvring readiness, not condition diagnosis.
  `QB5_C_A#q3` is **voyage** performance — it diagnoses the voyage against
  weather and slip and names engine deterioration only as one candidate cause;
  it never sets out how the engine itself is judged.
* `(decide|determine|assess|judge).{0,40}engine.{0,40}(perform|condition)` → 1
  hit, `QB5_A#q3`, rejected: it is the Johari Window, and the match is human —
  "how the engine room team performed".
* `engine.{0,25}(deteriorat|underperform|poor performance)` → 0 hits.

### Placement rationale

`QB5_J.html` is titled **"Main Engine, Fuel & Turbocharger"** and is the topic
owner. Its only existing card, `QB5_J#q1`, is *Lower Calorific Value and why
engine performance is quoted against LCV* — which is exactly the normalisation
basis this card depends on, and the card cross-references it. **No new QB file
was created**; total files stay at 86.

### 15-Second Answer — full text

> Never on a single reading. I decide by comparing the engine against **its own
> shop-trial and sea-trial baseline**, after correcting the measurement to
> reference conditions and after eliminating hull, propeller, weather and
> draught effects. The engine is underperforming when, at the same corrected
> power, it needs **more fuel index and more fuel — a rising SFOC** — or when it
> can no longer reach its rated power while still inside its own limiters.

### 60-Second Answer — full text

> "Sir, performance is a **comparison, not a measurement**. A single exhaust
> temperature or a slow passage tells me nothing on its own, so I work through a
> fixed sequence. First I fix the **reference** — the shop-trial and sea-trial
> curves and the ship's own steady-state record taken after the last drydock.
> Second I **normalise**: correct the readings to ISO 3046-1 standard reference
> conditions and correct SFOC to the reference LCV of **42,700 kJ/kg**, then
> strip out displacement, draught and trim, weather, current and hull and
> propeller fouling — otherwise I will blame the engine for the hull. Third I
> read the **engine's own parameters**, which do not depend on the sea: fuel
> index at a given power, Pcomp and Pmax from indicator or draw cards, exhaust
> temperature and its deviation across cylinders, scavenge pressure and
> temperature, turbocharger speed, and back pressure. Fourth I **localise** —
> one cylinder out of line is a unit fault, all cylinders drifting together is a
> system fault on the air side, the fuel side or the load. Only then, fifth, do
> I **confirm**: check the instrument before the engine, repeat at steady state,
> and make sure the engine is not simply sitting on a limiter. A limiter is
> protection, not a defect."

### Full answer — structure and summary

Sections: *Governing instrument* · *Step 1 — Fix the reference before you
measure anything* · *Step 2 — Normalise, or you will convict the wrong
component* · *Step 3 — Read the parameters that belong to the engine alone* ·
*Step 4 — Localise: one cylinder, or all of them?* · *Step 5 — Confirm before
you declare a fault* · *Trap point*.
Deep-dives: CE Relevance, Trap Questions, Common CE Failures, Numbers to
Memorise, Casualty Link, On My Vessel.

The spine the examiner asked for is **baseline → normalise → engine's own
parameters → localise → confirm**, not a parameter list.

* **Step 1** distinguishes shop trial (bed test, dynamometer), sea trial (actual
  installation and propeller) and the post-drydock steady-state record, and
  states that *a baseline taken with a fouled hull is worthless* because every
  later comparison inherits the error.
* **Step 2** normalises to ISO 3046-1 reference conditions, corrects SFOC to
  reference LCV, then removes displacement/draught/trim, weather, current,
  shallow water, and hull/propeller fouling via **ISO 19030**.
* **Step 3** lists only ship-independent parameters, with the diagnostic
  readings paired rather than isolated: **low Pcomp** → compression loss (rings,
  liner, leaking exhaust valve, or low scavenge pressure); **low Pmax with
  normal Pcomp** → injection side (timing, quantity, atomisation);
  **turbocharger speed read together with scavenge pressure** — speed up with
  boost down suggests a fouled/damaged compressor, speed down with boost down
  suggests the turbine side or fallen exhaust energy.
* **Step 4** is the load-bearing logic: **one cylinder out of line = unit fault;
  all cylinders drifting together = system fault**, worked through air side,
  fuel side, load side.
* **Step 5** requires suspecting the instrument before the engine (calibrate
  indicator/transducer, check thermocouples, prove the flowmeter against tank
  soundings), repeating at steady state, and checking for a limiter or economy
  mode before declaring a fault.
* **Trap point** separates a slow ship from a sick engine, and warns that the
  **NOx Technical File** bounds what may be adjusted — going outside it
  invalidates the EIAPP certificate.

### Key numbers / regulation references

* **42,700 kJ/kg** — ISO reference LCV to which SFOC is corrected *(reused from
  the sibling card `QB5_J#q1`, already in the corpus)*
* **ISO 3046-1** standard reference conditions for correcting declared power
* **ISO 19030** — hull and propeller performance monitoring
* Formulae carried: `Pi = pmi × L × A × n`; `SFOC = fuel mass flow ÷ power`
  corrected to 42,700 kJ/kg; `apparent slip % = (engine distance − observed
  distance) ÷ engine distance × 100`, engine distance = pitch × revolutions
* **No universal threshold is asserted.** The Numbers deep-dive states in terms
  that deviation and alarm bands are the maker's and the ship's, and instructs
  the candidate to quote their own figures and say so if the examiner presses.

### Source / currentness basis

Reuse-first, per the evidence hierarchy. **ISO 3046-1 / 42,700 kJ/kg** and the
LCV correction are taken from the existing verified card `QB5_J#q1`.
**ISO 19030** is already carried in the corpus at `QB3_I` as the hull and
propeller performance monitoring standard. The **NOx Technical File** constraint
is carried across 17 files including `QB1_F` (12 mentions). Nothing in this card
rests on an external claim the corpus did not already hold.

### REG-BOX contents

| Code | Description |
|---|---|
| ISO 3046-1 / ISO 15550 | Reciprocating IC engine performance — declared power and correction to standard reference conditions |
| ISO 19030 | Measurement of changes in hull and propeller performance — separating hull fouling from engine deterioration |
| ISO 8217 | Marine fuel specification — net specific energy, viscosity, quality: the fuel-side variables normalised before blaming the engine |
| NOx Technical Code 2008 / Technical File | Bounds the components and settings that may be adjusted; outside them the EIAPP is invalidated |
| MARPOL Annex VI, Reg. 26 & 28 | SEEMP and CII — sustained deterioration shows in the annual carbon intensity |
| ISM Code, Element 10 | Maintenance of ship and equipment — inspection, non-conformity reporting, the PMS route |

### CE Oral Tip — full text

> **CE Oral Tip (Kochi MMD):** The examiner is testing your *method*, not your
> vocabulary. Do not open with a list of parameters — open with "against what
> baseline?" and give the sequence: baseline, normalise, read the engine's own
> parameters, localise, confirm. Say early that you would correct to ISO
> reference conditions and eliminate hull, weather and draught first, because
> that is the sentence that separates a Chief Engineer from a watchkeeper. The
> answer that fails is a confident recital of exhaust temperatures and scavenge
> pressures with nothing to compare them to.

### Examiner Chain evidence classification

**`PANEL_LEVEL_ONLY`.** The panel was Nair (external) and Srivastava (internal),
but the intake record supports no individual attribution. Accordingly the card
carries **no `data-examiner` attribute, no Examiner Chain deep-dive, and no
examiner name in the CE Oral Tip**. No relationship was minted.

### On My Vessel

Generic to a container vessel with a low-speed two-stroke: performance taken at
fixed load in steady weather, logged against shop/sea-trial curves, corrected to
ISO reference conditions and reference LCV; pressure cards at a fixed interval;
exhaust deviation reviewed with the second engineer before any unit is opened
up. **No company-specific Maersk procedure is asserted.**

### Syllabus mapping

`NO_CARD_YET_SO_NO_MAPPING` at adjudication. The governed mapper is **not
production-authorised** — the exporter reserves and deliberately leaves empty
`official_syllabus_version / official_syllabus_node_id / miw_topic_id /
miw_topic_name / objective_id`. This card therefore **closes no syllabus gap**
and changes no P0/P1/P2/P3 queue.

### Reviewer findings

Length recorded: **1,931 words**, about **p93** against a corpus median of 1,055
over 766 cards. No section duplicates another; the ask is a whole diagnostic
method. Flagged for GPT judgement, not silently trimmed.

---

# B. QB5_I#q8 — AUG-0268

| Field | Value |
|---|---|
| **Canonical ID** | `QB5_I#q8` |
| **File path** | `meoclass1/QB5_I.html` |
| **Local anchor** | `#q8` |
| **Triggering occurrence** | `AUG-0268` (submission `AUG2026-S027`, Snapshot 03, 31-Aug-2026 LPG carrier) |
| **Candidate's question, as reported** | "What does the Chief Engineer have to do with inventory? Leadership, lot of cross questions." |
| **Card question text** | "What does the Chief Engineer have to do with inventory — engine-room spares and stores? (Expect leadership cross-questions.)" |
| **Action ID** | `H6-002` |
| **Post-edit digest** | `4d3f86175f399f9db8951f9cb1cc2a7324c598900dbf55b8e83a73ff961c98bb` |
| **Commits** | `e910dd3`, refined at `031a0d6` |

### Why a new canonical root was required

* `\binventory\b` over **question text** → 1 hit, `QB3_D#q1`, rejected: that is
  the *Inventory of Hazardous Materials* (green passport, Hong Kong Convention)
  — a different sense of the word.
* `spare parts? (management|control|inventory)|stores management|inventory
  (control|management)` over **bodies** → 4 hits, every one an incidental
  mention inside another subject: `QB3_B#q14` (O2 analyser routine),
  `QB4_G#q5` (drydock failure mode), `QB5_C_B#q2` (SWOT illustration),
  `QB7_D#q1` (cryogenic LCO2 tank inventory, not stores).

### Placement rationale

`QB5_I.html` — "Management, Leadership & Human Element" — carries the broadest
tag set in the QB5 management family and already holds `QB5_I#q4`, *"CE as
leader vs manager"*, which the leadership limb chains to. `QB5_G` was rejected
as an undifferentiated "Additional Questions" file; `QB5_D` and `QB5_H`
duplicate the leader question rather than owning management systems. **No new QB
file was created.**

### 15-Second Answer — full text

> Inventory is not storekeeping — it is my control of the ship's ability to keep
> **critical machinery** running. The **ISM Code, element 10** requires the
> company to identify equipment whose sudden failure could create a hazardous
> situation, so the spares that support that equipment are a **safety-management
> obligation, not a purchasing convenience**. My job is to set the minimum
> stock, own the requisition and budget cycle, verify the record against the
> shelf, and hold the second engineer accountable for the system — **not to
> count every item myself**.

### 60-Second Answer — full text

> "Sir, I own four things. **First, what must be in stock.** The
> critical-equipment list under ISM 10.3 drives the critical-spares list; from
> that I set a minimum stock and a reorder point built on consumption rate and
> lead time for our trading pattern. **Second, that the record is true.** A
> planned-maintenance system that says a spare is on board when it is not is
> worse than no record at all, so I verify by physical stocktaking and sample
> checks, and I insist on part-number discipline on receipt. **Third, closing
> the loop with maintenance and budget.** Requisitions must be raised early
> enough that lead time is not an emergency, and I must be able to defend a
> critical item to the office on safety grounds rather than price. **Fourth —
> and this is the part you are really asking — I lead it rather than do it.**
> The second engineer owns the day-to-day record and the storekeeping
> discipline; each engineer owns the spares for his own machinery; I set the
> standard, verify by sampling, review it at the monthly maintenance meeting,
> and make the critical-spares status an explicit item in my handover. If a
> critical spare cannot be obtained, that is not a stores problem — I raise it
> as a non-conformity under ISM 9 and it goes on the record."

### Full answer — structure and summary

Sections: *Governing instrument* · *Where the spares list actually comes from* ·
*Setting the level — minimum stock and reorder point* · *The stock that has a
number attached to it* · *Keeping the record true — each discipline, and the
failure it prevents* · *The leadership limb — what the examiner is pressing* ·
*Trap point*. Deep-dives: CE Relevance, Trap Questions, Common CE Failures,
Numbers to Memorise, Casualty Link, On My Vessel.

* The load-bearing move is that **the critical-spares list is derived from the
  ISM 10.3 critical-equipment list**, not chosen as a personal opinion — which
  is the answer to the examiner's usual first cross-question, *"how do you
  decide what is critical?"*.
* **Reorder point = (average consumption rate × lead time) + safety stock**,
  with consumption taken from PMS job intervals, lead time from the trading
  pattern, and obsolescence treated as the opposite risk for older plant.
* **Prescribed stock** is separated from commercial judgement, because only the
  former carries a number an examiner can demand.
* The **leadership limb** is answered as *delegate with defined authority under
  ISM 3.2, create ownership, verify by sampling rather than counting, and be
  accountable upward* — with a refused critical spare escalated under **ISM 9**
  rather than absorbed silently.
* **Trap point** separates stores inventory from the **Inventory of Hazardous
  Materials** and tells the candidate to establish which is meant.

### Key numbers / regulation references

* **ISM 10.3** — critical equipment; **ISM 10.4** — stand-by arrangements to be
  tested; **ISM 9** — non-conformity reporting; **ISM 3.2 / 6.3** — authority and
  resources
* **SOLAS II-2, Reg. 10.3.3** — extinguisher spare charges: **100%** of the
  first **ten**, **50%** of the remainder, maximum **60**; where extinguishers
  cannot be recharged on board, additional extinguishers of the same type,
  capacity and number instead
* `Reorder point = (consumption × lead time) + safety stock`
* Explicitly stated: **minimum stock levels are ship- and company-specific** —
  quote your own vessel's figures, not a remembered number.

### Source / currentness basis

**ISM Code element 10 / critical equipment** is already carried across 26 files
in the corpus (e.g. `QB3_F`: *"because the separator is critical equipment under
ISM 10.3"*) — reused, not re-derived. **SOLAS II-2 Reg. 10.3.3** was the one
figure the corpus did **not** already hold, and it was verified externally
against two independent authoritative surfaces: a ClassNK statutory technical
circular and the Netherlands Regulatory Framework's SOLAS chapter II-2 host,
which independently confirm both the numbering and the 100 % / 50 % / max-60
rule. **⚑ GPT: this is the single claim in this batch newly imported from
outside the corpus. Please check it.**

### REG-BOX contents

| Code | Description |
|---|---|
| ISM Code 10.1 / 10.2 | Maintenance of ship and equipment — inspections, defect reporting, corrective action |
| ISM Code 10.3 | Identification of equipment whose sudden operational failure may result in hazardous situations — the source of the critical-spares list |
| ISM Code 10.4 | Measures to promote reliability, including regular testing of stand-by arrangements |
| ISM Code 3.2 / 6.3 | Defined responsibility and authority; the company's duty to provide adequate resources |
| ISM Code 9 | Reports and analysis of non-conformities — the route for a critical spare that cannot be obtained |
| SOLAS II-2, Reg. 10.3.3 | Extinguisher spare charges — 100 % of the first ten, 50 % of the remainder, max 60; additional extinguishers where recharging on board is not possible |
| Classification society rules | Spare parts for propulsion and essential auxiliaries, verifiable at survey |

### CE Oral Tip — full text

> **CE Oral Tip (Kochi MMD):** Get **ISM 10.3** into your first sentence. That
> single move converts a question that sounds like storekeeping into a
> safety-management answer and stops the panel treating you as a storekeeper.
> Then give the leadership limb in one line the examiner can hold on to — "I own
> the standard, the second engineer owns the record, I verify by sampling" — and
> be ready for the pivot to the Inventory of Hazardous Materials, which is a
> different subject entirely. The failing answer is a tour of requisition
> procedure with no regulation in it and no delegation.

### Examiner Chain evidence classification

**`PANEL_LEVEL_ONLY`** — as for `QB5_J#q2`. No `data-examiner` attribute, no
Examiner Chain, no name in the CE Oral Tip. No relationship minted.

### On My Vessel

Generic to a modern managed vessel: PMS with an integrated stores module,
critical equipment flagged, minimum stock and reorder points held against those
items, consumption booked against the maintenance job, ROB verified at a
periodic stocktake with the second engineer, critical-spares status carried in
the CE's handover notes. **No company-specific Maersk procedure is asserted.**

### Syllabus mapping

As for `QB5_J#q2` — `NO_CARD_YET_SO_NO_MAPPING`; the governed mapper is not
production-authorised, so this card closes no syllabus gap.

### Reviewer findings, and what changed

**One material finding, applied.** The card originally carried two near-mirror
sections — *"Keeping the record true"* (five disciplines) and *"Where inventory
actually fails"* (five failure modes) — whose items paired one-to-one: location
discipline against "cannot be located", receipt part-number discipline against
"wrong or superseded part", preservation against "degraded", issue discipline
against "never booked out". That is duplication, not depth. They are now a
single section stating **each discipline with the failure it prevents**, and the
one genuinely unique failure — *a critical spare consumed on a non-critical job*
— is retained and attached to the verification item, the only control that
catches it. The manifest pin was refreshed to the reviewed state and the
reasoning recorded in `review_round_note` (commit `031a0d6`).

Length recorded: **2,183 words**, about **p96**. The ask is compound — the
candidate reported "leadership, lot of cross questions" — and after the merge no
section duplicates another.

---

# C. QB1_D#q7 — CE Oral Tip added (H5C-RES-01)

| Field | Value |
|---|---|
| **Canonical ID** | `QB1_D#q7` |
| **File path** | `meoclass1/QB1_D.html` |
| **Question** | "What is a Bonjean curve, and where would you actually use one?" |
| **Correction ID** | `CORR-CETIP-QB1D-Q7-20260902` |
| **Pre-edit digest** | `27c4ee371d3b5dc2fa2d2673403844bb9b3ed24201e36a990e09f764f746be85` |
| **Post-edit digest** | `f337a4d59d3ca5a6dfc97e567e3f39007eda92c709382e3ebf7779b28b50a5ff` |
| **Commit** | `9a65d7c` |

### Old state

The card carried a `reg-box` and a `q-footer` but **no `ce-tip`**. It was the
fourth and last such instance in the corpus and the only **numeric** card
without one. It predates the H series and already ships in published
`origin/main`, which is why it fell outside the three cards the H5 ruling named
and was registered instead as closure residue **H5C-RES-01** (severity MINOR,
owner "Oral content production"). The product contract requires it independently
of that ruling: `qb_health_check`'s `MANDATORY_CLASSES` requires exactly one
reg-box, one ce-tip and one q-footer per numeric card.

### New CE Oral Tip — full text

> **CE Oral Tip (Kochi MMD):** Lead with the limitation, not the definition —
> the hydrostatic tables assume even keel, and the moment the waterline is
> inclined they stop being valid. Only then say what the curve plots: immersed
> sectional area against draught, one curve per station. Name where you would
> reach for it — longitudinal strength, launching, grounding and flooded
> conditions. Two things sink candidates here: describing the curve without ever
> saying what it is plotted against, and stopping before Simpson's Rules. Let
> the examiner ask for the arithmetic.

**89 words**, against a corpus median of 67 and p75 of 84 across 762 ce-tip
blocks — deliberately shorter than the three H3B-1 tips, which sat at ~p92 and
were recorded as observation H5C-RES-03.

### Confirmation that no other answer content changed

* Question text, anchor and card position: **unchanged**.
* Only bytes moved: the inserted `ce-tip` block and the version badge
  `QB1_D · Q7 · v1.0 → v1.1`.
* Every other card in `QB1_D.html` is byte-identical — `q1`–`q6` digests match
  batch D's `baseline_card_digests` exactly.
* The tip asserts **no instrument, date or figure the card does not already
  carry**: the even-keel limitation, immersed sectional area against draught per
  station, the four use cases and Simpson's Rules are all in the card body.

### Examiner-index delta

**Zero.** The tip uses the corpus-standard non-attributing label
`CE Oral Tip (Kochi MMD):`, already carried by 58 live cards across ten files.
The examiner index is built from committed evidence records and from
`data-examiner` attributes on q-cards, neither of which this edit touches.
Before and after: **958 relationships / 7 examiners**, tiers identical
(confirmed 459 / reported 44 / ce_tip 214 / header 30 / inferred 211).

### Governance

`CORR-CETIP-QB1D-Q7-20260902`, manifest audit **20/20 PASS**;
`validate_corrections.py` **161 checks, 0 FAIL**.

**No supersession chain is declared, and that is a finding rather than an
omission.** `QB1_D#q7` was created by batch D as `PROMNEW-004` (family
GAP-0231). `batch_d_manifest.json` is a generation-1 record carrying only
`baseline_card_digests` — **pre**-edit pins — and its `QB1_D` pins cover `q1`
through `q6`, the cards that existed *before* batch D appended `q7`. So `q7` has
never been pinned by any manifest and there is no earlier post-edit state for
this correction to descend from.

---

# D. ANNEX — the three asks that already have canonical answers

**⚑ This annex is the part of the packet where GPT is being asked to audit a
closure rather than a creation.** If any of these three is judged insufficient,
that is a bounded correction to the named existing card — not a new root.

---

## D.1 AUG-0095 — "Freedom of navigation"

| Field | Value |
|---|---|
| **Occurrence** | `AUG-0095` (+ limb `AUG-0096`), submission `AUG2026-S009`, 27-Aug-2026 |
| **Exact reported question** | "Freedom of navigation." — and, as a follow-up limb, "condition of freedom of navigation" |
| **Existing canonical card** | **`QB1_A#q19`** — "UNCLOS — Under which provision does your ship sail? EEZ and Continental Shelf explained." |
| **Governing disposition** | `production_outcomes.H3A.already_answered_no_card_written` + correction `CORR-UNCLOS-FREEDOM-20260831` (known_traps entry 56) |

**Live-card extracts (verbatim from `QB1_A#q19`):**

> "Foreign ships retain freedom of navigation and overflight (Art. 58) exactly
> as on the high seas, subject only to those specific coastal-state rights. The
> condition on that freedom is Art. 58(3): a State exercising these freedoms
> 'shall have due regard to the rights and duties of the coastal State and shall
> comply with the laws and regulations adopted by the coastal State'…"

> "Art. 87 guarantees freedom of navigation, overflight, fishing, laying
> cables/pipelines, and scientific research to every state — and Art. 87(2)
> attaches the same condition here… **Due regard is therefore the condition in
> BOTH zones — Art. 58(3) in the EEZ, Art. 87(2) on the high seas — and that
> pairing is the complete answer to 'what are the conditions of freedom of
> navigation?'**"

> "…in port, full port/flag state jurisdiction; 0–12 nm, innocent passage
> (Art. 17–32); 12–200 nm EEZ, freedom of navigation under Art. 58 but exposed
> to MARPOL enforcement under Art. 220; through a strait, the stronger transit
> passage regime; beyond 200 nm, freedom of navigation under Art. 87 with
> exclusive flag-state jurisdiction under Art. 90–92."

**Why the card is sufficient.** The brief asked for freedom of navigation
located within the UNCLOS zones, its conditions, the coastal-State definition
and limits, and the distinction from innocent passage. The card carries all four
— internal waters, territorial sea, contiguous zone, EEZ, continental shelf and
high seas, each with the coastal State's powers and their limits; the "due
regard" condition in both zones with the article numbers; and an explicit
examiner trap on EEZ sovereignty.

**What superseded the intake classification.** The H3A outcome records the split
explicitly: the **root** was already answered; the **limb** (the "condition")
was genuinely missing — a sweep of all 86 question-bearing files returned **zero
occurrences of "due regard"** — and was fixed by a bounded correction to `q19`
under `CORR-UNCLOS-FREEDOM-20260831` with trap 56, *"not by a new card, because
the limb belongs inside the zones card."* Creating a standalone
freedom-of-navigation root now would duplicate `q19` **and contradict a
correction that has already shipped to answer that exact limb.**

---

## D.2 AUG-0140 — "Where to find crew entitlement onboard"

| Field | Value |
|---|---|
| **Occurrence** | `AUG-0140`, submission `AUG2026-S014`, 27-Aug-2026 |
| **Exact reported question** | "Where to find crew entitlement onboard." |
| **Existing canonical card** | **`QB9_H#q10`** — "What is the Articles of Agreement?" |
| **Governing disposition** | `production_outcomes.H3A` — *"CORRECTED AFTER REVIEW … EXISTING_CARD_SUFFICIENT stands; the destination changed."* |

**Live-card extract (verbatim from `QB9_H#q10`):**

> "MLC 2006 rebuilt this individually — **Std A2.1** requires a SEA signed by the
> seafarer and the shipowner or shipowner's representative, examined before
> signing with advice available, **an original for each party, a copy (with any
> CBA incorporated) carried onboard and available to PSC in English**, and a
> record of employment (no conduct/wage remarks) on discharge — plus **Std A2.2
> wage accounts**. India retains the Shipping Master institution and
> agreement/engagement machinery within the Merchant Shipping Act framework,
> aligned to MLC since ratification…"

**Why the card is sufficient.** The ask is *where* a seafarer's entitlements are
recorded and consulted onboard. The card answers exactly that: the individual
SEA, examined before signing, with an original for each party and a copy —
**with any applicable CBA incorporated** — carried onboard and available to PSC
in English; plus Std A2.2 wage accounts and the record of employment. It also
distinguishes the historical Articles of Agreement from the modern SEA and
carries the Indian statutory position.

**What superseded the intake classification.** Independent review moved the
destination. The batch first named `QB4_A#q14`, which explains DMLC Part I
(national law) and Part II (company procedure) — *"neither of which is the
seafarer's own document, as that card itself concedes."* The disposition
`EXISTING_CARD_SUFFICIENT` stood; only the target changed, to `QB9_H#q10`.

**⚑ Open question for GPT:** the card carries an explicit in-product hold —
`[cite the 2025 Act…]` / `[2025 Act — Part-level, sections pending
verification]` — on the Indian Merchant Shipping Act section numbers. That hold
is declared to the candidate and is **not** closed by this batch.

---

## D.3 AUG-0148 — "What is the Grain Loading Booklet?"

| Field | Value |
|---|---|
| **Occurrence** | `AUG-0148`, submission `AUG2026-S015`, 28-Aug-2026 |
| **Exact reported question** | "What is grain loading booklet" |
| **Existing canonical card** | **`QB2_A#q11`** — "Grain Code — intact stability criteria, grain heeling moment mechanism, and Document of Authorisation." |
| **Governing disposition** | `production_outcomes.H3A` — `EXISTING_CARD_SUFFICIENT`, with the card corrected on 31 Aug by H2 (`CORR-GRAIN-MSC552-20260831`, trap 55) |

**Live-card extract (verbatim from `QB2_A#q11`):**

> "**Accompanying Stability Booklet:** The DoA is **invalid unless accompanied by
> an approved Grain Stability Booklet**. This booklet provides the Master with
> pre-calculated volumetric heeling moments for every hold. Since 1 January 2026
> there are **three** compartment configurations, not two: 'filled', 'partly
> filled', and the category added by resolution **MSC.552(108)** — 'specially
> suitable compartment, partly filled in way of the hatch opening, with ends
> untrimmed'. A booklet that predates the amendment will not carry the third
> condition, and **the ship cannot be loaded to a condition its approved booklet
> does not cover.**"

> "**Document of Authorisation (DoA) — Definition & Issuance:** A statutory
> certificate issued by the Flag Administration or a recognized Class Society
> acting on its behalf. It serves as legal proof that the vessel is capable of
> complying with the International Grain Code."

**Why the card is sufficient.** The brief asked for the governing grain regime,
the booklet's purpose, who approves it, its contents, the stability/grain-heeling
information, operational use, the relationship to the Document of Authorization,
and Master/ship responsibilities. The card carries the regime (SOLAS Chapter VI /
International Grain Code), the booklet's purpose and contents (pre-calculated
volumetric heeling moments per hold), the approval authority (Flag or RO acting
on its behalf, via the DoA), the DoA relationship stated as a validity condition,
the current three-configuration position after MSC.552(108), and the operational
consequence.

**Recorded limitation, carried forward.** The H3A outcome records a terminology
limitation: **the Grain Code's own naming of the document** — booklet, manual, or
Document of Authorization — could not be verified from the sources held at the
time. That limitation is unchanged by this batch.

---

# E. What is deliberately NOT in this batch

The following were identified as useful but non-blocking and are **preserved as
post-release production items, untouched**. All four verified byte-identical to
`191441f`:

| Item | Card | Digest (unchanged) |
|---|---|---|
| "downtime clause" vocabulary | `QB9_B#q4` | `772dae08541f96d6…` |
| class vs statutory certificate extension limb | `QB4_H#q10` | `83a150beb65226b7…` |
| optional incinerator standard-specification circular | `QB3_C#q7` | `ac449506e9507522…` |
| title should name chemical/IBC scope more clearly | `QB1_G#q34` | `aa3956897e67891a…` |

Also registered and **not** actioned: the two Snapshot-03 limb-level expansion
candidates — the incinerator type-approval circular number (`AUG-0265`) and
class-versus-statutory certificate extension (`AUG-0267`).

---

# F. Compact review table

| ID | Question | Key regulation / source | Main trap | Commit |
|---|---|---|---|---|
| `QB5_J#q2` | As CE, how will you decide the main engine is not performing well? | ISO 3046-1 (reference conditions, LCV 42,700 kJ/kg) · ISO 19030 · NOx Technical File | A slow ship is not a sick engine — and an engine on its limiter is protected, not defective | `e910dd3` |
| `QB5_I#q8` | What does the CE have to do with inventory — spares and stores? | ISM 10.3 / 10.4 / 9 / 3.2 · SOLAS II-2 Reg. 10.3.3 | "Inventory" in a recycling context means the IHM — a different subject | `e910dd3`, `031a0d6` |
| `QB1_D#q7` | What is a Bonjean curve, and where would you use one? | *(CE tip only — card unchanged)* | Describing the curve without saying what it is plotted against; stopping before Simpson's Rules | `9a65d7c` |

---

# G. Verification state at the time of this packet

| Gate | Result |
|---|---|
| `oral_manifest` audit — batch H6 | 12 checks, 0 FAIL |
| `oral_manifest` audit — correction | 20 checks, 0 FAIL |
| `validate_batch_h_series` | 154 checks, 0 FAIL |
| `validate_corrections` | 161 checks, 0 FAIL |
| `validate_qb_content_index` | 24 checks, 0 FAIL |
| `validate_examiner_index` | 54 PASS / 0 FAIL |
| `validate_oral_intake` | 32 PASS / 0 FAIL |
| `test_oral_release_infra` | 104 checks, 0 FAIL |
| `test_oral_release_runner` | 123 checks, 0 FAIL |
| `mutate_batch_h_series` | 11 caught of 11, 0 escapes, 0 no-ops |
| H6 pin non-vacuity probe | corrupting `H6-001` fails `manifest_digest_matches` (PIN_MISMATCH); restore returns 154/0 |
| Workbook validators × 3 | all PASS, 761 rows each |
| `test_question_bank_xlsx` | 32 checks, 0 failed |
| `qb_health_check` vs `191441f` | **NEW = 0**, GONE = 1 (`QB1_D q7: missing ce-tip`) |

---

*Prepared for GPT content review. No push, no deploy, no publication, no
workbook distribution until the Founder gives authority.*


---
---

# GPT CONTENT REVIEW CORRECTIONS

*Addendum, 2 September 2026. This section SUPERSEDES every statement earlier in
this packet about the wording of `QB5_I#q8`, `QB2_A#q11`/`#q33` and
`QB9_H#q10`. The rest of the packet stands. The two-card H6 production scope was
NOT reopened: no card was created, no card was deleted, the corpus is unmoved at
761, and examiner relationships are unmoved at 958 across 7 examiners.*

Three bounded content items were raised by GPT's review of this packet and of
`AUGUST2026_H6_QUALIFICATION.json`. All three are resolved. The scope pass that
each one triggered found three further instances the review did not name, and
those are declared here rather than shipped silently.

| # | Card | Problem | Correction id | Supersedes |
|---|---|---|---|---|
| A | `QB5_I#q8` | ISM 10.3 / ISM 9 overstated; 10.3's limbs mis-filed under 10.4 | `CORR-ISM-SPARES-20260902` | `batch_h6_manifest.json` / `H6-002` |
| B | `QB2_A#q11` | DoA declared "invalid" without the booklet; Code terminology unverified | `CORR-GRAIN-TERMINOLOGY-20260902` | `correction_corr_grain_msc552_20260831_manifest.json` / `CORR-GRAIN-01` |
| B' | `QB2_A#q33` | same proposition, sibling card, found by the scope pass | `CORR-GRAIN-TERMINOLOGY-20260902` | `batch_h2_manifest.json` / `H2-002` |
| C | `QB9_H#q10` | five candidate-visible editorial placeholders | `CORR-MSACT-SEA-20260902` | none — the card was pinned by no manifest |

Baseline commit `d0a188f`; governing commit `897555c`.

---

## A. `QB5_I#q8` — ISM Code 10.3 and ISM 9

### A.1 The exact overstatement found

Four propositions, none supported by the Code:

1. *"The critical-equipment list under ISM 10.3 **drives** the critical-spares list"* — 60-second answer.
2. *"the critical-spares list **is derived from** the critical-equipment list, and that list comes out of ISM 10.3"* — body, and repeated in the cheat-sheet memory card, a self-test row and the trap-questions deep-dive.
3. ISM 10.3 standing behind *"a minimum stock and a reorder point"* — 15-second and 60-second answers.
4. *"If a critical spare cannot be obtained ... **I raise it as a non-conformity under ISM 9** and it goes on the record"* — 60-second answer, repeated in the leadership limb, two deep-dives, the reg-box and the cheat sheet.

**A fifth defect the review did not name, found by the scope pass.** ISM 10.3's
second and third limbs — the SMS reliability measures and the regular testing of
stand-by arrangements — were attributed to **10.4** in the Governing-instrument
paragraph, the reg-box, the stand-by bullet, the Casualty-Link deep-dive and the
cheat-sheet memory card. 10.4's actual content appeared nowhere on the card.

### A.2 The corrected interpretation

**ISM 10.3**, verbatim, as amended by MSC.273(85) item 7:

> The Company should identify equipment and technical systems the sudden operational failure of which may result in hazardous situations. The SMS should provide for specific measures aimed at promoting the reliability of such equipment or systems. These measures should include the regular testing of stand-by arrangements and equipment or technical systems that are not in continuous use.

It does **not** prescribe a statutory critical-spares list, a universal minimum
stock, a reorder point, or automatic ISM 9 consequences.

**ISM 10.4**, verbatim:

> The inspections mentioned in 10.2 as well as the measures referred to 10.3 should be integrated in the ship's operational maintenance routine.

**ISM 9** is the reporting and analysis route for non-conformities, accidents
and hazardous occurrences (9.1), with corrective action including measures
intended to prevent recurrence (9.2, as amended by MSC.273(85) item 6). Whether
an unobtainable spare produces a non-conformity is answered by **ISM 1.1.9** —
*"an observed situation where objective evidence indicates the non-fulfilment of
a specified requirement"* — not by the fact that procurement failed.

**The hierarchy the card now teaches:** ISM 10.3 identifies reliability-critical
equipment → the company's SMS and PMS translate that risk into maintenance,
testing and, where appropriate, spare-parts control → the CE manages stock
accordingly. The list is *informed by* 10.3 and built from maker recommendations,
class and statutory requirements where applicable, PMS maintenance scope, failure
consequence and risk, redundancy, lead time, consumption, trading pattern and the
company's SMS and procurement rules.

**Sources read:** `A.741(18)`, `MSC.104(73)`, `MSC.195(80)`, `MSC.273(85)`,
`MSC.353(92)` and `A.1184(33)`, all held locally with full text layers. Only
MSC.273(85) touches sections 9 or 10. Registered as `SRC-ISMCODE-CONSOLIDATED`.

### A.3 Old wording → new wording

| Where | Old | New |
|---|---|---|
| 15-sec | "The **ISM Code, element 10** requires the company to identify equipment whose sudden failure could create a hazardous situation, so the spares that support that equipment are a **safety-management obligation, not a purchasing convenience**." | "The **ISM Code, element 10.3** requires the company to identify equipment whose sudden operational failure may result in a hazardous situation and to provide specific measures promoting its reliability, so the spares that keep that equipment reliable sit inside the **safety-management system, not in purchasing convenience**." |
| 60-sec, limb 1 | "The critical-equipment list under ISM 10.3 drives the critical-spares list; from that I set a minimum stock and a reorder point..." | "ISM 10.3 makes the company identify the equipment whose sudden failure could be hazardous and provide measures to keep it reliable; the company's SMS and PMS then translate that risk into maintenance, testing and, where the company requires it, spare-parts control. From that I set a minimum stock and a reorder point..." |
| 60-sec, close | "If a critical spare cannot be obtained, that is not a stores problem — I raise it as a non-conformity under ISM 9 and it goes on the record." | "If a safety-critical spare cannot be obtained, that is not a stores problem: I assess it against the SMS and the critical-equipment requirements, weigh redundancy and operational risk, escalate it to the company, and impose an operational limitation or a repair plan — and where the resulting condition meets the company's own definition of a non-conformity, it is reported and analysed under ISM 9 rather than absorbed." |
| Body heading | "Where the spares list actually comes from" | "How the critical-spares list is actually built" |
| Governing instrument | "**10.3** requires identification ...; **10.4** requires measures to promote reliability of that equipment, including regular testing of stand-by arrangements." | "**10.3** requires the Company to identify ..., and requires the SMS to provide *specific measures aimed at promoting the reliability* ... including the *regular testing of stand-by arrangements* ...; **10.4** requires those measures, and the 10.2 inspections, to be integrated into the ship's operational maintenance routine." |
| Stand-by bullet | "ISM 10.4 also brings in what must be *proved* to work" | "ISM 10.3's third limb requires the *regular testing of stand-by arrangements ...*, and 10.4 puts that testing into the operational maintenance routine" |
| Casualty deep-dive | "That is precisely the failure ISM 10.4 is written to prevent" | "That is precisely the failure ISM 10.3 is written to prevent: it is 10.3 that names the regular testing ... and 10.4 that puts those measures into the ship's operational maintenance routine" |
| Reorder point | (formula alone) | formula + "*None of this arithmetic is prescribed by the ISM Code.* ISM 10.3 requires reliability measures; the minimum stock, the reorder point and the safety stock are how a company's SMS, PMS and procurement rules deliver them" |
| Cheat-sheet flow | "ISM 10.3 Critical equipment → drives → Critical spares list" | "ISM 10.3 Critical equipment → SMS / PMS reliability measures → Critical spares control" |
| Cheat-sheet memcard | "the critical-spares list is DERIVED from the critical-equipment list ... Refused critical spare → ISM 9 non-conformity" | rewritten to the identify → translate → manage hierarchy, with ISM 9 conditional |

### A.4 Corrected 15-Second Answer — full text

> Inventory is not storekeeping — it is my control of the ship's ability to keep
> **critical machinery** running. The **ISM Code, element 10.3** requires the
> company to identify equipment whose sudden operational failure may result in a
> hazardous situation and to provide specific measures promoting its reliability,
> so the spares that keep that equipment reliable sit inside the
> **safety-management system, not in purchasing convenience**. My job is to set
> the minimum stock, own the requisition and budget cycle, verify the record
> against the shelf, and hold the second engineer accountable for the system —
> **not to count every item myself**.

### A.5 Corrected 60-Second Answer — full text

> "Sir, I own four things. **First, what must be in stock.** ISM 10.3 makes the
> company identify the equipment whose sudden failure could be hazardous and
> provide measures to keep it reliable; the company's SMS and PMS then translate
> that risk into maintenance, testing and, where the company requires it,
> spare-parts control. From that I set a minimum stock and a reorder point built
> on consumption rate and lead time for our trading pattern. **Second, that the
> record is true.** A planned-maintenance system that says a spare is on board
> when it is not is worse than no record at all, so I verify by physical
> stocktaking and sample checks, and I insist on part-number discipline on
> receipt. **Third, closing the loop with maintenance and budget.** Requisitions
> must be raised early enough that lead time is not an emergency, and I must be
> able to defend a critical item to the office on safety grounds rather than
> price. **Fourth — and this is the part you are really asking — I lead it rather
> than do it.** The second engineer owns the day-to-day record and the
> storekeeping discipline; each engineer owns the spares for his own machinery; I
> set the standard, verify by sampling, review it at the monthly maintenance
> meeting, and make the critical-spares status an explicit item in my handover.
> If a safety-critical spare cannot be obtained, that is not a stores problem: I
> assess it against the SMS and the critical-equipment requirements, weigh
> redundancy and operational risk, escalate it to the company, and impose an
> operational limitation or a repair plan — and where the resulting condition
> meets the company's own definition of a non-conformity, it is reported and
> analysed under ISM 9 rather than absorbed."

### A.6 Corrected REG-BOX

| Code | Description |
|---|---|
| ISM Code 10.1 / 10.2 | Maintenance of the ship and equipment — inspections, defect reporting and corrective action within the SMS *(unchanged)* |
| **ISM Code 10.3** | **Identification of equipment and technical systems whose sudden operational failure may result in hazardous situations, and SMS measures aimed at promoting their reliability, including the regular testing of stand-by arrangements and equipment not in continuous use** |
| **ISM Code 10.4** | **Integration of the 10.2 inspections and the 10.3 reliability measures into the ship's operational maintenance routine** |
| ISM Code 3.2 / 6.3 | Defined responsibility and authority, and the company's duty to provide adequate resources *(unchanged)* |
| **ISM Code 9** | **Reports and analysis of non-conformities, accidents and hazardous occurrences — the route where an unobtainable critical spare produces a condition meeting the SMS's definition of a non-conformity** |
| SOLAS II-2, Reg. 10.3.3 | Spare charges for portable fire extinguishers — 100% of the first ten, 50% of the remainder, maximum 60; additional extinguishers where recharging on board is not possible *(unchanged)* |
| Classification society rules | Spare parts to be carried for propulsion and essential auxiliary machinery, verifiable at survey *(unchanged)* |

### A.7 CE Oral Tip — UNCHANGED

The tip tells the candidate to get **ISM 10.3** into the first sentence, then to
give the leadership limb in one line and to expect the pivot to the Inventory of
Hazardous Materials. It carried no overstatement and is not reproduced here
because it did not change.

### A.8 SOLAS II-2 Reg. 10.3.3 — independently re-verified, RETAINED

GPT's independent confirmation is upheld and the claim stays on the card
unchanged. Verification basis, stated with its limit:

* **The consolidated SOLAS chapter II-2 base text is NOT held** in the local
  primary-source corpus — only amendment resolutions are. The rule is therefore
  carried on concordant reproductions by competent authorities, not on the
  instrument's own bytes, and **no sub-paragraph structure below 10.3.3 is
  asserted to the candidate**.
* **Barbados Maritime Ship Registry, Bulletin 012 §§14.12–14.13** (flag
  administration): 100% for the first ten, 50% of the remaining up to a maximum
  of sixty; additional extinguishers of the same type and capacity in lieu where
  recharging on board is not possible.
* **Netherlands Regulatory Framework (NeRF) Maritime**, SOLAS chapter II-2, and
  National Cargo Bureau grain/fire material return the same rule against
  II-2/10.3.3.
* **Currency, asked publisher-anchored** (SKILL.md §8.2b): the two reg-10
  amendment resolutions held locally — `MSC.520(106)` and `MSC.550(108)` — were
  opened and **neither touches 10.3.3**. The most recent publicised change to
  regulation 10 is the new PFOS paragraph in force 1 January 2026, which does not
  touch spare charges.
* Registered as `SRC-SOLAS-II2-REG10-SPARECHARGES`, `ACCESS_LIMITED`,
  `CURRENT_VERIFIED`.

### A.9 Digest / correction / governance

| | |
|---|---|
| Pre-edit digest | `4d3f86175f399f9db8951f9cb1cc2a7324c598900dbf55b8e83a73ff961c98bb` |
| Post-edit digest | `b4e93098e30e27aa7c6ee70bfb928dcb233a4cace562a2ab5966ea9804cb8db3` |
| Correction id | `CORR-ISM-SPARES-20260902`, action `CORR-ISM-01`, `PRIMARY_CORRECTION` |
| Supersedes | `batch_h6_manifest.json` / `H6-002`, whose pinned post-state `4d3f86…` is the chain root |
| Convention | full `sha256` over the balanced card block, LF-normalised — same throughout the chain |

**H6's manifest is not rewritten.** Its pin, its `topic` field and its note still
record what H6 shipped, including the wording corrected here. `validate_batch_h_series`
keeps its claim and that claim becomes strictly stronger: not *"my state is
live"* but *"my state is the ancestor of what is live"*. The page cheat sheet
carries no `q-card` and is pinned by no guard, so it is recorded in the
correction's `artefacts[]` rather than given a digest.

---

## B. `QB2_A#q11` and `#q33` — the Grain Code

### B.1 Old terminology

> "**Accompanying Stability Booklet:** The DoA is **invalid unless accompanied by
> an approved Grain Stability Booklet**. This booklet provides the Master with
> pre-calculated volumetric heeling moments for every hold."

*"Grain Stability Booklet"* is not the Code's term, and *"invalid"* is not the
Code's legal effect. The H6 packet recorded the naming as an open limitation.

### B.2 Official Grain Code terminology — verbatim

| Section | Text |
|---|---|
| **A 3.1** | "A document of authorization shall be issued for every ship loaded in accordance with the regulations of this Code either by the Administration or an organization recognized by it or by a Contracting Government on behalf of the Administration. It shall be accepted as evidence that the ship is capable of complying with the requirements of these regulations." |
| **A 3.2** | "The document shall accompany or be incorporated into the grain loading manual provided to enable the master to meet the requirements of A 7. The manual shall meet the requirements of A 6.3." |
| **A 3.5** | "A ship without such a document of authorization shall not load grain until the master demonstrates to the satisfaction of the Administration, or of the Contracting Government of the port of loading acting on behalf of the Administration, that, in its loaded condition for the intended voyage, the ship complies with the requirements of this Code." |
| **A 6.1** | "Information in printed booklet form shall be provided to enable the master to ensure that the ship complies with this Code when carrying grain in bulk on an international voyage. This information shall include that which is listed in A 6.2 and A 6.3." |

**Four terms, four jobs.** *Grain loading manual* is the Code's own term for the
document (A 3.2, A 6.3). *Printed booklet form* is the required **format** of the
information (A 6.1). *Grain loading booklet* is common and examiner shorthand —
acceptable descriptive wording, but it does not replace the formal term where
precision matters. *Document of Authorization* is separate authorisation
evidence (A 3.1) that accompanies, or may be incorporated into, the manual.

### B.3 Final wording — `#q11`, the corrected paragraph

> **Relationship to the grain loading manual:** The Code does not make the DoA
> "invalid" on its own terms. Under Grain Code **A 3.2** the document *"shall
> accompany or be incorporated into the grain loading manual"* provided to enable
> the master to meet the requirements of A 7, and that manual must meet A 6.3.
> Under **A 6.1** the stability and grain-loading information is to be provided
> *"in printed booklet form"* — which is why examiners and crews say *grain
> loading booklet*, while **grain loading manual** is the Code's own term for the
> document and **printed booklet form** is its required format. The manual
> provides the Master with pre-calculated volumetric heeling moments for every
> hold. **Since 1 January 2026 there are three compartment configurations, not
> two**: "filled", "partly filled", and the category added by **resolution
> MSC.552(108)** — "specially suitable compartment, partly filled in way of the
> hatch opening, with ends untrimmed". A booklet that predates the amendment will
> not carry the third condition, and the ship cannot be loaded to a condition its
> approved booklet does not cover. See Q33.

Two further `#q11` limbs were re-based on the Code's own words: **Definition &
Issuance** now quotes A 3.1's *"shall be accepted as evidence that the ship is
capable of complying"*; **Carriage Without a DoA** now states A 3.5's actual
mechanism. The trap-questions deep-dive answer, which had said a ship without the
DoA "will be detained by Port State Control, unless an explicit emergency
dispensation is issued by the flag administration", now gives A 3.5's route
instead. Two new reg-box rows name A 3.1/A 3.2 and A 6.1/A 3.5.

### B.4 Final wording — `#q33`, the scope-pass repair

`#q33` carried the same proposition. It was already right about one thing —
that the grain-manual update requirement is class and P&I guidance and **not** in
the text of MSC.552(108) — and that distinction is preserved. Corrected clause:

> ... the ship can only load to a condition its approved booklet actually covers.
> Say it precisely: the Code does not declare the **Document of Authorisation**
> "invalid" without the booklet — under **A 3.2** the document *shall accompany
> or be incorporated into the grain loading manual*, and under **A 3.5** a ship
> without the document shall not load grain until the master demonstrates
> compliance. And the requirement to update the manual for the new option is
> **class-society and P&I practical guidance**; it is **not** in the text of
> MSC.552(108).

### B.5 Terminology limitation — **CLOSED: YES**

The H6 packet's open limitation was that the Code's own naming of
booklet / manual / Document of Authorization was unverified. It is now verified
verbatim at A 3.1, A 3.2, A 3.5 and A 6.1 and the four terms are separated on
the card and in `CORR-GRAIN-TERMINOLOGY-20260902`. `"Grain Stability Booklet"`
now returns **zero** occurrences corpus-wide.

**Source and its limit, stated.** The IMO base publication is **not held** —
that gap is already `RQ-G01` against `SRC-GRAINCODE-MSC552-2026` and is **not**
closed by this pass. The wording was read from a West of England P&I **verbatim**
reproduction of Part A, corroborated against IMO's own Grain Code page. Registered
as `SRC-GRAINCODE-PARTA-TEXT`, tier 2, **`CURRENTNESS_UNVERIFIED`** — deliberately
not `CURRENT_VERIFIED`, because a tier-2 reproduction cannot establish that Part A
has not been amended by something this corpus has not seen. The MSC.552(108)
content is unchanged and was re-read against `SRC-GRAINCODE-MSC552-2026` first.

### B.6 Digests / correction / supersession

| Card | Pre-edit | Post-edit | Class | Supersedes |
|---|---|---|---|---|
| `#q11` | `1db21b35c562e271be86ce03cb55526a247243285453abe542d88d1ddf8b69f1` | `44a592d6af94e47d68a113e03ecae0a8273be66825c9fb0347e62dc23aee1c3c` | `PRIMARY_CORRECTION` | `correction_corr_grain_msc552_20260831_manifest.json` / `CORR-GRAIN-01` |
| `#q33` | `84050473a1949132857a24dced9787910ce6866b762b08578f081a51a53180de` | `9dcfa3aead962dded1989ce38a5105996f84aefa09aa5acde6c6421b600a30a7` | `SCOPE_PASS_CORRECTION` | `batch_h2_manifest.json` / `H2-002` |

`CORR-GRAIN-MSC552-20260831` is **not** rewritten — it owned the previous
post-state of `#q11`, and the new record descends from it. `validate_corrections`
reports that predecessor `PASS live_matches_authorised_post_state` through the
resolved chain.

---

## C. `QB9_H#q10` — the candidate-visible placeholders

### C.1 Placeholders found — five, all inside the `#q10` card block

| Where | Text |
|---|---|
| 15-Second Answer | `[2025 Act — Part-level, sections pending verification]` |
| 60-Second Answer | `[cite the 2025 Act at Part level; the 1958 sections must not be quoted as current]` |
| Governing instrument | `[Part-level, sections pending verification]` |
| Key Numbers | "current statute; sections pending verification" |
| REG-BOX | "Part-level, sections pending verification" |

### C.2 Outcome — **A, not B**

The hold behind the placeholders was real and recorded: `SRC-MSACT-2025` listed
*"Section numbers outside s.4 and s.5"* under `claims_NOT_established`, with the
instruction *"Obtain [the 30 September 2025 corrigenda] before quoting any
section verbatim beyond s.4."*

**The corrigenda was retrieved rather than the wording softened.** Fetched by
direct HTTPS GET from DGMA's own endpoint (HTTP 200, no workaround),
sha256 `4a28b152426b0cd709be37a4bc0c176be059f56eed97566fe96ed0b1bedcf818`,
273,992 bytes. It makes **exactly three corrections, all typographical, with no
renumbering**: page 33 line 19 "matter"→"matters"; page 69 line 24 "himself
such"→"himself of such"; page 71 line 12 "sea borne"→"seaborne". The hold is
therefore discharged **on evidence, not waived**, and Part V was read directly
from the Act's own text layer (`SRC-MSACT-2025`, sha256 `6fb38616…`, DGMA's own
copy of the Gazette text). Registered as `SRC-MSACT-2025-CORRIGENDA`.

### C.3 Verified statutory references now on the card

| Section | Content |
|---|---|
| **s.63(1)** | Master, owner or recruitment-and-placement agency shall enter into a seafarers' employment agreement in the prescribed form with every seafarer engaged, and submit a copy to the shipping master |
| **s.63(3)** | The seafarer shall, before signing, be given an opportunity to examine and seek advice on the agreement |
| **s.64** | Payment at intervals not later than monthly, with a monthly account of sums due and paid |
| **s.83(1)** | A dispute arising under the agreement goes to the shipping master |
| **s.94(1)** | Serving-seafarer period: from the date of the agreement to thirty days after final discharge |

**Deliberately omitted:** any section outside Part V, and s.78(1)(e) (the MLC
rule-making hook) — the card is about where entitlement lives, not delegated
legislation. Nothing was reconstructed from the 1958 Act, and the standing
warning not to carry 1958 numbering across is retained.

### C.4 Exact final Indian-law paragraph — no placeholder remains

60-Second Answer, closing limb:

> India retains the Shipping Master institution and the agreement/engagement
> machinery within the Merchant Shipping Act framework, aligned to MLC. In the
> **Merchant Shipping Act 2025** (Part V, Seafarers) that machinery is **s.63** —
> the master, owner or recruitment-and-placement agency must enter into a
> seafarers' employment agreement in the prescribed form with every seafarer
> engaged and submit a copy to the shipping master (s.63(1)), and the seafarer
> must be given the opportunity to *examine and seek advice* on it before signing
> (s.63(3)); **s.64** requires payment at intervals not later than monthly with a
> monthly account of sums due and paid; and **s.83(1)** sends a dispute arising
> under the agreement to the shipping master. Do not carry 1958 numbering across.

15-Second Answer, closing limb:

> ... Indian ships continue equivalent engagement machinery under the **Merchant
> Shipping Act 2025, Part V (Seafarers)** — **s.63**, the seafarers' employment
> agreement in the prescribed form, a copy of which is submitted to the
> **shipping master**.

**Placeholder removed: YES.** A machine sweep of the `#q10` balanced card block
for `pending verification`, `[cite`, `TODO`, `FIXME` and any bracketed editorial
span returns **0** for every pattern.

### C.5 Digest / correction

| | |
|---|---|
| Pre-edit digest | `63df258cd94128b26192727fff37580bd400279b7a196e966d5398a5b6c08845` |
| Post-edit digest | `59f58ba9ee1bf3921d5dad020884f1d58086c5c4121c2c16f2e44eaf63beea40` |
| Correction id | `CORR-MSACT-SEA-20260902`, action `CORR-MSACT-01`, `PRIMARY_CORRECTION` |
| Supersedes | **none required** — `QB9_H#q10` is pinned by no manifest. It is named in the prose of `batch_h3a_manifest.json` and `batch_h6_manifest.json` as the card that already answers AUG-0140, but neither carries a digest for it |

The card's core answer is unchanged: the SEA as the individual employment
instrument, any CBA incorporated or referenced, the onboard copy and PSC access
under MLC Std A2.1, wage accounts under Std A2.2, the neutral discharge record
under A2.1.3, and the SEA distinguished from the DMLC and company procedure. It
was **not** expanded into a new MLC card.

---

## D. Candidate-facing placeholder sweep — the whole Oral product

**Scanned:** 234 HTML files (`meoclass1/**` and `SQ/**`), visible text only —
comments, `<script>`, `<style>` and HTML attributes stripped, so `placeholder="…"`
form attributes (219 raw hits) correctly return **0**.

| Class | Count | Verdict |
|---|---|---|
| `[cite the 2025 Act …]` / `[…pending verification]` in `QB9_H#q10` | 5 | **RESOLVED** — this pass |
| `[cite: N]` raw drafting markers | 62 across `QB3_C`, `QB8_A`, `QB9_A`, `QB9_B` | **PRE-EXISTING, REGISTERED** as `OPEN-G1-008`, `OPEN_AWAITING_FOUNDER_SIZING` |
| "pending verification" elsewhere | 22 — `QB9_H` (15 more), `QB1_I` (3), `QB3_J` (1), `QB5_B_CheatSheet` (1), `QB9_D` (1), `QB9_H_CheatSheet` (1) | **NOT a placeholder in kind** — see below. Reported for Founder sizing |
| `TODO` / `FIXME` / `TBD` / lorem ipsum | 0 | clean |
| `XXX` | 3 | all legitimate — `MOC No. XXX` as a form-field example, MMSI block `419XXXXXX`, container ID `XXXU-123456-7` |

**The distinction that matters.** An **imperative addressed to the author** —
`[cite the 2025 Act at Part level; …]` — is scaffolding and must never ship.
`(exact 2025 section pending verification)` is an **honest candidate-facing
currentness caveat**, the same species as `CURRENTNESS_UNVERIFIED` in the source
registry, and is a legitimate shippable state. The 22 remaining instances are all
of the second kind and all concern MS Act 2025 section mapping.

**Two of them are now closable cheaply and were deliberately left alone**, because
the authorisation is three items: the corrigenda retrieved here removes the exact
blocker those 22 cite. That is a bounded, well-scoped follow-up, not a defect.
`QB9_H_CheatSheet`'s line telling the candidate to cite the Act at Part level with
sections pending verification is **correct as it stands** — it describes the whole
`QB9_H` page, of which only `#q10` is resolved.

**Nothing else was expanded.** `QB3_F` carries the same "critical under ISM 10.3
→ non-conformity under ISM 9" inference for the oily-water separator; the Solved
QP pipeline carries "never for ISM 10.3 critical spares" in `QP2312` and `QP2402`.
Both are reported, neither is edited — the first is a different card outside the
three-item authorisation, the second is a different product with its own
generators and does not assert the derivation claim.

---

## E. Derived surfaces — measured, not assumed

| Surface | Result |
|---|---|
| `qb_content_index` | regenerated: **86 files, 761 canonical questions**; `--check` reports outputs already match the live derivation |
| `validate_qb_content_index` | **24 checks / 0 FAIL** — hygiene, note quality, renderer, corrections preserved, determinism |
| meoclass1 hub | rewritten by the same generator (`Q_INDEX` line, card qcounts, hero counter) |
| SQ home | unchanged — no question identity moved |
| examiner index | `--check` **PASS**, 4/4 generated artefacts current, semantic validation PASS. **958 relationships / 7 examiners**, tiers `{confirmed 459, reported 44, ce_tip 214, header 30, inferred 211}` — identical to the H6 snapshot |
| SHARE workbook | **761 rows** |
| INTERIM workbook | **761 rows** |
| WORKING master | **761 rows** |
| August month sheet | **134 NEW + 92 UPDATED = 226**, derived against baseline `2c0fd8b` — unchanged, and not manually adjusted |
| `validate_question_bank_xlsx` × 3 | **PASS** each: 761 == 761 canonical, 0 dup, 0 missing, 0 phantom, 0 dead files, 0 dead anchors, 761 hyperlinks, text/topic/qb/examiner exact, no leakage |
| `test_qb_question_text` | **7,974 controls / 0 failures** over 86 pages |
| `validate_oral_intake` | **32 PASS / 0 FAIL** |
| `validate_examiner_index` | **54 PASS / 0 FAIL** |
| `oral_manifest.py` (bare auditor) | **702 checks / 702 passed / 0 failed** |
| `validate_corrections` | **185 checks**, all PASS after known_traps entry 64 was written |
| `oral_bytes.py` | 0 control-byte or EOL hits across every file touched |

**Corpus did not move:** 761 canonical questions, 86 question-bearing files, 958
examiner relationships, 7 examiners — before and after.

---

## F. Source state

| | |
|---|---|
| Live 31-August inbox | 4,331 bytes, sha256 `d4d5b1df6a64b308f55666a89289f54b775de90cb171e9cfd3bc5d6ec4d71cfc`, mtime 2026-09-02 08:46:42 |
| Reconstruction | snapshot 01 minus its two trailing CRLF bytes + snapshot 02 + snapshot 03 = 2,615 + 722 + 994 = **4,331** |
| Verdict | **BYTE-EXACT MATCH.** Source residual **0**. No new bytes since Snapshot 03; no Snapshot 04 created or needed |

New registry rows: `SRC-MSACT-2025-CORRIGENDA`, `SRC-GRAINCODE-PARTA-TEXT`,
`SRC-SOLAS-II2-REG10-SPARECHARGES`, `SRC-ISMCODE-CONSOLIDATED`. Registry now
holds 30 sources. `SRC-MSACT-2025` updated: nine Part V claims added to
`verified_claims`, `claims_NOT_established` narrowed, `checked_on` 2026-09-02.

---

## G. Declared follow-up — content gates for these three corrections

SKILL.md §8.2a: a correction that turns on a **regulatory proposition** a later
well-meaning edit could quietly drop earns its own named content gates, as
`CORR-LSA-LIFEBOAT-VENTILATION-20260822` did. All three of these qualify:

* the ISM `10.3 identifies → SMS/PMS translates → CE manages` hierarchy, and the
  conditional ISM 9 limb;
* the Grain Code A 3.2 accompany-or-incorporate relationship and the four-term
  separation;
* the absence of any editorial placeholder in `QB9_H#q10`.

Each proposition is **enumerated in its correction manifest** so it is
recoverable, but **no `validate_correction_*.py` / `mutate_correction_*.py` pair
was written in this pass**. Writing six new gates would add gate ids to
`oral_release_gates.py`, `POST_E6_GATES` and `POST_E6_MUTATION_SUITES`, moving
totals that other controls pin — that is a sized job of its own and beyond a
three-item authorisation. **Recommended as the next bounded work order.** Until
then these three corrections are protected by their digest pins and by
`validate_corrections` / `mutate_corrections`, which is what every other
correction on main has, but not by content assertions.

---
