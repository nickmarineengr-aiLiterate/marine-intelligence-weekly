# Final Oral Enrichment — Batch E3 (Cargo, Codes and Safety Systems)

Six authorised existing-answer enrichment edits. **No canonical card was created,
removed, re-anchored or re-homed.** Corpus stays at **721** questions / 86 files.

Baseline commit `be339f7`. Consolidation `eb586ed`
(`research/oral-final-enrichment-consolidation`).

---

## 1. The action set — no discrepancy this time

The session brief named E3 as `ENRICH-A021`–`A026`. The consolidation agrees on
**both** of its independent representations: the `batches[]` entry for `E3`
lists exactly those six ids, and the `batch` field on each production action
assigns exactly those six to E3. Count 6.

Checking both rather than one is the point. `batches[].action_ids` is a
denormalised roll-up; `production_actions[].batch` is the per-record truth.
Agreement between them is a genuine cross-check — and it is what exposed E4's
off-by-one, where a human-written brief disagreed with both. Here nothing
needed reconciling.

## 2. Action matrix

| Action | Band | Verify class | Target | Family |
|---|---|---|---|---|
| ENRICH-A021 | E-P2 | PRIMARY_AUTHORITY | `QB8_G.html#q2` | GAP-0448 |
| ENRICH-A022 | E-P2 | PRIMARY_AUTHORITY | `QB2_B.html#q2` | GAP-0270 |
| ENRICH-A023 | E-P2 | PRIMARY_AUTHORITY | `QB2_G.html#q1` | GAP-0232 |
| ENRICH-A024 | E-P2 | PRIMARY_AUTHORITY | `QB2_H.html#q1` | GAP-0089 |
| ENRICH-A025 | **E-P1** | PRIMARY_AUTHORITY | `QB2_I.html#q4` | GAP-0222 |
| ENRICH-A026 | E-P2 | OEM_VERIFY | `QB2_A.html#q7` | GAP-0220 |

**Current-live recheck.** All six cards were opened in full against the live
721-question corpus before any edit: every target still correct, every limb
still genuinely missing, none absorbed by E4, GAP-0609 or Batch D. **Zero
actions downgraded or held.** One action was reduced in scope under its own
pre-authorised caution (A023, §4).

**Follow-up overlap: none.** No E3 target appears in any of the consolidation's
9 `followup_colocation` records.

## 3. The authorisation record was wrong twice — again

E4 recorded that its consolidation entry attributed the HFO/MGO carbon-factor
difference to "asphaltenes", which is chemically backwards, and concluded that
*the authorisation record is not itself a technical authority.* E3 met the same
problem twice more. The consolidation authorises **which limb to add**; it does
not establish **what the limb says**.

### A021 — an unconditional claim that the instrument makes conditional

The consolidation's limb asserted that "a fossil-to-methane main engine retrofit
on an LPG carrier is an IGF Code matter even though the ship is an IGC ship."

SOLAS II-1 regulation **56.4**, extracted verbatim from IMO resolution
MSC.392(95), disapplies Part G to a gas carrier that is either

> `.1` using their cargoes as fuel and complying with the requirements of the
> IGC Code; **or** `.2` using other low-flashpoint gaseous fuels provided that
> the fuel storage and distribution systems design and arrangements for such
> gaseous fuels comply with the requirements of the IGC Code for gas as a cargo.

An LPG carrier converting to methane fuel falls squarely inside `.2`. Whether it
is an IGF matter therefore **depends on how its fuel storage and distribution
system is arranged** — it is not settled by the ship being an IGC ship. Writing
the consolidation's sentence would have published a wrong answer to a
code-boundary question, which is precisely the question the examiner led with.

The card was written to the instrument instead, and the qualifier is now guarded
(§9, check `conditional_qualifiers_kept`).

### A026 — an OEM attribute neither manufacturer claims

The consolidation described AVD as leaving a "non-conductive **ceramic-like**
encapsulating layer".

- **Non-conductive is supported** — LiCELL states plainly that "The vermiculite
  film is not electrically conductive." Retained.
