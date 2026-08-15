// =============================================================
// Marine Intelligence Weekly — Deployment surface test
// Run: node --test tools/security/     (alongside security.test.mjs)
//
// The repository root is the static web root and the build is a
// no-op, so every file Vercel receives becomes a URL. .vercelignore
// is the only thing standing between "tracked" and "served". This
// suite proves, offline and deterministically, that:
//
//   1. representative AUTHORING-ONLY paths are excluded from the
//      deployment intent (specs, verification, governance docs, the
//      internal manifest, known_traps, tools/);
//   2. every class that .gitignore protects stays excluded on a CLI
//      deployment too. The Vercel CLI (verified in v58.11.0,
//      getVercelIgnore) reads .vercelignore + a fixed default list and
//      NEVER reads .gitignore -- so this file must carry .gitignore's
//      protections itself, and a synthetic sentinel in each protected
//      class is asserted excluded (NEGATIVE CONTROL);
//   3. every .gitignore pattern appears verbatim in .vercelignore
//      (fail-closed mirror: a new .gitignore entry breaks this test
//      until it is carried across);
//   4. every candidate runtime surface remains deployable: /solvedQP/,
//      /SQ/, /meoclass1/ product pages and indexes, api/, middleware,
//      vercel.json, assets and the marketing site.
//
// Matching semantics. Vercel evaluates .vercelignore with the
// `ignore` package (gitignore rules). No third-party dependency is
// added for a test, so the matcher in deploy_set.mjs implements the
// gitignore subset this repository's .vercelignore uses -- and REFUSES
// any syntax outside that subset (negation, `**`, character classes,
// escapes). If someone writes a pattern the matcher cannot evaluate
// faithfully, the suite fails rather than guessing. deploy_set.mjs is
// shared with link_integrity.test.mjs so both suites agree on KEEP.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import {
  ROOT, VERCEL_DEFAULT_IGNORES, parsePatterns, isIgnored,
  vercelignoreText, gitignoreText, PATTERNS, TRACKED,
} from "./deploy_set.mjs";

// -------------------------------------------------------------
// 0. The matcher itself: positive and negative controls, so a broken
//    matcher cannot make the rest of the suite pass vacuously.
// -------------------------------------------------------------
describe("matcher — gitignore subset behaves like gitignore", () => {
  const P = parsePatterns([
    "tools/", "*.pyc", "/*.md", "docs/*.pdf", "tools/notes/_*.txt", "Knowledge Central/",
  ].join("\n"), "fixture");

  test("directory pattern ignores everything beneath it, not a same-named file elsewhere", () => {
    assert.ok(isIgnored("tools/pastpapers/build_index.py", P));
    assert.ok(isIgnored("tools/x", P));
    assert.equal(isIgnored("SQ/tools", P), null, "file named tools is not the directory");
  });
  test("extension glob matches at any depth", () => {
    assert.ok(isIgnored("a/b/c.pyc", P));
    assert.equal(isIgnored("a/b/c.py", P), null);
  });
  test("root-anchored glob matches only the root", () => {
    assert.ok(isIgnored("README.md", P));
    assert.equal(isIgnored("RulesApp/README.md", P), null);
    assert.equal(isIgnored("meoclass1/known_traps.md", P), null);
  });
  test("slash patterns are anchored and * does not cross a slash", () => {
    assert.ok(isIgnored("docs/a.pdf", P));
    assert.equal(isIgnored("docs/sub/a.pdf", P), null);
    assert.equal(isIgnored("other/docs/a.pdf", P), null);
    const P2 = parsePatterns("tools/notes/_*.txt", "fixture");
    assert.ok(isIgnored("tools/notes/_scratch.txt", P2));
    assert.equal(isIgnored("tools/notes/scratch.txt", P2), null);
    assert.equal(isIgnored("tools/notes/deep/_scratch.txt", P2), null);
  });
  test("a directory name with a space is honoured", () => {
    assert.ok(isIgnored("Knowledge Central/FSS/ch15.json", P));
  });
  test("POSITIVE CONTROL: unsupported syntax is refused, not guessed", () => {
    assert.throws(() => parsePatterns("!keep.html", "fx"));
    assert.throws(() => parsePatterns("a/**/b", "fx"));
    assert.throws(() => parsePatterns("[abc].html", "fx"));
  });
});

