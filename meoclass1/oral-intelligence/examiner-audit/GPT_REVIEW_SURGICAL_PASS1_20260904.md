# GPT Independent Review — Surgical Correction Pass 1

**Date:** 2026-09-04
**Reviewed commit:** `9e26f02` (published; `origin/main` == local `HEAD` at review time)
**Correction id:** `CORR-GPT-PASS1-20260904`
**Scope:** deliberately surgical. Three candidate-facing cards, one source-governance
tranche, one governance-residue adjudication, one placeholder audit, one recommendation.
No new cards, no style regeneration, no Excel distribution, no full deep suite.

---

## 0. Authorisation

Founder/GPT independently inspected the published repository — live card bytes plus
authoritative external sources — and returned a bounded finding list. This document is
the authorisation record for `CORR-GPT-PASS1-20260904` and is the
`authorisation_source` named in
`tools/oral/correction_corr_gpt_pass1_20260904_manifest.json`.

The review's own instruction governs the shape of the work: *correct only the authorised
items, plus directly propagated copies of the exact same proposition where governance
requires consistency.* Where a related defect was found outside that boundary it is
**reported here and deliberately not edited**, following the precedent set by
`CORR-ISM-SPARES-20260902`.

---

## 1. `QB5_J#q2` — main engine underperformance

The diagnostic spine (baseline → normalise → engine parameters → localise → confirm) was
accepted and is unchanged. Two overstatements were corrected.

### 1A. NOx Technical File / EIAPP

**Rejected proposition.** Four locations asserted, in substance, that going outside the
identified Technical File settings/components *invalidates the EIAPP certificate*.

**Primary authority — read, not recalled.** The NOx Technical Code 2008 is held at
`03-imo-instruments/MARPOL-Annex-VI/_base-and-amendments/MARPOL_Annex_VI_and_NOx_Technical_code_2008_5th_Ed_2023.pdf`.
**It is an image-only scan: 535 pages, zero text layer.** The provisions below were
obtained by an OCR pass over the page images at 350 dpi.

| Provision | What it actually says |
|---|---|
| NTC 2008 **2.4.1.1** | the technical file identifies *"those components, settings and operating values of the engine that influence its NOx emissions including any NOx-reducing device or system"* |
| NTC 2008 **2.4.1.2** | it also identifies *"the full range of allowable adjustments or alternatives for the components of the engine"* |
| NTC 2008 **2.4.3.1** / **6.1.1.1** | the engine parameter check method verifies *"that an engine's component, setting and operating values have not deviated from the specifications in the engine's technical file"* |
| NTC 2008 **2.4.4** | a changed verification method is *"added as an amendment to the technical file or appended as an alternative"*, approved by the Administration |
| NTC 2008 **6.2.1.1.2** | engines *"that have undergone modifications or adjustments to the designated engine components and adjustable features since they were last surveyed"* are **eligible for** the parameter check method |
| NTC 2008 **6.2.1.2** | the limit *"may, however, be contravened by adjustments or modification to the engine. Therefore, an engine parameter check method shall be used to verify whether the engine is still within the applicable NOx emission limit."* |

**Why the original was wrong.** 2.4.1.2 means some adjustment is expressly allowed, so a
departure cannot be automatically fatal; and 6.2.1.1.2 treats an already-modified engine
as a normal survey subject rather than an uncertificated one. The consequence of an
unapproved departure is **verification against the limit at survey**, and the risk is
**non-compliance with the certified NOx configuration** — not instant invalidation.

**Corrected propositions (both locations).** The Technical File *defines* the approved
NOx-relevant components, settings and operating values and the full range of allowable
adjustments; departure from the approved configuration must follow the applicable
approved procedure, verification or survey route; an unapproved departure *can render*
the engine non-compliant with its certified NOx configuration. The practical oral warning
is preserved verbatim in effect: **do not re-time or change NOx-critical settings casually
to chase performance.**

### 1B. ISO 19030

**Rejected proposition.** ISO 19030 is *"the standard method for separating hull fouling
from engine deterioration"* — which promotes the standard beyond its own scope and implies
it diagnoses engine condition.

**Corrected proposition.** ISO 19030 provides a framework for measuring **changes in hull
and propeller performance**; read together with corrected engine-performance data it helps
distinguish the hull and propeller contribution from machinery deterioration. The reg-box
now states explicitly that **it does not itself assess engine condition.**

