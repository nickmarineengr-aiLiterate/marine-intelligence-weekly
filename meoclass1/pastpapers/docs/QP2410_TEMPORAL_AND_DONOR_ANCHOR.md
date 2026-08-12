# QP2410 — TEMPORAL AND DONOR ANCHOR

**Paper:** `QP2410` — MEO Class I, Engineering Management, **October 2024** (India)
**Printed serial:** `EM – 2410`
**Branch:** `pastpapers/qp2410-founder-review`, branched from `9c973596edb04db32c7bf4feb3cb5898b162662a`
**Built:** 2026-08-12, desktop QP team, work order `MIW::desktop::QP2410`

Written **before** any answer was authored, as
[`TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md`](TEMPORAL_AND_DONOR_VERIFICATION_PROTOCOL.md)
requires. Nothing below is inherited from intake metadata or from the allocation board; every
position was established for **this** sitting.

This is the sixth and last of the allocated 2024 papers, and the allocation names it the
**highest-risk paper in the whole 2024 set**. That is confirmed, but not for the reasons the
board gave. See §4.0 and §1.

---

## 0. THE CORPUS COMMIT ACTUALLY USED

| | |
|---|---|
| Playbook §16 / allocation §2 required commit | `64977b86ed9c601e273f1d0cb55abb0461835811` |
| **Commit actually consumed** | **`319524c24d11b2f89f33672c384b56e9ae1ab7db`** |
| Corpus state | `RulesApp-Local-Input` `main` == `origin/main`, 0 ahead / 0 behind, tracked tree clean |

The work order directs that the corpus be treated as **read-only at its current head** and not be
reset to the historic pin. That instruction governs; the departure is recorded rather than hidden.
This mirrors QP2401 §0, QP2412 §0, QP2409 and QP2411 §0.

**This paper depends on the corpus heavily — more than any other paper in the batch.** Five of the
nine questions are answered from instruments **read at source in the corpus this session**:

| Q | Instrument read at source |
|---|---|
| Q4 | **Hong Kong Convention 2009 — the complete text**, Articles 1 to 21 and the whole Annex, regulations 1 to 25 and Appendices 1 to 7 |
| Q6 | **MLC, 2006, as amended (ILO 2020 consolidated text)** — Regulation 2.5 and Standard A2.5.2 in full; **ILO Compendium of maritime labour instruments, 4th revised edition** |
| Q7 | `MEPC.328(76)` chapter 4 — for the regulatory framing only |
| Q8 | `MEPC.328(76)` regulations 23, 25, 26, 27, 28 in full; `MEPC.338(76)` G3 table 1; `MEPC.352(78)` G1 §2.4–2.5 and §5; `MEPC.354(78)` G4 §3; `MEPC.395(82)` and `MEPC.346(78)` operative paragraphs |
| Q9 | York-Antwerp Rules 2016 (via the verified April 2024 donor record) |

No corpus object was modified and no `TRUE_SOURCE_CORRECTION_REQUEST` arose.

> **One corpus finding is worth recording upward.** `QP2511-Q8` (November 2025) declared as an
> accepted limitation that *"MIW holds no licensed copy of the Hong Kong Convention text"*, and
> answered the Convention from IMO briefing material and classification-society guidance. **The
> corpus does hold it**, at `official-sources/HONGKONG_CONVENTION.pdf` — 47 pages, the complete
> instrument. `QP2410-Q4` is therefore answered at **P1 PRIMARY VERIFIED** where its donor was at
> `C_ACCEPTED_LIMITATION`. Referred to the laptop integration team as an **upgrade candidate** on
> `QP2511-Q8` and `QP2603-Q9`. Not fixed from this branch — §13.2 forbids it.

---

## 1. THE SITTING — AND THE ONE BOUNDARY THIS PAPER CANNOT RESOLVE

### 1.1 The examination date is established only to the month, and that is load-bearing

The source prints **`OCTOBER 2024`** and **`(India 2024)`**. It prints **no day**. No held source —
not the paper, not the corpus, not any MIW record — establishes the day of the sitting.

Normally that would not matter. Here it does, because of a single four-day meeting:

> ### MEPC 82 sat **30 September – 4 October 2024**, and adopted its resolutions on **4 October 2024**.
> ### The sitting month is October 2024.
> ### **This paper straddles that boundary and the day cannot be recovered.**

This is the exact inverse of QP2411's defining fact. For November 2024, MEPC 82 was unambiguously
**before** the sitting, and the committed November anchor treats `MEPC.395(82)` as operative and
`MEPC.346(78)` as revoked. **That treatment must not be pulled back one month.** For October 2024
the honest position is that the boundary is unresolved.

**How this paper handles it — the rule applied throughout:**

1. **No answer is allowed to depend on which side of 4 October 2024 the sitting fell.**
2. Where the guideline layer is touched at all (Q8 only), the answer is anchored on **the regulation
   in MARPOL Annex VI itself**, which is in force since 1 November 2022 and is edition-independent.
3. The guideline chain — `MEPC.346(78)` → amended by `MEPC.388(81)` → revoked and replaced by
   `MEPC.395(82)` on 4 October 2024 — is **stated with the boundary declared**, naming both editions
   and the revocation date, rather than silently picking one.
4. The uncertainty is recorded as a `B_CURRENCY_CHECK` on Q8, not buried.

**This is not a hedge. It is the correct answer to a question the evidence cannot settle**, and
stating it is worth more to a candidate than a confident guess: the candidate learns the boundary
and the reason it matters, which is exactly what the examiner tests when they set a question on an
instrument in flux.

### 1.2 The full boundary table

Every date below was established from a held source or from a named MIW verification record. Where
neither exists, the row says so.

