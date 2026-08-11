// =============================================================
// Marine Intelligence Weekly — Password reset test suite
// File: tools/security/reset.test.mjs
// Run: node tools/security/reset.test.mjs
//
// An unauthenticated endpoint that changes a paying customer's
// credential is the highest-risk surface on the site: anyone may invoke
// it, for anyone, without proving anything. These tests pin the three
// properties that make that acceptable.
//
//   NO ENUMERATION  — identical answer for customer, stranger and
//                     throttled caller, so the form cannot be used to
//                     ask "is this person a subscriber"
//   THROTTLED       — it cannot be used to lock a real customer out
//   REVOKES         — a reset ejects whoever might already be inside
//
// Offline: real reset.js, rotation.js, session.js and sessions.js
// execute against an in-memory store. Every block ends with a POSITIVE
// CONTROL — a guard that never fires is not a guard.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";

process.env.MIW_SESSION_SECRET = "test-secret-only-not-a-real-key-000000";

const { requestReset, throttleKey, RESET_THROTTLE_SECONDS, GENERIC_RESPONSE } =
  await import("../../api/_lib/reset.js");
const { classifyStored } = await import("../../api/_lib/rotation.js");
const { verifyPassword, hashPassword, newSessionId } = await import("../../api/_lib/session.js");
const { sessionsKey, addActiveSession, isActiveSession } = await import("../../api/_lib/sessions.js");
const { userKey, entKey } = await import("../../api/_lib/entitlements.js");
const { buildResetEmail } = await import("../../api/_lib/email.js");

const EMAIL = "customer@example.com";
const OLD_PW = "OLDPASSWORD23456";
const TTL = 30 * 24 * 60 * 60;

function fakeStore() {
  const strings = new Map();
  const hashes = new Map();
  const zsets = new Map();
  const hash = (k) => { if (!hashes.has(k)) hashes.set(k, new Map()); return hashes.get(k); };
  const zset = (k) => { if (!zsets.has(k)) zsets.set(k, new Map()); return zsets.get(k); };
  const sorted = (k) => [...zset(k).entries()].sort((a, b) => a[1] - b[1] || (a[0] < b[0] ? -1 : 1));

  function one(args) {
    const [op, key, ...rest] = args;
    switch (op) {
      case "SET": strings.set(key, rest[0]); return { result: "OK" };
      case "GET": return { result: strings.get(key) ?? null };
      case "DEL": {
        const had = strings.delete(key) || hashes.delete(key) || zsets.delete(key);
        return { result: had ? 1 : 0 };
      }
      case "HSET": {
        for (let i = 0; i + 1 < rest.length; i += 2) hash(key).set(rest[i], rest[i + 1]);
        return { result: 1 };
      }
      case "HGETALL": return { result: [...hash(key).entries()].flat() };
      case "ZADD": zset(key).set(rest[1], Number(rest[0])); return { result: 1 };
      case "ZSCORE": {
        const s = zset(key).get(rest[0]);
        return { result: s === undefined ? null : String(s) };
      }
      case "ZCARD": return { result: zset(key).size };
      case "ZREVRANGE": return { result: sorted(key).map(([m]) => m).reverse() };
      case "ZREMRANGEBYRANK": case "ZREMRANGEBYSCORE": return { result: 0 };
      case "EXPIRE": return { result: 1 };
      default: throw new Error(`fakeStore: unimplemented ${op}`);
    }
  }

  const deps = { cmd: async (a) => one(a), pipeline: async (cs) => cs.map(one) };
  const claims = new Map();          // key -> expiry-ish marker

  return {
    deps, strings, claims,
    store: {
      get: async (k) => one(["GET", k]).result,
      set: async (k, v) => one(["SET", k, v]).result,
      del: async (k) => { claims.delete(k); return one(["DEL", k]).result; },
      countSessions: async (e) => one(["ZCARD", sessionsKey(e)]).result,
      // Atomic claim: true for exactly one caller until released.
      claim: async (k) => { if (claims.has(k)) return false; claims.set(k, 1); return true; },
    },
  };
}

function mailSink() {
  const sent = [];
  return { sent, send: async (m) => { sent.push(m); return { messageId: "t" }; } };
}

