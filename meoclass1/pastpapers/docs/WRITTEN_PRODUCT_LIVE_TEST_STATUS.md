# WRITTEN PRODUCT — LIVE TEST STATUS

**Status: NOT DEPLOYED. LIVE DEPLOYMENT BLOCKED.**
Assessed 2026-08-11 in the parallel-production baseline session, under Founder authorisation to
deploy the current built system for controlled real-world testing.

The Founder authorised live deployment. That authorisation was explicitly conditioned:

> *"FOUNDER AUTHORISES LIVE DEPLOYMENT, BUT NOT AN INSECURE DEPLOYMENT. If a security prerequisite
> that would expose paid content, credentials, customer data or payment secrets is objectively
> unresolved: STOP BEFORE PRODUCTION DEPLOYMENT."*

**A security prerequisite is objectively unresolved.** Deployment was therefore not performed. No
secret was set, no branch was merged to `main`, no route was published. This file records why, and
exactly what the Founder must do.

---

## 1. THE BLOCKER

### `LAUNCH-BLOCK-1` — published customer credentials still authenticate

**Severity: BLOCKER. Status: OPEN, ACTIVE, ONGOING.**

Twenty-eight real customer email/password pairs are **published in plaintext in a public GitHub
repository** and **those same credentials still authenticate today**.

This was previously recorded as *"customer passwords have not been confirmed rotated —
UNCONFIRMED"*. That understates it. The exposure is not unconfirmed; it is **confirmed and
continuing**.

#### The four facts, each verified this session

| # | Fact | How it was verified |
|---|---|---|
| 1 | The repository is **public** | GitHub API: `"private": false`, `"visibility": "public"` |
| 2 | A source file containing 28 email→plaintext-password pairs is **in pushed history** | the blob is reachable at `0766d00^:api/migrate-users.js`; `0766d00` is `origin/main` |
| 3 | Login **still accepts those plaintext records** | `api/_lib/session.js::verifyPassword` has an explicit legacy plaintext branch |
| 4 | Deleting the file did **not** remove the credentials | nine commits across history add and delete these files; every one is on the public remote |

#### Why the earlier remediation did not close it

Commit `0766d00`, *"SECURITY: remove two credential-disclosing endpoints from production"*, removed
`api/check-db.js` and `api/migrate-users.js` from the working tree. That was correct and necessary,
and it did stop the *live endpoints* from serving credentials.

It did not, and could not, remove the credentials from the **published history**.

> **Removing a file from a git repository does not remove it from the repository.**
> `git ls-tree HEAD` reports both files ABSENT — the required pre-merge check passes — while the
> blobs remain fetchable by anyone from the public remote.

The check that was run proved *"not in the current tree"*. The claim that mattered was *"no longer
disclosed"*. Those are different claims and only the first was ever tested.

#### What each removed endpoint did

- **`api/check-db.js`** — unauthenticated `GET /api/check-db?email=…` returned that account's
  stored password in the JSON body. No secret, no session, no rate limit.
- **`api/migrate-users.js`** — guarded only by a hardcoded query secret, which is itself printed in
  the same public file. It contains the full 28-account credential table as a literal.

#### Why it is a deployment blocker specifically

The system being deployed is a **paid entitlement gate**. Login mints a signed session and returns
the account's entitlements. Any holder of a published password can therefore sign in as that
customer and receive that customer's paid entitlements — and, because `check-password.js`
transparently upgrades a legacy plaintext record to a salted hash on first successful login, an
attacker's login would *also* silently convert the record, destroying the signal that the legacy
credential was ever used.

Deploying the gate does not contain this. It **activates** it: today the paid content is exposed
generally, and after deployment it would be exposed specifically to whoever holds the published
list, wearing a legitimate customer's identity.

The affected list includes the **Founder's own accounts**.

---

## 2. REQUIRED FOUNDER ACTION

No action below was taken. Each requires the Founder's decision, and two of them require
credential handling that must not be automated from here.

