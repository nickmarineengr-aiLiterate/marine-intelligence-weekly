# Final Oral Enrichment — Batch E5 (STCW, MLC, Crew Welfare and Shipboard Management)

Twelve authorised existing-answer enrichment edits landing on **eleven** cards across
**nine** pages. **No canonical card was created, removed, re-anchored or re-homed.**
Corpus stays at **721** questions / 86 question-bearing files.

Baseline commit `e47c7e6`. Consolidation `eb586ed`
(`research/oral-final-enrichment-consolidation`).

---

## 1. Repo truth

Working tree clean at session start. `origin/main` = `e47c7e6`, matching the brief.
Consolidation tip `eb586ed`, matching. Branch cut:
`prod/oral-enrichment-e5-stcw-mlc`.

## 2. The action set — both representations agree

The brief named E5 as `ENRICH-A033`–`A044`. That was **verified, not assumed**. The
consolidation agrees on both independent representations: the `batches[]` entry for
E5 lists exactly those twelve ids, and the `batch` field on each production action
assigns exactly those twelve to E5. The two lists are equal *in order*, the declared
`action_count` is 12, and the batch's `source_family_ids` equal the union of the
per-action `family_ids`. No reconciliation needed.

Checking both remains the point — `batches[].action_ids` is a denormalised roll-up
and `production_actions[].batch` is the per-record truth.

## 3. Twelve actions, eleven cards

**`ENRICH-A036` and `ENRICH-A037` both target `QB4_C.html#q6`** (MLC 2006 — 5 Titles
and flag/port State duties). Both were **retargeted by the consolidation**: A036 from
`QB4_E#q3` and A037 from `QB5_D#q3`. Confirmed from the consolidation itself, not
taken from the brief.

E1 met the many-actions-to-one-card shape first. E5 needed more than E1 did, because
E1's shared pair could be checked by arithmetic alone. Here the two limbs sit on the
same card **and in adjacent prose**, so a tidy-up that merged them, or a manifest edit
that dropped one id while leaving the other, would keep the card looking right.
`shared_target_actions_enumerated` therefore requires the manifest to name both ids
and requires that declaration to equal the set derived from the card list;
`shared_target_limbs_independently_present` then requires each id's own limb tokens on
the card. Mutations M, N and O break exactly those three ways.

The recorded `byte_delta` for that card is the **card total for both limbs combined**,
not either action alone. The manifest states this in `shared_target_note`.

## 4. Action matrix

| Action | Band | Verify class | Target | Family | Status |
|---|---|---|---|---|---|
| ENRICH-A033 | E-P3 | PRIMARY_AUTHORITY | `QB4_A.html#q22` | GAP-0207 | IMPLEMENTED |
| ENRICH-A034 | E-P2 | PRIMARY_AUTHORITY | `QB5_A.html#q16` | GAP-0206 | IMPLEMENTED |
| ENRICH-A035 | E-P2 | PRIMARY_AUTHORITY | `QB4_H.html#q7` | GAP-0196 | IMPLEMENTED |
| ENRICH-A036 | E-P2 | PRIMARY_AUTHORITY | `QB4_C.html#q6` | GAP-0112 | **REDUCED SCOPE** |
| ENRICH-A037 | E-P2 | PRIMARY_AUTHORITY | `QB4_C.html#q6` | GAP-0703 | IMPLEMENTED |
| ENRICH-A038 | E-P2 | **CURRENT_REG** | `QB1_F.html#q12` | GAP-0530 | **REDUCED SCOPE** |
| ENRICH-A039 | E-P2 | **CURRENT_REG** | `QB9_H.html#q4` | GAP-0701 | IMPLEMENTED |
| ENRICH-A040 | E-P2 | **CURRENT_REG** | `QB4_H.html#q9` | GAP-0093 | IMPLEMENTED |
| ENRICH-A041 | E-P2 | TECHNICAL_REASONING | `QB4_B.html#q2` | GAP-0466 | IMPLEMENTED (authority upgraded) |
| ENRICH-A042 | E-P2 | TECHNICAL_REASONING | `QB4_B.html#q3` | GAP-0560 | IMPLEMENTED |
| ENRICH-A043 | E-P2 | TECHNICAL_REASONING | `QB5_D.html#q3` | GAP-0377 | IMPLEMENTED (scoped) |
| ENRICH-A044 | E-P3 | TECHNICAL_REASONING | `QB5_C_A.html#q7` | GAP-0325 | IMPLEMENTED |

Priority mix **10 × E-P2, 2 × E-P3, no E-P1**. Verification mix **5 primary, 3
currentness, 4 reasoning-only** — both as the E1 handoff projected.

## 5. Current-live recheck

All eleven target cards were opened in full against the live 721-question corpus
before any edit — q-text, timed blocks, full answer body, CE relevance, examiner
chain, traps, reg-box and deep dives. Every limb was then checked **token by token
against the baseline card**: a limb token the baseline already carried would make the
guard pass without the limb being there at all. That sweep found ten tokens already
present (`documentary evidence`, `shipowner`, `key worker`, `Shipping Master`, `DOC`,
`breakdown`, `corrective`, `disciplinary`, `evaluate`, `sea service require`) and none
of them was adopted as a limb token.

