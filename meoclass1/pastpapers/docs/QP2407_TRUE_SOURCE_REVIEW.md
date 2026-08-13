# QP2407 — TRUE SOURCE REVIEW

**Paper:** QP2407 — July 2024 — MEO Class I, Engineering Management (printed serial `Sr. No. EM – 2407`)
**Reviewed:** 2026-08-13 · laptop · branch `integration/qp2407-laptop-review`
**Desktop build reviewed:** `pastpapers/qp2407-founder-review` @ `7e71066`
**Source repository:** `miw-true-source` @ `7f8c9fb` (branch `main`, clean)

This is the **first controlled production use** of the True Source repository against a written paper.
It is a review of a completed desktop build, not a rebuild.

---

## 1. HEADLINE

The corpus is a **marine-law / admiralty** corpus. QP2407 is a **technical and IMO-regulatory** paper.
The two barely intersect: **one question of nine** draws on True Source, and only in part.

That single question, however, was the right one. Q8 was the question the desktop build itself
flagged as resting on the least source material, and it was the only question on the paper carrying
**no `P1_PRIMARY_VERIFIED` claims at all**. True Source closed exactly that gap.

| Measure | Before | After |
|---|---|---|
| `validate_spec` errors | 0 | 0 |
| `validate_spec` warnings | 11 | **10** |
| Q8 `P1_PRIMARY_VERIFIED` claims | **0** | **5** |
| Q8 warning "no claims recorded as P1_PRIMARY_VERIFIED" | present | **cleared** |

---

## 2. QUESTION-BY-QUESTION

| Q | Subject | Existing status | True Source coverage | Main finding | Action |
|---|---|---|---|---|---|
| Q1 | Gender equality in shipping | Built, weakest evidence on paper | `NO_COVERAGE` | No package covers MLC, IMO gender programmes or DG Shipping. Existing restraint (no resolution number, no statistic) is correct | `ACCEPT_AS_IS` |
| Q2 | ME vs MC engine | Built | `NO_COVERAGE` | Pure marine engineering. No statutory content | `ACCEPT_AS_IS` |
| Q3 | IMO structure & instrument hierarchy | Built, tier D from QP2402-Q1 | `NO_COVERAGE` | No package holds the Convention on the IMO. Council-at-40 reasoning already re-derived for the sitting | `ACCEPT_AS_IS` |
| Q4 | Revised GHG strategy | Built | `NO_COVERAGE` | MEPC.377(80) not in corpus. Temporal exclusion already correct | `ACCEPT_AS_IS` |
| Q5 | Ship ID number, CSR, ESP | Built | `NO_COVERAGE` | Package 1 holds SOLAS **Chapter V only** — not Chapter XI-1 | `ACCEPT_AS_IS` |
| Q6 | MLC flag & port State | Built | `NO_COVERAGE` | No MLC package. 2018-vs-2022 edition reasoning already correct | `ACCEPT_AS_IS` |
| Q7 | Propeller curves & margins | Built | `NO_COVERAGE` | Pure marine engineering | `ACCEPT_AS_IS` |
| **Q8** | **New Jason & 3/4ths Collision** | **Built, 0 primary claims** | **`PARTIAL_COVERAGE`** | **General average half now primary-verified; insurance clauses still unheld** | **`MAJOR_AMENDMENT`** |
| Q9 | NOx Tier II/III, SCR, Technical File | Built | `NO_COVERAGE` | No Annex VI package. NOx Technical Code gap already declared | `ACCEPT_AS_IS` |

```text
Questions reviewed:      9
Accepted as-is:          8
Minor amendments:        0
Major amendments:        1  (Q8)
Reconstructed:           0
True Source gaps:        1  (TS-GAP-1, non-blocking)
```

`ACCEPT_AS_IS` here means **True Source had nothing to say**, not that the questions went unexamined.
Each was read, classified and tested against the corpus before being left alone. Forcing an unrelated
package onto a question is expressly the thing this workflow must not do.

---

## 3. WHAT CHANGED ON Q8

All five additions are independent scoring points, each anchored to a corpus object.

