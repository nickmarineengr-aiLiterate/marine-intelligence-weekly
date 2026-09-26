"""Calendar-month boundary controls for tools/oral/oral_monthly.py.

  PYTHONIOENCODING=utf-8 python tools/oral/test_oral_monthly.py

The sheet is titled "<Month> - New & Updated", so a row must mean "the
qualifying event happened in that calendar month" -- not "this has changed at
some point since the month opened". Until 2026-09-04 only the left end was
bounded, and an August workbook exported from a September HEAD carried 14
September-built cards as August NEW and 8 September corrections as August
UPDATED.

Eight boundary cases are proved here against oral_monthly.project(), the pure
algebra: each hands it a small corpus and a handful of dated actions, so the
control does not depend on the repository happening to hold the right commits.

NON-VACUITY. A boundary test that passes because nothing was ever near the
boundary proves nothing. Every case the fix is supposed to change is run a
second time through _unbounded() -- a faithful reimplementation of the OLD
semantics, no window and the live corpus standing in for the month's closing
state -- and the two must DISAGREE. A case both implementations answer the same
way is reported as vacuous and fails the suite. The four cases where old and new
legitimately agree (1, 2, 5, 8) declare that agreement explicitly instead, so
neither direction can pass by accident.

The last checks run the real repository through classify() and assert the
property that started this: no row on the August sheet rests on evidence dated
outside August.
"""
from __future__ import annotations

import datetime as _dt
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_monthly as MM  # noqa: E402
import oral_lib as L  # noqa: E402

MONTH = "2026-08"
D = _dt.date

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  - " + detail) if detail else ""))


# --------------------------------------------------------------- old semantics

def _unbounded(month, base, closing, current_ids, actions):
    """The pre-2026-09-04 behaviour, kept only to prove the new controls bite.

    Two defects, faithfully reproduced: the wording comparison ran against the
    LIVE corpus rather than the month's closing state, and manifest actions were
    globbed with no date filter at all. Here that is `closing` ignored in favour
    of everything live, and every action forced inside the window."""
    live_as_closing = {q: closing.get(q, base.get(q, "")) for q in current_ids}
    inside = [(g, k, c, D(2026, 8, 15)) for g, k, c, _ in actions]
    return MM.project(month, base, live_as_closing, current_ids, inside)


def rows(p):
    return set(p["new"]) | set(p["updated"])


def case(name, base, closing, current, actions, want_new, want_upd, differs=True):
    """One boundary case, run through both implementations."""
    new = MM.project(MONTH, base, closing, set(current), actions)
    ok = (sorted(new["new"]) == sorted(want_new)
          and sorted(new["updated"]) == sorted(want_upd))
    check(name, ok, "NEW %s UPDATED %s (wanted %s / %s)"
          % (sorted(new["new"]), sorted(new["updated"]),
             sorted(want_new), sorted(want_upd)))

    old = _unbounded(MONTH, base, closing, set(current), actions)
    same = ((sorted(old["new"]), sorted(old["updated"]))
            == (sorted(new["new"]), sorted(new["updated"])))
    if differs:
        check(name + "/non_vacuous", not same,
              "old semantics gave the same answer (NEW %s UPDATED %s), so this "
              "case does not exercise the boundary"
              % (sorted(old["new"]), sorted(old["updated"])))
    else:
        check(name + "/unchanged_by_fix", same,
              "the fix was not supposed to move this case, but old gave NEW %s "
              "UPDATED %s" % (sorted(old["new"]), sorted(old["updated"])))
    return new


SMS = "what is a safety management system"
BUNKER = "how do you bunker safely"

AUG_MID = D(2026, 8, 15)
AUG_END = D(2026, 8, 31)
SEP_1 = D(2026, 9, 1)
SEP_2 = D(2026, 9, 2)


