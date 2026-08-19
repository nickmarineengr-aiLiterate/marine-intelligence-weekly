"""Generate meoclass1/qb_content_index.json from the LIVE Oral QB HTML.

Governing principle
-------------------
The live QB HTML is the question truth. qb_content_index.json is a DERIVED
index - not a source, and not a qnum authority. Identity is file + anchor;
array position is display metadata. Question text comes from the
candidate-facing q-card. Examiner / production metadata never enters it.

What this writes (and owns)
---------------------------
  meoclass1/qb_content_index.json      whole file
  meoclass1/index.html                 exactly three regions, anchored and
                                       counted, everything else byte-untouched:
                                         - the `const Q_INDEX = [...];` line
                                           (the hub search records)
                                         - each QB_GROUPS card's "qcount"
                                         - the first hero <span class="stat-val">
                                           ("Questions Live")
  Both are consumers of the same live derivation, which is what keeps
  qb_health_check.py's card/Q_INDEX/manifest count contract satisfied.

Inputs
------
  meoclass1/QB*.html (not cheat sheets)          via oral_lib.qb_files()
  meoclass1/*CheatSheet*.html on disk            cheat-sheet linkage
  meoclass1/index.html QB_GROUPS                 group membership ("qb" field)
  tools/oral/qb_content_index_governed.json      the hand-maintained parts that
                                                 cannot be derived from a page:
                                                 recently_updated changelog
                                                 ({date, note, files} only -
                                                 see check_corrections),
                                                 per-file corrections_applied,
                                                 version fallback where the page
                                                 carries no Version line, and
                                                 the one irregular cheat-sheet
                                                 name (QB1_FG).

Determinism
-----------
Files ordered by natural key; questions in document order; every dict emitted
with explicit key order; sets sorted before emission. Output is LF, UTF-8, and
written to a staging file then os.replace()d - an interrupted run never leaves a
half-written index.

  PYTHONIOENCODING=utf-8 python tools/oral/build_qb_content_index.py [--check] [--out-dir DIR]

  --check      derive everything, compare with what is on disk, write nothing;
               exit 3 if the committed outputs are stale.
  --out-dir    write both outputs under DIR instead of the repo (staging /
               determinism harness).
"""
from __future__ import annotations

import glob
import html
import json
import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_lib as L  # noqa: E402

MANIFEST_PATH = L.MEO / "qb_content_index.json"
INDEX_HTML_PATH = L.MEO / "index.html"
GOVERNED_PATH = HERE / "qb_content_index_governed.json"

MANIFEST_VERSION = "1.1"
GENERATED_BY = ("tools/oral/build_qb_content_index.py - derived from the live QB HTML "
                "(identity = file + anchor); governed fields from "
                "tools/oral/qb_content_index_governed.json")

# Candidate-facing text must never carry examiner / production metadata. The
# generator FAILS on a hit rather than scrubbing: the page is the truth, and a
# leak on the page is a live defect to fix at source, not to hide in the index.
LEAK = re.compile(
    r"\((?:[A-Z][a-z]+ )?(?:sir|Sir)\)"     # "(Simon sir)"
    r"|\bGAP-\d"                             # GAP-0123
    r"|\bASC-\d"
    r"|\bP0\b"
    r"|Examiner context:"
    r"|\bTODO\b|\bFIXME\b|\[\[|\]\]",
)

Q_INDEX_RE = re.compile(r"^const Q_INDEX = (\[.*\]);$", re.M)
QB_GROUPS_RE = re.compile(r"^const QB_GROUPS = (\[.*\]);$", re.M)
STAT_RE = re.compile(r'(<span class="stat-val">)(\d+)(</span><span class="stat-label">Questions Live</span>)')
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
VERSION_RE = re.compile(r"<strong>Version:</strong>\s*v?(\d+(?:\.\d+)*)")
INLINE_CHEAT_RE = re.compile(r"<h4>[^<]*Cheat Sheet", re.I)


class BuildFailure(Exception):
    pass


def fail(msg):
    raise BuildFailure(msg)


def natural_file_key(fname):
    parts = re.split(r"(\d+)", fname)
    return [int(p) if p.isdigit() else p for p in parts]


# ------------------------------------------------------------------ inputs

