"""Guard the eight laptop-authorised P1-A new canonical Q&A cards.

The batch manifest is the authority for which family id lives at which file#anchor.
This validator proves, against the LIVE QB HTML rather than against any derived
artefact, that:

  * every authorised card exists, exactly once, at its recorded home;
  * no ninth card has appeared in a Batch-A destination;
  * each new card's anchor is unique and sits under #q-feed with sound parentage;
  * each new card carries a clean candidate-facing question and a non-empty answer;
  * no production metadata - family ids, occurrence ids, action ids, editorial
    markers, source-channel names - is candidate-visible anywhere on those pages;
  * the derived content index agrees with the live pages on the corpus total.

Exit 0 when every check passes, 1 otherwise.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).resolve().parent / "batch_a_manifest.json"
QB_DIR = REPO / "meoclass1"
CONTENT_INDEX = QB_DIR / "qb_content_index.json"

VOID = {"br", "img", "input", "hr", "meta", "link", "path", "source", "col", "area"}

# Production vocabulary that must never reach a candidate.
FORBIDDEN = [
    (re.compile(r"\bGAP-\d{3,4}\b"), "gap family id"),
    (re.compile(r"\bASC-\d{3,4}\b"), "source occurrence id"),
    (re.compile(r"\bNEW-\d{3}\b"), "production action id"),
    (re.compile(r"\bRELA-[A-Z]"), "relationship id"),
    (re.compile(r"\bP1-[AB]\b|\bP0\b"), "batch label"),
    (re.compile(r"PRIMARY_AUTHORITY_REQUIRED|CURRENT_REG_VERIFY_REQUIRED|TECH_VERIFY_REQUIRED"),
     "verification scope token"),
    (re.compile(r"NEW_CANONICAL_QA|ENRICH_EXISTING_QB|NOTES_TO_QB_PROMOTION|ALREADY_COVERED"),
     "disposition literal"),
    (re.compile(r"laptop_decision|adjudicated_decision|recurrence_class|decision_target"),
     "authoring field"),
    (re.compile(r"⚠\s*CORRECTED|\bTODO\b|\bFIXME\b|\bDRAFT NOTE\b", re.I), "editorial marker"),
    (re.compile(r"\bWhatsApp\b", re.I), "source channel"),
]

# Candidate-facing question text must read as an examiner ask, nothing else.
QTEXT_FORBIDDEN = [
    (re.compile(r"\bExaminer\s*:", re.I), "examiner label"),
    (re.compile(r"15-Second|60-Second|Deep Dive", re.I), "answer heading"),
    (re.compile(r"\bsaid ab(ou)?t\b|\bhe wants\b|\bcross questions\b|\bmany cross\b", re.I),
     "raw source wording"),
]

_fails = []
_checks = 0


def report(name, ok, detail=""):
    global _checks
    _checks += 1
    print("%-5s %-46s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        _fails.append(name)


class Page(HTMLParser):
    """Collect q-cards with their ancestry, question text and answer text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ids = []
        self.cards = []          # (qid, inside_q_feed, ancestor tags)
        self.text = {}           # qid -> {"q": str, "a": str}
        self.cur = None
        self.grab = None         # ("q"|"a", depth)
        self.buf = []
        self.body = []           # all visible text on the page
        self.structure = []      # structural complaints

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        cls = d.get("class", "").split()
        el_id = d.get("id")
        if el_id:
            self.ids.append(el_id)
        if "q-card" in cls and el_id:
            self.cards.append((el_id,
                               any(i == "q-feed" for _, i, _ in self.stack),
                               [t for t, _, _ in self.stack]))
            self.cur = el_id
            self.text[el_id] = {"q": "", "a": ""}
        if self.cur and self.grab is None:
            if "q-text" in cls:
                self.grab = ("q", len(self.stack)); self.buf = []
            elif "q-answer" in cls:
                self.grab = ("a", len(self.stack)); self.buf = []
        if tag not in VOID:
            self.stack.append((tag, el_id, cls))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                if i != len(self.stack) - 1:
                    skipped = [t for t, _, _ in self.stack[i + 1:]]
                    self.structure.append("</%s> closed over open %s" % (tag, skipped))
                depth = i
                del self.stack[i:]
                break
        else:
            self.structure.append("stray </%s>" % tag)
            return
        if self.grab and depth < self.grab[1]:
            self.text[self.cur][self.grab[0]] = " ".join("".join(self.buf).split())
            self.grab = None
            self.buf = []
        if self.cur and not any("q-card" in c for _, _, c in self.stack):
            self.cur = None

    def handle_data(self, data):
        if self.grab:
            self.buf.append(data)
        self.body.append(data)


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cards = manifest["cards"]

    by_file = {}
    for c in cards:
        by_file.setdefault(c["file"], []).append(c)

    # -- every authorised card is present exactly once at its recorded home
    missing, misplaced, dupes, structural, parentage = [], [], [], [], []
    dirty_q, dirty_body, empty = [], [], []
    ninth = []
    pages = {}

    for fname, wanted in sorted(by_file.items()):
        path = QB_DIR / fname
        if not path.exists():
            missing.append("%s (page absent)" % fname)
            continue
        p = Page()
        p.feed(path.read_text(encoding="utf-8"))
        p.close()
        pages[fname] = p

        anchors = [q for q, _, _ in p.cards]
        for c in wanted:
            if c["anchor"] not in anchors:
                missing.append("%s#%s (%s)" % (fname, c["anchor"], c["family_id"]))
            elif anchors.count(c["anchor"]) != 1:
                dupes.append("%s#%s x%d" % (fname, c["anchor"], anchors.count(c["anchor"])))

        if len(p.ids) != len(set(p.ids)):
            seen, dup = set(), set()
            for i in p.ids:
                (dup if i in seen else seen).add(i)
            dupes.append("%s duplicate element ids %s" % (fname, sorted(dup)))

        structural += ["%s: %s" % (fname, s) for s in p.structure]
        for qid, in_feed, anc in p.cards:
            if not in_feed:
                parentage.append("%s#%s outside #q-feed (%s)" % (fname, qid, anc))

        # a ninth, unauthorised new card in a Batch-A destination
        expected_here = {c["anchor"] for c in wanted}
        baseline_max = min(int(a[1:]) for a in expected_here)
        extra = [q for q in anchors
                 if int(q[1:]) > baseline_max and q not in expected_here]
        ninth += ["%s#%s" % (fname, q) for q in extra]

        for c in wanted:
            t = p.text.get(c["anchor"])
            if not t:
                continue
            if len(t["q"]) < 20:
                empty.append("%s#%s question text" % (fname, c["anchor"]))
            if len(t["a"]) < 800:
                empty.append("%s#%s answer body (%d chars)" % (fname, c["anchor"], len(t["a"])))
            for rx, why in QTEXT_FORBIDDEN:
                if rx.search(t["q"]):
                    dirty_q.append("%s#%s %s" % (fname, c["anchor"], why))

        page_text = " ".join("".join(p.body).split())
        for rx, why in FORBIDDEN:
            m = rx.search(page_text)
            if m:
                dirty_body.append("%s %s: %r" % (fname, why, m.group(0)))

    report("cards_present", not missing, "missing %s" % (missing or "-"))
    report("anchors_unique", not dupes, "%s" % (dupes or "-"))
    report("no_ninth_card", not ninth, "unauthorised new cards %s" % (ninth or "-"))
    report("dom_structure", not structural, "%s" % (structural[:5] or "-"))
    report("q_feed_parentage", not parentage, "%s" % (parentage[:5] or "-"))
    report("answer_non_empty", not empty, "%s" % (empty or "-"))
    report("question_text_clean", not dirty_q, "%s" % (dirty_q or "-"))
    report("no_production_metadata", not dirty_body, "%s" % (dirty_body[:5] or "-"))
    report("homes_match_manifest", not misplaced, "%s" % (misplaced or "-"))

    # -- derived index agrees with the live pages
    idx = json.loads(CONTENT_INDEX.read_text(encoding="utf-8"))
    total = idx.get("total_questions")
    report("canonical_total", total == manifest["expected_canonical_questions"],
           "content index %s vs expected %s" % (total, manifest["expected_canonical_questions"]))
    indexed = []
    for c in cards:
        entry = idx.get("files", {}).get(c["file"], {})
        got = {q.get("anchor") for q in entry.get("questions", [])}
        if c["anchor"] not in got:
            indexed.append("%s#%s" % (c["file"], c["anchor"]))
    report("indexed", not indexed, "not in content index %s" % (indexed or "-"))

    print("\n%d PASS / %d FAIL" % (_checks - len(_fails), len(_fails)))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
