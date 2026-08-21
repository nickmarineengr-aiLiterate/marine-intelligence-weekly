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

manifests = sorted(HERE.glob("batch_*manifest.json"))
check("all eleven batch manifests are audited", len(manifests) == 11,
      "%d found" % len(manifests))

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

        bad = cprobe(lambda d: [c.__setitem__("classification", "PRIMARY_CORRECTION")
                                for c in d["cards"]])
        check("two events merged into one record are caught",
              "exactly_one_primary_correction" in bad, str(bad))

        bad = cprobe(lambda d: d["cards"][0].__setitem__("path", "elsewhere/Other.html"))
        check("a card whose path and file disagree is caught",
              "card_path_matches_file" in bad, str(bad))

        bad = cprobe(lambda d: d.__setitem__("nonsense_authorisation", "yes"))
        check("a new undeclared field cannot slip in",
              "all_fields_classified" in bad, str(bad))


# ===========================================================================
print("\n%d checks, %d FAIL" % (CHECKS[0], len(FAILURES)))
for f in FAILURES:
    print("  FAIL %s" % f)
sys.exit(1 if FAILURES else 0)
