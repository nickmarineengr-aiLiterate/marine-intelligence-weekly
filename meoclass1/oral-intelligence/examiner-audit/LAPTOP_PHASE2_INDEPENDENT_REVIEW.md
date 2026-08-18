# Laptop Independent Review — Oral 788-Question Reconciliation (Phase 2)

**Reviewer:** Laptop Claude (Opus 5) · 18 August 2026 · orals begin 24 August 2026
**Reviewed:** `research/oral-examiner-intelligence-v1-reconcile` @ `de6d3f2`
**Review branch:** `review/oral-examiner-intelligence-v1-phase2`
**Method:** cross-drive clean worktree on `C:` from a repo on `F:`; independent parsers written
from scratch for the live index and QB inventory; Desktop's own tooling used only to test
reproducibility, never to establish a count.

**VERDICT: HOLD — the reconciliation needs one bounded matching repair before its gap set can
drive production. The connection half is sound and a reduced Release A is authorised.**

---

## A–G. Repo truth, scope and input counts

| Item | Expected | Actual | |
|---|---|---|---|
| `origin/main` | `3b55bfb` | `3b55bfb5ac60875945490de97a9365d8dec74bbb` | OK |
| Phase 0/1 audit tip | `d8ed9e6` | `d8ed9e6f4424d8098a41b78a91e2f3a54d668a3c` | OK |
| Phase 2 reconcile tip | `de6d3f2` | `de6d3f2bd9e788d600495925972bcacb37cef647` | OK |

Main was clean at review start. Phase 2 is `main` + 1 audit commit + 4 reconcile commits, linear,
never merged. 60 files, +75,435 lines, confined to `meoclass1/oral-intelligence/examiner-audit/`,
`tools/oral/` and `.gitignore`.

Every headline input count reproduced **exactly** from the committed records:

| Claim | Reproduced | |
|---|---|---|
| 788 source occurrences | 788 | OK |
| John 129 / Simon 256 / Nair 300 / Paul 103 | identical | OK |
| 731 source families | 731 | OK |
| 26 cross-examiner families | 26 | OK |
| 681 live Oral QB questions | 681 | OK |
| 863 rendered index rows | 863 | OK |
| 862 unique relationships | 862 | OK |
| 863 evidence records | 863 | OK |
| 57 topics | 57 | OK (see note) |

**Topic note.** Distinct topic *labels* are 56, not 57; 57 is correct as the count of per-examiner
topic **sections** (9+18+22+8), because "UNCLOS" appears under both Nair and Paul. Not a defect,
but the generator must not render "57 topics" as if it were 57 distinct subjects.

**Dispositions reproduced exactly:** Exact 23 · Near 41 · Same-core 69 · Partial 364 · Missing 204 ·
Ambiguous 87. Mapping: NEW_LINK 336 · ALREADY_LINKED 161 · UNMAPPED 87 · NOT_APPLICABLE 204.
Unique new pairs 291, corroborated already-linked 127 — both reproduced.

**681 baseline is exactly complete.** I independently enumerated every `id="qN"` anchor across all
126 `meoclass1/*.html` files: 86 files, 681 anchors, **zero excluded, zero miscounted**, all gated,
all with answers. The QB side of the comparison is not under-scoped. This matters because it rules
out the most obvious cause of false MISSING — and forces the real cause (section I).

## D/F. Current-index recovery — independently confirmed

Written from scratch, not using `oral_lib`:

- 863 `q-row` elements; per-examiner 339/243/93/103/66/19 summing to 863
- **35 blank display-text rows** — confirmed
- **2 invalid `cetip` tier literals** — confirmed (no `filterTier()` toggle, so these vanish on first filter use)
- **1 duplicate relationship** — confirmed: `simon -> /meoclass1/QB5_C_A.html#q1`, correctly collapsed 863->862
- **12 `DISPLAY_TEXT_DRIFT`** rows preserved as variants, not scored as mismatches — confirmed
- Tiers: confirmed 406, ce_tip 45 (+2 `cetip`), header 87, inferred 323 -> repaired 406/47/87/322 — confirmed

