"""Re-derive the historical 788 from the .docx by an INDEPENDENT method.

`ingest_all_surveyors.py` segments the document with regex precedence over a
linear scan. This tool segments it by Word paragraph STYLE instead: `Heading1`
marks a topic header, so the topic/question ambiguity ("1. MARPOL ..." vs
"1. CLC ...") is resolved from the document's own structure rather than from
rule ordering. A defect shared by both would have to exist in a regex AND in a
style tree.

It then asserts the committed source records agree occurrence-for-occurrence.
This is the guard that the historical denominator is evidence-derived: if a
future re-ingest silently drops or rewrites a row, the two methods diverge.

The .docx is git-ignored, so this runs only where the source is present.

  python tools/oral/verify_788_independent.py --docx "<path>"
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
EXPECTED = 788

SECTION_RE = re.compile(r"^Surveyor:\s*([A-Z][A-Za-z ]+?)\s*$")
NUMBERED_RE = re.compile(r"^(\d+)[.)]\s+(.*)$", re.S)
DECLARED_RE = re.compile(
    r"^\d+\.\s*Surveyor:\s*(.+?)\s*\(\s*(\d+)\s+topics?,\s*(\d+)\s+questions?\s*\)\s*$")
GRAND_RE = re.compile(r"^Grand Total Questions:\s*(\d+)\s*$")
TOPIC_HEAD_RE = re.compile(r"^(\d+)\.\s*(.+?)\s*$")


def txt(p):
    return "".join(t.text or "" for t in p.iter(W + "t"))


def style(p):
    s = p.find(W + "pPr/" + W + "pStyle")
    return s.get(W + "val") if s is not None else ""


def reconstruct(docx):
    paras = [c for c in ET.fromstring(
        zipfile.ZipFile(docx).read("word/document.xml")).find(W + "body")
        if c.tag == W + "p"]

    declared, grand, occ = {}, None, []
    surveyor = topic = topic_no = None
    in_topic = False

    for idx, p in enumerate(paras):
        t = txt(p).strip()
        if not t:
            continue
        st = style(p)

        m = DECLARED_RE.match(t)
        if m:
            declared[m.group(1).strip()] = (int(m.group(2)), int(m.group(3)))
            continue
        m = GRAND_RE.match(t)
        if m:
            grand = int(m.group(1))
            continue
        m = SECTION_RE.match(t)
        if m and "(" not in t:
            surveyor, in_topic, topic = m.group(1).strip(), False, None
            continue
        if st == "Heading1":
            hm = TOPIC_HEAD_RE.match(t)
            topic_no = int(hm.group(1)) if hm else None
            topic = hm.group(2) if hm else t
            in_topic = True
            continue
        if st == "Heading2":
            in_topic = False       # suppresses the contents / section TOC lists
            continue
        if not in_topic:
            continue
        qm = NUMBERED_RE.match(t)
        if qm:
            occ.append({"seq": len(occ) + 1, "surveyor": surveyor,
                        "topic_number": topic_no, "topic": topic,
                        "q_number": int(qm.group(1)),
                        "raw_text": qm.group(2).strip(), "para_index": idx})

    return occ, declared, grand, paras


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx", required=True)
    a = ap.parse_args()

    occ, declared, grand, paras = reconstruct(a.docx)
    per = Counter(o["surveyor"] for o in occ)

    fails = []

    def check(name, ok, detail=""):
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
        if not ok:
            fails.append(name)

    check("I1_reconstructed_count_is_788", len(occ) == EXPECTED, f"{len(occ)}")
    check("I2_matches_document_grand_total", grand == len(occ), f"declared {grand}")
    check("I3_matches_declared_per_surveyor",
          all(per[k] == v[1] for k, v in declared.items()),
          f"{dict(per)}")
    check("I4_topic_headings_match_declared",
          sum(1 for p in paras if style(p) == "Heading1")
          == sum(v[0] for v in declared.values()),
          f"{sum(v[0] for v in declared.values())} topics")

    # per-topic numbering must run 1..N with no gap or repeat
    bytopic = defaultdict(list)
    for o in occ:
        bytopic[(o["surveyor"], o["topic_number"])].append(o["q_number"])
    breaks = [k for k, n in bytopic.items() if n != list(range(1, len(n) + 1))]
    check("I5_per_topic_numbering_contiguous", not breaks, f"{breaks[:3]}")

    # agreement with the committed store, occurrence for occurrence
    src = [json.loads(x) for x in
           (L.OUT / "ALL_SURVEYORS_SOURCE_RECORDS.jsonl")
           .read_text(encoding="utf-8").splitlines() if x.strip()]
    check("I6_committed_store_same_length", len(src) == len(occ),
          f"committed {len(src)} vs independent {len(occ)}")

    if len(src) == len(occ):
        raw_mm = [o["seq"] for o, s in zip(occ, src)
                  if o["raw_text"] != s["raw_question_text"]]
        pos_mm = [o["seq"] for o, s in zip(occ, src)
                  if o["surveyor"] != s["surveyor_raw"]
                  or o["q_number"] != s["source_question_number"]
                  or o["topic_number"] != s["topic_number"]]
        check("I7_raw_wording_identical", not raw_mm, f"{len(raw_mm)} differ")
        check("I8_position_identical", not pos_mm, f"{len(pos_mm)} differ")

    print(f"\n{'ALL INDEPENDENT CHECKS PASS' if not fails else 'FAILED: ' + str(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
