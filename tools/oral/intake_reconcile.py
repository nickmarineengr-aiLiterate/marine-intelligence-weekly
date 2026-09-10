"""PL-02 intake reconciliation: every source line, and every repeat, accounted for.

THE RULE THIS ENFORCES
----------------------
An unknown input shape must produce VISIBLE_UNPARSED_INPUT, never ZERO
QUESTIONS. Every grammar this pipeline has met arrived in a carrier the parser
had never seen, and every time the parser failed SILENTLY: 24 August lost a whole
submission to `1.`-only recognition, 27 August lost five starred probes,
31 August lost four lettered root asks and one unnumbered question and reported
`unparsed_blocks: []` while doing it. A lost occurrence raises no error. It
simply is not counted.

So this module walks every non-empty line of a carrier and requires each to reach
exactly ONE accountable disposition, and it refuses the write path when any line
does not. It reuses the ingest's own block split, submission test and parser --
never a second copy -- because a ledger that describes a different partition from
the one that produced the records proves nothing about the records.

Duplicates are the other half. A repeat is not a loss and is never discarded: a
question two candidates both report is evidence about what examiners ask. It is
identified, linked to the first occurrence of its text, counted, and kept.

Usage:
  python tools/oral/intake_reconcile.py              # every registered carrier
  python tools/oral/intake_reconcile.py --json       # the ledger as JSON
  python tools/oral/intake_reconcile.py --out <path> # write the ledger
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ingest_august_intake as I  # noqa: E402

#: The complete disposition vocabulary. A line reaches exactly one of these, and
#: `UNACCOUNTED` must always be empty -- it is the defect, not a category.
DISPOSITIONS = (
    "OCCURRENCE",            # became an examinable occurrence record
    "CONTEXT_COMMENT",       # preserved verbatim in context_comments
    "EXAMINER_DECLARATION",  # named a panel member
    "METADATA_CONSUMED",     # consumed into attempt / result / attribution state
    "UNPARSED_BLOCK",        # in a block that yielded no submission at all
    "UNACCOUNTED",           # reached nothing -- always a defect
)

#: The metadata branches of `parse_submission`, in one place. A line consumed by
#: one of these is accounted for by the VALUE it produced, not by surviving as
#: text: "Result - Pass" becomes attempt_result and "Internal:" becomes an
#: attribution state. Requiring those to reappear verbatim was the first version
#: of this idea's own bug, and it would have driven the fix in exactly the wrong
#: direction -- towards keeping copies of lines the parser had understood.
def _metadata_match(line: str) -> bool:
    t = line.strip()
    return bool(I.RESULT_RE.match(t) or I.ATTEMPT_RE.match(t)
                or I.ATTEMPT_ORDINAL_RE.match(t) or I.BARE_ROLE_RE.match(t)
                or I.CROSS_Q_RE.match(t) or I.DATE_ONLY_RE.match(t))


_NONWORD = re.compile(r"[^0-9a-z ]+")


def duplicate_key(text: str) -> str:
    """The identity a repeat is matched on.

    Case, punctuation and the invisible characters the messaging app inserts are
    decoration: a candidate who writes "what is the purpose of the ism code ?" is
    reporting the same ask as "What is the purpose of the ISM Code?". Word order
    and wording are NOT normalised -- no stemming, no synonym folding, no fuzzy
    distance -- so two differently worded asks about one subject stay two asks.
    """
    return re.sub(r"\s+", " ", _NONWORD.sub(" ", I.normalise(text).lower())).strip()


def parse_text(text: str, source_name: str = "synthetic.txt"):
    """Parse a carrier's text exactly as the ingest would."""
    return I.parse_source(text.splitlines(), source_name=source_name)


