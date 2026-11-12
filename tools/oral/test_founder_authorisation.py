#!/usr/bin/env python3
"""In-memory controls for the founder_authorisation contract (oral_manifest) and the landing gate's L4.

Each control states what MUST be judged well-formed / ill-formed / blocking. No file is read or written.
Prints "<N> checks, <M> FAIL".
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_manifest as M  # noqa: E402
from check_founder_authorisation_for_landing import open_cross_product_items  # noqa: E402

CARD = {"correction_action_id": "X-01"}
ART = {"correction_action_id": "X-CS-01"}
PEND = {"state": "PENDING_FOUNDER_DECISION", "prepared_under": "brief", "prepared_on": "2026-10-19"}
AUTH = {"state": "FOUNDER_AUTHORISED", "decided_on": "2026-10-20", "decided_by": "Founder",
        "decision_ref": "ref", "scope": ["X-01", "X-CS-01"]}


def verdict(m, legacy=False):
    return {c: ok for c, ok, _ in M.founder_authorisation_findings(m, legacy)}


CONTROLS = [
    ("A_new_record_without_field_fails_closed",
     lambda: verdict({"cards": [CARD]})["founder_authorisation_present_unless_legacy"] is False),
    ("B_legacy_record_without_field_unchanged",
     lambda: verdict({"cards": [CARD]}, legacy=True) == {"founder_authorisation_present_unless_legacy": True}),
    ("C_pending_well_formed",
     lambda: verdict({"cards": [CARD], "founder_authorisation": PEND})["founder_authorisation_well_formed"]),
    ("D_pending_missing_prepared_on_is_malformed",
     lambda: not verdict({"cards": [CARD], "founder_authorisation": {"state": "PENDING_FOUNDER_DECISION",
                                                                    "prepared_under": "x"}})["founder_authorisation_well_formed"]),
    ("E_unknown_state_is_malformed",
     lambda: not verdict({"cards": [CARD], "founder_authorisation": {"state": "AUTHORISED"}})["founder_authorisation_well_formed"]),
    ("F_authorised_with_exact_scope_incl_artefacts",
     lambda: verdict({"cards": [CARD], "governed_artefacts": [ART], "founder_authorisation": AUTH})["founder_authorisation_well_formed"]),
    ("G_authorised_scope_missing_an_artefact_is_malformed",
     lambda: not verdict({"cards": [CARD], "governed_artefacts": [ART],
                          "founder_authorisation": dict(AUTH, scope=["X-01"])})["founder_authorisation_well_formed"]),
    ("H_authorised_without_decision_ref_is_malformed",
     lambda: not verdict({"cards": [CARD], "governed_artefacts": [ART],
                          "founder_authorisation": {k: v for k, v in AUTH.items() if k != "decision_ref"}})["founder_authorisation_well_formed"]),
    ("I_pending_carrying_decided_fields_is_malformed",
     lambda: not verdict({"cards": [CARD], "founder_authorisation": dict(PEND, decided_by="x")})["founder_authorisation_well_formed"]),
    ("J_open_cross_product_item_blocks",
     lambda: open_cross_product_items({"propagation": {"cross_product_safety_items": [
         {"item_id": "XP-1", "product": "RulesApp", "status": "OPEN"}]}}) == ["XP-1 (RulesApp)"]),
    ("K_only_closed_verified_clears",
     lambda: open_cross_product_items({"propagation": {"cross_product_safety_items": [
         {"item_id": "XP-1", "product": "RulesApp", "status": "CLOSED_VERIFIED"}]}}) == []
     and open_cross_product_items({"propagation": {"cross_product_safety_items": [
         {"item_id": "XP-1", "product": "RulesApp", "status": "PROPOSED_FIX"}]}}) == ["XP-1 (RulesApp)"]),
    ("L_free_text_propagation_has_no_items",
     lambda: open_cross_product_items({"propagation": "prose only"}) == []),
    # ---- U-2 explicit three-record compatibility allowance (12 Nov 2026) ----
    ("M_allowance_is_exactly_the_three_lp617_records",
     lambda: sorted(M.FOUNDER_AUTHORISATION_LEGACY_COMPAT_RECORDS) == sorted([
         "correction_corr_lp617_sewage_sludge_20261028_manifest.json",
         "correction_corr_lp617_qb9a_q7_20261030_manifest.json",
         "correction_corr_lp617_simon_p8_20261030_manifest.json"])),
    ("N_allowlisted_name_with_released_blob_is_exempt",
     lambda: all(M.legacy_compat_allows(n, b) for n, b in M.FOUNDER_AUTHORISATION_LEGACY_COMPAT_RECORDS.items())),
    ("O_allowlisted_name_with_edited_content_is_not_exempt",
     lambda: not any(M.legacy_compat_allows(n, "0" * 40) for n in M.FOUNDER_AUTHORISATION_LEGACY_COMPAT_RECORDS)
     and not M.legacy_compat_allows("correction_corr_lp617_sewage_sludge_20261028_manifest.json", None)),
    ("P_future_or_renamed_record_cannot_inherit",
     lambda: not M.legacy_compat_allows("correction_corr_lp617_sewage_sludge_20261112_manifest.json",
                                        "89bd478484ad29625d5f2280de61e3409d1f5506")
     and not M.legacy_compat_allows("correction_corr_future_20261201_manifest.json",
                                    "89bd478484ad29625d5f2280de61e3409d1f5506")),
    ("Q_no_safety_record_in_allowance",
     lambda: not any("safety" in n for n in M.FOUNDER_AUTHORISATION_LEGACY_COMPAT_RECORDS)),
    ("R_legacy_commit_is_the_p0_baseline",
     lambda: M.FOUNDER_AUTHORISATION_LEGACY_COMMIT == "e016b2549182812b50f16d8e6e1512b3b32bfb2d"),
]


def main() -> int:
    fails = 0
    for name, fn in CONTROLS:
        try:
            ok = bool(fn())
        except Exception as e:  # a crash is a FAIL, never a skip
            ok, name = False, "%s (crash: %s)" % (name, e)
        fails += 0 if ok else 1
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
    print("%d checks, %d FAIL" % (len(CONTROLS), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
