#!/usr/bin/env python3
"""Content gate for CORR-ITC51-20260908 - the ITC-Hulls termination clause.

The proposition, in one line: on Institute Time Clauses - Hulls (1/11/95),
AUTOMATIC TERMINATION of the insurance on change, suspension, discontinuance,
withdrawal or expiry of Class is **Clause 5.1**. Clause 4.2 is a different
mechanism - the Underwriters' discharge from liability for breach of the
Clause 4.1 duty to maintain class.

Design rules, following validate_correction_pass2.py and the instruction's
section 9:

  * PROPOSITION-SCOPED, NOT TOKEN-SCOPED. The gate that missed this defect
    asked "does the card name ITC-Hulls?" - a presence check, which a citation
    naming the right instrument and the wrong clause satisfies perfectly. Every
    check here binds a MECHANISM to a CLAUSE NUMBER, in the same sentence.

  * NOT SATISFIABLE BY A BLANKET SUBSTITUTION. A gate that merely forbade 4.2
    would be green after a global 4.2 -> 5.1 replace, which would corrupt every
    genuine Clause-4 proposition in the bank. So the gate asserts BOTH
    directions: automatic termination must cite 5.1, and the duty/breach
    discharge must still cite 4.2 where it is taught. Check 6 and check 7 are
    each other's opposites and cannot both be satisfied by one substitution.

  * SITE-SCOPED, NOT PAGE-SCOPED. QB4_A carries four ITC citations and QB4_C
    three, on one page each. "The page contains cl. 5.1 somewhere" passes on a
    page where three of four sites are stale, which is exactly the state these
    files were found in. Every ITC citation on every page is enumerated and
    judged on its own sentence.

  * PROVENANCE EXCLUDED FROM TEACHING CHECKS. The five version stamps written
    by this correction QUOTE "Clause 4.2" in order to record what moved, and
    they state what 4.2 actually is. A card-wide absence check would go red on
    the correction's own audit trail - trap 89. teaching() strips the footer
    before any teaching assertion runs. But the stamps are NOT exempt from the
    correctness rule: check 7 reads them and requires that where they name 4.2
    they describe the duty/breach mechanism, so the audit trail cannot become a
    hiding place for the defect.

  * NON-VACUOUS BY CONSTRUCTION. Every sweep asserts its target count before it
    judges anything, so ZERO TRUE MATCHES is distinguishable from ZERO INPUTS
    SCANNED. A gate that returns green over an empty file list is the failure
    mode this batch exists to close.

  * NO CHECK WHOSE SUBJECT IS THIS RECORD, except the one the manifest schema
    requires: `candidate_introduced` is admitted to CORRECTION_FIELD_CLASSES
    only on the standing condition that this gate asserts it, so check 11 does.
"""
from __future__ import annotations

import html as htmllib
import json
import pathlib
import re
import subprocess
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
    print("%-4s %-56s %s" % ("PASS" if ok else "FAIL", check, detail))


# --------------------------------------------------------------------------
# the sites this correction owns, declared, so the gate can prove it read them
# --------------------------------------------------------------------------

#: page -> number of ITC-Hulls clause citations that must exist in TEACHING
#: text (footers excluded). Asserted before any of them is judged.
TEACHING_SITES = {
    "QB1_C.html": 1,
    "QB1_F.html": 3,   # two CE Relevance copies + the reg-box "cl. 4 and 5.1"
    "QB1_G.html": 1,
    "QB4_A.html": 3,
    "QB4_C.html": 3,
    "QB4_A_CheatSheet.html": 1,
    "QB1_K_CheatSheet.html": 1,
}

#: cards whose q-version changelog must carry the correction stamp.
STAMPED = {
    "QB1_C.html": "q6",
    "QB1_F.html": "q7",
    "QB1_G.html": "q36",
    "QB4_A.html": "q9",
    "QB4_C.html": "q5",
}

MANIFEST = HERE / "correction_corr_itc51_20260908_manifest.json"

# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

CARD_OPEN = re.compile(r'<div class="q-card', re.I)


def card_html(page: str, anchor: str) -> str:
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


def strip_all_footers(markup: str) -> str:
    """Drop every q-footer: the version stamps quote the wording they removed."""
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


#: An ITC-Hulls clause citation: the instrument, then a clause number, with at
#: most a short span between them. Matches "cl. 5.1", "cl. 4 and 5.1",
#: "Clause 4.2". Anchored on the INSTRUMENT so a MLC "Regulation 4.2" or a
#: SOLAS "II-2/13.4.2.1" can never be mistaken for one.
CITE = re.compile(
    r"(?:Institute Time Clauses\s*[-–]\s*Hulls|ITC[-\s]?Hulls)"
    r"[^.;:]{0,60}?"
    r"\b(?:cl\.?|clause)\s*((?:\d+(?:\.\d+)?)(?:\s+and\s+\d+(?:\.\d+)?)?)",
    re.I)