1. **Rule D — the material addition.** `YAR-D` was absent from the desktop build entirely. It is the
   doctrinal hinge of limb (a): rights to contribution are *not* affected by the fault of a party,
   **but that does not prejudice remedies or defences** in respect of the fault. The New Jason Clause
   exists precisely because Rule D leaves those defences intact. Without Rule D the answer narrates a
   historical problem; with it, the answer states the rule that creates the problem.
2. **General average vs particular average** (`TRAP-GA-PA`) — the distinction was nowhere in the answer.
3. **Rule C** (`YAR-C`) — only direct consequences allowed; delay and market loss excluded.
4. **Rule VI** (`YAR-VI`) — salvage, including Article 14 / SCOPIC special compensation, is a
   *particular charge* and falls outside the adjustment.
5. **Rule XVII** (`YAR-XVII`) — contributory values. Directly answers the printed limb "implications for
   cargo owners": it is what the cargo owner actually pays on.

Plus **edition control** (§14): the answer body now states that the York-Antwerp Rules are a
**contractual code of the Comité Maritime International with no entry into force of their own**,
2016 current and 1994 still live. Previously that sat only in metadata.

**Structure was deliberately preserved.** The material was folded into existing sections 2 and 5 rather
than added as a new numbered section, so `memory_cue`, `answer_route` step numbers and retrieval card
`C1` remain valid. The derived layer was updated in step (route points, keywords, aliases, a new
trap card `QP2407-Q8-C9`) so no cue is more categorical than the verified answer.

**What did NOT change:** every declared limitation stands. MIW still holds no wording of the New Jason
Clause, the 3/4ths Collision Clause or any Institute clause set; no section of the Marine Insurance
Act, 1963 is cited; no clause number is attributed.

---

## 4. TRUE SOURCE GAP

```text
TRUE_SOURCE_GAP: TS-GAP-1
Question:              QP2407-Q8 limb (a)
Required instrument:   Hague-Visby Rules — Article III r.1 (due diligence / seaworthiness)
                       and Article IV r.2(a) (nautical fault exception)
Why required:          The New Jason Clause operates on the words "for which the carrier is not
                       responsible". Those two provisions ARE the "not responsible". They are the
                       condition on which the whole clause rides.
Current coverage:      contract-of-carriage holds Hague-Visby ARTICLE I ONLY (definition of contract
                       of carriage). No article-level object for III or IV.
Recommended:           Extend contract-of-carriage with HV Art. III r.1 and HV Art. IV r.2(a).
Blocking publication?  NO — the substance is stated in effect only, with no article or rule number
                       cited, exactly as the anchor already required.
```

---

## 5. TRUE SOURCE REPOSITORY FINDINGS

Recorded, **not** acted upon. Per the governing rule this session reads the corpus and writes only to
the written-answer repository; canonical source objects are not edited from inside a QP review.

| # | Package | Finding | Severity |
|---|---|---|---|
| TS-DEF-1 | `casualty/` | **`PACKAGE_DESCRIPTION_MISMATCH`** — see §6 | Medium |
| TS-DEF-2 | root `README.md` | Says "Packages 1-4"; there are **five**. `contract-of-carriage` is Package 5 | Low |
| TS-DEF-3 | `contract-of-carriage`, `salvage`, `wreck-removal` | **Duplicate `object_id`s**: `ROT-ART-1` ×3, `SALV-ART1` ×2, `WRC-ART1` ×3. Object IDs are the traceability primitive — a citation `TRUE_SOURCE: ROT-ART-1` is ambiguous today | **High** |
| TS-DEF-4 | `salvage`, `wreck-removal` | Definition objects carry no `instrument` field (present in the other three packages) | Medium |
| TS-DEF-5 | `general-average/COVERAGE_MATRIX.md` | Claims "24/24 covered" but tabulates **10** rows; and cites Rules F and XVII–XX as covering objects when only `YAR-A/C/D/VI/XVII` exist | Medium |
| TS-DEF-6 | `general-average/CANDIDATE_TRAPS...md` | `TRAP-RULE-D-FAULT` states the "YAR 2016 Paramount Clause reinforces: GA barred where fault of party claiming". The Rule Paramount concerns **reasonableness** of sacrifice/expenditure, not fault; and Rule D itself says rights to contribution are *not* affected by fault, the bar arising from remedies/defences under the applicable law. No definition object in the package supports the proposition | **High — adjudicate before reuse** |

