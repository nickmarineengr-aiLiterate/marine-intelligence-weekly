# MIW Production Agents — Part N Current-State Assessment (v1)

**Status:** Assessment only. No implementation performed. No `.claude/agents/*.md` created. No Uday chapters regenerated. No QB backlog processed.
**Date:** 2026-08-05
**Scope:** Answers the 15 numbered items in `docs/agent-build/Brief_v1.md` ("Immediate first task (Part N)") and Part A/Part N of `docs/agent-build/Prompt.txt`.
**Repository:** `marine-intelligence-weekly`, branch `main`, HEAD `8bee774` at time of inspection. Verified via `git remote -v` — this is **not** RulesApp.
**Method:** Direct filesystem inspection of `F:\Marine-Intelligence-Weekly`, plus the out-of-repository source directories the workflow actually depends on. Every claim below is evidenced by a file, a byte count, or a command output — not inferred from conversation history.

---

## 0. Executive summary

Three findings dominate everything else in this document:

1. **The MIW project has almost no Python.** There is exactly **one** program in the repository — `meoclass1/qb_health_check.py`, 945 lines. It is genuinely good, and it is a validator, not a production engine. The brief's phrase "the Python programs and local tooling already built in the MIW project" overstates what exists: there is one validator, three JSON manifests, and nothing else. **The Level 1 execution engine has to be built, not extended.** This is the single biggest correction to the brief's premise.

2. **Uday transcription cannot be Level 1 work.** `Uday notesPDF-compressed.pdf` is 768 pages, every one a scanned image. Text extraction returns 1–3 characters per page (the printed page-number stamp only). Tesseract is installed (`C:\Program Files\Tesseract-OCR\tesseract`) but is not reliable on continuous handwriting. **A vision-model call per page is unavoidable.** Token savings in the Notes pipeline must therefore come from the build, validation and revision stages — not from transcription.

3. **There is currently no raw-transcription layer at all, anywhere.** The existing workflow's Gemini output files (`MIW notes pages 451-475.txt` and siblings) are **not transcriptions** — they are fully expanded, ~90 KB publication-style chapter drafts that jump straight from source page to Part D layer 5. Layers 2–4 of the required 7-layer model have never existed for any published Part. This is the concrete defect the new pipeline exists to fix, and it is also why Parts 1–18 cannot be retrospectively given page-level provenance.

---

## 1. Current-state assessment

### 1.1 Python programs

| File | Lines | Purpose | State |
|---|---|---|---|
| `meoclass1/qb_health_check.py` | 945 | Structural + regulatory-safety validator for QB, `oralnotes/`, and `SQ/` HTML | Mature, in production, run daily by CI |

That is the complete inventory. No other `.py` file exists in the repository. `F:\MIW-Production-Toolkit` exists as an **empty directory** — a stub, containing nothing.

`qb_health_check.py` implements, deterministically and with no AI:

- stack-based HTML tag-balance checking (void-element and `<script>`/`<style>` aware)
- mandatory block presence per question card (`reg-box`, `ce-tip`, `q-footer`)
- `q-card` id sequence: duplicates and internal gaps
- TOC-anchor ↔ card-id bidirectional integrity
- GA4 tag and robots-meta presence
- pipe-delimited markdown table leakage detection
- unrendered-LaTeX detection (`\frac`, `$...$`, `GM_{0}` forms) — the site has no MathJax
- `<img>` integrity: missing src/alt, `data:`/`blob:`/`file://`/localhost leftovers, relative paths, and asset-existence checks against the repo snapshot
- known-traps scanning with **negation-context awareness** (a trap phrase inside a "superseded by…" sentence is downgraded to `[REVIEW]`, not flagged as a resurfaced error)
- QB manifest ↔ disk cross-check in both directions, plus question-count drift and changelog-completeness gaps
- notes topic-block ↔ topic-footer count matching and topic-id sequencing
- notes auth-gate presence check (full paywall robots signature without `miw_auth=1`)
- `SQ/` free-sample divergence detection (>15% size drift from the `meoclass1/` original)

**Critical operational limitation:** `fetch_repo_tarball()` downloads `codeload.github.com/.../main` — it validates **what is already published on GitHub**, never the local working tree. It therefore cannot gate a batch *before* commit. That is a small fix and a large architectural consequence (see §11, PKG-A1).

### 1.2 Skills

In-repository:

| File | Type |
|---|---|
| `Claude skill/miw-correction-workflow_SKILL.md` | The only skill file committed anywhere near the repo — and `Claude skill/` is **untracked** (`git status` shows `?? "Claude skill/"`) |

The other six files in `Claude skill/` are governance duplicates of `reports/governance/` content, already flagged by `AI_SESSION_START.md` §3.

**`miw-qb-production_SKILL_v3.md` and `miw-notes-mgmt_SKILL.md` do not exist in this repository.**

### 1.3 Skill-porting status — Adaptation Note 5, resolved

The brief asked whether the Claude.ai project skills are installed for Claude Code, or need copying into `.claude/skills/`. Verified answer:

