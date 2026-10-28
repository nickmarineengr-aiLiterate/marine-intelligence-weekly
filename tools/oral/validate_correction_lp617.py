#!/usr/bin/env python3
"""Content gate for CORR-LP617-SEWAGE-SLUDGE-20261028 - sewage sludge left Annex 1.

The proposition, in four lines:
  1. Sewage sludge is NO LONGER on the 1996 Protocol's Annex 1 list: Resolution
     LP.6(17), adopted 7 October 2022, deleted it; in force generally on
     15 January 2023.
  2. No new dumping permits; an existing permit runs to expiry, not later than
     31 May 2027.
  3. It binds Contracting Parties to the 1996 Protocol - not a State party only
     to the 1972 Convention - so it is never taught as a worldwide ban.
  4. It is dumping law: MARPOL Annex IV (sewage discharge) and Annex VI reg 16
     (burning the ship's own sewage sludge) are untouched.

Shaped after validate_correction_nosdcp.py, the same page and the same twin:

  * PROPOSITION-SCOPED, never a banned string. The corrected card has to say
    "sewage sludge" in order to say it was removed, so the check is that every
    sentence naming it on a dumping subject carries the removal, not that the
    phrase is absent (SKILL.md 8.2a rule 2).
  * CLOSED-WORLD on the dates. Every entry-into-force claim on the card must
    give 15 January 2023 and every permit cut-off must give 31 May 2027, so a
    wrong rendering nobody has thought of fails on the day it is written.
  * SITE-SCOPED on the three limbs that shipped the defect - reverse-list
    paragraph, 60-second answer, CE Oral Tip - in BOTH the gated page and its
    SQ twin, and the twin must stay byte-identical.
  * CORPUS-WIDE for re-infection, with the two sites this record logs as open
    follow-ups (trap 141 A and B) TOLERATED, not required: correcting them under
    their own record must not turn this gate red, and a third site must.
  * OVER-CORRECTION guarded: the MARPOL Annex VI sewage-sludge text on QB3_C is
    correct and must survive a blanket substitution.
  * PROVENANCE EXCLUDED. The v1.1 stamp records what moved, so teaching checks
    strip every q-footer first; the stamp is then checked on its own.
  * NO digest pin: validate_corrections.py owns the pins.
"""
from __future__ import annotations

import html as htmllib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio, read_text  # noqa: E402
from validate_batch_b import card_digests  # noqa: E402

enable_utf8_stdio()

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-56s %s" % ("PASS" if ok else "FAIL", check, detail))


GATED = QB / "QB1_A.html"
TWIN = REPO / "SQ" / "QB1_A.html"
CARD = "q13"
MANIFEST = HERE / "correction_corr_lp617_sewage_sludge_20261028_manifest.json"
GOV = HERE / "qb_content_index_governed.json"
IDX = QB / "qb_content_index.json"
TRAPS = QB / "known_traps.md"
REGISTRY = REPO / "docs" / "sources" / "MIW_SOURCE_REGISTRY.json"
CORR_DATE = "2026-10-28"
SHIPPED_WRONG = "on the permitted list under 1996 Protocol"

#: Logged by trap 141 as open follow-ups A and B, to be corrected under their
#: own record. Tolerated so that record can land without editing this gate;
#: never required, so fixing them cannot turn this gate red.
KNOWN_OPEN = {"QB9_A.html": "Follow-up A",
              "oralnotes/simon-notes-p8.html": "Follow-up B"}

SLUDGE = re.compile(r"sewage\s+sludge", re.I)
#: A sentence that names sewage sludge on a DUMPING subject must say it left.
REMOVED = re.compile(r"no longer|removed|deleted|\bno new\b|not later than|"
                     r"not beyond|at the latest|LP\.6\(17\)", re.I)
#: Sewage sludge in a MARPOL Annex VI sentence is a different regime and correct.
ANNEX_VI = re.compile(r"Annex VI|reg(?:ulation|\.)?\s*16|incinerat|\bburn|boiler|"
                      r"power plant|generated (?:on board|during)", re.I)
