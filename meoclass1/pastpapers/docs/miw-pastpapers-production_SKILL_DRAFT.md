---
name: miw-pastpapers-production   (PROPOSED — not yet installed as a live skill)
description: >
  Full production, verification, dedup, and correction workflow for the Marine Intelligence Weekly
  MEO Class 1 Engineering Management PAST WRITTEN PAPER model-answer series at
  marineintelligenceweekly.com/meoclass1/pastpapers/. Use this skill whenever Nixon mentions "past
  paper", "full question paper", "written paper answers", "EM-26xx", "dieselship paper", or any task
  involving building complete model answers for an entire official MEO Class 1 written exam sitting.
  Distinct from: miw-qb-production (oral card Q&A), miw-notes-mgmt (page-range topic notes),
  miw-written-qa-production (single-topic deep-dive WA chapters). This series answers EVERY question
  of ONE official exam paper at a time, calibrated to real written-exam length and marks.
status: DRAFT — pending Nixon's review/approval of the open questions in Section 0 before first build.
---

# MIW MEO Class 1 Past Written Papers — Production Skill (DRAFT v0.1)

## 0. Open questions — confirm before/during the first build

These are judgment calls made while planning this series. Flag/confirm rather than silently lock in:

1. **Folder & naming.** Proposed: new top-level folder `meoclass1/pastpapers/`, one file per paper
   named `QP<YYMM>.html` (e.g. `QP2601.html` for Jan 2026), reusing DG Shipping's own official Sr.
   No. scheme rather than inventing a new prefix. [Judgement — confirm you're happy reusing "EM" as
   the file code rather than a MIW-native prefix like "PP".]
2. **Coverage.** Proposed: build model answers for **all 9 questions** in every paper (not just the
   6 a candidate would select), since which 6 a candidate picks isn't fixed and full coverage matches
   how the QB series already works. [Judgement — please confirm.]
3. **Answer length.** No official word/line guidance exists for this platform yet. Section 4 below
   proposes a marks-to-word-count heuristic. This is **[Speculative]** — if you have real graded
   answer booklets or examiner guidance on expected length, that should override my heuristic.
4. **May 2026 paper is missing** from the 6 uploaded PDFs (Jan, Feb, Mar, Apr, Jun, Jul present).
   Confirm whether a May 2026 EM paper exists and should be sourced before the series is "complete
   through July".
5. **`EM-2604-1` and `EM-2606-1`** carry a "-1" suffix in their official Sr. No. that `EM-2601/02/03/07`
   don't have. Unconfirmed whether this indicates a second paper set exists for April/June that hasn't
   been sourced yet, or is just DG Shipping's internal printing/versioning artifact. Worth a quick check
   before treating April/June as "one paper, fully captured."
6. **Toolchain vs. direct HTML for paper #1.** Proposed: build the very first paper (Jan 2026) as
   **direct hand-built HTML** (like the original WA chapters), then extract the JSON-spec + build-script
   toolchain (Section 6) from that real example — mirrors how the notes-mgmt toolchain was built only
   after several hand-built Parts existed. Avoids designing a schema before real content proves it out.

---

## 1. Why this is a new, fourth series (not an extension of an existing one)

| Series | Skill | Unit of content | Format | Manifest |
|---|---|---|---|---|
| QB (oral) | miw-qb-production | Single Q&A card | Short, examiner-pattern tagged | `meoclass1/qb_content_index.json` |
| Oral Notes | miw-notes-mgmt | Page-range chapter | Narrative notes | `meoclass1/oralnotes/notes_content_index.json` |
| Written Answers (WA) | miw-written-qa-production | Single topic, deep-dive | 11-section long-form chapter | `meoclass1/oralnotes/written_content_index.json` |
| **Past Papers (this skill)** | **miw-pastpapers-production** | **One full official exam sitting (9 Qs)** | **Exam-length model answer + study-notes companion, per question** | **`meoclass1/pastpapers/pastpapers_content_index.json` (NEW)** |

