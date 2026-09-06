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
        if fam in ("generated", "pastpapers"):
            continue
        t = teaching_text(p)
        if BAR_MINIMUM.search(flat(t)):
            bar_sites.append(rel_of(p))
        # A two-limb rule stated with ONE limb is not vague, it is wrong for
        # every ship on the other side of the threshold. The bar check above
        # cannot see this: 0.27 N/mm2 is the CORRECT figure, and the defect is
        # the absence of its partner. Element-scoped, so a 0.25 elsewhere on
        # the page cannot rescue a single-limb bullet.
        for el in re.finditer(r"<li>.*?</li>|<p>.*?</p>", t, re.S):
            txt = flat(el.group(0))
            if "0.27 N/mm" not in txt:
                continue
            if not re.search(r"hydrant|fire\s*main", txt, re.I):
                continue
            if "0.25 N/mm" not in txt or "6,000 GT" not in txt:
                single_limb.append("%s :: %s" % (rel_of(p), txt[:70]))
        if fam in ("qcard", "cheatsheet", "oralnotes"):
            if ORPHAN_RUN.search(t):
                orphan_sites.append(rel_of(p))
        # BMP5 taught in a reg-code SLOT is the shape corrected as A-6/A-7.
        for m in re.finditer(r'<span class="reg-code">([^<]*)</span>', t):
            code = m.group(1)
            # A slot that labels itself superseded is the QB4_H#q11 predecessor
            # record, kept on purpose because examiners still ask for BMP5 by
            # name. The defect is a slot that offers BMP5 as CURRENT.
            if re.search(r"BMP\s?5\b", code) and "supersed" not in code.lower():
                bmp_sites.append("%s :: %s" % (rel_of(p), code[:40]))

    report("no_bar_hydrant_minimum_anywhere_in_the_corpus", not bar_sites,
           str(bar_sites or "none"))
    report("no_single_limb_hydrant_figure_anywhere", not single_limb,
           str(single_limb or "none"))
    report("no_reg_code_slot_names_BMP5_as_current", not bmp_sites,
           str(bmp_sites or "none"))
    report("no_orphaned_markdown_bullet_run_anywhere", not orphan_sites,
           str(orphan_sites or "none"))

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
    report("past_papers_were_not_modernised",
           out.returncode == 0 and not out.stdout.strip(),
           "%d sitting-anchored files, 0 changed since %s"
           % (len(pp), man["baseline_commit"]))
    report("record_states_the_surface_policy",
           "sitting-anchored" in man["propagation"]["surface_policy"],
           "policy is in the record, not only in the code")
    report("record_declares_the_scope_numbers",
           man["invariants"]["corpus_files_enumerated_pass1"] == 128
           and man["invariants"]["corpus_files_enumerated_now"] == len(files),
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

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: " + ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
