"""Ingest the governed card/ledger examiner reconciliation.

CARD_EXAMINER_RECONCILIATION.json is the decision record: one adjudication per
in-card examiner attribution rendered by a QB question card. This tool is the
only writer that turns its ADD_RELATIONSHIP decisions into published rows, and
it writes through the two stores the rest of the toolchain already reads:

    CURRENT_EXAMINER_RELATIONSHIPS.jsonl   the canonical relationship ledger
    EXAMINER_EVIDENCE_LEDGER_V2.jsonl      the evidence records they cite

Why evidence records are written at all
---------------------------------------
validate_phase2.py resolves every relationship's evidence_ids against V2 and
nothing else, so citing a MASTER-AQ id straight from a relationship would fail
the gate. Each added relationship therefore gets one CARDREC evidence record
whose source_id names the master-tracker record that actually earns the tier:

    evidence_tier = PRIMARY_TRACKER    source_type = MASTER_TRACKER

Both are already in the provenance model, and MASTER_TRACKER is not a derived
source type, so the record is self-consistent under oral_provenance.violations.

Removals
--------
A REMOVE_RELATIONSHIP decision deletes published rows whose stated provenance
is disproved, together with the evidence records that cite them -- leaving the
evidence behind would trip validate_phase2's "every evidence record resolves to
a relationship". Removal is only ever executed from an adjudicated decision
carrying an `adjudication` field, never inferred, and the decision must name
the relationship ids so the diff is reviewable before it is run.

Tiering
-------
Two paths, and the tool refuses anything that mixes them:

  master_primary_evidence_ids  -> PRIMARY_CONFIRMED  -> 'confirmed'
      backed by a PRIMARY_CANDIDATE_RECORD in the master tracker whose
      examiner and question both match the pair.
  external_evidence_ids        -> EXTERNAL_SOURCE_CONFIRMED -> 'reported'
      backed by an ALL_SURVEYORS_COMPILATION source record. A reported
      attribution stays reported: the external compilation can never produce
      a primary tier, which oral_provenance enforces independently.

What this tool will not do
--------------------------
  * it never invents an examiner: every name must resolve in the alias register;
  * it never writes a HOLD_PROVENANCE or CONFLICT_REQUIRES_REVIEW decision;
  * it never writes a pair that is already published. The ledger is only one
    input to the published universe: build_examiner_index.py upserts it with
    card data-examiner attributes, RELEASE_A_PUBLICATION.json and the CE-tip
    review decisions. A pair absent from the ledger but present in Release A
    is already canonical, and writing it again would inflate the examiner
    count, so both stores are checked and a collision is a hard failure;
  * it never edits a QB page. The card display lines are left exactly as they
    are; this is an evidence repair, not an editorial one.

    PYTHONIOENCODING=utf-8 python tools/oral/ingest_card_examiners.py [--check]

--check recomputes both files in memory and compares bytes, writing nothing.
Exit 0 current, 3 stale/missing, 2 refused.
"""
from __future__ import annotations

import json
import sys

import oral_lib as L

OUT = L.OUT
RECORD = "CARD_EXAMINER_RECONCILIATION.json"
LEDGER = "CURRENT_EXAMINER_RELATIONSHIPS.jsonl"
EVIDENCE = "EXAMINER_EVIDENCE_LEDGER_V2.jsonl"

SOURCE_LAYER = "CARD_LEDGER_RECONCILIATION"
EVIDENCE_PREFIX = "CARDREC"


def fail(msg):
    print("REFUSED: " + msg)
    raise SystemExit(2)


def jl(name):
    with (OUT / name).open(encoding="utf-8") as fh:
        return [json.loads(x) for x in fh if x.strip()]


