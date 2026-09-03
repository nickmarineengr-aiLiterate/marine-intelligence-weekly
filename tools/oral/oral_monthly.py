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
  CLOSING    the corpus as it stood at the last commit before the month ENDED,
             read the same way. The month is the interval between the two.
  NEW        a card present at CLOSING whose question wording has no counterpart
             in BASELINE -- exact normalised match first, then a same-card
             similarity pass so a REWORDED old question is not counted as new
  UPDATED    a card that existed in the baseline AND was materially changed
             during the month: either its wording was rewritten by CLOSING, or a
             governed batch / correction manifest DATED INSIDE THE MONTH names it
             in a non-creating action

CALENDAR-MONTH BOUNDING -- WHY BOTH ENDS ARE CLOSED
The sheet is titled "<Month> - New & Updated", so it must mean "the qualifying
event belongs to that calendar month", not "everything that has changed since
the month opened". Until 2026-09-04 only the LEFT end was bounded: the wording
test compared the baseline against the LIVE corpus at HEAD, and the manifest
test globbed every manifest on disk with no date filter at all. On the August
2026 sheet read from a 3 September HEAD that put September work into an August
marketing artefact -- fourteen cards built on 1-2 September sold as "New in
August", and ten September correction manifests sold as "Updated in August".

Both ends are now closed, and each limb declares which event date owns it:

  NEW      owned by the CORPUS. A card is new in the month iff its wording is
           absent at BASELINE and present at CLOSING. No manifest date is
           consulted, because the corpus is the product: the qualifying event is
           the commit that put the question in front of a candidate.
  UPDATED  owned by the CORPUS for the wording-rewrite limb (baseline wording !=
           closing wording), and by the MANIFEST EVENT DATE for the governed
           non-wording limb -- an enrichment or correction that changes a card's
           body without touching its stem is invisible to a wording diff, which
           is the whole reason that limb exists.

MANIFEST EVENT DATE
Correction manifests declare `date`; batch manifests do not. The event date is
therefore the declared `date` where one exists, and otherwise the committer date
of the commit that FIRST ADDED the manifest file. The two streams are
cross-checked wherever both exist -- on the 24 correction manifests of August
and September 2026 they agree to the day -- and a disagreement that crosses a
month boundary is a hard failure, because that is the only disagreement that can
change which sheet a row lands on. A manifest that is neither committed nor
dated fails closed: a governance record must be able to say when it happened.

A later event never rewrites an earlier one. A card created in August and
corrected in September stays an August NEW row: the September correction is out
of the window, and NEW outranks UPDATED for the same card in any case.

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
    # The two H-series words. Both are UPDATES, and that is evidence rather
    # than judgement: each of the two cards carrying them has a real
    # pre_edit_digest matching its batch's baseline commit, so the card
    # demonstrably existed before the action ran. EXPANSION is H3B1-006's
    # bounded widening of QB2_B#q15; CURRENCY_EXPANSION is H4-004's currency
    # limb on QB5_E#q4. Classifying either as a CREATE would mint a new
    # candidate-facing "new question" out of a card the corpus already held,
    # and over-claiming new is the dangerous direction in a marketing artefact.
    "EXPANSION",
    "CURRENCY_EXPANSION",
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


def month_window(month):
    """('2026-08') -> (date(2026, 8, 1), date(2026, 9, 1)).

    Half-open [start, end_exclusive): an event at 2026-09-01 00:00:00 is
    September, never August. Every membership test in this module goes through
    this function so the boundary is stated once."""
    if not re.fullmatch(r"\d{4}-\d{2}", month or ""):
        fail("month must be YYYY-MM, got %r" % (month,))
    y, m = int(month[:4]), int(month[5:])
    return _dt.date(y, m, 1), _dt.date(y + (m == 12), (m % 12) + 1, 1)


