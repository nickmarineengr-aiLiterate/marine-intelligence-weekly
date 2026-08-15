// =============================================================
// Marine Intelligence Weekly — GA4 coverage contract
// Run: node --test tools/security/*.test.mjs
//
// Every SERVED HTML page (deploy_set.mjs KEEP — the same set
// deploy_surface.test.mjs and link_integrity.test.mjs use) must carry
// exactly ONE valid installation of the canonical GA4 property
// G-0YEE2CBNP5: one gtag.js loader, one gtag('config'), one gtag('js'),
// no other Measurement ID, no UA- legacy tag, no analytics.js loader.
//
// Part 0 runs the analyser over in-memory fixtures for every failure
// class this contract claims to detect, plus the correct installation.
// Nothing broken is ever written into the repository.
//
// Part 1 audits the real deployed set.
//
// Part 2 is the PERSISTENCE guard for the Written product: it renders a
// fresh head through tools/pastpapers/render_common.py::head_meta() (the
// one seam every solvedQP/ page passes through) and fails if the snippet
// is ever removed from the builder — independent of what today's
// generated files happen to contain.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import {
  analyzeHtml, auditDeployed, summarize, CANONICAL_ID, HOUSE_SNIPPET, KEEP_HTML,
} from "./ga_coverage.mjs";
import { ROOT } from "./deploy_set.mjs";

const wrap = (head) => `<!DOCTYPE html><html><head><title>t</title>${head}</head><body>x</body></html>`;
const LOADER = (id) => `<script async src="https://www.googletagmanager.com/gtag/js?id=${id}"></script>`;
const CONFIG = (id) => `<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${id}');</script>`;

// -------------------------------------------------------------
// 0. NEGATIVE / POSITIVE CONTROLS (in memory)
// -------------------------------------------------------------
describe("analyser — controls on in-memory pages", () => {
  test("correct canonical single installation (compact house form) passes", () => {
    const r = analyzeHtml(wrap(HOUSE_SNIPPET));
    assert.deepEqual(r.problems, []);
    assert.equal(r.ok, true);
    assert.deepEqual(r.loaders, [CANONICAL_ID]);
    assert.deepEqual(r.configs, [CANONICAL_ID]);
  });
  test("correct canonical installation in the expanded root-index form passes", () => {
    const html = wrap(`${LOADER(CANONICAL_ID)}<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '${CANONICAL_ID}', { page_title: 'x' });
</script>`);
    assert.equal(analyzeHtml(html).ok, true);
  });
  test("no GA at all -> missing", () => {
    const r = analyzeHtml(wrap(`<meta name="x">`));
    assert.deepEqual(r.problems, ["missing"]);
  });
  test("a commented-out snippet does not count as installed", () => {
    const r = analyzeHtml(wrap(`<!-- ${HOUSE_SNIPPET} -->`));
    assert.deepEqual(r.problems, ["missing"]);
  });
  test("wrong Measurement ID -> wrong-id", () => {
    const r = analyzeHtml(wrap(LOADER("G-BKBK70STQL") + CONFIG("G-BKBK70STQL")));
    assert.ok(r.problems.some((p) => p === "wrong-id(G-BKBK70STQL)"), r.problems.join());
    assert.equal(r.ok, false);
  });
  test("two different GA IDs on one page -> multiple-ids + wrong-id", () => {
    const r = analyzeHtml(wrap(LOADER(CANONICAL_ID) + CONFIG(CANONICAL_ID) + LOADER("G-7J47R7988H") + CONFIG("G-7J47R7988H")));
    assert.ok(r.problems.some((p) => p.startsWith("multiple-ids")), r.problems.join());
    assert.ok(r.problems.some((p) => p.startsWith("wrong-id(G-7J47R7988H)")));
    assert.equal(r.ok, false);
  });
  test("duplicate canonical loader -> duplicate-loader", () => {
    const r = analyzeHtml(wrap(LOADER(CANONICAL_ID) + LOADER(CANONICAL_ID) + CONFIG(CANONICAL_ID)));
    assert.ok(r.problems.includes("duplicate-loader(2)"), r.problems.join());
  });
  test("duplicate canonical config -> duplicate-config", () => {
    const r = analyzeHtml(wrap(HOUSE_SNIPPET + HOUSE_SNIPPET));
    assert.ok(r.problems.includes("duplicate-config(2)"), r.problems.join());
    assert.ok(r.problems.includes("duplicate-loader(2)"));
    assert.ok(r.problems.includes("gtag-js-count(2)"));
  });
  test("UA- legacy tag -> ua-legacy", () => {
    const r = analyzeHtml(wrap(`<script>ga('create','UA-12345678-1','auto');</script>`));
    assert.ok(r.problems.includes("ua-legacy(UA-12345678-1)"), r.problems.join());
    assert.equal(r.ok, false);
  });
  test("legacy analytics.js loader -> legacy-analytics-js", () => {
    const r = analyzeHtml(wrap(HOUSE_SNIPPET + `<script async src="https://www.google-analytics.com/analytics.js"></script>`));
    assert.ok(r.problems.includes("legacy-analytics-js"), r.problems.join());
  });
  test("loader without config / config without loader -> malformed", () => {
    assert.ok(analyzeHtml(wrap(LOADER(CANONICAL_ID))).problems.includes("no-config"));
    assert.ok(analyzeHtml(wrap(CONFIG(CANONICAL_ID))).problems.includes("no-loader"));
  });
  test("config without gtag('js', new Date()) -> gtag-js-count(0)", () => {
    const r = analyzeHtml(wrap(LOADER(CANONICAL_ID) + `<script>function gtag(){dataLayer.push(arguments);}gtag('config','${CANONICAL_ID}');</script>`));
    assert.ok(r.problems.includes("gtag-js-count(0)"), r.problems.join());
  });
});