DUMPING = re.compile(r"London|Protocol|reverse list|permitted|Annex 1|dump", re.I)
WORLDWIDE = re.compile(r"worldwide|world-wide|global(?:ly)?|all (?:IMO )?(?:Member )?States|"
                       r"every (?:State|country|flag)|all (?:countries|flag States|nations)|"
                       r"banned everywhere|universal|every (?:coastal )?State", re.I)
CLAIM_DATE = re.compile(
    r"(?:in force|into force|effective|took effect)[^.;<]{0,40}?"
    r"(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4})",
    re.I)
#: The same claim in reverse order: "15 January 2024 is when it entered into
#: force". An adoption date followed by its own entry-into-force clause
#: ("Adopted 7 Oct 2022, in force 15 Jan 2023") is not this claim.
CLAIM_DATE_REV = re.compile(
    r"(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4})"
    r"[^.;<]{0,30}?(?:in force|into force)", re.I)
ADOPTED_BEFORE = re.compile(r"adopt\w*(?:\s+on)?\s*$", re.I)
#: A date in a permit sentence that names its own event is not a cut-off.
EVENT_BEFORE = re.compile(r"(?:in force|into force|adopt\w*|entry)[^.;()]{0,25}$", re.I)
#: A permit sentence with one of these verbs is ABOUT the cut-off, so every
#: date in it must be the cut-off even where "entry into force" sits in front
#: of it ("existing permits lapse on entry into force, 15 January 2023").
ENDING = re.compile(r"\b(?:end\w*|laps\w*|expir\w*|until|ceas\w*|terminat\w*|kept|"
                    r"maintain\w*|run\w*|continu\w*|valid)\b", re.I)
PERMIT = re.compile(r"permit|authori[sz]ation|licen[cs]e", re.I)
#: The amendment binds 1996 Protocol Parties; a sentence saying it binds or
#: applies to Parties to the 1972 Convention, without a negation, widens it.
SCOPE_1972 = re.compile(r"(?:bind|bound|appl)\w*[^.;]{0,60}1972 Convention|"
                        r"1972 Convention[^.;]{0,40}(?:bound|bind|appl)\w*", re.I)
EIF_OK = re.compile(r"15 Jan(?:uary)? 2023", re.I)
ANY_DATE = re.compile(r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"
                      r"[a-z]*\s+\d{4}", re.I)
CUTOFF_OK = re.compile(r"31 May 2027")


# --------------------------------------------------------------------------
# helpers (the same extraction validate_correction_nosdcp.py uses)
# --------------------------------------------------------------------------

def card_html(page: str, anchor: str) -> str | None:
    at = page.find('<div class="q-card" id="%s"' % anchor)
    if at < 0:
        return None
    depth, pos = 0, at
    tok = re.compile(r"<div\b|</div>")
    while True:
        m = tok.search(page, pos)
        if not m:
            return None
        depth += -1 if m.group(0) == "</div>" else 1
        pos = m.end()
        if depth == 0:
            return page[at:pos]


def strip_footers(markup: str) -> str:
    out, pos = [], 0
    for m in re.finditer(r'<div class="q-footer"', markup):
        if m.start() < pos:
            continue
        out.append(markup[pos:m.start()])
        depth, end = 0, m.start()
        for tok in re.finditer(r"<div\b|</div>", markup[m.start():]):
            depth += -1 if tok.group(0) == "</div>" else 1
            end = m.start() + tok.end()
            if depth == 0:
                break
        pos = end
    out.append(markup[pos:])
    return "".join(out)


def footer(markup: str) -> str:
    at = markup.find('<span class="q-version"')
    return flatten(markup[at:]) if at >= 0 else ""


def flatten(markup: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", markup)))


def sentences(flat: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.;!?])\s+|\s(?=Q:\s)", flat) if s.strip()]


#: A quoted examiner question asks rather than asserts; its answer is checked
#: on its own (ce_tip_cross_question_answered_no).
QUOTED_QUESTION = re.compile(r"[“\"][^”\"]{0,200}\?[”\"]")


