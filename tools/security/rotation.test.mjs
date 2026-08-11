// =============================================================
// Marine Intelligence Weekly — Credential rotation test suite
// File: tools/security/rotation.test.mjs
// Run: node tools/security/rotation.test.mjs
//
// THE REHEARSAL. Rotation is customer-impacting and irreversible, so
// the complete path is proven here against a DISPOSABLE account and an
// in-memory Redis double before it is ever pointed at production. No
// real customer, no network, no secrets.
//
// The double is faithful in the way that matters: the REAL functions in
// api/_lib/rotation.js, session.js and sessions.js are what execute.
// Only the transport underneath them is fake, so what passes here is
// the same decision sequence production will run.
//
// The nine claims a rotation must earn, each asserted below:
//   1. the old password works BEFORE rotation      (the control)
//   2. rotation occurs
//   3. the old password FAILS afterwards
//   4. the new credential succeeds
//   5. the stored value is not plaintext
//   6. sessions live before rotation are dead after
//   7. a new session can be established
//   8. entitlements survive rotation untouched
//   9. no password is ever returned to a caller that could log it
//
// Every block ends with a POSITIVE CONTROL: a guard that never fires
// is not a guard.
// =============================================================

import { test, describe } from "node:test";
import assert from "node:assert/strict";

process.env.MIW_SESSION_SECRET = "test-secret-only-not-a-real-key-000000";

const {
  generatePassword, classifyStored, needsRotation,
  rotateAccount, maskEmail, PASSWORD_LENGTH,
} = await import("../../api/_lib/rotation.js");
const { hashPassword, verifyPassword, createSessionToken, newSessionId } =
  await import("../../api/_lib/session.js");
const {
  sessionsKey, legacySessionKey, addActiveSession, isActiveSession,
} = await import("../../api/_lib/sessions.js");
const { userKey, entKey } = await import("../../api/_lib/entitlements.js");
const { buildRotationEmail } = await import("../../api/_lib/email.js");

const TTL = 30 * 24 * 60 * 60;

// A disposable address. Deliberately at example.com, which RFC 2606
// reserves precisely so a test can never reach a real mailbox.
const TEST_EMAIL = "rehearsal.account@example.com";
const OLD_PASSWORD = "LEAKED-FROM-GIT-HISTORY";

// -------------------------------------------------------------
// In-memory Redis double. Strings, hashes and sorted sets — the three
// shapes this path touches. Unimplemented commands throw rather than
// return a plausible empty value, so a typo cannot pass as a success.
// -------------------------------------------------------------
function fakeRedis() {
  const strings = new Map();
  const hashes = new Map();
  const zsets = new Map();

  const hash = (k) => { if (!hashes.has(k)) hashes.set(k, new Map()); return hashes.get(k); };
  const zset = (k) => { if (!zsets.has(k)) zsets.set(k, new Map()); return zsets.get(k); };
  const sorted = (k) =>
    [...zset(k).entries()].sort((a, b) => a[1] - b[1] || (a[0] < b[0] ? -1 : 1));

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
      case "HGET": return { result: hash(key).get(rest[0]) ?? null };
      case "HGETALL": return { result: [...hash(key).entries()].flat() };
      case "ZADD": zset(key).set(rest[1], Number(rest[0])); return { result: 1 };
      case "ZSCORE": {
        const s = zset(key).get(rest[0]);
        return { result: s === undefined ? null : String(s) };
      }
      case "ZCARD": return { result: zset(key).size };
      case "ZREVRANGE": return { result: sorted(key).map(([m]) => m).reverse() };
      case "ZREMRANGEBYRANK": {
        const items = sorted(key);
        let [start, stop] = [Number(rest[0]), Number(rest[1])];
        const n = items.length;
        if (start < 0) start += n;
        if (stop < 0) stop += n;
        let removed = 0;
        for (let i = Math.max(0, start); i <= Math.min(n - 1, stop); i++) {
          zset(key).delete(items[i][0]); removed++;
        }
        return { result: removed };
      }
      case "ZREMRANGEBYSCORE": {
        const maxRaw = String(rest[1]);
        const exclusive = maxRaw.startsWith("(");
        const max = Number(exclusive ? maxRaw.slice(1) : maxRaw);
        let removed = 0;
        for (const [m, s] of [...zset(key).entries()]) {
          if (exclusive ? s < max : s <= max) { zset(key).delete(m); removed++; }
        }
        return { result: removed };
      }
      case "EXPIRE": return { result: 1 };
      default: throw new Error(`fakeRedis: unimplemented command ${op}`);
    }
  }

  const deps = { cmd: async (a) => one(a), pipeline: async (cs) => cs.map(one) };

  return {
    deps, strings, zsets,
    // The shape api/_lib/rotation.js expects.
    store: {
      get: async (k) => one(["GET", k]).result,
      set: async (k, v) => one(["SET", k, v]).result,
      del: async (k) => one(["DEL", k]).result,
      countSessions: async (e) => one(["ZCARD", sessionsKey(e)]).result,
    },
  };
}

