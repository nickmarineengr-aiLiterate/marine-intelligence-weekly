"""Semantic detectors for candidate-facing currentness defects.

WHY THIS MODULE EXISTS
----------------------
Three escapes in a row were caused by a guard that recognised a SPELLING or an
HTML SHAPE instead of a PROPOSITION:

  * Pass 1's hydrant check tested `"4.0 bar"` and the corpus carried `"4.0 Bar"`
    - defeated by CASE.
  * The Pass-1 repair's single-limb check tested the literal `"0.27 N/mm"` and
    scanned only `<li>` and `<p>`; `QB2_F` writes the numerically identical
    quantity as `0.27 MPa` inside a `<div>` - defeated by UNIT and ELEMENT TYPE.
  * The repair's BMP5 check inspected `<span class="reg-code">` slots only, so
    the `<td>` cell and CE-tip prose it had just corrected would have returned
    unnoticed - defeated by HTML CLASS NAME.

Each fix was correct and each was too narrow, because each was written against
the instance in front of it. The remedy is to detect the CLAIM: normalise the
units, take the innermost element of ANY candidate-facing tag, and ask whether
the sentence asserts the thing that is forbidden.

WHAT IS DELIBERATELY NOT HERE
-----------------------------
Unit normalisation is a DETECTOR rule, never an editorial one. 0.27 MPa and
0.27 N/mm2 are the same pressure and a card may legitimately print either; this
module exists so a guard cannot be fooled by the choice, not so a sweep can
rewrite one into the other.

Nothing here decides policy by directory. Surface policy lives in
`census_known_defect_families.surface_family`, and callers apply it.
"""
from __future__ import annotations

import html as htmllib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from oral_lib import strip_tags  # noqa: E402  - THE visible-text extractor

# --------------------------------------------------------------------------
# element geometry - shape-general, not class-name-driven
# --------------------------------------------------------------------------

#: Every tag that can carry candidate-facing text. The point is that the list
#: is about RENDERING, not about this repository's class vocabulary: a claim in
#: a <td> is as visible as one in a <p>, and a guard that knows only <li>/<p>
#: is one authoring style away from blindness.
BLOCK_TAGS = ("li", "p", "td", "th", "div", "span", "strong", "b", "em",
              "h1", "h2", "h3", "h4", "h5", "h6", "summary", "caption")


def enclosing_ladder(html: str, pos: int, tags=BLOCK_TAGS):
    """Every governed element containing `pos`, SMALLEST FIRST.

    A ladder, not a single element, because the innermost element is usually
    too small to carry the claim: in
    `<li>Minimum fire-main pressure: <strong>0.27 MPa</strong> at monitors</li>`
    the innermost element around the figure is the `<strong>`, whose visible
    text is "0.27 MPa" - no context, no modal, and a detector reading only that
    sees nothing. Climbing outward and taking the smallest element that carries
    a COMPLETE claim keeps element scoping (known_traps 89) while letting the
    claim be found wherever the author happened to put the emphasis tags.
    """
    # A STACK, not a depth counter. Tracking depth and only recording a start
    # at depth 0 yields the OUTERMOST element of each tag and never a nested
    # one - so `<div><b>Fire main</b>Min 0.27 MPa at monitors</div>` inside a
    # cheat card resolved to the whole cheat sheet, and the completeness test
    # was then satisfied by unrelated text elsewhere on the page. Every open
    # element containing the position has to be a rung on the ladder.
    spans = []
    for tag in tags:
        stack = []
        for m in re.finditer(r"<(/?)%s\b[^>]*?(/?)>" % tag, html, re.I):
            closing, selfclose = m.group(1), m.group(2)
            if selfclose:
                continue
            if not closing:
                stack.append(m.start())
            elif stack:
                start = stack.pop()
                if start <= pos < m.end():
                    spans.append((start, m.end()))
    return sorted(set(spans), key=lambda s: s[1] - s[0])


