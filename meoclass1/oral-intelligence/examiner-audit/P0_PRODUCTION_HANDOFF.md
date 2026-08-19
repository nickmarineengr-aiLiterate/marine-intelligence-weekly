# Oral P0 production handoff — Desktop → Laptop

**Branch:** `prod/oral-p0-pre24aug`
**Cut from:** `origin/main` @ `0242774` (not the approved `81ba223` — see §0)
**Commits:** `ac66d5b` (batch 1) · `9197a98` (batch 2) · `34a3f19` (batch 3)
**Scope:** the nine Laptop-approved P0 items and nothing else. No tenth item.

**Desktop verdict: GO for content review — with five red gates that Laptop must
close during integration, three of which Desktop is forbidden to touch.** See §4.
Read §4 before merging.

---

## 0. Repo truth

`origin/main` had moved one commit past the approved Stream-B baseline:

| | SHA | |
|---|---|---|
| Laptop-approved baseline | `81ba223` | Publish Examiner Index V2 Release A |
| Actual `origin/main` at session start | `0242774` | fix(storefront): correct the stale oral statistics and guard them |

The delta touches `SQ/index.html`, `SQ/pay.html`, `SQ/trial.html`,
`meoclass1/oralnotes/index.html`, `tools/oral/mutate_examiner_index.py`,
`tools/oral/validate_examiner_index.py`. **No P0 target or source QB page is in
it**, so production continued from current main and the delta is recorded here.

One consequence was foreseen at the start and has materialised: `0242774` added a
guard asserting that the SQ storefront's advertised oral-question count equals the
live corpus. Adding P0 questions changes that count. See §4.

Pre-flight condition 4 from the Laptop release review (`.gitignore` to cover
`docs/MIW-master-Question-bank/*.docx`) was already satisfied on main — verified
with `git check-ignore`.

---

## 1. The nine-item matrix

| P0 | Examiner | Actual ask | Production type | Target | New/enriched |
|---|---|---|---|---|---|
| GAP-0002 | Simon ×3 | What is girding? | NOTES→QB promotion | `QB1_K#q9` | new card from Notes |
| GAP-0034 | Simon ×2 | Dual fuel **and trifuel** engine | ENRICH | `QB6#q10` | tri-fuel limb added |
| GAP-0043 | Nair ×2 | Qualities of CE — assertiveness, empathy | ENRICH | `QB5_B#q4` | both limbs added |
| GAP-0409 | Nair ×1 | ME-GA — **convince the owner to invest** | ENRICH | `QB7_I#q2` | commercial limb added |
| GAP-0016 | John ×2 | BWM Convention status + content + G7/G8/G9 | NEW | `QB1_A#q31` | new card |
| GAP-0042 | Nair ×2 | Conflict incl. bullying/harassment, SMS, latest amendments | NEW | `QB5_D#q3` | new card |
| GAP-0048 | Nair ×2 | Second class society, IACS, Indian ROs, IRS mandatory? | NEW | `QB4_A#q21` | new card |
| GAP-0044 | Nair ×2 | STCW courses 2/E → CE | NEW | `QB4_A#q22` | new card |
| GAP-0410 | Nair ×2 | BWTS/UV new tech, D-2 onboard, US requirements | NEW | `QB3_J#q6` | new card |

**5 new answers · 3 enrichments · 1 promotion — as approved. No production type
was changed.**

---

## 2. Item-by-item

### GAP-0002 — girding (NOTES→QB promotion)

- **Notes source:** `meoclass1/oralnotes/simon-notes-p2.html#n9`, "Tug Girding —
  Capsizing Risk", page badge P.31.
- **Reused as written:** the definition (tug pulled beam-on by the towline) and
  the four influencing factors — suitability of the tug, towline length, towing
  point location, environmental conditions.
- **Adapted:** the Notes' SOLAS V/34 and ISM element 7 references are carried over;
  the Notes' own caution about the ICS reference was respected by **not** carrying
  that citation into the QB card.
- **Newly authored and verified:** the heeling couple (towline pull at the towing
  point against water resistance at the centre of lateral resistance); why the tug
  cannot recover once girded; tractor/ASD towing-point geometry; prevention (ship's
  speed, gog rope, quick-release hook, rendering winch); immediate actions; and the
  2008 IS Code (Res. MSC.267(85)) Part A §2.4 towing/escort stability criteria as
  the instrument governing tug stability.
