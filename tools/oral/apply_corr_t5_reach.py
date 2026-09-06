"""Apply CORR-T5-REACH-20260906: seven correction-reach sites.

The family. A correction lands on a card's teaching body and misses the
surfaces that carry the same proposition - the source-confidence footer, the
paired cheat sheet, a sibling card's reg-box. Tranche 5 named four of these
(N-1, N-2, N-4); the corpus-wide census found three more that no BMP sweep had
ever reached, because every earlier sweep derived its site list from a finding's
card list instead of from the corpus.

No new fact is advanced. Every edit carries an already-adjudicated,
externally-verified proposition to a surface that was left behind:

  BMP5 was replaced in 2025 by BMP Maritime Security, 1st Edition (2025) as
  updated during 2026, published by BIMCO, ICS, IMCA, INTERCARGO, INTERTANKO
  and OCIMF.  Established by CORR-GPT-T2C-CURRENCY-20260905; propagated once
  already by CORR-BMP-EDITION-PROP-20260905.

What is deliberately NOT touched. A `q-text`, a `cs-qtitle`, a TOC entry or a
`sub-desc` that echoes one is the EXAMINER'S OWN WORDING and stays as it is -
QB4_H#q11 is retained on purpose as the predecessor record because examiners
still ask for BMP5 by name. A currentness note that quotes "BMP5" in order to
deny it is the fix, not the defect. Rewriting either would be a sweep
destroying the evidence it exists to preserve.

Idempotent, and asserts an exact occurrence count for every edit before writing
anything: a silent zero-match edit is how two earlier mutations shipped having
exercised nothing at all.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
QB_ROOT = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import read_text  # noqa: E402

BMP_MS = "BMP Maritime Security"

EDITS = [
    # ---- N-1 --------------------------------------------------------------
    # QB4_H#q2 removed the unverifiable BMP5 section-number carry-over from its
    # body on 31 Aug and quoted the held current publication on 6 Sep - and its
    # source-confidence footer still offered "BMP5 Section 5" as the authority
    # the card had been VERIFIED against. The footer contradicted the card.
    dict(
        id="N-1",
        file="QB4_H.html",
        anchor="q2",
        count=1,
        old='JMIC advisory updates, BMP5 Section 5 (safe muster point vs. citadel, '
            'mscio.eu), and current open-source reporting',
        new='JMIC advisory updates, the held <strong>BMP Maritime Security, 1st '
            'Edition (2025) as updated June 2026</strong> (safe muster point vs. '
            'citadel), and current open-source reporting',
        proposition='the footer no longer cites a superseded publication as the '
                    'authority this card was verified against',
    ),
    # ---- N-2 --------------------------------------------------------------
    # QB9_A#q9 removed an unusable MSC.1/Circ.1606 row on 6 Sep. Its cheat sheet
    # kept the circular as TWO identical Numbers & Codes pills carrying no
    # proposition at all. Nothing is guessed in its place; the row would then be
    # an empty promise, so the row goes with the pills.
    dict(
        id="N-2",
        file="QB9_A_CheatSheet.html",
        anchor="-",
        count=1,
        old='\n          <div class="cs-row"><div class="cs-label">🔢 Numbers &amp; '
            'Codes</div><div class="nums-row"><code class="num-pill">'
            'MSC.1/Circ.1606</code><code class="num-pill">MSC.1/Circ.1606</code>'
            '</div></div>',
        new='',
        proposition='the cheat sheet no longer offers a circular the parent card '
                    'removed as unusable',
    ),
    # ---- N-4 (a) ----------------------------------------------------------
    dict(
        id="N-4a",
        file="QB5_B_CheatSheet.html",
        anchor="-",
        count=1,
        old='clear timeline to safe passage. BMP5 procedures. ISPS Security Level '
            'elevation.',
        new='clear timeline to safe passage. BMP Maritime Security procedures '
            '(1st Ed. 2025 as updated 2026 &mdash; replaced BMP5). ISPS Security '
            'Level elevation.',
        proposition='positive current teaching on the revision surface names the '
                    'current publication',
    ),
    # ---- N-4 (b) ----------------------------------------------------------
    # The examiner-cue column is QUOTED wording and is kept: QB4_H#q11 exists
    # precisely because examiners still ask for BMP5 by name. What was missing
    # is the parent card's own predecessor banner, so the ANSWER cell is
    # qualified and the cue is not touched.
    dict(
        id="N-4b",
        file="QB4_H_cheatsheet.html",
        anchor="-",
        count=1,
        old='<tr><td>11</td><td>"BMP5 details"</td><td>3 pillars, 3 phases, '
            'citadel (boarding)',
        new='<tr><td>11</td><td>"BMP5 details"</td><td><strong>Predecessor '
            'publication &mdash; superseded by BMP Maritime Security; see Q13.'
            '</strong> 3 pillars, 3 phases, citadel (boarding)',
        proposition='the revision surface carries the parent card\'s predecessor '
                    'status, without rewriting the examiner\'s own cue',
    ),
    # ---- A5 : never reached by any BMP sweep -------------------------------
    dict(
        id="A-5",
        file="QB1_F.html",
        anchor="q10",
        count=1,
        old='<span class="reg-code">Best Management Practices (BMP5)</span>'
            '<span class="reg-desc">Industry-standard guidelines for ship '
            'protection and hardening in high-risk areas.</span>',
        new='<span class="reg-code">BMP Maritime Security</span>'
            '<span class="reg-desc">Industry guidance for ship protection and '
            'hardening, 1st Edition (2025) as updated in 2026; global rather '
            'than region-scoped. Replaced BMP5 (2018), BMP West Africa and the '
            'Global Counter Piracy Guidance &mdash; see QB4_H Q13.</span>',
        proposition='the reg-box names the current publication',
    ),
    # ---- A6 : same FILE as N-1, a sibling card the sweep did not open ------
    dict(
        id="A-6",
        file="QB4_H.html",
        anchor="q6",
        count=1,
        old='<span class="reg-code">BMP5</span><span class="reg-desc">Guidance on '
            'electronic signature management during HRA transits</span>',
        new='<span class="reg-code">BMP Maritime Security</span>'
            '<span class="reg-desc">Guidance on electronic signature management '
            'during HRA transits; 1st Edition (2025) as updated in 2026, which '
            'replaced BMP5 &mdash; see Q13</span>',
        proposition='the reg-box names the current publication',
    ),
    # ---- A7 : QB5_B card layer, the sibling of the N-4a cheat sheet --------
    dict(
        id="A-7a",
        file="QB5_B.html",
        anchor="q14",
        count=1,
        old='<li><strong>BMP5 engineering measures:</strong>',
        new='<li><strong>BMP Maritime Security engineering measures:</strong>',
        proposition='positive current teaching in the answer body names the '
                    'current publication',
    ),
    dict(
        id="A-7b",
        file="QB5_B.html",
        anchor="q14",
        count=1,
        old='<span class="reg-code">BMP5 / Industry Best Management Practices'
            '</span><span class="reg-desc">War zone and piracy risk management',
        new='<span class="reg-code">BMP Maritime Security</span>'
            '<span class="reg-desc">1st Edition (2025) as updated in 2026, which '
            'replaced BMP5. War zone and piracy risk management',
        proposition='the reg-box names the current publication',
    ),
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    by_file = {}
    for e in EDITS:
        by_file.setdefault(e["file"], []).append(e)

    problems = []
    for fname, edits in sorted(by_file.items()):
        path = QB_ROOT / fname
        text = read_text(path)
        for e in edits:
            n = text.count(e["old"])
            # A DELETION has no new string to look for, so "already applied"
            # for it means the anchor is simply gone. Testing only for the
            # replacement text makes the check structurally blind to deletions
            # and reports a clean re-run as a refusal.
            done = (text.count(e["new"]) > 0) if e["new"] else (n == 0)
            if n != e["count"]:
                if done:
                    print("  %-6s %-24s ALREADY APPLIED" % (e["id"], fname))
                    continue
                problems.append("%s: expected %d occurrence(s) of its anchor in "
                                "%s, found %d" % (e["id"], e["count"], fname, n))
                continue
            text = text.replace(e["old"], e["new"])
            print("  %-6s %-24s %-5s %s" % (e["id"], fname, e["anchor"],
                                            e["proposition"]))
        if args.apply:
            path.write_bytes(text.encode("utf-8").replace(b"\r\n", b"\n"))

    if problems:
        print("\nREFUSED - no file written for these:")
        for p in problems:
            print("  " + p)
        return 1
    print("\n%s: %d edits across %d surfaces"
          % ("APPLIED" if args.apply else "DRY RUN", len(EDITS), len(by_file)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
