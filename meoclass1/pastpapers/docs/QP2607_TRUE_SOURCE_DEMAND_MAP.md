# QP2607 — TRUE SOURCE DEMAND MAP

**Handoff contract from the QP (Written Questions) track to the True Source corpus-production track.**
Written 2026-08-08 against `specs/QP2607.json` at commit `b2535d8`.

**This document creates no corpus content, no viewer and no reference-shelf entries.** It states
what the nine verified July 2026 answers actually need, so the corpus track can build in demand
order instead of book order.

Read with `MIW_TRUE_SOURCE_CONTRACT.md` (the schema and resolver boundary) and `CURRENT_STATUS.md`
(the product state). This document is the *demand* side; the contract is the *interface* side.

---

## 1. Architectural boundary — frozen

```
TRUE SOURCE CORPUS          canonical regulatory content: source text, edition,
        |                   amendment/consolidation state, provenance, effective
        |                   dates, structured + PDF representations, bookmarks
        v
REFERENCE REGISTRY / RESOLVER
        |
        v
STABLE LOGICAL OBJECT ID    e.g. MARPOL-VI-14, IMSBCCode-4, FSSCode-9-2
        |
        +--> QP (Written Questions)   +--> RulesApp   +--> QB   +--> Oral Notes   +--> future engines
```

**`RulesApp/repository/` is not the physical master store.** It is an intelligence and relationship
consumer. What it *does* provide, and what this map reuses, is an established and internally
consistent **logical ID convention** already applied across 78 registered standards.

**One canonical source, many consumers.** A corpus object is authored once and related to; it is
never copied into a question spec, and never duplicated per paper.

Nothing was moved, copied or imported in this session.

---

## 2. Object ID policy — adopt, do not reinvent

The convention in `RulesApp/repository/index/repo-data.json` is adopted as-is:

```
<INSTRUMENT>-<STRUCTURAL-TOKENS…>          single hyphens, no "::" separators

SOLAS-VI-2          SOLAS chapter VI regulation 2
SOLAS-XII-11        SOLAS chapter XII regulation 11
MARPOL-I-37-371     MARPOL Annex I regulation 37.1
MARPOL-VI-14-144    MARPOL Annex VI regulation 14.4
IMSBCCode-4         IMSBC Code section 4
ISM-9               ISM Code element 9
BunkerConvention2001-Articles-7
```

The object id identifies the **logical regulatory object**. It never identifies a PDF page, a local
path, a generated PDF or a viewer implementation. The resolver maps object → physical
representation. `validate_spec.py` already fails the build on any page-shaped reference.

### 2.1 Measurement taken this session

Counted directly from `repository/index/repo-data.json` on 2026-08-08:

| | |
|---|---|
| Registered standards | **78** |
| Total nodes | **1,006** |
| Standards with zero nodes | **31** (registered shells — identity exists, content does not) |

`MIW_TRUE_SOURCE_CONTRACT.md` §4 records 788 nodes. The figure has moved. Treat **1,006** as
current and re-measure rather than quoting either number from memory.

### 2.2 Collision and coverage findings — reported, not redesigned

The scheme itself is sound. **No syntax collision was found across 1,006 nodes.** Four issues are
worth the corpus track's attention, in descending severity:

**(a) MARPOL Annex VI is represented twice, under two disjoint vocabularies.** — *resolver ambiguity*

```
marpol-73-78    ->  MARPOL-VI-14        MARPOL-VI-14-141   MARPOL-VI-14-144   MARPOL-VI-14-148
mepc-328-76     ->  MEPC32876-3-14      MEPC32876-3-18     MEPC32876-1-4      MEPC32876-4-26
```

A question citing "MARPOL Annex VI regulation 14" today has **two** candidate object ids and no
stated rule for choosing. Q4 depends on this regulation more heavily than on anything else in the
paper. This is an ambiguity in the *registry*, not a flaw in the id syntax, and it must be resolved
before any Q4 reference is populated. `repository/index/provision-truth-aliases.json` already exists,
so the mechanism for declaring one canonical id and aliasing the other is in place.

**(b) Sub-paragraph tails repeat across annexes.** — *handling instruction, not a defect*

`MARPOL-I-14-146` already exists and means *Annex I reg 14.6 — oil filtering equipment
specification (15 ppm)*. Q4 needs `MARPOL-VI-14-146`, which means *Annex VI reg 14.6 — written
changeover procedure and logbook record*. Entirely different rules, one character apart, and the QP
layer will carry both. The annex token disambiguates correctly and the scheme works. **Every label
must name the annex**, so a derived layer can never render "reg 14.6" unqualified.

**(c) Granularity is coarser than the questions need in three places.** — *coverage, not identity*

| Node | Covers | Question needs |
|---|---|---|
| `ISM-13` | ISM elements 1–3 in one node | Q1 needs **1.2.2.2** specifically |
| `ISM-78` | elements 7 *and* 8 merged | Q2 and Q8 both cite **element 8** alone |
| `IMSBCCode-Appendix1` | one flat node for **all** individual schedules | Q1 needs the **named** IRON ORE PELLETS schedule |

The id scheme supports the depth — `ISM-13-1222` is well-formed. The nodes simply do not exist.

**(d) Finding (c), third row, is the structural expression of the Q1 semantic incident.** A single
flat node standing for every individual schedule is exactly the shape that lets "declared BCSN → its
current individual schedule" collapse into "pellets are Group C". See §5.

**Recommendation: adopt the existing scheme unchanged.** Fix (a) by declaring a canonical id; fix (c)
by adding nodes. Neither needs a new vocabulary.

---

## 3. How to read the demand tables

### Classification

| | |
|---|---|
| **P** | **PRIMARY ANSWER SUPPORT** — directly substantiates a material proposition in the Model Written Answer |
| **S** | **SUPPORTING** — authoritative background, procedure or related rule |
| **C** | **CONTEXT** — useful, but not needed to prove the examination answer |

**Corpus production priority is driven by P.** S is built when it comes cheaply with a P object.
C is recorded so that nobody builds it by mistake.

The demand was derived from each question's **model answer text**, its canonical `answer_route`, its
`regulations[]` list and its `quick_revision.critical_regulation` — not from everything named
anywhere in the study guide. Where an instrument appears only in the study guide it is marked C.

### The two availability axes — these are different questions

| Column | Question it answers | How it was established |
|---|---|---|
| **ID** | Does a stable logical identity already exist in the established convention? | **Verified** against `RulesApp/repository/index/repo-data.json`, 2026-08-08 |
| **Corpus** | Does the True Source layer hold resolvable consolidated source content? | **Not verifiable from this machine** — see below |