- **Judgement carried:** the release decision is framed on **rate of increase of
  heel**, not an absolute angle, because no such angle exists to memorise.
- **Placement:** `QB1_K` — the stability/surveys file, and Simon's file. Girding is
  a stability failure produced by a towing geometry, so it belongs with stability
  rather than with LSA or cargo.
- **Provenance:** `data-examiner="Simon" data-examiner-confidence="confirmed"` on
  the card. **No "Simon Sir" appears in candidate-facing question text.**

### GAP-0034 — tri-fuel (ENRICH `QB6#q10`)

- Confirmed absent: "trifuel" appears nowhere in the corpus.
- Added: three fuels not two; **HFO in diesel mode** is the defining distinction;
  **TFDE** (Tri-Fuel Diesel Electric) as the term met in service on LNG carriers;
  boil-off gas as the fuel that must be dealt with regardless; DFDE vs TFDE kept
  apart; ~25–30% efficiency gain over the steam turbine displaced; one trap Q.
- Untouched: the entire dual-fuel answer, the 20%/40% LEL thresholds, IGF Ch.13/6,
  the LPG bunkering material, STCW V/3.
- Question text widened to name tri-fuel, so the card is findable for the real ask.

### GAP-0043 — assertiveness and empathy (ENRICH `QB5_B#q4`)

- Confirmed absent: zero occurrences of "assertive"; empathy present only as a
  one-line Goleman EI table row.
- Added: a qualities-of-a-CE list; **assertiveness** on the passive/assertive/
  aggressive scale, as the authority-gradient countermeasure, explicitly a
  competency under **STCW Table A-III/2** and Model Course 2.07, with **graded
  assertiveness (PACE — Probe, Alert, Challenge, Emergency)** named and given an
  engine-room example; **empathy** separated from sympathy and from agreeing; the
  paired framing (assertiveness without empathy = aggression, empathy without
  assertiveness = passivity); one trap Q on assertiveness vs insubordination.
- Untouched: all five leadership theories, the tables, the deep-dive, On My Vessel.

### GAP-0409 — owner investment case (ENRICH `QB7_I#q2`)

- **No new ME-GI/ME-GA card was created.** The existing card already covers the
  family evolution correctly and currently, and the two engines are not collapsed.
- The missing limb was commercial. Added: the five arguments an owner acts on
  (regulatory survival, charterer demand and asset value, total cost of ownership,
  avoiding a mid-life retrofit, honest risk disclosure) and the CE's actual role as
  supplier of operating evidence.
- **Current-position handling:** the card refuses to make an investment case for
  the ME-GA, because MAN discontinued the line in November 2024, and redirects to
  ME-GI or ME-LGIM. The examiner's ask is preserved; the answer is today's.

### GAP-0016 — BWM Convention (NEW `QB1_A#q31`)

- **Cross-link condition met.** Three `href="#q30"` links: an opening pointer, a
  pointer inside the CE tip, and a closing Related line.
- **MEPC 84 duplication avoided.** No `MEPC.4xx(84)` resolution is restated. The
  D-2.3, E-1.4.3, 2016 G8 / BWMS Code unified interpretation and 2026 G4 material
  appears **only** as a signpost naming Q30 as its home, with an explicit "that
  material is not repeated here".
