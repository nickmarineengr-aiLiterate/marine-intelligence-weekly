#!/usr/bin/env python3
"""
Mutation suite for CORR-MSACT-SEA-20260902  (QB9_H#q10).

`validate_correction_msactsea.py` reports 19 green checks. Green output alone
is indistinguishable from a validator that reads nothing, so every proposition
is attacked here and each mutation must trip the check that OWNS it -- never
the digest pin, which fires on any byte change at all
(enforced by oral_content_mutation.DIGEST_PINS).

MUTATION C IS THE ONE THIS GUARD EXISTS FOR.
It adds a single plausible-looking neighbour section, `s.65`, to a list of
otherwise-correct citations. Nothing about the card LOOKS wrong afterwards --
which is exactly why the section set is asserted as a CLOSED set derived from
what was actually read out of the Gazette text, rather than as a set of
presence checks that a plausible addition would sail straight through.

MUTATION H is its mirror. It removes the "do not carry 1958 numbering across"
warning while leaving the 1958 mentions in place, turning a card that teaches
the supersession into one that merely cites a repealed Act.
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import run_suite, sub_in_file   # noqa: E402

CARD = REPO / "meoclass1/QB9_H.html"
MANIFEST = HERE / "correction_corr_msact_sea_20260902_manifest.json"
PROBE = "validate_correction_msactsea.py"

MUTATIONS = [
    ("A", "reinstate the author-facing [cite ...] placeholder",
     sub_in_file(CARD,
                 "aligned to MLC. In the <strong>Merchant Shipping Act 2025"
                 "</strong>",
                 "aligned to MLC since ratification <em>[cite the 2025 Act at "
                 "Part level; the 1958 sections must not be quoted as current]"
                 "</em>. In the <strong>Merchant Shipping Act 2025</strong>"),
     "no_cite_placeholder"),

    ("B", "reinstate a 'sections pending verification' hedge",
     sub_in_file(CARD,
                 "<strong>s.63</strong>, the seafarers&rsquo; employment "
                 "agreement in the prescribed form",
                 "<strong>s.63</strong> [Part-level, sections pending "
                 "verification], the seafarers&rsquo; employment agreement in "
                 "the prescribed form"),
     "no_pending_verification"),

    ("C", "add ONE plausible but unverified neighbouring section",
     sub_in_file(CARD,
                 "and <strong>s.83(1)</strong> sends a dispute arising under "
                 "the agreement to the shipping master.",
                 "and <strong>s.83(1)</strong> sends a dispute arising under "
                 "the agreement to the shipping master; s.65 governs the "
                 "seafarer&rsquo;s right to repatriation."),
     "no_unverified_ms_act_sections"),

    ("D", "remove the s.63 agreement obligation",
     # The card spells this several ways ("seafarers' employment agreement",
     # "Seafarer's Employment Agreement"); the proposition only dies when all
     # of them do, which is why the shared stem is the target.
     sub_in_file(CARD, "mployment agreement", "rew engagement paperwork"),
     "s63_agreement_with_seafarers"),

    ("E", "remove the s.63(3) examine-and-seek-advice right",
     sub_in_file(CARD, "examine and seek advice", "review at leisure"),
     "s63_3_examine_and_seek_advice"),

    ("F", "remove the s.64 monthly account",
     sub_in_file(CARD, "monthly account", "periodic statement"),
     "s64_monthly_account"),

    ("G", "remove the s.83(1) dispute route",
     sub_in_file(CARD, "s.83(1)", "the Act"),
     "s83_disputes_to_shipping_master"),

    ("H", "drop the 1958 warning while leaving the 1958 mentions",
     sub_in_file(CARD, "Do not carry 1958 numbering across.", ""),
     "no_1958_numbering_as_current"),

    ("I", "remove the MLC Std A2.1 core",
     sub_in_file(CARD, "Std A2.1", "the Convention"),
     "mlc_a2_1_core_preserved"),

    ("J", "remove the Std A2.2 wage accounts",
     sub_in_file(CARD, "Std A2.2", "the wages provisions"),
     "mlc_a2_2_wage_accounts_preserved"),

    ("K", "remove the classical articles layer",
     # The check accepts either name for the classical instrument, so removing
     # only one leaves the proposition standing.
     lambda: [sub_in_file(CARD, "Articles of Agreement", "crew paperwork")(),
              sub_in_file(CARD, "ship's articles", "crew paperwork")()],
     "classical_articles_layer_preserved"),
]

WATCHED = [CARD, MANIFEST]

if __name__ == "__main__":
    raise SystemExit(run_suite(
        "mutation suite: CORR-MSACT-SEA-20260902 (QB9_H#q10)",
        PROBE, MUTATIONS, WATCHED))