**The True Source corpus is a separately governed store and is not checked out on this machine.**
It was not inspected, imported or assumed. Therefore `Corpus` reads **UNKNOWN** for almost
everything, which is the honest value and is in the contract's vocabulary for exactly this reason.

Two exceptions are known with certainty and are stated as such:

- **NOT_AVAILABLE — IMSBC individual schedules.** MIW holds no licensed IMSBC Code. This is a
  standing rule (`CURRENT_STATUS.md` §11) and the basis of Q1's class C limitation. It is a
  **licensing gate, not a work item**.
- **IN HAND — Merchant Shipping Act 2025 and S.O. 1244(E).** Both were read in full from the Gazette
  during Q7 verification, with document numbers recorded in `verification/QP2607/Q7.md`.

`ID` values: **EXISTS** · **PARTIAL** (parent exists, needed depth does not) · **NONE**.
`Treat` values: **FULL_CORPUS** · **REFERENCE_PACK** · **EXISTING_OBJECT** (extend what is there).
`Curr` = currency sensitivity: LOW · MEDIUM · HIGH.

Proposed object ids are **proposals**. The corpus track owns final ids and may restructure within
the convention.

---

## 4. Q1 — Iron ore pellets: FSA, carriage and voyage monitoring

**Authority required:** IMO (MSC/MEPC circular; SOLAS; IMSBC Code — **licensed copy required**; BLU Code).

| Ref | Claim scope (answer section) | Instrument · section | Relationship | Desired object id | ID | Corpus | Treat | Curr |
|---|---|---|---|---|---|---|---|---|
| **P1** | (a) 1, 3 — FSA is a structured methodology **applied by Member States and IMO Committees, not by ships** (para 1.3.1) | MSC-MEPC.2/Circ.12/Rev.2, para 1.3.1 | PRIMARY_RULE | `MSCMEPC2Circ12Rev2-1-31` | NONE | UNKNOWN | REFERENCE_PACK | LOW |
| **P2** | (a) 2 — the five FSA steps | MSC-MEPC.2/Circ.12/Rev.2, methodology sections | PROCEDURE | `MSCMEPC2Circ12Rev2-2` | NONE | UNKNOWN | REFERENCE_PACK | LOW |
| **P3** | (b) 4 — shipper must provide cargo information before loading | SOLAS VI/2 | PRIMARY_RULE | `SOLAS-VI-2` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **P4** | (b) 4 — declaration content and the BCSN | IMSBC Code 4.2 | PRIMARY_RULE | `IMSBCCode-4-42` | PARTIAL (`IMSBCCode-4`) | NOT_AVAILABLE | FULL_CORPUS | MEDIUM |
| **P5** | (b) 4 — **declared BCSN and its current individual schedule govern, never the commodity name**; IRON ORE, IRON ORE FINES, IRON ORE PELLETS and DIRECT REDUCED IRON (B) are separate schedules | IMSBC Code Appendix 1, named individual schedules | PRIMARY_RULE | `IMSBCCode-Appendix1-IRONOREPELLETS` + siblings | PARTIAL (one flat `IMSBCCode-Appendix1`) | **NOT_AVAILABLE** | FULL_CORPUS | **HIGH** |
| **P6** | (b) 5 — loading instrument, bulk carriers 150 m and above | SOLAS XII/11 | NUMERIC_SOURCE | `SOLAS-XII-11` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **P7** | (b) 6 — water ingress alarms: 0.5 m above inner bottom; 15% of hold depth but not more than 2.0 m | SOLAS XII/12 | NUMERIC_SOURCE | `SOLAS-XII-12` | **NONE** | UNKNOWN | EXISTING_OBJECT | LOW |
| **S1** | (a) 3 — shipboard analogue is the SMS risk assessment | ISM Code 1.2.2.2 | SUPPORTING_RULE | `ISM-13-1222` | PARTIAL (`ISM-13`) | UNKNOWN | EXISTING_OBJECT | LOW |
| **S2** | (b) 5 — loading sequence and trimming | BLU Code | SUPPORTING_RULE | `BLUCode-…` | NONE | UNKNOWN | REFERENCE_PACK | LOW |
| **S3** | (b) 5 — approved loading plan, stowage of solid bulk cargoes | SOLAS VI/7 | SUPPORTING_RULE | `SOLAS-VI-7` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **C1** | amendment currency of the Code | IMSBC amendments 07-23, 08-25; MSC.393(95) | CONTEXT | edition/version metadata, not a node | — | NOT_AVAILABLE | FULL_CORPUS (edition state) | **HIGH** |

**Notes**

- **SOLAS XII/12 does not exist in the registry.** Chapter XII currently holds regs 1, 3, 5, 10 and 11
  only. P7 is one node's worth of work against an instrument already registered, and it carries three
  examinable numbers.
- **P5 is the reason this whole programme exists.** Q1's model answer states a *conditional*:
  pellets are carried as Group C **but establish that from the declared BCSN and its current
  individual schedule**. Derived layers had already flattened this to "pellets are Group C" — caught
  and fixed, now guarded by `SEMANTIC_GUARDS` and recorded as trap 16. **The corpus must make BCSN,
  the individual schedule, and the amendment state first-class properties.** Do not encode
  `pellets = Group C` as a universal semantic object; encode the route to the schedule.
- **P5's carriage requirement is unresolvable without a licensed IMSBC Code.** Nothing else in the
  paper is blocked this way.
- The iron ore *fines* goethite/particle-size thresholds are deliberately **not stated anywhere in
  the answer** because they were never verified. Do not let a corpus build invent a demand for them.

---

## 5. Q2 — Bunker overflow in foreign waters

**Authority required:** IMO (MARPOL, Assembly/MSC/LEG resolutions); IMO/diplomatic conference (Bunkers
Convention 2001, CLC 1992).