// -------------------------------------------------------------
// 1. THE DEPLOYED SET
// -------------------------------------------------------------
describe("deployed HTML — exactly one canonical GA4 installation per page", () => {
  const audit = auditDeployed();
  const s = summarize(audit);
  test("the served HTML set is non-trivial and every page is analysed", () => {
    assert.ok(KEEP_HTML.length > 200, `only ${KEEP_HTML.length} served HTML pages?`);
    assert.equal(audit.total, KEEP_HTML.length);
  });
  test("no served page is missing GA4", () => {
    const bad = s.bad.filter((r) => r.problems.includes("missing")).map((r) => r.path);
    assert.deepEqual(bad, []);
  });
  test("no served page carries a wrong or second Measurement ID", () => {
    const bad = s.bad.filter((r) => r.problems.some((p) => /^(wrong-id|multiple-ids)/.test(p)))
      .map((r) => `${r.path} ${r.problems.join(" ")}`);
    assert.deepEqual(bad, []);
  });
  test("no served page has a duplicate loader or config", () => {
    const bad = s.bad.filter((r) => r.problems.some((p) => p.startsWith("duplicate-")))
      .map((r) => `${r.path} ${r.problems.join(" ")}`);
    assert.deepEqual(bad, []);
  });
  test("no served page carries a UA- tag or analytics.js", () => {
    const bad = s.bad.filter((r) => r.problems.some((p) => /^(ua-legacy|legacy-analytics-js)/.test(p)))
      .map((r) => `${r.path} ${r.problems.join(" ")}`);
    assert.deepEqual(bad, []);
  });
  test("coverage is 100% of the served HTML set", () => {
    const offenders = s.bad.map((r) => `${r.path}  ${r.problems.join(" ")}`);
    assert.deepEqual(offenders, [], `\n${offenders.join("\n")}`);
    assert.equal(s.ok, s.total);
  });
  test("every served page contains the canonical ID literally exactly twice (loader + config)", () => {
    // Guards a page that hides the ID inside a variable, or repeats it a third time in dead code.
    const odd = [];
    for (const rel of KEEP_HTML) {
      const html = fs.readFileSync(path.join(ROOT, rel), "utf8").replace(/<!--[\s\S]*?-->/g, "");
      const n = html.split(CANONICAL_ID).length - 1;
      if (n !== 2) odd.push(`${rel} (${n})`);
    }
    assert.deepEqual(odd, []);
  });
});

// -------------------------------------------------------------
// 2. WRITTEN PRODUCT — PERSISTENCE GUARD ON THE CANONICAL BUILDER
// -------------------------------------------------------------
describe("Written builder — head_meta() emits the snippet on a FRESH render", () => {
  const py = process.platform === "win32" ? "python" : "python3";
  const render = (publish) => execFileSync(py, ["-c",
    "import sys; sys.path.insert(0, 'tools/pastpapers'); import render_common as r; " +
    `print('\\n'.join(r.head_meta('T', 'D', '/solvedQP/x.html', ${publish ? "True" : "False"})))`],
    { cwd: ROOT, encoding: "utf8" });
  for (const publish of [true, false]) {
    test(`head_meta(publish=${publish}) renders exactly one canonical installation`, () => {
      const head = render(publish);
      const r = analyzeHtml(head + "</head><body></body></html>");
      assert.deepEqual(r.problems, [], head);
      assert.equal(r.loaders[0], CANONICAL_ID);
    });
  }
  test("render_common exposes GA4_MEASUREMENT_ID === canonical and head_meta() uses it", () => {
    const src = fs.readFileSync(path.join(ROOT, "tools/pastpapers/render_common.py"), "utf8");
    assert.match(src, new RegExp(`GA4_MEASUREMENT_ID = '${CANONICAL_ID}'`));
    const body = src.slice(src.indexOf("def head_meta("));
    assert.match(body.slice(0, body.indexOf("\ndef ", 1)), /o\.extend\(GA4_SNIPPET\)/);
  });
  test("every Written builder routes its head through head_meta()", () => {
    for (const b of ["build_paper.py", "build_index.py", "build_questions_year.py",
                     "build_solvedqp_home.py", "build_topic_map.py", "build_sample.py"]) {
      const src = fs.readFileSync(path.join(ROOT, "tools/pastpapers", b), "utf8");
      assert.match(src, /head_meta\(/, `${b} no longer calls head_meta()`);
    }
  });
  test("Oral Notes template still carries the canonical snippet exactly once", () => {
    const html = fs.readFileSync(path.join(ROOT, "tools/notes/template/shell_head.html"), "utf8");
    const r = analyzeHtml(html + "</head><body></body></html>");
    assert.deepEqual(r.problems, []);
  });
});
