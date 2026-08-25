"""Validate batch G3 - the third August 2026 fresh-intake production batch.

G3 makes the same claims as G1 and G2 and is checked by the same contract, so
this file supplies the batch's paths and reuses that contract rather than
copying it. The alternative - a third, drifting copy - is how ten batch
validators each grew their own version of the sibling glob and then disagreed
about it.

G3 does add one thing the shared contract now checks conditionally: a FREEZE
RECORD. Every question identity in this batch was settled and written down
before any answer was, and validate_batch_g1.main reads that record rather than
taking the manifest's word for it - every produced ask must appear in the
freeze, and every frozen ask must be either produced or declared held.

  PYTHONIOENCODING=utf-8 python tools/oral/validate_batch_g3.py

Exit 0 all checks pass, 1 one or more failed.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio      # noqa: E402
import validate_batch_g1 as G                # noqa: E402

# Reach the shared UTF-8 stdio contract directly rather than inheriting it as
# a side effect of importing validate_batch_g1. The infra control scans this
# file's SOURCE, and a contract satisfied only at runtime by somebody else's
# import is exactly the kind of thing that stops being true after a refactor.
enable_utf8_stdio()

MANIFEST = HERE / "batch_g3_manifest.json"
REVIEW = (REPO / "meoclass1" / "oral-intelligence" / "examiner-audit"
          / "AUGUST2026_BATCH_G3_REVIEW.json")


if __name__ == "__main__":
    raise SystemExit(G.main(manifest_path=MANIFEST, review_path=REVIEW, label="g3"))
