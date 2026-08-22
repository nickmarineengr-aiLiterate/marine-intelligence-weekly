# Historical Written QI 2010–2020 — adoption adjudication

**Decision: `ADOPT_SOURCE_LAYER_ONLY`.** Taken 2026-08-23 by the Laptop,
independently of the Desktop research session that produced the evidence.

| | |
|---|---|
| Evidence reviewed | `origin/research/historical-written-qi-2010-2020` @ `2b22cd4` |
| Merged into main | **No**, and not proposed |
| Governed artefact created | `docs/study/historical_source_layer.json` (115 records) |
| Research records left unadopted | 1,026 occurrences, 1,873 modern join pairs, 83 family joins, 328 currentness flags |
| Roadmap weights changed | **No** |
| Public claim changed | **No** |
| Marketing | **Not activated** |

> Desktop recovered the evidence. This document decides what it is allowed to
> mean.

---

## 1. What was verified, independently

Every headline claim was recomputed from the artefacts rather than read from
the research report, and the modern-corpus checks were redone with a
token-overlap measure written here — not with the phase3b classifier that
produced the verdicts, so a fault in that classifier could not hide inside its
own output.

| Claim | Verdict |
|---|---|
| 115 archived papers, all VERIFIED, 0 fetch failures | **CONFIRMED** — 115 records, 115 distinct sha256, 115 archive URLs |
| 1,026 occurrences, 256 distinct source entities | **CONFIRMED** |
| Every date `MONTH_YEAR_CLAIMED_BY_SECONDARY_SOURCE`, zero `MONTH_YEAR_CERTAIN` | **CONFIRMED** — 1,026 / 1,026 |
| Source class `SECONDARY_REPOSITORY_VIA_ARCHIVE` throughout | **CONFIRMED** |
| 883 of 895 source-asserted modern links verify against MIW text | **CONFIRMED** — all 883 resolve, independent overlap min 0.72, median 1.00, none below 0.45 |
| 649 limb labels, 171 multi-limb stems | **PARTLY** — 649 labels confirmed; 171 stems carry *at least one* limb marker, of which **164** are genuinely multi-limb |
| 15 DGS result lists corroborating 2013-08 → 2015-09 | **OVERSTATED** — see §4 |
| Acquisition compliance: no login, no paywall, 403 not pressed, answers never touched | **CONFIRMED**, and exemplary |

The acquisition discipline is the strongest part of this work. The live-site
403 was recorded as a refusal rather than worked around, the answer paywall
was never touched, and every page carries a machine-independent re-obtain
recipe.

---

## 2. The three claims are not one claim

| | Claim | Status |
|---|---|---|
| **A** | This wording existed on the archived source page | **CORROBORATED** |
| **B** | This question belonged to the YYYY-MM sitting | **CLAIMED BY SECONDARY SOURCE** |
| **C** | DG Shipping officially administered this exact question in that sitting | **NOT ESTABLISHED** |

**A is stronger than Desktop claimed, on evidence Desktop did not use.** The
phase3b research branch holds nine items extracted from the Directorate's own
*Question Bank MEO CL-I*. Cross-checking them against the 263 distinct archived
wordings: **eight of the nine match**, five of them exactly (BANK-039,
BANK-054, BANK-072, BANK-085, BANK-160 at 1.00; BANK-135 at 0.93, BANK-015 at
0.92, BANK-018 at 0.71). Only BANK-105 has no counterpart. This is *official*
corroboration that the wording DieselShip publishes is the wording the
Directorate publishes. It is much better than "a commercial recall site said
so."

**It corroborates nothing about dates.** The official bank is undated
throughout — `date_confidence: NONE` — so it cannot move claim B or C by one
inch.

**B carries a limitation the research report understates.** Its §3 says
occurrences "preserve the per-sitting raw stem and the entity id separately."
They do not. The 1,026 occurrence records carry only **263 distinct
`raw_wording` values**; 250 of the 256 entities have exactly one wording
replicated across every sitting they are asserted in. The `Qn` prefix inside
`raw_wording` matches `printed_qno` in 1,026 of 1,026 cases and differs from
that occurrence's own `page_ordinal` in 628. So `raw_wording` is the source
**entity's** canonical text, not the text as printed in that sitting.

What *is* page-evidenced per sitting is **membership and position**: the
archived set page for a given month lists that entity at that ordinal. That is
a real, hashed, per-sitting observation, and it is what the adopted source
layer records.

---

## 3. Why the recurrence joins were not adopted

