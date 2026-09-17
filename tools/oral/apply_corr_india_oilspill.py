#!/usr/bin/env python3
"""CORR-INDIA-OILSPILL-REGULATORY-AUDIT-20260917 - four India oil-spill propositions.

One governed audit batch, four separate propositions. Each was verified at an
official source before any edit; each edit below names the proposition it
serves, so the diff reads proposition by proposition.

  A_TIER - NOSDCP tier tonnage bands. QB9_A Q8 and oralnotes/simon-notes-p3
    taught Tier 1 <700 t, Tier 2 700-10,000 t, Tier 3 >10,000 t. The NOSDCP
    plan text is not served by the Coast Guard any more and is not held. The
    official Coast Guard material that IS held grades the tiers by capability
    ("beyond their response capabilities that is beyond Tier-1", ICG OSD
    Policy 2025, and Tier-1 / Tier-2 responsibility by area), and its only
    700-ton figure is a dispersant-stocking RISK-EXPOSURE example. The bands
    are UNSUPPORTED: removed, not replaced by other figures.

  B_OPRC_DATE - India and OPRC 1990. simon-notes-p3 said "India ratified/
    acceded 1993 (verify exact year before quoting)". IMO Status of Treaties,
    26 August 2026: India (accession) 17 November 1997, entry into force
    17 February 1998. 1993 is the Government of India's approval of NOSDCP.

  C_BUNKERS_STATUS - India and the Bunkers Convention 2001. IMO Status of
    Treaties, 26 August 2026: India is NOT listed as a Contracting State.
    Separately, the Merchant Shipping Act, 2025 (in force 15 March 2026),
    Part IX Chapter IV, ss.196-210, imposes bunker-oil pollution liability,
    compulsory insurance above 1,000 GT (s.204), direct action (s.205(3)) and
    a certificate to enter or leave an Indian port (ss.206-207) as DOMESTIC
    law. Two sites blurred the two: QB1_A Q4's reg-box (with an unverified
    "replaces the 1958 Act equivalent") and a QB1_B cheat-sheet trap.

  D_PANS - Pre-Arrival Notification of Security. DG Shipping (now DGMA)
    Merchant Shipping Notice 13 of 2024, dated 3 September 2024, still listed
    by DGMA: submitted to the port and the regional authority AT LEAST 96
    hours before arrival; if the voyage is shorter than 96 hours, within 2
    hours of departure from the last port; for listed ship types; the 96-hour
    period comes from the national Rules (s.29 of the MS (Ships and Port
    Facility Security) Rules, 2024, saved by MSA 2025 s.324(2)(a)). QB1_A
    Q14 said "approx. 96 hours"; QB1_A Q18 attributed a 96-hour notice to
    SOLAS XI-2 / ISPS and sent PANS to a "DGS port office".

Always derives from BASELINE, never from the working tree, so a re-run
reproduces the authorised bytes. Cards on QB1_A and its SQ twin are asserted
byte-identical where the twin carries an answer (q4, q14); SQ q18 is a locked
teaser and is asserted untouched.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

#: origin/main when this correction was authored; the pre-edit state it applies to.
BASELINE = "91f71e8"

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from validate_batch_b import card_digests  # noqa: E402

STAMP_TAG = "India oil-spill regulatory audit"

# ---------------------------------------------------------------------------
# D_PANS - QB1_A Q14 (numbers box) and its SQ twin
# ---------------------------------------------------------------------------
Q14_EDITS = [
    ("D_PANS",
     " · Pre-arrival security notice (PANS, related context) ≈ <strong>96 hours</strong> for India.</div>",
     " · PANS — Pre-Arrival Notification of Security (India's port-entry security report, not a pollution report): "
     "at least <strong>96 hours</strong> before arrival, or within <strong>2 hours</strong> of departure from the last port "
     "if the voyage is shorter than 96 hours.</div>"),
    ("STAMP",
     '<span class="q-version">QB1 · Q14 · v1.1 — corrected 16 Sep 2026 (NOSDCP authority correction)',
     '<span class="q-version">QB1 · Q14 · v1.2 — corrected 17 Sep 2026 (%s): PANS line restated as '
     'Pre-Arrival Notification of Security at least 96 hours before arrival, or within 2 hours of departure '
     'when the voyage is shorter, replacing &quot;approximately 96 hours&quot;; earlier '
     'v1.1 — corrected 16 Sep 2026 (NOSDCP authority correction)' % STAMP_TAG),
]

# ---------------------------------------------------------------------------
# C_BUNKERS_STATUS - QB1_A Q4 (reg-box) and its SQ twin
# ---------------------------------------------------------------------------
Q4_EDITS = [
    ("C_BUNKERS_STATUS",
     '<span class="reg-desc">In force 15 March 2026; domestic implementation of the Bunker Convention '
     '(replaces the 1958 Act equivalent).</span>',
     '<span class="reg-desc">In force 15 March 2026; India\'s domestic bunker-oil pollution liability regime, '
     'modelled on the Bunker Convention — shipowner liability, compulsory insurance above 1,000 GT, direct action '
     'against the insurer, and a certificate carried to enter or leave an Indian port (ss.198, 204, 205, 206–207). '
     'India is not a Party to the Bunker Convention itself.</span>'),
    ("STAMP",
     '<span class="q-version">QB1 · Q4 · v1.1 — corrected 15 Jul 2026: Bunker Convention domestic implementation '
     'updated to MS Act 2025, Part IX Ch IV (Sec 196-210)</span>',
     '<span class="q-version">QB1 · Q4 · v1.2 — corrected 17 Sep 2026 (%s): India\'s treaty status stated — '
     'not a Party to the Bunker Convention 2001 — and the Merchant Shipping Act, 2025, Part IX Ch IV described '
     'as India\'s domestic bunker-liability regime; the unverified reference to a 1958 Act equivalent removed; '
     'earlier v1.1 — corrected 15 Jul 2026: MS Act 2025, Part IX Ch IV (Sec 196-210)</span>' % STAMP_TAG),
]

# ---------------------------------------------------------------------------
# D_PANS - QB1_A Q18 (gated only; the SQ copy is a locked teaser)
# ---------------------------------------------------------------------------
Q18_EDITS = [
    ("D_PANS",
     "<p>FAL facilitates; ISPS secures. The balance is maintained through advance notification requirements: "
     "<strong>96-hour advance arrival notification</strong> (SOLAS XI-2 / ISPS Code) with crew and cargo details "
     "feeds port state security assessments before the ship arrives.</p>",
     "<p>FAL facilitates; ISPS secures. The balance is maintained through advance notification: "
     "<strong>SOLAS regulation XI-2/9.2</strong> lets a Contracting Government require a ship intending to enter "
     "its port to provide security-related information <strong>before entry</strong> — its ISSC, current security "
     "level, security levels at recent port calls, any additional security measures, and cargo and crew details — "
     "so the port State can assess the ship before it arrives. India's own notice period is set by its national "
     "rules (below).</p>"),
    ("D_PANS",
     "<p>India-specific: <strong>PANS (Pre-Arrival Notification of Security)</strong> — ships notify DGS port "
     "office <strong>96 hours before arrival</strong>, containing crew details, cargo, voyage history, security "
     "status.</p>",
     "<p>India-specific: <strong>PANS (Pre-Arrival Notification of Security)</strong>, under DG Shipping (now DGMA) "
     "Merchant Shipping Notice 13 of 2024 — submitted to the <strong>port of call and its Port Facility Security "
     "Officer</strong> and to the <strong>regional authority</strong> the notice lists for that coast (an Indian "
     "Navy Joint Operations Centre or a Coast Guard MRCC) <strong>at least 96 hours before arrival</strong>; if "
     "the voyage is <strong>shorter than 96 hours</strong>, <strong>within 2 hours of departure</strong> from the "
     "last port. It applies to passenger ships and high-speed passenger craft, cargo ships and high-speed craft of "
     "<strong>500 GT and above</strong>, mobile offshore drilling units, pleasure yachts and sailing vessels, on "
     "international voyages to Indian ports and when trading on the coast between Indian ports. The form carries "
     "the ship's ISSC and security level, recent port calls and ship-to-ship activities, a cargo description with "
     "the <strong>Dangerous Goods Manifest (FAL Form 7)</strong>, and the <strong>Crew List (FAL Form 5)</strong>."
     "</p>"),
    ("D_PANS",
     '<div class="reg-item"><span class="reg-code">SOLAS XI-2 / ISPS Code</span><span class="reg-desc">96-hour '
     'advance security notification — security layer to FAL facilitation</span></div>',
     '<div class="reg-item"><span class="reg-code">SOLAS XI-2/9.2 / ISPS Code</span><span class="reg-desc">'
     'Security-related information a port State may require before a ship enters its port — the security layer '
     'to FAL facilitation</span></div>'),
    ("D_PANS",
     '<div class="reg-item"><span class="reg-code">DGS MS Notice — PANS</span><span class="reg-desc">India: '
     'Pre-Arrival Notification of Security — 96-hour submission to DGS</span></div>',
     '<div class="reg-item"><span class="reg-code">MS Notice 13 of 2024 — PANS</span><span class="reg-desc">'
     'India: Pre-Arrival Notification of Security — to the port of call and the regional authority at least '
     '96 hours before arrival, or within 2 hours of departure when the voyage is shorter; the 96-hour period is '
     'set by the Merchant Shipping (Ships and Port Facility Security) Rules, 2024</span></div>'),
    ("D_PANS",
     "PANS: India requires 96-hour pre-arrival security notification — this is submitted by the master/agent but "
     "the CE's DG data feeds directly into it.</div>",
     "PANS: India requires the Pre-Arrival Notification of Security at least 96 hours before arrival — or within "
     "2 hours of departure when the voyage is shorter than 96 hours; the master or agent submits it, but the CE's "
     "DG data feeds directly into it through the attached DG Manifest (FAL Form 7).</div>"),
    ("D_PANS",
     "Typical security notice = <strong>96-hour PANS</strong> pre-arrival notification for Indian ports · ",
     "India PANS = at least <strong>96 hours</strong> before arrival (voyage shorter than 96 hours → within "
     "<strong>2 hours</strong> of departure) · "),
    ("D_PANS",
     "  ↓ feeds into MSW (mandatory 1 Jan 2024) + PANS (96h, India)</div>",
     "  ↓ feeds into MSW (mandatory 1 Jan 2024) + India PANS (≥96 h before arrival; short voyage: within 2 h of "
     "departure)</div>"),
    ("STAMP",
     '<span class="q-version">QB1 · Q18 · v1.0</span>',
     '<span class="q-version">QB1 · Q18 · v1.1 — corrected 17 Sep 2026 (%s): PANS restated from MS Notice 13 '
     'of 2024 — at least 96 hours before arrival, or within 2 hours of departure when the voyage is shorter, '
     'submitted to the port of call and the regional Navy or Coast Guard authority rather than a &quot;DGS port '
     'office&quot;; the 96-hour period attributed to India\'s national rules rather than to SOLAS XI-2 / ISPS'
     '</span>' % STAMP_TAG),
]

# ---------------------------------------------------------------------------
# A_TIER - QB9_A Q8
# ---------------------------------------------------------------------------
QB9A_Q8_EDITS = [
    ("A_TIER",
     "<li><strong>Tiered Response Structure:</strong> It organizes oil spills into three logical scales to "
     "optimize resources:</li>\n"
     "<li><em>Tier 1 (Local):</em> Small operational spills (&lt;700 tonnes) managed directly by the local port "
     "facility or individual ship operator.</li>\n</ul>\n<ul>\n"
     "<li><em>Tier 2 (Regional):</em> Medium spills (700 to 10,000 tonnes) requiring regional coordination and "
     "mobilization of district-level Coast Guard assets.</li>\n</ul>\n<ul>\n"
     "<li><em>Tier 3 (National):</em> Catastrophic disasters (&gt;10,000 tonnes) requiring the activation of the "
     "full national contingency network, international assets, and multi-agency cooperation.</li>",
     "<li><strong>Tiered Response Structure:</strong> It grades the response by the capability the spill needs, "
     "not by fixed tonnage bands:</li>\n"
     "<li><em>Tier 1 (Local):</em> within the responsible agency's own resources — the port within port limits, "
     "the oil-handling agency within 500 m of its installation, the Indian Coast Guard elsewhere in the maritime "
     "zones — with the ship working its SOPEP.</li>\n</ul>\n<ul>\n"
     "<li><em>Tier 2 (Regional):</em> beyond local capability, escalated to Indian Coast Guard response in the "
     "Maritime Zones of India.</li>\n</ul>\n<ul>\n"
     "<li><em>Tier 3 (National):</em> beyond regional capability — national mobilisation and, where needed, "
     "international assistance.</li>\n</ul>\n<ul>\n"
     "<li><em>No tonnage limits:</em> the Coast Guard material held grades the tiers by capability and gives no "
     "tier tonnage bands; its 700-tonne figure is a dispersant-stocking example of risk exposure, not a tier "
     "definition. Verify against the current NOSDCP text before quoting any figure.</li>"),
    ("A_TIER",
     "<li><strong>Tier 3 (&gt;10,000 Tonnes):</strong> The volume threshold that classifies a marine oil spill as "
     "a national disaster under the NOSDCP.</li>",
     "<li><strong>NOSDCP Tiers 1 / 2 / 3:</strong> local, regional (Coast Guard) and national response, graded by "
     "the capability the spill needs — no tier tonnage threshold is quoted.</li>"),
    ("STAMP",
     '<span class="q-version">QB9_A · Q8 · v1.1</span>',
     '<span class="q-version">QB9_A · Q8 · v1.2 — corrected 17 Sep 2026 (%s): NOSDCP tiers restated by '
     'response capability; unsupported fixed tonnage bands removed</span>' % STAMP_TAG),
]

# ---------------------------------------------------------------------------
# A_TIER and B_OPRC_DATE - oralnotes/simon-notes-p3.html, note n5
# ---------------------------------------------------------------------------
NOTES_EDITS = [
    ("A_TIER",
     "        <h4>Oil Spill Volume Tiers</h4>",
     "        <h4>Tiered Response — by Capability</h4>"),
    ("A_TIER",
     "          Tier 1: Small localised spills up to <strong>700 MT</strong> — port/facility level response<br>\n"
     "          Tier 2: Regional incidents up to <strong>10,000 MT</strong> — ICG regional coordination<br>\n"
     "          Tier 3: National disaster exceeding <strong>10,000 MT</strong> — full national mobilisation\n"
     "        </div>",
     "          Tier 1: within the responsible agency's own resources — port within port limits, oil-handling "
     "agency within 500 m, Indian Coast Guard elsewhere in the maritime zones<br>\n"
     "          Tier 2: beyond local capability — Indian Coast Guard response in the Maritime Zones of India<br>\n"
     "          Tier 3: beyond regional capability — national mobilisation, with international assistance where "
     "needed\n"
     "        </div>\n"
     "        <p><em>No tonnage limits.</em> The Coast Guard material held grades the tiers by capability and gives "
     "no tier tonnage bands; its 700-tonne figure is a dispersant-stocking example of risk exposure, not a tier "
     "definition. Verify against the current NOSDCP text before quoting any figure.</p>"),
    ("A_TIER",
     "Know the three tiers by volume.",
     "Know the three tiers by response capability, not by tonnage."),
    ("B_OPRC_DATE",
     "— basis for national contingency plans; India ratified/acceded 1993 (verify exact year before quoting)</span>",
     "— basis for national contingency plans; India acceded on <strong>17 November 1997</strong>, in force for "
     "India <strong>17 February 1998</strong> (IMO Status of Treaties). 1993 is the year the Government of India "
     "approved NOSDCP, not India's OPRC date</span>"),
]

# ---------------------------------------------------------------------------
# C_BUNKERS_STATUS - QB1_B_CheatSheet.html (no q-card)
# ---------------------------------------------------------------------------
CHEAT_EDITS = [
    ("C_BUNKERS_STATUS",
     "HNS Fund cannot pay for Indian waters spill today — 2010 Protocol not in force. Candidates confuse with "
     "Bunker Convention 2001 (IS in force).</div>",
     "HNS Fund cannot pay for Indian waters spill today — 2010 Protocol not in force. Candidates confuse with "
     "Bunker Convention 2001, which IS in force internationally (since 21 Nov 2008) — but India is not a Party; "
     "bunker-spill liability in Indian waters rests on the Merchant Shipping Act, 2025, Part IX Ch IV.</div>"),
]


def card_bounds(page: str, anchor: str) -> tuple[int, int]:
    """[start, end) of the balanced q-card div carrying id=anchor."""
    at = page.find('<div class="q-card" id="%s"' % anchor)
    assert at >= 0, "card %s not found" % anchor
    assert page.count('<div class="q-card" id="%s"' % anchor) == 1, "card %s not unique" % anchor
    depth, pos = 0, at
    tok = re.compile(r"<div\b|</div>")
    while True:
        m = tok.search(page, pos)
        assert m, "unbalanced card %s" % anchor
        depth += -1 if m.group(0) == "</div>" else 1
        pos = m.end()
        if depth == 0:
            return at, pos


def apply_edits(text: str, edits, where: str) -> str:
    for prop, old, new in edits:
        n = text.count(old)
        assert n == 1, "%s [%s] matched %d times: %r" % (where, prop, n, old[:80])
        text = text.replace(old, new)
    return text


def baseline_text(rel: str) -> str:
    raw = subprocess.run(["git", "show", "%s:%s" % (BASELINE, rel)],
                         cwd=REPO, capture_output=True, check=True).stdout
    assert b"\r\n" not in raw, "%s is not LF-only" % rel
    return raw.decode("utf-8")


def write(rel: str, text: str) -> None:
    (REPO / rel).write_bytes(text.encode("utf-8"))


def fix_cards(rel: str, plan: dict, expect_moved: list[str]) -> tuple[dict, dict]:
    page = baseline_text(rel)
    before = card_digests(page)
    for anchor, edits in plan.items():
        a, b = card_bounds(page, anchor)
        page = page[:a] + apply_edits(page[a:b], edits, "%s#%s" % (rel, anchor)) + page[b:]
    after = card_digests(page)
    moved = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    assert moved == sorted(expect_moved), "unexpected cards moved in %s: %s" % (rel, moved)
    write(rel, page)
    for k in expect_moved:
        print("%s#%s %s -> %s" % (rel, k, before[k][:12], after[k][:12]))
    return before, after


def main() -> int:
    gated = fix_cards("meoclass1/QB1_A.html",
                      {"q4": Q4_EDITS, "q14": Q14_EDITS, "q18": Q18_EDITS}, ["q4", "q14", "q18"])
    twin = fix_cards("SQ/QB1_A.html", {"q4": Q4_EDITS, "q14": Q14_EDITS}, ["q4", "q14"])
    for k in ("q4", "q14"):
        assert gated[0][k] == twin[0][k] and gated[1][k] == twin[1][k], \
            "SQ twin %s not byte-identical to the gated copy" % k
    assert twin[0]["q18"] == twin[1]["q18"], "SQ q18 teaser must be untouched"
    print("SQ twin identical to gated copy for q4 and q14; SQ q18 teaser untouched")

    fix_cards("meoclass1/QB9_A.html", {"q8": QB9A_Q8_EDITS}, ["q8"])

    for rel, edits in (("meoclass1/oralnotes/simon-notes-p3.html", NOTES_EDITS),
                       ("meoclass1/QB1_B_CheatSheet.html", CHEAT_EDITS)):
        write(rel, apply_edits(baseline_text(rel), edits, rel))
        print("%s: %d edit(s)" % (rel, len(edits)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
