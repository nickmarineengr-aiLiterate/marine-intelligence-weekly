#!/usr/bin/env python3
"""
Mutation suite for CORR-CSM-BOILER-SURVEY-20260823.

Each mutation reintroduces the defect in one of the shapes it could plausibly
come back in, runs validate_correction_csmboiler.py as a subprocess, and
requires that the NAMED check for that shape fails - not merely the digest
pin, which fires on any edit at all and would therefore pass every mutation
without proving anything about the substance.

  A  "main boilers" put back into the Vital Auxiliary Systems bullet
  B  the boiler re-listed under a different wording in the same bullet
  C  the "Not the boiler itself" bullet deleted
  D  the 36-month Boiler Survey interval dropped
  E  the boiler auxiliaries stripped back out of the CMS list
  F  the unsupported IACS PR 1C citation restored
  G  the manifest's authority block emptied
  H  ClassNK stripped of its implementation-example label
  I  the Indian authority-order bullet deleted
  J  the CSM-vs-CE-credit trap bullet deleted
  K  the pressure-boundary framing reverted
  L  the retired name "DG Shipping" offered as a live alternative
  M  the "formerly DG Shipping" gloss dropped

Every mutation is preflighted in memory. A mutation that matches nothing
writes nothing and exercises nothing: it is an absent test that reports like a
passing one, so a no-op aborts the suite before any file is touched. Every
file is restored byte-for-byte afterwards.

    PYTHONIOENCODING=utf-8 python tools/oral/mutate_correction_csmboiler.py
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]

sys.path.insert(0, str(HERE))

# Reach the shared UTF-8 stdio contract in THIS file's source. Inheriting it
# as a side effect of somebody else's import is a contract satisfied only at
# runtime, and it stops being true the moment that import moves -- which is
# why test_oral_release_infra scans sources rather than processes.
from oral_bytes import enable_utf8_stdio  # noqa: E402

enable_utf8_stdio()
VALIDATOR = HERE / "validate_correction_csmboiler.py"
PAGE = REPO / "meoclass1" / "QB1_G.html"
MANIFEST = HERE / "correction_corr_csm_india_authority_20260823_manifest.json"

AUX_BULLET = (
    "boiler <em>auxiliaries</em> — IRS names forced or induced draught fans")
AUTHORITY_BULLET = "<li><strong>Answer this one in the Indian order:</strong>"
CREDIT_BULLET = "<li><strong>The trap: \"in CSM\" is not the same as"
CLASSNK_QUALIFIER = "Implementation example only, not Indian authority."
NOT_ITSELF = "<li><strong>Not the boiler itself:</strong>"
UR_Z18 = '<span class="reg-code">IACS UR Z18</span>'


def run_validator():
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    p = subprocess.run([sys.executable, str(VALIDATOR)],
                       capture_output=True, text=True, cwd=str(REPO), env=env)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def failing_checks(out: str) -> set:
    return {ln.split()[1] for ln in out.splitlines()
            if ln.startswith("FAIL") and len(ln.split()) > 1}


def sub(path, old, new):
    def apply(raw):
        t = raw.decode("utf-8")
        if old not in t:
            return None
        return t.replace(old, new, 1).encode("utf-8")
    return path, apply


def _drop_bullet(raw):
    """Delete the whole boiler-exclusion bullet, not just its heading.

    An earlier version of this mutation swapped only the <strong> label and
    left the sentence "Boilers ... are not CSM items" in place, so the check
    it was aiming at kept passing -- correctly, because the claim was still
    on the card. A mutation has to remove the substance to test the check
    that guards the substance.
    """
    t = raw.decode("utf-8")
    i = t.find(NOT_ITSELF)
    if i < 0:
        return None
    j = t.find("</li>", i)
    if j < 0:
        return None
    return (t[:i] + t[j + len("</li>"):]).encode("utf-8")


def _drop_li(raw, opener):
    """Delete a whole <li> by its opening fragment."""
    t = raw.decode("utf-8")
    i = t.find(opener)
    if i < 0:
        return None
    j = t.find("</li>", i)
    if j < 0:
        return None
    return (t[:i] + t[j + len("</li>"):]).encode("utf-8")


def drop_authority(raw):
    d = json.loads(raw.decode("utf-8"))
    if not d.get("authority"):
        return None
    d["authority"] = []
    return (json.dumps(d, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


MUTATIONS = [
    ("A", "'main boilers' restored to the CSM list",
     "boiler_not_a_listed_csm_item",
     sub(PAGE, "emergency fire pumps, heat exchangers",
         "emergency fire pumps, main boilers, heat exchangers")),

    ("B", "boiler re-listed under different wording",
     "boiler_not_a_listed_csm_item",
     sub(PAGE, "<li>Vital Auxiliary Systems (Main air compressors",
         "<li>Vital Auxiliary Systems (auxiliary boilers, Main air compressors")),

    ("C", "the boiler-exclusion bullet deleted",
     "boiler_excluded_from_csm_stated",
     (PAGE, lambda raw: _drop_bullet(raw))),

    ("D", "the 36-month Boiler Survey interval dropped",
     "boiler_survey_36_month_interval",
     sub(PAGE, "never exceeding <strong>36 months</strong>",
         "set by the attending surveyor")),

    ("E", "boiler auxiliaries stripped out of the CMS list",
     "boiler_auxiliaries_still_in_list",
     sub(PAGE, AUX_BULLET, "heat exchangers")),

    ("F", "unsupported IACS PR 1C citation restored",
     "pr1c_citation_not_restored",
     sub(PAGE, UR_Z18, '<span class="reg-code">IACS PR 1C</span>')),

    ("G", "manifest authority block emptied",
     "primary_authority_recorded",
     (MANIFEST, drop_authority)),

    ("H", "ClassNK stripped of its implementation-example label",
     "classnk_never_presented_as_authority",
     sub(PAGE, CLASSNK_QUALIFIER, "The governing CMS equipment list.")),

    ("I", "the Indian authority-order bullet deleted",
     "administration_named_in_full",
     (PAGE, lambda raw: _drop_li(raw, AUTHORITY_BULLET))),

    ("J", "the CSM-vs-CE-credit trap bullet deleted",
     "csm_vs_ce_credit_distinction",
     (PAGE, lambda raw: _drop_li(raw, CREDIT_BULLET))),

    ("L", "the retired name offered as a live alternative again",
     "dg_shipping_not_offered_as_a_current_name",
     sub(PAGE, "The <strong>Directorate General of Maritime Administration</strong> (formerly DG Shipping)",
         "<strong>DG Shipping / DGMA</strong>")),

    # Anchored on q40's own sentence. A bare " (formerly DG Shipping)" matched
    # an EARLIER question on the same page first -- QB1_G#q13 carries "the DGMA
    # (Directorate General of Maritime Administration, formerly DG Shipping)" --
    # so the mutation edited a card the validator does not read and escaped.
    ("M", "the historical gloss dropped, orphaning older circular titles",
     "former_name_kept_as_gloss_only",
     sub(PAGE, "</strong> (formerly DG Shipping) prescribes",
         "</strong> prescribes")),

    ("K", "the pressure-boundary framing reverted to the base wording",
     "pressure_boundary_framing",
     sub(PAGE, "The boiler's <em>pressure boundary</em> is not on the CSM clock.",
         "Boilers are not CSM items.")),
]


def main() -> int:
    rc, out = run_validator()
    if rc != 0:
        print("ABORT: the validator is not green before mutation\n" + out)
        return 2

    planned = []
    for mid, label, expect, (path, apply) in MUTATIONS:
        original = path.read_bytes()
        mutated = apply(original)
        if mutated is None or mutated == original:
            print("ABORT: mutation %s (%s) is a no-op against %s"
                  % (mid, label, path.name))
            return 2
        planned.append((mid, label, expect, path, original, mutated))
    print("preflight: %d/%d mutations change bytes\n" % (len(planned), len(MUTATIONS)))

    escapes = crashes = 0
    for mid, label, expect, path, original, mutated in planned:
        path.write_bytes(mutated)
        try:
            rc, out = run_validator()
        finally:
            path.write_bytes(original)
            assert path.read_bytes() == original, "restore failed for " + path.name

        fails = failing_checks(out)
        caught = rc != 0 and expect in fails and "Traceback" not in out
        if "Traceback" in out:
            crashes += 1
        if not caught:
            escapes += 1
        print("%s  %-46s %s" % (mid, label, "CAUGHT" if caught else "ESCAPED"))
        if not caught:
            print("    expected check to fail: %s" % expect)
            print("    actually failing: %s" % (sorted(fails) or "none"))

    rc, out = run_validator()
    residue = rc != 0
    print()
    print("%d mutations, %d escapes" % (len(MUTATIONS), escapes))
    print("crashes=%d residue=%s" % (crashes, residue))
    if residue:
        print("RESIDUE: the validator is not green after restore\n" + out)
    return 1 if (escapes or crashes or residue) else 0


if __name__ == "__main__":
    sys.exit(main())
