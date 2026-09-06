"""Apply the deep-dive suffix-cascade repair, and the empty deep-dive removal.

Two structural defects, one conversion generation, no content authored.

1. CASCADE. A markdown-to-HTML conversion took the tail from each
   `* <strong>Label:</strong>` marker ONWARD instead of the segment BETWEEN
   markers, so every typed `dd-block` renders its own content plus every
   following section as raw markdown. The repair truncates each block at its
   first stray marker. `analyse_ddcascade.py` proves, for every block, that the
   removed text is byte-identical to the OWN body of the later typed block that
   carries the same label - so the repair deletes only duplication.

   This applier REFUSES to touch a block the analyser has not proved lossless.
   A block that fails the proof would need its content recovered by a human;
   a sweep must not guess.

2. EMPTY PROMISE. Six `<details class="deep-dive">` elements carry a summary
   promising seven sections and an empty body. The instruction is explicit: an
   empty block with no trustworthy source content has its promise REMOVED
   rather than an answer fabricated. So the element goes; nothing is written in
   its place.

Idempotent: a second run finds no cascade and no empty promise, and reports
zero changes. Writes LF bytes explicitly - `write_text` on Windows would
translate every newline to CRLF and turn nine unrelated validators red.
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

from oral_bytes import read_text            # noqa: E402
from analyse_ddcascade import (             # noqa: E402
    DD_BLOCK, split_stray, analyse, card_spans, norm,
)

EMPTY_DETAILS = re.compile(
    r'\n?\s*<details class="deep-dive"><summary>[^<]*</summary></details>')


def repair_file(path: pathlib.Path, dry: bool):
    text = read_text(path)
    original = text

    # --- 1. cascade ------------------------------------------------------
    proved = {(r["file"], r["card"], r["dd_class"], r["label"])
              for r in analyse(path) if r["lossless"]}
    refused = [r for r in analyse(path) if not r["lossless"]]

    out, cursor, n_blocks, n_bytes = [], 0, 0, 0
    spans = card_spans(text)

    def card_of(pos):
        for anchor, s, e in spans:
            if s <= pos < e:
                return anchor
        return "-"

    for m in DD_BLOCK.finditer(text):
        own, strays = split_stray(m.group(3))
        if not strays:
            continue
        # `norm` is imported from the analyser, never re-implemented: the
        # applier's key must be the SAME string the proof was recorded under,
        # or a label carrying an entity ("Numbers &amp; Regulations") silently
        # fails to match and the block is skipped without anyone noticing.
        label = norm(m.group(2))
        key = (path.name, card_of(m.start()), m.group(1), label)
        if key not in proved:
            continue
        rebuilt = ('<div class="dd-block %s"><strong class="dd-label">%s</strong>'
                   '<p>%s</p></div>' % (m.group(1), m.group(2), own.rstrip()))
        out.append(text[cursor:m.start()])
        out.append(rebuilt)
        cursor = m.end()
        n_blocks += 1
        n_bytes += (m.end() - m.start()) - len(rebuilt)
    out.append(text[cursor:])
    text = "".join(out)

    # --- 2. empty promise ------------------------------------------------
    text, n_empty = EMPTY_DETAILS.subn("", text)

    changed = text != original
    if changed and not dry:
        path.write_bytes(text.encode("utf-8").replace(b"\r\n", b"\n"))
    return {
        "file": path.name,
        "cascade_blocks": n_blocks,
        "cascade_bytes": n_bytes,
        "empty_details": n_empty,
        "refused": len(refused),
        "changed": changed,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="write the repair (default is a dry run)")
    args = ap.parse_args()

    total = {"cascade_blocks": 0, "cascade_bytes": 0, "empty_details": 0,
             "refused": 0, "files": 0}
    for p in sorted(QB_ROOT.glob("*.html")):
        r = repair_file(p, dry=not args.apply)
        if not r["changed"] and not r["refused"]:
            continue
        total["files"] += 1 if r["changed"] else 0
        for k in ("cascade_blocks", "cascade_bytes", "empty_details", "refused"):
            total[k] += r[k]
        print("  %-26s cascade=%3d (-%5d B)  empty_details=%d  refused=%d"
              % (r["file"], r["cascade_blocks"], r["cascade_bytes"],
                 r["empty_details"], r["refused"]))

    print("\n%s: %d files, %d cascaded blocks truncated (-%d bytes), "
          "%d empty deep-dive promises removed, %d blocks REFUSED as unproven"
          % ("APPLIED" if args.apply else "DRY RUN", total["files"],
             total["cascade_blocks"], total["cascade_bytes"],
             total["empty_details"], total["refused"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