/** A mail sink that records what would have been delivered. */
function mailSink() {
  const sent = [];
  return { sent, send: async (m) => { sent.push(m); return { messageId: "test" }; } };
}

/**
 * Replays api/check-password.js's decision sequence against the REAL
 * password and session functions. This is what makes "the old password
 * fails afterwards" a claim about production behaviour rather than
 * about the test's own arithmetic.
 */
async function login(redis, email, password) {
  const stored = await redis.store.get(userKey(email));
  const { ok } = verifyPassword(stored, password);
  if (!ok) return { ok: false };
  const sessionId = newSessionId();
  await addActiveSession(email, sessionId, TTL, redis.deps);
  return { ok: true, sessionId, token: createSessionToken(email, sessionId) };
}

/**
 * THE DELETED VERIFIER, reproduced verbatim.
 *
 * api/_lib/session.js used to fall through to a direct comparison
 * against a plaintext record. That branch is now gone — which is what
 * closes the incident — but its removal also removes the ability to
 * demonstrate the "before" half of a rotation through the production
 * function, since a plaintext record no longer authenticates at all.
 *
 * Reproducing it here keeps the rehearsal meaningful: it proves the
 * rotation moved each record from a form the OLD code would accept to
 * a form only the NEW code accepts. It is a historical fixture and is
 * deliberately NOT imported from anywhere — nothing in the shipped
 * codebase can reach this behaviour any more.
 */
async function legacyLogin(redis, email, password) {
  const stored = await redis.store.get(userKey(email));
  if (!stored) return { ok: false };
  const ok = stored.startsWith("sha256$")
    ? verifyPassword(stored, password).ok
    : stored === String(password || "").trim();
  if (!ok) return { ok: false };
  const sessionId = newSessionId();
  await addActiveSession(email, sessionId, TTL, redis.deps);
  return { ok: true, sessionId, token: createSessionToken(email, sessionId) };
}

/** A store seeded exactly as an affected historical account looks. */
async function seedAffectedAccount(redis) {
  await redis.store.set(userKey(TEST_EMAIL), OLD_PASSWORD);       // legacy plaintext
  await redis.deps.cmd(["HSET", entKey(TEST_EMAIL), "ORAL_QB_NOTES", "1"]);
  await redis.deps.cmd(["HSET", entKey(TEST_EMAIL), "SOLVED_QP", "1"]);
}

// =============================================================
describe("generated credentials — strong enough that a fast hash is not the weak link", () => {
  test("length and alphabet are as declared", () => {
    const p = generatePassword();
    assert.equal(p.length, PASSWORD_LENGTH);
    assert.match(p, /^[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]+$/);
  });

  test("ambiguous characters are excluded — the customer retypes this", () => {
    const sample = Array.from({ length: 200 }, () => generatePassword()).join("");
    for (const ch of "01OIl") {
      assert.ok(!sample.includes(ch), `ambiguous character ${ch} must not be generated`);
    }
  });

  test("passwords do not repeat across a large sample", () => {
    const set = new Set(Array.from({ length: 2000 }, () => generatePassword()));
    assert.equal(set.size, 2000, "a collision at this sample size means the RNG is broken");
  });

  test("POSITIVE CONTROL: a fixed generator would be caught by the collision test", () => {
    const set = new Set(Array.from({ length: 50 }, () => "AAAAAAAAAAAAAAAA"));
    assert.equal(set.size, 1);
  });
});

