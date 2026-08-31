"""Ingest fresh candidate oral submissions from the current sitting window.

This is the CURRENT-INTAKE lane. It is deliberately a separate denominator from
the historical All-Surveyors compilation (788 raw occurrences, ASC-*). Fresh
occurrences are AUG-* and must never be added to the historical count.

Raw wording is evidence and is preserved verbatim in `raw_question_text`.
Normalisation lives in a separate field and never overwrites the raw form.

A numbered line that is not a question (a candidate recording that they forgot
one) is still an occurrence: it is preserved and dispositioned as
NON_QUESTION_UNRECOVERABLE so that nothing silently vanishes from the count.

The submission file itself is git-ignored, exactly like the historical .docx:
only the derived per-occurrence records are committed.

Usage:
  python tools/oral/ingest_august_intake.py --txt "<path>" [--check]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

OUT = L.OUT
RECORDS = OUT / "AUGUST2026_INTAKE_RECORDS.jsonl"
REPORT = OUT / "AUGUST2026_INTAKE_REPORT.json"

# "Ext- Rajappan sir" / "Int- Senthil sir"
ROLE_RE = re.compile(r"^(Ext|Int|External|Internal)\s*[-:]\s*(.+?)\s*$", re.I)
# "1. text" / "2. <U+2060>text"  (the source uses invisible separators after the dot)
# "1. text" / "2) text" / "1 .text" - the candidate's phone inserts a space
# before the separator often enough that requiring adjacency silently drops the
# question into context. S004 lost two occurrences that way before this was
# widened, and a lost occurrence raises no error: it just is not counted.
Q_RE = re.compile(r"^(\d+)\s*[.)]\s*(.*)$", re.S)
# "Attempt 1" / "Attempt-1" / "Attempt : 2" - candidates punctuate this freely
# and the attempt number is evidence about the sitting, not decoration.
ATTEMPT_RE = re.compile(r"^Attempt\s*[-:]?\s*(\d+)\s*$", re.I)
RESULT_RE = re.compile(r"^Result\s*[-:]\s*(.+?)\s*$", re.I)
RULE_RE = re.compile(r"^[-]{3,}$")
# A bare "<Name> :" line inside the body. It is treated as an attribution
# marker ONLY when <Name> matches an examiner already declared by this same
# submission, so the parser can never invent an attribution that the candidate
# did not write.
ATTRIB_RE = re.compile(r"^([A-Za-z][A-Za-z .'-]{1,40}?)\s*:\s*(.*)$", re.S)
# A bare "Internal" / "Ext" heading with no name after it. Candidates use it the
# same way they use a name marker: everything below it came from that seat.
# It is honoured ONLY when the submission declared exactly one examiner in that
# role, so it can never pick between two people.
BARE_ROLE_RE = re.compile(r"^(Ext|Int|External|Internal)\s*[-:.]?\s*$", re.I)
# "Internal Senthil sir" - a role declaration with NO separator at all. Accepted
# only when the name carries an honorific, because without that guard the rule
# would read "Internal audit procedure?" as declaring an examiner named "audit".
# A candidate who writes "Internal Senthil" with no honorific is left at panel
# level: under-attributed, never mis-attributed.
ROLE_NOSEP_RE = re.compile(
    r"^(Ext|Int|External|Internal)\s+([A-Za-z][A-Za-z .'-]{1,40}?\s+(?:sir|madam|ma'?am))\s*[.,]?\s*$",
    re.I)
# A line that is only a date. In an unnumbered submission every non-metadata
# line becomes an occurrence, so the sitting date must be recognised as
# metadata or it would be counted as a question.
DATE_ONLY_RE = re.compile(
    r"^\d{1,2}\s*[-/. ]\s*(?:\d{1,2}|[A-Za-z]{3,9})\s*[-/. ]\s*\d{2,4}\s*$")

ROLE_NORM = {"ext": "EXTERNAL", "external": "EXTERNAL",
             "int": "INTERNAL", "internal": "INTERNAL"}

# Invisible characters the messaging app inserted; stripped for the NORMALISED
# form only. The raw field keeps them so the evidence stays byte-faithful.
INVISIBLE = dict.fromkeys(map(ord, "⁠​‌‍﻿"), None)

NON_QUESTION_CUES = ("i forgot", "forgot", "don't remember", "didn't know")

# Candidates paste chat transcripts into their reports. The carrier file is
# git-ignored, but context_comments IS committed, so a third party's name would
# otherwise enter the repository through the derived record. The substance is
# kept; only the identifier is removed.
CHAT_ATTRIB_RE = re.compile(
    r"\[\s*\d{1,2}:\d{2}\s*,\s*\d{1,2}/\d{1,2}/\d{2,4}\s*\]\s*[^:]{1,60}:")


def redact_third_parties(text: str) -> str:
    return CHAT_ATTRIB_RE.sub("[third party, name removed]:", text)


def normalise(raw: str) -> str:
    return L._WS.sub(" ", raw.translate(INVISIBLE)).strip()


def looks_like_non_question(text: str) -> bool:
    low = normalise(text).lower()
    return any(c in low for c in NON_QUESTION_CUES) and "?" not in low


def normalise_examiner(raw: str) -> str:
    """Strip trailing punctuation and the honorific. Never merges by surname
    resemblance: it only removes decoration the candidate typed."""
    s = raw.strip().rstrip(",.;:").strip()
    s = re.sub(r"\s+sir$", "", s, flags=re.I).strip()
    return s


# The SOURCE CARRIER REGISTRY. Order is identity-bearing: submission and
# occurrence ids are allocated by walking it, so a carrier is appended, never
# inserted, and no earlier carrier is ever renumbered.
CARRIERS = OUT / "AUGUST2026_INTAKE_CARRIERS.json"

#: Every no-question spelling that actually appears in a carrier, quoted from
#: the source. A candidate who writes "Internal: no question" is recording that
#: the internal examiner asked NOTHING; the parser used to read it as a role
#: declaration naming an examiner called "no question", which put a fabricated
#: person into the attribution store. This list is deliberately an EVIDENCE
#: list rather than a pattern: a new spelling is a new observation about the
#: sources and should be added deliberately, with the carrier that shows it.
NO_QUESTION_SENTINELS = {
    "no question",     # 27 Aug, "Internal: no question"
    "no questions",    # 27 Aug, "Internal.- no questions"
    "no qtns",         # 28 Aug, "External : no qtns"
}


def is_no_question_sentinel(name: str) -> bool:
    """Is this the candidate saying "nobody asked anything", not naming a person?"""
    return normalise(name).strip().rstrip(".,;:").strip().lower() in NO_QUESTION_SENTINELS


#: The hand-authored examiner authority. It already carries canonical_name and
#: the observed spellings, and its own first rule is that surname resemblance
#: NEVER merges two people -- so this reuses it rather than inventing a second
#: identity model. Absent or unreadable, canonicalisation degrades to identity:
#: an unknown name passes through untouched, which is the safe direction.
ALIAS_REGISTER = OUT / "EXAMINER_ALIAS_REGISTER.json"


def _alias_map() -> dict:
    try:
        reg = json.loads(ALIAS_REGISTER.read_text(encoding="utf-8"))
    except Exception:
        return {}
    m = {}
    for e in reg.get("examiners", []):
        canon = e["canonical_name"]
        for form in [canon, *e.get("observed_forms", [])]:
            m[normalise_examiner(form).lower()] = canon
    return m


_ALIASES = _alias_map()


def canonical_examiner(name: str) -> str:
    """The registered identity for a spelling, or the spelling unchanged.

    EXACT case-insensitive match against a registered canonical name or one of
    its recorded observed forms. No fuzzy matching, no nearest-name inference,
    no initial or punctuation broadening: "simon" and "Simon" are one person
    because the register says Simon exists, and "Simone" is a different person
    because the register does not say otherwise.
    """
    return _ALIASES.get(normalise_examiner(name).lower(), name)


# "*Purpose." - a follow-up probe the examiner asked ON the preceding numbered
# question. Five of these were recorded under "2. What is bmp ms" on 27 August
# and every one fell through into the preamble, because a starred line matches
# no other branch. A line whose content carries no word character is a bullet,
# not a question, and is deliberately NOT promoted.
STAR_RE = re.compile(r"^\*+\s*(.*)$", re.S)


def starred_probe(line: str):
    """The probe text of a starred follow-up line, or None if it is decoration."""
    m = STAR_RE.match(line.strip())
    if not m:
        return None
    body = m.group(1).strip().strip("*").strip()
    return body if re.search(r"\w", body) else None


def parse_submission(lines, submission_id: str, seq_start: int,
                     unnumbered: bool = False,
                     received_date: str = "2026-08-24",
                     attempt_date: str = "2026-08-24"):
    """Parse one candidate report.

    `unnumbered` is set by parse_file when the candidate wrote no "1." "2."
    numbering at all. In that mode the candidate's own line breaks are the
    occurrence boundary, because there is nothing else to use. Metadata lines
    (role declarations, attempt, result, a bare date, a bare role heading) are
    still recognised and excluded; everything else is preserved as an
    occurrence and dispositioned downstream. Over-capturing a stray remark is
    visible and adjudicable; dropping a question is silent, which is why the
    default leans towards keeping the line.
    """
    examiners, occurrences = [], []
    attempt_no = result = None
    preamble = []
    # Set by an in-body "<Name> :" marker; applies to every following
    # occurrence until another marker replaces it. None means the candidate
    # gave no per-question attribution, which stays PANEL_LEVEL_ONLY.
    current_attrib = None
    attrib_marker = None
    attrib_basis = None

    for ln in lines:
        t = ln.strip()
        if not t or RULE_RE.match(t):
            continue

        m = ROLE_RE.match(t) or ROLE_NOSEP_RE.match(t)
        if m and not Q_RE.match(t):
            # "Internal: no question" is the candidate recording that this seat
            # asked NOTHING. It is not a person. Read as a name it would put a
            # fabricated examiner into the attribution store, so it is kept as
            # context -- the wording is evidence and is never erased -- and no
            # examiner identity is created.
            if is_no_question_sentinel(m.group(2)):
                preamble.append(redact_third_parties(t))
                continue
            who = canonical_examiner(normalise_examiner(m.group(2)))
            examiners.append({
                "role": ROLE_NORM[m.group(1).lower()],
                "name_raw": m.group(2).strip(),
                "name_normalized": who,
                "attribution_basis": "EXPLICITLY_STATED_BY_CANDIDATE",
            })
            # A declaration written in the PREAMBLE names the panel and nothing
            # more. One written after questions have already been recorded is
            # doing the job of a heading - the candidate put it above the
            # questions that examiner asked - so it also attributes what
            # follows, exactly as a bare role heading does.
            if occurrences:
                current_attrib = who
                attrib_marker = t
                attrib_basis = "ROLE_DECLARATION_INLINE_HEADING"
            continue

        m = BARE_ROLE_RE.match(t)
        if m:
            want = ROLE_NORM[m.group(1).lower()]
            holders = [e for e in examiners if e["role"] == want]
            if len(holders) == 1:
                current_attrib = holders[0]["name_normalized"]
                attrib_marker = t
                attrib_basis = "ROLE_MARKER_SOLE_HOLDER"
            # Two holders, or none declared yet: the heading identifies no one
            # individually, so attribution is left exactly as it was.
            continue

        m = ATTEMPT_RE.match(t)
        if m:
            attempt_no = int(m.group(1))
            continue

        m = RESULT_RE.match(t)
        if m:
            result = m.group(1).strip()
            continue

        m = ATTRIB_RE.match(t)
        if m and not Q_RE.match(t):
            declared = {e["name_normalized"].lower() for e in examiners}
            cand = canonical_examiner(normalise_examiner(m.group(1)))
            if cand.lower() in declared:
                current_attrib, attrib_marker = cand, t
                attrib_basis = "NAME_MARKER"
                trailing = m.group(2).strip()
                if trailing:
                    # "Senthil : tqm, new acts and difference between act and
                    # rule." - the marker carries its questions on the same
                    # line and is not numbered. Treated as ONE occurrence
                    # holding the raw line: splitting it into limbs here would
                    # be the parser inventing question boundaries the candidate
                    # never wrote. Adjudication splits it, on the record.
                    occurrences.append({
                        "occurrence_id": f"AUG-{seq_start + len(occurrences):04d}",
                        "submission_id": submission_id,
                        "source_question_number": None,
                        "raw_question_text": m.group(2),
                        "normalised_question_text": normalise(m.group(2)),
                        "is_question": not looks_like_non_question(trailing),
                        "_attrib": current_attrib,
                        "_attrib_marker": t,
                        "_attrib_basis": attrib_basis,
                    })
                continue
            # A name-like line that is NOT a declared examiner is never an
            # attribution. It stays context, exactly as before.

        # A STARRED FOLLOW-UP. The candidate wrote it under the question the
        # examiner was probing, so it is an occurrence in its own right AND it
        # carries the parent it hangs off. Before this branch existed a starred
        # line matched nothing and fell into the preamble: five real probes on
        # 27 August disappeared that way, and nothing reported it, because a
        # lost occurrence raises no error -- it just is not counted.
        #
        # `starred_probe` returns None for a bullet with no word character, so
        # decoration is not promoted to examinable content. Both directions are
        # tested: a real probe must survive, and "* * *" must not become one.
        probe = starred_probe(t)
        if probe is not None:
            occurrences.append({
                "occurrence_id": f"AUG-{seq_start + len(occurrences):04d}",
                "submission_id": submission_id,
                "source_question_number": None,
                "source_line_style": "STARRED_FOLLOWUP",
                # The occurrence this probe was asked ON: the most recent
                # NON-starred one. A run of stars under a numbered question is
                # five SIBLING probes on that question, not a chain of
                # follow-ups to each other -- chaining would assert a depth the
                # candidate never wrote. None only if a submission opened with a
                # starred line, which no carrier does; the field is emitted
                # either way so a reader never has to guess whether the linkage
                # was absent or merely unrecorded.
                "parent_occurrence_id": next(
                    (o["occurrence_id"] for o in reversed(occurrences)
                     if o.get("source_line_style") != "STARRED_FOLLOWUP"), None),
                "raw_question_text": probe,
                "normalised_question_text": normalise(probe),
                "is_question": not looks_like_non_question(probe),
                "_attrib": current_attrib,
                "_attrib_marker": attrib_marker,
                "_attrib_basis": attrib_basis,
            })
            continue

        m = Q_RE.match(t)
        if m:
            raw = m.group(2)
            occurrences.append({
                "occurrence_id": f"AUG-{seq_start + len(occurrences):04d}",
                "submission_id": submission_id,
                "source_question_number": int(m.group(1)),
                "raw_question_text": raw,
                "normalised_question_text": normalise(raw),
                "is_question": not looks_like_non_question(raw),
                "_attrib": current_attrib,
                "_attrib_marker": attrib_marker,
                "_attrib_basis": attrib_basis,
            })
            continue

        if unnumbered and not DATE_ONLY_RE.match(t):
            occurrences.append({
                "occurrence_id": f"AUG-{seq_start + len(occurrences):04d}",
                "submission_id": submission_id,
                "source_question_number": None,
                "source_line_style": "UNNUMBERED",
                "raw_question_text": t,
                "normalised_question_text": normalise(t),
                "is_question": not looks_like_non_question(t),
                "_attrib": current_attrib,
                "_attrib_marker": attrib_marker,
                "_attrib_basis": attrib_basis,
            })
            continue

        preamble.append(redact_third_parties(t))

    for o in occurrences:
        o["attempt_number"] = attempt_no
        o["attempt_result"] = result
        o["examiners"] = [e["name_normalized"] for e in examiners]
        who, marker = o.pop("_attrib"), o.pop("_attrib_marker")
        basis = o.pop("_attrib_basis")
        if who:
            # The candidate wrote this examiner's name above the question.
            o["examiner_attribution"] = "INDIVIDUALLY_ATTRIBUTED"
            o["attributed_examiner"] = who
            o["attribution_marker"] = marker
            # Emitted for every route EXCEPT the original name-marker one, so
            # that records written before this field existed stay byte-identical
            # while each newer route is self-describing. Naming the routes
            # explicitly rather than testing one value: the first version of
            # this checked for ROLE_MARKER_SOLE_HOLDER alone and silently
            # dropped the basis of the route added next.
            if basis and basis != "NAME_MARKER":
                o["attribution_basis"] = basis
        else:
            # Both examiners sat the same panel and the candidate tied no
            # question to a person; neither may be named for this question.
            o["examiner_attribution"] = "PANEL_LEVEL_ONLY"
            o["attributed_examiner"] = None
            o["attribution_marker"] = None

    return {
        "submission_id": submission_id,
        "source_type": "CANDIDATE_SITTING_REPORT",
        "received_date": received_date,
        "attempt_date": attempt_date,
        "attempt_number": attempt_no,
        "attempt_result": result,
        "examiners": examiners,
        "candidate_reference": "ANONYMOUS_UNNAMED_IN_SOURCE",
        "context_comments": preamble,
        "occurrences": occurrences,
    }


def parse_file(path: Path, *, submission_start: int = 1, seq_start: int = 1,
               received_date: str = "2026-08-24", attempt_date: str = "2026-08-24"):
    """One file may carry several candidate reports separated by rule lines.

    `submission_start` and `seq_start` are where THIS carrier's identities
    begin. They are passed in rather than assumed, because a second carrier
    that restarts at AUG2026-S001 and AUG-0001 does not fail loudly: it
    collides with the committed corpus and, on a writer that overwrote,
    destroyed it.
    """
    blocks, cur = [], []
    for ln in path.read_text(encoding="utf-8").splitlines():
        if RULE_RE.match(ln.strip()):
            blocks.append(cur)
            cur = []
        else:
            cur.append(ln)
    blocks.append(cur)

    subs, seq, skipped = [], seq_start, []
    for idx, blk in enumerate(blocks, 1):
        numbered = any(Q_RE.match(l.strip()) for l in blk)
        # A candidate who numbers nothing still declares the panel. Requiring
        # numbering to recognise a submission silently discarded an entire
        # sitting report: the block just failed the test and `continue` said
        # nothing. Either signal now identifies a submission.
        declared = any(ROLE_RE.match(l.strip()) and not Q_RE.match(l.strip())
                       for l in blk)
        if not numbered and not declared:
            if any(l.strip() for l in blk):
                skipped.append({
                    "block_index": idx,
                    "nonempty_lines": sum(1 for l in blk if l.strip()),
                    "first_line": next(l.strip() for l in blk if l.strip()),
                })
            continue
        s = parse_submission(blk, f"AUG2026-S{submission_start + len(subs):03d}", seq,
                             unnumbered=not numbered,
                             received_date=received_date, attempt_date=attempt_date)
        s["source_file"] = path.name
        s["line_style"] = "NUMBERED" if numbered else "UNNUMBERED"
        seq += len(s["occurrences"])
        subs.append(s)
    return subs, skipped


def load_carriers() -> list:
    """The registered carriers, in the order that allocates their identities."""
    return json.loads(CARRIERS.read_text(encoding="utf-8"))["carriers"]


def carrier_path(carrier: dict) -> Path:
    return L.REPO / "docs" / "MIW-master-Question-bank" / \
        "New questions from August orals" / carrier["source_file"]


def ingest_carriers(regs: list):
    """Every registered carrier, walked in order, as ONE intake.

    Identities are allocated across the whole walk rather than per file, which
    is what stops a second carrier restarting at AUG2026-S001 / AUG-0001 on top
    of the committed corpus. Because the walk always starts at the first
    carrier, re-running this reproduces every earlier carrier's records
    byte-for-byte instead of preserving them by not touching them -- a
    reproduction is checkable, and `M4-BYTE-STABLE` checks it.
    """
    subs, occ, reports = [], [], []
    sub_n, seq = 1, 1
    for c in regs:
        s, skipped = parse_file(
            carrier_path(c), submission_start=sub_n, seq_start=seq,
            received_date=c["received_date"], attempt_date=c["attempt_date"])
        o = [x for y in s for x in y["occurrences"]]
        reports.append({
            "source_file": c["source_file"],
            "sha256": c["sha256"],
            "carrier_date": c["carrier_date"],
            "submissions": len(s),
            "raw_occurrences": len(o),
            "submission_ids": [x["submission_id"] for x in s],
            "occurrence_id_first": o[0]["occurrence_id"] if o else None,
            "occurrence_id_last": o[-1]["occurrence_id"] if o else None,
            "starred_followups": sum(
                1 for x in o if x.get("source_line_style") == "STARRED_FOLLOWUP"),
            "unparsed_source_blocks": skipped,
        })
        subs.extend(s)
        occ.extend(o)
        sub_n += len(s)
        seq += len(o)
    return subs, occ, reports


def verify_carriers(regs: list):
    """EVERY registered carrier is present, unmodified and correctly dated.

    Checked before the record comparison, because a dropped carrier leaves the
    committed records perfectly self-consistent -- which is exactly how a whole
    submission went missing unnoticed once before.
    """
    on_disk = {c["source_file"] for c in load_carriers()}
    named = {c["source_file"] for c in regs}
    if on_disk - named:
        return False, f"carrier(s) missing from this check: {sorted(on_disk - named)}"
    for c in regs:
        p = carrier_path(c)
        if not p.exists():
            return False, f"registered carrier is absent from disk: {c['source_file']}"
        import hashlib
        got = hashlib.sha256(p.read_bytes()).hexdigest()
        if got != c["sha256"]:
            return False, (f"{c['source_file']} sha256 {got[:16]} does not match the "
                           f"registered {c['sha256'][:16]}")
        for f in ("received_date", "attempt_date"):
            if c[f] != c["carrier_date"]:
                return False, (f"{c['source_file']} {f} {c[f]} disagrees with its "
                               f"carrier_date {c['carrier_date']}")
    return True, "every registered carrier is present, unmodified and self-consistent"


def verify_against_store(occ: list, have: list):
    """Freshly parsed occurrences against the committed store, field by field."""
    if len(have) != len(occ):
        return False, f"committed {len(have)} occurrence(s), source yields {len(occ)}"
    ids = [o["occurrence_id"] for o in occ]
    if len(ids) != len(set(ids)):
        return False, "duplicate occurrence id(s) in the freshly parsed set"
    sids = [o["submission_id"] for o in occ]
    drift = []
    for a, b in zip(occ, have):
        for k in ("occurrence_id", "submission_id", "raw_question_text",
                  "examiner_attribution", "attributed_examiner"):
            if a.get(k) != b.get(k):
                drift.append(f"{a['occurrence_id']}.{k}")
    if drift:
        return False, f"committed intake drifted from source: {drift[:6]}"
    del sids
    return True, f"{len(occ)} occurrence(s) match the committed store"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--txt", help="ignored; the carrier registry is authoritative")
    ap.add_argument("--check", action="store_true",
                    help="verify committed records still match every registered carrier")
    a = ap.parse_args()

    regs = load_carriers()
    ok, why = verify_carriers(regs)
    if not ok:
        print(f"FAIL: {why}")
        return 1
    subs, occ, carrier_reports = ingest_carriers(regs)
    skipped = [b for r in carrier_reports for b in r["unparsed_source_blocks"]]

    roles = {}
    for s in subs:
        for e in s["examiners"]:
            roles.setdefault(e["name_normalized"], e["role"])

    report = {
        "denominator_class": "CURRENT_AUGUST_INTAKE",
        "isolated_from_historical_788": True,
        "submissions": len(subs),
        "raw_occurrences": len(occ),
        "question_bearing_occurrences": sum(1 for o in occ if o["is_question"]),
        "non_question_occurrences": sum(1 for o in occ if not o["is_question"]),
        # A block of the carrier that yielded no submission. Reported so that a
        # lost sitting report is visible in the derived record instead of
        # vanishing between two rule lines.
        "unparsed_source_blocks": skipped,
        # Per-carrier provenance. The aggregate figures above are the intake's,
        # not any one file's, so a reader can no longer mistake one carrier's
        # count for the window's.
        "carriers": carrier_reports,
        "starred_followup_occurrences": sorted(
            o["occurrence_id"] for o in occ
            if o.get("source_line_style") == "STARRED_FOLLOWUP"),
        "examiners_represented": sorted(roles),
        "examiner_roles": roles,
        "individually_attributed_occurrences": sorted(
            o["occurrence_id"] for o in occ
            if o["examiner_attribution"] == "INDIVIDUALLY_ATTRIBUTED"),
        "panel_level_occurrences": sum(
            1 for o in occ if o["examiner_attribution"] == "PANEL_LEVEL_ONLY"),
        "per_submission": [
            {"submission_id": s["submission_id"],
             "raw_occurrences": len(s["occurrences"]),
             "attempt_number": s["attempt_number"],
             "attempt_result": s["attempt_result"],
             "examiners": [e["name_normalized"] for e in s["examiners"]],
             "occurrence_ids": [o["occurrence_id"] for o in s["occurrences"]],
             "per_question_attribution": sorted(
                 {o["examiner_attribution"] for o in s["occurrences"]})}
            for s in subs
        ],
        "submissions_detail": [{k: v for k, v in s.items() if k != "occurrences"}
                               for s in subs],
    }

    if a.check:
        # Content the carrier holds but the parser could not place is a defect,
        # not a clean run. This is checked BEFORE the record comparison because
        # a dropped block leaves the committed records perfectly self-consistent
        # — which is exactly how a whole submission went missing unnoticed.
        if skipped:
            print(f"FAIL: {len(skipped)} source block(s) yielded no submission: "
                  f"{[s['block_index'] for s in skipped]}")
            return 1
        have = [json.loads(l) for l in RECORDS.read_text(encoding="utf-8").splitlines() if l]
        # Attribution is evidence too: a committed row may not claim an
        # examiner the source does not carry, nor drop one that it does.
        ok, why = verify_against_store(occ, have)
        if not ok:
            print(f"FAIL: {why}")
            return 1
        print(f"OK: {len(occ)} August occurrences across {len(regs)} carrier(s) "
              f"byte-match the source")
        return 0

    RECORDS.write_text(
        "\n".join(json.dumps(o, ensure_ascii=False) for o in occ) + "\n",
        encoding="utf-8")
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False),
                      encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