// -------------------------------------------------------------
// 1. Authoring-only paths are excluded from the deployment intent
// -------------------------------------------------------------
describe("deployment intent — authoring-only classes are excluded", () => {
  const MUST_EXCLUDE = [
    "meoclass1/pastpapers/specs/QP2301.json",
    "meoclass1/pastpapers/verification/QP2301_VERIFICATION.md",
    "meoclass1/pastpapers/docs/CURRENT_STATUS.md",
    "meoclass1/pastpapers/docs/LAPTOP_REVIEW_AND_INTEGRATION_PROTOCOL.md",
    "meoclass1/pastpapers/intelligence/historical_qp_intelligence.json",
    "meoclass1/pastpapers/sample/QP2601.sample.json",
    "meoclass1/pastpapers/known_traps.md",
    "meoclass1/pastpapers/pastpapers_content_index.json",
    // The review HTML tree itself, retired from the deploy. Real files, so
    // these fail loudly if the directory rule is ever narrowed back.
    "meoclass1/pastpapers/QP2301.html",
    "meoclass1/pastpapers/index.html",
    "meoclass1/pastpapers/topics-2026.html",
    // Synthetic: a review page that does not exist yet. A future paper build
    // must land outside the deploy by the DIRECTORY rule, without anyone
    // remembering to add its filename here.
    "meoclass1/pastpapers/SENTINEL.html",
    "meoclass1/known_traps.md",
    "meoclass1/qb_health_check.py",
    "tools/pastpapers/build_index.py",
    "tools/security/security.test.mjs",
    "docs/ARCHITECTURE.md",
    "reports/audit/2026-07-30_repo_audit.md",
    "engineering-reports/merchant-shipping-act-2025-qb-rebasing/REPORT.md",
    "production-system/verification/merchant-shipping-act-2025-crosswalk.md",
    "corrections/README.md",
    ".github/workflows/solvedqp-health-check.yml",
    ".claude/launch.json",
    "Claude skill/IMPLEMENTATION_CONTRACT.md",
    "README.md",
    "AI_SESSION_START.md",
    "REPOSITORY_STATUS.md",
  ];
  for (const p of MUST_EXCLUDE) {
    test(`excluded: ${p}`, () => {
      assert.ok(isIgnored(p, PATTERNS), `${p} would be deployed`);
    });
  }

  test("every TRACKED file under the internal pastpapers classes and tools/ is excluded", () => {
    const classes = [
      "meoclass1/pastpapers/specs/", "meoclass1/pastpapers/verification/",
      "meoclass1/pastpapers/docs/", "meoclass1/pastpapers/intelligence/",
      "meoclass1/pastpapers/", "tools/", "docs/", "reports/",
    ];
    const leaks = TRACKED.filter((f) => classes.some((c) => f.startsWith(c)))
      .filter((f) => !isIgnored(f, PATTERNS));
    assert.deepEqual(leaks, [], "tracked internal files that would still deploy");
  });
});

// -------------------------------------------------------------
// 2. NEGATIVE CONTROL: .gitignore-protected classes stay excluded on
//    a CLI deployment (synthetic sentinels; nothing real is touched)
// -------------------------------------------------------------
describe("CLI negative control — git-ignored classes remain undeployable", () => {
  const SENTINELS = [
    ".env",
    ".env.production",
    ".env.local",
    ".vercel/project.json",
    ".vercel/.env.preview.local",
    "Knowledge Central/FSS-Code/ch15-inert-gas.json",
    "meoclass1/pastpapers/docs/JANUARY 2023.pdf",
    "meoclass1/pastpapers/docs/notes from candidate/page-01.jpg",
    "meoclass1/pastpapers/verification/LOCAL_SOURCE_PROVENANCE.md",
    "meoclass1/pastpapers/intelligence/derived/sixyear.json",
    "Notes-for-written-answers/handout-01.pdf",
    "docs/MIW-master-Question-bank/master.xlsx",
    "tools/notes/_scratch_probe.txt",
    "node_modules/some-dep/index.js",
    "tools/pastpapers/__pycache__/build_index.cpython-311.pyc",
    "package-lock.json",
  ];
  for (const s of SENTINELS) {
    test(`sentinel stays excluded: ${s}`, () => {
      assert.ok(isIgnored(s, PATTERNS), `${s} would be uploaded by a CLI deploy`);
    });
  }

  test("each sentinel is genuinely git-ignored today (the control is real)", () => {
    // Skip node_modules / pycache / lockfile which are covered by Vercel
    // defaults regardless; the interesting ones are the repository's own.
    const own = SENTINELS.filter((s) => !/node_modules|__pycache__|package-lock/.test(s));
    for (const s of own) {
      let ignored = true;
      try {
        execFileSync("git", ["-c", "safe.directory=*", "check-ignore", "-q", "--no-index", s],
          { cwd: ROOT, stdio: "ignore" });
      } catch (e) {
        ignored = e.status === 0;
      }
      assert.ok(ignored, `${s} is not git-ignored -- the sentinel list has drifted from .gitignore`);
    }
  });

  test("every .gitignore pattern is carried verbatim into .vercelignore", () => {
    const gitPats = gitignoreText.split(/\r?\n/).map((l) => l.replace(/\s+$/, ""))
      .filter((l) => l && !l.startsWith("#"));
    const vPats = new Set(vercelignoreText.split(/\r?\n/).map((l) => l.replace(/\s+$/, "")));
    const missing = gitPats.filter((p) => !vPats.has(p));
    assert.deepEqual(missing, [], ".gitignore patterns absent from .vercelignore");
  });

  test("POSITIVE CONTROL: a matcher without section A would let a sentinel through", () => {
    // Rebuild the pattern set from the defaults plus ONLY the non-mirror
    // sections, and show the control has teeth.
    const withoutMirror = parsePatterns([
      "meoclass1/pastpapers/specs/", "tools/", "docs/",
    ].join("\n"), "fx");
    const P = [...parsePatterns(VERCEL_DEFAULT_IGNORES.join("\n"), "d"), ...withoutMirror];
    assert.equal(isIgnored("Knowledge Central/FSS-Code/ch15.json", P), null);
    assert.equal(isIgnored(".env", P), null);
    assert.equal(isIgnored("Notes-for-written-answers/handout-01.pdf", P), null);
    assert.equal(isIgnored("meoclass1/pastpapers/verification/LOCAL_SOURCE_PROVENANCE.md", P), null);
  });
});

