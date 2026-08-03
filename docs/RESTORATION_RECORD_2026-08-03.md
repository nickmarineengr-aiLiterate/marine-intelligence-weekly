# Restoration record — known_traps.md and qb_content_index.json (2026-08-03)

**Why accidental:** both files were unstaged working-tree deletions with no committed removal, no replacement, and active dependents (`qb_health_check.py` reads both; the MEO Class 1 index page consumes the content index). Founder confirmed the deletions were unintentional.

**Restored from:** HEAD (b57bbf8 file versions — the last commits touching each file; `git checkout -- <files>`). No stale archive or foreign branch used; no Founder content overwritten (deletions were the only local state for these paths).

**Regeneration:** `qb_content_index.json` has no automated builder (it is session-maintained). After byte-exact restoration it was deterministically refreshed: `generated` → 2026-08-03 and one `recently_updated` entry appended covering the MSA-2025 re-basing commits (7044e4b, 30fb6f5, 15 files, HOLD-01/HOLD-03 noted as HELD_PENDING_SUBSTANTIAL_EVIDENCE). No historical correction entries were altered or removed (now 24 entries).

**Validation:**
- JSON re-parses; historical entries intact.
- Local per-file reconciliation: **629 q-cards on disk = 629 manifest total; zero per-file mismatches.**
- `qb_health_check.py`: runs; all remaining flags are the pre-existing documented REVIEW-class items (see commit db5c158 / known_traps Entry 20). Note: the script's own tarball-side counter reports 627 — a pre-existing counter quirk, not an index error (local reconciliation is exact).
- known_traps.md: 26,392 bytes, structure and entries intact, available for candidate correction reports.

**Final status: RESTORED AND CURRENT.**
