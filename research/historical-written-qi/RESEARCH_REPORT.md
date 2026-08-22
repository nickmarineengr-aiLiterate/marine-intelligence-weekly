# Historical Written QI — 2010–2020 recovery

**RESEARCH_ONLY. `current_as_of: 2026-08-22/23` (Desktop session). Nothing here is
governed, nothing touches production, and no roadmap weight moves because of it.**

Branch: `research/historical-written-qi-2010-2020` (off `origin/main` @ `836f447`).
Brief executed: `docs/study/HISTORICAL_WRITTEN_QI_RECOVERY_BRIEF.md` (found on
`main`, prepared by the Laptop 2026-08-22).

---

## 1. Headline

**The 2010–2020 window has fallen.** Question stems for **115 of 132 months**
(every sitting that appears to have existed) are recovered, hashed and extracted:
**1,026 occurrence records** resolving to **256 distinct question entities**.

The route nobody had tried: DieselShip's paywall gates **answers**, not
questions. Its `?qcat=class-1-exam-qa` set pages render every stem publicly by
design, and the Internet Archive captured those pages en masse in 2023–2026.
Phase 2 had correctly recorded the plain set pages as metadata-only and the
subscription as untouchable; the category-filtered variants were the gap.

The 17 "missing" months are not losses: no May sitting exists for any year
2010–2019 on the source's own index (the ~11-sittings/year calendar), 2020
Apr–Sep is the COVID suspension, and 2010-SEP alone exists but has no archived
capture.

## 2. What was verified, not inherited

- **Every Laptop finding in the brief checked out**: 40/360 solved, 30/270
  wording-only, 1999–2005 archive research-only, 2006–2020 absent from repo
  state, 185-item bank held, QI-v2 prototypes on the unmerged phase3b branch.
- The "new" official lead this session (DGS `MEOCLASS-IWRITTENEXAMQUESTIONS.pdf`,
  uploaded 2018-02-12, on Wayback) is **byte-identical** (sha256 `0E0D6BC7…`) to
  the already-held 185-item bank — an alias URL, not new evidence.
- All acquisition rules held: no login, no paywall interaction, no CAPTCHA, no
  UA spoofing. The live-site 2013–2020 metadata fetch met HTTP 403 and was
  **not pressed**; the manifest records the refusal
  (`manifests/dieselship_2013_2020_sets.json`, 0/83, kept as a compliance record).

## 3. Provenance and date certainty — the honest limits

- **Source class: `SECONDARY_REPOSITORY_VIA_ARCHIVE`.** DieselShip is a
  commercial candidate-recall repository. These are not official papers.
- **Zero papers reach `MONTH_YEAR_CERTAIN`.** Every sitting date is
  `MONTH_YEAR_CLAIMED_BY_SECONDARY_SOURCE`. Official corroboration exists only
  as the 15 DGS result lists proving sittings occurred 2013-08 → 2015-09 —
  they date no question.
- **Indirect validation is strong**: of 895 DieselShip-asserted recurrence links
  into 2021+ sittings MIW holds, **883 verified against MIW's own canonical
  text** (723 EXACT_REPEAT / 124 NEAR_VERBATIM / 36 SAME_CORE_ASK, 12
  unmatched, 0 pointing at a sitting MIW does not hold). A source whose modern
  claims verify at 98.7% earns provisional trust for its historical claims —
  provisional, never `MONTH_YEAR_CERTAIN`.
- **Completeness per sitting is unknown** (8–10 stems/set vs the modern
  9-question format). Recorded per paper as
  `SOURCE_COMPLETE_PAPER_COMPLETENESS_UNKNOWN`.
- **Answers are not recoverable** and were never touched. MIW writes its own.
- **The 256-entity structure is source-asserted.** DieselShip stores one
  question entity and lists its appearances (`also_asked_in`). Its merges could
  collapse near-variants; that is why occurrences preserve the per-sitting raw
  stem and the entity id separately, and why family joins go through the
  unmodified phase3b classifier rather than trusting the entity graph.
- **`printed_qno` is the entity's stored heading, not necessarily this
  sitting's paper position.** The in-paper position for a given sitting is the
  set's own ref inside `source_asserted_recurrences` (e.g. `2014/MAR/02`).

## 4. Recurrence findings (candidates, not adjudications)

- **559 of 1,026 historical occurrences (54%) match a 2021–2026 MIW question**
  at SAME_CORE_ASK or better; **241 of MIW's 630 modern questions** now have
  dated-claim ancestry back into 2010–2020. The longitudinal series
  2010→2026 is now materially joinable.
- **83 family-join candidates** against the 9 QI-v2 families
  (12 HIGH_CONFIDENCE, 22 PROBABLE, 49 POSSIBLE). Family ids are used, never
  duplicated; joins are candidates for adjudication, not merges.
- Classifier: `qi_similarity.classify` from phase3b, **unmodified** — lexical
  containment proposes, demand/actor/polarity/number features demote.
- **328 occurrences flagged `REQUIRES_CURRENTNESS_REVIEW`** (instrument
  mentions: MARPOL/sulphur-era, M.S. Act, ISM/ISPS, PSC, survey regimes …).
  Flags only; nothing is "fixed". Recurrence is not currentness.

## 5. Artefacts

All under `research/historical-written-qi/`:

| File | Holds |
|---|---|
| `SOURCE_MAP_2010_2020.json` | six routes, status and evidence per route, per-year map |
| `PAPER_INVENTORY_2010_2020.json` | 115 papers: archive URL + sha256 recipe, counts, verification |
| `DATE_CERTAINTY.json` | vocabulary + per-paper certainty |
| `EXTRACTED_OCCURRENCES.json` | 1,026 raw+normalized stems, limbs, entity ids, source-asserted recurrences |
| `RECURRENCE_CANDIDATES.json` | family joins, modern-corpus joins, asserted-link verification |
| `CURRENTNESS_FLAGS.json` | 328 flags, everything else UNKNOWN |
| `YEAR_COVERAGE_MATRIX.json` | the year-by-year progress tracker |
| `GAP_REPORT.json` | Mays, COVID-2020, 2010-SEP, completeness, dating limits |

Raw HTML (115 pages) is git-ignored at
`D:\MIW-Historical-QP-Intake\wayback-dieselship\` with
`manifests/wayback_dieselship_class1_2010_2020.json`; the committed
archive-URL + sha256 pairs are the machine-independent re-obtain recipe —
the same doctrine as `PHASE3B_SOURCE_INVENTORY.json`.

## 6. Recommended first ingestion batch

**2016–2020 (49 sets, ~449 occurrences).** Uniform verification quality across
the window makes recency the tiebreaker: these years join directly onto the
2021+ canonical series, carry the least superseded-regime load, and give the
medium-term (5–10 y) window its evidence first. 2010–2015 follows as batch 2.

## 7. What this session did NOT do

No production mapping, no study-order change, no D01–D10 edit, no roadmap
weights, no public-page claims, no answer content, no socket population
(`written_evidence_horizon.json` untouched), no main push. The
`historical_written_qi` socket stays `NOT_STARTED` until the Laptop adjudicates
this evidence and ingests it through the governed chain.

## 8. Handoff to Laptop

Each occurrence carries: source id, source class, paper identity, date
certainty, page ordinal, entity id, printed qno, raw wording, normalized
wording, limbs, source-asserted recurrences, instrument flags. Family joins
carry classifier class, containments and both texts. Review can proceed
without reopening a single source; every page is re-obtainable and
hash-checkable from the committed recipe.
