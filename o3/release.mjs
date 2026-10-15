// O-3 private-content delivery: release packages, the public pin, and verification.
//
// The LOHAN series ("MIW MEO Class 1 Engineering Study Standard") lives in the PRIVATE
// repository nickmarineengr-aiLiterate/miw-protected-notes. This public repository holds
// only the pin: release id, package sha256, per-file sha256 and counts. A production build
// fetches the pinned package, verifies it completely, and mounts it behind the unchanged
// ORAL_QB_NOTES edge gate (middleware.js -> api/_lib/routes.js).
//
// Ported from the locally qualified prototype (LOHAN publication-prep 13 Oct 2026, 68/68,
// 20/20 mutants). Extension: "replace" entries let the full Notes index and manifest (titles,
// summaries, keywords: private under Founder FD-P2) replace their public IDs-only versions,
// but only when the public file on disk is byte-identical to the one the pin names.
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

export const FORMAT = "miw-protected-release/2";
export const PIN_FORMAT = "miw-protected-pin/2";
export const SERIES_KEY = "lohan-notes";
export const MOUNT = "meoclass1/oralnotes/";
export const PAGE_RE = /^lohan-notes-p([1-9]\d?)\.html$/;
export const REPLACEABLE = new Set(["meoclass1/oralnotes/index.html", "meoclass1/oralnotes/notes_content_index.json"]);
export const ENTITLEMENT = "ORAL_QB_NOTES";
export const GATE = '<script>if(!/miw_auth=1/.test(document.cookie)){window.location.replace("/SQ/pay.html");}</script>';

export const sha256 = (b) => crypto.createHash("sha256").update(b).digest("hex");

export function canonical(v) {
  if (Array.isArray(v)) return `[${v.map(canonical).join(",")}]`;
  if (v && typeof v === "object") {
    return `{${Object.keys(v).sort().map((k) => `${JSON.stringify(k)}:${canonical(v[k])}`).join(",")}}`;
  }
  return JSON.stringify(v);
}

/** Recount from markup, so declared totals can never drift from the content. */
export function countPage(html) {
  return {
    topics: (html.match(/<div class="topic-block" id="topic-p\d+-\d+"/g) || []).length,
    gated: html.split(GATE).length - 1 === 1 && !html.includes("GATE SCRIPT STRIPPED"),
  };
}

/**
 * Build a release package from the private repository checkout.
 *   pages/<name>     -> mounted at MOUNT/<name>        (21 LOHAN pages)
 *   replace/<path>   -> replaces the public <path>      (full Notes index and manifest)
 *   specs/<name>     -> private authoring inputs, never mounted
 * `publicTree` supplies the public bytes each replacement starts from.
 */
export function buildPackage({ privateRoot, publicTree, releaseId }) {
  const files = [];
  const add = (rel, abs) => files.push({ path: rel, bytes: fs.readFileSync(abs) });
  const ov = path.join(privateRoot, "lohan", "overlay", "meoclass1", "oralnotes");
  for (const name of fs.readdirSync(ov).sort()) {
    if (PAGE_RE.test(name)) add(`pages/${name}`, path.join(ov, name));
    else if (REPLACEABLE.has(MOUNT + name)) add(`replace/${MOUNT}${name}`, path.join(ov, name));
    else throw new Error(`UNEXPECTED_OVERLAY_FILE ${name}`);
  }
  const sp = path.join(privateRoot, "lohan", "source", "tools", "notes", "specs", "lohan");
  for (const name of fs.readdirSync(sp).sort()) add(`specs/${name}`, path.join(sp, name));
  files.sort((a, b) => (a.path < b.path ? -1 : a.path > b.path ? 1 : 0));
  let pages = 0, specs = 0, topics = 0, replace = 0;
  for (const f of files) {
    if (f.path.startsWith("pages/")) {
      pages++;
      const c = countPage(f.bytes.toString("utf8"));
      if (!c.gated) throw new Error(`PAGE_NOT_GATED ${f.path}`);
      topics += c.topics;
    } else if (f.path.startsWith("replace/")) replace++;
    else specs++;
  }
  const replaceFiles = files.filter((f) => f.path.startsWith("replace/")).map((f) => {
    const rel = f.path.slice("replace/".length);
    return { path: rel, sha256: sha256(f.bytes), public_sha256: sha256(fs.readFileSync(path.join(publicTree, ...rel.split("/")))) };
  });
  const manifest = {
    format: FORMAT, series: SERIES_KEY, release_id: releaseId, entitlement: ENTITLEMENT,
    totals: { pages, specs, topics, replace },
    files: files.map((f) => ({ path: f.path, sha256: sha256(f.bytes), bytes: f.bytes.length })),
  };
  const pkg = { manifest, blobs: Object.fromEntries(files.map((f) => [f.path, f.bytes.toString("base64")])) };
  const bytes = Buffer.from(canonical(pkg), "utf8");
  return { bytes, sha256: sha256(bytes), manifest, replaceFiles };
}

