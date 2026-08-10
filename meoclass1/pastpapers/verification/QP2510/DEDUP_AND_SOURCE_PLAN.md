# QP2510 — October 2025 — SOURCE RE-READ, PAIR AUDIT AND ADAPTATION PLAN

**Paper:** QP2510, October 2025, MEO Class I, Engineering Management
**Donor:** QP2403, March 2024 — solved 9/9, verification record for every question
**Branch:** `pastpapers/qp2510-founder-review`, cut from `e7d8bc0`
**State:** **RESEARCH COMPLETE — ANSWERS NOT AUTHORED.** See §8.
**Date:** 2026-08-10

> **This session resolved all three temporal blockers against primary sources and stopped there,
> rather than author nine answers on top of research that had not yet been done. One of the three
> overturned a donor assumption outright. See §5.**

---

## 1. Full source re-read — COMPLETE, ZERO CORRECTIONS

`meoclass1/pastpapers/docs/OCTOBER - 2025.pdf`, 3 pages, born-digital text layer, extracted with
PyMuPDF and compared programmatically against `specs/QP2510.json`.

| Element | Source copy | Spec | Result |
|---|---|---|---|
| Month / year | OCTOBER 2025 | October 2025 | match |
| Serial | `Sr. No. EM – 2510` | `QP-2510` | match (recorded form) |
| Printed authority | EXAMINATION OF MARINE ENGINEER OFFICER | same | match |
| Function | Marine Engineering Management at Management Level | same | match |
| Class / time / marks | M.E.O CLASS – I · 3 HOURS · Total Marks – 100 | same | match |
| Region note | (India 2025) | same | match |
| Instructions | 4 numbered items | 4 items | match |
| Questions | Q1–Q9 | 9 | match |
| Page continuations | Q3 straddles pages 1–2; host panel intervenes | — | handled |

**Every one of the nine `text_verbatim` strings occurs character-for-character in the source PDF**
after whitespace and smart-quote normalisation — tested by substring containment, not by eye.

**Printed marks, read off the source and confirmed against the spec:**

| Q | Printed | Sum |
|---|---|---|
| Q1 | (A) 8 · (B) 8 | 16 |
| Q2 | a) 3 · b) 5 · c) 8 | 16 |
| Q3 | a) 8 · b) 8 | 16 |
| Q4 | none printed | recorded 16 |
| Q5 | **(16) on the stem**, no limb marks | 16 |
| Q6 | none printed | recorded 16 |
| Q7 | **a) 6 · b) 5 · c) 5** | 16 |
| Q8 | none printed | recorded 16 |
| Q9 | a) 8 · b) 8 | 16 |

**No transcription correction was required.** The intake transcription is sound and the canonical
question truth stands unaltered. The source's own typo — *"prone **of** cyber risks"* in Q5 — is
correctly preserved in `text_verbatim` and correctly normalised in the decomposition.

The host's marketing panels and its recurrence table are editorial furniture and remain
untranscribed, per the standing provenance rule.

---

## 2. Direct QP2403 ↔ QP2510 pair audit — CONFIRMS THE CANONICAL DATA

Both stems opened for every pair; ratio computed on normalised strings.

| Q | Ratio | Class | Question delta | Marks delta |
|---|---|---|---|---|
| Q1 | **1.0000** | EXACT | none | none |
| Q2 | **1.0000** | EXACT | none | none |
| Q3 | **1.0000** | EXACT | none | none |
| Q4 | **1.0000** | EXACT | none | none |
| Q5 | 0.9947 | **NEAR** | **none** — sole delta is the printed `(16)` token | none |
| Q6 | **1.0000** | EXACT | none | none |
| Q7 | 0.9926 | **NEAR** | **none** — wording identical | **6+4+6 → 6+5+5** |
| Q8 | **1.0000** | EXACT | none | none |
| Q9 | **1.0000** | EXACT | none | none |

**Seven EXACT, two NEAR, and neither NEAR carries an examiner-demand change.** This is the
QP2604-Q4 sub-class — *NEAR by punctuation or marks alone* — and it is not licence to re-author.

- **Q5's only difference is that October prints a mark total March did not.** The demand is
  identical. Treat as EXACT for reuse purposes.
- **Q7's wording is character-identical**; only the limb weighting moved. See §6.

> The examiner reissued March 2024 essentially unchanged nineteen months later. **That makes the
> question layer safe to reuse and the answer layer dangerous to reuse** — which is the whole point
> of this paper.

---

## 3. The "Q1 cyber → Rev.3" statement — **NEITHER A TYPO NOR A DEFECT**

