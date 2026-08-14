<!-- GENERATED EXPORT — DO NOT HAND-EDIT.
     Authoritative source: tools/notes/SKILL.md
     Re-export with: python tools/notes/export_skill.py
     This copy exists only to be uploaded to Claude Project Knowledge.
     Last export: 2026-08-06 -->

---
name: miw-notes-mgmt
version: 2.0
updated: 2026-08-05
description: >
  Full production, verification and correction workflow for the Marine Intelligence Weekly MEO Class 1
  Engineering Management Notes series (the "Uday Notes") at marineintelligenceweekly.com/meoclass1/oralnotes/.
  Load immediately whenever Nixon mentions "mgmt notes", "management notes", "Uday notes", "Engineering
  Management Notes", "next set of pages", "Part N", or pastes/uploads a new batch of source pages.
  v2 adds the local Python toolchain (tools/notes/) which removes all boilerplate authoring from the
  token budget — Claude authors a JSON content spec only; the builder emits the HTML.
---

# MIW Engineering Management Notes — Production Skill v2

## 0. TL;DR for a new session

```
cd F:\marine-intelligence-weekly
python tools\notes\inspect_part.py meoclass1\oralnotes\miw-notes-mgmt-p<LATEST>.html   # continuity check
python tools\notes\extract_template.py meoclass1\oralnotes\miw-notes-mgmt-p<LATEST>.html  # refresh shell
#   ... author tools\notes\specs\p<N>.json  (content only — no HTML) ...
python tools\notes\validate_spec.py tools\notes\specs\p<N>.json
python tools\notes\build_part.py    tools\notes\specs\p<N>.json           # ungated review copy
python tools\notes\health_check.py  meoclass1\oralnotes\miw-notes-mgmt-p<N>.html
#   ... Nixon reviews, feedback applied to the JSON, rebuild ...
python tools\notes\build_part.py    tools\notes\specs\p<N>.json --gated
python tools\notes\health_check.py  meoclass1\oralnotes\miw-notes-mgmt-p<N>.html --require-gate
```

Never hand-write the `<head>`, CSS, watermark, topbar, sidebar, footer or closing scripts. They are
carried verbatim from the most recent live Part by `extract_template.py`. Editing them by hand is the
single largest avoidable token cost in this series.

---

## 1. Platform identity

| Field | Value |
|---|---|
| Series | MIW Engineering Management Notes ("Uday Notes") |
| Live path | `https://marineintelligenceweekly.com/meoclass1/oralnotes/` |
| Repo path | `F:\marine-intelligence-weekly\meoclass1\oralnotes\` |
| Filename | `miw-notes-mgmt-p<N>.html`, N = 1…31 |
| Source | Uday Sankar S. (Anglo-Eastern), 768-page personal notes |
| Audience | MEO Class 1 candidates, Kochi MMD |
| Compiled by | Nixon Antony, 2/E, Maersk A/S |
| Corrections | contactus@marineintelligenceweekly.com |
| GA4 | `G-0YEE2CBNP5` — mandatory in `<head>` |
| Robots | `noindex, nofollow, noarchive, nosnippet` on every gated file. No OG tags, no geo tags, no JSON-LD. |
| Canonical | `https://marineintelligenceweekly.com/meoclass1/oralnotes/miw-notes-mgmt-p<N>.html` — **resolved**, matches the live path (the Part 1 `/notes/` ambiguity from v1 is closed) |

**Page-range mapping:** Part N covers source pages `(N−1)×25 + 1` to `N×25`.
Part 18 = 426–450 · Part 19 = 451–475 · Part 20 = 476–500 · Part 21 = 501–525 · Part 22 = 526–550.

---

## 2. Status

| Part | Pages | Topics | Status |
|---|---|---|---|
| 1–18 | 1–450 | varies | Live, gated |
| 19 | 451–475 | 5 | **Live, gated** (2026-08-05) |
| 20 | 476–500 | 3 | **Live, gated** (2026-08-05) |
| 21 | 501–525 | 3 | **Live, gated** (2026-08-05) |
| 22 | 526–550 | 3 | **Live, gated** (2026-08-05) |
| 23–31 | 551–768 | TBD | Planned |

