// =============================================================
// Marine Intelligence Weekly — Candidate-Lifecycle closure, end to end
// Run: node --test tools/security/*.test.mjs
//
// member_lifecycle.test.mjs proves the DECISIONS as pure functions.
// This file proves the COMMAND: it stands up a throwaway HTTP server
// that speaks the handful of Upstash REST verbs the admin tool uses,
// points the real script at it, and runs the real commands.
//
// WHY BOTHER, GIVEN THE PURE TESTS
// A planner that returns the right answer and a tool that writes the
// wrong field are both consistent with a green unit suite. The gap
// between them is argument parsing, the confirmation gate, and which
// key the HSET actually names — none of which a pure test can see, and
// all of which are where an operator command goes wrong.
//
// NO LIVE DATA. The store is a Map that dies with the process. There
// are no credentials here, and KV_REST_API_URL is overridden per test,
// so this cannot reach production even by accident.
// =============================================================

import { test, describe, before, after } from "node:test";
import assert from "node:assert/strict";
import { createServer } from "node:http";
import { execFile } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

import { PERPETUAL, grantAllowsAccess } from "../../api/_lib/grants.js";

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), "entitlement_admin.mjs");

// -------------------------------------------------------------
// A minimal Upstash REST double. Hashes and plain keys only — exactly
// the surface entitlement_admin.mjs touches, and nothing more, so an
// unsupported command shows up as a failure rather than a silent no-op.
// -------------------------------------------------------------
const store = new Map();     // key -> Map(field -> value) for hashes
const plain = new Map();     // key -> string, for EXISTS/DEL targets

function execute(args) {
  const [verb, key, ...rest] = args.map(String);
  switch (verb.toUpperCase()) {
    case "HGETALL": {
      const h = store.get(key);
      if (!h) return [];
      return [...h.entries()].flat();
    }
    case "HMGET": {
      const h = store.get(key);
      return rest.map((f) => (h && h.has(f) ? h.get(f) : null));
    }
    case "HSET": {
      const h = store.get(key) || new Map();
      for (let i = 0; i + 1 < rest.length; i += 2) h.set(rest[i], rest[i + 1]);
      store.set(key, h);
      return rest.length / 2;
    }
    case "HDEL": {
      const h = store.get(key);
      let n = 0;
      for (const f of rest) if (h && h.delete(f)) n++;
      return n;
    }
    case "EXISTS":
      return plain.has(key) || store.has(key) ? 1 : 0;
    case "DEL": {
      const had = plain.delete(key) || store.delete(key);
      return had ? 1 : 0;
    }
    case "ZCARD":
      return 0;
    case "SCAN": {
      // Cursor "0" returns everything in one page; MATCH is honoured for
      // the one prefix pattern the tool uses.
      const at = rest.indexOf("MATCH");
      const pattern = at === -1 ? "*" : String(rest[at + 1]);
      const prefix = pattern.endsWith("*") ? pattern.slice(0, -1) : pattern;
      const keys = [...store.keys()].filter((k) => k.startsWith(prefix));
      return ["0", keys];
    }
    default:
      throw new Error(`fake store: unsupported command ${verb}`);
  }
}

let server;
let BASE;

before(async () => {
  server = createServer((req, res) => {
    let body = "";
    req.on("data", (c) => (body += c));
    req.on("end", () => {
      let result;
      try {
        result = execute(JSON.parse(body || "[]"));
      } catch (e) {
        res.writeHead(400, { "Content-Type": "application/json" });
        return res.end(JSON.stringify({ error: e.message }));
      }
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ result }));
    });
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  BASE = `http://127.0.0.1:${server.address().port}`;
});

after(() => server && server.close());

const EMAIL = "candidate@example.com";
const ENT = `miw:ent:${EMAIL}`;

/**
 * Run the real CLI against the fake store.
 *
 * ASYNC, and that is not a style choice. The fake store runs in THIS
 * process, so a synchronous spawn would block the event loop that has
 * to answer the child's HTTP request — the two would deadlock and the
 * suite would simply hang. Awaiting keeps the server able to reply.
 */
function cli(...args) {
  return new Promise((resolve) => {
    execFile(
      process.execPath,
      [SCRIPT, ...args],
      { encoding: "utf8", env: { ...process.env, KV_REST_API_URL: BASE, KV_REST_API_TOKEN: "test-token" } },
      (err, stdout, stderr) => resolve({
        code: err ? (err.code ?? 1) : 0,
        out: stdout || "",
        err: stderr || "",
      })
    );
  });
}

/** Seed one account. */
function seed(fields, { credential = true } = {}) {
  store.clear();
  plain.clear();
  store.set(ENT, new Map(Object.entries(fields)));
  if (credential) plain.set(`miw:user:${EMAIL}`, "sha256$salt$digest");
}

const held = (field) => store.get(ENT)?.get(field);