def main():
    A = "QB1_A#q1"
    B = "QB1_A#q2"

    # 1. August NEW event -> NEW. Old semantics agreed; the fix must not move it.
    case("1/august_new_is_new",
         base={}, closing={A: SMS}, current=[A],
         actions=[("H1", "NEW_CARD", A, AUG_END)],
         want_new=[A], want_upd=[], differs=False)

    # 2. July NEW + August correction -> UPDATED.
    case("2/july_card_august_correction_is_updated",
         base={A: SMS}, closing={A: SMS}, current=[A],
         actions=[("CORR-AUG", "PRIMARY_CORRECTION", A, AUG_MID)],
         want_new=[], want_upd=[A], differs=False)

    # 3. August NEW + September correction -> stays August NEW, and the September
    #    correction must not also mint an UPDATED row for the same card.
    #
    #    The ROW STATUS here was never the defect: NEW already outranked UPDATED
    #    for the same card, so both implementations answer NEW. What the old one
    #    got wrong is the PROVENANCE -- it cited a September correction as the
    #    reason an August row was on the sheet, which is how a marketing artefact
    #    ends up unable to say what it is claiming. Non-vacuity therefore lives
    #    on the evidence, and is asserted explicitly rather than by set equality.
    p3_actions = [("H1", "NEW_CARD", A, AUG_END),
                  ("CORR-SEP", "PRIMARY_CORRECTION", A, SEP_2)]
    p3 = case("3/august_new_september_correction_stays_new",
              base={}, closing={A: SMS}, current=[A], actions=p3_actions,
              want_new=[A], want_upd=[], differs=False)
    check("3/september_evidence_absent",
          not any("CORR-SEP" in e for e in p3["evidence"][A]),
          "August NEW row cites September evidence: %s" % p3["evidence"][A])
    p3_old = _unbounded(MONTH, {}, {A: SMS}, {A}, p3_actions)
    check("3/evidence_non_vacuous",
          any("CORR-SEP" in e for e in p3_old["evidence"][A]),
          "old semantics did not cite the September correction either, so this "
          "case does not exercise the window: %s" % p3_old["evidence"][A])

    # 4. July card touched ONLY in September -> off the August sheet entirely.
    case("4/july_card_september_only_is_excluded",
         base={A: SMS}, closing={A: SMS}, current=[A],
         actions=[("CORR-SEP", "PRIMARY_CORRECTION", A, SEP_2)],
         want_new=[], want_upd=[])

    # 5. An August correction on the month's last day -> UPDATED.
    case("5/august_correction_is_updated",
         base={A: SMS}, closing={A: SMS}, current=[A],
         actions=[("CORR-AUG", "PRIMARY_CORRECTION", A, AUG_END)],
         want_new=[], want_upd=[A], differs=False)

    # 6. A September correction -> excluded from August UPDATED.
    case("6/september_correction_is_excluded",
         base={A: SMS}, closing={A: SMS}, current=[A],
         actions=[("CORR-SEP", "PRIMARY_CORRECTION", A, SEP_1)],
         want_new=[], want_upd=[])

    # 7. The month ends exclusively at 1 September 00:00.
    check("7/in_month_last_day", MM.in_month(AUG_END, MONTH))
    check("7/in_month_first_of_next", not MM.in_month(SEP_1, MONTH))
    check("7/in_month_previous_day", not MM.in_month(D(2026, 7, 31), MONTH))
    check("7/window_is_half_open",
          MM.month_window(MONTH) == (D(2026, 8, 1), D(2026, 9, 1)),
          str(MM.month_window(MONTH)))
    on_31 = MM.project(MONTH, {A: SMS}, {A: SMS}, {A},
                       [("G", "PRIMARY_CORRECTION", A, AUG_END)])
    on_01 = MM.project(MONTH, {A: SMS}, {A: SMS}, {A},
                       [("G", "PRIMARY_CORRECTION", A, SEP_1)])
    check("7/midnight_is_the_cut",
          on_31["updated"] == [A] and on_01["updated"] == [],
          "31 Aug -> %s, 1 Sep -> %s" % (on_31["updated"], on_01["updated"]))

    # 8. Several qualifying August events on one card -> ONE row, and NEW wins.
    p8 = case("8/multiple_august_events_one_row",
              base={B: BUNKER}, closing={A: SMS, B: BUNKER}, current=[A, B],
              actions=[("H1", "NEW_CARD", A, AUG_MID),
                       ("E1", "ENRICHMENT", A, AUG_END),
                       ("CORR-AUG", "PRIMARY_CORRECTION", A, AUG_END),
                       ("E1", "ENRICHMENT", B, AUG_MID),
                       ("CORR-AUG", "PRIMARY_CORRECTION", B, AUG_END)],
              want_new=[A], want_upd=[B], differs=False)
    listed = p8["new"] + p8["updated"]
    check("8/no_duplicate_rows", len(listed) == len(set(listed)), str(listed))
    check("8/new_outranks_updated", A not in p8["updated"])
    check("8/all_august_evidence_kept", len(p8["evidence"][A]) == 3,
          str(p8["evidence"][A]))

    teaser_sync_cases()

    # ------------------------------------------------------ the real repository
    idx = json.loads((L.MEO / "qb_content_index.json").read_text(encoding="utf-8"))
    current = {q["id"]: q["text"] for f in idx["files"].values() for q in f["questions"]}
    p = MM.classify(MONTH, current)

    csha, cdate, closed = MM.closing_commit(MONTH)
    check("repo/closing_commit_inside_month", closed and cdate.startswith(MONTH),
          "closing %s %s closed=%s" % (csha[:7], cdate, closed))
    check("repo/baseline_precedes_month", p["baseline_date"] < "2026-08-01",
          p["baseline_date"])
    check("repo/closing_corpus_precedes_live",
          p["closing_questions"] <= p["current_questions"],
          "closing %d live %d" % (p["closing_questions"], p["current_questions"]))

    stamped = [(q, e) for q in sorted(rows(p)) for e in p["evidence"][q] if "@" in e]
    off = [(q, e) for q, e in stamped if not e.split("@")[-1].startswith(MONTH)]
    check("repo/no_out_of_month_evidence", not off,
          "%d row(s) rest on evidence dated outside %s: %s"
          % (len(off), MONTH, off[:3]))
    check("repo/evidence_is_dated", bool(stamped),
          "%d dated evidence string(s)" % len(stamped))
    # If the repository held no out-of-month records at all, every repo check
    # above would pass vacuously.
    check("repo/september_records_are_seen_and_excluded",
          p["manifest_actions_out_of_month"] > 0,
          "%d action(s) in month, %d outside"
          % (p["manifest_actions_in_month"], p["manifest_actions_out_of_month"]))
    check("repo/every_row_is_live",
          not [q for q in rows(p) if q not in current], "")

    teaser_sync_repository(current)

    bad = [n for n, ok, _ in RESULTS if not ok]
    print("\n%d/%d PASS" % (sum(1 for _, ok, _ in RESULTS if ok), len(RESULTS)))
    # The release runner's validator dialect: the second number is the verdict.
    print("%d checks, %d FAIL" % (len(RESULTS), len(bad)))
    if bad:
        print("FAILED: %s" % ", ".join(bad))
    return 1 if bad else 0


