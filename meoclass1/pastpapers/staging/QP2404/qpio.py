"""Canonical QP spec IO: indent=1, LF, trailing newline, ensure_ascii=False.

Matches the on-disk convention byte-for-byte. CRLF corrupts content-hashed
assets on this repository, so newline='' + explicit \n is used rather than
letting Windows translate.
"""
import io, json, os

# Derived from this file's own location, not a drive letter: the repository lives
# on an external volume whose letter is not guaranteed. staging/QP2404 -> ../../specs
SPECS = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', 'specs')) + os.sep


def load(paper):
    with io.open(SPECS + paper + '.json', encoding='utf-8') as f:
        return json.load(f)


def q(spec, qid):
    return [x for x in spec['questions'] if x['question_id'] == qid][0]


def save(spec):
    text = json.dumps(spec, ensure_ascii=False, indent=1) + '\n'
    with io.open(SPECS + spec['paper_id'] + '.json', 'w',
                 encoding='utf-8', newline='') as f:
        f.write(text)
