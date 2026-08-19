"""Load-bearing validator for meoclass1/qb_content_index.json and the hub
search records it must agree with (Q_INDEX in meoclass1/index.html).

Independence: this file does NOT use oral_lib's regex card parser. It walks
each live QB page with html.parser and counts real candidate-facing q-cards
(div.q-card whose id is q<N>) with its own state machine, so a shared parsing
bug cannot pass both the generator and the validator.

Checks (each is a named PASS/FAIL line; exit 1 on any FAIL):
  count           generated canonical count == independent live q-card count
  files           every live QB page with cards indexed; no non-QB entries
  complete        every live (file, anchor) present; no missing cards
  no_extras       every indexed (file, anchor) exists live (anchor resolves)
  no_nonquestion  no revision/map/nav/cheat card indexed (anchor must be q\\d+)
  unique          file+anchor unique; ids unique
  identity        id == stem#anchor and qnum == int(anchor[1:]) for every record
  text            normalised text == live candidate-facing q-text for every record
  leak            no examiner/production metadata in any indexed text
  qb1k_q8         QB1_K#q8 is IACS Common Structural Rules, no "(Simon sir)"
  csr_distinct    QB1_K#q8 (CSR = Common Structural Rules) and QB5_C_B#q8
                  (Continuous Synopsis Record) are distinct and not swapped
  p0_new          the six P0 canonical anchors are indexed
  p0_enriched     the three enrichment targets carry CURRENT live text
  order           files in natural order; questions in document order
  counts_agree    per-file question_count == len(questions); totals agree
  q_index         index.html Q_INDEX: same records (file, anchor, text) in the
                  same order; per-file counts == manifest; hero counter agrees
  cards           each QB_GROUPS card qcount == manifest question_count
  governed        recently_updated present and non-empty (hub correction log)
  corrections     every correction entry is {date, note, files?}: non-empty
                  note, files a list of str, no summary/files_touched, no dupes
  renderer        index.html correction-log renderer binds to e.date/e.note/
                  e.files only (the key it reads is the key the data carries)
  corrections_preserved
                  manifest recently_updated == governed (verbatim, same order);
                  per-file corrections_applied carried through unchanged
  determinism     a fresh in-memory derivation is byte-identical to disk

  PYTHONIOENCODING=utf-8 python tools/oral/validate_qb_content_index.py \
      [--manifest PATH] [--index-html PATH] [--quiet]

Overrides exist for the mutation harness: live QB HTML is always read from the
repo; only the two derived artefacts under test can be pointed elsewhere.
"""
from __future__ import annotations

import html
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_lib as L                        # noqa: E402  (paths + qb_files only)
import build_qb_content_index as B          # noqa: E402  (determinism check only)

MEO = L.MEO
RESULTS = []
FAILS = []


