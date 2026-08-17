# Watch register — Phase 2 queue

**RESEARCH ONLY.** `current_as_of: 2026-08-17`

---

## A. Current-answer correction candidates

**Evidence only. Nothing patched. Laptop adjudicates.**
Recorded under §48 — Desktop must not modify a current answer on this branch.

### CAC-001 — QP2608-Q2 (and Q1): no antifouling / AFS content

**Severity: MEDIUM–HIGH · Confidence: HIGH that the omission exists**

**Evidence.** The authored QP2608 Q1 and Q2 objects were searched for
`antifoul`, `AFS`, `cybutryne` and `biofoul`. **Zero occurrences in either.**
(`ballast` appears 9 times in Q2, but in the trim/stability sense — the ballast
plan and docking condition — not the BWM sense.)

**Why it matters.** A dry dock is where antifouling is applied and where the AFS
documentation is renewed. MIW's own verified corpus establishes that **two**
controls are in force — organotins, and **cybutryne from 1 January 2023**
(QP2301). An examiner asking about dry-docking preparations and yard
co-operation can reasonably expect antifouling to appear.

**What is NOT claimed.** That the answer is wrong. It is a possible **omission**
in scope. Q2 asks about coordination, delegation and undocking, and an
examiner may not expect antifouling within those limbs. This needs a judgement
about the question's demands, which is Laptop's call.

**Weaker sibling.** Whether the **BWM Convention** belongs in Q1/Q2 is more
arguable — ballast for docking is primarily a stability matter. Recorded at
**LOW–MEDIUM** confidence; do not treat it as equivalent to the AFS point.

**Do not patch on this branch.**

---

## B. Coverage gaps — content MIW does not hold

| ID | Gap | Where it bites |
|---|---|---|
| GAP-001 | **Charterers Contribution Clause** — no verified MIW material at all | QP2608-Q4(d). Least-supported limb in the paper. |
| GAP-002 | **War Risk Clause** under the Marine Insurance Act — no ancestor | QP2608-Q4(c) |
| GAP-003 | **Deviation** under the Marine Insurance Act — no ancestor | QP2608-Q4(a) |
| GAP-004 | **Laid-up notation** vs intermediate/annual/special survey cycle — no ancestor | QP2608-Q1(b), 6 marks |
| GAP-005 | **HV/LV switchboard, isolation, permit to work, power restoration** — nothing in the corpus 2021–2026 sets a switchboard or HV question | QP2608-Q7, entire 16 marks |
| GAP-006 | **Cargo abandonment** (as distinct from abandonment of the ship as wreck) | QP2608-Q3(b) |

GAP-005 is the largest single hole: a whole question with no corpus ancestor.

---

## C. Instrument identities to establish

| ID | Item | Status |
|---|---|---|
| INS-001 | Enclosed-space entry and rescue drill requirements — controlling instrument | MIW deliberately refers **descriptively, not by number** (QP2311) because identity could not be established from a held source. **Do not supply a number until it is.** |
| INS-002 | Biofouling / in-water hull cleaning discharge controls — instrument and status | MIW holds biofouling material but the controlling instrument was not verified this session |

---

## D. Acquisition to retry

| ID | Target | Why | Status |
|---|---|---|---|
| ACQ-001 | **DG Shipping question bank** `SRC-DGS-QBANK` | Official tier; would replace the user-upload source under H1/H2/H3 | `ECONNREFUSED` all session — retry |
| ACQ-002 | Re-source the **July 2012** attestation | H1/H2/H3 currently rest on one third-party upload that direct HTTP cannot even retrieve (3 KB stub) | open |
| ACQ-003 | DG Shipping **live notice archive** | Settle the NTA verdict against the primary archive | unreachable — retry |
| ACQ-004 | 2010 papers specifically | **Warning:** DieselShip 2010 sets hold only 10–25 questions across 7 categories vs 52–66 for 2011–2012. Buying access may **not** resolve 2010. Verify before any spend. | advisory |

---

## E. Model work for Phase 2

