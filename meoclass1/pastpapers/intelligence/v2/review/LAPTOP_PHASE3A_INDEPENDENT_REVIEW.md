# Question Intelligence V2 — Phase 3A independent review (Laptop)

**Reviewer:** Laptop (integration authority) · `current_as_of: 2026-08-18`
**Status of this document:** review finding. Nothing here is candidate-facing.
**Verdict:** `HOLD — QUESTION INTELLIGENCE V2 PHASE 3A NEEDS ONE MORE BOUNDED REPAIR`

This is the second adversarial review. Desktop's report and its repair register were
treated as claims to attack, not as evidence. Every headline number was recomputed on
this machine. The source artefact was re-obtained from the open internet rather than
copied. Five of the six Phase-2 defects are genuinely repaired and I can prove it.
The HOLD rests on three of the Founder's own explicit gates, not on the architecture.

---

## A. Repo truth

| | Actual | Brief said |
|---|---|---|
| `origin/main` | `3b55bfb` | `3b55bfb` ✓ |
| Phase 3A tip | `17ad3cf` | `17ad3cf` ✓ |
| Phase-2 review | `7d8177b` on `review/question-intelligence-v2-phase2` | "not locatable" |

Working tree clean at start and end. Phase 3A was **not** merged. Review performed in
a detached clean worktree at `17ad3cf`, which is also the portability test bed (§O).

Phase 3A commits (5): `fb73261 · f369db3 · cce4190 · ae02b45 · 17ad3cf`.

---

## B. The original Phase-2 review — RECOVERED

**`ORIGINAL LAPTOP PHASE-2 REVIEW RECOVERED IN FULL.`**

It exists on this machine as commit `7d8177b`, branch
`review/question-intelligence-v2-phase2`, one file, 663 lines:
`meoclass1/pastpapers/intelligence/v2/review/LAPTOP_PHASE2_INDEPENDENT_REVIEW.md`.

**Desktop's §0 caveat was correct and its diagnosis was correct.** The branch was
never pushed to origin. That was my failure at the end of the Phase-2 session and it
cost Desktop a whole reconstruction. It does not repeat: this review is pushed (§AN).

I read the original in full before reading the repair register. The findings below
are quoted from it, not from the Founder brief's paraphrase.

### The exact L-1 … L-7 reconciliation

My Phase-2 review recorded **seven** numbered defects, not six. Desktop's register
carries six and **its numbering is shifted**, because it reconstructed from the brief.

| Laptop ID (original) | Laptop finding, as written | Desktop's ID | Same defect? | Repair fixes it? | Test proves it? |
|---|---|---|---|---|---|
| **L-1** | Item **182** scrambled by the parser; `(i)/(ii)/(iii)` charter list out of reading order | **L-2** | **YES** | **YES** — verified | **YES** — independent extractor |
| **L-2** | `(Oct-05)` attributed to `BANK-4`; it is on item **3** | **L-3** | **YES** | **YES** — corrected in all three files | **PARTLY** — `C33` proves it, but `C33` **skips on this machine** |
| **L-3** | H1–H5 **filenames assert dates** the model refuses to assert | *(absent)* | **NOT REGISTERED** | **NO** | **NO** |
| **L-4** | Classifier **blind to examiner demand**; `STOP` deletes the command verbs; 6/6 adversarial cases fail | **L-4** | **YES** | **MOSTLY** — 6/6 now pass, but see §F | **YES**, for the cases Desktop anticipated |
| **L-5** | No **referential integrity** between `official_bank_ancestor` and the bank items | **L-1** | **YES** | **YES** | **YES** — 6 bank mutations |
| **L-6** | `date_confidence` is **hand-asserted, not derived**; C21 is a consistency check only | **L-6** | **YES** | **YES** | **YES** — 5 date mutations, and my own §Q |
| **L-7** | "63 matches across **21 of 40 papers**" — correct figure is **29** | *(folded)* | folded into headline rework | **MOOT** — headline replaced (§I) | n/a |
| *(prose, inside my §L)* | short-stem floor lives in the sweep, not the classifier; NC-5 near-unfalsifiable | **L-5** | **YES** — Desktop promoted it to its own number, correctly | **YES** | **YES** |

**Verdict on the mapping.** Desktop's reconstruction is substantively faithful. Its
numbering differs and I do **not** fail Phase 3A for that, exactly as the brief
directs. But the mapping is **not complete**: my **L-3 is absent from the register
and unrepaired**. Everything else maps.

**Desktop's procedural HOLD is resolved.** The register may now be treated as
mapped, with L-3 reopened.

---

## C. Phase-3A scope — PASS, cleanly

**34 files, 6,405 insertions, `A` on every one. Zero modifications, zero deletions.**

Every path is under `meoclass1/pastpapers/intelligence/v2/`. A purely additive diff
is the strongest available scope proof: it is structurally impossible to have
regressed anything. Counts of touched files: `pastpapers/specs/` **0**;
solvedQP / payment / entitlement / refund / Razorpay / magazine / `api/` **0**.

No contamination. §36, §37, §38 answered by construction.

---

## D. Defect register reconciliation — 5 of 6 repaired, 1 unregistered

| | Repaired | Independently verified by me |
|---|---|---|
| Item 182 (my L-1) | YES | **YES** — see §K |
| Oct-05 (my L-2) | YES | **YES** — see §L |
| Dated filenames (my L-3) | **NO** | still `H1_QP2608_Q1_JUN2010.md` … `H5_…_MAR2010.md` |
| Examiner demand (my L-4) | MOSTLY | **6/6 originals pass; 5 new failures** — §F |
| Bank integrity (my L-5) | YES | **YES** — §M |
| Derived dates (my L-6) | YES | **YES** — §P, §Q |

**L-3 restated.** The five verification filenames, and their `#` headings, assert
`JUN2010`, `DEC2011`, `OCT2012`, `APR2010`, `MAR2010`. The bodies are honest — they
frame these as *the claim* under adjudication — and §AB now states plainly that the
dates are unsupported. But the filenames are the part that gets indexed, linked and
quoted out of context. Phase 2 called this a naming hazard; it is still one.

