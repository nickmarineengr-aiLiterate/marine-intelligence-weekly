# Final Oral Enrichment — Batch E1 (Marine Insurance, Liability and Commercial)

Ten authorised existing-answer enrichment edits landing on **nine** cards. **No
canonical card was created, removed, re-anchored or re-homed.** Corpus stays at
**721** questions / 86 question-bearing files.

Baseline commit `ac96d5d`. Consolidation `eb586ed`
(`research/oral-final-enrichment-consolidation`).

---

## 1. Repo truth

Working tree clean at session start. `origin/main` = `ac96d5d`, matching the
brief. Consolidation tip `eb586ed`, matching. Branch cut:
`prod/oral-enrichment-e1-commercial`.

## 2. The action set — both representations agree

The brief named E1 as `ENRICH-A001`–`A010`. That was **verified, not assumed**.
The consolidation agrees on both of its independent representations: the
`batches[]` entry for `E1` lists exactly those ten ids, and the `batch` field on
each production action assigns exactly those ten to E1. Count 10, no
reconciliation needed.

Checking both remains the point — `batches[].action_ids` is a denormalised
roll-up and `production_actions[].batch` is the per-record truth. E4's brief was
off by one; E3's named the wrong next batch. This one was right, which is only
knowable by checking.

## 3. Ten actions, nine cards

**`ENRICH-A007` and `ENRICH-A008` both target `QB9_H.html#q9`** (Contract of
Affreightment). Every earlier enrichment batch was one action per card, so the
guard needed a property no previous validator had: `action_and_target_cardinality`
asserts the 10/9 split and names the shared target explicitly, and
`shared_target_declared` requires the manifest to say so. Without those, dropping
either limb from the shared card would have passed as arithmetic.

The recorded `byte_delta` for that card is the **card total for both limbs
combined**, not either action alone. The manifest states this in
`shared_target_note` rather than leaving it to be inferred.

## 4. Action matrix

| Action | Band | Verify class | Target | Family | Status |
|---|---|---|---|---|---|
| ENRICH-A001 | **E-P1** | PRIMARY_AUTHORITY | `QB1_A.html#q12` | GAP-0616 | REDUCED SCOPE |
| ENRICH-A002 | **E-P1** | PRIMARY_AUTHORITY | `QB1_F.html#q1` | GAP-0011 | IMPLEMENTED |
| ENRICH-A003 | E-P2 | PRIMARY_AUTHORITY | `QB1_A.html#q9` | GAP-0237 | IMPLEMENTED |
| ENRICH-A004 | E-P2 | CURRENT_REG | `QB1_B.html#q1` | GAP-0234 | IMPLEMENTED |
| ENRICH-A005 | E-P2 | PRIMARY_AUTHORITY | `QB1_B.html#q19` | GAP-0239 | IMPLEMENTED |
| ENRICH-A006 | E-P2 | CURRENT_REG | `QB1_G.html#q29` | GAP-0610 | REDUCED SCOPE |
| ENRICH-A007 | E-P2 | TECHNICAL_REASONING | `QB9_H.html#q9` | GAP-0157 | REDUCED SCOPE |
| ENRICH-A008 | E-P2 | PRIMARY_AUTHORITY | `QB9_H.html#q9` | GAP-0626 | IMPLEMENTED |
| ENRICH-A009 | E-P2 | TECHNICAL_REASONING | `QB2_B.html#q7` | GAP-0595 | REDUCED SCOPE |
| ENRICH-A010 | E-P2 | TECHNICAL_REASONING | `QB5_J.html#q1` | GAP-0447 | REDUCED SCOPE |

No action was retargeted by the consolidation, and none was retargeted here.

## 5. Current-live recheck

All nine target cards were opened in full against the live 721-question corpus
before any edit — q-text, timed blocks, full answer body, CE relevance, examiner
chain, traps and reg-box. **Zero actions were held. Zero were downgraded to
already-covered. Five were reduced in scope** (§6), which is a different thing
and is recorded as such.

The recheck was load-bearing on every one of the five. E2 established that the
consolidation can be wrong about a card's current state even when the action
remains broadly valid; E1 met that four more times, plus one case where the
consolidation was right about the limb but wrong about where it belonged.

## 6. The five reduced actions, in full

### ENRICH-A001 — one of four elements was already on the card

