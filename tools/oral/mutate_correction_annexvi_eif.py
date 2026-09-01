#!/usr/bin/env python3
"""Mutation suite for CORR-ANNEXVI-EIF-20260901.

Two rules from SKILL 8.2a govern every mutation here:

1. **Each mutation's required check must be a CONTENT check, never the digest
   pin.** Any edit to a card trips the pin, so accepting the pin as the catch
   would prove only that the pin works while the substantive checks rot into
   dead code. `validate_corrections.py` owns the pin; this file owns the
   proposition.

2. **A correction quotes the wording it rejects**, so nothing here may be a
   flat banned-phrase grep. Known trap 59 has to print `1 January 2023` in
   order to reject it, and the corrected cards have to keep that date as the
   APPLICATION limb. A guard that banned the string would fail on the fix.

The mutations attack the four ways this correction can be undone:

    put the wrong date back            -> the closed-world claim check
    delete the application limb        -> both limbs must survive
    restate the RECORD to authorise it -> the record must still claim what it claims
    trim the trap to one variant       -> the register must carry both renderings

and one that attacks the gate's own reach:

    move the defect to a page the correction did not touch, spelled the way
    QB7_C spells it -> the closed-world pass must still find it

That last one is the point of the whole design. The defect was found in
QB7_A by a targeted grep for "MEPC.328(76)"; the EIGHTH occurrence, in QB7_C,
spells the resolution "MEPC 76" and no such grep could reach it.

  PYTHONIOENCODING=utf-8 python tools/oral/mutate_correction_annexvi_eif.py

Exit 0 if every mutation is caught by its own check, 1 otherwise.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
MEO = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio, read_text, write_text   # noqa: E402

enable_utf8_stdio()

VALIDATOR = HERE / "validate_correction_annexvi_eif.py"
MANIFEST = HERE / "correction_corr_annexvi_eif_20260901_manifest.json"
TRAPS = MEO / "known_traps.md"
QB7_A = MEO / "QB7_A.html"
SHEET = MEO / "QB7_A_CheatSheet.html"
QB1_C = MEO / "QB1_C.html"


def run_probe() -> tuple[int, set]:
    out = subprocess.run([sys.executable, str(VALIDATOR)],
                         cwd=str(REPO), capture_output=True, check=False)
    text = (out.stdout + out.stderr).decode("utf-8", "replace")
    return out.returncode, set(re.findall(r"^FAIL\s+(\S+)", text, re.M))


class Snapshot:
    def __init__(self, paths):
        self.data = {pathlib.Path(p): (pathlib.Path(p).read_bytes()
                                       if pathlib.Path(p).is_file() else None)
                     for p in paths}

    def restore(self):
        bad = []
        for path, blob in self.data.items():
            if blob is None:
                if path.is_file():
                    path.unlink()
                continue
            path.write_bytes(blob)
            if path.read_bytes() != blob:
                bad.append(str(path))
        return bad


def sub(target, old, new):
    def apply():
        t = read_text(target)
        assert old in t, "mutation target absent: %r" % old[:70]
        write_text(target, t.replace(old, new, 1))
    return apply


def edit_manifest(mutate):
    def apply():
        d = json.loads(read_text(MANIFEST))
        mutate(d)
        write_text(MANIFEST, json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    return apply


def m_record_authorises_the_wrong_date(d):
    d["rationale"] = d["rationale"].replace("1 November 2022", "1 January 2023")


def m_record_drops_the_application_limb(d):
    d["rationale"] = d["rationale"].replace("OBLIGATIONS", "requirements")
    d["rationale"] = d["rationale"].replace("1 January 2023", "")


def m_record_forgets_the_trap(d):
    d["known_traps_entries"] = []


def m_sheet_loses_the_application_limb():
    x = read_text(SHEET)
    a = "in force <strong>1 Nov 2022</strong>; obligations apply from <strong>1 Jan 2023</strong>"
    b = "in force 1 Nov 2022; obligations apply from 1 Jan 2023"
    assert a in x and b in x, "mutation targets absent"
    write_text(SHEET, x.replace(a, "in force <strong>1 Nov 2022</strong>")
                       .replace(b, "in force 1 Nov 2022"))


MUTATIONS = [
    ("A", "put the wrong entry-into-force date back on the primary card",
     [QB7_A],
     sub(QB7_A, "entering into force <strong>1 November 2022</strong>",
                "entering into force <strong>1 January 2023</strong>"),
     "eif_no_other_entry_into_force_date_for_this_resolution"),

    # Deleting ONE of the sheet's two application-limb statements is not the
    # regression -- a reference row may correctly give the entry-into-force
    # date alone. The regression is a sheet that teaches one date and never
    # the other, so this removes both.
    ("B", "delete the application limb from the cheat sheet entirely",
     [SHEET], m_sheet_loses_the_application_limb,
     "eif_QB7_A_CheatSheet.html_keeps_application_limb"),

    ("C", "restate the RECORD so it authorises the wrong date",
     [MANIFEST], edit_manifest(m_record_authorises_the_wrong_date),
     "eif_record_states_the_right_date"),

    ("D", "strip the two-limb distinction out of the record",
     [MANIFEST], edit_manifest(m_record_drops_the_application_limb),
     "eif_record_keeps_the_application_limb"),

    ("E", "detach the correction from the trap that authorises it",
     [MANIFEST], edit_manifest(m_record_forgets_the_trap),
     "eif_record_cites_the_trap"),

    ("F", "trim the trap register back to the one wrong rendering it started with",
     [TRAPS],
     sub(TRAPS, "a *different* wrong value for the same fact — **1 January 2023** —",
                "a *different* wrong value for the same fact —"),
     "eif_trap_59_names_both_wrong_renderings"),

    ("G", "reintroduce the defect on an UNTOUCHED page, spelled 'MEPC 76'",
     [QB1_C],
     sub(QB1_C, "Note the renumbering by MEPC.328(76)",
                "MEPC 76 is in force 1 January 2023. "
                "Note the renumbering by MEPC.328(76)"),
     "eif_no_other_entry_into_force_date_for_this_resolution"),
]


def main() -> int:
    if not VALIDATOR.is_file() or not MANIFEST.is_file():
        print("correction gate or record missing")
        return 2

    print("--- preflight: every mutation must change content ---")
    no_ops = []
    for mid, desc, paths, apply, _req in MUTATIONS:
        snap = Snapshot(paths)
        before = dict(snap.data)
        try:
            apply()
        except Exception as exc:
            print("%-3s ERROR %s: %s" % (mid, type(exc).__name__, exc))
            snap.restore(); no_ops.append(mid); continue
        after = {q: (q.read_bytes() if q.is_file() else None) for q in snap.data}
        changed = after != before
        print("%-3s %-62s changed=%s" % (mid, desc[:62], changed))
        if not changed:
            no_ops.append(mid)
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad); return 2
    if no_ops:
        print("\npreflight FAILED -- no content change: %s" % ", ".join(no_ops))
        print("0 mutations, 0 escape(s), %d no-op(s), 0 crash(es)" % len(no_ops))
        return 1

    print("\n--- control: unmutated state ---")
    rc, failing = run_probe()
    print("CTL annexvi_eif  exit=%d failing=%s" % (rc, sorted(failing) or "none"))
    if failing:
        print("CONTROL IS NOT GREEN -- every later 'catch' would be meaningless")
        return 2

    print("\n--- mutations ---")
    caught, escapes, crashes = 0, [], 0
    for mid, desc, paths, apply, required in MUTATIONS:
        snap = Snapshot(paths)
        try:
            apply()
        except Exception as exc:
            print("%-3s CRASH  %s: %s" % (mid, type(exc).__name__, exc))
            snap.restore(); crashes += 1; continue
        rc, failing = run_probe()
        hit = required in failing
        caught += 1 if hit else 0
        if not hit:
            escapes.append("%s: %s (wanted %r, got %s)"
                           % (mid, desc, required, sorted(failing) or "none"))
        print("%-3s %-62s %s" % (mid, desc[:62], "caught" if hit else "ESCAPED"))
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad); return 2

    print("\n--- residue probe ---")
    rc, failing = run_probe()
    print("RES annexvi_eif  exit=%d failing=%s" % (rc, sorted(failing) or "none"))

    print("\n%d caught of %d" % (caught, len(MUTATIONS)))
    print("%d mutations, %d escape(s), 0 no-op(s), %d crash(es)"
          % (len(MUTATIONS), len(escapes), crashes))
    for line in escapes:
        print("  ESCAPE %s" % line)
    return 0 if (not escapes and not crashes and not failing) else 1


if __name__ == "__main__":
    raise SystemExit(main())
