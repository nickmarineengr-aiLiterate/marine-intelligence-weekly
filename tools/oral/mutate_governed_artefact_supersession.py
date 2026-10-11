#!/usr/bin/env python3
"""Mutation suite for governed whole-file artefact succession (GS-1 .. GS-12).

Every mutation must turn red the check that OWNS its proposition, and must do
so for the intended governance REASON: each expectation names a record, a check
and the reason token the failing detail has to carry. A mutation that turns
some unrelated check red is an escape, not a catch.

TWO LAYERS
----------

HERMETIC (always). A throwaway git repository is built under the sandbox TEMP
directory with real commits -- the root correction, a first successor, a
second successor, a side branch that deletes the protected proposition, and
an orphan branch that reproduces the same bytes with no shared history. The
REAL gate functions run against it (``oral_manifest.audit_succession_schema``
and ``oral_manifest.audit_governed_artefacts_live``, which call the real
resolver with real ``git``). Nothing in the product tree is touched.

LIVE (``--live``). Runs against whatever succession is actually declared on
disk in THIS repository, through ``validate_artefact_governance.py`` -- the
fast probe that shares its pins with ``validate_corrections.py``. Targets are
discovered at runtime, never hardcoded. Every file a mutation touches is held
by ``oral_content_mutation.Snapshot`` and restored byte-exactly in
``finally``. With no succession on disk the live layer has nothing to attack
and says so, and exits 2 rather than reporting a vacuous pass.

POSITIVE CONTROLS
-----------------
Dormant (no succession), one link, two links: every check green, the
predecessor reported as an authorised ancestor of live, the terminal as live.
A control that is not green stops the suite before any mutation runs, so no
mutation can be "caught" by a check that was already failing.
"""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import oral_manifest as M                                         # noqa: E402
from oral_content_mutation import Snapshot                         # noqa: E402

d = M.artefact_digest
SHEET = "meoclass1/QBZ_CheatSheet.html"
OTHER = "meoclass1/QBW_CheatSheet.html"
ROOT_LINE = ("<li>Casualty: cause not settled; most probably liquefaction or a "
             "free-surface effect (flag State found no physical evidence)</li>")
A_LINE = "<li>Fire main: MSC.1/Circ.1472; 2/4 breadth rule for five or more tiers</li>"
B_LINE = "<li>Inclinometer: recorded maximum roll angle</li>"

PAGE = "<html><body>\n<ul>\n%s\n</ul>\n</body></html>\n"
T0 = PAGE % "<li>Casualty: settled bauxite liquefaction sinking</li>"
T1 = PAGE % ROOT_LINE
T2 = PAGE % "\n".join([ROOT_LINE, A_LINE])
T3 = PAGE % "\n".join([ROOT_LINE, A_LINE, B_LINE])
T2X = PAGE % A_LINE                                  # side branch: root line deleted
T9 = PAGE % "\n".join([ROOT_LINE, A_LINE, "<li>unregistered</li>"])
W0 = PAGE % "<li>another cheat sheet</li>"

LIVE_CHECK = "live_matches_authorised_artefact_state"
# The dormant default's failure, and nothing else: the original
# "(live X, authorised Y)" detail with NO resolver status after it. A missing
# declaration must fail as an unexplained drift, not as some chain error.
DORMANT_PIN = r"re:\(live [0-9a-f]{10}, authorised [0-9a-f]{10}\)'\]$"


# --------------------------------------------------------------- fixture


def _git(cwd, *args):
    out = subprocess.run(
        ["git", "-c", "user.name=gas-fixture", "-c", "user.email=gas-fixture@invalid",
         "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false",
         "-c", "init.defaultBranch=main", *args],
        cwd=str(cwd), capture_output=True, text=True, check=True)
    return out.stdout.strip()


