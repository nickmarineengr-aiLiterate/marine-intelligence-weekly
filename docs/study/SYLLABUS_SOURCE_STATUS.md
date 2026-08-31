# Official DGMA syllabus — source status

**Status: FINAL OFFICIAL SOURCE INGESTED AND VERIFIED.**
Recorded 2026-08-22 on `review/dgma-study-spine-final`, from production main
`0d4fd7d`. Supersedes the 2026-08-22 revision written at `906e8a4`.

This file reports six independent things. They were previously entangled, and
that is what produced a misleading headline. Read them separately.

## 1. Final official circular — EXISTS, VERIFIED AT SOURCE

| Field | Value |
|---|---|
| Instrument | DGMA EAC Branch Circular **No.49 of 2026** |
| File number | F.No. 13-11028/1/2026-ENGG-DGS |
| Issuer | Directorate General of Maritime Administration, Mumbai |
| Subject | Preparatory courses for MEO and ETO grade of CoC examinations, reg. |
| Issue date | **15 August 2026** |
| MEO Class I syllabus | **Annexure III**, PDF pages 24–30 |
| Course duration | Two months (8 weeks, 40 working days, 240 contact hours) |
| Official nodes | **25** numbered syllabus items |
| Effective from | **01 January 2027** |
| Source URL | <https://dgma.gov.in/download/1787368075_6a89128b56069_1-eac-branch-circular-no-49-of-2026-on-preparatory-courses-for-meo-eto-grade-of-coc-examinations.pdf> |
| Listing | <https://dgma.gov.in/engineering-wing/ew-dgs-eac-circulars-orders-notices-engineering> |
| SHA-256 | `07170f572c99064fad25eedb0fe985886248a81a49b4eb5d4711fd38d186f44d` |
| Size / pages | 1,298,819 bytes / 33 pages |
| Acquired | 2026-08-22 |

The PDF was downloaded from the official site and **read**, not inferred from
a listing or a search snippet. Circular number, issue date, subject, annex
structure, Annexure III identity, duration and effective date were all
confirmed against the document's own text.

**Annexure III == MEO Class I: YES.** The circular states at Part A §V.5 that
"the revised course frameworks and syllabi for the MEO Class-II and MEO
Class-I Preparatory Courses are enclosed as Annexure-II and Annexure-III,
respectively", and Annexure III is headed *Syllabus for MEO Class I
Preparatory Course*.

## 2. Ingestion status — COMPLETE

`tools/study/ingest_official_syllabus.py` verifies the pinned SHA-256 and
extracts Annexure III into `docs/study/official_syllabus.json` — 25 nodes,
2,452 words of official wording, each carrying `official_node_id`,
`official_order`, `official_parent`, `source_page`, `source_digest`,
`syllabus_version`, `status` and `effective_from`.

The source PDF is **deliberately not committed** (`docs/study/sources/*.pdf`
is git-ignored): this repository is public and the instrument is served freely
by DGMA. The digest is committed instead, which is what makes the extraction
auditable without republishing the file.

## 3. Draft status — SUPERSEDED, HISTORICAL ONLY

An official **draft** dated 28-Jul-2026 also exists
(`b6365d2205428f34283b9e259c8a130b4b4dfd2072f52cd1d96141348a21d09c`). It is
**not** a safe substitute for the final, and the difference is substantive,
not cosmetic:

| Comparison | Result |
|---|---|
| Draft Annexure III items | **23** |
| Final Annexure III items | **25** |
| Items unchanged | 8 |
| Items with minor text change | 5 |
| Items substantively changed | 12 |
| Items new in final | 2 — casualty investigation (24), underwater noise (25) |

Other substantive final-only additions include the RO Code and
classification societies' duty of care (item 3); the Universal Declaration of
Human Rights and ICCPR in the MLC/ILO item (8); detention review panels and
appeal procedures (9); sensor-technology fundamentals (16); dual-fuel engines
and alternative-fuel supervisory competence (21); EU-waters GHG restrictions
(22); and management-level cyber-risk oversight under the ISM Code (23).

A system that quietly fell back to the draft would therefore be teaching a
syllabus missing two whole subjects. `tools/study/ingest_official_syllabus.py`
pins the draft's digest too, so that specific reversion fails **by name**.

## 4. Prior Desktop-derived artefacts — NOT FOUND ON ACCESSIBLE LAPTOP STATE

A session brief once asserted that a Desktop Claude stream had already built
syllabus extraction, an old→new crosswalk, a `syllabus_check`, exam-alignment
logic and a status-driven dual-version public builder. An exhaustive search
(every local and remote ref, `git fsck --dangling`, the working tree including
ignored paths, every other repository on `F:`, and all prior session
transcripts) found none of it.

That finding stands, and its correct scope is:

> **NOT_FOUND_ON_ACCESSIBLE_LAPTOP_STATE.** Desktop-local state is not
> verifiable from this machine.

It is **not** evidence that the artefacts never existed, and — critically — it
was never evidence about the circular. The two questions are independent.

## 5. What the previous revision got wrong

The superseded revision was scoped correctly in its body. It said plainly:

> "The existence and contents of Circular No. 49 of 2026 are **neither
> confirmed nor denied here** — only that this repository holds no copy."

