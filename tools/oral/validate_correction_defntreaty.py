#!/usr/bin/env python3
"""
Content validator for CORR-DEFN-TREATY-20260825.

WHY THIS EXISTS AND WHY THE DIGEST PIN IS NOT ENOUGH
----------------------------------------------------
`validate_corrections.py` answers "are these bytes the ones we authorised?".
It pins whatever it is given, so it is perfectly happy with wrong text. This
file answers the other question: "is what was authorised actually right?".

The defect was not a typo. `QB9_G#q6` printed a legal hierarchy under its own
heading -- Treaty, then Convention, then Protocol -- and international law
recognises no such ranking. VCLT 1969 Art.2(1)(a) makes an agreement a treaty
"whatever its particular designation", so Convention and Protocol are treaty
TITLES, not tiers. Three propositions travelled with the hierarchy: that a
Protocol is by definition an amendment, that a Protocol always requires its
own ratification, and that an IMO Resolution is guidance without treaty force.

Every one of those is the kind of tidy, memorable, wrong sentence that a later
well-meaning edit re-introduces precisely because it reads well. So each is
asserted here as a NAMED check, one per proposition:

    the VCLT definition is quoted, with its operative qualifier
    the UN Treaty Collection terminology is QUOTED, not glossed
    no hierarchy is asserted anywhere in either card or the cheat sheet
    a Protocol is not reduced to an amendment
    ratification is not made universal; the final clauses control
    a Resolution's effect is not flattened to "guidance"
    the MIW memory line is labelled as MIW's wording, not as law
    the record carries its independent review
    the cited authorities are first-party

Each is named so `mutate_correction_defntreaty.py` can require that its
mutation trips THAT check, and not merely the digest pin that fires on any
edit at all (SKILL section 8.2a, rule 1).

NEGATIVE CHECKS RUN ON UNESCAPED TEXT, AND ASSERT NEGATION, NOT ABSENCE
-----------------------------------------------------------------------
A guard spelled `h&m` is blind to `h&amp;m`, so every search runs against
`html.unescape()`. And a correction QUOTES the wording it rejects -- the
corrected card says "Never say 'Treaty -> Convention -> Protocol'" and "'a
Protocol always requires ratification' is wrong" -- which is why known_traps
entry 53 is marked GREP: SKIP. A flat banned-phrase grep would fail on the
very sentences carrying the fix. The assertion is therefore that every
occurrence is NEGATED OR QUOTED, with a deliberately wide lookback, never
that it is absent.
"""

from __future__ import annotations

import html as htmllib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_bytes import read_text                       # noqa: E402
from validate_batch_b import card_digests              # noqa: E402

CORRECTION_ID = "CORR-DEFN-TREATY-20260825"
MANIFEST = HERE / "correction_corr_defn_treaty_20260825_manifest.json"
PAGE = "meoclass1/QB9_G.html"
SHEET = "meoclass1/QB9_G_CheatSheet.html"

Q6_TEXT = ("What is the difference between a Convention, a Protocol, and a Treaty "
           "in international maritime law?")
Q3_MARK = "How is an IMO convention formally adopted?"

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-42s %s" % ("PASS" if ok else "FAIL", check, detail))


