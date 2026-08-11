// =============================================================
// Marine Intelligence Weekly — Upstash REST helpers (Node runtime)
// File: api/_lib/redis.js
//
// Consolidates the copy-pasted helpers that previously lived in
// verify-payment.js, razorpay-webhook.js and check-password.js.
// Behaviour is intentionally identical to the originals — in
// particular redisSetNX still uses the raw-command POST form,
// because NX is a bare flag and query-string encoding does not
// express it reliably. The webhook/verify send-lock races against
// this exact call shape, so it must not drift.
// =============================================================

const URL_BASE = () => process.env.KV_REST_API_URL;
const TOKEN = () => process.env.KV_REST_API_TOKEN;

function assertConfigured() {
  if (!URL_BASE() || !TOKEN()) {
    const e = new Error("Redis not configured");
    e.status = 500;
    throw e;
  }
}

/** Raw Redis command via Upstash's POST form. The unambiguous path. */
export async function redisCmd(args) {
  assertConfigured();
  const r = await fetch(URL_BASE(), {
    method: "POST",
    headers: {
      Authorization: `Bearer ${TOKEN()}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(args),
  });
  return r.json();
}

export async function redisGet(key) {
  const data = await redisCmd(["GET", key]);
  return data.result ?? null;
}

export async function redisSet(key, value) {
  const data = await redisCmd(["SET", key, value]);
  return data.result === "OK";
}

export async function redisSetEx(key, value, ttlSeconds) {
  const data = await redisCmd(["SET", key, value, "EX", ttlSeconds]);
  return data.result === "OK";
}

export async function redisDel(key) {
  const data = await redisCmd(["DEL", key]);
  return data.result;
}

export async function redisIncr(key) {
  const data = await redisCmd(["INCR", key]);
  return data.result;
}

/**
 * Atomic claim — SET key val NX EX ttl. True for exactly ONE caller.
 * Shared idempotency primitive between verify-payment and the webhook.
 */
export async function redisSetNX(key, value, ttlSeconds = 86400) {
  const data = await redisCmd(["SET", key, value, "NX", "EX", ttlSeconds]);
  return data.result === "OK";
}

/**
 * Multi-command pipeline via Upstash's /pipeline endpoint.
 * Returns an array of {result} objects, one per command, in order.
 *
 * Commands run sequentially on one connection but are NOT a MULTI
 * transaction. Every caller here is written so that any interleaving
 * of two concurrent pipelines still leaves a correct final state.
 */
export async function redisPipeline(commands) {
  assertConfigured();
  const r = await fetch(`${URL_BASE()}/pipeline`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${TOKEN()}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(commands),
  });
  return r.json();
}

/** SCAN wrapper for the migration tool. Returns {cursor, keys}. */
export async function redisScan(cursor, match, count = 200) {
  const data = await redisCmd(["SCAN", String(cursor), "MATCH", match, "COUNT", String(count)]);
  const [next, keys] = data.result || ["0", []];
  return { cursor: next, keys: keys || [] };
}
