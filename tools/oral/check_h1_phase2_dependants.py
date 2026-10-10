#!/usr/bin/env python3
"""
Targeted regression check for the H-1 Phase 2 corrections (CORR-H1-SOLAS-PHASE2-20261010, provisional ID).

WHY THIS EXISTS
---------------
The H-1 content gate evaluates card units. The SQ-1 / F2 / F3 dependants that carried the wrong
capacity and monitor claims sit OUTSIDE card units (page header, correction banner, sidebar, footer,
quick-recall flip cards, 'Fast Recall' recall grids) or on cheat sheets, so a regression there would be
invisible to the unit model. This check reads WHOLE FILES:

  forbidden  every wrong phrase removed by the correction must stay absent from its file;
  required   every corrected statement must stay present in its file.

`--self-test` proves the check can fail: in a temporary copy it re-injects each forbidden phrase and
deletes each required statement, one at a time, and requires every mutation to be caught (0 escapes).

NOT REGISTERED in the release gates or runner (no blocking integration; Phase 3 is not authorised).
Prints "<N> checks, <M> FAIL" like the repo's validators.

Usage: python tools/oral/check_h1_phase2_dependants.py [--repo PATH] [--self-test]
"""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

FORBIDDEN = {
    "meoclass1/QB2_B.html": ["400 L/min", "24 m³/hr", "24 m³/h", "48 m³/hr", "80 m³/hr", "Water monitor flow rate = 400"],
    "meoclass1/QB2_B_CheatSheet.html": ["400 L/min", "24 m³/hr", "48 m³/hr", "800 L/min", "80–120 m³/hr", "quote 80 m³/hr",
                                        "minimum <strong>2 portable water monitors</strong> mandatory"],
    "meoclass1/QB2_H.html": ["Minimum required discharge capacity for each mobile water monitor under SOLAS", "beam over 30 meters",
                             "<div class=\"back\">Min 1,000 L/min (60 m³/h) each."],
    "meoclass1/QB2_F.html": ["each ≥60 m³/hr", "<div><b>Monitor flow</b>&ge;60", "minimum monitor discharge", "each &ge;<strong>60 m&sup3;/hr"],
    "meoclass1/QB2_A.html": ["SOLAS Chapter V (Regulation 20)", "± 0.2°", "± 1.0°", "inclinometer additions"],
    "meoclass1/QB1_F.html": ["Emerging SOLAS Fire-Fighting", "lithium-ion battery transport", "active push through"],
    "meoclass1/QB10_B.html": ["IMO's GISIS database", "Central reporting point for confirmed container-loss", "(loss reporting, GISIS)",
                              "Coast Guard/Flag State/nearby vessels"],
}
REQUIRED = {
    "meoclass1/QB2_B.html": [
        "Portable Water Monitors (II-2/10.7.3 numbers; MSC.1/Circ.1472 capacity)",                                    # header l.151
        "<strong>⚠ Q10 Corrected:</strong> SOLAS sets no water monitor flow figure; the MSC.1/Circ.1472 guideline is 60 m³/h",  # banner l.157
        "<div class=\"sidebar-note\">⚠ Q10 corrected: SOLAS sets no water monitor flow figure",                       # sidebar l.203
        "<em>Q10 corrected: SOLAS II-2/10.7.3 sets no portable water monitor flow figure",                             # footer l.1791
        "at least <strong>four (4)</strong> where it is 30 m or more (II-2/10.7.3.2)",                                 # q10 five-tier item
    ],
    "meoclass1/QB2_B_CheatSheet.html": [
        "⚠ Q10 CORRECTED: SOLAS II-2/10.7.3 sets no portable water monitor flow figure",
        "at least <strong>4</strong> if breadth ≥ 30 m (II-2/10.7.3.2)",
        "MSC.1/Circ.1472 guideline minimum <strong>60 m³/h (1,000 l/min)</strong>",
        "⚠ Q10 corrected: SOLAS sets no portable water monitor flow figure",
    ],
    "meoclass1/QB2_H.html": [
        "MSC.1/Circ.1472 guideline: min 1,000 l/min (60 m³/h) each — SOLAS sets no flow figure. Five or more tiers:",   # quick-recall l.355
        "at least four where it is 30 m or more (II-2/10.7.3.2)",
    ],
    "meoclass1/QB2_F.html": [
        "<div><b>Breadth &lt;30m, 5+ tiers</b>2 monitors</div>",                                                      # Fast Recall l.416
        "<div><b>Breadth &ge;30m, 5+ tiers</b>4 monitors</div>",                                                      # l.417
        "<div><b>Monitor capacity</b>60 m&sup3;/h each (MSC.1/Circ.1472 guideline)</div>",                            # l.418
    ],
    "meoclass1/QB2_A.html": ["Under <strong>SOLAS V/19.2.12</strong>, added by MSC.532(107)", "<strong>5% of reading or ± 1°</strong>"],
    "meoclass1/QB1_F.html": ["has applied since 1 January 2016", "at least four where it is 30 m or more (II-2/10.7.3.2)"],
    "meoclass1/QB10_B.html": ["the flag State reports the loss to IMO (V/31.2.3)", "the nearest coastal State and the flag State"],
}


