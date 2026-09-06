"""Generate CORR-P1CLOSE-20260906 - the third link in the Pass-1 chain.

    CORR-T5-HYDRANT / -REACH / -DDCASCADE   the original Pass 1
      -> CORR-P1REPAIR-20260906             the repair of its two P0 escapes
        -> CORR-P1CLOSE-20260906            the closure of the repair's own
                                            three P1 escapes

Nothing earlier is rewritten. Each record states what the one before it got
wrong, and each keeps its own pins, because an escape is only auditable if the
claim that missed it survives verbatim. Three reviews found three defects; the
trail of all three is the point.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
QB_ROOT = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import read_text                              # noqa: E402
from validate_batch_h_series import card_digests              # noqa: E402
from oral_supersession import build_chain, load_card_records  # noqa: E402

BASELINE = "43597e3"
GOVERNING = ["0626fca"]
NAME = "correction_corr_p1close_20260906_manifest.json"

CARDS = [
    ("QB2_F.html", "q2", "PRIMARY_CORRECTION",
     "The deep-dive Numbers layer taught 'Minimum fire-main pressure benchmark: "
     "0.27 MPa at deck monitors' - single-limb, so wrong for every cargo ship "
     "under 6,000 GT, and attributing to SOLAS a deck-monitor figure the "
     "provision does not fix. Replaced with SOLAS II-2/10.2.1.6, both "
     "cargo-ship limbs, the two-pump condition, and an explicit statement that "
     "the figure applies AT THE HYDRANTS. The card's second site, a cheat-card "
     "<div>, carried the same claim and is corrected with it."),
    ("QB2_F.html", "q4", "PROPAGATED_FACT_CORRECTION",
     "Two further sites on the same page printed a RANGE, '0.27-0.35 MPa', at "
     "open-deck monitors - one in the Engineering Actions list and one in the "
     "'Numbers & Regulations to Memorise' block. The detector could not see "
     "them because in a range only the last figure carries the unit, so the "
     "governed 0.27 limb was never normalised: a FOURTH instance of the same "
     "defect class, this time number formatting. The operational target is "
     "kept - q2 of this card already sanctions that category - and the "
     "governing minimum is attached beside it in q2's own wording, which is "
     "propagation of an adjudicated sentence rather than a new editorial "
     "judgement."),
    ("QB2_H.html", "q2", "SCOPE_PASS_CORRECTION",
     "Version stamp corrected: it attributed the removal of an empty deep-dive "
     "element to this card's own 6 September correction, when that removal was "
     "made the same day by CORR-T5-DDCASCADE-20260906. Provenance, not "
     "teaching - but a stamp that misattributes an edit is the audit trail "
     "being wrong about itself."),
]

ARTEFACTS = [
    {"path": "meoclass1/oralnotes/miw-notes-mgmt-p10.html",
     "classification": "DEPENDENCY_CORRECTION",
     "rationale": "Carries no q-card. The BMP currentness banner had been "
                  "inserted at the FIRST occurrence of its anchor and landed in "
                  "the Marine Environmental Governance (UNCLOS Pt. XII) topic, "
                  "about 375 lines and four topics from the BMP material, while "
                  "topic-46 said 'see the currentness note above' and carried "
                  "none. A currentness note governs its container, so the "
                  "misplaced banner protected text that needed no protection "
                  "and left the real material unguarded. Relocated into "
                  "topic-46 by structural id. The timeline row also regains the "
                  "HRA geography, now as the contrast it has become.",
     "guarded_by": "validate_correction_p1repair.py"},
    {"path": "meoclass1/oralnotes/simon-notes-p1.html",
     "classification": "DEPENDENCY_CORRECTION",
     "rationale": "Restores 'but referenced in IMO circulars', dropped as "
                  "collateral by the earlier reg-item rewrite. The Witherby "
                  "attribution is deliberately NOT restored: it was BMP5's "
                  "publisher, and attaching it to BMP Maritime Security would "
                  "be a new error.",
     "guarded_by": "validate_correction_p1repair.py"},
    {"path": "tools/oral/oral_currentness.py",
     "classification": "GOVERNANCE_RECORD",
     "rationale": "THE semantic detector module, and the substance of this "
                  "record. Units normalised (0.27 MPa = 0.27 N/mm2 = 2.7 bar = "
                  "270 kPa), numerals normalised (two pumps = 2 pumps), claims "
                  "taken from the smallest ENCLOSING element of any "
                  "candidate-facing tag. Imported by the gates, never "
                  "re-implemented - three escapes came from three gates each "
                  "inventing its own narrow matcher.",
     "guarded_by": "validate_correction_p1repair.py"},
    {"path": "meoclass1/known_traps.md",
     "classification": "GOVERNANCE_RECORD",
     "known_traps_entry": 99,
     "rationale": "Entry 99 records that all three escapes were ONE defect - a "
                  "guard recognising a spelling, a shape or a position instead "
                  "of a proposition - with the case/unit/element/class table. "
                  "Entry 100 records insertion by structural identity, and that "
                  "this was the third wrong-occurrence bug in one session.",
     "guarded_by": "validate_correction_p1repair.py"},
    {"path": "tools/oral/apply_corr_p1close.py",
     "classification": "GOVERNANCE_RECORD",
     "rationale": "The applier, locating the topic by structural id rather than "
                  "by a text needle.",
     "guarded_by": "validate_correction_p1repair.py"},
]


def prior_pin(fname, anchor, records):
    chain, problem = build_chain((fname, anchor), records=records)
    if problem is not None:
        raise SystemExit("chain problem %s#%s: %s" % (fname, anchor, problem))
    if chain is not None:
        s = chain[-1]
        return {"manifest": s.manifest, "action_id": sorted(s.action_ids)[0],
                "post_edit_digest": s.post}
    hits = [r for r in records if r.file == fname and r.anchor == anchor]
    if not hits:
        return None
    if len(hits) > 1:
        raise SystemExit("ambiguous prior pin %s#%s" % (fname, anchor))
    return {"manifest": hits[0].manifest, "action_id": hits[0].action_id,
            "post_edit_digest": hits[0].post_edit_digest}


def baseline_digest(fname, anchor):
    out = subprocess.run(["git", "show", "%s:meoclass1/%s" % (BASELINE, fname)],
                         cwd=str(REPO), capture_output=True)
    if out.returncode:
        raise SystemExit("cannot read %s at %s" % (fname, BASELINE))
    return card_digests(out.stdout.decode("utf-8")).get(anchor)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    records = [r for r in load_card_records() if r.manifest != NAME]
    entries = []
    for i, (fname, anchor, klass, what) in enumerate(CARDS, 1):
        prior = prior_pin(fname, anchor, records)
        e = {
            "correction_action_id": "P1CLOSE-%02d" % i,
            "file": fname,
            "path": "meoclass1/%s" % fname,
            "anchor": anchor,
            "classification": klass,
            "pre_edit_digest": baseline_digest(fname, anchor),
            "post_edit_digest": card_digests(read_text(QB_ROOT / fname))[anchor],
            "what_changed": what,
        }
        if prior:
            e["supersedes"] = {
                "manifest": prior["manifest"],
                "action_id": prior["action_id"],
                "post_edit_digest": prior["post_edit_digest"],
                "note": "%s pinned the state this closure edits. Its post-edit "
                        "digest is this record's pre-edit digest, so the chain "
                        "Pass 1 -> Pass-1 repair -> Pass-1 closure is unbroken "
                        "and no earlier record was rewritten to accommodate it."
                        % prior["action_id"],
            }
            e["digest_pinned_by_earlier_manifest"] = True
        entries.append(e)

    rec = {
        "correction_id": "CORR-P1CLOSE-20260906",
        "kind": "POST_RELEASE_CORRECTION",
        "status": "AUTHORISED",
        "origin": "fresh_independent_verification_p1_block",
        "date": "2026-09-06",
        "baseline_commit": BASELINE,
        "governing_commits": GOVERNING,
        "known_traps_entries": [99, 100],
        "authorisation_source":
            "MIW PASS 1 REPAIR CLOSURE instruction of 6 September 2026, section "
            "0, which confirms the original P0s closed and rules that exactly "
            "three P1 escape mechanisms remain. Those three were found by a "
            "clean-context verifier that had not seen how the repair was "
            "produced, and each was independently re-verified here before any "
            "byte was written.",
        "title":
            "Three P1 escapes, one defect: a guard that recognised a spelling "
            "(case), a rendering (unit and element type) or a position (first "
            "matching anchor) instead of the proposition it was written to "
            "protect.",
        "candidate_claim":
            "Not a candidate report. Fresh independent verification of "
            "CORR-P1REPAIR-20260906: P1-A unit/element blindness, P1-B "
            "wrong-occurrence insertion, P1-C HTML-shape-limited BMP "
            "currentness gate.",
        "candidate_verdict":
            "UPHELD IN FULL and re-verified at source. The verifier also "
            "confirmed the two original P0s genuinely gone corpus-wide, "
            "pastpapers untouched, no content lost, 761/86 and 5/5 accepts - so "
            "the defects were guard breadth and one insertion locator, not the "
            "substance of the repair.",
        "authority":
            "SOLAS II-2/10.2.1.6 (Consolidated Edition 2024), already relied on "
            "by CORR-T5-HYDRANT: minimum pressure at the HYDRANTS with the two "
            "required pumps delivering simultaneously - cargo ships 0.27 N/mm2 "
            "at 6,000 GT and upwards, 0.25 N/mm2 below. The provision fixes no "
            "separate deck-monitor figure, so none is asserted. NO NEW SOURCE "
            "EVIDENCE. Unit equivalence (1 N/mm2 = 1 MPa; 1 bar = 0.1 MPa) is "
            "arithmetic used for DETECTION only and is never applied to rewrite "
            "a card's chosen units.",
        "propagation": {
            "derived_surfaces":
                "NONE. No question stem changed; 761 questions / 86 files, "
                "outputs already matching the live derivation.",
            "hub_date": "NOT ADVANCED.",
            "detector_generalisation":
                "tools/oral/oral_currentness.py replaces three narrow matchers "
                "with one semantic implementation: pressure normalised across "
                "MPa / N/mm2 / bar / kPa, 'two pumps' and '2 pumps' treated as "
                "one proposition, and the claim taken from the smallest "
                "ENCLOSING element of any candidate-facing tag (li, p, td, th, "
                "div, span, strong, b, em, h1-h6, summary, caption) rather than "
                "the innermost, which around a figure is usually a <strong> "
                "carrying no subject and no modal.",
            "false_positives_held":
                "A claim needs subject AND figure AND mandatory framing AND "
                "incomplete scope. Two of four is not the defect: figure plus "
                "subject alone fires on 'fire main water (typically 5-7 bar)', "
                "a HydroPen operating pressure that is correct; figure plus "
                "modal alone fires on the weathertightness hose test, a "
                "different quantity with no held source, already recorded as "
                "K-ITEM-HOSE-TEST-PRESSURE.",
            "surface_policy_unchanged":
                "The recursive classification stands: qcard, cheatsheet, "
                "oralnotes, pastpapers, rulesapp, generated. The currentness "
                "gate runs on the governed teaching surfaces only. pastpapers "
                "remain sitting-anchored and are asserted unchanged; generated "
                "pages echo question stems and are never hand-edited - "
                "topics.html carries a BMP5 stem echo that is KEEP for exactly "
                "that reason.",
            "collateral_prose_restored":
                "Two clauses dropped by the earlier oralnotes rewrites are "
                "restored: 'but referenced in IMO circulars', and the HRA "
                "geography, now framed as the contrast with a global guide. The "
                "Witherby attribution is NOT restored - it was BMP5's "
                "publisher, and attaching it to BMP MS would be a new error.",
        },
        "invariants": {
            "canonical_questions_before": 761,
            "canonical_questions_after": 761,
            "question_bearing_files": 86,
            "new_cards": 0,
            "corrected_cards": len(entries),
            "corrected_artefact_surfaces": 2,
            "pressure_forms_normalised": "MPa, N/mm2, bar, kPa; ranges with hyphen, en-dash, em-dash, solidus or 'to'; comma decimal separator; 'two pumps' and '2 pumps'",
            "firemain_scope_defects_remaining": 0,
            "bmp5_taught_as_current_remaining": 0,
            "currentness_banners_outside_intended_topic": 0,
        },
        "supersedes_summary": {
            "note": "Neither the Pass-1 records nor the Pass-1 repair record is "
                    "rewritten. Each states what the one before it got wrong "
                    "and keeps its own pins; the chain is Pass 1 -> repair -> "
                    "closure.",
            "corrected_claims": [
                "CORR-P1REPAIR-20260906's single-limb check was described as "
                "corpus-wide. It required the literal '0.27 N/mm' and read only "
                "<li> and <p>, so it could not see QB2_F's '0.27 MPa' in a "
                "<div>.",
                "CORR-P1REPAIR-20260906's BMP5 check was described as proving "
                "no surface teaches BMP5 as current. It inspected reg-code "
                "slots only, and would not have caught the <td> cell or CE-tip "
                "prose that same record had just corrected.",
                "CORR-P1REPAIR-20260906 recorded a currentness note as added to "
                "the SUA/BMP topic. It was inserted at the first matching "
                "anchor in the file and landed in an unrelated topic.",
            ],
        },
        "review": {
            "gate": "tools/oral/validate_correction_p1repair.py",
            "mutation_suite": "tools/oral/mutate_correction_p1close.py",
            "scope_control": "tools/oral/test_corpus_scope.py",
            "independent_review":
                "The three defects were found by fresh independent "
                "verification. A further clean-context verification of this "
                "closure is recorded separately.",
        },
        "artefacts": ARTEFACTS,
        "cards": entries,
    }

    blob = json.dumps(rec, indent=1, ensure_ascii=False) + "\n"
    print("%s  %d cards, %d artefacts" % (NAME, len(entries), len(ARTEFACTS)))
    if args.write:
        (HERE / NAME).write_bytes(blob.encode("utf-8").replace(b"\r\n", b"\n"))
        print("WRITTEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
