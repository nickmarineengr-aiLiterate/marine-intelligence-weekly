# Known Traps & Standing Corrections — Past Written Papers

Same purpose and format as `meoclass1/known_traps.md`: verified-correct facts that have
already been drafted wrong at least once in this series. Every new paper is checked
against this list before HTML is built — not recalled from memory.

Each entry carries a `GREP:` line. `known_traps_check.py` auto-scans only entries whose
`GREP:` gives a phrase that is unambiguous out of context and therefore safe to flag
wherever it appears. Where the wrong form uses words that are also legitimate in other
contexts, the entry is marked `GREP: SKIP` and stays manual-review-only — the checker
handles those, where it can, as a structural check against the spec instead.

Do not add brittle regex policing of nuanced legal prose. If a rule needs judgement,
mark it SKIP and leave it to the verification pass.

---

### 1. Bunkers Convention — liability is NOT confined to the registered owner
Article 1(3) defines "ship-owner" as the owner, **including the registered owner,
bareboat charterer, manager and operator**. Article 3 makes them liable jointly and
severally. Article 7(1) separately puts the **compulsory insurance** duty on the
**registered owner** alone, for ships over 1,000 GT. Liability and the insurance
obligation attach to different persons. Found in QP2607 Q2 v0.1 (red-team RT-07).

**Scope warning — added during QP2601 production, 2026-08-08.** This GREP phrase is
*not* wrong in every context. Liability **is** on the registered owner under the
**Nairobi Wreck Removal Convention 2007**, and CLC 1992 **channels** liability to the
registered owner. QP2601 Q4 tripped this trap with a sentence about Nairobi that was
correct. The phrase was left auto-scanned at full strength and the QP2601 wording was
changed instead — "makes the registered owner strictly liable" — so no protection was
given up.

If a later paper hits this again on a correct Nairobi or CLC statement, that is
evidence the phrase belongs at `GREP: SKIP`, with trap 2 — which carries the
Bunkers-qualified wording — remaining the auto-scanned form. Do not make that change
on one paper's evidence.
GREP: strict liability on the registered owner

### 2. Bunkers Convention — same error, other phrasings
GREP: Bunkers Convention imposes strict liability on the registered owner

### 3. CLC applicability must not be stated absolutely
CLC 1992 Art I(5) covers persistent oil "whether carried on board a ship as cargo **or in
the bunkers of such a ship**", and Bunkers Convention Art 4(1) excludes itself where the
damage is CLC pollution damage. So a bunker spill from a CLC ship IS CLC damage. Whether
CLC applies turns on two facts: is she a CLC ship, and is the oil persistent. Found in
QP2607 Q2 v0.1 (red-team RT-08).
GREP: CLC 1992 does not apply

### 4. CLC — same error, other phrasing
GREP: CLC does not apply to a bunker spill

### 5. Casualty Investigation Code is not engaged by every pollution incident
A **mandatory** marine safety investigation under Part II chapter 6 is required only for a
**very serious marine casualty** — total loss of the ship, a death, or severe damage to
the environment (§2.22). Marine casualties short of that, and marine incidents, fall under
Part III **recommended practice** (chapter 17). The environmental limb of §2.9.7 also
requires damage "brought about by the damage of a ship". A bunker overflow from an intact
ship is usually a **marine incident**. Found in QP2607 Q2 v0.1 (red-team RT-06).
GREP: SKIP

### 6. Iron ore pellets are not iron ore fines — and the split is not a clean binary
IRON ORE, IRON ORE FINES, IRON ORE PELLETS and DIRECT REDUCED IRON (B) are separate IMSBC
schedules in different Groups, and "pellets" appears in the DRI (B) schedule name too.
The fines schedule itself carries qualifying criteria (goethite content, particle size
distribution) under which fines may be carried as Group C. The declared Bulk Cargo
Shipping Name and its individual schedule govern — never the commodity name. Found in
QP2607 Q1 v0.1 (red-team RT-03).
GREP: SKIP

### 7. Do not state a TML for a Group C cargo
TML is a Group A concept. A Group C cargo does not have one; if a TML is being offered for
your cargo, question the classification rather than accept the figure.
GREP: SKIP

### 8. Indian marine insurance answers must cite the Marine Insurance Act, 1963
The examination is Indian. The governing statute is the **Marine Insurance Act, 1963** —
s.19 utmost good faith, s.20 disclosure, s.66 general average loss. The UK Marine
Insurance Act 1906 is its model but is **not** the operative statute, and the UK Insurance
Act 2015 reform of the avoidance remedy does **not** apply to Indian law. Note that
`meoclass1/QB9_C.html` attributes the principles to the 1906 Act — do not lift from it.
GREP: SKIP

### 9. Ammonia interim guidance is NOT a mandatory IGF Code amendment
MSC.1/Circ.1687 (26 February 2025), *Interim Guidelines for the Safety of Ships using
Ammonia as Fuel*, approved at MSC 109, is **non-mandatory**. The IGF Code's prescriptive
provisions were written for natural gas; approval proceeds through the alternative design
route in SOLAS II-1/55. Do not describe the interim guidelines as IGF Code text.
GREP: mandatory IGF Code requirements for ammonia

