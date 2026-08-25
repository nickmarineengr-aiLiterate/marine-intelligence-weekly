"""Monthly provenance projection for the Oral question bank.

Answers one product question -- "what did MIW add or materially update in a
given calendar month?" -- from governed repository evidence only, so the
candidate-facing "New & Updated" view can never be hand-curated.

WHY THIS IS NOT A GIT "WHEN DID THIS ANCHOR FIRST APPEAR" QUERY
Identity in this corpus is file + anchor, and anchors have been RENUMBERED
(the QB1_A / QB2_A q31->q32 div-nesting repairs of 2026-08-19). Dating a card
by the first commit carrying its anchor id therefore invents new cards out of
renumbered old ones: on the August 2026 corpus that test reported 109 "new"
anchors against 50 governed NEW_CARD manifest actions, and the surplus was
mostly renumbering.

So this module dates the QUESTION, not the anchor:

  BASELINE   the corpus as it stood at the last commit BEFORE the month began,
             read out of the git tree (never the working copy, never mtime)
  NEW        a current card whose question wording has no counterpart in that
             baseline -- exact normalised match first, then a same-card
             similarity pass so a REWORDED old question is not counted as new
  UPDATED    a card that existed in the baseline AND was materially changed
             during the month: either its wording was rewritten, or a governed
             batch / correction manifest names it in a non-creating action

A wording test on its own OVERSTATES "new", which is the dangerous direction
for a marketing artefact, so occupancy is the tie-breaker: a card sitting on an
anchor the baseline already carried existed in the baseline, whatever its
wording now says, and is capped at UPDATED. On the August 2026 corpus that rule
demoted five cards -- the four QB2_C slots whose July q-text was answer
scaffolding rather than a readable question, and one leadership question whose
enrichment fell just under the similarity floor. None of the five is governed
as a creation by any manifest, so the rule cannot contradict governed evidence;
where it is wrong it can only under-claim.

Manifest evidence and corpus evidence are cross-checked rather than trusted
singly: every NEW_CARD manifest action must land in the wording-derived NEW
set, and a disagreement is an error, not a silently preferred source. That
check is what proves the projection is complete -- the manifest regime only
began on 2026-08-19, so a month can legitimately contain new cards no manifest
governs (the eight QB pages published on 2026-08-04), but it can never contain
a manifest-governed new card the wording test disagrees with.

Deliberately NOT counted as an update (a product rule, not a technical one):
regenerated derived indexes, CSS/markup repair, table-of-contents fixes and
validator-only edits. Those move bytes without changing what a candidate
studies, so only manifest actions of a materially-changing kind qualify.
"""
from __future__ import annotations

import collections
import datetime as _dt
import glob
import html as _html
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_lib as L  # noqa: E402

# Manifest action kinds that CREATE a card ...
CREATE_KINDS = {
    "NEW_CARD",
    "NEW_CARD_FROM_GAP",
    "NEW_CARD_FROM_NOTES",
    "NEW_CARD_FROM_EXCEPTION_REVIEW",
}
# ... and the kinds that materially change an existing one. A kind absent from
# BOTH sets is a failure, so a new governance vocabulary word cannot slip into
# the corpus and quietly drop out of the candidate-facing monthly view.
UPDATE_KINDS = {
    "ENRICHMENT",
    "ENRICH_EXISTING",
    "FOLLOWUP",
    "PRIMARY_CORRECTION",
    "SCOPE_PASS_CORRECTION",
    "DEPENDENCY_CORRECTION",
    "PROPAGATED_FACT_CORRECTION",
}

# Below this token overlap a rewritten stem is treated as a different question.
REWORD_SIMILARITY = 0.5

STATUS_NEW = "NEW"
STATUS_UPDATED = "UPDATED"


class MonthlyFailure(Exception):
    pass


def fail(msg):
    raise MonthlyFailure(msg)


# ------------------------------------------------------------------ text keys

_WS_RE = re.compile(r"\s+")
_KEEP_RE = re.compile(r"[^a-z0-9 ]")


def norm(s):
    """Wording key: entities and markup resolved, dashes unified, punctuation and
    case discarded. Presentation-only -- two cards share a key when a reader
    would call them the same question."""
    s = _html.unescape(L.strip_tags(s or ""))
    s = s.replace("—", "-").replace("–", "-").replace("’", "'")
    return _KEEP_RE.sub("", _WS_RE.sub(" ", s).strip().lower())