def reconcile_text(text: str, source_name: str = "synthetic.txt") -> dict:
    """The ledger for one carrier: every line disposed, every repeat linked."""
    lines = text.splitlines()
    blocks = I.split_blocks(lines)
    subs, skipped = I.parse_source(lines, source_name=source_name)

    # The i-th submission-yielding block produced the i-th submission. Both walks
    # use `split_blocks` and `block_is_submission`, so the pairing is exact
    # rather than inferred.
    paired: list[tuple[list[str], dict | None]] = []
    si = 0
    for blk in blocks:
        is_sub, _ = I.block_is_submission(blk)
        if is_sub:
            paired.append((blk, subs[si] if si < len(subs) else None))
            si += 1
        else:
            paired.append((blk, None))

    counts: dict[str, int] = {}
    unaccounted: list[dict] = []
    meaningful = 0
    occurrences: list[dict] = []
    zero_yield: list[dict] = []

    for bi, (blk, sub) in enumerate(paired, 1):
        body = [l for l in blk
                if l.strip() and not I.RULE_RE.match(l.strip())]
        meaningful += len(body)
        if sub is None:
            if body:
                counts["UNPARSED_BLOCK"] = counts.get("UNPARSED_BLOCK", 0) + len(body)
            continue

        occurrences.extend(sub["occurrences"])
        occ_keys = {duplicate_key(o["raw_question_text"]) for o in sub["occurrences"]}
        comment_keys = {duplicate_key(c) for c in sub["context_comments"]}
        examiner_lines = {I.normalise(e["name_raw"]).lower()
                          for e in sub["examiners"]}
        #: A bare "<Name> :" line carries no text of its own: it is consumed into
        #: the attribution state, and the value it produced is the
        #: `attribution_marker` recorded on every occurrence that followed it.
        #: Accounting by that value is the same rule the metadata branches
        #: follow. Without it the ledger reported a correctly-understood line as
        #: a loss -- which would have driven a "fix" towards keeping copies of
        #: lines the parser had already read.
        marker_keys = {duplicate_key(o["attribution_marker"])
                       for o in sub["occurrences"] if o.get("attribution_marker")}

        unconsumed = 0
        for line in body:
            t = line.strip()
            k = duplicate_key(t)
            if any(k and (k in ok or ok in k) for ok in occ_keys):
                d = "OCCURRENCE"
            elif any(k and (k in ck or ck in k) for ck in comment_keys):
                d = "CONTEXT_COMMENT"
            # A pasted chat line is preserved with the third party's NAME
            # REMOVED, so the committed comment is deliberately not byte-equal to
            # the source line. Comparing the raw line alone reported five
            # correctly-preserved lines as lost. The redaction is applied to the
            # source line before the comparison, exactly as the ingest does.
            elif any(kr and (kr in ck or ck in kr)
                     for ck in comment_keys
                     for kr in [duplicate_key(I.redact_third_parties(t))]):
                d = "CONTEXT_COMMENT"
            elif any(k and k == mk for mk in marker_keys):
                d = "METADATA_CONSUMED"
            elif (I.ROLE_RE.match(t) or I.ROLE_NOSEP_RE.match(t)) and any(
                    n and n in I.normalise(t).lower() for n in examiner_lines):
                d = "EXAMINER_DECLARATION"
            elif _metadata_match(t):
                d = "METADATA_CONSUMED"
            else:
                d = "UNACCOUNTED"
                unaccounted.append({"blockIndex": bi, "line": t[:160]})
                unconsumed += 1
            counts[d] = counts.get(d, 0) + 1

        if not sub["occurrences"]:
            # A RECOGNISED submission that yielded nothing. It passed the
            # submission test so it is NOT an unparsed block, and before this it
            # contributed zero questions without saying so anywhere. The count of
            # body lines the parser could not consume says which case it is: zero
            # means a genuine metadata-only report, more than zero means the
            # parser read nothing while the candidate wrote something.
            zero_yield.append({
                "blockIndex": bi,
                "submissionId": sub["submission_id"],
                "bodyLines": len(body),
                "unconsumedBodyLines": unconsumed,
                "firstLine": body[0].strip()[:120] if body else "",
            })

    # ── duplicates: identified, linked, counted, kept ──────────────────────
    seen: dict[str, list[dict]] = {}
    for o in occurrences:
        seen.setdefault(duplicate_key(o["raw_question_text"]), []).append(o)
    groups = []
    for key, members in seen.items():
        if len(members) < 2 or not key:
            continue
        groups.append({
            "duplicateKey": key[:160],
            "firstOccurrenceId": members[0]["occurrence_id"],
            "occurrenceIds": [m["occurrence_id"] for m in members],
            "submissionIds": sorted({m["submission_id"] for m in members}),
            "spansSubmissions": len({m["submission_id"] for m in members}) > 1,
            "repeats": len(members) - 1,
            "rawForms": sorted({I.normalise(m["raw_question_text"])[:160]
                                for m in members}),
        })
    groups.sort(key=lambda g: g["firstOccurrenceId"])

    led = {
        "sourceFile": source_name,
        "meaningfulLines": meaningful,
        "dispositionCounts": {k: counts[k] for k in DISPOSITIONS if k in counts},
        "unaccounted": unaccounted,
        "unparsedBlocks": [s for s in skipped],
        "zeroYieldSubmissions": zero_yield,
        "submissions": len(subs),
        "occurrences": len(occurrences),
        "duplicateGroups": groups,
        "duplicateOccurrences": sum(g["repeats"] for g in groups),
        "clean": not unaccounted and not skipped and not zero_yield,
    }
    led["_occurrences"] = occurrences
    return led


