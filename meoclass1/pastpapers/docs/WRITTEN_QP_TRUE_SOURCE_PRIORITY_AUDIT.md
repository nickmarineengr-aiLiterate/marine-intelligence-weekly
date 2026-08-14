# WRITTEN QP — TRUE SOURCE PRIORITY AUDIT

**Analysis artefact. No corpus was modified, no QP spec was modified, no branch was integrated.**

| Field | Value |
|---|---|
| Produced | 2026-08-15 |
| Session | `MIW::desktop::written-qp-true-source-priority-audit` |
| Machine | `Dani-Desktop` |
| MIW branch | `analysis/written-qp-true-source-priority` (from `origin/main` `6120e8b`) |
| Corpus inspected | `D:\RulesApp-Local-Input` @ `319524c24d11b2f89f33672c384b56e9ae1ab7db` — **read-only, unmodified** |
| Machine-readable companion | `WRITTEN_QP_TRUE_SOURCE_PRIORITY_AUDIT.json` |

**The question this file answers:** what is the smallest amount of True Source correction or
construction that improves the largest number of *existing* answers and removes the most
correctness risk?

It ranks by **demand measured inside the solved estate**. It is therefore different from, and
complementary to, `TRUE_SOURCE_PRIORITY_FROM_SIX_YEAR_EVIDENCE.md`, which ranks by examination
demand across 61 papers including unsolved intake. Where the two disagree, the disagreement is
stated and explained — it is usually because a gap that is frequent in the *exam* has already been
absorbed defensively in the *answers*.

---

## A. THE AUTHORITATIVE SOLVED-QP ESTATE

**39 unique solved papers · 351 solved questions · 4 years (2023, 2024, 2025, 2026).**

| Year | Papers | Questions |
|---|---|---|
| 2023 | 11 | 99 |
| 2024 | 11 | 99 |
| 2025 | 11 | 99 |
| 2026 | 6 | 54 |
| **Total** | **39** | **351** |

Every paper carries exactly nine questions.

### Deduplication method — proved, not assumed

The estate was assembled mechanically from git, not from any allocation board.

1. `git ls-tree origin/main meoclass1/pastpapers/specs/` returned **34** specs. These are
   authoritative by the integration rule.
2. Every `pastpapers/*-founder-review` branch on origin was enumerated and its spec directory
   listed. Review branches carry the whole spec set, not only their own paper, so a naive union
   would have counted most papers many times over.
3. A branch spec was taken **only** where no spec of that ID exists on `main`. That yielded five:

   | QP | Authoritative source | SHA |
   |---|---|---|
   | QP2302 | `origin/pastpapers/qp2302-founder-review` | `ec402dcf` |
   | QP2306 | `origin/pastpapers/qp2306-founder-review` | `4811f3d7` |
   | QP2307 | `origin/pastpapers/qp2307-founder-review` | `9f8bf0c9` |
   | QP2308 | `origin/pastpapers/qp2308-founder-review` | `7bad6691` |
   | QP2311 | `origin/pastpapers/qp2311-founder-review` | `9e2019a8` |

4. 34 + 5 = **39**, with a one-line provenance record per paper. No QP ID appears twice.

**Reconciliation of the 2023 claim.** `main` holds six 2023 papers (QP2301, 2303, 2304, 2309,
2310, 2312); the five above are the remainder. Eleven of eleven available 2023 sittings are
solved — May 2023 (QP2305) is not in the estate because no source paper is held.

`origin/pastpapers/em2607-founder-review` was inspected and excluded: it carries only `QP2607.json`
and adds no unique paper.

---

## B. EVIDENCE PROFILE

### The uniform signal — this is what the ranking is built on

Every one of the 351 questions carries `unresolved` and `reverify_before_publication`. Together
they hold **2,425 declared limitation items**:

| Signal | Count |
|---|---|
| `unresolved` entries | 1,320 |
| `reverify_before_publication` entries | 1,105 |
| — of class `C_ACCEPTED_LIMITATION` | 735 |
| — of class `B_CURRENCY_CHECK` | 370 |
| Of all 2,425, items using **source-gap language** ("not held", "was not read", "MIW holds no…") | **790** |

