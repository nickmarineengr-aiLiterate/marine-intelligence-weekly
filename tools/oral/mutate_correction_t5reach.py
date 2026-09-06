#!/usr/bin/env python3
"""Mutation suite for CORR-T5-REACH-20260906.

Every mutation must trip the check that OWNS its proposition, never a digest
pin - and for three of the eight sites there is no pin at all, because a cheat
sheet carries no q-card. Mutations B, C, D and E attack exactly those surfaces,
and if they escaped, half this correction would be shipping unguarded.

THE TWO DIRECTIONS THIS SUITE HAS TO TEST
-----------------------------------------
A correction to a superseded label is not "remove every occurrence". Ninety-four
of the corpus's 102 occurrences are legitimate - the examiner's own wording, a
TOC echo, a currentness note quoting BMP5 in order to deny it, and QB4_H#q11
which is retained on purpose as the predecessor record.

So the suite attacks BOTH failure modes:

  * REGRESSION (A, B, D, F, G, H) - a corrected surface goes back to teaching
    the superseded publication as current;
  * OVER-SWEEP (I, J, K) - a future session runs a flat banned-phrase sweep and
    deletes the examiner's own question wording, or corrects away the
    predecessor card that exists to answer "what was BMP5?".

The second direction is the one nobody writes a check for, and it is the one
that destroys evidence rather than merely leaving it stale.

MUTATION C IS THE N-2 TRAP
--------------------------
It replaces the removed MSC.1/Circ.1606 pills with a plausible-looking security
circular. That is precisely what the instruction forbade - "do not replace with
a guessed security circular" - and it is the shape a well-meaning later editor
reaches for when a row looks empty. A check that only asserted 1606 was absent
would pass it.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    edit_json, run_suite, sub_in_file)

MANIFEST = HERE / "correction_corr_t5_reach_20260906_manifest.json"
QB4_H = REPO / "meoclass1/QB4_H.html"
QB1_F = REPO / "meoclass1/QB1_F.html"
QB5_B = REPO / "meoclass1/QB5_B.html"
QB9_A = REPO / "meoclass1/QB9_A.html"
CS9A = REPO / "meoclass1/QB9_A_CheatSheet.html"
CS5B = REPO / "meoclass1/QB5_B_CheatSheet.html"
CS4H = REPO / "meoclass1/QB4_H_cheatsheet.html"
TRAPS = REPO / "meoclass1/known_traps.md"
PROBE = "validate_correction_t5reach.py"

FOOTER_NOW = ('JMIC advisory updates, the held <strong>BMP Maritime Security, '
              '1st Edition (2025) as updated June 2026</strong> (safe muster '
              'point vs. citadel), and current open-source reporting')
FOOTER_WAS = ('JMIC advisory updates, BMP5 Section 5 (safe muster point vs. '
              'citadel, mscio.eu), and current open-source reporting')

GUESSED_ROW = ('<div class="cs-row"><div class="cs-label">🔢 Numbers &amp; '
               'Codes</div><div class="nums-row"><code class="num-pill">'
               'MSC.1/Circ.1334</code></div></div>')


def _drop_keep_declaration(d):
    d["propagation"]["deliberately_not_swept"] = "n/a"


def _drop_ambiguous(d):
    d["propagation"].pop("ambiguous_reported_not_corrected", None)


def _pin_a_cheat_sheet(d):
    """Give a cheat sheet a digest it has no business carrying."""
    for a in d["artefacts"]:
        if "heet" in a["path"]:
            a["digest"] = "0" * 64
            return


MUTATIONS = [
    # ---- regression: the corrected surfaces go back --------------------
    ("A", "revert the N-1 footer to citing BMP5 Section 5",
     sub_in_file(QB4_H, FOOTER_NOW, FOOTER_WAS, count=1),
     "N1_footer_no_longer_cites_BMP5_as_verification_authority"),

    ("B", "put the two MSC.1/Circ.1606 pills back on the cheat sheet",
     sub_in_file(CS9A, '<div class="cs-row"><div class="cs-label">🧠 Memory Link',
                 GUESSED_ROW.replace("MSC.1/Circ.1334", "MSC.1/Circ.1606")
                 + '<div class="cs-row"><div class="cs-label">🧠 Memory Link',
                 count=1),
     "N2_circular_removed_from_the_cheat_sheet"),

    # The forbidden repair, not the original defect.
    ("C", "guess a replacement security circular for the removed row",
     sub_in_file(CS9A, '<div class="cs-row"><div class="cs-label">🧠 Memory Link',
                 GUESSED_ROW + '<div class="cs-row"><div class="cs-label">'
                 '🧠 Memory Link', count=1),
     "N2_no_replacement_circular_was_guessed"),

    ("D", "revert the QB5_B cheat sheet to teaching BMP5 procedures",
     sub_in_file(CS5B,
                 "BMP Maritime Security procedures (1st Ed. 2025 as updated "
                 "2026 &mdash; replaced BMP5). ISPS",
                 "BMP5 procedures. ISPS", count=1),
     "N4a_teaches_the_current_publication"),

    ("E", "strip the predecessor banner off the QB4_H cheat-sheet row 11",
     sub_in_file(CS4H,
                 "<td><strong>Predecessor publication &mdash; superseded by "
                 "BMP Maritime Security; see Q13.</strong> 3 pillars",
                 "<td>3 pillars", count=1),
     "N4b_answer_cell_carries_the_predecessor_status"),

    ("F", "revert the QB1_F reg-code to Best Management Practices (BMP5)",
     sub_in_file(QB1_F,
                 '<span class="reg-code">BMP Maritime Security</span>',
                 '<span class="reg-code">Best Management Practices (BMP5)'
                 '</span>', count=1),
     "A5_reg_code_slot_names_no_superseded_publication"),

    ("G", "revert the QB4_H q6 reg-code to BMP5",
     sub_in_file(QB4_H,
                 '<span class="reg-code">BMP Maritime Security</span>'
                 '<span class="reg-desc">Guidance on electronic signature',
                 '<span class="reg-code">BMP5</span>'
                 '<span class="reg-desc">Guidance on electronic signature',
                 count=1),
     "A6_reg_code_slot_names_no_superseded_publication"),

    ("H", "revert the QB5_B answer body to BMP5 engineering measures",
     sub_in_file(QB5_B,
                 "<li><strong>BMP Maritime Security engineering measures:"
                 "</strong>",
                 "<li><strong>BMP5 engineering measures:</strong>", count=1),
     "A7_answer_body_no_longer_teaches_BMP5_measures"),

    # ---- over-sweep: the direction nobody guards -----------------------
    # The stem is targeted through its q-text WRAPPER. The same sentence also
    # appears in the page's JSON-LD block, and an unanchored count=1 replace
    # hit that copy instead - the mutation reported ESCAPED while never having
    # touched the surface under test. A mutation that edits the wrong element
    # exercises nothing.
    ("I", "sweep BMP5 out of QB4_H q11's stem - the examiner's own wording",
     sub_in_file(QB4_H,
                 '<div class="q-text">Describe the key content and operational '
                 'phases of BMP5 (Best Management Practices, Version 5).</div>',
                 '<div class="q-text">Describe the key content and operational '
                 'phases of BMP Maritime Security.</div>', count=1),
     "KEEP_examiner_wording_survives_QB4_H"),

    ("J", "sweep BMP5 out of QB9_A q9's stem",
     sub_in_file(QB9_A,
                 "What is vessel hardening? BMP5 measures.",
                 "What is vessel hardening? BMP MS measures.", count=1),
     "KEEP_examiner_wording_survives_QB9_A"),

    ("K", "correct away the predecessor record QB4_H q11 exists to be",
     sub_in_file(QB4_H,
                 "<strong>Predecessor publication — superseded; see Q13 "
                 "for the current guidance.</strong>", "", count=1),
     "KEEP_predecessor_card_is_still_a_predecessor_record"),

    ("L", "rewrite the examiner cue on the cheat sheet row 11",
     sub_in_file(CS4H, '<td>"BMP5 details"</td>',
                 '<td>"BMP MS details"</td>', count=1),
     "N4b_examiner_cue_is_KEPT_not_rewritten"),

    # ---- the record itself ---------------------------------------------
    ("M", "erase the KEEP boundary from the record",
     edit_json(MANIFEST, _drop_keep_declaration),
     "record_states_what_was_deliberately_not_swept"),

    ("N", "drop the ambiguous site instead of reporting it",
     edit_json(MANIFEST, _drop_ambiguous),
     "ambiguous_site_is_reported_not_silently_dropped"),

    # A pin on an unguarded file looks like governance and expires on the next
    # unrelated edit. The schema forbids it; this proves the gate enforces it.
    ("O", "pin a digest on a cheat sheet that no guard can hold",
     edit_json(MANIFEST, _pin_a_cheat_sheet),
     "cheat_sheets_are_declared_as_unpinned_artefacts"),

    ("Q", "erase the declaration that QB1_F#q10 was edited here",
     edit_json(MANIFEST, lambda d: d["propagation"].pop(
         "cards_edited_here_but_pinned_by_a_sibling_record", None) and None),
     "sibling_pinned_card_is_declared"),

    ("P", "strip the corpus-not-finding lesson out of known_traps 94",
     sub_in_file(TRAPS,
                 "**Emit the SURFACE with every hit.**",
                 "**Report the file and line.**", count=1),
     "known_traps_entry_94_carries_the_lesson"),
]


def main() -> int:
    return run_suite("CORR-T5-REACH-20260906", PROBE, MUTATIONS,
                     [QB4_H, QB1_F, QB5_B, QB9_A, CS9A, CS5B, CS4H,
                      MANIFEST, TRAPS])


if __name__ == "__main__":
    raise SystemExit(main())