| | |
|---|---|
| **Original limb** | Explain how the 3/4ths RDC operates rather than stating the fraction: the cross-liabilities basis, that it responds only to collision liability to the OTHER vessel, that the residual quarter plus any excess over the insured value plus the excluded heads (wreck removal, pollution, cargo on own ship, personal injury) fall to P&I |
| **Current-live** | The baseline Clause 8 bullet already reads "H&M covers ¾ of insured's liability **to the other vessel** in a collision. The ¼ balance + any excess covered by P&I". `cross-liab` occurs zero times; no exclusion head appears anywhere |
| **Authority** | ITC(H) 1/10/83 Clause 8, extracted verbatim |
| **Implemented** | Cross-liabilities settlement (Cl. 8.2.1); the ¾-of-insured-value ceiling per **any one collision** (Cl. 8.2.2); all five exclusions 8.4.1–8.4.5 and what they push to P&I |
| **Omitted** | "responds only to liability to the other vessel" |
| **Reason** | **Already present in target** — restating it would have been duplication inside one card |

A second correction inside the same action: the consolidation described the P&I
share as "the residual quarter plus any excess **over the insured value**". The
clause is more precise — 8.2.2 caps Underwriters at three-fourths of the insured
value **in respect of any one collision**. Written the clause's way.

### ENRICH-A006 — two of three sub-limbs are owned better elsewhere

| | |
|---|---|
| **Original limb** | The institutional and commercial response to recent maritime security incidents: the IMO's position and instruments, the flag State's role and advice to its ships, and the insurance consequence — war-risk listed areas, additional premium on transit, notice to underwriters, crew war-zone entitlements |
| **Current-live** | `QB1_G#q29` covers abandonment, fraudulent registries and MASS. Nothing on security. **But** corpus-wide search found `QB9_E#q3` "War Time Marine Insurance & Extra Premiums" already carries the Joint War Committee (LMA/IUA), Listed Areas, advance notice to underwriters, the Breach/Additional Premium and the charterparty allocation of who pays it; and `QB9_A#q9` already carries flag-State notification, BMP5, SSAS and MSC.1/Circ.1606 |
| **Authority** | SOLAS Ch XI-2 / ISPS (in force 1 July 2004); SUA 1988 (adopted 10 Mar 1988, in force 1 Mar 1992) + 2005 Protocols (in force 28 July 2010) |
| **Implemented** | The institutional/instrument limb only — that security of navigation is **not** the Legal Committee's remit, that IMO answers through existing MSC-owned instruments, and that what LEG contributes is the liability side |
| **Omitted** | The war-risk insurance limb and the flag-State/shipboard limb |
| **Reason** | **Duplicative — a dedicated canonical home already exists for each.** Publishing them onto a Legal Committee card would have created a third and fourth home for material the corpus already owns, which is the exact corpus-debt pattern the brief forbids. They are cross-referred in prose instead |

This is the largest reduction in the batch and the one most worth reading later:
the consolidation was right that the limb was missing *from this card*, and
wrong that this card should carry it.

### ENRICH-A007 — "rate stability" was already there

| | |
|---|---|
| **Original limb** | Who carries freight-market risk under a CoA and how: the owner exposed if the market rises, the shipper if it falls — a hedging instrument as much as a carriage contract |
| **Current-live** | The 60-second block already says a CoA "trades schedule security and volume for **rate stability**", which gestures at the point but never allocates the risk directionally and never names the hedging function |
| **Authority** | TECHNICAL_REASONING_ONLY — no external authority asserted; derived from the card's own stated anatomy |
| **Implemented** | The directional allocation and the hedging characterisation |
| **Omitted** | The rate-stability proposition itself |
| **Reason** | **Already present in target** |

### ENRICH-A009 — one baseline line already carried two of four elements

| | |
|---|---|
| **Original limb** | The tramp side of the contrast: no fixed schedule or published tariff, employed fixture by fixture under a charterparty rather than a liner bill of lading, freight negotiated per voyage against a market rate, and the different allocation of port, cargo-handling and delay risk |
| **Current-live** | The baseline bullet "Contrasted with Tramp Shipping: Unlike bulk carriers or tankers that move on-demand based on individual charter party spot contracts…" already carries no-fixed-schedule and charterparty. `laytime`, `demurrage`, `FIOST` and `liner terms` occur **zero** times on the card |
| **Authority** | TECHNICAL_REASONING_ONLY — GENCON, FIOST, laytime/demurrage/despatch named as terms of art; no clause number asserted |
| **Implemented** | Published tariff vs negotiated market freight; liner B/L vs charterparty; cargo-handling cost allocation; laytime/demurrage time-risk allocation |
| **Omitted** | No-fixed-schedule; bare "charterparty" |
| **Reason** | **Already present in target** |

