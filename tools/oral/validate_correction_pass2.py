#!/usr/bin/env python3
"""Content gate for the six Pass-2 correction records.

Design rules this gate is written against (Pass-2 instruction section 17):

  * PROPOSITION-LEVEL, not token-level. Every check that could be satisfied by
    a spelling is written against the claim instead. The IACS check does not
    look for the string "12"; it counts the societies the 60-second answer
    actually names, so rewording the sentence cannot satisfy it and dropping a
    society cannot hide behind a correct-looking count.

  * LAYER-SPECIFIC where the memorisation layer matters. QB4_E carried the
    right list in one layer and the wrong count in three others, and QB10_B
    carried the lowering-speed claim in two. A card-wide "is the correct text
    present somewhere" check passes on exactly the state these cards were
    found in, so each candidate-facing layer is extracted and guarded by name.

  * TEACHING IS CHECKED WITH PROVENANCE REMOVED. Every version stamp written
    this pass quotes the defective wording in order to record its removal, so
    a naive card-wide search for the old claim finds it in the footer and a
    naive absence check goes red on its own audit trail. `teaching()` strips
    the q-footer before any content assertion runs.

  * NO LITERAL-TRUE CHECKS, and no check whose subject is this record. A gate
    asserting that its own manifest exists proves nothing about the corpus.
    Schema and pin integrity belong to validate_corrections.py, which owns
    them for every record; this gate only asserts CONTENT.

  * RENDERED TEXT, not source text, where the defect was a rendering one. The
    unescaped "<" in QB10_B was invisible to every source-side check because
    the source bytes were complete. `rendered()` drops what a browser drops.
"""
from __future__ import annotations

import html as htmllib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio, read_text  # noqa: E402

enable_utf8_stdio()

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-58s %s" % ("PASS" if ok else "FAIL", check, detail))


# ---------------------------------------------------------------------------
# extraction
# ---------------------------------------------------------------------------

def card_html(page: str, anchor: str) -> str:
    """One card's raw markup, by balanced-div scan."""
    start = page.find('id="%s"' % anchor)
    assert start >= 0, "anchor not found: %s" % anchor
    start = page.rfind('<div class="q-card', 0, start)
    assert start >= 0, "card not found: %s" % anchor
    depth, pos = 0, start
    pat = re.compile(r"<div\b|</div>")
    while True:
        m = pat.search(page, pos)
        if not m:
            break
        depth += -1 if m.group(0) == "</div>" else 1
        pos = m.end()
        if depth == 0:
            break
    return page[start:pos]


def card(file_name: str, anchor: str) -> str:
    return card_html(read_text(QB / file_name), anchor)


def teaching(markup: str) -> str:
    """The card with its provenance footer removed.

    The version stamps written this pass QUOTE the defective wording in order
    to record what was removed. Any absence assertion run over the whole card
    would therefore fail on the correction's own audit trail -- which is trap
    89, and the reason this function exists rather than a card-wide search.
    """
    cut = markup.find('<div class="q-footer"')
    if cut < 0:
        cut = markup.find('<span class="q-version"')
    return markup if cut < 0 else markup[:cut]


