"""Controls for the shared Oral release infrastructure.

These are load-bearing assertions, not smoke tests. Every one exists because
the behaviour it pins was observed to be wrong during production batches
E1-E6, and cost either a wrong release claim or a wasted mutation suite.

  PYTHONIOENCODING=utf-8 python tools/oral/test_oral_release_infra.py

Exit 0 when every control holds. Portability: repo-relative, no drive letters,
no network, no external inputs.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "meoclass1"))

import oral_bytes as B          # noqa: E402
import oral_manifest as M       # noqa: E402
import oral_mutation as X       # noqa: E402

FAILURES = []
CHECKS = [0]


def check(name, ok, detail=""):
    CHECKS[0] += 1
    if not ok:
        FAILURES.append("%s -- %s" % (name, detail))
        print("FAIL %-52s %s" % (name, detail))
    else:
        print("ok   %-52s %s" % (name, detail))


def raises(fn, exc=Exception):
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False


# ===========================================================================
# 1. MUTATION SUMMARY PARSER
#
# The defect this guards: a loose `(\d+)\s*escape` pattern reads the 8 in
# "mutations=8 escapes=0" as the escape count. E5 documented it; E6 wrote the
# fallback order backwards and reproduced it, reporting 8 phantom escapes and
# 4 phantom crashes across a fifteen-suite aggregate.
# ===========================================================================
print("\n--- 1. mutation summary parser ---")

# All six dialects that actually ship in this repo.
DIALECTS = [
    ("gap0609 key=value",
     "mutations=8 escapes=0 no-ops=0 crashes=0", 8, 0, 0, 0),
    ("batch_e1..e6 prose",
     "25 mutations, 0 escape(s), 0 no-op(s), 0 crash(es)", 25, 0, 0, 0),
    ("batch_a..d prose (not applied)",
     "12 mutations, 0 escape(s), 0 not applied, 0 crash(es)", 12, 0, 0, 0),
    ("ce_tip / examiner short",
     "17 mutations, 0 escapes", 17, 0, 0, 0),
    ("phase2 slash",
     "33 mutations / 0 escapes", 33, 0, 0, 0),
    ("qb_content_index run-form",
     "mutations: 26 run, 0 escape(s), 0 crash(es); live artefacts byte-identical: True",
     26, 0, 0, 0),
]

for label, line, run, esc, noop, crash in DIALECTS:
    s = X.parse_summary(line)
    check("dialect parses: %s" % label,
          (s.run, s.escapes, s.no_ops, s.crashes) == (run, esc, noop, crash),
          s.describe())

# THE regression. If this ever reads 8, the E5/E6 defect is back.
s = X.parse_summary("mutations=8 escapes=0 no-ops=0 crashes=0")
check("8 is never misread as the escape count", s.escapes == 0,
      "escapes=%d (must be 0, never 8)" % s.escapes)
check("key=value dialect is recognised as such", s.dialect == "key=value", s.dialect)

# The phantom-crash defect: "fails=2 crash=False" donating its 2.
DETAIL_LOG = """BASELINE GREEN
A   corrupt the limb sentence                    exit=1 fails=2 crash=False  caught
B   corrupt the digest                           exit=1 fails=1 crash=False  caught
mutations=8 escapes=0 no-ops=0 crashes=0
"""
s = X.parse_summary(DETAIL_LOG)
check("per-mutation detail lines are not read as the summary",
      (s.run, s.escapes, s.crashes) == (8, 0, 0), s.describe())
check("fails=2 crash=False donates no crash count", s.crashes == 0,
      "crashes=%d" % s.crashes)

# A baseline banner carrying a crash word but no counts must not be selected.
check("baseline banner is not a summary",
      X.parse_summary("BASELINE NOT GREEN: exit=1 fails=3 crashed=False\n"
                      "10 mutations, 1 escape(s), 0 no-op(s), 0 crash(es)").escapes == 1,
      "escapes read from the real summary line")

# The last qualifying line wins.
s = X.parse_summary("5 mutations, 5 escapes\n9 mutations, 0 escapes")
check("last qualifying line wins", (s.run, s.escapes) == (9, 0), s.describe())

# caught is derived when the harness does not print it.
s = X.parse_summary("25 mutations, 0 escape(s), 0 no-op(s), 0 crash(es)")
check("caught derived when unprinted", s.caught == 25, "caught=%d" % s.caught)
check("green when clean", s.green is True, s.describe())

s = X.parse_summary("10 mutations, 2 escape(s), 1 no-op(s), 0 crash(es)")
check("not green with escapes and no-ops",
      s.green is False and s.escapes == 2 and s.no_ops == 1 and s.caught == 7,
      s.describe())

# Malformed and missing input must raise, never silently return zeros --
# a summary that fails to parse must not read as "0 escapes".
check("malformed summary raises", raises(lambda: X.parse_summary("all done!"), ValueError))
check("empty summary raises", raises(lambda: X.parse_summary(""), ValueError))
check("mutation count without escapes raises",
      raises(lambda: X.parse_summary("12 mutations completed"), ValueError))

agg = X.aggregate([X.parse_summary(d[1]) for d in DIALECTS])
check("aggregate totals structured results",
      (agg.run, agg.escapes, agg.no_ops, agg.crashes) == (121, 0, 0, 0), agg.describe())


# ===========================================================================
# 2. MUTATION PREFLIGHT
#
# The defect this guards: E5 mutation C and E6 mutation H matched nothing,
# wrote nothing, and exercised nothing. E6 burned a 22-minute suite to find it.
# ===========================================================================
print("\n--- 2. mutation preflight ---")

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    B.write_text(root / "card.html", "<strong>resolution MSC.550(108)</strong>\n")

    applied = X.replace_spec("A", "card.html",
                             "<strong>resolution MSC.550(108)</strong>",
                             "<strong>resolution MSC.999(999)</strong>")
    # E6's real mutation H: the tag sits before the word in the markup, so this
    # anchor -- which reads perfectly in prose -- matches nothing.
    noop = X.replace_spec("H", "card.html",
                          "resolution <strong>MSC.550(108)</strong>",
                          "resolution <strong>MSC.999(999)</strong>")
    shrink = X.replace_spec("S", "card.html", "resolution ", "")
    missing = X.replace_spec("Z", "absent.html", "a", "b")
    thrower = X.MutationSpec("T", "card.html",
                             lambda t: (_ for _ in ()).throw(RuntimeError("boom")))

    res = {r.mutation_id: r for r in X.preflight([applied, noop, shrink, missing, thrower],
                                                 root=root)}

    check("applied mutation reports applied", res["A"].applied is True, res["A"].describe())
    check("applied mutation reports byte delta", res["A"].byte_delta == 0, res["A"].describe())
    check("shrinking mutation reports negative delta",
          res["S"].applied and res["S"].byte_delta == -11, res["S"].describe())
    check("E6 mutation-H anchor is caught as a NO-OP", res["H"].applied is False,
          res["H"].describe())
    check("no-op reports zero byte delta", res["H"].byte_delta == 0, res["H"].describe())
    check("missing target reports an error", bool(res["Z"].error), res["Z"].describe())
    check("throwing mutation reports an error", bool(res["T"].error), res["T"].describe())

    # The contract: a suite containing a no-op must NOT launch.
    check("preflight_or_die refuses to launch on a no-op",
          raises(lambda: X.preflight_or_die([applied, noop], root=root, echo=False),
                 AssertionError))
    check("preflight_or_die passes when every mutation applies",
          not raises(lambda: X.preflight_or_die([applied, shrink], root=root, echo=False),
                     AssertionError))

    # Preflight is in-memory: the file on disk must be untouched afterwards.
    check("preflight never writes to disk",
          B.read_text(root / "card.html") == "<strong>resolution MSC.550(108)</strong>\n",
          "target unchanged")


# ===========================================================================
# 3. CONTROL-BYTE SAFETY
#
# The defect this guards: E1 lost a regex \b to a real 0x08 byte and E5 lost a
# \1 backreference to a real 0x01 byte, both through shell heredocs. E6's
# handoff then reproduced BOTH bytes in the paragraph describing them.
# ===========================================================================
print("\n--- 3. control-byte safety ---")

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)

    clean = root / "clean.py"
    clean.write_bytes(b"import re\r\nP = re.compile(r'\\bword\\b')\n\tindented\n")
    check("TAB, LF and CR are permitted", B.scan_control_bytes(clean) == [], "0 hits")

    # E1's byte and E5's byte, in one file, exactly as they arrived on disk.
    dirty = root / "dirty.py"
    dirty.write_bytes(b"P = re.compile('\x08word')\nsub(r'\x011', x)\n")
    hits = B.scan_control_bytes(dirty)
    check("0x08 (E1's lost \\b) is detected",
          any(h.byte == 0x08 for h in hits), "%d hit(s)" % len(hits))
    check("0x01 (E5's lost \\1) is detected", any(h.byte == 0x01 for h in hits),
          "; ".join("0x%02X@%d" % (h.byte, h.offset) for h in hits))
    check("hits carry a line number", all(h.line >= 1 for h in hits), "located")
    check("assert_clean raises on a dirty file",
          raises(lambda: B.assert_clean([dirty]), AssertionError))
    check("assert_clean passes on a clean file",
          not raises(lambda: B.assert_clean([clean]), AssertionError))

    # A prose artefact is release evidence too -- E6 proved that the hard way.
    prose = root / "HANDOFF.md"
    prose.write_bytes("E1 lost a \x08 and E5 lost a \x01.\n".encode("utf-8"))
    check("prose artefacts are scanned, not only executables",
          len(B.scan_control_bytes(prose)) == 2, "2 hits in Markdown")

# The infrastructure this session adds must itself be clean.
OWN = [HERE / "oral_bytes.py", HERE / "oral_mutation.py", HERE / "oral_manifest.py",
       HERE / "test_oral_release_infra.py", HERE / "SKILL.md",
       REPO / "meoclass1" / "qb_health_check.py"]
own_hits = B.scan_paths(OWN)
check("this session's own artefacts are control-byte clean", own_hits == [],
      "; ".join(h.describe() for h in own_hits) or "%d file(s) scanned" % len(OWN))


# ===========================================================================
# 4. UTF-8 AND LINE-ENDING CONTRACT
# ===========================================================================
print("\n--- 4. encoding and EOL contract ---")

with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / "u.txt"
    B.write_text(p, "MARPOL Annex VI — regulation 21\n")
    check("write_text/read_text round-trip non-ASCII",
          B.read_text(p) == "MARPOL Annex VI — regulation 21\n", "em dash survived")
    check("write_text does not translate LF to CRLF",
          b"\r\n" not in p.read_bytes(), "LF preserved on Windows")

check("normalise_eol collapses CRLF and lone CR",
      B.normalise_eol("a\r\nb\rc\n") == "a\nb\nc\n", "documented text contract")
check("normalise_eol is idempotent",
      B.normalise_eol(B.normalise_eol("a\r\nb")) == "a\nb", "safe to apply twice")


# ===========================================================================
# 5. MANIFEST SCHEMA CONTRACT
#
# The defect this guards: E6's mutation L pointed authorisation_batch_key at
# batches.E5 and the validator stayed green, because it hardcoded "E6" and
# never read the key. The audit showed the same field is unread by the A, E1,
# E2, E3, E4 and E5 validators too.
# ===========================================================================
print("\n--- 5. manifest schema contract ---")

findings = M.audit_all(HERE)
failed = [f for f in findings if not f.ok]
check("every batch manifest satisfies the shared schema contract", not failed,
      "; ".join(f.describe() for f in failed) or
      "%d checks over %d manifest(s)" % (len(findings),
                                         len(list(HERE.glob("batch_*manifest.json")))))

# EVERY batch manifest, named. Enumerated rather than counted for the same
# reason POST_E6_GATES is: this control used to read `len(manifests) == 11`,
# and F1 -- the first follow-up production batch -- turned it red simply by
# existing. A hardcoded total is a guard that expires the next time the thing
# it counts is added to, which is a confirmed defect class in this corpus.
# Adding a batch now means editing one reviewable line here.
EXPECTED_BATCH_MANIFESTS = [
    "batch_a_manifest.json",
    "batch_b_manifest.json",
    "batch_c_manifest.json",
    "batch_d_manifest.json",
    "batch_e1_enrichment_manifest.json",
    "batch_e2_enrichment_manifest.json",
    "batch_e3_enrichment_manifest.json",
    "batch_e4_enrichment_manifest.json",
    "batch_e5_enrichment_manifest.json",
    "batch_e6_enrichment_manifest.json",
    "batch_e_gap0609_manifest.json",
    "batch_f1_manifest.json",
    "batch_f1b_manifest.json",
    # The August 2026 fresh-intake batches. G1 and G2 were never registered
    # here, so this control has been red since G1 shipped -- the same
    # guard-expiry shape the E/F-series validators hit: a hardcoded list
    # that silently expires the next time the thing it counts grows.
    "batch_g1_manifest.json",
    "batch_g2_manifest.json",
    "batch_g3_manifest.json",
    "batch_g4_manifest.json",
    # The H-series. Registered by H5 closing H4-RES-01: all seven shipped with
    # digest pins that no validator, mutator or gate read, and G4 shipped
    # unregistered here for the same reason G1/G2 did. They are gated by
    # validate_batch_h_series.py / mutate_batch_h_series.py, which read THIS
    # list as their expectation -- so a future H manifest that is not added
    # here is not silently ungated: it fails h_manifests_none_undeclared.
    "batch_h1_manifest.json",
    "batch_h2_manifest.json",
    "batch_h3a_manifest.json",
    "batch_h3a_orb_manifest.json",
    "batch_h3b1_manifest.json",
    "batch_h3b2_manifest.json",
    "batch_h4_manifest.json",
    # H6 (2026-09-02): the two genuine new roots from the 31-August LPG
    # carrier report. There is no H5 manifest -- H5 was a closure phase
    # whose product edits were CE Oral Tips shipped as a correction, not a
    # card batch -- so the series numbering skips it by design rather than
    # by omission.
    "batch_h6_manifest.json",
]
manifests = sorted(HERE.glob("batch_*manifest.json"))
check("every batch manifest on disk is audited, and no other",
      sorted(p.name for p in manifests) == sorted(EXPECTED_BATCH_MANIFESTS),
      "on_disk=%d expected=%d unexpected=%s missing=%s"
      % (len(manifests), len(EXPECTED_BATCH_MANIFESTS),
         sorted(set(p.name for p in manifests) - set(EXPECTED_BATCH_MANIFESTS))
         or "none",
         sorted(set(EXPECTED_BATCH_MANIFESTS) - set(p.name for p in manifests))
         or "none"))

unclassified = set()
for path in manifests:
    for field in json.loads(B.read_text(path)):
        if M.classify(field) == M.UNCLASSIFIED:
            unclassified.add(field)
check("no manifest field is unclassified", not unclassified,
      "unclassified=%s" % (sorted(unclassified) or "none"))

check("authorisation fields are classified LOAD_BEARING",
      all(M.classify(f) == M.LOAD_BEARING for f in
          ("batch_id", "authorisation_batch_key", "authorisation_source",
           "authorisation_commit", "baseline_commit", "shared_target")),
      "identity/provenance fields are asserted, not decorative")

# NON-VACUITY. Each probe corrupts one thing in memory and requires the audit
# to name it. A guard that cannot fail is not a guard.
with tempfile.TemporaryDirectory() as tmp:
    src = json.loads(B.read_text(HERE / "batch_e6_enrichment_manifest.json"))

    def probe(name, mutate):
        d = json.loads(json.dumps(src))
        mutate(d)
        p = Path(tmp) / ("probe_%s_manifest.json" % name)
        B.write_text(p, json.dumps(d))
        return [f.check for f in M.audit_manifest(p) if not f.ok]

    bad = probe("key", lambda d: d.__setitem__("authorisation_batch_key", "batches.E5"))
    check("E6's escape is now caught: batch key pointed at another batch",
          "authorisation_batch_key_matches_batch_id" in bad, str(bad))

    bad = probe("decor", lambda d: d.__setitem__("authorisation_override", "yes"))
    check("a new authorisation-looking field cannot slip in unclassified",
          "all_fields_classified" in bad, str(bad))

    bad = probe("src", lambda d: d.__setitem__("authorisation_source", "no/such/record.json"))
    check("a dangling provenance pointer is caught",
          "authorisation_source_resolves" in bad, str(bad))

    bad = probe("dupe", lambda d: d["cards"].append(dict(d["cards"][0])))
    check("a duplicated action id is caught",
          "action_ids_unique_and_present" in bad, str(bad))

    # The shared-target probes run against E5, because E5 is the batch that
    # actually has one: ENRICH-A036 and ENRICH-A037 both target QB4_C.html#q6.
    # E6 has no shared target at all, so probing it would have proved nothing
    # while looking like a passing test.
    e5_src = json.loads(B.read_text(HERE / "batch_e5_enrichment_manifest.json"))

    def e5_probe(name, mutate):
        d = json.loads(json.dumps(e5_src))
        mutate(d)
        p = Path(tmp) / ("probe_e5_%s_manifest.json" % name)
        B.write_text(p, json.dumps(d))
        return [f.check for f in M.audit_manifest(p) if not f.ok]

    check("E5 is the shared-target fixture",
          e5_src.get("shared_target") == "QB4_C.html#q6",
          "shared_target=%s" % e5_src.get("shared_target"))

    def undeclare(d):
        d.pop("shared_target", None)
        d.pop("shared_target_actions", None)
        for c in d["cards"]:
            c.pop("shared_target_note", None)
    bad = e5_probe("shared", undeclare)
    check("an undeclared shared target is caught",
          "shared_target_declared_iff_present" in bad, str(bad))

    def disagree(d):
        for c in d["cards"]:
            if (c.get("file"), c.get("anchor")) == ("QB4_C.html", "q6"):
                c["post_edit_digest"] = c["action_id"]
    bad = e5_probe("digest", disagree)
    check("shared-target digest disagreement is caught",
          "shared_target_digests_agree" in bad, str(bad))

# E1 declares its shared target per-card; E5/E6 declare it at top level. Both
# spellings must be accepted, or the audit would report a false failure on
# historical release evidence and teach everyone to ignore it.
e1 = [f for f in M.audit_manifest(HERE / "batch_e1_enrichment_manifest.json") if not f.ok]
check("E1's per-card shared-target dialect is accepted", not e1,
      "; ".join(f.check for f in e1) or "clean")


# ===========================================================================
# 6. HEALTH-CHECK SOURCE IS REAL
#
# The defect this guards: qb_health_check hardcoded remote `main` and never
# read local disk, so every pre-merge "branch health == origin/main health"
# comparison was structurally incapable of seeing the change under test.
#
# This test proves the checker CONSUMES its requested source. It builds a
# scratch git repo, commits a clean tree, then corrupts a card WITHOUT
# committing. Local mode must see the corruption; ref mode must not.
# No network, and the real repository is never touched.
# ===========================================================================
print("\n--- 6. health-check source selection ---")

import qb_health_check as H  # noqa: E402

check("health check exposes a source selector", hasattr(H, "load_source"),
      "load_source present")
check("health check parses arguments", hasattr(H, "parse_args"), "parse_args present")
check("default source is remote main (CI contract unchanged)",
      H.parse_args([]).source == "remote", "default=%s" % H.parse_args([]).source)
check("local mode is selectable", H.parse_args(["--source", "local"]).source == "local")
check("ref mode carries its ref",
      H.parse_args(["--source", "ref", "--ref", "origin/main"]).ref == "origin/main")
check("ref mode without a ref is rejected",
      raises(lambda: H.load_source("ref", None), ValueError))
check("an unknown source is rejected, never silently substituted",
      raises(lambda: H.load_source("prod", None), ValueError))

# ---------------------------------------------------------------------------
# The runner's health comparison must strip PROVENANCE and keep FINDINGS.
#
# The runner deliberately runs the two sides with different `--source` flags, so
# every line describing where the report came from differs by construction. One
# of them -- `Loading source: ...` -- was not in the noise filter, leaked into
# the finding multiset, and produced a permanent NEW=1 / GONE=1. A gate that is
# always red detects nothing.
#
# Both directions are asserted: provenance must vanish, and a REAL difference
# must still survive, so this can never be "fixed" by filtering everything.
# ---------------------------------------------------------------------------
import run_oral_release as R  # noqa: E402

_LOCAL_REPORT = (
    "MIW QB + Notes Health Check\n"
    "Loading source: local ...\n"
    "source_type : local\n"
    "source      : F:\\Marine-Intelligence-Weekly (working tree, DIRTY)\n"
    "commit      : 67842df\n"
    "files       : 951\n"
    "findings    : 152\n"
    "QB1_A.html: some genuine finding\n")
_REF_REPORT = (
    "MIW QB + Notes Health Check\n"
    "Loading source: ref (origin/main) ...\n"
    "source_type : ref\n"
    "source      : origin/main\n"
    "commit      : 67842df\n"
    "files       : 837\n"
    "findings    : 152\n"
    "QB1_A.html: some genuine finding\n")

_cand = R.health_findings(_LOCAL_REPORT)
_base = R.health_findings(_REF_REPORT)
check("provenance lines never count as health findings",
      not (_cand - _base) and not (_base - _cand),
      "new=%s gone=%s" % (sorted(_cand - _base), sorted(_base - _cand)))
check("the source banner specifically is stripped",
      not any("Loading source" in line for line in _cand),
      "kept=%s" % sorted(_cand))

_changed = R.health_findings(
    _LOCAL_REPORT.replace("some genuine finding", "a DIFFERENT finding"))
check("a real finding difference is still detected (filter is not vacuous)",
      bool(_changed - _base), "new=%s" % sorted(_changed - _base))

# ---------------------------------------------------------------------------
# A LINE THAT IS A FUNCTION OF THE FINDINGS IS NOT ITSELF A FINDING.
#
# `Files with errors: N` and `Clean <kind> files: <list>` restate the finding
# set the report is already printing. Compared verbatim they blocked the gate
# on every IMPROVEMENT: fixing QB1_D#q7 moved the count 80 -> 79 and moved
# QB1_D into the clean list, and both showed up as NEW. Proved pre-existing --
# the identical pair was NEW at d0a188f, before any of that day's edits.
#
# They are not dropped. Each becomes the invariant it should satisfy, so the
# gate now catches two things the raw numbers never could: a report whose
# declared count disagrees with the file blocks it emitted, and a file listed
# as clean AND erroring at once.
#
# `Files scanned: N` is deliberately left alone -- it is corpus inventory, not
# a function of the findings, and it is the only line that would turn a
# collapsed scan into a NEW line instead of a silent mass GONE.
#
# Both directions are asserted below, and the classifier under test is the SAME
# function run_health calls.
# ---------------------------------------------------------------------------


def _health_report(declared, blocks, clean_qb):
    """A report in the real emitter's grammar (qb_health_check.build_report)."""
    L = ["MIW QB + Notes Health Check - x", "=" * 50, "--- QB SERIES ---",
         "Files scanned: 180",
         "Questions found on disk: 761  |  Manifest total: 761",
         "Files with errors: %d" % declared, ""]
    if blocks:
        L += ["QB FILE-LEVEL ISSUES", "-" * 30]
        for f, errs in blocks:
            L += ["", "\u25b6 %s  (12 questions)" % f]
            L += ["    \u2717 %s" % e for e in errs]
    L += ["", "-" * 50, "Clean QB files: " + ", ".join(clean_qb)]
    return "\n".join(L) + "\n"


