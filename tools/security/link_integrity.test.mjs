// =============================================================
// Marine Intelligence Weekly — Link-integrity contract
// Run: node --test tools/security/*.test.mjs   (alongside security.test.mjs)
//
// Every runtime reference on every SERVED HTML page must resolve to a
// SERVED file, every in-page fragment must exist, no served page may
// reach into the tracked-but-excluded set, and no Oral page may hand a
// customer a control that lands on the Written product (or the reverse).
//
// The resolver is tools/security/link_integrity.mjs; the served set is
// deploy_set.mjs KEEP, the same computation deploy_surface.test.mjs uses.
//
// Part 0 exercises the resolver on an IN-MEMORY fixture site with a
// deliberately broken link in every class this contract claims to
// detect, plus the cases that must NOT be reported (query strings,
// directory indexes, extensionless pages, hash routes, mailto/tel/
// external, comments and code samples). Nothing broken is ever written
// into the repository to make these controls fire.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";
import {
  buildContext, scan, resolveRef, extractRefs, entitlementFor, SAME_HOST,
} from "./link_integrity.mjs";

// -------------------------------------------------------------
// 0. NEGATIVE CONTROLS on a synthetic site (nothing touches disk)
// -------------------------------------------------------------
describe("resolver — negative and positive controls on an in-memory site", () => {
  const FILES = {
    "index.html": `<a href="SQ/">store</a> <a href="about">about</a> <a href="/solvedQP/">written</a>
      <a href="assets/logo.webp?v=3">logo</a> <a href="/meoclass1/QB1_A.html#q2">oral q2</a>
      <a href="mailto:x@y.z">m</a> <a href="tel:+1">t</a> <a href="https://imo.org/x">ext</a>
      <a href="//cdn.example/x.js">proto</a> <a href="javascript:void(0)">js</a>
      <a href="MISSING.html">gone</a> <a href="Assets/logo.webp">case</a>
      <a href="tools/x.md">excluded</a> <a href="#nowhere">frag</a> <a href="#">bare</a>
      <a href="app/#/route">spa</a> <a href="app/#tab=search">tab</a>
      <!-- <a href="commented-out.html">no</a> --> <pre><a href="in-pre.html">no</a></pre>
      <code>href="in-code.html"</code> <script>var x = 'href="in-script.html"';</script>
      <a href="https://marineintelligenceweekly.com/about.html">own-host</a>
      <a href="https://marineintelligenceweekly.com/nope.html">own-host-missing</a>
      <img srcset="assets/logo.webp 1x, assets/missing@2x.webp 2x">`,
    "about.html": `<h1 id="top-h">a</h1>`,
    "SQ/index.html": `<a href="../meoclass1/QB1_A.html">upgrade</a>`,
    "assets/logo.webp": "",
    "app/index.html": `<div id="app"></div>`,
    "meoclass1/QB1_A.html": `<div id="q1"></div><div id="q2"></div>
      <a href="/solvedQP/QP2301.html">CROSS</a> <a href="/meoclass1/QB1_B.html#q9">deadfrag</a>
      <a href="../SQ/index.html">store</a>`,
    "meoclass1/QB1_B.html": `<div id="q1"></div>`,
    "solvedQP/index.html": `<a href="/meoclass1/QB1_A.html">CROSS-BACK</a> <a href="QP2301.html">ok</a>`,
    "solvedQP/QP2301.html": ``,
    "meoclass1/index.html": `<a href="#qb2">grp</a><div id="qb-groups-root"></div>
      <script>const QB_GROUPS = [{"id": "qb1"}, {"id": "qb2"}];
      html += \`<div class="group-label" id="\${g.id}">\`;</script>`,
    "meoclass1/QB1_C.html": `<a href="index.html#qb2">to group</a> <a href="index.html#qb9">no group</a>`,
  };
  const KEEP = Object.keys(FILES);
  const TRACKED = [...KEEP, "tools/x.md", "docs/README.md"];
  const ctx = buildContext(KEEP, TRACKED, (rel) => FILES[rel] ?? null);
  const res = scan(ctx);
  const brokenRaw = res.brokenLocal.map((r) => r.raw);

  test("a missing local file is reported", () => {
    assert.ok(brokenRaw.includes("MISSING.html"));
  });
  test("a same-host absolute URL to a missing file is reported; to a real file is not", () => {
    assert.ok(brokenRaw.includes("https://marineintelligenceweekly.com/nope.html"));
    assert.ok(!brokenRaw.includes("https://marineintelligenceweekly.com/about.html"));
  });
  test("a wrong relative path (escaping the site) is reported", () => {
    const r = resolveRef("SQ/index.html", "../../oops.html", ctx);
    assert.equal(r.resolved, null); assert.ok(r.escaped);
  });
  test("a missing srcset candidate is reported; the present one is not", () => {
    assert.ok(brokenRaw.includes("assets/missing@2x.webp"));
    assert.ok(!brokenRaw.includes("assets/logo.webp"));
  });
  test("a KEEP -> EXCLUDED reference is its own class, not a plain 404", () => {
    assert.deepEqual(res.keepToExcluded.map((r) => r.raw), ["tools/x.md"]);
    assert.ok(!brokenRaw.includes("tools/x.md"));
  });
  test("a case mismatch is its own class (Vercel is case-sensitive)", () => {
    assert.deepEqual(res.caseMismatch.map((r) => r.raw), ["Assets/logo.webp"]);
  });
  test("a missing fragment is reported, in-page and cross-page", () => {
    const dead = res.deadFragments.map((r) => r.raw);
    assert.ok(dead.includes("#nowhere"));
    assert.ok(dead.includes("/meoclass1/QB1_B.html#q9"));
    assert.ok(!dead.includes("/meoclass1/QB1_A.html#q2"));
  });
  test("a runtime-rendered hub group id is credited only via the cited provider", () => {
    const dead = res.deadFragments.map((r) => r.raw);
    assert.ok(!dead.includes("index.html#qb2"), "QB_GROUPS id must be credited");
    assert.ok(dead.includes("index.html#qb9"), "an id absent from QB_GROUPS is still dead");
  });
  test("cross-entitlement references are reported in BOTH directions; PUBLIC -> paid is not", () => {
    const x = res.crossEntitlement.map((r) => `${r.source} -> ${r.raw}`).sort();
    assert.deepEqual(x, [
      "meoclass1/QB1_A.html -> /solvedQP/QP2301.html",
      "solvedQP/index.html -> /meoclass1/QB1_A.html",
    ]);
  });
  test("things that must PASS: query string, dir index, extensionless page, hash routes, bare #", () => {
    const pass = ["assets/logo.webp?v=3", "SQ/", "about", "/solvedQP/", "app/#/route", "app/#tab=search", "#"];
    for (const p of pass) {
      const rec = res.records.find((r) => r.source === "index.html" && r.raw === p);
      assert.ok(rec, `${p} should have been scanned`);
      assert.ok(rec.resolved, `${p} should resolve`);
      assert.notEqual(rec.fragmentOk, false, `${p} fragment should not be dead`);
    }
  });
  test("things that must be IGNORED: mailto, tel, javascript, external, protocol-relative, comments, pre/code/script", () => {
    const raws = res.records.map((r) => r.raw);
    for (const skip of ["mailto:x@y.z", "tel:+1", "https://imo.org/x", "//cdn.example/x.js",
      "javascript:void(0)", "commented-out.html", "in-pre.html", "in-code.html", "in-script.html"]) {
      assert.ok(!raws.includes(skip), `${skip} must not be scanned as a local ref`);
    }
  });
  test("entitlement classification mirrors api/_lib/routes.js", () => {
    assert.equal(entitlementFor("solvedQP/QP2301.html"), "SOLVED_QP");
    assert.equal(entitlementFor("meoclass1/pastpapers/QP2301.html"), "SOLVED_QP");
    assert.equal(entitlementFor("meoclass1/oralnotes/simon-notes-p1.html"), "ORAL_QB_NOTES");
    assert.equal(entitlementFor("meoclass1/QB1_A.html"), "ORAL_QB_NOTES");
    assert.equal(entitlementFor("SQ/QB1_A.html"), "PUBLIC");
    assert.equal(entitlementFor("index.html"), "PUBLIC");
    assert.equal(entitlementFor("assets/logo.webp"), "PUBLIC");
  });
  test("extractor sees href/src/poster/action/data-src and both quote styles", () => {
    const refs = extractRefs(`<a href='a.html'>x</a><img src=b.png><video poster="c.jpg"></video>
      <form action="/api/x"></form><img data-src="d.webp">`).map((r) => r.raw);
    assert.deepEqual(refs.sort(), ["/api/x", "a.html", "b.png", "c.jpg", "d.webp"]);
  });
  test("SAME_HOST does not swallow look-alike hosts", () => {
    assert.ok(SAME_HOST.test("https://marineintelligenceweekly.com/x"));
    assert.ok(SAME_HOST.test("https://www.marineintelligenceweekly.com"));
    assert.ok(!SAME_HOST.test("https://marineintelligenceweekly.com.evil/x"));
    assert.ok(!SAME_HOST.test("https://notmarineintelligenceweekly.com/x"));
  });
});

// -------------------------------------------------------------
// 1. THE CONTRACT on the real deployed set
// -------------------------------------------------------------
describe("deployed surface — every runtime reference resolves", () => {
  const res = scan();
  const fmt = (r) => `${r.source}:${r.line} ${r.attr}="${r.raw}"`;

  test("scan is not vacuous", () => {
    assert.ok(res.pagesScanned > 200, `only ${res.pagesScanned} pages scanned`);
    assert.ok(res.refsScanned > 5000, `only ${res.refsScanned} refs scanned`);
    console.log(`    pages ${res.pagesScanned}, refs ${res.refsScanned}`);
  });
  test("0 broken local references", () => {
    assert.deepEqual(res.brokenLocal.map(fmt), []);
  });
  test("0 dead fragments", () => {
    assert.deepEqual(res.deadFragments.map(fmt), []);
  });
  test("0 KEEP -> EXCLUDED references", () => {
    assert.deepEqual(res.keepToExcluded.map(fmt), []);
  });
  test("0 cross-entitlement references (ORAL <-> WRITTEN)", () => {
    assert.deepEqual(res.crossEntitlement.map(fmt), []);
  });
  test("0 case mismatches", () => {
    assert.deepEqual(res.caseMismatch.map(fmt), []);
  });
});
