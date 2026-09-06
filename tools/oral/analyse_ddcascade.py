"""Analyse the deep-dive suffix-cascade defect, and PROVE the repair is lossless.

The defect. A markdown-to-HTML conversion split one deep-dive blob into typed
`dd-block` divs by taking the tail from each `* <strong>Label:</strong>` marker
ONWARD, instead of the segment BETWEEN markers. Every block therefore renders
its own content plus every following section, still in raw markdown, to the
candidate. `dd-trap` shows four extra sections, `dd-fail` three, and so on.

Why this is repairable mechanically and not a rewrite. If the conversion really
took suffixes, then every section hanging off block N is byte-identical to the
OWN body of the later typed block that carries the same label. Truncating each
block at its first stray marker therefore DELETES ONLY TEXT THAT SURVIVES
VERBATIM IN A LATER BLOCK ON THE SAME CARD. Nothing is invented, nothing is
lost, and the candidate-visible set of propositions is unchanged - only the
duplication goes.

That is a claim about the bytes, so this tool checks it for every stray section
on every candidate BEFORE anything is written, and reports any block where it
does not hold. A block that fails the check is NOT repaired: recovering it would
be a content decision, which belongs to a human and not to a sweep.

The match is by LABEL, never by position. The blocks are not emitted in the same
order as the markdown sections - `dd-chain` sits between `dd-casualty` and
`dd-vessel` - so a positional comparison reports a false mismatch on every card.
"""
from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
QB_ROOT = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import read_text  # noqa: E402

CARD_OPEN = re.compile(r'<div class="q-card" id="(q\d+)"')

DD_BLOCK = re.compile(
    r'<div class="dd-block ([a-z-]+)">'
    r'<strong class="dd-label">(.*?)</strong>'
    r'<p>(.*?)</p></div>',
    re.S)

#: The stray marker the conversion left behind, at the start of a line.
STRAY = re.compile(r'\n\*\s+<strong>([^<]{2,60}?):</strong>\s*')

#: A markdown section label -> the dd-block class that owns that section.
#: Derived from the labels actually present in the corpus, not invented.
LABEL_TO_CLASS = {
    "ce relevance": "dd-relevance",
    "trap questions": "dd-trap",
    "common ce failures": "dd-fail",
    "numbers to memorise": "dd-numbers",
    "numbers and regulations to memorise": "dd-numbers",
    "casualty link": "dd-casualty",
    "examiner chain": "dd-chain",
    "on my vessel": "dd-vessel",
}


def norm(s: str) -> str:
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def card_spans(text: str):
    out = []
    for m in CARD_OPEN.finditer(text):
        start, depth, i, n = m.start(), 0, m.start(), len(text)
        while i < n:
            if text.startswith("<div", i):
                depth += 1
                i += 4
                continue
            if text.startswith("</div>", i):
                depth -= 1
                i += 6
                if depth == 0:
                    break
                continue
            i += 1
        out.append((m.group(1), start, i))
    return out


def split_stray(body: str):
    """(own_body, [(label, text), ...]) for one dd-block body."""
    first = STRAY.search(body)
    if not first:
        return body, []
    own = body[:first.start()]
    tail = body[first.start():]
    pairs, cursor, cur = [], None, None
    for m in STRAY.finditer(tail):
        if cur is not None:
            pairs.append((cur, tail[cursor:m.start()]))
        cur, cursor = m.group(1), m.end()
    if cur is not None:
        pairs.append((cur, tail[cursor:]))
    return own, pairs


def analyse_card(fname: str, anchor: str, block: str, base_line: int):
    blocks = []
    for m in DD_BLOCK.finditer(block):
        own, strays = split_stray(m.group(3))
        blocks.append({
            "cls": m.group(1),
            "label": norm(m.group(2)),
            "own": own,
            "strays": strays,
            "offset": m.start(),
            "full": m.group(3),
        })
    own_by_class = {b["cls"]: b["own"] for b in blocks}

    rows = []
    for b in blocks:
        if not b["strays"]:
            continue
        detail, lossless = [], True
        for lab, txt in b["strays"]:
            key = norm(lab).lower().replace("&", "and")
            cls = LABEL_TO_CLASS.get(key)
            if cls is None:
                lossless = False
                detail.append("%s: UNMAPPED LABEL" % lab)
                continue
            if cls not in own_by_class:
                lossless = False
                detail.append("%s: no %s block on this card" % (lab, cls))
                continue
            if norm(txt) != norm(own_by_class[cls]):
                lossless = False
                detail.append("%s: text differs from %s own body" % (lab, cls))
        rows.append({
            "file": fname,
            "card": anchor,
            "line": base_line + block.count("\n", 0, b["offset"]),
            "dd_class": b["cls"],
            "label": b["label"],
            "stray_sections": [s[0] for s in b["strays"]],
            "lossless": lossless,
            "detail": detail,
            "bytes_removed": len(b["full"]) - len(b["own"]),
        })
    return rows


def analyse(path: pathlib.Path):
    text = read_text(path)
    rows = []
    for anchor, s, e in card_spans(text):
        rows.extend(analyse_card(path.name, anchor, text[s:e],
                                 text.count("\n", 0, s) + 1))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", metavar="PATH")
    args = ap.parse_args()

    rows = []
    for p in sorted(QB_ROOT.glob("*.html")):
        rows.extend(analyse(p))

    files, cards, lossless, lossy = {}, set(), 0, []
    for r in rows:
        files[r["file"]] = files.get(r["file"], 0) + 1
        cards.add((r["file"], r["card"]))
        if r["lossless"]:
            lossless += 1
        else:
            lossy.append(r)

    print("cascaded dd-blocks found : %d  across %d cards" % (len(rows), len(cards)))
    print("  provably lossless      : %d" % lossless)
    print("  NOT provably lossless  : %d" % len(lossy))
    print("  duplicated bytes       : %d" % sum(r["bytes_removed"] for r in rows))
    print("\nby file:")
    for f, n in sorted(files.items(), key=lambda t: -t[1]):
        ncards = len({c for c in cards if c[0] == f})
        print("  %-26s %3d blocks / %2d cards" % (f, n, ncards))
    if lossy:
        print("\nNOT PROVABLY LOSSLESS - excluded from any mechanical repair:")
        for r in lossy:
            print("  %s#%s L%s %s :: %s" % (r["file"], r["card"], r["line"],
                                            r["dd_class"],
                                            "; ".join(r["detail"])[:200]))
    if args.json:
        pathlib.Path(args.json).write_bytes(
            json.dumps(rows, indent=1, ensure_ascii=False).encode("utf-8"))
        print("\nwrote %s" % args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
