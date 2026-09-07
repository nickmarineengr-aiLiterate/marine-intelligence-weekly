#!/usr/bin/env python3
"""Content gates for the three D01-S02 study-path corrections.

WHY THIS GATE IS WRITTEN DIFFERENTLY FROM ITS PREDECESSOR
---------------------------------------------------------
The D01-S01 gate asserted `"IACS HSSC" not in corpus`. That string genuinely
vanished, the check went green, and the commit message's claim was literally
true. The DEFECT survived in six sites that never contain the token - "the
IACS Harmonized System of Survey and Certification (HSSC) cycle" with the name
spelled out, "resets the 5-year HSSC clock", "Post-Renewal HSSC Matrix". A
token check certified a proposition it never looked at.

So the controls here are built on three rules:

1. MATCH THE PROPOSITION, NOT THE TOKEN. `_conflates()` looks for a
   class-subject and an HSSC-subject bound together by a possessive or
   equative construction, at sentence scope. It fires on "the IACS HSSC
   cycle", on "the Harmonized System of Survey and Certification cycle" for a
   class survey, and on "class operates under HSSC" - none of which share a
   literal string.

2. GUARD EVERY CANDIDATE-FACING LAYER, NAMED. A card-wide "phrase is present
   somewhere" test cannot tell a corrected REG-BOX from a defective 15-second
   answer, and that is exactly the state these two cards were left in. Each
   spoken layer is extracted and checked on its own.

3. THE CORRECTION'S OWN VERSION STAMP IS NOT EVIDENCE. It QUOTES the defect in
   order to record its removal. Every check strips provenance first, or it
   reports the audit trail as the defect (known_traps #89).
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
from census_known_defect_families import corpus_files, rel_of     # noqa: E402

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
    print("%-4s %-56s %s" % ("PASS" if ok else "FAIL", name, detail))


def flat(raw: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", raw)))


def teaching(block: str) -> str:
    """Candidate-facing text: provenance quotes the defect and is stripped."""
    return flat(re.sub(r'<span class="q-version">.*?</span>', " ", block,
                       flags=re.S))


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


def layers(block: str):
    """Every candidate-facing layer of a card, by name.

    Named individually because the defect these corrections fix lived in ONE
    layer while a sibling layer in the same card was already correct. A test
    that reads the card as one blob is blind to exactly that.
    """
    t = teaching(block)
    out = {"whole": t}
    for label, key in (("15-Second Answer", "15s"), ("60-Second Answer", "60s"),
                       ("15-Second", "15s"), ("60-Second", "60s")):
        i = t.find(label)
        if i >= 0 and key not in out:
            out[key] = t[i:i + 1400]
    for label, key in (("CE Oral Tip", "ce_tip"),
                       ("Examiner Chain", "chain"),
                       ("Numbers to Memorise", "numbers"),
                       ("Numbers &amp; Regulations", "numbers")):
        i = t.find(label)
        if i >= 0 and key not in out:
            out[key] = t[i:i + 900]
    return out


# ==========================================================================
# the PROPOSITION, not the token
# ==========================================================================

#: HSSC by any of its spellings - the acronym, or the name written out. The
#: previous gate knew only the two-word string "IACS HSSC", and the name
#: spelled out walked straight past it.
_HSSC = r"(?:HSSC|Harmoni[sz]ed System of Survey(?: and Certification)?)"
_CLASS = r"(?:class(?:ification)?(?: society)?)"

#: "the <HSSC> cycle/clock/framework/matrix/timeline/regime" used as the name
#: of the CLASS periodic survey regime, or a class subject bound to HSSC by an
#: equative or possessive verb.
CONFLATION = re.compile(
    r"(?:%s[^.]{0,60}?(?:operates?|runs?|follows?|is|are|on)[^.]{0,30}?%s"
    # NOT "framework" or "scheme": HSSC legitimately IS a framework, and
    # "the Cargo Ship Safety Certificate under the HSSC scheme" is correct
    # statutory usage that an earlier version of this pattern flagged. What
    # HSSC does NOT have is a "cycle" or a "clock" that a CLASS survey runs
    # on - those are the words that carry the defect.
    r"|%s\s+(?:cycle|clock|matrix|timeline)"
    r"|(?:resets?|reset)[^.]{0,40}%s"
    r"|%s[^.]{0,30}(?:renewal|special)\s+survey)"
    % (_CLASS, _HSSC, _HSSC, _HSSC, _HSSC), re.I)

#: The corrected text NAMES both regimes in one breath, because that is the
#: teaching point. A sentence that draws the distinction must not be read as
#: making the conflation, so an explicit separation acquits.
SEPARATED = re.compile(
    r"separate[^.]{0,40}(?:statutory|IMO|regime)"
    r"|statutory[^.]{0,40}%s[^.]{0,60}(?:separate|not)"
    r"|not[^.]{0,20}(?:a\s+)?shared clock"
    r"|aligned (?:alongside|in interval)"
    r"|not by (?:HSSC|Harmoni[sz]ed)"
    r"|is not[^.]{0,20}(?:HSSC|class)"
    r"|alignment,? not" % _HSSC, re.I)


#: Proposition boundaries. Full stops are not the only ones on these pages:
#: an ASCII box diagram separates its rows with box-drawing characters, and
#: without them "Class Status: No Open Conditions" and "Valid HSSC Statutory
#: Certificates" - two unrelated bullets in a checklist - merge into one
#: "sentence" and read as a conflation. Both bullets are correct as written.
_BOUNDARY = re.compile("|".join([
    r"(?<=[.;!?])\s+",
    "[" + "".join(chr(c) for c in (0x2502, 0x251C, 0x2524, 0x7C)) + "]+",
    r"\s+" + chr(0x2022) + r"\s+",
    r"\n",
]))


def conflates(text: str) -> list[str]:
    """Sentences that make the class-cycle-is-HSSC proposition."""
    bad = []
    for sent in _BOUNDARY.split(text):
        if CONFLATION.search(sent) and not SEPARATED.search(sent):
            bad.append(sent.strip()[:110])
    return bad


def main() -> int:
    # ============ RECORD A : HSSC/class reach ============================
    q1, q11, q9 = card("QB3_B.html", "q1"), card("QB3_B.html", "q11"), \
        card("QB3_B.html", "q9")
    L1, L11, L9 = layers(q1), layers(q11), layers(q9)

    report("A_proposition_matcher_is_not_a_token_matcher",
           bool(conflates("The system follows the IACS Harmonized System of "
                          "Survey and Certification cycle."))
           and bool(conflates("It resets the 5-year HSSC clock."))
           and bool(conflates("The classification survey system operates on "
                              "HSSC."))
           and not conflates("HSSC is a separate IMO statutory regime and does "
                             "not set the class cycle."),
           "catches three phrasings sharing no literal string; acquits the fix")

    for name, L in (("q1", L1), ("q11", L11), ("q9", L9)):
        for layer in ("whole", "15s", "60s", "ce_tip", "chain", "numbers"):
            if layer not in L:
                continue
            bad = conflates(L[layer])
            report("A_no_conflation_%s_%s" % (name, layer), not bad,
                   str(bad[:1] or "clean"))

    report("A_q11_states_what_a_class_renewal_actually_resets",
           re.search(r"class survey cycle", L11["15s"], re.I) is not None
           and re.search(r"statutory[^.]{0,120}(?:renewal survey|reissue)",
                         L11["60s"], re.I) is not None,
           "class period reset; statutory cycle reset by its own survey")
    report("A_q11_denies_the_shared_clock",
           re.search(r"not[^.]{0,30}(?:a\s+)?shared clock|aligned[^.]{0,60}"
                     r"not[^.]{0,30}(?:the )?same", L11["whole"], re.I)
           is not None,
           "aligned intervals are not one clock")
    report("A_q1_attributes_the_class_cycle_to_class_rules",
           re.search(r"UR\s*Z", L1["60s"]) is not None,
           "the class cycle's actual basis, in the spoken layer")

    # RC-08: ship type fixed; age band deliberately NOT asserted.
    # The body bullet and the REG-BOX row both carry this claim. Checking the
    # card as a whole let a mutation revert the ROW - putting the survey number
    # back under an "HSSC Annual Survey Checklist" title, which is itself the
    # conflation - while the bullet kept the check green.
    report("A_closeup_restricted_to_single_side_skin_bulk_carriers",
           "single side skin bulk carrier" in L1["whole"].lower()
           and "Z10.2" in L1["whole"]
           and "HSSC Annual Survey Checklist" not in L1["whole"]
           and re.search(r"IACS UR Z10\.2[^|]{0,40}Annual survey close-up",
                         L1["whole"]) is not None,
           "cargo hold side shell frames are an SSS feature, and the REG-BOX "
           "row cites Z10.2 rather than an HSSC checklist")
    report("A_closeup_no_longer_claims_oil_tankers",
           not re.search(r"Close-Up[^.]{0,40}Oil Tankers", L1["whole"], re.I),
           "Z10.1/Z10.4 govern oil tankers, not Z10.2")
    report("A_closeup_age_band_is_NOT_asserted",
           not re.search(r"(?:aged?|over|exceeding)\s+\d+\s+years?[^.]{0,80}"
                         r"25%|25%[^.]{0,80}(?:aged?|over|exceeding)\s+\d+\s+"
                         r"years?", L1["whole"], re.I)
           and "could not be verified" in L1["whole"],
           "SOURCE GAP declared, not guessed")
    # Scoped to the cards this record touched, and read WITHOUT provenance:
    # the version stamp names the citation in order to record its removal.
    # An earlier version of this check swept the whole corpus and failed on
    # QB3_A#q5 - a different card on a different topic, which section 16
    # puts out of scope. Over-reaching a check is not the same as being
    # thorough; it just makes the check unownable.
    _touched = [teaching(card("QB3_B.html", "q1")),
                teaching(card("QB1_F.html", "q8"))]
    report("A_tier6_citation_removed",
           not any("marinegyaan" in x.lower() for x in _touched),
           "a hard survey number must not rest on a blog "
           "(QB3_A#q5 carries one on another topic - out of scope, reported)")

    # RC-09
    report("A_zero_days_extension_claim_gone",
           "0 days" not in L11["whole"],
           "the annual window is six months wide and is not extended")
    report("A_class_extension_stated_with_its_scope",
           re.search(r"3 months[^.]{0,90}(?:exceptional|beyond the fifth)",
                     L11["whole"], re.I) is not None,
           "UR Z18 1.1.2")

    report("A_q9_control_is_byte_identical",
           card_digests(read_text(QB / "QB3_B.html"))["q9"]
           == "013eda598128e0f32eddd0503fa43ca975231639c40bfef15daf3245032acba0",
           "the session control, and Lane B's digest calibration")

    # ============ RECORD B : ESP ========================================
    q5 = card("QB3_B.html", "q5")
    L5 = layers(q5)
    # The corrected REG-BOX names A.1104(29) in order to DENY it is an ESP
    # instrument. A check that reads a denial as an assertion is the same
    # error as reading a version stamp as teaching - so a negation acquits.
    _a1104 = [x for x in re.split(r"(?<=[.;!?])\s+", L5["whole"])
              if "A.1104(29)" in x and re.search(r"ESP", x)
              and not re.search(r"\bnot\b|neither|is HSSC|statutory HSSC",
                                x, re.I)]
    report("B_A1104_not_taught_as_ESP", not _a1104,
           str(_a1104[:1] or "A.1104(29) is HSSC Survey Guidelines, 2015"))
    report("B_A1104_not_taught_as_current",
           not re.search(r"A\.1104\(29\)[^.]{0,60}[Cc]urrent(?![^.]{0,40}not)",
                         L5["whole"]),
           "superseded; current HSSC guidance is A.1207(34)")
    report("B_ESP_instrument_is_A1049",
           "A.1049(27)" in L5["whole"] and "30 November 2011" in L5["whole"],
           "the 2011 ESP Code, with its adoption date")
    report("B_mandating_regulation_retained",
           re.search(r"XI-1[^.]{0,10}(?:/|Reg)[^.]{0,10}2", L5["whole"])
           is not None,
           "SOLAS XI-1/2 was correct and is kept")
    report("B_replaces_A744_not_asserted",
           not re.search(r"replaces\s+A\.744", L5["whole"], re.I),
           "the preamble recasts; 'replaces' is not its language")

    esp_scope = [L5["whole"], teaching(card("QB1_F.html", "q16")),
                 teaching(card("QB1_G.html", "q30"))]
    # An earlier version required the word "ESP" within 140 characters of the
    # ship list. A mutation that wrote "It applies to bulk carriers, oil
    # tankers and chemical tankers" - with ESP named in the PREVIOUS sentence -
    # walked straight past it. What matters is the scope statement itself:
    # chemical tankers must never appear in an applies-to list unless the
    # sentence is denying it.
    def _bad_scope(txt):
        for sent in _BOUNDARY.split(txt):
            if not re.search(r"chemical tanker", sent, re.I):
                continue
            if not re.search(r"appl(?:ies|y|icable)|scope|covers?", sent, re.I):
                continue
            if re.search(r"\bnot\b|never|except|out of|class regime|Z10",
                         sent, re.I):
                continue
            return sent.strip()[:90]
        return None

    _scope_bad = [x for x in (_bad_scope(t) for t in esp_scope) if x]
    report("B_chemical_tankers_out_of_statutory_ESP_scope", not _scope_bad,
           str(_scope_bad[:1] or "3 surfaces: q5, QB1_F#q16, QB1_G#q30"))
    report("B_chemical_tanker_class_regime_named_instead",
           all(re.search(r"chemical tanker[^.]{0,160}Z10|Z10[^.]{0,160}"
                         r"chemical tanker", s, re.I) for s in esp_scope),
           "the defect converted into the teaching point")
    report("B_no_age_threshold_for_applicability",
           not re.search(r"(?:aged?\s+5 years and older"
                         r"|enters? (?:the )?ESP regime)", L5["whole"], re.I)
           and "no age threshold" in L5["whole"].lower(),
           "500 GT is the threshold; age drives scope")
    report("B_tonnage_threshold_present",
           re.search(r"500\s*(?:GT|gross tonnage)", L5["whole"], re.I)
           is not None,
           "Annex A part A 1.1.1")
    report("B_bulk_carrier_and_oil_tanker_scope_named",
           re.search(r"bulk carriers?[^.]{0,80}oil tankers?", L5["60s"], re.I)
           is not None,
           "Annex A and Annex B")

    # ============ RECORD C : CMS / PMS ==================================
    q4 = card("QB1_supplementary.html", "q4")
    t4 = teaching(q4)
    report("C_CMS_and_PMS_lists_are_separated",
           "Under CMS (UR Z18)" in t4 and "approved PMS (UR Z20) only" in t4,
           "two labelled lists, not one")
    # Bound the sample to the (A) section itself. An earlier version searched
    # 700 characters from the (A) heading, which ran straight through into the
    # (B) list and reported the correction as the defect.
    _a = t4.split("(A) Under CMS (UR Z18)", 1)
    _cms_section = _a[1].split("(B) Under an approved PMS", 1)[0] if len(_a) > 1 else ""
    report("C_PMS_items_not_under_the_CMS_heading",
           bool(_cms_section)
           and not re.search(r"crankshaft|thrust bearing|intermediate shaft"
                             r"|connecting rod|crosshead", _cms_section, re.I),
           "Z20 entitlements are not Z18 entitlements (%d chars sampled)"
           % len(_cms_section))
    report("C_multiple_engine_qualifier_restored",
           re.search(r"crankshafts? and bearings[^.]{0,120}multiple engine "
                     r"installations only", t4, re.I) is not None,
           "the qualifier the card had dropped")
    report("C_single_engine_consequence_stated",
           re.search(r"single-main-engine[^.]{0,200}crankshaft is[^.]{0,60}not",
                     t4, re.I) is not None,
           "which is the ship the card's own On My Vessel describes")
    report("C_maintenance_is_not_credit",
           re.search(r"maintenance[^.]{0,80}not the same[^.]{0,80}credit",
                     t4, re.I) is not None,
           "section 13 of the instruction")
    report("C_cylinder_liners_not_reserved",
           not re.search(r"REQUIRING Class Surveyor[^|]{0,400}?cylinder liners"
                         r"(?![^.]{0,80}NOT reserved)", t4, re.I),
           "liners are on the IRS section (A) CMS list")
    report("C_lists_attributed_to_the_society",
           "016/2014" in t4 and "not universal" in t4.lower(),
           "society rules, not a universal entitlement")
    # "UR Z18 appears somewhere in the card" is true even when the CMS
    # heading has been relabelled UR Z20 - the token survives elsewhere. The
    # attribution has to be checked where it is made.
    report("C_UR_attributions_unchanged_and_correct",
           "(A) Under CMS (UR Z18)" in t4
           and "(B) Under an approved PMS (UR Z20) only" in t4
           and re.search(r"Z7 is[^.]{0,60}Hull", t4, re.I) is not None,
           "audited per section 14; none was wrong, so none was invented")
    report("C_correct_layers_left_alone",
           re.search(r"crankshaft, thrust bearing, steering gear", t4, re.I)
           is not None,
           "the Numbers panel was already right")

    # ============ conflation scope: TWO scopes, deliberately ============
    # One scope cannot serve both purposes.
    #
    # (a) Over the cards this record TOUCHED, the full proposition matcher.
    #     These are the bytes I am accountable for.
    # (b) Over the WHOLE corpus, only the two forms that are unambiguous
    #     wherever they appear: HSSC attributed to IACS, and a survey said to
    #     RESET an HSSC clock.
    #
    # The broad matcher cannot go corpus-wide, because it fires on correct
    # content: "the Cargo Ship Safety Certificate under the HSSC scheme"
    # (QB1_G#q24) and "the ICOF's 5-year HSSC cycle" (QB2_A#q15) are RIGHT -
    # those are statutory certificates, and a statutory certificate's survey
    # cycle genuinely is HSSC. Widening a check until it fires on correct
    # content is how a sweep starts deleting the right things, and section 16
    # forbids whole-auditing unrelated cards.
    TOUCHED = [("QB3_B.html", "q1"), ("QB3_B.html", "q11"),
               ("QB3_B.html", "q5"), ("QB3_B.html", "q9"),
               ("QB1_F.html", "q8"), ("QB1_F.html", "q14"),
               ("QB1_F.html", "q16"), ("QB1_G.html", "q30"),
               ("QB1_G.html", "q31"), ("QB1_I.html", "q5"),
               ("QB1_F.html", "q7"), ("QB1_F.html", "q13"),
               ("QB1_supplementary.html", "q4")]
    sites = []
    for f, a in TOUCHED:
        bad = conflates(teaching(card(f, a)))
        if bad:
            sites.append("%s#%s :: %s" % (f, a, bad[0]))
    report("no_conflation_in_any_card_this_record_touched", not sites,
           str(sites[:2] or "%d cards clean" % len(TOUCHED)))

    IACS_HSSC = re.compile(r"IACS[^.]{0,40}" + _HSSC, re.I)
    RESET = re.compile(r"reset[^.]{0,50}" + _HSSC, re.I)
    wide = []
    for p_ in corpus_files():
        raw = read_text(p_)
        for m in re.finditer(r'<div class="q-card" id="(q[0-9]+)"', raw):
            blk = raw[m.start():_balanced_end(raw, m.start())]
            for sent in _BOUNDARY.split(teaching(blk)):
                if (IACS_HSSC.search(sent) or RESET.search(sent)) \
                        and not SEPARATED.search(sent):
                    wide.append("%s#%s :: %s"
                                % (rel_of(p_), m.group(1), sent.strip()[:80]))
                    break
    report("corpus_wide_no_IACS_HSSC_and_no_HSSC_reset_claim", not wide,
           str(wide[:2] or "none"))

    # ============ the records ===========================================
    for name, expect in (("hssc_reach", {("QB3_B.html", "q1"),
                                         ("QB3_B.html", "q11"),
                                         ("QB1_F.html", "q8"),
                                         ("QB1_F.html", "q14"),
                                         ("QB1_G.html", "q31"),
                                         ("QB1_I.html", "q5"),
                                         ("QB1_F.html", "q7"),
                                         ("QB1_F.html", "q13")}),
                         ("esp", {("QB3_B.html", "q5"), ("QB1_F.html", "q16"),
                                  ("QB1_G.html", "q30")}),
                         ("cms_pms", {("QB1_supplementary.html", "q4")})):
        man = json.loads(read_text(
            HERE / ("correction_corr_d01s02_%s_20260907_manifest.json" % name)))
        declared = set((c["file"], c["anchor"]) for c in man["cards"])
        report("record_%s_declares_every_card_it_touched" % name,
               declared == expect,
               "%d declared" % len(declared))
        for c in man["cards"]:
            live = card_digests(read_text(QB / c["file"]))[c["anchor"]]
            report("record_%s_%s_%s_post_digest_matches"
                   % (name, c["file"].split(".")[0], c["anchor"]),
                   c["post_edit_digest"] == live,
                   c["post_edit_digest"][:16])
            report("record_%s_%s_%s_pre_differs_from_post"
                   % (name, c["file"].split(".")[0], c["anchor"]),
                   c["pre_edit_digest"] != c["post_edit_digest"],
                   "a correction that changed nothing is not a correction")

    _claims = 0
    for nm in ("hssc_reach", "esp", "cms_pms"):
        m3 = json.loads(read_text(
            HERE / ("correction_corr_d01s02_%s_20260907_manifest.json" % nm)))
        _claims += sum(1 for c in m3["cards"] if c.get("supersedes"))
    report("records_declare_their_supersession_claims", _claims >= 10,
           "%d cards declare a predecessor - the resolver's own mechanism, "
           "not a bespoke re-derivation" % _claims)

    hssc = json.loads(read_text(
        HERE / "correction_corr_d01s02_hssc_reach_20260907_manifest.json"))
    report("record_hssc_declares_the_source_gap",
           "source_gap" in hssc and "Z10.2" in hssc["source_gap"],
           "an unretrievable source is recorded, not papered over")

    # ============ controls, untouched ===================================
    for label, path, anchor, digest in (
            ("QP2412_Q4", "pastpapers/QP2412.html", "q4",
             "8bbda01f6e0fc0548a5e02e9122544e0e6c0bf50f933b5d87bd7efbb550243d3"),
            ("QP2511_Q5", "pastpapers/QP2511.html", "q5",
             "edc2530804922b4728298aa57182aba46422245524949bca9509f6c554150ceb")):
        got = hashlib.sha256(
            article(path, anchor).replace("\r\n", "\n").encode("utf-8")
        ).hexdigest()
        report("control_%s_is_byte_identical" % label, got == digest,
               digest[:16])
    report("control_QP2511_Q5_still_states_ESP_correctly",
           "A.1049(27)" in flat(article("pastpapers/QP2511.html", "q5")),
           "the written control the corrected card now agrees with")

    _BS = chr(8)
    control_byte = [str(p.relative_to(REPO)) for p in sorted(
        (REPO / "tools").rglob("*.py")) if _BS in read_text(p)]
    report("no_control_byte_regex_in_the_toolchain", not control_byte,
           str(control_byte or "none"))

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: " + ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