| # | Action | Why |
|---|---|---|
| **1** | **Rotate all 28 credentials.** Every account in the published table must be issued a new password. | The published values must stop being valid. This is the one action that actually closes the blocker. |
| **2** | **Invalidate the legacy plaintext path.** Once rotation is complete, remove the plaintext branch from `verifyPassword` so no un-rotated record can ever authenticate. | Fail closed. While that branch exists, one missed account reopens the hole. |
| **3** | **Treat the published passwords as permanently compromised.** | Even after history rewriting, they must be assumed to have been cloned, forked, cached and indexed. Never reissue any of them. |
| **4** | **Decide on history remediation.** Purging the blobs (e.g. history rewrite + force push) reduces future casual discovery but **does not** undo the disclosure. | This is a containment measure, not a fix, and it rewrites a public repository — a Founder decision, not an engineering default. |
| **5** | **Notify the affected account holders.** | 27 of the 28 are third parties whose credentials were published. There may be a disclosure obligation; that is a Founder/legal judgement, not one to be made here. |

**Sequencing:** action 1 must complete before any paid surface is deployed. Actions 2–5 should
follow, but only action 1 gates deployment.

**Do not weaken security to unblock deployment.** A fail-closed system that denies everyone is
preferable to an exposed one. This was explicit in the authorisation.

---

## 3. WHAT WAS *NOT* A BLOCKER

Reported here so the blocker is not confused with ordinary incompleteness. **None of these
prevented deployment.**

| Item | Status |
|---|---|
| Product is partial — 13 of 28 papers solved | **Not a blocker.** Coverage is stated honestly; `coverage_check.py` proves no fabricated sitting |
| FSS / MARPOL corpus enrichment incomplete | **Not a blocker.** Producer team resolving; consumer layer degrades cleanly |
| Provision viewer not built | **Not a blocker.** Deferred by Founder decision |
| `BUNDLE` has no approved price | **Not a blocker** for deployment; it only prevents selling a bundle |
| Security stack is inert / no secrets set | **Not a blocker in itself** — it is a *consequence* of not deploying. Middleware fails closed |

---

## 4. PRE-DEPLOY ACCEPTANCE — RUN AND GREEN

The release candidate was fully validated. **The build is ready; the credential state is not.**

| Check | Result |
|---|---|
| `run_toolchain.py` | **ALL STAGES PASS**, 140 warnings |
| `run_toolchain.py --self-test` | **ALL STAGES PASS** |
| `solvedqp_check.py --self-test` | **PASS** — 117 questions across 13 papers; year navigation guard fired on the seeded regression |
| `coverage_check.py --self-test` | **PASS** — seeded fabricated sitting `(2099, 12)` was caught |
| `consumer_adapter_test.py` | **60 checks, 0 failures** |
| `security.test.mjs` | **34/34 pass** |
| `sessions.test.mjs` | **28/28 pass** |
| **Determinism** | A full toolchain run left the tracked tree **byte-identical**. No global derived artefact drifted |
| **Unsafe endpoint check** | `api/check-db.js` and `api/migrate-users.js` **absent from the release tree** — but see §1: absence from the tree is not absence from history |

Delivery inventory at assessment: `solvedQP/` — **13 papers, 117 questions, 3 year sheets, 1
index**, clean across 22 pages.

---

## 4a. PRODUCTION ENVIRONMENT CONFIGURATION

Read from the Vercel project `marineintelligenceweekly/marine-intelligence-weekly` on 2026-08-11.
**Presence only. No value was displayed, and every entry is marked Sensitive and unreadable.**

| Variable | Production | Note |
|---|---|---|
| `KV_REST_API_URL` | **CONFIGURED** | |
| `KV_REST_API_TOKEN` | **CONFIGURED** | |
| `KV_URL` · `REDIS_URL` · `KV_REST_API_READ_ONLY_TOKEN` | CONFIGURED | |
| `RAZORPAY_KEY_ID` · `RAZORPAY_KEY_SECRET` · `RAZORPAY_WEBHOOK_SECRET` | CONFIGURED | |
| `BREVO_*` (4) | CONFIGURED | |
| `QB_PASSWORD_POOL` | CONFIGURED | the legacy plaintext pool — in scope for `LAUNCH-BLOCK-1` rotation |
| **`MIW_SESSION_SECRET`** | **MISSING** | |

### `LAUNCH-BLOCK-2` — `MIW_SESSION_SECRET` is not set in production

**Severity: BLOCKER for a working deployment. Independent of `LAUNCH-BLOCK-1`.**

`check-password.js` refuses to issue sessions without it, and `middleware.js` fails closed. A
deploy in this state would therefore be *safe but useless*: it denies **everyone**, including
paying customers. It must be set (≥16 random characters, for **both** the Edge and Node runtimes)
before deployment — but **only after** `LAUNCH-BLOCK-1` is closed, since setting it is what turns
the gate on.