def claim_block(html: str, pos: int, needs):
    """The smallest enclosing element whose visible text satisfies `needs`.

    `needs` is a predicate on the visible text. Returning the SMALLEST
    satisfying element is what keeps the completeness test honest: a 0.25 limb
    three paragraphs away must not rescue a single-limb bullet.
    """
    for span in enclosing_ladder(html, pos):
        if needs(visible(html[span[0]:span[1]])):
            return span
    return None


def innermost_block(html: str, pos: int, tags=BLOCK_TAGS):
    """(start, end) of the SMALLEST governed element containing `pos`."""
    best = None
    for tag in tags:
        depth, start = 0, None
        for m in re.finditer(r"<(/?)%s\b[^>]*?(/?)>" % tag, html, re.I):
            closing, selfclose = m.group(1), m.group(2)
            if selfclose:
                continue
            if not closing:
                if depth == 0:
                    start = m.start()
                depth += 1
            else:
                depth -= 1
                if depth == 0 and start is not None:
                    if start <= pos < m.end():
                        span = (start, m.end())
                        if best is None or (span[1] - span[0]) < (best[1] - best[0]):
                            best = span
                        break
                    start = None
                if depth < 0:
                    depth = 0
    return best


def visible(fragment: str) -> str:
    return strip_tags(fragment)


#: Provenance and machine surfaces. A version stamp QUOTES what it removed, so
#: a negative check that reads one reports the changelog as the defect
#: (known_traps 89). `data-*` attributes and JSON-LD are generator input and
#: examiner wording, not teaching.
PROVENANCE = (
    re.compile(r'<span class="q-version">.*?</span>', re.S),
    re.compile(r'<span class="correction-link">.*?</span>', re.S),
    re.compile(r'<div class="q-footer">.*?</div>', re.S),
    re.compile(r'<script[^>]*type="application/ld\+json".*?</script>', re.S),
    re.compile(r'<script.*?</script>', re.S),
    re.compile(r'<style.*?</style>', re.S),
    re.compile(r'<!--.*?-->', re.S),
    re.compile(r'\sdata-(?:search|tags|kw)="[^"]*"', re.S),
    re.compile(r'<meta[^>]*>', re.S),
)


def teaching_html(raw: str) -> str:
    """The page with provenance and machine surfaces blanked, LENGTH-PRESERVED.

    Offsets are preserved so a hit's position still resolves against the
    original element geometry; the removed spans become spaces rather than
    disappearing.
    """
    out = raw
    for rx in PROVENANCE:
        out = rx.sub(lambda m: " " * (m.end() - m.start()), out)
    return out


# --------------------------------------------------------------------------
# unit-normalised pressure
# --------------------------------------------------------------------------

#: Conversions to MPa. DETECTION ONLY.
#: 1 N/mm2 == 1 MPa exactly; 1 bar == 0.1 MPa.
_UNIT_TO_MPA = {"mpa": 1.0, "n/mm": 1.0, "n/mm2": 1.0, "n/mm²": 1.0,
                "bar": 0.1, "kpa": 0.001}

#: A NUMBER GROUP carrying one unit. The unit binds to every figure in the
#: group, not only to the one it touches.
#:
#: The first version required the figure to be immediately adjacent to its
#: unit. In a range only the LAST figure carries it, so `0.27-0.35 MPa` left the
#: governed 0.27 limb unnormalised and invisible - and QB2_F carried exactly
#: that text, live, in a block headed "Numbers & Regulations to Memorise". That
#: was the FOURTH instance of one defect class: case, then unit, then element
#: type, then class name, then NUMBER FORMATTING. A quantity is not its
#: rendering.
#:
#: Separators covered: hyphen, en-dash, em-dash, solidus, "to", and the comma
#: decimal separator used in much of the world.
_NUM = r"\d+(?:[.,]\d+)?"
_SEP = r"\s*(?:-|–|—|/|to)\s*"
PRESSURE = re.compile(
    r"(%s(?:%s%s)*)\s*(MPa|N/mm(?:²|2|\^2)?|bar|kPa)\b" % (_NUM, _SEP, _NUM),
    re.I)


