// =============================================================
// Marine Intelligence Weekly — archive-continuity contract (R1)
// Run: node --test tools/security/*.test.mjs
//
// R2 proved the Issue 23-30 pages COULD survive the move into archive/.
// R1 actually moved them. This contract holds what R1 published:
//
//   1. archive/issue17.html .. issue30.html is a CONTINUOUS run, so the
//      archive's own record has no hole between the thematic map (01-16)
//      and the latest issue.
//   2. Each archived page 23-30 is the SAME DOCUMENT as its root twin.
//      The house convention (evidenced by issue17/issue19, which are
//      byte-identical to index17/index19) is a verbatim copy: the archive
//      page is not re-headed, and its canonical/og:url deliberately keep
//      pointing at the ROOT url, so the copy never claims a second SEO
//      identity for the same article.
//   3. The archive listing offers every issue 17-30 exactly once.
//   4. The R2 guarantee still holds ON THE PUBLISHED COPIES, not merely on
//      a simulation of them. archive_portability.mjs answers "would this
//      page survive the move"; once the move has happened the honest
//      question is "did it", so the real archive bytes are re-checked here.
//
// WHY CONTENT EQUIVALENCE IS ASSERTED, NOT EYEBALLED
//   Eight copied pages is exactly the size at which a silent divergence -
//   one stale copy, one half-applied edit - survives review. Comparing the
//   documents mechanically is the only claim that stays true next year.
//
// Line endings are normalised before comparison: .gitattributes pins *.html
// to LF in the repository while core.autocrlf leaves CRLF in the working
// tree, so raw bytes differ by checkout policy, not by content.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { ROOT, KEEP, TRACKED } from "./deploy_set.mjs";
import { buildContext, extractRefs, resolveRef } from "./link_integrity.mjs";
import {
  ARCHIVE_ISSUES, rootPageFor, archivePathFor, portableByConstruction,
} from "./archive_portability.mjs";

/** Every issue that must have a standalone page in archive/. */
const ARCHIVED_RANGE = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30];

const ARCHIVE_INDEX = "archive/index.html";

const read = (rel) => fs.readFileSync(path.join(ROOT, rel), "utf8");
const exists = (rel) => fs.existsSync(path.join(ROOT, rel));
/** Content identity, independent of checkout line-ending policy. */
const normalise = (s) => s.replace(/\r\n/g, "\n").trim();

// -------------------------------------------------------------
// 0. CONTROLS — the comparison actually discriminates
// -------------------------------------------------------------
describe("comparison controls", () => {
  test("normalise ignores line-ending policy but not content", () => {
    assert.equal(normalise("<a>\r\n<b>"), normalise("<a>\n<b>"));
    assert.equal(normalise("\n<a>\n"), normalise("<a>"));
    assert.notEqual(normalise("<a>x</a>"), normalise("<a>y</a>"));
  });

  test("a depth-sensitive reference is still recognised as such", () => {
    // Guards the guard: if portableByConstruction ever started returning a
    // reason for everything, part 3 below would pass vacuously.
    assert.equal(portableByConstruction("assets/cover30.webp"), null);
    assert.equal(portableByConstruction("index29.html"), null);
    assert.equal(portableByConstruction("/assets/cover30.webp"), "root-absolute");
  });
});

// -------------------------------------------------------------
// 1. THE ARCHIVE IS CONTINUOUS
// -------------------------------------------------------------
describe("archive continuity — issues 17-30 all present", () => {
  test("the thematic map still carries issues 01-16", () => {
    assert.ok(exists("archive/thematicmapissues01to16.html"),
      "archive/thematicmapissues01to16.html is the only record of issues 01-16");
  });

  test("every issue 17-30 has an archive page, with no gap", () => {
    const missing = ARCHIVED_RANGE.filter((n) => !exists(archivePathFor(n)));
    assert.deepEqual(missing, [], `archive pages missing for issue(s): ${missing.join(", ")}`);
  });

  test("the R1 backfill set specifically exists", () => {
    assert.deepEqual(ARCHIVE_ISSUES, [23, 24, 25, 26, 27, 28, 29, 30]);
    for (const n of ARCHIVE_ISSUES) {
      assert.ok(exists(archivePathFor(n)), `${archivePathFor(n)} was not published`);
    }
  });

  test("no archive page exists for an issue that has not been published", () => {
    // Issue 31 is not started; an archive page for it would be a phantom.
    assert.ok(!exists("archive/issue31.html"), "archive/issue31.html must not exist");
    assert.ok(!exists("index31.html"), "index31.html must not exist");
  });
});