// =============================================================
describe("classification — who actually needs remediation", () => {
  test("a legacy plaintext record is identified as needing rotation", () => {
    assert.equal(classifyStored(OLD_PASSWORD), "legacy_plaintext");
    assert.equal(needsRotation(OLD_PASSWORD), true);
  });

  test("an already-hashed record is not counted as affected", () => {
    const stored = hashPassword("anything");
    assert.equal(classifyStored(stored), "hashed");
    assert.equal(needsRotation(stored), false);
  });

  test("a missing record is 'absent', never silently treated as safe", () => {
    assert.equal(classifyStored(null), "absent");
    assert.equal(classifyStored(""), "absent");
    assert.equal(classifyStored(undefined), "absent");
  });

  test("POSITIVE CONTROL: a near-miss prefix is NOT mistaken for a hash", () => {
    assert.equal(classifyStored("sha256-notdollar$x$y"), "legacy_plaintext");
    assert.equal(classifyStored("SHA256$x$y"), "legacy_plaintext");
  });
});

// =============================================================
describe("the full rotation path — rehearsed on a disposable account", () => {
  test("CLAIM 1: the exposed password worked BEFORE rotation, under the code of the time", async () => {
    const redis = fakeRedis();
    await seedAffectedAccount(redis);
    // Against the verifier that shipped while the records were plaintext.
    assert.equal((await legacyLogin(redis, TEST_EMAIL, OLD_PASSWORD)).ok, true,
      "the control must hold or the rest proves nothing");
    // And against today's verifier it already fails — the second,
    // independent barrier added by removing the legacy branch.
    assert.equal((await login(redis, TEST_EMAIL, OLD_PASSWORD)).ok, false,
      "current code must refuse a plaintext record outright");
  });

  test("CLAIMS 2-8: rotation invalidates the old, issues the new, keeps what was paid for", async () => {
    const redis = fakeRedis();
    const mail = mailSink();
    await seedAffectedAccount(redis);

    // Two live sessions — the Founder's mobile + laptop policy in force.
    // Established through the verifier of the time, because that is the
    // state a real affected account was actually in.
    const s1 = await legacyLogin(redis, TEST_EMAIL, OLD_PASSWORD);
    const s2 = await legacyLogin(redis, TEST_EMAIL, OLD_PASSWORD);
    assert.equal(await isActiveSession(TEST_EMAIL, s1.sessionId, redis.deps), true);
    assert.equal(await isActiveSession(TEST_EMAIL, s2.sessionId, redis.deps), true);

    const result = await rotateAccount({
      email: TEST_EMAIL,
      store: redis.store,
      sendMail: mail.send,
      buildEmail: buildRotationEmail,
    });

    // CLAIM 2 — rotation occurred, and it counted the sessions it killed.
    assert.equal(result.status, "rotated");
    assert.equal(result.sessionsRevoked, 2);

    // CLAIM 5 — the stored value is a hash, not the password.
    const stored = await redis.store.get(userKey(TEST_EMAIL));
    assert.equal(classifyStored(stored), "hashed");
    assert.ok(!stored.includes(OLD_PASSWORD), "the old secret must not survive in the record");

    // CLAIM 3 — the exposed password no longer authenticates. This is the
    // closure test for the whole incident, and it is asserted against
    // the OLD verifier as well: rotation alone must be sufficient, so
    // that closure does not depend on the code removal having shipped.
    assert.equal((await login(redis, TEST_EMAIL, OLD_PASSWORD)).ok, false);
    assert.equal((await legacyLogin(redis, TEST_EMAIL, OLD_PASSWORD)).ok, false,
      "rotation must close the exposure on its own, not only via the removal");

    // CLAIM 4 + 7 — the credential that was emailed does authenticate,
    // and a fresh session can be established with it.
    assert.equal(mail.sent.length, 1);
    const emailed = mail.sent[0].html.match(/letter-spacing:1px">([A-Z2-9]+)</)?.[1];
    assert.ok(emailed, "the notification must actually carry the new credential");
    assert.ok(!emailed.includes(OLD_PASSWORD));
    const after = await login(redis, TEST_EMAIL, emailed);
    assert.equal(after.ok, true, "the customer must be able to get back in");
    assert.equal(await isActiveSession(TEST_EMAIL, after.sessionId, redis.deps), true);

    // CLAIM 6 — both pre-rotation sessions are dead, INCLUDING the one
    // an attacker might be holding. A rotation that leaves a live
    // session alive has remediated nothing.
    assert.equal(await isActiveSession(TEST_EMAIL, s1.sessionId, redis.deps), false);
    assert.equal(await isActiveSession(TEST_EMAIL, s2.sessionId, redis.deps), false);

    // CLAIM 8 — entitlements are untouched. Rotation is a credential
    // operation; it must never cost a customer what they paid for.
    const ent = await redis.deps.cmd(["HGETALL", entKey(TEST_EMAIL)]);
    const held = {};
    for (let i = 0; i + 1 < ent.result.length; i += 2) held[ent.result[i]] = ent.result[i + 1];
    assert.equal(held.ORAL_QB_NOTES, "1");
    assert.equal(held.SOLVED_QP, "1");
  });

  test("CLAIM 9: the result object carries no password field", async () => {
    const redis = fakeRedis();
    const mail = mailSink();
    await seedAffectedAccount(redis);
    const result = await rotateAccount({
      email: TEST_EMAIL, store: redis.store, sendMail: mail.send, buildEmail: buildRotationEmail,
    });
    assert.equal(Object.hasOwn(result, "password"), false);
    assert.ok(!JSON.stringify(result).includes(OLD_PASSWORD));
  });

  test("the pre-V2 single-session key is cleared too, not just the sorted set", async () => {
    const redis = fakeRedis();
    const mail = mailSink();
    await seedAffectedAccount(redis);
    await redis.store.set(legacySessionKey(TEST_EMAIL), "pre-v2-remnant");

    await rotateAccount({
      email: TEST_EMAIL, store: redis.store, sendMail: mail.send, buildEmail: buildRotationEmail,
    });
    assert.equal(await redis.store.get(legacySessionKey(TEST_EMAIL)), null,
      "a pre-V2 remnant would otherwise outlive the rotation");
  });

  test("the two-session policy is unchanged after rotation — it is not a side effect", async () => {
    const redis = fakeRedis();
    const mail = mailSink();
    await seedAffectedAccount(redis);
    await rotateAccount({
      email: TEST_EMAIL, store: redis.store, sendMail: mail.send, buildEmail: buildRotationEmail,
    });
    const pw = mail.sent[0].html.match(/letter-spacing:1px">([A-Z2-9]+)</)[1];

    const a = await login(redis, TEST_EMAIL, pw);
    const b = await login(redis, TEST_EMAIL, pw);
    assert.equal(await isActiveSession(TEST_EMAIL, a.sessionId, redis.deps), true);
    assert.equal(await isActiveSession(TEST_EMAIL, b.sessionId, redis.deps), true);

    const c = await login(redis, TEST_EMAIL, pw);

    // A third login retires one session rather than failing. What this
    // test owns is that ROTATION did not change that policy, so the
    // assertion is the cap itself.
    //
    // WHICH session is retired is deliberately NOT asserted, and the
    // reason is a real property worth recording rather than hiding.
    // loginCommands issues ZREMRANGEBYRANK <key> 0 -3, and sessions are
    // scored in WHOLE SECONDS. Three logins inside one second therefore
    // tie on score, and Redis breaks a rank tie lexicographically by
    // member — which here is a random hex session id. Inside a
    // one-second window the evicted session is thus arbitrary, and can
    // be the newest one, contradicting the "retires the OLDEST" comment
    // in api/check-password.js.
    //
    // That is a pre-existing property of the session module, not
    // something rotation introduced, and it is out of scope for the
    // incident work — the two-session design is deliberately left
    // untouched. It is reported to the Founder separately.
    // sessions.test.mjs proves the oldest-first ordering properly, by
    // sleeping past a second boundary.
    assert.equal(await redis.store.countSessions(TEST_EMAIL), 2,
      "the cap must still be two — rotation must not widen or narrow it");

    // Exactly two of the three survive. Resolve each check first —
    // Array.filter with an async predicate keeps everything, because a
    // pending Promise is truthy, and would assert nothing at all.
    const alive = await Promise.all(
      [a, b, c].map((s) => isActiveSession(TEST_EMAIL, s.sessionId, redis.deps))
    );
    assert.equal(alive.filter(Boolean).length, 2,
      "one session retired, two kept — the policy itself is unchanged");
  });

  test("an already-hashed account is skipped, not rotated, unless asked", async () => {
    const redis = fakeRedis();
    const mail = mailSink();
    await redis.store.set(userKey(TEST_EMAIL), hashPassword("already-upgraded"));

    const skipped = await rotateAccount({
      email: TEST_EMAIL, store: redis.store, sendMail: mail.send, buildEmail: buildRotationEmail,
    });
    assert.equal(skipped.status, "skipped_already_hashed");
    assert.equal(mail.sent.length, 0, "no customer should be emailed for nothing");

    const forced = await rotateAccount({
      email: TEST_EMAIL, store: redis.store, sendMail: mail.send,
      buildEmail: buildRotationEmail, includeHashed: true,
    });
    assert.equal(forced.status, "rotated");
  });

  test("an account with no credential record is reported, not counted as remediated", async () => {
    const redis = fakeRedis();
    const mail = mailSink();
    const r = await rotateAccount({
      email: "gone@example.com", store: redis.store, sendMail: mail.send,
      buildEmail: buildRotationEmail,
    });
    assert.equal(r.status, "skipped_absent");
    assert.equal(mail.sent.length, 0);
  });

  test("FAILURE MODE: a dead mail relay still leaves the account SECURE", async () => {
    const redis = fakeRedis();
    await seedAffectedAccount(redis);
    const r = await rotateAccount({
      email: TEST_EMAIL,
      store: redis.store,
      sendMail: async () => { throw new Error("smtp down"); },
      buildEmail: buildRotationEmail,
    });
    // Reported honestly as a partial outcome, never as success...
    assert.equal(r.status, "rotated_email_failed");
    // ...but the compromised password is dead all the same.
    assert.equal((await login(redis, TEST_EMAIL, OLD_PASSWORD)).ok, false);
    assert.equal(classifyStored(await redis.store.get(userKey(TEST_EMAIL))), "hashed");
  });

  test("FAILURE MODE: a store that silently drops the write is caught, not reported as done", async () => {
    const redis = fakeRedis();
    await seedAffectedAccount(redis);
    const noOpStore = { ...redis.store, set: async () => "OK" };  // accepts, persists nothing
    await assert.rejects(
      () => rotateAccount({
        email: TEST_EMAIL, store: noOpStore, sendMail: async () => {},
        buildEmail: buildRotationEmail,
      }),
      /did not persist as a hash/,
      "a rotation that did not happen must never be tallied as one"
    );
  });

  test("POSITIVE CONTROL: without rotation the exposed password still works", async () => {
    const redis = fakeRedis();
    await seedAffectedAccount(redis);
    assert.equal((await legacyLogin(redis, TEST_EMAIL, OLD_PASSWORD)).ok, true,
      "if this ever fails, CLAIM 3 above is passing for the wrong reason");
  });
});

// =============================================================
describe("output discipline — this transcript must be safe to keep", () => {
  test("addresses are masked", () => {
    assert.equal(maskEmail("someone@example.com"), "so***@example.com");
    assert.equal(maskEmail("not-an-address"), "***");
  });

  test("the notification carries the credential and nothing about the incident's internals", () => {
    const msg = buildRotationEmail("someone@example.com", "TESTPASSWORD2345");
    assert.ok(msg.html.includes("TESTPASSWORD2345"));
    assert.equal(msg.to, "someone@example.com");
    for (const leak of ["git", "repository", "commit", "GitHub", "blob"]) {
      assert.ok(!msg.html.toLowerCase().includes(leak.toLowerCase()),
        `the notice must not tell the world where to look: "${leak}"`);
    }
  });

  test("the notification states the three things a customer needs", () => {
    const msg = buildRotationEmail("someone@example.com", "TESTPASSWORD2345");
    assert.match(msg.html, /no longer work/i);        // what stopped
    assert.match(msg.html, /access is unchanged/i);   // what they keep
    assert.match(msg.html, /contactus@marineintelligenceweekly\.com/); // who to ask
  });

  test("POSITIVE CONTROL: the leak assertion fires on a message that does mention git", () => {
    assert.throws(() => {
      const html = "<p>your git repository password</p>";
      for (const leak of ["git"]) {
        assert.ok(!html.toLowerCase().includes(leak));
      }
    });
  });
});