| Ref | Claim scope | Instrument · section | Relationship | Desired object id | ID | Corpus | Treat | Curr |
|---|---|---|---|---|---|---|---|---|
| **P1** | 2 — ORB entries for the incident | MARPOL Annex I reg 17 | PRIMARY_RULE | `MARPOL-I-17` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **P2** | 2 — **a master-certified copy of an ORB entry is admissible in juridical proceedings as evidence of the facts stated** | MARPOL Annex I reg 17.6 | LEGAL_BASIS | `MARPOL-I-17-176` | **NONE** | UNKNOWN | FULL_CORPUS | LOW |
| **P3** | 1, 3 — SOPEP response and carriage thresholds (tankers 150 GT+, other ships 400 GT+) | MARPOL Annex I reg 37, 37.1, 37.2 | PRIMARY_RULE · NUMERIC_SOURCE | `MARPOL-I-37`, `-371`, `-372` | **EXISTS** (all three) | UNKNOWN | EXISTING_OBJECT | LOW |
| **P4** | 3 — duty to report an incident | MARPOL article 8 and Protocol I | PRIMARY_RULE | `MARPOL-Art-8`, `MARPOL-ProtocolI` | **NONE** (registry holds annex regulations only) | UNKNOWN | FULL_CORPUS | LOW |
| **P5** | 3 — the reporting format | res. A.851(20) | PROCEDURE | `A85120-…` | NONE | UNKNOWN | REFERENCE_PACK | LOW |
| **P6** | 5 — shipowner widely defined; strict liability | Bunkers Convention 2001 arts 1, 3 | LEGAL_BASIS | `BunkerConvention2001-Articles-12`, `-3` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **P7** | 5 — compulsory insurance on the **registered owner**, over 1,000 GT; direct action | Bunkers Convention 2001 art 7 | LEGAL_BASIS · NUMERIC_SOURCE | `BunkerConvention2001-Articles-7` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **P8** | 5 — CLC applies **only if** a CLC ship and persistent oil | CLC 1992 art I(1), I(5) | DEFINITION | `CLC1992-Articles-I` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **P9** | 4 — casualty investigation threshold and the duty to cooperate | Casualty Investigation Code, res. MSC.255(84), defs 2.9/2.10/2.22, chs 6 and 17 | PROCEDURE | `MSC25584-2`, `-6`, `-17` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **P10** | 6 — report, analyse, corrective action, close-out | ISM Code elements 8 and 9 | SUPPORTING_RULE | `ISM-78`, `ISM-9` | **EXISTS** (8 merged with 7) | UNKNOWN | EXISTING_OBJECT | LOW |
| **S1** | 5 — the CLC carve-out that bounds the Bunkers regime | Bunkers Convention 2001 art 4 | LEGAL_BASIS | `BunkerConvention2001-Articles-4` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **S2** | 2 — bunker delivery note and retained sample | MARPOL Annex VI reg 18 | SUPPORTING_RULE | `MEPC32876-3-18` (see §2.2(a)) | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **S3** | 4 — fair treatment of seafarers | res. LEG.3(91); res. A.1056(27) | SUPPORTING_RULE | `LEG391-…` | NONE | UNKNOWN | REFERENCE_PACK | LOW |
| **S4** | 4 — the flag/coastal State obligation to investigate | SOLAS XI-1/6 | LEGAL_BASIS | `SOLAS-XI1-6` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **C1** | preparedness and co-operation background | OPRC 1990 | CONTEXT | `OPRC1990-…` | NONE | UNKNOWN | — | LOW |

**Notes**

- **Q2 is the closest question in the paper to full P coverage on the identity axis** — 7 of its 10 P
  objects already have stable ids. What is missing is small and specific: **reg 17.6**, the **MARPOL
  articles/Protocol I layer**, and **MSC.255(84)**.
- `SOLAS-XI1-6` was found during this survey and is a useful anchor the answer does not cite by
  number. It is genuine supporting authority for the investigation limb.
- Jurisdiction risk is **HIGH** and is a *content* constraint, not a corpus one: "foreign waters" is
  unnamed, so criminal exposure and permitted legal assistance stay conditional. **A corpus object
  must not be labelled in a way that resolves that conditionality.**
- Both civil-liability branches are needed because the question does not state whether the ship is a
  CLC ship or whether the oil is persistent. Build **both** `CLC1992-Articles-I` and the Bunkers
  articles; do not pick a branch.

---

## 6. Q3 — IACS structure, UR/UI/PR, and the RO Code

**Authority required:** IACS (charter, resolutions procedure, Blue Book); IMO (MSC/MEPC resolutions).

| Ref | Claim scope | Instrument · section | Relationship | Desired object id | ID | Corpus | Treat | Curr |
|---|---|---|---|---|---|---|---|---|
| **P1** | (a) 1 — Council, GPG, Panels, Permanent Secretariat; members must meet the Quality System Certification Scheme | IACS constitutional / organisational material; QSCS | DEFINITION | `IACS-Structure`, `IACS-QSCS` | **NONE** (org `iacs` registered as an explicit placeholder, zero content) | UNKNOWN | REFERENCE_PACK | LOW |
| **P2** | (a) 2 — UR is a minimum technical floor; UI is a common interpretation of an IMO instrument; PR is procedural; members implement in their own rules by a set date | IACS resolutions procedure — definitions of UR, UI, PR and incorporation timing | DEFINITION | `IACS-Resolutions-UR`, `-UI`, `-PR` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **P3** | (b) 5 — **RO Code Parts 1 and 2 are mandatory; Part 3 is guidelines for oversight** | RO Code, res. MSC.349(92) / MEPC.237(65), Parts 1, 2, 3 | PRIMARY_RULE | `ROCode-1`, `-2`, `-3` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **P4** | (b) 5 — mandatory from 1 January 2015 under SOLAS, MARPOL and Load Lines | res. MSC.350(92), MSC.356(92), MEPC.238(65) | LEGAL_BASIS | `ROCode-MandatoryBasis` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **P5** | (b) 6 — authorization agreement, initial assessment, periodic audit, surveyor qualification, PSC detention monitoring, withdrawal of authority | RO Code Part 2 and Part 3 (oversight) | PROCEDURE | `ROCode-2`, `-3` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **S1** | (b) 6 — IMSAS audits the Administration itself | III Code; SOLAS chapter XIII | SUPPORTING_RULE | `IIICode-…`; `SOLAS-XIII`, `SOLAS-XIII-3` | PARTIAL (SOLAS XIII exists; III Code not registered) | UNKNOWN | REFERENCE_PACK | LOW |
| **S2** | (b) 4 — delegation of function, never of responsibility | SOLAS I/6 (recognition and delegation) | LEGAL_BASIS | `SOLAS-I-6` | NONE (chapter `SOLAS-I` exists) | UNKNOWN | EXISTING_OBJECT | LOW |
| **C1** | current IACS membership | IACS membership list | CONTEXT | — | — | — | **do not build** | HIGH |

**Notes**

- The `iacs` organization is already registered in the repository with the note *"Placeholder
  registration only — no content authored yet. Exists to prove that adding a new organization is
  'add a folder', not a redesign."* **Q3 is the first real demand against that placeholder** — the
  intended proof case has arrived.
- **Availability is favourable.** IACS publishes URs, UIs and PRs openly; the RO Code resolutions are
  free IMO documents. No licensing gate, unlike IMSBC.
- **The membership count must stay out of the corpus as an assertable fact.** The answer deliberately
  does not state it because it changes. A corpus object that fixes a number here would create exactly
  the staleness the answer avoids.
- This is a **REFERENCE PACK, not a full-corpus project.** Q3 needs institutional definitions and
  three RO Code parts, not the IACS Blue Book in full.

---

## 7. Q4 — ECA fuel changeover

