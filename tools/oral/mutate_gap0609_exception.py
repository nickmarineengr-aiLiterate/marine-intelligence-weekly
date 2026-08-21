"""Mutation harness for validate_gap0609_exception.py.

Each mutation is a defect the validator must catch. A mutation that the
validator still passes is an ESCAPE. A mutation whose bytes do not actually
change is a NO-OP - it proves nothing, and is reported as loudly as an escape,
because a stale anchor that silently fails to match is exactly how a mutation
harness reports a green it has not earned.

Everything runs in a scratch copy of the repo's relevant files; the working
tree is never modified.

  PYTHONIOENCODING=utf-8 python tools/oral/mutate_gap0609_exception.py

Exit 0 only when every mutation is APPLIED and CAUGHT.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import pathlib

# Windows encodes a child process's stdout with the locale codec, so printing a
# single non-cp1252 character -- U+26A0, which this toolchain reports and
# deliberately injects -- kills the process. When that happens between applying
# a mutation and restoring it, a mutated product page is left on disk. This tool
# reaches no other shared module, so the contract is imported explicitly.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from oral_bytes import enable_utf8_stdio      # noqa: E402

enable_utf8_stdio()


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REL_REVIEW = os.path.join("meoclass1", "oral-intelligence", "examiner-audit",
                          "GAP0609_EXCEPTION_REVIEW.json")
REL_INDEX = os.path.join("meoclass1", "qb_content_index.json")
VALIDATOR = os.path.join("tools", "oral", "validate_gap0609_exception.py")


def digest(path):
    return hashlib.sha256(io.open(path, "rb").read()).hexdigest()


# ---- mutations -----------------------------------------------------------
# Each takes the scratch root and returns a short label. They must mutate.

def m_a(root):
    """A. leave GAP-0609 unresolved"""
    p = os.path.join(root, REL_REVIEW)
    d = json.load(io.open(p, encoding="utf-8"))
    d["final_disposition"] = "NEW_CARD_REVIEW_REQUIRED"
    io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
    return "A leave GAP-0609 unresolved"


def m_b(root):
    """B. NEW disposition, but the card is missing from the live page"""
    d = json.load(io.open(os.path.join(root, REL_REVIEW), encoding="utf-8"))
    fname, _, anc = d["target"].partition("#")
    p = os.path.join(root, "meoclass1", fname)
    html = io.open(p, encoding="utf-8").read()
    html = html.replace('<div class="q-card" id="%s"' % anc,
                        '<div class="q-card" id="%s_removed"' % anc, 1)
    io.open(p, "w", encoding="utf-8", newline="").write(html)
    return "B NEW with missing card"


def m_c(root):
    """C. existing-card decision whose target does not resolve"""
    p = os.path.join(root, REL_REVIEW)
    d = json.load(io.open(p, encoding="utf-8"))
    d["final_disposition"] = "ENRICH_EXISTING_QB"
    d["target"] = "QB4_G.html#q999"
    d["baseline"]["canonical_questions_after"] = d["baseline"]["canonical_questions_before"]
    io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
    return "C EXISTING decision with missing target"


def m_d(root):
    """D. blank reasoning"""
    p = os.path.join(root, REL_REVIEW)
    d = json.load(io.open(p, encoding="utf-8"))
    d["target_selection_reason"] = ""
    d["last_resort_test"]["B_absorbable_as_bounded_enrichment"] = ""
    io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
    return "D blank reasoning"


def m_e(root):
    """E. duplicate anchor for the new card"""
    d = json.load(io.open(os.path.join(root, REL_REVIEW), encoding="utf-8"))
    fname, _, anc = d["target"].partition("#")
    p = os.path.join(root, "meoclass1", fname)
    html = io.open(p, encoding="utf-8").read()
    dup = '\n<div class="q-card" id="%s">\n  <div class="q-header"></div>\n</div>\n' % anc
    marker = '<div id="no-results">'
    assert marker in html
    html = html.replace(marker, dup + marker, 1)
    io.open(p, "w", encoding="utf-8", newline="").write(html)
    return "E duplicate anchor"


def m_f(root):
    """F. production marker injected into candidate-facing card text"""
    d = json.load(io.open(os.path.join(root, REL_REVIEW), encoding="utf-8"))
    fname, _, anc = d["target"].partition("#")
    p = os.path.join(root, "meoclass1", fname)
    html = io.open(p, encoding="utf-8").read()
    needle = '<div class="q-num-badge">13</div>'
    assert needle in html
    html = html.replace(needle, needle + "<!-- GAP-0609 ENR-049 -->", 1)
    io.open(p, "w", encoding="utf-8", newline="").write(html)
    return "F production marker in candidate text"


def m_g(root):
    """G. a pre-existing destination card is altered"""
    p = os.path.join(root, "meoclass1", "QB4_G.html")
    html = io.open(p, encoding="utf-8").read()
    needle = "Hull damage or oil pollution incident"
    assert needle in html
    html = html.replace(needle, "Hull damage incident", 1)
    io.open(p, "w", encoding="utf-8", newline="").write(html)
    # the index still describes the old text, so the derivation no longer matches
    ip = os.path.join(root, REL_INDEX)
    idx = json.load(io.open(ip, encoding="utf-8"))
    for q in idx["files"]["QB4_G.html"]["questions"]:
        if q["anchor"] == "q7":
            q["text"] = "Hull damage incident"
    io.open(ip, "w", encoding="utf-8").write(json.dumps(idx, ensure_ascii=False, indent=2))
    return "G pre-existing card altered"


def m_h(root):
    """H. wrong final canonical count for a NEW disposition"""
    p = os.path.join(root, REL_REVIEW)
    d = json.load(io.open(p, encoding="utf-8"))
    d["baseline"]["canonical_questions_after"] = d["baseline"]["canonical_questions_before"]
    io.open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
    return "H wrong final canonical count"


MUTATIONS = [m_a, m_b, m_c, m_d, m_e, m_f, m_g, m_h]

# G alters the page but not the review record; the validator catches it through
# the q-text/answer derivation only if the card it names moved. Mutations that
# touch the page are digested on the page, the rest on the review record.
PAGE_MUTATIONS = {m_b, m_e, m_f, m_g}


def run_once(fn):
    scratch = tempfile.mkdtemp(prefix="gap0609_mut_")
    try:
        for rel in (REL_REVIEW, REL_INDEX, VALIDATOR,
                    os.path.join("meoclass1", "QB4_G.html")):
            dst = os.path.join(scratch, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(os.path.join(ROOT, rel), dst)

        watched = os.path.join(scratch, "meoclass1", "QB4_G.html") \
            if fn in PAGE_MUTATIONS else os.path.join(scratch, REL_REVIEW)
        before = digest(watched)
        label = fn(scratch)
        after = digest(watched)
        applied = before != after

        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        # the validator resolves ROOT from its own location, so run the copy
        proc = subprocess.run(
            [sys.executable, os.path.join(scratch, VALIDATOR)],
            capture_output=True, env=env, cwd=scratch)
        out = proc.stdout.decode("utf-8", "replace") + proc.returncode * 0 * ""
        caught = proc.returncode != 0
        return label, applied, caught, out
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main():
    print("GAP-0609 exception mutation harness")
    escapes = noops = crashes = 0
    for fn in MUTATIONS:
        try:
            label, applied, caught, out = run_once(fn)
        except Exception as exc:                     # noqa: BLE001
            crashes += 1
            print("  CRASH     %s -> %s" % (fn.__name__, exc))
            continue
        if not applied:
            noops += 1
            print("  NOT APPLIED  %s (bytes unchanged - mutation proves nothing)" % label)
            continue
        if not caught:
            escapes += 1
            print("  ESCAPE    %s (validator still passed)" % label)
            continue
        print("  caught    %s" % label)

    print("mutations=%d escapes=%d no-ops=%d crashes=%d"
          % (len(MUTATIONS), escapes, noops, crashes))
    return 1 if (escapes or noops or crashes) else 0


if __name__ == "__main__":
    sys.exit(main())