The joins are sound evidence attached to an inflated count. They are counted
per **occurrence**, which restates a single entity-level decision once for
every sitting the source asserts:

| Reported | Distinct decisions |
|---|---|
| 83 family joins | **18** entity–family pairs |
| 12 `HIGH_CONFIDENCE_SAME_FAMILY` | **2** entities — 11 of the 12 are the same question |
| 22 PROBABLE | **5** entity–family pairs |
| 49 POSSIBLE | **11** entity–family pairs |
| 1,873 modern join pairs | **287** entity–modern pairs |
| 559 occurrences matching a modern question | **109** entities of 256 |
| 895 asserted-link checks | **147** entity–sitting pairs |
| 883 verified | **74** distinct entities |

Every high-confidence family join was read in full. They are not wrong —
FAMILY-EM-0006 really is the same question, and it really does recur — but
"12 high-confidence joins" describes **two questions**, and adopting the
occurrence-level count would push an eleven-fold overstatement of one
question's weight straight into a recurrence model.

One further deflation matters for how the corroboration reads: of the 883
verified modern links, **728 resolve into MIW's wording-only 2021–2023 band**
and only 155 into the solved 2023–2026 corpus. Of the 241 modern questions
that gain ancestry, **100 are in the solved band**.

The joins therefore stay `RESEARCH_ONLY` and are re-adjudicated at **entity
granularity** before any of them may move a number.

---

## 4. What the official result lists actually prove

Desktop reports "15 DGS result lists proving sittings occurred 2013-08 →
2015-09". Reading `PHASE3B_SOURCE_INVENTORY.json` on the phase3b branch:

- There are **17**, not 15.
- All 17 are `retrieval_status: DISCOVERED` with **`sha256: null`** — they were
  identified by URL and **never retrieved or hashed**. In-repo they are
  references, not held evidence.
- Four carry no sitting month at all (two 2017 `MEOCLIAPRIL` uploads, two 2018
  `MEOCLI-II` uploads), leaving 13 dated ones.
- Those 13 name **seven distinct sitting months** — 2013-08, 2013-10, 2013-11,
  2014-01, 2014-04, 2015-01, 2015-09. "2013-08 → 2015-09" is the *envelope*,
  not the coverage: 7 of 26 months inside it.
- They are result lists. Even fully retrieved, they would prove a sitting
  happened and would **date no question**.

They also live on an unmerged research branch, so nothing on `main` currently
depends on them — which is correct, and should stay that way until they are
actually retrieved and hashed.

---

## 5. Month gaps — absence of a page is not absence of an exam

17 months in 2010–2020 have no paper. They are three different things and the
adopted layer records them as three:

| Months | Classification | No-sitting evidence |
|---|---|---|
| May, 2010–2019 (10) | `NO_SOURCE_PAGE` | **INFERRED, NOT EVIDENCED** |
| 2020-04 … 2020-09 (6) | `NO_SOURCE_PAGE` | **EXTERNALLY PLAUSIBLE, NOT EVIDENCED** |
| 2010-09 (1) | `NO_ARCHIVE_CAPTURE` | Source page known to exist |

The research report's headline — "no May sitting exists for any year
2010–2019" — is a no-exam claim resting on one secondary index's silence. The
underlying artefact is more careful. The adopted layer keeps the careful
version: a missing page is a missing page until something says otherwise.
Only 2010-09 is a pure acquisition gap.

---

## 6. Currentness — the rule is fail-safe but under-inclusive

The rule is "any stem citing a regulatory instrument requires currentness
review; everything else is UNKNOWN". Directionally right: it only flags, it
fixes nothing, and unflagged defaults to UNKNOWN rather than CURRENT, so it
fails safe in both directions. Keep it.

It misses the risk that actually bites. The flags key off instrument names, so
**time-relative language is invisible to them**. 42 occurrences across 13
entities say "ongoing developments", "the latest", "new generation",
"the latest emission control requirements" — and carry no flag.

Among them is `FAMILY-EM-0006`: *"What are the ongoing developments at IMO
with respect to the technical and operational measures … for combating
greenhouse gas emissions"* — claimed from 2010 through 2018, and the single
most confidently joined question in the whole research layer. A 2010 answer
and a 2026 answer to that stem describe different regulatory worlds. It is the
most currentness-dangerous item in the set and the rule does not see it.

**Required before any historical stem informs answer work:** add a
time-relative-language trigger alongside the instrument trigger, and never
read "unflagged" as "current". (328 flags cover 327 occurrences — one duplicate
record — over 88 of 256 entities.)

---

## 7. Date policy — internal and public thresholds differ, on purpose

