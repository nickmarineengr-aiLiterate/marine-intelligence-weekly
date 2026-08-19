"""Mutation harness proving validate_batch_c.py is load-bearing.

Each mutation is applied to the live Batch-C pages, the validator is run, and the
page is restored from a byte snapshot taken beforehand. A mutation that changes
no bytes is reported as NOT APPLIED rather than silently counted as caught - a
stale no-op mutation is the failure mode this harness exists to avoid.

Line endings: two of the three Batch-C destinations (QB9_H, QB5_I) are CRLF in
the working tree while QB4_G is LF. Every read and write here uses newline="" so
a restore cannot quietly rewrite a CRLF page to LF - which a snapshot taken with
universal newlines would not detect, because both sides would already be
normalised. That is not theoretical here: the majority of these pages are CRLF.

Mutation H is the currentness guard. The stowaway card's whole value is that it
cites resolution FAL.20(50), adopted 27 March 2026, rather than A.871(20), the
predecessor that most training material still quotes. H downgrades the citation
to A.871(20) and requires the validator to notice - the same class of trap
Batch B caught with MEPC.1/Circ.815 against 896.

Exit 0 when every mutation is applied, caught, and cleanly restored.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB = REPO / "meoclass1"
MANIFEST = json.loads((HERE / "batch_c_manifest.json").read_text(encoding="utf-8"))
CARDS = MANIFEST["cards"]
FILES = sorted({c["file"] for c in CARDS})


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read(f):
    return (QB / f).read_text(encoding="utf-8", newline="")


def write(f, text):
    (QB / f).write_text(text, encoding="utf-8", newline="")


def snapshot():
    return {f: read(f) for f in FILES}


def restore(snap):
    for f, text in snap.items():
        write(f, text)


def run_validator():
    r = subprocess.run([sys.executable, str(HERE / "validate_batch_c.py")],
                       capture_output=True, cwd=str(REPO),
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    out = r.stdout.decode("utf-8", "replace")
    fails = [ln.strip() for ln in out.splitlines() if ln.startswith("FAIL")]
    return r.returncode, fails


def card_span(text, anchor):
    """(start, end) of the q-card carrying `anchor`, by balancing <div> tags."""
    m = re.search(r'<div class="q-card"[^>]*id="%s"' % anchor, text)
    if not m:
        raise AssertionError("anchor %s not found" % anchor)
    depth = 0
    for t in re.finditer(r"<(/?)div\b[^>]*>", text[m.start():]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return m.start(), m.start() + t.end()
    raise AssertionError("unbalanced card %s" % anchor)


def by_family(fid):
    return next(c for c in CARDS if c["family_id"] == fid)


# ------------------------------------------------------------------ mutations

def m_A(snap):
    """Remove one authorised new q-card entirely."""
    c = by_family("GAP-0376")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    write(c["file"], t[:s] + t[e:])


def m_B(snap):
    """Duplicate a new card's anchor onto a second element."""
    c = by_family("GAP-0159")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    write(c["file"], t[:e] + t[s:e] + t[e:])


def m_C(snap):
    """Break the authorised linkage: move a card off its recorded anchor."""
    c = by_family("GAP-0558")
    t = snap[c["file"]]
    write(c["file"], t.replace('id="%s"' % c["anchor"], 'id="q97"', 1))


def m_D(snap):
    """Add a sixth, unauthorised new card to a Batch-C destination."""
    c = by_family("GAP-0516")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    clone = t[s:e].replace('id="%s"' % c["anchor"], 'id="q96"', 1)
    write(c["file"], t[:e] + clone + t[e:])


def m_E(snap):
    """Blank a new card's answer body."""
    c = by_family("GAP-0562")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    card = t[s:e]
    stripped = re.sub(r'(<div class="q-answer">).*?(<div class="q-footer">)',
                      r"\1\2", card, flags=re.S)
    if stripped == card:
        stripped = re.sub(r'(<div class="q-answer">).*(</div>\s*</div>\s*$)',
                          r"\1\2", card, flags=re.S)
    write(c["file"], t[:s] + stripped + t[e:])


