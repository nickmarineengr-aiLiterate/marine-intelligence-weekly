#!/usr/bin/env python3
"""Extract official DG Shipping MEO Class I written papers from the archived
Word originals into a deterministic, portable JSON representation.

RESEARCH ONLY. Phase 3B.

Governance
----------
This follows the storage rule already established for the DGS question bank:
the raw binary stays OUTSIDE version control and the extracted representation
is committed. The raw directory is supplied by ``--raw-dir`` or the
``MIW_DGS_RAW_DIR`` environment variable so that no machine-specific path is
ever baked into a committed tool (Phase 3A.1 defect C-portability).

What this tool does NOT do
--------------------------
It does not decide dates. It records what the paper PRINTS. A filename token is
a hint and is carried as ``filename_date_token`` only; it never becomes a
sitting date. Papers that print no month get ``month: null`` and the caller is
expected to treat their date confidence accordingly. A paper that prints
"SAMPLE PAPER" is marked as such and is NOT a sitting.

Extraction path
---------------
``antiword`` renders the Word 97 binary. Its output is stable for these
documents and is the same renderer used to read the bank's sibling artefacts.
Where a ``.txt`` sidecar already exists next to the ``.doc`` it is used
instead, so a machine without antiword can still reproduce the JSON from the
committed text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCHEMA = "miw.pastpapers.qi_v2.dgs_class1_paper_extract.v1"

# ---------------------------------------------------------------- header reads

SUBJECT_CODES = {
    "am": "Applied Mechanics",
    "ed": "Engineering Drawing",
    "ekg": "Engineering Knowledge (General)",
    "ekm": "Engineering Knowledge (Motor)",
    "eks": "Engineering Knowledge (Steam)",
    "et": "Electrotechnology",
    "he": "Heat Engines",
    "ht": "Heat Transfer",
    "mem": "Engineering Management",
    "na": "Naval Architecture",
}

_FILENAME = re.compile(
    r"^(?P<a>a?)meo(?P<subject>[a-z0-9]+?)(?P<cls>I{1,3}V?|IV)_(?P<token>\d{3,4})"
    r"(?:_\d)?(?:_I)?\.doc$",
    re.I,
)

_MONTH_YEAR = re.compile(
    r"\b(january|february|march|april|may|june|july|august|september|october|"
    r"november|december)\s*[-/,]?\s*((?:19|20)\d{2})\b",
    re.I,
)
_COUNTRY_YEAR = re.compile(r"\bINDIA\s*\(\s*((?:19|20)\d{2})\s*\)", re.I)
_SERIAL = re.compile(r"\bSr\.?\s*No\.?\s*[:.]?\s*(\d+)", re.I)
_FORM_CODE = re.compile(r"^\s*(\d{2,3}(?:/\d{2,3})*\s*[A-Z]{1,4}\s*-\s*\d+)\s*$")
_TOTAL_MARKS = re.compile(r"Total\s+Marks?\s*[:.]?\s*(\d{2,3})", re.I)
_TIME_ALLOWED = re.compile(r"Time\s+allowed\s*[-–:]?\s*([0-9]+)\s*h", re.I)
_SESSION = re.compile(r"\b(Morning|Afternoon|Evening)\s+Paper\b", re.I)
_SAMPLE = re.compile(r"\bSAMPLE\s+PAPER\b", re.I)
_CLASS_LINE = re.compile(r"\bCLASS\s*[-–]?\s*(I{1,3}V?|IV)\b", re.I)

MONTH_NUM = {
    m.lower(): i
    for i, m in enumerate(
        [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ],
        start=1,
    )
}

# --------------------------------------------------------------- question reads

# "1.", "1)", "1. (a)" - a question opener must start the line.
_Q_OPEN = re.compile(r"^\s{0,6}(\d{1,2})\s*[.)]\s+(?P<rest>\S.*)$")
# subpart openers: "a)", "(a)", "i)", "(iii)"
_SUB_OPEN = re.compile(
    r"^\s*\(?\s*([a-z]|[ivx]{1,4})\s*\)\s+(?P<rest>\S.*)$", re.I
)
_INLINE_MARKS = re.compile(r"\((\d{1,2})\)\s*$")
_NB_LINE = re.compile(r"^\s*N\.?\s*B\.?\s*[-–:]", re.I)
_END_RULE = re.compile(r"^\s*-{3,}\s*X+\s*-{3,}\s*$|^\s*[-X]{8,}\s*$", re.I)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def render_text(doc: Path, antiword: str | None) -> tuple[str, str]:
    """Return (text, how). Prefers a committed .txt sidecar for portability."""
    sidecar = doc.with_suffix(".txt")
    if sidecar.exists():
        return sidecar.read_text(encoding="utf-8", errors="replace"), "txt_sidecar"
    if not antiword:
        raise RuntimeError(
            f"no .txt sidecar for {doc.name} and antiword is not on PATH"
        )
    out = subprocess.run(
        [antiword, "-w", "0", str(doc)],
        capture_output=True,
    )
    if out.returncode != 0:
        raise RuntimeError(
            f"antiword failed on {doc.name}: {out.stderr.decode(errors='replace')[:200]}"
        )
    return out.stdout.decode("cp1252", errors="replace"), "antiword"


def header_region(lines: list[str]) -> list[str]:
    """Everything printed above the rubric or the first question.

    The cut matters. A paper body can contain a date - "ships whose keel was
    laid before 1st July 1986" - and a fixed-size window swallows it, inventing
    a 1986 sitting out of a regulation's application date. The header ends at
    the N.B. rubric or the first question opener, whichever comes first.
    """
    end = len(lines)
    for i, ln in enumerate(lines):
        if _NB_LINE.search(ln) or (_Q_OPEN.match(ln) and i > 3):
            end = i
            break
    return lines[:end]


def parse_header(lines: list[str]) -> dict:
    head = "\n".join(header_region(lines))
    hdr: dict = {
        "is_sample_paper": bool(_SAMPLE.search(head)),
        "form_code": None,
        "serial_no": None,
        "printed_year": None,
        "printed_month": None,
        "printed_month_source": None,
        "session": None,
        "total_marks": None,
        "time_allowed_hours": None,
        "class_printed": None,
    }

    for ln in lines[:40]:
        m = _FORM_CODE.match(ln.strip())
        if m and hdr["form_code"] is None:
            hdr["form_code"] = re.sub(r"\s+", "", m.group(1))

    m = _SERIAL.search(head)
    if m:
        hdr["serial_no"] = int(m.group(1))

    m = _MONTH_YEAR.search(head)
    if m:
        hdr["printed_month"] = MONTH_NUM[m.group(1).lower()]
        hdr["printed_year"] = int(m.group(2))
        hdr["printed_month_source"] = "PRINTED_MONTH_YEAR_LINE"
    else:
        m = _COUNTRY_YEAR.search(head)
        if m:
            hdr["printed_year"] = int(m.group(1))
            hdr["printed_month_source"] = "PRINTED_YEAR_ONLY"

    m = _SESSION.search(head)
    if m:
        hdr["session"] = m.group(1).title()
    m = _TOTAL_MARKS.search(head)
    if m:
        hdr["total_marks"] = int(m.group(1))
    m = _TIME_ALLOWED.search(head)
    if m:
        hdr["time_allowed_hours"] = int(m.group(1))
    m = _CLASS_LINE.search(head)
    if m:
        hdr["class_printed"] = m.group(1).upper()
    return hdr


def parse_instructions(lines: list[str]) -> list[str]:
    out: list[str] = []
    started = False
    for ln in lines[:45]:
        if _NB_LINE.search(ln):
            started = True
        if not started:
            continue
        if _Q_OPEN.match(ln):
            break
        s = " ".join(ln.split())
        if s:
            out.append(s)
    merged: list[str] = []
    for s in out:
        parts = re.split(r"(?=\(\d\)\s)", s)
        for p in parts:
            p = p.strip()
            p = re.sub(r"^N\.?\s*B\.?\s*[-–:]\s*", "", p, flags=re.I).strip()
            if p:
                merged.append(p)
    return merged


def parse_questions(lines: list[str]) -> list[dict]:
    """Split the body into questions and printed subparts.

    Marks are recorded ONLY where the paper prints them in brackets. They are
    never inferred and never divided.
    """
    # find body start: first question opener after the instructions
    start = 0
    for i, ln in enumerate(lines):
        if _Q_OPEN.match(ln) and i > 3:
            start = i
            break
    body = lines[start:]

    questions: list[dict] = []
    cur: dict | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal cur, buf
        if cur is None:
            return
        cur["_raw"] = "\n".join(buf).strip()
        questions.append(cur)
        cur, buf = None, []

    for ln in body:
        if _END_RULE.match(ln):
            break
        m = _Q_OPEN.match(ln)
        if m:
            n = int(m.group(1))
            # The sequence check must run against the question currently OPEN,
            # not the last flushed one - otherwise nothing after Q1 ever opens
            # and the whole paper collapses into a single question.
            expected = (cur["question_no"] + 1) if cur is not None else 1
            if cur is None or n == expected:
                flush()
                cur = {"question_no": n}
                buf = [m.group("rest")]
                continue
        if cur is not None:
            buf.append(ln)
    flush()

    out: list[dict] = []
    for q in questions:
        raw = q.pop("_raw")
        subparts = split_subparts(raw)
        text = " ".join(raw.split())
        out.append(
            {
                "question_no": q["question_no"],
                "raw_text": text,
                "marks_printed": marks_of(raw),
                "subparts": subparts,
            }
        )
    return out


def marks_of(raw: str) -> int | None:
    """Marks printed for the whole question, only when there are no subparts
    carrying their own marks."""
    tail = [m for m in _INLINE_MARKS.finditer(raw)]
    if len(tail) == 1:
        lines = [l for l in raw.splitlines() if l.strip()]
        if lines and _INLINE_MARKS.search(lines[-1].strip()):
            return int(tail[0].group(1))
    return None


def split_subparts(raw: str) -> list[dict]:
    lines = raw.splitlines()
    parts: list[dict] = []
    cur_label: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal cur_label, buf
        if cur_label is None:
            return
        chunk = "\n".join(buf)
        mk = None
        for m in _INLINE_MARKS.finditer(chunk):
            mk = int(m.group(1))
        txt = " ".join(_INLINE_MARKS.sub("", chunk).split())
        parts.append(
            {"label": f"({cur_label})", "raw_text": txt, "marks_printed": mk}
        )
        cur_label, buf = None, []

    for ln in lines:
        m = _SUB_OPEN.match(ln)
        if m:
            flush()
            cur_label = m.group(1).lower()
            buf = [m.group("rest")]
            continue
        if cur_label is not None:
            buf.append(ln)
    flush()
    return parts


def extract_one(doc: Path, antiword: str | None) -> dict:
    text, how = render_text(doc, antiword)
    lines = [l.rstrip() for l in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]

    fm = _FILENAME.match(doc.name)
    subject_code = fm.group("subject").lower() if fm else None
    cls = fm.group("cls").upper() if fm else None
    token = fm.group("token") if fm else None

    hdr = parse_header(lines)
    questions = parse_questions(lines)

    return {
        "file": doc.name,
        "sha256": sha256_of(doc),
        "bytes": doc.stat().st_size,
        "extraction": how,
        "subject_code": subject_code,
        "subject": SUBJECT_CODES.get(subject_code or "", "UNKNOWN"),
        "class_from_filename": cls,
        "filename_date_token": token,
        "header": hdr,
        "instructions": parse_instructions(lines),
        "question_count": len(questions),
        "questions": questions,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--raw-dir",
        default=os.environ.get("MIW_DGS_RAW_DIR"),
        help="directory holding the archived .doc originals (or .txt sidecars)",
    )
    ap.add_argument("--out", required=True, help="path to write the extract JSON")
    ap.add_argument("--class", dest="only_class", default="I")
    args = ap.parse_args()

    if not args.raw_dir:
        print("ERROR: --raw-dir or MIW_DGS_RAW_DIR is required", file=sys.stderr)
        return 2
    raw = Path(args.raw_dir)
    if not raw.is_dir():
        print(f"ERROR: not a directory: {raw}", file=sys.stderr)
        return 2

    antiword = shutil.which("antiword")
    docs = sorted(p for p in raw.glob("*.doc"))
    papers, failed = [], []
    for d in docs:
        fm = _FILENAME.match(d.name)
        if not fm or fm.group("cls").upper() != args.only_class.upper():
            continue
        try:
            papers.append(extract_one(d, antiword))
        except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
            failed.append({"file": d.name, "error": str(exc)})

    papers.sort(key=lambda p: (p["subject_code"] or "", p["file"]))
    doc = {
        "schema": SCHEMA,
        "status": "RESEARCH_ONLY",
        "what_this_is": (
            "Deterministic text extraction of archived official DG Shipping MEO "
            "Class I written papers. Records what each paper PRINTS. Filename "
            "date tokens are hints and are never sitting dates. A paper marked "
            "is_sample_paper is not a sitting."
        ),
        "extraction_tool": "tools/extract_dgs_class1_papers.py",
        "renderer": "antiword" if antiword else "txt_sidecar",
        "paper_count": len(papers),
        "extraction_failures": failed,
        "papers": papers,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"papers extracted : {len(papers)}")
    print(f"failures         : {len(failed)}")
    for f in failed:
        print(f"  FAIL {f['file']}: {f['error'][:120]}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
