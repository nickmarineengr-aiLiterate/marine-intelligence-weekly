# 2026 SIX-PAPER INTELLIGENCE REVIEW + V1 DECISION REGISTER

**Review session, 2026-08-09.** Branch `pastpapers/2026-v1-product-review`, cut from `0c6932a`.
The 2026 production set is complete and closed: **6 papers, 54 questions, 0 class A blocking flags.**

Every number in this document is **derived from the canonical specs at review time**, not transcribed
from an earlier document. Where a figure disagrees with an older note, the derivation wins and the
disagreement is called out.

Three labels are used throughout and are not interchangeable:

| Label | Meaning |
|---|---|
| **FACT** | Measured from `specs/*.json`. Reproducible by re-running the derivation. |
| **INTERPRETATION** | MIW's reading of the facts. Arguable. |
| **RECOMMENDATION** | A proposed Founder decision. Nothing here is self-executing. |

---

## 1. DATASET — FACT

| | |
|---|---|
| Papers | **6** — QP2601, QP2602, QP2603, QP2604, QP2606, QP2607 |
| Questions | **54**, nine per paper, no exceptions |
| Months present | January, February, March, April, June, July 2026 |
| Month absent | **May.** Not "not yet built" — the sitting does not exist. The examiner's own 2025 serials run `EM–2501…2504, 2506…2512` with **nothing at 2505**, and May is absent in both years. |
| Marks | Every question recorded at **16**; six answered questions total **96** against a printed **Total Marks 100** |
| Blocking flags | **0** across all six papers |
| Re-verification flags | **110 total: 0 class A, 45 class B, 65 class C** |

### The 96-vs-100 discrepancy — FACT

The discrepancy is **printed on the source copy** and is not a transcription error. Instruction 2
states all questions carry equal marks; six answers are required; the printed total is 100. Six ×
16 = 96. It is recorded in each spec's `marks_note` and rendered on the paper page, the year sheet
and the sample.

**RECOMMENDATION — leave it exactly as it is.** Normalising to 16.67 would invent a figure the
examiner never printed, and rounding to make it total 100 would misstate the paper. The candidate
is better served by seeing the discrepancy than by seeing tidy arithmetic MIW made up.

### Source anomalies — FACT

- QP2604 prints limb marks on **all nine** questions, and **Q6 alone prints (5)+(5)+(5)+(5) = 20**
  against a 16-mark question. Recorded as printed; sub-part marks are `null`. **A future session
  must not "fix" this.**
- Filename inconsistencies (`06- JUNE - 2026.pdf`, `OCTOBER - 2025.pdf`, `DECEMBER  - 2025.pdf`)
  are recorded and not renamed.
- QP2606 carries `SOLAS ch.ll-1` with a double-L, a mismatched quote on `"Andaman and Nicobar
  Islands'`, and unhyphenated "York Antwerp". All reproduced from the source, verified twice.

---

## 2. RECURRENCE — AND A DEFECT IN HOW IT IS CURRENTLY EXPRESSED

### 2.1 The authoring field is not a candidate-facing field — FACT

`recurrence_class` records what was true **when the question was built**. Production order is not
sitting order, and on three of 54 questions the two now disagree outright:

| Question | Sitting | Stored `recurrence_class` | Chronological truth |
|---|---|---|---|
| QP2601-Q3 | **January** | `near_recurrence` | **First occurrence** in its family |
| QP2602-Q3 | **February** | `near_recurrence` | **First occurrence** in its family |
| QP2607-Q1 | **July** | `new` | **A repeat** — the task was set in February, March and April first |

The cause is benign: QP2607 was the pilot and was built first, so January and February questions
correctly record that their *answers* were derived from the July object. But `reused_from` is an
**authoring lineage pointer**, not a chronological one.

> **INTERPRETATION.** Rendering `recurrence_class` to a candidate tells them, on QP2607-Q1, that a
> question is new when it is the fourth time it has been set; and on QP2601-Q3, that January repeats
> a paper sat six months later. The 2026 year sheet is the first surface where this becomes visible,
> which is exactly what §19 of `CURRENT_STATUS.md` predicted would happen.

