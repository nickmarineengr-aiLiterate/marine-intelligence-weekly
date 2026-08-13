# meoclass1 Search & Updates — architecture note

Internal. Written 2026-08-13 (laptop team) as the reference study for bringing the
Written product (`/solvedQP/`) to the same functional maturity the Founder gets
from the Oral product (`/meoclass1/`).

Traced from source data → generator → generated artefact → page → user
interaction, by reading the files and driving the pages over HTTP. Nothing here
is inferred from a screenshot.

---

## 1. What actually exists

### 1.1 The two surfaces are not symmetric

| | Oral (`/meoclass1/`) | Written (`/solvedQP/`) |
|---|---|---|
| Content unit | QB file (`QB1_A.html`), ~78 files | Paper (`QP2607.html`), 28 papers |
| Search index | `Q_INDEX`, a JS array **inlined into `index.html`** | `solvedqp_content_index.json`, **fetched** |
| Index authored by | **hand**, via the `miw-qb-production` skill | **generated** from `specs/*.json` |
| Index validated by | `meoclass1/qb_health_check.py` | `build_solvedqp_manifest.py --self-test` |
| Updates source | `qb_content_index.json → recently_updated[]`, **hand-written** | `spec.changelog[]` → `recently_updated[]`, **generated** |

The single most important finding: **meoclass1 has no build step.** Its index and
its update log are typed by a human and only *checked* by a script. The Written
product already has the harder half — a generator with a paid-text guard that
fails the build — and is missing the easier half, which is surfacing.

### 1.2 meoclass1 Search — the actual mechanism

`meoclass1/index.html`, one file, no fetch for search:

- **Line 375** — `const Q_INDEX = [{q, file, qb}, …]`, ~630 entries inlined. Question
  text only. No answer text; the answer stays behind the gate, and the results
  panel says so explicitly.
- **Line 445** — `handleSearch(raw)` runs on every keystroke and does **two things
  at once**:
  1. **Card filter.** Every `.qb-card` carries a generated
     `data-search="title + filename + tags"` blob. Non-matching cards get
     `.search-hide`; group labels whose whole grid is hidden collapse too. The
     page *reshapes* as you type.
  2. **Question-level dropdown.** Below 4 characters it does nothing. At 4+ it
     substring-matches `Q_INDEX[].q`, takes the **first 8** hits, and renders
     them as `<a href="QB1_A.html">` with the caption "Found in QB1_A —
     subscriber content", followed by a standing note that answers are gated.
- Matching is `String.toLowerCase().includes(q)` — **one contiguous substring**,
  no term splitting, no folding of punctuation or entities. `"port state"`
  matches; `"state port"` does not; `"P&I"` only matches if the stem happens to
  carry the same entity encoding.
- Ranking is **insertion order truncated at 8** — deterministic, but not relevance
  ranked. A common word silently hides most of its own hits.
- The search bar is its own **`.search-bar` chrome strip** above the page body,
  results are an **overlay panel** (`#qsearch-results.open`) that closes on any
  outside click. Nothing in the page below is pushed around by results.
- `clearSearch()` resets input, re-runs with empty query, closes the panel.
- **No deep link.** No `?q=` read or written; a search cannot be shared or
  bookmarked, and back/forward do not restore it.
- **No keyboard affordance** beyond the browser default — no `/` to focus, no
  arrow-key result traversal, no Enter-to-open, no Escape-to-close.
- **Mobile**: the search strip is in normal flow and the input is `flex:1`; a
  prior regression (noted in the `/solvedQP/` CSS comments) was a bar that
  overlapped the topbar and hid the input entirely, so this is fragile but
  currently correct.
- **Empty state**: `"No matching question found in the live question banks."`
  Below 4 characters the panel is simply closed — there is no "keep typing" hint.

### 1.3 meoclass1 Updates — the actual mechanism

Three layers, only one of which a candidate sees:

