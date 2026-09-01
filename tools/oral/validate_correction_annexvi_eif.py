"""Content gate for CORR-ANNEXVI-EIF-20260901.

A digest pin cannot tell you the content is RIGHT (SKILL section 8.2a). It
pins whatever it is given, and it would be perfectly happy with the wrong date
back again as long as the manifest were repinned to match. So the regulatory
proposition this correction turns on gets its own named checks, exactly as
CORR-LSA-LIFEBOAT-VENTILATION and CORR-DEFN-TREATY do.

WHAT THIS ASSERTS, AND WHY IT IS SHAPED THIS WAY
-------------------------------------------------
Known trap 59 already recorded this proposition before the correction, and it
did not catch the defect. Its GREP names ONE spelling of the wrong value,
`1 November 2023`; the cards carried a different wrong rendering of the same
fact, `1 January 2023`, and the guard was blind to all six occurrences. The
shared true-source corpus independently hit a third form, `EIF 2023-01-01`.

One fact, three wrong renderings, a guard written for one of them.

So this file does NOT enumerate wrong dates. It asserts the proposition:

  * every page in scope states 1 November 2022 as the entry into force of the
    MEPC.328(76) amendments; and
  * NO entry-into-force / "effective" / "in force" claim anywhere in scope
    attaches ANY other date to MEPC.328(76) or to the revised Annex VI.

The second half is a closed-world check over an extracted claim set rather
than a blacklist, so a FOURTH wrong rendering nobody has thought of fails on
the day it is written.

AND THE APPLICATION LIMB MUST SURVIVE
--------------------------------------
1 January 2023 is a real, correct date in this subject -- the first year the
CII and SEEMP Part III obligations apply. The defect was collapsing two limbs
into one, not the presence of that date. A guard that simply banned it would
push the next author into deleting a true fact to get green, which is how the
MSC.535(107) card lost its second limb in the first place. So both limbs are
required to be present, and required to be described as different things.

  PYTHONIOENCODING=utf-8 python tools/oral/validate_correction_annexvi_eif.py

Exit 0 if every check passes, 1 otherwise.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
MEO = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio      # noqa: E402

enable_utf8_stdio()

MANIFEST = HERE / "correction_corr_annexvi_eif_20260901_manifest.json"
TRAPS = MEO / "known_traps.md"

# The pages this correction owns. The cheat sheet carries no q-card and takes
# no digest, which is exactly why it needs a content check: nothing else in
# the toolchain would notice it going stale.
# QB7_C joined this list when the closed-world check below found an EIGHTH
# occurrence there that the targeted grep had missed: it spells the
# resolution "MEPC 76", which no search for "MEPC.328(76)" can find.
PAGES = ["QB7_A.html", "QB7_A_CheatSheet.html", "QB7_C.html"]

# Every page that cites this resolution at all, so the check cannot be
# satisfied by the two corrected pages while a third drifts the other way.
CITING = ["QB1_C.html", "QB3_C.html", "QB6.html", "QB6_cheatsheet.html",
          "QB7_A.html", "QB7_A_CheatSheet.html", "QB7_C.html"]

EIF_CORRECT = re.compile(
    r"1 Nov(?:ember)? 2022", re.I)
APPLIES_CORRECT = re.compile(
    r"1 Jan(?:uary)? 2023", re.I)

# An entry-into-force CLAIM: one of these words, then a date, within a short
# window. Deliberately claim-shaped rather than date-shaped -- see the module
# docstring.
CLAIM = re.compile(
    r"(?:in force|into force|effective|entry into force)"
    r"[^.<]{0,60}?"
    r"(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"
    r"[a-z]*\s+\d{4})",
    re.I)

results: list[tuple[str, bool, str]] = []


def check(name: str, ok, detail: str = "") -> None:
    results.append(("eif_" + name, bool(ok), detail))


def visible(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text))


# Reference tables and "Numbers to Memorise" lines pack many instruments into
# one paragraph, separated by bullets and semicolons. A fixed-width lookbehind
# therefore straddles neighbours: the first draft of this check read FuelEU
# Maritime's own correct "effective 1 January 2025" as a claim about Annex VI,
# because "MARPOL Annex VI / Reg 28" was the NEXT cell in the table.
SEPARATORS = re.compile(r"·|;|\. |\|")


def claim_subject_window(text: str, start: int) -> str:
    """The text between the nearest preceding separator and the claim.

    The subject of one of these claims always precedes it inside its own
    item, so cutting at the separator keeps a neighbour's instrument name out
    of this claim's evidence.
    """
    left = max(0, start - 200)
    seg = text[left:start]
    cuts = [m.end() for m in SEPARATORS.finditer(seg)]
    return seg[cuts[-1]:] if cuts else seg


def near_resolution(window: str) -> bool:
    """Is this claim about MEPC.328(76) / the revised Annex VI?

    A competing instrument named in the SAME item wins: an item reading
    "FuelEU Maritime (Regulation 2023/1805), effective 1 January 2025" is not
    a claim about Annex VI even when Annex VI is mentioned nearby.
    """
    if re.search(r"FuelEU|2023/1805|EU ETS|Directive 2003/87|MEPC[.\s]*3(?:33|46|47|95)",
                 window, re.I):
        return False
    return bool(re.search(r"MEPC[.\s]*328\s*\(?76\)?|MEPC[.\s]*76\b|Annex\s*VI",
                          window, re.I))


def eif_statements(v: str) -> list:
    """Every window in which this page states the verified entry-into-force
    date, wide enough to contain the application limb if it is stated."""
    return [v[max(0, m.start() - 90):m.end() + 130]
            for m in EIF_CORRECT.finditer(v)]


def main() -> int:
    results.clear()

    if not MANIFEST.is_file():
        check("manifest_present", False, "correction record absent")
        return report()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    check("manifest_present", True)

    # 1. the correction still claims what it claims. A record silently
    #    restated to authorise the OLD date would make every check below a
    #    description of whatever happens to be on disk.
    check("record_states_the_right_date",
          "1 November 2022" in manifest.get("rationale", ""),
          "the rationale no longer names the verified entry-into-force date")
    check("record_keeps_the_application_limb",
          "1 January 2023" in manifest.get("rationale", "")
          and "OBLIGATIONS" in manifest.get("rationale", "").upper(),
          "the rationale no longer distinguishes application from entry "
          "into force")
    check("record_cites_the_trap",
          59 in (manifest.get("known_traps_entries") or []),
          "known_traps_entries=%s" % manifest.get("known_traps_entries"))

    # 2. the trap register carries BOTH wrong renderings, so the next author
    #    meets the whole defect and not the half of it that was found first.
    traps = TRAPS.read_text(encoding="utf-8") if TRAPS.is_file() else ""
    # Scoped to entry 59 itself, and to the sentence that names the second
    # rendering AS a wrong rendering. A bare `"1 January 2023" in traps` was
    # satisfied by the two-limb bullet list further down the same entry, so
    # trimming the sentence that explains the variant escaped the check.
    entry = ""
    m = re.search(r"^### 59\..*?(?=^### 60\.)", traps, re.S | re.M)
    if m:
        entry = m.group(0)
    check("trap_59_names_both_wrong_renderings",
          bool(entry)
          and "1 November 2023" in entry
          and bool(re.search(r"different\*{0,2} wrong value for the same "
                             r"fact[^\n]*1 January 2023", entry))
          and "GREP: SKIP" in entry,
          "entry 59 must name BOTH wrong renderings as wrong -- it quotes them "
          "in order to reject them, which is why it is GREP: SKIP -- or the "
          "next author meets only the half of the defect found first")

    # 3. both limbs present on every corrected page, and DISTINGUISHED.
    for name in PAGES:
        path = MEO / name
        if not path.is_file():
            check("%s_present" % name, False, "absent")
            continue
        v = visible(path.read_text(encoding="utf-8"))
        check("%s_states_entry_into_force" % name, bool(EIF_CORRECT.search(v)),
              "no '1 November 2022' on the page")
        # Page-wide presence is not enough. The first version of this check
        # searched the whole page, and mutation B -- deleting the application
        # limb from the statement standing beside the entry-into-force date --
        # escaped it, because an unrelated table row elsewhere still carried
        # "1 Jan 2023". The two limbs have to travel TOGETHER or the candidate
        # reads one date and never meets the other.
        total = eif_statements(v)
        paired = [w for w in total if APPLIES_CORRECT.search(w)]
        # Requiring EVERY statement to pair both limbs was too strong and
        # produced a false failure: QB7_C's regulatory-reference table row
        # gives the entry-into-force date alone, which is correct and complete
        # for a reference row. What the correction is actually about is that
        # the page must TEACH both limbs somewhere and must never present the
        # application date AS the entry into force -- and the closed-world
        # check below owns that second half. So: at least one statement here
        # must carry both.
        check("%s_keeps_application_limb" % name, bool(paired),
              "%d of %d entry-into-force statements on this page carry the "
              "application limb beside them; a page that states one date and "
              "never the other is how the MSC.535(107) card lost its second "
              "limb" % (len(paired), len(total)))

    # 4. THE CLOSED-WORLD CHECK. Not a blacklist: every entry-into-force claim
    #    made anywhere near this resolution must give the verified date. A
    #    fourth wrong rendering fails here on the day it is written.
    bad = []
    for name in CITING:
        path = MEO / name
        if not path.is_file():
            continue
        v = visible(path.read_text(encoding="utf-8"))
        for m in CLAIM.finditer(v):
            window = claim_subject_window(v, m.start())
            if not near_resolution(window):
                continue
            date = re.sub(r"\s+", " ", m.group(1)).strip()
            if not EIF_CORRECT.fullmatch(date):
                bad.append("%s: %r in %r" % (name, date, window[-140:]))
    check("no_other_entry_into_force_date_for_this_resolution", not bad,
          "; ".join(bad[:4]) or "none")

    return report()


def report() -> int:
    failed = [r for r in results if not r[1]]
    for name, ok, detail in results:
        if not ok:
            print("FAIL %-56s %s" % (name, detail))
    print()
    print("correction ANNEXVI-EIF validator -- %d checks, %d FAIL"
          % (len(results), len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
