"""Generate the three Pass-1 correction records from the live corpus.

Three coherent families, three records - never one giant manifest:

  CORR-T5-DDCASCADE-20260906  structural: the deep-dive suffix cascade, the
                              orphaned markdown bullets it left, and six empty
                              deep-dive promises
  CORR-T5-REACH-20260906      correction reach: a proposition that landed on a
                              teaching body and missed the footer, the cheat
                              sheet or a sibling card
  CORR-T5-HYDRANT-20260906    numeric standard: SOLAS II-2/10.2.1.6 hydrant
                              minimum pressure

Ordering matters and is recorded, not assumed. The three families were applied
in the order above, and two cards were touched by two of them:
QB1_F#q10 (cascade, then reach) and QB2_H#q2 (empty promise, then hydrant). The
INTERMEDIATE state of each is reconstructed deterministically by reversing the
later edit on the live bytes, so the cascade record pins the state it actually
produced and the later record declares descent from it. Collapsing the two into
one pin would make the cascade record claim a state it never made.

DIGEST CONVENTION. A chain stays in its ROOT's convention (SKILL.md 7.5). Four
cards descend from E-series enrichment pins recorded as `sha256(text)[:16]`, so
this record pins those four in 16 hex characters and every other card in the
full 64 the correction family uses. Mixing them is reported by the resolver as
DIGEST_CONVENTION_MISMATCH rather than silently compared as strings.
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

from oral_bytes import read_text                       # noqa: E402
from validate_batch_h_series import card_digests       # noqa: E402
from oral_supersession import build_chain, load_card_records  # noqa: E402

BASELINE = "464bc3c"
#: The commits that carry the product edits these three records govern. Two,
#: because the candidate-facing correction provenance (the q-version stamps)
#: landed after the content itself and is part of the same correction event.
GOVERNING = ["4c8dfd6", "e8c2ec7"]
DATE = "2026-09-06"

# EVERY CARD BELONGS TO EXACTLY ONE RECORD.
#
# Two cards were touched by two families - QB1_F#q10 (cascade, then the reach
# reg-box row) and QB2_H#q2 (empty promise, then the hydrant figure). The first
# design pinned each family's own intermediate state and chained them. That is
# unverifiable and `validate_corrections` is right to refuse it: it requires a
# record's pre-state to be the card at its BASELINE commit and its post-state to
# be the card at its LAST GOVERNING commit, and all three families landed in one
# content commit, so no commit holds an intermediate. A pin is a claim a third
# party must be able to check from the repository alone; a state that was never
# committed cannot be pinned.
#
# So each doubly-touched card is pinned ONCE, baseline -> live, by the record
# whose family is substantive for it, and the other record DECLARES the overlap
# in `propagation` without pinning it. The declaration is asserted by that
# record's content gate, so the overlap cannot be forgotten - it is recorded as
# structure, never as prose.
CASCADE_CARDS = {
    "QB1_F.html": ["q1", "q2", "q4", "q5", "q6", "q7", "q9", "q10", "q11", "q12",
                   "q13", "q14", "q15", "q16", "q17", "q18", "q19", "q20"],
    "QB1_G.html": ["q%d" % n for n in range(21, 41)],
    "QB1_I.html": ["q2", "q3", "q4", "q5", "q6"],
}
REACH_CARDS = [("QB4_H.html", "q2"), ("QB4_H.html", "q6"),
               ("QB5_B.html", "q14")]
HYDRANT_CARDS = [("QB2_A.html", "q8"), ("QB2_B.html", "q18"),
                 ("QB2_H.html", "q2")]

def live_digests(fname):
    return card_digests(read_text(QB_ROOT / fname))


def prior_pin(fname, anchor, records):
    """The terminal authorised state for this card before Pass 1, or None."""
    chain, problem = build_chain((fname, anchor), records=list(records))
    if problem is not None:
        raise SystemExit("chain problem for %s#%s: %s" % (fname, anchor, problem))
    if chain is not None:
        s = chain[-1]
        return {"manifest": s.manifest,
                "action_id": sorted(s.action_ids)[0],
                "post_edit_digest": s.post}
    hits = [r for r in records if r.file == fname and r.anchor == anchor]
    if not hits:
        return None
    if len(hits) > 1:
        raise SystemExit("ambiguous prior pin for %s#%s" % (fname, anchor))
    r = hits[0]
    return {"manifest": r.manifest, "action_id": r.action_id,
            "post_edit_digest": r.post_edit_digest}


#: A correction record ALWAYS pins the full 64-character sha256, even when it
#: supersedes an E-series batch pin recorded as `sha256(text)[:16]`. That is not
#: a convention breach: `oral_supersession._same_convention` treats a 16- and a
#: 64-character digest as comparable and compares them on the common prefix,
#: because the two are one function at two truncations over the same balanced
#: card block. Pinning the successor at 16 instead would satisfy the chain and
#: break `validate_corrections`, which computes live digests at 64 - and the
#: correction schema rejects a 16-character pin outright.


def card_entry(fname, anchor, action_id, classification, what_changed,
               pre_override=None, post_override=None, supersedes_override=None,
               records=None):
    prior = supersedes_override or prior_pin(fname, anchor, records)
    post = post_override or live_digests(fname)[anchor]
    pre = pre_override
    if pre is None:
        if not prior:
            raise SystemExit("no pre-edit state available for %s#%s"
                             % (fname, anchor))
        pre = prior["post_edit_digest"]
    entry = {
        "correction_action_id": action_id,
        "file": fname,
        "path": "meoclass1/%s" % fname,
        "anchor": anchor,
        "classification": classification,
        "pre_edit_digest": pre,
        "post_edit_digest": post,
        "what_changed": what_changed,
    }
    if prior:
        entry["supersedes"] = {
            "manifest": prior["manifest"],
            "action_id": prior["action_id"],
            "post_edit_digest": prior["post_edit_digest"],
            "note": "%s pinned the state this record edits. Its post-edit digest "
                    "is this record's pre-edit digest, so the chain is unbroken "
                    "and nothing edited the card in between."
                    % prior["action_id"],
        }
        entry["digest_pinned_by_earlier_manifest"] = True
    return entry


def git_pre_digests():
    """Pre-Pass-1 digests, read from the baseline tree rather than remembered."""
    out = {}
    for fname in sorted(set(list(CASCADE_CARDS) + [f for f, _ in REACH_CARDS] +
                            [f for f, _ in HYDRANT_CARDS])):
        blob = subprocess.run(["git", "show", "%s:meoclass1/%s" % (BASELINE, fname)],
                              cwd=str(REPO), capture_output=True)
        if blob.returncode != 0:
            raise SystemExit("cannot read %s at %s" % (fname, BASELINE))
        out[fname] = card_digests(blob.stdout.decode("utf-8"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    # The generator must NOT read its own output. Once a T5 record is on disk,
    # build_chain sees it as a state in the chain and reports
    # PREDECESSOR_PIN_ALTERED against the very pins this run is recomputing -
    # a generator that is not idempotent because it is its own input.
    OWN = {"correction_corr_t5_ddcascade_20260906_manifest.json",
           "correction_corr_t5_reach_20260906_manifest.json",
           "correction_corr_t5_hydrant_20260906_manifest.json"}
    records = [r for r in load_card_records() if r.manifest not in OWN]
    pre = git_pre_digests()

    # ---------------------------------------------------------------- 1
    cascade_entries = []
    n = 0
    for fname, anchors in CASCADE_CARDS.items():
        for a in anchors:
            n += 1
            post = live_digests(fname)[a]
            what = ("cascaded deep-dive blocks truncated at their first stray "
                    "markdown marker; every removed section survives verbatim as "
                    "the own body of the later typed block carrying that label")
            if fname == "QB1_I.html":
                what = ("empty <details class=\"deep-dive\"> element removed - it "
                        "promised seven sections and delivered none, and no "
                        "trustworthy source content existed to fill it")
            if (fname, a) in (("QB1_I.html", "q3"), ("QB1_F.html", "q2")):
                what += "; orphaned markdown bullet removed from the answer body"
            if fname == "QB1_G.html" and a in ("q34", "q36", "q37", "q38", "q39",
                                               "q40"):
                what += "; orphaned markdown bullet removed before the trap answer"
            # Exactly one card carries the record's origin. QB1_G#q40 is the
            # card Tranche 5 actually named in this family; the other 43 are
            # the same conversion defect found by the corpus census.
            klass = ("PRIMARY_CORRECTION" if (fname, a) == ("QB1_G.html", "q40")
                     else "SCOPE_PASS_CORRECTION")
            cascade_entries.append(card_entry(
                fname, a, "T5-DDCASCADE-%02d" % n, klass, what,
                pre_override=pre[fname][a], post_override=post, records=records))

    cascade = {
        "correction_id": "CORR-T5-DDCASCADE-20260906",
        "kind": "POST_RELEASE_CORRECTION",
        "status": "AUTHORISED",
        "origin": "known_defect_family_remediation_pass_1",
        "date": DATE,
        "baseline_commit": BASELINE,
        "governing_commits": list(GOVERNING),
        "authorisation_source":
            "MIW KNOWN-DEFECT-FAMILY REMEDIATION - PASS 1 instruction of "
            "6 September 2026, sections 4 and 5. Section 5 authorises correcting "
            "structural duplication and emptiness, and directs that an empty "
            "block with no trustworthy source content has its promise REMOVED "
            "rather than an answer fabricated. Section 4 authorises removing raw "
            "authoring residue once the owning block has been read.",
        "title":
            "A markdown-to-HTML conversion split each deep-dive blob into typed "
            "blocks by taking the tail from every '* <strong>Label:</strong>' "
            "marker ONWARD instead of the segment BETWEEN markers. Every block "
            "therefore rendered its own content plus every following section as "
            "raw markdown - 82,736 bytes of cascaded duplication across 146 "
            "blocks on 38 cards. Six further cards promised a seven-section "
            "deep dive and delivered an empty <details>.",
        "candidate_claim":
            "Not a candidate report. Tranche 5 named QB1_G#q40, QB1_I#q2 and "
            "QB2_H as members of this family; the corpus-wide census found the "
            "other 41 cards and established the single conversion-step root "
            "cause behind all of them.",
        "candidate_verdict":
            "UPHELD, and proved lossless before application. For all 146 blocks "
            "tools/oral/analyse_ddcascade.py showed the removed text is "
            "byte-identical to the OWN body of the later typed block carrying "
            "the same label on the same card, so the repair deletes only "
            "duplication. 0 blocks were unproven; the applier refuses any block "
            "the analyser has not proved.",
        "authority":
            "NONE REQUIRED - and that is the point. No regulatory proposition is "
            "added, removed or altered by this record. The set of propositions "
            "visible to a candidate is unchanged on every one of the 44 cards; "
            "only the duplicate rendering of them is gone. The six empty "
            "deep-dive elements carried no proposition at all.",
        "propagation": {
            "derived_surfaces":
                "NONE. No <div class=\"q-text\"> stem changed - "
                "build_qb_content_index.py --check reports the on-disk outputs "
                "still match the live derivation at 761 questions / 86 files, so "
                "qb_content_index.json, the hub, search, the examiner index, "
                "topics and study_mappings are byte-identical and were "
                "deliberately not regenerated. No XLSX regeneration is required.",
            "hub_date": "NOT ADVANCED. The Pass-1 instruction forbids it.",
            "cards_edited_here_but_pinned_by_a_sibling_record":
                "QB2_H.html#q2. Its empty deep-dive promise was removed by THIS "
                "family, and its 4.0 bar hydrant figure by "
                "CORR-T5-HYDRANT-20260906, both in the same content commit - so "
                "no commit holds an intermediate state and the card cannot be "
                "pinned twice. It is pinned once, baseline to live, by the "
                "hydrant record, whose family is the substantive one for it. "
                "The structural edit is declared here and asserted by this "
                "record's own content gate, which checks that NO empty "
                "deep-dive promise remains anywhere in the corpus - QB2_H "
                "included.",
            "residue_remaining":
                "This record closes the cascade, the orphaned bullets and the "
                "empty promises. A SECOND conversion generation remains and is "
                "reported as Pass-2 backlog, not silently dropped: 97 "
                "<p>#### heading residues (QB9_D 71, QB5_C_B 26), 18 "
                "<p>> blockquote residues, 19 <p>```</p> fence residues and 176 "
                "long rule separators. Those need re-rendering, not truncation, "
                "so a sweep must not touch them.",
        },
        "invariants": {
            "canonical_questions_before": 761,
            "canonical_questions_after": 761,
            "question_bearing_files": 86,
            "new_cards": 0,
            "corrected_cards": len(cascade_entries),
            "cascaded_blocks_repaired": 146,
            "duplicated_bytes_removed": 82736,
            "empty_deep_dive_promises_removed": 6,
            "orphaned_markdown_bullets_removed": 8,
            "blocks_refused_as_unproven": 0,
        },
        "review": {
            "gate": "tools/oral/validate_correction_t5struct.py",
            "mutation_suite": "tools/oral/mutate_correction_t5struct.py",
            "independent_review":
                "NOT YET - this record is produced by the same session that made "
                "the edits.",
        },
        "known_traps_entries": [90, 91, 92],
        "artefacts": [
            {"path": "meoclass1/known_traps.md",
             "classification": "GOVERNANCE_RECORD",
             "known_traps_entry": 90,
             "rationale": "Entry 90 records the cascade, the proof that makes it "
                          "mechanically repairable, and the two traps that cost "
                          "this repair a full re-run: matching blocks by "
                          "position instead of by label, and re-implementing the "
                          "normaliser beside its own proof so that 37 blocks "
                          "silently failed to match and were skipped with no "
                          "error raised. Entries 91 and 92 record the "
                          "deletion-blind idempotency check and the generator "
                          "that read its own output.",
             "guarded_by": "validate_correction_t5struct.py"},
            {"path": "tools/oral/analyse_ddcascade.py",
             "classification": "GOVERNANCE_RECORD",
             "rationale": "The losslessness proof. Re-runnable: it reports 0 "
                          "cascaded blocks on the corrected corpus, and would "
                          "report any block a future edit re-broke.",
             "guarded_by": "validate_correction_t5struct.py"},
            {"path": "tools/oral/apply_ddcascade_repair.py",
             "classification": "GOVERNANCE_RECORD",
             "rationale": "The applier. Idempotent, and refuses any block the "
                          "analyser has not proved lossless.",
             "guarded_by": "validate_correction_t5struct.py"},
            {"path": "tools/oral/census_known_defect_families.py",
             "classification": "GOVERNANCE_RECORD",
             "rationale": "The Pass-1 census that found the 41 cards the tranche "
                          "did not name, and that measures the Pass-2 residue "
                          "backlog this record deliberately leaves.",
             "guarded_by": "validate_correction_t5struct.py"},
        ],
        "cards": cascade_entries,
    }

    # ---------------------------------------------------------------- 2
    reach_what = {
        ("QB1_F.html", "q10"):
            "reg-box row 'Best Management Practices (BMP5)' migrated to BMP "
            "Maritime Security with its edition, scope and what it replaced. "
            "This card had never been reached by any BMP sweep.",
        ("QB4_H.html", "q2"):
            "the source-confidence footer still cited 'BMP5 Section 5 "
            "(mscio.eu)' as an authority this card was verified against, five "
            "days after the card's own body removed that carry-over as "
            "unverifiable and quoted the held current publication instead. The "
            "footer now cites the held BMP Maritime Security 1st Edition (2025) "
            "as updated June 2026. This is Tranche 5 finding N-1.",
        ("QB4_H.html", "q6"):
            "reg-box row 'BMP5' migrated to BMP Maritime Security. A sibling "
            "card in the SAME FILE as N-1 that three BMP sweeps did not open.",
        ("QB5_B.html", "q14"):
            "'BMP5 engineering measures' in the answer body and the 'BMP5 / "
            "Industry Best Management Practices' reg-box row migrated to the "
            "current publication. The card layer paired with the N-4a cheat "
            "sheet, and left behind by the same sweep.",
    }
    reach_entries = []
    for i, (fname, a) in enumerate(REACH_CARDS, 1):
        prior = None
        # The baseline tree is the source of the pre-edit state, read from git
        # rather than remembered. Where a prior pin exists it agrees with it;
        # where none exists this is the only place the state can come from.
        pre_override = pre[fname][a]
        # N-1 is the reported defect; the rest carry the same adjudicated fact.
        klass = ("PRIMARY_CORRECTION" if (fname, a) == ("QB4_H.html", "q2")
                 else "PROPAGATED_FACT_CORRECTION")
        reach_entries.append(card_entry(
            fname, a, "T5-REACH-%02d" % i, klass,
            reach_what[(fname, a)], pre_override=pre_override,
            supersedes_override=prior, records=records))

    reach = {
        "correction_id": "CORR-T5-REACH-20260906",
        "kind": "POST_RELEASE_CORRECTION",
        "status": "AUTHORISED",
        "origin": "known_defect_family_remediation_pass_1",
        "date": DATE,
        "baseline_commit": BASELINE,
        "governing_commits": list(GOVERNING),
        "authorisation_source":
            "MIW KNOWN-DEFECT-FAMILY REMEDIATION - PASS 1 instruction of "
            "6 September 2026, sections 3, 6 and 8. Section 8 authorises N-1, "
            "N-2 and N-4 by name. Sections 3 and 6 require the same census to "
            "be run corpus-wide and each hit classified; the three further "
            "sites here are MUST CORRECT under that census, and carry a fact "
            "already adjudicated and externally verified rather than a new one.",
        "title":
            "A correction reaches the teaching body and misses the surfaces "
            "carrying the same proposition. Seven such surfaces: a "
            "source-confidence footer offering a superseded publication as its "
            "verification authority, two cheat sheets teaching a superseded "
            "publication as current, a third cheat sheet missing its parent's "
            "predecessor banner, and three card-layer reg-box rows that no BMP "
            "sweep had ever opened because every sweep derived its site list "
            "from a finding's card list instead of from the corpus.",
        "candidate_claim":
            "Not a candidate report. Tranche 5 findings N-1, N-2 and N-4, plus "
            "three sites the Pass-1 corpus census added.",
        "candidate_verdict":
            "UPHELD. No new factual theory is advanced. Every edit carries the "
            "BMP supersession already established by "
            "CORR-GPT-T2C-CURRENCY-20260905 and propagated once by "
            "CORR-BMP-EDITION-PROP-20260905, to surfaces those records missed.",
        "authority":
            "BMP Maritime Security, 1st Edition (2025) as updated during 2026, "
            "published by BIMCO, ICS, IMCA, INTERCARGO, INTERTANKO and OCIMF; "
            "it replaced BMP5 (2018), BMP West Africa and the Global Counter "
            "Piracy Guidance. Registered SRC-BMPMS-2026 / SRC-BMPMS-2025. THIS "
            "RECORD ADDS NO SOURCE EVIDENCE OF ITS OWN. For N-2 no replacement "
            "circular is asserted: MSC.1/Circ.1606 was removed from the parent "
            "card as unusable and is not re-cited anywhere, so guessing a "
            "successor would be invention.",
        "propagation": {
            "derived_surfaces":
                "NONE. No question stem changed; build_qb_content_index.py "
                "--check reports 761 / 86 unchanged and byte-identical outputs.",
            "hub_date": "NOT ADVANCED.",
            "deliberately_not_swept":
                "94 of the 102 corpus BMP5/MSC.1-Circ.1606 sites are KEEP. A "
                "q-text, a cs-qtitle, a TOC entry, a sub-desc or a generated "
                "index row echoing one is the EXAMINER'S OWN WORDING; QB4_H#q11 "
                "is retained on purpose as the predecessor record because "
                "examiners still ask for BMP5 by name; and a currentness note "
                "that quotes BMP5 in order to deny it is the fix, not the "
                "defect. The N-4b cheat-sheet cue '\"BMP5 details\"' is kept for "
                "the same reason and only its ANSWER cell is qualified.",
            "cards_edited_here_but_pinned_by_a_sibling_record":
                "QB1_F.html#q10. Its reg-box row was migrated to BMP Maritime "
                "Security by THIS family (site A-5), and the same card was "
                "structurally repaired by CORR-T5-DDCASCADE-20260906, both in "
                "the same content commit - so no commit holds an intermediate "
                "state and the card cannot be pinned twice. It is pinned once, "
                "baseline to live, by the structural record, whose edit rewrote "
                "far more of the card. The A-5 propositions are declared here "
                "and asserted by this record's own content gate, reg-code slot "
                "and reg-desc separately.",
            "ambiguous_reported_not_corrected":
                "QB4_B.html page-level provenance disclaimer lists BMP5 among "
                "the publications the bank was derived from. That is a "
                "historical statement about sources used, not current teaching, "
                "and is reported rather than swept.",
        },
        "invariants": {
            "canonical_questions_before": 761,
            "canonical_questions_after": 761,
            "question_bearing_files": 86,
            "new_cards": 0,
            "corrected_cards": len(reach_entries),
            "revision_surfaces_corrected": 3,
            "sites_corrected": 8,
        },
        "review": {
            "gate": "tools/oral/validate_correction_t5reach.py",
            "mutation_suite": "tools/oral/mutate_correction_t5reach.py",
            "independent_review":
                "NOT YET - this record is produced by the same session that made "
                "the edits.",
        },
        # Revision surfaces carry no q-card, so no release guard can pin them.
        # They are recorded here for scope completeness WITHOUT a digest, per
        # the schema note on `artefacts`, and their propositions are asserted
        # instead by this correction's own content gate - which is the only
        # thing that can guard them.
        "known_traps_entries": [94, 95],
        "artefacts": [
            {"path": "meoclass1/QB9_A_CheatSheet.html",
             "classification": "DEPENDENCY_CORRECTION",
             "rationale": "Carries no q-card, so it takes no digest pin, but it "
                          "held the two proposition-less MSC.1/Circ.1606 pills "
                          "the parent card removed as unusable. N-2. The whole "
                          "cs-row goes with them: two pills removed from a row "
                          "that held nothing else would leave an empty promise, "
                          "which is the defect family next door.",
             "guarded_by": "validate_correction_t5reach.py"},
            {"path": "meoclass1/QB5_B_CheatSheet.html",
             "classification": "DEPENDENCY_CORRECTION",
             "rationale": "Carries no q-card. Its Q34 answer taught 'BMP5 "
                          "procedures' as current. N-4a.",
             "guarded_by": "validate_correction_t5reach.py"},
            {"path": "meoclass1/QB4_H_cheatsheet.html",
             "classification": "DEPENDENCY_CORRECTION",
             "rationale": "Carries no q-card. Its row 11 examiner cue '\"BMP5 "
                          "details\"' is QUOTED wording and is KEPT - QB4_H#q11 "
                          "exists precisely because examiners still ask for BMP5 "
                          "by name. Only the ANSWER cell is qualified, with the "
                          "predecessor banner the parent card already carries. "
                          "N-4b.",
             "guarded_by": "validate_correction_t5reach.py"},
            {"path": "meoclass1/known_traps.md",
             "classification": "GOVERNANCE_RECORD",
             "known_traps_entry": 94,
             "rationale": "Entry 94 records why a sweep driven by a finding's "
                          "card list leaves siblings behind, and that 94 of 102 "
                          "corpus occurrences are KEEP. Entry 95 records that a "
                          "cheat sheet takes no digest pin, so a content gate is "
                          "the only thing that can guard it.",
             "guarded_by": "validate_correction_t5reach.py"},
            {"path": "tools/oral/apply_corr_t5_reach.py",
             "classification": "GOVERNANCE_RECORD",
             "rationale": "The applier, with the KEEP boundary stated in code "
                          "rather than in prose.",
             "guarded_by": "validate_correction_t5reach.py"},
        ],
        "cards": reach_entries,
    }

    # ---------------------------------------------------------------- 3
    hyd_what = {
        ("QB2_A.html", "q8"):
            "'4 to 6 Bar' asserted as the 'minimum operational pressure range "
            "required at the furthest hydrant' - roughly double the SOLAS floor "
            "and carrying no source - replaced by SOLAS II-2/10.2.1.6 with both "
            "of its cargo-ship limbs, and a sentence saying that a higher "
            "monitor-throw figure is a design target and not a SOLAS minimum. "
            "This is Tranche 5 finding N-3.",
        ("QB2_B.html", "q18"):
            "the correct 0.27 N/mm2 was stated as 'the mandatory minimum "
            "pressure' with no threshold, so it read as governing every cargo "
            "ship. The 6,000 GT limb is restored in both directions.",
        ("QB2_H.html", "q2"):
            "'the 4.0 bar minimum required at the highest hydrant' replaced by "
            "the governing provision and its two limbs. This site was found by "
            "the Pass-1 census, not by the tranche, and it contradicted the "
            "already-corrected QB9_B#q5 in the same corpus.",
    }
    hyd_entries = []
    for i, (fname, a) in enumerate(HYDRANT_CARDS, 1):
        prior = None
        pre_override = pre[fname][a]
        # N-3 is the reported defect; the other two are the same false
        # proposition found elsewhere by the census.
        klass = ("PRIMARY_CORRECTION" if (fname, a) == ("QB2_A.html", "q8")
                 else "PROPAGATED_FACT_CORRECTION")
        hyd_entries.append(card_entry(
            fname, a, "T5-HYDRANT-%02d" % i, klass,
            hyd_what[(fname, a)], pre_override=pre_override,
            supersedes_override=prior, records=records))

    hydrant = {
        "correction_id": "CORR-T5-HYDRANT-20260906",
        "kind": "POST_RELEASE_CORRECTION",
        "status": "AUTHORISED",
        "origin": "known_defect_family_remediation_pass_1",
        "date": DATE,
        "baseline_commit": BASELINE,
        "governing_commits": list(GOVERNING),
        "authorisation_source":
            "MIW KNOWN-DEFECT-FAMILY REMEDIATION - PASS 1 instruction of "
            "6 September 2026, sections 7 and 8. Section 8 authorises N-3 by "
            "name and states the governing provision and both cargo-ship "
            "figures. Section 7 authorises correcting a census hit where held "
            "primary source directly adjudicates it or where the proposition "
            "conflicts with another corrected card; both further sites meet "
            "that test.",
        "title":
            "A hard number presented to the candidate under regulatory wording "
            "for a quantity SOLAS actually fixes, and the number is not "
            "SOLAS's. Three sites: a '4 to 6 Bar' required minimum, a '4.0 bar "
            "minimum required', and the correct figure with only one of its two "
            "limbs.",
        "candidate_claim":
            "Not a candidate report. Tranche 5 finding N-3, plus two sites the "
            "Pass-1 numeric census added.",
        "candidate_verdict":
            "UPHELD. The 4-6 bar and 4.0 bar figures are unsupported and "
            "contradict held SOLAS text; they also contradicted QB9_B#q5, which "
            "was corrected to the governing figures on 6 September 2026. A "
            "single-limb version of a two-limb rule is not a blurred rule - it "
            "is simply wrong for every ship on the other side of the threshold, "
            "the same shape as the MSC.535(107) lifeboat-ventilation defect.",
        "authority":
            "SOLAS II-2/10.2.1.6 (Consolidated Edition 2024, held): minimum "
            "pressure at the hydrants with the two required pumps delivering "
            "simultaneously - for cargo ships 0.27 N/mm2 at 6,000 GT and "
            "upwards and 0.25 N/mm2 below 6,000 GT. SOURCE RELIED ON: "
            "SRC-SOLAS-CONSOLIDATED-2024. The passenger-ship limbs are "
            "deliberately NOT introduced: these are container and cargo cards, "
            "and importing a limb the card never addressed would be authoring "
            "rather than correcting.",
        "propagation": {
            "derived_surfaces":
                "NONE. No question stem changed; 761 / 86 unchanged.",
            "hub_date": "NOT ADVANCED.",
            "deferred_to_k_items":
                "The census also found the weathertightness hose test stated as "
                "'at least 1 bar (100 kPa)' on QB2_B#q16 and as '0.2 N/mm2 "
                "(2 bar)' on QB2_B#q13 and QB2_A#q21 - an internal "
                "contradiction inside one file. No governing source for the "
                "hose test is held in the repository, so it is raised as a "
                "source-acquisition item and NOT guessed. QB2_F#q2's '0.27 MPa "
                "at deck monitors' applies the hydrant figure to a different "
                "location and is reported as AMBIGUOUS.",
        },
        "invariants": {
            "canonical_questions_before": 761,
            "canonical_questions_after": 761,
            "question_bearing_files": 86,
            "new_cards": 0,
            "corrected_cards": len(hyd_entries),
        },
        "review": {
            "gate": "tools/oral/validate_correction_t5hydrant.py",
            "mutation_suite": "tools/oral/mutate_correction_t5hydrant.py",
            "independent_review":
                "NOT YET - this record is produced by the same session that made "
                "the edits.",
        },
        "known_traps_entries": [93],
        "artefacts": [
            {"path": "meoclass1/known_traps.md",
             "classification": "GOVERNANCE_RECORD",
             "known_traps_entry": 93,
             "rationale": "Entry 93 records the governing figures and their "
                          "6,000 GT scope, that internal contradiction against a "
                          "corrected sibling is what promotes a numeric hit out "
                          "of a 1,034-hit census, and that a single-limb version "
                          "of a two-limb rule is wrong rather than vague.",
             "guarded_by": "validate_correction_t5hydrant.py"},
            {"path": "tools/oral/apply_corr_t5_hydrant.py",
             "classification": "GOVERNANCE_RECORD",
             "rationale": "The applier, carrying the governing sentence once so "
                          "the three sites cannot drift apart.",
             "guarded_by": "validate_correction_t5hydrant.py"},
        ],
        "cards": hyd_entries,
    }

    outputs = [
        ("correction_corr_t5_ddcascade_20260906_manifest.json", cascade),
        ("correction_corr_t5_reach_20260906_manifest.json", reach),
        ("correction_corr_t5_hydrant_20260906_manifest.json", hydrant),
    ]
    for name, obj in outputs:
        blob = json.dumps(obj, indent=1, ensure_ascii=False) + "\n"
        print("%-56s %3d cards" % (name, len(obj["cards"])))
        if args.write:
            (HERE / name).write_bytes(blob.encode("utf-8").replace(b"\r\n", b"\n"))
    print("\n%s" % ("WRITTEN" if args.write else "DRY RUN"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
