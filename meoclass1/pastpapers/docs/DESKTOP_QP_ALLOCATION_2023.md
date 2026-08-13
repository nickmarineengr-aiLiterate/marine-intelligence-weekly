# DESKTOP QP ALLOCATION — 2023 (BATCH 4)

**Written 2026-08-13. The 2023 sittings are the FINAL set MIW will solve and publish.**
Authority for how to build a paper is `DESKTOP_QP_PRODUCTION_PLAYBOOK.md`. This file says which
papers, in what order, and what is structurally different about the 2023 year. Where the two
disagree, the playbook wins.

> **Do not start this batch until QP2407 and QP2408 are live.** See
> `DESKTOP_QP_HANDOVER_BATCH3.md`. Those two close the 2024–2026 corpus and their donors matter
> to 2023. **This gate was released in part by Founder instruction on 2026-08-13 — see §0.2.**

---

## 0. BATCH 4 BASELINE — recorded 2026-08-13

### 0.1 The baseline commit

| | |
|---|---|
| **MIW Batch 4 baseline** | **`57b9342c0b6782b6eb8c44fd996bbaef08f250fa`** (`57b9342`, *Review QP2407 against MIW True Source*) — `main` |
| **How it is proven** | **This commit's PARENT is the baseline.** Same self-verifying pattern as Batch 1 (`9c97359`), Batch 2 (`333e814`) and Batch 3 (`e5843b1` recorded by `1401b13`). No commit asserts its own hash |
| **Baseline branch** | `pastpapers/batch4-baseline` |
| **Built state AT the baseline** | **28 papers · 252 questions · 243 built** — 27 papers `Pilot Review Ready`, `QP2408` alone at `Intake Complete` (0/9) |
| **Tracked tree** | clean, 0 ahead / 0 behind `origin/main`, no git operation in progress |

**Do not reuse an older batch baseline.** `e5843b1` (Batch 3) predates the QP2407 integration, so a
2023 branch cut from it would compute donor readiness against a corpus one whole paper short.

### 0.2 Two deviations from this file, both by explicit Founder instruction

Recorded because the session prompt overrides governed workflow under
`PRODUCTION_PROTOCOL_INDEX.md` §1, and an override that is not written down becomes an
undocumented precedent.

1. **The batch opened before QP2408 was live.** The header gate above requires QP2407 *and* QP2408.
   At the baseline **QP2407 is live on `main`** (integrated, 9/9) but **QP2408 is not** — it is
   authored 9/9 on `pastpapers/qp2408-founder-review` at `0f78df1`, pushed and awaiting laptop
   review. The QP2408 donors are therefore **unavailable to this paper** and none is claimed.
2. **QP2301 was built first, not third.** §5 recommends `QP2312 · QP2304 · QP2301 · …` and warns
   *"Do it once the team is warmed up, not first"* because of the §1.3 printed numbering variants.
   The Founder allocated QP2301 as the opening paper. The numbering variants were handled at
   transcription and are recorded in the spec and in `QP2301_TEMPORAL_AND_DONOR_ANCHOR.md`.

### 0.3 The readiness figures in §4 are stale — recompute, do not read

§4 was computed against **234 built questions across 26 papers**. The baseline holds **243 across
27**, because QP2407 has since been integrated. Every "with a donor" count in §4 is therefore a
*lower* bound taken at a different corpus state. **Recompute readiness for each paper at the moment
you author it**, exactly as §2 already requires within the batch.

---

## 1. THE 2023 INTAKE — what was acquired and audited

Acquired 2026-08-13 from the same third-party host as every other source copy. **Eleven papers,
not twelve.** All eleven were audited before allocation.

| Verified at intake | Result |
|---|---|
| Subject | **All eleven are `ENGINEERING MANAGEMENT`**, Function: Marine Engineering Management at Management Level, M.E.O Class I |
| Rubric | All eleven print *"Answer SIX questions only"*, *"All questions carry equal marks"*, `Total Marks – 100` |
| Pages | 2 pages each |
| Questions | **9 per paper on all eleven**, confirmed by reading, not by pattern count |
| Region note | `(India 2023)` |
| Integrity | All eleven downloaded as valid PDFs; SHA-256 recorded |