def _health_new(cand, base):
    """(blocking, review) exactly as the runner classifies them."""
    new = R.health_findings(cand) - R.health_findings(base)
    blocking, reviews, _attr = R.classify_health_new(new)
    return blocking, reviews, new


_H_BASE = _health_report(
    2, [("QB1_A.html", ["q3: missing reg-box"]),
        ("QB1_D.html", ["q7: missing ce-tip"])],
    ["QB2_A.html", "QB3_A.html"])

# A. a pure improvement (QB1_D fixed) must not block
_H_BETTER = _health_report(
    1, [("QB1_A.html", ["q3: missing reg-box"])],
    ["QB1_D.html", "QB2_A.html", "QB3_A.html"])
_blk, _rev, _new = _health_new(_H_BETTER, _H_BASE)
check("a health IMPROVEMENT is not a blocking regression", not _blk,
      "blocking=%s" % sorted(_blk))
check("the improvement is still reported as GONE",
      bool(R.health_findings(_H_BASE) - R.health_findings(_H_BETTER)),
      "gone present")

# B. genuine regressions must still block -- four shapes
_H_NEWFILE = _health_report(
    3, [("QB1_A.html", ["q3: missing reg-box"]),
        ("QB1_D.html", ["q7: missing ce-tip"]),
        ("QB2_A.html", ["q11: malformed q-card"])], ["QB3_A.html"])
