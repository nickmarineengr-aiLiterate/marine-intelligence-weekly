"""Mutation harness for validate_qb_content_index.py.

Each mutation copies the two derived artefacts to a scratch directory, injects
one defect into the copy, runs the validator against the copy, and requires
that (a) the validator exits non-zero and (b) the NAMED check fails - a crash
or an unrelated failure is an escape, not a catch. Live QB HTML is never
touched.

  A  drop one real q-card record            -> count / complete
  B  add a navigation/revision card record  -> no_nonquestion / no_extras
  C  shift an anchor to the next q-number   -> identity / text
  D  reintroduce "(Simon sir)" in QB1_K#q8  -> leak / qb1k_q8
  E  swap the two CSR question texts        -> csr_distinct / text
  F  duplicate a record                     -> unique
  G  stale the text of an enrichment        -> p0_enriched / text
  H  reorder files non-deterministically    -> order / determinism
  I  drift Q_INDEX from the manifest        -> q_index
  J  drift a QB_GROUPS card qcount          -> cards
  K  point one anchor at a missing card     -> no_extras
  L  blank one correction note              -> corrections
  M  restore obsolete "summary" on one row  -> corrections
  N  files_touched / scalar files           -> corrections
  O  duplicate a correction record          -> corrections
  P  renderer reads e.summary again         -> renderer
  Q  generator drops corrections            -> corrections_preserved / governed
  R  restore QB2_C q2 scaffolding text      -> leak / text  (repaired 2026-08-19)

  PYTHONIOENCODING=utf-8 python tools/oral/mutate_qb_content_index.py [--keep]
Exit 0 only when every mutation is caught by its named check.
"""
from __future__ import annotations

import io
import json
import re
import shutil
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_qb_content_index as B      # noqa: E402
import validate_qb_content_index as V   # noqa: E402


def load(work):
    m = json.loads((work / "qb_content_index.json").read_text(encoding="utf-8"))
    h = (work / "index.html").read_bytes().decode("utf-8")
    return m, h