def m_F(snap):
    """Insert an editorial marker into candidate-visible answer text."""
    c = by_family("GAP-0516")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    card = t[s:e].replace("</h4>", "</h4><p>TODO: FIXME before publication.</p>", 1)
    write(c["file"], t[:s] + card + t[e:])


def m_G(snap):
    """Break DOM parentage - a stray close that lifts the card out of #q-feed."""
    c = by_family("GAP-0558")
    t = snap[c["file"]]
    s, _ = card_span(t, c["anchor"])
    write(c["file"], t[:s] + "</div>\n" + t[s:])


def m_H(snap):
    """Downgrade the verified stowaway authority to its superseded predecessor.

    FAL.20(50) (27 March 2026) replaced a chain running back to A.871(20).
    Citing A.871(20) in 2026 is the dated-but-plausible failure this guards.
    """
    c = by_family("GAP-0376")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    card = t[s:e].replace("FAL.20(50)", "A.871(20)")
    write(c["file"], t[:s] + card + t[e:])


def m_I(snap):
    """Replace a candidate-facing question with raw source metadata."""
    c = by_family("GAP-0562")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    card = re.sub(r'(<div class="q-text"[^>]*>).*?(</div>)',
                  r"\1GAP-0562 Nair asked what is a ship broker (ASC-0594)\2",
                  t[s:e], count=1, flags=re.S)
    write(c["file"], t[:s] + card + t[e:])


def m_J(snap):
    """Modify a pre-existing neighbouring card - the regression guard."""
    c = by_family("GAP-0159")
    t = snap[c["file"]]
    s, e = card_span(t, "q1")
    card = t[s:e].replace("</h4>", "</h4><p>Neighbouring card quietly edited.</p>", 1)
    write(c["file"], t[:s] + card + t[e:])


MUTATIONS = [
    ("A", "remove one authorised new q-card", m_A),
    ("B", "duplicate a new card anchor", m_B),
    ("C", "break the authorised card linkage", m_C),
    ("D", "add a sixth unauthorised card", m_D),
    ("E", "blank a new card's answer body", m_E),
    ("F", "insert an editorial marker", m_F),
    ("G", "move a card outside #q-feed", m_G),
    ("H", "downgrade a verified authority reference", m_H),
    ("I", "mutate q-text into source metadata", m_I),
    ("J", "modify a pre-existing destination card", m_J),
]


def main():
    base = snapshot()
    base_digests = {f: digest(t) for f, t in base.items()}

    rc, fails = run_validator()
    if rc != 0:
        print("BASELINE NOT GREEN: validate_batch_c.py exit=%d" % rc)
        for f in fails:
            print("  " + f)
        return 2

    escapes = crashes = not_applied = 0
    for key, name, fn in MUTATIONS:
        try:
            fn(base)
        except Exception as exc:                       # noqa: BLE001
            print("%s  %-42s MUTATION CRASHED: %s" % (key, name, exc))
            crashes += 1
            restore(base)
            continue

        now = {f: digest(read(f)) for f in FILES}
        if now == base_digests:
            print("%s  %-42s NOT APPLIED (no bytes changed)" % (key, name))
            not_applied += 1
            restore(base)
            continue

        rc, fails = run_validator()
        verdict = "CAUGHT" if rc != 0 else "ESCAPE"
        if rc == 0:
            escapes += 1
        print("%s  %-42s exit=%d fails=%d  %s" % (key, name, rc, len(fails), verdict))
        for f in fails[:2]:
            print("      " + f[:150])

        restore(base)
        after = {f: digest(read(f)) for f in FILES}
        if after != base_digests:
            print("      RESTORE FAILED for %s"
                  % [f for f in FILES if after[f] != base_digests[f]])
            crashes += 1

    rc, _ = run_validator()
    print("\nrestored: validator exit=%d; pages byte-identical: %s"
          % (rc, all(digest(read(f)) == base_digests[f] for f in FILES)))
    print("%d mutations, %d escape(s), %d not applied, %d crash(es)"
          % (len(MUTATIONS), escapes, not_applied, crashes))
    return 1 if (escapes or crashes or not_applied or rc) else 0


if __name__ == "__main__":
    sys.exit(main())