That sentence was accurate and is why nothing downstream had to be un-taught.
Two things were nonetheless wrong:

1. **The headline over-reached its evidence.** A file titled *"NO OFFICIAL
   SOURCE EXISTS"* reads, at a glance and in every later summary of it, as a
   finding about the world rather than about this repository.
2. **The search never left the repository.** It queried refs, dangling
   objects, local disk and transcripts — all of which can only ever establish
   "not ingested here" — and never queried the issuing authority. The
   circular was, at that moment, published and downloadable.

The operative lesson is recorded in `tools/study/SKILL.md`: absence in a
corpus is not absence in the world, and only the issuer can settle the
existence of an instrument.

One environmental fact made this trap easy to fall into and is worth stating
plainly: **the authority now publishes at `dgma.gov.in`, not
`dgshipping.gov.in`**, and the old host refuses connections. Worse, two
listings on the official site disagreed — the site-wide circular index still
showed only the July draft and skipped from 48 to 50, while the Engineering
Wing branch listing carried the final Circular 49 correctly. The branch
listing plus the PDF itself are authoritative.

## 6. Effective-date model — ADOPTED, NOT YET OPERATIVE

As at 2026-08-22 there are **two live syllabus versions** and they must not be
collapsed:

| Version | Meaning | Status today |
|---|---|---|
| `MIW-DERIVED-1.0` | The MIW topic spine derived from the governed corpora | **Currently operative** |
| `DGMA-C49-2026-ANNEX3` | The official revised syllabus | **FINAL_ADOPTED_NOT_YET_EFFECTIVE** until 2027-01-01 |

Until 01-Jan-2027 no public surface may describe the revised syllabus as being
in force. The official layer is authoritative as to **scope**; it becomes
authoritative as to **applicability** on 01-Jan-2027.

## 7. What this means for the study layer

The study spine remains the durable join layer, but it is no longer the top of
the stack. The architecture is now:

```
DGMA Circular 49 / Annexure III   (official scope, 25 nodes)
        ↓  official → topic crosswalk
canonical MIW topics              (10 domains, the study/join layer)
        ↓
oral + written questions → examiner & question intelligence → study packs
```

Official wording lives only in `official_syllabus.json` and is never
paraphrased. MIW topic labels are normalized study headings and are **not**
required to match DGMA headings — they answer different questions.

## 8. Draft source — ABSENT, AND THE DRAFT-TO-FINAL CROSSWALK IS UNVERIFIED

`docs/study/official_change_crosswalk.json` now exists as the machine-readable
draft-to-final relationship layer. It is **distinct** from
`docs/study/official_crosswalk.json`, which remains the official-node to
MIW-topic layer and is untouched by it.

**The 28-Jul-2026 draft PDF is not in this repository.** Only its digest
(`b6365d2205428f34283b9e259c8a130b4b4dfd2072f52cd1d96141348a21d09c`), its
issuing date, its source listing and its item count of 23 are pinned. No draft
text has been extracted, so **no tool in this repository has performed an
item-to-item comparison between the draft and the final.**

The draft side of every record in the change crosswalk therefore rests on the
narrative table in section 3 above, and on nothing else. Consequently every
record carries:

| Field | Value |
|---|---|
| `classification` | `AMBIGUOUS` |
| `provenance` | `NARRATIVE_UNVERIFIED` |
| `review_required` | `true` |
| `source_verified` | `false` |

The narrative counts in section 3 — 8 unchanged, 5 minor, 12 substantive, 2 new
— are reproduced in that file but are **not adopted**. They are also internally
unreconciled: 8 + 5 + 12 = 25, with 2 new listed in addition, which matches
neither 23 draft items nor 25 final items. That discrepancy is reported rather
than repaired, because only the draft source can settle it.

**This layer awaits source acquisition.** Acquiring the draft was explicitly
out of scope for the job that built this file, and no network request was made.
When the draft is acquired, `tools/study/build_official_change_crosswalk.py` is
where the real comparison belongs, and the classification vocabulary
(`UNCHANGED / RENAMED / MOVED / MERGED / SPLIT / EXPANDED / REDUCED / NEW /
REMOVED`) is already declared there for it.

## 9. D07 (Cargo Operations & Bulk Carriage) — UNADJUDICATED HYPOTHESIS

**Observable fact.** Domain D07 carries no Annexure III edge of any role in
`docs/study/official_crosswalk.json`. That is a property of the governed
crosswalk and it is checkable.

**Unadjudicated hypothesis.** A comment in `tools/study/mapping_engine.py`
explains that absence by asserting that cargo is a Class II subject. That is a
substantive claim about the DGMA syllabus. **No adjudication record in this
repository supports it, and nothing here establishes it.** It is carried in a
code comment, which is not a governed decision surface.

The comment has deliberately **not been deleted** — it is the reasoning that
was actually used and removing it would hide the provenance of a decision. It
has been labelled in place instead. Accordingly:

- no output of this repository asserts as governed truth that cargo has no
  Annexure III home because it is a Class II subject;
- D07-related mappings are carried as `AMBIGUOUS_MAPPING` pending
  adjudication, and appear under `domains_without_official_home` in
  `docs/study/syllabus_gap_register.json` with `review_required: true`;
- settling this requires a human adjudication against the circular, not a
  build.