---

## E. Similarity architecture — ONE classifier, confirmed

`tools/qi_similarity.py`, 627 lines, is the single executable classifier.

- `match_bank_to_corpus.py`, `adversarial_controls.py` → `import qi_similarity as qs`.
- `negative_controls.py` is a pure shim delegating to `adversarial_controls.py`.
- **Zero** local definitions of `cont`, `toks`, `classify`, `STOP`, `T_EXACT` or
  `_containment_class` anywhere else in the tree.

No stale alternate classifier remains load-bearing. **Phase 2's three drifted copies
are genuinely gone.** This is the single best structural improvement in Phase 3A.

The five-feature model (demand / actor / polarity / numbers / lexis) with
demote-only semantics is the right shape: containment proposes a ceiling, and no
feature can ever promote. `Options` exists solely so a mutation can prove each guard
is load-bearing, which is the correct discipline.

---

## F. Examiner demand — the six originals PASS; five NEW failures

I wrote a fresh suite (`laptop_adv.py`, 27 cases) without reading Desktop's fixtures,
and re-ran the six cases that **all failed** in Phase 2.

### The Phase-2 killers — 6/6 now correctly rejected

| Phase-2 case | Phase 2 | Phase 3A | |
|---|---|---|---|
| `Deviation` vs magnetic-compass deviation | `ANCESTOR_NARROWED` | `UNSCOREABLE_SHORT_STEM` | fixed |
| `War Risk Clause` vs war-risk transit ops | `SAME_CORE_ASK_CANDIDATE` | `UNSCOREABLE_SHORT_STEM` | fixed |
| reg 28 *state* vs *criticise as ineffective* | `ANCESTOR_NARROWED` | `TOPIC_ONLY` (demand 0.25) | fixed |
| **Chief Engineer vs PSC officer actions** | `ANCESTOR_ABSORBED_AND_EXTENDED` | `TOPIC_ONLY` (actor INVERTED) | **fixed** |
| *describe* vs *criticise*, same valve | `EXACT_OR_NEAR_VERBATIM` | `TOPIC_ONLY` (demand 0.25) | **fixed** |

The dangerous one — the inverted duty — is properly demoted. **L-4's core is repaired
and I confirm it independently.** True repeats carrying MIW mark annotations `(4)`,
`(6)` stay `EXACT_REPEAT`, so the guard does not over-fire.

### Five new failures, and one root cause behind three of them

| ID | Case | Result | Should be |
|---|---|---|---|
| **L7-B** | Flag State duties, *Describe* vs *Criticise* | **`EXACT_REPEAT`** | distinguished |
| **L7-D** | "maintained in a **state of readiness**", *Describe* vs *Criticise* | **`EXACT_REPEAT`** | distinguished |
| **L6-E** | equipment **required** vs **not required** | **`NEAR_VERBATIM`** | distinguished |
| **L10-A** | sulphur **0.50%** vs **0.10%** | **`EXACT_REPEAT`** | distinguished |
| **L10-B** | **440 V** vs **1000 V** switchboard | **`NEAR_VERBATIM`** | distinguished |

**P3A-1 (HIGH) — `demand_compatibility` aggregates with `max()`.**

```
{DESCRIBE, RESPONSIBILITY} vs {CRITICISE, RESPONSIBILITY}  ->  1.00
{DESCRIBE}                 vs {CRITICISE}                  ->  0.25
```

Any **shared secondary demand marker neutralises an opposite primary command verb**.
`responsibilities of` → `RESPONSIBILITY` is extremely common in MEO Class I stems, and
`PROCEDURAL_ACTION` (`what action`, `how would you`) is commoner still. This is L-4
re-entering through a side door on a large fraction of the corpus. It did not surface
in Desktop's 21 controls because every control pairs stems carrying a *single* demand.

**P3A-2 (MEDIUM) — regime masking is not general enough.** `_REGIME_PHRASES` covers
`state of the art` but not `state of readiness` — or any other `state of X`. §7's
requirement is only partly met: `Port State Control`, `Flag State` and `coastal State`
mask correctly, but `state of readiness` yields a spurious `STATE`, which then feeds
P3A-1.

**P3A-3 (MEDIUM-HIGH) — no negation / requirement-polarity feature.** `_POLARITIES`
models lay-up/reactivation, docking/undocking, loading/discharging and so on, but not
`required` vs `not required`, `permitted` vs `prohibited`, `mandatory` vs
`recommended`. A candidate who answers the affirmative of a negative stem fails
outright — the same severity as the actor inversion that Phase 3A rightly fixed.

**P3A-4 (MEDIUM) — `numbers()` covers only integers 1–20, and mangles decimals.**

```
'0.50 percent'  -> numbers = []        # 0 and 50 both out of range
'0.10 percent'  -> numbers = [10]      # 10 happens to be in range
'440 volt'      -> []      '1000 volt' -> []
```

The conflict test is `A.numbers and B.numbers and A != B`, so an empty side never
fires. Whether a load-bearing technical magnitude is caught is **arbitrary**, decided
by which decimal digits happen to land in 1–20. Sulphur limits, voltages, pressures
and tonnage thresholds — the numbers an MEO Class I answer actually turns on — are
outside the guard. `0.50` vs `0.10` reads as an exact repeat.

**What still works:** counting quantities are caught (`five` vs `three` causes →
`SAME_CORE_ASK`), `two` vs `three years` is caught, and the marks-annotation fix is
correct and necessary.

---

## G. Actor / polarity / number tests

**Actor — good, with a scope gap.** `CHIEF_ENGINEER` vs `PSC_OFFICER`, vs `SURVEYOR`,
`FLAG_STATE` vs `PORT_STATE`, `OWNER` vs `CHARTERER` all invert correctly. The
`_ACTOR_ECLIPSE` design is the right answer to my Phase-2 concern that generic
`PORT_STATE` masking could hide a `PSC_OFFICER` inversion — a specific actor now
eclipses its general, so the sets no longer spuriously intersect. Adjacent ranks
(`CHIEF_ENGINEER`/`SECOND_ENGINEER`) demote to `NEAR_VERBATIM` rather than being
destroyed, which is right: the bank itself reuses item 64/182 across ranks. Shared
actors are **not** over-penalised — a question naming both CE and PSC is `SAME`, not
inverted.

