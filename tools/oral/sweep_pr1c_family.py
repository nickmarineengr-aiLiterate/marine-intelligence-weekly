#!/usr/bin/env python3
"""Generate the PR1C-family sweep, instead of asserting it.

WHY THIS EXISTS
---------------
Three consecutive Pass-2 rounds recorded a sweep-completeness claim in prose,
and all three were false:

  round 1  "Beyond QB4_C q5 the only remaining hits are the already-corrected
            QB1_K q2, and past-paper examiner wording."
            -> missed QB4_A#q9, eight layers.
  round 2  "every other hit is a past-paper stem, each of which was OPENED."
            -> missed QB4_A_CheatSheet, QB1_C#q6, QB4_E#q13, QB1_F#q7.
  round 3  this file.

Each miss had the same cause. The sweep was run in the vocabulary of the card
being fixed, over the surfaces that card lives on, and its RESULT was written
down as a conclusion that nothing could check. The cheat sheet escaped twice
because it abbreviates "certificates" to "certs".

So the claim is replaced by an artefact. This tool enumerates every page from
disk -- not from a manifest, which can be stale, and not from a card index,
which cannot see the 34 cheat sheets because they contain no q-card -- reads
what a browser would RENDER, and searches on token variants.

WHAT IT DOES NOT DO
-------------------
It does not adjudicate. A hit is a site to read, not a defect. The
classification below is deliberately coarse and errs toward REVIEW: the one
bucket that has caused every failure is "past-paper examiner wording", which is
where a hit goes when nobody opened it, so this tool never assigns it. Only a
human, having read the site, may move a hit out of REVIEW -- and the allow-list
that records those decisions cites the reason inline.
"""
from __future__ import annotations

import argparse
import html as htmllib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio, read_text  # noqa: E402

enable_utf8_stdio()

#: Token variants matter more than phrasing. "certs" is why a P0 survived two
#: sweeps, so every certificate pattern carries the abbreviation.
CERT = r"(?:certificates?|certs?)"

#: The family's subject. Every pattern below is anchored to it, so this sweep
#: stays a bounded propagation check and does not drift into a discovery pass
#: over every mention of insurance or certificates in the corpus.
CLASS = (r"(?:suspen\w+|withdraw\w+|out of class|loss of class|lose[sd]?\s+"
         r"(?:its\s+)?class|class(?:ification)?\s+(?:is\s+)?"
         r"(?:suspended|withdrawn)|[Cc]ondition of [Cc]lass)")

PROPOSITIONS = {
    "ALL_STATUTORY_CERTIFICATES": [
        r"\ball\b[^.]{0,40}?statutory\s+" + CERT + r"[^.]{0,60}?(?:invalid|void|lapse)",
        r"every\s+statutory\s+" + CERT,
        r"statutory\s+" + CERT + r"[^.]{0,50}?(?:become|are|is)\s+"
        r"(?:simultaneously\s+)?invalid",
        r"statutory\s+" + CERT + r"[^.]{0,40}?invalid\s+simultaneously",
    ],
    # Anchored to CLASS. The proposition under correction is "loss of class
    # destroys cover", not "insurance can be avoided", which is a different and
    # often correct subject elsewhere in the corpus.
    "INSURANCE_AUTOMATICALLY_LOST": [
        CLASS + r"[^.]{0,110}?(?:insurance|P&I|H&M|\bcover\b|coverage)"
        r"[^.]{0,60}?(?:void|avoided|lapse\w*|forfeit\w*|falls?\s+away|"
        r"fell\s+away|rendered void|automatically\s+(?:invalidat|end|ceas))",
        r"(?:void\w*|invalidat\w*|forfeit\w*)[^.]{0,60}?"
        r"(?:insurance|P&I|H&M|\bcover\b|coverage)[^.]{0,110}?" + CLASS,
        CLASS + r"[^.]{0,110}?(?:voids?|invalidates?)\s+"
        r"(?:the\s+)?(?:vessel|ship)(?:&#x27;s|'s|’s)?\s*"
        r"(?:P&I|H&M|hull)?\s*insurance",
    ],
    "COC_AUTOMATICALLY_SUSPENDS": [
        r"(?:[Cc]ondition of [Cc]lass|\bCoC\b)[^.]{0,90}?automatic\w*[^.]{0,40}?suspen",
        r"(?:[Cc]ondition of [Cc]lass|\bCoC\b)[^.]{0,60}?"
        r"(?:overdue|not (?:met|cleared|rectified))[^.]{0,60}?suspen",
        r"[Oo]verdue[^.]{0,40}?(?:\u2192|->|=>)\s*suspension",
        r"invalidates? class automatic\w*",
        r"automatic\w*\s+[Ss]uspension of [Cc]lass",
        r"(?:due date|timeframe)[^.]{0,50}?results in[^.]{0,30}?[Ss]uspension",
        r"[Cc]lass suspended if not met",
        r"suspension if missed",
    ],
    "WRONG_INSTRUMENT": [
        r"\bUR\s*Z15\b",
        r"\bUR\s*Z23\b",
        r"IACS\s+PR\s*No\.?\s*[13]\b",
        # bare "PR 1" / "(PR1)" - the form that hid three sites in the notes
        r"\(?\bPR\s?1\)?(?!\s*[A-D]\b)(?![A-D0-9])",
        r"\bPR\s*No\.?\s*3\b(?!\s*5)",
    ],
}

