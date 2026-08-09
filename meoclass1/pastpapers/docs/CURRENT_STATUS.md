# CURRENT STATUS — MEO Class I Written Questions / the complete 2026 set

**Canonical restart document for the Past Written Papers product.**
Last updated: 2026-08-09, at the close of the **QP2606 (June) production** session. Read this first.

> # **THE 2026 PRODUCTION DATASET IS COMPLETE. 6 of 6 available sittings, 54 questions.**
>
> **QP2607 (July)** — frozen V1 template, Founder review candidate.
> **QP2601 (January)** — Founder review candidate, cross-paper validation. **0 class A blocking flags.**
> **QP2602 (February)** — Founder review candidate. **0 class A blocking flags.**
> **QP2603 (March)** — Founder review candidate. **0 class A blocking flags.**
> **QP2604 (April)** — Founder review candidate. **0 class A blocking flags.**
> **QP2606 (June)** — **BUILT AND VERIFIED.** Founder review candidate. **0 class A blocking flags.**
> See **§2f**, `verification/QP2606/` and `docs/QP2606_TRUE_SOURCE_DEMAND_MAP.md`.
>
> **May 2026 does not exist in the source set — and the examiner's own serial numbering confirms
> it.** The 2025 bundle runs `EM–2501 … 2504, 2506 … 2512`, with a gap exactly at **2505**. May is
> absent in both years. Keep it `coming_later`; do not create a QP2605 spec.

> **NEXT SESSION IS A REVIEW SESSION, NOT A PRODUCTION SESSION.** See §18. The six-paper
> intelligence review, the generated ONLY QUESTIONS year sheet, the V1 freeze/refinement decisions
> and the 2025 production strategy are all reserved for it and were deliberately **not** started
> during June production.

> **BRANCH: `pastpapers/qp2606-founder-review`**, created from `5744143` (the QP2604 completion).
> The April, March, February, January and July branches are untouched and preserved.

> **QP2607 IS A FOUNDER REVIEW CANDIDATE.** There are **no class A (blocking) flags left**.
> Q7's two publication blockers were closed against primary Gazette text. What
> remains is four class B currency checks and two class C accepted limitations — see §8.

> **QP2607 V1 TEMPLATE — FROZEN, AND NOW CROSS-PAPER VALIDATED.** See §2a and the new §2b.
> QP2601 was built on the frozen template **without a single schema change**. Two defects were
> found — both in the *test harness and trap layer*, not in the template — and both are fixed.

> Scope note: `AI_SESSION_HANDOVER.md` at the repository root is a *repository bootstrap*
> handover dated 2026-07-30 and is stale. This file is the product-scoped status for Past
> Papers and is the one to trust for this work.

---

## 1. Repository

| | |
|---|---|
| Path | `F:\Marine-Intelligence-Weekly` |
| Remote | `https://github.com/nickmarineengr-aiLiterate/marine-intelligence-weekly.git` |
| **Visibility** | **PUBLIC** — verified via the GitHub API this session (`"private": false`) |
| Branch | **`pastpapers/qp2603-founder-review`** — current working branch, created from `65ae91a` (the QP2602 completion). Follows the established `pastpapers/<paper>-founder-review` convention. |
| Previous branches | `pastpapers/qp2602-founder-review` at `65ae91a`, `pastpapers/qp2601-founder-review` at `f2cd57e` and `pastpapers/em2607-founder-review` at `4230a83` — all three **untouched and preserved**. The July branch NAME deliberately keeps the historical wording; the product identity is QP2607. Do not rename it for cosmetics. |
| Branched from | `main` @ `2bf6e49` (unchanged; nothing merged to main) |
| Push status | **RESOLVED.** Branch pushed and tracking `origin/pastpapers/em2607-founder-review`. |
| Architecture checkpoint | `d078843` — "Build scalable QP series architecture and migrate EM2607 to QP2607" |

All git commands in this repo need `-c safe.directory=*`.

**The public-repository fact drives several decisions below.** Anything committed here is
published, regardless of `noindex`, of which branch it sits on, or of whether the site is
deployed. There is no such thing as a "private" field inside a committed spec.

---

## 2. Product state

**QP2607 (July 2026, Engineering Management, MEO Class I) — all 9 questions built.**

| Output | Path | Nature |
|---|---|---|
| Paper | `meoclass1/pastpapers/QP2607.html` | **generated** — never hand-edit |
| Written Questions index | `meoclass1/pastpapers/index.html` | **generated** |
| 2026 topic coverage | `meoclass1/pastpapers/topics-2026.html` | **generated** |
| Retrieval manifest | `meoclass1/pastpapers/pastpapers_content_index.json` | **generated** (manifest v2.0) |
| Canonical content | `meoclass1/pastpapers/specs/QP2607.json` | **SOURCE OF TRUTH** |
| Known traps | `meoclass1/pastpapers/known_traps.md` | hand-maintained |
| Verification records | `meoclass1/pastpapers/verification/QP2607/*.md` | hand-maintained evidence |
| Local provenance | `meoclass1/pastpapers/verification/LOCAL_SOURCE_PROVENANCE.md` | **git-ignored, local only** |

Everything is FOUNDER REVIEW state: not published, not gated, not indexable.

---

## 2a. QP2607 V1 TEMPLATE FREEZE — 2026-08-08

**QP2607 is frozen as `MIW WRITTEN QUESTIONS — V1 TEMPLATE`.**

```
FIRST-PAPER VALIDATED
CROSS-PAPER VALIDATION STILL REQUIRED
```

One paper validates that the architecture *works*; it does not prove the method universally.
QP2601 exists to test that, and has not been built.

**Frozen at commit `b2535d8` — "Stabilise MIW learning and true-source reference contract".**

### What is frozen

| | |
|---|---|
| Learning modes | **Five, and no more**: Understand · Exam Plan · **Answer (default)** · Study Guide · Recall |
| Spine | one canonical `answer_route`; knowledge map, recall test, exam plan and rapid-revision line are **derived, never authored** |
| Written answer | numbered principal sections matching the route; blank skeleton for recall |
| Remember / Cover | *Remember N route headings · Cover M core points beneath them* — two different targets, stated explicitly |
| Support | flashcards (≥4, stable ids) · Quick / Rapid Revision · optional `understand_first` · optional `memory_cue` |
| Verification | optional `reference_shelf` — **outside the mode selector**, currently empty by design |
| Semantic guard | `SEMANTIC_GUARDS` in `validate_spec.py` — a derived layer may never be more categorical than its source |

**Do not add a sixth mode.** Verification is a capability, not a way of studying — see
`MIW_TRUE_SOURCE_CONTRACT.md` §1.

### Founder decisions recorded this session

**1 — Canonical corpus is separate from the relationship repository.**

The MIW True Source corpus is a **separately governed canonical regulatory-content layer**: source
content, edition, amendment/consolidation state, provenance, effective dates, structured and PDF
representations, canonical section destinations.

`RulesApp/repository/` **is not** to become the physical master store merely because it already
holds regulatory nodes. It is an intelligence and relationship **consumer**. What is reused is its
**logical ID convention** (`MARPOL-VI-14`, `IMSBCCode-4`, `FSSCode-9-2`), which is adequate and was
adopted rather than replaced. One canonical source, many consumers.

Nothing was moved, copied or imported. The other corpus was **not** assumed to be
GitHub-synchronised — it is not checked out on this machine and was not inspected.

**2 — CSS and JS stay inline for QP V1.**

Paper pages are generated, so UI code cannot drift independently of the spec; the repeated payload
is modest at one paper; and shared content-hashed assets previously introduced checkout/CRLF risk.
No measured user problem justifies extraction.

> **REVISIT AFTER MULTI-PAPER REAL-USAGE DATA.** Not before.

### True source demand map

**`docs/QP2607_TRUE_SOURCE_DEMAND_MAP.md`** — the handoff contract to the corpus-production track.

Q1–Q9 object demand classified P / S / C, with both availability axes recorded separately: the
**identity** axis verified against `RulesApp/repository/index/repo-data.json` (78 standards, 1,006
nodes, measured 2026-08-08), and the **corpus** axis honestly `UNKNOWN` because the True Source
store is separately governed and was not inspected.

Headline: **49 primary objects; ≈29% have a stable identity today.** Full-corpus priority
**MARPOL Annex VI → MARPOL Annex I → IMSBC (licence-gated)**; reference-pack priority
**Merchant Shipping Act 2025 → Marine Insurance Act 1963 → IACS/RO Code**. FSS and LSA:
**no direct July demand**.

**`reference_shelf` stays empty** until a real resolvable object exists. No placeholders.

---

## 2b. QP2601 — CROSS-PAPER VALIDATION RESULT, 2026-08-08

**QP2601 (January 2026) is built: all 9 questions, Founder review candidate, 0 blocking flags.**

| Output | Path |
|---|---|
| Paper | `meoclass1/pastpapers/QP2601.html` — **generated** |
| Canonical content | `meoclass1/pastpapers/specs/QP2601.json` — **SOURCE OF TRUTH** |
| Verification records | `meoclass1/pastpapers/verification/QP2601/Q1..Q9.md` + `DEDUP_AND_SOURCE_PLAN.md` |
| True source demand | `docs/QP2601_TRUE_SOURCE_DEMAND_MAP.md` |
| Pattern register | `docs/2026_PATTERN_REGISTER.md` — **new, opened this session** |

### The template held

**No schema change was required.** The frozen question object absorbed a six-limb legal question
(Q3), a four-task institutional question (Q6) and a four-sub-item technical question (Q5) unchanged.
Five modes, one `answer_route`, everything else derived — all held. **No sixth mode. No new
archetype. No new primary category.** `reference_shelf` remains empty on every question.

### Two defects found — both in the harness, not the template

1. **`ui_behaviour_test.cjs` hard-coded QP2607 fixtures while deriving its page list from the specs.**
   Adding a second spec made it run the July assertions against the January page: **17 failures**.
   Fixed by keying probes to `paper_id`, deriving study-state ids from the actual cards, and — the
   important part — **failing loudly when a page has no fixtures**, so a future paper cannot report a
   clean run having tested nothing. This is the same class of defect as the old `glob('EM*.html')`
   lesson in §4. *Add a `FIXTURES` entry whenever a paper is added.*
2. **Known trap 1 fired on correct prose.** Its GREP phrase, `strict liability on the registered
   owner`, is right for the **Nairobi Wreck Removal Convention** and for **CLC channelling** — it is
   only wrong for the Bunkers Convention. The guard was **left at full strength** and the QP2601
   wording changed instead; a scope warning is recorded in `known_traps.md`. If a later paper hits it
   again on correct prose, that is the evidence to move it to `GREP: SKIP`. Not on one paper.

### Regression against QP2607 — clean

`QP2607.html` is **byte-identical** before and after (`a574cd36261778e4`), and `specs/QP2607.json`
has **no diff** against `4230a83`. `index.html`, `topics-2026.html` and the manifest changed, which
is correct — they are multi-paper aggregates that must now include January. Rebuild is deterministic:
all five artefacts byte-identical across two consecutive runs.

### Cross-paper behaviour now demonstrable

