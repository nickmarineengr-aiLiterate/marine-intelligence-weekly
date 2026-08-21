---
name: miw-correction-workflow
description: >
  Full workflow for handling a factual/regulatory correction to any live
  Marine Intelligence Weekly file (QB question banks, cheat sheets, oral
  notes, written-answer series, examiner index). Use this skill immediately
  whenever Nixon flags a factual error, reports a subscriber/candidate
  correction, or asks to "check and fix" a claim in any gated MIW content.
  Covers: repo sync verification, environment/connector audit, scoped
  conflation search, multi-file surgical editing technique (Windows +
  Desktop Commander), known_traps.md entry authoring, manifest update,
  tag-balance validation, commit/push, and live verification. Do not wait
  for an explicit trigger — if the topic is a content correction anywhere
  in the MIW platform, this skill applies.
---

# MIW Correction Workflow

Full loop for taking a flagged factual/regulatory error from report to
verified-live push, in a single session, using the local clone.

## The loop, in order

```
candidate feedback
  -> verify against a primary source        (2)
  -> scope the conflation search            (3)
  -> edit                                   (4)
  -> known_traps.md entry                   (6)
  -> correction manifest                    (7a)   <-- NEVER SKIP
  -> historical delegation checks           (7b)
  -> content / index sync                   (7c)
  -> release validation                     (7d)
  -> commit / push                          (8)
  -> live verification                      (9)
```

**Step 7a is not optional and it is not paperwork.** Every Oral question card
is owned by a release guard that pins its bytes. A correction that edits a card
without declaring it reads to those guards as undeclared drift, and they go red
— correctly. On 21 August 2026 the fair-treatment correction was pushed without
a manifest and turned **7 of 11** batch validators red; the product edits were
right, the authorisation record was simply missing. Do not discover this after
the push.

## 0. Environment check (do this first, every session)

Filesystem/GitHub access is **not guaranteed** to be present in every
chat — it depends on which connectors are attached to that session. Before
assuming local-clone access:

1. `tool_search` for "filesystem" / "desktop commander" and "github" to see
   if the tools load.
2. If Desktop Commander is available, confirm it can actually see the repo:
   `get_file_info` on `F:\marine-intelligence-weekly`.
3. If GitHub MCP is available, call `get_me` to confirm auth as
   `nickmarineengr-aiLiterate`.
4. If neither is available, fall back to `raw.githubusercontent.com` /
   codeload fetches and hand Nixon diffs to apply locally himself — do not
   claim local access you don't have.

**If both are available**, work directly against
`F:\marine-intelligence-weekly` (matches Nixon's saved workflow — saves
tokens vs. fetching over network) and push via `git` yourself.

## 1. Verify repo sync (local vs. online)

Before editing anything:

```
Set-Location 'F:\marine-intelligence-weekly'
git status
git log -1 --format=%H%n%ci
git remote -v
```

Cross-check the local HEAD/date against the online manifest's `generated`
field (`meoclass1/qb_content_index.json`, fetched via
`raw.githubusercontent.com?nocache=<timestamp>`). If local shows
uncommitted changes or the HEAD doesn't match what the manifest implies,
**stop and reconcile with Nixon before touching files** — do not silently
overwrite either side.

## 2. Confirm the flagged error against a primary source

Never take a correction claim at face value or apply it purely from
memory. Web-search and verify against a primary source per the standard
reference-priority order (IMO conventions/codes > SOLAS/MARPOL/STCW >
IACS UR/UI > class rules > DG Shipping/DGMA > manufacturer docs > ISO/IEC).
State confidence level ([Certain]/[Likely]/[Speculative]) when reporting
back to Nixon.

## 3. Scope the search — find every instance of the same conflation

A single wrong claim is rarely isolated. Search the whole
`meoclass1/` tree (not just the one file Nixon flagged) for the same
error pattern:

```python
import glob, re
files = glob.glob(r"F:\marine-intelligence-weekly\meoclass1\**\*.html", recursive=True)
flagged = []
for f in files:
    txt = open(f, encoding='utf-8', errors='ignore').read()
    for m in re.finditer(r'<anchor term>', txt):
        window = txt[max(0,m.start()-400):m.start()+700]
        if re.search(r'<conflated concept>', window, re.I):
            flagged.append([f, m.start()])
print(flagged)
```

Then inspect each hit's actual surrounding text (strip HTML tags, print
context) before deciding it's a real error — some hits will be legitimate
correct usage (e.g. a file that already correctly separates the two
concepts). Only files with a genuine false claim get fixed.

