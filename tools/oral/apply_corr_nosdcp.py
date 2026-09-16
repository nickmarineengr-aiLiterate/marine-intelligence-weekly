#!/usr/bin/env python3
"""CORR-NOSDCP-MINISTRY-20260916 - who owns NOSDCP, and who pays for the spill.

Candidate report on QB1_A Q15 ("NOSDCP - Explain."): "Pls check under which
ministry". Verified at primary source:

  * The Indian Coast Guard is under the MINISTRY OF DEFENCE. Government of India
    (Allocation of Business) Rules, 1961, as amended up to Amendment Series
    no. 386 of 22 July 2026, Ministry of Defence, Department of Defence, item 17:
    "All matters relating to Coast Guard Organisation, including- ... (c) Central
    Coordinating Agency for Combating of Oil Pollution in the coastal and marine
    environment of various maritime zones; (d) implementation of National
    Contingency Plan for oil spill disaster".
  * Coast Guard NOSDCP documents call the Coast Guard the CENTRAL COORDINATING
    AUTHORITY (ICG Marine Environment page; Chairman NOSDCP circulars 2012-2017;
    ICG dispersant policy 2025). The DG Coast Guard is Chairman NOSDCP.
  * The card said "Authority: Ministry of Earth Sciences" and "nodal (implementing)
    agency". MoES institutions support the response (oceanographic and
    spill-trajectory services); they do not control the plan.

The same two cards (Q14 OPRC, Q15 NOSDCP) also taught the P&I club as the party
"strictly liable for ALL costs" and a fixed reporting chain that put the DPA and
"DGS" in front of the statutory pollution report. Both are corrected here, and
Q14/Q15 are made to agree.

Scope is exactly two cards on one page and its SQ free-sample twin, which is kept
byte-identical to the gated copy for both cards.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

#: origin/main when this correction was authored; the pre-edit state it applies to.
BASELINE = "2e70859"

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from validate_batch_b import card_digests  # noqa: E402

PAGES = [REPO / "meoclass1" / "QB1_A.html", REPO / "SQ" / "QB1_A.html"]

# ---------------------------------------------------------------------------
# Q15 - the reported card. The whole answer region between the q-answer open
# and the related-q line is replaced: every limb of it carried the defect
# (body, 15s, 60s, reg-box, CE tip, trap, numbers, scenario, memory map).
# ---------------------------------------------------------------------------

Q15_REGION = """        <div class="answer-body">
          <h4>Full Form and Authority</h4>
          <p><strong>NOSDCP = National Oil Spill Disaster Contingency Plan</strong> — India's national plan for oil-spill preparedness and response in the Maritime Zones of India, and the national system India maintains as a Party to OPRC 1990. <strong>Ministry: Ministry of Defence.</strong> <strong>Central Coordinating Authority: Indian Coast Guard</strong> — the <strong>Director General, Indian Coast Guard</strong> is Chairman NOSDCP.</p>
          <p><em>Terminology — keep the two words apart:</em> Coast Guard NOSDCP documents call the Coast Guard the <strong>Central Coordinating Authority</strong>. The Government of India (Allocation of Business) Rules, 1961 list, under the Ministry of Defence, the Coast Guard Organisation as the <strong>Central Coordinating Agency</strong> for combating oil pollution and as responsible for implementing the national contingency plan for oil spill disaster. Say "Authority" in the oral; know that the Rules say "Agency".</p>
          <p><em>Not the Ministry of Earth Sciences.</em> MoES institutions such as INCOIS support the response with oceanographic and spill-trajectory services; they do not control NOSDCP.</p>
          <h4>History and Edition</h4>
          <p>Coast Guard designated for oil-spill response in <strong>1986</strong>; plan approved by the Government of India in <strong>1993</strong>; the revised NOSDCP edition was released in <strong>2015</strong> and has since been amended through Chairman NOSDCP circulars.</p>
          <h4>Who Responds Where</h4>
          <ul>
            <li><strong>Maritime Zones of India</strong> — Territorial Sea (12 nm), Contiguous Zone (24 nm), EEZ (200 nm): <strong>Indian Coast Guard</strong>.</li>
            <li><strong>Within port limits</strong> (harbour and anchorage): <strong>the port</strong>.</li>
            <li><strong>Within 500 m</strong> of offshore exploration and production platforms, coastal refineries and associated facilities (SBM, crude oil terminal, pipelines): <strong>the oil-handling agency</strong>.</li>
            <li><strong>Shoreline</strong>, when oil reaches the shore: <strong>the coastal State or Union Territory</strong>.</li>
          </ul>
          <h4>Three-Tier Response Structure</h4>
          <ul>
            <li><strong>Tier 1 — Local:</strong> the responsible agency's own resources — the ship under its SOPEP, the port within port limits, the oil-handling agency at its installation, the Coast Guard elsewhere in the maritime zones</li>
            <li><strong>Tier 2 — Regional:</strong> spill beyond local capability; Indian Coast Guard response in the Maritime Zones of India</li>
            <li><strong>Tier 3 — National:</strong> beyond regional capability; national resources mobilised and, where needed, international assistance under the OPRC co-operation provisions</li>
          </ul>
          <p><em>Tier tonnage limits are not given here — verify them against the current NOSDCP text before quoting figures.</em></p>
          <h4>Polluter Pays — Who Is Actually Liable</h4>
          <p>The Coast Guard leads the response; the cost is recovered from the polluter. Liability rests on the <strong>shipowner</strong> — strict, but normally <strong>within the convention limits</strong> and subject to the convention defences. The <strong>P&amp;I club is the liability insurer, not the liable party</strong>; where the applicable Convention provides for direct action (CLC 1992, Bunkers Convention), a claim may also be brought <strong>directly against the insurer</strong>. Persistent oil from tankers: <strong>CLC 1992</strong> (owner) with the <strong>1992 Fund</strong> on top. Bunker oil from other ships: the separate bunker-spill regime (see Q4). The CE's record of every response action, time and resource supports the claim.</p>
          <h4>Reporting</h4>
          <p>The CE informs the <strong>Master</strong> immediately and supports the report with operational data. The Master reports <strong>without delay</strong> to the coastal State under <strong>MARPOL Protocol I</strong> — in Indian waters, the <strong>Indian Coast Guard (nearest MRCC)</strong>, and the port authority as well when within port limits. The <strong>Company/DPA is informed in parallel</strong> under the SOPEP; the statutory report does not wait for the DPA.</p>
        </div>
        <div class="oral-box oral-15"><span class="oral-label">15-Second Answer</span>NOSDCP is India's National Oil Spill Disaster Contingency Plan under the Ministry of Defence, with the Indian Coast Guard as Central Coordinating Authority and the DG Coast Guard as Chairman. It gives effect to India's OPRC 1990 obligations through a Tier 1/2/3 response, with ports, oil-handling agencies and coastal States responsible within their own areas.</div>
        <div class="oral-box oral-60"><span class="oral-label">60-Second Answer</span>NOSDCP is the Government of India's national oil-spill contingency plan, maintained by the Indian Coast Guard under the Ministry of Defence. The Coast Guard is the Central Coordinating Authority — designated in 1986, plan approved in 1993, revised edition released in 2015 and amended since by circular — and the DG Coast Guard chairs it; the Allocation of Business Rules word the same role as Central Coordinating Agency. The Coast Guard responds in the Maritime Zones of India (TS 12 nm, CZ 24 nm, EEZ 200 nm); ports respond within port limits, oil-handling agencies within 500 m of their installations, and coastal States on the shoreline. Tier 1 is local resources, Tier 2 Coast Guard response beyond local capability, Tier 3 national mobilisation with international assistance under OPRC. The polluter pays: the shipowner is liable, normally within convention limits; the P&amp;I club insures that liability, and where the applicable Convention provides for direct action a claim may also be brought directly against the insurer; the CE's response records support cost recovery.</div>
        <div class="reg-box">
          <div class="reg-box-title">⚖ Regulatory References</div>
          <div class="reg-item"><span class="reg-code">NOSDCP (Indian Coast Guard)</span><span class="reg-desc">National Oil Spill Disaster Contingency Plan — revised edition 2015, amended by Chairman NOSDCP circulars; Indian Coast Guard as Central Coordinating Authority</span></div>
          <div class="reg-item"><span class="reg-code">Allocation of Business Rules 1961 — MoD item 17</span><span class="reg-desc">Ministry of Defence: Coast Guard as Central Coordinating Agency for combating oil pollution; implementation of the national contingency plan for oil spill disaster</span></div>
          <div class="reg-item"><span class="reg-code">OPRC Convention 1990</span><span class="reg-desc">Art. 6 — national system for preparedness and response, which NOSDCP provides for India</span></div>
          <div class="reg-item"><span class="reg-code">MARPOL Protocol I</span><span class="reg-desc">Reporting of incidents involving harmful substances — the Master's report that brings the national plan into action</span></div>
          <div class="reg-item"><span class="reg-code">MARPOL Annex I — Reg.37</span><span class="reg-desc">SOPEP — shipboard component of NOSDCP response chain</span></div>
          <div class="reg-item"><span class="reg-code">CLC 1992 / Fund 1992</span><span class="reg-desc">Shipowner's liability, normally limited, for persistent oil pollution from tankers, with Fund compensation above it</span></div>
        </div>
        <div class="ce-tip"><strong>CE Oral Tip (Nair):</strong> "Who coordinates oil spill response in Indian waters?" — the Indian Coast Guard, as Central Coordinating Authority under the Ministry of Defence. Not DGMA, and not the Ministry of Earth Sciences. DGMA handles flag-State and certification matters; the Coast Guard leads the operational response under NOSDCP. Know the three tiers and who responds where — port limits, 500 m around oil installations, the shoreline. On money, say "the shipowner is liable and the P&amp;I club insures that liability" — never "the P&amp;I club is liable for all costs".</div>
        <div class="trap-box"><strong class="trap-label">⚠ Examiner Trap</strong>"Is NOSDCP itself an international convention?" — <strong>No.</strong> NOSDCP is India's domestic plan; the international legal basis is OPRC 1990 (Art. 6 — national systems for preparedness and response). "Which ministry?" — <strong>Ministry of Defence</strong> (Indian Coast Guard). MoES/INCOIS supports with oceanographic and spill-trajectory services and is not the controlling authority.</div>
        <div class="numbers-box"><h4>Numbers to Memorise</h4>Maritime zones: TS <strong>12 nm</strong>, CZ <strong>24 nm</strong>, EEZ <strong>200 nm</strong> → Indian Coast Guard · port limits → port · <strong>500 m</strong> around oil installations → oil-handling agency · shoreline → coastal State/UT · Coast Guard designated <strong>1986</strong> · plan approved <strong>1993</strong> · revised edition <strong>2015</strong>, amended since · Central Coordinating Authority = <strong>Indian Coast Guard</strong> (Ministry of Defence).</div>
        <div class="casualty-box"><strong class="cas-label">⚓ Scenario Anchor</strong>Spill inside Indian port limits — the port leads the Tier 1 response with the ship working its SOPEP; beyond local capability it escalates to Coast Guard response. The CE's documented response actions support the cost claim against the shipowner and its P&amp;I insurer.</div>
        <div class="mental-map"><span class="root">NOSDCP — Who's Who</span>
 NOSDCP → MoD → DG ICG = Central Coordinating Authority
 MoES/INCOIS → supporting oceanographic / spill-trajectory services, not the controlling authority
 Report: Master → ICG MRCC (MARPOL Protocol I) · Company/DPA in parallel</div>
