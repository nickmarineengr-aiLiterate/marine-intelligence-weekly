"""Ingest fresh candidate oral submissions from the current sitting window.

This is the CURRENT-INTAKE lane. It is deliberately a separate denominator from
the historical All-Surveyors compilation (788 raw occurrences, ASC-*). Fresh
occurrences are AUG-* and must never be added to the historical count.

Raw wording is evidence and is preserved verbatim in `raw_question_text`.
Normalisation lives in a separate field and never overwrites the raw form.

A numbered line that is not a question (a candidate recording that they forgot
one) is still an occurrence: it is preserved and dispositioned as
NON_QUESTION_UNRECOVERABLE so that nothing silently vanishes from the count.

The submission file itself is git-ignored, exactly like the historical .docx:
only the derived per-occurrence records are committed.

Usage:
  python tools/oral/ingest_august_intake.py --txt "<path>" [--check]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

OUT = L.OUT
RECORDS = OUT / "AUGUST2026_INTAKE_RECORDS.jsonl"
REPORT = OUT / "AUGUST2026_INTAKE_REPORT.json"

# "Ext- Rajappan sir" / "Int- Senthil sir"
ROLE_RE = re.compile(r"^(Ext|Int|External|Internal)\s*[-:]\s*(.+?)\s*$", re.I)
# "1. text" / "2. <U+2060>text"  (the source uses invisible separators after the dot)
Q_RE = re.compile(r"^(\d+)[.)]\s*(.*)$", re.S)
ATTEMPT_RE = re.compile(r"^Attempt\s+(\d+)\s*$", re.I)
RESULT_RE = re.compile(r"^Result\s*[-:]\s*(.+?)\s*$", re.I)
RULE_RE = re.compile(r"^[-]{3,}$")

ROLE_NORM = {"ext": "EXTERNAL", "external": "EXTERNAL",
             "int": "INTERNAL", "internal": "INTERNAL"}

# Invisible characters the messaging app inserted; stripped for the NORMALISED
# form only. The raw field keeps them so the evidence stays byte-faithful.
INVISIBLE = dict.fromkeys(map(ord, "⁠​‌‍﻿"), None)

NON_QUESTION_CUES = ("i forgot", "forgot", "don't remember", "didn't know")


def normalise(raw: str) -> str:
    return L._WS.sub(" ", raw.translate(INVISIBLE)).strip()


def looks_like_non_question(text: str) -> bool:
    low = normalise(text).lower()
    return any(c in low for c in NON_QUESTION_CUES) and "?" not in low


def normalise_examiner(raw: str) -> str:
    """Strip trailing punctuation and the honorific. Never merges by surname
    resemblance: it only removes decoration the candidate typed."""
    s = raw.strip().rstrip(",.;:").strip()
    s = re.sub(r"\s+sir$", "", s, flags=re.I).strip()
    return s


def parse_submission(lines, submission_id: str, seq_start: int):
    examiners, occurrences = [], []
    attempt_no = result = None
    preamble = []

    for ln in lines:
        t = ln.strip()
        if not t or RULE_RE.match(t):
            continue

        m = ROLE_RE.match(t)
        if m and not Q_RE.match(t):
            examiners.append({
                "role": ROLE_NORM[m.group(1).lower()],
                "name_raw": m.group(2).strip(),
                "name_normalized": normalise_examiner(m.group(2)),
                "attribution_basis": "EXPLICITLY_STATED_BY_CANDIDATE",
            })
            continue

        m = ATTEMPT_RE.match(t)
        if m:
            attempt_no = int(m.group(1))
            continue

        m = RESULT_RE.match(t)
        if m:
            result = m.group(1).strip()
            continue

        m = Q_RE.match(t)
        if m:
            raw = m.group(2)
            occurrences.append({
                "occurrence_id": f"AUG-{seq_start + len(occurrences):04d}",
                "submission_id": submission_id,
                "source_question_number": int(m.group(1)),
                "raw_question_text": raw,
                "normalised_question_text": normalise(raw),
                "is_question": not looks_like_non_question(raw),
            })
            continue

        preamble.append(t)

    for o in occurrences:
        o["attempt_number"] = attempt_no
        o["attempt_result"] = result
        # Both examiners sat the same panel; neither can be tied to one question.
        o["examiner_attribution"] = "PANEL_LEVEL_ONLY"
        o["examiners"] = [e["name_normalized"] for e in examiners]

    return {
        "submission_id": submission_id,
        "source_type": "CANDIDATE_SITTING_REPORT",
        "received_date": "2026-08-24",
        "attempt_date": "2026-08-24",
        "attempt_number": attempt_no,
        "attempt_result": result,
        "examiners": examiners,
        "candidate_reference": "ANONYMOUS_UNNAMED_IN_SOURCE",
        "context_comments": preamble,
        "occurrences": occurrences,
    }


def parse_file(path: Path):
    """One file may carry several candidate reports separated by rule lines."""
    blocks, cur = [], []
    for ln in path.read_text(encoding="utf-8").splitlines():
        if RULE_RE.match(ln.strip()):
            blocks.append(cur)
            cur = []
        else:
            cur.append(ln)
    blocks.append(cur)

    subs, seq = [], 1
    for blk in blocks:
        if not any(Q_RE.match(l.strip()) for l in blk):
            continue
        s = parse_submission(blk, f"AUG2026-S{len(subs) + 1:03d}", seq)
        s["source_file"] = path.name
        seq += len(s["occurrences"])
        subs.append(s)
    return subs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--txt", required=True)
    ap.add_argument("--check", action="store_true",
                    help="verify committed records still match the source")
    a = ap.parse_args()

    subs = parse_file(Path(a.txt))
    occ = [o for s in subs for o in s["occurrences"]]

    roles = {}
    for s in subs:
        for e in s["examiners"]:
            roles.setdefault(e["name_normalized"], e["role"])

    report = {
        "denominator_class": "CURRENT_AUGUST_INTAKE",
        "isolated_from_historical_788": True,
        "submissions": len(subs),
        "raw_occurrences": len(occ),
        "question_bearing_occurrences": sum(1 for o in occ if o["is_question"]),
        "non_question_occurrences": sum(1 for o in occ if not o["is_question"]),
        "examiners_represented": sorted(roles),
        "examiner_roles": roles,
        "per_submission": [
            {"submission_id": s["submission_id"],
             "raw_occurrences": len(s["occurrences"]),
             "attempt_number": s["attempt_number"],
             "attempt_result": s["attempt_result"],
             "examiners": [e["name_normalized"] for e in s["examiners"]]}
            for s in subs
        ],
        "submissions_detail": [{k: v for k, v in s.items() if k != "occurrences"}
                               for s in subs],
    }

    if a.check:
        have = [json.loads(l) for l in RECORDS.read_text(encoding="utf-8").splitlines() if l]
        drift = [o["occurrence_id"] for o, h in zip(occ, have)
                 if o["raw_question_text"] != h["raw_question_text"]]
        if len(have) != len(occ) or drift:
            print(f"FAIL: committed intake drifted from source "
                  f"(count {len(have)} vs {len(occ)}, drift={drift})")
            return 1
        print(f"OK: {len(occ)} August occurrences byte-match the source")
        return 0

    RECORDS.write_text(
        "\n".join(json.dumps(o, ensure_ascii=False) for o in occ) + "\n",
        encoding="utf-8")
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False),
                      encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