**Authority required:** IMO (MARPOL Annex VI and its amending MEPC resolutions; ECA designation record).

| Ref | Claim scope | Instrument · section | Relationship | Desired object id | ID | Corpus | Treat | Curr |
|---|---|---|---|---|---|---|---|---|
| **P1** | 1 — ECA limit 0.10% m/m | MARPOL Annex VI reg 14.4 | PRIMARY_RULE · NUMERIC_SOURCE | `MARPOL-VI-14-144` | **EXISTS** (also `MEPC32876-3-14` — see §2.2(a)) | UNKNOWN | EXISTING_OBJECT | MEDIUM |
| **P2** | 1 — global cap 0.50% m/m outside | MARPOL Annex VI reg 14.1 | NUMERIC_SOURCE | `MARPOL-VI-14-141` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **P3** | 6 — **written changeover procedure, and logbook record of tank quantities with date, time and position** on completion before entry and commencement after exit | MARPOL Annex VI reg 14.6 | PRIMARY_RULE | `MARPOL-VI-14-146` | **NONE** | UNKNOWN | FULL_CORPUS | MEDIUM |
| **P4** | 7 — grace period for newly designated ECAs | MARPOL Annex VI reg 14.7 | PRIMARY_RULE | `MARPOL-VI-14-147` | **NONE** | UNKNOWN | FULL_CORPUS | **HIGH** |
| **P5** | 1 — which areas are ECAs and from when: Mediterranean 1 May 2025; Canadian Arctic and Norwegian Sea in force 1 Mar 2026, limits bite 1 Mar 2027 | ECA designation record — Annex VI appendix III and the amending MEPC resolutions | NUMERIC_SOURCE | `MARPOL-VI-AppendixIII` + designation/version metadata | **NONE** | UNKNOWN | FULL_CORPUS | **HIGH** |
| **S1** | 3, 6 — fuel oil availability and quality; BDN and retained sample | MARPOL Annex VI reg 18 | SUPPORTING_RULE | `MEPC32876-3-18` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **S2** | 6 — an approved equivalent such as an EGCS may be used where fitted and accepted | MARPOL Annex VI reg 4 (equivalents); reg 14.8 (EGCS equivalence) | SUPPORTING_RULE | `MEPC32876-1-4`; `MARPOL-VI-14-148` | **EXISTS** (both) | UNKNOWN | EXISTING_OBJECT | LOW |
| **S3** | 8 — the changeover procedure must live in the SMS | ISM Code | SUPPORTING_RULE | `ISM-78` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **C1** | regional overlays (e.g. EU schemes) | named only as a category; **no specific regional requirement was verified** | CONTEXT | — | — | — | **do not build on Q4's account** | HIGH |
| **C2** | SEEMP | MARPOL Annex VI reg 26 | CONTEXT | `MARPOL-VI-26` | **EXISTS** | UNKNOWN | — | LOW |

**Notes**

- **`MARPOL-VI-14-146` is the single highest-value missing object in the entire paper.** It is Q4's
  `critical_regulation`; the record requirement is what the question is really testing; and its id
  sits one character from `MARPOL-I-14-146`, which already exists and means something else entirely.
  See §2.2(b).
- **FONAR is NOT demanded by Q4.** The session brief hypothesised it. The verified model answer never
  mentions it — the contingency limb says only that *"an approved equivalent such as an exhaust gas
  cleaning system may be used where fitted and accepted"*. Recorded here so the corpus track does not
  build a FONAR object on QP2607's authority. (A DGMA FONAR corrigendum shell is registered with zero
  nodes; it stays out of scope for July.)
- **SEEMP is a route cue that the model answer does not assert.** Route step 8 lists it; the answer's
  statutes limb cites ISM, SOLAS and regional requirements. Classified C. No corpus work for July.
- **Currency is the story of this question.** The ECA list changed twice in eighteen months and the
  Canadian Arctic / Norwegian Sea limits bite on 1 March 2027. **P5 is not a text object — it is a
  dated designation register**, and it must carry effective-from/effective-to state or it will be
  quietly wrong within the year. This is the strongest argument for MARPOL Annex VI ranking first.

---

## 8. Q5 — Particular Average, General Average, average adjusters

**Authority required:** Government of India (Marine Insurance Act 1963); Comité Maritime International
(York-Antwerp Rules 2016 — **CMI copyright, check redistribution terms**).

| Ref | Claim scope | Instrument · section | Relationship | Desired object id | ID | Corpus | Treat | Curr |
|---|---|---|---|---|---|---|---|---|
| **P1** | 2 — statutory definition of general average loss | Marine Insurance Act 1963 (India) s.66 | PRIMARY_RULE | `MIA1963-66` | **NONE** (no Indian insurance statute is registered) | UNKNOWN | REFERENCE_PACK | LOW |
| **P2** | 3 — **all Rule A elements must be present**: extraordinary sacrifice or expenditure, intentionally and reasonably made, in time of peril, for the common safety | York-Antwerp Rules 2016, Rule A | PRIMARY_RULE | `YAR2016-RuleA` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **P3** | 5 — **the YAR are not law**; they apply contractually when the bill of lading or charterparty incorporates a named edition | YAR 2016 — status and incorporation; CMI adoption record, New York, May 2016 | LEGAL_BASIS | `YAR2016-Status` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **S1** | 1 — particular average as a partial loss | Marine Insurance Act 1963 s.64 (partial loss) | DEFINITION | `MIA1963-64` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **S2** | 4 — the adjuster secures the GA bond and guarantee, allows or disallows sacrifices, apportions contribution, is independent — and **does not declare GA; the shipowner does** | authoritative average-adjusting practice material | PROCEDURE | `AverageAdjusting-Practice-…` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **C1** | GA in practice | *Maersk Honam* and comparable casualties | CONTEXT | — | — | — | do not build | LOW |

**Notes**

- **Q5's statutory anchor is Indian.** Cite the Marine Insurance Act 1963. See Q9 — the two questions
  share the same statute and should share the same corpus objects.
- **S1 is a proposal, not a verified citation.** The model answer defines particular average without
  citing a section; s.64 is the natural statutory anchor. **The corpus track must confirm it against
  the Act before any shelf entry claims it.** Recorded here rather than asserted.
- **P3 must survive into every derived label.** "York-Antwerp Rules" reads like an instrument with
  force of law and is not one. A corpus object that omits the contractual-only status will produce
  derived layers more categorical than the answer — the exact failure `SEMANTIC_GUARDS` exists to stop.
- **S2 has no statutory source.** The adjuster's role rests on practice, not legislation. Either the
  corpus supplies an authoritative practice source or the claim stays industry-grade and no shelf
  entry should imply otherwise.
- **Do not build a general marine-insurance corpus for one question.** A compact pack of the sections
  Q5 and Q9 actually use is the right size.

