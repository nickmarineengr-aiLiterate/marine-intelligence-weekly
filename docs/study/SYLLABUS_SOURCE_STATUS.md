# Official DGMA syllabus — source status

**Status: NO OFFICIAL SOURCE EXISTS IN THIS REPOSITORY.**
Recorded 2026-08-22 at main `906e8a4`.

This file exists because a session brief asserted that substantial DGMA MEO
Class I syllabus work already existed here, created by an earlier Desktop
Claude stream, and that it was ready to be reviewed and promoted. **That
premise did not survive verification.** Any future session that is told the
same thing should read this file before spending a session looking for it.

## What the brief asserted

- DGMA EAC Branch Circular **No. 49 of 2026**, dated 15-Aug-2026
- MEO Class I syllabus at **Annexure III**, effective **01-Jan-2027**
- Status ADOPTED / FINAL but not yet in force
- Existing repository artefacts: syllabus extraction, an old→new crosswalk,
  a status module, `syllabus_check`, exam-alignment logic, a public builder
  with "status-driven dual-version handling"
- That earlier "no final circular found" conclusions were obsolete

## What the repository actually contains

Nothing of the above. The search was exhaustive, in this order, because a
filename grep of one working tree is the weakest possible evidence and this
project has previously found committed data living only on an unmerged branch:

| Search | Scope | Result |
|---|---|---|
| Filenames `*syllab*`, `*dgma*`, `*annexure*`, `*crosswalk*` | every local ref + every remote ref | only `merchant-shipping-act-2025-crosswalk.md`, unrelated |
| `git ls-remote --heads origin` | 90 remote heads, authoritative | no syllabus/topic/study branch |
| `git fsck --dangling` | 31 dangling commits | none syllabus-related |
| Working tree, incl. git-ignored | `F:\Marine-Intelligence-Weekly` | no match |
| Every other repo/dir on `F:` | RulesApp, miw-true-source, MIW-Magazine-Production, MIW-Telegram-Assistant, RulesApp-Local-Input, AI, Production-Toolkit, NIXON, Ongoing | no match |
| Content grep `Circular No.49`, `EAC Branch`, `Annexure III` | main | one hit: a `QB4_A.html` reg-item about the DGMA EAC Branch nautical wing — not a syllabus |
| All prior Claude session transcripts | `~/.claude/projects/` | one hit: a **web-search result** from 2026-08-16 describing a *draft* EAC circular on **GME course eligibility** — a different instrument entirely |
| Markers `MEO1-SYL`, `syllabus_check`, `syllabus_node` | all transcripts | appear **only** in the session brief that asserted them |

`tools/pastpapers/topic_taxonomy.py` states in its own docstring that it holds
"no question ids, no counts and no syllabus of its own."

## Conclusion

There is no official DGMA syllabus artefact, no structured extraction, no
old→new crosswalk, no `syllabus_check` and no dual-version status model in
this repository — on any branch, in any dangling object, or on disk. The
earlier "no final circular found" conclusion was **not** obsolete; it is what
the evidence still supports.

The existence and contents of Circular No. 49 of 2026 are **neither confirmed
nor denied here** — only that this repository holds no copy and no derived
artefact. It may well exist in the world. It has never been ingested.

## What this means for the study layer

The study spine in this directory is **MIW-DERIVED**, not official. It is
built from the two corpora MIW actually governs — 40 solved written papers
(360 questions) and the 721-question oral corpus — and it says so in every
record it emits.

The data model already carries the official layer as empty, load-bearing
fields, so ingesting the real instrument later is an **addition, not a
restructure**:

- every domain carries `official_syllabus_nodes: []` and
  `syllabus_status: "NO_OFFICIAL_SOURCE_IN_REPO"`
- every mapping record carries `syllabus_version: "MIW-DERIVED-1.0"` and
  `syllabus_node_id: null`
- `validate_study_spine.py` **fails** (rule `R-OFFICIAL`) if any domain claims
  official nodes while this status stands, and `mapping_engine.validate_mapping`
  rejects a record that sets `syllabus_node_id` under the same status

So the layer cannot silently start claiming DGMA authority it does not have.

## Required next action (blocking for official alignment only)

Obtain the primary instrument — not a summary, not a search snippet:

1. the actual circular PDF from the DGMA circulars listing, with its download
   URL and retrieval date recorded;
2. confirm number, date, the Annexure that carries MEO Class I, and the
   effective date;
3. preserve the official bytes distinctly from MIW judgement;
4. extract structured nodes and assign stable `syllabus_node_id`s;
5. populate `official_syllabus_nodes`, bump `SYLLABUS_VERSION`, and re-run
   `build_study_mappings.py --force`. Every existing mapping is then reported
   as `STALE` by `--status` and re-derived; nothing is silently stranded.

**Until step 5, no MIW surface may describe any topic list as "the DGMA
syllabus".** Topic 01 is study-ready without it: the exam is set from the same
body of law the corpus already covers, and the corpus is real evidence of what
is actually asked.

## Two-version model (2026 vs 01-Jan-2027)

The dual-version requirement is **designed for but not populated**, because
neither version exists here yet. `syllabus_version` is the discriminator and
`classify_against_taxonomy()` already reports `STALE` / `ORPHANED_NODE` /
`MIGRATED` so that a version change re-reviews rather than strands historical
questions. When both syllabi are ingested, a question keeps one mapping per
`syllabus_version`; the old syllabus is never overwritten, because a past
paper must stay judged against the syllabus in force at its sitting.
