# GPT REVIEW PASS 2B — MS ACT 2025 SURGICAL IMPLEMENTATION

**Date:** 2026-09-04
**Baseline:** HEAD `4784b9c`, origin/main `9e26f02`, 2 ahead / 0 behind, tree clean
**Origin:** `gpt_content_review` — Founder/GPT authorisation issued from *GPT REVIEW PASS 2A
— MS ACT 2025 EXACT-SECTION MAPPING*
**Governs:** `CORR-MSACT2B-CEHANDOVER-20260904`, `CORR-MSACT2B-GREEN-20260904`,
`CORR-MSACT2B-CASUALTY-20260904`, `CORR-MSACT2B-COC-20260904`

---

## 0. What this pass is

A bounded legal-currentness pass against **one primary instrument**: the Merchant
Shipping Act, 2025 (Act No. 24 of 2025), `SRC-MSACT-2025`, held at sha256
`6fb38616ed8b82ae7e831e5589ffd59a7b27e13d55b1728940fe25892f758f63`, with its
corrigenda of 30 September 2025, `SRC-MSACT-2025-CORRIGENDA`, sha256
`4a28b152426b0cd709be37a4bc0c176be059f56eed97566fe96ed0b1bedcf818`. Both digests
were re-verified against the files at rest before any edit was made.

It is **not** a legal rewrite. No new subject was authored, no card was created, no
examiner attribution changed and no past paper was touched.

## 1. Evidence discipline — what was actually done

Pass 2A's mapping was delivered in review, not on disk. It was therefore treated as an
**authorisation**, not as evidence, and every one of the 23 authorised section mappings
was **independently re-verified against the held Gazette text** before being written
candidate-facing. The Act's text layer was extracted in full — 118 pages, 393,583
characters — and each section resolved and read.

**Result: all 23 authorised mappings confirmed, plus `s.12`, which the brief named
conditionally. Each occurs exactly once as an operative section.** The full mapping, the
Part structure and the negatives are now registered in `SRC-MSACT-2025`.

### 1.1 Two extraction hazards, recorded because one produced a false negative

* The Act's PDF separates a section number from its text with a **`0x03` control byte**
  as well as with a space. A `^[0-9]+[.]\s` scan therefore under-reports: **`s.319` was
  reported "NOT FOUND" on the first pass and is present**, exactly where the
  authorisation said. A negative from a text scan is only evidence once the scan is
  proved able to find a positive.
* The **`s.281(2)` penalty table renumbers its rows `1..N`**, so a naive scan resolves
  "section 15" to a table row about `s.139`. Table rows must be excluded before a
  section number is resolved.

### 1.2 Corrigenda

Three corrections, all typographical — page 33 line 19 *matter*→*matters*; page 69
line 24 *himself such*→*himself of such*; page 71 line 12 *sea borne*→*seaborne*. **None
touches any mapped provision.** The mapping stands against the corrected text.

## 2. Three findings the authorisation did not contain

These came out of reading the provisions rather than accepting the mapping, and two of
them changed what the cards were allowed to say.

1. **`s.324(1)` is narrower than "except Part XIV".** The enacted text is *"except Part
   XIV **but not including section 411A therein**"*. The saving is Part XIV **minus**
   `s.411A`. Every card stating the repeal now carries that limb. Quoting `s.411A` is not
   a new 1958 assertion — it is quoted from inside `s.324(1)` of the 2025 Act itself.
2. **"Very serious marine casualty" appears exactly once in the Act, and is not
   defined.** It occurs only inside the `s.224(a)` inclusion list for *marine incident*.
   The Act **names** the term; the definition remains Casualty Investigation Code
   (MSC.255(84)) terminology. A card saying "the Act defines it" is wrong; a card saying
   "the term does not appear" is also wrong. `QB9_H#q11` now states the true, narrower
   proposition.