def dumps(rows):
    """One compact JSON object per line, LF, trailing newline -- byte-identical
    to how both stores are already written."""
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def build():
    record = json.loads((OUT / RECORD).read_text(encoding="utf-8"))
    alias = json.loads((OUT / "EXAMINER_ALIAS_REGISTER.json").read_text(encoding="utf-8"))
    known = {e["canonical_name"] for e in alias["examiners"]}

    ledger = jl(LEDGER)
    evidence = jl(EVIDENCE)

    # Everything this tool has written before, so a re-run is idempotent rather
    # than additive. Prior rows are dropped and rebuilt from the record.
    base_ledger = [r for r in ledger if r.get("source_layer") != SOURCE_LAYER]
    base_evidence = [e for e in evidence
                     if not str(e.get("evidence_id", "")).startswith(EVIDENCE_PREFIX + "-")]

    # ---- adjudicated removals -------------------------------------------
    # Executed only from a decision that carries an adjudication and names the
    # rows. A removal inferred from a classification alone would let a future
    # edit to this record silently delete published relationships.
    doomed = set()
    for d in record["decisions"]:
        if d.get("decision") != "REMOVE_RELATIONSHIP":
            continue
        if not d.get("adjudication"):
            fail("a REMOVE_RELATIONSHIP decision for %s carries no adjudication"
                 % d.get("file"))
        named = d.get("relationships_removed") or []
        if not named:
            fail("the REMOVE_RELATIONSHIP decision for %s names no relationship ids"
                 % d.get("file"))
        for row in named:
            doomed.add((row["relationship_id"], row["question_id"], row["examiner"]))

    live = {r["relationship_id"]: r for r in base_ledger}
    live_pairs = {(r["question_id"], r["examiner"]): r["relationship_id"]
                  for r in base_ledger}
    for rid, qid, ex in sorted(doomed):
        r = live.get(rid)
        if r is None:
            # Already removed: a second run is a no-op, which is what makes
            # --check a meaningful byte comparison. But absence of the ID is
            # not proof the row is gone -- it could have been rewritten under
            # a different id, and deleting nothing while reporting success is
            # exactly the silent failure this tool exists to prevent.
            if (qid, ex) in live_pairs:
                fail("removal target %s is absent but %s/%s is still published as %s"
                     % (rid, qid, ex, live_pairs[(qid, ex)]))
            continue
        # The record must still describe the row it is deleting. If the ledger
        # moved under the record, the reviewed diff is not the applied one.
        if (r["question_id"], r["examiner"]) != (qid, ex):
            fail("removal target %s is %s/%s in the ledger, not %s/%s"
                 % (rid, r["question_id"], r["examiner"], qid, ex))

    removed_ids = {rid for rid, _q, _e in doomed}
    base_ledger = [r for r in base_ledger if r["relationship_id"] not in removed_ids]
    # The evidence records that cited them go too: an orphan evidence record
    # fails validate_phase2's "every evidence record resolves to a relationship".
    base_evidence = [e for e in base_evidence
                     if e.get("relationship_id") not in removed_ids]

    pub = json.loads((OUT / "RELEASE_A_PUBLICATION.json").read_text(encoding="utf-8"))
    release_a = {(c["canonical_question_id"], c["examiner"]): c["relation_id"]
                 for c in pub["connections"]}

    existing_pairs = {(r["question_id"], r["examiner"]) for r in base_ledger}
    existing_rel_ids = {r["relationship_id"] for r in base_ledger}
    existing_ev_ids = {e["evidence_id"] for e in base_evidence}

    inventory = {q["canonical_question_id"] for q in L.build_inventory()}
    anchors = L.all_anchors()

    master = {e["evidence_id"]: e for e in jl("EXAMINER_EVIDENCE_LEDGER.jsonl")}
    surveyors = {s["source_id"]: s
                 for s in jl("ALL_SURVEYORS_SOURCE_RECORDS.jsonl")}

    adds = [d for d in record["decisions"] if d.get("decision") == "ADD_RELATIONSHIP"]
    if not adds:
        fail("the decision record carries no ADD_RELATIONSHIP decisions")

    new_rels, new_ev = [], []
    for n, d in enumerate(sorted(adds, key=lambda x: x["question_id"])):
        qid = d["question_id"]
        ex = d["canonical_examiner"]
        file_, anchor = d["file"], d["anchor"]

        if ex not in known:
            fail("examiner %r (%s) is not in the alias register" % (ex, qid))
        if qid not in inventory:
            fail("%s does not resolve to a live canonical question" % qid)
        if anchor not in anchors.get(file_, set()):
            fail("anchor %s does not exist on %s" % (anchor, file_))
        if (qid, ex) in existing_pairs:
            fail("the ledger already carries %s / %s -- a second row would "
                 "inflate the examiner count" % (qid, ex))
        if (qid, ex) in release_a:
            fail("%s / %s is already published by Release A as %s -- a ledger "
                 "row would duplicate a published relationship"
                 % (qid, ex, release_a[(qid, ex)]))

        primaries = d.get("master_primary_evidence_ids") or []
        externals = d.get("external_evidence_ids") or []
        if primaries and externals:
            fail("%s / %s cites both master and external evidence; the two tier "
                 "differently and the record must choose" % (qid, ex))
        if not primaries and not externals:
            fail("%s / %s is an ADD with no evidence at all" % (qid, ex))

        # The cited record must actually name this examiner and this question:
        # an id that resolves is a pointer, not evidence.
        for pid in primaries:
            m = master.get(pid)
            if m is None:
                fail("evidence id %s (%s) does not exist in the master ledger" % (pid, qid))
            if m["examiner_normalized"] != ex:
                fail("%s names examiner %r, not %r (%s)"
                     % (pid, m["examiner_normalized"], ex, qid))
            if m.get("canonical_question_id") != qid:
                fail("%s points at %r, not %s" % (pid, m.get("canonical_question_id"), qid))

        for sid in externals:
            s = surveyors.get(sid)
            if s is None:
                fail("source id %s (%s) is not in ALL_SURVEYORS_SOURCE_RECORDS" % (sid, qid))
            if s.get("surveyor_normalized") != ex:
                fail("%s names surveyor %r, not %r (%s)"
                     % (sid, s.get("surveyor_normalized"), ex, qid))

        if externals:
            if d["research_best_tier"] != "EXTERNAL_SOURCE_CONFIRMED":
                fail("%s / %s is externally sourced and may only carry "
                     "EXTERNAL_SOURCE_CONFIRMED, not %r"
                     % (qid, ex, d["research_best_tier"]))
            if d["current_tier"] != "reported":
                fail("%s / %s is externally sourced and may only publish at "
                     "'reported', not %r" % (qid, ex, d["current_tier"]))
        elif d["research_best_tier"] != "PRIMARY_CONFIRMED":
            fail("%s / %s cites master evidence but claims %r"
                 % (qid, ex, d["research_best_tier"]))

        rel_id = "REL-%s-%s-%s" % (ex.upper(), file_[:-5], anchor)
        if rel_id in existing_rel_ids:
            fail("relationship id %s already exists" % rel_id)
        ev_id = "%s-%04d" % (EVIDENCE_PREFIX, n)
        if ev_id in existing_ev_ids:
            fail("evidence id %s already exists" % ev_id)

        if primaries:
            src = master[primaries[0]]
            new_ev.append({
                "evidence_id": ev_id,
                "relationship_id": rel_id,
                "examiner_raw": d["raw_examiner_string"],
                "examiner_normalized": ex,
                "source_type": "MASTER_TRACKER",
                "source_id": ",".join(primaries),
                "source_location": "%s#%s (in-card examiner-tag)" % (file_, anchor),
                "source_date": src.get("source_date"),
                "raw_question_text": src.get("source_wording") or "",
                "source_comment": "card/ledger reconciliation 2026-08-23",
                "evidence_tier": "PRIMARY_TRACKER",
                "match_status": "RESOLVED",
                "notes": ("The primary candidate record earns this tier. The card's "
                          "examiner-tag corroborates it and is what surfaced the gap; "
                          "the card alone would never carry a primary tier."),
            })
        else:
            src = surveyors[externals[0]]
            new_ev.append({
                "evidence_id": ev_id,
                "relationship_id": rel_id,
                "examiner_raw": src.get("surveyor_raw") or d["raw_examiner_string"],
                "examiner_normalized": ex,
                "source_type": "ALL_SURVEYORS_COMPILATION",
                "source_id": ",".join(externals),
                "source_location": "%s p.%s para %s (%s)"
                                   % (src.get("source_provenance"), src.get("source_page"),
                                      src.get("source_paragraph"), src.get("source_family_id")),
                "source_date": None,
                "raw_question_text": src.get("raw_question_text") or "",
                "source_comment": "card/ledger reconciliation 2026-08-23, Founder-authorised",
                "evidence_tier": "EXTERNAL_SURVEYOR_COMPILATION",
                "match_status": "RESOLVED",
                "notes": ("An external compilation record: a reported ask, not a tracker "
                          "record. It publishes at 'reported' and can never reach a primary "
                          "tier - oral_provenance refuses EXTERNAL_SURVEYOR_COMPILATION on "
                          "any primary tier independently of this tool."),
            })

        new_rels.append({
            "relationship_id": rel_id,
            "question_id": qid,
            "examiner": ex,
            "examiner_raw": d["raw_examiner_string"],
            "target_file": file_,
            "target_anchor": anchor,
            "relationship_type": "UNSPECIFIED",
            "status": "PUBLISHED",
            "current_tier": d["current_tier"],
            "current_tier_valid": True,
            "repaired_tier": d["current_tier"],
            "index_display_text": "",
            "current_question_text": "",
            "recovery_status": "NOT_IN_INDEX_RECOVERY",
            "source_layer": SOURCE_LAYER,
            "first_row_index": None,
            "duplicate_row_indexes": [],
            "evidence_ids": [ev_id],
            "notes": ("Added by the card/ledger examiner reconciliation. The index "
                      "recovery never saw this file, so the relationship was absent "
                      "while the card displayed it."),
            "primary_evidence_ids": primaries,
            "primary_evidence_count": len(primaries),
            "external_evidence_ids": externals,
            "derived_sibling_evidence_count": len(d.get("corroborating_sibling_evidence_ids") or []),
            "prose_strength": None,
            "research_best_tier": d["research_best_tier"],
            "evidence_count": len(primaries) + len(externals),
            "tier_changed": False,
        })

    return (dumps(base_ledger + new_rels), dumps(base_evidence + new_ev),
            len(new_rels), len(base_ledger))


def main():
    check = "--check" in sys.argv[1:]
    ledger_txt, evidence_txt, added, before = build()

    targets = ((LEDGER, ledger_txt), (EVIDENCE, evidence_txt))
    if check:
        stale = [n for n, t in targets
                 if not (OUT / n).exists()
                 or (OUT / n).read_bytes() != t.encode("utf-8")]
        if stale:
            print("STALE: " + ", ".join(stale))
            return 3
        print("CARD EXAMINER INGEST CHECK: PASS")
        print("  %d reconciled relationships current in both stores" % added)
        return 0

    for name, text in targets:
        (OUT / name).write_bytes(text.encode("utf-8"))
    print("wrote %s and %s" % (LEDGER, EVIDENCE))
    print("  relationships %d -> %d (+%d)" % (before, before + added, added))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
