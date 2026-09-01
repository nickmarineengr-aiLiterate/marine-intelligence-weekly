#!/usr/bin/env python3
"""Mutation suite for the H-series gate -- proves it is not decoration.

WHY A SUITE AT ALL
------------------
`H4-RES-01` is not "the H batches have no validator". It is "seven manifests
carry digest pins that nothing reads". Adding a file called
`validate_batch_h_series.py` does not close that; adding one whose every claim
is shown to FAIL when the thing it claims is broken does.

This repository has shipped a nominal guard before -- a half-wired digest pin,
a control that pinned a corpus total and passed vacuously once the corpus grew,
and two mutations (E5's C, E6's H) that matched nothing, wrote nothing and
exercised nothing for twenty-two minutes. So every mutation here must trip the
check that OWNS it, by name; tripping some other check does not count as caught.

WHAT IS ATTACKED
----------------
    delete a manifest              -> a missing H manifest must fail
    corrupt a post-edit digest     -> the pin must describe what actually shipped
    corrupt a pre-edit digest      -> the baseline claim must be true too
    rename an anchor               -> a card id that names nothing must fail
    repoint a card at another page -> a path that names nothing must fail
    make pre == post               -> an inert record pins nothing
    claim a second owner for one card -> overlapping primary ownership must show
    edit an undeclared card on a page the batch touched
                                   -> an EXTRA card must not ride along
    drop a name from the registry  -> an ungated manifest must not go quiet

THE LAST TWO ARE THE POINT
--------------------------
A digest pin only ever looks at the cards it names, so it is structurally blind
to a card smuggled onto a page the batch legitimately edited -- mutation H.
And a registry that can be trimmed would let a future H manifest become ungated
in silence, which is guard expiry in its dangerous direction: nothing goes red,
the guard simply stops describing the repository (SKILL section 7.5b). Mutation I
attacks that.

  PYTHONIOENCODING=utf-8 python tools/oral/mutate_batch_h_series.py

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
from oral_mutation import parse_summary                            # noqa: E402

enable_utf8_stdio()

VALIDATOR = HERE / "validate_batch_h_series.py"
REGISTRY = HERE / "test_oral_release_infra.py"

H1 = HERE / "batch_h1_manifest.json"
H2 = HERE / "batch_h2_manifest.json"
H4 = HERE / "batch_h4_manifest.json"


# --------------------------------------------------------------------- probe
def run_probe() -> tuple[int, set]:
    out = subprocess.run([sys.executable, str(VALIDATOR)],
                         cwd=str(REPO), capture_output=True, check=False)
    text = (out.stdout + out.stderr).decode("utf-8", "replace")
    return out.returncode, set(re.findall(r"^FAIL\s+(\S+)", text, re.M))


class Snapshot:
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


def _json(p):
    return json.loads(read_text(p))


def _write(p, data):
    write_text(p, json.dumps(data, indent=1, ensure_ascii=False) + "\n")


def edit(target, mutate):
    def apply():
        data = _json(target)
        mutate(data)
        _write(target, data)
    return apply


# ------------------------------------------------------------------ mutators
def m_corrupt_post_digest(d):
    d["cards"][0]["post_edit_digest"] = "0" * 64


def m_corrupt_pre_digest(d):
    d["cards"][0]["pre_edit_digest"] = "0" * 64


def m_falsify_real_pre_digest(d):
    """H4-004 is the CURRENCY_EXPANSION of QB5_E#q4 -- one of only two cards in
    the whole series with a genuine baseline state. This attacks the equality
    direction; mutation B attacks the absence direction."""
    for card in d["cards"]:
        if card.get("pre_edit_digest"):
            card["pre_edit_digest"] = "1" * 64
            return
    raise AssertionError("no card with a real pre-edit digest")


def m_rename_anchor(d):
    d["cards"][0]["anchor"] = "q9999"


def m_repoint_file(d):
    d["cards"][0]["file"] = "QB10_B.html"


def m_repoint_to_nothing(d):
    d["cards"][0]["file"] = "QB_NO_SUCH_PAGE.html"


def m_inert_card(d):
    d["cards"][0]["pre_edit_digest"] = d["cards"][0]["post_edit_digest"]


def m_claim_another_batchs_card(d):
    """H2 claims primary ownership of a card H1 already owns.

    Two records pinning one card is not a harmless duplicate: it makes
    "which batch is answerable for this card?" unanswerable from repository
    data, which is the question every later correction has to ask.
    """
    victim = _json(H1)["cards"][0]
    stolen = dict(d["cards"][0])
    stolen["action_id"] = stolen["action_id"] + "-DUPE"
    stolen["file"] = victim["file"]
    stolen["anchor"] = victim["anchor"]
    stolen["pre_edit_digest"] = victim["pre_edit_digest"]
    stolen["post_edit_digest"] = victim["post_edit_digest"]
    d["cards"].append(stolen)


def m_delete_manifest():
    H2.unlink()


def m_drop_from_registry():
    text = read_text(REGISTRY)
    old = '    "batch_h2_manifest.json",\n'
    assert old in text, "registry line absent"
    write_text(REGISTRY, text.replace(old, "", 1))


def m_smuggle_an_undeclared_card():
    """Edit a card the H series did NOT declare, on a page it DID touch.

    H2, H3B-1 and H3B-2 all edited QB1_F. Every digest pin is perfectly happy
    about a change to QB1_F#q1, because no pin names it. Only the
    baseline comparison sees it.
    """
    page = MEO / "QB1_F.html"
    text = read_text(page)
    # q5 is declared by NO record anywhere, so no delegation can excuse
    # it. Aiming at q1 -- which batch A legitimately owns -- proved only
    # that delegation works, which is a different property.
    marker = '<div class="q-card" id="q5"'
    assert marker in text, "mutation target absent"
    i = text.index(marker)
    j = text.index(">", i) + 1
    write_text(page, text[:j] + "<!-- smuggled -->" + text[j:])


# (id, description, files touched, apply(), the check it MUST break)
MUTATIONS = [
    ("A", "corrupt a post-edit digest - the pin misdescribes what shipped",
     [H1], edit(H1, m_corrupt_post_digest),
     "batch_h1/H1-001:manifest_digest_matches"),

    ("B", "declare a pre-edit state for a card that did not exist at baseline",
     [H1], edit(H1, m_corrupt_pre_digest),
     "batch_h1/H1-001:pre_edit_state_is_as_declared"),

    ("B2", "falsify the pre-edit digest of a card that DID exist at baseline",
     [H4], edit(H4, m_falsify_real_pre_digest),
     "batch_h4/H4-004:pre_edit_state_is_as_declared"),

    ("C", "rename an anchor to a card that does not exist",
     [H2], edit(H2, m_rename_anchor),
     "batch_h2/H2-001:card_anchor_exists"),

    ("D", "repoint a card at a page it was never on",
     [H2], edit(H2, m_repoint_file),
     "batch_h2/H2-001:card_anchor_exists"),

    ("D2", "repoint a card at a page that does not exist at all",
     [H2], edit(H2, m_repoint_to_nothing),
     "batch_h2/H2-001:card_path_exists"),

    ("E", "make pre == post so the record pins nothing",
     [H4], edit(H4, m_inert_card),
     "batch_h4/H4-001:card_digests_differ"),

    ("F", "let two H manifests claim primary ownership of one card",
     [H2], edit(H2, m_claim_another_batchs_card),
     "h_series_no_overlapping_primary_ownership"),

    ("G", "delete an H manifest entirely",
     [H2], m_delete_manifest,
     "h_manifests_all_present"),

    ("H", "smuggle an undeclared card edit onto a page the batch touched",
     [MEO / "QB1_F.html"], m_smuggle_an_undeclared_card,
     "batch_h3b2_manifest.json:only_authorised_cards_changed"),

    ("I", "quietly drop an H manifest from the registry so it becomes ungated",
     [REGISTRY], m_drop_from_registry,
     "h_manifests_none_undeclared"),
]


def main() -> int:
    if not VALIDATOR.is_file():
        print("H-series validator missing")
        return 2

    # ---- preflight: a mutation that changes no bytes exercises nothing -----
    # A mutation must change CONTENT, not merely size. Mutation A replaces a
    # 64-character digest with 64 zeros: the byte_delta is exactly 0 and the
    # file is completely different. A size-only preflight would have called
    # the strongest probe in this suite a no-op and refused to launch.
    print("--- preflight: every mutation must change content ---")
    no_ops = []
    for mid, desc, paths, apply, _req in MUTATIONS:
        snap = Snapshot(paths)
        before = dict(snap.data)
        pre_size = sum(len(b or b"") for b in before.values())
        try:
            apply()
        except Exception as exc:
            print("%-3s ERROR %s: %s" % (mid, type(exc).__name__, exc))
            snap.restore()
            no_ops.append(mid)
            continue
        after = {q: (q.read_bytes() if q.is_file() else None) for q in snap.data}
        post_size = sum(len(b or b"") for b in after.values())
        changed = after != before
        print("%-3s %-56s changed=%-5s byte_delta=%+d"
              % (mid, desc[:56], changed, post_size - pre_size))
        if not changed:
            no_ops.append(mid)
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2
    if no_ops:
        print("\npreflight FAILED -- these mutations change no content: %s"
              % ", ".join(no_ops))
        print("0 mutations, 0 escape(s), %d no-op(s), 0 crash(es)" % len(no_ops))
        return 1

    # ---- control ----------------------------------------------------------
    print("\n--- control: unmutated state ---")
    rc, failing = run_probe()
    print("CTL h_series  exit=%d failing=%s" % (rc, sorted(failing) or "none"))
    if failing:
        # Section 7.4a: the precondition is "no NEW failures". This gate is
        # new, so its baseline is empty and that reduces to "green".
        print("CONTROL IS NOT GREEN -- every later 'catch' would be meaningless")
        return 2

    # ---- mutations --------------------------------------------------------
    print("\n--- mutations ---")
    caught, escapes = 0, []
    crashes = 0
    for mid, desc, paths, apply, required in MUTATIONS:
        snap = Snapshot(paths)
        try:
            apply()
        except Exception as exc:
            print("%-3s CRASH  %s: %s" % (mid, type(exc).__name__, exc))
            snap.restore()
            crashes += 1
            continue
        rc, failing = run_probe()
        # The named check must be the one that broke. A mutation caught only
        # because some unrelated digest moved has not proved its guard.
        hit = required in failing
        if hit:
            caught += 1
        else:
            escapes.append("%s: %s (wanted %r, got %s)"
                           % (mid, desc, required, sorted(failing) or "none"))
        print("%-3s %-62s %s  [%s]"
              % (mid, desc[:62], "caught" if hit else "ESCAPED", required))
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    # ---- residue ----------------------------------------------------------
    print("\n--- residue probe ---")
    rc, failing = run_probe()
    print("RES h_series  exit=%d failing=%s" % (rc, sorted(failing) or "none"))

    print("\n%d caught of %d" % (caught, len(MUTATIONS)))
    print("%d mutations, %d escape(s), 0 no-op(s), %d crash(es)"
          % (len(MUTATIONS), len(escapes), crashes))
    for line in escapes:
        print("  ESCAPE %s" % line)
    if failing:
        print("  RESIDUE: the probe is still red after restore")
    return 0 if (not escapes and not crashes and not failing) else 1


if __name__ == "__main__":
    raise SystemExit(main())