def _tokens(key):
    return set(key.split())


def _similarity(a, b):
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


# ------------------------------------------------------------------ git

def _git(*args):
    r = subprocess.run(["git", "-C", str(L.REPO)] + list(args),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        fail("git %s failed: %s" % (" ".join(args[:2]), r.stderr.strip()[:200]))
    return r.stdout


def month_bounds(month):
    """('2026-08') -> (date(2026, 8, 1), date(2026, 8, 31))."""
    if not re.fullmatch(r"\d{4}-\d{2}", month or ""):
        fail("month must be YYYY-MM, got %r" % (month,))
    y, m = int(month[:4]), int(month[5:])
    start = _dt.date(y, m, 1)
    end = _dt.date(y + (m == 12), (m % 12) + 1, 1) - _dt.timedelta(days=1)
    return start, end


def baseline_commit(month):
    """The last commit before the month opened -- the state the month changed."""
    start, _ = month_bounds(month)
    out = _git("log", "--format=%H %ad", "--date=short",
               "--until", "%s 00:00:00" % start.isoformat(), "-1").strip()
    if not out:
        fail("no commit precedes %s: cannot establish a baseline" % start)
    sha, date = out.split()
    return sha, date


def _qb_paths_at(commit):
    out = _git("ls-tree", "-r", "--name-only", commit, "meoclass1/")
    return [p for p in out.splitlines()
            if re.fullmatch(r"meoclass1/QB[^/]*\.html", p) and "cheatsheet" not in p.lower()]


def _cards_in(blob):
    """(anchor, raw q-text) for every q-card in one page, using the same card and
    q-text shapes oral_lib parses live pages with."""
    out = []
    matches = list(L.CARD.finditer(blob))
    for i, m in enumerate(matches):
        attrs = dict(L.ATTR.findall(m.group(1)))
        cid = attrs.get("id", "")
        if not re.fullmatch(r"q\d+", cid):
            continue
        end = matches[i + 1].start() if i + 1 < len(matches) else len(blob)
        qm = L.QTEXT.search(blob[m.start():end])
        if qm:
            out.append((cid, L.strip_tags(qm.group(1))))
    return out


_BASELINE_CACHE = {}


def baseline_cards(commit):
    """{canonical_id: wording key} for the whole corpus at one commit."""
    if commit not in _BASELINE_CACHE:
        cards = {}
        for path in _qb_paths_at(commit):
            fname = path.split("/")[-1]
            for anchor, text in _cards_in(_git("show", "%s:%s" % (commit, path))):
                cards["%s#%s" % (fname[:-5], anchor)] = norm(text)
        if not cards:
            fail("baseline commit %s carries no QB cards" % commit[:7])
        _BASELINE_CACHE[commit] = cards
    return _BASELINE_CACHE[commit]


# ------------------------------------------------------------------ manifests

def manifest_actions():
    """[(governance_id, kind, canonical_id)] over every batch and correction
    manifest in tools/oral/. Kind is the per-card action where the manifest
    records one, else the manifest-level kind."""
    rows = []
    files = sorted(glob.glob(str(HERE / "batch_*_manifest.json"))) + \
        sorted(glob.glob(str(HERE / "correction_*_manifest.json")))
    for p in files:
        m = json.loads(Path(p).read_text(encoding="utf-8"))
        gid = m.get("batch_id") or m.get("batch") or m.get("correction_id") or Path(p).stem
        top = m.get("kind") or m.get("action_kind")
        for c in m.get("cards", []):
            kind = c.get("action_kind") or c.get("classification") or c.get("kind") or top
            if kind not in CREATE_KINDS and kind not in UPDATE_KINDS:
                fail("%s: unclassified manifest action kind %r -- add it to "
                     "CREATE_KINDS or UPDATE_KINDS in oral_monthly.py" % (gid, kind))
            rows.append((gid, kind, "%s#%s" % (c["file"][:-5], c["anchor"])))
    return rows


# ------------------------------------------------------------------ projection

def classify(month, current):
    """current: {canonical_id: display question text} for the live corpus.

    Returns a dict with the month's NEW and UPDATED id sets plus the evidence
    behind every one of them. Raises MonthlyFailure when the two independent
    evidence streams disagree."""
    sha, sha_date = baseline_commit(month)
    base = baseline_cards(sha)

    base_keys = collections.defaultdict(list)
    for bid, key in base.items():
        base_keys[key].append(bid)

    cur_keys = {qid: norm(text) for qid, text in current.items()}
    carried, candidates = {}, []
    for qid, key in cur_keys.items():
        if key in base_keys:
            carried[qid] = base_keys[key][0]
        else:
            candidates.append(qid)

    # A baseline card nothing carried forward is either gone or reworded.
    matched_keys = {cur_keys[q] for q in carried}
    loose = [(bid, key) for bid, key in base.items() if key not in matched_keys]

    reworded, new_ids = {}, []
    for qid in sorted(candidates):
        key = cur_keys[qid]
        best = None
        for bid, bkey in loose:
            raw = _similarity(key, bkey)
            # same file+anchor is strong corroboration that this is the same card
            score = raw + (0.15 if bid == qid else 0.0)
            if best is None or score > best[0]:
                best = (score, bid, raw)
        if best and best[2] >= REWORD_SIMILARITY:
            reworded[qid] = best[1]
        elif qid in base:
            # occupancy beats wording: this anchor carried a card before the
            # month opened, so the card is not new however far its text moved
            reworded[qid] = qid
        else:
            new_ids.append(qid)

    actions = manifest_actions()
    m_new = {cid for _, kind, cid in actions if kind in CREATE_KINDS}
    m_upd = {cid for _, kind, cid in actions if kind in UPDATE_KINDS}
    evidence = collections.defaultdict(list)
    for gid, kind, cid in actions:
        evidence[cid].append("%s/%s" % (gid, kind))

    new_set = set(new_ids)
    # Cross-check: a governed creation the wording test does not see as new means
    # one of the two streams is wrong. Never silently prefer either.
    stray = sorted((m_new & set(current)) - new_set)
    if stray:
        fail("%d manifest NEW_CARD action(s) are not new against the %s baseline "
             "(%s): %s" % (len(stray), month, sha[:7], stray[:5]))

    updated_set = ((m_upd & set(current)) | set(reworded)) - new_set

    def why(qid):
        ev = list(evidence.get(qid, []))
        if qid in reworded:
            ev.append("wording-rewritten-since:%s" % sha[:7])
        if not ev:
            ev.append("absent-from-corpus-at:%s" % sha[:7])
        return ev

    start, end = month_bounds(month)
    return {
        "month": month,
        "month_start": start.isoformat(),
        "month_end": end.isoformat(),
        "baseline_commit": sha[:7],
        "baseline_date": sha_date,
        "baseline_questions": len(base),
        "current_questions": len(current),
        "new": sorted(new_set),
        "updated": sorted(updated_set),
        "status": {**{q: STATUS_NEW for q in new_set},
                   **{q: STATUS_UPDATED for q in updated_set}},
        "evidence": {q: why(q) for q in sorted(new_set | updated_set)},
        "manifest_new": sorted(m_new),
        "manifest_updated": sorted(m_upd & set(current)),
        "reworded": reworded,
        "retired": sorted(bid for bid, _ in loose if bid not in set(reworded.values())),
    }


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--month", default="2026-08")
    ap.add_argument("--json", help="write the full projection here")
    a = ap.parse_args(argv)
    idx = json.loads((L.MEO / "qb_content_index.json").read_text(encoding="utf-8"))
    current = {q["id"]: q["text"] for f in idx["files"].values() for q in f["questions"]}
    try:
        p = classify(a.month, current)
    except MonthlyFailure as e:
        print("MONTHLY FAILURE: %s" % e)
        return 2
    print("%s: baseline %s (%s, %d questions) -> %d questions; NEW %d, UPDATED %d, "
          "retired %d" % (p["month"], p["baseline_commit"], p["baseline_date"],
                          p["baseline_questions"], p["current_questions"],
                          len(p["new"]), len(p["updated"]), len(p["retired"])))
    if a.json:
        Path(a.json).write_text(json.dumps(p, indent=1, ensure_ascii=False) + "\n",
                                encoding="utf-8")
        print("wrote %s" % a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