- Searching *"general average"* on the index returns **both** `QP2601.html#q3` and `QP2607.html#q5`.
- `topics-2026.html` renders **18 question links, zero duplicates** — the one-primary-category rule
  holds at two papers.
- Study state is namespaced per `question_id`, so January and July progress coexist.

### The one open quality question — for Founder decision

**All 9 QP2601 model answers exceed the 450–650 word band (744–981); July had 2 of 9, ceiling 709.**
A trim pass removed ~400 words by moving explanation into the study guide, where the three-layer rule
puts it, but they remain above band. Part is real — January's questions carry more printed limbs than
July's. Part is authoring drift. **Decide before QP2602 whether the band should be expressed per
limb-count.** Related: `understand_first` was used on **9/9** questions where the design says it is
conditional (July: 6/9). Both are recorded in `docs/2026_PATTERN_REGISTER.md` §4.

---

## 2c. QP2602 — FEBRUARY PRODUCTION RESULT, 2026-08-08

**QP2602 (February 2026) is built: all 9 questions, Founder review candidate, 0 blocking flags.**

| Output | Path |
|---|---|
| Paper | `meoclass1/pastpapers/QP2602.html` — **generated** |
| Canonical content | `meoclass1/pastpapers/specs/QP2602.json` — **SOURCE OF TRUTH** |
| Verification records | `meoclass1/pastpapers/verification/QP2602/Q1..Q9.md` + `DEDUP_AND_SOURCE_PLAN.md` |
| True source demand | `docs/QP2602_TRUE_SOURCE_DEMAND_MAP.md` |
| Pattern register | `docs/2026_PATTERN_REGISTER.md` — **updated to 3 papers / 27 questions** |

### The template held again — second consecutive paper with no schema change

**No schema change was required.** The frozen question object absorbed a three-limb convention
question (Q1, printed 5+5+6), an applied general-average problem requiring a reasoned yes/no with
justification (Q6), and a question **word-for-word identical to one already built on another paper**
(Q4) — all unchanged. Five modes, one `answer_route`, everything else derived. **No sixth mode. No
new archetype. No new primary category.** `reference_shelf` remains empty on every question.

Four new secondary `subject_tags` were added (`Limitation of Liability`, `General Average`,
`Treaty Law`, `Fire Safety`), which the vocabulary explicitly permits.

### The first EXACT recurrence in the set — and how it was handled

**QP2602 Q4 is character-for-character identical to QP2601 Q9.** The same question was set in two
consecutive sittings five weeks apart.

**The verified January answer was reused unchanged rather than re-authored**, because one question
has exactly one canonical route: authoring a second route for an identical question would force a
candidate revising both sittings to reconcile two competing structures under exam pressure. What was
re-done is verification *currency* — the fatigue circular, the STCW amendment state and the review
status were re-checked at the February sitting date and were unchanged. Card ids were re-keyed;
cross-links point back to January.

> **STANDING CONSEQUENCE.** The two question objects are deliberately identical in substance.
> **Any correction made to QP2601 Q9 on Founder review must be applied to QP2602 Q4 as well.**
> Recorded in the spec's `unresolved` list and in `verification/QP2602/Q4.md` so it cannot be lost.

### The headline verification finding

**The IMO Net-Zero Framework was APPROVED but NOT ADOPTED at the February sitting date.** The second
extraordinary session of MEPC (14–17 October 2025) was convened to adopt the draft new MARPOL Annex
VI Chapter 5 and **adjourned for twelve months** on 17 October 2025 without agreement — read on the
IMO's own meeting summary and press briefing.

A large volume of material published between April and October 2025 asserts that the framework would
be adopted in October 2025 and enter into force in 2027. **Any Q8 answer built on that material is
wrong for this sitting.** Same failure mode as January's pre-Manila STCW text and July's "not yet in
force" secondary source on the MS Act 2025 — a correct-looking source describing a superseded state
of affairs, now **3/3 papers**.

A second, smaller correction of the same family was caught: a search summary gave the ro-ro fire
amendments (MSC.550(108), MSC.555(108)) an entry-into-force date of 1 January 2028. They entered into
force **1 January 2026**; 2028 is the *existing-ship* compliance date.

### Sitting-date truth was load-bearing on two more questions

**Q5 and Q9 are answered on the Merchant Shipping Act 1958**, which was in force on the examination
date and was repealed by s.324(1) of the Merchant Shipping Act 2025 with effect from **15 March
2026** — five weeks *after* the paper was sat. The QP2607 Q7 Gazette work paid for itself a second
time. Both study guides carry an explicit current note; both carry a B-class currency flag.

### Regression against QP2607 and QP2601 — clean

`QP2607.html` (`a574cd36261778e4`) and `QP2601.html` (`38b420fc88da8ad4`) are **byte-identical**
before and after, and `specs/QP2607.json` and `specs/QP2601.json` have **no diff**. `index.html`,
`topics-2026.html` and the manifest changed, which is correct — they are multi-paper aggregates that
must now include February. Rebuild is deterministic: all artefacts byte-identical across two
consecutive runs.

### Cross-paper behaviour at three papers

- Searching *"general average"* on the index returns **one question from each of the three
  sittings** — `QP2601-Q3`, `QP2602-Q6`, `QP2607-Q5`.
- `topics-2026.html` renders **27 question links, zero duplicates**, nine per paper.
- The index payload carries **27 questions**. The §4 search-payload threshold — split into a fetched
  JSON file **when the sixth paper is added** — is unchanged and has not been reached.

### One harness fix, one product fix

- `ui_behaviour_test.cjs` gained a `FIXTURES` entry for QP2602, per the standing rule. Its `narrow`
  probe had to be Rule VII's own wording (`damage to machinery and boilers`) because February sets
  general average twice over, so the January probe would not have resolved to one card. **No guard
  was weakened.**
- The first fixture run failed on one alias, which was correct behaviour: `poseidon principles` was
  not in any `search_alias`. **Both sides were fixed properly** — the term was added to Q2's search
  aliases, because a candidate would plausibly search it, and the test alias was changed to a
  genuinely metadata-only term (`annual efficiency ratio`).

### Open quality questions — for Founder decision

**1. The 450–650 word band should be retired or re-derived.** February ran a deliberate three-pass
trim that removed roughly **1,600 words** by moving explanation into the study guide, with no scoring
proposition removed — Q1 1303→1022, Q9 1376→997, Q6 1180→930, Q5 1109→934. It still lands at
**829–1022 (mean 925)**. Across the set, **18 of 27 questions exceed the band and it generates 18 of
the toolchain's 20 warnings.** A band expressed per *printed limb* (≈250–320 words) fits all three
papers. See `2026_PATTERN_REGISTER.md` §4(a).

**2. `understand_first` — January's 9/9 now looks clearly like drift.** February applied the
conditional test explicitly and landed at **7/9**, deliberately omitting Q3 and Q7 because the
knowledge map already carries their structure. Two papers that applied the test: 6/9 and 7/9. The
paper that did not: 9/9. The QP2601 recommendation to prune stands and is better supported.

**3. Mobile sticky chrome is pre-existing, not a February regression.** Measured at 375px: QP2602
**60%** of viewport, QP2601 **60%**, QP2607 **51%**. February matches January exactly; July is lower
only because it generates fewer filter chips (24 filter buttons on the January/February pages). The
"24.8% on mobile" figure in §15 does **not** hold for paper pages and appears to have been measured
on the index. No horizontal overflow on any page at either width. Flagged for Founder review; **not**
fixed this session, because shared chrome is a design change and the brief forbids redesign.

---

## 2d. QP2603 — MARCH PRODUCTION RESULT, 2026-08-08

**QP2603 (March 2026) is built: all 9 questions, Founder review candidate, 0 blocking flags.**

| Output | Path |
|---|---|
| Paper | `meoclass1/pastpapers/QP2603.html` — **generated** |
| Canonical content | `meoclass1/pastpapers/specs/QP2603.json` — **SOURCE OF TRUTH** |
| Verification records | `meoclass1/pastpapers/verification/QP2603/Q1..Q9.md` + `DEDUP_AND_SOURCE_PLAN.md` |
| True source demand | `docs/QP2603_TRUE_SOURCE_DEMAND_MAP.md` |
| Pattern register | `docs/2026_PATTERN_REGISTER.md` — **updated to 4 papers / 36 questions** |

### The template held again — third consecutive paper with no schema change

**No schema change was required.** The frozen question object absorbed **three simultaneous exact
recurrences** (Q1, Q4, Q8), a four-process operational question (Q5), a three-limb
compare-plus-enumerate question (Q6) and a single-stem procedural management question (Q7), all
unchanged. Five modes, one `answer_route`, everything else derived. **No sixth mode. No new
archetype. No new primary category.** `reference_shelf` remains empty on every question.

Three new secondary `subject_tags` were added (`Cargo Securing`, `War Risks`, `Ship Recycling`).

### THE ARCHITECTURE FINDING — an exact question is NOT an exact answer object

**This is the most important outcome of the March session.** February established the reuse rule
with one instance. March applied it three times and exposed what one instance could not:

> **A verified answer contains sitting-relative prose, and that prose is false at the new sitting
> even when every underlying fact is unchanged.**

**Ten such statements** were found across the three reused questions — *"the Net-Zero Framework in
**Q8 of this paper**"* (March's Q8 is a different question entirely), *"in force 1 January 2026 —
**five weeks** before this examination"* (correct for February, wrong for March), *"**four
months** before this sitting"* (correct for January, six for March), and *"back onto **February**
2026"*.

Each was re-anchored by an **asserted patch** in the assembly step: the build fails if a patch does
not fire and fails again if the old string survives. **The tenth was found only by sweeping the
assembled spec** — the patch list built by reading the sources had missed it.

> **STANDING RULE FOR QP2604 AND QP2606.** Scanning a reused object for sitting-relative prose is a
> **mandatory step** of Tier D reuse, not a judgement call, and the **assembled spec must be swept
> afterwards** rather than the patch list trusted. Search for `this paper`, `this sitting`, `this
> examination`, `weeks/months before`, a named month-year, and any cross-reference to another
> question **by number** on the same paper.

This does **not** reopen the reuse rule. The verified answers and canonical routes were reused
exactly as February decided; no scoring proposition was altered on any of the three.

### Three exact recurrences, and the first NONE

**EXACT 3 · NEAR 0 · TOPIC 5 · NONE 1.** All three EXACT claims were established by **string
comparison of transcribed stems** — Q1 = QP2602 Q7 (398 chars), Q4 = QP2601 Q6 (453 chars), Q8 =
QP2602 Q3 (245 chars) — not from the source copy's recurrence table.

**Q2 (container cargo securing) is the set's first NONE.** February's finding that every question
had at least a topic relationship did not survive. A full similarity sweep of all nine March stems
against all 27 prior stems found **no middle ground**: exactly three pairs scored above 0.5, and
all three scored 1.0000.

> **FOUR LINKED PAIRS NOW EXIST.** QP2601 Q9 ↔ QP2602 Q4 · QP2602 Q7 ↔ QP2603 Q1 · QP2601 Q6 ↔
> QP2603 Q4 · QP2602 Q3 ↔ QP2603 Q8. **A correction to either member of any pair on Founder review
> must be applied to the other.** Recorded in each spec's `unresolved` list and each verification
> record.

