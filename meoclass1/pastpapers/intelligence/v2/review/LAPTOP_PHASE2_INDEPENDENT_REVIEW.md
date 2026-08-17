# Question Intelligence V2 — Phase 2 independent review (Laptop)

**Reviewer:** Laptop (integration authority) · `current_as_of: 2026-08-18`
**Status of this document:** review finding. Nothing here is candidate-facing.
**Verdict:** `GO — QUESTION INTELLIGENCE V2 PHASE 2 INDEPENDENTLY VERIFIED`
(with six defects to fix, none load-bearing on the architecture).

Desktop's report was treated as evidence, not truth. Every headline number was
recomputed from source on this machine, on this network, with independently written
tooling wherever a shared tool would have shared a failure mode.

---

## A. Repo truth

| | Actual | Brief said |
|---|---|---|
| `origin/main` | `3b55bfb` | `6562bae` — **stale by 2 commits** |
| Phase 1 | `73305a0` | `73305a0` ✓ |
| Phase 2 | `72aab17` | `72aab17` ✓ |

`6562bae` is the merge-base of Phase 2 and is an ancestor of main; main has since
advanced by `bca4153` and `3b55bfb`, both documentation. Working tree was clean at
session start and is clean now.

**Phase 1 is NOT an ancestor of Phase 2.** The two research branches are siblings
off `6562bae`, not a chain. Phase 2 re-creates all 17 Phase-1 files and adds 12.
Nothing is lost, but the branches must not be merged in sequence expecting a
fast-forward.

Phase 2 commits (9): `159aeb1 · e2e30d2 · f8f6837 · 70eaec8 · a3b958c · 1857e63 ·
166865a · 3da631c · 72aab17`.

## B. Phase-2 diff safety — PASS

29 files, **4,622 insertions, zero deletions, zero modifications**. Every path is
under `meoclass1/pastpapers/intelligence/v2/`. No `solvedQP`, no QP spec, no
commercial, entitlement, payment, homepage or magazine file is touched. Scope
invariant (§44) holds. No contamination.

## C. DG Shipping question bank — AUTHENTIC, independently reproduced

**Classification: `OFFICIAL_ORIGIN_HIGH_CONFIDENCE`** (Desktop's
`OFFICIAL_SOURCE_VIA_ARCHIVE` tier is accepted and is the right name for it).

I re-downloaded the artefact myself from the Wayback raw `id_` route:

| Property | Desktop | Laptop, independently | |
|---|---|---|---|
| Bytes | 314,710 | **314,710** | ✓ |
| sha256 | `0E0D…CB51` | **`0e0d6bc7a7b738335687b57d6f33364d728d2dad99bc22ed0e2a5d371438cb51`** | ✓ exact |
| Header | `%PDF-1.7` | `%PDF-1.7` | ✓ |

The hash proves *artefact integrity* — Desktop hashed the real PDF, not a Wayback
HTML wrapper. The `id_`-route caveat is real and reproduced: the plain snapshot URL
returns the toolbar wrapper.

**Origin attestation** (this, not the hash, is what proves authorship). The Wayback
response replays the origin server's own headers:

- `link: rel="original"` → `https://dgshipping.gov.in/WriteReadData/ExamResult/…`
  — the archive attests the object was crawled from the Directorate's host.
- `x-archive-orig-last-modified: Mon, 12 Feb 2018 10:15:00 GMT` — the origin
  server's own timestamp.
- `x-archive-orig-etag: "02aee56eaa3d31:0"` — IIS ETag form, consistent with a
  `gov.in` ASP.NET estate.

**Internal marks.** PDF `creationDate D:20180212100342`, producer
`Microsoft Excel 2016`. Three independent date signals agree on 12 February 2018:
the DGS filename prefix `20180212`, the origin `Last-Modified`, and the PDF's own
creation stamp. The Excel origin also explains the document's two-column
`Sr.No | Questions` shape.

Internet Archive hosting alone would not be authorship. Origin-header attestation
plus three concordant internal dates is. **Authenticity accepted.**

## D. Extraction — 185/185 CONFIRMED, one parser defect found

I did not re-run Desktop's parser as the primary check. I wrote an independent
extractor using **real table-cell recovery** (PyMuPDF `find_tables`), which shares
no failure mode with Desktop's line-geometry approach.

- 186 rows: 1 header + **185 numbered rows, 1–185, no gaps, no duplicates.**
- **183 of 185 items byte-identical** between the two independent extractors.

This matters because Desktop's own evidence for 185/185 — *"verified by contiguous
numbering with no gaps"* — is **self-fulfilling**: the parser's post-split loop
explicitly splits text to fill numbering gaps, so it optimises for the very metric
offered as proof. The claim is nonetheless **true**; it just needed independent
confirmation, which it now has.