# Correction-log contract (recently_updated). ONE schema, rendered by the hub
# correction log and read by qb_health_check's changelog-gap check:
#   date   YYYY-MM-DD                        required
#   note   human-readable description        required, non-empty string
#   files  list of str, structured metadata  optional, never the description
# "summary" and "files_touched" were a July-2026 authoring drift that left 21
# of 33 entries blank on the live hub; the generator refuses them so a
# regeneration can never re-admit the split.
CORRECTION_KEYS = ("date", "note", "files")
CORRECTION_OBSOLETE_KEYS = ("summary", "files_touched")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def check_corrections(entries):
    """Validate the governed recently_updated array; raise BuildFailure on
    the first contract violation. Order is the governed order (untouched)."""
    if not isinstance(entries, list) or not entries:
        fail("governed recently_updated: missing or empty")
    seen = set()
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            fail("recently_updated[%d]: not an object" % i)
        bad = [k for k in e if k in CORRECTION_OBSOLETE_KEYS]
        if bad:
            fail("recently_updated[%d]: obsolete key(s) %s - use %s"
                 % (i, bad, list(CORRECTION_KEYS)))
        extra = [k for k in e if k not in CORRECTION_KEYS]
        if extra:
            fail("recently_updated[%d]: unknown key(s) %s" % (i, extra))
        if not isinstance(e.get("date"), str) or not DATE_RE.match(e["date"]):
            fail("recently_updated[%d]: date must be YYYY-MM-DD" % i)
        note = e.get("note")
        if not isinstance(note, str) or not note.strip():
            fail("recently_updated[%d] (%s): note missing or blank" % (i, e["date"]))
        if "files" in e and (not isinstance(e["files"], list)
                             or not all(isinstance(f, str) and f.strip() for f in e["files"])):
            fail("recently_updated[%d] (%s): files must be a list of non-empty strings"
                 % (i, e["date"]))
        key = (e["date"], note.strip())
        if key in seen:
            fail("recently_updated[%d] (%s): duplicate correction entry" % (i, e["date"]))
        seen.add(key)
    return entries


def load_governed():
    governed = json.loads(GOVERNED_PATH.read_text(encoding="utf-8"))
    check_corrections(governed.get("recently_updated"))
    return governed


def read_index_html():
    return INDEX_HTML_PATH.read_bytes().decode("utf-8").replace("\r\n", "\n")


def qb_groups(index_text):
    m = QB_GROUPS_RE.search(index_text)
    if not m:
        fail("index.html: QB_GROUPS literal not found")
    groups = json.loads(m.group(1))
    group_of = {}
    for g in groups:
        for c in g.get("cards", []):
            group_of[c["file"]] = g["id"]
    return groups, group_of


def cheatsheets_on_disk():
    """stem (case-insensitive) -> cheat sheet file name, from disk."""
    out = {}
    for p in sorted(glob.glob(str(L.MEO / "QB*.html"))):
        name = os.path.basename(p)
        m = re.match(r"^(QB\S+?)_[Cc]heat[Ss]heet\.html$", name)
        if m:
            out[m.group(1).lower()] = name
    return out


# ---------------------------------------------------------------- derivation

def page_meta(path):
    h = path.read_text(encoding="utf-8")
    tm = TITLE_RE.search(h)
    title = L.strip_tags(tm.group(1)) if tm else path.stem
    # "<QBx> — <Title> | MIW MEO Class 1" -> "<Title>"
    title = re.sub(r"^QB\S+\s+[—-]\s+", "", title)
    title = re.sub(r"\s+\|.*$", "", title).strip()
    vm = VERSION_RE.search(h)
    return title, (vm.group(1) if vm else None), bool(INLINE_CHEAT_RE.search(h))


def letter_of(stem):
    return stem.split("_", 1)[1] if "_" in stem else "A"