---

## 9. Q6 — Green ammonia: IC engines versus fuel cells

**Authority required:** IMO (MSC circular, SOLAS, IGF/IGC Codes).

| Ref | Claim scope | Instrument · section | Relationship | Desired object id | ID | Corpus | Treat | Curr |
|---|---|---|---|---|---|---|---|---|
| **P1** | 5 — **MSC.1/Circ.1687 interim guidelines are NON-mandatory** | MSC.1/Circ.1687, 26 Feb 2025, approved at MSC 109 | PRIMARY_RULE (guidance) | `MSC1Circ1687-…` | **NONE** | UNKNOWN | REFERENCE_PACK | **HIGH** |
| **P2** | 5 — approval route is alternative design and arrangements | SOLAS II-1/55 | LEGAL_BASIS | `SOLAS-II1-55` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **P3** | 5 — IGF Code prescriptive text was written for natural gas and does not prescriptively cover ammonia | IGF Code — scope and application | DEFINITION | `IGFCode-1` scope node | PARTIAL (`igf-code`, 59 nodes — confirm a scope node) | UNKNOWN | EXISTING_OBJECT | MEDIUM |
| **S1** | 3 — toxicity dominates the risk case; refrigerated containment near −33 °C; copper alloys attacked | authoritative ammonia safety/technical guidance | NUMERIC_SOURCE | `AmmoniaSafety-…` | NONE | UNKNOWN | REFERENCE_PACK | MEDIUM |
| **C1** | gas carriers using **cargo** as fuel — a **different regime**, study guide only | IGC Code ch.16, as amended by MSC.566(109), in force 1 Jul 2026 | CONTEXT | `IGCCode-16` | **EXISTS** | UNKNOWN | — | MEDIUM |

**Notes**

- **Recommendation: register the objects, defer the content.** MSC 111 (May 2026) is reported to have
  approved a set of ammonia interim guidelines, and it is not yet confirmed whether MSC.1/Circ.1687
  was superseded or renumbered. A further revision is expected at CCC 12. **The answer cites that
  circular by number**, so building consolidated content now risks encoding a superseded number into
  the one layer whose whole purpose is to be trustworthy. Register `MSC1Circ1687-…` with a
  supersession watch; build the text once MSC 111's outcome is confirmed. This is the paper's class B
  currency flag for Q6.
- **C1 is a live confusion risk, and the answer already guards against it.** IGC chapter 16 governs
  *gas carriers burning their own cargo*; it is not the regime for a non-gas-carrier bunkering
  ammonia. `IGCCode-16` exists and is easy to reach for. **A shelf label must not let it drift into
  the P-set.**
- **No numeric ammonia values are asserted anywhere in the answer** — toxicity exposure limits,
  flammability range, autoignition temperature, energy-density ratio and N₂O GWP were all deliberately
  left out as unverified. S1 would *enable* a future revision; it does not substantiate the current
  answer. Do not treat it as P.
- `SOLAS-II1-55` already existing is a real convenience: the load-bearing legal route for the whole
  question resolves today on the identity axis.

---

## 10. Q7 — Merchant Shipping Act, 2025

**Authority required:** Government of India — Gazette of India (Act and commencement notification).
**Both primary texts have already been read in full** and are documented in `verification/QP2607/Q7.md`.

| Ref | Claim scope | Instrument · section | Relationship | Desired object id | ID | Corpus | Treat | Curr |
|---|---|---|---|---|---|---|---|---|
| **P1** | 1 — Act No. 24 of 2025, assent 18 Aug 2025; 325 sections in 16 Parts; s.1(2) expressly permits different dates for different provisions | Merchant Shipping Act 2025 — long title, s.1(2) | LEGAL_BASIS | `MSAct2025-1-2` | **NONE** (`dgma-merchant-shipping-act-2025` registered, **zero nodes**) | **IN HAND** | REFERENCE_PACK | LOW |
| **P2** | 1 — **the whole Act came into force 15 March 2026; the staging power was not exercised** | S.O. 1244(E), 10 March 2026 | LEGAL_BASIS | `SO1244E-2026` | **NONE** | **IN HAND** | REFERENCE_PACK | LOW |
| **P3** | 2 — ownership widened to NRIs and OCIs; OCI-wholly-owned not required to register | s.15(1), s.15(2) | PRIMARY_RULE | `MSAct2025-15-1`, `-15-2` | NONE | **IN HAND** | REFERENCE_PACK | MEDIUM |
| **P4** | 2 — bareboat charter-cum-demise registration | s.16 | PRIMARY_RULE | `MSAct2025-16` | NONE | **IN HAND** | REFERENCE_PACK | MEDIUM |
| **P5** | 2 — temporary registration for recycling | s.17 | PRIMARY_RULE | `MSAct2025-17` | NONE | **IN HAND** | REFERENCE_PACK | MEDIUM |
| **P6** | 4 — minimum age for employment on board is sixteen | s.59 | NUMERIC_SOURCE | `MSAct2025-59` | NONE | **IN HAND** | REFERENCE_PACK | LOW |
| **P7** | 1 — **repeals the 1958 Act (except Part XIV, but not including s.411A) and the Coasting Vessels Act 1838**; s.325 consequential amendment | s.324(1), s.325 | LEGAL_BASIS | `MSAct2025-324-1`, `-325` | NONE | **IN HAND** | REFERENCE_PACK | LOW |
| **S1** | 4 — the long title's treaty-compliance purpose; **MLC 2006 is named in the Act; the IMO is not** | Act long title; MLC 2006 | SUPPORTING_RULE | `MSAct2025-LongTitle`; `mlc-2006` nodes | PARTIAL (`mlc-2006`, 8 nodes) | UNKNOWN | REFERENCE_PACK | LOW |
| **S2** | 1 — what was repealed | Merchant Shipping Act 1958 | CONTEXT | `ms-act-1958` | PARTIAL (registered, **zero nodes**) | UNKNOWN | REFERENCE_PACK | LOW |
| **C1** | 5 — tonnage growth, FDI, ease of doing business | Government policy material (RIS and similar) | CONTEXT | **keep out of the statutory corpus** | — | — | do not build | HIGH |

**Notes**

- **This is the cheapest complete win in the map.** The standard shell is already registered with the
  correct id and full descriptive metadata; the Gazette text of both the Act and the commencement
  notification has already been read and documented; and only the section nodes are missing.
- **The law/policy separation is load-bearing.** The answer's fifth route step is precisely *what the
  Act legally does* versus *what Government expects it to achieve*. **C1 must never enter the
  statutory corpus.** If policy material is held at all, it belongs in a clearly separate class that
  no shelf entry can present as statutory.
