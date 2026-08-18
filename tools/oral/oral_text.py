"""Meaning-preserving text handling for the Oral examiner matcher.

Phase 2A-i correctness floor. Three rules govern this module:

  1. An unknown token is not a typo. The 681 QB questions are a corpus, not a
     dictionary of valid English or valid maritime terminology. A missed
     misspelling costs one unmatched row; a silent "correction" changes what
     the examiner asked. Only verified source misspellings are repaired, from
     an explicit curated map.

  2. A load-bearing token is never rewritten. Digits, roman numerals,
     regulation and paragraph references, engine designators and alphanumeric
     standard identifiers carry the legal or technical meaning of the ask.
     ATTENDED is not UNATTENDED; III/16 is not III/6.

  3. A designator that changes the meaning must survive tokenisation and must
     stay distinguishable. ME-GI is not ME-GA; Annex I is not Annex VI;
     Form A is not Form B.

Portability: no paths, no I/O. Import-only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

# --------------------------------------------------------------------------
# designators
# --------------------------------------------------------------------------
# Alphanumeric designator written with an optional separator: A-60, D-1, G8,
# ISO 8217, Reg 13, III/2. Requires a digit, so it never fires on prose.
_DESIGNATOR = re.compile(r"\b([a-z]{1,4})[\s\-/]?(\d{1,4})\b")

# Roman numerals used as designators. Kept as a token in their own right, and
# mapped to arabic only inside a keyword designator slot (Annex VI == Annex 6),
# never globally - a bare "v" in prose is not the number five.
_ROMAN = {"i": "1", "ii": "2", "iii": "3", "iv": "4", "v": "5", "vi": "6",
          "vii": "7", "viii": "8", "ix": "9", "x": "10", "xi": "11", "xii": "12"}

# An ALL-CAPS hyphen/slash group is a technical designator; a lower-case one is
# ordinary English. That single distinction is what lets ME-GI and ME-GA
# survive while "well-founded" and "state-of-the-art" tokenise as prose.
_CAPS_DESIGNATOR = re.compile(r"\b([A-Z][A-Z0-9]*(?:[-/][A-Z0-9]+)+)\b")

# Keyword + designator slot. The keyword is what makes a bare "I", "A" or "6"
# a designator rather than a pronoun, an article or a loose number.
_SLOT_KEYWORD = ("annex", "form", "part", "type", "class", "table", "appendix",
                 "schedule", "chapter", "grade", "category", "tier", "section",
                 "regulation", "reg", "division", "stage")
_KEYWORD_DESIGNATOR = re.compile(
    r"\b(%s)\s+((?:[IVX]{1,4}|[A-Z]|\d{1,4}[A-Z]?)(?:[-/]\d{1,3})?)\b"
    % "|".join(_SLOT_KEYWORD),
    re.I,
)

# An ALL-CAPS letter run is an identifier, not prose. This is what lets the
# source's unhyphenated "MEGI"/"MEGA" meet MIW's own "ME-GI"/"ME-GA", which are
# emitted with their separators stripped as well. It fires only on mixed-case
# text: in a sentence typed entirely in capitals, case carries no information,
# and applying it there would make an all-caps source row score against a
# mixed-case corpus row on a signal neither of them really sent.
_ACRONYM = re.compile(r"\b([A-Z]{2,8})\b")

# A bare alphanumeric identifier written without a separator: G8, G9, A60, D1.
# Emitted in the same alpha/digit shape as its hyphenated spelling, so G8 and G9
# share a family and read as a conflict, and A60 meets A-60.
_BARE_IDENTIFIER = re.compile(r"\b([A-Za-z]{1,4})(\d{1,4})\b")

_DESIG_PREFIX = "dsg:"


def _slot_value(raw):
    """Canonical value of a keyword designator slot: VI, vi and 6 all -> 6."""
    v = raw.lower().replace("/", "-")
    head, _, tail = v.partition("-")
    head = _ROMAN.get(head, head)
    return head + ("-" + tail if tail else "")


def designators(s):
    """Designator tokens read from the ORIGINAL text, before normalisation.

    Emitted with a `dsg:` prefix so a designator can never collide with an
    ordinary word (ME-GA must not equal the English "mega"), and with the
    separator kept, so ME-GI and ME-GA share a family key and read as a
    conflict rather than as two unrelated tokens.
    """
    if not s:
        return set()
    txt = str(s)
    out = set()
    for m in _CAPS_DESIGNATOR.finditer(txt):
        body = re.sub(r"[^a-z0-9-]", "", m.group(1).lower().replace("/", "-"))
        out.add(_DESIG_PREFIX + body)
        joined = body.replace("-", "")
        if joined != body:
            out.add(_DESIG_PREFIX + joined)   # ME-GI meets an unhyphenated MEGI
    for m in _BARE_IDENTIFIER.finditer(txt):
        out.add(_DESIG_PREFIX + m.group(1).lower() + "-" + m.group(2))
    if txt != txt.upper():
        for m in _ACRONYM.finditer(txt):
            out.add(_DESIG_PREFIX + m.group(1).lower())
    for m in _KEYWORD_DESIGNATOR.finditer(txt):
        out.add(_DESIG_PREFIX + m.group(1).lower() + "-" + _slot_value(m.group(2)))
    return out


def mtokens(s):
    """Matching tokens: prose tokens plus surviving technical designators.

    Designators are additive. The prose pass is unchanged, so every designator
    the audit already handled (A-60, D-1/D-2, G8/G9, III/1 vs III/2, ISO 8217,
    Reg 13, II-1) keeps its existing token; letter-suffix and keyword-slot
    designators gain one they never had.
    """
    n = L.norm(s)
    n = _DESIGNATOR.sub(lambda m: m.group(1) + m.group(2), n)
    out = designators(s)
    for t in n.split():
        if t in L.STOP:
            continue
        if t.isdigit():
            out.add(t)
        elif t.isalpha():
            if len(t) > 2:
                out.add(t)
            elif t in _ROMAN:
                out.add(t)
        else:
            out.add(t)
    return out


def designator_conflict(a_tokens, b_tokens):
    """True when both sides name the SAME designator family with a DIFFERENT
    value - Annex I against Annex VI, D-1 against D-2, ME-GI against ME-GA.

    Silence is not conflict: a side that names no designator never conflicts.
    """
    def by_family(toks):
        fam = {}
        for t in toks:
            if not str(t).startswith(_DESIG_PREFIX):
                continue
            body = str(t)[len(_DESIG_PREFIX):]
            key, sep, val = body.partition("-")
            fam.setdefault(key if sep else _family_of(body), set()).add(
                val if sep else body)
        return fam

    fa, fb = by_family(a_tokens), by_family(b_tokens)
    for key in set(fa) & set(fb):
        if not (fa[key] & fb[key]):
            return True
    return False


_FAMILY_SPLIT = re.compile(r"^([a-z]+)(\d.*)$")


def _family_of(body):
    """Family key for a separator-less designator: me-gi -> megi has no split,
    so fall back on the alpha prefix of an alphanumeric identifier (d1 -> d)."""
    m = _FAMILY_SPLIT.match(body)
    return m.group(1) if m else body


# --------------------------------------------------------------------------
# load-bearing tokens
# --------------------------------------------------------------------------
def is_load_bearing(tok):
    """A token whose exact form carries technical, legal or regulatory meaning.

    General rule, not a list of examples: anything carrying a digit, anything
    that is a roman numeral, and anything that survived as a designator or a
    joined alphanumeric identifier. Such a token is never rewritten.
    """
    if not tok:
        return False
    t = str(tok)
    if t.startswith(_DESIG_PREFIX):
        return True
    if any(c.isdigit() for c in t):
        return True
    if t.lower() in _ROMAN:
        return True
    if not t.isalpha():          # joined / punctuated identifier
        return True
    return False


# --------------------------------------------------------------------------
# spell repair - curated only
# --------------------------------------------------------------------------
# Verified misspellings observed in the candidate-typed source compilation.
# Every entry is a token that is not a word in any language of this domain, and
# whose intended spelling is unambiguous from its own record. Nothing is
# inferred from proximity to the QB vocabulary: the speculative nearest-corpus-
# token repairer this replaces produced attended->unattended,
# convinced->convicted, provident->provide, and92->and9, stcw5->stcw15 and
# iii16->iii6 alongside its genuine fixes.
SOURCE_TYPO_MAP = {
    "ammendment": "amendment",
    "ammendments": "amendments",
    "approvel": "approval",
    "chosed": "chose",
    "comercial": "commercial",
    "costal": "coastal",
    "coverd": "covered",
    "deligation": "delegation",
    "diffence": "difference",
    "eletrical": "electrical",
    "emmision": "emission",
    "emmission": "emission",
    "fullfill": "fulfill",
    "johri": "johari",
    "lastest": "latest",
    "mannanging": "managing",
    "motivaton": "motivation",
    "personm": "personam",
    "safties": "safeties",
    "sturucture": "structure",
    "techiniques": "techniques",
    "wellfare": "welfare",
}


def repair(tok):
    """Return (token, note). A token is repaired only when it is a curated,
    verified source misspelling AND is not load-bearing."""
    if is_load_bearing(tok):
        return tok, None
    fixed = SOURCE_TYPO_MAP.get(tok)
    if not fixed or fixed == tok:
        return tok, None
    return fixed, "%s->%s" % (tok, fixed)


def repair_tokens(raw_tokens):
    """Repair a token set deterministically.

    Iteration is over sorted input and the note list is sorted, so the recorded
    repairs do not vary with set-iteration order between runs.
    """
    out, notes = set(), []
    for t in sorted(raw_tokens):
        fixed, note = repair(t)
        out.add(fixed)
        if note:
            notes.append(note)
    return out, sorted(notes)
