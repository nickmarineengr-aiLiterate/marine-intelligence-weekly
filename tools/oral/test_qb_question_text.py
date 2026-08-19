"""Candidate-facing question-text and card-nesting controls for the live QB
pages, born from the QB2_C repair of 2026-08-19.

Four QB2_C cards (q1-q4) shipped with answer scaffolding in the q-text slot
("15-Second Answer (Elevator Pitch)**", a truncated "EDITORIAL CORRECTION:**"
note). Every downstream surface - hub search, examiner index, SQ teaser -
copied that text because live HTML is the truth. This gate pins:

  qtext_clean     no q-text on any QB page matches the scaffolding / metadata
                  vocabulary (the generator's LEAK regex + this file's own
                  SCAFFOLD regex, kept independent so one edit cannot loosen both)
  qtext_shape     every q-text is non-empty, contains no raw markdown emphasis
                  and no dangling "**"
  qb2c_repaired   QB2_C q1-q4 carry the approved wording exactly and none of
                  the four old strings survives anywhere in a q-text
  qb2c_answers    the QB2_C answer regions (q-answer .. q-footer) hash to the
                  values recorded at the repair - the questions were fixed, the
                  answers were not
  anchors         every QB page has unique q-card ids and every card id has
                  the shape q<N>
  nesting         a REAL html.parser walk: every q-card is a direct child of
                  div#q-feed (never the sidebar / grid column), and every card
                  owns exactly one q-header and one q-answer as direct
                  children and a q-footer somewhere inside it.  Balanced tag counts are not enough - QB1_K q9
                  proved that.

  PYTHONIOENCODING=utf-8 python tools/oral/test_qb_question_text.py
      [--file PATH ...]   check only these page(s) (mutation harness)
      [--print-hashes]    print the current QB2_C answer hashes
      [--mutate]          run the mutation harness (scratch copies only)

Exit 0 when every control holds (or every mutation is caught).
"""
from __future__ import annotations

import hashlib
import io
import re
import shutil
import sys
import tempfile
from contextlib import redirect_stdout
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_lib as L                        # noqa: E402
import build_qb_content_index as B          # noqa: E402

MEO = L.MEO

# Independent of B.LEAK on purpose (see module docstring).
SCAFFOLD = re.compile(
    r"\b\d+-Second Answer\b|Elevator Pitch|EDITORIAL CORRECTION"
    r"|\bANSWER\b|Examiner context|\bFull Answer\b|\bCE Tip\b|REG-BOX"
    r"|Why this matters|On [Mm]y [Vv]essel|\bGAP-\d|\bP0-\d|\bP0\b"
    r"|\((?:[A-Z][a-z]+ )?[Ss]ir\)|\*\*|\bTODO\b|\bFIXME\b"
)

QB2C = "QB2_C.html"
QB2C_APPROVED = {
    "q1": "What are the latest amendments to SOLAS Chapter II-2 under "
          "MSC.520(106), and when do they enter into force?",
    "q2": "How would you, as Chief Engineer, approach a fire in a container "
          "carrying undeclared dangerous goods?",
    "q3": "How would you fight a container fire when the cargo inside is unknown?",
    "q4": "Explain the water mist lance and portable water monitor — their "
          "construction, working, and the SOLAS carriage requirements.",
}
QB2C_OLD = (
    "EDITORIAL CORRECTION:** MSC.520(106) covers SOLAS Ch II-2 fire safety for "
    "container ships (water mist lance, portable wa",
    "15-Second Answer (Elevator Pitch)**",
)
# sha256 of the normalised answer region of each QB2_C card at the repair.
# Update ONLY with a deliberate answer edit, and say so in the commit.
QB2C_ANSWER_SHA = {
    "q1": "5740f51f26f0b38214e84b36938bc5cd4146575afd20b42f8b4fce3ae325ff67",
    "q2": "79db29e41b6e094a81b7b10a2b61363fbb79d6d3107b90c51bf7af7814eaf6a3",
    "q3": "4071ee0fb4ce771f7e87b0fd901a4dedfcf2cf57d57f43f187250dd231e019e3",
    "q4": "53a9ea1a96ba0443dd57846441411916195829c03652c6bc74194fdf30acf083",
}

FAILURES = []
CHECKS = [0]


def ok(name, cond, detail=""):
    CHECKS[0] += 1
    if not cond:
        FAILURES.append("%s %s" % (name, ("- " + detail) if detail else ""))


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


