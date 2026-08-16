# Disney Audit — Approved Implementation Report

**Date:** 16 August 2026
**Session scope:** Implementation of the Founder-approved canonical solvedQP changes arising from the Disney candidate-notes Founder Review Closure. No re-opening of the Disney audit.
**Status:** IMPLEMENTED — awaiting Founder review of the diff. **Not committed. Not pushed.**

---

## 1. Baseline

| Field | Value |
|---|---|
| Repository | `F:\Marine-Intelligence-Weekly` |
| Branch | `main` |
| HEAD at start | `59230fb2b4525a03375b50f51f36c2f7648e8ae3` |
| `git status` at start | **Clean.** Zero modified, zero untracked. |
| Safe isolation | Guaranteed. No unrelated uncommitted work existed, so nothing was reset, stashed, cleaned or overwritten. |

The Disney working directory (`meoclass1/pastpapers/docs/notes from candidate/`) is excluded by `.gitignore:83`, which is why the audit outputs produced in the previous session do not appear in `git status`. They were read, not modified.

### 1a. Pre-edit baseline build — and a trap caught before any edit

The toolchain was run **before** editing, to separate generator behaviour from my own changes. This immediately mattered:

- `python tools/pastpapers/run_toolchain.py` (no arguments) passed every stage **but rewrote 48 tracked pages**, replacing the published `robots` directive with `noindex, nofollow, noarchive, nosnippet` and stripping the Open Graph and JSON-LD blocks. A no-argument build emits the *unpublished* variant of every page.
- Per STEP 8 I stopped and investigated rather than accepting the drift.
- `python tools/pastpapers/run_toolchain.py --publish` restored all 48 files **byte-identically to HEAD** (`git status` → 0 files). Determinism confirmed, baseline restored.

`--publish` is therefore the correct invocation, and is the one used for all validation below. Had the build been run only *after* editing, this drift would have been indistinguishable from my own changes.

**This hazard was already documented, and the documentation is clear.** `LAPTOP_REVIEW_AND_INTEGRATION_PROTOCOL.md` §3.M states that "`main` commits the **publish** build. `run_toolchain.py --publish` is therefore the pre-commit gate; the bare run is not," warns that the build-state assertion is mode-symmetric so a green checker proves only that the tree matches the mode requested, and records a prior incident in which a review-mode run left 37 pages carrying `noindex`. `QA_AND_HANDOVER_PROTOCOL.md` §1 repeats the point and cross-references it. Nothing needed to be added; the pre-edit baseline simply re-derived a known trap.

---

## 2. Authoritative York-Antwerp Rule XXI verification

### Source hierarchy actually followed

1. **Local true-source corpus first.** `F:\miw-true-source\general-average` was located and read in full (9 files). It is a definitions/metadata package: it holds `YAR_DEFINITIONS.json`, an instrument register, a coverage matrix and a watch register. **It contains no text of Rule XXI**, and its instrument register records only "YAR 2016 … current" with **no mention of the October 2022 alteration**. It could not resolve the question. (See §8, NEW FINDING 1.)
2. **CMI primary material.** Resolved there.

### Primary source used

- Comité Maritime International, **published English text of the York-Antwerp Rules 2016**
  `https://comitemaritime.org/wp-content/uploads/2023/01/YAR-2016-English-Version.pdf`
  Retrieved and text-extracted 16 August 2026.
- Compared directly against the superseded CMI text
  `https://comitemaritime.org/wp-content/uploads/2023/01/YAR-2016-English-with-Rule-XVII-correction-1.pdf`

**Why the previous session was blocked.** It fetched the PDF whose filename advertises the Rule XVII correction — the natural-looking "current text" link — and correctly declined to assert a replacement rate it had not seen. The operative text sits at the plainer filename, uploaded January 2023, *after* the Antwerp meeting. When a body reissues an amended text under the same edition title, the filename carries no version signal; upload date and internal footnotes do.

### The two texts, side by side

| | Rule XXI(b) |
|---|---|
| **As adopted** (New York, May 2016) | "the 12-month ICE LIBOR for the currency in which the adjustment is prepared, as announced on the first banking day of that calendar year, **increased by four percentage points**. If the adjustment is prepared in a currency for which no ICE LIBOR is announced, the rate shall be the 12-month US Dollar ICE LIBOR, increased by four percentage points." |
| **As amended** (Antwerp, October 2022) | "**2 per cent per annum added to the USD Prime Rate, as published in the Wall Street Journal for the first banking day of that calendar year.**" |

### Findings established (all to high confidence, from the primary text)

