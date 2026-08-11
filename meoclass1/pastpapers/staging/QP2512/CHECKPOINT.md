# QP2512 — STAGING CHECKPOINT

**Paper:** QP2512, December 2025, serial `EM – 2512`.
**Branch:** `pastpapers/qp2512-founder-review`, based on `7e51b97` (`origin/main`, live product lineage).
**Session:** 2026-08-12, laptop production.
**State:** **3 of 9 authored and staged. PARTIAL — SAFE CHECKPOINT.**

> **The canonical spec `specs/QP2512.json` is UNTOUCHED and remains `Intake Complete`.**
> Nothing was partially promoted. `PASTPAPER_PRODUCTION_PROTOCOL.md` §3 admits no half-authored
> canonical state, so the three finished questions live here until all nine are ready.

---

## 1. WHY THE SESSION STOPPED

Not blocked — **out of session capacity, with quality intact.** Six questions remain and five of
them are fresh authoring from primary sources. The session brief's own instruction was to *"not
sacrifice verification quality just to claim completion"*. Stopping at a clean boundary with the
temporal foundation, the donor adjudication and three complete questions banked is worth more than
nine thin ones.

**No question is half-authored.** Each staged object is complete, self-consistent and validates.

---

## 2. WHAT IS DONE

| Item | State | Where |
|---|---|---|
| Machine preflight | done, dry-run only | one stale cluster reported, not reaped |
| Git truth verified | `origin/main` = `7e51b97`, 8 untracked Founder files untouched | — |
| Branch created | `pastpapers/qp2512-founder-review` @ base `7e51b97` | — |
| Source read-back | **complete, 2 of 2 pages**, text layer + 150 dpi render | §4 below |
| Temporal anchor | **complete and primary-verified** | `docs/QP2512_TEMPORAL_AND_DONOR_ANCHOR.md` |
| Donor map | **complete, adjudicated from printed stems** | anchor §5 |
| Reverse-hint sweep | **complete, recorded negative** | anchor §4 |
| Corpus check | commit `64977b8…`, **no demand from this paper** | §6 below |
| **Q1** | **STAGED + verified** | `Q1.json`, `verification/QP2512/Q1.md` |
| **Q2** | **STAGED + verified** | `Q2.json`, `verification/QP2512/Q2.md` |
| **Q9** | **STAGED + verified** | `Q9.json`, `verification/QP2512/Q9.md` |
| Q3–Q8 | **NOT STARTED** — research foundation recorded below | §7 |
| Build / delivery / UI / determinism | **NOT RUN** — correctly, the paper is incomplete | — |

**Probe assembly result:** the three staged objects merged with the six intake questions validate at
**0 errors, 3 warnings**. The warnings are the deferred 450–650 word band (`CURRENT_STATUS.md` §6
item 3), not defects.

---

## 3. THE ONE THING TO READ FIRST ON RESUMPTION

`docs/QP2512_TEMPORAL_AND_DONOR_ANCHOR.md`. Two findings in it are load-bearing and neither is
obvious:

1. **The `A.12xx(34)` family is excluded, and the reason is a DOCUMENT date.** `A 34/Res.1206` was
   adopted 3 December 2025 and **issued 5 December 2025**. The examination date is not printed on
   the source copy, but the exclusion does not depend on establishing it.
2. **The Procedures for Port State Control have THREE editions, not two.** `A.1185(33)` of
   **6 December 2023** is the operative one at this sitting. `A.1155(32)` was revoked in 2023;
   `A.1206(34)` did not exist. **This bites on Q8.**

---

## 4. SOURCE VERIFICATION — COMPLETE, DO NOT REPEAT

| | |
|---|---|
| File | `meoclass1/pastpapers/docs/DECEMBER  - 2025.pdf` (note the **double space**) |
| sha256 | `dd651a5f6533e42800da232688354a8d82fa42cb2cb12e3d04003d5dcfb341e4` |
| Size / pages | 234,066 bytes / 2 pages, born-digital |
| Method | PyMuPDF text layer, **then both pages rendered at 150 dpi and read back visually** |
| Result | **No discrepancy** between text layer and render on either page |
| Serial | `EM – 2512`. Printed month: **`DECEMBER 2025`**. **No day-level date anywhere.** |
| Marks | Every question prints `(16)`. Six answered against a printed `Total Marks – 100` = 96. **Printed discrepancy, reproduced not corrected.** |
| Anomalies | All seven recorded in the intake spec were confirmed as printed. Q3 *"each of the principle"*; Q5 *"how is relayed"*, *"responsible conducting"*; Q7 *"actions you would takes"*, *"the different option you have"*; Q4 host token *"2022/APR/4"*. **Reproduce as printed; do not repair examiner wording.** |