### ENRICH-A010 — the mass-basis caveat was already on the card

| | |
|---|---|
| **Original limb** | The owner's case for an alternative fuel expressed through the card's own quantity: because LCV sets mass burned per unit of work, a low-carbon fuel's benefit must be stated per unit of ENERGY not per tonne — deciding bunker cost, tank capacity and compliance value |
| **Current-live** | The card already warns against "quoting LNG's calorific advantage without noting it is on a mass basis (volumetrically LNG stores less energy than HFO)" and already notes a low-energy stem burns more mass for the same energy |
| **Authority** | Regulation (EU) 2023/1805 (FuelEU Maritime), applying from 1 January 2025 — GHG intensity of energy used on board in gCO2e/MJ from a 91.16 gCO2eq/MJ reference |
| **Implemented** | Cost per gigajoule; the volumetric tank-capacity consequence; the compliance metric being written per megajoule |
| **Omitted** | Restating the mass-basis caveat |
| **Reason** | **Already present in target.** Separately, the IMO Net-Zero Framework was **not** cited — its adoption vote stands reconvened and it is not in force. That is an **over-broad consolidation limb** narrowed on currentness grounds |

## 7. Claims rejected from the authorisation record

Consistent with E2, E3 and E4: **the consolidation authorises which limb to add;
it does not establish what the limb says, and it is not a reliable description
of the card's current state.**

1. **A001** — "any excess over the insured value" replaced with the clause's own
   ceiling: three-fourths of the insured value **in respect of any one
   collision** (Cl. 8.2.2).
2. **A004** — "composition and weights reviewed on a fixed multi-year cycle" is
   true but incomplete, and incomplete in a way that leaves a candidate unable
   to say why the figure moves *between* reviews. The verified IMF position is
   that the fixed currency **amounts** are held constant across the five-year
   period while the **weights float with exchange rates**. Both mechanisms
   written. No basket weights and no next-review date published — neither could
   be verified to a current primary source this session.
3. **A005** — "s.33 as reformed by the Insurance Act 2015" is imprecise in a way
   that matters. The 2015 Act did **not** touch exact compliance. Only the
   **second sentence** of s.33(3) and the whole of s.34 were repealed, so "must
   be exactly complied with, whether it be material to the risk or not" is still
   law. Written that way.
4. **A008** — "identify the clause that effects the transfer" presumes one
   current answer. There is not one. See §9.
5. **A006** — the three-sub-limb authorisation was reduced to one on
   corpus-ownership evidence (§6).
6. **A003** — the consolidation's content was correct. The verified CMI text
   adds a stronger exam point it did not carry — that the adjustment is **not
   legally binding** in most jurisdictions — so that was included. The baseline
   card's loose phrase "Lloyd's Average Adjuster or equivalent" was **left
   untouched**: correcting it would be a delete/replace and is outside the
   authorised limb.

## 8. Authority — every action primary, or explicitly reasoning-only

| Action | Authority |
|---|---|
| A001 | **ITC(H) 1/10/83 Clause 8**, extracted verbatim: 8.1 (three-fourths of damages for loss/damage to any OTHER vessel or property thereon), 8.2.1 (cross-liabilities where both to blame and neither limited by law), 8.2.2 (total liability capped at their proportionate part of ¾ of the insured value in respect of any one collision), 8.4.1 removal/disposal of obstructions, wrecks, cargoes · 8.4.2 any property except other vessels and property on them · 8.4.3 the cargo, other property on, or the engagements of, the insured Vessel · 8.4.4 loss of life, personal injury or illness · 8.4.5 pollution or contamination except of the other vessel in collision |
| A002 | **Marine Insurance Act 1906, s.55(1)** "Included and excluded losses"; ISM Code Section 9 retained as the root-cause side |
| A003 | **CMI Guidelines relating to General Average (2nd ed., 2022) §3.1** — usually the shipowner's responsibility to appoint; findings not legally binding unlike an arbitration award — and **§3.2** — impartial and independent irrespective of the instructing party. **Association of Average Adjusters** (London, est. 1869), Fellowship by examination |
| A004 | **IMF** SDR valuation — five-currency basket (USD, EUR, CNY, JPY, GBP), calculated daily from market rates, basket reviewed every five years or earlier if warranted |
| A005 | **MIA 1906 s.33** "Nature of warranty", s.33(3) first sentence (survives); **Insurance Act 2015 s.10**, in force 12 August 2016, s.10(7) omitting the second sentence of s.33(3) and the whole of s.34 |
| A006 | **SOLAS Ch XI-2 + ISPS Code** in force 1 July 2004, maintained by the MSC; **SUA Convention 1988** adopted 10 March 1988, in force 1 March 1992; **2005 Protocols** in force 28 July 2010 |
| A007 | **TECHNICAL_REASONING_ONLY** — no external authority asserted |
| A008 | **BIMCO BARECON 2001** optional Part IV (Hire/Purchase Agreement); **BIMCO BARECON 2017** optional Part IV (purchase option). Confirmed by two independent practitioner analyses of the 2017 revision |
| A009 | **TECHNICAL_REASONING_ONLY** — GENCON, FIOST, laytime/demurrage/despatch as terms of art; no clause number asserted |
| A010 | **Regulation (EU) 2023/1805 (FuelEU Maritime)**, applying from 1 January 2025 — gCO2e/MJ, 91.16 gCO2eq/MJ reference |

