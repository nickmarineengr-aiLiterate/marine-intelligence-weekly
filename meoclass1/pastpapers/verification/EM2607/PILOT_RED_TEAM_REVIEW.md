# EM2607 — Pilot red-team review of Q1 and Q2

Reviewed: 2026-08-08. Reviewer stance: adversarial. The v0.1 answers were treated as prototypes
containing probable defects, not as work to be defended.

Result: **15 findings — 2 Critical, 6 Major, 5 Minor, 2 Style.** Two Critical findings are legal
errors that would have propagated into every future liability question in this series had they been
carried forward.

Severity key: **Critical** = wrong as a matter of law or fact, would mislead a candidate ·
**Major** = materially overstated, mis-scoped or badly prioritised for the examination ·
**Minor** = imprecise or unlabelled · **Style** = presentation only.

---

## RT-01 — Q1(a) answer shape is academically inverted

**Section.** Q1 model answer, limb (a).

**Current wording.** Five blocks: definition, five steps, *"Where it applies… **A ship does not carry
out an FSA.**"*, *"How FSA reaches this cargo"*, then a single short paragraph applying Step 1 to the
cargo.

**Finding.** The examiner asked to *"Discuss the application of a formal safety assessment in loading
and carriage of iron ore pellets as cargo in bulk."* The object of the sentence is the **application
of the methodology to the operation**. The v0.1 answer spends roughly half of an 8-mark limb
establishing that a ship does not formally conduct an FSA, and applies only Step 1. Steps 2–5 are
dismissed in one clause as "already discharged at IMO level". A candidate writing this would be
answering a narrower question than the one set, and would forfeit marks available for hazard
identification, risk analysis, control options and cost-benefit reasoning.

The distinction itself is correct and worth keeping — it is what separates a strong answer from a
recited list — but it must **support** the answer, not consume it.

**Primary source.** MSC-MEPC.2/Circ.12/Rev.2 §4.2.1: *"the problem under consideration should be
characterized by a number of functions. Where the problem relates for instance to a type of ship,
these functions include carriage of payload… Alternatively, where the problem relates to a type of
hazard… the functions include prevention, detection, alarm, containment…"* The Guidelines' own generic
model therefore contemplates scoping FSA onto a defined problem such as a cargo operation. IMO did
exactly this for bulk carrier safety. Applying the five steps to iron ore pellet carriage is
methodologically coherent and is what the question invites.

**Severity.** Major.

**Action.** Restructure limb (a): brief definition and the five steps, then **apply all five steps**
to the loading and carriage of iron ore pellets, then a two-line qualifier that FSA is strictly a
rule-development methodology and shipboard implementation runs through risk assessment under the SMS
and compliance with the resulting mandatory instruments. Move the fuller treatment of that
distinction into Study Notes.

**Agent rule learned.** *Answer the grammatical object of the question.* Where a question says
"application of X to Y", the marks are in the applying, not in defining X or in explaining the limits
of X. A correct-but-off-axis insight is still off-axis. Decompose the question stem before drafting
and identify what is being asked to be **done**, not merely discussed.

---

## RT-02 — "IRON ORE PELLETS = Group C" stated more categorically than the evidence supports

**Section.** Q1 model answer limb (b), Q1 study notes, Q1.md verification table row 1.12.

**Current wording.** *"Confirm the BCSN is IRON ORE PELLETS (Group C)"* and, in the study notes,
*"Iron ore **pellets** are Group C."* Q1.md records this as VERIFIED.

