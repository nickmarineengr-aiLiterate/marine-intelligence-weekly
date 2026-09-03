#!/usr/bin/env python3
"""
Mutation suite for CORR-CIC-STEM-20260903  (QB8_C#q4).

`validate_correction_cicstem.py` reports 19 green checks. Green output alone is
indistinguishable from a validator that reads nothing, so every proposition is
attacked here and each mutation must trip the check that OWNS it -- never a
digest pin, which fires on any byte change at all (enforced by
oral_content_mutation.DIGEST_PINS).

THREE MUTATIONS EARN THEIR PLACE PARTICULARLY.

E is the one this correction exists to make impossible. It leaves the stem
saying a real-sounding campaign the body never mentions -- exactly the shape of
the original defect, a card that disagrees with itself -- and it must be caught
by `stem_and_body_agree` rather than by any single-phrase check. Nothing in the
release suite had that control before this correction.

N plants the rejected expansion on a DIFFERENT candidate page and leaves
QB8_C perfect. That is the half-finished repair of known_traps entry 51: the
sweep that found this defect found QB8_C alone, and a guard that only watches
the reported card would never notice the term reappearing elsewhere.

D AND G BOTH ESCAPED ON THEIR FIRST FORM, and the reason is worth keeping.
Each originally rewrote a single <h4> heading. Both checks stayed green,
because the card names the PSC campaign correctly FOUR times and the industry
sense TWICE -- so removing one instance left the proposition intact and the
mutation demonstrated nothing about the guard. A mutation must delete the
PROPOSITION, not one of its instances; a phrase-count of one is an assumption,
not a fact, and here it was wrong in both directions.

O deletes the rejected expansion from the correction's own changelog note. The
guard grants that note a quoting exemption under SKILL.md 8.2a rule 2, and an
exemption nobody checks is an amnesty: if the note stops quoting the wrong
term, the exemption is stale and must be removed rather than left standing as
a permanent hole in the negative sweep.
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    edit_json, run_suite, sub_in_file)

CARD = REPO / "meoclass1/QB8_C.html"
MANIFEST = HERE / "correction_corr_cic_stem_20260903_manifest.json"
INDEX = REPO / "meoclass1/qb_content_index.json"
GOVERNED = HERE / "qb_content_index_governed.json"
HUB = REPO / "meoclass1/index.html"
EXAMINER = REPO / "meoclass1/examiner-index.html"
TOPICS = REPO / "meoclass1/topics.html"
MAPPINGS = REPO / "docs/study/study_mappings.json"
OTHER_PAGE = REPO / "meoclass1/QB8_D.html"
PROBE = "validate_correction_cicstem.py"

STEM = ('<div class="q-text">CIC (Concentrated Inspection Campaign / '
        'Cargo Integrity Check) — explain in detail.</div>')
TYPE2 = ('<h4>CIC Type 2: PSC Concentrated Inspection Campaign '
         '(Tokyo MOU / Paris MOU)</h4>')


def _set_status(value):
    def mutate(d):
        d["status"] = value
    return mutate


def _index_text(new):
    def mutate(d):
        for q in d["files"]["QB8_C.html"]["questions"]:
            if q["anchor"] == "q4":
                q["text"] = new
    return mutate


def _mapping_text(new):
    def mutate(d):
        d["mappings"]["QB8_C#q4"]["text"] = new
    return mutate


def _drop_changelog_quote(d):
    for e in d["recently_updated"]:
        e["note"] = e["note"].replace("Consolidated Inspection Campaign",
                                      "wrong campaign name")


MUTATIONS = [
    ("A", "reinstate the rejected expansion in the q4 stem",
     sub_in_file(CARD, STEM,
                 STEM.replace("Concentrated", "Consolidated")),
     "stem_never_says_consolidated"),

    ("B", "strip the expansion out of the stem entirely",
     sub_in_file(CARD, STEM,
                 '<div class="q-text">CIC — explain in detail.</div>'),
     "stem_uses_concentrated"),

    ("C", "reinstate the rejected expansion in the answer body",
     sub_in_file(CARD, TYPE2, TYPE2.replace("Concentrated", "Consolidated")),
     "body_never_says_consolidated"),

    ("D", "strip the campaign's correct name out of the answer entirely",
     # EVERY instance, not the heading alone. The body names the campaign
     # correctly four times, so removing one leaves the proposition standing
     # and the mutation proves nothing -- see the escape note above.
     sub_in_file(CARD, "Concentrated Inspection Campaign",
                 "Inspection Campaign"),
     "body_teaches_psc_concentrated"),

    ("E", "make the stem name a campaign the body never teaches",
     sub_in_file(CARD, STEM,
                 STEM.replace("Concentrated", "Coordinated")),
     "stem_and_body_agree"),

    ("F", "move the campaign window off the published dates",
     sub_in_file(CARD, "from 1 September to 30 November",
                 "from 1 January to 31 March"),
     "body_window_retained"),

    ("G", "drop the industry Cargo Integrity Check sense entirely",
     # Again every instance: the heading and the sentence beneath it both
     # name it, so mutating only the heading leaves the sense taught.
     sub_in_file(CARD, "Cargo Integrity Check", "Container Care Programme"),
     "body_both_senses_retained"),

    ("H", "delete the pre-published questionnaire mechanism",
     sub_in_file(CARD, "pre-published questionnaire",
                 "pre-published checklist of interest"),
     "body_questionnaire_mechanism_retained"),

    ("I", "regress the generated content-index display text",
     edit_json(INDEX, _index_text(
         "CIC (Consolidated Inspection Campaign / Cargo Integrity Check) "
         "— explain in detail.")),
     "derived_content_index"),

    ("J", "regress the hub search record",
     sub_in_file(HUB,
                 '{"q": "CIC (Concentrated Inspection Campaign',
                 '{"q": "CIC (Consolidated Inspection Campaign'),
     "derived_hub_search_records"),

    ("K", "regress the generated examiner index display text",
     sub_in_file(EXAMINER, "CIC (Concentrated Inspection Campaign",
                 "CIC (Consolidated Inspection Campaign"),
     "derived_examiner_index"),

    ("L", "regress the topic page question list",
     sub_in_file(TOPICS, "CIC (Concentrated Inspection Campaign",
                 "CIC (Consolidated Inspection Campaign"),
     "derived_topic_pages"),

    ("M", "regress the study mapping store",
     edit_json(MAPPINGS, _mapping_text(
         "CIC (Consolidated Inspection Campaign / Cargo Integrity Check) "
         "— explain in detail.")),
     "derived_study_mappings"),

    ("N", "plant the rejected expansion on a DIFFERENT candidate page",
     sub_in_file(OTHER_PAGE, "</body>",
                 "<p>Consolidated Inspection Campaign</p></body>", 1),
     "no_candidate_page_says_consolidated"),

    ("O", "remove the quote the changelog exemption is granted for",
     edit_json(GOVERNED, _drop_changelog_quote),
     "changelog_quoting_exemptions_are_live"),

    ("P", "mark the correction record superseded",
     edit_json(MANIFEST, _set_status("SUPERSEDED")),
     "correction_record_authorised"),
]

WATCHED = [CARD, MANIFEST, INDEX, GOVERNED, HUB, EXAMINER, TOPICS, MAPPINGS,
           OTHER_PAGE]

if __name__ == "__main__":
    raise SystemExit(run_suite(
        "mutation suite: CORR-CIC-STEM-20260903 (QB8_C#q4)",
        PROBE, MUTATIONS, WATCHED))
