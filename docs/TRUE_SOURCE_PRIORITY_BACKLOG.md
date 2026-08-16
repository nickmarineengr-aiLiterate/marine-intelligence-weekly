# True Source — prioritised micro-package backlog

Internal. 2026-08-13, laptop team. Built from the **actual 252-question solved
corpus** at main `161c2b1`, plus QP2301 (read-only, desktop-owned). This is not a
maritime-law wishlist: every package below is here because named questions that
are already published need it.

---

## 0. The two corpora are different systems

| | **MIW True Source** | **RulesApp True Source** |
|---|---|---|
| Path | `F:\miw-true-source` | `F:\RulesApp-Local-Input\true-source` |
| Repo | `nixonvantony/miw-true-source` | RulesApp private local input |
| Shape | 5 subject packages, each with `*_DEFINITIONS.json`, `*_INSTRUMENT_REGISTER.md`, `*_SEQUENCE.json`, `COVERAGE_MATRIX.md`, `CANDIDATE_TRAPS_AND_MISSING_POINTS.md`, `WATCH_REGISTER.md`, `CURRENT_STATUS.md` | numbered governance tree, `00-governance` … `13-validation-reports`, `99-review-queue` |
| Role here | **the corpus this backlog is for** | read-only supporting evidence only |

Structurally verified this session, not assumed. They share no ID convention.
Nothing below may be merged, migrated or renamed across them, and any answer
that draws on RulesApp material must say so in its own `sources[]` entry.

---

## 1. MIW True Source — current health

Five packages, all at **FOUNDER_REVIEW** with validation gates passing.

| Package | Instruments actually held | Objects |
|---|---|---|
| `salvage` | Salvage Convention 1989 + SCOPIC | 79, all verified |
| `general-average` | York-Antwerp Rules (2016 current, 1994 live) | — |
| `contract-of-carriage` | Hague-Visby / Hamburg / Rotterdam | — |
| `wreck-removal` | Nairobi WRC | — |
| `casualty` | **SOLAS Chapter V, COLREGs 1972, SAR 1979** | 45 |

### Known defects — do not treat the corpus as infallible

- **`casualty/` IS MISNAMED, and it matters commercially.** It holds *navigation,
  collision and search-and-rescue*. It does **not** hold casualty
  *investigation* — no SOLAS I/21, no XI-1/6, no MSC.255(84). Verified this
  session against `CASUALTY_INSTRUMENT_REGISTER.md`. Anyone assigning "casualty"
  work off the folder name will assign the wrong thing. (TSCR-7 class.)
- **TSCR-6 — `TRAP-RULE-D-FAULT` is wrong.** It asserts the Rule Paramount bars
  general average on fault. The Rule Paramount is a reasonableness gate; Rule D
  preserves the *remedies and defences* residue. Already found and worked around
  during the QP2407 enrichment. **Prefer provision text over any gloss object.**
- **TSCR-5 — duplicate object IDs**; **TSCR-8 — README/coverage inconsistency.**
  Both still open and both block confident scaling.

### The most important finding for planning

**Four of the five packages are built and have never been applied to the QP
corpus.** Only ONE question in 252 — QP2407-Q8 — has been enriched from True
Source. Salvage scores an 83% verification gap in §2 *while a complete,
79-object, fully verified Salvage package sits in the repo.*

That reframes the backlog: the highest-value next actions are **APPLY**, not
**BUILD**. Applying stock costs no corpus-construction effort at all.

---

## 2. Verification-gap map — measured, not guessed

`Qs` = solved questions turning on the instrument. `noP1` = of those, how many
carry **zero** `P1_PRIMARY_VERIFIED` source. Corpus-wide: **195 of 252 questions
(77%) have no primary-verified source**.