**All 862 targets resolve.** I rebuilt the anchor set for every QB file and checked each
relationship: **0 missing files, 0 missing anchors.** Desktop did not claim this; it is true.

## H. Evidence circularity — conclusion stands

Reproduced independently by re-running step 1 cross-drive: the July per-examiner sheets overlap the
recovered relationships on **824 of 862 pairs (95.6%)**. They are a derived product surface and are
correctly excluded from tier strength. Counting them would inflate every "confirmed" number.

I also tested the converse claim. `PROSE_EVIDENCE_SUMMARY` reports 2 John in-card mentions, which
appears to contradict "John has zero MIW-native evidence". Both are false positives — "John
Ziegler" (Ziegler-Nichols) and "USS John S. McCain" — and both are correctly graded
`WEAK_INCIDENTAL_MENTION` and never promoted. **The handoff's claim is correct and the strength
grader works.**

## I. Matcher implementation — four claimed repairs, all real

Read in source, not accepted from the report:

1. **Topic-tag pollution — FIXED.** `tag_tok` is computed but appears in exactly one place
   (`reconcile_788.py:268`) where it sets the recorded field `matched_on_topic_tag`. It never
   enters `classify()` or any coverage computation. Verified by grep: 4 references, none scoring.
2. **Corpus-wide over-rescue — FIXED, and structurally.** `classify()` reaches `SAME_CORE` only via
   `qcov` and `target_acov` (the *matched* question's own answer). `best_acov` can produce
   `PARTIAL` and nothing stronger. A broad answer elsewhere therefore **cannot** manufacture a
   "covered" verdict. This is the section 9 requirement and it is met by construction, not by tuning.
3. **Designator handling — PARTIALLY fixed.** See section Q; three real classes still fail.
4. **Ties are not ambiguity — FIXED.** `cov >= 0.9` with a near-equal runner-up records
   `alternative_target_question_id`; only `0.5 <= cov < 0.9` becomes ambiguous. Reproduced.

### The defect Desktop did not find: the coverage universe excludes the Notes product

`prose_evidence.py` and `reconcile_788.py` both iterate `oral_lib.qb_files()` — the 681 QB
questions only. **`meoclass1/oralnotes/` (43 pages, 4.9 MB) is outside both the coverage universe
and the evidence universe.** It is part of the same purchased entitlement (`ORAL_QB_NOTES`), and it
is organised *by examiner*.

Consequences, verified by reading the content:

- **GAP-0002 "GIRDING"** — Desktop's leading P0, 3 Simon occurrences, "MIW holds almost no material
  on this ask". `oralnotes/simon-notes-p2.html` carries note **P.31 "Tug Girding — Capsizing
  Risk"**: definition, the four influencing factors, SOLAS V/34 and ISM cl. 7 references, and the
  explicit cue *"Simon Sir typically asks 'What is tug girding?'"*. **NOT_A_GAP.**
- **GAP-0494 "HKG initial survey / parts in IHM cert"** — "best existing answer covers 0%".
  `oralnotes/WA1-HKC1.html` contains "The IHM Framework — Three-Part Engineering Logbook" setting
  out Parts I, II and III with contents, plus Appendix 1/2 materials. **NOT_A_GAP.**
- **12 of the 15 P0 gaps** have material in the Notes.
- Sampled MISSING rows scored `best_answer_coverage = 0.00` for asks MIW covers in both products:
  CLC 69 vs 92 (a dedicated Notes topic), NOx compliance / NOx Technical File, casualty
  investigation (21 QB files, 13 Notes pages), DMLC Parts I/II, incineration.

There is a second consequence the audit's own framing missed. Phase 1 concluded that
`examiner-index.html` is the only place tying an examiner to a *question*. I swept for
examiner-attribution cues across the product and found **468 outside the index — 279 in QB cards
and 189 in the Notes** (Simon 162, Nair 17, Senthil 4, Rajappan 3, Paul 2, Srivastava 1). The QB
ones are harvested by `prose_evidence.py`; **the 189 in the Notes are not harvested at all.**

## J. Stratified sample — 75 adjudicated

Deterministic stratified sample, spread across all four examiners and many topics.

| Class | Sampled | Agree | Disagree | Agreement |
|---|---|---|---|---|
| EXACT | 10 | 10 | 0 | **100%** |
| NEAR | 15 | 13 | 2 | **87%** |
| SAME_CORE | 20 | 12 | 8 | **60%** |
| MISSING | 30 | ~15 | ~15 | **~50%** |
| **Total** | **75** | | | |

AMBIGUOUS was reviewed as the full 87-item queue rather than a sample (sections R and S).

### K. EXACT — 10/10 correct
General/Particular Average, Hague-Visby, Condition of Class, MIS, RO Code, FSS+FTP, Cabotage, Fund
Convention, MS Act welfare. High precision; the `sim >= 0.55` floor is doing its job.
**Release-ready.**

### L. NEAR — 13/15 correct
Two failures, both instructive:
- **ASC-0107 "UNCLOS FS duties"** (Flag State) matched to `QB9_D#q10` **Coastal state duties**. The
  correct target, `QB1_A#q22` (Port/Coastal/Flag State duties), exists in the corpus. Right class,
  **wrong target** — this would publish a wrong connection.
- **ASC-0090 "Bill of lading"** matched to `QB8_B#q3` **Smart/E-Bill of Lading**. A candidate who
  studied e-B/L cannot answer "what is a B/L and its three functions". Should be PARTIAL.

### M. SAME_CORE — 12/20 correct. This is the weak class.
`classify()` applies a similarity floor to EXACT (`sim >= 0.55`) and NEAR (`sim >= 0.30`) but
**imposes none on SAME_CORE**. 52% of the 69 SAME_CORE rows sit below `sim 0.25`; 34 of those also
have reverse-coverage below 0.35. Median SAME_CORE similarity is 0.22 against 0.67 for EXACT.

Confirmed false matches:

| Source ask | Matched to | sim | Why wrong |
|---|---|---|---|
| Shipping master duties | **VGM** — verified gross mass | 0.15 | Unrelated. Notes cover "ROFR & Duties of a Shipping Master" |
| LSA Code — latest amendment | **Polar Code** — latest amendment | 0.12 | Matched on "latest amendment" boilerplate; wrong instrument |
| GA PA YA rule | **Act vs rule** (Indian legal) | 0.12 | Matched on "rule". Correct target `QB9_G#q7` exists |
| Intl Convention on **Registration** of Ships | **Fraudulent** Registration | 0.40 | Different instrument |
| LLMC — what does it apply to | HNS Convention (mentions LLMC) | 0.13 | Answer-side rescue; PARTIAL at best |
| How to check **CII compliance onboard** | **Shore power** and its CII effect | 0.17 | Wrong limb |
| MLC (bare) | "Who is the **assessor** in MLC/STCW" | 0.25 | Narrow sliver of a broad ask |
| MRCC (bare) | Major-accident contact procedure | 0.09 | PARTIAL |

### N. PARTIAL — direction is safe
PARTIAL is the conservative sink: `best_acov >= 0.7` lands here and never higher. Under-crediting a
covered question as PARTIAL costs an enrichment task; it never misleads a candidate. No change
recommended beyond what the Notes fix will move out of it.

### O. MISSING — materially over-reported (~50% of sample)
Direction is *over-reporting gaps*, which is not candidate-dangerous but is production-dangerous:
it would have Desktop author answers MIW already holds. Root cause is the Notes exclusion
(section I) plus the designator and spell-repair defects (section Q).

Genuinely missing in the sample and confirmed absent from both products: PEMS, the flammability-
diagram slope, and the QF term in the static-stability criterion.

## Q. Designator tests — three real failures

| Designator | Result | |
|---|---|---|
| A-60 / A60 | `a60` both ways | PASS |
| D-1 / D-2 | `d1` / `d2` distinct | PASS |
| G8 / G9 | distinct | PASS |
| III/1 vs III/2 | `iii1` / `iii2` distinct | PASS |
| ISO 8217, Reg 13, II-1, Tier II/III | preserved | PASS |
| **ME-GI / ME-GA / ME-LGI** | **both tokenise to empty** | **FAIL** |
| **Annex VI vs Annex 6** | `vi` vs `6` — never unified | **FAIL** |
| **Annex I** | `i` dropped as a stopword -> bare `annex` | **FAIL** |
| **IOPP Form A vs Form B** | both -> `form` | **FAIL** |

- `_DESIGNATOR` requires digits, so letter-suffix designators die: `ME-GI` -> `me` + `gi`, both under
  the length floor. **All 4 ME-GI/ME-GA occurrences scored MISSING at coverage 0.00**, and MIW's own
  ME-GI text is equally invisible, so no match was ever possible. GAP-0409 (ME-GA) rests on this.
- `_ROMAN` is defined but used only as a *keep-list* — it never maps roman to arabic. The handoff
  lists "Annex 6" as fixed; it is not. The source is candidate-typed ("Annex 6"), MIW writes
  "Annex VI".
- Annex I is indistinguishable from a bare "Annex" — a live confusion risk across Annexes I/IV/V/VI.
- Form A vs Form B is a classic examiner discriminator and is invisible.

Incidence across the 788: ~24 occurrences, concentrated in MISSING/PARTIAL/AMBIGUOUS — that is,
precisely in the set that drives P0 production. Small in percentage, decisive in effect.

### Spell repairer corrupts correct words and designators
`repair()` fires on any token of 5+ characters absent from the **QB** vocabulary — which, after the
Notes exclusion, is a narrow dictionary. 72 applications across 65 records. Genuine fixes exist
(`johri->johari`, `ammendment->amendment`, `deligation->delegation`), but so do these:

- `attended -> unattended` (x2) — **semantic inversion**, fatal around UMS
- `convinced -> convicted`, `biased -> based` (x2), `provident -> provide` (x2, breaks Provident Fund)
- `conciliation -> reconciliation`, `interesting -> intersecting`, `appealing -> appearing`
- **`and92 -> and9`** (destroys the CLC 1992 Protocol reference), **`stcw5 -> stcw15`**,
  **`iii16 -> iii6`** — the repairer damages the very designators the tokeniser was fixed to protect

## R. Terse prompts — 25 adjudicated

| Verdict | Count |
|---|---|
| **A — canonical match obvious, resolve** | 10 |
| **B — retarget to a different existing question** | 1 |
| **C — still ambiguous or a genuine gap** | 14 |

Resolve (A): TBT, GISIS x2, CIC (MOU), FSI, mutual/non-mutual P&I, subdivision stability,
grievance redressal, latest technologies, laytime (partial — laycan uncovered).

Retarget (B): "GT and formula, unit" is matched to **Free Surface Effect** formula; the correct
target `QB2_B#q12` (GT/NT calculation) is in the corpus.

The remaining 14 carry plainly wrong candidates driven by homonym collisions — **VDR "location"**
-> lifeboat *location*; **uptake fire** -> shore-power *uptake*; **note of protest** -> ship-breaking
*credit note*; **controlled document** -> Grain Code *Document of Authorisation*; **BWMS D1/D2
status** -> *MLC 2006 titles*; **SOLAS chapters** and **STCW chapters** -> *IBC Code* chapters.

**The quarantine is working** — Desktop was right to route these to human review rather than
publish them. But the same mechanism produces confidently wrong targets on rows that were *not*
quarantined, which is what section M measured. The guard fires only when `len(stoks) <= 2` and
`0.5 <= cov < 0.95`; a three-token prompt or a full-coverage match escapes it.

## S. Two-target queue — 62 items
Correctly separated from the terse set and correctly withheld. Given that SAME_CORE (the adjacent
class) runs at 60% precision, I do **not** recommend bulk-resolving these before the repair; they
should be re-derived once the coverage universe includes the Notes, at which point many will resolve
against a Notes target rather than either QB candidate.

## T/U. New connections and Release A

370 ready connections: `READY_VERIFIED_MULTI_SOURCE` 46 · `READY_VERIFIED` 38 ·
`READY_BUT_CE_TIP_ONLY` 81 · `NEEDS_REVIEW_WEAK_PROSE` 205.

Desktop's proposed Release A = 84 Phase-1 ready + 78 new = **162**. I decomposed the 78:

| Component | Count | Sampled precision | Verdict |
|---|---|---|---|
| Phase-1 ready (46 multi-source + 38 tracker-verified) | 84 | primary/tracker evidence | **RELEASE_READY_STRONG** |
| New pairs, EXACT + NEAR | **41** | ~95% | **RELEASE_READY_STRONG** |
| New pairs, SAME_CORE | **37** | ~60% | **HOLD_AMBIGUOUS** |

**Authorised Release A = 125 pairs, not 162.** The 37 SAME_CORE-dependent pairs are held: at 60%
precision roughly 15 of them are wrong, and a wrong examiner connection on a candidate page six days
before an oral is the one failure mode this project exists to prevent.

`READY_BUT_CE_TIP_ONLY` (81): admissible under the Founder's threshold D only where the page
declaration is unambiguous. These are page-declared, not tracker-confirmed, and must render as
**CE tip**, never as Confirmed. I have not cleared them individually; keep them out of the first
release.

**REJECT_WRONG_MATCH:** none of the 84 Phase-1 ready connections; the rejects are inside the 37
held SAME_CORE pairs and should be re-derived rather than hand-pruned.

### Blocking presentation defect for Release A
Eight live questions carry internal production vocabulary in their **display text** — all in
`QB5_C_B`: *"Q12: Simon — SWOT analysis"*, *"Q11: Rajappan — Mentoring vs reverse mentoring"*,
*"Q14: Nair — Ear muff selection criteria"*, and five more. One is already a Release-A target, and
source ASC-0444 connects **Nair** to `QB5_C_B#q2`, which would render a Nair row reading
*"Q12: **Simon** — SWOT analysis"*. The generator spec says display text comes from the live
question, so it would reproduce this verbatim. Must be fixed at the QB source before Release A
renders.

## V. John — PUBLISH, in Release A, as Reported

129 occurrences, 9 topic sections, 77 proposed new pairs, zero already-linked, zero MIW-native
evidence. I confirmed the two apparent QB mentions are false positives (section H), so
external-only is the true state — as Laptop Phase 1 already established, and old-tracker evidence is
correctly not required.

John's asks are substantively well-formed and match the corpus cleanly (Fund Convention, GA/PA,
RO Code, tacit/explicit acceptance, UNCLOS, Hague-Visby all sampled correct). **Authorise a John
section** provided every John row renders at the **Reported** tier (`EXTERNAL_SOURCE_CONFIRMED`)
with the compilation named as its basis, and provided only his EXACT/NEAR pairs ship in Release A.
John carries 3 of the 15 P0 gaps; those wait for the repair.

