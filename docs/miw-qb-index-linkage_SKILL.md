---
name: miw-qb-index-linkage
description: >
  Rules for keeping meoclass1/index.html in sync with qb_content_index.json whenever a QB
  file is added, renamed, or has questions added or removed. Use this skill together with
  miw-qb-production any time a QB HTML file is created or its question count changes —
  including new batches, A/B companion files, and single-question additions. A QB file is
  not "done" when the manifest is updated: index.html carries two separate hand-maintained
  data structures that no tool generates, and a file missing from them is invisible to
  subscribers even though it is live, gated and manifested.
---

# MIW QB — Index Linkage & Discoverability

## 1. Why this skill exists

On 4 August 2026, commit `78caad4` shipped eight QB files (QB1_K, QB2_I, QB3_J, QB4_J,
QB5_J, QB6_H, QB8_H, QB9_H — 54 questions) as "gated and indexed". Every one was built,
validated, gated, added to `qb_content_index.json` and added to `examiner-index.html`.

None was added to `meoclass1/index.html`.

The result: eight files live on the server, reachable only by typing the exact URL, with
47 of their questions absent from the on-page search. The defect survived two weeks and
several health-check runs because nothing checked for it. It was found only when a
subscriber asked why a file could not be found.

**The manifest was never the problem.** `qb_content_index.json` was correct throughout.
The lesson is that manifest correctness does not imply discoverability.

---

## 2. The three structures that must agree

| Structure | Location | Generated? | Purpose |
|---|---|---|---|
| `qb_content_index.json` | `meoclass1/` | No — hand-maintained | Authoritative manifest |
| `QB_GROUPS` | inline JS in `meoclass1/index.html` | No — hand-maintained | Renders the file cards + cheat-sheet buttons |
| `Q_INDEX` | inline JS in `meoclass1/index.html` | No — hand-maintained | Powers the question-text search box |

None is derived from another. All three drift independently.

`examiner-index.html` is a fourth surface, question-level rather than file-level; see §6.

---

## 3. Mandatory steps when adding a QB file

Do all of these in the same session as the build. A file is not done until every box is ticked.

1. Build and validate the QB HTML (see `miw-qb-production` Section 18).
2. Add the file entry to `qb_content_index.json` — `question_count`, `questions[]`, `tags`,
   `version`, `title`, `cheatsheet`.
3. **`index.html` → `QB_GROUPS`**: append the filename to the correct group's `files[]`
   **and** add a card object to that group's `cards[]`. Both. `files[]` alone renders nothing.
4. **`index.html` → `Q_INDEX`**: append one record per question,
   `{"q": <escaped text>, "file": <filename>, "qb": <group id>}`.
5. **`index.html` hero counters**: `Questions Live` = `len(Q_INDEX)`,
   `QB Files` = total cards across all groups. Update `Last Updated`.
6. `examiner-index.html`: add a row per question under the attributed examiner, and bump
   that examiner's section counter (§6).
7. Master tracker xlsx: mark `Build_Status=Built`, fill `Live_File` / `Live_Q_No` / `Live_Q_Text`.
8. Run the health check — `check_index_linkage()` will fail the run if 3–5 were missed.

### Card object shape

```json
{"file": "QB1_K.html",
 "title": "QB1_K — Engine Construction, Stability & Surveys",
 "qcount": 8, "version": "1.0",
 "tags": ["ghg","iacs","ism","load-line","machinery","solas","survey"],
 "cheatsheet": "QB1_K_CheatSheet.html", "isnew": true}
```

Source `title`, `qcount`, `version` and `tags` **from the manifest**, never by hand — that
is how card/manifest drift starts. `cheatsheet` must be the real filename or `null`; a
wrong value silently drops the cheat-sheet button. Cheat sheets never get their own card —
they attach to their parent card through this field.

### Q_INDEX record shape

```json
{"q": "(Simon sir) \"What is CSR?\" — what does he mean, and what is its scope?",
 "file": "QB1_K.html", "qb": "qb1"}
```

`q` uses the same HTML-entity escaping as existing records (`&` → `&amp;`). Generate these
from the manifest's `questions[]` so search text and manifest text cannot diverge.

---

## 4. Question added to an existing file

Adding one question to a live file touches five places. Missing any one leaves a
detectable inconsistency:

- the QB HTML (card, TOC entry, header count, `Showing N of N`)
- manifest `question_count` + `questions[]` + `total_questions`
- `QB_GROUPS` card `qcount`
- `Q_INDEX` — one new record
- hero counter `Questions Live`

---

## 5. Examiner attribution

Every new q-card carries:

```html
data-examiner="Simon" data-examiner-confidence="confirmed"
```

Confidence values follow the examiner-index tier vocabulary (`confirmed`, `inferred`,
`header`). This requirement was introduced on 11 July 2026 so `examiner-index.html` would
stop relying on a fragile parse-time fallback. Most existing cards predate it and lack the
attributes; that is a known backlog, not a licence to omit them on new cards.

---

## 6. examiner-index.html

Question-level, grouped by examiner, with a per-examiner count in the section heading.
Row shape:

```html
<div class="q-row tier-confirmed" data-tier="confirmed">
  <a class="q-link" href="/meoclass1/QB1_K.html#q8">QB1_K &middot; Q8</a>
  <div class="q-txt">question text</div>
  <span class="tier-badge">&#9989; Confirmed</span>
</div>
```

A file's questions may legitimately span several examiner sections — QB1_K has questions
under Simon, Nair and Paul. Place each question under the examiner who actually asked it,
not under one owner for the whole file. Bump the section counter you added to.

The page's own header total is known to be stale and is not maintained per-commit; do not
treat it as authoritative.

---

## 7. Verification before commit

```python
carded  = {c['file'] for g in QB_GROUPS for c in g['cards']}
cheats  = {m['cheatsheet'] for m in manifest['files'].values() if m.get('cheatsheet')}
qbfiles = set(manifest['files']) - cheats
assert qbfiles - carded == set()                      # nothing unlinked
assert len(Q_INDEX) == manifest['total_questions']    # search covers the corpus
assert sum(c['qcount'] for ...) == manifest['total_questions']
```

Then the standard gates: tag balance, no duplicate ids, both JSON blobs re-parse,
`node --check` on every script block.

---

## 8. Automated enforcement

`meoclass1/qb_health_check.py` → `check_index_linkage()`, wired into `main()` and reported
under **QB MANIFEST ISSUES**. It fails on:

- a manifest QB file with no card in `QB_GROUPS`
- a card referencing a file absent from the manifest
- card `qcount` ≠ manifest `question_count`
- `Q_INDEX` record count ≠ manifest `question_count`
- hero counters disagreeing with the structures they summarise

Runs daily at 03:00 UTC via GitHub Actions, and locally straight after a build session.
Do not treat a clean manifest as a clean index — run the check.

---

## 9. Known state (18 August 2026)

- `index.html`: 86 cards, 684 `Q_INDEX` records, counters 684 / 86 / 10 topics / 6
  examiners / 18 Aug 2026 — fully reconciled with the manifest.
- Every non-cheat-sheet manifest file is carded. Zero unlinked.
- `examiner-index.html`: 864 question links; its header total (791) is stale.
- Most q-cards still lack `data-examiner`; QB1_K Q8 is the first to carry it.