// -------------------------------------------------------------
// 2. ROOT AND ARCHIVE DO NOT DIVERGE
// -------------------------------------------------------------
describe("archived issues 23-30 are the same document as their root twin", () => {
  for (const n of ARCHIVE_ISSUES) {
    const rootRel = rootPageFor(n);
    const archRel = archivePathFor(n);

    test(`${archRel} is a verbatim copy of ${rootRel}`, () => {
      const rootDoc = normalise(read(rootRel));
      const archDoc = normalise(read(archRel));
      assert.ok(rootDoc.length > 5000, `${rootRel} is suspiciously small`);
      assert.equal(archDoc.length, rootDoc.length,
        `${archRel} differs from ${rootRel} by ${archDoc.length - rootDoc.length} chars`);
      assert.equal(archDoc, rootDoc, `${archRel} has diverged from ${rootRel}`);
    });

    test(`${archRel} keeps the ROOT url canonical`, () => {
      const doc = read(archRel);
      const canonical = doc.match(/<link[^>]+rel="canonical"[^>]+href="([^"]+)"/i);
      assert.ok(canonical, `${archRel} has no canonical link`);
      assert.equal(canonical[1], `https://marineintelligenceweekly.com/${rootRel}`,
        "an archive copy must not claim a second SEO identity for the same article");
    });
  }
});

// -------------------------------------------------------------
// 3. THE R2 GUARANTEE HOLDS ON THE PUBLISHED COPIES
// -------------------------------------------------------------
describe("published archive pages lead where the root page leads", () => {
  // The real tree, with the archive copies now genuinely on disk. No
  // simulation: R2 asked "would the move preserve meaning", R1 must answer
  // "it did", and only the published bytes can answer that.
  const ctx = buildContext(KEEP, TRACKED, (rel) => {
    try { return fs.readFileSync(path.join(ROOT, rel), "utf8"); } catch { return null; }
  });

  for (const n of ARCHIVE_ISSUES) {
    const rootRel = rootPageFor(n);
    const archRel = archivePathFor(n);

    test(`${archRel} — every reference resolves to the same file as on ${rootRel}`, () => {
      const refs = extractRefs(read(archRel));
      assert.ok(refs.length > 0, "no references extracted — the scan would be vacuous");

      let compared = 0;
      const drift = [];
      for (const r of refs) {
        const atRoot = resolveRef(rootRel, r.raw, ctx);
        if (!atRoot) continue;                       // external, mailto, tel, …
        if (portableByConstruction(r.raw) === "self-reference") continue;
        compared++;
        const atArchive = resolveRef(archRel, r.raw, ctx);
        if (atArchive?.resolved !== atRoot.resolved) {
          drift.push(`${r.attr}="${r.raw}" root=${atRoot.resolved} archive=${atArchive?.resolved ?? "(404)"}`);
        }
      }
      assert.deepEqual(drift, []);
      assert.ok(compared > 0, `no in-scope references on ${archRel} — check would be vacuous`);
    });
  }
});

// -------------------------------------------------------------
// 4. THE ARCHIVE LISTING OFFERS EVERY ISSUE, ONCE
// -------------------------------------------------------------
describe("archive/index.html lists issues 17-30", () => {
  const listing = read(ARCHIVE_INDEX);

  /**
   * A card may point at either the root page or the archive copy — both are
   * in use in the listing today (issue 17 links to the archive copy, 18-30
   * link to the canonical root page). What must hold is that each issue is
   * offered, and offered once.
   */
  const cardsFor = (n) => {
    const pat = new RegExp(
      `href="https://marineintelligenceweekly\\.com/(?:index${n}\\.html|archive/issue${n}\\.html)"`, "g");
    return listing.match(pat) ?? [];
  };

  test("every issue 17-30 appears in the listing", () => {
    const absent = ARCHIVED_RANGE.filter((n) => cardsFor(n).length === 0);
    assert.deepEqual(absent, [], `not listed in the archive index: ${absent.join(", ")}`);
  });

  test("no issue is listed twice", () => {
    const dupes = ARCHIVED_RANGE.filter((n) => cardsFor(n).length > 1);
    assert.deepEqual(dupes, [], `listed more than once: ${dupes.join(", ")}`);
  });

  test("the R1 issues carry a kicker with their issue number", () => {
    for (const n of ARCHIVE_ISSUES) {
      assert.ok(listing.includes(`>Issue ${n} ·`),
        `archive index has no "Issue ${n} ·" kicker`);
    }
  });

  test("exactly one card is badged as the latest, and it is the latest issue", () => {
    const badges = listing.match(/class="card-new"/g) ?? [];
    assert.equal(badges.length, 1, "there must be exactly one 'Latest in Archive' badge");
    const latest = Math.max(...ARCHIVED_RANGE);
    const badgeAt = listing.indexOf('class="card-new"');
    const cardStart = listing.lastIndexOf('<a href=', badgeAt);
    assert.ok(listing.slice(cardStart, badgeAt).includes(`index${latest}.html`),
      `the 'Latest in Archive' badge must sit on Issue ${latest}`);
  });

  test("the published-issues stat matches the latest issue number", () => {
    const stat = listing.match(/id="s-issues"[^>]*>(\d+)</);
    assert.ok(stat, "archive index has no #s-issues stat");
    assert.equal(Number(stat[1]), Math.max(...ARCHIVED_RANGE));
  });
});