## 9. Contract editions — the trap this batch was built to survive

E1 is the first batch whose subject matter is standard-form contract wording,
where the same Part number means different things in different editions.

**BARECON 2001** optional **Part IV** is a *Hire/Purchase Agreement*: where the
parties elect it, title passes to the charterer **on payment of the final
instalment of hire** — the classic bareboat charter-cum-demise shape.

**BARECON 2017** replaced that. Optional **Part IV is now a purchase option**,
giving the charterer the right to buy **during** the charter term at a
pre-agreed price, rather than title vesting automatically at the end.

Both editions are on the card, and the card says explicitly: *"Do not quote the
2001 mechanism as though it were current BARECON wording."* The qualifier
`BARECON 2017 changed this` is guarded (`required_qualifiers_kept`) and a
mutation relabelling 2017 Part IV as a Hire/Purchase Agreement is caught
(`unsubstantiated_claims_absent`).

No Indian statutory section number was cited. The MS Act 2025 bareboat
charter-cum-demise provision could not be verified to primary text this session,
so the Indian angle is stated only as the recognised registration form — which
two corpus cards already assert independently.

**ITC(H)**: the 1/10/83 edition was used throughout A001, matching the card's
own reg-box, which cites both 1983 and 1995.

## 10. Notes used

**None.** No action in this batch drew on the `oralnotes/` product. Every
authority is primary text, a professional-body guideline, or explicitly declared
technical reasoning.

## 11. Changed sections

Every edit is confined to the **answer body**. No reg-box, timed block, CE tip,
trap box, numbers box, mental map or related-questions block was touched on any
card.

| Action | Section added |
|---|---|
| A001 | h4 "How the ¾ Collision Liability (RDC) Actually Works" + lead para + 2-item list + exclusions para |
| A002 | h4 "Root Cause vs Proximate Cause" + 2 paras + closing one-liner |
| A003 | h4 "Who the Average Adjuster Is — and Why Independence Matters" + 2 paras |
| A004 | h4 "What an SDR Actually Is — and Why the Limit Moves" + 2 paras |
| A005 | h4 "Warranty Is Not Guarantee" + 2 paras |
| A006 | h4 "3. Maritime Security Incidents — Which IMO Organ Actually Responds" + lead + 2-item list + attribution para |
| A007 | h4 "Who Carries the Freight-Market Risk in a CoA" + 2 paras |
| A008 | h4 "Bareboat Charter vs Bareboat Charter-Cum-Demise" + lead + 2-item list + edition para |
| A009 | h4 "Liner vs Tramp — the Full Commercial Contrast" + lead + 4-item list |
| A010 | h4 "Why the Owner Argues an Alternative Fuel Per Megajoule, Not Per Tonne" + lead + 3-item list |

## 12. Additivity — normalised, character level

**9 insert opcodes. 0 delete. 0 replace.** One insert per card.

| File | Card | Opcodes | Bytes added |
|---|---|---|---|
| QB1_A.html | q9 | ins=1 del=0 rep=0 | +1242 |
| QB1_A.html | q12 | ins=1 del=0 rep=0 | +2088 |
| QB1_B.html | q1 | ins=1 del=0 rep=0 | +1148 |
| QB1_B.html | q19 | ins=1 del=0 rep=0 | +1367 |
| QB1_F.html | q1 | ins=1 del=0 rep=0 | +1391 |
| QB1_G.html | q29 | ins=1 del=0 rep=0 | +1843 |
| QB9_H.html | q9 | ins=1 del=0 rep=0 | +2849 (both limbs) |
| QB2_B.html | q7 | ins=1 del=0 rep=0 | +1680 |
| QB5_J.html | q1 | ins=1 del=0 rep=0 | +1658 |

