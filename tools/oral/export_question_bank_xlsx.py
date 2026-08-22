"""Export the CURRENT published MIW Oral question bank to a candidate workbook.

Born 2026-08-22 for the August 2026 INTERIM snapshot, so that every future
interim/final spreadsheet comes from repository truth rather than manual Excel
patching of the July workbook.

Architecture (and the one rule that keeps it honest):

    CANONICAL ORAL DATA        meoclass1/qb_content_index.json   (identity + text)
                               EXAMINER_INDEX_SNAPSHOT.json      (examiner rows)
                               live QB HTML                      (anchor proof only)
            |
    NORMALIZED EXPORT MODEL    build_export_model()  -> list of plain dicts
            |
    XLSX RENDERER              render_workbook()     -> openpyxl workbook

The renderer NEVER infers topic, examiner or syllabus data. Every cell is a
field of the model, and every field of the model is read from a governed
repository artefact. The model already carries the syllabus fields the future
governed mapper will populate (official_syllabus_version, official_syllabus_node_id,
miw_topic_id, miw_topic_name, objective_id); today they are empty and are NOT
rendered -- this exporter must never populate them itself.

Sources and what each is trusted for:
  * qb_content_index.json  - the 721/86 canonical identity (file + anchor), the
                             candidate-facing question text, the QB group and the
                             page title used as the current production
                             "Topic / Category". The exporter re-runs the index
                             generator's --check so a stale index cannot be exported.
  * EXAMINER_INDEX_SNAPSHOT.json - exactly the object meoclass1/examiner-index.html
                             is rendered from. One row = one (examiner, question)
                             relationship (960 / 7 examiners on production). The
                             exporter joins rows to questions by canonical id and
                             shows examiner NAMES only; tiers, refs and evidence
                             counts stay internal.
  * live QB HTML           - proof that each exported anchor exists on the page it
                             links to (id="q<N>" on a q-card in that file).

Usage:
  PYTHONIOENCODING=utf-8 python tools/oral/export_question_bank_xlsx.py --candidate-interim
      writes docs/MIW-master-Question-bank/MIW_August2026_QuestionBank_INTERIM.xlsx
  ... --out PATH            write somewhere else (a validator/test scratch path)
  ... --working-master      also write MEO_QB_master_v27_WORKING.xlsx (internal,
                            same model, adds the Examiner-relationship projection)
  ... --model-json PATH     dump the normalized model (for diffing / tests)

Historical release workbooks are never overwritten: any output whose file name
is in PROTECTED_OUTPUTS (or ends in a FINAL-style name) is refused.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html as _html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_lib as L  # noqa: E402

SITE_BASE = "https://marineintelligenceweekly.com"
INDEX_PATH = L.MEO / "qb_content_index.json"
SNAPSHOT_PATH = L.OUT / "EXAMINER_INDEX_SNAPSHOT.json"
REGISTER_PATH = L.OUT / "EXAMINER_ALIAS_REGISTER.json"
RELEASE_DIR = L.REPO / "docs" / "MIW-master-Question-bank"

INTERIM_NAME = "MIW_August2026_QuestionBank_INTERIM.xlsx"
WORKING_NAME = "MEO_QB_master_v27_WORKING.xlsx"

# Historical releases (never overwritten) and the final names this exporter is
# not allowed to produce until the final release sequence authorises them.
PROTECTED_OUTPUTS = {
    "MEO_QB_master_v26.xlsx",
    "MIW_July2026_QuestionBank_SHARE.xlsx",
    "MEO_QB_master_v27.xlsx",
    "MIW_August2026_QuestionBank_SHARE.xlsx",
}
FINAL_NAME_RE = re.compile(r"final|master_v\d+\.xlsx$|_SHARE\.xlsx$", re.I)

SNAPSHOT_LABEL = "August 2026 — INTERIM SNAPSHOT"
ABOUT_NOTE = (
    "This is an interim snapshot of the current live MIW Oral question bank. "
    "Recent examiner follow-ups are still being incorporated and reconciled. "
    "A final audited consolidated workbook will follow. The current file is being "
    "shared now so candidates do not have to wait."
)
ACCESS_NOTE = "Question links use normal MIW access permissions."

# Candidate sheet columns: (header, model field, width)
MAIN_COLUMNS = [
    ("No.", "no", 6),
    ("Canonical Question ID", "id", 16),
    ("Question", "question", 80),
    ("Topic / Category", "topic", 34),
    ("Question Bank", "qb", 14),
    ("Examiner(s)", "examiners_text", 26),
    ("MIW Answer Link", "url", 52),
]
MAIN_SHEET = "All Questions"
ABOUT_SHEET = "About"

# Reserved for the governed syllabus mapper. Present in the model, never
# rendered to a candidate, never populated here.
SYLLABUS_FIELDS = (
    "official_syllabus_version",
    "official_syllabus_node_id",
    "miw_topic_id",
    "miw_topic_name",
    "objective_id",
)


class ExportFailure(Exception):
    pass


def fail(msg):
    raise ExportFailure(msg)


# ------------------------------------------------------------------ text

_WS_RE = re.compile(r"\s+")


def display_text(s):
    """Presentation-only normalisation: entities, markup, line breaks, whitespace.
    No semantic rewriting."""
    s = _html.unescape(L.strip_tags(s or ""))
    s = s.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    return _WS_RE.sub(" ", s).strip()


def natural_file_key(fname):
    parts = re.split(r"(\d+)", fname)
    return [int(p) if p.isdigit() else p for p in parts]


# ------------------------------------------------------------------ sources

def check_index_fresh():
    """Refuse to export from an index that no longer matches the live HTML."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, str(HERE / "build_qb_content_index.py"), "--check"],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    if r.returncode != 0:
        fail("qb_content_index.json is stale against the live QB HTML:\n" + r.stdout + r.stderr)