Source files are at `meoclass1/pastpapers/docs/<MONTH> 2023.pdf` and are **git-ignored**. Local
filenames, host filenames, printed serials and hashes are recorded in
`verification/LOCAL_SOURCE_PROVENANCE.md`, which is also git-ignored. **This repository is public —
never commit a source PDF and never name the host in a committed artefact.**

### 1.1 The serial convention is REVERSED in 2023

2024 and later print `Sr. No. EM – 2406`. **2023 prints `2301 EM`** — number first, no `Sr. No.`
prefix, no dash. Record `printed_serial` exactly as printed. Do not normalise it to the 2024 shape
and do not write a parser that assumes one form.

### 1.2 May 2023 does not exist — and this is now a three-year pattern

The host publishes eleven papers and the printed serials run **2304 → 2306 with nothing at 2305**.
That is the same serial-gap evidence that established `NO SITTING` for May 2025 (…2504, 2506…).
**May is now absent in 2023, 2024 and 2025.** Record May 2023 as `NO SITTING` on evidence, exactly
as May 2024 and May 2025 are recorded — never as "missing" or "not yet acquired".

### 1.3 Printed numbering is inconsistent in 2023 — preserve it, do not tidy it

The 2023 papers do not number their questions uniformly, and an automated extractor under-reads
two of them. **This is the printed source, not damage.** Confirmed examples:

| Paper | What is printed | Do |
|---|---|---|
| January (`2301`) | Q1–Q7 as `Q1.`…`Q7.`, then **`Q8)`**, then a bare **`9.`** | Transcribe all nine; keep the printed forms |
| February (`2302`) | Q1–Q3 and Q6–Q9 with `Q`, but **`4.`** and **`5.`** bare | Transcribe all nine |
| February Q3 | *"Phase 2 ( f 20% - 30% reduction)"* — a stray `f` | Preserve; do not silently repair |
| February Q4 | *"How is the amount of award calculated .JS per this form?"* — `.JS` for "as" | Preserve |
| January Q2 | limbs run **a) then c)** — no b) | Preserve; note the printed gap |

**The house rule is unchanged: printed errors are preserved and recorded, never corrected.** A
candidate sitting that paper saw exactly this.

---

## 2. THE SYSTEMIC FACT ABOUT 2023 — read this before anything else

> **Every 2023 paper pre-dates the entire solved corpus. Every donor available to any 2023
> question is LATER than the sitting it is donating to. There are no exceptions until a 2023 paper
> is itself solved.**

MIW's solved set runs 2024 to 2026. The normal MIW case — a donor that pre-dates its recipient and
therefore *cannot* drag later law backwards — **does not occur anywhere in this batch at the
start.** This is the QP2406 situation applied to eleven papers instead of one.

The standing rule for the whole batch, on every question:

> **No donor statement is inherited. Every sitting-relative statement is re-derived from the 2023
> position and the re-derivation is recorded in that question's `temporal_review`.**

A donor is a **route** — the shape of the answer, the limbs, the order — not prose to be carried
across. QP2406 proved this is survivable and produced a clean paper by working exactly this way;
read `QP2406_TEMPORAL_AND_DONOR_ANCHOR.md` §1 and §8 before starting.

**As 2023 papers are solved they become each other's safe donors**, because they sit in the same
year. Expect readiness to improve within the batch, and recompute it rather than trusting the
table in §4.

---

## 3. TEMPORAL ANCHOR — 2023 SITTINGS

Build a per-paper anchor. These boundaries are shared across the year.

### Operative during 2023

- **Merchant Shipping Act, 1958.** The 2025 Act commenced 15 March 2026 — roughly **three years**
  after these sittings. It is the standing statute trap for the whole batch.
- **32nd IMO Assembly** (adopted **December 2021**) governs the first eleven months. The **33rd
  Assembly adopted 6 December 2023** — so it is **future for every 2023 sitting except December**,
  and even for December the adoption date must be checked against the sitting. `A.1155(32)` PSC
  procedures, not `A.1185(33)`.
- **EEXI and CII in force from 1 January 2023** — operative for the whole year and squarely in
  scope (February Q3 is an EEXI/CII question). `MEPC.328(76)` is the governing Annex VI revision.
- **MEPC.346(78)** 2022 SEEMP guidelines — operative.
- **ISM Code** as amended through `MSC.353(92)`.
- **MLC 2006 as amended through the 2018 set** — the 2022 amendments enter force 23 December 2024.
- **MEPC 79** (Dec 2022) past; **MEPC 80 (3–7 July 2023)** adopted the **2023 IMO GHG Strategy** —
  a mid-year boundary, see below.