def month_bounds(month):
    """('2026-08') -> (date(2026, 8, 1), date(2026, 8, 31)).

    The INCLUSIVE last day, for display only -- 'August 2026 - New & Updated'
    reads better ending on the 31st than on 1 September. Never test membership
    with this; use month_window()."""
    start, end_excl = month_window(month)
    return start, end_excl - _dt.timedelta(days=1)


def in_month(day, month):
    """Half-open calendar membership: start <= day < next month's first day."""
    start, end_excl = month_window(month)
    return start <= day < end_excl


def _commit_before(when, what):
    """The last commit STRICTLY before `when` (a date, treated as midnight).

    git's --until is inclusive of a commit landing exactly on the instant given,
    so the exclusive bound is expressed as the last second of the previous day.
    That one second is the whole difference between a commit at 2026-09-01
    00:00:00 belonging to August and belonging to September.

    --until filters on committer date, so this reports the committer date too:
    reporting the author date of a commit selected by its committer date is how
    a boundary quietly moves by a day."""
    edge = when - _dt.timedelta(days=1)
    out = _git("log", "--format=%H %cd", "--date=short",
               "--until", "%s 23:59:59" % edge.isoformat(), "-1").strip()
    if not out:
        fail("no commit precedes %s: cannot establish %s" % (when, what))
    sha, date = out.split()
    return sha, date


def baseline_commit(month):
    """The last commit before the month opened -- the state the month changed."""
    start, _ = month_window(month)
    return _commit_before(start, "a baseline")


def closing_commit(month):
    """The last commit before the month ENDED -- the state the month reached.

    Returns (sha, date, closed). `closed` is False when that commit is HEAD,
    which means the month has not finished inside this repository: for an
    in-progress month the caller must project the LIVE corpus, because holding
    an open month to its last commit would hide work done today. For a month
    that has closed, the tree at this commit IS the month's product and later
    commits are somebody else's month."""
    _, end_excl = month_window(month)
    sha, date = _commit_before(end_excl, "a closing state")
    head = _git("rev-parse", "HEAD").strip()
    return sha, date, sha != head


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

def _git_added_date(path):
    """The committer date of the commit that FIRST ADDED this file, or None when
    the file has never been committed."""
    out = _git("log", "--diff-filter=A", "--format=%cd", "--date=short", "-1",
               "--", str(path)).strip()
    return _dt.date.fromisoformat(out.splitlines()[0]) if out else None


def manifest_event_date(path, manifest, gid):
    """When this governance record HAPPENED -- (date, source).

    Correction manifests declare `date`; batch manifests do not, so the fallback
    is the committer date of the commit that first added the file. Where both
    exist they are cross-checked, but only to the MONTH: a record dated the 30th
    and committed on the 1st is normal working life, while a record whose two
    dates fall in different months is the one disagreement that can move a row
    onto the wrong sheet, and that is refused."""
    declared = manifest.get("date")
    if declared is not None:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", declared):
            fail("%s: manifest `date` %r is not YYYY-MM-DD" % (gid, declared))
        declared = _dt.date.fromisoformat(declared)
    added = _git_added_date(path)
    if declared and added and (declared.year, declared.month) != (added.year, added.month):
        fail("%s: declared date %s and first-commit date %s fall in different "
             "months -- one of them is wrong, and the difference decides which "
             "monthly sheet its cards appear on" % (gid, declared, added))
    if declared:
        return declared, "declared"
    if added:
        return added, "first-commit"
    fail("%s: no event date -- the manifest declares no `date` and the file is "
         "not committed, so nothing can say which month it belongs to. Add a "
         "`date` field, or commit the manifest." % gid)