| Boundary | Date | Position at **October 2024** | Evidence |
|---|---|---|---|
| 33rd IMO Assembly resolutions adopted | 6 December 2023 | **BEFORE** — `A.11xx(33)` editions operative | Batch standing anchor |
| **MLC 2014 amendments (Standard A2.5.2)** | **in force 18 January 2017** | **BEFORE — IN FORCE. Load-bearing for Q6** | ILO Compendium, read at source |
| MLC 2016 and 2018 amendments | in force before the sitting | **BEFORE** — the ILO **2020 consolidated text is the operative edition** | Held corpus edition |
| 2021 revised MARPOL Annex VI, `MEPC.328(76)` | accepted 1 May 2022; **in force 1 November 2022** | **BEFORE — IN FORCE** | Operative paras 2 and 3, read at source |
| MARPOL Annex VI EEXI / CII apply | 1 January 2023 | **BEFORE** | Regs 25, 26.3.1, 28.1, read at source |
| **`FAL.14(46)`** — mandatory maritime single window | adopted 13 May 2022; **in force 1 January 2024** | **BEFORE — IN FORCE, nine months before the sitting. This is *the* recent amendment for Q5** | MIW record `QP2403/Q1`, P1 |
| **First CII reporting deadline** | **31 March 2024** | **BEFORE — the first attained CII values have been reported and the first ratings assigned** | Reg 28.1–28.2, read at source |
| **MEPC 81** | 18–22 March 2024 | **BEFORE** | — |
| `MEPC.385(81)` Annex VI amendments | adopted 22 March 2024 | **ADOPTED BUT NOT IN FORCE** — enters into force **1 August 2025** | Held; QP2411 anchor §1.1 |
| **MSC 108** | May 2024 | **BEFORE** | — |
| `MSC.560(108)` harassment/bullying training | adopted 2024 | **ADOPTED BUT NOT IN FORCE** — 1 January 2026 | QP2411 anchor §1.1 |
| FAL 48 | 2024, before the sitting | **BEFORE** — but its output is a **guidelines** resolution, **not an annex amendment** | MIW record `QP2511/Q9` |
| **MEPC 82** | **30 Sept – 4 Oct 2024** | **BOUNDARY UNRESOLVED — see §1.1** | `MEPC.395(82)` cover page, read at source |
| **`MEPC.395(82)` 2024 SEEMP Guidelines** | **adopted 4 October 2024**, revoking `MEPC.346(78)` | **BOUNDARY UNRESOLVED.** No answer depends on it | Operative para 5, read at source |
| `MEPC.392(82)` Canadian Arctic + Norwegian Sea ECAs | adopted 4 October 2024 | **NOT IN FORCE either way** — 1 March 2026 | Held; QP2411 anchor §1.1 |
| **`FAL.15(47)`** — Recommended Practice 7.11 | adopted 17 March 2023; objection window closed **1 October 2024**; **in force 1 January 2025** | **ADOPTED BUT NOT YET IN FORCE.** Load-bearing for Q5 | MIW record `QP2511/Q9`, P1, resolution read in full |
| **Hong Kong Convention enters into force** | **26 June 2025** | **AFTER — NOT IN FORCE. Eight months after this sitting. The defining fact of Q4** | §2.1 |
| **MSC 109** | **2–6 December 2024** | **AFTER** | QP2411 anchor §3.1 |
| **MLC 2022 amendments enter into force** | **23 December 2024** | **AFTER — not in force.** Load-bearing negative for Q6 | Corpus MLC instrument log |
| **Merchant Shipping Bill, 2024 introduced in Lok Sabha** | **10 December 2024** | **AFTER — the Bill did not yet exist before Parliament.** Load-bearing for Q1 | MIW record via `QP2506/Q9`, P2 |
| FuelEU Maritime applies | 1 January 2025 | **AFTER** | QP2411 anchor §1.1 |
| Interim guidelines, ammonia as fuel | issued 26 February 2025 | **AFTER** | QP2411 anchor §3.1 |
| **MEPC 83 / IMO Net-Zero Framework / GFI** | April 2025 | **AFTER — does not exist** | QP2411 anchor §1.1 |
| FAL 49 and `FAL.18(49)` | 10–14 March 2025 | **AFTER** | MIW record `QP2511/Q9` |
| MLC 2025 amendments | adopted 6 June 2025; expected in force 23 December 2027 | **AFTER** | ILO Compendium; corpus instrument log |
| 34th IMO Assembly | 3 December 2025 | **AFTER** | Batch standing anchor |
| `MSC.560(108)` enters into force | 1 January 2026 | **AFTER** | — |
| FAL 50 | 23–27 March 2026 | **AFTER** | MIW record `QP2511/Q9` |
| **Merchant Shipping Act 2025 commences** | **15 March 2026** | **AFTER — seventeen months** | Gazette + `S.O. 1244(E)`, via `QP2607/Q7` |
| Coastal Shipping Act 2025 | 2025 | **AFTER** | Batch standing anchor |

### 1.3 Indian statute — the position is cleaner here than at any other sitting in the batch

The **Merchant Shipping Act, 1958** governs throughout, and at October 2024 it governs
**unopposed**. The Merchant Shipping Bill, 2024 was introduced in the Lok Sabha on
**10 December 2024**, two months *after* this sitting. So at this examination there was not merely
no replacing Act — there was **no Bill before Parliament at all**.

That is a genuine and useful difference from the donor. `QP2506-Q9` (June 2025) had to explain that
a Bill was pending and had been passed by neither House; `QP2508-Q5` (August 2025) had to explain
that an Act had received assent but had not commenced; `QP2602-Q5` (February 2026) sat before
commencement by three weeks. **QP2410 has none of that complexity, and the answer must not import
it.** Q1 states the 1958 Act as the operative law and records the later chain as a study-guide
currency warning for the candidate revising today, not as live law.

---

## 2. WHAT WAS READ AT SOURCE, AND WHAT IT ESTABLISHED

### 2.1 The Hong Kong Convention, 2009 — read complete, and it decides Q4

Read at source from `official-sources/HONGKONG_CONVENTION.pdf`. This is the single most important
reading on the paper.

**Article 17 — Entry into force, read verbatim.** The Convention enters into force **24 months
after** the date on which three conditions are met:

1. not less than **15 States** have signed without reservation or deposited the requisite instrument;
2. their combined merchant fleets constitute not less than **40 per cent** of the gross tonnage of
   the world's merchant shipping; and
3. their **combined maximum annual ship recycling volume during the preceding 10 years** constitutes
   not less than **3 per cent** of the combined gross tonnage of those same States.

**The consequence for this sitting, and it is decisive:**

| | |
|---|---|
| Adopted | at a diplomatic conference in Hong Kong, China, **May 2009** |
| Article 17 conditions met | **26 June 2023** — **DERIVED**, being 24 months before entry into force, on the express words of Article 17.1. Stated as derived, not as read |
| **Entry into force** | **26 June 2025** |
| **Position at October 2024** | **ADOPTED. CONDITIONS MET. ENTRY INTO FORCE FIXED AND KNOWN. NOT YET IN FORCE — eight months to run** |

The entry-into-force date of 26 June 2025 is `INTERNAL_REUSE_VERIFIED` from `QP2511-Q8`, whose
author read it on the IMO's own briefing. It is **not** re-derived here and it is not asserted as
read at source.

**This is the whole temporal content of Q4 and it inverts the donor completely.** The November 2025
donor describes a Convention in force for five months, quotes 24 Parties at about 57 per cent of
world tonnage **at entry into force**, and says "now" of the benefits. At October 2024:

- the Convention is **not in force**, so **no obligation in it binds anybody**;
- the Party count and tonnage figure at entry into force **had not yet happened** and must not be
  quoted as a current figure. **No Party count is asserted for October 2024** — none was verified;
- the certificates, the authorisations and the yard obligations are described as **what the
  Convention will require from 26 June 2025**, not as what it does require;
- but the date is **certain**, which is the interesting part of the October 2024 answer: the
  industry was in the final run-up, and that is precisely why the examiner set it.

**Other Article and regulation content read at source and carried into Q4:**

| Provision | What it establishes |
|---|---|
| Article 2 | Definitions — "Ship", "Ship Recycling", "Ship Recycling Facility", "Competent Authority", "Recycling Company" |
| **Article 3.3** | **Does not apply to ships of less than 500 GT, or to ships operating throughout their life only in waters under the sovereignty or jurisdiction of the flag State.** Note the precise scope: it is **not** "500 GT on international voyages" |
| Article 3.4 | No more favourable treatment for non-Party ships |
| Article 10 | Violations — sanctions under national law, adequate in severity to discourage |
| Article 11 | Undue delay or detention — compensation |
| Article 12 | Communication of information — the list of authorised facilities goes to IMO |
| Regulation 4 + **Appendix 1** | Controls of hazardous materials: **asbestos, ozone-depleting substances, PCBs, and anti-fouling compounds and systems regulated under the AFS Convention** |
| **Regulation 5** | Inventory of Hazardous Materials — **Part I** structure and equipment; **Part II** operationally generated wastes; **Part III** stores. Parts II and III added before recycling |
| **Regulation 5.2** | Existing ships comply **not later than 5 years after entry into force, or before going for recycling if earlier** — hence **26 June 2030** |
| Regulation 8 | Ships destined for recycling — authorised facility only; minimise residues; tanker safe-for-entry/hot-work; certified ready for recycling |
| Regulation 9 | Ship Recycling Plan — ship-specific, by the facility, explicit or **tacit** approval with a **14-day** review period |
| **Regulation 10** | Surveys — initial, renewal (not exceeding five years), additional, and **final survey** before recycling starts |
| **Regulation 11** | **International Certificate on Inventory of Hazardous Materials**; and after final survey the **International Ready for Recycling Certificate** |
| Regulations 15–16 | Facility authorisation by the Competent Authority, site inspection, **Document of Authorisation**, valid not exceeding **five years** |
| Regulations 17–23 | Facility management systems; **Ship Recycling Facility Plan**; safe-for-entry and safe-for-hot-work; hazardous material removal before cutting; emergency preparedness; worker safety and training; incident reporting |
| Regulations 24–25 | Initial notification and reporting upon completion |

