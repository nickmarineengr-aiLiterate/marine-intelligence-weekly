#!/usr/bin/env python3
"""Content gates for the five D01-S01 study-path corrections.

Every check here guards a proposition Nixon is about to memorise, so each one
is written to fail on the DEFECT, not on a spelling of it. Three rules were
applied throughout:

1. A negative check is scoped to the layer that taught the defect. A bare
   "HSSC must not appear near class" would fire on the very sentence that
   draws the distinction - the correction names both regimes in one breath,
   because that IS the teaching point.

2. A positive check names the proposition, not the wording. The corrections
   are the remediation lane's prose; a gate that pinned the prose would go red
   on any later editorial pass and teach the next author to route around it.

3. Provenance is excluded before matching. A version stamp QUOTES what it
   removed - that is the audit trail working - and a gate that reads it
   reports the correction as the defect (known_traps #89).
"""
from __future__ import annotations

import hashlib
import html as htmllib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import read_text                                  # noqa: E402
from validate_batch_h_series import card_digests, _balanced_end   # noqa: E402

FAILS: list[str] = []
CHECKS = 0


def report(name: str, ok, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if callable(ok):
        try:
            ok = bool(ok())
        except Exception as exc:                                  # noqa: BLE001
            ok, detail = False, "raised %s: %s" % (type(exc).__name__, exc)
    if not ok:
        FAILS.append(name)
    print("%-4s %-58s %s" % ("PASS" if ok else "FAIL", name, detail))


def flat(raw: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", raw)))


def teaching(block: str) -> str:
    """Candidate-facing text only: the version stamp quotes what it removed."""
    return flat(re.sub(r'<span class="q-version">.*?</span>', " ", block,
                       flags=re.S))


def layer(block: str, label: str) -> str:
    """One named answer layer of a card.

    Card-wide checks proved too coarse: the same proposition is stated in the
    15-second, 60-second and deep-dive layers, so reverting ONE of them left
    the phrase present elsewhere and every card-wide check stayed green. A
    candidate memorises the 15-second layer, so that layer is guarded on its
    own as well as the card as a whole.
    """
    i = block.find(label)
    if i < 0:
        return ""
    j = block.find("<h4", i + len(label))
    k = block.find("</p>", i)
    end = min(x for x in (j, k + 4 if k >= 0 else len(block)) if x > 0)
    return flat(block[i:end])


def card(path: str, anchor: str) -> str:
    raw = read_text(QB / path)
    i = raw.find('<div class="q-card" id="%s"' % anchor)
    assert i >= 0, "%s#%s" % (path, anchor)
    return raw[i:_balanced_end(raw, i)]


def article(path: str, anchor: str) -> str:
    raw = read_text(QB / path)
    i = raw.find('<article class="q-card" id="%s"' % anchor)
    assert i >= 0, "%s#%s" % (path, anchor)
    depth, j, n = 0, i, len(raw)
    while j < n:
        if raw.startswith("<article", j):
            depth += 1
            j += 8
            continue
        if raw.startswith("</article>", j):
            depth -= 1
            j += 10
            if depth == 0:
                break
            continue
        j += 1
    return raw[i:j]


def main() -> int:
    # ============ CORR-D01-HSSC-CLASS : RC-01 / RC-02 ====================
    q9 = card("QB3_B.html", "q9")
    t9 = teaching(q9)

    # The defect is the ATTRIBUTION, so the check is scoped to the class
    # subject. "HSSC" alone is legitimate and now appears in the correction.
    report("RC01_class_system_not_said_to_operate_on_HSSC",
           not re.search(r"(?:class\w*[^.]{0,80}?)"
                         r"(?:operates?\s+on|runs?\s+on)[^.]{0,40}HSSC", t9, re.I)
           and not re.search(r"\b(?:5-year|five-year)\s+HSSC", t9, re.I),
           "no 'class system operates on a 5-year HSSC framework'")
    report("RC01_IACS_HSSC_attribution_gone_corpus_wide",
           not any("IACS HSSC" in read_text(p)
                   for p in sorted(QB.rglob("*.html")))
           and not any("IACS HSSC" in read_text(p)
                       for p in sorted((REPO / "docs").rglob("*.md"))),
           "HSSC guidelines are an IMO Assembly instrument, not an IACS one")
    report("RC01_HSSC_named_as_statutory_where_it_is_mentioned",
           re.search(r"statutory[^.]{0,120}HSSC|HSSC[^.]{0,120}statutory",
                     t9, re.I) is not None,
           "the card states which regime HSSC belongs to")
    report("RC01_1988_protocols_named",
           "1988 Protocol" in t9,
           "the instruments that introduced HSSC")
    report("RC01_class_cycle_attributed_to_class_rules",
           re.search(r"UR\s*Z", t9) is not None,
           "the class cycle's actual basis is named")
    report("RC01_key_distinction_bullet_untouched",
           "Key distinction for exam" in q9
           and "Class Survey = verifies Class rules" in flat(q9),
           "the anchor of the fix survives the fix")

    # VISIBLE text, not raw text: a mutation that merely marked the docking
    # item `hidden` left the words in the file and this check stayed green,
    # while a candidate would never have seen them. Presence in the bytes is
    # not presence on the page.
    from oral_visible import segments                              # noqa: E402
    vis9 = " ".join(t for t, _st, _ln, _cl in segments(q9)).lower()
    report("RC02_survey_list_is_complete",
           all(w in vis9 for w in ("docking", "bottom", "tailshaft", "boiler"))
           and not re.search(r"<li[^>]*\bhidden\b", q9),
           "docking/bottom, tailshaft and boiler are VISIBLE")
    report("RC02_bottom_survey_interval_present",
           "36 months" in t9 and re.search(r"[Tt]wo\b[^.]{0,60}five-year", t9),
           "two in five years, max 36 months")
    report("RC02_intermediate_timing_corrected",
           "at or between the second and third annual survey" in t9.lower()
           and not re.search(r"[Bb]etween\s+2nd\s+and\s+3rd", t9),
           "PR1C A.1.3 ties it to the third annual survey")
    report("RC02_boiler_marked_not_a_CSM_item",
           re.search(r"[Bb]oiler[^.]{0,80}not[^.]{0,30}(?:CSM|continuous)",
                     t9) is not None,
           "known_traps #43")
    report("RC02_regimes_visibly_separate_in_the_reg_box",
           "A.1207(34)" in t9 and "UR Z series" in t9,
           "one row per regime, so the box itself distinguishes them")

    # ============ CORR-D01-INSTRUMENT-LEGAL-EFFECT : RC-03 ================
    skel = read_text(REPO / "docs/study/TOPIC_01_STATUTORY_SURVEYS_AND_CLASS.md")
    body = skel.split("## MENTAL SKELETON", 1)[1]
    # Isolate branch 1 from BOTH ends. Splitting only on "\n2. " left the
    # section's own preamble in the sample, so the length check was measuring
    # 179 words of which ~110 were not the branch at all - it failed a branch
    # that was already short enough, which is the mirror image of a check that
    # passes something it never looked at.
    branch1 = body.split("\n1. ", 1)[1].split("\n2. ", 1)[0]
    # The correction note QUOTES the ladder to say it was struck out, exactly
    # as a version stamp does. Read the branch without its own audit trail.
    b1 = branch1.split("*Corrected", 1)[0]
    report("RC03_ladder_gone_from_the_skeleton",
           not re.search(r"Convention\s*(?:→|->)\s*Protocol", b1),
           "no descending-legal-force chain")
    report("RC03_branch_1_asks_what_makes_it_binding",
           "binding" in b1.lower() and "mandatory" in b1.lower(),
           "legal effect is derived, not ranked")
    report("RC03_protocol_may_be_treaty_law",
           re.search(r"Protocol[^.]{0,60}treaty law", b1, re.I) is not None,
           "the fact the ladder denied")
    report("RC03_code_mandatory_by_incorporation",
           re.search(r"Code[^.]{0,90}mandatory", b1, re.I) is not None,
           "a Code's force comes from the instrument that adopts it")
    report("RC03_resolution_has_no_single_effect",
           re.search(r"Resolution[^.]{0,90}(?:no single|not have one)",
                     b1, re.I) is not None,
           "an MSC resolution adopts mandatory amendments")
    report("RC03_skeleton_still_short",
           len(b1.split()) < 150,
           "%d words - it must be recallable in seconds" % len(b1.split()))
    report("RC03_only_branch_1_changed",
           body.count("\n2. **Entry into force**") == 1
           and "9." in body and "Flag State duties" in body,
           "branches 2-9 intact")

    # ============ CORR-D01-NETZERO-CURRENTNESS : RC-04 ====================
    q2p = article("pastpapers/QP2506.html", "q2")
    t2p = flat(q2p)
    report("RC04_netzero_not_stated_as_adopted",
           not re.search(r"Net-Zero[^.]{0,80}\b(?:was|has been|is)\s+adopted",
                         t2p, re.I)
           and "not adopted until four months after" not in t2p,
           "approval is not adoption")
    report("RC04_current_status_stated",
           "still not been adopted" in t2p and "adjourned for one year" in t2p,
           "MEPC/ES.2 adjourned; MEPC 84 no final agreement")
    report("RC04_no_unverified_future_date_asserted",
           not re.search(r"(?:adopt\w*|reconven\w*|resum\w*)[^.]{0,60}"
                         r"(?:December\s+2026|4\s+December|Dec\s+2026)",
                         t2p, re.I),
           "section 8 forbids asserting an unverified scheduling date")
    report("RC04_reverify_instruction_present",
           "re-verify" in t2p.lower() and "known_traps" in t2p,
           "the volatile part is routed to the register, not frozen")
    report("RC04_sitting_anchored_flashcard_untouched",
           "At the date of this examination it had been circulated but not "
           "adopted." in t2p,
           "a past paper is anchored to its sitting")

    # ============ CORR-D01-COC-PR1C : RC-05 ==============================
    k2 = card("QB1_K.html", "q2")
    tk = teaching(k2)
    report("RC05_overdue_CoC_is_not_taught_as_automatic",
           not re.search(r"(?:overdue|miss\w*)[^.]{0,90}[Cc]ondition of [Cc]lass"
                         r"[^.]{0,90}automatic", tk, re.I)
           and not re.search(r"automatic[^.]{0,60}on an overdue CoC", tk, re.I),
           "PR1C A.2.1 is a suspension PROCEDURE")
    k15 = layer(k2, "15-Second Answer")
    report("RC05_suspension_procedure_named",
           "subject to a suspension procedure" in tk
           and "subject to a suspension procedure" in k15
           and "automatically suspended" not in k15,
           "in the 15-second layer, which is the one that gets memorised")
    report("RC05_automatic_still_attributed_to_overdue_SURVEYS",
           re.search(r"survey[^.]{0,120}automatic", tk, re.I) is not None,
           "A.1.1-A.1.3 - the distinction cuts both ways")
    report("RC05_certain_statutory_certificates_preserved",
           "certain statutory certificates" in tk
           and "implicitly invalidated" in tk
           and "certain statutory certificates" in k15,
           "PR1C B.1.3 - not a blanket collapse, in the 15s layer too")
    report("RC05_no_blanket_statutory_collapse_claim",
           not re.search(r"collapses the statutory certificates", tk, re.I)
           and not re.search(r"all statutory certificates[^.]{0,40}"
                             r"(?:void|invalid|collapse)", tk, re.I),
           "the qualifier is the point")
    report("RC05_owner_and_flag_notification_present",
           re.search(r"in writing[^.]{0,80}Owner[^.]{0,60}Flag", tk, re.I)
           is not None
           and re.search(r"in writing[^.]{0,80}Owner[^.]{0,60}Flag", k15,
                         re.I) is not None,
           "PR1C B.1.1-B.1.2 - the mechanism an examiner asks for")
    report("RC05_six_month_withdrawal_rule_scoped",
           re.search(r"six months?|six \(6\) months", tk, re.I) is not None
           and re.search(r"(?:six months?|six \(6\) months)[^.]{0,140}"
                         r"withdraw", tk, re.I) is not None,
           "A.4.1, with its overdue-surveys/CoC scope")
    report("RC05_no_universal_insurance_void_claim",
           not re.search(r"insurance[^.]{0,60}automatically[^.]{0,30}void",
                         tk, re.I),
           "cover conditional on class is prejudiced - not voided by rule")
    report("RC05_harmonized_floor_caveat_present",
           re.search(r"(?:floor|society'?s? own Rules may)", tk, re.I)
           is not None,
           "PR1C is a floor, not a ceiling")
    report("RC05_IACS_definition_sentence_untouched",
           "specific measures, repairs or surveys to be completed within a "
           "stated time limit in order to retain class" in tk,
           "verbatim correct against PR1C Definitions")
    report("RC05_deeper_layers_agree_with_the_fix",
           "typically automatic when a CoC falls overdue" not in tk
           and not re.search(r"overdue CoC[^.]{0,40}status[^.]{0,120}"
                             r"Class is suspended;", tk),
           "Trap Questions and Numbers no longer contradict the 15s/60s")

    # ============ CORR-D01-IACS-UI : RC-06 ===============================
    h3 = card("QB1_H.html", "q3")
    th = teaching(h3)
    report("RC06_UI_not_universal_flag_binding",
           not re.search(r"become[s]?\s+the\s+standard\s+by\s+which\s+Flag",
                         th, re.I),
           "a UI does not bind a Flag State's interpretation")
    report("RC06_UI_fallback_mechanism_stated",
           "not issued definite instructions" in th
           and re.search(r"instructions govern|Administration has spoken",
                         th, re.I) is not None,
           "it governs silence and yields to instruction")
    report("RC06_PR1C_not_attributed_to_transfer_of_class",
           not re.search(r"PR\s?1C\s*(?:—|-|–|:)?\s*transfer of class",
                         th, re.I),
           "PR1C is the suspension/withdrawal procedure")
    report("RC06_PR1C_given_its_actual_subject",
           re.search(r"PR\s?1C[^.]{0,120}(?:suspension|withdrawal)", th, re.I)
           is not None,
           "the real instrument, on the real proposition")
    report("RC06_no_guessed_transfer_of_class_letter",
           not re.search(r"PR\s?1[A-Z]\b[^.]{0,40}transfer of class", th, re.I),
           "UNRESOLVED stays unasserted")
    report("RC06_PR9_ISM_retained",
           re.search(r"PR\s?9[^.]{0,60}ISM", th, re.I) is not None,
           "verified correct - not collateral damage")
    report("RC06_trap_line_still_contradicts_nothing",
           re.search(r"Flag State may reject a UI", th, re.I) is not None,
           "the body now agrees with the line that was already right")

    # ============ the gate audits ITSELF for the byte trap ===============
    # known_traps #102: a shell heredoc silently turns a backslash-b into a literal
    # 0x08, the regex still compiles, and the alternative can never match.
    # It has now happened FOUR times in this repository, most recently in
    # THIS file's own `hidden` guard - written minutes after the trap was
    # documented, and it made a live mutation escape. Documenting a trap does
    # not prevent it; a check does.
    # The needle is built with chr(8), not written as an escape: the first
    # version of this very check spelled its own needle as a literal
    # backspace and so reported ITSELF as the offender.
    _BS = chr(8)
    control_byte = [str(p.relative_to(REPO)) for p in sorted(
        (REPO / "tools").rglob("*.py")) if _BS in read_text(p)]
    report("no_control_byte_regex_in_the_toolchain", not control_byte,
           str(control_byte or "none - scanned every tools/**/*.py"))

    # ============ the control, and the record ============================
    q1 = article("pastpapers/QP2402.html", "q1")
    report("QP2402_Q1_control_is_byte_identical",
           hashlib.sha256(q1.replace("\r\n", "\n").encode("utf-8")).hexdigest()
           == "e002caeee176a6a01fc8bb70ded01f68f968a37e38606fe6af32e5d8acba0c6b",
           "the session's conceptual control is untouched")

    # Every correction record must pin the bytes it claims to have produced.
    # Only THREE of the five are correction manifests: the skeleton is a
    # markdown study pack and QP2506 q2 is an <article> in a past paper, and
    # the card layer can digest neither. Declaring them as cards made the
    # corpus-wide validator refuse the records - correctly - so they are a
    # governance document instead and their pins are checked from it.
    for name, path in (("hssc_class", "QB3_B.html"),
                       ("coc_pr1c", "QB1_K.html"),
                       ("iacs_ui", "QB1_H.html")):
        man = json.loads(read_text(
            HERE / ("correction_corr_d01_%s_20260907_manifest.json" % name)))
        live = card_digests(read_text(QB / path))
        for rec in man["cards"]:
            got = live[rec["anchor"]]
            report("record_%s_%s_post_digest_matches_the_bytes"
                   % (name, rec["anchor"]),
                   rec["post_edit_digest"] == got,
                   "declared %s" % rec["post_edit_digest"][:16])
            report("record_%s_%s_pre_digest_differs_from_post"
                   % (name, rec["anchor"]),
                   rec["pre_edit_digest"] != rec["post_edit_digest"],
                   "a correction that changed nothing is not a correction")
        report("record_%s_pins_its_governing_commit" % name,
               bool(man.get("governing_commits")),
               str(man.get("governing_commits")))

    # The two propagation cards must be DECLARED, not merely described. They
    # were described in the record's prose first, and the corpus-wide validator
    # reported them as undeclared change - prose is not a declaration.
    hssc = json.loads(read_text(
        HERE / "correction_corr_d01_hssc_class_20260907_manifest.json"))
    report("propagation_cards_are_declared_not_just_described",
           set(c["anchor"] for c in hssc["cards"]) == set(("q9", "q1", "q11")),
           "q9 primary, q1 and q11 propagation")
    # The classification vocabulary is a CLOSED SET, and "PROPAGATION" is not
    # in it - PROPAGATED_FACT_CORRECTION is. An unclassified card fails by
    # design, which is how this was found rather than shipped.
    report("propagation_cards_use_the_schema_vocabulary",
           set(c["classification"] for c in hssc["cards"])
           == set(("PRIMARY_CORRECTION", "PROPAGATED_FACT_CORRECTION")),
           "closed-set classes, not invented ones")

    # The non-card record carries the same pins, re-derived here from live
    # bytes rather than copied out of the record.
    nc = read_text(REPO / ("meoclass1/oral-intelligence/examiner-audit/"
                           "D01_S01_NON_CARD_CORRECTIONS.md"))
    skel_live = hashlib.sha256(
        (REPO / "docs/study/TOPIC_01_STATUTORY_SURVEYS_AND_CLASS.md")
        .read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    qp_live = hashlib.sha256(
        article("pastpapers/QP2506.html", "q2")
        .replace("\r\n", "\n").encode("utf-8")).hexdigest()
    report("non_card_record_exists_and_explains_the_vehicle",
           "D01-S01-NONCARD-20260907" in nc
           and "the schema is usually right" in nc,
           "the schema refused a card it cannot digest, and was right")
    report("non_card_record_pins_the_live_skeleton", skel_live in nc,
           "pin re-derived from the live file")
    report("non_card_record_pins_the_live_past_paper", qp_live in nc,
           "pin re-derived from the live article")


    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: " + ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
