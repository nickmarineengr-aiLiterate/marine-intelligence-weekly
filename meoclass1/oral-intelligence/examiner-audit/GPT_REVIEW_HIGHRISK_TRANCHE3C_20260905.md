# GPT HIGH-RISK CONTENT REVIEW — TRANCHE 3C AUTHORISATION RECORD

**Date:** 5 September 2026
**Baseline:** `faebcd4` on `main`, tree clean, 20 ahead of `origin/main` (`9e26f02`)
**Corpus at baseline:** 761 canonical questions across 86 question-bearing files
**Scope:** close the five adjudicated Tranche-3 P1 findings, and only the source-custody
gaps needed to make those corrections reproducible. **No Tranche 4.**

---

## Authorised findings

| id | Card | Finding | Authorisation |
|----|------|---------|---------------|
| **F-1** | `QB6#q1` | An unsupported vessel-specific claim — a `MAN B&W 11G90ME-C` main engine at `~35,000 kW MCR` on a *Maersk TRIPLE-E* — presented as the candidate's own vessel. | **DELETE.** Do **not** substitute another Triple-E engine specification: replacing one vessel-specific claim with another risks a second over-generalisation, and the card does not need a vessel-class propulsion example to explain CII. |
| **F-2** | `QB6#q1` | The card teaches an unqualified `gCO₂/DWT·nm` in eight layers, with only one body occurrence carrying a qualifier. DWT is **not** the universal CII capacity measure. | **CORRECT THE CARD AS A WHOLE**, to `gCO₂ per capacity-nautical-mile`, with the ship-type split explained. Accurate first in the short layer; detail in the body; no taxonomy lecture in the 15-second answer. |
| **F-3** | `QB7_I#q10` | The card's body and trap correctly say `capacity × distance`; its 15-second answer says `per DWT-mile`. | **CORRECT THE SHORT LAYER ONLY.** Do not rewrite the card. |
| **F-4** | `QB3_F#q3` ×5, `QB3_F#q11` ×2 | Seven candidate-facing positive teaching occurrences of `1/30,000` as a universal, and **zero** occurrences of `1/15,000` corpus-wide. MARPOL Annex I reg. 34.1.5 has two limbs. | **CORRECT ALL SEVEN AS ONE COHERENT PROPAGATION.** Where a short layer cannot carry the full sentence, a compact split is permitted provided the 31 December 1979 boundary stays exact. Do not alter other reg. 34 criteria. |
| **F-5** | `QB2_A#q31` | An "On My Vessel" block asserting a personal fine-ore / concentrate pre-loading routine with no Founder-grounded evidence. | **GENERICISE OR REMOVE.** Keep the technical/casualty content. |

## Also authorised, tied to cards already being edited

* **`QB2_A#q31` source-confidence block.** The only reviewed card carrying none. Add one in the
  house pattern. No decorative claims; never say a source was read unless it was.
* **Recent named casualty governance ruling.** A candidate-facing card publishing a recent named
  casualty with detailed factual claims must have a registered supporting source before release.
  Applied **only** to the casualty already identified in `QB2_A#q31`. Verify every published fact
  individually; remove or qualify anything that cannot be verified. **No corpus-wide casualty audit.**
* **IACS Z-series custody, bounded.** Acquire and register **UR Z7, UR Z18 and UR Z20** — the
  instruments Tranche 3 directly observed. **Not** every IACS Unified Requirement.
* **UR Z20 content verification.** The affected card cites Z20 to sub-paragraph level; verify every
  cited paragraph against the held current revision. Correct only a mismatched proposition.
* **UR Z7 / Z18.** Verify only the propositions the corpus already relies on. Mismatch ⇒ stop and report.
* **MS Notice 9 currentness.** Informational/P2. Check the issuer if it can be done without
  acquisition; record verification only. **Do not create a correction to move a date by four days.**

## Standing rule adopted this pass

**A ship specification or fleet fact may be factually true and still be inappropriate in
"On My Vessel" if it is presented as the candidate's own experience without grounding.**
Source proof does not rescue a provenance failure. Delete or genericise unsupported personal
and fleet claims; do **not** replace them with sourced trivia. This is a content-provenance
rule, not an accuracy rule.

## Governance

Four coherent families, kept as separate records — **not** one giant manifest:

| Family | Record |
|---|---|
| A — CII corrections and currentness | `CORR-GPT-T3C-CII-20260905` |
| B — MARPOL Annex I reg. 34 propagation | `CORR-GPT-T3C-REG34-20260905` |
| C — `QB2_A#q31` provenance, casualty, source confidence | `CORR-GPT-T3C-Q31-20260905` |
| D — IACS source-custody repair | `CORR-GPT-T3C-IACS-20260905` |

Predecessor ancestry preserved through declared supersession chains. No rebaselining.

## Explicitly out of scope

No Tranche 4. No filling of the 17 empty 15-second answers. No normalisation of the 10 no-layer
cards. No release-gate registration. No commit-graph repair. No full release suite. No push,
no deploy, no Excel distribution. Hub date stays at 2 Sep 2026.

Source-custody gaps other than those named above are **carried forward for later adjudication**,
not closed.