**Zero actions were held. Zero were downgraded to already-covered. Two were reduced in
scope**, which is a different thing and is recorded as such.

## 6. The two reduced actions

### ENRICH-A036 — a sub-limb the instrument does not contain

| | |
|---|---|
| **Original limb** | MLC Title 3 accommodation minima — berth internal dimensions, headroom, floor area per seafarer **and door sill/coaming heights** — as numbers a candidate can quote |
| **Current-live** | The Title 3 bullet reads "Specifies structural dimensions for cabins, mess rooms, ventilation systems". `203`, `198`, `4.5`, `5.5`, `A3.1`, `headroom` and `berth` occur **zero** times |
| **Implemented** | Headroom 6(a); berth 9(d)/9(e); single-berth floor area 9(f); officers 9(k)/9(l); master/CE/chief navigating officer 9(m); plus the Regulation 3.1(2) construction-date limitation and the 2022-amendment currentness position |
| **Omitted** | **Door sill and coaming heights** |
| **Reason** | **Not in the instrument.** The string `door` does not occur anywhere in Standard A3.1. Sill and coaming heights are **Load Line Convention** weathertight-integrity requirements, not MLC accommodation minima. The consolidation conflated two regimes |

Rather than silently dropping it, the card now **names the confusion as the trap**:
"these are MLC accommodation minima — door sill and coaming heights are Load Line
requirements, not MLC ones, and mixing the two is a giveaway." No ICLL figure is
imported, so the addition stays inside the authorised limb. The disclaimer is a
`REQUIRED_QUALIFIER`, because a later tidy-up that deletes it leaves the reader with
the consolidation's original error and nothing to correct it (mutation S).

### ENRICH-A038 — two of three sub-limbs are already on the card

| | |
|---|---|
| **Original limb** | The Indian seafarer welfare funding institutions — the Seamen's Provident Fund **and the seafarers' welfare fund/board machinery**, who contributes and what they pay for — **and the COVID-era relief measures** for stranded and repatriated seafarers |
| **Current-live** | The card already carries the Seafarer's Welfare Board under Part II Chapter I, its grants and welfare funds, hostels, clubs, welfare officers and repatriation of distressed seamen. It also already carries seafarers' **"key worker" status** for unhindered movement, shore leave and medical access. `Provident`, `SPFO` and `contribut` occur **zero** times |
| **Implemented** | The Seamen's Provident Fund only — the Act, the SPFO, automatic membership, matched contributions, what it pays for, and the distinction between contributory social security and grant-funded welfare |
| **Omitted** | The welfare fund/board machinery, and the COVID-era relief measures |
| **Reason** | **Already present in target** for the board machinery. For COVID: the durable, codified legacy of that period *is* the "key worker" status, which the live 60-second block already carries; adding 2020–21 relief measures to a card whose whole frame is the Merchant Shipping Act, 2025 would drag a current-law answer backwards. This is the same currentness narrowing E1 applied to A010 |

**No contribution percentage is stated anywhere.** Sources disagree — one gives an
employer rate rising 6 → 8 → 10 → 12 per cent, another gives 10 per cent from each
party — and `dgshipping.gov.in` was unreachable from this environment throughout the
session (ECONNREFUSED on 164.100.60.201, and curl timeout). The card says the employer
**matches** the seafarer's contribution and that the rate has been **raised in stages
since 1964**, which both sources support, and pins no figure that could not be
verified.

## 7. Claims rejected from the authorisation record

Consistent with E1–E4: **the consolidation authorises which limb to add; it does not
establish what the limb says, and it is not a reliable description of the card's
current state.** Three rejections this batch, one of which would have shipped a wrong
number.

1. **A036 — door sill/coaming heights as MLC Title 3 minima.** Rejected outright; not
   in Standard A3.1 at all (§6).
2. **A034 — the sea-service figures.** A secondary coaching site (July 2024) gives
   MEO Class I as **24 months, or 18** with qualifying second-engineer time. **TEAP
   Part A, Chapter III, Rule 37 gives 36 months, reduced to 30.** The primary text was
   obtained and the secondary figure discarded. Had the batch trusted the readily
   available secondary source, it would have published a wrong number on a
   certification card.
3. **A038 — the COVID-era relief sub-limb**, narrowed on currentness and
   already-present grounds (§6).

A fourth correction runs the other way — see §8 on A041.

## 8. A041 — an authority upgrade, not a downgrade

The consolidation classed `ENRICH-A041` **TECHNICAL_REASONING_ONLY**. It is not.
**ISM Code section 14 answers the limb directly and by name:**

* **14.2.2** — an Interim Safety Management Certificate may be issued *when a Company
  takes on responsibility for the operation of a ship which is new to the Company*.
  That is the change-of-management case, in the Code's own words.