1. **Prior basis:** 12-month ICE LIBOR for the currency of the adjustment, + four percentage points, with a USD ICE LIBOR fallback.
2. **What changed in October 2022:** paragraph **(b) only** — the rate formula. Paragraph (a) (interest runs on expenditure, sacrifices and allowances until **three months after the date of issue of the adjustment**, with allowance for payments on account) is **unchanged**.
3. **Exact benchmark:** the **USD Prime Rate as published in the Wall Street Journal**.
4. **Exact margin:** **2 per cent per annum**, added to that rate.
5. **How/when determined:** annually — the rate for interest accruing during each calendar year is fixed by reference to the WSJ USD Prime Rate **for the first banking day of that calendar year**. Note that the currency-of-adjustment selection and the fallback limb both disappear: the amended rule is a single USD-referenced rate.
6. **Edition status: NOT a new edition.** The document is titled "YORK-ANTWERP RULES 2016" and carries a footnote to Rule XXI(b): *"This paragraph was amended, due to technical reasons, by the CMI Assembly in Antwerp in October 2022."* The amendment is internal to the 2016 edition. Nothing in the corrected answers implies a "YAR 2022".
7. **Temporal application:** the amendment (October 2022) **predates all three sittings** — QP2403 March 2024, QP2510 October 2025, QP2606 June 2026. There is no historical-accuracy defence for any of them.
8. **"LIBOR" appears zero times in the current CMI text.**

**Terminology note.** The CMI *web page* attributes the change to the "CMI Conference in Antwerp in October 2022"; the *official text's own footnote* attributes it to the **CMI Assembly**. The corrections follow the official text and say **Assembly**.

**Why the existing QP wording was stale.** The three answers presented the ICE LIBOR formula as the current text of Rule XXI. Two of them carried a caveat, but the caveat diagnosed a **market event** (LIBOR ceasing to be published) rather than the operative **rule amendment** by the CMI. A candidate was left believing the 2016 Rule still reads ICE LIBOR — which it does not, and has not since October 2022.

**Confidence: HIGH.** Both texts obtained from the issuing body, extracted, and compared directly.

---

## 3. Files modified

```
meoclass1/pastpapers/specs/QP2403.json
meoclass1/pastpapers/specs/QP2510.json
meoclass1/pastpapers/specs/QP2601.json
meoclass1/pastpapers/specs/QP2606.json
```

Deterministically regenerated from those specs (not hand-edited):

```
meoclass1/pastpapers/QP2403.html
meoclass1/pastpapers/QP2510.html
meoclass1/pastpapers/QP2601.html
meoclass1/pastpapers/QP2606.html
solvedQP/QP2403.html
solvedQP/QP2510.html
solvedQP/QP2601.html
solvedQP/QP2606.html
SQ/solved-qp-sample-january-2026.html
meoclass1/oralnotes/written-sample-january-2026.html
meoclass1/oralnotes/solved-qp-january-2026-full.html
```

All edits were applied as **exact-match raw-text surgery** on the spec JSON (which is serialised with `indent=1`), each replacement asserting its expected hit count, with an all-or-nothing write. No spec was reserialised, so no incidental formatting drift was introduced.

---

## 4. Question-level changes

### 4.1 `QP2403-Q3` — General Average, Principles and Contribution (March 2024)

**Previous defect.** The answer asserted, in seven places, that Rule XXI's interest basis is 12-month ICE LIBOR for the currency of the adjustment plus four percentage points — the paragraph as adopted in 2016, superseded since October 2022. The provenance caveat misattributed the staleness to LIBOR's withdrawal from the market rather than to the CMI's amendment of the Rule.

**Sites corrected (7 — the whole semantic unit, not one prose string):**

| # | Location | Change |
|---|---|---|
| 1 | `sources[25]` — the `PRIMARY` line | Now states the amended rate and records the October 2022 amendment; the 2016-as-adopted wording is kept parenthetically as history |
| 2 | `model_answer.blocks[16].p` | States the amended rate as current; marks the ICE LIBOR wording expressly `superseded`; states that the amendment did not create a new edition |
| 3 | `study_notes.blocks[7].ul[3]` | Rule XX/XXI note rewritten to the amended rate, original wording labelled superseded |
| 4 | `answer_route.steps[3].points[9]` | Route point restated to the amended rate |
| 5 | `quick_revision.critical_numbers[5]` | Critical number restated; former figure retained as labelled history |
| 6 | `temporal_review.notes[4]` | Wrong diagnosis replaced: the operative event is a CMI amendment, not the market withdrawal of LIBOR. Records that the amendment predates both sittings |
| 7 | `reverify_before_publication[2]` | `claim` and `why` rewritten to the verified position with the source and retrieval date; `class` moved `C_ACCEPTED_LIMITATION` → `B_CURRENCY_CHECK` |

