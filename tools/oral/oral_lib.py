"""Shared parsing helpers for the Oral Examiner Intelligence audit.

Portability: the repo root is derived from this file's location, never a
drive letter. External workbook / document paths arrive as CLI arguments.
"""
from __future__ import annotations

import html as _html
import json
import re
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MEO = REPO / "meoclass1"
OUT = MEO / "oral-intelligence" / "examiner-audit"

# --------------------------------------------------------------------------
# text normalisation
# --------------------------------------------------------------------------
_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")


def strip_tags(s):
    return _WS.sub(" ", _html.unescape(_TAG.sub(" ", s))).strip()


def norm(s):
    """Aggressive comparison key: fold case, punctuation and whitespace."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return _WS.sub(" ", s).strip()


STOP = set(
    """a an the of to in on for and or is are was were be been what which who how why when
where do does did explain describe state list give your you it its as at by with from that this
i we they he she""".split()
)


def tokens(s):
    return {t for t in norm(s).split() if t not in STOP and len(t) > 2}


def jaccard(a, b):
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def containment(a, b):
    """Fraction of the smaller token set covered by the larger."""
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / min(len(ta), len(tb))


# --------------------------------------------------------------------------
# live QB inventory
# --------------------------------------------------------------------------
CARD = re.compile(r'<div class="q-card[^"]*"([^>]*)>', re.I)
ATTR = re.compile(r'([\w-]+)="([^"]*)"')
QTEXT = re.compile(r'<div class="q-text"[^>]*>(.*?)</div>', re.S | re.I)
QANS = re.compile(r'<div class="q-answer">', re.I)
GATE = re.compile(r"miw_auth", re.I)


def qb_files():
    """Every live Oral QB page: QB*.html excluding cheat sheets."""
    out = []
    for p in sorted(MEO.glob("QB*.html")):
        if "cheatsheet" in p.name.lower():
            continue
        out.append(p)
    return out


def parse_qb_file(path):
    h = path.read_text(encoding="utf-8", errors="replace")
    gated = bool(GATE.search(h))
    rows = []
    matches = list(CARD.finditer(h))
    for i, m in enumerate(matches):
        attrs = dict(ATTR.findall(m.group(1)))
        cid = attrs.get("id", "")
        end = matches[i + 1].start() if i + 1 < len(matches) else len(h)
        block = h[m.start():end]
        qm = QTEXT.search(block)
        text = strip_tags(qm.group(1)) if qm else ""
        num = None
        mm = re.fullmatch(r"q(\d+)", cid)
        if mm:
            num = int(mm.group(1))
        rows.append(
            {
                "file": path.name,
                "anchor": cid,
                "q_number": num,
                "is_question": num is not None,
                "question_text": text,
                "tags": attrs.get("data-tags", ""),
                "has_answer": bool(QANS.search(block)),
                "answer_chars": len(strip_tags(block)),
                "gated": gated,
            }
        )
    return rows


def qb_group(fname):
    m = re.match(r"(QB\d+)", fname)
    return m.group(1) if m else ""


def build_inventory():
    inv = []
    for p in qb_files():
        for r in parse_qb_file(p):
            if not r["is_question"]:
                continue
            r["canonical_question_id"] = p.stem + "#" + r["anchor"]
            r["qb_group"] = qb_group(p.name)
            r["url"] = "/meoclass1/" + p.name + "#" + r["anchor"]
            inv.append(r)
    return inv


def all_anchors():
    """file name -> set of every id= present on the page (any element)."""
    out = {}
    for p in MEO.glob("*.html"):
        h = p.read_text(encoding="utf-8", errors="replace")
        out[p.name] = set(re.findall(r'\sid="([^"]+)"', h))
    return out


# --------------------------------------------------------------------------
# examiner index
# --------------------------------------------------------------------------
SECTION = re.compile(r'<section class="ex-section" id="ex-([^"]+)">(.*?)</section>', re.S)
ROW = re.compile(
    r'<div class="q-row[^"]*"\s+data-tier="([^"]*)">\s*'
    r'<a class="q-link" href="([^"]*)">(.*?)</a>\s*'
    r'<div class="q-txt"[^>]*>(.*?)</div>\s*'
    r'<span class="tier-badge">(.*?)</span>',
    re.S,
)
BATCH = re.compile(r'id="batch-([^"-]+)-(\d+)"')


def parse_examiner_index(path):
    h = path.read_text(encoding="utf-8", errors="replace")
    body = h.split("</style>", 1)[1]
    rows = []
    sections = []
    for sm in SECTION.finditer(body):
        slug, blob = sm.group(1), sm.group(2)
        hm = re.search(r'<h2>(.*?)<span class="ex-count">(.*?)</span>', blob, re.S)
        name = strip_tags(hm.group(1)) if hm else slug
        heading_count = None
        if hm:
            cm = re.search(r"(\d+)", hm.group(2))
            heading_count = int(cm.group(1)) if cm else None
        stats = re.search(r'<div class="ex-stats">(.*?)</div>', blob, re.S)
        srow = {}
        if stats:
            for n, lab in re.findall(r"(\d+)\s*([A-Za-z-]+)", strip_tags(stats.group(1))):
                srow[lab.lower()] = int(n)
        n_rows = 0
        for rm in ROW.finditer(blob):
            tier, href, label, txt, badge = rm.groups()
            n_rows += 1
            rows.append(
                {
                    "row_index": len(rows),
                    "examiner_slug": slug,
                    "examiner_raw": name,
                    "tier": tier,
                    "href": href,
                    "link_label": strip_tags(label),
                    "display_text": strip_tags(txt),
                    "badge": strip_tags(badge),
                }
            )
        sections.append(
            {
                "slug": slug,
                "name": name,
                "heading_count": heading_count,
                "ex_stats": srow,
                "rendered_rows": n_rows,
                "batches": len(set(BATCH.findall(blob))),
            }
        )
    sb = re.search(r'<div class="summary-bar">(.*?)</div>\s*\n', h, re.S)
    header = {}
    if sb:
        t = strip_tags(sb.group(1))
        for n, lab in re.findall(r"(\d+)\s+([A-Za-z -]+?)(?:\s*·|\s*$)", t):
            header[lab.strip().lower()] = int(n)
    mini = {}
    mn = re.search(r'<div class="mininav">(.*?)</div>\s*\n\s*<div class="search-bar"', h, re.S)
    if mn:
        for name, cnt in re.findall(
            r'<a class="mini-pill"[^>]*>(.*?)<span>\D*(\d+)', mn.group(1), re.S
        ):
            mini[strip_tags(name)] = int(cnt)
    return {"rows": rows, "sections": sections, "header": header, "mininav": mini}


def split_href(href):
    h = href.split("?")[0]
    if "#" in h:
        f, a = h.rsplit("#", 1)
    else:
        f, a = h, ""
    return Path(f).name, a


def jdump(obj, name):
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p