# ------------------------------------------------------------------ TEASER_SYNC
#
# TEASER_SYNC is the correction class for a free-sample (SQ/) copy realigned to
# its gated card in the same event. It is dated, NON-COUNTING evidence: the
# candidate-facing change is the gated card's, which the twin already counts.
# Valid only beside exactly one counted gated twin in the same manifest with the
# same file, anchor and pre/post digests. Anything else fails closed.

DIG_PRE = "a" * 64
DIG_POST = "b" * 64


def _gated(aid="X-01", file="QB1_A.html", anchor="q4", kind="PRIMARY_CORRECTION",
           pre=DIG_PRE, post=DIG_POST, path=None):
    return {"correction_action_id": aid, "file": file,
            "path": path or "meoclass1/" + file, "anchor": anchor,
            "classification": kind, "pre_edit_digest": pre, "post_edit_digest": post}


def _teaser(aid="X-02", file="QB1_A.html", anchor="q4", pre=DIG_PRE, post=DIG_POST,
            path=None):
    return {"correction_action_id": aid, "file": file,
            "path": path or "SQ/" + file, "anchor": anchor,
            "classification": "TEASER_SYNC", "pre_edit_digest": pre,
            "post_edit_digest": post}


def _manifest(cards, cid="CORR-X"):
    return {"correction_id": cid, "kind": "POST_RELEASE_CORRECTION", "cards": cards}


