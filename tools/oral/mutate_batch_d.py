"""Mutation harness proving validate_batch_d.py is load-bearing.

Each mutation is applied to the live Batch-D pages or to the manifest, the
validator is run, and everything is restored from a byte snapshot taken
beforehand. A mutation that changes no bytes is reported as NOT APPLIED rather
than silently counted as caught - a stale no-op mutation is the failure mode
this harness exists to avoid, and it is the escape class that had to be closed
in the content-index harness.

The manifest is inside the snapshot, not just the pages. Four of these
mutations attack the manifest rather than the HTML - the Notes source identity,
the disposition of the family the laptop review downgraded, the published
count, and the authorised set - and a harness that snapshotted only the pages
would leave a corrupted manifest on disk after a kill.

Line endings: two of the nine Batch-D destinations (QB2_I, QB4_H) are CRLF in
the working tree while the other seven are LF. Every read and write here uses
newline="" so a restore cannot quietly rewrite a CRLF page to LF - which a
snapshot taken with universal newlines would not detect, because both sides
would already be normalised.

Mutation H is the currentness guard. The free-fall card's whole value is that
it names resolution MSC.218(82), which deleted LSA Code paragraph 4.7.3.3 and
the definition of "required free-fall height" - the wording most training
material still quotes as current. H removes that citation and requires the
validator to notice, the same class of trap Batch C caught with A.871(20)
against FAL.20(50).

Exit 0 when every mutation is applied, caught, and cleanly restored.
"""
import hashlib
import json
import os
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
MANIFEST_PATH = HERE / "batch_d_manifest.json"
MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
CARDS = MANIFEST["cards"]
FILES = sorted({c["file"] for c in CARDS})
MKEY = "<manifest>"


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read(f):
    if f == MKEY:
        return MANIFEST_PATH.read_text(encoding="utf-8", newline="")
    return (QB / f).read_text(encoding="utf-8", newline="")


def write(f, text):
    if f == MKEY:
        MANIFEST_PATH.write_text(text, encoding="utf-8", newline="")
        return
    (QB / f).write_text(text, encoding="utf-8", newline="")


ALL = FILES + [MKEY]


def snapshot():
    return {f: read(f) for f in ALL}


def restore(snap):
    for f, text in snap.items():
        write(f, text)


