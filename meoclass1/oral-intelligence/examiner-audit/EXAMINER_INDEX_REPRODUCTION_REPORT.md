# Examiner Index — Production Truth and Reproduction Report

**Date:** 18 August 2026 · **Branch:** `research/oral-examiner-intelligence-v1-audit`
**Subject:** `meoclass1/examiner-index.html` (277,881 bytes)
**Tooling:** `tools/oral/audit_index.py`, `tools/oral/verify_tiers.py`

---

## 1. How is the page created today?

**Verdict: (E) stale output whose generator does not exist in the repository.**

There is no generator. The evidence:

| Probe | Result |
|---|---|
| Repo-wide search for a script emitting `examiner-index.html` | none — the only Python touching `meoclass1/` is `qb_health_check.py`, which does not write it |
| `tools/` subtrees | `corpus/`, `notes/`, `pastpapers/`, `security/` — no `oral/` or `examiner/` producer existed before this audit |
| Git history of the file | `4fe3b3d` and `8bbbc1e` are both **"Add files via upload"** (GitHub web UI), i.e. the artefact was produced off-repo and uploaded |
| Later commits | `78caad4` (July batch), `dac9261` (wording), `e23a557` + `3256684` (**anchor repairs**) — all hand edits to a delivered artefact |

So the page is a **hand-uploaded generated artefact, subsequently hand-patched**. Its inputs are not
version-controlled and its production pathway is not reproducible from this repository.

### Consequence for the anchors

Commit `3256684` — *"Send in-page anchors to the ids the target pages actually carry"* — is the load-bearing
repair. It worked: **0 of 863 links are broken**, every `#qN` resolves to a real q-card. That repair is
the reason this audit can proceed at all.

It also means the anchors were **not** derived from any surviving source. Neither workbook carries a
question anchor:

| Source | Link granularity |
|---|---|
| `MEO_QB_master_v26.xlsx` → `All Questions.Live_File` | **file only** (`QB9_A.html`), 0 rows carry `#q` |
| `MIW_July2026_QuestionBank_SHARE.xlsx` hyperlinks | **file only** (`.../QB1_A.html`), 0 of 1,332 carry `#` |

The question-level precision visible on the page exists **nowhere else in MIW**. It is unique to this
HTML file, and until it is extracted into data it is one bad edit away from being lost.

---

## 2. Independently reproduced counts

Every figure below is recomputed from the rendered `.q-row` elements, not read from the page furniture.

| Quantity | Value |
|---|---|
| **Rendered rows (examiner→question links actually shown)** | **863** |
| Unique (examiner, question) pairs | 862 |
| Duplicate rows | 2 (one pair rendered twice) |
| Examiner sections | 6 |
| Live QB questions reachable from the index | 651 |

### The three count layers disagree

| Layer | Nair | Simon | Rajappan | Srivastava | Senthil | Paul | **Total** |
|---|---|---|---|---|---|---|---|
| **Rendered rows (truth)** | 339 | 243 | 93 | 103 | 66 | 19 | **863** |
| Section heading (`N questions`) | 339 | 243 | 93 | 103 | 66 | 19 | **863** ✅ |
| Mini-nav pill | 324 | 217 | 93 | 102 | 63 | 10 | **809** ❌ |
| Summary bar header | — | — | — | — | — | — | **791** ❌ |

- **Section headings are correct** and are the only trustworthy furniture on the page.
- **Mini-nav is 54 short.** Paul is the worst: the pill says **10**, the section renders **19**.
- **The header says 791**, which is 72 short. Its tier breakdown (359 + 45 + 71 + 316 = 791) is internally
  consistent but jointly stale — it is a frozen snapshot of an earlier generation.

### Tier distribution — reproduced

| Tier literal | Header claims | Actually rendered |
|---|---|---|
| `confirmed` | 359 | **406** |
| `ce_tip` | 45 | **45** |
| `cetip` *(invalid)* | — | **2** |
| `header` | 71 | **87** |
| `inferred` | 316 | **323** |
| **Total** | **791** | **863** |

The per-section `ex-stats` strip is a **fourth** layer and reports only two of the four tiers
(e.g. Nair "✅150 confirmed · 🔹130 inferred-only", omitting his 27 `ce_tip` and 32 `header` rows), so it
sums to 280 against a section of 339. It is not wrong, it is partial — but it reads as a total.

---

## 3. Link integrity

| Check | Result |
|---|---|
| Target file exists | **863 / 863** ✅ |
| Target anchor exists on that page | **863 / 863** ✅ |
| Anchor resolves to a numbered q-card | **863 / 863** ✅ |
| Displayed text corresponds to the live question | 825 pass, 3 drift, 35 blank |

**Zero broken links.** This is the single healthiest fact about the page.

### Defects found