* **14.1** — Interim Document of Compliance, not exceeding **12 months**.
* **14.3** — Interim SMC extendable in special cases by a further **6 months**.
* **14.4.1–.6** — the triage the limb asks for: the DOC is relevant to the ship, the
  SMS includes the Code's key elements, the master and officers are familiar with it,
  information is in a working language the crew understand, **instructions identified
  as essential are provided prior to sailing**, and the Company has **planned the
  internal audit within three months**.

The action was written against primary text rather than reasoned, which strengthens it
beyond its declared verification class. `AUTHORITY_TOKENS` for A041 requires ISM 14.1
and 14.2.2 on the card, and `prior to sailing` is a required qualifier. **Do not
downgrade this back to reasoning-only.**

## 9. Authority — every action primary, or explicitly reasoning-only

| Action | Authority |
|---|---|
| A033 | **STCW Regulation III/1** — OICEW in a manned engine-room or designated duty engineer in a periodically unmanned engine-room, ships of **750 kW propulsion power or more**; not less than **18 years**; either **12 months** combined workshop skills training and approved seagoing service under an approved training programme with onboard training meeting **Code section A-III/1** in an approved training record book, or **36 months** combined of which **30 months** is engine-department seagoing service; and engine-room watchkeeping **under the supervision of the chief engineer officer or a qualified engineer officer for not less than six months** |
| A034 | **TEAP Part A (Consolidated Rev. 1, 1 May 2015), Chapter III**, restating **Rules 35–37 of the M.S. (STCW) Rules**. Class IV: stream-dependent, ten streams, Flow Diagrams III/1 and III/2, TAR book published by IME(I) in the Directorate-approved format. Class II: **12 months** as Assistant Engineer Officer or OIC EW on ships of **750 kW or more** after Class IV, plus the approved **4-month** competency course. Class I: **36 months** on ships of 750 kW or more including **12 months as OIC EW after Class II** on ships of **3,000 kW or more**, **reduced to 30 months** if twelve of them were as **Second Engineer Officer** on a ship of 3,000 kW or more, or pro rata, plus the **2-month** Engineering Management Course and Machinery Space Simulator Training |
| A035 | **STCW Regulation I/1** (definitions: CoP is a certificate other than a CoC; documentary evidence is documentation other than a CoC or CoP); **Regulation I/2** (issue and endorsement by the Administration only, on full verification of authenticity and validity since the 2010 Manila amendments); **Regulations I/6 and I/8** (training and assessment; quality standards); **Regulations VI/1, VI/2, VI/3** with **Code sections A-VI/1 ¶3, A-VI/2 ¶¶5 and 11, A-VI/3 ¶5** for the five-yearly evidence of maintained competence; **A-VI/4** and **A-VI/6** carry no fixed STCW five-year refresher |
| A036 | **MLC 2006 Standard A3.1** ¶6(a) headroom **203 cm**; ¶9(d)/(e) separate berth, minimum inside dimensions **198 × 80 cm**; ¶9(f) single-berth floor area **4.5 / 5.5 / 7 m²** by tonnage band; ¶9(k) officers without private day room **7.5 / 8.5 / 10 m²**; ¶9(l) junior officers = operational level, senior officers = management level; ¶9(m) master, chief engineer and chief navigating officer to have an adjoining sitting room, day room or equivalent. **Regulation 3.1 ¶2** — construction and equipment requirements apply only to ships constructed on or after entry into force for the Member. **2022 amendments (in force 23 December 2024)** amended Regulation 3.1 at ¶17 only (social connectivity); **no dimension changed** |
| A037 | **MLC 2006 Titles 1–4** impose their obligations on the **shipowner**; **Title 5** is the compliance and enforcement layer. **Standard A5.1.3** — DMLC Part I by the competent authority, Part II by the shipowner. **Merchant Shipping Act, 2025 (Act No. 24 of 2025), Part V — Seafarers**, in force **15 March 2026** |
| A038 | **Seamen's Provident Fund Act, 1966**; the **Seamen's Provident Fund Organisation**, a statutory body under the Ministry of Ports, Shipping and Waterways; automatic membership for seafarers employed in the Indian merchant navy; matched employer contribution; retirement, death, assistance and partial-withdrawal benefits. **No percentage asserted** |
| A039 | **MS Notice No. 03 of 2013** (Grievance Redressal Mechanism), as reproduced in the Directorate's Crew Manual — **Designated Grievance Redressal Officers** are the Surveyors-in-Charge at the smaller MMDs, specially designated officers in the offices of the Principal Officers MMD at Chennai, Kandla, **Kochi**, Kolkata and Mumbai, and the Shipping Masters at Chennai, Kolkata and Mumbai; submission only after the RPS provider/employer/shipowner has been approached; registration within **three working days**; disposal by speaking order within **thirty working days**; **First Appellate Authority** the jurisdictional Principal Officer MMD (thirty days; disposal thirty, extendable to sixty); **Second Appellate Authority** a designated officer at the Directorate's headquarters in Mumbai, decision **final and binding**. **MS Notice No. 04 of 2013** preserves the direct routes |
| A040 | **ILO/IMO Guidelines on the medical examinations of seafarers (2013)**; **STCW Regulation I/9** and **MLC Standard A1.2** — **two years**, **one year** under 18, **colour vision six years**; **MLC Standard A1.2 ¶9** — expiry in the course of a voyage continues to the next port with a duly qualified practitioner, never more than **three months**; **2022 amendments in force 23 December 2024** added to **Regulation 4.1** prompt disembarkation for immediate medical care and repatriation of remains — **validity periods unchanged**; **April 2025 ILO STC amendments adopted, not yet in force** |
| A041 | **ISM Code 14.1, 14.2.2, 14.3, 14.4.1–.6** (§8) |
| A042 | **ISM Code Sections 10.2 and 10.3**; the taxonomy itself (planned/preventive, corrective/breakdown, condition-based, predictive, risk-based) is named as terms of art with no clause asserted, and the class-approved planned maintenance scheme is described as requiring Class or Administration approval without citing a specific rule |
| A043 | **TECHNICAL_REASONING_ONLY** — the rungs are company disciplinary practice under the SEA/CBA and the SMS; no clause number is asserted |
| A044 | **TECHNICAL_REASONING_ONLY** — Bloom's revised taxonomy named as an educational framework, tied back to the card's own Show-Do-Check sequence and training-record sign-off; no convention provision asserted |

