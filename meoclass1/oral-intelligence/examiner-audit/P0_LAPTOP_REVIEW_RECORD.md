# Oral P0 — Laptop final content review and integration record

**Reviewer:** Laptop session, 19 August 2026
**Reviewed:** `origin/prod/oral-p0-pre24aug` @ `35d7684` (Desktop), cut from `0242774`
**Integrated onto:** `origin/main` @ `8b1f6a2`
**Branch:** `review/oral-p0-final-content`

**Verdict: 9/9 content items approved.** Two defects were found and repaired
during integration; neither was a wrong answer in an approved item, and no tenth
item was authored.

---

## 0. Repo truth and scope

`origin/main` had moved one commit past the Desktop baseline (`0242774` →
`8b1f6a2`, "number the purchase flow and state the real order"). That commit
touches `SQ/index.html`, `SQ/pay.html`, `SQ/trial.html` only — **no overlap with
the eight P0 QB files** — so the merge was clean and no deliberate conflict
resolution was needed.

The Desktop diff scope was exactly as briefed: eight QB files,
`meoclass1/index.html`, `qb_content_index.json`, two bounded P0 docs. No
forbidden surface appeared — `examiner-index.html`, `SQ/`, payments,
`pastpapers/`, Written QI, magazine and the matcher tools were all untouched by
Desktop.

---

## 1. Two integration repairs

### R-1 — the girding card was nested outside the question feed (layout defect)

A stray `</div>` sat between Q8's card and the new Q9 in `QB1_K`. Tag **counts
balanced** (175 open / 175 close), there were no duplicate ids and no broken
links, so every structural check Desktop ran passed.

Balance is not nesting. The extra close terminated `#q-feed` early, and an HTML
parse put `q9` at **depth 4 as a sibling of the feed**, while every other card in
the corpus sits at depth 5 inside it. `.main-layout` is a CSS grid of
`220px | 1fr`, so as a third grid child the girding card would have rendered
**in the sidebar column, about 220px wide**.

Repaired by deleting the stray tag. Re-parsed to 0 stray closes, 0 unclosed
elements, `q9` at depth 5. All eight files were swept for this class — `QB1_K`
was the only one affected.

### R-2 — the girding card cited the wrong Intact Stability Code chapter

The card cited **"2008 IS Code (Res. MSC.267(85)) Part A section 2.4 — towing and
escort-operation stability criteria"**, in the reg-box and again in the "Numbers
and terms to carry" deep-dive, and told the candidate that was the instrument to
name for tug stability.

Part A **2.4 is the severe wind and rolling (weather) criterion**. The towing and
escort criteria are **Part A chapter 2.8**, introduced by the 2016/2018
amendments (Res. MSC.443(99) amending Part A; Part B ch. 2.8 carries the matching
recommended design criteria) and applying to keels laid on or after
**1 January 2020**. A candidate quoting 2.4 would have been quoting the weather
criterion at the examiner. Corrected in both places.

---

## 2. Item-by-item

| P0 | Target | Type | Verdict | Note |
|---|---|---|---|---|
| GAP-0002 | `QB1_K#q9` | Notes→QB promotion | **APPROVED** after R-1 + R-2 | mechanism, heeling couple, gog rope, tractor/ASD geometry all correct; release framed on rate of increase of heel, which is the right judgement; Notes material reused, ICS citation correctly not carried over |
| GAP-0034 | `QB6#q10` | ENRICH | **APPROVED** | tri-fuel limb only; dual-fuel answer, LEL thresholds and IGF material untouched; TFDE/DFDE correctly separated; HFO-in-diesel-mode is the right distinction |
| GAP-0043 | `QB5_B#q4` | ENRICH | **APPROVED** | assertiveness on the passive/assertive/aggressive scale, PACE graded assertiveness, empathy separated from sympathy and from agreeing; five leadership theories untouched |
| GAP-0409 | `QB7_I#q2` | ENRICH | **APPROVED** | remained an enrichment; no duplicate ME-Gx card; ME-GI and ME-GA still distinct; the commercial limb is genuinely new |
| GAP-0016 | `QB1_A#q31` | NEW | **APPROVED** | **3 × `href="#q30"` confirmed**; MEPC 84 material signposted, not restated |
| GAP-0042 | `QB5_D#q3` | NEW | **APPROVED** | the two amendment layers are correctly separated; treats prohibited conduct as a safety and legal matter, not mediation |
| GAP-0048 | `QB4_A#q21` | NEW | **APPROVED** | class / RO / IACS boundaries correct; dual class correctly stated as harder and dearer, not softer |
| GAP-0044 | `QB4_A#q22` | NEW | **APPROVED** | four STCW layers plus a national layer; V/4 correctly not claimed as an engineer's certificate |
| GAP-0410 | `QB3_J#q6` | NEW | **APPROVED** | "the ship cannot measure D-2" is the right spine; no confusion with the Situational Leadership D2 |