_blk, _rev, _new = _health_new(_H_NEWFILE, _H_BASE)
check("a finding on a newly-erroring file BLOCKS", bool(_blk),
      "blocking=%s" % sorted(x[:44] for x in _blk))

_H_EXTRA = _health_report(
    2, [("QB1_A.html", ["q3: missing reg-box", "q9: stale regulatory text"]),
        ("QB1_D.html", ["q7: missing ce-tip"])],
    ["QB2_A.html", "QB3_A.html"])
_blk, _rev, _new = _health_new(_H_EXTRA, _H_BASE)
check("an extra finding on an already-erroring file BLOCKS", bool(_blk),
      "blocking=%s" % sorted(x[:44] for x in _blk))

# STALE-LAW DETECTION IS NOT WEAKENED: the error-class trap still blocks.
_H_TRAP = _health_report(
    3, [("QB1_A.html", ["q3: missing reg-box"]),
        ("QB1_D.html", ["q7: missing ce-tip"]),
        ("QB9_H.html", ['KNOWN TRAP resurfaced: "Merchant Shipping Act, 1958"'
                        ' found in visible text'])],
    ["QB2_A.html", "QB3_A.html"])
_blk, _rev, _new = _health_new(_H_TRAP, _H_BASE)
check("an error-class KNOWN TRAP (stale law) still BLOCKS", bool(_blk),
      "blocking=%s" % sorted(x[:56] for x in _blk))