class Fixture:
    """A real git repository whose history the chain must be proved against."""

    def __init__(self, root: pathlib.Path):
        self.root = root
        self.dir = root / "tools" / "oral"
        self.dir.mkdir(parents=True)
        (root / "meoclass1").mkdir()
        _git(root, "init", "-q")
        self.c = {}
        self.c["c0"] = self._commit({SHEET: T0, OTHER: W0}, "c0 settled wording")
        self.c["c1"] = self._commit({SHEET: T1}, "c1 root correction")
        self.c["c2"] = self._commit({SHEET: T2}, "c2 first successor")
        self.c["c3"] = self._commit({SHEET: T3}, "c3 second successor")
        _git(root, "checkout", "-q", "-b", "side", self.c["c1"])
        self.c["x2"] = self._commit({SHEET: T2X}, "x2 successor that deletes the root line")
        _git(root, "checkout", "-q", "--orphan", "orphan")
        self.c["o1"] = self._commit({SHEET: T1, OTHER: W0}, "o1 same bytes, no history")
        self.c["o2"] = self._commit({SHEET: T2}, "o2 same bytes, no history")
        _git(root, "checkout", "-q", "main")

    def _commit(self, files, msg):
        for rel, text in files.items():
            (self.root / rel).write_bytes(text.encode("utf-8"))
        _git(self.root, "add", "-A", "meoclass1")
        _git(self.root, "commit", "-q", "-m", msg)
        return _git(self.root, "rev-parse", "HEAD")

    def materialise(self, state):
        for p in self.dir.glob("*.json"):
            p.unlink()
        for name, doc in state["records"].items():
            (self.dir / name).write_text(json.dumps(doc, indent=1), encoding="utf-8")
        for rel, text in state["live"].items():
            (self.root / rel).write_bytes(text.encode("utf-8"))

    def evaluate(self) -> dict:
        """(record, check) -> Finding, over every record in the fixture."""
        out = {}
        for rec in sorted(self.dir.glob(M.CORRECTION_MANIFEST_GLOB)):
            for f in (M.audit_succession_schema(rec, self.root)
                      + M.audit_governed_artefacts_live(rec, self.root)):
                out[(rec.name, f.check)] = f
        return out


R = "correction_corr_gas_fx_root_20260101_manifest.json"
A = "correction_corr_gas_fx_a_20260102_manifest.json"
B = "correction_corr_gas_fx_b_20260103_manifest.json"


def _record(cid, base, gov, **body):
    doc = {"correction_id": cid, "kind": M.CORRECTION_KIND, "status": "AUTHORISED",
           "origin": "gas_fixture", "baseline_commit": base,
           "governing_commits": [gov], "authorisation_source": "fixture",
           "cards": []}
    doc.update(body)
    return doc


def _succ(sid, pre, post, sup_manifest, sup_aid, sup_post, preserved):
    return {"succession_action_id": sid, "path": SHEET, "artefact_type": "CHEAT_SHEET",
            "pre_edit_digest": pre, "post_edit_digest": post,
            "supersedes": {"manifest": sup_manifest, "action_id": sup_aid,
                           "post_edit_digest": sup_post},
            "preserved_propositions": list(preserved),
            "succession_reason": "fixture"}


def scenarios(fx: Fixture) -> dict:
    c = fx.c
    root = _record("CORR-GAS-FX-ROOT-20260101", c["c0"], c["c1"], governed_artefacts=[{
        "correction_action_id": "FX-R-01", "path": SHEET, "artefact_type": "CHEAT_SHEET",
        "classification": "ARTEFACT_PROPAGATION", "governing_correction": "CORR-PARENT",
        "proposition": "cause not settled", "proposition_markers": ["not settled"],
        "propagation_reason": "fixture", "expected_text_after": ROOT_LINE,
        "pre_edit_digest": d(T0), "post_edit_digest": d(T1)}])
    a = _record("CORR-GAS-FX-A-20260102", c["c1"], c["c2"], governed_artefact_successions=[
        _succ("FX-A-01", d(T1), d(T2), R, "FX-R-01", d(T1), [ROOT_LINE])])
    b = _record("CORR-GAS-FX-B-20260103", c["c2"], c["c3"], governed_artefact_successions=[
        _succ("FX-B-01", d(T2), d(T3), A, "FX-A-01", d(T2), [ROOT_LINE, A_LINE])])
    return {
        "dormant": {"records": {R: root}, "live": {SHEET: T1, OTHER: W0}},
        "one": {"records": {R: root, A: a}, "live": {SHEET: T2, OTHER: W0}},
        "two": {"records": {R: root, A: a, B: b}, "live": {SHEET: T3, OTHER: W0}},
    }


def _sa(state, name):                       # the first succession of a record
    return state["records"][name]["governed_artefact_successions"][0]


def _crlf(text):
    return hashlib.sha256(text.replace("\n", "\r\n").encode("utf-8")).hexdigest()