## 10. A043 — the limb that could have contradicted its own card

`QB5_D#q3` teaches, correctly, that harassment is **not** ordinary conflict, that
compromise is the wrong outcome, and that informal mediation between a senior and a
junior resolves in the senior's favour. The authorised limb is a **graded ladder
beginning at counselling and informal correction** — which, written unqualified, reads
as a licence to do precisely what the card forbids.

The addition is therefore scoped explicitly to the **disciplinary and corrective
response after the facts are established**. It opens by saying that everything above
it is the handling of the complaint and that none of *that* is graded, and it closes
with two guarded sentences: the ladder is entered **only after** the complaint has
been recorded and investigated, and it applies to the perpetrator — it is **never a
menu for settling the matter between the two seafarers**. Both are
`REQUIRED_QUALIFIER`s and mutation **T** proves the guard fires when the second is
flattened.

Written any other way, an authorised limb would have degraded the answer it was added
to. That is a general lesson for the remaining batch, not a one-off.

## 11. Currentness review — the three CURRENT_REG actions

| Action | Instrument | Latest amendment / status | Effective | Was the card stale? |
|---|---|---|---|---|
| **A038** | Seamen's Provident Fund Act, 1966; SPFO under MoPSW | Act in force; SPFO live under the Directorate's crew division | — | Not stale — **silent**. The card carried the Welfare Board and no contributory fund |
| **A039** | MS Notice No. 03 of 2013, as carried in the Directorate's Crew Manual | Mechanism current; DGS renamed DGMA, which the card already reflects | 30 Jan 2013 | Not stale — **incomplete**. The card reached for "the Indian Shipping Master/DGMA machinery" without naming the office |
| **A040** | STCW Reg. I/9; MLC Std A1.2; ILO/IMO Guidelines 2013; MLC Reg. 4.1 as amended 2022 | 2022 amendments **IN FORCE**; April 2025 STC amendments **ADOPTED, NOT IN FORCE** | **23 Dec 2024** | Not stale — **silent on validity**. Section 4 named the guidelines and stopped |

**Adopted ≠ in force** is guarded in both directions: `not yet in force` is a required
qualifier and asserting the April 2025 package is in force is a forbidden claim
(mutation U). `23 December 2024` is a required qualifier and staledating it is caught
(mutation R).

The A036 currentness position was verified even though A036 is not a CURRENT_REG
action: the 2022 amendments **did** touch Regulation 3.1, so the dimensions had to be
re-checked against the amendment rather than assumed. They changed ¶17 only.

## 12. Notes used

**None.** No action in this batch drew on the `oralnotes/` product. Every authority is
primary text, an official Administration instrument, or explicitly declared technical
reasoning.

## 13. Changed sections

Every edit is confined to the **answer body**. No reg-box, timed block, CE tip, trap
box, numbers box, mental map, deep dive or related-questions block was touched.

| Action | Section added |
|---|---|
| A033 | h4 "The rung below — where the engineer ladder actually starts" + lead + 3-item list |
| A034 | h4 "What TEAP Actually Sets Out — Engineer Sea Service" + lead + 3-row table + distinction para |
| A035 | h4 "How a CoP Is Actually Obtained" + lead + 4-item list + category para |
| A036 | h4 "Title 3 Accommodation — the Numbers to Quote" + lead + 5-item list + qualifier para |
| A037 | h4 "The Third Duty-Holder — the Shipowner" + 2 paras |
| A038 | h4 "The Funding Institution — Seamen's Provident Fund" + 2 paras |
| A039 | h4 "The Indian rung the ladder usually leaves unnamed" + lead + 4-item list + preservation para |
| A040 | 2 paras appended to the Seafarer Medical Fitness Certificate section |
| A041 | h4 "When It Is a Change of Management, Not a Change of Chief" + lead + 3-item list + reservation para |
| A042 | h4 "Naming the Types of Maintenance" + lead + 5-item list + management para |
| A043 | h4 "The graded response — what happens after, not instead" + lead + 4-item ordered list + selection para |
| A044 | h4 "Setting the Objective — Bloom's Taxonomy" + lead + 5-item list + assessment para |

