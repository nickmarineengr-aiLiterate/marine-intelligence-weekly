#!/usr/bin/env python3
"""R-7 rebased-correction provenance controls for tools/oral/oral_monthly.py
(FOUNDER-DECISION-R7-R8-20261113).

  python tools/oral/test_oral_monthly_provenance.py

Three layers:
  P  positive: the one listed record verifies on the live repository and keeps
     its October origin and November integration dates separately
  C  conservation: every OTHER manifest's event date and source are exactly what
     the plain rule (no allow-list) gives, and the listed record still fails
     under the plain rule -- the allow-list changes one record and nothing else
  N  negative / mutation: each forged, missing, unrelated or contradictory input
     to the pure check is refused, including a re-hashed forged October commit and
     an attacker who also re-pins the evidence hash

Prints "<N> checks, <M> FAIL". Reads the repository; writes nothing.
"""
from __future__ import annotations

import base64
import copy
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_monthly as MM  # noqa: E402

REL = "tools/oral/correction_corr_safety_hpfuel_pipe_20261022_manifest.json"
PATH = MM.L.REPO / REL
ENTRY = MM.REBASED_PROVENANCE[REL]
MAN = json.loads(PATH.read_text(encoding="utf-8"))
EVB = (MM.L.REPO / ENTRY["evidence"]).read_bytes()
ADDED = MM._git("log", "--diff-filter=A", "--format=%H", "-1", "--", str(PATH)).strip()
MSG = MM._git("log", "-1", "--format=%B", ADDED)
IDATE = dt.datetime.fromisoformat(MM._git("log", "-1", "--format=%cI", ADDED).strip())

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  - " + detail) if detail else ""))


def probs(manifest=MAN, entry=ENTRY, ev=EVB, added=ADDED, msg=MSG, idate=IDATE, local=None):
    return MM.rebased_provenance_problems(REL, manifest, entry, ev, added, msg, idate, local)


def refused(name, **kw):
    p = probs(**kw)
    check(name, p != [], (p[0][:150] if p else "ACCEPTED -- escape"))


def ev_doc():
    return json.loads(EVB.decode("utf-8"))


def pack(doc):
    return (json.dumps(doc, indent=1) + "\n").encode("utf-8")


def repinned(doc, **entry_over):
    """An attacker who can also edit the code pin: evidence re-hashed and pinned."""
    b = pack(doc)
    e = dict(ENTRY, evidence_sha256=hashlib.sha256(b).hexdigest(), **entry_over)
    return b, e


def obj(doc, kind):
    return next(o for o in doc["objects"] if o["type"] == kind)


def raw(o):
    return base64.b64decode(o["base64"])


def put(o, otype, body):
    o["type"], o["base64"] = otype, base64.b64encode(body).decode()
    o["id"] = MM._object_id(otype, body)