def load_index():
    d = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    if d.get("manifest_version") != "1.1":
        fail("unexpected qb_content_index manifest_version %r" % d.get("manifest_version"))
    return d


def load_examiner_rows():
    s = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    reg = json.loads(REGISTER_PATH.read_text(encoding="utf-8"))
    names = {e["slug"]: e["canonical_name"] for e in reg["examiners"]}
    by_q = {}
    for r in s["rows"]:
        if r["slug"] not in names:
            fail("examiner slug %r in snapshot but not in the alias register" % r["slug"])
        by_q.setdefault(r["canonical_question_id"], []).append(r)
    return s, by_q, names


_ANCHOR_CACHE = {}


def anchor_exists(fname, anchor):
    """True when the live page carries a q-card with id=<anchor>."""
    if fname not in _ANCHOR_CACHE:
        p = L.MEO / fname
        if not p.is_file():
            _ANCHOR_CACHE[fname] = None
        else:
            h = p.read_text(encoding="utf-8")
            _ANCHOR_CACHE[fname] = set(re.findall(
                r'<div[^>]*\bclass="[^"]*\bq-card\b[^"]*"[^>]*\bid="(q\d+)"', h))
            _ANCHOR_CACHE[fname] |= set(re.findall(
                r'<div[^>]*\bid="(q\d+)"[^>]*\bclass="[^"]*\bq-card\b', h))
    ids = _ANCHOR_CACHE[fname]
    return ids is not None and anchor in ids


# ------------------------------------------------------------------ model

