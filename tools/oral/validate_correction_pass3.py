#!/usr/bin/env python3
"""
Content validator for GPT REVIEW PASS 3 -- the two residual content records.

WHY A CONTENT GATE AND NOT JUST THE DIGEST PIN
----------------------------------------------
`validate_corrections.py` proves the shipped bytes are the authorised bytes.
SKILL.md 8.2a is explicit that this is a different question from "is what was
authorised actually correct?", and a pin is perfectly content with wrong text.

Both defects this pass corrects are of exactly the kind a pin cannot see,
because both cite a REAL instrument and use REAL words about a REAL process:

    a term the IMO Casualty Investigation Code does not use, attributed to it
    a clause about the MASTER, cited as the basis for a CHIEF ENGINEER's duty

Neither is a wrong fact of the kind a fact check finds.  So the substance is
asserted here as NAMED checks, one per proposition a future well-meaning edit
could quietly lose, and each is named so that `mutate_correction_pass3.py` can
require its mutation to trip THAT check rather than the digest pin -- which
fires on any edit at all and would let every substantive check rot as dead
code.

NEGATIVES RUN ON UNESCAPED TEXT
-------------------------------
A guard spelled `h&m` is blind to `h&amp;m` (CORR-E1).  Every banned-phrase
search below runs against `html.unescape()` of the page, never raw markup.

THE ALLOWLIST-HYGIENE CHECK IS THE INTERESTING ONE
--------------------------------------------------
Pass 2B could not correct these two sites -- they were outside its
authorisation -- so it did the honest thing and ENUMERATED them in
`validate_correction_msact2b.ADJUDICATED` as "reported, not corrected".  This
pass corrects them, which turns those two enumeration entries into STALE
NO-OPS: entries that can never match, and that therefore silently license
their own phrasings if anyone reinstates them.

That is a known defect class in this repository (the content-index escape
sequences that were stale no-op mutations).  So this gate does not merely
require the two entries to be gone -- it requires EVERY entry in that
allowlist to still match a live occurrence.  An allowlist that has stopped
describing the corpus is an allowlist that has stopped guarding it.
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

RECORDS = {
    "CIC": "correction_corr_cicterm_20260904_manifest.json",
    "ISM": "correction_corr_ismsec5_20260904_manifest.json",
}

_checks = 0
_failed: list[str] = []


def report(name: str, ok: bool, detail: str = "") -> None:
    global _checks
    _checks += 1
    print("%-4s %-52s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        _failed.append(name)


TAG = re.compile(r"<[^>]+>")


def flat(s: str) -> str:
    return " ".join(TAG.sub(" ", s).split())


_pages: dict[str, str] = {}


def page(rel: str) -> str:
    if rel not in _pages:
        _pages[rel] = html.unescape(read_text(MEO / rel))
    return _pages[rel]


def card(rel: str, anchor: str) -> str:
    t = page(rel)
    i = t.find('id="%s"' % anchor)
    if i < 0:
        return ""
    j = t.find('class="q-card"', i + 10)
    return t[i:j if j > 0 else len(t)]


def main() -> int:
    print("correction content validator: GPT REVIEW PASS 3")

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

    # Both records descend from a Pass 2B correction.  A record that lost its
    # supersession claim would leave the Pass 2B pin red on a legitimately
    # corrected card, which is the failure mode the chain exists to prevent.
    for key, want in (("CIC", "CORR-MSACT2B-C-03"), ("ISM", "CORR-MSACT2B-A-01")):
        rec = records.get(key) or {}
        claims = [c.get("supersedes") for c in rec.get("cards", [])
                  if c.get("supersedes")]
        report("record_%s_declares_supersession" % key,
               len(claims) == 1 and claims[0].get("action_id") == want,
               "supersedes %s" % (claims[0].get("action_id") if claims else "-"))

    # ============================================================ PART C
    print("\n[C: the Casualty Investigation Code's own term]")

    q5 = card("QB5_C_B.html", "q5")
    report("cic_card_found", bool(q5), "%d chars" % len(q5))

    # 1. THE NEGATIVE.  Enumerated, not heuristic: the two exact surfaces the
    #    review adjudicated.  A flat ban on "formal investigation" is wrong
    #    here for the same reason it was wrong in Pass 2B -- the card's own MS
    #    Act bullet must be free to say the 2025 Act does NOT use the phrase.
    #
    #    AND IT RUNS ON TAG-STRIPPED TEXT, not on markup. The first version
    #    searched the card's raw HTML, and mutation A ESCAPED it: the stale
    #    sentence reads "under the <strong>IMO Casualty Investigation
    #    Code</strong>", so the banned phrase spans a tag and a raw search can
    #    never match it. Same family as the entity-escape defect (`h&m` blind
    #    to `h&amp;m`) -- a candidate reads rendered text, so a guard over
    #    candidate-facing wording has to read rendered text too. Pass 2B's own
    #    gate caught that mutation; this one did not, until now.
    banned = (
        "formal investigation phase under the IMO Casualty Investigation Code",
        "Formal Investigation & Evidence Preservation Procedure",
    )
    rendered = flat(q5)
    present = [b for b in banned if b in rendered]
    report("no_imo_code_formal_investigation_attribution", not present,
           "still present: %s" % (present or "-"))

    # 2. THE POSITIVE.  Deleting the sentence would satisfy the negative by
    #    SILENCE, which is a worse card rather than a better one.
    #
    #    SCOPED TO THE 60-SECOND BLOCK, not to the card. The card's Numbers/Regs
    #    list independently says "ISM Code Section 9" and "marine safety
    #    investigations", so a card-wide search would stay green with the
    #    corrected sentence deleted outright -- the check would be asserting
    #    another paragraph's content and calling it this one's.
    i = q5.find("60-Second Answer")
    j = q5.find('<div class="answer-body"', i)
    sixty = q5[i:j] if i >= 0 and j > i else ""
    report("sixty_second_block_found", bool(sixty), "%d chars" % len(sixty))
    report("cic_term_marine_safety_investigation_taught",
           "marine safety investigation" in sixty.lower(),
           "%d mention(s) in the 60s block"
           % sixty.lower().count("marine safety investigation"))

    # 3. THE ATTRIBUTION.  The deeper defect: a Chief Engineer does not conduct
    #    a marine safety investigation -- CIC 2.13 gives that to a State's
    #    Authority.  A bare term-swap would have left a worse claim standing.
    f = flat(sixty)
    # The apostrophe here is U+2019, not U+0027, and html.unescape does not
    # normalise the two. A guard spelled with the ASCII apostrophe would be
    # blind to the page exactly as `h&m` was blind to `h&amp;m`.
    report("investigation_belongs_to_the_flag_state",
           re.search(r"flag State[’']s\s+marine safety investigation", f,
                     re.I) is not None,
           "the card names whose investigation it is")
    report("cic_investigation_not_claimed_by_the_ce",
           re.search(r"marine safety investigation Authority,?\s+not by me", f,
                     re.I) is not None,
           "the card says the investigation is the Authority's, not the CE's")

    # 4. What the CE actually runs.
    report("company_investigation_is_ism_9",
           re.search(r"ISM Code\s*(§|Section |Sec\.\s*)9", f) is not None,
           "the company limb is attributed to ISM 9")

    # 5. INVARIANTS -- what this correction asserts it did NOT change.
    report("msact_denial_survives",
           "The 2025 Act does not use" in q5 and "formal investigation" in q5,
           "the Pass 2B denial sentence is untouched")
    report("part_xi_four_steps_survive",
           all(x in q5 for x in ("s.231(2)", "s.231(3)", "s.231(5)", "s.232")),
           "24h notice / preliminary inquiry / MSI / action")
    report("msc255_84_still_cited", "MSC.255(84)" in q5, "the Code is still named")

    # ============================================================ PART D
    print("\n[D: ISM section 5 is the MASTER's, not the incoming CE's]")

    q1 = card("QB5_B.html", "q1")
    cheat = page("QB5_B_CheatSheet.html")
    report("ism_card_found", bool(q1), "%d chars" % len(q1))

    # 1. THE NEGATIVE, on the ISM Code only.  Scoped by instrument, because the
    #    cheat sheet legitimately cites STCW Reg. VIII/2 §5 for the 0.05% BAC
    #    limit and a bare "§5" ban would fire on it.
    ism5 = re.compile(r"ISM(\s+Code)?\s*(§|Section |Sec\.\s*)5\b")
    report("qb5b_q1_cites_no_ism_section_5", ism5.search(q1) is None,
           "match=%s" % (ism5.search(q1).group(0) if ism5.search(q1) else "-"))
    report("cheatsheet_cites_no_ism_section_5", ism5.search(cheat) is None,
           "match=%s" % (ism5.search(cheat).group(0) if ism5.search(cheat) else "-"))

    # 2. THE POSITIVE.  The right clause, named, with what it actually says.
    fq1 = flat(q1)
    report("qb5b_q1_names_ism_6_3",
           re.search(r"ISM Code\s*(§|Section |Sec\.\s*)6\.3", fq1) is not None,
           "the familiarisation clause is named")
    report("qb5b_q1_states_familiarisation_substance",
           "familiaris" in fq1.lower() and "new assignment" in fq1.lower(),
           "6.3's actual subject reaches the candidate")
    report("qb5b_q1_names_section_7_operations",
           re.search(r"(§|Section |Sec\.\s*)7\b", fq1) is not None
           and "key shipboard operations" in fq1.lower(),
           "the documented-procedures limb is named")
    report("qb5b_q1_names_the_company_sms_as_governing",
           re.search(r"Company'?s? own SMS handover procedure", fq1,
                     re.I) is not None,
           "the handover's real governing instrument")

    # 3. THE BOUNDARY.  The replacement must not claim what the old row claimed,
    #    only about a different clause.  Both halves are required: the denial
    #    must be there, AND no clause may be said to mandate a certificate.
    report("no_ism_clause_said_to_mandate_a_takeover_certificate",
           re.search(r"No ISM clause prescribes a CE takeover certificate",
                     fq1) is not None,
           "the denial is on the card")
    mandates = re.search(
        r"(§|Section |Sec\.\s*)(6\.3|7)[^.]{0,80}"
        r"(requires?|mandates?|prescribes?)[^.]{0,60}"
        r"(takeover|take-over|handover) certificate", fq1, re.I)
    report("no_clause_said_to_require_a_certificate", mandates is None,
           "match=%s" % (mandates.group(0)[:50] if mandates else "-"))
    report("section_5_named_as_the_masters",
           re.search(r"§5 is the .{0,12}Master", fq1) is not None,
           "the card inoculates against the clause it removed")

    # 4. The cheat sheet's corrected hook.
    prearrival = ""
    for row in re.findall(r"<tr>.*?</tr>", read_text(MEO / "QB5_B_CheatSheet.html"),
                          re.S):
        if "Pre-arrival" in row:
            prearrival = html.unescape(row)
    report("cheatsheet_prearrival_row_found", bool(prearrival),
           "%d chars" % len(prearrival))
    report("cheatsheet_prearrival_hook_corrected",
           "6.3" in prearrival and "SMS handover procedure" in prearrival,
           flat(prearrival)[-70:] if prearrival else "-")

    # 5. INVARIANTS.  A blind global substitution of "§5" would have broken
    #    both of these, which is exactly what makes them worth asserting.
    report("stcw_viii_2_para_5_untouched",
           cheat.count("VIII/2 §5") == 2,
           "%d STCW alcohol-limit citation(s) intact" % cheat.count("VIII/2 §5"))
    report("formal_declaration_row_survives",
           "no ISM clause prescribes a takeover certificate" in cheat,
           "the Pass 2B cheat-sheet correction is intact")
    report("qb5b_body_ism_sections_unchanged",
           "ISM Sec. 3 (company responsibilities), Sec. 6" in q1,
           "the card's own correct sentence is untouched")

    # ================================================== ALLOWLIST HYGIENE
    print("\n[allowlist hygiene: no stale no-op entries in the Pass 2B gate]")

    import validate_correction_msact2b as M2B                    # noqa: E402

    retired = (
        "I transition to the formal investigation phase under the IMO Casualty",
        "Formal Investigation & Evidence Preservation Procedure",
    )
    still_listed = [e for e in M2B.ADJUDICATED
                    if any(r in e or e in r for r in retired)]
    report("retired_allowlist_entries_removed", not still_listed,
           "still listed: %s" % (still_listed or "-"))

    # And the general form: every surviving entry must still be able to exempt
    # something.  "Alive" is defined as the gate itself defines a match -- an
    # entry must appear in the flattened NEIGHBOURHOOD of a real occurrence --
    # and the corpus is built by calling the gate's own windowing rather than
    # re-deriving one.
    #
    # That is not fastidiousness.  The first version of this check flattened
    # whole pages, which DROPS attribute text, and it therefore reported the
    # `data-kw="... preliminary inquiry, formal investigation ..."` entry as
    # dead when it is alive: the gate's 130-character window cuts the tag open,
    # so flattening the window keeps what flattening the page throws away. A
    # hygiene check that reconstructs its subject's semantics instead of
    # borrowing them tests its own reconstruction.
    surfaces = ["QB9_H.html", "QB5_C_B.html", "QB9_H_CheatSheet.html",
                "oralnotes/simon-notes-p6.html",
                "oralnotes/miw-notes-mgmt-p15.html"]
    windows = []
    for rel in surfaces:
        raw = page(rel)
        for m in re.finditer(r"formal[ \-]investigation", raw, re.I):
            windows.append(M2B.flat(raw[max(0, m.start() - 130):m.end() + 90]))
    dead = [e for e in M2B.ADJUDICATED
            if not any(e in w for w in windows)]
    report("adjudicated_windows_found", bool(windows),
           "%d live occurrence(s) across %d surface(s)" % (len(windows), len(surfaces)))
    report("no_adjudicated_entry_is_a_dead_noop", not dead,
           "dead=%s" % ([d[:44] for d in dead] or "-"))

    print("\n%d checks, %d FAIL" % (_checks, len(_failed)))
    if _failed:
        print("failed: %s" % ", ".join(sorted(set(_failed))))
    return 1 if _failed else 0


if __name__ == "__main__":
    sys.exit(main())