The WA series answers *"teach me everything about GHG Strategy"* (one topic, unlimited depth). This
series answers *"here is January 2026's actual paper — show me what I'd write in the exam booklet for
all 9 questions, in the time I actually have."* Different question (exam-realistic, marks-calibrated,
time-boxed) needs a different content shape — hence a new series rather than folding into WA, and a
new manifest rather than overloading `written_content_index.json` (per your instruction — that file is
reserved for the WA topic-chapter series and must not absorb this different content shape).

---

## 2. Source material handling

- Source: the official DG Shipping / Kochi MMD written exam papers, currently sourced via aggregator
  PDFs (dieselship.com "EM" series). The **exam questions themselves are official government exam
  content**, not the aggregator's creative work — reproducing the verbatim question text is standard,
  necessary exam-prep practice (the WA skill already does this for its primary question per chapter).
- **Do not reproduce** the aggregator's own marketing copy, watermark text, or the "recurrence index"
  presentation style — only the underlying factual data (which prior sittings a question repeated in)
  is used, restated in MIW's own format.
- Each paper PDF also carries a small **recurrence table** under most questions (e.g. `2023/MAR/Q8
  2024/JAN/Q5 2026/JUL/Q3`) — this is high-value metadata: it tells you which questions are frequently
  repeated "favourites" vs. one-off. Capture this in the JSON spec (`recurrence` array) — it drives the
  dedup workflow in Section 3.

---

## 3. Dedup-first workflow (the core efficiency mechanism)

Given how often these questions repeat verbatim or near-verbatim across sittings — and how much
regulatory ground is *already* covered by the QB and WA series — **never draft a question cold without
checking for reusable content first.** Classify every question into one of four reuse tiers before
writing anything:

| Tier | Condition | Action |
|---|---|---|
| **A — Direct reuse** | An existing WA chapter already deep-dives this exact question (e.g. Mar/Q9 "Hong Kong Convention" ↔ `WA1-HKC1`) | Write a **condensed, exam-length** answer derived from the WA content (not copy-pasted), tailored to this paper's exact wording/marks. Add a "Full deep-dive: WA1-HKC" cross-link box. Do not duplicate the WA chapter's full content here. |
| **B — Partial overlap** | QB cards cover pieces of the topic but the written question needs broader synthesis (e.g. PSC detention + right of appeal spans several QB cards) | Build a fresh synthesized paragraph answer; QB's short oral-card format doesn't translate directly, but its verified facts/citations do. |
| **C — New topic** | Nothing on the platform covers this yet (e.g. Jan/Q1, low-speed 2-stroke operation drawbacks) | Build from scratch per the Section 5 verification standard. |
| **D — Recurring instance** | This exact question already has a **built pastpapers answer** in an earlier paper (e.g. `2023/DEC/Q1 2026/JUN/Q1`) | **Reuse the existing verified answer wholesale.** Light re-verification only (has anything regulatory changed since it was last verified?). Note "recurs from EM2312 — re-verified <date>" in the verify-box. Never redraft from scratch. |

This tiering is the direct answer to "volume will keep growing" — without it, every new monthly paper
would re-derive answers to the same ~20–30 evergreen questions (GA, PSC, FSA, ISM, UNCLOS, biofouling,
etc.) that already recur almost every sitting.

**Practical dedup check per paper**, before drafting:
1. Pull `recurrence` tags straight from the source PDF for every question.
2. Grep `pastpapers_content_index.json` for any of those recurrence codes already marked `Built`.
3. Grep `written_content_index.json` and `qb_content_index.json` topic tags for keyword overlap with
   this question's subject.
4. Tag each question A/B/C/D in the JSON spec before writing a single word of answer content.

---

## 4. Answer format per question

Each question gets **two stacked blocks**, clearly separated so a candidate can tell "what I'd actually
write" from "what I should understand more deeply":