> **Two precision points the donor gets slightly wrong and this paper does not.**
> First, **application** is 500 GT and *not-purely-domestic*, per Article 3.3 — not "500 GT on
> international voyages". Second, **cybutryne** is not named in Appendix 1 of the 2009 text; Appendix
> 1 controls anti-fouling systems **by reference to the AFS Convention as in force at the time of
> application**, which is how later AFS listings are caught. Q4 states it that way.

### 2.2 MLC, 2006 — the operative edition at this sitting is the one the corpus holds

Read at source from `official-sources/mlc-2006.pdf`. Its own title page:

> *"Consolidated text established by the International Labour Office, including the Amendments of
> 2014, 2016 and 2018 to the Code of the Convention. 2020"*

**That is exactly the correct edition for October 2024**, because the 2022 amendments entered into
force on **23 December 2024**, two and a half months *after* this sitting. The corpus holds the 2022
consolidation separately, and it is **deliberately not used** for this paper.

**Regulation 2.5 and Standard A2.5.2 read in full.** The provisions that carry Q6:

| Provision | What it establishes |
|---|---|
| **Standard A2.5.2 §2** | **The definition of abandonment.** A seafarer is deemed abandoned where, in violation of the Convention or the employment agreement, the shipowner **(a)** fails to cover the cost of repatriation; or **(b)** has left the seafarer without necessary maintenance and support; or **(c)** has otherwise unilaterally severed ties, **including failure to pay contractual wages for a period of at least two months** |
| Standard A2.5.2 §3 | A financial security system must be in place for ships flying the flag — social security scheme, insurance, national fund or similar |
| Standard A2.5.2 §4 | **Direct access, sufficient coverage and expedited financial assistance** |
| Standard A2.5.2 §5 | Necessary maintenance and support = adequate food, accommodation, drinking water, **essential fuel for survival on board**, and necessary medical care |
| Standard A2.5.2 §§6–7 | Certificate of financial security carried on board and **posted conspicuously**; content per **Appendix A2-I**; English or with English translation |
| **Standard A2.5.2 §9** | **What the security must cover** — outstanding wages and entitlements **limited to four months** of each; all expenses reasonably incurred including repatriation; and essential needs until arrival home |
| Standard A2.5.2 §10 | Repatriation cost — travel by appropriate and expeditious means, **normally by air**, with food, accommodation, medical care and personal effects |
| Standard A2.5.2 §11 | Security may not cease before expiry without **at least 30 days' prior notification** to the flag State competent authority |
| Standard A2.5.2 §12 | The provider acquires the seafarer's rights by **subrogation** |
| Standard A2.5.2 §14 | Not exclusive — other rights, claims and remedies survive |
| Standard A2.5 §§5–6 | Flag State must arrange repatriation and may recover from the shipowner; a State that has paid may **detain the ship**, taking the Arrest Convention 1999 into account |
| Standard A2.5 §8 | A Member **shall not refuse** repatriation because of the shipowner's financial circumstances |

**ILO Compendium, 4th revised edition — read at source.** It establishes, in the Office's own words:

- MLC, 2006 adopted **23 February 2006**, entered into force **20 August 2013**;
- the **2014 amendments entered into force on 18 January 2017**, and *"before the entry into force of
  the 2014 amendments … the MLC, 2006 did not directly address the serious problem of abandonment"*;
- the 2014 amendments introduced **Standard A2.5.2** in implementation of Regulation 2.5 §2;
- the financial security provider **can be a P&I Club**, and must provide assistance **wherever the
  abandonment takes place — even in a State that has not ratified the Convention**;
- Resolution III of the 94th (Maritime) Session, 2006 — the **Joint IMO/ILO Ad Hoc Expert Working
  Group on Liability and Compensation regarding Claims for Death, Personal Injury and Abandonment of
  Seafarers**, and the joint **Guidelines on Provision of Financial Security in Cases of Abandonment
  of Seafarers** adopted by both the IMO Assembly and the ILO Governing Body;
- amendments adopted June 2025, expected in force 23 December 2027 — **excluded**.

### 2.3 MARPOL Annex VI chapter 4 — the numbering, read off the annex itself

`MEPC.328(76)`, adopted 17 June 2021, deemed accepted 1 May 2022, **entered into force 1 November
2022** (operative paragraphs 2 and 3, read verbatim).

| Regulation | Subject |
|---|---|
| 21 | **Functional requirements** |
| **22** | **Attained EEDI** |
| **23** | **Attained EEXI** |
| 24 | Required EEDI |
| **25** | **Required EEXI** |
| **26** | **SEEMP** |
| 27 | Collection and reporting of ship fuel oil consumption data |
| **28** | **Operational carbon intensity** |

**This is the same table the November anchor calls its most important technical finding, and it is
live on this paper twice** — Q7's regulatory framing and the whole of Q8. See §7.

**Regulation 25 and Table 3, read at source — and it corrects a framing in the printed question.**
The **required EEXI** is `Attained EEXI ≤ (1 − Y/100) × EEDI reference line value`, where **Y is a
single fixed reduction factor per ship type and size band in Table 3** — bulk carrier 20 per cent
at 20,000–200,000 DWT and 15 per cent above; tanker likewise; gas carrier and general cargo ship 30
per cent; containership 20 to 50 per cent by size; ro-ro 5 per cent. **EEXI is not phased.** The
"Phase 2" language belongs to **regulation 24 Table 1, the required EEDI**, which is genuinely
phased (Phase 0/1/2/3). See §7.2 — the printed stem's framing is preserved and explained, not
corrected away.

**Regulation 28 read in full** — attained CII from calendar year 2023; report within three months;
`Required CII = (1 − Z/100) × CIIR`; ratings **A to E** with **the middle point of band C equal to
the required CII**; **D for three consecutive years or E in any year** triggers a plan of corrective
actions, a revised SEEMP submitted no later than one month after reporting, and the actions duly
undertaken; incentives encouraged for A and B; **review to be completed by 1 January 2026**.

**Regulation 26.3.1 read at source** — on or before **1 January 2023** an affected ship's SEEMP must
contain the CII calculation methodology, the required CII **for the next three years**, an
implementation plan, and a procedure for self-evaluation and improvement. **This is the hook that
lets Q8 answer the SEEMP limb without depending on the 4 October 2024 guideline boundary.**

### 2.4 The CII guideline layer — read at source

| Guideline | Resolution | Adopted | What was read |
|---|---|---|---|
| **G1** — CII and calculation methods | `MEPC.352(78)` | 10 June 2022 | §2.4–2.5 demand-based vs supply-based; **AER is the supply-based CII using DWT**, cgDIST using GT. **§5 — EEOI, EEPI, cbDIST and clDIST are encouraged for TRIAL PURPOSES only; EEOI as defined in `MEPC.1/Circ.684`** |
| **G2** — reference lines | `MEPC.353(78)` | 10 June 2022 | Identity only |
| **G3** — reduction factors | `MEPC.338(76)` | 17 June 2021 | **Table 1 — Z relative to the 2019 reference line: 2023 5%, 2024 7%, 2025 9%, 2026 11%; 2027–2030 expressly not yet set** |
| **G4** — rating of ships | `MEPC.354(78)` | 10 June 2022 | §2.4 the five grades; §3 four boundaries; the 2019 distribution the bands were set to — **A 15%, B 20%, C 30%, D 20%, E 15%**. Revokes the 2021 G4, `MEPC.339(76)` |
| **G5** — correction factors and voyage adjustments | `MEPC.355(78)` | 10 June 2022 | Identity; and its own limit — use *"should in no way undermine the goal"* |

