"""Semantic detectors for candidate-facing currentness defects.

WHAT CHANGED, AND WHY IT HAD TO
-------------------------------
Five review rounds each found the same defect wearing new clothes: a guard that
recognised a RENDERING of a claim instead of the claim - case, then unit, then
element type, then HTML class name, then number formatting. Every round added a
list; every next reviewer found that list's edge.

So the lists are gone:

  * matching runs on NORMALISED VISIBLE TEXT (`oral_visible`), never on raw
    HTML, so entities, `&nbsp;`, unicode dashes, superscripts and figures split
    across tags collapse before anything is compared;
  * element coverage is by EXCLUSION - the inline-tag set is small, standard
    and closed, and everything else is a block, so a claim in a `<dd>` or a
    `<figcaption>` is segmented like any other;
  * BMP5 currentness is DEFAULT-SUSPICIOUS. The old detector asked "does this
    sentence match one of my 14 operative phrasings?", and missed the plainest
    form of the proposition it was named for - "BMP5 is the current industry
    guidance". It now asks the opposite question: is this mention EXCUSED? A
    mention that is not historical, not quoted, not a stem, not bibliography
    and not governed by a currentness note is a live claim;
  * DENIAL IS SENTENCE-SCOPED. A denial token anywhere in an element used to
    silence the whole element, so "BMP5 replaced BMP4, but BMP5 is the guidance
    we apply today" passed. Each proposition is now judged on its own.

WHAT IS DELIBERATELY NOT HERE
-----------------------------
Unit normalisation is a DETECTOR rule and never an editorial one: a card may
print MPa or N/mm2 as it likes, and nothing here rewrites product text. And no
surface policy - which surfaces are governed lives in
`census_known_defect_families.surface_family`, and callers apply it.
"""
from __future__ import annotations

import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from oral_visible import (                     # noqa: E402
    segments, sentences, normalise, container_classes)

# ==========================================================================
# pressure - quantity, not spelling
# ==========================================================================

#: Conversions to MPa. Deterministic and isolated - DETECTION ONLY.
#: 1 N/mm2 == 1 MPa exactly. The imperial and legacy metric units are here
#: because a defect re-entering as "39 psi" would be exactly as wrong and
#: exactly as invisible; conversion is arithmetic, not judgement.
_UNIT_MPA = {
    "mpa": 1.0,
    "n/mm2": 1.0, "n/mm": 1.0,
    "n/cm2": 0.01,
    "bar": 0.1,
    "mbar": 0.0001,
    "kpa": 0.001,
    "pa": 1e-6,
    "kg/cm2": 0.0980665,
    "kgf/cm2": 0.0980665,
    "psi": 0.00689476,
    "atm": 0.101325,
}

#: After normalisation "N/mm²" is "N/mm2" and "kg/cm²" is "kg/cm2", so the
#: pattern needs no superscript or entity alternatives at all.
_UNIT_RX = (r"MPa|N\s*/\s*mm2?|N\s*/\s*cm2|kgf?\s*/\s*cm2|mbar|bar|kPa|Pa|psi|"
            r"atm|megapascals?")
_NUM = r"\d+(?:[.,]\d+)?"
_SEP = r"\s*(?:-|/|to|and|or)\s*"
PRESSURE = re.compile(r"(%s(?:%s%s)*)\s*(%s)\b" % (_NUM, _SEP, _NUM, _UNIT_RX),
                      re.I)


def _unit_key(unit: str) -> str:
    u = re.sub(r"\s+", "", unit.lower())
    if u.startswith("megapascal"):
        return "mpa"
    return u


def to_mpa(value: str, unit: str):
    """One figure + one unit -> MPa, or None if the unit is unknown."""
    f = _UNIT_MPA.get(_unit_key(unit))
    if f is None:
        return None
    try:
        return round(float(str(value).replace(",", ".")) * f, 9)
    except ValueError:
        return None


def _figures(group: str):
    return re.findall(_NUM, group)


def pressures_mpa(text: str):
    """Every pressure in normalised text, in MPa.

    A range yields one entry per figure: "0.27-0.35 MPa" asserts something
    about 0.27 as much as about 0.35, and in a range only the last figure
    carries the unit - the blind spot that let a governed limb through.
    """
    out = []
    for m in PRESSURE.finditer(text):
        for fig in _figures(m.group(1)):
            v = to_mpa(fig, m.group(2))
            if v is not None:
                out.append((v, m.group(0)))
    return out