### The EOL trap, and why the first proof was wrong

`QB5_J.html` is **CRLF** in the working tree while the other six destination
files are **LF**. `.gitattributes` pins `*.html` to `eol=lf`, so the object store
is LF either way, and git reported the file clean before this batch touched it.

The first additivity run compared **disk bytes against the blob** and reported
**57 insert opcodes** on QB5_J — every one a phantom `\r`, not a word of content.
Re-run against the LF-normalised text git actually stores, it is a single clean
insert. The number that mattered was wrong until the comparison was fixed.

The lesson is not "QB5_J is odd". It is that **an additivity proof must run
against the bytes git will store, not the bytes on disk** — otherwise a
CRLF-checked-out file manufactures thousands of insert opcodes, and a genuine
`replace` could hide among them. The manifest records this in
`line_ending_note`, and both `cards_of()` in the validator and the proof script
normalise before hashing or diffing.

Line-level diffstat (`52` added, `0` removed across 7 files) is reported only as
corroboration, never as the proof.

## 13. Timed-block delta — zero

All nine cards: 15-second and 60-second blocks **byte-identical** to baseline.
No timed block was touched, so no word-count rebalancing was needed or done.
Several cards sit outside the 48–67 / 106–153 word bands; those are pre-existing
and outside the authorised limb.

## 14. Follow-up overlap — three of ten, none implemented

| Action | Target | Follow-up | Follow-up ask | Distinct? |
|---|---|---|---|---|
| A001 | `QB1_A#q12` | GAP-0603 | "P&I insurance. Which all pollutions does P&I cover?" | **Yes** — scope of P&I pollution cover is broader than, and different from, the Clause 8.4 exclusion heads |
| A003 | `QB1_A#q9` | GAP-0620 | "Explain how GA was applicable for ship ever given stuck in suez" | **Yes** — a worked casualty application, not who appoints the adjuster. The card already carries an Ever Given anchor |
| A006 | `QB1_G#q29` | GAP-0602 | "How will deal with disputes to cargo damage..?" | **Yes** — cargo-damage dispute handling is unrelated to which IMO organ answers security incidents |

All three remain open follow-up work. **Follow-up workload unchanged at 35
groups.**

## 15. The HTML-entity guard defect, and its repair

This is the most important engineering finding of the batch.

`FORBIDDEN_CLAIMS` for A001 forbids the single most common wrong answer about
the collision split — *"P&I covers everything not covered by H&M"*. The pattern
was written the way a person writes it: `everything not covered by h&m`.

**These pages encode `&` as `&amp;`.** The live HTML carrying that claim would
read `everything not covered by h&amp;m`, and the pattern could never match. The
guard was blind to the exact claim it existed to forbid.

Mutation **P** proved it: injecting the claim entity-encoded left
`unsubstantiated_claims_absent` **green**, and the mutation was caught only
incidentally by `manifest_digests_match` — a catch that would **not** have fired
had someone made the same edit deliberately and regenerated the manifest.

**Repair.** The negative-claim match is now made against `html.unescape(card)`.
This is strictly stronger: unescaping can only ever expose more text to the
pattern, so it catches both spellings and can never catch less.

**Proof the hole is closed and not merely moved.** Mutation **Y** was added,
injecting the identical claim with a **bare** ampersand. Both now fail through
the intended check:

```
P  assert P&I covers everything H&M does not (A001)    caught (unsubstantiated_claims_absent)
Y  assert the same claim with a bare ampersand (A001)  caught (unsubstantiated_claims_absent)
```

**Defect class.** This is the same class E2 recorded for `tripping` inside
`stripping` — a negative guard that does not match the text as actually written —
in a new form: **HTML entity encoding rather than substring collision**. The
sibling validators were checked: `FORBIDDEN_CLAIMS` in E2, E3 and E4 contain no
`&`, `<` or `>`, so none of them is currently blind. **They were deliberately not
touched** — that would be unscoped guard maintenance — but the class is recorded
here so the next batch checks before writing a negative pattern.

Two incidental defects were fixed in the same file: a literal backspace byte
(`0x08`), introduced when `\b` was interpreted during file generation, and a
missing `import html`. The validator now parses with zero control characters.

## 16. Sibling-manifest delegation — no maintenance needed