**Old proposition:** *Rule XXI interest = 12-month ICE LIBOR (currency of adjustment) + 4 percentage points, stated as current.*
**New proposition:** *Rule XXI interest runs until three months after issue of the adjustment; the rate for each calendar year is the WSJ USD Prime Rate for the first banking day of that year + 2 per cent per annum, following the CMI Assembly's technical amendment at Antwerp in October 2022. The ICE LIBOR formulation is the 2016-as-adopted wording and is superseded.*

**Reverify class change rationale.** The closed vocabulary permits only `B_CURRENCY_CHECK` and `C_ACCEPTED_LIMITATION`. The entry is no longer an accepted limitation — it is resolved against primary text — but it remains the kind of provision to re-check at each sitting. `B_CURRENCY_CHECK` is the correct existing value; no vocabulary was invented.

**Cross-link change:** one added (see §5).

### 4.2 `QP2510-Q3` — General Average, Principles and Contribution (October 2025)

Treated identically to QP2403-Q3, as directed — the two are a recurring pair (`QP2510-Q3` reuses `QP2403-Q3`) with the same answer substance.

**Sites corrected (7):** items 1–5 and 7 exactly as above, plus:

| # | Location | Change |
|---|---|---|
| 6 | `temporal_review.notes[1]` | This note asserted the 2016 edition's currency at the sitting and discussed a *different* 2022 CMI event (the GA Guidelines 2nd edition) while missing the actual 2022 rule change. A clause was added recording that Rule XXI(b) was amended in October 2022, before this sitting, and that the answer states the amended rate. |

**Old proposition / new proposition:** identical to §4.1.

**Cross-link change:** one added (see §5).

### 4.3 `QP2606-Q3` — Types of Loss, General Average and Warranties (June 2026)

Lowest severity of the three, as the closure predicted: the stem asks for the General Average Act **as per York-Antwerp Rules 1994**, and the 1994 position (interest fixed at 7 per cent per annum) is unaffected by the 2022 amendment and was left untouched. The defect reached only the 2016 comparative material.

**Sites corrected (3):**

| # | Location | Change |
|---|---|---|
| 1 | `sources[4]` | The 2016 limb now records the amendment and the amended rate; the 1994 limb (7 per cent) unchanged |
| 2 | `model_answer.blocks[14].table.rows[3][2]` — the 1994-vs-2016 comparison table | "…a published benchmark plus four percentage points" → "…a published benchmark: since the technical amendment of October 2022, the USD Prime Rate plus 2 per cent per annum" |
| 3 | `study_notes.blocks[20].p` — provenance note | Rewritten: see below |

**Old proposition:** *YAR 2016 Rule XXI sets the rate by reference to a published benchmark plus four percentage points; no current rate is asserted because the benchmark has been affected by the withdrawal of LIBOR.*
**New proposition:** *YAR 2016 Rule XXI sets the rate by reference to a published benchmark; since the October 2022 technical amendment that is the WSJ USD Prime Rate + 2 per cent per annum. The 1994 figure of 7 per cent is unaffected.*

**One consequential edit the Founder should see explicitly.** The provenance note previously read: *"MIW holds no licensed copy of the published Rules themselves, and that limitation is recorded rather than glossed."* Once the CMI's own published English text of the 2016 Rules had been read directly and a rate asserted from it, that sentence became **self-contradictory within its own paragraph** and its neighbouring sentence ("no current rate is asserted") became false. I therefore replaced the denial with an accurate statement that the CMI text has now been read directly. This was not an opportunistic holdings-denial sweep — it was required to stop my own correction creating a contradiction. The paragraph's other limitations (Marine Insurance Act 1963 section numbers, the English Insurance Act 2015 contrast) were **left untouched**. The wider holdings-denial question is raised as NEW FINDING 2 and not acted on.

### 4.4 `QP2601-Q7` — UNCLOS Flag State Duties and India's Mechanism (January 2026)

**Previous gap.** Limb (c) went straight to the institutional machinery (statute, Administration, delegation) without the constitutional step that makes it intelligible: *why* domestic legislation is needed at all, and *where* Parliament's power to enact it comes from.

**Exact material added** — one new `model_answer` paragraph, inserted after the heading "4. (c) India's mechanism" and before the existing statutory paragraph (97 words, three sentences):

> UNCLOS does not execute itself in Indian law. India is a **dualist** State: accepting the Convention binds India internationally, but its provisions do not thereby become enforceable domestic shipping law — they must be carried in by statute. **Article 253 of the Constitution** supplies the power, empowering Parliament to make law for the whole or any part of India to implement any treaty, agreement or convention with another country, notwithstanding the ordinary distribution of legislative powers; and the subject matter is Union business in any event, **Seventh Schedule, Union List entry 25** covering **maritime shipping and navigation**.