#: SOLAS II-2/10.2.1.6, cargo ships, in MPa.
UPPER_MPA, LOWER_MPA = 0.27, 0.25

#: RELATIVE tolerance, because a legacy unit does not convert to a round
#: number: 2.7538 kg/cm2 and 39.16 psi are both 0.27 MPa to any practical
#: precision, and an exact-equality test simply cannot see them. 1% is safe -
#: the two limbs differ by 8%, so no tolerance this size can confuse them.
_REL_TOL = 0.01


def _is(value, limb):
    return abs(value - limb) <= limb * _REL_TOL

FIREMAIN = re.compile(r"hydrant|fire[\s-]*main|deck\s*monitor|fire\s*pump", re.I)
MANDATORY = re.compile(
    r"minimum|min\b|required|require|mandatory|must|shall|at least|"
    r"no less than|not fall below|lowest|benchmark|target", re.I)
THRESHOLD = re.compile(r"6[,.]?000\s*(?:GT|gross)", re.I)
TWO_PUMPS = re.compile(r"(?:two|2|both)\s+(?:required\s+)?pumps", re.I)

#: A proposition that is about the PAST or is being denied.
DENIAL = re.compile(
    r"supersed|replaced|predecessor|no longer|formerly|former\b|earlier\b|"
    r"revoked|withdrawn|historical|repealed|used to\b|previously|"
    r"not a SOLAS|is not the current|do not (?:offer|use|quote|present)|"
    r"was the\b|prior\b", re.I)


def _governed(values):
    return any(_is(v, UPPER_MPA) or _is(v, LOWER_MPA) for v in values)


def firemain_scope_defects(raw: str):
    """Fire-main pressure claims that state a governed limb with incomplete scope.

    A hit needs ALL of: the fire-main subject, a governed figure, mandatory
    framing, and MISSING ship-size scope. Any three of the four is not the
    defect - which is why an equipment operating pressure ("fire main water,
    typically 5-7 bar") and a weathertightness hose test ("minimum pressure of
    2 Bar") are both correctly ignored: neither carries a governed figure.
    """
    hits = []
    for text, stack, line, seg_cls in segments(raw):
        cls = container_classes(stack) | seg_cls
        # A version stamp QUOTES what it removed; reading it reports the
        # changelog as the defect (known_traps 89).
        if cls & {"q-version", "correction-link", "q-footer"}:
            continue
        for sent in sentences(text):
            vals = [v for v, _ in pressures_mpa(sent)]
            if not _governed(vals):
                continue
            if not (FIREMAIN.search(sent) or FIREMAIN.search(text)):
                continue
            if not (MANDATORY.search(sent) or MANDATORY.search(text)):
                continue
            if DENIAL.search(sent):
                continue
            # Completeness is judged on the SEGMENT, never the page: a 0.25
            # three paragraphs away must not rescue a single-limb bullet.
            seg_vals = [v for v, _ in pressures_mpa(text)]
            complete = (
                any(_is(v, UPPER_MPA) for v in seg_vals)
                and any(_is(v, LOWER_MPA) for v in seg_vals)
                and THRESHOLD.search(text) and TWO_PUMPS.search(text))
            if complete:
                continue
            missing = []
            if not any(_is(v, UPPER_MPA) for v in seg_vals) \
                    or not any(_is(v, LOWER_MPA) for v in seg_vals):
                missing.append("a limb")
            if not THRESHOLD.search(text):
                missing.append("the 6,000 GT threshold")
            if not TWO_PUMPS.search(text):
                missing.append("the two-pump condition")
            hits.append({"line": line, "missing": ", ".join(missing),
                         "text": sent[:160]})
            break
    return hits


# ==========================================================================
# BMP5 - default-suspicious, excused by context
# ==========================================================================

BMP5 = re.compile(r"\bBMP\s?5\b", re.I)

#: Container classes that carry the EXAMINER'S wording, navigation, indexes or
#: bibliography rather than teaching. These are identities, not phrasings, so
#: they do not rot the way a phrase list does.
EXCUSED_CLASSES = frozenset("""
q-text cs-qtitle q-txt topic-title topic-tag topic-meta topic-pages
toc-link sub-desc nc-title nc-sub nc-topic nc-header idx-topic idx-note
idx-page idx-row ref-list qa-q exam-q q-version correction-link q-footer
marks-badge search-hit
""".split())

