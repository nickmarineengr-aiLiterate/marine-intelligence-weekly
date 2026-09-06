"""Normalised visible text, segmented the way a reader sees it.

WHY THIS EXISTS
---------------
Five review rounds each found the same defect: a guard that recognised a
RENDERING of a claim instead of the claim. Case, then unit, then element type,
then HTML class name, then number formatting. Every fix enumerated one more
list, and the next reviewer found the next list's edge.

The lists were the defect. This module removes the need for them:

  * **Entities, `&nbsp;`, split tags and unicode punctuation disappear before
    matching**, because matching happens on decoded, normalised text - never on
    raw HTML. `0.27&nbsp;MPa`, `<strong>0.27</strong> MPa` and
    `0.27 <span>MPa</span>` are all the string `0.27 MPa`.
  * **Element coverage is by exclusion, not enumeration.** A guard cannot list
    every block tag an author might use - `<dd>`, `<figcaption>`, `<caption>`
    were all missed by the last attempt. It CAN list the inline tags, because
    that set is small, standard and closed. Everything not inline is a block,
    so a claim in a tag nobody has thought of is still segmented correctly.

WHAT A SEGMENT IS
-----------------
The text a reader sees as one run: block boundaries and `<br>` end a segment,
inline formatting does not. That is the natural unit for "is this one claim?".
Sentences within a segment are then available separately, because a denial in
one clause must not silence an assertion in the next - "BMP5 replaced BMP4, but
BMP5 is what we use today" is two propositions and only the second is a defect.

Import-only: no paths, no policy, no I/O.
"""
from __future__ import annotations

import re
import unicodedata
from html.parser import HTMLParser

#: Inline tags do not break the run of text a reader sees. Closed, standard,
#: and the ONLY tag list in this module - everything else is a block.
INLINE = frozenset("""
a abbr acronym b bdi bdo big cite code data del dfn em font i ins kbd label
mark nobr q rp rt ruby s samp small span strike strong sub sup time tt u var
wbr
""".split())

#: Never rendered.
SKIP = frozenset(("script", "style", "template", "noscript", "head", "title"))

#: Void tags that force a visual break inside a block.
BREAK = frozenset(("br", "hr"))

_DASHES = dict.fromkeys(map(ord, "‐‑‒–—―"
                                 "−⁃﹘﹣－"), "-")
_SPACES = dict.fromkeys(map(ord, "       "
                                 "     　"), " ")
_SUPERS = {ord("²"): "2", ord("³"): "3", ord("¹"): "1",
           ord("·"): ".", ord("⋅"): ".", ord("⁄"): "/"}


def normalise(text: str) -> str:
    """Fold the renderings a reader cannot tell apart.

    Dashes, exotic spaces, superscript digits, fullwidth digits and the
    multiplication dot all collapse. Case is NOT folded here - callers that
    need case-insensitivity ask for it, because some checks legitimately care
    about capitalisation of a proper noun.
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(_DASHES).translate(_SPACES).translate(_SUPERS)
    return re.sub(r"[ \t\r\f\v]+", " ", text).strip()


class _Segmenter(HTMLParser):
    """Emit (segment_text, container_stack, lineno) for a document."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.segments = []
        self._buf = []
        self._stack = []          # [(tag, attrs_dict)]
        #: The stack AS IT WAS when this segment's text began. Capturing it at
        #: flush time loses every inline ancestor, because an inline end tag
        #: pops the stack without flushing - so a `<span class="q-version">`
        #: emitted its text with an EMPTY stack and the provenance skip could
        #: never see it.
        self._seg_stack = ()
        #: Classes seen ANYWHERE in the segment, not only at its first byte.
        #: An inline `<a class="toc-link">` opened mid-segment is still the
        #: container of the words it wraps, and a stack sampled once at the
        #: start cannot see it - which made every navigation and index row
        #: look like teaching.
        self._seg_classes = set()
        self._skip = 0
        self._line = 1
        #: A SERIAL per open element, parallel to `_stack`. Tag names cannot
        #: identify an element: two sibling `<div>`s both spell "div", so a
        #: heading's container looked identical to the next container along and
        #: a label leaked across a closed boundary. Serials are identity.
        self._serials = []
        self._seg_serials = ()
        self._next_serial = 0

    # -- helpers ---------------------------------------------------------
    def _flush(self):
        text = normalise("".join(self._buf))
        if text:
            self.segments.append(
                (text, self._seg_stack, self._line,
                 frozenset(self._seg_classes), self._seg_serials))
        self._buf = []
        self._seg_classes = set()

    def _open_block(self):
        self._flush()
        self._line = self.getpos()[0]

    # -- parser hooks ----------------------------------------------------
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in SKIP:
            self._skip += 1
            return
        d = {k.lower(): (v or "") for k, v in attrs}
        if tag in BREAK:
            self._flush()
            self._line = self.getpos()[0]
            return
        if tag not in INLINE:
            self._open_block()
        self._stack.append((tag, d))
        self._serials.append(self._next_serial)
        self._next_serial += 1
        self._seg_classes.update(d.get("class", "").split())

    def handle_startendtag(self, tag, attrs):
        if tag.lower() in BREAK:
            self._flush()
            self._line = self.getpos()[0]

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in SKIP:
            self._skip = max(0, self._skip - 1)
            return
        if tag not in INLINE and tag not in BREAK:
            self._flush()
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                del self._stack[i:]
                del self._serials[i:]
                break

    def handle_data(self, data):
        if self._skip:
            return
        if not self._buf:
            self._line = self.getpos()[0]
            self._seg_stack = tuple(self._stack)
            self._seg_serials = tuple(self._serials)
        self._buf.append(data)

    def close(self):
        super().close()
        self._flush()