def to_mpa(value: str, unit: str):
    key = unit.lower().replace("²", "").replace("^2", "").rstrip("2") \
        if unit.lower().startswith("n/mm") else unit.lower()
    key = "n/mm" if key.startswith("n/mm") else key
    factor = _UNIT_TO_MPA.get(key)
    return None if factor is None else round(float(value) * factor, 6)


def _figures(group: str):
    """Every figure in a number group, comma decimals accepted."""
    return [f.replace(",", ".") for f in re.findall(_NUM, group)]


def pressures_mpa(text: str):
    """Every pressure in `text`, normalised to MPa.

    A range yields ONE ENTRY PER FIGURE, because "0.27-0.35 MPa" asserts
    something about 0.27 as much as about 0.35.
    """
    out = []
    for m in PRESSURE.finditer(text):
        for fig in _figures(m.group(1)):
            v = to_mpa(fig, m.group(2))
            if v is not None:
                out.append((v, m.group(0)))
    return out


#: The two limbs SOLAS II-2/10.2.1.6 fixes for CARGO ships, in MPa.
UPPER_MPA, LOWER_MPA = 0.27, 0.25

FIREMAIN_CONTEXT = re.compile(
    r"hydrant|fire[\s-]*main|deck\s*monitor|fire\s*pump", re.I)
MANDATORY = re.compile(
    r"minimum|min\b|required|require|mandatory|must|at least|no less than|"
    r"benchmark|shall", re.I)
THRESHOLD = re.compile(r"6[,.]?000\s*(?:GT|gross)", re.I)
#: "two pumps", "2 pumps", "both pumps" - a cheat card writes the numeral and a
#: card writes the word, and the proposition is identical. Spelling-dependence
#: is the defect class this whole module exists to end; it applies to numerals
#: exactly as it applies to units.
TWO_PUMPS = re.compile(r"(?:two|2|both)\s+(?:required\s+)?pumps", re.I)

#: Words that mark a sentence as historical, quoted or self-denying. A
#: correction QUOTES the wording it rejects, so these must not be flagged.
DENIAL = re.compile(
    r"supersed|replaced|predecessor|no longer|formerly|former\b|revoked|"
    r"withdrawn|not a SOLAS minimum|is not a SOLAS|historical|repealed", re.I)


def firemain_scope_defects(raw: str):
    """Elements teaching a fire-main pressure minimum with incomplete scope.

    A hit needs ALL of: fire-main/hydrant/monitor context, a pressure figure at
    a governed value, mandatory framing, and MISSING ship-size scope. Any one
    of those alone is not the defect - which is why an operating pressure
    ("fire main water, typically 5-7 bar") and a weathertightness hose test
    ("minimum pressure of 2 Bar") are both correctly ignored.
    """
    text = teaching_html(raw)
    hits, seen = [], set()
    for m in PRESSURE.finditer(text):
        # A GOVERNED limb anywhere in the group - a range whose floor is the
        # SOLAS cargo-ship figure is making a claim about that figure.
        governed = [to_mpa(f, m.group(2)) for f in _figures(m.group(1))]
        if not any(v in (UPPER_MPA, LOWER_MPA) for v in governed if v is not None):
            continue
        mpa = next(v for v in governed if v in (UPPER_MPA, LOWER_MPA))
        # The smallest enclosing element that actually states a claim: has the
        # fire-main subject AND mandatory framing. If no enclosing element has
        # both, there is no claim here - only a number.
        span = claim_block(
            text, m.start(),
            lambda v: bool(FIREMAIN_CONTEXT.search(v)) and bool(MANDATORY.search(v)))
        if span is None or span in seen:
            continue
        seen.add(span)
        vis = visible(text[span[0]:span[1]])
        if DENIAL.search(vis):
            continue
        values = {v for v, _ in pressures_mpa(vis)}
        complete = (UPPER_MPA in values and LOWER_MPA in values
                    and THRESHOLD.search(vis) and TWO_PUMPS.search(vis))
        if not complete:
            missing = []
            if UPPER_MPA not in values or LOWER_MPA not in values:
                missing.append("a limb")
            if not THRESHOLD.search(vis):
                missing.append("the 6,000 GT threshold")
            if not TWO_PUMPS.search(vis):
                missing.append("the two-pump condition")
            hits.append({"line": text.count("\n", 0, m.start()) + 1,
                         "figure": m.group(0), "mpa": mpa,
                         "missing": ", ".join(missing),
                         "text": vis[:150]})
    return hits