#: A hit is DISARMED when the card is warning against the claim rather than
#: making it. Kept narrow on purpose: this is the mechanism that let a defect
#: hide behind the word "no" in an earlier gate.
DISARM = re.compile(
    r"(?:\bnot\b\s*[\u201c\u201d\"\']?\s*(?:UR|PR)|records as Deleted|"
    r"index records|there is no\s*[\u201c\u201d\"\']?\s*.{0,3}PR|"
    r"\bDeleted\b|not all of them|"
    r"rather than claiming|do not (?:tell|call|go further|forget to)|"
    r"there is no universal|contains no insurance|says nothing about insurance|"
    r"is not automatic|not automatic|cover may be prejudiced|"
    r"suspension procedure|can lead to|may lead to|A\.2\.1|A\.1\.1|"
    r"terminates automatically|ITC-Hulls|Institute Time Clauses|"
    r"PR\s?1 family|PR1 family|UR ?/ ?UI ?/ ?PR|neighbouring procedures|"
    r"which is Hull Survey|which is Hull, Structure|is Deleted in the IACS)",
    re.I)


#: Hits a human has OPENED and adjudicated. Each entry cites its reason inline,
#: because the bucket that caused three consecutive false completeness claims
#: was "past-paper examiner wording" - the label a hit gets when nobody read it.
#: A hit not listed here is REVIEW, and --check fails on it.
ADJUDICATED = {
    ("meoclass1/QB4_A.html", "statutory certificates also become invalid"):
        "EXAMINER QUESTION, not teaching. The card quotes a trap question - 'are only "
        "the classification records invalid, or do statutory certificates also become "
        "invalid?' - and its own answer corrects it to PR1C B.1.3's 'certain'.",

    ("meoclass1/oralnotes/miw-notes-mgmt-p1.html", "Every statutory certificate"):
        "DIFFERENT SENSE, and correct. 'Every statutory certificate on board - IOPP, Safety "
        "Equipment, Loadline - is issued under an IMO convention' is set membership, with "
        "no invalidation claim.",

    ("meoclass1/oralnotes/miw-notes-mgmt-p21.html",
     "Loss of class \u2014 hull and machinery cover and most financing covenants fall away"):
        "CORRECT AS WRITTEN, and it is this batch that was wrong. Institute Time Clauses - "
        "Hulls (1/11/95) cl. 5.1 terminates hull cover AUTOMATICALLY on suspension, "
        "discontinuance or withdrawal of class. Rounds 1-3 of this batch replaced that with "
        "'cover may be prejudiced', which was an over-correction; round 4 reversed it "
        "across every card it had touched. This note was right all along.",

    ("meoclass1/oralnotes/miw-notes-mgmt-p22.html", "every statutory certificate"):
        "DIFFERENT SENSE, and correct. 'A ship can hold every statutory certificate and "
        "still be commercially unemployable on a poor vetting record' uses 'every "
        "certificate' to mean the full set, and makes no invalidation claim at all.",

    ("meoclass1/oralnotes/miw-notes-mgmt-p7.html", "automatic suspension of class"):
        "DIFFERENT PROPOSITION, and hedged. The trigger is an unapproved structural or "
        "machinery modification made without class approval, not an overdue survey or "
        "condition of class, and the text says 'can trigger'. Outside the PR1C overdue-"
        "item family this sweep is scoped to. Not corrected, and not claimed correct: "
        "the Notes series is generated from a JSON content spec by tools/notes, so its "
        "HTML must not be hand-edited.",
}