| Instrument | Qs | noP1 | Gap | Package state |
|---|---|---|---|---|
| MARPOL Annex VI | 69 | 42 | 61% | **EXISTING BUILD — DO NOT DUPLICATE** |
| ISM Code | 48 | 37 | 77% | none |
| MLC 2006 | 37 | 25 | 68% | none |
| **Marine Insurance Act 1963** | **33** | **26** | **79%** | none |
| STCW | 24 | 20 | 83% | none |
| **York-Antwerp Rules** | 24 | 18 | 75% | **BUILT — apply** |
| **PSC / A.1185(33) / A.1206(34)** | 24 | 22 | **92%** | none |
| CLC / Fund / Bunkers | 19 | 14 | 74% | none |
| **LLMC** | **18** | **13** | 72% | none |
| **UNCLOS** | 17 | 16 | **94%** | none |
| **Nairobi Wreck Removal** | 15 | 8 | 53% | **BUILT — apply** |
| Load Lines | 14 | 9 | 64% | none |
| **Casualty Investigation Code** | **13** | **11** | **85%** | **none — `casualty/` is a different subject** |
| **Salvage Convention 1989** | 12 | 10 | 83% | **BUILT — apply** |
| FSA | 11 | 9 | 82% | none |
| BWM Convention | 8 | 7 | 88% | none |
| AFS Convention | 8 | 5 | 62% | none |
| Hague-Visby / carriage | 8 | 4 | 50% | **BUILT — apply** |
| Hong Kong Convention | 7 | 5 | 71% | none |

Human Element & Management carries 38 zero-P1 questions and appears in no
package below **on purpose**: it is largely doctrine and good practice with no
single citable instrument, so a package would capture little.

---

## 3. MARPOL Annex VI — EXISTING BUILD, DO NOT DUPLICATE

Largest single dependency in the corpus: **69 questions, 42 with no primary
source**. A corpus is already under construction elsewhere. **No Kimi package is
to be assigned.**

Priority provisions to feed to that existing build, from actual QP demand and
from the two numbering defects already corrected on live pages:

- **Chapter 4 headings verbatim** — reg 21 Functional requirements, 22 Attained
  EEDI, 23 Attained EEXI, 24 Required EEDI, 25 Required EEXI, 26 SEEMP, 27 fuel
  oil consumption data, 28 operational carbon intensity. *Two separate live
  defects came from this list alone (QP2402 Q3/Q5/Q6, QP2601-Q1).*
- reg 14 sulphur limits and reg 18.3 fuel oil quality (with Appendix V, the ten
  BDN items) — QP2408-Q6 turns entirely on these
- reg 13 NOx tiers; reg 25.3 review deadline
- CII / SEEMP Part III chain: MEPC.346(78) → MEPC.388(81) → MEPC.395(82)

---

## 4. Tier A — APPLY existing packages (no construction, immediate marks)

These need **no Kimi work at all**. They are laptop enrichment sessions of the
exact shape QP2407-Q8 already proved, which took one question from zero to five
P1 sources and reduced validator warnings.

| # | Action | Questions served | Notes |
|---|---|---|---|
| **A1** | Apply `salvage` to Salvage questions | **12** (10 zero-P1) | Package is 79 objects, all verified, 31/31 coverage. **QP2408-Q7 and QP2411-Q5 are also the corpus's two worst recall-card questions** — enrich and fix cards in one pass. Also serves **QP2301-Q4 (SCOPIC)**. |
| **A2** | Apply `general-average` to remaining GA questions | **24** (18 zero-P1) | QP2407-Q8 is the worked precedent. **Avoid `TRAP-RULE-D-FAULT`** (TSCR-6). Also serves **QP2301-Q6**. |
| **A3** | Apply `wreck-removal` | 15 (8 zero-P1) | Lowest gap of the built set. |
| **A4** | Apply `contract-of-carriage` | 8 (4 zero-P1) | Smallest. Do last. |

**A1 and A2 together serve 36 questions and cost zero corpus construction.**
This is the single most under-exploited asset in the project.

---

## 5. Tier B — BUILD: top packages for Kimi

