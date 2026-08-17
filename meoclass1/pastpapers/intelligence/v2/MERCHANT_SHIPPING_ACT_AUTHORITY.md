# Merchant Shipping Act, 2025 — primary authority

**RESEARCH ONLY. NOT CANDIDATE-FACING.** `current_as_of: 2026-08-18`

Laptop declined to certify the commencement and repeal because it had not read the
Gazette. This pins it. Every fact below is read from the Gazette of India itself,
retrieved from the Ministry's own domain — not from MIW True Source, not from a
law-firm note, not from an encyclopaedia.

**Status: `PRIMARY_AUTHORITY_PINNED`.**

---

## 1. The artefacts

| | |
|---|---|
| Document | Gazette of India, Extraordinary — the Act and the commencement notification, published together |
| Host | `shipmin.gov.in` — Ministry of Ports, Shipping and Waterways, Government of India |
| URL | `https://shipmin.gov.in/sites/default/files/MS%20Act%202025_merged.pdf` |
| Retrieved | 18 August 2026, direct from the Ministry (no archive intermediary) |
| Artefact | `%PDF-1.6`, 2,576,336 bytes |
| sha256 | `B5C096DC141EF63E4789663FA3308F6668B44DC7646CFBEA3F31BFB797CEC7A4` |

Two secondary routes were tried first and both failed, which is worth recording so
the next session does not repeat them: `indiacode.nic.in` answers `302` to a direct
PDF request and `403` to WebFetch, and `dgshipping.gov.in` remains unreachable
(`Unable to connect`), consistent with the ECONNREFUSED state seen in both earlier
phases.

The Merchant Shipping Act, 1958 was read separately, from the India Code text via
the Wayback raw `id_` variant, because the identification of what survives repeal
cannot be taken from commentary. See §4.

---

## 2. Commencement — verbatim

> S.O. 1244(E).— In exercise of the powers conferred by sub-section (2) of section 1
> of the Merchant Shipping Act, 2025 (24 of 2025), the Central Government hereby
> appoints the 15th day of March, 2026 as the date on which the provisions of said
> Act shall come into force.

| Field | Value |
|---|---|
| Notification | **S.O. 1244(E)** |
| Notification date | **10 March 2026**, New Delhi |
| Gazette part | Extraordinary, **Part II — Section 3 — Sub-section (ii)**, No. 1192 |
| Gazette id | `CG-DL-E-11032026-270832` |
| Ministry | Ports, Shipping and Waterways |
| File number | F. No. SR-20020/5/2020-ML |
| Signatory | Rajesh Kumar Sinha, Special Secretary |
| **Commencement date** | **15 March 2026** |

The Act itself: **Merchant Shipping Act, 2025, No. 24 of 2025**, Presidential assent
**18 August 2025**, published Gazette Extraordinary Part II — Section 1, No. 29,
`CG-DL-E-19082025-265484`.

**The reported date and notification are confirmed.** 15 March 2026 and S.O. 1244(E)
are both correct as MIW recorded them.

---

## 3. Repeal — verbatim

Section 324(1):

> The Merchant Shipping Act, 1958 (except Part XIV but not including section 411A
> therein) and the Coasting Vessels Act, 1838 is hereby repealed.

Section 324(2) then saves, notwithstanding the repeal, rules and notifications made
under the repealed enactments until revoked; offices and appointments; documents
referring to a repealed enactment, which are construed as referring to the 2025 Act;
fines and offences; vessel registrations; recorded mortgages; and — the limb that
matters most to a marine engineer — **certificates**:

> any licence, certificate of competency or service, certificate of survey, A or B
> certificate, safety certificate, … issued … under any enactment hereby repealed and
> in force at the commencement of this Act, shall be deemed to have been issued …
> under this Act and shall, unless cancelled under this Act, continue in force until
> the date shown in the certificate or document

Section 324(3) preserves the general application of section 6 of the General Clauses
Act, 1897.

---

## 4. What actually survives — and the correction it forces