Those 790 items are the True Source demand. Everything in sections C–F is derived from them, and
every count is traceable to named question IDs in the JSON companion.

### A measurement that could NOT be made, and why

An estate-wide P1/P2/P3 profile **cannot** be computed from the `sources` field, and any figure
purporting to give one should be distrusted. The grading vocabulary is not normalised across
papers. Of 3,283 source claims: 47.5% carry a primary-shaped prefix, 30.2% secondary-shaped,
12.9% tertiary-shaped and **9.4% carry no grade prefix at all** — and the ungraded ones are
concentrated in whole papers. QP2607 and QP2404, for example, write bare source strings
(`"IMO MSC-MEPC.2/Circ.12/Rev.2, 9 April 2018 - full text read"`) with no `P1:` marker, which a
prefix-based count scores as zero-primary when the claim is plainly primary and read at source.

A naive count returns "71 questions with zero P1 claims". **That number is an artefact and must
not be used.** The genuinely evidence-thin cases inside it — `QP2304-Q3` is the documented example,
whose entire answer rests on `INTERNAL REUSE VERIFIED` donors plus ungraded York-Antwerp statements
— are real, but they cannot be separated from the vocabulary noise by counting.

Recorded as a governance observation, not as a corpus job: **normalising the evidence-grade
vocabulary across the estate would make the product's own evidence claims measurable.** It is a QP
metadata job, XS–S, and it is not a release blocker.

### The estate's posture toward corpus defects — the central finding

The solved answers **do not consume corpus defects silently. They declare and reject them.**

This was tested directly rather than assumed. On the known TSCR-3 date defect, 31 questions assert
the correct `1 November 2022`; several state, in candidate-facing prose, that the corpus register
records `2023-11-01` and is wrong by one year. On the Merchant Shipping Act wrong-Act trap, every
inspected pre-2026 use of "Merchant Shipping Act 2025" is a *guard* — "Neither exists at this
sitting", "Do not import the Merchant Shipping Act, 2025", "the contamination risk does not arise".

This posture is what makes the release recommendation in section J possible. It also means the
corpus jobs below mostly buy **depth and citability**, not **correctness rescue** — with the
specific exceptions named in section C.

---

## C. RELEASE-CRITICAL CORPUS CORRECTIONS

Strictly limited to items where an answer may be materially wrong, misleading or non-defensible,
or where a frozen record will re-inject an error into future work. All three are cheap.

### TS-P01 — Correct the entry into force of `MEPC.328(76)` (TSCR-3)

- **Type:** A · CORRECTION **Effort:** XS (metadata) → S (frozen-record propagation)
- **Release blocker: YES**

**Verified at primary source this session.** `MEPC.328(76)` operative paragraph 3, read from the
held PDF at `true-source/03-imo-instruments/MARPOL-Annex-VI/_base-and-amendments/MEPC.328(76).pdf`:

> …the amendments to MARPOL Annex VI shall enter into force on **1 November 2022** upon its
> acceptance in accordance with paragraph 2 above

Paragraph 2 records deemed acceptance on 1 May 2022. The date is not in doubt.

**TSCR-3 materially understates the defect.** The register describes "three canonical True Source
records". The measured extent is **62 files and 259 occurrences of `2023-11-01`** across the
frozen `TS-MARPOL-VI` build — including `config.json`, `INSTRUMENT_LOG.md`, the freeze record, the
final closure audit, the canonical unit files, and **`12-search-index/QP_REFERENCE_RESOLVER.json`,
which is the layer QP tooling consumes.**

**The corpus is also internally contradictory on this date — three different values:**

| Value | Where |
|---|---|
| `2023-11-01` | 62 files, 259 occurrences (metadata, resolver `sourceState`, freeze records) |
| `1 November 2022` | `MARPOLVI_REG22.json`, resolver provision reasoning, `MEPC.328(76).pageindex.json` |
| `EIF 2023-01-01… VERIFY 2022-11-01` | `10-amendment-register/AMENDMENT_REGISTER.md` line 30 — a **third** variant |

**Why release-critical.** Two solved answers already consumed it (see section I). It sits inside a
**frozen and qualified** instrument, so nothing downstream flags it and any regeneration re-injects
it. And it is the resolver, not just documentation.