check("...and is never reclassified as a review note", not _rev,
      "reviews=%s" % sorted(_rev))

# C. the emitting tool's own downgrade is honoured: [REVIEW] reports, not blocks
_H_REVIEW = _health_report(
    3, [("QB1_A.html", ["q3: missing reg-box"]),
        ("QB1_D.html", ["q7: missing ce-tip"]),
        ("QB9_H.html", ['[REVIEW] KNOWN TRAP phrase present but in negation/'
                        'correction context: "Merchant Shipping Act, 1958"'])],
    ["QB2_A.html", "QB3_A.html"])
_blk, _rev, _new = _health_new(_H_REVIEW, _H_BASE)
check("a [REVIEW] note does not block (check_known_traps downgrades it)",
      not _blk, "blocking=%s" % sorted(_blk))
check("...but a [REVIEW] note is still surfaced", bool(_rev),
      "reviews=%d" % sum(_rev.values()))

# D. the replacement invariants must themselves bite
_H_MISCOUNT = _health_report(
    0, [("QB1_A.html", ["q3: missing reg-box"]),
        ("QB1_D.html", ["q7: missing ce-tip"])],
    ["QB2_A.html", "QB3_A.html"])
_blk, _rev, _new = _health_new(_H_MISCOUNT, _H_BASE)
check("a declared error count that disagrees with the emitted blocks BLOCKS",
      any("EMITTED FILE BLOCKS" in k for k in _blk),
      "blocking=%s" % sorted(x[:56] for x in _blk))