3. **The registry's wrong locator carried a right proposition.** `s.93(c)` does not
   exist — `s.93` has clauses (a), (b), sub-clauses (i)–(iv) and an Explanation defining
   *international voyage*. The shipping-master definition is in the **Explanation to
   `s.91`, clause (c)**. Nothing candidate-facing was wrong, which is precisely why
   nothing candidate-facing could have flagged it.

## 3. Negatives established by whole-document search

Each of these is load-bearing for a correction below, and each was established by
searching the whole Act rather than by inference.

| Search term | Occurrences | What it authorises |
|---|---|---|
| `formal investigation` | **0** | The stale-terminology correction (§4 of the brief) |
| `contingency plan` / `OPRC` / `NOS-DCP` / `national oil spill` | **0** | `QB3_J#q5` may not claim the Act names NOS-DCP |
| `handover` / `hand over` / `taking over` / `taking-over` / `delivery of charge` / `chief engineer` | **0** | The RED item: no CE-handover provision exists |

The ISM Code was checked on the same terms, from the held `A.741(18)` text: it contains
**zero** occurrences of `handover`, `takeover`, `taking over` or `chief engineer`. ISM
**§5 is "Master's Responsibility and Authority"** and concerns the master, not the CE.
**§6.3** requires familiarisation for personnel transferred to new assignments and **§7**
requires procedures for key shipboard operations — those two, plus the company's SMS, are
the whole defensible basis for a CE handover, and no ISM clause prescribes a takeover
certificate.

## 4. Scope discipline — what was deliberately NOT corrected

`formal investigation` occurs 83 times across the corpus. The §12 gate is scoped to a
candidate-facing **MS Act 2025** claim, and that scoping did the work:

* **Past papers `QP2304`, `QP2307`, `QP2503`, `QP2507`, `QP2512` — NOT TOUCHED.** Every
  one of those sittings predates 15 March 2026. At those sittings the 1958 Act *was* the
  law and "formal investigation" *was* the correct answer. Writing the 2025 machinery into
  them would inject a present-day answer into a sitting-anchored paper, which is a defect,
  not a fix.
* **`oralnotes/miw-notes-mgmt-p15.html` — one row corrected, the rest left.** Its
  comparison table is headed *"Historical MS Act, 1958 Structure"* and its reporting chain
  *"Historical MS Act 1958 Framework"*; both are correct as written. Only its reg-box,
  which said *"now MS Act 2025 … governs statutory Preliminary Inquiries and Formal
  Investigations"* and called the change a *"2025 renumbering"*, was corrected. It is a
  restructure, not a renumbering.
* **`QB4_B#q789` (MV El Faro, 2015) — NOT TOUCHED.** A factual description of a US
  investigation, not an MS Act claim.
* **`oralnotes/miw-notes-mgmt-p16.html` — NOT TOUCHED**, per §10 of the brief. The RSV
  framework's *"pending confirmation of a re-notification"* is carried forward unresolved;
  it needs evidence of a DGMA re-notification, which is a different question from Act text.

## 5. Reported, not corrected — out of scope, needs a decision

* **`QB5_C_B#q5`, two further sites (L499, L515).** The card says *"I transition to the
  formal investigation phase under the **IMO Casualty Investigation Code**"* and heads a
  block *"Formal Investigation & Evidence Preservation Procedure"*. The Casualty
  Investigation Code does not use "formal investigation" either — it uses *marine safety
  investigation*. This is a **different proposition** (IMO Code, not MS Act 2025) and lies
  outside this authorisation. The card's MS Act limb *was* corrected. **Recommend a
  bounded follow-up.**
* **`QB5_B#q1` reg-box cites ISM §5** for the incoming CE's duty to review the SMS. ISM §5
  is the *Master's* responsibility and authority. The row's description names it correctly
  and draws an analogy rather than asserting a CE obligation, so it was left; the same
  hook appears on the cheat sheet's *Pre-arrival* row. **Recommend review.**
