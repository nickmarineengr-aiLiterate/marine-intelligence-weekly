#!/usr/bin/env python3
"""
Shared harness for CONTENT-gate mutation suites.

WHY THIS MODULE EXISTS
----------------------
`mutate_correction_lsavent.py` and `mutate_correction_g1_010.py` each grew
their own copy of the same four things: a byte-exact snapshot/restore, a probe
runner that lifts FAILing check names out of a validator's stdout, a card-text
substituter that asserts its target exists, and a manifest editor. Three more
content corrections landed on 2026-09-02, and copying that machinery a third,
fourth and fifth time is how ten copies of one glob let two record families
drift apart in the first place (SKILL.md section 8).

The rule this harness encodes, and the reason content suites are hard:

    A MUTATION THAT TRIPS THE DIGEST PIN IS NOT A CATCH.

Every mutation that edits a card also breaks `card_digest_matches_manifest`,
because the pin fires on any byte change at all. If a suite accepted that as
the catch it would prove only that the pin works -- which was never in doubt --
while every substantive check could be dead code. So each mutation NAMES the
check it must break, `required` is never the digest pin, and a mutation whose
named check stays green is an ESCAPE even when the probe exits non-zero.
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

from oral_bytes import read_text, write_text          # noqa: E402

# Checks that fire on ANY byte change and therefore can never be a valid
# `required` for a mutation. Named here so a suite cannot quietly regress into
# accepting the pin as its evidence.
DIGEST_PINS = {
    "card_digest_matches_manifest",
    "card_digest_matches_manifest_q11",
    "card_digest_matches_manifest_q33",
    "live_matches_authorised_post_state",
}


class Snapshot:
    """Byte-exact custody of every file a mutation touches.

    Restores from what this object personally read, never from git:
    `git checkout <ref> -- <file>` destroys uncommitted work, which has already
    cost real edits in this repository.
    """

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


def run_probe(script: str) -> tuple[int, set]:
    """Run one validator; return (exit code, set of FAILing check names)."""
    out = subprocess.run([sys.executable, str(HERE / script)],
                         cwd=str(REPO), capture_output=True, check=False)
    text = (out.stdout + out.stderr).decode("utf-8", "replace")
    failing = set(re.findall(r"^FAIL\s+(\S+)", text, re.M))
    # validate_corrections rolls its schema audit into one aggregate check and
    # names the violated sub-checks in `violations=[...]`. Lift them out so a
    # schema mutation cannot be satisfied by the aggregate name alone.
    for payload in re.findall(r"violations=\[([^\]]*)\]", text):
        failing.update(re.findall(r"'([^']+)'", payload))
    return out.returncode, failing


def sub_in_file(path, old: str, new: str, count: int = 0):
    """Replace text in a live file, asserting the target actually exists."""
    def apply():
        text = read_text(path)
        assert old in text, "mutation target absent from %s: %r" % (
            pathlib.Path(path).name, old[:70])
        write_text(path, text.replace(old, new) if count == 0
                   else text.replace(old, new, count))
    return apply


def edit_json(path, mutate):
    def apply():
        data = json.loads(read_text(path))
        mutate(data)
        write_text(path, json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    return apply


def run_suite(title: str, probe_script: str, mutations, watched_paths) -> int:
    """Apply each mutation, require its OWN named check to go red, restore.

    `mutations` is a sequence of (id, description, apply_fn, required_check).
    """
    print(title)
    print("=" * len(title))

    for mid, _desc, _apply, want in mutations:
        if want in DIGEST_PINS:
            print("SUITE ERROR: %s requires a digest pin (%s) as its catch"
                  % (mid, want))
            return 2

    code, control = run_probe(probe_script)
    if control:
        print("control is not green: failing=%s" % sorted(control))
        return 2
    print("control: %s exits %d with no failing check\n" % (probe_script, code))

    caught, escapes, crashes = 0, [], []
    for mid, desc, apply, want in mutations:
        snap = Snapshot(watched_paths)
        try:
            apply()
        except Exception as exc:                      # noqa: BLE001
            crashes.append("%s: %s" % (mid, exc))
            print("%-3s %-58s CRASH   [%s]" % (mid, desc, exc))
            snap.restore()
            continue
        _rc, failing = run_probe(probe_script)
        hit = want in failing
        if hit:
            caught += 1
        else:
            escapes.append("%s (wanted %s, got %s)"
                           % (mid, want, sorted(failing) or "nothing"))
        print("%-3s %-58s %s  [%s]"
              % (mid, desc, "CAUGHT " if hit else "ESCAPED", want))
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    # Summary dialect is the batch_e1..e6 form on purpose: oral_mutation.
    # parse_summary() already covers it, and inventing a new dialect is how a
    # harness ends up reporting green through a parser that never read it.
    print("\n%d caught of %d" % (caught, len(mutations)))
    print("%d mutations, %d escape(s), 0 no-op(s), %d crash(es)"
          % (len(mutations), len(escapes), len(crashes)))
    for line in escapes:
        print("  ESCAPE %s" % line)
    for line in crashes:
        print("  CRASH %s" % line)
    return 0 if (not escapes and not crashes) else 1