Small, instrument-specific, provision-specific, independently completable.

### P1 — CASUALTY INVESTIGATION CORE  ·  SIZE: SMALL  ·  BUILD FIRST

- **Why:** 13 questions, 11 with no primary source (85%). The Founder's own
  worked example. **The existing `casualty/` package does NOT cover this** —
  verified, not assumed. Also the topic where a real candidate-reported gap
  (SOLAS I/21(b)) was found and fixed this month, which is evidence the answers
  here are thin.
- **QPs supported:** QP2506-Q7, QP2601-Q8, QP2604-Q8, QP2408-Q3, **QP2301-Q7**, +8 more
- **Exact sources:** SOLAS reg I/21; SOLAS reg XI-1/6; resolution MSC.255(84)
  (Casualty Investigation Code); MARPOL Articles 8 and 12
- **Provisions to capture:** I/21(a) duty to investigate and the "may assist in
  identifying changes" test; **I/21(b)** supply of findings to IMO and the
  non-disclosure rule — capture explicitly that it binds *reports or
  recommendations OF THE ORGANIZATION*, not the investigating Administration;
  XI-1/6; Code Parts I–III with the **mandatory Part II / recommendatory Part III
  split**; definitions of marine casualty, very serious marine casualty, marine
  incident, marine safety investigation, substantially interested State
- **Known traps:** (a) the non-disclosure target inversion above — a real
  candidate got this wrong; (b) **GISIS is NOT part of the Casualty
  Investigation Code** — already recorded; (c) Part III is recommendatory and
  must not be cited as mandatory
- **Completion test:** every Code definition resolves to an object; I/21(b)'s
  target is stated as IMO output; the Part II/III split is explicit; GISIS is
  recorded as a negative-knowledge object
- **Name it `casualty-investigation`, never `casualty`.**

### P2 — LLMC CORE  ·  SIZE: SMALL

- **Why:** 18 questions, 13 zero-P1. Structurally clean — a short convention with
  a well-bounded article set. Fallback limit for HNS-type incidents, so it is
  load-bearing for other answers too.
- **QPs supported:** QP2301-Q5, QP2504-Q8, and 16 more
- **Exact sources:** LLMC 1976; 1996 Protocol; **LEG.5(99)** 2012 amendments
- **Provisions:** Art 1 persons entitled; Art 2 claims subject to limitation;
  **Art 3 claims excepted**; Art 4 conduct barring limitation; Arts 6–7 limits;
  Art 8 unit of account (SDR); Arts 11–13 the fund; the tacit-acceptance
  amendment mechanism
- **Numbers:** current Art 6/7 limits with the LEG.5(99) uplift and **the date it
  took effect**; tonnage bands
- **Known traps:** the 2012 amendments are **LEG.5(99), not LEG.3(91)** — this
  exact error was found and fixed in the Oral bank, so it is live in the house;
  Art 4's "personal act or omission, committed with intent… or recklessly and
  with knowledge" is a *conduct* test, not negligence
- **Completion test:** every limit carries its amendment instrument and effective
  date; Art 3 exclusions are enumerated; the Art 4 wording is verbatim

### P3 — MARINE INSURANCE ACT 1963 — HIGH-FREQUENCY PROVISIONS  ·  SIZE: MEDIUM

- **Why:** **33 questions, 26 zero-P1 — the largest non-Annex-VI gap in the
  corpus.** MIW currently cites **no section** of the Act at all: recorded as a
  standing declared limitation on QP2407-Q8. Indian statute, so it also anchors
  the Indian Maritime Legislation category.
- **QPs supported:** QP2301-Q3, QP2504-Q8, + 31 more
- **Exact source:** Marine Insurance Act, 1963 (India). **Use `shipmin.gov.in` /
  `dgma.gov.in`; India Code 403s automated fetch.**
