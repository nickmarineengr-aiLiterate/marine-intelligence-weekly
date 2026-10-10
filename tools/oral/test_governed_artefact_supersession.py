#!/usr/bin/env python3
"""
Controls for governed whole-file artefact succession.

THREE LAYERS
------------

Sections 1-4 exercise the resolver in memory, over synthetic records and a
test double for repository history. That is where the whole negative matrix
lives, because building a bad chain or a lying history costs nothing.

Section 5 proves DORMANCY on the real corpus: for every governed artefact on
disk, the resolver's verdict is exactly the bare ``pin == live`` comparison
``audit_governed_artefacts_live`` made before successions existed, and no
record that declares no succession gains or loses a single schema check.

The live wiring -- real git, real records, the real gate functions -- is
proved by ``mutate_governed_artefact_supersession.py``, which builds a
throwaway fixture repository and also runs against any succession actually
on disk. A resolver that is correct and unreachable passes every test here.

NOTHING HERE IS RELEASE EVIDENCE FOR ANY CORRECTION RECORD.
"""

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import oral_manifest as M                                         # noqa: E402
from oral_supersession import (                                   # noqa: E402
    ArtefactRecord, build_artefact_chain, resolve_authorised_artefact_state,
    load_artefact_records,
    LIVE_TERMINAL, SUPERSEDED_OK, PIN_MISMATCH, CHAIN_BREAK, CHAIN_FORK,
    CHAIN_CYCLE, AMBIGUOUS_ROOT, TERMINAL_NOT_LIVE, DIGEST_CONVENTION_MISMATCH,
    MALFORMED_CLAIM, NOT_IN_CHAIN, MISSING_ANCESTOR, PATH_MISMATCH,
    TYPE_MISMATCH, UNKNOWN_FIELD, UNAUTHORISED_LINK, HISTORY_UNVERIFIED,
    HISTORY_MISMATCH, PROPOSITION_NOT_PRESERVED, _MISSING)

FAILURES = []
COUNT = [0]


def check(name, ok, detail=""):
    COUNT[0] += 1
    print("%-4s %-5s %-66s %s" % ("ok" if ok else "FAIL", "%d." % COUNT[0],
                                  name, str(detail)[:160]))
    if not ok:
        FAILURES.append(name)


d = M.artefact_digest
PATH = "meoclass1/QBX_CheatSheet.html"
OTHER = "meoclass1/QBY_CheatSheet.html"
ROOT_LINE = "<li>Casualty: cause not settled (flag State found no physical evidence)</li>"
A_LINE = "<li>Fire main: 2/4 breadth rule for five or more tiers</li>"
T0 = "<ul>\n<li>Casualty: settled cause</li>\n</ul>\n"
T1 = "<ul>\n%s\n</ul>\n" % ROOT_LINE
T2 = "<ul>\n%s\n%s\n</ul>\n" % (ROOT_LINE, A_LINE)
T3 = "<ul>\n%s\n%s\n<li>B edit</li>\n</ul>\n" % (ROOT_LINE, A_LINE)
T9 = "<ul>\n%s\n%s\n<li>unregistered</li>\n</ul>\n" % (ROOT_LINE, A_LINE)

RM, AM, BM = "correction_root.json", "correction_a.json", "correction_b.json"


class FakeHistory:
    """`text_at` / `is_ancestor` over an explicit commit graph."""

    def __init__(self, files, parents):
        self.files, self.parents = files, parents

    def text_at(self, commit, path):
        return self.files.get((commit, path))

    def is_ancestor(self, older, newer):
        seen = newer
        while seen is not None:
            if seen == older:
                return True
            seen = self.parents.get(seen)
        return False


def history(overrides=None):
    files = {("c0", PATH): T0, ("c1", PATH): T1, ("c2", PATH): T2,
             ("c3", PATH): T3}
    files.update(overrides or {})
    return FakeHistory(files, {"c1": "c0", "c2": "c1", "c3": "c2"})


HIST = history()


def root(**kw):
    base = dict(manifest=RM, action_id="R-01", path=PATH,
                artefact_type="CHEAT_SHEET", pre_edit_digest=d(T0),
                post_edit_digest=d(T1), is_succession=False, supersedes=None,
                preserved=(ROOT_LINE,), unknown_fields=(),
                record_status="AUTHORISED", baseline_commit="c0",
                governing_commit="c1")
    base.update(kw)
    return ArtefactRecord(**base)