**Scope note for whoever executes it:** the frozen build's temporal reasoning about regulation 28
is correct *as reasoning* and must not be disturbed. What is wrong is the EIF metadata value. This
is a find-and-correct with a per-file read, not a rebuild.

- **Affects:** 39 answers sit in the corrupted window (Jan–Nov 2023 sittings); 47 answers name
  `MEPC.328(76)` directly; **2 answers are wrong today**.
- **Closes:** the TSCR-3 declarations carried in ~10 papers, which currently spend candidate-facing
  words explaining a corpus defect.
- **Risk removed:** temporal — the highest-consequence class in the estate.

### TS-P02 — Mark `MEPC.376(80)` revoked and record `MEPC.391(81)` (TSCR-4)

- **Type:** A · CORRECTION (metadata) + B · MISSING PRIMARY SOURCE (text)
- **Effort:** XS for the log line · S to acquire the resolution
- **Release blocker: YES (the metadata line only)**

`GHG-instruments/INSTRUMENT_LOG.md` lists the revoked `MEPC.376(80)` as `GUIDANCE` with no
supersession note, and routes LCA demand to it — while correctly marking `MEPC.346(78)` as
superseded. Revoked is not superseded. Any sitting after 22 March 2024 that follows the log cites
an instrument withdrawn by the body that made it.

- **Affects:** 18 questions across 17 papers touch the LCA/life-cycle layer.
- **Status verified this session:** still open; `MEPC.391(81)` is still not held.
- **Note:** `QP2507-Q2` already departs from the log deliberately and is correct. The exposure is
  to *future* work and to regeneration, which is why the one-line correction is the blocker and the
  text acquisition is not.

### TS-P03 — Adjudicate `TRAP-RULE-D-FAULT` (TSCR-6)

- **Type:** A · CORRECTION **Effort:** XS **Release blocker: YES**

A negative-knowledge object in the `miw-true-source` `general-average` package asserts that a party
at fault cannot claim contribution in general average. The package's own verbatim `YAR-D` text says
rights to contribution **shall not be affected** by fault, relocating the consequence into remedies
and defences.

A trap object exists to be trusted over a candidate's instinct. A wrong one propagates by design.

- **Affects:** the general-average / salvage / limitation family — **58 questions across 35 papers**
  engage it. Nothing has consumed the gloss yet (`QP2407-Q8` was deliberately written from the
  verbatim rule instead), so this is prevention, and prevention is why it is cheap.
- **Requested:** add a verbatim `YAR-PARAMOUNT` object and restate the trap against it.

---

## D. HIGH-ROI TRUE SOURCE ADDITIONS

Materially improve many answers. **None should delay launch.** Ranked by
answer impact × recurrence leverage ÷ construction effort.

### TS-P04 — SOLAS: rights clearance + provision layer

- **Type:** C · MISSING PROVISION LAYER (**not** a missing source) **Effort:** M
- **Affects: 43 questions across 27 papers, all four years** — the largest single demand in the
  estate.

**This is the finding that most changes the plan.** Forty-three answers say some version of *"MIW
holds no licensed SOLAS text"*. Read literally that suggests acquisition. It is not true in the way
it reads:

- `official-sources/SOLAS_2024-Part1/2/3.pdf` **is held** — the IMO Consolidated Edition 2024,
  556 pages, *"incorporating all amendments in effect on 1 July 2024"*, with a **clean extractable
  text layer** (verified this session by direct extraction of Regulation II-1/29 text).
- Five post-base amendment resolutions are filed and logged.

What is missing is **not the text**. It is (i) a rights position — SOLAS sits at the default
`local-internal-use-only` with no dedicated `source-register.json`, on the
`instrumentsPendingDedicatedRegister` list — and (ii) a provision layer. `FD-RIGHTS-1/2/3` cleared
`TS-MARPOL-VI`, `TS-FSS` and `TS-LSA` and nothing else.

**Acquisition cost is therefore zero, and the effort drops from L to M.** This is the highest-ROI
construction job available.

Scope it to the chapters the estate actually reaches: **I** (surveys and certificates), **III**
(life-saving), **IV** (GMDSS), **V** (safety of navigation), **IX** (ISM mandating hook),
**XI-1/XI-2**, plus **II-1/29, II-1/42 and II-2/10** which are already audited.

