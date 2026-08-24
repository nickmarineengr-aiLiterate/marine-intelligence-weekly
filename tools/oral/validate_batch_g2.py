"""Validate batch G2 - the second August 2026 fresh-intake production batch.

G2 makes exactly the same claims as G1 and is checked by exactly the same
contract, so this file supplies the batch's paths and reuses that contract
rather than copying three hundred lines. The alternative - a second, drifting
copy - is how ten batch validators each grew their own version of the sibling
glob and then disagreed about it.

  PYTHONIOENCODING=utf-8 python tools/oral/validate_batch_g2.py

Exit 0 all checks pass, 1 one or more failed.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

import validate_batch_g1 as G  # noqa: E402

MANIFEST = HERE / "batch_g2_manifest.json"
REVIEW = (REPO / "meoclass1" / "oral-intelligence" / "examiner-audit"
          / "AUGUST2026_BATCH_G2_REVIEW.json")


if __name__ == "__main__":
    raise SystemExit(G.main(manifest_path=MANIFEST, review_path=REVIEW, label="g2"))
