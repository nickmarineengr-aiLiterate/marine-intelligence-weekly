# P0 safety corrections — preparation authority (NOT landing authority)

**Records governed:** every `tools/oral/correction_corr_safety_*_20261019_manifest.json`.

## What was authorised

The Founder decision for task **MIW-P0-SAFETY-FINAL-QUALIFICATION** (19 Oct 2026, DANI-DESKTOP, Claude Code CLI) gave:

- **GO** for local completion of the safety corrections and for their full qualification;
- **NO** production GO;
- **NO** permission to deploy, push, distribute, or bypass correction authorisation.

It followed the preparation task **MIW-QB-P0-SAFETY-CORRECTION-PREPARATION**, which:

- prepared and independently qualified the five S1 corrections on candidate 05645a1;
- tagged that candidate `frozen/p0-safety-qualified-20261019`;
- had its scope extended on 19 Oct 2026 to four further cards that stated the same enclosed-space entry error (QB1_F#q8, QB3_B#q1, QB3_B#q3, QB3_G#q4).

## Disclosed within this candidate (Founder review required)

- **Whole-card scope.** The cards were re-certified by independent whole-card review. Errors that review demonstrated on the same cards are corrected under the same records:
  - QB1_F#q8: bottom inspections (A.1207(34) 4.6), the UR Z10.2 close-up scope and age bands, wastage repair (UR Z7 1.3);
  - QB3_B#q3: coating grades (UR Z7 1.2.10, 2.2.7);
  - plus smaller items, listed per card in the P0S pack, `03_review`.
- **One historical validator changed.** In `validate_batch_e1.py`, `timed_blocks_unchanged` now checks E1's own produced state, recovered from history by its pinned digest, once a later authorised record supersedes the card. It fails if that state cannot be found.
  - Why: the qualified P0 candidate 05645a1 failed this registered gate, which production passes, because the authorised EEBD correction to QB1_F#q1's 60-second answer was read as E1's defect.
  - Precedent: the same file already applies this contract to its additive check (CORR-T5-DDCASCADE).
  - Controls: `test_e1_timed_supersession.py`, registered as gate `e1_timed_supersession_controls`.
- **Unchanged and still failing:** `validate_correction_d01s02` (not a release gate) hard-pins digests. Production already fails it on two cards. The successor adds QB1_F#q8, which it supersedes through a governed chain.

## What this file is and is not

This file is the `authorisation_source` for the CORR-SAFETY-* records **for preparation and qualification only**.

Each record carries `status: AUTHORISED`. That is the repository's pin-enforcement schema: it means "these digests are enforced". It does **not** record a Founder decision.

The Founder decision lives in each record's `founder_authorisation` field. That field is **`PENDING_FOUNDER_DECISION`** in every CORR-SAFETY record.

`tools/oral/check_founder_authorisation_for_landing.py` refuses landing while any record is pending (L3). It also refuses landing while any record declares an open cross-product safety item (L4): the RulesApp lifeboat-falls statement, XP-RULESAPP-FALLS-01.

## How landing is authorised (not done here)

Landing requires a new commit that sets each record's `founder_authorisation` to:

```json
{"state": "FOUNDER_AUTHORISED", "decided_on": "...", "decided_by": "...", "decision_ref": "...", "scope": [<every action id of that record>]}
```

It also requires the RulesApp item to be closed as `CLOSED_VERIFIED` by that product's owner. Both are recorded in the successor pack: `P0S_SAFETY_SUCCESSOR_20261019/08_AUTHORISATION_TRANSACTION.md` (job root, outside this repository).