def build_export_model(check_fresh=True):
    """Return (meta, rows). Rows are plain dicts; one row per canonical question,
    in QB file order then document order. Raises ExportFailure on any identity
    defect so a broken model never reaches a renderer."""
    if check_fresh:
        check_index_fresh()
    idx = load_index()
    snapshot, ex_by_q, ex_names = load_examiner_rows()
    order = sorted(snapshot.get("sections", []), key=lambda s: s.get("slug", ""))
    slug_rank = {s["slug"]: i for i, s in enumerate(
        sorted(order, key=lambda s: -s.get("count", 0)))}

    rows, seen = [], set()
    files = sorted(idx["files"].items(), key=lambda kv: natural_file_key(kv[0]))
    for fname, f in files:
        if not (L.MEO / fname).is_file():
            fail("%s listed in the index but missing on disk" % fname)
        for q in f["questions"]:
            qid = q["id"]
            if qid in seen:
                fail("duplicate canonical id %s" % qid)
            seen.add(qid)
            if qid != "%s#%s" % (Path(fname).stem, q["anchor"]):
                fail("%s: id does not match file+anchor" % qid)
            if not anchor_exists(fname, q["anchor"]):
                fail("%s: anchor %s not found on %s" % (qid, q["anchor"], fname))
            text = display_text(q["text"])
            if not text:
                fail("%s: empty question text" % qid)
            exs = sorted({r["slug"] for r in ex_by_q.get(qid, [])},
                         key=lambda s: (slug_rank.get(s, 99), s))
            rows.append({
                "no": len(rows) + 1,
                "id": qid,
                "file": fname,
                "anchor": q["anchor"],
                "qnum": q["qnum"],
                "question": text,
                "qb": f["qb_group"],
                "topic": display_text(f["title"]),
                "url": "%s/meoclass1/%s#%s" % (SITE_BASE, fname, q["anchor"]),
                "examiners": [ex_names[s] for s in exs],
                "examiners_text": ", ".join(ex_names[s] for s in exs),
                "examiner_relationships": len(ex_by_q.get(qid, [])),
                **{k: "" for k in SYLLABUS_FIELDS},
            })

    if len(rows) != idx["total_questions"]:
        fail("row count %d != index total_questions %d" % (len(rows), idx["total_questions"]))
    phantom = set(ex_by_q) - seen
    if phantom:
        fail("examiner snapshot names %d question ids not in the canonical index: %s"
             % (len(phantom), sorted(phantom)[:5]))

    meta = {
        "snapshot_label": SNAPSHOT_LABEL,
        "canonical_questions": len(rows),
        "question_files": len({r["file"] for r in rows}),
        "examiner_relationships": snapshot["totals"]["relationships"],
        "examiners": snapshot["totals"]["examiners"],
        "questions_with_examiner": sum(1 for r in rows if r["examiners"]),
        "examiner_names": [ex_names[s["slug"]] for s in snapshot["sections"]],
        "index_source": str(INDEX_PATH.relative_to(L.REPO)).replace("\\", "/"),
    }
    return meta, rows


# ------------------------------------------------------------------ renderer

def _styles():
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    thin = Side(style="thin", color="D9D9D9")
    return {
        "head_font": Font(bold=True, color="FFFFFF"),
        "head_fill": PatternFill("solid", fgColor="1F3A5F"),
        "title_font": Font(bold=True, size=14, color="1F3A5F"),
        "bold": Font(bold=True),
        "link": Font(color="0563C1", underline="single"),
        "wrap": Alignment(wrap_text=True, vertical="top"),
        "top": Alignment(vertical="top"),
        "border": Border(top=thin, bottom=thin, left=thin, right=thin),
    }


def _table(ws, headers, widths, rows, st, link_col=None):
    from openpyxl.utils import get_column_letter
    ws.append(headers)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.font, cell.fill, cell.alignment = st["head_font"], st["head_fill"], st["top"]
        ws.column_dimensions[get_column_letter(c)].width = widths[c - 1]
    for r in rows:
        ws.append(r)
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(headers)):
        for cell in row:
            cell.alignment = st["wrap"]
            cell.border = st["border"]
        if link_col is not None:
            cell = row[link_col]
            cell.hyperlink = cell.value
            cell.font = st["link"]
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(headers)), ws.max_row)