### The March temporal check — the headline risk, and it is clear

**The Merchant Shipping Act 2025 commenced on 15 March 2026, mid-sitting-month.** The exact sitting
date **cannot be established**: no examination date is printed, and the source copy's PDF metadata
records only **20 April 2026** — the date the third-party host batch-generated *all six* 2026 files,
after every sitting.

**All nine questions were checked individually and none turns on the commencement**, so no
`A_BLOCKING` flag arises. The decisive one is **Q9**: India's recycling law is the **Recycling of
Ships Act 2019**, separate legislation, and **s.324(1) of the 2025 Act repeals the MS Act 1958 and
the Coasting Vessels Act 1838 only** — a closed list read in the Gazette for QP2607 Q7. **That July
Gazette work has now paid for itself a third time.** Q4 has zero Merchant Shipping Act references
(it rests on the IHR and the Indian Port Health Rules 1955, made under the Indian Ports Act 1908),
and the four "MSA" hits in Q8 are all the substring inside **EMSA**. Q7 was drafted to stay clear by
expressing flag-State reporting as a conditional test untied to a named national instrument.

### One harness defect found and fixed — the THIRD of its class

`ui_behaviour_test.cjs` hard-coded `search('general average').length === 1` inside the
graceful-degradation block. That silently assumed every paper sets a general average question —
true of QP2607, QP2601 and QP2602 by coincidence, **false of QP2603**, which failed on a page whose
search was working perfectly.

This is the same defect family as the old `glob('EM*.html')` and the hard-coded QP2607 fixtures:
**a harness that derives its page list dynamically while keeping a paper-specific assumption
inline.** Fixed at the definition level — the probe is now derived from the paper's own `FIXTURES`
entry, so it asserts what the test *means* (search is independent of storage) for any paper.
**The guard was not weakened**: it still fails if search returns nothing, and a paper with no
fixtures is already failed separately. A `FIXTURES` entry for QP2603 was added per the standing rule.

### Regression against all three prior papers — clean

`QP2607.html` (`a574cd36261778e4`), `QP2601.html` (`38b420fc88da8ad4`) and `QP2602.html`
(`abad5ab7706e370c`) are **byte-identical** before and after, and their specs have **no diff**
against `65ae91a`. `index.html`, `topics-2026.html` and the manifest changed, which is correct.
Rebuild is deterministic: all seven artefacts byte-identical across two consecutive runs.
`--publish` also passes in full, and review/noindex artefacts were restored afterwards.

### Cross-paper behaviour at four papers

- The index carries **36 questions, 9 per paper**; `topics-2026.html` renders **36 links, zero
  duplicates**.
- Searching *"general average"* returns **three** sittings and correctly **not** March, which sets
  no general average question.
- Each exact-repeat family is discoverable as a pair: *"ship sanitation"* → QP2601 Q6 + QP2603 Q4;
  *"thermal runaway"* → QP2602 Q3 + QP2603 Q8; *"signature subject to ratification"* → QP2602 Q7 +
  QP2603 Q1.
- **The §4 search-payload threshold — split into a fetched JSON file when the SIXTH paper is added
  — is now two papers away.** The index payload carries 36 questions.

### Measured statistics

| | QP2607 | QP2601 | QP2602 | **QP2603** |
|---|---|---|---|---|
| Answer words, mean | 560 | 844 | 925 | **863** |
| Answer words, range | 441–709 | 744–981 | 829–1022 | **745–953** |
| `understand_first` | 6/9 | 9/9 | 7/9 | **6/9** |
| Route steps, mean | 5.8 | 6.0 | 6.0 | **5.9** |
| Core points, mean | 24.3 | 30.2 | 30.3 | **30.9** |
| Flashcards, mean | 6.6 | 9.8 | 7.6 | **8.4** |
| Reverify A / B / C | 0/4/2 | 0/6/8 | 0/7/12 | **0/7/18** |

**March looks closest to January.** Mean 863 against January's 844. The likely reason is that March
has *fewer printed limbs* than February but *more named sub-tasks* — Q5 names four processes, Q6
three, Q9 three inside a running stem — and every named task must be visibly answered. A real
layering pass ran (Q7 956→918, Q9 952→921, Q2 938→847, Q5 884→852) with **no scoring proposition
removed**; what moved was reasoning the study guide already carried.

**`understand_first` came out at 6/6 on the new questions before review** — the January drift
re-emerging — and was corrected to 5/6 by applying the conditional test explicitly and dropping Q9,
whose route step 3 already carries the point. That the drift needed an explicit check rather than
instinct is itself worth recording.

### Open quality questions — unchanged from February, plus one new

1. **The 450–650 word band** now fails **27/36** questions and produces 27 of the 29 warnings. A
   per-*printed-limb* band does **not** fit March (six of nine questions print no limb marks); a
   per-*named sub-task* band fits all four. **Any replacement must account for tables** — Q6
   measures 892 words of which ~150 are a comparison table that *is* limb (a) in its most compact
   form. **No validator change was made**; the Founder's decision to wait for all six stands.
2. **`understand_first` pruning on QP2601** is now supported by three papers at 6/9, 7/9 and 6/9.
3. **Mobile sticky chrome** measured at 375px: QP2603 **59.6%**, QP2602 60%, QP2601 60%, QP2607 51%.
   March matches January and February — **pre-existing, not a March regression**. Desktop 20.2% at
   1280×900. No horizontal overflow at either width. Not fixed; the brief forbids redesign.
4. **NEW — the corpus temporal model needs a "live external list" state.** Three instances across
   three papers: Joint War Committee Listed Areas (March Q3), authorised Indian ports for ship
   sanitation certificates (January Q6), EU-approved recycling facilities (March Q9). These are not
   editions or amendment states; they are continuously revised third-party registers whose current
   value is load-bearing. A corpus object must be a pointer with "as-at" semantics, or not exist.
   **No workaround was invented in QP.** Handed to the corpus track in the demand map §4.

---

## 2e. QP2604 — APRIL PRODUCTION RESULT, 2026-08-09

**QP2604 (April 2026) is built: all 9 questions, Founder review candidate, 0 blocking flags.**

| Output | Path |
|---|---|
| Paper | `meoclass1/pastpapers/QP2604.html` — **generated** |
| Canonical content | `meoclass1/pastpapers/specs/QP2604.json` — **SOURCE OF TRUTH** |
| Verification records | `meoclass1/pastpapers/verification/QP2604/Q1..Q9.md` + `DEDUP_AND_SOURCE_PLAN.md` |
| True source demand | `docs/QP2604_TRUE_SOURCE_DEMAND_MAP.md` |
| Pattern register | `docs/2026_PATTERN_REGISTER.md` — **updated to 5 papers / 45 questions** |

### The template held again — fourth consecutive paper with no schema change

**No schema change was required.** The frozen question object absorbed a paper printing marks on
**all nine** questions, one question whose printed limb marks **contradict the paper's own
equal-marks instruction**, **seven NEAR recurrences** each needing re-authoring against changed
wording, and a reuse whose **governing statute changed** between the two sittings. Five modes,
one `answer_route`, everything else derived. **No sixth mode. No new archetype. No new primary
category.** `reference_shelf` remains empty on every question. Two new secondary `subject_tags`
were added (`Salvage Law`, `Biofouling`).

### THE ARCHITECTURE FINDING — a changed STATUTE is not a re-anchor

March established that a verified answer carries **sitting-relative prose** which must be
re-anchored. April establishes the category above it:

> **Sometimes the underlying legal truth is itself different at the two sittings, and no amount
> of re-anchoring will fix it.**

**Q7** is the instance. April falls **after** the 15 March 2026 commencement of the **Merchant
Shipping Act 2025**; January fell before it. January's limb (c) is correctly built on the **1958
Act**, and a statute sweep found that Act asserted on **eight surfaces** of the January object —
model answer, study guide, `recall_15s`, `major_trap`, an `answer_route` core point, a retrieval
card, `regulations` and `search_aliases`. **Limb (c) was re-authored, not patched**, and recorded
as a currentness change. The same commencement also re-anchored a study-guide note on **Q4**.

**The sweep caught a miss again, exactly as March predicted.** The hand-built patch list
re-anchored seven of the eight surfaces and **missed the Regulation and source map**. It was
found only by sweeping the **assembled** spec. March's rule is now 2/2 and should be treated as
permanent.

**A refinement, new from April:** the sweep produces **false positives** and every hit needs
human adjudication. Of **55 hits** on the assembled spec, **exactly one was a defect**. Q1's
fourteen are provisions of MARPOL Article 16 ("six months", "ten months"); Q3's three are the
absolute historical date "adopted by the CMI in May 2016".

### Recurrence — the profile inverted, and the host table failed both ways

**EXACT 0 · NEAR 7 · TOPIC 1 · NONE 1**, against March's EXACT 3 · NEAR 0 · TOPIC 5 · NONE 1.
**April is the first paper containing no exact repeat of any previously built question.**

**Six of April's nine questions map onto the January paper at the SAME question number** — Q3,
Q4, Q6, Q7, Q8 and Q9. April reads as a systematic re-issue of January with limbs and marks made
explicit and several limbs widened.

**The host recurrence table over-claimed on Q2** (listing FEB/Q3 and MAR/Q8, implying a third
instance of a known exact pair — it is NEAR at 0.6409, limb b) rewritten) **and under-claimed on
Q6** (listing only this sitting, omitting the Jan/Mar relationship entirely). Strongest evidence
yet for the standing rule that host tables establish topic recurrence only.

> **NEW WARNING — the similarity ratio is length-sensitive.** Q6 scores **0.1527** and Q7
> **0.1880** against questions whose tasks map one-to-one, purely because April's stems are much
> longer. **The ratio surfaces candidates; a task-by-task comparison classifies them.** A session
> ranking by score alone would have called both NONE and needlessly re-authored two answers.

> **NEW SUB-CLASS — NEAR by punctuation alone.** **Q4 scores 0.9946** against QP2601 Q4, with
> exactly two change blocks: an inserted colon and an inserted printed `(16)`. **No semantic
> difference at all.** Classified NEAR because EXACT means string equality, but **reused as
> though EXACT**. Do not read "NEAR" here as licence to re-author.

> **STANDING CONSEQUENCE, WIDENED.** A correction to **QP2601 Q3, Q4, Q6, Q7, Q8 or Q9** on
> Founder review must now be considered against **QP2604 Q3, Q4, Q6, Q7, Q8 and Q9** as well.

### The printed-marks anomaly — new class

**April prints a mark allocation on all nine questions** (QP2601 2/9, QP2602 6/9, QP2603 3/9).
Eight sum to exactly 16. **Q6 alone prints (5)+(5)+(5)+(5) = 20** against a question instruction 2
values at 16.

**Recorded as printed, NOT normalised.** Q6's machine-readable subpart marks are `null`: writing
5 into each would assert a 20-mark total the paper contradicts, and normalising to 4 would invent
figures the examiner never printed. **A future session must not "fix" this.**

