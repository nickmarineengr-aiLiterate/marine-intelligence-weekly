#!/usr/bin/env python3
"""
Mutation suite for CORR-DEFN-TREATY-20260825.

WHAT THIS SUITE HAS TO PROVE
----------------------------
`validate_correction_defntreaty.py` reports a screen of green checks on the
corrected cards. Green output on its own is indistinguishable from a validator
that reads nothing. So every proposition this correction rests on is attacked
here, and each mutation must trip the check that OWNS that proposition.

A MUTATION THAT TRIPS THE DIGEST PIN IS NOT A CATCH
---------------------------------------------------
Every mutation below that edits a card also breaks
`card_digest_matches_manifest_q3` or `..._q6`, because the pin fires on any
byte change at all. Accepting that as the catch would prove only that the pin
works -- which was never in doubt -- while the substantive checks rotted as
dead code. So each mutation names the check it must break, and the required
check is NEVER the digest pin (SKILL section 8.2a, rule 1).

WHY SEVERAL MUTATIONS RE-INSERT WORDING THE CARD ALREADY CONTAINS
------------------------------------------------------------------
The corrected cards quote the formulations they reject -- "Never say 'Treaty
-> Convention -> Protocol'", "'a Protocol always requires ratification' is
wrong". The validator therefore asserts NEGATION, not absence. A mutation that
merely adds one more quoted mention would be caught by nothing and would
deserve to be. Each mutation below instead makes the card ASSERT the wrong
rule in its own voice, which is exactly the edit a future well-meaning session
would make.

MUTATION J IS THE HARNESS TESTING ITSELF
----------------------------------------
A mutation that changes no bytes exercises nothing while printing a reassuring
line. Two such mutations shipped in this repository before (E5's C, E6's H) and
one cost 22 minutes to find. The preflight below refuses to launch the suite if
any mutation is a no-op, and J is a deliberately inert mutation used to prove
the preflight itself is not asleep -- run with --selftest-noop.
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

MANIFEST = HERE / "correction_corr_defn_treaty_20260825_manifest.json"
CARD = REPO / "meoclass1/QB9_G.html"
SHEET = REPO / "meoclass1/QB9_G_CheatSheet.html"

PROBES = {
    "defntreaty": "validate_correction_defntreaty.py",
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
    """Byte-exact custody. Restores from what this object read, never from git:
    `git checkout <ref> -- <file>` destroys uncommitted work."""

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


def append_to_card(anchor: str, sentence: str):
    """Insert an ASSERTED sentence into a card's answer body, unquoted and
    unnegated -- the shape a real regression takes."""
    def apply():
        text = read_text(CARD)
        marker = '<div class="q-card" id="%s"' % anchor
        i = text.find(marker)
        assert i >= 0, "card %s not found" % anchor
        j = text.find("<h4>", i)
        assert j > i, "no h4 in card %s" % anchor
        write_text(CARD, text[:j] + "<p>" + sentence + "</p>\n      " + text[j:])
    return apply


def edit_manifest(mutate):
    def apply():
        data = json.loads(read_text(MANIFEST))
        mutate(data)
        write_text(MANIFEST, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return apply


def strip_review_record(d):
    for key in ("rationale", "note"):
        if key in d:
            d[key] = str(d[key]).replace("independent clean-context review", "look over")
    for c in d.get("cards", []):
        if "rationale" in c:
            c["rationale"] = c["rationale"].replace(
                "independent clean-context review", "look over").replace(
                "second independent review", "later look")


def taint_authority():
    """Swap a first-party citation for a secondary one. SKILL section 2a rule 2
    is only mechanically governable at the reg-box, which is where a card
    states where its law came from."""
    return sub_in(CARD,
                  '<span class="reg-code">UN Treaty Collection / Treaty Handbook</span>',
                  '<span class="reg-code">marineinsight.com treaty guide</span>')


# ----------------------------------------------------------------- mutations
# (id, description, files touched, apply(), probe, the check it MUST break)

MUTATIONS = [
    ("A", "assert the Treaty -> Convention -> Protocol hierarchy again",
     [CARD],
     append_to_card("q6", "In short, the ranking runs Treaty &rarr; Convention &rarr; "
                          "Protocol, and a Protocol sits at the bottom of that ladder."),
     "defntreaty", "no_hierarchy_asserted"),

    ("B", "reduce a Protocol to an amendment device",
     [CARD],
     append_to_card("q6", "For oral purposes a Protocol is only an amendment to its "
                          "parent Convention, a major structural add-on/update and "
                          "nothing more."),
     "defntreaty", "protocol_not_amendment_only"),

    ("C", "make ratification universal again",
     [CARD],
     append_to_card("q6", "Remember that a Protocol always requires ratification, "
                          "because every Protocol needs its own ratification before it "
                          "can bind a State."),
     "defntreaty", "protocol_ratification_not_universal"),

    ("D", "flatten an IMO Resolution back to guidance",
     [CARD],
     append_to_card("q6", "An IMO Resolution is committee guidance without independent "
                          "treaty force, and a resolution is always merely guidance."),
     "defntreaty", "resolution_effect_not_flattened"),

    ("E", "delete the VCLT foundation from the verified legal definition",
     [CARD],
     sub_in(CARD, "an international agreement concluded between States in written form "
                  "and governed by international law",
                  "an agreement between countries"),
     "defntreaty", "vclt_definition_quoted"),

    ("F", "leave the old hierarchy standing in the cheat sheet after the card is fixed",
     [SHEET],
     sub_in(SHEET, "Treaty = the legal category.",
                   "Treaty = umbrella legal term; the ranking is Treaty &rarr; "
                   "Convention &rarr; Protocol."),
     "defntreaty", "no_hierarchy_asserted"),

    ("G", "relabel the MIW memory line as an official definition",
     [CARD],
     sub_in(CARD, "memory line (this is MIW wording, not an official definition)",
                  "the official definition, in short"),
     "defntreaty", "miw_line_labelled_as_miw"),

    ("H", "replace the quoted UN Treaty Collection terminology with a paraphrase",
     [CARD],
     sub_in(CARD, "less formal than those entitled", "broadly similar to"),
     "defntreaty", "untc_terminology_quoted"),

    ("I", "strip the independent clean-context review from the correction record",
     [MANIFEST],
     edit_manifest(strip_review_record),
     "defntreaty", "independent_review_recorded"),

    ("J", "cite a secondary web source where first-party authority exists",
     [CARD],
     taint_authority(),
     "defntreaty", "authorities_are_first_party"),

    ("K", "re-close the consent list in q3's summary, leaving its body correct",
     [CARD],
     sub_in(CARD, "<strong>These four are not a closed list.</strong>", ""),
     "defntreaty", "q3_four_routes_not_closed"),

    ("L", "drop the operative designation qualifier from the VCLT quotation",
     [CARD],
     sub_in(CARD, "and whatever its particular designation", "and so on", 1),
     "defntreaty", "designation_qualifier_present"),
]

# A deliberately inert mutation, used only by --selftest-noop to prove the
# preflight actually detects a no-op rather than printing "applied" by habit.
NOOP = ("Z", "inert mutation (self-test of the preflight)", [CARD],
        sub_in(CARD, "Regulatory References", "Regulatory References"),
        "defntreaty", "no_hierarchy_asserted")


# ---------------------------------------------------------------------- main

def main() -> int:
    selftest = "--selftest-noop" in sys.argv
    suite = MUTATIONS + ([NOOP] if selftest else [])

    if not MANIFEST.is_file():
        print("correction record missing: %s" % MANIFEST.name)
        return 2

    print("--- preflight: every mutation must change bytes ---")
    no_ops = []
    for mid, desc, files, apply, _probe, _check in suite:
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
        print("%-3s %-62s %s" % (mid, desc, "applied" if changed else "NO-OP"))
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
        # Under --selftest-noop this is the CORRECT outcome: the harness has
        # proved it can see an inert mutation.
        return 0 if (selftest and no_ops == ["Z"]) else 1

    if selftest:
        print("\nSELFTEST FAILED -- the preflight did not notice the inert mutation Z")
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
    for mid, desc, files, apply, probe, want in suite:
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

    print("\n%d caught of %d" % (caught, len(suite)))
    print("%d mutations, %d escape(s), 0 no-op(s), %d crash(es)"
          % (len(suite), len(escapes), len(crashes)))
    for line in escapes:
        print("  ESCAPE %s" % line)
    return 0 if (not escapes and not crashes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