Candidate test: each of the nine can be answered from its own card without
needing another card that does not exist. GAP-0016 and GAP-0410 depend on each
other only by signpost, and each stands alone.

---

## 3. Primary-source verification of load-bearing claims

| Claim | Source | Result |
|---|---|---|
| Towing/escort stability is IS Code **Part A 2.8**, not 2.4; Res. MSC.443(99); keels on/after 1 Jan 2020 | IMO resolution index; imorules | **CORRECTED** — see R-2 |
| BWM adopted 13 Feb 2004, in force 8 Sep 2017; B-3 phase-in complete 8 Sep 2024 | IMO BWM pages | verified |
| D-2 limits (<10/m³ ≥50 µm; <10/mL 10–50 µm; Vibrio <1, E. coli <250, Enterococci <100 cfu/100 mL) | BWM Annex Reg. D-2 | verified — `&lt;` entities intact in the markup |
| D-1 95% exchange; B-4 200 nm / 200 m, fallback 50 nm / 200 m | BWM Annex Reg. D-1 / B-4 | verified |
| G7 MEPC.289(71) · G8 MEPC.279(70) · G9 MEPC.169(57) · BWMS Code MEPC.300(72) | IMO resolution list | verified |
| UV uses no Active Substance, so it does not go through G9 | BWM G9 scope | verified |
| USCG UV type approval December 2016 (Optimarin 2 Dec; Alfa Laval PureBallast 3 23 Dec); CMFDA/FDA vs MPN | USCG MSC records; Alfa Laval; trade press | verified |
| G2 sampling = MEPC.173(58); 46 CFR Part 162 | IMO / US CFR | verified |
| IACS founded 1968; **12 members**; >90% of cargo-carrying tonnage; RS withdrawn **11 Mar 2022**; Türk Loydu most recent (1 Nov 2023) | IACS; RS statement; trade press | verified — 12 is current for 2026 |
| RO Code MSC.349(92) / MEPC.237(65); SOLAS XI-1/1 | IMO | verified |
| MLC 2022 amendments **in force 23 Dec 2024**; April 2025 STC package adopted 11 Apr 2025, **not in force**, expected 23 Dec 2027 | ILO; DNV; BIMCO | verified — the card says "around December 2027", correctly hedged |
| STCW III/2 at **3,000 kW or more**; Table A-III/2; I/11 five-yearly revalidation; V/3, V/2, V/4 (V/4 masters and deck officers) | STCW Convention and Code | verified |
| MAN discontinued the ME-GA over IMO methane-slip regulation; ME-GI / ME-LGIM the alternative | MAN ES; DieselNet; LNG Prime | verified. Nuance: the decision is dated **18 Oct 2024** and was reported in November 2024. The card's "November 2024" is defensible and does not change the answer, so it was left as written |

No number was approved from memory.

---

## 4. Deliberately withheld claims — both upheld

1. **How many ROs India recognises** — withheld. DG Shipping publishes the
   authorised list by circular and it changes. The card teaches the authorisation
   framework (Merchant Shipping Act + RO Code) and tells the candidate to confirm
   the current circular. **Approved as the correct conservative answer** —
   inventing this number is precisely the failure the question is built to
   produce.
2. **The current DGS MEO Class I syllabus and durations** — withheld, named as
   revised by circular, with the same instruction to confirm. **Approved.**

`Is IRS mandatory for an Indian-flag ship?` is answered **No** — the ship must
use a DGS-recognised organisation, and IRS is one of them. Correct.

---

## 5. Counts and structure — derived, not trusted

- Canonical questions counted from **live HTML**: **688** (682 + 6). Manifest
  total **690**; the two extra are `QB1_A#family-trees` and `#dependency-graph`,
  which are revision cards, not questions. 86 QB files carry cards.
- Exactly **six** new canonical anchors, all present and unique: `QB1_K#q9`,
  `QB1_A#q31`, `QB5_D#q3`, `QB4_A#q21`, `QB4_A#q22`, `QB3_J#q6`.
- The three enrichments added **no** cards.
- 0 duplicate ids; 0 broken in-page fragments; 0 broken cross-file anchors across
  the eight QB files, both examiner-index pages and both hub/storefront pages.
- Candidate-facing hygiene: zero `GAP-…`, `ASC-…`, "Simon Sir" or "Nair Sir" in
  the eight P0 files.

