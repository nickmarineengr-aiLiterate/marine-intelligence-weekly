"""Apply CORR-P1CLOSE-20260906 - the Pass-1 repair closure.

Three P1 escapes, all of the same underlying shape: a guard, or an edit, that
matched a SPELLING or a POSITION rather than the thing it meant.

P1-A  QB2_F taught `0.27 MPa` as a fire-main minimum "at deck monitors", at two
      sites, single-limb. The repair's sweep required the literal `0.27 N/mm`
      and read only `<li>` and `<p>`, so it was blind to the unit and to the
      `<div>`. Both sites are corrected here, and the DETECTOR is rebuilt to
      normalise units and to work on any candidate-facing element
      (`oral_currentness.firemain_scope_defects`).

P1-B  The BMP currentness banner was inserted at the FIRST occurrence of its
      anchor in the file and landed in the UNCLOS Part XII topic, ~375 lines
      and four topics away from the BMP material it was written for. Topic 46
      then pointed at "the currentness note above", across four unrelated
      topics. It is removed from there and inserted INSIDE the topic-46 block,
      located by its structural id, not by a text needle.

P1-C  The BMP5 gate inspected `<span class="reg-code">` only, so the `<td>` cell
      and CE-tip prose the repair had just corrected would have returned
      unnoticed. Replaced by a semantic check
      (`oral_currentness.bmp5_current_teaching`) that reads visible text on any
      element and asks whether the sentence is OPERATIVE.

UNIT NORMALISATION IS A DETECTOR RULE, NOT AN EDITORIAL ONE. QB2_F prints MPa
and keeps printing MPa; 0.27 MPa and 0.27 N/mm2 are the same pressure and the
guard now knows that, which is all that was wrong.

AND THE PROVISION IS NOT RELOCATED. SOLAS II-2/10.2.1.6 fixes the minimum at
the HYDRANTS with the two required pumps delivering simultaneously. It sets no
separate figure for deck monitors, so the corrected text says where the figure
actually applies rather than inventing a monitor limit.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
QB_ROOT = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import read_text  # noqa: E402

P10 = QB_ROOT / "oralnotes/miw-notes-mgmt-p10.html"

EDITS = [
    dict(id="P1-A1", file="QB2_F.html", anchor="q2", count=1,
         old='<li>Minimum fire-main pressure benchmark: <strong>0.27 MPa'
             '</strong> at deck monitors</li>',
         new='<li>Minimum pressure at the <strong>hydrants</strong>, both '
             'required pumps delivering simultaneously (SOLAS II-2/10.2.1.6, '
             'cargo ships): <strong>0.27 MPa</strong> at 6,000 GT and upwards, '
             '<strong>0.25 MPa</strong> below. The provision fixes this at the '
             'hydrants and sets no separate figure for deck monitors.</li>',
         why="single-limb 0.27 MPa taught as a fire-main minimum AT DECK "
             "MONITORS - wrong for every cargo ship under 6,000 GT, and "
             "attributing to SOLAS a monitor figure it does not fix"),

    dict(id="P1-A2", file="QB2_F.html", anchor="-", count=1,
         old='<div><b>Fire main</b>Min 0.27 MPa at monitors</div>',
         new='<div><b>Fire main</b>Min at hydrants, 2 pumps (SOLAS '
             'II-2/10.2.1.6, cargo): 0.27 MPa at 6,000 GT and upwards, '
             '0.25 MPa below</div>',
         why="the same claim on the cheat-card surface, in a <div> - the "
             "element type the previous sweep could not see"),
    # Found by the GENERALISED detector, after the range form was added. The
    # framing is "target", not "minimum", and an operational target is a
    # sanctioned category on this corpus - q2 of this same card says so. What
    # is not sanctioned is a range whose FLOOR is the SOLAS cargo-ship limb,
    # printed at monitors, in a block headed "Numbers & Regulations to
    # Memorise", with no statement of what the regulation actually fixes. The
    # target is kept and the governing minimum is attached beside it, in the
    # wording q2 already carries - propagation of an adjudicated sentence, not
    # a new editorial judgement.
    dict(id="P1-A3", file="QB2_F.html", anchor="q4", count=1,
         old='<li>Run main and emergency fire pumps in parallel, targeting '
             '0.27-0.35 MPa at open-deck monitors.</li>',
         new='<li>Run main and emergency fire pumps in parallel, targeting '
             '0.27–0.35 MPa at open-deck monitors &mdash; an operational '
             'target, not a SOLAS minimum. SOLAS II-2/10.2.1.6 fixes the '
             'minimum at the <strong>hydrants</strong>, both required pumps '
             'delivering simultaneously: 0.27 MPa at 6,000 GT and upwards, '
             '0.25 MPa below.</li>',
         why="a range whose floor is the SOLAS limb, printed at monitors with "
             "no statement of what the regulation fixes"),
    dict(id="P1-A4", file="QB2_F.html", anchor="q4", count=1,
         old='<li>Target fire-main pressure: <strong>0.27-0.35 MPa</strong>'
             '</li>',
         new='<li>Target fire-main pressure at open-deck monitors: '
             '<strong>0.27–0.35 MPa</strong> &mdash; an operational '
             'target. The SOLAS II-2/10.2.1.6 minimum is at the '
             '<strong>hydrants</strong>, both required pumps delivering '
             'simultaneously: <strong>0.27 MPa</strong> at 6,000 GT and '
             'upwards, <strong>0.25 MPa</strong> below.</li>',
         why="the same range in the card's Numbers & Regulations block, the "
             "layer a candidate memorises"),
]

#: P1-B. The banner is located by the topic's STRUCTURAL ID, never by a text
#: needle: "first occurrence of the anchor" is precisely what put it in the
#: wrong topic.
TOPIC_ID = 'topic-46'
TOPIC_OPEN = '<div class="topic-block" id="%s"' % TOPIC_ID
#: Inside that block, the banner goes immediately before the topic's own
#: "Why It Matters" head - the first section a candidate reads after the
#: definition.
IN_TOPIC_ANCHOR = '<div class="section-head">⚓ Why It Matters (CE Perspective)</div>'

BANNER_RX = re.compile(r'<div class="notes-callout"[^>]*>.*?</div>', re.S)


def topic_span(text: str):
    """(start, end) of the topic-46 block, by balanced-div scan from its id."""
    i = text.find(TOPIC_OPEN)
    if i < 0:
        return None
    depth, j, n = 0, i, len(text)
    while j < n:
        if text.startswith("<div", j):
            depth += 1
            j += 4
            continue
        if text.startswith("</div>", j):
            depth -= 1
            j += 6
            if depth == 0:
                break
            continue
        j += 1
    return (i, j)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    problems = []
    for e in EDITS:
        path = QB_ROOT / e["file"]
        text = read_text(path)
        n = text.count(e["old"])
        if n != e["count"]:
            if text.count(e["new"]) > 0:
                print("  %-6s %-26s ALREADY APPLIED" % (e["id"], e["file"]))
                continue
            problems.append("%s: expected %d in %s, found %d"
                            % (e["id"], e["count"], e["file"], n))
            continue
        print("  %-6s %-26s %-4s %s" % (e["id"], e["file"], e["anchor"],
                                        e["why"][:74]))
        if args.apply:
            path.write_bytes(text.replace(e["old"], e["new"])
                             .encode("utf-8").replace(b"\r\n", b"\n"))

    # ---- P1-B : move the banner into topic-46 ---------------------------
    text = read_text(P10)
    span = topic_span(text)
    if span is None:
        problems.append("P1-B: topic-46 block not found")
    else:
        inside = BANNER_RX.search(text[span[0]:span[1]]) is not None
        outside = [m for m in BANNER_RX.finditer(text)
                   if not (span[0] <= m.start() < span[1])]
        if inside and not outside:
            print("  %-6s %-26s ALREADY APPLIED" % ("P1-B", "…-p10.html"))
        else:
            print("  %-6s %-26s %-4s %s"
                  % ("P1-B", "oralnotes/…-p10.html", TOPIC_ID,
                     "banner removed from the UNCLOS Pt XII topic and inserted "
                     "inside topic-46, located by structural id"))
            if args.apply:
                banner = (BANNER_RX.search(text[span[0]:span[1]])
                          or (outside[0] if outside else None))
                if banner is None:
                    problems.append("P1-B: no banner found to move")
                else:
                    blob = banner.group(0)
                    # Remove EVERY banner first, then re-insert exactly one.
                    text = BANNER_RX.sub("", text)
                    span = topic_span(text)
                    k = text.find(IN_TOPIC_ANCHOR, span[0], span[1])
                    if k < 0:
                        problems.append(
                            "P1-B: in-topic anchor not found inside topic-46")
                    else:
                        text = text[:k] + blob + text[k:]
                        P10.write_bytes(text.encode("utf-8")
                                        .replace(b"\r\n", b"\n"))

    if problems:
        print("\nREFUSED - nothing written for these:")
        for p in problems:
            print("  " + p)
        return 1
    print("\n%s: %d replacements + topic-local banner relocation"
          % ("APPLIED" if args.apply else "DRY RUN", len(EDITS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
