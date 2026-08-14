# SIX-YEAR QP INTELLIGENCE — 2021 to 2026

**INTERNAL. Not a candidate-facing surface, and not exposed in any rendered page.**
Built 2026-08-14, after QP2304 was published. Question wording and lineage only — no answer
content was read or produced for any unsolved sitting.

Derived from two **committed** inputs:

- `meoclass1/pastpapers/specs/QP####.json` — the **solved** papers
- `meoclass1/pastpapers/intelligence/historical_qp_intelligence.json` — the question-only shelf
  record of every held 2021–2023 sitting

Both are fed through the **governed** `tools/pastpapers/recurrence_model.py`
(`normalise_stem` / `build_families`) rather than a second equality rule, so a "family" here means
exactly what a family means on a paid page.

### Regeneration

```
python tools/pastpapers/build_sixyear_intelligence.py    # from the two committed inputs
python tools/pastpapers/extract_historical_questions.py   # refresh the shelf record from local PDFs
```

The layer is derived and **gitignored**; the two inputs above are the truth. A clean checkout
rebuilds it with no source PDF and no local state, and a double build is byte-identical.

The shelf record deliberately keeps **every** held sitting, including any that has since been
solved. **Graduation is applied by the builder**: a paper that gains a canonical solved spec is
excluded from the intelligence-only set by rule, so the same sitting is never counted twice and no
one has to remember to delete it. `tools/pastpapers/sixyear_intelligence_test.py` holds that
property, and its `--self-test` shows the totals double-counting once the rule is removed.

**The per-year table below is a snapshot taken when QP2304 was the newest paper.** The solved and
intelligence-only columns move every time a paper graduates; the **61 papers / 549 questions**
total does not, because graduation moves a sitting between columns rather than into or out of the
window. Run the builder for current figures rather than reading them from here.

---

## 1. THE WINDOW

| Year | Papers | Questions | Solved | Intelligence-only |
|---|---|---|---|---|
| 2021 | 11 | 99 | 0 | 11 |
| 2022 | 11 | 99 | 0 | 11 |
| 2023 | 11 | 99 | 3 | 8 |
| 2024 | 11 | 99 | 11 | 0 |
| 2025 | 11 | 99 | 11 | 0 |
| 2026 | 6 | 54 | 6 | 0 |
| **Total** | **61** | **549** | **31** | **30** |

2026 is partial by calendar, not by gap — it runs to the newest sitting MIW holds.

---

## 2. INVENTORY, AND THE DISTINCTION THAT MATTERS

The Founder's instruction was to separate **NO SITTING** from **NO PAPER IN MIW'S SOURCE SET**.
Those are different claims and only one of them is evidenced here.

### 2.1 What the evidence actually is

The printed serial is `YYMM EM` — `2101` is January 2021 exactly as `2304` is April 2023. The
serial is therefore **month-aligned and sequential within the year**, so a missing serial is a
month for which no paper was numbered.

| Year | Serials held | Missing | Sequence evidence |
|---|---|---|---|
| 2021 | 2101–2104, 2107–2112 | **2105, 2106** | runs 2104 → 2107 |
| 2022 | 2201–2204, 2206–2212 | **2205** | runs 2204 → 2206 |
| 2023 | 2301–2304, 2306–2312 | **2305** | runs 2304 → 2306 |
| 2024 | — | 2405 | recorded previously |
| 2025 | — | 2505 | recorded previously |
| 2026 | — | 2605 | recorded previously |

### 2.2 May — six consecutive years

**May is absent in 2021, 2022, 2023, 2024, 2025 and 2026**, with a serial gap in every year.
Six consecutive years of the same gap, evidenced the same way each time, is strong.

**It is still not official confirmation.** A DGMA / DG Shipping examination calendar stating that
no May sitting is held **was searched for and could not be located**. So the honest encoding is:

> `NO_SITTING_INFERRED` — no paper numbered in six consecutive years; serial sequence skips it
> every time; **no official calendar located**.

That is deliberately not the same token as a confirmed `NO SITTING`. If the Founder obtains a
DGMA calendar, it upgrades in one edit.

### 2.3 June 2021 — a different thing entirely, and the July paper explains it

June 2021 is the **only** non-May gap in 2021–2025. Three facts sit together:

1. **2020 held six papers, not eleven** — January, February, March, October, November, December.
   April to September 2020 are absent. That is the COVID-19 signature and nobody would read it as
   a standing calendar feature.
2. **June 2021 is absent** — India's second COVID wave peaked April–June 2021.
3. **July 2021 has TWO papers.** `QP2107` prints serial `2107 EM`. The second, `QP2107-S2`,
   **prints no serial at all** — the only paper in either year that does not.

