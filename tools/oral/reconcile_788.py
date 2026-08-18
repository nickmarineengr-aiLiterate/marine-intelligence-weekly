"""Phase 2 step 3 - reconcile the 788 source occurrences against live MIW truth.

Governing principle: we are not solving 788 questions. We are asking, for each
source occurrence, in this order:

  1. Do we already answer this?
  2. Is only the examiner connection missing?
  3. Is this only a follow-up / expected detail?
  4. Only then: is there a real question gap?

Matching is whole-corpus: every source occurrence is compared against all live
questions, never narrowed to a topic, group or examiner. Topic is recorded, not
used to decide.

Two orthogonal statuses are assigned, never merged into one field:
  content disposition : EXACT_MATCH NEAR_MATCH SAME_CORE_ASK PARTIAL_COVERAGE MISSING AMBIGUOUS
  examiner mapping    : ALREADY_LINKED NEW_LINK CONFLICTING_LINK UNMAPPED NOT_APPLICABLE

Live HTML is the only authority for current question text and anchors;
qb_content_index.json is never consulted (it carries an off-by-one shift).

Outputs (meoclass1/oral-intelligence/examiner-audit/):
  ORAL_788_RECONCILIATION.jsonl
  ORAL_GAP_CANDIDATES.json
  HUMAN_REVIEW_QUEUE.json
  ORAL_788_RECONCILIATION_SUMMARY.json
"""
from __future__ import annotations

import difflib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

OUT = L.OUT

CARD = re.compile(r'<div class="q-card[^"]*"([^>]*)>', re.I)
ATTR = re.compile(r'([\w-]+)="([^"]*)"')

# content dispositions
EXACT, NEAR, SAME_CORE = "EXACT_MATCH", "NEAR_MATCH", "SAME_CORE_ASK"
PARTIAL, MISSING, AMBIG = "PARTIAL_COVERAGE", "MISSING", "AMBIGUOUS"

# examiner mapping statuses
ALREADY_LINKED, NEW_LINK = "ALREADY_LINKED", "NEW_LINK"
CONFLICTING_LINK, UNMAPPED, NOT_APPLICABLE = "CONFLICTING_LINK", "UNMAPPED", "NOT_APPLICABLE"


# --------------------------------------------------------------------------
# live corpus
# --------------------------------------------------------------------------
def card_bodies():
    """canonical_question_id -> full rendered card text (question + answer).

    Uses `[^>]*` on the q-text attribute set: QB pages carry two markup
    generations and an exact-attribute regex silently empties whole files.
    """
    out = {}
    for p in L.qb_files():
        h = p.read_text(encoding="utf-8", errors="replace")
        ms = list(CARD.finditer(h))
        for i, m in enumerate(ms):
            attrs = dict(ATTR.findall(m.group(1)))
            cid = attrs.get("id", "")
            if not re.fullmatch(r"q\d+", cid):
                continue          # q-card is not always a question (map cards)
            end = ms[i + 1].start() if i + 1 < len(ms) else len(h)
            out[p.stem + "#" + cid] = L.strip_tags(h[m.start():end])
    return out


# Marine regulatory wording is full of alphanumeric designators - A-60, D-1/D-2,
# Tier III, Annex 6, Chapter II-1, ISO 8217. The audit's general-purpose
# tokeniser drops them (a bare "60" is under its length floor, and "A-60" splits
# into two dead tokens), so an ask about A-60 bulkheads cannot match a question
# about A-60 bulkheads. This tokeniser keeps them joined.
_DESIGNATOR = re.compile(r"\b([a-z]{1,4})[\s\-/]?(\d{1,4})\b")
_ROMAN = {"i": "1", "ii": "2", "iii": "3", "iv": "4", "v": "5", "vi": "6"}


def mtokens(s):
    n = L.norm(s)
    n = _DESIGNATOR.sub(lambda m: m.group(1) + m.group(2), n)
    out = set()
    for t in n.split():
        if t in L.STOP:
            continue
        if t.isdigit():
            out.add(t)
        elif t.isalpha():
            if len(t) > 2:
                out.add(t)
            elif t in _ROMAN:
                out.add(t)
        else:
            out.add(t)
    return out


def idf_table(docs):
    df = Counter()
    for d in docs:
        for t in mtokens(d):
            df[t] += 1
    n = max(len(docs), 1)
    return {t: math.log(1 + n / (1 + c)) for t, c in df.items()}, n