def succ(manifest, aid, pre, post, claim, preserved, base, gov, **kw):
    rec = dict(manifest=manifest, action_id=aid, path=PATH,
               artefact_type="CHEAT_SHEET", pre_edit_digest=pre,
               post_edit_digest=post, is_succession=True, supersedes=claim,
               preserved=tuple(preserved), unknown_fields=(),
               record_status="AUTHORISED", baseline_commit=base,
               governing_commit=gov)
    rec.update(kw)
    return ArtefactRecord(**rec)


def claim(manifest, aid, post, **extra):
    c = {"manifest": manifest, "action_id": aid, "post_edit_digest": post}
    c.update(extra)
    return c


def _link(defaults, kw):
    merged = dict(defaults)
    merged.update(kw)
    return succ(**merged)


def A(**kw):
    return _link(dict(manifest=AM, aid="A-01", pre=d(T1), post=d(T2),
                      claim=claim(RM, "R-01", d(T1)), preserved=[ROOT_LINE],
                      base="c1", gov="c2"), _rename(kw))


def B(**kw):
    return _link(dict(manifest=BM, aid="B-01", pre=d(T2), post=d(T3),
                      claim=claim(AM, "A-01", d(T2)),
                      preserved=[ROOT_LINE, A_LINE], base="c2", gov="c3"),
                 _rename(kw))


def _rename(kw):
    """Accept ArtefactRecord field names as overrides on A() / B()."""
    alias = {"pre_edit_digest": "pre", "post_edit_digest": "post",
             "supersedes": "claim", "baseline_commit": "base",
             "governing_commit": "gov"}
    return {alias.get(k, k): v for k, v in kw.items()}


def res(records, manifest, aid, pin, live, hist=HIST, text=None, path=PATH):
    return resolve_authorised_artefact_state(
        manifest=manifest, action_id=aid, path=path, pinned_post_digest=pin,
        live_digest=live, records=records, history=hist, live_text=text)


def expect(name, r, status, ok=False):
    check(name, r.ok == ok and r.status == status, r.describe())


print("=" * 110)
print("1. DORMANT BY DEFAULT -- a path no succession names behaves exactly as before")
print("=" * 110)

r = res([root()], RM, "R-01", d(T1), d(T1), hist=None)
expect("no succession + pin == live -> accepted, needs no history", r,
       LIVE_TERMINAL, ok=True)
r = res([root()], RM, "R-01", d(T1), d(T2), hist=None)
expect("GS-1a no succession declared + live edit -> PIN_MISMATCH (the dormant default)",
       r, PIN_MISMATCH)
chain, problem = build_artefact_chain(PATH, records=[root()])
check("an undeclared path builds no chain at all", chain is None and problem is None)
# Two records governing ONE path with no succession: each keeps its own
# independent `pin == live`, exactly as before. Chain rules (one root) engage
# only when a succession is declared.
two_roots = [root(), root(manifest="correction_other.json", action_id="O-01")]
check("two independent governing records, no succession -> both still dormant",
      build_artefact_chain(PATH, records=two_roots) == (None, None))


print()
print("=" * 110)
print("2. POSITIVE CONTROLS -- single link, two links, ancestor resolution, exact terminal")
print("=" * 110)

one = [root(), A()]
expect("single link: predecessor is an authorised ANCESTOR of live",
       res(one, RM, "R-01", d(T1), d(T2), text=T2), SUPERSEDED_OK, ok=True)
expect("single link: successor is the verified terminal and live",
       res(one, AM, "A-01", d(T2), d(T2), text=T2), LIVE_TERMINAL, ok=True)
two = [root(), A(), B()]
expect("two links: root resolves as historical ancestor",
       res(two, RM, "R-01", d(T1), d(T3), text=T3), SUPERSEDED_OK, ok=True)
expect("two links: middle link resolves as historical ancestor",
       res(two, AM, "A-01", d(T2), d(T3), text=T3), SUPERSEDED_OK, ok=True)
expect("two links: exact terminal live digest -> LIVE_TERMINAL",
       res(two, BM, "B-01", d(T3), d(T3), text=T3), LIVE_TERMINAL, ok=True)
chain, problem = build_artefact_chain(PATH, records=two)
check("two links order root -> A -> B",
      problem is None and [s.manifest for s in chain] == [RM, AM, BM],
      [s.describe() for s in chain or []])
