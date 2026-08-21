"""Mutation harness proving validate_batch_a.py is load-bearing.

Each mutation is applied to the live Batch-A pages, the validator is run, and the
page is restored from a byte snapshot taken beforehand. A mutation that does not
change any bytes is reported as NOT APPLIED rather than silently counted as caught -
a stale no-op mutation is the failure mode this harness exists to avoid.

Exit 0 when every mutation is applied, caught, and cleanly restored.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import pathlib

# Windows encodes a child process's stdout with the locale codec, so printing a
# single non-cp1252 character -- U+26A0, which this toolchain reports and
# deliberately injects -- kills the process. When that happens between applying
# a mutation and restoring it, a mutated product page is left on disk. This tool
# reaches no other shared module, so the contract is imported explicitly.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from oral_bytes import enable_utf8_stdio      # noqa: E402

enable_utf8_stdio()


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB = REPO / "meoclass1"
MANIFEST = json.loads((HERE / "batch_a_manifest.json").read_text(encoding="utf-8"))
CARDS = MANIFEST["cards"]
FILES = sorted({c["file"] for c in CARDS})


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def snapshot():
    return {f: (QB / f).read_text(encoding="utf-8") for f in FILES}


def restore(snap):
    for f, text in snap.items():
        (QB / f).write_text(text, encoding="utf-8", newline="")


def run_validator():
    r = subprocess.run([sys.executable, str(HERE / "validate_batch_a.py")],
                       capture_output=True, cwd=str(REPO),
                       env=dict(__import__("os").environ, PYTHONIOENCODING="utf-8"))
    out = r.stdout.decode("utf-8", "replace")
    fails = [ln.strip() for ln in out.splitlines() if ln.startswith("FAIL")]
    return r.returncode, fails


def card_span(text, anchor):
    """(start, end) of the q-card div carrying `anchor`, by balancing <div> tags."""
    m = re.search(r'<div class="q-card"[^>]*id="%s"' % anchor, text)
    if not m:
        raise AssertionError("anchor %s not found" % anchor)
    depth = 0
    for t in re.finditer(r"<(/?)div\b[^>]*>", text[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return m.start(), m.start() + t.end()
    raise AssertionError("unbalanced card %s" % anchor)


# ------------------------------------------------------------------ mutations

def m_A(snap):
    """Remove one authorised new q-card entirely."""
    c = CARDS[0]
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    (QB / c["file"]).write_text(t[:s] + t[e:], encoding="utf-8", newline="")


def m_B(snap):
    """Duplicate a new card's anchor onto a second element."""
    c = CARDS[1]
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    (QB / c["file"]).write_text(t[:e] + t[s:e] + t[e:], encoding="utf-8", newline="")


def m_C(snap):
    """Break the authorised gap-id linkage: move a card to a different anchor."""
    c = CARDS[2]
    t = snap[c["file"]]
    (QB / c["file"]).write_text(
        t.replace('id="%s"' % c["anchor"], 'id="q97"', 1), encoding="utf-8", newline="")


def m_D(snap):
    """Add a ninth, unauthorised new card to a Batch-A destination."""
    c = CARDS[3]
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    clone = t[s:e].replace('id="%s"' % c["anchor"], 'id="q96"', 1)
    (QB / c["file"]).write_text(t[:e] + clone + t[e:], encoding="utf-8", newline="")


def m_E(snap):
    """Blank a new card's answer body."""
    c = CARDS[4]
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    card = t[s:e]
    stripped = re.sub(r'(<div class="q-answer">).*?(</div>\s*</div>\s*$)',
                      r"\1\2", card, flags=re.S)
    if stripped == card:
        stripped = re.sub(r'(<div class="q-answer">).*(<div class="q-footer">)',
                          r"\1\2", card, flags=re.S)
    (QB / c["file"]).write_text(t[:s] + stripped + t[e:], encoding="utf-8", newline="")


def m_F(snap):
    """Insert an editorial marker into candidate-visible answer text."""
    c = CARDS[5]
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    card = t[s:e].replace("</h4>", "</h4><p>⚠CORRECTED: TODO verify this before publication.</p>", 1)
    (QB / c["file"]).write_text(t[:s] + card + t[e:], encoding="utf-8", newline="")


def m_G(snap):
    """Break DOM parentage - a stray close that lifts the card out of #q-feed."""
    c = CARDS[6]
    t = snap[c["file"]]
    s, _ = card_span(t, c["anchor"])
    (QB / c["file"]).write_text(t[:s] + "</div>\n" + t[s:], encoding="utf-8", newline="")


def m_H(snap):
    """Leak a production family id into candidate-visible text."""
    c = CARDS[7]
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    card = t[s:e].replace("</h4>", "</h4><p>Source: %s / %s.</p>"
                          % (c["family_id"], c["production_action_id"]), 1)
    (QB / c["file"]).write_text(t[:s] + card + t[e:], encoding="utf-8", newline="")


MUTATIONS = [
    ("A", "remove one authorised new q-card", m_A),
    ("B", "duplicate a new card anchor", m_B),
    ("C", "break the authorised gap-id linkage", m_C),
    ("D", "add a ninth unauthorised card", m_D),
    ("E", "blank a new card's answer body", m_E),
    ("F", "insert an editorial marker", m_F),
    ("G", "break DOM parentage", m_G),
    ("H", "leak a production family id", m_H),
]


def main():
    base = snapshot()
    base_digests = {f: digest(t) for f, t in base.items()}

    rc, fails = run_validator()
    if rc != 0:
        print("BASELINE NOT GREEN: validate_batch_a.py exit=%d" % rc)
        for f in fails:
            print("  " + f)
        return 2

    escapes = crashes = not_applied = 0
    for key, name, fn in MUTATIONS:
        try:
            fn(base)
        except Exception as exc:                       # noqa: BLE001
            print("%s  %-40s MUTATION CRASHED: %s" % (key, name, exc))
            crashes += 1
            restore(base)
            continue

        now = {f: digest((QB / f).read_text(encoding="utf-8")) for f in FILES}
        if now == base_digests:
            print("%s  %-40s NOT APPLIED (no bytes changed)" % (key, name))
            not_applied += 1
            restore(base)
            continue

        rc, fails = run_validator()
        verdict = "CAUGHT" if rc != 0 else "ESCAPE"
        if rc == 0:
            escapes += 1
        print("%s  %-40s exit=%d fails=%d  %s" % (key, name, rc, len(fails), verdict))
        for f in fails[:2]:
            print("      " + f[:150])

        restore(base)
        after = {f: digest((QB / f).read_text(encoding="utf-8")) for f in FILES}
        if after != base_digests:
            print("      RESTORE FAILED for %s"
                  % [f for f in FILES if after[f] != base_digests[f]])
            crashes += 1

    rc, _ = run_validator()
    print("\nrestored: validator exit=%d; pages byte-identical: %s"
          % (rc, all(digest((QB / f).read_text(encoding="utf-8")) == base_digests[f]
                     for f in FILES)))
    print("%d mutations, %d escape(s), %d not applied, %d crash(es)"
          % (len(MUTATIONS), escapes, not_applied, crashes))
    return 1 if (escapes or crashes or not_applied or rc) else 0


if __name__ == "__main__":
    sys.exit(main())