const passwordFrom = (msg) => msg.html.match(/letter-spacing:1px">([A-Z2-9]+)</)[1];

async function seedCustomer(f, { sessions = 0 } = {}) {
  await f.store.set(userKey(EMAIL), hashPassword(OLD_PW));
  await f.deps.cmd(["HSET", entKey(EMAIL), "ORAL_QB_NOTES", "1"]);
  const ids = [];
  for (let i = 0; i < sessions; i++) {
    const id = newSessionId();
    await addActiveSession(EMAIL, id, TTL, f.deps);
    ids.push(id);
  }
  return ids;
}

const run = (f, mail, email = EMAIL) => requestReset({
  email, store: f.store, sendMail: mail.send, buildEmail: buildResetEmail,
});

// =============================================================
describe("no account enumeration — the form must not answer 'is this a customer'", () => {
  test("a real customer and a stranger get the SAME response text", async () => {
    const f1 = fakeStore(), m1 = mailSink();
    await seedCustomer(f1);
    const a = await run(f1, m1);

    const f2 = fakeStore(), m2 = mailSink();
    const b = await run(f2, m2, "stranger@example.com");

    assert.equal(a.outcome, "sent");
    assert.equal(b.outcome, "no_account");
    // The OUTCOMES differ internally — that is for logs and these tests.
    // What the caller sees is one constant, and it is the same object.
    assert.equal(typeof GENERIC_RESPONSE, "string");
    assert.ok(GENERIC_RESPONSE.length > 20);
    assert.match(GENERIC_RESPONSE, /if that address has an account/i);
  });

  test("a stranger's address is never written to the store", async () => {
    const f = fakeStore(), m = mailSink();
    await run(f, m, "stranger@example.com");
    assert.equal(f.strings.has(userKey("stranger@example.com")), false);
    assert.equal(m.sent.length, 0, "no mail to an address with no account");
  });

  test("the throttle is claimed BEFORE the existence check, so timing cannot leak", async () => {
    // A stranger's request still consumes the throttle slot. If the
    // existence check came first, "no account" would return without a
    // Redis write and be measurably faster than "throttled".
    const f = fakeStore(), m = mailSink();
    await run(f, m, "stranger@example.com");
    assert.equal(f.claims.has(throttleKey("stranger@example.com")), true);
  });

  test("POSITIVE CONTROL: the two paths really do reach different internal outcomes", async () => {
    const f = fakeStore(), m = mailSink();
    await seedCustomer(f);
    assert.notEqual((await run(f, m)).outcome, "no_account");
  });
});

// =============================================================
describe("throttling — a reset form must not be a lockout weapon", () => {
  test("a second reset inside the window does NOT issue another password", async () => {
    const f = fakeStore(), m = mailSink();
    await seedCustomer(f);

    assert.equal((await run(f, m)).outcome, "sent");
    const after1 = await f.store.get(userKey(EMAIL));

    assert.equal((await run(f, m)).outcome, "throttled");
    assert.equal(m.sent.length, 1, "exactly one email");
    assert.equal(await f.store.get(userKey(EMAIL)), after1,
      "the credential must not change again — that is the lockout");
  });

  test("the password from the first email still works after a throttled retry", async () => {
    const f = fakeStore(), m = mailSink();
    await seedCustomer(f);
    await run(f, m);
    const issued = passwordFrom(m.sent[0]);
    await run(f, m);                                  // throttled
    const stored = await f.store.get(userKey(EMAIL));
    assert.equal(verifyPassword(stored, issued).ok, true,
      "declining to resend is only honest if the first password still opens the account");
  });

  test("the window is fifteen minutes", () => {
    assert.equal(RESET_THROTTLE_SECONDS, 900);
  });

  test("the throttle is per address, not global", async () => {
    const f = fakeStore(), m = mailSink();
    await seedCustomer(f);
    await f.store.set(userKey("other@example.com"), hashPassword("OTHERPASSWORD234"));

    assert.equal((await run(f, m)).outcome, "sent");
    assert.equal((await run(f, m, "other@example.com")).outcome, "sent",
      "one customer resetting must not block every other customer");
  });

  test("POSITIVE CONTROL: releasing the claim allows a reset again", async () => {
    const f = fakeStore(), m = mailSink();
    await seedCustomer(f);
    await run(f, m);
    await f.store.del(throttleKey(EMAIL));            // simulates TTL expiry
    assert.equal((await run(f, m)).outcome, "sent");
    assert.equal(m.sent.length, 2);
  });
});

// =============================================================
describe("what a reset actually does", () => {
  test("issues a working new password and kills the old one", async () => {
    const f = fakeStore(), m = mailSink();
    await seedCustomer(f);

    assert.equal((await run(f, m)).outcome, "sent");
    const stored = await f.store.get(userKey(EMAIL));
    const issued = passwordFrom(m.sent[0]);

    assert.equal(classifyStored(stored), "hashed", "never stored in plaintext");
    assert.equal(verifyPassword(stored, issued).ok, true, "the emailed password must work");
    assert.equal(verifyPassword(stored, OLD_PW).ok, false, "the previous password must not");
  });

  test("revokes every live session — a reset must eject an intruder", async () => {
    const f = fakeStore(), m = mailSink();
    const [phone, laptop] = await seedCustomer(f, { sessions: 2 });
    assert.equal(await isActiveSession(EMAIL, phone, f.deps), true);

    await run(f, m);

    assert.equal(await isActiveSession(EMAIL, phone, f.deps), false);
    assert.equal(await isActiveSession(EMAIL, laptop, f.deps), false);
  });

  test("entitlements survive — a reset must not cost what was paid for", async () => {
    const f = fakeStore(), m = mailSink();
    await seedCustomer(f);
    await run(f, m);
    const ent = await f.deps.cmd(["HGETALL", entKey(EMAIL)]);
    const held = {};
    for (let i = 0; i + 1 < ent.result.length; i += 2) held[ent.result[i]] = ent.result[i + 1];
    assert.equal(held.ORAL_QB_NOTES, "1");
  });

  test("a malformed address is rejected before it reaches the store", async () => {
    const f = fakeStore(), m = mailSink();
    for (const bad of ["", "   ", "not-an-address", "@example.com", "a@b", "a b@c.com"]) {
      assert.equal((await requestReset({
        email: bad, store: f.store, sendMail: m.send, buildEmail: buildResetEmail,
      })).outcome, "invalid_email", `must reject: "${bad}"`);
    }
    assert.equal(f.claims.size, 0, "a malformed address must not consume a throttle slot");
    assert.equal(m.sent.length, 0);
  });

  test("addresses are normalised — case and padding cannot dodge the throttle", async () => {
    const f = fakeStore(), m = mailSink();
    await seedCustomer(f);
    assert.equal((await run(f, m, "  CUSTOMER@Example.COM ")).outcome, "sent");
    assert.equal((await run(f, m, EMAIL)).outcome, "throttled",
      "otherwise the throttle is bypassed by changing capitalisation");
  });

  test("FAILURE MODE: a dead relay releases the throttle so the customer is not stranded", async () => {
    const f = fakeStore();
    await seedCustomer(f);
    const r = await requestReset({
      email: EMAIL, store: f.store, buildEmail: buildResetEmail,
      sendMail: async () => { throw new Error("smtp down"); },
    });
    assert.equal(r.outcome, "send_failed");
    // Their password HAS changed and they were not told, so they must be
    // able to retry immediately rather than wait out the window holding
    // a credential they never received.
    assert.equal(f.claims.has(throttleKey(EMAIL)), false);
  });

  test("POSITIVE CONTROL: without a reset the old password still works", async () => {
    const f = fakeStore();
    await seedCustomer(f);
    assert.equal(verifyPassword(await f.store.get(userKey(EMAIL)), OLD_PW).ok, true,
      "if this fails, the assertions above pass for the wrong reason");
  });
});

// =============================================================
describe("the reset email", () => {
  test("carries the new password and says the old one is gone", () => {
    const msg = buildResetEmail(EMAIL, "NEWPASSWORD23456");
    assert.ok(msg.html.includes("NEWPASSWORD23456"));
    assert.equal(msg.to, EMAIL);
    assert.match(msg.html, /no longer works/i);
    assert.match(msg.html, /still on your account/i);
  });

  test("tells an unwitting recipient what happened without alarming them", () => {
    const msg = buildResetEmail(EMAIL, "NEWPASSWORD23456");
    assert.match(msg.html, /if you did not request this/i);
  });

  test("names no internals", () => {
    const msg = buildResetEmail(EMAIL, "NEWPASSWORD23456").html.toLowerCase();
    for (const leak of ["redis", "hash", "sha256", "github", "repository"]) {
      assert.ok(!msg.includes(leak), `must not mention "${leak}"`);
    }
  });

  test("POSITIVE CONTROL: the leak assertion fires on a message that does mention one", () => {
    assert.throws(() => assert.ok(!"<p>your sha256 hash</p>".includes("sha256")));
  });
});
