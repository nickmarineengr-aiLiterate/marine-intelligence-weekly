"""Notes support for a source ask - a SECOND, separate dimension.

A source occurrence has two independent dimensions:

    CANONICAL QB COVERAGE      what MIW asks as a canonical question
    NOTES SUPPORT              what else MIW already knows

They are graded on different vocabularies and neither may be read as the
other. `QB: MISSING` with `NOTES: COMPLETE_SUPPORT` means MIW holds the
knowledge but not yet as a canonical answer - a future NOTES_TO_QB_PROMOTION,
never "an EXACT QB match".

Three rules keep Notes support honest:

  1. Section-local only. The score is computed against one note unit, never a
     page. A 116 KB page mentions everything.

  2. Aboutness, not mention. Coverage of the ask by a unit's BODY says the
     words appear somewhere in it; coverage by the unit's TITLE says the unit
     is about the ask. A generic MARPOL note mentions a discharge limit in
     passing; a note titled for that limit answers it. Only the second may
     reach STRONG or COMPLETE.

  3. A question is not an answer. A unit that only poses a written-exam prompt
     can evidence that MIW knows the topic is examinable, never that MIW holds
     the answer, and is capped accordingly.

Thresholds here are the Notes layer's own. They are deliberately NOT the
canonical matcher's, and nothing in this module changes SAME_CORE admission.

Portability: no paths beyond oral_lib's repo-relative OUT. Import-only helpers.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
import oral_text as T  # noqa: E402
import oral_notes as N  # noqa: E402

# --------------------------------------------------------------------------
# the Notes support vocabulary - deliberately disjoint from the canonical one
# --------------------------------------------------------------------------
NO_SUPPORT = "NO_NOTES_SUPPORT"
TOPIC_SUPPORT = "NOTES_TOPIC_SUPPORT"
PARTIAL_SUPPORT = "NOTES_PARTIAL_SUPPORT"
STRONG_SUPPORT = "NOTES_STRONG_SUPPORT"
COMPLETE_SUPPORT = "NOTES_COMPLETE_SUPPORT"

SUPPORT_TIERS = [NO_SUPPORT, TOPIC_SUPPORT, PARTIAL_SUPPORT,
                 STRONG_SUPPORT, COMPLETE_SUPPORT]
SUPPORT_RANK = {t: i for i, t in enumerate(SUPPORT_TIERS)}

# Canonical dispositions must never appear on a Notes record. Asserted by the
# validator rather than trusted.
CANONICAL_DISPOSITIONS = {"EXACT_MATCH", "NEAR_MATCH", "SAME_CORE_ASK",
                          "PARTIAL_COVERAGE", "MISSING", "AMBIGUOUS"}

# --- Notes-layer thresholds. Not the canonical matcher's, and not shared. ---
NOTES_MIN_TOKENS = 3        # a one- or two-token prompt is a label, not an ask
NOTES_COMPLETE_BODY = 0.90
NOTES_COMPLETE_TITLE = 0.50
NOTES_STRONG_BODY = 0.75
NOTES_STRONG_TITLE = 0.34
NOTES_PARTIAL_BODY = 0.55
NOTES_TOPIC_BODY = 0.35


def _cap(tier, ceiling):
    return tier if SUPPORT_RANK[tier] <= SUPPORT_RANK[ceiling] else ceiling


def satisfied(token, hay):
    """Whether a note unit meets one token of the ask's demand.

    A `dsg:` token is an alias of a word, not always a second demand. The
    source compilation writes ordinary words in capitals for emphasis - 'What
    is "GIRDING"?' - and the acronym pass turns each into `dsg:girding`
    alongside the prose `girding`. Ordinary prose can never carry that alias,
    so the same word counted twice made a dedicated note section unmatchable.
    A designator alias is satisfied when the unit carries the word itself.

    This is a Notes-layer matching rule. It does not touch the tokeniser, and
    designator CONFLICT is still computed on the raw sets, so ME-GI against
    ME-GA is unaffected: `me-gi` is not a word that appears in prose.
    """
    if token in hay:
        return True
    if str(token).startswith("dsg:"):
        body = str(token)[4:]
        return body in hay or body.replace("-", "") in hay
    return False


def classify_support(body_cov, title_cov, n_src_tokens, conflict,
                     answer_bearing, missing_load_bearing,
                     unit_is_about_whole_ask=False):
    """(tier, reason) for one source ask against one note unit."""
    if body_cov >= NOTES_COMPLETE_BODY and title_cov >= NOTES_COMPLETE_TITLE:
        tier = COMPLETE_SUPPORT
        why = "the unit is about this ask and carries its whole demand"
    elif body_cov >= NOTES_STRONG_BODY and title_cov >= NOTES_STRONG_TITLE:
        tier = STRONG_SUPPORT
        why = "the unit is about this ask and carries most of its demand"
    elif body_cov >= NOTES_PARTIAL_BODY:
        tier = PARTIAL_SUPPORT
        why = "the unit carries a substantial part of the ask"
    elif body_cov >= NOTES_TOPIC_BODY:
        tier = TOPIC_SUPPORT
        why = "the unit shares the subject area"
    else:
        return NO_SUPPORT, "no meaningful section-local overlap"

    # Ceilings. Each states a reason the evidence cannot mean what the raw
    # score would otherwise say.
    if conflict:
        return _cap(tier, TOPIC_SUPPORT), "contradictory technical designator"
    if n_src_tokens < NOTES_MIN_TOKENS and not (
            unit_is_about_whole_ask and answer_bearing):
        # A terse prompt proves nothing when it merely appears somewhere inside
        # a large unit. It proves a great deal when the unit is titled for it
        # and answers it: a section called "Tug Girding - Capsizing Risk" is a
        # dedicated treatment of "What is GIRDING?", not a coincidence of
        # vocabulary. A broad unit that only mentions the term is still capped,
        # because its title will not carry the ask.
        return _cap(tier, TOPIC_SUPPORT), "source prompt too terse to support"
    if not answer_bearing:
        return (_cap(tier, TOPIC_SUPPORT),
                "the unit poses a question rather than answering one")
    if missing_load_bearing and SUPPORT_RANK[tier] > SUPPORT_RANK[PARTIAL_SUPPORT]:
        return PARTIAL_SUPPORT, ("the unit does not carry the ask's specific "
                                 "designator or numeric demand")
    return tier, why


# --------------------------------------------------------------------------
def unit_index(units):
    """Token sets for every note unit, computed once.

    `body` is the unit's own text; `about` is its title, subtitle and authored
    keywords - what the unit is FOR, as opposed to what it happens to mention.
    """
    idx = {}
    for u in units:
        if u["parent_unit_id"]:
            # A child carries its parent's title and authored keywords as
            # CONTEXT. Counting them as aboutness let a Q&A item titled
            # "Differentiate Gross Tonnage from Deadweight" score 1.00 aboutness
            # for "Hong Kong Convention", because its parent's data-kw said so.
            # A child is about what its own question says.
            about = u["section_title"]
        else:
            about = " ".join(x for x in (u["section_title"],
                                         u["section_subtitle"],
                                         u["keywords"]) if x)
        body = " ".join(x for x in (about, u["text"],
                                    " ".join(u["reg_codes"])) if x)
        idx[u["note_unit_id"]] = {
            "about_tokens": T.mtokens(about),
            "body_tokens": T.mtokens(body),
            "unit": u,
        }
    return idx


def source_tokens(record):
    """The ask's tokens, repaired by the same curated map the matcher uses."""
    raw = T.mtokens(record.get("question_core_text") or "")
    if not raw:
        raw = T.mtokens(record.get("raw_question_text") or "")
    toks, _ = T.repair_tokens(raw)
    return toks


