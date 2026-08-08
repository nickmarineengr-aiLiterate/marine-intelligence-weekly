# CURRENT STATUS — MEO Class I Written Questions / QP2607

**Canonical restart document for the Past Written Papers product.**
Last updated: 2026-08-08, at the close of the V1 freeze / true-source demand session. Read this first.

> **QP2607 IS THE FOUNDER REVIEW CANDIDATE.** There are **no class A (blocking) flags left**.
> Q7's two publication blockers were closed against primary Gazette text this session. What
> remains is four class B currency checks and two class C accepted limitations — see §8.

> **QP2607 V1 TEMPLATE — FROZEN FOR CROSS-PAPER VALIDATION.** See §2a. First paper validated;
> cross-paper validation still required. One paper does not prove the method universally.

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
| Branch | `pastpapers/em2607-founder-review` — the branch NAME deliberately keeps the historical wording; the product identity is QP2607. Do not rename the branch for cosmetics. |
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
SPEC          PASS  (2 warning(s))
PAPER BUILD   PASS
INDEX BUILD   PASS
UI BEHAVIOUR  PASS  1 page(s)      58 assertions
KNOWN TRAPS   PASS
HEALTH        PASS
AUDIT         PASS
ALL STAGES PASS   2 warning(s)
```

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

- All three pages are **`noindex`**; **no gate** is enabled.
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
6. **Only after QP2607 is approved**, build QP2601–QP2606 against the frozen V1 template (§2a).
   QP2601 is the **cross-paper validation** of the method, not merely the next paper.
7. **Only after more than one paper**, mature the skill draft and consider the production
   agent. **Do not build the agent yet.**

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
- **Starting a second paper.** Not until QP2607 is approved.
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
