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

    pub = json.loads((OUT / "RELEASE_A_PUBLICATION.json").read_text(encoding="utf-8"))
    release_a = {(c["canonical_question_id"], c["examiner"]): c["relation_id"]
                 for c in pub["connections"]}

    existing_pairs = {(r["question_id"], r["examiner"]) for r in base_ledger}
    existing_rel_ids = {r["relationship_id"] for r in base_ledger}
    existing_ev_ids = {e["evidence_id"] for e in base_evidence}

    inventory = {q["canonical_question_id"] for q in L.build_inventory()}
    anchors = L.all_anchors()

    master = {e["evidence_id"]: e for e in jl("EXAMINER_EVIDENCE_LEDGER.jsonl")}

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

        primaries = d["master_primary_evidence_ids"]
        if not primaries:
            fail("%s / %s is an ADD with no master-tracker evidence" % (qid, ex))

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

        rel_id = "REL-%s-%s-%s" % (ex.upper(), file_[:-5], anchor)
        if rel_id in existing_rel_ids:
            fail("relationship id %s already exists" % rel_id)
        ev_id = "%s-%04d" % (EVIDENCE_PREFIX, n)
        if ev_id in existing_ev_ids:
            fail("evidence id %s already exists" % ev_id)

        new_ev.append({
            "evidence_id": ev_id,
            "relationship_id": rel_id,
            "examiner_raw": d["raw_examiner_string"],
            "examiner_normalized": ex,
            "source_type": "MASTER_TRACKER",
            "source_id": ",".join(primaries),
            "source_location": "%s#%s (in-card examiner-tag)" % (file_, anchor),
            "source_date": master[primaries[0]].get("source_date"),
            "raw_question_text": master[primaries[0]].get("source_wording") or "",
            "source_comment": "card/ledger reconciliation 2026-08-23",
            "evidence_tier": "PRIMARY_TRACKER",
            "match_status": "RESOLVED",
            "notes": ("The primary candidate record earns this tier. The card's "
                      "examiner-tag corroborates it and is what surfaced the gap; "
                      "the card alone would never carry a primary tier."),
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
            "derived_sibling_evidence_count": len(d.get("corroborating_sibling_evidence_ids") or []),
            "prose_strength": None,
            "research_best_tier": d["research_best_tier"],
            "evidence_count": len(primaries),
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
