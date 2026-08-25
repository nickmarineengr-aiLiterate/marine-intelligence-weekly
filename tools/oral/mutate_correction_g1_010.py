#!/usr/bin/env python3
"""Mutation suite for CORR-G1-010-RORO-ATTRIBUTION-20260825.

WHAT THIS SUITE PROVES
----------------------
`validate_correction_g1_010.py` asserts the SUBSTANCE of a correction to
published regulatory content.  Substance checks are the easiest kind of guard
to write badly: a check that a correct card cannot satisfy is noise, and a
check that a wrong card can satisfy is decoration.  So every mutation below
restores a specific way the defect could come back, and each must trip the ONE
named check that owns that property -- never the digest pin, which fires on any
edit at all and therefore proves nothing about what the edit said.

Two of the mutations exist because of things that actually happened:

    D  puts the wrong resolution back in the REG-BOX only, leaving the prose
       correct.  This repo has repaired prose and shipped the summary bullet,
       the Numbers block, the reg-box or an SVG label still stating the
       corrected-away claim.  D is the second-pass property, made assertable.

    J  drops the correction record's second review pass.  G1-010's second
       independent pass caught a MATERIAL defect that the FIRST round of fixes
       had introduced.  A record claiming one pass is claiming less assurance
       than this correction was actually given, and the gate should say so.

Mutation B is deliberately the inverse of a guard that had to be rewritten
during authoring: the first version of `no_wrong_attribution_on_any_surface`
used a +/- 260 character window and reported nine findings on a correct card,
because a card whose purpose is to CONTRAST two resolutions necessarily puts
them near each other.  B confirms the rescoped, sentence-level guard still
catches the real thing.

RESTORATION IS FROM A BYTE SNAPSHOT, IN EVERY PATH
--------------------------------------------------
Never from git.  `git checkout <ref> -- <file>` destroys uncommitted work, and
has already cost real edits in this repository.  A previous session also killed
a mutation suite on a timeout and left a deliberately-wrong content mutation
live on a paid page, so the suite re-probes after the run and reports residue.

  PYTHONIOENCODING=utf-8 python tools/oral/mutate_correction_g1_010.py
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_bytes import read_text, write_text, enable_utf8_stdio   # noqa: E402

enable_utf8_stdio()

MANIFEST = HERE / "correction_corr_g1_010_roro_attribution_20260825_manifest.json"
CARD = REPO / "meoclass1" / "QB2_F.html"
SIBLING = REPO / "meoclass1" / "QB10_B.html"

PROBES = {
    "g1_010": "validate_correction_g1_010.py",
    "corrections": "validate_corrections.py",
}


def run_probe(key: str) -> tuple[int, set]:
    out = subprocess.run([sys.executable, str(HERE / PROBES[key])],
                         cwd=str(REPO), capture_output=True, check=False)
    text = (out.stdout + out.stderr).decode("utf-8", "replace")
    failing = set(re.findall(r"^FAIL\s+(\S+)", text, re.M))
    for payload in re.findall(r"violations=\[([^\]]*)\]", text):
        failing.update(re.findall(r"'([^']+)'", payload))
    return out.returncode, failing


class Snapshot:
    """Byte-exact custody of every file a mutation touches."""

    def __init__(self, paths):
        self.data = {}
        for path in paths:
            p = pathlib.Path(path)
            self.data[p] = p.read_bytes() if p.is_file() else None

    def restore(self) -> list[str]:
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


# ------------------------------------------------------------------ helpers

def sub_in(target: pathlib.Path, old: str, new: str, count: int = 0):
    def apply():
        text = read_text(target)
        assert old in text, "mutation target absent from %s: %r" % (target.name, old[:70])
        write_text(target, text.replace(old, new) if count == 0
                   else text.replace(old, new, count))
    return apply


def edit_manifest(mutate):
    def apply():
        data = json.loads(read_text(MANIFEST))
        mutate(data)
        write_text(MANIFEST, json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    return apply


# ----------------------------------------------------------------- mutations
# (id, description, files touched, apply(), probe, the check it MUST break)

MUTATIONS = [
    ("A", "restore the wrong resolution in the 60-Second summary",
     [CARD],
     sub_in(CARD,
            "it also rewrites II-2/7.5.5, so smoke detection in all control "
            "stations <em>and</em> cargo control rooms is MSC.550(108), not "
            "MSC.532(107)",
            "MSC.532(107) also brings in ro-ro space detection and cargo "
            "control room alarms"),
     "g1_010", "no_wrong_attribution_on_any_surface"),

    ("B", "credit the vehicle and ro-ro spaces to MSC.532(107) in the body",
     [CARD],
     sub_in(CARD,
            "<h4>Chapter II-2 — Package 2: Res. MSC.550(108) (adopted 23 May 2024), "
            "with FSS Code Res. MSC.555(108)</h4>",
            "<h4>Chapter II-2 — Res. MSC.532(107) also covers vehicle, special "
            "category and ro-ro space detection</h4>"),
     "g1_010", "no_wrong_attribution_on_any_surface"),

    ("C", "delete MSC.550(108) from the card entirely",
     [CARD],
     sub_in(CARD, "MSC.550(108)", "the 2026 amendments"),
     "g1_010", "roro_package_credited_to_msc550"),

    ("D", "correct the prose but leave the wrong resolution in the REG-BOX",
     [CARD],
     sub_in(CARD,
            '<span class="reg-desc">Protection of vehicle, special category, open '
            'and closed ro-ro spaces and weather decks intended for vehicles — '
            'Res. MSC.550(108), eff. 1 Jan 2026',
            '<span class="reg-desc">Protection of vehicle, special category, open '
            'and closed ro-ro spaces and weather decks intended for vehicles — '
            'Res. MSC.532(107), eff. 1 Jan 2026'),
     "g1_010", "no_wrong_attribution_on_any_surface"),

    ("E", "move the entry into force off 1 January 2026",
     [CARD],
     sub_in(CARD, "1 January 2026", "1 January 2027"),
     "g1_010", "entry_into_force_stated"),

    ("F", "delete the existing-passenger-ship application date",
     [CARD],
     sub_in(CARD, "first survey on or after 1 January 2028",
            "first survey after entry into force"),
     "g1_010", "existing_ship_application_date_stated"),

    ("G", "claim the 10 mg/kg threshold is in MSC.532(107) itself",
     [CARD],
     sub_in(CARD,
            "The familiar <strong>10 mg/kg (0.001% by weight)</strong> figure is "
            "<em>not</em> in SOLAS: it comes from the unified interpretation in "
            "<strong>MSC.1/Circ.1694</strong> (4 Jul 2025), mirrored by IACS UI SC309.",
            "MSC.532(107) prohibits media above 10 mg/kg."),
     "g1_010", "pfos_threshold_attributed_to_the_circular"),

    ("H", "flatten the populations by deleting the cargo-ship detection limb",
     [CARD],
     sub_in(CARD, "20.4.1.5", "20.4.1"),
     "g1_010", "cargo_ship_limb_distinguished"),

    ("I", "leave the sibling card understating the video replay period",
     [SIBLING],
     sub_in(SIBLING,
            "replayable for <strong>at least seven days</strong> on ro-ro "
            "passenger ships built on/after 1 Jan 2026 and <strong>24 hours</strong> "
            "on existing ones",
            "replayable for <strong>24 hours</strong>"),
     "g1_010", "sibling_video_replay_is_not_understated"),

    ("J", "drop the correction's second independent review pass",
     [MANIFEST],
     edit_manifest(lambda d: d["review"].update({"passes": 1})),
     "g1_010", "review_ran_a_second_pass"),

    ("K", "leak the internal correction id onto the candidate surface",
     [CARD],
     sub_in(CARD, '<div class="numbers-box"><h4>Key Numbers</h4>',
            '<div class="numbers-box"><h4>Key Numbers</h4>CORR-G1-010 applied. '),
     "g1_010", "no_internal_vocabulary_on_the_candidate_surface"),

    ("L", "reword the governed question text under an unchanged record",
     [CARD],
     sub_in(CARD,
            "What are the latest SOLAS Chapter II amendments and their key changes?",
            "What are the newest SOLAS Chapter II changes?"),
     "g1_010", "primary_question_text_unchanged"),

    ("M", "corrupt the declared post-edit digest",
     [MANIFEST],
     edit_manifest(lambda d: d["cards"][0].__setitem__("post_edit_digest", "0" * 64)),
     "g1_010", "live_state_matches_the_record"),

    ("N", "change an undeclared card on the same page",
     [CARD],
     sub_in(CARD, '<div class="q-card" id="q5"',
            '<div class="q-card" id="q5"><!--mutation-probe-->', 1),
     "corrections", "no_undeclared_change_in_window"),
]


# ---------------------------------------------------------------------- main

def main() -> int:
    if not MANIFEST.is_file():
        print("correction record missing: %s" % MANIFEST.name)
        return 2

    print("--- preflight: every mutation must change bytes ---")
    no_ops = []
    for mid, desc, files, apply, _probe, _check in MUTATIONS:
        snap = Snapshot(files)
        before = dict(snap.data)
        try:
            apply()
        except Exception as exc:
            print("%-3s ERROR %s: %s" % (mid, type(exc).__name__, exc))
            no_ops.append(mid)
            snap.restore()
            continue
        after = {p: (p.read_bytes() if p.is_file() else None) for p in snap.data}
        changed = any(before[p] != after[p] for p in before)
        delta = sum(len(after[p] or b"") - len(before[p] or b"") for p in before)
        print("%-3s %-62s %-8s byte_delta=%+d"
              % (mid, desc, "applied" if changed else "NO-OP", delta))
        if not changed:
            no_ops.append(mid)
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    if no_ops:
        print("\npreflight FAILED -- these mutations change no bytes: %s"
              % ", ".join(no_ops))
        print("0 mutations, 0 escape(s), %d no-op(s), 0 crash(es)" % len(no_ops))
        return 1

    print("\n--- control: unmutated state ---")
    control_dirty = False
    for key in PROBES:
        rc, failing = run_probe(key)
        print("CTL %-12s exit=%d failing=%s" % (key, rc, sorted(failing) or "none"))
        if failing:
            control_dirty = True
    if control_dirty:
        print("CONTROL IS NOT GREEN -- every later 'catch' would be meaningless")
        return 1

    print("\n--- mutations ---")
    caught, escapes, crashes = 0, [], []
    for mid, desc, files, apply, probe, want in MUTATIONS:
        snap = Snapshot(files)
        try:
            apply()
            rc, failing = run_probe(probe)
        except Exception as exc:
            print("%-3s CRASH  %s: %s" % (mid, type(exc).__name__, exc))
            crashes.append(mid)
            snap.restore()
            continue
        hit = want in failing
        if hit:
            caught += 1
        else:
            escapes.append("%s (wanted %s, got %s)"
                           % (mid, want, sorted(failing) or "nothing"))
        print("%-3s %-62s %s  [%s]"
              % (mid, desc, "CAUGHT " if hit else "ESCAPED", want))
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    # Residue probe: the control must be green again, byte-for-byte.
    print("\n--- residue probe ---")
    residue = False
    for key in PROBES:
        rc, failing = run_probe(key)
        print("RES %-12s exit=%d failing=%s" % (key, rc, sorted(failing) or "none"))
        if failing:
            residue = True

    print("\n%d caught of %d" % (caught, len(MUTATIONS)))
    print("%d mutations, %d escape(s), 0 no-op(s), %d crash(es)"
          % (len(MUTATIONS), len(escapes), len(crashes)))
    for line in escapes:
        print("  ESCAPE %s" % line)
    if residue:
        print("  RESIDUE: a probe is still red after restore")
    return 0 if (not escapes and not crashes and not residue) else 1


if __name__ == "__main__":
    raise SystemExit(main())