**The G1 finding is the discriminating content of Q8(b)** and it is read at source: **AER is the
regulatory metric and EEOI is not.** EEOI is a voluntary, trial-purpose, demand-based indicator.
The question asks the candidate to "critically discuss the role of measuring metrics of AER and
EEOI", and that distinction *is* the critical discussion.

### 2.5 The SEEMP guideline chain — read at source, boundary declared

| Resolution | Adopted | Effect |
|---|---|---|
| `MEPC.282(70)` | 2016 | Revoked by `MEPC.346(78)` |
| `MEPC.346(78)` | **10 June 2022** | 2022 SEEMP Guidelines. Revoked `MEPC.282(70)` |
| `MEPC.395(82)` | **4 October 2024** | 2024 SEEMP Guidelines. Operative paragraph 5 **revokes `MEPC.346(78)`** |

Both operative paragraphs were read at source. **The boundary falls inside the sitting month and is
not resolved** — see §1.1. Q8 names the chain and the revocation date and rests its substance on
regulation 26.

### 2.6 What the corpus does **not** hold — evidence gaps declared, not filled

| Needed for | Instrument | Position |
|---|---|---|
| **Q1** | **Merchant Shipping Act, 1958** | **NOT HELD.** Sections 334, 335 and 336 come from MIW verification record `QP2602/Q5`, which read them in a reproduction of the Act. Recorded as `INTERNAL_REUSE_VERIFIED` with the limitation restated, exactly as `QP2506-Q9` did |
| **Q2** | Charterparty forms, BIMCO/INTERTANKO wordings, Indian Contract Act | **NOT HELD**, and no instrument governs a charterparty. Commercial-practice class. **No clause number is asserted anywhere** |
| **Q3** | — | No instrument is engaged. Naval architecture and engine-layout practice |
| **Q4** | Indian **Recycling of Ships Act, 2019** and Rules 2019 | **NOT HELD.** Named as the domestic implementing instruments — established via `QP2511-Q8` — with **no section number asserted** |
| **Q5** | **FAL Convention and its annex** | **NOT HELD.** Standards 1.3quin, 2.1, 2.1bis and Recommended Practice 7.11 are cited **by number and effect from the amending resolutions**, which were read at P1 for `QP2403/Q1` and `QP2511/Q9`. Articles VII(2)(a) and VII(2)(b) **are** primary, being recited in the operative text of those resolutions |
| **Q6** | ITF constitution or agreements; the joint IMO/ILO abandonment database's establishing instrument | **NOT HELD.** The ITF is described as an industry federation; the database is described **by function**, with **no resolution number invented** |
| **Q7** | Propeller design guidance; any instrument prescribing a propeller type | **NONE EXISTS.** Engineering-judgement class, as `QP2403-Q4` established |
| **Q8** | — | Fully covered at P1; see §2.3–2.5 |
| **Q9** | **Indian Marine Insurance Act, 1963** | **NOT HELD.** Named, per known trap 8, with **no section number asserted** — the same declared limitation `QP2404-Q6` carries |

**No resolution number, regulation number, article number, section number or circular number has
been invented anywhere on this paper.** Where identity could not be verified from a held copy or a
named MIW record, the instrument is described rather than numbered.

---

## 3. TEMPORAL CLASSIFICATION OF EVERY QUESTION

| Q | Subject | Classification | Risk |
|---|---|---|---|
| Q1 | Unseaworthy vessel, MSA 1958 | **INDIAN STATUTE BOUNDARY — operative before sitting.** MSA 1958 unopposed; no Bill yet before Parliament | LOW–MEDIUM |
| Q2 | Charter party — types, clauses, rights | **No instrument.** Commercial practice; nothing moved in 2024 | LOW |
| Q3 | Directional stability, manoeuvring, propeller demand curve | **No instrument.** Hydrodynamics and engine layout carry no boundary | LOW |
| Q4 | Hong Kong Convention and Indian ship recycling | **CONVENTION NOT YET IN FORCE — enters into force 26 June 2025, eight months after this sitting.** The donor is a five-months-in-force answer and inverts | **HIGH** |
| Q5 | FAL Convention — objectives and recent amendments | **SITTING-RELATIVE AMENDMENT LIMB.** `FAL.14(46)` in force; **`FAL.15(47)` adopted but NOT in force**; everything from FAL 49 onward excluded | **HIGH** |
| Q6 | Abandonment of seafarers; ILO, ITF, MLC 2006 | **Operative before sitting** — 2014 amendments in force since 18 January 2017. **MLC 2022 amendments NOT in force** (23 December 2024) | MEDIUM |
| Q7 | High-efficiency propellers | **No instrument prescribes a propeller.** Regulatory framing operative before sitting | LOW |
| Q8 | EEXI design compliance and the CII rating | **IMO INSTRUMENT IN FLUX.** Annex VI reg 23/25/26/28 in force. **First CII ratings now assigned.** SEEMP guideline edition boundary **unresolved** | **HIGH** |
| Q9 | General average — essential features and refloating | **Stable.** York-Antwerp Rules 2016 current; Rule VII materially unchanged since 1994 | LOW |

### 3.1 Q8 — the CII fact that inverts between January and October 2024

The January 2024 donor (`QP2401-Q3`) states, correctly for its own sitting:

> *"2023 was the first calculation year, the first attained CII falls due for reporting by 31 March
> 2024, and **no ship has yet been assigned a CII rating**."*

**At October 2024 that sentence is false.** The regulation 28.2 deadline of **31 March 2024** has
passed by six months. The 2023 attained CII values have been reported and verified, and **the first
CII ratings in the history of the measure have been assigned**. The October answer says so, and it
is a far better answer for it: the candidate can discuss what a D or E rating actually means to a
ship that now has one, which the January candidate could only discuss hypothetically.

The Z factor is **7 per cent for 2024** at both sittings — calendar year 2024 spans both — so that
figure transfers unchanged. The regulation 28.11 review, due by 1 January 2026, had not reported at
either sitting and nothing is asserted about its outcome.

---

## 4. DONOR ADJUDICATION — DERIVED, NOT INHERITED

The pool was every solved question on this baseline **plus** the five completed desktop papers read
from their branch git objects (`QP2401` @ `37af6d4`, `QP2412` @ `48badc3`, `QP2402` @ `af5a8d9`,
`QP2409` @ `6ca65d9`, `QP2411` @ `2cc73be`). **Corpus at derivation: 28 papers, 252 questions, 162
solved, 18 papers fully solved.** Every candidate above threshold was adjudicated by **reading both
printed stems** and then **reading the donor answer itself**.

### 4.0 The allocation board is stale — and this time it is wrong in BOTH directions

`DESKTOP_QP_ALLOCATION_2024.md` §6.2 predicts five donor relationships for QP2410. Re-derivation
against the **current** solved corpus returns a materially different picture:

| Board §6.2 | Board's prediction | **Re-derived truth** |
|---|---|---|
| `QP2410-Q4` ← `QP2511-Q8` (alt `QP2603-Q9`), HIGH | Correct donor | ✅ **CONFIRMED — 1.000 EXACT.** And the HIGH volatility flag is **correct and understated**; see §4.1 |
| `QP2410-Q5` ← `QP2511-Q7`, MEDIUM | Correct donor | ✅ **CONFIRMED — 1.000 EXACT.** Board missed a **second, earlier, same-year** relative: `QP2401-Q2` |
| `QP2410-Q9` ← `QP2404-Q6`, stable | Correct donor | ✅ **CONFIRMED — 1.000 EXACT** |
| `QP2410-Q1` | **"— " no donor**, INDIAN STATUTE BOUNDARY only | ❌ **WRONG. Three genuine donors exist** at 0.768 stem similarity; see §4.2 |
| `QP2410-Q8` | **"— " no donor**, IMO INSTRUMENT IN FLUX only | ❌ **WRONG. `QP2401-Q3` carries limb (b) VERBATIM**; see §4.5 |
| — | Board is silent on Q7 | ❌ **WRONG BY OMISSION. `QP2403-Q4` is a 0.969 same-year earlier donor**; see §4.4 |

