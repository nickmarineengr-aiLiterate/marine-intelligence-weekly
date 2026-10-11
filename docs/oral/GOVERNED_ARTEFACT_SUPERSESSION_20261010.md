# Governed artefact supersession — implementation record (10 Oct 2026)

**Status:** local tooling candidate. Not pushed, not deployed. Authorised by the
Lane A dispatch *MIW / Lane A — Governed Artefact Supersession Tooling* of
10 October 2026. Implements the design in
`GOVERNED_ARTEFACT_SUPERSESSION_CONTRACT_DESIGN_20261010.md` (H-1 Phase 2
review package, sha256 `fbd36965…3f07`).

## 1. The defect

`QB2_B_CheatSheet.html` is pinned whole-file by
`CORR-REL-BJ-CHEATSHEET-20260909` / `REL-BJ-CS-01` at
`64f04f3c50f47fd63be77634d88f4039cbe81ed7afd77f8199c0353aa04d1152`.
A later, valid correction (H-1 Phase 2, SQ-1/SQ-2 dependants of `QB2_B#q10`)
changes the file. Before this change the gate had no way to express "this later
state descends from that one". It could only fail
`live_matches_authorised_artefact_state`, or the historical record could be
edited. Editing it is forbidden.

## 2. Decision

A new load-bearing correction-record field, `governed_artefact_successions`.
The **later** record declares descent. The historical record is never written.
This mirrors the card contract in `oral_supersession.py`.

```json
"governed_artefact_successions": [{
  "succession_action_id": "<id unique in this record>",
  "path": "meoclass1/QB2_B_CheatSheet.html",
  "artefact_type": "CHEAT_SHEET",
  "pre_edit_digest":  "<artefact_digest at this record's baseline_commit>",
  "post_edit_digest": "<artefact_digest at this record's last governing commit>",
  "supersedes": {
    "manifest": "<predecessor record filename>",
    "action_id": "<predecessor correction_action_id or succession_action_id>",
    "post_edit_digest": "<the predecessor's pinned post digest, verbatim>"
  },
  "preserved_propositions": ["<every proposition the predecessor governs, verbatim>"],
  "succession_reason": "<why>"
}]
```

The key set is **closed** at both levels. An unknown key fails as `UNKNOWN_FIELD`.

### Why a separate field

- **Not inside `governed_artefacts`.** That form requires a parent proposition
  (`governing_correction`) and forbids a record from naming itself. A
  succession is a first-instance edit with no parent proposition.
- **Not `status: SUPERSEDED`.** Setting it would mean editing the historical
  record, and it would stop enforcing that record's pins.

### Why `succession_action_id`

It is an addition to the design sketch. Without it, a succession has no
identity that a *further* successor can name, so a two-link chain could not be
expressed.

## 3. Resolution

The resolver is `oral_supersession.resolve_authorised_artefact_state`. The card
resolver is unchanged and is not reused.

| | |
|---|---|
| **Dormant** | No succession names the path anywhere, so the check is `pin == live`, byte-for-byte the old comparison and detail text. Every record on main is this case. |
| **Declared** | The chain is built and keyed `(manifest, pre, post)`, with action ids as members. Each link must pass:<br>• exact predecessor identity (manifest and action id exist, else `MISSING_ANCESTOR`)<br>• the claim's pin equals the predecessor's stored pin (else `MISSING_ANCESTOR`)<br>• same path (`PATH_MISMATCH`) and same type (`TYPE_MISMATCH`)<br>• 64-hex `artefact_digest` only (`DIGEST_CONVENTION_MISMATCH`), with no prefix tolerance<br>• both records `AUTHORISED` (`UNAUTHORISED_LINK`)<br>• `successor.pre == predecessor.post` (`CHAIN_BREAK`)<br>• no fork, including a duplicate successor with the same post (`CHAIN_FORK`)<br>• no cycle or self-succession (`CHAIN_CYCLE`)<br>• one root and one terminal |
| **History** | `verify_artefact_chain_history`: every link is proved against git. A chain is never accepted on JSON alone (`HISTORY_UNVERIFIED`). |
| **Terminal** | The terminal post digest must equal live, else `TERMINAL_NOT_LIVE`. An unregistered edit after the terminal therefore fails. |

