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
QB_ROOT = HERE.parents[1] / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_currentness import (                       # noqa: E402
    firemain_scope_defects, bmp5_current_teaching, to_mpa, pressures_mpa)
from oral_visible import (segments, sentences, normalise,
                          HEADING_REACH)  # noqa: E402

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
    # This asserted `len(s) >= 1`, which is true of every non-empty string. It
    # was the NAMED guard for clause-scoped denial and it could not fail, so it
    # certified the escape below as closed. The property is not "how many
    # propositions came back" but "the denial and the live claim are in
    # DIFFERENT ones".
    def _split(sent):
        parts = sentences(normalise(sent))
        d = [i for i, x in enumerate(parts) if "replaced" in x]
        c = [i for i, x in enumerate(parts) if "use today" in x
             or "remains the current" in x]
        return bool(d) and bool(c) and set(d) != set(c)

    check("denial_and_claim_separate_into_propositions",
          _split("BMP5 replaced BMP4, but BMP5 is what we use today."),
          "subordinating conjunction: denial and claim are separated")

    # ---- E1: coordinated clauses --------------------------------------
    # Was reported OPEN by the previous record. Two properties, both needed:
    # the coordinator SPLITS a clause pair, and does NOT split a noun pair.
    check("E1_coordinator_splits_clauses_not_noun_lists",
          len(sentences(normalise(
              "BMP5 replaced BMP4 and remains the current standard"))) == 2
          and len(sentences(normalise(
              "BMP5 and BMP4 are historical predecessors"))) == 1,
          "left needs a verb, right must open with one")

    E1_CATCH = [
        # SHARED subject - the live clause omits it.
        "BMP5 replaced BMP4 and remains the current industry standard",
        # OWN subject - the commoner shape, and the one an earlier version of
        # this detector was blind to because it demanded that a coordinated
        # clause OPEN with its verb.
        "BMP4 was withdrawn and BMP5 is the current industry guidance.",
        "BMP4 is superseded, so BMP5 is what we use today.",
        "BMP4 no longer applies and BMP5 remains the standard on board.",
        "BMP5 superseded BMP4 but BMP5 is still what we use today",
        "BMP5 was the predecessor, yet refer to BMP5 for current operations",
    ]
    E1_PASS = [
        "BMP5 replaced BMP4 and was itself superseded by BMP Maritime Security",
        "BMP5 and BMP4 are historical predecessors",
        "examiner asked for BMP5 and BMP Maritime Security differences",
    ]
    check("E1_MUST_CATCH_denial_then_live_claim",
          all(bmp5_current_teaching("<p>%s</p>" % c) for c in E1_CATCH),
          "%d case(s); the live clause inherits BMP5 as its subject"
          % len(E1_CATCH))
    check("E1_MUST_NOT_CATCH_wholly_historical",
          not any(bmp5_current_teaching("<p>%s</p>" % c) for c in E1_PASS),
          "%d case(s)" % len(E1_PASS))

    # ---- E2: the name is one publication, three spellings --------------
    check("E2_hyphenated_name_is_the_same_publication",
          bool(bmp5_current_teaching("<p>BMP-5 is current guidance</p>"))
          and bool(bmp5_current_teaching("<p>BMP 5 is current guidance</p>"))
          and not bmp5_current_teaching("<p>BMP-5 was superseded</p>"),
          "BMP5 / BMP 5 / BMP-5 catch alike; denial still excuses")

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

    # ---- E3: a figure can govern without a modal -----------------------
    E3_CATCH = ["<li>Hydrant pressure - 0.27 N/mm&sup2;</li>",
                "<li>Fire main: 0.27 MPa</li>",
                "<h4>Key numbers</h4><ul><li>hydrant 2.7 bar</li></ul>",
                # A label:value row with four trailing words, and ordinary
                # prose. Both walked past a shape-and-vocabulary version of
                # this check; the reg-box row is the very surface three prior
                # defects in this family were found on.
                '<div class="reg-box"><div class="reg-row"><span>SOLAS '
                'II-2/10.2.1.6</span><span>Hydrant pressure: 0.27 N/mm2 on '
                'cargo ships</span></div></div>',
                '<div class="q-a"><p>SOLAS II-2/10.2.1.6 gives 0.27 N/mm2 at '
                'the hydrant for cargo ships.</p></div>',
                '<table><tr><td>Fire main</td><td>0.27 N/mm2 at the hydrants, '
                'two pumps delivering</td></tr></table>',
                '<div class="q-a"><p>Sir, the hydrant pressure is 0.27 N/mm2 '
                'with both pumps running.</p></div>']
    E3_PASS = ["<li>HydroPen operating pressure 5-7 bar</li>",
               "<li>Hose-test pressure 2 bar</li>",
               "<p>On trials the fire pump delivered 0.27 MPa at the manifold "
               "and the reading was logged.</p>",
               '<span class="q-version">was "4.0 Bar", corrected</span>']
    check("E3_MUST_CATCH_modal_free_governing_figure",
          all(firemain_scope_defects(c) for c in E3_CATCH),
          "label:value, and figures presented to memorise")
    check("E3_MUST_NOT_CATCH_prose_or_ungoverned_figures",
          not any(firemain_scope_defects(c) for c in E3_PASS),
          "%d case(s): operating pressure, hose test, prose, changelog"
          % len(E3_PASS))

    # ---- E4: the subject lives in the preceding sibling block ----------
    check("E4_MUST_CATCH_subject_in_preceding_sibling",
          bool(firemain_scope_defects(
              "<div><h4>Fire main</h4><ul><li>Minimum 0.27 MPa</li></ul></div>")),
          "a heading labels the block beneath it")
    # The decisive case is a label that WOULD produce a hit if it leaked: the
    # same "Fire main" heading, the same governed figure, separated only by a
    # closed container. An earlier version of this check used an unrelated
    # heading ("Lifeboat davits"), which passes whether the boundary is
    # enforced or not - it was the subject test doing the work, not the bound.
    # A mutation that removed the bound proved it, and this is the repair.
    check("E4_label_does_not_leak_across_containers",
          not firemain_scope_defects(
              "<div><h4>Fire main</h4></div>"
              "<div><ul><li>Minimum 0.27 MPa</li></ul></div>")
          and not firemain_scope_defects(
              "<div><h4>HydroPen</h4><ul><li>Operating pressure 5-7 bar</li>"
              "</ul></div>"),
          "same label, same figure, closed sibling: identity, not tag name")

    check("E4_label_reach_is_bounded",
          not firemain_scope_defects(
              "<div><h4>Fire main</h4><ul>"
              + "<li>filler line</li>" * (HEADING_REACH + 2)
              + "<li>Minimum 0.27 MPa</li></ul></div>"),
          "a heading does not label the whole rest of a long container")

    # ---- generated-surface policy (one test, both directions) ----------
    # A generated page gets no blanket exemption: the stem echo is excused by
    # the href that names the card it quotes, and a label the generator wrote
    # itself is judged like any teaching text. Same page, same class, same
    # element - opposite verdicts, decided by provenance alone.
    check("generated_surface_status_follows_item_provenance",
          not bmp5_current_teaching(
              '<ul class="q-list"><li><a href="QB9_A.html#q9">'
              'BMP5 measures.</a></li></ul>')
          and bool(bmp5_current_teaching(
              '<ul class="q-list"><li><a href="topics.html#D09">'
              'BMP5 is the current piracy guidance</a></li></ul>')),
          "stem echo KEEP; generator-authored label CAUGHT")

    # ---- the detector NEVER rewrites -----------------------------------
    # This compared a `str` to itself. Python strings are immutable, so it
    # could not fail whatever the detectors did - including writing files. The
    # real risk a "detection only" record must exclude is a detector EDITING
    # the corpus, so the corpus is what is now hashed.
    import hashlib
    import tempfile

    probe = "<li>Minimum required hydrant pressure 0.27 MPa</li>"
    with tempfile.TemporaryDirectory() as tmp:
        f = pathlib.Path(tmp) / "probe.html"
        f.write_bytes(probe.encode("utf-8"))
        watched = sorted(QB_ROOT.rglob("*.html")) + [f]
        before = {w: hashlib.sha256(w.read_bytes()).hexdigest() for w in watched}
        v1 = (firemain_scope_defects(probe), bmp5_current_teaching(probe))
        v2 = (firemain_scope_defects(probe), bmp5_current_teaching(probe))
        after = {w: hashlib.sha256(w.read_bytes()).hexdigest() for w in watched}
    moved = [w.name for w in watched if before[w] != after[w]]
    check("detectors_are_pure_and_rewrite_nothing",
          not moved and v1 == v2,
          "%d files hashed unchanged; verdict idempotent" % len(watched)
          if not moved else "MOVED: %s" % moved[:5])

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: " + ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