### Two errors caught by opening the source

- A search summary asserted *"severe damage to the environment means a discharge of 50MT or more
  of pollutant"*. The Casualty Investigation Code **2.19** defines it as damage producing a
  **major deleterious effect upon the environment** as evaluated by the State(s) affected or the
  flag State — an **evaluative test, not a tonnage threshold**.
- Published summaries give the tacit-amendment objection threshold as *two thirds*. MARPOL
  **16(2)(f)(iii)** says **one third of Parties, or 50 per cent of world tonnage, whichever is
  fulfilled**.

**Fifth consecutive paper on which "open the source" caught a substantive error.**

### Regression against all four prior papers — clean

`QP2601.html` (`38b420fc88da8ad4`), `QP2602.html` (`abad5ab7706e370c`), `QP2603.html`
(`895bf9ca1e0a993e`) and `QP2607.html` (`a574cd36261778e4`) are **byte-identical** before and
after, and their specs have **no diff** against `03799dc`. `index.html`, `topics-2026.html` and
the manifest changed, which is correct. Rebuild is deterministic: all eight artefacts
byte-identical across two consecutive runs. `--publish` passes in full, and review/noindex
artefacts were restored afterwards.

### Cross-paper behaviour at five papers

- The index carries **45 questions, 9 per paper**; `topics-2026.html` renders **45 links, zero
  duplicates**.
- Searching *"general average"* returns **four** sittings and correctly **not** March.
- The Jan/Mar/Apr health-certificate family is discoverable as a trio via *"ship sanitation"*;
  the treaty-procedure family via *"tacit acceptance"* (Feb Q7, Feb Q8, Mar Q1, Apr Q1).
- *"biofouling"* returns April alone; the metadata-only alias *"bfrb"* resolves to QP2604 Q5.
- **The §4 search-payload threshold — split into a fetched JSON file when the SIXTH paper is
  added — is now ONE paper away.** `index.html` is **155.5 KB**, of which the search blob is
  **90.8 KB**. **Expect to act on it during QP2606.**

### Measured statistics

| | QP2607 | QP2601 | QP2602 | QP2603 | **QP2604** |
|---|---|---|---|---|---|
| Answer words, mean | **632** | 844 | 925 | 864 | **984** |
| Answer words, range | 572–709 | 744–981 | 829–1022 | 745–953 | **771–1238** |
| `understand_first` | 6/9 | 9/9 | 7/9 | 6/9 | **8/9** |
| Route steps, mean | 5.8 | 6.0 | 6.0 | 5.9 | **5.8** |
| Core points, mean | 24.3 | 30.2 | 30.3 | 30.9 | **31.6** |
| Flashcards, mean | 6.6 | 9.8 | 7.6 | 8.4 | **9.6** |
| Reverify A / B / C | 0/4/2 | 0/6/8 | 0/7/12 | 0/7/18 | **0/9/10** |

> **The QP2607 mean is corrected here from 560 to 632.** The old figure predates the heading
> renumbering documented in §7 below and was never updated in the register. See
> `2026_PATTERN_REGISTER.md` §0.

**April is the longest and widest paper in the set.** A real layering pass ran and is recorded —
Q1 1071→1015, Q5 1244→1166, Q7 1226→1186, Q9 1264→1238 — with **no scoring proposition removed**.
The residual length tracks April's **~29 named sub-tasks**, more than any prior paper: the three
longest answers are precisely the three with the most internal tasks. **The C-flag count fell for
the first time** (18→10) because both new questions rest on freely published primary sources read
in full.

**`understand_first` at 8/9 is partly inherited**, not a fresh 8/9 decision: April's two new
questions are 2/2, and five of the remaining six inherit from QP2601's 9/9. **Pruning QP2601's on
review would automatically improve QP2604.**

### Open quality questions — unchanged, plus one sharpened

1. **The 450–650 word band** now fails **36/45** and produces 36 of the 38 warnings. A
   per-*named-sub-task* band is the only shape that has fitted all five papers. **No validator
   change was made.**
2. **`understand_first` pruning on QP2601** now propagates to five April questions.
3. **Mobile sticky chrome**: QP2604 **60.5%** at 375px, against QP2603 59.6%, QP2602 60%,
   QP2601 60%, QP2607 51%. Desktop 182px = **20.2%** at 1280×900, identical to March. No
   horizontal overflow at either width. **Pre-existing, not an April regression.**
4. **The corpus "live external list" state** reaches a **fourth** instance (national biofouling
   arrival requirements). The demand map adds a refinement: a live register may carry
   **immutable historical facts** — India's UNCLOS ratification date — which *are* safe as corpus
   objects.
5. **NEW — MARPOL corpus objects must resolve to the ARTICLES of the parent Convention**, to the
   third level of sub-paragraph. Every prior paper demanded Annex/regulation level; Q1 turns on
   the difference between `16(2)(f)(i)` and `16(2)(f)(iii)`.

---

## 2f. QP2606 — JUNE PRODUCTION RESULT, 2026-08-09. THE 2026 SET IS COMPLETE.

**QP2606 (June 2026) is built: all 9 questions, Founder review candidate, 0 blocking flags.**
**This completes the six available 2026 sittings — 54 questions.**

| Output | Path |
|---|---|
| Paper | `meoclass1/pastpapers/QP2606.html` — **generated** |
| Canonical content | `meoclass1/pastpapers/specs/QP2606.json` — **SOURCE OF TRUTH** |
| Verification records | `meoclass1/pastpapers/verification/QP2606/Q1..Q9.md` + `DEDUP_AND_SOURCE_PLAN.md` |
| True source demand | `docs/QP2606_TRUE_SOURCE_DEMAND_MAP.md` — **carries the six-paper aggregate** |
| Transcription record | `docs/QP2606_SOURCE_TRANSCRIPTION_AND_RECURRENCE.md` — unchanged, still accurate |
| Pattern register | `docs/2026_PATTERN_REGISTER.md` — **updated to 6 papers / 54 questions** |

### The template held again — fifth consecutive paper with no schema change

**No schema change was required.** The frozen question object absorbed the most expensive paper in
the set: **five questions with no relationship at all to any of the 45 previously built**, **zero
Tier D reuse**, one question (Q6) sitting substantially **outside the regulatory corpus**, and one
question (Q3) requiring **two editions of the same instrument to be held simultaneously**. Five
modes, one `answer_route`, everything else derived. **No sixth mode. No new archetype. No new
primary category.** `reference_shelf` remains empty on every question. Two new secondary
`subject_tags` were added (`Port State Control`, `Ship Economics`).

### June was resumed from a checkpoint, and the checkpoint held

The previous session deliberately stopped after transcription, recurrence and the verification of
Q1 and Q2, rather than lowering verification quality. **That decision was correct and the handover
worked.** This session re-derived the transcription independently from the source PDF and
**every anomaly the checkpoint recorded reproduced exactly** — the `SOLAS ch.ll-1` double-L, the
mismatched quote on `"Andaman and Nicobar Islands'`, the unhyphenated York Antwerp, and all nine
printed mark allocations. Nothing in the checkpoint had to be revised.

### Recurrence — a third distinct profile, and the first paper with no repeat at all

**EXACT 0 · NEAR 0 · TOPIC 4 · NONE 5.** The checkpoint's classification was re-read and
**left unchanged**; no new evidence contradicted it.

| Paper | EXACT | NEAR | TOPIC | NONE |
|---|---|---|---|---|
| QP2603 March | 3 | 0 | 5 | 1 |
| QP2604 April | 0 | 7 | 1 | 1 |
| **QP2606 June** | **0** | **0** | **4** | **5** |

**June is the first paper with neither an exact nor a near recurrence**, and it carries **five
genuinely new questions — more than the previous five papers produced between them.** Tiers are
**C ×5, B ×4, no A, and NO TIER D.**

**Two recurrence failure modes were recorded, both new:** the similarity ratio **ranked the wrong
neighbour** on Q3 (top scorer QP2601 Q3 is a salvage question; the real relative QP2607 Q5 scores
lower), and Q4 shares the token "decarbonisation" with QP2601 Q2 as a **homonym** — main-engine
decarbonisation versus the energy transition. Full detail in
`verification/QP2606/DEDUP_AND_SOURCE_PLAN.md` §3.

### THE ARCHITECTURE FINDING — the edition axis is load-bearing, not metadata

March established that a reused answer carries sitting-relative prose. April established that the
governing statute can itself differ between sittings. **June establishes the case above both:**

> **A question can require TWO EDITIONS OF THE SAME INSTRUMENT AT ONCE.**

Q3 names the **York Antwerp Rules 1994** — an edition superseded twice. It cannot be answered on
YAR 2016, and it cannot be answered without knowing YAR 2016 either. The finding that made it
tractable is that **Rule A is word-for-word identical in the 1994 and 2016 editions**, while
Rules VI, XX, XXI and XXIII differ materially and the 1994 Rules contain **no time bar at all**.

**Consequence for the corpus:** an object model that stores "the York-Antwerp Rules" as current
text plus an edition tag **cannot answer this question**. Editions must be first-class objects with
a diff relationship. Recorded in the demand map §2, Q3.

### Seven substantive findings from opening the primary source

**Seventh consecutive paper on which reading the instrument caught something the summaries got
wrong.** June produced an unusually rich crop:

1. **GBS tier count (Q1).** MSC.287(87) §1.5 records a **five-tier system**; §3 states the
   Standards **consist of three tiers**. Both are true. An automated summary of that same
   resolution asserted a "four-tier framework", which is neither.
2. **GBS verification guidelines (Q1).** No longer MSC.296(87) — now **MSC.454(100)**.
3. **PSC procedures (Q2).** **A.1206(34), adopted 3 December 2025, revokes A.1185(33)** and is
   operative at this sitting. Much material dated well into 2025 still cites the old one.
4. **The PSC "Review Procedures" trap (Q2).** Chapter 5 carries that title and is **not** the
   appeal route; the owner's remedy is §2.3.11, which also establishes that the right belongs to
   **the company, not the Chief Engineer**, and that **an appeal does not suspend the detention**.
5. **Cyber guidelines (Q5).** **MSC-FAL.1/Circ.3/Rev.3, 4 April 2025**, sets out **SIX** functional
   elements — **Govern** was added ahead of Identify, Protect, Detect, Respond, Recover. Almost all
   published material, including industry guidance, still says five.
6. **HSSC survey guidelines (Q8).** **A.1207(34), adopted 3 December 2025, revokes A.1186(33)** —
   the same Assembly session as the PSC resolution. And the **periodical survey has two different
   frequencies**: second-or-third anniversary for the Safety Equipment Certificate, **every**
   anniversary for the Safety Radio Certificate.
7. **FSA criterion (Q9).** The Guidelines prescribe **no mandatory monetary threshold** for
   averting a fatality. §9.2.2 says no risk acceptance standard is universally accepted, and
   appendix 7 says its values are "provided for illustrative purposes only". The widely quoted
   figure is not an IMO requirement.

One further correction was caught before it reached an answer: the **RO Code is MSC.349(92)**, not
MSC.349(90) as a search summary asserted.

