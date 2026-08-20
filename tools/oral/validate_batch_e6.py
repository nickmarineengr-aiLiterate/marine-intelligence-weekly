"""Guard the six authorised E6 IMO-instruments/maritime-law/pollution ENRICHMENT edits.

batch_e6_enrichment_manifest.json is the authority for which enrichment action
edits which existing file#anchor. This validator proves, against the LIVE QB
HTML and against the consolidation record, that:

  * the manifest carries exactly the consolidation's E6 action set, on BOTH of
    the consolidation's independent representations;
  * every action targets the file#anchor, priority band and families the
    consolidation records;
  * every target card still exists, exactly once, under #q-feed;
  * NO new canonical card was created - the corpus total is unchanged, not
    merely "not regressed";
  * only the six authorised cards differ from the baseline commit;
  * each action's missing limb is now actually present, by required token;
  * each action's required authority is cited on the card;
  * every edit is PURELY ADDITIVE - no baseline character was deleted or
    replaced on any authorised card;
  * the manifest's recorded pre/post digests match reality;
  * currentness is stated correctly in BOTH directions;
  * no production metadata is candidate-visible in the added text;
  * q-text and anchors are untouched - this is enrichment, not re-homing;
  * the examiner relationship count is unchanged.

E6 IS THE FINAL ENRICHMENT BATCH. That is a reason for more care, not less: it
is the last chance for a defect to enter the corpus through this route, and
there is no following batch whose guards would catch a mistake made here.

WHY E6 HAS NO SHARED TARGET - AND WHY THAT IS ASSERTED
E1 and E5 both carried two actions on one card, and both needed extra guards to
stop the pair collapsing into one. E6 does not: six actions land on six
distinct cards in six distinct files. That makes the arithmetic
actions == distinct cards == changed cards == 6 exact rather than approximate,
so `no_shared_target` asserts the absence rather than leaving it implied. If a
future edit ever put two E6 actions on one card, the arithmetic would break
loudly instead of silently weakening every count in this file.

WHY LINE ENDINGS ARE A GUARD IN THIS BATCH AND NOT THE EARLIER ONES
E6 is the FIRST enrichment batch with a mixed destination set. QB4_I.html and
QB9_G.html are 100% CRLF on disk; the other four destinations are 100% LF. E5
recorded that a shell probe (`grep -c $'\\r'`) reported all nine of its files as
CRLF when they were all LF, and that writing insertions on that false evidence
would have left every one of them mixed-ending. Here the evidence is real and
the files genuinely differ, so a single batch-wide convention would corrupt two
files or four. `line_endings_homogeneous_per_file` measures untranslated bytes
and requires each destination to be wholly one convention and to match what the
manifest recorded. Digests everywhere in this batch are LF-normalised so they
are independent of the on-disk convention.

WHY CURRENTNESS IS GUARDED IN BOTH DIRECTIONS
E6 carries three CURRENT_REG_VERIFY_REQUIRED actions - the highest
concentration of any enrichment batch - and they do NOT all run the same way:

  * A047 - SOLAS V/31 and V/32 as amended by MSC.550(108) were adopted on
    23 May 2024 and ENTERED INTO FORCE on 1 January 2026. The risk here is the
    REVERSE of the usual one: describing a rule that already binds as though it
    were still pending. Asserting that container-loss reporting "will apply" or
    "is not yet in force" is therefore a forbidden claim.
  * A045 - the revised IMSAS Framework and Procedures, resolution A.1211(34),
    is ADOPTED but does not begin to operate until the second audit cycle opens
    in July 2027. Presenting risk-based continuous monitoring as today's regime
    is the defect, so "does not begin to operate until the second cycle opens"
    is a required qualifier.
  * A048 - the Merchant Shipping Act, 2025 is in force, but the 2026 pollution
    rules made under Part VII are DRAFTS. Presenting them as in force is
    forbidden.

Adopted is not in force, and in force is not forthcoming. Both errors are
caught, because E6 contains a live example of each.

WHY A047 FORBIDS A FAL FORM CARRYING THE CONTAINER REPORT
The consolidation asked for "which declaration/form carries" a container-loss
report, on the FAL card. Checked against FAL Standard 2.1 as amended by
FAL.14(46), the answer is that NO FAL declaration carries it: the report is a
danger message under SOLAS V/31 and V/32, with MARPOL Protocol I Article V
routing the harmful-substances report through the same regulations. Naming a
FAL form as the vehicle would be wrong law, and it is exactly the wrong answer
a candidate reaches for, so it is forbidden outright rather than left to the
positive token checks. This is the same shape as E5's A036, where the
consolidation asked for door sill heights as MLC accommodation minima and the
instrument did not contain them.

WHY A048 BANS 1958-ACT SECTION NUMBERING
While researching this batch, a secondary source confidently placed India's
oil-pollution provisions at "Part XIA, sections 356A-356O of the Merchant
Shipping Act, 2025". That is the numbering of the Merchant Shipping Act, 1958
as amended. The 2025 Act is a consolidating statute of sixteen Parts and 325
sections, so a section 356A cannot exist in it. The verified position - Part VII
and the section 133 to 143 block - comes from the Government of India's own
2026 draft rules, each of which recites the sections it is made under. A
letter-suffixed section number in the 300s is therefore a forbidden claim: it is
the specific wrong answer the available secondary sources will hand a future
editor.

WHY THE HYGIENE SCAN RUNS ON ADDED TEXT ONLY
Carried from E5. These pages hold pre-existing candidate-visible debt that E6 is
not authorised to repair - QB3_J#q5's reg-box says "section mapping pending
verification" and QB9_B#q2 carries a literal "CORRECTION FOOTER" line with the
wrong card id. Scanning whole cards would fail the batch for text it did not
write and cannot touch, so the scan runs on the inserted characters only.

WHY THE NEGATIVE GUARDS ARE ENTITY-UNESCAPED
Carried from E1: these pages write "&" as "&amp;", and a forbidden-claim guard
spelled with a bare "&" is blind to the escaped form. Every negative guard runs
over html.unescape(card).
"""
import difflib
import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).resolve().parent / "batch_e6_enrichment_manifest.json"
QB_DIR = REPO / "meoclass1"
CONSOL_REL = ("meoclass1/oral-intelligence/examiner-audit/"
              "FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json")
