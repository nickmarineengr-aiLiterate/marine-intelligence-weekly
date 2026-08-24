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
# "1. text" / "2) text" / "1 .text" - the candidate's phone inserts a space
# before the separator often enough that requiring adjacency silently drops the
# question into context. S004 lost two occurrences that way before this was
# widened, and a lost occurrence raises no error: it just is not counted.
Q_RE = re.compile(r"^(\d+)\s*[.)]\s*(.*)$", re.S)
# "Attempt 1" / "Attempt-1" / "Attempt : 2" - candidates punctuate this freely
# and the attempt number is evidence about the sitting, not decoration.
ATTEMPT_RE = re.compile(r"^Attempt\s*[-:]?\s*(\d+)\s*$", re.I)
RESULT_RE = re.compile(r"^Result\s*[-:]\s*(.+?)\s*$", re.I)
RULE_RE = re.compile(r"^[-]{3,}$")
# A bare "<Name> :" line inside the body. It is treated as an attribution
# marker ONLY when <Name> matches an examiner already declared by this same
# submission, so the parser can never invent an attribution that the candidate
# did not write.
ATTRIB_RE = re.compile(r"^([A-Za-z][A-Za-z .'-]{1,40}?)\s*:\s*(.*)$", re.S)
# A bare "Internal" / "Ext" heading with no name after it. Candidates use it the
# same way they use a name marker: everything below it came from that seat.
# It is honoured ONLY when the submission declared exactly one examiner in that
# role, so it can never pick between two people.
BARE_ROLE_RE = re.compile(r"^(Ext|Int|External|Internal)\s*[-:.]?\s*$", re.I)
# A line that is only a date. In an unnumbered submission every non-metadata
# line becomes an occurrence, so the sitting date must be recognised as
# metadata or it would be counted as a question.
DATE_ONLY_RE = re.compile(
    r"^\d{1,2}\s*[-/. ]\s*(?:\d{1,2}|[A-Za-z]{3,9})\s*[-/. ]\s*\d{2,4}\s*$")

ROLE_NORM = {"ext": "EXTERNAL", "external": "EXTERNAL",
             "int": "INTERNAL", "internal": "INTERNAL"}

# Invisible characters the messaging app inserted; stripped for the NORMALISED
# form only. The raw field keeps them so the evidence stays byte-faithful.
INVISIBLE = dict.fromkeys(map(ord, "⁠​‌‍﻿"), None)

NON_QUESTION_CUES = ("i forgot", "forgot", "don't remember", "didn't know")

# Candidates paste chat transcripts into their reports. The carrier file is
# git-ignored, but context_comments IS committed, so a third party's name would
# otherwise enter the repository through the derived record. The substance is
# kept; only the identifier is removed.
CHAT_ATTRIB_RE = re.compile(
    r"\[\s*\d{1,2}:\d{2}\s*,\s*\d{1,2}/\d{1,2}/\d{2,4}\s*\]\s*[^:]{1,60}:")


def redact_third_parties(text: str) -> str:
    return CHAT_ATTRIB_RE.sub("[third party, name removed]:", text)


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