A036 and A037 are delivered by **one insert** on the shared card, A037's block first.

## 14. Additivity — normalised, character level

**11 insert opcodes. 0 delete. 0 replace.** One insert per card, measured against the
`origin/main` blob on LF-normalised text.

| File | Card | Opcodes | Chars added |
|---|---|---|---|
| QB4_A.html | q22 | ins=1 del=0 rep=0 | +1745 |
| QB5_A.html | q16 | ins=1 del=0 rep=0 | +2528 |
| QB4_H.html | q7 | ins=1 del=0 rep=0 | +2158 |
| QB4_H.html | q9 | ins=1 del=0 rep=0 | +1642 |
| QB4_C.html | q6 | ins=1 del=0 rep=0 | +3506 (both limbs) |
| QB1_F.html | q12 | ins=1 del=0 rep=0 | +1197 |
| QB9_H.html | q4 | ins=1 del=0 rep=0 | +2356 |
| QB4_B.html | q2 | ins=1 del=0 rep=0 | +2712 |
| QB4_B.html | q3 | ins=1 del=0 rep=0 | +1949 |
| QB5_D.html | q3 | ins=1 del=0 rep=0 | +2210 |
| QB5_C_A.html | q7 | ins=1 del=0 rep=0 | +1851 |

Line-level diffstat is **96 insertions, 0 deletions** across 9 files, reported only as
corroboration, never as the proof.

### Two mechanical traps hit while producing that proof

**The shared marker.** `QB4_B#q2` and `#q3` contain the *identical* string
`<h4>Chief Engineer Relevance</h4>`. A file-global `str.replace` would have put A042's
block inside A041's card and left A042's own card untouched — and the digests would
still have "changed", so a naive count would have passed. Every insertion is therefore
**card-scoped**: the card is extracted by anchor, the marker is required to occur
exactly once *inside that card*, and the rewritten card is required to occur exactly
once in the file. This is the same no-op/wrong-anchor class the content-index work
recorded in August.

**The line-ending probe was wrong.** A first pass used `grep -c $'\r'` and reported all
nine destination files as 100% CRLF. They are **100% LF**; the shell pattern matched
every line. Measuring the bytes in Python settled it. Had the insertions been written
with CRLF on that evidence, every one of them would have been mixed-ending on disk.
**Line-ending state must be measured on untranslated bytes, not inferred from a shell
line count.**

A first application also **doubled the marker's indentation** on five cards, because
the inserted block's trailing whitespace was added *in front of* indentation the marker
already carried. That is purely additive, so the character-level proof could not see
it. The applier now derives the required trailing indentation from the marker's own
line and the edits were re-applied from a clean checkout of the nine files — the
content being fully reproducible from the generator script.

## 15. Timed-block delta — zero

All eleven cards: 15-second and 60-second blocks **byte-identical** to baseline. No
timed block was touched, so no word-count rebalancing was needed or done. Mutation W
proves the guard fires if one drifts.

## 16. Follow-up overlap — three of twelve, none implemented

Re-derived from the current consolidation, not carried from the brief.

| Action | Target | Follow-up | Follow-up ask | Distinct? |
|---|---|---|---|---|
| A038 | `QB1_F#q12` | GAP-0523 | "Sturucture of MS act, preamble" | **Yes** — a funding institution is not the statute's layout |
| A036 | `QB4_C#q6` | GAP-0511 | "Complaint redressal mechanism" | **Yes** — accommodation minima are not complaint handling |
| A037 | `QB4_C#q6` | GAP-0511 | "Complaint redressal mechanism" | **Yes** — the duty-holder taxonomy is not complaint handling |

A039 adds the Indian grievance ladder to `QB9_H#q4`, a **different card** from
GAP-0511's `QB4_C#q6` and a different ask, so the two do not collide.

All three remain open follow-up work. **Follow-up workload unchanged at 35 groups.**

## 17. Candidate-visible hygiene — one new finding, not repaired

`QB9_H#q4` carries **internal status language in candidate view**, twice:

> *[MS Act 2025 — Part-level, sections pending verification]*
> *[2025 Act — Part-level pending verification]*

Pre-existing, left by an earlier session, and **outside E5's authorised limb**, so it
was not repaired. It is recorded here as debt. It survived every earlier gate because
the shared `FORBIDDEN` regex bans uppercase `VERIFY` only — lowercase "pending
verification" never matched. E5's validator adds `pending verification` and
`sections pending` to its own pattern.

The irony is worth stating plainly: **A039's limb lands on that exact card**, and the
new prose names the Indian machinery the old bracket admitted it could not verify. The
bracket is now factually obsolete as well as leaky. Repairing it is a delete/replace
outside the limb, so it stays for a scoped follow-up.