# The successor's OWN digest pin is still enforced at the terminal.
expect("terminal record whose pin is not the chain's own -> rejected",
       res(two, BM, "B-01", d(T2), d(T3), text=T3), "PREDECESSOR_PIN_ALTERED")
# Resolution order is not a function of record order on disk.
expect("records in reverse order resolve identically",
       res(list(reversed(two)), RM, "R-01", d(T1), d(T3), text=T3),
       SUPERSEDED_OK, ok=True)


print()
print("=" * 110)
print("3. NEGATIVE MATRIX -- GS-1 .. GS-12 at the resolver")
print("=" * 110)

expect("GS-1b succession with no supersedes -> MALFORMED_CLAIM",
       res([root(), A(supersedes=_MISSING)], RM, "R-01", d(T1), d(T2)), MALFORMED_CLAIM)
expect("GS-2 claim's pinned digest != predecessor pin -> MISSING_ANCESTOR",
       res([root(), A(supersedes=claim(RM, "R-01", "e" * 64))], RM, "R-01", d(T1), d(T2)),
       MISSING_ANCESTOR)
expect("GS-2b claim names an action that does not exist -> MISSING_ANCESTOR",
       res([root(), A(supersedes=claim(RM, "R-99", d(T1)))], RM, "R-01", d(T1), d(T2)),
       MISSING_ANCESTOR)
expect("GS-2c claim names a manifest that does not exist -> MISSING_ANCESTOR",
       res([root(), A(supersedes=claim("correction_gone.json", "R-01", d(T1)))],
           RM, "R-01", d(T1), d(T2)), MISSING_ANCESTOR)
expect("GS-3 predecessor pin rebaselined -> MISSING_ANCESTOR (chain broken)",
       res([root(post_edit_digest=d(T2)), A()], RM, "R-01", d(T2), d(T2)),
       MISSING_ANCESTOR)
expect("GS-4 successor pre != predecessor post -> CHAIN_BREAK",
       res([root(), A(pre_edit_digest=d(T0))], RM, "R-01", d(T1), d(T2)), CHAIN_BREAK)
expect("GS-5a successor names another file -> PATH_MISMATCH (predecessor side)",
       res([root(), A(path=OTHER)], RM, "R-01", d(T1), d(T2)), PATH_MISMATCH)
expect("GS-5a successor names another file -> PATH_MISMATCH (successor side)",
       res([root(), A(path=OTHER)], AM, "A-01", d(T2), d(T2), path=OTHER),
       PATH_MISMATCH)
expect("GS-5b successor declares another artefact type -> TYPE_MISMATCH",
       res([root(), A(artefact_type="NOTES_PAGE")], RM, "R-01", d(T1), d(T2)),
       TYPE_MISMATCH)
fork = succ("correction_f.json", "F-01", d(T1), d(T3), claim(RM, "R-01", d(T1)),
            [ROOT_LINE], "c1", "c3")
expect("GS-6 two successors, different posts, one predecessor -> CHAIN_FORK",
       res([root(), A(), fork], RM, "R-01", d(T1), d(T2)), CHAIN_FORK)
dup = succ("correction_f.json", "F-01", d(T1), d(T2), claim(RM, "R-01", d(T1)),
           [ROOT_LINE], "c1", "c2")
expect("GS-6b duplicate successor in another record, SAME post -> CHAIN_FORK",
       res([root(), A(), dup], RM, "R-01", d(T1), d(T2)), CHAIN_FORK)
same_rec = succ(AM, "A-02", d(T1), d(T3), claim(RM, "R-01", d(T1)), [ROOT_LINE], "c1", "c2")
expect("GS-6c one record declaring two conflicting successions -> CHAIN_FORK",
       res([root(), A(), same_rec], RM, "R-01", d(T1), d(T2)), CHAIN_FORK)
cyc_a = A(pre_edit_digest=d(T3), supersedes=claim(BM, "B-01", d(T3)))
cyc_b = B(pre_edit_digest=d(T2))
expect("GS-7 A -> B -> A -> CHAIN_CYCLE",
       res([root(), cyc_a, cyc_b], RM, "R-01", d(T1), d(T2)), CHAIN_CYCLE)
expect("GS-7b a succession naming its own record -> CHAIN_CYCLE",
       res([root(), A(supersedes=claim(AM, "A-01", d(T2)))], RM, "R-01", d(T1), d(T2)),
       CHAIN_CYCLE)