## W. Paul — confirmed: a connection problem, not a content gap

103 occurrences against 19 published pairs. Reproduced: 24 already answered, 55 partial, 13
missing, 66 new pairs against 3 already-linked, **zero P0**. I tested for over-rescue specifically
and the mechanism that would cause it is structurally absent (section I, item 2). Sampled Paul rows
were correct (Condition of Class, FSS+FTP, Innocent Passage, anniversary date, coastal/port state
duties). Paul's live section shows **19** rows against a sales page still advertising "All 10
Questions". **Paul is the highest-value, lowest-risk expansion in Release A.**

## X/Y. Simon and Nair
Large existing coverage; both reproduce correctly. Their weakness is concentrated in the SAME_CORE
boundary (section M) — the four worst false matches I found are Simon and Nair rows. The 12
`DISPLAY_TEXT_DRIFT` rows and the 35 blanks are theirs to inherit, and the generator fixes both by
sourcing display text live. Simon additionally owns 162 of the 189 unharvested Notes examiner cues,
so his connection count is understated by a margin nobody has yet measured.

## Z. Adjusted global counts

Confirmed as computed: all six disposition totals reproduce exactly. **But the classifier's own
inputs are wrong**, so the true distribution is not the reported one:

| Class | Desktop | Estimated error | Direction |
|---|---|---|---|
| EXACT 23 | confirmed | ~0% | — |
| NEAR 41 | confirmed | ~13% | mostly right target, occasional wrong |
| SAME_CORE 69 | confirmed | **~40%** | over-classified from PARTIAL |
| PARTIAL 364 | confirmed | low | conservative, safe |
| MISSING 204 | confirmed | **~50%** | **over-reported** — Notes + designators |
| AMBIGUOUS 87 | confirmed | correctly quarantined | — |