- Content is the Convention itself: adoption 13 Feb 2004, entry into force
  8 Sep 2017, Articles + Annex Sections A–E with the regulations in each; B-3
  phase-in and its completion on **8 Sep 2024** (the actual answer to "present
  condition"); D-1 vs D-2 with both figure sets; the three guidelines with
  resolutions; the G8-vs-G9 distinction (**UV uses no Active Substance so it does
  not go through G9**); four trap Qs.
- **Placement rationale:** QB1_A is the Conventions file *and* holds the mandated
  cross-link target, so the link is in-file rather than cross-file.

### GAP-0042 — harassment, SMS, latest amendments (NEW `QB5_D#q3`)

- Placed beside the existing women-at-sea question (`QB5_D#q2`), which is a related
  but different ask, and pointing at `QB5_B Q2` for general conflict technique
  rather than restating it.
- Spine: this is **not conflict to be mediated** — it is prohibited conduct to be
  stopped, recorded and escalated, and compromise is the wrong outcome where there
  is a power imbalance. Seven-step CE action sequence; SMS machinery named by its
  correct unit (MLC Reg. 5.1.5; **ISM elements** 2, 4, 5, 6, 9 — not "regulations").
- **Two amendment layers kept apart:** 2022 package **IN FORCE 23 Dec 2024**;
  April 2025 ILO STC package **adopted, NOT in force**, expected ~Dec 2027.

### GAP-0048 — second class society / IACS / Indian ROs (NEW `QB4_A#q21`)

- Placed beside `QB4_A#q8` (Flag State vs RO) and `#q9` (Condition of Class), both
  cross-linked.
- Class-vs-statutory table; seven accepted reasons for a second society; the
  explicit correction that dual class is **harder and dearer, not softer**.
- IACS: 1968, **12 members**, >90% of cargo-carrying tonnage, NGO with consultative
  status, **not part of IMO**; RS withdrawn 11 Mar 2022.
- **Two limbs deliberately answered by mechanism, not by a number** — see §3.

### GAP-0044 — STCW 2/E → CE (NEW `QB4_A#q22`)

- The examiner "wanted more" after simulator/preparatory/HV/tanker. What was
  missing was **structure**, so the answer is four layers plus a national layer:
  III/2 certificate and Table A-III/2 at **3,000 kW propulsion power or more**;
  Chapter VI set; management-level ERM and leadership from the 2010 Manila
  amendments; Chapter V ship-type training; then DGS preparatory/simulator named
  explicitly as **national, not STCW**.
- The two commonly-omitted limbs are carried: the **five-yearly refresher** cycle
  and **Reg. V/3** for low-flashpoint-fuelled ships.
- Polar **V/4 is stated as directed at masters and deck officers**, not claimed as
  an engineer's certificate.

### GAP-0410 — BWTS / UV / D-2 (NEW `QB3_J#q6`)

- Kept **distinct from GAP-0016** and cross-referenced to it, exactly as the
  adjudication resolved: Q31 answers the Convention, this card answers technology
  and onboard verification.
- Limb 1: UV-LED, UVT-driven dose control, reactor/filter improvements.
- Limb 2 — the load-bearing one: **the ship cannot measure D-2**. Compliance is
  demonstrated by operation within the **System Design Limitations**, the control
  and monitoring record, sensor calibration, and a complete BWRB. Indicative tools
  framed as an operational check, **not** proof. G2 (MEPC.173(58)) detailed
  analysis is a port State / accredited-lab activity. Contingency by the BWMP.
- Limb 3: **UV systems do hold USCG type approval** (first, December 2016). The
  reason it was ever in doubt is IMO *viable* (MPN) vs USCG *living* (FDA/CMFDA),
  MPN having been rejected by the USCG in 2016, requiring roughly **2–3× the dose**.
  Two approvals needed for US trading; AMS described as a lapsed bridge; VIDA named.
- **No false D2 match reused.** The Situational Leadership "D2 development level"
  in `QB5_B` is untouched and unreferenced.

---

## 3. Numbers deliberately NOT stated

Two limbs were answered by naming the mechanism rather than quoting a figure,
because no authoritative current figure could be verified:

1. **How many ROs India recognises.** DG Shipping publishes the authorised list by
   circular and it changes. The card teaches the candidate to cite the
   authorisation framework (Merchant Shipping Act + RO Code) and say they would
   confirm the current circular. Inventing this number is the failure the question
   is built to produce.
2. **The current DGS MEO Class I course syllabus and durations.** Named as revised
   by circular, with the same instruction to confirm.

`IRS is mandatory for Indian-flag ships` is answered **No** — the ship must use a
DGS-recognised organisation and IRS is one of them.

---

## 4. Validation — including what is RED

### Green

- **QB structural gates** — the repo's own `meoclass1/qb_health_check.py` checkers
  (`check_file`, `check_manifest`, `check_index_linkage`, notes and SQ checkers)
  run against the working tree via a local harness, because the committed script
  only ever fetches GitHub `main`. **No new error group relative to a baseline
  captured on `0242774` before any edit.** 104 pre-existing advisory groups in,
  104 out.
- **Anchors** — no duplicate `q-card` id in any of the eight touched files.
- **Internal links** — zero broken `href="#…"` across all eight files.
- **Candidate text hygiene** — no `GAP-…`, `P0`, `ASC-…`, "Simon Sir"/"Nair Sir",
  examiner context or production status in any candidate-facing question text.
- **Forbidden surfaces** — `git diff --name-only origin/main...HEAD` returns only
  eight QB files, `index.html` and `qb_content_index.json`. `examiner-index.html`,
  `SQ/`, payments, `pastpapers/`, `articles/`, magazine, Written QI and the matcher
  (`tools/oral/*`) are all untouched.

### RED — five failures Laptop must close

`tools/oral/validate_examiner_index.py`: **origin/main = 52 PASS / 0 FAIL;
this branch = 47 PASS / 5 FAIL.** All five are downstream consequences of adding
questions, not content defects, and **Desktop cannot fix three of them without
touching a forbidden surface.**

| # | Failure | Cause | Who fixes |
|---|---|---|---|
| 1 | snapshot ≠ fresh resolve of canonical data | new anchors exist that the Release-A snapshot predates | **Laptop** — regenerate the examiner index |
| 2 | rendered text ≠ live question text — `QB6#q10`, `QB5_B#q4` | both question texts were widened by the approved enrichments; the generator takes display text from the live question | **Laptop** — same regeneration |
| 3 | SQ `data-oral-questions` attribute ≠ corpus — 682 vs 688 | six new canonical questions | **Laptop** — `SQ/index.html` is forbidden to Desktop |
| 4 | SQ `data-oral-questions` visible text ≠ attribute — 682 vs 688 | same | **Laptop** |
| 5 | SQ prose oral-question claim ≠ corpus — 682 vs 688 | same | **Laptop** |

Failures 3–5 are the guard added by `0242774` doing exactly its job. The corpus
moves 682 → **688** canonical questions (the manifest total moves 684 → **690**;
the two figures differ by the two non-question revision cards in `QB1_A`,
`#family-trees` and `#dependency-graph`).

**This means the brief's conditional next action is now unconditional: the new QB
anchors DO require the examiner index to be regenerated.**

---

## 5. Anchors and placement

| File | Anchor | Placement rationale |
|---|---|---|
| `QB1_K` | `#q9` | stability/surveys file; Simon's file; girding is a stability failure |
| `QB1_A` | `#q31` | Conventions file, and holds the mandated `#q30` cross-link target |
| `QB5_D` | `#q3` | Management/Human Element; adjacent to the related women-at-sea card |
| `QB4_A` | `#q21`, `#q22` | ISM/ISPS/MLC/STCW file; q21 sits beside the RO and Condition-of-Class cards, q22 beside the Manila-amendments card |
| `QB3_J` | `#q6` | MARPOL/environmental file; the operational counterpart to the QB1_A convention card |

No existing question or anchor was renumbered. In `QB1_A` the two named-anchor
revision cards moved from manifest `qnum` 31/32 to 32/33 so manifest order still
matches page order; their anchors are `#family-trees` and `#dependency-graph`, so
**no candidate link changed**.

---

## 6. Sources used

IMO (BWM Convention and Guidelines page — the G1–G14 resolution table; Implementing
the BWM Convention — B-3 schedule, 8 Sep 2024, full D-2 limits), IMO RO Code
material (MSC.349(92)/MEPC.237(65), in force 1 Jan 2015), US Federal Register and
USCG type-approval records (FDA/CMFDA vs MPN, 2016 MPN rejection, December 2016 UV
type approvals), ILO/DNV (MLC 2022 amendments in force 23 Dec 2024; April 2025 STC
package not yet in force), IACS membership records, and maritime engineering
sources for TFDE and graded assertiveness. Existing MIW canonical material was
reused in preference to rewriting — notably `QB1_A#q30` for the MEPC 84 layer,
`QB7_I#q2` for the ME-Gx families, and `simon-notes-p2.html#n9` for girding.

Candidate feedback was used **only** to establish what was asked.

---

## 7. What Laptop should check hardest

1. **The five red gates in §4** — specifically that regenerating the examiner index
   and updating the SQ figures to 688 is the intended integration step, and that
   688 is the number you agree with.
2. **GAP-0016 §** — that the cross-link satisfies the condition and that nothing in
   Q31 duplicates Q30 in substance.
3. **GAP-0409** — that the refusal to make an investment case for a discontinued
   ME-GA is the answer you want a candidate giving, rather than a neutral
   business-case recital.
4. **The two withheld numbers in §3** — if you hold a current DGS RO figure, it can
   be dropped straight into `QB4_A#q21`.
5. **GAP-0002 placement** — `QB1_K` was chosen over the QB2 (LSA) and QB9 (casualty)
   families; confirm that is the taxonomy you want for tug stability.