This covers exactly the three approved elements, and only those: (1) domestic implementation rather than automatic executability; (2) Article 253; (3) Seventh Schedule, Union List Entry 25.

**One supporting change.** A single `answer_route` core point was added at the head of step 4, limb (c):

> "Art 253 and Union List entry 25 — Parliament's power to implement a convention; UNCLOS needs domestic legislation"

**Why this was necessary rather than scope creep.** `answer_route` is the corpus's one canonical answering sequence, from which the knowledge map, recall, plan and cheat-sheet derive. A scoring point present in the model answer but absent from the route is a point the candidate is never led to write — the enrichment would be inert. This is the minimum needed to make the approved addition actually scoreable. Core-point count for the question moves 27 → 28.

**Confirmation the historical position is untouched.** The following paragraph is unchanged and still reads: *"At the date of this paper — January 2026 — the operative statute was the Merchant Shipping Act, 1958. The Merchant Shipping Act, 2025 had received assent on 18 August 2025 but had not commenced; it was brought into force on 15 March 2026, two months after this sitting…"* The added paragraph asserts no statute and no date, so the January 2026 temporal position is intact.

**Confirmation the do-not-import list was honoured.** Automated check over the whole question object:

| Excluded item | Present? |
|---|---|
| Article 297 | absent |
| Article 51(c) | absent |
| Maritime Zones Act 1976 / "1976" | absent |
| Union List entries 14, 21, 57 | absent |
| UNCLOS signature date (10 December 1982) | absent |
| UNCLOS ratification date (29 June 1995) | absent |
| MS Act 2025 as operative at the sitting | absent — expressly stated as *not* commenced |

The word "ratification" does occur once, but only inside the **cross-link label** describing what the April question asks. No ratification date or position is imported into the January answer.

`question_delta`, `recurrence_class` (`topic_recurrence`) and `recurrence_adjudication` were **not modified**.

---

## 5. Cross-links

The repository has an established mechanism: a `cross_links` array of `{label, href}` objects. It is in wide use — **717 links corpus-wide, 185 of them cross-paper** — and cross-paper recurrence links with distinguishing labels are already conventional (e.g. `QP2404-Q7 → QP2506-Q6`, "the same question at the June 2025 sitting"). **No new schema field was invented and no new architecture introduced.**

### 5.1 Artificial general average — `CROSS_LINK_ONLY` (item C)

Added to **`QP2403-Q3`** and **`QP2510-Q3`**:

> `QP2601.html#q3` — "QP2601 Q3 — salvage and general average, where artificial general average is treated at length"

No artificial-GA prose was added to either answer. Both are already long, and the full treatment stays in `QP2601-Q3` as decided.

### 5.2 UNCLOS recurrence — reciprocal link (item D)

`QP2604-Q7` **already** linked to `QP2601-Q7`, labelled *"the same subject at the January 2026 sitting, when the 1958 Act still applied"*. The relationship was therefore only half-discoverable. Added the missing reciprocal to **`QP2601-Q7`**:

> `QP2604.html#q7` — "QP2604 Q7 — the same subject at the April 2026 sitting, where the question also asks for the constitutional mechanism and the position since ratification"

The label deliberately says **"the same subject"**, not "the same question", and names the two ways April is broader (constitutional mechanism; position since ratification). This preserves the existing `question_delta` on `QP2604-Q7`, which records April as a NEAR recurrence that widened. No recurrence metadata was altered on either question, so there is no conflict with existing recurrence semantics.

**Not added:** nothing was withheld under items C or D. Both were implementable on the established mechanism.

---

## 6. SIRE low-priority closure — AUDIT ONLY, `NO_CHANGE`

All three were read completely, model answer end to end. **No file was modified.**

| Question | Sitting | Result |
|---|---|---|
| `QP2502-Q4` — Vetting inspection on an oil tanker and the Chief Engineer | February 2025 | **NO_CHANGE.** SIRE 2.0 correctly described as the current generation at a February 2025 sitting, with its risk-based, question-pool, hardware/process/human-element and digital-capture characteristics accurately stated. TMSA, CDI, ISGOTT and the Pre-Inspection Questionnaire correctly placed. The commercial-not-statutory distinction is correct. No stale date claim, no forward-looking claim that has since been overtaken. |
| `QP2507-Q7` — Substantial corrosion | July 2025 | **NO_CHANGE.** Temporally and substantively correct: 2011 ESP Code (resolution A.1049(27)) mandatory through SOLAS XI-1/2, definition at paragraph 1.2.9, both the general and CSR limbs, and the paragraph 1.1.3 survey-extension trigger. |
| `QP2507-Q8` — Classification and dual class | July 2025 | **NO_CHANGE.** SOLAS II-1/3-1, I/6 and XI-1/1 and the RO Code (MSC.349(92), parts 1–2 mandatory, part 3 recommendatory) all correctly stated, as is the central point that dual class doubles the class obligation and leaves the statutory obligation single. |