`batch_e1_enrichment_manifest.json` was created **before** any prior guard ran.
That ordering is load-bearing: the exemption in every earlier guard is keyed on a
glob over `batch_*_manifest.json`, so in the window before the manifest exists,
A–D, GAP-0609, E2, E3 and E4 would all report genuine-looking drift on nine
legitimately edited cards.

With the manifest in place, **every prior guard passed unchanged**:

- `validate_batch_e2` reports all **nine** E1 cards by name as `authorised-elsewhere`;
- `validate_batch_e3` reports **nineteen** (E1's nine plus E2's ten);
- `validate_batch_e4` reports **twenty-five**;
- A/B/C/D and GAP-0609 pass unchanged.

Not vacuous: mutation **C** targets `QB1_H.html#q1`, a card no manifest owns, and
the harness **asserts that fact at run time** before running rather than trusting
it. An unowned card still fails.

**Sibling pin delegation: none needed.** No earlier manifest pins any of the nine
E1 targets — checked programmatically against every `batch_*_manifest.json`.

## 17. Verification

| Property | Result |
|---|---|
| Canonical total | **721 → 721** (equality vs baseline `ac96d5d`) |
| Question-bearing files | 86, unchanged |
| Cards added / removed | **0 / 0** |
| Cards changed corpus-wide | **exactly 9, all authorised, 0 unauthorised** |
| Edits purely additive | **yes** — 9 insert opcodes, 0 delete, 0 replace, LF-normalised |
| q-text / anchors | unchanged on every card, corpus-wide |
| DOM | balanced on all nine, ids unique, all under `#q-feed`, no nested lists |
| Candidate-visible hygiene | clean — no new leak on any touched card |
| `build_qb_content_index --check` | **CURRENT — no regeneration** (86 files / 721 questions) |
| `build_examiner_index --check` | **960 relationships / 7 examiners — zero delta**, 4/4 artefacts current |
| Public corpus count | **721**, unchanged. Pricing untouched |
| Determinism | **26 artefacts / 0 non-reproducible** under `PYTHONHASHSEED` 0 / 1 / 524287 |

### Full release suite — 37 gates, every one executed

The runner executed **37** gates, a superset of the 36 required: `examiner_check_tests`
was added. Every required gate is present exactly once; none was skipped or duplicated.

`content_index_check` · `content_index_validate` **24/0** · `content_index_mutate` ·
`qb_question_text` · `oral_controls` · `notes_controls` ·
`validate_batch_a` **11/0** +mut · `validate_batch_b` **16/0** +mut ·
`validate_batch_c` **16/0** +mut · `validate_batch_d` **22/0** +mut ·
`validate_gap0609_exception` **59/0** +mut ·
`validate_batch_e4` **16/0** +mut · `validate_batch_e3` **21/0** +mut ·
`validate_batch_e2` **23/0** +mut · `validate_batch_e1` **25/0** +mut ·
`examiner_check` · `validate_examiner_index` **52/0** +mut · `test_examiner_check` ·
`validate_ce_tip_review` **28/0** +mut · `validate_phase2` **107/0** +mut ·
`validate_audit` (see below) · Node `deploy_surface`, `regulatory_facts`,
`link_integrity` · `qb_health_check` — **all exit 0**.

**A parser caveat worth recording.** A first pass at classifying these logs
flagged `phase2_mutate` as a semantic failure and reported `FAIL:` strings on five
mutators. Those were the **caught-mutation evidence** — a mutation harness prints
the validator's FAIL output precisely to prove detection. Reading them as gate
failures inverts their meaning. Classification is taken from each harness's
**summary line only**. The discipline that says "exit 0 is not PASS" also says "a
FAIL string in a mutator log is not a failure".

### Mutations — 208 across 13 suites, 0 escapes, 0 no-ops, 0 crashes

`content_index` 26 · `batch_a` 8 · `batch_b` 10 · `batch_c` 10 · `batch_d` 12 ·
`gap0609` 8 · `batch_e4` 12 · `batch_e3` 16 · `batch_e2` 18 · **`batch_e1` 25** ·
`examiner` 13 · `ce_tip` 17 · `phase2` 33. Every suite ended byte-identical.

The E1 suite breaks each property in turn — omit an action, retarget an action,
touch a card no manifest owns, blank an added limb, inject an internal id, add a
q-card, misstate the canonical total, strip a required authority, alter q-text,
claim a relationship delta, delete baseline text, break manifest/consolidation
identity, declare new-card creation, falsify a digest — plus eleven E1 additions:

