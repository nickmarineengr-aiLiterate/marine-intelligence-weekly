# EXECUTION EFFICIENCY POLICY

**Governed by `PRODUCTION_PROTOCOL_INDEX.md`. Read every production session — it is short.**

## The principle

**Claude is the adjudicator, not the manual operator.**

Claude's scarce resource is judgement: what a question actually asks, whether a regulation
applied at the sitting date, whether an answer is defensible. Everything mechanical around
that should be automated, batched, or skipped.

## Rules

1. **Automate repetitive deterministic work.** If an operation will be done more than about
   three times, write the loop instead of repeating the step.
2. **Reuse the existing toolchain before writing anything new.** `tools/pastpapers/` already
   contains validation, audit, recurrence, trap-checking, building and UI testing. Check there
   first.
3. **Cheap scratch scripts are encouraged.** A throwaway script that answers one question is
   good practice. Promote it to `tools/` only if it is genuinely reusable.
4. **Prefer structured intermediate evidence** — a JSON or table you can re-query — over
   re-deriving the same facts by eye across several passes.
5. **Use text extraction for navigation and counting.** Do not re-render a PDF page to find
   out how many questions it has.
6. **Do not re-render or rebuild expensively to check something cheap.** Read the spec.
7. **Batch safe read-only work**; keep write operations deliberate and reviewable.
8. **Automate acceptance checkpoints** — make the check a command that returns pass/fail,
   not a paragraph of prose you have to re-read.
9. **Semantic, legal and technical decisions remain Claude's own.** Never automate the
   judgement itself. A script may gather; only Claude may conclude.
10. **Do not over-engineer.** No framework where a script will do.

## Resource-aware execution — binding on this machine

**Do not parallelise RAM- or disk-heavy operations merely because they are logically
independent.**

The production laptop has **4 cores / 8 threads and a single SATA SSD**. Concurrent Python,
Node, browser, PDF-render and build jobs contend for the same four cores and the same one disk
queue, so the parallel run finishes *later* than a sequential one would.

- Prefer **one structured batch pass**.
- Parallelise only cheap read-only work whose cost is known and small.

**Machine-specific numbers are deliberately not repeated here.** RAM size, session-concurrency
limits and cleanup procedure live in `CLAUDE_MACHINE_OPERATING_POLICY.md` (see
`PRODUCTION_PROTOCOL_INDEX.md` §4), because they describe one laptop and not the product. This
file previously restated a 7.87 GB figure that became false the moment the machine was
upgraded — which is exactly the duplicate-truth failure the protocol architecture exists to
prevent. Read the machine policy for the current concurrency rule.

## Local servers — mandatory teardown

Every locally started server must be stopped by the same command that started it. Four
abandoned `python -m http.server` processes were found on 2026-08-10, the oldest 25 hours old,
two of them double-bound to the same port — meaning a UI verification could have been served
by a stale server pointing at the **wrong directory**.

Forbidden:

```bash
python -m http.server 8899 --directory . >/dev/null 2>&1 &     # no teardown
( python -m http.server 8899 & )                               # detached, unreapable
```

Required:

```bash
python -m http.server 8731 --bind 127.0.0.1 >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null' EXIT
sleep 1
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8731/meoclass1/pastpapers/QP####.html
kill $SRV
```

Start one server per session, reuse it for all checks, kill it when verification completes.
Before finishing, confirm no listener survives.

## Browser and UI verification

- `file://` cannot be inspected properly — serve over HTTP on localhost first.
- Reuse a single browser session; do not open a new one per check.
- Batch desktop and mobile viewport checks in one pass.
- Confirm no browser automation process survives the session.