T2_DROPPED = T2.replace(ROOT_LINE + "\n", "")
expect("GS-8a predecessor proposition deleted from live -> not the terminal",
       res(one, RM, "R-01", d(T1), d(T2_DROPPED), text=T2_DROPPED), TERMINAL_NOT_LIVE)
expect("GS-8b successor declaration drops the predecessor proposition",
       res([root(), A(preserved=("something else",))], RM, "R-01", d(T1), d(T2)),
       PROPOSITION_NOT_PRESERVED)
expect("GS-8c successor's governing commit deleted the proposition",
       res([root(), A(post_edit_digest=d(T2_DROPPED))], RM, "R-01", d(T1),
           d(T2_DROPPED), hist=history({("c2", PATH): T2_DROPPED})),
       PROPOSITION_NOT_PRESERVED)
expect("GS-8d two links: last link drops the ROOT proposition (transitive)",
       res([root(), A(), B(preserved=(A_LINE,))], RM, "R-01", d(T1), d(T3)),
       PROPOSITION_NOT_PRESERVED)
expect("GS-9 unregistered live edit after the terminal -> TERMINAL_NOT_LIVE",
       res(one, RM, "R-01", d(T1), d(T9), text=T9), TERMINAL_NOT_LIVE)
expect("GS-9b ... and the successor itself fails too",
       res(one, AM, "A-01", d(T2), d(T9), text=T9), TERMINAL_NOT_LIVE)
expect("GS-10a unknown key in the claim -> UNKNOWN_FIELD",
       res([root(), A(supersedes=claim(RM, "R-01", d(T1), override=True))],
           RM, "R-01", d(T1), d(T2)), UNKNOWN_FIELD)
expect("GS-10b unknown key on the succession entry -> UNKNOWN_FIELD",
       res([root(), A(unknown_fields=("grandfathered",))], RM, "R-01", d(T1), d(T2)),
       UNKNOWN_FIELD)
for status in ("SUPERSEDED", "DRAFT", None):
    expect("GS-11 successor record status=%s -> UNAUTHORISED_LINK" % status,
           res([root(), A(record_status=status)], RM, "R-01", d(T1), d(T2)),
           UNAUTHORISED_LINK)
expect("GS-11d predecessor record not AUTHORISED -> UNAUTHORISED_LINK",
       res([root(record_status="SUPERSEDED"), A()], AM, "A-01", d(T2), d(T2)),
       UNAUTHORISED_LINK)
expect("GS-12a 16-char card-style digests -> DIGEST_CONVENTION_MISMATCH",
       res([root(), A(pre_edit_digest=d(T1)[:16], post_edit_digest=d(T2)[:16])],
           RM, "R-01", d(T1), d(T2)), DIGEST_CONVENTION_MISMATCH)
crlf = __import__("hashlib").sha256(T2.replace("\n", "\r\n").encode()).hexdigest()
expect("GS-12b non-LF-normalised post digest -> HISTORY_MISMATCH",
       res([root(), A(post_edit_digest=crlf)], RM, "R-01", d(T1), crlf), HISTORY_MISMATCH)
expect("GS-12c terminal checked against a non-artefact live digest",
       res(one, RM, "R-01", d(T1), d(T2)[:16]), DIGEST_CONVENTION_MISMATCH)


print()
print("=" * 110)
print("4. HISTORY -- a JSON declaration alone never passes")
print("=" * 110)

expect("a sound chain with NO history supplied -> HISTORY_UNVERIFIED",
       res(one, RM, "R-01", d(T1), d(T2), hist=None), HISTORY_UNVERIFIED)
expect("successor baseline does not hold its declared pre-state",
       res([root(), A(baseline_commit="c0")], RM, "R-01", d(T1), d(T2)), HISTORY_MISMATCH)
expect("successor governing commit does not hold its declared post-state",
       res([root(), A(governing_commit="c1")], RM, "R-01", d(T1), d(T2)), HISTORY_MISMATCH)
expect("root governing commit does not hold the root pin",
       res([root(governing_commit="c0"), A()], RM, "R-01", d(T1), d(T2)), HISTORY_MISMATCH)
# Same bytes, unrelated history: an orphan branch reproducing both states.
orphan = FakeHistory({("c0", PATH): T0, ("c1", PATH): T1, ("o1", PATH): T1,
                      ("o2", PATH): T2},
                     {"c1": "c0", "o2": "o1"})
