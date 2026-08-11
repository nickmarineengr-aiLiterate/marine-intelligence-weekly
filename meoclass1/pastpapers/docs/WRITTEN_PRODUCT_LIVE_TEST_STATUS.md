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
