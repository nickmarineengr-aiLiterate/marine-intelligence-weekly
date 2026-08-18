# -*- coding: utf-8 -*-
"""The single source of path truth for the Question Intelligence v2 layer.

Phase 3A resolved some paths from the repository and hardcoded others to a
Desktop drive. The Laptop review proved the cost: `validate_families.py`
silently skipped two checks and let one mutation escape, and
`match_bank_to_corpus.py` would not run at all — because `SPECS` pointed at an
absolute `D:` path to reach *committed repository content* sitting two
directories above the tool.

Every path the layer needs is derived here from this file's own location, so
the same branch resolves identically on any machine and from any working
directory. Nothing in the layer may name a drive letter.

No tool accepts a `--repo-root` override, and none needs one: every path is
derived from this file, so pointing a tool at another checkout is done by
running that checkout's own copy of the tool. An earlier draft of this module
promised the flag and shipped a `for_root()` helper to serve it; neither the
flag nor a single caller was ever written. A portability layer may not document
a portability escape hatch that does not exist, so the claim and the dead
helper are both gone rather than left to be discovered by someone relying on
them.
"""
from __future__ import unicode_literals

import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(TOOLS)
INTELLIGENCE = os.path.dirname(V2)
PASTPAPERS = os.path.dirname(INTELLIGENCE)
MEOCLASS1 = os.path.dirname(PASTPAPERS)
REPO_ROOT = os.path.dirname(MEOCLASS1)

# --- repository content -----------------------------------------------------
SPECS = os.path.join(PASTPAPERS, 'specs')
HIST = os.path.join(PASTPAPERS, 'intelligence', 'historical_qp_intelligence.json')

# --- the research layer's own artefacts -------------------------------------
FAMILIES = os.path.join(V2, 'QUESTION_FAMILIES.json')
OCCURRENCES = os.path.join(V2, 'QUESTION_OCCURRENCES.jsonl')
MANIFEST = os.path.join(V2, 'SOURCE_MANIFEST.json')
BANK = os.path.join(V2, 'OFFICIAL_BANK_ITEMS.json')
VERIFICATION = os.path.join(V2, 'verification')

# --- the committed official source extract ----------------------------------
# The deterministic extraction of the Directorate's published MEO Class I
# question bank: 185 items, number and text only. It travels with the research
# code so that referential integrity is executable on every machine rather than
# on the one that happens to hold the raw intake directory. The PDF binary
# itself is NOT committed; SOURCE_MANIFEST.json carries the retrieval recipe
# and the sha256 that re-obtains and re-verifies it on demand.
OFFICIAL_SOURCES = os.path.join(PASTPAPERS, 'sources', 'official', 'dgshipping')
EXTRACTED_BANK = os.path.join(OFFICIAL_SOURCES, 'dgs_meo_cl1_bank_items.json')

