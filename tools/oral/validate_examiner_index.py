"""Release gate for the generated Examiner Index V2 and its SQ teaser.

Proves, from the files on disk, what the generator promises:

  * both pages and EXAMINER_INDEX_SNAPSHOT.json describe the same rows, and
    that snapshot is what resolve_snapshot() derives from canonical data now;
  * every count on either page is a len() of rendered rows;
  * every row links to a live question at a live anchor and shows that
    question's current text;
  * every tier literal is governed, badged per policy, and filterable;
  * no relationship renders twice; no review-held pair renders;
  * the two CSR questions stay distinct;
  * the full index keeps its access gate, the teaser does not gain one;
  * neither page links into the research tree;
  * no raw question-bank source format is tracked by git.

Exit 0 only when every check passes. Failures are named, never thrown.

    PYTHONIOENCODING=utf-8 python tools/oral/validate_examiner_index.py [--json]
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L                       # noqa: E402
import build_examiner_index as G           # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append({"check": name, "status": "PASS" if ok else "FAIL",
                    "detail": "" if ok else str(detail)})


def unesc(s):
    return html.unescape(L.strip_tags(s)).strip()


def main(argv):
    snap_path = G.OUT / G.SNAPSHOT_NAME
    if not (snap_path.exists() and G.INDEX_PATH.exists() and G.SQ_PATH.exists()):
        check("generated artefacts present", False,
              "missing one of snapshot / index / SQ teaser")
        return finish(argv)
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    index_html = G.INDEX_PATH.read_bytes()
    sq_html = G.SQ_PATH.read_bytes()

    # ------------------------------------------------------ 0. byte hygiene
    check("index is LF-only", b"\r\n" not in index_html)
    check("SQ teaser is LF-only", b"\r\n" not in sq_html)
    index_html = index_html.decode("utf-8")
    sq_html = sq_html.decode("utf-8")

    # ------------------------------------------- 1. snapshot == canonical now
    try:
        fresh = G.resolve_snapshot()
        check("snapshot equals a fresh resolve of canonical data",
              fresh == snap, "snapshot on disk differs from canonical data")
    except G.BuildFailure as e:
        check("canonical data resolves", False, str(e))
        fresh = None

    rows = snap["rows"]
    tot = snap["totals"]
    secs = {s["slug"]: s for s in snap["sections"]}
    tiers = G.TIERS
    check("snapshot totals are len() of its rows",
          tot["relationships"] == len(rows)
          and tot["examiners"] == len(snap["sections"])
          and all(tot["by_tier"][t] == sum(1 for r in rows if r["tier"] == t)
                  for t in tiers)
          and all(s["count"] == sum(1 for r in rows if r["slug"] == s["slug"])
                  and all(s["by_tier"][t] == sum(
                      1 for r in rows if r["slug"] == s["slug"] and r["tier"] == t)
                      for t in tiers)
                  for s in snap["sections"]))
    keys = [(r["examiner"], r["canonical_question_id"]) for r in rows]
    check("no duplicate relationship in snapshot", len(keys) == len(set(keys)),
          str([k for k, v in Counter(keys).items() if v > 1][:5]))

    # ------------------------------------------------- 2. full index parse
    parsed = L.parse_examiner_index(G.INDEX_PATH)
    prow = parsed["rows"]
    check("rendered row count equals snapshot row count",
          len(prow) == len(rows), "%d vs %d" % (len(prow), len(rows)))
    check("rendered rows equal snapshot rows in order",
          [(r["examiner_slug"], r["href"], r["tier"]) for r in prow]
          == [(r["slug"], r["url"], r["tier"]) for r in rows])

    inv = {q["canonical_question_id"]: q for q in L.build_inventory()}
    anchors = L.all_anchors()
    bad_link, bad_text, empty = [], [], []
    for r in prow:
        f, a = L.split_href(r["href"])
        qid = f[:-5] + "#" + a
        q = inv.get(qid)
        if q is None or a not in anchors.get(f, set()):
            bad_link.append(r["href"])
            continue
        if not unesc(r["display_text"]):
            empty.append(qid)
        if unesc(r["display_text"]) != q["question_text"].strip():
            bad_text.append(qid)
    check("every rendered link resolves to a live question anchor", not bad_link,
          str(bad_link[:5]))
    check("every rendered text is the live question text", not bad_text,
          str(bad_text[:5]))
    check("no rendered row has empty text", not empty, str(empty[:5]))
    dup = [k for k, v in Counter((r["examiner_slug"], r["href"]) for r in prow).items()
           if v > 1]
    check("no relationship renders twice", not dup, str(dup[:5]))

    # ------------------------------------------- 3. tiers, badges, filters
    bad_tier = sorted({r["tier"] for r in prow} - set(tiers))
    check("every rendered tier literal is governed", not bad_tier, str(bad_tier))
    bad_badge = [(r["href"], r["badge"]) for r in prow
                 if r["tier"] in tiers and unesc(r["badge"]) != tiers[r["tier"]]["badge"]]
    check("every badge matches its tier policy", not bad_badge, str(bad_badge[:5]))
    missing_toggle = []
    for m in re.finditer(r'<section class="ex-section" id="ex-([^"]+)">(.*?)</section>',
                         index_html, re.S):
        slug, blob = m.groups()
        toggles = set(re.findall(r'data-tier-toggle="([^"]+)"', blob))
        lits = set(re.findall(r'data-tier="([^"]+)"', blob))
        if not lits <= toggles:
            missing_toggle.append((slug, sorted(lits - toggles)))
        if not set(tiers) <= toggles:
            missing_toggle.append((slug, "toggle set incomplete"))
    check("every rendered tier literal has a filter toggle in its section",
          not missing_toggle, str(missing_toggle[:5]))

    # ------------------------------------------------- 4. counts by construction
    bad_counts = []
    for s in parsed["sections"]:
        want = secs.get(s["slug"])
        if want is None:
            bad_counts.append((s["slug"], "not in snapshot"))
            continue
        if s["rendered_rows"] != want["count"] or s["heading_count"] != want["count"]:
            bad_counts.append((s["slug"], s["rendered_rows"], s["heading_count"], want["count"]))
        # ex-stats: every tier with rows appears with the right number and they sum
        stats = s["ex_stats"]
        for t, n in want["by_tier"].items():
            lab = tiers[t]["label"].lower().split()[0]   # 'ce' for 'ce tip'
            got = next((v for k, v in stats.items() if k.startswith(lab)), 0)
            if n and got != n:
                bad_counts.append((s["slug"], "stat", t, got, n))
        if sum(stats.values()) != want["count"]:
            bad_counts.append((s["slug"], "stats-sum", sum(stats.values()), want["count"]))
        if parsed["mininav"].get(want["name"]) != want["count"]:
            bad_counts.append((s["slug"], "mininav", parsed["mininav"].get(want["name"]),
                               want["count"]))
        expected_batches = -(-want["count"] // G.CONFIG["batch_size"])
        if s["batches"] != expected_batches:
            bad_counts.append((s["slug"], "batches", s["batches"], expected_batches))
    check("section heading, rendered rows, tier sub-counts, mini-nav and batches agree",
          not bad_counts, str(bad_counts[:6]))
    check("every snapshot section is rendered",
          {s["slug"] for s in parsed["sections"]} == set(secs))
    # summary bar: parse precisely rather than through the legacy header regex
    hdr = {}
    sb = re.search(r'<div class="summary-bar">(.*?)</div>', index_html, re.S).group(1)
    m = re.search(r"<strong>(\d+)</strong> tagged pairs · (\d+) examiners", sb)
    hdr["tagged pairs"], hdr["examiners"] = (int(m.group(1)), int(m.group(2))) if m else (None, None)
    for n, lab in re.findall(r"<strong>(\d+)</strong> ([a-z ]+)</span>", sb):
        hdr[lab.strip()] = int(n)
    hdr_total = hdr.get("tagged pairs")
    check("header examiner count equals rendered sections",
          hdr.get("examiners") == len(parsed["sections"]))
    check("header total equals rendered rows", hdr_total == len(prow),
          "%s vs %d" % (hdr_total, len(prow)))
    bad_hdr = [(t, hdr.get(tiers[t]["label"].lower()), tot["by_tier"][t])
               for t in tiers if tot["by_tier"][t]
               and hdr.get(tiers[t]["label"].lower()) != tot["by_tier"][t]]
    check("header tier totals equal rendered tier totals", not bad_hdr, str(bad_hdr))
    check("mini-nav sums to rendered rows",
          sum(parsed["mininav"].values()) == len(prow),
          "%d vs %d" % (sum(parsed["mininav"].values()), len(prow)))
    check("no hand-entered legacy total survives",
          not re.search(r"\b791\b|\b809\b|\b863\b", index_html.split("<main>")[0]))

    # ------------------------------------------ 5. Release-A holds + CSR trap
    dec = json.loads((G.OUT / "RELEASE_A_REVIEW_DECISIONS.json").read_text(encoding="utf-8"))
    ra = json.loads((G.OUT / "RELEASE_A_CONNECTIONS.json").read_text(encoding="utf-8"))
    ra_by_id = {c["relation_id"]: c for c in ra["connections"]}
    held_pairs = {(ra_by_id[h["relation_id"]]["examiner"],
                   ra_by_id[h["relation_id"]]["canonical_question_id"])
                  for h in dec["held"] if h["relation_id"] in ra_by_id}
    rendered_pairs = {(r["examiner"], r["canonical_question_id"]) for r in rows}
    leaked = sorted(held_pairs & rendered_pairs)
    # a held pair may legitimately exist as an OLDER relationship; report which
    older = [(k, [r["sources"] for r in rows if (r["examiner"], r["canonical_question_id"]) == k])
             for k in leaked]
    check("no review-held Release-A pair renders as a Release-A relationship",
          all("RELEASE_A" not in s for _, srcs in older for s in srcs), str(older[:5]))
    held = json.loads((G.OUT / "RELEASE_A_HELD.json").read_text(encoding="utf-8"))
    below = {(h["examiner"], h["canonical_question_id"]) for h in held["held"]
             if h["decision"] == "HOLD_EVIDENCE_BELOW_FLOOR"}
    leaked = [k for k in below & rendered_pairs
              if any("RELEASE_A" in r["sources"] for r in rows
                     if (r["examiner"], r["canonical_question_id"]) == k)]
    check("no below-floor Release-A pair renders as a Release-A relationship",
          not leaked, str(leaked[:5]))

    csr1 = [r for r in rows if r["canonical_question_id"] == "QB1_K#q8"]
    csr2 = [r for r in rows if r["canonical_question_id"] == "QB5_C_B#q8"]
    check("CSR acronym trap: QB1_K#q8 (IACS CSR) and QB5_C_B#q8 (Continuous Synopsis "
          "Record) render as distinct questions",
          bool(csr1) and bool(csr2)
          and csr1[0]["url"] != csr2[0]["url"]
          and csr1[0]["display_text"] != csr2[0]["display_text"]
          and csr1[0]["display_text"] == inv["QB1_K#q8"]["question_text"].strip()
          and csr2[0]["display_text"] == inv["QB5_C_B#q8"]["question_text"].strip()
          and "E-CSR" in csr2[0]["display_text"] and "E-CSR" not in csr1[0]["display_text"],
          "csr1=%s csr2=%s" % ([r["url"] for r in csr1], [r["url"] for r in csr2]))

    # -------------------------------------------- 6. John and provenance
    ext_only = [s for s in snap["sections"] if s["status"] == "NEW_EXTERNAL_ONLY_EXAMINER"]
    check("an external-only examiner never renders a Confirmed row",
          all(s["by_tier"].get("confirmed", 0) == 0 for s in ext_only),
          str([(s["slug"], s["by_tier"]) for s in ext_only]))
    check("external-only examiner section carries the Reported note",
          all(('id="ex-%s"' % s["slug"]) in index_html
              and re.search(r'id="ex-%s">.*?class="ex-note"' % s["slug"], index_html, re.S)
              for s in ext_only))

    # ------------------------------------------------ 7. access + hygiene
    check("full index keeps its access gate",
          'if(!/miw_auth=1/.test(document.cookie)){window.location.replace("/SQ/pay.html");}'
          in index_html)
    check("full index is noindex", 'name="robots" content="noindex' in index_html)
    check("SQ teaser has no access gate and keeps its CTA",
          "miw_auth" not in sq_html and 'href="/SQ/pay.html"' in sq_html)
    check("neither page links into the research tree",
          "oral-intelligence" not in index_html and "oral-intelligence" not in sq_html)

    # ---------------------------------------------- 8. SQ teaser == snapshot
    sq = G.CONFIG["sq"]
    free, promo = secs.get(sq["free_examiner"]), secs.get(sq["promo_examiner"])
    nums = {}
    for m in re.finditer(r'<div class="stat-num">(\d+)</div><div class="stat-label">([^<]+)</div>', sq_html):
        nums[m.group(2)] = int(m.group(1))
    check("SQ stats derive from the snapshot",
          nums.get("Questions Tagged") == tot["relationships"]
          and nums.get("Examiners Covered") == tot["examiners"]
          and promo and nums.get("%s Sir Questions" % promo["name"]) == promo["count"]
          and nums.get("QB Files") == tot["qb_files"], str(nums))
    hero = re.search(r'<div class="hero">.*?<p>(\d+) MEO Class 1', sq_html, re.S)
    check("SQ hero total equals snapshot total",
          hero and int(hero.group(1)) == tot["relationships"])
    free_rows = re.findall(r'<div class="q-row-open">\s*<span class="q-badge">(.*?)</span>\s*<div class="q-txt">(.*?)</div>', sq_html, re.S)
    snap_free = [r for r in rows if r["slug"] == sq["free_examiner"]]
    check("SQ free sample is the free examiner's complete section",
          free and len(free_rows) == free["count"] == len(snap_free)
          and [unesc(t) for _, t in free_rows] == [r["display_text"] for r in snap_free]
          and ("All %d Questions" % free["count"]) in sq_html,
          "%d rendered vs %s" % (len(free_rows), free and free["count"]))
    faq = re.search(r'"mainEntity":\[(.*?)\]\}\n</script>', sq_html, re.S)
    faq_names = [json.loads("[" + faq.group(1) + "]") if faq else []][0]
    check("SQ FAQ JSON-LD lists exactly the free sample questions",
          [q["name"] for q in faq_names] == [r["display_text"] for r in snap_free])
    prev = re.findall(r'<div class="q-row-preview">', sq_html)
    locked = re.search(r"(\d+) more %s Sir questions.*?Unlock all (\d+) %s Sir" % (
        promo["name"], promo["name"]) if promo else "x^", sq_html, re.S)
    check("SQ promo preview + locked remainder equal the promo examiner's count",
          promo and locked and len(prev) == min(sq["promo_preview_rows"], promo["count"])
          and int(locked.group(1)) == promo["count"] - len(prev)
          and int(locked.group(2)) == promo["count"], str(locked and locked.groups()))
    cards = dict((n, int(c)) for n, c in re.findall(
        r'<h3>([^<]+)</h3>.*?<div class="locked-count">(\d+) questions tagged</div>', sq_html, re.S))
    others = {s["name"]: s["count"] for s in snap["sections"]
              if s["slug"] not in (sq["free_examiner"], sq["promo_examiner"])}
    check("SQ locked cards list every other examiner with its snapshot count",
          cards == others, "%s vs %s" % (cards, others))
    cta = re.search(r"all (\d+) tagged questions", sq_html)
    check("SQ final CTA total equals snapshot total",
          cta and int(cta.group(1)) == tot["relationships"])
    check("no hand-entered legacy total survives on the SQ teaser",
          not re.search(r"\b791\b|\b212\b|62\+", sq_html))

    # ------------------------------------- 8b. storefront card == snapshot
    home = G.SQ_HOME_PATH.read_bytes()
    check("SQ home is LF-only", b"\r\n" not in home)
    home = home.decode("utf-8")
    m = G.CARD_RE.search(home)
    want_title, want_desc, want_tags = G.render_sq_home_card(snap)
    check("SQ home examiner-index card title, description and tags derive from the snapshot",
          bool(m) and m.group(2) == want_title and m.group(4) == want_desc
          and m.group(6) == want_tags,
          "card=%r" % (m.group(4)[:120] if m else None))
    check("SQ home carries no hand-typed legacy examiner numbers",
          not re.search(r"10-question set|Simon Sir's 212|791\+", home))

    # ------------------------------- 8c. storefront stats ribbon == corpus
    # Same discipline tools/pastpapers/solvedqp_check.py applies to the two
    # Written figures: the attribute AND the number a candidate actually
    # reads must both equal the derived count, so neither can be corrected
    # while the other stays wrong. These two advertised 417+ and 5 against a
    # real 682 and 7.
    n_answered = sum(1 for q in inv.values() if q["has_answer"])
    for attr, expected, what in (("data-oral-questions", n_answered,
                                  "answered canonical questions"),
                                 ("data-oral-examiners", tot["examiners"],
                                  "examiners covered")):
        found = re.findall(attr + r'="(\d+)"', home)
        check("SQ home carries a guarded %s figure" % what, bool(found),
              "no element carries %s -- the storefront count is unguarded, "
              "which is how 417+ survived to %d" % (attr, expected))
        check("SQ home %s attribute equals the corpus" % attr,
              all(int(v) == expected for v in found),
              "%s vs %d" % (found, expected))
        for m in re.finditer(attr + r'="\d+"[^>]*>(.*?)</div>\s*</div>', home, re.S):
            nums = re.findall(r"\d+", unesc(m.group(1)))
            check("SQ home %s visible text equals its attribute" % attr,
                  nums and int(nums[0]) == expected,
                  "visible %s vs %d" % (nums, expected))

    # The free sample advertised on the storefront is the SQ teaser's free
    # examiner section; it said 10 while the teaser published 33.
    free_sec = secs[G.CONFIG["sq"]["free_examiner"]]
    found = re.findall(r'data-oral-free-sample="(\d+)"[^>]*>(\d+)<', home)
    check("SQ home free-sample count is guarded and equals the teaser",
          found and all(int(a) == int(b) == free_sec["count"] for a, b in found),
          "%s vs %d" % (found, free_sec["count"]))

    # Every prose claim of the oral question count, wherever it is phrased.
    # The stale figure may survive inside an HTML comment -- that comment is
    # the record of what drifted -- but never in candidate-visible text.
    visible = re.sub(r"<!--.*?-->", "", home, flags=re.S)
    claims = re.findall(r"(\d+)\+?\s+solved oral", visible)
    check("SQ home states the oral question count in prose", bool(claims))
    check("every SQ home prose oral-question claim equals the corpus",
          all(int(c) == n_answered for c in claims),
          "%s vs %d" % (sorted(set(claims)), n_answered))
    check("no stale oral figure survives in candidate-visible SQ home text",
          "417" not in visible)

    # ---------------------------------------------- 9. git safety gate (H)
    try:
        ls = subprocess.run(["git", "ls-files", "--", "docs/MIW-master-Question-bank"],
                            cwd=str(L.REPO), capture_output=True, text=True, timeout=60)
        tracked = [x for x in ls.stdout.splitlines() if x.strip()]
        # fail closed: if git cannot answer, that is not the same as "none"
        check("no raw question-bank source file is tracked by git",
              ls.returncode == 0 and not tracked,
              (str(tracked[:5]) if ls.returncode == 0
               else "git ls-files exit %d: %s" % (ls.returncode, ls.stderr.strip()[:160])))
    except Exception as e:  # git absent: name it, do not pass silently
        check("no raw question-bank source file is tracked by git", False, repr(e))

    # -------------------- 10. the QB hub agrees with the examiner universe
    # meoclass1/index.html is HAND-MAINTAINED -- no generator writes it -- and
    # it advertised "6 Examiners Covered" with six name pills while
    # examiner-index.html, one click away and fully generated, published seven
    # including John. That is a candidate-facing contradiction between two
    # pages of the same product, and nothing owned it.
    #
    # Guarded here rather than generated: the hub is a curated marketing
    # surface and turning it into a build artefact is a larger change than
    # this release should make. A bounded, validator-guarded hand-update is
    # what SKILL section 20 asks for. The check derives BOTH sides -- the
    # expected count and the expected names come from the generator, never
    # from a literal here, so it cannot expire when an eighth examiner
    # arrives.
    hub = L.MEO / "index.html"
    if not hub.is_file():
        check("the QB hub states the examiner count", False, "index.html absent")
    else:
        hub_text = hub.read_text(encoding="utf-8")
        expected = sorted(sec["name"] for sec in snap["sections"])
        m = re.search(r'<span class="stat-val">(\d+)</span>'
                      r'<span class="stat-label">Examiners Covered</span>',
                      hub_text)
        check("the QB hub states the examiner count",
              m is not None and int(m.group(1)) == len(expected),
              "hub says %s, generator publishes %d"
              % (m.group(1) if m else "<absent>", len(expected)))
        pills = sorted(set(re.findall(r'<span class="ex-pill">([^<]+)</span>',
                                      hub_text)))
        check("the QB hub names every published examiner",
              pills == expected,
              "hub=%s generator=%s" % (pills, expected))

    return finish(argv)


def finish(argv):
    n_fail = sum(1 for r in RESULTS if r["status"] == "FAIL")
    if "--json" in argv:
        print(json.dumps({"results": RESULTS, "passed": len(RESULTS) - n_fail,
                          "failed": n_fail}, indent=1))
    else:
        for r in RESULTS:
            print("%s  %s %s" % (r["status"], r["check"],
                                  ("- " + r["detail"]) if r["detail"] else ""))
        print("\n%d PASS / %d FAIL" % (len(RESULTS) - n_fail, n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
