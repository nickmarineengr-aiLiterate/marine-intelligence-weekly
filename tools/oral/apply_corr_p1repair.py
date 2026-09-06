"""Apply CORR-P1REPAIR-20260906 - the Pass-1 repair layer.

This record does not replace the Pass-1 records. Those stay on main as the
historical evidence of what the first attempt did and claimed; this one records
what an independent review found wrong with it and what was done about that.
Rewriting the originals to look correct would destroy the only account of how
the escape happened.

TWO CONFIRMED P0 ESCAPES

P0-A  QB2_H#q2 still taught "4.0 Bar: Minimum operational pressure required at
      the furthest deck hydrant" in its Key Numbers layer - the highest-salience
      block on the card - four lines above its own new version stamp saying that
      figure "is not a SOLAS figure". CORR-T5-HYDRANT rewrote the card's
      extra-block and left this one, and its gate reported PASS because the
      negative check was CASE-SENSITIVE: it looked for "4.0 bar" and the residue
      reads "4.0 Bar".

P0-B  Every Pass-1 census and gate enumerated `meoclass1/*.html` - top level
      only, 128 files. The corpus is 224. Ninety-six files were outside every
      claim of "corpus-wide", and the whole `oralnotes` study series sits in that
      gap teaching BMP5 as current, including a timeline row dating BMP5 to 2024.

WHAT IS AND IS NOT SWEPT IN THE NEWLY-VISIBLE SCOPE

A recursive enumeration is not a licence to sweep 224 files under one policy.
`pastpapers` is sitting-anchored: a present-day term cannot be written into a
past paper, and the CORR-CICTERM propagation record already settled that. It
returns ZERO hits for this family in any case. `oralnotes` is current study
material by its own titles, so currentness rules apply there exactly as they do
to a card. Navigation echoes of a topic whose SUBJECT is BMP5, and an index row
pointing at a printed book's page, are the examiner-wording case and are kept.

NO DATE IS INVENTED TO REPLACE A FALSE ONE. The timeline row said "2024 BMP5
supersedes BMP4". That is false. The repository holds no registry row for BMP5's
own publication date - "BMP5 (2018)" is asserted at six card sites on corpus
convention alone - so this record does not assert 2018 either. It replaces the
row with the fact that IS held and digest-pinned: SRC-BMPMS-2025, 31 March 2025,
BMP Maritime Security replacing BMP5, BMP West Africa and the Global Counter
Piracy Guidance. The unsourced 2018 convention is reported, not propagated.
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

#: The governing sentence, written once so the sites cannot drift apart.
SOLAS_LIMBS = ("SOLAS II-2/10.2.1.6 minimum pressure at the hydrants with the "
               "two required pumps delivering simultaneously &mdash; for cargo "
               "ships <strong>0.27 N/mm&sup2;</strong> at 6,000 GT and upwards "
               "and <strong>0.25 N/mm&sup2;</strong> below")

BMP_MS = ("<strong>BMP Maritime Security</strong> (BMP MS), 1st Edition 2025 as "
          "updated in 2026, published by BIMCO, ICS, IMCA, INTERCARGO, "
          "INTERTANKO and OCIMF")

CURRENTNESS = (
    '<div class="notes-callout" style="border-left:4px solid #b45309;'
    'background:#fffbeb;padding:10px 14px;margin:12px 0;">'
    '<strong>Currentness note (6 Sep 2026):</strong> <strong>BMP5 has been '
    'superseded.</strong> It was replaced in 2025 by ' + BMP_MS + ', which also '
    'replaced BMP West Africa and the Global Counter Piracy Guidance and is '
    'global rather than region-scoped. The hardening technique below carries '
    'forward and is still examinable, but do not offer BMP5 as the current '
    'publication. See QB4_H Q13 for the current publication and its status.'
    '</div>')

EDITS = [
    # ================= P0-A =================================================
    dict(id="P0-A", file="QB2_H.html", anchor="q2", count=1,
         old='<li>4.0 Bar: Minimum operational pressure required at the '
             'furthest deck hydrant on a large container vessel during '
             'multi-line operations.</li>',
         new='<li><strong>0.27 / 0.25 N/mm&sup2;:</strong> ' + SOLAS_LIMBS +
             '. A higher pressure carried at the furthest hydrant for '
             'multi-line or monitor operations is an operational design '
             'target, not a SOLAS minimum.</li>',
         why="the false 4.0 Bar regulatory minimum, in the card's Key Numbers "
             "layer, which CORR-T5-HYDRANT left behind and its case-sensitive "
             "gate could not see"),

    # ================= F-3 : the same single-limb defect on a cheat sheet ====
    dict(id="F-3a", file="QB2_B_CheatSheet.html", anchor="-", count=1,
         old='<li>Min hydrant pressure maintained: <strong>0.27 N/mm²'
             '</strong></li>',
         new='<li>Min hydrant pressure, two pumps running: <strong>0.27 '
             'N/mm²</strong> at 6,000 GT and upwards, <strong>0.25 '
             'N/mm²</strong> below (SOLAS II-2/10.2.1.6, cargo ships)</li>',
         why="single-limb 0.27 stated as the cargo-ship minimum, which the "
             "parent card now calls wrong below 6,000 GT"),
    dict(id="F-3b", file="QB2_B_CheatSheet.html", anchor="-", count=1,
         old='<li>Maintain <strong>0.27 N/mm²</strong> at all hydrants '
             'during firefighting</li>',
         new='<li>Minimum at the hydrants with both required pumps running: '
             '<strong>0.27 N/mm²</strong> at 6,000 GT and upwards, '
             '<strong>0.25 N/mm²</strong> below (SOLAS II-2/10.2.1.6, '
             'cargo ships)</li>',
         why="worse than the card defect it derives from: it dropped the pump "
             "condition too and stated the figure as a continuous duty"),

    # The SAME card CORR-T5-HYDRANT corrected as E-3 - its Key Numbers bullet
    # was fixed and its deep-dive "Numbers to Memorise" layer was not. Found by
    # the new single-limb check, not by any hand-built list: a reach failure
    # inside a card the previous pass believed it had closed.
    dict(id="F-3c", file="QB2_B.html", anchor="q18", count=1,
         old='<p>Minimum hydrant pressure limits (0.27 N/mm²); FSS Code '
             'hose flow metrics.</p>',
         new='<p>Minimum hydrant pressure, both required pumps delivering '
             '(SOLAS II-2/10.2.1.6, cargo ships): <strong>0.27 '
             'N/mm&sup2;</strong> at 6,000 GT and upwards, <strong>0.25 '
             'N/mm&sup2;</strong> below. FSS Code hose flow metrics.</p>',
         why="the card's deep-dive numbers layer still carried single-limb "
             "0.27, on the very card whose Key Numbers bullet Pass 1 corrected"),

    # ================= P0-B : oralnotes, mgmt part 10 =======================
    dict(id="ON-1", file="oralnotes/miw-notes-mgmt-p10.html", anchor="topic-46",
         count=1,
         old='<span class="t-year">2024</span>  BMP5 supersedes BMP4 — '
             'extends HRA coverage (Red Sea, Gulf of Aden, Indian Ocean, '
             'Arabian Sea)',
         new='<span class="t-year">2025</span>  BMP Maritime Security replaces '
             'BMP5, BMP West Africa and the Global Counter Piracy Guidance '
             '— one global guide, not region-scoped',
         why="a FALSE date: the row dated BMP5 to 2024. No held source gives "
             "BMP5's own publication year, so none is asserted; the row now "
             "carries the supersession fact that IS held (SRC-BMPMS-2025)"),
    dict(id="ON-2", file="oralnotes/miw-notes-mgmt-p10.html", anchor="topic-46",
         count=1,
         old='<div class="reg-item"><span class="reg-code">BMP5</span>'
             '<span class="reg-desc">Industry-issued (ICS-led coalition) '
             'ship-hardening & operational guidance for HRA transits '
             '— supersedes BMP4.</span></div>',
         new='<div class="reg-item"><span class="reg-code">BMP Maritime '
             'Security</span><span class="reg-desc">Industry ship-hardening '
             'and operational guidance for HRA transits; 1st Edition 2025 as '
             'updated in 2026, published by BIMCO, ICS, IMCA, INTERCARGO, '
             'INTERTANKO and OCIMF. Replaced BMP5, BMP West Africa and the '
             'Global Counter Piracy Guidance.</span></div>',
         why="a reg-code slot naming a superseded publication as current - the "
             "identical shape corrected as A-6 and A-7 on cards, in a file no "
             "Pass-1 census could see"),
    dict(id="ON-3", file="oralnotes/miw-notes-mgmt-p10.html", anchor="topic-46",
         count=1,
         old='Operational counter-piracy guidance for High Risk Areas is '
             'codified in <strong>Best Management Practices (BMP5)</strong>.',
         new='Operational counter-piracy and maritime-security guidance for '
             'High Risk Areas is now codified in ' + BMP_MS +
             ', which replaced BMP5.',
         why="present-tense teaching that BMP5 is the live guidance"),
    dict(id="ON-4", file="oralnotes/miw-notes-mgmt-p10.html", anchor="topic-46",
         count=1,
         old="BMP5's issuing body (ICS-led industry coalition) and its "
             "supersession of BMP4 (Somali-piracy focus) match the published "
             "BMP5 document",
         new="BMP5's issuing body and its supersession of BMP4 match the "
             "published BMP5 document, but BMP5 is no longer current &mdash; "
             "see the currentness note above; the verification below did not "
             "test currency",
         why="a verification note vouching for teaching that is out of date - "
             "the N-1 shape (a confidence claim standing behind a superseded "
             "authority), found here by the recursive census"),

    # ================= P0-B : oralnotes, simon notes =======================
    dict(id="ON-5", file="oralnotes/simon-notes-p1.html", anchor="-", count=1,
         old='Not mandatory — but highly recommended by BMP5.',
         new='Not mandatory — but highly recommended by BMP Maritime '
             'Security, the current guide that replaced BMP5.',
         why="current teaching attributing a live recommendation to a "
             "superseded publication"),
    dict(id="ON-6", file="oralnotes/simon-notes-p1.html", anchor="-", count=1,
         old='Both are referenced in <strong>BMP5 (Best Management Practices 5)'
             '</strong>',
         new='Both are referenced in <strong>BMP Maritime Security</strong>, '
             'the current guide that replaced BMP5',
         why="current teaching naming the superseded publication"),

    # Found by the RECURSIVE gate, not by the hand-built site list - the
    # reg-code slot on the same page whose prose sites were corrected as ON-5
    # and ON-6. Exactly the miss the scope defect exists to prevent.
    dict(id="ON-10", file="oralnotes/simon-notes-p1.html", anchor="-", count=1,
         old='<div class="reg-item"><span class="reg-code">BMP5</span>'
             '<span class="reg-desc"><em>"Best Management Practices to Deter '
             'Piracy and Enhance Maritime Security (BMP5)"</em> — industry '
             'guidance (Witherby/BIMCO/ICS et al.), not an IMO instrument but '
             'referenced in IMO circulars</span></div>',
         new='<div class="reg-item"><span class="reg-code">BMP Maritime '
             'Security</span><span class="reg-desc">Industry guidance (BIMCO, '
             'ICS, IMCA, INTERCARGO, INTERTANKO and OCIMF), 1st Edition 2025 as '
             'updated in 2026; not an IMO instrument. It replaced <em>"Best '
             'Management Practices to Deter Piracy and Enhance Maritime '
             'Security (BMP5)"</em>, BMP West Africa and the Global Counter '
             'Piracy Guidance.</span></div>',
         why="a reg-code slot still offering BMP5 as a current reference, on a "
             "page whose prose sites were corrected - caught by the recursive "
             "gate after the hand-built list missed it"),

    # ================= P0-B : oralnotes, mgmt part 1 =======================
    dict(id="ON-8", file="oralnotes/miw-notes-mgmt-p1.html", anchor="-",
         count=1,
         old='<td>ISGOTT, BMP5, OCIMF guidelines</td>',
         new='<td>ISGOTT, BMP Maritime Security (replaced BMP5), OCIMF '
             'guidelines</td>',
         why="a non-mandatory-guidance list naming the superseded publication"),
    dict(id="ON-9", file="oralnotes/miw-notes-mgmt-p1.html", anchor="-",
         count=1,
         old='Also know that ISGOTT and BMP5 are non-mandatory industry '
             'guidance',
         new='Also know that ISGOTT and BMP Maritime Security (which replaced '
             'BMP5) are non-mandatory industry guidance',
         why="current teaching naming the superseded publication"),

    # ================= F-10 : orphaned markdown bullets =====================
    dict(id="F-10", file="QB9_E.html", anchor="q7", count=1,
         old='Operationally, you must ensure:\n\n'
             '* All auxiliary engines are online or available for immediate '
             'parallel operation to prevent an electrical blackout.\n'
             '* The emergency steering gear and quick-closing valve trip '
             'mechanisms are fully tested and functional.\n'
             '* Fuel oil systems are optimized, with clean filters and settled '
             'tanks to prevent fuel starvation during sudden evasive '
             'maneuvering.\n\n'
             'If a breakdown occurs',
         new='Operationally, you must ensure:<ul>'
             '<li>All auxiliary engines are online or available for immediate '
             'parallel operation to prevent an electrical blackout.</li>'
             '<li>The emergency steering gear and quick-closing valve trip '
             'mechanisms are fully tested and functional.</li>'
             '<li>Fuel oil systems are optimized, with clean filters and '
             'settled tanks to prevent fuel starvation during sudden evasive '
             'maneuvering.</li></ul>'
             'If a breakdown occurs',
         why="three raw markdown bullets rendered literally to the candidate. "
             "A SECOND orphan form: Pass-1's scan was `\\* <strong>` and these "
             "bullets do not open with a <strong>, so they were neither "
             "repaired nor declared"),
]

#: F-9 - the currentness note is INSERTED, so it is not a replacement edit.
CURRENTNESS_ANCHOR = ('<div class="section-head">⚓ Why It Matters '
                      '(CE Perspective)</div>')

#: F-9 - version stamp. The two same-day clauses are merged into one; nothing
#: is erased, because both clauses describe edits that really happened.
V15_OLD = ('QB4_H · Q2 · v1.5 — corrected 31 Aug 2026:')
V16_NEW = ('QB4_H · Q2 · v1.6 — corrected 31 Aug 2026:')
DUP_OLD = ('; candidate name de-identified; corrected 6 Sep 2026: the '
           'source-confidence footer still offered')
DUP_NEW = ('; candidate name de-identified; and the '
           'source-confidence footer still offered')


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    problems = []
    for e in EDITS:
        path = QB_ROOT / e["file"]
        text = read_text(path)
        n = text.count(e["old"])
        if n != e["count"]:
            if text.count(e["new"]) > 0:
                print("  %-6s %-38s ALREADY APPLIED" % (e["id"], e["file"]))
                continue
            problems.append("%s: expected %d occurrence(s) in %s, found %d"
                            % (e["id"], e["count"], e["file"], n))
            continue
        print("  %-6s %-38s %-6s %s" % (e["id"], e["file"], e["anchor"],
                                        e["why"][:76]))
        if args.apply:
            path.write_bytes(text.replace(e["old"], e["new"])
                             .encode("utf-8").replace(b"\r\n", b"\n"))

    # ---- currentness note on the oralnotes topic ------------------------
    p10 = QB_ROOT / "oralnotes/miw-notes-mgmt-p10.html"
    t = read_text(p10)
    if "Currentness note (6 Sep 2026)" in t:
        print("  %-6s %-38s ALREADY APPLIED" % ("ON-7", p10.name))
    elif t.count(CURRENTNESS_ANCHOR) < 1:
        problems.append("ON-7: currentness anchor not found in %s" % p10.name)
    else:
        print("  %-6s %-38s %-6s %s" % ("ON-7", "oralnotes/…-p10.html",
                                        "topic-46",
                                        "currentness note added to the topic"))
        if args.apply:
            i = t.find(CURRENTNESS_ANCHOR)
            t = t[:i] + CURRENTNESS + t[i:]
            p10.write_bytes(t.encode("utf-8").replace(b"\r\n", b"\n"))

    # ---- F-9 version stamp ----------------------------------------------
    qb4h = QB_ROOT / "QB4_H.html"
    t = read_text(qb4h)
    if "QB4_H · Q2 · v1.6" in t:
        print("  %-6s %-38s ALREADY APPLIED" % ("F-9", "QB4_H.html"))
    elif t.count(V15_OLD) != 1 or t.count(DUP_OLD) != 1:
        problems.append("F-9: version stamp anchors not found uniquely")
    else:
        print("  %-6s %-38s %-6s %s" % ("F-9", "QB4_H.html", "q2",
                                        "v1.5 -> v1.6; two same-day clauses "
                                        "merged, neither erased"))
        if args.apply:
            t = t.replace(V15_OLD, V16_NEW).replace(DUP_OLD, DUP_NEW)
            qb4h.write_bytes(t.encode("utf-8").replace(b"\r\n", b"\n"))

    if problems:
        print("\nREFUSED - nothing written for these:")
        for p in problems:
            print("  " + p)
        return 1
    print("\n%s: %d replacements + currentness note + version stamp"
          % ("APPLIED" if args.apply else "DRY RUN", len(EDITS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