def save(work, m=None, h=None):
    if m is not None:
        (work / "qb_content_index.json").write_bytes(
            (json.dumps(m, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    if h is not None:
        (work / "index.html").write_bytes(h.encode("utf-8"))


def qs(m, fname):
    return m["files"][fname]["questions"]


# ------------------------------------------------------------------ mutations

def mut_A(work):
    m, _ = load(work)
    qs(m, "QB1_K.html").pop(2)                       # drop q3, keep count field stale on purpose
    save(work, m)


def mut_B(work):
    m, _ = load(work)
    qs(m, "QB1_A.html").append({"qnum": 32, "anchor": "family-trees", "id": "QB1_A#family-trees",
                                "order": 32, "text": "Convention family trees (revision map)"})
    m["files"]["QB1_A.html"]["question_count"] += 1
    m["total_questions"] += 1
    save(work, m)


def mut_C(work):
    m, _ = load(work)
    for q in qs(m, "QB2_B.html"):                    # every record slides one anchor forward
        n = int(q["anchor"][1:]) + 1
        q["anchor"] = "q%d" % n
        q["id"] = "QB2_B#q%d" % n
        q["qnum"] = n
    save(work, m)


def mut_D(work):
    m, h = load(work)
    for q in qs(m, "QB1_K.html"):
        if q["anchor"] == "q8":
            q["text"] = '(Simon sir) "What is CSR?" — what does he mean, and what is its scope?'
    h = h.replace('"q": "\\"What is CSR?\\" — what does the examiner mean, and what is its scope?"',
                  '"q": "(Simon sir) \\"What is CSR?\\" — what does he mean, and what is its scope?"')
    save(work, m, h)


def mut_E(work):
    m, _ = load(work)
    a = next(q for q in qs(m, "QB1_K.html") if q["anchor"] == "q8")
    b = next(q for q in qs(m, "QB5_C_B.html") if q["anchor"] == "q8")
    a["text"], b["text"] = b["text"], a["text"]
    save(work, m)


def mut_F(work):
    m, _ = load(work)
    lst = qs(m, "QB4_A.html")
    lst.append(dict(lst[0]))
    m["files"]["QB4_A.html"]["question_count"] += 1
    m["total_questions"] += 1
    save(work, m)


def mut_G(work):
    m, _ = load(work)
    for q in qs(m, "QB6.html"):
        if q["anchor"] == "q10":
            q["text"] = "Explain tri-fuel engines."      # pre-enrichment stale wording
    save(work, m)


def mut_H(work):
    m, _ = load(work)
    items = list(m["files"].items())
    items = items[::-1]                                  # any non-natural order
    m["files"] = dict(items)
    save(work, m)


def mut_I(work):
    m, h = load(work)
    line = B.Q_INDEX_RE.search(h)
    qi = json.loads(line.group(1))
    qi[5], qi[6] = qi[6], qi[5]
    h = h[:line.start(1)] + json.dumps(qi, ensure_ascii=False) + h[line.end(1):]
    save(work, None, h)


def mut_J(work):
    m, h = load(work)
    h = h.replace('"file": "QB1_A.html", "title": "Conventions & Liability Law", "qcount": 31',
                  '"file": "QB1_A.html", "title": "Conventions & Liability Law", "qcount": 33')
    save(work, None, h)


def mut_K(work):
    m, _ = load(work)
    q = qs(m, "QB1_K.html")[-1]
    q["anchor"] = "q99"
    q["id"] = "QB1_K#q99"
    q["qnum"] = 99
    save(work, m)


def mut_L(work):
    m, _ = load(work)
    m["recently_updated"][3]["note"] = "   "
    save(work, m)


def mut_M(work):
    m, _ = load(work)
    e = m["recently_updated"][5]
    e["summary"] = e.pop("note")                     # the old split, one row
    save(work, m)


def mut_N(work):
    m, _ = load(work)
    e = m["recently_updated"][0]
    e["files"] = ", ".join(e["files"])               # scalar where a list belongs
    e2 = m["recently_updated"][1]
    e2["files_touched"] = e2.pop("files")            # the other old key
    save(work, m)


def mut_O(work):
    m, _ = load(work)
    m["recently_updated"].append(dict(m["recently_updated"][2]))
    save(work, m)


def mut_P(work):
    m, h = load(work)
    h = h.replace("${(e.note||'').replace(/</g,'&lt;')}", "${(e.summary||'').replace(/</g,'&lt;')}")
    save(work, None, h)


def mut_Q(work):
    m, _ = load(work)
    m.pop("recently_updated")                        # generator "forgot" the governed log
    for f in m["files"].values():
        f.pop("corrections_applied", None)
    save(work, m)


def mut_R(work):
    m, h = load(work)
    new = "How would you, as Chief Engineer, approach a fire in a container carrying undeclared dangerous goods?"
    old = "15-Second Answer (Elevator Pitch)**"
    for q in qs(m, "QB2_C.html"):
        if q["anchor"] == "q2":
            q["text"] = old
    h = h.replace(json.dumps(new, ensure_ascii=False), json.dumps(old, ensure_ascii=False))
    save(work, m, h)


MUTATIONS = [
    ("A drop real record", mut_A, {"count", "complete"}),
    ("B add revision card", mut_B, {"no_nonquestion", "no_extras"}),
    ("C shift anchors +1", mut_C, {"text", "no_extras", "complete"}),
    ("D reintroduce (Simon sir)", mut_D, {"leak", "qb1k_q8"}),
    ("E swap CSR texts", mut_E, {"csr_distinct", "text"}),
    ("F duplicate record", mut_F, {"unique"}),
    ("G stale enrichment text", mut_G, {"p0_enriched", "text"}),
    ("H nondeterministic file order", mut_H, {"order", "determinism"}),
    ("I Q_INDEX drift", mut_I, {"q_index"}),
    ("J card qcount drift", mut_J, {"cards"}),
    ("K anchor to missing card", mut_K, {"no_extras"}),
    ("L blank correction note", mut_L, {"corrections"}),
    ("M obsolete summary key", mut_M, {"corrections"}),
    ("N files not a list / files_touched", mut_N, {"corrections"}),
    ("O duplicate correction", mut_O, {"corrections"}),
    ("P renderer reads e.summary", mut_P, {"renderer"}),
    ("Q generator drops corrections", mut_Q, {"corrections_preserved", "governed"}),
    ("R restore QB2_C scaffolding text", mut_R, {"leak", "text"}),
]


def run_validator(work):
    V.RESULTS.clear()
    V.FAILS.clear()
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = V.main(["--manifest", str(work / "qb_content_index.json"),
                     "--index-html", str(work / "index.html"), "--quiet"])
    return rc, set(V.FAILS)


def main(argv):
    keep = "--keep" in argv
    root = Path(tempfile.mkdtemp(prefix="qbidx-mut-"))
    # baseline: the committed artefacts must be green before mutating them
    base = root / "base"
    base.mkdir()
    shutil.copy(B.MANIFEST_PATH, base / "qb_content_index.json")
    shutil.copy(B.INDEX_HTML_PATH, base / "index.html")
    rc, fails = run_validator(base)
    if rc != 0:
        print("BASELINE NOT GREEN: %s - mutations are meaningless" % sorted(fails))
        return 2
    escapes = 0
    for name, fn, expected in MUTATIONS:
        work = root / name.split()[0]
        work.mkdir()
        shutil.copy(B.MANIFEST_PATH, work / "qb_content_index.json")
        shutil.copy(B.INDEX_HTML_PATH, work / "index.html")
        try:
            fn(work)
            rc, fails = run_validator(work)
            crashed = False
        except Exception as e:           # a crash is an escape, not a catch
            rc, fails, crashed = 1, {"<crash: %s>" % e}, True
        caught = (rc != 0) and bool(fails & expected) and not crashed
        print("%-32s %s  named=%s  observed=%s" % (
            name, "CAUGHT " if caught else "ESCAPE ", sorted(expected), sorted(fails)))
        if not caught:
            escapes += 1
    print("mutations: %d run, %d escape(s)" % (len(MUTATIONS), escapes))
    if not keep:
        shutil.rmtree(root, ignore_errors=True)
    return 1 if escapes else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