**RESOLVED THIS SESSION.** `tools/pastpapers/recurrence_model.py` derives status from `(year, month)`
and nothing else. `reused_from` is consumed as an **undirected** edge. The new year sheet and the
sample both use it. **No spec was changed** — the authoring field is correct for what it records.

### 2.2 Canonical recurrence at six papers — FACT

Computed by union-find over two undirected edge kinds — `reused_from`, and equality of the
normalised printed stem — then ordered by sitting date.

| Chronological status | Count |
|---|---|
| Set once in the canonical set | **33** |
| First occurrence of a family that returns | **8** |
| Repeat, same wording | **4** |
| Repeat, reworded | **9** |

**8 families cover 21 of the 54 questions. 33 are singletons.**

For comparison, the stored authoring vocabulary reads: `topic_recurrence` 26, `new` 14,
`near_recurrence` 10, `exact_recurrence` 4. **The two are answering different questions and both
are correct in their own frame.** Only the chronological one may face a candidate.

### 2.3 The eight families — FACT

| # | Chronological chain | Size |
|---|---|---|
| 1 | Jan Q3 → Apr Q3 → **Jul Q5** — salvage law and general average | 3 |
| 2 | Jan Q4 → Apr Q4 — VLCC total loss, insurance and conventions | 2 |
| 3 | Jan Q6 → **Mar Q4 (exact)** → Apr Q6 — WHO, disease vectors, ship health certification | 3 |
| 4 | Jan Q7 → Apr Q7 — UNCLOS flag-State duties and India's machinery | 2 |
| 5 | Jan Q8 → Apr Q8 — Casualty Investigation Code and VSMC | 2 |
| 6 | Jan Q9 → **Feb Q4 (exact)** → Apr Q9 — human element, STCW, fatigue | 3 |
| 7 | Feb Q3 → **Mar Q8 (exact)** → Apr Q2 → **Jul Q1** — FSA, lithium batteries, ro-ro | 4 |
| 8 | Feb Q7 → **Mar Q1 (exact)** — entry into force of an IMO convention | 2 |

**INTERPRETATION — the two structural readings, and no prediction is offered.**

1. **April is a systematic re-issue of January.** Six of April's nine questions (Q3, Q4, Q6, Q7, Q8,
   Q9) sit in a January family, five of them **at the same question number**. That is a fact about
   two papers; it is not a claim about any future sitting.
2. **The exact repeats cluster in consecutive months.** All four fall within a five-week to
   two-month window of their first occurrence. Again: observed, not predicted.

> **No statement of the form "this will appear" occurs anywhere in this document or in any generated
> page.** The permitted form is "appeared in X of the six available sittings".

### 2.4 The host recurrence table must not become candidate-facing — FACT + RECOMMENDATION

Each spec carries a `recurrence` list (`2018/APR`, `2025/SEP/Q6`, `2022/MAR/1`). This is the
**third-party source copy host's own annotation**, and standing policy classes it DISCOVERY ONLY.
The 2026 set proved it wrong in both directions — April's table over-claimed on Q2 and under-claimed
on Q6; June's under-claimed on two.

**FACT, and this is a live finding:** `build_paper.py:435` renders that table into the question card
**outside** the `if not publish:` guard, and `build_index.py:417` renders it on the topic pages. Both
therefore ship to students in a `--publish` build.

> **RECOMMENDATION — FOUNDER DECISION REQUIRED, and it is a publication blocker rather than a
> defect.** A public MIW page should not present another party's analysis as recurrence fact,
> particularly analysis MIW has itself measured to be unreliable, and particularly on a public
> repository. Three options: (a) drop the block in publish mode; (b) keep it but re-label it
> explicitly as an unverified third-party annotation; (c) replace it with the canonical
> `recurrence_model` output, which is MIW's own work.
>
> **MIW recommends (c), falling back to (a).** **Not changed this session** — it alters six approved
> paper pages, and the brief reserves content-policy changes for the Founder. The two NEW products
> built this session already carry (c) and never emit the host table.

---

## 3. ANSWER LENGTH — THE DECISION IS NOW RIPE, AND THE ANSWER IS NOT A WORD COUNT

### 3.1 Measured — FACT

