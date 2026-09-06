#!/usr/bin/env python3
"""Mutation suite for CORR-P1CLOSE-20260906.

The suite is shaped by HOW the three escapes happened, not by what they said.
Each family below reintroduces the same claim in a different disguise, because
"the same claim in a different disguise" is precisely what defeated the three
previous guards:

  A-C  the single-limb fire-main claim in <div>, <td> and <span> - three
       element types, one proposition. The guard that missed QB2_F read only
       <li> and <p>.
  D    the same claim written as 2.7 bar instead of 0.27 MPa. The guard that
       missed QB2_F required a literal unit string.
  E    the lower limb deleted from a complete claim - the quiet failure mode,
       since the remaining figure is correct and only the ships below the
       threshold are now taught wrongly.
  F/G  the currentness banner moved to another topic, and deleted from the
       intended one. "Exists somewhere in the file" must not be enough.
  H/I  BMP5 taught as current in prose and in a <td> - the two shapes the
       reg-code-only check could not see, on the very pages it had corrected.
  J    a historical BMP5 quote planted in a PAST PAPER, which must NOT be
       flagged. Sitting-anchored examiner wording is correct as written, and a
       sweep that cannot tell it from current teaching is the opposite defect.

J is registered as an expected NON-catch and is reported separately, because a
suite that only proves a guard fires has not shown it fires on the right thing.

Serial. Digest-only catches are not accepted: each mutation names the
substantive control that must go red.
"""
from __future__ import annotations

import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB_ROOT = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    Snapshot, run_probe, sub_in_file)

QB2_F = QB_ROOT / "QB2_F.html"
P10 = QB_ROOT / "oralnotes/miw-notes-mgmt-p10.html"
P1 = QB_ROOT / "oralnotes/miw-notes-mgmt-p1.html"
PASTPAPER = QB_ROOT / "pastpapers/QP2301.html"

GATE = "validate_correction_p1repair.py"

#: A live, complete claim to hang the element-shape mutations off.
HOST = '<div class="reg-box">'

FIREMAIN = "no_incomplete_scope_firemain_claim_anywhere"
BMP = "no_surface_teaches_BMP5_as_current"


def inject(path, host, payload):
    return sub_in_file(path, host, payload + host, count=1)


def shape(tag, figure="0.27 MPa"):
    return ('<%s>Minimum fire-main pressure required at the hydrant: '
            '<b>%s</b></%s>' % (tag, figure, tag))


def drop_lower_limb():
    """Delete only the 0.25 limb from the corrected QB2_F bullet."""
    return sub_in_file(
        QB2_F,
        ' at 6,000 GT and upwards, <strong>0.25 MPa</strong> below. The '
        'provision fixes this at the hydrants and sets no separate figure for '
        'deck monitors.',
        '.', count=1)


def move_banner():
    """Relocate the banner out of topic-46 into an earlier topic."""
    def apply():
        text = P10.read_text(encoding="utf-8")
        m = re.search(r'<div class="notes-callout"[^>]*>.*?</div>', text, re.S)
        assert m, "no banner"
        blob = m.group(0)
        text = text[:m.start()] + text[m.end():]
        k = text.find('<div class="topic-block"')
        j = text.find('<div class="section-head">', k)
        assert j > 0
        text = text[:j] + blob + text[j:]
        P10.write_bytes(text.encode("utf-8").replace(b"\r\n", b"\n"))
    return apply


def delete_banner():
    def apply():
        text = P10.read_text(encoding="utf-8")
        text = re.sub(r'<div class="notes-callout"[^>]*>.*?</div>', "", text,
                      count=1, flags=re.S)
        P10.write_bytes(text.encode("utf-8").replace(b"\r\n", b"\n"))
    return apply