**Carry the recorded node defects forward.** `SOLAS-1974/INSTRUMENT_LOG.md` records verified,
unapplied defects in `SOLAS-II1-29-2914`, `SOLAS-II1-29-296` and the `SOLAS-II1-29` parent
(120 mm/230 mm conflation, wrong paragraph pairing). Build the layer from the official text, not
from the RulesApp nodes, or the layer inherits them.

- **Papers:** QP2304, 2306, 2307, 2308, 2309, 2402, 2403, 2404, 2406, 2408, 2409, 2411, 2412,
  2502, 2503, 2504, 2506, 2507, 2508, 2509, 2510, 2511, 2512, 2602, 2603, 2604, 2606.

### TS-P05 — Merchant Shipping Act 1958, working Parts only

- **Type:** B · MISSING PRIMARY SOURCE (with an active wrong-Act inversion) **Effort:** M
- **Affects: 25 questions across 16 papers, all four years.**

The corpus holds the Merchant Shipping Act **2025** and the Coastal Shipping Act **2025**, and not
the 1958 Act — which governs every sitting in the estate before 15 March 2026, i.e. 37 of 39
papers. The specs call this "the standing register inversion of this batch".

The estate is defended against it (section B), so this is not release-critical. What it costs today
is real but bounded: `QP2304-Q4` carries its section numbers as inherited authoritative secondary
from `QP2503-Q9` — a citation chain with no primary anchor at the bottom — and `QP2307-Q1` and
others decline to name a section at all.

Scope per `K-2` in the six-year ranking: **Part IX** (ss. 334–336), **Part XA** (ss. 356J–356L),
**Part XIII** (ss. 390–404), plus the collision-duty and casualty-inquiry Parts. Publicly published
Indian legislation; acquisition is straightforward.

- **Papers:** QP2304, 2307, 2310, 2312, 2402, 2406, 2407, 2409, 2410, 2501, 2502, 2503, 2507,
  2508, 2512, 2602.

### TS-P06 — Marine Insurance Act 1963 + York-Antwerp Rules (1994, 2004, 2016)

- **Type:** B · MISSING PRIMARY SOURCE **Effort:** M
- **Affects: 19 questions across 18 papers, all four years.**

The corpus holds nothing: no Marine Insurance Act 1963, no 1906 UK Act, no York-Antwerp Rules in
any edition. This is the six-year ranking's #1 and it stays high here, though **one place lower
than SOLAS** because SOLAS reaches more solved answers and needs no acquisition.

**Carry all three YAR editions.** The edition is contractual, `QP2312-Q3`'s printed stem names the
1994 Rules, and a 1994-for-2016 substitution is a recorded defect class. This job also supplies the
verbatim `YAR-PARAMOUNT` object that TS-P03 needs.

- **Papers:** QP2301, 2303, 2304, 2311, 2312, 2404, 2406, 2407, 2410, 2411, 2501, 2503, 2506,
  2507, 2508, 2512, 2602, 2606.

### TS-P07 — Extend the resolver beyond MARPOL Annex VI

- **Type:** D · RESOLVER / INDEX GAP **Effort:** S per instrument (ship with each layer)

`12-search-index/QP_REFERENCE_RESOLVER.json` holds **320 objects, every one of them MARPOL
Annex VI, and nothing else.** No ID from SOLAS, ISM, STCW, MLC, LSA, FSS, the Admiralty Act or any
India instrument resolves. Combined with TSCR-2 (no ID→anchor deep link exists for any corpus), the
"Verify source" affordance cannot land on a provision for any instrument.

**Do not run this as a standalone project.** It is the last stage of every layer job above.
Recorded separately so it is costed and not forgotten.

### TS-P08 — ISM Code provision layer

- **Type:** C · MISSING PROVISION LAYER **Effort:** S–M
- **Affects: 17 questions across 14 papers, all four years.**

**The Founder's framing is confirmed: there is nothing to fix in ISM terminology.** The desktop ISM
audit was correct and `594fdcf` ("Cite the ISM Code in the units it actually has") settled it.
The corpus holds the complete official chain — `A.741(18)` base plus `MSC.104(73)`, `MSC.179(79)`,
`MSC.195(80)`, `MSC.273(85)`, `MSC.353(92)`, and `A.1184(33)` guidance — with a clean amendment
cutoff statement. What it does not hold is any provision-level representation.