1. **Model Written Answer** — exam-realistic, marks-calibrated, structured the way a candidate would
   actually pen it in the answer booklet (sub-headers for multi-part questions, not a sprawling essay).
2. **Study Notes** — a compact companion box (not a full WA-style 11-section chapter) covering: why it
   works, common mistakes/examiner traps, one CE Oral Tip, and regulation references. This is where
   your MEO Class 1 teaching-style preferences (why it exists, why alternatives fail, examiner
   follow-ups, memory aids) live — kept visually distinct so it doesn't bloat the "what to actually
   write" answer above it.

**Length calibration — [Speculative], override if you have better data:**

| Marks | Target length | Structural note |
|---|---|---|
| 4 | 60–90 words | one short paragraph or 3–4 bullets |
| 5 | 80–110 words | one paragraph |
| 6 | 90–130 words | one paragraph or short list |
| 8 | 150–200 words | 2 short paragraphs / labelled sub-points |
| 10 | 180–240 words | 2–3 sub-headers |
| 16 | 320–420 words | full structured answer, sub-header per sub-part, table/ASCII diagram where it naturally helps |

Heuristic basis: 3 hours ÷ 6 questions ≈ 30 min/question including reading and structuring time, at a
realistic sustained handwriting pace. This should be recalibrated against real graded scripts if you
have access to any.

---

## 5. Regulatory verification standard

**Identical to the WA series standard (miw-written-qa-production Section 5) — reused wholesale, not
reinvented:**
- Verify every regulation/resolution number and consequential figure against a primary source before
  publishing.
- State the current legal stage explicitly (proposed → approved → adopted → in force) for any
  instrument that isn't fully in force yet — several of these papers touch fast-moving items (Merchant
  Shipping Act 2025/DGMA, IMO Net-Zero Framework/GFI, EU ETS) where "in force" framing goes stale fast.
- Cross-check consequential numbers against ≥2 independent sources; flag disagreement rather than
  silently picking one.
- Drop unverifiable figures rather than presenting them as fact.
- Source hierarchy: IMO primary > class societies > DG Shipping/DGMA > ISO > P&I/maritime law firms >
  general trade press.

---

## 6. File architecture

**Folder:** `meoclass1/pastpapers/` (new, sibling to `meoclass1/oralnotes/`)

**File per paper:** `QP<YYMM>.html` — e.g. `QP2601.html`. All 9 questions live in one file (anchored
`#q1`…`#q9`) unless a paper genuinely oversizes past ~150–200KB, in which case split PartA/PartB by
size (same convention as oversized QB files) — do not split by default.

**Manifest (NEW):** `meoclass1/pastpapers/pastpapers_content_index.json` — the authoritative index for
this series, separate from `qb_content_index.json` and `written_content_index.json` per your
instruction. Proposed schema:

```json
{
  "generated": "",
  "generated_by": "",
  "papers": [
    {
      "paper_id": "QP2601",
      "sr_no": "EM-2601",
      "month": "January 2026",
      "source_pdf": "01_-_JANUARY_-_2026.pdf",
      "file": "meoclass1/pastpapers/QP2601.html",
      "total_marks": 100,
      "build_status": "Not Started",
      "questions": [
        {
          "q_no": "Q1",
          "marks": null,
          "topic_tags": ["GHG", "low-speed operation", "two-stroke ME"],
          "recurrence": ["2026/JAN/Q1"],
          "reuse_tier": "C",
          "cross_ref": null,
          "status": "Not Built"
        }
      ]
    }
  ]
}
```

**Manifest path registration:** add `PASTPAPERS_MANIFEST` / `PASTPAPERS_MANIFEST_REL` constants to the
**existing** `tools/notes/miw_paths.py` (already the established single source of truth across QB/WA/
Notes manifests) rather than creating a second paths module — new pastpapers tooling imports from it,
same pattern as `audit_master_index.py`/`match_qb.py`. Register it with `assert_no_legacy_manifest()`
too, so the July duplicate-manifest mistake can't repeat for this series.