- 0.50 % m/m sulphur limit; Anti-Fouling Convention as amended (**cybutryne controls applied from
  1 January 2023**).

### The mid-year boundary that splits this batch

> **MEPC 80 adopted the 2023 IMO GHG Strategy on 7 July 2023.**
> Before it, the operative instrument is the **Initial GHG Strategy of 2018**.

- **January, February, March, April, June 2023 → Initial Strategy 2018.**
- **July 2023 → check the sitting against 7 July.** The paper prints `JULY 2023` with no day, so
  **the day is unknown and a day-dependent claim cannot be made.** Treat this exactly as trap 17
  requires: state the position without asserting which side of 7 July the sitting fell, or anchor
  the answer on material unaffected by the change.
- **August–December 2023 → 2023 Strategy operative.**

This is the single most important intra-year boundary in the batch and it is invisible to any
detector, because a month-only sitting carries no day.

### Future during 2023 — PROHIBITED

| Item | Date |
|---|---|
| SOLAS Consolidated Edition 2024 | 1 July 2024 |
| MLC 2022 amendments | in force 23 Dec 2024 |
| **Hong Kong Convention** | in force **26 June 2025** — not in force anywhere in 2023 |
| MEPC 81 / 82 / 83 | 2024–2025 |
| 33rd Assembly `A.11xx(33)` | adopted 6 Dec 2023 — future for Jan–Nov |
| 34th Assembly `A.12xx(34)` | adopted 3 Dec 2025 |
| IMO Net-Zero Framework / GFI | Oct 2025 |
| **Merchant Shipping Act, 2025** | commenced 15 Mar 2026 |
| MSC 108 resolutions | adopted May 2024, in force 1 Jan 2026 |

**The corpus register inversion is worse here than for 2024.** The register is maintained for the
present; for a 2023 sitting a great many "superseded" markings are the operative instrument, and
the "current" edition is future by two or three years. Check direction on every consumption.

---

## 4. THE SIX ALLOCATED PAPERS

Selected by **donor readiness recomputed on 2026-08-13 against the full 234-question solved
corpus** — not by chronology. Ranked most-ready first.

| # | Paper | Sitting | Serial | Exact/near | Family | **With a donor** | Notes |
|---|---|---|---|---|---|---|---|
| 1 | **QP2312** | December 2023 | `2312 EM` | **9** | 0 | **9 / 9** | Fully donor-covered |
| 2 | **QP2304** | April 2023 | `2304 EM` | 7 | 0 | **7 / 9** | Dense legal paper |
| 3 | **QP2301** | January 2023 | `2301 EM` | 6 | 1 | **7 / 9** | Printed numbering variants |
| 4 | **QP2303** | March 2023 | `2303 EM` | 5 | 1 | **6 / 9** | |
| 5 | **QP2309** | September 2023 | `2309 EM` | 4 | 2 | **6 / 9** | |
| 6 | **QP2302** | February 2023 | `2302 EM` | 3 | 3 | **6 / 9** | Most printed anomalies |

### Not allocated in this batch, and why

| Paper | With a donor | Why deferred |
|---|---|---|
| QP2310 October | 5 / 9 | Batch 5 |
| QP2307 July | 5 / 9 | **Straddles the 7 July GHG boundary** — hold until the batch has practice |
| QP2308 August | 4 / 9 | Batch 5 |
| QP2306 June | 3 / 9 | Batch 5 |
| QP2311 November | 2 / 9 | **Least ready paper in 2023** — do last, once 2023 papers can donate |

**QP2307 is deliberately deferred despite ranking joint-seventh on donors.** Its sitting month
contains the GHG Strategy adoption date and it prints no day. That is a judgement call best made
after the team has built several 2023 anchors, not on the first pass.

---

## 5. RECOMMENDED ORDER — 1 → 6

**QP2312 · QP2304 · QP2301 · QP2303 · QP2309 · QP2302**

Reasoning:

1. **QP2312 first.** Nine of nine questions have an exact or near donor — the highest coverage of
   any unsolved paper MIW holds. It is also **December**, so the 33rd Assembly question is live and
   worth settling early, and it is the one 2023 paper where the 2023 GHG Strategy is unambiguously
   operative. Getting it done first banks the year's hardest temporal reasoning while the batch is
   fresh.
