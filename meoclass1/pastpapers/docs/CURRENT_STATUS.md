# CURRENT STATUS — MEO Class I Written Questions / QP2607

**Canonical restart document for the Past Written Papers product.**
Last updated: 2026-08-08, at the close of the QP-series architecture session. Read this first.

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
| Branch | `pastpapers/em2607-founder-review` |
| Branched from | `main` @ `2bf6e49` (unchanged; nothing merged to main) |
| Push status | **RESOLVED.** Branch pushed and tracking `origin/pastpapers/em2607-founder-review`. An off-machine backup now exists. |

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
SPEC          PASS  (4 warning(s))
PAPER BUILD   PASS
INDEX BUILD   PASS
UI BEHAVIOUR  PASS  1 page(s)      42 assertions, was 34
KNOWN TRAPS   PASS
HEALTH        PASS
AUDIT         PASS
ALL STAGES PASS   4 warning(s)
```

Rebuild is **byte-identical** — verified by hashing all four generated artefacts before
and after a second run.

Health and trap checks are **positive-controlled**: `--self-test` injects real faults and
asserts they are caught. Faults that are an *absence* (a page that lost its study-state
migration; a month cell that lost its link) are controlled by `strip_from_pages`, which
removes the marker instead of appending one. Keep it that way.

### The 4 warnings are accepted, not defects

| Warning | Decision |
|---|---|
| Q2 model answer ≈ 709 words (band 450–650) | **Accepted.** Corrected Bunkers/CLC legal wording. Do not shorten. |
| Q6 model answer ≈ 695 words | **Accepted.** Zero-carbon qualification + ICE-vs-fuel-cell contrast. Do not shorten. |
| 2 × re-verify notices | Informational — see §8. |

**Do not spend a session trimming these.**

### `.gitattributes` now pins LF

`core.autocrlf=true` rewrote LF→CRLF on checkout while the builders write LF, so the
committed bytes never matched builder output and every build dirtied the tree. The new
root `.gitattributes` pins `*.html/json/css/js/py/md` to LF and marks `*.pdf` binary,
which makes the byte-reproducibility guarantee actually true.

---

## 8. PUBLICATION BLOCKER: Q7 primary-source verification

**Q7 — Merchant Shipping Act, 2025.** Two blockers, both real:

1. **Commencement scope not established.** `S.O. 1244(E)` of 10 March 2026 brought the Act
   into force from **15 March 2026**. Whether that commenced **every** provision is **not
   confirmed** — the Act permits different dates for different provisions.
2. **No section-level citations.** Full statutory text could not be retrieved (India Code
   PDF returned HTTP 403). **No section number of the 2025 Act is cited anywhere**,
   deliberately.

Re-ground from primary Government of India / Gazette / DG Shipping sources before any
release. Verified and safe: Act No. 24 of 2025, assent 18 August 2025, in force
15 March 2026 by S.O. 1244(E), repeals the MS Act 1958 (saving Part XIV, not s.411A) and
the Coasting Vessels Act 1838.

**Seven claims carry `reverify_before_publication` flags** (Q1 ×2, Q4 ×1, Q6 ×2, Q7 ×2).
`validate_spec.py` prints them every run.

---

## 9. Q9 / QB9_C — known cross-link issue, repair deferred

QP2607 Q9 correctly treats the **Indian Marine Insurance Act, 1963** as operative (s.19
utmost good faith, s.20 disclosure incl. the four s.20(3) exceptions).

`meoclass1/QB9_C.html` attributes the principles to the **UK Marine Insurance Act 1906** —
wrong statute for an Indian examination. QP2607 Q9 carries an **explicit caution** rather
than silently inheriting it. `meoclass1/QB9_E.html` handles it correctly.

A broad Question Bank repair is **deliberately deferred** and is a separate task. Once
QB9_C is fixed, soften the caution in `specs/QP2607.json` (Q9 `cross_links`) and
regenerate. Recorded as trap 8.

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

1. **Founder visual review** of the three pages. Four CSS/render defects were found and
   fixed this session (§15); the pages have not yet been seen by the Founder.
2. **Q7 primary-source resolution** (§8). The publication blocker.
3. Correct any defects found in review. **Edit the spec, never the HTML.**
4. Re-run the toolchain; confirm deterministic rebuild.
5. **Founder approval.**
6. Only then decide gating / publication / indexability.
7. **Only after QP2607 is approved**, build QP2601–QP2606 against the frozen pattern.
8. **Only after more than one paper**, mature the skill draft and consider the production
   agent. **Do not build the agent yet.**

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

---

## 17. Known environment quirks

- A repo hook, `validate_antipatterns.py`, is misconfigured — its plugin path does not
  exist on disk, so it reports an error on every file write. It blocks nothing, but it is
  a no-op safety net. Worth fixing or removing.
- `package.json` sets `"type": "module"`, so Node test files must use `.cjs`.
- The in-app browser cannot inspect `file://` pages (they load as non-inspectable
  snapshots) and `Control_Chrome` is macOS-only. Serve over HTTP for visual review.