## 4. Editing technique on Windows via Desktop Commander

`edit_block` (the MCP surgical-edit tool) has been observed to **hang and
time out** (~4 min) intermittently in this environment without applying
the edit. Prefer this more reliable pattern instead:

1. Write a small Python script to a `.py` file in the repo root using
   `write_file` (not `edit_block`).
2. Run it via `start_process` with `cmd /c "cd /d F:\... && python script.py"`.
3. Inside the script: read the file, locate the exact text to replace
   using a **plain-ASCII marker substring** (avoid typing em-dashes,
   curly quotes, or other non-ASCII characters directly in tool-call
   parameters — they can get mangled in transport), then do a
   slice-based replacement (`txt.find(marker)`, `txt.rfind(open_tag, 0, idx)`,
   `txt.find(close_tag, idx)`), not a literal multi-line `str.replace` on
   text containing special characters typed by hand.
4. Use `\uXXXX` escapes in the Python string for em-dashes (`\u2014`),
   non-breaking hyphens (`\u2011`), or HTML entities (`&mdash;`) instead of
   typing the literal character.
5. Always `assert txt.count(old) == 1` (or the expected count) before
   replacing, so a silent no-op or double-match fails loudly.
6. When printing file content back for inspection, wrap stdout:
   `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')` —
   the default Windows console codec (cp1252) will crash on em-dashes,
   curly quotes, and other Unicode punctuation common in this content.
7. Keep each script's scope to one or two related edits — small, verifiable
   steps, not one giant multi-hundred-line rewrite blob.
8. **Delete every scratch/inspection `.py` file from the repo root before
   committing.** Run `git status --short` immediately before `git add` and
   confirm only the intended content files are modified — no leaked
   scratch scripts.

## 5. Validate before pushing

1. HTML tag-balance check (Python `HTMLParser` subclass with a void-elements
   set) on every touched file — confirm empty stack, no errors.
2. `json.load()` the manifest after editing it, to confirm it's still valid
   JSON.
3. Spot-check a sample of "still flagged" hits from the re-scan (step 3's
   search re-run after edits) — most will now be false positives (the
   corrected sentence itself mentions both terms, e.g. "does NOT list") —
   confirm this is the case rather than assuming.

## 6. known_traps.md entry

Append a new numbered `### N. <short title>` entry, following the existing
style exactly (see entries 1–16 for tone/structure): what was wrong, the
correct position, which files were affected, who flagged it and when.