This is a genuine second gate, not a restatement of the first. Closing `LAUNCH-BLOCK-1` alone would
still not produce a working live product.

---

## 5. NOT TESTED — because nothing was deployed

Every item below was in scope and is **untested**, not passed:

- live access matrix (public / Oral-only / Solved-only / dual entitlement)
- live deep-link redirect to `/SQ/pay.html?next=…` and return after entitled login
- live session behaviour: refresh, logout, expiry, two-session policy, third-session eviction
- forged `miw_auth` / client-hint rejection, path-traversal normalisation, fail-closed behaviour
- the free January sample from both public entry paths, live
- live SolvedQP home, year sheets, Planned-soon and No-sitting cards
- live production environment configuration for `MIW_SESSION_SECRET`, `KV_REST_API_URL`,
  `KV_REST_API_TOKEN`

**These were not skipped for convenience.** Exercising the live access matrix requires test
accounts in the same credential store that is currently compromised, so testing it would neither be
safe nor produce a trustworthy result.

**No payment was made.** No real or test-mode transaction was performed, no price was altered, no
`BUNDLE` price was set.

---

## 6. RETEST REQUIREMENTS

When `LAUNCH-BLOCK-1` action 1 is complete, the next session must, **in this order**:

1. Re-verify that no published credential authenticates — confirm against the rotated store.
2. Confirm the legacy plaintext branch is removed or provably unreachable.
3. Confirm production environment configuration (report CONFIGURED / MISSING only, never values).
4. Verify fail-closed: a missing security dependency **denies** paid content rather than bypassing
   middleware.
5. Deploy, then run every item in §5 live using **controlled test accounts only** — never a real
   customer credential.
6. Record the deployment commit and the live results in this file.

---

## 7. RECORD

| | |
|---|---|
| Assessed | 2026-08-11 |
| Assessed at | `workflow/corpus-consumer-integration` |
| Deployment commit | **NONE — not deployed** |
| Routes tested live | **NONE** |
| Test accounts created | **NONE** |
| Credentials in this file | **NONE**, by design. The affected accounts are identified by their location in history, never reproduced here |
| Merge to `main` | **NOT PERFORMED** |
| Verdict | **LIVE DEPLOYMENT BLOCKED** |

---

# SESSION 2 — 2026-08-12 — REMEDIATION ATTEMPT

Assessed on `release/written-live-test-v1`. The intent was to close both blockers, reconcile with
`main`, and deploy for controlled testing. **Deployment was again not performed.** Two of the three
blockers cannot be closed from an engineering session at all, and the third was found to be larger
than previously recorded.

## 8. `LAUNCH-BLOCK-3` — production has no Security V2 at any level

**Severity: BLOCKER. Status: OPEN. Newly characterised this session.**

Earlier sessions recorded that paid content was exposed. This session established *why*, and the
reason changes what deployment means.

`origin/main` (`0766d00`) contains **no `api/_lib/`, no `middleware.js`, and no Security V2
`check-password.js`**. Verified by `git ls-tree -r origin/main`. The entire signed-session
architecture — session minting, entitlement lookup, Edge middleware gating — exists **only on
unmerged branches**. Production has never run any of it.

Two consequences follow, and both were verified live against `marineintelligenceweekly.com`:

| Probe | Result |
|---|---|
| `GET /meoclass1/QB1_A.html`, no cookie, no session | **HTTP 200, 280,350 bytes** — the complete paid question bank |
| Gate present in that payload | `if(!/miw_auth=1/.test(document.cookie))` — client-side only |
| `GET /solvedQP/…` | 404 — the Written product has never been deployed, so nothing leaks there |

**The paid Oral product is currently readable by anyone with `curl`.** The redirect is evaluated in
the browser *after* the bytes have already been delivered, so it protects nothing against a client
that simply does not run it. Setting `document.cookie="miw_auth=1"` defeats it in a browser too.

This also explains `LAUNCH-BLOCK-2`. `MIW_SESSION_SECRET` is not "missing by oversight" — it is
absent because **nothing in production consumes it yet**. The two facts are one fact.

> Deployment is therefore not a configuration change. It is an **architecture cutover**: merging
> Security V2 to `main` for the first time, on a live paying product. That is not a step to take in
> the same motion as an unrelated release, and not one to take while `LAUNCH-BLOCK-1` is open.