def score(src_toks, entry, idf, default):
    """(body_cov, title_cov, conflict, missing_load_bearing) for one unit."""
    body = entry["body_tokens"]
    body_cov = _weighted(src_toks, body, idf, default)
    title_cov = _weighted(src_toks, entry["about_tokens"], idf, default)
    conflict = T.designator_conflict(src_toks, body)
    missing = sorted(t for t in src_toks
                     if T.is_load_bearing(t) and not satisfied(t, body))
    return body_cov, title_cov, conflict, missing


def _weighted(src_tokens, hay_tokens, idf, default):
    """IDF-weighted fraction of the ask's demand present in the unit.

    Sorted, because float addition is not associative and an unsorted sum would
    make the score itself depend on set-iteration order between runs.
    """
    if not src_tokens:
        return 0.0
    toks = sorted(src_tokens)
    tot = sum(idf.get(t, default) for t in toks)
    hit = sum(idf.get(t, default) for t in toks if satisfied(t, hay_tokens))
    return hit / tot if tot else 0.0


def best_support(src_toks, idx, idf, default, limit=5):
    """Every unit that supports this ask, best first, with full traceability.

    Ordering is total: score, then tier rank, then unit id, so two runs order
    identical evidence identically.
    """
    hits = []
    for uid in sorted(idx):
        entry = idx[uid]
        body_cov, title_cov, conflict, missing = score(
            src_toks, entry, idf, default)
        about_whole = all(satisfied(t, entry["about_tokens"]) for t in src_toks)
        tier, why = classify_support(
            body_cov, title_cov, len(src_toks), conflict,
            entry["unit"]["answer_bearing"], bool(missing), about_whole)
        if tier == NO_SUPPORT:
            continue
        hits.append({
            "note_unit_id": uid,
            "file": entry["unit"]["file"],
            "series": entry["unit"]["series"],
            "url": entry["unit"]["url"],
            "anchor": entry["unit"]["anchor"],
            "unit_level": entry["unit"]["unit_level"],
            "section_title": entry["unit"]["section_title"],
            "page_badge": entry["unit"]["page_badge"],
            "notes_support": tier,
            "support_reason": why,
            "body_coverage": round(body_cov, 3),
            "about_coverage": round(title_cov, 3),
            "designator_conflict": conflict,
            "missing_load_bearing": missing,
        })
    # Aboutness ranks before body coverage. Ranking on body coverage first put
    # a "Marine Insurance Fundamentals" topic above the Hong Kong Convention
    # topic for an IHM ask, because the generic words of the prompt ("detail",
    # "certificate", "every") appear in any long unit. Which unit is ABOUT the
    # ask is the better discriminator, and the sort stays total.
    # A unit that carries the ask's own designator or numeric demand is better
    # evidence than one that does not, whatever its prose overlap.
    hits.sort(key=lambda h: (-SUPPORT_RANK[h["notes_support"]],
                             bool(h["missing_load_bearing"]),
                             -h["about_coverage"], -h["body_coverage"],
                             h["note_unit_id"]))
    return hits[:limit]


def idf_over_units(idx):
    """IDF across note units. The Notes have their own vocabulary
    distribution; borrowing the QB's would misweight both."""
    from collections import Counter
    df = Counter()
    for uid in sorted(idx):
        for t in idx[uid]["body_tokens"]:
            df[t] += 1
    import math
    n = max(len(idx), 1)
    table = {t: math.log(1 + n / (1 + c)) for t, c in df.items()}
    return table, (max(table.values()) if table else 1.0)