def gate(led: dict) -> tuple[bool, str]:
    """May the ingest write records from this carrier?

    Refused when anything the carrier holds went unplaced. A repeat is NOT a
    refusal: duplicates are evidence, and treating them as loss would stop a
    perfectly good intake.
    """
    why = []
    if led["unaccounted"]:
        why.append(f"{len(led['unaccounted'])} line(s) reached no disposition: "
                   f"{[u['line'][:60] for u in led['unaccounted'][:3]]}")
    if led["unparsedBlocks"]:
        why.append(f"{len(led['unparsedBlocks'])} source block(s) yielded no "
                   f"submission: {[b['block_index'] for b in led['unparsedBlocks']]}")
    if led["zeroYieldSubmissions"]:
        why.append(f"{len(led['zeroYieldSubmissions'])} recognised submission(s) "
                   f"yielded zero occurrences: "
                   f"{[z['submissionId'] for z in led['zeroYieldSubmissions']]}")
    return (not why), "; ".join(why) or "every line is accounted for"


def public(led: dict) -> dict:
    return {k: v for k, v in led.items() if not k.startswith("_")}


def reconcile_registered() -> dict:
    """Every registered carrier, read-only, in registry order."""
    out = []
    for c in I.load_carriers():
        p = I.carrier_path(c)
        if not p.exists():
            out.append({"sourceFile": c["source_file"], "clean": False,
                        "error": "registered carrier absent from disk"})
            continue
        out.append(public(reconcile_text(p.read_text(encoding="utf-8"),
                                        c["source_file"])))
    return {
        "record_class": "CURRENT_INTAKE_RECONCILIATION_LEDGER",
        "generated_by": "tools/oral/intake_reconcile.py",
        "contract": "tools/oral/SKILL.md section 14",
        "carriers": out,
        "totals": {
            "carriers": len(out),
            "meaningfulLines": sum(c.get("meaningfulLines", 0) for c in out),
            "occurrences": sum(c.get("occurrences", 0) for c in out),
            "unaccountedLines": sum(len(c.get("unaccounted", [])) for c in out),
            "unparsedBlocks": sum(len(c.get("unparsedBlocks", [])) for c in out),
            "zeroYieldSubmissions": sum(
                len(c.get("zeroYieldSubmissions", [])) for c in out),
            "duplicateOccurrences": sum(
                c.get("duplicateOccurrences", 0) for c in out),
        },
        "clean": all(c.get("clean") for c in out),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="print the full ledger")
    ap.add_argument("--out", help="write the ledger to this path")
    a = ap.parse_args(argv)

    led = reconcile_registered()
    if a.json:
        print(json.dumps(led, indent=2, ensure_ascii=False))
    else:
        t = led["totals"]
        print(f"{t['carriers']} carrier(s), {t['meaningfulLines']} meaningful "
              f"line(s), {t['occurrences']} occurrence(s)")
        for c in led["carriers"]:
            print(f"  {'OK  ' if c.get('clean') else 'LOSS'} "
                  f"{c['sourceFile'][:52]:54} "
                  f"{c.get('occurrences', 0):4} occ  "
                  f"{c.get('duplicateOccurrences', 0):3} repeat(s)  "
                  f"{c.get('dispositionCounts', {})}")
        print(f"unaccounted lines: {t['unaccountedLines']} · "
              f"unparsed blocks: {t['unparsedBlocks']} · "
              f"zero-yield submissions: {t['zeroYieldSubmissions']} · "
              f"duplicate occurrences: {t['duplicateOccurrences']}")
    if a.out:
        Path(a.out).write_text(json.dumps(led, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
        print(f"ledger written to {a.out}")
    return 0 if led["clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
