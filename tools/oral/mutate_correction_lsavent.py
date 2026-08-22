#!/usr/bin/env python3
"""
Mutation suite for CORR-LSA-LIFEBOAT-VENTILATION-20260822.

WHAT THIS SUITE HAS TO PROVE
----------------------------
`validate_correction_lsavent.py` reports 22 green checks on the corrected
card. Green output on its own is indistinguishable from a validator that
reads nothing. So every proposition the correction rests on is attacked here,
and each mutation must trip the check that owns that proposition.

A MUTATION THAT TRIPS THE DIGEST PIN IS NOT A CATCH
---------------------------------------------------
This is the whole difficulty of testing a content correction. Every mutation
below that edits the card also breaks `card_digest_matches_manifest`, because
the pin fires on any byte change at all. If the suite accepted that as the
catch, it would prove only that the pin works -- which was never in doubt --
while the substantive checks could all be dead code.

So each mutation names the check it must break, and the required check is
never the digest pin. A mutation whose named check stays green is an ESCAPE
even when the probe exits non-zero. Same rule E6's mutation L was written to
enforce, applied to content rather than to schema.

MUTATION H, AND WHY IT IS NOT A SUPERSESSION TEST
-------------------------------------------------
No production batch pins QB2_F#q6, so this correction has no historical
digest chain to break, and a mutation that "breaks supersession continuity"
here would be theatre. What CAN be tested is the assertion that stands in for
it: `no_batch_pins_this_card`. H injects a QB2_F pin into a batch manifest
and requires that check to go red -- proving that if a future batch ever does
pin this card, the correction is forced to grow a chain rather than silently
overwrite that batch's release evidence.
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

MANIFEST = HERE / "correction_corr_lsa_lifeboat_ventilation_20260822_manifest.json"
GOVERNED = HERE / "qb_content_index_governed.json"
INDEX = REPO / "meoclass1/qb_content_index.json"
CARD = REPO / "meoclass1/QB2_F.html"
BATCH = HERE / "batch_a_manifest.json"

PROBES = {
    "lsavent": "validate_correction_lsavent.py",
    "corrections": "validate_corrections.py",
}


def run_probe(key: str) -> tuple[int, set]:
    """Run one validator; return (exit code, set of FAILing check names)."""
    out = subprocess.run([sys.executable, str(HERE / PROBES[key])],
                         cwd=str(REPO), capture_output=True, check=False)
    text = (out.stdout + out.stderr).decode("utf-8", "replace")
    failing = set(re.findall(r"^FAIL\s+(\S+)", text, re.M))
    # validate_corrections rolls its schema audit into one aggregate check and
    # names the violated sub-checks in `violations=[...]`. Lift them out, so a
    # schema mutation cannot be satisfied by the aggregate name alone.
    for payload in re.findall(r"violations=\[([^\]]*)\]", text):
        failing.update(re.findall(r"'([^']+)'", payload))
    return out.returncode, failing


class Snapshot:
    """Byte-exact custody of every file a mutation touches.

    Restores from what this object personally read, never from git:
    `git checkout <ref> -- <file>` destroys uncommitted work, which has
    already cost real edits in this repository.
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


# ------------------------------------------------------------------ helpers

def sub_in_card(old: str, new: str, count: int = 0):
    """Replace text in the live card, asserting the target actually exists."""
    def apply():
        text = read_text(CARD)
        assert old in text, "mutation target absent from card: %r" % old[:60]
        write_text(CARD, text.replace(old, new) if count == 0
                   else text.replace(old, new, count))
    return apply


