# SESSION HISTORY — MEO Class I Written Questions

**Historical record only. For current state use [`../CURRENT_STATUS.md`](../CURRENT_STATUS.md).**

This file is **append-only evidence**. Nothing in it is authoritative about the present, and
nothing in it is policy. Where a section here restates a rule, the governed protocol file that
owns that rule wins — see [`../PRODUCTION_PROTOCOL_INDEX.md`](../PRODUCTION_PROTOCOL_INDEX.md).

Sections are in their original order, oldest master section first, then §22 onward in the order
they were written. Wording, dates, commit ids, paper ids, counts, decisions and mistakes are
preserved verbatim from `CURRENT_STATUS.md` as it stood at commit `850bdde`. **Old records were
not corrected to match current state — that is what makes them evidence.**

Two structural changes were made during the split, and nothing else:

1. The master section's heading was retitled to say what it is (it was previously the file title).
2. The duplicate `# 31` heading was renumbered to `§30.6` and marked superseded; the completed
   QP2509 section keeps `§31`.

Relative links to sibling protocol files gained a `../` because this file sits one directory down.

---

## APPEND FORMAT — for FUTURE entries only

New entries use the schema below. **Do not retrofit it onto the records already in this file**;
they stand as written.

```markdown
# §NN — <session / paper> — <YYYY-MM-DD>

## Outcome
## Branch / commits
## Key findings
## Corpus delta
## QA
## Next action
```

Append at the end. Take the next free `§NN`. Never renumber an existing section.

---

# §1–§21 — CURRENT STATUS master section as it stood to 2026-08-11 (historical)

**Canonical restart document for the Past Written Papers product.**
Last updated: 2026-08-11, after **QP2509 SEPTEMBER 2025 — COMPLETE** (§31).
Read this first.

---

## CURRENT STATE — read this table, not the history below

| | |
|---|---|
| **Corpus** | **252 questions / 99 solved / 153 unsolved** — 28 papers, **11 solved**, 17 answerless intake |
| **Solved papers** | QP2601, QP2602, QP2603, QP2604, QP2606, QP2607 (2026) · QP2403 · QP2506 · QP2508 · **QP2509** · QP2510 |
| **Toolchain** | ALL STAGES PASS, 110 warnings; `REUSE SELFTEST` PASS; `health_check.py` 0 errors; double build **23 artefacts, 0 byte differences** |
| **Branch** | `pastpapers/qp2509-founder-review`, cut from `0d7f872` |
| **Published** | Nothing. No paper merged to `main`; all pages `noindex` and ungated |
| **Current paper** | **QP2509 September 2025 — COMPLETE, 9 / 9 authored, built, QA green. FOUNDER REVIEW.** §31 |
| **Open defect** | **Host recurrence edges are DIRECTIONAL** in the donor derivation — an earlier paper cannot see a later paper that names it. Cost one missed donor this session. §31.3 |
| **Tier D (derived)** | **21** of 153 unsolved; QP2509 promoted 3 questions C→D and improved 1 |
| **Next paper** | **QP2404 April 2024** — 3/9 Tier D, family reach 5, 1 temporal flag. §31.5 |
| **Standing stop conditions** | §28.13, unchanged |

Everything below this table is **historical narrative**, newest section first. A section marked
*superseded* was accurate when written and is retained as the record of how a decision arose — it is
not the present state.

---

> ## THIS FILE IS **STATE**, NOT **POLICY** — added 2026-08-10
>
> Stable policy now lives in governed protocol files. Start from
> **[`PRODUCTION_PROTOCOL_INDEX.md`](../PRODUCTION_PROTOCOL_INDEX.md)**, which defines precedence
> and routing:
>
> | File | Owns |
> |---|---|
> | [`PASTPAPER_PRODUCTION_PROTOCOL.md`](../PASTPAPER_PRODUCTION_PROTOCOL.md) | sources, spec→build, learning architecture, branch/review rules |
> | [`TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md`](../TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md) | sitting-date truth, donor reuse, recurrence, contamination sweeps |
> | [`EXECUTION_EFFICIENCY_POLICY.md`](../EXECUTION_EFFICIENCY_POLICY.md) | how work is executed on this project |
> | [`QA_AND_HANDOVER_PROTOCOL.md`](../QA_AND_HANDOVER_PROTOCOL.md) | validation, determinism, Git, report schema |
>
> **Where this file restates a rule that a protocol file also states, the protocol file
> wins.** Sections here that read as policy — naming, architecture, template, provenance,
> standing content rules, source-PDF policy, restart commands, environment quirks — are
> retained as **historical record of how the rule arose**, not as the authoritative statement
> of it.
>
> This file should answer only: *where are we now, what was completed, what is next, what is
> blocked.* Do not add policy to it. Append state; do not rewrite history.
>
> ### ✔ STATE CONFLICT RESOLVED — 2026-08-10, at the start of QP2506 production
>
> The conflict was between the **§27 research-checkpoint header** (QP2510 *"NOT built, NOT
> solved"*, corpus **252 / 72 / 180**) and the repository.
>
> **The repository was right and the header was stale.** Re-verified at `30de4b3` before any
> QP2506 work:
>
> | Evidence | Result |
> |---|---|
> | `health_check.py` | 9 solved papers, 19 intake; **81 manifest deep links**, 171 intake questions; 0 errors, 0 warnings |
> | Generated pages | `QP2510.html` present and reproducing exactly from its spec |
> | Git history | `b6ecd40` *Build QP2510 and recompute the three-year donor intelligence*, then `4d0487a`, then `30de4b3` |
> | §28 of this file | already recorded **252 / 81 / 171** and the post-build donor analysis |
>
> **The §27 header simply predated the §28 build and was never demoted.** §27 has now been
> marked superseded and the CURRENT STATE table above carries the live figures. No historical
> section was rewritten and no count in §26–§28 was altered.

---

> # **§31 IS THE NEWEST SECTION. READ IT FIRST.**
>
> **QP2509 September 2025 is COMPLETE: 9 of 9 authored, built, toolchain ALL STAGES PASS,
> `REUSE SELFTEST` PASS, determinism 23/23 byte-identical.** Corpus **252 / 99 / 153**,
> 11 solved papers. Branch `pastpapers/qp2509-founder-review`.
> Headline: **the Q9 donor cited `A.1207(34)`, adopted 3 December 2025 — three months AFTER
> the sitting — on FOURTEEN surfaces, and its own "common mistake" bullet was inverted.** The
> operative edition is `A.1186(33)`. Second finding: **host recurrence edges are directional**,
> so QP2509-Q6 was scored "no donor" when a near-identical built answer existed (§31.3).
> Next paper: **QP2404 April 2024** (§31.5).

> # **§30 — superseded by §31. The donor-readiness fix and the QP2509 pre-authoring anchor.**
>
> Its temporal adjudications remain valid and were the input to §31; its "0 / 9 authored,
> spec untouched" state does not.

> # **§29 — superseded by §31 for the handover; still current for QP2506.**
>
> **QP2506 June 2025 is COMPLETE: 9 of 9 authored, built, toolchain ALL STAGES PASS.**
> Corpus **252 / 90 / 162**, 10 solved papers. Branch `pastpapers/qp2506-founder-review`.
> Headline: **the IMO places of refuge guidance is A.1184(33), which revoked A.949(23) on
> 6 December 2023 — eighteen months BEFORE this sitting.** Second finding: the generated reuse
> map understates Tier D because it reads a stored field instead of computing it (§29.3).
> Next paper: **QP2509 September 2025** (§29.6).

> # **§28 — superseded by §29 for the handover; still current for QP2510 and the rhythm finding.**
>
> **QP2510 October 2025 is COMPLETE: 9 of 9 authored, built, toolchain ALL STAGES PASS.**
> Corpus **252 / 81 / 171**, 9 solved papers. Branch `pastpapers/qp2510-founder-review`, head
> `30de4b3`. Its two load-bearing findings: **QP2510 created ZERO new donors** (§28.9), and a
> pure temporal adaptation must be budgeted as *product*, not as capacity building (§28.10).
> Next paper: **QP2506 June 2025** (§28.12).

> # **§27 — SUPERSEDED by §28. The research checkpoint that preceded the QP2510 build.**
>
> **At the time this was written**, QP2510 was a RESEARCH CHECKPOINT: every temporal blocker
> resolved against primary sources, but NO answer authored, and corpus stood at **252 / 72 /
> 180**. §28 then authored and built the paper. The temporal adjudications recorded here remain
> valid; the counts and the "NOT built" state do not.
>
> Headline: **the Carriage of Goods by Sea Act 2025 does NOT carry the Hague-Visby position
> unchanged.** It redefines "goods" to *include* live animals and deck cargo, omits Article IV bis,
> adds a three-month judicial extension of the time bar, and re-letters Article I throughout.
>
> A **fourth** item was found and closed: **A.1187(33) was still current at the sitting.** Its
> successor A.1208(34) was adopted **3 December 2025 — after the paper** — so citing it would be
> future-date contamination.

> # **§26 — superseded by §27 for the QP2510 handover; still current for the solved corpus.**
>
> **QP2403 March 2024 is COMPLETE: 9 of 9 authored, built, toolchain ALL STAGES PASS.**
> Branch `pastpapers/qp2403-founder-review`. Solved count **63 → 72 of 252**; 180 unsolved.
> **QP2510 October 2025 goes 0/9 → 9/9 Tier D** — metadata only; it is NOT built and NOT solved.
> Five QP2510 intake temporal flags corrected: **Q2, Q5, Q9 HIGH; Q1, Q7 MEDIUM.**
> The previous session's open question is **CLOSED**: both 2025 Indian carriage Acts came into
> force **10 September 2025**, five weeks before the October sitting.

> # **§25 — superseded by §26. The checkpoint that produced Q5 and Q6.**
>
> QP2403 was deliberately stopped at 2 of 9 rather than lower verification quality. That decision,
> and the whole-paper groundwork it produced — the source re-read, the QP2510 pair audit, the tier
> classification and the nine-question temporal sweep — are recorded in
> `verification/QP2403/DEDUP_AND_SOURCE_PLAN.md` and were **used, not redone**, by §26.

> # **§24 — superseded by §25, still current for the solved corpus.**
>
> **QP2508 August 2025 is SOLVED — 63 of 252 questions built, 7 solved papers.**
> Branch `pastpapers/qp2508-founder-review`. Next session is **QP2403 March 2024**.
> Two temporal findings, one of which the intake flag missed; three generator defects fixed.

> # **§22 — superseded by §24, still current for the 2025 intake picture.**
>
> Branch **`pastpapers/2025-question-intake`**, cut from `217fbba` — the accepted content baseline,
> deliberately **not** the Security V2 branch. Security V2 stays frozen at `eaedfda` and was not
> touched.
>
> **All eleven 2025 papers are transcribed. 99 questions, questions only, no answers anywhere.**
> The corpus is now **17 papers / 153 questions**, 54 of them with built answers.
>
> **The six 2026 paper pages are byte-identical. 54 solved questions unchanged.**
>
> **The next session is 2025 SOLVED-PAPER PRODUCTION — BATCH 1, and it must start with QP2508
> (August), not January.** August carries **8 of 9** Tier D donors. See §22.

> # **§21 — the 2026 V1 product review. Still current except where §22 supersedes it.**
>
> The review session promised by §18 has happened. Branch **`pastpapers/2026-v1-product-review`**,
> cut from `0c6932a`. It produced the six-paper intelligence review, the V1 decision register, the
> generated **ONLY QUESTIONS** year sheet, the **free January Solved QP sample**, the commercial and
> access architecture, and the 2025 strategy.
>
> **All six papers and all six specs are byte-identical to `0c6932a`.** No spec was edited, no
> validator was changed, nothing was published, nothing was merged.
>
> **Two findings in §21 need a Founder decision before publication**, and one of them is a blocker:
> the answer-length band, and the third-party recurrence table that currently ships to students.

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

---

## 21. THE 2026 V1 PRODUCT REVIEW SESSION — 2026-08-09

**This is the session §18 reserved. It was a review and design session, not a production session.**

| | |
|---|---|
| Branch | **`pastpapers/2026-v1-product-review`**, cut from `0c6932a` (QP2606 completion) |
| Previous branches | all six preserved and untouched |
| Baseline | `ALL STAGES PASS`, 6 specs, 54 questions, UI 6 pages, 47 warnings |
| Close | `ALL STAGES PASS`, **26 stages** (4 new), 47 warnings — unchanged |
| Regression | six paper pages and all six specs **byte-identical to `0c6932a`** |

### 21a. Deliverable documents

| Document | Contents |
|---|---|
| `docs/2026_SIX_PAPER_INTELLIGENCE_REVIEW.md` | dataset, recurrence, families, answer length, five-mode verdict, taxonomy, **V1 decision register**, True Source six-paper ranking |
| `docs/SOLVED_QP_COMMERCIAL_ARCHITECTURE.md` | traced payment/auth flow, **security findings**, entitlements, login, email, delivery, SQ integration, folder decision |
| `docs/2025_PRODUCTION_STRATEGY.md` | A→E intake staging, the 2025 statute-boundary risk, sequencing |

### 21b. New products — built, tested, NOT published

| Artefact | Path | State |
|---|---|---|
| Questions-only year sheet | `meoclass1/pastpapers/questions-2026.html` | generated, **noindex** |
| Free conversion sample | `SQ/solved-qp-sample-january-2026.html` | generated, **noindex** |
| Projection config | `meoclass1/pastpapers/sample/QP2601.sample.json` | hand-maintained |

New tools: `recurrence_model.py` · `build_questions_year.py` · `questions_year_check.py` ·
`build_sample.py` · `sample_check.py`. Four new toolchain stages: **QYEAR BUILD · QYEAR CHECK ·
SAMPLE BUILD · SAMPLE CHECK**.

> **STANDING RULE, same class as the `FIXTURES` rule.** Adding a paper requires nothing for the year
> sheet — it is generic. But **`sample_check.py` must keep passing**, and it will start failing if a
> future paper joins a recurrence family containing a sample demo question. That failure is correct
> and must be resolved by changing the sample, never by weakening the check.

### 21c. THE CHRONOLOGY DEFECT — found and fixed in the derived layer

**`recurrence_class` is an AUTHORING field and must never face a candidate.** Production order is
not sitting order, and on three of 54 questions they now disagree outright:

| Question | Sitting | Stored | Chronological truth |
|---|---|---|---|
| QP2601-Q3 | January | `near_recurrence` | **first occurrence** |
| QP2602-Q3 | February | `near_recurrence` | **first occurrence** |
| QP2607-Q1 | July | `new` | **a repeat** — set in Feb, Mar and Apr first |

`reused_from` is an authoring-lineage pointer (July was the pilot and was built first), not a
chronological one. **`recurrence_model.py` derives status from `(year, month)` only** and consumes
`reused_from` as an undirected edge. **No spec was changed** — the stored field is correct for what
it records. This is exactly what §19 predicted the year sheet would expose.

**Canonical chronological recurrence at six papers:** 33 set once · 8 first occurrence ·
4 repeat same wording · 9 repeat reworded. **8 families over 21 questions.**

### 21d. FOUNDER DECISIONS WAITING

1. **Answer-length band — evidence is now decisive.** Correlation of answer words against printed
   limbs **0.103**, named sub-tasks 0.560, **core points 0.827**. Words per core point: mean 29.6,
   σ 4.23. **Recommendation: retire 450–650 and warn outside 20–36 words per core point** — 3 of 54
   outside, against 47 of 54 today. Validator change = Founder decision. **Not made.**
2. **PUBLICATION BLOCKER — the host recurrence table ships to students.** `build_paper.py:435` and
   `build_index.py:417` render the third-party source copy's own recurrence annotation **outside**
   the `if not publish:` guard. Policy classes it discovery-only and the 2026 set measured it wrong
   in both directions. Recommendation: replace it with the canonical `recurrence_model` output.
   **Not changed** — it alters six approved pages.
3. **`understand_first`** — prune QP2601 only (9/9 against 6/9, 7/9, 6/9, 6/9 elsewhere); five
   QP2604 questions improve automatically.
4. **Solved QP price** — `PRICE_TBD`. `sample_check.py` fails the build if any rupee value renders.
5. **Free/paid placement of the year sheet** — MIW recommends **free and indexable**.
6. **Search payload split** — recommendation changed to **DEFER to a measured UX trigger** rather
   than splitting on the six-paper threshold. No observable problem.

### 21e. SECURITY — the existing commerce stack, traced

Findings in full in `SOLVED_QP_COMMERCIAL_ARCHITECTURE.md` §2. Three matter here:

- **The paid content is not access-controlled.** `meoclass1/QB1_A.html:165` is a client-side regex
  on `miw_auth=1` — a non-HttpOnly cookie whose value is the literal `1`. **There is no `vercel.json`
  and no `middleware.js` in the repository**, so `curl` returns any paid file in full.
- **The client sets the price.** `api/create-order.js:77` takes `amount` from the request body;
  `verify-payment.js` verifies the signature correctly but never checks the amount.
- **There is no entitlement model.** Adding Solved QP on top would grant it to every existing Oral QB
  customer, and vice versa.

> **Solved QP must not ship on this stack unchanged.** The recommended V1 is a ~40-line
> `middleware.js` gate plus a server-side price table and a per-product entitlement set — extending
> the three existing endpoints, not cloning them.

### 21f. Folder decision — **DO NOT MOVE**

Canonical content stays at `meoclass1/pastpapers/`. Commercial independence comes from the gate and
the entitlement, not from the directory name. Reasons in `SOLVED_QP_COMMERCIAL_ARCHITECTURE.md` §7.

### 21g. Sample selection — a commercial constraint the recurrence model exposed

The January sample's two full demos are **Q1 (Low-Load Two-Stroke Operation)** and **Q5 (Tank
Corrosion, Coatings and the CTF)**. Both are **recurrence-family singletons**.

**Six of January's nine questions are the first occurrence of a family that returns later in 2026**,
so publishing one in full publishes its paid twin — and **Q3's family reaches QP2607-Q5, the July
paper the storefront exists to sell**. `build_sample.py` enforces this and refuses to build
otherwise. A consequence worth recording: **no legal-archetype demonstration is available in
January**, because Q3, Q4 and Q7 are all family firsts.

### 21h. Verified at source this session

- **The 2025 serial gap.** Extracted from page 1 of all eleven PDFs: `2501–2504, 2506–2512`, **no
  2505**. May is the examiner's gap in both years. This now appears on a candidate-facing page, so
  it was re-verified rather than inherited.
- **All 17 source PDFs are git-ignored** (`.gitignore:42`). The §20 commit risk is **closed**.
- **`validate_spec.py` already tolerates an answerless question** (`answer_status: "Not Built"`), so
  2025 Stage A needs no validator change.

### 21i. Mobile chrome

The year sheet was measured at 375px, found at **56.3%** sticky chrome, and **fixed to 31.7%** by
making the two filter rows single-line and horizontally scrollable. The paper pages' pre-existing
51–60.5% is unchanged and remains a Founder decision — but the fix pattern is now proven and cheap.

### 21j. What this session did NOT do

No spec edited · no validator changed · no generated paper page changed · nothing published ·
`noindex` intact · **`SQ/index.html`, `SQ/pay.html` and `api/**` untouched** · no Razorpay pricing
touched · no test orders issued · no 2025 production · no merge to `main` · no production agent.

---

# §22 — 2025 QUESTION INTELLIGENCE. Eleven papers ingested, cross-year map built.

**Session of 2026-08-09. Branch `pastpapers/2025-question-intake`, cut from `217fbba`.**
No answer was authored. No paper was published. Nothing was merged to `main`.

## 22.1 What exists now — FACT

| | |
|---|---|
| Papers | **17** — 6 solved (2026), 11 intake (2025) |
| Questions | **153** — 54 with built answers, 99 questions only |
| 2025 papers | QP2501–QP2504, QP2506–QP2512. **May absent from the available source set, both years.** |
| Toolchain | `ALL STAGES PASS`, self-test included |
| 2026 regression | Six paper pages **byte-identical**. `solvedQP/`, the January sample and the oral promo untouched. |

Read next, in this order:

- `docs/2025_SOURCE_INVENTORY.md` — **generated.** What was transcribed, from what, and how far verified.
- `docs/2025_2026_RECURRENCE_AND_REUSE_MAP.md` — **generated.** Families, tiers, temporal risk, solving order.

Both are derived from `specs/*.json` by `tools/pastpapers/build_reuse_map.py`. **Do not hand-edit
either.** `run_toolchain.py` runs `--check` on them and fails the build if they go stale.

## 22.2 The toolchain learned a new concept — INTAKE

An intake spec is real transcribed questions with no answers. Before this session every stage
assumed each spec was a solvable paper, and the first answerless spec broke four of them.
`render_common.is_intake()` is now the single shared predicate. Consequences:

- an intake paper has **no paper page**, no verification directory, and null `url`/`deep_link`;
- search routes an intake question to its card on `questions-<year>.html`, so it can never return a
  result it cannot open;
- the topic page renders it as plain text plus **"Solution in production"**;
- health_check gained the **inverse** guard: an intake paper that *has* a page is an error.

Both new guards were positive-controlled by injection and both fired.

## 22.3 Recurrence — the payoff of fixing chronology first

Adding 2025 re-ranked 2026 with **no spec edit**, exactly as §21 predicted. Across 153 questions:
**104 families, 33 multi-sitting, 14 spanning both years.** The 2026 year sheet's scope sentence
corrected itself from "6 2026 sittings" to "7 sittings across 2025–2026".

**The similarity tool failed a third time, in a new way.** `QP2502-Q5` and `QP2504-Q5` are a
one-to-one task match — both are (a) scope of Indian admiralty law, (b) assessors and their
qualifications — and lexical similarity scores them at **0.101**. Any usable threshold discards
them. Conversely it offered `QP2502-Q5`/`QP2504-Q6` at **0.470**: admiralty law versus CII rating,
no relationship at all. **Eight same-task edges were adjudicated by reading both printed stems;
two candidates were rejected as TOPIC.** Host annotations were used only to propose candidates, and
their bare-month tokens (`2019/OCT`) linked wholly unrelated questions.

## 22.4 Reuse tiers — and why A and B are zero

**Tier D 20 · Tier C 79 · Tier A 0 · Tier B 0.**

Tier D is mechanical and certain: the question's family contains a 2026 question whose answer is
built and verified.

**A and B were deliberately not assigned, and that is a finding, not a gap.** Both claim an existing
canonical object covers the examiner demand, which cannot be asserted without reading the object —
and this session authors and verifies nothing. A keyword sweep of the 132-file Oral corpus was run
and rejected as a basis for B: no threshold produced a natural break (2 terms → 91 hits, 3 → 76,
4 → 49). A manufactured B count would have been planned against. The sweep output is recorded per
question in `reuse_evidence` as **named candidate files to read**, explicitly labelled discovery;
**71 of the 79 Tier C questions carry them.** Promotion to A or B belongs to the solving session.

## 22.5 Temporal risk — 24 flagged, and one that is worse than the rest

**24 of 99 flagged: 13 HIGH, 11 MEDIUM.** Classes: Indian statute boundary 9, IMO instrument in
flux 9, convention not yet in force 2, guideline edition 2, convention newly in force 1, recent
SOLAS chapter 1.

> **Every available 2025 sitting predates 15 March 2026**, when the Merchant Shipping Act, 2025
> commenced and repealed the 1958 Act by s.324(1).

So reuse runs **backwards** here: a 2026 answer pulled into a 2025 paper is a **statute
regression**, not a re-anchor. The April 2026 sweep found the 1958 Act asserted on **eight separate
surfaces** of one question object. Expect eight again, in reverse. A 2025 answer must **never** be
"corrected" to current law — it answers the examination as sat.

**`QP2508-Q8` is the single most dangerous Tier D reuse in the set.** It asks about the revised IMO
GHG strategy and the proposed MARPOL Annex VI Chapter V, and its own stem says the amendments are
"being considered". The status of the Net-Zero Framework moved repeatedly between August 2025 and
its 2026 relative. **The same question has a different correct answer at the two sittings.**

## 22.6 Marks and source anomalies

**13 of 99 questions print no mark allocation at all**, across four papers (QP2506, QP2509, QP2510,
QP2511). Each is recorded at 16 under instruction 2 with `printed_marks_absent` set. The omission is
demonstrably the printed copy's: `QP2506-Q9` prints none where the identical question printed (16)
in August, and `QP2511-Q4` prints none where the identical question printed (16) in December.

> **Correction to the record.** The commit message on `bec8543` says "Nine questions across five
> papers". The correct figure is **13 across four**, as derived in `2025_SOURCE_INVENTORY.md`, which
> is the authority. The specs were always right; the prose was not.