The previous session's report said *"One update: Q1 (cyber → Rev.3)"*, while the paper overview
identifies **Q5** as the cyber question. This was flagged for adjudication. It was tested rather
than assumed.

**QP2403-Q1 (big data) genuinely carries the cyber circular in its own answer** — 10 occurrences of
`MSC-FAL.1/Circ.3` and 10 of `Rev.2`, across **eight distinct surfaces**:

`sources[5]` · `model_answer.blocks[20]` · `study_notes.blocks[10]` · `study_notes.blocks[15]` ·
`regulations[3]` · `answer_route.steps[6].points[1]` · `quick_revision.critical_numbers[4]` ·
`retrieval_cards[6].answer`

The donor's own `temporal_review.notes[4]` states the position exactly:

> *"For QP2510 the Single Window obligation is equally in force and the answer needs no change; the
> cyber cross-reference must move to Rev.3."*

**Verdict: REPORT CORRECT · CANONICAL METADATA CORRECT.** Q1 cross-references the circular; Q5 *is*
the circular question. Both §26.7 rows are right, and **Q1 does need the Rev.2 → Rev.3 update** on
all eight surfaces. Nothing is to be changed on the strength of a misreading — but nothing is to be
skipped either.

---

## 4. Temporal review — all nine, at the October 2025 sitting date

Stored flags were treated as prompts, never as evidence. The intake flag was **0 for 9** on the
donor paper; it is not trusted here.

| Q | State | Risk | Sitting-date finding |
|---|---|---|---|
| Q1 | **REVIEW** | MEDIUM | MSW obligation (FAL.14(46), Standard 1.3quin) in force 1 Jan 2024 — **operative at both sittings, answer substance unchanged**. The embedded **cyber cross-reference must move to Rev.3** (§3). |
| Q2 | **CORRECTED** | **HIGH** | **Both Indian statutes replaced and in force 10 Sep 2025** — five weeks before the sitting. Regime materially changed. **§5.** |
| Q3 | STABLE | LOW | General average rests on York-Antwerp Rules and Marine Insurance Act 1963. No edition change between the sittings; MIA 1963 unamended. **Re-verify at authoring.** |
| Q4 | STABLE | LOW | Engineering explanation. No instrument prescribes a propeller type; donor correctly carries `regulations: []`. Nothing in propeller practice changed the printed demand. |
| Q5 | **CORRECTED** | **HIGH** | **Rev.2 → Rev.3 (4 Apr 2025); five elements → six; eight systems → nine; annex renumbered.** **§5.** |
| Q6 | STABLE | LOW | MEPC.312(74) not revised; the enabling MARPOL electronic-record-book amendments unchanged. **Cleanest donor on the paper.** Confirm at authoring that no superseding MEPC resolution intervened. |
| Q7 | **REVIEW** | MEDIUM | A.1070(28) unamended — the III Code at both sittings. **A.1187(33) CONFIRMED still current at the sitting** — see below. Plus the marks re-weight, §6. |
| Q8 | STABLE | LOW | Operational/diagnostic question; no instrument governs it. Donor carries `regulations: []`. |
| Q9 | **CORRECTED** | **HIGH** | **MLC 2022 amendments in force 23 Dec 2024** — ten months before the sitting. **§5.** |

> ### **Q7 — RESOLVED, AND THE TRAP RUNS BACKWARDS**
>
> The June 2026 paper established that **A.1206(34) and A.1207(34), adopted 3 December 2025**,
> revoked the PSC and HSSC procedures resolutions. The suspicion that the Non-exhaustive List moved
> in the same Assembly session was correct — **and it did not help the target, it endangered it.**
>
> **Resolution A.1208(34), adopted 3 December 2025**, is the *2025 Non-exhaustive list of
> obligations under instruments relevant to the III Code*. Read on the IMO CDN, it recalls
> A.1187(33) as the 2023 List and states in terms: **"REVOKES resolution A.1187(33)."**
>
> **3 December 2025 falls AFTER the October 2025 sitting.**
>
> > **Therefore A.1187(33) WAS STILL THE CURRENT LIST at this sitting. The donor's citation is
> > correct for the target and must be RETAINED. Citing A.1208(34) would be future-date
> > contamination.**
>
> This is the **Q1 mirror-image error from §26.3 in a new place**: the danger is not that the answer
> is stale, but that an author working in 2026 finds the successor resolution presented as "current"
> and imports it. The A.1208(34) List expressly gathers requirements entering into force **by 1 July
> 2026** — none of which existed for a candidate sitting in October 2025.

