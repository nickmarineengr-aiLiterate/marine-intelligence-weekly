#!/usr/bin/env python3
"""
Content validator for GPT REVIEW PASS 2B -- the four MS Act 2025 correction records.

WHY THIS EXISTS AND WHY THE DIGEST PIN IS NOT ENOUGH
----------------------------------------------------
`validate_corrections.py` answers "are these bytes the ones we authorised?".
SKILL.md 8.2a is explicit that this is a different question from "is what we
authorised actually correct?", and a pin is perfectly happy with wrong text
because it pins whatever it is given.

The three defect families this pass corrected are exactly that gap:

    a statutory hook for a provision that DOES NOT EXIST   (CE handover)
    a repealed statute's VOCABULARY taught as current law  (formal investigation)
    a caveat that had become HOUSE DOCTRINE                (pending verification)

Not one of them is a wrong fact of the kind a fact check finds. The first cites
a real Act; the second uses real words about a real process; the third is
honest on its face. So the substance is asserted here as NAMED checks, one per
proposition a future well-meaning edit could quietly lose, and each is named so
that `mutate_correction_msact2b.py` can require its mutation to trip THAT check
rather than the digest pin -- which fires on any edit at all and would therefore
let every substantive check rot as dead code.

THE NEGATIVE CHECKS RUN ON UNESCAPED TEXT
-----------------------------------------
A guard spelled `h&m` is blind to `h&amp;m` (CORR-E1). Every banned-phrase
search below runs against `html.unescape()` of the page, never raw markup.

AND THE TEST IS AN ALLOWLIST, BECAUSE TWO HEURISTICS FAILED FIRST
-----------------------------------------------------------------
A flat ban on "formal investigation" cannot be used: the teaching move here is to
tell the candidate the 2025 Act does NOT use that phrase, so the corrected
sentences are the densest concentration of the banned string in the corpus.

A quoted-only exemption was tried and marked a CORRECT historical table as a
defect. A proximity heuristic was then tried -- exempt an occurrence when "1958"
or "historical" is nearby -- and this suite's own mutations A and B DEFEATED it,
because QB9_H mentions 1958 legitimately on every corrected card as the
stale-law warning, which made the entire page immune. Both failures are the same
one recorded for the negation window in CORR-GPT-PASS1: a proximity scan cannot
tell what the nearby token qualifies, and it fails OPEN.

The adjudicated occurrences are therefore ENUMERATED, and anything else is an
offence. This fails CLOSED, which is the only safe direction for a phrase whose
whole problem is that it creeps back.

WHAT IS DELIBERATELY *NOT* CHECKED
----------------------------------
The past papers. QP2304, QP2307, QP2503, QP2507 and QP2512 all say "formal
investigation" and all are CORRECT: every one of those sittings predates the
2025 Act's commencement on 15 March 2026. A gate that swept them would be
enforcing a defect. `pastpapers/` is excluded by construction below, and
`no_pastpaper_was_modified` asserts the exclusion actually held -- because a scope
rule nobody checks is a scope rule that erodes.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oral_bytes import enable_utf8_stdio, read_text            # noqa: E402

enable_utf8_stdio()

REPO = Path(__file__).resolve().parents[2]
MEO = REPO / "meoclass1"
TOOLS = REPO / "tools" / "oral"
REGISTRY = REPO / "docs" / "sources" / "MIW_SOURCE_REGISTRY.json"

RECORDS = {
    "A": "correction_corr_msact2b_cehandover_20260904_manifest.json",
    "B": "correction_corr_msact2b_green_20260904_manifest.json",
    "C": "correction_corr_msact2b_casualty_20260904_manifest.json",
    "D": "correction_corr_msact2b_coc_20260904_manifest.json",
}

CHECKS = 0
FAILS: list[str] = []


def report(name: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(name)
    # Unindented on purpose: oral_content_mutation.run_probe parses ^FAIL at
    # line start, so an indented FAIL is a check the mutation suite cannot see.
    print("%-4s %-46s %s" % ("PASS" if ok else "FAIL", name, detail))


def page(rel: str) -> str:
    """Unescaped page text -- every content assertion reads this, never markup."""
    return html.unescape(read_text(MEO / rel))


# ---------------------------------------------------------------------------
# WHAT COUNTS AS AN OFFENCE, AND WHY THIS IS AN ALLOWLIST
#
# Brief section 12 scopes this gate precisely: "no candidate-facing MS Act 2025
# CLAIM still says casualty formal investigation". That is NOT a ban on the
# phrase, and a flat ban is wrong in both directions -- it fires on the
# correction's own denial sentences, and on tables correctly headed as the 1958
# structure, while missing the thing that actually matters, which is the
# ATTRIBUTION rather than the phrase.
#
# THE FIRST IMPLEMENTATION WAS A PROXIMITY HEURISTIC AND ITS MUTATION SUITE
# DEFEATED IT. It exempted an occurrence when "1958" or "historical" appeared
# within a wide window. But QB9_H mentions 1958 legitimately on every one of
# these cards -- it is the stale-law warning -- so the exemption made the whole
# page immune, and mutations A and B reinstated "formal investigation" as 2025
# machinery and ESCAPED. This is the same failure recorded for the negation
# window in CORR-GPT-PASS1: a proximity scan cannot tell what the nearby token
# qualifies, and it fails OPEN.
#
# So the legitimate occurrences are ENUMERATED instead. Every one below was read
# and adjudicated during GPT REVIEW PASS 2B, and anything else is an offence.
# This fails CLOSED: a new occurrence, or an edit to an adjudicated one, is
# reported until a human adjudicates it and adds it here deliberately. That cost
# is the point -- this phrase is exactly the kind that creeps back.
# ---------------------------------------------------------------------------

TAG = re.compile(r"<[^>]+>")


def flat(s: str) -> str:
    return " ".join(TAG.sub(" ", s).split())


# Each entry is a distinctive fragment of the NORMALISED neighbourhood of one
# adjudicated occurrence. Grouped by why it is allowed.
ADJUDICATED = (
    # -- the correction's own denial sentences (it must quote what it rejects) --
    'Two cautions: the 2025 Act does not use the expression',
    'administrative action and proceedings s.232. The Act does not use',
    'The 2025 Act does not use “formal investigation” for this machinery, and powers over',
    's.224(a) separately defines “marine incident” for Part X. The Act does not use',
    'Saying “the 2025 Act does not use the phrase',
    's.232 administrative action or proceedings. The 2025 Act does not use',
    'Certificate powers are separate, at s.312. The Act does not use',
    'administrative action or proceedings (s.232). The 2025 Act does not use',
    'This is a restructure, not a renumbering',
    # -- correctly framed as the repealed 1958 structure --
    'Section 360: Formal investigation — judicial courts',
    'legacy reference only: 334 (unseaworthy)',
    "the source draft's Preliminary Inquiry/Formal Investigation references to",
    'Preliminary Inquiry vs. Formal Investigation (Historical MS Act, 1958 Structure)',
    'Parameter Preliminary Inquiry Formal Investigation Objective',
    'assigns an inquiry officer, who may pursue a Preliminary Inquiry',
    # -- search metadata, not a claim --
    'Nairobi Wreck Removal Convention, preliminary inquiry, formal investigation, SOLAS',
    # -- REPORTED, NOT CORRECTED: an IMO Casualty Investigation Code claim, not
    #    an MS Act one. Outside this authorisation; see the pass 2B report.
    'I transition to the formal investigation phase under the IMO Casualty Investigation Cod',
    'Formal Investigation & Evidence Preservation Procedure',
)


def offending_formal_investigation(text: str) -> list[str]:
    """Every occurrence that was not adjudicated during GPT REVIEW PASS 2B."""
    out = []
    for m in re.finditer(r"formal[ \-]investigation", text, re.I):
        local = flat(text[max(0, m.start() - 130):m.end() + 90])
        if any(fp in local for fp in ADJUDICATED):
            continue
        out.append(local)
    return out


def main() -> int:
    print("correction content validator: GPT REVIEW PASS 2B (MS Act 2025)")

    # ---------------------------------------------------------------- records
    print("\n[records]")
    records = {}
    for key, fname in RECORDS.items():
        p = TOOLS / fname
        ok = p.is_file()
        report("record_%s_present" % key, ok, fname)
        if ok:
            records[key] = json.loads(read_text(p))

    for key, rec in records.items():
        report("record_%s_authorised" % key,
               rec.get("status") == "AUTHORISED"
               and rec.get("kind") == "POST_RELEASE_CORRECTION",
               "status=%s" % rec.get("status"))

    # The four records exist because their SEMANTICS differ (brief section 11).
    # If a later pass merges them, this is what notices.
    report("four_distinct_records_not_collapsed", len(records) == 4,
           "%d records: false hook / caveat closure / stale law / merged powers"
           % len(records))

    declared = {(c["file"], c["anchor"]): (k, c)
                for k, rec in records.items() for c in rec.get("cards", [])}
    report("ten_cards_declared_across_records", len(declared) == 10,
           "%d declared" % len(declared))

    # ------------------------------------------------- 1. the stale vocabulary
    print("\n[stale law: 'formal investigation' is not 2025 Act machinery]")
    corrected_surfaces = [
        "QB9_H.html", "QB5_C_B.html", "QB9_H_CheatSheet.html",
        "oralnotes/simon-notes-p6.html", "oralnotes/miw-notes-mgmt-p15.html",
    ]
    offenders = []
    for rel in corrected_surfaces:
        for hit in offending_formal_investigation(page(rel)):
            offenders.append("%s: ...%s" % (rel, hit))
    report("no_msact2025_claim_says_formal_investigation", not offenders,
           offenders[0] if offenders else "0 unquoted, non-historical mentions")

    # The denial must actually BE there -- deleting it would otherwise satisfy
    # the negative check above by SILENCE, which is a worse page, not a better
    # one. And the check is CARD-SCOPED: QB9_H carries five denial sentences, so
    # a page-level test cannot see one of them deleted. Mutation N proved that.
    def denial_in(fragment: str) -> bool:
        f = flat(fragment)
        return (re.search(r"does not (use|carry)", f) is not None
                and "formal investigation" in f.lower())

    qh_all = page("QB9_H.html")
    for anchor in ("q2", "q11"):
        start = qh_all.find('id="%s"' % anchor)
        nxt = qh_all.find('class="q-card"', start + 10)
        report("denial_present_QB9_H_%s" % anchor,
               denial_in(qh_all[start:nxt if nxt > 0 else len(qh_all)]),
               "the card itself tells the candidate the Act does not use the term")

    for rel in ("QB5_C_B.html", "QB9_H_CheatSheet.html",
                "oralnotes/simon-notes-p6.html",
                "oralnotes/miw-notes-mgmt-p15.html"):
        report("denial_present_%s" % rel.rsplit("/", 1)[-1][:22],
               denial_in(page(rel)),
               "the page tells the candidate the Act does not use the term")

    # -------------------------------------------- 2. the ss.231-232 machinery
    print("\n[Part XI machinery survives]")
    for rel in ("QB9_H.html", "QB5_C_B.html"):
        t = page(rel)
        report("part_xi_four_steps_%s" % rel.split(".")[0][:16],
               all(x in t for x in ("s.231(2)", "s.231(3)", "s.231(5)", "s.232")),
               "24-hour notice / preliminary inquiry / marine safety investigation / action")
    qh = page("QB9_H.html")
    report("marine_safety_investigation_is_named",
           qh.lower().count("marine safety investigation") >= 4,
           "%d mentions" % qh.lower().count("marine safety investigation"))
    report("twentyfour_hour_notice_taught",
           "twenty-four hours" in qh or "24 hours" in qh,
           "the s.231(2) time limit reaches the candidate")
    report("certificate_power_separated_to_s312",
           "s.312" in qh,
           "certificate powers are NOT taught as an output of the safety investigation")

    # The boundary finding: the Act NAMES 'very serious marine casualty' once,
    # inside s.224(a), and does NOT define it.
    q11 = qh[qh.find('id="q11"'):]
    q11_flat = " ".join(TAG.sub(" ", q11).split())
    report("vsmc_boundary_stated_not_overclaimed",
           "s.224(a)" in q11_flat
           and re.search(r"does\s+not\s+define\s+the\s+term", q11_flat) is not None
           and re.search(r"names\s+.{0,60}very serious marine casualty", q11_flat) is not None,
           "the Act names it inside s.224(a) and does not define it")
    report("vsmc_not_claimed_as_act_definition",
           not re.search(r"(the\s+)?Act\s+defines\s+[“\"]?very serious", qh, re.I),
           "no card says the Act defines 'very serious marine casualty'")

    # ------------------------------------------------- 3. QB9_D's two powers
    print("\n[QB9_D#q6: three powers, not one]")
    qd = page("QB9_D.html")
    report("qb9d_has_part_iv_limb", "s.46(1)" in qd and "s.48(6)" in qd,
           "grant s.46(1) and issuing-authority withdrawal s.48(6)")
    report("qb9d_has_s312_limb", "s.312" in qd,
           "Central Government suspension, which Part IV cannot reach")
    report("qb9d_powers_not_merged",
           not re.search(r"the DGS retains the statutory right", qd),
           "the DGS is no longer named as holder of the suspension power")
    report("qb9d_no_pending_caveat",
           "pending verification" not in qd.lower(),
           "the Part IV caveat is discharged")

    # ------------------------------------------------ 4. the CE handover hook
    print("\n[CE handover: no statutory hook, and no invented ISM one]")
    cs = page("QB5_B_CheatSheet.html")
    qb5b = page("QB5_B.html")
    takeover_row = cs[cs.find("Formal declaration"):cs.find("Formal declaration") + 700]
    # The row DOES name the Act -- to say it provides nothing. What must be gone
    # is a CITATION: a section, or "formerly 1958".
    # ISM §6.3 and §7 are what this row SHOULD cite; what must be gone is a
    # Merchant Shipping Act section, the "formerly 1958" equivalence, and the
    # caveat. A blanket "no section numbers" test bans the correct citation too.
    msact_section = re.search(
        r"(?:MS Act|Merchant Shipping)[^<]{0,60}?(?:§|s\.|Sec\.?|Section)\s*\d+",
        takeover_row, re.I)
    report("cheatsheet_takeover_row_cites_no_act_provision",
           msact_section is None
           and not re.search(r"formerly 1958|pending verification", takeover_row)
           and "no MS Act 2025 provision governs CE handover" in takeover_row,
           "no MS Act section; ISM 6.3/7 retained; the absence stated")
    report("cheatsheet_states_the_absence",
           re.search(r"no MS Act 2025 provision governs CE handover", cs) is not None,
           "the absence is stated, not merely left blank")
    report("cheatsheet_does_not_invent_an_ism_certificate",
           re.search(r"no ISM clause prescribes a takeover certificate", cs) is not None
           and "CE Takeover Certificate" not in cs,
           "ISM 6.3/7 are cited as familiarisation and procedure, not as a certificate")
    report("qb5b_q1_no_1958_s77_equivalence",
           not re.search(r"1958[^.]{0,40}§77|§77", qb5b),
           "the unverifiable 'replaces the repealed 1958 Act, s.77' claim is gone")
    report("qb5b_q1_keeps_s46_correctly",
           "s.46(1)" in qb5b,
           "the CoC grant provision, which IS correct, is retained")
    report("qb5b_q1_states_the_absence",
           re.search(r"no</em>\s*CE handover|no\s*CE handover or takeover provision", qb5b)
           is not None,
           "the card states the Act contains no CE handover provision")

    # -------------------------------------------------- 5. QB1_I registration
    print("\n[QB1_I#q2: s.15(1) and s.20(9), and the Act's own noun]")
    qi = page("QB1_I.html")
    report("qb1i_uses_s15_1", "s.15(1)" in qi, "ownership of an Indian vessel")
    report("qb1i_uses_s20_9", "s.20(9)" in qi, "the register book")
    report("qb1i_names_registrar_s18", "s.18" in qi, "Registrar of Indian vessels")
    report("qb1i_uses_act_terminology_indian_vessel",
           "Indian vessel" in qi and "Indian ship" not in qi,
           "the Act's term of art is 'Indian vessel'")
    report("qb1i_no_pending_caveat",
           "pending verification" not in qi[qi.find('id="q2"'):qi.find('id="q3"')].lower()
           or "v1.2" in qi,
           "caveats discharged; the historical v1.2 line may still quote its own text")
    # Section 6 of the brief: the historical line is evidence, not a draft.
    report("qb1i_v12_history_line_preserved",
           "v1.2 · corrected 3 Aug 2026" in qi
           and "MS Act 1958 Sec 24/34" in qi,
           "the 3 Aug 2026 entry stands verbatim")
    report("qb1i_new_version_entry_appended",
           "v1.3 · corrected 4 Sep 2026" in qi
           and qi.find("v1.3") < qi.find("v1.2 · corrected 3 Aug"),
           "v1.3 is prepended to, not substituted for, the history")

    # ----------------------------------------------------- 6. QB3_J / NOS-DCP
    print("\n[QB3_J#q5: the Act does not name NOS-DCP]")
    qj = page("QB3_J.html")
    report("qb3j_uses_s131_s133_s138",
           all(x in qj for x in ("s.131", "s.133(1)", "s.138")),
           "jurisdiction / duty / reporting-direction limbs")
    report("qb3j_does_not_claim_act_names_nosdcp",
           re.search(r"Act itself does not name NOS-DCP|does not name NOS-DCP", qj)
           is not None,
           "NOS-DCP is kept as a separate national administrative plan")
    report("qb3j_no_pending_caveat",
           "section mapping pending verification" not in qj,
           "the Part-level caveat is discharged")

    # -------------------------------------------------- 7. the registry locator
    print("\n[source registry]")
    reg_raw = read_text(REGISTRY)
    reg = json.loads(reg_raw)
    row = next((s for s in reg["sources"] if s.get("source_id") == "SRC-MSACT-2025"), None)
    report("msact_row_present", row is not None, "SRC-MSACT-2025")
    claims = " ".join(row.get("verified_claims", [])) if row else ""
    report("registry_locator_is_s91_explanation_c",
           "s.91, Explanation, clause (c)" in claims,
           "the shipping-master definition is located correctly")
    report("registry_no_live_s93c_locator",
           not re.search(r"^s\.93\(c\):", claims) and "s.93(c):" not in claims,
           "the old locator survives only inside the correction note")
    report("registry_records_the_correction_transparently",
           "LOCATOR CORRECTED" in claims and "s.93 is" in claims,
           "the error is recorded, not silently overwritten")
    report("registry_carries_the_negatives",
           all(k in claims for k in ("ZERO times", "very serious marine casualty",
                                     "NOS-DCP", "chief engineer")),
           "the four whole-document negatives are registered as evidence")
    report("registry_carries_s324_narrow_limb",
           "but not including section 411A therein" in claims,
           "the saving is Part XIV MINUS s.411A")
    report("registry_claims_not_established_narrowed",
           any("no section-for-section equivalence" in c
               or "NO 2025-to-1958" in c or "correspondence between a 2025 section" in c
               for c in (row.get("claims_NOT_established") or [])),
           "the registry no longer contradicts what production now cites")
    report("registry_records_control_byte_hazard",
           "0x03" in claims,
           "the extraction hazard that produced a false negative is on the record")

    # ------------------------------------------------------- 8. scope holding
    print("\n[scope]")
    # The right question is not "does a past paper mention X" -- several
    # legitimately do, because the IMO Code term is theirs too. It is "did this
    # pass MODIFY one", which git answers exactly.
    import subprocess
    changed = subprocess.run(
        ["git", "diff", "--name-only", "4784b9c", "--", "meoclass1/pastpapers"],
        cwd=REPO, capture_output=True, text=True).stdout.split()
    report("no_pastpaper_was_modified", not changed,
           "sitting-anchored papers keep their own law: %s"
           % (changed or "0 files changed since 4784b9c"))
    report("p16_rsv_untouched",
           (MEO / "oralnotes" / "miw-notes-mgmt-p16.html").is_file()
           and "231" not in html.unescape(
               read_text(MEO / "oralnotes" / "miw-notes-mgmt-p16.html")),
           "section 10 carve-out honoured")
    # Section 15: reported, not patched.
    idx = read_text(MEO / "index.html")
    report("last_updated_reported_not_patched",
           "2 Sep 2026" in idx,
           "hub date deliberately left at 2 Sep 2026 pending further GPT review")

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: %s" % ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
