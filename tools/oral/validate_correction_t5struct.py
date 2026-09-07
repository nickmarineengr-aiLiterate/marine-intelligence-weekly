#!/usr/bin/env python3
"""Content gate for CORR-T5-DDCASCADE-20260906 -- the deep-dive suffix cascade.

WHY A DIGEST PIN IS NOT ENOUGH HERE
-----------------------------------
The record pins 44 cards, and a pin is perfectly happy with wrong text: it pins
whatever it is given. What this correction actually claims is two things a pin
cannot express:

  1. the cascade is GONE -- no `dd-block` renders a following section as raw
     markdown any more; and
  2. NOTHING WAS LOST -- every typed block that existed before still exists,
     still carries its own body, and the propositions the cascade duplicated
     are still on the card exactly once.

Claim 2 is the one that matters. A "repair" that deleted the tail AND the block
that owned it would satisfy every digest pin in the toolchain and would silently
strip content from 38 cards. So this gate re-derives the losslessness proof
against the live corpus rather than trusting the applier's own report.

WHY THE COUNTS ARE RE-DERIVED AND NOT READ
------------------------------------------
`invariants.cascaded_blocks_repaired` says 146. A gate that read that number
back out of the record and printed it would assert nothing. The number is
recomputed from the baseline tree and the live tree and compared to the record,
so a record that overstates what it did fails here.

WHY TWO CARDS RESOLVE AS SUPERSEDED AND THAT IS CORRECT
------------------------------------------------------
QB1_F#q10 and QB2_H#q2 were touched by this family and then again by
CORR-T5-REACH / CORR-T5-HYDRANT. This record pins the state IT produced, and the
later records declare descent from it. So the digest check must go through
`resolve_authorised_card_state`, which accepts `SUPERSEDED_OK` -- comparing the
pin directly to the live card would report a correct chain as tampering.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_bytes import read_text                                  # noqa: E402
from validate_batch_h_series import card_digests                  # noqa: E402
from oral_supersession import resolve_authorised_card_state       # noqa: E402
from analyse_ddcascade import (                                   # noqa: E402
    analyse, DD_BLOCK, STRAY, norm, card_spans, split_stray)
#: The corpus enumeration is IMPORTED, never re-globbed locally. Every
#: "corpus-wide" claim in this repository must resolve through one function, or
#: they drift and a scope defect hides in the difference - which is exactly
#: what happened in Pass 1.
from census_known_defect_families import corpus_files, rel_of  # noqa: E402

CORRECTION_ID = "CORR-T5-DDCASCADE-20260906"
MANIFEST = HERE / "correction_corr_t5_ddcascade_20260906_manifest.json"
QB_ROOT = REPO / "meoclass1"
INDEX = REPO / "meoclass1/qb_content_index.json"
TRAPS = REPO / "meoclass1/known_traps.md"

EMPTY_DETAILS = re.compile(r'<details class="deep-dive"><summary>[^<]*</summary>'
                           r'</details>')

#: Two or more consecutive `* ` lines - a markdown bullet RUN, which a lone
#: footnote marker can never be.
ORPHAN_RUN = re.compile(r"(?m)^\*\s+\S[^\n]*\n\*\s+\S")

#: Pass 1 removed orphan bullet markers as well as truncating the cascade, so
#: a baseline body legitimately differs from its live body by exactly that
#: marker. Normalise it out of BOTH sides before comparing, or the body check
#: reports six declared edits as content loss.
ORPHAN_MARKER = re.compile(r'(["”’])\*\s+(?=<strong>)|(</em>|</strong>|:)\s*\*\s+(?=<strong>)')

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-52s %s" % ("PASS" if ok else "FAIL", check, detail))


def baseline_text(commit: str, rel: str):
    out = subprocess.run(["git", "show", "%s:%s" % (commit, rel)],
                         cwd=str(REPO), capture_output=True)
    return out.stdout.decode("utf-8") if out.returncode == 0 else None


def main() -> int:
    man = json.loads(read_text(MANIFEST))
    report("manifest_is_this_correction",
           man.get("correction_id") == CORRECTION_ID, man.get("correction_id"))
    report("status_authorised", man.get("status") == "AUTHORISED",
           man.get("status"))

    cards = man["cards"]
    inv = man["invariants"]

    # ---- 1. the cascade is gone, corpus-wide -----------------------------
    live_cascade = []
    for p in corpus_files():
        live_cascade.extend(analyse(p))
    report("no_cascaded_deep_dive_block_remains", not live_cascade,
           "%d remaining" % len(live_cascade))

    # ---- 2. no empty deep-dive promise remains ---------------------------
    empty = [(rel_of(p), len(EMPTY_DETAILS.findall(read_text(p))))
             for p in corpus_files()]
    empty = [(n, c) for n, c in empty if c]
    report("no_empty_deep_dive_promise_remains", not empty, str(empty or "none"))

    # ---- 3. no orphaned markdown bullet remains in the repaired files -----
    touched = sorted({c["file"] for c in cards})
    # Corpus-wide, not just the pinned files: QB2_H is edited by this family
    # and pinned by a sibling, so a check scoped to `cards` would stop seeing it.
    # BOTH orphan forms. Pass 1 scanned only bullets opening with a <strong>,
    # so three raw bullets in QB9_E whose text starts with a plain word were
    # neither repaired nor declared. A bullet is a bullet.
    #
    # A RUN of two or more, though - never a single line. `miw-notes-mgmt-p6`
    # carries a lone `* Day-counts are ...` that is the FOOTNOTE paired with
    # the `3 days*` / `7 days*` / `~30 days*` markers above it. It is content,
    # and a scan that cannot tell a footnote from a bullet would have deleted
    # the note explaining that those day-counts are not MLC statutory text.
    orphan = [(rel_of(p), len(ORPHAN_RUN.findall(read_text(p))))
              for p in corpus_files()]
    orphan = [(f, n) for f, n in orphan if n and f != "QB9_D.html"]
    report("no_orphaned_markdown_bullet_in_repaired_files", not orphan,
           "%s (QB9_D excluded: its bullet sits inside the Pass-2 blockquote "
           "block and half-repairing that would hide it)" % (orphan or "none"))

    # ---- 4. NOTHING WAS LOST --------------------------------------------
    # For every card this record touched, the set of typed dd-block classes on
    # the live page must equal the set on the baseline page, and each block
    # must still carry a non-empty body. A repair that removed a block rather
    # than its duplicated tail fails here and passes every digest check.
    base_commit = man["baseline_commit"]
    lost, emptied = [], []
    for fname in touched:
        base = baseline_text(base_commit, "meoclass1/%s" % fname)
        if base is None:
            report("baseline_readable_%s" % fname, False, base_commit)
            continue
        live = read_text(QB_ROOT / fname)
        # PER CARD, and comparing BODIES. The Pass-1 version compared
        # (class, label) pairs file-wide: DD_BLOCK group 3 is the body and it
        # was never read, so a repair that replaced all 146 bodies with one
        # character would have passed - and a block migrating between cards in
        # the same file was invisible. What this correction actually claims is
        # that each block kept ITS OWN body, which is the surviving head of
        # the baseline body up to the first stray marker.
        for anchor, bs, be in card_spans(base):
            live_span = [x for x in card_spans(live) if x[0] == anchor]
            if not live_span:
                lost.append("%s#%s MISSING" % (fname, anchor))
                continue
            _, ls, le = live_span[0]
            base_map = {(m.group(1), norm(m.group(2))): split_stray(m.group(3))[0]
                        for m in DD_BLOCK.finditer(base[bs:be])}
            live_map = {(m.group(1), norm(m.group(2))): m.group(3)
                        for m in DD_BLOCK.finditer(live[ls:le])}
            if set(base_map) != set(live_map):
                lost.append("%s#%s block set" % (fname, anchor))
                continue
            for key, expected in base_map.items():
                a = norm(ORPHAN_MARKER.sub(lambda m: (m.group(1) or m.group(2))
                                           + " ", expected))
                b = norm(ORPHAN_MARKER.sub(lambda m: (m.group(1) or m.group(2))
                                           + " ", live_map[key]))
                if a != b:
                    lost.append("%s#%s %s body" % (fname, anchor, key[0]))
        for m in DD_BLOCK.finditer(live):
            body = re.sub(r"<[^>]+>", "", m.group(3)).strip()
            if not body:
                emptied.append("%s/%s" % (fname, m.group(1)))
    # A LATER authorised correction may legitimately rewrite a typed block -
    # CORR-D01S02-ESP-20260907 rewrote the dd-trap answers in QB1_F#q16 and
    # QB1_G#q30, because those trap answers were themselves wrong. This check
    # exists to prove the deep-dive CASCADE lost nothing, not to freeze every
    # block for all time, so a loss is excused where a later record declares
    # that card and its supersession chain resolves. Everything else still
    # fails: an undeclared change is exactly what this check is for.
    _later = set()
    for path in sorted(HERE.glob("correction_*_manifest.json")):
        if path.name == MANIFEST.name:
            continue
        try:
            m2 = json.loads(read_text(path))
        except Exception:                                   # noqa: BLE001
            continue
        for c2 in m2.get("cards", []):
            if c2.get("supersedes"):
                _later.add("%s#%s" % (c2.get("file"), c2.get("anchor")))
    lost = [x for x in lost
            if " ".join(x.split(" ")[:1]) not in _later]
    report("every_typed_block_survived_the_repair", not lost,
           "files with a changed block set: %s" % (lost or "none"))
    report("no_block_was_emptied_by_the_repair", not emptied,
           str(emptied[:5] or "none"))

    # ---- 5. the counts are RE-DERIVED, never read back -------------------
    # Derived CORPUS-WIDE from the baseline tree, not from the pinned files.
    # Scoping this to `cards` made the empty-promise count read 5 against a
    # declared 6, because QB2_H is edited by this family and pinned by a
    # sibling - the same blind spot as the orphan-bullet scan above.
    derived_blocks = derived_bytes = derived_empty = 0
    for p_live in corpus_files():
        base = baseline_text(base_commit, "meoclass1/%s" % rel_of(p_live))
        if base is None:
            continue
        derived_empty += len(EMPTY_DETAILS.findall(base))
        for m in DD_BLOCK.finditer(base):
            first = STRAY.search(m.group(3))
            if first:
                derived_blocks += 1
                derived_bytes += len(m.group(3)) - len(m.group(3)[:first.start()])
    report("declared_block_count_matches_baseline",
           derived_blocks == inv["cascaded_blocks_repaired"],
           "derived %d, declared %d" % (derived_blocks,
                                        inv["cascaded_blocks_repaired"]))
    report("declared_empty_promise_count_matches_baseline",
           derived_empty == inv["empty_deep_dive_promises_removed"],
           "derived %d, declared %d"
           % (derived_empty, inv["empty_deep_dive_promises_removed"]))
    # RE-DERIVED, not read back. The Pass-1 version computed `derived_bytes`
    # in the loop above and then never used it, asserting only that the
    # manifest's own number was greater than 50,000 - a record could have
    # claimed any large figure.
    report("declared_duplicated_bytes_matches_baseline",
           derived_bytes == inv["duplicated_bytes_removed"],
           "derived %d, declared %d" % (derived_bytes,
                                        inv["duplicated_bytes_removed"]))
    report("no_block_was_refused_as_unproven",
           inv["blocks_refused_as_unproven"] == 0,
           str(inv["blocks_refused_as_unproven"]))

    # ---- 6. digests, through the supersession resolver -------------------
    digest_cache: dict[str, dict] = {}
    bad = []
    for c in cards:
        d = digest_cache.setdefault(c["file"],
                                    card_digests(read_text(QB_ROOT / c["file"])))
        res = resolve_authorised_card_state(
            manifest=MANIFEST.name, action_id=c["correction_action_id"],
            file=c["file"], anchor=c["anchor"],
            pinned_post_digest=c["post_edit_digest"],
            live_digest=d.get(c["anchor"]))
        if not res.ok:
            bad.append("%s#%s:%s" % (c["file"], c["anchor"], res.status))
    report("every_pinned_state_is_live_or_a_proven_ancestor", not bad,
           "%d card(s), problems: %s" % (len(cards), bad or "none"))

    # ---- 7. the sibling-pinned card is DECLARED, not forgotten -----------
    # QB2_H#q2 was edited by this family and is pinned by the hydrant record,
    # because all three families landed in one commit and no commit holds an
    # intermediate state. An undeclared overlap is indistinguishable from an
    # unauthorised edit, so the declaration is asserted here - and the empty-
    # promise check above already covers QB2_H substantively, corpus-wide.
    overlap = man["propagation"].get(
        "cards_edited_here_but_pinned_by_a_sibling_record", "")
    report("sibling_pinned_card_is_declared",
           "QB2_H.html#q2" in overlap
           and "CORR-T5-HYDRANT-20260906" in overlap,
           "the overlap is recorded as structure, not left implicit")
    report("sibling_pinned_card_is_not_also_pinned_here",
           not [c for c in cards if c["file"] == "QB2_H.html"],
           "no card is pinned by two records")

    # ---- 8. corpus invariants -------------------------------------------
    idx = json.loads(read_text(INDEX))
    report("canonical_questions_unchanged",
           idx["total_questions"] == inv["canonical_questions_after"],
           str(idx["total_questions"]))
    report("question_bearing_files_unchanged",
           idx["total_files"] == inv["question_bearing_files"],
           str(idx["total_files"]))
    report("no_cards_added", inv["new_cards"] == 0, str(inv["new_cards"]))
    report("declared_corrected_card_count_matches_records",
           inv["corrected_cards"] == len(cards), str(inv["corrected_cards"]))

    # ---- 9. governance ---------------------------------------------------
    # BOTH directions. "every declared artefact exists" is one-directional and
    # passes happily when a declaration is DELETED - mutation J escaped on
    # exactly that. The record's evidence chain names four files; all four must
    # be declared AND present.
    declared = {a["path"] for a in man["artefacts"]}
    REQUIRED = {"meoclass1/known_traps.md",
                "tools/oral/analyse_ddcascade.py",
                "tools/oral/apply_ddcascade_repair.py",
                "tools/oral/census_known_defect_families.py"}
    report("declared_artefacts_exist",
           all((REPO / a["path"]).is_file() for a in man["artefacts"])
           and not (REQUIRED - declared),
           "%d declared, missing declaration: %s"
           % (len(declared), sorted(REQUIRED - declared) or "none"))
    traps = read_text(TRAPS)
    # Needles are chosen to be UNIQUE to the lesson. "position" alone survived
    # mutation K because entry 90 uses the word twice; the imperative sentence
    # that carries the rule does not.
    for n, needles in ((90, ("suffix cascade", "byte-identical",
                             "never by position",
                             "never re-implement it beside its own proof")),
                       (91, ("deletion", "idempotency")),
                       (92, ("own output", "PREDECESSOR_PIN_ALTERED"))):
        m = re.search(r"### %d\..*?(?=\n### |\Z)" % n, traps, re.S)
        body = m.group(0) if m else ""
        report("known_traps_entry_%d_carries_the_lesson" % n,
               bool(body) and all(x in body for x in needles),
               "entry %d" % n)

    # ---- 10. the Pass-2 backlog is DECLARED, not dropped -----------------
    # A record that closed one residue generation and stayed silent about the
    # next would read as "residue: done". The successor family has to be named
    # in the record itself or the next session will believe the field is clear.
    prop = man["propagation"].get("residue_remaining", "")
    report("remaining_residue_generation_is_declared",
           all(x in prop for x in ("QB9_D", "QB5_C_B", "blockquote", "fence")),
           "Pass-2 backlog named in the record")

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: " + ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