**Answering the question that was asked — does it justify priority?** On measured impact: it ranks
**fifth**, behind SOLAS, MSA 1958 and marine insurance. Seventeen questions currently say some form
of *"the ISM Code is referred to at regime level only, no provision number is asserted"*. A
provision layer converts those to clause-level citation, and the source is already held and clean,
so the effort is small. **Build it — but after TS-P04, and not before it.** It does not warrant
displacing the larger gaps, and it is not release-critical.

- **Papers:** QP2303, 2306, 2308, 2309, 2311, 2312, 2403, 2404, 2408, 2411, 2412, 2502, 2510, 2606.

### TS-P09 — India secondary layer: DG Shipping circulars and MS Rules

- **Type:** B/C **Effort:** M · **Affects: 18 questions across 12 papers, all four years.**
- Papers: QP2307, 2404, 2409, 2503, 2504, 2507, 2509, 2511, 2512, 2601, 2603, 2604.

### TS-P10 — STCW provision layer

- **Type:** C · MISSING PROVISION LAYER **Effort:** M · **Affects: 14 questions across 13 papers.**
- `official-sources/STCW-2017.pdf` is held, plus the `MSC.416/417(97)`, `MSC.486/487(103)`,
  `MSC.560(108)` chain and two PQ supplements. Same shape as SOLAS: text present, layer absent.
- Papers: QP2303, 2309, 2404, 2409, 2411, 2506, 2508, 2509, 2512, 2601, 2602, 2604, 2606.

### TS-P11 — III Code / RO Code / IMSAS framework resolutions

- **Type:** B · MISSING PRIMARY SOURCE **Effort:** S · **Affects: 14 questions across 12 papers.**
- The recurring limitation is specific and narrow: *"MIW holds no copy of any resolution setting
  out the Framework and Procedures for the IMO Member State Audit Scheme"*, so no resolution number
  and no audit periodicity can be asserted. A small, bounded acquisition.
- Papers: QP2302, 2306, 2308, 2309, 2401, 2403, 2408, 2411, 2412, 2503, 2507, 2510.

### TS-P12 — Liability convention texts, with **dated** status facts

- **Type:** B · MISSING PRIMARY SOURCE **Effort:** M · **Affects: 12 questions across 12 papers.**
- `05-un-and-treaty-law/liability-and-compensation/` holds **no document at all** — an
  `INSTRUMENT_LOG.md` and a `manifest.json`, nothing else. Its status facts are dated 2026
  ("12 contracting States as of April 2026", "VERIFY figures before citing numerically"), which is
  forward-contamination for every historical sitting. **Text plus per-date status fixes both.**
- Papers: QP2301, 2303, 2306, 2307, 2406, 2409, 2503, 2506, 2507, 2508, 2509, 2602.

### TS-P13 — HSSC survey guidelines, operative editions

- **Type:** B · MISSING PRIMARY SOURCE **Effort:** S · **Affects: 11 questions across 8 papers.**
- The corpus holds only the 33rd-Assembly successors `A.1185(33)`, `A.1186(33)`, `A.1187(33)`. The
  edition operative at the 2023 and 2024 sittings — `A.1155(32)` / `A.1156(32)` — is absent, so
  `QP2304-Q9` names it and asserts nothing from it. Two short resolutions.
- Papers: QP2303, 2304, 2308, 2309, 2312, 2403, 2412, 2510.

### TS-P14 — Resolve duplicate `object_id`s in the new corpus repository (TSCR-5)

- **Type:** D · RESOLVER / INDEX GAP **Effort:** XS–S
- `ROT-ART-1` resolves to three different definitions, `SALV-ART1` to two, `WRC-ART1` to three.
  The citation primitive does not identify a proposition. No shipped answer cites an affected
  object, but **no future paper drawing on `salvage`, `wreck-removal` or `contract-of-carriage` can
  be given source traceability until it is fixed** — 26 questions across 19 papers already engage
  that subject area.

---

## E. DEFERRED SOURCE WORK

