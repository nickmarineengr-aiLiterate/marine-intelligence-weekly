// =============================================================
// Marine Intelligence Weekly — the deployed file set, computed offline
//
// The repository root is the static web root and the build is a no-op,
// so "what Vercel serves" is exactly "tracked files minus .vercelignore
// minus the CLI's fixed default exclusions". Two suites need that set:
// deploy_surface.test.mjs (is the right material excluded / retained?)
// and link_integrity.test.mjs (does every runtime reference on a served
// page resolve to a served file?). Both import from here so there is one
// matcher and one notion of KEEP.
//
// Matching semantics. Vercel evaluates .vercelignore with the `ignore`
// package (gitignore rules). No third-party dependency is added for a
// test, so the matcher below implements the gitignore subset this
// repository's .vercelignore uses -- and REFUSES any syntax outside that
// subset (negation, `**`, character classes, escapes). If someone writes
// a pattern the matcher cannot evaluate faithfully, callers fail rather
// than guess.
// =============================================================

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(HERE, "..", "..");

// Vercel's always-on default exclusions. Copied from the CLI source
// (@vercel/client getVercelIgnore, CLI 58.11.0). Applied BEFORE
// .vercelignore in both deploy paths.
export const VERCEL_DEFAULT_IGNORES = [
  ".hg", ".git", ".gitmodules", ".svn", ".cache", ".next", ".now",
  ".vercel", ".npmignore", ".dockerignore", ".gitignore", ".*.swp",
  ".DS_Store", ".wafpicke-*", ".lock-wscript", ".env.local",
  ".env.*.local", ".venv", ".yarn/cache", ".pnp*", "npm-debug.log",
  "config.gypi", "node_modules", "__pycache__", "venv", "CVS",
];

const UNSUPPORTED = /(^!|\*\*|\[|\\)/;

export function parsePatterns(text, source) {
  const out = [];
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.replace(/\s+$/, "");
    if (!line || line.startsWith("#")) continue;
    if (UNSUPPORTED.test(line)) {
      throw new Error(`${source}: pattern "${line}" uses syntax this matcher ` +
        `does not implement (negation, **, [], or escapes). Extend the ` +
        `matcher deliberately or rewrite the pattern.`);
    }
    let pat = line;
    const dirOnly = pat.endsWith("/");
    if (dirOnly) pat = pat.slice(0, -1);
    let anchored = false;
    if (pat.startsWith("/")) { anchored = true; pat = pat.slice(1); }
    if (pat.includes("/")) anchored = true;
    const re = new RegExp("^" + pat.split("").map((c) => {
      if (c === "*") return "[^/]*";
      if (c === "?") return "[^/]";
      return c.replace(/[.+^${}()|]/g, "\\$&");
    }).join("") + "$");
    out.push({ line, dirOnly, anchored, re });
  }
  return out;
}

/** Is `relPath` (posix, file) ignored under `patterns`? Returns the matching line or null. */
export function isIgnored(relPath, patterns) {
  const parts = relPath.split("/");
  const ancestors = [];
  for (let i = 1; i < parts.length; i++) ancestors.push(parts.slice(0, i).join("/"));
  const full = relPath;
  for (const p of patterns) {
    const targets = p.dirOnly ? ancestors : [...ancestors, full];
    for (const t of targets) {
      const subject = p.anchored ? t : t.split("/").pop();
      if (p.re.test(subject)) return p.line;
    }
  }
  return null;
}

export const vercelignoreText = fs.readFileSync(path.join(ROOT, ".vercelignore"), "utf8");
export const gitignoreText = fs.readFileSync(path.join(ROOT, ".gitignore"), "utf8");
export const PATTERNS = [
  ...parsePatterns(VERCEL_DEFAULT_IGNORES.join("\n"), "vercel-defaults"),
  ...parsePatterns(vercelignoreText, ".vercelignore"),
];

export function tracked() {
  const out = execFileSync("git", ["-c", "safe.directory=*", "ls-files", "-z"],
    { cwd: ROOT, encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });
  return out.split("\0").filter(Boolean);
}
export const TRACKED = tracked();

/** The served set: tracked files that survive every exclusion. */
export const KEEP = TRACKED.filter((f) => !isIgnored(f, PATTERNS));