---

## 3. Topic numbering — settled convention

Topic IDs are **local to the Part**: `id="topic-p<N>-<n>"`, badge `Part N · Topic n`, version tag
`Notes-p<N> · P<N>-T<n> · v1.0`. There is **no continuous global T-number** across the series. Global
renumbering is deferred until all 31 Parts are confirmed live (standing platform rule). The attribution
strip states this explicitly on every Part — `build_part.py` generates that sentence automatically.

Topics per Part is **whatever the source batch contains** — one topic block per source chapter. Do not
force a fixed count. Part 19 had 5 chapters; Parts 20–22 have 3 each.

---

## 4. Toolchain (`F:\marine-intelligence-weekly\tools\notes\`)

| File | Purpose |
|---|---|
| `inspect_part.py` | Prints structural metadata of any Part: title, canonical, robots, GA4, gate state, topic IDs/titles/meta, class inventory. Run first, for continuity. |
| `extract_template.py` | Splits a reference Part into `template/shell_head.html`, `template/shell_tail.html`, `template/sample_topic.html`. Prints the shell with CSS/JS elided for cheap review. Re-run whenever the design changes. |
| `build_part.py` | Assembles the Part from `specs/p<N>.json` + the shell. `--gated` inserts the auth gate; default emits the review copy with `<!-- GATE SCRIPT STRIPPED FOR REVIEW COPY -->`. |
| `validate_spec.py` | JSON syntax + required-key check before building. Reports the offending line/column on a syntax error. |
| `health_check.py` | Tag balance (HTMLParser stack), head-block checks, canonical↔filename match, topic ID sequence, mandatory sections per topic, artifact scan (`[cite:]`, LaTeX, placeholders, mojibake), TOC anchor resolution. `--require-gate` enforces the gate. Exit 1 on error. |
| `specs/p<N>.json` | The **only file Claude authors**. Content, not markup. |
| `template/` | Generated. Do not hand-edit; regenerate from a live Part. |

`build_part.py` rewrites exactly these variable regions of the shell: `<title>`, meta description,
canonical, notes-badge text, `<h1>`, page-sub, header-meta block, attribution strip, the whole sidebar,
and the page footer. Everything else — CSS, watermark SVG, topbar, deep-dive toggle, IntersectionObserver
TOC highlighting, copy/contextmenu/selectstart blockers — passes through untouched. If a rewrite target
is not found exactly once the build **fails loudly** rather than silently producing a wrong file.

---

## 5. Spec schema (`specs/p<N>.json`)

Top level: `part`, `prev_part`, `prev_pages`, `pages`, `total_pages`, `gated`, `title_topics`,
`meta_description`, `page_sub`, `qb_links` (list of `[href, label]`), `topics` (list).
Optional: `next_part` — **omit until that Part actually exists**; add retroactively.

Each topic:

| Key | Required | Notes |
|---|---|---|
| `n` | ✔ | 1-based, sequential |
| `toc` | ✔ | Short sidebar label |
| `title` | ✔ | Full h2 |
| `kw` | – | `data-kw` search keywords |
| `tag`, `pages`, `examiner` | ✔ | topic-meta row; `pages` = "Uday pp. X–Y (approx.)" |
| `freq` | – | `high` (default) or `medium` |
| `verify` | – | **Mandatory whenever anything was corrected.** Omit only if genuinely nothing needed changing. |
| `definition` | ✔ | Single paragraph |
| `why` | ✔ | List — CE-perspective bullets |
| `timeline` | – | List of `[year, event]` |
| `regs` | – | `{title, items:[[code, desc], …]}` |
| `sections` | – | List of `{head, body}`; body nodes: `{"p":…}` (+ optional `style`), `{"ul":[…]}`, `{"table":{head,rows}}`, `{"ascii":"…"}`, `{"raw":"…"}` |
| `ce_tip` | – | `{examiner, text}` |
| `qa` | ✔ | ≥3 `[question, model answer]` pairs. Auto-numbers if the question doesn't start `Qn.` |
| `exam` | ✔ | ≥3 `[marks, question]` — conventionally 5 / 10 / 15 |
| `memory` | ✔ | List of mnemonic/recall lines |
| `deep_dive` | – | `{title, blocks:[[tag, text], …]}` — tags `h4` / `p` |
| `refs` | ✔ | Named official sources, not raw URLs |
| `version` | – | Defaults `1.0`; bump on correction |