- **O** flatten the BARECON edition contrast → `required_qualifiers_kept`
- **P** assert P&I covers everything H&M does not (entity-encoded) → `unsubstantiated_claims_absent`
- **Q** relabel BARECON 2017 Part IV as hire/purchase → `unsubstantiated_claims_absent`
- **R** flatten what the Insurance Act 2015 abolished → `required_qualifiers_kept`
- **S** drop the shared-target declaration → `shared_target_declared`
- **T** edit a timed block on an authorised card → `timed_blocks_unchanged`
- **U** revert one authorised card to baseline (deliberately the CRLF file) → `every_authorised_card_changed`
- **V** credit the Legal Committee with maritime security → `required_qualifiers_kept`
- **W** flatten the mass-versus-volume distinction → `required_qualifiers_kept`
- **X** misstate the distinct target-card count → `action_and_target_cardinality`
- **Y** assert the same claim with a bare ampersand → `unsubstantiated_claims_absent`

Mutation **U** targets `QB5_J.html` on purpose, so the harness also proves the
guard's LF normalisation works in the direction that matters.

### Audit validator — semantic result, not exit code

`validate_audit` reports **`passed 12 / failed 1 / unavailable 0`** while exiting
**0**. The failing check is `index_tier_literals_valid` — "43 invalid literals".

Run on a **detached clean `origin/main` worktree** at `ac96d5d`, the result is
**identical**: same counters, same failing check, same detail string, and the two
JSON outputs are byte-identical (`142c1166…`).

**PRE-EXISTING AUDIT BASELINE — ZERO E1 AUDIT DELTA.** Reported here rather than
counted as green, because reading the exit code alone would call it a pass. This
is carried debt from E2, E3 and E4, still unfixed.

### Health check — multiset baseline

`qb_health_check`: **480 finding lines on both the E1 branch and a clean
`origin/main` worktree**, compared as multisets — **0 new, 0 gone**.

The multiset method was load-bearing, not ceremonial. The two logs are **not**
byte-identical — a 62-line diff — but every difference is pure **reordering** of
the same changelog-gap findings. `PYTHONHASHSEED` is unpinned, so the health
check emits in hash-seed-dependent order. A byte or line-order comparison would
have manufactured a false regression across 361 findings.

### Gate-generated artefacts

Three separate cleanups, every one by explicit path, never a blanket restore:

1. After the release suite: `VALIDATION_RESULTS.json` and
   `PHASE2_VALIDATION_RESULTS.json`, both proven written by `validate_audit.py`
   / `validate_phase2.py` / the mutators.
2. After a stray `check_determinism.py --help` (§18): 7 artefacts plus an
   untracked `.determinism-snapshot/` directory.
3. After the real determinism run: 24 artefacts, 23 matching the tool's own
   `GENERATED` list literally and the 24th (`ORAL_NOTES_IMPACT.md`) attributed to
   `report_notes_impact.py`, which is in the same generator sequence.

E1 card digests were re-verified intact after every cleanup.

**Pre-existing debt observed, not fixed:** the committed copies of these
artefacts are **stale** — `VALIDATION_RESULTS.json` still says `688` live
questions and `954` headings, `PHASE2_VALIDATION_RESULTS.json` says `682`
canonical questions. Any gate run rewrites them to current truth (721 / 960 /
721), which is why they dirty on every suite.

### Render

**NOT BROWSER VERIFIED.** One genuine attempt was made: the preview pane serves
files outside the project folder as static snapshots that execute no JS and
expose neither DOM nor page text; `get_page_text` returned "No site is open in
this tab." No browser claim is made.

Substituted and clean on all nine cards: DOM parse and div balance, id
uniqueness, `#q-feed` parentage, q-text stability, candidate-hygiene regex over
the **added text only**, and table / image / inline-style / nested-list /
fixed-width / long-token scans — all zero.

## 18. Two operational traps hit this session

**An unrecognised flag is a full run.** Probing `check_determinism.py --help`
executed the entire generator chain — the tool has no `--help` handler. It left
7 tracked artefacts modified and a `.determinism-snapshot/` directory behind,
reproducing the exact trap E2 recorded. The correct response was to identify the
changed artefacts by name, restore only those, and re-verify all ten E1 card
digests before continuing. A blanket `git checkout -- .` at that moment would
have destroyed all nine production edits. **Read a tool's argument handling from
source before invoking it.**

