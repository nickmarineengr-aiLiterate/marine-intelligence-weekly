#!/usr/bin/env python3
"""Content gates for the pre-Tranche-4 propagation cleanup.

WHY THIS EXISTS
---------------
`validate_corrections.py` pins each corrected card's post-correction digest and
asks "are these bytes the ones we authorised?".  It cannot ask "is what we
authorised actually correct?", because a pin is perfectly happy with wrong text.

This pass closes two propagations that a previous correction left half-done, and
both are the kind that come back:

  * **CII capacity.**  Tranche 3C corrected QB6#q1 to teach `gCO2 per
    capacity-nm` with a ship-type-specific capacity term, and RECORDED IN ITS OWN
    MANIFEST that it was leaving QB6#q2 and QB6_cheatsheet.html uncorrected.  For
    four hours QB6.html taught two versions of one unit.  The failure mode these
    gates guard is not "somebody types DWT again" - it is "somebody equalises the
    file in the WRONG direction", making q1 agree with q2.
  * **UR Z7 / ESP.**  QB4_E taught `IACS UR Z7: ESP for Bulk Carriers and
    Tankers`.  UR Z7 is Hull Classification Surveys and applies to all
    self-propelled vessels; its own section 1.1.3 routes the additional tanker
    and bulk-carrier hull requirements to the Z10 series.  ESP is statutory - the
    2011 ESP Code, A.1049(27), mandatory through SOLAS XI-1/2.

THREE RULES THIS FILE OBEYS
---------------------------
1. **No check may be satisfied by the digest pin.**  Any edit trips the pin, so
   accepting it as the catch would prove only that the pin works while these
   substantive checks rot as dead code.  Nothing here reads a card digest.
2. **A correction quotes the wording it rejects**, so a flat banned-phrase grep
   fails on the very sentences carrying the fix - and on the correction footers,
   which must name the defect to be readable.  Every negative check below asserts
   that a rejected phrase is QUOTED OR NEGATED, never that it is absent.
3. **A scoped occurrence is not a defect.**  `gCO2/DWT.nm for my ship type` and
   `the container-ship CII (gCO2/DWT.nm)` are CORRECT and are kept.  The negative
   gates are therefore written against the corrected surfaces specifically, not
   against the corpus as a bag of strings - a corpus-wide ban would fail on cards
   that were right all along and would pressure a future editor to break them.

FAILS CLOSED.  If a held instrument cannot be read, that is reported and the exit
code is non-zero -- never skipped.

DIALECT
-------
Prints "<N> checks, <M> FAIL", the repo's standard batch-validator summary, so
`run_oral_release.py` classifies it with the shared validator parser.  This pass
does NOT register it as a release gate, on the brief's instruction.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_batch_b import CARD_OPEN, _balanced_end                # noqa: E402

REPO = Path(__file__).resolve().parents[2]
QB = REPO / "meoclass1"
TOOLS = REPO / "tools" / "oral"
SOURCES = REPO / "docs" / "sources"
REGISTRY = SOURCES / "MIW_SOURCE_REGISTRY.json"
UR_Z7 = SOURCES / "IACS-UR-Z7-Rev29-Corr1.pdf"
UR_Z7_SHA = "6b1e62488d85f230d970e0beed7b13cab76afc6812a1112ae2fd29788282ea84"

MANIFEST_CII = TOOLS / "correction_corr_pre_t4_cii_20260905_manifest.json"
MANIFEST_Z7 = TOOLS / "correction_corr_pre_t4_z7esp_20260905_manifest.json"

CHECKS: list[tuple[str, bool, str]] = []


def report(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append((name, bool(ok), detail))


def raw(rel: str) -> str:
    return (QB / rel).read_text(encoding="utf-8", newline="").replace("\r\n", "\n")


def page(rel: str) -> str:
    """Entity-unescaped page text.

    Unescaped because a guard spelled `>=500` is blind to `&ge;500`, and the same
    is true of every `&ldquo;`, `&mdash;` and `&#8322;` in these pages.
    """
    return html.unescape(raw(rel))


def card(rel: str, anchor: str) -> str:
    text = raw(rel)
    for m in CARD_OPEN.finditer(text):
        got = re.search(r'\bid="([^"]+)"', m.group(0))
        if got and got.group(1) == anchor:
            return html.unescape(text[m.start():_balanced_end(text, m.start())])
    raise AssertionError("card %s#%s not found" % (rel, anchor))


def strip_footer(block: str) -> str:
    """Card text with its q-version correction footer removed.

    A correction footer MUST quote the defect it corrected, so leaving it in
    would make every negative gate below unsatisfiable - or, worse, would push a
    future editor to write a vague footer that no longer names the error.
    """
    return re.sub(r'<span class="q-version">.*?</span>', "", block, flags=re.S)


def layer(block: str, cls: str) -> str:
    """The markup of ONE answer layer, balanced from its opening div.

    Deliberately NOT a `.*?</div>` regex. The first cut was one, and it silently
    returned the WRONG BLOCK for `oral-box oral-60`, whose label is a <span> and
    not a <div>: the lazy match closed on the box's own </div> and captured the
    deep-dive prose that follows it. It still worked for QB6's `tier tier-15`,
    whose label IS a div - so one layer dialect passed and the other quietly
    read the wrong text. Balanced extraction is dialect-independent.


    Exists because four gates in the first cut of this file were VACUOUS: they
    asked whether a phrase appeared anywhere in a card, and a mutation that
    removed it from the 15-second layer left the CE tip still carrying it, so
    the gate stayed green while the card taught the wrong thing at the layer a
    candidate answers from. A check that cannot say WHERE a proposition lives
    cannot notice it moving out of the place it is needed.
    """
    m = re.search(r'<div[^>]*class="[^"]*%s[^"]*"[^>]*>' % re.escape(cls),
                  block)
    if not m:
        return ""
    return block[m.start():_balanced_end(block, m.start())]


def negated_or_quoted(block: str, phrase: str, window: int = 420) -> bool:
    """True if EVERY occurrence of `phrase` sits inside a rejection."""
    markers = ("wrong", "not ", "no,", "never", "trap", "reject", "instead of",
               "rather than", "is not", "neither", "“", "”", "myth",
               "corrected", "was taught", "was given")
    for m in re.finditer(re.escape(phrase), block, re.I):
        lo = max(0, m.start() - window)
        near = block[lo:m.end() + window].lower()
        if not any(k in near for k in markers):
            return False
    return True


def sha256_of(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def pdf_text(path: Path) -> str | None:
    try:
        import pypdf
    except ImportError:
        try:
            import fitz
        except ImportError:
            return None
        try:
            doc = fitz.open(path)
        except Exception:
            return None
        return re.sub(r"\s+", " ", " ".join(p.get_text() for p in doc))
    try:
        r = pypdf.PdfReader(str(path))
    except Exception:
        return None
    return re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in r.pages))


# =====================================================================
# FAMILY A -- CII capacity propagation closure
# =====================================================================
UNIVERSAL_FORMS = ("gCO₂/DWT·nm", "gCO₂ / DWT·nm",
                   "per DWT-mile", "DWT × Distance_nm")


def family_a_cii() -> None:
    q1 = card("QB6.html", "q1")
    q2 = card("QB6.html", "q2")
    q2_body = strip_footer(q2)
    sheet = page("QB6_cheatsheet.html")

    # --- q1 must still be correct: this pass must not have moved it ---------
    q1_15s = layer(q1, "tier-15")
    report("cii_q1_still_teaches_capacity_not_universal_dwt",
           "gCO₂ per capacity-nautical-mile" in q1_15s
           and "gCO₂/DWT" not in q1_15s
           and "gCO₂ per capacity" in q1,
           "the capacity unit is bound to q1's 15-second layer, not merely "
           "present somewhere in the card")
    report("cii_q1_still_carries_the_ship_type_split",
           "gross tonnage (GT) for cruise passenger ships" in q1
           and "deadweight tonnage (DWT) for bulk carriers" in q1,
           "the DWT and GT category lists both survive in q1")
    for i, form in enumerate(("gCO₂/DWT·nm", "per DWT-mile"), 1):
        report("cii_q1_universal_form_%d_quoted_or_negated" % i,
               negated_or_quoted(q1, form),
               "any occurrence of %r in q1 is the quoted-and-rejected trap" % form)

    # --- q2: the headline of this pass -------------------------------------
    report("cii_q2_teaches_capacity_form",
           "gCO₂ per capacity·nm" in q2_body,
           "QB6#q2 now states the capacity unit")
    report("cii_q2_carries_the_ship_type_distinction",
           "ship-type specific" in q2_body
           and "DWT" in q2_body and "GT" in q2_body,
           "q2 names both capacity measures, not just the correct unit")
    report("cii_q2_names_the_gt_ship_types",
           "ro-ro" in q2_body and "cruise passenger" in q2_body,
           "the GT categories are named, so 'capacity' is not left abstract")
    for i, form in enumerate(UNIVERSAL_FORMS, 1):
        report("cii_q2_no_universal_form_%d" % i, form not in q2_body,
               "%r absent from q2 outside its footer" % form)

    # --- q2's short layers were to stay concise ----------------------------
    m = re.search(r'tier tier-15.*?</div>(.*?)</div>', q2, re.S)
    report("cii_q2_15s_layer_still_states_no_cii_unit",
           bool(m) and "DWT" not in m.group(1) and "capacity·nm" not in m.group(1),
           "the 15-second layer was left alone, not padded with the correction")

    # --- the two cards in one file must now agree --------------------------
    report("cii_qb6_file_teaches_one_unit_not_two",
           strip_footer(page("QB6.html")).count("gCO₂ per capacity") >= 6,
           "q1 and q2 express the same unit in the same words")

    # --- the revision layer -------------------------------------------------
    report("cii_cheatsheet_formula_uses_capacity",
           "Attained CII (gCO₂ per capacity·nm)" in sheet
           and "÷ (C × Distance_nm)" in sheet,
           "the cheat sheet formula box no longer divides by DWT")
    report("cii_cheatsheet_unit_row_uses_capacity",
           "gCO₂ / capacity·nm" in sheet,
           "the Unit row is corrected")
    report("cii_cheatsheet_states_what_capacity_is",
           "Capacity C" in sheet and "ro-ro" in sheet
           and "MEPC.412(84)" in sheet,
           "the cheat sheet supplies the replacement fact and its source, "
           "not merely the absence of the wrong one")
    report("cii_cheatsheet_examiner_tip_drills_capacity_first",
           "Always say gCO₂ per capacity·nm" in sheet,
           "the Nair reflex tip no longer drills the wrong unit")
    report("cii_cheatsheet_comparison_table_row_corrected",
           "<td>gCO₂ per capacity·nm</td>" in sheet,
           "the CII-vs-GFI table Unit row is corrected")
    for i, form in enumerate(UNIVERSAL_FORMS, 1):
        report("cii_cheatsheet_no_universal_form_%d" % i, form not in sheet,
               "%r absent from the revision layer" % form)

    # --- what must NOT have been swept -------------------------------------
    report("cii_eedi_reference_line_preserved",
           "Ref Line = a × DWT" in sheet and "174.22" in sheet,
           "the EEDI container reference line is genuinely DWT-based and was kept")
    report("cii_scoped_occurrences_kept_qb3j",
           "for my ship type" in page("QB3_J.html")
           and "CII units for container ships" in page("QB3_J.html"),
           "QB3_J's correctly-scoped DWT statements were not damaged")
    report("cii_scoped_occurrences_kept_qb1k",
           "container-ship CII" in page("QB1_K.html"),
           "QB1_K's tonnage-definition use of the unit was not damaged")
    report("cii_scoped_occurrences_kept_qb7a",
           "gCO₂/DWT·nm or gCO₂/GT·nm" in page("QB7_A.html"),
           "QB7_A already named both measures and was not touched")
    report("cii_inoculating_trap_kept_in_q1",
           "So CII is always gCO₂ per DWT·nm?" in q1,
           "the corpus's own trap against this defect still exists")

    # --- the record ---------------------------------------------------------
    man = json.loads(MANIFEST_CII.read_text(encoding="utf-8"))
    report("cii_manifest_authorised", man.get("status") == "AUTHORISED",
           man.get("correction_id", "?"))
    report("cii_manifest_pins_q2_only",
           [(c["file"], c["anchor"]) for c in man["cards"]] == [("QB6.html", "q2")],
           "one card pinned; the cheat sheet is a revision surface and carries no digest")
    report("cii_manifest_records_the_predecessor_undercount",
           "FIVE" in man["candidate_verdict"] and "4 sites" in man["candidate_verdict"],
           "the deferral list's own miscount is recorded, not absorbed")


# =====================================================================
# FAMILY B -- UR Z7 is Hull Classification Surveys, not ESP
# =====================================================================
def family_b_z7() -> None:
    q9 = strip_footer(card("QB4_E.html", "q9"))
    q12 = strip_footer(card("QB4_E.html", "q12"))
    notes = page("oralnotes/simon-notes-p3.html")

    # --- the defect is gone -------------------------------------------------
    report("z7_q9_no_longer_calls_z7_esp",
           "UR Z7: ESP" not in q9 and "IACS UR Z7 / ESP" not in q9
           and "ESP (IACS UR Z7)" not in q9,
           "every QB4_E#q9 site that equated Z7 with ESP is gone")
    report("z7_q12_no_longer_calls_z7_esp",
           "UR Z7 for the Enhanced Survey Programme" not in q12
           and "UR Z7 (ESP)" not in q12 and "UR Z7 for ESP" not in q12,
           "every QB4_E#q12 site that equated Z7 with ESP is gone")
    report("z7_notes_no_longer_calls_z7_1_esp",
           "mandatory under IACS UR Z7" not in notes
           and ">IACS UR Z7.1<" not in notes,
           "the false ATTRIBUTION is gone from both the prose and the reg code. "
           "negated_or_quoted() was tried here first and produced a FALSE PASS: "
           "its 420-char window found the words 'Not mandatorily' in the very "
           "next sentence, which is about container ships and has nothing to do "
           "with the claim. An unrelated neighbouring negation must not be able "
           "to launder a restored error, so this gate matches the attribution "
           "literally instead")

    # --- Z7 is positively re-identified, not merely deleted ----------------
    report("z7_q9_states_what_z7_actually_is",
           q9.count("Hull Classification Surveys") >= 2
           and q9.count("all self-propelled vessels") >= 2,
           "q9 re-identifies Z7 at BOTH sites that carried the false claim - "
           "the Numbers/Regs box and the reg box. Requiring two occurrences is "
           "what makes this a binding check rather than a presence check: the "
           "reg box alone would satisfy 'appears in the card'")
    report("z7_q12_states_what_z7_actually_is",
           "hull classification surveys" in q12.lower(),
           "q12 re-identifies Z7 rather than dropping it")
    report("z7_notes_states_what_z7_and_z71_actually_are",
           "Hull Classification Surveys" in notes
           and "water level detector" in notes,
           "the notes page identifies BOTH mis-cited URs")

    # --- ESP is tied to an actually applicable authority -------------------
    for name, block in (("q9", q9), ("q12", q12), ("notes", notes)):
        report("z7_%s_ties_esp_to_z10_series" % name,
               "Z10" in block,
               "the enhanced bulk-carrier / oil-tanker surveys point at the Z10 series")
    q9_60s = layer(q9, "oral-60")
    report("z7_q9_cites_the_statutory_esp_authority",
           "SOLAS Reg XI-1/2" in q9_60s and "ESP Code" in q9_60s
           and "A.1049(27)" in q9,
           "the statutory authority is bound to the 60-second answer - the "
           "layer that actually asserts why ESP binds - and the resolution "
           "number is somewhere in the card")
    report("z7_notes_cites_the_statutory_esp_authority",
           "A.1049(27)" in notes and "XI-1/2" in notes,
           "the notes page cites the ESP Code, not a UR, for mandatory status")

    # --- no invented precision ---------------------------------------------
    for name, block in (("q9", q9), ("q12", q12), ("notes", notes)):
        report("z7_%s_asserts_no_guessed_z10_sub_number" % name,
               not re.search(r"Z10\.\d", block),
               "generic Z10 series only; the sub-number mapping is unresolved "
               "and is NOT guessed")

    # --- alignment target must still be correct ----------------------------
    q1i = page("QB1_I.html")
    report("z7_esp_alignment_target_intact",
           "A.1049(27)" in q1i and "XI-1/2" in q1i
           and q1i.count("IACS UR Z10") >= 2,
           "QB1_I#q1 carries the Z10 alignment at BOTH its sites - the "
           "60-second answer and the reg box. One occurrence is not enough: "
           "corrupting the prose while the reg box survives would leave the "
           "corpus internally consistent and uniformly wrong")

    # --- custody ------------------------------------------------------------
    got = sha256_of(UR_Z7)
    report("z7_source_held_and_hash_matches", got == UR_Z7_SHA,
           "%s" % ((got or "MISSING")[:16]))
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    row = next((s for s in reg["sources"]
                if s.get("source_id") == "SRC-IACS-URZ7-REV29-CORR1"), None)
    report("z7_registry_row_present", row is not None, "SRC-IACS-URZ7-REV29-CORR1")
    if row is not None:
        report("z7_registry_title_is_hull_classification_surveys",
               "Hull Classification Surveys" in row.get("title", ""),
               "the registry was right while the corpus was wrong")
        report("z7_registry_sha_matches_disk", row.get("sha256") == got,
               "registry hash and the file on disk agree")

    text = pdf_text(UR_Z7)
    if text is None:
        report("z7_source_readable", False,
               "UNAVAILABLE -- reported, never skipped")
    else:
        report("z7_source_readable", True, "%d chars extracted" % len(text))
        report("z7_source_title_is_hull_classification_surveys",
               "Hull Classification Surveys" in text,
               "the held instrument's own title refutes the corrected claim")
        report("z7_source_applies_to_all_self_propelled_vessels",
               "apply to all self-propelled vessels" in text,
               "section 1.1.1 -- Z7 is not a two-ship-type regime")
        report("z7_source_routes_esp_ship_types_to_z10",
               "Z10.1, Z10.2, Z10.3, Z10.4, Z10.5" in text,
               "section 1.1.3 -- Z7 itself sends tankers and bulk carriers to Z10")
        report("z7_source_defines_z7_1_as_water_level_detectors",
               "water level detectors fitted on single hold cargo ships" in text,
               "section 1.1.5 -- what UR Z7.1 really is")

    # --- the record ---------------------------------------------------------
    man = json.loads(MANIFEST_Z7.read_text(encoding="utf-8"))
    report("z7_manifest_authorised", man.get("status") == "AUTHORISED",
           man.get("correction_id", "?"))
    report("z7_manifest_pins_both_cards",
           sorted((c["file"], c["anchor"]) for c in man["cards"])
           == [("QB4_E.html", "q12"), ("QB4_E.html", "q9")],
           "q9 and q12 pinned; the notes page carries no card digest")
    report("z7_manifest_records_the_unresolved_sub_number",
           "UNRESOLVED" in man["authority"]["open_question_referred_forward"],
           "the Z10.1/Z10.2 ambiguity is referred forward, not silently resolved")
    report("z7_manifest_records_the_swept_find",
           "simon-notes-p3" in json.dumps(man["propagation"], ensure_ascii=False),
           "the site the sweep found but the brief did not name is recorded")


# =====================================================================
# CROSS-FAMILY -- what this pass was forbidden to touch
# =====================================================================
def family_c_restraint() -> None:
    hub = page("index.html")
    report("restraint_hub_date_unchanged",
           "2 Sep 2026" in hub,
           "the hub 'Last Updated' date was not moved")
    idx = json.loads((QB / "qb_content_index.json").read_text(encoding="utf-8"))
    report("restraint_corpus_totals_unmoved",
           idx.get("total_questions") == 761 and idx.get("total_files") == 86,
           "761 / 86")
    report("restraint_no_release_gate_registered",
           "validate_correction_pret4" not in
           (TOOLS / "oral_release_gates.py").read_text(encoding="utf-8"),
           "these gates are deliberately NOT registered in the release suite")


def main() -> int:
    for fn in (family_a_cii, family_b_z7, family_c_restraint):
        try:
            fn()
        except Exception as exc:                                   # fail closed
            report("%s_ran" % fn.__name__, False,
                   "%s: %s" % (type(exc).__name__, exc))

    width = max(len(n) for n, _, _ in CHECKS)
    for name, ok, detail in CHECKS:
        print("%s %-*s %s" % ("PASS" if ok else "FAIL", width, name, detail))
    failed = sum(1 for _, ok, _ in CHECKS if not ok)
    print("\nPre-Tranche-4 cleanup content gates: %d checks, %d FAIL"
          % (len(CHECKS), failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