- **One correction already made, worth carrying forward:** the Act **never names the IMO** (0
  occurrences). Any corpus summary asserting IMO alignment would reintroduce a defect this product
  has already fixed.
- **Currency: MEDIUM, and it is not the Act.** The statutory facts are settled. What is fluid is the
  subordinate Merchant Shipping Rules 2026, still in draft as at August 2026 — the question's class B
  flag. The corpus should be able to express "Act in force, rules pending".
- Retrieval lesson recorded in `CURRENT_STATUS.md` §8 and worth reusing: **India Code returns HTTP 403
  to automated fetch. Use `shipmin.gov.in` and `dgma.gov.in`.**

---

## 11. Q8 — Competence versus performance, and automation

**Authority required:** IMO (STCW Convention and Code, ISM Code, Assembly resolution).

| Ref | Claim scope | Instrument · section | Relationship | Desired object id | ID | Corpus | Treat | Curr |
|---|---|---|---|---|---|---|---|---|
| **P1** | (a) 1 — **training and assessment administered, supervised and monitored** | STCW regulation I/6 | PRIMARY_RULE | `STCW-I-6` | **NONE** (chapter `STCW-I` exists; only `STCW-I-11` beneath it) | UNKNOWN | REFERENCE_PACK | LOW |
| **P2** | (a) 1 — the standard against which competence is assessed | STCW Code section A-I/6 | PRIMARY_RULE | `STCWCodeA-I-6` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **P3** | (a) 1 — competence is demonstrated ability against stated criteria | STCW Code part A competence tables | DEFINITION | `STCWCodeA-III-2` etc. | PARTIAL (`STCW-III-2`, `-III-3` exist at *regulation* level; Code part A tables do not) | UNKNOWN | REFERENCE_PACK | LOW |
| **P4** | (a) 4 — drill programmes and emergency preparedness | ISM Code element 8 | SUPPORTING_RULE | `ISM-78` | **EXISTS** (merged with 7) | UNKNOWN | EXISTING_OBJECT | LOW |
| **P5** | (a) 4 — reports and analysis close the loop | ISM Code element 9 | SUPPORTING_RULE | `ISM-9` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **S1** | (a) 3 — resources, personnel and familiarisation | ISM Code element 6 | SUPPORTING_RULE | `ISM-6` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **S2** | (b) 6 — human-centred design; training matched to the equipment fitted; honest reporting culture | res. A.947(23), 27 Nov 2003 (superseding A.850(20)) | SUPPORTING_RULE | `A94723-…` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **S3** | (a) 3 — fatigue and hours of rest | STCW VIII/1 fitness for duty | SUPPORTING_RULE | `STCW-VIII-1` | **EXISTS** | UNKNOWN | EXISTING_OBJECT | LOW |
| **C1** | (b) 5 — automation bias, mode confusion, skill fade, out-of-the-loop decrement | human-factors research literature | CONTEXT | **not a regulatory object** | — | — | do not build | LOW |
| **C2** | — | MASS regulatory work | CONTEXT | — | — | — | do not build | HIGH |

**Notes**

- **Q8's `critical_regulation` — STCW I/6 with Code A-I/6 — does not exist on the identity axis.** The
  STCW registration is shallow: 12 nodes, all in chapters I, III, V and VIII, with nothing at I/6 and
  no Code part A layer at all.
- `STCW-VIII-1` already existing is a genuine find: it is the authority behind the answer's
  fatigue-and-hours-of-rest proposition, which the answer makes without citing it.
- **C1 is deliberately non-regulatory and the answer labels it as such.** The automation
  failure-mode taxonomy is research, not a binding instrument. **Do not ingest it as corpus objects.**
  If it is held at all, it must be in a class no shelf entry can present as regulatory.
- **Reuse value is high and disproportionate to July coverage.** STCW is examined constantly across
  MEO orals and the Question Bank. One question drives the demand; many will consume the result.

---

## 12. Q9 — Uberrimae fidei and disclosure

**Authority required:** Government of India — Marine Insurance Act, 1963.

| Ref | Claim scope | Instrument · section | Relationship | Desired object id | ID | Corpus | Treat | Curr |
|---|---|---|---|---|---|---|---|---|
| **P1** | 2 — utmost good faith; **mutual**, binding on both parties; remedy is avoidance | Marine Insurance Act 1963 s.19 | PRIMARY_RULE | `MIA1963-19` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **P2** | 3 — every material circumstance known to the assured; deemed knowledge in the ordinary course of business | s.20(1), s.20(2) | PRIMARY_RULE | `MIA1963-20-1`, `-20-2` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **P3** | 4 — **the four categories which need not be disclosed in the absence of enquiry** — required verbatim | s.20(3) | PRIMARY_RULE | `MIA1963-20-3` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **P4** | 5 — insurer may avoid; avoidance is ab initio; the contract is voidable, not void; non-disclosure need not be fraudulent | s.19, s.20 read together | LEGAL_BASIS | `MIA1963-19`, `MIA1963-20` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **S1** | 3 — materiality is a question of fact in each case | s.20(4), s.20(5) | SUPPORTING_RULE | `MIA1963-20-4`, `-20-5` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **S2** | 3 — disclosure by an agent; representations pending the contract | s.21, s.22 | SUPPORTING_RULE | `MIA1963-21`, `MIA1963-22` | **NONE** | UNKNOWN | REFERENCE_PACK | LOW |
| **C1** | contrast only, **study notes only, expressly not applied to Indian law** | UK Marine Insurance Act 1906; UK Insurance Act 2015 | CONTEXT | separate jurisdiction class | — | — | build only with a hard jurisdiction flag | LOW |

**Notes**

- **This is the paper's declared jurisdiction trap, and it has already produced a real defect.**
  `meoclass1/QB9_C.html` attributes these principles to the **UK Marine Insurance Act 1906** — the
  wrong statute for an Indian examination. The cross-link was removed from Q9 and the caution now
  lives as study-guide prose.
- **Therefore the corpus requirement is not merely "hold the 1963 Act".** It is: **hold the Indian Act
  with a jurisdiction property strong enough that no resolver, label or derived layer can substitute
  the 1906 Act for it.** C1 may be held for contrast; it must be unmistakably a different jurisdiction.
- **Q9 and Q5 share one statute.** Build `MIA1963-*` once. Sections needed across both:
  **19, 20(1)–(5), 21, 22, 64 (to confirm), 66.** That is a small, bounded, stable object set covering
  **two of nine July questions**.
- No Indian case law was verified for this build and none is needed; the statutory text answers the
  question as asked. Do not expand scope into case law on July's authority.

---

## 13. Existing object coverage — the aggregate picture

Identity axis, verified against `RulesApp/repository/index/repo-data.json` on 2026-08-08.