CONSOL_REF = "origin/research/oral-final-enrichment-consolidation"

EXPECTED_ACTIONS = 6

FORBIDDEN = re.compile(
    r"ENRICH-A\d|GAP-\d{4}|\bTODO\b|\bFIXME\b|(?<![\w-])VERIFY(?![\w-])"
    r"|\bCORRECTED:|recurrence_class|laptop_review|missing_limb|batch_id"
    r"|production_action|pending verification|sections pending"
    r"|\b[a-z_]+\.(?:json|py|xlsx)\b")

# Tokens that can only be present if the action's missing limb was supplied.
# Every one was checked ABSENT from the BASELINE card before adoption. Two
# candidates were rejected on that test: "protocol" and "by reference" for
# A046, both of which the baseline card already carried in its deep-dive - a
# reminder that A046's limb was PARTLY pre-covered and that guarding on either
# would have passed without the ladder being there at all.
LIMB_TOKENS = {
    "ENRICH-A045": ["nominated by Member States", "IMO Secretariat",
                    "4 March 2024", "A.1211(34)", "July 2027"],
    "ENRICH-A046": ["Annexes III to VI", "no binding force of its own",
                    "recommendatory"],
    "ENRICH-A047": ["thirteen", "FAL.14(46)", "MSC.550(108)", "Regulation V/31",
                    "Regulation V/32", "IX/1.2", "Universal Postal Union",
                    "Ship Sanitation Control", "XI-2/9.2.2"],
    "ENRICH-A048": ["Part VII", "sections 133 to 143", "Act 24 of 2025",
                    "Maritime Rescue Coordination Centre",
                    "Spill Notification Pro forma"],
    "ENRICH-A049": ["strategic layer", "tactical layer", "rehearses and tests"],
    "ENRICH-A050": ["International Telecommunication Union",
                    "United Nations specialised agency", "Appendix 42",
                    "Articles 30 to 34", "Maritime Identification Digits"],
}

# Authority that must remain cited for the limb to stand up. A046 and A049 are
# TECHNICAL_REASONING_ONLY and assert no instrument of their own, so their sets
# are deliberately empty rather than absent by oversight.
AUTHORITY_TOKENS = {
    "ENRICH-A045": ["A.1070(28)", "A.1211(34)"],
    "ENRICH-A046": [],
    "ENRICH-A047": ["FAL.14(46)", "MSC.550(108)", "MARPOL Protocol I, Article V"],
    "ENRICH-A048": ["Merchant Shipping Act, 2025", "Part VII"],
    "ENRICH-A049": [],
    "ENRICH-A050": ["Appendix 43", "Appendix 42", "Radio Regulations"],
}