def segments_ex(html: str):
    """[(text, stack, lineno, classes, serials)] - runs plus element identity.

    `serials` is one integer per open element, so two sibling `<div>`s are
    distinguishable. Callers that only need text and containers use
    `segments()`; only the label logic needs identity.
    """
    p = _Segmenter()
    try:
        p.feed(html)
        p.close()
    except Exception:                                    # noqa: BLE001
        # A malformed page must not blind a guard. Fall back to a whole-tag
        # strip so the text is still scanned, at coarser scope.
        return [(normalise(re.sub(r"<[^>]+>", " ", html)), (), 1,
                 frozenset(), ())]
    return p.segments


def segments(html: str):
    """[(text, stack, lineno, classes)] - normalised visible runs, in order."""
    return [(t, st, ln, cl) for t, st, ln, cl, _s in segments_ex(html)]


#: STAGE 1 - hard proposition boundaries. Sentence ends, bullets, semicolons,
#: and the SUBORDINATING conjunctions, which reliably start a new proposition
#: whatever precedes them.
#:
#: An em-dash aside is NOT a boundary. "Before 2025 the guidance was
#: region-locked - BMP5 for the Red Sea..." is one proposition, and splitting
#: it severed the historical framing from the clause it governs, reporting the
#: corpus's own supersession card as a defect.
_SENT = re.compile(
    r"(?<=[.;!?])\s+"
    r"|\s+[•·]\s+"
    r"|,?\s+(?:but|however|whereas|although|though|yet|while)\s+"
    r"|;\s*")

#: STAGE 2 - COORDINATED clauses (E1).
#:
#: "BMP5 replaced BMP4 and remains the current industry standard" is two
#: propositions and only the second is a defect, but `and` cannot simply be a
#: boundary: "BMP5 and BMP4 are historical predecessors" would then leave a
#: bare "BMP5" with nothing to deny it, and the guard would flag the corpus's
#: own history. So a coordinator splits ONLY where it joins two CLAUSES:
#:
#:   * the left side must already contain a finite verb, and
#:   * the right side must OPEN with one (optionally after a pronoun or an
#:     adverb such as "still" or "itself"), because a coordinated predicate
#:     shares its subject and therefore begins with the verb.
#:
#: A noun coordination fails both tests and is left intact. This is bounded
#: clause segmentation, not a parser - it decides one question only.
_VERB = (r"(?:is|are|was|were|be|been|being|remains?|remained|stays?|stayed|"
         r"continues?|continued|applies|apply|applied|refers?|refer|uses?|use|"
         r"used|requires?|required|provides?|gives?|serves?|governs?|covers?|"
         r"sets?|forms?|shall|should|must|may|can|will|would|has|have|had|"
         r"does|do|did|replaced?|replaces|supersede[sd]?|superseded|"
         r"describes?|states?|lists?)")
#: The coordinator is CONSUMED; the verb is only LOOKED AHEAD at, because it
#: belongs to the clause that follows and has to survive the split.
_ADV = (r"(?:it|they|this|these|those|itself|themselves|still|also|now|then|"
        r"therefore|thus|hence|nevertheless|nonetheless)")
_COORD = re.compile(
    r",?\s+(?:and|or|so|which|that)\s+(?=(?:%s\s+)?%s\b)" % (_ADV, _VERB),
    re.I)