| Question | P objects | ID EXISTS | PARTIAL | NONE | Comment |
|---|---|---|---|---|---|
| Q1 | 7 | 3 | 2 | 2 | IMSBC schedules licence-blocked; SOLAS XII/12 absent |
| Q2 | 10 | 6 | 0 | 4 | Best-covered question in the paper |
| Q3 | 5 | 0 | 0 | 5 | Nothing exists — IACS is a placeholder, RO Code unregistered |
| Q4 | 5 | 2 | 0 | 3 | The three missing are the ones the answer leans on hardest |
| Q5 | 3 | 0 | 0 | 3 | No Indian insurance statute, no YAR |
| Q6 | 3 | 1 | 1 | 1 | `SOLAS-II1-55` present; the circular is the gap |
| Q7 | 7 | 0 | 0 | 7 | Shell registered with zero nodes; **primary text in hand** |
| Q8 | 5 | 2 | 1 | 2 | STCW I/6 and Code A-I/6 absent |
| Q9 | 4 | 0 | 0 | 4 | Nothing exists |
| **Total** | **49** | **14** | **4** | **31** | **≈29% of primary demand has a stable identity today** |

### What is already available and directly usable

`SOLAS-VI-2` · `SOLAS-VI-7` · `SOLAS-XII-11` · `SOLAS-II1-55` · `SOLAS-XI1-6` · `SOLAS-XIII` ·
`MARPOL-I-17` · `MARPOL-I-37` · `MARPOL-I-37-371` · `MARPOL-I-37-372` · `MARPOL-VI-14` ·
`MARPOL-VI-14-141` · `MARPOL-VI-14-144` · `MARPOL-VI-14-148` · `MEPC32876-1-4` · `MEPC32876-3-18` ·
`BunkerConvention2001-Articles-12` · `-3` · `-7` · `CLC1992-Articles-I` · `ISM-6` · `ISM-78` ·
`ISM-9` · `STCW-VIII-1` · `IGCCode-16` · `mlc-2006` nodes

### PRIORITY 0 — eight single-node additions to instruments already registered

The largest coverage gain per unit of effort in this entire map, and it is not a "pack" at all:

| Object | Instrument already registered | Serves | Why it matters |
|---|---|---|---|
| `MARPOL-VI-14-146` | `marpol-73-78` | **Q4 P3** | Q4's `critical_regulation`. The record requirement the question is really testing. |
| `MARPOL-VI-14-147` | `marpol-73-78` | **Q4 P4** | The grace-period rule behind the 1 Mar 2027 cliff |
| `MARPOL-I-17-176` | `marpol-73-78` | **Q2 P2** | Q2's `critical_regulation` — ORB evidential admissibility |
| `SOLAS-XII-12` | `solas-1974` | **Q1 P7** | Three examinable numbers; chapter XII already present |
| `SOLAS-I-6` | `solas-1974` | Q3 S2 | Delegation to an RO |
| `STCW-I-6` | `stcw-1978` | **Q8 P1** | Q8's `critical_regulation` |
| `BunkerConvention2001-Articles-4` | `bunker-convention-2001` | Q2 S1 | The CLC carve-out that bounds the Bunkers regime |
| `IMSBCCode-4-42` | `imsbc-code` | **Q1 P4** | Declaration content and the BCSN |

**Five of these eight are a `critical_regulation` or carry examinable numbers.** They require no new
standard registration, no new organization and no new id convention — only source content and nodes.
Doing these first converts a large share of the paper from NONE to EXISTS.

---

## 14. Corpus priority — full corpus

Ranked on July coverage, cross-product reuse, technical/numeric risk, currency burden, source
availability and build efficiency. **The session hypothesis (VI, I, IMSBC) survives — but the reasons
differ from those proposed, and one scheduling change follows.**

### PRIORITY 1 — MARPOL ANNEX VI

| Criterion | Assessment |
|---|---|
| July coverage | **Q4 (P, heavily) + Q2 (S)** — the only full-corpus candidate touching two questions |
| Future reuse | **Very high** — sulphur, NOx, EEXI, CII, SEEMP, EGCS recur across written, oral and QB |
| Technical/numeric | **High** — 0.10 / 0.50 % m/m, ECA boundaries and dates |
| Currency burden | **Highest in the paper** — ECA list changed twice in 18 months; limits bite 1 Mar 2027 |
| Build efficiency | Reconciliation, not greenfield — partial content already exists under **two competing ids** |

**Rationale.** It combines the heaviest currency burden with the paper's most valuable missing object
(`MARPOL-VI-14-146`), and it is the only instrument carrying an active **registry ambiguity** (§2.2(a)).
That ambiguity makes it the one instrument where doing nothing is not neutral: a reference populated
today could bind to either vocabulary.

**Deliver:** resolve the `marpol-73-78` / `mepc-328-76` duplication and declare a canonical id; add
regs **14.6** and **14.7**; build the **ECA designation register** as dated version state, not prose.

### PRIORITY 2 — MARPOL ANNEX I

| Criterion | Assessment |
|---|---|
| July coverage | **Q2 (P)** |
| Future reuse | **Very high** — ORB, OWS, 15 ppm, SOPEP, discharge criteria are core MEO material |
| Technical/numeric | **High** — 15 ppm, 150/400 GT thresholds |
| Currency burden | **Low** — all instruments long in force and stable |
| Build efficiency | **Best in class** — regs 12, 14, 15, 17, 19, 31, 37 already carry sub-nodes |

**Rationale.** Ranked second on *buildability*, not on demand. It has the strongest existing coverage
of any instrument in this map and the smallest remaining gap — essentially **reg 17.6 plus the MARPOL
articles/Protocol I layer**. It is the fastest route to a question that is fully substantiated
end to end, which is the thing worth proving before scaling.

**Deliver:** add **17.6**; add the **articles and Protocol I** layer (the registry currently holds
annex regulations only); complete Annex I to the depth already set by regs 31 and 37.

### PRIORITY 3 — IMSBC CODE — *acquire now, build when licensed*

| Criterion | Assessment |
|---|---|
| July coverage | **Q1 (P)** |
| Future reuse | High for cargo questions; narrower than Annex I/VI for engineering management |
| Technical/numeric | **Highest integrity value in the map** — this is where a real regression occurred |
| Currency burden | **High** — 07-23 mandatory; 08-25 voluntary 1 Jan 2026, mandatory 1 Jan 2027 |
| Build efficiency | **Poor, and gated** — Appendix 1 is a large body of schedules, and **MIW holds no licensed Code** |

**Rationale — and the one change to the hypothesis.** On *value* IMSBC arguably outranks both MARPOL
annexes: it is the only instrument in this map that has already caused a semantic defect, and Q1's
class C limitation cannot be closed without it. But it is the **only demand in the entire map behind a
licensing gate**, and it is the largest build. Ranking it third is therefore a statement about
*sequencing*, not importance.