- **Ceramic-like is not.** Neither manufacturer describes a ceramic. Both
  describe a **film**: the platelets are deposited by the mist, the water
  flashes off, and "the high aspect ratio platelet particles overlap and bind
  together". Dropped rather than reproduced.

Worth recording for the next OEM-verified action: **AVD Fire Limited's own page
makes no electrical claim at all.** The non-conductivity statement rests on
LiCELL. One manufacturer page is not the same as "OEM-verified" — the second
source is what turned an unsupported adjective into a supported one and an
assumed one into a dropped one.

## 4. A023 — a pre-authorised scope reduction

The consolidation's limb named three elements: permitted extent, permitted
height, and "the reckoning point used in the timber freeboard assignment".

Extent and height substantiate verbatim (§5). The third does not exist. The
string `reckon` appears **zero times in the entire Load Line Convention** —
all 143,186 characters of it, Chapter III included — so there is no reckoning
point to state.

This is a reduction the family record itself pre-authorised. Its
`evidence_caution` read:

> The candidate-reported figures … are a garbled recollection and must be
> verified against ICLL Annex I Chapter III before anything is written. If they
> cannot be substantiated the limb reduces to the stow-extent criteria only.

So the action is `IMPLEMENTED_REDUCED_SCOPE`, not held and not narrowed on my
own authority.

**Where the candidate's figures actually came from.** Both garbled fragments
decompose into real criteria, just not the ones they were attached to:

| Candidate fragment | Actually |
|---|---|
| `33 PERC NT ON DECK` | ICLL Reg 44(3) — height not exceeding **one-third of the extreme breadth** in a seasonal winter zone in winter. Real, and implemented. |
| `500M OR 2SHIP LENGTH FRM FRWD TO RECKONING POINT` | SOLAS **V/22.1.1** line of sight — two ship lengths or 500 m. Real, but it is a **navigation-visibility** limit, not part of the timber freeboard assignment. |

The second was **not** imported into A023. It belongs to A022's authorised limb,
where it is the correct authority, and that is the only card it was written to.
Searching the whole Convention rather than only the cited chapter is what turned
"I could not find it" into "it is not there".

## 5. Missing limbs, and what was added

### ENRICH-A021 — `QB8_G#q2`

*The current answer lacks the IGC/IGF boundary and the rule that decides which
Code governs a gas-fuelled conversion.*

At 1,663 characters the card covered only tank types A/B/C and membrane; the IGF
Code was never mentioned. Added: the boundary is the **role of the gas, not the
type of ship** — IGC governs gas as cargo, the IGF Code (Res. MSC.391(95)),
mandatory through SOLAS chapter II-1 Part G from **1 January 2017**, governs
low-flashpoint gas as fuel. Then the conversion rule itself: under **56.2** a
ship of any age converting on or after 1 January 2017 is treated as a
low-flashpoint-fuel ship *from the date the conversion commenced*, and
**regulation 57** requires IGF compliance; **56.3** applies the same test to a
ship taking up a fuel different from the one it was approved for; **56.4** is
the conditional gas-carrier exception set out in §3.

The consolidation's own `scope_note` excluded the ask's retrofit
advantages/disadvantages and owner-persuasion limbs as commercial rather than
tank-type content. Honoured — nothing commercial was added.

### ENRICH-A022 — `QB2_B#q2`

*The current answer lacks what actually caps on-deck tier height, and the
derivation that makes the bay plan an output rather than a rule.*

The card covered the CSM, CSAP and lashing certification but gave no tier limit.
Added the four limits, whichever binds first, with the bay plan named as their
*result*:

- **MSC.1/Circ.1353/Rev.2 §4.2.1** — the CSM stowage plan must give **maximum
  stack masses**, the **permissible vertical sequence of masses in a stack**,
  and **maximum stack heights with respect to approved sight lines**, with
  securing devices specified against stowage position, stack mass, mass sequence
  and stack height.
- **Securing-gear capacity** — rods, turnbuckles, twistlocks and lashing-bridge
  height fix racking and corner-post loads; each tier lengthens the lever.
