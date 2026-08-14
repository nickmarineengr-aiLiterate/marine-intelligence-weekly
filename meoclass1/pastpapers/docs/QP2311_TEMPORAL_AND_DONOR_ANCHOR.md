# QP2311 — NOVEMBER 2023 — TEMPORAL AND DONOR ANCHOR

**Paper:** QP2311 · November 2023 · printed serial `2311 EM` · `(India 2023)`
**Branch:** `pastpapers/qp2311-founder-review`
**Baseline:** `604ca40512b93143b05ea0fd07823228b4dc66c8` (`origin/main` at session start)
**Corpus consumed:** `RulesApp-Local-Input` `319524c24d11b2f89f33672c384b56e9ae1ab7db`, READ ONLY
**Authority for method:** `DESKTOP_QP_PRODUCTION_PLAYBOOK.md`, `DESKTOP_QP_ALLOCATION_2023.md` §3

> **This is the eleventh and final 2023 paper.** With it the 2023 year closes at eleven of eleven
> available sittings and the Written corpus reaches **39 papers · 351 questions**.

---

## 1. SOURCE RECONCILIATION

Read directly from `meoclass1/pastpapers/docs/NOVEMBER 2023.pdf` (git-ignored, local only), both
pages, text layer extracted and read in full. **The printed paper is the authority.**

| Checked | Found |
|---|---|
| Printed serial | **`2311 EM`** — number first, no `Sr. No.` prefix, no dash. The 2023 convention (allocation §1.1) |
| Month / year printed | `NOVEMBER 2023` — **month only, no day** |
| Region note | `(India 2023)` |
| Function | `Marine Engineering Management at Management Level` |
| Subject | `ENGINEERING MANAGEMENT` |
| Class | `M.E.O CLASS – I` — en-dash, and **no** trailing stop after `M.E.O` |
| Time / marks | `TIME ALLOWED - 3 HOURS`; `Total Marks – 100` |
| Pages | **2** — Q1–Q3 on page 1, Q4–Q9 on page 2 |
| Questions | **9**, `Q1`–`Q9`, every one carrying the `Q` prefix |
| Page-break join | **None.** No question is split across the page break. Q3 closes page 1 complete, with its host annotation block and the app advertisement below it; Q4 opens page 2 |

### 1.1 THE KNOWN EXTRACTOR UNDER-READ — resolved, and how

> The Founder's standing warning on this paper was that **an old automated extraction saw only
> about five questions**, and that no automated count was to be trusted.

**That warning was honoured and the paper was established by reading.** Both printed pages were
read in full and all nine questions, all limb letters and all mark splits were written down from
the print **before** any repository artefact was consulted.

The reading was then reconciled against the repository's own maintained intake record, and the two
agree completely — nine questions, identical stems, identical limbs, identical marks. The
historical under-read is therefore **not live**: it was a defect in the extractor, and it was fixed
on `main` in commit `afa1042`, *"Solve March 2023, and fix the extractor that was hiding its own
ancestry"*. The reading is what this spec records; the agreement is corroboration, not authority.

**Why this paper was vulnerable.** November prints its host recurrence annotations as bare tokens
on their own lines directly beneath each question (`2013/SR02`, `2010/JAN`, `2022/SEP/Q5`), and
prints an app advertisement inside the page-1 question flow. A pattern-based extractor that
anchored on the question-number token and stopped at the first block of non-question lines would
terminate early. Nothing about the printed *paper* is defective.

### 1.2 Printed marks — recorded exactly as printed

**November 2023 is the most completely marked of the eleven 2023 sittings.** Every question prints
a mark figure, and every limb of every limbed question prints its own. There is no omission
anywhere, so `printed_marks_absent` is `false` throughout and no question needs a marks inference.

| Question | Printed split | Sums to |
|---|---|---|
| Q1 | `(8)` `(8)` | 16 |
| Q2 | `(5)` `(5)` `(6)` | 16 |
| Q3 | `(4)` `(4)` `(4)` `(4)` | 16 |
| Q4 | `(6)` `(6)` `(4)` | 16 |
| Q5 | `(6)` `(6)` `(4)` | 16 |
| Q6 | `(4)` `(4)` `(4)` `(4)` | 16 |
| Q7 | `(16)` unlimbed | 16 |
| Q8 | `(16)` unlimbed | 16 |
| Q9 | `(5)` `(5)` `(6)` | 16 |

