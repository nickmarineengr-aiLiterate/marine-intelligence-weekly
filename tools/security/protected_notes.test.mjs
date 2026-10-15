// O-3 private-content delivery: controls for o3/release.mjs, o3/assemble-protected.mjs and the
// public-repository invariants (Founder FD-P1/FD-P2, 15 Oct 2026).
//
// Runs anywhere: it uses only the committed SYNTHETIC package (no real content, no token).
// Every verification rule has a mutant that must be caught, and a control that must pass.
import { test, describe } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync, spawnSync } from "node:child_process";
import { verifyPackage, buildPackage, makePin, sha256, canonical, GATE, MOUNT, ENTITLEMENT } from "../../o3/release.mjs";
import { requiredEntitlementForPath } from "../../api/_lib/routes.js";
import { ROOT, TRACKED, SERVED, PROTECTED_MOUNTS, PROTECTED_PIN } from "./deploy_set.mjs";

const SYN_DIR = path.join(ROOT, "o3", "synthetic");
const SYN_PKG = fs.readFileSync(path.join(SYN_DIR, "lohan-synthetic.pkg"));
const SYN_PIN = JSON.parse(fs.readFileSync(path.join(SYN_DIR, "lohan.synthetic.pin.json"), "utf8"));
const emptyDir = () => fs.mkdtempSync(path.join(os.tmpdir(), "o3-pub-"));
const verify = (over = {}) => verifyPackage({ pkgBytes: SYN_PKG, pin: SYN_PIN, publicDir: emptyDir(),
  requiredEntitlementForPath, ...over });
const repack = (mutate) => {
  const pkg = JSON.parse(SYN_PKG.toString("utf8"));
  mutate(pkg);
  const bytes = Buffer.from(canonical(pkg), "utf8");
  return { bytes, pin: { ...SYN_PIN, package_sha256: sha256(bytes) } };
};

describe("O-3 package verification (synthetic package)", () => {
  test("control: the committed synthetic package verifies and yields 21 gated mounts", () => {
    const v = verify();
    assert.equal(v.writes.length, 21);
    assert.ok(v.writes.every((w) => w.rel.startsWith(MOUNT) && w.kind === "mount"));
    assert.equal(v.totals.pages, 21);
  });
  test("mutant: one package byte changed -> BUILD_FAIL_PACKAGE_HASH", () => {
    const b = Buffer.from(SYN_PKG); b[b.length - 3] ^= 1;
    assert.throws(() => verify({ pkgBytes: b }), /BUILD_FAIL_PACKAGE_HASH/);
  });
  test("mutant: pin names a different page hash -> BUILD_FAIL_PIN_MISMATCH", () => {
    const pin = structuredClone(SYN_PIN); pin.deploy_files[0].sha256 = "0".repeat(64);
    assert.throws(() => verify({ pin }), /BUILD_FAIL_PIN_MISMATCH/);
  });
  test("mutant: blob edited, manifest hash kept -> BUILD_FAIL_FILE_HASH", () => {
    const { bytes, pin } = repack((p) => { const k = Object.keys(p.blobs).find((x) => x.startsWith("pages/"));
      p.blobs[k] = Buffer.from("tampered").toString("base64"); });
    assert.throws(() => verify({ pkgBytes: bytes, pin }), /BUILD_FAIL_FILE_HASH/);
  });
  test("mutant: a page without the exact gate -> BUILD_FAIL_UNGATED_PAGE", () => {
    const { bytes, pin } = repack((p) => {
      const k = "pages/lohan-notes-p1.html";
      const html = Buffer.from(p.blobs[k], "base64").toString("utf8").replace(GATE, "");
      const b = Buffer.from(html, "utf8");
      p.blobs[k] = b.toString("base64");
      const f = p.manifest.files.find((x) => x.path === k); f.sha256 = sha256(b); f.bytes = b.length;
    });
    const pin2 = { ...pin, deploy_files: pin.deploy_files.map((d) => d.path === "lohan-notes-p1.html"
      ? { ...d, sha256: JSON.parse(bytes.toString()).manifest.files.find((x) => x.path === "pages/lohan-notes-p1.html").sha256 } : d) };
    assert.throws(() => verify({ pkgBytes: bytes, pin: pin2 }), /BUILD_FAIL_UNGATED_PAGE/);
  });
  test("mutant: declared totals drift from content -> BUILD_FAIL_TOTALS", () => {
    const pin = structuredClone(SYN_PIN); pin.totals.topics += 1;
    assert.throws(() => verify({ pin }), /BUILD_FAIL_TOTALS/);
  });
  test("mutant: mount path not gated by the production route table -> BUILD_FAIL_UNGATED_MOUNT", () => {
    assert.throws(() => verify({ requiredEntitlementForPath: () => null }), /BUILD_FAIL_UNGATED_MOUNT/);
  });
  test("mutant: a public file already occupies a mount path -> BUILD_FAIL_PUBLIC_COLLISION", () => {
    const d = emptyDir(); fs.mkdirSync(path.join(d, ...MOUNT.split("/")), { recursive: true });
    fs.writeFileSync(path.join(d, ...MOUNT.split("/"), "lohan-notes-p1.html"), "public");
    assert.throws(() => verify({ publicDir: d }), /BUILD_FAIL_PUBLIC_COLLISION/);
  });
  test("mutant: wrong entitlement in the pin -> BUILD_FAIL_ENTITLEMENT", () => {
    assert.throws(() => verify({ pin: { ...SYN_PIN, entitlement: "SOLVED_QP" } }), /BUILD_FAIL_ENTITLEMENT/);
  });
});