**Escaping:** inline HTML (`<strong>`, `<em>`, `<sub>`) is allowed and passes through. Bare `&` is
auto-escaped to `&amp;`; existing entities are left alone. Use `\n` inside `ascii` blocks. Do not paste
raw newlines into JSON strings.

---

## 6. Examiner assignment (Kochi MMD)

| Examiner | Domain |
|---|---|
| Nair (External) | Conventions, MARPOL, carriage regimes, commercial/liability law, regulation numbers |
| Simon (External) | Machinery, 2-stroke, GHG/decarbonisation, MEPC outcomes |
| Rajappan | Stability, cargo, GZ curves |
| Srivastava | Electrotechnology |
| Senthil (Internal) | Safety, LSA, STCW, ISM, MLC, commercial ship management, sustainability |
| Paul (External) | Statutory surveys, certification, lifting appliances |

Default: Nair for regulatory/legislative, Senthil for management/organisational, Paul for survey-heavy.

---

## 7. Verification standard (non-negotiable)

1. Every regulation number, resolution number, date, percentage, currency figure and statistical claim in
   the source draft is checked against a primary source (IMO, IACS, ClassNK, DNV, ISO, indiacode.nic.in,
   CMI, ICC) before it is written.
2. **Strip, don't hedge.** Unverifiable figures are removed or replaced — never retained with a soft
   caveat. (Part 19 example: the Worldscale "24-hour canal allowance" and "March–September bunker index
   window" were unverifiable against a primary source and were stripped, while the widely published
   nominal-vessel parameters were retained and labelled as commercial benchmarks.)
3. Draft / not-yet-in-force instruments are labelled as such **every time they appear**, not once at the
   top. Rotterdam Rules = adopted, not in force. Say it in the reg box, the table and the Q&A.
4. **Every correction gets a visible `.verify-note`** at the top of the affected topic, in plain language,
   naming what the draft said and what the verified position is.
5. Mnemonics and teaching formulas are explicitly labelled as memory aids, never presented as rule text.
6. Watch for **stale legislative status** in source drafts — "Bill" vs "Act" is the classic tell.

### Standing corrections established in this series (carry forward)

- **Bills of Lading Act, 2025** (India) — assent 24 Jul 2025, repeals the Indian Bills of Lading Act 1856. Not a "Bill".
- **Carriage of Goods by Sea Act, 2025** (Act 19 of 2025) — assent 8 Aug 2025, commenced 10 Sep 2025, repeals the Indian COGSA 1925, applies Hague-Visby (1968 + 1979 Protocols). India is now a Hague-Visby jurisdiction.
- **Merchant Shipping Act, 2025** (Act 24 of 2025) — in force 15 Mar 2026; DG Shipping renamed DGMA; cabotage moved to the Coastal Shipping Act 2025.
- **Hague-Visby dates** — Visby Protocol *signed* 23 Feb 1968, *in force* 23 Jun 1977; SDR Protocol 21 Dec 1979, in force 14 Feb 1984. Signature ≠ entry into force.
- **Hague-Visby limits** — 666.67 SDR/package or 2 SDR/kg, whichever higher. Hamburg 835 / 2.5. Rotterdam 875 / 3 (not in force).
- **YAR Rule XXIII** — 1 year from issue of the adjustment, 6-year long stop from termination of the adventure. Present in YAR 2004 and 2016; **absent from YAR 1994**.
- **BARECON** — A (1974) = commissioned vessels; B (1974) = newbuildings financed by mortgage; amalgamated into BARECON 89 → 2001 → 2017. **There is no BARECON C**, and the A/B split was never about insurance premiums.
- **Incoterms** — "ship's rail" deleted in Incoterms 2010; risk passes on placement on board. Incoterms 2020: DAT→DPU; CIP requires ICC (A), CIF still ICC (C).
- **Volumetric ratios** — express as volume per tonne: ocean 1 CBM, road 3 CBM, air 6 CBM (IATA divisor 6,000 cm³/kg ⇒ 1 CBM ≈ 167 kg). "1 CBM = 6 tonnes" for air is inverted and wrong.
- **GHG track separation** — CII is Tank-to-Wake (MARPOL Annex VI Reg 28); FuelEU Maritime and IMO GFI are Well-to-Wake. IMO GFI baseline 93.3 gCO₂eq/MJ; FuelEU baseline 91.16 gCO₂eq/MJ. Never conflate.