MUTATIONS = [
    ("A", "single-limb fire-main claim in a <div>",
     inject(QB2_F, HOST, shape("div")), FIREMAIN),
    ("B", "the same claim in a <td>",
     inject(QB2_F, HOST, "<table><tr>%s</tr></table>" % shape("td")), FIREMAIN),
    ("C", "the same claim in a <span>",
     inject(QB2_F, HOST, shape("span")), FIREMAIN),
    ("D", "the same claim written as 2.7 bar, not 0.27 MPa",
     inject(QB2_F, HOST, shape("div", "2.7 bar")), FIREMAIN),
    ("E", "delete the lower limb from the corrected QB2_F bullet",
     drop_lower_limb(), FIREMAIN),

    ("F", "move the currentness banner into an earlier topic",
     move_banner(), "banner_exists_exactly_once_in_the_intended_topic"),
    ("G", "delete the banner from the intended topic",
     delete_banner(), "banner_exists_exactly_once_in_the_intended_topic"),

    ("H", "teach BMP5 as current in PROSE, outside any reg-code slot",
     inject(P1, '<div class="ce-tip">',
            '<p>Vessel hardening for an HRA transit is carried out in '
            'accordance with BMP5, which sets the current industry standard.'
            '</p>'), BMP),
    ("I", "teach BMP5 as current in a <td>",
     inject(P1, '<div class="ce-tip">',
            '<table><tr><td>Hardening measures are applied as per BMP5.</td>'
            '</tr></table>'), BMP),
]

#: J - must NOT be caught. A past paper legitimately preserves the wording of
#: the sitting; modernising it is the opposite defect, and a guard that cannot
#: tell the two apart is not usable on a recursive corpus.
NON_CATCH = (
    "J", "historical BMP5 wording planted in a PAST PAPER - must NOT be caught",
    inject(PASTPAPER, "</body>",
           '<div class="qa"><p>Candidates were expected to answer as per BMP5, '
           'the guidance current at the sitting.</p></div>'))

WATCHED = [QB2_F, P10, P1, PASTPAPER]


def main() -> int:
    title = "CORR-P1CLOSE-20260906"
    print(title)
    print("=" * len(title))

    code, control = run_probe(GATE)
    if control:
        print("control NOT green: %s" % sorted(control))
        return 2
    print("control green: %s exits %d\n" % (GATE, code))

    caught, escapes, crashes = 0, [], []
    for mid, desc, apply, want in MUTATIONS:
        snap = Snapshot(WATCHED)
        try:
            apply()
        except Exception as exc:                        # noqa: BLE001
            crashes.append("%s: %s" % (mid, exc))
            print("%-3s %-58s CRASH   [%s]" % (mid, desc, exc))
            snap.restore()
            continue
        _rc, failing = run_probe(GATE)
        hit = want in failing
        caught += 1 if hit else 0
        if not hit:
            escapes.append("%s (wanted %s, got %s)"
                           % (mid, want, sorted(failing) or "nothing"))
        print("%-3s %-58s %s [%s]"
              % (mid, desc, "CAUGHT " if hit else "ESCAPED", want))
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    # ---- J : the expected NON-catch --------------------------------------
    mid, desc, apply = NON_CATCH
    snap = Snapshot(WATCHED)
    try:
        apply()
        _rc, failing = run_probe(GATE)
    finally:
        bad = snap.restore()
    if bad:
        print("    RESTORE FAILED: %s" % bad)
        return 2
    ok = not failing
    if ok:
        caught += 1
    else:
        escapes.append("%s (wrongly flagged: %s)" % (mid, sorted(failing)))
    print("\n%-3s %-58s %s" % (mid, desc,
                               "CORRECTLY IGNORED" if ok
                               else "WRONGLY FLAGGED %s" % sorted(failing)))

    total = len(MUTATIONS) + 1
    print("\n%d of %d behaved as required" % (caught, total))
    print("%d mutations, %d failure(s), %d crash(es)"
          % (total, len(escapes), len(crashes)))
    for e in escapes:
        print("  PROBLEM " + e)
    for c in crashes:
        print("  CRASH   " + c)
    return 1 if (escapes or crashes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