Adequately covered by the answers as written, or low impact for the cost.

| Job | Type | Qs | Papers | Why deferred |
|---|---|---|---|---|
| Gas/bulk/chemical codes (IGF, IGC, IMSBC, IMDG, IBC, ESP) | C | 11 | 8 | IMDG 2024, IGC, IGF, IMSBC, IBC all **held**; demand is shallow and per-code |
| AFS / BWM / Hong Kong Convention | B/C | 11 | 11 | HKC held; AFS and BWM demand is regime-level and answered as such |
| Port State Control regime (Tokyo/Paris MOU) | E-adjacent | 10 | 9 | MOU documents are third-party; `A.1185(33)` is held and carries the IMO layer |
| MARPOL Annexes I/II/IV/V | C | 9 | 8 | Consolidated MARPOL 2022 + Annex I/II folders held; provision layer only |
| Carriage regimes (Hague-Visby, Hamburg, Rotterdam) | B | 8 | 8 | Partly served by the `contract-of-carriage` package once TSCR-5 is fixed |
| Salvage Convention 1989 / LOF / SCOPIC / Nairobi | B | 7 | 7 | `salvage` and `wreck-removal` packages exist; blocked on TSCR-5, not on acquisition |
| Human-element circulars (`MSC.1/Circ.1598`, `A.947(23)`) | B | 6 | 6 | MLC 2006 + 2022 amendments held; circulars are recommendatory |
| UNCLOS indexing | D | 6 | 6 | Full 202-page convention **held**; indexing only, and demand is low in the solved estate |
| Load Line / Tonnage | C | 2 | 2 | Load Line 2021 held; two questions |
| Casualty Investigation Code | migration | 2 | 2 | Validated package exists in `Knowledge Central/` — **migration, not build** |

---

## F. EXTERNAL / NON-CORPUS LIMITATIONS

**Do not propose building these into True Source.** All are proprietary or licensed. Recorded so
the demand is visible and so no future session mistakes them for corpus gaps.

| Domain | Qs | Papers | Position |
|---|---|---|---|
| **IACS** — Unified Requirements, URs, CSR, procedural documents | **16** | 10 | `07-iacs-and-class/` holds one notes file. IACS documents are member-restricted. Answers correctly grade the whole area P3 industry guidance. **Highest external demand in the estate** — worth a Founder decision on whether any licensed subscription is wanted, but not a construction job |
| **ISO / quality-management standards** | 11 | 8 | Priced standards. `QP2303-Q7` handles it correctly: defines correction / corrective action / preventive action by what each acts upon and attributes them to no standard number |
| **Manufacturer / OEM / trial data** — efficiency-device gains, coating service life, shop-test figures | 10 | 6 | Commercial literature. Answers state these as claims and make nothing depend on a figure. This is the correct treatment and needs no corpus response |
| **P&I club rules / International Group** | 4 | 4 | Club rules are contractual and member-facing |

---

## G. MINIMUM VIABLE TRUE SOURCE SET

The smallest set that removes the most risk and improves the most answers:

```
TS-P01 → TS-P02 → TS-P03 → TS-P04 → TS-P05 → TS-P06 → TS-P07
```

- **TS-P01 · TS-P02 · TS-P03** are the release gate. All three are XS-class corrections. Together
  they cost a fraction of a session and remove every identified material-correctness risk.
- **TS-P04 · TS-P05 · TS-P06** are the enrichment core: **87 questions across 35 distinct papers**
  after de-duplication.
- **TS-P07** ships inside each of TS-P04/05/06 rather than after them.

**Stop there and reassess.** TS-P08 onward should be re-ranked against a re-measured estate once
the core lands, because closing SOLAS will change what the remaining limitation text says.

---

## H. IMPACT MAP

Full question-level lists are in the JSON companion under `jobs[*].question_ids`. Summary:

