#!/usr/bin/env python3
"""Controls for validate_batch_e1's supersession-aware timed-blocks check.

`timed_blocks_unchanged` asserts that E1's enrichment never touched a card's 15-/60-second answer blocks. Once a later
authorised record supersedes an E1 card, the check reads E1's own produced state (recovered from history by its pinned
digest) instead of the live card. These controls prove the check still bites:

  A  the live candidate passes;
  B  an unauthorised timed-block edit on an E1 card that is NOT superseded fails (the original comparison);
  C  a superseded card whose E1 state cannot be found in history fails (never silently skipped);
  D  a superseded card whose E1 produced state did change a timed block fails;
  E  the superseded path is actually exercised for QB1_F#q1 (non-vacuity).

B edits a live page and restores it byte-for-byte (verified). Prints "<N> checks, <M> FAIL".
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from oral_bytes import read_text, write_text  # noqa: E402
import validate_batch_e1 as V  # noqa: E402

TIMED = re.compile(r'(<div class="(?:practice-block|oral-box)[^"]*"[^>]*>)(.*?)(</div>)', re.S)
_checks, _failed = 0, []


def report(name, ok, detail=""):
    global _checks
    _checks += 1
    print("%-5s %-58s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        _failed.append(name)


def run_e1():
    V._checks, V._fails = 0, []
    with contextlib.redirect_stdout(io.StringIO()):
        V.main()
    return list(V._fails)


@contextlib.contextmanager
def patched(name, fn):
    orig = getattr(V, name)
    setattr(V, name, fn)
    try:
        yield
    finally:
        setattr(V, name, orig)


def main() -> int:
    report("A_live_candidate_passes", "timed_blocks_unchanged" not in run_e1())

    page = V.QB_DIR / "QB1_B.html"
    before = read_text(page)
    digest = hashlib.sha256(before.encode("utf-8")).hexdigest()
    try:
        card = V.cards_of(before)["q1"]
        m = TIMED.search(card)
        assert m, "QB1_B#q1 has no timed block"
        start = before.index(card) + m.start(2)
        write_text(page, before[:start] + "UNAUTHORISED " + before[start:])
        report("B_unauthorised_timed_edit_on_live_e1_card_fails", "timed_blocks_unchanged" in run_e1())
    finally:
        write_text(page, before)
    report("B_restore_verified", hashlib.sha256(read_text(page).encode("utf-8")).hexdigest() == digest)

    with patched("e1_produced_card", lambda f, a, d: None):
        report("C_superseded_card_without_e1_state_fails", "timed_blocks_unchanged" in run_e1())

    real = V.e1_produced_card

    def altered(f, a, d):
        txt = real(f, a, d)
        return TIMED.sub(lambda m: m.group(1) + "CHANGED BY E1 " + m.group(2) + m.group(3), txt, count=1) \
            if (f, a) == ("QB1_F.html", "q1") and txt else txt
    with patched("e1_produced_card", altered):
        report("D_e1_state_with_changed_timed_block_fails", "timed_blocks_unchanged" in run_e1())

    calls = []

    def spy(f, a, d):
        calls.append("%s#%s" % (f, a))
        return real(f, a, d)
    with patched("e1_produced_card", spy):
        run_e1()
    report("E_superseded_path_exercised_for_QB1_F_q1", "QB1_F.html#q1" in calls, str(calls))

    print("\n%d checks, %d FAIL" % (_checks, len(_failed)))
    return 1 if _failed else 0


if __name__ == "__main__":
    sys.exit(main())