Preserved: hull/propeller fouling as an external load cause; the need to normalise
weather, draught and current; the speed–power comparison; ISO 3046-1 / 42,700 kJ/kg.

---

## 2. `QB1_D#q7` — Bonjean curves

Everything GPT accepted is unchanged: one curve per transverse station, immersed sectional
area against draught, superimposed actual waterline, Simpson integration, displacement and
LCB, longitudinal strength, launching, grounding, damaged/flooded/inclined conditions, and
that it is not an LCF/waterplane-property curve.

**Rejected proposition.** *"The moment the waterline is not parallel to the baseline …
those tables stop being valid."*

**Corrected proposition.** Ordinary hydrostatic tables are tabulated for the ship upright
and on even keel and are **not, by themselves, sufficient** for an arbitrary inclined or
heavily trimmed waterline, because every station is then at a different draught. Bonjean
curves let us reconstruct the immersed sectional areas station by station for that actual
waterline.

**Why more precise.** The tabulated hydrostatics do not become invalid — they remain a
correct answer to the question they were computed for. What fails is their *sufficiency*
for a different waterline. "Invalid" misdescribes the geometry and, in the room, signals a
candidate who does not know what the tables are.

**Two sections were examined and deliberately left alone**, because they were already
correct and are the model the others were brought into line with:

* the body heading *"Why the hydrostatic tables are not enough"* and its paragraph, which
  already said the tables *cannot answer* a trimmed-and-aground case "because the waterline
  is no longer parallel to the baseline and every station is at a different draught";
* the deep-dive, which already said the tables *"assume even keel"* and that every Bonjean
  situation is one *"where that assumption has failed"*.

---

## 3. `QB5_I#q8` — critical equipment / spares examples

The corrected ISM logic from `CORR-ISM-SPARES-20260902` is preserved in full and is
unchanged: ISM 10.3 identifies equipment whose sudden operational failure may create
hazardous situations; the SMS provides measures promoting reliability; those measures
include regular testing of stand-by arrangements and equipment not in continuous use; 10.4
integrates them into the operational maintenance routine; ISM does **not** prescribe a
critical-spares list; minimum and reorder levels are SMS/company/vessel specific; the ISM 9
conditionality and the leadership/delegation structure stand.

**Residual risk found by GPT.** The worked example lists still read as though the
enumeration were itself ISM-prescribed and universal.

**Corrected wording.**

* **Critical equipment** is now introduced as *"typical examples that a company's SMS and
  risk assessment may designate, depending on the ship's design, machinery and trade"*,
  and closes by saying ISM 10.3 does not prescribe the list — it requires the **company**
  to identify the equipment, and *"what that catches legitimately differs from ship to
  ship"*.
* **Critical spares** is now introduced *"again by way of example"* and closes: which
  parts a given ship carries, and in what quantity, is set by the SMS, the maker's
  recommendations and the vessel's own risk assessment — *"the ISM Code prescribes no
  critical-spares list"*.
* **Class-required spares** is now conditioned *"where applicable under the vessel's own
  class rules, notation and machinery arrangement"*, and warns that scope differs between
  societies, so the candidate should quote the rules the ship is actually classed under
  *"rather than a single universal list"*. The reg-box carries the same qualifier.

**Not weakened.** Every named item survives — main engine and its fuel/cooling/starting-air
systems, steering gear, generators and emergency generator, emergency fire pump, bilge and
ballast, OWS and its 15 ppm alarm, inert gas; fuel valves, pump plungers, exhaust-valve
spindles and seats, liner and ring sets, bearings, gaskets and seals, control-air
components, PCBs and sensors. The practical CE inventory answer is intact.

---

## 4. Source-governance upgrades

### 4A. Grain Code — genuine tier-1 acquisition

`SRC-GRAINCODE-PARTA-TEXT` relied on a **P&I club reproduction**, `CURRENTNESS_UNVERIFIED`
and `NOT FILED`. **Resolution MSC.23(59)** — the instrument that adopted the Grain Code,
with the Code as adopted in its annex — was retrieved from IMO's own resolutions CDN
(HTTP 200, no workaround), filed, and registered as **`SRC-GRAINCODE-MSC23-59`**
(4,835,438 bytes, `sha256 5b2107d3…`).