_H_OVERLAP = _health_report(
    2, [("QB1_A.html", ["q3: missing reg-box"]),
        ("QB1_D.html", ["q7: missing ce-tip"])],
    ["QB1_D.html", "QB2_A.html", "QB3_A.html"])
_blk, _rev, _new = _health_new(_H_OVERLAP, _H_BASE)
check("a file reported as clean AND erroring BLOCKS",
      any("ALSO REPORTED AS ERRORING" in k for k in _blk),
      "blocking=%s" % sorted(x[:56] for x in _blk))

check("a healthy report satisfies both invariants",
      all(("==" in k or "disjoint" in k)
          for k in R.health_findings(_H_BASE)
          if k.startswith(("Files with errors:", "Clean "))),
      "%s" % [k for k in R.health_findings(_H_BASE)
              if k.startswith(("Files with errors:", "Clean "))])

# The notes series counts its blocks in `topic-blocks`, not `questions`, and
# was missed when the per-file header normalisation was first written.
check("a notes file header is normalised like a QB one",
      "\u25b6 miw-notes-mgmt-p1.html" in R.health_findings(
          "\u25b6 miw-notes-mgmt-p1.html  (7 topic-blocks)\n"),
      "kept=%s" % sorted(R.health_findings(
          "\u25b6 miw-notes-mgmt-p1.html  (7 topic-blocks)\n")))

