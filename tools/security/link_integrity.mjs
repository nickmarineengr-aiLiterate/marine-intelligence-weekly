// =============================================================
// Marine Intelligence Weekly — link-integrity resolver
//
// Resolves every runtime reference on every SERVED HTML page against the
// SERVED file set (deploy_set.mjs KEEP), so "does this control lead
// somewhere" is a computed fact rather than an impression. Used by
// link_integrity.test.mjs (the contract) and runnable directly for a
// ledger:
//
//     node tools/security/link_integrity.mjs            # summary + defects
//     node tools/security/link_integrity.mjs --json     # machine-readable
//
// WHAT IS A RUNTIME REFERENCE
//   href / src / poster / action / data-src attributes on elements in
//   the rendered document, plus srcset candidates. Comments, <script>,
//   <style>, <pre>, <code> and <template> bodies are removed first, so
//   code examples and inline JS never masquerade as links.
//
// WHAT IS NOT CHECKED (by design)
//   external URLs (scheme or protocol-relative, except the site's own host,
//   which is folded to root-absolute), mailto:, tel:, sms:,
//   javascript:, data:, blob:, about:, and empty hrefs. Query strings
//   are stripped before resolution -- `?v=3` must never make a real file
//   read as missing. Runtime-generated paths built in JS are out of
//   scope for the attribute pass; the manifest fetches those scripts
//   make are covered by the toolchain's own contract tests.
//
// RESOLUTION
//   A reference resolves if the target is a served file, or a served
//   directory index (`dir/` -> `dir/index.html`), or -- because Vercel
//   serves `page.html` at `/page` -- an extensionless path whose `.html`
//   sibling is served. Percent-encoding is decoded. A path that exists
//   only under a different letter-case is a CASE MISMATCH (Vercel is
//   case-sensitive; Windows checkouts are not, which is how these ship).
//
// FRAGMENTS
//   `#id` must match an id="" or <a name=""> in the target document (or
//   the source document for a bare `#id`). `#`, `#top` and `#!` are
//   conventional no-ops and pass; hash routes (`#/x`, `#tab=x`) are opaque
//   and pass; ids a page renders from its own data literal are credited
//   only through RUNTIME_ANCHOR_PROVIDERS, each with its render site cited.
//
// ENTITLEMENT
//   Every served path is classified with the same prefix policy the edge
//   middleware uses (api/_lib/routes.js): /solvedQP/ and
//   /meoclass1/pastpapers/ are SOLVED_QP; /meoclass1/ is ORAL_QB_NOTES;
//   /SQ/, /api/, /assets/ and everything else are PUBLIC. A reference
//   from an ORAL page into a SOLVED_QP page (or the reverse) is a
//   CROSS-ENTITLEMENT reference: a customer who bought one product is
//   being handed a control that 302s them to a paywall for the other.
//   PUBLIC -> paid is intentional (samples, storefront CTAs) and is not
//   a defect. A reference from a served page to a TRACKED-BUT-EXCLUDED
//   file is KEEP -> EXCLUDED: it worked in the checkout and 404s live.
// =============================================================

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { ROOT, KEEP, TRACKED } from "./deploy_set.mjs";

// --- entitlement policy (mirrors api/_lib/routes.js; kept literal so the
//     scanner has no runtime dependency on the edge bundle) ---------------
const PUBLIC_PREFIXES = ["/SQ/", "/api/", "/assets/"];
const ROUTE_RULES = [
  { prefix: "/solvedQP/", requires: "SOLVED_QP" },
  { prefix: "/meoclass1/pastpapers/", requires: "SOLVED_QP" },
  { prefix: "/meoclass1/oralnotes/", requires: "ORAL_QB_NOTES" },
  { prefix: "/meoclass1/", requires: "ORAL_QB_NOTES" },
];
export function entitlementFor(relPath) {
  const p = "/" + relPath.replace(/^\/+/, "");
  for (const pub of PUBLIC_PREFIXES) if (p.startsWith(pub)) return "PUBLIC";
  for (const r of ROUTE_RULES) {
    if (p.startsWith(r.prefix) || p === r.prefix.replace(/\/$/, "")) return r.requires;
  }
  return "PUBLIC";
}

