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
  S  reintroduce "via Nixon" in a note      -> hygiene      (editorial pass 2026-08-19)
  T  add a WhatsApp reference               -> hygiene
  U  add commit SHAs                        -> hygiene
  V  add "known_traps.md Entry 6"           -> hygiene
  W  add GAP-/P0- ticket ids                -> hygiene
  X  blank a note                           -> corrections / note_quality
  Y  restore a pre-cleanup unsafe note      -> hygiene
  Z  hygienic but empty "Content updated."  -> note_quality

  PYTHONIOENCODING=utf-8 python tools/oral/mutate_qb_content_index.py [--keep]
Exit 0 only when every mutation is caught by its named check.

Mutation quality (2026-08-19 hardening): a mutation must actually change the
scratch artefacts - one that leaves them byte-identical is reported as
"NOT APPLIED" and counts as an escape, never as a validator catch. Hygiene
mutations (S T U V W Y) additionally assert the CORRECTION_FORBIDDEN label
that fired. Regression strings are pinned in this file; nothing is fetched
from git history. Live artefacts are hashed before and after the run.
"""
from __future__ import annotations

import hashlib
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
import pathlib

# Windows encodes a child process's stdout with the locale codec, so printing a
# single non-cp1252 character -- U+26A0, which this toolchain reports and
# deliberately injects -- kills the process. When that happens between applying
# a mutation and restoring it, a mutated product page is left on disk. This tool
# reaches no other shared module, so the contract is imported explicitly.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from oral_bytes import enable_utf8_stdio      # noqa: E402

enable_utf8_stdio()



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


def _note(work, idx, text):
    m, _ = load(work)
    m["recently_updated"][idx]["note"] = text
    save(work, m)


def _append_note(work, idx, suffix):
    """Append a pinned regression fragment to row `idx`. Rows are addressed by
    position only for variety; the fragment never depends on the row's current
    wording, so a governed-log prepend (which shifted every index by 3 on
    2026-08-19 and silently no-op'd the old str.replace-on-anchor S/U) can
    never turn the mutation into a no-op again."""
    m, _ = load(work)
    _note(work, idx, m["recently_updated"][idx]["note"] + suffix)


# Pinned regression strings (§16): the two dataset regressions the editorial
# cleanup removed. Kept literal in test code - never fetched from git history.
REGRESSION_VIA_NIXON = " Re-evaluation request received via Nixon."
REGRESSION_SHA = " Applied under a1b2c3d and 30fb6f5."   # hex letters + digits, no "commit" word:
                                                          # the SHA regex itself must be load-bearing


def mut_S(work):                                     # reintroduce "via Nixon"
    _append_note(work, 3, REGRESSION_VIA_NIXON)


def mut_T(work):                                     # WhatsApp reference
    _append_note(work, 0, " Sourced from a WhatsApp report.")


def mut_U(work):                                     # commit SHA (bare, no "commit" word)
    _append_note(work, 9, REGRESSION_SHA)


def mut_V(work):                                     # known_traps.md Entry 6
    m, _ = load(work)
    e = m["recently_updated"][1]
    _note(work, 1, e["note"] + " See known_traps.md Entry 6.")


def mut_W(work):                                     # GAP-/P0- ticket ids
    m, _ = load(work)
    e = m["recently_updated"][11]
    _note(work, 11, e["note"] + " Closes GAP-04 and P0-02.")


def mut_X(work):                                     # blank a note (also a "clean" note by regex)
    _note(work, 7, "")


PRE_CLEANUP_NOTE_2 = (   # verbatim opening of governed row 2 as it stood at ca881c4
    "Candidate-flagged re-evaluation request (via Nixon, screenshot) on Q5 (Q15: Rajappan, "
    "war-zone/3 Indian crew died investigation). Verification against primary sources found "
    "the Casualty Link's True Confidence (2024) reference implicitly mismatched the question's "
    "'Indian crew' premise ... q-version Q5 v1.1->v1.2. See known_traps.md Entry 6 scope note.")


def mut_Y(work):                                     # generator restores the stale unsafe note
    _note(work, 2, PRE_CLEANUP_NOTE_2)


def mut_Z(work):                                     # a note that passes hygiene but says nothing
    _note(work, 20, "Content updated.")


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
    # hygiene mutations also name the CORRECTION_FORBIDDEN label that must fire
    ("S reintroduce 'via Nixon'", mut_S, {"hygiene"}, {"workflow: via <person>", "person: Nixon"}),
    ("T add WhatsApp reference", mut_T, {"hygiene"}, {"chat: WhatsApp/Telegram"}),
    ("U add commit SHAs", mut_U, {"hygiene"}, {"repo: commit/SHA"}),
    ("V add known_traps.md Entry 6", mut_V, {"hygiene"}, {"repo: known_traps", "repo: Entry n"}),
    ("W add GAP-/P0- ids", mut_W, {"hygiene"}, {"ticket: GAP-/P0-/HOLD-"}),
    ("X blank a note", mut_X, {"corrections", "note_quality"}),
    ("Y restore pre-cleanup unsafe note", mut_Y, {"hygiene"}, {"workflow: via <person>", "repo: known_traps"}),
    ("Z hygienic but empty 'Content updated.'", mut_Z, {"note_quality"}),
]


def run_validator(work):
    V.RESULTS.clear()
    V.FAILS.clear()
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = V.main(["--manifest", str(work / "qb_content_index.json"),
                     "--index-html", str(work / "index.html"), "--quiet"])
    return rc, set(V.FAILS)


def _digest(work):
    """SHA-256 of both scratch artefacts - proves a mutation actually landed."""
    h = hashlib.sha256()
    for f in ("qb_content_index.json", "index.html"):
        h.update((work / f).read_bytes())
    return h.hexdigest()


def _hygiene_labels(work):
    m, _ = load(work)
    return {lab for _, _, lab, _ in B.correction_hygiene_violations(m.get("recently_updated"))}


def _live_hashes():
    return {p: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (B.MANIFEST_PATH, B.INDEX_HTML_PATH, B.GOVERNED_PATH)}


def main(argv):
    keep = "--keep" in argv
    live_before = _live_hashes()
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
    base_digest = _digest(base)
    escapes = crashes = 0
    for row in MUTATIONS:
        name, fn, expected = row[0], row[1], row[2]
        exp_labels = row[3] if len(row) > 3 else set()
        work = root / name.split()[0]
        work.mkdir()
        shutil.copy(B.MANIFEST_PATH, work / "qb_content_index.json")
        shutil.copy(B.INDEX_HTML_PATH, work / "index.html")
        crashed, applied, labels = False, False, set()
        try:
            fn(work)
            applied = _digest(work) != base_digest
            rc, fails = run_validator(work)
            if exp_labels:
                labels = _hygiene_labels(work)
        except Exception as e:           # a crash is an escape, not a catch
            rc, fails, crashed = 1, {"<crash: %s>" % e}, True
        # A mutation that leaves the artefacts byte-identical never reached the
        # validator: name it NOT APPLIED rather than letting `observed=[]` pass
        # for a validator blind spot (the S/U escape class of 2026-08-19).
        semantic = (rc != 0) and bool(fails & expected) and not crashed and applied
        label_ok = (not exp_labels) or bool(labels & exp_labels)
        caught = semantic and label_ok
        if crashed:
            verdict = "ESCAPE (crash)"
        elif not applied:
            verdict = "ESCAPE (NOT APPLIED - mutation is a no-op)"
        elif not semantic:
            verdict = "ESCAPE (unnamed / no failure)"
        elif not label_ok:
            verdict = "ESCAPE (wrong hygiene label)"
        else:
            verdict = "CAUGHT (semantic)"
        print("%-40s %s" % (name, verdict))
        print("    target=%s  applied=%s  expected=%s  observed=%s%s" % (
            "scratch copy of meoclass1/qb_content_index.json + index.html",
            applied, sorted(expected), sorted(fails),
            ("  hygiene_labels=%s" % sorted(labels & exp_labels) if exp_labels else "")))
        if not caught:
            escapes += 1
        if crashed:
            crashes += 1
    if not keep:
        shutil.rmtree(root, ignore_errors=True)
    live_after = _live_hashes()
    restored = live_before == live_after
    print("mutations: %d run, %d escape(s), %d crash(es); live artefacts byte-identical: %s"
          % (len(MUTATIONS), escapes, crashes, restored))
    if not restored:
        print("RESIDUE: live artefacts changed during the run - %s" %
              [str(p) for p in live_before if live_before[p] != live_after[p]])
    return 1 if (escapes or not restored) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