### 10. Ammonia is not a zero-emission fuel
No carbon in the molecule means no direct CO2. It does not mean zero emissions: N2O and
ammonia slip are emissions, and lifecycle GHG depends on the production pathway.
GREP: SKIP
NOTE: the phrase legitimately appears in study notes where the answer refutes it
("Is ammonia a zero-emission fuel? No."), so it fails this file's own
unambiguous-out-of-context rule. Structural check instead.

### 11. Merchant Shipping Act 2025 claims are time-sensitive
Act No. 24 of 2025, assent 18 August 2025, in force 15 March 2026 by S.O. 1244(E) of
10 March 2026. Repeals the MS Act 1958 (saving Part XIV, not s.411A) and the Coasting
Vessels Act 1838. The **scope** of commencement and any provision-level citation must
carry a re-verification flag until confirmed against the Gazette. Never invent section
numbers of the 2025 Act.
GREP: SKIP

### 12. HATC coaching notes are never a verification source
`Notes-for-written-answers/` is HATC material whose own footer states that certain
statements and figures were **intentionally made wrong**. Discovery and question-scope
evidence only. Never authority, never verification, never reproduced.
GREP: SKIP
NOTE: naming HATC in order to record that it was NOT used is correct and expected,
so a bare phrase match is wrong. Enforced structurally: no HATC reference may
appear in a question's `sources` list.

### 13. Source provenance must not be overstated
The held paper PDFs are aggregator-hosted copies, not official publications. Do not claim
an official DG Shipping or MMD source unless an independently authoritative copy has
actually been compared.
GREP: official DG Shipping PDF

### 14. Third-party host branding must never appear in the product
Previously scoped to generated HTML only, on the reasoning that the spec and manifest
should record host provenance verbatim. That reasoning does not survive the fact that
**this repository is public**: a host name in a spec is a published brand trace just as
much as one in a page. The host identity now lives only in
`verification/LOCAL_SOURCE_PROVENANCE.md`, which is git-ignored. The scan therefore
covers generated pages, specs and the manifest alike.
GREP: dieselship

### 16. A derived learning layer must never out-state its source answer
**Structural consistency is not semantic consistency.** The route, core points, knowledge
map, flashcards, Quick Revision, Rapid Revision and memory cues are all *derived*
representations of a verified answer. The failure mode is that a nuanced conditional
statement gets flattened into a categorical one on the way out.

Found for real in Q1: the model answer said iron ore pellets are "carried as Group C ... but
establish that from the declared BCSN and its current individual schedule", while a route
core point, `recall_15s`, `major_trap` and a flashcard all said flatly **"pellets are
Group C"**. `recall_15s` even contradicted itself inside one field. That is precisely the
simplification earlier red-teaming rejected, and it also overstated provenance: the group
rests on authoritative-secondary sources and is recorded as a class C limitation.

Founder policy: **IMSBC cargo classification and carriage requirements follow the declared
BCSN and its current applicable individual schedule, not the casual commodity name used in
the examination question.**

Every derived layer must preserve scope, conditions, uncertainty, jurisdiction,
applicability and regulatory status. Enforced structurally by `SEMANTIC_GUARDS` in
`validate_spec.py`, which scans the derived fields only -- the model answer and study guide
are the source and are allowed to carry the full conditional sentence.
GREP: pellets are Group C
SCOPE: product

### 15. Stale build-state terminology
Once a question's status moves on, "Pilot Built" must not survive in generated HTML.
Generated pages are rebuilt from the spec, so this only appears if someone hand-edited
output — which is itself the error.
GREP: Pilot Built

### 17. Week-granularity distances from an undated sitting day
**No source copy prints an examination day — only a month.** Any statement of the form
"N weeks before/after this sitting" is therefore a distance measured from a day nobody
knows, and it silently asserts one. Across a 30-day sitting month the true figure moves by
more than four weeks, so a week count is only ever the value for one arbitrary day.

Two severities, and only the first is a defect of substance:

- **Material** — the event falls *inside* the sitting month, and the week count disguises
  an in-month boundary as a settled pre-sitting fact. Found for real twice: QP2504-Q6 said
  the 2024 attained CII "fell due for reporting by 31 March 2025 — **three weeks before
  this paper**" across seven surfaces, when the true gap runs from one day to four weeks;
  and QP2510-Q6 said the electronic Ballast Water Record Book amendments "took effect on
  1 October 2025, **three weeks before this examination**" when 1 October is the *first day
  of QP2510's own sitting month*. The second was shipping in the Study Guide.
- **Cosmetic** — the event lies comfortably outside the sitting month, so the substance is
  day-independent and only the precision is spurious (QP2402, QP2411, QP2503, QP2508,
  QP2602, QP2603).

**Rule.** Use month granularity — "in the month immediately before this sitting", "the
winter before", "two months after this sitting month". A week or day count is admissible
only where the event lies more than a full month outside the sitting month, and even then
adds nothing. Where the event falls inside the sitting month it must be classified as an
in-month boundary under the paper's temporal anchor, never expressed as a distance.