**Internal: PERMITTED.** `MONTH_YEAR_CLAIMED_BY_SECONDARY_SOURCE` is
sufficient for recurrence, dormancy and trend analysis. The source's modern
claims verify against MIW's own canonical text at a rate that earns provisional
trust, and being wrong about a month costs an internal model a study-priority
nudge.

**Public: FORBIDDEN, indefinitely on the present evidence.** A public dated
claim costs credibility when it is wrong, and no official document dates any
2010–2020 sitting. This is not a "not yet" pending more coverage: **more
coverage cannot fix it**, because coverage is not the missing thing.

That distinction is now enforced in code rather than remembered.
`evidence_model.py` gains a `date_certainty` axis independent of `QI_STATUS`,
and `public_evidence_claim()` consults `date_certainty_gate()`, which requires
`OFFICIAL_DATED`. **A historical layer may be `COMPLETE` and still be barred.**

This closed a live trap. Before the change, promoting the socket to
`VALIDATED_RANGE` would have made the public roadmap sentence say
"validated historical papers from 2010 to 2020" **automatically** — and with
115 of 132 months held and every page hashed, a future session reading only the
coverage number would have had every reason to promote it.

`"since 2010"`, `"asked since 2010"`, `"papers from 2010"` and
`"16 years of question intelligence"` are now named in
`forbidden_until_validated` and gated by the validator.

**What would later be safe**, if a Founder chooses to say anything at all:
a qualified, undated statement of the kind *"recurrence patterns cross-checked
against archived question sets going back to 2010, dated by a secondary
repository"* — which claims the archive and discloses the date provenance in
the same breath. That is a Founder decision, not a build decision, and it is
not taken here.

---

## 8. What was adopted

`docs/study/historical_source_layer.json` — **115 governed records**, built by
`tools/study/ingest_historical_source_layer.py` from the pinned research
commit, carrying **provenance only**: source id, set id, claimed sitting month,
date certainty, source class, original and archive URLs, archive timestamp,
sha256, byte count, stem counts, completeness, verification status.

It contains **no question text, no answers, no occurrences and no joins**, and
the ingest tool refuses to build an artefact that does. It adds **zero**
questions to any MIW count.

The QI coverage socket stays `NOT_STARTED`. Adopting a source layer is not
ingesting questions, and saying `PARTIAL` would put a number on a layer that
has none.

---

## 9. Evidence horizon after — four bands, not one

Never flatten these into "a 2010–2026 verified official corpus":

| Band | What it is |
|---|---|
| 2023-01 … 2026-08 | **40 solved papers, 360 questions.** Governed, officially sourced. |
| 2021 … 2023 | **30 papers, 270 questions, wording only.** Printed wording and rubric; no answers. |
| 2010 … 2020 | **Source layer only.** 115 archived pages; wording corroborated, dates secondary-claimed; **no question ingested**. |
| 2006 … 2009 | **Absent.** Sets exist on the source index; deliberately unacquired. |
| 1999 … 2005 | Archive context. Different subject family. Not ingested — and **not to be started** before this policy settles. |

**Long-term recurrence available: PARTIAL.** The source layer establishes that
a 2010–2020 series exists and is re-obtainable. It does not yet carry the
questions, so no recurrence number spans the window today.

---

## 10. Roadmap preview — computed, not applied

Nothing was applied. Study order is unchanged and **no roadmap weight moved**.

What the research layer *would* offer once entity-level ingestion is
adjudicated: 109 of 256 historical entities join MIW's modern corpus at
`SAME_CORE_ASK` or better, giving 241 modern questions dated-claim ancestry
(100 of them in the solved band). That is enough to distinguish persistent
topics from recently risen ones — the signal MIW currently lacks entirely.

It is also enough to distort the model if adopted at occurrence granularity,
which is exactly why it was not. Founder approval must precede any new
priority weighting.

---

## 11. Next steps, in order

1. **Re-adjudicate the joins at entity granularity** — 287 entity–modern pairs
   and 18 entity–family pairs, not 1,873 and 83.
2. **Retrieve and hash the 17 DGS result lists.** They are currently
   references, not evidence. Retrieved, they would corroborate 7 sitting
   months — worth having, and still dating no question.
3. **Add a time-relative-language currentness trigger** before any historical
   stem informs answer work.
4. **Then**, and only then, design the occurrence ingest.
5. **Do not start 1999–2005.** Pre-2010 stays archive context until this policy
   settles.

Nothing above changes what Nixon studies. `D01 → D03 → D02` stands.
