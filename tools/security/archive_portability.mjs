// =============================================================
// Marine Intelligence Weekly — archive-portability resolver
//
// A magazine issue is published at the site root as `indexNN.html` and is
// LATER copied into the archive as `archive/issueNN.html` (playbook §3.2(b),
// remediation R1). A reference written relative to the page — `assets/x.webp`,
// `index29.html` — silently changes meaning when the page moves down a
// directory. This module answers, for a page that has not been moved yet:
//
//     "if this page were served from archive/issueNN.html instead of
//      /indexNN.html, would every one of its references still lead to the
//      SAME file it leads to today?"
//
//     node tools/security/archive_portability.mjs            # ledger
//     node tools/security/archive_portability.mjs --json     # machine-readable
//
// WHY "SAME FILE" AND NOT "RESOLVES"
//   Two distinct failures hide under a relative path. `assets/logo.webp`
//   becomes `archive/assets/logo.webp`, which does not exist — a loud 404.
//   But `index.html` becomes `archive/index.html`, which DOES exist: the
//   archive listing page. That link does not break, it silently points
//   somewhere else. Only an identity comparison catches the second class,
//   so this contract compares RESOLVED TARGETS, never mere resolvability.
//
// WHAT IS PORTABLE BY CONSTRUCTION (not a defect)
//   * root-absolute      `/assets/x.webp`  — depth-invariant by definition
//   * same-host absolute `https://marineintelligenceweekly.com/x` — folded
//                        to root-absolute by the shared resolver
//   * self references    `#feature`, `?v=2` — these address the CONTAINING
//                        document, so their target is *meant* to follow the
//                        page to its new location. A pure fragment is the
//                        one case where a changed target is correct, which
//                        is why it is excluded rather than "fixed".
//   * everything the link-integrity resolver already ignores: external
//     URLs, mailto:, tel:, javascript:, data:, blob:, and the contents of
//     comments, <script>, <style>, <pre>, <code> and <template>.
//
// HOW THE SIMULATION WORKS — NO ARCHIVE COPY IS EVER WRITTEN
//   The served set is extended with a VIRTUAL `archive/issueNN.html` backed
//   by the bytes of the real `indexNN.html`, and the page's references are
//   resolved a second time from that path. Modelling the destination is
//   what makes self-referential fragments resolve honestly; without it every
//   `#anchor` would read as a false break. Nothing touches disk.
//
// This module reuses tools/security/link_integrity.mjs for extraction and
// resolution, so "what counts as a reference" cannot drift between the two
// contracts.
// =============================================================

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { ROOT, KEEP, TRACKED } from "./deploy_set.mjs";
import { buildContext, extractRefs, resolveRef, SAME_HOST } from "./link_integrity.mjs";

/** Issues that exist at the root but are not yet archived (playbook R1). */
export const ARCHIVE_ISSUES = [23, 24, 25, 26, 27, 28, 29, 30];

export const rootPageFor = (n) => `index${n}.html`;
export const archivePathFor = (n) => `archive/issue${n}.html`;

/**
 * Is this reference's meaning independent of the depth it is served from?
 * Returns a reason string when portable by construction, else null.
 */
export function portableByConstruction(raw) {
  let s = raw.trim();
  const own = s.match(SAME_HOST);
  if (own) s = s.slice(own[0].length) || "/";
  if (s.startsWith("/")) return "root-absolute";
  // A reference with no path part addresses the containing document.
  if (s === "" || s.startsWith("#") || s.startsWith("?")) return "self-reference";
  return null;
}

/**
 * Build a context whose served set also contains the virtual archive copies.
 * `readFile` serves those copies the bytes of their root original.
 */
export function buildArchiveContext(issues = ARCHIVE_ISSUES, readRoot = defaultRead,
  keepList = KEEP, trackedList = TRACKED) {
  const virtual = new Map();
  for (const n of issues) {
    const html = readRoot(rootPageFor(n));
    if (html != null) virtual.set(archivePathFor(n), html);
  }
  const read = (rel) => (virtual.has(rel) ? virtual.get(rel) : readRoot(rel));
  const keep = [...keepList, ...virtual.keys()];
  const tracked = [...trackedList, ...virtual.keys()];
  return { ctx: buildContext(keep, tracked, read), virtual, read };
}

function defaultRead(rel) {
  try { return fs.readFileSync(path.join(ROOT, rel), "utf8"); } catch { return null; }
}

/** Audit one issue. Returns {issue, page, refsScanned, checked, defects[]}. */
export function auditIssue(n, sim) {
  const page = rootPageFor(n);
  const arch = archivePathFor(n);
  const html = sim.read(page);
  if (html == null) return { issue: n, page, missing: true, refsScanned: 0, checked: 0, defects: [] };

  const defects = [];
  let checked = 0;
  const refs = extractRefs(html);
  for (const r of refs) {
    const atRoot = resolveRef(page, r.raw, sim.ctx);
    if (!atRoot) continue;                       // out of scope (external, mailto, …)
    const why = portableByConstruction(r.raw);
    if (why) continue;                           // depth-invariant by definition
    checked++;
    const atArchive = resolveRef(arch, r.raw, sim.ctx);
    const rootTarget = atRoot.resolved;
    const archTarget = atArchive ? atArchive.resolved : null;
    if (rootTarget && archTarget === rootTarget) continue;   // portable
    defects.push({
      issue: n, source: page, line: r.line, attr: r.attr, raw: r.raw,
      rootTarget, archiveTarget: archTarget,
      archiveWouldResolve: Boolean(archTarget),
      kind: archTarget ? "silent-misresolution" : "archive-404",
      suggestion: rootTarget ? "/" + rootTarget : null,
    });
  }
  return { issue: n, page, refsScanned: refs.length, checked, defects };
}

export function audit(issues = ARCHIVE_ISSUES, sim = buildArchiveContext(issues)) {
  const perIssue = issues.map((n) => auditIssue(n, sim));
  return {
    perIssue,
    defects: perIssue.flatMap((r) => r.defects),
    checked: perIssue.reduce((a, r) => a + r.checked, 0),
    refsScanned: perIssue.reduce((a, r) => a + r.refsScanned, 0),
  };
}

// --- CLI ----------------------------------------------------------------
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const res = audit();
  if (process.argv.includes("--json")) {
    process.stdout.write(JSON.stringify(res, null, 2) + "\n");
  } else {
    console.log(`issues simulated:        ${res.perIssue.length}  (${ARCHIVE_ISSUES.join(", ")})`);
    console.log(`runtime refs scanned:    ${res.refsScanned}`);
    console.log(`depth-sensitive checked: ${res.checked}`);
    console.log(`portability defects:     ${res.defects.length}`);
    for (const r of res.perIssue) {
      const mark = r.defects.length ? "FAIL" : "ok  ";
      console.log(`  ${mark} ${r.page}  refs ${r.refsScanned}, checked ${r.checked}, defects ${r.defects.length}`);
      for (const d of r.defects) {
        console.log(`        ${d.source}:${d.line} ${d.attr}="${d.raw}"  [${d.kind}]`);
        console.log(`            at root    -> ${d.rootTarget}`);
        console.log(`            at archive -> ${d.archiveTarget ?? "(404)"}    fix: ${d.suggestion}`);
      }
    }
    if (res.defects.length) process.exitCode = 1;
  }
}