/** The public pin: hashes, paths and counts only. Never content. */
export function makePin({ manifest, packageSha, replaceFiles, store }) {
  return {
    format: PIN_FORMAT, series: manifest.series, release_id: manifest.release_id,
    package_sha256: packageSha, entitlement: manifest.entitlement, mount: MOUNT,
    totals: manifest.totals, store,
    deploy_files: manifest.files.filter((f) => f.path.startsWith("pages/"))
      .map((f) => ({ path: f.path.slice("pages/".length), sha256: f.sha256 })),
    replace_files: replaceFiles,
  };
}

/**
 * Verify a fetched package against the pin and return the exact writes to make.
 * Every failure throws: the caller fails the build, and the previous deployment stays live.
 * `requiredEntitlementForPath` is the PRODUCTION route table (api/_lib/routes.js).
 */
export function verifyPackage({ pkgBytes, pin, publicDir, requiredEntitlementForPath }) {
  if (sha256(pkgBytes) !== pin.package_sha256) throw new Error("BUILD_FAIL_PACKAGE_HASH");
  const pkg = JSON.parse(pkgBytes.toString("utf8"));
  const m = pkg.manifest;
  if (m.format !== FORMAT || pin.format !== PIN_FORMAT || m.release_id !== pin.release_id || m.series !== SERIES_KEY)
    throw new Error("BUILD_FAIL_MANIFEST_IDENTITY");
  if (m.entitlement !== ENTITLEMENT || pin.entitlement !== ENTITLEMENT) throw new Error("BUILD_FAIL_ENTITLEMENT");
  const blobPaths = Object.keys(pkg.blobs).sort();
  const manPaths = m.files.map((f) => f.path).sort();
  if (JSON.stringify(blobPaths) !== JSON.stringify(manPaths)) throw new Error("BUILD_FAIL_MANIFEST_PATHS");
  const bytesOf = {};
  for (const f of m.files) {
    const b = Buffer.from(pkg.blobs[f.path], "base64");
    if (sha256(b) !== f.sha256 || b.length !== f.bytes) throw new Error(`BUILD_FAIL_FILE_HASH ${f.path}`);
    bytesOf[f.path] = b;
  }
  const pages = m.files.filter((f) => f.path.startsWith("pages/"));
  const want = pin.deploy_files.map((f) => `${f.path}:${f.sha256}`).sort();
  const got = pages.map((f) => `${f.path.slice(6)}:${f.sha256}`).sort();
  if (JSON.stringify(want) !== JSON.stringify(got)) throw new Error("BUILD_FAIL_PIN_MISMATCH");
  const reps = m.files.filter((f) => f.path.startsWith("replace/"));
  const wantR = (pin.replace_files || []).map((r) => `${r.path}:${r.sha256}`).sort();
  const gotR = reps.map((f) => `${f.path.slice(8)}:${f.sha256}`).sort();
  if (JSON.stringify(wantR) !== JSON.stringify(gotR)) throw new Error("BUILD_FAIL_PIN_MISMATCH replace");
  let topics = 0;
  for (const f of pages) {
    const c = countPage(bytesOf[f.path].toString("utf8"));
    if (!c.gated) throw new Error(`BUILD_FAIL_UNGATED_PAGE ${f.path}`);
    topics += c.topics;
  }
  const recount = { pages: pages.length, specs: m.files.length - pages.length - reps.length, topics, replace: reps.length };
  for (const k of Object.keys(recount)) {
    if (recount[k] !== m.totals[k] || recount[k] !== pin.totals[k]) throw new Error(`BUILD_FAIL_TOTALS ${k}`);
  }
  const writes = [];
  for (const f of pages) {
    const name = f.path.slice(6);
    if (!PAGE_RE.test(name)) throw new Error(`BUILD_FAIL_UNSAFE_PATH ${name}`);
    const rel = MOUNT + name;
    if (requiredEntitlementForPath("/" + rel) !== ENTITLEMENT) throw new Error(`BUILD_FAIL_UNGATED_MOUNT ${rel}`);
    if (fs.existsSync(path.join(publicDir, ...rel.split("/")))) throw new Error(`BUILD_FAIL_PUBLIC_COLLISION ${rel}`);
    writes.push({ rel, bytes: bytesOf[f.path], kind: "mount" });
  }
  for (const r of pin.replace_files || []) {
    if (!REPLACEABLE.has(r.path)) throw new Error(`BUILD_FAIL_UNSAFE_PATH ${r.path}`);
    if (requiredEntitlementForPath("/" + r.path) !== ENTITLEMENT) throw new Error(`BUILD_FAIL_UNGATED_MOUNT ${r.path}`);
    const p = path.join(publicDir, ...r.path.split("/"));
    if (!fs.existsSync(p) || sha256(fs.readFileSync(p)) !== r.public_sha256) throw new Error(`BUILD_FAIL_PUBLIC_BASE ${r.path}`);
    writes.push({ rel: r.path, bytes: bytesOf[`replace/${r.path}`], kind: "replace" });
  }
  return { writes, totals: recount, release_id: m.release_id };
}
