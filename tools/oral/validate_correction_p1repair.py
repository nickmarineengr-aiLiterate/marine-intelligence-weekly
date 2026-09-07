#!/usr/bin/env python3
"""Content gate for CORR-P1REPAIR-20260906.

Every check here exists because a Pass-1 check did not. The gates this repair
hardens were written by the session that made the edits, and four of them passed
while asserting nothing. So this gate is written to the opposite standard: each
check names a reachable failing state, and the mutation suite reaches it.

THE TWO PROPOSITIONS THAT MUST STAY TRUE
----------------------------------------
1. No candidate-facing surface anywhere in the corpus teaches a bar figure as a
   hydrant minimum, IN ANY CAPITALISATION. The Pass-1 check was case-sensitive
   and that is exactly how the escape survived, so this one lower-cases both
   sides and the suite attacks it with three spellings.
2. No current-teaching surface anywhere in the corpus teaches BMP5 as the live
   publication - and "anywhere" means the RECURSIVE corpus, because the Pass-1
   censuses saw 128 of 224 files.

WHY THIS GATE READS THE WHOLE CORPUS AND THE PASS-1 GATES DID NOT
-----------------------------------------------------------------
A record that repairs a scope defect cannot be guarded by a check with the same
scope. The enumeration is imported from the single corpus function; it is never
re-globbed here. `test_corpus_scope.py` separately proves that function is
recursive, by planting a file where a top-level glob cannot see it.

SURFACE POLICY IS ENFORCED, NOT ASSUMED
---------------------------------------
`pastpapers` is sitting-anchored and its historical wording is CORRECT. This
gate asserts positively that past papers were left alone, because the failure
mode of a recursive sweep is the opposite of the failure mode it fixes: having
been caught missing 96 files, the tempting over-correction is to modernise an
examiner's own question.
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
QB_ROOT = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import read_text                                  # noqa: E402
from validate_batch_h_series import card_digests, _balanced_end   # noqa: E402
from oral_supersession import resolve_authorised_card_state       # noqa: E402
from census_known_defect_families import (                        # noqa: E402
    corpus_files, rel_of, surface_family)
#: The semantic detectors, imported - never re-implemented per gate. Three
#: escapes in a row came from a guard that knew a spelling or an HTML shape
#: instead of a proposition; one implementation is what stops the fourth.
from oral_currentness import (                                    # noqa: E402
    firemain_scope_defects, bmp5_current_teaching, to_mpa)

CORRECTION_ID = "CORR-P1REPAIR-20260906"
MANIFEST = HERE / "correction_corr_p1repair_20260906_manifest.json"
INDEX = REPO / "meoclass1/qb_content_index.json"
TRAPS = REPO / "meoclass1/known_traps.md"

CURRENT = "BMP Maritime Security"
UPPER = "0.27 N/mm² at 6,000 GT and upwards"
LOWER = "0.25 N/mm² below"

#: A bar figure asserted as a HYDRANT / fire-main minimum. Case-insensitive
#: over normalised whitespace - the whole point of this record - and SCOPED to
#: the quantity SOLAS II-2/10.2.1.6 fixes. Unscoped, it also matched the
#: weathertightness hose test ("minimum pressure of 2 Bar"), which is a
#: different quantity, has no held governing source, and is already declared as
#: K-ITEM-HOSE-TEST-PRESSURE. Widening a negative check until it fires on
#: legitimate content is how a sweep starts deleting the wrong things.
#: THREE elements, all required: a bar figure, a hydrant/fire-main subject, and
#: MANDATORY framing. Two of the three is not the defect. Scoped to figure +
#: subject alone it fired on "fire main water (typically 5-7 bar)", which is a
#: HydroPen operating pressure and correct; scoped to figure + modal alone it
#: fired on the weathertightness hose test, a different quantity with no held
#: source and already declared as K-ITEM-HOSE-TEST-PRESSURE. The forbidden
#: proposition is a bar figure presented as a REQUIRED hydrant pressure.
_MODAL = r"minimum|required|mandatory|must|at least|no less than"
BAR_MINIMUM = re.compile(
    r"(?:(?:%s)[^.]{0,80}?[\d.]+\s*bar\b[^.]{0,80}?(?:hydrant|fire\s*main)"
    r"|(?:%s)[^.]{0,80}?(?:hydrant|fire\s*main)[^.]{0,80}?[\d.]+\s*bar\b"
    r"|[\d.]+\s*bar\b[^.]{0,40}?(?:%s)[^.]{0,80}?(?:hydrant|fire\s*main))"
    % (_MODAL, _MODAL, _MODAL), re.I)

#: Two or more consecutive markdown bullets. A LONE starred line is a footnote.
ORPHAN_RUN = re.compile(r"(?m)^\*\s+\S[^\n]*\n\*\s+\S")

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-56s %s" % ("PASS" if ok else "FAIL", check, detail))


def flat(raw: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", raw)))


def without_provenance(text: str) -> str:
    """Version stamps and correction links quote what they removed."""
    text = re.sub(r'<span class="q-version">.*?</span>', " ", text, flags=re.S)
    text = re.sub(r'<span class="correction-link">.*?</span>', " ", text,
                  flags=re.S)
    return text


BANNER_RX = re.compile(r'<div class="notes-callout"[^>]*>.*?</div>', re.S)


def topic_span(text: str, topic_id: str):
    """(start, end) of a notes topic block, by STRUCTURAL ID.

    Never by a text needle. "First occurrence of the anchor in the file" is
    exactly what put the currentness banner four topics away from the material
    it warns about, in a topic that never mentions BMP5.
    """
    i = text.find('<div class="topic-block" id="%s"' % topic_id)
    if i < 0:
        return None
    depth, j, n = 0, i, len(text)
    while j < n:
        if text.startswith("<div", j):
            depth += 1
            j += 4
            continue
        if text.startswith("</div>", j):
            depth -= 1
            j += 6
            if depth == 0:
                break
            continue
        j += 1
    return (i, j)


def card_block(text: str, anchor: str) -> str:
    i = text.find('<div class="q-card" id="%s"' % anchor)
    assert i >= 0, anchor
    return text[i:_balanced_end(text, i)]


def teaching_text(path) -> str:
    """A file's candidate-facing text, provenance and currentness notes out.

    A currentness note NAMES the superseded publication in order to deny it -
    the fix, not the defect - so a negative sweep that reads it reports the
    correction as the problem.
    """
    t = without_provenance(read_text(path))
    t = re.sub(r'<div class="notes-callout".*?</div>', " ", t, flags=re.S)
    t = re.sub(r'<div class="practice-block"><strong>Currentness note.*?</div>',
               " ", t, flags=re.S)
    return t


def main() -> int:
    man = json.loads(read_text(MANIFEST))
    report("manifest_is_this_correction",
           man.get("correction_id") == CORRECTION_ID, man.get("correction_id"))
    report("status_authorised", man.get("status") == "AUTHORISED",
           man.get("status"))

    # ================= P0-A : the escaped figure, ANY capitalisation ======
    q2 = card_block(read_text(QB_ROOT / "QB2_H.html"), "q2")
    teach = flat(without_provenance(q2))
    report("P0A_no_bar_figure_survives_as_a_hydrant_minimum",
           not BAR_MINIMUM.search(teach),
           "case-insensitive: '4.0 bar', '4.0 Bar' and '4.0 BAR' all fail")
    report("P0A_key_numbers_layer_carries_the_governing_limbs",
           UPPER in teach and LOWER in teach and "II-2/10.2.1.6" in teach,
           "both cargo-ship limbs and the provision are on the card")
    report("P0A_card_no_longer_contradicts_its_own_stamp",
           "4.0" not in re.sub(r"\s+", " ", teach),
           "the figure the stamp calls 'not a SOLAS figure' is gone from the "
           "teaching layers")
    report("P0A_provenance_still_records_what_was_removed",
           "4.0 bar" in read_text(QB_ROOT / "QB2_H.html").lower(),
           "the version stamp still quotes the figure - history preserved")

    # ================= corpus-wide, RECURSIVE ==============================
    files = corpus_files()
    top = list(QB_ROOT.glob("*.html"))  # scope-control: comparison only
    report("gate_reads_the_recursive_corpus", len(files) > len(top),
           "%d files (top-level glob sees %d)" % (len(files), len(top)))

    bar_sites, bmp_sites, orphan_sites, single_limb = [], [], [], []
    for p in files:
        fam = surface_family(p)
        # `pastpapers` stays out: a sitting is anchored in time and the
        # examiner's wording is CORRECT as written.
        #
        # `generated` is now IN. It was skipped because a generated index
        # loses the `q-text` class that marks an examiner's words, so every
        # stem echo read as the site's own teaching. That was a detector gap,
        # not a reason to stop looking - and skipping the surface meant a
        # topic label the generator authors ITSELF was never examined either.
        # The detector now decides item by item from provenance, so the whole
        # surface can be swept.
        if fam == "pastpapers":
            continue
        t = teaching_text(p)
        if BAR_MINIMUM.search(flat(t)):
            bar_sites.append(rel_of(p))
        # SEMANTIC, unit-normalised, shape-general. The previous versions of
        # these two checks were defeated by a unit (`0.27 MPa` vs the literal
        # `0.27 N/mm`), by an element type (`<div>` vs `<li>/<p>`) and by an
        # HTML class name (`reg-code` only). Both now resolve through
        # `oral_currentness`, which normalises MPa / N/mm2 / bar / kPa to one
        # scale and takes the smallest enclosing element of ANY candidate-facing
        # tag that actually states a claim.
        raw = read_text(p)
        for h in firemain_scope_defects(raw):
            single_limb.append("%s:%s :: missing %s :: %s"
                               % (rel_of(p), h["line"], h["missing"],
                                  h["text"][:60]))
        for h in bmp5_current_teaching(raw):
            bmp_sites.append("%s:%s :: %s" % (rel_of(p), h["line"],
                                              h["text"][:60]))
        if fam in ("qcard", "cheatsheet", "oralnotes"):
            if ORPHAN_RUN.search(t):
                orphan_sites.append(rel_of(p))

    report("no_bar_hydrant_minimum_anywhere_in_the_corpus", not bar_sites,
           str(bar_sites or "none"))
    report("no_incomplete_scope_firemain_claim_anywhere", not single_limb,
           str(single_limb or "none"))
    report("no_surface_teaches_BMP5_as_current", not bmp_sites,
           str(bmp_sites or "none"))
    report("no_orphaned_markdown_bullet_run_anywhere", not orphan_sites,
           str(orphan_sites or "none"))

    # ================= unit equivalence, for DETECTION only ===============
    # A detector-normalisation rule, never an editorial one: a card may print
    # MPa or N/mm2 as it likes, and the guard must not care which.
    equivalences = [(("0.27", "MPa"), ("0.27", "N/mm2"), ("2.7", "bar"),
                     ("270", "kPa"), 0.27),
                    (("0.25", "MPa"), ("0.25", "N/mm2"), ("2.5", "bar"),
                     ("250", "kPa"), 0.25)]
    ok = all(all(to_mpa(v, u) == expect for v, u in forms)
             for *forms, expect in equivalences)
    report("pressure_units_normalise_to_one_scale", ok,
           "0.27 MPa = 0.27 N/mm2 = 2.7 bar = 270 kPa; 0.25 likewise")
    # A REAL detection-only invariant. The previous version asserted
    # `"0.27 MPa" in QB2_F.html` - which was ALSO true before the correction,
    # so it passed on a complete revert and proved nothing about the policy it
    # named. What "detection only" actually means is: the detector is pure, and
    # a card may print either unit without the guard's verdict changing.
    probe_mpa = ("<li>Minimum at the hydrants, both required pumps: "
                 "0.27 MPa at 6,000 GT and upwards, 0.25 MPa below.</li>")
    probe_nmm = probe_mpa.replace("MPa", "N/mm&sup2;")
    probe_bar = ("<li>Minimum at the hydrants, both required pumps: "
                 "2.7 bar at 6,000 GT and upwards, 2.5 bar below.</li>")
    before = (probe_mpa, probe_nmm, probe_bar)
    verdicts = [bool(firemain_scope_defects(x)) for x in before]
    single = "<li>Minimum required hydrant pressure 0.27 MPa</li>"
    single_nmm = "<li>Minimum required hydrant pressure 0.27 N/mm&sup2;</li>"
    report("detector_verdict_is_unit_independent",
           verdicts == [False, False, False]
           and bool(firemain_scope_defects(single))
           and bool(firemain_scope_defects(single_nmm)),
           "the same claim gets the same verdict in MPa, N/mm2 and bar")
    report("detector_rewrites_no_product_text",
           (probe_mpa, probe_nmm, probe_bar) == before,
           "pure function - detection never edits")
    report("no_product_unit_change_was_required",
           "0.27 MPa" in read_text(QB_ROOT / "QB2_F.html")
           and "0.27 N/mm" in read_text(QB_ROOT / "QB2_B.html"),
           "QB2_F keeps MPa and QB2_B keeps N/mm2 - both pass the same guard")

    # ================= D5 / D9 : exemptions must be bounded ===============
    unrelated = ('<div class="q-card"><p>Currentness note: MSC.535(107) has '
                 'been superseded for lifeboat ventilation.</p>'
                 '<p>Harden the vessel as per BMP5.</p></div>')
    report("currentness_exemption_is_subject_specific",
           bool(bmp5_current_teaching(unrelated)),
           "a note about another instrument grants no immunity to a BMP5 claim")
    stem_near = ('<div><h2 class="topic-title">Security</h2></div>'
                 '<div><p>BMP5 is the current industry guidance.</p></div>')
    report("stem_exemption_does_not_leak_into_neighbouring_teaching",
           bool(bmp5_current_teaching(stem_near)),
           "a nearby heading no longer excuses a live claim - the old +/-220 "
           "character window swallowed teaching text")

    # ================= P1-B : the banner is TOPIC-LOCAL ===================
    p10 = QB_ROOT / "oralnotes/miw-notes-mgmt-p10.html"
    t10 = read_text(p10)
    tspan = topic_span(t10, "topic-46")
    banners = [m for m in BANNER_RX.finditer(t10)]
    in_topic = [m for m in banners
                if tspan and tspan[0] <= m.start() < tspan[1]]
    report("banner_exists_exactly_once_in_the_intended_topic",
           len(in_topic) == 1, "topic-46 carries %d banner(s)" % len(in_topic))
    report("banner_exists_in_no_other_topic",
           len(banners) == len(in_topic),
           "%d banner(s) outside topic-46" % (len(banners) - len(in_topic)))
    report("intended_topic_is_the_BMP_topic",
           tspan is not None
           and "BMP5 Counter-Piracy Architecture" in t10[tspan[0]:tspan[1]],
           "topic-46 is the SUA/BMP5 topic, located by structural id")
    # SAME TOPIC **and** the direction word agrees with the actual order. The
    # previous version tested for the literal phrase "…note above", so it was
    # green while the banner rendered BELOW that sentence - a check that names
    # locality and is structurally incapable of seeing the one thing about
    # locality that was wrong.
    xref = re.search(r"see the currentness note (above|below)",
                     t10[tspan[0]:tspan[1]] if tspan else "")
    direction_ok = False
    if tspan and xref and in_topic:
        xpos = tspan[0] + xref.start()
        bpos = in_topic[0].start()
        direction_ok = ((xref.group(1) == "below" and bpos > xpos)
                        or (xref.group(1) == "above" and bpos < xpos))
    report("the_note_that_refers_to_the_banner_is_in_the_same_topic",
           tspan is not None and xref is not None and direction_ok,
           "cross-reference and banner in one block, and '%s' matches the "
           "rendered order" % (xref.group(1) if xref else "-"))

    # ================= the newly-visible surface, repaired =================
    p10 = QB_ROOT / "oralnotes/miw-notes-mgmt-p10.html"
    t10 = read_text(p10)
    report("oralnotes_topic_carries_a_currentness_note",
           "Currentness note (6 Sep 2026)" in t10 and CURRENT in t10,
           "the SUA/BMP topic now says BMP5 is superseded")
    report("oralnotes_false_2024_date_is_gone",
           not re.search(r'2024</span>\s*BMP5 supersedes', t10),
           "the timeline no longer dates BMP5 to 2024")
    report("no_replacement_publication_year_was_invented",
           "BMP5 (2018)" not in t10 and "BMP5 2018" not in t10,
           "no BMP5 publication year is asserted - none is held")
    report("oralnotes_timeline_carries_the_HELD_supersession_fact",
           "2025</span>" in t10 and "BMP Maritime Security replaces" in t10,
           "SRC-BMPMS-2025 is what the row now says")

    # ================= surface policy, asserted positively ================
    pp = [p for p in files if surface_family(p) == "pastpapers"]
    out = subprocess.run(["git", "diff", "--name-only",
                          man["baseline_commit"], "HEAD", "--",
                          "meoclass1/pastpapers"],
                         cwd=str(REPO), capture_output=True)
    # "No past-paper file changed at all" was the right check while no past
    # paper had been corrected. QP2506 q2 has since been corrected under
    # CORR-D01-NETZERO-CURRENTNESS-20260907 - a source-map clause that made a
    # claim about the FUTURE of the sitting, not about the sitting - so the
    # blanket form now fails on an authorised and correct edit.
    #
    # What this check actually protects is the EXAMINER'S WORDING. That is
    # what "sitting-anchored" means, and it is what must never be modernised.
    # So the check now asserts the property instead of the proxy: any changed
    # past paper must be declared in an authorised correction record, and no
    # question stem may differ from its baseline.
    changed = [x for x in out.stdout.decode("utf-8", "replace").split()
               if x.strip()]
    declared = set()
    for man_path in sorted(HERE.glob("correction_*_manifest.json")):
        try:
            m2 = json.loads(read_text(man_path))
        except Exception:                                   # noqa: BLE001
            continue
        for c in m2.get("cards", []):
            declared.add(c.get("path"))
    # A correction whose target the CARD schema cannot digest is recorded in a
    # governance document instead, so that document is a declaration too.
    for doc in sorted((REPO / "meoclass1/oral-intelligence/examiner-audit")
                      .glob("*NON_CARD*.md")):
        declared.update(re.findall(r"meoclass1/[\w/.-]+\.html", read_text(doc)))
    undeclared = [x for x in changed if x not in declared]

    stems_moved = []
    for rel in changed:
        was = subprocess.run(["git", "show", "%s:%s"
                              % (man["baseline_commit"], rel)],
                             cwd=str(REPO), capture_output=True)
        if was.returncode != 0:
            continue
        before = was.stdout.decode("utf-8", "replace")
        now = read_text(REPO / rel)
        rx = re.compile(r'<div class="(?:q-text|q-txt|cs-qtitle|exam-q|qa-q)"'
                        r'[^>]*>(.*?)</div>', re.S)
        if sorted(rx.findall(before)) != sorted(rx.findall(now)):
            stems_moved.append(rel)

    report("past_papers_were_not_modernised",
           out.returncode == 0 and not undeclared and not stems_moved,
           "%d sitting-anchored files; %d changed; undeclared: %s; "
           "examiner stems moved in: %s"
           % (len(pp), len(changed), undeclared or "none",
              stems_moved or "none"))
    report("record_states_the_surface_policy",
           "sitting-anchored" in man["propagation"]["surface_policy"],
           "policy is in the record, not only in the code")
    # All THREE numbers asserted. The previous version checked 128 and 224 and
    # printed the 96 without testing it, so a record claiming
    # `files_previously_invisible: 1` would still have passed - the number that
    # measures the defect was the one nothing read.
    report("record_declares_the_scope_numbers",
           man["invariants"]["corpus_files_enumerated_pass1"] == 128
           and man["invariants"]["corpus_files_enumerated_now"] == len(files)
           and man["invariants"]["files_previously_invisible"]
           == len(files) - 128,
           "128 -> %d, %d previously invisible"
           % (len(files), man["invariants"]["files_previously_invisible"]))
    report("record_does_not_rewrite_pass1_history",
           "NOT rewritten" in man["supersedes_summary"]["note"]
           and len(man["supersedes_summary"]["corrected_claims"]) == 2,
           "the superseded claims are stated, the originals left standing")
    report("false_positive_is_recorded",
           "footnote" in man["propagation"]["false_positive_recorded"],
           "the miw-notes-mgmt-p6 footnote is declared, not deleted")

    # ================= digests, through the resolver =======================
    bad = []
    for c in man["cards"]:
        d = card_digests(read_text(QB_ROOT / c["file"]))
        res = resolve_authorised_card_state(
            manifest=MANIFEST.name, action_id=c["correction_action_id"],
            file=c["file"], anchor=c["anchor"],
            pinned_post_digest=c["post_edit_digest"],
            live_digest=d.get(c["anchor"]))
        if not res.ok:
            bad.append("%s#%s:%s" % (c["file"], c["anchor"], res.status))
    report("every_pinned_state_is_live_or_a_proven_ancestor", not bad,
           "%d card(s), problems: %s" % (len(man["cards"]), bad or "none"))

    idx = json.loads(read_text(INDEX))
    report("canonical_questions_unchanged",
           idx["total_questions"] == man["invariants"]["canonical_questions_after"],
           str(idx["total_questions"]))
    report("question_bearing_files_unchanged",
           idx["total_files"] == man["invariants"]["question_bearing_files"],
           str(idx["total_files"]))

    # ================= governance ==========================================
    report("declared_artefacts_exist",
           all((REPO / a["path"]).is_file() for a in man["artefacts"]),
           "%d artefact(s)" % len(man["artefacts"]))
    traps = read_text(TRAPS)
    for n, needles in ((96, ("case-insensitive", "not a fix",
                             "moves the same hole to")),
                       (97, ("invisible from inside its own scope",
                             "plants a file in a nested directory",
                             "not a licence to sweep")),
                       (98, ("body that is never read",
                             "computed and discarded", "literal `True`"))):
        m = re.search(r"### %d\..*?(?=\n### |\Z)" % n, traps, re.S)
        body = m.group(0) if m else ""
        report("known_traps_entry_%d_carries_the_lesson" % n,
               bool(body) and all(x in body for x in needles), "entry %d" % n)

    # ================= the CLOSURE record, and the chain ==================
    close_path = HERE / "correction_corr_p1close_20260906_manifest.json"
    close = json.loads(read_text(close_path))
    report("closure_record_exists_and_is_authorised",
           close.get("correction_id") == "CORR-P1CLOSE-20260906"
           and close.get("status") == "AUTHORISED",
           close.get("correction_id"))
    bad = []
    for c in close["cards"]:
        d = card_digests(read_text(QB_ROOT / c["file"]))
        res = resolve_authorised_card_state(
            manifest=close_path.name, action_id=c["correction_action_id"],
            file=c["file"], anchor=c["anchor"],
            pinned_post_digest=c["post_edit_digest"],
            live_digest=d.get(c["anchor"]))
        if not res.ok:
            bad.append("%s#%s:%s" % (c["file"], c["anchor"], res.status))
    report("closure_pins_are_live_or_proven_ancestors", not bad,
           "%d card(s), problems: %s" % (len(close["cards"]), bad or "none"))
    # The chain has to be THREE links, and each link must still hold its own
    # claim. A repair that quietly rebaselined its predecessor would look
    # identical from the outside except for this.
    # Asserted against the OBJECT STORE, not against the record's own prose.
    # "the earlier records are not rewritten" is a claim about bytes, and a
    # sentence saying so is not evidence of it - the first version of this
    # check tested for a phrase, which is exactly the class of check this whole
    # chain exists to stop shipping.
    earlier = subprocess.run(
        ["git", "diff", "--name-only", "d07591c", "HEAD", "--",
         "tools/oral/correction_corr_t5_ddcascade_20260906_manifest.json",
         "tools/oral/correction_corr_t5_reach_20260906_manifest.json",
         "tools/oral/correction_corr_t5_hydrant_20260906_manifest.json"],
        cwd=str(REPO), capture_output=True)
    repair_rec = subprocess.run(
        ["git", "diff", "--name-only", "43597e3", "HEAD", "--",
         "tools/oral/correction_corr_p1repair_20260906_manifest.json"],
        cwd=str(REPO), capture_output=True)
    report("the_three_link_chain_is_intact",
           len(close["supersedes_summary"]["corrected_claims"]) == 3
           and earlier.returncode == 0 and not earlier.stdout.strip()
           and repair_rec.returncode == 0 and not repair_rec.stdout.strip(),
           "Pass 1 -> Pass-1 repair -> Pass-1 closure; the three Pass-1 "
           "records are byte-unchanged since d07591c and the repair record "
           "since 43597e3")
    report("closure_declares_zero_remaining_defects",
           close["invariants"]["firemain_scope_defects_remaining"] == 0
           and close["invariants"]["bmp5_taught_as_current_remaining"] == 0
           and close["invariants"][
               "currentness_banners_outside_intended_topic"] == 0,
           "DECLARED FIGURES ONLY - this check reads the record's own JSON. "
           "The corpus-derived versions are the three checks above it, which "
           "are separate; the justification previously printed here claimed "
           "otherwise and was false.")
    report("closure_artefacts_exist",
           all((REPO / a["path"]).is_file() for a in close["artefacts"]),
           "%d artefact(s)" % len(close["artefacts"]))
    m99 = re.search(r"### 99\..*?(?=\n### |\Z)", read_text(TRAPS), re.S)
    m100 = re.search(r"### 100\..*?(?=\n### |\Z)", read_text(TRAPS), re.S)
    report("known_traps_entry_99_carries_the_lesson",
           bool(m99) and all(x in m99.group(0) for x in
                             ("Detect the **proposition**", "depth counter is not a stack",
                              "DETECTOR rule")),
           "entry 99")
    report("known_traps_entry_100_carries_the_lesson",
           bool(m100) and all(x in m100.group(0) for x in
                              ("structural identity", "third wrong-occurrence",
                               "governs its container")),
           "entry 100")

    # ================= the guard-closure record ===========================
    # It is a governance DOCUMENT, not a correction manifest, because it
    # corrects no card - the schema refusing a card-less correction is the
    # schema working, and manufacturing a card to satisfy it would produce the
    # decorative record that schema exists to forbid.
    guard = REPO / ("meoclass1/oral-intelligence/examiner-audit/"
                    "PASS1_GUARD_CLOSURE.md")
    gtext = read_text(guard) if guard.is_file() else ""
    report("guard_closure_record_exists", bool(gtext), guard.name)
    report("guard_record_states_the_four_link_chain",
           all(x in gtext for x in ("CORR-P1REPAIR-20260906",
                                    "CORR-P1CLOSE-20260906",
                                    "P1GUARD-20260906"))
           and "Nothing earlier is rewritten" in gtext,
           "Pass 1 -> repair -> closure -> guard, none rewritten")
    report("guard_record_states_zero_product_change",
           "Product bytes changed: ZERO" in gtext,
           "content was clean before this pass and was not reopened")
    # This check previously accepted the words "Residual limits" and "P3 debt".
    # It passed while the record graded four P1 guard escapes as P3 - a gate
    # that reads its record's headings can be satisfied by a wrong grading as
    # easily as a right one. It now demands the escapes themselves, by name,
    # and demands that the record does NOT claim closure while they are open.
    escapes = ("Known escapes", "and` / `or` / `so`", "BMP-5",
               "no modal word", "sibling block")
    report("guard_record_names_its_open_escapes",
           all(x in gtext for x in escapes)
           and "Pass 1 is NOT closed on this record" in gtext,
           "four confirmed escapes named; closure not claimed over them")
    report("guard_record_withdraws_the_wrong_P3_grading",
           "That grading was wrong and is withdrawn" in gtext,
           "an escape that keeps the gate green while the defect is live is P1")
    m101 = re.search(r"### 101\..*?(?=\n### |\Z)", read_text(TRAPS), re.S)
    report("known_traps_entry_101_carries_the_lesson",
           bool(m101) and all(x in m101.group(0) for x in
                              ("enumerating renderings never converges",
                               "open set", "EXCLUSION",
                               "schema refusing your record")),
           "entry 101")

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: " + ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
