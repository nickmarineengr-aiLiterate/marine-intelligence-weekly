"""Phase 2 step 2 - ingest the All-Surveyors external compilation.

The document is evidence of WHAT WAS REPORTED ASKED. It is never authority for
what the correct answer is, and one source occurrence never implies one new
canonical question.

Raw wording is preserved byte-for-byte in `raw_question_text`. Grammar is never
"improved"; the normalised form lives in a separate field.

The .docx is read with the standard library (zipfile + ElementTree) so the tool
carries no third-party dependency. The document path is a CLI argument: the
source file is git-ignored on a public repository and must never be committed.

Usage:
  python tools/oral/ingest_all_surveyors.py --docx "<path to .docx>"

Outputs (meoclass1/oral-intelligence/examiner-audit/):
  ALL_SURVEYORS_SOURCE_RECORDS.jsonl
  ALL_SURVEYORS_SOURCE_FAMILIES.json
  ALL_SURVEYORS_INGESTION_REPORT.json
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

# Only well-supported honorific aliases. Surname resemblance never merges people.
SURVEYOR_ALIASES = {
    "JOHN SIR": "John",
    "JOHN": "John",
    "SIMON SIR": "Simon",
    "SIMON": "Simon",
    "NAIR SIR": "Nair",
    "NAIR": "Nair",
    "PAUL SIR": "Paul",
    "PAUL": "Paul",
}

SURVEYOR_RE = re.compile(r"^Surveyor:\s*(.+?)\s*$", re.I)
TOPIC_RE = re.compile(r"^(\d+)\.\s*(.+?)\s*$")
QUESTION_RE = re.compile(r"^(\d+)[.)]\s*(.+?)\s*$", re.S)
CONTENTS_RE = re.compile(r"\(\s*\d+\s+questions?\s*\)\s*$", re.I)
DECLARED_RE = re.compile(
    r"Surveyor:\s*(.+?)\s*\(\s*(\d+)\s+topics?,\s*(\d+)\s+questions?\s*\)", re.I)
GRAND_TOTAL_RE = re.compile(r"Grand Total Questions:\s*(\d+)", re.I)
TRAILING_PAREN = re.compile(r"\(([^()]*)\)\s*$")


def para_text(p):
    return "".join(t.text or "" for t in p.iter(W + "t"))


def para_style(p):
    st = p.find(W + "pPr/" + W + "pStyle")
    return st.get(W + "val") if st is not None else ""


def has_page_break(p):
    return any(b.get(W + "type") == "page" for b in p.iter(W + "br"))


def parse_docx(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")
    paras = [c for c in body if c.tag == W + "p"]

    records = []
    declared = []          # contents-page headline claims, for cross-check
    section_topic_claims = []
    surveyor_raw = surveyor = topic_raw = None
    topic_number = None
    page = 1
    seq = 0
    in_topics_list = False
    seen_first_topic = False

    for i, p in enumerate(paras):
        if has_page_break(p):
            page += 1
        text = para_text(p).replace(" ", " ").strip()
        if not text:
            continue
        style = para_style(p)

        dm = DECLARED_RE.search(text)
        if dm and surveyor_raw is None:
            declared.append({
                "paragraph": i,
                "text": text,
                "surveyor_raw": dm.group(1).strip(),
                "declared_topics": int(dm.group(2)),
                "declared_questions": int(dm.group(3)),
            })
            continue
        gm = GRAND_TOTAL_RE.search(text)
        if gm and surveyor_raw is None:
            declared.append({"paragraph": i, "text": text,
                             "grand_total_declared": int(gm.group(1))})
            continue

        m = SURVEYOR_RE.match(text)
        if m:
            surveyor_raw = m.group(1).strip()
            surveyor = SURVEYOR_ALIASES.get(surveyor_raw.upper())
            topic_raw = None
            topic_number = None
            seen_first_topic = False
            in_topics_list = False
            continue

        if style == "Heading2":
            # "Contents" (document level) or "Topics in this section"
            in_topics_list = True
            continue

        if style == "Heading1":
            tm = TOPIC_RE.match(text)
            topic_number = int(tm.group(1)) if tm else None
            topic_raw = tm.group(2).strip() if tm else text
            seen_first_topic = True
            in_topics_list = False
            continue

        # contents / per-section topic listings: "3. STCW & Manning  (6 questions)"
        if CONTENTS_RE.search(text):
            entry = {"paragraph": i, "text": text, "surveyor_raw": surveyor_raw}
            (declared if surveyor_raw is None else section_topic_claims).append(entry)
            continue

        if in_topics_list and not seen_first_topic:
            continue
        if surveyor is None or topic_raw is None:
            continue

        qm = QUESTION_RE.match(text)
        if not qm:
            continue

        seq += 1
        raw = qm.group(2)
        comment = None
        core = raw
        pm = TRAILING_PAREN.search(raw)
        if pm and len(pm.group(1).split()) >= 2:
            comment = pm.group(1).strip()
            core = raw[: pm.start()].strip()

        records.append({
            "source_id": "ASC-%04d" % seq,
            "surveyor_raw": surveyor_raw,
            "surveyor_normalized": surveyor,
            "topic_raw": topic_raw,
            "topic_number": topic_number,
            "source_question_number": int(qm.group(1)),
            "raw_question_text": raw,
            "question_core_text": core,
            "source_comment": comment,
            "source_page": page,
            "source_paragraph": i,
            "source_sequence": seq,
            "source_type": "ALL_SURVEYORS_COMPILATION",
            "source_provenance": Path(path).name,
            "source_confidence": (
                "TERSE_PROMPT" if len(L.tokens(core)) <= 2 else "REPORTED_ASK"
            ),
            "normalization_notes": (
                "trailing parenthetical lifted into source_comment"
                if comment else ""
            ),
        })

    return records, declared, section_topic_claims


def build_families(records):
    """Cluster near-identical source wordings without discarding any occurrence."""
    fams = []
    by_norm = defaultdict(list)
    for r in records:
        by_norm[L.norm(r["question_core_text"])].append(r)

    keys = list(by_norm)
    assigned = {}
    for k in keys:
        if k in assigned:
            continue
        members = [k]
        assigned[k] = k
        for k2 in keys:
            if k2 in assigned or k2 == k:
                continue
            # merge only on strong containment of the shorter token set
            if L.containment(k, k2) >= 0.85 and L.jaccard(k, k2) >= 0.6:
                assigned[k2] = k
                members.append(k2)
        fams.append((k, members))

    out = []
    for n, (key, members) in enumerate(sorted(fams, key=lambda f: -sum(len(by_norm[m]) for m in f[1])), 1):
        occ = [r for m in members for r in by_norm[m]]
        occ.sort(key=lambda r: r["source_sequence"])
        examiners = sorted({r["surveyor_normalized"] for r in occ})
        fid = "ASF-%04d" % n
        for r in occ:
            r["source_family_id"] = fid
        out.append({
            "family_id": fid,
            "representative_text": max((r["question_core_text"] for r in occ), key=len),
            "occurrence_count": len(occ),
            "source_ids": [r["source_id"] for r in occ],
            "examiners_supported": examiners,
            "examiner_count": len(examiners),
            "topics": sorted({r["topic_raw"] for r in occ}),
            "distinct_wordings": len(members),
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx", required=True, help="path to the All-Surveyors .docx")
    a = ap.parse_args()

    records, declared, section_claims = parse_docx(a.docx)
    families = build_families(records)

    per_examiner = Counter(r["surveyor_normalized"] for r in records)
    topic_counts = Counter((r["surveyor_normalized"], r["topic_raw"]) for r in records)

    # cross-check the document's own headline claims against what parsing found
    claimed = {}
    grand_total_declared = None
    for d in declared:
        if "grand_total_declared" in d:
            grand_total_declared = d["grand_total_declared"]
            continue
        name = SURVEYOR_ALIASES.get(d["surveyor_raw"].upper(), d["surveyor_raw"])
        claimed[name] = {
            "declared_topics": d["declared_topics"],
            "declared_questions": d["declared_questions"],
        }

    OUT = L.OUT
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "ALL_SURVEYORS_SOURCE_RECORDS.jsonl").open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    L.jdump(families, "ALL_SURVEYORS_SOURCE_FAMILIES.json")

    report = {
        "source_document": Path(a.docx).name,
        "raw_source_occurrences_parsed": len(records),
        "normalized_source_families": len(families),
        "per_examiner_parsed": dict(per_examiner),
        "per_examiner_declared_by_document": claimed,
        "declared_grand_total_in_document": grand_total_declared,
        "declared_per_examiner_sum": sum(v["declared_questions"] for v in claimed.values()),
        "parse_matches_declared": {
            k: (per_examiner.get(k, 0) == v["declared_questions"]) for k, v in claimed.items()
        },
        "topics_parsed": len({(e, t) for e, t in topic_counts}),
        "declared_topics_sum": sum(v["declared_topics"] for v in claimed.values()),
        "pages_spanned": max(r["source_page"] for r in records) if records else 0,
        "occurrences_with_source_comment": sum(1 for r in records if r["source_comment"]),
        "terse_prompts": sum(1 for r in records if r["source_confidence"] == "TERSE_PROMPT"),
        "multi_examiner_families": sum(1 for f in families if f["examiner_count"] > 1),
        "families_by_occurrence": dict(Counter(f["occurrence_count"] for f in families)),
    }
    L.jdump(report, "ALL_SURVEYORS_INGESTION_REPORT.json")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