1. **HTML comment at line 1 of `index.html`** — a dense engineering changelog
   ("HNS entry-into-force corrected to 29 Nov 2027… fabricated STSDSS definition
   replaced"). Not rendered. This is a maintainer's note that happens to live in
   a shipped file.
2. **`qb_content_index.json → recently_updated[]`** — the candidate-facing ledger.
   Each entry is `{date, note, files[]}`. Hand-written when a correction pass
   lands.
3. **`toggleCorrectionLog()`, line 228** — a collapsed `<details>`-style panel.
   On first open it `fetch`es the manifest `{cache:'no-store'}`, renders every
   entry newest-first as date / note / affected files, and marks
   `dataset.loaded` so it fetches once. On failure it degrades to
   "Could not load correction log." Above it, a permanent banner states the bank
   is corrected on an ongoing basis.

What makes this *feel* mature to the Founder is not the code. It is that
`recently_updated[]` **contains real corrections with real prose** —
"PSC detention appeal procedure corrected to full 3-stage chain",
"superseded A.1185(33) corrected to A.1206(34)" — and that **the whole log is
reachable**, not a truncated teaser.

`qb_health_check.py::check_manifest` closes the loop: it flags a **changelog gap**
when a file is named in a `recently_updated` summary but the manifest's own file
records disagree. The ledger is hand-written but not unpoliced.

Card-level "New" badges (`c.isnew` → `<span class="new-badge">`) are the second
update surface: recency is visible *in the grid*, not only in the log.

---

## 2. Answers to the questions this note was asked

**What data source powers Search?** An inlined JS array (`Q_INDEX`) of question
stems, hand-maintained alongside `qb_content_index.json`. Card filtering uses
generated `data-search` attributes built at render time from title/file/tags.

**What fields are indexed?** Question stem (dropdown); title, filename and topic
tags (card filter). Not: answers, examiner, regulation citations, dates.

**Fuzzy / substring / topic matching?** Substring only, case-folded, no term
splitting, no stemming, no entity normalisation, no alias list. Topic matching
exists only insofar as tags are concatenated into the card blob.

**What content surfaces appear in results?** Question stem + owning QB file, plus
a standing "answer is gated" note. Never answer text.

**How are links constructed?** `href = item.file` — **file-level, no anchor**. The
reader lands at the top of a 40-question page and must find the question again.

**Mobile?** Same DOM, `.search-row` is flex; input keeps `min-width:0` so it does
not blow out. No separate mobile affordance.

**No-result states?** One string for "no match"; silence below 4 characters.

**Is ranking deterministic?** Yes — source order, truncated to 8. Deterministic
but not relevance-ordered, and the truncation is invisible.

**How are updates generated?** They are not generated. They are typed into
`qb_content_index.json` and rendered on demand.

**What determines "new"?** A hand-set `isnew` boolean per card, plus position in
`recently_updated[]`. No date arithmetic.

**Manual vs generated?** Everything content-bearing is manual. Only the checks are
automated.

---

## 3. What is reusable in solvedQP, and what is not

### Reuse (patterns worth porting)

- **Dual-mode search.** Filtering the visible grid *and* listing question hits is
  the behaviour that makes the page feel like a search product rather than a page
  with a search box. solvedQP filters nothing today.
- **Search as page chrome, not a page section.** A strip that is always at hand,
  with results as an overlay, so results never reflow the page under the reader.
- **A reachable full update log**, with corrections in prose, not a truncated
  teaser of "added" rows.
- **Recency visible in the grid** ("New" badge), not only in a list.
- **A health check that polices the ledger** (`check_manifest`'s changelog-gap
  rule) — port the *rule*, applied to `spec.changelog[]`.
- **The gated-content honesty note** in results: say plainly that the answer is
  behind the subscription rather than implying an open document.

### Do NOT copy (Oral-product-specific or simply weaker)

- **Inlining the index into the page.** Correct for ~630 short stems in a file the
  Oral product ships as one page; wrong for 252 questions × rich metadata, and it
  would defeat the paid-text guard that currently runs at build time.
- **A hand-maintained index or hand-maintained update ledger.** solvedQP already
  derives both from `specs/*.json`. Moving to hand maintenance would be a
  regression, and the Founder's complaint is not that the data is generated.
- **Substring-only matching with a 4-character floor and an 8-result cap.**
  solvedQP's existing term-splitting AND match with folded `search_text` is
  strictly better; keep it.
- **File-level links.** solvedQP already deep-links to `#anchor`. Keep.
- **Examiner-based navigation** (`examiner-index.html`, examiner pills). Examiners
  are an Oral-orals concept; the Written paper has no examiner axis.
- **Cheat-sheet companion-file model.** Written papers carry Recall as a mode
  inside the paper, not as a separate file.
- **The line-1 HTML-comment changelog.** Engineering prose in a shipped customer
  file. Not a pattern to spread.

---

## 4. Why the Founder experiences solvedQP as immature

Recorded here because it is the finding, not an opinion:

1. **Search exists on exactly one page** — `/solvedQP/index.html`. Measured: the
   field *is* above the fold on arrival at both 1280×720 (top 336px) and 375×812
   (top 507px), so "you cannot see it" is not the defect. Two things are:
   it is an **in-flow section, not sticky**, so it is gone the moment the reader
   scrolls into the 28-card grid; and the paper page and year sheet have their
   own searches, each **scoped to that paper or that year with no escape hatch**
   to the other 27 sittings — a reader inside QP2607 searching "general average"
   is told there is nothing, when twelve other papers cover it.
2. **`recently_updated[]` contains 28 records and every single one is
   `kind: "added"`.** Not one correction has ever been written to a
   `spec.changelog[]`, although many corrections have shipped. The Updates section
   is therefore structurally capable of expressing a correction and has never
   expressed one — it reads as a release log, not a maintenance ledger.
3. **Only 6 of the 28 records are rendered**, with no "view full log", so even the
   "added" history is truncated with no way through.
4. **No deep link, no keyboard, no card filtering, no topic browse.** The
   `topics-2024/25/26.html` pages exist under `meoclass1/pastpapers/` and are
   **never published to the delivery surface at all**.

None of that is fixed by adding a manifest. The manifest is already good.

Measured evidence for (1), from `solvedqp_content_index.json`:

| Reader types, inside QP2607 | In-paper hits | Hits that exist corpus-wide |
|---|---|---|
| `port state control` | **0** | 23 questions / 18 papers |
| `ballast water` | **0** | 2 questions / 2 papers |
| `general average` | 1 | 22 questions / 19 papers |
| `salvage` | 1 | 25 questions / 21 papers |
| `llmc` | 1 | 11 questions / 11 papers |

The paper-page search is not wrong — it is correctly scoped. It is that a scoped
search with no global fallback teaches the reader the corpus is empty.

---

## 5. Functional gap matrix

`M` = meoclass1 today · `S` = solvedQP today.

| # | Feature | M | S | Gap | Required action |
|---|---|---|---|---|---|
| F1 | Search index is generated, not hand-typed | ✗ hand | ✓ generated | none — **S is ahead** | keep; do not port M's hand model |
| F2 | Paid text excluded from the payload by a build-time guard | ✗ convention | ✓ `assert_no_paid_text` | none — **S is ahead** | keep |
| F3 | Multi-term AND matching over folded text | ✗ substring only | ✓ | none — **S is ahead** | keep |
| F4 | Result links resolve to the question anchor | ✗ file-level | ✓ `#anchor` | none — **S is ahead** | keep |
| F5 | Result grouping + hit counts | ✗ flat, capped at 8 | ✓ grouped by paper | none — **S is ahead** | keep |
| F6 | Search reachable from **every** page of the product | partial | **✗ home only** | **major** | global search on paper pages and year sheets |
| F7 | Cross-scope fallback ("0 here, 23 elsewhere") | n/a | **✗** | **major** | when a scoped search returns 0, offer the corpus-wide result |
| F8 | Search stays reachable while scrolling | ✓ chrome strip | **✗ in-flow section** | **major** | sticky search affordance |
| F9 | Search filters the visible grid as you type | ✓ dual-mode | **✗** | **moderate** | filter paper cards from the same keystroke |
| F10 | Deep-linkable / shareable search (`?q=`) | ✗ | ✗ | **moderate** | read and write `?q=` + history |
| F11 | Keyboard: focus shortcut, Escape, Enter | ✗ | ✗ | **moderate** | `/` focus, Escape clear, Enter → first hit |
| F12 | Update log is generated from governed data | ✗ hand | ✓ `spec.changelog[]` | none — **S is ahead** | keep |
| F13 | Update log **contains corrections** | ✓ real prose | **✗ 28/28 are `added`** | **major** | backfill `changelog[]` for corrections already shipped |
| F14 | Whole update history reachable | ✓ full log panel | **✗ 6 of 28, no more** | **major** | full log surface |
| F15 | Recency visible in the grid ("New") | ✓ badge | **✗** | **moderate** | derive a New badge from the newest change date |
| F16 | Update ledger policed by a health check | ✓ changelog-gap rule | **✗** | **moderate** | port the rule to `spec.changelog[]` |
| F17 | Topic browse pages published to the delivery surface | ✓ topic clusters + floating nav | **✗ built but unpublished** | **moderate** | publish `topics-*.html` under `/solvedQP/` |
| F18 | "Answer is gated" honesty note in results | ✓ | ✓ (hint line) | none | keep |
| F19 | Examiner axis | ✓ | n/a | none | **Oral-specific — do not port** |
| F20 | Cheat-sheet companion files | ✓ | n/a | none | **Oral-specific — do not port** |

Nine of twenty rows are places where the Written product is already the stronger
implementation. The Founder's judgement is nonetheless correct: every row marked
**major** is a place where the candidate cannot get at the function, and a
function a candidate cannot reach is functionally absent regardless of how well
it is built underneath.