The reading that fits all three: **the June 2021 sitting was deferred and held as a second July
sitting**, which is why the extra paper carries no month-serial of its own. That is an inference,
labelled as one, not a recorded fact — but it is a much better explanation than "June is
sometimes missing", and it means June 2021 must **not** be encoded in the same class as May.

### 2.4 Encoded states

| State | Meaning | Count |
|---|---|---|
| `SOLVED` | full MIW answer product exists | 31 sittings |
| `INTELLIGENCE_ONLY` | question wording held, no answers | 30 sittings |
| `NO_SITTING_INFERRED` | no paper numbered; serial gap | May ×6, June 2021 |
| `SOURCE_NOT_HELD` | month not yet sat or not published | Aug–Dec 2026 |

---

## 3. RECURRENCE ACROSS THE WINDOW

| Class | Families | Questions | Share of 549 |
|---|---|---|---|
| **EXACT_REPEAT** | 76 | 184 | **33.5 %** |
| **NEAR_REPEAT** | 29 | 107 | **19.5 %** |
| **UNIQUE** | 258 | 258 | **47.0 %** |
| Total | 363 | 549 | 100 % |

**105 families repeat; 291 of 549 questions (53 %) belong to one.**

"Exact" means the normalised printed stem is identical — the same scoring demand — not keyword
overlap. Printed marks are excluded from the comparison because the same examiner task is printed
with different marks tokens at different sittings.

### 3.1 Most repeated exact families

| Times | Years | Span | Question |
|---|---|---|---|
| 5 | 3 | Feb 2023 → Oct 2025 | III Code — objectives, and the flag/port/coastal State duties |
| 5 | 3 | Apr 2023 → Dec 2025 | Maritime lien, in rem / in personam, order of settlement |
| 5 | 2 | Jun 2025 → Mar 2026 | Entry into force of an IMO convention after adoption |
| 4 | 2 | Jul 2021 → Jun 2022 | Lay-up of a vessel for 3 months |
| 4 | 2 | Jul 2021 → Mar 2022 | Influence of a charter on propulsion and machinery operation |
| 4 | 3 | Apr 2022 → Jun 2026 | Formal Safety Assessment in IMO rule-making |
| 4 | 3 | Sep 2022 → Oct 2025 | Maritime cyber risk management, MSC-FAL.1/Circ.3 |

### 3.2 Longest-running families

| Years | Times | Span | Question |
|---|---|---|---|
| **5** | 6 | Oct 2022 → Jun 2026 | Classification societies in rule formation; SOLAS II-1; annual vs periodical surveys |
| 4 | 8 | Jan 2023 → Apr 2026 | Human element in STCW; IMO fatigue guidance |
| 4 | 6 | Jan 2022 → Jun 2025 | Rudder efficiency improvement devices |
| 4 | 6 | Jan 2023 → Feb 2026 | General average — essential features |
| 4 | 6 | Apr 2023 → Jul 2026 | Particular and general average; average adjusters |

### 3.3 Dormant-return

**15 families** went ≥ 24 months without being set and then returned. Longest: Fault Tree Analysis,
**33 months** (April 2021 → January 2024). Others at 30–31 months include perils of the sea,
Formal Safety Assessment, *uberrimae fidei*, and the IACS structure question.

---

## 4. FIRST-SEEN — WHAT THE TWO NEW YEARS ACTUALLY CHANGED

**16 families now root before 2023**, i.e. a question MIW has solved and treated as originating in
2023–2026 in fact first appeared in 2021 or 2022.

Three of them are on the paper published earlier today:

| Solved question | MIW's assumed origin | **True first sitting** |
|---|---|---|
| `QP2304-Q1`, `QP2509-Q1` — bauxite casualties | April 2023 | **September 2022** |
| `QP2304-Q2`, `QP2503-Q6`, `QP2509-Q5` — HNS Convention | April 2023 | **September 2022** |
| `QP2304-Q9`, `QP2312-Q8`, `QP2412-Q4` — classification societies | October 2022 confirmed | **October 2022** |

Others include Fault Tree Analysis (April 2021), rudder efficiency (January 2022), hull and
propeller maintenance (February 2022), propeller curves (March 2022), *uberrimae fidei* and EEDI
(October 2022), and ammonia as a marine fuel (December 2022).

### 4.1 The host's printed annotations were right, and MIW can now say so on its own evidence

The April 2023 source copy printed `2022/SEP/Q2` against Q1, `2022/SEP/Q8` against Q2 and
`2022/OCT/Q5` against Q9. Standing policy classes those annotations as **discovery only**, because
the 2026 set proved they over- and under-claim in both directions — and that policy stands.

But on these three, MIW has now **transcribed the 2022 papers itself** and confirms them. The value
is not that the host was right; it is that the claim no longer rests on the host.