// -------------------------------------------------------------
describe("mark-passed, run for real", () => {
  test("without --confirm it changes NOTHING and says what it would do", async () => {
    seed({ ORAL_QB_NOTES: PERPETUAL });
    const r = await cli("mark-passed", EMAIL);

    // Exactly 2, and this is a REGRESSION GUARD, not a formality. The
    // refusal originally used process.exit(2) while the reads above were
    // still tearing down their connection pool, which trips a libuv
    // assertion on Windows: the operator got a crash and exit status
    // 0xC0000409. A wrapper script would read that as "unknown failure"
    // rather than "not confirmed".
    assert.equal(r.code, 2);
    assert.match(r.out, /CLOSE/);
    assert.match(r.err, /Nothing was changed/);
    assert.equal(held("ORAL_QB_NOTES"), PERPETUAL, "the grant was written without confirmation");
  });

  test("the plan is printed BEFORE the refusal, so the operator sees the account", async () => {
    seed({ ORAL_QB_NOTES: PERPETUAL });
    const r = await cli("mark-passed", EMAIL);
    assert.match(r.out, /Candidate-Lifecycle \/ ACTIVE/);
    assert.match(r.out, /mark-passed would:/);
  });

  test("with --confirm the lifecycle grant is closed and access is denied", async () => {
    seed({ ORAL_QB_NOTES: PERPETUAL });
    const r = await cli("mark-passed", EMAIL, "--confirm");

    assert.equal(r.code, 0);
    const after = held("ORAL_QB_NOTES");
    assert.match(after, /^passed:\d+:1$/);
    assert.equal(grantAllowsAccess(after, Math.floor(Date.now() / 1000)), false);
    assert.match(r.out, /PASSED_CLOSED/);
  });

  test("PRODUCT SEPARATION, END TO END: a paid Written year is untouched", async () => {
    // The account the Founder is worried about: legacy Oral + a
    // separately-bought one-year Written term, closed with no product
    // named. If this ever regresses, a customer silently loses a product
    // they paid for and nobody finds out for months.
    const writtenExpiry = String(Math.floor(Date.now() / 1000) + 200 * 86400);
    seed({ ORAL_QB_NOTES: PERPETUAL, SOLVED_QP: writtenExpiry });

    const r = await cli("mark-passed", EMAIL, "--confirm");
    assert.equal(r.code, 0);

    assert.match(held("ORAL_QB_NOTES"), /^passed:/);
    assert.equal(held("SOLVED_QP"), writtenExpiry, "the Written grant was rewritten");
    assert.equal(grantAllowsAccess(held("SOLVED_QP"), Math.floor(Date.now() / 1000)), true);

    // And the operator was TOLD it was left alone, rather than having to
    // infer it from silence.
    assert.match(r.out, /SOLVED_QP\s+no change — dated one-year access — UNTOUCHED/);
  });

  test("closing signs every device out", async () => {
    seed({ ORAL_QB_NOTES: PERPETUAL });
    plain.set(`miw:sessions:${EMAIL}`, "x");
    await cli("mark-passed", EMAIL, "--confirm");
    assert.equal(plain.has(`miw:sessions:${EMAIL}`), false);
  });

  test("the credential SURVIVES a closure by default", async () => {
    // Account identity and product entitlement are separate things.
    seed({ ORAL_QB_NOTES: PERPETUAL });
    await cli("mark-passed", EMAIL, "--confirm");
    assert.equal(plain.has(`miw:user:${EMAIL}`), true);
  });

  test("--remove-credential is REFUSED while another product is still valid", async () => {
    const writtenExpiry = String(Math.floor(Date.now() / 1000) + 200 * 86400);
    seed({ ORAL_QB_NOTES: PERPETUAL, SOLVED_QP: writtenExpiry });

    const r = await cli("mark-passed", EMAIL, "--confirm", "--remove-credential");
    assert.match(r.err, /credential NOT removed/);
    assert.equal(plain.has(`miw:user:${EMAIL}`), true, "a paying customer was locked out");
    // The closure itself still stands — the refusal is scoped to the
    // credential, not a rollback of the whole command.
    assert.match(held("ORAL_QB_NOTES"), /^passed:/);
  });

  test("--remove-credential proceeds when nothing valid remains", async () => {
    seed({ ORAL_QB_NOTES: PERPETUAL });
    const r = await cli("mark-passed", EMAIL, "--confirm", "--remove-credential");
    assert.match(r.out, /credential removed/);
    assert.equal(plain.has(`miw:user:${EMAIL}`), false);
  });

  test("an account nobody holds is refused outright", async () => {
    store.clear();
    plain.clear();
    const r = await cli("mark-passed", "typo@example.com", "--confirm");
    assert.equal(r.code, 2);
    assert.match(r.err, /no account and no entitlement exist/);
    assert.equal(store.size, 0, "a closure was written onto an unknown address");
  });

  test("a dated-only customer has nothing to close and nothing is written", async () => {
    const expiry = String(Math.floor(Date.now() / 1000) + 100 * 86400);
    seed({ SOLVED_QP: expiry });
    const r = await cli("mark-passed", EMAIL, "--confirm");
    assert.equal(r.code, 0);
    assert.match(r.out, /nothing to do/);
    assert.equal(held("SOLVED_QP"), expiry);
  });

  test("running it twice is idempotent and does not rewrite the audit stamp", async () => {
    seed({ ORAL_QB_NOTES: PERPETUAL });
    await cli("mark-passed", EMAIL, "--confirm");
    const first = held("ORAL_QB_NOTES");
    const r = await cli("mark-passed", EMAIL, "--confirm");
    assert.match(r.out, /already closed/);
    assert.equal(held("ORAL_QB_NOTES"), first);
  });

  test("naming one product leaves the other lifecycle grant open", async () => {
    seed({ ORAL_QB_NOTES: PERPETUAL, SOLVED_QP: PERPETUAL });
    await cli("mark-passed", EMAIL, "SOLVED_QP", "--confirm");
    assert.equal(held("ORAL_QB_NOTES"), PERPETUAL);
    assert.match(held("SOLVED_QP"), /^passed:/);
  });
});

