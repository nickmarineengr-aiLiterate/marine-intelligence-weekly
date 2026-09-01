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
C31 = "_snapshots/31 Aug 2026 oral questions - snapshot 01.txt"

#: The 24/27/28 carriers are the HISTORICAL PREFIX of the registry. They are
#: named here so the controls can assert that they stay first and unchanged.
#: The registry itself is deliberately NOT pinned to a fixed set: 31 August is
#: a rolling day and more snapshot carriers are expected, so a control that
#: asserted the whole registry would go red on the next candidate report --
#: the guard-expiry defect this repository has now hit five times.
HISTORICAL_PREFIX = [C24, C27, C28]

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
    # NOT an equality against a fixed set. The claim a rolling registry can make
    # forever is that the historical carriers are still its first entries, in
    # order, and that every entry is distinct.
    names = [c["source_file"] for c in regs]
    check("M5-HISTORICAL-PREFIX", names[:3] == HISTORICAL_PREFIX,
          f"registry opens with {names[:3]}")
    check("M5-NO-DUPLICATE-CARRIER", len(names) == len(set(names)),
          f"a carrier is registered twice: {names}")
    check("M5-31AUG-REGISTERED", C31 in names,
          f"the 31 August snapshot is not registered: {names}")

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

# ── S4: the grammar the 31-August carrier introduced ────────────────────────
# Every defect below was reproduced against the pre-fix parser on the real
# snapshot before a line of the fix was written. None of them raises an error
# on its own: three of the four are SILENT LOSSES, which is the whole reason
# this block exists.

def _s31():
    """The 31-August snapshot's submissions, parsed in registry position."""
    regs = carriers()
    idx = [c["source_file"] for c in regs].index(C31)
    subs, occ, _ = ingest_all()
    return [s for s in subs if s.get("source_file") == Path(C31).name], occ, idx


def t_s4_lettered_roots():
    print("\nS4  lettered root asks with 'Cross questions:' underneath")
    subs, _, _ = _s31()
    occ = [o for s in subs for o in s["occurrences"]]
    roots = [o for o in occ if o.get("source_line_style") == "LETTERED_ROOT"]
    texts = [o["normalised_question_text"] for o in roots]

    # The candidate wrote four top-level asks as A. B. C. D. and hung the
    # examiner's cross-questions under each. The pre-fix parser recognised only
    # "1." numbering, so all four roots fell into the preamble and the eight
    # probes under A were promoted to eight independent root questions.
    check("S4-ROOTS-CAPTURED", len(roots) == 4, f"{len(roots)} lettered roots: {texts}")
    for want in ("Reason for Bulk carrier losses",
                 "Dry docking flooding precautions",
                 "H&M insurance",
                 "Manage Stress on board"):
        check(f"S4-ROOT {want[:24]!r}", any(want.lower() in x.lower() for x in texts),
              f"root not captured; have {texts}")

    # A lettered root must not be mistaken for a question number.
    check("S4-ROOT-NO-QNUM", all(o.get("source_question_number") is None for o in roots),
          "a lettered root carried a numeric source_question_number")