# Over-simplifications that are wrong law and are not on the card today.
# Every pattern was run against the BASELINE card before adoption.
FORBIDDEN_CLAIMS = {
    # The revised IMSAS framework is adopted, not operating.
    "ENRICH-A045": [r"continuous monitoring[^.]{0,60}(?:is|are) (?:now )?in (?:force|operation)",
                    r"second cycle[^.]{0,40}(?:is|has) (?:already )?(?:begun|started|under way)",
                    r"audit(?:s|ed)? (?:are |is )?(?:conducted|carried out) by imo staff"],
    # No FAL declaration carries a container-loss report.
    "ENRICH-A047": [r"fal form \d[^.]{0,60}container",
                    r"container[^.]{0,60}(?:reported|declared) on a fal form",
                    r"(?:msc\.550\(108\)|container-loss reporting)[^.]{0,60}"
                    r"(?:not yet in force|will (?:enter into force|apply)|comes into force)"],
    # The 1958 Act's numbering is not the 2025 Act's, and the rules are drafts.
    "ENRICH-A048": [r"section 3\d\d[a-o]\b",
                    r"part xi[ab]\b",
                    r"2026 rules[^.]{0,40}(?:are|is) in force",
                    # The card DENIES a threshold ("assuming a reportable
                    # threshold is the single most common error"), so the guard
                    # must ban the ASSERTION, not the phrase. Banning the bare
                    # words failed the card for saying the correct thing - the
                    # same shape E5 hit when a guard was written against
                    # "Rule 37" and the card correctly said "Rules 35 to 37".
                    r"reportable (?:threshold|quantity)[^.]{0,25}\d",
                    r"only (?:reportable|reported)[^.]{0,40}"
                    r"(?:exceeds|more than|above|over)",
                    r"minimum (?:reportable )?quantity of[^.]{0,20}\d"],
}

# Conditions that must accompany a claim for it to stay true. A later tidy-up
# could keep every positive token above and still flatten these into wrong law.
REQUIRED_QUALIFIER = {
    # Adopted is not operating.
    "ENRICH-A045": ["does not begin to operate until the second cycle opens",
                    "not IMO staff"],
    # A code binds only through the regulation that references it.
    "ENRICH-A046": ["no binding force of its own"],
    # The trap, and the in-force position stated as current.
    "ENRICH-A047": ["No FAL declaration carries a container-loss report",
                    "Since <strong>1 January 2026</strong>"],
    # No section number is pinned for the reporting duty, and no threshold.
    "ENRICH-A048": ["no single &quot;spill reporting&quot; section to quote",
                    "of any quantity"],
    # The drill tests the plan; it does not replace it.
    "ENRICH-A049": ["rehearses and tests"],
    # The ITU is not an IMO body.
    "ENRICH-A050": ["United Nations specialised agency"],
}

VALID_STATUS_PREFIX = ("IMPLEMENTED", "REDUCED SCOPE")

_fails = []
_checks = 0


def report(name, ok, detail=""):
    global _checks
    _checks += 1
    print("%-5s %-46s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        _fails.append(name)


CARD_OPEN = re.compile(r'<div class="q-card[^"]*"[^>]*>', re.I)
CANONICAL_ANCHOR = re.compile(r"q\d+")


def _balanced_end(text, start):
    depth = 0
    for m in re.finditer(r"<div\b[^>]*>|</div\s*>", text[start:], re.I):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return start + m.end()
    raise AssertionError("unbalanced q-card at %d" % start)


def cards_of(text):
    text = text.replace("\r\n", "\n")
    out = {}
    for m in CARD_OPEN.finditer(text):
        end = _balanced_end(text, m.start())
        a = re.search(r'\bid="([^"]+)"', m.group(0))
        if a:
            out[a.group(1)] = text[m.start():end]
    return out


def canonical_cards(text):
    """Only the q-cards that are canonical QUESTIONS.

    Counting the .q-card class rather than the anchor convention inflates the
    corpus and lets a count assertion pass vacuously - the corpus carries more
    .q-card blocks than canonical questions.
    """
    return {a: c for a, c in cards_of(text).items()
            if CANONICAL_ANCHOR.fullmatch(a)}


def git_show(ref, rel):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, rel)],
                       cwd=str(REPO), capture_output=True)
    if r.returncode != 0 or not r.stdout:
        return None
    return r.stdout.decode("utf-8", "replace")


