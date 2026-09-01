"""Validate the H-series August 2026 production batches -- H1 .. H4.

WHY THIS FILE EXISTS
--------------------
`H4-RES-01`, the material residue H4 registered for H5:

    NO H-SERIES BATCH HAS A VALIDATOR, A MUTATOR OR A GATE.  tools/oral/ holds
    validate_batch_{a..d,e1..e6,f1,f1b,g1..g4} and nothing for H1, H2, H3A,
    H3A-ORB, H3B-1, H3B-2 or H4.  The seven H manifests' digest pins are
    asserted by nothing in the toolchain.

Seven manifests, nineteen cards and one held limb were carrying pins that no
code read.  A pin nobody checks is not weaker than no pin -- it is worse, because
the record *looks* governed.  This closes that.

ONE VALIDATOR FOR THE WHOLE SERIES, NOT SEVEN
---------------------------------------------
The seven H manifests share one schema exactly: full `sha256` digests over the
balanced card block, `cards[]` of {file, anchor, pre_edit_digest,
post_edit_digest, action_id, source_occurrence_ids}.  Seven near-identical
files is how ten batch validators each grew a private copy of the sibling glob
and then disagreed about it (SKILL section 8).  So this iterates the series the
way `validate_corrections.py` iterates every correction record: **adding H5
adds a manifest, not a gate.**

WHAT IS EXPECTED, AND WHY IT IS NOT A LITERAL HERE
--------------------------------------------------
"A missing manifest must fail" needs an expectation, and a private list here
would be a *second* registry that could drift from the real one.  The
expectation is read from `test_oral_release_infra.EXPECTED_BATCH_MANIFESTS` --
the enumerated list the repository already treats as the manifest registry, and
the same one line a new batch already has to edit (SKILL section 7.5b).  One
registry, two readers.

DIGEST PINS RESOLVE THROUGH THE SUPERSESSION CHAIN
--------------------------------------------------
`oral_supersession.resolve_authorised_card_state` is folded into the digest
check rather than added beside it, exactly as every generation-2 validator does
(SKILL section 7.5).  A later authorised batch may legitimately land on an
H-series card; it must then DECLARE that its state descends from the pin.  An
unmanifested edit still fails.

  PYTHONIOENCODING=utf-8 python tools/oral/validate_batch_h_series.py

Exit 0 if every check passes, 1 otherwise.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
MEO = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio          # noqa: E402
from oral_manifest import (                        # noqa: E402
    audit_manifest, authorisation_manifest_paths,
)
from oral_supersession import (                    # noqa: E402
    load_card_records, resolve_authorised_card_state,
)

enable_utf8_stdio()

CARD_OPEN = re.compile(r'<div class="q-card"[^>]*>')

results: list[tuple[str, bool, str]] = []


def check(name: str, ok, detail: str = "") -> None:
    results.append((name, bool(ok), detail))


# --------------------------------------------------------------------- cards
def _balanced_end(text: str, start: int) -> int:
    """End index of the div opened at `start`, by balanced <div> nesting.

    The same walk every batch validator uses.  Counting tags instead would be
    blind to the defect H5 repaired in QB1_F and QB5_C_B, where the file was
    perfectly balanced and three cards had still fallen out of #q-feed.
    """
    depth, i = 0, start
    tag = re.compile(r"<(/?)div\b", re.I)
    while True:
        m = tag.search(text, i)
        if not m:
            return len(text)
        depth += -1 if m.group(1) else 1
        i = m.end()
        if depth == 0:
            close = text.find(">", i)
            return (close + 1) if close >= 0 else len(text)


def card_digests(text: str) -> dict:
    """anchor -> sha256 over the card's balanced block, LF-normalised.

    LF-normalised because .gitattributes pins these pages to LF in the object
    store while a freshly written working copy may hold CRLF; a raw-byte digest
    would then report every card on such a page as changed.
    """
    text = text.replace("\r\n", "\n")
    out = {}
    for m in CARD_OPEN.finditer(text):
        a = re.search(r'\bid="([^"]+)"', m.group(0))
        if a:
            out[a.group(1)] = hashlib.sha256(
                text[m.start():_balanced_end(text, m.start())].encode("utf-8")
            ).hexdigest()
    return out


def git_show(ref: str, rel: str):
    out = subprocess.run(["git", "show", "%s:%s" % (ref, rel)],
                         cwd=str(REPO), capture_output=True)
    return out.stdout.decode("utf-8", "replace") if out.returncode == 0 else None


# ---------------------------------------------------------------- expectation
def expected_h_manifests() -> list[str] | None:
    """The H-series names the manifest registry says must exist.

    Read from the registry rather than restated, so this validator cannot come
    to disagree with `test_oral_release_infra` about what the series is.

    The registry is read by PARSING that module's source, never by importing
    it: `test_oral_release_infra` runs its whole suite at import time, so an
    import here would execute ninety-nine unrelated checks inside this
    validator and print their output as if it were ours.

    Returns None if the registry cannot be read -- reported as a FAILURE
    below, never as "nothing is expected".
    """
    import ast
    src = HERE / "test_oral_release_infra.py"
    try:
        tree = ast.parse(src.read_text(encoding="utf-8"))
    except Exception:
        return None
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if "EXPECTED_BATCH_MANIFESTS" not in names:
            continue
        try:
            value = ast.literal_eval(node.value)
        except Exception:
            return None
        return sorted(n for n in value if str(n).startswith("batch_h"))
    return None


def main() -> int:
    results.clear()

    expected = expected_h_manifests()
    check("h_registry_readable", expected is not None,
          "EXPECTED_BATCH_MANIFESTS could not be read from "
          "test_oral_release_infra")
    if expected is None:
        # Fail closed.  An unreadable registry is not permission to check
        # nothing -- that is how a guard silently expires.
        report()
        return 1

    # Discovery goes through the SHARED authorisation surface, never a private
    # glob: ten batch validators each grew their own copy of that glob, and
    # widening it in ten places is how the two record families drifted apart.
    on_disk = sorted(p.name for p in authorisation_manifest_paths(HERE)
                     if p.name.startswith("batch_h"))
    check("h_manifests_all_present", set(expected) <= set(on_disk),
          "missing=%s" % (sorted(set(expected) - set(on_disk)) or "none"))
    check("h_manifests_none_undeclared", set(on_disk) <= set(expected),
          "undeclared=%s" % (sorted(set(on_disk) - set(expected)) or "none"))

    records = list(load_card_records(HERE))
    ownership: dict[tuple, list[str]] = {}
    live_cache: dict[str, dict] = {}
    seen = 0

    for name in expected:
        path = HERE / name
        if not path.is_file():
            check("%s:present" % name, False, "absent")
            continue

        # 1. schema -- the bare auditor, so a phantom field or an unclassified
        #    one fails here rather than at ship time.
        findings = audit_manifest(path)
        bad = [f for f in findings if not f.ok]
        check("%s:schema_audit" % name, not bad,
              "; ".join("%s: %s" % (f.check, f.detail) for f in bad[:4]) or "ok")

        manifest = json.loads(path.read_text(encoding="utf-8"))
        cards = manifest.get("cards") or []
        check("%s:declares_cards" % name, bool(cards), "cards=%d" % len(cards))

        baseline = manifest.get("baseline_commit")
        touched_files = sorted({c.get("file") for c in cards if c.get("file")})

        for card in cards:
            seen += 1
            aid = card.get("action_id") or "?"
            fname = card.get("file") or ""
            anchor = card.get("anchor") or ""
            # No spaces in a check name: the runner and every mutation harness
            # read failing names with ^FAIL\s+(\S+), so a space silently
            # truncates the name and every "catch" degrades to a prefix match.
            tag = "%s/%s:" % (name.replace("_manifest.json", ""), aid)

            # 2. the declared path is a real question-bearing page
            page = MEO / fname
            check("%scard_path_exists" % tag, page.is_file(),
                  "file=%r" % fname)
            if not page.is_file():
                continue

            if fname not in live_cache:
                live_cache[fname] = card_digests(
                    page.read_text(encoding="utf-8"))
            live = live_cache[fname]

            # 3. the declared anchor is a real card on that page
            check("%scard_anchor_exists" % tag, anchor in live,
                  "anchor=%r on %s" % (anchor, fname))
            if anchor not in live:
                continue

            # 4. an inert record pins nothing
            check("%scard_digests_differ" % tag,
                  card.get("pre_edit_digest") != card.get("post_edit_digest"),
                  "pre == post")

            # 4b. the PRE-edit claim must be TRUE, not merely different.
            #     Mutation B corrupted it and nothing failed: `pre != post`
            #     alone lets a manifest misdescribe where the card started,
            #     and a supersession chain is built on exactly that value
            #     (its contract is pre == the predecessor's post).
            base = manifest.get("baseline_commit")
            before = git_show(base, "meoclass1/%s" % fname) if base else None
            if before is None:
                check("%spre_edit_state_is_as_declared" % tag, False,
                      "baseline %r unavailable for %s" % (base, fname))
            else:
                was = card_digests(before).get(anchor)
                declared = card.get("pre_edit_digest") or ""
                # BOTH directions, or the check is vacuous for whichever kind
                # of card it does not cover -- and nineteen of these twenty-
                # three cards are NEW_CARD, so a created-card exemption would
                # have exempted almost the whole series:
                #
                #   existed at baseline -> the declared pre MUST equal it
                #   did not exist       -> the manifest MUST declare no pre,
                #                          because a pre-edit state for a card
                #                          that did not exist is a fabricated
                #                          baseline, and a supersession chain
                #                          would later be built on it.
                if was is None:
                    ok, detail = (not declared,
                                  "card absent at baseline but pre=%s declared"
                                  % (declared[:16] or "<none>"))
                else:
                    ok, detail = (was == declared,
                                  "baseline=%s declared=%s"
                                  % (was[:16], declared[:16] or "<none>"))
                check("%spre_edit_state_is_as_declared" % tag, ok, detail)

            # 5. THE PIN.  Folded through the supersession resolver so a later
            #    AUTHORISED state descends from it, and an unmanifested edit
            #    does not.  No separate check: the meaning is stronger, the
            #    count is unchanged.
            res = resolve_authorised_card_state(
                manifest=name, action_id=aid, file=fname, anchor=anchor,
                pinned_post_digest=card.get("post_edit_digest"),
                live_digest=live[anchor], records=records)
            check("%smanifest_digest_matches" % tag, res.ok,
                  "%s %s" % (getattr(res, "status", ""), getattr(res, "detail", "")))

            # 6. one primary owner per card across the whole series
            ownership.setdefault((fname, anchor), []).append(tag)

        # 7. no card changed on a touched page that the manifest does not
        #    declare.  This is what catches an EXTRA card smuggled into a page
        #    the batch legitimately edited -- a digest pin alone cannot, because
        #    it only ever looks at the cards it names.
        if baseline:
            declared = {(c.get("file"), c.get("anchor")) for c in cards}
            undeclared = []
            for fname in touched_files:
                before = git_show(baseline, "meoclass1/%s" % fname)
                if before is None:
                    undeclared.append("%s: baseline unavailable" % fname)
                    continue
                old = card_digests(before)
                new = live_cache.get(fname) or card_digests(
                    (MEO / fname).read_text(encoding="utf-8"))
                for anchor, digest in new.items():
                    if old.get(anchor) == digest:
                        continue
                    if (fname, anchor) in declared:
                        continue
                    if authorised_elsewhere(fname, anchor, name, records):
                        continue
                    undeclared.append("%s#%s" % (fname, anchor))
            check("%s:only_authorised_cards_changed" % name, not undeclared,
                  "undeclared=%s" % (undeclared[:6] or "none"))
        else:
            check("%s:only_authorised_cards_changed" % name, False,
                  "no baseline_commit to compare against")

    dupes = {k: v for k, v in ownership.items() if len(v) > 1}
    check("h_series_no_overlapping_primary_ownership", not dupes,
          "; ".join("%s#%s claimed by %s" % (f, a, v)
                    for (f, a), v in list(dupes.items())[:4]) or "none")
    check("h_series_cards_checked", seen > 0, "cards=%d" % seen)

    return report()


def authorised_elsewhere(fname, anchor, own_manifest, records) -> bool:
    """Is this card's change authorised by some OTHER governed record?

    A card an H batch touched may legitimately be edited later by a correction
    or a subsequent batch.  Anchor-level delegation answers 'was it allowed';
    the digest pin above answers 'is it still what was authorised'.  Both are
    required, and neither subsumes the other (SKILL section 8.2).
    """
    others = {p.name for p in
              authorisation_manifest_paths(HERE, exclude=HERE / own_manifest)}
    for rec in records:
        if rec.manifest not in others:
            continue
        if (rec.file, rec.anchor) == (fname, anchor):
            return True
    return False


def report() -> int:
    failed = [r for r in results if not r[1]]
    for name, ok, detail in results:
        if not ok:
            print("FAIL %-58s %s" % (name, detail))
    print()
    print("batch H-series validator -- %d checks, %d FAIL"
          % (len(results), len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