> **FUTURE-DATE CONTROL, Q9.** The **2025 MLC amendments** (ILC 113th Session, June 2025) are
> **adopted but NOT in force** — expected December 2027. The corpus holds them segregated under
> `not-yet-in-force/`. **They must not appear in an October 2025 model answer.** This is a live
> contamination risk precisely because they were adopted four months *before* the sitting.

---

## 5. The three temporal findings — ALL RESOLVED AGAINST PRIMARY SOURCES

### 5.1 Q2 — the carriage-law blocker: **RESOLVED, AND THE ANSWER IS NO**

The open research item was *"whether COGSA 2025 carries the Hague-Visby position unchanged"*.

**It does not.** Both Acts were read in full in the **official Gazette of India (Extraordinary,
Part II — Section 1)**. Detail in `Q2.md`. Headline:

| | |
|---|---|
| Operative at the sitting | **Bills of Lading Act 2025** (18 of 2025) · **Carriage of Goods by Sea Act 2025** (19 of 2025) |
| Both in force | **10 September 2025** — S.O. 4083(E) and S.O. 4082(E) of 8 Sep 2025 |
| Repealed | Indian Bills of Lading Act **1856** (BoLA 2025 s.6(1)); Indian Carriage of Goods by Sea Act **1925** (COGSA 2025 s.12(1)) |

**Four substantive changes, not a citation refresh:**

1. **"Goods" now INCLUDES live animals and deck cargo.** Schedule Art **I(d)**. The Hague-Visby
   Art I(c) exclusion is **reversed**. The donor asserts the exclusion as a P1 primary claim; that
   claim is **true for March 2024 and false for October 2025**.
2. **Article IV bis is not reproduced.** The Schedule runs Articles **I–IX** with **zero**
   occurrences of "bis". The Visby tort-channelling / servants-and-agents article is absent.
3. **A three-month judicial extension of the one-year time bar** — Art III(6)(c) proviso. Hague-Visby
   permits extension only by agreement.
4. **Article I and Article IV(5) are re-lettered throughout.** Every Article I citation in the donor
   answer is wrong for this sitting.

**The Bills of Lading Act 2025 is the opposite case — it re-enacts.** ss.2, 3 and 4 carry the same
three subjects as the 1856 Act's ss.1, 2 and 3. There, the donor needs only a citation update.

### 5.2 Q5 — cyber Rev.3: **RESOLVED, BOTH EDITIONS READ**

`MSC-FAL.1/Circ.3/Rev.3`, **4 April 2025**, obtained from the IMO CDN and read in full; **Rev.2 of
7 June 2022 also re-read** so the delta is measured rather than inferred. Detail in `Q5.md`.

| | Rev.2 — March 2024 | Rev.3 — October 2025 |
|---|---|---|
| Functional elements | **five**, annex 3.5 | **six**, annex 3.5 — **Govern** added, and placed **first** |
| Vulnerable systems | **eight**, annex **2.1.1** | **nine**, annex **2.2.1** |
| IT / OT | annex 2.1.2, descriptive | annex **2.1**, formally **defined** with examples; segregation duty at 2.2.2 |
| New defined terms | — | **Computer Based System (CBS)**, cyber incident |

Approved by **MSC 108** (15–24 May 2024) and **FAL 49** (10–14 March 2025). **All four printed limbs
of Q5 are touched by this revision** — (A) the list, (B) the elements, (D) the IT/OT definitions —
which is why Q5 is the most expensive question on the paper.

### 5.3 Q9 — MLC operative state: **RESOLVED, ALL FOUR ADDITIONS VERIFIED VERBATIM**

The **2022 amendments entered into force 23 December 2024**, corroborated twice: the corpus
instrument log (verified against the ILO 2026 Compendium) and the ILO's own published notice.
The corpus holds the 2022 consolidation. Detail in `Q9.md`. Each addition located in the text:

| Addition | Provision | Verified |
|---|---|---|
| Social connectivity, including internet access | **Standard A3.1 §17** | verbatim |
| Appropriately-sized PPE | **Standard A4.3 §1(b)** | verbatim |
| Engineering/design control has precedence over PPE | **Guideline B4.3.1 §3** | verbatim |
| Deaths investigated, recorded and reported annually to the ILO Director-General for a **global register** | **Standard A4.3 §5(a)** | verbatim |
| Registered owner named on the financial security certificate where different from the shipowner | **Appendix A4-I(g)** | verbatim |

---

## 6. Q7 — same words, different weight

**6 + 4 + 6 → 6 + 5 + 5.** Limb (a) is unchanged. Limb (b) — the key performance indicators — gains
a mark; limb (c) — flag / coastal / port State responsibilities — loses one.