CLEAN = "<div class=\"q-card\" id=\"q1\"><p>clean</p></div>\n"
DIRTY = "<div class=\"q-card\" id=\"q1\"><p>CORRUPTED-BY-TEST</p></div>\n"

with tempfile.TemporaryDirectory() as tmp:
    scratch = Path(tmp) / "repo"
    (scratch / "meoclass1").mkdir(parents=True)
    (scratch / "SQ").mkdir(parents=True)
    B.write_text(scratch / "meoclass1" / "QB_TEST.html", CLEAN)
    B.write_text(scratch / "SQ" / "sample.html", CLEAN)

    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")

    def git(*args):
        return subprocess.run(["git"] + list(args), cwd=str(scratch),
                              capture_output=True, check=True, env=env)

    git("init", "-q")
    git("add", "-A")
    git("commit", "-qm", "clean tree")

    original_root = H._repo_root
    H._repo_root = lambda: str(scratch)
    try:
        # Corrupt the card on disk only -- nothing is committed.
        B.write_text(scratch / "meoclass1" / "QB_TEST.html", DIRTY)

        local_files, local_info = H.load_source("local")
        ref_files, ref_info = H.load_source("ref", "HEAD")

        local_card = local_files["QB_TEST.html"].decode("utf-8")
        ref_card = ref_files["QB_TEST.html"].decode("utf-8")

        check("LOCAL mode sees the uncommitted corruption",
              "CORRUPTED-BY-TEST" in local_card, "local read the working tree")
        check("REF mode does NOT see the uncommitted corruption",
              "CORRUPTED-BY-TEST" not in ref_card, "ref read the committed tree")
        check("the two sources genuinely differ", local_card != ref_card,
              "a local regression is now visible")

        check("local mode reports source_type=local", local_info.source_type == "local")
        check("ref mode reports source_type=ref", ref_info.source_type == "ref")
        check("local mode reports a commit SHA", bool(local_info.commit),
              str(local_info.commit)[:12])
        check("local mode reports the tree is DIRTY", "DIRTY" in local_info.location,
              "uncommitted state is disclosed")
        check("source banner names type, source, commit and file count",
              all(k in local_info.describe()
                  for k in ("source_type", "source", "commit", "files")),
              "reportable")

        # SQ/ keeps its prefix; meoclass1/ loses it. Both loaders must agree.
        check("local and ref agree on the path convention",
              set(local_files) == set(ref_files) == {"QB_TEST.html", "SQ/sample.html"},
              str(sorted(local_files)))
    finally:
        H._repo_root = original_root

check("the real repository was not modified by the source test",
      H._repo_root() == str(REPO), H._repo_root())


# ===========================================================================
# 6. POST-RELEASE CORRECTION RECORDS
#
# The defect this guards: on 21 August 2026 a candidate-feedback correction was
# committed with no authorisation record. Seven of eleven batch validators went
# red, correctly, because no record existed that COULD own a post-release edit.
#
# Declaring that correction turns those guards green again -- which is either an
# authorisation or a very effective way of switching seven guards off. These
# controls pin the difference.
# ===========================================================================
print("\n--- 6. post-release correction records ---")

CORRECTIONS = sorted(HERE.glob(M.CORRECTION_MANIFEST_GLOB))
check("at least one correction record exists", bool(CORRECTIONS),
      "%d found" % len(CORRECTIONS))