def t_s4_cross_questions():
    print("\nS4  cross-questions hang off their lettered root")
    subs, _, _ = _s31()
    occ = [o for s in subs for o in s["occurrences"]]
    roots = {o["occurrence_id"]: o for o in occ
             if o.get("source_line_style") == "LETTERED_ROOT"}
    cross = [o for o in occ if o.get("source_line_style") == "CROSS_QUESTION"]

    check("S4-CROSS-CAPTURED", len(cross) == 16,
          f"{len(cross)} cross-questions (8+3+3+1 under letters, +1 with no letter)")

    # EVERY cross-question has a parent. Most hang off a lettered root; the
    # product-tanker candidate wrote "Cross questions" with no lettered root at
    # all, and that probe falls back to the most recent non-cross occurrence -
    # the same rule the starred-probe branch uses. The claim is "never an
    # orphan", not "always a letter": asserting the stronger form was this
    # control's first version and it would have kept the parser's asymmetry.
    orphan = [o["occurrence_id"] for o in cross if not o.get("parent_occurrence_id")]
    check("S4-CROSS-NEVER-ORPHAN", not orphan, f"cross-questions with no parent: {orphan}")
    lettered = [o for o in cross if o.get("parent_occurrence_id") in roots]
    check("S4-CROSS-HAS-ROOT", len(lettered) == 15,
          f"{len(lettered)} of {len(cross)} cross-questions hang off a lettered root")

    # The candidate restarted numbering at 1 under every letter. That is what
    # the source says and the record keeps it, so source_question_number is NOT
    # unique within a submission -- occurrence_id is the only identity.
    nums = [o.get("source_question_number") for o in cross
            if o.get("parent_occurrence_id") in roots]
    check("S4-RESTARTED-NUMBERING-KEPT", nums.count(1) == 4,
          f"expected four restarts at 1, saw {nums}")

    # And the eight probes under A must NOT be siblings of the three under B.
    by_root = {}
    for o in cross:
        by_root.setdefault(o["parent_occurrence_id"], []).append(o)
    by_letter = {k: v for k, v in by_root.items() if k in roots}
    check("S4-CROSS-GROUPED", sorted(len(v) for v in by_letter.values()) == [1, 3, 3, 8],
          f"grouping under lettered roots is {sorted(len(v) for v in by_letter.values())}")


def t_s4_unnumbered_question():
    print("\nS4  an unnumbered question under a bare role heading")
    subs, _, _ = _s31()
    occ = [o for s in subs for o in s["occurrences"]]
    hit = [o for o in occ if "doc will be withdrawn" in o["normalised_question_text"].lower()]

    # "Internal:" then, on its own line, "When DOC will be withdrawn ?". The
    # submission was in numbered mode, so this line matched no branch and went
    # to the preamble. A question ending in "?" is never preamble.
    check("S4-UNNUMBERED-Q-CAPTURED", len(hit) == 1,
          f"{len(hit)} occurrences for the unnumbered DOC question")
    if hit:
        check("S4-UNNUMBERED-Q-IS-QUESTION", hit[0]["is_question"],
              "captured but marked not-a-question")


def t_s4_honorifics():
    print("\nS4  'Mr. Simon' is Simon")
    check("S4-HONORIFIC-STRIPPED",
          I.canonical_examiner(I.normalise_examiner("Mr. Simon,")) == "Simon",
          repr(I.canonical_examiner(I.normalise_examiner("Mr. Simon,"))))
    check("S4-HONORIFIC-STRIPPED-2",
          I.canonical_examiner(I.normalise_examiner("Mr. Srivastava.")) == "Srivastava",
          repr(I.canonical_examiner(I.normalise_examiner("Mr. Srivastava."))))

    # The register is the authority on identity, so no carrier may introduce a
    # name it does not know. This is what stops "Mr. Simon" quietly becoming a
    # seventh examiner in the attribution store.
    reg = json.loads((L.OUT / "EXAMINER_ALIAS_REGISTER.json").read_text(encoding="utf-8"))
    known = {e["canonical_name"] for e in reg["examiners"]}
    subs, _, _ = ingest_all()
    seen = {e["name_normalized"] for s in subs for e in s["examiners"]}
    check("S4-NO-NEW-EXAMINER-IDENTITIES", seen <= known,
          f"identities not in the alias register: {sorted(seen - known)}")


def t_s4_commentary():
    print("\nS4  the candidate's own commentary is not an examiner question")
    subs, _, _ = _s31()
    occ = [o for s in subs for o in s["occurrences"]]
    texts = [o["normalised_question_text"].lower() for o in occ]
    for phrase in ("conducting yoga",
                   "main answer he is expecting",
                   "these are the main points"):
        bad = [x for x in texts if phrase in x and len(x) < 120]
        check(f"S4-COMMENTARY-NOT-A-QUESTION {phrase[:22]!r}",
              all(not o["is_question"] for o in occ
                  if phrase in o["normalised_question_text"].lower()),
              f"commentary promoted to an examinable question: {bad}")