The intake transcription is **character-accurate**. It was verified, not assumed.

---

## 5. DONOR MAP — ADJUDICATED, DO NOT RE-DERIVE FROM THE STORED TIER

The derived reuse map returns **3/9**. It traverses only host-derived edges and is blind to
same-task pairs no host ever linked. Every one of Q3–Q8 was adjudicated by reading printed stems.

| Q | Preferred donor / support | Direction | Relation | Status |
|---|---|---|---|---|
| Q1 | `QP2511-Q3`; shape ref `QP2601-Q6` | forward 1 mo | NEAR | **DONE** |
| Q2 | `QP2511-Q4` | forward 1 mo | EXACT | **DONE** |
| Q3 | `QP2607-Q9`, `QP2606-Q3`, `QP2509-Q3` | mixed | **limb support only** | to do |
| Q4 | **none** | — | fresh | to do |
| Q5 | `QP2601-Q8` / `QP2604-Q8` / `QP2506-Q7` | mixed | **one limb of three** | to do |
| Q6 | `QP2403-Q9`, `QP2510-Q9` — **family, NOT donor** | — | fresh | to do |
| Q7 | **none** | — | fresh | to do |
| Q8 | `QP2508-Q5` (limb 1) + `QP2606-Q2` (limbs 2–3) | forward + **backward** | **composite** | to do |
| Q9 | `QP2509-Q4` | forward 3 mo | EXACT | **DONE** |

**`QP2512` is a FORWARD-pull paper** — the inverse of `QP2511`. Q8 carries the only backwards limb.
The class to expect is therefore **inherited internal `Q`-references**, which travel in both
directions. It has already fired once, on Q2.

---

## 6. CORPUS — CHECKED, NO DEMAND

Private corpus `F:\RulesApp-Local-Input` at **`64977b86ed9c601e273f1d0cb55abb0461835811`**
(= `origin/main`, 0 ahead / 0 behind, tracked tree clean; one untracked local report, not touched).
**No newer producer work is pushed** — the readiness picture in `CURRENT_STATUS.md` §2a stands: LSA
quotation-ready, FSS evidence-only, MARPOL Annex VI citation-only.

**None of QP2512's nine questions cites the LSA Code, the FSS Code or MARPOL Annex VI.** The paper's
instruments are the IHR, the IGF Code, the Marine Insurance Act 1963, the Casualty Investigation
Code, the MS Act 1958, MLC 2006, charterparty law, `A.1185(33)` and the 1993 Liens Convention.
`reference_shelf` therefore stays **empty** on every question, which is the correct outcome and not
an omission. **Corpus availability is not a blocker for this paper.**

---

## 7. RESEARCH FOUNDATION FOR Q3–Q8 — SETTLED, DO NOT RE-DERIVE

### Q3 — Principles of Marine Insurance (16)

Fresh, with limb support. **No donor.** `QP2607-Q9` covers *uberrimae fidei* and disclosure in
depth; `QP2606-Q3` covers warranties and types of loss; `QP2509-Q3` / `QP2506-Q3` cover average.
None of them sets this examiner's task, which is the **set of principles, each with an example**.

**Authority:** the **Marine Insurance Act, 1963 (India)** is the operative statute at this sitting
and is the right anchor for an Indian paper — insurable interest ss.7–8, disclosure and utmost good
faith ss.19–20, indemnity s.3, subrogation s.79, contribution s.80, proximate cause s.55. The UK
MIA 1906 may be named as the source the 1963 Act follows; it must not be substituted for it.
**Temporal: stable.** No Assembly interaction.

### Q4 — Maslow's theory of motivation, and the CE's response (16)

**Fully fresh. No corpus coverage of Maslow at all** — the six "Human Element in STCW and IMO
Fatigue Guidance" objects are a different task and must not be mined as though they were a donor.