**Gap:** §8 named `Company` and `Administration`. Neither exists in `ACTORS`.
`Administration` is arguably covered by `FLAG_STATE`; **`Company` is not covered at
all**, and the Company/Master and Company/DPA distinctions are ISM-central.

**Polarity — works where modelled**, does not cover negation (P3A-3).

**Numbers — see P3A-4.**

---

## H. Short-stem guard — PASS, and it is in the right place

`classify()` called **directly**, self-paired (the worst case), not through the sweep:

| Stem | distinct tokens | Result |
|---|---|---|
| Deviation | 1 | `UNSCOREABLE_SHORT_STEM` |
| Warranty | 1 | `UNSCOREABLE_SHORT_STEM` |
| War risk | 2 | `UNSCOREABLE_SHORT_STEM` |
| Salvage | 1 | `UNSCOREABLE_SHORT_STEM` |
| CII | 1 | `UNSCOREABLE_SHORT_STEM` |

The floor is inside the shared classifier, returns a dedicated class rather than a
silent skip, and NC-5 now permits exactly one outcome. **Fully repaired.**

---

## I. 63 → 45 — VALID reclassification, no recurrence lost

I reconstructed the Phase-2 model (containment only, floor in the sweep loop) and
diffed the two result sets rather than comparing headline numbers.

| | |
|---|---|
| Phase-2 reconstruction, containment-strong | **66** |
| Phase-3A exact/near | **45** |
| **kept in both** | **45** |
| **new in Phase 3A only** | **0** |
| demoted | 21 |

**The exact/near set is identical. Nothing was gained and nothing legitimate was
lost.** Every one of the 21 demotions is `ANCESTOR_ABSORBED_AND_EXTENDED` or
`ANCESTOR_NARROWED` → `SAME_CORE_ASK`. **Not one** was demoted to `TOPIC_ONLY` by
demand incompatibility.

Sampling the demoted set settles it. `QP2608-Q8 __WHOLE__` scored fwd **0.26** /
rev 1.00 — a bank item sitting wholly *inside* a much larger question. `QP2311-Q3`
scored fwd 0.35. Calling those "exact or near repeats" was always wrong. They are
real recurrence, of a different kind, and they are **still reported** — in the
same-core bucket, 37 of them.

Phase 2's "63 strong" conflated two relationships under one word. The correction is
a reporting fix, not a loss. **Do not preserve 63.** (My reconstruction yields 66
rather than Desktop's 63 because I emulate Phase 2's sweep-level floor rather than
re-running its exact code; the load-bearing set — 45 — matches exactly.)

---

## J. QP2608 Paper DNA — 48/144 reproduces, third independent time

Recomputed from `QP2608.json` and my own sweep. Denominator 9 × 16 = **144**, every
mark printed.

| Q | Unit | Marks | Class |
|---|---|---|---|
| Q1 | limb (a) — whole suppressed | 10 | `EXACT_REPEAT` |
| Q2 | whole | 16 | `EXACT_REPEAT` |
| Q4 | whole — limbs unscoreable, parent inherited | 16 | `NEAR_VERBATIM` |
| Q8 | limb (b) | 6 | `EXACT_REPEAT` |
| Q8 | limb (a) | 10 | `SAME_CORE_ASK` |

- **Verified exact/near: 48 / 144 = 33.3%** ✓
- **Same-core inclusive: 58 / 144 = 40.3%** ✓

**Inheritance does NOT double count**, and I tested the trap the brief named:

| | Trap | Outcome |
|---|---|---|
| Q1 | whole (16) + limb (a) (10) | whole **suppressed**, 10 counted, not 26 |
| Q4 | four short-stem limbs + whole (16) | limbs score 0, whole counted, **16 not 32** |
| Q8 | whole (16) + (a) 10 + (b) 6 | whole **suppressed**, 16 counted, not 32 |

No question ever contributes more than its printed 16. A naive limb-eclipses-whole
rule (ignoring short-stem inheritance) yields 32/144 = 22.2%; the model's own
documented rule yields 48/144. Desktop's figure stands, and the rule that produces it
is stated in the model rather than invented to reach a number.

---

## K. Bank extraction — item 182 REPAIRED, independently confirmed

I did not accept Desktop's re-extraction. I **re-downloaded the source** using the
manifest's own retrieval recipe and extracted it twice by structurally different
means.

| | |
|---|---|
| Re-download, Wayback raw `id_` route | **314,710 bytes**, `%PDF-1.7` |
| sha256 | `0e0d6bc7…1438cb51` — **exact match**, second independent day |

- Desktop's repaired parser on my copy: **185 items, range 1–185, gaps `[]`**.
- My PyMuPDF `find_tables` extractor: **185 items, 1–185, no gaps, no duplicates**.
- **Cross-extractor agreement: 184 / 185.**

**Item 182 is identical between the two extractors and in correct reading order.** The
Phase-2 scramble (*"Differentiate the (iii) Time charter. As a Chief Engineer…"*) is
gone; the text now reads `Bill of Lading … (i) Bare boat (ii) Voyage (iii) Time …`.

Phase 2 measured 183/185 with **two** disagreements — Desktop's item-182 defect and
one clip artefact of my own extractor. Phase 3A measures **184/185 with only my clip
artefact left.** That is exactly the predicted delta and it independently confirms
Desktop's claim: **184 items unchanged, only 182 corrected, 185/185 held.**

**Item 181** — `a. b. d. c.` — is byte-identical in both extractors. It is a genuine
DGS source typo, correctly preserved, not a defect. Confirmed for the second time.

**All 9 curated bank items verify EXACT** against my independent extract, including
all 7 cited ancestors plus `BANK-039` and `BANK-160`.

---

## L. Oct-05 — CORRECT everywhere

