# TRUE SOURCE CORRECTION REQUESTS

**Raised by the consumer team. Nothing here was corrected in place.**

The corpus is read-only to consumers. Handover instruction 12 requires that any error found in
the True Source is reported to the Founder and reviewed before correction. This file is the
consumer-side register of such reports. **Corpus truth flows outward; QP content never overwrites
it, and nothing downstream routes around an entry here.**

| Field | Value |
|---|---|
| Raised | 2026-08-11 |
| Session | `MIW::consumer-team::first-integration` |
| MIW branch | `workflow/corpus-consumer-integration` |
| Corpus commit inspected | `64977b86ed9c601e273f1d0cb55abb0461835811` (`origin/main`) |

---

## TSCR-1 — FSS derivative text is a summary, but the rights record treats it as quotable wording

**Instrument:** FSS Code (`TS-FSS`)

**Objects:**
- `true-source/03-imo-instruments/FSS-Code/consolidated/MIW-FSS-2026.08.08-BUILD-2/MIW_FSS_CODE_CONSOLIDATED_2026.json`
- `true-source/03-imo-instruments/FSS-Code/consolidated/MIW-FSS-2026.08.08-BUILD-1/MIW_FSS_CODE_CONSOLIDATED_2026.json`
- `true-source/source-rights-register.json` → `founderDecisions[FD-RIGHTS-1].corporaCleared[TS-FSS]`
- `MIW_CORPUS_CONSUMER_HANDOVER.md` §4.3(a) and §11

### Expected

`FD-RIGHTS-1` records `TS-FSS` as `operativeToday: true` with
`textObject: …MIW_FSS_CODE_CONSOLIDATED_2026.json`, and clears rendering **the complete text of a
single provision** candidate-facing. Its `permittedForm.nonOfficialStatement` states the required
non-official-status statement is *"already built into the LSA and FSS consolidations"*. The
handover repeats this: FSS verbatim wording is *"obtainable from"* that file, and §11 calls FSS
*"cleared and text-bearing"*.

### Observed

The derivative's own embedded `disclaimer`, **identical in BUILD-1 and BUILD-2** (so it is the
build's declared nature, not a stray string), reads:

> NON-OFFICIAL VERIFIED-INTELLIGENCE CONSOLIDATION — INTERNAL USE ONLY. … the wording here is a
> **verified summary, NOT the official text**. … Not citation-ready until released; **never for
> redistribution**.

The `natureStatement` is consistent with that reading: it certifies *"every provision **statement**"*
as citation-verified against the official rendered page — a verified statement *about* the
provision, not a transcription *of* it.

Three measurements support the same conclusion:

| Measure | FSS BUILD-2 | LSA (for contrast) |
|---|---|---|
| Provisions with no `text` at all | **35 of 421** | 0 of 292 |
| `text` shorter than 40 characters | **22 of 386** | **0** of 292 (shortest is 65) |
| Example short values | `"Section"`, `"test switches"`, `"sea inlet to pump"`, `"monitor throw distance"` | — |
| Per-provision `textSource` | not carried | `official-base-ocr(MSC.48(66)) page-verified` |

Label-shaped entries such as `"Section"` for chapter 9 paragraph 1.2.1 — a *definition* — are
coherent as a requirement digest and incoherent as provision wording.

### Why this is raised rather than worked around

