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
import json
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


def strip_all_footers(markup: str) -> str:
    """Whole-page provenance stripper.

    `teaching()` handles one card. A page-wide scan needs the same discipline,
    because every version stamp in this batch quotes the wording it removed.
    """
    out, pos = [], 0
    for m in re.finditer(r'<div class="q-footer"', markup):
        out.append(markup[pos:m.start()])
        depth, i = 0, m.start()
        for tok in re.finditer(r"<div\b|</div>", markup[m.start():]):
            depth += -1 if tok.group(0) == "</div>" else 1
            i = m.start() + tok.end()
            if depth == 0:
                break
        pos = i
    out.append(markup[pos:])
    return "".join(out)


def flatten(markup: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", markup)))


#: Element names a browser will actually open a tag for. A "<" followed by an
#: ASCII letter that is NOT one of these is the only form that eats text -- and
#: there are zero such sites in this corpus. See trap 126: the first draft of
#: this gate modelled "<" + ANY character as tag-opening, which is not how
#: HTML5 tokenises, and invented a content-loss defect that did not exist.
HTML_AND_SVG_ELEMENTS = frozenset("""
a abbr address area article aside audio b base bdi bdo blockquote body br button canvas
caption circle cite clippath code col colgroup data datalist dd defs del desc details dfn
dialog div dl dt ellipse em embed feblend fieldset figcaption figure footer foreignobject
form g h1 h2 h3 h4 h5 h6 head header hgroup hr html i iframe image img input ins kbd label
legend li line lineargradient link main map mark marker mask menu meta meter nav noscript
object ol optgroup option output p param path pattern picture polygon polyline pre progress
q radialgradient rect rp rt ruby s samp script section select slot small source span stop
strong style sub summary sup svg symbol table tbody td template text textarea textpath tfoot
th thead time title tr track tspan u ul use var video wbr
""".split())


#: Cues that turn a claim into its own denial. A corrected card frequently has
#: to NAME the defect in order to warn against it -- "not UR Z15", "there is no
#: universal rule that cover becomes void", "say X, not Y" -- and a check that
#: cannot tell an assertion from a warning goes red on the correction itself.
#: That is trap 89 in the absence-check direction: the first draft of this gate
#: failed six checks, every one of them on wording the correction had added.
#: Constructions that actually DENY a following claim. These may sit anywhere
#: in the same sentence before the match.
_DENIAL = re.compile(
    r"(?:there is no\b|there are no\b|no universal\b|no such\b|"
    r"contains no\b|says nothing\b|nothing whatever\b|"
    r"do(?:es)? not\b|did not\b|is not\b|are not\b|was not\b|"
    r"\bnever\b|rather than\b|instead of\b|to hedge over\b|"
    r"deliberately says\b|not merely\b|"
    r"not\s+(?:UR|PR|MSC|IACS|A\.)|which is Hull|is Deleted\b)",
    re.I)

#: Bare negation particles. These are NOT evidence on their own -- "Make no
#: mistake, sir, every statutory certificate is invalidated" contains "no" and
#: asserts the defect. They count only when they immediately precede the match,
#: which is the position from which they can actually govern it.
_BARE_NEGATION = re.compile(r"(?:\bno\b|\bnothing\b)\s+\S+\s*$", re.I)


#: Clause boundaries. A denial in the previous clause did not survive into this
#: one -- "PR1C is not an insurance document, YET our cover falls away" is an
#: assertion, and the first draft read it as a denial.
_CLAUSE_BREAK = re.compile(r"[.;:?!]\s|\s[\u2014\u2013-]\s|,\s(?:yet|but|and|so|or|nor|"
                           r"however|although|though|while|whereas|then|thus)\s", re.I)

#: The explicit contrast form: say X, NOT Y. Only this shape lets a negation
#: INSIDE the match disarm it -- a parenthetical "whether or not" must not.
_CONTRAST = re.compile(r"[,\u201d\"']\s*not\s(?!or\b)", re.I)


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
        # ONE rule, replacing three that each leaked. Take the prefix AND the
        # matched span together, clip at the last clause break anywhere in that
        # context, and ask whether a denial survives into the final clause.
        #
        # A denial governs the clause it is in and no further:
        #   "PR1C is not an insurance document, YET our cover falls away"
        #       -> clipped at ", yet"; final clause has no denial; CAUGHT
        #   "PR1C contains no insurance provision, AND there is no universal
        #    rule that cover becomes void"
        #       -> clipped at ", and"; "there is no" survives; disarmed
        #   "DO NOT FORGET: all statutory certificates become invalid"
        #       -> clipped at ":"; final clause has no denial; CAUGHT
        #   "our cover, whether or NOT the club agrees, lapses outright"
        #       -> "or not" is neither a denial construction nor adjacent;
        #          CAUGHT
        context = text[max(0, m.start() - window):m.end()]
        breaks = list(_CLAUSE_BREAK.finditer(context))
        if breaks:
            context = context[breaks[-1].end():]
        if (_DENIAL.search(context) or _BARE_NEGATION.search(context)
                or _CONTRAST.search(context)):
            continue
        # An examiner's QUESTION is not a taught proposition -- but only when
        # it is genuinely a quoted question. Requiring an OPEN QUOTE before the
        # match and a "?" closing it before the quote closes is what separates
        # 'do statutory certificates also become invalid?' from mutation X3,
        # which asserted the defect and appended a rhetorical question.
        tail = text[m.end():m.end() + 200]
        head = text[max(0, m.start() - 200):m.start()]
        q_open = max(head.rfind('"'), head.rfind('\u201c'))
        if q_open >= 0 and not re.search(r'["\u201d]', head[q_open + 1:]):
            close = re.search(r'["\u201d]', tail)
            qmark = tail.find('?')
            if qmark >= 0 and (close is None or qmark < close.start()):
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
    #: Verbs for "the cover stops applying". "prejudiced" is deliberately
    #: absent: that is the correct framing this correction introduced.
    LOST = (r"void|avoid|lapse|invalidat|cease|null|forfeit|withdrawn|"
            r"falls? away|fell away|at an end|no longer (?:applies|responds)|"
            r"stops? (?:answering|responding)|ends? outright")
    #: [^.,;:] rather than [^.] -- clause-local, so a match cannot begin in a
    #: denied clause and end in an asserting one.
    void = asserts(flat, r"(?:insurance|cover|coverage|P&I|H&M)[^.,;:]{0,90}?"
                         r"(?:" + LOST + r")"
                         r"|(?:" + LOST + r")[^.,;:]{0,50}?"
                         r"(?:insurance|cover|coverage)"
                         # comma-tolerant: an interposed clause must not hide it
                         r"|(?:our|the)\s+(?:P&I\s+|H&M\s+|hull\s+)?"
                         r"(?:insurance|cover|coverage)[^.;:]{0,70}?(?:" + LOST + r")")
    report("pr1c_no_universal_insurance_void_claim", void is None,
           "found=%r" % (void.group(0) if void else None))
    report("pr1c_insurance_limb_names_its_instrument",
           re.search(r"ITC-Hulls|Institute Time Clauses", flat) is not None,
           "PR1C is silent on insurance; the consequence comes from the POLICY")
    # The over-correction, guarded in its own right. "Cover may be prejudiced"
    # understates ITC-Hulls cl. 4.2, which terminates hull cover AUTOMATICALLY.
    under = asserts(flat, r"cover (?:may be|might be|could be) prejudiced"
                          r"|(?:cover|insurance) is not automatically void"
                          r"|not automatically void")
    report("pr1c_no_insurance_understatement", under is None,
           "found=%r -- see trap 130" % (under.group(0) if under else None))

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

    # The CE Oral Tip is the sentence the card tells the candidate to SAY, and
    # the first draft of this gate never opened it -- so the unqualified
    # "invalidates our statutory certificates" survived there, in the one layer
    # that reaches an examiner, while every other layer was corrected.
    tip = layer(c, "CE Oral Tip")
    tip_over = asserts(tip, r"invalidates (?:our|the|all) statutory certificates"
                            r"|statutory certificates are invalidated"
                            r"|(?:all|every) statutory certificate")
    report("pr1c_ce_tip_no_unqualified_certificate_claim", tip_over is None,
           "found=%r" % (tip_over.group(0) if tip_over else None))
    report("pr1c_ce_tip_carries_the_qualifier",
           re.search(r"certain", tip, re.I) is not None,
           "the tip must say 'certain', like every other layer")

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

    # M4: the first draft tested only that the three names appear. The card
    # could put Maersk in Premier Alliance and stay green.
    for grouping, members in (("Gemini", ("Maersk", "Hapag-Lloyd")),
                              ("Ocean Alliance", ("CMA CGM", "COSCO", "Evergreen", "OOCL")),
                              ("Premier Alliance", ("ONE", "HMM", "Yang Ming"))):
        best = None
        for m in re.finditer(re.escape(grouping), flat):
            span = flat[m.start():m.start() + 240]
            missing = [x for x in members if x not in span]
            if best is None or len(missing) < len(best):
                best = missing
            if not missing:
                break
        report("alliance_membership_correct_%s" % grouping.split()[0].lower(),
               best == [], "no occurrence carries full membership; best miss=%s"
               % (best if best else "none"))

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

def check_qb4a_sibling() -> None:
    """QB4_A#q9 - the card the PR1C record's sweep claimed did not exist.

    A second independent review ran the record's own declared search and found
    this card carrying all three corrected propositions in six layers. It is
    guarded here on the same terms as QB4_C#q5, layer by layer, because the
    defect that hid in a CE Oral Tip once can hide in one again.
    """
    c = teaching(card("QB4_A.html", "q9"))
    flat = flatten(c)

    over = asserts(flat, r"all statutory certificates[^.]{0,60}?"
                         r"(?:invalid|simultaneous)"
                         r"|every statutory certificate"
                         r"|statutory certificates[^.]{0,40}?become "
                         r"(?:simultaneously )?invalid")
    report("qb4a_no_all_statutory_certificates_claim", over is None,
           "found=%r" % (over.group(0)[:60] if over else None))
    report("qb4a_certain_statutory_certificates_taught",
           re.search(r"certain[^.]{0,40}statutory certificates", flat, re.I) is not None,
           "B.1.3 as written")

    LOST = (r"void|lapse|invalidat|cease|forfeit|falls? away|at an end|"
            r"no longer (?:applies|responds)|automatically ends?")
    ins = asserts(flat,
                  r"(?:P&I|H&M|insurance|cover|coverage)[^.,;:]{0,80}?(?:" + LOST + r")")
    report("qb4a_no_universal_insurance_loss_claim", ins is None,
           "found=%r" % (ins.group(0)[:60] if ins else None))
    report("qb4a_insurance_limb_names_its_instrument",
           re.search(r"ITC-Hulls|Institute Time Clauses", flat) is not None,
           "the consequence is contractual, not PR1C's -- trap 130")
    # Mutation Z7b stripped the instrument from ONE site and the card-wide
    # presence check stayed green on the others. The understatement itself is
    # the thing to forbid, and it must be forbidden here as well as on QB4_C.
    under = asserts(flat, r"cover (?:may be|might be|could be) prejudiced"
                          r"|(?:cover|insurance) is not automatically void"
                          r"|not automatically void")
    report("qb4a_no_insurance_understatement", under is None,
           "found=%r -- see trap 130" % (under.group(0) if under else None))

    auto = asserts(flat, r"[Cc]ondition of [Cc]lass[^.,;:]{0,90}?"
                         r"(?:automatic\w*[^.,;:]{0,40}?suspen|suspends? class)"
                         r"|automatic\w*\s+[Ss]uspension of [Cc]lass"
                         r"|(?:class|classification) is suspended automatic\w*"
                         r"|suspend\w*\s+automatic\w*"
                         r"|(?:due date|timeframe)[^.,;:]{0,60}?results in[^.,;:]{0,30}?[Ss]uspen"
                         r"|[Cc]lass suspended if not met"
                         r"|suspension if missed"
                         r"|the society suspends class")
    report("qb4a_coc_is_a_suspension_procedure", auto is None,
           "A.2.1 - an overdue CoC is not automatic; found=%r"
           % (auto.group(0)[:60] if auto else None))
    report("qb4a_procedure_limb_taught",
           re.search(r"suspension procedure", flat, re.I) is not None,
           "the distinction, stated")

    z23 = asserts(flat, r"UR\s*Z23")
    report("qb4a_no_ur_z23_attribution", z23 is None,
           "UR Z23 is Hull Survey for New Construction; found=%r"
           % (z23.group(0) if z23 else None))
    report("qb4a_notification_attributed_to_pr1c",
           re.search(r"PR1C[^.]{0,60}B\.1\.1|B\.1\.1", flat) is not None,
           "the provision that actually requires the letter")

    # The layer that hid the same defect on QB4_C#q5.
    tip = layer(c, "CE Oral Tip")
    tip_over = asserts(tip, r"all[^.]{0,40}statutory certificates[^.]{0,40}invalid"
                            r"|every statutory certificate")
    report("qb4a_ce_tip_no_unqualified_certificate_claim", tip_over is None,
           "found=%r" % (tip_over.group(0)[:60] if tip_over else None))


def check_pr1c_family_reach() -> None:
    """Every surface the PR1C family reaches -- including derived ones.

    The P0 of this batch was QB4_A_CheatSheet, the DERIVED surface of a card
    that had just been corrected, still teaching the opposite. No check in the
    first three rounds of this gate read a cheat sheet, because the corpus's
    card digester cannot see one: cheat sheets contain no q-card. So this check
    reads whole pages, and the sweep behind it enumerates from disk.
    """
    cs = flatten(read_text(QB / "QB4_A_CheatSheet.html"))
    over = asserts(cs, r"ALL[^.]{0,40}statutory\s+certs?"
                       r"|statutory\s+certs?[^.]{0,40}invalid\s+simultaneously")
    report("cheatsheet_no_all_statutory_certs_claim", over is None,
           "found=%r" % (over.group(0)[:60] if over else None))
    report("cheatsheet_carries_the_qualifier",
           re.search(r"certain", cs, re.I) is not None,
           "the derived surface must teach what the card teaches")
    report("cheatsheet_no_false_pr_citation",
           not re.search(r"PR\s*No\.?\s*[13]\b", cs),
           "PR 1 is Deleted; PR 3 is Transparency of Classification")
    coc = asserts(cs, r"suspension if missed|[Cc]lass suspended if not met")
    report("cheatsheet_coc_is_a_procedure", coc is None,
           "found=%r" % (coc.group(0) if coc else None))

    # QB4_A#q9's own table and Numbers layers, which round 2 missed.
    q9 = teaching(card("QB4_A.html", "q9"))
    q9flat = flatten(q9)
    report("qb4a_table_row_is_a_procedure",
           re.search(r"Suspension procedure[^|]{0,80}A\.2\.1", q9flat, re.I) is not None,
           "the notation table is the card's most memorisable layer")
    report("qb4a_three_month_window_is_a_1_2_and_a_1_3",
           re.search(r"A\.1\.2[^.]{0,80}A\.1\.3[^.]{0,60}three months", q9flat)
           is not None
           or re.search(r"A\.1\.1[^.]{0,90}certificate expiry date", q9flat) is not None,
           "A.1.1 suspends from the certificate expiry date, not at three months")
    report("qb4a_no_false_pr_citation",
           not re.search(r"IACS\s+PR\s*No\.?\s*[13]\b", q9flat),
           "PR 1 is Deleted; PR 3 is Transparency of Classification")

    # The sibling teaching cards the sweep found.
    for name, anchor, key in (("QB1_C.html", "q6", "qb1c"),
                              ("QB4_E.html", "q13", "qb4e_q13"),
                              ("QB1_G.html", "q36", "qb1g_q36")):
        f = flatten(teaching(card(name, anchor)))
        bad = asserts(f, r"automatic\w*\s+[Ss]uspension of [Cc]lass"
                         r"|[Ss]uspension automatic\w*\s+voids?"
                         r"|(?:voids?|invalidat\w+)[^.,;:]{0,40}?"
                         r"(?:insurance|P&I|H&M|hull insurance)"
                         r"|\ball\b[^.,;:]{0,40}statutory certificates")
        report("%s_no_pr1c_family_defect" % key, bad is None,
               "%s#%s found=%r" % (name, anchor, bad.group(0)[:60] if bad else None))

    # The sweep itself, run as a check rather than asserted in prose.
    import subprocess
    rc = subprocess.run([sys.executable, str(HERE / "sweep_pr1c_family.py"), "--check"],
                        cwd=str(REPO), capture_output=True)
    out = (rc.stdout + rc.stderr).decode("utf-8", "replace")
    tail = [l for l in out.splitlines() if "UNADJUDICATED" in l]
    report("pr1c_family_sweep_has_no_unadjudicated_hit", rc.returncode == 0,
           tail[0].strip() if tail else "sweep did not report")


def check_terminal_closure() -> None:
    """The four Pass-2 terminal-closure blockers.

    Three of these guard SOURCE-OWNED or GENERATED surfaces rather than cards,
    which is the gap that let the Notes mis-citations and the stale correction
    log sit outside every earlier gate in this batch.
    """
    import subprocess

    # -- A. PR 1 / PR 3 / PR 35 attribution, corpus-wide including the Notes --
    # PR1C, PR1A..PR1D and PR 35 are legitimate; a bare PR 1 or a PR No.3 cited
    # for conditions of class is not. Checked over rendered text so a citation
    # inside an attribute cannot hide.
    bad = []
    for page in sorted((QB).rglob("*.html")):
        flat = flatten(strip_all_footers(read_text(page)))
        for m in re.finditer(r"\(?\bPR\s?1\)?(?!\s*[A-D]\b)(?![A-D0-9])"
                             r"|\bPR\s*No\.?\s*[13]\b(?!\s*5)", flat, re.I):
            window = flat[max(0, m.start() - 90):m.end() + 40]
            if re.search(r"\bnot\b|Deleted|index records|there is no|family|"
                         r"UR ?/ ?UI|neighbouring", window, re.I):
                continue
            bad.append("%s: %r" % (page.name, flat[m.start():m.start() + 50]))
    report("notes_and_qb_no_bare_pr1_or_pr3_citation", not bad,
           "found=%s" % (bad[:3] or "none"))
    # Read the reg-CODE, not the whole page: the instrument name survives in the
    # reg-description after the code is swapped, so a page-wide test passes on a
    # card that now cites the wrong number. Mutations TB and TC found this.
    for page, must in (("oralnotes/simon-notes-p2.html", "PR1C"),
                       ("oralnotes/simon-notes-p6.html", "PR 35"),
                       ("oralnotes/miw-notes-mgmt-p7.html", "PR1C A.4.1")):
        raw = read_text(QB / page)
        codes = " | ".join(re.findall(r'<span class="reg-code">(.*?)</span>', raw))
        hay = codes if codes and "reg-code" in raw else flatten(raw)
        if page.endswith("p7.html"):
            hay = flatten(raw)          # p7 has no reg box; the claim is in prose
        report("notes_%s_cites_the_right_instrument" % page.split("/")[-1].replace(
                   "-", "_").replace(".html", ""),
               must in hay, "expects %r in the cited code" % must)
    # p7 carried a second error in the same sentence: six months is WITHDRAWAL
    # after suspension, not a trigger that causes it.
    p7 = flatten(read_text(QB / "oralnotes/miw-notes-mgmt-p7.html"))
    trig = asserts(p7, r"six[- ]month[^.,;:]{0,40}?(?:automatic[- ]suspension )?trigger"
                       r"|6-month automatic-suspension trigger")
    report("notes_p7_six_months_is_withdrawal_not_a_trigger", trig is None,
           "found=%r" % (trig.group(0) if trig else None))

    # -- B. qb_content_index freshness, proved by regeneration ---------------
    idx = REPO / "meoclass1" / "qb_content_index.json"
    before = idx.read_bytes()
    rc = subprocess.run([sys.executable, str(HERE / "build_qb_content_index.py")],
                        cwd=str(REPO), capture_output=True)
    after = idx.read_bytes()
    if after != before:
        idx.write_bytes(before)
    report("qb_content_index_is_current_and_deterministic",
           rc.returncode == 0 and after == before,
           "regenerating from HEAD reproduces the committed file byte for byte")
    governed = json.loads(read_text(HERE / "qb_content_index_governed.json"))
    report("qb_content_index_records_the_pass2_batch",
           any(e.get("date") == "2026-09-07" for e in governed.get("recently_updated", [])),
           "the correction log is hand-maintained, so a generated rebuild alone "
           "cannot make it current")

    # -- C. the seven QB10_B propositions, each guarded by its own claim -----
    q1 = flatten(teaching(card("QB10_B.html", "q1")))
    report("qb10b_stcwf_convention_vs_amendments",
           re.search(r"Convention[^.]{0,60}?in force since 2012", q1) is not None,
           "the Convention predates 2026; the amendments and Code did not")
    report("qb10b_polar_population_is_precise",
           all(s in q1 for s in ("24 m LOA", "300 GT")) ,
           "fishing vessels 24 m LOA+, yachts 300 GT+, cargo 300-500 GT")
    # The card names the pairing only to record that it is NOT asserted.
    # Require every occurrence to sit inside that disclaimer.
    pair = [m.start() for m in re.finditer(r"MSC\.532\(107\)/MSC\.538\(107\)", q1)]
    disc = [m.start() for m in re.finditer(r"adopting resolution is not stated here", q1)]
    loose = [p for p in pair
             if not any(0 < p - d < 160 for d in disc)]
    report("qb10b_polar_no_unverified_resolution", not loose,
           "every mention must sit inside the not-asserted disclaimer; loose=%d"
           % len(loose))
    # PRESENCE of both dates is not the claim. A card can carry 2026 and 2027
    # and still bind them to the wrong events - which is the whole trap this
    # bullet warns about. Test the PAIRING: designation/in-force is 2026,
    # enforcement of the 0.10% limit is 2027, and neither may take the other
    # date. Mutation TI collapsed the pairing while leaving both dates on the
    # card, and a presence check stayed green on it.
    wrong = asserts(q1,
                    r"(?:become ECAs|designat\w+|in force)[^.;]{0,60}?1 March 2027"
                    r"|(?:enforc\w+|0\.10% limit|0\.10% sulphur)[^.;]{0,60}?1 March 2026")
    both = "1 March 2026" in q1 and "1 March 2027" in q1
    report("qb10b_eca_both_dates_present", both and wrong is None,
           "designation 2026 / enforcement 2027; miswired=%r"
           % (wrong.group(0)[:60] if wrong else None))
    jup = asserts(q1, r"traces directly to"
                      r"|<em>Jupiter</em>"
                      r"|Jupiter</em> bauxite cargo-shift")
    report("qb10b_no_unsupported_jupiter_causal_claim", jup is None,
           "found=%r" % (jup.group(0)[:50] if jup else None))
    shift = asserts(q1, r"lost to a? ?bauxite cargo shift|bauxite cargo-shift")
    report("qb10b_jupiter_named_and_mechanism_correct",
           "Bulk Jupiter" in q1 and "liquefaction" in q1.lower() and shift is None,
           "ship is Bulk Jupiter, mechanism is liquefaction; found=%r"
           % (shift.group(0) if shift else None))
    for label, pat in (("lrit", r"status as at September 2026"),
                       ("msc112", r"still a future session as at\s*September 2026")):
        report("qb10b_%s_is_as_at_dated" % label,
               re.search(pat, q1) is not None,
               "a perishable status must carry the date it was true")

    # -- D. K-items closed earlier must not regress -------------------------
    for name, pat in (("msc482_amendment", r"MSC\.482\(103\)"),
                      ("davit_launched_scope", r"davit-launched"),
                      ("lowering_formula", r"0\.4 \+ 0\.02"),
                      ("formula_cap", r"whichever is less"),
                      ("max_speed", r"1\.3\s*m/s")):
        report("qb10b_preserved_%s" % name, re.search(pat, q1) is not None,
               "closed K-item must not regress")


def check_closeup() -> None:
    c = teaching(card("QB3_A.html", "q5"))
    flat = flatten(c)

    report("closeup_scoped_to_single_side_skin_bulk_carriers",
           re.search(r"single side skin bulk carriers", flat, re.I) is not None
           and re.search(r"not(?:</strong>)?\s*an oil tanker requirement", flat, re.I)
           is not None,
           "population named AND oil tankers excluded -- the proposition, not the "
           "word 'only'")
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

    # The independent review found this correction had propagated the
    # POPULATION from QB3_B#q1 and dropped its extent, hold scope, modality and
    # age condition -- stating as an unconditional rule what the source record
    # states conditionally. All four are now guarded.
    report("closeup_extent_restated",
           re.search(r"25% of cargo hold side shell", flat, re.I) is not None,
           "UR Z10.2 extent, as QB3_B#q1 attributes it")
    report("closeup_hold_scope_restated",
           re.search(r"forward cargo hold and one other", flat, re.I) is not None,
           "which holds")
    report("closeup_is_age_conditioned",
           re.search(r"age-conditioned", flat, re.I) is not None,
           "the qualification the source record makes")
    report("closeup_modality_is_can_require",
           re.search(r"can require", flat, re.I) is not None,
           "'can require', not 'includes' -- QB3_B#q1's own modality")

    # Cross-card: this record's entire authority is QB3_B#q1, so a check that
    # cannot see the two disagree cannot certify the propagation.
    sib_flat = flatten(teaching(card("QB3_B.html", "q1")))
    for prop, pat in (("population", r"single side skin bulk carriers"),
                      ("extent", r"25% of cargo hold side shell"),
                      ("age_condition", r"age-conditioned")):
        report("closeup_agrees_with_qb3b_q1_on_%s" % prop,
               (re.search(pat, flat, re.I) is not None)
               == (re.search(pat, sib_flat, re.I) is not None),
               "QB3_A#q5 and QB3_B#q1 must not diverge")
    sib_numbers = layer(teaching(card("QB3_B.html", "q1")), "Numbers to Memorise") \
        if "Numbers to Memorise" in sib_flat else sib_flat
    close_line = next((s for s in sib_numbers.split(" \u2014 ")
                       if "close-up" in s.lower()), sib_numbers)
    # No "close-up ... within N characters" anchor: the layer contains
    # "UR Z10.2", and a [^.] window stops dead at that period, which is how
    # mutation Z3 escaped. Match the widening CLAIM itself and let asserts()
    # discount the legitimate "not oil tankers".
    sib_over = asserts(sib_numbers,
                       r"bulk carriers?\s*/\s*tankers?"
                       r"|bulk carriers and (?:oil )?tankers"
                       r"|tankers generally"
                       r"|applied to[^;]{0,60}?tankers")
    report("closeup_sibling_numbers_layer_not_over_broad", sib_over is None,
           "found=%r" % (sib_over.group(0)[:60] if sib_over else None))
    report("closeup_sibling_numbers_layer_names_the_population",
           re.search(r"single side skin", sib_numbers, re.I) is not None,
           "the memorisation layer must carry the scope, not just the body")

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
                           r"[^.,;:]{0,70}?formula"
                           r"|formula[^.,;:]{0,70}?(?:no longer applies|is withdrawn|"
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

    # M1: the first draft read "Administration may accept" and never read the
    # figure, so 1.3 could be changed to 2.3 in the very provision this record
    # exists to fix and the gate stayed green.
    for name, text in (("formula_block", formula_layer), ("numbers_block", numbers_layer)):
        maxima = set(re.findall(r"maximum(?:\s+\w+){0,4}?\s+(?:is\s+|shall be\s+)?"
                                r"(\d+\.\d+)\s*m/s", text, re.I))
        report("amend_%s_maximum_is_1_3_ms" % name, maxima == {"1.3"},
               "the numeral itself, not the discretion clause; found=%s"
               % (sorted(maxima) or "none"))

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

    # -- markup hygiene, stated as what it actually is ----------------------
    # Trap 126: "<150 GT" renders correctly, so escaping it fixed nothing that
    # was broken. The check is kept because the escaping is correct markup, but
    # it no longer claims to be preventing content loss.
    report("amend_lt_before_numeral_is_escaped",
           re.search(r"<\d", raw) is None,
           "markup hygiene -- NOT content loss; see trap 126")

    # The mechanism that DOES eat text: "<" plus a letter that is not an
    # element name. Checked against a real element list rather than modelled.
    bogus = [m.group(1) for m in re.finditer(r"<(/?[A-Za-z][A-Za-z0-9-]*)", raw)
             if m.group(1).lstrip("/").lower() not in HTML_AND_SVG_ELEMENTS]
    report("amend_no_unclosed_pseudo_tag_eating_text", not bogus,
           "found=%s" % (sorted(set(bogus))[:4] or "none"))

    # The dates themselves, asserted directly rather than via a parser model.
    report("amend_2028_and_2029_compliance_dates_present",
           "1 Jan 2028" in flat and "1 Jan 2029" in flat,
           "the pilot-transfer compliance dates")

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
                     ("QB4_A q9   PR1C sibling (8th card)", check_qb4a_sibling),
                     ("PR1C family reach + generated sweep", check_pr1c_family_reach),
                     ("QB3_A q5   annual close-up scope", check_closeup),
                     ("Terminal closure: Notes PR, index, QB10_B", check_terminal_closure),
                     ("QB10_B q1  amendment overview", check_amend)):
        print("\n-- %s" % name)
        fn()
    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    for f in FAILS:
        print("  FAIL " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
