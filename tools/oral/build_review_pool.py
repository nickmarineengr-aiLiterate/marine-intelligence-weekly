"""Build the ranked Oral QB review pool from committed repository evidence.

The pool answers "which cards still need an independent whole-card read", and
its governing rule is CORRECTED != REVIEWED: correction manifests RANK a card,
they never clear it. The only thing that removes a card is an explicit
WHOLE_CARD entry in tools/oral/review_pool_accepts.json, and later evidence
reopens even that.

Prose reviews (GPT_REVIEW_*.md) are read for HINTS only. A card they call
"untouched" is surfaced as UNKNOWN / manual adjudication - never excluded.

  PYTHONIOENCODING=utf-8 python tools/oral/build_review_pool.py [--check]

Outputs (generated, git-ignored - regenerate, do not edit):
  reports/oral-review-pool/review_pool.json
  reports/oral-review-pool/review_pool.md

Exit 0 written / current, 1 stale (with --check), 2 an input was unavailable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio, write_text      # noqa: E402
import review_pool as RP                                  # noqa: E402

enable_utf8_stdio()

MANIFEST_GLOB = "*manifest*.json"
PROSE_DIR = REPO / "meoclass1" / "oral-intelligence" / "examiner-audit"
PROSE_GLOB = "GPT_REVIEW_*.md"
ACCEPTS = HERE / "review_pool_accepts.json"
OUT_DIR = REPO / "reports" / "oral-review-pool"


def load_manifests():
    docs = []
    for path in sorted(HERE.glob(MANIFEST_GLOB)):
        try:
            docs.append((path.name,
                         json.loads(path.read_text(encoding="utf-8"))))
        except ValueError as exc:
            raise RP.PoolError("%s: cannot parse as JSON - %s"
                               % (path.name, exc)) from exc
    if not docs:
        raise RP.PoolError("no manifests matched %s under %s"
                           % (MANIFEST_GLOB, HERE))
    return docs


def sha256_of(path):
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generator_commit():
    """Best-effort provenance. Never fatal - the pool must build without git."""
    try:
        out = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, timeout=15)
        return out.stdout.strip() or None if out.returncode == 0 else None
    except Exception:                                      # noqa: BLE001
        return None


def build():
    docs = load_manifests()
    evidence = RP.collect_evidence(docs)
    accepts = RP.load_accepts(ACCEPTS, set(evidence))
    hints = RP.extract_prose_hints(sorted(PROSE_DIR.glob(PROSE_GLOB))
                                   if PROSE_DIR.is_dir() else [])
    return RP.build_pool(docs, accepts=accepts, prose_hints=hints)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="verify the written pool matches the evidence; write nothing")
    args = ap.parse_args(argv)

    try:
        pool = build()
    except RP.PoolError as exc:
        print("REVIEW POOL: REFUSED - %s" % exc)
        return 2

    json_path = OUT_DIR / "review_pool.json"
    digest = RP.content_hash(pool)

    if args.check:
        if not json_path.exists():
            print("REVIEW POOL: STALE - %s has not been generated" % json_path)
            return 1
        try:
            written = json.loads(json_path.read_text(encoding="utf-8"))
            same = written["provenance"]["canonical_sha256"] == digest
        except Exception as exc:                           # noqa: BLE001
            print("REVIEW POOL: STALE - cannot read written pool (%s)" % exc)
            return 1
        if not same:
            print("REVIEW POOL: STALE - evidence has moved since the pool was built")
            return 1
        print("REVIEW POOL: CURRENT (%d cards, canonical %s)"
              % (pool["summary"]["cards_in_pool"], digest[:12]))
        return 0

    doc = RP.build_document(pool,
                            accepts_hash=sha256_of(ACCEPTS),
                            generator_commit=generator_commit())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_text(json_path, json.dumps(doc, sort_keys=True, ensure_ascii=False,
                                     indent=1) + chr(10))
    write_text(OUT_DIR / "review_pool.md", RP.render_markdown(pool))

    s = pool["summary"]
    print("REVIEW POOL: WRITTEN - %d in pool, %d accepted-out, %d reopened, "
          "%d unknown (canonical %s)"
          % (s["cards_in_pool"], s["explicitly_accepted"], s["reopened"],
             s["unknown_manual_adjudication"], digest[:12]))
    print("  %s" % json_path.relative_to(REPO).as_posix())
    print("  %s" % (OUT_DIR / "review_pool.md").relative_to(REPO).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