1. **Re-key occurrences on `(question_id, limb_label)`.** Question-level keys
   both under- and over-report on this paper. This is the single most important
   change.
2. **Always report recurrence mark-weighted as well as question-wise.**
   4/9 questions vs ~17% of marks describe the same paper very differently.
3. **Do not build a numeric revival score.** See `SIMILARITY_MODEL.md`.
4. **Keep the four provenance tiers.** The distinction between a text comparison
   and a recollection is what this whole layer rests on.
5. Decide placement of the temporal block — Study Guide vs Exam Plan
   (see `BULLET_CONNECTION_PILOT.md`).

---

## F. Standing cautions

- **MIW's evidence floor is January 2021.** Any statement of the form "asked
  since 2010" is unsupported today, whoever says it.
- **Dormancy is partly an artefact.** "Not seen for 14 years" means "not seen in
  the window MIW can see". Never publish it as an examining fact.
- **`TOPIC_ONLY` is not a repeat.** It is the class that inflates statistics.
- **DieselShip is a historical source, never MIW's answer authority.**

---

# Phase 2 — dispositions and the Phase 3 queue

`current_as_of: 2026-08-17`

## Sections A–E, closed out

| Item | Disposition |
|---|---|
| **CAC-001** — QP2608 Q1/Q2 carry no AFS/cybutryne content | **CLOSED, NOT A CORRECTION.** The Laptop adjudicated this `USEFUL_ENRICHMENT` on Q2 and `OPTIONAL_DETAIL` on Q1. Phase 2 confirms the omission is real and confirms it is **not a defect**: the stem asks about coordination, delegation and undocking inspections, not environmental compliance. Carried instead as Temporal Delta pilot B at `MINOR`. See `CURRENT_ANSWER_CORRECTION_CANDIDATES.md`. |
| **ACQ-001** — DG Shipping question bank | **ACHIEVED.** Origin host still `ECONNREFUSED`; obtained from the Internet Archive. `SRC-DGS-QBANK-ARCHIVED`, 185/185 items, `PRESERVED_RAW`. This was the highest-value item on the register and it is the Phase-2 headline. |
| **ACQ-002** — re-source the July 2012 attestation | **CLOSED BY SUPERSESSION, NOT BY RE-SOURCING.** The stems are now evidenced officially. The July 2012 **date** was not re-sourced and is counted nowhere. |
| **ACQ-003** — DG Shipping live notice archive | **PARTIALLY ACHIEVED.** Live host unreachable; 12,130 archived DGS URLs enumerated via the Wayback CDX index, 830 mentioning MEO, and the exam module document index recovered. **No NTA reference found.** |
| **ACQ-004** — 2010 papers | **UNCHANGED, advisory stands.** No 2010–2012 paper was recovered. |
| **E-1** — re-key occurrences on `(question_id, limb_label)` | **DONE**, with `limb_kind` added so a scaffold cannot key a recurrence. |
| **E-2** — always report mark-weighted | **DONE.** `QP2608_PAPER_DNA.md` reports both, and the mark-weighted figure moved from ~17% estimated to 33.3% verified. |
| **E-3** — no numeric revival score | **HELD.** None built. |
| **E-4** — keep the provenance tiers | **HELD**, with `OFFICIAL_BANK_ANCESTOR` added above them. |
| **E-5** — decide temporal block placement | **DONE.** Study Guide. Rule in `TEMPORAL_CONTEXT_BOUNDARY.md`. |

`INS-001` and `INS-002` remain **open and unchanged**. Neither instrument identity
was established in Phase 2, and no number has been supplied for either.

---

## Phase 3 queue

