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

    # -- helpers ---------------------------------------------------------
    def _flush(self):
        text = normalise("".join(self._buf))
        if text:
            self.segments.append(
                (text, self._seg_stack, self._line, frozenset(self._seg_classes)))
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
                break

    def handle_data(self, data):
        if self._skip:
            return
        if not self._buf:
            self._line = self.getpos()[0]
            self._seg_stack = tuple(self._stack)
        self._buf.append(data)

    def close(self):
        super().close()
        self._flush()


def segments(html: str):
    """[(text, stack, lineno, classes)] - normalised visible runs, in order."""
    p = _Segmenter()
    try:
        p.feed(html)
        p.close()
    except Exception:                                    # noqa: BLE001
        # A malformed page must not blind a guard. Fall back to a whole-tag
        # strip so the text is still scanned, at coarser scope.
        return [(normalise(re.sub(r"<[^>]+>", " ", html)), (), 1, frozenset())]
    return p.segments


#: Sentence-ish split. Bullets and semicolons separate propositions as surely
#: as full stops do on these pages, and an em-dash aside is its own clause.
#: Sentence AND clause boundaries. "BMP5 replaced BMP4, but BMP5 is what we
#: use today" is two propositions in one sentence, and only the second is a
#: defect - so a coordinating conjunction has to end a proposition, or a
#: historical first clause silences a live second one.
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


def sentences(text: str):
    """Bounded proposition units within one segment."""
    return [s.strip() for s in _SENT.split(text) if s and s.strip()]


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