describe("O-3 metadata replacement (pin public_sha256 binding)", () => {
  const mk = () => {
    const priv = emptyDir(), pub = emptyDir();
    const ov = path.join(priv, "lohan", "overlay", ...MOUNT.split("/"));
    const sp = path.join(priv, "lohan", "source", "tools", "notes", "specs", "lohan");
    fs.mkdirSync(ov, { recursive: true }); fs.mkdirSync(sp, { recursive: true });
    fs.mkdirSync(path.join(pub, ...MOUNT.split("/")), { recursive: true });
    fs.writeFileSync(path.join(ov, "lohan-notes-p1.html"), `<body>\n${GATE}\n<div class="topic-block" id="topic-p1-1">x</div></body>`);
    fs.writeFileSync(path.join(ov, "index.html"), "FULL INDEX");
    fs.writeFileSync(path.join(pub, ...MOUNT.split("/"), "index.html"), "PUBLIC INDEX");
    fs.writeFileSync(path.join(sp, "p1.json"), "{}");
    const r = buildPackage({ privateRoot: priv, publicTree: pub, releaseId: "lohan-r9" });
    const pin = makePin({ manifest: r.manifest, packageSha: r.sha256, replaceFiles: r.replaceFiles, store: {} });
    return { r, pin, pub };
  };
  test("control: the replacement applies over the exact public base", () => {
    const { r, pin, pub } = mk();
    const v = verifyPackage({ pkgBytes: r.bytes, pin, publicDir: pub, requiredEntitlementForPath });
    assert.deepEqual(v.writes.map((w) => w.kind).sort(), ["mount", "replace"]);
  });
  test("mutant: the public base changed after pinning -> BUILD_FAIL_PUBLIC_BASE", () => {
    const { r, pin, pub } = mk();
    fs.writeFileSync(path.join(pub, ...MOUNT.split("/"), "index.html"), "PUBLIC INDEX, edited");
    assert.throws(() => verifyPackage({ pkgBytes: r.bytes, pin, publicDir: pub, requiredEntitlementForPath }), /BUILD_FAIL_PUBLIC_BASE/);
  });
  test("mutant: a replacement outside the replaceable set -> BUILD_FAIL_UNSAFE_PATH", () => {
    const { r, pin, pub } = mk();
    const p2 = structuredClone(pin); p2.replace_files[0].path = "SQ/pay.html";
    assert.throws(() => verifyPackage({ pkgBytes: r.bytes, pin: p2, publicDir: pub, requiredEntitlementForPath }), /BUILD_FAIL_(PIN_MISMATCH|UNSAFE_PATH)/);
  });
});