**Because of TS-DEF-6, the Q8 answer was written from the verbatim `YAR-D` text, not from the trap gloss.**

---

## 6. PACKAGE 1 — THE NAMING QUESTION (§21)

**Verdict: `PACKAGE_DESCRIPTION_MISMATCH`.**

The *content description* is correct and internally consistent. The *directory name* is the wrong element.

| Evidence | Says |
|---|---|
| Directory name | `casualty` |
| `casualty/README.md` | "Package 1: SOLAS Chapter V (Safety of Navigation); COLREGs 1972; SAR Convention 1979" |
| `CASUALTY_INSTRUMENT_REGISTER.md` | SOLAS Chapter V · COLREGs 1972 · SAR Convention 1979 — and nothing else |
| `CASUALTY_DEFINITIONS.json` | `SOLAS-V33`, `COLREGS-R5`, `SAR-131` |

No casualty-investigation instrument (the Casualty Investigation Code, resolution MSC.255(84)) appears
anywhere in the package. The package is **safety of navigation**.

This matters beyond tidiness: MIW's Knowledge Central holds a **separate and genuinely different**
casualty-investigation corpus. Two different things are now both called "casualty". Recommended rename
to `navigation-safety` — **not performed here**, since renaming a canonical package is a corpus
governance act, not a QP-review act.

---

## 7. WORKFLOW ASSESSMENT (§27)

### What True Source improved
- Converted the paper's weakest-evidenced question from **zero** primary-verified claims to five.
- Supplied **Rule D**, a genuinely missing scoring point that no amount of careful writing would have
  recovered, because the gap was in the *evidence*, not in the prose.
- Supplied three further independent scoring points and a mark-bearing distinction (GA vs PA).
- Enforced version discipline (§14) with a register that states the editions plainly.
- The trap objects worked **in both directions**: they prevented standard candidate errors, and one of
  them (TS-DEF-6) was itself caught as wrong. A corpus that can be audited is worth more than one that
  is merely quoted.

### What was cumbersome
- **Retrieval is manual.** There is no index from a question to candidate objects; coverage was
  established by reading five READMEs and five registers. Fine for one paper, not for fifty.
- **Duplicate object IDs (TS-DEF-3)** actively defeat the citation convention the architecture depends on.
- **The coverage matrices overstate coverage** (TS-DEF-5), so they cannot yet be trusted as the
  screening layer they look like.
- **Packages are thin.** Five definition objects for the whole of general average is a spine, not a body.
  Rule Paramount, Rule B, Rules E–G and Rules XX–XXII are all referenced but undefined.

### What should change before the next paper
1. **Fix the duplicate `object_id`s.** Highest priority — the traceability convention does not work until this is done.
2. **Adjudicate TS-DEF-6** before any other paper cites Rule D or the Rule Paramount.
3. **Add a one-line `TOPICS:` key to each package README** so a paper can be screened against five lines rather than five documents.
4. **Correct the coverage matrices** to list only objects that exist.
5. **Choose pilot papers by subject fit, not by sequence** — see §8.

### Verdict
**The workflow is sound and is suitable for scaling — but QP2407 was a poor choice of pilot.**
It exercised the mechanism (locate → classify → verify → enrich → validate → publish) end to end and
the mechanism held, producing a measurable quality gain and a clean validation run. But a 1-of-9 hit
rate is a property of *this paper*, not of the method. Scaling should now follow subject fit.

---

## 8. NEXT RECOMMENDED PAPER — NOT STARTED

**QP2501 (January 2025).** Its UI fixture probes are `wreck hazard` (Q1), `limitation fund` (Q2) and
`cap survey` (Q3) — wreck removal and liability. That paper should exercise `wreck-removal`,
`salvage` and `general-average` together, which is the corpus's centre of gravity and the proper test
of whether this workflow scales.

Do not begin it until TS-DEF-3 and TS-DEF-6 are resolved.
