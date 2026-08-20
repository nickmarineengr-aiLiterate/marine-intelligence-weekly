"""Extract a canonical Oral QB card's full candidate-facing content by file#anchor.

Used by the final enrichment consolidation to decide, per authorised
enrichment family, whether the missing limb is genuinely still missing from
the CURRENT (post Batch A-D) live card - rather than from its title, its
search snippet, or the historical 688-question corpus.

Identity is file + anchor, matching tools/oral/build_qb_content_index.py.
This module READS the live HTML only; it never writes product.

  PYTHONIOENCODING=utf-8 python tools/oral/enrichment_cards.py QB1_F#q7
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_lib as L  # noqa: E402

# Card sections vary by page generation: reg-box and the q-footer sit inside
# q-answer on some pages and outside it on others, and the deep-dive block set
# is not uniform. The extractor therefore slices from one q-card open to the
# next q-card open rather than trusting a fixed inner structure.
_CARD_OPEN = re.compile(r'<div[^>]*class="[^"]*\bq-card\b[^"]*"[^>]*id="(q\d+)"', re.I)
_SECTIONS = {
    "q_text": r'<div class="q-text">(.*?)</div>',
    "answer_15": r'<div class="practice-block practice-15">(.*?)</div>',
    "answer_60": r'<div class="practice-block practice-60">(.*?)</div>',
    "answer_body": r'<div class="answer-body">(.*?)(?=<div class="(?:deep-dive|reg-box|q-footer)|\Z)',
}

# The deep-dive sub-blocks are siblings, and the reg-box is a list of
# reg-item rows. Both are recovered by splitting rather than by a lookahead
# regex: a lookahead that stops at the first "</div></div>" silently swallows
# the following sibling, which made dd_trap report dd_fail's text as its own.
_DD_SPLIT = re.compile(r'<div class="dd-block (dd-[a-z]+)"', re.I)
_REG_ITEM = re.compile(
    r'<div class="reg-item">.*?<div class="reg-code">(.*?)</div>.*?'
    r'<div class="reg-desc">(.*?)</div>', re.S | re.I)


def card_html(qid):
    """Return the raw HTML slice for one file#anchor, or None."""
    fname, anchor = qid.split("#")
    path = L.MEO / (fname if fname.endswith(".html") else fname + ".html")
    if not path.exists():
        return None
    src = path.read_text(encoding="utf-8")
    opens = [(m.group(1), m.start()) for m in _CARD_OPEN.finditer(src)]
    for i, (aid, pos) in enumerate(opens):
        if aid == anchor:
            end = opens[i + 1][1] if i + 1 < len(opens) else len(src)
            return src[pos:end]
    return None


def card(qid):
    """Return {section: plain text} for one file#anchor."""
    raw = card_html(qid)
    if raw is None:
        return None
    out = {"id": qid}
    for name, pat in _SECTIONS.items():
        m = re.search(pat, raw, re.S | re.I)
        out[name] = L.strip_tags(m.group(1)) if m else ""
    # deep-dive sub-blocks, split at sibling boundaries
    parts = _DD_SPLIT.split(raw)
    dd = {}
    for i in range(1, len(parts), 2):
        dd[parts[i].replace("-", "_")] = L.strip_tags(parts[i + 1])
    for k in ("dd_relevance", "dd_trap", "dd_chain", "dd_fail", "dd_numbers", "dd_vessel"):
        out[k] = dd.get(k, "")
    # regulatory references, as code -> description pairs
    out["reg_box"] = [f"{L.strip_tags(c)} :: {L.strip_tags(dsc)}"
                      for c, dsc in _REG_ITEM.findall(raw)]
    # answer-body headings carry the card's own section architecture, which is
    # what tells us whether a missing limb has a home or needs a new one.
    out["headings"] = [L.strip_tags(h) for h in re.findall(r"<h4[^>]*>(.*?)</h4>", raw, re.S | re.I)]
    out["chars"] = len(L.strip_tags(raw))
    return out


if __name__ == "__main__":
    for qid in sys.argv[1:]:
        c = card(qid)
        if c is None:
            print(f"{qid}: NOT FOUND")
            continue
        print("=" * 70)
        print(qid, f"({c['chars']} chars)")
        for k, v in c.items():
            if k in ("id", "chars") or not v:
                continue
            print(f"--- {k} ---")
            print(v if isinstance(v, str) else " | ".join(v))
