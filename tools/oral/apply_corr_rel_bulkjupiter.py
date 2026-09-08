#!/usr/bin/env python3
"""CORR-REL-BULKJUPITER-20260908 -- the two Bulk Jupiter cards.

Release qualification found two live material factual errors about the loss of
`Bulk Jupiter`, both in memorisation-weighted Casualty Link blocks, and both
contradicted by the flag State's own report:

  QB8_A#q4  attributed the marine safety investigation to *the IMO*, and turned
            an expressly qualified finding into a conclusion. The investigation
            was the Bahamas Maritime Authority's, as flag State. Its report
            says in terms that there is no physical evidence to confirm the
            cause, and concludes only that liquefaction OR a free-surface
            effect is most probable. Who investigates a casualty is itself a
            MEO Class I oral topic, so this card taught the wrong answer to a
            question the candidate will be asked directly.

  QB5_A#q11 said the vessel "sank within 5 minutes". The report gives
            approximately 20 minutes, and the same figure again as the
            abandonment window (0640 general alarm -> 0700 EPIRB).

Source, read at source: BMA `M.v Bulk Jupiter - Marine Safety Investigation
Report` (published 18 August 2015), sections 3, 4.2-4.6 and 5. The 21.3% / 10%
moisture pair, the ~20 minutes, the heavy-weather NE monsoon Beaufort 6-7
conditions and the "no physical evidence ... most probable" conclusion are all
taken from it.

Every edit is a single exact-string replacement which must match exactly once.
Nothing else on either page is touched. Read/write use `newline=""` in both
directions so the file's own line endings survive the edit byte for byte.
"""

from __future__ import annotations

import pathlib

QB = pathlib.Path(__file__).resolve().parents[2] / "meoclass1"

DOT = "·"          # the pages store the separator as the literal character
MDASH = "—"

EDITS: list[tuple[str, str, str]] = [
    (
        "QB8_A.html",
        "In 2015, the bulk carrier <em>Bulk Jupiter</em> sank rapidly off the "
        "coast of Vietnam while carrying 46,000 tonnes of bauxite, resulting in "
        "the loss of 18 crew members. The subsequent investigation by the IMO "
        "concluded that the bauxite cargo, which had been treated as a standard "
        "Group C cargo, contained a high percentage of fines and high internal "
        "moisture. Under the ship&#x27;s movements, the material underwent "
        "rapid liquefaction (Group A transition), causing an immediate loss of "
        "stability and a sudden capsize, which led to a revision of the IMSBC "
        "Code individual schedules for bauxite.",

        "On 2 January 2015 the bulk carrier <em>Bulk Jupiter</em> foundered in "
        "approximately 20 minutes in the South China Sea off Vung Tau, Vietnam, "
        "while carrying 46,400 tonnes of bauxite, with the loss of 18 of her 19 "
        "crew. The marine safety investigation was carried out by the "
        "<strong>Bahamas Maritime Authority</strong> as flag State &mdash; "
        "investigating a casualty is a flag-State duty under SOLAS XI-1/6 and "
        "the Casualty Investigation Code, and the IMO does not investigate "
        "casualties; it received the Bahamas submission and issued the warning. "
        "The report found the cargo, which had been declared as a standard "
        "Group C cargo, carried an average moisture content of "
        "<strong>21.3%</strong> against the <strong>10%</strong> declared. On "
        "cause it is expressly qualified: there is <em>no physical evidence</em> "
        "to confirm what caused the unrecoverable list to starboard, and it "
        "concludes only that it is <em>most probable</em> that either "
        "liquefaction or a free-surface effect induced it. Say it that way round "
        "in an oral &mdash; the high fines content and moisture of bauxite led "
        "in due course to a revision of the IMSBC Code individual schedules, "
        "adding a separate Group A schedule for BAUXITE FINES.",
    ),
    (
        "QB8_A.html",
        '<span class="q-version">QB8 %s Q4 %s v1.0</span>' % (DOT, DOT),
        '<span class="q-version">QB8 %s Q4 %s v1.1 &mdash; corrected 8 Sep 2026 '
        'by CORR-REL-BULKJUPITER-20260908: the Casualty Link attributed the '
        '<em>Bulk Jupiter</em> marine safety investigation to the IMO and stated '
        'its finding as a conclusion. The investigation was the Bahamas Maritime '
        'Authority&#x27;s as flag State, and its report records no physical '
        'evidence of cause and only a most-probable finding of liquefaction or '
        'free-surface effect. Date, position, tonnage, crew toll and the '
        '21.3%% / 10%% moisture pair added from that report. %s v1.0</span>'
        % (DOT, DOT, DOT),
    ),
    (
        "QB5_A.html",
        "The vessel sank within 5 minutes of bauxite cargo liquefying in heavy "
        "weather, resulting from inadequate moisture content risk assessment "
        "before loading.",

        "The vessel foundered in approximately 20 minutes in heavy weather "
        "(NE monsoon, Beaufort 6&ndash;7) after the bauxite cargo most probably "
        "liquefied or developed a free surface, resulting from inadequate "
        "moisture content risk assessment before loading.",
    ),
    (
        "QB5_A.html",
        '<span class="q-version">QB5_A %s Q11 %s v1.0</span>' % (DOT, DOT),
        '<span class="q-version">QB5_A %s Q11 %s v1.1 &mdash; corrected 8 Sep '
        '2026 by CORR-REL-BULKJUPITER-20260908: the card said <em>Bulk '
        'Jupiter</em> &ldquo;sank within 5 minutes&rdquo;. The Bahamas Maritime '
        'Authority report gives approximately 20 minutes, and the same figure as '
        'the abandonment window. The mechanism is now stated as the report states '
        'it %s most probably liquefaction or a free-surface effect. The '
        'risk-assessment teaching, the TML point and the heavy-weather '
        'conditions are unchanged. %s v1.0</span>' % (DOT, DOT, MDASH, DOT),
    ),
]


def main() -> int:
    bad = 0
    for fname, old, new in EDITS:
        path = QB / fname
        text = path.read_text(encoding="utf-8", newline="")
        n = text.count(old)
        if n != 1:
            print("ABORT %-12s matched %d times: %.70s" % (fname, n, old))
            bad += 1
            continue
        path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")
        print("OK    %-12s %5d -> %5d bytes" % (fname, len(old), len(new)))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