- **Stability and wind heeling** — VCG and windage rise per tier; the condition
  must still satisfy the 2008 IS Code **Part A, 2.3** severe wind and rolling
  (weather) criterion.
- **SOLAS V/22.1.1** — sea surface from the conning position not obscured by
  more than **two ship lengths, or 500 m, whichever is the less**, forward of
  the bow to 10° either side, *under all conditions of draught, trim and deck
  cargo*; no single blind sector forward of the beam exceeding 10°.

The circular's own phrase — "maximum stack heights **with respect to approved
sight lines**" — is what ties the CSM limit and the navigation limit together in
the instrument's own words, which is stronger than asserting the link.

### ENRICH-A023 — `QB2_G#q1`

*The current answer lacks the Load Line numeric stow criteria — the permitted
extent and height of the timber deck stow.*

Added, verbatim from ICLL Annex I Chapter III:

- **Reg 44(2) extent** — the cargo shall extend over at least the **entire
  available length**, being the total length of the well or wells between
  superstructures; where there is no limiting superstructure at the after end,
  at least to the **after end of the aftermost hatchway**; stowed as solidly as
  possible to at least the **standard height of the superstructure**.
- **Reg 44(3) height** — in a **seasonal winter zone in winter**, not exceeding
  **one-third of the extreme breadth**.
- **Reg 41 applicability** — Chapter III applies *only* to ships to which timber
  load lines are assigned, which is exactly why a container ship without that
  assignment cannot reach for these criteria. This reinforces the card's
  existing and correct refusal to claim a capability the ship does not hold.

Regulation 44 carries further figures the card still omits (upright and lashing
spacing ≤3 m, lashings ≥19 mm close-link chain or equivalent, guard rails ≤330 mm
vertical spacing to ≥1 m above the stow). These are **outside the authorised
limb**, which named extent and height, and were deliberately left. They are a
clean candidate for a future action.

### ENRICH-A024 — `QB2_H#q1`

*The current answer lacks the definition of an A-class division and the
consequence that A-0 is still a full A division carrying no insulation
requirement.*

The card already held A-60 as a figure and already gave the 140 °C / 180 °C test
criteria — so the *number* was explained but the *class* never was. Added, from
SOLAS II-2 regulation 3.2: an "A" class division is **constructed of steel or
other equivalent material**, **suitably stiffened**, and **capable of preventing
the passage of smoke and flame to the end of the one-hour standard fire test**,
prototype-tested per the FTP Code — requirements that attach to *every* A
division whatever number follows. The suffix states only how long insulation
holds the unexposed face within the permitted rise: **A-60 60 min, A-30 30 min,
A-15 15 min, A-0 0 min**.

Hence the limb's point, stated plainly: **A-0 is still a full A-class division**
— steel, stiffened and smoke- and flame-tight for the whole hour — carrying no
insulation requirement. It is not a weaker barrier against fire spread; it is an
uninsulated one.

### ENRICH-A025 — `QB2_I#q4` — the batch's only E-P1

*The current answer lacks the contents-verification method the Code names, the
stored pressure expressed in pascals, and the low-pressure/leak alarm
arrangement.*

The card was entirely the MSC.1/Circ.1318/Rev.1 hydrostatic interval regime, and
presented ultrasonic level gauging as *the* contents method. Four limbs added.

**Weighing, and why the examiner contrasts it with ultrasonic.** The method the
Code names for CO₂ is weighing. FSS Code Ch.5 **2.1.1.3** requires means to check
the quantity safely *without moving the containers completely from their fixing
position*, and for carbon dioxide systems specifies **hanging bars for a weighing
device above each bottle row**, or other means — surface indicators being the
option offered for *other* media, not CO₂. Added the mechanics (stamped **tare
weight**, weigh, subtract, >10% short of charge → refill or replace) and the
distinction that matters: weighing **measures the mass** the Code makes you
prove, while ultrasonic gauging **infers** it from a level and so depends on
charge density and reads only the liquid column. Both are acceptable under "or
other means"; the practical regime is ultrasonic routinely with weighing as the
reference check.

