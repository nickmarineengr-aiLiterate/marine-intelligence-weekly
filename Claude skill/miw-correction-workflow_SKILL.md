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

## 7. Manifest update

Insert a new object at the front of `recently_updated` in
`qb_content_index.json`: `date`, a `summary` describing what was found and
fixed (specific enough that a future correction pass can see this was
already handled), and `files_touched`. Update the top-level `generated`
and `generated_by` fields.

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

Stage files explicitly by name (not `git add .`) so scratch files that
were missed by cleanup don't get committed.

## 9. Post-push live verification

Fetch each corrected file from `raw.githubusercontent.com` with a
cache-busting query param (`?nocache=<timestamp>`) and grep for a distinctive
phrase from the fix, plus confirm the manifest's `generated` date matches.
Report back to Nixon with: files touched, commit hash, and live-verification
confirmation — not just "pushed."

## Common failure modes to watch for

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
