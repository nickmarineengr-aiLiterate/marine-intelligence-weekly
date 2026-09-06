"""Generate CORR-P1REPAIR-20260906 from the live corpus.

A repair layer, not a rewrite. The three Pass-1 records stay exactly as they
were published: they are the account of what the first attempt did and what it
claimed, and an escape is only auditable if the claim that missed it survives.
This record supersedes their PINS where the repair moved a card, and says in
terms what they got wrong.
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

from oral_bytes import read_text                            # noqa: E402
from validate_batch_h_series import card_digests            # noqa: E402
from oral_supersession import build_chain, load_card_records  # noqa: E402

BASELINE = "d07591c"
GOVERNING = ["816b1e3"]
DATE = "2026-09-06"
NAME = "correction_corr_p1repair_20260906_manifest.json"

CARDS = [
    ("QB2_H.html", "q2", "PRIMARY_CORRECTION",
     "The Key Numbers / Regs layer still carried '4.0 Bar: Minimum operational "
     "pressure required at the furthest deck hydrant on a large container "
     "vessel during multi-line operations' - the highest-salience block on the "
     "card, four lines above the v1.1 stamp CORR-T5-HYDRANT had just written "
     "saying that figure is not a SOLAS figure. Replaced with SOLAS "
     "II-2/10.2.1.6 and both cargo-ship limbs, plus one sentence separating an "
     "operational design target from a regulatory minimum."),
    ("QB4_H.html", "q2", "SCOPE_PASS_CORRECTION",
     "Version stamp advanced v1.5 -> v1.6 and its two same-day 'corrected 6 Sep "
     "2026:' clauses merged into one. Neither clause was erased: both describe "
     "edits that really happened, and two different card states were sharing "
     "one version label."),
    ("QB2_B.html", "q18", "SCOPE_PASS_CORRECTION",
     "The deep-dive 'Numbers to Memorise' layer still read 'Minimum hydrant "
     "pressure limits (0.27 N/mm2)' - single-limb, no threshold, no pump "
     "condition - on the very card whose Key Numbers bullet CORR-T5-HYDRANT "
     "corrected as E-3. A reach failure inside a card the previous pass "
     "believed it had closed, found by the new single-limb check rather than "
     "by any hand-built site list."),
    ("QB9_E.html", "q7", "SCOPE_PASS_CORRECTION",
     "Three raw markdown bullets inside the CE Relevance block were rendered "
     "literally to the candidate. A SECOND orphan form: Pass 1 scanned for "
     "'* <strong>' and these bullets open with a plain word, so they were "
     "neither repaired nor declared."),
]

ARTEFACTS = [
    {"path": "meoclass1/QB2_B_CheatSheet.html",
     "classification": "DEPENDENCY_CORRECTION",
     "rationale": "Carries no q-card, so it takes no digest pin. Two sites "
                  "taught single-limb 0.27 N/mm2 as the cargo-ship minimum - "
                  "the exact defect CORR-T5-HYDRANT calls 'wrong, not merely "
                  "incomplete' - and one of them had dropped the two-pump "
                  "condition as well, stating the figure as a continuous "
                  "firefighting duty. The hydrant record declared no "
                  "cheat-sheet artefacts at all, unlike its sibling reach "
                  "record which swept three.",
     "guarded_by": "validate_correction_p1repair.py"},
    {"path": "meoclass1/oralnotes/miw-notes-mgmt-p10.html",
     "classification": "PROPAGATED_FACT_CORRECTION",
     "rationale": "Topic 46 taught BMP5 as the live counter-piracy guidance and "
                  "dated it to 2024 on a timeline. Four sites corrected and a "
                  "currentness note added. The false date is removed without a "
                  "replacement publication year being asserted, because none is "
                  "held.",
     "guarded_by": "validate_correction_p1repair.py"},
    {"path": "meoclass1/oralnotes/simon-notes-p1.html",
     "classification": "PROPAGATED_FACT_CORRECTION",
     "rationale": "Two present-tense attributions to BMP5 and one reg-code slot "
                  "naming it as current industry guidance.",
     "guarded_by": "validate_correction_p1repair.py"},
    {"path": "meoclass1/oralnotes/miw-notes-mgmt-p1.html",
     "classification": "PROPAGATED_FACT_CORRECTION",
     "rationale": "A non-mandatory-guidance list and its accompanying tip named "
                  "BMP5 as a current industry document.",
     "guarded_by": "validate_correction_p1repair.py"},
    {"path": "meoclass1/known_traps.md",
     "classification": "GOVERNANCE_RECORD",
     "known_traps_entry": 96,
     "rationale": "Entries 96 and 97 record the two defect classes this repair "
                  "exists for: a case-sensitive forbidden-proposition matcher, "
                  "and a scope defect that is invisible from inside its own "
                  "scope.",
     "guarded_by": "validate_correction_p1repair.py"},
    {"path": "tools/oral/test_corpus_scope.py",
     "classification": "GOVERNANCE_RECORD",
     "rationale": "The scope control. It plants a file in a nested directory "
                  "and requires the enumeration to see it, so a reverted glob "
                  "goes red instead of passing vacuously.",
     "guarded_by": "validate_correction_p1repair.py"},
    {"path": "tools/oral/apply_corr_p1repair.py",
     "classification": "GOVERNANCE_RECORD",
     "rationale": "The applier, with each site's reason stated beside it.",
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

    OWN = {NAME}
    records = [r for r in load_card_records() if r.manifest not in OWN]

    entries = []
    for i, (fname, anchor, klass, what) in enumerate(CARDS, 1):
        prior = prior_pin(fname, anchor, records)
        pre = baseline_digest(fname, anchor)
        post = card_digests(read_text(QB_ROOT / fname))[anchor]
        e = {
            "correction_action_id": "P1REPAIR-%02d" % i,
            "file": fname,
            "path": "meoclass1/%s" % fname,
            "anchor": anchor,
            "classification": klass,
            "pre_edit_digest": pre,
            "post_edit_digest": post,
            "what_changed": what,
        }
        if prior:
            e["supersedes"] = {
                "manifest": prior["manifest"],
                "action_id": prior["action_id"],
                "post_edit_digest": prior["post_edit_digest"],
                "note": "%s pinned the state this repair edits. Its post-edit "
                        "digest is this record's pre-edit digest, so the chain "
                        "is unbroken. The earlier record is NOT rewritten: its "
                        "claim becomes 'my state is the ancestor of what is "
                        "live', which is true, rather than 'my state is live', "
                        "which stopped being true when the escape was repaired."
                        % prior["action_id"],
            }
            e["digest_pinned_by_earlier_manifest"] = True
        entries.append(e)

    rec = {
        "correction_id": "CORR-P1REPAIR-20260906",
        "kind": "POST_RELEASE_CORRECTION",
        "status": "AUTHORISED",
        "origin": "independent_review_p0_block",
        "date": DATE,
        "baseline_commit": BASELINE,
        "governing_commits": GOVERNING,
        "authorisation_source":
            "MIW PASS 1 REPAIR instruction of 6 September 2026, section 0, which "
            "confirms the independent-review block and rules that Pass 1 is NOT "
            "accepted as closed until both P0 defects are repaired. The review "
            "itself was run in a clean context that had not seen how Pass 1 was "
            "produced, and its two P0 findings were independently re-verified "
            "here before any byte was written.",
        "title":
            "Pass 1 shipped two P0 escapes and did not know it. A case-sensitive "
            "forbidden-proposition check reported PASS on a card still teaching "
            "the false figure it existed to remove, and every census that called "
            "itself corpus-wide enumerated 128 of the corpus's 224 files.",
        "candidate_claim":
            "Not a candidate report. Independent adversarial review of "
            "CORR-T5-DDCASCADE, CORR-T5-REACH and CORR-T5-HYDRANT, findings F-1 "
            "and F-2 (P0), F-3, F-4, F-5, F-6, F-7, F-9, F-10.",
        "candidate_verdict":
            "UPHELD IN FULL, and both P0s re-verified at source before repair. "
            "The review also UPHELD the Pass-1 losslessness claim by its own "
            "independent differ - the defects are reach and gate scope, not "
            "substance.",
        "authority":
            "SOLAS II-2/10.2.1.6 (Consolidated Edition 2024) for the hydrant "
            "limbs, as already relied on by CORR-T5-HYDRANT. SRC-BMPMS-2025 and "
            "SRC-BMPMS-2026 for the BMP supersession, both held in-repo with "
            "digests. NO NEW SOURCE EVIDENCE IS ADDED, and no date is invented: "
            "the repository holds no registry row for BMP5's own publication "
            "year, so the false 2024 timeline row was replaced with the held "
            "2025 supersession fact rather than with an unsourced 2018.",
        "propagation": {
            "derived_surfaces":
                "NONE. No question stem changed; build_qb_content_index.py "
                "--check reports 761 questions / 86 files with outputs already "
                "matching the live derivation.",
            "hub_date": "NOT ADVANCED.",
            "recursive_scope_established":
                "The corpus enumeration is now ONE function, "
                "census_known_defect_families.corpus_files(), recursive over "
                "meoclass1/**/*.html = 224 files, imported by every consumer "
                "that claims corpus-wide scope. tools/oral/test_corpus_scope.py "
                "plants a file in a nested directory and requires it to be "
                "seen, so reverting the glob goes red rather than passing "
                "vacuously.",
            "surface_policy":
                "224 files are NOT one product. qcard and cheatsheet: current "
                "teaching must be current. oralnotes: current study material by "
                "its own titles, so currentness rules apply - this is where the "
                "escape was. pastpapers: sitting-anchored, historical examiner "
                "wording is CORRECT and must not be modernised; it returns zero "
                "hits for this family in any case. generated: never hand-edited.",
            "deliberately_not_swept":
                "Of 139 recursive BMP5 / MSC.1-Circ.1606 sites, the oralnotes "
                "navigation cards, the Topic 46 title and tag, the uday index "
                "cross-reference rows and the bibliography entry are KEEP: they "
                "identify or cite a topic whose SUBJECT is BMP5, which is the "
                "examiner-wording case already settled on cards.",
            "false_positive_recorded":
                "oralnotes/miw-notes-mgmt-p6.html carries a lone '* Day-counts "
                "are ...' line that the recursive orphan-bullet scan flagged. It "
                "is the FOOTNOTE paired with the '3 days*' / '7 days*' / "
                "'~30 days*' markers above it. The scan now requires a RUN of "
                "two or more consecutive bullets, because a sweep that cannot "
                "tell a footnote from a bullet would have deleted the note "
                "explaining that those day-counts are not MLC statutory text.",
        },
        "invariants": {
            "canonical_questions_before": 761,
            "canonical_questions_after": 761,
            "question_bearing_files": 86,
            "new_cards": 0,
            "corrected_cards": len(entries),
            "corrected_artefact_surfaces": 4,
            "corpus_files_enumerated_pass1": 128,
            "corpus_files_enumerated_now": 224,
            "files_previously_invisible": 96,
        },
        "supersedes_summary": {
            "note": "The Pass-1 records are NOT rewritten. They remain on main "
                    "as the account of what the first attempt did and claimed, "
                    "because an escape is only auditable if the claim that "
                    "missed it survives.",
            "corrected_claims": [
                "CORR-T5-HYDRANT-20260906 stated its three sites closed the "
                "false-hydrant-figure family. QB2_H#q2 was not closed; its Key "
                "Numbers layer kept the figure.",
                "CORR-T5-DDCASCADE-20260906, CORR-T5-REACH-20260906 and "
                "CORR-T5-HYDRANT-20260906 each described their censuses as "
                "corpus-wide. They covered meoclass1/*.html only - 128 of 224 "
                "files.",
            ],
        },
        "review": {
            "gate": "tools/oral/validate_correction_p1repair.py",
            "mutation_suite": "tools/oral/mutate_correction_p1repair.py",
            "scope_control": "tools/oral/test_corpus_scope.py",
            "independent_review":
                "The DEFECT was found by independent review. A second, fresh "
                "independent verification of this repair is recorded separately.",
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