def t_s4_duplicate_numbering():
    print("\nS4  the source's own duplicate '1.' is kept, not deduplicated")
    subs, _, _ = _s31()
    first = subs[0]["occurrences"]
    ones = [o for o in first if o.get("source_question_number") == 1]
    check("S4-DUPLICATE-NUMBER-KEPT", len(ones) == 2,
          f"the carrier writes '1.' twice; parser kept {len(ones)}")


def t_s4_attempt_ordinal():
    print("\nS4  '2nd attempt' is an attempt number, not a comment")
    subs, _, _ = _s31()
    # ATTEMPT_RE reads "Attempt 2"; this candidate wrote "2nd attempt". The
    # number is evidence about the report's weight - a resit is a different
    # kind of witness - so it belongs in the field, not in prose.
    got = [s.get("attempt_number") for s in subs]
    check("S4-ORDINAL-ATTEMPT-PARSED", 2 in got, f"attempt numbers are {got}")
    occ = [o for s in subs for o in s["occurrences"] if s.get("attempt_number") == 2]
    check("S4-ATTEMPT-ON-OCCURRENCES", occ and all(o["attempt_number"] == 2 for o in occ),
          "the attempt number did not reach that submission's occurrences")


def t_s4_line_accounting():
    print("\nS4  every meaningful source line is accounted for")
    subs, _, _ = _s31()
    src = (SRC / C31).read_text(encoding="utf-8").splitlines()
    meaningful = [l.strip() for l in src
                  if l.strip() and not I.RULE_RE.match(l.strip())]
    accounted = set()
    for s in subs:
        for o in s["occurrences"]:
            accounted.add(I.normalise(o["raw_question_text"]).lower())
        for c in s["context_comments"]:
            accounted.add(I.normalise(c).lower())
        for e in s["examiners"]:
            accounted.add(I.normalise(e["name_raw"]).lower())

    # A line CONSUMED by a metadata branch is accounted for by the value it
    # produced, not by surviving as text: "RESULT: PASS!" becomes
    # attempt_result, "Internal:" becomes an attribution state. Requiring those
    # to reappear verbatim was this control's own first bug, and it would have
    # driven the fix in exactly the wrong direction - towards keeping copies of
    # lines the parser had correctly understood.
    consumed = 0
    lost = []
    for line in meaningful:
        n = I.normalise(line).lower()
        if any(n in a or a in n for a in accounted if a):
            continue
        if (I.RESULT_RE.match(line) or I.BARE_ROLE_RE.match(line)
                or I.ATTEMPT_RE.match(line) or I.ATTEMPT_ORDINAL_RE.match(line)
                or I.CROSS_Q_RE.match(line)):
            consumed += 1
            continue
        lost.append(line)
    check("S4-NO-SILENT-LINE-LOSS", not lost,
          f"{len(lost)} source line(s) reach neither an occurrence, the record, "
          f"nor a metadata branch: {lost[:4]}")
    check("S4-METADATA-CONSUMED", consumed >= 3,
          f"only {consumed} lines were consumed by a metadata branch")
    # and the values those lines produced actually landed
    results = {s.get("attempt_result") for s in subs}
    check("S4-RESULT-LANDED", {"pass", "PASS!"} <= {str(r) for r in results},
          f"attempt_result values are {results}")


# ── S5: the rolling-snapshot contract ───────────────────────────────────────
# 31 August is a rolling day: the human inbox file keeps growing as more
# candidates report. ingest_carriers re-walks EVERY carrier from the first and
# reproduces earlier records byte-for-byte, so a carrier that grew between runs
# would renumber identities already issued and published. The contract is that
# the inbox is never a carrier - an immutable SNAPSHOT is - and that appending
# the next snapshot moves nothing. This control proves it instead of asserting
# it, by simulating snapshot 02 without writing one.