**Stored pressure, in pascals as asked.** Two arrangements, two pressures:

- **High-pressure cylinders** hold liquid CO₂ at its own saturated vapour
  pressure, so stored pressure is set by temperature rather than by a setting —
  about **5.1 × 10⁶ Pa** at 15 °C and **5.8 × 10⁶ Pa** at 20 °C, with no liquid
  phase at all above the critical temperature of **31 °C** (7.38 × 10⁶ Pa). That
  is why the cylinder room is ventilated and kept cool, and it leaves the card's
  existing and correct position — that *test* pressure is a cylinder-marking
  value — untouched.
- **Low-pressure refrigerated bulk units** are what the Code puts a number on.
  FSS Ch.5 **2.2.4.2** requires storage under a working pressure of **1.8 to
  2.2 N/mm²** — which *is* the pascal answer, since 1 N/mm² = 1 MPa = 10⁶ Pa —
  with liquid charge limited to **95%** of volumetric capacity.

**Alarms.** FSS Ch.5 **2.2.4.3** requires a pressure gauge, a high-pressure alarm
no higher than the relief valve setting, a **low-pressure alarm not less than
1.8 N/mm²**, a liquid level indicator and two safety valves; **2.2.4.11**
requires **audible and visual** alarms at a central control station on low or
high vessel pressure, on failure of **any one** refrigerating unit, or at the
**lowest permissible liquid level**. Closed with the operational read: a pressure
falling toward the low alarm with the refrigeration plant healthy is the leak
signature, and that alarm is what surfaces it.

### ENRICH-A026 — `QB2_A#q7`

*The current answer lacks what AVD is, how it works, and how it is applied
relative to the boundary cooling the card already prescribes.*

AVD appeared nowhere on the card. Added: **chemically exfoliated vermiculite** —
a hydrated magnesium-iron-aluminium silicate — broken into microscopic platelets
freely suspended in water, two components only, the mineral inert and non-toxic;
discharged as a **mist** rather than a jet; the water phase flashes off and the
high-aspect-ratio platelets **overlap and bind into a film** that dries and
encapsulates the cell, forming a thermal barrier that interrupts heat transfer
between adjacent cells — so it attacks the **propagation path**, not the flame.
Manufacturers characterise the action as **cooling and isolation**, with the
dried film markedly reducing re-ignition hours later. The film is **not
electrically conductive**, which is what makes a water-based agent defensible
around a battery.

Closed with the placement the limb asked for: AVD does not replace boundary
cooling. Boundary cooling is the bulk heat sink and remains the baseline for a
sealed box you cannot open; AVD is the close-range agent for cells you can
actually reach, applied so the film forms where propagation is happening. **For
a stowed, closed container the honest answer remains continuous boundary
cooling** — which keeps the card's existing and correct position intact rather
than displacing it.

## 6. Authority — all primary or OEM

| Action | Authority |
|---|---|
| A021 | IMO Res. **MSC.392(95)**, new SOLAS II-1 Part G regs **56** and **57**, extracted verbatim from the IMO resolution PDF; IGF Code = Res. MSC.391(95) |
| A022 | **MSC.1/Circ.1353/Rev.2** §4.2.1; **SOLAS V/22.1.1**; **2008 IS Code Part A, 2.3** |
| A023 | **ICLL 1966** Annex I Ch. III **Regs 41, 44(2), 44(3)**, from the full 90-page Convention text |
| A024 | **SOLAS II-2 reg 3.2** |
| A025 | **FSS Code Ch.5** §2.1.1.3, §2.2.4.2, §2.2.4.3, §2.2.4.11 (local `FSS_CODE_CORPUS`, chapter 5 flagged COMPLETE/verbatim); CO₂ saturation data (NIST-derived); **ISO 13769** for tare-weight stamp marking |
| A026 | **LiCELL** and **AVD Fire Limited** manufacturer documentation; regulatory anchor MSC.1/Circ.1615 already on the card |