### THE HIGHEST-RISK CLAIM ON THE PAPER WAS TESTED AND REJECTED

**Q7's stem invites a false statement, and the answer does not make it.**

The question asserts that the Lakshadweep and Andaman and Nicobar Islands "are known for their
critical habitat and required to be protected". True — and it tempts the candidate into saying they
**are** Particularly Sensitive Sea Areas.

**They are not.** IMO's own record of designations was checked: **nineteen PSSAs exist worldwide
and none of them is in India.** Indian waters hold no MARPOL Special Area and no Emission Control
Area either. **The examiner wrote "could be protected", in the conditional**, and the answer is
written prospectively for exactly that reason.

The Indian statutory layer was established at a sitting falling **after 15 March 2026**: the
**Merchant Shipping Act, 2025** governs ship-source pollution, but the islands' coastal-zone and
habitat protection rests on the **Island Coastal Regulation Zone Notification, 2019** under the
**Environment (Protection) Act, 1986** and on the **Wild Life (Protection) Act, 1972** — specialist
legislation the shipping Act does not displace. **The QP2607 Gazette work has now paid for itself a
fourth time.**

> **One citation is deliberately not asserted.** The exact Gazette number and date of the ICRZ
> Notification, 2019 could not be settled — published sources give both a January 2019 and a
> January 2021 instrument bearing the 2019 title, consistent with a draft followed by a final
> notification. The substance is consistently supported and is what the answer states.
> `B_CURRENCY_CHECK`. India Code returned **HTTP 403** again.

### Q6 — the deliberate abstention

**Q6 sits substantially outside the regulatory corpus, and no citations were manufactured for it.**
The capital/voyage/operating cost taxonomy and every inventory technique — ABC, VED, FSN, SDE, HML,
economic order quantity, reorder level, safety stock — are accepted shipping-economics and
operations-management practice, **not the content of any instrument**. They are presented as
reasoning and practice, and recorded as `C_ACCEPTED_LIMITATION`.

Exactly two regulatory constraints genuinely bear on the question and are used only there:
**ISM Code 10.3** (critical equipment — which is why critical spares cannot be run just-in-time)
and **MARPOL Annex VI regs 25 and 28** (efficiency as a compliance outcome). **No numerical cost
proportions are asserted anywhere**, because MIW holds no verified dataset for them.

> This is the first question in the set with a near-empty demand map entry, and that is the correct
> outcome rather than a gap. See the demand map §2, Q6.

### One known trap fired, and the CONTENT was fixed rather than the guard weakened

`known_traps_check.py` **trap 10 — "Ammonia is not a zero-emission fuel"** — failed on QP2606 Q4,
because the quick-revision named ammonia but neither N2O nor slip.

**The guard was right.** The answer discussed ammonia purely as a toxicity hazard and never said it
is not zero-emission, so a candidate could have inferred that it is. **The guard was left at full
strength and the answer was extended**: the fuel table now records that there is no carbon in the
molecule but combustion produces **N2O and ammonia slip** and the lifecycle result depends on the
production pathway, with a matching route point, `major_trap` entry and retrieval card. This is the
QP2601 precedent applied a second time — *fix the content, not the guard*.

### Regression against all five prior papers — clean

`QP2601.html` (`38b420fc88da8ad4`), `QP2602.html` (`abad5ab7706e370c`), `QP2603.html`
(`895bf9ca1e0a993e`), `QP2604.html` (`93984e85c6f6c136`) and `QP2607.html` (`a574cd36261778e4`) are
**byte-identical** before and after, and all five specs show **zero diff** against `13d29cc`.
`index.html`, `topics-2026.html` and the manifest changed, which is correct. Rebuild is
deterministic: **all nine generated artefacts byte-identical across two consecutive runs.**
`--publish` passes in full, and review/noindex artefacts were restored afterwards.

### Cross-paper behaviour at six papers — the complete year

- The index carries **54 questions, 9 per paper**; `topics-2026.html` renders **54 links, zero
  duplicates**.
- **May renders as `coming later`** with an em-dash and no link. **`QP2605` appears nowhere.**
- Searching *"general average"* returns **five** sittings — Jan, Feb, Apr, Jun, Jul — and correctly
  not March.
- The FSA family is discoverable across **five** papers; June is the only one that asks for the
  method rather than an application.
- A `FIXTURES` entry for QP2606 was added to `ui_behaviour_test.cjs`, per the standing rule.
  Its Q1 probe is deliberately `ship construction file` rather than `goal-based`, because Q8 also
  refers to goal-based standards and the bare term resolves to two cards.

### THE SEARCH-PAYLOAD THRESHOLD IS NOW REACHED — MEASURED, NOT ACTED ON

§4 records the threshold as *"split the search index into a fetched JSON file when the sixth paper
is added"*, and §14 said to act on it during QP2606. **It has been measured and deliberately NOT
implemented**, because the June session brief explicitly reserved search architecture for the
Founder review and forbade redesign during production.

**Measured at six papers:** `index.html` is **181.4 KB**, of which the inlined search payload is
**134.9 KB — 74% of the page** — and the `search_blob` field alone is **112.7 KB**. Projecting
linearly, twelve papers gives roughly **270 KB of payload**.

> **FOUNDER DECISION REQUIRED.** No performance problem is observable at six papers. The decision
> is whether to split now, at the threshold as originally written, or to defer to a measured
> user-experience trigger. **This is a §16 stop condition item; do not implement it inside a
> production session.**

### Measured statistics

| | QP2607 | QP2601 | QP2602 | QP2603 | QP2604 | **QP2606** |
|---|---|---|---|---|---|---|
| Answer words, mean | 632 | 844 | 925 | 864 | 984 | **1334** |
| Answer words, median | — | — | — | — | — | **1394** |
| Answer words, range | 572–709 | 744–981 | 829–1022 | 745–953 | 771–1238 | **1010–1516** |
| `understand_first` | 6/9 | 9/9 | 7/9 | 6/9 | 8/9 | **6/9** |
| Route steps, mean | 5.8 | 6.0 | 6.0 | 5.9 | 5.8 | **7.1** |
| Core points, mean | 24.3 | 30.2 | 30.3 | 30.9 | 31.6 | **41.1** |
| Flashcards, mean | 6.6 | 9.8 | 7.6 | 8.4 | 9.6 | **9.7** |
| Reverify A / B / C | 0/4/2 | 0/6/8 | 0/7/12 | 0/7/18 | 0/9/10 | **0/12/15** |

**June is by a wide margin the longest paper in the set, and the reason is structural rather than
stylistic.** It carries the most named sub-tasks of any paper — Q3 sets five distinct tasks, Q9
names three deliverables and then singles out three of five steps for detailed explanation, Q6
carries three tasks in an unlimbed sixteen-mark question — and **five of nine questions had no
reusable material at all**, so every proposition had to be stated rather than inherited. Route
steps (7.1) and core points (41.1) rose in the same proportion, which is the honest signal: the
answers are longer because there is more to answer, not because the prose is looser.

**A layering pass was run on Q9**, the outlier, moving explanatory material into the study guide
(1577 → 1516) **with no scoring proposition removed**. No further trimming was attempted, because
the session brief was explicit: **record June's datapoint, do not change the length policy, and do
not cut scoring propositions to hit a number.**

**`understand_first` was pruned from 9/9 to 6/9 by applying the conditional test explicitly.**
Q1, Q4 and Q6 were dropped because each duplicated a study-guide section that already made the same
point. This reproduces the pattern exactly: the three papers that applied the test landed at 6/9,
7/9 and 6/9; the paper that did not landed at 9/9. **The drift is real and it needs an explicit
check every time.** Note that the Understand *tab* still renders on all nine cards — it carries the
derived knowledge map, which is always present, so pruning removes clutter without emptying a mode.

### Mandatory assembled-spec sweep — run, and clean

Run per the standing rule despite June carrying **no Tier D reuse** and therefore no inherited
prose. **~385 hits across ten patterns, adjudicated by hand, ZERO defects.** Every hit is a
deliberate "this is superseded" teaching point, a correctly anchored sitting-relative statement
(the arithmetic was checked), or a real instrument date. `cross-ref by number` returned **0 hits**.

### Open quality questions — unchanged, plus one sharpened

1. **The 450–650 word band** now fails **45/54** and produces 45 of the 47 warnings. A
   per-*named-sub-task* band remains the only shape that has fitted every paper, and **June is the
   strongest evidence yet**: it has the most sub-tasks and the highest word count, and the two rose
   together. **No validator change was made.** All six papers now exist; the decision is ripe.
2. **`understand_first` pruning on QP2601** is now supported by four papers at 6/9, 7/9, 6/9 and
   6/9 against January's unchecked 9/9.
3. **Mobile sticky chrome**: QP2606 **55.3%** at 375px, against QP2604 60.5%, QP2603 59.6%,
   QP2602 60%, QP2601 60%, QP2607 51%. **Pre-existing, not a June regression.** No horizontal
   overflow at 375px; search input visible; deep link `#q7` opens expanded.
4. **The corpus "live external list" state reaches a FIFTH instance** — the IMO register of
   designated PSSAs — **with a new and sharper sub-class: the load-bearing claim is a NEGATIVE.**
   Q7 depends on no Indian area being designated, and a negative claim decays silently when the
   list changes. A live-list object needs an **absence** relationship, not just membership. Also
   new from June: **a meeting outcome is not an instrument** (the HTW 12 result is load-bearing for
   Q4 and has no edition). Both handed to the corpus track in the demand map §4.

---

## 3. Naming — canonical, one identity everywhere

```
QP<YY><MM>            QP = Question Paper.  QP2607 = July 2026.
QP<YY><MM>.html       the generated page
QP<YY><MM>-Q<n>       question_id
#q1 .. #q9            anchors (paper-relative, unchanged by renames)
```

The old `EM26xx` identity is **gone from every canonical and generated surface**. Two
Founder decisions govern this:

1. **`sr_no` is now `QP-2607`.** The printed serial on the source copy differs. Founder
   decision was absolute one-identity-everywhere, accepting that the spec no longer
   records the printed serial. The printed serial is preserved in
   `verification/LOCAL_SOURCE_PROVENANCE.md` instead, so nothing is lost.
2. **Legacy identifiers may still appear in prose** — in this file, in the verification
   records, in `known_traps.md` and in the migration tests. That is correct and
   deliberate: describing history is not carrying a legacy identity. `health_check.py`
   scopes its "no legacy identifier" rule to the **manifest and the generated pages only**.

**Saved study state migrates, it is not discarded.** `migrateLegacyKeys()` is injected
into both page scripts from `render_common.LS_MIGRATE_JS` and remaps `EM<YYMM>-Q<n>` keys
to `QP<YYMM>-Q<n>` on load. It is idempotent, never overwrites an existing QP value, and
writes nothing on a fresh device. Eight tests in `ui_behaviour_test.cjs` exercise the
**real shipped function**, extracted out of the generated page rather than reimplemented.

---

## 4. Architecture — settled, do not redesign

```
specs/QP2607.json          <-- ONE canonical question object per question
      |
      +-- build_paper.py   --> QP2607.html
      |
      +-- build_index.py   --> pastpapers_content_index.json
                           --> index.html
                           --> topics-<year>.html
```

