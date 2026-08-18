"""Phase 2A-ii Oral Notes controls.

Load-bearing assertions for the secondary Notes layer. Each pins a behaviour
that was observed to be wrong while building this phase, or that the Laptop's
Phase-2 review at c78a228 identified as the reason the Notes were excluded.

The four things these controls exist to prevent:

    a page rescuing an ask its sections do not answer
    a note unit becoming a canonical QB question
    a note cue becoming tracker evidence
    "John" the legal example, the ship and the author becoming John the examiner

Imported by test_oral_controls.py so one gate owns every control and the
mutation harness exercises them. Runnable on its own:

  PYTHONIOENCODING=utf-8 python tools/oral/test_notes_controls.py

Portability: repo-relative, no drive letters, no external inputs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L          # noqa: E402
import oral_text as T         # noqa: E402
import oral_provenance as P   # noqa: E402
import oral_notes as N        # noqa: E402
import notes_coverage as C    # noqa: E402

FAILURES = []
CHECKS = [0]


def ok(name, condition, detail=""):
    CHECKS[0] += 1
    if not condition:
        FAILURES.append("%s %s" % (name, ("- " + detail) if detail else ""))


# --------------------------------------------------------------------------
# fixtures, built once
# --------------------------------------------------------------------------
FILES = N.classify_files()
UNITS = N.build_units()
IDX = C.unit_index(UNITS)
IDF, DEFAULT = C.idf_over_units(IDX)
ALIAS = json.loads((L.OUT / "EXAMINER_ALIAS_REGISTER.json").read_text(
    encoding="utf-8"))
ALIAS_MAP = N.examiner_aliases(ALIAS)
BY_ID = {u["note_unit_id"]: u for u in UNITS}

GIRDING_UNIT = "NOTE-SIMON-P2-N9-NO-009-TUG-GIRDING-CAPSIZING-RISK"


def support_for(ask, unit_id=None):
    """Best Notes support for an ask, or its support against one named unit."""
    toks = C.source_tokens({"question_core_text": ask})
    if unit_id is None:
        hits = C.best_support(toks, IDX, IDF, DEFAULT)
        return (hits[0]["notes_support"] if hits else C.NO_SUPPORT), hits
    entry = IDX[unit_id]
    body, title, conflict, missing = C.score(toks, entry, IDF, DEFAULT)
    about_whole = all(C.satisfied(t, entry["about_tokens"]) for t in toks)
    tier, _ = C.classify_support(body, title, len(toks), conflict,
                                 entry["unit"]["answer_bearing"],
                                 bool(missing), about_whole)
    return tier, {"body": body, "about": title, "conflict": conflict,
                  "missing": missing}


def cue_for(text, name, in_tip=False, in_heading=False):
    i = text.index(name)
    return N.classify_cue(text, i, i + len(name), name, in_tip, in_heading)


RANK = C.SUPPORT_RANK


# ==========================================================================
# 1. Inventory integrity
#
# The coverage universe must be a stated set, not whatever globbing returns.
# ==========================================================================
roles = {r["file"]: r["role"] for r in FILES}
ok("every notes page is classified",
   all(r["role"] != N.ROLE_UNCLASSIFIED for r in FILES),
   str([r["file"] for r in FILES if r["role"] == N.ROLE_UNCLASSIFIED]))

for nav in N.NAVIGATION_PAGES:
    ok("navigation page %s is excluded from the semantic universe" % nav,
       roles.get(nav) == N.ROLE_NAVIGATION)
    ok("navigation page %s contributes no note unit" % nav,
       not any(u["file"] == nav for u in UNITS))

for oos in N.OUT_OF_SCOPE_PAGES:
    ok("written-exam page %s is out of scope" % oos,
       roles.get(oos) == N.ROLE_OUT_OF_SCOPE)
    ok("written-exam page %s contributes no note unit" % oos,
       not any(u["file"] == oos for u in UNITS))

ok("the substantive set is non-trivial",
   sum(1 for r in FILES if r["role"] == N.ROLE_SUBSTANTIVE) >= 30)
ok("every substantive page yields at least one unit",
   all(any(u["file"] == r["file"] for u in UNITS)
       for r in FILES if r["role"] == N.ROLE_SUBSTANTIVE),
   str([r["file"] for r in FILES if r["role"] == N.ROLE_SUBSTANTIVE
        and not any(u["file"] == r["file"] for u in UNITS)]))

# ==========================================================================
# 2. Unit identity - a note is never a canonical question
# ==========================================================================
ids = [u["note_unit_id"] for u in UNITS]
ok("no duplicate note unit ids", len(ids) == len(set(ids)),
   str([i for i in ids if ids.count(i) > 1][:3]))
ok("no note unit id is shaped like a canonical QB question id",
   not [i for i in ids if N.is_canonical_shaped(i)],
   str([i for i in ids if N.is_canonical_shaped(i)][:3]))
ok("every note unit id carries the NOTE- prefix",
   all(i.startswith(N.NOTE_ID_PREFIX) for i in ids))

canonical = {q["canonical_question_id"] for q in L.build_inventory()}
# Was `len(canonical) == 681`. A frozen corpus size is not a Notes-layer
# control: the collision check below is. The literal fired on the legitimate
# 682nd question (QB1_K#q8). Assert no recorded question was lost instead --
# that is the property live relationships actually depend on.
_recorded = {q["canonical_question_id"] for q in json.loads(
    (L.OUT / "CURRENT_ORAL_QB_INVENTORY.json").read_text(encoding="utf-8"))}
ok("no canonical question recorded by the audit has vanished",
   not (_recorded - canonical), str(sorted(_recorded - canonical)[:5]))
ok("no note unit id collides with a canonical question id",
   not (set(ids) & canonical))
ok("every note unit resolves to a real file",
   all((N.NOTES_DIR / u["file"]).exists() for u in UNITS))
ok("every note unit level is in the closed vocabulary",
   not ({u["unit_level"] for u in UNITS} - N.UNIT_LEVELS))
ok("every child unit names an existing parent",
   all(u["parent_unit_id"] in BY_ID for u in UNITS if u["parent_unit_id"]))

# ==========================================================================
# 3. Site chrome never becomes content
# ==========================================================================
blob = " ".join(u["text"] for u in UNITS)
for junk in ("gtag(", "dataLayer", "miw_auth", "function(", "addEventListener",
             "<script", "localStorage"):
    ok("chrome fragment %r never reaches unit text" % junk, junk not in blob)

# ==========================================================================
# 4. Section-level, not page-level
#
# The Laptop's decisive finding: GAP-0002 GIRDING is answered by a dedicated
# note section. The unit must be that section, not the 116 KB page holding it.
# ==========================================================================
ok("the Tug Girding section is a retrievable unit", GIRDING_UNIT in BY_ID)
if GIRDING_UNIT in BY_ID:
    g = BY_ID[GIRDING_UNIT]
    ok("the girding unit is a section, not a page",
       g["text_chars"] < 4000, "%d chars" % g["text_chars"])
    ok("the girding unit resolves to its own anchor",
       g["url"] == "/meoclass1/oralnotes/simon-notes-p2.html#n9", g["url"])
    ok("the girding unit is titled for the ask",
       "girding" in g["section_title"].lower())
    page_chars = len((N.NOTES_DIR / "simon-notes-p2.html").read_text(
        encoding="utf-8", errors="replace"))
    ok("the girding unit is a small fraction of its page",
       g["text_chars"] * 10 < page_chars,
       "%d of %d" % (g["text_chars"], page_chars))

# ==========================================================================
# 5. The load-bearing Notes fixtures
#
# M14 deletes the Notes coverage layer; these are what must break when it does.
# ==========================================================================
tier, hits = support_for('What is "GIRDING"?')
ok("GIRDING reaches complete Notes support", tier == C.COMPLETE_SUPPORT, tier)
ok("GIRDING support is traced to the Tug Girding section",
   bool(hits) and hits[0]["note_unit_id"] == GIRDING_UNIT,
   str(hits[:1]))
ok("GIRDING support names its file and anchor",
   bool(hits) and hits[0]["file"] == "simon-notes-p2.html"
   and hits[0]["anchor"] == "n9")

tier, _ = support_for("Hong Kong convention: requirements and certificate")
ok("the Hong Kong Convention ask reaches strong or better Notes support",
   RANK[tier] >= RANK[C.STRONG_SUPPORT], tier)

# Positive fixtures spanning the syllabus. Each is a real source occurrence
# whose Notes support was verified against the actual section.
POSITIVE = [
    ("BWTS USCG and IMO, AMS", C.STRONG_SUPPORT, "environment / BWM"),
    ("CO2 bottle filling rate", C.STRONG_SUPPORT, "fire and safety"),
    ("How do you calculate weight inclining experiment?", C.STRONG_SUPPORT,
     "stability"),
    ("Diff between EU MRV IMO DCS", C.STRONG_SUPPORT, "MARPOL / reporting"),
    ("Interim certificate. DOC SMC. Why interim?", C.STRONG_SUPPORT,
     "management / ISM"),
    ("Regulation for issuance of IAPP certificate", C.STRONG_SUPPORT,
     "survey and certification"),
    ("No more favourable treatment", C.STRONG_SUPPORT, "legal"),
    ("AFS latest paints", C.STRONG_SUPPORT, "engine / hull technology"),
]
for ask, floor, area in POSITIVE:
    tier, _ = support_for(ask)
    ok("Notes support holds for %s: %r" % (area, ask[:44]),
       RANK[tier] >= RANK[floor], tier)

# ==========================================================================
# 6. Over-rescue negative controls
#
# A broad note that mentions a topic must not rescue a specific ask. Each
# control names a real unit and asserts a CEILING, not a floor.
# ==========================================================================
def unit_titled(fragment, level=None):
    for u in sorted(UNITS, key=lambda u: u["note_unit_id"]):
        if fragment.lower() in u["section_title"].lower():
            if level is None or u["unit_level"] == level:
                return u["note_unit_id"]
    return None


NEGATIVE = [
    # a generic instrument topic is not a specific numeric criterion
    ("What is the 15 ppm bilge discharge limit and the 30 litres per nautical "
     "mile instantaneous rate?", "MARPOL", C.PARTIAL_SUPPORT,
     "generic MARPOL topic vs a specific numeric criterion"),
    # a generic management topic is not a specific certification procedure
    ("What is the exact interval and extension procedure for the intermediate "
     "ISM audit of the SMC?", "GESAMP", C.TOPIC_SUPPORT,
     "unrelated management topic vs a specific audit procedure"),
]
for ask, title_fragment, ceiling, why in NEGATIVE:
    uid = unit_titled(title_fragment)
    ok("negative fixture unit exists: %s" % title_fragment, uid is not None)
    if uid:
        tier, detail = support_for(ask, uid)
        ok("over-rescue guard - %s" % why,
           RANK[tier] <= RANK[ceiling], "%s %s" % (tier, detail))

# A written-exam prompt states an ask; it never answers one.
exam_units = [u for u in UNITS if u["unit_level"] == N.LEVEL_EXAM_Q]
ok("written-exam prompts exist as units", bool(exam_units))
ok("no written-exam prompt unit is answer-bearing",
   all(not u["answer_bearing"] for u in exam_units))
if exam_units:
    e = sorted(exam_units, key=lambda u: u["note_unit_id"])[0]
    tier, _ = support_for(e["section_title"], e["note_unit_id"])
    ok("a written-exam prompt cannot exceed topic support even against itself",
       RANK[tier] <= RANK[C.TOPIC_SUPPORT], tier)

# A contradictory designator caps support however well the prose overlaps.
for a, b in (("D-1", "D-2"), ("ME-GI", "ME-GA"), ("Annex I", "Annex VI")):
    ok("designator conflict is detected: %s against %s" % (a, b),
       T.designator_conflict(T.mtokens(a), T.mtokens(b)))
    tier, _ = C.classify_support(1.0, 1.0, 5, True, True, False, True)
    ok("a designator conflict caps Notes support at topic (%s/%s)" % (a, b),
       tier == C.TOPIC_SUPPORT, tier)

# The Phase 2A-ii limitation, REPAIRED in Phase 2A-iii and pinned the right way
# round. `designator_conflict` is exercised in production on mixed-case
# SENTENCES, not on bare designators, and in a sentence the acronym pass also
# emits the bare family head `dsg:me` beside `dsg:me-gi`. That head was admitted
# as a member, so both sides carried the pseudo-value "me", it intersected, and
# the real GI/GA disagreement cancelled. A family named without a member now
# contributes no member, so the shared "ME" no longer erases the conflict.
# The full-sentence controls live in test_oral_controls.py section 3a.
_sentence_conflict = T.designator_conflict(
    T.mtokens("explain the ME-GI standard"),
    T.mtokens("explain the ME-GA standard"))
ok("the mixed-case sentence conflict fires: ME-GI is not ME-GA in prose",
   _sentence_conflict is True,
   "the Phase 2A-iii designator repair has regressed")
ok("no Oral Note text exercises the ME-GI / ME-GA family",
   not any(d in u["text"] for u in UNITS
           for d in ("ME-GI", "ME-GA", "ME-LGI")))

# A terse prompt is capped unless the unit is titled for it and answers it.
tier, _ = C.classify_support(1.0, 0.2, 1, False, True, False, False)
ok("a terse prompt inside a broad unit is capped at topic support",
   tier == C.TOPIC_SUPPORT, tier)
tier, _ = C.classify_support(1.0, 1.0, 1, False, True, False, True)
ok("a terse prompt whose unit is titled for it may reach complete support",
   tier == C.COMPLETE_SUPPORT, tier)
tier, _ = C.classify_support(1.0, 1.0, 1, False, False, False, True)
ok("a terse prompt against a non-answering unit stays capped",
   tier == C.TOPIC_SUPPORT, tier)

# A missing specific demand caps below strong.
tier, _ = C.classify_support(1.0, 1.0, 6, False, True, True, False)
ok("a missing designator or numeric demand caps below strong support",
   RANK[tier] <= RANK[C.PARTIAL_SUPPORT], tier)

# ==========================================================================
# 7. The Notes vocabulary is disjoint from the canonical one
# ==========================================================================
ok("no Notes support tier reuses a canonical disposition",
   not (set(C.SUPPORT_TIERS) & C.CANONICAL_DISPOSITIONS))
for t in C.SUPPORT_TIERS:
    ok("Notes tier %s is not a canonical disposition" % t,
       t not in C.CANONICAL_DISPOSITIONS)

# ==========================================================================
# 8. Examiner cue controls
#
# The false positives the Laptop named, plus the substring class this phase
# found: 53 of the literal "Nair" hits inside note units are "Nairobi".
# ==========================================================================
ok("Nairobi does not contain the examiner Nair",
   "Nair" not in [m for m in ALIAS_MAP
                  if __import__("re").search(r"\b%s\b" % m,
                                             "the Nairobi Convention 2007")],
   "word-boundary matching failed")

NON_EXAMINER = [
    ('the vessel is named as the defendant, "John Doe v. The Motor Vessel '
     'Olympic Prometheus"', "John", "legal case party"),
    ("PID tuning after John Ziegler and Nichols", "John", "author name"),
    ("the collision involving USS John S. McCain", "John", "ship name"),
    ("these notes were compiled by Paul Anderson", "Paul", "author attribution"),
]
for text, name, why in NON_EXAMINER:
    disp, control, _ = cue_for(text, name)
    ok("non-examiner control holds - %s" % why,
       disp == N.CUE_NON_EXAMINER, "%s / %s" % (disp, control))
    ok("non-examiner control names its rule - %s" % why, bool(control))

EXPLICIT = [
    ('Simon Sir typically asks "What is tug girding?" - define the mechanism',
     "Simon", N.CUE_PRIMARY_ASK, "structured tip with a bound ask"),
    ("Nair frequently tests whether candidates confuse the two eras",
     "Nair", N.CUE_PRIMARY_ASK, "bound ask verb in prose"),
    ("Paul favourite is to ask why a ship does not need three dockings",
     "Paul", N.CUE_PRIMARY_ASK, "bound ask noun"),
    ("Rajappan's standard escalation is to push on the next question",
     "Rajappan", N.CUE_FOLLOWUP, "follow-up marker"),
    ("Senthil expects a concrete example rather than the definition",
     "Senthil", N.CUE_EXPECTED_DETAIL, "expectation marker"),
]
for text, name, want, why in EXPLICIT:
    disp, control, _ = cue_for(text, name, in_tip=True)
    ok("explicit cue is recognised - %s" % why, disp == want,
       "%s (control %s)" % (disp, control))

# A structured examiner field is an explicit label; the capitalised word after
# it is a frequency badge, not a surname.
disp, control, _ = cue_for("Uday pp. 3 Examiner: Nair Medium Frequency",
                           "Nair")
ok("a structured Examiner: field is not suppressed as a longer proper name",
   disp == N.CUE_PRIMARY_ASK, "%s / %s" % (disp, control))

# Comparison is not litigation: this domain writes "vs" constantly.
disp, _, _ = cue_for("Bunker Convention 2001 vs. CLC 92 - Examiner: Nair",
                     "Nair")
ok("a maritime 'vs' comparison is not read as a legal case party",
   disp != N.CUE_NON_EXAMINER, disp)

# Without a bound ask, a name states no ask.
disp, _, _ = cue_for("this area is more likely from Nair or Srivastava given "
                     "the regulatory complexity", "Nair")
ok("a name with no bound ask is only a weak mention",
   disp == N.CUE_WEAK_MENTION, disp)

ok("weak and non-examiner dispositions are not evidence",
   not (N.EXPLICIT_CUES & {N.CUE_WEAK_MENTION, N.CUE_NON_EXAMINER,
                           N.CUE_HEADING_CONTEXT}))
ok("the cue disposition vocabulary is closed",
   N.EXPLICIT_CUES < N.CUE_DISPOSITIONS)

# ==========================================================================
# 9. Note evidence never becomes tracker evidence
# ==========================================================================
def rec(tier, source):
    return {"evidence_id": "NT-1", "evidence_tier": tier, "source_type": source}


ok("a note cue carries the NOTE_EXPLICIT tier",
   N.NOTE_EVIDENCE_TIER == "NOTE_EXPLICIT")
ok("a note cue's provenance is an oral note page",
   N.NOTE_SOURCE_TYPE == "ORAL_NOTE_PAGE")
ok("NOTE_EXPLICIT on note provenance is self-consistent",
   P.incompatible(rec(N.NOTE_EVIDENCE_TIER, N.NOTE_SOURCE_TYPE)) is None,
   str(P.incompatible(rec(N.NOTE_EVIDENCE_TIER, N.NOTE_SOURCE_TYPE))))
ok("a note cue cannot be relabelled PRIMARY_TRACKER",
   P.incompatible(rec("PRIMARY_TRACKER", N.NOTE_SOURCE_TYPE)) is not None)
ok("a note cue cannot be relabelled EXTERNAL_SURVEYOR_COMPILATION",
   P.incompatible(rec("EXTERNAL_SURVEYOR_COMPILATION",
                      N.NOTE_SOURCE_TYPE)) is not None)
ok("a note cue cannot be relabelled TOPIC_INFERRED",
   P.incompatible(rec("TOPIC_INFERRED", N.NOTE_SOURCE_TYPE)) is not None)
ok("note provenance is a derived source type",
   N.NOTE_SOURCE_TYPE in P.DERIVED_SOURCE_TYPES)

# ==========================================================================
# 10. Designator survival through Notes text
# ==========================================================================
for text, want in (("ME-GI dual fuel engine", "dsg:me-gi"),
                   ("ME-GA engine", "dsg:me-ga"),
                   ("A-60 class division", "dsg:a-60"),
                   ("BWM D-2 standard", "dsg:d-2"),
                   ("STCW III/2 certificate", "dsg:iii-2"),
                   ("IMO G8 guidelines", "dsg:g-8"),
                   ("MARPOL Annex VI", "dsg:annex-6"),
                   ("IOPP supplement Form B", "dsg:form-b")):
    ok("Notes ingestion preserves the designator in %r" % text,
       want in T.mtokens(text), str(sorted(T.mtokens(text))))

# The alias rule must not blur a real designator family.
ok("the designator alias rule does not satisfy ME-GA with ME-GI",
   not C.satisfied("dsg:me-ga", T.mtokens("ME-GI dual fuel")))
ok("the designator alias rule satisfies an emphasis-capitalised word",
   C.satisfied("dsg:girding", T.mtokens("tug girding capsizing risk")))


# ==========================================================================
if __name__ == "__main__":
    for f in FAILURES:
        print("FAIL  " + f)
    print("\n%d notes controls / %d failures" % (CHECKS[0], len(FAILURES)))
    sys.exit(1 if FAILURES else 0)