// -------------------------------------------------------------
describe("reopen-candidate, run for real", () => {
  test("without --confirm nothing is restored", async () => {
    seed({ ORAL_QB_NOTES: PERPETUAL });
    await cli("mark-passed", EMAIL, "--confirm");
    const closed = held("ORAL_QB_NOTES");

    const r = await cli("reopen-candidate", EMAIL);
    assert.equal(r.code, 2);
    assert.equal(held("ORAL_QB_NOTES"), closed);
  });

  test("a closure made in error is fully undone", async () => {
    seed({ ORAL_QB_NOTES: PERPETUAL });
    await cli("mark-passed", EMAIL, "--confirm");
    const r = await cli("reopen-candidate", EMAIL, "--confirm");

    assert.equal(r.code, 0);
    assert.equal(held("ORAL_QB_NOTES"), PERPETUAL);
    assert.equal(grantAllowsAccess(held("ORAL_QB_NOTES"), Math.floor(Date.now() / 1000)), true);
    assert.match(r.out, /Candidate-Lifecycle \/ ACTIVE/);
  });

  test("reopen does not disturb a dated grant beside it", async () => {
    const writtenExpiry = String(Math.floor(Date.now() / 1000) + 200 * 86400);
    seed({ ORAL_QB_NOTES: PERPETUAL, SOLVED_QP: writtenExpiry });
    await cli("mark-passed", EMAIL, "--confirm");
    await cli("reopen-candidate", EMAIL, "--confirm");

    assert.equal(held("ORAL_QB_NOTES"), PERPETUAL);
    assert.equal(held("SOLVED_QP"), writtenExpiry);
  });

  test("reopening somebody who was never closed mints nothing", async () => {
    seed({ ORAL_QB_NOTES: PERPETUAL });
    const r = await cli("reopen-candidate", EMAIL, "--confirm");
    assert.match(r.out, /nothing to do/);
    assert.equal(held("ORAL_QB_NOTES"), PERPETUAL);

    seed({ SOLVED_QP: undefined });
    store.set(ENT, new Map());
    plain.set(`miw:user:${EMAIL}`, "sha256$salt$digest");
    const r2 = await cli("reopen-candidate", EMAIL, "--confirm");
    assert.match(r2.out, /nothing to do/);
    assert.equal(held("SOLVED_QP"), undefined);
  });
});

// -------------------------------------------------------------
describe("summary counts what is actually stored", () => {
  test("the four Founder-facing figures come out of the store", async () => {
    const future = String(Math.floor(Date.now() / 1000) + 100 * 86400);
    const past = String(Math.floor(Date.now() / 1000) - 100 * 86400);
    store.clear();
    plain.clear();
    store.set("miw:ent:a@x.com", new Map([["ORAL_QB_NOTES", PERPETUAL]]));
    store.set("miw:ent:b@x.com", new Map([["ORAL_QB_NOTES", `passed:${Math.floor(Date.now() / 1000)}:1`]]));
    store.set("miw:ent:c@x.com", new Map([["SOLVED_QP", future]]));
    store.set("miw:ent:d@x.com", new Map([["SOLVED_QP", past]]));

    const r = await cli("summary");
    assert.equal(r.code, 0);
    assert.match(r.out, /accounts with an entitlement record : 4/);
    assert.match(r.out, /Candidate-Lifecycle ACTIVE\s+: 1/);
    assert.match(r.out, /Candidate-Lifecycle PASSED_CLOSED : 1/);
    assert.match(r.out, /Fixed-term ACTIVE\s+: 1/);
    assert.match(r.out, /Fixed-term EXPIRED\s+: 1/);
  });

  test("summary needs no email and writes nothing", async () => {
    store.clear();
    plain.clear();
    store.set("miw:ent:a@x.com", new Map([["ORAL_QB_NOTES", PERPETUAL]]));
    const before = JSON.stringify([...store.get("miw:ent:a@x.com")]);
    await cli("summary");
    assert.equal(JSON.stringify([...store.get("miw:ent:a@x.com")]), before);
  });
});