**One question object → six outputs. No answer text exists twice anywhere.**

- **Tools stay at `tools/pastpapers/`.**
- **No separate Study Guide HTML file.**
- **Search is driven by generated `data-search` attributes**, never `innerText`.
- **Bookmarks/progress**: `localStorage`, keys `miw:pastpapers:v1:bookmarks` and
  `miw:pastpapers:v1:progress`, keyed by stable `question_id`.
- **Publication mode exists**: `--publish` switches noindex→index and removes the
  per-question production metadata block. Review mode is the default.
- **Never derive build targets from a filename glob.** `run_toolchain.py` and
  `health_check.py` both derive the pages under test from the specs. The old
  `glob('EM*.html')` would have matched zero files after the rename and still printed
  `UI BEHAVIOUR PASS`, silently deleting 34 tests. A stage that tests nothing now fails.

### Index scales by year and month

`index.html` answers three intents, in this order:

1. **"I know the sitting"** — one compact block per year, twelve month cells each. Flows
   12 across on desktop down to 4 on a phone, so a year stays one glance at any width.
2. **"I know the topic"** — the year topic pages.
3. **"I want to carry on"** — four study-state filters.

Configured by `SERIES_YEARS` in `build_index.py`. **A year is advertised from
configuration, never from placeholder specs** — do not create empty spec files for
future months. `topics-<year>.html` already generates per year automatically; a 2025
spec produces `topics-2025.html` with no code change.

**Public paper status is deliberately two-valued**: `available` / `coming_later`. A month
is `available` only when answers actually exist, so holding a source PDF can never make a
paper read as solved. The manifest keeps the richer internal state
(`build_state`, `review_state`, `official_source_verified`).

### Search payload — a known future threshold

Every question's `search_blob` is inlined into `index.html`. Measured: 47 KB at 9
questions, projecting to **~549 KB at 12 papers and ~1.1 MB at 24**. Acceptable now,
not at scale. **When the sixth paper is added, split the search index into a fetched
JSON file.** Do not do it before then — one paper does not justify a loading state.

---

## 5. Canonical Written Answer template — now enforced

Derived from the nine existing answers, not invented. `validate_spec.py` enforces it.

```
QUESTION
  -> EXAM APPROACH (answer skeleton)      <- above the model answer
  -> MODEL WRITTEN ANSWER
  -> STUDY GUIDE
  -> QUICK REVISION
  -> cross-links / recurrence
```

### The learning layer — `answer_route` is the spine

Design rationale: **`docs/MIW_LEARNING_METHOD_DESIGN.md`**. Read it before authoring a paper.

One canonical numbered route per question. **Everything else is derived from it** — the
model answer's principal headings, the knowledge map branches, the blank-skeleton recall
test, the exam plan and the rapid-revision route line. `validate_spec.py` enforces the
correspondence, so a route step and its heading cannot drift apart.

| Field | Status |
|---|---|
| `answer_route` — `archetype`, `steps[]` (`n`, `limb`, `title`, `points[]`) | **REQUIRED** on a built answer |
| `retrieval_cards[]` — `id`, `type`, `prompt`, `answer`, `why` | **REQUIRED**, ≥4, stable ids |
| `understand_first` | **CONDITIONAL** — only where the topic is counter-intuitive |
| `memory_cue` | **OPTIONAL** — only where genuinely memorable. No invented acronyms. |
| knowledge map · recall test · exam plan | **DERIVED — never authored** |

`quick_revision.skeleton` was **removed**: it was a second copy of the route. Five
archetypes cover the corpus: `procedure`, `explain`, `compare`, `legal`, `evaluate`.

**The learning layer must never be able to hide the answer.** Every mode renders unhidden
and only the script hides them, so with scripting off the whole card still reads top to
bottom. `health_check.py` fails the build if the answer mode is emitted pre-hidden.

**Every re-verification flag must carry a class** from `A_BLOCKING` / `B_CURRENCY_CHECK` /
`C_ACCEPTED_LIMITATION`, plus a `claim` and a `why`. `validate_spec.py` rejects anything
else and prints the blocking count, so "is this publishable?" is answered by the toolchain
rather than by reading prose. A flag that no longer applies is **deleted**, not downgraded.

**Study guide spine — all six required:** Why this structure scores · Common mistakes ·
Examiner traps · Likely oral follow-up · Memory framework · Regulation and source map.
Plus at least one section whose heading **starts with** `Uncertainty` — the tail is
question-specific by design. Question-specific analysis sections in between are
deliberately unconstrained; that is where the thinking lives.

**Quick revision — all six fields required:** `recall_15s`, `skeleton`, `keywords`,
`critical_numbers`, `critical_regulation`, `major_trap`. A skeleton of fewer than three
steps is rejected as not a usable exam-writing map.

**The Exam Approach block renders `quick_revision.skeleton` above the model answer**, and
the skeleton was removed from the Quick Revision list so it appears exactly once per
card. Same single source of truth still feeds the paper-level Rapid Revision table.

**Three-layer rule unchanged:** model answer = what scores plus only the reasoning needed
to make it correct; study guide = the rest.

---

## 6. Provenance model — neutral, and honest about authority

```
source_copy_provenance: {
  described_as:   "Third-party-hosted copy of an examination paper",
  source_copy_type: "third_party_scan",     <- WHAT kind of copy
  source_authority: "unverified",           <- how much authority it carries
  host_identity_record: <points at the local-only file>
}
official_source_verified: false             <- SEPARATE axis, unchanged
```

`validate_spec.py` rejects a spec carrying `host_branding`, and rejects
`source_authority: verified_official` unless `official_source_verified` is also true.
**Removing a host's name does not promote a scan to an official source.** Trap 14 in
`known_traps.md` now scans generated pages, specs *and* the manifest — previously it was
scoped to HTML only, on the since-invalidated assumption that specs were private.

---

## 7. QA state

```
python tools/pastpapers/run_toolchain.py --self-test
```

```
SPEC          PASS  (9 warning(s))     <- QP2601, all 9 are word-count band warnings
SPEC          PASS  (9 warning(s))     <- QP2602, all 9 are word-count band warnings
SPEC          PASS  (9 warning(s))     <- QP2603, all 9 are word-count band warnings
SPEC          PASS  (9 warning(s))     <- QP2604, all 9 are word-count band warnings
SPEC          PASS  (9 warning(s))     <- QP2606, all 9 are word-count band warnings
SPEC          PASS  (2 warning(s))     <- QP2607, the two accepted exceptions below
PAPER BUILD   PASS
PAPER BUILD   PASS
PAPER BUILD   PASS
PAPER BUILD   PASS
PAPER BUILD   PASS
PAPER BUILD   PASS
INDEX BUILD   PASS
UI BEHAVIOUR  PASS  6 page(s)
KNOWN TRAPS   PASS
HEALTH        PASS
AUDIT         PASS
AUDIT         PASS
AUDIT         PASS
AUDIT         PASS
AUDIT         PASS
AUDIT         PASS
ALL STAGES PASS   47 warning(s)
```

Six specs now, so the per-spec stages run six times. **47 warnings = 2 QP2607 (accepted, below)
+ 9 each for QP2601, QP2602, QP2603, QP2604 and QP2606 word-count warnings** — see §2f for the open
question those raise. Zero errors, zero blocking flags on any of the six papers.

**45 of the 47 warnings are the one disputed band.** That is warning noise rather than signal, and
it is the reason §2c, §2d, §2e and §2f recommend retiring or re-deriving the 450–650 band. **All six
papers now exist, so that decision is ripe and belongs to the Founder review.**

QP2606 carries **27 re-verification flags: 0 class A, 12 class B, 15 class C** — the highest B count
in the set, which is the honest signal of a paper resting on four instruments that are re-adopted on
a cycle (A.1206(34), A.1207(34), MSC-FAL.1/Circ.3/Rev.3, MSC.454(100)) plus an unsettled Indian
Gazette citation. The single most important class B is on **Q7**: that **no Indian sea area holds
PSSA designation**. That is the negative claim the whole of Q7 limb (a) rests on, and it decays
silently — re-confirm it against IMO's record before publication.

QP2604 carries **19 re-verification flags: 0 class A, 9 class B, 10 class C.** The most important
class B is the pair on Q7 and Q4 — that the **Merchant Shipping Act 2025** is the operative Indian
statute at the April sitting, which must be re-checked as a unit if either question is corrected.
The most important class C is on Q1: **MIW holds no licensed IMO consolidated MARPOL edition**, so
Article 16's consolidation state is not independently established.

**A `FIXTURES` entry for QP2604 was added to `ui_behaviour_test.cjs`**, per the standing rule. Its
probe for Q7 is deliberately `article 253` rather than `unclos`, because April Q8 also cites
UNCLOS article 94(7) and the bare convention name resolves to two cards.

QP2602 carries **19 re-verification flags: 0 class A, 7 class B, 12 class C.** The single most
important is the class B on Q8 — the approved-but-not-adopted status of MARPOL Annex VI Chapter 5,
which the reconvened extraordinary session (due around October 2026) may change.

QP2603 carries **25 re-verification flags: 0 class A, 7 class B, 18 class C.** The high C count is
the honest signal of March's licence gap — seven distinct licence-gated instruments (SOLAS, CSS
Code, IGF Code, ISO 20519, 2011 ESP Code, ISO 484, Hong Kong Convention) blocked a P1 claim, the
widest of any paper. The most important class B is on Q9: that s.324(1) of the MS Act 2025 does not
reach the Recycling of Ships Act 2019, which should be re-checked against the subordinate Merchant
Shipping Rules 2026 once they leave draft.

`--publish` also passes in full. That is new: `audit_paper.py` used to rebuild in review
mode and compare against a publish-built page, so **`--publish` could never pass its own
audit** — a failure that would have surfaced only at the moment of publication. It now
takes `--publish` and `run_toolchain.py` passes it through.

Rebuild is **byte-identical** — verified by hashing all four generated artefacts before
and after a second run.

Health and trap checks are **positive-controlled**: `--self-test` injects real faults and
asserts they are caught. Faults that are an *absence* (a page that lost its study-state
migration; a month cell that lost its link) are controlled by `strip_from_pages`, which
removes the marker instead of appending one. Keep it that way.

### The 2 remaining warnings are accepted, not defects

| Warning | Decision |
|---|---|
| Q2 model answer ≈ 709 words (band 450–650) | **Accepted.** Corrected Bunkers/CLC legal wording. Do not shorten. |
| Q6 model answer ≈ 695 words | **Accepted.** Zero-carbon qualification + ICE-vs-fuel-cell contrast. Do not shorten. |

**Do not spend a session trimming these.**

Warnings went 4 → 2. The other two were `freshness_risk` values that did not start with
LOW/MEDIUM/HIGH (`"MEDIUM-HIGH …"` on Q4, `"HIGHEST IN THE PAPER …"` on Q7). Both were
fixed by making the field conform to its own vocabulary while stating the truth — Q4 is
HIGH, Q7 is now MEDIUM because its statutory facts are settled. Neither was suppressed.