---

## 8. Workflow

1. **Intake** — Nixon uploads the next 25-page batch (often pre-passed through Perplexity/Gemini with a
   correction document). Read the raw notes *and* the correction document.
2. **Continuity** — `inspect_part.py` on the latest live Part; confirm page range and that the previous
   Part has no forward link to build yet.
3. **Template refresh** — `extract_template.py` on the latest live Part.
4. **Verification pass** — Section 7 applied to every chapter. Web-verify anything legislative, dated or
   numeric. Log every correction for the `verify` field.
5. **Author** `specs/p<N>.json`. One topic per source chapter.
6. **Validate** → **build** (ungated) → **health check**.
7. **Present the ungated review copy to Nixon.** Do not gate without approval.
8. **Revise the JSON** (never the HTML) and rebuild.
9. **Gate**: `build_part.py … --gated`, then `health_check.py … --require-gate`.
10. **Manifest**: update `meoclass1/oralnotes/notes_content_index.json` (UNDERSCORE — see Section 8a)
    in the **same session** as the build — Part entry, page range, topic count, topic titles, and bump
    `total_files` + `generated`. A Part is not "done" until the manifest reflects it.
11. **Index**: update the notes index `index.html` card for the new Part, and add the forward
    `Part N+1 →` link into Part N−1's sidebar spec and rebuild that Part.
12. **Commit**: stage files **explicitly by name** (never `git add .`), push to `origin/main`,
    cache-busted live verification.

---

## 8a. Manifest authority — ONE file per series, no exceptions

Two manifests exist. They are **separate by design and must never be merged**:

| Manifest | Covers | Do not confuse with |
|---|---|---|
| `meoclass1/oralnotes/notes_content_index.json` | **Oral / page-range series**: Simon Sir Notes, Current Topics, MIW Engineering Management Notes (Uday Notes) | the written manifest |
| `meoclass1/oralnotes/written_content_index.json` | **Written Answer series**: WA1-HKC, WA2-GHG, WA3-LIEN | the oral manifest |

**The oral manifest filename uses UNDERSCORES: `notes_content_index.json`.**

A hyphenated `notes-content-index.json` existed until 2026-08-06 as a stale divergent duplicate
(generated 2026-07-18, `total_files` 25, EM Notes Parts 1–16). It was verified a strict subset of the
underscore file — all 25 shared entries byte-identical, nothing unique to it — and removed via
`git rm` (commit `89291e5`; content recoverable at `64ab22d`). **Never recreate the hyphenated name.**
If a tool, script or session note refers to `notes-content-index.json`, that reference is wrong — fix
the reference, do not recreate the file.

Why this failed silently for 11 days: nothing loads the oral manifest at request time, so a stale copy
breaks no page and throws no error. The only defence is discipline — **update the manifest in the same
session as the content change**, exactly as `qb_content_index.json` is handled for the QB series.

Known recurrence risk — **mitigated 2026-08-06**. Manifest paths are now defined once in
`tools/notes/miw_paths.py` (`NOTES_MANIFEST`, `WRITTEN_MANIFEST`, `QB_MANIFEST`, plus repo-relative
`*_REL` forms). Never spell a manifest filename as a bare inline string again — import it.

- `tools/notes/audit_master_index.py` and `tools/notes/match_qb.py` import from `miw_paths` and call
  `assert_no_legacy_manifest()` at startup.