def parse_submission(lines, submission_id: str, seq_start: int,
                     unnumbered: bool = False):
    """Parse one candidate report.

    `unnumbered` is set by parse_file when the candidate wrote no "1." "2."
    numbering at all. In that mode the candidate's own line breaks are the
    occurrence boundary, because there is nothing else to use. Metadata lines
    (role declarations, attempt, result, a bare date, a bare role heading) are
    still recognised and excluded; everything else is preserved as an
    occurrence and dispositioned downstream. Over-capturing a stray remark is
    visible and adjudicable; dropping a question is silent, which is why the
    default leans towards keeping the line.
    """
    examiners, occurrences = [], []
    attempt_no = result = None
    preamble = []
    # Set by an in-body "<Name> :" marker; applies to every following
    # occurrence until another marker replaces it. None means the candidate
    # gave no per-question attribution, which stays PANEL_LEVEL_ONLY.
    current_attrib = None
    attrib_marker = None
    attrib_basis = None

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

        m = BARE_ROLE_RE.match(t)
        if m:
            want = ROLE_NORM[m.group(1).lower()]
            holders = [e for e in examiners if e["role"] == want]
            if len(holders) == 1:
                current_attrib = holders[0]["name_normalized"]
                attrib_marker = t
                attrib_basis = "ROLE_MARKER_SOLE_HOLDER"
            # Two holders, or none declared yet: the heading identifies no one
            # individually, so attribution is left exactly as it was.
            continue

        m = ATTEMPT_RE.match(t)
        if m:
            attempt_no = int(m.group(1))
            continue

        m = RESULT_RE.match(t)
        if m:
            result = m.group(1).strip()
            continue

        m = ATTRIB_RE.match(t)
        if m and not Q_RE.match(t):
            declared = {e["name_normalized"].lower() for e in examiners}
            cand = normalise_examiner(m.group(1))
            if cand.lower() in declared:
                current_attrib, attrib_marker = cand, t
                attrib_basis = "NAME_MARKER"
                trailing = m.group(2).strip()
                if trailing:
                    # "Senthil : tqm, new acts and difference between act and
                    # rule." - the marker carries its questions on the same
                    # line and is not numbered. Treated as ONE occurrence
                    # holding the raw line: splitting it into limbs here would
                    # be the parser inventing question boundaries the candidate
                    # never wrote. Adjudication splits it, on the record.
                    occurrences.append({
                        "occurrence_id": f"AUG-{seq_start + len(occurrences):04d}",
                        "submission_id": submission_id,
                        "source_question_number": None,
                        "raw_question_text": m.group(2),
                        "normalised_question_text": normalise(m.group(2)),
                        "is_question": not looks_like_non_question(trailing),
                        "_attrib": current_attrib,
                        "_attrib_marker": t,
                        "_attrib_basis": attrib_basis,
                    })
                continue
            # A name-like line that is NOT a declared examiner is never an
            # attribution. It stays context, exactly as before.

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
                "_attrib": current_attrib,
                "_attrib_marker": attrib_marker,
                "_attrib_basis": attrib_basis,
            })
            continue

        if unnumbered and not DATE_ONLY_RE.match(t):
            occurrences.append({
                "occurrence_id": f"AUG-{seq_start + len(occurrences):04d}",
                "submission_id": submission_id,
                "source_question_number": None,
                "source_line_style": "UNNUMBERED",
                "raw_question_text": t,
                "normalised_question_text": normalise(t),
                "is_question": not looks_like_non_question(t),
                "_attrib": current_attrib,
                "_attrib_marker": attrib_marker,
                "_attrib_basis": attrib_basis,
            })
            continue

        preamble.append(redact_third_parties(t))

    for o in occurrences:
        o["attempt_number"] = attempt_no
        o["attempt_result"] = result
        o["examiners"] = [e["name_normalized"] for e in examiners]
        who, marker = o.pop("_attrib"), o.pop("_attrib_marker")
        basis = o.pop("_attrib_basis")
        if who:
            # The candidate wrote this examiner's name above the question.
            o["examiner_attribution"] = "INDIVIDUALLY_ATTRIBUTED"
            o["attributed_examiner"] = who
            o["attribution_marker"] = marker
            # Emitted only for the role-heading route, so that records written
            # by the original name-marker route stay byte-identical.
            if basis == "ROLE_MARKER_SOLE_HOLDER":
                o["attribution_basis"] = basis
        else:
            # Both examiners sat the same panel and the candidate tied no
            # question to a person; neither may be named for this question.
            o["examiner_attribution"] = "PANEL_LEVEL_ONLY"
            o["attributed_examiner"] = None
            o["attribution_marker"] = None

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

    subs, seq, skipped = [], 1, []
    for idx, blk in enumerate(blocks, 1):
        numbered = any(Q_RE.match(l.strip()) for l in blk)
        # A candidate who numbers nothing still declares the panel. Requiring
        # numbering to recognise a submission silently discarded an entire
        # sitting report: the block just failed the test and `continue` said
        # nothing. Either signal now identifies a submission.
        declared = any(ROLE_RE.match(l.strip()) and not Q_RE.match(l.strip())
                       for l in blk)
        if not numbered and not declared:
            if any(l.strip() for l in blk):
                skipped.append({
                    "block_index": idx,
                    "nonempty_lines": sum(1 for l in blk if l.strip()),
                    "first_line": next(l.strip() for l in blk if l.strip()),
                })
            continue
        s = parse_submission(blk, f"AUG2026-S{len(subs) + 1:03d}", seq,
                             unnumbered=not numbered)
        s["source_file"] = path.name
        s["line_style"] = "NUMBERED" if numbered else "UNNUMBERED"
        seq += len(s["occurrences"])
        subs.append(s)
    return subs, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--txt", required=True)
    ap.add_argument("--check", action="store_true",
                    help="verify committed records still match the source")
    a = ap.parse_args()

    subs, skipped = parse_file(Path(a.txt))
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
        # A block of the carrier that yielded no submission. Reported so that a
        # lost sitting report is visible in the derived record instead of
        # vanishing between two rule lines.
        "unparsed_source_blocks": skipped,
        "examiners_represented": sorted(roles),
        "examiner_roles": roles,
        "individually_attributed_occurrences": sorted(
            o["occurrence_id"] for o in occ
            if o["examiner_attribution"] == "INDIVIDUALLY_ATTRIBUTED"),
        "panel_level_occurrences": sum(
            1 for o in occ if o["examiner_attribution"] == "PANEL_LEVEL_ONLY"),
        "per_submission": [
            {"submission_id": s["submission_id"],
             "raw_occurrences": len(s["occurrences"]),
             "attempt_number": s["attempt_number"],
             "attempt_result": s["attempt_result"],
             "examiners": [e["name_normalized"] for e in s["examiners"]],
             "occurrence_ids": [o["occurrence_id"] for o in s["occurrences"]],
             "per_question_attribution": sorted(
                 {o["examiner_attribution"] for o in s["occurrences"]})}
            for s in subs
        ],
        "submissions_detail": [{k: v for k, v in s.items() if k != "occurrences"}
                               for s in subs],
    }

    if a.check:
        # Content the carrier holds but the parser could not place is a defect,
        # not a clean run. This is checked BEFORE the record comparison because
        # a dropped block leaves the committed records perfectly self-consistent
        # — which is exactly how a whole submission went missing unnoticed.
        if skipped:
            print(f"FAIL: {len(skipped)} source block(s) yielded no submission: "
                  f"{[s['block_index'] for s in skipped]}")
            return 1
        have = [json.loads(l) for l in RECORDS.read_text(encoding="utf-8").splitlines() if l]
        drift = [o["occurrence_id"] for o, h in zip(occ, have)
                 if o["raw_question_text"] != h["raw_question_text"]]
        # Attribution is evidence too: a committed row may not claim an
        # examiner the source does not carry, nor drop one that it does.
        drift += [o["occurrence_id"] for o, h in zip(occ, have)
                  if (o["examiner_attribution"] != h.get("examiner_attribution")
                      or o["attributed_examiner"] != h.get("attributed_examiner"))
                  and o["occurrence_id"] not in drift]
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
