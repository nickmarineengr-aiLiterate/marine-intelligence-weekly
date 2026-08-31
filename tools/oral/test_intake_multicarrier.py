#!/usr/bin/env python3
"""Stage 0 controls for the multi-carrier August Oral intake.

    PYTHONIOENCODING=utf-8 python tools/oral/test_intake_multicarrier.py

WHY THIS FILE EXISTS
--------------------
The intake pipeline was born single-carrier: one `--txt`, one write of
AUGUST2026_INTAKE_RECORDS.jsonl, one hardcoded date. A second carrier could not
be ingested without silently destroying the first, and a read-only probe of the
27 and 28 August carriers reproduced five distinct failures before a single byte
was mutated:

  * both carriers stamped `received_date` / `attempt_date` 2026-08-24;
  * both restarted at AUG2026-S001 and AUG-0001, colliding with the committed
    24-August corpus;
  * the writer overwrote the store unconditionally;
  * `--check` validated only the carrier it was handed, so a dropped carrier
    left the committed records perfectly self-consistent -- which is exactly how
    submission S007 went missing once before;
  * "Internal: no question" parsed as an examiner NAMED "no question", and
    "simon"/"Simon" and "senthil"/"Senthil" split one person into two.

And one loss that only the source could reveal: the five `*` follow-up probes
the 27-August candidate recorded under "2. What is bmp ms" fell through every
branch into the preamble and vanished.

Eleven controls. Each asserts the SAFE behaviour, so every one of them is RED
against the pre-Stage-0 parser and GREEN after it. A lost occurrence raises no
error on its own: it just is not counted. That is what these tests are for.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
import ingest_august_intake as I  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "docs" / "MIW-master-Question-bank" / "New questions from August orals"
STORE = L.OUT / "AUGUST2026_INTAKE_RECORDS.jsonl"

C24 = "24 Aug 2026 oral questions.txt"
C27 = "27 Aug 2026 oral questions.txt"
C28 = "28 Aug 2026 oral questions.txt"

# The committed 24-August corpus. These are historical identities and this file
# exists partly to keep them that way.
COMMITTED_OCCURRENCES = 87
COMMITTED_SUBMISSIONS = 8

_failures: list[str] = []
_passes = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global _passes
    if cond:
        _passes += 1
        print(f"  PASS {name}")
    else:
        _failures.append(f"{name}: {detail}")
        print(f"  FAIL {name}  {detail}")


def carriers() -> list[dict]:
    return I.load_carriers()


def ingest_all() -> tuple[list[dict], list[dict], list[dict]]:
    """Every carrier, in registry order, as the production writer would."""
    return I.ingest_carriers(carriers())


# ── M1: carrier-specific dates ──────────────────────────────────────────────

def t_m1_dates():
    print("\nM1  carrier dates are the carrier's own, never a hardcoded constant")
    subs, _, _ = ingest_all()
    by_file: dict[str, set] = {}
    for s in subs:
        by_file.setdefault(s["source_file"], set()).add((s["received_date"], s["attempt_date"]))
    check("M1-24AUG", by_file.get(C24) == {("2026-08-24", "2026-08-24")}, str(by_file.get(C24)))
    check("M1-27AUG", by_file.get(C27) == {("2026-08-27", "2026-08-27")},
          f"27 August must not inherit 2026-08-24; got {by_file.get(C27)}")
    check("M1-28AUG", by_file.get(C28) == {("2026-08-28", "2026-08-28")},
          f"28 August must not inherit 2026-08-24; got {by_file.get(C28)}")


# ── M2 / M3: globally unique identities ─────────────────────────────────────

def t_m2_m3_identities():
    print("\nM2/M3  submission and occurrence identities are globally unique")
    subs, occ, _ = ingest_all()
    sids = [s["submission_id"] for s in subs]
    oids = [o["occurrence_id"] for o in occ]
    check("M2-NO-COLLISION", len(sids) == len(set(sids)),
          f"{len(sids) - len(set(sids))} duplicate submission id(s)")
    check("M3-NO-COLLISION", len(oids) == len(set(oids)),
          f"{len(oids) - len(set(oids))} duplicate occurrence id(s)")

    first24 = [s["submission_id"] for s in subs if s["source_file"] == C24]
    check("M2-24AUG-STABLE", first24 == [f"AUG2026-S{i:03d}" for i in range(1, 9)], str(first24[:3]))

    later = [s["submission_id"] for s in subs if s["source_file"] != C24]
    check("M2-NO-RESTART", "AUG2026-S001" not in later,
          "a later carrier restarted the submission sequence at S001")

    later_occ = [o["occurrence_id"] for o in occ
                 if o["submission_id"] in set(later)]
    check("M3-NO-RESTART", "AUG-0001" not in later_occ,
          "a later carrier restarted the occurrence sequence at AUG-0001")
    check("M3-CONTINUES", all(int(o[4:]) > COMMITTED_OCCURRENCES for o in later_occ),
          "later-carrier occurrence ids must continue past the committed 87")


# ── M4: prior-carrier preservation ──────────────────────────────────────────

def t_m4_preservation():
    print("\nM4  ingesting a later carrier preserves the committed 24-August records")
    _, occ, _ = ingest_all()
    have = [json.loads(l) for l in STORE.read_text(encoding="utf-8").splitlines() if l.strip()]

    # NOT "the store holds exactly 87". That is a guard that expires the first
    # time the corpus legitimately grows -- the batch-guard expiry defect this
    # repository has already paid for once. What M4 actually protects is that
    # the 24-August carrier still OCCUPIES the first 87 slots and still says the
    # same thing, which stays true however many carriers are appended after it.
    check("M4-COMMITTED-PREFIX", len(have) >= COMMITTED_OCCURRENCES,
          f"store holds {len(have)}, fewer than the committed {COMMITTED_OCCURRENCES}")
    committed = have[:COMMITTED_OCCURRENCES]
    check("M4-PREFIX-IS-24AUG",
          {o["submission_id"] for o in committed}
          == {f"AUG2026-S{i:03d}" for i in range(1, COMMITTED_SUBMISSIONS + 1)},
          "the first 87 stored records are no longer the 24-August submissions")

    regenerated = occ[:COMMITTED_OCCURRENCES]
    drift = [(a["occurrence_id"], k) for a, b in zip(regenerated, committed)
             for k in set(a) | set(b) if a.get(k) != b.get(k)]
    check("M4-BYTE-STABLE", not drift,
          f"regenerating the 24-August carrier changed {len(drift)} field(s): {drift[:4]}")

    # The mutation: drop one committed record and prove the check refuses.
    mutated = [dict(o) for o in occ]
    del mutated[10]
    ok, why = I.verify_against_store(mutated, have)
    check("M4-MUTATION-CAUGHT", not ok, f"a deleted prior record was accepted: {why}")


# ── M5: multi-carrier --check ───────────────────────────────────────────────

def t_m5_check():
    print("\nM5  --check validates EVERY registered carrier")
    regs = carriers()
    check("M5-ALL-REGISTERED", {c["source_file"] for c in regs} == {C24, C27, C28},
          f"registry holds {[c['source_file'] for c in regs]}")

    ok, why = I.verify_carriers(regs)
    check("M5-CLEAN-PASSES", ok, f"a clean tree failed the multi-carrier check: {why}")

    dropped = [c for c in regs if c["source_file"] != C28]
    ok, why = I.verify_carriers(dropped)
    check("M5-DROPPED-CARRIER-CAUGHT", not ok, "dropping a carrier was accepted")

    tampered = [dict(c) for c in regs]
    tampered[1] = {**tampered[1], "sha256": "0" * 64}
    ok, why = I.verify_carriers(tampered)
    check("M5-WRONG-HASH-CAUGHT", not ok, "a wrong carrier hash was accepted")

    redated = [dict(c) for c in regs]
    redated[1] = {**redated[1], "carrier_date": "2026-08-24"}
    ok, why = I.verify_carriers(redated)
    check("M5-WRONG-DATE-CAUGHT", not ok, "a wrong carrier date was accepted")


# ── S1: negative examiner sentinels ─────────────────────────────────────────
# Every spelling below is quoted from the actual carriers. Nothing generalised.
SENTINEL_LINES = [
    ("Internal: no question", C27),
    ("External : no qtns", C28),
    ("External : No Questions", C28),
]


def t_s1_sentinels():
    print("\nS1  a no-question sentinel never becomes an examiner identity")
    subs, occ, _ = ingest_all()
    names = {e["name_normalized"] for s in subs for e in s["examiners"]}
    names |= {n for o in occ for n in o.get("examiners", [])}
    bad = sorted(n for n in names if I.is_no_question_sentinel(n))
    check("S1-NO-FABRICATED-EXAMINER", not bad, f"fabricated examiner identities: {bad}")

    for line, _ in SENTINEL_LINES:
        check(f"S1-RECOGNISED {line!r}", I.is_no_question_sentinel(line.split(":", 1)[-1]),
              "not recognised as a sentinel")

    # A real examiner must NOT be swallowed by the sentinel rule.
    for real in ("Senthil", "simon", "Srivastava sir", "Nair"):
        check(f"S1-KEEPS {real!r}", not I.is_no_question_sentinel(real),
              "a real examiner name was treated as a sentinel")

    # Provenance: the sentinel wording is preserved somewhere, never erased.
    ctx = " ".join(c for s in subs for c in s["context_comments"]).lower()
    check("S1-PROVENANCE-KEPT", "no question" in ctx or "no qtns" in ctx,
          "the sentinel wording was erased instead of preserved as context")


# ── S2: examiner identity canonicalisation ──────────────────────────────────

def t_s2_canonical():
    print("\nS2  case-only variants of a KNOWN examiner unify; different names do not")
    subs, _, _ = ingest_all()
    names = {e["name_normalized"] for s in subs for e in s["examiners"]}
    for lower, canon in (("simon", "Simon"), ("senthil", "Senthil")):
        check(f"S2-UNIFIED {lower!r}", lower not in names,
              f"{lower!r} survived beside {canon!r}: {sorted(names)}")
    check("S2-CANONICAL-PRESENT", {"Simon", "Senthil", "Srivastava", "Nair"} <= names,
          f"expected canonical identities missing from {sorted(names)}")

    raws = {e["name_raw"] for s in subs for e in s["examiners"]}
    check("S2-RAW-PRESERVED", any(r.lower().startswith("simon") and r[0].islower() for r in raws),
          "the raw candidate spelling was overwritten by the canonical form")

    # Never merge by resemblance: the register's own rule.
    check("S2-NO-SURNAME-MERGE", I.canonical_examiner("Simone") == "Simone",
          "an unknown name was merged into a known one")
    check("S2-UNKNOWN-KEPT", I.canonical_examiner("Bhaskar") == "Bhaskar",
          "an unregistered examiner must pass through unchanged")


# ── S3: starred follow-up preservation ──────────────────────────────────────
STARRED_27AUG = [
    "Purpose.",
    "Before that what are all they.",
    "Why we are following  bmp ms",
    "Is application to all area",
    "Is only applicable to war zone?",
]


def t_s3_starred():
    print("\nS3  starred follow-up probes survive, with their parent, and bullets do not inflate")
    _, occ, _ = ingest_all()
    texts = [o["raw_question_text"] for o in occ]
    for probe in STARRED_27AUG:
        check(f"S3-SURVIVES {probe[:34]!r}", any(probe.strip() in t for t in texts),
              "a genuine starred examiner probe was lost")

    starred = [o for o in occ if o.get("source_line_style") == "STARRED_FOLLOWUP"]
    check("S3-COUNT", len(starred) == 5, f"expected 5 starred follow-ups, got {len(starred)}")
    check("S3-HAS-PARENT", all(o.get("parent_occurrence_id") for o in starred),
          "a starred follow-up carries no parent occurrence")

    by_id = {o["occurrence_id"]: o for o in occ}
    parents = {by_id[o["parent_occurrence_id"]]["raw_question_text"].strip().lower()
               for o in starred if o.get("parent_occurrence_id") in by_id}
    check("S3-PARENT-IS-Q2", parents == {"what is bmp ms"},
          f"the five probes must hang off '2. What is bmp ms'; got {parents}")

    # The other side: a decorative bullet is NOT promoted to examinable content.
    for decorative in ("*", "* ", "*---", "* * *"):
        check(f"S3-NOT-PROMOTED {decorative!r}", not I.starred_probe(decorative),
              "a decorative bullet was promoted to an examinable follow-up")
    check("S3-REAL-PROMOTED", I.starred_probe("*Purpose.") == "Purpose.",
          "a real starred probe was not recognised")


# ── source-line accounting ──────────────────────────────────────────────────

def t_accounting():
    print("\nACC  nothing in a carrier disappears silently")
    _, _, reports = ingest_all()
    for r in reports:
        check(f"ACC-NO-UNPARSED {r['source_file'][:6]}", not r["unparsed_source_blocks"],
              f"{len(r['unparsed_source_blocks'])} block(s) yielded no submission")


def main() -> int:
    print("multi-carrier August intake -- Stage 0 controls")
    for fn in (t_m1_dates, t_m2_m3_identities, t_m4_preservation, t_m5_check,
               t_s1_sentinels, t_s2_canonical, t_s3_starred, t_accounting):
        try:
            fn()
        except Exception as e:  # a missing hook is a RED result, not a crash
            _failures.append(f"{fn.__name__}: {type(e).__name__}: {e}")
            print(f"  FAIL {fn.__name__}  {type(e).__name__}: {e}")
    print(f"\nmulti-carrier intake controls -- {_passes} passed, {len(_failures)} failed")
    for f in _failures:
        print(f"  - {f}")
    return 1 if _failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