Every wording claim the tier-2 reproduction carried is **confirmed word-for-word against
the instrument**: A 3.1 (issue of the DoA, *"shall be accepted as evidence that the ship is
capable of complying"*), A 3.2 (*"shall accompany or be incorporated into the grain loading
manual"*), A 3.4, A 3.5 and A 6.1 (*"in printed booklet form"*). The reproduction was
faithful.

**Non-destructive, per the registry's own history convention.** The old row is retained,
marked `HISTORICAL_SUPERSEDED` with `superseded_by: SRC-GRAINCODE-MSC23-59`, and its
`revalidation_note` records that it is being replaced exactly as it itself directed. It is
evidence of what the corpus relied on between 2026-09-02 and 2026-09-04.

**Stated limits.** MSC.23(59) is the **adopted baseline, not a consolidated edition**, and
must be read with the amendment chain — `SRC-GRAINCODE-MSC552-2026` is held in full and
carries the new specially-suitable-compartment condition and the 1 January 2026 effective
date. The PDF is a scan whose OCR layer carries artefacts (`HSC.23(S9)`, `ahall`,
`boa rd`); it is reliable for substance and for locating provisions, and a verbatim
candidate-facing quotation is taken from the page image. **RQ-G01 is closed in substance,
open in form**, and the now-stale sentence asserting the base publication is not held has
been corrected on the MSC.552 row rather than left to read as current.

**No candidate content changed.** `QB2_A#q11` was checked line by line against the
instrument — the A 3.1 quotation, the A 3.2 accompany-or-incorporate relationship, the
A 6.1 printed-booklet requirement, the A 3.5 route, the third compartment category and the
1 January 2026 date all match. **No conflict was found, so nothing was edited.**

### 4B. Merchant Shipping Act 2025 — `PENDING_FILING` discharged on evidence

The 30 September 2025 corrigenda was re-retrieved from DGMA's own endpoint (HTTP 200) and
filed beside the Act at
`06-india-law-and-dg-shipping/Merchant-Shipping-Act-2025/_base/MS_Act_2025_corrigenda_30092025.pdf`.
The re-retrieved bytes hash to `4a28b152…`, **identical to the digest registered on
2026-09-02** — which independently confirms both the registered digest and the file at
rest. `local_path` no longer says `PENDING_FILING`.

`s.63(1)`, `s.63(3)`, `s.64`, `s.83` and `s.94` were already read from the Act's own text
layer and stand in `SRC-MSACT-2025.verified_claims`; the corrigenda's three corrections are
typographical and renumber nothing, so none is disturbed. **`QB9_H#q10` was not altered —
no discrepancy was found.**

### 4C. SOLAS II-2/10.3.3 — honestly retained

The local `SOLAS-1974` holding was enumerated in full: seven files — MSC.532(107),
MSC.520(106), MSC.550(108), MSC.404(96), MSC.557(108), an `INSTRUMENT_LOG.md` and a
`manifest.json`. **There is still no consolidated chapter II-2 text.** The row therefore
stays `ACCESS_LIMITED` and was **not** upgraded; the numerical claim (100% of the first
ten, 50% of the remainder, maximum sixty) is retained on two concordant competent-authority
reproductions, and the re-verification is recorded. No candidate content was changed merely
to improve the registry.

---

## 5. H6 governance residue — history not rewritten

`batch_h6_manifest.json` `cards[1].topic` still describes the critical-spares list as
*"DERIVED from the ISM 10.3 critical-equipment list rather than chosen"* — the proposition
entry 64 overturned.

**It is left intact, deliberately, and this was already adjudicated.** The superseding
record `CORR-ISM-SPARES-20260902` says so in terms: *"H6's own topic field still describes
what H6 shipped, including the wording this record corrects; that is what H6 did and it is
left alone."*

**How ancestry and currentness are actually represented.** Not by prose — by the
supersession chain, which is machine-resolvable and fail-closed:

```
batch_h6_manifest.json / H6-002        post 4d3f8617…   (release evidence, never rebaselined)
  └─ CORR-ISM-SPARES-20260902 / CORR-ISM-01   pre 4d3f8617…  post b4e93098…
       └─ CORR-GPT-PASS1-20260904 / CORR-GPT-P1-03  pre b4e93098…  post bc41fb23…  = LIVE
```

`oral_supersession.resolve_authorised_card_state()` walks this chain for every validator
that pins a live digest. H6's claim is not weakened but **strengthened**: not "my state is
live" but "my state is the ancestor of what is live", with `CHAIN_BREAK`,
`PREDECESSOR_PIN_ALTERED`, `TERMINAL_NOT_LIVE`, `CHAIN_FORK` and `ORPHAN_SUCCESSOR` all
failing closed. The **effective interpretation pointer therefore already resolves to the
corrected proposition**, and it does so by enforcement rather than by annotation.

**A forward pointer was considered and rejected on schema grounds.** Adding a
"superseded-by" note field to `batch_h6_manifest.json` would require registering that field
in `oral_manifest.FIELD_CLASSES`, because **`UNCLASSIFIED` is a hard failure** — by design,
so that "a new decorative field on a future batch cannot slip in unnoticed". That is a
shared-schema change plus a mutation of a historical record, for a pointer the chain
already provides. Reverse lookup is answered the way `SKILL.md` 7.5a answers the same
question for holds: **search for a successor**, do not read it off the ancestor.

---

## 6. Candidate-visible `pending verification` — audited, not deleted

**20 occurrences, 6 files.** Every one was classified individually.

| # | File | Card | Category | Proposition | Source now available | Action |
|---|---|---|---|---|---|---|
| 1–2 | `QB9_H` | q1 | **B** | MS Act 2025 implements treaties; detail via rules/circulars | partial | keep |
| 3–5 | `QB9_H` | q2 | **B** | Indian casualty reporting / inquiry machinery | **yes** (Part XI) | keep |
| 6–7 | `QB9_H` | q4 | **B** | Shipping Master / DGMA wage-dispute machinery | **yes** (s.83) | keep |
| 8–9 | `QB9_H` | q8 | **B** | statutory duties and penalties | **yes** (Part XIV) | keep |
| 10–13 | `QB9_H` | q11 | **B** | preliminary inquiry → formal investigation | **yes** (Part XI) | keep |
| 14–16 | `QB1_I` | q2 | **B** | Indian ship definition; register book custody | **yes** (Part III) | keep |
| 17 | `QB3_J` | q5 | **B** | pollution jurisdiction frame | **yes** (Part VII) | keep |
| 18 | `QB5_B_CheatSheet` | page-level | **B** | handover/CE takeover, formerly 1958 §77 | partial | keep |
| 19 | `QB9_D` | q6 | **B** | CoC issuance / suspension | **yes** (**s.46(1)**, Part IV) | keep |
| 20 | `QB9_H_CheatSheet` | page-level | **B** | cite the Act at Part level; 1958 numbering is the stale-law trap | **yes** | keep |

**Counts: A = 0, B = 20, C = 0.**

**No occurrence is a Category-A authoring placeholder.** The species GPT was right to worry
about — an imperative addressed to the author, `[cite the 2025 Act at Part level; …]` — was
resolved in the 2026-09-02 pass and does not recur. All 20 survivors are the other species:
an honest candidate-facing currentness caveat of exactly the kind
`CURRENTNESS_UNVERIFIED` describes in the source registry. **#20 is not merely
tolerable but actively useful** — it names the stale-law trap and tells the candidate to
cite at Part level rather than reciting repealed 1958 section numbers.

**Every Part-level attribution was verified against the Act's real structure**, which is
new work in this pass and could have gone the other way:

* `QB1_I` "Part III" → **PART III REGISTRATION OF VESSELS** ✔
* `QB9_D` "Part IV" → **PART IV MARITIME EDUCATION AND TRAINING**, and s.2(8) defines a
  certificate of competency as one *"granted under sub-section (1) of section 46"*, which
  sits in Part IV ✔
* `QB3_J` pollution → **PART VII** ✔
* `QB9_H` casualty → **PART X / PART XI** ✔ (the cards name no Part number, so no claim
  conflicts)

**Nothing was deleted and no section number was invented.**

**The blocker these 20 cite is now removable, and that is a bounded follow-up rather than
this pass's work.** The Act PDF carries a **clean full text layer** (118 pages, 391,920
characters) and its Part structure reads cleanly, so the exact sections behind all 20 can
be mapped — `s.46` is already in hand for `QB9_D`. Closing them means editing six
candidate-facing files under correction governance and reading Parts III, IV, VII, X, XI
and XIV, which is outside the three-item authorisation and outside §8's expansion bar.
**Recommended as the next authorised tranche.**

