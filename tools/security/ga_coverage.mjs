// =============================================================
// Marine Intelligence Weekly — GA4 coverage auditor
//
// Every SERVED HTML page must carry exactly ONE valid installation of
// the canonical GA4 property. "Valid installation" is the house snippet:
//
//   <script async src="https://www.googletagmanager.com/gtag/js?id=G-…"></script>
//   <script> window.dataLayer = …; function gtag(){…}
//            gtag('js', new Date()); gtag('config', 'G-…'); </script>
//
// The served set is deploy_set.mjs KEEP — the same computation used by
// deploy_surface.test.mjs and link_integrity.test.mjs — so the coverage
// denominator is exactly what Vercel serves, never review/docs/tools.
//
// analyzeHtml() is a pure function over page text so the contract test
// can run negative controls on in-memory fixtures. Nothing broken is
// ever written into the repository to make a control fire.
// =============================================================

import fs from "node:fs";
import path from "node:path";
import { KEEP, ROOT } from "./deploy_set.mjs";

export const CANONICAL_ID = "G-0YEE2CBNP5";

// The compact house snippet: the form tools/notes/template/shell_head.html,
// meoclass1/ and (via render_common.GA4_SNIPPET) every Written page emit.
// Base page-view only -- no page_location/page_path override, no events.
export const HOUSE_SNIPPET =
`<script async src="https://www.googletagmanager.com/gtag/js?id=${CANONICAL_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${CANONICAL_ID}');</script>`;

const LOADER_RE = /<script\b[^>]*\bsrc\s*=\s*["']https?:\/\/www\.googletagmanager\.com\/gtag\/js\?id=([A-Za-z0-9-]+)["'][^>]*>/gi;
const CONFIG_RE = /gtag\(\s*["']config["']\s*,\s*["']([A-Za-z0-9-]+)["']/gi;
const JS_RE = /gtag\(\s*["']js["']\s*,\s*new Date\(\)\s*\)/gi;
const UA_RE = /\bUA-\d{4,}-\d+\b/g;
const GA_LEGACY_LOADER_RE = /google-analytics\.com\/(analytics|ga)\.js/gi;

const STRIP_COMMENTS = /<!--[\s\S]*?-->/g;

/**
 * Analyse one HTML document. Returns:
 *   { loaders: [ids], configs: [ids], js: n, ua: [ids], legacyLoader: bool,
 *     ids: Set, ok: bool, problems: [string] }
 * `ok` means: exactly one loader, exactly one config, one gtag('js'),
 * all IDs === CANONICAL_ID, no UA tags, no legacy analytics.js loader.
 */
export function analyzeHtml(html, canonical = CANONICAL_ID) {
  const text = html.replace(STRIP_COMMENTS, (m) => m.replace(/[^\n]/g, " "));
  const loaders = [...text.matchAll(LOADER_RE)].map((m) => m[1]);
  const configs = [...text.matchAll(CONFIG_RE)].map((m) => m[1]);
  const js = [...text.matchAll(JS_RE)].length;
  const ua = [...new Set([...text.matchAll(UA_RE)].map((m) => m[0]))];
  const legacyLoader = GA_LEGACY_LOADER_RE.test(text);
  GA_LEGACY_LOADER_RE.lastIndex = 0;
  const ids = new Set([...loaders, ...configs]);
  const problems = [];
  if (loaders.length === 0 && configs.length === 0) problems.push("missing");
  else {
    if (loaders.length === 0) problems.push("no-loader");
    if (configs.length === 0) problems.push("no-config");
    if (loaders.length > 1) problems.push(`duplicate-loader(${loaders.length})`);
    if (configs.length > 1) problems.push(`duplicate-config(${configs.length})`);
    if (js !== 1) problems.push(`gtag-js-count(${js})`);
    const wrong = [...ids].filter((i) => i !== canonical);
    if (wrong.length) problems.push(`wrong-id(${wrong.join(",")})`);
    if (ids.size > 1) problems.push(`multiple-ids(${[...ids].join(",")})`);
  }
  if (ua.length) problems.push(`ua-legacy(${ua.join(",")})`);
  if (legacyLoader) problems.push("legacy-analytics-js");
  return { loaders, configs, js, ua, legacyLoader, ids, ok: problems.length === 0, problems };
}

export const KEEP_HTML = KEEP.filter((f) => f.toLowerCase().endsWith(".html"));

/** Audit every served HTML page. Returns { total, ok, rows:[{path, ...analysis}] }. */
export function auditDeployed(files = KEEP_HTML) {
  const rows = files.map((rel) => {
    const html = fs.readFileSync(path.join(ROOT, rel), "utf8");
    return { path: rel, ...analyzeHtml(html) };
  });
  return { total: rows.length, ok: rows.filter((r) => r.ok).length, rows };
}

export function summarize(audit) {
  const bad = audit.rows.filter((r) => !r.ok);
  const count = (pred) => audit.rows.filter(pred).length;
  return {
    total: audit.total,
    ok: audit.ok,
    missing: count((r) => r.problems.includes("missing")),
    wrongId: count((r) => r.problems.some((p) => p.startsWith("wrong-id"))),
    duplicate: count((r) => r.problems.some((p) => p.startsWith("duplicate-"))),
    multipleIds: count((r) => r.problems.some((p) => p.startsWith("multiple-ids"))),
    ua: count((r) => r.problems.some((p) => p.startsWith("ua-legacy"))),
    malformed: count((r) => r.problems.some((p) => /^(no-loader|no-config|gtag-js-count|legacy-analytics-js)/.test(p))),
    bad,
  };
}

// CLI: node tools/security/ga_coverage.mjs
if (process.argv[1] && path.basename(process.argv[1]) === "ga_coverage.mjs") {
  const s = summarize(auditDeployed());
  console.log(`deployed HTML: ${s.total}\ncanonical GA: ${s.ok}\nmissing: ${s.missing}\nwrong ID: ${s.wrongId}\nduplicates: ${s.duplicate}\nmultiple IDs: ${s.multipleIds}\nUA: ${s.ua}\nmalformed: ${s.malformed}\ncoverage: ${(100 * s.ok / s.total).toFixed(1)}%`);
  for (const r of s.bad) console.log(`  ${r.path}  ${r.problems.join(" ")}`);
}