## 9. WHY ROTATION COULD NOT BE EXECUTED

The rotation mechanism is **built, committed and proven** (`eeb8cfe`; `api/_lib/rotation.js`,
`tools/security/rotate_credentials.mjs`, 22 rehearsal tests). It was not run, for one reason:

**The production datastore is unreachable from an engineering session.** Every credential-bearing
variable on the Vercel project is marked *Sensitive*. `vercel env pull` returns all of them as a
single identical 11-character placeholder — confirmed by an identity test across five variables and
by the fact that `KV_REST_API_URL` does not parse as a URL. No value was displayed at any point.

`rotate_credentials.mjs` requires `KV_REST_API_URL` and `KV_REST_API_TOKEN` and exits `2` without
them. **This is correct behaviour and must not be worked around.** Sensitive-marking is doing its
job; the appropriate response is for the Founder to supply the credentials through a governed
channel, not for the tooling to be loosened.

Consequently the affected-account audit (§4–5 of the session brief) returned **no counts**. The
often-quoted figure of 28 is the size of the *leaked blob*, not a production measurement. The two
diverge: some accounts will have been silently hash-upgraded by ordinary logins since the leak, and
some may no longer exist. **Do not rotate from the blob.** `audit` must be run first.

## 10. WHAT WAS COMPLETED THIS SESSION

| Item | Result |
|---|---|
| Machine preflight, governed stale-session reap | 1 cluster reaped, 259 MB recovered |
| `origin/main` reconciled into `release/written-live-test-v1` | **clean merge**, no conflicts |
| LLMC correction `LEG.3(91)` → `LEG.5(99)` preserved | **YES** — 7 corrected citations; the 2 remaining mentions are correction-footer text documenting the fix |
| Security-endpoint removal preserved | **YES** — `api/check-db.js`, `api/migrate-users.js` absent |
| `security.test.mjs` / `sessions.test.mjs` / `rotation.test.mjs` | **34 + 28 + 22 = 84/84 pass** |
| `run_toolchain.py` and `--self-test` | **ALL STAGES PASS**, 140 warnings |
| `solvedqp_check.py` and `--self-test` | **PASS** — 117 questions, 13 papers |
| Determinism | **byte-identical** across a double build |
| Local site test (10 routes, server torn down) | all **200** |
| Product inventory | **13 Available · 15 Planned soon · 3 No sitting**; 13 papers, 3 year sheets, 1 index |
| Legacy credential-path audit | **clean** — 5 endpoints, no debug/migration/credential-return route; new accounts stored **hashed** |
| `MIW_SESSION_SECRET` set | **NO — deliberately not set.** Per §4a it must follow `LAUNCH-BLOCK-1`, and per §8 it would do nothing until Security V2 ships |

Nothing was pushed, nothing was merged to `main`, no secret was set, no customer record was read or
written, and no email was sent.

## 11. THE THREE BLOCKERS, AND WHO CAN CLOSE THEM

| Blocker | Closable by an engineering session? |
|---|---|
| **1** — published credentials still authenticate | **No.** Needs production datastore credentials from the Founder, then `rotate_credentials.mjs audit`, then `rotate --confirm` |
| **2** — `MIW_SESSION_SECRET` missing | **Yes**, but only meaningfully after 1 and 3 |
| **3** — paid content requires no authentication in production | **No.** Requires a Founder decision to cut Security V2 over to `main` on a live paying product |

**Ordering is forced:** 3 must ship for 2 to matter, and 1 must close before 3 ships — because
deploying the entitlement gate while published passwords still work hands an attacker a legitimate
customer identity rather than merely exposing content. Closing them in any other order makes things
worse.

## 12. SESSION 2 RECORD

| | |
|---|---|
| Assessed | 2026-08-12 |
| Assessed at | `release/written-live-test-v1` (reconciled with `origin/main`) |
| Deployment commit | **NONE — not deployed** |
| Routes tested live | **read-only unauthenticated probes only**, to establish exposure |
| Test accounts created | **NONE** |
| Credentials rotated | **NONE** — mechanism proven, execution blocked on datastore access |
| Emails sent | **NONE** |
| Secrets set or displayed | **NONE** |
| Merge to `main` | **NOT PERFORMED** |
| Verdict | **SECURITY REMEDIATION BLOCKED — DO NOT DEPLOY** |