- The skills **are reachable from Claude Code**, exposed in the `anthropic-skills:` namespace: `miw-qb-production`, `miw-production`, `marine-intelligence-weekly`, `miw-archive`, `miw-ecosystem`, `miw-timeline`, `miw-ghgdecarb-timeline`. They resolve and invoke.
- They are **not on local disk**. `C:\Users\User\.claude\plugins\cache\` contains only `claude-plugins-official` marketplace plugins; a filesystem search for `*miw*` under `C:\Users\User\.claude` returns nothing. There is no `C:\Users\User\.claude\skills\` directory and no `.claude/` directory in the MIW repository at all.

So the porting question has a more useful answer than "yes" or "no": **no copy is needed for Claude to use them, but a copy is needed for anything else to.** They are account-synced, not repository-versioned, which means:

- they are not in git history, so a change to the QB answer standard leaves no reviewable diff;
- they cannot be read by deterministic Python, so the Level 1 builder cannot be driven from the same source of truth Claude reads;
- `docs/ENGINEERING_PRINCIPLES.md` P1 (Repository First) and P7 (Repository Independence) are both violated by the current arrangement — a human with no AI access cannot read the QB production standard.

**Recommendation:** export `miw-qb-production` and `miw-notes-mgmt` to `skills/` in the repository (a directory already in the frozen architecture), and treat the account-synced copies as mirrors of the committed files. This is a prerequisite for the Level 1 builder, not an optional tidy-up.

### 1.4 Templates, schemas, validators

- **`templates/`** — does not exist. Frozen in the architecture, never built.
- **Schemas** — no JSON Schema files exist. The three manifests have de-facto shapes, never formally specified.
- **Validators** — `qb_health_check.py` only.
- **The MIW Notes chapter standard is not in the repository.** It lives outside, in `F:\1111my course videos\meoclass1\handwritten notes to convert\`, as four plain-text files: `uday notes master template plan.txt` (a 30-section master template), `MIW_Style_Guide.txt` (a 10-section order that **contradicts** the 30-section plan), `MIW_IMO_Citation_Guide.txt`, `MIW_Diagram_and_Flowchart_Guide.txt`, and `MIW notes master prompt for Gemini.txt` (an 11-section compulsory structure — a **third** conflicting section list).

That three-way conflict between the 30-section plan, the 10-section style guide, and the 11-section Gemini prompt is unresolved, undocumented, and currently arbitrated only by whatever the published HTML happens to do. Part E of the prompt says the repository standard takes precedence — but there is no repository standard to take precedence.

### 1.5 Manifests and state files

| File | Contents | Role |
|---|---|---|
| `meoclass1/qb_content_index.json` | 91 files, 683 questions, per-file `qb_group`/`letter`/`title`/`version`/`tags`/`question_count`/`questions[]`/`corrections_applied[]`, plus a `recently_updated[]` changelog | De-facto QB corpus database — **the most valuable existing asset for the QB agent** |
| `meoclass1/oralnotes/notes_content_index.json` | 27 files across 3 series; per-file `part`/`page_range`/`topic_count`/`topics[]`/`summary`/`status`/`last_verified`/`gating_note` | Notes manifest, **authoritative** (contains Parts 17–18) |
| `meoclass1/oralnotes/notes-content-index.json` | Same shape, stops at Part 16 | **Stale duplicate.** PKG-1.8's unresolved issue, confirmed still open |
| `meoclass1/oralnotes/written_content_index.json` | 3 WA series | WA written-answer series |
| `meoclass1/known_traps.md` | 306 lines, 24 numbered entries, 24 `GREP:` lines (some `SKIP`) | Standing-corrections reference, machine-readable by design |
| `corrections/README.md`, `corrections/TEMPLATE.md` | Ledger format standard (PKG-11a) | **Correction record schema already exists** — Part J deliverable #9 is largely satisfied |
| `production-system/verification/` | 3 MSA-2025 rebasing artifacts (ledger JSON, crosswalk MD, pipeline export JSON) | One-off; evidence a pipeline-export pattern has been used before |

I diffed the two notes manifests directly: `notes_content_index.json` is a strict superset (adds Parts 17 and 18, `total_files` 27 vs 26, updated status line). The stale one is safe to delete — **but that is a Founder decision, and it must be made before any Python is allowed to write to a notes manifest**, or the tool will eventually write to the wrong file.

### 1.6 Workflow state, queues, agent definitions

**None exist.** No state file, no queue file, no `.claude/` directory, no agent definitions, no hooks, no settings, no `CLAUDE.md`. Part G's resumability requirement is currently met by nothing at all — resumption today depends entirely on chat memory and `AI_SESSION_START.md`'s prose.

### 1.7 Source material — all of it is outside the repository

| Source | Location | Notes |
|---|---|---|
| Uday handwritten notes (master) | `F:\1111my course videos\meoclass1\handwritten notes to convert\Uday notesPDF-compressed.pdf` | 768 pages, 61.9 MB, **image-only** |
| Uday notes (pre-split) | `…\Uday notesPDF-compressed\` | 55 PDFs, 5 pages each, covering PDF pages 501–768 |
| Gemini chapter drafts, unbuilt | `…\MIW notes pages 451-475.txt`, `476-500`, `501-525`, `526-550` | 282 KB total — **pages 451–550 already drafted but never built into Parts** |
| Gemini chapter drafts, built | `…\MIW notes completed\` | Parts 1–18 source drafts plus 7 correction files |
| QB source batches | `F:\1111my course videos\meoclass1\nw Qs from whatsapp.txt`, `new whatsapp questions July end .txt` | 20 KB total |
| QB true-source corpus | `F:\RulesApp-Local-Input\true-source\` | Referenced by `qb_content_index.json` as the verification corpus |

All of it sits on unversioned paths, one of which contains spaces and a non-descriptive name (`1111my course videos`). Nothing about the current arrangement is reproducible from the repository alone.

### 1.8 The Uday backlog, quantified

`notes_content_index.json` gives exact coverage: Parts 1–18 cover pages **1–450 of 768**.

- **Remaining: pages 451–768 = 318 pages ≈ 13 further Parts (19–31)** at the established 25-pages-per-Part cadence.
- Pages 451–550 already have Gemini drafts sitting unbuilt (4 Parts' worth).
- Pages 501–768 already exist as 5-page split PDFs (55 files) — a page-batching step that does not need rebuilding.

### 1.9 Two source-fidelity defects found during inspection

**(a) A 6-page numbering offset.** PDF page 501 carries the printed stamp `495`; page 551 → `545`; page 768 → `762`. Page 1 → `1`. The offset is constant at 6 through the body of the document. The split-PDF filenames (`501-505.pdf`) use **PDF page index**; the stamps inside them read `495`–`499`. The manifest's `"page_range": "401-425 of 768"` does not state which numbering it uses. Until this is resolved, no page-level provenance claim in the new pipeline is trustworthy.

**(b) The Gemini output is not a transcription.** `MIW notes pages 451-475.txt` opens with `# Chapter 1: General Average Principles…` and proceeds through fully written Definition/Importance/Historical Background/Regulatory References sections with LaTeX formulas. It contains no verbatim source text, no page markers, and no uncertainty flags. Every technical claim in it is Gemini's expansion, structurally indistinguishable from Uday's original note. There is no artifact anywhere from which the original handwriting could be recovered short of re-reading the PDF.