#: Hits that ARE defects but sit outside what this pass may correct. Separated
#: from ADJUDICATED on purpose: "not a defect" and "a real defect somebody else
#: must fix" are different claims, and collapsing them is how a live defect
#: comes to look cleared. Each entry names where it is tracked.
DEFERRED = {
    ("meoclass1/pastpapers/QP2503.html",
     "condition of class with a due date; if that is not cleared, class is suspen"):
        "COMPRESSION IN A PLAN BLOCK, P3. MIW-authored model-answer planning text, not an "
        "examiner stem, so it is not protected by the examiner-wording rule - but it is "
        "sitting-anchored past-paper content and outside this pass's declared families. "
        "The same compression was corrected where it appeared in QB teaching cards.",
    ("meoclass1/pastpapers/QP2507.html",
     "condition of class with a due date; if that is not cleared, class is suspen"):
        "COMPRESSION IN A PLAN BLOCK, P3. Same as QP2503.",
}


def adjudication(hit):
    """An adjudication covers the TEXT that was read, not the file.

    The first version matched (file, substring), so any later hit anywhere in
    that page inherited the human decision as long as it happened to contain
    the fragment. That is a permanent per-file blind spot, and it is the same
    shape as the acceptance rule the review pool already gets right: a
    clearance covers the bytes somebody read.
    """
    for (f, frag), why in ADJUDICATED.items():
        if hit["file"] == f and hit["text"].strip() == frag.strip():
            return "CLEARED: " + why
    for (f, frag), why in DEFERRED.items():
        if hit["file"] == f and frag in hit["text"]:
            return "DEFERRED: " + why
    return None


def rendered_text(markup: str) -> str:
    """What a browser shows. Scripts and styles never reach the reader."""
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", markup, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", htmllib.unescape(t))


def strip_provenance(markup: str) -> str:
    """Drop q-footers before sweeping.

    Every version stamp written in this batch QUOTES the wording it removed, so
    a sweep that reads footers reports each correction as a fresh hit -- trap 89
    in the sweep direction. The footers are provenance, not teaching.
    """
    out, pos = [], 0
    for m in re.finditer(r'<div class="q-footer"', markup):
        out.append(markup[pos:m.start()])
        depth, i = 0, m.start()
        for t in re.finditer(r"<div\b|</div>", markup[m.start():]):
            depth += -1 if t.group(0) == "</div>" else 1
            i = m.start() + t.end()
            if depth == 0:
                break
        pos = i
    out.append(markup[pos:])
    return "".join(out)


def anchor_for(markup: str, pos: int) -> str:
    """Nearest preceding id="qN", or the page's surface kind."""
    head = markup[:pos]
    m = None
    for m in re.finditer(r'id="(q\d+)"', head):
        pass
    return m.group(1) if m else "-"


