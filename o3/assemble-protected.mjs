// O-3 build step (vercel.json "buildCommand"). It runs inside the Vercel build, in the
// repository root, which is also the static output directory (framework: null).
//
//   production (VERCEL_ENV=production): fetch the pinned release from the private repository
//     with MIW_NOTES_STORE_TOKEN (a Production-only, read-only token scoped to that one repo),
//     verify it completely (o3/release.mjs), then mount the 21 LOHAN pages and the two full
//     metadata files behind the ORAL_QB_NOTES gate. Any failure exits non-zero: the build fails
//     and the previous production deployment stays live. A partial or unverified series is
//     never shipped.
//   preview on a branch named o3-preview/*: mount the committed SYNTHETIC package only (canary
//     text, no real content, no token), for the hosted security checks HV-1..HV-6.
//   anything else (other previews, local runs): mount nothing.
//
// In every mode it removes o3/ from the output, so the build step and the pin are never
// served. It prints counts, ids and sha256 only: never package bytes or the token.
import fs from "node:fs";
import path from "node:path";
import { verifyPackage, sha256 } from "./release.mjs";
import { requiredEntitlementForPath } from "../api/_lib/routes.js";

const ROOT = process.cwd();
const O3 = path.join(ROOT, "o3");
const log = (m) => console.log(`[o3] ${m}`);

function cleanup() {
  fs.rmSync(O3, { recursive: true, force: true });
  log("removed o3/ from the output");
}

async function fetchPrivate(pin, token) {
  const { repo, ref, path: p } = pin.store || {};
  if (!/^[\w.-]+\/[\w.-]+$/.test(repo || "") || !/^[\w.\-/]+$/.test(ref || "") || !/^[\w.\-/]+$/.test(p || ""))
    throw new Error("BUILD_FAIL_STORE_COORDINATES");
  const url = `https://api.github.com/repos/${repo}/contents/${p}?ref=${encodeURIComponent(ref)}`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}`, Accept: "application/vnd.github.raw+json",
      "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "miw-o3-build" },
  });
  if (res.status === 401 || res.status === 403 || res.status === 404) throw new Error(`STORE_ACCESS_DENIED ${res.status}`);
  if (!res.ok) throw new Error(`STORE_FETCH_FAILED ${res.status}`);
  return Buffer.from(await res.arrayBuffer());
}

function mount(writes) {
  for (const w of writes) {
    const dst = path.join(ROOT, ...w.rel.split("/"));
    fs.mkdirSync(path.dirname(dst), { recursive: true });
    fs.writeFileSync(dst, w.bytes);
  }
}

async function main() {
  const env = process.env.VERCEL_ENV || "unset";
  const ref = process.env.VERCEL_GIT_COMMIT_REF || "";
  let mode = "NO_PROTECTED_CONTENT";
  if (env === "production") {
    const pin = JSON.parse(fs.readFileSync(path.join(O3, "lohan.pin.json"), "utf8"));
    const token = process.env.MIW_NOTES_STORE_TOKEN;
    if (!token) throw new Error("BUILD_FAIL_TOKEN_MISSING");
    const pkgBytes = await fetchPrivate(pin, token);
    const v = verifyPackage({ pkgBytes, pin, publicDir: ROOT, requiredEntitlementForPath });
    mount(v.writes);
    mode = "PROTECTED_RELEASE_MOUNTED";
    log(`release ${v.release_id} package ${sha256(pkgBytes).slice(0, 16)} pages ${v.totals.pages} topics ${v.totals.topics} replace ${v.totals.replace}`);
  } else if (env === "preview" && ref.startsWith("o3-preview/")) {
    const pin = JSON.parse(fs.readFileSync(path.join(O3, "synthetic", "lohan.synthetic.pin.json"), "utf8"));
    const pkgBytes = fs.readFileSync(path.join(O3, "synthetic", "lohan-synthetic.pkg"));
    const v = verifyPackage({ pkgBytes, pin, publicDir: ROOT, requiredEntitlementForPath });
    mount(v.writes);
    mode = "SYNTHETIC_PREVIEW_MOUNTED";
    log(`SYNTHETIC release ${v.release_id} pages ${v.totals.pages} replace ${v.totals.replace}`);
  }
  log(`mode ${mode} (VERCEL_ENV=${env})`);
  cleanup();
}

main().catch((e) => {
  console.error(`[o3] BUILD FAILED: ${String(e && e.message).slice(0, 200)}`);
  process.exit(1);
});