A Founder decision may reclassify MIW's own constructed record. It cannot convert a summary into
the provision's wording. Rendering these strings candidate-facing as the regulation would present
a paraphrase as wording, which `MIW_FOUNDER_AIM.md` rules out directly and which the handover warns
against in §4.3(a) (*"do not paper over it by paraphrasing and presenting the paraphrase as
wording"*).

The two statements also disagree about status: the register says FSS quotation is operative today;
the artifact says INTERNAL USE ONLY and never for redistribution.

### Consumer-side handling in the meantime

`tools/corpus/consumer_adapter.py` classifies `TS-FSS` as `verified-requirement-summary` and
**refuses to mark any FSS provision `quotable`**, while still resolving it, citing it and carrying
its text as **verification evidence**. FSS therefore remains fully useful for confirming
requirements, numerics and amendment attribution — it is simply not a verbatim-quotation source.

A guard test asserts the FSS disclaimer still contains `NOT the official text`. **If a future FSS
build carries genuine verbatim wording, that test fails on purpose**, forcing the classification to
be re-read rather than leaving a stale block in place.

### Requested producer-team action

One of the following, at the Founder's and producer team's discretion:

1. Confirm the artifact is correct and **amend `FD-RIGHTS-1` and handover §4.3(a)/§11** so FSS is
   recorded as verification evidence rather than a verbatim-quotation source; or
2. Build an FSS derivative that carries transcribed provision wording with per-provision
   `textSource` provenance, as LSA already does, and re-point `FD-RIGHTS-1`'s `textObject` at it; or
3. Identify a different FSS text object that the consumer team has not found.

Retiring reservation `FD-RIGHTS-1-R1` by re-sourcing FSS wording to the official MSC resolutions and
the Dec-2019 / Jan-2024 supplements — already recorded as recommended future work — would naturally
resolve this at the same time.

**Blocking?** Not for citation, reference or verification use, which are integrated and tested.
**Blocking for the candidate-facing verbatim provision view on FSS.**

---

## TSCR-2 — Observation, not a defect: no ID→anchor deep link exists for any corpus

Recorded so it is not rediscovered. Consistent with handover §9.2 and verified against the
resolver: 305 of 320 MARPOL Annex VI entries carry `derivativeDestination: null` and the remaining
15 carry prose location descriptors, not anchors. FSS and LSA have bookmarked PDFs but no resolver
entries, so no ID maps to a bookmark.

Consequence for the consumer: `reference_href()` can address an object, but **no viewer route can
land on an exact section** for any instrument today. This is why every pilot shelf entry is
`REFERENCE_PENDING` rather than `REFERENCE_AVAILABLE` — a "Verify source" control that cannot land
on the provision would destroy the confidence the feature exists to build.

**No corpus change requested.** This is a sequencing fact for the viewer decision.

---

> **Entered 2026-08-13, QP2507 laptop review.** TSCR-3 and TSCR-4 were both *raised* by earlier
> paper sessions and recorded in their anchors and in `CURRENT_STATUS.md`, but neither was ever
> written into this register — which is the file the anchors say they were raised in. They are
> transcribed here so the register is the single place a producer-team reader has to look. Nothing
> about either defect is new; only its location is.

---

## TSCR-3 — `MEPC.328(76)` entry into force is recorded a year late

**Instrument:** MARPOL Annex VI, revised — `MEPC.328(76)`

**Raised by:** QP2504 (April 2025) session, 2026-08-13. Referenced and left open by QP2507.

### Expected

`MEPC.328(76)` operative paragraph 3 determines the amendments *"shall enter into force on
1 November 2022"*. Two further held resolutions corroborate that date.

### Observed

Three canonical True Source records give entry into force as `2023-11-01`.

### Why it matters

It is a wrong date inside a frozen register, so nothing downstream flags it: an answer that takes
the date from the corpus is internally coherent and wrong, which is the failure class
`TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md` §8 exists to prevent. Any sitting between
1 November 2022 and 1 November 2023 is decided the wrong way by it.

### Consumer-side handling

The corpus was **not modified**. Papers engaging the date use the resolution's own operative
paragraph. **No QP2507 question depends on it** — Q2 engages the LCA guideline layer, not the entry
into force of the revised Annex VI — so QP2507 references this entry without re-verifying it.

**Status: OPEN.** Producer-team action requested: correct the three records, or record why
`2023-11-01` is right and the resolution's own paragraph 3 is not.

---

## TSCR-4 — the corpus presents a REVOKED instrument as current guidance

**Instrument:** LCA Guidelines — `MEPC.376(80)` (2023) and `MEPC.391(81)` (2024)

**Object:** `true-source/03-imo-instruments/GHG-instruments/INSTRUMENT_LOG.md`

**Raised by:** QP2507 (July 2025) session, 2026-08-13.

### Expected

`MEPC.391(81)`, the *2024 Guidelines on Life Cycle GHG Intensity of Marine Fuels*, adopted
22 March 2024, operative paragraph 5: *"REVOKES the LCA Guidelines adopted by resolution
MEPC.376(80)."* Verified at primary source this session — retrieved from the IMO CDN, 69 pp,
SHA-256 `f7601f21ad7a52404eff7cfc1d2c4a07d4ae03356be1ab57a26a4f23f0634c5f`.

### Observed

The corpus **holds `MEPC.376(80)`, does not hold `MEPC.391(81)`**, and its instrument log lists the
revoked resolution as `GUIDANCE` with no supersession note — although the same table *does*
correctly mark `MEPC.346(78)` as `SUPERSEDED — retain for history`. The log then routes LCA demand
to `MEPC.376(80)` directly.

### Why it matters

**Revoked is not superseded.** A superseded instrument still describes a state of the world; a
revoked one has been withdrawn by the body that made it. Any sitting after 22 March 2024 that
follows the log cites an instrument that had been revoked for over a year.

### Consumer-side handling

The corpus was **not modified**. `QP2507-Q2` uses `MEPC.391(81)` at P1 from the resolution's own
operative paragraphs and departs from the log deliberately. This is a **different record and a
different defect class** from TSCR-3 — that one is a wrong date in a frozen register, this one is a
revoked instrument presented as current guidance — so it is not folded into it.

This finding also upgrades the lineage: `QP2501-Q7` had the supersession right but carried
`MEPC.391(81)` at P2 with the express limitation *"the resolution was NOT read"*. It has now been
read, and the verbatim revocation wording is on the record for the whole lineage.

**Status: OPEN.** Producer-team action requested: mark `MEPC.376(80)` revoked, record
`MEPC.391(81)` as the operative LCA framework, and acquire its text.