**Long gates must be backgrounded from the start.** The 37-gate suite runs ~13
mutation harnesses, each spawning a validator that shells out to
`build_examiner_index --check`. That is far past any interactive timeout. The
suite, both mutation runs and the determinism gate were all backgrounded with
completion waiters, and the repo was left untouched while any mutator could be
transiently active.

## 19. New debt (5)

1. **`validate_audit` still exits 0 while reporting `failed: 1`.** Carried from
   E4, E3 and E2, still unfixed. A caller trusting the exit code reads a failure
   as a pass. Failing check: `index_tier_literals_valid`, 43 invalid literals.
2. **Committed gate-result artefacts are stale.** `VALIDATION_RESULTS.json`
   (`688` questions, `954` headings) and `PHASE2_VALIDATION_RESULTS.json` (`682`
   canonical) were committed at an older corpus state, so every gate run dirties
   them. They are noise on every future batch until regenerated deliberately.
3. **`qb_health_check` output order is hash-seed dependent.** 361 findings emit
   in a different order per process. Harmless under multiset comparison, but any
   future check that diffs its output by line will report false regressions.
4. **`QB1_B#q19` carries markup leakage in candidate view.** The card ends with a
   literal `---` `---` pair and writes `H\&M` with a LaTeX-style escape. Same
   class as the E3 `QB2_B#q2` and E2 `QB3_H#q6` items. Pre-existing, outside the
   authorised limb, untouched.
5. **`QB1_A#q9` says "Lloyd's Average Adjuster or equivalent".** Not a standard
   term; the professional body is the Association of Average Adjusters, now named
   correctly in the same card's new section. Correcting the old phrase would be a
   delete/replace outside the authorised limb, so it was left. The card now
   carries both phrasings.

## 20. Status

- Brand-new answer inventory: **COMPLETE 33/33**, unchanged.
- Canonical corpus: **721**, unchanged. Public count unchanged. Pricing untouched.
- Examiner index: **960 relationships / 7 examiners**, delta zero.
- Enrichment workload: **28 → 18 unique actions remaining** (E1's ten complete).
- Follow-up workload: **35 groups**, unchanged — E1's three colocated follow-ups
  are different limbs and were not resolved.
- Master XLSX: **deferred**.

## 21. Next batch — E5, derived from current consolidation data

Both remaining batches were re-derived from `FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json`
rather than taken from the brief.

| | **E5** — STCW, MLC, crew welfare, shipboard management | **E6** — IMO instruments, maritime law, pollution response |
|---|---|---|
| Actions | **12** (`ENRICH-A033`–`A044`) | 6 (`ENRICH-A045`–`A050`) |
| Band mix | 10 × E-P2, 2 × E-P3, **no E-P1** | 1 × **E-P1**, 3 × E-P2, 2 × E-P3 |
| Currentness exposure | 3 of 12 — **25%** | 3 of 6 — **50%** |
| Verification mix | 5 primary, 3 currentness, 4 reasoning-only | 1 primary, 3 currentness, 2 reasoning-only |
| Authority | One accessible set: STCW Convention + Code, MLC 2006 as amended | Mixed; the E-P1 (`QB1_A#q18`) is currentness-gated |
| Coherence | High — one regime, one authority family | Lower — instrument hierarchy, audit regime and pollution response are three subjects |

**Recommendation: E5.** It carries twice the exam value per unit of verification
risk — 12 actions against one accessible authority family, with currentness
confined to 3 of 12 and a third of the batch needing no external authority at
all. E6 holds the last remaining E-P1, but half its actions are currentness-gated
and two of six are low-value E-P3; E3's handoff already flagged E6 as
"50% currentness-risk" and deprioritised it for that reason.

E5 also reuses infrastructure E1 just built: `ENRICH-A036` and `ENRICH-A037` both
target `QB4_C#q6`, the same many-actions-to-one-card shape that
`action_and_target_cardinality` and `shared_target_declared` now guard.

**Exact next set:** `ENRICH-A033`, `A034`, `A035`, `A036`, `A037`, `A038`,
`A039`, `A040`, `A041`, `A042`, `A043`, `A044`.

## 22. Verdict

**GO** — Final Oral Enrichment Batch E1 complete. All ten authorised
insurance/liability/commercial edits verified against primary authority, five
reduced on current-live and corpus-ownership evidence and recorded as such,
purely additive at character level, 721 → 721, examiner delta zero, 208
mutations with zero escapes, audit and health baselines identical to clean
`origin/main`, determinism reproducible across three seeds.