`QP2507-Q9` carries a host **"PROVIOUSLY ASKED"** block (the misspelling is the host's) quoting the
March wording beneath the July question. It is host annotation, not examiner text, excluded from
`text_verbatim` and recorded in a note.

## 22.7 Next session — BATCH 1 is AUGUST, not January

Figures below are the generated ones in `2025_2026_RECURRENCE_AND_REUSE_MAP.md` §6, which is the
authority. **Six of the eleven papers have no Tier D donor at all**, which is precisely why calendar
order is the wrong sequence.

| Paper | Sitting | Tier D | Temporal flags |
|---|---|---|---|
| **QP2508** | August 2025 | **8 / 9** | 4 |
| QP2506 | June 2025 | **4 / 9** | 1 |
| QP2509 | September 2025 | **3 / 9** | 2 |
| QP2511 | November 2025 | **3 / 9** | 2 |
| QP2502 | February 2025 | **2 / 9** | 2 |
| QP2501 · QP2503 · QP2504 · QP2507 · QP2510 · QP2512 | — | **0 / 9** | 2 · 3 · 4 · 2 · 0 · 2 |

**Start with QP2508.** Eight of its nine questions have a verified donor, so it converts more
research into review than any other paper — and it carries the joint-highest temporal load (4), so
it front-loads the two hardest problems, `QP2508-Q8` (GHG) and the Indian statute boundary on
`QP2508-Q5`/`Q9`, rather than meeting them later on a paper chosen for its date.

Then QP2506, QP2509, QP2511, QP2502. Calendar order would be the worst available choice: **January
has zero Tier D donors**, and it would research the same families twice — **QP2501 and QP2507 share
five families**, July 2025 being very largely a re-run of January and March.

**Every Tier D reuse carries three mandatory steps, none optional:** scan the donor for
sitting-relative prose; sweep the assembled spec afterwards rather than trusting the patch list (it
missed one in March and one in April); and check whether the governing instrument itself differed at
the two sittings.

## 22.8 Stop conditions still in force

- **Do not** author 2025 answers beyond the agreed batch.
- **Do not** ingest 2024 yet. The family model re-derives from the calendar, so 2024 will demote
  current "first occurrence" claims automatically — nothing is cached and no spec needs editing.
- **Do not** reopen Security V2 (`eaedfda`), Vercel, Razorpay or customer migration.
- **Do not** merge to `main`. **Do not** publish 2025 into `/solvedQP/`.
- **Do not** commit or delete the source PDFs. All 17 are git-ignored; verified this session.
- The two §21 blockers — the answer-length band and the third-party recurrence table shipping to
  students — are **still open** and now apply to eleven more papers.

---

# §23 — 2024–2026 INTELLIGENCE FOUNDATION. Three years transcribed, intake is closed.

**Session of 2026-08-10. Branch `pastpapers/2024-question-intake`, cut from `3a4aa14`.**
No answer was authored. No paper was published. Nothing was merged to `main`. Security V2 untouched.

Commits: `a09c1c6` recurrence provenance boundary · `c75b0aa` 2024 intake · `619e0ba` intelligence layer.

## 23.1 What exists now — FACT

| | |
|---|---|
| Papers | **28** — 6 solved (2026), 22 intake (2024, 2025) |
| Questions | **252** — 54 with built answers, 198 questions only |
| 2024 papers | QP2401–QP2404, QP2406–QP2412 |
| Source-page read-back | **2024: 24 of 24. 2025: 25 of 25.** Both years now complete. |
| Toolchain | `ALL STAGES PASS`, self-test included, one new stage |
| 2026 regression | Six paper pages changed on **recurrence surfaces only**. Answer content byte-identical. |

Read next, in this order. Both are **generated** by `tools/pastpapers/build_reuse_map.py`; do not
hand-edit either, and re-run it after any spec change or `run_toolchain.py` will fail on staleness.

- `docs/SOURCE_INVENTORY.md` — what was transcribed, from what, how far verified, every anomaly.
- `docs/2024_2026_RECURRENCE_AND_REUSE_MAP.md` — families, year-pair matrix, tiers, temporal risk,
  solving order, study intelligence.

`2025_2026_RECURRENCE_AND_REUSE_MAP.md` and `2025_SOURCE_INVENTORY.md` are **deleted**, not
archived. They were the same derivation over a smaller corpus and leaving them would leave two
generated documents making different current claims.

## 23.2 The §21 recurrence blocker is CLOSED, and it was worse than recorded

It was not only that the host's recurrence table shipped to students. It shipped on **four**
surfaces, and a fifth signal was wrong in a different way:

| Surface | What was there |
|---|---|
| Paper page, per question | `<p class="rec-note">Recurrence recorded on the source paper: 2018/APR, …` |
| `data-search` on every card | the same tokens, invisible on screen and present in the bytes |
| `pastpapers_content_index.json` | `recurrence`, `recurrence_class`, `prior_sittings`, published |
| `topics-<year>.html` | "Other recorded sittings: …" |
| Question-card badge | `recurrence_class` — an **authoring** field, in production order |

The last one is the subtle one. `recurrence_class` records what was true of the MIW corpus when the
question was *built*, and production order is not sitting order — for three questions in the 2026 set
it stated the opposite of the chronological truth. Both are now unrenderable anywhere:

- `host_recurrence_hint` — the host's printed table. Discovery provenance, kept in the spec, never rendered.
- `recurrence_class` — authoring record. Kept, never rendered.
- `recurrence_adjudication` — MIW's own reading of two printed stems, on 62 questions. Kept, never rendered.
- `prior_sittings` — a **count of host claims** presented as MIW truth. Deleted outright.

Everything candidate-facing now comes from `recurrence_model.py` and the calendar.
`recurrence_check.py` is a new toolchain stage that fails the build if a host sitting token or an
authoring class reaches any generated artefact, if a spec reinstates a retired key, or if the stem
normalisation is loosened. Every layer is positive-controlled. The UI test that used to **require** a
host code be findable is now a leak probe.

## 23.3 Printed marks are metadata — and the fix paid for itself immediately

`normalise_stem` compared the marks token as if it were examiner wording, so the same task printed
once with `(16)` and once without compared unequal and was labelled **"Repeated — reworded"** to a
candidate who could see the two stems were word for word the same.

A marks token is now stripped, but only when it is a bare parenthesised integer with whitespace
before the bracket **and** its value is one the question itself declares. `MEPC.312(74)` survives on
both tests. Regression: **4 questions** upgraded from reworded to same wording, **0 families merged**,
104 families before and after on the 2025–2026 corpus. All four were read; all four are correct
(`QP2508-Q5`, `QP2512-Q2`, `QP2602-Q5`, `QP2604-Q4` — each differs from its family's first sitting by
the trailing `(16)` and nothing else).

The payoff landed in the same session: `QP2510-Q5` is EXACT with `QP2403-Q5` **only** because of this
fix, which is what makes October 2025 a complete re-run rather than an eight-ninths one.

## 23.4 `reused_from` is not always "the same examiner task"

`QP2602-Q3` (formal safety assessment applied to **lithium batteries** in vehicles, containers and
ro-ro spaces) was authored from `QP2607-Q1` (the same method applied to **iron ore pellets** in bulk
carriers). What was reused is the method and the answer shape. Different cargo, ship type, hazard and
carriage requirements. Treating that pointer as a family edge told a candidate the lithium question
had been set five times when it had been set four.

`reuse_kind` now separates `same_task` from `shape_only`. Absent means `same_task`, so the 38 genuine
edges needed no annotation and the claim that needs evidence is the one that has to be written down.
All 39 edges were re-read this session; exactly one was rejected.

## 23.5 The headline finding — October 2025 is March 2024, reprinted whole

**Nine of nine questions, every one word-for-word identical.** Not a topic overlap, not a rewording.
`QP2403` and `QP2510` are the same paper set twice, nineteen months apart.

Adding 2024 moved **34 of the 153** previously transcribed questions with **no spec edited** — the
2024-readiness guarantee the chronological model was built for, tested for real. Two questions on
*published* 2026 pages went from "Once in this set" to "Repeated — same wording" because January 2024
had set them first (`QP2607-Q3` IACS/RO Code, `QP2607-Q9` Uberrimae Fidei).

Corpus shape: **174 families, 52 multi-sitting, 34 cross-year, 3 in all three years.**

| Year pair | EXACT | NEAR |
|---|---|---|
| 2024 internal | 8 | 0 |
| 2024 ↔ 2025 | 27 | 3 |
| 2024 ↔ 2026 | 8 | 1 |
| 2025 internal | 17 | 7 |
| 2025 ↔ 2026 | 23 | 11 |
| 2026 internal | 5 | 11 |

**TOPIC is deliberately not a canonical relation** and never has been. A shared subject is not a
repeated question. Shared-subject browsing is `topics-<year>.html`, which says nothing about
recurrence.

## 23.6 Reuse and temporal — 2024 did NOT move the 2025 map

**2024: Tier C 92, Tier D 7. 2025: Tier C 79, Tier D 20 — unchanged.** 2024 bridges no 2025 question
to a built answer, so the previous session's numbers stand exactly. A and B remain unassigned for the
same reason as before: neither can be claimed without reading the candidate object.

**Temporal: 40 of 198 flagged — 22 HIGH, 18 MEDIUM.** Classes: IMO instrument in flux 17, Indian
statute boundary 12, guideline edition 6, convention not yet in force 3, recent SOLAS chapter 1,
convention newly in force 1.

> Every available 2024 and 2025 sitting predates 15 March 2026. Reuse runs **backwards** and a 2026
> donor is a **statute regression**, not a re-anchor.

The sharpest new case is **`QP2410-Q4`**: it asks about the Hong Kong Convention in October 2024,
**eight months before that convention entered into force**, and its November 2025 relative
(`QP2511-Q8`) is answered on the opposite footing. Same family, same wording, opposite legal status.
`QP2508-Q8` (GHG) remains the single most dangerous Tier D reuse in the set.

## 23.7 Next session — BATCH 1 is still AUGUST 2025, then MARCH 2024

The three-year evidence did **not** overturn `QP2508`. It reinforced it and added a second paper
behind it that was invisible before.

| Paper | Sitting | Tier D | Family reach | Temporal flags |
|---|---|---|---|---|
| **QP2508** | August 2025 | **8 / 9** | 10 | 4 |
| **QP2403** | March 2024 | 0 / 9 | **12** | 0 |
| QP2506 | June 2025 | 4 / 9 | 9 | 1 |
| QP2404 | April 2024 | 1 / 9 | 10 | 1 |

*Family reach* is how many OTHER unsolved questions across the corpus sit in the same families as
this paper's questions.

- **QP2508 alone** puts **19 of the 198** unsolved questions in scope.
- **QP2508 + QP2403** puts **40 of 198** in scope — a fifth of the remaining corpus from two papers
  of research, because QP2403 carries the whole of QP2510 with it and has **zero temporal flags**.

Then QP2506, QP2404. Calendar order remains the worst available choice.

**PAPER-FIRST, ordered by family reach.** Not family-first. The evidence: 198 unsolved questions sit
in 150 distinct families, and only **85** of them share a family with another unsolved question. A
family-first pass would leave most papers incomplete for a long time while the customer product is a
complete paper — and paper-first ordered by reach already captures the leverage (40 of 198 from two
papers). The rule that matters is inside each paper: **research a family once**, then adapt per
sitting under the temporal review.

**Every Tier D reuse still carries three mandatory steps, none optional:** scan the donor for
sitting-relative prose; sweep the assembled spec afterwards rather than trusting the patch list (it
missed one in March and one in April); check whether the governing instrument itself differed at the
two sittings.

## 23.8 Stop conditions still in force

- **Do not** author answers beyond the agreed batch. 198 questions are `Not Built` and must stay so
  until a solving session is authorised.
- **Do not** ingest another year. Intake is closed at 2024–2026 until the Founder says otherwise.
- **Do not** reopen Security V2 (`eaedfda`), Vercel, Razorpay or customer migration.
- **Do not** merge to `main`. **Do not** publish 2024 or 2025 into `/solvedQP/`.
- **Do not** commit or delete the source PDFs. All 28 are git-ignored; verified this session.
- The **answer-length band** is the one §21 blocker still open. It is **DEFERRED TO SOLVED-PAPER
  PRODUCTION** — there are no new solved answers to measure, and the standing warnings are the
  existing 2026 answers exceeding the 450–650 band for 16 marks. Re-derive the band per printed limb
  when authoring resumes, not before.

---

# §24 — QP2508 AUGUST 2025 SOLVED. FIRST PAPER OF THE 2025 PRODUCTION RUN. 2026-08-10

> **§24 IS NOW THE NEWEST SECTION. READ IT BEFORE §23 AND §22.**

Branch **`pastpapers/qp2508-founder-review`**, cut from `7ca36b6`. Security V2 untouched at `eaedfda`.
Nothing merged, nothing published, no source PDF committed.

## 24.1 What exists now — FACT

| | Before | After |
|---|---|---|
| Papers | 28 | 28 |
| Question instances | 252 | 252 |
| **Solved** | **54** | **63** |
| Unsolved | 198 | 189 |
| Solved papers | 6 (all 2026) | **7 (2025–2026)** |

**QP2508 August 2025 is built: 9 / 9 READY, 0 class A blocking flags**, 21 re-verification flags
(B_CURRENCY_CHECK on the date-driven claims, the rest C_ACCEPTED_LIMITATION).

**All six 2026 specs and all six 2026 paper pages are byte-identical to `7ca36b6`.** No 2024 spec and
no other 2025 spec was touched. `questions-2025.html` now deep-links only QP2508's nine questions;
the other ninety 2025 questions remain answerless year-card destinations.

Toolchain: **ALL STAGES PASS, 59 warnings** (47 pre-existing + 12 QP2508 word-band). Build run twice:
**41 generated files, 0 differ.**

## 24.2 The two temporal findings — one predicted, one NOT

**Q8 (predicted, HIGH).** The intake correctly called this the most dangerous reuse in the set, and
it was. The February 2026 donor's status step is an account of the **MEPC/ES.2 adjournment of 14–17
October 2025** — an event **four months in the future** when this paper was sat. The step was
**replaced, not adapted**. The correct August 2025 position, fixed against **IMO Circular Letter
No.5005 of 11 April 2025** (the article 16(2)(a) circulation itself): approved at MEPC 83
(7–11 April 2025), **circulated for adoption at MEPC/ES.2 (14–17 October 2025)**, therefore
**approved and circulated, NOT adopted, NOT in force, adoption session not yet held.**

A second-order contamination was also caught: the donor lists "it enters into force in 2027" among
its *common mistakes*. At **this** sitting that was the reasonable expectation, so importing the
bullet would have taught the candidate that a correct August 2025 statement was an error.

**Q3 (NOT predicted — the intake flag was WRONG).** The intake records
`temporal_review: STABLE / LOW` for Q3. It is not stable. The donor closes on resolutions
**MSC.550(108)** and **MSC.555(108)** as amendments *in force* — true from **1 January 2026**, and
**five months in the future** at this sitting, where they were **adopted (MSC 108, May 2024) but not
yet in force**. An in-force date falls *between* this sitting and every donor in the family.

> **This was caught by the mandatory assembled-answer sweep, not by the flag.** Had the flag been
> trusted, a five-month currency error would have shipped inside a question labelled low risk.
> **The sweep is not a formality.** The intake flag is reported here, deliberately not silently
> patched — a future session should decide whether to correct the `temporal_review` on that question.

## 24.3 A verification upgrade the 2026 set should inherit

QP2602 Q8 records as an accepted limitation that the draft Chapter 5 text "was not read" and that
"**no consolidated text exists**". The second half is **not correct**: the draft consolidated revised
MARPOL Annex VI **is the annex to Circular Letter No.5005**, and it was read here — regulations 30
to 44 in full. Every Chapter 5 figure in QP2508 Q8 (5,000 GT threshold; GFI reference 93.3; Table 4
base/direct factors 4.0/17.0 for 2028 rising to 30.0/43.0 for 2035; US$100 and US$380 remedial units;
ZNZ 19.0 tightening to 14.0 from 2035; two-year surplus unit validity; the reg 44 review
contemplating 400 GT) is therefore **primary-verified**, where the donor held it at
authoritative-secondary.

**Recommended follow-up, not actioned:** revisit QP2602 Q8's `unresolved` and
`reverify_before_publication` in the light of this.

## 24.4 Indian statutory boundary — resolved, and sharper than the donor's

Both Q5 and Q9 carried `INDIAN STATUTE BOUNDARY / HIGH`. **The boundary lies after this sitting**, so
the Merchant Shipping Act 1958 governs both, exactly as it did for the February 2026 donors — **no
statutory regression was required**. What this sitting adds is a better fact than the donor's
"five weeks":

> The **Merchant Shipping Act, 2025** (Act No. 24 of 2025) received the assent of the President on
> **18 August 2025 — the same month as this examination** — and still did not commence until
> **15 March 2026** (S.O. 1244(E)). **Assent is not commencement.**

That is now the teaching point of Q5, and it ties to Q7 (adoption versus entry into force) and Q8
(the same problem in an IMO instrument). The Bharatiya Nyaya Sanhita 2023 had been in force since
**1 July 2024**, over a year before this sitting, so citing the IPC was *already* an error here.

## 24.5 Three generator defects found by being the first non-2026 paper

**(a) `build_reuse_map.py` dropped a whole year.** `_solved_years()` returned every year containing
*any* built answer, and three planning sections then skipped those years wholesale. Solving one 2025
paper made 2025 a "solved year" and **silently deleted the other ten 2025 papers — ninety unsolved
questions — from the tier table, the temporal table and the recommended solving order.** Solving
QP2403 next would have deleted 2024 too, leaving the map empty.

Fixed: exclusion is now **per paper** (`_solved_papers`), open years are those still containing an
unsolved question, and tier counts count unsolved questions only. **Positive control run:** QP2506
temporarily marked fully built → QP2506 alone left the solving order, 2025 stayed in the tier table,
the other nine 2025 papers remained listed. Clean state restored.

**(b) `build_sample.py` mislabelled the commercial sample.** The offer block hard-coded "The complete
**2026** solved paper set" and then listed **August 2025** beneath it; the count read "every 6
sitting", ungrammatical for every N. Both now derive from the data: "The complete 2025–2026 solved
paper set … all 7 sittings". Wording only — no commercial activation.

**(c) `ui_behaviour_test.cjs`** required a `FIXTURES` entry for the new paper, as its own comment
says. Added, including the inverted host-recurrence leak probe. **61 passed, 0 failed.**

## 24.6 Reuse map — before and after

| Tier | 2024 before | 2024 after | 2025 before | 2025 after |
|---|---|---|---|---|
| C | 92 | 92 | 79 | **78** |
| D | 7 | 7 | 20 | **12** |

2025 D falls by the eight Tier D questions solved; 2025 C falls by one (Q6, the only Tier C). Totals
reconcile: 92 + 78 + 7 + 12 = **189 unsolved**.

**Seven unsolved questions gained a QP2508 donor**, and they are *date-adjacent*, which matters more
than the count:

| Question | Gains | Why it beats the 2026 donor |
|---|---|---|
| QP2506-Q9 (June 2025) | QP2508-Q5 | same statute era — no 15 March 2026 boundary to regress across |
| QP2509-Q2 (September 2025) | QP2508-Q2 | **same CII review window** (after MEPC 83, before 1 Jan 2026) — **zero temporal change needed** |
| QP2506-Q2, QP2511-Q9 | QP2508-Q7 | stable either way |
| QP2404-Q7, QP2502-Q2, QP2506-Q8 | QP2508-Q4 | stable either way |

## 24.7 Next session — QP2403 MARCH 2024. The recommendation HOLDS, on stronger evidence

| Paper | Tier D | Family reach | Temporal flags |
|---|---|---|---|
| QP2506 June 2025 | 4 / 9 | 5 | 1 |
| **QP2403 March 2024** | **0 / 9** | **12** | **0** |
| QP2510 October 2025 | 0 / 9 | 12 | 0 |

QP2506 is now top of the *readiness* table, but its reach fell from 9 to 5 — QP2508 already converted
what they shared. **QP2403's reach of 12 is the only one QP2508 did not touch**, and the decisive
fact is re-verified from the regenerated map:

> **All nine March 2024 questions map one-to-one onto October 2025** — Q1→Q1 through Q9→Q9.
> **QP2403 and QP2510 are the same paper.** Solving QP2403 takes QP2510 from **0/9 to 9/9 Tier D**.

It is the only paper in the corpus whose solution hands over a *complete second paper*; it has **zero
temporal flags**, unique at its size; and it is nine questions of genuinely new research, the
opposite workload from QP2508, which will test the pipeline where QP2508 did not.

**Next session: QP2403 — MARCH 2024 SOLVED-PAPER PRODUCTION.**

## 24.8 Open items carried forward

- **Answer-length band.** Now measurable. QP2508: **837–1141 words, mean 1029**. The 2026 corpus:
  median 905, range 572–1516, **7 of 54 inside the 450–650 band**. With QP2508 the band now fails
  **59 of 63** built answers, so it is not a useful warning as written. Evidence for re-deriving it:
  median **29.4 words per core point**, with QP2508 at 30–34 core points per question. **Founder
  decision still required; deliberately not changed here.**
- **The Q3 intake temporal flag is wrong** (§24.2). Reported, not patched.
- **`primary_category` divergence.** QP2602-Q9 is `Statutory Framework & Class`; the QP2508 intake
  classifies the identical question `Indian Maritime Legislation`. The **intake value was kept**, so
  that an answer build does not move a question on `topics-2025.html`. Pre-existing, reported.
- **QP2508 Q4 is one of four identical objects** (QP2601-Q9, QP2602-Q4, QP2604-Q9). A correction to
  any one must be applied to all four.

## 24.9 Stop conditions still in force

- **Do not** start QP2403's answers without authorisation. 189 questions remain `Not Built`.
- **Do not** ingest another year. Intake is closed at 2024–2026.
- **Do not** reopen Security V2 (`eaedfda`), Vercel, Razorpay or customer migration.
- **Do not** merge to `main`. **Do not** publish QP2508 into `/solvedQP/`. Founder review first.
- **Do not** commit or delete the source PDFs.

---

# §25 — QP2403 MARCH 2024: CHECKPOINT, NOT COMPLETE. 2026-08-10

> **§25 IS NOW THE NEWEST SECTION. READ IT BEFORE §24.**
>
> **QP2403 is 2 of 9 authored. The paper is NOT built and the toolchain is RED by design.**
> This is a deliberate checkpoint on the QP2606 precedent — stop rather than lower verification
> quality — not a failure and not a partial claim of completion.

Branch **`pastpapers/qp2403-founder-review`**, cut from `dedce2c` (the QP2508 completion).
Security V2 untouched at `eaedfda`. Nothing merged, nothing published, no source PDF committed.

## 25.1 What exists now — FACT

| | Before | After |
|---|---|---|
| Papers | 28 | 28 |
| Question instances | 252 | 252 |
| **Solved (built + page generated)** | **63** | **63 — unchanged** |
| QP2403 questions authored in the spec | 0 | **2 (Q5, Q6)** |
| QP2403 page generated | no | **no** |

**Every generated artefact is byte-identical to `dedce2c`.** `index.html`, the manifest,
`questions-2024.html`, `topics-2024.html`, the January sample and all seven built paper pages were
regenerated during testing and then **restored**, deliberately, so that the committed tree
contains **no dead link to a QP2403 page that does not exist**. The only content change is
`specs/QP2403.json` plus new verification records.

**The toolchain is RED and the reason is exactly one thing:** the corpus is **all-or-nothing per
paper**. `health_check.py`, `audit_paper.py` and `ui_behaviour_test.cjs` all require a generated
page for any spec containing a built question. Two authored questions therefore fail the build
until the other seven are authored. **Nothing else is broken.** `validate_spec.py` on QP2403 is
**0 errors, 2 warnings** (both the known word-band warning).

> **This is itself a finding worth recording: there is no valid "half-authored paper" state.**
> A future session must either finish a paper or leave its spec at intake. Reverting verified
> content to make a checker green was rejected as the wrong trade.

## 25.2 The three temporal findings — and the intake model is now 4 for 4 wrong

The mandatory sitting-date sweep was run on **all nine** questions, not only the authored ones.
**The intake recorded `STABLE / LOW` on all nine. Three are wrong, and all three are material.**

| Q | Intake | Truth at March 2024 |
|---|---|---|
| **Q2** Bill of lading | STABLE/LOW | **WRONG.** Governed by the **Indian Bills of Lading Act 1856** and the **Indian Carriage of Goods by Sea Act 1925** (as amended 1993, Hague-Visby). Both repealed in 2025 — Bills of Lading Act 2025 (assent 24 July 2025), Carriage of Goods by Sea Act 2025 (assent 8 August 2025). |
| **Q5** Cyber | STABLE/LOW | **WRONG.** `MSC-FAL.1/Circ.3/Rev.2` (7 June 2022) governs — **FIVE** functional elements. Rev.3 (4 April 2025) adds **Govern** for six, thirteen months *after* the sitting. |
| **Q9** MLC 2006 | STABLE/LOW | **WRONG.** The **2022 amendments** entered into force **23 December 2024**, nine months *after* the sitting. Social connectivity/internet, sized PPE, registered-owner financial-security certificates and ILO fatality reporting are **not** requirements at this sitting. |

> **A NEW INDIAN STATUTORY BOUNDARY.** Every prior finding concerned the MS Act 1958 → 2025
> boundary of 15 March 2026. Q2 crosses a **different** pair of Acts on a **different** date, in
> mid-2025 — and it falls **between QP2403 and QP2510**. §23.6's framing that "reuse runs
> backwards across one boundary" is **incomplete**. Commencement dates of the two 2025 Acts were
> **not** established and must be before QP2510-Q2 is answered; assent is not commencement.

**Two further currency facts, not flag corrections:** the **FAL Convention Maritime Single Window
became mandatory 1 January 2024**, two months before this sitting (Q1 must use it); and
**A.1187(33), 6 December 2023** replaced the 2021 Non-exhaustive List of Obligations under the III
Code, three months before the sitting (Q7). **IACS UR E26/E27 were NOT in application** — the
1 January 2024 date was withdrawn and the revised requirements apply from **1 July 2024**.

> **Treat `temporal_review` as populated at intake as UNEVALUATED, not as evidence.** It has now
> failed on QP2508-Q3 and on three QP2403 questions. Only the sweep is evidence.

## 25.3 Source re-read and the QP2403 to QP2510 pair audit — both COMPLETE

**Full visual re-read of all 3 pages at 150 dpi against the text layer: NO discrepancy, NO
transcription correction required.** New provenance fact: the source PDF was generated
**1 April 2024**, days after the sitting — a tighter sitting bound than any 2026 paper has.

**All nine pairs verified directly by string comparison, not inherited from the previous report.
The one-to-one claim HOLDS.** Seven **EXACT**; two **NEAR differing only in a printed marks
token** — Q5 (inserted `(16)`, semantically identical) and Q7 (**6+4+6 → 6+5+5**, identical
words: a new sub-class, *NEAR by limb-mark redistribution*).

> **But "the same paper twice" is true of the QUESTIONS and false of the ANSWERS.** Four of the
> nine carry a temporal delta across the nineteen months and **three are material (Q2, Q5, Q9)**.
> A session that treats QP2510 as a copy job will ship three legal errors. **Q6 is the cleanest
> donor on the paper**: identical question, identical marks, no temporal movement.

## 25.4 Reuse classification — zero Tier D, and one rejected near-miss

All 63 built answers reviewed by examiner demand. **Tier B x2 (Q3 general average, Q7 III Code),
Tier C x7, Tier D x0.** `reused_from` is null on all nine. **No false donor was manufactured.**

`QP2606-Q5` route step 6 ("Cyber risk") would have been offered by any lexical search for Q5. It
was rejected on two independent grounds — it is one step of an ISM Code question (the
QP2602-Q3/QP2607-Q1 *shape_only* precedent), and it is written on **Rev.3**, so importing it would
have placed a **non-existent functional element** in a March 2024 answer.

## 25.5 What was authored, and what "open the source" caught

**Q5** — cyber risk. `MSC-FAL.1/Circ.3/Rev.2` read in full. **Q6** — electronic record books.
`MEPC.312(74)` read in full. Both `Pilot Review Ready`, both with verification records.

**Eighth consecutive paper on which reading the instrument caught a summary error.** An automated
summary of MEPC.312(74) offered the **Ballast Water Record Book** (not MARPOL), "engine
maintenance and fuel consumption logs" (not a MARPOL record), and **omitted the Cargo Record Book,
the ODS Record Book and the NOx Technical Code engine parameter book**. The correct list at annex
2.1 is **seven** items. Limb (a) asks the candidate to name them *all*.

## 25.6 Measured statistics so far

| | Q5 | Q6 |
|---|---|---|
| Route steps | 7 | 7 |
| Core points | 43 | 44 |
| Model answer words | 1471 | 1318 |
| Words per core point | 34.2 | 30.0 |
| Study notes words | 1564 | 1464 |
| Retrieval cards | 10 | 10 |
| Reverify A / B / C | 0 / 1 / 3 | 0 / 1 / 2 |

Both exceed the 450–650 band, as 59 of the previous 63 do. **No validator change was made** and
no scoring proposition was trimmed to hit a number. Q5 at 34.2 words per core point is above the
corpus median of 29.4 and a further layering pass is a reasonable review action.

## 25.7 NEXT SESSION — finish QP2403. Do not start another paper.

**Everything below is already done and must NOT be redone:** the source re-read, the pair audit,
the tier classification, the temporal sweep on all nine, the source-demand map, and Q5 and Q6.
They are recorded in **`verification/QP2403/DEDUP_AND_SOURCE_PLAN.md`**, `Q5.md` and `Q6.md`.

**Author Q1, Q2, Q3, Q4, Q7, Q8, Q9**, then build, recompute the reuse map, and run the QP2510
donor test. Suggested order, cheapest first:

1. **Q7** — `A.1070(28)` has already been **read in full** and the paragraph map is in the plan
   (objective para 1, strategy para 3, scope para 6, KPIs paras 42–44, coastal paras 45–51, port
   paras 52–63). Note the trap: the Code's scope at para 6 is **six subject areas and does NOT
   include maritime security**, while IMSAS audits **nine treaty instruments**. Both answer
   "which instruments".
2. **Q3** — Tier B support from `QP2607-Q5`, `QP2602-Q6`, `QP2606-Q3`. What is *not* covered and
   must be researched: **contribution among the parties** (contributory values, GA bond and
   guarantee, the adjustment process) and limb (b)'s worked examples.
3. **Q9, Q2** — the two India/ILO temporal questions. The boundary facts are established; the
   substantive research is not.
4. **Q1, Q4, Q8** — expect `ENGINEERING_JUDGEMENT` and `C_ACCEPTED_LIMITATION` to dominate; Q4 and
   Q8 sit substantially outside the regulatory corpus, like `QP2606-Q6`. Do not manufacture
   citations for them.

Then: build, determinism double-build, `build_reuse_map.py` (verify **no year disappears** — the
§24.5 per-paper fix), the QP2510 0/9 → 9/9 Tier D test, UI review at 1280/375, a `FIXTURES` entry
for QP2403 in `ui_behaviour_test.cjs`, and the sample regression.

## 25.8 Stop conditions still in force

- **Do not** mark QP2510 built. A donor is not a solved target, and three of its nine questions
  need a substantive legal update rather than a re-anchor.
- **Do not** start any other paper. **Do not** ingest another year.
- **Do not** reopen Security V2 (`eaedfda`), Vercel, Razorpay or customer migration.
- **Do not** merge to `main`. **Do not** publish QP2403 or QP2508 into `/solvedQP/`.
- **Do not** commit or delete the source PDFs.
- **Write specs with LF line endings.** A patch script writing CRLF was caught this session; the
  rest of the corpus is LF and content-hashed comparisons depend on it.

---

# §26 — QP2403 MARCH 2024: **COMPLETE**. 2026-08-10

> **9 of 9 authored and verified. Paper built. `run_toolchain.py --self-test` = ALL STAGES PASS.**
> **63 → 72 solved of 252. 180 unsolved. Double build: 0 byte differences over 18 artefacts.**

## 26.1 What this session did, and what it deliberately did not redo

Authored **Q7, Q3, Q9, Q2, Q1, Q4, Q8** — the seven the checkpoint left. **Q5 and Q6 were not
touched**; they were reviewed against the finished paper and left unchanged (see §26.6).

The §25 groundwork was **used as given**: no re-read of the source paper, no re-run of the QP2510
pair audit, no re-derivation of the tier classification. That was the point of the checkpoint, and
it held.

## 26.2 Verification — every question opened its own primary source where one exists

| Q | Primary source | How obtained |
|---|---|---|
| Q1 | **FAL.14(46)**, 13 May 2022 | IMO resolutions CDN, read in full |
| Q2 | **Hague-Visby Rules**; **India Code** (BoLA 2025, COGSA 2025) | scheduled official text; India Code **by browser** |
| Q3 | **York-Antwerp Rules 2016**; **MIA 1963 ss.64–66** | IG P&I copy — **no text layer, so rendered at 160 dpi and read visually page by page** |
| Q4 | none — no instrument prescribes a propeller type | `regulations: []`, and that is correct |
| Q7 | **A.1070(28)** in full; **A.1187(33)** | IMO CDN; local true-source corpus |
| Q8 | none — operational question | `regulations: []`; ISM and SOLAS referred to by effect only |
| Q9 | **MLC 2006 as amended to 2018** | local true-source corpus — **the edition operative at the sitting** |

**Q9 is the methodological high point.** The corpus holds *both* ILO consolidations — to-2018 and
to-2022. Normalising both and probing term by term turned "the 2022 amendments were not in force"
from a recollection into a **reproducible textual fact**: `social connectivity` appears 0 times in
one text and 1 in the other. Six 2022-only provisions were identified and excluded that way.

The **positive** marker matters as much: **Appendix A5-I lists SIXTEEN items, not the original
fourteen**, because the 2014 amendments added the two financial-security entries. An answer that
says "sixteen" has dated itself correctly; one that says "fourteen" is pre-2017.

## 26.3 Temporal review — the intake flag is now 0 for 9 as evidence

All nine intake flags said `STABLE / LOW`. **Five are wrong or materially incomplete.**

| Q | Intake | Actual | Why |
|---|---|---|---|
| Q2 | STABLE/LOW | **CORRECTED — HIGH** | both Indian carriage Acts replaced between the sittings |
| Q5 | STABLE/LOW | **CORRECTED — HIGH** | Rev.2 → Rev.3, five elements → six |
| Q9 | STABLE/LOW | **CORRECTED — HIGH** | MLC 2022 amendments in force between the sittings |
| Q1 | STABLE/LOW | **CONFIRMED — MODERATE** | MSW became mandatory 1 Jan 2024, *two months before* the sitting |
| Q7 | STABLE/LOW | **CONFIRMED — LOW** | but A.1187(33) replaced the 2021 list *three months before* the sitting |
| Q3, Q4, Q6, Q8 | STABLE/LOW | **CONFIRMED — LOW** | with a recorded reason in each case |

> **Q1 is the mirror-image error, and it is new to the corpus.** The habitual risk is importing
> *later* law. Q1's risk is writing on *pre-2024* material and describing the Maritime Single Window
> as forthcoming — which would be wrong at this sitting. **The flag must be checked in both
> directions, not just for contamination from the future.**

## 26.4 The Q2 statutory boundary — the §25 open question is **CLOSED**

§25 flagged that commencement of the two 2025 Acts *"was not established and must be, before
QP2510-Q2 is answered — assent is not commencement"*. Established this session from **India Code by
browser** (it refuses automated retrieval — `curl` returns an HTML shell):

| Act | Commencement | Notification |
|---|---|---|
| **Bills of Lading Act 2025** (18 of 2025) | **10 September 2025** | S.O. **4083(E)** of 8 Sep 2025 |
| **Carriage of Goods by Sea Act 2025** (19 of 2025) | **10 September 2025** | S.O. **4082(E)** of 8 Sep 2025 |

Both fall **after** March 2024 and about **five weeks before** October 2025. Section **6(1)** of the
former reads *"The Indian Bills of Lading Act, 1856 (9 of 1856) is hereby repealed"*, with savings
at 6(2).

**Mitigation:** the 2025 Act **re-enacts rather than reforms** — its ss.2, 3 and 4 carry the same
three subjects as the 1856 Act's ss.1, 2 and 3. QP2510-Q2 therefore needs a **citation update, not
new law**.

> **STILL OPEN, deliberately:** whether **COGSA 2025 carries the Hague-Visby Rules unchanged**.
> **Read that Act before authoring QP2510-Q2.** It is the single open research item on the donor set.

## 26.5 Answer statistics — the paper sits at corpus density

| Q | Steps | Core points | Words | w/cp |
|---|---|---|---|---|
| Q1 | 7 | 61 | 1,635 | 26.8 |
| Q2 | 7 | 67 | 2,170 | 32.4 |
| Q3 | 7 | 64 | 1,941 | 30.3 |
| Q4 | 6 | 59 | 1,420 | 24.1 |
| Q5 | 7 | 43 | 1,471 | 34.2 |
| Q6 | 7 | 44 | 1,318 | 30.0 |
| Q7 | 7 | 54 | 1,848 | 34.2 |
| Q8 | 7 | **75** | 1,841 | 24.5 |
| Q9 | 7 | 71 | 2,082 | 29.3 |
| **Paper** | **62** | **538** | **15,726** | **29.2** |

**Paper mean 29.2 against the corpus centre of 29.4.** The 450–650 band warning fires on all nine
and remains **uncalibrated**; it is not evidence of verbosity here. The validator was **not**
changed.

## 26.6 Whole-paper layering review — Q5 and Q6 were **NOT** changed

§25 asked whether Q5 is over-layered. **Measured against the finished paper, it is not.** Q5 sits at
**34.2 w/cp — identical to Q7**, and its absolute length is the 4th shortest of nine. It carries the
*fewest core points* (43), which is a property of the question rather than of the writing. **No
change made.** Q6 at 30.0 is at the corpus centre. **No change made.**

Three questions did get layering passes at authoring time: Q7 (surveyor regime moved to Study
Guide), Q3 (two passes, 2,368 → 1,941), Q2 (route steps 6–7 colour moved to Study Guide).

## 26.7 QP2510 — **0/9 → 9/9 Tier D. Metadata only.**

`reuse_tier: D` plus `reused_from` on an unsolved spec is the established donor pointer (precedent:
QP2511-Q5 → QP2603-Q6). **No `answer_status` was touched. QP2510 is NOT built and NOT solved.**

| QP2510 | Donor | Class | Temporal delta | Production-usable? |
|---|---|---|---|---|
| Q1 | QP2403-Q1 | EXACT | cyber cross-ref Rev.2 → **Rev.3** | yes, one cross-ref update |
| Q2 | QP2403-Q2 | EXACT | **statutes replaced 10 Sep 2025** | **NO — read COGSA 2025 first** |
| Q3 | QP2403-Q3 | EXACT | none | **yes, as is** |
| Q4 | QP2403-Q4 | EXACT | none | **yes, as is** |
| Q5 | QP2403-Q5 | NEAR (marks token) | **Rev.2 → Rev.3, five → six elements** | substantive update to limb (B) |
| Q6 | QP2403-Q6 | EXACT | none | **yes, as is — cleanest on the paper** |
| Q7 | QP2403-Q7 | NEAR (**6+4+6 → 6+5+5**) | A.1187(33) currency check | yes, **re-weight** limbs (b)/(c) |
| Q8 | QP2403-Q8 | EXACT | none | **yes, as is** |
| Q9 | QP2403-Q9 | EXACT | **MLC 2022 amendments in force** | substantive update — **4 requirements to ADD** |

The four Q9 additions are **exact rather than approximate**, because they came from textual
comparison: social connectivity and internet access; appropriately-sized PPE and the precedence of
engineering controls over PPE; annual reporting of seafarer deaths to the ILO for a global register;
the registered owner on the financial security certificate.

**Five QP2510 intake temporal flags were corrected**, because the reuse map was reporting "stable"
for three questions carrying a material legal delta. That is precisely the failure this corpus keeps
hitting, and it is now visible in the generated artefact instead of hidden in it.

## 26.8 Two guard changes, each positive-controlled and then restored

- **`known_traps_check.py`** — the HATC guard used `'hatc' in src.lower()`, a substring test that
  also fires on **"hatches"**. QP2403-Q3 tripped it the moment it quoted York-Antwerp Rule II. It is
  now a **word-boundary** match. **Proved both ways:** injecting a real HATC source fires it;
  "hatches" alone does not. A *precision* fix — no true positive is lost.
- **`ui_behaviour_test.cjs`** — QP2403 fixture added; **61/61 pass**. The leak probe is `2011/SR8`,
  a host provider code unique to Q8 on this paper. **Proved by injection:** putting that code into a
  search alias and rebuilding makes the probe fail.

## 26.9 Sweeps

| Sweep | Result |
|---|---|
| Corpus transition | **252 / 72 / 180** — verified, not assumed |
| questions-2024 deep links | **exactly 9**, all QP2403, no others, no dead anchors |
| Determinism | **0 byte differences**, 18 artefacts, double build |
| Year survival in reuse map | **11 papers in 2024, 11 in 2025** — no year disappeared |
| Post-sitting years in model answers | **zero** mentions of 2025 or 2026 anywhere |
| QP2510 contamination | 2 hits, **both false positives** (FAL *2022 amendments*; the verb *govern*) |
| Host recurrence codes in output | **0 of 19** across every generated file |
| Candidate-facing field leak | none — the two field-name hits are in the build manifest, which no page fetches |
| UI 1280 / 375 | 9 cards, 5 modes, Answer pre-selected, search narrows live, all 9 anchors resolve, **no console errors, no horizontal overflow** |
| Regression | six 2026 papers, QP2508, their specs, the 2025/2026 year sheets and the public sample **byte-identical** |
| Security V2 | **untouched** |

## 26.10 NEXT SESSION — **QP2510 OCTOBER 2025**

Unambiguous on the data: QP2510 is the **only** unsolved paper at **9/9 Tier D**, and its donor is a
paper solved in this session with a verification record for every question. Four of the nine reuse
with no legal change at all.

**Before authoring, do these three things:**

1. **Read the Carriage of Goods by Sea Act 2025.** Establish whether it carries Hague-Visby
   unchanged. This is the one open research item, and it blocks Q2.
2. **Obtain MSC-FAL.1/Circ.3/Rev.3** (4 April 2025) for Q5 — six functional elements including
   Govern.
3. **Confirm whether A.1187(33) was still the current Non-exhaustive list** at October 2025.

Then Q3, Q4, Q6 and Q8 reuse as is; Q1 and Q7 need one update each; Q2, Q5 and Q9 need substantive
work. **Expected outcome: 72 → 81 solved.**

## 26.11 Stop conditions still in force

- **Do not** merge to `main`. **Do not** publish QP2403 or QP2508 into `/solvedQP/`.
- **Do not** reopen Security V2 (`eaedfda`), Vercel, Razorpay or customer migration.
- **Do not** commit or delete the source PDFs.
- **Do not** mark QP2510 built. A donor is not a solved target.
- **Write specs with LF line endings.** Both specs touched this session are LF — verified.
- **The intake `temporal_review` field is a review prompt, never evidence.** It is now 0 for 9 on
  this paper, and it failed in **both** directions — Q1 understated an obligation that was already
  live.


---

# §27 — QP2510 OCTOBER 2025: **RESEARCH COMPLETE, ANSWERS NOT AUTHORED.** 2026-08-10

> **All three temporal blockers RESOLVED against primary sources, plus a fourth found and closed.**
> **No answer authored. No `answer_status` touched. QP2510 is NOT built and NOT solved.**
> Branch `pastpapers/qp2510-founder-review`, cut from `e7d8bc0`. Corpus unchanged at **252 / 72 / 180**.

## 27.1 What this session did

Ground truth first: baseline toolchain **ALL STAGES PASS** (28 specs, 8 solved papers, 76 warnings),
corpus counted from spec truth at **252 / 72 / 180**. Then the four things the brief front-loaded:

1. **Full source re-read** of `OCTOBER - 2025.pdf` — **zero transcription corrections**.
2. **Direct QP2403 ↔ QP2510 pair audit** — confirms §26.7 exactly.
3. **The "Q1 cyber → Rev.3" adjudication** — resolved, and it is neither a typo nor a defect.
4. **The three temporal blockers** — all resolved from primary text.

Everything is recorded in `verification/QP2510/DEDUP_AND_SOURCE_PLAN.md` and three research records.

## 27.2 Source re-read and pair audit

Every one of the nine `text_verbatim` strings occurs **character-for-character** in the source PDF
(substring containment, not eyeballing). Header, serial `EM – 2510`, all four instructions and every
printed mark match the spec. **No correction was required.**

| Q | Ratio | Class | Delta |
|---|---|---|---|
| Q1 Q2 Q3 Q4 Q6 Q8 Q9 | **1.0000** | EXACT | none |
| Q5 | 0.9947 | NEAR | **only** the printed `(16)` token — demand identical |
| Q7 | 0.9926 | NEAR | wording identical; **6+4+6 → 6+5+5** |

**Seven EXACT, two NEAR, neither NEAR carrying an examiner-demand change.**

## 27.3 The "Q1 cyber → Rev.3" statement — **REPORT CORRECT, METADATA CORRECT**

Tested, not assumed. **QP2403-Q1 (big data) genuinely carries the cyber circular in its own answer**
— 10 hits on `MSC-FAL.1/Circ.3` and 10 on `Rev.2` across **eight surfaces**. The donor's own
`temporal_review.notes[4]` says *"the cyber cross-reference must move to Rev.3"*.

> Q1 cross-references the circular; Q5 **is** the circular question. Both §26.7 rows are right.
> **Q1 still needs the Rev.2 → Rev.3 update on all eight surfaces.**

## 27.4 **Q2 — THE BLOCKER IS CLOSED, AND THE ANSWER IS NO**

Both 2025 Acts read **in full in the official Gazette of India**. India Code refused automated
retrieval a third time (HTTP 302 to an HTML shell); the Gazette is the better source regardless.

**COGSA 2025 does NOT carry the Hague-Visby position unchanged.** Its preamble enacts the rules
*"with modifications"*, and four are material:

1. **"Goods" now INCLUDES live animals and deck cargo** — Schedule Art **I(d)**, verbatim
   *"including live animals … irrespective of whether such property is to be or is carried on or
   under deck"*. **The donor asserts the Hague-Visby exclusion as a P1 claim. True for March 2024,
   FALSE for October 2025.**
2. **Article IV bis is not reproduced.** Schedule runs Articles **I–IX**; **zero** occurrences of
   `bis`. The donor cites *"Article IV bis rules 1–3"* — no referent in Indian law at this sitting.
3. **Three-month judicial extension of the one-year time bar** — Art III(6)(c) proviso. Hague-Visby
   allows extension only by agreement.
4. **Article I and Article IV(5) re-lettered throughout** — carrier I(a)→**I(b)**, contract
   I(b)→**I(c)**, goods I(c)→**I(d)**, ship I(d)→**I(e)**, carriage I(e)→**I(a)**, recklessness
   IV r.5(e)→**IV(5)(c)**.

**Repeals from primary text:** BoLA 2025 **s.6(1)** repeals the 1856 Act; COGSA 2025 **s.12(1)**
repeals the 1925 Act. **s.12(3) preserves s.331 and Part XA of the Merchant Shipping Act 1958** —
correct at this sitting, since the MS Act 2025 did not commence until 15 March 2026. **Do not
modernise that reference.**

**BoLA 2025 confirmed as a re-enactment**: ss.2, 3, 4 carry the same subjects as the 1856 Act's
ss.1, 2, 3. **There, the change really is a citation update.**

**Assent-date discrepancy from §26.4 is RESOLVED**: the Gazette gives BoLA assent as **24 July
2025** (matching the corpus record, not India Code's 17 June field) and COGSA as 8 August 2025.
Commencement **10 September 2025** for both, corroborated independently of the donor.

## 27.5 Q5 — cyber Rev.3, **both editions read**

`MSC-FAL.1/Circ.3/Rev.3`, **4 April 2025**, read in full from the IMO CDN; **Rev.2 re-read** so the
delta is measured. Approved by **MSC 108** (May 2024) and **FAL 49** (March 2025).

| | Rev.2 — March 2024 | Rev.3 — October 2025 |
|---|---|---|
| Functional elements | **five**, annex 3.5 | **six** — **Govern added and placed FIRST** |
| Vulnerable systems | **eight**, annex **2.1.1** | **nine**, annex **2.2.1** — Communication folded into Bridge; **Ship-port interfaces** and **Ship-to-shore integrated systems (MASS)** added |
| IT / OT | annex 2.1.2, descriptive | annex **2.1**, formally **defined** with examples; OT/IT segregation duty at 2.2.2 |
| New terms | — | **Computer Based System (CBS)**, cyber incident |

**Three of the four printed limbs are touched.** The **OT definition example is a marine-engineering
example** (main engine oil temperature forwarded to the control room) — the most useful sentence in
the circular for limb (D), which asks for *"suitable examples"*.

> **HIGHEST CONTAMINATION RISK ON THE PAPER.** The donor emphasises *"There are five functional
> elements at this sitting, not six."* Reused verbatim that is a confident false statement.
> **The trap must be INVERTED, not deleted.** The mnemonic goes **IPDRR → G-IPDRR**.

## 27.6 Q9 — MLC, and a future-date trap already armed

**2022 amendments in force 23 December 2024**, corroborated twice — the corpus instrument log
(verified against the ILO 2026 Compendium) and the ILO's own notice. The 2022 consolidation is held
locally. **All four additions located verbatim:**

| Addition | Provision |
|---|---|
| Social connectivity, incl. internet access | **Standard A3.1 §17** |
| Appropriately-sized PPE | **Standard A4.3 §1(b)** |
| Engineering/design control has precedence over PPE | **Guideline B4.3.1 §3** |
| Deaths reported annually to the ILO for a **global register** | **Standard A4.3 §5(a)** |
| Registered owner on the financial security certificate | **Appendix A4-I(g)** |

> **QUARANTINE — the 2025 MLC amendments are ADOPTED BUT NOT IN FORCE** (ILC 113th Session, June
> 2025; expected December 2027). They were adopted **four months before this sitting**, so anything
> written from current ILO pages will present them as law. The corpus already segregates them under
> `not-yet-in-force/`. **They must not appear in an October 2025 answer.**

## 27.7 **Q7 — a FOURTH item found, and the trap runs backwards**

The brief's third pre-authoring item was to confirm A.1187(33)'s currency. It moved — but too late
to matter, and in the dangerous direction.

**Resolution A.1208(34), adopted 3 December 2025**, is the *2025 Non-exhaustive list of obligations
under instruments relevant to the III Code*, and states **"REVOKES resolution A.1187(33)"** — read
on the IMO CDN. **That is AFTER the October 2025 sitting.**

> **A.1187(33) WAS still current at this sitting. RETAIN the donor's citation. Citing A.1208(34)
> would be future-date contamination.** The A.1208(34) List gathers requirements entering into force
> by 1 July 2026 — none of which existed for this candidate.

This is the **§26.3 Q1 mirror-image error in a new place**: the risk is not staleness but an author
in 2026 finding the successor presented as current. **Same 34th Assembly session as A.1206(34) and
A.1207(34)** from the June 2026 paper — that session revised this whole family.

## 27.8 Adaptation map — evidence-based, not expectation-based

**Four A · two B · three C.**

| Q | Class | Work |
|---|---|---|
| Q3 Q4 Q6 Q8 | **A — reuse as is** | re-verify at the sitting, re-key, re-anchor, sweep |
| Q1 | **B** | Rev.2 → Rev.3 cross-reference on **eight surfaces**; substance stands |
| Q7 | **B** | retain A.1187(33); re-weight limbs (b)/(c) for 6+5+5 |
| Q2 | **C** | re-cite to the 2025 Acts; **invert the deck-cargo/live-animals proposition**; drop Art IV bis; add the three-month extension; re-letter all Article I citations |
| Q5 | **C** | six elements with Govern; nine systems; annex renumbering; formal IT/OT definitions |
| Q9 | **C** | integrate four additions **into** limb (a)'s sections; reverse the "not yet in force" prose; quarantine the 2025 set |

## 27.9 Why this session stopped here

The three temporal questions had to be researched **before** any of the nine could be written: Q2's
result changes what limb (c) may assert, Q5's changes three of four limbs, Q9's changes half of limb
(a). That research is done and primary-sourced. Authoring nine ~45 KB objects, nine verification
records, the build, sweeps and regression on top of it was not achievable in the remainder of the
session at the standard §59 sets — and §59 forbids lowering it because eight of nine look easy.

**This is the §25 precedent.** QP2403 was deliberately stopped at 2 of 9 rather than lower
verification quality; §26 records that the checkpoint held and its groundwork was *used, not redone*.

> **The expensive, hard-to-redo work is the part that is finished.** Three resolved legal positions,
> a verified source re-read, a confirmed pair audit, a per-question adaptation class, and four
> primary instruments pulled and read.

## 27.10 NEXT SESSION — **finish QP2510. Do not start another paper.**

All four pre-authoring research items from §26.10 are **CLOSED**. Nothing blocks authoring.

**Author Q2, Q5, Q9 first** (the three C-class), then Q7 and Q1, then Q3, Q6, Q4, Q8. Then build,
recompute the reuse map, run the sweeps, UI review at 1280/375, add a `FIXTURES` entry for QP2510,
double-build for determinism, and regression the eight solved papers.

**Expected outcome: 72 → 81 solved, 252 / 81 / 171.**

Mandatory for every question including class A — re-key ids/`verification_file`/in-paper
`cross_links`; re-anchor sitting-relative prose; sweep the **assembled** spec, not the patch list;
adjudicate every hit by hand (April: 55 hits, one defect).

## 27.11 Stop conditions still in force

- **Do not** merge to `main`. **Do not** publish into `/solvedQP/`. **Do not** reopen Security V2.
- **Do not** commit or delete the source PDFs. The four instruments pulled this session were written
  to the session scratchpad, **outside the repository**, and are not committed.
- **Do not** mark QP2510 built. A donor is not a solved target, and it is still not solved.
- **Write specs with LF line endings.** All four files added this session are LF — verified.
- **The intake `temporal_review` field is a review prompt, never evidence.**
- **The broken `validate_antipatterns.py` PostToolUse hook did not fire this session.** No `hooks`
  key exists in any settings file; only historical transcripts mention it. Environment noise, gone.

---

# 28. QP2510 OCTOBER 2025 — **SOLVED 9/9 AND BUILT**

**Branch:** `pastpapers/qp2510-founder-review`, continued from the §27 research checkpoint `b97d207`
**Date:** 2026-08-10
**Verdict:** **READY FOR FOUNDER REVIEW.** Not merged, not launched.

## 28.1 The checkpoint held, and was used rather than redone

§27 stopped after the research and before the answers. **That research was inherited whole.** No
source was re-pulled, no Gazette re-read, no circular re-obtained. The three resolved legal positions,
the source re-read, the pair audit and the per-question adaptation class were all used as given.

This session authored **all nine answers**, in the §27 order: Q2, Q5, Q9, then Q7 and Q1, then Q3,
Q6, Q4, Q8.

## 28.2 Adaptation result — the plan survived contact

| Class | Questions | Outcome |
|---|---|---|
| **C — substantive** | Q2, Q5, Q9 | as planned |
| **B — minor** | Q1, Q7 | as planned |
| **A — reuse after re-verification** | Q3, Q4, Q6, Q8 | as planned |

**Four A, two B, three C — exactly the shape §27.8 predicted on evidence.**

## 28.3 The three substantive transitions

**Q2 — the Indian statute book changed five weeks before the sitting.** Bills of Lading Act 2025
(18 of 2025) and Carriage of Goods by Sea Act 2025 (19 of 2025), both in force **10 September 2025**.
The load-bearing edit was **not** the citations: Schedule **Article I(d)** now *includes* live animals
and deck cargo, **reversing** a donor P1 primary claim. Article IV *bis* was removed as an Indian
citation (the Schedule runs I–IX with no "bis"); the three-month judicial extension at III(6)(c) was
added; Article I and IV(5) were re-lettered clause by clause. New enacting-section content — s.3,
s.4, s.5, s.12(3) — was added, which the donor never had.

> A find-and-replace on article letters alone would have shipped a **correctly cited falsehood**.
> This remains the most dangerous single edit in the corpus to date.

**Q5 — cyber Rev.3.** MSC-FAL.1/Circ.3/**Rev.3 of 4 April 2025**. Five functional elements became
**six**, with **GOVERN** added and placed first; eight vulnerable systems became **nine** at annex
**2.2.1** as a *restructure, not an append*; IT and OT became **formal definitions** with the
circular's own examples; **CBS** was introduced; segregation became a stated duty at 2.2.2. The
donor's emphasised trap — *"five, not six"* — was **inverted, not deleted**. IPDRR → **G-IPDRR**.
One reversal in the target's favour: **IACS UR E26/E27 ARE in application here** (ships contracted
on or after 1 July 2024), where the donor correctly recorded them as not yet applying.

**Q9 — the MLC 2022 amendments are simply the law.** In force **23 December 2024**, ten months
before the sitting. Five requirements **integrated into the limb-(a) sections they amend**, not
appended: A3.1 §17 social connectivity; A4.3 §1(b) appropriately-sized PPE; B4.3.1 §3 with A4.3 §2
the hierarchy of controls; A4.3 §5(a) deaths reported annually for a **global register**; Appendix
A4-I(g) registered owner. Every donor statement describing them as *not yet in force* was reversed —
the largest re-anchoring job on the paper. Limb (b) gained exactly one proposition.

**The 2025 MLC amendments are quarantined.** Adopted June 2025 — *four months before the sitting* —
not in force, expected 2027. They appear nowhere in the Model Answer. **No ratification count is
asserted anywhere**, because the available figures are as at 2026.

## 28.4 Q7 — the trap that runs backwards

Wording character-identical; marks moved **6+4+6 → 6+5+5**. Handled as **emphasis**: limb (b)'s
guidance was rewritten on every surface that stated the split, and **no proposition was deleted from
limb (c)**.

**A.1187(33) was RETAINED on 18 candidate-facing references.** A.1208(34) revokes it but was adopted
**3 December 2025 — roughly seven weeks AFTER the examination** — and gathers obligations entering
into force by 1 July 2026. It is named only as the thing not to substitute, with a `B_CURRENCY_CHECK`
guard so a later editor does not "modernise" the citation.

## 28.5 Q1 — the cross-reference that was real

The apparent oddity of a Big Data question needing a cyber update was **tested, not assumed**. Q1
genuinely carries the circular across **eight surfaces**; all eight moved Rev.2 → Rev.3. Nine
candidate-facing Rev.3 references stand and **zero Rev.2 references remain**. Big Data content was
deliberately **not** modernised — the Maritime Single Window obligation is in force at both sittings.

Independent confirmation from the built page: searching `msc-fal.1/circ.3` resolves to **Q1 and Q5**.

## 28.6 A defect the toolchain could not see

The HTTP visual review caught one real defect. An ordered-replacement rule — a specific pattern
followed by a broad fallback — met an instance with `</b>` between the label and the date. The
specific rule missed it, the fallback fired, and the result was **"Rev.3 (7 June 2022)"**: a Rev.3
label carrying Rev.2's issue date. Both fragments are individually well-formed, so every validator
passed it.

> **A broad fallback after a specific rule does not merely under-match — it can synthesise a claim
> present in neither the source nor the target.** Fixed, and a guard added asserting that no edition
> label sits with another edition's date. This is the fourth defect class that only HTTP review has
> caught.

## 28.7 Sweeps

Run on the **assembled** spec and split by surface, because the rule is not "these words must not
appear":

- **Model-answer surfaces** — superseded and not-yet-in-force material must be **zero as an
  assertion**. 15 hits found; **all 15 adjudicated as explicit exclusions** (Rev.2 named as the wrong
  edition, the 2025 MLC set named as not in force). None asserts superseded or future law.
- **Study Guide** — change context is **required**, and is present and labelled for Q2, Q5, Q7, Q9.
- **Donor contamination** — `March 2024` and `QP2403` pointers: **zero** on candidate-facing surfaces.
- **Future contamination** — A.1208(34), the 2025 MLC amendments and 2027 appear **only** as
  labelled exclusions.

## 28.8 Build, determinism and regression

| Check | Result |
|---|---|
| Toolchain | **ALL STAGES PASS**, 92 warnings (76 baseline + 16 new QP2510 length warnings) |
| Determinism | **21 generated artefacts compared, 0 byte differences** across a full double build |
| Corpus | **252 / 81 / 171** — 9 solved papers, 19 intake, as predicted |
| questions-2025 | exactly **nine** QP2510 deep links, 0 broken; all other 2025 sittings still intake |
| Regression | **QP2403, QP2508 and all six 2026 papers byte-unchanged.** No other spec touched |
| UI | 9 cards, 5 modes, Answer default, **0px horizontal overflow at 1280 and 375**, no console errors |
| Provenance | every host recurrence code clean; the new leak probe **positive-controlled** |
| Security | untouched |

A `FIXTURES` entry was added for QP2510 — nine content probes **re-tested against this page rather
than inherited**, plus three *temporal fingerprint* probes (`carriage of goods by sea act 2025`,
`six functional elements`, `social connectivity`) that a regression to donor content would remove.

## 28.9 **The donor finding — and it is not the comfortable one**

**QP2510 created ZERO new donors.**

Tier D fell from 21 to 12 for 2025, which is exactly QP2510's own nine rows leaving the unsolved
list. Computed directly: **four** unsolved questions share a family with a QP2510 question —
QP2504-Q9, QP2401-Q9, QP2410-Q7, QP2412-Q9 — and **all four already had QP2403 in the same family**.

**Nor does QP2510 become the preferred donor for any of them.** Three targets (January 2024, October
2024, December 2024) are *earlier* than both donors, and QP2403 is temporally closer; pulling QP2510
backwards would mean reversing currency corrections rather than inheriting them.

> **The one genuinely interesting case is QP2504-Q9, April 2025**, which falls *between* the two
> donors and sits almost exactly on the Rev.3 boundary — the circular is dated **4 April 2025**.
> Whether Rev.2 or Rev.3 governs that sitting depends on the examination date itself. **This is now
> the most temporally delicate unsolved question in the corpus**, and it must not be answered from
> either donor without establishing that date first.

Family reach also *fell* for three papers (QP2401 4→3, QP2412 3→2, QP2504 6→5), because QP2510's
questions are no longer unsolved members of those families.

**Why this happened, and it was structurally inevitable:** QP2510 is a question-for-question reprint
of a paper that was *already solved*. Every family it touches was already covered by QP2403.

## 28.10 What that means for the production rhythm

§27 proposed: research-heavy family creator → donor-heavy temporal adaptation → repeat. **The
evidence does not support that as a standing rule**, and it should not be adopted as one.

- QP2403, the creator, produced donors for **QP2510 (9) and four other questions**.
- QP2510, the adapter, produced donors for **none**.

A pure temporal adaptation of an already-solved paper delivers **real product value and zero donor
reach**. It is worth doing — the October 2025 candidate needs the October 2025 law — but it must be
budgeted as *product*, not as *capacity building*, and it should not be scheduled on the expectation
that it will make the next paper cheaper.

**The better shape is the hybrid**, which is what the next paper is: part donor adaptation, part
family creation, so each paper both consumes and produces reach.

## 28.11 Study intelligence — stable route, changing law

The QP2403 → QP2510 pair is the cleanest demonstration in the corpus of a principle worth teaching:

> **MEMORISE A STABLE ROUTE. UPDATE THE TIME-SENSITIVE CONTENT.**

**Q5 is the exemplar.** Seven route steps, identical at both sittings; steps 1, 3, 5 and 7 reuse
verbatim, and only the *content of steps 2, 4 and 6* changes. A candidate who learned the route in
2024 still knows where to start, in what order to write and where to stop. They update two facts.

**Q2 is the counter-example.** Same question, same route, but the governing statute was replaced and
one proposition **inverted**. Route stability does **not** imply answer stability.

**Q9 sits between them** — the architecture of limb (a) survives; five requirements thread into it.

**Q7 is the fourth case**: same truth, different emphasis, driven only by a mark split.

This is the raw material for *"How this topic has been asked"* and the question-family study guides.
**Not built now** — recorded for the derivation session.

## 28.12 NEXT SESSION — **QP2506, JUNE 2025**

Ranked across all 19 remaining unsolved papers on the recomputed map:

| | |
|---|---|
| **Tier D readiness** | **4 / 9** — the highest in the set. Q2 ← QP2602-Q7, Q7 ← QP2601-Q8, Q8 ← QP2601-Q9, Q9 ← QP2602-Q5 |
| **Family reach** | **5** other unsolved questions in the same families — real donor creation |
| **Temporal burden** | **1** flag, the lowest of any paper with donors. Q9 *Unseaworthy Vessels under the Merchant Shipping Act* is HIGH — June 2025 is on the **MS Act 1958**, and the donor QP2602-Q5 (February 2026) is also pre-15-March-2026, so the donor is on the same Act |
| **Fresh research** | **5** — rudder efficiency devices, marine insurance short notes, SCOPIC and post-collision jurisdiction, LLMC, and general average. Q3 and Q6 sit adjacent to the general-average work already built at QP2403-Q3 and QP2510-Q3, which is supporting material rather than a donor |

**Why not the alternatives.** QP2511 (3/9, reach 5) and QP2509 (3/9, reach 4) each carry two
temporal flags. QP2507 has the highest reach in the corpus at **8** but **0/9** Tier D and two flags,
so it is a pure creator and the most expensive single paper available. QP2502 has reach 7 but only
2/9.

**QP2506 is the hybrid the rhythm finding at §28.10 argues for**: four donors to consume, five
families to create, and the lightest temporal burden available to a paper with donors.

## 28.13 Stop conditions still in force

- **Do not** merge to `main`. **Do not** publish into `/solvedQP/`. **Do not** reopen Security V2.
- **Do not** commit or delete the source PDFs.
- **QP2504-Q9 must not be answered from either cyber donor** until the April 2025 examination date
  is established against the 4 April 2025 issue date of Rev.3. See §28.9.
- **Write specs with LF line endings.** Verified byte-identical on a JSON round-trip before the first
  write this session.
- **The intake `temporal_review` field is a review prompt, never evidence.** It was 0 for 9 on the
  donor and was not trusted here; all nine classifications are evidence-based.
- **A broad find-and-replace fallback is not safe on citation text.** See §28.6.

---

# §29 — QP2506 JUNE 2025, COMPLETE

**Branch `pastpapers/qp2506-founder-review`**, cut from `8fa4f5f`, which is `30de4b3` plus the
state reconciliation described in the header. Commits `f610818` (verify and author) and `fb22611`
(build and refresh intelligence).

## 29.1 State

| | |
|---|---|
| Corpus | **252 / 90 / 162** — 10 solved papers, 18 intake |
| Toolchain | **ALL STAGES PASS**, 102 warnings (76 baseline + the new QP2506 length warnings) |
| Determinism | 18 generated artefacts, **0 byte differences** on a full double build |
| Regression | QP2403, QP2508, QP2510 and all six 2026 papers **byte-unchanged**; no other spec touched |
| UI | 5 modes, 6 numbered route headings identical across map / plan / answer / recall, **0px overflow at 1280 and 375**, no console errors, noindex and ungated, no host branding |

## 29.2 Donor map as built

Tier was recomputed from repository truth rather than taken from the intake metadata, which was
frozen before QP2508 was solved.

| Q | Tier | Donor used | Wording | Temporal work |
|---|---|---|---|---|
| Q1 Rudder efficiency devices | **C** | none — no donor and no adjacent built material anywhere | — | none |
| Q2 Entry into force | **D** | QP2508-Q7 (Aug 2025) | EXACT task | nil; April 2025 worked example kept and re-checked |
| Q3 Marine insurance short notes | **B** | QP2607-Q5, QP2606-Q3, QP2601-Q4 | — | **A.949(23) → A.1184(33)** |
| Q4 SCOPIC and collision | **B** | QP2601-Q3, QP2602-Q1 | — | none; SCOPIC 2020 primary-verified |
| Q5 LLMC | **B** | QP2508-Q1, QP2602-Q1 | — | none; stability argument inherited |
| Q6 General average refloating | **D** | QP2508-Q6 (Aug 2025) | **EXACT, raw-identical** | nil |
| Q7 Casualty investigation | **D** | QP2601-Q8 (Jan 2026) | EXACT | nil; only question with no 2025 donor |
| Q8 Human element and fatigue | **D** | QP2508-Q4 (Aug 2025) | NEAR | nil |
| Q9 Unseaworthy ships | **D** | QP2508-Q5 (Aug 2025) | EXACT task, June prints no marks | **12 surfaces rewritten** |

## 29.3 **The reuse map understates Tier D, and it is a real defect**

`tools/pastpapers/build_reuse_map.py` prints the definition *"Tier D — family contains a question
whose answer is built and verified"* but its implementation reads the **stored `reuse_tier` field**
off the spec rather than computing it. That field was written during the 2025 intake, before
QP2403, QP2508 and QP2510 were solved, and was never recomputed.

Six unsolved questions are misclassified as Tier C when their family already contains a built
answer. True Tier D across the unsolved corpus is **25, not 19**:

| Question | Stored | True | Donor |
|---|---|---|---|
| QP2401-Q9 | C | **D** | QP2403-Q7, QP2510-Q7 |
| QP2404-Q6 | C | **D** | QP2508-Q6 |
| QP2410-Q9 | C | **D** | QP2508-Q6 |
| QP2412-Q9 | C | **D** | QP2403-Q7, QP2510-Q7 |
| QP2504-Q9 | C | **D** | QP2403-Q5, QP2510-Q5 |
| QP2506-Q6 | C | **D** | QP2508-Q6 — corrected in this paper's spec |

**The generator was deliberately not changed on a paper branch.** Fixing it would alter the recorded
Tier D counts for five other papers in a corpus-wide planning artefact, which is a governance
change rather than a production one. Only QP2506's own stored field was corrected. **The ranking at
§29.6 is computed from repository truth, not from the map.**

## 29.4 Temporal review — the finding runs backwards

> **The IMO Guidelines on places of refuge are resolution A.1184(33), adopted 6 December 2023.
> Operative paragraph 4: "REVOKES resolution A.949(23)."**

The revocation is **eighteen months before this sitting**, so the 2003 resolution that practically
every circulating note set still quotes is not merely dated for June 2025 — it is wrong for it. It
is freely available on an official domain, and an answer built on it would be internally coherent,
confidently written and wrong. **The intake temporal review had this question as STABLE / LOW with
no risk classes.** The sweep found it; the flag list did not.

The Q9 hazard was also not the one predicted. Both donors are pre-15-March-2026 and already sit on
the 1958 Act, so there was **no statute regression to undo**. The realised hazard came from the
donor's *currency paragraph*: QP2508-Q5 turns on the 2025 Act having received assent on 18 August
2025, in the month of its own sitting — which is after this paper. At June 2025 the Merchant
Shipping Bill, 2024 had been introduced on **10 December 2024** and passed by **neither House**. The
teaching point becomes **"a Bill is not an Act"**, one rung earlier on the same ladder, and it was
rewritten across **twelve** surfaces. The intake flag predicted eight.

Everything else was checked in both directions and recorded as checked, including the explicit
finding that the MLC 2022 amendments in force 23 December 2024 neither add to nor subtract from Q8.

## 29.5 What the sweeps caught that the patches did not

The assembled-answer sweep found **four defects** the targeted patches had missed, all of one class:
cross-references left pointing at the **donor paper**. Q2 carried three `see Q8` references to the
August paper's GHG question — on this paper Q8 is human element — and a currency paragraph still
naming *"the February 2026 donor"* after the donor had been changed to August 2025.

This is the argument for the sweep being mandatory rather than a formality: the targeted patch
fixes what you looked for, and the sweep finds what you did not.

Every replacement in this session was written as an **asserted exact substitution required to fire
exactly once**, never as a pattern with a fallback — §28.6.

## 29.6 NEXT SESSION — **QP2509, SEPTEMBER 2025**

Ranked across all 18 remaining unsolved papers, on Tier D **computed from repository truth**:

| | |
|---|---|
| **Tier D** | **3 / 9** — Q2 ← QP2508-Q2/QP2602-Q2, Q3 ← QP2601-Q3/QP2604-Q3/QP2607-Q5, Q9 ← QP2606-Q8. Tied top with QP2511 |
| **Nearest donor** | **QP2508, one month earlier** — the tightest donor interval anywhere in the corpus |
| **Family reach** | 4 |
| **Temporal burden** | 2 flags, and both are *clean adjudications* rather than boundary problems: Q5 HNS Convention **not yet in force** (a statement of fact) and Q2 CII in flux (bounded) |
| **Hidden Tier B** | at least two more questions the tier field cannot see. **Q8** IMO and ILO human element regimes and fatigue — the largest family in the corpus is fully researched at QP2506-Q8. **Q7** Bunker Convention 2001 against CLC 92 — both verified at QP2607-Q2. Effectively **5 of 9 already covered** |

**Why not QP2511 November 2025**, which ties on Tier D and reach: its flags are harder. Q8 is the
**Hong Kong Convention newly in force**, which needs the entry-into-force position established
against the Indian Recycling of Ships Act, and Q7 is FAL amendments. Its six Tier C questions are
also genuinely new technical ground — LNG bunkering, torque-rich operation, SOLAS chapter XII, a
propeller blade crack. That is valuable corpus breadth, and the engineering thinness this paper
exposed at Q1 argues for it eventually, but it is the more expensive paper of the two.

**Do not start it.** QP2506 is Founder-review only.

## 29.7 Carried forward

- **Q1 carries a validator warning that no claim is primary-verified, and that is correct.** No
  primary instrument governs rudder hydrodynamics. It was not engineered away, and every efficiency
  figure is an industry-quoted range with its dependency stated. **This is the corpus's first
  naval-architecture question** and the solved set remains heavily weighted to law and management.
- **17 claims are flagged for re-verification before publication, 0 blocking.** The two that matter
  most are the A.1184(33) currency check and the Part XA / MS Act 1958 boundary shared with Q9.
- **QP2506-Q8 is substantively identical to QP2508-Q4, QP2601-Q9, QP2602-Q4 and QP2604-Q9.** A
  correction to any one of the five must be applied to all five.

---

# 30. DONOR-READINESS FIX AND QP2509 PRE-AUTHORING — 2026-08-11

Branch `pastpapers/qp2509-founder-review`, cut from **`0d7f872`**.
Corpus unchanged: **252 / 90 / 162**. Toolchain ALL STAGES PASS with `--self-test`.

**QP2509 is at 0 / 9 authored and `specs/QP2509.json` is untouched intake.** This session did
the machine preflight, closed the §29.3 defect, clarified the source-authority protocol, and
completed QP2509's source verification, donor map and temporal sweep. It stopped **before**
authoring rather than leave the half-authored state `PASTPAPER_PRODUCTION_PROTOCOL.md` §3
forbids.

Full pre-authoring record: **`QP2509_TEMPORAL_AND_DONOR_ANCHOR.md`**.

## 30.1 The §29.3 defect is CLOSED — and the "six" reconciles to five

`build_reuse_map.py` classified tier D by reading the stored `reuse_tier` field, which is
frozen at intake and cannot move when some *other* paper is solved. Donor readiness is now
derived on every run from the current built set (`recurrence_model.donor_readiness`).

**Stored 15 → derived 20** over the unsolved corpus (2024: 7→11, 2025: 8→9; tier C 147→142,
per-year totals conserved). Five questions moved:

`QP2401-Q9`, `QP2404-Q6`, `QP2410-Q9`, `QP2412-Q9`, `QP2504-Q9`.

**§29.3 recorded six, and both counts are right.** Its sixth row was `QP2506-Q6` — a question
inside the paper being solved in that session. When QP2506 completed, its nine questions left
the unsolved set carrying 4 stored-D and 5 derived-D with them: 19−4 = 15, 25−5 = 20. A tier-D
count is only meaningful relative to the solved state at which it was computed, which is
precisely why it is now derived rather than stored.

Stored `reuse_tier` is **retained** as the authoring record — `validate_spec.py`,
`build_paper.py`, `build_index.py` and `audit_paper.py` all still depend on it. Intake metadata
and current production readiness are now two named things.

Recurrence family, donor set and **preferred donor** are also separated. Preferred selection is
deterministic: EXACT printed stem first, then nearest sitting, then question id.

Regression coverage: `build_reuse_map.py --self-test`, wired into `run_toolchain.py
--self-test`. Cases 1–2 mutate the built set and assert the tier follows; reintroducing the
defect fails both and exits 1 (verified by mutation). Cases 4–5 pin preferred-donor selection
on `QP2509-Q3` and `QP2509-Q2`. §5.1 of the generated map now prints stored against derived.

No spec and no generated page changed.

## 30.2 Solving order changed — five papers re-ranked

`QP2401` 2→3, `QP2404` 1→2, `QP2410` 1→2, `QP2412` 1→2, `QP2504` 0→1.
`QP2509` and `QP2511` are unchanged at **3 / 9** and remain joint top of the order.

## 30.3 QP2509 — source PASS, donors 3/9, and the QP2506 expectation was wrong

Source verification: 9/9 stems verbatim, serial `EM – 2509`, 2 pages, instructions and marks
match, `printed_marks_absent` correct on Q1/Q6/Q8. **No source correction needed.** Q9 prints
`SOLAS ch.ll-1` and Q8 prints a capital `B).`; both are reproduced, not fixed.

Tier D 3/9 — **Q2** (`QP2508-Q2`, EXACT, one month), **Q3** (`QP2607-Q5`, EXACT),
**Q9** (`QP2606-Q8`, EXACT).

**§29.6 expected Q7 and Q8 to have useful existing coverage. They do not.** Both are family
singletons with no donor at any tier. Q8 has real *topical* leverage in the fatigue material
already verified for `QP2602-Q4` and its four relatives, but that is research to be re-read,
not a donor. Promotion of Q7 or Q8 to tier B remains open to the authoring session.

## 30.4 Temporal findings — three that change the answer

- **Q5 HNS is the highest risk in the paper and it runs forward.** Not in force at the sitting,
  and its Article 21 conditions were not met until **29 May 2026**, with force on **29 November
  2027**. Every present-day HNS fact is unusable. The stem's "expected shortly to come into
  force" is the sitting's state and must be preserved. **Quote no Contracting-State count** —
  the September-2025 figure could not be established.
- **Q2 CII sits one month before the decision.** MEPC 83 (April 2025) **approved** amendments
  to regs 20/25/28 for adoption at the extraordinary session in **October 2025** — after the
  sitting. Approved, not adopted, not in force. The `QP2602-Q2` donor is on the far side.
- **Q8 MLC is a three-state trap in both directions.** The 2022 amendments were in force
  (23 December 2024). The **2025 amendments were ADOPTED on 6 June 2025** — three months before
  the sitting — but not in force (expected late 2027). Omitting them is as wrong as applying
  them.

Also verified: IMSBC **07-23** mandatory from 1 January 2025 is the operative edition for Q1;
the **MS Act 1958** governs (2025 Act commenced 15 March 2026, so the Q3 and Q9 donors must be
statute-reversed); maritime cyber Rev.3 is **not load-bearing**; and the Indian carriage-law
commencement of **10 September 2025 is not load-bearing** — no question raises a bill of lading
or contract of carriage, so the unprinted sitting day does not need resolving for this paper.

## 30.5 Next session

**Author QP2509 from `QP2509_TEMPORAL_AND_DONOR_ANCHOR.md` §4.** The temporal work is done and
verified; seven items are carried as TO VERIFY at §5 of that file. Do not re-derive the donor
map — regenerate it only if another paper is solved first.

**NO MAIN MERGE. NO SOLVED-QP LAUNCH. QP2509 is Founder-review only.**

# §30.6 — QP2509 authoring checkpoint, 2026-08-11 (SUPERSEDED by §31)

**Delta only. The full record is `QP2509_AUTHORING_CHECKPOINT.md`; this section is the pointer
and must not be expanded into a narrative.**

| | |
|---|---|
| Corpus | **252 / 90 / 162**, 10 solved papers — **unchanged** |
| QP2509 | **3 of 9 authored — Q2, Q5, Q7 READY.** `specs/QP2509.json` is **untouched intake** |
| Where the work is | staged at `staging/QP2509/authored_questions.json`; records at `verification/QP2509/` |
| Toolchain | `ALL STAGES PASS`, 102 warnings, `REUSE SELFTEST` PASS — identical to baseline |
| Built page | **none, correctly** |

**Why the spec is untouched.** `build_paper.py` selects a paper by the **presence of answers**,
not by `build_state`, so a 3/9 spec enters the build pipeline and turns the branch red. That was
observed, not assumed. The protocol's "no valid half-authored-paper state" is therefore
mechanically enforced, and the resolution was to park the verified objects outside the spec
rather than discard them or leave a failing build.

**Resume with one command:** `python meoclass1/pastpapers/staging/QP2509/apply_staged.py`, then
author **Q8 → Q3 → Q9 → Q4 → Q1 → Q6**. Do not commit an applied spec until 9/9.

**Three findings not to re-derive:** the `QP2508-Q2` donor carried **"See Q8"** on four surfaces
pointing at its own paper's Net-Zero question — a dateless defect a temporal sweep cannot see,
and the Q3 and Q9 donors should be expected to carry the same class; the HNS Convention contains
**no bunkers exclusion** (the word does not appear in it — bunkers are outside because article
1.5(a) reaches only cargo); and the Bunkers Convention sets **no limitation figure of its own**,
article 6 referring out to the LLMC. Anchor §5 items 2 and 5 are **discharged**; item 7 is
answered for Q7 (**no tier B promotion**) and still open for Q8.

**NO MAIN MERGE. NO SOLVED-QP LAUNCH. NO BUILD. QP2509 remains unfinished.**

> **§30 is SUPERSEDED by §31.** The resume command above has been executed, the staging
> directory has been retired, and QP2509 is complete. The temporal adjudications in §30.4 remain
> valid and were the input to §31.

---

# §31 — QP2509 SEPTEMBER 2025, COMPLETE

Authored 2026-08-11, resuming from checkpoint `25e049f`. Detail lives in the nine records at
`verification/QP2509/`; this section carries state and the two findings that change how the
next paper is chosen.

## 31.1 State

| | |
|---|---|
| Corpus | **252 / 99 / 153**, **11** solved papers (was 252 / 90 / 162, 10) |
| Toolchain | `ALL STAGES PASS`, 110 warnings; `REUSE SELFTEST` PASS |
| Determinism | rebuild produced **23 generated artefacts, 0 byte differences** |
| UI | 61 assertions PASS on QP2509; desktop 1280 and mobile 375 clean, no console errors, no horizontal overflow, Answer is the default mode, host recurrence not searchable |
| Staged work | Q2, Q5 and Q7 restored **mechanically** by the committed applier; staging then retired |

The nine word-count warnings are the corpus-normal band excursion and were not trimmed.

## 31.2 THE HEADLINE — a donor cited a resolution that did not exist at the sitting

`QP2606-Q8` (June 2026) cites **`A.1207(34)`**, *Survey Guidelines under the HSSC 2025*, adopted
**3 December 2025**. **QP2509 was sat in September 2025.** The operative edition is
**`A.1186(33)`**, adopted 6 December 2023, revoking `A.1156(32)`.

Three things make this the most instructive defect the series has produced:

1. **It occupied FOURTEEN surfaces** — sources ×6, model answer, route, `regulations`,
   `search_aliases`, `quick_revision` ×2, four study-guide sections, a retrieval card,
   `reverify_before_publication` and `verification_status`.
2. **The donor's own trap warning was inverted.** Its *Common mistakes* list said *"Citing
   A.1186(33) as the current Survey Guidelines. It was revoked by A.1207(34)."* For this sitting
   that instruction is exactly backwards.
3. **The routine sweep could not see it.** The contamination sweep probes future *year* tokens.
   This defect is dated **3 December 2025** — the same calendar year as the sitting.
   **A future-contamination sweep must be date-aware relative to the sitting MONTH.**

The survey *content* is identical in both editions, so the answer would have read as entirely
correct. This is the §8 "wrong edition" case in its purest form. It joins `A.1208(34)` (§27) and
`A.1184(33)` (§29) — **the 34th Assembly of December 2025 is now a standing boundary** for every
2025 sitting.

## 31.3 SECOND FINDING — host recurrence edges are DIRECTIONAL

`QP2509-Q6` was scored **Tier C, "no family member with a built answer"**. `QP2601-Q2` is a
built, verified answer to the **same printed question**, differing in two words.

`QP2601-Q2`'s hint list names `2025/SEP/Q6`. `QP2509-Q6`'s cannot name `2026/JAN/Q2` — its source
paper was printed before that sitting existed. **If edges are built from each paper's own hint
list without symmetrising, an earlier paper can never see a later paper that names it** — and
that is the direction a backwards-working programme needs.

**Recommended fix, deliberately NOT made this session:** treat host recurrence hints as an
**undirected** relation in `recurrence_model.py` / `build_reuse_map.py`. It would alter the map
for the whole corpus and must not be done mid-paper.

Together with the Q8 finding — the model is blind to a **limb-level** exact donor, where
`QP2509-Q8` limb B) matches `QP2508-Q4` limb B word for word — the derivation has **two known
blind spots**, both understating readiness.

## 31.4 Three anticipated traps that did not exist

The anchor flagged **Q3, Q4 and Q9** for reversal of the Merchant Shipping Act 2025 to the 1958
Act. **None of the three engages that Act.** Q3 runs on the **Marine Insurance Act 1963 s.66**,
Q9 is wholly international, and Q4 runs on the **Admiralty (Jurisdiction and Settlement of
Maritime Claims) Act, 2017**. The prediction was reasonable from the donors' sitting dates and
wrong in every case — but it caused all three donors to be swept carefully, which is how §31.2
was found. Recorded as *checked, no temporal issue*, per protocol §2.

Two questions declined a claim rather than guess: **Q4** states nothing about India's party
status to the 1993 Convention (the UN document retrieved is the treaty text, not the
participation list), and **Q1** quotes no TML value.

## 31.5 NEXT SESSION — **QP2404, APRIL 2024**

| Paper | Tier D | Family reach | Temporal flags |
|---|---|---|---|
| **QP2404** | **3 / 9** | **5** | **1** |
| QP2511 | 3 / 9 | 4 | 2 |
| QP2401 | 3 / 9 | 3 | 2 |
| QP2507 | 0 / 9 | 8 | 2 |

Chosen because it ties for the highest derived Tier D while carrying the **fewest temporal
flags** of that group, and because **QP2509 itself created one of its donors** — `QP2404-Q3`
(maritime lien) ← `QP2509-Q4`. Its one flag, `QP2404-Q2` **GUIDELINE EDITION**, should be taken
seriously in light of §31.2.

QP2509 created three C→D promotions — `QP2404-Q3` and `QP2512-Q9` from Q4, `QP2503-Q6` from Q5
(flagged **HIGH**, HNS) — and gave `QP2412-Q4` a second donor that **predates the 34th Assembly**,
which is the safer one for any pre-December-2025 sitting.

**NO MAIN MERGE. NO SOLVED-QP LAUNCH. QP2509 IS FOUNDER-REVIEW ONLY.**

## 31.6 Recommendation — split this file

`CURRENT_STATUS.md` is now **~196 KB / 3,300+ lines**. The CURRENT STATE table and the newest
section are what any session actually needs; §26–§30 are narrative. **Recommend splitting
`SESSION_HISTORY.md` out of it**, leaving state plus the newest delta here. Not done this
session — it would be a large diff landing on top of a paper awaiting review.

---

# 32. PRE-QP2404 INFRASTRUCTURE HARDENING — 2026-08-11

**Branch:** `workflow/pre-qp2404-hardening`, from `75cccb8` on `workflow/state-history-hygiene`
(verified to descend from `850bdde` PIL V1 and `a5f2551` QP2509).
**Verdict:** READY FOR FOUNDER REVIEW. Not merged, not launched. **No QP2404 work started.**
**No semantic answer content touched.** Zero generated-artefact drift.

## 32.1 §31.3 was right about the symptom and wrong about the layer

§31.3 recorded "host recurrence edges are DIRECTIONAL **in the donor derivation**" and proposed
symmetrising the edges. `WORKFLOW_LESSONS.md` R4 then deferred that fix because symmetrising edges
would move donor rankings and recurrence semantics, and doing it safely needs a semantic
equivalence oracle. **The deferral reasoning was sound. The premise it rested on was not.**

Reproduced mechanically before changing anything, by rewinding to the state immediately before
QP2509 was authored — its answers removed, its `reused_from` edges un-adjudicated:

```
PRE  QP2509-Q6 family : []
PRE  QP2509-Q6 donors : []
PRE  QP2509-Q6 tier   : C          <-- "no donor"
PRE  QP2601-Q2 built  : True       <-- ...while the counterpart was already solved
PRE  stems equal      : False      <-- near, not exact: stem equality could not save it
```

Then the diagnosis was tested rather than trusted. Two synthetic fixtures recorded the same
adjudicated edge on one side only, in each direction:

```
edge recorded on B only ->  A family: ['QP2409-Q9','QP2506-Q1']  donors: ['QP2506-Q1']
edge recorded on A only ->  A family: ['QP2409-Q9','QP2506-Q1']  donors: ['QP2506-Q1']
```

**The adjudicated layer was never directional.** `build_families` unions `reused_from` as an
undirected edge and has always traversed both ways. There were no edges to symmetrise, and
"fixing" it would have meant inventing them.

## 32.2 The directionality is in the host annotation, one layer up

Census over every host token in the corpus:

| Direction | Tokens |
|---|---|
| Backward | 551 |
| Self | 252 |
| **Forward** | **0** |
| Unresolvable month | 16 |

The host prints a **cumulative** table — each token names the current sitting or an earlier one.
It is structurally incapable of naming a later sitting. MIW produces **newest-paper-first**. So
the only machine-readable trace of a relationship always sits on the paper MIW has *already*
solved, pointing at the paper it has not: invisible in the direction of travel.

Naming the layer correctly also dissolved R4's blocker. Inverting an *annotation* into a queue for
a human needs **no equivalence oracle** — the tool moves visibility, the author still makes every
judgement.

## 32.3 The fix — visibility, not judgement

`recurrence_model.reverse_hint_candidates` inverts the annotation and subtracts everything MIW has
already adjudicated. It creates **no family, no donor, no tier, no ranking**. `build_families` and
`donor_readiness` were not modified.

**Corpus delta: zero.** `2024_2026_RECURRENCE_AND_REUSE_MAP.md` and `SOURCE_INVENTORY.md`
regenerate **byte-identical**. No question changed donor state, readiness, preferred donor or
tier. No candidate-facing surface changed. `QP2404` remains the next production paper (3/9 Tier D,
reach 5, 1 temporal flag).

New generated document `REVERSE_HINT_CANDIDATES.md`, all 819 tokens accounted for and none
silently dropped:

| | Tokens |
|---|---|
| Ambiguous form (`SR09`, `JAN2`, `JULY(M)`) | 16 |
| Names a sitting but not a question | 225 |
| Outside the transcribed corpus | 199 |
| Points at itself | 251 |
| Already adjudicated by MIW | 103 |
| **Surfaced as unadjudicated** | **25** (16 targets) |

## 32.4 STOP-AND-REPORT — 25 pairs rest on host metadata alone

Per the session's own boundary: every surfaced row depends **only** on raw host metadata with no
MIW adjudication, so **none was promoted**. **12** of the 16 targets pair an unsolved question with
an already-built counterpart — the exact shape of the QP2509-Q6 miss. **Two are in QP2404 itself:**
`QP2404-Q4` ← `QP2506-Q1` and `QP2404-Q6` ← `QP2602-Q6`.

**These are not donors.** A row becomes real only when an author reads both questions and writes
`reused_from` — at which point the adjudicated layer picks it up in both directions unaided.

## 32.5 Positive control — pre-fix FAIL, post-fix PASS

Self-test cases 8–11 added to `build_reuse_map.py --self-test`. Run against the **pre-fix**
`recurrence_model.py` restored from `HEAD`:

```
AttributeError: module 'recurrence_model' has no attribute 'reverse_hint_candidates'
```

The capability did not exist, so the test cannot pass by accident. Post-fix: 8a the boundary holds
(no adjudicated donor appears — if this ever flips, provider metadata has been promoted to truth);
8b the reverse index surfaces `QP2601-Q2`; 9 no reverse candidate leaks into any family or donor
list across all 25 rows; 10 a mutation removing the adjudication filter makes the adjudicated pair
reappear, proving the filter load-bearing; 11 all 819 tokens accounted for. **All PASS.**

## 32.6 PIL V1.1 — implemented

`CANDIDATE_FACING_PAID` joined `ESCALATING`. The V1 advisory NOTE was **removed** rather than kept
alongside: reporting the same page twice under two severities is how a signal gets learned as
noise. Retrospective proof over `a5f2551^..a5f2551 --target QP2509`:

```
FOUNDER REVIEW REQUIRED -- 8 change(s)
    CANDIDATE_FACING_PAID DERIVED_NON_TARGET  meoclass1/pastpapers/QP2601.html
```

Detection and reporting only, as decided — nothing blocks. 42 controls, 0 failed, including a
mutation that removes `PAID` and confirms the escalation falls silent again.

## 32.7 `validate_antipatterns.py` — there was nothing to repair

Verified: **no `hooks` key in any settings file** — `~/.claude/settings.json`, both repo `.claude/`
trees, no `settings.local.json`, no managed-policy directory — and **`validate_antipatterns.py`
exists nowhere on disk**. §2901 of this file had already reached that conclusion; `CURRENT_STATUS.md`
item 10 was the stale half of a contradiction between the two documents, and it re-cost
investigation time in this session. Struck from state.

Acceptance-tested with a representative scratch write and edit: no hook error, no silent failure,
no process leak. Its intended protection is already carried by `validate_spec.py`,
`known_traps_check.py`, `recurrence_check.py`, `temporal_sweep.py` and `health_check.py`, each of
which positive-controls itself.

## 32.8 Validation

`run_toolchain.py --self-test`: **ALL STAGES PASS**, 110 warnings — identical to the pre-change
baseline. TEMPORAL, SURFACE, REUSE and RECURRENCE self-tests all green; known traps, health, audit
and 11 UI pages green. Determinism: after a full build the only modified tracked files are the
three tool files. No generated artefact moved.

## 32.9 Next

**QP2404 — April 2024, unchanged.** Not started, deliberately. Before authoring `QP2404-Q4` and
`QP2404-Q6`, read `REVERSE_HINT_CANDIDATES.md` — the host links each to a built counterpart and
MIW has not ruled on either. **Adjudicate by reading both questions. Do not plan them as donors.**

**NO MAIN MERGE. NO PRODUCT LAUNCH. INFRASTRUCTURE FOUNDER-REVIEW ONLY.**

# 33. QP2404 — REVERSE-HINT ADJUDICATION LANDED, AUTHORING STOPPED AT 4/9 — 2026-08-11

Branch `pastpapers/qp2404-founder-review`, cut from the verified hardening head `c612a02`
(confirmed a descendant of both the QP2509 content head `a5f2551` and the PIL V1 tooling head
`850bdde`). Baseline reproduced from canonical tooling, not carried forward: 252 / 99 / 153,
11 solved papers, `health_check.py` 0 errors 0 warnings.

## 33.1 Source verification

`APRIL 2024.pdf`, serial **EM-2404**, two pages, nine questions. The transcribed spec matches the
printed paper exactly, **including the examiner's own errors**, which are reproduced and not
corrected: `loT` for IoT throughout Q1, `(Ill)` for `(iii)` in Q5, the `Q7)` numbering style, and
the host tokens `2024/APR/Q78` and `2024/APR/9`. Printed marks sum to 16 per question; six answered
questions give 96 against a printed "Total Marks — 100", and that discrepancy is on the source copy
and is preserved.

## 33.2 The reverse-hint queue's first production test — 3 surfaced, 3 accepted, 0 rejected

Three rows touched this paper. All three were adjudicated by reading both printed stems. Diffs are
on the **normalised** stem, so case, punctuation and printed marks are already discounted.

| Pair | Normalised difference | Ruling | Effect |
|---|---|---|---|
| `QP2404-Q4` ← `QP2506-Q1` | `to`→`in`, `improvements`→`improvement` | EXACT | **new donor, C → D** |
| `QP2404-Q6` ← `QP2602-Q6` | one inserted `proper` | EXACT | already D; third donor |
| `QP2404-Q5` ← `QP2409-Q8` | `(Ill)` → `(iii)`, a scanning artifact | EXACT | none — counterpart unbuilt |

**The mechanism is useful, and this is why.** A family edge forms on `reused_from` or on EXACT
equality of the normalised stem. Each pair above is the same examiner task and misses that equality
by one or two words. The exact-equality rule is correct and was not weakened; the queue is what
reaches the cases sitting just outside it. In Q5's case the corpus was hidden from itself by an
**OCR error** — the source copy renders the roman numeral `(iii)` as `(Ill)`, and nothing else in
the pipeline was looking for that.

**It also corrected two already-built pages.** Before adjudication `QP2506-Q1` and `QP2602-Q6` each
rendered **"Once in this set"**. Both are repeats — the rudder question is held at three sittings and
the general-average question at five. Landing the edges moved both to "Repeated — reworded" and grew
`QP2508-Q6`'s family from four members to five. Three built pages changed as a result.

## 33.3 PIL run prospectively, before adaptation — its first such use

`temporal_sweep.py` was run over the donor and support specs **before** any answer was adapted.
13 findings fell on this paper's donor set and each was adjudicated:

- **4 `INTERNAL_QREF` — REAL.** `QP2506-Q6` carries "See Q5 of this paper" and `QP2508-Q6` "See Q1
  of this paper", both pointing at their own paper's LLMC limitation question. **QP2404 has no
  limitation question**, so on this paper those numbers are antifouling paint and IoT. The
  cross-reference was **dropped, not renumbered**.
- **5 `POST_SITTING` `2027` — LEGITIMATE.** The STCW comprehensive review. HTW 10 sat **5–9 February
  2024**, two months before this examination, and agreed the roadmap, methodology and review areas
  with adoption targeted 2027. Sitting-known and citable, with nothing adopted.
- **2 `POST_SITTING` `August 2026` — REAL.** "Nothing had been adopted as at August 2026" is an
  authoring-date statement and does not travel backwards.
- **2 `2026` — FALSE POSITIVE** as a temporal flag: internal corpus provenance ("identical to three
  built 2026 objects"), not a regulatory date. Rewritten anyway because the count changes.

Nothing was suppressed to produce a clean list. One methodological catch worth recording: an initial
filter of the sweep's JSON keyed on `question_id` where the field is `question`, and returned **zero
findings on the donor set**. That false clean was noticed and corrected. A filter that returns
nothing is a claim that must be tested, not a result.

## 33.4 Temporal findings from primary sources

- **Q2 — the flag was real.** At April 2024 **no IMO instrument governed ammonia as fuel**.
  `MSC.1/Circ.1687` is dated **26 February 2025** and was approved at **MSC 109 (2–6 December 2024)**
  on a proposal from CCC 10 — read verbatim from the circular. The route at this sitting was SOLAS
  II-1/55 alternative design read with the IGF Code's goal and functional requirements.
- **Q8 — a wrong-edition trap, and the sharper of the two.** `A.1188(33)`, adopted **6 December
  2023**, paragraph 5: **"REVOKES resolution A.1118(30)."** So the operative edition at April 2024 is
  the **2023 Guidelines**, and A.1118(30) — which stood for six years and is the natural default —
  had been revoked **four months before the sitting**.
- **Q5 — a trap running backwards.** Cybutryne controls under `MEPC.331(76)` entered into force
  **1 January 2023** and were in force at this sitting. An answer describing only the TBT position
  is wrong for April 2024.
- **EU.** EU ETS extended to maritime 1 January 2024 — in force. FuelEU Maritime adopted September
  2023 but applying only from 1 January 2025 — nameable as upcoming, never as applying.

**The generalisable finding: the 33rd IMO Assembly (December 2023) is a standing boundary for every
2024 sitting**, exactly as the 34th (December 2025) already is for 2025 sittings.

## 33.5 Why authoring stopped at 4/9

Q3, Q4, Q6 and Q7 were authored — the four donor-backed questions — and validated. The five
remaining are full fresh research, and two of them (Q2, Q8) sit on the wrong-edition trap the
protocol calls the most dangerous single error. Completing them plus nine verification records, the
sweeps, build, QA, determinism, UI review and surface impact would have meant writing regulatory
answers at speed. That is the failure this protocol exists to prevent, so the session stopped.

`PASTPAPER_PRODUCTION_PROTOCOL.md` §3 was applied: the completed objects were staged to
`staging/QP2404/`, the canonical spec was **restored to intake**, and the branch left green. The spec
on the branch carries **no answers** — only the three adjudicated edges, which stand on their own.

The resume is mechanical and was **verified this session by running it**: the two staged scripts
reproduce exactly 4 answered questions and preserve `reused_from` as `QP2509-Q4`, `QP2506-Q1`,
`QP2602-Q6`, `QP2508-Q4`. Two hazards in the staged scripts were found and closed before commit — a
hardcoded drive letter, and an overwrite of the `QP2602-Q6` edge that would have regressed an
already-built page to "Once in this set".

## 33.6 Machine

One stale session cluster reaped under the governed policy (+395 MB). Four further ended clusters
held ~5.8 GB but sat under the 120-minute threshold; the rule was **not** weakened to reclaim them.


---

# §34 QP2404 COMPLETED — 2026-08-11

Continuation of §33. Branch `pastpapers/qp2404-founder-review`, resumed at `b26ea45`, closed at
`84fee6f`. Three commits. No merge to `main`, no launch.

## 34.1 QP2601-Q9 authoring-date leakage — corrected

Founder decision 2 of the session prompt. The candidate-facing `study_notes` of a **January 2026**
paper carried *"and nothing had been adopted **as at August 2026**"* under the heading *"Currency —
what applies and what does not"*. August 2026 is the month the answer was authored.

Removed. One line, one clause, nothing else touched — the sentence already carried the
sitting-relative form ahead of it.

**The load-bearing check was on the sentence that was NOT changed.** The same paragraph says the
STCW comprehensive review had *"completion targeted around 2027"*. The IMO's own FAQ now gives
**2029–2030**. That revision is **not** a January 2026 fact: **HTW 12 (23–27 February 2026) agreed
the work plan extending to 2029**, a month *after* the sitting. "Modernising" the figure would have
been a forward temporal violation on an approved page. It was deliberately left alone.

**Scope held.** The same string also appears in `QP2601-Q9 unresolved[1]` and
`QP2601-Q7 reverify_before_publication[0].why`, but `build_paper.py` renders both inside
`if not publish:` — review build only. There the authoring date is correctly quarantined and it
stays. Two further **candidate-facing** instances — `QP2601-Q1` and `QP2602-Q2` — were **reported
for a Founder decision, not silently fixed**, being outside the authorised target and on
already-approved pages.

## 34.2 Guarded resume

`author_q4.py` then `author_q367.py`, exactly as `CHECKPOINT.md` specified. Reproduced Q3, Q4, Q6,
Q7; five unanswered. The one trap held: **`QP2404-Q6.reused_from` is still `QP2602-Q6`** —
verified after restore. `QP2506-Q6` and `QP2508-Q6` join the general-average family by exact stem
equality on their own; `QP2602-Q6` differs by the single inserted word *"proper"*, so the explicit
edge is the only thing keeping it in, and "tidying" it would have regressed an approved page to
*"Once in this set"*.

Exactly the four predicted errors on validation — the four missing verification records.

## 34.3 The five questions

Authored Q2 → Q8 → Q5 → Q1 → Q9, taking the demonstrated edition traps first.

**Q2 — ammonia.** Intake `GUIDELINE EDITION` flag confirmed **REAL**. At April 2024 no IMO
instrument governed ammonia as a fuel; `MSC.1/Circ.1687` is dated 26 February 2025, approved at
MSC 109 (2–6 December 2024). Answered through **SOLAS II-1/55 alternative design**, with CCC 9
(20–29 September 2023, toxicity principles agreed) as work in progress. The circular appears on
**no candidate-facing surface**.

**Q8 — ISM certification. The unflagged trap, and the more dangerous one.** `A.1188(33)` read at
source from the IMO's own copy; operative paragraph 5: *"REVOKES resolution A.1118(30)."* Adopted
**6 December 2023**, four months before the sitting. Eleven of its paragraphs carry the answer
(1.3.1, 1.3.2, 4.4.1–4.4.4, 4.5.1, 4.13.1–4.13.3, 4.14.1–4.14.3, Part 2). ISM Code section 13
(13.5, 13.5.1, 13.9) from an Administration reproduction. It bites because the substance barely
moved between editions: an answer citing `A.1118(30)` **reads correctly and is wrong only about its
authority**.

**Q8's open item, closed honestly.** Limbs (b)(iii) *extension of the SMC* and (b)(iv) *revision of
an entry* correspond to **no named IMO provision**. The whole of `A.1188(33)` was searched at
source for "extension", "revision", "withdraw" and "invalid" — none appears — and the ISM Code
provides renewal, not extension. Both limbs are answered by reasoning from the RO's delegated
authority, with the absence stated in the answer. Protocol §2.1 applied deliberately: an invented
paragraph number would have been far worse.

**Q5 — anti-fouling. The trap that runs backwards, and the intake flag was WRONG.** Intake said
`STABLE / LOW`. `MEPC.331(76)` read at source: cybutryne controls in force **1 January 2023**,
fifteen months *before* the sitting; remove or barrier-coat at the next renewal after that date and
**no later than 60 months** after the last application, with the platform/FSU/FPSO,
non-international and sub-400 GT exclusions; Annex 4 regulation 2(3) replaced; amended certificate
form read. Both the 60-month limit and the certificate transition were **still running at the
sitting** and are stated for that reason.

**Q1 — IoT.** Predominantly `ENGINEERING_JUDGEMENT`, declared. A third edition boundary was found:
`MSC-FAL.1/Circ.3/Rev.3` is dated **4 April 2025** and withdrew Rev.2 (7 June 2022). Resolved by
relying on `MSC.428(98)`, which is mandatory and has not moved, and putting **no revision number in
front of the candidate**.

**Q9 — UNCLOS.** The one question whose intake flag was **correct**, recorded as answered rather
than passed over. Live boundary: the **BBNJ Agreement**, adopted 19 June 2023 (before) and in force
17 January 2026 (long after) — named as adopted and awaiting entry into force, never as applying.

## 34.4 Sweeps

`temporal_sweep.py` returned **4** candidates on QP2404, **all four legitimate**: `4 April 2025`
(Q1), `December 2024` and `February 2025` (Q2), `2027` (Q7). The first three sit inside explicit
**exclusion** statements; the fourth is sitting-known (HTW 10 sat 5–9 February 2024, two months
before the paper). See lesson 14.

The zero-result control of lesson 12 was applied and passed: the output key is `question`, the base
run returned 4 non-zero, and `--self-test` / `--retrospective` both fire.

Targeted sweeps over the finished paper: **zero** occurrences of "as at August 2026"; **zero**
candidate-facing `MSC.1/Circ.1687`; **zero** candidate-facing internal Q-references; all eleven
candidate-facing `A.1118(30)` occurrences name it **as the revoked predecessor**.

## 34.5 Build, QA, UI

`run_toolchain.py` and `--self-test` both **ALL STAGES PASS**. Determinism: **20 generated files
byte-identical** across a rebuild. `ui_behaviour_test.cjs` **61 passed, 0 failed** after a QP2404
fixture was added through the established pattern — its `regulation` probe is `a.1188(33)`, so the
probe guards the wrong-edition trap, and its `recurrence` entry is a **leak** probe asserting the
host sitting code is not searchable.

HTTP review at 1280 and 375. Nine cards, five modes, Answer the visible default on all nine, no
console errors, no horizontal page scroll at either width, deep links `q1`–`q9` resolve, live
search verified including an alias never rendered (`nh3` → Q2) and the host-code probe returning
empty. **The server survived the first teardown**: the bash job id was not the Windows PID. Killed
by real PID and the listener confirmed gone.

## 34.6 Surface impact

`surface_impact.py --base b26ea45 --target QP2404`, 42 controls passing. **5 new**
`DERIVED_NON_TARGET` changes, distinct from the 11 the Founder accepted in §33:
`QP2601.html` (`CANDIDATE_FACING_PAID`, from the §34.1 correction) and four `PUBLIC_FREE`
surfaces regenerating because QP2404 joined the solved set.

## 34.7 Corpus

**252 / 108 solved / 144 unsolved**, 12 solved papers — the predicted +9 / −9, calculated not
assumed. Derived Tier D over the unsolved set **22 → 20**: QP2404's own four left the set, and
solving it newly unlocked **`QP2409-Q8`** (from `QP2404-Q5` — the reverse-hint edge paying off
directly) and **`QP2411-Q2`** (from `QP2404-Q2`).

Next paper recommended: **QP2511**. Not started.

## 34.8 Found and left alone

`QP2509` is answered 9/9 but its spec still records `build_state: Intake Complete` and
`review_state: "Answerless intake — questions only, no answers authored"`. Every other solved
paper records `Pilot Review Ready`. Nothing downstream reads these fields, so the toolchain is
green either way. Another paper's branch; reported, not touched.

## 34.9 Machine

Three stale clusters reaped under the governed policy at session start (~4.3 GB eligible). Two
further ended clusters sat under the 120-minute threshold and the rule was **not** weakened.


## 34.10 Founder follow-up — both reported items fixed

The Founder authorised both items reported at the close of §34. Commit `caf5020`.

**The scan found three times what the report named.** The report said two candidate-facing
authoring-date leaks. A field-class-aware scan of the whole corpus — the discipline of lesson 13,
applied properly this time — found **six across five papers**, and corrected two errors in the
original report: the second instance is `QP2602-Q4`, not `QP2602-Q2` (the earlier id came from a
line-number grep rather than a parsed object), and `QP2506-Q5`, `QP2508-Q1`, `QP2602-Q8` and
`QP2607-Q7` had been missed entirely because the first grep searched only for *"August 2026"* —
**two of them say February 2026**.

*Searching for the string you happened to find is not the same as searching for the defect.* The
scan now tests `as at <month> <year>`, `as of <month> <year>` and the bare token, and classifies
every hit by render path.

**Five corrected, each judged separately:**

| Paper | Sitting | What the authoring date was doing | Fix |
|---|---|---|---|
| `QP2506-Q5` | Jun 2025 | provenance reasoning (*"verified unchanged as at February 2026, which covers this sitting"*) | anchored to the sitting; the provenance belongs in the verification record |
| `QP2508-Q1` | Aug 2025 | the reasoning **is** the point — why stability *"can be asserted rather than hoped"* | logic preserved in sitting-relative form, month removed |
| `QP2601-Q1` | Jan 2026 | pure authoring context; the heading already said *"what was true in January 2026"* | clause removed |
| `QP2602-Q4` | Feb 2026 | the STCW paragraph already corrected on `QP2601-Q9` | identical edit, so the family stays identical |
| `QP2607-Q7` | Jul 2026 | asserted a state **one month after its own sitting** | anchored to the sitting; the checking instruction kept |

**One deliberately kept.** `QP2602-Q8` reads *"Currency warning for anyone revising this after
August 2026: … the sitting-date answer above remains correct for February 2026 but the current
position will differ."* Explicitly labelled as later context, clearly quarantined, and it
**protects** the sitting answer. The date is load-bearing — it tells the reader when the snapshot
was taken and therefore what to re-check. Editing it to make a counter read zero is precisely what
lesson 14 forbids.

**`QP2509` state corrected** to `Pilot Review Ready` / *"Awaiting Founder Review — complete paper"*,
version 1.0. All 28 papers now check consistent.

**A correction to §34.8.** That section said nothing downstream reads `build_state` and
`review_state`. That is wrong. The two HTML renderings are publish-guarded, but `build_index.py`
writes both into `pastpapers_content_index.json` **unconditionally**, and `surface_impact.py`
classifies that manifest as `PUBLIC_FREE`. The stale value was sitting in a public artefact, which
makes the fix more clearly right than the original report implied.

**Verification.** Toolchain and self-test both ALL STAGES PASS; determinism zero drift over 20
files. The load-bearing check was on **shipped bytes**: each built page was stripped of its
`prod-meta` and review-banner blocks and re-scanned, leaving **exactly one hit corpus-wide** — the
`QP2602-Q8` keep. That strip is also the first empirical test of lesson 13's field-class model
against rendered output rather than against source: every review-only instance really is confined
to the review build.

Surface impact against `440eebf`: 8 non-target changes — six `CANDIDATE_FACING_PAID` paper pages
plus `index.html` and the manifest. All are the intended effect of a Founder-authorised correction,
and all are reported rather than assumed.

---

# 35. Solved QP commercial architecture recovery — 2026-08-11

Branch `commerce/solvedqp-recovery`, from `bf87b1a` on
`pastpapers/qp2404-founder-review`. Six commits. Nothing merged, nothing deployed,
no secret set, no payment path exercised.

## 35.1 What this session was

The Solved QP delivery architecture and the Security V2 access stack existed only on
`commerce/solvedqp-security-v2`, which was never merged. The production lineage forked
at `217fbba`, *before* that branch's own security work, and had been carrying paper
production forward ever since. The task was to bring the architecture across
selectively, without merging the branch and without regressing eleven papers' worth of
later production work.

## 35.2 The security incident came first

`api/check-db.js` and `api/migrate-users.js` — unauthenticated handlers, one exposing
database state and one performing a bulk user migration — were still live in this
lineage. They had been deleted on the commerce branch by `76cc003`, but that deletion
lived only on the branch nobody merged. **The fix existed; it just was not where it
mattered.** Deleted here in its own commit before any recovery work.

A sweep of the tracked tree afterwards found no hardcoded customer credentials. The one
`MIW-` literal in `SQ/pay.html` is an input `placeholder` attribute showing the password
*format*, not a password. `surface_impact.py` already classifies both deleted paths as
`SECURITY`, so a reappearance escalates rather than passing quietly.

**Password rotation: UNCONFIRMED.** No evidence of completion exists in the repository.
Not attempted, not assumed. Launch blocker, not an engineering blocker.

## 35.3 The recovery was cleaner than expected, and provably so

Before porting anything, every overlapping file was compared three ways: fork point
`217fbba`, the commerce branch, and current.

For all six overlapping files — the four money paths, `SQ/pay.html`, `SQ/index.html` —
**current was byte-identical to the fork point.** This lineage had never touched them
after the branch was cut, so there was no later fix to preserve and taking the commerce
version was a port rather than a regression. The three-way comparison did not just guide
the merge; it *proved the merge was safe*, which no amount of reading the diffs would
have established on its own.

The eighteen additive files had no counterpart at all and were recovered by path with
their index blob hashes verified identical to the source branch.

## 35.4 Where the two branches genuinely disagreed

The four delivery-tooling files had diverged on **both** sides, and one disagreement
mattered.

The commerce branch kept a candidate from seeing the source-copy host's recurrence
annotation and the `recurrence_class` authoring field by **gating them behind
`publish`**. This lineage had since solved the same problem by **deleting both**:
`search_tokens` drops them unconditionally in every mode, and the card renders
`corpus_relations()` — MIW's own chronological model over its own transcriptions.

Porting the commerce gating would have *reintroduced the very fields current removed*.
The delivery guards settle it independently: current's labels are "Once in this set" and
"Repeated — reworded", which the checker's forbidden-label list does not match. The
stronger rule already satisfied the weaker one, so only the delivery plumbing was taken.

## 35.5 Two defects found while porting, neither reported by any test

**The storefront was frozen at fork time.** `SQ/index.html` advertised "Six complete
solved sittings — 54 questions" and listed 2026 months only. The product is twelve
sittings and 108 questions across three years. Restoring the file unchanged would have
under-described a paid product on a public page. No test asserts on marketing copy;
only the three-way comparison surfaced it. Corrected from the specs.

**Cross-links break on the delivery surface.** `cross_links` are authored relative to
`/meoclass1/pastpapers/`, so `../QB10_B.html` resolves correctly there and resolves to a
non-existent root path from `/solvedQP/`. The delivery guard matches *absolute*
`href="/meoclass1/..."` only, so these would have shipped as silent dead ends inside a
paid page. Delivery now keeps only sibling links to papers that are actually delivered.

## 35.6 Year-aware navigation

The audit's known defect: delivery navigation carried one hard-coded link to
`questions-2026.html`. Correct while 2026 was the only solved year; with 2024 and 2025
solved it offered a 2024 reader the 2026 sheet and no route to their own. The link
resolved and the page existed, so nothing failed.

Fixed by `delivery_links(year=...)` — a paper links to its own year, a year sheet links
to itself, the home carries one link per solved year — and then **guarded**, because a
defect that breaks nothing is exactly the kind that returns. The guard is proved by
mutation: a synthetic 2024 page offering only the 2026 sheet must be rejected, and is.

## 35.7 Results

- Offline security: **62 tests pass, 0 fail** across both suites, each carrying positive
  controls, so passing is evidence the guards fire rather than evidence they never ran.
- Offline gate matrix: `/meoclass1/pastpapers/` requires `SOLVED_QP`, not
  `ORAL_QB_NOTES` — the rule that stops the ₹1,500 Written library being handed to every
  Oral customer. Traversal normalises before matching. Misconfigured and evicted both
  deny.
- Delivery: **16 files** — 12 papers, 3 year sheets, 1 index — plus the Oral-subscriber
  promo. 108 questions across 12 papers, derived by the checker, never asserted by the
  generator. The 16 intake specs were skipped by `is_intake()`.
- `solvedqp_check.py --self-test`: all eleven guards fire on pages built to trip them.
- Determinism: two consecutive full builds byte-identical across all 16 files. All output
  LF. `*.mjs` was unpinned in `.gitattributes` and is now pinned — the recovered security
  tests were the tree's only `.mjs` files and would have been checked out CRLF.
- Review build byte-identical after the refactor: the existing product is untouched.
- Full toolchain: **ALL STAGES PASS**, `run_toolchain.py` is `+43/-0`, no stage lost.

## 35.8 PIL

Surface impact against `bf87b1a`: **38 changes escalated for Founder review** — 17
`SECURITY_SENSITIVE`, 17 `CANDIDATE_FACING_PAID`, 2 `COMMERCIAL`, 1 `PUBLIC_FREE`, 1
`UNKNOWN_REVIEW`. This is the expected shape for a recovery and is reported, not
suppressed.

The first run classified the whole delivered product as `UNKNOWN_REVIEW` — escalated, so
nothing was hidden, but "unclassified" is weaker than the truth. Rules for `solvedQP/`
and `meoclass1/oralnotes/` were added as `CANDIDATE_FACING_PAID`. `.gitattributes` stays
`UNKNOWN_REVIEW` deliberately: it carries no rule and it silently determines the bytes
every delivered file is checked out with, so being asked about it is correct.

## 35.9 Carried, not lost

`SQ/solved-qp-sample-january-2026.html` was already modified in the working tree when the
session began: 11 → 12 sittings, April 2024 added, and the removal of "and still as at
August 2026", an authoring-date leak that dates the page the moment the month passes.
Verified against the specs and committed on its own, so it reads as current product work
rather than as part of the recovery.

---

# §36 — QP2511, NOVEMBER 2025: STOPPED AT 1 OF 9

**2026-08-11.** Branch `pastpapers/qp2511-founder-review`, from `commerce/solvedqp-recovery`
@ `462cfbc`. Heads: `4c22510` (anchor), `886cfd0` (Q9 + checkpoint), and the state/history
commit that follows.

## 36.1 What this session was and was not

It was a full production attempt on QP2511 and it did **not** produce a paper. It produced the
complete research foundation for one, plus one finished question. The spec was left untouched at
answerless intake, nothing was built, and `solvedQP/` still delivers 12 papers and 108 questions.

That is the protocol working rather than failing. `PASTPAPER_PRODUCTION_PROTOCOL.md` §3 forbids a
half-authored-paper state and §4 forbids building an incomplete paper; promoting the one authored
question into the spec would have produced a paper that renders, indexes and counts as solved with
eight answers missing. The corpus's own history calibrates this — QP2404 stopped at 4/9 and QP2403
at 2/9 before later sessions finished them.

## 36.2 Baselines, all three green before anything was touched

Corpus 252 / 108 / 144 across 12 solved papers, derived from the specs rather than carried
forward. `solvedqp_check.py` and its self-test green — 12 papers, 3 year sheets, 1 index, 19 pages
clean, 10 guards firing on the deliberately defective fixture. Offline security **62 / 62**
(34 + 28). `run_toolchain.py` ALL STAGES PASS. Every one of these was re-run at the end unchanged.

## 36.3 Source truth needed no correction

Both pages read back visually against a 150 dpi render, closing the residual risk the intake spec
had itself recorded (*"Pages read back this session: 1 of 2"*). Serial `EM – 2511`, marks printed
only on Q7/Q8/Q9, and all three printed anomalies — Q2's sentence break, Q3's missing word, Q6's
missing verb — confirmed and correctly preserved.

## 36.4 The reverse-hint queue paid out again

Three unadjudicated rows, all three ruled by reading both printed stems. Q4 and Q6 are EXACT
(`fueled`/`fuelled`; a dropped verb). Q3 is NEAR — the November stem is a **compressed** form that
folds "who can issue these certificates in India" into "the different certificates in India".
`QP2604-Q6` was rejected as preferred donor on shape and recorded as a family member so it cannot
silently become one later. **Tier D 3/9 → 6/9.**

## 36.5 The stored donor field was stale and the derived layer was right

The intake spec named `QP2602-Q7` (February 2026) for Q9. The derived reuse map prefers
`QP2508-Q7` (August 2025), and it is correct: an earlier same-year donor is a **forward**
adaptation and avoids a backwards pull entirely. `QP2508-Q7`'s own verification record had
predicted exactly this under *Family benefit*. This is the concrete instance of the standing rule
that stored `reuse_tier` and `reused_from` are not to be trusted.

## 36.6 Three boundaries established, two of which bite on unauthored questions

**The 34th Assembly sat 24 November – 3 December 2025** — it convened *inside* the sitting month
and adopted at the close. The exclusion therefore holds for the whole `A.12xx(34)` family, and the
operative Assembly editions at this sitting are the 33rd Assembly's of 6 December 2023. This bites
on **Q5**, whose March 2026 donor may legitimately cite the **2025** HSSC Survey Guidelines.

**The Merchant Shipping Act 2025** was assented 18 August 2025 and commenced only **15 March 2026**
(`S.O. 1244(E)`), established repository-first from the `QP2607/Q7` record which read the Gazette
and the commencement notification directly. At this sitting the **1958** Act governs. This bites on
**Q8**, whose donor reasons about the 2025 Act as live law across several study-note blocks.

**FAL** was researched to primary level for Q7 even though Q7 is unauthored: `FAL.15(47)` was read
in full from the IMO resolutions CDN. Its operative paragraph 2 is a quotable tacit-acceptance
determination — in force 1 January 2025 unless one third objected before 1 October 2024 — and it
amends **Recommended Practice 7.11**, not the garbage-record-book item the IMO summary page
attributes to it. The primary text governs; that summary page must not be authored from.

## 36.7 A legitimate future date, kept

`26 June 2030` appears seven times in the Q8 donor and is the Hong Kong Convention's **own**
transitional deadline for existing ships — equally true and equally stateable in November 2025. It
was adjudicated as keep. A blind date-strip would have deleted a correct answer point. `PIL FLAGS;
CLAUDE ADJUDICATES` earned its keep on a paper where five of six donors run backwards.

## 36.8 The contamination was where it was least expected

The session was set up to reverse the currency corrections of five backwards donors. The internal
`Q`-reference defect — the QP2509 class — turned up in `QP2508-Q7`, **the one donor pushed
forward**. Promoted to a workflow lesson: post-sitting dates travel backwards, but internal
cross-references are relative to the donor's own paper and travel in both directions, so the
reference sweep must never be directional.

## 36.9 PIL surface impact, and `staging/`

4 changed paths, all `TARGET_DIRECT`; nothing touched a non-target public, paid, commercial or
security surface. Two rows classify `UNKNOWN_REVIEW` because `staging/` is a new top-level
directory with no rule. **No rule was added.** Following the `.gitattributes` precedent of §35.8,
being asked about a new top-level directory in a public repository is the correct outcome, and it
is reported to the Founder rather than suppressed.

---

## §37 — QP2511 RESUMED AND COMPLETED 9/9 (2026-08-11)

Resumed `pastpapers/qp2511-founder-review` from `cb85c82` with **1 of 9 authored**. Ended with the
paper **complete, assembled, built, delivered and swept**, and `staging/` retired.

### Starting state, verified rather than assumed

Branch and head matched the prompt exactly. `run_toolchain.py` **ALL STAGES PASS**; corpus derived
independently at **252 / 108 / 144, 12 solved papers**; delivery at **12 papers, 3 year sheets, 1
index**; offline security **62/62**. Governed stale-session cleanup reaped **2 eligible clusters**
(184 min and 155 min old), recovering 735 MB; the 82-minute cluster was correctly skipped and the
120-minute threshold was **not weakened**.

### The three anchor predictions — one confirmed, two cleared

The paper's temporal anchor named three places where a backwards donor would bite. Investigating a
prediction and finding **nothing** is a completed piece of work, and all three are recorded either way.

| Question | Anchor prediction | Outcome |
|---|---|---|
| **Q8** | The March 2026 donor reasons under the **Merchant Shipping Act, 2025** | **CONFIRMED — reversed in six places** |
| Q5 | The March 2026 donor may cite the **2025 HSSC Survey Guidelines** | **ABSENT.** Donor cites no HSSC, no `A.12xx(34)`, no 2025/2026 edition |
| Q3 | The Merchant Shipping Act boundary is "available" on the Indian issuing authority | **ABSENT.** Donor contains **zero** occurrences of "Merchant Shipping" in any field |

### Q8 — the conclusion survived, the reasoning did not

The donor was sat on or after **15 March 2026**, the commencement date of the 2025 Act, and treated
it as live law in six fields. At this sitting the Act had **assent (18 Aug 2025) but not
commencement**, so the **Merchant Shipping Act 1958** governs.

The subtlety worth preserving: **India's recycling law is the same at both sittings** — the Recycling
of Ships Act, 2019 is separate legislation either way. So the donor reaches a **right conclusion
through a premature premise**: it asserts the effect of a repeal provision that had not yet taken
effect. Nothing downstream catches that; the sentence is coherent, confident and about the right
statute. `26 June 2030` was adjudicated **KEEP** — the Convention's own transitional deadline.

### Q3 — the compressed stem changed the answer

This sitting prints **three** demands where the January 2026 donor prints four, folding *"certificates
issued to a vessel **for maintenance of the ship in good health**"* and *"who can issue these in
India"* into *"the different certificates **in India**"*. The deleted qualifier is the one the donor's
own gate had relied on to confine the limb to the ship — and this stem's first sentence names *"the
ship **and the crew**"*. A **sixth route step** was authored on the seafarer's medical certificate,
primary-verified this session from the ILO's own MLC FAQ: Standard A1.2 ¶7 (two years / one / six)
and ¶9 (expiry in voyage, to the next port, **not exceeding three months**). The printed word
*"options"* is plural and now has two answers: **ship 6+1, crew 2 years + 3 months**.

### Fresh questions

**Q7 (FAL)** paid back the checkpoint's prediction exactly: `FAL.15(47)`, read in full for Q9, made
the amendment limb cheap to author *correctly*, and the two questions now cite the same instrument for
different purposes. **Q1** asserts **no casualty statistic** and **no `Derbyshire` date** — IMO's own
material does not quantify the losses. **Q2** is the corpus's first question with
`P1_PRIMARY_VERIFIED: 0`, correctly: no instrument prescribes what a torque rich condition is, and the
`regulations` field **states the absence** instead of being padded. MAN Energy Solutions' *Basic
Principles of Ship Propulsion* was read in full and supplies every quantity.

### The assembly guard earned its place

Assembly asserted identity, printed stem against intake, marks, state, evidence and card ids for all
nine **before** touching the spec. It **blocked**, on a real defect: the previously staged Q9 carried
the **donor's** `host_recurrence_hint` (7 entries) and had lost this paper's own `2025/NOV/Q9`.
Authoring-only and never rendered, so nothing candidate-facing was affected — but the donor's list
would have flowed into the recurrence intelligence as this paper's own. Corrected from intake and
recorded on the object.

### Defects found in my own drafting, and removed

- A study-notes block on Q8 originally taught the entry-into-force boundary **by naming the sittings
  at which this question has appeared** — provider recurrence intelligence, derived from
  `host_recurrence_hint`, on a candidate-facing surface. Rewritten to make the identical point
  (*check whether your notes predate 26 June 2025*) **without disclosing any sitting**. Verified 0 hits.
- Nine model-answer headings had drifted from their route steps, and Q2 used a non-vocabulary
  `primary_category` and a non-vocabulary archetype. The single-spine validator caught all of it.

### Outcome

`0 errors`. **ALL STAGES PASS** on `run_toolchain.py` and `--self-test`. Double-build **byte-identical
across 38 artefacts**. `solvedqp_check.py` and `--self-test` pass and **independently discovered** the
new paper: **13 papers, 117 questions**. UI reviewed over HTTP at 1280 and 375 — nine cards, five
modes, Answer default, every anchor and same-paper link resolving, no console errors, no horizontal
overflow, and the delivery pages carrying **no review banner, no provider leakage and no price**.
Security **62/62**. Server torn down and the listener confirmed gone.

Corpus **252 / 117 / 135, 13 solved papers**. Staging retired after verifying all nine staged objects
were hash-identical to the promoted spec.

---

## §38 — PRE-CORPUS-SYNC HYGIENE AND PRODUCTION FREEZE (2026-08-11)

Not a paper session. No question was authored, no spec changed, no verification record moved.
The purpose was to close the QP2511 lineage cleanly, audit repository hygiene, and freeze a
trustworthy checkpoint before the Founder synchronises the completed MARPOL Annex VI corpus.

### 38.1 State was re-derived, not carried forward

Head verified as `fddae20` on `pastpapers/qp2511-founder-review`, tracked tree clean.
`health_check.py` 0 errors / 0 warnings; corpus **252 questions / 117 solved / 135 intake**,
**28 papers -- 13 solved, 15 intake**; `solvedqp_check.py` and `--self-test` green, **13 papers,
117 questions, 3 year sheets, 1 index**; security **62/62** (34 + 28). Every figure matched the
expectation in the session brief, so nothing had drifted while the branch sat.

### 38.2 The `.vercel` finding -- the one real hygiene defect

`.vercel/project.json` was **untracked and unignored** in a **public** repository. It carries the
Vercel `projectId` and the `orgId`. Vercel's own bundled README in that folder says it should not
be shared and states that linking normally self-adds the `.gitignore` entry -- which had not
happened here.

Nothing had leaked: the folder was never committed. But the only thing preventing publication was
the standing "never `git add .`" discipline, and a rule enforced by discipline is one slip from
failing. Ignored, along with `tools/notes/_*.txt` scratch output and the Founder's master
question-bank spreadsheets under `docs/MIW-master-Question-bank/`, each with the reason and the
reversal written into `.gitignore` beside it.

Untracked paths fell from **30 to 16**. The remaining 16 are all governance and design markdown
-- `Claude skill/`, `docs/agent-build/`, three root `ENGINEERING_PRINCIPLES` / `REPOSITORY_STATUS`
documents -- classified **FOUNDER REVIEW**. None was deleted. Ownership was not proven, so nothing
was moved.

### 38.3 Staging was already retired; one orphan remained

`meoclass1/pastpapers/staging/` held nothing but a `__pycache__` containing
`qpio.cpython-314.pyc`, bytecode for a helper whose source no longer exists. Git saw the
directory as clean because `__pycache__/` is ignored and git does not track empty directories.
The `.pyc` was removed. Two empty directories remain; a recursive removal was declined by the
environment and they are harmless, git-invisible, and safe for the Founder to delete.

**No finished paper looks partial.** QP2509, QP2404 and QP2511 all have their staging retired,
and `QP2509_AUTHORING_CHECKPOINT.md` was **kept** -- it is governed historical evidence, not
residue.

### 38.4 The corpus drift, which is the actual finding of this session

Two `RulesApp` trees exist on this machine and they are not the same thing:

| | canonical | MIW projection |
|---|---|---|
| `F:\RulesApp\repository\` | **1,006 nodes**, 14 subdirectories, `provision-truth/` present | -- |
| `F:\Marine-Intelligence-Weekly\RulesApp\repository\` | -- | **788 nodes**, `index/` only, `provision-truth-aliases.json` **absent** |

Both counted directly this session. The MIW copy is a **2026-07-25 snapshot, 218 nodes behind**,
and its `manifest.json` and `version.json` still report the old figure.

This also reconciles an apparent contradiction. `MIW_TRUE_SOURCE_CONTRACT.md` §13 reports 1,006
nodes; MIW's own `manifest.json` reports 788. **Neither is wrong** -- §13 measured the canonical
repository and the manifest describes the projection. The lesson generalises: a corpus count is
meaningless unless it names the tree it was taken from.

`provision-truth-aliases.json` being absent from MIW matters specifically, because §13 names that
file as the mechanism for resolving the **MARPOL Annex VI dual representation** -- 56 Annex
VI-shaped nodes split across `MARPOL-VI-*` and `MEPC32876-*` with no stated rule for choosing.
The resolver cannot answer an Annex VI question without it, and picking an id per paper would
fragment the corpus silently, without any build failing.

Recorded, with the sync destination and the consumption contract, in
`CORPUS_SYNC_AND_CONSUMPTION_PLAN.md`. **No corpus file was imported, copied or moved.** The
completed Annex VI work is not in the local canonical repository either -- only Annex I ODME
reg 31 and the two SOLAS II-1 batches are -- so the Founder's sync from the desktop is a genuine
prerequisite and no source path was invented.

### 38.5 Planned-soon was already built

The session brief asked for a design to generate "Planned soon" cards rather than hand-maintain
them. **That design already exists and already ships.** `build_questions_year.py` renders three
governed month states -- available, `KNOWN_ABSENT` -> *"No sitting"* with the serial-numbering
proof, and otherwise *"Not yet in the MIW set"*, worded explicitly as a statement about MIW's
coverage rather than about whether the examination was held. `paper_status()` returns
`'available'` only when answers exist, so a source PDF in a folder can never make a paper look
solved. Two checkers guard it.

The real delta is **one function**: `build_solvedqp_home.py::solved_sittings()` filters intake
papers out entirely, so the delivery home implies a 13-paper library rather than 13 of 28. Scoped
in `ONLINE_TEST_PLAN.md` §3.1 and deliberately **not implemented here**, because it moves
candidate-facing delivery bytes and this session's determinism requirement was that no product
byte moves.

### 38.6 Parallel production, and the conflict that would have bitten

Designed in `PARALLEL_PRODUCTION_BOARD.md` with an **empty** allocation table -- no branch
created, no paper allocated.

The load-bearing decision is the global-derived-artefact rule. Six paper branches would each
regenerate the reuse map, recurrence surfaces, search index, year sheets, `solvedQP/` and the
state documents wholesale. Git cannot merge that meaningfully, and a textual merge that
*succeeds* is worse than one that fails: it yields an index describing a corpus state that never
existed. So paper branches own `specs/QPxxxx.json`, `verification/QPxxxx/**` and that paper's
anchor doc; integration owns everything global and regenerates it **once per paper**.

One-at-a-time integration is a correctness requirement, not a throughput compromise -- solving a
paper changes the derived readiness of other papers, proven twice already in this corpus.

Six candidates proposed (QP2401, QP2410, QP2412, QP2409, QP2502, QP2411), with three constraints
that must travel with any allocation: QP2401-Q9 and QP2412-Q9 share an **identical donor set** and
must go to one owner or be sequenced; QP2410 carries the corpus's only HIGH-volatility donor pair
and must be re-anchored to October 2024 rather than inheriting November 2025 prose; and QP2504 is
**blocked** by the standing Rev.3 stop condition. QP2512 is deliberately excluded despite scoring
best -- its 34th Assembly boundary risk belongs where the temporal history lives.

### Outcome

Hygiene and state only. **No QP semantic spec changed, no verification record changed, no
delivery byte moved, no public sample changed, no security behaviour changed.** Toolchain,
`solvedqp_check.py` and both security suites re-run green after the changes. Corpus unchanged at
**252 / 117 / 135, 13 solved papers**; delivery unchanged at **13 papers, 117 questions, 3 year
sheets, 1 index**.

**QP production is PAUSED after QP2511.** The next Founder action is the corpus sync, not a paper.

---

# SESSION — 2026-08-11 — FIRST TRUE SOURCE CONSUMER INTEGRATION

**Branch:** `workflow/corpus-consumer-integration`, from the freeze head `9904af4`.
**Corpus consumed:** `RulesApp-Local-Input` @ `64977b8` (= `origin/main`, clean, 0 ahead / 0 behind).
**Work order:** `MIW::consumer-team::first-integration`. **No paper was authored.**

## What the corpus turned out to be

The receiving plan written in the freeze session assumed the completed corpus would arrive through
`F:\RulesApp\repository\` and be consumed as `repo-data.json` nodes. It does not. The True Source is
a **different private repository** — `RulesApp-Local-Input` — with its own governance, freeze records
and rights register. The `RulesApp` projection remains a legacy consumer store and is no longer the
resolver target.

That single fact retired a recorded blocker. `CORPUS_SYNC_AND_CONSUMPTION_PLAN.md` §2.1 made the
MARPOL Annex VI dual-representation problem a **stop condition** before any Annex VI reference could
be written. Measured this session: in the legacy projection the problem is real (56 Annex VI-shaped
nodes, 36 `MEPC32876-*` against 20 `MARPOL-VI-*`, no rule for choosing). In True Source it does not
exist — all **320** resolver entries are canonical `MARPOL-VI-*`, and `MEPC32876-*` appears only
among the 527 aliases, resolving **in** and never out, by a stated `identityPolicy`. The stop
condition was answered by reading the right store, not by adjudicating a tie.

## The finding the documents could not have told us

Three governing documents — the handover, `FD-RIGHTS-1` and the founder aim — agree that FSS is
cleared and text-bearing, and that the required non-official-status statement is *"already built into
the LSA and FSS consolidations"*. The **artifact disagrees**. The FSS derivative's own embedded
disclaimer, identical across BUILD-1 and BUILD-2, states its wording is a *"verified summary, NOT the
official text"*, marked INTERNAL USE ONLY and *"never for redistribution"*. Its `natureStatement`
certifies every provision **statement**, not every provision text.

The measurements agree with the artifact and not with the documents: 35 of 421 FSS provisions carry
no text at all, and 22 of the 386 that do are labels — `"Section"`, `"test switches"`, `"sea inlet to
pump"`. LSA, by contrast, carries 292 of 292 with per-provision `textSource:
official-base-ocr(MSC.48(66)) page-verified` and a shortest entry of 65 characters.

A Founder decision can reclassify MIW's own record; it cannot turn a summary into wording. Raised as
**TSCR-1**, not corrected — the corpus is read-only to consumers. FSS is integrated as verification
evidence and is refused as a quotation source, behind a guard test that fails on purpose if a future
FSS build ever carries real wording.

## What was built

`tools/corpus/consumer_adapter.py` keeps four questions apart on every result rather than collapsing
them into one boolean: `rights_cleared` (read live from the register, because the clearance is
revocable), `text_available`, `text_is_verbatim`, `text_adequate`. Only all four together make a
provision `quotable`. Bulk access is refused structurally — there is no chapter-level text call to
reach for. Missing objects return `NOT_FOUND`; nothing is ever fabricated.

`validate_spec.py` needed one honest correction. `REF_ID_RE` admitted hyphen segments only, so it
**rejected `LSA-1.1.1`** — the one corpus that is frozen, text-bearing and quotation-cleared. The
pattern had encoded an accident of the only worked example (`MARPOL-VI-14-146`) as though it were a
rule. **No schema change was needed**: the five `reference_shelf` fields were sufficient, exactly as
the contract predicted.

Pilot on three already-solved questions — `QP2508-Q3`, `QP2602-Q3`, `QP2607-Q4` — six entries, no
answer wording touched. The corpus **independently confirmed** the MSC.555(108) entry-into-force date
of 1 January 2026 that those answers had previously taken from a class-society notice, and confirmed
their sitting-relative handling was already right: QP2508 (August 2025) correctly records the
amendments as adopted but not yet in force; QP2602 (February 2026) correctly records them in force.
**No QP correction was required.** The FSS half of a recorded `unresolved` item is retired; the SOLAS
half stands, because SOLAS is not a ready corpus.

## Why the provision view is not built

Not caution — arithmetic. Of the three corpora, the one with real demand from solved answers
(MARPOL Annex VI) has **no text**; the one with both text and demand (FSS) has **summaries, not
wording**; and the one that is fully quotation-ready (LSA) is **cited by none of the 117 solved
questions**. There is no instrument on which the feature could be piloted today. Compounding it,
this repository is **PUBLIC**, so rendering corpus text into `solvedQP/` is a publication decision
distinct from the quotation clearance, and no ID→anchor deep link exists for any corpus.

Every pilot entry is therefore `REFERENCE_PENDING`: the paid publish build is byte-unchanged and no
dead "Verify source" control was emitted.

## Coverage, stated honestly

The product home derived its cards from `solved_sittings()` alone, so the 15 transcribed-but-unsolved
sittings were not unlinked — they were **absent**, indistinguishable from months that never had an
examination. Added a coverage section with three states and one deliberate silence: a month with
neither a spec nor a `KNOWN_ABSENT` record is **not rendered at all**, which is what stops the page
asserting sittings for the rest of 2026. `KNOWN_ABSENT` is imported from the year-sheet builder
rather than restated, so there is one statement of which months are genuinely absent.

Measured on the built page: 13 available (all linked), 15 planned soon (zero links), 3 no sitting.
August–December 2026 do not appear.

## Outcome

`run_toolchain` PASS and `--self-test` PASS · `solvedqp_check` PASS and `--self-test` PASS ·
`coverage_check` PASS with a self-test that patches the builder to emit an unevidenced sitting and
requires the check to catch it · `security.test.mjs` 34/34 · `sessions.test.mjs` 28/28 ·
`consumer_adapter_test` 60/60, deterministic across runs. Frozen corpus verified **unmodified** by
SHA-256 before and after. No private corpus file, source PDF or corpus text entered this repository.

Corpus unchanged at **252 / 117 / 135, 13 solved papers**; delivery unchanged at **13 papers, 117
questions, 3 year sheets, 1 index**.

**QP production remains PAUSED.** The next Founder actions are the provision-view decisions in
`CURRENT_STATUS.md` §6, not a paper.

---

# SESSION — 2026-08-12 — SECURITY REMEDIATION AND LIVE DEPLOYMENT

**Outcome: SECURITY REMEDIATED — WRITTEN PRODUCT LIVE FOR CONTROLLED TESTING.**
Production commit `f626d6b`. Started on `workflow/corpus-consumer-integration` @ `d2e09a4`.

Two blockers were briefed. Four were closed. The two that were not briefed were the ones that
mattered most, and both were invisible from inside the repository.

## What the brief got wrong, and how it was found

**The affected-account count was 100, not 28.** 28 was the size of the leaked git blob. Measuring
production instead of trusting the brief found 100 accounts holding legacy plaintext and zero
hashed. The second cause was `api/check-db.js`, a removed endpoint that had answered an
unauthenticated `GET /api/check-db?email=...` with the stored credential for any address supplied.
The exposure was therefore never limited to the git blob, and the brief's instruction — *"do not
assume all 28 still need work if production truth differs"* — was the single most valuable line in
it.

A previous session had hypothesised that some accounts would have been silently hash-upgraded by
ordinary logins. **Measurement disproved it: zero had.** Security V2 had never been deployed, so
the opportunistic upgrade path had never executed once. A hypothesis about production that nobody
had measured had been carried forward across two sessions.

## LAUNCH-BLOCK-3 — the gate had never shipped, because of a missing dependency

Probing the live domain to verify LAUNCH-BLOCK-2 found `/meoclass1/QB1_A.html` returning **HTTP
200, 280,350 bytes, to an anonymous request**. `middleware.js`, `routes.js` and `sessions.js` were
absent from `origin/main` entirely.

The cutover then failed to deploy:

    The Edge Function "middleware" is referencing unsupported modules:
        - __vc__ns__/0/middleware.js: @vercel/edge

`middleware.js` had imported `next` from `@vercel/edge` since it was written, but the package was
never in `dependencies`. Nothing caught it: the build script is `echo 'Build successful'`, and the
Edge bundler is the first stage that resolves the import — which had never run, because the
middleware had never been deployed. **A missing dependency presented for weeks as a public content
exposure.**

## LAUNCH-BLOCK-4 — the deploy caused it, the Founder found it in minutes

Immediately after the cutover the Founder signed in and saw *"No products are attached to this
account yet."*

`miw:ent:*` held **zero records for all 100 accounts**. `migrate_entitlements.mjs` — which
translates the pre-V2 model (*has a password therefore may open /meoclass1/*) into per-product
entitlements — had never been run. While `/meoclass1/` was ungated this was invisible: customers
read the content regardless. The gate then began correctly enforcing an entitlement that had never
been recorded for anyone.

**The deploy converted a silent data gap into 100 locked-out paying customers**, and the only
signal was a real person signing in. Closed by running the back-fill: 100 granted
`ORAL_QB_NOTES`, 0 granted `SOLVED_QP`.

## Ordering decisions that mattered

- **The secret was set AFTER rotation.** Setting `MIW_SESSION_SECRET` first would have re-armed
  every leaked password, because the secret is what makes the login path operative at all. While
  it was absent, `check-password.js` returned 500 before even reaching the password check — the
  compromised credentials were unusable, and restoring service was what re-armed them.
- **Legacy plaintext was removed AFTER rotation, never before.** Removing it earlier would have
  locked out every customer whose record had not been upgraded — which, since V2 had never
  deployed, was all 100.
- **Rotation writes the credential, then revokes sessions, then emails.** Revoking first and
  failing to write leaves the old password valid; emailing first announces a change that has not
  happened. The email is last because it is the only irreversible step and the only one whose
  failure leaves a recoverable state.

## Work delivered beyond the brief

- **Funnel**: nothing under `/meoclass1/` linked to `/solvedQP/` and nothing linked back. All 100
  Oral subscribers had no route to discover the Written product. Cross-sell added to the Oral hub
  and the Oral notes header, carrying the five-mode explainer verbatim from `solvedQP/index.html`.
- **Subscriber ceiling removed**: `assignNewPassword` drew from `QB_PASSWORD_POOL` by index and
  threw past its end — *after* Razorpay captured the payment and after the fulfilment lock was
  claimed. Exhaustion meant money taken, no entitlement, no email, and a webhook retrying the same
  failure forever. Credentials are now generated per sale.
- **Self-service password reset**: cannot resend an existing password and never will be able to.
  Issues a new one, throttled one per address per 15 minutes, revoking all sessions, with a single
  constant response for every path.

## Process failures worth recording

- **Two Claude sessions were committing to the same release branch concurrently.** Detected when
  a merge reported "Already up to date" seconds after another session had performed it, and two
  unfamiliar commits appeared. Concurrent `rotate --confirm` runs would have rotated and emailed
  every customer twice, with the first password dead on arrival. The rotation tool's default scope
  excludes already-hashed records, which limits the damage structurally, but the session should
  have been confirmed stopped before any customer-impacting run.
- **Operator credentials were pasted into the chat transcript** rather than into the git-ignored
  file that had been prepared for them. The Upstash token, Brevo SMTP key and a Brevo account
  password must be rotated at source.
- **A live enumeration probe used the Founder's real address**, resetting their password a second
  time. A throwaway address should have been used.

---

## 20. STOREFRONT AND SAMPLE WORK — 2026-08-12 (second session)

Production commits `a3a3003` and `2f38586`. Started as a request to change one link on the Oral
notes header; found two live exposures on the way.

### 20.1 The public QB page was publishing the paid product — `a3a3003`

`SQ/QB1_A.html` served **94.7% of the paid `meoclass1/QB1_A.html`** to anyone, no gate, linked from
the storefront. 11 of 12 randomly sampled long sentences from the paid file appeared verbatim.

This was **not** a gate failure. `/SQ/` is deliberately outside the middleware matcher so the
storefront and login work without a session, which means anything placed there is *published by
definition*. `examiner-index.html` (4% of paid) and `index.html` (39%) are correctly trimmed; this
one was a near-complete copy dropped in and never cut.

The 17 "lock" markers already in the file were a **red herring** — the substring `lock` inside CSS
`display:block` and `white-space:nowrap`. There was no locking mechanism at all.

Founder decision: the free QB was kept deliberately to build trust, so keep the first 15 answered
and tease the rest. All 30 questions remain listed; answers 16–30 became a ₹1,499 subscriber panel.
Withheld answers are **deleted from the bytes**, never CSS-hidden.

| | Before | After |
|---|---|---|
| Public share of paid content | 94.7% | **50.2%** |
| Withheld answers readable | all | **0 of 20 sampled** |
| Questions listed | 30 | 30 |

Also removed three internal sections from that public page: *QB1 Upgrade Notes v1.2*, *QB1 Roadmap
to v1.3*, *QB1 Roadmap to v1.4* — feature plans and a per-question editorial changelog that also
enumerated edits to answers now behind the paywall.

### 20.2 THE ROOT CAUSE: publish state lived on the command line — `2f38586`

The live public sample was telling customers **"Founder review copy — not published, not
indexable"**, showing `PRICE_TBD`, naming internal file paths, and carrying `noindex` — on the page
the entire Oral→Written funnel points at.

The cause was not a bad build. `--publish` is a **flag**, and `run_toolchain.py:194` calls
`build_sample.py` with no arguments, so **every routine rebuild silently reverted a published page
to a review copy.** Nothing failed and nothing warned. This was observed live mid-session: the
banner was removed, the toolchain was run, and it came back.

Publish state is a property of the artefact, so it now lives in the projection config
(`"publish": true`). A flagless rebuild — proven in the commit — keeps both pages published.
`--publish` survives as an override.

### 20.3 The public sample became a real marketing page

No review banner, no internal paths, `index, follow` instead of `noindex`, and the approved
**₹1,500** in three places. `PRICE_TBD` remains the sentinel and every price renders through one
helper, so a placeholder still cannot reach a customer by accident.

Added the five-mode explainer to the header (same copy as `solvedQP/index.html`) and a mid-page
conversion strip placed **after** a worked question, never before one — leading with the offer is
what makes a sample read as an advert. The strip is suppressed on a gated build, where the reader
already holds what it sells.

### 20.4 Gated full January paper for Oral subscribers

`meoclass1/oralnotes/solved-qp-january-2026-full.html` — inside the `ORAL_QB_NOTES` prefix, verified
against `routes.js#requiredEntitlementForPath` and live (`302 nosession`). All nine questions worked
in full, for customers who already bought the Oral product. Badged *"Included with your Oral
access"*, not "Free sample".

**MEASURED COST, printed by the build on every run: 18 questions across 11 other sittings** —
QP2404-Q7, QP2502-Q2, QP2506-Q7/Q8, QP2508-Q4, QP2509-Q3/Q6, QP2511-Q3, QP2512-Q1, QP2602-Q4,
QP2603-Q4, QP2604-Q3/Q4/Q6/Q7/Q8/Q9, QP2607-Q5. **QP2604 loses six of its nine questions**;
QP2607-Q5 is in the July paper the storefront exists to sell.

An earlier estimate of "February, March, April and July" **understated this**. The Founder decided
on the understated figure; the true one is now printed by the build and recorded in the config, and
the decision is reversible by deleting `sample/QP2601.full.sample.json` and rebuilding.

The guard is **not disabled**. `allow_family_members` requires a written reason AND a named
entitlement, refuses any output under `SQ/`, and prints every question it unlocks. `sample_check.py`
honours the identical exception and **verifies the gate claim against the output path** rather than
believing it — otherwise the build passes while the check fails forever, which is how a real guard
gets deleted by someone who does not know why it existed.

A gated page is forced to `noindex` whatever publish says: a crawler cannot read a page behind the
gate and would only surface the login bounce as content.

### 20.5 Verification

Toolchain ALL STAGES PASS · `sample_check` OK · 121 security tests green (38+32+22+29) ·
double-build byte-identical · no horizontal overflow at 1280 or 375 · every claim above re-checked
against the **live production URLs**, not just local files.

---

# QP2512 — December 2025 — production resumed, stopped at 3/9 with a safe checkpoint

**2026-08-12. Branch `pastpapers/qp2512-founder-review`, based on `7e51b97`.**

The Founder lifted the production pause and authorised QP2512 as the sole laptop object, with the
six 2024 papers reserved for desktop. The session verified git truth against the brief rather than
assuming it — `origin/main` was `7e51b97` as reported, eight untracked Founder-review files present
and left untouched — branched from the live product lineage, and read the governed protocol set.

**Baselines were derived, not carried.** `health_check.py` returned 252 questions / 117 solved /
135 unsolved across 28 papers, 13 solved, at 0 errors and 0 warnings; `solvedqp_check.py` and
`coverage_check.py` both passed. The private corpus was at `64977b8…`, unchanged, and QP2512 turned
out to have no demand on any of the three corpora at all, so the open provision-view decisions were
confirmed not to block this paper.

## The December boundary, and why it was harder than November's

`QP2511`'s anchor had left one sharp question for this paper: the 34th Assembly sat 24 November to
3 December 2025 and adopted at the close, so a December sitting can fall on either side of it.

The source copy was read in full — text layer plus both pages rendered at 150 dpi — and it prints
`DECEMBER 2025` with **no day-level date**. The governed fallback would have excluded the
`A.12xx(34)` family by default. Instead the session found a second date that settles it: an IMO
resolution carries a **document date** as well as an adoption date. `A 34/Res.1206` reads *"adopted
on 3 December 2025"* on a cover dated **5 December 2025**. The text was not circulated until then,
so no December sitting could have been examined against it. The exclusion became reasoned rather
than defaulted, and it holds without pinning the examination to a day.

## The finding nobody had predicted — three editions, not two

Pulling on that thread produced the session's most valuable result. The Assembly boundary lands on
the Procedures for Port State Control, and the corpus already contains `QP2606-Q2` (June 2026) built
**entirely on `A.1206(34)`** — the natural support for `QP2512-Q8`.

Reading operative paragraph 4 of both resolutions directly showed that `A.1206(34)` revokes
**`A.1185(33)`** of 6 December 2023, which had itself revoked `A.1155(32)` of 2021. **`A.1185(33)`
is the operative edition at a December 2025 sitting.** The intuitive re-anchoring — *"before the
2025 Procedures came the 2021 Procedures"* — skips an entire edition and reaches an instrument
revoked two years before the sitting, and nothing downstream would catch it. `A.1185(33)` was
downloaded and its detention and release chapters read, so Q8's primary source is banked.

## Donor adjudication beat the derived tier

The derived reuse map returns 3/9 for this paper. It traverses only host-derived edges, so it cannot
see two questions that set the same task and that no host ever linked. Each of Q3–Q8 was adjudicated
by reading printed stems: three carry real support the map does not show, two of them limb-level.
The reverse-hint sweep was run in both directions and recorded as a **negative** — QP2512 adds no
rows to the unadjudicated queue.

**QP2512 is a forward-pull paper, the structural inverse of QP2511.** That prediction was tested
rather than trusted, and it held in both directions: the post-sitting sweep returned nothing on
every donor, and the directionless class — an inherited internal `Q`-reference — fired on Q2, whose
donor closed its study guide with *"read this question against Q2, the propeller-curve question"*.
On QP2512, Q2 **is** that question. The paragraph was rewritten to keep its engineering point as a
cross-paper reading rather than renumbered.

## Q1 — the compression lesson, running backwards

The substantive adjudication of the session. December restores the qualifier *"certificates issued
**to a vessel**"* that November had deleted — and the November donor's own model answer says, in
terms, that the deletion is why the seafarer's medical certificate belonged in its answer. That
condition is not met here, so the crew limb left the answer layer and is taught in the study guide
instead. Because `answer_route` is the single spine, the cut was made there and the model answer,
decomposition, memory cue, recall numbers, major trap and retrieval cards were all brought into line
behind it. A session treating "same topic, one month apart" as licence to copy would have shipped a
substantial section the examiner did not ask for.

Q1's inherited cross-link was **re-pointed, not renumbered**: `QP2512 Q8` genuinely is the other
question on this paper turning on which Indian statute was in force.

## Where it stopped, and why

**3 of 9 — Q1, Q2 and Q9, each with a verification record.** Six remain and five are fresh authoring
from primary sources. The session stopped on capacity rather than on a blocker, at a clean boundary,
because the brief's own instruction was not to trade verification quality for a completion claim.

The canonical spec was **not touched** and still reads `Intake Complete`; no build of any kind was
run; QP2512 remains `PLANNED_SOON` on the delivery surface. A probe assembly of the three staged
objects with the six intake questions validates at **0 errors**. The research foundation for all six
remaining questions — donors, authority ladder, statute sections, the `A.1185(33)` chapter map — is
recorded in `staging/QP2512/CHECKPOINT.md` so the resumption does not re-derive any of it.

Two lessons were promoted, both primary-proven this session: the issue-date rule for an ambiguous
Assembly boundary, and the three-edition warning for re-issued instruments.

---

# QP2512 — December 2025 — RESUMED FROM 3/9 AND COMPLETED 9/9 — 2026-08-12

## Outcome

**COMPLETE. 9 of 9 authored, verified, assembled, built, swept and pushed for Founder review.**
The paper that the previous session left at a safe 3/9 checkpoint is finished. `staging/QP2512/`
is retired. No merge to `main`, no deployment.

## Branch / commits

`pastpapers/qp2512-founder-review`, base `7e51b97`, resumed from `d442af2` exactly as the checkpoint
recorded — local and remote heads both verified before any work began.

- `5835056` — Q8 and Q6 with their verification records
- `fd89578` — Q5, Q3, Q4 and Q7 with theirs; nine of nine staged
- `b5ec72c` — canonical assembly, both surface builds, staging retired

## Key findings

**The highest-risk adaptation was avoided by construction rather than by correction.** `QP2606-Q2`
was the natural support for Q8's port State control limbs and is built **entirely on the 2025
Procedures**, which had not been issued at this sitting. The intake note predicts an excluded
instrument spreading across **eight** surfaces of a question object. Rather than clone and then
hunt it out of eight places, Q8 was authored fresh, so the excluded edition could never enter.
`A.1185(33)` was re-obtained from the IMO resolutions CDN and read at source; its operative
paragraph 4 confirmed the revocation chain directly.

**A predicted numbering drift was checked and did not occur.** The anchor warned that chapter
numbering moves between editions of the Procedures and that equivalents must be located rather than
assumed. The right of appeal sits at **`2.3.11` in the 2023 edition as well** — so on that provision
the numbering *did* survive the revision. Established by reading, not inferred, and recorded
because the warning predicted it might not.

**Section 358(1) of the Merchant Shipping Act 1958 answers Q5's premise, and it is flag-neutral.**
Three of its five limbs say *"any ship"* and only two say *"Indian ship"*, so India's competence
over a casualty on a foreign ship in its port is **territorial, not flag-based**. The boundary then
reappears exactly where it should: `s.369(2)` sends the report to the foreign certificating
authority and `s.363(1)(b)` reaches a foreign certificate only on an Indian ship. India owns the
facts; the flag State owns the officer.

**GISIS is not in the Casualty Investigation Code.** The Code says only that the report goes *to the
Organization*. The GISIS Marine Casualties and Incidents module comes from
`MSC-MEPC.3/Circ.4/Rev.1`, a separate circular. Attributing it to the Code would have been a
citation error; the two are cited separately.

**There is no Standard A1.3 and no Guideline B1.3.** Established by searching the MLC text rather
than inferred from the pattern of the other three Title 1 Regulations. Regulation 1.3 stands alone
and defers to STCW. This is the point on Q6 most likely to be invented rather than checked.

**Two questions had no regulatory source for their main limbs and say so.** Maslow is attributed as
management literature by name and date; no instrument governs what a charterer may instruct. In both,
the genuinely regulatory limb was kept separable and verified, and §2.1's rule against manufacturing
a rule to satisfy a checkbox was applied deliberately. Q4 also records a limit it could not pass:
the corpus holds the STCW **amendment resolutions** but not the **Code tables**, so Table A-III/2 is
named and no competence wording is quoted.

## Corpus delta

| | before | after |
|---|---|---|
| Questions solved | 117 | **126** — the halfway point of 252 |
| Papers solved | 13 | **14** |
| Tier D over the unsolved set (derived) | 20 | **17** |
| `REVERSE_HINT_CANDIDATES.md` | 4 open rows | **4 open rows — byte-identical** |

QP2512 consumed three tier-D donors of its own and **unlocked none**. Unlike QP2511, its six
tier-C questions produced no new donor edge, because six of the nine were adjudicated as fresh or
limb-supported rather than family-linked. That is a real property of the paper, not a gap in the
derivation, and it is why the derived tier-D count fell by exactly three.

The reverse-hint queue being byte-identical confirms the anchor's recorded negative: **QP2512
contributes no new rows**, and the four open rows (`QP2402-Q3`, `QP2406-Q8`, `QP2408-Q3`,
`QP2410-Q1`) remain unadjudicated.

## QA

`ALL STAGES PASS`, and again with `--self-test`. `validate_spec` **0 errors**; the nine remaining
warnings are the deferred 450–650 word band, which fires on every question of every paper. **0
blocking** re-verification flags. `solvedqp_check`, `coverage_check` and both their self-tests pass.
Double-build **byte-identical across 91 generated artefacts**. Local UI review at 1280 and 375 on
all four pages: no overflow, no console errors, five modes with Answer default, search narrowing
correctly, no host-recurrence or provider leakage, review banner present on the review build and
absent from delivery.

**Two toolchain stages failed on the first run and both were honest consequences of a paper becoming
a product**: the reuse map was stale, and `ui_behaviour_test.cjs` had no fixture for QP2512 — by
design, since a page with no fixtures must fail rather than report a clean run having tested
nothing. The fixture's terms were chosen by probing the built page rather than guessed, and its
regulation probe is `A.1185(33)` deliberately: if that ever resolves to a different resolution
number, the paper has been re-anchored onto the wrong Procedures.

**Two validator warning classes were real defects and were fixed rather than accepted:** four
`freshness_risk` fields did not begin with a parseable risk word, and three flashcard answers ran
past 90 words, which the validator rightly calls being read rather than retrieved.

## Next action

**Founder review of `pastpapers/qp2512-founder-review`.** Nothing else is authorised. For
information only, the recomputed best remaining 2025 candidate is **QP2502, February 2025** (tier D
2/9, family reach 5, two temporal flags) — which confirms rather than overturns the previous
estimate. It is **not** started.

---

# QP2512 PUBLISHED · SOLVEDQP DERIVED LAYER BUILT · DESKTOP BATCH 2 ALLOCATED

**2026-08-12.** Laptop. Three pieces of work, in the order the Founder set them: allocate the next
desktop six *before* touching any product file, publish QP2512 safely, then build the manifest,
search and health system the Solved QP product had been missing.

## 1. Batch 2 was recomputed, not inherited

The carried-forward note recommended QP2502 at "tier D 2/9, family reach 5". Rather than trust it,
readiness was recomputed through `recurrence_model.py` under a **simulated built set that assumes
Batch 1 is complete** — 180 answers, not today's 126. QP2502 is now **3/9**: Batch 1's QP2402
creates a Q1 donor that did not exist when the note was written.

Two findings changed the allocation:

**QP2507's entire reach points at two papers.** It has the highest family reach in the corpus (8)
and zero donors, which is why Batch 1 correctly refused to start from it. All eight edges land
inside QP2501 and QP2503. Solved after them it is **8/9** — the largest single readiness conversion
available anywhere. It went into the batch with a hard ordering constraint rather than being held.

**The mid-2024 trio is not a block.** Batch 1's board expected QP2406/2407/2408 to be "the natural
second batch". They are not: all three finish at 1/9 with reach 0 in every scenario tested, because
their donors come from 2025 and 2026 and never from each other. That turned a three-paper Batch 3
into a two-paper one, and freed the sixth slot for QP2406 — the only zero-temporal-flag paper left.

The order was verified exhaustively: 18 of 54 questions arrive donor-ready, the maximum over all
720 permutations. It is also, for the first time, the calendar order — a coincidence of this donor
graph, not a rule.

## 2. QP2512 was reconciled, not merged

`main` had moved three commits ahead of the branch base. Twelve files were main-only; four were
touched by both sides. The one that mattered was the public sample: the branch's copy carried two
review markers, `main`'s carried none. The merge kept `main`'s bytes and took the branch's content
delta (13 → 14 sittings).

**The regression guard was not the merge.** It was rebuilding with `run_toolchain.py` and no
arguments — the exact invocation that silently un-published the page in the first place — and
confirming both samples stayed published. The measured unlock cost of the gated Oral full paper is
unchanged at 18 questions across 11 sittings; QP2512-Q1 was already in that set as an unsolved stem.

## 3. The derived layer, and the three false positives that shaped it

`solvedQP/solvedqp_content_index.json` is now the single generated inventory. The interesting work
was not building it but stopping it from being wrong every day.

**The paid-text guard convicted the product of leaking its own question paper.** A 60-character
scan for model-answer prose fired on the first build: QP2403-Q4's answer opens by restating its
printed stem word for word. The guard now subtracts the surface it is allowed to publish.

**The health check raised 18 leakage errors on an HTML comment.** Every delivered paper carries
`<!-- GATE SCRIPT STRIPPED FOR REVIEW COPY -->`. Comments are stripped before any prose scan.

**The temporal guard raised seven errors on correct content.** Scanning whole pages for later law
flags the Study Guide, which is *required* to tell the candidate the law has since changed. The
guard now reads answer panes only, ignores negated sentences ("had assent but had not commenced"),
and downgrades same-month collisions to REVIEW. The last false positive standing was QP2602's
"...in force 15 March 2026 — some five weeks after this paper was sat", which is a model sentence.

The self-test then failed one case, correctly: the future-law fixture was being injected after
`<body>`, outside any answer pane, so it proved nothing once the scoping landed. Moving it inside
an answer pane made it fail as intended.

## 4. The exposure that was confirmed and not fixed

Checking where the manifest could safely live established that the repository is public and
`solvedQP/QP2601.html` — 389 KB of paid answers — returns HTTP 200 unauthenticated from
`raw.githubusercontent.com`. The middleware gates the site, not the source. Pre-existing,
unchanged by this session, and recorded rather than quietly worked around.

---

# SESSION — 2026-08-12 — DESKTOP BATCH 1 REVIEW, INTEGRATION AND PUBLICATION

Laptop session. **No paper was authored.** Six desktop-authored 2024 papers were independently
reviewed, corrected where wrong, integrated into current `main` and published, one at a time.

Starting `main` `0d128a8` — 14 papers, 126 questions. Ending `main` `88aa4c7` — **20 papers, 180
questions**, 72 unsolved across 8 papers.

## 1. Why nothing was merged

All six branches were cut from `9c973596`, which predates main's manifest, search, health checker
and publish-state fix. Merging any of them would have dragged that stale tree back over newer
global work. Instead each paper's twelve owned files were extracted by path onto a fresh branch
from current `origin/main`.

That is only lossless if `main` never touched those paths, so it was checked before the first
extraction rather than assumed: `git diff 9c973596 origin/main -- <the twelve paths>` was empty for
all six papers. The two approaches therefore differed *only* in the globals, which is exactly the
part the laptop owns.

## 2. Order

Default order held — QP2401, QP2412, QP2402, QP2409, QP2411, QP2410 — and it turned out to be
dependency-correct rather than merely conventional. QP2402 carried the defect QP2411 referred, so
it had to land first. QP2410's Q8 donor is `QP2401-Q3`, and QP2401 was integrated first, so by the
time QP2410 was reviewed its donor was live and 9/9.

## 3. Per paper

| Paper | Commit | Outcome |
|---|---|---|
| QP2401 January 2024 | `28e419f` | Five declared traps each checked against candidate-facing text, not verification prose. 67 temporal candidates adjudicated. No defect |
| QP2412 December 2024 | `6eaa21a` | Intake's zero temporal flags disproved — four instruments moved inside 2024. MLC boundary lands *inside* the sitting month and Q6 is authored to survive either side. No defect |
| QP2402 February 2024 | `484a167` | **The referred regulation-21 defect, confirmed and fixed** — and found in Q5 and Q6 as well |
| QP2409 September 2024 | `4f622be` | §8 contamination list checked mechanically; every named anachronism present *only* as an express exclusion. No defect |
| QP2411 November 2024 | `6730727` | The branch that raised the referral. Its own chapter 4 reading is correct; referral closed and annotated as historical. No defect |
| QP2410 October 2024 | `88aa4c7` | MEPC 82 boundary design preserved, no exam day manufactured. Donor findings confirmed 6/9 tier D. No defect |

Two corrections were committed separately from any Batch 1 paper: `fd9e366` (QP2601-Q1, live) and
the Hong Kong Convention half of `88aa4c7` (QP2511-Q8 and QP2603-Q9, both live).

## 4. The regulation-21 investigation

`MEPC.328(76)` chapter 4 was read directly from the corpus copy rather than inferred: 21 Functional
requirements, 22 attained EEDI, 23 attained EEXI, 24 required EEDI, 25 required EEXI, 26 SEEMP,
27 fuel oil consumption data, 28 operational carbon intensity. Regulation 21 is not EEDI, so the
referral was correct. Classification: **wrong regulation number**, correct instrument, correct
temporal position, not donor contamination — `QP2402-Q3` was authored fresh and is itself the
forward donor `QP2411-Q3` draws from.

Three independent readings of that list now agree — QP2411's, QP2410's and this session's.

Generalising the referral into a corpus-wide scan is what found `QP2402-Q5`, `QP2402-Q6`,
`QP2601-Q1` and, separately, the Hong Kong Convention records. Applied only to the question named,
five of the six defects would have survived.

## 5. Hong Kong Convention

QP2410-Q4 read the Convention complete. Verified independently here:
`official-sources/HONGKONG_CONVENTION.pdf`, 47 pages, ARTICLE 17 verbatim and matching QP2410's
transcription. `QP2511-Q8` and `QP2603-Q9` both declared MIW held no copy — false — and both stated
application as "500 GT and above on international voyages". Article 3.3 excludes ships under 500 GT
*or* ships operating throughout their life only in flag-State waters; the exclusion is purely
domestic operation, not international voyaging. Both corrected, source state upgraded to PRIMARY.

**No temporal distinction was touched.** Not in force at October 2024; in force at November 2025
and March 2026. QP2511's contrast between the two is preserved verbatim.

## 6. Verification at each gate

Per paper: `validate_spec` 0 errors and 0 blocking, full toolchain ALL STAGES PASS, temporal sweep
adjudicated by value rather than by count, leak sweep over the shipped bytes, five-mode and
Answer-default check, double-build byte-identical, then merge, push, and live confirmation before
the next paper began.

Final state: toolchain and `--self-test` PASS, `solvedqp_check` 180 questions across 20 papers and
29 pages, search 13/13, coverage PASS, health PASS, corpus consumer 60/60, **security 121/121**,
double-build byte-identical across 265 artefacts.

## 7. Two process faults, both caught

A PowerShell here-string broke a commit message and left staged changes on `main` after a checkout.
Nothing was lost or pushed; the fix was to commit from a message file thereafter.

The QP2411 commit missed three derived files because it staged from a hand-written path list rather
than from what the build actually changed. Landed immediately in `3a19f02`. The final paper staged
from `git status`.

## 2026-08-12 — Batch 2 papers 1 and 2 integrated and published (laptop)

Desktop had already completed QP2501 (`fb2796f`, 16:18 IST) and QP2502 (`c04b402`, 20:27 IST) while a
laptop prompt was still describing QP2501 as possibly partial. The laptop's first session on this
correctly **stopped and authored nothing** — wrong machine, paper already complete, another session
demonstrably active 25 minutes earlier, and no QP2503/2504/2507/2406 branches on origin. The Founder
then re-scoped the laptop to review and integrate.

Both papers were integrated by **controlled path extraction**, not branch merge. Independent source
verification against the PDFs passed 9/9 on each; the apparent mismatches were the host's marketing
panels and recurrence table interleaved into the PDF text stream, which both specs correctly exclude.

Three laptop corrections in total: examiner-voice Understand openings on QP2501 Q4 and QP2502 Q4, and
QP2501 Q1/Q3 study notes telling a paying reader a claim was "flagged for confirmation before
publication" on a page that is published. QP2502 Q6 was checked specifically against the Batch 1
regulation-21-is-not-EEDI defect and is clean (regulations 22 and 24, primary-verified).

Two integration lessons recorded in CURRENT_STATUS §7e: a new paper's `solvedQP/QP####.html` arrives
**untracked** and must be named explicitly or the paid page ships as a 404; and REUSE MAP plus UI
BEHAVIOUR always fail on first build of a new paper, by design.

Published at `eb3a1c5` and `a1cc735`. **22 available papers, 198 published questions, 54 unsolved
across 6 papers.** Batch 2 is 2/6. QP2503 is next and belongs to the desktop.

---

## 2026-08-13 — QP2503 (March 2025) reviewed and published (laptop)

Desktop pushed `pastpapers/qp2503-founder-review` at `2ca4aa4` at 22:42 IST, thirteen minutes
before this session opened. The recorded coordination rule treats a push inside the last hour as
evidence the other machine is live, so the branch was **not** taken on trust: it was probed three
times across the session — at preflight, before commit and before merge — and `2ca4aa4` never
moved, nor did `origin/main` from `27f46bc`. The branch shape was also complete rather than
partial: one commit, paper HTML, anchor document, spec and nine verification records, and **no
global derived artefact**. Integrated by controlled path extraction onto a branch cut from current
`origin/main`; the desktop tip was left untouched.

**Source.** Both pages extracted and read back. All nine stems, every marks split and every printed
anomaly are verbatim, including the printed errors `a ship is classes by two classification
societies`, the lower-case `international Maritime Organization` and the lower-case l in `EEDl`.
Six answered questions at 16 marks total 96 against a printed `Total Marks - 100`; that is the
paper's own anomaly and is recorded, not corrected.

**Temporal.** The anchor's load-bearing claim was checked at source rather than accepted. MARPOL
Annex VI regulation 24 Table 1 prints two phase timetables split by ship type, and the corpus
canonical record `MARPOLVI_REG24.json` confirms it independently, down to naming the
transplantation of one onto the other as the unit's most transplantable error. At March 2025 Phase
2 has closed on both — 1 April 2022 for containerships and the larger gas carriers, 1 January 2025
for tankers, bulk carriers and the ro-ro classes, ten weeks before the paper. Q7's printed premise
is therefore false, and the desktop's handling is right: preserve the stem, deliver the
phase-independent design content in full, and state the position. Q9 was checked against the
Casualty Investigation Code independently — the very-serious-marine-casualty definition is correct,
`MSC.255(84)` via SOLAS XI-1/6 is correct, and the QP2512 GISIS trap is not repeated. The
Merchant Shipping Act, 2025 appears only inside trap warnings and never in a model answer.

**Understand — the first paper authored directly under §10.1.** Seven PASS, two MINOR, no FAIL on
the reconstruction test. Two corrections. Q5 carried `(section 2)` and `(section 3)`, which point
at answer-route steps but read as sections of the Marine Insurance Act, 1963 — on the single
question whose verification record deliberately refuses to assert any section beyond 19, 20 and 66.
The Understand column was manufacturing exactly the false statutory precision the Answer had been
built to avoid. A corpus sweep confirmed the pattern is unique to it: QP2502-Q5's section numbers
are genuine Admiralty Act citations and were left alone. Q3 addressed the examiner as "he" on the
paper's gender-equality question and substituted exam strategy for explanation; the same pronoun
defect existed in one other live paper, QP2508-Q8, and was corrected there too.

**Did the standard work?** Measurably on length and shape, not on citations. Understand median
words: QP2501 205, QP2502 272, QP2503 **196**, with the narrowest spread of the three and
single-thesis openings throughout. Rule-4 breaches — dates, regulation and article numbers — were
4/9, 6/9 and **5/9**, so direct authoring under the standard did not move that rule at all. Where
the numbers are load-bearing they are defensible; the rule's own rationale is still not being met,
and that is the open item for the next paper rather than a defect in this one.

**Two harness defects, both fixed.** The reuse-map self-test case 1 went red at the QA gate because
QP2503 supplied donors to the last five questions that satisfied its fixture condition — exactly
the five the anchor predicted it would unlock. The corpus had become more complete and the suite
reported it as a regression; it now synthesises the baseline instead of harvesting it. Separately,
two spec rewrites reformatted whole files because the corpus carries two JSON indent conventions.
Both are recorded as WORKFLOW_LESSONS §22 and §23.

**Also cleaned.** Nine live delivery pages told paying candidates a point was flagged "before
publication". The earlier report placed this in QP2508 and QP2602 only; the real reach was twelve
occurrences across eight specs. Corrected at canonical source by one uniform substitution, in its
own commit. The generated `Re-verify before publication` heading was left alone — it sits inside
`build_paper.py`'s `if not publish:` branch and never reaches a delivery page.

`solvedQP/QP2503.html` was untracked when generated, the third consecutive paper, and was named
explicitly. That gate is now written into `QA_AND_HANDOVER_PROTOCOL.md` §6 rather than left in
session history.

Integrated at `b4f2469`, cleanup at `0816f3d`, merged fast-forward and pushed. Production deploy
Ready; the live public sample is hash-identical to the local build. **23 available papers, 207
published questions, 45 unsolved across 5 papers.** Batch 2 is 3/6.

Readiness recomputed on the governed model: **QP2507 converts 0/9 → 8/9**, the largest conversion
in the corpus and exactly what the Batch 2 board predicted, with five of its eight donors coming
from QP2503. QP2504 5/9, QP2406/QP2407/QP2408 1/9 each, reach 0 for all five. Governed order still
puts QP2504 next. Nothing was started.


---

## 41. QP2504 (April 2025) - laptop review and publication, 2026-08-13

Session opened at `main` = `1d14118`, 23 papers / 207 questions. Desktop branch
`pastpapers/qp2504-founder-review` present at `aa0d8a6`, based on `333e814`, pushed
2026-08-13 00:14 IST. Tip re-fetched twice at preflight and unchanged, so the desktop was idle
on QP2504 and the review proceeded. Twelve files, every one paper-owned, **no global artefacts
in the branch** - the cleanest desktop handover of the batch. Integrated by path extraction onto
`integration/qp2504-laptop-review` cut from current `origin/main`; the desktop branch was not
merged and is retained as provenance.

**Source verification.** `APRIL 2025.pdf`, two pages, `Sr. No. EM - 2504`, three hours, total
marks 100, answer six of nine. All nine `text_verbatim` fields match the printed source exactly,
including every printed anomaly: Q1's missing sentence break, Q3's unlabelled limb (a), Q4's
comma splice, Q7's number disagreement, Q8's "What is P&I clubs?" and "filling a claim", and
Q9's "MSC. FAL.1/Circ.3" and "prone of cyber risks". Sub-part marks 8+8, 4+6+6, 8+8, 16, 8+8,
16, 8+8, 5+5+6 and an unmarked four-limb list, each summing to 16. No host branding reached any
shipped surface, and the host's five printed recurrence codes are recorded in the spec but are
not searchable in the built page - verified by the inverted fixture probe.

**Temporal anchor re-verified against primary sources, not accepted.** `MEPC.397(83)`,
`MEPC.398(83)` and `MEPC.400(83)` were each opened from the corpus and each prints **11 April
2025** on its face, fixing the MEPC 83 adoption day independently of any meeting calendar.
`MEPC.338(76)` Table 1 and the `MEPC.400(83)` replacement table were read verbatim and compared:
the 2023-2026 rows are identical, so **Z = 9 % governs the 2025 reporting year before and after
11 April 2025** and the Q6 answer is day-independent, exactly as section 2.2 of the anchor claims.
`MEPC.328(76)` operative paragraph 3 was read and states **1 November 2022**, confirming the
`TRUE_SOURCE_CORRECTION_REQUEST` at section 5; three canonical corpus records still carry
`2023-11-01` and were **not** modified.

**Four anchor-document defects corrected.** Section 2 was headed "THE TWO IN-MONTH BOUNDARIES"
while section 1 and section 2.4 establish three. Section 2.1 twice claimed "four MEPC 83
resolutions" where the corpus holds three - the conclusion is unaffected, three independent
instruments still fix the date. Section 3.1 described 1 May 2025 as "three weeks after this
sitting month closes" when it is **the day after**. Section 3's MLC and Hong Kong Convention rows
carried week counts that are day-dependent within April.

**The one material shipped defect.** Q6 stated on **seven** surfaces - Understand, model answer,
study notes, quick-revision cue, a retrieval card, the question delta and the temporal-review
record - that the 2024 attained CII "fell due for reporting by 31 March 2025, three weeks before
this paper". Three weeks after 31 March is 21 April; the source copy prints no day, and the true
gap runs from one day to four weeks. This breaches the paper's own governing rule at anchor
section 1. All seven were rewritten to "in the month immediately before...". The four *other*
occurrences of "three weeks" in Q6 are a hypothetical worked example - a ship at anchor for three
weeks, showing that AER rewards distance - and were deliberately left untouched; a blind grep
would have destroyed them.

**Corpus-wide propagation.** Ten papers carry week- or day-granularity sitting-relative claims.
Adjudicated individually rather than swept: eight are cosmetic, describing events comfortably
outside their sitting month where the substance is day-independent. **One was material and
live** - `QP2510-Q6` described the electronic Ballast Water Record Book amendments as taking
effect "three weeks before this examination" when 1 October 2025 is the first day of QP2510's
own sitting month, misclassifying an in-month boundary as a settled pre-sitting fact, in a
shipped Study Guide paragraph. Fixed on all three of its surfaces. Recorded as **known trap 17**
with an explicit instruction not to grep the phrase bare.

**Understand audit.** 5 PASS (Q2, Q3, Q7, Q8, Q9), 4 MINOR (Q1, Q4, Q5, Q6), 0 FAIL; every
MINOR corrected. Rule 4 was applied as judgement, not purge: Q1 lost three regulation numbers,
Q4 one, Q5 two section numbers and four colonial statute years. **Understand now carries zero
citations across all nine questions** - the first Batch 2 paper to reach that, and the answer to
the QP2503 finding that section 10.1 had improved quality without moving rule 4. Four dates were
kept because the concept dies without them: SOLAS **1974** and the **2017** Act are instrument
names, the CII **2019** reference line is the mechanism, and Q9's **4 April 2025** is the whole
point of its section.

**Content.** Q1 was re-verified line by line against the held SOLAS 2024 consolidated edition -
regulation 1.1, 1.3, 2.2, 2.3, 3.1, the three-rung retrofit ladder at 3.2/3.3/3.4 and 3.5 are all
exact. Q5's section 13 quotation is verbatim against the official India Code PDF, and the answer
correctly states that the Act **delegates** assessor qualifications to rules rather than
enumerating them - the obvious place to invent a statutory list, and it does not. Q2 draws the
IMO/MOU boundary expressly rather than inventing Detention Review Panel procedure the corpus
cannot support. No defect was found in any of the nine model answers.

**Validation and QA.** `validate_spec` 0 errors, 0 blocking on QP2504 and on QP2510 after its
fix. Full toolchain **ALL STAGES PASS**. Two failures were fixed on the way, both anticipated:
the UI fixture had no `QP2504` entry, and the reuse map was stale. UI behaviour 62/62 after the
fixture was written. Reuse self-test PASS including the synthesised-baseline case, which now
names `QP2504-Q8`. Security 121 tests across four suites, 0 failures. Corpus consumer 60 checks,
0 failures. Coverage, search 13/13, health and known-traps all pass. **Double-build
byte-identical across eleven generated artefacts.**

**Delivery-page gate.** `solvedQP/QP2504.html` was generated **untracked**, the same failure that
hit QP2501, QP2502 and QP2503. Caught by the Part 15 gate and staged explicitly. It is not
gitignored - it is simply a new path, and `git add -u` never sees one.

**Desktop coordination.** `pastpapers/qp2507-founder-review` **appeared during this session**, at
`57b940a`, 02:46 IST, carrying only `QP2507_TEMPORAL_AND_DONOR_ANCHOR.md` and a staging
checkpoint - no questions built. QP2507 is **ACTIVE, not complete**, and was not touched.
`QP2406`, `QP2407` and `QP2408` remain absent.

**Published:** 24 available papers, 216 published questions, 36 unsolved across 4 papers.

---

## 42. QP2507 (July 2025) - laptop review and publication, 2026-08-13

**Result: QP2507 REVIEWED AND LIVE. The 2025 examination year is complete.**
`main` `391e517` -> `0a6f685`. Product 24/216 -> **25 papers / 225 questions**, 3 unsolved papers.

### Ownership

Desktop pushed `pastpapers/qp2507-founder-review` to `3f37176` at 03:58 IST, nineteen minutes
before this session opened. Because a still-moving branch must not be raced, the tip was probed
three times over roughly twenty minutes and did not move, and the commit subject - *"author Q1-Q9,
promote the July 2025 paper to 9/9"* - matches the terminal handover pattern of QP2501, QP2502,
QP2503 and QP2504 exactly. Footprint was 12 paper-owned files with no global derived artefacts.
Integration proceeded on that evidence, by path extraction onto current `main`; the branch was
retained unmerged.

### Source

Independently re-verified against the printed copy: serial `EM - 2507`, 3 pages, Q1-Q9, 16 marks
each, every limb and mark split confirmed. Six of nine stems match their donor character-for-
character. Printed errors are preserved rather than corrected - *"is classes by"* in Q8(b),
lower-case *"international Maritime Organization"* in Q6(b), the colon after Q3(a) - and the
printed `Total Marks - 100` against six answers of 16 is reproduced with a note.

A mechanical verbatim diff flagged Q3 as a mismatch. It was not: the source copy interrupts Q3
between limbs (b) and (c) with a marketing panel and a page break, and the spec correctly stitches
across it while excluding the panel. **The host's `"- - PROVIOUSLY ASKED - - -"` block, which
reprints the March 2025 wording under Q9, appears in two authoring fields and on no surface.**

### Temporal

No boundary this paper engages moves inside July 2025 - provable rather than assumed, with the two
nearest boundaries four days before and one day after the month. **The Hong Kong Convention, which
the work order named as the highest-risk donor contamination on this paper, is not engaged by any
of the nine questions**, so no pre-EIF donor wording existed to correct; the sweep returns zero
against a control that fires. One real re-anchoring was made by desktop and confirmed here: the
January donor's *"FuelEU Maritime began to apply in the sitting month itself"*.

Donors: 8/9 as the board predicted, three from QP2501 and five from QP2503, **every one backward**.
Family reach came out 0 against a predicted 8, for the same reason as QP2504 - the papers that emit
reach are the papers the board required solved first.

### Corrections - 14

Rule 4 took Understand to **zero regulatory citations on all nine questions**, the first Batch 2
paper to measure zero. The audit also established that the citations in the knowledge map are
correct on every paper and are not in scope - see `WORKFLOW_LESSONS.md` L-B2-1. Q5's `(section 2)`
and `(section 3)` were the sharpest find: they point at answer sections but sit in a paragraph
about the Marine Insurance Act whose `regulations` list cites sections 19, 20 and 66.

Internal vocabulary removed from candidate-facing prose; the corpus-provenance sentences were
**reported, not rewritten**, as a corpus-wide class needing a Founder decision - `CURRENT_STATUS.md`
§7i.

### Two process faults

**The delivery page was untracked for the fifth consecutive paper** and was staged explicitly.

**Two True Source referrals had never been raised where they said they were.** Both anchors state
the defect was raised as a `TRUE_SOURCE_CORRECTION_REQUEST`; the register held only TSCR-1 and
TSCR-2. Transcribed as **TSCR-3** (`MEPC.328(76)` entry into force) and **TSCR-4** (the corpus
presenting the revoked `MEPC.376(80)` as current). No corpus file was touched.

### Verification

`validate_spec` 0 errors / 0 blocking; known traps 205 checks 0 failures; recurrence 0 failures;
`run_toolchain` and `--self-test` ALL STAGES PASS; double build byte-identical across 65 artefacts;
UI behaviour 66 passed / 0 failed on a new fixture whose probes were derived from the built page and
re-tested for uniqueness; delivery surface clean with every detector controlled against the review
build; desktop and mobile reviewed at 1280 and 375 with no overflow and no console errors.

### Next

**QP2406 is the last paper of Batch 2 and has not been started.** No branch exists on `origin` for
QP2406, QP2407 or QP2408. All three remain at **1/9** donor-readiness - QP2507 created no new
donors, which its own anchor predicted.

---

# §37 — QP2406 (June 2024) laptop review and publication — 2026-08-13

## Outcome

**QP2406 REVIEWED AND LIVE. Batch 2 closed at 6/6.** Product moved from 25 papers / 225 questions
to **26 papers / 234 questions**. Eighteen unsolved questions remain across two unsolved papers,
QP2407 and QP2408, both 2024 sittings.

## Branch / commits

Starting `main` `2d9435d`. Desktop branch `pastpapers/qp2406-founder-review` at `49e31e2`, based on
`333e814`, pushed 07:38 IST, stable across two fetches before any work began. Twelve files, all
paper-owned. Integrated by path extraction on `integration/qp2406-laptop-review` cut from current
`main`; the desktop branch was never merged and is retained. Published at `c368d5d`.

## Key findings

**The brief's account of the remote was wrong and preflight caught it.** It stated the desktop had
completed QP2406, QP2407 and QP2408. Only the QP2406 branch exists; QP2407 and QP2408 are still
`Intake Complete` at 0/9 with no branch on `origin`.

**Five corrections.** (1) The source host was named by brand in all nine verification records while
the same spec declares host identity is recorded outside this public repository — a prose record
contradicting a structured declaration inside one object, unique to this paper in twenty-five.
(2) The anchor header claimed eight of nine donor relations where its own table lists seven.
(3) Production jargon in six candidate-facing study-note blocks — the register-only subset of §7i,
fixed; the provenance-claim subset left untouched and still Founder-blocked. (4) Rule 4: `Article
14` and `the 2014 amendments` removed from `understand_first`; `Merchant Shipping Act, 1958` kept,
because the year is part of the statute's name. (5) Trap 17, second occurrence — a "two weeks"
distance from a sitting printed with no day.

**The donor claims were accurate.** All three tier D relations were re-derived rather than trusted:
`Q7 ← QP2504-Q8` exact nil delta, `Q8 ← QP2601-Q3` presentational delta only, `Q9 ← QP2411-Q9`
substantive enlarging delta. Six of the seven relations travel backward; only `QP2403-Q9` pre-dates
the sitting. Adding the earliest paper in the set re-anchored `QP2601`'s recurrence note to June
2024 Q8 — a derived change on a live page, produced by the toolchain.

**Source verification.** Three pages, serial `EM – 2406`, nine questions, every limb, 16 marks each.
Printed errors preserved. The printed 96-versus-100 marks anomaly recorded, not corrected.

## Corpus delta

252 in corpus · 234 solved · 18 unsolved. `QP2406` Planned soon → Available. `2024_2026_RECURRENCE_
AND_REUSE_MAP.md`, `REVERSE_HINT_CANDIDATES.md`, `SOURCE_INVENTORY.md`, both content indexes, the
year and topic sheets, the solvedQP home and five sibling papers all regenerated. A QP2406 fixture
was added to `ui_behaviour_test.cjs`, including the inverted host-recurrence leak probe.

## QA

`validate_spec` 0 errors / 0 blocking · `known_traps_check` 205 checks / 0 failures · all toolchain
stages pass with the five positive-control stages firing · **120 generated files byte-identical
across a double build** · UI clean at 1280 and 375 · live verified against a public control, the
paywall being path-agnostic. `solvedQP/QP2406.html` untracked for the sixth consecutive paper and
staged by explicit path.

## Next action

**Do not start QP2407 or QP2408 on the laptop.** Both are desktop-authored papers and neither has
been started. Recommended desktop order is **QP2407 then QP2408**. See the Batch 3 handover.