* **`meoclass1/index.html` still reads `Last Updated: 2 Sep 2026`.** This pass changed
  candidate-facing content on 4 September 2026. Per §15 the value is **reported, not
  patched**, because further GPT review is pending. The eventual release value must become
  **4 Sep 2026**.

## 6. The 1958 limitation, restated

The Merchant Shipping Act 1958 is **not held**. This pass therefore authored **no new
1958 section-number assertion**, and *removed* three unverifiable ones it found in rows it
was already rewriting — `QB1_I#q2` (*formerly 1958 Sec 24 / Sec 34*), `QB9_D#q6`
(*formerly 1958 Sec 76 & 87*), `QB5_B#q1` (*replaces the repealed 1958 Act, §77*) — and
`QB5_C_B#q5` (*erstwhile Section 358*). Each was replaced by the verified 2025 provision,
which is a weakening, not a new claim. `s.324` continuity language is preserved exactly
where relevant.

The `QB1_I` v1.2 correction line, which records the earlier re-basing and itself mentions
1958 Sec 24/34, was **not edited**; the new entry is appended in front of it.

---

## 7. Authorised implementation, as executed

### RED — `CORR-MSACT2B-CEHANDOVER-20260904`
`QB5_B#q1` (primary) and `QB5_B_CheatSheet.html`. The MS Act hook for CE handover is
removed. The defensible basis — company SMS, the company's own handover procedure, ISM
§6.3 familiarisation and §7 key-shipboard-operations procedures — is kept, and neither
document now claims any ISM clause prescribes a takeover certificate.

### GREEN — `CORR-MSACT2B-GREEN-20260904`
`QB9_H#q1` (primary), `QB9_H#q4`, `QB9_H#q8`, `QB1_I#q2`, `QB3_J#q5`. Twelve
pending-verification caveats closed against `s.319(1)`, `s.320`, `s.301`, `s.324`, `s.83`,
`s.62`, `s.12`, Part XIV `ss.281–292`, `s.15(1)`, `s.20(9)`, `s.18`, `s.131`, `s.133(1)`
and `s.138`.

### CASUALTY — `CORR-MSACT2B-CASUALTY-20260904`
`QB9_H#q2` (primary), `QB9_H#q11`, `QB5_C_B#q5`, plus `QB9_H_CheatSheet.html`,
`oralnotes/simon-notes-p6.html` and `oralnotes/miw-notes-mgmt-p15.html`. Stale *formal
investigation* terminology replaced with the current four-step structure: 24-hour notice
`s.231(2)` → preliminary inquiry `s.231(3)–(4)` → marine safety investigation
`s.231(5)–(6)` → administrative action or proceedings `s.232`, with certificate powers
placed separately at `s.312`.

### CoC — `CORR-MSACT2B-COC-20260904`
`QB9_D#q6` (primary). The multi-Part answer: grant `s.46(1)` and issuing-authority
withdrawal `s.48(6)-(7)` in Part IV, Central Government suspension `s.312` in Part XV,
described as three distinct powers rather than merged into one.

---

## 8. Governance note

The RED item is a separate record because its semantics are separate: it removes a
**false statutory hook**, where the GREEN batch **closes honest caveats** and the CASUALTY
record **replaces stale law**. Collapsing them would have produced exactly the vague
single manifest §11 of the brief forbids.

One schema constraint is worth recording. A correction manifest with **no cards** fails
three schema checks (`cards_present`, `action_ids_unique_and_present`,
`exactly_one_primary_correction`), which was confirmed by probe rather than assumed. The
RED item first presented as cheat-sheet-only. It was given a proper card not by inventing
one but by finding that `QB5_B#q1` — the card the cheat sheet summarises — carried the
same unverifiable *"replaces the repealed 1958 Act, §77"* equivalence. The pin therefore
rests on a real candidate-facing card, and the cheat sheet rides as an artefact, which is
how every previous cheat-sheet change in this repository has been governed.

No push, no deploy, no Excel distribution, no full release suite.
