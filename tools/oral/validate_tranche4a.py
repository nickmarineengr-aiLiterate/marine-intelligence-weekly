#!/usr/bin/env python3
"""Tranche 4A binding gates.

Four families, each narrow and each tied to a Tranche-4 finding that this
correction pass closed:

  A. Grain Code        QB2_A#q33   (P1-01, P2-01)
  B. CII G2/G4 + CF    QB7_I#q10, QB6#q1, QB6_cheatsheet.html   (P1-02, P2-05)
  C. BMP / security    QB4_B#q16, QB4_H#q2, QB9_A#q9, QB9_B#q5
                       (P1-03..08, P1-10..11, P1-13..16, P1-18..19, P2-06/14/15)
  D. Authoring artefacts   bounded census across meoclass1/*.html

Scoping rule: every content check is evaluated against the CARD it belongs to,
extracted by balanced <div> from its anchor, never against the whole file.  A
file-scoped check would pass on a defect that had merely moved to a different
question.

Exit 0 = all gates PASS.  Exit 1 = any FAIL.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QB = os.path.join(ROOT, "meoclass1")

RESULTS = []


def read(name):
    with io.open(os.path.join(QB, name), encoding="utf-8") as fh:
        return fh.read()


def card(text, anchor):
    """Return the balanced q-card div that carries id="<anchor>"."""
    idx = text.find('id="%s"' % anchor)
    if idx < 0:
        return None
    start = text.rfind('<div class="q-card"', 0, idx)
    if start < 0:
        return None
    depth = 0
    pos = start
    tag = re.compile(r"</?div\b", re.I)
    while True:
        m = tag.search(text, pos)
        if not m:
            return text[start:]
        depth += -1 if text[m.start():m.start() + 2] == "</" else 1
        pos = m.end()
        if depth == 0:
            return text[start:text.find(">", pos) + 1]


def flat(s):
    """Tag-stripped, entity-normalised, whitespace-collapsed CANDIDATE text.

    The q-version stamp is stripped first.  A correction stamp necessarily
    quotes the defect it removed ("no longer claims SOLAS XI-2/8...", "the
    invented 72 hours..."), so a content guard that reads it will flag the
    very audit trail that proves the fix.  Provenance is not candidate teaching
    and must sit outside the sweep.
    """
    import html as _h
    s = re.sub(r'<span class="q-version">.*?</span>', " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = _h.unescape(s)
    return re.sub(r"\s+", " ", s)


def elements(fragment):
    """Leaf-ish candidate-facing blocks: list items, reg rows, paragraphs, tiers.

    A character window around a match is not a scope: two adjacent bullets can
    satisfy each other's guard, so a defect reintroduced in one bullet hides
    behind the correct wording in its neighbour.  Element scoping removes that.
    """
    pats = [
        r"<li\b[^>]*>.*?</li>",
        r'<div class="reg-item">.*?</div>',
        r'<div class="practice-block">.*?</div>',
        r"<p\b[^>]*>.*?</p>",
        r"<h4\b[^>]*>.*?</h4>",
        r"<h5\b[^>]*>.*?</h5>",
    ]
    out = []
    for pat in pats:
        out.extend(re.findall(pat, fragment, re.S))
    return [flat(x) for x in out]


def reg_codes(fragment):
    """The reg-code slots of a card - the tokens a candidate actually quotes.

    A reg-desc may legitimately name a revoked resolution while explaining the
    revocation; a reg-CODE may not.  Checking only the flattened card lets a
    wrong code hide behind a right description.
    """
    return re.findall(r'<span class="reg-code">(.*?)</span>', fragment, re.S)


def check(gate, cid, ok, detail):
    RESULTS.append((gate, cid, bool(ok), detail))


def near(text, needle, other, window=420):
    """True if every occurrence of `needle` has `other` within `window` chars."""
    for m in re.finditer(re.escape(needle), text):
        lo = max(0, m.start() - window)
        if not re.search(other, text[lo:m.start() + window], re.I):
            return False
    return True


# ---------------------------------------------------------------- A. Grain
def gate_grain():
    g = "GRAIN"
    c = card(read("QB2_A.html"), "q33")
    check(g, "G-00", c is not None, "QB2_A#q33 card extracted")
    if c is None:
        return
    f = flat(c)
    # The Document of Authorisation is A 3, the booklet A 6 - never A 7.
    check(g, "G-01", "International Grain Code, A 3 / A 6" in f,
          "reg-box cites Grain Code A 3 / A 6 for the DoA and booklet")
    check(g, "G-02",
          not re.search(r"International Grain Code,\s*A 7\b", f),
          "no reg-box row cites 'International Grain Code, A 7'")
    check(g, "G-03",
          not re.search(r"A 7[^.]{0,80}Document of Authorisation", f, re.I),
          "A 7 is not offered as the Document of Authorisation authority")
    check(g, "G-04", re.search(r"A 7 is the stability criteria", f, re.I) is not None,
          "card states positively that A 7 is the stability criteria")
    # The 12 deg criterion must keep its applicability limb wherever it is taught.
    twelve = [m.start() for m in re.finditer(r"12°", f)]
    check(g, "G-05", len(twelve) >= 2, "12 deg criterion taught in at least two layers (%d)" % len(twelve))
    check(g, "G-06", near(f, "deck edge is immersed", r"1 January 1994"),
          "body deck-edge limb carries its 1 January 1994 applicability")
    check(g, "G-07", near(f, "deck-edge immersion if less", r"1 January 1994"),
          "Numbers layer deck-edge limb carries its 1 January 1994 applicability")
    check(g, "G-08", f.count("1 January 1994") >= 2,
          "the 1994 condition appears in both places the 12 deg limit is taught")
    # Untouched grain teaching must survive.
    for token, label in (("0.075", "residual area 0.075 m.rad"),
                         ("0.30 m", "corrected GM 0.30 m"),
                         ("MSC.552(108)", "the amending resolution"),
                         ("1 January 2026", "entry into force")):
        check(g, "G-09:" + token, token in f, "retained: %s" % label)


# ------------------------------------------------------------------ B. CII
def gate_cii():
    g = "CII"
    qb7 = read("QB7_I.html")
    qb6 = read("QB6.html")
    cs = read("QB6_cheatsheet.html")
    c7 = card(qb7, "q10")
    c6 = card(qb6, "q1")
    check(g, "C-00", c7 is not None and c6 is not None, "QB7_I#q10 and QB6#q1 extracted")
    if c7 is None or c6 is None:
        return
    f7, f6, fc = flat(c7), flat(c6), flat(cs)

    # Current G2 / G4 must be the 2022 pair, everywhere the pair is taught.
    codes7, codes6 = " | ".join(reg_codes(c7)), " | ".join(reg_codes(c6))
    check(g, "C-01",
          "MEPC.353(78)" in codes7 and "MEPC.354(78)" in codes7
          and "MEPC.337(76)" not in codes7 and "MEPC.339(76)" not in codes7,
          "QB7_I#q10 reg-CODE slot carries the 2022 pair and not the revoked pair")
    check(g, "C-02",
          "MEPC.353(78)" in f6 and "MEPC.354(78)" in f6
          and "MEPC.337(76)" not in codes6 and "MEPC.339(76)" not in codes6
          and not re.search(r"<strong>MEPC\.33[79]\(76\)</strong>\s*(&mdash;|—)\s*CII reference lines|"
                            r"<strong>MEPC\.33[79]\(76\)</strong>\s*(&mdash;|—)\s*rating bands", c6),
          "QB6#q1 teaches the 2022 pair and never labels a 2021 resolution as the live G2/G4")
    check(g, "C-03", "MEPC.353(78)" in fc and "MEPC.354(78)" in fc,
          "QB6_cheatsheet carries the current G2/G4 pair")

    # The revoked 2021 pair may survive ONLY as an explicitly historical mention.
    for label, frag in (("QB7_I#q10", f7), ("QB6#q1", f6), ("QB6_cheatsheet", fc)):
        for old in ("MEPC.337(76)", "MEPC.339(76)"):
            ok = old not in frag or near(frag, old, r"revoke|revoked|2021|superseded", 300)
            check(g, "C-04:%s:%s" % (label, old), ok,
                  "%s: %s appears only as a revoked/2021 reference" % (label, old))

    # An EEDI guideline must not stand alone as the CII authority.
    for label, raw in (("QB7_I#q10", c7), ("QB6#q1", c6)):
        bad = [e for e in elements(raw)
               if "MEPC.364(79)" in e and not re.search(r"MEPC\.352\(78\)|\bG1\b", e)]
        check(g, "C-05:" + label, not bad,
              "%s: no element cites MEPC.364(79) for CII without naming G1/MEPC.352(78)" % label)
    check(g, "C-06", "MEPC.352(78)" in f7, "QB7_I#q10 names G1 as the CII authority")

    # The EEXI trap the card exists to teach must survive.
    check(g, "C-07", "MEPC.333(76)" in f7 and re.search(r"EEXI", f7), "EEXI/CII trap retained")
    # G3 was not part of this correction and must be untouched.
    check(g, "C-08", "MEPC.338(76)" in f6, "G3 MEPC.338(76) left in place")


# ------------------------------------------------------------------ C. BMP
BMP_CARDS = [("QB4_B.html", "q16"), ("QB4_H.html", "q2"),
             ("QB9_A.html", "q9"), ("QB9_B.html", "q5")]

CURRENT_CLAIM = re.compile(
    r"BMP\s*5[^.]{0,120}?\b(is|as)\b[^.]{0,60}?current"
    r"|current\s+(active|applicable)\s+(edition|version|publication)[^.]{0,80}?BMP\s*5"
    r"|current\s+(active|applicable)\s+(edition|version|publication)\s+is\s+BMP\s*5"
    r"|BMP\s*5[^.]{0,40}(the\s+)?current\s+(active\s+)?(edition|version|publication)"
    r"|current\s+(edition|version|publication)\s+is\s+(<[^>]*>)?\s*BMP\s*5",
    re.I)


def gate_bmp():
    g = "BMP"
    frags, raws = {}, {}
    for fn, anch in BMP_CARDS:
        c = card(read(fn), anch)
        check(g, "B-00:%s#%s" % (fn, anch), c is not None, "card extracted")
        if c is None:
            return
        key = "%s#%s" % (fn.replace(".html", ""), anch)
        frags[key] = flat(c)
        raws[key] = c

    for key, f in frags.items():
        # 1. no positive teaching that BMP5 is current - element-scoped, so a
        #    correct neighbouring bullet cannot excuse a defective one.  The
        #    element's OWN negation ("do not present BMP5 as current") is
        #    allowed, because that is the teaching, not the defect.
        offenders = []
        for e in elements(raws[key]):
            m = CURRENT_CLAIM.search(e)
            if not m:
                continue
            # The exemption must ATTACH to the claim, not merely co-occur in
            # the element.  A blanket element-level exemption lets a card
            # assert "BMP5 is the current edition" and be excused by an
            # unrelated "do not offer BMP5 as current" further down the same
            # bullet - which is exactly what the mutation suite proved.
            lead = e[max(0, m.start() - 70):m.end()]
            if re.search(r"not\s+BMP\s*5|do not present|do not offer|do not quote"
                         r"|has been superseded|is not the current|no longer|never", lead, re.I):
                continue
            offenders.append(e[:110])
        check(g, "B-01:" + key, not offenders,
              "%s: no element teaches BMP5 as the current publication%s"
              % (key, "" if not offenders else " -> %r" % offenders[0]))

        # 2. correct edition label, and never a "2026 edition"
        check(g, "B-02:" + key, "1st Edition" in f or "1st Edition (2025)" in f,
              "%s: current publication labelled 1st Edition" % key)
        bad = re.search(r"(the\s+)?2026\s+edition|2nd\s+edition|second\s+edition|BMP\s*MS\s*2", f, re.I)
        if bad and re.search(r"never|not\b|no second", f[max(0, bad.start() - 80):bad.start() + 30], re.I):
            bad = None
        check(g, "B-03:" + key, bad is None, "%s: no false second/2026 edition wording" % key)

        # 3. no unsupported company-specific claim
        # "Maersk Alabama" is a VESSEL name in a casualty reference, not a
        # company-practice claim; strip that token before testing.
        company = re.sub(r"(MV\s+)?Maersk\s+Alabama", " ", f)
        check(g, "B-04:" + key, not re.search(r"Maersk", company, re.I),
              "%s: no company-specific operational claim" % key)

    # 4. threat-based muster distinction survives where the threat is hull breach
    for key in ("QB4_H#q2", "QB9_A#q9", "QB9_B#q5"):
        f = frags[key]
        # the pairing must be explicit: the hull-breach threat and the
        # above-waterline location have to be stated together, and the citadel
        # has to be named as the OTHER branch.
        paired = [e for e in elements(raws[key])
                  if re.search(r"WBIED|UAV|hull breach", e, re.I)
                  and re.search(r"above the waterline", e, re.I)
                  and re.search(r"citadel", e, re.I)]
        ok = bool(paired)
        check(g, "B-05:" + key, ok,
              "%s: citadel vs above-waterline muster point distinguished by threat" % key)
    # and it must not be flattened back into "citadel for everything"
    for key in ("QB9_A#q9", "QB9_B#q5"):
        f = frags[key]
        unscoped = [e for e in elements(raws[key])
                    if "steering gear room" in e
                    and not re.search(r"boarding|intruder|piracy", e, re.I)]
        ok = not unscoped
        check(g, "B-06:" + key,
              ok, "%s: a steering-gear-room citadel is scoped to a boarding threat" % key)

    # 5. no automatic SSAS activation on area entry
    f = frags["QB9_A#q9"]
    bad = re.search(r"activation of the Ship Security Alert System", f, re.I)
    if bad and re.search(r"not its activation|never something you do", f[bad.start():bad.start() + 260], re.I):
        bad = None
    check(g, "B-07", bad is None, "QB9_A#q9: SSAS is not activated merely on entering an area")
    check(g, "B-08", re.search(r"tested", f, re.I) is not None,
          "QB9_A#q9: SSAS pre-entry action is testing")

    # 6. citadel endurance: BMP MS guidance, not an invented 72-hour standard
    f = frags["QB9_B#q5"]
    bad72 = None
    for m in re.finditer(r"72[\s-]*hours?", f, re.I):
        ctx = f[max(0, m.start() - 140):m.end() + 140]
        if not re.search(r"no 72|not a 72|there is no|invented", ctx, re.I):
            bad72 = m
            break
    check(g, "B-09", bad72 is None,
          "QB9_B#q5: no invented 72-hour citadel baseline (only its explicit negation)")
    check(g, "B-10", re.search(r"3-5 days|3&ndash;5 days|3–5 days", f) is not None,
          "QB9_B#q5: BMP MS 3-5 day citadel guidance taught instead")

    # 7. no invented SOLAS fire-main figure
    check(g, "B-11", not re.search(r"6\s*Bar\s*Pressure", f, re.I),
          "QB9_B#q5: no invented 6-bar fire-main minimum")
    check(g, "B-12", "0.27 N/mm" in f and "0.25 N/mm" in f and "II-2/10.2.1.6" in f,
          "QB9_B#q5: actual SOLAS II-2/10.2.1.6 hydrant pressures taught")

    # 8. machinery-space escape grounded in SOLAS II-2/13, not the LSA Code
    bad = re.search(r"Life-Saving Appliance \(LSA\) code, mandatory emergency escape", f, re.I)
    check(g, "B-13", bad is None, "QB9_B#q5: LSA Code no longer the escape-route authority")
    check(g, "B-14", "II-2/13" in f, "QB9_B#q5: SOLAS II-2/13 cited for means of escape")

    # 9. XI-2/8 is not a CE machinery-bypass authority
    f = frags["QB4_B#q16"]
    bad = re.search(r"fully justified under the Master's overriding authority", f, re.I)
    check(g, "B-15", bad is None, "QB4_B#q16: alarm-bypass no longer 'fully justified' doctrine")
    check(g, "B-16", re.search(r"XI-2/8", f) is not None
          and near(f, "XI-2/8", r"Do not claim|confers nothing|Master", 400),
          "QB4_B#q16: XI-2/8 explicitly disclaimed as CE authority")
    check(g, "B-17", re.search(r"maximum speed|full speed", f, re.I) is not None,
          "QB4_B#q16: the legitimate maintain-propulsion point survives")

    # 10. publisher attribution
    f = frags["QB4_B#q16"]
    check(g, "B-18", not re.search(r"BIMCO, ICS, IMO", f),
          "QB4_B#q16: IMO no longer listed as a BMP publisher")
    check(g, "B-19", "IMCA" in f and "INTERTANKO" in f,
          "QB4_B#q16: six-publisher industry list present")


# ------------------------------------------------------------ D. Artefacts
def gate_artefacts():
    g = "ARTEFACT"
    cite = scaf = foot = 0
    files = sorted(n for n in os.listdir(QB) if n.endswith(".html"))
    for name in files:
        t = read(name)
        cite += len(re.findall(r"\[cite:", t))
        scaf += len(re.findall(r"REGULATORY REFERENCE BOX", t))
        foot += len(re.findall(r"CORRECTION FOOTER:", t))
    check(g, "D-01", cite == 0, "no raw [cite: generation residue anywhere in meoclass1 (%d)" % cite)
    check(g, "D-02", scaf == 0, "no plain-text scaffold reg-box block survives (%d)" % scaf)
    check(g, "D-03", foot == 0, "no scaffold CORRECTION FOOTER stamp survives (%d)" % foot)

    # removing the scaffold must not have cost a card its real reg-box or CE tip
    for name in ("QB3_C.html", "QB8_A.html", "QB9_A.html", "QB9_B.html"):
        t = read(name)
        cards = re.findall(r'class="q-card"', t)
        rb = re.findall(r'class="reg-box"', t)
        ct = re.findall(r'class="ce-tip"', t)
        o, c = len(re.findall(r"<div\b", t)), len(re.findall(r"</div>", t))
        check(g, "D-04:" + name, len(rb) >= len(cards),
              "%s: every card retains a rendered reg-box (%d cards, %d reg-boxes)" % (name, len(cards), len(rb)))
        check(g, "D-05:" + name, len(ct) >= len(cards),
              "%s: every card retains a rendered CE tip (%d cards, %d tips)" % (name, len(cards), len(ct)))
        check(g, "D-06:" + name, o == c,
              "%s: <div> balanced after excision (%d/%d)" % (name, o, c))
        check(g, "D-07:" + name,
              len(re.findall(r"<details", t)) == len(re.findall(r"</details>", t)),
              "%s: <details> balanced after excision" % name)


def main():
    gate_grain()
    gate_cii()
    gate_bmp()
    gate_artefacts()
    fails = [r for r in RESULTS if not r[2]]
    width = max(len(r[1]) for r in RESULTS)
    for gate, cid, ok, detail in RESULTS:
        print("%-9s %-*s %s  %s" % (gate, width, cid, "PASS" if ok else "FAIL", detail))
    print("-" * 72)
    print("%d checks, %d PASS, %d FAIL" % (len(RESULTS), len(RESULTS) - len(fails), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