Because a large fraction of rows would move, **section 19's own instruction applies: HOLD.**

## AA/AB. Gap families — dedup is mostly sound, one confirmed split
196 gap families / 115 material-partial reproduce. Family dedup is generally correct, but
**GAP-0410 and GAP-0454 are the same ask** — both Nair, both "how do you know onboard that
discharge meets the D-2 standard", one phrased via UV type-approval and one via BWTS. They should
be one family. This also means the P0 count is inflated by at least one before the Notes fix.

## AC. P0 — all 15 adjudicated

| Gap | Verdict | Basis |
|---|---|---|
| GAP-0002 GIRDING | **NOT_A_GAP** | Notes P.31 answers it, cued to Simon |
| GAP-0494 HKC / IHM parts | **NOT_A_GAP** | `WA1-HKC1` gives IHM Parts I/II/III |
| GAP-0016 G8/G9 convention status | **P0_ENRICH_EXISTING** | best answer 83%; reuse `QB1_supplementary#q20` |
| GAP-0023 OPRC free service / parties | **P0_ENRICH_EXISTING** | best answer 70%; `QB9_B#q1` |
| GAP-0043 assertiveness / empathy | **P0_ENRICH_EXISTING** | best answer 67%; `QB5_B#q4`; "empathy" in Notes |
| GAP-0034 dual-fuel / trifuel | **P0_ENRICH_EXISTING** | 52%; dual-fuel in 3 Notes pages |
| GAP-0410 BWTS / UV / D-2 | **P0_ENRICH_EXISTING** | merge with GAP-0454; D-2 in 4 Notes pages |
| GAP-0454 UV / D-2 verification | **MERGE into GAP-0410** | duplicate family |
| GAP-0404 PSC/USCG selection + appeal | **P0_ENRICH_EXISTING** | 42%; USCG in 4 Notes pages |
| GAP-0048 IACS members / RO India / IRS | **P0_NEW_ANSWER** | 47%; factual limbs genuinely absent |
| GAP-0042 bullying / harassment / SMS | **P0_NEW_ANSWER** | current amendments; thin coverage; note the source token was corrupted `biased->based` |
| GAP-0044 STCW 2E->CE course set | **P0_NEW_ANSWER** | absent from QB and Notes |
| GAP-0409 ME-GA working principle | **P0_NEW_ANSWER** | genuinely absent — but re-derive; the 0.00 score is a tokeniser artefact, not evidence |
| GAP-0093 medical certificate change | **DEMOTE_P1** | single occurrence; "medical certificate" in 2 Notes pages |
| GAP-0069 TIO2 APPLICATION | **DEMOTE_P1** | two-word terse prompt, one occurrence; belongs in the ambiguous queue, not P0 |