- `meoclass1/qb_health_check.py` keeps its own repo-relative constants **by design** — it scans the
  GitHub tree, not local disk, so it cannot import a local-path module. It now carries
  `LEGACY_NOTES_MANIFEST_NAME` and raises a hard error from `check_notes_manifest()` if the retired
  file reappears in the repo. If a manifest is ever renamed, change **both** places.
- `build_part.py` does not read any manifest — it only emits Part HTML. Manifest updating is a
  separate, manual step (workflow step 10).

`assert_no_legacy_manifest()` keys severity to git tracking, not mere presence: a **tracked**
duplicate raises (it would be pushed and would mislead every future session), while an **untracked**
local remnant warns on stderr and continues (it cannot reach the repo, and must not block work).

---

## 9. Environment notes

- Work from the **local clone** `F:\marine-intelligence-weekly` via Desktop Commander. Do not fetch files
  from GitHub raw to read them — it costs tokens and `raw.githubusercontent.com` silently caps large files
  around 100 KB and serves stale CDN cache.
- `GitHub:create_or_update_file` returns 403 for this repo. All writes go through the local filesystem.
- **PowerShell inline Python is unreliable** — UTF-8 punctuation (₹, —, ·) and nested quotes break the
  parser. Always write a `.py` file and run it. All tools in `tools/notes/` set
  `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')` for this reason.
- Redirecting Python output to a file from PowerShell produces UTF-16; read the file with
  `Desktop Commander:read_file` only if you accept the mojibake, or print to console instead.
- Delete scratch files before committing.

---

## 10. Open items

- **Parts 19–22: complete, gated, live, pushed, verified on GitHub raw and on the live site (2026-08-05).**
  `notes_content_index.json` updated (+4 entries, `total_files` 27→31), `oralnotes/index.html` has 4 new
  live cards, Part 18 sidebar has the `Part 19 →` forward link. Nothing outstanding for these four Parts.
- **Two flagged issues from the overlap audit (§11) rectified same day:** Part 2 Topic 9's stale NZF date
  (6 occurrences, "November 2026" → confirmed 4 December 2026) fixed directly on the live file; back-links
  added in both directions — Parts 3, 11, 13, 15 and 18 (old) now each carry a "See also" reference forward
  to the new Part 19-22 topic that generalises or complements them, matching the forward links already in
  the new topics' verify notes.
- **`known_traps.md` entries #25-30 added** (Bills of Lading Act 2025, COGSA 2025/India-now-Hague-Visby,
  fictional "BARECON C", inverted air-freight volumetric ratio, ESP Code citation A.1049(27), and an
  evergreen "always re-verify the current MEPC session" reminder for the Net-Zero Framework specifically).
- **`uday-index-crossref.html` reconciled for pages 451-550**, using actual built topic locations rather
  than the original page-based Part guess (several terms landed in a different Part than assumed — e.g.
  CSR and CAS/CAP were guessed for Part 20 but actually built in Part 21; SIRE/Kyoto/GHG were guessed for
  Part 21 but actually built in Part 22). Stats: 118/28/117 → 155/30/78 matched/gap/planned (263 total).
  Two terms ("ZESIS") could not be verified against any built content and were honestly left as a gap
  rather than force-matched — if a future session identifies what this refers to in the source book, close
  it out in the crossref index directly (search for `idx-gap` rows with that text).
- **Volatile content re-verified 2026-08-05 (second pass), same day as the above:** MEPC 84 (27 Apr–1 May
  2026) reached **no final agreement** on the Net-Zero Framework. Both Part 22 Topic 3 and Part 2 Topic 9
  now correctly state the current decision point as **4 December 2026** (resumed MEPC/ES.2, immediately
  after MEPC 85, 30 Nov–3 Dec 2026), superseding the original "October/November 2026" framing that was
  accurate only at initial drafting. **If any future session touches NZF content, re-verify the MEPC
  session status again before publishing — this has now moved twice in the time this series has existed
  and will keep moving until the Framework is actually adopted.**
- Also re-verified this pass, both confirmed accurate, no changes needed: the SOLAS I/14 extension figures
  (5 months / 3 months / 1 month, Part 21 Topic 1) against primary SOLAS text; the ESP Code citation
  A.1049(27), adopted 30 Nov 2011, mandatory via SOLAS XI-1/2 from 1 Jan 2014 (Part 21 Topic 2).