The hygiene scan therefore runs on the **added text only** — scanning the whole card
would fail the batch for text it did not write and cannot touch. Mutation E proves the
scan still catches a leak in new prose.

## 18. Sibling-manifest delegation — no maintenance needed

`batch_e5_enrichment_manifest.json` was created **before** any prior guard ran. That
ordering is load-bearing: the exemption in every earlier guard is keyed on a glob over
`batch_*_manifest.json`, so in the window before the manifest exists, A–D, GAP-0609 and
E1–E4 would all report genuine-looking drift on eleven legitimately edited cards.

With the manifest in place, **every prior guard passed unchanged and no guard
maintenance was required** — the first batch since E2 needing none. E5's own validator
carries the same exemption from the start, so it cannot expire when E6 lands.

Not vacuous: mutation **C** targets `QB1_H.html#q1`, a card no manifest owns, and the
harness **asserts that fact at run time** before running rather than trusting it.

**Sibling pin delegation: none needed.** No earlier manifest pins any of the eleven E5
targets.

## 19. E5 validator

`tools/oral/validate_batch_e5.py` — **27 checks, 0 FAIL.**

Beyond the properties inherited from E1, three are new:

* `shared_target_actions_enumerated` — the manifest must name both partners against the
  shared target, and that declaration must equal the set derived from the card list.
* `shared_target_limbs_independently_present` — each partner's own limb tokens must be
  on the shared card, so the two actions cannot collapse into one another.
* `mlc_part_a_and_b_not_conflated` — a mandatory Standard presented as guidance, or a
  Guideline presented as mandatory, fails outright on every MLC action in the batch.

The validator caught a real defect during development: `Rules 35 to 37` is what the
A034 card says, and the guard had been written against `Rule 37`. The card was right
and the token was wrong; the token was corrected rather than the card.

## 20. E5 mutations

**25 mutations. 0 escapes, 0 no-ops, 0 crashes.** Tree byte-identical afterwards.

| | Mutation | Caught by |
|---|---|---|
| A | omit one authorised action from the manifest | `authorised_action_set` |
| B | retarget an action to the wrong anchor | `authorised_targets` |
| C | alter a neighbouring card no manifest owns | `only_authorised_cards_changed` |
| D | blank one supplied limb (A042 taxonomy) | `missing_limb_supplied` |
| E | inject an internal action id into candidate prose | `no_candidate_visible_metadata` |
| F | add a canonical q-card | `canonical_total_unchanged` |
| G | misstate the canonical corpus total | `canonical_total_unchanged` |
| H | strip a required STCW authority (A033) | `required_authority_cited` |
| I | alter the q-text of an authorised card | `q_text_and_anchors_stable` |
| J | claim an examiner relationship delta | `examiner_relationship_delta_zero` |
| K | delete baseline text from an authorised card | `edits_purely_additive` |
| L | break manifest/consolidation disposition identity | `authorised_enrichment_disposition` |
| **M** | **drop A036 but leave A037 on the shared card** | `shared_target_actions_enumerated` |
| **N** | **drop A037 but leave A036 on the shared card** | `shared_target_actions_enumerated` |
| **O** | **collapse A036 and A037 into one action id** | `shared_target_actions_enumerated` |
| **P** | **make a mandatory MLC Standard read as guidance** | `mlc_part_a_and_b_not_conflated` |
| **Q** | **make MLC Part B guidance read as mandatory** | `mlc_part_a_and_b_not_conflated` |
| **R** | **staledate the 2022 amendments' entry into force** | `required_qualifiers_kept` |
| S | delete the Load Line disclaimer on A036 | `required_qualifiers_kept` |
| T | flatten A043's not-a-mediation thesis | `required_qualifiers_kept` |
| U | assert the April 2025 amendments are in force | `unsubstantiated_claims_absent` |
| V | falsify a recorded post-edit digest | `manifest_digests_match` |
| W | edit a timed block on an authorised card | `timed_blocks_unchanged` |
| X | revert one authorised card to baseline | `every_authorised_card_changed` |
| Y | claim the A3.1 dimensions bind every ship afloat | `unsubstantiated_claims_absent` |

## 21. The mutation-C incident — a harness that certified nothing

**The first standalone E5 mutation run was not clean: 25 run, 24 caught, 0 escapes,
1 NO-OP, 0 crashes.** Mutation C was the no-op. It is recorded here rather than
smoothed over, because the failure mode is the most dangerous one a mutation harness
has.

**Root cause.** C was anchored on `</div>\s*\Z` — a `</div>` at end of file.
`QB1_H.html` ends with `</html>`, so the pattern never matched, the write changed no
bytes, and the mutation exercised nothing. The harness reported `NO-OP (not applied)`
exactly as designed; had it counted an unapplied mutation as a pass, E5 would have
shipped believing the sibling-manifest exemption had been proven in the negative
direction when it had not.

**Repair.** Re-anchored **inside** the unowned card, on its opening `q-card` div.