- **Provisions:** insurable interest; utmost good faith; disclosure and
  representation; warranties; the voyage/time policy distinction; total loss —
  actual vs constructive; abandonment and notice of abandonment; particular
  average vs general average; **the sue and labour clause**; subrogation;
  double insurance and contribution
- **Known traps:** particular average is **not** a small general average — it is
  a different concept entirely; a constructive total loss needs notice of
  abandonment; MIA 1963 largely tracks the UK MIA 1906 but section numbers must
  be cited from the **Indian** Act
- **Completion test:** every listed concept resolves to a numbered section of the
  1963 Act, cited as such

### P4 — UNCLOS FLAG-STATE CORE  ·  SIZE: SMALL

- **Why:** **94% gap — the worst in the corpus** (17 questions, 16 zero-P1). Four
  articles.
- **Exact sources:** UNCLOS 1982 Articles **91, 92, 94, 217**
- **Provisions:** Art 91 nationality and **genuine link**; Art 92 exclusive flag
  jurisdiction on the high seas and the two exceptions; Art 94 duties in
  administrative, technical and social matters, including the inquiry duty at
  94(7); Art 217 flag-State enforcement
- **Known traps:** a "genuine link" is required but UNCLOS provides **no sanction
  for its absence** — the common wrong answer is that a flag without a genuine
  link is void; Art 94(7)'s inquiry duty is frequently confused with the SOLAS
  I/21 duty (**pair this with P1**)
- **Completion test:** all four articles verbatim; the no-sanction point recorded
  as negative knowledge; the 94(7) / I/21 boundary stated

### P5 — PSC CORE  ·  SIZE: SMALL

- **Why:** 24 questions, 22 zero-P1 (**92%**). A live superseded-resolution trap
  already burned the Oral bank.
- **Exact sources:** resolution **A.1185(33)**; resolution **A.1206(34)**; Paris
  MoU NIR
- **Provisions:** clear grounds; detainable deficiencies; the three-stage appeal
  chain (Port State → Flag State/RO → MoU Secretariat); NIR ship risk profile
- **Known traps — TEMPORAL, and this one is sharp:** **A.1206(34) supersedes
  A.1185(33), but A.1185(33) is CORRECT for any sitting before December 2025**,
  including QP2512. The package must carry both with their dates. A
  current-law-only package would corrupt every historical paper.
- **Completion test:** both resolutions present with adoption dates and the
  supersession date; the appeal chain has all three stages

### P6 — BWM CORE  ·  SIZE: SMALL

- 8 questions, 7 zero-P1 (88%). Definitions; **D-1 vs D-2** standards; BWMP;
  ballast water record book; survey and certification; the amendment chain used
  by current QPs. Trap: D-1 exchange vs D-2 treatment, and the implementation
  schedule tied to the IOPP renewal survey.

### P7 — AFS CORE  ·  SIZE: SMALL

- 8 questions, 5 zero-P1. **Serves QP2301-Q2 directly.** Scope; controls; Annex 1
  prohibited systems (TBT, and the **cybutryne** addition, MEPC.331(76), in force
  1 January 2023); survey and certification (IAFS Certificate); the 400 GT / 24 m
  thresholds. Trap: cybutryne is a *later* addition — check it against the
  sitting date, and QP2301 is January 2023.

### P8 — LOAD LINES CORE  ·  SIZE: SMALL

- 14 questions, 9 zero-P1. Definitions; conditions of assignment; zones, areas
  and seasonal periods; freeboard assignment; the 1988 Protocol. Trap:
  "conditions of assignment" is a defined term, not a general phrase.

### P9 — HONG KONG CONVENTION CORE  ·  SIZE: SMALL

- 7 questions, 5 zero-P1. **MIW already holds the complete official 47-page PDF**
  — this is close to an APPLY. **Article 3.3** application (the exclusion is
  lifelong domestic operation, **not** the absence of international voyages — a
  live correction was made on two papers this month); Art 17 entry-into-force
  conditions (15 States / 40% / 3%); IHM; Ship Recycling Plan.