"""

Q15_STAMP_OLD = '<span class="q-version">QB1 · Q15 · v1.0</span>'
Q15_STAMP_NEW = ('<span class="q-version">QB1 · Q15 · v1.1 — corrected 16 Sep 2026 (NOSDCP authority correction): '
                 'ministry corrected from the Ministry of Earth Sciences to the Ministry of Defence; '
                 'Indian Coast Guard designation corrected from &quot;nodal implementing agency&quot; to Central Coordinating Authority '
                 '(Allocation of Business Rules: Central Coordinating Agency); response responsibilities by area added; '
                 'liability restated &mdash; the shipowner is liable, normally within convention limits, and the P&amp;I club is the insurer, '
                 'not the party liable for all costs; reporting restated under MARPOL Protocol I with the Company/DPA informed in parallel</span>')

# ---------------------------------------------------------------------------
# Q14 - three limbs only: the Coast Guard designation, the P&I liability
# statement, and the reporting chain. Everything else on the card is untouched.
# (old, new, expected count within the card)
# ---------------------------------------------------------------------------

Q14_EDITS = [
    ("<li>Report oil spill immediately to master → master reports to ICG / DGS / port authority</li>",
     "<li>Report the spill immediately to the Master; the Master reports without delay to the coastal State under MARPOL Protocol I — in Indian waters the Indian Coast Guard (nearest MRCC), and the port authority as well within port limits — with the Company/DPA informed in parallel</li>"),
    ("<li><strong>Polluter Pays Principle:</strong> ICG mobilises response but holds the registered shipowner (through P&amp;I club) strictly liable for ALL costs of containment, clean-up, and environmental restoration. CE must document every response action, time, and resource — this record forms the basis of cost recovery claims</li>",
     "<li><strong>Polluter Pays Principle:</strong> ICG mobilises the response and the cost is recovered from the polluter. The <strong>shipowner</strong> is liable — strictly, but normally within the convention limits and subject to the convention defences; the <strong>P&amp;I club insures that liability</strong>, and where the applicable Convention provides for direct action (CLC 1992, Bunkers Convention) a claim may also be brought directly against the insurer. CLC 1992 with the 1992 Fund covers persistent oil from tankers; bunker spills from other ships fall under the separate bunker regime (Q4). CE must document every response action, time, and resource — this record supports cost recovery claims</li>"),
    ("India's NOSDCP implements OPRC domestically: the Indian Coast Guard is the nodal agency, with a three-tier system where Tier 1 is ship/port-level response, Tier 2 is regional ICG centres, and Tier 3 is national mobilisation and international assistance; under the Polluter Pays principle, the shipowner's P&amp;I club is held strictly liable for all clean-up and restoration costs.",
     "India's NOSDCP implements OPRC domestically: the Indian Coast Guard, under the Ministry of Defence, is the Central Coordinating Authority, with a three-tier system where Tier 1 is local resources (ship, port, oil-handling agency), Tier 2 is Coast Guard response beyond local capability, and Tier 3 is national mobilisation and international assistance; under the Polluter Pays principle, the shipowner is liable, normally within convention limits, and the P&amp;I club insures that liability."),
    ("Know the reporting chain cold: CE → Master → DPA → ICG/Coast Guard → DGS → port authority. The ICG coordinates response but recovery of all costs goes back to the P&amp;I club via the Polluter Pays Principle.",
     "Know the reporting chain: CE → Master → coastal State under MARPOL Protocol I (Indian Coast Guard MRCC in Indian waters), with the Company/DPA informed in parallel — the statutory report does not wait for the DPA. The ICG coordinates the response; under the Polluter Pays Principle the cost is recovered from the shipowner, whose liability the P&amp;I club insures."),
    ("Indian waters — DGS or Indian Coast Guard?",
     "Indian waters — DGMA (formerly DG Shipping) or Indian Coast Guard?"),
    ("DGS handles flag-state and certification matters, but the ICG coordinates field response under NOSDCP.",
     "DGMA handles flag-State and certification matters, but the Indian Coast Guard, as Central Coordinating Authority under NOSDCP, coordinates the response."),
    ("ICG declares Tier 2 or Tier 3 NOSDCP response, and all costs are later recovered from the shipowner's P&amp;I club.",
     "ICG declares Tier 2 or Tier 3 NOSDCP response, and the response costs are later claimed from the shipowner and its P&amp;I insurer, within the applicable liability limits."),
    (" Tier 2 — Regional ICG centres\n",
     " Tier 2 — Coast Guard response beyond local capability\n"),
    ("  (Polluter Pays → P&amp;I club pays)</div>",
     "  (Polluter Pays → shipowner liable; P&amp;I insures)</div>"),
    ('<span class="q-version">QB1 · Q14 · v1.0</span>',
     '<span class="q-version">QB1 · Q14 · v1.1 — corrected 16 Sep 2026 (NOSDCP authority correction): '
     'Indian Coast Guard designation corrected from &quot;nodal agency&quot; to Central Coordinating Authority; '
     'liability restated &mdash; the shipowner is liable, normally within convention limits, and the P&amp;I club is the insurer, '
     'not the party liable for all costs; reporting chain restated under MARPOL Protocol I with the Company/DPA informed in parallel '
     'and DGS updated to DGMA</span>'),
]


def card_bounds(page: str, anchor: str) -> tuple[int, int]:
    """[start, end) of the balanced q-card div carrying id=anchor."""
    at = page.find('<div class="q-card" id="%s"' % anchor)
    assert at >= 0, "card %s not found" % anchor
    assert page.count('<div class="q-card" id="%s"' % anchor) == 1, "card %s not unique" % anchor
    depth, pos = 0, at
    import re
    tok = re.compile(r"<div\b|</div>")
    while True:
        m = tok.search(page, pos)
        assert m, "unbalanced card %s" % anchor
        depth += -1 if m.group(0) == "</div>" else 1
        pos = m.end()
        if depth == 0:
            return at, pos


def fix_q15(card: str) -> str:
    start = card.find('        <div class="answer-body">')
    end = card.find('        <div class="related-q">')
    assert start > 0 and end > start, "Q15 region markers missing"
    assert card.count('<div class="answer-body">') == 1
    old = card[start:end]
    assert "Ministry of Earth Sciences" in old, "Q15 already corrected?"
    card = card[:start] + Q15_REGION + card[end:]
    assert card.count(Q15_STAMP_OLD) == 1, "Q15 stamp"
    return card.replace(Q15_STAMP_OLD, Q15_STAMP_NEW)


def fix_q14(card: str) -> str:
    for old, new in Q14_EDITS:
        n = card.count(old)
        assert n == 1, "Q14 edit matched %d times: %r" % (n, old[:70])
        card = card.replace(old, new)
    return card


def main() -> int:
    results = {}
    for p in PAGES:
        # Always derive from the baseline commit, never from the working tree,
        # so a re-run reproduces the authorised bytes instead of compounding.
        raw = subprocess.run(
            ["git", "show", "%s:%s" % (BASELINE, p.relative_to(REPO).as_posix())],
            cwd=REPO, capture_output=True, check=True).stdout
        assert b"\r\n" not in raw, "%s is not LF-only" % p
        page = raw.decode("utf-8")
        before = card_digests(page)
        for anchor, fn in (("q15", fix_q15), ("q14", fix_q14)):
            a, b = card_bounds(page, anchor)
            page = page[:a] + fn(page[a:b]) + page[b:]
        after = card_digests(page)
        moved = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        assert moved == ["q14", "q15"], "unexpected cards moved in %s: %s" % (p, moved)
        p.write_bytes(page.encode("utf-8").replace(b"\r\n", b"\n"))
        results[p] = (before, after)
        print("%s: q14 %s -> %s | q15 %s -> %s" % (
            p.relative_to(REPO).as_posix(),
            before["q14"][:12], after["q14"][:12], before["q15"][:12], after["q15"][:12]))
    gated, teaser = (results[PAGES[0]], results[PAGES[1]])
    for k in ("q14", "q15"):
        assert gated[0][k] == teaser[0][k] and gated[1][k] == teaser[1][k], \
            "SQ twin %s not byte-identical to the gated copy" % k
    print("SQ twin identical to gated copy for q14 and q15, before and after")
    return 0


if __name__ == "__main__":
    sys.exit(main())