**AD. Authorised P0 new answers: 4** — GAP-0048, GAP-0042, GAP-0044, GAP-0409.

**AE. Authorised P0 enrichments: 6** — GAP-0016, GAP-0023, GAP-0043, GAP-0034, GAP-0410 (merged
with GAP-0454), GAP-0404.

**Not authorised: 2 NOT_A_GAP, 2 demoted to P1, 1 merged.**

None of this should be built until the reconciliation is re-run against a Notes-inclusive corpus,
because the same defect that produced two NOT_A_GAPs may promote other families into P0.

## AF. Follow-up model — sound, defer
178 follow-up / expected-detail records; `relationship_type` is derived from source-comment phrasing
("he wanted", "not satisfied", "cross question") and is well-founded. Release C (about 158
enrichments) is genuinely useful but is **not** pre-24-August work. Defer.

## AG. Re-tiering — HOLD

197 of 862 pairs would change tier. The rules themselves are honest: July sheets never raise a
tier, `CURRENT_INDEX_RECOVERY` is explicitly annotated *"Not independent evidence"*, and `CE_TIP`
never renders Confirmed.

I withhold authorisation for one reason: **mutation M5 escaped.** Relabelling a
`CURRENT_INDEX_RECOVERY` evidence record as `PRIMARY_TRACKER` passes validation at **35 PASS / 0
FAIL**. The validator has no guard on the one axis re-tiering depends on. Add that guard, then
re-tier. **HOLD RETIERING UNTIL GENERATOR REVIEW.**