// -------------------------------------------------------------
// 3. Candidate runtime remains deployable
// -------------------------------------------------------------
describe("runtime allowlist — product and public surfaces still deploy", () => {
  const MUST_DEPLOY = [
    "middleware.js", "vercel.json", "package.json", "robots.txt", "CNAME",
    "index.html", "terms.html", "privacy.html", "logo.webp",
    "api/session.js", "api/trial.js", "api/verify-payment.js", "api/_lib/routes.js",
    "SQ/index.html", "SQ/pay.html", "SQ/QB1_A.html",
    "solvedQP/index.html", "solvedQP/QP2301.html", "solvedQP/questions-2023.html",
    "solvedQP/solvedqp_content_index.json",
    "meoclass1/index.html", "meoclass1/QB2_E.html", "meoclass1/examiner-index.html",
    "meoclass1/qb_content_index.json",
    "meoclass1/oralnotes/notes_content_index.json",
    "meoclass1/oralnotes/written-sample-january-2026.html",
    "assets/logo.webp", "RulesApp/app/index.html", "archive/index.html",
    "GHGDecarb/timeline.html", "ecosystem.html", "timeline.html",
  ];
  for (const p of MUST_DEPLOY) {
    test(`deployable: ${p}`, () => {
      assert.ok(TRACKED.includes(p), `${p} is not tracked -- fixture is stale`);
      assert.equal(isIgnored(p, PATTERNS), null, `${p} would be excluded from deploy`);
    });
  }

  test("no tracked file under the served product roots is excluded, except the named internals", () => {
    const roots = ["solvedQP/", "SQ/", "api/", "assets/", "meoclass1/", "RulesApp/",
      "articles/", "archive/", "GHGDecarb/"];
    const internals = [
      // The whole review tree, not its sub-classes: the 48 generated review
      // pages were retired from the deploy alongside the authoring layer.
      "meoclass1/pastpapers/",
      "meoclass1/known_traps.md", "meoclass1/qb_health_check.py",
    ];
    const wrongly = TRACKED.filter((f) => roots.some((r) => f.startsWith(r)))
      .filter((f) => !internals.some((i) => f.startsWith(i)))
      .filter((f) => isIgnored(f, PATTERNS));
    assert.deepEqual(wrongly, [], "served files that .vercelignore would drop");
  });

  test("root HTML issues and web assets remain deployable", () => {
    const wrongly = TRACKED.filter((f) => !f.includes("/") &&
      /\.(html|webp|txt|json|js)$/.test(f) && f !== "package-lock.json")
      .filter((f) => isIgnored(f, PATTERNS));
    assert.deepEqual(wrongly, []);
  });
});

// -------------------------------------------------------------
// 4. Report the reduction, so the number in the session record is
//    computed rather than estimated.
// -------------------------------------------------------------
describe("deployment set — size report", () => {
  test("tracked vs deployed", () => {
    let nAll = 0, bAll = 0, nDep = 0, bDep = 0;
    for (const f of TRACKED) {
      let size = 0;
      try { size = fs.statSync(path.join(ROOT, f)).size; } catch { continue; }
      nAll++; bAll += size;
      if (!isIgnored(f, PATTERNS)) { nDep++; bDep += size; }
    }
    const mb = (b) => (b / 1048576).toFixed(2);
    console.log(`    tracked ${nAll} files / ${mb(bAll)} MB  ->  deployed ${nDep} files / ${mb(bDep)} MB` +
      `  (excluded ${nAll - nDep} files / ${mb(bAll - bDep)} MB)`);
    assert.ok(nDep > 0 && nDep < nAll);
  });
});