def report(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    if not ok:
        FAILS.append(name)


# ------------------------------------------------- independent live extraction

class CardWalker(HTMLParser):
    """Collect (anchor, text) for every div.q-card with id q<N>, in document
    order, taking the text of the first div.q-text inside the card."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # depth counter for div nesting
        self.cards = []          # [anchor, text, done]
        self.in_card = None      # index into cards
        self.card_depth = None
        self.in_qtext_depth = None
        self.buf = []
        self.nonq_cards = 0

    def handle_starttag(self, tag, attrs):
        if tag != "div":
            return
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        self.stack.append(tag)
        depth = len(self.stack)
        if "q-card" in cls:
            cid = a.get("id") or ""
            if re.fullmatch(r"q\d+", cid):
                self.cards.append([cid, None])
                self.in_card = len(self.cards) - 1
                self.card_depth = depth
            else:
                self.nonq_cards += 1
                self.in_card = None
                self.card_depth = None
        elif "q-text" in cls and self.in_card is not None and self.cards[self.in_card][1] is None \
                and self.in_qtext_depth is None:
            self.in_qtext_depth = depth
            self.buf = []

    def handle_endtag(self, tag):
        if tag != "div":
            return
        depth = len(self.stack)
        if self.in_qtext_depth is not None and depth == self.in_qtext_depth:
            self.cards[self.in_card][1] = " ".join("".join(self.buf).split())
            self.in_qtext_depth = None
        if self.card_depth is not None and depth == self.card_depth:
            self.in_card = None
            self.card_depth = None
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if self.in_qtext_depth is not None:
            self.buf.append(data)


def live_cards():
    """file -> [(anchor, text), ...] in document order; also nonq count."""
    out = {}
    nonq = 0
    for p in L.qb_files():
        w = CardWalker()
        w.feed(p.read_text(encoding="utf-8"))
        w.close()
        nonq += w.nonq_cards
        if w.cards:
            out[p.name] = [(a, t or "") for a, t in w.cards]
    return out, nonq


def norm(s):
    s = html.unescape(s or "")
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[–—]", "-", s)
    return " ".join(s.split()).strip().lower()


def natural_file_key(fname):
    parts = re.split(r"(\d+)", fname)
    return [int(p) if p.isdigit() else p for p in parts]


# ------------------------------------------------------------------ the checks

P0_NEW = ["QB1_K#q9", "QB1_A#q31", "QB5_D#q3", "QB4_A#q21", "QB4_A#q22", "QB3_J#q6"]
P0_ENRICHED = ["QB6#q10", "QB5_B#q4", "QB7_I#q2"]


def run(manifest_path, index_html_path):
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    index_text = Path(index_html_path).read_bytes().decode("utf-8").replace("\r\n", "\n")
    live, nonq_live = live_cards()
    live_pairs = {(f, a): t for f, rows in live.items() for a, t in rows}
    live_count = len(live_pairs)

    files = manifest.get("files", {})
    recs = []
    for fname, entry in files.items():
        for i, q in enumerate(entry.get("questions", []), 1):
            recs.append((fname, q, i))

    # count
    report("count", len(recs) == live_count,
           "indexed %d vs live q-cards %d (live non-question cards ignored: %d)"
           % (len(recs), live_count, nonq_live))
    report("files", set(files) == set(live),
           "indexed-only %s live-only %s" % (sorted(set(files) - set(live)),
                                            sorted(set(live) - set(files))))
    idx_pairs = {(f, q.get("anchor")) for f, q, _ in recs}
    report("complete", not (set(live_pairs) - idx_pairs),
           "missing %s" % sorted(set(live_pairs) - idx_pairs)[:10])
    report("no_extras", not (idx_pairs - set(live_pairs)),
           "unresolvable %s" % sorted(idx_pairs - set(live_pairs))[:10])
    bad_anchor = [(f, q.get("anchor")) for f, q, _ in recs
                  if not re.fullmatch(r"q\d+", str(q.get("anchor")))]
    report("no_nonquestion", not bad_anchor, "%s" % bad_anchor[:10])
    ids = [q.get("id") for _, q, _ in recs]
    report("unique", len(idx_pairs) == len(recs) and len(set(ids)) == len(recs),
           "%d records, %d unique pairs, %d unique ids" % (len(recs), len(idx_pairs), len(set(ids))))
    ident = [(f, q) for f, q, _ in recs
             if q.get("id") != f[:-5] + "#" + str(q.get("anchor"))
             or not re.fullmatch(r"q\d+", str(q.get("anchor")))
             or q.get("qnum") != int(str(q.get("anchor"))[1:])]
    report("identity", not ident, "%s" % [(f, q.get("id")) for f, q in ident[:10]])

    # text
    drift = [(f, q.get("anchor")) for f, q, _ in recs
             if (f, q.get("anchor")) in live_pairs
             and norm(q.get("text")) != norm(live_pairs[(f, q.get("anchor"))])]
    report("text", not drift, "text drift on %d: %s" % (len(drift), drift[:10]))
    leaks = [(f, q.get("anchor")) for f, q, _ in recs if B.LEAK.search(q.get("text") or "")]
    report("leak", not leaks, "%s" % leaks[:10])

    # QB1_K#q8 and CSR distinction
    by_id = {q.get("id"): q for _, q, _ in recs}
    k8 = by_id.get("QB1_K#q8", {}).get("text", "")
    c8 = by_id.get("QB5_C_B#q8", {}).get("text", "")
    report("qb1k_q8", "CSR" in k8 and "sir" not in k8.lower() and "simon" not in k8.lower()
           and norm(k8) == norm(live_pairs.get(("QB1_K.html", "q8"), "")),
           repr(k8[:90]))
    # Both questions say "CSR"; the acronym resolves differently. The index must
    # keep each text bound to its own anchor: QB1_K#q8's live card is about the
    # IACS Common Structural Rules, QB5_C_B#q8's about the Continuous Synopsis
    # Record. A swap makes each indexed text disagree with its own live card.
    def live_card_body(fname, anchor):
        h = (MEO / fname).read_text(encoding="utf-8")
        m = re.search(r'<div class="q-card[^"]*" id="%s".*?(?=<div class="q-card|\Z)' % anchor, h, re.S)
        return L.strip_tags(m.group(0)) if m else ""
    k8_body = live_card_body("QB1_K.html", "q8")
    c8_body = live_card_body("QB5_C_B.html", "q8")
    k8_bound = "csr" in norm(k8) and "Common Structural Rules" in k8_body \
        and norm(k8) == norm(live_pairs.get(("QB1_K.html", "q8"), ""))
    c8_bound = "csr" in norm(c8) and "Continuous Synopsis Record" in c8_body \
        and "Common Structural Rules" not in c8_body \
        and norm(c8) == norm(live_pairs.get(("QB5_C_B.html", "q8"), ""))
    report("csr_distinct", k8_bound and c8_bound and norm(k8) != norm(c8),
           "QB1_K#q8=%r QB5_C_B#q8=%r" % (k8[:60], c8[:60]))

    # P0
    missing_p0 = [i for i in P0_NEW if i not in by_id]
    report("p0_new", not missing_p0, "missing %s" % missing_p0)
    stale_p0 = []
    for i in P0_ENRICHED:
        f, a = i.split("#")
        lt = live_pairs.get((f + ".html", a))
        if i not in by_id or lt is None or norm(by_id[i].get("text")) != norm(lt):
            stale_p0.append(i)
    report("p0_enriched", not stale_p0, "stale/missing %s" % stale_p0)

    # order
    file_order_ok = list(files) == sorted(files, key=natural_file_key)
    q_order_ok = all([q.get("anchor") for q in files[f].get("questions", [])] == [a for a, _ in live[f]]
                     for f in files if f in live)
    order_field_ok = all(q.get("order") == i for _, q, i in recs)
    report("order", file_order_ok and q_order_ok and order_field_ok,
           "files_natural=%s doc_order=%s order_field=%s" % (file_order_ok, q_order_ok, order_field_ok))

    # counts
    counts_ok = all(e.get("question_count") == len(e.get("questions", [])) for e in files.values())
    tot_ok = manifest.get("total_questions") == len(recs) and manifest.get("total_files") == len(files)
    report("counts_agree", counts_ok and tot_ok,
           "total_questions=%s total_files=%s" % (manifest.get("total_questions"), manifest.get("total_files")))

    # Q_INDEX in index.html
    m = B.Q_INDEX_RE.search(index_text)
    if not m:
        report("q_index", False, "Q_INDEX literal not found")
    else:
        try:
            qi = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            qi = None
            report("q_index", False, "Q_INDEX not JSON: %s" % e)
        if qi is not None:
            want = [(f, q.get("anchor"), norm(q.get("text"))) for f, q, _ in recs]
            got = [(r.get("file"), r.get("anchor"), norm(r.get("q"))) for r in qi]
            hero = B.STAT_RE.search(index_text)
            hero_ok = bool(hero) and int(hero.group(2)) == len(qi) == len(recs)
            leak_qi = [r for r in qi if B.LEAK.search(r.get("q") or "")]
            escaped_qi = [r for r in qi if "&amp;" in (r.get("q") or "") or "&mdash;" in (r.get("q") or "")]
            report("q_index", want == got and hero_ok and not leak_qi and not escaped_qi,
                   "records equal=%s hero=%s leaks=%d html-escaped=%d"
                   % (want == got, hero.group(2) if hero else None, len(leak_qi), len(escaped_qi)))
    gm = B.QB_GROUPS_RE.search(index_text)
    if not gm:
        report("cards", False, "QB_GROUPS not found")
    else:
        cards = {c["file"]: c for g in json.loads(gm.group(1)) for c in g.get("cards", [])}
        bad = [f for f, e in files.items()
               if f not in cards or cards[f].get("qcount") != e.get("question_count")]
        report("cards", not bad, "qcount mismatch/missing card: %s" % bad[:10])

    report("governed", isinstance(manifest.get("recently_updated"), list)
           and len(manifest["recently_updated"]) > 0
           and all("date" in e for e in manifest["recently_updated"]),
           "%d changelog entries" % len(manifest.get("recently_updated") or []))

    # correction-log contract: every entry the hub renders is {date, note,
    # files?} with a non-empty note; obsolete summary/files_touched refused;
    # no duplicates. Independent of B.check_corrections (own walk, own rules).
    ru = manifest.get("recently_updated") or []
    corr_bad = []
    corr_seen = set()
    for i, e in enumerate(ru):
        if not isinstance(e, dict):
            corr_bad.append("[%d] not an object" % i)
            continue
        if any(k in e for k in ("summary", "files_touched")):
            corr_bad.append("[%d] obsolete key" % i)
        if set(e) - {"date", "note", "files"}:
            corr_bad.append("[%d] unknown key %s" % (i, sorted(set(e) - {"date", "note", "files"})))
        if not (isinstance(e.get("note"), str) and e["note"].strip()):
            corr_bad.append("[%d] blank note" % i)
        if "files" in e and not (isinstance(e["files"], list)
                                 and all(isinstance(f, str) and f.strip() for f in e["files"])):
            corr_bad.append("[%d] files not list[str]" % i)
        k = (e.get("date"), (e.get("note") or "").strip())
        if k in corr_seen:
            corr_bad.append("[%d] duplicate" % i)
        corr_seen.add(k)
    report("corrections", not corr_bad, "; ".join(corr_bad[:6]))

    # candidate-facing hygiene: the rendered log must carry no internal
    # workflow / person / chat / repository / AI-tooling vocabulary. Runs on the
    # MANIFEST (what the hub actually fetches), so a generator that re-admits a
    # stale unsafe note is caught here even if the governed source is clean.
    hyg = B.correction_hygiene_violations(ru)
    report("hygiene", not hyg,
           "%d hit(s): %s" % (len(hyg), ["[%d] %s %r" % (i, lab, t) for i, _, lab, t in hyg[:5]]))
    # blank/short notes are not "clean" - every row must still tell the
    # candidate what changed (min 40 chars, at least one QB/notes/page ref
    # or a regulation-shaped token).
    thin = [i for i, e in enumerate(ru)
            if isinstance(e, dict) and (len((e.get("note") or "").strip()) < 40
            or not re.search(r"\bQB\d+_[A-Z]|notes|page|Resolution|Act|Code|SOLAS|MARPOL|citation|corrected|updated|added|fixed",
                             e.get("note") or "", re.I))]
    report("note_quality", not thin, "thin/unspecific rows %s" % thin[:10])

    # the hub renderer must bind to the canonical keys and nothing else
    log_js = re.search(r"async function toggleCorrectionLog\(\)\{.*?\n\}\n", index_text, re.S)
    if not log_js:
        report("renderer", False, "toggleCorrectionLog not found in index.html")
    else:
        js = log_js.group(0)
        ok = ("e.note" in js and "e.files" in js and "e.date" in js
              and "e.summary" not in js and "files_touched" not in js
              and "data.recently_updated" in js)
        report("renderer", ok, "renders e.date/e.note/e.files only" if ok
               else "renderer binds to a non-canonical key")

    # generator preserves the governed correction records verbatim and in order
    try:
        gov = B.load_governed()
        gov_files = gov.get("files", {})
        ca_ok = all((manifest["files"].get(f, {}).get("corrections_applied") or None)
                    == (m.get("corrections_applied") or None)
                    for f, m in gov_files.items() if f in manifest.get("files", {}))
        report("corrections_preserved", ru == gov.get("recently_updated") and ca_ok,
               "recently_updated %s governed; corrections_applied %s"
               % ("==" if ru == gov.get("recently_updated") else "!=", "ok" if ca_ok else "drift"))
    except B.BuildFailure as e:
        report("corrections_preserved", False, "governed file violates contract: %s" % e)

    # determinism / freshness: a fresh derivation equals the artefact under test
    try:
        _, fresh_manifest, fresh_index = B.build()
        same = fresh_manifest == Path(manifest_path).read_bytes().decode("utf-8").replace("\r\n", "\n") \
            and fresh_index == index_text
        report("determinism", same, "fresh derivation %s disk" % ("==" if same else "!="))
    except B.BuildFailure as e:
        report("determinism", False, "generator refused: %s" % e)


def main(argv):
    manifest_path = B.MANIFEST_PATH
    index_html_path = B.INDEX_HTML_PATH
    if "--manifest" in argv:
        manifest_path = Path(argv[argv.index("--manifest") + 1])
    if "--index-html" in argv:
        index_html_path = Path(argv[argv.index("--index-html") + 1])
    quiet = "--quiet" in argv
    run(manifest_path, index_html_path)
    if not quiet:
        for name, ok, detail in RESULTS:
            print("%-16s %s  %s" % (name, "PASS" if ok else "FAIL", detail if (not ok or detail) else ""))
    print("qb_content_index validator: %d checks, %d FAIL%s"
          % (len(RESULTS), len(FAILS), (" -> " + ", ".join(FAILS)) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