def hermetic_mutations(fx):
    c = fx.c

    def extra(name, cid, base, gov, entry):
        def f(s):
            s["records"][name] = _record(cid, base, gov,
                                         governed_artefact_successions=[entry])
        return f

    F = "correction_corr_gas_fx_fork_20260104_manifest.json"
    F2 = "correction_corr_gas_fx_dup_20260105_manifest.json"

    def cycle(s):
        _sa(s, A).update(pre_edit_digest=d(T3))
        _sa(s, A)["supersedes"] = {"manifest": B, "action_id": "FX-B-01",
                                   "post_edit_digest": d(T3)}

    def own(s):
        _sa(s, A)["supersedes"] = {"manifest": A, "action_id": "FX-A-01",
                                   "post_edit_digest": d(T2)}

    def side(s):
        s["records"][A]["governing_commits"] = [c["x2"]]
        _sa(s, A)["post_edit_digest"] = d(T2X)
        s["live"][SHEET] = T2X

    def orphan(s):
        s["records"][A]["baseline_commit"] = c["o1"]
        s["records"][A]["governing_commits"] = [c["o2"]]

    return [
        ("GS-1a", "missing successor declaration (key removed)", "one",
         lambda s: s["records"][A].pop("governed_artefact_successions"),
         [(R, LIVE_CHECK, DORMANT_PIN)]),
        ("GS-1b", "successor declares no supersedes", "one",
         lambda s: _sa(s, A).pop("supersedes"),
         [(R, LIVE_CHECK, "MALFORMED_CLAIM"), (A, "succession_identity_complete", None),
          (A, "succession_target_is_governed", "MISSING_ANCESTOR")]),
        ("GS-2", "incorrect ancestor digest in the claim", "one",
         lambda s: _sa(s, A)["supersedes"].update(post_edit_digest="e" * 64),
         [(R, LIVE_CHECK, "MISSING_ANCESTOR"),
          (A, "succession_live_or_descended", "MISSING_ANCESTOR")]),
        ("GS-2b", "claim names a predecessor action that does not exist", "one",
         lambda s: _sa(s, A)["supersedes"].update(action_id="FX-R-99"),
         [(R, LIVE_CHECK, "MISSING_ANCESTOR"),
          (A, "succession_target_is_governed", "MISSING_ANCESTOR")]),
        ("GS-2c", "claim names a predecessor record that does not exist", "one",
         lambda s: _sa(s, A)["supersedes"].update(
             manifest="correction_corr_gone_20260101_manifest.json"),
         [(R, LIVE_CHECK, "MISSING_ANCESTOR"),
          (A, "succession_target_is_governed", "MISSING_ANCESTOR")]),
        ("GS-3", "tampered predecessor: pin rebaselined to the live state", "one",
         lambda s: s["records"][R]["governed_artefacts"][0].update(post_edit_digest=d(T2)),
         [(R, LIVE_CHECK, "MISSING_ANCESTOR"),
          (R, "governing_commits_produced_artefact_state", None)]),
        ("GS-4", "incorrect successor pre-digest", "one",
         lambda s: _sa(s, A).update(pre_edit_digest=d(T0)),
         [(R, LIVE_CHECK, "CHAIN_BREAK"), (A, "succession_pre_matches_baseline", None)]),
        ("GS-5a", "succession pointed at another cheat sheet", "one",
         lambda s: _sa(s, A).update(path=OTHER),
         [(R, LIVE_CHECK, "PATH_MISMATCH"),
          (A, "succession_target_is_governed", "PATH_MISMATCH")]),
        ("GS-5b", "succession declares another artefact type", "one",
         lambda s: _sa(s, A).update(artefact_type="NOTES_PAGE"),
         [(R, LIVE_CHECK, "TYPE_MISMATCH"),
          (A, "succession_target_is_governed", "TYPE_MISMATCH")]),
        ("GS-6", "fork: a second successor with a different post", "one",
         extra(F, "CORR-GAS-FX-FORK-20260104", c["c1"], c["c3"],
               _succ("FX-F-01", d(T1), d(T3), R, "FX-R-01", d(T1), [ROOT_LINE])),
         [(R, LIVE_CHECK, "CHAIN_FORK"), (A, "succession_live_or_descended", "CHAIN_FORK")]),
        ("GS-6b", "duplicate successor in another record, same post", "one",
         extra(F2, "CORR-GAS-FX-DUP-20260105", c["c1"], c["c2"],
               _succ("FX-D-01", d(T1), d(T2), R, "FX-R-01", d(T1), [ROOT_LINE])),
         [(R, LIVE_CHECK, "CHAIN_FORK")]),
        ("GS-7", "cycle: A supersedes B, B supersedes A", "two", cycle,
         [(R, LIVE_CHECK, "CHAIN_CYCLE"), (B, "succession_live_or_descended", "CHAIN_CYCLE")]),
        ("GS-7b", "a succession naming its own record", "one", own,
         [(R, LIVE_CHECK, "CHAIN_CYCLE"), (A, "succession_does_not_supersede_own_record", None)]),
        ("GS-8a", "predecessor proposition deleted from the live file", "one",
         lambda s: s["live"].__setitem__(SHEET, T2.replace(ROOT_LINE + "\n", "")),
         [(A, "succession_preserves_predecessor_propositions", "absent_live=['"),
          (R, LIVE_CHECK, "TERMINAL_NOT_LIVE")]),
        ("GS-8b", "successor declaration drops the predecessor proposition", "one",
         lambda s: _sa(s, A).update(preserved_propositions=[A_LINE]),
         [(A, "succession_preserves_predecessor_propositions", "dropped=['"),
          (R, LIVE_CHECK, "PROPOSITION_NOT_PRESERVED")]),
        ("GS-8c", "successor's governing commit deleted the proposition", "one", side,
         [(R, LIVE_CHECK, "PROPOSITION_NOT_PRESERVED"),
          (A, "succession_preserves_predecessor_propositions", "absent_live=['")]),
        ("GS-8d", "two links: second link drops the ROOT proposition", "two",
         lambda s: _sa(s, B).update(preserved_propositions=[A_LINE]),
         [(R, LIVE_CHECK, "PROPOSITION_NOT_PRESERVED"),
          (B, "succession_preserves_predecessor_propositions", "dropped=['")]),
        ("GS-9", "unregistered live edit after the terminal state", "one",
         lambda s: s["live"].__setitem__(SHEET, T9),
         [(R, LIVE_CHECK, "TERMINAL_NOT_LIVE"),
          (A, "succession_live_or_descended", "TERMINAL_NOT_LIVE")]),
        ("GS-9b", "unregistered live edit after a TWO-link terminal", "two",
         lambda s: s["live"].__setitem__(SHEET, T3 + "<!-- x -->\n"),
         [(R, LIVE_CHECK, "TERMINAL_NOT_LIVE"),
          (B, "succession_live_or_descended", "TERMINAL_NOT_LIVE")]),
        ("GS-10a", "unknown field in the supersedes claim", "one",
         lambda s: _sa(s, A)["supersedes"].update(waiver=True),
         [(A, "succession_fields_known", "UNKNOWN_FIELD"), (R, LIVE_CHECK, "UNKNOWN_FIELD")]),
        ("GS-10b", "unknown field on the succession entry", "one",
         lambda s: _sa(s, A).update(grandfathered=True),
         [(A, "succession_fields_known", "UNKNOWN_FIELD"), (R, LIVE_CHECK, "UNKNOWN_FIELD")]),
        ("GS-11a", "successor record status=SUPERSEDED", "one",
         lambda s: s["records"][A].update(status="SUPERSEDED"),
         [(A, "succession_record_is_authorised", None), (R, LIVE_CHECK, "UNAUTHORISED_LINK")]),
        ("GS-11b", "successor record status=DRAFT", "one",
         lambda s: s["records"][A].update(status="DRAFT"),
         [(A, "succession_record_is_authorised", None), (R, LIVE_CHECK, "UNAUTHORISED_LINK")]),
        ("GS-11c", "predecessor record status=SUPERSEDED", "one",
         lambda s: s["records"][R].update(status="SUPERSEDED"),
         [(A, "succession_live_or_descended", "UNAUTHORISED_LINK")]),
        ("GS-12a", "16-char card-style digests", "one",
         lambda s: _sa(s, A).update(pre_edit_digest=d(T1)[:16], post_edit_digest=d(T2)[:16]),
         [(A, "succession_digest_convention", "DIGEST_CONVENTION_MISMATCH"),
          (R, LIVE_CHECK, "DIGEST_CONVENTION_MISMATCH")]),
        ("GS-12b", "post digest over raw CRLF bytes, not LF-normalised", "one",
         lambda s: _sa(s, A).update(post_edit_digest=_crlf(T2)),
         [(A, "succession_post_produced_by_governing_commit", None),
          (R, LIVE_CHECK, "HISTORY_MISMATCH")]),
        ("GS-H1", "successor baseline commit does not hold its pre-state", "one",
         lambda s: s["records"][A].update(baseline_commit=c["c0"]),
         [(A, "succession_pre_matches_baseline", None), (R, LIVE_CHECK, "HISTORY_MISMATCH")]),
        ("GS-H2", "successor governing commit does not hold its post-state", "one",
         lambda s: s["records"][A].update(governing_commits=[c["c1"]]),
         [(A, "succession_post_produced_by_governing_commit", None),
          (R, LIVE_CHECK, "HISTORY_MISMATCH")]),
        ("GS-H3", "same bytes on an orphan branch: no shared history", "one", orphan,
         [(R, LIVE_CHECK, "HISTORY_MISMATCH"),
          (A, "succession_live_or_descended", "does not descend")]),
    ]