def derive(governed, index_text):
    """Return (manifest_dict, q_index_list, per_file_qcount)."""
    _, group_of = qb_groups(index_text)
    cs_disk = cheatsheets_on_disk()
    overrides = governed.get("cheatsheet_overrides", {})
    gov_files = governed.get("files", {})

    files = {}
    q_index = []
    total_q = 0
    for path in sorted(L.qb_files(), key=lambda p: natural_file_key(p.name)):
        fname = path.name
        stem = path.stem
        rows = [r for r in L.parse_qb_file(path) if r["is_question"]]
        if not rows:
            continue
        seen = set()
        questions = []
        for order, r in enumerate(rows, 1):
            anchor = r["anchor"]
            if anchor in seen:
                fail("%s: duplicate anchor %s" % (fname, anchor))
            seen.add(anchor)
            text = r["question_text"]
            if not text:
                fail("%s#%s: empty candidate-facing q-text" % (fname, anchor))
            if LEAK.search(text):
                fail("%s#%s: examiner/production metadata in live q-text: %r"
                     % (fname, anchor, text[:80]))
            questions.append({
                "qnum": r["q_number"],
                "anchor": anchor,
                "id": stem + "#" + anchor,
                "order": order,
                "text": text,
            })
            q_index.append({"q": text, "file": fname,
                            "qb": group_of.get(fname, L.qb_group(fname).lower()),
                            "anchor": anchor})
        title, page_version, inline_cheat = page_meta(path)
        gov = gov_files.get(fname, {})
        tags = sorted({t for r in rows for t in r["tags"].split()})
        cheatsheet = overrides.get(fname) or cs_disk.get(stem.lower())
        entry = {
            "qb_group": L.qb_group(fname),
            "letter": letter_of(stem),
            "title": title,
            "version": page_version or gov.get("version") or "1.0",
            "version_source": "page" if page_version else "governed",
            "tags": tags,
        }
        if cheatsheet:
            entry["cheatsheet"] = cheatsheet
        if inline_cheat:
            entry["cheatsheet_inline"] = True
        if gov.get("corrections_applied"):
            entry["corrections_applied"] = gov["corrections_applied"]
        entry["question_count"] = len(questions)
        entry["questions"] = questions
        files[fname] = entry
        total_q += len(questions)

    manifest = {
        "manifest_version": MANIFEST_VERSION,
        "generated_by": GENERATED_BY,
        "source": "live QB HTML under meoclass1/ - identity is file + anchor; "
                  "qnum is read from the anchor id, order is document position",
        "total_questions": total_q,
        "total_files": len(files),
        "recently_updated": governed.get("recently_updated", []),
        "files": files,
    }
    return manifest, q_index


# ----------------------------------------------------------------- rendering

def render_manifest(manifest):
    return json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"


def render_q_index_line(q_index):
    return "const Q_INDEX = %s;" % json.dumps(q_index, ensure_ascii=False)


def patch_index_html(index_text, manifest, q_index):
    """Return index.html text with the three generator-owned regions rewritten."""
    if len(Q_INDEX_RE.findall(index_text)) != 1:
        fail("index.html: Q_INDEX line found %d times, expected 1"
             % len(Q_INDEX_RE.findall(index_text)))
    text = Q_INDEX_RE.sub(lambda m: render_q_index_line(q_index), index_text, count=1)

    # each card's qcount, in place, without re-serialising QB_GROUPS
    for fname, entry in manifest["files"].items():
        pat = re.compile(r'("file": "%s", "title": "[^"]*", "qcount": )(\d+)' % re.escape(fname))
        hits = pat.findall(text)
        if len(hits) != 1:
            fail("index.html: QB_GROUPS card for %s found %d times, expected 1" % (fname, len(hits)))
        text = pat.sub(lambda m: m.group(1) + str(entry["question_count"]), text, count=1)

    if len(STAT_RE.findall(text)) != 1:
        fail("index.html: 'Questions Live' hero counter found %d times, expected 1"
             % len(STAT_RE.findall(text)))
    text = STAT_RE.sub(lambda m: m.group(1) + str(manifest["total_questions"]) + m.group(3),
                       text, count=1)
    return text


# --------------------------------------------------------------------- write

def write_atomic_lf(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = text.replace("\r\n", "\n").encode("utf-8")
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".staging", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def build():
    governed = load_governed()
    index_text = read_index_html()
    manifest, q_index = derive(governed, index_text)
    return manifest, render_manifest(manifest), patch_index_html(index_text, manifest, q_index)


def main(argv):
    check_only = "--check" in argv
    out_dir = None
    if "--out-dir" in argv:
        out_dir = Path(argv[argv.index("--out-dir") + 1])
    try:
        manifest, manifest_text, index_text = build()
    except BuildFailure as e:
        print("BUILD FAILURE: %s" % e)
        return 2
    print("qb_content_index: %d files, %d canonical questions"
          % (manifest["total_files"], manifest["total_questions"]))

    if check_only:
        stale = []
        if MANIFEST_PATH.read_bytes().decode("utf-8").replace("\r\n", "\n") != manifest_text:
            stale.append(str(MANIFEST_PATH.relative_to(L.REPO)))
        if read_index_html() != index_text:
            stale.append(str(INDEX_HTML_PATH.relative_to(L.REPO)))
        if stale:
            print("--check: STALE - would rewrite %s" % ", ".join(stale))
            return 3
        print("--check: outputs on disk already match the live derivation")
        return 0

    if out_dir:
        m_path = out_dir / "qb_content_index.json"
        i_path = out_dir / "index.html"
    else:
        m_path, i_path = MANIFEST_PATH, INDEX_HTML_PATH
    write_atomic_lf(m_path, manifest_text)
    write_atomic_lf(i_path, index_text)
    print("wrote %s and %s (Q_INDEX line, card qcounts, hero counter only)" % (m_path, i_path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