**The board records QP2410 at Tier D 3 / 9. The true figure is 6 / 9.** Three of the six were
invisible to the board, and one of those three (`QP2402`, via the Q3 line) did not exist as a solved
paper when the board was written. This is the **third consecutive confirmation** — after QP2409 §1.1
and QP2411 §4.0 — that a frozen `reuse_tier` goes stale the moment another paper is solved.

**§6.3 of the allocation is also only half true for this paper.** Its standing rule — *"every donor
available to a 2024 paper is a 2025 or 2026 answer … pulled backwards"* — describes Q1, Q4 and Q5.
It is **false for Q7, Q8 and Q9**, whose preferred donors are **March 2024, January 2024 and April
2024** — all *earlier same-year* sittings. So this paper carries **both** hazards at once, and they
are opposite:

- **Backward pull (Q1, Q4, Q5):** what did the later author add *because* their sitting was later? Take it out.
- **Forward pull (Q7, Q8, Q9):** what happened *between* the donor's sitting and October 2024 that the donor could not know? Put it in. Audited at §5.

**No question on this paper takes a donor from `QP2411`.** The work order records that
"QP2410-Q8 is the nearest relative to QP2411-Q7". **Re-derivation does not bear that out.** Stem
similarity between `QP2410-Q8` and `QP2411-Q7` is **0.107** — the two are not close, and `QP2411-Q7`
does not appear in `QP2410-Q8`'s top six candidates at any threshold. The examiner tasks differ
completely: `QP2411-Q7` asks for the IMO **decarbonisation ambitions and pathways** plus the two
short-term measures *named*; `QP2410-Q8` asks for **EEXI design features** and then for the
**mechanics of the CII rating and its metrics**. `QP2411-Q7` is retained as a **content-family
cross-check and a cross-link**, not as a donor. The real donor for Q8 is `QP2401-Q3`, at 0.520
overall and **verbatim on limb (b)**.

### 4.1 `QP2410-Q4` ← `QP2511-Q8` (November 2025) — **EXACT stem, INVERTED answer**

Stem similarity **1.000**. `QP2603-Q9` (March 2026) is 0.996, differing only in a typographic
apostrophe, and is **rejected as preferred donor** for being a further four months later.

- **Question delta: NIL.** Character-for-character identical, including the curly apostrophe in
  `India's`.
- **Marks delta: NIL.** Undifferentiated `(16)` at both sittings.
- **Temporal delta: TOTAL, and it is the largest single delta in the whole desktop batch.**

> #### The donor is an in-force answer. This sitting is a not-in-force answer.
>
> `QP2511-Q8` was written eight months into the Convention's life. Its own temporal review records
> the warning explicitly: *"KEPT AFTER ADJUDICATION: the Convention treated as IN FORCE … **This is
> NOT the position at the October 2024 member of the same family, and that member must not inherit
> this object unmodified.**"*
>
> **That warning is this question.** Everything the donor states in the present tense becomes future
> tense here, and the following are stripped:
>
> - **"entered into force on 26 June 2025"** → *will enter into force on 26 June 2025, eight months
>   after this examination*;
> - **"24 Parties representing about 57 per cent of world tonnage"** → **deleted.** That is the
>   position *at* entry into force, which has not happened. No October 2024 figure was verified and
>   **none is asserted**;
> - **the word "now"** in the benefit block → deleted; nothing has changed yet;
> - **every operative obligation** — certificates held, yards authorised, plans approved → recast as
>   what the Convention **will require**;
> - **the Merchant Shipping Act, 2025 reasoning** → deleted entirely. The donor devotes a paragraph
>   and a retrieval card to explaining that the 2025 Act had been assented but not commenced. At
>   October 2024 that Act did not exist in any form, not even as a Bill. The *conclusion* survives —
>   ship recycling is governed by the separate Recycling of Ships Act, 2019 — and the *reason*
>   changes: at this sitting the general statute is simply the 1958 Act, and there is nothing else
>   to discuss.
>
> **What is added, and it is what makes the October 2024 answer distinctive:** the Convention is in
> its **final run-up**. The date is fixed and known; owners, yards and administrations are preparing
> against a deadline eight months out. That is a genuinely different and more interesting commercial
> position than either "awaiting conditions" or "in force", and it is why an October 2024 examiner
> set the question.

**What is KEPT deliberately:** **26 June 2030**, the existing-ship inventory deadline. It is derived
from regulation 5.2 (five years after entry into force) applied to a date already fixed, so it is
equally stateable at this sitting. A blind post-sitting date strip would delete a correct answer
point — the same adjudication the November anchor made at its §7.

**Upgrade over the donor:** the whole Convention was read at source here (§2.1), so Q4 asserts
regulation and article numbers at **P1 PRIMARY VERIFIED**, and corrects the donor's application
scope. See §2.1.

### 4.2 `QP2410-Q1` ← `QP2506-Q9` (June 2025) — near-exact, **and the board said there was no donor**

Three donors share one stem family. Ranked:

| Donor | Sitting | Stem similarity | Verdict |
|---|---|---|---|
| **`QP2506-Q9`** | **June 2025** | **0.768** | **PREFERRED** — nearest sitting, and its own temporal work is the cleanest of the three |
| `QP2508-Q5` | August 2025 | 0.421 | Rejected — further away, and its answer turns on the 2025 Act having received assent *in the month of its own sitting*, which is pure backward-pull contamination here |
| `QP2602-Q5` | February 2026 | 0.421 | Rejected — sixteen months later; carries the fullest 2025-Act treatment |

- **Question delta: REAL AND STRUCTURAL.** June 2025 prints one undifferentiated running stem.
  **October 2024 prints three lettered limbs with three separate mark allocations** — `a) (5)`,
  `b) (6)`, `c) (5)`. The three demands are the same three demands, in the same order, but they are
  now *marked separately*.
- **Marks delta: MATERIAL.** `(16)` undifferentiated → **`5 + 6 + 5`**. The consequence decides the
  answer shape: **limb (b), the comparison, carries the most marks of the three.** That is the limb
  candidates most often omit, and on this paper omitting it costs six marks out of sixteen. The
  October answer is therefore built to three limbs in the printed proportion, not to the donor's six
  running steps.
- **Wording delta:** October drops the quotation marks the June paper prints around
  `"Unseaworthy vessels"`, `"Unseaworthy ships"` and `"Unsafe ships"`, and uses the **singular**
  (`Unseaworthy vessel`, `Unseaworthy ship`, `Unsafe ship`). Preserved as printed in both specs.
- **Temporal delta: REAL AND SIMPLIFYING.** See §1.3. The donor must explain a pending Bill; this
  paper must explain that no Bill existed. **Everything the donor says about the Merchant Shipping
  Bill 2024, its passage, its assent and its commencement is taken back out of the answer** and
  appears only as a study-guide currency warning aimed at a candidate revising today.
- **Donor answer inspected.** Its statutory content — the section 334 description of
  unseaworthiness, the two offences and their defences, the section 336 unsafe-ship definition and
  the staged detention procedure, and the section 335 implied non-excludable obligation — is
  sitting-independent and is reused as verified internal reuse, re-shaped to the printed limbs.

### 4.3 `QP2410-Q5` ← `QP2511-Q7` (November 2025) — **EXACT stem, and the amendment limb re-derived**

Stem similarity **1.000**, character for character.