**Observation, not a defect:** `QP2507-Q7` and `QP2507-Q8` are not in fact SIRE questions — they are substantial corrosion and classification/dual class respectively. They were nonetheless read in full as directed, so the low-priority review is closed on its merits either way.

**The low-priority SIRE review is closed as `NO_CHANGE`.** No further audit session is needed for these three.

---

## 7. Corpus-wide Rule XXI safety sweep (read-only)

Loose matching across **all 39 specs / 351 questions**, over every string value at every JSON path, for: `LIBOR`, `ICE LIBOR`, `Rule XXI`, `four percentage` / `4 percentage points`, `interest on general average`, `prime rate`, `SOFR`, `per cent per annum`, `benchmark`.

**Occurrences examined:** 17 questions matched the loose pattern; all were inspected and the false positives (unrelated uses of "benchmark" and "per cent per annum") discarded.

**Genuine Rule XXI / GA-interest occurrences outside the three authorised targets: one question.**

| Question | Finding | Action |
|---|---|---|
| `QP2312-Q3` (December 2023) — 5 sites: `sources[0]`, `model_answer.blocks[12].ul[2]`, `regulations[4]`, `quick_revision.critical_numbers[1]`, `search_aliases[15]` | **NOT STALE — no change required.** The stem expressly asks to "Define General Average Act as per York Antwerp Rules **1994**". Every occurrence is the **1994** Rule XXI at **7 per cent per annum**, which is correct for that edition and wholly unaffected by the October 2022 amendment to the 2016 Rules. | **NO CHANGE.** Correctly stated. |

**No additional stale occurrences were found. No propagation beyond the three authorised targets.** No file outside the authorised scope was modified as a result of this sweep.

Post-correction coherence check confirms every surviving mention of "LIBOR" in the three targets is accompanied by a historical marker (`as adopted` / `superseded` / `October 2022` / `amended`) — there is no unguarded stale assertion left anywhere in the corpus.

---

## 8. New findings — FOUNDER APPROVAL REQUIRED

Recorded only. **Nothing below was modified.**