_HAS_VERB = re.compile(r"\b%s\b" % _VERB, re.I)


def _split_coordinated(piece: str):
    """One hard proposition -> its coordinated clauses.

    A clause with no finite verb is not a proposition; it is the subject of the
    one after it, so it MERGES FORWARD. Without that rule a relative-clause
    split leaves a bare "BMP5" that no denial in the rest of the sentence can
    reach, and the guard reports history as a live claim.
    """
    parts, out, pending = [], [], ""
    last = 0
    for m in _COORD.finditer(piece):
        left = piece[last:m.start()]
        if not _HAS_VERB.search(left):
            continue                      # noun coordination - not a clause
        parts.append(left)
        last = m.end()
    parts.append(piece[last:])
    for part in parts:
        part = (pending + " " + part).strip() if pending else part.strip()
        if not part:
            continue
        if not _HAS_VERB.search(part) and part is not parts[-1]:
            pending = part               # verbless fragment: carry it forward
            continue
        pending = ""
        out.append(part)
    if pending:
        out.append(pending)
    return out or [piece.strip()]


def propositions(text: str):
    """[(clause, group)] - clauses, tagged with their hard-sentence group.

    The group matters because a SUBJECT carries across coordinated clauses of
    one sentence and no further: "BMP5 replaced BMP4 and remains current" is
    about BMP5 throughout, but the next sentence is a fresh subject.
    """
    out = []
    for g, piece in enumerate(s for s in _SENT.split(text) if s and s.strip()):
        for clause in _split_coordinated(piece.strip()):
            if clause:
                out.append((clause, g))
    return out


def sentences(text: str):
    """Bounded proposition units within one segment."""
    return [c for c, _g in propositions(text)]


#: Tags whose text LABELS the block that follows it (E4). Closed and
#: structural - a heading, a definition term, a table header, a caption.
HEADING_TAGS = frozenset(("h1", "h2", "h3", "h4", "h5", "h6",
                          "dt", "th", "caption", "legend", "summary"))

#: Classes that make a non-heading element behave as one on these pages.
HEADING_CLASSES = frozenset("""
cs-h cs-head cs-title dd-h dd-title sec-h sec-title kv-k label block-label
nc-title t-head topic-title
""".split())

#: How far a label reaches. Bounded by STRUCTURE first - a heading only labels
#: segments inside the element that contains it - and by this count second, so
#: a heading cannot lend its subject to the whole rest of a long container.
#: Deliberately NOT a character window: the +-220-character window is the
#: defect this replaces.
HEADING_REACH = 8


def _tags(stack):
    return tuple(t for t, _a in stack)


def _is_heading(stack, classes):
    if stack and stack[-1][0] in HEADING_TAGS:
        return True
    return bool(set(classes) & HEADING_CLASSES)


def segments_with_context(html: str):
    """segments(), each with the nearest STRUCTURALLY APPLICABLE label.

    A label applies to a later segment only while that segment is still inside
    the element that CONTAINS the label - compared by element identity, not by
    tag name - and only for HEADING_REACH segments. That is what makes
    `<h4>Fire main</h4><li>Minimum 0.27 MPa</li>` one claim while a heading in
    a sibling that has already CLOSED lends nothing.

    Identity is the whole point. Comparing tag names, two adjacent `<div>`s
    both read "div", so a label leaked across the boundary and the check that
    was supposed to forbid it passed for an unrelated reason.
    """
    out = []
    label = None                 # (text, parent_serials, segments_remaining)
    for text, stack, line, cls, serials in segments_ex(html):
        applies = None
        if label is not None:
            ltext, lparent, left = label
            if left > 0 and serials[:len(lparent)] == lparent:
                applies = ltext
                label = (ltext, lparent, left - 1)
            else:
                label = None
        out.append({"text": text, "stack": stack, "line": line,
                    "classes": cls, "label": applies})
        if _is_heading(stack, cls):
            label = (text, serials[:-1] if serials else (), HEADING_REACH)
    return out


def in_container(stack, *, tag=None, cls=None, ident=None) -> bool:
    """Is any ancestor a tag / class / id match?"""
    for t, attrs in stack:
        if tag and t != tag:
            continue
        if ident and attrs.get("id") != ident:
            continue
        if cls and cls not in attrs.get("class", ""):
            continue
        if tag or cls or ident:
            return True
    return False


def container_classes(stack):
    out = set()
    for _t, attrs in stack:
        out.update(attrs.get("class", "").split())
    return out