Six answered questions therefore total **96 against the printed `Total Marks – 100`**. **The
discrepancy is printed on the source and is not corrected.**

### 1.3 Printed anomalies — preserved, never normalised

| Where | What is printed | Disposition |
|---|---|---|
| **Numbering** | `Q1.a)` `Q2. a)` **`Q3) a)`** `Q4.a)` `Q5.` `Q6.` `Q7.` `Q8.` **`Q9) a)`** — Q3 and Q9 close the question number with a **round bracket**, the other seven with a **full stop** | Preserved. Both forms are printed on the same paper |
| **Q2 limb b)** | *"Explain how **means** piston speed is related to rpm"* — **"means"** for "mean" | **Preserved.** The correct form appears in the same question's limb a) two lines above, so this is a printing slip and not a term of art |
| **Q2 limb c)** | *"After **Joining** an old ship"* — capitalised mid-sentence | Preserved |
| **Q2 limb c)** | *"vis-à-vis"* — renders as `vis-?-vis` in the raw text layer | An **encoding artefact of the extraction**, not of the print. The spec records the correct character |
| **Q3 limb c)** | *"on-hire **Survey** of a ship"* — capitalised mid-sentence | Preserved |
| **Q3 limb d)** | *"which of the above three **Survey** is the most demanding"* — **singular noun after a plural numeral**, and capitalised | **Preserved.** The intended sense is plainly "surveys"; the answer reads the limb as printed and does not silently repair it |
| **Q6 stem** | *"…and ISM code with the following terms**,**"* — a **comma** where a colon is required to introduce the four lettered terms; and lower-case **"code"** in "ISM code" | Preserved |
| **Q6 limbs a)–c)** | terminated with **semicolons**, limb d) with a full stop | Preserved |
| **Q8** | *"Discuss developments in marine diesel engines … of ships**?**"* — a **question mark closing a sentence that begins with an imperative** | Preserved |
| **Q9 limb b)** | *"the term **"protection"** and **"indemnity"**"* — curly quotation marks, and **singular "term"** governing two quoted words | Preserved |
| **Q9 limb c)** | *"to get **averages** under P&I club"* — "averages" used loosely, and **no article** before "P&I club" | **Preserved, and adjudicated in the answer.** See §5, Q9 |
| Header | `M.E.O CLASS – I`, `Total Marks – 100` — en-dashes; `M.E.O` without a trailing stop | Preserved |

### 1.4 Host and editorial furniture — excluded from every committed artefact

The source copy is a **third-party scan** carrying host branding, page numbers, a repeated footer,
an in-flow app advertisement on page 1 and a trailing purchase solicitation after Q9. **None of it
is transcribed.**

The host also prints its own recurrence annotations beneath each question. On this paper they take
**three different shapes on one page** — `2023/NOV/Q4` (sitting/month/question), `2022/SEP/Q5`
(a cross-year pointer), and bare tokens such as `2013/SR02`, `2011/SR10`, `2010/JAN`, `2016/JUN`
that carry no question number at all and, in the `SR` cases, no recognisable sitting identifier.
They are recorded in `host_recurrence_hint` as **discovery-only provenance**: they create no family
edge, they are not MIW truth, and they reach no candidate-facing surface. The internal
inconsistency of the annotation on this single paper is one more reason it is not treated as data.

Host identity is recorded only in the git-ignored `verification/LOCAL_SOURCE_PROVENANCE.md`.
**This repository is public.**

---

## 2. NOVEMBER 2023 TEMPORAL STATE

> **November 2023 is the cleanest window in the whole 2023 year.** It sits **four months after** the
> MEPC 80 boundary of 7 July 2023 and **one month before** the 33rd Assembly boundary of
> 6 December 2023. Neither boundary falls inside the sitting month, so **no day-level reasoning is
> needed anywhere in this paper and none is used.**

