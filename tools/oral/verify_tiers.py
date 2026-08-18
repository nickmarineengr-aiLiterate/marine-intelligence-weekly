"""Test whether each examiner-index tier is still reproducible from the
metadata the live pages actually carry.

  confirmed -> claimed to come from candidate/tracker records
  ce_tip    -> claimed to come from a named CE Oral Tip on the q-card
  header    -> claimed to come from page-level examiner metadata
  inferred  -> topic fallback, no page evidence expected

For each tier this asks the only question that matters for regeneration:
can the tag be re-derived today from the repo alone?
"""
from __future__ import annotations

import collections
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

NAMES = ["Nair", "Simon", "Rajappan", "Srivastava", "Senthil", "Paul", "John"]
NAME_RE = {n: re.compile(r"\b" + n + r"\b", re.I) for n in NAMES}
TIPBLOCK = re.compile(r"(ce[\s-]*oral[\s-]*tip|examiner[\s-]*tip)", re.I)


def card_blocks(path):
    """anchor -> raw html of that q-card, plus the page-level preamble."""
    h = path.read_text(encoding="utf-8", errors="replace")
    ms = list(L.CARD.finditer(h))
    out = {}
    for i, m in enumerate(ms):
        attrs = dict(L.ATTR.findall(m.group(1)))
        end = ms[i + 1].start() if i + 1 < len(ms) else len(h)
        out[attrs.get("id", "")] = h[m.start():end]
    preamble = h[: ms[0].start()] if ms else h
    return out, preamble


def main():
    ix = L.parse_examiner_index(L.MEO / "examiner-index.html")
    cache = {}
    rows = []
    for r in ix["rows"]:
        fname, anchor = L.split_href(r["href"])
        if fname not in cache:
            p = L.MEO / fname
            cache[fname] = card_blocks(p) if p.exists() else ({}, "")
        cards, preamble = cache[fname]
        block = cards.get(anchor, "")
        ex = r["examiner_raw"]
        rx = NAME_RE.get(ex)
        in_card = bool(rx and rx.search(block))
        tipmatch = False
        if rx and block:
            for tm in TIPBLOCK.finditer(block):
                if rx.search(block[tm.start(): tm.start() + 1200]):
                    tipmatch = True
                    break
        in_preamble = bool(rx and rx.search(preamble))
        rows.append(
            {
                "examiner": ex,
                "tier": r["tier"],
                "canonical_question_id": Path(fname).stem + "#" + anchor,
                "examiner_named_in_qcard": in_card,
                "examiner_named_in_ce_tip": tipmatch,
                "examiner_named_in_page_preamble": in_preamble,
                "reproducible_from_repo": in_card or in_preamble,
            }
        )

    per_tier = collections.defaultdict(collections.Counter)
    for r in rows:
        t = per_tier[r["tier"]]
        t["rows"] += 1
        t["named_in_qcard"] += r["examiner_named_in_qcard"]
        t["named_in_ce_tip"] += r["examiner_named_in_ce_tip"]
        t["named_in_preamble"] += r["examiner_named_in_page_preamble"]
        t["reproducible"] += r["reproducible_from_repo"]

    report = {
        "tiers": {k: dict(v) for k, v in sorted(per_tier.items())},
        "verdict": {},
    }
    for tier, c in per_tier.items():
        pct = round(100 * c["reproducible"] / c["rows"], 1)
        if tier == "inferred":
            expect = "no page evidence expected"
        else:
            expect = "page evidence expected"
        report["verdict"][tier] = {
            "rows": c["rows"],
            "reproducible_pct": pct,
            "expectation": expect,
            "status": "REPRODUCIBLE" if pct >= 90 else "NOT_REPRODUCIBLE",
        }
    L.jdump(report, "TIER_REPRODUCIBILITY.json")

    keys = list(rows[0])
    with (L.OUT / "TIER_EVIDENCE_ROWS.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