**All 7 cited ancestors verified verbatim-exact** (BANK-015, 018, 054, 072, 085,
105, 135) against my extraction. The load-bearing text is sound.

**DEFECT L-1 (parser, low impact).** Item **182** is scrambled by Desktop's parser:
the `(i)/(ii)/(iii)` charter list is interleaved out of reading order
(*"Differentiate the (iii) Time charter. As a Chief Engineer on board explain (ii)
Voyage charter salient features…"*). Positional ground truth confirms the correct
text. Not a cited ancestor, but it proves the geometry parser can break reading
order inside a wrapped cell. Item 181's odd `a. b. d. c.` order is a **genuine DGS
typo**, correctly preserved by both extractors — not a defect.

**DEFECT L-2 (documentation).** `OFFICIAL_QUESTION_BANK.md` and
`OFFICIAL_BANK_ITEMS.json` both state the inline `(Oct-05)` annotation is on
**`BANK-4`**. It is on **item 3**. Both extractors agree, including Desktop's own.
This is a prose error, not an extraction error — but it is the *single dated
annotation in the entire bank*, so it is the worst place in the document to be
wrong by one.

## E. Source storage recommendation

**Recommendation: B — a dedicated historical-QP source archive, mirrored with
manifest (a governed blend of B and C).**

Governing facts:
1. The MIW GitHub repo is **PUBLIC**. The standing rule is *never commit source
   PDFs*.
2. The artefact is **not on the Laptop**. `raw_file_path` points to
   `D:\MIW-Historical-QP-Intake\…` and **there is no D: drive on this machine** —
   only C, F, G, H, I. So the file is genuinely single-copy on one machine.
3. It is now load-bearing for the entire recurrence layer.

Do **not** commit the PDF to the public repo, and do not place it under MIW True
Source (that store is a *canonical-law* corpus; an exam question bank is not law).
Instead: keep the binary in the git-ignored historical-QP intake store, mirror it to
a second physical location, and commit **only** the manifest entry — which already
carries URL, snapshot id, sha256 and byte count, and is sufficient to re-obtain and
re-verify the file, as this review just demonstrated end-to-end.

**Required fix:** the manifest must record a machine-independent retrieval recipe
rather than a `D:\` path. The `D:\` path is not resolvable by the integration
authority, which is precisely the machine that must be able to verify it.

## F. 2005 dated paper

Provenance route is the same archive mechanism and is sound. Desktop's own grading
is correct and commendably careful: **year 2005 HIGH** (printed on the paper),
**month February MEDIUM** (rests on the DGS filename token `0205` and an OLE
creation stamp, neither printed). Value: **primarily proof that the archival route
yields dated official papers** — which the CDX evidence below confirms at scale.
It is outside the 2010–2012 window and must not be used to colour it.

## G. 2010–2012 coverage — Desktop's honesty gate PASSES

`RECURRENCE_METADATA_ONLY`, zero readable papers. Verified structurally, not just
by reading the claim: **no occurrence record in `QUESTION_OCCURRENCES.jsonl` bears a
2010, 2011 or 2012 date.** The alleged sittings survive only as
`unverified_asserted_occurrences` blocks with
`status: UNVERIFIABLE_FROM_REPOSITORY`. The bank is **not** counted as 2010–2012
coverage anywhere. This gate is clean.

**DEFECT L-3 (naming hazard).** The five verification files are still named
`H1_QP2608_Q1_JUN2010.md`, `H2_…_DEC2011.md`, `H3_…_OCT2012.md`,
`H4_…_APR2010.md`, `H5_…_MAR2010.md`. The filenames assert dates the model
explicitly refuses to assert. Contents are correct; the names are Phase-1 residue
and should be de-dated before anything is indexed or published from them.

## H. H1–H5 — independent adjudication

I recomputed containment from source rather than accepting Desktop's figures. **All
five reproduce exactly.**

| | Question | Recurrence | Date | Source | Similarity class | Scope |
|---|---|---|---|---|---|---|
| **H1** | `QP2608-Q1(a)` lay-up | HIGH — BANK-015 **1.00/1.00** | **NONE** | HIGH | `EXACT_REPEAT` | **limb (a) only, 10 of 16** |
| **H2/H3** | `QP2608-Q2` dry dock | HIGH — BANK-018 **1.00/1.00** | **NONE** | HIGH | `EXACT_REPEAT` | **whole question, 16** |
| **H4** | `QP2608-Q4` insurance | HIGH — BANK-072 **0.93/1.00** | **NONE** | HIGH | `NEAR_VERBATIM` | **whole question, 16** |
| **H5** | `QP2608-Q8(b)` motivation | HIGH — BANK-054 **1.00/1.00** | **HIGH** (MIW sittings) | HIGH | `EXACT_REPEAT` | **limb (b), 6 of 16** |
| — | `QP2608-Q8(a)` comms | MEDIUM — BANK-105 **0.48/0.96** | NONE | HIGH | `SAME_CORE_ASK` | limb (a), 10 of 16 |

**H1 (§9).** BANK-015 is a whole-question ancestor of **limb (a) only**. The whole
`Q1` scores 0.72/1.00 — absorbed and extended, because limb (b) (laid-up notation
vs survey cycles, 6 marks) has no ancestor. Desktop does not over-promote it.
Correct.

**H2/H3 (§10).** Verified directly against the bank text: BANK-018 does carry all
three demands — Master coordination, preparations *and* delegation to engineers,
and undocking inspections/co-operation. Phase 1's "only one third has an ancestor"
was an artefact of the Scribd excerpt carrying the first sentence alone.
`EXACT_REPEAT` for all three components is justified. This is the largest and
best-evidenced correction in Phase 2.

**H4 (§11).** This was the sharpest test, because Phase 1 said SOURCE NOT FOUND and
topic overlap could masquerade as recurrence. It does not here: BANK-072 is not a
list of the same four terms, it is **the same examiner task** —
*"As per the Marine Insurance Act, write short notes on the following: (a) Deviation
(b) Warranties (c) War Risk Clause (d) Charterers Contribution Clause."* Same
instrument, same command, same four limbs, same order. `NEAR_VERBATIM` at 0.93/1.00
is right, and `NEAR_` rather than `EXACT_` is the correct restraint.

**H5 (§12).** Recurrence is real and is the cleanest in the paper. Desktop correctly
declines the 2010 date and correctly declines to substitute the host annotation's
2018/2019/2020 for it — those are recorded at their actual evidence level and are
not promoted. No unsupported date replaced another.

## I. FAMILY-EM-0004 repair — independently verified

Before: `frequency_known: 5` with one record. After: five records. I verified each
against MIW holdings rather than against each other:

| Occurrence | Verified |
|---|---|
| `OCC-2021-02-Q8` / `OCC-2022-02-Q8` | text confirmed in `historical_qp_intelligence.json`; marks correctly `null`, not inferred |
| `OCC-2023-12-Q3B` / `OCC-2026-06-Q3B` | text and inline `(8)` marks confirmed in specs |
| `OCC-2026-08-Q4B` | confirmed in `QP2608.json`, 4 marks |

The declared counts were correct and the *records* were missing, so creating five
records — rather than reducing frequency to 1 — is the right repair. Validator now
derives all five fields from one list. **These are not internally-consistent fakes.**

## J. Scribd — properly demoted

`SRC-SCRIBD-106245627` is marked `UNVERIFIABLE_FROM_REPOSITORY`, `superseded_by:
SRC-DGS-QBANK-ARCHIVED`, and its 3,043-byte stub hash is explicitly labelled as
hashing *the stub, not the historical text*. Swept all 29 Phase-2 artefacts: **zero**
references use Scribd as `TEXT_VERIFIED`, `DATE_VERIFIED` or candidate-grade
evidence. Clean.

## K. Limb / scaffold model

The four-way typing (`SOURCE_LIMB_CONFIRMED`, `SOURCE_LIMB_ASSERTED`,
`ANALYTICAL_SEGMENT`, `AUTHORING_SCAFFOLD`, plus `WHOLE_QUESTION`) is the right
shape and is applied honestly — `OCC-2023-12-Q3B` is downgraded to `ASSERTED`
purely because QP2312's spec carries `subparts: null`, which is exactly the
discipline required.

Scaffold exclusion holds: the sweep only reads `subparts[]` entries that have a
`label`, and the boundary inspection found both Study-Guide cases sitting on limb
`framing` — correctly identified as scaffold, not printed subpart. `main` is never
treated as a printed limb.

Residual risk (not a defect): the corpus uses **two `subparts[]` key conventions**
(`ref` vs `label`) under one `schema_version`. The sweep keys on `label`, so
`ref`-convention limbs are silently invisible to it. That understates coverage; it
cannot manufacture a false ancestor.

## L. Similarity — the main technical finding

Bidirectional containment is a genuine improvement and is what surfaced `Q8(a)`
(0.48 forward would have been missed; 0.96 reverse found it). All published
containment figures reproduce exactly on my own extraction.

**The short-stem guard is real but lives in only one of the two tools.**
`match_bank_to_corpus.py` skips any limb with `len(set(tokens)) < 4`, so one-word
limbs such as *Deviation* and *Warranties* never reach the classifier in the corpus
sweep. `negative_controls.py` has **no such floor**, and NC-5 feeds it the bare word
*"Warranties"* while accepting **four of six possible classes** as a pass — so NC-5
is close to unfalsifiable as written.

**DEFECT L-4 (model, the significant one): the classifier is blind to examiner
demand.** The `STOP` list deletes `give state explain list`, and there is no
duty-direction or command-verb term. I ran six adversarial cases of my own; **all
six fail**, and the last three clear the 4-token floor and so would reach the
classifier in a live sweep:

| My adversarial case | fwd | rev | Classified | Should be |
|---|---|---|---|---|
| ADV-1b *"Deviation"* vs **magnetic-compass deviation** | 1.00 | 0.14 | `ANCESTOR_NARROWED` | no match |
| ADV-1c *"War Risk Clause"* vs war-risk-area transit ops | 0.67 | 0.14 | `SAME_CORE_ASK_CANDIDATE` | no match |
| ADV-2 same reg 28, *state requirements* vs *criticise as ineffective* | 1.00 | 0.79 | `ANCESTOR_NARROWED` | distinguished |
| **ADV-3 inverted duty** — Chief Engineer's actions vs **PSC officer's** actions | 0.77 | 0.91 | `ANCESTOR_ABSORBED_AND_EXTENDED` | distinguished |
| ADV-4 *describe* vs *criticise*, same valve procedure | 0.90 | 0.90 | **`EXACT_OR_NEAR_VERBATIM`** | distinguished |

ADV-3 is the dangerous one: a candidate who answers the wrong party's duties fails
the question outright, and the model rates that pairing as an absorbed ancestor.
ADV-4 rates a changed command verb as a verbatim repeat.

This does **not** invalidate the seven families — each was adjudicated by reading,
and the Phase-2 prose is explicit that a changed command verb is *not* normalised
away (which is why `FAMILY-EM-0004` is `SAME_CORE_ASK` and not `EXACT_REPEAT`). The
finding is that **the declared model and the implemented model diverge**: the
discipline exists in the authors' heads and in the prose, not in the code. That is
safe at seven hand-checked families and unsafe at corpus scale.

## M. Validator — 105 checks / 0 failures reproduce; two gaps

Reproduced exactly: 105 checks, 0 failures; negative controls 6/6. C21 and C28
behave as documented — I confirmed C21 fires by setting `publication_status:
DATE_VERIFIED` while leaving `date_confidence: NONE`.

I then ran four corruptions of my own design, including two the validator was not
authored for:

| My mutation | Caught |
|---|---|
| **M-A** duplicate occurrence id (list length still equals `frequency_known`) | **YES** — 3 failures |
| **M-C** `earliest_occurrence` later than `latest_occurrence` | **YES** — 2 failures |
| **M-B** dangling `official_bank_ancestor: BANK-999` | **NO** |
| **M-D** `date_confidence` NONE → HIGH *and* status → `DATE_VERIFIED` together | **NO** |

M-A is the encouraging result: it defeats a naive length check and the validator
still caught it.

**DEFECT L-5.** No referential integrity between `official_bank_ancestor` and
`OFFICIAL_BANK_ITEMS.json` — a family may cite a bank item that does not exist.

**DEFECT L-6, and the one that qualifies Desktop's strongest claim.** `C21` enforces
*consistency* between status and `date_confidence`; **nothing derives
`date_confidence` from the occurrence records.** It is a hand-authored assertion. A
single-field edit promotes a family to `DATE_VERIFIED`. So Pilot D's statement —
*"under C21 the family cannot reach DATE_VERIFIED, so no 'Asked in July 2012' line
can ever render"* — is **too strong**. C21 makes the promotion *inconsistent to
write carelessly*; it does not make it *impossible*. The correct guarantee is
authoring discipline plus one consistency check, and that should be stated as such
before anything renders.

The data as it stands is correct. The *guard* is weaker than advertised.

## N. Paper DNA — recomputed from scratch, Desktop CONFIRMED

Computed from `QP2608.json` and my own sweep, not from Desktop's arithmetic.

Denominator: 9 × 16 = **144**, every mark printed and `KNOWN`. ✓

| Q | Unit counted | Marks | Class |
|---|---|---|---|
| Q1 | limb (a) only | 10 | `EXACT_REPEAT` |
| Q2 | whole | 16 | `EXACT_REPEAT` |
| Q4 | whole | 16 | `NEAR_VERBATIM` |
| Q8 | limb (b) | 6 | `EXACT_REPEAT` |
| Q8 | limb (a) | *10* | `SAME_CORE_ASK` |
| Q3, Q5, Q6, Q7, Q9 | — | 0 | none located |

- Wholly ancestored **2** (Q2, Q4) · partly **2** (Q1, Q8) · none **5** ✓
- Verified exact/near: 10 + 16 + 16 + 6 = **48 / 144 = 33.3%** ✓
- Same-core-inclusive: 48 + 10 = **58 / 144 = 40.3%** ✓

**No double-counting.** The two overlap traps are both correctly avoided: `Q1`'s
whole-question hit (0.72/1.00, 16 marks) is suppressed in favour of limb (a)'s 10;
and `FAMILY-EM-0004`'s limb-level 4 marks are not added to `FAMILY-EM-0007`'s
whole-question 16. Desktop's 33.3% stands.

**Corpus sweep also reproduces:** 93 non-null matches, **63 strong** — exactly
Desktop's figure — with `BANK-162 ×5, BANK-160 ×5, BANK-097 ×5, BANK-048 ×4` as the
most-reused items, exactly as claimed.

**DEFECT L-7.** Desktop reports 63 matches across **"21 of 40 papers"**. The correct
figure is **29 of 40**. Understates its own finding, but it is a wrong number in a
headline.

## O–R. Temporal pilots

**O · Pilot A (motivation) — `NONE`. AGREE.** Nothing regulated moved. Desktop
correctly classifies the 16→6 mark drop and the disappearance of the Maslow limb as
**recurrence-structure drift, not answer-law drift**, and refuses to let it inflate
impact. That is exactly the discrimination §23 asked for.

**P · Pilot B (dry dock) — `MINOR`. AGREE, and this is the best judgement call in
Phase 2.** Applying the brief's own test: a candidate who wrote the historical core
answer today and omitted BWM and cybutryne entirely would **not** materially fail —
the stem asks for coordination with the Master, preparations and delegation, and
undocking inspections. It does not ask about environmental compliance. BWM and AFS
are genuine law changes that are *not required to score this question*. Downgrading
from Phase 1's `MODERATE` is correct, and refusing to reward "new law exists" with
automatic impact is the whole point of the enum.

**Q · Pilot C (Merchant Shipping Act) — `MODERATE`. AGREE on impact; verification
is partial.** What I verified directly: **all five sittings are real** — `QP2307-Q9`,
`QP2410-Q1`, `QP2506-Q9`, `QP2508-Q5`, `QP2602-Q5` all print the unseaworthy-vessel
question and all name the *Merchant Shipping Act, 1958, as amended*. The recurrence
and the `DO NOT WRITE TODAY` construction are sound, and this is the only genuinely
demonstrable one in the corpus.

**Caveat — §25 asked for PRIMARY authority and I could not supply it.** The
commencement claim (Act 24 of 2025, assent 18 August 2025, whole Act in force
15 March 2026 by S.O. 1244(E), repealing the 1958 Act at s.324(1)) is corroborated
by MIW True Source and by prior session records, and is consistent across five
independently authored papers — but that is **repository authority, not primary**.
The Gazette notification itself was not read in this session. Given the entire
`MODERATE` pilot and the flagship candidate prototype hang from `S.O. 1244(E)`,
**Phase 3 should read the Gazette and pin it in the manifest.** I am not disputing
the fact; I am declining to certify it as primary-verified.

**R · Pilot D (lay-up) — date-block wording verified.** The block renders no year:
not "2012", not "around 2012", not "over a decade ago". The field is *absent*, not
hedged, which is the right design — a hedge is still a claim.

## S. Current answer correction candidates — NONE. AGREE, for a stronger reason.

I challenged this hard, expecting the GHG family to yield a stale answer. It does
not, and the reason matters: **MIW answers are sitting-anchored by design.**
`QP2309-Q3`'s own temporal record states *"NOTHING FROM MEPC 82, MEPC 83, THE 2025
EXTRAORDINARY SESSION OR THE NET-ZERO FRAMEWORK APPEARS. All are future by between
one and two years."* A sitting-anchored answer is a historical document; it cannot
go stale, only wrong-for-its-own-sitting.

Desktop's sweep is the right shape and its arithmetic is honest: 42 naive flags →
**2** after applying the sitting rule → **0** confirmed on reading the surrounding
step. The two survivors were single-bullet false positives.

**No correction candidate found. Nothing was patched. §31 confirmed.**

## T–U. Study-guide prototypes

Prototypes 1 and 2 are publishable in shape. Prototype 2 is the quietly important
one — an intelligence block that only ever fires on change teaches candidates that
its absence means "not checked", so `NONE` must be an ordinary visible outcome.

**Prototype 3 — recommend HOLD, and Founder decision 2 should stand.** Desktop
identified the risk but did not remove its two strongest carriers:

1. The heading is **"ASKED BEFORE"**. For a bank-only item, nothing was asked
   before, so far as we can prove.
2. The similarity line reads **"exact repeat"**. *Repeat* presupposes a prior
   occasion.

Removing the year is necessary but not sufficient; the surrounding frame still
asserts a prior sitting by implicature. Two evidence types genuinely need two
copy templates.

Recommended wording for the bank-only case — heading **"OFFICIAL QUESTION BANK
ITEM"**, and *"This question appears in the Directorate General of Shipping's own
published MEO Class I question bank, in these words."* No *asked*, no *repeat*, no
*again*, no *due*.

**Also note:** Prototype 1, the most publishable-looking of the three, rests on
`FAMILY-EM-0008`, which is **not serialised and therefore has no validator
coverage at all**. The most polished candidate artefact currently sits on the least
validated family. It must not ship in that order.

## V. Answer impact — recommend KEEP INTERNAL, translated when it does surface

Agree with the Founder's provisional decision. `NONE/MINOR/MODERATE/MAJOR` is
authoring vocabulary; MIW has been burned before by internal production vocabulary
reaching paid pages. When it eventually surfaces, translate rather than label:
*"No material answer change." / "Update one current-law point." / "Do not use the
older statutory reference."* The enum stays as the internal field that decides
whether and how the block renders.

## W. Exam Plan / Study Guide boundary — rule VALIDATED

Inspected the four named questions. Of 29 route steps, **2** cross the line, both on
limb `framing` — an authoring scaffold, which is exactly where an author-facing
edition-selection note should live. That is consistent with the Laptop's earlier
"<10 across 14,979" and means this is a forward rule, not a cleanup backlog.

The rule — *does removing this point change what the candidate writes?* — is sound
and I would keep it verbatim. One sharpening: *"the 2022 amendments are adopted but
not yet in force"* is Exam Plan because it **qualifies a requirement the candidate
is stating**; *"the operative text is the Convention as amended in 2014, 2016 and
2018"* is Study Guide because it selects an edition for the **author**. Status that
qualifies a stated requirement is Exam Plan; status that selects a source is Study
Guide.

## X. Publication status model — do NOT add `OFFICIAL_BANK_VERIFIED`

**Recommend the simpler design: `source_type` + `date_status`.** The status ladder
is a single linear axis; official-bank ancestry is not a rung on it — it is a
*stronger source* at the *same* date-evidence level. Adding a rung would put a
non-comparable value on an ordered scale and would immediately break C21's
`STATUS_ORDER.index()` arithmetic. The information is already fully represented by
`provenance_tier: OFFICIAL_BANK_ANCESTOR` + `date_confidence: NONE`. Nothing is
missing; no new status is needed.

## Y. Three-claim separation — HOLDS, and this is the best part of Phase 2

The three claims are independently representable and independently stored:

| Claim | Where | Can it leak? |
|---|---|---|
| Exists in an official DGS bank | `OFFICIAL_BANK_ITEMS.json` + `provenance_tier` | No — C28 blocks bank items from the occurrence file |
| Asked at a specific sitting | `QUESTION_OCCURRENCES.jsonl` + `date_confidence` | Guarded by C21, but see **L-6** — the guard is consistency, not evidence |
| Current answer has changed | `QP2608_TEMPORAL_DELTAS.md` + `answer_impact` | Independent of both |

A family reading `text HIGH / date NONE / source HIGH` is the model working, and
Phase 2 demonstrates it repeatedly and without embarrassment. C28 is verified to
block the inflation path: no bank item can reach `frequency_known`.

**DEFECT (documentation, folded into L-2's class).** Two internal contradictions:
`QUESTION_FAMILIES.json` calls `FAMILY-EM-0006` (GHG) *"Temporal Delta pilot C"* and
*"the only genuinely demonstrable DO NOT WRITE TODAY"*, while
`QP2608_TEMPORAL_DELTAS.md` assigns both to `FAMILY-EM-0008` (MS Act). The same
file's headline says *"Four of the six families"* — there are **seven**, and **all
seven** carry a bank ancestor. Stale text from before `FAMILY-EM-0007` was added.

## Z. NTA — recommend CLOSE WATCH

`NO OFFICIAL EVIDENCE FOUND` is retained and the reasoning is now stronger, not
weaker: the official bank supplies a **mundane, documented mechanism** for the
long-run recurrence the rumour was invoked to explain. Desktop correctly refuses to
treat that as causal evidence either way. 12,130 archived DGS URLs enumerated, no
NTA reference. Further searching has low expected yield. **Close it**; reopen only
on new primary evidence. No setter speculation may ever go candidate-facing.

## AA. DieselShip — CONFIRM DO-NOT-PURCHASE

Phase 2 **lowered** its value. A paid third-party aggregation would sit at a
*strictly lower provenance tier* than the Directorate's own published bank, would
still carry no verifiable sitting dates, and would reintroduce exactly the
unpreservable-third-party-source problem that Scribd already caused. No login, no
purchase.

## AB. The 830 archived MEO URLs — independently verified, with a correction that
changes Phase 3

I queried the Wayback CDX index myself: **11,917 archived `dgshipping.gov.in` URLs,
832 mentioning MEO** — matching Desktop's 12,130 / 830 to within snapshot drift.
Composition: **707 `.doc`, 120 `.pdf`** — and the one dated official paper already
recovered (2005) was a `.doc`. The naming convention is dated, centre-tagged and
machine-parseable: `meoclassI_mum_oct13_wo.pdf`, `meoiv(A)_chn_oct13.pdf`,
`meoclassII(B)_kol_sept13_wo.pdf`.

**Verdict: MEDIUM-HIGH — but Desktop's framing must be corrected.**

`WATCH_REGISTER` P3-002 says each recovered paper *"directly attacks the date
problem that blocks H1–H5"*. It does not. Class split across the 832:

| | Files |
|---|---|
| MEO Class **IV** | 60 |
| MEO Class **II** | 15 |
| MEO **Class I** | **12** |
| Marine Engineering **Management** (`mem`) | **2** |

The 12 Class I files run **Oct 2013 – Sept 2015** (year tokens: 13 ×31, 14 ×31,
15 ×19, 16 ×3), and the twelfth is the question bank itself. **There is nothing
from 2010–2012.** So the lead will supply dated official Class I artefacts — real
and valuable — but it **cannot** resolve the specific 2010–2012 claims behind
H1–H5. Several are also `_wo` result/notice documents rather than question papers,
so classification must precede extraction.

Founder decision 3 (attack the archive before broad 2013–2020 ingestion) is
**still right** — the archive *is* 2013–2015 material, so the two are largely the
same work, and doing it via the archive gets official provenance for free.

## AC. FAMILY-EM-0008 — Phase 3 should own it

Do **not** serialise now. Desktop's reasoning is correct and self-aware:
manufacturing five records in the closing stage would repeat the exact Phase-1
defect it just repaired, and the validator would not catch it because the numbers
would agree with each other. I independently confirmed the five sittings are real,
so the family is sound — it is the *records* that need building to the repaired
`FAMILY-EM-0004` standard. Phase 3's first task.

## AD. Research integration decision — **B, with a bounded exception**

**Keep Phase 2 branch-only until Phase 3**, with one exception: the six defects
below should be fixed **on the Phase-2 branch**, not carried into Phase 3.

Rejecting A (integrate infrastructure to main): the schema, validator and manifest
are the parts I found defects in (L-4, L-5, L-6, and a `D:\` path unresolvable by
the integration authority). Integrating them now would bless the weakest components.

Rejecting C (integrate validator/schema only): same objection, and it would split
the layer from the evidence that justifies it.

Nothing here is candidate-facing, nothing is on a delivery path, and the branch is
purely additive — so there is no cost to leaving it in place and a real cost to
merging claims for convenience.

## AE. Test results

| Check | Result |
|---|---|
| JSON / JSONL validity | all parse ✓ |
| Family validator | **105 checks, 0 failures** ✓ reproduced |
| Negative controls | **6/6 pass** ✓ reproduced |
| Desktop parser re-run on verified PDF | 185/185, gaps `[]` ✓ |
| Independent table-cell extractor | 185/185, no gaps, no dups ✓ |
| Cross-extractor agreement | **183/185 identical** (1 Desktop defect, 1 Laptop clip artefact) |
| 7 cited ancestors verbatim | **7/7 exact** ✓ |
| Corpus sweep | **63 strong matches** ✓ reproduced exactly |
| Paper DNA | **48/144 = 33.3%** ✓ reproduced exactly |
| Artefact sha256 | ✓ **exact match on independent re-download** |
| My adversarial similarity cases | **0/6 pass** → **DEFECT L-4** |
| My validator mutations | **2/4 caught** → **DEFECTS L-5, L-6** |
| Candidate-facing outputs | **none** ✓ |

## AF–AI. Boundaries

- **AF · Candidate-facing:** NOT PUBLISHED. Nothing wired to `solvedQP`, no spec, no
  Exam Plan. Confirmed by diff.
- **AG · Commercial:** untouched. No payment, entitlement, pricing or storefront
  file in the diff. *(Operational reminder only, outside this review: Razorpay
  `refund.created` / `refund.processed` webhook events still need enabling.)*
- **AH · Magazine:** untouched, paused.
- **AI · Bullet system:** untouched. 40 papers / 360 questions, bullet Exam Plan
  standard, no `plan_bullets` flag. QI-v2 adapts to it, not the reverse — confirmed:
  the sweep *reads* `subparts[]`, it never writes.

## AJ. Files / git

- Review branch `review/question-intelligence-v2-phase2` from `3b55bfb`.
- One file added: this report. No existing file modified. `main` untouched.
- Phase-2 branch not merged. No force push. Temporary worktree removed; both repos
  verified clean.

## AK. Founder decisions (5)

1. **Canonical storage for the bank PDF.** Approve the git-ignored historical-QP
   intake store + second physical mirror + manifest-only in git (§E)? It is
   currently single-copy on one machine and load-bearing. Not for the public repo,
   not for True Source.
2. **Prototype 3 wording.** Approve replacing *"ASKED BEFORE"* / *"exact repeat"*
   with *"OFFICIAL QUESTION BANK ITEM"* / *"appears in the Directorate's own
   published question bank, in these words"* for bank-only evidence — two evidence
   types, two copy templates?
3. **Similarity hardening before scale (L-4).** Require a command-verb and
   duty-direction term in the classifier, and a real NC-5, **before** QI-v2 is run
   beyond the seven hand-checked families?
4. **Date guarantee (L-6).** Require `date_confidence` to be *derived* from
   occurrence records rather than hand-asserted, before any block renders?
5. **Phase 3 scope, given AB.** The archive yields dated Class I material for
   **2013–2015 only, not 2010–2012**. Confirm Phase 3 targets it anyway (I
   recommend yes — it is real dated official evidence and largely the same work as
   2013–2020 ingestion), accepting that H1–H5's dates stay unproven?

## AL. Phase 3 design (do not execute)

1. **Fix the six defects on the Phase-2 branch first** — L-1 (item 182 reading
   order), L-2 (BANK-4→3, pilot-C contradiction, "four of six"→seven, 21→29
   papers), L-3 (de-date the H1–H5 filenames), L-4 (command-verb/duty-direction
   term + a real NC-5), L-5 (bank-ancestor referential integrity), L-6 (derive
   `date_confidence`; restate the Pilot D guarantee accurately). Replace the `D:\`
   paths with a machine-independent retrieval recipe.
2. **Inventory the 832 archived MEO URLs** — classify by class, centre, month/year
   and document type; separate question papers from `_wo` result notices.
3. **Recover and hash dated official papers**, prioritising the 12 Class I files
   (Oct 2013 – Sept 2015). Preserve raw; manifest each with sha256.
4. **Read the Gazette for S.O. 1244(E)** and pin the MS Act 2025 commencement to
   primary authority (§Q).
5. **Serialise `FAMILY-EM-0008`** to the repaired `FAMILY-EM-0004` standard — five
   occurrence records, limb kinds resolved against printed subparts, marks read not
   inferred.
6. **Link verified bank ancestors to verified sittings** wherever a recovered dated
   paper permits — this is the only route that converts bank ancestry into dated
   occurrence.
7. **Extend temporal deltas only on HIGH-confidence families.** The GHG family
   (`FAMILY-EM-0006`) is the strongest untouched candidate — its stem asks for a
   current state of play, which makes it the one family guaranteed to go stale for
   a candidate studying an older answer. Desktop named it the sharpest test and
   then piloted something else.
8. **No candidate publication.**

## AM. Next action

**GO.** Fix the six defects on the Phase-2 branch, then:

> **DESKTOP CLAUDE — BEGIN QUESTION INTELLIGENCE V2 PHASE 3 BY SYSTEMATICALLY
> MINING THE ARCHIVED DG SHIPPING MEO URL SET FOR DATED OFFICIAL PAPERS, LINKING
> VERIFIED BANK ANCESTORS TO VERIFIED SITTINGS, AND EXTENDING TEMPORAL ANSWER
> INTELLIGENCE ONLY ON HIGH-CONFIDENCE FAMILIES.**

## AN. Verdict

# GO — QUESTION INTELLIGENCE V2 PHASE 2 INDEPENDENTLY VERIFIED

The source is authentic and I reproduced its hash byte-for-byte from a different
machine. The extraction is sound and I confirmed it with a structurally independent
extractor. The recurrence families are real and their containment figures reproduce
exactly. The Paper DNA arithmetic is right to the mark. Date confidence and
recurrence confidence are genuinely separated, and no bank item can reach a sitting
count.

The six defects are real but none is architectural: two documentation errors, one
parser reading-order fault on an uncited item, one filename hazard, and two guards
weaker than advertised. The one that matters is **L-4** — the classifier scores
nouns, not examiner demand — and it matters *at scale*, not at seven hand-adjudicated
families.

The governing principle held under adversarial test, which is the finding that
counts: **question recurrence is high while date confidence is zero, and the model
says so without flinching.**
