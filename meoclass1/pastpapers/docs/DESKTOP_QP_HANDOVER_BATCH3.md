# DESKTOP QP HANDOVER — BATCH 3 (QP2407, QP2408)

**Written 2026-08-13, immediately after QP2406 went live and closed Batch 2 at 6/6.**
Authority for how to build a paper is `DESKTOP_QP_PRODUCTION_PLAYBOOK.md`. This file says
**which** papers, **in what order**, **from what baseline**, and **what is different about them**.
Where the two disagree, the playbook wins.

---

## 1. CORPUS TRUTH AT ALLOCATION

| | |
|---|---|
| **Baseline commit** | `e5843b1` on `main` — the state after QP2406 was published |
| **Product** | **26 available papers · 234 published questions** |
| **Corpus** | 252 questions · 234 solved · **18 unsolved** |
| **Unsolved** | `QP2407` (July 2024) and `QP2408` (August 2024) — **nothing else** |
| **Both papers** | `Intake Complete`, **0/9 built**, no branch on `origin` |

**These two are the last papers of the 2024–2026 corpus.** When they are live, every sitting MIW
holds from 2024 to 2026 is solved. The 2023 intake is a separate, later batch — see
`DESKTOP_QP_ALLOCATION_2023.md`. **Do not start 2023 work inside this batch.**

### Verify the baseline before you start

```bash
git fetch origin --prune
git rev-parse origin/main          # must print e5843b1... or later
git ls-remote origin 'refs/heads/pastpapers/qp240[78]*'   # must print NOTHING before you begin
```

---

## 2. RECOMMENDED ORDER — QP2407 FIRST, THEN QP2408

This is **not** a coin toss and it is not chronology. It is donor readiness, recomputed against
the current 234-question corpus on 2026-08-13. The figures in `DESKTOP_QP_ALLOCATION_2024.md`
(QP2407 "zero verified donors", QP2408 "one donor") are **stale** — six papers have been published
since, and both improved.

| | QP2407 (July 2024) | QP2408 (August 2024) |
|---|---|---|
| Exact / near donors | **3** | 2 |
| Family / strong | **2** | 1 |
| **Questions with a donor** | **5 / 9** | **3 / 9** |
| **No donor — fresh research** | **4** | **6** |
| Research burden | Moderate | **Heaviest remaining paper in the corpus** |

**QP2407 is the more finishable paper and it goes first.** QP2408 carries six questions with no
donor at all, which is the largest fresh-research load of any paper left.

### Does either unlock the other? — No, and this was checked

Cross-matching the two papers' stems against each other produces **no relation above the family
threshold**. Their topics do not overlap: QP2407 runs gender, ME engine, IMO structure, GHG
strategy, ship identification, MLC, propeller curves, Jason clause, NOx; QP2408 runs RO Code, SUA,
casualty investigation, market-based measures, ship dimensions, ISO 8217, salvage, turbochargers,
SMS. **Order them for research burden, not for dependency** — and the order still matters, because
finishing the easier paper first banks a live paper sooner.

---

## 3. QP2407 (July 2024) — question-by-question

| Q | Topic | Donor | Sitting | Class |
|---|---|---|---|---|
| Q1 | Gender equality in shipping | `QP2503-Q3` | March 2025 | FAMILY |
| Q2 | ME engine vs conventional MC engine | — | — | **NONE — fresh** |
| Q3 | IMO structure and instrument hierarchy | `QP2402-Q1` | February 2024 | **EXACT** |
| Q4 | IMO Revised GHG Strategy | `QP2409-Q3` | September 2024 | **EXACT/NEAR** |
| Q5 | Ship identification number, CSR, ESP | — | — | **NONE — fresh** |
| Q6 | MLC — flag State and port State obligations | `QP2406-Q6` | June 2024 | FAMILY |
| Q7 | Propeller curves, margins, layout diagram | `QP2410-Q3` | October 2024 | **EXACT/NEAR** |
| Q8 | New Jason clause, 3/4ths collision clause | — | — | **NONE — fresh** |
| Q9 | NOx — Tier II/III, emulsion, SCR, Technical File | — | — | **NONE — fresh** |

