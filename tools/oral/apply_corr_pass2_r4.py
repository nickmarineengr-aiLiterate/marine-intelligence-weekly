#!/usr/bin/env python3
"""Pass-2 remediation round 4 -- correcting my own over-correction.

A fourth independent review found that the insurance framing this batch pushed
across six cards is WRONG IN THE OTHER DIRECTION, and that QB1_F#q7 - the card
round 3 edited - already carried the right answer three paragraphs above the
edit:

  Institute Time Clauses - Hulls (1/11/95), cl. 4.2: the insurance
  "terminates automatically" on change of Classification Society, or change,
  suspension, discontinuance, withdrawal or expiry of Class - deferred until
  arrival at the next port if the vessel is at sea, and disapplied where the
  class event resulted from insured damage and the Society approves sailing.

So the original cards saying "suspension voids insurance" were CRUDE, not
simply false. What was false was attributing that consequence to IACS PR1C,
which contains no insurance provision at all. Rounds 1-3 fixed the attribution
and then overshot, replacing it with "cover may be prejudiced, not
automatically void" - which teaches a candidate that hull cover survives a
class suspension. On ITC terms it does not.

The accurate teaching, applied at every site this batch touched:
  * PR1C is silent on insurance - so do not cite PR1C for it;
  * the consequence is CONTRACTUAL, and under the standard hull classification
    clause it is automatic termination, with the two qualifications above;
  * P&I cover is conditional on class under club rules.

Also closed here, all found by the fourth review:
  QB1_C#q6            a Trap-Question model answer still said "Unreported hull
                      damage invalidates class automatically" - two paragraphs
                      below the bullet round 3 corrected to "not automatic".
  QB1_K_CheatSheet    "Overdue -> suspension -> statutory/insurance cascade",
                      a second derived surface with the same defect as the P0.
  QB1_I#q6            "11-12 Members" - the exact hedge trap 120 was written to
                      kill, invisible to the IACS record's declared search
                      terms because it is hyphenated.
  QB4_A#q9 footer     asserted that the PR No.1/No.3 entries were "left as they
                      stand and are recorded as unverified". Round 3 replaced
                      both, three lines above. A footer that describes an edit
                      that did not happen is a candidate-facing falsehood.
  QB4_A#q9 table      round 3's own new "Recommendation (Memo)" row said a
                      thing with "no due date attached" can go "overdue", and
                      contradicted four sibling surfaces that call a
                      Recommendation non-binding. Reverted to the accurate
                      distinction.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
QB = HERE.parent.parent / "meoclass1"

ITC = ("Institute Time Clauses &ndash; Hulls (1/11/95) cl. 4.2 terminates hull cover "
       "<strong>automatically</strong> on suspension, discontinuance or withdrawal of class "
       "&mdash; deferred until arrival at the next port if the vessel is at sea, and "
       "disapplied where the class event resulted from insured damage and the Society "
       "approves sailing. P&amp;I cover is conditional on class under club rules. So the "
       "consequence is real, and it comes from the POLICY, not from PR1C, which contains no "
       "insurance provision at all.")

EDITS = [
    # ---- QB4_C#q5, three sites ------------------------------------------
    ("QB4_C.html",
     "Say &quot;our class warranty is breached and cover may be prejudiced&quot;, not "
     "&quot;insurance is void&quot;.",
     "Attribute it correctly: " + ITC, 1),

    ("QB4_C.html",
     "Our class warranty is also breached, so cover may be prejudiced.",
     "Cover is also affected, and by its own terms rather than by PR1C: on Institute Time "
     "Clauses &ndash; Hulls (1/11/95) cl. 4.2 hull cover terminates automatically on "
     "suspension or withdrawal of class, deferred to the next port if we are at sea.", 1),

    ("QB4_C.html",
     "On insurance I would say our class warranty is breached and cover may be prejudiced, "
     "rather than claiming that cover is void.",
     "On insurance I would not cite PR1C, sir &mdash; it has no insurance provision. I would "
     "cite the policy: under ITC-Hulls (1/11/95) cl. 4.2 hull cover terminates automatically "
     "on suspension or withdrawal of class, deferred until we reach the next port.", 1),

    # ---- QB4_A#q9, three sites -------------------------------------------
    ("QB4_A.html",
     "Our class warranty is breached, so cover may be prejudiced; PR1C itself says nothing "
     "about insurance.",
     "Cover is affected by the policy&#x27;s own classification clause &mdash; ITC-Hulls "
     "(1/11/95) cl. 4.2 terminates hull cover automatically on suspension or withdrawal "
     "&mdash; and not by PR1C, which says nothing about insurance.", 1),

    ("QB4_A.html",
     "so loss of class breaches it and cover may be prejudiced &mdash; the consequence is "
     "whatever the policy and its governing law provide. PR1C contains no insurance provision "
     "at all, so do not tell an examiner that cover automatically ends.",
     "and the standard hull wording goes further than a warranty: " + ITC, 1),

    ("QB4_A.html",
     "our class warranty is breached so cover may be prejudiced, and the ship cannot trade.",
     "hull cover terminates automatically under ITC-Hulls cl. 4.2 &mdash; from the policy, "
     "not from PR1C &mdash; and the ship cannot trade.", 1),

    # ---- the two cheat sheets --------------------------------------------
    ("QB4_A_CheatSheet.html",
     "Class warranty breached, so cover may be prejudiced &mdash; PR1C says nothing about "
     "insurance",
     "Hull cover terminates automatically: ITC-Hulls (1/11/95) cl. 4.2, deferred to next port "
     "if at sea &mdash; from the POLICY, not PR1C, which says nothing about insurance", 1),

    ("QB1_K_CheatSheet.html",
     "Overdue &rarr; suspension &rarr; statutory/insurance cascade.",
     "Overdue survey &rarr; automatic suspension (PR1C A.1.1&ndash;A.1.3). Overdue CoC &rarr; "
     "suspension <em>procedure</em> (A.2.1). Then: certain statutory certs implicitly "
     "invalidated (B.1.3), and hull cover terminates automatically under ITC-Hulls cl. 4.2.",
     1),

    # ---- QB1_C#q6, two sites ---------------------------------------------
    ("QB1_C.html",
     "Hull &amp; Machinery and P&amp;I cover is written subject to a class warranty, so loss "
     "of class breaches it and cover may be prejudiced &mdash; PR1C contains no insurance "
     "provision, and cover is not automatically void.",
     "On insurance, cite the policy rather than PR1C: " + ITC, 1),

    ("QB1_C.html",
     "invalidates class automatically",
     "puts the vessel into a suspension procedure under PR1C A.2.1 once the rectification "
     "date passes &mdash; and, if it is an overdue periodical survey rather than a condition "
     "of class, suspends class automatically under A.1.1&ndash;A.1.3", 1),

    # ---- QB1_F#q7, both copies -------------------------------------------
    ("QB1_F.html",
     "which breaches the class warranty in the ship's cover, so cover may be prejudiced, and "
     "gives Port State Control legal grounds to detain. See section 4 of this card for the "
     "full ladder; cover is not automatically void.",
     "and on ITC-Hulls (1/11/95) cl. 4.2 hull cover then terminates automatically, deferred "
     "until arrival at the next port if the vessel is at sea. Port State Control also has "
     "legal grounds to detain. See section 4 of this card for the full ladder.", 2),

    # ---- QB1_G#q36 --------------------------------------------------------
    ("QB1_G.html",
     "Hull and P&amp;I cover is written subject to a class warranty, so loss of class breaches "
     "it and cover may be prejudiced; charterers will normally have a class or "
     "trading-certificate warranty too. Do not say cover and the charter are automatically "
     "void &mdash; PR1C contains no insurance provision, and the consequence is whatever each "
     "contract provides.",
     "On insurance, cite the policy and not PR1C: ITC-Hulls (1/11/95) cl. 4.2 terminates hull "
     "cover automatically on suspension or withdrawal of class, deferred to the next port if "
     "at sea. Charterers will normally have their own class or trading-certificate warranty, "
     "and that consequence depends on the charter, so do not lump the two together.", 1),

    ("QB1_G.html",
     "loss of class breaches it and cover may be prejudiced &mdash; it is not automatically "
     "void, and the charter consequence depends on that contract&rsquo;s own warranty.",
     "hull cover terminates automatically under ITC-Hulls cl. 4.2, while the charter "
     "consequence depends on that contract&rsquo;s own warranty.", 1),

    # ---- QB1_I#q6 ---------------------------------------------------------
    ("QB1_I.html",
     "11-12 Members",
     "12 Members", 1),

    # ---- QB4_A#q9 table row: revert round 3's own error -------------------
    ("QB4_A.html",
     "Recommendation (Memo)</td><td>Advisory</td><td>No due date attached, so no immediate "
     "class consequence &mdash; but PR1C covers <em>recommendations</em> going overdue as well "
     "as conditions of class, so do not call it consequence-free",
     "Recommendation (Memo)</td><td>No &mdash; advisory</td><td>No class consequence; action "
     "as practical. (Beware the vocabulary: some societies use &ldquo;Recommendation&rdquo; as "
     "a synonym for Condition of Class &mdash; IACS PR 35 is titled "
     "&ldquo;Recommendations/Conditions of Class&rdquo; &mdash; so confirm which sense the "
     "examiner means)", 1),

    # ---- QB4_A#q9 footer: it describes an edit that did not happen --------
    ("QB4_A.html",
     "The PR No.1 and PR No.3 entries are left as they stand and are "
     "recorded as unverified &mdash; no replacement number is asserted. · v1.1",
     "PR No.1 and PR No.3 were both replaced: the IACS PR index records PR 1 as Deleted and "
     "PR 3 as Transparency of Classification and Statutory Information, and the instrument "
     "this card described is PR 35, Procedure for Imposing and Clearing "
     "Recommendations/Conditions of Class. · v1.3, 7 Sep 2026: the notation table still taught "
     "an overdue Condition of Class as suspending class outright; the Numbers line "
     "generalised A.1.2/A.1.3&rsquo;s three-month window to A.1, where A.1.1 suspends from the "
     "certificate expiry date; and the insurance limb has been re-attributed from a bare "
     "class warranty to ITC-Hulls (1/11/95) cl. 4.2, under which hull cover terminates "
     "automatically. · v1.1", 1),
]


def main() -> int:
    pages: dict[str, str] = {}
    for name, _, _, _ in EDITS:
        if name not in pages:
            pages[name] = (QB / name).read_text(encoding="utf-8", newline="")

    errors, applied = [], 0
    for name, old, new, expect in EDITS:
        text = pages[name]
        # These pages mix "&mdash;" with a literal em dash, and "&rarr;" with a
        # literal arrow, in the same file. Try the entity form first, then the
        # literal one, rather than guessing per site.
        if text.count(old) != expect:
            for a, b in (("&mdash;", "—"), ("&ndash;", "–"),
                         ("&rarr;", "→"), ("&rsquo;", "’"),
                         ("&#x27;", "'")):
                cand = old.replace(a, b)
                if text.count(cand) == expect:
                    old = cand
                    break
        n = text.count(old)
        if n != expect:
            errors.append("%s: anchor occurs %d times, expected %d: %.70s"
                          % (name, n, expect, old))
            continue
        pages[name] = text.replace(old, new)
        applied += n

    if errors:
        print("ABORTED - nothing written.")
        for e in errors:
            print("  " + e)
        return 1

    for name, text in pages.items():
        (QB / name).write_text(text, encoding="utf-8", newline="")
    print("Applied %d replacements across %d files." % (applied, len(pages)))
    for n in sorted(pages):
        print("  meoclass1/%s" % n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