### 4.2 No live page is wrong because of this

The candidate-facing labels are scoped — *"Set once in the sittings MIW has transcribed"*,
*"2 sittings in this set"*. They are claims about the transcribed corpus, not about examination
history, so nothing shipped is false. Widening the corpus would make them **more informative**, not
correct an error. That remains a Founder decision.

---

## 5. TEMPORAL REPEAT — SAME QUESTION, DIFFERENT REQUIRED ANSWER

This is the highest-value class in the whole map: a stem that is stable while the law under it
moved, so an answer copied forward or backward across the boundary is **wrong for one of the two
sittings**.

**17 of the 105 repeating families cross at least one dated legal boundary.**

| Times | Span | Boundary crossed | Question |
|---|---|---|---|
| 8 | Jan 2023 → Apr 2026 | **MLC 2022 amendments in force 23 Dec 2024** | Human element in STCW; fatigue guidance |
| 5 | Feb 2023 → Oct 2025 | **33rd Assembly, 6 Dec 2023** | III Code objectives and duties |
| 4 | Dec 2022 → Nov 2024 | **EEXI/CII apply 1 Jan 2023** | Hull-form optimisation for energy efficiency |
| 3 | Feb 2022 → Mar 2025 | **EEXI/CII apply 1 Jan 2023** | Hull and propeller maintenance |
| 3 | Sep 2022 → Sep 2025 | **IMSBC 06-21 in force 1 Dec 2023** | Bauxite casualties |
| 3 | Dec 2022 → Nov 2024 | **2023 GHG Strategy, 7 Jul 2023** | Ammonia as a marine fuel |
| 3 | Apr 2023 → Sep 2025 | **MLC 2022 amendments** | IMO/ILO human-element regimes |
| 3 | Oct 2024 → Mar 2026 | **Hong Kong Convention in force 26 Jun 2025** | Ship recycling |
| 2 | Oct 2022 → Mar 2025 | **2023 GHG Strategy** | EEDI under MARPOL Annex VI ch. 4 |
| 2 | Jan 2026 → Apr 2026 | **MS Act 2025 commences 15 Mar 2026** | VLCC casualty, tank explosion |

Two operational consequences:

- **Any future donor reuse inside these 17 families must re-derive the affected limb**, not carry
  it. The bauxite family is the worked example: the answer is materially the same either side,
  but the *statement of which amendment is mandatory* is not.
- The **MS Act 2025 family straddles 15 March 2026 inside a single year** — January 2026 is under
  the 1958 Act and April 2026 is under the 2025 Act. That is the narrowest boundary in the window.

---

## 6. NOVELTY BY YEAR — AND THE ARTEFACT IN IT

Share of each year's 99 questions that are the **first** appearance of their family:

| Year | First appearances | Rate |
|---|---|---|
| 2021 | 89 / 99 | 90 % |
| 2022 | 75 / 99 | 76 % |
| 2023 | 82 / 99 | 83 % |
| 2024 | 61 / 99 | 62 % |
| 2025 | 42 / 99 | 42 % |
| 2026 | 14 / 54 | 26 % |

**Read the top of this table with care.** 2021 scores 90 % largely because **the window starts
there and there is nothing earlier for it to repeat from** — left-censoring, not examiner
innovation. Extending the window to 2019–2020 (both available from the same host) would pull 2021
and 2022 down.

The part that is **not** an artefact is the 2024 → 2026 decline, measured against three or more
prior years: **by 2026 roughly three questions in four are a return of something already set in the
window.** That is a genuine, measured property of the recent examination.

---

## 7. HOW TO SPEAK ABOUT THIS

Permitted, because each is a count over a defined window:

- "repeated in X sittings across Y years"
- "persistent family"
- "returned after a Z-month gap"
- "first set in <sitting> within the 2021–2026 window"

Not permitted, and not supported by anything above: any probability, any "likely to appear", any
"guaranteed", any forecast for a future sitting. The map is a record of what was set. It is not a
prediction, and it must never be dressed as one.

---

## 8. LIMITS

1. **Source copies are third-party scans.** `official_source_verified` is `false` for all 30
   intelligence-only papers, exactly as for the solved set.
2. **May's NO SITTING is inferred, not officially confirmed** (§2.2).
3. **June 2021's deferral into July is an inference** (§2.3).
4. **NEAR_REPEAT is a family judgement, not a similarity score.** The governed model deliberately
   refuses similarity ranking, which has picked the wrong neighbour twice in this corpus.
5. **The window is left-censored at 2021** (§6). 2019 and 2020 are available from the same host
   and would extend it; 2020 is COVID-disrupted and holds only six papers.
6. **No answer content was read, inferred or written for any unsolved sitting.**
