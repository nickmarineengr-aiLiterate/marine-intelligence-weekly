#!/usr/bin/env python3
"""Mutation proof for the Tranche 4A gates.

A gate that never fails proves nothing.  For each mutation below we
reintroduce the exact defect the correction removed, run
validate_tranche4a.py, and require that the NAMED check goes FAIL.  Every
file is then restored and its SHA-256 compared against the pre-mutation
digest, so the suite cannot leave the tree altered.

An "escape" is a mutation the gates did not catch.  Escapes must be zero.

Serial execution only: one mutation live at a time.
"""
import hashlib
import io
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
#: Reaches the shared UTF-8 stdio contract -- and this file is the one that
#: actually needs it. It is a mutation harness: it writes a product page,
#: runs the validator, prints the result and then restores. A
#: UnicodeEncodeError on that print lands BETWEEN the mutation and the
#: restore and leaves the mutation on disk, which is the incident the
#: contract exists to prevent.
from oral_bytes import enable_utf8_stdio  # noqa: E402,F401

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QB = os.path.join(ROOT, "meoclass1")
VALIDATOR = os.path.join(ROOT, "tools", "oral", "validate_tranche4a.py")

# (label, file, expected-failing-check-id, find, replace[, count])
# count defaults to 1; use 0 to replace every occurrence (retention probes).
MUTATIONS = [
    # ---- A. Grain -------------------------------------------------------
    ("grain: DoA reattributed to A 7", "QB2_A.html", "G-01",
     "International Grain Code, A 3 / A 6", "International Grain Code, A 7"),
    ("grain: 1994 limb dropped from body", "QB2_A.html", "G-06",
     ", <em>in the case of ships constructed on or after 1 January 1994</em>, the angle at which the deck edge is immersed, whichever is the lesser &mdash; A 7.1.1",
     " deck edge is immersed if less"),
    ("grain: 1994 limb dropped from Numbers", "QB2_A.html", "G-07",
     " &mdash; or deck-edge immersion if less, but that limb applies only to <strong>ships constructed on or after 1 January 1994</strong> (A 7.1.1) &mdash;",
     " maximum heel, or deck-edge immersion if less,"),
    ("grain: residual-area criterion deleted (all sites)", "QB2_A.html", "G-09:0.075",
     "0.075", "some", 0),

    # ---- B. CII ---------------------------------------------------------
    ("cii: QB7_I G2/G4 reverted to 2021 pair", "QB7_I.html", "C-01",
     "MEPC.353(78) / MEPC.354(78)", "MEPC.337(76) / MEPC.339(76)"),
    ("cii: QB7_I 2021 pair asserted without revocation context", "QB7_I.html", "C-04:QB7_I#q10:MEPC.337(76)",
     "Each expressly <strong>revokes</strong> its 2021 predecessor &mdash; MEPC.353(78) revokes <strong>MEPC.337(76)</strong> and MEPC.354(78) revokes <strong>MEPC.339(76)</strong> &mdash; so quote the 2022 pair, not the 2021 pair.",
     "See also <strong>MEPC.337(76)</strong> and <strong>MEPC.339(76)</strong> for the same material."),
    ("cii: QB6 q1 reverted to 2021 pair", "QB6.html", "C-02",
     "<strong>MEPC.353(78)</strong> — CII reference lines (G2), 2022, revoked MEPC.337(76)",
     "<strong>MEPC.337(76)</strong> — CII reference lines (G2)"),
    ("cii: cheatsheet reverted to 2021 pair", "QB6_cheatsheet.html", "C-03",
     "<tr><td>MEPC.353(78) / MEPC.354(78)</td>", "<tr><td>MEPC.337(76) / MEPC.339(76)</td>"),
    ("cii: EEDI resolution restored as sole CII authority", "QB7_I.html", "C-05:QB7_I#q10",
     "The CII authority is <strong>G1, MEPC.352(78)</strong>",
     "The authority is <strong>MEPC.364(79)</strong>, and not MEPC dot 352"),

    # ---- C. BMP / security ---------------------------------------------
    ("bmp: QB4_B reasserts BMP5 as current", "QB4_B.html", "B-01:QB4_B#q16",
     "<strong>The current publication is not BMP5.</strong> It is <strong>BMP Maritime Security &mdash; 1st Edition 2025, updated 2026</strong>",
     "The current applicable version is <strong>BMP5</strong> (2018)"),
    ("bmp: QB9_A Key Numbers reasserts BMP5 as current", "QB9_A.html", "B-01:QB9_A#q9",
     "updated 2026:</strong> the current industry guide",
     "updated 2026:</strong> BMP5 is the current active edition of the industry guide"),
    ("bmp: QB9_B Key Numbers reasserts BMP5 as current", "QB9_B.html", "B-01:QB9_B#q5",
     "updated 2026:</strong> the current Best Management Practices publication",
     "updated 2026:</strong> BMP5 is the current active edition of the Best Management Practices publication"),
    ("bmp: company-specific claim reinstated (QB4_H)", "QB4_H.html", "B-04:QB4_H#q2",
     "<b>On My Vessel:</b> Answer from your own ship's actual arrangements.",
     "<b>On My Vessel:</b> Implemented through the Maersk Corporate Security Management System."),
    ("bmp: company-specific claim reinstated (QB9_B)", "QB9_B.html", "B-04:QB9_B#q5",
     "<p>Answer from your own ship and say what is actually done in your engine room before and during a high-risk transit:</p>",
     "<p>On a Maersk container liner, hardening protocols are integrated into engine room operations:</p>"),
    ("bmp: threat distinction flattened (QB9_A)", "QB9_A.html", "B-05:QB9_A#q9",
     "the correct destination is instead a <strong>security muster point above the waterline</strong>",
     "the correct destination is still the citadel"),
    ("bmp: steering-gear citadel unscoped from threat (QB9_B)", "QB9_B.html", "B-06:QB9_B#q5",
     "and appropriate where the threat is <strong>boarding</strong>",
     "and appropriate whatever the threat"),
    ("bmp: SSAS activation on area entry restored", "QB9_A.html", "B-07",
     "<strong>testing</strong> of the Ship Security Alert System &mdash; not its activation. Activating the SSAS transmits a covert security alert ashore; it is an <em>incident</em> action governed by the Ship Security Plan, never something you do merely because the ship has entered an area.".replace("&mdash;", "—"),
     "activation of the Ship Security Alert System (SSAS)."),
    ("bmp: 72-hour citadel baseline restored", "QB9_B.html", "B-09",
     "<li><strong>Citadel endurance",
     "<li><strong>72 Hours:</strong> The standard baseline requirement for provisions inside a citadel. Citadel endurance"),
    ("bmp: invented 6-bar fire main restored", "QB9_B.html", "B-11",
     "<li><strong>Fire main pressure",
     "<li><strong>6 Bar Pressure:</strong> The standard minimum at the fire main deck monitors. Fire main pressure"),
    ("bmp: LSA Code restored as escape authority", "QB9_B.html", "B-13",
     "No, sir. The authority is <strong>SOLAS II-2/13</strong>",
     "No, sir. Under SOLAS safety regulations and the international Life-Saving Appliance (LSA) code, mandatory emergency escape routes must never be locked. The authority is <strong>SOLAS II-2/13</strong>"),
    ("bmp: XI-2/8 restored as CE bypass authority", "QB4_B.html", "B-15",
     "Answer firmly but bound it:", "Your answer is that bypassing an alarm is fully justified under the Master's overriding authority. Answer firmly but bound it:"),
    ("bmp: IMO reinstated as a BMP publisher", "QB4_B.html", "B-18",
     "published by the industry associations <strong>BIMCO, ICS, IMCA, INTERCARGO, INTERTANKO and OCIMF</strong>",
     "published by BIMCO, ICS, IMO and EUNAVFOR"),

    # ---- D. Artefacts ---------------------------------------------------
    ("artefact: one [cite: 1] token reintroduced", "QB9_B.html", "D-01",
     "<span class=\"reg-code\">BMP Maritime Security</span>",
     "<span class=\"reg-code\">BMP Maritime Security[cite: 1]</span>"),
    ("artefact: scaffold reg-box block reintroduced", "QB8_A.html", "D-02",
     "</details>", "<pre>\n====\nREGULATORY REFERENCE BOX\n====\n</pre></details>"),
    ("artefact: scaffold correction footer reintroduced", "QB9_A.html", "D-03",
     "</details>", "<p><code>CORRECTION FOOTER: QB9_A &middot; Q1 &middot; v1.1</code></p></details>"),
]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def failing_ids():
    r = subprocess.run([sys.executable, VALIDATOR], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = []
    for line in (r.stdout or "").splitlines():
        m = re.match(r"^\S+\s+(\S+)\s+FAIL\b", line)
        if m:
            out.append(m.group(1))
    return out


def main():
    files = sorted({m[1] for m in MUTATIONS})
    base = {f: sha(os.path.join(QB, f)) for f in files}
    original = {f: io.open(os.path.join(QB, f), encoding="utf-8").read() for f in files}

    pre = failing_ids()
    if pre:
        print("ABORT: gates are not green before mutation: %s" % pre)
        return 1

    escapes, applied, restore_fail = [], 0, []
    for mut in MUTATIONS:
        label, fname, expect, find, repl = mut[:5]
        count = mut[5] if len(mut) > 5 else 1
        path = os.path.join(QB, fname)
        text = original[fname]
        if find not in text:
            print("%-56s  SKIP (anchor not found)" % label)
            escapes.append(label + " [anchor missing]")
            continue
        mutated = text.replace(find, repl) if count == 0 else text.replace(find, repl, count)
        io.open(path, "w", encoding="utf-8", newline="").write(mutated)
        applied += 1
        fails = failing_ids()
        caught = expect in fails
        # restore immediately - serial execution, one mutation live at a time
        io.open(path, "w", encoding="utf-8", newline="").write(text)
        if sha(path) != base[fname]:
            restore_fail.append(fname)
        print("%-56s  %-9s expected=%-28s %s" % (
            label, "CAUGHT" if caught else "ESCAPED", expect,
            "" if caught else ("(fails seen: %s)" % (fails or "none"))))
        if not caught:
            escapes.append(label)

    post = failing_ids()
    print("-" * 100)
    print("%d mutations applied, %d escapes" % (applied, len(escapes)))
    print("byte-exact restoration: %s" % ("OK for all %d files" % len(files)
                                          if not restore_fail else "FAILED: %s" % restore_fail))
    print("gates green after suite: %s" % ("yes" if not post else "NO - %s" % post))
    ok = not escapes and not restore_fail and not post
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