- Parts 23–31 (pages 551–768) not started — no source uploaded.
- **Standing rule confirmed by Nixon (2026-08-05):** a topic must sit wholly within one Part and must never
  be carried across Parts; merge related source chapters within a Part where the material supports it.
  Applied as: P19 = 5 topics (5 source chapters), P20/21/22 = 3 topics each. Deliberate cross-Part
  hand-offs, cross-referenced rather than split: GA (P18 T4 → P19 T1), B/L and charterparties
  (P19 T2/T3 → P20 T2), HSSC surveys vs certification (P20 T3 → P21 T1), vetting (P21 T3 → P22 T1).
- **Skill-file provenance note (2026-08-05):** the version of this skill uploaded to Claude's project
  knowledge (`miw-notes-mgmt_SKILL.md`) is a stale v1 — it describes Part 2 as the current frontier and a
  continuous global topic-numbering scheme that was abandoned before Part 11. Project knowledge files are
  read-only from inside a chat and there is no tool to push to it directly, so this repo file
  (`tools/notes/SKILL.md`) remains the actual living, current version and is kept in sync every session.
  **Same-day follow-up:** Claude prepared a corrected standalone copy and delivered it via `present_files`
  for Nixon to drag into Project Knowledge (replacing the stale upload), and packaged this file as a
  formal Claude Skill (`miw-notes-mgmt.skill`, mirroring the existing `miw-qb-production` entry) delivered
  the same way with a "Save skill" button. **Two human actions remain, both one click:** (1) drag the
  corrected `.md` into the project's Files/Knowledge panel to replace the old upload, (2) click "Save
  skill" on the packaged `.skill` card to install it so it auto-triggers without needing to be named or
  found in the repo. Once installed, the Skill's own copy will drift from this repo file over time unless
  re-packaged after future sessions — treat the repo file as the source of truth and re-run the packaging
  step periodically, not as a one-time action.
- Reusable audit tools kept for future Parts: `audit_overlap.py` (cross-checks new topics against
  `uday-index-crossref.html` and a direct Parts 1-18 grep) and `match_qb.py` (matches new topics against
  `qb_content_index.json` for real, justified QB sidebar links). Both are hard-coded to Parts 19-22 in
  their current form — update the Part-number list at the top of each before reusing on Parts 23+. The
  one-off backfill scripts used to apply the Part 19-22 reconciliation to the crossref index and manifest
  (`update_crossref_19_22.py`, `update_manifest.py`) were scratch and have been deleted; the method and
  findings are preserved in §11 below for the next reconciliation pass.

---

## 11. Overlap-with-Parts-1-18 audit (run 2026-08-05, after Part 19-22 build)

Two new reusable tools support this check for future Parts:

- `tools/notes/audit_overlap.py` — cross-checks a set of new topics (by `kw` field) against
  `oralnotes/uday-index-crossref.html` (the repo's own curated A-Z book-index → Parts 1-18 map) and against
  a direct full-text grep of Parts 1-18. Currently hard-coded to Parts 19-22; update the `load_new_topics()`
  Part-number tuple for future runs. Writes `tools/notes/_overlap_report.txt` (kept as a reference artifact).
- `tools/notes/match_qb.py` — matches new topics' `kw` fields against `meoclass1/qb_content_index.json`
  (title + tags + question text) to find real, justified QB sidebar links instead of guessing. Re-run this
  for every future Part before setting `qb_links` in the spec.

**Method:** ran both tools against all 14 Parts 19-22 topics. For every hit, pulled the full topic-block text
of the candidate Parts 1-18 topic and judged genuine duplication vs. incidental keyword overlap vs. a
different, complementary angle.

**Findings — two genuine, significant duplicates found and cross-linked (not rewritten):**
1. **Part 21 Topic 1** (HSSC Certification Framework) duplicates the core SOLAS I/14 survey-window and
   extension mechanics already in **Part 11 Topic 48** (Statutory Survey Engineering — Load Line Framework),
   which has the identical 5-year/±3-month/5-3-1-month figures anchored to the Load Line Certificate.
   P21T1's own contribution — confirmed genuinely absent from Parts 1-18 by direct grep — is generalising
   across all statutory certificate types, the 3-way statutory/commercial/class categorisation, and
   electronic certificates (FAL.5/Circ.39/Rev.2). Cross-reference added to P21T1's verify note.
2. **Part 21 Topic 3** (CSR, ISM Certification & Auditing) duplicates **Part 13 Topic 2** (ISM Code — SMS
   Architecture, DOC/SMC Certification & Non-Conformity Management) on the NC/MNC/Observation taxonomy and
   DOC/SMC validity table, and duplicates **Part 15 Topic 1** (Ship Identification Systems & Statutory
   Credentials) on CSR contents/amendment mechanics. P21T3's distinct contribution: the downgrade-vs-close-out
   procedural distinction, the bareboat-handover certification-sequencing walkthrough, and the "why engine
   room findings become MNCs" pattern analysis. Cross-reference added to P21T3's verify note pointing to both.

**One partial overlap, judged complementary not duplicate — cross-linked:**
3. **Part 22 Topic 3** (IMO GHG Strategy, MBMs & EEDI) vs. **Part 2 Topic 9** (Decarbonisation Pathways & the
   IMO Net-Zero Framework). P2T9 goes deep on pricing mechanics (draft two-tier $/tonne figures, Net-Zero Fund,
   draft Z-factor trajectory to 2030) which P22T3 deliberately does not repeat; P22T3 covers Strategy history
   (2018 vs 2023), the in-force EEDI/EEXI/SEEMP/CII measures, and tank-to-wake/well-to-wake, which P2T9 does
   not. Cross-reference added both ways in P22T3's verify note.
   - **Bonus finding, not yet actioned:** P2T9's own verify note states NZF adoption was "rescheduled to
     November 2026" — accurate when P2T9 was written, now superseded by the confirmed 4 December 2026 date
     (MEPC 84, Apr–May 2026, reached no agreement; MEPC 85 30 Nov–3 Dec 2026; MEPC/ES.2 resumes 4 Dec 2026).
     **P2T9 itself has not been edited** — this is Parts 1-18 content and editing it wasn't in scope for this
     build. Flagged in P22T3's verify note; needs Nixon's go-ahead to action.
4. **Part 19 Topic 1** (General Average) vs. **Part 18 Topic 4** — checked and confirmed genuinely
   complementary (P18T4 = definition/Rule A pillars/apportionment/New Jason Clause; P19T1 = lien mechanics/
   Average Adjuster/Rule VII/Rule XXIII time bar). Already flagged in P19T1's original verify note; no change
   needed this pass.

**Confirmed no overlap** (direct full-text grep across all of Parts 1-18, zero hits): Incoterms/Worldscale,
bunker ROB dispute mechanics (VCF/ASTM 54B), ESP/CAS/CAP as a dedicated topic (only scattered single-keyword
incidental mentions in P7T32, P8T34, P14T3, P3T11, P12T53 — none is a dedicated ESP/CAS/CAP treatment),
SIRE 2.0/CDI/TMSA, Kyoto/Paris genesis, e-Certificates, the statutory/commercial/class 3-way distinction,
*The Rafaela S*, ad valorem, Worldscale, CDI-Marine, nitrogen trifluoride, Clean Development Mechanism, BARECON.

**QB links corrected using real matches (not guesses) — all four Parts' `qb_links` updated and rebuilt:**

| Part | QB links (verified via `match_qb.py`) |
|---|---|
| 19 | QB1_A, QB9_A, QB9_B, QB8_A |
| 20 | QB3_A, QB3_B, QB9_B |
| 21 | QB4_A, QB3_A, QB1_B |
| 22 | QB6_E, QB7_C, QB10_B, QB5_A |

**Not done as of the original audit — both actioned later the same day, see §10:**
- Back-links from Parts 1-18 (P3T13, P11T48, P13T2, P15T1, P18T4) pointing forward to the new P19-22
  topics — **added**.
- P2T9's stale NZF date ("November 2026" → "4 December 2026") — **corrected**, 6 occurrences.