#: The automatic-termination mechanism, in the words the corpus uses for it.
TERMINATES = re.compile(
    r"terminat\w*\s+hull\s+cover\s+automatically"
    r"|hull\s+cover\s+(?:then\s+)?terminat\w*\s+automatically"
    r"|cover\s+terminates\s+automatically"
    r"|automatic\s+termination\s+of\s+hull\s+cover", re.I)

#: The Clause 4 duty/breach mechanism - discharge from liability for breach of
#: the duty to maintain class. Distinct trigger, distinct consequence.
DUTY_BREACH = re.compile(
    r"discharge[d]?\s+from\s+liability"
    r"|breach\s+of\s+the\s+Clause\s*4\.1\s+duty"
    r"|duty\s+to\s+maintain\s+class", re.I)


def sites(page_text: str):
    """Every ITC clause citation with the sentence it lives in."""
    flat = flatten(page_text)
    out = []
    for m in CITE.finditer(flat):
        lo = max(0, flat.rfind(".", 0, m.start()) + 1)
        hi = flat.find(".", m.end())
        hi = len(flat) if hi < 0 else hi
        # a citation's mechanism can sit a clause or two away, so widen a
        # little either side rather than trusting one sentence boundary
        wide = flat[max(0, m.start() - 200):min(len(flat), m.end() + 260)]
        out.append({"clause": m.group(1), "sentence": flat[lo:hi], "wide": wide})
    return out


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