That is the opposite of July 2023, which straddles the GHG boundary with no printed day, and of
December 2023, where the Assembly adoption date falls inside the sitting month.

### 2.1 Operative at this sitting

| Instrument | Position in November 2023 |
|---|---|
| **Merchant Shipping Act, 1958** | **Governs.** The Merchant Shipping Act 2025 commenced 15 March 2026 — **twenty-eight months future** |
| **2023 IMO GHG Strategy** (`MEPC.377(80)`) | **OPERATIVE.** Adopted 7 July 2023, four months before this sitting. It is a strategy, not law |
| **`MEPC.328(76)`** — 2021 revised MARPOL Annex VI | **IN FORCE since 1 November 2022.** See §4 — this is where True Source is wrong, and `TSCR-3` is carried |
| **EEXI and CII** | In force 1 January 2023. **2023 is the first CII data year and it is still running at this sitting**; no ship has yet been issued a CII rating |
| **`MEPC.346(78)`** — 2022 SEEMP Guidelines | **OPERATIVE.** The corpus register marks it *superseded by `MEPC.395(82)`*; that supersession is 2024 and is **future here**. Register inversion — see §4 |
| **`MEPC.352(78)`** G1, **`MEPC.353(78)`** G2, **`MEPC.338(76)`** G3, **`MEPC.354(78)`** G4, **`MEPC.355(78)`** G5 | Operative — the 2021–2022 CII guideline set |
| **AFS Convention 2001 as amended** | In force. The **cybutryne** controls introduced by `MEPC.331(76)` **applied from 1 January 2023** — ten months old at this sitting and squarely live for Q5 |
| **ISM Code** as amended through **`MSC.353(92)`** (in force 1 January 2015) | Operative — the latest Code amendment. `MSC.428(98)` cyber-in-the-SMS obligation operative since the first DOC verification after 1 January 2021 |
| **`ISO 8217:2017`** — Petroleum products, fuels (class F), specifications of marine fuels | **The current edition at this sitting.** `ISO 8217:2024` is **eight months future**. See §4 — this is the single most dangerous donor reversal in the paper |
| **32nd Assembly instruments** | Operative — `A.1155(32)` PSC Procedures 2021, `A.1156(32)` HSSC Survey Guidelines 2021 |
| **`A.1118(30)`** Revised Guidelines on implementation of the ISM Code by Administrations | Operative — `A.1184(33)` is its successor and is future here |
| **OPRC 1990** (in force 13 May 1995) and the **OPRC-HNS Protocol 2000** | In force and unamended |
| **CLC 1992 · Fund 1992 · Bunkers 2001 · Nairobi WRC 2007 · LLMC 1976/96 with the 2012 limits** | All in force |
| **Hague-Visby Rules** | Operative in India through the **Indian Carriage of Goods by Sea Act, 1925 as amended in 1993** |
| **Marine Insurance Act, 1963** (India) | Operative |
| **MLC 2006** as amended through the **2018** set | Operative; the **2022 amendments enter force 23 December 2024** and are future |
| **IACS** unified requirements and the classification survey regimes, including **continuous survey of machinery** | Class rules, operative; not IMO instruments |

### 2.2 Future at this sitting — PROHIBITED

| Item | Date | Distance from sitting |
|---|---|---|
| **33rd IMO Assembly — every `A.118x(33)`** | adopted 6 December 2023 | **+1 month** |
| `A.1184(33)` ISM implementation guidelines | 6 December 2023 | +1 month |
| `A.1185(33)` PSC Procedures · `A.1186(33)` HSSC Survey Guidelines | 6 December 2023 | +1 month |
| **`ISO 8217:2024`** | 2024 | +8 months |
| **EU ETS extension to maritime** | 1 January 2024 | +2 months |
| `MEPC.385(81)` amendments to Annex VI regulation 18 | MEPC 81, 2024 | +5 months, and not in force until later still |
| `MEPC.395(82)` 2024 SEEMP development guidelines | 2024 | +12 months |
| **MLC 2022 amendments** | in force 23 December 2024 | +13 months |
| SOLAS Consolidated Edition 2024 | 1 July 2024 | +8 months |
| **Hong Kong Convention** | in force 26 June 2025 | +19 months |
| MEPC 81 / 82 / 83 outcomes | 2024–2025 | — |
| 34th Assembly `A.12xx(34)` | adopted 3 December 2025 | +25 months |
| IMO Net-Zero Framework / GFI | October 2025, and **still not adopted** | — |
| **Merchant Shipping Act, 2025** | commenced 15 March 2026 | +28 months |