def run(repo: Path, quiet: bool = False) -> list[str]:
    failed = []
    for rel in sorted(set(FORBIDDEN) | set(REQUIRED)):
        p = repo / rel
        text = p.read_text(encoding="utf-8") if p.is_file() else None
        for phrase in FORBIDDEN.get(rel, []):
            ok = text is not None and phrase not in text
            failed += [] if ok else ["%s forbidden %r" % (rel, phrase)]
            if not quiet:
                print("%-5s forbidden_absent  %-36s %s" % ("PASS" if ok else "FAIL", rel.replace("meoclass1/", ""), phrase[:70]))
        for phrase in REQUIRED.get(rel, []):
            ok = text is not None and phrase in text
            failed += [] if ok else ["%s required %r" % (rel, phrase)]
            if not quiet:
                print("%-5s required_present  %-36s %s" % ("PASS" if ok else "FAIL", rel.replace("meoclass1/", ""), phrase[:70]))
    return failed


def self_test(repo: Path) -> int:
    """Each mutation runs on a fresh temporary copy of the governed files; the live tree is never written."""
    mutations, escapes = 0, []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for rel in sorted(set(FORBIDDEN) | set(REQUIRED)):
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
        def fresh():
            for rel in sorted(set(FORBIDDEN) | set(REQUIRED)):
                shutil.copyfile(repo / rel, tmp / rel)
        fresh()
        if run(tmp, quiet=True):
            print("SELF-TEST ABORT: the clean copy does not pass")
            return 2
        for rel, phrases in FORBIDDEN.items():
            for phrase in phrases:                      # re-inject at the end of <body>, i.e. outside every card unit
                fresh()
                t = (tmp / rel).read_text(encoding="utf-8")
                (tmp / rel).write_text(t.replace("</body>", "<p>%s</p></body>" % phrase, 1) if "</body>" in t else t + phrase, encoding="utf-8")
                mutations += 1
                if not run(tmp, quiet=True):
                    escapes.append("inject %s %r" % (rel, phrase))
        for rel, phrases in REQUIRED.items():
            for phrase in phrases:
                fresh()
                t = (tmp / rel).read_text(encoding="utf-8")
                (tmp / rel).write_text(t.replace(phrase, ""), encoding="utf-8")
                mutations += 1
                if not run(tmp, quiet=True):
                    escapes.append("delete %s %r" % (rel, phrase))
    print("self-test: %d mutations, %d escapes%s" % (mutations, len(escapes), ("\n  " + "\n  ".join(escapes)) if escapes else ""))
    return 1 if escapes else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    repo = Path(a.repo)
    if a.self_test:
        return self_test(repo)
    failed = run(repo)
    n = sum(len(v) for v in FORBIDDEN.values()) + sum(len(v) for v in REQUIRED.values())
    print("\n%d checks, %d FAIL" % (n, len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
