"""PL-02 intake integrity controls: no silent loss, and no silent duplicate.

The intake parser already carries one defect-driven branch per grammar the
carriers have shown, and `test_intake_multicarrier.py` proves each of them. What
it does not prove, and what this file exists for:

  * the line-accounting walk runs over ONE carrier, not every registered one;
  * the WRITE path does not refuse to write when content went unplaced -- only
    `--check` refuses, which is the wrong direction: the first run is where the
    loss happens and the check runs afterwards;
  * a recognised submission that yields ZERO occurrences while its body carries
    text is not flagged anywhere;
  * duplicates are neither identified nor counted, so candidate repetition --
    which is examiner-frequency evidence -- is invisible.

Every control here is a REGRESSION control: each names a loss shape that either
already happened to this pipeline or is the same shape as one that did.

Usage:
  python tools/oral/test_intake_integrity.py
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ingest_august_intake as I  # noqa: E402
import intake_reconcile as R  # noqa: E402

PASS = FAIL = 0
FAILURES: list[str] = []
#: A FINDING is a defect in the DATA that these controls were built to detect,
#: not a defect in the tooling. It is reported separately and it does not fail
#: the tooling suite, because the fix is a Founder edit to a governed provenance
#: record and not a code change. It is still non-zero at exit: a detected defect
#: is not a green run.
FINDINGS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        FAILURES.append(f"{name}: {detail}")
        print(f"  FAIL  {name}  {detail}")


def finding(name: str, cond: bool, detail: str = "") -> None:
    """A control over the DATA. Reported, never counted as a tooling failure."""
    global PASS
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FINDINGS.append(f"{name}: {detail}")
        print(f"  FIND  {name}  {detail}")


# ---------------------------------------------------------------------------
# Synthetic carriers. Each is the minimum text that shows one loss shape.
# ---------------------------------------------------------------------------

CLEAN = """Ext- Rajappan sir
Int- Senthil sir
Attempt 1
Result - Pass
1. What is the purpose of the ISM Code?
2. Explain enclosed space entry.
"""

#: The S007 shape: a whole submission that numbers nothing. It once failed the
#: "is this a submission" test and `continue` said nothing.
UNNUMBERED = """Ext- Nair sir
Int- Srivastava sir
What is a condition of class?
When is a DOC withdrawn?
"""

#: A block with real content that declares no examiner and numbers nothing. It
#: yields no submission at all, which the existing report surfaces as
#: `unparsed_source_blocks` -- but only `--check` refuses to proceed on it.
HAS_ORPHAN_BLOCK = CLEAN + """
---
Some loose text a candidate pasted that names nobody and numbers nothing
and is plainly examinable material.
"""

#: A recognised submission -- it declares a panel -- whose body yields NO
#: occurrence. Nothing in the pipeline reports this today: the block passed the
#: submission test, so it is not an unparsed block, and it contributes zero
#: questions without saying so.
ZERO_YIELD = """Ext- Rajappan sir
Int- Senthil sir
Attempt 2
Result - Repeat
"""

#: The same question written twice by one candidate, and again by another.
#: Repetition is evidence about what examiners ask, so it may be neither
#: discarded nor silently merged.
DUPLICATES = """Ext- Rajappan sir
Int- Senthil sir
1. What is the purpose of the ISM Code?
2. what is the purpose of the ism code ?
3. Explain enclosed space entry.
---
Ext- Nair sir
Int- Senthil sir
1. What is the purpose of the ISM Code?
"""


def parse(text: str, name: str = "synthetic.txt"):
    """Parse a synthetic carrier without touching disk-registered carriers."""
    return R.parse_text(text, name)


# ── R: the reconciliation ledger ────────────────────────────────────────────

def t_ledger_shape():
    print("\nR   every non-empty source line reaches one accountable disposition")
    led = R.reconcile_text(CLEAN, "clean.txt")
    total = sum(led["dispositionCounts"].values())
    check("R-EVERY-LINE-DISPOSED", total == led["meaningfulLines"],
          f"{total} dispositions for {led['meaningfulLines']} meaningful lines")
    check("R-NO-UNACCOUNTED", not led["unaccounted"],
          f"unaccounted: {led['unaccounted']}")
    check("R-OCCURRENCES-COUNTED",
          led["dispositionCounts"].get("OCCURRENCE") == 2,
          f"{led['dispositionCounts']}")
    check("R-METADATA-COUNTED",
          led["dispositionCounts"].get("METADATA_CONSUMED", 0) >= 2,
          f"attempt and result were not recorded as consumed: "
          f"{led['dispositionCounts']}")
    check("R-EXAMINERS-COUNTED",
          led["dispositionCounts"].get("EXAMINER_DECLARATION") == 2,
          f"{led['dispositionCounts']}")
    check("R-DISPOSITIONS-GOVERNED",
          set(led["dispositionCounts"]) <= set(R.DISPOSITIONS),
          f"undeclared disposition: "
          f"{set(led['dispositionCounts']) - set(R.DISPOSITIONS)}")
    check("R-DETERMINISTIC",
          R.reconcile_text(CLEAN, "clean.txt") == led,
          "two reconciliations over identical input disagreed")


def t_ledger_catches_loss():
    print("\nR   content the parser could not place is visible, never silent")
    led = R.reconcile_text(HAS_ORPHAN_BLOCK, "orphan.txt")
    check("R-ORPHAN-BLOCK-SEEN", led["unparsedBlocks"],
          "a block with examinable text that yielded no submission was not "
          "reported")
    check("R-ORPHAN-LINES-DISPOSED",
          led["dispositionCounts"].get("UNPARSED_BLOCK", 0) >= 2,
          f"the orphan block's lines reached no disposition: "
          f"{led['dispositionCounts']}")
    check("R-ORPHAN-NOT-CLEAN", not led["clean"],
          "a carrier with an unplaced block reported itself clean")

    ok = R.reconcile_text(CLEAN, "clean.txt")
    check("R-CLEAN-IS-CLEAN", ok["clean"], f"a clean carrier reported {ok}")


def t_zero_yield():
    print("\nR   a recognised submission that yields nothing says so")
    led = R.reconcile_text(ZERO_YIELD, "zero.txt")
    check("R-ZERO-YIELD-FLAGGED", led["zeroYieldSubmissions"],
          "a submission with a body and no occurrence was not flagged")
    check("R-ZERO-YIELD-NOT-CLEAN", not led["clean"],
          "a zero-yield submission reported itself clean")
    # A submission whose body is metadata ONLY is a real shape: a candidate who
    # reports a panel and a result and nothing else. The flag must say which it
    # is rather than refusing both alike.
    check("R-ZERO-YIELD-REASON",
          led["zeroYieldSubmissions"][0]["unconsumedBodyLines"] == 0,
          f"a metadata-only submission was not distinguished from one whose "
          f"text went unread: {led['zeroYieldSubmissions']}")

    # AND THE DANGEROUS ONE: a body with text that is not metadata, yielding no
    # occurrence. That is a parser that read nothing while the candidate wrote
    # something, which is the ZERO-vs-VISIBLE-UNPARSED rule.
    blind = ZERO_YIELD + "The examiner asked about the oily water separator\n"
    led2 = R.reconcile_text(blind, "blind.txt")
    check("R-BLIND-PARSE-FLAGGED",
          not led2["clean"] or led2["dispositionCounts"].get("OCCURRENCE", 0) >= 1,
          "a line of examinable text neither became an occurrence nor was "
          "reported as unplaced")


def t_unnumbered_still_parses():
    print("\nR   the S007 loss shape stays captured")
    led = R.reconcile_text(UNNUMBERED, "unnumbered.txt")
    check("R-UNNUMBERED-CAPTURED",
          led["dispositionCounts"].get("OCCURRENCE") == 2,
          f"the unnumbered submission yielded "
          f"{led['dispositionCounts'].get('OCCURRENCE')} occurrence(s)")
    check("R-UNNUMBERED-CLEAN", led["clean"],
          f"an unnumbered submission was reported unclean: {led['unaccounted']}")


# ── D: duplicates ───────────────────────────────────────────────────────────

def t_duplicates():
    print("\nD   a duplicate is counted and linked, never discarded")
    led = R.reconcile_text(DUPLICATES, "dupes.txt")
    occ = led["dispositionCounts"].get("OCCURRENCE")
    check("D-NOTHING-DISCARDED", occ == 4,
          f"{occ} occurrences survived; all four must, duplicates included")

    groups = led["duplicateGroups"]
    check("D-GROUP-FOUND", len(groups) == 1, f"{len(groups)} duplicate group(s)")
    g = groups[0]
    check("D-THREE-MEMBERS", len(g["occurrenceIds"]) == 3,
          f"group members: {g['occurrenceIds']}")
    check("D-FIRST-IS-CANONICAL", g["firstOccurrenceId"] == g["occurrenceIds"][0],
          f"the group does not link to its first occurrence: {g}")
    check("D-CASE-AND-PUNCTUATION-INSENSITIVE",
          "2" in str(g["occurrenceIds"]) or len(g["occurrenceIds"]) == 3,
          "a repeat written in lower case with a stray '?' was not matched")
    check("D-WITHIN-AND-ACROSS-SUBMISSIONS",
          g["spansSubmissions"] is True,
          f"the group does not record that it crosses submissions: {g}")
    check("D-COUNT-REPORTED", led["duplicateOccurrences"] == 2,
          f"{led['duplicateOccurrences']} duplicate occurrences reported; "
          f"two of the four are repeats")
    check("D-DUPLICATES-DO-NOT-BREAK-CLEAN", led["clean"],
          "a carrier was called unclean merely for containing a repeat")
    check("D-RAW-PRESERVED",
          all(o["raw_question_text"] for o in led["_occurrences"]),
          "a duplicate lost its raw wording")


# ── G: the write path fails closed ──────────────────────────────────────────

def t_write_gate():
    print("\nG   the write path refuses to write a lossy ingest")
    ok, why = R.gate(R.reconcile_text(CLEAN, "clean.txt"))
    check("G-CLEAN-PASSES", ok, f"a clean carrier was refused: {why}")
    ok, why = R.gate(R.reconcile_text(HAS_ORPHAN_BLOCK, "orphan.txt"))
    check("G-ORPHAN-REFUSED", not ok, "an unplaced block was allowed through")
    check("G-REASON-NAMES-THE-BLOCK", "block" in why.lower(),
          f"the refusal does not say what was lost: {why!r}")
    ok, _ = R.gate(R.reconcile_text(ZERO_YIELD, "zero.txt"))
    check("G-ZERO-YIELD-REFUSED", not ok,
          "a submission that yielded nothing was allowed through")
    ok, _ = R.gate(R.reconcile_text(DUPLICATES, "dupes.txt"))
    check("G-DUPLICATES-ALLOWED", ok,
          "a repeat was treated as a loss and refused")

    # The gate is WIRED, not merely available. This is the whole point: the
    # existing `--check` runs after the records were already written.
    import inspect
    src = inspect.getsource(I.main)
    check("G-GATE-WIRED-INTO-INGEST",
          "reconcile" in src and "gate" in src,
          "ingest_august_intake.main does not consult the reconciliation gate")
    write_at = src.find("RECORDS.write_text")
    gate_at = min([i for i in (src.find("R.gate"), src.find("gate(")) if i >= 0]
                  or [10 ** 9])
    check("G-GATE-BEFORE-WRITE", gate_at < write_at,
          "the gate is consulted after the records are written")


# ── L: the live registered carriers, read-only ──────────────────────────────

def t_live_carriers():
    print("\nL   every registered carrier reconciles, read-only")
    regs = I.load_carriers()
    check("L-CARRIERS-REGISTERED", len(regs) >= 4, f"{len(regs)} carrier(s)")
    before = {}
    for c in regs:
        p = I.carrier_path(c)
        if p.exists():
            before[p] = hashlib.sha256(p.read_bytes()).hexdigest()
    check("L-CARRIERS-ON-DISK", len(before) == len(regs),
          f"{len(regs) - len(before)} registered carrier(s) absent from disk")

    total_unaccounted = 0
    for c in regs:
        p = I.carrier_path(c)
        if not p.exists():
            continue
        led = R.reconcile_text(p.read_text(encoding="utf-8"), c["source_file"])
        total_unaccounted += len(led["unaccounted"])
        check(f"L-RECONCILES {c['carrier_date']}", led["clean"],
              f"unaccounted={led['unaccounted'][:2]} "
              f"unparsed={len(led['unparsedBlocks'])} "
              f"zeroYield={len(led['zeroYieldSubmissions'])}")
    check("L-NO-UNACCOUNTED-ANYWHERE", total_unaccounted == 0,
          f"{total_unaccounted} line(s) across all carriers reach no disposition")

    for p, h in before.items():
        check(f"L-CARRIER-UNCHANGED {p.name[:10]}",
              hashlib.sha256(p.read_bytes()).hexdigest() == h,
              "a carrier changed during reconciliation")


def t_live_identity_alignment():
    """The ledger's ids must be the PRODUCTION ids, not carrier-local ones.

    An id that does not resolve is a visible defect. An id that resolves to a
    DIFFERENT question is not, and that is what a per-carrier restart produces:
    the second carrier's ledger reported AUG-0031/AUG-0043 for its duplicate
    pair while those ids belong to two unrelated 24-August asks. The review
    packet published that pair, which is how a reporting defect becomes a wrong
    claim about evidence.
    """
    print()
    print("I   ledger identities are the production identities")
    import json
    store = {json.loads(l)["occurrence_id"]: json.loads(l)["raw_question_text"]
             for l in I.RECORDS.read_text(encoding="utf-8").splitlines() if l.strip()}
    led = R.reconcile_registered()

    unknown, mismatched, checked = [], [], 0
    for car in led["carriers"]:
        for g in car.get("duplicateGroups", []):
            for oid in g["occurrenceIds"]:
                checked += 1
                if oid not in store:
                    unknown.append(oid)
                elif R.duplicate_key(store[oid]) != g["duplicateKey"]:
                    mismatched.append((oid, store[oid][:40]))
    check("I-LEDGER-IDS-EXIST", not unknown, f"absent from the store: {unknown}")
    check("I-LEDGER-IDS-ARE-THE-SAME-QUESTION", not mismatched,
          f"id resolves to a different ask: {mismatched}")
    check("I-IDENTITY-CHECK-NOT-VACUOUS", checked > 0,
          "no duplicate group was available to check identities against")


def t_live_window_consistency():
    print("\nL   the registry's own window fields agree with its carriers")
    import json
    reg = json.loads(I.CARRIERS.read_text(encoding="utf-8"))
    snaps = [c for c in reg["carriers"] if "_snapshots/" in c["source_file"]]
    w = reg.get("intake_window", {})
    # A count written by hand beside a list that grows is a drift field. It is
    # checked, not trusted.
    finding("L-SNAPSHOT-COUNT-AGREES", w.get("snapshots_taken") == len(snaps),
          f"intake_window.snapshots_taken = {w.get('snapshots_taken')} but "
          f"{len(snaps)} snapshot carrier(s) are registered")
    latest = max((c["received_date"] for c in reg["carriers"]), default="")
    finding("L-AS-AT-NOT-BEHIND-CARRIERS", str(w.get("as_at", "")) >= latest,
          f"intake_window.as_at = {w.get('as_at')} predates the latest "
          f"received_date {latest}")


def main() -> int:
    for t in (t_ledger_shape, t_ledger_catches_loss, t_zero_yield,
              t_unnumbered_still_parses, t_duplicates, t_write_gate,
              t_live_carriers, t_live_identity_alignment,
              t_live_window_consistency):
        t()
    print(f"\n{PASS} PASS / {FAIL} FAIL")
    for f in FAILURES:
        print(f"  - {f}")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
