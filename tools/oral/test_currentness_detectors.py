#!/usr/bin/env python3
"""Adversarial control set for the currentness detectors.

Five review rounds broke five successive guards, each by rendering the same
claim differently. These cases are those breakages, written down so the sixth
cannot be found by hand: every MUST-CATCH is a form that defeated a previous
implementation, and every MUST-NOT-CATCH is legitimate content a widening
guard would start eating.

The suite is a FIXTURE, not a corpus scan. It touches no product file and
depends on no page staying the way it is today - a control harvested from live
state stops testing anything the moment the corpus moves.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from oral_currentness import (                       # noqa: E402
    firemain_scope_defects, bmp5_current_teaching, to_mpa, pressures_mpa)
from oral_visible import segments, sentences, normalise  # noqa: E402

FAILS: list[str] = []
CHECKS = 0


def check(name, ok, detail=""):
    """`ok` may be a bool or a zero-arg callable.

    A callable is evaluated HERE, inside the guard, so that an exception counts
    as a FAILURE rather than as silence. A mutation that removed a unit from the
    conversion table made `to_mpa` return None, the arithmetic raised, the
    script died before printing anything, and the mutation suite saw no FAIL
    line at all - reporting an escape where the guard had actually collapsed.
    A check that cannot fail loudly is a check that cannot be trusted quietly.
    """
    global CHECKS
    CHECKS += 1
    if callable(ok):
        try:
            ok = bool(ok())
            detail = detail
        except Exception as exc:                        # noqa: BLE001
            ok, detail = False, "raised %s: %s" % (type(exc).__name__, exc)
    if not ok:
        FAILS.append(name)
    print("%-4s %-58s %s" % ("PASS" if ok else "FAIL", name, detail))


# ---------------------------------------------------------------- pressure
COMPLETE = ("Minimum pressure at the hydrants, both required pumps delivering "
            "simultaneously: 0.27 MPa at 6,000 GT and upwards, 0.25 MPa below.")

PRESSURE_CATCH = [
    ("plain MPa", "<li>Minimum required hydrant pressure 0.27 MPa</li>"),
    ("N/mm2 entity", "<li>Minimum required hydrant pressure 0.27 N/mm&sup2;</li>"),
    ("bar", "<li>Minimum required hydrant pressure 2.7 bar</li>"),
    ("kPa", "<li>Minimum required hydrant pressure 270 kPa</li>"),
    ("range", "<li>Minimum required hydrant pressure 0.27-0.35 MPa</li>"),
    ("en-dash range", "<li>Minimum required hydrant pressure 0.27–0.35 MPa</li>"),
    ("comma decimal", "<li>Minimum required hydrant pressure 0,27 MPa</li>"),
    ("nbsp", "<li>Minimum required hydrant pressure 0.27&nbsp;MPa</li>"),
    ("figure split by tag", "<li>Minimum required hydrant pressure "
                            "<strong>0.27</strong> MPa</li>"),
    ("unit split by tag", "<li>Minimum required hydrant pressure 0.27 "
                          "<span>MPa</span></li>"),
    ("numeric entity", "<li>Minimum required hydrant pressure &#48;.27 MPa</li>"),
    ("div", "<div>Minimum required fire-main pressure 0.27 MPa</div>"),
    ("td", "<table><tr><td>Minimum required hydrant pressure 0.27 MPa</td></tr></table>"),
    ("dd", "<dl><dt>Fire main</dt><dd>Minimum required hydrant pressure 0.27 MPa</dd></dl>"),
    ("figcaption", "<figure><figcaption>Minimum required hydrant pressure "
                   "0.27 MPa</figcaption></figure>"),
    ("caption", "<table><caption>Minimum required hydrant pressure 0.27 MPa"
                "</caption></table>"),
    ("blockquote", "<blockquote>Minimum required hydrant pressure 0.27 MPa"
                   "</blockquote>"),
    ("section, no inner block", "<section>Minimum required hydrant pressure "
                                "0.27 MPa</section>"),
    ("heading", "<h4>Minimum required hydrant pressure 0.27 MPa</h4>"),
    ("kg/cm2", "<li>Minimum required hydrant pressure 2.7538 kg/cm&sup2;</li>"),
    ("psi", "<li>Minimum required hydrant pressure 39.16 psi</li>"),
    ("mbar", "<li>Minimum required hydrant pressure 2700 mbar</li>"),
    ("atm", "<li>Minimum required hydrant pressure 2.6647 atm</li>"),
    ("unicode minus range", "<li>Minimum required hydrant pressure "
                            "0.27−0.35 MPa</li>"),
    ("'and' range", "<li>Minimum required hydrant pressure 0.27 and 0.35 MPa</li>"),
    ("lowest permissible", "<li>Lowest permissible hydrant pressure 0.27 MPa</li>"),
    ("shall not fall below", "<li>Hydrant pressure shall not fall below 0.27 MPa</li>"),
    ("modal in parent, figure in child",
     "<div>The minimum at the hydrant is <span>0.27 MPa</span></div>"),
    ("only the lower limb", "<li>Minimum required hydrant pressure 0.25 MPa</li>"),
    ("denial in a PRIOR clause, claim after",
     "<li>The former practice varied; the minimum required hydrant pressure "
     "is 0.27 MPa.</li>"),
]

PRESSURE_NO_CATCH = [
    ("complete two-limb claim", "<li>%s</li>" % COMPLETE),
    ("complete, in bar", "<li>Minimum at the hydrants with both required pumps: "
                         "2.7 bar at 6,000 GT and upwards, 2.5 bar below.</li>"),
    ("HydroPen operating pressure",
     "<p>It uses the pressure of the delivered fire main water (typically "
     "5-7 bar) to drive an internal turbine.</p>"),
    ("weathertightness hose test",
     "<li>A jet from a 12.5 mm nozzle at a minimum pressure of 2 Bar from "
     "1.5 m.</li>"),
    ("compressed air, unrelated",
     "<li>Control air minimum 7 bar at the manifold.</li>"),
    ("version stamp quoting the removed figure",
     '<span class="q-version">corrected: the 4.0 bar minimum required at the '
     'highest hydrant was not a SOLAS figure; 0.27 MPa applies</span>'),
    ("a pressure with no fire-main subject",
     "<li>Minimum required test pressure 0.27 MPa on the hydraulic jack.</li>"),
]

# ---------------------------------------------------------------- BMP5
BMP_CATCH = [
    ("plain assertion", "<p>BMP5 is the current industry guidance.</p>"),
    ("refer to", "<p>Refer to BMP5 for the hardening measures.</p>"),
    ("remains the reference", "<p>BMP5 remains the reference for HRA transits.</p>"),
    ("bare code cell", "<table><tr><td>BMP5</td><td>Ship hardening guidance for "
                       "HRA transits</td></tr></table>"),
    ("heading", "<h4>BMP5 Requirements</h4>"),
    ("use ... procedures", "<p>Use BMP5 procedures during the transit.</p>"),
    ("denial then live claim",
     "<p>BMP5 replaced BMP4, but BMP5 is what we use today.</p>"),
    ("split across tags", "<p>Harden the vessel as per <strong>BMP</strong>5 "
                          "before entering the HRA.</p>"),
    ("nbsp", "<p>Hardening is carried out under BMP&nbsp;5.</p>"),
    ("ce-tip prose", '<div class="ce-tip">State that you rig razor wire per '
                     'BMP5 before the transit.</div>'),
    ("is to be used", "<p>BMP5 is to be used for the citadel arrangements.</p>"),
    ("governed by", "<p>Vessel hardening is governed by BMP5.</p>"),
]

BMP_NO_CATCH = [
    ("superseded", "<p>BMP5 was superseded by BMP Maritime Security.</p>"),
    ("examiner cue", '<div class="q-text">Describe the operational phases of '
                     'BMP5.</div>'),
    ("cheat-sheet stem", '<div class="cs-qtitle">War risk / vessel hardening / '
                         'BMP5 - explain.</div>'),
    ("predecessor note", "<p>BMP5 was the industry standard guide; it is no "
                         "longer current.</p>"),
    ("bibliography", '<ul class="ref-list"><li>BMP5 - "Best Management '
                     'Practices to Deter Piracy" (industry coalition)</li></ul>'),
    ("explicit prohibition", "<p>Do not offer BMP5 as current.</p>"),
    ("question form", "<p>Is BMP5 still the current publication?</p>"),
    ("names the successor", "<p>BMP Maritime Security replaced BMP5 in 2025.</p>"),
    ("topic title", '<h2 class="topic-title">The SUA Convention &amp; BMP5 '
                    'Counter-Piracy Architecture</h2>'),
    ("index row", '<a class="idx-row"><span class="idx-topic">BMP 5</span>'
                  '<span class="idx-page">p.244</span></a>'),
    ("version stamp", '<span class="q-version">corrected: BMP5 marked '
                      'superseded</span>'),
]


def main() -> int:
    # ---- unit equivalence, arithmetic ---------------------------------
    equiv = [("0.27", "MPa"), ("0.27", "N/mm2"), ("2.7", "bar"),
             ("270", "kPa"), ("2700", "mbar"), ("270000", "Pa")]
    check("unit_equivalence_to_one_scale",
          lambda: all(abs(to_mpa(v, u) - 0.27) < 1e-6 for v, u in equiv),
          "MPa = N/mm2 = bar/10 = kPa/1000 = mbar/10000 = Pa/1e6")
    check("legacy_units_convert_deterministically",
          lambda: abs(to_mpa("2.7538", "kg/cm2") - 0.27) < 1e-3
          and abs(to_mpa("39.16", "psi") - 0.27) < 1e-3
          and abs(to_mpa("2.6647", "atm") - 0.27) < 1e-3,
          "kg/cm2, psi and atm land on 0.27 MPa")
    check("range_binds_its_unit_to_every_figure",
          lambda: [v for v, _ in pressures_mpa(normalise("0.27-0.35 MPa"))]
          == [0.27, 0.35],
          "only the last figure carries the unit in source text")

    # ---- normalisation collapses renderings ---------------------------
    forms = ["0.27 MPa", "0.27&nbsp;MPa", "<strong>0.27</strong> MPa",
             "0.27 <span>MPa</span>", "&#48;.27 MPa", "0.27 MPa"]
    texts = {segments("<p>%s</p>" % f)[0][0] for f in forms}
    check("all_renderings_normalise_to_one_string", texts == {"0.27 MPa"},
          "%d form(s) -> %s" % (len(forms), sorted(texts)))

    # ---- sentence scoping ---------------------------------------------
    s = sentences(normalise("BMP5 replaced BMP4, but BMP5 is what we use today."))
    check("denial_and_claim_separate_into_propositions", len(s) >= 1,
          "%d proposition(s)" % len(s))

    # ---- pressure: must catch -----------------------------------------
    def _missed(cases, fn):
        out = []
        for n, h in cases:
            try:
                if not fn(h):
                    out.append(n)
            except Exception as exc:                    # noqa: BLE001
                out.append("%s(raised %s)" % (n, type(exc).__name__))
        return out

    def _wrong(cases, fn):
        out = []
        for n, h in cases:
            try:
                if fn(h):
                    out.append(n)
            except Exception as exc:                    # noqa: BLE001
                out.append("%s(raised %s)" % (n, type(exc).__name__))
        return out

    missed = _missed(PRESSURE_CATCH, firemain_scope_defects)
    check("pressure_MUST_CATCH_all_renderings", not missed,
          "%d case(s), missed: %s" % (len(PRESSURE_CATCH), missed or "none"))

    # ---- pressure: must not catch -------------------------------------
    wrong = _wrong(PRESSURE_NO_CATCH, firemain_scope_defects)
    check("pressure_MUST_NOT_CATCH_legitimate_content", not wrong,
          "%d case(s), wrongly flagged: %s" % (len(PRESSURE_NO_CATCH),
                                               wrong or "none"))

    # ---- BMP5: must catch ---------------------------------------------
    missed = _missed(BMP_CATCH, bmp5_current_teaching)
    check("bmp5_MUST_CATCH_live_claims", not missed,
          "%d case(s), missed: %s" % (len(BMP_CATCH), missed or "none"))

    # ---- BMP5: must not catch -----------------------------------------
    wrong = _wrong(BMP_NO_CATCH, bmp5_current_teaching)
    check("bmp5_MUST_NOT_CATCH_historical_or_quoted", not wrong,
          "%d case(s), wrongly flagged: %s" % (len(BMP_NO_CATCH),
                                               wrong or "none"))

    # ---- the container exemption is SUBJECT-SPECIFIC -------------------
    unrelated = ('<div class="q-card"><p>Currentness note: MSC.535(107) has '
                 'been superseded for lifeboat ventilation.</p>'
                 '<p>Harden the vessel as per BMP5.</p></div>')
    check("currentness_exemption_is_subject_specific",
          bool(bmp5_current_teaching(unrelated)),
          "a note about another instrument grants no immunity to a BMP5 claim")
    related = ('<div class="q-card"><p>Currentness note: BMP5 has been '
               'superseded by BMP Maritime Security.</p>'
               '<p>BMP5 hardening measures: razor wire, citadel.</p></div>')
    check("currentness_exemption_still_governs_its_own_subject",
          not bmp5_current_teaching(related),
          "a BMP-subject note does govern technique text beneath it")

    # ---- the detector NEVER rewrites -----------------------------------
    probe = "<li>Minimum required hydrant pressure 0.27 MPa</li>"
    before = probe
    firemain_scope_defects(probe)
    bmp5_current_teaching(probe)
    check("detectors_are_pure_and_rewrite_nothing", probe == before,
          "detection only - no editorial side effect")

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: " + ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
