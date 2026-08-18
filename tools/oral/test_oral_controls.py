"""Phase 2A-i correctness-floor controls.

These are load-bearing assertions, not smoke tests. Each one exists because the
behaviour it pins was observed to be wrong in the Phase 2 reconciliation and
was found by the Laptop's independent review at c78a228.

  PYTHONIOENCODING=utf-8 python tools/oral/test_oral_controls.py

Exit 0 when every control holds. Portability: repo-relative, no drive letters,
no external inputs.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_text as T          # noqa: E402
import oral_provenance as P    # noqa: E402
import reconcile_788 as R      # noqa: E402

FAILURES = []
CHECKS = [0]


def ok(name, condition, detail=""):
    CHECKS[0] += 1
    if not condition:
        FAILURES.append("%s %s" % (name, ("- " + detail) if detail else ""))


# ==========================================================================
# 1. Spell-repair regression controls
#
# The speculative repairer fired on any token of five or more characters absent
# from the QB vocabulary and replaced it with its nearest corpus spelling. An
# unknown token is not a typo, and the QB corpus is not a dictionary: it
# inverted meanings (attended -> unattended), changed legal facts (convinced ->
# convicted) and damaged the designators the tokeniser exists to protect
# (and92 -> and9, stcw5 -> stcw15, iii16 -> iii6).
# ==========================================================================
UNCHANGED = [
    # correct English the corpus simply does not happen to contain
    "attended", "unattended", "convinced", "convicted", "provident", "provide",
    "biased", "conciliation", "interesting", "appealing", "shale", "strees",
    # load-bearing alphanumerics
    "and92", "and9", "stcw5", "stcw15", "iii16", "iii6",
    "megi", "mega", "a60", "d1", "d2", "g8", "g9", "iso8217",
]
for tok in UNCHANGED:
    fixed, note = T.repair(tok)
    ok("spell-repair leaves %r alone" % tok, fixed == tok and note is None,
       "became %r" % fixed)

# designator tokens are load-bearing by construction, never rewritten
for tok in ("dsg:me-gi", "dsg:me-ga", "dsg:annex-1", "dsg:annex-6",
            "dsg:form-a", "dsg:form-b", "dsg:iii-16"):
    ok("designator token %r is load-bearing" % tok, T.is_load_bearing(tok))

# the general guard, stated as a rule rather than as a list of examples
for tok in ("and92", "stcw15", "iii16", "a60", "ii", "iii", "vi", "x",
            "annex-6", "me-gi"):
    ok("load-bearing guard covers %r" % tok, T.is_load_bearing(tok))
for tok in ("amendment", "delegation", "welfare", "survey", "stability"):
    ok("load-bearing guard does not over-reach on %r" % tok,
       not T.is_load_bearing(tok))

# the curated map still does the work that was worth keeping
for wrong, right in (("johri", "johari"), ("ammendment", "amendment"),
                     ("deligation", "delegation"), ("wellfare", "welfare"),
                     ("personm", "personam"), ("lastest", "latest")):
    fixed, note = T.repair(wrong)
    ok("curated repair %s -> %s" % (wrong, right), fixed == right,
       "got %r" % fixed)

# no curated entry may itself be load-bearing, now or after future edits
for k, v in T.SOURCE_TYPO_MAP.items():
    ok("curated key %r is not load-bearing" % k, not T.is_load_bearing(k))
    ok("curated value %r is not load-bearing" % v, not T.is_load_bearing(v))

# repairs are emitted in a stable order regardless of set iteration
_raw = {"ammendment", "wellfare", "johri", "survey", "and92"}
ok("repair notes are deterministic",
   T.repair_tokens(_raw)[1] == T.repair_tokens(set(reversed(sorted(_raw))))[1])


# ==========================================================================
# 2. Designator tokenisation controls
#
# ME-GI and ME-GA both tokenised to nothing, so all four occurrences scored
# MISSING at coverage 0.00 against a corpus holding 27 ME-GI and 46 ME-GA
# mentions. Annex I was indistinguishable from a bare "Annex", Annex VI never
# met Annex 6, and Form A never met Form B.
# ==========================================================================
def toks(s):
    return T.mtokens(s)


for d in ("ME-GI", "ME-GA", "ME-LGI", "A-60", "A-0", "D-1", "D-2",
          "III/1", "III/2", "G8", "G9", "ISO 8217", "Reg 13"):
    ok("designator %s survives tokenisation" % d, bool(toks(d)), "empty")

DISTINCT = [("ME-GI", "ME-GA"), ("ME-GI", "ME-LGI"), ("A-0", "A-60"),
            ("D-1", "D-2"), ("III/1", "III/2"), ("G8", "G9"),
            ("Annex I", "Annex VI"), ("Form A", "Form B"),
            ("Tier II", "Tier III")]
for a, b in DISTINCT:
    ok("%s is distinguishable from %s" % (a, b), toks(a) != toks(b))
    ok("%s conflicts with %s" % (a, b),
       T.designator_conflict(toks(a), toks(b)))

# the same designator written differently must meet, not conflict
for a, b in (("Annex VI", "Annex 6"), ("A-60", "A60 bulkhead"),
             ("ME-GI", "MEGI and MEGA engines"), ("Tier III", "Tier 3")):
    ok("%s meets %s" % (a, b), bool(toks(a) & toks(b)), "no shared token")
for a, b in (("Annex VI", "Annex 6"), ("ME-GI engine", "ME-GI dual fuel"),
             ("D-1 standard", "ballast water exchange")):
    ok("%s does not conflict with %s" % (a, b),
       not T.designator_conflict(toks(a), toks(b)))

# ordinary hyphenated English must NOT be treated as a designator, or the rule
# is overbroad and every compound word becomes a false discriminator
for phrase in ("well-founded", "state-of-the-art", "cross-question",
               "self-assessment", "risk-based", "long-term"):
    ok("ordinary hyphenation %r yields no designator" % phrase,
       not T.designators(phrase), str(T.designators(phrase)))
ok("ordinary hyphenation does not conflict with itself",
   not T.designator_conflict(toks("well-founded decision"),
                             toks("well-founded judgement")))
ok("unrelated prose never conflicts",
   not T.designator_conflict(toks("bunker delivery note"),
                             toks("oil record book")))


# ==========================================================================
# 3. SAME_CORE_ASK admission floor
#
# classify() applied a similarity floor to EXACT (0.55) and NEAR (0.30) and
# none at all to SAME_CORE: 52% of SAME_CORE rows sat below sim 0.25, median
# similarity was 0.22 against 0.67 for EXACT, and reviewed precision was 60%
# against 100% for EXACT. Same subject area is not the same ask.
#
# The calibration set below is drawn from real Phase-2 rows. Each entry is
# (label, source ask, matched question, n source tokens, sim, reverse coverage).
# ==========================================================================
TRUE_SAME_CORE = [
    ("legal", "Difference between Act and rule",
     "Act vs rule - difference in Indian legal context", 4, 0.33, 0.37),
    ("fire/safety", "Watertight and weathertight doors difference",
     "What is the difference between watertight and weathertight", 4, 0.33, 0.44),
    ("stability", "Damage stability conditions & criteria",
     "State the Damage Stability Criteria for cargo ships", 4, 0.30, 0.37),
    ("survey/class", "Contents of Class Status Report",
     "What is the class quarterly listing / survey status report", 4, 0.38, 0.42),
    ("MARPOL", "MARPOL Annexes related to your vessel",
     "All MARPOL related documents on your type of ship", 4, 0.43, 0.47),
    ("management", "Decision making techniques",
     "Decision-Making Tools Onboard", 3, 0.40, 0.57),
]
SAME_TOPIC_DIFFERENT_ASK = [
    ("legal", "Shipping master duties",
     "VGM - who is responsible, two certified methods", 3, 0.15, 0.15),
    ("regulations", "LSA code - latest amendment in LSA code",
     "Polar Code - what is the latest amendment", 4, 0.12, 0.51),
    ("legal/insurance", "What is LLMC, what all does it apply to?",
     "Explain the HNS Convention - to whom does it apply", 3, 0.13, 0.13),
    ("MARPOL", "How to check CII compliance onboard",
     "What is shore power (cold ironing) and its CII effect", 4, 0.17, 0.20),
    ("survey/class", "Explain safety construction survey related to the ship",
     "If a ship has already undergone a Renewal survey ...", 6, 0.16, 0.20),
    ("engine", "NOx reduction procedures before and after combustion",
     "NOx reduction methods - EGR vs SCR", 6, 0.25, 0.28),
]
TERSE = [
    ("MRCC", 1, 0.09, 0.10),        # -> a major-accident contact question
    ("MLC", 1, 0.25, 0.25),         # -> "who is the assessor in MLC/STCW"
    ("GA PA YA rule", 1, 0.12, 0.17),   # -> "Act vs rule", matched on "rule"
]

for area, ask, target, n, sim, rev in TRUE_SAME_CORE:
    admitted, why = R.same_core_admissible(n, sim, rev, False)
    ok("SAME_CORE admits a true match [%s] %r" % (area, ask[:34]), admitted, why)

for area, ask, target, n, sim, rev in SAME_TOPIC_DIFFERENT_ASK:
    admitted, why = R.same_core_admissible(n, sim, rev, False)
    ok("SAME_CORE rejects same-topic-different-ask [%s] %r" % (area, ask[:34]),
       not admitted, "admitted %r -> %r" % (ask[:30], target[:30]))

for ask, n, sim, rev in TERSE:
    admitted, why = R.same_core_admissible(n, sim, rev, False)
    ok("SAME_CORE rejects the terse prompt %r" % ask, not admitted)

# a contradictory load-bearing designator blocks SAME_CORE outright, however
# similar the surrounding prose is
ok("a designator conflict blocks SAME_CORE",
   not R.same_core_admissible(8, 0.90, 0.90, True)[0])

# ...and blocks it inside classify() too, so an ME-GI ask can never be awarded
# an ME-GA question just because the engine designator carried no weight
disp, _ = R.classify(1.0, 0.9, 1.0, 1.0, 1.0, 1, n_src_tokens=8, rev=0.9,
                     conflict=True)
ok("classify() never promotes a conflicting designator above PARTIAL",
   disp not in (R.EXACT, R.NEAR, R.SAME_CORE), disp)

# a rejected SAME_CORE falls to PARTIAL, never to MISSING: under-crediting a
# covered ask costs an enrichment task, it never misleads a candidate
disp, _ = R.classify(0.80, 0.12, 0.5, 0.5, 0.5, 1, n_src_tokens=4, rev=0.20)
ok("a row below the SAME_CORE floor lands in PARTIAL", disp == R.PARTIAL, disp)

# the floor must not swallow the classes that already had one
disp, _ = R.classify(1.00, 0.70, 1.0, 1.0, 1.0, 1, n_src_tokens=2, rev=0.30)
ok("EXACT is unaffected by the SAME_CORE floor", disp == R.EXACT, disp)
disp, _ = R.classify(0.90, 0.40, 1.0, 1.0, 1.0, 1, n_src_tokens=2, rev=0.30)
ok("NEAR is unaffected by the SAME_CORE floor", disp == R.NEAR, disp)


# ==========================================================================
# 4. Evidence provenance controls
#
# Strong evidence cannot be established by changing a label. Mutation M5 -
# relabelling a CURRENT_INDEX_RECOVERY record PRIMARY_TRACKER - passed the
# 35-check validator, because nothing looked at provenance.
# ==========================================================================
def rec(tier, source):
    return {"evidence_id": "T-1", "evidence_tier": tier, "source_type": source}


PROMOTIONS = ["CURRENT_INDEX_RECOVERY", "JULY_DERIVED_SIBLING",
              "TOPIC_INFERRED", "CE_TIP", "NOTE_EXPLICIT"]
for source in PROMOTIONS:
    ok("%s cannot be relabelled PRIMARY_TRACKER" % source,
       P.incompatible(rec("PRIMARY_TRACKER", source)) is not None)

for tier in PROMOTIONS:
    ok("%s is a legitimate tier on its own provenance" % tier,
       P.incompatible(rec(tier, tier)) is None,
       str(P.incompatible(rec(tier, tier))))

ok("a genuine primary record is accepted",
   P.incompatible(rec("PRIMARY_TRACKER", "PRIMARY_TRACKER")) is None)
ok("a tier with no provenance at all is rejected",
   P.incompatible({"evidence_id": "T-2",
                   "evidence_tier": "PRIMARY_TRACKER"}) is not None)
ok("an unknown tier is rejected",
   P.incompatible(rec("TOTALLY_CONFIRMED", "PRIMARY_TRACKER")) is not None)

# NOTE_EXPLICIT is provisioned for Phase 2A-ii and must already be governed
ok("NOTE_EXPLICIT is a known tier", "NOTE_EXPLICIT" in P.EVIDENCE_TIERS)
ok("NOTE_EXPLICIT is not a primary tier",
   "NOTE_EXPLICIT" not in P.PRIMARY_TIERS)
ok("NOTE_EXPLICIT is not TOPIC_INFERRED",
   P.incompatible(rec("TOPIC_INFERRED", "NOTE_EXPLICIT")) is not None)


# ==========================================================================
if __name__ == "__main__":
    for f in FAILURES:
        print("FAIL  " + f)
    print("\n%d controls / %d failures" % (CHECKS[0], len(FAILURES)))
    sys.exit(1 if FAILURES else 0)