def _caught(findings, expectations):
    misses = []
    for rec, check, token in expectations:
        f = findings.get((rec, check))
        if f is None:
            misses.append("%s:%s not reported" % (rec[:28], check))
        elif f.ok:
            misses.append("%s:%s PASS" % (rec[:28], check))
        elif token and token.startswith("re:"):
            if not re.search(token[3:], f.detail):
                misses.append("%s:%s red, but not as %s" % (rec[:28], check, token))
        elif token and token not in f.detail:
            misses.append("%s:%s red without %s" % (rec[:28], check, token))
    return misses


def run_hermetic() -> tuple:
    title = "Governed artefact succession -- HERMETIC (real git fixture)"
    print(title)
    print("=" * len(title))
    tmp = tempfile.mkdtemp(prefix="gas_fixture_")
    try:
        fx = Fixture(pathlib.Path(tmp) / "repo")
        sc = scenarios(fx)

        # ---- positive controls ---------------------------------------
        controls_ok = True
        for name in ("dormant", "one", "two"):
            fx.materialise(copy.deepcopy(sc[name]))
            got = fx.evaluate()
            red = sorted("%s:%s" % (k[0][:28], k[1]) for k, f in got.items() if not f.ok)
            live = got.get((R, LIVE_CHECK))
            if name == "dormant":
                shape = live is not None and live.detail == "drifted=none"
            else:
                shape = (live is not None and "authorised_ancestor_of_live" in live.detail
                         and all(got[(x, "succession_live_or_descended")].ok
                                 for x in sc[name]["records"] if x != R))
            ok = not red and shape and bool(got)
            controls_ok &= ok
            print("CONTROL %-8s %-6s %d checks; root: %s"
                  % (name, "GREEN" if ok else "RED", len(got),
                     (live.detail[:120] if live else "-") if not red else red))
        if not controls_ok:
            print("control is not green; no mutation is run")
            return 0, ["CONTROL"], [], []

        # ---- mutations -------------------------------------------------
        muts = hermetic_mutations(fx)
        caught, escapes, crashes, noops = 0, [], [], []
        for mid, desc, base, apply, expectations in muts:
            state = copy.deepcopy(sc[base])
            try:
                apply(state)
                # A mutation that changes nothing proves nothing, and looks
                # identical to a catch if the gate is red for another reason.
                if state == sc[base]:
                    noops.append(mid)
                    print("%-6s %-58s NO-OP" % (mid, desc))
                    continue
                fx.materialise(state)
                got = fx.evaluate()
            except Exception as exc:                          # noqa: BLE001
                crashes.append("%s: %s" % (mid, exc))
                print("%-6s %-58s CRASH   [%s]" % (mid, desc, exc))
                continue
            misses = _caught(got, expectations)
            if misses:
                escapes.append("%s %s" % (mid, misses))
            else:
                caught += 1
            print("%-6s %-58s %s  %s" % (mid, desc[:58], "ESCAPED" if misses else "CAUGHT ",
                                         misses or ", ".join(
                                             "%s[%s]" % (c, t or "red")
                                             for _r, c, t in expectations)))
        print("\n%d caught of %d" % (caught, len(muts)))
        print("%d mutations, %d escape(s), %d no-op(s), %d crash(es)"
              % (len(muts), len(escapes), len(noops), len(crashes)))
        return caught, escapes, crashes + noops, muts
    finally:
        _remove_tree(tmp)