`(Oct-05)` is carried by **item 3**, confirmed by both extractors independently.
All three write-ups now say `BANK-3`. Swept the whole `intelligence/v2` tree: the
only surviving mentions of `BANK-4` are inside the **correction notes themselves**
("Phase 2 recorded this against BANK-4; it belongs to BANK-3"), which is proper
disclosure, not a stale claim. **No stale attribution remains.**

**One minor documentation defect:** `SOURCE_MANIFEST.json` says the attribution is
now derived by check **`C29`**. It is derived by **`C33`**; `C29` is the bank-id
uniqueness check.

---

## M. Bank referential integrity — real, and mutation-proven

Desktop's 6 bank mutations: duplicate id, id/number disagreement, missing cited item,
blank text, altered text, unknown source. **5 caught here; the 6th (`C32`) escapes on
this machine only because the extract is absent** — see §O.

With the extract supplied, **all 6 caught.**

---

## N. Extracted bank JSON — COMMIT IT. I can now prove the case rather than argue it.

I did not take this on recommendation. I measured it, both ways:

| | Checks | Skipped | Mutations | **Escapes** |
|---|---|---|---|---|
| Branch as committed, on Laptop | **166** | **2** (`C32`, `C33`) | 33 | **1** |
| Same branch + the extracted JSON | **169** | **0** | 33 | **0** |

Committing the extract converts **two silent-skipping checks and one escaping
mutation into three executable ones**, and reproduces Desktop's headline exactly.
Without it, a **tampered bank text passes undetected on the integration authority's
machine** — and that is the single most load-bearing integrity check in the layer,
because it is what ties the curated ancestors to the official source.

The Founder's four conditions are all met, and I verified each rather than assuming:

1. **From the authenticated public official DGS bank** — yes; I re-downloaded it
   myself and the sha256 matched byte-for-byte.
2. **Only extracted question-bank research data** — yes; two fields per item,
   number and text.
3. **No licensing or security concern** — it is a Government of India public
   examination question bank, published on the Directorate's own host, no paywall,
   no login, no restriction. `pastpapers/` is already outside the deploy.
4. **Lets Laptop validators run** — proven above.

It is also **reproducible, not merely copyable**: I regenerated it from the branch's
own manifest recipe in this session. That is what makes it a legitimate research
artefact rather than an opaque blob.

**Recommend: commit `dgs_meo_cl1_bank_items.json` (~53 KB) under
`meoclass1/pastpapers/sources/official/dgshipping/`, and repoint the tools to it.
Do NOT commit the 314 KB PDF** — the manifest recipe demonstrably re-obtains and
re-verifies it on demand, which I have now done twice on two different days.

---

## O. Portability — **FAILS**, and more broadly than Desktop reported

This is the decisive section. From a clean worktree, with no `D:` drive on this
machine (only C, F, G, H, I):

| Tool | Hardcoded `D:` path | Consequence on Laptop |
|---|---|---|
| `validate_families.py` | `EXTRACTED_BANK` | 2 checks skip, **1 mutation escapes** |
| `match_bank_to_corpus.py` | `BANK` **and `SPECS`** | **will not run at all** |
| `parse_dgs_question_bank.py` | `PDF`, `OUT` | **will not run at all** |

**Desktop reported only the bank JSON. The larger problem is `SPECS`:**

```python
SPECS = r'D:\Marine-Intelligence-Weekly\meoclass1\pastpapers\specs'
```

Those 40 spec files are **committed repo content**, sitting two directories above the
tool, and the tool points at a Desktop-local absolute path to reach them. That needs
no Founder decision and no new artefact — it is a one-line repo-relative fix, and
`validate_families.py` already does it correctly with `HERE`/`V2`/`PASTPAPERS`.

Consequence: **the 45-match sweep and the 48/144 Paper DNA are not reproducible on
this machine from the branch as committed.** I reproduced both only by editing the
tools. The Founder's rule — *"Any load-bearing check that SKIPS because a Desktop
path is absent is a HOLD"* — is met, and so is the governing principle *"do not scale
until Laptop can reproduce the model from a clean worktree."*

The manifest itself is portable: `retrieved_via_url` records the Wayback raw `id_`
route, which is exactly the Phase-2 required fix, and it worked end-to-end. **The
data is portable; the tools are not.**

---

## P. Date evidence model — genuinely DERIVED. L-6 repaired.

`C36`–`C38` derive the date claim from evidence, with `OFFICIAL_QUESTION_BANK` in
`NEVER_DATE_BEARING` and — the important part — **the current sitting excluded**, so
a paper can never be evidence of an earlier one.

Desktop's 5 date mutations, each keeping every field mutually consistent and removing
only the evidence: **5/5 caught.** I ran my own (§Q, LC-6b): re-sourcing all 21
occurrences of the five date-bearing families to the bank fires `C36`/`C37`/`C38`
across every one.

Phase 2's Pilot D guarantee was overstated and is now true by construction. **This
is the second-best improvement in Phase 3A.**

---

## Q. Duplicate-ID test — CAUGHT, and not by a length check

The brief's explicit §18 test: replace one occurrence id with another existing id so
the list length is unchanged and still equals `frequency_known`.

**CAUGHT — three checks fire:** `C13` (duplicates within the family), `C26` (an
occurrence claimed twice), `C27` (the displaced record orphaned). `len(list) ==
frequency_known` is explicitly not what is relied on.

---

## R. Three-claim separation — HOLDS

| Claim | Store | Leak-proof? |
|---|---|---|
| A · Official DGS bank ancestry | `OFFICIAL_BANK_ITEMS.json` + `provenance_tier` | `C28` blocks bank items from the occurrence file |
| B · Verified dated sitting | `QUESTION_OCCURRENCES.jsonl` + derived date | `C36`–`C38`, now evidence-derived |
| C · Temporal answer change | `QP2608_TEMPORAL_DELTAS.md` + `answer_impact` | independent of both |

Live combinations observed in the data: `EM-0001/0002/0007` = bank yes / dated no /
change none; `EM-0008/0009` = bank yes / dated yes / change MAJOR; `EM-0005` =
`RESEARCH_HYPOTHESIS`, dated no. No single field blurs the three. `PUBLICATION_STATUS_MODEL.md`
correctly declines to add an `OFFICIAL_BANK_VERIFIED` rung, which was my Phase-2
recommendation.