Q7 briefly went 13 words over band when the section citations were added; it was tightened
back to **650**, the band ceiling, rather than becoming a third documented exception.

Model answer lengths: Q1 643 · Q2 709 · Q3 640 · Q4 594 · Q5 572 · Q6 708 · Q7 650 ·
Q8 588 · Q9 581. These rose slightly when the principal headings were renumbered and given
route titles — heading text counts toward the word count. Q6 moved 695 → 708 for that
reason alone; **no answer content was added or removed.**

### `.gitattributes` now pins LF

`core.autocrlf=true` rewrote LF→CRLF on checkout while the builders write LF, so the
committed bytes never matched builder output and every build dirtied the tree. The new
root `.gitattributes` pins `*.html/json/css/js/py/md` to LF and marks `*.pdf` binary,
which makes the byte-reproducibility guarantee actually true.

---

## 8. Q7 — RESOLVED against primary sources. Publication register.

**Both Q7 blockers are closed.** Full detail in `verification/QP2607/Q7.md`.

**Sources actually read**, both in full:

- **The Act** — Gazette of India, Extraordinary, Part II Section 1, No. 29, 18 August 2025,
  `CG-DL-E-19082025-265484`, via **`dgma.gov.in`** (118 pages).
- **S.O. 1244(E)** — Gazette of India, Extraordinary, Part II Section 3(ii), No. 1192,
  10 March 2026, Ministry of Ports, Shipping and Waterways, `F. No. SR-20020/5/2020-ML`,
  `CG-DL-E-11032026-270832`, via **`shipmin.gov.in`**.

`indiacode.nic.in` returned **HTTP 403** again. **The reusable lesson: when India Code
blocks automated retrieval, go to the administering Ministry (`shipmin.gov.in`) and to
`dgma.gov.in`.** That is what cleared a blocker the previous session could not.

**Commencement — the question mattered.** Section 1(2) *expressly* permits different dates
for different provisions, so partial commencement was a real possibility. But S.O. 1244(E)
appoints a single date for "the provisions of said Act", enumerating nothing and excluding
nothing. **The whole Act came into force on 15 March 2026; the staging power was not
exercised.**

**Section-level citations now carried**, each read in the Gazette: `s.1(2)` commencement ·
`s.15(1)` ownership incl. NRI/OCI · `s.15(2)` OCI-wholly-owned not required to register ·
`s.16` bareboat charter-cum-demise · `s.17` recycling registration · `s.59` minimum age
sixteen · `s.324(1)` repeal · `s.325` consequential amendment. **325 sections, 16 Parts.**

**One claim was corrected.** The answer said the Act gives effect to "**IMO** and ILO
instruments". The Act never names the IMO (0 occurrences). It now cites the **long title's**
treaty-compliance purpose and the **MLC 2006**, which *is* named in the Act.

> Caution for the corpus: a widely-read public secondary source still described the Act as
> *"not yet in force"* in late March 2026, after commencement. Go to the Gazette.

### The publication register — `A` / `B` / `C`, now enforced

`validate_spec.py` requires every flag to carry a class and prints the blocking count.

| Class | Meaning | Count |
|---|---|---|
| **A — blocking** | Publication cannot proceed | **0** |
| **B — currency check** | Ships, but re-check immediately before publication | 4 |
| **C — accepted limitation** | Ships as-is with the limitation stated in the answer | 2 |

| Q | Flag | Class |
|---|---|---|
| Q1 | IMSBC amendment currency (08-25 mandatory 1 Jan 2027) | B |
| Q1 | IRON ORE PELLETS = Group C, authoritative-secondary only — MIW holds no licensed IMSBC Code | C |
| Q4 | ECA list and dates; Canadian Arctic / Norwegian Sea limits bite 1 Mar 2027 | B |
| Q6 | MSC.1/Circ.1687 still operative and non-mandatory — confirm MSC 111 did not supersede/renumber it | B |
| Q6 | Marine fuel cell maturity vs ammonia dual-fuel | C |
| Q7 | Status of subordinate Merchant Shipping Rules 2026 (draft as at Aug 2026) | B |

**Class C is not a promotion to primary.** It is a decision to publish with the limitation
stated. Do not silently re-label a C as verified.

---

## 9. Q9 / QB9_C — known cross-link issue, repair deferred

QP2607 Q9 correctly treats the **Indian Marine Insurance Act, 1963** as operative (s.19
utmost good faith, s.20 disclosure incl. the four s.20(3) exceptions).

`meoclass1/QB9_C.html` attributes the principles to the **UK Marine Insurance Act 1906** —
wrong statute for an Indian examination. QP2607 Q9 carries an **explicit caution** rather
than silently inheriting it. `meoclass1/QB9_E.html` handles it correctly.

**The QB9_C cross-link has been REMOVED from Q9.** The caution was carried as the link
*label*, so the entire warning rendered as one long hyperlink pointing at the flawed page —
the warning text was the click target. The warning now lives as prose in the Q9 study guide,
where it informs without inviting the click. Q9 still links to `QB9_E`, which is correct.

A broad Question Bank repair is **deliberately deferred** and is a separate task. Once
QB9_C is fixed, restore the cross-link in `specs/QP2607.json` (Q9 `cross_links`) and
regenerate. Recorded as trap 8.

> Template lesson: a `cross_links` entry renders as an anchor, so its `label` must be a
> destination name, never a warning. If a target needs a caveat, the caveat belongs in the
> study guide and the link belongs nowhere.

---

## 10. Review / publication state — do not change without Founder approval

- All **five** paper pages are **`noindex`**; **no gate** is enabled.
- **Nothing deployed. Nothing published. No publication approval given.**
- `meoclass1/index.html` has one nav link to `/meoclass1/pastpapers/`.

---

## 11. Standing content rules

- **`Notes-for-written-answers/` is never a verification source.** 45 coaching PDFs whose
  own pages state that certain statements/figures were *intentionally made wrong*.
  Discovery and question-scope evidence only. (Exception: `DOC-20251125-WA0009.pdf` is
  genuinely IRS Guidelines on Ballast Water Management 2018.) Now git-ignored.
- **MIW holds no licensed IMSBC Code.** Q1's Group C classification sits at
  `P2_AUTHORITATIVE_SECONDARY`, not P1. Acquiring the 2023 (07-23) and 2025 (08-25)
  editions is the highest-value unblock for every future cargo question.
- **The source copies are third-party scans, not official.** `official_source_verified` is
  `false` by design and is stated on the page.

---

## 12. Source PDFs — policy now enforced, not remembered

Six source copies under `meoclass1/pastpapers/docs/` are **git-ignored**. Previously they
were merely unstaged, so a single `git add -A` would have published watermarked
third-party material to a public repository.

**Recommendation, unchanged and now firmer given the repo is public: do not commit them.**
The pipeline has **no runtime dependency** on them — the toolchain passes in full with the
PDFs absent; the structured spec is the durable production input. Official sources are
used separately for verification and are cited in the verification records.

**Nothing was deleted.** All six remain on disk. Deleting them needs Founder approval.

---

## 13. Restart commands

```bash
cd /d F:\Marine-Intelligence-Weekly
git -c safe.directory=* status --short --branch
git -c safe.directory=* log -3 --oneline --decorate
python tools/pastpapers/run_toolchain.py --self-test
```

Visual review needs an HTTP origin — the browser tooling cannot inspect `file://` pages:

```bash
python -m http.server 8899 --directory F:\Marine-Intelligence-Weekly
```

then open `http://localhost:8899/meoclass1/pastpapers/index.html`.
Deep-link check: `QP2607.html#q5` must open Q5 already expanded.

Rebuild after a spec edit (never edit the HTML):

```bash
python tools/pastpapers/run_toolchain.py --self-test
```

---

## 14. Outstanding work — priority order

1. **Founder content and UI review of QP2607.** This is now the only thing in the way.
   The pages have still not been seen by the Founder. Everything machine-checkable passes.
2. Correct any defects found in review. **Edit the spec, never the HTML.**
3. Re-run the toolchain; confirm deterministic rebuild.
4. **Founder approval.**
5. Only then decide gating / publication / indexability — and work the four class B
   currency checks in §8 immediately before publishing, not earlier.
6. ~~Only after QP2607 is approved, build QP2601.~~ **DONE.** The Founder directed production to
   continue, and QP2601 is built and cross-paper validated — see §2b.
7. **Founder content and UI review of QP2601, QP2602 and QP2603**, alongside QP2607. Four decisions
   are waiting, all in §2d: the model-answer word band, whether `understand_first` should be pruned
   to the questions that genuinely need it, the pre-existing mobile sticky-chrome proportion, and
   the new corpus "live external list" state.
8. ~~Build QP2602 (February 2026).~~ **DONE.** ~~Build QP2603 (March 2026).~~ **DONE.**
   ~~Build QP2604 (April 2026).~~ **DONE** — see §2e.
   ~~Build QP2606 (June 2026), the last available sitting.~~ **DONE** — see §2f.
   **ALL SIX AVAILABLE 2026 SITTINGS ARE NOW BUILT. 54 questions. Production for 2026 is closed.**
   **May 2026 does not exist in the source set** — keep it unavailable, and note that the 2025
   serials confirm the gap is the examiner's, not the source set's. Add a `FIXTURES` entry to
   `ui_behaviour_test.cjs` for every new paper.

   **FOUR LINKED EXACT PAIRS** must each be corrected as a unit on review:
   QP2601 Q9 ↔ QP2602 Q4 · QP2602 Q7 ↔ QP2603 Q1 · QP2601 Q6 ↔ QP2603 Q4 · QP2602 Q3 ↔ QP2603 Q8.

   **SEVEN NEAR-LINKED APRIL QUESTIONS now join them.** A correction to **QP2601 Q3, Q4, Q6, Q7,
   Q8 or Q9** must be considered against **QP2604 Q3, Q4, Q6, Q7, Q8 and Q9**; and QP2604 Q2
   inherits from QP2602 Q3 / QP2603 Q8.

   **Tier D reuse carries three mandatory steps, now proven over two papers:**
   1. **Scan the reused object for sitting-relative prose** (`this paper`, `this sitting`,
      `this examination`, `weeks/months before`, a named month-year, a cross-reference to another
      question by number).
   2. **Sweep the ASSEMBLED spec afterwards** — never trust the patch list. It missed one in
      March and one in April, and the sweep caught both. **But adjudicate every hit by hand:**
      of 55 April hits exactly one was a defect, the rest being provisions and absolute historical
      dates.
   3. **NEW FROM APRIL — check whether the GOVERNING INSTRUMENT itself differs at the two
      sittings.** This is a category above re-anchoring: where the law changed, the limb must be
      **re-authored** and recorded as a currentness change. QP2604 Q7 is the worked example, and
      the 1958 Act was asserted on **eight** separate surfaces of the January object.
9. **After all six 2026 papers**, run the full pattern/repeat/reference analysis using
   `docs/2026_PATTERN_REGISTER.md`, then begin the 2025 papers. **THE SIX PAPERS NOW EXIST. This
   is the next session — see §18. It was deliberately NOT started during June production.**