def main() -> int:
    pages = {}
    for name in TEACHING_SITES:
        p = QB / name
        if not p.exists():
            report("page_present:%s" % name, False, "MISSING")
            continue
        pages[name] = strip_all_footers(read_text(p))

    # 9. NON-VACUITY, first, because every check below is worthless without it.
    report("target_pages_all_readable", len(pages) == len(TEACHING_SITES),
           "%d/%d" % (len(pages), len(TEACHING_SITES)))

    all_sites = {n: sites(t) for n, t in pages.items()}
    total = sum(len(v) for v in all_sites.values())
    report("census_non_vacuous_total", total > 0, "%d ITC citation(s) found" % total)
    for name, n in TEACHING_SITES.items():
        got = len(all_sites.get(name, []))
        report("census_exact:%s" % name, got == n, "expected %d, found %d" % (n, got))

    # 1. Every site teaching automatic termination cites 5.1 - site-scoped.
    term_sites = 0
    bad = []
    for name, ss in all_sites.items():
        for s in ss:
            if TERMINATES.search(s["wide"]):
                term_sites += 1
                if "5.1" not in s["clause"]:
                    bad.append("%s: cl. %s -- %s" % (name, s["clause"],
                                                     s["sentence"][:90]))
    report("termination_census_non_vacuous", term_sites > 0,
           "%d automatic-termination site(s)" % term_sites)
    report("every_termination_site_cites_5_1", not bad,
           "stale=%r" % (bad[:3] if bad else None))

    # 2. No teaching site anywhere in the corpus still ties termination to 4.2.
    #    Corpus-wide, not just the declared pages: a defect that reappears in a
    #    file this record never touched is still this proposition's defect.
    scanned, corpus_bad = 0, []
    for p in sorted(QB.rglob("*.html")):
        try:
            t = strip_all_footers(read_text(p))
        except (OSError, UnicodeDecodeError):
            continue
        scanned += 1
        for s in sites(t):
            if TERMINATES.search(s["wide"]) and re.search(r"\b4\.2\b", s["clause"]):
                corpus_bad.append("%s: %s" % (p.name, s["sentence"][:90]))
    report("corpus_scan_non_vacuous", scanned > 50, "%d page(s) scanned" % scanned)
    report("no_corpus_site_ties_termination_to_4_2", not corpus_bad,
           "found=%r" % (corpus_bad[:3] if corpus_bad else None))

    # 3. The seed card's reg-box, which was right all along, is still right.
    qb1f = pages.get("QB1_F.html", "")
    report("qb1f_regbox_keeps_cl_4_and_5_1",
           re.search(r"cl\.?\s*4\s+and\s+5\.1", flatten(qb1f), re.I) is not None,
           "the entry the round-4 review read the mechanism out of")

    # 4. Governed changelog states the correct mechanism and clause.
    gov = json.loads(read_text(HERE / "qb_content_index_governed.json"))
    notes = " ".join(e.get("note", "") for e in gov.get("recently_updated", []))
    report("governed_changelog_non_vacuous", len(notes) > 500,
           "%d chars of changelog" % len(notes))
    report("governed_changelog_no_4_2_termination",
           not re.search(r"cl\.?\s*4\.2\s+terminates", notes, re.I),
           "the 7 Sep note attributed automatic termination to 4.2")
    report("governed_changelog_names_5_1",
           re.search(r"(?:cl\.?|Clause)\s*5\.1", notes) is not None)

    # 5. Generated index agrees with its governed source, note for note.
    idx = json.loads(read_text(QB / "qb_content_index.json"))
    gnotes = [e.get("note") for e in gov.get("recently_updated", [])]
    inotes = [e.get("note") for e in idx.get("recently_updated", [])]
    report("generated_index_matches_governed_changelog", gnotes == inotes,
           "%d governed vs %d generated" % (len(gnotes), len(inotes)))

    # 6/7. The two directions. Together these make a blanket substitution fail.
    #      6: no teaching site uses 4.2 for the termination mechanism (above).
    #      7: 4.2 SURVIVES where the duty/breach mechanism is the proposition -
    #         which after this correction is the five version stamps. Reading
    #         the footers here is deliberate: it is the one place 4.2 is still
    #         asserted, so it is the one place a wrong 4.2 could now hide.
    stamps_ok, stamps_seen = [], 0
    for name, anchor in STAMPED.items():
        page = read_text(QB / name)
        blk = card_html(page, anchor)
        stamp = blk[blk.find('<span class="q-version"'):]
        flat = flatten(stamp)
        if "ITC-Hulls clause correction" not in flat:
            stamps_ok.append("%s#%s: no correction stamp" % (name, anchor))
            continue
        stamps_seen += 1
        if re.search(r"\b4\.2\b", flat) and not DUTY_BREACH.search(flat):
            stamps_ok.append("%s#%s: names 4.2 without the duty/breach mechanism"
                             % (name, anchor))
        if not re.search(r"\b5\.1\b", flat):
            stamps_ok.append("%s#%s: does not name 5.1" % (name, anchor))
        # The stamp exists to record the DISTINCTION, so it must name both
        # clauses. Without this, a blanket 4.2 -> 5.1 substitution applied to
        # the stamp itself would delete the only surviving statement of what
        # Clause 4.2 is, and every other check here would stay green.
        if not re.search(r"\b4\.2\b", flat):
            stamps_ok.append("%s#%s: no longer states what Clause 4.2 is"
                             % (name, anchor))
    report("stamp_census_non_vacuous", stamps_seen == len(STAMPED),
           "%d/%d stamped" % (stamps_seen, len(STAMPED)))
    report("clause_4_2_survives_only_as_duty_breach", not stamps_ok,
           "problems=%r" % (stamps_ok[:3] if stamps_ok else None))

    # 8. The three layers stay separate: no PR1C or P&I proposition was
    #    rewritten as ITC-Hulls, and ITC-Hulls did not absorb either.
    for name, txt in pages.items():
        flat = flatten(txt)
        conflated = re.search(
            r"(?:PR1C|Procedural Requirement 1C)[^.;:]{0,60}"
            r"(?:terminates? hull cover|hull cover terminates)", flat, re.I)
        report("pr1c_not_rewritten_as_itc:%s" % name, conflated is None,
               "found=%r" % (conflated.group(0) if conflated else None))
    qb4a = flatten(pages.get("QB4_A.html", ""))
    report("qb4a_keeps_pandi_warranty_as_pandi",
           re.search(r"seaworthy and in class[^.]{0,80}"
                     r"fundamental warranty under standard P&I Club Rules",
                     qb4a, re.I) is not None,
           "the accurate half of that card's insurance claim")

    # 10. Cheat sheets do not disagree with their cards.
    for cs in ("QB4_A_CheatSheet.html", "QB1_K_CheatSheet.html"):
        ss = all_sites.get(cs, [])
        ok = bool(ss) and all("5.1" in s["clause"] for s in ss
                              if TERMINATES.search(s["wide"]))
        report("cheatsheet_agrees:%s" % cs, ok,
               "%d citation(s)" % len(ss))

    # 11. The manifest field the schema admits only because this gate reads it.
    man = json.loads(read_text(MANIFEST))
    ci = man.get("candidate_introduced", "")
    report("record_states_candidate_introduced_status",
           isinstance(ci, str) and len(ci) > 80 and "origin/main" in ci,
           "%d chars" % len(ci))
    # and the claim it makes is checked against origin/main, not believed
    absent = True
    for c in man["cards"]:
        try:
            blob = subprocess.run(
                ["git", "show", "origin/main:%s" % c["path"]],
                cwd=REPO, capture_output=True, text=True, encoding="utf-8",
                errors="replace")
        except OSError:
            absent = None
            break
        if blob.returncode == 0 and "cl. 4.2" in (blob.stdout or ""):
            absent = False
    report("candidate_introduced_claim_holds_against_origin_main", absent is True,
           "no ITC 'cl. 4.2' on origin/main in any corrected card"
           if absent else "claim does NOT hold")

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    for f in FAILS:
        print("  FAIL " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