**Authority:** `PASTPAPER_PRODUCTION_PROTOCOL.md` **§2.1 governs this question.** No instrument
prescribes a motivation theory. Maslow is management literature and must be attributed as such;
**do not manufacture an IMO or statutory rule** to satisfy a primary-source checkbox. The second
limb (the Chief Engineer's response) may legitimately draw on **STCW Table A-III/2 leadership and
managerial skill competences** and the **ISM Code** for the management framework, and those *are*
regulatory limbs requiring primary verification. Keep the two provenance classes distinguishable.
**Temporal: stable.**

### Q5 — Indian inquiries into casualties on foreign ships (16, three limbs)

Support on **one limb of three**. `QP2601-Q8` / `QP2604-Q8` / `QP2506-Q7` share the **Casualty
Investigation Code** limb and the definitional limb, but they define *very serious marine casualty*
where this stem asks for **marine casualty** — adjacent, not the same. Their spine is flag-State
investigation; this stem's spine is **Indian port-State jurisdiction over foreign ships**.

**Fresh work required on two limbs:**
- **(i)** the **Merchant Shipping Act 1958** sections on inquiries and investigations — Part XII.
  **The 1958 Act governs**; the 2025 Act had not commenced. Read the sections at source.
- **(iii)** what the **marine safety investigation report** consists of and how it reaches the IMO —
  Casualty Investigation Code (`MSC.255(84)`) chapter 14, **SOLAS XI-1/6**, and **GISIS**.

**Temporal: `INDIAN STATUTE BOUNDARY`, flagged HIGH at intake.** The Code is an **MSC** instrument
and is *not* on the Assembly re-issue cycle, so §2 of the anchor does not reach it. Apply the
**premise test** to any support drawn from the 2026 objects.

### Q6 — MLC 2006 minimum requirements, Title 1 (16, four limbs)

**Fresh. `QP2403-Q9` and `QP2510-Q9` are a FAMILY MEMBER, NOT A DONOR** — they ask for the MLC's key
provisions across employment, hours, accommodation, health and welfare, plus enforcement challenges.
This stem asks only for **Title 1**, and its four limbs map one-to-one onto its four Regulations:

| Limb | MLC 2006 |
|---|---|
| (a) minimum age | Regulation 1.1 / Standard A1.1 |
| (b) medical certification | Regulation 1.2 / Standard A1.2 |
| (c) training and qualification | Regulation 1.3 / Standard A1.3 |
| (d) recruitment and placement | Regulation 1.4 / Standard A1.4 |

**Temporal:** the **2022 amendments are in force** (December 2024); the **2025 amendments are
adopted but NOT in force** at this sitting. State the operative text. Note `QP2511-Q3`'s route step 6
already carries verified Standard A1.2 detail — validity two years, one year under 18, colour vision
six years, A1.2(9) three-month continuation — which is **directly reusable for limb (b)**, and is
exactly the material removed from `QP2512-Q1`'s answer layer. **That is the cheapest win in the
remaining six.**

### Q7 — Charterer influence on machinery operation, time charter (16)

**Fully fresh. No corpus coverage.**

**Authority:** largely **§2.1** territory — charterparty practice, standard forms (NYPE), off-hire
and employment clauses, bunker specification (**ISO 8217**, subject to the same no-licensed-copy
limitation recorded on Q2's ISO 20519), planned maintenance and class survey status. The **ISM
Code** supplies the operative management obligation and *is* a regulatory limb. **Do not invent a
regulation governing charterer instructions.** **Temporal: stable.**

### Q8 — Unseaworthy ship, detainable deficiency, PSC release (16)

**The highest-risk question on the paper, and the one with the most work already banked.**

**Limb 1 — unseaworthy ship under the MS Act.** Same sub-task as `QP2508-Q5` / `QP2506-Q9` /
`QP2602-Q5`, all already anchored on the **1958 Act**, so there is **no statute regression to
reverse** — but the premise test still applies. `QP2508-Q5` (August 2025) is the preferred donor:
forward pull, nearest 2025 sitting.

**Limbs 2 and 3 — detainable deficiency, and release procedure.** `QP2606-Q2` (June 2026) is the
natural support and is built **entirely on `A.1206(34)`**. **Every citation drawn from it must be
re-anchored onto `A.1185(33)`.**

**`A.1185(33)` was obtained and read this session.** Downloaded from the IMO resolutions CDN
(`A 33-Res.1185`, 167 pages, adopted 6 December 2023, reissued 5 March 2024 with editorial changes).
Sections read and confirmed present:

| Section | Content |
|---|---|
| 1.7.3 / 1.7.4 | definitions of **deficiency** and **detention** |
| 1.7.11 | **substandard ship** |
| 1.7.7 | **nearest appropriate and available repair yard** |
| 3.1 | identification of a substandard ship, `.1`–`.5` |
| 3.5 | guidance for the detention of ships; flag State and RO notified in writing, **and notified of release** |
| 3.6 | suspension of inspection |
| **3.7** | **rectification of deficiencies and release** — `3.7.1`–`3.7.6`, including the repair-yard route at `3.7.3` |
| 4.1.3 | detention notification content, and release notification content |
| 4.2.1 | flag State informs IMO of remedial action, via **GISIS** |
| **Appendix 2** | **Guidelines for the detention of ships** — §3.3/§3.4 the eleven-point assessment, §4 general, **§5 the detainable-deficiencies list** |

Appendix 2 §3.4's eleven capability tests (navigate safely, operate the engine-room safely, maintain
proper propulsion and steering, maintain adequate stability, maintain watertight integrity, …) are
the natural spine for the *"serious structural deficiencies"* framing this stem prints.

**Note the chapter numbering differs between editions** — `QP2606-Q2` cites `A.1206(34)` §2.3.11 for
the right of appeal and §1.4 for the legal framework. **Locate the equivalents in `A.1185(33)`
directly; do not assume the numbering carried across.**

---

## 8. EXACT RESUME INSTRUCTIONS

```bash
cd F:\Marine-Intelligence-Weekly
git -c safe.directory=* checkout pastpapers/qp2512-founder-review
git -c safe.directory=* status
python tools/pastpapers/health_check.py
```

Then:

1. Read `docs/QP2512_TEMPORAL_AND_DONOR_ANCHOR.md`. **Do not re-derive it.**
2. Read this checkpoint §7 for the question you are authoring. **Do not re-derive the donor map.**
3. Author into `staging/QP2512/Q<n>.json`. For a donor-backed question use the harness:

   ```python
   import sys; sys.path.insert(0, "meoclass1/pastpapers/staging/QP2512")
   import adapt
   adapt.adapt("Q8", donor_id="QP2508-Q5", patch={...})
   ```

   `adapt.adapt()` re-asserts every printed-truth field from the **intake spec last**, after donor
   inheritance and after the patch. Do not bypass it — that guard is what stops a donor's
   `host_recurrence_hint` entering this paper's recurrence intelligence.
   For a fresh question call `adapt.adapt("Q4", patch={...})` with no `donor_id`.
   **The harness writes LF.** Do not write staged JSON with a bare `open(...,'w')` on Windows.
4. Write `verification/QP2512/Q<n>.md` in the same pass. `validate_spec.py` errors without it.
5. Check as you go: `python meoclass1/pastpapers/staging/QP2512/adapt.py check`
6. **When and only when all nine are staged:**

   ```bash
   python meoclass1/pastpapers/staging/QP2512/adapt.py assemble
   python tools/pastpapers/run_toolchain.py
   ```

   `assemble` refuses unless all nine pass their intake assertions, then promotes them into
   `specs/QP2512.json` and sets `build_state` `Pilot Review Ready`, `review_state`
   *"Awaiting Founder Review - complete paper"*, `version` `1.0`.
7. Then the paper sweeps (`temporal_sweep.py`, internal `Q`-reference, donor contamination,
   authoring-date leakage), the delivery build, determinism double-build, and local UI review at
   1280 and 375. **None of these has been run and none should be, until the paper is complete.**
8. **Retire `staging/QP2512/` once promoted**, as `QP2511` did.

### Known dependency

`Q1.json` cross-links to `QP2512.html#q8`. **`health_check.py` will fail link resolution until Q8 is
authored.** This is intended, not a defect — it is the link-integrity check doing its job.

---

## 9. WHAT WAS DELIBERATELY NOT DONE

- **The canonical spec was not touched.** No partial promotion.
- **No build of any kind was run** — `PASTPAPER_PRODUCTION_PROTOCOL.md` §4: build only when the
  paper is complete; partial builds create misleading artefacts.
- **`solvedQP/` was not regenerated.** QP2512 correctly remains `PLANNED_SOON` on the coverage
  surface. It must not be advertised as available.
- **No security, Vercel, secret, middleware or environment change.** Out of scope, untouched.
- **The eight Founder-review untracked files were not added, deleted, moved or modified.**
- **The six desktop-allocated 2024 papers** (`QP2401`, `QP2412`, `QP2402`, `QP2409`, `QP2411`,
  `QP2410`) **were not touched.** No branch of theirs was created, read into or modified.
- **No merge to `main`, no deployment.**
- **The stale session cluster found at preflight was reported, not reaped** — governed dry-run only,
  per the session brief.