# --------------------------------------------------------------------------
# BMP5 taught as current - semantic, not class-name driven
# --------------------------------------------------------------------------

BMP5 = re.compile(r"BMP\s?5\b", re.I)

#: Present-tense operative constructions. These are what "teaching BMP5 as
#: current" actually looks like on a page, in prose, a table cell, a CE tip or
#: a reg row alike.
OPERATIVE = re.compile(
    r"(?:is|are)\s+codified\s+in|as\s+per\b|per\s+BMP|under\s+BMP|"
    r"in\s+accordance\s+with|recommended\s+by|required\s+by|"
    r"BMP\s?5\s+(?:requires|recommends|provides|sets|states|mandates|says|"
    r"applies|covers|specifies)|follow\s+BMP|apply\s+BMP|"
    r"complies?\s+with|according\s+to", re.I)

#: A reg/code table row treats its code as operative unless it says otherwise.
CODE_SLOT = re.compile(r'<span class="reg-code">([^<]*)</span>', re.I)

#: Stems, navigation and bibliography. A topic whose SUBJECT is BMP5 names it
#: in its title; an index row points at a printed book page; a reference list
#: cites the document that was read. None of these is teaching.
STEM_MARKERS = re.compile(
    r'class="(?:q-text|cs-qtitle|topic-title|topic-tag|idx-|nc-|ref-|qa-q|'
    r'exam-q|toc-link|sub-desc|q-txt)', re.I)

CURRENTNESS_MARK = re.compile(r"Currentness note|has been superseded", re.I)


def governing_container(raw: str, pos: int):
    """The q-card or notes topic that governs `pos`, as (start, end).

    A currentness banner governs its whole card or topic - which is exactly why
    the banner has to be INSIDE the right one. Placed in a neighbouring topic
    it protects the wrong text and leaves the real material unguarded.
    """
    best = None
    for rx in (re.compile(r'<div class="q-card"[^>]*>'),
               re.compile(r'<div class="topic-block"[^>]*>')):
        for m in rx.finditer(raw):
            if m.start() > pos:
                break
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
            if m.start() <= pos < i:
                span = (m.start(), i)
                if best is None or (span[1] - span[0]) < (best[1] - best[0]):
                    best = span
    return best


def bmp5_current_teaching(raw: str):
    """Elements presenting BMP5 as current operational guidance.

    KEEP, and why: a stem or navigation echo is the examiner's own wording; a
    bibliography entry cites a real document; a sentence that denies currency
    is the fix rather than the defect; and any element inside a card or topic
    carrying a currentness note is already governed by it.
    """
    text = teaching_html(raw)
    hits, seen = [], set()
    for m in BMP5.finditer(text):
        span = innermost_block(text, m.start())
        if span is None or span in seen:
            continue
        seen.add(span)
        frag = text[span[0]:span[1]]
        vis = visible(frag)
        head = text[max(0, span[0] - 220):span[0] + 60]
        if STEM_MARKERS.search(head) or STEM_MARKERS.search(frag):
            continue
        if DENIAL.search(vis):
            continue
        container = governing_container(text, m.start())
        if container and CURRENTNESS_MARK.search(text[container[0]:container[1]]):
            continue
        operative = bool(OPERATIVE.search(vis))
        for cm in CODE_SLOT.finditer(frag):
            if BMP5.search(cm.group(1)):
                operative = True
        if not operative:
            continue
        hits.append({"line": text.count("\n", 0, m.start()) + 1,
                     "text": vis[:150]})
    return hits