2. **QP2304 second.** Seven donors, and it is a heavily legal paper — bauxite carriage, HNS,
   general average, collision, maritime lien, Bunker/CLC, classification societies. Its donors are
   concentrated in `QP2509` and `QP2503`, so the corpus reading is efficient.
3. **QP2301 third.** Strong coverage, but it carries the printed numbering variants in §1.3 and
   needs careful transcription. Do it once the team is warmed up, not first.
4. **QP2303, QP2309, QP2302** in that order — steadily thinner donor coverage and more fresh
   research.

**QP2302 last of the six**, because it has the most printed anomalies *and* the thinnest exact
coverage — three exact and three family.

### Known relations worth reading before authoring

| 2023 question | Donor | Sitting | Distance |
|---|---|---|---|
| `QP2303-Q9` lubricating oil analysis | `QP2406-Q9` | June 2024 | +15 months |
| `QP2303-Q3` perils of the sea, due diligence | `QP2503-Q5` | March 2025 | +24 months |
| `QP2304-Q3` particular and general average | `QP2509-Q3` | September 2025 | +29 months |
| `QP2304-Q1` bauxite in bulk carriers | `QP2509-Q1` | September 2025 | +29 months |
| `QP2301-Q2` anti-fouling convention | `QP2404-Q5` | April 2024 | +15 months |
| `QP2309-Q4` IMO structure and hierarchy | `QP2502-Q1` | February 2025 | +17 months |
| `QP2309-Q8` UNCLOS and marine environment | `QP2404-Q9` | April 2024 | +7 months |
| `QP2312-Q7` PSSA and Indian island habitats | `QP2502-Q9` | February 2025 | +14 months |

**Every one of these is a later donor.** Note the distances — several exceed two years. The
further a donor sits from its recipient, the more of its prose is unusable.

---

## 6. WHAT TO CARRY FORWARD FROM QP2406

QP2406 is the closest precedent in the corpus: it was the earliest paper in the set, its donors all
ran backwards, and it came through clean. Reuse its method, and avoid the five defects its review
caught.

1. Never name the source host in a committed artefact, **including the verification records**.
2. Derive summary counts from the detail table **last**, not first.
3. Keep production vocabulary — *donor*, *before publication*, *reverify*, *production protocol* —
   out of every candidate-facing field. Provenance claims (*"the corpus does not hold X"*) are a
   separate class and are Founder-held: **leave them as they are**.
4. Rule 4: no regulation, resolution, article or section numbers and no sitting-specific dates in
   `understand_first`. A statute's own name with its year is fine. The knowledge map is derived and
   is not governed by Rule 4.
5. **No week-granularity distance from a month-only sitting.** Every 2023 paper prints a month and
   no day. This bites hardest at the 7 July 2023 GHG boundary.

Additionally, for this batch specifically:

6. **A low similarity score means the wording differs, not that no donor exists.** Read the family
   before concluding a question is fresh research.
7. **Record `NO SITTING` for May 2023 on serial-gap evidence**, in the same words used for May 2024
   and May 2025.

---

## 7. BRANCH AND ARTEFACT RULES

- One branch per paper: `pastpapers/qp2312-founder-review`, `pastpapers/qp2304-founder-review`, …
- **One paper at a time. 9/9 before the next.**
- A paper branch commits **only its twelve paper-owned files**. No global derived artefact — no
  reuse map, manifest, index, year sheet, topic sheet or `solvedQP/` page. The laptop regenerates
  those and will reject a branch that carries them.
- **Never commit a source PDF.** The repository is public.
- Push and stop. The laptop reviews, integrates by path extraction onto current `main`, publishes.
  Desktop branches are never merged; they are retained as provenance.

---

## 8. STOP GATE

**Stop after the sixth paper and report.** Batch 5 is the remaining five — QP2310, QP2307, QP2308,
QP2306, QP2311 — and its order must be **recomputed** once these six are live, because six new
same-year papers will change every readiness figure in §4.

When all eleven are published the corpus is **39 papers · 351 questions** — the present 28 papers
and 252 questions, plus eleven 2023 sittings at nine questions each — and the Written product is
complete as scoped.