# --------------------------------------------------------------------------
# a real DOM walk (html.parser), no regex over tag counts
# --------------------------------------------------------------------------
class Walk(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []          # [(tag, attrs-dict, node)]
        self.cards = []          # dicts: id, parent_id, parent_class, children
        self.qtext = {}          # card id -> raw text of its .q-text
        self._qtext_target = None
        self._qtext_depth = 0
        self._buf = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        node = {"tag": tag, "attrs": a, "children": []}
        parent = self.stack[-1][2] if self.stack else None
        if parent is not None:
            parent["children"].append(node)
        if a.get("id"):
            self.ids.append(a["id"])
        cls = (a.get("class") or "").split()
        if tag == "div" and "q-card" in cls:
            self.cards.append({
                "id": a.get("id"), "node": node,
                "parent_id": parent["attrs"].get("id") if parent else None,
                "parent_class": (parent["attrs"].get("class") or "") if parent else "",
                "depth": len(self.stack),
            })
        if tag == "div" and "q-text" in cls and self._qtext_target is None:
            card = self.cards[-1]["id"] if self.cards else None
            self._qtext_target = card
            self._qtext_depth = len(self.stack)
            self._buf = []
        if tag not in self.VOID:
            self.stack.append((tag, a, node))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        # pop to the nearest matching open tag (tolerant of stray closes,
        # which is exactly the defect class we want to see the effect of)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                if (self._qtext_target is not None and tag == "div"
                        and i == self._qtext_depth):
                    self.qtext[self._qtext_target] = "".join(self._buf)
                    self._qtext_target = None
                del self.stack[i:]
                break

    def handle_data(self, d):
        if self._qtext_target is not None:
            self._buf.append(d)

    def handle_entityref(self, name):
        if self._qtext_target is not None:
            self._buf.append("&%s;" % name)

    def handle_charref(self, name):
        if self._qtext_target is not None:
            self._buf.append("&#%s;" % name)


def walk(path):
    w = Walk()
    w.feed(path.read_text(encoding="utf-8"))
    w.close()
    return w


def qcard_children(node):
    out = []
    for c in node["children"]:
        cls = (c["attrs"].get("class") or "").split()
        for k in ("q-header", "q-answer", "q-footer"):
            if k in cls:
                out.append(k)
    return out


def has_descendant(node, klass):
    for c in node["children"]:
        if klass in (c["attrs"].get("class") or "").split():
            return True
        if has_descendant(c, klass):
            return True
    return False


def qb2c_answer_hashes(text):
    starts = [m.start() for m in re.finditer(r'<div class="q-card"', text)]
    end = text.find("<!-- /#q-feed -->")
    starts.append(end if end >= 0 else len(text))
    out = {}
    for i in range(len(starts) - 1):
        card = text[starts[i]:starts[i + 1]]
        a = re.search(r'id="(q\d+)"', card)
        s = card.find('<div class="q-answer">')
        e = card.find('<div class="q-footer">')
        if a and s >= 0 and e > s:
            out[a.group(1)] = hashlib.sha256(card[s:e].encode("utf-8")).hexdigest()
    return out


# --------------------------------------------------------------------------
def check_page(path, is_qb2c):
    fname = path.name
    w = walk(path)
    cards = [c for c in w.cards if c["id"] and re.fullmatch(r"q\d+", c["id"])]
    ids = [c["id"] for c in cards]

    ok("%s anchors unique" % fname, len(ids) == len(set(ids)),
       str([i for i in ids if ids.count(i) > 1][:5]))
    ok("%s ids unique page-wide" % fname, len(w.ids) == len(set(w.ids)),
       str([i for i in w.ids if w.ids.count(i) > 1][:5]))
    ok("%s has q-cards" % fname, bool(cards))

    for c in cards:
        cid = c["id"]
        ok("%s#%s q-card is a direct child of #q-feed" % (fname, cid),
           c["parent_id"] == "q-feed",
           "parent id=%r class=%r" % (c["parent_id"], c["parent_class"]))
        ok("%s#%s q-card is not inside the sidebar" % (fname, cid),
           "sidebar" not in c["parent_class"])
        kids = qcard_children(c["node"])
        # two live templates: q-footer is either a direct child of the card
        # or nested at the end of q-answer; header and answer are always direct
        ok("%s#%s owns one q-header and one q-answer as direct children"
           % (fname, cid),
           kids.count("q-header") == 1 and kids.count("q-answer") == 1, str(kids))
        ok("%s#%s has a q-footer" % (fname, cid),
           has_descendant(c["node"], "q-footer"))
        t = norm(w.qtext.get(cid))
        ok("%s#%s q-text non-empty" % (fname, cid), bool(t))
        ok("%s#%s q-text has no scaffolding (SCAFFOLD)" % (fname, cid),
           not SCAFFOLD.search(t), t[:80])
        ok("%s#%s q-text has no scaffolding (generator LEAK)" % (fname, cid),
           not B.LEAK.search(t), t[:80])
        ok("%s#%s q-text has no dangling markdown emphasis" % (fname, cid),
           "**" not in t and not t.endswith("*"), t[-20:])
        for old in QB2C_OLD:
            ok("%s#%s old QB2_C scaffolding must not return" % (fname, cid),
               old not in t)

    if is_qb2c:
        for a, want in QB2C_APPROVED.items():
            got = norm(w.qtext.get(a))
            ok("QB2_C#%s carries the approved wording" % a, got == want,
               "got %r" % got[:100])
        ok("QB2_C has exactly the four repaired anchors",
           ids == ["q1", "q2", "q3", "q4"], str(ids))
        hashes = qb2c_answer_hashes(path.read_text(encoding="utf-8"))
        for a, want in QB2C_ANSWER_SHA.items():
            ok("QB2_C#%s answer region unchanged since the repair" % a,
               hashes.get(a) == want,
               "have %s" % (hashes.get(a) or "<none>")[:16])