def _rows(cards, when=AUG_MID):
    return MM.manifest_rows("CORR-X", _manifest(cards), when)


def expect_ok(name, fn, detail=""):
    try:
        out = fn()
    except Exception as e:  # noqa: BLE001 -- any exception is a failed control
        check(name, False, "raised %s: %s" % (type(e).__name__, e))
        return None
    check(name, True, detail)
    return out


def expect_fail(name, fn, needle):
    """PASS only on a MonthlyFailure whose message names the reason. Any other
    exception (including the helper not existing) is a FAIL, so a crash can
    never pass as a refusal."""
    try:
        fn()
    except MM.MonthlyFailure as e:
        ok = needle.lower() in str(e).lower()
        check(name, ok, ("refused: %s" if ok else
                         "refused, but for the wrong reason (wanted %r): %%s" % needle) % e)
        return
    except Exception as e:  # noqa: BLE001
        check(name, False, "raised %s instead of MonthlyFailure: %s" % (type(e).__name__, e))
        return
    check(name, False, "accepted; it must fail closed (%s)" % needle)


def teaser_sync_cases():
    A = "QB1_A#q4"

    # 9a. valid teaser + valid counted twin -> accepted, and ZERO extra count.
    rows_ok = expect_ok("9a/valid_pair_accepted", lambda: _rows([_gated(), _teaser()]))
    if rows_ok is not None:
        kinds = sorted(k for _, k, _, _ in rows_ok)
        check("9a/teaser_row_is_kept_as_dated_evidence",
              kinds == ["PRIMARY_CORRECTION", "TEASER_SYNC"]
              and all(c == A and w == AUG_MID for _, _, c, w in rows_ok), str(rows_ok))
        with_t = expect_ok("9a/project_accepts_pair",
                           lambda: MM.project(MONTH, {A: SMS}, {A: SMS}, {A}, rows_ok))
        without = MM.project(MONTH, {A: SMS}, {A: SMS}, {A},
                             [r for r in rows_ok if r[1] != "TEASER_SYNC"])
        if with_t is not None:
            check("9a/zero_contribution",
                  (with_t["new"], with_t["updated"]) == (without["new"], without["updated"])
                  == ([], [A]),
                  "with %s/%s without %s/%s" % (with_t["new"], with_t["updated"],
                                                without["new"], without["updated"]))
            check("9a/teaser_is_cited_dated",
                  "CORR-X/TEASER_SYNC@2026-08-15" in with_t["evidence"][A],
                  str(with_t["evidence"][A]))
            check("9a/teaser_not_in_manifest_updated_twice",
                  with_t["manifest_updated"] == [A], str(with_t["manifest_updated"]))
        # A teaser on a card created this month is still NEW, still one row.
        rows_new = _rows([_gated(kind="NEW_CARD"), _teaser()])
        pn = MM.project(MONTH, {}, {A: SMS}, {A}, rows_new)
        check("9a/zero_contribution_on_new_card",
              pn["new"] == [A] and pn["updated"] == [], "%s/%s" % (pn["new"], pn["updated"]))

    # 9b. no twin at all.
    expect_fail("9b/no_twin", lambda: _rows([_teaser()]), "no counted gated twin")
    # a counted card on a DIFFERENT anchor is not a twin
    expect_fail("9b/no_twin_other_card_only",
                lambda: _rows([_gated(anchor="q5"), _teaser()]), "no counted gated twin")

    # 9c. file mismatch -- both directions.
    expect_fail("9c/mismatched_twin_file",
                lambda: _rows([_gated(file="QB1_B.html"), _teaser()]), "no counted gated twin")
    expect_fail("9c/teaser_path_disagrees_with_file",
                lambda: _rows([_gated(), _teaser(path="SQ/QB1_B.html")]), "free-surface")

    # 9d. anchor mismatch.
    expect_fail("9d/mismatched_anchor",
                lambda: _rows([_gated(), _teaser(anchor="q5")]), "no counted gated twin")

    # 9e. digest mismatch -- each digest on its own.
    expect_fail("9e/mismatched_pre_digest",
                lambda: _rows([_gated(), _teaser(pre="c" * 64)]), "pre_edit_digest")
    expect_fail("9e/mismatched_post_digest",
                lambda: _rows([_gated(), _teaser(post="c" * 64)]), "post_edit_digest")
    expect_fail("9e/missing_teaser_digest",
                lambda: _rows([_gated(), _teaser(post="")]), "digest")

    # 9f. ambiguous / duplicate mapping.
    expect_fail("9f/two_gated_twins",
                lambda: _rows([_gated(), _gated(aid="X-03"), _teaser()]), "ambiguous")
    expect_fail("9f/two_teasers_one_twin",
                lambda: _rows([_gated(), _teaser(), _teaser(aid="X-04")]), "already claimed")

    # 9g. the twin must itself be a COUNTED, GATED card.
    # Through a whole manifest the vocabulary guard refuses first; called
    # directly, the twin-kind guard itself must refuse.
    expect_fail("9g/twin_is_not_counted_manifest",
                lambda: _rows([_gated(kind="INDEX_METADATA"), _teaser()]), "unclassified")
    expect_fail("9g/twin_is_not_counted",
                lambda: MM.teaser_sync_twins("CORR-X", [_gated(kind="INDEX_METADATA"),
                                                        _teaser()]),
                "not a counted kind")
    expect_fail("9g/teaser_on_gated_path",
                lambda: _rows([_gated(), _teaser(path="meoclass1/QB1_A.html")]),
                "free-surface")

    # 9h. unknown action kinds fail closed at BOTH layers.
    expect_fail("9h/unknown_kind_in_manifest",
                lambda: _rows([_gated(kind="COSMETIC_TIDY")]), "unclassified")
    expect_fail("9h/unknown_kind_handed_to_project",
                lambda: MM.project(MONTH, {A: SMS}, {A: SMS}, {A},
                                   [("G", "COSMETIC_TIDY", A, AUG_MID)]), "unclassified")

    # 9i. project() refuses an orphan TEASER_SYNC action: without this, the pure
    # layer could be handed a teaser that no counted action backs.
    expect_fail("9i/project_orphan_teaser",
                lambda: MM.project(MONTH, {A: SMS}, {A: SMS}, {A},
                                   [("G", "TEASER_SYNC", A, AUG_MID)]), "counted twin")
    expect_fail("9i/project_teaser_twin_other_event",
                lambda: MM.project(MONTH, {A: SMS}, {A: SMS}, {A},
                                   [("G", "PRIMARY_CORRECTION", A, AUG_MID),
                                    ("H", "TEASER_SYNC", A, AUG_MID)]), "counted twin")

    # 9j. ordinary counted rows are unchanged by the new path: same tuples, same
    # kind resolution (per-card kind, else manifest-level kind).
    plain = _rows([_gated(), _gated(aid="X-05", anchor="q9", kind="SCOPE_PASS_CORRECTION")])
    check("9j/ordinary_rows_unchanged",
          plain == [("CORR-X", "PRIMARY_CORRECTION", A, AUG_MID),
                    ("CORR-X", "SCOPE_PASS_CORRECTION", "QB1_A#q9", AUG_MID)], str(plain))
    batch = MM.manifest_rows("H9", {"batch_id": "H9", "kind": "ENRICHMENT",
                                    "cards": [{"file": "QB1_A.html", "anchor": "q4"}]}, AUG_MID)
    check("9j/manifest_level_kind_unchanged",
          batch == [("H9", "ENRICHMENT", A, AUG_MID)], str(batch))