"Except Part XIV" is meaningless until you know what Part XIV of the **1958** Act is,
and this is where secondary sources are actively misleading. A web search returned
the confident claim that the surviving Part is wreck and salvage. **It is not.**
Read from the 1958 Act's own arrangement of sections:

| 1958 Act | Subject | Status from 15 March 2026 |
|---|---|---|
| Part XII, ss. 357–389 | Investigations and Inquiries | **repealed** |
| Part XIII, ss. 390–404 | **Wreck and Salvage** | **repealed** |
| **Part XIV, ss. 405–414** | **Control of Indian Ships and Ships Engaged in Coasting Trade** | **in force**, except s. 411A |
| Part XV–XVIII | Sailing vessels, penalties, miscellaneous, repeals | **repealed** |

Part XIV is the licensing regime: s.406 Indian ships and chartered ships to be
licensed, s.407 licensing for coasting trade, s.408 revocation, s.409 surrender,
s.410 no port clearance until licence produced, s.411 power to give directions,
s.413 Director-General's power to call for information, s.414 rule-making.
(s.412 was already repealed; s.404 of Part XIII carried the wreck and salvage
rule-making power under which the Merchant Shipping (Wrecks and Salvage) Rules,
1974 were made.)

Section **411A** — the Central Government's power to protect Indian shipping from
undue foreign intervention — is carved *out* of the survival and is repealed,
because the 2025 Act re-enacts that power itself immediately before s.324.

> **Do not write that "the 1958 Act was repealed" without qualification, and do not
> repeat the claim that wreck and salvage survives.** The 1958 Act survives only as
> its coasting-trade licensing Part.

---

## 5. Temporal delta for FAMILY-EM-0008

The family asks, across five sittings from March 2023 to July 2025: after a casualty
to an Indian flag vessel off the coast of India, what steps must be initiated under
the Merchant Shipping Act, and who must initiate them.

All five sittings predate 15 March 2026. All five were answered under the 1958 Act.
The casualty-reporting and inquiry machinery those answers rest on is **Part XII of
the 1958 Act, which is repealed**.

**OLD REFERENCE** — the 1958 Act's Part XII: s.358 shipping casualties and report
thereof, s.359 power to hold a preliminary inquiry, s.361 formal investigation,
and the marine board machinery; with wreck and abandonment under Part XIII for the
QP2402 grounding variant.

**CURRENT POSITION** — from 15 March 2026 the governing statute is the Merchant
Shipping Act, 2025 (24 of 2025). The 1958 Act survives only as Part XIV
(coasting-trade licensing), which is not what this question asks about.

**DO NOT WRITE TODAY** — a bare citation of "section 358 of the Merchant Shipping
Act, 1958" or "the Merchant Shipping Act, 1958, as amended" as the current source of
the casualty-reporting duty; any statement that the marine board is constituted
under the 1958 Act; any answer to the QP2402 abandonment limb resting on Part XIII.

**STATE TODAY** — the duty arises under the Merchant Shipping Act, 2025, in force
15 March 2026 by S.O. 1244(E). Where a candidate cites the historical position, it
must be dated: "under the 1958 Act, which governed until 15 March 2026".

**ANSWER IMPACT: MAJOR** *(internal field — see `TEMPORAL_DELTA_SCHEMA.json`)*.
The structure of the answer survives; the statutory authority under it does not.

**The specific section mapping from the 1958 Part XII duties into the 2025 Act has
NOT been done and is not asserted here.** Doing it needs a section-by-section read
of the 2025 Act's casualty and inquiry Part, and that is Phase 3B work. Until it is
done this family must not advance toward candidate use, however well its
commencement date is pinned.

---

## 6. What this does not do

Pinning commencement changes **CLAIM 3** (current answer temporal change) only.
It says nothing about **CLAIM 1** (official bank ancestry — BANK-039, undated) and
nothing about **CLAIM 2** (dated exam occurrence — the five MIW-held sittings).
The three remain orthogonal, and the Gazette is authority for the third alone.

No candidate-facing text is produced from this document.