Two consequences worth stating plainly: Part D's layers 2–4 have never existed; and the LaTeX in that output is directly incompatible with the site (`check_formula_rendering` in the health checker flags it), so every Gemini draft carries a guaranteed conversion cost.

### 1.10 Toolchain readiness

Python 3.14.0. `pypdf` 6.9.1, `PyMuPDF` 1.28.0, `pdfplumber`, `beautifulsoup4`, `html5lib` all present. Tesseract installed but not wrapped (`pytesseract` absent). **No new dependencies are required for anything proposed below.**

### 1.11 Governance state (bears directly on what may be built)

Per `AI_SESSION_START.md` and `REPOSITORY_STATUS.md`, both verified current:

- Frozen top-level structure: `docs/`, `skills/`, `templates/`, `reports/`, `corrections/`, `tools/` (incl. `tools/_lib/`) + existing content dirs. `skills/`, `templates/`, `tools/` are **approved but unbuilt** — creating them needs no ADR, only a package that genuinely needs them.
- **`.claude/` is not in the frozen structure.** Rule 4 of `AI_SESSION_START.md` §10 prohibits adding a top-level directory without a new ADR. Creating `.claude/agents/` and `.claude/hooks/` therefore requires a Founder ruling or ADR **before** Adaptation Notes 2 and 4 can be implemented. See §14, blocker B5.
- `docs/ENGINEERING_PRINCIPLES.md` is **Draft v0.2, not Approved**; six reserved ADRs are undrafted. The Governance Gate checks every package against "Principles and relevant ADRs" as a pair.
- The 8-stage package lifecycle is binding and may not be skipped or merged.
- Commit and push require explicit, session-level Founder authorization every time.

---

## 2. Existing components reusable unchanged