describe("O-3 build step mode selection (assemble-protected.mjs in a scratch copy)", () => {
  const scratch = () => {
    const d = emptyDir();
    fs.cpSync(path.join(ROOT, "o3"), path.join(d, "o3"), { recursive: true });
    fs.mkdirSync(path.join(d, "api", "_lib"), { recursive: true });
    for (const f of fs.readdirSync(path.join(ROOT, "api", "_lib"))) fs.copyFileSync(path.join(ROOT, "api", "_lib", f), path.join(d, "api", "_lib", f));
    fs.copyFileSync(path.join(ROOT, "package.json"), path.join(d, "package.json"));
    return d;
  };
  const run = (d, env) => spawnSync(process.execPath, ["o3/assemble-protected.mjs"],
    { cwd: d, env: { PATH: process.env.PATH, SystemRoot: process.env.SystemRoot, ...env }, encoding: "utf8" });
  const mounted = (d) => fs.existsSync(path.join(d, ...MOUNT.split("/"))) ? fs.readdirSync(path.join(d, ...MOUNT.split("/"))) : [];
  test("no Vercel env: mounts nothing, removes o3/", () => {
    const d = scratch(); const r = run(d, {});
    assert.equal(r.status, 0, r.stderr); assert.deepEqual(mounted(d), []); assert.ok(!fs.existsSync(path.join(d, "o3")));
  });
  test("ordinary preview branch: mounts nothing (never the real release)", () => {
    const d = scratch(); const r = run(d, { VERCEL_ENV: "preview", VERCEL_GIT_COMMIT_REF: "feature/x", MIW_NOTES_STORE_TOKEN: "x" });
    assert.equal(r.status, 0, r.stderr); assert.deepEqual(mounted(d), []);
  });
  test("o3-preview/* branch: mounts the 21 SYNTHETIC pages, gated, then removes o3/", () => {
    const d = scratch(); const r = run(d, { VERCEL_ENV: "preview", VERCEL_GIT_COMMIT_REF: "o3-preview/hv" });
    assert.equal(r.status, 0, r.stderr);
    const m = mounted(d); assert.equal(m.length, 21);
    const html = fs.readFileSync(path.join(d, ...MOUNT.split("/"), m[0]), "utf8");
    assert.ok(html.includes("SYNTH-CANARY-O3-PAGE-") && html.includes(GATE));
    assert.ok(!fs.existsSync(path.join(d, "o3")));
  });
  test("production without the token: the build FAILS (previous deployment stays live)", () => {
    const d = scratch(); const r = run(d, { VERCEL_ENV: "production" });
    assert.notEqual(r.status, 0); assert.match(r.stderr, /BUILD_FAIL_TOKEN_MISSING/); assert.deepEqual(mounted(d), []);
  });
  test("the build log never prints package bytes or the token", () => {
    const d = scratch(); const r = run(d, { VERCEL_ENV: "preview", VERCEL_GIT_COMMIT_REF: "o3-preview/hv", MIW_NOTES_STORE_TOKEN: "SECRET-TOKEN-XYZ" });
    assert.ok(!(r.stdout + r.stderr).includes("SECRET-TOKEN-XYZ") && !(r.stdout + r.stderr).includes("SYNTH-CANARY"));
  });
});

describe("O-3 public-repository invariants", () => {
  test("no LOHAN page or private spec is tracked in the public repository", () => {
    const bad = TRACKED.filter((f) => /^meoclass1\/oralnotes\/lohan-notes-p\d+\.html$/.test(f) || f.startsWith("tools/notes/specs/lohan/"));
    assert.deepEqual(bad, []);
  });
  test("the pin carries hashes, paths and counts only (no content field)", () => {
    assert.ok(PROTECTED_PIN, "o3/lohan.pin.json present");
    const allowed = new Set(["format", "series", "release_id", "package_sha256", "entitlement", "mount", "totals", "store", "deploy_files", "replace_files"]);
    assert.deepEqual(Object.keys(PROTECTED_PIN).filter((k) => !allowed.has(k)), []);
    for (const f of PROTECTED_PIN.deploy_files) assert.deepEqual(Object.keys(f).sort(), ["path", "sha256"]);
    assert.ok(Buffer.byteLength(JSON.stringify(PROTECTED_PIN)) < 16384);
  });
  test("every pin mount and replacement is served behind ORAL_QB_NOTES", () => {
    for (const p of PROTECTED_MOUNTS) assert.equal(requiredEntitlementForPath("/" + p), ENTITLEMENT, p);
    for (const r of PROTECTED_PIN.replace_files) assert.equal(requiredEntitlementForPath("/" + r.path), ENTITLEMENT, r.path);
    assert.equal(PROTECTED_MOUNTS.length, 21);
    assert.ok(PROTECTED_MOUNTS.every((p) => SERVED.includes(p)));
  });
  test("o3/ is build-only: never in the served set", () => {
    assert.deepEqual(SERVED.filter((f) => f.startsWith("o3/")), []);
  });
  test("vercel.json runs the O-3 build step", () => {
    const vj = JSON.parse(fs.readFileSync(path.join(ROOT, "vercel.json"), "utf8"));
    assert.equal(vj.buildCommand, "node o3/assemble-protected.mjs");
  });
});