`verify_artefact_chain_history` checks, for every link:

- the root's governing commit holds the root pin;
- the successor's baseline commit holds its `pre_edit_digest`;
- its last governing commit holds its `post_edit_digest`;
- the predecessor's governing commit is an ancestor of the successor's baseline;
- the baseline is an ancestor of the governing commit;
- `preserved_propositions` contains everything the predecessor governs, transitively;
- every preserved proposition is present at the governing commit.

## 4. Checks emitted

**Schema** (`audit_correction_manifest` 5e). These run only when the key is
present:

- `governed_artefact_successions_non_empty`
- `succession_fields_known`
- `succession_identity_complete`
- `succession_ids_unique_and_present`
- `succession_type_governed`
- `succession_digest_convention`
- `succession_digests_differ`
- `succession_path_exists`
- `succession_does_not_supersede_own_record`
- `succession_record_is_authorised`

**Live** (`audit_governed_artefacts_live`). This function is shared by
`validate_corrections.py` §8 and `validate_artefact_governance.py`.

- The predecessor keeps `live_matches_authorised_artefact_state`. When a chain
  resolves, its detail adds `authorised_ancestor_of_live=[…]`.
- The successor gets five new checks:
  - `succession_pre_matches_baseline`
  - `succession_post_produced_by_governing_commit`
  - `succession_target_is_governed`
  - `succession_preserves_predecessor_propositions`
  - `succession_live_or_descended`

## 5. What did not change

- `CORRECTION_STATUSES`
- `GOVERNED_ARTEFACT_CLASSES`
- `GOVERNED_ARTEFACT_FIELDS`
- every governed-artefact check name and its dormant detail text
- the card supersession resolver
- `live_matches_authorised_artefact_state`, which is still enforced. There is
  no allowlist and no H-1 exception.

## 6. Tests

- `tools/oral/test_governed_artefact_supersession.py` runs in memory and
  covers:
  - chain algebra and history doubles: GS-1…GS-12 and history negatives;
  - positive controls: dormant, single link, two links, ancestor resolution,
    exact terminal;
  - dormancy over the real corpus.
- `tools/oral/mutate_governed_artefact_supersession.py` has two layers:
  - **Hermetic layer:** a throwaway git repository with real commits. Each
    mutation must turn its owning check red *with the intended reason token*.
  - **`--live` layer:** attacks whatever succession is declared on disk,
    through `validate_artefact_governance.py`, with byte-exact restore. With
    none on disk it exits 2 and does not claim a pass.

Neither suite is registered in `oral_release_gates.py`. That is a Lane A
decision.

## 7. Applying it to H-1

Add one entry to the H-1 record. Do not touch `CORR-REL-BJ-CHEATSHEET-20260909`.

```json
"governed_artefact_successions": [{
  "succession_action_id": "H1SOLAS-P2-CS-01",
  "path": "meoclass1/QB2_B_CheatSheet.html",
  "artefact_type": "CHEAT_SHEET",
  "pre_edit_digest":  "64f04f3c50f47fd63be77634d88f4039cbe81ed7afd77f8199c0353aa04d1152",
  "post_edit_digest": "0688c2ac3e2501ad0fbf41730999bdcae313f459e7316d4b3bdbb44f9faeba6d",
  "supersedes": {
    "manifest": "correction_corr_rel_bj_cheatsheet_20260909_manifest.json",
    "action_id": "REL-BJ-CS-01",
    "post_edit_digest": "64f04f3c50f47fd63be77634d88f4039cbe81ed7afd77f8199c0353aa04d1152"
  },
  "preserved_propositions": [
    "<li>Casualties: <em>MV Bulk Jupiter (2015)</em> — bauxite; most probably liquefaction or a free-surface effect (flag State found no physical evidence of cause)</li>"
  ],
  "succession_reason": "H-1 Phase 2 SQ-1/SQ-2 dependants of QB2_B#q10 …"
}]
```

The values come from the record itself:

- `pre` = the file at H-1 `baseline_commit` `d8b48e8`;
- `post` = the file at H-1's last governing commit `5f58bfe`, which is also the
  live file at `516f1f3`.