## AH. Inference-only pairs — logic accepted
41 promoted by external evidence, 268 remain inferred, 0 conflicted. The reasoning is right:
silence in the 788 is not contradiction, and the compilation covers only 4 of the 6 indexed
examiners — Rajappan, Srivastava and Senthil appear nowhere in it, so their pairs *cannot* be
corroborated or refuted by it. Do not delete inference-only pairs. Do render them as **Topic
inference**, never as Confirmed.

## AI. Raw source wording on a public repo — recommendation B, and one thing to fix now

The `.gitignore` addition (`*.docx`, `*.doc`, `*.pdf` under `docs/MIW-master-Question-bank/`) is
correct and the binary is not committed. But the research tree was placed at
**`meoclass1/oral-intelligence/examiner-audit/`** — inside the published web root, not under
`docs/`.

- **Live site: gated.** `middleware.js` matches `/meoclass1/:path*` and `routes.js` requires
  `ORAL_QB_NOTES` for the `/meoclass1/` prefix, with no extension exemption and fail-closed
  branches. Verified.
- **`.vercelignore`: not excluded.** It excludes `meoclass1/pastpapers/`, `known_traps.md` and
  `qb_health_check.py` but has no entry for `meoclass1/oral-intelligence/`. So about 75,000 lines of
  research data — including `CURRENT_ORAL_QB_INVENTORY.json`, a machine-readable dump of all 681
  paid questions — **deploys as URLs**, gated but served. That contradicts the file's own stated
  data-minimisation purpose.