### 2.3 The one boundary that has to be stated rather than assumed

**MEPC 80 is past and the 33rd Assembly is future.** Every donor available to this paper is a 2024,
2025 or 2026 object, and a majority of them cite `A.1185(33)` or `A.1186(33)` where this sitting
requires `A.1155(32)` or `A.1156(32)`. The reversal is applied per question and recorded in each
`temporal_review`.

---

## 3. Q1–Q9 DONOR MAP

**Every donor available to this paper is LATER than it.** That is the standing 2023 condition
(allocation §2). A donor supplies **route and shape**, never sitting-relative prose.

| Q | Printed subject | Class | Donor(s) | Distance | What was taken · what was reversed |
|---|---|---|---|---|---|
| **Q1** | Continuous survey of machinery — objectives, methodology, technology; challenges and solutions | **FRESH** (family only) | none. Family context: `QP2310-Q2` (Oct 2023, annual surveys and condition of class), `QP2308-Q8` (Aug 2023, survey types), `QP2402-Q7` (HSSC) | — | **Nothing was inherited.** CSM is a *classification* scheme and no solved question in the corpus addresses it. The two same-year family members were read to avoid contradicting them on survey vocabulary, and are cross-linked, not donated from |
| **Q2** | Mean piston speed — significance for FO consumption; relation to rpm and combustion; a Chief Engineer's method on an old ship | **FRESH** | none | — | No solved question in 39 papers touches piston speed. Authored from first principles of engine geometry and operation |
| **Q3** | Bill of lading; precautions before signing under voyage and time charter; on-hire survey under three charter types; which survey is most demanding | **LIMB** | `QP2403-Q2` / `QP2510-Q2` (B/L definition and significance); `QP2410-Q2` (charter party types and the parties' rights); `QP2302-Q6` (Feb 2023, B/L function and 'to order') | +5 to +24 months | Limb (a) only takes the B/L definition route. **Limbs (b), (c) and (d) are fresh** — no solved question addresses signing precautions or the on-hire survey. `QP2302-Q6` is the same-year member and was read first |
| **Q4** | OPRC — key provisions and objectives; role of Member States and implementation challenges; documents for Member States and ships | **NEAR** | **`QP2504-Q4`** (April 2025) | **+17 months** | Route and the MARPOL Annex I reg 37 document analysis taken. **Reversed:** the donor answers *Flag State* duties; **this paper asks Member States**, which is the wider Party obligation and pulls article 6 back *into* scope where the donor expressly excluded it. The donor's `MEPC.384(81)` Protocol I currency note is future here and is dropped |
| **Q5** | Alternatives to tin-based antifouling paints — hull roughness by paint type; oil incorporation in foul-release coatings; personnel and health safety | **FAMILY** | `QP2306-Q5` (June 2023) shares the preamble only; `QP2301-Q2` / `QP2404-Q5` / `QP2409-Q8` share the paint taxonomy; `QP2503-Q8` / `QP2307-Q7` supply hull-roughness management | +5 to +21 months | **The preamble recurs; all three printed limbs are new to the corpus.** Only the CDP / SPC / hybrid / foul-release taxonomy is inherited. Hull roughness *by paint type*, oil-incorporated silicone, and AF paint occupational health are authored fresh. `reused_from` is **null** — this is not the same examiner task |
| **Q6** | PMS and the ISM Code — corrective action; maintenance records; systematic approach; intervals and inspection periodicity | **LIMB** | `QP2401-Q4` (Jan 2024, preventive maintenance and the SMS); `QP2312-Q5` (Dec 2023, SMS and continuous improvement) | +2 to +14 months | The ISM 10/ISM 9 architecture and the maintenance-to-SMS link taken. **The four printed terms are the answer's spine and none of them is a donor heading**; the limb content is authored |
| **Q7** | Present ISO standards for marine fuel; salient features; content of a fuel oil analysis report; corrective action per adverse observation | **NEAR** | **`QP2408-Q6`** (August 2024) limb (a) | **+9 months** | Route taken. **Reversed, and this is the paper's most dangerous reversal: the donor sits after `ISO 8217:2024` and this sitting does not.** `ISO 8217:2017` is the present edition here. The donor's limb (b) on the Bunker Delivery Note is **not** set by this paper; the report-content task **is**, and is fresh |
| **Q8** | Developments in marine diesel engines, and retrofit methods enabling slow and ultra-slow steaming | **FRESH** | none. Family context: `QP2306-Q9` (skin friction), `QP2303-Q4` / `QP2310-Q5` (NOx measures) | — | No solved question addresses slow steaming or de-rating retrofits. Authored fresh, anchored on the 2023 GHG Strategy and the operational-efficiency pressure that CII created |
| **Q9** | P&I clubs — what they are and how they collect funds; risks under "protection" and "indemnity"; the minimum to get averages under a club | **NEAR** | **`QP2406-Q7`** (June 2024); also `QP2504-Q8`, `QP2502-Q7` | **+7 months** | **Limbs (a) and (b) recur almost verbatim** — the only wording change is printed *"What are P&I clubs?"* here against *"What is P&I clubs?"* in the donors. **Limb (c) is entirely different**: the donors ask how a club handles a claim; this paper asks the minimum an owner must do to *obtain cover* — entry, class, certification, condition survey, warranties, calls. Authored fresh |

### 3.1 Same-year relations — the 2023 graph used as intended

Ten 2023 papers were available in integrated or pushed governed state when this paper was built,
and four of them were read for this paper: `QP2302-Q6` (Q3), `QP2306-Q5` (Q5), `QP2308-Q8` and
`QP2310-Q2` (Q1), `QP2312-Q5` (Q6). **Not one of them supplied prose.** Their value was
*negative* — they fix the vocabulary and the temporal position this paper must not contradict, and
`QP2310-Q2` in particular sits one month before this sitting, which makes it the closest temporal
neighbour anywhere in the corpus.

### 3.2 Later-donor reversals applied

| Reversal | Where | Wrong answer it prevents |
|---|---|---|
| `ISO 8217:2024` → **`ISO 8217:2017`** | Q7 | Citing an edition published eight months after the candidate sat the paper, with its bio-blend grades and revised parameters |
| `A.1185(33)` / `A.1186(33)` → **`A.1155(32)`** / **`A.1156(32)`** | Q1, Q6 | Citing 33rd Assembly instruments adopted one month after the sitting |
| `MEPC.395(82)` → **`MEPC.346(78)`** | Q8 (SEEMP) | Citing 2024 SEEMP guidelines; the corpus register marks the 2022 set "superseded", which is true today and false here |
| `MEPC.385(81)` reg 18 replacement → **`MEPC.328(76)`** text | Q7 | Importing a 2024 amendment into a 2023 answer; the corpus resolver annotates reg 18.3 and 18.4 *"as replaced by MEPC.385(81)"* |
| `MEPC.384(81)` Protocol I amendment | Q4 | Inherited from the `QP2504-Q4` donor's own currency note; adopted 2024, in force 2026 — dropped entirely |
| MS Act 2025 → **MS Act 1958** | Q3, Q4, Q9 | The standing statute trap for the whole batch |
| Hong Kong Convention | Q8 | Not in force anywhere in 2023; end-of-life material excluded from the engine-retrofit answer |
| MLC 2022 amendments | Q9 | Not in force until December 2024; P&I financial-security material framed on the 2014 set |

---

## 4. TRUE SOURCE — WHAT WAS AVAILABLE, WHAT WAS NOT

**Corpus consumed READ ONLY at `319524c24d11b2f89f33672c384b56e9ae1ab7db`.** No corpus file was
created, edited or deleted by this session.

### 4.1 What the corpus supplied

| Question | Corpus object | Level |
|---|---|---|
| **Q7** | **MARPOL Annex VI regulation 18** — the full paragraph tree `MARPOL-VI-18-181` through `MARPOL-VI-18-1811` is present in `QP_REFERENCE_RESOLVER.json`, including 18.3 fuel oil quality, 18.5.1 the bunker delivery note and appendix V, 18.6 three-year retention, 18.8.1 the MARPOL delivered sample and its twelve-month retention, and 18.8.2 analysis per appendix VI | **Citation-ready identity only.** Standing corpus position: MARPOL Annex VI resolves to identity and provenance, **never to text**. No provision is quoted |
| **Q4** | MARPOL Annex I regulation 37 is held with a full text layer (`MEPC.117(52)`), as recorded and used by the `QP2504-Q4` donor | Primary, through the donor's verified reading — re-checked, not re-quoted |
| **all** | `10-amendment-register/AMENDMENT_REGISTER.md` — the ISM Code chain, the MARPOL Annex VI chain, the GHG guideline layer, and the treaty-status rows | Primary for instrument identity and status |

### 4.2 What the corpus does NOT hold — accepted limitations, referrals raised

| Not held | Questions affected | Disposition |
|---|---|---|
| **IACS unified requirements and classification society rules** — no `07-iacs-and-class` content addressing the continuous survey of machinery | **Q1** | `C_ACCEPTED_LIMITATION`. CSM is described at authoritative-secondary level; **no UR number is attributed a paragraph and no class rule is quoted**. **Referral raised** — see §4.3 |
| **`ISO 8217`, any edition** | **Q7** | `C_ACCEPTED_LIMITATION`. ISO standards are commercially licensed and the corpus holds none. The edition identity and the *shape* of the table are carried at authoritative-secondary level; **no limit value is presented as a quotation from the standard** and the answer says so in its own text |
| **AFS Convention 2001** | **Q5** | `C_ACCEPTED_LIMITATION`. Same class of gap as OPRC. The cybutryne amendment identity `MEPC.331(76)` and its 1 January 2023 application date are stated; no annex or regulation is quoted |
| **OPRC 1990 and the OPRC-HNS Protocol 2000** | **Q4** | `C_ACCEPTED_LIMITATION`, **already recorded** in the corpus's own acquisition records and carried unchanged from `QP2504-Q4`. No article is quoted verbatim |
| **ISM Code text** | **Q6** | `C_ACCEPTED_LIMITATION`. The amendment register holds the ISM chain and its dates to primary level, but the corpus does not hold an extractable Code text. Sections 9 and 10 are described, **not quoted** |
| **P&I club rules, the International Group pooling agreement, Marine Insurance Act 1963 text** | **Q9** | `C_ACCEPTED_LIMITATION`. Club rules are private contractual instruments and are not corpus candidates; no club rule number is cited |
| **Indian Carriage of Goods by Sea Act 1925, charter party forms (NYPE, BALTIME, BARECON, GENCON)** | **Q3** | `C_ACCEPTED_LIMITATION`. Standard forms are copyright industry documents; they are **named**, and no clause is quoted or numbered |
| **Engine-maker technical documentation** | **Q2, Q8** | `C_ACCEPTED_LIMITATION`. De-rating and slow-steaming retrofit content is engineering practice, attributed as such. **No maker, model, power figure or SFOC value is presented as sourced.** |

### 4.3 Correction requests and referrals

| Ref | Kind | Status |
|---|---|---|
| **`TSCR-3`** | Existing, OPEN. `MEPC.328(76)` entry into force is recorded a year late in the corpus register (`EIF 2023-01-01 … VERIFY 2022-11-01`). **The correct date is 1 November 2022** | **CARRIED, not re-raised.** Engaged by Q7, which cites Annex VI regulation 18 at identity level. The answer uses the correct date and does not consume the register's date |
| **`TS-REFERRAL-QP2311-1`** | **NEW — acquisition referral, not a defect.** The corpus holds no IACS or classification-society layer capable of supporting a class-survey question. `07-iacs-and-class` exists as a directory but returns nothing for continuous survey of machinery, and `QP_REFERENCE_RESOLVER.json` holds **320 entries, all of them MARPOL Annex VI** | **RAISED.** Recorded here and in `verification/QP2311/Q1.md`. No corpus file was touched |
| **`TS-REFERRAL-QP2311-2`** | **NEW — register-direction note.** `AMENDMENT_REGISTER.md` marks `MEPC.346(78)` *"SUPERSEDED by MEPC.395(82) — do not cite as current"* and annotates Annex VI regs 18.3 and 18.4 *"as replaced by MEPC.385(81)"*. Both are correct **for today** and both are **wrong for any 2023 sitting**. This is the register inversion the allocation predicted, observed and adjudicated rather than consumed | **RAISED as a directional-consumption note.** The register is not defective; it is present-tense. No correction to the corpus is requested |

---

## 5. QUESTION-LEVEL ADJUDICATIONS WORTH RECORDING

**Q3 limb (d) — "which of the above three Survey".** The limb prints a singular noun after a
plural numeral. It is preserved. The answer reads it as the examiner plainly meant — *which of the
three on-hire surveys* — and says so once, in the study guide, rather than silently repairing the
stem.

**Q3 limb (c) — "on-hire Survey … under Bare-boat charter".** A bare-boat charter conventionally
takes an **on-hire condition survey on delivery**, and the limb's premise is sound. The answer
does not dispute the premise; it explains why the bareboat survey is the one with the widest scope
and the longest consequences, which is what limb (d) then turns on.

**Q5 — the printed preamble does not govern limb (c).** *"Referring to various alternatives to
tin-based Antifouling paints"* introduces three limbs, but limb (c) — personnel and health safety
during application — is about **occupational exposure to the coating system as a whole**, not about
tin alternatives specifically. The answer treats the preamble as governing (a) and (b) fully and
(c) contextually, and says so in the exam plan.

**Q6 — the printed comma.** *"…PMS onboard ships and ISM code with the following terms,"* prints a
comma where a colon is required. The consequence is that the stem reads as though the four terms
were a continuation rather than a list; the answer supplies the structure the paper does not, and
the four printed terms become the four principal sections.

**Q9 limb (c) — "get averages under P&I club".** *Average* is a term of art in marine insurance
meaning **loss or damage**, and general average and particular average are hull-and-machinery
concepts, not P&I concepts. The limb is nonetheless answerable exactly as an examiner would expect:
it asks **what an owner must minimally do for the ship to have effective P&I cover** — enter the
ship in a club, maintain class and statutory certification, satisfy the club's condition survey and
warranties, pay the calls, and comply with the notification and co-operation conditions. The answer
states the terminological point once, in the study guide, and then answers the question that was
asked. **The stem is not corrected.**

**Q8 — the printed question mark.** The stem opens *"Discuss developments…"* and closes with `?`.
Preserved. It has no effect on the answer.

---

## 6. EVIDENCE LIMITATIONS — SUMMARY

- **Zero `A_BLOCKING` flags.** Nothing in this paper blocks publication.
- Every limitation above is a **`C_ACCEPTED_LIMITATION`** — a stated limit on the evidence, not a
  promotion of secondary material to primary.
- Two `B_CURRENCY_CHECK` flags exist and both are edition-date driven: **Q7** (`ISO 8217:2017` is
  the edition at this sitting and `ISO 8217:2024` must never be imported) and **Q5** (the cybutryne
  compliance-date arithmetic, which runs from 1 January 2023 to the first renewal survey).
- **No provision of any instrument is quoted verbatim anywhere in this paper** except where the
  quoted text was read from a held corpus object — which, for this paper, is MARPOL Annex I
  regulation 37 alone, through the `QP2504-Q4` donor's verified reading.

---

## 7. VERDICT

**ANCHOR COMPLETE.** Source reconciled by reading against the print, all nine questions
established, the historic extractor under-read investigated and resolved, every printed anomaly
preserved and recorded, the November 2023 window established as boundary-free at day level, the
donor map derived from printed stems on both sides, and every later-donor reversal recorded before
authoring began.
