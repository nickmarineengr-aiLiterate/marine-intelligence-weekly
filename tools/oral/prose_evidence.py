"""Harvest examiner attribution that already sits in the live q-card prose
(CE Oral Tip blocks and other in-card mentions) and diff it against the
connections examiner-index.html actually shows.

This is repo-native evidence: it needs no workbook and no new authoring.
Strength is graded, because an in-card mention is not automatically a claim
that the examiner asked THIS question - it may be comparative prose.
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
import verify_tiers as V  # noqa: E402

# phrasing that asserts this examiner asks this question
ASSERTIVE = re.compile(
    r"\b(asks?|asked|favourite|favorite|wants?|expects?|presses?|pushes?|"
    r"insists?|drills?|follows? up|will ask|has asked|likes? to ask|"
    r"specifically|invariably|always asks)\b",
    re.I,
)
# phrasing that merely contrasts examiners
COMPARATIVE = re.compile(r"\b(unlike|whereas|compared with|as opposed to|rather than)\b", re.I)
# illustrative phrasing: names the examiner as an EXAMPLE of a type, which is
# weaker than naming them as the asker of this particular question
HEDGED = re.compile(
    r"\b(examiners?\s+(?:like|such as)|like\s+Capt\.?\s|such as\s+Capt\.?\s)", re.I
)


def tip_windows(block):
    out = []
    for tm in V.TIPBLOCK.finditer(block):
        out.append(L.strip_tags(block[tm.start(): tm.start() + 1400]))
    return out


def main():
    inv = L.build_inventory()
    by_qid = {r["canonical_question_id"]: r for r in inv}

    ix = L.parse_examiner_index(L.MEO / "examiner-index.html")
    idx = collections.defaultdict(set)
    for r in ix["rows"]:
        f, a = L.split_href(r["href"])
        idx[Path(f).stem + "#" + a].add(r["examiner_raw"])

    rows = []
    for p in L.qb_files():
        cards, _ = V.card_blocks(p)
        for anchor, block in cards.items():
            if not re.fullmatch(r"q\d+", anchor or ""):
                continue
            qid = p.stem + "#" + anchor
            tips = tip_windows(block)
            plain = L.strip_tags(block)
            for name, rx in V.NAME_RE.items():
                if not rx.search(block):
                    continue
                in_tip = any(rx.search(t) for t in tips)
                # sentence around the first mention, for adjudication
                m = rx.search(plain)
                ctx = plain[max(0, m.start() - 160): m.start() + 200] if m else ""
                assertive = bool(ASSERTIVE.search(ctx))
                comparative = bool(COMPARATIVE.search(ctx))
                hedged = bool(HEDGED.search(ctx))
                if in_tip and assertive and not comparative and not hedged:
                    strength = "STRONG_CE_TIP_ASSERTION"
                elif in_tip and hedged:
                    strength = "SUPPORTED_ILLUSTRATIVE_CE_TIP"
                elif in_tip and not comparative:
                    strength = "SUPPORTED_CE_TIP_MENTION"
                elif comparative:
                    strength = "WEAK_COMPARATIVE_MENTION"
                else:
                    strength = "WEAK_INCIDENTAL_MENTION"
                rows.append(
                    {
                        "canonical_question_id": qid,
                        "url": by_qid[qid]["url"] if qid in by_qid else "",
                        "examiner": name,
                        "in_ce_tip_block": in_tip,
                        "assertive_phrasing": assertive,
                        "hedged_illustrative": hedged,
                        "comparative_phrasing": comparative,
                        "strength": strength,
                        "already_in_index": name in idx.get(qid, set()),
                        "context": ctx.strip()[:300],
                        "question_text": by_qid[qid]["question_text"] if qid in by_qid else "",
                    }
                )

    gaps = [r for r in rows if not r["already_in_index"]]
    by_strength = collections.Counter(r["strength"] for r in rows)
    gap_strength = collections.Counter(r["strength"] for r in gaps)
    ready = [r for r in gaps if r["strength"] == "STRONG_CE_TIP_ASSERTION"]
    review = [r for r in gaps if r["strength"].startswith("SUPPORTED_")]

    L.OUT.mkdir(parents=True, exist_ok=True)
    keys = list(rows[0])
    with (L.OUT / "PROSE_EXAMINER_EVIDENCE.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    with (L.OUT / "PROSE_CONNECTION_GAPS.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(gaps)

    rep = {
        "in_card_examiner_mentions": len(rows),
        "distinct_questions_with_a_mention": len({r["canonical_question_id"] for r in rows}),
        "mentions_by_strength": dict(by_strength),
        "mentions_already_connected_by_index": sum(1 for r in rows if r["already_in_index"]),
        "mentions_NOT_connected_by_index": len(gaps),
        "gaps_by_strength": dict(gap_strength),
        "gaps_by_examiner": dict(collections.Counter(r["examiner"] for r in gaps)),
        "READY_CONNECTION_strong": len(ready),
        "ready_strong_by_examiner": dict(collections.Counter(r["examiner"] for r in ready)),
        "NEEDS_MATCH_REVIEW_supported": len(review),
    }
    L.jdump(rep, "PROSE_EVIDENCE_SUMMARY.json")
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()