**Finding.** MIW holds no licensed IMSBC Code. The classification rests on corroborating secondary
sources (BIMCO's Group C listing and several industry references) plus the metallurgical logic that
pelletising removes the fine fraction that drives liquefaction. That is genuine corroboration, but it
is **not** the primary schedule text, and the v0.1 files presented it as though it were. Under the
provenance scheme now adopted this is `P2_AUTHORITATIVE_SECONDARY`, not `P1_PRIMARY_VERIFIED`.

**Primary source.** None obtained. Attempts against the IMO-hosted supplement, an official
government-hosted copy of the Code, and class circulars all failed to return the individual schedule.

**Severity.** Major.

**Action.** Retain the classification — the corroboration is strong and a candidate needs an answer —
but attribute it honestly and make the *method* the load-bearing point: the shipper's declared BCSN
and the individual schedule govern, and the answer shows the candidate checking rather than assuming.
Downgrade Q1.md row to P2 and keep the schedule text on the unresolved list.

**Agent rule learned.** *Corroboration is not primary verification.* Two secondary sources agreeing is
worth recording, but it must not be laundered into a primary citation. Where the primary text is
unobtainable, the answer should lean on the verifiable **procedure** (check the declaration, consult
the schedule) rather than on the unverifiable **value**.

---

## RT-03 — The fines/pellets binary is itself an oversimplification

**Section.** Q1 study notes, "The trap in this question"; Q1.md §0 table.

**Current wording.** *"Iron ore **pellets** are Group C. Iron ore **fines** are Group A."* presented as
a clean binary.

**Finding.** Not reliably true as stated. The IRON ORE schedule family was substantially amended, and
the classification of iron ore fines is **conditional**: fines meeting stated criteria based on
goethite content and particle size distribution may be carried as a Group C cargo rather than Group A.
The v0.1 answer taught a binary that the Code itself does not draw. This is the same class of error
the pilot congratulated itself for catching — one level deeper.

**Primary source.** Not obtained. The conditional criteria are reported by class/industry commentary
(IRClass technical circular material; industry summaries referencing goethite content and particle
size distribution). Resolution **MSC.393(95)**, adopted June 2015, is the instrument that introduced
IRON ORE FINES as a Group A schedule and the Modified Proctor/Fagerberg procedure, mandatory
1 January 2017. The exact numeric thresholds could **not** be verified and are **not** stated
anywhere in the answer.

**Severity.** Major.

**Action.** Replace the binary with the accurate proposition: several distinct iron-ore cargoes exist,
their Groups differ, and the fines schedule carries qualifying criteria under which fines may be
Group C. The operative rule for a candidate is unchanged and becomes stronger: **the declared BCSN and
its individual schedule govern — never the commodity name.**

**Agent rule learned.** *A memorable simplification is a defect vector.* When the pilot produces a
crisp "X versus Y" teaching point, red-team the simplification itself before publishing it; crisp
binaries are exactly what candidates memorise and therefore exactly what must be right.

---

## RT-04 — "Group C cargoes have no TML"

**Section.** Q1 study notes, common mistakes.

**Current wording.** *"Quoting a TML for iron ore pellets. Group C cargoes have no TML."*

**Finding.** Directionally right but loosely put. TML is a property defined for cargoes that may
liquefy; it is not that Group C cargoes possess a null TML, but that the concept does not apply to a
cargo properly classified outside Group A. Given RT-03, the phrasing also invites the false inference
that Group is a fixed attribute of a commodity.

**Primary source.** IMSBC Code §1.7 definitions (Group A / Group C); TML defined in relation to
cargoes which may liquefy.

**Severity.** Minor.

**Action.** Reword: TML is a Group A concept and does not apply to a cargo correctly classified as
Group C; if a TML is being demanded for your cargo, question the classification.

**Agent rule learned.** State the *reason* a property is inapplicable, not merely that it is absent.
"Does not apply because…" survives red-teaming; "has none" usually does not.

---

## RT-05 — Unlabelled engineering judgement

**Section.** Q1 model answer limb (b); Q1 study notes.

**Current wording.** *"tank-top strength and permissible mass per hold, not cubic capacity, are the
limits"* and *"For this cargo the binding constraint is usually tank-top strength."*

**Finding.** Sound engineering, but presented in the same register as the regulatory statements around
it. The brief requires established legal requirement, guidance, company practice and engineering
judgement to be distinguishable. "Usually" is doing undeclared work.

**Primary source.** None — this is judgement informed by the loading manual regime under SOLAS XII/11
and the approved loading conditions.

**Severity.** Minor.

**Action.** Keep the content, mark it as engineering judgement, and anchor the hard constraint to the
approved loading manual, which is the actual governing document.

**Agent rule learned.** Every sentence in a model answer should be classifiable into one of the four
registers on sight. If a reader cannot tell whether a sentence is law or judgement, it is written
wrongly regardless of whether it is true.

---

## RT-06 — Casualty Investigation Code presented as automatically engaged *(Q2)*

**Section.** Q2 model answer, component 4.

**Current wording.** *"Cooperate fully with the coastal, port and flag States and with the safety
investigation under the **Casualty Investigation Code, resolution MSC.255(84)**, mandatory through
SOLAS chapter XI-1."*

**Finding.** Materially overstated. The Code's mandatory investigation requirement is confined to
**very serious marine casualties**. A bunker overflow will not usually meet that threshold, and may
not meet the definition of a marine casualty at all.

**Primary source.** Casualty Investigation Code (res. MSC.255(84)), full text retrieved and read:
- §2.22: *"A **very serious marine casualty** means a marine casualty involving the total loss of the
  ship or a death or severe damage to the environment."*
- §2.9: a **marine casualty** requires one of seven listed outcomes; the environmental limb, §2.9.7,
  is *"severe damage to the environment, or the potential for severe damage to the environment,
  **brought about by the damage of a ship or ships**"* — an intact ship overfilling a tank does not
  obviously satisfy it.
- §2.10: a **marine incident** is an event *"other than a marine casualty"* which endangered or would
  endanger safety or the environment.
- Part II (mandatory) **chapter 6** is titled *"Requirement to investigate very serious marine
  casualties"*. Part III (recommended practice) **chapter 17** covers *"Investigation of marine
  casualties (other than very serious marine casualties) and marine incidents"*.

So an ordinary bunker overflow most likely sits at **marine incident**, where investigation is
recommended practice, not a mandatory Code obligation.

**Severity.** Major.

**Action.** Rewrite conditionally and separate the investigation types the Chief Engineer may
actually face: coastal/port State pollution and enforcement investigation; flag State investigation;
a marine safety investigation under the Code **if the event meets the threshold**; a criminal
investigation; and the owner's own P&I/insurer investigation. State that the Chief Engineer's conduct
is the same whichever authority attends — which is the real examinable point.

**Agent rule learned.** *Check the trigger, not just the instrument.* Before citing a convention or
code as engaged, verify that the factual scenario meets its own definitional threshold. Naming a
correct instrument that does not apply is a substantive error, not a citation quibble.

---

## RT-07 — Bunkers Convention: liability and insurance conflated **[CRITICAL]**

**Section.** Q2 model answer, component 5; Q2 study notes; Q2.md rows 2.12 and 2.13.

**Current wording.** *"the **Bunkers Convention 2001** … imposes strict liability on the **registered
owner**, with compulsory insurance above 1,000 GT and direct action against the insurer."*

**Finding.** **Wrong.** The Convention deliberately separates the person who is *liable* from the
person who must *insure*, and the v0.1 answer collapsed them — the precise error the brief warned
against. Liability attaches to a **much broader** set of persons than the registered owner, jointly
and severally.

**Primary source.** Bunkers Convention 2001, full text retrieved and read:
- **Article 1(3):** *"'Ship-owner' means the owner, including the registered owner, bareboat
  charterer, manager and operator of the ship."*
- **Article 1(4):** *"'Registered owner' means the person or persons registered as the owner of the
  ship…"*
- **Article 3(1):** *"…the ship-owner at the time of an incident shall be liable for pollution damage
  caused by any bunker oil on board or originating from the ship…"*
- **Article 3(2):** *"Where more than one person is liable in accordance with paragraph 1, their
  liability shall be **joint and several**."*
- **Article 7(1):** *"The **registered owner** of a ship having a gross tonnage greater than 1000
  registered in a State Party shall be required to maintain insurance or other financial security…"*

**Severity.** **Critical.**

**Action.** Rewrite: liability under Article 3 attaches to the *shipowner* as defined in Article 1(3)
— owner, registered owner, bareboat charterer, manager and operator — jointly and severally; the
Article 7 compulsory insurance duty falls on the **registered owner** alone, for ships over 1,000 GT.
Correct Q2.md rows 2.12/2.13. Add the Article 3(3)/(4) defences so "strict" is properly qualified
(see RT-09).

**Agent rule learned.** *Read the definition article before using a defined term.* Conventions define
terms precisely and often counter-intuitively; a term of art repeated from memory or from secondary
summaries is a primary source of error. Where a convention has both a liability article and an
insurance article, assume they address different persons until proven otherwise.

---

## RT-08 — "CLC 1992 does not apply" is too categorical **[CRITICAL]**

**Section.** Q2 model answer component 5; Q2 study notes, "The distinction that separates good from
average"; Q2.md row 2.14.

**Current wording.** *"**CLC 1992 does not apply** — it covers persistent oil carried as cargo in bulk
by an oil tanker."* The study notes elevate this to the answer's headline discriminator.

**Finding.** **Wrong as stated, and wrong in a way that inverts the intended teaching point.** CLC
1992 expressly covers persistent oil *in the bunkers* of a CLC "ship". Where the vessel is a CLC
"ship", a bunker spill is CLC pollution damage and the **Bunkers Convention is excluded** by its own
Article 4(1). The question says only *"a large merchant ship"* — it does not say non-tanker. The
correct answer is conditional, and the conditionality is the sophisticated point.

**Primary source.**
- **Bunkers Convention Article 4(1):** *"This Convention shall not apply to pollution damage as
  defined in the Civil Liability Convention, whether or not compensation is payable in respect of it
  under that Convention."* (retrieved and read)
- **CLC 1992 Article I(5), "Oil":** *"any persistent hydrocarbon mineral oil such as crude oil, fuel
  oil, heavy diesel oil and lubricating oil, whether carried on board a ship as cargo **or in the
  bunkers of such a ship**."*
- **CLC 1992 Article I(1), "Ship":** *"any sea-going vessel and seaborne craft of any type whatsoever
  constructed or adapted for the carriage of oil in bulk as cargo, provided that a ship capable of
  carrying oil and other cargoes shall be regarded as a ship only when it is actually carrying oil in
  bulk as cargo and during any voyage following such carriage unless it is proved that it has no
  residues of such carriage of oil in bulk aboard."*

Two further conditions the v0.1 answer missed entirely: CLC reaches only **persistent** oil, so a
distillate bunker spill falls outside it regardless of ship type; and the CLC "ship" test turns on
laden/following-voyage status, not merely on the vessel being a tanker.

**Severity.** **Critical.**

**Action.** Replace with conditional wording: if the vessel is a CLC "ship" and the escaped bunker oil
is persistent, the CLC regime applies and the Bunkers Convention is excluded by Article 4(1);
otherwise the Bunkers Convention governs. Note that the question does not specify ship type and that
saying so is itself creditworthy. Correct Q2.md row 2.14 and the study-notes headline.

**Agent rule learned.** *Where two regimes are mutually exclusive, verify the exclusion clause and
both scope definitions before asserting which applies.* Also: when a scenario is silent on a fact that
determines the legal answer, the model answer must be conditional and must say why — inventing the
missing fact is the error, and so is picking one branch silently.

---

## RT-09 — "Strict liability" unqualified

**Section.** Q2 model answer component 5.

**Current wording.** *"imposes strict liability on the registered owner"*.

**Finding.** Article 3 liability arises without proof of fault, but it is not absolute: Article 3(3)
provides three complete defences (act of war or an exceptional, inevitable and irresistible natural
phenomenon; damage wholly caused by a third party's intentional act or omission; damage wholly caused
by the negligence or wrongful act of an authority responsible for navigational aids), and Article 3(4)
provides for whole or partial exoneration where the claimant contributed.

**Primary source.** Bunkers Convention Articles 3(3) and 3(4), retrieved and read.

**Severity.** Minor.

**Action.** Phrase as liability without proof of fault, subject to the Article 3 defences, and list
the defences compactly in the study notes.

**Agent rule learned.** "Strict" is a term of art that examiners probe. Always pair it with its
statutory exceptions.

---

## RT-10 — "No admission of liability" mis-registered as a legal duty

**Section.** Q2 model answer component 4; study notes examiner traps.

**Current wording.** Listed inline among MARPOL and Casualty Investigation Code obligations: *"no
admission of liability"*.

**Finding.** Prudent and correct advice, but it is **P&I and legal-protection practice**, not an
international-law requirement. Placed among convention citations it reads as though a treaty requires
it. Similarly, the right to have a Company representative or P&I correspondent present is a matter of
local procedural law and club practice, not a universal entitlement — the fair-treatment guidelines
(res. LEG.3(91)) are recommendatory.

**Primary source.** Res. LEG.3(91) is a Legal Committee resolution adopting **guidelines**, promoted
by Assembly res. A.1056(27) — recommendatory in character.

**Severity.** Major.

**Action.** Separate the conduct advice into an explicitly labelled block: *"P&I and legal-protection
practice, not a statutory requirement."* Keep the fair-treatment guidelines but describe them as
guidelines whose application depends on the coastal State.

**Agent rule learned.** *Register-tag every imperative.* Advice of the form "do not X" must carry its
authority: law, guideline, club practice, or judgement. Un-sourced imperatives placed near citations
inherit unearned authority from their neighbours.

---

## RT-11 — Criminal-exposure claim overstated as general

**Section.** Q2 model answer component 5; study notes.

**Current wording.** *"The gravest risk is usually not the spill but the record — a false ORB entry is
a separate offence, often prosecuted more severely than the discharge itself."*

**Finding.** This reflects a real and well-documented enforcement pattern, but it is heavily shaped by
United States APPS prosecutions. The question specifies an unnamed foreign jurisdiction. Presenting a
jurisdiction-specific enforcement pattern as a general truth ("usually") is exactly the overreach the
answer elsewhere avoids by refusing to name an authority.

**Primary source.** The underlying legal mechanism *is* verifiable and general: MARPOL Annex I
regulation 17.6 makes a master-certified copy of an ORB entry *"admissible in any juridical
proceedings as evidence of the facts stated in the entry"*. That supports "a false entry is
evidentially dangerous everywhere"; it does not support "usually prosecuted more severely".

**Severity.** Major.

**Action.** Keep the reg 17.6 mechanism as the load-bearing statement. Reduce the enforcement pattern
to a labelled observation in the study notes — *practical enforcement experience, most prominently in
the United States* — and remove "usually" from the model answer.

**Agent rule learned.** *Enforcement practice is not law, and enforcement practice is jurisdictional.*
Where the scenario's jurisdiction is unspecified, only generally-applicable mechanisms may appear in
the model answer; jurisdiction-flavoured colour belongs in study notes, labelled.

---

## RT-12 — Q2 model answer over length

**Section.** Q2 model answer, whole.

**Current wording.** 667 words against a 450–650 band for 16 marks.

**Finding.** 2.6% over. The corrections in RT-06 to RT-11 add conditional wording, which will worsen
it unless offset. The six-heading structure is right; the prose within it can carry less.

**Severity.** Minor.

**Action.** Absorb the legal corrections and bring the total back within band by compressing narrative
in components 1 and 2, which are the least mark-dense.

**Agent rule learned.** Budget words against marks *before* drafting, per component. Retrofitting
length after a legal rewrite tends to cut the wrong material.

---

## RT-13 — Provenance granularity too coarse

**Section.** Both questions; `verification_status` field.

**Current wording.** `"Verified with two items unresolved"` / `"Verified"` — one string for an entire
question.

**Finding.** A single status per question cannot answer the two questions a production agent must ask:
which individual claims need re-verification before publication, and which came from internal reuse
versus external research. RT-02, RT-07 and RT-08 would all have been caught earlier had claims carried
provenance classes, because RT-07 and RT-08 were both recorded as VERIFIED on the strength of
secondary summaries.

**Severity.** Major.

**Action.** Adopt per-claim provenance classes (implemented — see §9 of the workflow notes) and have
the validator count and surface `TIME_SENSITIVE_REVERIFY` and `UNRESOLVED` claims.

**Agent rule learned.** *Verification state belongs on the claim, not on the question.* Question-level
status averages away exactly the claims most likely to be wrong.

---

## RT-14 — Study-notes flourish now partly false

**Section.** Q1 study notes, "The trap in this question".

**Current wording.** *"Almost every textbook example of liquefaction uses iron ore fines."*

**Finding.** Rhetorical, unverifiable as stated, and undercut by RT-03. Also nickel ore and bauxite are
at least as commonly used.

**Severity.** Style.

**Action.** Reword factually.

**Agent rule learned.** Avoid unfalsifiable intensifiers ("almost every", "usually", "invariably") in
verified content. They cannot be sourced and they age badly.

---

## RT-15 — Answer philosophy: sophistication displaced scoring content

**Section.** Cross-cutting, both questions.

**Finding.** The pilot's failure mode was not carelessness — it was **impressive material crowding out
examinable material**. Q1(a) traded application marks for a methodological aside. Q2 elevated a
CLC/Bunkers distinction to headline status and got it backwards. In both cases the research was
genuinely good and the *placement* was wrong.

**Severity.** Major (process).

**Action.** Adopt the three-layer test for every future answer: Layer 1 what must be written to score;
Layer 2 why it is true; Layer 3 deeper understanding, traps, oral follow-ups. **Model answer = Layer 1
plus only the Layer 2 needed to make it correct. Study notes = the rest.**

**Agent rule learned.** *The model answer is not where you demonstrate research depth.* Depth that does
not earn marks belongs in study notes. A production agent optimising for apparent sophistication will
reliably produce lower-scoring answers than one optimising for the marking scheme.

---

## Disposition

| ID | Severity | Action |
|---|---|---|
| RT-01 | Major | Q1(a) restructured to apply all five FSA steps |
| RT-02 | Major | Group C claim attributed to P2, method made load-bearing |
| RT-03 | Major | Binary replaced with conditional schedule framing |
| RT-04 | Minor | TML wording corrected |
| RT-05 | Minor | Engineering judgement labelled |
| RT-06 | Major | Casualty Code made conditional; investigation types separated |
| RT-07 | **Critical** | Liability vs insurance separated per Arts 1(3), 3, 7(1) |
| RT-08 | **Critical** | CLC applicability made conditional per Art 4(1) and CLC Art I |
| RT-09 | Minor | "Strict" qualified by Art 3 defences |
| RT-10 | Major | Conduct advice re-registered as P&I practice |
| RT-11 | Major | Enforcement pattern labelled and de-generalised |
| RT-12 | Minor | Length brought back within band |
| RT-13 | Major | Per-claim provenance classes implemented |
| RT-14 | Style | Flourish reworded |
| RT-15 | Major (process) | Three-layer test adopted for all future questions |

All fifteen were actioned in the same pass. See `Q1.md`, `Q2.md` and the spec for the corrected text.