def sweep():
    hits = []
    for path in sorted(QB.rglob("*.html")):
        rel = path.relative_to(REPO).as_posix()
        raw = read_text(path)
        # Map rendered offsets back to markup offsets cheaply: run the search on
        # rendered text for TRUTH, then locate a distinctive fragment in the
        # markup for the anchor. Where that fails the anchor is reported as "-"
        # rather than guessed.
        text = rendered_text(strip_provenance(raw))
        for family, patterns in PROPOSITIONS.items():
            for pat in patterns:
                for m in re.finditer(pat, text, re.I):
                    # Scoped like the validator's asserts(): a disarming
                    # phrase in a NEIGHBOURING sentence is not evidence about
                    # this one. An unscoped window let "Reinstatement ... is
                    # not automatic" clear an assertion two sentences earlier.
                    head = text[max(0, m.start() - 200):m.start()]
                    cut = max(head.rfind(". "), head.rfind("; "), head.rfind("? "))
                    tail = text[m.end():m.end() + 160]
                    stop = min([i for i in (tail.find(". "), tail.find("; "))
                                if i >= 0] or [len(tail)])
                    window = head[cut + 2:] + m.group(0) + tail[:stop]
                    if DISARM.search(window):
                        continue
                    # Locate the match in the MARKUP, not the first occurrence
                    # of its first word -- that reported QB1_G's hit as q24 when
                    # it is in q36, and an anchor that is confidently wrong is
                    # worse than one that admits it does not know.
                    words = [w for w in re.split(r"\s+", m.group(0)) if len(w) > 3]
                    loc = -1
                    for probe in (" ".join(words[:4]), " ".join(words[:2])):
                        if not probe:
                            continue
                        loc = raw.find(probe)
                        if loc >= 0:
                            break
                    if loc < 0 and words:
                        loc = raw.find(max(words, key=len))
                    hits.append({
                        "file": rel,
                        "anchor": anchor_for(raw, loc) if loc >= 0 else "-",
                        "surface": ("cheatsheet" if "CheatSheet" in path.name
                                    else "pastpaper" if "pastpapers" in rel
                                    else "notes" if "oralnotes" in rel
                                    else "qb"),
                        "family": family,
                        "text": m.group(0)[:220],
                    })
    # de-duplicate: the same sentence can match two patterns in one family
    seen, out = set(), []
    for h in hits:
        key = (h["file"], h["family"], h["text"][:80])
        if key in seen:
            continue
        seen.add(key)
        out.append(h)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write the full result here")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any hit is unadjudicated, on any surface")
    a = ap.parse_args()

    hits = sweep()
    for h in hits:
        h["adjudication"] = adjudication(h)
    live = [h for h in hits if h["adjudication"] is None]

    print("PR1C-family sweep -- %d page(s) scanned, %d undisarmed hit(s)"
          % (len(list(QB.rglob("*.html"))), len(hits)))
    for h in sorted(hits, key=lambda x: (x["surface"], x["file"], x["family"])):
        print("  %-4s %-10s %-30s %-6s %-28s %s"
              % ("OK" if h["adjudication"] else "OPEN",
                 h["surface"], h["file"].split("/")[-1], h["anchor"],
                 h["family"], h["text"][:70]))
    cleared = [h for h in hits if (h["adjudication"] or "").startswith("CLEARED")]
    deferred = [h for h in hits if (h["adjudication"] or "").startswith("DEFERRED")]
    print("\ncleared: %d   deferred: %d   UNADJUDICATED: %d"
          % (len(cleared), len(deferred), len(live)))
    for h in deferred:
        print("  DEFERRED %s [%s] %s"
              % (h["file"], h["family"], h["adjudication"].split(".")[0][10:]))
    for h in live:
        print("  OPEN %s#%s [%s] %s"
              % (h["file"], h["anchor"], h["family"], h["text"][:110]))

    if a.json:
        pathlib.Path(a.json).write_text(
            json.dumps({"schema": "miw-pr1c-family-sweep/1",
                        "scanned": len(list(QB.rglob("*.html"))),
                        "hits": hits}, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8", newline="\n")
        print("wrote %s" % a.json)

    return 1 if (a.check and live) else 0


if __name__ == "__main__":
    raise SystemExit(main())