# The four TEASER_SYNC rows the repository held when this control was written,
# each with the counted gated twin it must resolve to. New rows may be added;
# these may not silently stop resolving.
KNOWN_TEASER_TWINS = {
    ("CORR-NOSDCP-MINISTRY-20260916", "NOSDCP-03"): "NOSDCP-01",
    ("CORR-NOSDCP-MINISTRY-20260916", "NOSDCP-04"): "NOSDCP-02",
    ("CORR-INDIA-OILSPILL-REGULATORY-AUDIT-20260917", "INDIA-OILSPILL-C-02"): "INDIA-OILSPILL-C-01",
    ("CORR-INDIA-OILSPILL-REGULATORY-AUDIT-20260917", "INDIA-OILSPILL-D-03"): "INDIA-OILSPILL-D-02",
}

# August 2026 is a CLOSED month: its baseline and closing trees are fixed
# commits and its governance records are all committed. These are the counts it
# carried before any TEASER_SYNC row existed. A change is not a test to update:
# it means a card was withdrawn or renumbered off its anchor, or a record was
# re-dated, and must be explained first.
AUGUST_2026 = (120, 85)


def teaser_sync_repository(current):
    try:
        pairs = MM.teaser_sync_pairs()
    except Exception as e:  # noqa: BLE001
        check("repo/teaser_pairs_resolve", False, "%s: %s" % (type(e).__name__, e))
        pairs = {}
    missing = {k: v for k, v in KNOWN_TEASER_TWINS.items() if pairs.get(k) != v}
    check("repo/known_teaser_rows_resolve_to_their_twins", not missing,
          "unresolved or re-mapped: %s (found %s)" % (missing, pairs))

    for month in ("2026-08", "2026-09"):
        try:
            acts = MM.manifest_actions()
            p = MM.classify(month, current, actions=acts)
            q = MM.classify(month, current,
                            actions=[a for a in acts if a[1] != "TEASER_SYNC"])
        except Exception as e:  # noqa: BLE001
            check("repo/%s/exports" % month, False, "%s: %s" % (type(e).__name__, e))
            continue
        check("repo/%s/exports" % month, True,
              "NEW %d UPDATED %d" % (len(p["new"]), len(p["updated"])))
        check("repo/%s/teaser_sync_contributes_zero" % month,
              (p["new"], p["updated"]) == (q["new"], q["updated"]),
              "with teasers %d/%d, without %d/%d" % (len(p["new"]), len(p["updated"]),
                                                     len(q["new"]), len(q["updated"])))
        if month == "2026-08":
            got = (len(p["new"]), len(p["updated"]))
            check("repo/2026-08/counts_preserved", got == AUGUST_2026,
                  "NEW/UPDATED %s, historical %s" % (got, AUGUST_2026))
        else:
            n_teaser = sum(1 for a in acts if a[1] == "TEASER_SYNC"
                           and MM.in_month(a[3], month))
            check("repo/2026-09/teaser_rows_are_in_window", n_teaser >= 4,
                  "%d TEASER_SYNC action(s) dated in %s" % (n_teaser, month))


if __name__ == "__main__":
    sys.exit(main())