| Job | Type | Effort | Questions | Papers | Years | Blocker |
|---|---|---|---|---|---|---|
| TS-P01 `MEPC.328(76)` EIF | A | XS→S | 2 wrong · 39 in window · 47 citing | 10 / 21 / 27 | 4 | **YES** |
| TS-P02 LCA revocation | A(+B) | XS(+S) | 18 | 17 | 4 | **YES** (metadata) |
| TS-P03 Rule D trap | A | XS | 58 exposed · 0 consumed | 35 | 4 | **YES** |
| TS-P04 SOLAS layer | C | M | **43** | 27 | 4 | no |
| TS-P05 MSA 1958 | B | M | 25 | 16 | 4 | no |
| TS-P06 MIA 1963 + YAR | B | M | 19 | 18 | 4 | no |
| TS-P07 Resolver extension | D | S each | enables all | — | — | no |
| TS-P08 ISM layer | C | S–M | 17 | 14 | 4 | no |
| TS-P09 India secondary | B/C | M | 18 | 12 | 4 | no |
| TS-P10 STCW layer | C | M | 14 | 13 | 4 | no |
| TS-P11 III / RO / IMSAS | B | S | 14 | 12 | 3 | no |
| TS-P12 Liability texts + dated status | B | M | 12 | 12 | 4 | no |
| TS-P13 HSSC operative editions | B | S | 11 | 8 | 3 | no |
| TS-P14 Duplicate `object_id`s | D | XS–S | 26 exposed · 0 consumed | 19 | 4 | no |

**Counts do not sum to 351 and must not be added.** A question with three declared source gaps
appears under three jobs. The de-duplicated reach of TS-P04+P05+P06 is 87 questions / 35 papers.

---

## I. QP CORRECTION REFERRALS

### `QP_CORRECTION_REQUIRED` — QP2502-Q1 and QP2502-Q6

**Not fixed in this session.** Recorded for the laptop review/integration stream.

| Field | Value |
|---|---|
| Paper | QP2502 (February 2025), authoritative on `origin/main` |
| Questions | `QP2502-Q1` (IMO Structure and the Instrument Hierarchy), `QP2502-Q6` (EEDI Verification of a New Ship) |
| Defect | Both assert that the revised MARPOL Annex VI adopted by `MEPC.328(76)` is **"in force 1 November 2023"** / **"in force since 1 November 2023"**. The correct date is **1 November 2022**, on the face of the resolution's own operative paragraph 3 |
| Extent | Five unqualified occurrences in each question — in candidate-facing model-answer prose, in the `regulations` list, in retrieval/revision cards, and in the source list |
| Aggravating | `QP2502-Q1` grades the claim **`P1 PRIMARY VERIFIED (corpus holding)`**. It is not primary-verified; it is the TSCR-3 corpus error, consumed and then labelled primary |
| Why it slipped | Neither question mentions TSCR-3, and neither carries the `1 November 2022` date anywhere. Every other paper that touched the date declared the defect and rejected it |
| Conclusion inverted? | **No.** At a February 2025 sitting the Annex is in force on either date, so no downstream reasoning is wrong. The **stated fact** is wrong, is presented to candidates as primary-verified, and is exactly the failure class TSCR-3 predicted |
| Recommended fix | Correct both to 1 November 2022; re-grade the `QP2502-Q1` source claim; add the TSCR-3 declaration these two questions lack |

**This is the only material correctness defect found.** It was found by targeted test, not by a
general QA sweep — answer quality was not re-audited in this session, per scope.

### Observation (not a defect) — evidence-grade vocabulary

See section B. Normalising the `sources` grading vocabulary is a QP metadata job, XS–S, no
correctness impact, not a blocker.

---

## J. RECOMMENDED RELEASE DECISION

> **Can the written-QP product reasonably proceed to release after laptop review/integration,
> before all high-ROI True Source enrichment is complete?**

# YES — conditional on TS-P01, TS-P02, TS-P03 and the QP2502 correction.

The evidence, not the preference:

1. **The estate declares its limits instead of overstating.** 790 source-gap items across 351
   questions are written into the product as explicit limitations. An answer that says *"no GMDSS
   carriage requirement or SOLAS chapter IV regulation number is asserted"* and then answers by
   function and management measure is **defensible**, not defective. That is the difference between
   an evidence limitation and a correctness failure, and section 11 of the audit brief asks
   precisely that they not be conflated.

2. **The known corpus defects were resisted, not absorbed.** Directly tested on the two worst
   traps. On TSCR-3, 31 questions carry the correct date and several warn the reader about the
   register in candidate-facing prose. On the wrong-Act inversion, every inspected pre-2026 use of
   the 2025 Act is a guard against it.