### P10 — FSA FRAMEWORK  ·  SIZE: SMALL

- 11 questions, 9 zero-P1. `MSC-MEPC.2/Circ.12/Rev.x` — **capture the revision
  number and its date**, since the QPs span 2023–2026. The five steps; hazard
  identification; risk analysis; RCOs; cost-benefit; recommendations.

---

## 6. Recommended order

**Do Tier A first.** A1 and A2 serve 36 published questions from packages that
already exist and are already verified. No other action in this document has a
better ratio.

**Top 3 for Kimi to build next:**

1. **P1 Casualty Investigation Core** — SMALL, 13 QPs, 85% gap, the existing
   package does not cover it, and it serves QP2301-Q7
2. **P2 LLMC Core** — SMALL, 18 QPs, clean article boundary, serves QP2301-Q5
3. **P3 Marine Insurance Act 1963** — MEDIUM, 33 QPs, the largest non-Annex-VI
   gap, and MIW currently cites no section of it whatsoever

P4 (UNCLOS flag state) is the best fourth: four articles, worst gap percentage in
the corpus, and it pairs with P1.

---

## 8. Package integrity and rights — registered 2026-08-16

Two items that are **not build work**. Both came out of the York-Antwerp Rule XXI
repair (`nixonvantony/miw-true-source` @ `44e6975`) and were deliberately left
outside its scope. Neither blocks any Tier A or Tier B package above.

### C — unsupported relationship-object metrics in other packages

`general-average/CURRENT_STATUS.md` was recomputed from its own files on
2026-08-16, after it was found claiming *"Rule objects: 24"*, *"Relationship
objects: 8"*, *"Total structured objects: 33"* and *"Verified: all"* — none of
which the tree ever held.

The same pattern is visible elsewhere and was **not** corrected, being out of
scope: `casualty/CURRENT_STATUS.md` claims **10** relationship objects and
`contract-of-carriage/CURRENT_STATUS.md` claims **12**, while **no
relationship-object file exists in any package**. The remaining packages were not
checked at all.

**Classification:** TRUE_SOURCE PACKAGE HONESTY AUDIT.
**Priority:** below active written-QP work — *unless* a metric is being relied on
as a completeness or validation claim, in which case it becomes a correctness
issue rather than a tidiness one. The general-average precedent is the model:
recount from the files, state what is actually held, and record what is missing
rather than quietly deleting the claim.

### D — verbatim source wording in earlier public Git history

`miw-true-source` is a **public** repository. The public-derived / private-evidence
migration (2026-08-15) closed forward exposure — the current tree holds
MIW-authored propositions and no substantial source wording — but commits made
before it remain publicly reachable and still contain verbatim CMI text.
`PRIVATE_EVIDENCE_BOUNDARY.md` records this explicitly as a known limitation and
expressly leaves it open.

**Classification:** FOUNDER / GOVERNANCE / RIGHTS DECISION. Not a content
correction, and not an agent decision.

**Constraints for whoever picks this up:** do not rewrite Git history, do not
force-push, do not delete evidence. The prior local implementation is preserved on
the local branch `archive/yar-rule-xxi-pre-private-boundary` (`ec23862`), which was
never pushed and is **not** in `main`'s ancestry. The decision to be taken is
whether any remediation is legally or operationally necessary at all — leaving it
is a legitimate outcome.

---

## 7. 2023 reuse signal — QP2301 (read-only)

QP2301 was inspected via `git show` on `origin/pastpapers/qp2301-founder-review`
and **not modified**. 9/9 authored, every question at zero P1 sources.

**Five of its nine questions are served by this backlog:** Q2 (AFS → P7), Q3
(Marine Insurance → P3), Q4 (SCOPIC → **A1, stock**), Q5 (LLMC → P2), Q6
(General Average → **A2, stock**).

That is a strong reuse signal: the packages ranked highest on the 2024–2026
corpus are the same ones 2023 will need, and two of the five need no
construction at all.