**Isolated re-test after repair:** applied (**+15 bytes**), validator exit 1, caught by
`only_authorised_cards_changed` — the intended semantic reason, not an incidental
digest check — and restored byte-identical.

**Release-suite result:** `C  alter a neighbouring card no manifest owns  caught
(only_authorised_cards_changed)`, inside a run of **25 mutations, 0 escapes, 0 no-ops,
0 crashes**.

**Contract, now explicit:** *a mutation that does not alter its target certifies
nothing, and its caught result must not be accepted.* The harness already enforced
this by reporting no-ops separately; what was missing was a reviewer reading that line.

## 22. The control-byte incident

Repairing mutation C introduced a second defect. The patch was applied through a shell
heredoc, and the replacement backreference `\1` reached Python as a **non-raw string
escape**, where `\1` is octal for **U+0001**. The file was written with a literal
**SOH control byte** in place of the backreference. The mutation would have replaced
the card's opening tag with a comment instead of inserting after it.

This is the same class E1 recorded, in a new form — E1's was a `\b` becoming a
backspace byte (0x08). **A backslash escape that survives one layer of quoting will not
survive two.**

Repaired by rebuilding the backslash from its codepoint rather than writing it as an
escape. All three E5 artefacts — validator, mutator and manifest — now scan **clean of
every C0 control byte** except TAB, LF and CR, and both Python files parse.

## 23. Verification

| Property | Result |
|---|---|
| Canonical total | **721 → 721** (equality vs baseline `e47c7e6`) |
| Question-bearing files | **86**, unchanged |
| Cards added / removed | **0 / 0** |
| Cards changed corpus-wide | **exactly 11**, all authorised, 0 unauthorised |
| Edits purely additive | **yes** — 11 insert opcodes, 0 delete, 0 replace, LF-normalised |
| q-text / anchors | unchanged on every card, corpus-wide |
| DOM | balanced on all eleven, ids unique, all under `#q-feed`, no nested lists |
| Candidate-visible hygiene | clean on all added text |
| `build_qb_content_index --check` | **CURRENT — no regeneration** (86 files / 721 questions) |
| `build_examiner_index --check` | **960 relationships / 7 examiners — zero delta**, 4/4 artefacts current |
| Public corpus count | **721**, unchanged. Pricing untouched |
| Determinism | **26 artefacts / 0 non-reproducible** under `PYTHONHASHSEED` 0 / 1 / 524287 |

### Full release suite — 37 gates, every one executed

37 gate records, **37 unique, 0 duplicates, 0 skipped**. Total wall time 6,657s.

All 37 completed; **36 exited 0 on the first attempt**. `node_security_tests` exited 1
in 0.4s — a **runner invocation defect, not a gate failure**: Node 24 resolves
`--test <dir>` as a module to load and reported `Cannot find module`. Re-run correctly
as `node --test tools/security/*.test.mjs`: **611 tests, 610 pass, 0 fail, 1 skipped,
exit 0**, covering deploy-surface, regulatory-facts and link-integrity.

### Mutations — 233 across 14 suites, 0 escapes, 0 no-ops, 0 crashes

`content_index` 26 · `batch_a` 8 · `batch_b` 10 · `batch_c` 10 · `batch_d` 12 ·
`gap0609` 8 · `batch_e4` 12 · `batch_e3` 16 · `batch_e2` 18 · `batch_e1` 25 ·
**`batch_e5` 25** · `examiner` 13 · `ce_tip` 17 · `phase2` 33. Every suite ended
byte-identical.

**A parser caveat, met again.** A first aggregation reported 8 escapes. The
`gap0609` harness prints `mutations=8 escapes=0`, and a pattern of the form
`(\d+)\s*escape` reads the **8** as the escape count. Classification must key on the
`escapes=N` form before the bare-number form. This is the same failure shape as reading
a mutator's `FAIL:` lines as gate failures — the summary must be parsed, not
pattern-matched loosely.

### Audit validator — semantic result, not exit code

`validate_audit` reports **`passed 12 / failed 1 / unavailable 0`** while exiting **0**.

Run on a **detached clean `origin/main` worktree** at `e47c7e6`, the result is
**identical**: same counters, same failing check, same failure detail.

**PRE-EXISTING AUDIT BASELINE — ZERO E5 AUDIT DELTA.** Reported here rather than
counted as green, because reading the exit code alone would call it a pass. Carried
debt from E1–E4, still unfixed.

### Health check — multiset baseline

`qb_health_check`: **370 findings on both the E5 branch and a clean `origin/main`
worktree**, compared as multisets — **0 new, 0 gone**. Emission order differs
(`PYTHONHASHSEED` unpinned), so a line-order diff would have manufactured a false
regression.

**A comparison artefact worth recording.** A first comparison reported **481 new
lines**. Every one was a blank line: the suite runner wrote captured output through a
newline-translating stream, turning each `\r\n` into `\r\r\n` and doubling the line
count. The only genuine difference between the two runs is the wall-clock timestamp in
the report header. **A baseline comparison must normalise the transport before it
compares the content** — otherwise the logger's own behaviour is read as a regression
in the product.

