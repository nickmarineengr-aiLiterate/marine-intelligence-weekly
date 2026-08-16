// =============================================================
// Marine Intelligence Weekly — archive-portability contract
// Run: node --test tools/security/*.test.mjs
//
// Magazine issues are published at the root as `indexNN.html` and are later
// copied into `archive/issueNN.html` (playbook §3.2(b), remediation R1).
// This contract holds the precondition for that copy: every reference on
// Issues 23-30 must lead to the SAME file whether the page is served from
// the root or from one directory down. Until it does, R1 would publish
// eight pages with broken images and misdirected navigation.
//
// Part 0 exercises the analyser on an IN-MEMORY fixture site containing one
// example of every class this contract claims to detect, plus every class it
// must NOT report. Nothing broken is ever written into the repository to make
// these controls fire, and the controls keep working after the real pages are
// clean — a contract whose only evidence is the current tree stops testing
// anything the moment the tree is fixed.
//
// Part 1 is the contract on the real Issues 23-30.
//
// Part 2 is the FORWARD guard: templates/issue_shell.html (the shell every
// new issue is built from) must not reintroduce depth-sensitive paths, so
// Issue 31 onward cannot re-open this debt.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { ROOT } from "./deploy_set.mjs";
import { extractRefs } from "./link_integrity.mjs";
import {
  ARCHIVE_ISSUES, rootPageFor, archivePathFor, portableByConstruction,
  buildArchiveContext, auditIssue, audit,
} from "./archive_portability.mjs";

// -------------------------------------------------------------
// 0. CONTROLS on a synthetic site (nothing touches disk)
// -------------------------------------------------------------
describe("analyser — controls on an in-memory site", () => {
  // index99.html plays the part of an unarchived issue. archive/index.html
  // exists, which is what makes a bare `index.html` silently misresolve.
  const FILES = {
    "index99.html": `
      <a href="index.html">HOME-SILENT</a>
      <img src="assets/logo.webp">
      <a href="index98.html">PREV-404</a>
      <a href="sub/page.html">SUB-404</a>
      <a href="/assets/logo.webp">ok-root-absolute</a>
      <a href="/index.html">ok-root-home</a>
      <a href="https://marineintelligenceweekly.com/index.html">ok-same-host</a>
      <a href="#feature">ok-self-fragment</a>
      <a href="#">ok-bare-hash</a>
      <a href="https://imo.org/x">ok-external</a>
      <a href="mailto:a@b.c">ok-mailto</a>
      <a href="tel:+1">ok-tel</a>
      <a href="javascript:void(0)">ok-js</a>
      <a href="//cdn.example/x.js">ok-proto-rel</a>
      <div id="feature"></div>
      <!-- <a href="commented.html">no</a> -->
      <script>var s = 'href="in-script.html"';</script>
      <pre><a href="in-pre.html">no</a></pre>`,
    "index.html": "<h1>home</h1>",
    "index98.html": "<h1>prev</h1>",
    "archive/index.html": "<h1>archive listing</h1>",
    "assets/logo.webp": "",
    "sub/page.html": "<h1>sub</h1>",
  };
  const KEEP = Object.keys(FILES);
  const read = (rel) => FILES[rel] ?? null;
  const sim = buildArchiveContext([99], read, KEEP, KEEP);
  const res = auditIssue(99, sim);
  const byRaw = new Map(res.defects.map((d) => [d.raw, d]));

  test("the fixture is wired up and the analyser actually ran", () => {
    assert.equal(res.page, "index99.html");
    assert.ok(res.refsScanned > 10, `only ${res.refsScanned} refs extracted`);
    assert.ok(sim.virtual.has("archive/issue99.html"), "virtual archive copy must exist");
  });

  test("a relative asset that would 404 one level down is reported", () => {
    const d = byRaw.get("assets/logo.webp");
    assert.ok(d, "assets/logo.webp must be reported");
    assert.equal(d.kind, "archive-404");
    assert.equal(d.rootTarget, "assets/logo.webp");
    assert.equal(d.archiveTarget, null);
    assert.equal(d.suggestion, "/assets/logo.webp");
  });

  test("a relative sibling page that would 404 one level down is reported", () => {
    for (const raw of ["index98.html", "sub/page.html"]) {
      const d = byRaw.get(raw);
      assert.ok(d, `${raw} must be reported`);
      assert.equal(d.kind, "archive-404");
    }
  });

  // The class a plain "does it 404" check cannot see.
  test("a relative link that SILENTLY resolves to a different file is reported", () => {
    const d = byRaw.get("index.html");
    assert.ok(d, "bare index.html must be reported");
    assert.equal(d.kind, "silent-misresolution");
    assert.equal(d.rootTarget, "index.html");
    assert.equal(d.archiveTarget, "archive/index.html", "it resolves — to the WRONG page");
    assert.ok(d.archiveWouldResolve, "this defect does not 404, which is what makes it dangerous");
    assert.equal(d.suggestion, "/index.html");
  });

  test("things that must NOT be reported: root-absolute, same-host, self-fragment, bare #", () => {
    for (const raw of ["/assets/logo.webp", "/index.html",
      "https://marineintelligenceweekly.com/index.html", "#feature", "#"]) {
      assert.ok(!byRaw.has(raw), `${raw} must not be reported`);
    }
  });

  test("things that must NOT be reported: external, mailto, tel, javascript, protocol-relative", () => {
    for (const raw of ["https://imo.org/x", "mailto:a@b.c", "tel:+1",
      "javascript:void(0)", "//cdn.example/x.js"]) {
      assert.ok(!byRaw.has(raw), `${raw} must not be reported`);
    }
  });

  test("references inside comments, <script> and <pre> are never rewritten", () => {
    for (const raw of ["commented.html", "in-script.html", "in-pre.html"]) {
      assert.ok(!byRaw.has(raw), `${raw} must not be reported`);
    }
  });

  test("exactly the four intended defects are reported — no more", () => {
    assert.deepEqual(res.defects.map((d) => d.raw).sort(),
      ["assets/logo.webp", "index.html", "index98.html", "sub/page.html"]);
  });

  test("portableByConstruction classifies each depth-invariant form", () => {
    assert.equal(portableByConstruction("/assets/x.webp"), "root-absolute");
    assert.equal(portableByConstruction("https://marineintelligenceweekly.com/x"), "root-absolute");
    assert.equal(portableByConstruction("#feature"), "self-reference");
    assert.equal(portableByConstruction("?v=2"), "self-reference");
    assert.equal(portableByConstruction(""), "self-reference");
    assert.equal(portableByConstruction("assets/x.webp"), null);
    assert.equal(portableByConstruction("index29.html"), null);
  });

  test("archive path convention matches the one R1 will publish", () => {
    assert.equal(rootPageFor(30), "index30.html");
    assert.equal(archivePathFor(30), "archive/issue30.html");
  });
});

