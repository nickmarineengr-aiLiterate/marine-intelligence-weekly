"""Phase 2 gate - deterministic validation of the reconciliation artefacts.

Fails closed: an unavailable input is a failure, never a silent pass. Run after
any regeneration; a new failure means something regressed.

  PYTHONIOENCODING=utf-8 python tools/oral/validate_phase2.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
import oral_provenance as P  # noqa: E402
import oral_notes as N  # noqa: E402
import notes_coverage as C  # noqa: E402

OUT = L.OUT

CONTENT_DISPOSITIONS = {"EXACT_MATCH", "NEAR_MATCH", "SAME_CORE_ASK",
                        "PARTIAL_COVERAGE", "MISSING", "AMBIGUOUS"}
MAPPING_STATUSES = {"ALREADY_LINKED", "NEW_LINK", "CONFLICTING_LINK",
                    "UNMAPPED", "NOT_APPLICABLE"}
RELATIONSHIP_TYPES = {"PRIMARY_ASK", "CROSS_QUESTION", "FOLLOW_UP",
                      "EXPECTED_DETAIL", "UNSPECIFIED", "TOPIC_INFERENCE_ONLY"}
RESEARCH_TIERS = {"MULTI_SOURCE_CONFIRMED", "PRIMARY_CONFIRMED",
                  "EXTERNAL_SOURCE_CONFIRMED", "CE_TIP", "HEADER",
                  "INFERRED_ONLY", "CONFLICTED"}
# The evidence tier vocabulary lives with the provenance model, so a tier can
# never be added without a statement of what provenance may carry it.
EVIDENCE_TIERS = P.EVIDENCE_TIERS
# Stated here rather than imported from the builder: the gate must fail if the
# builder invents a seventh production action, which it cannot do if it is the
# builder that defines the vocabulary the gate checks against.
PRODUCTION_ACTIONS = {"NO_ACTION_ALREADY_COVERED", "CONNECT_EXISTING",
                      "CONNECT_AND_ENRICH", "NOTES_TO_QB_PROMOTION",
                      "NEW_ANSWER_REQUIRED", "MERGE_WITH_EXISTING_GAP",
                      "HUMAN_REVIEW"}
P0_ACTIONS = {"P0_NEW_ANSWER", "P0_ENRICH_EXISTING_QB",
              "P0_NOTES_TO_QB_PROMOTION", "P0_MERGE_WITH_OTHER",
              "P0_HUMAN_REVIEW"}

results = []


def check(name, ok, detail=""):
    results.append({"check": name,
                    "status": "PASS" if ok else "FAIL",
                    "detail": detail})


def jsonl(name):
    p = OUT / name
    if not p.exists():
        return None
    return [json.loads(l) for l in p.open(encoding="utf-8")]


def jsonobj(name):
    p = OUT / name
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def main():
    inv = {q["canonical_question_id"]: q for q in L.build_inventory()}
    anchors = L.all_anchors()

    rels = jsonl("CURRENT_EXAMINER_RELATIONSHIPS.jsonl")
    ev = jsonl("EXAMINER_EVIDENCE_LEDGER_V2.jsonl")
    src = jsonl("ALL_SURVEYORS_SOURCE_RECORDS.jsonl")
    recon = jsonl("ORAL_788_RECONCILIATION.jsonl")
    for name, obj in (("CURRENT_EXAMINER_RELATIONSHIPS.jsonl", rels),
                      ("EXAMINER_EVIDENCE_LEDGER_V2.jsonl", ev),
                      ("ALL_SURVEYORS_SOURCE_RECORDS.jsonl", src),
                      ("ORAL_788_RECONCILIATION.jsonl", recon)):
        check("input available: " + name, obj is not None,
              "missing" if obj is None else "%d records" % len(obj))
    if not all((rels, ev, src, recon)):
        return emit()

    gaps = json.loads((OUT / "ORAL_GAP_CANDIDATES.json").read_text(encoding="utf-8"))
    ready = json.loads((OUT / "READY_CONNECTIONS_V2.json").read_text(encoding="utf-8"))
    fams = json.loads((OUT / "ALL_SURVEYORS_SOURCE_FAMILIES.json").read_text(encoding="utf-8"))
    alias = json.loads((OUT / "EXAMINER_ALIAS_REGISTER.json").read_text(encoding="utf-8"))
    known = {e["canonical_name"] for e in alias["examiners"]} | {"John"}

    # --- identifier integrity ------------------------------------------------
    bad = [r["relationship_id"] for r in rels if r["question_id"] not in inv]
    check("every relationship resolves to a live question", not bad, str(bad[:5]))

    bad = [r["relationship_id"] for r in rels
           if not (L.MEO / r["target_file"]).exists()]
    check("every relationship target file exists", not bad, str(bad[:5]))

    bad = [r["relationship_id"] for r in rels
           if r["target_anchor"] not in anchors.get(r["target_file"], set())]
    check("every relationship anchor exists", not bad, str(bad[:5]))

    dup = [k for k, v in Counter(r["relationship_id"] for r in rels).items() if v > 1]
    check("no duplicate relationship ids", not dup, str(dup[:5]))

    dup = [k for k, v in Counter(e["evidence_id"] for e in ev).items() if v > 1]
    check("no duplicate evidence ids", not dup, str(dup[:5]))

    rel_ids = {r["relationship_id"] for r in rels}
    bad = [e["evidence_id"] for e in ev if e["relationship_id"] not in rel_ids]
    check("every evidence record resolves to a relationship", not bad, str(bad[:5]))

    ref = {i for r in rels for i in r["evidence_ids"]}
    have = {e["evidence_id"] for e in ev}
    check("every referenced evidence id exists", ref <= have, str(sorted(ref - have)[:5]))

    bad = [r["relationship_id"] for r in rels if r["examiner"] not in known]
    check("every examiner resolves in the alias register", not bad, str(bad[:5]))

    # --- vocabulary ----------------------------------------------------------
    bad = sorted({r["research_best_tier"] for r in rels} - RESEARCH_TIERS)
    check("no impossible research tier values", not bad, str(bad))

    bad = sorted({r["relationship_type"] for r in rels} - RELATIONSHIP_TYPES)
    check("relationship type vocabulary is closed (relationships)", not bad, str(bad))

    bad = sorted({e["evidence_tier"] for e in ev} - EVIDENCE_TIERS)
    check("evidence tier vocabulary is closed", not bad, str(bad))

    bad = sorted({r["evidence_tier"] for r in recon} - EVIDENCE_TIERS)
    check("788 evidence tier vocabulary is closed", not bad, str(bad))

    # --- evidence provenance -------------------------------------------------
    # A tier is a claim about strength; source_type is where the record came
    # from. Validating the tier vocabulary alone lets a derived record be
    # relabelled PRIMARY_TRACKER and pass - the escape the Laptop found.
    bad = [e["evidence_id"] for e in ev if "source_type" not in e]
    check("every evidence record states its provenance", not bad, str(bad[:5]))

    bad = P.violations(ev)
    check("no evidence tier outruns its own provenance", not bad,
          "; ".join("%s: %s" % v for v in bad[:5]))

    derived = [e["evidence_id"] for e in ev
               if e.get("source_type") in P.DERIVED_SOURCE_TYPES
               and e.get("evidence_tier") in P.PRIMARY_TIERS]
    check("no derived or inferred record carries a primary evidence tier",
          not derived, str(derived[:5]))

    bad = sorted({r["relationship_type"] for r in recon} - RELATIONSHIP_TYPES)
    check("relationship type vocabulary is closed (788)", not bad, str(bad))

    # --- source accounting ---------------------------------------------------
    check("788 source occurrences ingested", len(src) == 788, "%d parsed" % len(src))

    src_ids = [s["source_id"] for s in src]
    dup = [k for k, v in Counter(src_ids).items() if v > 1]
    check("no duplicate source ids", not dup, str(dup[:5]))

    rec_ids = [r["source_id"] for r in recon]
    check("every source occurrence is dispositioned exactly once",
          sorted(rec_ids) == sorted(src_ids) and len(rec_ids) == len(set(rec_ids)),
          "%d source / %d dispositioned" % (len(src_ids), len(rec_ids)))

    bad = [r["source_id"] for r in recon
           if r["content_disposition"] not in CONTENT_DISPOSITIONS]
    check("one closed-vocabulary content disposition per occurrence", not bad, str(bad[:5]))

    bad = [r["source_id"] for r in recon
           if r["examiner_mapping_status"] not in MAPPING_STATUSES]
    check("one closed-vocabulary mapping status per occurrence", not bad, str(bad[:5]))

    bad = [r["source_id"] for r in recon
           if r["content_disposition"] != "MISSING" and r["matched_question_id"] is None]
    check("every non-MISSING occurrence carries a target", not bad, str(bad[:5]))

    bad = [r["source_id"] for r in recon
           if r["matched_question_id"] and r["matched_question_id"] not in inv]
    check("every matched question id resolves to live HTML", not bad, str(bad[:5]))

    fam_ids = {f["family_id"] for f in fams}
    bad = [r["source_id"] for r in recon if r["source_family_id"] not in fam_ids]
    check("every occurrence belongs to a known source family", not bad, str(bad[:5]))

    covered = {sid for f in fams for sid in f["source_ids"]}
    check("no source occurrence dropped by family clustering",
          covered == set(src_ids), "%d of %d covered" % (len(covered), len(src_ids)))

    # --- derived structures --------------------------------------------------
    bad = [g["gap_id"] for g in gaps
           if g["reuse_candidate"] and g["reuse_candidate"] not in inv]
    check("every gap reuse candidate resolves", not bad, str(bad[:5]))

    bad = [g["gap_id"] for g in gaps if g["source_family_id"] not in fam_ids]
    check("every gap resolves to a source family", not bad, str(bad[:5]))

    bad = [g["gap_id"] for g in gaps
           if not set(g["source_ids"]) <= set(src_ids)]
    check("every gap traces to real source occurrences", not bad, str(bad[:5]))

    bad = [r["canonical_question_id"] for r in ready
           if r["canonical_question_id"] not in inv]
    check("every ready connection resolves to a live question", not bad, str(bad[:5]))

    bad = [r["canonical_question_id"] for r in ready if r["examiner"] not in known]
    check("every ready-connection examiner resolves", not bad, str(bad[:5]))

    # --- counts are derived, never carried -----------------------------------
    summ = json.loads((OUT / "ORAL_788_RECONCILIATION_SUMMARY.json").read_text(encoding="utf-8"))
    live = dict(Counter(r["content_disposition"] for r in recon))
    check("summary dispositions recomputed from records",
          live == summ["content_dispositions"], "summary vs recount")

    matrix = (OUT / "ORAL_788_RECONCILIATION_MATRIX.md").read_text(encoding="utf-8")
    check("matrix reports the ingested total",
          "| Raw source occurrences ingested | 788 |" in matrix,
          "matrix headline total")

    # --- Phase 2A-ii: the Oral Notes secondary layer -------------------------
    # The Notes are a SECOND dimension, never a substitute for the canonical
    # one. These checks enforce that separation structurally: a note unit
    # cannot become a canonical question, a note cue cannot become tracker
    # evidence, and every Notes claim must resolve to a section that exists.
    n_units = jsonl("ORAL_NOTES_UNITS.jsonl")
    n_ev = jsonl("ORAL_NOTES_EXAMINER_EVIDENCE.jsonl")
    n_cov = jsonl("ORAL_NOTES_COVERAGE.jsonl")
    for name, obj in (("ORAL_NOTES_UNITS.jsonl", n_units),
                      ("ORAL_NOTES_EXAMINER_EVIDENCE.jsonl", n_ev),
                      ("ORAL_NOTES_COVERAGE.jsonl", n_cov)):
        check("input available: " + name, obj is not None,
              "missing" if obj is None else "%d records" % len(obj))

    if n_units is not None and n_ev is not None and n_cov is not None:
        inv_notes = json.loads((OUT / "ORAL_NOTES_INVENTORY.json").read_text(
            encoding="utf-8"))
        unit_ids = [u["note_unit_id"] for u in n_units]
        by_unit = {u["note_unit_id"]: u for u in n_units}

        dup = [k for k, v in Counter(unit_ids).items() if v > 1]
        check("no duplicate note unit ids", not dup, str(dup[:5]))

        bad = [u for u in unit_ids if N.is_canonical_shaped(u)]
        check("no note unit id is shaped like a canonical question id",
              not bad, str(bad[:5]))

        clash = sorted(set(unit_ids) & set(inv))
        check("no note unit id collides with a canonical question id",
              not clash, str(clash[:5]))

        # A Notes unit must never enter the canonical universe. The canonical
        # count is recomputed from the live HTML, never carried.
        #
        # This used to assert `len(inv) == 681`. That literal tested the corpus
        # size, not the Notes layer -- the two checks above already prove no
        # note unit reaches the canonical set. It fired the moment the Founder
        # published a legitimate 682nd question (QB1_K#q8), which is growth, not
        # leakage. What must never happen is a canonical question *vanishing*,
        # because live relationships point at it. Derive that from the recorded
        # audit inventory instead of freezing a number.
        recorded = {q["canonical_question_id"] for q in json.loads(
            (OUT / "CURRENT_ORAL_QB_INVENTORY.json").read_text(
                encoding="utf-8"))}
        lost = sorted(recorded - set(inv))
        check("no canonical question recorded by the audit has vanished",
              not lost, "%d lost: %s" % (len(lost), lost[:5]))
        check("the canonical universe admits no note unit",
              not (set(inv) & set(unit_ids)),
              "%d canonical questions" % len(inv))

        bad = [u["note_unit_id"] for u in n_units
               if not (N.NOTES_DIR / u["file"]).exists()]
        check("every note unit resolves to an existing notes file", not bad,
              str(bad[:5]))

        note_anchors = {}
        for u in n_units:
            if u["file"] not in note_anchors:
                h = (N.NOTES_DIR / u["file"]).read_text(
                    encoding="utf-8", errors="replace")
                note_anchors[u["file"]] = set(
                    re.findall(r'\sid="([^"]+)"', h))
        bad = [u["note_unit_id"] for u in n_units
               if u["anchor_authored"]
               and u["anchor"] not in note_anchors[u["file"]]]
        check("every authored note anchor exists on its page", not bad,
              str(bad[:5]))

        bad = [u["note_unit_id"] for u in n_units
               if u["parent_unit_id"] and u["parent_unit_id"] not in by_unit]
        check("every note child unit resolves to its parent", not bad,
              str(bad[:5]))

        bad = sorted({u["unit_level"] for u in n_units} - N.UNIT_LEVELS)
        check("note unit level vocabulary is closed", not bad, str(bad))

        excluded = {r["file"] for r in inv_notes["files"]
                    if r["role"] != N.ROLE_SUBSTANTIVE}
        bad = sorted({u["file"] for u in n_units} & excluded)
        check("no navigation or out-of-scope page contributes a note unit",
              not bad, str(bad))
        check("every notes page is classified",
              inv_notes["unclassified_pages"] == 0,
              "%d unclassified" % inv_notes["unclassified_pages"])

        # --- note examiner evidence ---------------------------------------
        dup = [k for k, v in Counter(e["evidence_id"] for e in n_ev).items()
               if v > 1]
        check("no duplicate note evidence ids", not dup, str(dup[:5]))

        bad = [e["evidence_id"] for e in n_ev
               if e["note_unit_id"] not in by_unit]
        check("every note evidence record resolves to a note unit", not bad,
              str(bad[:5]))

        bad = [e["evidence_id"] for e in n_ev if e["examiner"] not in known]
        check("every note evidence examiner resolves in the alias register",
              not bad, str(bad[:5]))

        bad = [e["evidence_id"] for e in n_ev
               if e["cue_disposition"] not in N.EXPLICIT_CUES]
        check("only explicit cues become note evidence", not bad, str(bad[:5]))

        bad = [e["evidence_id"] for e in n_ev
               if e.get("evidence_tier") != N.NOTE_EVIDENCE_TIER
               or e.get("source_type") != N.NOTE_SOURCE_TYPE]
        check("every note evidence record carries NOTE_EXPLICIT on note "
              "provenance", not bad, str(bad[:5]))

        bad = P.violations(n_ev)
        check("no note evidence tier outruns its own provenance", not bad,
              "; ".join("%s: %s" % v for v in bad[:5]))

        bad = [e["evidence_id"] for e in n_ev
               if e.get("evidence_tier") in P.PRIMARY_TIERS]
        check("no note evidence record carries a primary evidence tier",
              not bad, str(bad[:5]))

        bad = [e["evidence_id"] for e in n_ev
               if not str(e.get("evidence_excerpt") or "").strip()]
        check("every note evidence record carries a source excerpt", not bad,
              str(bad[:5]))

        # --- note coverage --------------------------------------------------
        cov_ids = [c["source_id"] for c in n_cov]
        check("every source occurrence has exactly one Notes coverage record",
              sorted(cov_ids) == sorted(s["source_id"] for s in src),
              "%d coverage / %d source" % (len(cov_ids), len(src)))

        bad = sorted({c["notes_support"] for c in n_cov}
                     - set(C.SUPPORT_TIERS))
        check("Notes support vocabulary is closed", not bad, str(bad))

        bad = sorted({c["notes_support"] for c in n_cov}
                     & C.CANONICAL_DISPOSITIONS)
        check("no Notes support tier reuses a canonical disposition", not bad,
              str(bad))

        bad = [c["source_id"] for c in n_cov for h in c["notes_units"]
               if h["note_unit_id"] not in by_unit]
        check("every Notes coverage claim resolves to a note unit", not bad,
              str(bad[:5]))

        bad = [c["source_id"] for c in n_cov for h in c["notes_units"]
               if not str(h.get("section_title") or "").strip()
               and not str(h.get("anchor") or "").strip()]
        check("every Notes coverage claim names a section or anchor", not bad,
              str(bad[:5]))

        bad = [c["source_id"] for c in n_cov
               if c["notes_support"] != C.NO_SUPPORT and not c["notes_units"]]
        check("no Notes support without a supporting unit", not bad,
              str(bad[:5]))

        bad = [c["source_id"] for c in n_cov for u in
               c["notes_units_naming_this_examiner"] if u not in by_unit]
        check("every examiner-cued unit reference resolves", not bad,
              str(bad[:5]))

    # --- Phase 2A-iii final package ------------------------------------------
    # The final datasets are what a production session and the index generator
    # will read. An error here is not a reporting error, it is a wrong answer
    # or a wrong connection in front of a candidate.
    final = jsonl("FINAL_788_PRODUCTION_DISPOSITION.jsonl")
    if final is None:
        check("final 788 production dataset present", False,
              "FINAL_788_PRODUCTION_DISPOSITION.jsonl missing")
    else:
        src_ids = {r["source_id"] for r in src}
        fin_ids = [r["source_id"] for r in final]
        check("every source occurrence reaches the final dataset",
              set(fin_ids) == src_ids and len(fin_ids) == len(src_ids),
              "final %d vs source %d" % (len(fin_ids), len(src_ids)))
        check("no duplicate source occurrence in the final dataset",
              len(fin_ids) == len(set(fin_ids)),
              str([k for k, v in Counter(fin_ids).items() if v > 1][:5]))

        bad = [r["source_id"] for r in final
               if r["content_disposition"] not in CONTENT_DISPOSITIONS]
        check("every final row carries exactly one known content disposition",
              not bad, str(bad[:5]))

        bad = [r["source_id"] for r in final
               if r["notes_support"] not in C.SUPPORT_TIERS]
        check("every final row carries exactly one known Notes support tier",
              not bad, str(bad[:5]))

        bad = [r["source_id"] for r in final
               if r["examiner_mapping_status"] not in MAPPING_STATUSES]
        check("every final row carries a valid examiner mapping status",
              not bad, str(bad[:5]))

        bad = [r["source_id"] for r in final
               if r["production_action"] not in PRODUCTION_ACTIONS]
        check("every final row carries exactly one production action",
              not bad, str(bad[:5]))

        # A MISSING ask over complete Notes is a promotion. Calling it a new
        # answer would have a production session research from zero material
        # MIW already holds, which is the specific waste this layer exists to
        # prevent.
        bad = [r["source_id"] for r in final
               if r["content_disposition"] == "MISSING"
               and r["notes_support"] in ("NOTES_COMPLETE_SUPPORT",
                                          "NOTES_STRONG_SUPPORT")
               and r["production_action"] != "NOTES_TO_QB_PROMOTION"]
        check("a MISSING ask over strong Notes is a promotion, not a new answer",
              not bad, str(bad[:5]))

        bad = [r["source_id"] for r in final
               if r["matched_question_id"] and r["matched_question_id"] not in inv]
        check("every final canonical target resolves to a live question",
              not bad, str(bad[:5]))

    rel = jsonobj("RELEASE_A_CONNECTIONS.json")
    if rel is None:
        check("Release-A dataset present", False,
              "RELEASE_A_CONNECTIONS.json missing")
    else:
        conns = rel["connections"]
        keys = [(c["examiner"], c["canonical_question_id"]) for c in conns]
        check("no duplicate Release-A relationship",
              len(keys) == len(set(keys)),
              str([k for k, v in Counter(keys).items() if v > 1][:5]))
        check("Release-A pair count matches its own records",
              rel["unique_pairs"] == len(conns),
              "%s vs %d" % (rel["unique_pairs"], len(conns)))

        bad = [c["relation_id"] for c in conns
               if c["canonical_question_id"] not in inv]
        check("every Release-A target resolves to a live question", not bad,
              str(bad[:5]))
        bad = [c["relation_id"] for c in conns
               if c["anchor"] not in anchors.get(c["file"], set())]
        check("every Release-A target anchor exists on its page", not bad,
              str(bad[:5]))
        bad = [c["relation_id"] for c in conns if not c["examiner"]
               or c["examiner"] not in known]
        check("every Release-A examiner resolves in the alias register",
              not bad, str(bad[:5]))

        # The two exclusions the review made conditions of authorising a
        # release at all.
        bad = [c["relation_id"] for c in conns
               if c["strongest_evidence_tier"] in ("TOPIC_INFERRED",
                                                   "NOTE_WEAK_MENTION")]
        check("no Release-A relationship rests on inference alone", not bad,
              str(bad[:5]))
        bad = [c["relation_id"] for c in conns
               if c["strongest_evidence_tier"] in ("CURRENT_INDEX_RECOVERY",
                                                   "JULY_DERIVED_SIBLING",
                                                   "CE_TIP")]
        check("no Release-A relationship rests on a derived or page-declared "
              "source alone", not bad, str(bad[:5]))

        # The evidence universe a Release-A id may point into. The final review
        # found this check vacuous because the research rows carried no ids;
        # it was ALSO wrong-by-construction, because it never admitted the
        # V1 ledger (MASTER-AQ / JULY-*) or the 788 source records (ASC-*),
        # which is where the primary and external evidence actually lives.
        ev_ids = ({e["evidence_id"] for e in ev}
                  | {e["evidence_id"] for e in
                     (jsonl("ORAL_NOTES_EXAMINER_EVIDENCE.jsonl") or [])}
                  | {e["evidence_id"] for e in
                     (jsonl("EXAMINER_EVIDENCE_LEDGER.jsonl") or [])}
                  | {r["source_id"] for r in src})
        bad = [c["relation_id"] for c in conns
               for e in c["evidence_ids"] if e not in ev_ids]
        check("every Release-A evidence id resolves to an evidence record",
              not bad, str(bad[:5]))

        if final is not None:
            fin_ids = {r["source_id"] for r in final}
            bad = [c["relation_id"] for c in conns
                   for sid in c["source_occurrence_ids"] if sid not in fin_ids]
            check("every Release-A source occurrence resolves", not bad,
                  str(bad[:5]))
            # A pair carried by the compilation must actually hold an EXACT or
            # NEAR row; a SAME_CORE row may not carry one on its own.
            by_sid = {r["source_id"]: r for r in final}
            bad = []
            for c in conns:
                if c["strongest_evidence_tier"] != "EXTERNAL_SOURCE_CONFIRMED":
                    continue
                d = [by_sid[s]["content_disposition"]
                     for s in c["source_occurrence_ids"] if s in by_sid]
                if not any(x in ("EXACT_MATCH", "NEAR_MATCH") for x in d):
                    bad.append(c["relation_id"])
            check("no Release-A pair rests on a SAME_CORE-only external row",
                  not bad, str(bad[:5]))

    # ------------------------------------------------------------ Release A
    # publication set (finalize_release_a.py). These are the checks the final
    # review asked for: real evidence ids, each resolving to a record that
    # names THIS examiner and THIS question, a tier derivable from those
    # records, and the two review-held pairs absent.
    pub = jsonobj("RELEASE_A_PUBLICATION.json")
    dec = jsonobj("RELEASE_A_REVIEW_DECISIONS.json")
    if pub is None or dec is None:
        check("Release-A publication set present", False,
              "RELEASE_A_PUBLICATION.json / RELEASE_A_REVIEW_DECISIONS.json missing")
    else:
        pconns = pub["connections"]
        held_ids = {h["relation_id"] for h in dec["held"]}
        pub_ids = [c["relation_id"] for c in pconns]
        check("no review-held Release-A pair is published",
              not (held_ids & set(pub_ids)), str(sorted(held_ids & set(pub_ids))))
        check("every review-held pair is recorded in RELEASE_A_HELD",
              held_ids <= {h["relation_id"] for h in
                           (jsonobj("RELEASE_A_HELD.json") or {"held": []})["held"]})
        pkeys = [(c["examiner"], c["canonical_question_id"]) for c in pconns]
        check("no duplicate published Release-A relationship",
              len(pkeys) == len(set(pkeys)),
              str([k for k, v in Counter(pkeys).items() if v > 1][:5]))
        check("published Release-A count matches its own records",
              pub["published_pairs"] == len(pconns)
              and pub["new_relationships"] == sum(
                  1 for c in pconns if c["disposition"] == "NEW_RELATIONSHIP")
              and pub["evidence_for_existing"] == sum(
                  1 for c in pconns if c["disposition"] == "EVIDENCE_FOR_EXISTING"),
              "%s/%s/%s vs %d" % (pub["published_pairs"], pub["new_relationships"],
                                  pub["evidence_for_existing"], len(pconns)))
        check("published Release-A composition matches its own records",
              pub["composition_published"] == dict(sorted(Counter(
                  c["strongest_evidence_tier"] for c in pconns).items())))

        bad = [c["relation_id"] for c in pconns
               if c["canonical_question_id"] not in inv]
        check("every published Release-A target resolves to a live question",
              not bad, str(bad[:5]))
        bad = [c["relation_id"] for c in pconns
               if c["anchor"] not in anchors.get(c["file"], set())]
        check("every published Release-A anchor exists on its page",
              not bad, str(bad[:5]))

        bad = [c["relation_id"] for c in pconns if not c["evidence_ids"]]
        check("every published Release-A relationship carries evidence ids",
              not bad, str(bad[:5]))
        bad = [c["relation_id"] for c in pconns
               if c["evidence_ids"] != sorted(set(c["evidence_ids"]))]
        check("published Release-A evidence ids are unique and stably ordered",
              not bad, str(bad[:5]))

        # Resolution AND back-reference: an id must exist and its record must
        # name this examiner and this question with the strength its bucket
        # claims. Anything less is a pointer, not evidence.
        v1 = {e["evidence_id"]: e for e in
              (jsonl("EXAMINER_EVIDENCE_LEDGER.jsonl") or [])}
        fin = {r["source_id"]: r for r in (final or [])}
        nev = {e["evidence_id"]: e for e in
               (jsonl("ORAL_NOTES_EXAMINER_EVIDENCE.jsonl") or [])}
        rev_pairs = set()
        rev = jsonobj("ORAL_NOTES_REVERSE_CONNECTIONS.json")
        for r in (rev or {"rows": []})["rows"]:
            for u in r.get("note_units", []):
                rev_pairs.add((r["examiner"], r.get("canonical_question_id"), u))
        unresolved, misattributed = [], []
        for c in pconns:
            ex, qid = c["examiner"], c["canonical_question_id"]
            for eid in c["evidence_ids"]:
                if eid in v1:
                    r = v1[eid]
                    if not (r["examiner_normalized"] == ex
                            and r.get("canonical_question_id") == qid
                            and r.get("legacy_mapping") in ("VERIFIED_MATCH",
                                                            "VERIFIED_SAME_CORE")):
                        misattributed.append((c["relation_id"], eid))
                elif eid in fin:
                    r = fin[eid]
                    if not (r["examiner"] == ex
                            and r.get("matched_question_id") == qid
                            and r["content_disposition"] in ("EXACT_MATCH",
                                                             "NEAR_MATCH")):
                        misattributed.append((c["relation_id"], eid))
                elif eid in nev:
                    r = nev[eid]
                    if not (r["examiner"] == ex
                            and (ex, qid, r["note_unit_id"]) in rev_pairs):
                        misattributed.append((c["relation_id"], eid))
                else:
                    unresolved.append((c["relation_id"], eid))
        check("every published Release-A evidence id resolves to a record",
              not unresolved, str(unresolved[:5]))
        check("every published Release-A evidence record names its own "
              "examiner and question", not misattributed, str(misattributed[:5]))

        # Tier is derivable from the evidence, not carried as a string.
        rank = {"NOTE_EXPLICIT": 3, "EXTERNAL_SOURCE_CONFIRMED": 4,
                "PRIMARY_TRACKER": 5}
        bad = []
        for c in pconns:
            tiers = []
            if any(e in v1 and v1[e]["evidence_class"] == "PRIMARY_CANDIDATE_RECORD"
                   for e in c["evidence_ids"]):
                tiers.append("PRIMARY_TRACKER")
            if any(e in fin for e in c["evidence_ids"]):
                tiers.append("EXTERNAL_SOURCE_CONFIRMED")
            if any(e in nev for e in c["evidence_ids"]):
                tiers.append("NOTE_EXPLICIT")
            derived = max(tiers, key=rank.get) if tiers else None
            if derived != c["strongest_evidence_tier"]:
                bad.append((c["relation_id"], c["strongest_evidence_tier"], derived))
        check("every published Release-A tier is derivable from its evidence ids",
              not bad, str(bad[:5]))
        bad = [c["relation_id"] for c in pconns
               if rank.get(c["strongest_evidence_tier"], -1) < 3]
        check("every published Release-A relationship sits at or above the "
              "release floor", not bad, str(bad[:5]))

        cur_by_id = {r["relationship_id"]: r for r in rels}
        cur_keys = {(r["examiner"], r["question_id"]) for r in rels}
        bad = [c["relation_id"] for c in pconns
               if c["disposition"] == "NEW_RELATIONSHIP"
               and (c["examiner"], c["canonical_question_id"]) in cur_keys]
        check("no published NEW Release-A relationship duplicates a current "
              "index relationship", not bad, str(bad[:5]))
        bad = [c["relation_id"] for c in pconns
               if c["disposition"] == "EVIDENCE_FOR_EXISTING"
               and (c["existing_relationship_id"] not in cur_by_id
                    or (cur_by_id[c["existing_relationship_id"]]["examiner"],
                        cur_by_id[c["existing_relationship_id"]]["question_id"])
                    != (c["examiner"], c["canonical_question_id"]))]
        check("every EVIDENCE_FOR_EXISTING Release-A row points at the matching "
              "current relationship", not bad, str(bad[:5]))

    p0 = jsonobj("FINAL_P0_PRODUCTION_BATCH.json")
    if p0 is None:
        check("final P0 batch present", False,
              "FINAL_P0_PRODUCTION_BATCH.json missing")
    else:
        items = p0["items"]
        ids = [i["production_id"] for i in items]
        check("every P0 production id is unique", len(ids) == len(set(ids)),
              str([k for k, v in Counter(ids).items() if v > 1][:5]))
        fams = [i["gap_id"] for i in items]
        check("no duplicate P0 production family",
              len(fams) == len(set(fams)),
              str([k for k, v in Counter(fams).items() if v > 1][:5]))
        check("P0 count matches its own records", p0["p0_count"] == len(items),
              "%s vs %d" % (p0["p0_count"], len(items)))
        bad = [i["production_id"] for i in items
               if i["production_action"] not in P0_ACTIONS]
        check("every P0 item carries exactly one production action", not bad,
              str(bad[:5]))
        if final is not None:
            fin_ids = {r["source_id"] for r in final}
            bad = [i["production_id"] for i in items
                   for s in i["source_occurrence_ids"] if s not in fin_ids]
            check("every P0 source occurrence resolves", not bad, str(bad[:5]))
        bad = [i["production_id"] for i in items
               if i["current_closest_qb"] and i["current_closest_qb"] not in inv]
        check("every P0 reuse target resolves to a live question", not bad,
              str(bad[:5]))
        # A merged family may not also stand as its own P0 item.
        merged = set(p0["merged_families"])
        bad = [i["production_id"] for i in items if i["gap_id"] in merged]
        check("no merged family also ships as its own P0 item", not bad,
              str(bad[:5]))

    # --- boundary: this phase writes no live candidate page ------------------
    check("research outputs stay inside the audit folder",
          OUT.name == "examiner-audit" and OUT.parent.name == "oral-intelligence",
          # repo-relative, with forward slashes: the absolute form wrote the
          # producer's own drive and user name into a committed artefact, so the
          # same run on another machine produced a different file
          OUT.relative_to(L.REPO).as_posix())
    stray = [p.name for p in OUT.glob("*")
             if p.suffix.lower() in (".html", ".htm")]
    check("no HTML page written into the research folder", not stray, str(stray[:5]))

    return emit()


def emit():
    n_pass = sum(1 for r in results if r["status"] == "PASS")
    n_fail = len(results) - n_pass
    L.jdump({"passed": n_pass, "failed": n_fail, "checks": results},
            "PHASE2_VALIDATION_RESULTS.json")
    for r in results:
        print("%-5s %s %s" % (r["status"], r["check"],
                              ("- " + r["detail"]) if r["status"] == "FAIL" else ""))
    print("\n%d PASS / %d FAIL" % (n_pass, n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