- **Question delta: NIL. Marks delta: NIL** — `(16)` at both.
- **Temporal delta: MATERIAL, and confined precisely to the amendment limb.** The objectives and
  mechanism limbs are sitting-independent and transfer. The "recent amendments" limb is by
  definition sitting-relative and is **re-derived from this paper's own anchor**:

| Instrument | At November 2025 (donor) | **At October 2024 (this paper)** |
|---|---|---|
| `FAL.14(46)` — mandatory single window | in force 1 Jan 2024 | **IN FORCE, nine months before the sitting.** *The* recent amendment |
| `FAL.15(47)` — Recommended Practice 7.11 | **in force 1 Jan 2025**, ten months before | **ADOPTED, NOT IN FORCE.** Objection window closed 1 Oct 2024; enters into force 1 Jan 2025 |
| FAL 49 items (RP 6.24, revised MSW Guidelines, new Compendium edition) | approved only | **DO NOT EXIST** — March 2025 |
| `FAL.18(49)` mooring personnel | adopted, guidelines | **DOES NOT EXIST** |
| `FAL.17(48)` wildlife smuggling | adopted, guidelines | **Adopted before the sitting**, but a **guidelines** resolution, not an annex amendment |
| FAL 50 | after the donor's sitting | **DOES NOT EXIST** — March 2026 |
| IMO Strategy on Maritime Digitalization | a work plan | **Not an instrument.** Excluded |

> **The October 2024 position is sharper than the donor's and is the better teaching example.** At
> this sitting there is exactly **one** annex amendment recently in force and exactly **one**
> adopted and waiting — and the waiting one's tacit-acceptance objection window closed at the very
> start of the examination month. A candidate who can say *"`FAL.14(46)` in force since 1 January
> 2024; `FAL.15(47)` adopted, objection window closed, in force 1 January 2025"* has demonstrated
> the adopted / in-force distinction on live facts, which is precisely what the examiner is testing.

**Second donor found and used as a cross-check, not inherited: `QP2401-Q2` (January 2024)** — *"FAL
Convention — Provisions, Impact and Significance"*, 0.359 stem similarity, three lettered limbs at
6 + 4 + 6. **Same instrument, same year, ten months earlier, different examiner task** — it asks for
provisions, efficiency/security impact and global-cooperation significance; it does **not** ask for
the recent amendments or for digitalization and sustainability. Classified **PARTIAL / content-family**:
its objectives-and-mechanism material corroborates this answer's first two steps, and it confirms
that the single-window amendment was already in force at the start of 2024. **No `reused_from` is
written to it** — the preferred donor is the exact-stem November 2025 object.

### 4.4 `QP2410-Q7` ← `QP2403-Q4` (March 2024) — near-exact, and the delta **reverses the donor's advice**

| Donor | Sitting | Stem similarity | Verdict |
|---|---|---|---|
| **`QP2403-Q4`** | **March 2024** | **0.969** | **PREFERRED — earlier, same year, seven months before** |
| `QP2510-Q4` | October 2025 | 0.969 | Rejected as preferred: identical stem to `QP2403-Q4`, but a **year later**. Used as corroboration only |

- **Question delta: SMALL IN WORDS, DECISIVE IN EFFECT.** March 2024 prints *"Discuss **any three
  of** the following high-efficiency propellers"*. **October 2024 prints *"Discuss the following"* —
  the three words are gone.**

> #### The October paper requires **all four**. The donor's own closing advice must be reversed.
>
> `QP2403-Q4` ends by telling the candidate *"the stem asks for any three of the four … Three
> treated properly earns more than four treated superficially"*, and it demotes **azimuth
> propulsion** to the Study Guide as the optional fourth. **On this paper that advice is wrong and
> would cost marks.** Azimuth propulsion is promoted to a full model-answer section, the sixteen
> marks divide four ways at roughly four marks per device, and the answer is built to cover four
> devices with merits and demerits each — a genuinely different budget from the donor's.

- **Marks delta: presentational.** October prints `(16)` inline after the colon; March prints it at
  the end. Both are 16 with four unmarked limbs.
- **Temporal delta: NIL on the hydrodynamics.** Propeller theory is not dated law. Confirmed against
  §5.
- **UPGRADE OVER THE DONOR.** `QP2403-Q4` recorded as an accepted limitation that *"MARPOL Annex VI
  was NOT read in a licensed consolidated edition … the Model Answer asserts NO regulation number
  and NO date for EEXI or CII."* **`MEPC.328(76)` has been read at source for this paper (§2.3).**
  Q7's regulatory framing therefore cites the correct 2021 numbering at P1 where the donor could
  only gesture at it — and the answer still quotes **no percentage efficiency gain for any device**,
  which remains a deliberate omission for exactly the donor's reason.

### 4.5 `QP2410-Q8` ← `QP2401-Q3` (January 2024) — **PARTIAL: limb (b) is verbatim, limb (a) is fresh**

Overall stem similarity 0.520, which understates the relationship. Aligned limb by limb:

| Limb | October 2024 | January 2024 donor | Relationship |
|---|---|---|---|
| **(a)** `(8)` | EEXI design features for existing vessels to meet "Phase 2 (of 20% - 30% reduction)" | — | **NO DONOR. FRESH RESEARCH** |
| **(b)** `(8)` | *"Explain the concept of CII rating and critically discuss the role of measuring metrics of AER and EEOI. What are the measures required to be taken by the vessel to improve its CII ratings."* | **identical text, at `(16)`** | **EXACT — word for word** |

- **Question delta on limb (b): NIL.** The donor's entire printed stem is limb (b) of this question,
  reproduced without the change of a character.
- **Marks delta on limb (b): HALVED — `(16)` → `(8)`.** This is the governing constraint. The donor
  spends four full model-answer sections on the mechanism, AER, EEOI and the improvement measures,
  correctly, for sixteen marks. **Here the same material is worth eight and must share the question
  with an equally-weighted EEXI limb.** The October answer keeps the discriminating content — the
  AER-versus-EEOI critique and the corrective-action trigger — and compresses the recital.
- **Temporal delta: REAL. See §3.1.** The donor's most distinctive sentence — no ship has yet been
  rated — is false here.
- **Limb (a) has no donor anywhere.** `QP2503-Q7` (March 2025) *"EEDI Phase 2 Design Features"* is
  the nearest stem in the corpus at 0.455 and **carries no answer — the paper is unsolved intake**.
  It is recorded as a cross-family relative and nothing is taken from it. Limb (a) is fresh research
  from `MEPC.328(76)` regulations 23 and 25 read at source, plus settled engineering.

### 4.6 `QP2410-Q9` ← `QP2404-Q6` (April 2024) — **EXACT, all three deltas genuinely NIL**

Four donors carry this stem. Ranked:

| Donor | Sitting | Stem similarity | Verdict |
|---|---|---|---|
| **`QP2404-Q6`** | **April 2024** | **1.000** | **PREFERRED — earlier, same year, six months before. No backward pull is possible from it** |
| `QP2506-Q6` | June 2025 | 1.000 | Rejected as preferred — eight months later |
| `QP2508-Q6` | August 2025 | 1.000 | Rejected — ten months later |
| `QP2602-Q6` | February 2026 | 0.991 | Rejected — sixteen months later; prints *"Give **proper** justification"* |

- **Question delta: NIL.** Identical, including the printed capital in `Included`.
- **Marks delta: NIL.** `8 + 8` at both sittings.
- **Temporal delta: NIL, and checked in both directions.** General average is among the most stable
  doctrines in maritime law. The York-Antwerp Rules 2016 were the current CMI text at April 2024 and
  at October 2024; Rule VII is materially unchanged from the 1994 and 2004 texts, and the Rules bind
  by **contractual incorporation, not as law**, so the version question is a contract question at
  both sittings alike. Nothing relied on entered force or was superseded in the six-month window.

