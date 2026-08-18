"""Oral Notes as a SECONDARY coverage and examiner-evidence layer.

Phase 2A-ii. The QB answers "what is our canonical question?"; the Notes answer
"what else does MIW already know?". Those are different questions and this
module keeps them apart:

  1. A Notes relation is never a canonical relation. Notes support is graded on
     its own vocabulary (NOTES_*), never EXACT_MATCH / NEAR_MATCH /
     SAME_CORE_ASK, and no Notes unit can become a canonical QB question id.

  2. Section-level evidence only. A page is not a unit. "Tug Girding -
     Capsizing Risk" is one retrievable unit; `simon-notes-p2.html` is not.
     Whole-page similarity is never computed, because a 116 KB page mentions
     everything and would rescue every ask put to it.

  3. A name is not an examiner. `Nairobi Convention` is not Nair, `John Doe
     v. The Motor Vessel Olympic Prometheus` is not an examiner called John,
     and `USS John S. McCain` is a ship. An explicit cue needs an ask, a
     recognised alias, and the absence of a non-examiner context.

Portability: the repo root comes from oral_lib, never a drive letter.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
import oral_text as T  # noqa: E402

NOTES_DIR = L.MEO / "oralnotes"

# --------------------------------------------------------------------------
# file classification
# --------------------------------------------------------------------------
# The two manifests in the notes folder are the governed statement of what each
# series is; they are read rather than re-derived, so a page cannot silently
# change series. Anything they do not claim is excluded from the semantic
# universe and recorded as such.
NOTES_MANIFEST = NOTES_DIR / "notes_content_index.json"
WRITTEN_MANIFEST = NOTES_DIR / "written_content_index.json"

# Pages that exist to route a reader, not to teach. Their rows are links into
# other pages; ingesting them as content would let a table of contents rescue
# an ask that the page it points at does not actually answer.
NAVIGATION_PAGES = {
    "index.html": "series landing page - cards generated from the manifest",
    "notes-master-index.html": "Simon notes x QB cross-reference table",
    "uday-index-crossref.html": "source-book index to MIW notes cross-reference",
}

# Written-exam product that happens to sit in the same folder. Different
# product surface, and structurally not notes: no note unit container of any
# dialect appears in either file.
OUT_OF_SCOPE_PAGES = {
    "solved-qp-january-2026-full.html": "Written QI solved paper, not an Oral Note",
    "written-sample-january-2026.html": "Written QI sample paper, not an Oral Note",
}

SERIES_SIMON = "SIMON_ORAL_NOTES"
SERIES_MGMT = "ENGINEERING_MANAGEMENT_NOTES"
SERIES_CURRENT = "CURRENT_TOPICS"
SERIES_WA = "WRITTEN_ANSWER_SERIES"

ROLE_SUBSTANTIVE = "SUBSTANTIVE_NOTES"
ROLE_NAVIGATION = "NAVIGATION_INDEX"
ROLE_OUT_OF_SCOPE = "OUT_OF_SCOPE_WRITTEN_SAMPLE"
ROLE_UNCLASSIFIED = "UNCLASSIFIED"

SERIES_CODE = {SERIES_SIMON: "SIMON", SERIES_MGMT: "MGMT",
               SERIES_CURRENT: "CURR", SERIES_WA: "WA"}

_MANIFEST_SERIES = {
    "simon-notes": SERIES_SIMON,
    "engineering-management-notes": SERIES_MGMT,
    "current-topics": SERIES_CURRENT,
}


def _manifest_files(path):
    """file name -> manifest series key, in a stable order."""
    if not path.exists():
        return {}
    d = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for skey in sorted(d.get("series", {})):
        files = d["series"][skey].get("files", {})
        names = sorted(files) if isinstance(files, dict) else []
        for n in names:
            out[n] = skey
    return out


def classify_files():
    """Every HTML page in the notes folder, with its series and its role."""
    notes_map = _manifest_files(NOTES_MANIFEST)
    written_map = _manifest_files(WRITTEN_MANIFEST)
    rows = []
    for p in sorted(NOTES_DIR.glob("*.html")):
        n = p.name
        # Measured on LF-normalised bytes, not on stat().st_size. These pages
        # are text with `* text=auto` and `*.html text eol=lf`, so a working
        # tree checked out on Windows can hold CRLF while the committed blob
        # holds LF. Recording the on-disk size therefore wrote a number that
        # differed between two checkouts of the same commit - the same class of
        # defect as the absolute path Phase 2A-i removed from a committed
        # artefact, and found the same way, by running the gate from a fresh
        # worktree on another drive.
        size = len(p.read_bytes().replace(b"\r\n", b"\n"))
        if n in NAVIGATION_PAGES:
            row = (None, ROLE_NAVIGATION, NAVIGATION_PAGES[n])
        elif n in OUT_OF_SCOPE_PAGES:
            row = (None, ROLE_OUT_OF_SCOPE, OUT_OF_SCOPE_PAGES[n])
        elif n in notes_map:
            row = (_MANIFEST_SERIES[notes_map[n]], ROLE_SUBSTANTIVE,
                   "claimed by notes_content_index.json")
        elif n in written_map:
            row = (SERIES_WA, ROLE_SUBSTANTIVE,
                   "claimed by written_content_index.json")
        else:
            row = (None, ROLE_UNCLASSIFIED, "no manifest claims this page")
        rows.append({"file": n, "series": row[0], "role": row[1],
                     "reason": row[2], "bytes": size})
    return rows


# --------------------------------------------------------------------------
# markup handling
# --------------------------------------------------------------------------
# Site chrome carries no teaching content. Scripts (including the analytics and
# auth-gate blocks), styles, inline SVG, nav and footer are removed before any
# unit is read, so none of it can reach a coverage score or an examiner cue.
_CHROME = re.compile(
    r"<(script|style|svg|nav|footer|head)\b[^>]*>.*?</\1>", re.S | re.I)
_NOTE_CHROME = re.compile(
    r'<(div|span)\s+class="(?:note-footer|correction-link|note-version|toc'
    r'|toc-link|breadcrumb|site-footer|legal|nav-chain)"[^>]*>.*?</\1>',
    re.S | re.I)


def page_text(html):
    """Page markup with site chrome removed."""
    return _NOTE_CHROME.sub(" ", _CHROME.sub(" ", html))


_OPEN_DIV = re.compile(r"<div\b", re.I)
_CLOSE_DIV = re.compile(r"</div>", re.I)


def div_block(html, start):
    """Text of the <div> starting at `start`, balanced over nested divs.

    A note unit contains nested divs, so a non-greedy `</div>` match truncates
    every unit at its first inner element. Depth is tracked explicitly.
    """
    depth = 0
    i = start
    n = len(html)
    while i < n:
        o = _OPEN_DIV.search(html, i)
        c = _CLOSE_DIV.search(html, i)
        if c is None:
            return html[start:]
        if o is not None and o.start() < c.start():
            depth += 1
            i = o.end()
        else:
            depth -= 1
            i = c.end()
            if depth == 0:
                return html[start:i]
    return html[start:]


def _attr(tag, name):
    m = re.search(r'\b%s="([^"]*)"' % name, tag)
    return m.group(1) if m else ""


def _first(pattern, block, flags=re.S | re.I):
    m = re.search(pattern, block, flags)
    return L.strip_tags(m.group(1)) if m else ""


def slug(s, limit=44):
    s = re.sub(r"[^a-z0-9]+", "-", L.norm(s)).strip("-")
    return (s[:limit].strip("-") or "unit").upper()


# --------------------------------------------------------------------------
# unit extraction
# --------------------------------------------------------------------------
LEVEL_NOTE_CARD = "NOTE_CARD"     # a Simon note card - one topic, one ask
LEVEL_TOPIC = "TOPIC"             # a management topic block / WA section
LEVEL_QA = "QA"                   # one oral question and its answer
LEVEL_EXAM_Q = "EXAM_Q"           # a written-exam prompt: a question, not an answer

UNIT_LEVELS = {LEVEL_NOTE_CARD, LEVEL_TOPIC, LEVEL_QA, LEVEL_EXAM_Q}


def _reg_codes(block):
    return sorted({L.strip_tags(m) for m in re.findall(
        r'<span class="reg-code">(.*?)</span>', block, re.S | re.I)})


def _body_of(block, opener):
    m = re.search(opener, block, re.I)
    return div_block(block, m.start()) if m else block


def _simon_units(html):
    """simon-notes-pN: one unit per note card."""
    out = []
    for m in re.finditer(r'<div class="note-card"([^>]*)>', html, re.I):
        block = div_block(html, m.start())
        out.append({
            "level": LEVEL_NOTE_CARD,
            "anchor": _attr(m.group(1), "id"),
            "anchor_authored": bool(_attr(m.group(1), "id")),
            "page_badge": _first(r'<span class="page-badge">(.*?)</span>', block),
            "title": _first(
                r'<div class="note-title"[^>]*>(.*?)(?:<div class="note-subtitle"|</div>)',
                block),
            "subtitle": _first(r'<div class="note-subtitle">(.*?)</div>', block),
            "keywords": _attr(m.group(1), "data-kw"),
            "body": L.strip_tags(_body_of(block, r'<div class="note-body">')),
            "reg_codes": _reg_codes(block),
            "answer_bearing": True,
            "raw": block,
            "children": [],
        })
    return out


def _qa_children(block):
    out = []
    for qm in re.finditer(
            r'<div class="qa-item"[^>]*>\s*<div class="qa-q">(.*?)</div>\s*'
            r'<div class="qa-a">(.*?)</div>\s*</div>', block, re.S | re.I):
        q = L.strip_tags(qm.group(1))
        a = L.strip_tags(qm.group(2))
        if not q:
            continue
        out.append({"level": LEVEL_QA, "title": q, "body": a,
                    "raw": qm.group(0), "answer_bearing": bool(a)})
    return out


_MARKS = re.compile(r'<span class="marks(?:-badge)?">(.*?)</span>', re.S | re.I)


def _exam_children(block):
    out = []
    for em in re.finditer(r'<div class="exam-q"[^>]*>', block, re.I):
        raw = div_block(block, em.start())
        # The two dialects differ: the management pages put the prompt directly
        # in the exam-q div, the WA pages nest it in a q-text child. Reading the
        # div flat would prefix every WA prompt with its marks badge, so the
        # badge is lifted out and the nested prompt preferred where present.
        inner = _first(r'<div class="q-text"[^>]*>(.*?)</div>', raw)
        marks = _first(r'<span class="marks(?:-badge)?">(.*?)</span>', raw)
        t = inner or L.strip_tags(_MARKS.sub(" ", raw))
        if not t:
            continue
        # A written-exam prompt states an ask; it does not answer one. It can
        # evidence that MIW knows a topic is examinable, never that MIW holds
        # the answer, so it is recorded with answer_bearing False.
        out.append({"level": LEVEL_EXAM_Q, "title": t, "body": "",
                    "raw": raw, "page_badge": marks, "answer_bearing": False})
    return out


def _with_children(parent, block):
    for child in _qa_children(block) + _exam_children(block):
        child.setdefault("page_badge", parent["page_badge"])
        # A child keeps its OWN markup. Handing it the parent's block made every
        # Q&A item claim the whole topic as its cue scope, which counted each
        # examiner cue once per sibling - 158 Nair hits on a page holding 17.
        child.update({"anchor": parent["anchor"],
                      "anchor_authored": parent.get("anchor_authored", False),
                      "keywords": parent["keywords"],
                      "subtitle": parent["title"],
                      "reg_codes": _reg_codes(child.get("raw", "")),
                      "children": []})
        parent["children"].append(child)
    return parent


def _mgmt_units(html):
    """miw-notes-mgmt-pN: one unit per topic block, plus its Q&A children."""
    out = []
    for m in re.finditer(r'<div class="topic-block"([^>]*)>', html, re.I):
        block = div_block(html, m.start())
        parent = {
            "level": LEVEL_TOPIC,
            "anchor": _attr(m.group(1), "id"),
            "anchor_authored": bool(_attr(m.group(1), "id")),
            "page_badge": _first(r'<span class="topic-pages?">(.*?)</span>', block),
            "title": _first(r'<h2 class="topic-title">(.*?)</h2>', block),
            "subtitle": "",
            "keywords": _attr(m.group(1), "data-kw"),
            "body": L.strip_tags(block),
            "reg_codes": _reg_codes(block),
            "answer_bearing": True,
            "raw": block,
            "children": [],
        }
        out.append(_with_children(parent, block))
    return out


def _wa_units(html):
    """WA*: one unit per section heading run, plus its exam prompts."""
    out = []
    heads = list(re.finditer(r'<h2 class="section-h"([^>]*)>(.*?)</h2>',
                             html, re.S | re.I))
    # Each WA page opens with its headline written question above the first
    # section heading. Starting at heads[0] silently dropped it - one prompt per
    # WA page, and the most important one on the page.
    spans = []
    if heads:
        lead = html[:heads[0].start()]
        if re.search(r'<div class="exam-q"', lead, re.I):
            spans.append(("lead", _first(r"<h1[^>]*>(.*?)</h1>", html)
                          or "Headline written question", lead))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(html)
        spans.append((_attr(m.group(1), "id") or "sec-%d" % (i + 1),
                      L.strip_tags(m.group(2)), html[m.start():end]))
    for anchor, title, block in spans:
        parent = {
            "level": LEVEL_TOPIC,
            "anchor": anchor,
            "anchor_authored": anchor not in ("lead",) and not anchor.startswith("sec-"),
            "page_badge": "",
            "title": title,
            "subtitle": "",
            "keywords": "",
            "body": L.strip_tags(block),
            "reg_codes": _reg_codes(block),
            "answer_bearing": True,
            "raw": block,
            "children": [],
        }
        out.append(_with_children(parent, block))
    return out


def _current_units(html):
    """current-topics-pN: one unit per numbered question block."""
    out = []
    heads = list(re.finditer(r'<div class="q-text"[^>]*>(.*?)</div>', html, re.S | re.I))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(html)
        block = html[m.start():end]
        out.append({
            "level": LEVEL_TOPIC,
            "anchor": "q-%d" % (i + 1),
            "anchor_authored": False,
            "page_badge": "",
            "title": L.strip_tags(m.group(1)),
            "subtitle": "",
            "keywords": " ".join(sorted({L.strip_tags(t) for t in re.findall(
                r'<span class="q-tag">(.*?)</span>', block, re.S | re.I)})),
            "body": L.strip_tags(block),
            "reg_codes": _reg_codes(block),
            "answer_bearing": True,
            "raw": block,
            "children": [],
        })
    return out


DIALECT = {
    SERIES_SIMON: _simon_units,
    SERIES_MGMT: _mgmt_units,
    SERIES_WA: _wa_units,
    SERIES_CURRENT: _current_units,
}


# --------------------------------------------------------------------------
# unit identity
# --------------------------------------------------------------------------
# A note unit id must never be mistakable for a canonical QB question id.
# Canonical ids are `QB<n>_<L>#q<n>`; note ids carry the NOTE- prefix and no
# `#`, and `is_canonical_shaped` is asserted against every emitted id.
NOTE_ID_PREFIX = "NOTE-"
_CANONICAL_SHAPE = re.compile(r"^QB\d+[_A-Z]*#q\d+$", re.I)


def is_canonical_shaped(unit_id):
    """True when an id could be read as a canonical QB question id."""
    return bool(_CANONICAL_SHAPE.match(str(unit_id))) or "#" in str(unit_id)


def _page_code(fname):
    stem = Path(fname).stem
    m = re.search(r"p(\d+)$", stem)
    if m:
        return "P" + m.group(1)
    return slug(stem, 18)


def make_unit_id(series, fname, anchor, title, level, ordinal):
    """Deterministic, file-and-section derived. The ordinal disambiguates only;
    it is never the sole source of identity, because Simon pages reuse an
    anchor id across two elements."""
    parts = [NOTE_ID_PREFIX.rstrip("-"), SERIES_CODE.get(series, "NOTE"),
             _page_code(fname), (anchor or "x").upper().replace("#", ""),
             level[:2], "%03d" % ordinal, slug(title, 32)]
    return "-".join(p for p in parts if p)


_CHILD_CONTAINER = re.compile(r'<div class="(?:qa-item|exam-q)"[^>]*>', re.I)


def _cue_html(u):
    """The markup a unit may claim a cue from.

    A topic block contains its own Q&A children, so scanning the block whole
    would count every child's cue twice - once for the child and once for the
    parent. A parent's cue scope is its block with the child containers
    removed; a child's scope is its own text.
    """
    raw = u.get("raw", "")
    if not u.get("children"):
        return raw
    out, i = [], 0
    for m in _CHILD_CONTAINER.finditer(raw):
        if m.start() < i:
            continue
        out.append(raw[i:m.start()])
        i = m.start() + len(div_block(raw, m.start()))
    out.append(raw[i:])
    return "".join(out)


_TIP = re.compile(r'<div class="(?:simon-tip|ce-tip)"[^>]*>', re.I)


def cue_scopes(unit):
    """(text, in_tip, in_heading) spans a cue may be read from, in a stable
    order. Tip blocks are separated from surrounding prose so a structured
    examiner tip is distinguishable from an incidental mention."""
    html = unit.get("cue_html", "")
    tips, rest, i = [], [], 0
    for m in _TIP.finditer(html):
        if m.start() < i:
            continue
        block = div_block(html, m.start())
        rest.append(html[i:m.start()])
        tips.append(L.strip_tags(block))
        i = m.start() + len(block)
    rest.append(html[i:])
    spans = [(t, True, False) for t in tips]
    head = " ".join(x for x in (unit.get("section_title", ""),
                                unit.get("section_subtitle", "")) if x)
    if head:
        spans.append((head, False, True))
    spans.append((L.strip_tags("".join(rest)), False, False))
    return [(t, a, b) for t, a, b in spans if t.strip()]


def build_units(keep_html=False):
    """Every note unit in the substantive pages, in a stable order."""
    units = []
    for row in classify_files():
        if row["role"] != ROLE_SUBSTANTIVE:
            continue
        series, fname = row["series"], row["file"]
        html = page_text((NOTES_DIR / fname).read_text(
            encoding="utf-8", errors="replace"))
        ordinal = 0
        for parent in DIALECT[series](html):
            flat = [parent] + parent.get("children", [])
            parent_id = None
            for u in flat:
                ordinal += 1
                uid = make_unit_id(series, fname, u.get("anchor", ""),
                                   u.get("title", ""), u["level"], ordinal)
                if u is parent:
                    parent_id = uid
                rec = {
                    "note_unit_id": uid,
                    "parent_unit_id": None if u is parent else parent_id,
                    "file": fname,
                    "series": series,
                    "url": "/meoclass1/oralnotes/" + fname +
                           ("#" + u["anchor"] if u.get("anchor") else ""),
                    "anchor": u.get("anchor", ""),
                    "anchor_authored": bool(u.get("anchor_authored")),
                    "unit_level": u["level"],
                    "page_badge": u.get("page_badge", ""),
                    "section_title": u.get("title", ""),
                    "section_subtitle": u.get("subtitle", ""),
                    "keywords": u.get("keywords", ""),
                    "text": u.get("body", ""),
                    "reg_codes": u.get("reg_codes", []),
                    "answer_bearing": bool(u.get("answer_bearing")),
                    "text_chars": len(u.get("body", "")),
                }
                if keep_html:
                    rec["cue_html"] = _cue_html(u)
                units.append(rec)
    return units


# --------------------------------------------------------------------------
def harvest_cues(alias_map):
    """Every alias occurrence in every note unit, classified.

    Returns (cues, raw_counts). `raw_counts` records the unbounded substring
    hit count beside the word-bounded one, because the gap between them is a
    real defect class: 79 of 246 literal "Nair" hits in the Notes are
    "Nairobi", a convention rather than an examiner.
    """
    cues, raw_counts = [], {}
    for canon in sorted(alias_map):
        raw_counts[canon] = {"substring_hits": 0, "word_bounded_hits": 0}
    for unit in build_units(keep_html=True):
        for text, in_tip, in_heading in cue_scopes(unit):
            for canon in sorted(alias_map):
                for form in alias_map[canon]:
                    raw_counts[canon]["substring_hits"] += len(
                        re.findall(re.escape(form), text))
                    for m in re.finditer(r"\b%s\b" % re.escape(form), text):
                        raw_counts[canon]["word_bounded_hits"] += 1
                        disp, control, window = classify_cue(
                            text, m.start(), m.end(), form, in_tip, in_heading)
                        cues.append({
                            "note_unit_id": unit["note_unit_id"],
                            "file": unit["file"],
                            "series": unit["series"],
                            "url": unit["url"],
                            "anchor": unit["anchor"],
                            "unit_level": unit["unit_level"],
                            "section_title": unit["section_title"],
                            "examiner": canon,
                            "matched_form": form,
                            "cue_disposition": disp,
                            "non_examiner_control": control,
                            "cue_vehicle": (
                                "STRUCTURED_ATTRIBUTION"
                                if is_role_labelled(text, m.start()) else
                                "STRUCTURED_TIP" if in_tip else
                                "HEADING" if in_heading else "PROSE"),
                            "evidence_excerpt": re.sub(
                                r"\s+", " ", window).strip()[:320],
                            "char_offset": m.start(),
                        })
    for canon in raw_counts:
        c = raw_counts[canon]
        c["suppressed_by_word_boundary"] = (
            c["substring_hits"] - c["word_bounded_hits"])
    return cues, raw_counts


# --------------------------------------------------------------------------
# examiner cues
# --------------------------------------------------------------------------
# A cue disposition says what kind of examiner claim a Note makes. Only the
# three EXPLICIT ones are evidence; the rest are recorded so the count can be
# audited, and are excluded from the evidence ledger. Nothing here is stronger
# than NOTE_EXPLICIT: a Note is a Note, never the tracker.
CUE_PRIMARY_ASK = "NOTE_EXPLICIT_PRIMARY_ASK"
CUE_FOLLOWUP = "NOTE_EXPLICIT_FOLLOWUP"
CUE_EXPECTED_DETAIL = "NOTE_EXPLICIT_EXPECTED_DETAIL"
CUE_HEADING_CONTEXT = "NOTE_HEADING_CONTEXT"
CUE_WEAK_MENTION = "NOTE_WEAK_MENTION"
CUE_NON_EXAMINER = "NON_EXAMINER_NAME"

CUE_DISPOSITIONS = {CUE_PRIMARY_ASK, CUE_FOLLOWUP, CUE_EXPECTED_DETAIL,
                    CUE_HEADING_CONTEXT, CUE_WEAK_MENTION, CUE_NON_EXAMINER}

# The dispositions that may carry the NOTE_EXPLICIT evidence tier. A heading
# mention, an incidental mention and a non-examiner name are not evidence that
# anyone asked anything.
EXPLICIT_CUES = {CUE_PRIMARY_ASK, CUE_FOLLOWUP, CUE_EXPECTED_DETAIL}

NOTE_EVIDENCE_TIER = "NOTE_EXPLICIT"
NOTE_SOURCE_TYPE = "ORAL_NOTE_PAGE"

# Honorifics attach to a person without changing who they are, so they never
# make a bare alias into a longer proper name.
_HONORIFIC = {"Sir", "Capt", "Capt.", "Captain", "Mr", "Mr.", "Sr", "Sr.",
              "Shri", "Sri"}

# Non-examiner controls. Each names the rule that fired, so a suppressed hit is
# auditable rather than silently dropped.
CONTROL_LONGER_NAME = "ALIAS_ABSORBED_INTO_LONGER_PROPER_NAME"
CONTROL_SHIP = "SHIP_NAME"
CONTROL_CASE = "LEGAL_CASE_PARTY"
CONTROL_AUTHOR = "AUTHOR_OR_COMPILER_ATTRIBUTION"
CONTROL_SUBSTRING = "SUBSTRING_OF_A_LARGER_WORD"

_SHIP_PREFIX = re.compile(
    r"\b(USS|USNS|HMS|RMS|MV|MT|SS|M/V|M/T|MSC|OOCL|EVER)\s*$", re.I)

# A case party, structurally: the alias sits on one side of a citation "v.".
# The looser reading - any nearby "vs", "in rem", "defendant" - suppressed real
# cues, because this domain compares things constantly: "Bunker Convention 2001
# vs. CLC 92", "Audit vs Survey", "Double Class vs Dual Class". Comparison is
# not litigation.
_CASE_AFTER = re.compile(r"^\s*(?:[A-Z][A-Za-z.]*\s+){0,2}v\.?\s+[A-Z]")
_CASE_BEFORE = re.compile(r"\bv\.?\s+(?:[A-Z][A-Za-z.]*\s+){0,2}$")

_AUTHOR_MARKER = re.compile(
    r"\b(compiled by|prepared by|transcribed by|written by|authored by|"
    r"originally by|et al\.?|courtesy of)\b", re.I)

# A structured examiner field states outright who examines the topic:
# "Examiner: Nair", "Examiner: Nair / Paul", "CE Oral Tip (Senthil)". It is an
# explicit examiner label, and it must outrank the negative heuristics - the
# capitalised word after such a field is a frequency badge ("Nair Medium
# Frequency"), not a surname, and suppressing it discarded real evidence.
_ROLE_MARKER = re.compile(
    r"(?:examiners?|surveyor|asked by|oral tip|tip)\s*[:\-–—(/]?\s*"
    r"(?:[A-Z][a-z]+\s*[/&,]\s*)*$", re.I)

# Ask evidence, bound to the name. "Bound" means the verb sits in the short span
# that follows the alias, so a page that names an examiner in one sentence and
# uses the word "asks" three sentences later never becomes an explicit cue.
_BIND = r"(?:'s|s')?\s*(?:Sir|sir)?[^.!?;]{0,48}?"
_ASK_VERB = (r"asks?|asked|asking|examines?|tests?|probes?|quizzes|grills|"
             r"questions|enquires|inquires")
_ASK_NOUN = (r"trap|favourite|favorite|classic|phrasing|tell-tale|telltale|"
             r"question|line of questioning|high-yield|opener|starter")
_FOLLOWUP_MARKER = (r"may then ask|then asks?|may also ask|also asks?|"
                    r"follow-?up|follows? up|further asks?|escalation|"
                    r"escalates|cross-question|next asks?|second question")
_EXPECT_MARKER = (r"expects?|wants?|looking for|insists?|requires? you|"
                  r"emphasis|wants? you to|expected answer")


def _bound(pattern, window, name):
    return re.search(r"\b%s\b%s\b(?:%s)\b" % (re.escape(name), _BIND, pattern),
                     window, re.I | re.S) is not None


def examiner_aliases(alias_register):
    """canonical name -> the literal forms that name that examiner.

    Surname resemblance never merges two people, so only the register's own
    observed forms are used, reduced to the distinct name tokens.
    """
    out = {}
    for e in alias_register["examiners"]:
        canon = e["canonical_name"]
        forms = {canon}
        for f in e.get("observed_forms") or []:
            f = re.sub(r"\((?:[^)]*)\)", " ", f)
            for tok in re.findall(r"[A-Za-z]{3,}", f):
                if tok in _HONORIFIC or tok.lower() in ("capt", "sir"):
                    continue
                if tok.lower() == canon.lower():
                    forms.add(tok)
        out[canon] = sorted(forms)
    return out


def is_role_labelled(text, start):
    """True when a structured examiner field introduces this occurrence."""
    return bool(_ROLE_MARKER.search(text[max(0, start - 40):start]))


def _non_examiner(text, start, end, name):
    """Which non-examiner control fires on this occurrence, if any."""
    before = text[max(0, start - 12):start]
    after = text[end:end + 40]
    if _SHIP_PREFIX.search(before):
        return CONTROL_SHIP
    if _CASE_AFTER.match(after) or _CASE_BEFORE.search(text[max(0, start - 30):start]):
        return CONTROL_CASE
    if _AUTHOR_MARKER.search(text[max(0, start - 60):start]):
        return CONTROL_AUTHOR
    # An explicit examiner field wins over the shape of the following word.
    if is_role_labelled(text, start):
        return None
    m = re.match(r"\s+([A-Z][a-zA-Z]*\.?)", after)
    if m and m.group(1).rstrip(".") not in {h.rstrip(".") for h in _HONORIFIC}:
        return CONTROL_LONGER_NAME
    return None


def classify_cue(text, start, end, name, in_tip, in_heading):
    """(disposition, control, window) for one alias occurrence."""
    control = _non_examiner(text, start, end, name)
    if control:
        return CUE_NON_EXAMINER, control, text[max(0, start - 90):end + 90]
    window = text[start:end + 260]
    if _bound(_FOLLOWUP_MARKER, window, name):
        return CUE_FOLLOWUP, None, window
    if _bound(_ASK_VERB, window, name) or _bound(_ASK_NOUN, window, name):
        return CUE_PRIMARY_ASK, None, window
    if _bound(_EXPECT_MARKER, window, name):
        return CUE_EXPECTED_DETAIL, None, window
    if is_role_labelled(text, start):
        # "Examiner: Nair" states who examines this topic without stating the
        # ask. That is an explicit examiner label, and the vehicle records that
        # it is a structured field rather than a sentence about an ask.
        return CUE_PRIMARY_ASK, None, text[max(0, start - 40):end + 200]
    if in_tip:
        # A structured tip block names an examiner because the block is about
        # that examiner, but with no ask bound to the name it states no ask.
        return CUE_WEAK_MENTION, None, window
    if in_heading:
        return CUE_HEADING_CONTEXT, None, window
    return CUE_WEAK_MENTION, None, window