_QB_BASELINE = {}


def baseline_qb(ref, page):
    """Baseline text of meoclass1/<page>, read from ONE git archive call.

    The obvious implementation calls `git show` once per file, which this
    validator would do 172 times per run - and the mutation harness runs the
    validator 30-plus times. Streaming the whole meoclass1 tree out of the
    object store once turns ~172 subprocesses into one and takes the run from
    about ninety seconds to a few.
    """
    if ref not in _QB_BASELINE:
        cache = {}
        r = subprocess.run(["git", "archive", "--format=tar", ref, "meoclass1"],
                           cwd=str(REPO), capture_output=True)
        if r.returncode == 0 and r.stdout:
            import io as _io
            import tarfile
            with tarfile.open(fileobj=_io.BytesIO(r.stdout)) as tf:
                for mem in tf.getmembers():
                    if not mem.isfile():
                        continue
                    name = mem.name.split("/")[-1]
                    if name.startswith("QB") and name.endswith(".html"):
                        f = tf.extractfile(mem)
                        if f is not None:
                            cache[name] = f.read().decode("utf-8", "replace")
        _QB_BASELINE[ref] = cache
    return _QB_BASELINE[ref].get(page)


def load_consolidation(manifest):
    p = REPO / CONSOL_REL
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8")), "tree"
    raw = git_show(manifest.get("authorisation_commit") or CONSOL_REF, CONSOL_REL)
    if raw is None:
        raw = git_show(CONSOL_REF, CONSOL_REL)
    if raw is None:
        return None, "unavailable"
    return json.loads(raw), "git"


def added_text(base_card, live_card):
    sm = difflib.SequenceMatcher(None, base_card, live_card, autojunk=False)
    return "".join(live_card[j1:j2] for tag, _, _, j1, j2 in sm.get_opcodes()
                   if tag in ("insert", "replace"))