| Class | Count | Detail |
|---|---|---|
| `BLANK_DISPLAY_TEXT` | **35** | `<div class="q-txt"></div>` — the row renders a link with **no question text at all**. Concentrated in `QB4_G` (18), `QB5_C_A` (6), `QB5_G` (6), `QB6_E` (3), `QB7_F` (2). |
| `INVALID_TIER_LITERAL` | **2** | `data-tier="cetip"` on `QB7_I#q1` and `QB7_I#q3` (Simon). The literal is not among the four `data-tier-toggle` values, so `filterTier()` looks up `active["cetip"]` → `undefined` → **both rows disappear permanently the moment a candidate touches any tier checkbox**, with no way to bring them back. |
| `DUPLICATE_PAIR` | **2 rows / 1 pair** | Simon → `QB5_C_A#q1` rendered twice; one copy is also blank. |
| `TEXT_DRIFT` | **3** | `QB1_F#q3`, `QB7_I#q2`, `QB7_I#q3`. All three are **same-core**: the index shows the raw candidate wording ("Vgr who issues and who verifies…") while the page shows the re-authored MIW question ("VGM (Verified Gross Mass) — who issues, who verifies…"). Not mismatches; stale display text. |

None of these is a wrong destination. Every one is a presentation defect on a correct link.

---

## 4. Is the three-tier methodology still reproducible?

The historical description — (1) tracker-confirmed, (2) CE Oral Tip / page metadata, (3) topic-inferred —
is broadly accurate, but only two tiers survive as reproducible.

| Tier | Rows | Re-derivable from the repo today | Verdict |
|---|---|---|---|
| `ce_tip` | 45 | **100.0%** — every one names its examiner inside a CE Oral Tip block on that exact q-card | **REPRODUCIBLE** |
| `confirmed` | 406 | 93.1% name the examiner somewhere on the card or page | **REPRODUCIBLE**, but see caveat |
| `header` | 87 | 81.6% | **NOT REPRODUCIBLE** — 16 rows have no page-level examiner metadata at all |
| `inferred` | 323 | 60.7% *name an examiner anyway* | **MISLABELLED IN BOTH DIRECTIONS** |

### Caveat on `confirmed`

"Confirmed" is supposed to mean *a candidate record says this examiner asked this question*. Against the
two workbooks, only **406 of 862** index pairs have any primary candidate record behind them — and the
overlap is not aligned with the tier label. **456 index pairs carry no primary evidence in either
workbook**, including 147 rows badged `confirmed`, `ce_tip` or `header`. Some of those are legitimately
backed by CE Oral Tip prose rather than a tracker row, but the tier literal does not record which.

### The `inferred` tier is not what it says

196 of 323 `inferred` rows name their examiner in the page's own prose, and **100 of them do so with
assertive CE-Oral-Tip phrasing** ("Rajappan will almost certainly…", "…are the two he asks most"). Those
are not inferences. They are page-declared attributions wearing the weakest badge on the page.

Meanwhile 127 `inferred` rows have no page evidence and no workbook evidence — those are true topic
fallbacks, and **309 pairs in total rest on inference alone**.

---

## 5. The stale count has already escaped the page

`SQ/examiner-index.html` is a **separate, commerce-facing sales page** for this product (13,374 bytes,
paywall pitch, ₹1,499 CTA). It republishes the frozen numbers:

| Sales page claims | Live truth |
|---|---|
| "791+ MEO Class 1 oral questions" | 863 pairs across 681 questions |
| "212 Simon Sir Questions" | 243 |
| "Paul Sir — **All 10 Questions** … the complete, unlocked set" | Paul has **19** index rows; the sample block itself renders **15** |
| "62+ QB Files" | 86 live QB files |

This is the cross-product inconsistency class, not a stale-source problem: the product page and its own
sales page were generated from the same snapshot and neither was refreshed. **`SQ/` is outside this
session's git boundary and was not touched** — recorded here for the Founder.

---

## 6. Regeneration recommendation

Do **not** hand-patch the header and mini-nav. That would fix the symptom and leave MIW with the same
unreproducible artefact.

The correct order:

1. **Extract before repair.** The 863 question-level pairs exist only inside this HTML. Lift them to
   `EXAMINER_RELATIONSHIPS.jsonl` first — that is the asset, the page is a rendering of it.
2. **Re-tier from evidence**, using the closed vocabulary in `EXAMINER_EVIDENCE_LEDGER.jsonl`, so the
   badge states *why* a pair exists rather than which pass created it.
3. **Build a generator** (`tools/oral/build_examiner_index.py`) whose only inputs are the relationship
   file and the live QB inventory, with every count derived from the records it just wrote — header,
   mini-nav, section heading and `ex-stats` computed once from one list.
4. **Gate it**: `validate_audit.py` already fails on all three count mismatches and on the invalid tier
   literal. That gate should block publication.

Blank display text and the `cetip` literal then cannot recur, because neither would be hand-written.