def _remove_tree(path):
    """git marks object files read-only; on Windows rmtree then fails, and
    ignore_errors would silently strand the fixture in TEMP."""
    import os
    import stat

    def unlock(func, p, _exc):
        os.chmod(p, stat.S_IWRITE)
        func(p)

    shutil.rmtree(path, onexc=unlock)
    if pathlib.Path(path).exists():
        print("WARNING: fixture not removed: %s" % path)


# ------------------------------------------------------------------ live


PROBE = "validate_artefact_governance.py"


def run_probe() -> dict:
    out = subprocess.run([sys.executable, str(HERE / PROBE)], cwd=str(REPO),
                         capture_output=True, check=False)
    text = (out.stdout + out.stderr).decode("utf-8", "replace")
    findings, record = {}, "-"
    for line in text.splitlines():
        m = re.match(r"^=== (\S+) ===$", line)
        if m:
            record = m.group(1)
            continue
        m = re.match(r"^(PASS|FAIL)\s+(\S+)\s?(.*)$", line)
        if m:
            findings[(record, m.group(2))] = M.Finding(record, m.group(2),
                                                       m.group(1) == "PASS", m.group(3))
    return findings


def live_targets():
    """The first succession declared on disk, and what it supersedes."""
    for path in sorted(HERE.glob(M.CORRECTION_MANIFEST_GLOB)):
        doc = json.loads(path.read_text(encoding="utf-8"))
        for s in doc.get(M.GOVERNED_ARTEFACT_SUCCESSION_FIELD) or []:
            pred = HERE / s["supersedes"]["manifest"]
            return path, s, pred
    return None