def t_s5_rolling_snapshot():
    print("\nS5  appending the next snapshot moves no existing identity")
    regs = carriers()
    subs, occ, _ = ingest_all()
    before = {o["occurrence_id"]: o for o in occ}

    # A hypothetical snapshot 02 carrying ONLY new material. Any file will do -
    # the 28-August carrier is reused as a stand-in for "some further text",
    # because what is under test is IDENTITY ALLOCATION, not that file's content.
    nxt = [dict(c) for c in regs] + [{
        **{k: v for k, v in regs[2].items()},
        "carrier_date": "2026-08-31", "received_date": "2026-08-31",
        "attempt_date": "2026-08-31",
    }]
    subs2, occ2, _ = I.ingest_carriers(nxt)
    after = {o["occurrence_id"]: o for o in occ2}

    # 1. every identity that existed still exists, unchanged
    drift = [k for k in before if k not in after
             or after[k]["raw_question_text"] != before[k]["raw_question_text"]
             or after[k]["submission_id"] != before[k]["submission_id"]]
    check("S5-EXISTING-IDS-IMMOVABLE", not drift,
          f"{len(drift)} identity/identities moved when a snapshot was appended: {drift[:4]}")

    # 2. the new material lands strictly AFTER, never interleaved
    fresh = [k for k in after if k not in before]
    check("S5-NEW-IDS-CONTINUE", fresh and all(int(k[4:]) > len(before) for k in fresh),
          f"appended snapshot did not continue the sequence: {sorted(fresh)[:3]}")

    # 3. and the submission sequence continues too
    old_subs = {s["submission_id"] for s in subs}
    new_subs = {s["submission_id"] for s in subs2} - old_subs
    check("S5-NEW-SUBMISSIONS-CONTINUE",
          new_subs and min(new_subs) > max(old_subs),
          f"submission ids collided or restarted: {sorted(new_subs)[:3]}")

    # 4. the inbox itself must never be registered as a carrier
    inbox = "31 Aug 2026 oral questions.txt"
    check("S5-INBOX-NOT-A-CARRIER",
          inbox not in {c["source_file"] for c in regs},
          "the mutable inbox file is registered as a carrier; it will renumber "
          "identities the next time a candidate adds to it")

    # 5. and the snapshot that IS registered must still match its recorded hash.
    #    Checked directly rather than through verify_carriers, which refuses a
    #    SUBSET on purpose - dropping a carrier is itself a failure mode it
    #    guards (M5-DROPPED-CARRIER-CAUGHT), and handing it one was this
    #    control's own first bug.
    import hashlib
    snaps = [c for c in regs if c["source_file"].startswith("_snapshots/")]
    check("S5-SNAPSHOT-REGISTERED", bool(snaps), "no snapshot carrier is registered")
    for c in snaps:
        got = hashlib.sha256(I.carrier_path(c).read_bytes()).hexdigest()
        check(f"S5-SNAPSHOT-IMMUTABLE {c['source_file'][-13:]}", got == c["sha256"],
              f"snapshot bytes changed: recorded {c['sha256'][:12]}, on disk {got[:12]}")



def t_accounting():
    print("\nACC  nothing in a carrier disappears silently")
    _, _, reports = ingest_all()
    for r in reports:
        check(f"ACC-NO-UNPARSED {r['source_file'][:6]}", not r["unparsed_source_blocks"],
              f"{len(r['unparsed_source_blocks'])} block(s) yielded no submission")


# ── S6: a sitting reported later than it happened ───────────────────────────

