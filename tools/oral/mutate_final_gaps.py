"""Mutation harness for the final Oral gap adjudication.

Each mutation injects one defect the count must never survive, runs the
validator, and requires it to fail. Two things are proved for every mutation,
because a harness that skips either can report a clean sweep while testing
nothing:

  APPLIED  - the artefact's SHA-256 actually changed. A mutation that silently
             no-ops (a moved anchor, a renamed key) is reported NOT APPLIED and
             counted as an escape, not a pass.
  RESTORED - the original bytes are back afterwards, digest-checked.

An escape is a mutation the validator did not catch. A crash is not a pass:
the validator must FAIL, not blow up.
"""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

DATA = L.OUT / "FINAL_REMAINING_ORAL_PRODUCTION_DECISIONS.json"
VALIDATOR = Path(__file__).resolve().parent / "validate_final_gaps.py"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_validator():
    """Return (exit_code, output). Decoded explicitly as UTF-8: the default
    Windows codepage would mangle the artefact's text and manufacture noise."""
    r = subprocess.run([sys.executable, str(VALIDATOR)],
                       capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace")


# --------------------------------------------------------------------------
def m_ambiguous_counted_as_new(p):
    """A: an ambiguous family is promoted to a counted NEW card."""
    # deliberately the LOWEST-coverage ambiguous family: if the catch depended
    # on the coverage check rather than on the ambiguity itself, this escapes.
    cands = sorted((f for f in p["families"]
                    if f["decision"] == "HUMAN_REVIEW_REQUIRED"),
                   key=lambda x: x["current_best_answer_coverage"])
    for f in cands:
        if True:
            f["decision"] = "NEW_CANONICAL_QA"
            f["production_id"] = "ORALQA-9001"
            f["recommended_qb_file"] = "QB1_A"
            f["confidence"] = "READY_HIGH_CONFIDENCE"
            f["batch"] = "P1-A"
            p["headline"]["ADDITIONAL_NEW_CANONICAL_QA_COUNT"] += 1
            p["headline"]["TOTAL_NEW_AFTER_APPROVED_BATCH"] += 1
            p["headline"]["HUMAN_REVIEW_REQUIRED_COUNT"] -= 1
            return p
    raise AssertionError("fixture missing: no ambiguous family")


def m_duplicate_production_family(p):
    """B: two approved new cards collapse onto one unadjudicated home."""
    high = [f for f in p["families"]
            if f["decision"] == "NEW_CANONICAL_QA"
            and f["confidence"] == "READY_HIGH_CONFIDENCE"]
    a, b = high[0], high[1]
    b["recommended_qb_file"] = a["recommended_qb_file"]
    b["decision_target"] = a["recommended_qb_file"]
    return p


def m_duplicate_production_id(p):
    """B2: the same production id issued twice."""
    new = [f for f in p["families"] if f["decision"] == "NEW_CANONICAL_QA"]
    new[1]["production_id"] = new[0]["production_id"]
    return p


def m_new_with_unexplained_enrichment_home(p):
    """C: a new card whose live answer already covers it, with no reason."""
    for f in p["families"]:
        if f["decision"] == "NEW_CANONICAL_QA":
            f["current_best_answer_coverage"] = 0.93
            f["decision_reason"] = "no existing answer prepares the candidate"
            return p
    raise AssertionError("fixture missing: no new card")


def m_notes_complete_called_new(p):
    """D: a Notes-complete family relabelled NEW with no Notes justification."""
    for f in p["families"]:
        if f["decision"] == "NEW_CANONICAL_QA":
            f["notes_support"] = "NOTES_COMPLETE_SUPPORT"
            f["decision_reason"] = "returns zero hits corpus-wide"
            return p
    raise AssertionError("fixture missing: no new card")


def m_p0_family_reintroduced(p):
    """E: a completed P0 family reappears as outstanding work."""
    tmpl = copy.deepcopy(p["families"][0])
    tmpl["family_id"] = "GAP-0002"
    tmpl["decision"] = "NEW_CANONICAL_QA"
    tmpl["confidence"] = "READY_HIGH_CONFIDENCE"
    tmpl["batch"] = "P1-A"
    tmpl["production_id"] = "ORALQA-0002"
    tmpl["recommended_qb_file"] = "QB1_K"
    p["families"].append(tmpl)
    return p


def m_missing_source_occurrence_id(p):
    """F: a proposed new card loses its source evidence."""
    for f in p["families"]:
        if f["decision"] == "NEW_CANONICAL_QA":
            f["source_ids"] = []
            return p
    raise AssertionError("fixture missing: no new card")


def m_unknown_source_occurrence_id(p):
    """F2: a source id that no 788 row supports."""
    for f in p["families"]:
        if f["decision"] == "NEW_CANONICAL_QA":
            f["source_ids"] = ["ASC-9999"]
            return p
    raise AssertionError("fixture missing: no new card")


def m_enrichment_target_dangling(p):
    """G: an enrichment aimed at an anchor that is not live."""
    for f in p["families"]:
        if f["decision"] == "ENRICH_EXISTING_QB":
            f["decision_target"] = "QB1_A#q999"
            return p
    raise AssertionError("fixture missing: no enrichment")


def m_notes_source_dangling(p):
    """H: a Notes promotion aimed at a Notes file that does not exist."""
    for f in p["families"]:
        if f["decision"] == "NOTES_TO_QB_PROMOTION":
            f["decision_target"] = "no-such-notes-page.html#n1"
            return p
    raise AssertionError("fixture missing: no Notes promotion")


def m_headline_inflated(p):
    """I: the headline claims more new cards than the dataset holds."""
    p["headline"]["ADDITIONAL_NEW_CANONICAL_QA_COUNT"] += 7
    return p


def m_headline_enrich_deflated(p):
    """I2: the headline understates outstanding enrichment work."""
    p["headline"]["ADDITIONAL_ENRICH_EXISTING_COUNT"] = 0
    return p


def m_merge_chain(p):
    """J: a merge pointing at another merge, so the family never lands."""
    merges = [f for f in p["families"]
              if f["decision"] == "MERGE_WITH_EXISTING_FAMILY"]
    merges[0]["decision_target"] = merges[1]["family_id"]
    return p


def m_merge_target_dangling(p):
    """J2: a merge into a family that does not exist."""
    for f in p["families"]:
        if f["decision"] == "MERGE_WITH_EXISTING_FAMILY":
            f["decision_target"] = "GAP-9999"
            return p
    raise AssertionError("fixture missing: no merge")


def m_family_dropped(p):
    """K: a family silently disappears from the accounting."""
    p["families"] = p["families"][:-1]
    return p


def m_family_duplicated(p):
    """K2: a family counted twice."""
    p["families"].append(copy.deepcopy(p["families"][0]))
    return p


def m_missing_left_as_instruction(p):
    """L: a family left with the raw matcher verdict as its instruction."""
    p["families"][0]["decision"] = "MISSING"
    return p


def m_new_card_home_not_live(p):
    """M: a new card filed to a QB page that does not exist."""
    for f in p["families"]:
        if f["decision"] == "NEW_CANONICAL_QA":
            f["recommended_qb_file"] = "QB99_Z"
            return p
    raise AssertionError("fixture missing: no new card")


def m_terse_prompt_force_resolved(p):
    """N: a one-token human-review prompt forced onto a target."""
    for r in p["human_review"]["rows"]:
        if r["prompt_token_mass"] < 3:
            r["verdict"] = "RESOLVED_TO_EXISTING"
            r["target"] = "QB1_A#q1"
            return p
    raise AssertionError("fixture missing: no terse human-review row")


def m_human_review_verdict_invented(p):
    """O: a human-review verdict outside the governed vocabulary."""
    p["human_review"]["rows"][0]["verdict"] = "PROBABLY_FINE"
    return p


def m_duplicate_home_pair_collapsed(p):
    """P: the duplicate-home debt record points a pair at itself."""
    p["duplicate_home_debt"][0]["pair"][1] = p["duplicate_home_debt"][0]["pair"][0]
    return p


def m_unbatched_new_card(p):
    """Q: an approved new card with no batch, so it never gets scheduled."""
    for f in p["families"]:
        if (f["decision"] == "NEW_CANONICAL_QA"
                and f["confidence"] == "READY_HIGH_CONFIDENCE"):
            f["batch"] = None
            return p
    raise AssertionError("fixture missing: no approved new card")


MUTATIONS = [
    ("A  ambiguous counted as NEW", m_ambiguous_counted_as_new),
    ("B  duplicate production family", m_duplicate_production_family),
    ("B2 duplicate production id", m_duplicate_production_id),
    ("C  NEW with unexplained enrichment home", m_new_with_unexplained_enrichment_home),
    ("D  Notes-complete called NEW", m_notes_complete_called_new),
    ("E  completed P0 family reintroduced", m_p0_family_reintroduced),
    ("F  missing source occurrence id", m_missing_source_occurrence_id),
    ("F2 unknown source occurrence id", m_unknown_source_occurrence_id),
    ("G  enrichment target dangling", m_enrichment_target_dangling),
    ("H  Notes source dangling", m_notes_source_dangling),
    ("I  headline inflated", m_headline_inflated),
    ("I2 headline enrichment deflated", m_headline_enrich_deflated),
    ("J  merge chain", m_merge_chain),
    ("J2 merge target dangling", m_merge_target_dangling),
    ("K  family dropped", m_family_dropped),
    ("K2 family duplicated", m_family_duplicated),
    ("L  MISSING left as instruction", m_missing_left_as_instruction),
    ("M  new card home not live", m_new_card_home_not_live),
    ("N  terse prompt force-resolved", m_terse_prompt_force_resolved),
    ("O  human-review verdict invented", m_human_review_verdict_invented),
    ("P  duplicate-home pair collapsed", m_duplicate_home_pair_collapsed),
    ("Q  approved new card unbatched", m_unbatched_new_card),
]


def main():
    if not DATA.exists():
        print("unavailable: %s not generated - run adjudicate_final_gaps.py"
              % DATA.name)
        return 2
    original = DATA.read_bytes()
    base_digest = digest(DATA)

    code, _ = run_validator()
    if code != 0:
        print("baseline validator does not pass; fix that before mutating")
        return 2
    print("baseline: validator PASS, artefact %s\n" % base_digest[:12])

    escapes, crashes, not_applied = [], [], []
    for name, fn in MUTATIONS:
        payload = json.loads(original.decode("utf-8"))
        try:
            mutated = fn(payload)
        except AssertionError as exc:
            print("%-42s FIXTURE %s" % (name, exc))
            crashes.append(name)
            continue
        DATA.write_text(json.dumps(mutated, ensure_ascii=False, indent=1),
                        encoding="utf-8", newline="\n")
        applied = digest(DATA) != base_digest
        code, out = run_validator()
        DATA.write_bytes(original)
        restored = digest(DATA) == base_digest

        if not applied:
            print("%-42s NOT APPLIED (mutation was a no-op)" % name)
            not_applied.append(name)
            continue
        if not restored:
            print("%-42s RESTORE FAILED" % name)
            crashes.append(name)
            continue
        if code == 0:
            print("%-42s ESCAPED" % name)
            escapes.append(name)
        elif code == 1:
            caught = [l.split(None, 1)[1].strip()
                      for l in out.splitlines() if l.startswith("FAIL")]
            print("%-42s caught by: %s" % (name, "; ".join(caught)[:80]))
        else:
            print("%-42s CRASHED exit=%d" % (name, code))
            crashes.append(name)

    code, _ = run_validator()
    print("\n%d mutations, %d escapes, %d not applied, %d crashes"
          % (len(MUTATIONS), len(escapes), len(not_applied), len(crashes)))
    print("post-run baseline validator: %s" % ("PASS" if code == 0 else "FAIL"))
    return 1 if (escapes or crashes or not_applied or code) else 0


if __name__ == "__main__":
    sys.exit(main())