def run(files):
    FAILURES.clear()
    CHECKS[0] = 0
    for p in files:
        check_page(p, p.name == QB2C or p.name.startswith("QB2_C"))
    return list(FAILURES)


# --------------------------------------------------------------------------
# mutation harness - scratch copies of QB2_C only, live HTML never touched
# --------------------------------------------------------------------------
def _m_restore_old(t):
    return t.replace(QB2C_APPROVED["q2"], QB2C_OLD[1], 1)


def _m_examiner_context(t):
    return t.replace(QB2C_APPROVED["q3"],
                     "Examiner context: " + QB2C_APPROVED["q3"], 1)


def _m_answer_body(t):
    return t.replace("400 L/min per monitor", "450 L/min per monitor", 1)


def _m_anchor(t):
    return t.replace('id="q4"', 'id="q5"', 1).replace("#q4\">Q4.", "#q5\">Q4.", 1)


def _m_dup_id(t):
    return t.replace('id="q3"', 'id="q2"', 1)


def _m_wrong_parent(t):
    # close #q-feed early so q4 becomes a sibling of the feed (the QB1_K defect)
    return t.replace('<div class="q-card" id="q4"',
                     '</div><div class="q-card" id="q4"', 1)


def _m_editorial(t):
    return t.replace(QB2C_APPROVED["q1"], "EDITORIAL CORRECTION:** " +
                     QB2C_APPROVED["q1"], 1)


MUTATIONS = [
    ("A restore old scaffolding q-text", _m_restore_old,
     ("old QB2_C scaffolding must not return", "approved wording")),
    ("B inject Examiner context",        _m_examiner_context,
     ("no scaffolding", "approved wording")),
    ("C modify answer body",             _m_answer_body,
     ("answer region unchanged",)),
    ("D change q anchor",                _m_anchor,
     ("exactly the four repaired anchors", "approved wording")),
    ("E duplicate q id",                 _m_dup_id,
     ("anchors unique", "ids unique")),
    ("F card outside #q-feed",           _m_wrong_parent,
     ("direct child of #q-feed",)),
    ("G editorial-note prefix",          _m_editorial,
     ("no scaffolding", "approved wording")),
]


def mutate():
    src = MEO / QB2C
    root = Path(tempfile.mkdtemp(prefix="qb2c-mut-"))
    base = root / "base"
    base.mkdir()
    shutil.copy(src, base / QB2C)
    if run([base / QB2C]):
        print("BASELINE NOT GREEN: %s" % FAILURES[:5])
        return 2
    escapes = 0
    for name, fn, expected in MUTATIONS:
        work = root / name.split()[0]
        work.mkdir()
        t = src.read_text(encoding="utf-8")
        t2 = fn(t)
        if t2 == t:
            print("%-36s ESCAPE  (mutation did not apply)" % name)
            escapes += 1
            continue
        (work / QB2C).write_text(t2, encoding="utf-8")
        try:
            fails = run([work / QB2C])
            crashed = False
        except Exception as e:      # a crash is an escape, not a catch
            fails, crashed = ["<crash: %s>" % e], True
        named = [f for f in fails if any(x in f for x in expected)]
        caught = bool(named) and not crashed
        print("%-36s %s  named=%d  total=%d" % (
            name, "CAUGHT " if caught else "ESCAPE ", len(named), len(fails)))
        if not caught:
            escapes += 1
    shutil.rmtree(root, ignore_errors=True)
    print("mutations: %d run, %d escape(s)" % (len(MUTATIONS), escapes))
    return 1 if escapes else 0


def main(argv):
    if "--print-hashes" in argv:
        for a, h in sorted(qb2c_answer_hashes(
                (MEO / QB2C).read_text(encoding="utf-8")).items()):
            print(a, h)
        return 0
    if "--mutate" in argv:
        return mutate()
    files = []
    if "--file" in argv:
        i = argv.index("--file") + 1
        while i < len(argv) and not argv[i].startswith("--"):
            files.append(Path(argv[i]))
            i += 1
    else:
        files = list(L.qb_files())
    fails = run(files)
    for f in fails:
        print("FAIL  " + f)
    print("\n%d controls / %d failures over %d page(s)"
          % (CHECKS[0], len(fails), len(files)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