### `qb_content_index.json`

Validated **against live HTML**, not accepted because Desktop updated it. Method:
compare every indexed question's text and position against the live cards, on the
baseline and on the merge, then diff the two result sets.

- baseline 95 mismatches · after P0 95 mismatches · **0 new, 0 fixed**
- Inside the eight P0 files: one mismatch, `QB1_K` q8, **identical at baseline** —
  the index entry still carries `(Simon sir)` while the live card correctly says
  "the examiner". Pre-existing; recorded as fast-follow, not patched here.

---

## 6. Regeneration

Ran the Stream-A deterministic generator `tools/oral/build_examiner_index.py`,
which writes `EXAMINER_INDEX_SNAPSHOT.json`, `meoclass1/examiner-index.html`,
`SQ/examiner-index.html` and the SQ home card **from one snapshot in one pass**.

Snapshot diff, decoded as UTF-8 — decoding it with the Windows locale instead
manufactures 450 false "changes", which is a trap worth recording:

- **6 rows added**, one per new question, all tier `ce_tip`, evidence_count 1 —
  `Simon QB1_K#q9`, `John QB1_A#q31`, `Nair QB3_J#q6`, `Nair QB4_A#q21`,
  `Nair QB4_A#q22`, `Nair QB5_D#q3`.
- **0 rows removed** → no held Release-A pair was resurrected.
- **0 retiered** → Release-A adjudication was not reopened.
- **Exactly 2 display texts changed** — `QB5_B#q4` and `QB6#q10`, the two
  enrichments whose question text was widened. `QB7_I#q2` is correctly unchanged,
  because that enrichment added a limb without altering the question.

No `confirmed` relationship was invented for the new cards. The generator tiers
them `ce_tip` from the CE tip that names the examiner, so John remains
external-only with zero Confirmed rows and that gate still passes.

Totals moved 948 → 954 relationships, 682 → 688 canonical questions, 7 examiners
unchanged, 86 QB files unchanged.

### Storefront counts

`data-oral-questions` is not written by any generator — it is hand-entered
**behind a guard** that derives truth from the corpus, and that guard is the
governance. Updated 682 → 688 in the attribute, the visible stat, the meta
description and the four prose claims. The `682` inside the HTML comment was
deliberately left in place: the validator exempts comments because that comment
is the record of what drifted.

---

## 7. Validation

| Gate | Result |
|---|---|
| `validate_examiner_index.py` | **52 PASS / 0 FAIL** (Desktop branch was 47/5; main's baseline was 52/0) |
| `check_determinism.py` | **26 artefacts / 0 non-reproducible** across seeds 0, 1, 524287 |
| `test_oral_controls.py` | 315 controls / 0 failures |
| `test_notes_controls.py` | 106 notes controls / 0 failures |
| `validate_audit.py` | 12 pass / 1 fail — `index_tier_literals_valid`, 43 invalid literals. **Confirmed pre-existing by running the same tool on a clean `origin/main` worktree, which also reports 43.** The committed `VALIDATION_RESULTS.json` said "2", but that file was itself stale — it also carried a `mininav` failure that this regeneration cleared |
| Link and anchor validation | 0 broken fragments, 0 missing targets |
| CSR acronym trap | `QB1_K#q8` (IACS Common Structural Rules) and `QB5_C_B#q8` (Continuous Synopsis Record) still render as distinct questions |
| Auth | full index keeps its access gate and stays noindex; SQ teaser ungated and keeps its CTA; neither page links into the research tree |

`ORAL_NOTES_IMPACT.md` moved MISSING 45 → 42: the P0 answers closed three
notes-coverage gaps.

---

## 8. Fast-follow debt (deliberately not actioned)

1. Four `QB2_C` cards with answer scaffolding in q-text (Stream-A finding).
2. Ten held `STRONG_CE_TIP` pairs — authorization status unchanged by this work.
3. Reverse "Asked by" badges — not mass-added.
4. **New:** `qb_content_index.json` carries 95 stale entries against live HTML,
   one of which (`QB1_K` q8) leaks `(Simon sir)` into the hub search index in
   `meoclass1/index.html`. Pre-existing; the fix belongs at the generator, not in
   hand-patched generated data.
5. **New:** `validate_audit.py` `index_tier_literals_valid` — 43 invalid literals,
   pre-existing on `origin/main`.
6. **New:** the committed `VALIDATION_RESULTS.json` can go stale relative to the
   tool that writes it, so it must not be read as a baseline. Baselines should be
   taken by running the tool on a clean worktree.

No tenth P0 item was authored.