def sludge_still_permitted(flat: str) -> list[str]:
    """Sentences naming sewage sludge without its removal or an Annex VI subject."""
    bad = []
    for s in sentences(flat):
        s = QUOTED_QUESTION.sub(" ", s)
        if not SLUDGE.search(s) or s.rstrip().endswith("?"):
            continue
        if ANNEX_VI.search(s) or REMOVED.search(s):
            continue
        bad.append(s.strip()[:110])
    return bad


def dumping_sentences(flat: str) -> list[str]:
    """Sentences naming sewage sludge whose subject is dumping.

    The subject is read from a window reaching back before the sentence,
    because the oral notes list Annex 1 as "Dredged material; sewage sludge;
    ..." and the semicolons cut the heading off the item.
    """
    out = []
    for m in re.finditer(r"[^.;!?]*[.;!?]?", flat):
        s = m.group(0)
        if s.strip() and SLUDGE.search(s) and DUMPING.search(
                flat[max(0, m.start() - 250):m.end()]):
            out.append(s)
    return out


def section(flat: str, start: str, stop: str) -> str:
    m = re.search(re.escape(start) + r"(.*?)" + stop, flat)
    return m.group(1) if m else ""


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

def main() -> int:
    pages = {"gated": read_text(GATED), "twin": read_text(TWIN)}
    cards = {side: card_html(page, CARD) for side, page in pages.items()}
    missing = [side for side, c in cards.items() if c is None]
    report("target_card_present", not missing, "missing=%s" % (missing or "none"))
    if missing:
        return finish()

    g, t = card_digests(pages["gated"]), card_digests(pages["twin"])
    report("twin_identical_to_gated", g.get(CARD) == t.get(CARD),
           "q13 %s" % ("==" if g.get(CARD) == t.get(CARD) else "!="))

    for side, c in cards.items():
        teach = flatten(strip_footers(c))
        n = len(SLUDGE.findall(teach))
        report("non_vacuous_sludge:%s" % side, n >= 4, "%d mention(s)" % n)

        # 1. Sewage sludge is never taught as permitted, anywhere on the card.
        bad = sludge_still_permitted(teach)
        report("no_sludge_taught_as_permitted:%s" % side, not bad,
               "found=%r" % (bad[:2] or None))
        report("shipped_wrong_phrase_absent:%s" % side, SHIPPED_WRONG not in teach)

        # 2. Each limb that shipped the defect carries the correction itself.
        rev = section(teach, "Reverse List Approach", r"CE Relevance")
        report("reverse_list_states_removal:%s" % side,
               re.search(r"Sewage sludge is no longer on the list", rev) is not None
               and "LP.6(17)" in rev and "7 October 2022" in rev
               and EIF_OK.search(rev) is not None,
               "LP.6(17), adoption 7 October 2022 and 15 January 2023 required")
        listed = section(rev, "Permitted materials include:", r"\.\s")
        report("reverse_list_enumeration_excludes_sludge:%s" % side,
               bool(listed) and not SLUDGE.search(listed), "list=%r" % listed[:90])
        report("no_new_permits_and_cutoff:%s" % side,
               re.search(r"No new permits", rev) is not None
               and re.search(r"expiry date, but not later than 31 May 2027", rev) is not None)
        report("scope_binds_protocol_parties_only:%s" % side,
               re.search(r"binds Contracting Parties to the 1996 Protocol", rev) is not None
               and re.search(r"party only to the 1972 Convention is not bound", rev) is not None,
               "the amendment is not a worldwide ban")
        widened = [s.strip()[:90] for s in sentences(teach) if SCOPE_1972.search(s)
                   and not re.search(r"\bnot\b|\bonly\b", s)]
        report("scope_not_extended_to_1972_parties:%s" % side, not widened,
               "found=%r" % (widened[:1] or None))
        report("marpol_annex_iv_separated:%s" % side,
               re.search(r"does not change MARPOL Annex IV", rev) is not None)

        s60 = section(teach, "60-Second Answer", r"⚖|Regulatory References")
        report("s60_states_removal:%s" % side,
               re.search(r"sewage sludge was removed from Annex 1 by Resolution LP\.6\(17\)", s60)
               is not None and EIF_OK.search(s60) is not None,
               "%d words" % len(s60.split()))

        reg = section(teach, "Regulatory References", r"CE Oral Tip")
        report("reg_box_has_lp617_row:%s" % side,
               re.search(r"Resolution LP\.6\(17\) Adopted 7 Oct 2022, in force 15 Jan 2023", reg)
               is not None and CUTOFF_OK.search(reg) is not None)

        tip = section(teach, "CE Oral Tip", r"⚠ Examiner Trap")
        report("ce_tip_states_no_longer_permitted:%s" % side,
               re.search(r"Sewage sludge: no longer on the permitted list", tip) is not None
               and "LP.6(17)" in tip)
        report("ce_tip_states_permit_cutoff:%s" % side,
               re.search(r"existing permits end by 31 May 2027 at the latest", tip) is not None)
        report("ce_tip_cross_question_answered_no:%s" % side,
               re.search(r"Is sewage sludge still on the London Protocol's permitted reverse "
                         r"list\?\W*—\s*No\.", tip) is not None)

        # 3. Closed-world dates: no other entry-into-force date, no other cut-off.
        eif_bad = [m.group(1) for m in CLAIM_DATE.finditer(teach)
                   if not EIF_OK.fullmatch(re.sub(r"\s+", " ", m.group(1)))]
        eif_bad += [m.group(1) for m in CLAIM_DATE_REV.finditer(teach)
                    if not EIF_OK.fullmatch(re.sub(r"\s+", " ", m.group(1)))
                    and not ADOPTED_BEFORE.search(teach[max(0, m.start() - 20):m.start()])]
        report("every_entry_into_force_is_15_jan_2023:%s" % side, not eif_bad,
               "other=%r" % (eif_bad[:2] or None))
        # Closed-world: in a permit sentence every date is the cut-off unless the
        # words before it name its own event (adopted / in force / entry). The
        # first version exempted 15 Jan 2023 and 7 Oct 2022 by VALUE, so a tip
        # cut-off moved to either date escaped (independent review F1).
        # Re-check R3: a sentence with an ending verb is about the cut-off, so
        # EVENT_BEFORE no longer exempts its dates; "authorisation" and
        # "licence" count as permits.
        cut_bad = [m.group(0) for s in sentences(teach) if PERMIT.search(s)
                   for m in ANY_DATE.finditer(s)
                   if not CUTOFF_OK.fullmatch(m.group(0))
                   and (ENDING.search(s) or not EVENT_BEFORE.search(s[:m.start()]))]
        report("every_permit_cutoff_is_31_may_2027:%s" % side, not cut_bad,
               "other=%r" % (cut_bad[:2] or None))

        # 4. Never widened into a worldwide ban.
        # Over the whole card, not only sentences that name sludge: "the ban now applies to all IMO Member States" escaped the
        # sentence-scoped first version (independent review F3).
        # The whole teaching text, so the first version's coverage (every
        # sludge sentence, including the reg-box row) stays a subset of this
        # one (re-check R1).
        wide = [m.group(0) for m in WORLDWIDE.finditer(teach)]
        report("not_taught_as_worldwide_ban:%s" % side, not wide,
               "found=%r" % (wide[:1] or None))

    # 5. The stamp records the correction (read on its own: provenance quotes).
    f = footer(cards["gated"])
    report("stamp_records_correction",
           "Q13 · v1.1" in f and "corrected 28 Oct 2026" in f and "LP.6(17)" in f,
           "%r" % f[:80])

    # 6. Corpus: no OTHER page teaches sewage sludge as still on the Annex 1 list.
    scanned, hits, bad_sites, open_seen = 0, 0, [], set()
    for root in (QB, REPO / "SQ"):
        for p in sorted(root.rglob("*.html")):
            try:
                flat = flatten(strip_footers(read_text(p)))
            except (OSError, UnicodeDecodeError):
                continue
            scanned += 1
            rel = p.relative_to(root).as_posix()
            for s in dumping_sentences(flat):
                hits += 1
                if sludge_still_permitted(s):
                    if root == QB and rel in KNOWN_OPEN:
                        open_seen.add(rel)
                    else:
                        bad_sites.append("%s/%s: %s" % (root.name, rel, s[:90]))
    report("corpus_scan_non_vacuous", scanned > 50 and hits >= 8,
           "%d page(s), %d dumping-context sludge sentence(s)" % (scanned, hits))
    report("corpus_no_other_page_teaches_sludge_permitted", not bad_sites,
           "found=%r" % (bad_sites[:2] or None))
    print("INFO tolerated open follow-up sites still uncorrected: %s"
          % (sorted(open_seen) or "none"))

    # 7. Over-correction: MARPOL Annex VI reg 16 sewage-sludge text survives.
    qb3c = flatten(read_text(QB / "QB3_C.html"))
    report("qb3c_annex_vi_sludge_burning_survives",
           re.search(r"Sewage sludge and sludge oil generated during normal operation", qb3c)
           is not None and "reg. 16.4" in qb3c,
           "burning the ship's own sludge is Annex VI and correct")

    # 8. Changelog: governed note states the correction; derived index agrees.
    gov = json.loads(read_text(GOV))
    notes = [e for e in gov.get("recently_updated", []) if e.get("date") == CORR_DATE
             and "LP.6(17)" in e.get("note", "")]
    note = notes[0]["note"] if notes else ""
    report("governed_note_present", len(notes) == 1, "%d note(s)" % len(notes))
    report("governed_note_states_removal",
           re.search(r"sewage sludge", note, re.I) is not None
           and re.search(r"removed|no longer|deleted", note) is not None
           and "15 January 2023" in note)
    idx = json.loads(read_text(IDX))
    report("generated_index_matches_governed_changelog",
           [e.get("note") for e in gov.get("recently_updated", [])]
           == [e.get("note") for e in idx.get("recently_updated", [])])

    # 9. The trap entry: exact shipped phrase as GREP, both open follow-ups logged.
    traps = read_text(TRAPS)
    at = traps.find("### 141. Sewage sludge")
    entry = traps[at:] if at >= 0 else ""
    nxt = re.search(r"\n### \d+\.", entry[5:])
    entry = entry[:nxt.start() + 5] if nxt else entry
    report("trap_141_present", at >= 0)
    grep = re.search(r"^GREP:\s*(.+)$", entry, re.M)
    report("trap_141_greps_the_shipped_phrase",
           bool(grep) and grep.group(1).strip() == SHIPPED_WRONG,
           "GREP=%r" % (grep.group(1)[:50] if grep else None))
    report("trap_141_logs_open_followups",
           all(("**%s.**" % k[-1]) in entry for k in KNOWN_OPEN.values())
           and "QB9_A" in entry and "simon-notes-p8" in entry,
           "every tolerated site must be a logged follow-up")

    # 10. The record still claims what it claims.
    if not MANIFEST.is_file():
        report("record_present", False, "correction record absent")
        return finish()
    rec = json.loads(read_text(MANIFEST))
    text = rec.get("authority", "") + " " + rec.get("rationale", "")
    report("record_states_the_proposition",
           all(x in text for x in ("7 October 2022", "15 January 2023", "31 May 2027"))
           and re.search(r"Delete sub-paragraph 1\.2", text) is not None)
    report("record_cites_trap_141", 141 in (rec.get("known_traps_entries") or []),
           "known_traps_entries=%s" % rec.get("known_traps_entries"))

    # 11. Both sources the record rests on are registered against the card.
    reg_rows = {s.get("source_id"): s for s in json.loads(read_text(REGISTRY)).get("sources", [])}
    want = ("SRC-IMO-LP6-17", "SRC-IMO-STATUS-TREATIES-VOL2-2026-09-30")
    report("sources_registered_for_the_card",
           all(w in reg_rows and "meoclass1/QB1_A.html#q13" in reg_rows[w].get("used_by", [])
               and reg_rows[w].get("supports_correction") == rec.get("correction_id")
               for w in want),
           "missing=%r" % ([w for w in want if w not in reg_rows] or None))

    return finish()


def finish() -> int:
    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    for f in FAILS:
        print("  FAIL " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