**Notes used: none.** No E3 family carried Notes support, and no claim was taken
from `oralnotes/`, from neighbouring MIW content, or from a general maritime
study site. Where a claim could not be verified it was dropped (§3, §4), not
softened.

A note on the local FSS corpus: it was used because its chapter 5 is flagged
COMPLETE and verbatim in `CURRENT_STATUS.md`, and because §2.1.1.3's text is
reproduced there in full. It supplied the exact wording that made the weighing
limb Code-anchored rather than practice-anchored.

## 7. Scope of change

```
meoclass1/QB2_A.html    +9
meoclass1/QB2_B.html   +10 -1
meoclass1/QB2_G.html    +9 -1
meoclass1/QB2_H.html    +7 -1
meoclass1/QB2_I.html   +16
meoclass1/QB8_G.html    +6 -1
                  53 insertions, 4 deletions
```

**The four "deletions" are a line-level artefact, not lost content.** Several
reg-boxes are a single very long line; appending a reg-item to one shows as a
line removed and a line added. At character level every one of the six edits is
**purely additive** — `SequenceMatcher` opcodes over each card give `insert`
only, with **zero delete and zero replace ops**. Not one baseline character was
disturbed. This is now a standing guard (§9, `edits_purely_additive`).

**Timed-block delta: zero** — every 15-second and 60-second block is
byte-identical to baseline on all six cards. **Zero new CSS classes, zero new
inline styles, zero tables, zero images, zero nested lists, zero fixed widths,
zero unbreakable tokens.** Tags used across all additions: `div, em, h4, li, p,
span, strong, sup, ul`. The single `<sup>` (A025, the 10⁶ Pa exponents) is a
browser-default element; the page's only global rule is
`*{box-sizing:border-box}`, which does not touch it.

## 8. Claim review

Every new numeric, code-section, date and equipment claim introduced by E3, and
how it was verified:

