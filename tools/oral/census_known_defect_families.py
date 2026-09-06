"""Read-only corpus census for the KNOWN mechanically-detectable defect families.

Pass 1 of the post-discovery remediation phase. Discovery converged (Tranche 5
found zero genuinely new material defect classes); what remains is corpus-wide
remediation of families that are already known and already adjudicated at least
once. This tool finds the SITES. It adjudicates nothing and it writes nothing to
any product file.

Families, as scoped by the Pass-1 instruction:

  A  correction reach failures      - a correction landed on the teaching body
                                      but missed the footer / cheat sheet /
                                      revision surface / sibling card layer
  B  authoring / model residue      - candidate-facing scaffold left by the
                                      authoring or conversion step
  C  empty / broken deep-dive       - empty <details>, empty promised block,
                                      cascaded duplicate deep-dive payload
  D  stale revision-layer labels    - a superseded instrument taught as current
                                      on a cheat sheet or revision surface
  E  unsupported numeric standard   - a hard number carrying regulatory/mandatory
                                      wording

Every hit is emitted with the SURFACE it sits on, because the surface is what
decides the classification. The same string is a defect in an answer body, and
correct in a `q-text` that quotes the examiner. Family A and D exist precisely
because earlier sweeps derived their site list from a finding's card list rather
than from the corpus, and left the sibling surfaces behind.

Nothing here is a verdict. `MUST CORRECT / HISTORICAL-QUOTED-KEEP / AMBIGUOUS`
is a human adjudication recorded in the Pass-1 report, never a grep result.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
QB_ROOT = REPO / "meoclass1"

sys.path.insert(0, str(HERE))

from oral_bytes import read_text  # noqa: E402

# --------------------------------------------------------------------------
# surface classification
# --------------------------------------------------------------------------

#: Ordered most-specific-first. A hit is attributed to the nearest PRECEDING
#: opening marker, which is how the rendered surfaces actually nest.
SURFACE_MARKERS = [
    ('q-text', re.compile(r'<div class="q-text">')),
    ('cs-qtitle', re.compile(r'<div class="cs-qtitle">')),
    ('q-version', re.compile(r'<span class="q-version">')),
    ('correction-link', re.compile(r'<span class="correction-link">')),
    ('source-confidence', re.compile(r'<em>Source confidence:')),
    ('currentness-note', re.compile(r'<strong>Currentness note')),
    ('reg-desc', re.compile(r'<span class="reg-desc">')),
    ('reg-code', re.compile(r'<span class="reg-code">')),
    ('num-pill', re.compile(r'<code class="num-pill">')),
    ('ce-tip', re.compile(r'<div class="ce-tip">')),
    ('deep-dive', re.compile(r'<div class="dd-item">')),
    ('practice-block', re.compile(r'<div class="practice-block">')),
    ('answer-body', re.compile(r'<div class="answer-body">')),
    ('cheatsheet-cell', re.compile(r'<td>')),
    ('cs-row', re.compile(r'<div class="cs-row">')),
    ('toc-link', re.compile(r'<a class="toc-link"')),
    ('sub-desc', re.compile(r'<p class="sub-desc">')),
]


def surface_at(text: str, pos: int) -> str:
    """Name the innermost candidate-facing surface containing offset `pos`."""
    best_name, best_start = "other", -1
    for name, rx in SURFACE_MARKERS:
        last = None
        for m in rx.finditer(text, 0, pos):
            last = m
        if last is not None and last.start() > best_start:
            best_name, best_start = name, last.start()
    return best_name


CARD_OPEN = re.compile(r'<div class="q-card" id="(q\d+)"')


def card_spans(text: str):
    """(anchor, start, end) for every q-card, by balanced-div scan."""
    out = []
    for m in CARD_OPEN.finditer(text):
        start = m.start()
        depth, i = 0, start
        n = len(text)
        while i < n:
            if text.startswith("<div", i):
                depth += 1
                i += 4
                continue
            if text.startswith("</div>", i):
                depth -= 1
                i += 6
                if depth == 0:
                    break
                continue
            i += 1
        out.append((m.group(1), start, i))
    return out


def card_at(spans, pos: str) -> str:
    for anchor, s, e in spans:
        if s <= pos < e:
            return anchor
    return "-"


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def excerpt(text: str, pos: int, span: int, width: int = 170) -> str:
    lo = max(0, pos - width // 2)
    hi = min(len(text), pos + span + width // 2)
    return re.sub(r"\s+", " ", text[lo:hi]).strip()


# --------------------------------------------------------------------------
# family A / D  - superseded instrument labels
# --------------------------------------------------------------------------

#: A governed list, not an open-ended "looks old" heuristic. Each entry names
#: the superseding fact and the record that established it, so a hit can be
#: adjudicated without re-doing the research.
SUPERSEDED_LABELS = [
    {
        "id": "BMP5",
        "pattern": r"BMP\s?5\b",
        "superseded_by": "BMP Maritime Security, 1st Edition (2025) as updated 2026",
        "established_by": "CORR-GPT-T2C-CURRENCY-20260905, propagated by "
                          "CORR-BMP-EDITION-PROP-20260905",
    },
    {
        "id": "MSC.1/Circ.1606",
        "pattern": r"MSC\.1/Circ\.1606",
        "superseded_by": "no replacement asserted - the row was removed from the "
                         "parent card as unusable, not re-cited",
        "established_by": "QB9_A#q9 v1.3 correction of 6 Sep 2026",
    },
]


def census_labels(files):
    hits = []
    for path in files:
        text = read_text(path)
        spans = card_spans(text)
        for spec in SUPERSEDED_LABELS:
            for m in re.finditer(spec["pattern"], text):
                hits.append({
                    "family": "A/D",
                    "label": spec["id"],
                    "file": path.name,
                    "line": line_of(text, m.start()),
                    "card": card_at(spans, m.start()),
                    "surface": surface_at(text, m.start()),
                    "superseded_by": spec["superseded_by"],
                    "excerpt": excerpt(text, m.start(), len(m.group(0))),
                })
    return hits


# --------------------------------------------------------------------------
# family B  - authoring / model residue
# --------------------------------------------------------------------------

RESIDUE_PATTERNS = [
    ("markdown-bullet-strong", r"\*\s*<strong>"),
    ("markdown-rule", r"-{5,}"),
    ("scaffold-below-are", r"Below are\b"),
    ("scaffold-drafted-in", r"drafted in the exact"),
    ("scaffold-chat-ready", r"chat-ready"),
    ("scaffold-as-requested", r"as requested\b"),
    ("scaffold-here-is-the", r"Here (?:is|are) the (?:following|requested)"),
    ("markdown-heading", r"(?m)^\s*#{2,}\s"),
    # A second conversion generation wrapped raw markdown in <p> instead of
    # rendering it. These three shapes are what it left on the page.
    ("markdown-heading-in-p", r"<p>#{2,}"),
    ("markdown-blockquote-in-p", r"<p>(?:&gt;|>)\s"),
    ("markdown-fence-in-p", r"<p>`{3}</p>"),
    ("markdown-orphan-bullet", r"(?<![>\s])\s\*\s+<strong>|\*\s+<strong>"),
    ("markdown-bold-pair", r"\*\*[^*\n]{2,80}\*\*"),
]


def census_residue(files):
    hits = []
    for path in files:
        text = read_text(path)
        spans = card_spans(text)
        for name, pat in RESIDUE_PATTERNS:
            for m in re.finditer(pat, text):
                hits.append({
                    "family": "B",
                    "pattern": name,
                    "file": path.name,
                    "line": line_of(text, m.start()),
                    "card": card_at(spans, m.start()),
                    "surface": surface_at(text, m.start()),
                    "match": m.group(0)[:60],
                    "excerpt": excerpt(text, m.start(), len(m.group(0))),
                })
    return hits


# --------------------------------------------------------------------------
# family C  - empty / broken deep-dive structure
# --------------------------------------------------------------------------

DD_LABEL = re.compile(r"<b>([^<]{2,60}?):\s*</b>")
DETAILS_OPEN = re.compile(r"<details\b[^>]*>")


def census_deepdive(files):
    hits = []
    for path in files:
        text = read_text(path)
        spans = card_spans(text)

        # empty <details> - opening tag whose body carries no visible text
        for m in DETAILS_OPEN.finditer(text):
            end = text.find("</details>", m.end())
            if end < 0:
                continue
            body = text[m.end():end]
            visible = re.sub(r"<[^>]+>", "", body)
            visible = re.sub(r"&[a-z]+;", " ", visible).strip()
            summary = re.search(r"<summary[^>]*>(.*?)</summary>", body, re.S)
            summary_text = re.sub(r"<[^>]+>", "", summary.group(1)).strip() if summary else ""
            rest = visible.replace(summary_text, "").strip()
            if not rest:
                hits.append({
                    "family": "C",
                    "defect": "empty_details",
                    "file": path.name,
                    "line": line_of(text, m.start()),
                    "card": card_at(spans, m.start()),
                    "summary": summary_text[:120],
                })

        # empty dd-item, and duplicated dd-item labels inside one card
        for anchor, s, e in spans:
            block = text[s:e]
            labels = [x.group(1).strip() for x in DD_LABEL.finditer(block)]
            seen = {}
            for lab in labels:
                seen[lab] = seen.get(lab, 0) + 1
            for lab, n in sorted(seen.items()):
                if n > 1:
                    hits.append({
                        "family": "C",
                        "defect": "duplicate_dd_label",
                        "file": path.name,
                        "card": anchor,
                        "line": line_of(text, s),
                        "label": lab,
                        "count": n,
                    })
            for m in re.finditer(r'<div class="dd-item">(.*?)</div>', block, re.S):
                inner = re.sub(r"<[^>]+>", "", m.group(1))
                inner = re.sub(r"&[a-z]+;", " ", inner)
                stripped = re.sub(r"^[^:]{0,60}:", "", inner).strip()
                if not stripped:
                    hits.append({
                        "family": "C",
                        "defect": "empty_dd_item",
                        "file": path.name,
                        "card": anchor,
                        "line": line_of(text, s + m.start()),
                        "raw": m.group(1)[:120],
                    })
    return hits


# --------------------------------------------------------------------------
# family E  - numeric claim under mandatory wording
# --------------------------------------------------------------------------

MODAL = (r"required|minimum|maximum|standard|must\b|mandatory|always|"
         r"permitted interval|shall\b|at least|no less than|not exceed")
NUMBER = r"\d+(?:[.,]\d+)?(?:\s*(?:&ndash;|&mdash;|-|to)\s*\d+(?:[.,]\d+)?)?"
UNIT_BROAD = (r"bar|N/mm|kPa|MPa|psi|m/s|m\b|mm\b|cm\b|kg|tonne|litre|l/min|"
              r"month|months|year|years|day|days|hour|hours|minute|minutes|"
              r"%|degC|&deg;C|GT\b|kW\b|ppm\b")

#: The TIGHT profile is the Pass-1 priority set, and it is narrow on purpose.
#: Every known member of this defect family - the invented 6 bar, Tranche 5's
#: "4-6 bar required minimum", QB10_B's 1.0-1.3 m/s - is a PHYSICAL engineering
#: quantity presented as a regulatory floor. Time intervals dominate the broad
#: census and are overwhelmingly properly cited survey/retention periods, so
#: sweeping them would bury the class this pass exists to find.
UNIT_TIGHT = r"bar|N/mm|kPa|MPa|psi|m/s|l/min"

MODAL_RX = re.compile(MODAL, re.I)

#: A hit needs the modal word WITHIN this many characters of the number, in the
#: same sentence-ish neighbourhood. Wider windows drown the census in prose.
MODAL_WINDOW = 90
MODAL_WINDOW_TIGHT = 55

CANDIDATE_SURFACES = {
    "practice-block", "answer-body", "reg-desc", "ce-tip", "deep-dive",
    "cheatsheet-cell", "cs-row", "num-pill", "source-confidence",
}


def census_numeric(files, profile="tight"):
    unit = UNIT_TIGHT if profile == "tight" else UNIT_BROAD
    span_w = MODAL_WINDOW_TIGHT if profile == "tight" else MODAL_WINDOW
    num_unit = re.compile(r"(%s)\s*(%s)" % (NUMBER, unit))
    hits = []
    for path in files:
        text = read_text(path)
        spans = card_spans(text)
        for m in num_unit.finditer(text):
            lo = max(0, m.start() - span_w)
            hi = min(len(text), m.end() + span_w)
            window = text[lo:hi]
            mod = MODAL_RX.search(window)
            if not mod:
                continue
            surface = surface_at(text, m.start())
            if surface not in CANDIDATE_SURFACES:
                continue
            hits.append({
                "family": "E",
                "profile": profile,
                "file": path.name,
                "line": line_of(text, m.start()),
                "card": card_at(spans, m.start()),
                "surface": surface,
                "number": m.group(0),
                "modal": mod.group(0),
                "excerpt": excerpt(text, m.start(), len(m.group(0)), width=260),
            })
    return hits


# --------------------------------------------------------------------------

FAMILIES = {
    "A": census_labels,
    "D": census_labels,
    "B": census_residue,
    "C": census_deepdive,
    "E": census_numeric,
}


def target_files(scope: str):
    files = sorted(QB_ROOT.glob("*.html"))
    if scope == "cards":
        return [p for p in files if re.match(r"QB\d", p.name)
                and "heat" not in p.name.lower()]
    if scope == "revision":
        return [p for p in files if "heat" in p.name.lower()]
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--family", choices=["A", "B", "C", "D", "E", "AD", "all"],
                    default="all")
    ap.add_argument("--scope", choices=["all", "cards", "revision"], default="all")
    ap.add_argument("--numeric-profile", choices=["tight", "broad"],
                    default="tight",
                    help="tight = the Pass-1 priority set (physical engineering "
                         "quantities under mandatory wording); broad = the whole "
                         "field, including time intervals")
    ap.add_argument("--json", metavar="PATH")
    args = ap.parse_args()

    files = target_files(args.scope)
    out = {}
    if args.family in ("A", "D", "AD", "all"):
        out["A/D_superseded_labels"] = census_labels(files)
    if args.family in ("B", "all"):
        out["B_authoring_residue"] = census_residue(files)
    if args.family in ("C", "all"):
        out["C_deepdive_structure"] = census_deepdive(files)
    if args.family in ("E", "all"):
        out["E_numeric_standard"] = census_numeric(files, args.numeric_profile)

    print("files scanned: %d  (scope=%s)" % (len(files), args.scope))
    for key, hits in out.items():
        print("\n=== %s : %d hits ===" % (key, len(hits)))
        for h in hits:
            bits = [h["file"], h.get("card", "-"), "L%s" % h.get("line", "?"),
                    h.get("surface", h.get("defect", ""))]
            head = " | ".join(str(b) for b in bits)
            tail = (h.get("excerpt") or h.get("label") or h.get("summary")
                    or h.get("raw") or "")
            print("  %-58s %s" % (head, tail[:230]))

    if args.json:
        pathlib.Path(args.json).write_bytes(
            json.dumps(out, indent=1, ensure_ascii=False).encode("utf-8"))
        print("\nwrote %s" % args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