---

## 7. `QB8_C#q4` — short-form layer: recommendation only, no content added

**Finding: it is not a card-level defect. It is a file-level architecture.**

* **All four** `QB8_C` cards (q1–q4) lack the 15s/60s layer — q4 is not an outlier.
* Corpus-wide, **10 of 761** cards lack it: `QB4_A` q3, q8, q12, q14, q17, q18 and
  `QB8_C` q1–q4. Two grandfathered files, nothing else.
* The markup confirms it: `QB8_C#q4` runs `q-answer` → `answer-body` with the layer slots
  empty, an older dialect rather than a dropped block.

**Recommendation: do not add one.** Writing a 15-second and a 60-second answer is
**content creation, not correction**, and doing it for q4 alone would leave one card of
four inconsistent with its own file. If the product contract does require the layer, the
correct unit of work is **the two files (10 cards) as a separately authorised batch**, not
a single card inside a surgical correction pass.

No 15s/60s content was written.

---

## 8. Reported, deliberately not edited

* **`QB3_F`** carries EIAPP language in two places: a CE-relevance line (*"so no
  unauthorised modification invalidates the EIAPP"*) and a trap answer (*"it **can**
  invalidate the EIAPP **if** it modifies emission-critical components specified in the
  Engine Technical File"*). The trap is already conditional and the CE line is already
  qualified by *unauthorised* — so this is **not the same absolute proposition** corrected
  in `QB5_J#q2`, and §8's expansion bar applies. It is nevertheless the same family and is
  offered for a future authorisation. Precedent: the 2026-09-02 pass reported `QB3_F`'s
  ISM inference on identical terms and did not edit it.
* **The 20 `pending verification` caveats** — closable, bounded, recommended above.
* **`QB4_A` / `QB8_C` short-form layer** — 10 cards, recommended above.

---

## 9. What was NOT touched

No other P0 card; no prose regenerated for style; no new cards; no deep-dives added; no
examiner attribution altered; no syllabus mapping changed; no written bank; no shared
RulesApp source; no Excel distribution; no full release suite; **no push and no deploy.**

---

## 10. A latent defect in the supersession layer, exposed by this correction

Declaring the chain on `QB1_D#q7` turned `validate_corrections.py` red — not on
this record's content, but on `AMBIGUOUS_ROOT`:

```
QB1_D.html#q7 AMBIGUOUS_ROOT: 2 states have no predecessor:
  batch_d_manifest.json/PROMNEW-004
  correction_corr_cetip_qb1d_q7_20260902_manifest.json/CORR-CETIP-Q7-01
```

**Cause.** `oral_supersession.load_card_records()` ingests every card entry on the
authorisation surface, including generation-1 production records that name a card and
pin **no digests at all** — `batch_d`'s `PROMNEW-*` entries are shaped this way. Such a
record became a state `(batch_d_manifest.json, None, None)` with no parent, i.e. a
**phantom second root**, so `build_chain()` could not identify a single root.

**Why it had never fired.** Chain resolution is dormant until some record declares
descent. `QB1_D#q7` is the first card in this corpus to have *both* a digestless
generation-1 record *and* a supersession chain. The guard failed closed, exactly as
designed — on the wrong cause.

**Fix.** One filter in `_states_for()`: a record that pins no post-edit digest is not a
*pinned state* — it authorises the card's existence but makes no claim about its bytes,
so it can be neither an ancestor nor a root. A record that pins nothing **and** claims
descent is malformed rather than dormant, and is deliberately kept so it fails loudly.

**Evidence.** `test_oral_supersession.py` — the module's own control suite, which drives
the real E1 and F1 validators against the live corpus — **62 checks, 0 FAIL**.
`validate_corrections.py` across every correction record: **0 FAIL**.

**One process note worth keeping.** Two intermediate runs of that suite reported a
failure that was not real. The suite mutates `QB1_A#q9` and restores it, so it must run
**serially**; an earlier run was killed by a two-minute timeout and left its probe
paragraphs in place, and a later run then snapshotted that dirty state and restored it.
`validate_batch_e1.py` read 1 FAIL on `manifest_digests_match` purely as crossfire. On a
clean tree, run serially, it is **25 checks, 0 FAIL**. A validator result taken while
another suite is mutating the tree is not evidence.