// -------------------------------------------------------------
// 1. THE CONTRACT on the real Issues 23-30
// -------------------------------------------------------------
describe("Issues 23-30 — every reference survives the move into archive/", () => {
  const res = audit();
  const fmt = (d) => `${d.source}:${d.line} ${d.attr}="${d.raw}" [${d.kind}] root=${d.rootTarget} archive=${d.archiveTarget ?? "404"}`;

  test("scan is not vacuous", () => {
    assert.equal(res.perIssue.length, 8);
    assert.deepEqual(ARCHIVE_ISSUES, [23, 24, 25, 26, 27, 28, 29, 30]);
    for (const r of res.perIssue) {
      assert.ok(!r.missing, `${r.page} is missing from the repository`);
      assert.ok(r.refsScanned > 20, `${r.page} yielded only ${r.refsScanned} refs`);
    }
    console.log(`    ${res.perIssue.length} issues, ${res.refsScanned} refs simulated at archive depth`);
  });

  test("0 archive-portability defects across Issues 23-30", () => {
    assert.deepEqual(res.defects.map(fmt), []);
  });

  test("no reference on any target page is depth-sensitive at all", () => {
    assert.equal(res.checked, 0,
      `${res.checked} reference(s) still resolve differently by depth`);
  });
});

// -------------------------------------------------------------
// 2. FORWARD GUARD — the shell new issues are built from
// -------------------------------------------------------------
describe("issue shell — Issue 31 onward cannot re-open this debt", () => {
  const shell = path.join(ROOT, "templates", "issue_shell.html");

  test("if the issue shell exists, none of its references are depth-sensitive", (t) => {
    if (!fs.existsSync(shell)) {
      t.skip("templates/issue_shell.html not present in this repository");
      return;
    }
    const offenders = extractRefs(fs.readFileSync(shell, "utf8"))
      .filter((r) => portableByConstruction(r.raw) === null)
      .map((r) => `${r.attr}="${r.raw}"`);
    assert.deepEqual(offenders, []);
  });
});