corr_findings = [f for c in CORRECTIONS for f in M.audit_correction_manifest(c)]
corr_failed = [f for f in corr_findings if not f.ok]
check("every correction record satisfies the correction schema contract",
      not corr_failed,
      "; ".join(f.describe() for f in corr_failed)
      or "%d checks over %d record(s)" % (len(corr_findings), len(CORRECTIONS)))

# The delegation surface must be the UNION. A helper that quietly returns only
# batch manifests would make every correction unauthorised again.
surface = M.authorisation_manifest_paths(HERE)
names = {p.name for p in surface}
check("the delegation surface unions both record families",
      any(n.startswith("batch_") for n in names)
      and any(n.startswith("correction_") for n in names),
      "%d record(s): %d batch, %d correction"
      % (len(names),
         sum(1 for n in names if n.startswith("batch_")),
         sum(1 for n in names if n.startswith("correction_"))))

# AUTHORISATION REGISTER vs BATCH PRODUCTION MANIFEST -- two different records.
#
# The register says what future follow-up production is AUTHORISED to do. A
# batch manifest says what a production run actually IMPLEMENTED, and it is the
# batch manifest alone that delegates authority over a card to a later record.
#
# Collapsing them would be a real hole: the register names 35 parent cards it
# has never edited, so admitting it to the delegation surface would pre-emptively
# exempt all 35 from every historical guard -- authorising edits that no batch
# had made and no manifest had pinned.
REGISTER = HERE / "oral_followup_register.json"
check("the follow-up register exists", REGISTER.exists(), REGISTER.name)
check("the follow-up register is NOT part of the delegation surface",
      REGISTER not in surface and REGISTER.name not in names,
      "an authorisation register delegates nothing")
_reg = json.loads(B.read_text(REGISTER)) if REGISTER.exists() else {}
check("the follow-up register declares itself an authorisation record",
      _reg.get("record_class") == "AUTHORISATION_REGISTER",
      str(_reg.get("record_class")))
check("the follow-up register authorises no card edit of its own",
      _reg.get("provenance", {}).get("content_authored_here") is False
      and all(a.get("creates_new_card") is False
              for a in _reg.get("actions", [])),
      "%d actions, none create a card" % len(_reg.get("actions", [])))
check("every register action still names a batch only when it has one",
      all(a.get("batch") is None or isinstance(a.get("batch"), str)
          for a in _reg.get("actions", [])),
      "batch assignment is a production-time field")

check("authorisation_manifest_paths honours exclude",
      CORRECTIONS[0] not in M.authorisation_manifest_paths(HERE, exclude=CORRECTIONS[0])
      if CORRECTIONS else False,
      "a manifest never delegates to itself")

# Every batch validator must read the shared surface. A local glob left behind
# in even one validator is a correction that authorises nine guards out of ten.
stale = []
for path in sorted(HERE.glob("validate_batch_*.py")):
    body = B.read_text(path)
    if 'glob("batch_*_manifest.json")' in body:
        stale.append(path.name)
    elif "authorisation_elsewhere" in body or "authorised_elsewhere" in body:
        if "authorisation_manifest_paths" not in body:
            stale.append(path.name + " (delegates without the shared helper)")
check("no batch validator keeps a private manifest glob", not stale,
      "stale=%s" % (stale or "none"))

check("correction identity fields are LOAD_BEARING",
      all(M.classify_correction(f) == M.LOAD_BEARING for f in
          ("correction_id", "kind", "status", "origin", "governing_commits",
           "baseline_commit", "authorisation_source", "cards")),
      "identity/authorisation is asserted, not decorative")

check("artefacts are explicitly INFORMATIONAL",
      M.classify_correction("artefacts") == M.INFORMATIONAL,
      "recorded scope, deliberately unpinned -- a decision, not an accident")

# NON-VACUITY. Each probe corrupts one thing in memory and requires the
# correction audit to name it. A guard that cannot fail is not a guard.
if CORRECTIONS:
    with tempfile.TemporaryDirectory() as tmp:
        src = json.loads(B.read_text(CORRECTIONS[0]))
        stem = CORRECTIONS[0].name

        def cprobe(mutate, name=stem):
            d = json.loads(json.dumps(src))
            mutate(d)
            q = Path(tmp) / name
            B.write_text(q, json.dumps(d))
            return [f.check for f in M.audit_correction_manifest(q) if not f.ok]

        bad = cprobe(lambda d: d.__setitem__("correction_id", "CORR-OTHER-1"))
        check("a corrupted correction id is caught",
              "correction_id_matches_filename" in bad, str(bad))

        bad = cprobe(lambda d: d.__setitem__("kind", "BATCH"))
        check("a record claiming to be a batch is caught",
              "kind_is_correction" in bad, str(bad))

        bad = cprobe(lambda d: d.__setitem__("governing_commits", ["deadbee"]))
        check("a dangling governing commit is caught",
              "governing_commits_resolve" in bad, str(bad))

        bad = cprobe(lambda d: d["cards"][0].__setitem__("post_edit_digest", "nope"))
        check("a malformed post-edit digest is caught",
              "card_digests_well_formed" in bad, str(bad))

        bad = cprobe(lambda d: d["cards"][0].__setitem__(
            "pre_edit_digest", d["cards"][0]["post_edit_digest"]))
        check("an inert card (pre == post) is caught",
              "card_digests_differ" in bad, str(bad))

        bad = cprobe(lambda d: d["cards"][0].__setitem__("classification", "MISC"))
        check("an unknown correction classification is caught",
              "card_classifications_known" in bad, str(bad))

        # This probe needs a record with MORE THAN ONE card. CORRECTIONS[0] sorts
        # to a single-card manifest whose only card is already
        # PRIMARY_CORRECTION, so setting every card to PRIMARY_CORRECTION there
        # mutates nothing and the control can never fire -- it read as a passing
        # guard for as long as the first correction on disk had one card. Pick a
        # multi-card record explicitly, and fail loudly if none exists rather
        # than quietly going vacuous again.
        _multi = next((c for c in CORRECTIONS
                       if len(json.loads(B.read_text(c)).get("cards") or []) > 1), None)
        check("a multi-card correction record exists to test merging against",
              _multi is not None,
              _multi.name if _multi else "no correction manifest has >1 card")
        if _multi is not None:
            _src = json.loads(B.read_text(_multi))
            _d = json.loads(json.dumps(_src))
            for _c in _d["cards"]:
                _c["classification"] = "PRIMARY_CORRECTION"
            _q = Path(tmp) / _multi.name
            B.write_text(_q, json.dumps(_d))
            bad = [f.check for f in M.audit_correction_manifest(_q) if not f.ok]
            check("two events merged into one record are caught",
                  "exactly_one_primary_correction" in bad, str(bad))

        bad = cprobe(lambda d: d["cards"][0].__setitem__("path", "elsewhere/Other.html"))
        check("a card whose path and file disagree is caught",
              "card_path_matches_file" in bad, str(bad))

        bad = cprobe(lambda d: d.__setitem__("nonsense_authorisation", "yes"))
        check("a new undeclared field cannot slip in",
              "all_fields_classified" in bad, str(bad))