def edit_manifest(mutate):
    def apply():
        data = json.loads(read_text(MANIFEST))
        mutate(data)
        write_text(MANIFEST, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return apply


def edit_governed(mutate):
    def apply():
        data = json.loads(read_text(GOVERNED))
        mutate(data)
        write_text(GOVERNED, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        subprocess.run([sys.executable, str(HERE / "build_qb_content_index.py")],
                       cwd=str(REPO), capture_output=True, check=False)
    return apply


def pin_qb2f_into_batch():
    def apply():
        data = json.loads(read_text(BATCH))
        data.setdefault("cards", []).append({
            "action_id": "MUTATION-PIN",
            "file": "QB2_F.html",
            "path": "meoclass1/QB2_F.html",
            "anchor": "q6",
        })
        write_text(BATCH, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return apply


def strip_primary_authority(d):
    for key in ("rationale", "note", "title"):
        if key in d:
            d[key] = str(d[key]).replace("MSC.535(107)", "the amendment") \
                                .replace("8 June 2023", "2023")


# ----------------------------------------------------------------- mutations
# (id, description, files touched, apply(), probe, the check it MUST break)

MUTATIONS = [
    ("A", "restore the wrong 2026 application date",
     [CARD],
     sub_in_card("applied to totally enclosed lifeboats installed on or after "
                 "1 January 2029</strong>",
                 "applied to totally enclosed lifeboats installed on or after "
                 "1 January 2026</strong>"),
     "lsavent", "no_application_in_2026"),

    ("B", "move the application year from 2029 back to 2026 everywhere",
     [CARD],
     sub_in_card("1 January 2029", "1 January 2026"),
     "lsavent", "application_year_is_2029"),

    ("C", "delete the entry-into-force / application separation sentence",
     [CARD],
     sub_in_card(" Entry into force is not the application date.", ""),
     "lsavent", "force_and_application_distinguished"),

    ("D", "corrupt the correction record's identity",
     [MANIFEST],
     edit_manifest(lambda d: d.__setitem__("correction_id", "CORR-SOMETHING-ELSE")),
     "lsavent", "correction_record_authorised"),

    ("E", "corrupt the declared pre-edit digest",
     [MANIFEST],
     edit_manifest(lambda d: d["cards"][0].__setitem__("pre_edit_digest", "0" * 64)),
     "corrections", "pre_edit_digests_match_baseline"),

    ("F", "corrupt the declared post-edit digest",
     [MANIFEST],
     edit_manifest(lambda d: d["cards"][0].__setitem__("post_edit_digest", "0" * 64)),
     "lsavent", "card_digest_matches_manifest"),

    ("G", "change an undeclared card on the same page",
     [CARD],
     sub_in_card('<div class="q-card" id="q5"',
                 '<div class="q-card" id="q5"><!--mutation-probe-->', 1),
     "corrections", "no_undeclared_change_in_window"),

    ("H", "let a production batch pin this card without a supersession chain",
     [BATCH],
     pin_qb2f_into_batch(),
     "lsavent", "no_batch_pins_this_card"),

    ("I", "remove the primary authority from the record",
     [MANIFEST],
     edit_manifest(strip_primary_authority),
     "lsavent", "primary_authority_recorded"),

    ("J", "reintroduce the keel-laid application test",
     [CARD],
     sub_in_card("<strong>building contract is placed</strong> on or after "
                 "1 January 2029",
                 "building contract is dated, or keel-laid on or after "
                 "1 January 2029"),
     "lsavent", "no_keel_laid_application_test"),

    ("K", "drop limb (b) -- the limb whose loss inverted the rule",
     [CARD],
     sub_in_card("<li><strong>(b) All other ships:</strong>", "<li><!--dropped-->"),
     "lsavent", "definition_limb_b_present"),

    ("L", "assert new-build-only again, undenied",
     [CARD],
     sub_in_card("So this is <strong>not a new-build-only requirement</strong>.",
                 "So this is a new-builds only requirement."),
     "lsavent", "newbuild_only_always_negated"),

    ("M", "gut a verified technical figure",
     [CARD],
     sub_in_card("5 m&sup3;/h per person", "some air per person"),
     "lsavent", "technical_capsule_intact"),

    ("N", "reword the canonical question text",
     [CARD],
     sub_in_card("What are the ventilation requirements for a totally enclosed "
                 "lifeboat?",
                 "What about lifeboat ventilation?"),
     "lsavent", "question_text_unchanged"),

    ("O", "put the stale new-build-only claim back in the content index",
     [GOVERNED, INDEX],
     edit_governed(lambda d: d["files"]["QB2_F.html"]["corrections_applied"].append(
         "Q6 application date 1 Jan 2029 (new-build only).")),
     "lsavent", "content_index_records_correction"),
]


# ---------------------------------------------------------------------- main

def main() -> int:
    if not MANIFEST.is_file():
        print("correction record missing: %s" % MANIFEST.name)
        return 2

    # ---- preflight: every mutation must really change bytes ---------------
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
        print("%-3s %-58s %s" % (mid, desc, "applied" if changed else "NO-OP"))
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

    # ---- control: unmutated, both probes must be green --------------------
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

    # ---- the suite --------------------------------------------------------
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
        print("%-3s %-58s %s  [%s]"
              % (mid, desc, "CAUGHT " if hit else "ESCAPED", want))
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    # The content index is regenerated by mutation O; make sure the restored
    # governed source and the generated twin are back in agreement on disk.
    subprocess.run([sys.executable, str(HERE / "build_qb_content_index.py")],
                   cwd=str(REPO), capture_output=True, check=False)

    # Summary dialect is the batch_e1..e6 form on purpose: oral_mutation.
    # parse_summary() already covers it, and inventing a seventh dialect is how
    # a harness ends up reporting green through a parser that never read it.
    print("\n%d caught of %d" % (caught, len(MUTATIONS)))
    print("%d mutations, %d escape(s), 0 no-op(s), %d crash(es)"
          % (len(MUTATIONS), len(escapes), len(crashes)))
    for line in escapes:
        print("  ESCAPE %s" % line)
    return 0 if (not escapes and not crashes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