| Component | Why it survives untouched |
|---|---|
| `known_traps.md` + its `GREP:` convention | Already a machine-readable rules file with a deliberate manual/automatic split. The Level 1 engine consumes it as-is. |
| `corrections/README.md` + `TEMPLATE.md` | The correction/amendment record schema (Part J #9) already exists and is binding. Reuse verbatim; do not invent a parallel format. |
| `check_tag_balance`, `check_ga4_tag`, `check_robots_meta`, `check_pipe_table_format`, `check_formula_rendering`, `check_image_rendering`, `check_known_traps`, `check_q_id_sequence`, `check_toc_anchors`, `check_mandatory_block_counts`, `check_topic_block_counts`, `check_topic_id_sequence`, `check_notes_gate` | Thirteen deterministic validators, already debugged against real production failures. They move to `tools/_lib/` unchanged and are imported by both the CI path and the new local path. |
| `qb_content_index.json` shape | Already carries per-question text and per-file correction history. This is the QB corpus database; extend it, do not replace it. |
| `notes_content_index.json` shape | Same, for Notes. |
| The 5-page split PDFs (pages 501–768) | Page batching for two-thirds of the backlog is already done. |
| `.github/workflows/qb-health-check.yml` | Daily published-state check stays exactly as it is. The new local gate is additive. |
| The 8-stage lifecycle, `corrections/` classification, severity scale | Process reuse. No new governance is proposed by this assessment. |

**Requires modification, not replacement:** `qb_health_check.py` — add a local filesystem source alongside the tarball fetch, and split the check functions into an importable library. No check logic changes.

**Genuinely new:** everything in the Level 1 execution engine (intake parsers, dedup, scaffold builders, state machine, packet builders, diff/patch tooling), the JSON schemas, the repository copy of the QB and Notes production standards, test fixtures and tests.

---

## 3. Token-heavy steps in the present QB workflow

Measured, not estimated: the 86 QB question files total **8.13 MB ≈ 2.03 M tokens**. `QB2_A.html` alone is 354,921 bytes ≈ **89 k tokens**; `QB1_A.html` is 282,585 ≈ **71 k tokens**.

| # | Step | Why it is expensive today | Level 1 replacement |
|---|---|---|---|
| Q1 | **Deduplicating a new batch against the corpus** | Establishing whether a new question already exists means Claude holding QB content in context. Even reading a handful of the larger group files is 100–250 k tokens before a single judgement is made. | `qb_content_index.json` already lists all 683 question texts in ~90 KB. Python normalises and fuzzy-matches (token-set ratio + n-gram overlap) and returns exact/near/distinct buckets. Only the *near* bucket ever reaches Claude — typically a handful of pairs per batch, ~50 tokens each. |
| Q2 | **Applying a single-fact correction** | The 2026-08-04 HSSC correction touched 9 instances across 4 files. Done by reading and rewriting whole files, that is ~40 k tokens of input and a comparable output. | Python finds every occurrence corpus-wide, applies the substitution, bumps `q-version`, appends the correction footer, and updates `corrections_applied[]`. Claude verifies the *citation*, not the *edit*. |
| Q3 | **Building the HTML for a new batch** | Every `q-card` is emitted token-by-token: header, badge, tags, chevron SVG, answer body, `reg-box`, `ce-tip`, `q-footer`. The 54-question July batch is well over 100 k output tokens of pure boilerplate. | Templated emission. Claude supplies only the answer prose; Python supplies every wrapper, id, badge, tag span, TOC entry and footer. |
| Q4 | **Manifest maintenance** | Hand-editing `qb_content_index.json` after each build, then discovering drift via the next day's health check. | Generated from the built HTML. Drift becomes impossible rather than detected. |
| Q5 | **Cheat-sheet generation** | Separately authored per group. | Derived deterministically from the built cards. |
| Q6 | **`SQ/` free-sample sync** | Hand-duplicated; the health checker only detects >15% drift after the fact. | Python re-derives the teaser from the canonical file. |
| Q7 | **Re-reviewing unchanged content** | Each review pass re-reads whole files including sections settled months ago. | Content hashing per card; only changed cards enter a review packet. |

The intake side is more tractable than it looks. `new whatsapp questions July end .txt` is highly regular — `Int:` / `Ext:` / attempt / `Ship:` headers, numbered question lines, `Result:`, and `-----` separators. **Question separation, examiner attribution and batch metadata are all pure Level 1.**

## 4. Token-heavy steps in the present MIW Notes workflow

The 18 published Parts total 1.28 MB, averaging **71 KB ≈ 17.8 k tokens of HTML per Part**.

| # | Step | Why it is expensive today | Replacement |
|---|---|---|---|
| N1 | **Gemini generates a full expanded chapter** | ~90 KB of generated prose per 25-page batch, most of it structural scaffolding and standard sections. | Transcription (bounded AI) + Python scaffold + targeted expansion (bounded AI). The scaffolding never gets generated by a model again. |
| N2 | **Manual copy of Gemini output into a text file, then upload to Claude** | Human step, no provenance, no checksum, unrepeatable. | Files written directly to the staging tree by the pipeline. |
| N3 | **Claude re-reads the entire chapter to verify it** | ~25 k input tokens per Part, every pass, including sections that are pure boilerplate. | Deterministic validators run first; Claude receives only failures, uncertainty flags, unresolved citations and changed sections. |
| N4 | **Claude re-emits the entire chapter as MIW HTML** | ~18 k output tokens per Part of `topic-block`/`topic-footer`/callout markup. **This is the single largest recurring cost in the Notes workflow.** | Python builds the HTML from the template and the section content. Zero AI tokens. |
| N5 | **LaTeX → Unicode conversion** | Guaranteed rework on every Gemini draft, because the site has no MathJax. | Deterministic transform, validated by the existing `check_formula_rendering`. |
| N6 | **Gating, nav-chain, version-footer application** | Applied by hand per Part; `gating_note` fields in the manifest record several instances of it being done as a separate later pass. | Deterministic post-build step. |
| N7 | **Regulatory re-verification of stable citations** | The same conventions get re-verified in every Part. | Local verified-reference catalogue with amendment dates; only unknown or stale citations escalate. |
| N8 | **Correction round-trips** | e.g. the A.949(23) → A.1184(33) fix touched 3 files and 7 instances across QB and Notes. | Corpus-wide deterministic substitution; Claude verifies the citation once. |

**Transcription (the read step) is explicitly not on this list**, because it cannot be made cheaper — see §13.

---

## 5. Proposed QB Production Agent architecture

Two components, deliberately unequal in size.

### 5.1 Python execution engine — `tools/qb/`

```
tools/
├── _lib/
│   ├── html_checks.py        # the 13 validators, lifted from qb_health_check.py
│   ├── manifest.py           # read/write qb_content_index.json + notes manifests
│   ├── traps.py              # known_traps.md parsing (moved from qb_health_check.py)
│   ├── state.py              # batch state machine, atomic writes
│   ├── packets.py            # AI task packet construction + response validation
│   ├── corrections.py        # corrections/ ledger entry emission
│   └── hashing.py            # content hashing for change detection
└── qb/
    ├── intake.py             # WhatsApp/text batch → questions.jsonl with provenance
    ├── normalise.py          # formatting normalisation, original_text preserved
    ├── dedup.py              # exact / formatting / near / distinct classification
    ├── classify.py           # subject/topic/examiner/source/batch assignment
    ├── build.py              # questions + answers → QB HTML from template
    ├── cheatsheet.py         # derived cheat sheet generation
    ├── sq_sync.py            # SQ/ teaser derivation
    ├── validate.py           # runs _lib.html_checks against the working tree
    ├── report.py             # Claude review packet + Founder decision packet
    └── cli.py                # `python -m tools.qb <command>`
```

Every stage reads and writes files. Nothing is held in memory between commands, so any command is independently resumable.

### 5.2 `qb-production-agent` subagent scope

**Proposed only. Not created. Requires the `.claude/` ADR (blocker B5) plus Founder review of this scope.**

- **Invoked for exactly four Level 2 judgements**, and nothing else:
  1. near-duplicate classification (materially different, or the same question reworded?)
  2. examiner-variant detection
  3. answer drafting from verified source material
  4. multi-part / incomplete question resolution
- **Never** invoked for: intake, numbering, HTML emission, manifest updates, validation, or reporting.
- **Proposed tool allowlist:** `Read`, `Grep`, `Bash` restricted to `python -m tools.qb *`. **No `Edit`, no `Write`.** The brief suggested `Edit` scoped to `meoclass1/` and `SQ/`; I recommend against it. An agent that can edit published HTML directly can bypass the correction ledger, the version footer, and the manifest update — the three things `docs/CORRECTION_WORKFLOW.md` exists to enforce. The agent should emit a decision packet; Python applies it. This keeps Part I's "no irreversible corpus changes without a logged change" mechanically true rather than instruction-dependent.
- **`description:` field** must name the four judgement types explicitly and state what the agent does *not* do. Per Adaptation Note 2, a vague description is the dominant mis-routing failure mode.

---

## 6. Proposed MIW Notes Production Agent architecture

### 6.1 Python execution engine — `tools/notes/`

```
tools/notes/
├── register.py       # source PDF registration: checksum, page count, page-number offset detection
├── manifest.py       # page-level manifest generation
├── extract.py        # page image extraction (PyMuPDF), 5-page batching
├── transcribe_io.py  # writes/reads raw transcription records — does NOT call a model
├── normalise.py      # deterministic normalisation of raw transcription
├── plan.py           # chapter-boundary heuristics → chapter plan for Founder approval
├── scaffold.py       # MIW chapter HTML from template + section content
├── verify_refs.py    # citation extraction + local verified-reference catalogue lookup
├── validate.py       # runs _lib.html_checks (notes variants)
├── report.py         # Claude review packet + Founder decision packet
└── cli.py
```

### 6.2 The seven layers, as files on disk

Part D's layer model becomes a directory structure, so mixing layers is physically impossible rather than merely discouraged:

```
staging/notes/<source_id>/
├── source.json                    # 1. source_page — path, sha256, page count, offset
├── pages/p0451.png                #    extracted page images
├── raw/p0451.json                 # 2. raw_transcription  — verbatim + uncertainty spans
├── normalised/p0451.json          # 3. normalized_transcription
├── corrected/p0451.json           # 4. corrected_source_notes — with correction records
├── plan.json                      #    chapter plan (Founder-approved before drafting)
├── draft/ch19.json                # 5. expanded_chapter_draft
├── verified/ch19.json             # 6. verified_chapter
├── review/ch19-packet.md          #    Claude review packet
├── out/miw-notes-mgmt-p19.html    # 7. founder_review_version
└── state.json
```

A layer file is never edited in place. Layer *n+1* is derived from layer *n* and records the derivation.

### 6.3 `miw-notes-production-agent` subagent scope

**Proposed only. Not created.**

- **Invoked for exactly five Level 2 tasks:**
  1. handwriting transcription of one 5-page batch (page images in, verbatim text + explicit uncertainty spans out)
  2. resolving flagged-uncertain words against surrounding technical context
  3. chapter-boundary proposal from normalised transcription
  4. bounded technical expansion of one section from verified source
  5. reconciling conflicting technical statements between source pages
- **Proposed tool allowlist:** `Read` restricted to `staging/notes/` and `templates/`, `Bash` restricted to `python -m tools.notes *`. **No `Edit`, no `Write`, no access to `meoclass1/`.** Output goes to the packet, and Python writes the layer file. The agent must not be able to touch published Parts 1–18.
- **Hard rule enforced by schema, not prose:** a transcription record with an unresolved uncertainty span cannot advance past `TRANSCRIBED` — Python rejects the state transition. This is what makes Part D's "prevent guessed text from being treated as confirmed text" mechanical.

---

## 7. Shared utilities architecture

`tools/_lib/` is shared; `tools/qb/` and `tools/notes/` are not. Per Part F, shared utilities are permitted but workflows, prompts, states, reports and acceptance rules stay distinct.

The boundary rule: **a module belongs in `_lib/` only if both agents call it with the same semantics.** `html_checks.py` qualifies (both produce site HTML validated the same way). Chapter planning does not (QB has no concept of it). A `_lib/` module must never branch on which agent is calling it — that is the signature of a generic agent forming, which Part F prohibits.

`qb_health_check.py` becomes a thin CI entry point that imports `_lib/html_checks.py`. Its published-state behaviour and its email report are unchanged; the check logic simply stops living in a script that only CI can run.

---

## 8. AI-versus-Python responsibility matrix

Level 1 = deterministic Python, zero AI. L2 = bounded subagent call. L3 = Claude engineering review. L4 = Founder.

| Operation | Level | Why Python alone is insufficient (L2+ only) |
|---|---|---|
| Source file discovery, registration, checksums | 1 | — |
| PDF page extraction, image preparation, batching | 1 | — |
| **Handwriting transcription** | **2** | No text layer exists; the page is an image. Tesseract is unreliable on continuous handwriting. This is the one genuinely irreducible AI cost in the Notes pipeline. |
| Uncertainty flagging in transcription | 2 | The model that reads the handwriting is the only thing that knows what it could not read. |
| Transcription normalisation | 1 | — |
| Question separation from a batch file | 1 | The source format is regular and delimiter-driven. |
| Exact + formatting duplicate detection | 1 | — |
| **Near-duplicate: same question or materially different?** | **2** | Requires knowing that "Company definition in ISM" and "Who is the Company under the ISM Code?" are one question, while "ESP Code explain" and "ESP survey intervals" are two. String similarity cannot make that distinction — and Part C forbids merging technically distinct questions on wording similarity alone. |
| **Examiner-variant detection** | **2** | Requires recognising that the same underlying topic is being probed differently by different examiners. |
| Subject/topic/tag assignment | 1 | Keyword + existing-corpus mapping, with unmatched items escalated. |
| Question numbering, id assignment, TOC generation | 1 | — |
| **Answer drafting from verified source** | **2** | Engineering composition. |
| **Bounded technical expansion of a section** | **2** | Same. |
| HTML emission (cards, blocks, callouts, footers, gating) | 1 | Templated. |
| Cheat-sheet derivation, `SQ/` teaser derivation | 1 | — |
| Manifest generation and update | 1 | — |
| Correction ledger entry emission | 1 | Fields come from the change itself. |
| Citation extraction from prose | 1 | Pattern-matched. |
| **Citation currency verification against primary source** | **3** | P4 (Verify Before Trust) forbids trusting model recall; requires an authoritative lookup and judgement. Cached in the reference catalogue once verified. |
| All 13 structural/safety validators | 1 | — |
| Change detection, diffing, patch application | 1 | — |
| Review packet + Founder packet assembly | 1 | — |
| **Technical correctness, engineering logic, operational realism, exam suitability** | **3** | — |
| **Publication approval** | **4** | — |

Per Part I: Python never makes an engineering judgement because a similarity threshold was crossed. Below-threshold items route to review; they do not auto-resolve.

---

## 9. State and queue design (files, not chat memory)

### 9.1 State files

```
state/
├── ACTIVE.md                        # human-readable: active batch, last command, next command
├── qb/batches/<batch_id>/state.json
└── notes/sources/<source_id>/state.json
```

`ACTIVE.md` is generated from the JSON, never hand-edited, and answers Part G's seven questions in plain text — deliberately readable by a human with no AI (P7).

### 9.2 States actually used

**QB** — `DISCOVERED → REGISTERED → EXTRACTED → NORMALIZED → DEDUP_PENDING → AI_REVIEW_REQUIRED → CLASSIFIED → ANSWER_PENDING → ANSWER_DRAFTED → REGULATORY_VERIFICATION_PENDING → BUILT → VALIDATION_FAILED | VALIDATED → CLAUDE_REVIEW_PENDING → READY_FOR_FOUNDER_REVIEW → FOUNDER_CHANGES_REQUIRED | APPROVED → PUBLISHED`

**Notes** — `DISCOVERED → REGISTERED → EXTRACTED → TRANSCRIPTION_PENDING → TRANSCRIBED → NORMALIZED → PLAN_PENDING → PLAN_APPROVED → STRUCTURED → EXPANSION_PENDING → REGULATORY_VERIFICATION_PENDING → CORRECTION_REQUIRED → VALIDATION_FAILED | VALIDATED → CLAUDE_REVIEW_PENDING → READY_FOR_FOUNDER_REVIEW → FOUNDER_CHANGES_REQUIRED | APPROVED → PUBLISHED`

Per Part G, only the states each workflow needs. Two design rules:

- **Transitions are one-way except through an explicit failure state.** There is no path from `VALIDATION_FAILED` to `VALIDATED` other than re-running validation on changed content.
- **`APPROVED` and `PUBLISHED` are writable only by an explicit Founder command**, never by any pipeline step. This is what makes "Claude may not mark an output Founder-approved" mechanical.

State is written atomically (temp file + rename) so an interrupted run cannot leave a half-written state.

---

## 10. Implementation package sequence

Each is small enough to review in one sitting and follows the binding 8-stage lifecycle. **Level 1 is proven before any subagent exists** — per Adaptation Note 1, subagents are the judgement layer, not the savings layer.

| Pkg | Scope | Creates | Gate to proceed |
|---|---|---|---|
| **A0** | Governance unblock. Founder ruling or ADR on `.claude/`; decision on the stale notes manifest; decision on source-material location; ruling on the three-way chapter-standard conflict. **No code.** | — | Founder decisions recorded in the repo |
| **A1** | `tools/_lib/html_checks.py` — lift the 13 validators out of `qb_health_check.py`; add a local-filesystem source; `qb_health_check.py` becomes a thin CI wrapper. Test fixtures + tests. | `tools/`, `tools/_lib/` | Local run reproduces the current CI report byte-for-byte on the same input |
| **A2** | Commit the QB and Notes production standards to `skills/` and the chapter template to `templates/`. Resolve the section-list conflict into one canonical standard. | `skills/`, `templates/` | Founder approval of the canonical standard |
| **A3** | QB intake + normalisation + dedup. Emits `questions.jsonl` with full provenance and the four dedup buckets. No HTML, no AI. | `tools/qb/` | Replays the July 2026 batch and reproduces its known dedup outcome |
| **A4** | QB state machine, queue files, `ACTIVE.md`, CLI. | `state/` | A fresh session can determine next action from disk alone |
| **A5** | QB HTML builder + cheat sheet + `SQ/` sync + manifest generation. | — | Rebuilds an existing QB file and diffs clean against the published version |
| **A6** | Notes source registration, page manifest, **page-number offset resolution**, extraction, 5-page batching. | `tools/notes/`, `staging/` | Registers the 768-page source with correct dual page numbering |
| **A7** | Transcription record schema, ingest, uncertainty enforcement, normalisation. Reads model output; does not call a model. | — | A record with an unresolved span is rejected at the state transition |
| **A8** | Notes chapter scaffold builder + notes validators + review packet. | — | Rebuilds Part 18 and diffs clean against the published version |
| **A9** | AI task packet schemas + prompt templates for the nine bounded tasks. | — | Packets round-trip; malformed responses rejected by schema |
| **A10** | Subagent definitions + validation hook. **Only now.** | `.claude/` (needs A0) | Routing verified by test invocations |
| **A11** | QB pilot + Notes pilot (§12). | — | Part K's seven proof conditions met |
| **A12** | Token-use comparison + final implementation and verification report. | — | Measured, per §13 |

A5 and A8 are the load-bearing gates. If Python cannot reproduce an already-published file byte-for-byte, the builder is not yet a substitute for regeneration and no savings claim is defensible.

---

## 11. Premortem

Format per Part L: cause / impact / detection / preventive control / recovery / test.

| # | Failure mode | Cause | Impact | Detection | Preventive control | Recovery | Test |
|---|---|---|---|---|---|---|---|
| P1 | **Transcription error becomes authoritative** | Model misreads handwriting, no flag raised | Wrong technical content published under Uday's name | Layer-3 vs layer-2 diff review; Founder page-image spot check | Verbatim layer is immutable; every downstream layer records its derivation; uncertainty spans block advancement | Re-transcribe the page; all derived layers invalidate automatically | Fixture page with known-ambiguous handwriting must produce an uncertainty span |
| P2 | **Hallucinated regulation number** | Model recall treated as fact | Candidate fails an oral on our content | Citation extractor + catalogue lookup; unknown citations blocked | Every citation must resolve to a catalogue entry with a primary source, or be marked unresolved | Correction workflow + `known_traps.md` entry | Fixture with a fabricated `MSC.9999(99)` must fail validation |
| P3 | **Superseded amendment presented as current** | Catalogue entry goes stale | Exactly the A.949(23) and A.1140(31) failures already in the record | Catalogue entries carry `verified_on`; entries past a staleness threshold re-verify | Time-boxed verification, not one-time | Corpus-wide deterministic substitution + ledger entry | Backdate a catalogue entry; confirm re-verification is forced |
| P4 | **Source and corrected text mixed** | A layer file edited in place | Provenance destroyed, unrecoverable | Layer checksums recorded at creation and re-checked | Layers are separate files; writes to layer *n* after layer *n+1* exists are rejected | Restore layer from checksum-verified copy | Attempt an in-place layer edit; must be refused |
| P5 | **Python alters technical meaning** | Over-eager normalisation | Silent content corruption at scale | `original_text` retained on every record; normalisation diff reviewed on first run of any new rule | Normalisation is whitespace/entity/casing only — never lexical substitution without a correction record | Re-derive from `original_text` | Property test: normalisation must be idempotent and must not change the token multiset |
| P6 | **Near-duplicates wrongly merged** | Similarity threshold treated as judgement | Distinct exam questions lost from the corpus | Every merge produces a reviewable record naming both originals | Python never merges; it classifies and escalates. Merging requires an explicit decision. | Both originals retained; un-merge is a data operation | Fixture pair of technically-distinct-but-similar questions must reach the review bucket, not the merge bucket |
| P7 | **Full documents still sent to Claude** | Packet builder falls back to whole-file on an edge case | Savings evaporate silently | Packet size logged per AI call; hard ceiling enforced | Packet builder raises rather than truncating or expanding | Fix the packet builder | Any packet over the ceiling must raise in tests |
| P8 | **Unclear workflow state** | Two sources of truth for state | Duplicated or skipped work | `ACTIVE.md` regenerated from JSON on every command; a mismatch is an error | Single writer; atomic writes | Rebuild `ACTIVE.md` from JSON | Corrupt `ACTIVE.md`; next command must regenerate and warn |
| P9 | **Loss of page-level provenance** | The 6-page offset (§1.9a) unresolved | Every page citation off by six | Registration records both numberings and asserts the offset | Dual page numbering is mandatory in the source manifest | Re-register; page references recompute | Registration of the known source must report offset = 6 |
| P10 | **Approved material overwritten** | Builder writes to `meoclass1/` before Founder approval | Published content silently changed | Builder writes only to `staging/`; promotion is a separate explicit command | Subagents have no `Write`/`Edit` at all | git restore | Attempt a build targeting `meoclass1/` directly; must be refused |
| P11 | **Output diverges from the MIW template** | Template drift between the three conflicting section lists | Inconsistent handbook | A2 resolves the conflict; scaffold builds only from the committed template | One canonical template in `templates/`, git-versioned | Rebuild from template | Rebuilt Part 18 must diff clean against the published version |
| P12 | **A generic agent forms** | `_lib/` accumulates agent-specific branches | Unmaintainable, contrary to Part F | Code review of every `_lib/` addition | A `_lib/` module may not branch on caller identity | Split the module | Grep `_lib/` for agent-name references in tests |
| P13 | **Poor resumability** | State not written until end of run | Interrupted runs unrecoverable | Fresh-session test: determine next action from disk alone | State written after every stage, atomically | Re-run the last stage (idempotent) | Kill mid-run; a new session must correctly identify the next command |
| P14 | **Manual copy-paste survives** | A stage has no CLI entry point | The exact defect this project exists to remove | Every documented command must exist and be tested (Part J) | No stage ships without a CLI command | Add the command | Operating manual commands are executed in CI |
| P15 | **Validators report false success** | A check silently skips (e.g. `known_traps.md` unreadable) | Broken content passes the gate | Checks report *checks run*, not just failures; a skipped check is itself a failure | Explicit skip accounting — the existing script already does this for the traps file; generalise it | Re-run with the input restored | Remove a fixture input; the run must fail, not pass quietly |
| P16 | **Token savings claimed without measurement** | No baseline exists | An unfalsifiable claim in the final report | §13's method | Per-call token logging from A9 onward; old-workflow cost reconstructed from measured artifact sizes and stated as a model | Re-derive from logs | The report must cite logged call counts and sizes, not estimates alone |
| P17 | **Subagent mis-routing from a vague `description:`** | Description states the domain but not the boundary | Notes work routed to the QB agent, or Level 1 work routed to a subagent | Test invocations against a fixed set of phrasings | Description names the specific judgement types *and* what the agent does not do | Rewrite the description | A routing fixture set must route correctly, including negative cases |
| P18 | **Hook fails silently** | Non-zero exit swallowed, or hook not firing | The validation gate is decorative | Hook writes a timestamped receipt; the promotion step requires a receipt newer than the content hash | Absence of a receipt blocks promotion — the gate fails closed | Re-run validation | Disable the hook; promotion must be refused |

---

## 12. Recommended pilot

Both pilots are chosen so that **ground truth already exists** — proving the pipeline reproduces known-good output is a far stronger test than producing new output nobody can check.

### 12.1 QB pilot — replay the July 2026 batch

Input: `F:\1111my course videos\meoclass1\new whatsapp questions July end .txt`.
Known outcome: 54 questions across QB1_K, QB2_I, QB3_J, QB4_J, QB5_J, QB6_H, QB8_H, QB9_H, deduped against the then-629-question corpus, with two citation corrections applied (HSSC A.1140(31) → A.1207(34); QB2_I title-tag).

The batch contains, per Part K's requirements: multi-part questions, ambiguous wording, examiner-specific variants (the same Simon/Senthil pairing across three attempts, with overlapping topics), and questions requiring answer verification. It also gives a real duplicate population, since three transcripts in one file cover the same examiner.

Success criteria: Python reproduces the same dedup classification; the number of items escalated to Claude is recorded and is small; rebuilt HTML diffs clean against the published files; the two known corrections are surfaced by validation rather than by hand.

### 12.2 Uday Notes pilot — pages 451–455

Five pages, the smallest meaningful unit, taken from the master PDF (the pre-split PDFs start at 501). Pages 451–475 already have a Gemini draft (`MIW notes pages 451-475.txt`), which gives a direct quality comparator for Part K's "equal to or better than the previous Gemini-to-Claude workflow" condition.

Demonstrates every Part K item: page registration with dual numbering, transcription storage as a distinct layer, uncertainty marking, normalisation, chapter-boundary assessment, scaffold generation, correction tracking, bounded expansion, regulatory verification, deterministic checks, the Claude review packet, and the Founder output.

**Do not proceed past the pilot** until all seven of Part K's conditions hold, particularly source traceability and measured token reduction.

---

## 13. Expected token-reduction mechanism

**Attribution, stated plainly per Adaptation Note 1: the reduction comes from Level 1 Python, not from subagent isolation.** Subagents add context-isolation overhead and can increase total cost. They are in this design because Part F requires operational separation and bounded tool scope — not because they save tokens. No savings figure in the final report may be attributed to them.

Where the reduction actually comes from, in order of size:

1. **HTML emission stops being generated.** ~18 k output tokens per Notes Part and ~100 k+ per QB batch move from model output to templated Python. This is the largest single item, and it is a hard zero, not a reduction.
2. **Dedup reads a 90 KB index instead of an 8 MB corpus.** Roughly 2.03 M tokens of QB HTML never enters context.
3. **Review packets replace whole documents.** Claude sees failed checks, uncertainty flags, diffs and changed sections — not the ~25 k-token chapter.
4. **Patch-based revision replaces regeneration.** A correction touching 9 instances becomes a substitution plus one citation verification, instead of rewriting 4 files.
5. **Verified-reference caching.** Stable citations are verified once and reused with a staleness date.
6. **Unchanged content is never re-reviewed.** Content hashing per card and per section.

Transcription is explicitly *excluded* from the savings claim. It is a new, genuine AI cost that the previous workflow paid to Gemini rather than to Claude. Moving it in-repo buys provenance, uncertainty flagging and resumability — not cheapness. **The honest framing for the final report is: transcription cost is roughly preserved and relocated; construction, validation and revision cost falls substantially.**

### Measurement method (Part J #23)

No historical token baseline exists — there is no record of past usage to compare against. Any comparison must therefore be:

- **New pipeline: measured.** Per-call token logging from package A9 onward, recorded per batch with the reason each AI call was required (Part H's last requirement).
- **Old workflow: reconstructed, and labelled as reconstructed.** Derived from measured artifact sizes — 71 KB average per published Part, 90 KB per Gemini draft, 8.13 MB QB corpus — multiplied by the known number of passes. Presented as a model with its assumptions stated, never as a measurement.

If the Founder has Claude.ai usage records for the Parts 13–18 sessions, those would convert the reconstruction into a real baseline; that is worth checking before A12.

---

## 14. Genuine blockers

Ordered by what blocks the most downstream work.

**B1 — `.claude/` is not in the frozen architecture.** `AI_SESSION_START.md` §10 rule 4 prohibits adding a top-level directory without a new ADR, and the frozen list (`docs/`, `skills/`, `templates/`, `reports/`, `corrections/`, `tools/`) does not include it. Adaptation Notes 2 and 4 — subagent definitions and the validation hook — cannot be implemented without a Founder ruling or an ADR. *Blocks A10. Does not block A1–A9.*

**B2 — Source material lives outside the repository, on unversioned paths.** The 768-page Uday PDF, the four unbuilt Gemini drafts, the QB batch files, the chapter template, the style guide and the citation guide are all under `F:\1111my course videos\...` and `F:\RulesApp-Local-Input\`. Nothing in the pipeline is reproducible from the repository alone, contrary to P1 and P7. A decision is required: register externally by absolute path + SHA-256 (cheap, keeps the 62 MB PDF out of git, but leaves the repository non-self-contained), or import the source into the repo or a git-LFS/DVC-style pointer arrangement. *Blocks A6.*

**B3 — Page-number ambiguity (§1.9a).** A constant 6-page offset exists between PDF page index and the printed page stamps, and the existing manifest's `"of 768"` ranges do not state which they use. Every page-level provenance claim depends on resolving this. *Blocks A6.*

**B4 — No raw transcription layer exists for Parts 1–18 (§1.9b), and cannot be reconstructed.** The Gemini artifacts are expanded chapters, not transcriptions. A decision is required: apply the 7-layer model forward from Part 19 only (leaving Parts 1–18 with their current provenance level, honestly documented), or re-transcribe 450 pages to backfill. The first is my recommendation; the second is ~450 vision calls. *Blocks the A6 scope definition.*

**B5 — Transcription cannot be Level 1, and the choice of transcriber is a Founder decision.** The PDF is image-only. Options: (a) transcribe via the `miw-notes-production-agent` in 5-page batches — full provenance, resumable, uncertainty-flagged, costs Claude tokens; (b) keep Gemini but redirect it to produce *transcriptions* rather than chapters — cheaper, but reintroduces manual copy unless an API path is built; (c) tesseract — installed, but unreliable on continuous handwriting and would need a per-page confidence gate. Note that keeping Gemini **as currently used** does not satisfy Part D at all, since it produces no transcription layer. *Blocks A7.*

**B6 — Two competing notes manifests (PKG-1.8, open since PKG-1).** I verified `notes_content_index.json` is the authoritative superset and `notes-content-index.json` is stale at Part 16. Deleting the stale file is a Founder decision. Until it is made, any Python that writes a notes manifest risks writing to the wrong file. *Blocks A8.*

**B7 — Three conflicting chapter-standard definitions (§1.4).** The 30-section master plan, the 10-section style guide, and the 11-section Gemini prompt disagree, and none is in the repository. Part E says the repository standard takes precedence, but there isn't one. The scaffold builder cannot be written against an undefined template. *Blocks A2 and A8.*

**B8 — `docs/ENGINEERING_PRINCIPLES.md` is Draft, and six ADRs are undrafted.** The Governance Gate checks every package against "Principles and relevant ADRs" as a pair. Strictly, every package in §10 is gated on this. Worth an explicit Founder ruling on whether this work proceeds under Draft v0.2 or waits. *Potentially blocks everything; likely a one-line decision.*

**B9 — No test fixtures or tests exist anywhere in the repository.** Part J #19 and #20 build from zero, and Part M's "success requires tested execution using representative input" has no existing harness. Not a decision — just unbudgeted work to acknowledge in A1.

**B10 — No token baseline exists.** See §13. Not blocking, but it constrains what the final report can honestly claim, and it is better acknowledged now than discovered at A12.

---

## 15. What was deliberately not done

Per the brief's closing instruction: no Uday Notes chapters were regenerated, no QB backlog was processed, no `.claude/agents/*.md` files were created, no directories were added, no files in the repository were modified, and nothing was committed. This document is the only artifact produced.

**Next action:** Founder review of this assessment, with decisions on B1–B8. A0 is a decision package, not a code package — nothing below it should start until those decisions are recorded in the repository.