def main():
    # ---------------------------------------------------------------- P
    check("P1 pure check accepts the live record", probs() == [], "; ".join(probs())[:200])
    when, src = MM.manifest_event_date(PATH, MAN, MAN["correction_id"])
    check("P2 event date is the declared October date",
          (when, src) == (dt.date(2026, 10, 22), "declared+rebased-provenance"), "%s %s" % (when, src))
    rp = MM.rebased_provenance(PATH, MAN)
    check("P3 origin and integration kept separately",
          rp["origin_commit"] == ENTRY["origin_commit"] and rp["origin_date"] == dt.date(2026, 10, 23)
          and rp["integration_commit"] == ENTRY["integration_commit"]
          and rp["integration_date"] == dt.date(2026, 11, 12), str(rp))
    cbody = raw(next(o for o in ev_doc()["objects"] if o["id"] == ENTRY["origin_commit"]))
    check("P4 accepted with the origin object present locally and equal",
          probs(local=cbody) == [])
    check("P5 accepted with the origin object absent (fresh release clone)", probs(local=None) == [])
    check("P6 allow-list holds exactly one entry", list(MM.REBASED_PROVENANCE) == [REL])
    check("P7 rebind fields are exactly the documented four",
          MM.REBIND_FIELDS == {"founder_authorisation", "baseline_commit", "governing_commits", "note"})

    # ---------------------------------------------------------------- C
    plain, saved = {}, MM.REBASED_PROVENANCE
    files = MM._manifest_files()
    new = {}
    for f in files:
        m = json.loads(Path(f).read_text(encoding="utf-8"))
        new[MM._rel(f)] = MM.manifest_event_date(f, m, MM._manifest_gid(f, m))
    try:
        MM.REBASED_PROVENANCE = {}
        for f in files:
            m = json.loads(Path(f).read_text(encoding="utf-8"))
            try:
                plain[MM._rel(f)] = MM.manifest_event_date(f, m, MM._manifest_gid(f, m))
            except MM.MonthlyFailure as e:
                plain[MM._rel(f)] = ("FAIL", str(e)[:80])
    finally:
        MM.REBASED_PROVENANCE = saved
    others = [k for k in new if k != REL]
    diff = [k for k in others if new[k] != plain[k]]
    check("C1 every other manifest keeps its plain-rule date and source (%d records)" % len(others),
          not diff and len(others) > 100, str(diff[:3]))
    check("C2 the listed record still fails under the plain rule", plain[REL][0] == "FAIL", str(plain[REL]))
    check("C3 no other manifest needed or uses the provenance source",
          all(new[k][1] != "declared+rebased-provenance" for k in others))

    # ------------------------------------------------- N: entry and record
    refused("N1 no entry", entry=None)
    refused("N2 entry copied to another correction_id",
            manifest=dict(MAN, correction_id="CORR-SAFETY-OTHER-20261022"))
    refused("N3 declared date moved to November", manifest=dict(MAN, date="2026-11-12"))
    refused("N4 declared date moved to September", manifest=dict(MAN, date="2026-09-30"))
    refused("N5 declared date malformed", manifest=dict(MAN, date="22 Oct 2026"))
    m = copy.deepcopy(MAN)
    m["cards"][0]["after"] = "edited " + str(m["cards"][0].get("after", ""))
    refused("N6 current record's cards changed (not the same correction)", manifest=m)
    refused("N7 current record's title changed", manifest=dict(MAN, title="x"))
    refused("N8 extra key in the current record", manifest=dict(MAN, extra=1))
    m = dict(MAN)
    m.pop("review")
    refused("N9 key removed from the current record", manifest=m)
    check("N10 a rebind field may change without breaking the proof",
          probs(manifest=dict(MAN, note=MAN["note"] + " x")) == [])
    refused("N11 first-add commit is not the pinned integration commit", added="0" * 40)
    refused("N12 first-add commit missing (record not committed)", added=None)
    refused("N13 integration commit lacks the cherry-pick trailer",
            msg=MSG.replace("cherry picked from commit", "picked from"))
    refused("N14 trailer names a different origin",
            msg=MSG.replace(ENTRY["origin_commit"], "1" * 40))
    refused("N15 integration date before the origin date",
            idate=dt.datetime(2026, 10, 1, tzinfo=dt.timezone.utc))
    refused("N16 integration date missing", idate=None)
    refused("N17 local origin object differs from the evidence", local=b"tree 0\n")

    # ------------------------------------------------- N: evidence
    refused("N20 evidence missing", ev=None)
    refused("N21 evidence one byte altered (pin catches it)", ev=EVB[:-2] + b"X\n")
    refused("N22 evidence not JSON (re-pinned)", **dict(zip(("ev", "entry"),
            (b"nope", dict(ENTRY, evidence_sha256=hashlib.sha256(b"nope").hexdigest())))))
    d = ev_doc()
    d["schema"] = "miw-rebased-provenance/0"
    b, e = repinned(d)
    refused("N23 wrong schema (re-pinned)", ev=b, entry=e)
    d = ev_doc()
    d["path"] = "tools/oral/correction_other_manifest.json"
    b, e = repinned(d)
    refused("N24 evidence for another path (re-pinned)", ev=b, entry=e)
    d = ev_doc()
    blob = obj(d, "blob")
    blob["base64"] = base64.b64encode(raw(blob) + b" ").decode()
    b, e = repinned(d)
    refused("N25 object body altered, id kept (re-pinned)", ev=b, entry=e)
    d = ev_doc()
    d["objects"] = [o for o in d["objects"] if o["type"] != "blob"]
    b, e = repinned(d)
    refused("N26 record blob missing from the evidence (re-pinned)", ev=b, entry=e)
    d = ev_doc()
    d["objects"] = [o for o in d["objects"] if o["id"] != MM._parse_tree(
        raw(next(x for x in d["objects"] if x["type"] == "tree" and b"tools" in raw(x)[:4000])))
        .get("tools", ("", ""))[1]]
    b, e = repinned(d)
    refused("N27 a tree on the path missing (re-pinned)", ev=b, entry=e)
    d = ev_doc()
    extra = {"type": "blob", "base64": base64.b64encode(b"unrelated").decode()}
    extra["id"] = MM._object_id("blob", b"unrelated")
    d["objects"].append(extra)
    b, e = repinned(d)
    refused("N28 extra unrelated object in the evidence (re-pinned)", ev=b, entry=e)
    d = ev_doc()
    d["objects"].append(dict(d["objects"][0]))
    b, e = repinned(d)
    refused("N29 duplicate object (re-pinned)", ev=b, entry=e)
    d = ev_doc()
    obj(d, "blob")["type"] = "tree"
    b, e = repinned(d)
    refused("N30 object type relabelled (re-pinned)", ev=b, entry=e)
    refused("N31 entry pins a different origin record blob",
            entry=dict(ENTRY, origin_record_blob="2" * 40))

    # ------------------------------------------------- N: fabricated October history
    # A forged commit object with a valid hash: same tree, new message.
    d = ev_doc()
    c = obj(d, "commit")
    put(c, "commit", raw(c).replace(b"NOT FOR PUSH", b"FORGED"))
    d["origin_commit"] = c["id"]
    b, e = repinned(d)
    refused("N40 re-hashed forged commit, code pin unchanged", ev=b, entry=e)
    b, e = repinned(d, origin_commit=c["id"])
    refused("N41 forged commit AND code pin moved to it (trailer still names the real origin)",
            ev=b, entry=e)
    check("N42 ...and refused for the trailer, not by accident",
          any("cherry-pick origin" in x for x in probs(ev=b, entry=e)))
    # Forged origin with a November committer date: everything re-pinned and the
    # trailer rewritten -- the month rule must still refuse it.
    d = ev_doc()
    c = obj(d, "commit")
    body = raw(c)
    lines = body.split(b"\n")
    nov = int(dt.datetime(2026, 11, 2, tzinfo=dt.timezone.utc).timestamp())
    lines = [(l.rsplit(b" ", 2)[0] + b" %d +0000" % nov) if l.startswith((b"committer ", b"author ")) else l
             for l in lines]
    put(c, "commit", b"\n".join(lines))
    d["origin_commit"] = c["id"]
    b, e = repinned(d, origin_commit=c["id"])
    refused("N43 origin re-dated to November, fully re-pinned, trailer forged",
            ev=b, entry=e, msg=MSG.replace(ENTRY["origin_commit"], c["id"]))
    check("N44 ...and refused for the month",
          any("declared month" in x for x in probs(ev=b, entry=e,
                                                       msg=MSG.replace(ENTRY["origin_commit"], c["id"]))))
    # Only the author line in another month.
    d = ev_doc()
    c = obj(d, "commit")
    lines = raw(c).split(b"\n")
    lines = [(l.rsplit(b" ", 2)[0] + b" %d +0000" % nov) if l.startswith(b"author ") else l for l in lines]
    put(c, "commit", b"\n".join(lines))
    d["origin_commit"] = c["id"]
    b, e = repinned(d, origin_commit=c["id"])
    refused("N45 author date in another month (committer October)",
            ev=b, entry=e, msg=MSG.replace(ENTRY["origin_commit"], c["id"]))

    # ------------------------------------------------- N: future backdating
    saved_added = MM._git_added_date
    try:
        MM._git_added_date = lambda p: dt.date(2026, 12, 3)
        fake = MM.L.REPO / "tools/oral/correction_corr_future_backdated_20261101_manifest.json"
        try:
            MM.manifest_event_date(fake, {"date": "2026-11-01", "correction_id": "CORR-FUTURE"}, "CORR-FUTURE")
            check("N50 unlisted backdated record is refused", False, "ACCEPTED -- escape")
        except MM.MonthlyFailure as ex:
            check("N50 unlisted backdated record is refused", "different months" in str(ex), str(ex)[:120])
    finally:
        MM._git_added_date = saved_added
    saved = MM.REBASED_PROVENANCE
    try:
        MM.REBASED_PROVENANCE = dict(saved)
        MM.REBASED_PROVENANCE["tools/oral/correction_corr_safety_eebd_entry_20261019_manifest.json"] = ENTRY
        other = MM.L.REPO / "tools/oral/correction_corr_safety_eebd_entry_20261019_manifest.json"
        om = json.loads(other.read_text(encoding="utf-8"))
        try:
            MM.manifest_event_date(other, om, om["correction_id"])
            check("N51 entry copied onto another record is refused", False, "ACCEPTED -- escape")
        except MM.MonthlyFailure as ex:
            check("N51 entry copied onto another record is refused", "refused" in str(ex), str(ex)[:120])
    finally:
        MM.REBASED_PROVENANCE = saved

    n_fail = sum(1 for _, ok in RESULTS if not ok)
    print("%d checks, %d FAIL" % (len(RESULTS), n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