| ID | Item | Why |
|---|---|---|
| **P3-001** | **Serialise `FAMILY-EM-0008`** — unseaworthy vessels / MS Act | Five verified sittings, an official ancestor, and the only demonstrable `DO NOT WRITE TODAY` found. Documented in `QP2608_TEMPORAL_DELTAS.md` but deliberately not serialised — building five occurrence records at speed is how the Phase-1 defect happened. **Highest value item on this register.** |
| **P3-002** | **Work the 832 archived MEO URLs** | ~~Each recovered dated official paper directly attacks the date problem that blocks H1–H5.~~ **Corrected in Phase 3A — see the reframe below. It does not attack H1–H5.** The set is still high value, for a different reason: it can build verified dated history from 2013 forward. |
| **P3-003** | Build families for the other **62 strong bank matches** | 21 papers have a bank ancestor. Only QP2608's were modelled. |
| **P3-004** | Decide canonical storage for the bank PDF | Official, public, load-bearing — and currently in one place on one machine, outside version control. |
| **P3-005** | Re-run the leak sweep at **step** level | The point-level probe produces two standing false positives. Method note in `CURRENT_ANSWER_CORRECTION_CANDIDATES.md`. |
| **P3-006** | Re-check whether the DGS domain is reachable | Every remaining official route runs through it. |

---

## Standing cautions — Phase 2 additions

- **The official bank dates nothing.** It is the strongest evidence of ancestry in
  the layer and carries `date_confidence: NONE`. Read the date column every time.
- **QP2608 is not a typical paper.** It has 7 strong bank matches, the most in the
  corpus, where the median matched paper has 2. Do not generalise its DNA.
- **`SOURCE NOT FOUND` is a statement about our sources, not about the question.**
  H4 was `SOURCE NOT FOUND` in Phase 1 and its full ancestor was found in Phase 2.
  Phase 1 was right to phrase it as a limit on the search; had it been written as
  “this question is new”, Phase 2 would have had to retract a published claim.

---

## Phase 3A corrections

### The 2010–2012 route is closed

Laptop enumerated the DGS Wayback holdings independently: **11,917 archived DGS
URLs, 832 mentioning MEO, but only 12 MEO Class I files, all falling roughly
October 2013 – September 2015. Zero from 2010–2012.**

The archive lead was recorded as attacking the alleged 2010–2012 dates behind
H1–H5. **It does not, and Phase 3A stops claiming it does.** There is nothing in
that archive from those years to find.

**H1–H5 dates remain unsupported**, exactly as Phase 2 left them. Nothing in
Phase 3A strengthened or weakened them; the route that was supposed to settle
them turned out not to lead there. Chasing 2010–2012 through this archive is
not a plan, and no further Phase-3A time was spent on it.

### The archive is still high value — for a different job

Its role is now **build verified dated history from 2013 forward**, not *prove
the old 2010–2012 rumours*. Twelve official dated MEO Class I files is twelve
more dated sittings than the layer has outside MIW's own holdings, and each one
can carry a Type A block. That is Phase 3B (`P3-002`), and it is not started.

### NTA — closed

Recommendation: **`CLOSED_NO_EVIDENCE`**. Extensive official and archive
searching across Phases 2 and 3A found the DGS question bank, the DGS archived
MEO materials, and a dated 2005 official paper — and **no NTA reference of any
kind**. Reopen only on a primary signal. No candidate publication either way.

### DieselShip — unchanged

**DO NOT PURCHASE. Do not log in.** The official DGS evidence has further reduced
its marginal value: the bank supersedes it for wording at a strictly higher
provenance tier. Revisit only if future evidence shows uniquely useful *dated*
material available nowhere else. The 37 `SRC-DS-*` manifest entries stay as
provenance records, and remain untyped precisely because they assert sittings
whose text was never seen.

### The 2005 dated paper

Retained as a provenance and acquisition-method control only. Checked in Phase 3A:
**no date claim from it has leaked into any unrelated recurrence family.** It is
cited by `SRC-DGS-2005-MGMT` alone and keys no occurrence record.

### Standing caution added in Phase 3A

- **A classifier that cannot tell `describe` from `criticise` must not be pointed
  at history.** It could not, until Phase 3A. If a future change makes the
  adversarial suite pass with a guard switched off, that guard has stopped
  working — run `adversarial_controls.py --mutate`, not just the controls.