def run_live() -> tuple:
    title = "Governed artefact succession -- LIVE (on-disk succession, %s)" % PROBE
    print(title)
    print("=" * len(title))
    target = live_targets()
    if target is None:
        print("no governed_artefact_successions declared on disk: the live layer has "
              "nothing to attack. This is NOT a pass.")
        return None
    srec, succ, prec = target
    S, P = srec.name, prec.name
    sheet = REPO / succ["path"]
    pdoc = json.loads(prec.read_text(encoding="utf-8"))
    pentry = next(a for a in pdoc["governed_artefacts"]
                  if a["correction_action_id"] == succ["supersedes"]["action_id"])
    sdoc0 = json.loads(srec.read_text(encoding="utf-8"))
    others = sorted(p for p in (REPO / "meoclass1").glob("*CheatSheet.html")
                    if p != sheet)
    other_rel = "meoclass1/" + others[0].name
    fork = HERE / "correction_corr_gas_mutation_fork_20261010_manifest.json"
    cyc_x = HERE / "correction_corr_gas_mutation_cyc_x_20261010_manifest.json"
    cyc_y = HERE / "correction_corr_gas_mutation_cyc_y_20261010_manifest.json"
    watched = [srec, prec, sheet, fork, cyc_x, cyc_y]
    print("successor %s/%s -> predecessor %s/%s on %s"
          % (S, succ["succession_action_id"], P, pentry["correction_action_id"],
             succ["path"]))

    def edit(path, fn):
        def apply():
            doc = json.loads(path.read_text(encoding="utf-8"))
            fn(doc)
            path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n",
                            encoding="utf-8", newline="\n")
        return apply

    def s0(doc):
        return doc[M.GOVERNED_ARTEFACT_SUCCESSION_FIELD][0]

    def sub(old, new):
        def apply():
            text = sheet.read_text(encoding="utf-8", newline="")
            assert old in text, "mutation target absent: %r" % old[:60]
            sheet.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")
        return apply

    def write(path, doc):
        def apply():
            path.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8", newline="\n")
        return apply

    def synthetic(cid, entry):
        doc = dict(sdoc0)
        doc.update(correction_id=cid, cards=[])
        doc.pop("governed_artefacts", None)
        doc[M.GOVERNED_ARTEFACT_SUCCESSION_FIELD] = [entry]
        return doc

    pin = pentry["post_edit_digest"]
    fork_entry = dict(succ, succession_action_id="GASMUT-F-01", post_edit_digest="f" * 64)
    x_post, y_post = "1" * 64, "2" * 64
    cx = dict(succ, succession_action_id="GASMUT-X-01", pre_edit_digest=y_post,
              post_edit_digest=x_post,
              supersedes={"manifest": cyc_y.name, "action_id": "GASMUT-Y-01",
                          "post_edit_digest": y_post})
    cy = dict(succ, succession_action_id="GASMUT-Y-01", pre_edit_digest=x_post,
              post_edit_digest=y_post,
              supersedes={"manifest": cyc_x.name, "action_id": "GASMUT-X-01",
                          "post_edit_digest": x_post})

    def both(*fns):
        def apply():
            for f in fns:
                f()
        return apply

    text = sheet.read_text(encoding="utf-8", newline="")
    crlf = hashlib.sha256(text.replace("\r\n", "\n").replace("\n", "\r\n")
                          .encode("utf-8")).hexdigest()
    muts = [
        ("GS-1a", "missing successor declaration",
         edit(srec, lambda d_: d_.pop(M.GOVERNED_ARTEFACT_SUCCESSION_FIELD)),
         [(P, LIVE_CHECK, DORMANT_PIN)]),
        ("GS-1b", "successor declares no supersedes",
         edit(srec, lambda d_: s0(d_).pop("supersedes")),
         [(P, LIVE_CHECK, "MALFORMED_CLAIM"), (S, "succession_identity_complete", None)]),
        ("GS-2", "incorrect ancestor digest",
         edit(srec, lambda d_: s0(d_)["supersedes"].update(post_edit_digest="e" * 64)),
         [(P, LIVE_CHECK, "MISSING_ANCESTOR"),
          (S, "succession_live_or_descended", "MISSING_ANCESTOR")]),
        ("GS-3", "tampered predecessor pin (temporary copy, restored)",
         edit(prec, lambda d_: next(a for a in d_["governed_artefacts"]
                                    if a["correction_action_id"]
                                    == pentry["correction_action_id"]).update(
             post_edit_digest=succ["post_edit_digest"])),
         [(P, LIVE_CHECK, "MISSING_ANCESTOR"),
          (P, "governing_commits_produced_artefact_state", None)]),
        ("GS-4", "incorrect successor pre-digest",
         edit(srec, lambda d_: s0(d_).update(pre_edit_digest=pentry["pre_edit_digest"])),
         [(P, LIVE_CHECK, "CHAIN_BREAK"), (S, "succession_pre_matches_baseline", None)]),
        ("GS-5a", "succession pointed at %s" % other_rel,
         edit(srec, lambda d_: s0(d_).update(path=other_rel)),
         [(P, LIVE_CHECK, "PATH_MISMATCH"),
          (S, "succession_target_is_governed", "PATH_MISMATCH")]),
        ("GS-5b", "succession declares NOTES_PAGE",
         edit(srec, lambda d_: s0(d_).update(artefact_type="NOTES_PAGE")),
         [(P, LIVE_CHECK, "TYPE_MISMATCH"),
          (S, "succession_target_is_governed", "TYPE_MISMATCH")]),
        ("GS-6", "fork: a second record supersedes the same pin",
         write(fork, synthetic("CORR-GAS-MUTATION-FORK-20261010", fork_entry)),
         [(P, LIVE_CHECK, "CHAIN_FORK"), (S, "succession_live_or_descended", "CHAIN_FORK")]),
        ("GS-7", "cycle: X supersedes Y, Y supersedes X",
         both(write(cyc_x, synthetic("CORR-GAS-MUTATION-CYC-X-20261010", cx)),
              write(cyc_y, synthetic("CORR-GAS-MUTATION-CYC-Y-20261010", cy))),
         [(P, LIVE_CHECK, "CHAIN_CYCLE"), (S, "succession_live_or_descended", "CHAIN_CYCLE")]),
        ("GS-8a", "predecessor proposition deleted from the live file",
         sub(pentry["expected_text_after"], ""),
         [(S, "succession_preserves_predecessor_propositions", "absent_live=['"),
          (P, LIVE_CHECK, "TERMINAL_NOT_LIVE")]),
        ("GS-8b", "declaration drops the predecessor proposition",
         edit(srec, lambda d_: s0(d_).update(preserved_propositions=["<li>"])),
         [(S, "succession_preserves_predecessor_propositions", "dropped=['"),
          (P, LIVE_CHECK, "PROPOSITION_NOT_PRESERVED")]),
        ("GS-9", "unregistered live edit after the terminal state",
         sub("</body>", "<!-- gas-mutation: unregistered -->\n</body>"),
         [(P, LIVE_CHECK, "TERMINAL_NOT_LIVE"),
          (S, "succession_live_or_descended", "TERMINAL_NOT_LIVE")]),
        ("GS-10a", "unknown field in the claim",
         edit(srec, lambda d_: s0(d_)["supersedes"].update(waiver=True)),
         [(S, "succession_fields_known", "UNKNOWN_FIELD"), (P, LIVE_CHECK, "UNKNOWN_FIELD")]),
        ("GS-10b", "unknown field on the entry",
         edit(srec, lambda d_: s0(d_).update(grandfathered=True)),
         [(S, "succession_fields_known", "UNKNOWN_FIELD"), (P, LIVE_CHECK, "UNKNOWN_FIELD")]),
        ("GS-11a", "successor status=SUPERSEDED",
         edit(srec, lambda d_: d_.update(status="SUPERSEDED")),
         [(S, "succession_record_is_authorised", None), (P, LIVE_CHECK, "UNAUTHORISED_LINK")]),
        ("GS-11b", "successor status=DRAFT",
         edit(srec, lambda d_: d_.update(status="DRAFT")),
         [(S, "succession_record_is_authorised", None), (P, LIVE_CHECK, "UNAUTHORISED_LINK")]),
        ("GS-12a", "16-char card-style digests",
         edit(srec, lambda d_: s0(d_).update(pre_edit_digest=pin[:16],
                                             post_edit_digest=succ["post_edit_digest"][:16])),
         [(S, "succession_digest_convention", "DIGEST_CONVENTION_MISMATCH"),
          (P, LIVE_CHECK, "DIGEST_CONVENTION_MISMATCH")]),
        ("GS-12b", "post digest over raw CRLF bytes",
         edit(srec, lambda d_: s0(d_).update(post_edit_digest=crlf)),
         [(S, "succession_post_produced_by_governing_commit", None),
          (P, LIVE_CHECK, "HISTORY_MISMATCH")]),
        ("GS-H1", "successor baseline set to the predecessor's own baseline",
         edit(srec, lambda d_: d_.update(baseline_commit=pdoc["baseline_commit"])),
         [(S, "succession_pre_matches_baseline", None), (P, LIVE_CHECK, "HISTORY_MISMATCH")]),
        ("GS-H2", "successor governing commit set to its own baseline",
         edit(srec, lambda d_: d_.update(governing_commits=[d_["baseline_commit"]])),
         [(S, "succession_post_produced_by_governing_commit", None),
          (P, LIVE_CHECK, "HISTORY_MISMATCH")]),
    ]

    before = {p: (hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None)
              for p in watched}
    control = run_probe()
    red = sorted("%s:%s" % k for k, f in control.items() if not f.ok)
    live = control.get((P, LIVE_CHECK))
    if red or live is None or "authorised_ancestor_of_live" not in live.detail:
        print("control is not green: %s" % (red or (live.detail if live else "no live check")))
        return 0, ["CONTROL"], [], muts, before, before
    print("control: %s 0 FAIL; %s: %s\n" % (PROBE, P, live.detail[:150]))

    caught, escapes, crashes, noops = 0, [], [], []
    for mid, desc, apply, expectations in muts:
        snap = Snapshot(watched)
        try:
            try:
                apply()
            except Exception as exc:                          # noqa: BLE001
                crashes.append("%s: %s" % (mid, exc))
                print("%-6s %-58s CRASH   [%s]" % (mid, desc, exc))
                continue
            if not snap.changed():
                noops.append(mid)
                print("%-6s %-58s NO-OP" % (mid, desc))
                continue
            misses = _caught(run_probe(), expectations)
        finally:
            bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return caught, escapes + ["RESTORE"], crashes, muts, before, before
        if misses:
            escapes.append("%s %s" % (mid, misses))
        else:
            caught += 1
        print("%-6s %-58s %s  %s" % (mid, desc[:58], "ESCAPED" if misses else "CAUGHT ",
                                     misses or ", ".join("%s[%s]" % (c, t or "red")
                                                         for _r, c, t in expectations)))
    after = {p: (hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None)
             for p in watched}
    print("\n%d caught of %d" % (caught, len(muts)))
    print("%d mutations, %d escape(s), %d no-op(s), %d crash(es)"
          % (len(muts), len(escapes), len(noops), len(crashes)))
    crashes = crashes + noops
    for p in watched:
        print("custody %-62s %s %s" % (p.name, (before[p] or "absent")[:16],
                                       "restored" if before[p] == after[p] else "CHANGED"))
    return caught, escapes, crashes, muts, before, after


def main(argv) -> int:
    caught, escapes, crashes, muts = run_hermetic()
    rc = 0 if (not escapes and not crashes and caught == len(muts)) else 1
    if "--live" in argv:
        print()
        result = run_live()
        if result is None:
            return 2
        lc, le, lx, lm, before, after = result
        if le or lx or lc != len(lm) or before != after:
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