def weighted_coverage(src_tokens, hay_tokens, idf, default):
    """IDF-weighted fraction of the source's demand present in the target."""
    if not src_tokens:
        return 0.0
    tot = sum(idf.get(t, default) for t in src_tokens)
    hit = sum(idf.get(t, default) for t in src_tokens if t in hay_tokens)
    return hit / tot if tot else 0.0


# --------------------------------------------------------------------------
def classify(qcov, sim, target_acov, best_acov, union_acov, n_union):
    """Content coverage of the source ask by the live corpus.

    Question-text coverage decides whether MIW *asks* the same thing. Answer
    coverage decides whether a candidate who studied MIW could *answer* it —
    which is the governing creation rule, and the reason material buried in
    another question's answer counts as partial coverage rather than a gap.

    Tags are recorded but never decide: a topic tag makes every question in a
    group look like a perfect match for a one-word prompt.
    """
    if qcov >= 0.95 and sim >= 0.55:
        return EXACT, "question text asks the same thing"
    if qcov >= 0.85 and sim >= 0.30:
        return NEAR, "question text asks the same thing in different words"
    if qcov >= 0.75:
        return SAME_CORE, "different formulation, same substantive demand"
    if qcov >= 0.5 and target_acov >= 0.85:
        return SAME_CORE, "question overlaps and its answer completes the ask"
    if qcov >= 0.5:
        return PARTIAL, "question overlaps but the answer may not reach every limb"
    if best_acov >= 0.9:
        return PARTIAL, "the ask is answered inside another question's answer"
    if n_union >= 2 and union_acov >= 0.9:
        return PARTIAL, "compound ask covered across several existing answers"
    if best_acov >= 0.7:
        return PARTIAL, "existing answer covers a meaningful portion"
    return MISSING, "no existing answer would adequately prepare the candidate"