GREP: SKIP
NOTE: a bare phrase match is wrong here — "three weeks at anchor" is a legitimate
hypothetical in QP2504-Q6 that shows AER rewards distance, and a mechanical purge would
destroy it. The test is whether the phrase measures from the examination day, which needs
the surrounding clause. Detect on the pattern
`<number> (week|day)s? (before|after|ago) ... (this )?(sitting|paper|examination)`.
SCOPE: product

### 18. The ISM Code has no regulations
The ISM Code is **not divided into regulations**. Part A is divided into numbered
**elements** (1 General ... 9 Reports and analysis of non-conformities, accidents and
hazardous occurrences ... 12 Company verification, review and evaluation), and those are
divided into **paragraphs** (1.2 Objectives, 1.2.2, 1.2.2.1). *Regulation* is the unit of
SOLAS and MARPOL. The Code's own text confirms it: it uses "regulation" only for SOLAS
chapter IX (`regulation IX/1`, `regulation IX/6.2`) and for generic "rules and
regulations", and calls its own components **elements** ("a safety management system
element", "key elements of this Code").

Cite an ISM top-level number as an **element**, a dotted number as a **paragraph**. The
corpus house forms agree: element, paragraph, section.

Found for real in exactly two papers, and the second inherited it from the first:
`QP2412-Q5` (December 2024) carried 21 wrong tokens and is `QP2310-Q9`'s Tier D donor, so
the same wrong unit shipped again in October 2023. Both are corrected. Note that the
QP2310 correction was itself incomplete for a week: it purged `ISM Code regulation N` but
left the **abbreviated** `ISM reg 9`, `reg 1.2.2`, `reg 12` alive on the recall card,
which is why this trap needs the structural layer below and not only a phrase match.

`SOLAS regulation XI-1/6` sits beside these citations and is **correct** — never purge the
word "regulation" mechanically from a question that carries both.
GREP: ISM Code regulation
SCOPE: product
NOTE: the phrase match stops at the full word `regulation` on purpose. Truncating the
needle to `ISM Code reg` looks like it catches more -- the abbreviated `ISM Code reg 9`
as well -- but it fires on **`the ISM Code regulates a system`**, which is correct English
and appears three times across QP2402, QP2408 and QP2412. That was tried and rejected here
rather than discovered in production.

Two forms therefore fall to the structural layer instead, both requiring a DIGIT after the
unit so that no verb can satisfy them: the abbreviated `ISM Code reg 9`, and the
un-prefixed `ISM reg 9` -- the latter can never be a safe literal, because a bare
`ism reg` substring fires on "mechanism regulates". The structural form matches `ISM` as a
whole uppercase token, an optional `Code`, then a numbered reg, which no other
instrument's citation can satisfy and which `SOLAS regulation XI-1/6` cannot reach.

---

### 19. `A.1184(33)` is places of refuge — the ISM implementation guidance is `A.1188(33)`
The 33rd Assembly adopted both on **6 December 2023**, four digits apart:

| Resolution | Subject | Adopted | Revokes |
|---|---|---|---|
| `A.1184(33)` | Guidelines on places of refuge for ships in need of assistance | 6 Dec 2023 | `A.949(23)` (op. para 4) |
| `A.1188(33)` | 2023 Guidelines on implementation of the ISM Code by Administrations | 6 Dec 2023 | `A.1118(30)` (op. para 5) |
| `A.1118(30)` | Revised Guidelines on the implementation of the ISM Code by Administrations | 6 Dec 2017 | `A.1071(28)` (op. para 5) |

All three read at source in the Organization's own published resolutions.

The defect is **corpus-inherited, not authored**: `10-amendment-register/AMENDMENT_REGISTER.md`
records `A.1184(33)` as ISM implementation guidance and the ISM-Code folder holds the
places-of-refuge PDF under that filename. Raised as `TS-REFERRAL-QP2311-3`; the corpus is not
edited from a paper branch. Four papers detected it and refused to consume it (`QP2309`,
`QP2311`, `QP2312`, and `QP2306` partially); two consumed it and shipped —
`QP2406-Q5` and `QP2502-Q1/Q3`, corrected 15 August 2026.

**Temporal note before correcting anything.** `A.1188(33)` is only operative from 6 December
2023. For a sitting before that date the operative ISM guidance is `A.1118(30)` of 2017 and
`A.1188(33)` may appear only as a future development or a trap — which is exactly how
`QP2308`, `QP2309` and `QP2311` already carry it. A blind number swap would forward-contaminate
every 2023 paper.

GREP: SKIP
NOTE: no phrase match is safe in either direction. `A.1184(33)` is **correct** in `QP2304`,
`QP2402`, `QP2503`, `QP2506` and `QP2507`, and the sentences that correct the defect must name
the ISM Code in order to deny it. The structural layer therefore reads context: an ISM marker
within 300 characters of the citation, with no places-of-refuge marker to disarm it. Its
positive control is `QP2502-Q3`'s shipped model answer; its negative control is `QP2507-Q9`'s
correct citation and a correcting sentence, both of which must pass.