def manifest_actions():
    """[(governance_id, kind, canonical_id, event_date)] over every batch and
    correction manifest in tools/oral/. Kind is the per-card action where the
    manifest records one, else the manifest-level kind. The event date is the
    manifest's, not the card's: a manifest is one governance event.

    Every manifest on disk is read, and every kind is classified, regardless of
    date -- the unclassified-kind guard is a governance-vocabulary control and
    must not be narrowed to one month. Date filtering is the caller's job."""
    rows = []
    files = sorted(glob.glob(str(HERE / "batch_*_manifest.json"))) + \
        sorted(glob.glob(str(HERE / "correction_*_manifest.json")))
    for p in files:
        m = json.loads(Path(p).read_text(encoding="utf-8"))
        gid = m.get("batch_id") or m.get("batch") or m.get("correction_id") or Path(p).stem
        top = m.get("kind") or m.get("action_kind")
        when, _src = manifest_event_date(p, m, gid)
        for c in m.get("cards", []):
            kind = c.get("action_kind") or c.get("classification") or c.get("kind") or top
            if kind not in CREATE_KINDS and kind not in UPDATE_KINDS:
                fail("%s: unclassified manifest action kind %r -- add it to "
                     "CREATE_KINDS or UPDATE_KINDS in oral_monthly.py" % (gid, kind))
            rows.append((gid, kind, "%s#%s" % (c["file"][:-5], c["anchor"]), when))
    return rows


# ------------------------------------------------------------------ projection

def project(month, base, closing, current_ids, actions,
            baseline_label="baseline", closing_label="closing"):
    """The month's algebra -- no git, no filesystem, no manifests on disk.

      base        {canonical_id: wording key} at the last commit BEFORE the month
      closing     {canonical_id: wording key} at the last commit before it ENDED
      current_ids the live corpus. A row must resolve to a card a candidate can
                  actually open, so nothing outside this is ever listed.
      actions     [(governance_id, kind, canonical_id, event_date)] over ALL
                  governance records. THIS function applies the month window, so
                  the boundary is exercised by the pure tests rather than only by
                  a repository that happens to hold the right commits.

    Keeping the algebra separate from the evidence-gathering is what makes the
    eight boundary cases in test_oral_monthly.py non-vacuous: each one hands this
    function a two-card corpus and one dated action."""
    start, end_excl = month_window(month)
    live = set(current_ids)
    at_close = set(closing)

    base_keys = collections.defaultdict(list)
    for bid, key in base.items():
        base_keys[key].append(bid)

    carried, candidates = {}, []
    for qid, key in closing.items():
        if key in base_keys:
            carried[qid] = base_keys[key][0]
        else:
            candidates.append(qid)

    # A baseline card nothing carried forward is either gone or reworded.
    matched_keys = {closing[q] for q in carried}
    loose = [(bid, key) for bid, key in base.items() if key not in matched_keys]

    reworded, new_ids = {}, []
    for qid in sorted(candidates):
        key = closing[qid]
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

    # ---------------------------------------------------------------- window
    # The ONLY place a governance record's date is tested. An action outside
    # [start, end_excl) contributes nothing at all: not a row, not an update,
    # not evidence, and not to the completeness cross-check.
    inside = [a for a in actions if start <= a[3] < end_excl]
    outside = [a for a in actions if not (start <= a[3] < end_excl)]
    m_new = {cid for _, kind, cid, _ in inside if kind in CREATE_KINDS}
    m_upd = {cid for _, kind, cid, _ in inside if kind in UPDATE_KINDS}
    evidence = collections.defaultdict(list)
    for gid, kind, cid, when in inside:
        evidence[cid].append("%s/%s@%s" % (gid, kind, when.isoformat()))

    new_set = set(new_ids) & live
    # NEW outranks UPDATED for the same card, so a card created this month and
    # also enriched this month is one row, not two.
    updated_set = (((m_upd & at_close) | set(reworded)) & live) - new_set

    # Cross-check, scoped to the window: a creation this month's governance
    # records claim, that the wording test does not see as new, means one of the
    # two streams is wrong. Never silently prefer either.
    stray = sorted((m_new & at_close & live) - new_set)
    if stray:
        fail("%d in-month manifest NEW_CARD action(s) are not new against the %s "
             "baseline (%s): %s" % (len(stray), month, baseline_label, stray[:5]))

    # Reported rather than silently dropped: a card the month produced or
    # changed that a LATER month withdrew or renumbered off its anchor.
    withdrawn = sorted(((set(new_ids) | set(reworded) | (m_upd & at_close)) - live))
    # An in-month action naming a card that was not on that anchor at the close
    # of the month -- renumbering, which this corpus really does.
    unresolved = sorted(((m_new | m_upd) - at_close))

    def why(qid):
        ev = list(evidence.get(qid, []))
        if qid in reworded:
            ev.append("wording-rewritten-by:%s" % closing_label)
        if qid in new_set and not ev:
            ev.append("absent-from-corpus-at:%s" % baseline_label)
        if not ev:
            ev.append("absent-from-corpus-at:%s" % baseline_label)
        return ev

    start_d, end_d = month_bounds(month)
    return {
        "month": month,
        "month_start": start_d.isoformat(),
        "month_end": end_d.isoformat(),
        "month_end_exclusive": end_excl.isoformat(),
        "new": sorted(new_set),
        "updated": sorted(updated_set),
        "status": {**{q: STATUS_NEW for q in new_set},
                   **{q: STATUS_UPDATED for q in updated_set}},
        "evidence": {q: why(q) for q in sorted(new_set | updated_set)},
        "manifest_new": sorted(m_new),
        "manifest_updated": sorted(m_upd & live),
        "manifest_actions_in_month": len(inside),
        "manifest_actions_out_of_month": len(outside),
        "reworded": reworded,
        "withdrawn_after_month": withdrawn,
        "unresolved_at_close": unresolved,
        "retired": sorted(bid for bid, _ in loose if bid not in set(reworded.values())),
    }