| | QP2607 | QP2601 | QP2602 | QP2603 | QP2604 | QP2606 |
|---|---|---|---|---|---|---|
| Mean words | 632 | 844 | 925 | 864 | 984 | **1334** |
| Median | 640 | 827 | 933 | 860 | 962 | **1394** |
| Range | 572–709 | 744–981 | 829–1022 | 745–953 | 771–1238 | 1010–1516 |
| `understand_first` | 6/9 | **9/9** | 7/9 | 6/9 | 8/9 | 6/9 |
| Route steps, mean | 5.8 | 6.0 | 6.0 | 5.9 | 5.8 | **7.1** |
| Core points, mean | 24.3 | 30.2 | 30.3 | 30.9 | 31.6 | **41.1** |
| Flashcards, mean | 6.6 | 9.8 | 7.6 | 8.4 | 9.6 | 9.8 |
| Printed limbs, mean | 1.2 | 1.9 | 1.4 | 1.4 | 2.6 | 1.6 |
| Re-verify A/B/C | 0/4/2 | 0/6/8 | 0/7/12 | 0/9/10 | 0/9/10 | 0/12/15 |

**All 54: mean 931, median 905, range 572–1516, σ 241.**
**47 of 54 questions fall outside the 450–650 band** (45 raise warnings; QP2607's two are recorded
as accepted exceptions, so the totals reconcile with `CURRENT_STATUS.md` §7).

### 3.2 Is June drift? — FACT settles it

Correlation of answer length against four candidate explanatory variables, over all 54 questions:

| Against | Correlation |
|---|---|
| Printed limbs | **0.103** |
| Route steps | 0.432 |
| Named sub-tasks | 0.560 |
| **Core points** | **0.827** |

**INTERPRETATION.** June is **not** drift. Its answers are ~41% longer than the set mean and carry
~34% more core points and 22% more route steps; length and substance rose together, which is the
signature of a harder paper rather than looser prose. June also had **five questions with no
reusable material at all**, so every proposition had to be stated rather than inherited.

The per-**printed-limb** band that February and March proposed is **not supported**: correlation
0.103, and six of nine March questions print no limb marks at all. The per-**named-sub-task** band
that April and June proposed is better but still moderate at 0.560.

### 3.3 Words per core point — FACT

| | |
|---|---|
| Mean | **29.6** words per core point |
| Median | 29.4 |
| σ | 4.23 |
| Range | 20.2 – 40.9 |

| Candidate band | Questions outside |
|---|---|
| 450–650 words (current) | **47 / 54** |
| 20–34 words per core point | 8 / 54 |
| **20–36 words per core point** | **3 / 54** |
| mean ± 2σ (21.1–38.0) | 4 / 54 |

### 3.4 RECOMMENDATION — replace the fixed band with a density band