### Gate-generated artefacts

Two files dirtied by the suite, both reverted by **exact path**, never a blanket
restore: `VALIDATION_RESULTS.json` and `PHASE2_VALIDATION_RESULTS.json`, attributed to
`validate_audit.py` / `validate_phase2.py` and their mutators. The diff is entirely the
known stale-counter debt (`live_questions` 688 → 721, `headings=954` → `960`). E5 card
digests were re-verified intact afterwards.

**Pre-existing debt observed, not fixed:** the committed copies remain stale, so any
gate run rewrites them. Unchanged from E1.

## 24. Status

- Brand-new answer inventory: **COMPLETE 33/33**, unchanged.
- Canonical corpus: **721**, unchanged. Public count unchanged. Pricing untouched.
- Examiner index: **960 relationships / 7 examiners**, delta zero.
- Enrichment workload: **18 → 6 unique actions remaining** (E5's twelve complete).
- Follow-up workload: **35 groups**, unchanged.
- Master XLSX: **deferred**.

## 25. Next batch — E6, derived from current consolidation data

Re-derived from `FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json` rather than taken from the
brief, and confirmed on **both** representations.

**E6 — IMO instruments, maritime law and pollution response. 6 actions:**
`ENRICH-A045`, `A046`, `A047`, `A048`, `A049`, `A050`.

Band mix 1 × **E-P1** (the last remaining E-P1 in the whole programme), 3 × E-P2,
2 × E-P3. Verification mix 1 primary, **3 currentness**, 2 reasoning-only — **50%
currentness exposure**, twice E5's rate, and the reason E3's handoff deprioritised it.
One follow-up colocation: `ENRICH-A046` on `QB9_G#q3` with GAP-0481 (Maritime Single
Window / Sagar Setu).

Nothing in E5 touched any E6 target, so their current-live status is unchanged by this
batch.

## 26. Determinism

`check_determinism.py` run **bare** — the tool has no argv parsing at all, so there is
no safe flag to probe; E1's `--help` executed the entire generator chain for exactly
that reason. Seeds are hardcoded `0`, `1`, `524287`.

**26 artefacts / 0 non-reproducible.** Afterwards a single tracked artefact was dirty,
`ORAL_NOTES_IMPACT.md`, attributed to `report_notes_impact.py` in the same generator
sequence and reverted **by exact path**. All twelve E5 action digests were re-verified
intact after the revert.

## 27. Render

**NOT BROWSER VERIFIED.** One genuine attempt was made: the preview pane serves files
outside the project folder as static snapshots that execute no JS and expose neither
DOM nor page text; `get_page_text` returned "No site is open in this tab." No browser
claim is made. This reproduces E1's finding exactly.

Substituted and clean on all eleven cards: div balance, `<p>` and `<li>` balance, id
uniqueness, `#q-feed` parentage, q-text stability, candidate-hygiene regex over the
**added text only**, and nested-list, fixed-width and long-token scans — all zero.

**One static-check trap worth recording.** A first tag-balance pass reported an
unclosed `<p>` on both `QB4_B` cards. It was an artefact: the balance was computed over
the *difflib insert region*, and difflib had aligned the region boundary on a bare `>`
character, so the extracted fragment began and ended mid-tag. Counted over the whole
card, both are balanced — 9→11 and 10→12 paired `<p>`/`</p>`. **A structural check must
run on a well-formed unit, not on a diff hunk.**

## 28. New debt (5)

1. **`QB9_H#q4` leaks internal status language to candidates** — "[MS Act 2025 —
   Part-level, sections pending verification]", twice. New finding, pre-existing,
   outside the limb (§17). Now doubly obsolete because A039 supplies the very
   machinery the bracket said was unverified. Scoped follow-up.
2. **`validate_audit` still exits 0 while reporting `failed: 1`.** Carried from E1–E4.
   Failing check `index_tier_literals_valid`.
3. **Committed gate-result artefacts are stale.** `VALIDATION_RESULTS.json` (688
   questions, 954 headings) and `PHASE2_VALIDATION_RESULTS.json`. They dirty on every
   gate run. Unchanged from E1.
4. **`qb_health_check` output order is hash-seed dependent.** Harmless under multiset
   comparison; any future line-order diff will report false regressions.
5. **`QB4_C#q6` carries two pre-existing structural defects.** Its flag/port State
   table has 3 header columns but only 2 cells in two of its rows, so the port-State
   text is glued into the flag-State cell; and the CE tip ends with a stray `--` with
   `**` markdown leakage in the deep dive. Pre-existing, outside the limb, untouched.

## 29. Verdict

**GO** — Final Oral Enrichment Batch E5 complete. All twelve authorised
STCW/MLC/crew/management edits verified against primary authority, two reduced on
instrument-text and already-present evidence and recorded as such, purely additive at
character level, 721 → 721, examiner delta zero, 233 mutations across 14 suites with
zero escapes, zero no-ops and zero crashes, audit and health baselines identical to
clean `origin/main`, determinism reproducible across three seeds.
