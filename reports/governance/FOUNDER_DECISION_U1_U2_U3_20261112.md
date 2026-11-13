# Founder decision FOUNDER-DECISION-U1-U2-U3-20261112

- **Date:** 12 November 2026.
- **Release:** S1-SAFETY-REMEDIATION-20261112, the MIW S1 safety remediation.
- **Candidate under review:** `aea3531f877f076f22da43e5daf1e90ffa2bc969`, tree `3411caa2cfde072e59943b96cc9611fe883786f5`.
- **Production baseline:** `ad7cd3db8c802891b13585163743df340837d291`.

This record states what the Founder decided and what each part authorises. It does **not** authorise a production push.

## Four separate authorisations

| Layer | Status | Where it is recorded |
|---|---|---|
| 1. Content correction authorisation | **Authorised for local integration and qualification.** Covers the nine CORR-SAFETY-* records, within their documented action IDs (decision §6). | Each record's `founder_authorisation` (`FOUNDER_AUTHORISED`, `decision_ref` = this record) |
| 2. Governance-exception authorisation | **Authorised, narrowly** (U-1 CONDITIONAL GO): `GX-S1-RULESAPP-FALLS-20261112` | `tools/oral/governance_exception_gx_s1_rulesapp_falls_20261112.json`, SHA-pinned in `governance_exceptions.KNOWN_EXCEPTIONS` |
| 3. Release qualification | **Not a Founder decision.** It is the evidence returned for review. | Release evidence outside the repository (`evidence/s1-safety-remediation-20261112/`) |
| 4. Final production push approval | **NOT GIVEN.** A separate Founder decision is needed, naming the exact final commit and tree. | — |

## U-1: XP-RULESAPP-FALLS-01

**Justification.** The affected RulesApp content is excluded from the MIW production deployment (`.vercelignore`, rule `RulesApp/`), while the corresponding MIW subscriber-facing safety errors are live.

**Scope:**
- the product Marine Intelligence Weekly;
- this release and its qualified successor only;
- one item, `XP-RULESAPP-FALLS-01` (RulesApp, status OPEN);
- one record, `CORR-SAFETY-LSA-FALLS-COLDSTART-20261019`.

**Safeguards.** The exception record lists them, and the landing gate enforces them (X1–X9 in `governance_exceptions.py`):
- RulesApp is not changed.
- The item is not closed or verified.
- The RulesApp owner obligation is preserved.
- The deployment exclusion is not changed.
- No general bypass is created.
- A stable identifier and a SHA pin are used.
- The exception is linked to the record and release.
- Fresh live non-deployment evidence for the exact tree is required at qualification and immediately before any push.

If RulesApp becomes deployed, the exception does not apply.

**Expiry.** `expires_on` is 2026-12-12. This was chosen at implementation as a conservative limit and is disclosed to the Founder.

## U-2: legacy compatibility

The Founder accepted it, preferring an explicit allowance. `oral_manifest.FOUNDER_AUTHORISATION_LEGACY_COMPAT_RECORDS` exempts exactly three records, each by filename **and** by the git blob released at `ad7cd3d`:
- CORR-LP617-SEWAGE-SLUDGE-20261028;
- CORR-LP617-QB9A-Q7-20261030;
- CORR-LP617-SIMON-P8-20261030.

The legacy commit stays `e016b25`. No retrospective `founder_authorisation` is written into those records: their released provenance (status AUTHORISED, `authorisation_source` `meoclass1/known_traps.md`) is unchanged.

## U-3: scope extension

**Confirmed.** The 19 Oct enclosed-space propagation is retained. That covers QB1_F#q8, QB3_B#q1, QB3_B#q3, QB3_G#q4, QB5_A#q10, QB5_B#q15 and both cheat sheets, including:
- the MSC.581(110) 7.4 entry criteria;
- the separation of shipboard enclosed-space requirements from the ship-recycling criteria in MEPC.210(63).
