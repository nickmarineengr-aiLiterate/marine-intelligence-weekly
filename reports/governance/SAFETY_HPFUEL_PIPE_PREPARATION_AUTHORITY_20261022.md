# Safety successor CORR-SAFETY-HPFUEL-PIPE-20261022 — preparation authority (NOT landing authority)

**Record governed:** `tools/oral/correction_corr_safety_hpfuel_pipe_20261022_manifest.json`.

## What was authorised

The Founder authorised, for the 22 Oct 2026 oral/Excel closeout, **controlled safety-release preparation** and
**bounded, independently reviewed successors** to the frozen P0S safety stack. The Founder did **not** authorise:

- production deployment or push;
- Excel distribution;
- any change to `founder_authorisation` metadata.

## Why this successor exists

The closeout found that `QB5_A#q11` also teaches, in its "On My Vessel" example, fitting a temporary clamp to a leaking
high-pressure fuel pipe and deferring the repair to port. An independent reviewer rated this S1. No existing
CORR-SAFETY record covers it: the 19 Oct records corrected the same card's enclosed-space entry criteria only.

## Scope

- One card section: the `QB5_A#q11` On My Vessel paragraph and its q-version footer. Stems, anchors and card counts
  are unchanged.
- `validate_correction_safety.py` gains a seventh unsafe proposition (`hp_fuel_pipe_no_clamp_repair`) and card checks;
  `mutate_correction_safety.py` gains mutations BA-BJ; `known_traps.md` gains entry 167.
- Base: `446e726`, the tip of frozen Transaction A. This successor is landed **after** Transaction A's authorisation
  commit, as its own transaction.

## What this file is and is not

This file is the `authorisation_source` of the record **for preparation and qualification only**. The record carries
`status: AUTHORISED`, the repository's pin-enforcement schema. Its `founder_authorisation` is
**`PENDING_FOUNDER_DECISION`**, and `check_founder_authorisation_for_landing.py` refuses landing (L3) until a separate
Founder authorisation commit sets it.