---

## S. FAMILY-EM-0008 — CORRECT, and it matches my Phase-2 verification exactly

Ancestor **BANK-160**, five occurrences, the unseaworthy-vessels family:

| Occurrence | Paper | Verified in Phase 2 |
|---|---|---|
| `OCC-2023-07-Q9` | QP2307-Q9 | ✓ |
| `OCC-2024-10-Q1` | QP2410-Q1 | ✓ |
| `OCC-2025-06-Q9` | QP2506-Q9 | ✓ |
| `OCC-2025-08-Q5` | QP2508-Q5 | ✓ |
| `OCC-2026-02-Q5` | QP2602-Q5 | ✓ |

These are the **exact five sittings I independently confirmed in Phase 2 §Q**. Marks
read (16 each), text preserved, `BANK-160` verbatim-exact against my extract.
**Serialised correctly. P3-001 discharged.**

### But the prose still names the wrong family in two places

`MERCHANT_SHIPPING_ACT_AUTHORITY.md` §5 is headed **"Temporal delta for
FAMILY-EM-0008"** and then describes *"five sittings from March 2023 to July 2025"*
with *"the QP2402 grounding variant"*. That is **FAMILY-EM-0009**'s data exactly.
`PROTOTYPE_EVIDENCE_CLASSES.md` repeats it: its Type A worked example lists
EM-0009's dates and captions them *"as FAMILY-EM-0008 does"*.

`QP2608_TEMPORAL_DELTAS.md:234` and `WATCH_REGISTER` P3-001 both correctly define
EM-0008 as unseaworthy vessels, so the **data is right and the write-ups are wrong** —
the same direction of error as the Oct-05 defect, and the same *class* of error
Desktop made when it first serialised the wrong family under EM-0008.

**Consequence that matters:** the repair register's §4 gate — *"`FAMILY-EM-0008` must
not advance toward candidate use until the section-by-section mapping is done"* —
is attached to the **wrong family**. The Part XII casualty mapping is what
**EM-0009** needs. As written, EM-0009 is ungated and EM-0008 is gated for a reason
that is not its own.

---

## T. FAMILY-EM-0009 — KEEP SEPARATE. Confirmed on the evidence.

Ancestor **BANK-039**, five occurrences 2023-03 → 2025-07. The core ask is *the steps
to be initiated under the Merchant Shipping Act following a casualty to an Indian
flag vessel* — a different examiner task from EM-0008's *what is an unseaworthy
vessel and how does it differ from an unsafe ship*. Different ancestor, different
stems, different marks distribution.

**Agree with the Founder's provisional decision: keep EM-0009 separate.** There is no
evidence for folding, and folding would merge a 10-sitting super-family that never
existed.

*(Within-family note, not a defect: `OCC-2024-02` is a grounding-and-abandonment
variant while the other four are collisions. The core ask holds.)*

---

## U. Merchant Shipping Act 2025 — primary authority CONFIRMED

Independently verified, not taken from Desktop's summary:

- **Act 24 of 2025**, Presidential assent **18 August 2025**.
- **S.O. 1244(E)**, dated **10 March 2026**, appoints **15 March 2026** as the
  commencement date.
- **s.324(1)** repeals the Merchant Shipping Act, 1958 *"except Part XIV but not
  including section 411A therein"*, and the Coasting Vessels Act, 1838.

All three corroborated from independent public sources. `dgshipping.gov.in` remains
`ECONNREFUSED 164.100.60.201:443` and `indiacode.nic.in` returns `403` to automated
fetch — both exactly as Desktop recorded, and as I saw in Phase 2. Desktop's Gazette
route via `shipmin.gov.in` is sound and its hash is recorded.

**My Phase-2 §Q caveat is discharged.** The commencement is now pinned to primary
authority.

---

## V. Section 324 / Part XIV — Desktop is RIGHT, and there is one material omission

### The correction is correct

| 1958 Act | Subject | Independently confirmed |
|---|---|---|
| Part XII | **Investigations and Inquiries** | ✓ |
| Part XIII | **Wreck and Salvage** | ✓ |
| **Part XIV** | **Control of Indian Ships and Ships Engaged in Coasting Trade** | ✓ |

Confirmed from the Directorate's own page title (`dgshipping.gov.in/Content/PARTXIV.aspx`
— *"PART XIV Control Or Indian Ships And Ships Engaged In Coasting Trade"*) and from
independent legal reporting. **Wreck and Salvage is Part XIII, not Part XIV.** The
confident secondary source Desktop encountered was wrong, and Desktop was right to
refuse it. This is the most valuable single finding in Phase 3A.

### The omission — the Coastal Shipping Act, 2025

Desktop's authority document says Part XIV is **"in force"** from 15 March 2026,
except s.411A. It does not mention the **Coastal Shipping Act, 2025 (Act No. 20 of
2025**, assent **9 August 2025)**, which **separately repeals Part XIV of the 1958
Act, except s.411A**, and re-enacts coasting-trade licensing as a standalone statute.

The two interlock precisely: MSA 2025 saves Part XIV *minus* 411A and repeals 411A;
the CSA 2025 repeals Part XIV *except* 411A. Between them, **Part XIV is
comprehensively dismantled** — the MSA 2025 alone does not tell that story.

I could not confirm the CSA's commencement notification, so I do **not** assert Part
XIV is already gone. But a document titled *primary authority* on what survives
repeal that omits the statute repealing the surviving Part is incomplete, and will
become wrong the moment the CSA is notified.

**Notably, MIW's own live corpus already knows this** — `QB10_A.html` and
`oralnotes/simon-notes-p2.html` both correctly name the Coastal Shipping Act as
replacing 1958 ss.406–407 (Part XIV). **The live product is ahead of the research
branch here.**

---

## W. Current answer correction candidates — the specific error is ABSENT; a related class is PRESENT

Bounded exact/semantic sweep of the current corpus. **No edits made.**

