#!/usr/bin/env python3
"""CORR-ITC51-20260908 - the ITC-Hulls automatic-termination clause citation.

The mechanism taught across these sites is Institute Time Clauses - Hulls
(1/11/95) Clause 5.1: the insurance terminates AUTOMATICALLY on change of the
Classification Society, or change, suspension, discontinuance, withdrawal or
expiry of Class, deferred until arrival at the next port if the Vessel is at
sea, and subject to the Clause 6 proviso. It was cited as Clause 4.2, which is
a different mechanism - the Underwriters' discharge from liability for breach
of the Clause 4.1 duty to maintain class.

Only the citation moves. No teaching is rewritten.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OLD = "cl. 4.2"
NEW = "cl. 5.1"

#: path -> exact number of ITC citations that must be present and corrected.
#: An assertion, not a guess: the census established every one of these counts,
#: and a file that no longer matches its count stops the applier.
EXPECTED = {
    "meoclass1/QB1_C.html": 1,
    "meoclass1/QB1_F.html": 2,
    "meoclass1/QB1_G.html": 2,
    "meoclass1/QB4_A.html": 4,
    "meoclass1/QB4_C.html": 3,
    "meoclass1/QB4_A_CheatSheet.html": 1,
    "meoclass1/QB1_K_CheatSheet.html": 1,
    "meoclass1/known_traps.md": 2,
    "tools/oral/qb_content_index_governed.json": 1,
}

#: cards that carry a q-version changelog and get a new entry.
STAMP = {
    "meoclass1/QB1_C.html": ("q6", "QB1_C", "Q6"),
    "meoclass1/QB1_F.html": ("q7", "QB1_F", "Q7"),
    "meoclass1/QB1_G.html": ("q36", "QB1_G", "Q36"),
    "meoclass1/QB4_A.html": ("q9", "QB4", "Q9"),
    "meoclass1/QB4_C.html": ("q5", "QB4_C", "Q5"),
}

NOTE = (
    "corrected 8 Sep 2026 (ITC-Hulls clause correction): the automatic-termination "
    "of hull cover was cited as Institute Time Clauses &ndash; Hulls (1/11/95) "
    "Clause 4.2. Clause 4.2 is a different mechanism &mdash; the Underwriters&rsquo; "
    "discharge from liability for breach of the Clause 4.1 duty to maintain class. "
    "Automatic termination of the insurance on change, suspension, discontinuance, "
    "withdrawal or expiry of Class, deferred until arrival at the next port if the "
    "Vessel is at sea and subject to the Clause 6 proviso, is <strong>Clause 5.1"
    "</strong>. The citation is corrected; the mechanism taught was already correct "
    "and is unchanged."
)

sys.path.insert(0, os.path.join(REPO, "tools", "oral"))
from validate_batch_b import CARD_OPEN, _balanced_end  # noqa: E402

VER = re.compile(r'(<span class="q-version">)(.*?)(</span>)', re.S)


def bump(block, prefix, qlabel):
    """Prepend a new changelog entry to the card's q-version span."""
    m = VER.search(block)
    if not m:
        raise AssertionError("no q-version span in %s" % qlabel)
    body = m.group(2)
    vers = [float(x) for x in re.findall(r'v(\d+\.\d+)', body)]
    if not vers:
        raise AssertionError("no version token in %s" % qlabel)
    nxt = "v%.1f" % (max(vers) + 0.1)
    head = "%s &middot; %s &middot; %s &mdash; %s" % (prefix, qlabel, nxt, NOTE)
    # keep the whole existing changelog, minus its now-superseded lead label
    rest = re.sub(r'^\s*' + re.escape(prefix) + r'\s*&middot;\s*'
                  + re.escape(qlabel) + r'\s*&middot;\s*', '', body).strip()
    return block[:m.start()] + m.group(1) + head + " &middot; " + rest + m.group(3) + block[m.end():]


def main():
    for rel in EXPECTED:
        if "ITC-Hulls clause correction" in open(
                os.path.join(REPO, rel), encoding="utf-8").read():
            raise SystemExit("already applied: %s carries the correction stamp" % rel)
    changed = []
    for rel, n in EXPECTED.items():
        path = os.path.join(REPO, rel)
        raw = open(path, encoding="utf-8", newline="").read()
        found = raw.count(OLD)
        assert found == n, "%s: expected %d ITC citations, found %d" % (rel, n, found)
        out = raw.replace(OLD, NEW)
        assert out.count(NEW) - raw.count(NEW) == n, "%s: replacement count wrong" % rel
        assert OLD not in out, "%s: a citation survived" % rel

        if rel in STAMP:
            anchor, prefix, qlabel = STAMP[rel]
            probe = out.replace("\r\n", "\n")
            hit = None
            for m in CARD_OPEN.finditer(probe):
                if re.search(r'\bid="%s"' % re.escape(anchor), m.group(0)):
                    hit = (m.start(), _balanced_end(probe, m.start()))
                    break
            assert hit, "%s: card %s not found" % (rel, anchor)
            s, e = hit
            stamped = bump(probe[s:e], prefix, qlabel)
            assert stamped != probe[s:e], "%s: version stamp was a no-op" % rel
            probe = probe[:s] + stamped + probe[e:]
            out = probe if "\r\n" not in raw else probe.replace("\n", "\r\n")

        open(path, "w", encoding="utf-8", newline="").write(out)
        changed.append((rel, n))

    for rel, n in changed:
        print("  corrected %2d citation(s)  %s" % (n, rel))
    print("files changed: %d" % len(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
