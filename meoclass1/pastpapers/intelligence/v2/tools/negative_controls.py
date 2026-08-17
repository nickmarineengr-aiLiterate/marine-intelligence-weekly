# -*- coding: utf-8 -*-
"""Superseded by tools/adversarial_controls.py.

This file used to carry its own copy of the classifier. That is precisely how
the model drifted: the copy here and the copy in match_bank_to_corpus.py both
held a short-stem floor in the caller rather than in the classifier, so calling
the classifier directly bypassed it.

NC-1 through NC-6 are retained verbatim as controls in adversarial_controls.py,
which imports the one classifier in tools/qi_similarity.py. This shim runs that
suite so the old entry point keeps working.
"""
from __future__ import unicode_literals

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    sys.stderr.write(
        'negative_controls.py is superseded; running adversarial_controls.py\n\n')
    import adversarial_controls
    sys.exit(adversarial_controls.main())