- *"1958 Act wholly repealed"* (unqualified, candidate-facing) — **NONE.**
- *"Part XIV = wreck and salvage"* — **NONE.** The specific error Desktop guarded
  against does not exist in MIW.
- *"wreck / salvage survived repeal"* — **NONE.**
- *"Investigations survived repeal"* — **NONE.**

The past-paper specs are clean for the reason my Phase-2 §S established: **MIW answers
are sitting-anchored.** Every hit is an authoring `why` note explicitly dating itself
("correct at this sitting and until 15 March 2026"). That is the model working.

### Two candidates found, of a different kind

**`CURRENT_ANSWER_CORRECTION_CANDIDATE` W-1 — `meoclass1/oralnotes/miw-notes-mgmt-p15.html:432`.**
States the MS Act 2025 repeals the 1958 Act *"(retaining only limited savings under
Part XIV)"*. Part XIV is not a savings provision — it is the substantive coasting-trade
licensing Part. The sentence reads as though Part XIV were a transitional clause.

**`CURRENT_ANSWER_CORRECTION_CANDIDATE` W-2 (class) — "Part XIV" is live with two
different meanings.**

| Page | Meaning used |
|---|---|
| `QB5_A.html:1493`, `QB9_E.html:642,645` | **2025** Act Part XIV = *Offences and Penalties* |
| `QB9_D.html:1103,1132`, `simon-notes-p3.html:1258`, `simon-notes-p6.html:535` | **1958** Act Part XIV = the surviving Part |
| `QB10_A.html:196`, `simon-notes-p2.html:1116` | 1958 Act Part XIV = coasting trade ✓ correct and complete |

A candidate reading QB9_D ("the 1958 Act stands repealed except Part XIV") and then
QB9_E ("MS Act 2025, Part XIV (Offences and Penalties)") has no way to know these are
different statutes. This is the **cross-product inconsistency** class — the same
defect shape as the MEPC ES.2 finding, where four pages were wrong while four others
were right. Recommended remedy is a naming convention, always qualifying the Act.

Both are reported only. **Nothing was edited.**

---

## X. Temporal pilot — Merchant Shipping Act

**WHAT STILL STANDS.** The five sittings are real and I verified them in Phase 2. The
recurrence is genuine. The `DO NOT WRITE TODAY` construction is sound. Commencement is
now primary-verified: 15 March 2026 by S.O. 1244(E).

**WHAT CHANGED.** Part XIV is *not* wreck and salvage — so the surviving Part has
nothing to do with casualty, inquiry, wreck or salvage, and every one of those regimes
is repealed. The exam consequence is therefore *larger*, not smaller, than the
secondary reading suggested.

**DO NOT WRITE TODAY** — *"under section 358 of the Merchant Shipping Act, 1958"* as
the current source of the casualty-reporting duty; *"the marine board is constituted
under the 1958 Act"*; any abandonment answer resting on Part XIII; and — my addition —
*"the 1958 Act survives as Part XIV"* stated without naming the Coastal Shipping Act.

**STATE TODAY** — the duty arises under the Merchant Shipping Act, 2025, in force
15 March 2026 by S.O. 1244(E). Historical positions must be dated: *"under the 1958
Act, which governed until 15 March 2026"*.

**ANSWER IMPACT: MAJOR.** Agreed — the answer's structure survives, its statutory
authority does not.

**Gate agreed, but attach it to the right family (§S):** the 1958 Part XII → 2025 Act
section mapping is **not done**, and the casualty family must not advance to candidate
use until it is. That family is **EM-0009**.

---

## Y. Verified-sitting prototype (Type A) — APPROVED in shape

*"ASKED BEFORE — WHAT CHANGED FOR TODAY?"* is used only where `C36`–`C38` are
satisfied by dated evidence. Months and years are listed individually and derived
from occurrence records rather than typed; "most recent appearance" is evidenced.
Frequency is never asserted beyond the enumerated list, so the wording cannot
overstate it. Correct.

---

## Z. Bank-only prototype (Type B) — CANDIDATE-SAFE. My Phase-2 recommendation adopted and improved.

Heading **"IN THE OFFICIAL QUESTION BANK"**; body *"This question appears in the
Directorate General of Shipping's own published Question Bank for MEO Class I, in
almost the same words"*; and an explicit **"What it does not mean: we cannot say when,
or whether, it has been set at a sitting."**

`PROTOTYPE_EVIDENCE_CLASSES.md` carries an explicit forbidden-vocabulary table —
*asked before, any year or month, asked N times, due again, overdue, revival, returns,
dormant, not asked since, last seen* — each with the reason it leaks. **None of them
appears in the Type B block.** This is exactly Founder decision 2 from Phase 2,
implemented and then strengthened.

**One housekeeping point:** `CANDIDATE_BLOCK_PROTOTYPES.md` still carries the
superseded Phase-2 Prototype 3, headed *"ASKED BEFORE"* with *"exact repeat"*, and
does not say on its face that `PROTOTYPE_EVIDENCE_CLASSES.md` replaces it. Two
documents, one obsolete, no cross-reference — mark it superseded.

---

## AA. Answer impact — KEEP INTERNAL, translate on surfacing

Unchanged from Phase 2 and I still recommend it. `NONE/MINOR/MODERATE/MAJOR` is
authoring vocabulary, and MIW has been burned before by internal production
vocabulary reaching paid pages. **Recommend: hidden internal field; when it surfaces,
a translated sentence, not a badge and not the raw enum.** A badge invites comparison
between questions and turns a judgement into a score. Not implemented; nothing built.

---

## AB. 2010–2012 — still unsupported, and the route is correctly closed

Desktop adopted my finding verbatim and my figures reproduce: **11,917 archived DGS
URLs, 832 mentioning MEO, 12 MEO Class I files, all c. Oct 2013 – Sept 2015, zero
from 2010–2012.**

`WATCH_REGISTER.md` §"The 2010–2012 route is closed" now states explicitly that the
archive *"does not"* attack the H1–H5 dates and that Phase 3A *"stops claiming it
does"*. **No research document still asserts otherwise.** H1–H5 dates remain
unsupported, exactly as Phase 2 left them.