// --- reference extraction ---------------------------------------------
const STRIP_BLOCKS = /<!--[\s\S]*?-->|<script\b[^>]*>[\s\S]*?<\/script\s*>|<style\b[^>]*>[\s\S]*?<\/style\s*>|<pre\b[^>]*>[\s\S]*?<\/pre\s*>|<code\b[^>]*>[\s\S]*?<\/code\s*>|<template\b[^>]*>[\s\S]*?<\/template\s*>/gi;
const ATTR_RE = /\b(href|src|poster|action|data-src|srcset)\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))/gi;
const SKIP_SCHEME = /^(https?:|\/\/|mailto:|tel:|sms:|javascript:|data:|blob:|about:)/i;
export const SAME_HOST = /^https?:\/\/(www\.)?marineintelligenceweekly\.com(?=[/?#]|$)/i;

function decodeEntities(s) {
  return s.replace(/&amp;/g, "&").replace(/&#39;/g, "'").replace(/&quot;/g, '"')
    .replace(/&lt;/g, "<").replace(/&gt;/g, ">");
}

/** Extract {attr, raw, line} references from an HTML document string. */
export function extractRefs(html) {
  const stripped = html.replace(STRIP_BLOCKS, (m) => m.replace(/[^\n]/g, " "));
  const refs = [];
  let m;
  while ((m = ATTR_RE.exec(stripped))) {
    const attr = m[1].toLowerCase();
    const val = decodeEntities((m[3] ?? m[4] ?? m[5] ?? "").trim());
    const line = stripped.slice(0, m.index).split("\n").length;
    if (attr === "srcset") {
      for (const cand of val.split(",")) {
        const url = cand.trim().split(/\s+/)[0];
        if (url) refs.push({ attr, raw: url, line });
      }
    } else if (val) {
      refs.push({ attr, raw: val, line });
    }
  }
  return refs;
}

// --- anchors ------------------------------------------------------------
const ID_RE = /\b(?:id|name)\s*=\s*("([^"]*)"|'([^']*)'|([^\s>]+))/gi;
const anchorCache = new Map();

// Pages whose section ids are rendered by their own inline script from a
// data literal in the same file. The static contract credits ONLY these,
// each read from the data the page really renders -- never a blanket "any
// string in a script counts". Add an entry only with the render site cited.
export const RUNTIME_ANCHOR_PROVIDERS = {
  // meoclass1/index.html renders `<div class="group-label" id="${g.id}">` for
  // every entry of `const QB_GROUPS = [...]`, and its own floating nav links
  // `#qb1`..`#qb10`; a hub-group deep link is therefore a real target.
  "meoclass1/index.html": (html) => {
    const m = html.match(/const QB_GROUPS = (\[[\s\S]*?\]);\s*\n/);
    if (!m || !/id="\$\{g\.id\}"/.test(html)) return [];
    try { return JSON.parse(m[1]).map((g) => g.id).filter(Boolean); } catch { return []; }
  },
};

export function anchorsOf(relPath, readFile) {
  if (anchorCache.has(relPath)) return anchorCache.get(relPath);
  const html = readFile(relPath);
  const ids = new Set();
  if (html != null) {
    // ids inside comments are not reachable targets; scripts may set them at
    // runtime but the static contract only credits static ids (plus the
    // cited runtime providers above).
    const stripped = html.replace(/<!--[\s\S]*?-->/g, "").replace(/<script\b[^>]*>[\s\S]*?<\/script\s*>/gi, "");
    let m;
    while ((m = ID_RE.exec(stripped))) ids.add(decodeEntities(m[2] ?? m[3] ?? m[4] ?? ""));
    const provider = RUNTIME_ANCHOR_PROVIDERS[relPath];
    if (provider) for (const id of provider(html)) ids.add(id);
  }
  anchorCache.set(relPath, ids);
  return ids;
}

// --- resolution ---------------------------------------------------------
function posixNormalize(p) {
  const out = [];
  for (const seg of p.split("/")) {
    if (seg === "" || seg === ".") continue;
    if (seg === "..") { if (out.length) out.pop(); else out.push(".."); continue; }
    out.push(seg);
  }
  return out.join("/");
}

/**
 * Resolve one raw reference from `sourceRel` (posix, served path).
 * Returns null for out-of-scope refs, else a record.
 */
export function resolveRef(sourceRel, raw, ctx) {
  // Same-host absolute URLs are internal references written the long way
  // round (the estate mixes both styles); reduce them to root-absolute.
  const original = raw;
  const own = raw.match(SAME_HOST);
  if (own) raw = raw.slice(own[0].length) || "/";
  if (SKIP_SCHEME.test(raw)) return null;
  const hashAt = raw.indexOf("#");
  let fragment = hashAt >= 0 ? raw.slice(hashAt + 1) : null;
  let pathPart = hashAt >= 0 ? raw.slice(0, hashAt) : raw;
  const qAt = pathPart.indexOf("?");
  const query = qAt >= 0 ? pathPart.slice(qAt) : "";
  if (qAt >= 0) pathPart = pathPart.slice(0, qAt);
  try { pathPart = decodeURIComponent(pathPart); } catch { /* keep raw */ }
  try { if (fragment != null) fragment = decodeURIComponent(fragment); } catch { /* keep raw */ }

  const srcDir = path.posix.dirname(sourceRel);
  let target;
  let escaped = false;
  if (pathPart === "") {
    target = sourceRel;                       // bare #fragment or ?query
  } else if (pathPart.startsWith("/")) {
    target = posixNormalize(pathPart);
    if (pathPart.endsWith("/")) target += "/";
  } else {
    target = posixNormalize(path.posix.join(srcDir === "." ? "" : srcDir, pathPart));
    if (pathPart.endsWith("/")) target += "/";
    if (target.startsWith("..")) escaped = true;
  }
  if (target === "" || target === "/") target = "index.html";

  // existence
  let resolved = null;
  let via = null;
  if (!escaped) {
    if (target.endsWith("/")) {
      const idx = target + "index.html";
      if (ctx.keep.has(idx)) { resolved = idx; via = "dir-index"; }
    } else if (ctx.keep.has(target)) {
      resolved = target; via = "file";
    } else if (ctx.keep.has(target + "/index.html")) {
      resolved = target + "/index.html"; via = "dir-index-noslash";
    } else if (!path.posix.extname(target) && ctx.keep.has(target + ".html")) {
      resolved = target + ".html"; via = "extensionless";
    }
  }
  let caseMatch = null;
  if (!resolved && !escaped) {
    const lower = target.toLowerCase();
    caseMatch = ctx.keepLower.get(lower) ?? ctx.keepLower.get(lower + "/index.html") ?? null;
  }
  const excluded = !resolved && !escaped && (ctx.excludedSet.has(target) ||
    ctx.excludedSet.has(target.replace(/\/$/, "") + "/index.html"))
    ? (ctx.excludedSet.has(target) ? target : target.replace(/\/$/, "") + "/index.html") : null;

  const rec = {
    source: sourceRel, raw: original, query, fragment, target, resolved, via,
    escaped, caseMatch, excluded,
    sourceEntitlement: entitlementFor(sourceRel),
    targetEntitlement: resolved ? entitlementFor(resolved) : (excluded ? entitlementFor(excluded) : null),
    fragmentOk: null,
  };
  if (resolved && fragment != null) {
    if (fragment === "" || fragment === "top" || fragment === "!") rec.fragmentOk = true;
    // Hash ROUTES (`#/path`, `#tab=search`) are read by the page's own script,
    // not matched against an element id; they are opaque to this contract.
    else if (fragment.startsWith("/") || fragment.includes("=")) rec.fragmentOk = true;
    else if (/\.html?$/i.test(resolved)) rec.fragmentOk = anchorsOf(resolved, ctx.readFile).has(fragment);
    else rec.fragmentOk = true;                // non-HTML targets: fragment is opaque
  }
  return rec;
}

// --- scan ---------------------------------------------------------------
export function buildContext(keepList = KEEP, trackedList = TRACKED, readFile = defaultRead) {
  const keep = new Set(keepList);
  const keepLower = new Map();
  for (const f of keepList) keepLower.set(f.toLowerCase(), f);
  const excludedSet = new Set(trackedList.filter((f) => !keep.has(f)));
  return { keep, keepLower, excludedSet, readFile };
}
function defaultRead(rel) {
  try { return fs.readFileSync(path.join(ROOT, rel), "utf8"); } catch { return null; }
}

export function scan(ctx = buildContext()) {
  anchorCache.clear();
  const pages = [...ctx.keep].filter((f) => /\.html?$/i.test(f)).sort();
  const records = [];
  for (const page of pages) {
    const html = ctx.readFile(page);
    if (html == null) continue;
    for (const r of extractRefs(html)) {
      const rec = resolveRef(page, r.raw, ctx);
      if (rec) records.push({ ...rec, attr: r.attr, line: r.line });
    }
  }
  return classify(records, pages.length);
}

export function classify(records, pagesScanned) {
  const broken = records.filter((r) => !r.resolved);
  const brokenLocal = broken.filter((r) => !r.excluded && !r.caseMatch);
  const keepToExcluded = broken.filter((r) => r.excluded);
  const caseMismatch = broken.filter((r) => !r.excluded && r.caseMatch);
  const deadFragments = records.filter((r) => r.resolved && r.fragmentOk === false);
  const crossEntitlement = records.filter((r) => r.resolved &&
    r.sourceEntitlement !== "PUBLIC" && r.targetEntitlement !== "PUBLIC" &&
    r.sourceEntitlement !== r.targetEntitlement);
  return {
    pagesScanned, refsScanned: records.length, records,
    brokenLocal, deadFragments, keepToExcluded, crossEntitlement, caseMismatch,
  };
}

// --- CLI ----------------------------------------------------------------
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const res = scan();
  const json = process.argv.includes("--json");
  const slim = (r) => ({ source: r.source, line: r.line, attr: r.attr, raw: r.raw, target: r.target,
    fragment: r.fragment, resolved: r.resolved, caseMatch: r.caseMatch, excluded: r.excluded,
    sourceEntitlement: r.sourceEntitlement, targetEntitlement: r.targetEntitlement });
  if (json) {
    const out = {
      pagesScanned: res.pagesScanned, refsScanned: res.refsScanned,
      brokenLocal: res.brokenLocal.map(slim), deadFragments: res.deadFragments.map(slim),
      keepToExcluded: res.keepToExcluded.map(slim), crossEntitlement: res.crossEntitlement.map(slim),
      caseMismatch: res.caseMismatch.map(slim),
    };
    process.stdout.write(JSON.stringify(out, null, 2) + "\n");
  } else {
    const line = (r) => `  ${r.source}:${r.line}  ${r.attr}="${r.raw}"${r.fragment != null && r.resolved ? "  -> " + r.resolved : ""}`;
    console.log(`HTML pages scanned:      ${res.pagesScanned}`);
    console.log(`runtime refs scanned:    ${res.refsScanned}`);
    console.log(`broken local refs:       ${res.brokenLocal.length}`);
    console.log(`dead fragments:          ${res.deadFragments.length}`);
    console.log(`KEEP -> EXCLUDED:        ${res.keepToExcluded.length}`);
    console.log(`cross-entitlement refs:  ${res.crossEntitlement.length}`);
    console.log(`case mismatches:         ${res.caseMismatch.length}`);
    const section = (title, arr) => { if (arr.length) { console.log(`\n${title}`); arr.forEach((r) => console.log(line(r))); } };
    section("BROKEN LOCAL", res.brokenLocal);
    section("DEAD FRAGMENTS", res.deadFragments);
    section("KEEP -> EXCLUDED", res.keepToExcluded);
    section("CROSS-ENTITLEMENT", res.crossEntitlement);
    section("CASE MISMATCH", res.caseMismatch);
  }
}