### NEW FINDING 1 — the true-source General Average package does not record the October 2022 amendment
**Location:** `F:\miw-true-source\general-average\` (separate repository, outside `Marine-Intelligence-Weekly`) — `YAR_INSTRUMENT_REGISTER.md`, `WATCH_REGISTER.md`, `CURRENT_STATUS.md`.
**Issue:** the register lists "YAR 2016 … current" with no reference to the technical amendment of Rule XXI(b), and the watch register's `W3` still describes the official text as uncaptured ("working text = CMI reproduction + BIMCO guidance"). The package claims 24 rule objects but holds no Rule XXI text. Its status is `FOUNDER_REVIEW` with all validation gates passing — so the gates do not currently detect a missing in-edition amendment.
**Why it matters:** this is the package a future session would consult first for General Average, and it would not have resolved today's question. The CMI's published English text is freely downloadable and could be captured.
**Severity:** medium. No candidate-facing surface is affected.

### NEW FINDING 2 — holdings-denial in `QP2606-Q3` was broader than the one clause corrected
**Location:** `meoclass1/pastpapers/specs/QP2606.json`, `QP2606-Q3`, `study_notes.blocks[20].p`.
**Issue:** the paragraph asserted that "MIW holds no licensed copy of the published Rules themselves". I corrected this only so far as the **2016** Rules, because leaving it would have contradicted the rate I was asserting (§4.3). The claim also appears to be too broad for the **1994** Rules: `QP2312-Q3`'s own `sources[0]` records the York-Antwerp Rules 1994 as "read in full from a published copy of the text", and the CMI serves the 1994 English text publicly. This is the understated-holdings defect class that has recurred in this corpus.
**Why it is only reported:** the 1994 limb is outside the authorised Rule XXI scope and needs no change for the correction to be sound.
**Severity:** low. Understates capability; asserts nothing false to a candidate.

---

## 9. Validation

All commands run from `F:\Marine-Intelligence-Weekly`.

| Check | Command / method | Result |
|---|---|---|
| Baseline build determinism | `python tools/pastpapers/run_toolchain.py --publish` (pre-edit) | **PASS** — 48 files restored byte-identical to HEAD, `git status` clean |
| Every edited JSON parses | `json.loads` gate inside the edit script, all-or-nothing write | **PASS** — 4/4 |
| Every replacement matched exactly once | assertion per edit (25 edits) | **PASS** — 25/25 at expected count 1 |
| Full toolchain after edits | `python tools/pastpapers/run_toolchain.py --publish` | **ALL STAGES PASS**, exit 0 |
| — SPEC (schema validation) | `validate_spec.py`, all 39 specs | PASS |
| — AUDIT (each page faithful to its spec) | `audit_paper.py` | PASS, all papers |
| — RECURRENCE (provenance boundary) | `recurrence_check.py` | PASS |
| — KNOWN TRAPS | `known_traps_check.py` | PASS |
| — TEMPORAL | `temporal_sweep.py` | PASS (candidate list only; non-blocking by design) |
| — HEALTH (coherence, links, safety, review state) | `health_check.py` | PASS (1 warning) |
| — SOLVEDQP HOME / TOPIC MAP contract tests | contract tests | PASS |
| — DELIVERY | `delivery_gate.py` | PASS (12 warnings — see below) |
| No duplicate question IDs | corpus-wide `Counter` over all `question_id` | **PASS** — zero duplicates |
| Question count unchanged | corpus-wide count | **39 papers / 351 questions** — unchanged |
| No broken cross-links | every `cross_links.href` target resolved on disk | **PASS** — 0 unresolved of 720 (717 before, 3 added) |
| Answer donors unaltered | `reused_from`, `question_delta`, `recurrence_class`, `recurrence_adjudication` untouched on every edited question | **PASS** |
| No unrelated files changed | `git status` reviewed file by file | **PASS** — see §10 |

**Warning delta: 509 → 521 (+12), fully explained.** All twelve are `DELIVERY` `UNSTAGED` warnings — exactly the 4 papers × 3 artefacts (`specs/*.json`, `meoclass1/pastpapers/*.html`, `solvedQP/*.html`) that this session modified. The delivery gate reads the Git index rather than the working tree, so it correctly reports uncommitted work. They will clear on commit. No new warning of any other class appeared.

**Generated-artifact drift check.** The build did **not** rewrite large numbers of unrelated files. Fifteen files changed, all traceable to the four edited specs (§10).

**Public-surface check.** `SQ/solved-qp-sample-january-2026.html` is public by design, so its diff was inspected directly: the only change is a depth counter, `27 core points` → `28 core points`. **No paid content leaked** — the new constitutional paragraph and the new route point are absent from the public sample (verified by grep for `Art 253` / `Union List entry 25` / `dualist` → 0 hits). The two `meoclass1/oralnotes/` pages do carry the new text, and are **server-side gated** behind the `ORAL_QB_NOTES` entitlement (`api/_lib/routes.js:38`), so the exposure posture is unchanged.

---

## 10. Git diff summary

15 files changed, **84 insertions, 64 deletions**.

```
 SQ/solved-qp-sample-january-2026.html                |  2 +-
 meoclass1/oralnotes/solved-qp-january-2026-full.html |  9 +++++----
 meoclass1/oralnotes/written-sample-january-2026.html |  9 +++++----
 meoclass1/pastpapers/QP2403.html                     | 10 +++++-----
 meoclass1/pastpapers/QP2510.html                     | 10 +++++-----
 meoclass1/pastpapers/QP2601.html                     | 11 ++++++-----
 meoclass1/pastpapers/QP2606.html                     |  4 ++--
 meoclass1/pastpapers/specs/QP2403.json               | 22 +++++++++++++---------
 meoclass1/pastpapers/specs/QP2510.json               | 22 +++++++++++++---------
 meoclass1/pastpapers/specs/QP2601.json               |  8 ++++++++
 meoclass1/pastpapers/specs/QP2606.json               |  6 +++---
 solvedQP/QP2403.html                                 | 10 +++++-----
 solvedQP/QP2510.html                                 | 10 +++++-----
 solvedQP/QP2601.html                                 | 11 ++++++-----
 solvedQP/QP2606.html                                 |  4 ++--
```

**Unrelated files changed: none.** Every one of the fifteen is either a spec I was authorised to edit or a deterministic regeneration from one of those four specs. The three files that are not obviously per-paper artefacts are all derived from `QP2601` (January 2026): the public sample and the two gated oralnotes pages, each accounted for above.

---

## 11. Scope control — explicitly NOT modified

**Not modified, as directed:**

- `QP2307-Q5` (nautical assessors) — untouched
- `QP2401-Q7` (SIRE) — untouched
- `QP2504-Q7` (SIRE) — untouched
- `QP2510-Q1` (Big Data) — untouched
- All other Big Data recurrence questions — untouched
- `QP2502-Q4`, `QP2507-Q7`, `QP2507-Q8` — **read in full, deliberately not modified** (§6)
- `QP2312-Q3` — stale-looking on a loose sweep, verified correct, **deliberately not modified** (§7)
- Disney `.docx` (`Disney_MEO_Class_I_Notes_Corrected_Updated_2026-08-16.docx`) — **not regenerated, not modified**
- Disney JSON companion and the enrichment-candidate JSONs — **not modified** (read as proposal material only)
- Any candidate-note source image — not touched
- The Disney audit — **not reopened**

**Not added, as directed:** nautical-assessor material; zettabyte trivia; EU ETS; Article 297; Article 51(c); Maritime Zones Act 1976; UNCLOS signature or ratification dates; Union List entries 14, 21 or 57; MS Act 2025 as operative at the January 2026 sitting; any asserted replacement benchmark beyond what the CMI's own published text states; any suggestion that a "YAR 2022" edition exists.

**No answer was rewritten for prose quality.** Every edit is traceable to an approved item.

---

## 12. Final pre-commit review (Founder review complete)

Conducted as a separate pass over the finished working tree, treating §§1–11 as claims to verify rather than as established fact.

### 12.1 Changed-file classification — zero `UNEXPECTED`

| Classification | Count | Files |
|---|---|---|
| `CANONICAL_SPEC` | 4 | `specs/QP2403.json`, `specs/QP2510.json`, `specs/QP2601.json`, `specs/QP2606.json` |
| `EXPECTED_GENERATED_ARTIFACT` | 11 | `meoclass1/pastpapers/QP{2403,2510,2601,2606}.html`; `solvedQP/QP{2403,2510,2601,2606}.html`; `SQ/solved-qp-sample-january-2026.html`; `meoclass1/oralnotes/{written-sample,solved-qp}-january-2026*.html` |
| `IMPLEMENTATION_REPORT` | 1 | this file (`docs/` already tracks 73 `.md`, including dated audit reports, so repository convention is to track it) |
| `UNEXPECTED` | **0** | — |

Every generated artifact traces to one of the four authorised canonical changes; the three non-per-paper files all derive from `QP2601` (January 2026).

### 12.2 Canonical specs re-read in full after modification

**`QP2403-Q3` / `QP2510-Q3`** — stale current-LIBOR formulation corrected at every site. Rule XXI(a) verified unaltered: three sites each still read "until three months after the date of issue of the adjustment". The current Rule XXI(b) formulation is internally consistent at every occurrence (7 and 6 `USD Prime Rate` sites respectively). Artificial-GA cross-link resolves. No unrelated general-average content changed. `model_answer` blocks 18 and 19 match a naive `Rule XXI` search only because they contain Rule XX**II** and Rule XX**III** — the interest explanation appears once per answer, so no duplicated Rule XXI passage was introduced.

**Answer length** (model answer, words): `QP2403-Q3` 1,831 → 1,913 (+4.5%); `QP2510-Q3` 1,831 → 1,913 (+4.5%); `QP2606-Q3` 989 → 989 (0%); `QP2601-Q7` 928 → 1,025 (+10.5%). No answer became materially longer or disproportionate; all remain exam-writeable.

**`QP2606-Q3`** — the 1994 position is untouched at all nine sites where it is historically relevant (interest fixed at 7 per cent per annum; Rule XX 2 per cent commission; no time bar). The 2016/2022 position is correct in both the comparison table and the source line. The provenance wording no longer contradicts direct consultation of the CMI text. **No claim about possession or licensing of the YAR 1994 text was introduced** — the revised sentence asserts only that the CMI's published English text of the **2016** Rules was read directly, which this session in fact did.

**`QP2601-Q7`** — the constitutional bridge is a single 97-word, three-sentence paragraph establishing exactly the approved chain and nothing beyond it: UNCLOS obligation → domestic implementation required → Article 253 → Union List Entry 25 → (existing paragraph) central maritime legislation and administration. Automated exclusion check: Article 297, Article 51(c), Maritime Zones Act 1976, UNCLOS signature (1982) and ratification (1995) dates, and Union List entries 14/21/57 are all **absent**. The string "2025 Act" is present only in the pre-existing sentence recording that it *had not commenced* at the January 2026 sitting, so the historical statutory position is unchanged. The reciprocal cross-link reads "the same **subject** at the April 2026 sitting" and names the two respects in which April is broader — it does not describe the questions as identical, and no recurrence metadata was altered.

### 12.3 Rule XXI source traceability — existing structure sufficient, no change made

The corrected proposition is traceable without any new citation mechanism. `QP2403-Q3` and `QP2510-Q3` carry the full basis in `reverify_before_publication[2].why` — issuing body, document (`YAR-2016-English-Version.pdf`), the footnote's own wording, and the retrieval date — with `sources[25]` recording the amendment. `QP2606-Q3` carries it in `sources[4]` and the study-guide provenance note. Verified that no URL or filename reaches any rendered page, so no lengthy source prose entered a candidate answer. **No provenance change was needed and none was made.**

### 12.4 Generated-artifact review

Inspected rather than assumed. All four published paper pages carry `robots: index, follow, max-image-preview:large`; JSON-LD and Open Graph blocks are present. **The diff contains zero `robots`, `ld+json`, `og:` or `twitter:` lines**, which is the positive proof that the earlier no-argument build left no residue — the committed output corresponds to `run_toolchain.py --publish`. Every changed line in the generated files maps to an approved source change (Rule XXI paragraph, study-note line, critical number, route/knowledge-map point, constitutional paragraph, cross-link "Also on the platform" line, depth counter, QP2606 table row and provenance note). The public `/SQ/` page changed by exactly one line — `27 core points` → `28 core points`, deterministically explained by the single added route core point — and contains zero occurrences of the new constitutional or Rule XXI material. The gated oralnotes pages remain behind the established server-side entitlement: `api/_lib/routes.js:38` maps `/meoclass1/oralnotes/` to `ORAL_QB_NOTES`, and no file under `api/` or `middleware.js` was modified.

### 12.5 Final validation

| Check | Result |
|---|---|
| `run_toolchain.py --publish` | **ALL STAGES PASS**, exit 0 |
| Rebuild determinism | No new drift — file set unchanged after re-run |
| Papers / questions | **39 / 351** — unchanged |
| Duplicate question IDs | **0** |
| Cross-links | **720**, unresolved **0** |
| Donor relationships (`reused_from`) | 174, targets missing **0** |
| `git diff --check` | clean, exit 0 |
| Warnings | 521 (509 baseline + 12 `DELIVERY UNSTAGED` for this session's own files; clears on commit) |

**Targeted terminal sweep** over all 39 specs for `ICE LIBOR`, `LIBOR`, `Rule XXI`, `USD Prime`, `four percentage points`, `4 percentage points` and spelled variants:

| Classification | Count |
|---|---|
| `HISTORICAL_AND_CORRECT` | 26 |
| `UNRELATED_CORRECT` | 5 (all `QP2312-Q3`, the YAR **1994** question — 7 per cent, correct) |
| **`STALE`** | **0** |

Zero `STALE` occurrences inside the authorised current-YAR answers, and none anywhere else. No out-of-scope occurrence was modified.

## 13. Status

**IMPLEMENTED — NOT COMMITTED, NOT PUSHED.** Working tree holds the change for Founder review of the diff.

### Follow-up queue — NOT actioned in this commit

**FOLLOW-UP 1 — TRUE-SOURCE GAP.** `F:\miw-true-source\general-average` does not encode the October 2022 Rule XXI technical alteration, and holds no Rule XXI text at all, despite the package sitting at `FOUNDER_REVIEW` with all validation gates passing. Capture the CMI 2016 text and update the instrument and watch registers. **Deliberately excluded from this commit** — separate repository, separate task.

**FOLLOW-UP 2 — QP2606 PROVENANCE / HOLDINGS REVIEW.** Possible pre-existing overstatement of what source editions MIW holds. This session corrected the wording **only** to the extent its own change created a factual contradiction (asserting a rate from the CMI 2016 text while the same paragraph denied holding the Rules). The residual question — whether the YAR **1994** text is likewise held, given `QP2312-Q3`'s `sources[0]` records it as "read in full from a published copy" — is **pre-existing and left untouched**. No unestablished holdings claim was introduced in its place.

**FOLLOW-UP 3 — BUILD SAFETY: ALREADY DOCUMENTED, NO ACTION REQUIRED.** Checked before commit. The hazard is documented clearly and in more than one place: `LAPTOP_REVIEW_AND_INTEGRATION_PROTOCOL.md` §3.M ("`main` commits the **publish** build. `run_toolchain.py --publish` is therefore the pre-commit gate; the bare run is not"), including the mode-symmetry warning and the earlier 37-page `noindex` incident, with `QA_AND_HANDOVER_PROTOCOL.md` §1 repeating and cross-referencing it. **No governance documentation was written or modified.** This item is closed, not queued.