expect("successor baseline is not a descendant of the predecessor's commit",
       res([root(), A(baseline_commit="o1", governing_commit="o2")], RM, "R-01",
           d(T1), d(T2), hist=orphan), HISTORY_MISMATCH)
# c1 (T1) -> g (T2) -> b (T1 again). Every digest the record states is
# true somewhere, but its "baseline" comes AFTER its "governing" commit.
backwards = FakeHistory({("c0", PATH): T0, ("c1", PATH): T1, ("g", PATH): T2,
                         ("b", PATH): T1},
                        {"c1": "c0", "g": "c1", "b": "g"})
expect("successor governing commit does not descend from its baseline",
       res([root(), A(baseline_commit="b", governing_commit="g")], RM, "R-01",
           d(T1), d(T2), hist=backwards), HISTORY_MISMATCH)
check("an inert link (pre == post) cannot hide in the chain",
      not res([root(), A(post_edit_digest=d(T1))], RM, "R-01", d(T1), d(T1)).ok)
expect("a record not in the chain asking about the path -> NOT_IN_CHAIN",
       res(one, "correction_x.json", "X-01", d(T2), d(T2)), NOT_IN_CHAIN)
expect("a second, unrelated root alongside a declared chain -> AMBIGUOUS_ROOT",
       res(one + [root(manifest="correction_other.json", action_id="O-01",
                       pre_edit_digest=d(T3), post_edit_digest=d(T9))],
           RM, "R-01", d(T1), d(T2)), AMBIGUOUS_ROOT)


print()
print("=" * 110)
print("5. THE REAL CORPUS -- dormant, and unchanged, for every existing record")
print("=" * 110)

CORRECTIONS = sorted(HERE.glob(M.CORRECTION_MANIFEST_GLOB))
records = load_artefact_records(HERE)
declared = sorted({r.manifest for r in records if r.is_succession})
governed = [r for r in records if not r.is_succession]
check("governed artefacts exist on disk to test dormancy against", bool(governed),
      "%d governed artefact entr(y/ies)" % len(governed))

mismatched = []
for r in governed:
    live = (REPO / r.path).read_text(encoding="utf-8", newline="")
    got = d(live)
    want_ok = got == r.post_edit_digest
    v = resolve_authorised_artefact_state(
        manifest=r.manifest, action_id=r.action_id, path=r.path,
        pinned_post_digest=r.post_edit_digest, live_digest=got,
        records=records, history=M.GitArtefactHistory(REPO), live_text=live)
    undeclared_path = not any(x.is_succession and x.path == r.path for x in records)
    if undeclared_path and (v.ok != want_ok
                            or v.status != (LIVE_TERMINAL if want_ok else PIN_MISMATCH)):
        mismatched.append("%s/%s %s" % (r.manifest, r.action_id, v.describe()))
check("for every undeclared governed artefact, resolver == bare pin == live",
      not mismatched, mismatched or "%d entr(y/ies); successions declared in %s"
      % (len(governed), declared or "no record"))

added = []
for path in CORRECTIONS:
    doc = json.loads(path.read_text(encoding="utf-8"))
    names = [f.check for f in M.audit_correction_manifest(path)]
    gained = [n for n in names if n.startswith("succession_")
              or n == "governed_artefact_successions_non_empty"]
    if M.GOVERNED_ARTEFACT_SUCCESSION_FIELD not in doc and gained:
        added.append("%s: %s" % (path.name, gained))
check("no record without a succession gains a succession check", not added,
      added or "%d record(s) audited" % len(CORRECTIONS))

check("governed_artefact_successions is LOAD_BEARING",
      M.classify_correction("governed_artefact_successions") == M.LOAD_BEARING)
check("CORRECTION_STATUSES is unchanged",
      M.CORRECTION_STATUSES == ("AUTHORISED", "SUPERSEDED"), M.CORRECTION_STATUSES)
check("GOVERNED_ARTEFACT_CLASSES is unchanged (no succession class smuggled in)",
      M.GOVERNED_ARTEFACT_CLASSES == ("ARTEFACT_PROPAGATION",))
check("one digest convention: artefact_digest is LF-normalised sha256",
      d("a\r\nb\n") == d("a\nb\n") and len(d("x")) == 64)


print()
print("%d checks, %d FAIL" % (COUNT[0], len(FAILURES)))
for f in FAILURES:
    print("  FAIL %s" % f)
sys.exit(1 if FAILURES else 0)
