#!/usr/bin/env python3
"""
Mutation suite for GPT REVIEW PASS 3 -- the two residual content records.

WHAT THIS SUITE HAS TO PROVE
----------------------------
`validate_correction_pass3.py` went green the moment it was written, which is
what a validator written alongside its own subject always does.  Green output
does not distinguish a check that is asserting something from a check that
cannot fail.  So every mutation below reinstates, precisely, the defect the
review corrected, and requires the NAMED check to be the one that goes red.

A MUTATION MUST BREAK THE CHECK IT NAMES
----------------------------------------
A validator that fails for the wrong reason is not evidence.  E6's mutation L
is the reason this is enforced: it corrupted a field nothing read, and the
suite's coarse verdict said "caught" because something else was failing anyway.
Extra failures are tolerated -- reinstating a defect legitimately trips more
than one check -- but the named one must be among them.

TWO PROBES, AND THE SECOND ONE IS THE POINT
-------------------------------------------
Mutations A and B are ALSO required to trip Pass 2B's
`no_msact2025_claim_says_formal_investigation`.  Pass 2B could see these two
surfaces and was not authorised to correct them, so it enumerated them in its
allowlist as "reported, not corrected".  This pass corrects them and RETIRES
those two entries.  Requiring the PASS 2B gate to catch a reinstatement is what
proves the retirement restored that gate's reach, rather than merely tidying a
tuple -- and it is the one claim this suite could not make by probing its own
validator.

CUSTODY
-------
Every mutation runs inside `oral_custody.Custodian`: restored on return, on
raise, on KeyboardInterrupt and on SystemExit alike, journalled to disk before
the first byte changes, and verified byte-for-byte plus `git status` at the end.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
MEO = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import read_text, write_text                       # noqa: E402
from oral_custody import Custodian, CustodyError, stale_runs       # noqa: E402

QB5CB = MEO / "QB5_C_B.html"
QB5B = MEO / "QB5_B.html"
CHEAT = MEO / "QB5_B_CheatSheet.html"
M2B = HERE / "validate_correction_msact2b.py"

PROBES = {
    "pass3": "validate_correction_pass3.py",
    "msact2b": "validate_correction_msact2b.py",
}


def run_probe(key):
    out = subprocess.run([sys.executable, str(HERE / PROBES[key])],
                         cwd=str(REPO), capture_output=True, check=False)
    text = (out.stdout + out.stderr).decode("utf-8", "replace")
    return out.returncode, set(re.findall(r"^FAIL\s+(\S+)", text, re.M))


def sub_in(path, old, new, count=1):
    """Replace exactly `count` occurrences, and refuse to be a no-op.

    A mutation that silently matches nothing is the worst outcome a suite of
    this shape can have: it reports a catch that was really the corpus already
    failing, or a clean pass over a check it never exercised.
    """
    def apply():
        text = read_text(path)
        found = text.count(old)
        if found != count:
            raise AssertionError("expected %d occurrence(s) in %s, found %d"
                                 % (count, path.name, found))
        write_text(path, text.replace(old, new))
    return apply


# The corrected 60-second sentence, verbatim, so a reinstatement is exact.
CORRECTED_60S = (
    "I move to evidence preservation for the flag State’s <strong>marine "
    "safety investigation</strong> — the term the <strong>IMO Casualty "
    "Investigation Code</strong> actually uses, and under that Code the "
    "investigation is conducted by the flag State’s marine safety "
    "investigation Authority, not by me — and to the company’s own "
    "investigation under <strong>ISM Code §9</strong>.")
STALE_60S = ("I transition to the formal investigation phase under the "
             "<strong>IMO Casualty Investigation Code</strong> and the ISM Code.")

ISM9_LIMB = (" — and to the company’s own investigation under "
             "<strong>ISM Code §9</strong>.")

DENIAL = (" The 2025 Act does not use “formal investigation” for this "
          "machinery.")

RETIRED_ENTRY = (
    "    # validate_correction_pass3.no_adjudicated_entry_is_a_dead_noop keeps every\n"
    "    # surviving entry honest on the same terms.\n)")


MUTATIONS = [
    ("A", "reinstate the IMO-Code 'formal investigation' attribution",
     [QB5CB], sub_in(QB5CB, CORRECTED_60S, STALE_60S),
     [("pass3", "no_imo_code_formal_investigation_attribution"),
      ("msact2b", "no_msact2025_claim_says_formal_investigation")]),

    ("B", "reinstate the 'Formal Investigation' body heading",
     [QB5CB],
     sub_in(QB5CB,
            "<h5>Evidence Preservation &amp; Company Investigation Procedure</h5>",
            "<h5>Formal Investigation &amp; Evidence Preservation Procedure</h5>"),
     [("pass3", "no_imo_code_formal_investigation_attribution"),
      ("msact2b", "no_msact2025_claim_says_formal_investigation")]),

    ("C", "delete the ISM 9 company-investigation limb from the 60-second",
     [QB5CB], sub_in(QB5CB, ISM9_LIMB, "."),
     [("pass3", "company_investigation_is_ism_9")]),

    ("D", "strip the flag-State ownership limb, keeping the corrected term",
     [QB5CB],
     sub_in(QB5CB,
            " — the term the <strong>IMO Casualty Investigation "
            "Code</strong> actually uses, and under that Code the investigation "
            "is conducted by the flag State’s marine safety investigation "
            "Authority, not by me —", " under the Code, and"),
     [("pass3", "cic_investigation_not_claimed_by_the_ce")]),

    ("E", "revert the QB5_B reg-box row to ISM Code section 5",
     [QB5B],
     sub_in(QB5B, '<span class="reg-code">ISM Code §6.3</span>',
            '<span class="reg-code">ISM Code §5</span>'),
     [("pass3", "qb5b_q1_cites_no_ism_section_5")]),

    ("F", "claim ISM 6.3 mandates a CE takeover certificate",
     [QB5B],
     sub_in(QB5B, "No ISM clause prescribes a CE takeover certificate",
            "ISM Code §6.3 requires a signed CE takeover certificate"),
     [("pass3", "no_clause_said_to_require_a_certificate")]),

    ("G", "revert the cheat sheet's pre-arrival hook to ISM Code section 5",
     [CHEAT],
     sub_in(CHEAT,
            "<td>Company SMS handover procedure; ISM Code §6.3 "
            "(familiarisation on a new assignment) / SOLAS V/14</td>",
            "<td>ISM Code §5 / SOLAS V/14</td>"),
     [("pass3", "cheatsheet_cites_no_ism_section_5")]),

    ("H", "delete the MS Act 'does not use formal investigation' denial",
     [QB5CB], sub_in(QB5CB, DENIAL, ""),
     [("pass3", "msact_denial_survives")]),

    ("I", "substitute section 5 blindly across the whole cheat sheet",
     [CHEAT], sub_in(CHEAT, "VIII/2 §5", "VIII/2 §6.3", count=2),
     [("pass3", "stcw_viii_2_para_5_untouched")]),

    ("J", "delete the Pass 2B cheat-sheet 'no takeover certificate' fix",
     [CHEAT],
     sub_in(CHEAT, ", and no ISM clause prescribes a takeover certificate", ""),
     [("pass3", "formal_declaration_row_survives")]),

    ("K", "re-add a retired entry to the Pass 2B allowlist",
     [M2B],
     sub_in(M2B, RETIRED_ENTRY,
            RETIRED_ENTRY[:-1]
            + "    'Formal Investigation & Evidence Preservation Procedure',\n)"),
     [("pass3", "retired_allowlist_entries_removed")]),
]


def main() -> int:
    if stale_runs(REPO):
        print("REFUSING TO RUN -- unrecovered mutation journal present; run "
              "`python tools/oral/mutate_corrections.py --recover` first")
        return 2

    dirt_before = subprocess.run(["git", "status", "--porcelain"], cwd=str(REPO),
                                 capture_output=True).stdout

    cust = Custodian(REPO, name="pass3-content")
    escapes, crashes, caught = [], [], 0
    try:
        # ---- preflight: every mutation must really change bytes -------------
        print("--- preflight: every mutation must change bytes ---")
        no_ops = []
        for mid, desc, files, apply, _want in MUTATIONS:
            with cust.guard(files):
                try:
                    apply()
                except Exception as exc:
                    print("%-3s ERROR %s: %s" % (mid, type(exc).__name__, exc))
                    no_ops.append(mid)
                    continue
                changed = any(
                    cust.original(p) != (pathlib.Path(p).read_bytes()
                                         if pathlib.Path(p).is_file() else None)
                    for p in files)
                print("%-3s %-58s %s" % (mid, desc,
                                         "applied" if changed else "NO-OP"))
                if not changed:
                    no_ops.append(mid)
        if no_ops:
            print("\npreflight FAILED -- no-ops: %s" % ", ".join(no_ops))
            return 1

        # ---- control --------------------------------------------------------
        print("\n--- control: unmutated, both gates must be green ---")
        control = {}
        for key in ("pass3", "msact2b"):
            rc, failing = run_probe(key)
            control[key] = failing
            print("CTL %-9s exit=%d failing=%s" % (key, rc, sorted(failing) or "none"))
        if control["pass3"] or control["msact2b"]:
            print("CTL CONTROL IS NOT GREEN -- every later catch is meaningless")
            escapes.append("CTL")

        # ---- the suite ------------------------------------------------------
        print("\n--- mutations ---")
        for mid, desc, files, apply, wants in MUTATIONS:
            with cust.guard(files):
                try:
                    apply()
                    results = {p: run_probe(p)[1] for p, _ in wants}
                except Exception as exc:
                    print("%-3s %-58s CRASH %s" % (mid, desc, exc))
                    crashes.append(mid)
                    continue

            missed = []
            for probe, want in wants:
                new = results[probe] - control.get(probe, set())
                if want not in new:
                    missed.append("%s wanted=%s got=%s"
                                  % (probe, want, sorted(new) or "none"))
            if missed:
                escapes.append(mid)
                print("%-3s %-58s ESCAPED  %s" % (mid, desc, "; ".join(missed)))
            else:
                caught += 1
                print("%-3s %-58s CAUGHT   %s"
                      % (mid, desc, ", ".join("%s/%s" % w for w in wants)))

        print("\n%d mutations, %d escape(s), %d crash(es)"
              % (len(MUTATIONS), len(escapes), len(crashes)))
        if escapes:
            print("escaped: %s" % ", ".join(escapes))

        # ---- closing integrity ---------------------------------------------
        print("\n--- closing integrity ---")
        drift = cust.verify_pristine()
        dirt_after = subprocess.run(["git", "status", "--porcelain"],
                                    cwd=str(REPO), capture_output=True).stdout
        print("custody drift: %s" % (drift or "none"))
        print("git status restored: %s" % (dirt_after == dirt_before))
        if drift or dirt_after != dirt_before:
            print("HARD FAIL -- the working tree was NOT restored.")
            return 2
        return 1 if (escapes or crashes) else 0
    finally:
        leftover = cust.restore_all()
        if leftover:
            print("SUITE-LEVEL RESTORE FAILED: %s" % leftover)
        cust.close()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CustodyError as exc:
        print("\nHARD FAIL -- custody: %s" % exc)
        sys.exit(2)