def flat(raw: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", raw)))


def card_text(page_text: str, anchor: str) -> str:
    start = page_text.find('<div class="q-card" id="%s"' % anchor)
    assert start >= 0, "card not found: %s" % anchor
    nxt = page_text.find('<div class="q-card"', start + 10)
    return flat(page_text[start:nxt if nxt > 0 else len(page_text)])


# A mention of a rejected formulation is acceptable in exactly two shapes: it
# is quoted (cited as the wording being rejected), or a denial precedes it in
# the same passage. The lookback is 260 chars because the tightest real case
# in this correction puts the denial behind two full quoted phrases:
#   Never say "Treaty -> Convention -> Protocol" -- that ladder does not exist
NEGATORS = re.compile(
    r"(?:\bnot\b|\bnever\b|\bno such\b|\bno longer\b|\bdo not\b|\bdon't\b|"
    r"\brather than\b|\bwrong\b|\bis false\b|\binstead of\b|\bavoid\b|"
    r"\bcommonest error\b|\bdismiss\b|\bfailures?\b|\bforbid\b|\breciting\b|"
    r"\bcalling\b|\bdefining\b|\bsaying\b|\btrap\b|\bmistake\b|\bcannot\b)", re.I)

_QUOTES = "\"“”‘’'"

# Contexts in which a mention is a correctly SCOPED statement rather than the
# universal claim being banned. The UN Treaty Collection's own terminology says
# an OPTIONAL protocol is "of independent character and subject to independent
# ratification" -- true, and true only of that kind. Banning the phrase outright
# would force the card to drop the source's wording, which is precisely the
# defect (MIW gloss replacing quoted terminology) that this correction removed.
SCOPED_OK = re.compile(r"optional protocol|protocol of signature|"
                       r"framework treaty|kinds?, including", re.I)


def _inside_quotes(text: str, start: int, end: int) -> bool:
    """Is the match inside a quoted span, even if it begins mid-quote?

    The naive test -- a quote character immediately before and after -- misses
    the commonest real shape here, where the pattern matches part-way into the
    quotation:  so "a Protocol >>>always requires ratification" is wrong.
    So look back for an unclosed opening quote instead.
    """
    look = text[max(0, start - 300):start]
    opens = [i for i, ch in enumerate(look) if ch in _QUOTES]
    if not opens:
        return False
    # an odd number of quote characters behind us means one is still open
    return len(opens) % 2 == 1 and any(ch in _QUOTES for ch in text[end:end + 120])


def _sentence_before(text: str, start: int) -> str:
    """The match's own sentence, looking back at most 400 chars.

    THE NEGATION WINDOW MUST BE SENTENCE-SCOPED, NOT CHARACTER-SCOPED.
    A flat 260-char lookback was the first implementation and mutation F walked
    straight through it: corrected prose is dense with denials ("not tiers",
    "not necessarily ratification"), so a NEW wrong sentence inserted anywhere
    near them inherited somebody else's "not" and was excused. The denial has to
    belong to the same sentence as the claim it denies.

    SKILL section 8.2a still requires a WIDE window for the genuine case -- the
    tightest one here puts the denial behind two full quoted phrases -- and that
    case is preserved, because `Never say "Treaty -> Convention -> Protocol"` has
    its negator inside its own sentence AND is quoted.

    The sentence is taken WHOLE, not just the part before the match: a denial
    lands on either side of the claim it denies. "a protocol is not, by
    definition, merely an amendment" carries its negator AFTER the phrase, and a
    backward-only window reported that very sentence as the defect.
    """
    look = text[max(0, start - 400):start]
    cut = max(look.rfind(". "), look.rfind("? "), look.rfind("! "))
    head = look[cut + 1:] if cut >= 0 else look
    ahead = text[start:start + 400]
    end = min([i for i in (ahead.find(". "), ahead.find("? "), ahead.find("! "))
               if i >= 0] or [len(ahead)])
    return head + ahead[:end]


def mentions(text: str, pattern: str) -> tuple[list[str], list[str]]:
    """Split every match into (acceptable-because-negated-quoted-or-scoped, asserted)."""
    ok, asserted = [], []
    for m in re.finditer(pattern, text, re.I):
        sentence = _sentence_before(text, m.start())
        if (_inside_quotes(text, m.start(), m.end())
                or NEGATORS.search(sentence)
                or SCOPED_OK.search(text[max(0, m.start() - 260):m.start()])):
            ok.append(m.group(0))
        else:
            asserted.append("..." + sentence[-72:].strip() + " >>>" + m.group(0))
    return ok, asserted


# The shapes that must never be ASSERTED again. Each is the wording the
# product actually carried before this correction.
HIERARCHY = (r"treaty\s*(?:→|->|>)\s*convention|"
             r"convention\s*(?:→|->)\s*protocol|"
             r"treaty,?\s+then\s+convention|"
             r"umbrella (?:legal )?term")
OWN_RATIF = (r"(?:own|separate|independent)\s+(?:signature and )?ratification|"
             r"requires? (?:its )?own ratification|always requires ratification")
RES_GUIDE = (r"resolution[^.]{0,90}(?:committee guidance|"
             r"without (?:independent )?treaty force|merely guidance|mere guidance)|"
             r"resolution is always")
AMEND_ONLY = (r"protocol[^.]{0,30}(?:is |=\s*)?(?:only|merely|just) an amendment|"
              r"major structural add-on|structural add-on/update")


def main() -> int:
    print("correction content validator: %s" % CORRECTION_ID)

    # ---- the record ------------------------------------------------------
    if not MANIFEST.is_file():
        report("correction_record_present", False, "missing %s" % MANIFEST.name)
        print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
        return 1
    record = json.loads(read_text(MANIFEST))
    report("correction_record_present", True, MANIFEST.name)

    report("correction_record_authorised",
           record.get("status") == "AUTHORISED"
           and record.get("correction_id") == CORRECTION_ID,
           "status=%s id=%s" % (record.get("status"), record.get("correction_id")))

    declared = {c.get("anchor"): c for c in record.get("cards", [])
                if c.get("file") == "QB9_G.html"}
    report("cards_declared_in_record", set(declared) == {"q3", "q6"},
           "anchors=%s" % sorted(declared))

    prose = " ".join(str(record.get(k, "")) for k in ("rationale", "note", "title"))
    prose += " ".join(str(c.get("rationale", "")) for c in record.get("cards", []))

    # The primary authority must be NAMED, not implied. A correction whose
    # record does not say which instrument decided it cannot be re-checked.
    needed = ["Art.2(1)(a)", "Art.11", "UN Treaty Collection",
              "MARPOL Protocol of 1978", "Art.IV(1)", "Art.5(1)",
              "SOLAS Art.VIII(b)", "MSC.48(66)"]
    absent = [n for n in needed if n not in prose]
    report("primary_authority_recorded", not absent, "absent=%s" % (absent or "none"))

    # SKILL section 23: a material correction is not finished without an
    # independent clean-context review, and the record has to say so, or
    # "it was reviewed" becomes indistinguishable from "nobody looked".
    report("independent_review_recorded",
           prose.count("independent clean-context review") >= 2
           or ("independent clean-context review" in prose
               and "SECOND independent clean-context review" in prose),
           "clean-context review mentions=%d"
           % prose.count("independent clean-context review"))

    # ---- the live cards --------------------------------------------------
    page = read_text(REPO / PAGE)
    sheet = read_text(REPO / SHEET)
    q6 = card_text(page, "q6")
    q3 = card_text(page, "q3")
    both = q6 + " " + q3
    sheet_flat = flat(sheet)

    for anchor, card in declared.items():
        live = card_digests(page).get(anchor)
        report("card_digest_matches_manifest_%s" % anchor,
               live == card.get("post_edit_digest"), "live=%s" % (live or "-")[:16])

    report("question_text_unchanged",
           Q6_TEXT in htmllib.unescape(page) and Q3_MARK in htmllib.unescape(page),
           "both canonical q-texts present")

    ids = re.findall(r'<div class="q-card" id="([^"]+)"', page)
    report("card_order_unchanged", ids == ["q1", "q2", "q3", "q4", "q5", "q6", "q7"],
           "ids=%s" % ids)

    # ---- the substance ---------------------------------------------------
    report("vclt_definition_quoted",
           ("an international agreement concluded between States in written form "
            "and governed by international law" in q6),
           "Art.2(1)(a) operative wording present in q6")

    # The qualifier IS the answer. Losing it turns the card back into one that
    # has to invent a ranking from somewhere.
    #
    # A COUNT THRESHOLD IS NOT A GUARD. The first implementation asserted
    # "at least 2 occurrences in q6", and mutation L deleted one of four and
    # walked through it. What matters is not how many times the phrase appears
    # but WHERE: it has to be in the quoted definition, and it has to be in the
    # 15-second answer, because that is the sentence a candidate actually says
    # out loud. So both locations are asserted by position.
    qual = "whatever its particular designation"
    fifteen = q6[q6.find("15-Second Answer"):q6.find("60-Second Answer")]
    official = q6[q6.find("Official definition"):q6.find("Scope note")]
    report("designation_qualifier_present",
           qual in fifteen and qual in official and q6.count(qual) >= 2,
           "in_15s=%s in_quoted_definition=%s total=%d"
           % (qual in fifteen, qual in official, q6.count(qual)))

    report("vclt_scope_note_present",
           "Art.3" in q6 and "for the purposes of the present Convention" in q6,
           "definition is not universalised beyond the VCLT")

    # The UNTC block must QUOTE the source. Its first replacement in this very
    # correction carried MIW's own gloss under an "Official terminology"
    # heading while omitting the source's actual sentence -- the same defect
    # class the correction exists to remove, reproduced by the fix.
    report("untc_terminology_quoted",
           ("less formal than those entitled" in q6
            and "formal multilateral treaties with a broad number of parties" in q6),
           "both UNTC sentences present verbatim")

    ok_h, bad_h = mentions(both + " " + sheet_flat, HIERARCHY)
    report("no_hierarchy_asserted", not bad_h,
           "negated/quoted=%d asserted=%s" % (len(ok_h), bad_h or "none"))

    report("hierarchy_heading_removed",
           "<h4>Hierarchy</h4>" not in page,
           "the heading that WAS the claim is gone")

    ok_a, bad_a = mentions(both + " " + sheet_flat, AMEND_ONLY)
    report("protocol_not_amendment_only", not bad_a,
           "negated/quoted=%d asserted=%s" % (len(ok_a), bad_a or "none"))

    report("protocol_kinds_stated",
           ("protocol of signature" in q6 and "optional protocol" in q6
            and "framework" in q6 and "supplementary treaty" in q6),
           "the UNTC kinds are listed")

    ok_r, bad_r = mentions(both + " " + sheet_flat, OWN_RATIF)
    report("protocol_ratification_not_universal", not bad_r,
           "negated/quoted=%d asserted=%s" % (len(ok_r), bad_r or "none"))

    # Two worked cases in OPPOSITE directions, from one regime, are what make
    # "the final clauses control" checkable rather than a slogan.
    report("final_clauses_control_both_ways",
           ("Art.IV(1)" in q6 and "Art.5(1)" in q6
            and "Only" in q6 and "accession" in q6),
           "1978 open to States; 1997 open only to Contracting States")

    report("consent_means_open_list",
           ("or any other means if so agreed" in q6
            and "any other means if so agreed" in q3),
           "VCLT Art.11 residual clause in BOTH cards")

    # q3's summary surfaces taught a closed set of four for one round after
    # its body had been corrected. That is what the second review caught.
    report("q3_four_routes_not_closed",
           ("not a closed list" in q3
            and "all four have identical legal effect" not in q3),
           "q3 no longer presents four routes as the whole rule")

    ok_g, bad_g = mentions(both + " " + sheet_flat, RES_GUIDE)
    report("resolution_effect_not_flattened", not bad_g,
           "negated/quoted=%d asserted=%s" % (len(ok_g), bad_g or "none"))

    report("resolution_binding_route_stated",
           ("Art.VIII(b)" in q6 and "MSC.48(66)" in q6
            and "tacit acceptance" in q6.lower()
            and "MSC.48(66)" in q3),
           "the binding route is stated in both cards")

    # SKILL section 2a rule 4: never present MIW shorthand as an official
    # definition. The memory line is the surface candidates actually retain.
    report("miw_line_labelled_as_miw",
           ("this is MIW wording, not an official definition" in q6
            and "this is MIW" in q6.replace("this is MIW wording, not an official definition", "", 1)),
           "memory line AND the UNTC gloss are both fenced as MIW's")

    report("q3_ladder_scoped_to_bindingness",
           ("ranks instruments by" in q3 and "not by legal class" in q3
            and "neither title outranks the other" in q3),
           "q3's ladder cannot be read as a legal hierarchy")

    # ---- the cheat sheet -------------------------------------------------
    # Candidates memorise the sheet first, so a corrected card beside a stale
    # mnemonic still fails. All four surfaces are asserted.
    report("cheatsheet_confusable_corrected",
           "neither title outranks the other" in sheet_flat,
           "Convention vs Protocol pair carries the corrected model")
    report("cheatsheet_q554_corrected",
           "not necessarily ratification" in sheet_flat,
           "Q554 flip-card no longer asserts own ratification")
    report("cheatsheet_q548_corrected",
           ("all equal legal effect" not in sheet_flat
            and "VCLT Art.11 leaves the" in sheet_flat),
           "Q548 flip-card no longer closes the consent list")
    report("cheatsheet_caption_describes_diagram",
           ("adoption route for a convention" in sheet_flat
            and "structural add-on" not in sheet_flat),
           "caption matches the SVG it captions")

    # ---- authorities are first-party -------------------------------------
    # SKILL section 2a rule 2: never a blog or training-note site where
    # first-party authority exists.
    codes = re.findall(r'<span class="reg-code">(.*?)</span>', page, re.S)
    junk = re.compile(r"(?i)wikipedia|marineinsight|blogspot|\.blog|medium\.com|"
                      r"training ?institute|coursehero|quora|scribd|studocu")
    tainted = [flat(c).strip() for c in codes if junk.search(flat(c))]
    report("authorities_are_first_party", not tainted, "tainted=%s" % (tainted or "none"))

    # ---- verified capsule ------------------------------------------------
    capsule = {
        "VCLT adopted": r"22 May 1969",
        "VCLT in force": r"27 January 1980",
        "MARPOL adopted": r"2 November 1973",
        "73/78 in force": r"2 October 1983",
        "Annex VI in force": r"19 May 2005",
        "1997 Protocol done": r"26 September 1997",
        "SOLAS PROT 1988 in force": r"3 February 2000",
        "LLMC PROT 1996 in force": r"13 May 2004",
        "LSA Code mandatory": r"1 July 1998",
    }
    lost = [k for k, rx in capsule.items() if not re.search(rx, q6)]
    report("verified_date_capsule_intact", not lost, "lost=%s" % (lost or "none"))

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failing: %s" % ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