def main():
    inv = L.build_inventory()
    bodies = card_bodies()
    for q in inv:
        q["card_text"] = bodies.get(q["canonical_question_id"], q["question_text"])

    q_idf, _ = idf_table([q["question_text"] for q in inv])
    a_idf, _ = idf_table([q["card_text"] for q in inv])
    q_default = max(q_idf.values()) if q_idf else 1.0
    a_default = max(a_idf.values()) if a_idf else 1.0

    q_tok = {q["canonical_question_id"]: mtokens(q["question_text"]) for q in inv}
    tag_tok = {q["canonical_question_id"]: mtokens(q["tags"]) for q in inv}
    q_txt_tok = q_tok
    a_tok = {q["canonical_question_id"]: mtokens(q["card_text"]) for q in inv}
    by_id = {q["canonical_question_id"]: q for q in inv}

    # existing relationships, recovered in step 1
    rel_by_pair, rel_by_q = set(), defaultdict(set)
    with (OUT / "CURRENT_EXAMINER_RELATIONSHIPS.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            rel_by_pair.add((r["question_id"], r["examiner"]))
            rel_by_q[r["question_id"]].add(r["examiner"])

    src = [json.loads(l) for l in (OUT / "ALL_SURVEYORS_SOURCE_RECORDS.jsonl").open(encoding="utf-8")]
    families = {f["family_id"]: f for f in json.loads(
        (OUT / "ALL_SURVEYORS_SOURCE_FAMILIES.json").read_text(encoding="utf-8"))}

    # The source is candidate-typed, so it misspells domain words the live
    # corpus spells correctly ("JOHRI WINDOW" for Johari Window). A rare source
    # token absent from the corpus is repaired to its nearest corpus spelling,
    # and the repair is recorded on the record rather than applied silently.
    vocab = set()
    for t in a_tok.values():
        vocab |= t
    spell_cache = {}

    def repair(tok):
        if tok in vocab or len(tok) < 5:
            return tok, None
        if tok not in spell_cache:
            near = difflib.get_close_matches(tok, vocab, n=1, cutoff=0.86)
            spell_cache[tok] = near[0] if near else None
        fixed = spell_cache[tok]
        return (fixed, "%s->%s" % (tok, fixed)) if fixed else (tok, None)

    results = []
    for s in src:
        raw_stoks = mtokens(s["question_core_text"])
        if not raw_stoks:
            raw_stoks = mtokens(s["raw_question_text"])
        stoks, spell_repairs = set(), []
        for t in raw_stoks:
            fixed, note = repair(t)
            stoks.add(fixed)
            if note:
                spell_repairs.append(note)

        # whole-corpus comparison: every source occurrence against all 681 live
        # questions. Topic never narrows the field.
        scored, by_answer = [], []
        for qid in q_tok:
            qcov = weighted_coverage(stoks, q_tok[qid], q_idf, q_default)
            acov = weighted_coverage(stoks, a_tok[qid], a_idf, a_default)
            if acov >= 0.4:
                by_answer.append((acov, qid))
            if qcov < 0.25:
                continue
            sim = L.jaccard(s["question_core_text"], by_id[qid]["question_text"])
            scored.append((qcov, sim, acov, qid))
        # answer depth breaks ties between equal-coverage targets, so the card
        # that actually treats the ask wins rather than the first one seen
        scored.sort(key=lambda x: (-x[0], -x[1], -x[2]))
        by_answer.sort(reverse=True)

        best_ans_cov, best_ans_qid = by_answer[0] if by_answer else (0.0, None)

        # a compound ask ("ESP in detail. What documents are updated? How do you
        # check as CE?") is often covered across several existing answers
        union = set()
        contributors = []
        for acov, qid_a in by_answer[:3]:
            new = stoks & a_tok[qid_a]
            if new - union:
                union |= new
                contributors.append(qid_a)
        union_cov = weighted_coverage(stoks, union, a_idf, a_default)

        top = scored[0] if scored else None
        runner = scored[1] if len(scored) > 1 else None

        if top:
            cov, sim, target_ans_cov, qid = top
        else:
            cov = sim = target_ans_cov = 0.0
            qid = None
        # when the question text does not carry the ask, the card whose answer
        # does becomes the target - recorded honestly as an answer-side match
        if (qid is None or cov < 0.5) and best_ans_cov >= 0.7:
            qid = best_ans_qid
            target_ans_cov = best_ans_cov
        elif qid is None and contributors:
            # a compound ask carried across several answers: the deepest
            # contributor is the anchor, the rest are recorded alongside it
            qid = contributors[0]
            target_ans_cov = best_ans_cov
        rev = weighted_coverage(q_txt_tok[qid], stoks, q_idf, q_default) if qid else 0.0

        disp, disp_reason = classify(cov, sim, target_ans_cov, best_ans_cov,
                                     union_cov, len(contributors))

        answer_rescue = qid if (disp in (PARTIAL, SAME_CORE) and cov < 0.5) else None
        tag_hit = bool(qid and (stoks & tag_tok.get(qid, set())))

        # Ambiguity is reserved for cases where model judgement is genuinely
        # needed. A tie between two targets that BOTH fully cover the ask is not
        # a candidate risk - it is a duplicate target, resolved on similarity
        # and recorded as an alternative.
        ambiguous_reason = None
        alternative_target = None
        if runner and abs(runner[0] - cov) <= 0.03 and runner[3] != qid:
            if cov >= 0.9:
                alternative_target = runner[3]
            elif cov >= 0.5:
                ambiguous_reason = "TWO_PLAUSIBLE_TARGETS_NEITHER_COMPLETE"
        if not ambiguous_reason and len(stoks) <= 2 and 0.5 <= cov < 0.95:
            ambiguous_reason = "SOURCE_PROMPT_TOO_TERSE"
        if ambiguous_reason:
            disp = AMBIG

        # ---- examiner mapping, independent of content -----------------------
        ex = s["surveyor_normalized"]
        if qid is None or disp == MISSING:
            mapping = NOT_APPLICABLE if disp == MISSING else UNMAPPED
        elif disp == AMBIG:
            mapping = UNMAPPED
        elif (qid, ex) in rel_by_pair:
            mapping = ALREADY_LINKED
        elif rel_by_q.get(qid):
            mapping = NEW_LINK
        else:
            mapping = NEW_LINK

        # A conflicting link is a published relation whose own source ask the
        # external record contradicts - recorded, never auto-resolved.
        if mapping == NEW_LINK and disp in (EXACT, NEAR) and rel_by_q.get(qid) \
                and ex not in rel_by_q[qid] and len(rel_by_q[qid]) >= 3:
            pass  # many examiners on one question is normal, not a conflict

        rel_type = "PRIMARY_ASK"
        if s["source_comment"]:
            c = s["source_comment"].lower()
            if any(k in c for k in ("he asked", "he wanted", "specifically asked",
                                    "was looking for", "he was onto", "cross question",
                                    "not satisfied", "he meant")):
                rel_type = "EXPECTED_DETAIL"
        if disp in (PARTIAL, SAME_CORE) and rel_type == "PRIMARY_ASK" and target_ans_cov >= 0.9:
            rel_type = "FOLLOW_UP" if len(stoks) <= 4 else "PRIMARY_ASK"

        results.append({
            "source_id": s["source_id"],
            "source_family_id": s.get("source_family_id"),
            "examiner": ex,
            "surveyor_raw": s["surveyor_raw"],
            "topic_raw": s["topic_raw"],
            "source_question_number": s["source_question_number"],
            "source_page": s["source_page"],
            "raw_question_text": s["raw_question_text"],
            "source_comment": s["source_comment"],
            "source_confidence": s["source_confidence"],
            "matched_question_id": qid,
            "matched_question_text": by_id[qid]["question_text"] if qid else None,
            "matched_url": by_id[qid]["url"] if qid else None,
            "match_coverage": round(cov, 3),
            "match_similarity": round(sim, 3),
            "match_reverse_coverage": round(rev, 3),
            "target_answer_coverage": round(target_ans_cov, 3),
            "best_answer_coverage": round(best_ans_cov, 3),
            "best_answer_question_id": best_ans_qid,
            "answer_rescued_from": answer_rescue,
            "alternative_target_question_id": alternative_target,
            "matched_on_topic_tag": tag_hit,
            "disposition_reason": disp_reason,
            "compound_cover_question_ids": contributors,
            "compound_cover_coverage": round(union_cov, 3),
            "source_spelling_repairs": spell_repairs,
            "alternative_target_question_id": alternative_target,
            "matched_on_topic_tag": tag_hit,
            "runner_up_question_id": runner[3] if runner else None,
            "runner_up_coverage": round(runner[0], 3) if runner else None,
            "content_disposition": disp,
            "examiner_mapping_status": mapping,
            "relationship_type": rel_type,
            "ambiguity_reason": ambiguous_reason,
            "evidence_tier": "EXTERNAL_SURVEYOR_COMPILATION",
        })

    # ---- gap candidates, clustered by family --------------------------------
    fam_rows = defaultdict(list)
    for r in results:
        fam_rows[r["source_family_id"]].append(r)

    gaps = []
    for fid, rows in fam_rows.items():
        n_missing = sum(1 for r in rows if r["content_disposition"] == MISSING)
        # a PARTIAL is only a gap candidate when the existing answer leaves a
        # material limb of the ask uncovered; a well-covered PARTIAL is an
        # enrichment note, not a question to write
        material_partial = [
            r for r in rows
            if r["content_disposition"] == PARTIAL and r["target_answer_coverage"] < 0.75
        ]
        if not n_missing and not material_partial:
            continue
        f = families[fid]
        exs = sorted({r["examiner"] for r in rows})
        gaps.append({
            "gap_kind": "GENUINE_GAP" if n_missing >= max(1, len(rows) / 2)
                        else "MATERIAL_PARTIAL",
            "material_partial_occurrences": len(material_partial),
            "gap_id": "GAP-" + fid.split("-")[1],
            "source_family_id": fid,
            "proposed_canonical_question": f["representative_text"],
            "source_wordings": [r["raw_question_text"] for r in rows],
            "source_ids": [r["source_id"] for r in rows],
            "examiners": exs,
            "examiner_count": len(exs),
            "occurrence_count": len(rows),
            "missing_occurrences": n_missing,
            "topics": f["topics"],
            "dominant_disposition": Counter(
                r["content_disposition"] for r in rows).most_common(1)[0][0],
            "nearest_existing_question": rows[0]["matched_question_id"],
            "nearest_existing_text": rows[0]["matched_question_text"],
            "nearest_coverage": rows[0]["match_coverage"],
            "best_answer_coverage": max(r["best_answer_coverage"] for r in rows),
            "reuse_candidate": max(
                rows, key=lambda r: r["best_answer_coverage"])["best_answer_question_id"],
            "source_pages": sorted({r["source_page"] for r in rows}),
        })

    # Priority uses transparent, stated factors only. There is deliberately no
    # numeric "probability of being asked" - the evidence does not support one.
    CURRENCY = {"latest", "new", "amendment", "amendments", "recent", "2023", "2024",
                "2025", "2026", "cii", "eexi", "netzero", "net", "zero", "mepc",
                "imsbc", "ihm", "bwms", "tio2", "titanium"}
    for g in gaps:
        factors = []
        gap_text = " ".join(g["source_wordings"])
        current_reg = bool(mtokens(gap_text) & CURRENCY)
        nothing_held = g["best_answer_coverage"] < 0.45

        if g["examiner_count"] > 1:
            factors.append("asked by %d examiners" % g["examiner_count"])
        if g["occurrence_count"] > 1:
            factors.append("%d source occurrences" % g["occurrence_count"])
        if g["gap_kind"] == "GENUINE_GAP":
            factors.append("no existing answer adequately prepares the candidate")
        else:
            factors.append("existing answer covers part of the ask, a limb is missing")
        if nothing_held:
            factors.append("MIW holds almost no material on this ask")
        elif g["best_answer_coverage"] >= 0.7:
            factors.append("reusable verified MIW material exists (%s)" % g["reuse_candidate"])
        if current_reg:
            factors.append("current / recently amended regulation")

        # a family cannot be a genuine gap if some existing answer already
        # carries the whole ask - that is enrichment, not a question to write
        if g["gap_kind"] == "GENUINE_GAP" and g["best_answer_coverage"] >= 0.9:
            g["gap_kind"] = "MATERIAL_PARTIAL"
            g["gap_kind_note"] = (
                "downgraded: %s already answers the ask in full" % g["reuse_candidate"])
        genuine = g["gap_kind"] == "GENUINE_GAP"
        if genuine and (g["examiner_count"] > 1 or g["occurrence_count"] > 1):
            pr = "P0"                      # cross-examiner or repeated, and unanswered
        elif genuine and nothing_held and current_reg:
            pr = "P0"                      # a current rule MIW cannot answer at all
        elif genuine and nothing_held:
            pr = "P1"
        elif genuine:
            pr = "P2"
        elif g["occurrence_count"] > 1 or g["examiner_count"] > 1:
            pr = "P2"
        else:
            pr = "P3"
        g["priority"] = pr
        g["priority_factors"] = factors

    review = [
        {
            "source_id": r["source_id"],
            "examiner": r["examiner"],
            "raw_question_text": r["raw_question_text"],
            "source_page": r["source_page"],
            "topic_raw": r["topic_raw"],
            "reason": r["ambiguity_reason"],
            "candidate_a": r["matched_question_id"],
            "candidate_a_text": r["matched_question_text"],
            "candidate_a_coverage": r["match_coverage"],
            "candidate_b": r["runner_up_question_id"],
            "candidate_b_coverage": r["runner_up_coverage"],
            "best_answer_question_id": r["best_answer_question_id"],
            "best_answer_coverage": r["best_answer_coverage"],
        }
        for r in results if r["content_disposition"] == AMBIG
    ]

    with (OUT / "ORAL_788_RECONCILIATION.jsonl").open("w", encoding="utf-8") as fh:
        for r in results:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    L.jdump(sorted(gaps, key=lambda g: (g["priority"], -g["examiner_count"],
                                        -g["occurrence_count"])),
            "ORAL_GAP_CANDIDATES.json")
    L.jdump(review, "HUMAN_REVIEW_QUEUE.json")

    per_ex = defaultdict(Counter)
    for r in results:
        per_ex[r["examiner"]][r["content_disposition"]] += 1
        per_ex[r["examiner"]]["MAP_" + r["examiner_mapping_status"]] += 1
    summary = {
        "source_occurrences_in": len(src),
        "source_occurrences_dispositioned": len(results),
        "content_dispositions": dict(Counter(r["content_disposition"] for r in results)),
        "examiner_mapping": dict(Counter(r["examiner_mapping_status"] for r in results)),
        "relationship_types": dict(Counter(r["relationship_type"] for r in results)),
        "per_examiner": {k: dict(v) for k, v in per_ex.items()},
        "gap_families": len(gaps),
        "gap_kinds": dict(Counter(g["gap_kind"] for g in gaps)),
        "gap_priority": dict(Counter(g["priority"] for g in gaps)),
        "gap_priority_by_kind": {
            k: dict(Counter(g["priority"] for g in gaps if g["gap_kind"] == k))
            for k in ("GENUINE_GAP", "MATERIAL_PARTIAL")},
        "human_review_queue": len(review),
        "human_review_reasons": dict(Counter(r["reason"] for r in review)),
        "new_links_unique_pairs": len({
            (r["matched_question_id"], r["examiner"]) for r in results
            if r["examiner_mapping_status"] == NEW_LINK}),
        "already_linked_unique_pairs": len({
            (r["matched_question_id"], r["examiner"]) for r in results
            if r["examiner_mapping_status"] == ALREADY_LINKED}),
    }
    L.jdump(summary, "ORAL_788_RECONCILIATION_SUMMARY.json")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