- **GitHub: public.** The repository is public, so the 788 raw candidate-typed surveyor questions,
  the full QB inventory and all internal production vocabulary are readable by anyone today,
  entitlement or not.

**Recommendation B.** Keep the derived research data (families, reconciliation, IDs, hashes) but
move the tree out of the web root to `docs/MIW-master-QB/examiner-audit/`, add a `.vercelignore`
entry, and hold the verbatim `raw_question_text` locally rather than committed. Nothing was deleted
during this review. This is a Founder decision, not a unilateral one.

## AJ. Generator spec — APPROVED with one addition
`EXAMINER_INDEX_V2_GENERATOR_SPEC.md` meets every requirement in section 27: all counts are `len()`
of rendered records with no hand-entered literals; live HTML re-parsed each run;
`qb_content_index.json` correctly excluded for its off-by-one shift; an unresolvable relationship is
a build failure; every emitted tier literal must have a `filterTier()` toggle (which is exactly what
the 2 `cetip` rows needed); display text sourced live, fixing both the 35 blanks and the 12 drifts;
one data pass emits both `meoclass1/examiner-index.html` and `SQ/examiner-index.html`.

**Required addition:** a build gate rejecting display text matching `^Q\d+:\s*(examiner name)` — the
eight `QB5_C_B` questions would otherwise render production vocabulary, including an examiner name
contradicting the row's own examiner.

**AK. SQ same-pass: CONFIRMED.** Do not patch `SQ/examiner-index.html` independently. Its "791+",
"Simon 212", "Paul Sir — All 10 Questions" and "62+ QB Files" (live: 86) are all stale; correcting
them now would produce a second stale number within a week.

## AL. Validator and mutations — 8 of 9 caught

Baseline reproduced cross-drive: **35 PASS / 0 FAIL, exit 0.**

| Mutation | Result |
|---|---|
| wrong question anchor | 2 FAIL — caught |
| duplicate relation | 1 FAIL — caught |
| orphan evidence | 1 FAIL — caught |
| unknown examiner alias | 1 FAIL — caught |
| **derived sibling promoted to strong evidence** | **35 PASS / 0 FAIL — ESCAPED** |
| source occurrence silently dropped | 2 FAIL — caught |
| two dispositions assigned | crash, exit 1 — caught (fails closed, ungracefully) |
| missing disposition | crash, exit 1 — caught (same) |
| invalid tier | 1 FAIL — caught |