The one residue is **L-3**: the filenames still say `JUN2010`, `DEC2011`, `OCT2012`,
`APR2010`, `MAR2010`.

---

## AC. Phase 3B order — AGREE with the Founder's A → B → C

The proposed order is right, and §V sharpens why **A must come first**: the Part XIV
correction shows the statutory picture is not a single clean repeal, and the Coastal
Shipping Act interaction is still unmapped. Temporal translation built on an
incomplete repeal map would propagate into every Indian-law family at once.

One refinement: **A should be scoped to the 1958 Part XII → 2025 Act mapping plus the
CSA 2025 interaction**, not the whole Act. That is what EM-0009 needs and it is
bounded. The rest of the Act can wait for the families that touch it.

**B** — the 12 dated official Class I files — is the right second step and is
genuinely new dated evidence. **C** — do **not** blindly process 832 URLs; classify
first (707 `.doc` / 120 `.pdf`, many `_wo` result notices rather than question
papers), then extract.

---

## AD. NTA — CLOSE permanently, reopen only on new primary evidence

`CLOSED_NO_EVIDENCE` is right and the reasoning is now stronger than the absence of
evidence. The official bank supplies a **mundane, documented mechanism** for the
long-run recurrence the rumour was invented to explain — 45 exact/near matches across
29 of 40 papers is exactly what a published question bank produces. 11,917 archived
DGS URLs enumerated, no NTA reference.

**Recommend: close the active investigation permanently.** Reopen only on new primary
signal. No setter speculation may ever go candidate-facing.

---

## AE. DieselShip — CONFIRM DO NOT PURCHASE

The value proposition is weaker again. A paid third-party aggregation sits at a
**strictly lower provenance tier** than the Directorate's own published bank, carries
no verifiable sitting dates, and reintroduces the unpreservable-third-party problem
Scribd already caused. The archive supplies 12 official dated Class I papers for
nothing. **No login, no purchase.**

---

## AF. Source storage — approve the extract, defer the binary

Desktop's proposed `meoclass1/pastpapers/sources/official/dgshipping/` fits existing
governance: under `pastpapers`, already outside the deploy, and it does **not**
create a duplicate architecture — `SOURCE_MANIFEST.json` remains the single index.

- **A · extracted JSON — COMMIT.** Proven necessary (§N), reproducible from the
  manifest, no licensing or security concern.
- **B · official PDF binary — DEFER.** The manifest recipe re-obtains and re-verifies
  it on demand; I have now done so twice, on two different days, hash-exact. Settle
  LFS and `.vercelignore` first.
- **C · manifest / hash — ALREADY CORRECT.** `retrieved_via_url` is the
  machine-independent recipe my Phase-2 review required, and it works.

Keep the raw PDF in the git-ignored intake store **and mirror it to a second physical
location** — it is still single-copy on one machine.

---

## AG. Validation — reproduced, with one escape and two novel gaps

| | Desktop | Laptop, branch as committed | Laptop + extract |
|---|---|---|---|
| Validator checks | 169 (brief) / 151 (register) | **166 + 2 skipped** | **169** |
| Failures | 0 | **0** | **0** |
| Similarity controls | 21 | **21, 0 failures** | 21 |
| Validator mutations | 33, 0 escapes | **33, 1 ESCAPE** | **33, 0 escapes** |

*(The register's "151" is stale against its own final state; the brief's "169" is the
with-extract figure. Reported for accuracy, not as a defect.)*

### My own corruptions — 6 designed, 4 caught, 2 genuine escapes

My first harness was **dead** — it copied only `v2`, breaking the tool's `SPECS`
resolution, so every corruption "escaped". A positive control caught it. Re-run
in-process against the real `validate()` (specs=360, extract=185, positive control
fires):

| | Corruption | Result |
|---|---|---|
| **LC-1** | duplicate occurrence id, list length unchanged | **CAUGHT** — `C13`, `C26`, `C27` |
| **LC-2** | bank id valid and unique, text copied from another *real* item | **CAUGHT** — `C32` *(only with the extract)* |
| **LC-3** | **two families SWAP ancestors** — every id real, every text real, nothing dangling | **ESCAPED** |
| **LC-4** | valid dated source, question reference swapped to a real other question | **CAUGHT** — `C7`, `C8` |
| **LC-5** | **historical stem actor inverted** CE → PSC officer, all ids intact | **ESCAPED** |
| **LC-6b** | all 21 occurrences of the date-bearing families re-sourced to the bank | **CAUGHT** — `C36`, `C37`, `C38` |

§33 is satisfied — four independent corruptions are caught by an appropriate guard.

**P3A-5 (MEDIUM) — LC-3, no ancestor-fit check.** The validator proves an ancestor
*exists*, is *unique*, and its text *matches the official extract*. Nothing checks it
is the *right* ancestor for that family. **This is not hypothetical: the identical
error is live in the branch right now** — the EM-0008/EM-0009 mislabel in §S — and it
is the error Desktop already made once when it first serialised EM-0008. A cheap
guard exists: require the family's `canonical_core_ask` to reach at least
`SAME_CORE_ASK` against its own bank ancestor under the classifier that now exists.

**P3A-6 (LOW-MEDIUM) — LC-5, `raw_stem` is unvalidated against the source spec.**
Now that actor is load-bearing in the classifier, an unverified actor inside the
preserved historical stem is a real hole. `C7`/`C8` validate limb and marks against
the spec; the stem text itself is not.

---

## AH. Research integration decision — **A. Still branch-only.**

**Do not merge Phase 3A to main.** Of the four things a merge would bless, three are
where I found defects: the classifier (§F, four defects), the tools' portability
(§O, unrunnable here), and the write-ups (§S, wrong family named twice). Integrating
now would bless exactly the weakest components, which is the same reasoning that kept
Phase 2 on its branch.

Rejecting B (infrastructure/schema/tools only): the tools are the portability defect.
Rejecting C (full research tree): the write-ups carry a live family mislabel.

The branch is purely additive, nothing is on a delivery path, and nothing is
candidate-facing — so there is no cost to leaving it in place and a real cost to
merging for convenience. **Fix the six items on the Phase-3A branch, then merge.**

