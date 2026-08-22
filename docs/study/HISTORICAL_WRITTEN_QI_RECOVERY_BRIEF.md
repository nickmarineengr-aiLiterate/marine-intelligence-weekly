# Next session — recover / continue the historical Written Question Intelligence

**Prepared 2026-08-22 on `review/dgma-study-spine-final`. Do not execute any of
this in the session that wrote it.**

> **Re-validated 2026-08-22** against `main` after the public study roadmap
> shipped. Everything below still holds; the only change is that the
> regeneration chain in §5 now has a fourth output — the public page — and one
> extra fail-closed guard, both noted there.

---

> ## ⚠ CORRECTED 2026-08-22 — read this before §1 and §2
>
> The asset claims below were **verified against the refs themselves** and four
> of them were wrong. The machine-readable record is now
> **`docs/study/historical_qi_asset_inventory.json`** (regenerate with
> `tools/study/build_historical_qi_inventory.py`); prefer it over the prose
> here wherever the two differ.
>
> **1. The paths in §2 do not exist as written.** The real prefix is
> `meoclass1/pastpapers/intelligence/v2/`, not `intelligence/v2/`.
>
> **2. The headline finding: the archive is DISCOVERED, not INGESTED.** Not one
> historical question has become an occurrence record. Every one of the 25
> occurrence records and all 9 families begin in **2021-02 or later** — inside
> bands MIW already holds. The QI-v2 layer therefore does **not currently
> extend the evidence horizon backwards at all**. That ingestion is the actual
> remaining work, and it is not a small residue of the project; it is the
> project.
>
> **3. "80 papers, 1999–2005" overstates what can be dated.** There are 80
> question papers plus 1 sample paper. Of those, only **5 print month AND year
> (all of them 1999)**; **59 are year-only** (58 of 2001, 1 of 2005); and **17
> print no date at all**. Content status is 76 PARSED, 4 PARTIAL, 1 UNREADABLE. So "1999–2005" is a range of
> *filing*, not a timeline that 81 papers can each be placed on.
>
> **4. The raw objects are not on this laptop.** The PDFs/DOCs are deliberately
> not committed (public repo) and live in a git-ignored intake store on the
> authoring workstation (a `D:\` path). What IS preserved is the
> machine-independent recipe — archive URL + sha256 — so ingestion needs either
> that workstation or a re-fetch from the Wayback URLs recorded in
> `PHASE3B_SOURCE_INVENTORY.json`.
>
> **5. 2006–2020 is confirmed absent from accessible state.** A bounded search
> over **125 distinct trees across 183 refs** found no gap-era paper id in any
> filename and no gap-era `sitting_year` anywhere. Status stands at
> `NOT_FOUND_ON_ACCESSIBLE_STATE` — which is not the same as "never existed".
>
> **6. The D01–D10 join is already proved and needs no new taxonomy.** All 9
> families join to exactly one spine topic *through the questions they
> contain* (occurrence `question_id` → `study_mappings.json`), never through
> the QI-v2 topic string. Two questions sit in two families each
> (`QP2608-Q4, QP2608-Q8`) and are flagged for adjudication rather than resolved silently.
>
> **7. Nothing was widened.** The socket is still `NOT_STARTED`, the study
> order is unchanged, D01 is still Topic 01, and the public sentence is
> untouched. `tools/study/test_historical_qi_inventory.py` sweeps the
> reader-facing surfaces for the forbidden claims and proves the sweep fires.

The study system now has a governed, empty socket for historical Written QI
(`docs/study/written_evidence_horizon.json`, layer `HISTORICAL_WRITTEN_QI`,
status `NOT_STARTED`). This brief is what the recovery session needs so it does
not repeat the search.

---

## 1. Correct the premise first

The task was framed as recovering Written QI "from approximately 2010 onward".
**No 2010-onward corpus exists in accessible state, and none was found.** What
exists falls into two disjoint bands with roughly fifteen years missing between
them:

| Band | What exists | Where |
|---|---|---|
| **1999–2005** | 80 archived DG Shipping MEO Class I question papers | unmerged QI-v2 branch |
| **2006–2020** | **nothing** | — |
| **2021–2023** | 30 papers / 270 questions, question wording only | committed on `main` |
| **2023–2026** | 40 papers / 360 questions, fully solved | committed on `main` (the current layer) |

Do **not** record the missing band as "never existed". The correct status is
`NOT_FOUND_ON_ACCESSIBLE_LAPTOP_STATE`: Desktop-local state is not verifiable
from this machine, and DG Shipping's own archive was only partially walked.

**Public-claim consequence:** until a validated range is stored, no surface may
say "16 years", "since 2010", or "2010–2026". `evidence_model.public_evidence_claim()`
enforces this by construction, and `test_study_expandability.py` asserts it.

---

## 2. Assets found — start here, do not re-search

| Asset | Location | Class | Holds |
|---|---|---|---|
| `historical_qp_intelligence.json` | `main`, committed | `FOUND_AND_CURRENT` | 30 papers / 270 questions, 2021–2023, `INTELLIGENCE_ONLY` |
| `intelligence/v2/QUESTION_FAMILIES.json` | `origin/research/question-intelligence-v2-phase3b` **(unmerged)** | `FOUND_PARTIAL` | 9 families (7 counted, 7 excluded), 2021-02 → 2026-08 |
| `intelligence/v2/QUESTION_OCCURRENCES.jsonl` | same branch | `FOUND_PARTIAL` | 25 occurrence records |
| `intelligence/v2/PHASE3B_SOURCE_INVENTORY.json` | same branch | `FOUND_PARTIAL` | 98 archived DGS objects; 80 question papers, 1999–2005 |
| `intelligence/v2/OFFICIAL_BANK_ITEMS.json` | same branch | `FOUND_PARTIAL` | the DGS's own 185-item *Question Bank MEO CL-I*, undated |
| `intelligence/v2/SOURCE_MANIFEST.json` | same branch | `FOUND_PARTIAL` | 42 sources with access-compliance record |
| Sittings 2006–2020 | nowhere reachable | `NOT_FOUND_ON_ACCESSIBLE_LAPTOP_STATE` | — |

Everything on the QI-v2 branch is marked `RESEARCH_ONLY`. It is **not** merged
to `main` and must not be treated as governed until it is.

Related review records, all on unmerged branches:
`review/question-intelligence-v2-phase2`, `…-phase3a`, `…-phase3a1`,
`…-phase3a2`, `…-phase3a3`. Phase 3A.2 and 3A.3 both ended on **HOLD**.

---

## 3. Known landmines, already paid for

Read these before touching the data — each was learned the expensive way:

- **The DGS archive dates almost nothing.** Of 80 archived question papers,
  58 print a **year only** (mostly 2001) and 17 print **no date at all**. A
  test on that branch already enforces "a sitting month must be printed by the
  paper". An earlier 2005 sitting date was *withdrawn* as unsupported.
- **Bank ancestry proves existence, not date.** An item appearing in the
  official 185-item DGS bank shows the question is official. It dates nothing.
- **Recurrence is observed at LIMB level, not whole-question level.** Families
  key on `(question_id, limb_label)`. A family model keyed on whole questions
  will under-count.
- **A 14-year "revival" was a false positive.** Phase 1 classed two families
  as `LONG_DORMANT_REVIVAL` on a 14-year gap; both rested on a single
  third-party source whose full text was never seen. Phase 2 corrected it.
  Expect long-gap claims to be wrong until the primary source is read.
- **Crude keyword sweeps invent false ancestry.** Read the stem.
- **The 24/48-month dormancy cuts follow the sitting calendar**, not
  statistics — MEO Class I sits about eleven times a year.

---

## 4. Schema the study system will accept

The socket already publishes the vocabulary, and it was **adopted from QI-v2
rather than invented**, so no translation layer is needed:

```
dormancy   ACTIVE_RECURRENCE · RECENT_RETURN · HISTORICAL_RETURN ·
           LONG_GAP_RETURN · ONE_OFF_HISTORICAL · INSUFFICIENT_HISTORY
relevance  CURRENT_RELEVANT · HISTORICAL_RELEVANT · SUPERSEDED ·
           REQUIRES_CURRENTNESS_REVIEW
windows    all_time · last_10_years · last_5_years · last_3_years ·
           current_syllabus_era
trend      INCREASING · DECREASING · PERSISTENT · DORMANT · RE_EMERGING ·
           INSUFFICIENT_HISTORY
status     NOT_STARTED · PARTIAL · VALIDATED_RANGE · COMPLETE
families   stable ids in the `FAMILY-EM-` namespace
```

**Store raw occurrence counts first.** Every window above is a transparent cut
over them, and a consumer may ignore all of them. There is no weighting and no
opaque score.

**Historical frequency is not current relevance.** A family that recurred for a
decade under a superseded instrument must be able to say `SUPERSEDED` rather
than being promoted into the study order by its raw count. That is what the
`relevance` axis is for, and it is separate from `dormancy` on purpose.

---

## 5. Integration point — one function, nothing else

```
recovered papers → canonical question identities → occurrences → families
        ↓
docs/study/written_evidence_horizon.json   (layers.historical_written_qi)
        ↓
build_study_spine.py → export_roadmap_xlsx.py → build_topic_pages.py
                                             → build_public_study_roadmap.py
```

Concretely:

1. Populate the socket via `evidence_model.empty_qi_socket(status, **known)`.
2. Run `evidence_model.assert_honest(socket)` — it **fails closed** on a
   completeness claim wider than the stored evidence, and that is deliberate.
3. Regenerate: `build_evidence_horizon.py` → `build_study_spine.py` →
   `build_coverage_matrix.py` → `export_roadmap_xlsx.py` →
   `build_topic_pages.py` → `build_public_study_roadmap.py`.
4. The last of those renders the PUBLIC page `SQ/study-roadmap.html`. It
   recomputes the evidence sentence with `evidence_model.public_evidence_claim()`
   and **fails closed if the stored `derived_sentence` disagrees**, so step 3
   must be run in order — a widened socket with a stale horizon artefact stops
   the build rather than publishing either wording. Its guards also refuse any
   claim wider than the socket states, which is the last line of defence against
   a partial recovery being marketed as a complete one.

The workbook columns and the website copy then populate **by themselves**. The
reserved fields already exist (`historical_written_papers`,
`long_term_recurrence`, `recent_recurrence`, `trend`, `currentness`, …) and
render as `NOT YET INTEGRATED` until the layer is live.

**Do not** put QI interpretation inside the Excel renderer, the HTML generator
or the roadmap UI. They consume governed output. A classifier in a renderer is
a second taxonomy by the back door.

**Do not** create a second topic taxonomy or a second roadmap. Families attach
to the existing `D01–D10` spine through the existing crosswalk.

---

## 6. Family stability

New historical evidence must **attach to existing families**, not recreate them
each rebuild. Family ids are stable identity, not derived data. If family
semantics genuinely change, use governed supersession/migration — the same
pattern the oral follow-up register uses — rather than silently reassigning an
id.

---

## 7. Priority model — do not pre-emptively re-weight

Today's roadmap uses current verified evidence only. `study_priority` in
`tools/study/study_spine.py` is transparent: every component publishes its raw
input, weight and scaled contribution.

When historical QI is `GO`, components such as `historical_written_recurrence`,
`recent_written_recurrence` and `trend_persistence` may be added — **explicitly
and documented**, scaling existing weights proportionally rather than re-tuning
them, exactly as `official_scope` was added this session. Then recompute and
**record whether the study order changed**.

**D01 remains Topic 01** until current verified data says otherwise. Do not
destabilise it on the expectation of future evidence.

---

## 8. Expected outputs of the recovery session

1. A validated coverage statement — the **real** range, e.g. `VALIDATED_RANGE
   2021–2026` plus whatever of 1999–2005 can be dated, with gaps recorded.
2. Canonical question identities for every recovered paper.
3. Occurrence records, sittings never collapsed.
4. Families with stable ids, dormancy **and** relevance classified separately.
5. A populated `historical_written_qi` layer passing `assert_honest()`.
6. Regenerated roadmap, workbook and topic pages — with the public sentence
   strengthened *by the generator*, never by hand.

## 9. Explicitly out of scope for that session

F2 · the 788 audit · the final v27 XLSX · the `QP2303-Q9` / `QP2406-Q9` /
`QP2411-Q9` lubricating-oil `primary_category` defect (a written-production
task) · Topic 01 gaps N6/N7/N8 · the D07 cargo scope decision.