def digest(s):
    return hashlib.sha256(s.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def read_page(page):
    return (QB_DIR / page).read_text(encoding="utf-8", newline="")


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cards = manifest.get("cards", [])
    baseline = manifest.get("baseline_commit") or "origin/main"

    # ---------- authorisation identity ----------
    consol, src = load_consolidation(manifest)
    if consol is None:
        report("consolidation_available", False, "unavailable")
        print("\nE6 enrichment validator: %d checks, %d FAIL" % (_checks, len(_fails)))
        return 1
    report("consolidation_available", True, "source=%s" % src)

    # The batch is selected THROUGH the manifest's own authorisation_batch_key
    # rather than through a hardcoded "E6". The first mutation run proved why:
    # with the key unused, pointing it at batches.E5 changed nothing and the
    # mutation ESCAPED. A field the validator does not read is decoration, and
    # decoration in an authorisation record is worse than nothing - it looks
    # like provenance while guaranteeing none.
    key = str(manifest.get("authorisation_batch_key") or "")
    bid = key.split(".")[-1] if key.startswith("batches.") else None
    report("authorisation_batch_key_matches_batch_id",
           bid is not None and bid == manifest.get("batch_id") == "E6",
           "key=%s -> batch_id=%s manifest.batch_id=%s"
           % (key or "-", bid or "-", manifest.get("batch_id")))

    batch = [b for b in consol.get("batches", []) if b.get("batch_id") == bid]
    rep1 = batch[0]["action_ids"] if batch else []
    rep2 = [a["action_id"] for a in consol.get("production_actions", [])
            if a.get("batch") == bid]
    mine = [c["action_id"] for c in cards]

    report("consolidation_representations_agree", bool(batch) and rep1 == rep2,
           "batches=%d production_actions=%d equal_in_order=%s"
           % (len(rep1), len(rep2), rep1 == rep2))
    report("authorised_action_set", mine == rep1 and len(mine) == EXPECTED_ACTIONS,
           "manifest=%s consolidation=%s" % (mine, rep1))
    report("declared_action_count_matches",
           bool(batch) and batch[0].get("action_count") == EXPECTED_ACTIONS == len(mine),
           "declared=%s actual=%d" % (batch[0].get("action_count") if batch else "-", len(mine)))

    by_id = {a["action_id"]: a for a in consol.get("production_actions", [])}
    tgt_bad, fam_bad, pri_bad = [], [], []
    for c in cards:
        a = by_id.get(c["action_id"])
        if not a:
            tgt_bad.append("%s absent from consolidation" % c["action_id"])
            continue
        if a["target"] != "%s#%s" % (c["file"].replace(".html", ""), c["anchor"]):
            tgt_bad.append("%s: %s vs %s#%s" % (c["action_id"], a["target"],
                                                c["file"], c["anchor"]))
        if sorted(a["family_ids"]) != sorted(c["family_ids"]):
            fam_bad.append(c["action_id"])
        if a["priority"] != c["priority"] or \
           a["verification_scope"] != c["verification_scope"]:
            pri_bad.append(c["action_id"])
    report("authorised_targets", not tgt_bad, "%s" % (tgt_bad or "all six match"))
    report("authorised_families", not fam_bad, "%s" % (fam_bad or "all six match"))
    report("authorised_priority_and_scope", not pri_bad,
           "%s" % (pri_bad or "all six match"))

    fams = set()
    for c in cards:
        fams |= set(c["family_ids"])
    report("batch_family_union_matches",
           bool(batch) and fams == set(batch[0].get("source_family_ids", [])),
           "union=%d declared=%d" % (len(fams), len(batch[0].get("source_family_ids", [])) if batch else 0))

    # ---------- E6 has no shared target ----------
    pairs = ["%s#%s" % (c["file"], c["anchor"]) for c in cards]
    report("no_shared_target",
           len(set(pairs)) == len(pairs) == EXPECTED_ACTIONS
           and manifest.get("shared_target") is None
           and manifest.get("distinct_target_cards") == EXPECTED_ACTIONS,
           "actions=%d distinct_cards=%d shared_target=%s"
           % (len(pairs), len(set(pairs)), manifest.get("shared_target")))

    report("manifest_declares_no_new_cards",
           manifest.get("creates_new_cards") is False,
           "creates_new_cards=%s" % manifest.get("creates_new_cards"))

    bad_status = [c["action_id"] for c in cards
                  if not str(c.get("status", "")).startswith(VALID_STATUS_PREFIX)]
    report("authorised_enrichment_disposition", not bad_status,
           "%s" % (bad_status or "all six IMPLEMENTED / REDUCED SCOPE"))

    # ---------- targets resolve ----------
    live, base = {}, {}
    resolve_bad = []
    for c in cards:
        page, anchor = c["file"], c["anchor"]
        try:
            lt = read_page(page)
        except OSError:
            resolve_bad.append("%s missing" % page)
            continue
        lc = canonical_cards(lt)
        if anchor not in lc:
            resolve_bad.append("%s#%s absent" % (page, anchor))
            continue
        if lt.replace("\r\n", "\n").count(lc[anchor]) != 1:
            resolve_bad.append("%s#%s not unique" % (page, anchor))
        live[c["action_id"]] = lc[anchor]
        bt = baseline_qb(baseline, page)
        base[c["action_id"]] = canonical_cards(bt).get(anchor) if bt else None
    report("targets_resolve", not resolve_bad, "%s" % (resolve_bad or "6/6 resolve uniquely"))

    missing_base = [k for k, v in base.items() if v is None]
    report("baseline_cards_available", not missing_base,
           "baseline=%s %s" % (baseline, missing_base or "6/6"))

    # ---------- line endings ----------
    eol_bad = []
    for c in cards:
        raw = (QB_DIR / c["file"]).read_bytes()
        lf, crlf = raw.count(b"\n"), raw.count(b"\r\n")
        actual = "CRLF" if (lf and crlf == lf) else ("LF" if crlf == 0 else "MIXED")
        if actual == "MIXED":
            eol_bad.append("%s is MIXED" % c["file"])
        elif actual != c.get("file_line_endings"):
            eol_bad.append("%s is %s, manifest says %s"
                           % (c["file"], actual, c.get("file_line_endings")))
    report("line_endings_homogeneous_per_file", not eol_bad,
           "%s" % (eol_bad or "6/6 homogeneous and as recorded"))

    # ---------- corpus totals ----------
    total, files = 0, 0
    for p in sorted(QB_DIR.glob("QB*.html")):
        n = len(canonical_cards(p.read_text(encoding="utf-8", newline="")))
        if n:
            files += 1
            total += n
    exp_q = manifest.get("expected_canonical_questions")
    exp_f = manifest.get("expected_question_bearing_files")
    report("canonical_total_unchanged", total == exp_q and files == exp_f,
           "questions=%d (expect %s) files=%d (expect %s)" % (total, exp_q, files, exp_f))

    # ---------- only authorised cards changed ----------
    authorised_elsewhere = set()
    for sib in sorted(MANIFEST.parent.glob("batch_*_manifest.json")):
        if sib == MANIFEST:
            continue
        for sc in json.loads(sib.read_text(encoding="utf-8")).get("cards", []):
            authorised_elsewhere.add("%s#%s" % (sc["file"], sc["anchor"]))

    changed = []
    for p in sorted(QB_DIR.glob("QB*.html")):
        bt = baseline_qb(baseline, p.name)
        if bt is None:
            continue
        bc = canonical_cards(bt)
        lc = canonical_cards(p.read_text(encoding="utf-8", newline=""))
        for a in set(bc) | set(lc):
            if bc.get(a) != lc.get(a):
                changed.append("%s#%s" % (p.name, a))
    authorised = set(pairs)
    unauthorised = sorted(set(changed) - authorised - authorised_elsewhere)
    exempt = sorted((set(changed) - authorised) & authorised_elsewhere)
    report("only_authorised_cards_changed", not unauthorised,
           "unauthorised=%s authorised-elsewhere=%d"
           % (unauthorised or "-", len(exempt)))

    not_changed = sorted(authorised - set(changed))
    report("every_authorised_card_changed", not not_changed,
           "%s" % (not_changed or "6/6 differ from baseline"))

    # ---------- limbs, authority, additivity, digests ----------
    limb_bad, auth_bad, add_bad, dig_bad, qual_bad, claim_bad = [], [], [], [], [], []
    hygiene_bad, qtext_bad, timed_bad = [], [], []
    for c in cards:
        aid = c["action_id"]
        lc, bc = live.get(aid), base.get(aid)
        if lc is None or bc is None:
            continue
        low = html.unescape(lc).lower()

        missing = [t for t in LIMB_TOKENS.get(aid, []) if t.lower() not in low]
        if missing:
            limb_bad.append("%s lacks %s" % (aid, missing))

        amiss = [t for t in AUTHORITY_TOKENS.get(aid, []) if t.lower() not in low]
        if amiss:
            auth_bad.append("%s lacks %s" % (aid, amiss))

        qmiss = [q for q in REQUIRED_QUALIFIER.get(aid, [])
                 if q.lower() not in lc.lower()]
        if qmiss:
            qual_bad.append("%s lacks %s" % (aid, qmiss))

        for pat in FORBIDDEN_CLAIMS.get(aid, []):
            m = re.search(pat, low)
            if m:
                claim_bad.append("%s: %r" % (aid, m.group(0)[:70]))

        ops = difflib.SequenceMatcher(None, bc, lc, autojunk=False).get_opcodes()
        nondd = [t for t, _, _, _, _ in ops if t in ("delete", "replace")]
        if nondd:
            add_bad.append("%s has %s" % (aid, nondd))

        if digest(bc) != c.get("pre_edit_digest"):
            dig_bad.append("%s pre" % aid)
        if digest(lc) != c.get("post_edit_digest"):
            dig_bad.append("%s post" % aid)

        add = added_text(bc, lc)
        hit = FORBIDDEN.search(html.unescape(add))
        if hit:
            hygiene_bad.append("%s: %r" % (aid, hit.group(0)))

        def qt(card):
            m = re.search(r'class="q-text"[^>]*>(.*?)</div>', card, re.S)
            return re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        if qt(bc) != qt(lc):
            qtext_bad.append(aid)

        def timed(card):
            return re.findall(r"(15-Second Answer.*?</div>|60-Second Answer.*?</div>"
                              r"|oral-box oral-\d+.*?</div>)", card, re.S)
        if timed(bc) != timed(lc):
            timed_bad.append(aid)
        if c.get("timed_blocks_changed") is not False:
            timed_bad.append("%s manifest claims a timed change" % aid)

    report("missing_limb_supplied", not limb_bad, "%s" % (limb_bad or "6/6 supplied"))
    report("required_authority_cited", not auth_bad, "%s" % (auth_bad or "6/6 cited"))
    report("required_qualifiers_kept", not qual_bad, "%s" % (qual_bad or "6/6 kept"))
    report("unsubstantiated_claims_absent", not claim_bad,
           "%s" % (claim_bad or "no forbidden claim on any card"))
    report("edits_purely_additive", not add_bad,
           "%s" % (add_bad or "6/6 insert-only, 0 delete, 0 replace"))
    report("manifest_digests_match", not dig_bad, "%s" % (dig_bad or "12/12 digests match"))
    report("no_candidate_visible_metadata", not hygiene_bad,
           "%s" % (hygiene_bad or "added text clean on 6/6"))
    report("q_text_and_anchors_stable", not qtext_bad,
           "%s" % (qtext_bad or "q-text unchanged on 6/6"))
    report("timed_blocks_unchanged", not timed_bad,
           "%s" % (timed_bad or "15s/60s byte-identical on 6/6"))

    # ---------- currentness declared ----------
    cur_bad = []
    for c in cards:
        if c["verification_scope"] == "CURRENT_REG_VERIFY_REQUIRED":
            cur = c.get("currentness") or {}
            for k in ("instrument", "latest_amendment", "mandatory_now",
                      "adopted_not_in_force", "card_was_stale"):
                if not cur.get(k):
                    cur_bad.append("%s missing %s" % (c["action_id"], k))
    n_cur = sum(1 for c in cards
                if c["verification_scope"] == "CURRENT_REG_VERIFY_REQUIRED")
    report("currentness_recorded_for_current_reg", not cur_bad and n_cur == 3,
           "%s (current_reg actions=%d)" % (cur_bad or "3/3 fully recorded", n_cur))

    # ---------- follow-up overlap ----------
    colo = [c for c in consol.get("followup_colocation", [])
            if c.get("enrichment_action_id") in set(mine)]
    declared = [c for c in cards if c.get("followup_overlap")]
    fu_ok = (len(colo) == len(declared) == 1
             and declared[0]["action_id"] == colo[0]["enrichment_action_id"]
             and declared[0]["followup_overlap"].get("distinctness") == "DISTINCT"
             and declared[0]["followup_overlap"].get("consumed") is False
             and bool(declared[0]["followup_overlap"].get("distinctness_reason")))
    report("followup_overlap_explicit", fu_ok,
           "consolidation=%d manifest=%d action=%s consumed=%s"
           % (len(colo), len(declared),
              declared[0]["action_id"] if declared else "-",
              declared[0]["followup_overlap"].get("consumed") if declared else "-"))

    # ---------- examiner delta ----------
    rel_live = rel_base = 0
    for p in sorted(QB_DIR.glob("QB*.html")):
        rel_live += len(re.findall(r"examiner-tag",
                                   p.read_text(encoding="utf-8", newline="")))
        bt = baseline_qb(baseline, p.name)
        if bt:
            rel_base += len(re.findall(r"examiner-tag", bt))
    report("examiner_relationship_delta_zero", rel_live == rel_base,
           "live=%d baseline=%d delta=%d" % (rel_live, rel_base, rel_live - rel_base))

    # The inline examiner-tag count above proves DELTA only. The absolute
    # 960/7 lives in the generated examiner index snapshot, so the manifest's
    # declared expectations are checked against that artefact rather than
    # against a number typed into this file.
    snap_p = (REPO / "meoclass1" / "oral-intelligence" / "examiner-audit"
              / "EXAMINER_INDEX_SNAPSHOT.json")
    if snap_p.exists():
        tot = json.loads(snap_p.read_text(encoding="utf-8")).get("totals", {})
        ok = (manifest.get("expected_examiner_relationships") == tot.get("relationships")
              and manifest.get("expected_examiners") == tot.get("examiners")
              and manifest.get("expected_question_bearing_files") == tot.get("qb_files")
              and manifest.get("expected_canonical_questions") == tot.get("canonical_questions"))
        report("examiner_index_expectation_stable", ok,
               "snapshot relationships=%s examiners=%s qb_files=%s questions=%s"
               % (tot.get("relationships"), tot.get("examiners"),
                  tot.get("qb_files"), tot.get("canonical_questions")))
    else:
        report("examiner_index_expectation_stable", False,
               "EXAMINER_INDEX_SNAPSHOT.json unavailable")

    print("\nE6 enrichment validator: %d checks, %d FAIL" % (_checks, len(_fails)))
    if _fails:
        print("failed:", ", ".join(_fails))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