**Do not let it block Priorities 1 and 2. Start the acquisition immediately and in parallel** —
acquiring the 2023 (07-23) and 2025 (08-25) editions is the long-lead item and the highest-value
unblock for every future cargo question.

**Deliver, once licensed:** §4.2; **named individual schedules** as addressable objects (IRON ORE,
IRON ORE FINES, IRON ORE PELLETS, DIRECT REDUCED IRON (B)); BCSN and amendment state as **first-class
properties**, never as prose.

---

## 15. Corpus priority — reference packs

Ranked on July P-weight, cross-product reuse and buildability. All are compact and governed; none
should become a full-book project.

| # | Pack | Serves | P objects | Why here |
|---|---|---|---|---|
| **1** | **Merchant Shipping Act 2025** — Act, S.O. 1244(E), ss.1(2), 15, 16, 17, 59, 324(1), 325 | **Q7** | **7 of 7** | Shell already registered with correct id; **both primary Gazette texts already read in full**; highest Indian-law reuse across QB and orals. Cheapest complete question in the map. |
| **2** | **Marine Insurance Act 1963** — ss.19, 20(1)–(5), 21, 22, 64, 66 | **Q5 + Q9** | **4 of 7 across two questions** | **The only pack serving two July questions.** Jurisdiction-critical, with a known live defect (QB9_C cites the UK 1906 Act). Few sections, stable, public text. |
| **3** | **IACS + RO Code** — IACS structure, QSCS, UR/UI/PR definitions; RO Code Parts 1–3; the mandating resolutions | **Q3** | **5 of 5** | Q3 has **zero** existing coverage. Both sources are openly published — no licensing gate. `iacs` placeholder exists precisely for this. |
| **4** | **IMO FSA Guidelines** — MSC-MEPC.2/Circ.12/Rev.2, incl. para 1.3.1 | **Q1(a)** | **2 of 7** | **One circular.** Smallest possible build, and it closes half of Q1 **without touching IMSBC licensing**. Carries Q1's `critical_regulation`. |
| **5** | **STCW I/6 + Code A-I/6 + human element** — plus res. A.947(23) | **Q8** | **3 of 5** | Q8's `critical_regulation` is absent. STCW reuse across orals and QB is disproportionate to July coverage. |
| **6** | **Q2 completion** — Bunkers art 4; Casualty Investigation Code MSC.255(84); res. A.851(20); res. LEG.3(91) | **Q2** | 4 remaining | Small and additive; Q2 is already 6 of 10 covered. Finishes the paper's best-covered question. |
| **7** | **York-Antwerp Rules 2016** — Rule A, status/incorporation, adjusting practice | **Q5** | 2 of 3 | Needed for Rule A, but **contractual, not law**, and CMI copyright applies. Must carry a hard "not law" status flag. |
| **8** | **Ammonia** — MSC.1/Circ.1687 and ammonia safety guidance | **Q6** | 1 of 3 | **Register the object with a supersession watch; defer the content.** MSC 111 may have superseded or renumbered the circular the answer cites by number, and CCC 12 revision is expected. Building now risks encoding a stale number. |

---

## 16. FSS and LSA — no direct July demand

The corpus track holds FSS and LSA work at various stages. **It was not imported, referenced or
inspected in this session.**

Checked against all nine verified answers:

> **NO DIRECT JULY DEMAND.**

No QP2607 question turns on a fire-safety-systems or life-saving-appliance provision. Q2's emergency
limb is muster and containment under SOPEP and the SMS, not an LSA or FSS requirement. Nothing in
Q1–Q9 cites the FSS Code or the LSA Code.

`fss-code` (69 nodes) and `lsa-code` (35 nodes) are registered in the relationship repository and
remain valuable for other QB, oral and RulesApp uses. **They are simply not on July's critical path,
and no connection should be manufactured to justify the work already done.**

---

## 17. Reference shelf — deferred, deliberately

`QP2607.json` carries **zero** `reference_shelf` entries and **must continue to**, until a real,
resolvable canonical object is confirmed in the True Source layer.

**No pending or placeholder entries are to be created.** `MIW_TRUE_SOURCE_CONTRACT.md` §8 provides
for `REFERENCE_PENDING`, but nothing in the design requires demonstration placeholders, and a shelf
populated to show off the feature is precisely the dead "Verify source" control §8 exists to prevent.

**This demand map is the handoff. The QP spec stays clean.**

The seam is one function — `reference_href()` in `build_paper.py`. When the resolver lands, that
function changes and nothing else does. The toolchain has **no corpus-file dependency** and must
acquire none.

---

## CORPUS TEAM — NEXT ACTION

A production sequence. Interface only — the corpus track owns its own toolchain.

1. **Confirm source availability and licensing** for the Priority 1–3 instruments and the eight
   Priority-0 nodes. **Start IMSBC Code acquisition (07-23 and 08-25) immediately and in parallel** —
   it is the long-lead item and blocks nothing else.
2. **Resolve the MARPOL Annex VI registry ambiguity** (§2.2(a)). Declare one canonical id, alias the
   other. Nothing on Q4 should be populated before this.
3. **Build PRIORITY 0** — the eight single-node additions in §13. Highest coverage gain per unit of
   effort; five of the eight are a `critical_regulation` or carry examinable numbers.
4. **Build reference packs 1–3** (§15): Merchant Shipping Act 2025 → Marine Insurance Act 1963 →
   IACS + RO Code. These complete Q7, Q5, Q9 and Q3.
5. **Build full corpus in priority order** (§14): MARPOL Annex VI → MARPOL Annex I → IMSBC when
   licensed.
6. **Emit a canonical object index** — object id → instrument → edition → consolidated state →
   effective/current-through → exact destination → provenance → verification status.
7. **Return the object mappings to the QP track**, as `question_id` → `object_id` with a
   `claim_scope`, using the §3 vocabularies.
8. **QP track populates `reference_shelf`** and re-runs the toolchain. Only real, resolvable objects.
9. **Resolver and viewer validate exact-section landing** — never "page 1 of the Annex, go and search".

### Constraints that hold throughout

- **Never expose the QP layer to PDF page numbers, local paths or generated PDF filenames.** Object
  ids must survive repagination, consolidated amendments and replacement editions.
- **Reuse the established ID convention.** No `::` separators, no parallel vocabulary.
- **Semantic integrity applies to the corpus too.** A label, title or summary may never be more
  categorical than the source. `pellets = Group C` is the worked example of what not to do.
- **Keep law separate from policy** (Q7) and **jurisdiction unmistakable** (Q9).
- **State amendment and currency as structured state**, not prose — Q4's ECA dates and Q1's IMSBC
  edition are both time-bombs otherwise.