# ===========================================================================
# 12. STDOUT IS UTF-8, IN EVERY TOOL
# ===========================================================================
# Lesson 2 in oral_bytes governed FILE I/O and stopped there, leaving the
# loudest channel unguarded. On Windows a child's piped stdout uses the locale
# codec, so printing U+26A0 raises UnicodeEncodeError -- and this toolchain both
# reports that character and deliberately injects it (mutate_batch_a mutation
# F). The harness died between mutating a product page and restoring it, and
# left the mutation on disk.

check("oral_bytes exposes an idempotent UTF-8 stdio contract",
      callable(getattr(B, "enable_utf8_stdio", None))
      and B.enable_utf8_stdio() is False,
      "already applied on import, so a second call changes nothing")

check("stdout really is UTF-8 in this process",
      (sys.stdout.encoding or "").lower().replace("-", "") == "utf8",
      "encoding=%s" % sys.stdout.encoding)

check("an unencodable character degrades to text, never to an exception",
      "backslashreplace" in B.read_text(HERE / "oral_bytes.py"),
      "strict would trade one crash class for another")

# Non-vacuity: EVERY tool must reach the contract, whether by importing a
# shared module or by importing it explicitly. A tool that reaches neither is
# exactly mutate_batch_a before the fix.
SHARED = ("oral_bytes", "oral_manifest", "oral_mutation", "oral_supersession",
          "oral_lib", "oral_text", "oral_notes", "validate_batch_b",
          # The content-gate harness (2026-09-03). It imports oral_bytes, so a
          # suite built on it reaches the contract transitively -- but this list
          # is what makes that reachability CHECKABLE, so a new shared module
          # has to be named here or every suite using it reads as unreached.
          "oral_content_mutation")
unreached = []
for path in sorted(list(HERE.glob("validate_*.py")) + list(HERE.glob("mutate_*.py"))):
    src = B.read_text(path)
    if not any(name in src for name in SHARED):
        unreached.append(path.name)
# --- validator_failing must read every dialect on the gate list -----------
# H4-RES-11: validate_study_spine.py INDENTS its failures and suffixes the
# check name with a colon, so an anchored ^FAIL matched none of them. That
# gate therefore had no derivable baseline, could only be classified FAIL,
# and a default --full run stopped at gate 5 of 66 with sixty-one guards
# unrun. Pinned here as a fixture rather than harvested from live output: a
# self-test that reads the live corpus stops testing anything the moment the
# corpus changes.
_DIALECTS = [
    ("batch/unit      ", "FAIL  QB1_F.html#q22 q-card is a direct child of #q-feed",
     {"QB1_F.html#q22"}),
    ("study spine     ", "  FAIL R-ACCOUNT-ORAL: mapped 699 + unresolved 39 != 759",
     {"R-ACCOUNT-ORAL"}),
    ("indented tagged ", "   FAIL batch_h1/H1-001:manifest_digest_matches detail",
     {"batch_h1/H1-001:manifest_digest_matches"}),
    ("mutator evidence", "FAIL: this line is CAUGHT-evidence inside a mutator log",
     set()),
]
for _name, _line, _want in _DIALECTS:
    check("validator_failing reads the %s dialect" % _name.strip(),
          X.validator_failing(_line) == _want,
          "got %s wanted %s" % (sorted(X.validator_failing(_line)), sorted(_want)))
check("validator_failing still ignores a bare FAIL: evidence line",
      X.validator_failing("FAIL: caught") == set(),
      "a mutator's own FAIL: output is evidence, not a failure")

check("every validator and mutation harness reaches the UTF-8 contract",
      not unreached, "unreached=%s" % (unreached or "none"))


# ===========================================================================
print("\n%d checks, %d FAIL" % (CHECKS[0], len(FAILURES)))
for f in FAILURES:
    print("  FAIL %s" % f)
sys.exit(1 if FAILURES else 0)