---

## AI–AL. Boundaries

- **AI · Candidate-facing:** `NOT PUBLISHED`. Nothing wired to solvedQP, no spec, no
  Exam Plan, no HTML. Confirmed by diff.
- **AJ · Bullet Exam Plan:** **untouched.** 0 files under `pastpapers/specs/` in the
  diff. QI-v2 only ever *reads* `subparts[]`.
- **AK · Commercial:** **untouched.** 0 payment, entitlement, refund, Razorpay or
  pricing files in the diff. Refund logic not modified.
- **AL · Magazine:** **untouched.** Separate repo; 0 files in the diff.

---

## AM. Files / git

- Review branch `review/question-intelligence-v2-phase3a`, cut from `origin/main`
  at `3b55bfb`.
- One file added: this report. No existing file modified. `main` untouched.
  Phase 3A not merged, not rebased, no force push.
- Review worktree at `17ad3cf` removed; both repos verified clean.

## AN. Review branch remote proof

Pushed, and verified with `git ls-remote --heads origin`. See the session transcript
for the confirming output. **The Phase-2 failure does not repeat.**

---

## AO. Founder decisions (5)

1. **Commit the extracted bank JSON, and make the tools repo-relative (§N, §O).**
   Approve committing `dgs_meo_cl1_bank_items.json` (~53 KB) under
   `meoclass1/pastpapers/sources/official/dgshipping/`, and fixing the four hardcoded
   `D:` paths — `SPECS` especially, which points off-machine at committed repo
   content? Measured effect: 166→169 checks, 2 skips→0, **1 mutation escape→0**.
2. **Repair demand aggregation before any scaling (§F, P3A-1).** Require
   `demand_compatibility` to be governed by the primary command verb rather than
   `max()` over all demands, so a shared `RESPONSIBILITY` or `PROCEDURAL_ACTION`
   cannot neutralise *describe* vs *criticise*? This is L-4 partially reopened and it
   is the single highest-risk item for bulk ingestion.
3. **Negation and technical magnitudes (§F, P3A-3/P3A-4).** Add a
   required/not-required polarity feature and widen `numbers()` beyond integers 1–20
   to cover decimals and technical values — or explicitly accept the gap and bound
   the sweep to stems without them? As it stands, sulphur `0.50` vs `0.10` reads as
   an exact repeat.
4. **Ancestor-fit guard (§AG, P3A-5).** Require each family's `canonical_core_ask` to
   reach `SAME_CORE_ASK` against its own bank ancestor, so an ancestor swap fails —
   given the EM-0008/EM-0009 mislabel is live in the branch today?
5. **Coastal Shipping Act, 2025 (§V).** Authorise adding it to
   `MERCHANT_SHIPPING_ACT_AUTHORITY.md` before the MS Act temporal pilot is relied
   on, since it repeals the very Part that document says survives?

---

## AP. Next action

**One bounded repair phase — Phase 3A.1 — on the existing branch. Not Phase 3B.**

> **DESKTOP CLAUDE — BEGIN QUESTION INTELLIGENCE V2 PHASE 3A.1: MAKE THE MODEL
> REPRODUCIBLE FROM A CLEAN CHECKOUT AND CLOSE THE SIX RESIDUAL DEFECTS. COMMIT THE
> EXTRACTED BANK JSON AND REPLACE EVERY `D:` PATH WITH A REPO-RELATIVE ONE; FIX
> `demand_compatibility` SO THE PRIMARY COMMAND VERB GOVERNS; ADD NEGATION AND
> TECHNICAL-MAGNITUDE FEATURES; MASK `state of X` GENERALLY; ADD AN ANCESTOR-FIT
> CHECK; CORRECT THE FAMILY-EM-0008/0009 MISLABEL IN THE TWO WRITE-UPS; DE-DATE THE
> H1–H5 FILENAMES; AND ADD THE COASTAL SHIPPING ACT 2025 TO THE AUTHORITY DOCUMENT.
> NO BULK INGESTION, NO CANDIDATE PUBLICATION.**

Every item is bounded, none is architectural, and all eight are testable. Phase 3B
should follow immediately after, in the Founder's A → B → C order.

---

## AQ. Verdict

# HOLD — QUESTION INTELLIGENCE V2 PHASE 3A NEEDS ONE MORE BOUNDED REPAIR

This is not a failure and it is close to a GO. Phase 3A did the hard thing well: it
collapsed three drifted classifiers into one, made examiner demand and actor genuinely
load-bearing, moved the short-stem floor to where it belongs, made date confidence
derived rather than asserted, and repaired the item-182 parser fault — and **I
verified every one of those independently, from a re-downloaded source, with tools
that share no failure mode with Desktop's.** All six of my Phase-2 adversarial cases
now fail correctly. The 45-match set, the 48/144 Paper DNA, the 21 controls and the
33 mutations all reproduce. The Part XIV correction is right and it matters.

The HOLD rests on the Founder's own gates, in the Founder's own words:

- *"THE BANK EXTRACT MUST BE PORTABLE ENOUGH FOR BOTH MACHINES TO VALIDATE"* — it is
  not. Two checks skip, **one mutation escapes**, and two of the three tools will not
  run at all on this machine.
- *"DO NOT SCALE UNTIL LAPTOP CAN REPRODUCE THE MODEL FROM A CLEAN WORKTREE"* — I
  could not, without editing the tools.
- *"COMMAND WORDS MUST MATTER"* — they do, until a shared secondary demand lets
  `Describe` and `Criticise` score **1.00**.

None of these is architectural, all are bounded, and the layer is safer than it has
ever been. But the whole purpose of Phase 3A was to harden the model *before* bulk
historical ingestion, and a classifier that still calls *describe* and *criticise* the
same question whenever the stem also says *"responsibilities of"* is not yet ready to
be pointed at hundreds of unadjudicated historical stems.

The governing principle from Phase 2 still holds, and Phase 3A strengthened it:
**question recurrence is high while date confidence is zero, and the model now says so
by construction rather than by discipline.**