**Q3's donor is the only one that pre-dates the sitting.** `QP2402-Q1` is February 2024, five
months earlier, and is therefore the one donor on this paper that cannot drag later law backwards.
Every other donor is later. See §5.

**Q6 became reachable because QP2406 was published.** `QP2406-Q6` is June 2024 — one month before
this sitting — so it is a **safe, earlier donor**. It is also the MLC question, which means the
December-2024 boundary in §5 has already been worked out once and can be reused with its reasoning
intact rather than re-derived from nothing.

---

## 4. QP2408 (August 2024) — question-by-question

| Q | Topic | Donor | Sitting | Class |
|---|---|---|---|---|
| Q1 | RO Code — approval and oversight | — | — | **NONE — fresh** |
| Q2 | SUA Convention | — | — | **NONE — fresh** |
| Q3 | Casualty investigation, very serious marine casualty | `QP2506-Q7` | June 2025 | **EXACT** |
| Q4 | Market-based measures at MEPC 81 | — | — | **NONE — fresh** |
| Q5 | Ship dimension optimisation for energy efficiency | `QP2402-Q3` | February 2024 | STRONG |
| Q6 | ISO 8217 marine fuel standards, bunker delivery note | — | — | **NONE — fresh** |
| Q7 | Salvage Convention — award criteria, duties, LOF 2000 | — | — | **NONE by the tool** |
| Q8 | Marine turbocharger developments | — | — | **NONE — fresh** |
| Q9 | SMS and the evolution of the ISM Code | `QP2606-Q5` | June 2026 | **EXACT** |

### Q7 is NOT as bare as the table says — check it by hand

The matcher scores `QP2408-Q7` against the corpus at 0.10 and reports no donor. **That is a
wording artefact, not the truth.** `QP2406-Q8` (June 2024) is a solved salvage and general-average
question covering Articles 8, 12, 13 and 14, no-cure-no-pay, SCOPIC and LOF, and `QP2509-Q3` and
`QP2604-Q3` are in the same family. They score low only because QP2408 phrases its stem around
"award criteria, duties and LOF 2000" while QP2406 phrases its around "principles of modern
salvage law". **Read `QP2406-Q8` before authoring `QP2408-Q7`.** It is a two-month-earlier sitting
and therefore a safe donor.

This is the general warning: **a low similarity score is evidence about wording, not about
subject matter.** Adjudicate the family by reading, not by threshold.

### Q9's donor is two years later — the single most dangerous relation in this batch

`QP2606-Q5` is **June 2026**, twenty-two months after this sitting, and it is an ISM-evolution
question. Anything it says about cyber risk management, the 34th Assembly, or post-2024 amendment
activity is **future law for QP2408** and must not transfer. Treat it as a route, not as prose.

---

## 5. TEMPORAL ANCHOR — JULY AND AUGUST 2024

Build the anchor **before** the answers. Both sittings sit in the same narrow window, so most
boundaries are shared.

### Operative at both sittings

- **Merchant Shipping Act, 1958.** The 2025 Act commenced **15 March 2026** — twenty months later.
- **33rd IMO Assembly**, adopted **6 December 2023**: the `A.11xx(33)` editions are operative.
  `A.1185(33)` is the PSC basis. The 34th Assembly (**adopted 3 December 2025**) is future.
- **ISM Code** as amended through `MSC.353(92)`, in force 1 January 2015, unamended.
- **MLC 2006 as amended through the 2018 set.**
- **MEPC 81** (18–22 March 2024) is **past**. **MSC 108** (15–24 May 2024) is past but its
  resolutions were **adopted, not in force** — entry into force 1 January 2026.
- **SOLAS Consolidated Edition 2024**, in effect **1 July 2024** — this one **is** operative for
  both sittings, unlike QP2406 where it fell after the sitting.
- 0.50 % m/m global sulphur limit outside ECAs, in force since 1 January 2020.
- EEXI / CII / SEEMP Part III; EU ETS maritime.

### Future at both sittings — PROHIBITED