def render_workbook(meta, rows, generated_at, internal=False):
    import openpyxl
    st = _styles()
    wb = openpyxl.Workbook()

    # --- About (first sheet)
    ws = wb.active
    ws.title = ABOUT_SHEET
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 90
    lines = [
        ("Marine Intelligence Weekly", None, st["title_font"]),
        ("MEO Class I Oral Question Bank", None, st["bold"]),
        (meta["snapshot_label"], None, st["bold"]),
        ("", None, None),
        ("Generated:", generated_at, None),
        ("Canonical questions:", meta["canonical_questions"], None),
        ("Question bank pages:", meta["question_files"], None),
        ("Examiners:", ", ".join(meta["examiner_names"]), None),
        ("", None, None),
        ("Note:", ABOUT_NOTE, None),
        ("Access:", ACCESS_NOTE, None),
        ("", None, None),
        ("How to use:", "Open the 'All Questions' sheet. Filter by Topic / Category, "
                        "Question Bank or Examiner(s), then click the MIW Answer Link.", None),
    ]
    if internal:
        lines.append(("Internal:", "WORKING copy - not a release. Examiner relationships: %d "
                      "across %d examiners; %d of %d questions carry at least one examiner."
                      % (meta["examiner_relationships"], meta["examiners"],
                         meta["questions_with_examiner"], meta["canonical_questions"]), None))
    for a, b, font in lines:
        ws.append([a, b])
        if font:
            ws.cell(row=ws.max_row, column=1).font = font
        ws.cell(row=ws.max_row, column=2).alignment = st["wrap"]

    # --- All Questions (the candidate sheet)
    ws = wb.create_sheet(MAIN_SHEET)
    headers = [h for h, _, _ in MAIN_COLUMNS]
    widths = [w for _, _, w in MAIN_COLUMNS]
    fields = [f for _, f, _ in MAIN_COLUMNS]
    _table(ws, headers, widths, [[r[f] for f in fields] for r in rows], st,
           link_col=fields.index("url"))

    # --- Projections (same model, different grouping; cheap)
    ws = wb.create_sheet("By Examiner")
    proj = []
    for r in rows:
        for ex in r["examiners"]:
            proj.append([ex, r["id"], r["question"], r["topic"], r["qb"], r["url"]])
    # stable sort: examiner presentation order, model (document) order inside each examiner
    proj.sort(key=lambda x: meta["examiner_names"].index(x[0]))
    _table(ws, ["Examiner", "Canonical Question ID", "Question", "Topic / Category",
                "Question Bank", "MIW Answer Link"], [14, 16, 80, 34, 14, 52], proj, st, link_col=5)

    ws = wb.create_sheet("By Question Bank")
    qbs, seen_files = [], []
    for r in rows:  # one row per QB page, in model order
        if r["file"] not in seen_files:
            seen_files.append(r["file"])
    for fname in seen_files:
        sub = [r for r in rows if r["file"] == fname]
        qbs.append([sub[0]["qb"], sub[0]["topic"], len(sub), sub[0]["url"].split("#")[0]])
    _table(ws, ["Question Bank", "Topic / Category", "Questions", "MIW Page Link"],
           [14, 44, 11, 52], qbs, st, link_col=3)

    if internal:
        ws = wb.create_sheet("Examiner Relationships")
        _table(ws, ["Canonical Question ID", "Examiner(s)", "Relationship rows", "Question"],
               [16, 26, 16, 80],
               [[r["id"], r["examiners_text"], r["examiner_relationships"], r["question"]] for r in rows], st)
    return wb


# ------------------------------------------------------------------ output

def check_output_allowed(path):
    name = Path(path).name
    if name in PROTECTED_OUTPUTS or (FINAL_NAME_RE.search(name) and "WORKING" not in name):
        fail("refusing to write %s: historical release / final name is protected" % name)


def write_workbook(wb, path):
    check_output_allowed(path)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp.xlsx")
    wb.save(tmp)
    os.replace(tmp, path)
    return path


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--candidate-interim", action="store_true",
                    help="write the August 2026 interim candidate workbook")
    ap.add_argument("--working-master", action="store_true",
                    help="also write the internal WORKING master (same model)")
    ap.add_argument("--out", help="explicit output path for the candidate workbook")
    ap.add_argument("--model-json", help="also dump the normalized export model here")
    ap.add_argument("--no-fresh-check", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    if not (a.candidate_interim or a.out or a.model_json or a.working_master):
        ap.error("nothing to do: pass --candidate-interim (and/or --out/--model-json)")

    try:
        meta, rows = build_export_model(check_fresh=not a.no_fresh_check)
        generated_at = _dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
        written = []
        if a.model_json:
            Path(a.model_json).write_text(json.dumps({"meta": meta, "rows": rows}, indent=1,
                                                     ensure_ascii=False) + "\n", encoding="utf-8")
            written.append(a.model_json)
        if a.candidate_interim or a.out:
            out = Path(a.out) if a.out else RELEASE_DIR / INTERIM_NAME
            written.append(str(write_workbook(render_workbook(meta, rows, generated_at), out)))
        if a.working_master:
            written.append(str(write_workbook(
                render_workbook(meta, rows, generated_at, internal=True), RELEASE_DIR / WORKING_NAME)))
    except ExportFailure as e:
        print("EXPORT FAILURE: %s" % e)
        return 2
    print("export: %d canonical questions, %d files, %d examiner relationships / %d examiners"
          % (meta["canonical_questions"], meta["question_files"],
             meta["examiner_relationships"], meta["examiners"]))
    for w in written:
        print("wrote %s (%d bytes)" % (w, Path(w).stat().st_size))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