**All three deltas are genuinely nil and are recorded as such rather than left implied**, as the
temporal protocol §4 requires. **That does not license copying the object.** The answer is
re-authored for this sitting; the substance transfers because the law did not move.

### 4.7 The three fresh researches

`Q2`, `Q3` and `Q6` have **no verified donor**. Derived tier **C** for each, confirmed by stem
re-derivation against all 162 solved questions.

| Q | Best candidate anywhere in the corpus | Verdict |
|---|---|---|
| **Q2** | **Nothing above 0.35.** No solved question anywhere treats charterparties. `QP2502-Q7` (Feb 2025, P&I clubs) and `QP2506-Q3` (marine insurance short notes) are the nearest commercial-law neighbours | **NO DONOR.** Fresh research. Charterparty law is a genuine gap in the MIW corpus |
| **Q3** | `QP2407-Q7` (July 2024) *"Propeller Curves, Safety Margins and the Engine Layout Diagram"* — **0.583 on shared vocabulary**, the closest relative in the corpus to limb (B) | **NOT A DONOR — the paper is unsolved intake.** Same-year, three months earlier, and it carries no answer. Recorded as a cross-family relative. Fresh research |
| **Q6** | `QP2407-Q6` (July 2024) *"MLC 2006 — Flag State and Port State Obligations"*; `QP2409-Q1` (Sept 2024) fitness for duty | **NOT DONORS.** `QP2407-Q6` is **unsolved intake**; `QP2409-Q1` is a different regime question about watchkeeping fitness. No solved question treats abandonment. Fresh research from the MLC read at source |

**Reuse count was not optimised for.** Six of nine questions carry a donor, but three of the six are
partial or structural and every one of the six required substantive re-anchoring. Correct
October-2024 answers are the objective.

### 4.8 Host recurrence hints — discovery only

The source copy carries third-party host annotations: `2019/OCT 2020/MAR/Q9 2023/JUL/Q9` on Q1;
`2017/FEB 2017/DEC 2021/JUL/Q4 2021/AUG/Q4` on Q3; `2023/FEB/Q3` on Q8; `2023/JAN/Q6 2024/APR/Q6`
on Q9. These are **not MIW truth**, they point backwards only, and **no `reused_from` was written
from them.** In every accepted case the donor was established independently by stem re-derivation
and confirmed by reading both printed stems and the donor answer. They must not leak to any
candidate-facing surface.

Two observations worth recording:

- The Q9 hint at `2024/APR/Q6` **does** coincide with the independently-derived preferred donor
  `QP2404-Q6`. Coincidence is not authority — the donor stands on the stem re-derivation.
- The hints on **Q1** (2019, 2020, 2023) and **Q3** (2017 twice, 2021 twice) point at sittings
  **MIW does not hold at all**. They could not have been used even if they were authority.
- **Q2, Q4, Q5, Q6 and Q7 carry no prior-sitting hint at all** — the host treats five of the nine as
  new. For Q4, Q5 and Q7 that is demonstrably wrong as a statement about the question family, since
  MIW independently derived exact or near-exact relatives. It is a further illustration of why host
  annotations are directional and systematically under-report.

---

## 5. THE FORWARD-PULL WINDOW AUDIT — January / March / April 2024 → October 2024

Three donors (Q7, Q8, Q9) are **earlier** than the sitting, so the window between them is audited
explicitly rather than assumed empty. This is the opposite question from §4.1's.

| Event in the window | Date | Touches `QP2403-Q4` (Q7, propellers)? | Touches `QP2401-Q3` (Q8, CII)? | Touches `QP2404-Q6` (Q9, GA)? |
|---|---|---|---|---|
| **First CII reporting deadline** | **31 Mar 2024** | No | **YES — the single material change. The first ratings are now assigned; the donor says none had been** | No |
| **MEPC 81** | 18–22 Mar 2024 | No — no chapter 4 renumbering | `MEPC.385(81)` is low-flashpoint-fuel and DCS granularity, **in force 1 Aug 2025**, after this sitting. `MEPC.384(81)` likewise not cited | No |
| **MSC 108** | May 2024 | No | No | No |
| **MEPC 82** | **30 Sep – 4 Oct 2024** | No | **BOUNDARY — SEEMP guideline edition only. Handled per §1.1; the answer does not depend on it** | No |
| `MEPC.392(82)` ECAs | adopted 4 Oct 2024 | No | No — in force 1 Mar 2026 | No |
| York-Antwerp Rules | no CMI revision in the window | No | No | **No. 2016 remains the current text** |
| Merchant Shipping Bill 2024 | introduced **10 Dec 2024** | No | No | No — and after the sitting in any event |

**Conclusion: the forward pull is benign on Q7 and Q9, and requires one substantive change plus one
declared boundary on Q8.** No proposition in any of the three donors was falsified by an event in
the window, except `QP2401-Q3`'s "no ship has yet been assigned a rating", which is corrected.

---

## 6. CORPUS USE

| Instrument | Held? | How used on this paper |
|---|---|---|
| **Hong Kong Convention, 2009** | **YES — complete** | **READ AT SOURCE for Q4** — Articles 2, 3, 10, 11, 12, **17**; Annex regulations 4, 5, 8, 9, 10, 11, 15–25; Appendices 1 and 2. **P1 PRIMARY VERIFIED.** An upgrade over the donor — see §0 |
| **MLC, 2006 as amended (ILO 2020 consolidated, incl. 2014/2016/2018)** | **YES** | **READ AT SOURCE for Q6** — Regulation 2.5, Standard A2.5 §§5–8, **Standard A2.5.2 in full**. **The correct edition for this sitting.** P1 PRIMARY VERIFIED |
| **ILO Compendium of maritime labour instruments, 4th rev. ed.** | **YES** | **READ AT SOURCE for Q6** — adoption and entry-into-force dates, **the 18 January 2017 date for the 2014 amendments**, the P&I-club point, the Joint IMO/ILO Ad Hoc Expert Working Group and the joint abandonment guidelines. P1 |
| MLC 2022 consolidated text; MLC 2025 STC papers | **YES** | **READ ONLY to establish they are AFTER this sitting.** Deliberately not used as law |
| **`MEPC.328(76)`** 2021 revised MARPOL Annex VI | **YES** | **READ AT SOURCE for Q7 and Q8** — operative paras 2–3; chapter 4 regulation list; regs 23, 24 (Table 1), 25 (Table 3), 26, 27, 28 in full. **P1 PRIMARY VERIFIED** |
| **`MEPC.338(76)` G3** | **YES** | **READ AT SOURCE for Q8** — Table 1 Z factors. P1 |
| **`MEPC.352(78)` G1** | **YES** | **READ AT SOURCE for Q8** — §§2.4–2.5 and §5. **The AER/EEOI distinction.** P1 |
| **`MEPC.354(78)` G4** | **YES** | **READ AT SOURCE for Q8** — §§2.4 and 3, rating bands. P1 |
| `MEPC.353(78)` G2, `MEPC.355(78)` G5 | **YES** | Identities and adoption dates. P1 |
| **`MEPC.395(82)`, `MEPC.346(78)`** | **YES** | **READ AT SOURCE** — adoption dates and operative revocation paragraphs, to establish the §1.1 boundary exactly |
| `MEPC.385(81)`, `MEPC.392(82)` | **YES** | Entry-into-force dates only, to classify them as adopted-but-future |
| `MEPC.377(80)` 2023 GHG Strategy | **YES** | **Context only** on Q7 and Q8. No ambition level is attributed to regulation 28 |
| **Merchant Shipping Act, 1958** | **NO** | **Q1 — declared limitation.** Sections 334–336 via MIW record `QP2602/Q5` |
| Merchant Shipping Act, 2025; Coastal Shipping Act 2025 | **YES** | **READ ONLY to confirm they are AFTER this sitting.** Not used as law anywhere |
| **FAL Convention and annex** | **NO** | **Q5 — declared limitation.** Standards cited by number and effect from the amending resolutions |
| **Recycling of Ships Act, 2019 (India)** | **NO** | **Q4 — declared limitation.** Named; no section asserted |
| **Marine Insurance Act, 1963 (India)** | **NO** | **Q9 — declared limitation** (known trap 8). Named; no section asserted |
| Charterparty forms and wordings | **NO** | **Q2** — no instrument exists to hold. Commercial-practice class |
| LSA Code, FSS Code, IMDG, SOLAS, STCW | Held | **Not required by any question on this paper** |