def run_validator():
    r = subprocess.run([sys.executable, str(HERE / "validate_batch_d.py")],
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


def put_manifest(snap, mutate):
    d = json.loads(snap[MKEY])
    mutate(d)
    write(MKEY, json.dumps(d, ensure_ascii=False, indent=2) + "\n")


# ------------------------------------------------------------------ mutations

def m_A(snap):
    """Remove one promoted card entirely."""
    c = by_family("GAP-0231")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    write(c["file"], t[:s] + t[e:])


def m_B(snap):
    """Break the Notes source identity the promotion was built from."""
    def f(d):
        for c in d["cards"]:
            if c["family_id"] == "GAP-0355":
                c["notes_source"] = "meoclass1/oralnotes/simon-notes-p2.html#n999"
    put_manifest(snap, f)


def m_C(snap):
    """Duplicate a promoted card's anchor onto a second element."""
    c = by_family("GAP-0621")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    write(c["file"], t[:e] + t[s:e] + t[e:])


def m_D(snap):
    """Label the downgraded ALREADY_COVERED family as a Batch-D new card.

    GAP-0065 is adjudicated NOTES_TO_QB_PROMOTION but the laptop review
    downgraded it. Re-admitting it is the exact mis-selection this batch had
    to reason its way past.
    """
    def f(d):
        d["cards"].append({
            "family_id": "GAP-0065",
            "production_action_id": "PROMNEW-010",
            "file": "QB9_A.html", "anchor": "q10",
            "topic": "re-admitted downgraded family",
            "notes_source": "meoclass1/oralnotes/miw-notes-mgmt-p8.html#topic-36",
            "authority_tokens": [],
        })
    put_manifest(snap, f)


def m_E(snap):
    """Blank a promoted card's answer body."""
    c = by_family("GAP-0534")
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
    """Inject production metadata into candidate-visible answer text."""
    c = by_family("GAP-0342")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    card = t[s:e].replace(
        "</h4>", "</h4><p>GAP-0342 promoted from notes; TODO verify.</p>", 1)
    write(c["file"], t[:s] + card + t[e:])


def m_G(snap):
    """Break DOM parentage - a stray close that lifts the card out of #q-feed."""
    c = by_family("GAP-0334")
    t = snap[c["file"]]
    s, _ = card_span(t, c["anchor"])
    write(c["file"], t[:s] + "</div>\n" + t[s:])


def m_H(snap):
    """Remove the currentness citation from the free-fall card.

    MSC.218(82) is what makes the card's height section correct in 2026: it
    deleted LSA Code 4.7.3.3 and the "required free-fall height" definition.
    Without it the card reads as the pre-2008 position.
    """
    c = by_family("GAP-0218")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    card = t[s:e].replace("MSC.218(82)", "the 1996 Code")
    write(c["file"], t[:s] + card + t[e:])


def m_I(snap):
    """Modify a pre-existing neighbouring card - the regression guard."""
    c = by_family("GAP-0180")
    t = snap[c["file"]]
    s, e = card_span(t, "q1")
    card = t[s:e].replace("</h4>", "</h4><p>Neighbouring card quietly edited.</p>", 1)
    write(c["file"], t[:s] + card + t[e:])


def m_J(snap):
    """Make actual_new_card_count disagree with the live corpus delta."""
    def f(d):
        d["actual_new_card_count"] = 7
    put_manifest(snap, f)


def m_K(snap):
    """Add an unauthorised tenth promotion to a Batch-D destination page."""
    c = by_family("GAP-0151")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    clone = t[s:e].replace('id="%s"' % c["anchor"], 'id="q94"', 1)
    write(c["file"], t[:e] + clone + t[e:])


def m_L(snap):
    """Leak an internal Oral Notes source path into candidate-visible text."""
    c = by_family("GAP-0621")
    t = snap[c["file"]]
    s, e = card_span(t, c["anchor"])
    card = t[s:e].replace(
        "</h4>", "</h4><p>Adapted from miw-notes-mgmt-p19.html.</p>", 1)
    write(c["file"], t[:s] + card + t[e:])


MUTATIONS = [
    ("A", "remove one promoted card", m_A),
    ("B", "break the Notes source identity", m_B),
    ("C", "duplicate a promoted card anchor", m_C),
    ("D", "re-admit the downgraded family as NEW", m_D),
    ("E", "blank a promoted card's answer body", m_E),
    ("F", "inject production metadata", m_F),
    ("G", "move a card outside #q-feed", m_G),
    ("H", "remove the currentness authority reference", m_H),
    ("I", "modify a pre-existing destination card", m_I),
    ("J", "make the published count disagree", m_J),
    ("K", "add an unauthorised tenth promotion", m_K),
    ("L", "leak a Notes source path to candidates", m_L),
]


def main():
    base = snapshot()
    base_digests = {f: digest(t) for f, t in base.items()}

    rc, fails = run_validator()
    if rc != 0:
        print("BASELINE NOT GREEN: validate_batch_d.py exit=%d" % rc)
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

        now = {f: digest(read(f)) for f in ALL}
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
        after = {f: digest(read(f)) for f in ALL}
        if after != base_digests:
            print("      RESTORE FAILED for %s"
                  % [f for f in ALL if after[f] != base_digests[f]])
            crashes += 1

    rc, _ = run_validator()
    print("\nrestored: validator exit=%d; files byte-identical: %s"
          % (rc, all(digest(read(f)) == base_digests[f] for f in ALL)))
    print("%d mutations, %d escape(s), %d not applied, %d crash(es)"
          % (len(MUTATIONS), escapes, not_applied, crashes))
    return 1 if (escapes or crashes or not_applied or rc) else 0


if __name__ == "__main__":
    sys.exit(main())