**No engineering or legal truth changes because marks moved.** What changes is emphasis: the donor
built limb (c) as the joint-heaviest limb and limb (b) as the lightest. At October 2025 they are
equal. The KPI limb should carry proportionally more of the answer than it does in the donor, and
limb (c) proportionally less, **without removing any scoring proposition from either**.

---

## 7. Adaptation plan — per question

Classes: **A** reuse as is after re-verification · **B** minor update · **C** substantive update.

| Q | Donor | Class | What must happen |
|---|---|---|---|
| Q1 | QP2403-Q1 | **B** | Substance stands. Move the cyber cross-reference Rev.2 → Rev.3 on **all eight surfaces** (§3). Do **not** turn it into an AI/2026 answer. |
| Q2 | QP2403-Q2 | **C** | Re-cite to the 2025 Acts; **reverse the deck-cargo/live-animals proposition**; drop or re-frame the Article IV bis material; add the three-month extension; re-letter every Article I citation. |
| Q3 | QP2403-Q3 | **A** | Re-verify YAR edition status and MIA 1963 at the sitting; reuse route and propositions. |
| Q4 | QP2403-Q4 | **A** | Reuse verified engineering base. Add no newer technology merely because it exists. |
| Q5 | QP2403-Q5 | **C** | Six elements with **Govern**; nine systems; annex renumbering; formal IT/OT definitions. **Route is preserved** — see §9. |
| Q6 | QP2403-Q6 | **A** | Cleanest donor. Confirm no superseding MEPC resolution, then reuse. |
| Q7 | QP2403-Q7 | **B** | **Retain A.1187(33) — confirmed current at the sitting.** Re-weight limbs (b) and (c) per §6. Do **not** cite A.1208(34). |
| Q8 | QP2403-Q8 | **A** | Reuse the diagnostic and reporting sequence unchanged. |
| Q9 | QP2403-Q9 | **C** | Integrate the four 2022 additions **into the relevant limb-(a) sections** — not as an appended "2022 amendments" paragraph. Quarantine the 2025 set. |

**Four A · two B · three C** — which matches the shape the handover predicted, now on evidence
rather than expectation.

### Mandatory for every question, including class A

1. **Re-key** `question_id`, `verification_file`, retrieval-card ids, and in-paper `cross_links`
   (`QP2403.html#qN` → `QP2510.html#qN`).
2. **Re-anchor sitting-relative prose.** March's rule, 2/2 on later papers: search the **assembled**
   spec for `this paper`, `this sitting`, `this examination`, `weeks/months before`, any named
   month-year, and any cross-reference to another question **by number**.
3. **Assembled-answer temporal sweep**, then a **future-date sweep** for post-October-2025 facts.
4. Expect **false positives** and adjudicate every hit by hand — April found 55 hits and exactly
   one defect.

---

## 8. What this session did NOT do, and why

**No answer was authored. No `answer_status` was changed. QP2510 is NOT built and NOT solved.**

The three temporal questions had to be researched before any of the nine could be written, because
Q2's result changes what limb (c) may assert, Q5's changes three of four limbs, and Q9's changes
half of limb (a). That research is now complete and primary-sourced. Authoring nine answers on top
of it — nine ~45 KB objects, nine verification records, build, sweeps and regression — was not
achievable in the remainder of this session at the standard the brief sets.

This follows the **§25 precedent**, where QP2403 was deliberately stopped at 2 of 9 rather than
lower verification quality. §26 records that the checkpoint held and its groundwork was *used, not
redone*. The same is intended here.

> **The expensive, hard-to-redo work is the part that is finished.** A future session inherits three
> resolved legal/regulatory positions, a verified source re-read, a confirmed pair audit and a
> per-question adaptation class.

---

## 9. Study intelligence — stable route, changing law

The QP2403 → QP2510 pair is the cleanest demonstration in the corpus of a principle worth teaching
directly:

> **THE ROUTE MAY REMAIN STABLE WHILE THE REGULATORY CONTENT CHANGES.**

**Q5 is the exemplar.** The examiner's four limbs are identical, so the seven-step route that serves
March serves October unchanged. What changes is the *content of two branches*: the element list
grows by one and gains a new first member, and the system list grows by one. A candidate who learned
the route in 2024 still knows where to start, what order to write and where to stop; they need to
update two facts, not relearn a question.

**Q2 is the counter-example.** Same question, same route, but the governing statute was replaced and
one proposition inverted. Route stability does **not** imply answer stability.

**Q9 sits between them** — the architecture of limb (a) survives; four requirements must be threaded
into it.

This is the raw material for *"How this topic has been asked"*, *"Stable route / changing law"* and
the question-family study guides. **Not built now** — recorded for the derivation session.