> **Retire the 450–650 fixed word band. Replace it with a review warning at
> `< 20` or `> 36` words per core point`, evaluated per question.**

Why this shape and not another:

- **It is complexity-aware without being a quota.** A question with more to say earns more words,
  automatically. That is what the Founder asked for and what a fixed band structurally cannot do.
- **It cannot be gamed in the direction that matters.** Padding raises words without raising core
  points and pushes the question *out* of band. Inventing core points to buy words is caught by the
  existing `validate_spec.py` rule that route steps and answer headings must correspond.
- **It fits every paper**, including the two extremes: QP2607 (632 mean) and QP2606 (1334 mean) both
  sit inside it. No paper needs an exception.
- **It turns the warning stream back into signal.** 47 warnings become 3, and those 3 are worth a
  human look rather than being scrolled past.
- **Tables are handled.** March's objection — that Q6's ~150-word comparison table *is* limb (a) in
  compact form — dissolves, because a table's propositions are core points like any other.

**This is a validator change and is therefore a Founder decision. No validator change was made this
session.** The three questions that would fall outside the new band should be looked at once, on
their merits, rather than trimmed to a number.

---

## 4. `understand_first` — FACT + RECOMMENDATION

Design says CONDITIONAL: present only where the topic is counter-intuitive.

**FACT.** The four papers that applied the conditional test explicitly landed at **6/9, 7/9, 6/9 and
6/9**. The one paper that did not apply it landed at **9/9** (QP2601). April's 8/9 is **partly
inherited** — its two new questions are 2/2 and five of the remaining six inherit January's.

**INTERPRETATION.** The drift is real, it is specific to QP2601, and it needs an explicit check every
time rather than instinct — four papers now demonstrate that.

**RECOMMENDATION — SMALL CHANGE, on QP2601 only.** Prune QP2601's `understand_first` to the questions
that genuinely need it, which automatically improves five QP2604 questions that inherit from it.
**Do not normalise counts for aesthetics** and do not touch the other four papers, which applied the
test correctly. **Not done this session:** it edits five approved specs and needs the Founder's eye
on which three or four blocks are genuinely redundant.

Note that the Understand *tab* renders on all nine cards regardless — it carries the derived
knowledge map, which is always present. Pruning removes clutter without emptying a mode.

---

## 5. ROUTES, CORE POINTS, FLASHCARDS — FACT + VERDICT

| | Mean | Median | Range |
|---|---|---|---|
| Route steps | 6.1 | 6 | 5 – 8 |
| Core points | 31.4 | 31 | 20 – 52 |
| Flashcards | 8.6 | 9 | 6 – 10 |

**These are DESCRIPTIVE. They are not quotas and must not become quotas.** A question with five clean
steps is not deficient against one with eight.

**VERDICT on the organising principle — REMEMBER THE ROUTE · COVER THE CORE POINTS · RETRIEVE WITH
CARDS: it survived six papers intact.** The evidence is that the spine held under every structural
shock the set produced — a six-limb legal question, a four-task institutional question, three
simultaneous exact recurrences, a question requiring two editions of one instrument at once, and a
question sitting substantially outside the regulatory corpus. In no case was a second route needed,
and the derived layers (knowledge map, recall skeleton, exam plan, rapid-revision line) never had to
be authored separately.

---

## 6. FIVE-MODE VERDICT

| Mode | Verdict | Reason |
|---|---|---|
| **Understand** | **KEEP · SMALL REFINE** | Keep the mode. Refine only the optional `understand_first` block on QP2601 (§4). The knowledge map carries the mode regardless. |
| **Exam Plan** | **KEEP — FREEZE** | Derived from the one canonical route; no drift in six papers. It is also the layer that carries the commercial argument on the free sample. |
| **Answer** | **KEEP — FREEZE, remains the default** | No evidence argues otherwise. Length policy changes (§3); the mode does not. |
| **Study Guide** | **KEEP — FREEZE** | The six-section spine plus an `Uncertainty…` section absorbed all six papers. It is where the three-layer rule sends explanation, and every layering pass this year relied on it. |
| **Recall** | **KEEP — FREEZE** | Blank skeleton derived from the route; no authored duplicate. |

**NO SIXTH MODE.** Verification is a capability, not a way of studying — `MIW_TRUE_SOURCE_CONTRACT.md`
§1. Reconfirmed, and nothing in six papers challenged it.

---

## 7. ARCHETYPES AND TAXONOMY — FACT + VERDICT

**Archetypes (5, closed):** `explain` 23 · `legal` 15 · `procedure` 10 · `evaluate` 4 · `compare` 2.

**Primary categories (7, closed):** Statutory Framework & Class 16 · Marine Insurance & Commercial
Law 10 · Human Element & Management 8 · Pollution Prevention & Response 7 · Alternative Fuels &
Decarbonisation 5 · Cargo & Bulk Carriage 5 · Indian Maritime Legislation 3.

**Reuse tiers:** B 27 · C 14 · D 13.

**VERDICT — no schema or category expansion was required by any of the six papers, and none is
recommended.** Five consecutive papers were built on the frozen template with **zero schema
changes**. `compare` at 2 and `Indian Maritime Legislation` at 3 are thin but real; thinness is not
a defect, and merging them would lose a distinction the corpus actually uses.

What *did* extend, exactly as designed, is the open secondary `subject_tags` vocabulary, which now
carries **29 distinct values** — grown a few at a time by each paper (Limitation of Liability,
General Average, Treaty Law, Fire Safety, Cargo Securing, War Risks, Ship Recycling, Salvage Law,
Biofouling, Port State Control, Ship Economics, and six added by QP2601). **That is the vocabulary
working, not straining.**

> **Do not confuse a writing mistake with a schema defect.** Every anomaly the year produced — the
> printed-marks contradiction, the sitting-relative prose, the changed governing statute, the
> two-editions question — was absorbed by the existing object.

---

## 8. V1 FOUNDER DECISION REGISTER

`FREEZE` = settled, do not reopen without test evidence. `SMALL CHANGE` = do it, scoped.
`DEFER TO V1.1` = real, not now.

| # | Item | Verdict | Note |
|---|---|---|---|
| 1 | **Answer-length control** | **SMALL CHANGE** | Retire 450–650. Adopt **20–36 words per core point** (§3). Validator change = Founder decision. |
| 2 | **`understand_first`** | **SMALL CHANGE** | Prune QP2601 only; five QP2604 questions improve automatically (§4). |
| 3 | **Route structure** | **FREEZE** | One canonical `answer_route`; everything derived. Six papers, no failure. |
| 4 | **Core points** | **FREEZE (descriptive)** | Never a quota. Now load-bearing as the length denominator (§3). |
| 5 | **Flashcards** | **FREEZE** | ≥4, stable ids. Mean 8.6, no drift. |
| 6 | **Recurrence model** | **SMALL CHANGE — DONE** | Chronology derived from the calendar in `recurrence_model.py`. Specs unchanged. |
| 7 | **Host recurrence table on public pages** | **DEFER — FOUNDER DECISION, publication blocker** | Currently ships in `--publish` (§2.4). New products already exclude it. |
| 8 | **Exact reuse (Tier D)** | **FREEZE** | One question → one canonical route. The three mandatory reuse steps stay mandatory. |
| 9 | **Sitting-context sweep** | **FREEZE — permanent** | Caught a miss in March and again in April; ~385 hits adjudicated clean in June. Every hit needs human adjudication (April: 55 hits, 1 defect). |
| 10 | **Search payload split** | **DEFER TO V1.1** | Threshold reached and measured: `index.html` 181.4 KB, payload 134.9 KB (74%). **No observable problem at six papers.** Recommend deferring to a measured UX trigger, not splitting on a number. |
| 11 | **Mobile sticky chrome** | **DEFER TO V1.1** | Pre-existing on paper pages (51–60.5% at 375px). Not a regression from any paper. **The new year sheet was built and then fixed to 31.7%**, so the pattern is understood and cheap to apply when the Founder authorises chrome work. |
| 12 | **Category taxonomy** | **FREEZE** | 5 archetypes, 7 primary categories, open secondary tags (§7). |
| 13 | **Reference Shelf** | **FREEZE — stays empty** | No placeholders until a real resolvable corpus object exists. |
| 14 | **True Source linking** | **FREEZE (seam only)** | `reference_href()` remains a seam. No viewer, resolver, auth or watermarking. |
| 15 | **Questions-only year sheet** | **SMALL CHANGE — DONE** | Built, generic across years, tested (§ new products). Free/paid placement is a Founder decision — MIW recommends free. |
| 16 | **Solved QP free sample** | **SMALL CHANGE — DONE** | Built from a projection config, two full demos, seven previews, leak-tested. Awaiting Founder review. |
| 17 | **Solved QP pricing** | **BLOCKED — FOUNDER ONLY** | `PRICE_TBD`. The generator refuses to render a currency value while it is unset. |

---

## 9. TRUE SOURCE — SIX-PAPER EVIDENCE RANKING

Aggregated from the six `QP26xx_TRUE_SOURCE_DEMAND_MAP.md` files, with the coverage count
**re-derived from the specs** rather than taken from the narratives.

### 9.1 Instrument coverage — FACT

| Instrument | Papers | |
|---|---|---|
| **SOLAS** | **6/6** | *the Founder's assumption is confirmed* |
| **MARPOL** | **6/6** | |
| **STCW** | **6/6** | |
| **ISM Code** | **6/6** | |
| **Marine Insurance Act, 1963 (India)** | **6/6** | |
| **Merchant Shipping Act (1958 and/or 2025)** | **6/6** | |
| York-Antwerp Rules | 5/6 | |
| UNCLOS | 5/6 | |
| IMSBC Code | 5/6 | |
| FSA Guidelines (MSC-MEPC.2/Circ.12/Rev.2) | 5/6 | |
| LLMC · Casualty Investigation Code · CLC · Bunkers Convention | 4/6 each | |
| Salvage Convention 1989 · IHR 2005 · **FSS Code** | 3/6 each | |
| BWM Convention | 2/6 | |
| Hong Kong Convention · AFS Convention | 1/6 each | |
| **LSA Code** | **0/6** | |

> **Read this as breadth of touch, not as load-bearing primary demand.** It counts any appearance
> anywhere in a spec, including study guides and search aliases. The demand maps' `P` / `S` / `C`
> classification remains the authority on what an answer actually *turns on*. The two agree on the
> top of the table, which is why it is usable.

### 9.2 Priorities — RECOMMENDATION

**FULL CORPUS, in order:**

1. **SOLAS** — 6/6, licence-gated, and it blocked a P1 claim on more questions than anything else.
   Chapter II-1, II-2, VI, VII, IX and XI-1 are all demanded at regulation level. **The single
   highest-value acquisition in the series.**
2. **MARPOL** — 6/6, and April raised the resolution requirement: objects must resolve to the
   **Articles** of the parent Convention down to the third sub-paragraph level (`16(2)(f)(iii)`),
   not merely to Annex/regulation.
3. **Marine Insurance Act, 1963 (India)** — 6/6, freely available on India Code, and **only s.66 has
   ever been verified against primary statutory text.** The cheapest high-value unblock on the list.
4. **IMSBC Code (07-23 and 08-25)** — 5/6, licence-gated, and the standing blocker on every cargo
   question.
5. **STCW** and **ISM Code** — 6/6 each; STCW is licence-gated, ISM largely reproducible.

**REFERENCE PACK:** Merchant Shipping Act 2025 (Gazette copy already read) · York-Antwerp Rules
(**edition-keyed — see below**) · IACS/RO Code · FSA Guidelines · A.1206(34) and A.1207(34) ·
MSC-FAL.1/Circ.3/Rev.3 · Salvage/SCOPIC/LOF contract forms.

**LICENSED ACQUISITION REQUIRED:** SOLAS · IMSBC · STCW · CSS Code · IGF Code · 2011 ESP Code ·
IMDG · AFS Convention · York-Antwerp Rules (both editions) · IACS Common Structural Rules.

**FACT worth surfacing: the LSA Code has ZERO demand across all six 2026 written papers, and the FSS
Code only 3/6.** Memory records an LSA/FSS corpus consolidation package as complete. That work is not
wasted — it presumably serves the oral Question Bank — but **it should not be counted as progress
against written-paper demand**, and the next corpus increment should go to SOLAS rather than to more
LSA/FSS depth.

### 9.3 Corpus object-model requirements the year produced — FACT

Five requirements, each forced by a specific question and none of them optional:

1. **Editions must be first-class objects with a diff relationship** (June Q3). A store holding "the
   York-Antwerp Rules" as current text plus an edition tag **cannot answer** a question that names
   the 1994 edition and requires 2016 to contrast it.
2. **A "live external list" state**, five instances: Joint War Committee Listed Areas, authorised
   Indian ports for ship sanitation certificates, EU-approved recycling facilities, national
   biofouling arrival requirements, and the IMO register of designated PSSAs.
3. **A live list needs an ABSENCE relationship** (June Q7). The load-bearing claim is a **negative** —
   that no Indian sea area holds PSSA designation — and a negative decays silently when the list
   changes.
4. **A meeting outcome is not an instrument** (June Q4, HTW 12). Load-bearing, and it has no edition.
5. **Amendment state must be a property, not prose** (February). Tacit acceptance makes LLMC limit
   figures perishable, and "approved but not adopted" is a state the model must be able to hold —
   it was the single most dangerous claim in the February paper.

**Do not start corpus production from this document.** It is the demand side only.

---

## 10. WHAT WAS DELIBERATELY NOT DONE

- **No spec was edited.** All six papers and all six specs are byte-identical to `0c6932a`.
- **No validator change**, so the 47 warnings are unchanged and the decision stays with the Founder.
- **No change to the six generated paper pages**, the index, the topic pages or the manifest.
- **No publication**, no gating, no `noindex` removal, no merge to `main`.
- **No 2025 production.**
- **`SQ/index.html` was not modified** — see `SOLVED_QP_COMMERCIAL_ARCHITECTURE.md` §5 for why, and
  for the exact markup that is ready to apply once pricing and entitlement are approved.