## AM/AN. Clean worktree and portability — PASS
Run entirely from a fresh worktree on **`C:`** against a repository on **`F:`** — a genuine
cross-drive portability test. No hardcoded drive letters in `tools/oral/` (the only `D:`-shaped grep
hit is the constant `T_VERIFIED`). No untracked source required: `recover_relationships.py`,
`reconcile_788.py` and `report_phase2.py` all re-ran to completion **with no DOCX present**, from
committed records alone. `PYTHONIOENCODING=utf-8` remains mandatory on Windows.

**One reproducibility defect.** Re-running `reconcile_788.py` changes 5 records: the
`source_spelling_repairs` list is emitted in set-iteration order, so it varies across runs under
string hash randomisation. No disposition, target or coverage changes — counts are identical
(291/127, 25/62, 15 P0, 26 cross-examiner). Sort the list to restore byte-reproducibility.

## AO/AP/AQ. Product safety, files and remote
**No live product file was edited by Phase 2 or by this review.** `meoclass1/examiner-index.html` is
byte-identical to `main`; QB HTML, `SQ/`, oralnotes, payments, homepage, Written QI and magazine are
untouched. This review adds exactly one file, this report. Review branch pushed and verified with
`git ls-remote`.

## AR. Founder decisions (5)

1. **Ship Release A at 125 pairs, not 162?** (drops the 37 SAME_CORE-dependent new pairs)
2. **Publish a John section at the "Reported" tier**, external-compilation-only, EXACT/NEAR only?
3. **Fold `meoclass1/oralnotes/` into the coverage and evidence universe** before any gap
   production — this is the bounded repair.
4. **Move the research tree out of the web root** (recommendation B) and add the `.vercelignore`
   entry?
5. **Fix the 8 `QB5_C_B` display texts** that leak production vocabulary, before the index renders?

## AS/AT/AU. Authorisations

- **RELEASE A: YES — reduced to 125 pairs**, conditional on the generator existing (no
  hand-patching) and on decision 5.
- **P0 PRODUCTION: NO** — re-derive the gap set first. Of 15 P0 items, 2 are not gaps, 2 demote,
  1 merges, 6 are enrichments and only 4 are new answers.
- **NEXT ACTION: one bounded reconciliation repair**, then re-run and re-review the gap set only.

### The bounded repair
1. Add `meoclass1/oralnotes/` to `oral_lib` corpus building, for both coverage and prose evidence.
2. Add a similarity or reverse-coverage floor to `SAME_CORE_ASK` (EXACT and NEAR already have one).
3. Extend `_DESIGNATOR` to letter-suffix designators (`ME-GI`, `ME-GA`, `ME-LGI`), apply `_ROMAN` as
   a mapping rather than a keep-list, protect `Annex I` from the stopword list, and keep
   single-letter form discriminators.
4. Restrict `repair()` to purely alphabetic tokens and skip any token containing a digit.
5. Sort `source_spelling_repairs`.
6. Add a validator check that no `CURRENT_INDEX_RECOVERY` or July-derived record can carry a primary
   evidence tier.

Connections do not depend on the gap set, so Release A and the repair can proceed in parallel.

## AV. VERDICT

**HOLD — ORAL 788 RECONCILIATION NEEDS ONE BOUNDED MATCHING/ADJUDICATION REPAIR**

The recovery half is excellent and is now independently verified: 863 rows, 862 relationships, all
targets resolving, the duplicate, the 35 blanks, the 2 `cetip` literals and the circularity
conclusion all reproduce from scratch. The fragility Phase 1 identified is genuinely closed.

The matching half is not ready to drive production. It compares a 788-question examiner corpus
against 681 QB questions while ignoring 4.9 MB of examiner-organised Notes sitting in the same
product — which is how the leading P0 gap turned out to be a Notes page that names the examiner who
asks it.

Ship the connections we can defend. Re-derive the gaps.