| Claim | Verified against |
|---|---|
| IGF Code = MSC.391(95); Part G mandatory 1 Jan 2017 | MSC.392(95) + IMO record |
| SOLAS II-1 **56.2 / 56.3 / 56.4 / 57** | MSC.392(95) verbatim |
| CSM gives max stack masses, mass sequence, max stack heights w.r.t. approved sight lines | MSC.1/Circ.1353/Rev.2 §4.2.1 |
| Two ship lengths **or 500 m, whichever is the less**; 10° either side; blind sector ≤10° | SOLAS V/22.1.1 |
| Weather criterion at **Part A, 2.3** | 2008 IS Code |
| Extent over well(s) / aftermost hatchway / standard superstructure height | ICLL Reg 44(2) verbatim |
| Height ≤ **one-third extreme breadth**, seasonal winter zone in winter | ICLL Reg 44(3) verbatim |
| Chapter III applies only where timber load lines assigned | ICLL Reg 41 verbatim |
| A division: steel/equivalent, suitably stiffened, smoke- and flame-tight to end of one-hour standard fire test | SOLAS II-2 reg 3.2 |
| **140 °C** average / **180 °C** single point; A-60/30/15/**0** = 60/30/15/**0** min | SOLAS II-2 reg 3.2 |
| **Hanging bars for a weighing device above each bottle row**; no need to move containers from fixings; surface indicators for *other* media | FSS Ch.5 2.1.1.3 verbatim |
| Cylinders carry a stamped **tare** mass | ISO 13769 (stamp marking; FSS 2.1.1.4 footnotes it) |
| Low-pressure working pressure **1.8–2.2 N/mm²**; charge ≤ **95%** | FSS Ch.5 2.2.4.2 verbatim |
| Low-pressure alarm **not less than 1.8 N/mm²**; high alarm ≤ relief setting; two safety valves | FSS Ch.5 2.2.4.3 verbatim |
| **Audible and visual** alarms at CCS on low/high pressure, any refrigerating unit failure, lowest permissible level | FSS Ch.5 2.2.4.11 verbatim |
| CO₂ saturation **≈5.1 × 10⁶ Pa** at 15 °C, **≈5.8 × 10⁶ Pa** at 20 °C; critical **31 °C / 7.38 × 10⁶ Pa** | NIST-derived saturation data (5.063 / 5.776 MPa; 31.03 °C) |
| AVD = chemically exfoliated vermiculite platelets in water; applied as **mist**; dries to a **film**; **not electrically conductive**; cooling and isolation | LiCELL + AVD Fire Limited |

Two claims from the authorisation record were **rejected** on verification
("ceramic-like"; the unconditional IGF reading) and one **could not be
substantiated at all** ("reckoning point"). Nothing unverifiable was retained,
and nothing was made to look authoritative with a guessed section number.

The **10% refill threshold** and the cylinder **test**-pressure position were
already on the card and were left as they stood; they are not E3 claims.

## 9. Verification

| Property | Result |
|---|---|
| Canonical total | **721 → 721** (equality vs baseline `be339f7`) |
| Question-bearing files | 86, unchanged |
| Cards added / removed | **0 / 0** |
| Cards changed corpus-wide | **exactly 6, all authorised, 0 unauthorised** |
| Edits purely additive | **yes** — insert-only opcodes, 0 delete, 0 replace |
| q-text / anchors | unchanged on every card, corpus-wide |
| DOM | balanced, ids unique, all six under `#q-feed`, no nested lists |
| Candidate-visible hygiene | clean |
| `build_qb_content_index --check` | current — **no regeneration** (86 files / 721 questions; the index derives identity from file + anchor and q-text, never from answer bodies) |
| `build_examiner_index --check` | **960 relationships / 7 examiners — zero delta** |
| Public corpus count | **721**, unchanged. Pricing untouched. |
| Determinism | **26 artefacts / 0 non-reproducible** under `PYTHONHASHSEED` 0 / 1 / 524287, and every artefact identical to what was already on disk — the deterministic *no-change* state |

### Gates — every required suite executed

`validate_batch_e3` **21/0** · `validate_batch_e4` 16/0 · `validate_batch_a`
11/0 · `validate_batch_b` 16/0 · `validate_batch_c` 16/0 · `validate_batch_d`
22/0 · `validate_gap0609_exception` 59/0 · `validate_qb_content_index` 24/0 ·
`validate_examiner_index` 52/0 · `validate_phase2` 107/0 ·
`validate_ce_tip_review` 28/0 · `test_qb_question_text` **7487 controls / 0
failures over 86 pages** · `test_oral_controls` 315/0 · `test_notes_controls`
106/0 · `qb_health_check` exit 0 · Node `deploy_surface` 92/0 ·
`regulatory_facts` 16/0 · `link_integrity` 20/0.

### Mutations — 165 total, 0 escapes, 0 no-ops, 0 crashes

`mutate_batch_e3` **16** · `mutate_batch_e4` 12 · `mutate_batch_a` 8 ·
`mutate_batch_b` 10 · `mutate_batch_c` 10 · `mutate_batch_d` 12 ·
`mutate_gap0609_exception` 8 · `mutate_qb_content_index` 26 ·
`mutate_examiner_index` 13 · `mutate_phase2` 33 · `mutate_ce_tip_review` 17.
All restored byte-exact.

The E3 suite breaks each property in turn: omit an action, retarget an action,
touch a neighbouring card, blank the added limb, inject an internal id, add a
q-card, misstate the canonical total, strip a required authority, alter q-text,
claim a relationship delta, declare new-card creation, revert an authorised
card — plus four E3 additions:

- **M** reintroduce the disproved "ceramic" descriptor → caught
  (`disproved_claims_absent`)
- **N** strip the condition from the 56.4 exclusion → caught
  (`conditional_qualifiers_kept`)
- **O** delete baseline text from an authorised card → caught
  (`edits_purely_additive`)
- **P** falsify a recorded digest → caught (`manifest_digests_match`)

M and N exist because two E3 limbs were written *against* the authorisation
record. A future edit that "restores" the consolidation's wording would
reintroduce a verified-wrong claim, and **no positive-token check would notice** —
the limb tokens would all still be present. These are negative-token guards for
exactly that.

### Audit validator — semantic result, not exit code

`validate_audit` reports `passed 12 / failed 1 / unavailable 0` while exiting
**0**. The failing check is `index_tier_literals_valid` (43 invalid literals).

Run on a **clean `origin/main` worktree** the result is `passed 12 / failed 1 /
unavailable 0`, exit 0 — **identical**. Pre-existing, unrelated to E3, and
already recorded as E4 debt item 4. Reported here rather than counted as green,
because reading the exit code alone would have called it a pass.

`qb_health_check` likewise: **189 findings on both the branch and clean
`origin/main`** — zero delta — and none of the 189 concerns any of the six E3
target files.

Gate-generated result artefacts (`VALIDATION_RESULTS.json`,
`PHASE2_VALIDATION_RESULTS.json`, `ORAL_NOTES_IMPACT.md`) were dirtied by these
runs and **reverted after proof**.

### Render

**NOT BROWSER VERIFIED.** The preview pane serves files outside the project
folder as static `data:` snapshots which execute no JS and expose neither DOM
nor page text, so no browser claim is made. Substituted: DOM parse and div
balance, id uniqueness, `#q-feed` parentage, CSS-class existence, inline-style
count, and table/image/nested-list/fixed-width/overflow-token scans over the
**added text only** — all clean (§7).

## 10. Guard repair — the delegation defect, one level up

`validate_batch_e4` failed `only_authorised_cards_changed` the moment E3 landed.

Investigated before touching anything, per the standing rule never to
re-baseline a pin: **12 cards differ from E4's baseline `4272ad6` — exactly
E4's six plus E3's six, with zero unaccounted for.** So the edits were
authorised and the guard had simply expired.

This is the **third** appearance of one structural defect in this corpus: a
guard that pins corpus-wide state and expires on the next authorised batch.
Batch B's guard pinned the corpus total; E4 found the A–D digest pins were
half-wired; and E4's own enrichment-scope check carried the identical incomplete
loop. **E4 diagnosed the class, fixed the instances it was failing on, and left
it live one level up in its own validator.**

Repaired by applying E4's own founder-approved contract — *a card a sibling
manifest authorises is exempt and reported BY NAME, never silently dropped* — to
`only_authorised_cards_changed` in `validate_batch_e4.py`, and pre-emptively in
`validate_batch_e3.py` so E3's guard will not expire when E2, E5 or E6 lands.

Proven not to be a weakening:

- **Negative test** — an edit to `QB5_D#q1`, a card no manifest owns, still
  fails **both** guards, naming it as `unauthorised` and cleanly separated from
  the six delegated cards. Restored byte-exact (SHA verified).
- The exemption is keyed on a plain `file#anchor`, while `CARD ADDED` /
  `CARD REMOVED` entries carry a suffix — so card creation and deletion can
  never match it.
- `mutate_batch_e3` **C** and `mutate_batch_e4` **C** both still catch an edit
  to a neighbouring unowned card, after the change.

E4's guard now reports the six E3 cards by name as `authorised-elsewhere`; E3's
reports none, correctly, because no later batch exists yet.

### The sibling-pin delegation also got its first real test

Two E3 targets are pinned by earlier manifests — `QB2_H#q1` by Batch B and
`QB2_I#q4` by Batch D. Both guards now list them under `authorised-elsewhere`
rather than flagging drift. **E3 is the first batch to exercise E4's digest-pin
repair against an actual later edit**, and it holds.

Ordering matters here and is worth recording: the E3 manifest had to exist
*before* those guards were run. In the window before it was written, B and D
would have reported genuine-looking drift on cards I had legitimately edited —
the guards would not have been wrong, the delegation record simply would not yet
have existed.

## 11. Follow-up overlap

**None.** No E3 target appears in any of the consolidation's 9
`followup_colocation` records. Nothing reconciled, nothing deferred.

## 12. Examiner relationships

**Delta 0** — 960 relationships, 7 examiners, unchanged. No relationship, tier
or held mapping was touched.

## 13. New debt (5)

1. **`QB2_B#q2` list markup.** The baseline card's bullets are a run of
   consecutive single-`<li>` `<ul>` blocks rather than one list, so each bullet
   renders as its own list. Pre-existing and outside the authorised limb, so
   left. The E3 addition uses one properly-formed `<ul>`.
2. **`QB2_B#q2` `data-tags`.** Reads
   `"Ship Section 3: **SECTION:** Container Operations cargo"` — production
   scaffolding with literal markdown emphasis in a filter attribute. Not
   candidate-visible (it is an attribute, stripped before the hygiene scan), but
   it pollutes the tag filter.
3. **`QB2_H#q1` footer identity.** The correction mailto subject reads
   `"Reconciled Batch, QQ1"` and the version slug
   `"v1.1 · Finalised — pending Nixon final sign-off before gating"` — a
   correction email would be misfiled, and an internal review status is
   candidate-visible. Same class as E4 debt item 2.
4. **`validate_audit`** exits 0 while reporting `failed: 1`. Carried from E4
   debt item 4, still unfixed; a caller trusting the exit code reads a failure
   as a pass.
5. **ICLL Reg 44 figures still absent from `QB2_G#q1`** — upright and lashing
   spacing ≤3 m, lashings ≥19 mm close-link chain or equivalent, guard rails
   ≤330 mm to ≥1 m above the stow. Verified during this batch but outside the
   authorised limb. A future action can add them cheaply, the text is in hand.

## 14. Status

- Brand-new answer inventory: **COMPLETE 33/33**, unchanged.
- Canonical corpus: **721**, unchanged. Public count unchanged. Pricing untouched.
- Enrichment workload: **44 → 38 unique actions remaining** (E3's six complete).
- Follow-up workload: **35 groups**, unchanged — no E3 overlap to resolve.
- Master XLSX: deferred.

## 15. Next batch

**E2 — Class, survey, structure and statutory certification**
(`ENRICH-A011`–`A020`, 10 actions).

Chosen on the consolidation's own figures rather than on numbering or size. The
remaining four batches:

| Batch | n | E-P1 | Currentness risk (`CURRENT_REG_VERIFY`) | Dominant authority |
|---|---|---|---|---|
| E1 | 10 | 2 (20%) | 2 (20%) | market clause wording |
| **E2** | **10** | **2 (20%)** | **1 (10%)** | **primary instrument + class rule (7/10)** |
| E5 | 12 | **0** | 3 (25%) | mixed; 4 technical-reasoning |
| E6 | 6 | 1 (17%) | **3 (50%)** | current-regulation |

E2 carries the joint-highest E-P1 count, the **lowest** currentness risk of the
four, and the most favourable authority profile — 5 `PRIMARY_AUTHORITY_REQUIRED`
plus 2 `CLASS_RULE_VERIFY_REQUIRED`, both classes this session reached and
extracted verbatim. It is technically coherent: the class/survey spine plus the
two loading-and-stability limbs that share its class-rule verification regime.

**E6 was the obvious pick on size and is the wrong one on the criteria.** At
6 actions it looks like the natural successor to E3 and E4, but half of its
actions are `CURRENT_REG_VERIFY_REQUIRED` — the highest temporal exposure of any
remaining batch — and it holds only one E-P1. Size is not the selection
criterion; verification profile is. E6 is better taken when there is appetite
for a currency-heavy batch, and the standing temporal boundaries plus the
Coastal Shipping Act 2025 / MS Act 2025 interactions will be live hazards for it.

E1 ties E2 on E-P1 but its authority is market clause wording rather than
convention text, which is the weakest class for primary verification — the same
reason E4 deprioritised it.

E5 is last: twelve actions and **zero** E-P1.

Note before starting E2: at 10 actions it is larger than the six that made E3
and E4 tractable in one session, so it may warrant splitting. Its class-rule
actions will need IACS UR / class-rule text rather than IMO instruments, which
is an authority source this session did not have to reach for.