3. **Exactly one material defect was found in 351 questions**, it is confined to two questions on
   one paper, and it does not invert either answer's conclusion.

4. **The release gate is cheap.** All three release-critical items are XS-class corrections to
   metadata and one glossary object. None requires construction, acquisition or a rebuild. There is
   no argument for shipping without them and no reason they should delay anything.

5. **The high-ROI work buys citability, not correctness.** TS-P04 through TS-P14 move answers from
   "correct, and honest that it cannot quote the provision" to "correct, and quotes the provision".
   That is a product-depth improvement on a defensible base — the right thing to do after launch,
   with a re-enrichment queue already defined, and the wrong thing to block launch on.

**What must NOT ship:** QP2502-Q1 and QP2502-Q6 in their current form.

**Caveat, stated plainly.** This audit examined True Source demand only. It did not re-audit prose,
depth, marks, UI or flashcards, per the scope given. This recommendation is therefore about
**source defensibility**, and it assumes the laptop review/integration stream clears the quality
dimensions it owns.

---

## K. RE-ENRICHMENT QUEUE

After any corpus job, run this — and **only** this. A corpus job is not a licence to regenerate
the estate.

```
1. CONSTRUCT / FIX      the corpus unit                        (producer team, corpus repo)
2. VALIDATE             validate-derivatives.ps1 + the unit's own validation gate
3. IDENTIFY             read jobs[TS-Pxx].question_ids from the JSON companion
4. RE-VERIFY            re-run source/provenance verification on THOSE answers only
5. UPDATE               the affected specs' sources / unresolved /
                        reverify_before_publication / regulations fields
6. REBUILD              only the affected papers' delivery outputs, then the seven
                        global derived artefacts, in the governed order
```

Per-job specifics:

| Job | Step 3 list | Step 4 depth |
|---|---|---|
| TS-P01 | 47 questions naming `MEPC.328(76)` | Temporal only — confirm each carries 1 Nov 2022 and drop the now-stale TSCR-3 declarations |
| TS-P02 | 18 LCA questions | Instrument identity only — `MEPC.376(80)` → `MEPC.391(81)` where the sitting is after 22 Mar 2024 |
| TS-P03 | 58 GA/salvage questions | **Read-only confirmation** that none consumed the gloss. Expected result: no edit |
| TS-P04 | 43 SOLAS questions | Full source re-verification — these answers can newly cite provisions |
| TS-P05 | 25 MSA questions | Section-number verification; retire the `QP2304-Q4` inherited chain |
| TS-P06 | 19 insurance/GA questions | Full — plus confirm the YAR edition per paper |
| TS-P08 | 17 ISM questions | Clause-level citation upgrade |

Steps 5 and 6 are the expensive ones. Do not run them for a job whose step 4 produced no change.

---

## L. VALIDATION OF THIS AUDIT

| Check | Result |
|---|---|
| Every priority maps to real question IDs | **PASS** — all IDs machine-extracted from authoritative specs, carried in the JSON companion |
| No duplicate jobs | **PASS** — jobs are keyed by instrument/package; TSCR-3/4/6 appear once each |
| Impact counts reconcile | **PASS** — counts are per-job and overlapping **by design**; stated as non-additive in section H |
| Integrated-vs-review deduplication proved | **PASS** — 34 from `origin/main` + 5 branch-only = 39, one provenance line per paper |
| No corpus modifications | **PASS** — `D:\RulesApp-Local-Input` at `319524c`, tracked tree clean |
| No QP spec modifications | **PASS** — this branch adds two files under `docs/` and touches nothing else |
| No global derived artefacts changed | **PASS** — no build, no regeneration, no tool run that writes |
| Staging | Explicit per-path. `git add -A` was not used |

**Known limits of this audit, stated so they are not mistaken for coverage:**

- Instrument attribution is by regex over declared limitation text. A limitation that names no
  instrument is not attributed to one; 790 gap items were classified and the long tail is thinner
  than the head.
- Impact counts measure **declared** demand. A question whose author silently omitted a provision
  without recording it is invisible to this method.
- Section B's evidence profile is deliberately incomplete — the reason is given there.