#: A reference LIST cites what was read. `<li>BMP5 - "Best Management
#: Practices..."` under a References head is history, not instruction.
BIBLIO_HINT = re.compile(
    r'^\s*BMP\s?5\s*[-:–]|Best Management Practices to Deter Piracy', re.I)

#: The current publication. A sentence naming it alongside BMP5 is drawing the
#: contrast, not teaching the old one.
SUCCESSOR = re.compile(r"BMP\s*(?:MS|Maritime\s+Security)", re.I)

#: A page-level statement of what the material was compiled from. Provenance,
#: not instruction - and naming a superseded publication among one's sources is
#: a historical fact about the compilation, not a claim that it is current.
PROVENANCE_HINT = re.compile(
    r"compiled from|derived from|sources? consulted|material is compiled|"
    r"reclassified backlog|questions on", re.I)

#: A container statement that puts its subject in the past. Broader than
#: "Currentness note" on purpose: QB4_H#q11 opens "Predecessor publication -
#: superseded; see Q13 for the current guidance", which governs that whole card
#: just as effectively, and a marker that only recognised one house phrasing
#: reported the corpus's own predecessor record as a defect.
CURRENTNESS_MARK = re.compile(
    r"currentness note|supersed|predecessor|no longer current|replaced|"
    r"current publication", re.I)


def _excused(sent: str, seg: str, cls: frozenset) -> str | None:
    """Why this BMP5 mention is NOT a live claim, or None if it is one."""
    if cls & EXCUSED_CLASSES:
        return "examiner wording / navigation / index / provenance"
    if BIBLIO_HINT.search(seg):
        return "bibliography entry"
    if PROVENANCE_HINT.search(seg):
        return "page provenance / compilation note"
    # A mention wholly inside quotation marks is somebody else's words - an
    # examiner cue on a cheat sheet, a quoted question. The corpus keeps those
    # deliberately.
    if re.search(r'[\"“‘][^\"”’]{0,80}BMP\s?5'
                 r'[^\"”’]{0,80}[\"”’]', seg, re.I):
        return "quoted wording"
    if sent.rstrip().endswith("?"):
        return "a question, not an assertion"
    if DENIAL.search(sent):
        return "the sentence denies currency"
    if SUCCESSOR.search(sent):
        return "the sentence names the successor publication"
    return None


def _governing_currentness(raw: str):
    """Byte ranges of containers carrying a BMP-SUBJECT currentness note.

    Subject-specific on purpose: a card may carry a currentness note about a
    different instrument entirely, and that must not grant blanket immunity to
    an unrelated BMP5 claim sitting beside it.
    """
    spans = []
    for m in re.finditer(r'<div class="(?:q-card|topic-block)"[^>]*>', raw):
        depth, i, n = 0, m.start(), len(raw)
        while i < n:
            if raw.startswith("<div", i):
                depth += 1
                i += 4
                continue
            if raw.startswith("</div>", i):
                depth -= 1
                i += 6
                if depth == 0:
                    break
                continue
            i += 1
        body = raw[m.start():i]
        if CURRENTNESS_MARK.search(body) and BMP5.search(body) \
                and SUCCESSOR.search(body):
            spans.append((m.start(), i, raw.count("\n", 0, m.start()) + 1,
                          raw.count("\n", 0, i) + 1))
    return spans


def bmp5_current_teaching(raw: str):
    """Sentences presenting BMP5 as live guidance.

    DEFAULT-SUSPICIOUS. The question is not "does this match an operative
    phrasing I listed?" - that missed "BMP5 is the current industry guidance",
    the plainest form of the claim. The question is "is this mention excused?".
    """
    governed = _governing_currentness(raw)
    hits = []
    for text, stack, line, seg_cls in segments(raw):
        if not BMP5.search(text):
            continue
        cls = container_classes(stack) | seg_cls
        if any(a <= line <= b for _s, _e, a, b in governed):
            continue
        for sent in sentences(text):
            if not BMP5.search(sent):
                continue
            why = _excused(sent, text, cls)
            if why is None:
                hits.append({"line": line, "text": sent[:160]})
                break
    return hits