def t_s6_late_report():
    """The 31-August day received a second snapshot on 1 September, because a
    candidate who sat on 31 August only shared his report the following day.

    verify_carriers() used to require received_date == carrier_date, which made
    a late report unrepresentable and refused the whole ingest. The exam date and
    the report date are different facts and the registry has always carried both;
    the invariant is that a report cannot arrive BEFORE the sitting.
    """
    import copy
    from ingest_august_intake import verify_carriers
    print("\nS6  a report may arrive after the sitting, never before it")
    regs = carriers()

    ok, why = verify_carriers(regs)
    check("S6-LATE-REPORT-ACCEPTED", ok,
          f"the registry as it stands must verify; got: {why}")

    late = [c for c in regs if c["received_date"] > c["carrier_date"]]
    check("S6-LATE-REPORT-PRESENT", bool(late),
          "snapshot 02 is a 31-August carrier received on 1 September; if no carrier "
          "has received_date after carrier_date this control is no longer exercising "
          "anything")

    for c in late:
        check(f"S6-EXAM-DATE-HELD {c['source_file'][-13:]}",
              c["attempt_date"] == c["carrier_date"] == "2026-08-31",
              f"a late report must NOT move the exam date; got carrier={c['carrier_date']} "
              f"attempt={c['attempt_date']}")

    # A report dated before its sitting is impossible and must be refused.
    bad = copy.deepcopy(regs)
    bad[-1]["received_date"] = "2026-08-30"
    ok2, why2 = verify_carriers(bad)
    check("S6-REPORT-BEFORE-EXAM-REFUSED", not ok2,
          "a received_date earlier than the carrier_date must be refused; "
          f"verify_carriers said: {why2}")

    # The exam date itself is still pinned to the carrier.
    bad2 = copy.deepcopy(regs)
    bad2[-1]["attempt_date"] = "2026-09-01"
    ok3, why3 = verify_carriers(bad2)
    check("S6-ATTEMPT-DATE-STILL-PINNED", not ok3,
          "attempt_date must still be required to equal carrier_date; "
          f"verify_carriers said: {why3}")


def t_s6_no_september_identities():
    """A 31-August late report must not create September identities."""
    print("\nS6  a late 31-August report creates AUG identities, never SEP")
    subs, occ, _ = ingest_all()
    bad_sub = [s["submission_id"] for s in subs if not s["submission_id"].startswith("AUG2026-S")]
    bad_occ = [o["occurrence_id"] for o in occ if not o["occurrence_id"].startswith("AUG-")]
    check("S6-NO-SEP-SUBMISSION-IDS", not bad_sub, f"non-August submission ids: {bad_sub[:5]}")
    check("S6-NO-SEP-OCCURRENCE-IDS", not bad_occ, f"non-August occurrence ids: {bad_occ[:5]}")

    s02 = [s for s in subs if s["source_file"].endswith("snapshot 02.txt")]
    check("S6-SNAPSHOT02-IS-31AUG",
          bool(s02) and all(s["attempt_date"] == "2026-08-31" for s in s02),
          "snapshot 02 submissions must carry the 31-August exam date; got "
          f"{[s.get('attempt_date') for s in s02]}")
    check("S6-SNAPSHOT02-REPORTED-LATE",
          bool(s02) and all(s["received_date"] == "2026-09-01" for s in s02),
          "snapshot 02 submissions must carry the 1-September report date; got "
          f"{[s.get('received_date') for s in s02]}")


def main() -> int:
    print("multi-carrier August intake -- Stage 0 controls")
    for fn in (t_m1_dates, t_m2_m3_identities, t_m4_preservation, t_m5_check,
               t_s1_sentinels, t_s2_canonical, t_s3_starred,
               t_s4_lettered_roots, t_s4_cross_questions,
               t_s4_unnumbered_question, t_s4_honorifics, t_s4_commentary,
               t_s4_duplicate_numbering, t_s4_attempt_ordinal,
               t_s4_line_accounting, t_s5_rolling_snapshot,
               t_s6_late_report, t_s6_no_september_identities, t_accounting):
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