10. **Only after more than one paper**, mature the skill draft and consider the production
   agent. Six papers now exist, so the skill draft is well supported — but **do not build the
   agent yet.**

**Search payload watch — THRESHOLD REACHED, MEASURED, NOT ACTED ON.** `index.html` carries **all
six** papers' search blobs: **54 questions, 181.4 KB total, of which the inlined search payload is
134.9 KB (74% of the page) and the `search_blob` field alone is 112.7 KB.** Projecting linearly,
twelve papers gives roughly **270 KB of payload**.

The §4 threshold — split into a fetched JSON file when the sixth paper is added — **has been reached
and deliberately not implemented**, because the June session brief reserved search architecture for
the Founder review and forbade redesign during production. **No performance problem is observable at
six papers.** This is now a §16 stop-condition item and a Founder decision: split at the threshold as
originally written, or defer to a measured user-experience trigger.

Q7 primary-source resolution is **done** (§8) and is no longer on this list.

**Running in parallel, on a separate track:** the corpus session works
`docs/QP2607_TRUE_SOURCE_DEMAND_MAP.md`. It does not block Founder review, and Founder review does
not block it. The QP track's next involvement is step 8 of that document's handoff sequence —
populating `reference_shelf` from returned object mappings. Nothing before then.

---

## 15. Defects found and fixed this session (visual review)

None of these were visible to the toolchain; all four needed a real browser.

| Defect | Fix |
|---|---|
| `.nav-btn` had **no CSS rule at all** — "Rapid revision" rendered `#0000EE` on `#0F172A`, ≈**1.9:1** contrast, unreadable | Rule added; now white on teal, **≈5.5:1** |
| **Mobile search input hidden.** Topbar and controls bar both claimed `top:0` at ≤768px; topbar won on z-index | `--topbar-h` measured in JS on load/resize/font-load; controls bar offsets by it |
| Sticky chrome consumed **50.9%** of a 375px viewport; 29px gap on desktop | **24.8%** on mobile, gap now −0.4px |
| All three `<title>` tags rendered the literal text `&mdash;` | `plain_text()` decodes entities before `esc_attr()` |

Measured after the fix: 17 filter buttons → 4; desktop sticky chrome 273px → 108.5px;
no horizontal overflow at 375px; `#q5` deep link opens expanded; searching
"general average" returns `July 2026 · Q5 · 16 marks → QP2607.html#q5`.

---

## 16. Stop conditions — require Founder decision

- **Publication, gating or removing `noindex`.** Blocked on Q7 regardless.
- **Committing the source PDFs**, or deleting them.
- **Merging this branch into `main`.**
- ~~Starting a second paper. Not until QP2607 is approved.~~ **LIFTED by Founder direction,
  2026-08-08.** The Founder directed production to continue through the six available 2026 sittings
  before a broader publication decision, under the standing instruction to **keep the production
  line moving**. QP2601 and QP2602 were both built under that direction. Starting **QP2603 (March)**
  needs QP2602 to be accepted first.
- **Building the autonomous production agent.**
- **Any change to the settled architecture in §4–§6** without test evidence of a defect.
- **Any change to the frozen V1 template in §2a** — adding a sixth learning mode, extracting shared
  CSS/JS, or making `RulesApp/repository/` the physical corpus master. All three are Founder
  decisions already taken; reopening one needs a Founder decision, not a session's judgement.
- **Populating `reference_shelf`** before a real resolvable corpus object exists. No placeholders.
- **Building any part of the viewer or resolver** — no PDF.js, no auth, no entitlement, no
  watermarking, no source ingestion. Only the `reference_href()` seam exists, and it stays a seam.

---

## 17. Known environment quirks

- A repo hook, `validate_antipatterns.py`, is misconfigured — its plugin path does not
  exist on disk, so it reports an error on every file write. It blocks nothing, but it is
  a no-op safety net. Worth fixing or removing.
- `package.json` sets `"type": "module"`, so Node test files must use `.cjs`.
- The in-app browser cannot inspect `file://` pages (they load as non-inspectable
  snapshots) and `Control_Chrome` is macOS-only. Serve over HTTP for visual review.

---

## 18. THE 2026 SET IS CLOSED — what the next session is, and what it must not do

**Production for 2026 is finished.** The next session is a **review and design session**, not a
production session. The June session deliberately did **not** start any of the following, and the
next one should take them in this order:

1. **The six-paper intelligence / refinement review.** All six papers, 54 questions, in front of the
   Founder. Six decisions are waiting and are now ripe because the complete dataset exists:
   the model-answer word band (45/54 fail it); `understand_first` pruning on QP2601;
   the pre-existing mobile sticky-chrome proportion; the corpus **live external list** state
   (now five instances, plus the **negative-claim** sub-class from June Q7); the **search payload
   threshold**, reached and measured at 134.9 KB but not implemented; and whether the **edition
   axis** finding from June Q3 changes the corpus object model.
2. **Design and build the generated ONLY QUESTIONS year sheet** — see §19.
3. **V1 freeze / refinement decisions.**
4. **2025 production strategy** — see §20.

> **These are reserved deliberately.** Turning June's observations into frozen product decisions
> inside a production session is exactly the drift the register exists to prevent. The pattern
> register is labelled **DATA COMPLETE — FOUNDER INTERPRETATION PENDING** for the same reason.

---

## 19. ONLY QUESTIONS YEAR SHEET — approved in direction, NOT built

**The Founder has approved the direction. It was deliberately not implemented during June
production.** Recorded here so the requirement survives the session.

**Concept:** a generated `questions-2026.html`, later `questions-2025.html`, showing every question
month by month **without answers**.

| Requirement | Detail |
|---|---|
| Generated | From the canonical paper specs. **Never hand-maintained**, exactly like `topics-<year>.html`. |
| Per item | month · Q number · full question text · marks · primary category · recurrence status · related sittings · link to the solved question where one exists |
| Recurrence display | Candidate-facing intelligence must distinguish **NEW** from **REPEATED**, with useful detail — **EXACT / NEAR / TOPIC** — and the occurrences and sittings |
| Missing months | May, or any absent month, must appear **explicitly** as *"No paper available in MIW source set."* — never silently omitted |

### A recurrence-model requirement to solve at design time, not now

**Annual aggregate status and historical-direction status are different things, and the year sheet
will expose the difference.**

A January question may belong to a family that recurs in July. In the annual sheet it may correctly
read *"appears in 2 sittings"* — but internally January is the **first known occurrence within that
dataset** and July is the **repeated** one. Once 2025 and 2026 coexist, an **earlier-year
occurrence** must also be considered, and a question that looks "new" in 2026 may not be.

**Do not solve this architecture during a production session.** It is recorded as a design input.

---

## 20. THE 2025 SOURCE BUNDLE — inventoried only, NOT produced

The Founder has placed a 2025 Engineering Management question-paper bundle under
`meoclass1/pastpapers/docs/`. **A lightweight file inventory was taken and nothing else was done:
no transcription, no recurrence analysis, no answers, no specs, and no files were moved, renamed or
deleted.**

### Inventory — 11 files, all readable, all Engineering Management, all nine questions

| Month | Filename | Serial | Pages | Bytes | Readable | Likely source paper |
|---|---|---|---|---|---|---|
| January | `JANUARY 2025.pdf` | `EM – 2501` | 3 | 222,721 | yes | yes |
| February | `FEBRUARY 2025.pdf` | `EM – 2502` | 2 | 204,437 | yes | yes |
| March | `MARCH 2025.pdf` | `EM – 2503` | 2 | 222,263 | yes | yes |
| April | `APRIL 2025.pdf` | `EM – 2504` | 2 | 223,717 | yes | yes |
| **May** | **— absent —** | **(2505 missing)** | — | — | — | — |
| June | `JUNE 2025.pdf` | `EM – 2506` | 2 | 272,127 | yes | yes |
| July | `JULY 2025.pdf` | `EM – 2507` | 3 | 225,320 | yes | yes |
| August | `AUGUST 2025.pdf` | `EM – 2508` | 2 | 223,183 | yes | yes |
| September | `SEPTEMBER 2025.pdf` | `EM – 2509` | 2 | 225,337 | yes | yes |
| October | `OCTOBER - 2025.pdf` | `EM – 2510` | 3 | 241,977 | yes | yes |
| November | `NOVEMBER 2025.pdf` | `EM – 2511` | 2 | 232,004 | yes | yes |
| December | `DECEMBER  - 2025.pdf` | `EM – 2512` | 2 | 234,066 | yes | yes |

Every file carries `EXAMINATION OF MARINE ENGINEER OFFICER`, the subject `ENGINEERING MANAGEMENT`
and nine question markers. **Approximately 99 additional question instances.**

> ### **MAY IS ABSENT — AND THE SERIAL NUMBERING PROVES IT IS THE EXAMINER'S GAP**
>
> The serials run `EM–2501, 2502, 2503, 2504, **2506**, 2507 … 2512`. **There is no 2505.** May is
> missing from the examiner's own numbering, not merely from the files the Founder supplied — and
> May is likewise absent in 2026. This is a much stronger statement than "no file was provided",
> and it should inform the year-sheet design in §19.

**Filename inconsistency, recorded and not corrected:** `OCTOBER - 2025.pdf` and
`DECEMBER  - 2025.pdf` (two spaces) do not match the pattern of the others. This is the same class
of anomaly as `06- JUNE - 2026.pdf` in the 2026 set. **Recorded, not renamed.**

### PROVENANCE WARNING FOR WHOEVER PRODUCES 2025

The 2025 files come from the same third-party host as the 2026 set and carry the same material:

- **Host branding and purchase advertising.** This repository is **PUBLIC**. Host branding must
  never reach a spec, a generated page or the manifest — `validate_spec.py` rejects `host_branding`
  and trap 14 scans pages, specs *and* the manifest.
- **Host-printed recurrence annotations** such as `2024/MAR/Q5`. These are **DISCOVERY ONLY**.
  They are **not** canonical recurrence, and the 2026 set proved why: April's table over-claimed on
  one question and under-claimed on another, and June's table under-claimed on two.
  **Canonical recurrence is decided by comparing actual question stems**, then adjudicated by hand.
- **The question-paper wording itself is source-copy content** and requires the same
  character-level transcription and visual verification every 2026 paper received.

**Do not delete the raw local files** merely because they carry branding.

### LOCATION — flagged, not changed

**The 2025 bundle currently sits under `meoclass1/pastpapers/docs/`**, alongside the six 2026
source copies and the project's own markdown documentation. **No file was moved this session**, and
none should be until the Founder decides.

> **RECOMMENDATION FOR THE REVIEW SESSION.** `docs/` is where the product's *documentation* lives.
> Mixing seventeen raw third-party source PDFs into it is workable but is not the long-term shape,
> and the risk is not theoretical: everything under `meoclass1/pastpapers/docs/` that is not
> git-ignored is publishable, and this repository is public. **A dedicated raw-source area, kept
> git-ignored, is the cleaner arrangement.** The 2026 PDFs are already git-ignored; **confirm the
> 2025 files are covered by the same ignore rule before any commit that touches `docs/`.**

**Nothing about 2025 production has been decided or started.**