**No corpus object was modified.** No `TRUE_SOURCE_CORRECTION_REQUEST` arose from this paper.

---

## 7. THE INHERITED DONOR DEFECT — AND WHY IT IS LIVE TWICE HERE

### 7.1 The regulation-21 defect must not be reintroduced

`QP2402-Q3` (February 2024) maps EEDI to **MARPOL Annex VI regulation 21**. That is the **pre-2021
numbering**, in which chapter 4 ran reg 20 attained EEDI / reg 21 required EEDI / reg 22 SEEMP — the
scheme **superseded by `MEPC.328(76)` when the revised Annex VI entered into force on 1 November
2022**. The defect was found and referred by `QP2411` §4.2 and is **still open upstream**.

**QP2410 does not inherit it, and the exposure is doubled**: both Q7 and Q8 touch chapter 4. The
numbering read at source at §2.3 governs both:

> **Reg 21 functional requirements · reg 22 attained EEDI · reg 23 attained EEXI · reg 24 required
> EEDI · reg 25 required EEXI · reg 26 SEEMP · reg 27 fuel oil consumption data · reg 28 operational
> CII.**

`QP2402` is **not modified from this branch** — §13.2 forbids it. The referral stands.

### 7.2 A second, subtler numbering trap that is specific to this paper

The printed Q8(a) says *"the EEXI framework under **Phase 2** (of 20% - 30% reduction)"*.

**Read at source, EEXI has no phases.** Regulation 25 Table 3 sets **a single fixed reduction factor
Y per ship type and size band** — 20 per cent for a Panamax-to-VLCC bulk carrier or tanker, 30 per
cent for a gas carrier or general cargo ship, 15 to 50 per cent for containerships by size. The
**phases belong to regulation 24 Table 1, the required EEDI**, which runs Phase 0/1/2/3 on dated
windows.

**The printed wording is preserved exactly and is not corrected in `text_verbatim`.** The answer
explains the position from source: it identifies what the examiner is reaching for — the EEXI
reduction factors do fall in the 15–30 per cent band for most merchant ship types, and they are
derived from the **EEDI phase 2 reference-line stringency** — and states plainly that the phased
scheme is the EEDI's. That is the honest reading of a slightly loose stem, and it is the sort of
distinction that separates a Class I answer from a recital.

---

## 8. WHAT THIS PAPER DELIBERATELY DOES NOT SAY

A contamination sweep target list, stated positively so it can be checked mechanically.

- **The Hong Kong Convention presented as in force** — it enters into force 26 June 2025, **eight
  months after this sitting**. This is the October-specific trap and the highest-value one on the paper
- **Any Party count or tonnage percentage for the Hong Kong Convention** — the 24 Parties / 57 per
  cent figure is the position *at entry into force*, which has not happened
- **`FAL.15(47)` presented as in force** — 1 January 2025
- **FAL 49, `FAL.18(49)`, the revised Maritime Single Window Guidelines, the new IMO Compendium
  edition, FAL 50** — March 2025 and March 2026
- **The IMO Strategy on Maritime Digitalization** as an adopted instrument
- **MLC 2022 amendments presented as in force** — 23 December 2024, two and a half months too late
- **MLC 2025 amendments** — adopted June 2025, expected in force 23 December 2027
- **The Merchant Shipping Act, 2025, the Merchant Shipping Bill 2024, or the Coastal Shipping Act
  2025** — the Bill was not introduced until 10 December 2024 and the Act commenced 15 March 2026
- **`MEPC.395(82)` presented as unambiguously operative, OR `MEPC.346(78)` presented as
  unambiguously operative** — the 4 October 2024 boundary is declared, not decided
- **Any MEPC 83 or later outcome; the IMO Net-Zero Framework; the GFI; draft MARPOL Annex VI
  chapter 5** — April 2025
- **Any resolution numbered above `MEPC.395(82)`**
- **`MEPC.385(81)` or `MEPC.392(82)` presented as in force** — 1 August 2025 and 1 March 2026
- **`MSC.560(108)` presented as in force** — 1 January 2026
- **MSC 109, the ammonia interim guidelines** — December 2024 and February 2025
- **FuelEU Maritime presented as applying** — 1 January 2025
- **`A.12xx(34)`** and every 34th Assembly instrument — fourteen months too early
- **Pre-2021 MARPOL Annex VI chapter 4 numbering** — regulation 21 is *Functional requirements*, not
  EEDI. See §7.1
- **"No ship has yet been assigned a CII rating"** — true in January 2024, **false here**. See §3.1
- **Any invented MSA 1958 section beyond 334–336, Recycling of Ships Act section, Marine Insurance
  Act 1963 section, FAL Standard, charterparty clause number, or percentage efficiency gain for a
  propeller device**

---

## 9. STANDING TRAPS FOR THE REVIEWER TO CHECK

1. **Q4 must say the Hong Kong Convention is NOT YET IN FORCE**, and must give 26 June 2025 as a
   future date. It must quote no Party count.
2. **Q4 must not mention the Merchant Shipping Act 2025** in any form. The donor does, six times.
3. **Q5 must place `FAL.14(46)` in force and `FAL.15(47)` adopted-but-not-in-force**, and must name
   nothing from FAL 49 or later.
4. **Q1 must state that no replacing Bill was before Parliament**, not that a Bill was pending.
5. **Q1 must answer to the printed 5 + 6 + 5 split**, with the comparison limb carrying the most.
6. **Q7 must treat all FOUR propeller types.** The donor's "any three" advice is reversed.
7. **Q7 and Q8 must use the 2021 numbering** — attained EEDI 22, attained EEXI 23, required EEXI 25,
   SEEMP 26, CII 28. Never regulation 21 for EEDI. See §7.1.
8. **Q8 must say the first CII ratings have been assigned**, not that none has been.
9. **Q8 must state that EEOI is a trial-purpose, voluntary metric** and AER the regulatory one.
10. **Q8 must declare the 4 October 2024 SEEMP guideline boundary** rather than picking a side.
11. **Q9 must not assert a Marine Insurance Act 1963 section number** (known trap 8), and must record
    that the York-Antwerp Rules bind by contractual incorporation.
12. **Q2 must not invent a charterparty clause number** or attribute a clause to a named form it was
    not verified in.
13. **No percentage efficiency gain anywhere on Q3 or Q7**; no vendor or product named.
14. **No third-party host branding anywhere** (known trap 14). The source pages carry it throughout.

---

## 10. NOT A QP2410 MATTER

The global reuse map, the reverse-hint queue, recurrence indexes, `pastpapers_content_index.json`,
`questions-2024.html`, `topics-2024.html`, `solvedQP/*`, `CURRENT_STATUS.md` and
`history/SESSION_HISTORY.md` are **laptop-owned**. Solving this paper makes the global reuse map
stale; that staleness is **expected and is not committed from this branch**.

Two findings are **referred, not fixed**:

1. The `QP2402-Q3` regulation-mapping defect (§7.1), already referred by `QP2411` and still open.
2. The `QP2511-Q8` / `QP2603-Q9` **source-availability under-statement** (§0) — those answers declare
   that MIW holds no copy of the Hong Kong Convention, and it does. They are answerable at P1.