**Toolchain (build after paper #1 is hand-built — see Section 0.6):** `tools/pastpapers/`
- `build_paper.py` — JSON content spec → HTML (mirrors `build_part.py`; Claude authors content, never
  hand-writes markup once this exists).
- `validate_spec.py` — schema check before build.
- `dedup_scan.py` — new: runs the Section 3 tiering check against QB/WA/pastpapers manifests, outputs a
  reuse report before drafting starts.
- Health check: **extend `qb_health_check.py`** to also scan `meoclass1/pastpapers/` (tag balance,
  manifest↔disk sync) rather than standing up a second daily email — one consolidated health report.

---

## 7. Page structure (per question, inside the paper file)

```
<head>  — GA4, robots noindex, canonical, OG tags, FAQPage JSON-LD (question text only), inline <style>
          (copy design tokens from an existing WA file — --teal/--navy/--orange, Georgia serif body,
          Segoe UI chrome — same visual family as QB/WA/Notes)
<body>
  gate script (or stripped-for-review comment, per standard workflow)
  .topbar / .page-header — badge "PP · Engineering Management · EM-2601" | paper title | header-meta
  .main
    .verify-box   — paper-level verification note (what was checked, reuse tiers applied, corrections)
    NB block      — official exam instructions (answer 6 of 9, marks, time allowed) reproduced concisely
    per question (Q1…Q9), each:
      .exam-q       — verbatim question text + marks + recurrence badge (with cross-links if a prior
                      sitting's answer already exists on the platform)
      .model-answer — Section 4's exam-length model answer
      .study-notes  — Section 4's companion box (why/traps/CE tip/regs)
      .reg-box      — citations for this question
    .verify-box   — Reference Sources
    .q-footer     — correction email + version tag
  .page-footer
</body>
```

Content-protection stack, gate script, and SEO rules are identical to every other gated MIW file — no
changes needed there.

---

## 8. Site integration

- **Does not touch** `meoclass1/oralnotes/notes_content_index.json` or its `index.html` — confirmed per
  your instruction.
- Needs its own `meoclass1/pastpapers/index.html` (paper list, newest first, build-status per paper) and
  a new card/section on the MEO Class 1 hub/landing page (verify the exact filename against the live
  repo — likely `meoclass1/index.html`, distinct from `examiner-index.html` which is QB-examiner-pattern
  specific and doesn't apply here since written papers are set centrally by DG Shipping, not by
  individual oral examiners).
- No examiner-pattern tagging for this series (Nair/Simon/Rajappan/etc. patterns are an *oral* exam
  concept — written papers are uniform nationally).

---

## 9. Production workflow (one paper, start to finish)

1. **Environment check** (per miw-correction-workflow Section 0) — confirm Desktop Commander + GitHub
   MCP availability before assuming local-clone/push access. *(Not available in this planning chat —
   run actual builds from a session with both connected, e.g. Claude Desktop/Code.)*
2. **Source intake** — extract all 9 questions + recurrence tags from the source PDF into the JSON spec
   skeleton.
3. **Dedup scan** (Section 3) — tier every question A–D before drafting anything.
4. **Draft** — Tier C/new questions drafted fresh (Gemini draft → Claude verify, for batches of 3+,
   matching the QB two-tool pipeline; smaller batches direct in Claude). Tier A/B condensed from
   existing content. Tier D reused with light re-verification.
5. **Verification pass** — Section 5 standard, web-search every citation.
6. **Build HTML** — Section 7 structure, gate stripped, review comment in its place.
7. **Health check** — tag balance, manifest-valid JSON, FAQPage JSON-LD present.
8. **Present ungated review copy** to Nixon.
9. **Revise per feedback.**
10. **Gate** — canonical script:
    `<script>if(!/miw_auth=1/.test(document.cookie)){window.location.replace("/SQ/pay.html");}</script>`
11. **Update `pastpapers_content_index.json`** — mark each question Built, set `reuse_tier`/`cross_ref`.
12. **Update `pastpapers/index.html`** and the MEO Class 1 hub page.
13. **Commit** (stage files explicitly, not `git add .`) **and push** to `origin/main`.
14. **Cache-busted live verification** against `raw.githubusercontent.com`.
15. **known_traps.md** — no new file needed; this series' corrections use the existing shared file, just
    tagged with `meoclass1/pastpapers/QP<YYMM>.html` paths like any other correction.

---

## 10. Known open items

- Toolchain (Section 6) not yet built — planned to follow the first hand-built paper (see Section 0.6).
- `pastpapers/index.html` and hub-page integration not yet built.
- May 2026 paper not yet sourced (Section 0.4).
- April/June "-1" Sr. No. suffix unresolved (Section 0.5).


---
---

# ANNOTATIONS FROM THE QP2607 BUILD (2026-08-07 / 08)

> **Status: still a DRAFT.** These annotations record what the first real production run validated,
> corrected or superseded. They are not a licence to automate. The skill becomes
> `miw-pastpapers-production_SKILL.md` only after the complete QP2607 paper passes Founder review.

## Z. THE PRODUCTION ORDER (supersedes any earlier ordering in this draft)

```
1  verified source research            primary sources; provenance class per claim
2  verified Model Answer               the three-layer test
3  answer_route                        ONE canonical numbered sequence, 5-9 steps
4  derived learning aids               map, recall, exam plan, cards, cheat sheet
5  SEMANTIC REGRESSION REVIEW          <-- mandatory gate, see below
6  reference-object mapping            ONLY where a corpus object already exists
7  deterministic build                 run_toolchain.py --self-test
8  known traps / health                positive-controlled
9  human Founder review
```

### Step 5 is a gate, not a formality

Derived aids are written from the answer, and the recurring failure is that they come out
**more categorical than the answer**. Before building, re-read every derived field against
its source and confirm scope, conditions, uncertainty, jurisdiction, applicability and
regulatory status all survived. `SEMANTIC_GUARDS` in `validate_spec.py` catches known
patterns; it is not a substitute for reading. See `MIW_LEARNING_METHOD_DESIGN.md` §3a.

### Step 6: absence of a corpus object is a normal outcome

**Never invent a corpus object id.** If no verified object exists for a claim, leave
`reference_shelf` absent, or record the entry with `state: NO_CORPUS_OBJECT_YET`. A question
with no shelf is valid and builds cleanly. Questions and corpus objects are produced on
parallel tracks, and a fabricated reference is worse than a missing one because it looks
authoritative. Never copy regulation text into a question spec, and never reference a PDF
page — `validate_spec.py` fails the build on both. See `MIW_TRUE_SOURCE_CONTRACT.md`.

### One primary category per question

Assign exactly one `primary_category` from the topic tree; the topic page renders each
question once, under it. `subject_tags` remain the searchable secondary tags.

## A. Superseded assumptions

| Draft said | Superseded by | Why |
|---|---|---|
| §0.6 — hand-build paper #1 in HTML, extract the toolchain afterwards | Spec → validate → render → audit from the start | The notes-series toolchain already proved the pattern. Hand-building first would have produced a page nobody could regenerate. |
| §3 Tier D — "reuse the existing verified answer wholesale" | Tier D never permits wholesale copying; record wording, marks, jurisdictional and regulatory deltas and adapt | Recurrence metadata is not evidence of semantic equivalence. |
| §4 length table (16 marks = 320–420 words) | 16 marks = 450–650 words, banded on **total** marks | The draft's own table was internally inconsistent: two 8-mark bands summed to 360–560, against 450–650 for a single 16. Writing time scales with what the question is worth, not with how the examiner split it. |
| §9 — requires Desktop Commander and GitHub MCP | Direct filesystem access is sufficient | Environment-specific assumption. |
| §2 — source described as "official DG Shipping papers sourced via aggregator" | Printed authority and actual local provenance recorded **separately**; `official_source_verified: false` | The held PDF is an aggregator copy. Calling it official would be a provenance claim we cannot support. |

## B. Third-party coaching notes — STANDING RULE

`Notes-for-written-answers/` contains **45 PDFs, 767 pages, of HATC coaching handouts** in two sets: a
machine-readable *Additional Set October 2024* (325 pages) and an image-only *June 2025* set with no
text layer.

**Every one of the 325 machine-readable pages carries the publisher's own line:**

> *"Certain statements/figures have been intentionally made wrong; same will be corrected in class."*

Occurrence count verified: **325 / 325**.

**The rule, which is not negotiable:**

- These notes **may** be used for topic discovery and question-scope evidence — the June 2025 set is
  organised *by past-paper question*, which makes it a useful question→topic map.
- They **must not** be treated as factual authority.
- They **must not** be used as verification for any claim.
- They **must not** be reproduced into MIW output — they are watermarked third-party copyright.
- **Every factual statement taken from them is untrusted input** and must independently survive
  authoritative verification before appearing anywhere in MIW.

Observed in practice: the HATC FSA page mis-names FSA Step 2 as "assessment of risks" against the
instrument's actual "Risk Analysis". That is exactly the class of plausible, memorable error the
disclaimer warns about.

One exception in that folder: `DOC-20251125-WA0009.pdf` is genuinely **IRS Guidelines on Ballast Water
Management 2018 (IRS-G-ENV-01)** — real classification-society material, and citable.

## C. Answer philosophy — the three-layer test

The pilot's failure mode was not carelessness. It was **impressive material crowding out examinable
material**. Q1(a) traded application marks for a methodological aside; Q2 elevated a CLC/Bunkers
distinction to headline status and stated it backwards. In both cases the research was good and the
*placement* was wrong.

- **Layer 1 — Examiner requirement.** What must be written to score.
- **Layer 2 — Correct technical / regulatory basis.** Why it is true.
- **Layer 3 — Study intelligence.** Traps, oral follow-ups, cross-links, deeper reasoning.

**Model answer = Layer 1 + only the Layer 2 needed to make it correct. Study notes = the rest.**

A production agent optimising for apparent sophistication will reliably produce lower-scoring answers
than one optimising for the marking scheme.

## D. The decomposition gate — mandatory before research

No question may be researched or drafted until `decomposition_gate` is complete in the spec
(schema 1.1). `validate_spec.py` raises an ERROR on a built answer with no gate. Fields:
`question_intent`, `mark_allocation`, `examiner_expectation`, `primary_source_plan`,
`freshness_risk`, `jurisdiction_risk`, `technical_ambiguities`, `target_answer_shape`. Command verbs,
required components and the internal reuse map live in the existing `command_verbs`, `decomposition`
and `reuse_evidence` fields and are deliberately **not** duplicated in the gate.

## E. Provenance classes — per claim, not per question

`verification_status` alone was too coarse: both Critical red-team findings (RT-07, RT-08) sat inside
questions marked simply "Verified". Schema 1.1 adds `provenance_summary` (counts by class) and
`reverify_before_publication` (an explicit list). Classes:

`P1_PRIMARY_VERIFIED` · `P2_AUTHORITATIVE_SECONDARY` · `P3_INDUSTRY_GUIDANCE` ·
`INTERNAL_REUSE_VERIFIED` · `ENGINEERING_JUDGEMENT` · `UNRESOLVED` · `TIME_SENSITIVE_REVERIFY`

This is deliberately **not** a citation database. Per-claim detail lives in the human-readable
`verification/<paper>/Q<n>.md` records. The JSON answers only two questions: *which claims need
re-verification before publication*, and *which came from internal reuse versus external research*.

## F. AGENT_LESSONS

Reusable rules extracted from real work on QP2607. Each was paid for by an actual defect.

1. **Answer the grammatical object of the question.** "Application of X to Y" puts the marks in the
   applying. A correct-but-off-axis insight is still off-axis. *(RT-01)*
2. **Tag-level dedup is unsafe. Read the matched content.** The corpus taught iron ore *fines*; the
   question asked about *pellets*. Tags said "covered".
3. **A memorable simplification is a defect vector.** Red-team the crisp "X versus Y" teaching point
   before publishing — that is exactly what candidates memorise. The pilot's own headline insight
   (fines = A, pellets = C) was itself an oversimplification. *(RT-03)*
4. **Corroboration is not primary verification.** Two secondary sources agreeing is worth recording,
   never launderable into a primary citation. Where the primary text is unobtainable, lean the answer
   on the verifiable *procedure*, not the unverifiable *value*. *(RT-02)*
5. **Read the definition article before using a defined term.** Conventions define terms
   counter-intuitively. Where an instrument has both a liability article and an insurance article,
   assume they address different persons until proven otherwise. *(RT-07 — Critical)*
6. **Where two regimes are mutually exclusive, check the exclusion clause and both scope
   definitions.** *(RT-08 — Critical)*
7. **Check the trigger, not just the instrument.** Verify the scenario meets the instrument's own
   definitional threshold before citing it as engaged. *(RT-06)*
8. **When the scenario is silent on a fact that decides the answer, be conditional and say why.**
   Inventing the missing fact is an error; silently picking a branch is the same error.
9. **Jurisdiction is determined before drafting, not during.** The corpus itself carried a wrong-
   jurisdiction citation (QB9_C attributes marine insurance principles to the UK 1906 Act in an Indian
   exam context). Internal reuse must be jurisdiction-screened.
10. **Register-tag every imperative and every consequential sentence.** Law / guideline / club
    practice / engineering judgement. Un-sourced imperatives placed near citations inherit unearned
    authority.
11. **Enforcement practice is not law, and it is jurisdictional.** Keep it in study notes, labelled.
12. **Regulatory-stage checking is mandatory for emerging fuels and new legislation.** State adoption,
    entry into force and any grace period separately. Never describe interim guidance as a mandatory
    Code amendment.
13. **Absence of a primary source must create an UNRESOLVED state, never an invented answer.** Q7 cites
    no section numbers because the statutory text could not be retrieved. That is the correct outcome.
14. **Measurement instruments must cover every content type.** The word counter ignored table cells, so
    a 735-word answer measured as 492. A metric that silently skips a content type manufactures false
    confidence — worse than no metric.
15. **Never patch a block array by index. Rebuild it.** Index-patching caused two defects in one
    session: a `p` added beside an existing `ul` (which the renderer would silently resolve in favour
    of one, dropping the other), and a wrong-index assignment that clobbered a different section.
    `validate_spec.py` now errors on any block carrying more than one content key.
16. **A safety check that never fires is worse than none.** Positive-control the auditor: inject the
    fault and confirm it fails. The path-leak detector was verified this way.
17. **Generated HTML is never the source of truth.** The spec is authoritative; the page is rendered
    and must be byte-reproducible from it.
18. **Model answer and study intelligence stay separated.** See section C.

## G. What the toolchain now enforces

`validate_spec.py` — schema completeness, marks arithmetic within each question, id/anchor uniqueness,
provenance honesty on the source copy, the answer/verification state machine, **decomposition gate
present before any built answer**, **provenance summary present**, **exactly one content key per
block**, word counts against the marks band (WARN only), and a printed list of every claim flagged for
re-verification.

`audit_paper.py` — 13 brief-mandated checks plus a filesystem-path leak detector, all positive-
controlled.

`build_paper.py` — deterministic: no clock reading, no random value, no absolute path. CSS is lifted
verbatim from a live reference file by `extract_shell.py` and never retyped.