| Item | Date | After the sitting |
|---|---|---|
| **MEPC 82** | 30 Sep – 4 Oct 2024 | 2–3 months |
| `MEPC.395(82)` 2024 SEEMP guidelines | MEPC 82 | 2–3 months |
| **MLC 2006 2022 amendments** | in force **23 Dec 2024** | 4–5 months |
| **Hong Kong Convention** | in force **26 June 2025** | ~11 months |
| **34th IMO Assembly** `A.12xx(34)` | adopted 3 Dec 2025 | ~16 months |
| IMO Net-Zero Framework / GFI | Oct 2025 | ~14 months |
| **Merchant Shipping Act, 2025** | commenced 15 Mar 2026 | ~20 months |
| MEPC 83 | 2025 | — |

### Two boundaries that bite specific questions

1. **QP2408-Q4 names MEPC 81 in its own stem.** MEPC 81 sat in March 2024 and is past, so the
   question is answerable — but **MEPC 82 is only two to three months away** and everything the
   market-based-measures debate produced at MEPC 82 and after is future. This question is the
   highest contamination risk in the batch because its whole subject is a moving negotiation.
2. **QP2407-Q4 is the Revised GHG Strategy.** The operative instrument is the **2023 Strategy
   adopted at MEPC 80 (July 2023)**. Do not carry the Net-Zero Framework or any 2025 outcome back.

### The inversion trap still applies

The corpus register is maintained for **current** law. For a 2024 sitting it is inverted in at
least two places: `MEPC.346(78)` is marked *superseded* but is **operative** at these sittings, and
the register's newest PSC edition is the 34th Assembly revision when **`A.1185(33)`** is the
operative one. **Check the direction before consuming a "superseded" marking.**

---

## 6. WHAT QP2406 TAUGHT THAT APPLIES HERE

Five defects were found in QP2406 at laptop review. Four are avoidable at authoring:

1. **Do not name the source host anywhere in a committed artefact** — not in the spec, not in the
   HTML, and **not in the verification records**. QP2406 named it nine times in a public repo while
   its own spec declared host identity was kept out. Say "the host".
2. **Do not write a summary count before the detail is final.** QP2406's anchor header claimed
   "8 of 9 donor relations" over a table listing seven. Derive the header from the table last.
3. **Keep production vocabulary out of candidate-facing fields.** "donor", "before publication",
   "reverify", "the production protocol" must not appear in `study_notes`, `model_answer`,
   `understand_first`, `answer_route`, `quick_revision` or `retrieval_cards`. Provenance *claims*
   ("the corpus does not hold X") are a different class — leave those alone, they are Founder-held.
4. **Rule 4 in `understand_first`:** no regulation, resolution, article, section numbers or
   sitting-specific dates. A statute's own name including its year (*Merchant Shipping Act, 1958*)
   is fine. The knowledge map beneath is derived and is **not** governed by Rule 4.
5. **Never state a week-granularity distance from a month-only sitting.** These papers print
   `JULY 2024` and `AUGUST 2024` with no day. "Two weeks after" is unprovable; "the following
   month" is honest.

---

## 7. BRANCH AND ARTEFACT RULES

- Branch per paper from the recorded baseline: `pastpapers/qp2407-founder-review`, then
  `pastpapers/qp2408-founder-review`.
- **One paper at a time.** Finish 9/9 before starting the second.
- A paper branch commits **only its own twelve files**: `QP24xx.html`, `specs/QP24xx.json`,
  `docs/QP24xx_TEMPORAL_AND_DONOR_ANCHOR.md`, `verification/QP24xx/Q1..Q9.md`.
- **Never commit a global derived artefact** from a paper branch — no reuse map, no manifest, no
  index, no year or topic sheet, no `solvedQP/` page. The laptop regenerates all of those.
- **Never commit a source PDF.** `meoclass1/pastpapers/docs/*.pdf` is git-ignored and this
  repository is **public**.
- Push the branch and stop. The laptop reviews, integrates by path extraction onto current `main`,
  and publishes. **Desktop branches are never merged** and are retained as provenance.

---

## 8. STOP GATE

**Stop after QP2408 and report.** Do not begin the 2023 intake without the Founder, even though
the source PDFs are already on disk. When these two are live the 2024–2026 corpus is complete, and
that is a decision point, not a milestone to run through.