def flatten(markup: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", markup)))


def rendered(markup: str) -> str:
    """What a BROWSER shows, which is not what the source contains.

    An unescaped "<" opens a tag as far as a parser is concerned, and
    everything up to the next ">" disappears from the page. Stripping tags with
    a `<[^>]+>` pattern models exactly that, so text lost this way is lost here
    too -- whereas reading the source bytes would show it present.
    """
    return flatten(markup)


#: Cues that turn a claim into its own denial. A corrected card frequently has
#: to NAME the defect in order to warn against it -- "not UR Z15", "there is no
#: universal rule that cover becomes void", "say X, not Y" -- and a check that
#: cannot tell an assertion from a warning goes red on the correction itself.
#: That is trap 89 in the absence-check direction: the first draft of this gate
#: failed six checks, every one of them on wording the correction had added.
_NEGATION = re.compile(
    r"(?:\bno\b|\bnot\b|\bnever\b|\bnothing\b|rather than|instead of|"
    r"does not|is not|was not|say[^.]{0,40}?,\s*$|there is no|no universal|"
    r"no such|to hedge over|deliberately says)",
    re.I)


def asserts(text: str, pattern: str, window: int = 130):
    """First match of `pattern` that the card ASSERTS rather than denies.

    A match is treated as a denial when a negation cue appears in the `window`
    characters immediately before it. The window is deliberately short: a
    negation three sentences away does not disarm a fresh assertion, so a
    mutation that reintroduces the defective claim in its own sentence is still
    caught. Returns the match, or None if every occurrence is a denial.
    """
    for m in re.finditer(pattern, text, re.I | re.S):
        # The preceding window catches "there is no rule that cover is void".
        # The matched span itself catches the contrast form -- say "cover may
        # be prejudiced", NOT "insurance is void" -- where the negation follows
        # the words rather than preceding them. A claim that contains its own
        # negation is a contrast, not an assertion.
        prefix = text[max(0, m.start() - window):m.start()]
        # Negation scopes to its own SENTENCE. Mutations A/B/F escaped the
        # first draft because an unrelated "is not a Member." or "do not tell
        # an examiner" one sentence earlier disarmed a fresh assertion. Clip
        # the prefix at the last sentence break so only same-sentence negation
        # counts.
        cut = max(prefix.rfind(". "), prefix.rfind("; "), prefix.rfind("? "))
        if cut >= 0:
            prefix = prefix[cut + 2:]
        if _NEGATION.search(prefix):
            continue
        if _NEGATION.search(m.group(0)):
            continue
        return m
    return None


#: Every visible layer label the guarded cards use. A layer ENDS where the next
#: one begins; without this list a fixed-width window runs on into the layer
#: below, and mutation A escaped exactly that way -- KR was deleted from the
#: 60-second list and the check still found "Korean Register" further down, in
#: the detail list the window had swallowed.
LAYER_LABELS = (
    "15-Second Answer", "60-Second Answer", "Numbers to Memorise",
    "Numbers & Regulations to Memorise", "Numbers / Regs", "Key Numbers",
    "List of Current Members", "Role of IACS", "CE Oral Tip", "CE Relevance",
    "Trap Questions", "Trap Warning", "Common CE Failures", "Casualty Link",
    "Examiner Chain", "On My Vessel", "Regulatory References",
    "Lifeboat lowering speed", "Operational and Legal Distinctions",
    "The Five Levels", "Deep Dive",
)


def layer(markup: str, label: str) -> str:
    """The text of one named candidate-facing layer, bounded by the next label.

    Layers are found by their visible label rather than by class name, because
    the class names differ across generations of the corpus (`oral-box`,
    `practice-block`) and a gate keyed to one of them silently stops guarding
    a card authored under the other.
    """
    flat = flatten(markup)
    i = flat.find(label)
    assert i >= 0, "layer label absent: %s" % label
    start = i + len(label)
    ends = [flat.find(other, start) for other in LAYER_LABELS
            if other != label and flat.find(other, start) >= 0]
    return flat[i:min(ends)] if ends else flat[i:]


# ---------------------------------------------------------------------------
# 1. QB4_E q12 -- IACS membership
# ---------------------------------------------------------------------------

SOCIETIES = ["ABS", "Bureau Veritas", "China Classification", "Croatian Register",
             "DNV", "Indian Register", "Korean Register", "Lloyd", "Kaiji",
             "Polski", "Registro Italiano", "Loydu"]


def check_iacs() -> None:
    c = teaching(card("QB4_E.html", "q12"))
    sixty = layer(c, "60-Second Answer")

    # The proposition is "the enumerated list is complete", so the check counts
    # societies rather than trusting a numeral the card states about itself.
    named = [s for s in SOCIETIES if s in sixty]
    report("iacs_60s_enumerates_all_twelve_societies", len(named) == 12,
           "named=%d missing=%s" % (len(named),
                                    [s for s in SOCIETIES if s not in named] or "none"))

    # KR by name, because KR is the one that was missing and a count check
    # alone would pass on any twelve.
    report("iacs_60s_names_korean_register",
           "Korean Register" in sixty or re.search(r"\bKR\b", sixty) is not None,
           "the society the card had dropped")

    fifteen = layer(c, "15-Second Answer")
    report("iacs_15s_names_korean_register", re.search(r"\bKR\b", fifteen) is not None,
           "15-second layer guarded separately from 60-second")

    # The hedge is a proposition, not a string: "some number depending on TL".
    flat = flatten(c)
    hedge = asserts(flat, r"(?:\b1[01]\b|eleven)\s*(?:or|/|to)\s*(?:\b12\b|twelve)"
                          r"|depending on (?:the inclusion|whether)"
                          r"|(?:\b12\b|twelve)\s*(?:or|/)\s*(?:\b1[01]\b|eleven)")
    report("iacs_no_count_ambiguity_hedge", hedge is None,
           "found=%r" % (hedge.group(0) if hedge else None))

    # An eleven-count claim in ANY layer, however worded.
    eleven = re.search(r"(?:\b11\b|eleven)\s+(?:full\s+)?(?:current\s+)?members?"
                       r"|members?\s+(?:list\s+)?to\s+(?:\b11\b|eleven)"
                       r"|consists of (?:\b11\b|eleven)", flat, re.I)
    report("iacs_no_layer_claims_eleven_members", eleven is None,
           "found=%r" % (eleven.group(0) if eleven else None))

    report("iacs_scaffold_removed",
           "Below are Q13-Q15" not in flat and "------------------------" not in c,
           "authoring scaffold and rule gone from the CE tip")


# ---------------------------------------------------------------------------
# 2. QB4_C q5 -- PR1C suspension / withdrawal
# ---------------------------------------------------------------------------

def check_pr1c() -> None:
    c = teaching(card("QB4_C.html", "q5"))
    flat = flatten(c)

    # The defect was CONFLATION, so the check is that both limbs are present
    # AND distinguished -- not that a clause number appears.
    report("pr1c_automatic_limb_is_surveys",
           re.search(r"overdue periodical survey.{0,400}?automatic", flat, re.S | re.I)
           is not None,
           "overdue survey -> automatic suspension")
    report("pr1c_procedure_limb_is_condition_of_class",
           re.search(r"overdue condition of class.{0,400}?subject to a suspension procedure",
                     flat, re.S | re.I) is not None,
           "overdue CoC -> suspension PROCEDURE, not automatic")
    report("pr1c_limbs_are_contrasted_not_merged",
           re.search(r"not automatic|that is not automatic|rather than automatic", flat, re.I)
           is not None,
           "the distinction is stated, not merely implied by ordering")

    # "certain", not "all". Written as a proposition so a reworded overstatement
    # is still caught.
    over = asserts(flat, r"all statutory certificates? (?:invalid|become invalid|are invalid)"
                         r"|rendering all statutory|every statutory certificate")
    report("pr1c_no_all_statutory_certificates_claim", over is None,
           "found=%r" % (over.group(0) if over else None))
    report("pr1c_certain_statutory_certificates_taught",
           re.search(r"certain\s+statutory certificates", flat, re.I) is not None,
           "B.1.3 as written")

    # Guarded in BOTH spoken layers. A card-wide search passes while the
    # 60-second answer has lost the limb entirely, because the 15-second answer
    # still carries it -- which is mutation I, and which section 17 forbids.
    notify = r"Owner and (?:to )?(?:the )?Flag State"
    for name, text in (("15s", layer(c, "15-Second Answer")),
                       ("60s", layer(c, "60-Second Answer"))):
        report("pr1c_%s_owner_and_flag_notification_taught" % name,
               re.search(notify, text) is not None,
               "B.1.1 -- absent from the card before this pass")

    # Insurance: no universal-void claim in any layer, in any wording.
    void = asserts(flat, r"(?:insurance|cover|coverage|P&I|H&M)[^.]{0,90}?"
                         r"(?:void|avoid|lapse|invalidat|cease|null)"
                         r"|(?:void|avoid|freeze|invalidat)\w*[^.]{0,50}?"
                         r"(?:insurance|cover|coverage)")
    report("pr1c_no_universal_insurance_void_claim", void is None,
           "found=%r" % (void.group(0) if void else None))
    report("pr1c_class_warranty_framing_present",
           "class warranty" in flat.lower(),
           "the accurate replacement, not merely a deletion")

    # The false governing citation, in every layer that carried it.
    z15 = asserts(flat, r"UR\s*Z15")
    report("pr1c_no_ur_z15_attribution", z15 is None,
           "found=%r -- the card may WARN about Z15, never cite it" % (z15.group(0) if z15 else None))
    report("pr1c_governing_instrument_is_pr1c",
           len(re.findall(r"PR1C", flat)) >= 3,
           "named in reg box, numbers block and body")
    report("pr1c_six_month_withdrawal_rule_taught",
           re.search(r"six\s*\(?6?\)?\s*months?", flat, re.I) is not None,
           "A.4.1")

    # Markdown escape artefacts that reached the candidate.
    report("pr1c_no_markdown_escape_artefacts",
           "H\\&" not in c and ":**" not in flat,
           "backslash-escaped ampersand and stray bold markers")


# ---------------------------------------------------------------------------
# 3. QB8_A q3 -- alliance currentness
# ---------------------------------------------------------------------------

def check_alliance() -> None:
    c = teaching(card("QB8_A.html", "q3"))
    flat = flatten(c)

    # A retired alliance named as a CURRENT example. The card may still discuss
    # 2M historically -- and does -- so the check is about the claim, not the
    # token: no retired name may appear as an example of what a consortium is.
    for name, pattern in [("2M", r"\b2M\b"), ("THE Alliance", r"THE Alliance")]:
        hits = [m.start() for m in re.finditer(pattern, flat)]
        bad = [h for h in hits
               if re.search(r"such as|e\.g\.|for example|like",
                            flat[max(0, h - 90):h], re.I)]
        report("alliance_%s_not_offered_as_current_example"
               % name.replace(" ", "_").lower(),
               not bad, "example-context hits=%d of %d" % (len(bad), len(hits)))

    for name in ("Gemini", "Premier Alliance", "Ocean Alliance"):
        report("alliance_current_grouping_named_%s" % name.split()[0].lower(),
               name in flat, "the 2026 line-up")
    report("alliance_2m_end_is_dated",
           re.search(r"2M.{0,120}?(?:ended|no longer exists)", flat, re.S | re.I) is not None
           and "January 2025" in flat,
           "stated as ended, with its date")

    report("alliance_cber_expiry_taught",
           "25 April 2024" in flat and re.search(r"expired", flat, re.I) is not None,
           "906/2009 lapsed, not merely 'historical'")

    # The BAF ownership claim, as a proposition.
    baf = asserts(flat, r"(?:BAF|Bunker Adjustment Factor|surcharge)[^.]{0,120}?"
                        r"(?:managed|administered|set|controlled|owned|run|handled)"
                        r"[^.]{0,40}?(?:engineering|engine department|engine room|"
                        r"chief engineer)"
                        r"|(?:engineering|engine department|engine room)[^.]{0,90}?"
                        r"(?:manages|administers|sets|controls)[^.]{0,40}?"
                        r"(?:BAF|Bunker Adjustment Factor|surcharge)"
                        r"|baseline projections managed by the commercial BAF")
    report("alliance_no_engine_room_owns_baf_claim", baf is None,
           "found=%r" % (baf.group(0)[:60] if baf else None))
    report("alliance_baf_ownership_corrected",
           re.search(r"commercial department", flat, re.I) is not None,
           "who actually sets the surcharge")

    scfi = re.search(r"led to an unprecedented increase.{0,120}?historic highs", flat, re.S | re.I)
    report("alliance_no_scfi_sole_cause_claim", scfi is None,
           "the Ever Given causal overstatement")


# ---------------------------------------------------------------------------
# 4. QB5_A q4 -- human element
# ---------------------------------------------------------------------------

def check_human() -> None:
    c = teaching(card("QB5_A.html", "q4"))
    flat = flatten(c)

    # The two numbers the block exists to teach. Checked INSIDE the block, not
    # card-wide: 1943 appears in the 15-second answer and in a CE-failures
    # bullet, so a card-wide search passes on exactly the broken state.
    numbers = layer(c, "Numbers to Memorise")
    report("human_numbers_block_carries_the_year", "1943" in numbers,
           "the list item had lost it from the markup")
    report("human_numbers_block_carries_the_level_count",
           re.search(r"\b5\b\s*levels|five\s*levels", numbers, re.I) is not None,
           "the list item had lost it from the markup")
    report("human_numbers_block_has_no_empty_list_item",
           not re.search(r"<li>\s*(?:&mdash;|—|-)?\s*(?:Maslow theory published|"
                         r"levels \(pyramid)", c),
           "no item beginning where its number should be")

    # False legal attribution, as a proposition.
    mlc = asserts(flat, r"MLC\s*Reg\.?\s*1\.4[^)]{0,60}Fair Treatment", window=40)
    report("human_no_mlc_1_4_fair_treatment_attribution", mlc is None,
           "found=%r" % (mlc.group(0) if mlc else None))
    report("human_mlc_1_4_correctly_described",
           re.search(r"1\.4 is\s*(?:<em>)?\s*Recruitment and placement", flat, re.I)
           is not None,
           "and the row now says esteem has no MLC hook")

    # Maslow distortion.
    rigid = re.search(r"Maslow[^.]{0,40}is strictly upward progression", flat, re.I)
    report("human_no_strict_upward_progression_claim", rigid is None,
           "found=%r" % (rigid.group(0) if rigid else None))

    # Fabricated anecdote: the invented figures and the invented effect.
    for label, pattern in [
        ("invented_port_stay", r"prolonged port stay \(10 days\)"),
        ("invented_roster_figure", r"24 hours'? off-duty every third day"),
        ("invented_recovery_time",
         r"(?:recovered|recovery|motivation returned)[^.]{0,30}?within\s+\d+\s*"
         r"(?:hours?|days?|weeks?)"),
        ("invented_effect_name", r"restoration effect"),
    ]:
        m = re.search(pattern, flat, re.I)
        # The replacement text mentions that no such effect exists, so the
        # effect-name check must not fire on the correction's own denial.
        if label == "invented_effect_name" and m:
            ctx = flat[max(0, m.start() - 90):m.start()]
            if re.search(r"there is no|no such", ctx, re.I):
                m = None
        report("human_no_%s" % label, m is None,
               "found=%r" % (m.group(0) if m else None))

    report("human_own_ship_guidance_present",
           re.search(r"from your own ship", flat, re.I) is not None,
           "the block still answers the On My Vessel prompt")

    # What the correction promised NOT to change.
    report("human_five_levels_preserved",
           all(w in flat for w in ("Physiological", "Safety", "Esteem",
                                   "Self-Actualisation")),
           "the teaching the card exists for")
    report("human_a2_3_rest_figures_preserved",
           "10 hrs rest / 24 hrs" in flat and "77 hrs rest / 7 days" in flat,
           "correct before, unchanged")


# ---------------------------------------------------------------------------
# 5. QB3_A q5 -- annual close-up scope
# ---------------------------------------------------------------------------

def check_closeup() -> None:
    c = teaching(card("QB3_A.html", "q5"))
    flat = flatten(c)

    report("closeup_scoped_to_single_side_skin_bulk_carriers",
           re.search(r"single side skin bulk carriers?\s*(?:</strong>)?\s*only"
                     r"|single side skin bulk carriers only", flat, re.I) is not None,
           "UR Z10.2 population")
    report("closeup_attributed_to_ur_z10_2",
           re.search(r"UR\s*Z10\.2", flat) is not None, "not a blog")

    # The over-broad scope, as a proposition rather than a phrase.
    broad = re.search(r"close-up[^.]{0,200}?\(bulk carriers/oil tankers\)"
                      r"|Annual Survey Close-Up Extension", flat, re.I)
    report("closeup_no_general_bulker_or_tanker_scope", broad is None,
           "found=%r" % (broad.group(0)[:60] if broad else None))

    # Citation quality is a property of the whole card, not of one bullet.
    report("closeup_no_blog_citation_in_card",
           "marinegyaan" not in c and "[reference]" not in c,
           "tier-6 source and its placeholder anchor text")

    # The correction promised NOT to restate an unsourced figure.
    report("closeup_no_unsourced_percentage_restated",
           not re.search(r"25%\s*of cargo hold side shell", flat, re.I),
           "the figure came from the blog and is not held")

    report("closeup_drydock_teaching_preserved",
           "36 months" in flat and re.search(r"twice in", flat, re.I) is not None,
           "what the question actually asks")


# ---------------------------------------------------------------------------
# 6. QB10_B q1 -- amendment overview
# ---------------------------------------------------------------------------

def check_amend() -> None:
    raw = card("QB10_B.html", "q1")
    c = teaching(raw)
    flat = flatten(c)

    # -- lowering speed, guarded in BOTH layers that carried the claim -------
    formula_layer = layer(c, "Lifeboat lowering speed")
    numbers_layer = layer(c, "Numbers to Memorise")

    for name, text in (("formula_block", formula_layer), ("numbers_block", numbers_layer)):
        replaced = asserts(text,
                           r"(?:replac|supersed|abolish|withdraw|retir)\w*"
                           r"[^.]{0,70}?formula"
                           r"|formula[^.]{0,70}?(?:no longer applies|is withdrawn|"
                           r"has been replaced|was replaced|is superseded|no longer used)"
                           r"|(?:in place of|instead of) the (?:old )?"
                           r"(?:H-dependent )?formula")
        report("amend_%s_no_formula_replaced_claim" % name, replaced is None,
               "found=%r" % (replaced.group(0) if replaced else None))
        report("amend_%s_carries_the_formula" % name,
               re.search(r"0\.4\s*\+\s*0\.02", text) is not None,
               "S = 0.4 + 0.02H survives MSC.554(108)")
        report("amend_%s_states_whichever_is_less" % name,
               re.search(r"whichever is less", text, re.I) is not None,
               "1.0 m/s caps the formula-derived minimum")
        report("amend_%s_cites_msc554" % name,
               "MSC.554(108)" in text, "the resolution that actually did it")

    report("amend_maximum_is_administration_variable",
           re.search(r"Administration may accept", flat, re.I) is not None,
           "6.1.2.10 is a default, not an absolute")

    # -- free-fall / III/33.2 ----------------------------------------------
    removed = re.search(r"removed the 5-knot headway", flat, re.I)
    report("amend_no_requirement_removed_claim", removed is None,
           "found=%r" % (removed.group(0) if removed else None))
    report("amend_iii_33_2_scoped_to_davit_launched",
           re.search(r"davit-launched", flat, re.I) is not None
           and re.search(r"narrowed, not abolished", flat, re.I) is not None,
           "the direction of the amendment")
    report("amend_iii_33_2_scoped_to_cargo_ships",
           re.search(r"cargo ships of 20,000 gross tonnage", flat, re.I) is not None,
           "population is cargo ships, not ships")
    report("amend_cites_msc482", "MSC.482(103)" in flat,
           "the 2024 tranche had no reference at all")

    # -- the rendering defect, checked as a BROWSER sees it -----------------
    # This is the check the source-side gates could not express: the source
    # bytes were complete, and the teaching was still gone from the page.
    page_text = rendered(raw)
    report("amend_2028_compliance_dates_survive_rendering",
           "1 Jan 2028" in page_text and "1 Jan 2029" in page_text,
           "an unescaped '<' was deleting both from the rendered card")
    report("amend_no_unescaped_lt_before_numeral",
           re.search(r"<\d", raw) is None,
           "the mechanism, not just this instance")

    # -- resolution custody -------------------------------------------------
    report("amend_msc535_named_as_ventilation_requirement",
           re.search(r"MSC\.535\(107\)[^.]{0,120}ventilation", flat, re.I) is not None,
           "the requirement MSC.559(108) serves")
    report("amend_msc559_named_as_amending_msc402",
           re.search(r"MSC\.559\(108\)[^.]{0,200}MSC\.402\(96\)", flat, re.S) is not None,
           "MSC.559 is the testing regime, not the ventilation rule")

    # -- perishable self-dating --------------------------------------------
    report("amend_no_self_dating_currency_claim",
           not re.search(r"it is now (?:mid|early|late)-20\d\d", flat, re.I),
           "a card must date itself from its instruments")

    # -- invariants the record claimed -------------------------------------
    report("amend_roro_attribution_preserved",
           re.search(r"MSC\.550\(108\)", flat) is not None,
           "CORR-G1-010's correction is untouched")
    report("amend_msc520_vs_521_discrimination_preserved",
           "MSC.520(106)" in flat and "MSC.521(106)" in flat,
           "the adjacent-resolution trap the card teaches")


def main() -> int:
    print("Pass-2 known-defect remediation -- content gate")
    print("=" * 47)
    for name, fn in (("QB4_E q12  IACS membership", check_iacs),
                     ("QB4_C q5   PR1C suspension", check_pr1c),
                     ("QB8_A q3   alliance currentness", check_alliance),
                     ("QB5_A q4   human element", check_human),
                     ("QB3_A q5   annual close-up scope", check_closeup),
                     ("QB10_B q1  amendment overview", check_amend)):
        print("\n-- %s" % name)
        fn()
    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    for f in FAILS:
        print("  FAIL " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