def classify(month, current):
    """current: {canonical_id: display question text} for the live corpus.

    Gathers the two corpus states and every governance record's event date, then
    hands the decision to project(). Raises MonthlyFailure when the two
    independent evidence streams disagree."""
    sha, sha_date = baseline_commit(month)
    base = baseline_cards(sha)
    csha, csha_date, closed = closing_commit(month)
    if closed:
        closing = baseline_cards(csha)
    else:
        # The month has not finished in this repository, so its closing state is
        # whatever the corpus says right now.
        closing = {qid: norm(text) for qid, text in current.items()}

    p = project(month, base, closing, set(current), manifest_actions(),
                baseline_label=sha[:7], closing_label=csha[:7])
    p.update({
        "baseline_commit": sha[:7],
        "baseline_date": sha_date,
        "baseline_questions": len(base),
        "closing_commit": csha[:7],
        "closing_date": csha_date,
        "closing_questions": len(closing),
        "month_closed": closed,
        "current_questions": len(current),
    })
    return p


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
    print("%s: [%s, %s) baseline %s (%s, %d q) -> closing %s (%s, %d q)%s; "
          "live %d q; NEW %d, UPDATED %d, retired %d"
          % (p["month"], p["month_start"], p["month_end_exclusive"],
             p["baseline_commit"], p["baseline_date"], p["baseline_questions"],
             p["closing_commit"], p["closing_date"], p["closing_questions"],
             "" if p["month_closed"] else " [MONTH STILL OPEN: live corpus]",
             p["current_questions"], len(p["new"]), len(p["updated"]),
             len(p["retired"])))
    print("  governance records: %d in month, %d outside"
          % (p["manifest_actions_in_month"], p["manifest_actions_out_of_month"]))
    if p["withdrawn_after_month"]:
        print("  withdrawn after the month (not listed): %s" % p["withdrawn_after_month"])
    if p["unresolved_at_close"]:
        print("  in-month action on a card absent at close: %s" % p["unresolved_at_close"])
    if a.json:
        Path(a.json).write_text(json.dumps(p, indent=1, ensure_ascii=False) + "\n",
                                encoding="utf-8")
        print("wrote %s" % a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