- Add a `GREP:` line: either an exact phrase for daily auto-scan, or `SKIP`
  if the corrected sentences will legitimately contain the same trigger
  words as the error (classic case: a correction that says "X does NOT
  include Y" will always contain both X and Y). SKIP entries stay as a
  manual verification-pass checklist rather than daily auto-scan.
- Update the "Change log" table at the bottom with a new row.

## 7a. Correction manifest (Oral / QB card corrections)

**Required whenever the correction changed a `q-card` in `meoclass1/QB*.html`
or its `SQ/` twin.** Skip only for a correction that touched no card at all.

Write one record per correction *event* (one candidate report and the scope
pass it triggers), at:

```
tools/oral/correction_<correction_id_lowercased>_manifest.json
```

e.g. `CORR-FAIR-TREATMENT-20260821` ->
`correction_corr_fair_treatment_20260821_manifest.json`. The filename must
match the id; `oral_manifest.py` asserts it.

Load-bearing fields (asserted — see `oral_manifest.CORRECTION_FIELD_CLASSES`):

| Field | Meaning |
|---|---|
| `correction_id` | identity; must match the filename |
| `kind` | always `POST_RELEASE_CORRECTION` |
| `status` | `AUTHORISED` or `SUPERSEDED` |
| `origin` | e.g. `candidate_feedback` |
| `baseline_commit` | the commit **before** the first correction commit |
| `governing_commits` | the commits that made the edits, in order |
| `authorisation_source` | normally `meoclass1/known_traps.md` |
| `cards[]` | one entry per changed card |

Each `cards[]` entry needs `correction_action_id`, `file` (bare page name),
`path` (repo-relative), `anchor`, `classification`, `pre_edit_digest` and
`post_edit_digest`. Derive the digests with the guards' own function — never by
hand:

```python
import sys; sys.path.insert(0, "tools/oral")
from validate_batch_b import card_digests
card_digests(open(path, encoding="utf-8", newline="").read())["q25"]
```

**Classify every card honestly.** `PRIMARY_CORRECTION` (exactly one — the card
actually reported), `DEPENDENCY_CORRECTION`, `PROPAGATED_FACT_CORRECTION`,
`SCOPE_PASS_CORRECTION` (an independent defect the sweep happened to find),
`TEASER_SYNC`, `INDEX_METADATA`. Sharing a commit is not the same as being the
same fix, and the schema refuses to let the record blur the two.

Files with no `q-card` that no guard pins (free-sample notes pages, `known_traps.md`,
derived indexes) go in `artefacts[]` — recorded for scope, deliberately carrying no
digest.

## 7b. Historical delegation checks

Prove the record works **in both directions** before committing:

```bash
python tools/oral/oral_manifest.py                 # schema contract
python tools/oral/validate_corrections.py          # pins vs live pages
python tools/oral/run_oral_release.py --category batch --read-only --keep-going
```

The sweep must be green apart from known standing debt. Then confirm the
delegation is **non-vacuous**: temporarily move the manifest aside, re-run one
historical validator, and check it goes red again. A delegation that passes
with the record absent is not a delegation — it is a suppressed guard.
`mutate_corrections.py` automates exactly this and more.

## 7c. Content / index sync

`meoclass1/qb_content_index.json` is **generated**. Never hand-edit it.

Edit the governed source, `tools/oral/qb_content_index_governed.json`, then
regenerate:

```bash
python tools/oral/build_qb_content_index.py
python tools/oral/build_qb_content_index.py --check     # must report CURRENT
python tools/oral/validate_qb_content_index.py
```

The correction-log entry (`recently_updated`) has **one** schema:

```json
{ "date": "YYYY-MM-DD", "note": "what changed", "files": ["QB1_A.html"] }
```

`summary` and `files_touched` are obsolete July-2026 keys; the generator
**refuses** them (they left 21 of 33 entries blank on the live hub).

`note` and `files` are rendered verbatim to paying candidates, so
`CORRECTION_FORBIDDEN` bans internal detail — no person names, no chat sources,
no commit SHAs, no `known_traps` or `Entry N` references, no AI tooling. Say
*what* changed, never who reported it or where. Keep QB page names in the note:
the health check's changelog-gap count scans note text for them.

## 7d. Release validation

```bash
python tools/oral/run_oral_release.py --plan
python tools/oral/run_oral_release.py --full
```

## 8. Commit and push

**PowerShell quoting gotcha:** `cmd /c "git commit -m \"...\""` style
commands can get mis-parsed by PowerShell (the default shell) and split
the commit message on internal punctuation. Prefer running git directly
via `start_process` with a plain PowerShell command string:

```
Set-Location 'F:\marine-intelligence-weekly'
git add <file1> <file2> ...
git commit -m "Fix: <short description>"
git push origin main
```

Stage the **correction manifest** alongside the content files. A correction
commit that ships the product edit without its authorisation record is the
exact failure this workflow exists to prevent — and it will not be visible
until the next release run.

Stage files explicitly by name (not `git add .`) so scratch files that
were missed by cleanup don't get committed.

## 9. Post-push live verification

Fetch each corrected file from `raw.githubusercontent.com` with a
cache-busting query param (`?nocache=<timestamp>`) and grep for a distinctive
phrase from the fix, plus confirm the manifest's `generated` date matches.
Report back to Nixon with: files touched, commit hash, and live-verification
confirmation — not just "pushed."

## Common failure modes to watch for

- **Shipping a correction with no authorisation record.** The product edit is
  correct, the tests you ran are green, and the release suite goes red days
  later for reasons that look like tooling breakage. It is not tooling
  breakage. See steps 7a–7b, and `tools/oral/SKILL.md` §8.2.

- **Desktop Commander MCP going unresponsive mid-session** (4-minute
  timeout, no result). It usually recovers — retry with `get_config` to
  confirm the connection is back before resuming file operations.
- **Scope creep during a "single answer" fix** — a factual claim repeated
  in the 15s answer, 60s answer, body section, reg-box, CE tip, AND every
  deep-dive subsection (trap Q&A, failures, numbers, casualty link,
  examiner chain, on-my-vessel) is common in this content's structure.
  Search the *whole* answer block for the same claim before considering
  the fix complete — don't stop after the first two paragraphs.
- **Encoding mismatches** between what gets typed in a tool call and what
  lands in the file (em-dashes, non-breaking hyphens, curly quotes). Use
  the ASCII-marker-plus-slice technique from step 4 to sidestep this
  entirely rather than fighting it per-edit.
