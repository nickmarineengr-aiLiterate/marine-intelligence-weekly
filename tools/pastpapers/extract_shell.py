#!/usr/bin/env python3
"""Lift the design-system <style> block verbatim from a live reference file.

Usage:
  python extract_shell.py [reference.html]

Default reference: meoclass1/oralnotes/WA2-GHG1.html

Writes:
  tools/pastpapers/template/style.css        -- the reference <style> body, byte-for-byte
  tools/pastpapers/template/PROVENANCE.json  -- which file it came from, and its hash

Why this exists rather than a pasted style block in build_paper.py: the repo
already settled this question for the notes series (tools/notes/extract_template.py).
CSS is never retyped and never hand-copied, because a hand-copy silently drifts from
the live design system and nobody notices until two pages look different. Re-run this
whenever the reference file's design changes; the diff on style.css is then the exact
design delta.

This script never edits the reference file.
"""
import hashlib, io, json, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
TPL = os.path.join(HERE, 'template')
DEFAULT_REF = os.path.join(REPO_ROOT, 'meoclass1', 'oralnotes', 'WA2-GHG1.html')


def main(ref):
    if not os.path.exists(ref):
        print('ERROR: reference file not found: %s' % ref)
        sys.exit(1)

    raw = open(ref, encoding='utf-8').read()
    m = re.search(r'<style>(.*?)</style>', raw, re.S)
    if not m:
        print('ERROR: no <style> block found in %s' % ref)
        sys.exit(1)

    css = m.group(1)
    os.makedirs(TPL, exist_ok=True)

    out = os.path.join(TPL, 'style.css')
    with io.open(out, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(css)

    rel = os.path.relpath(ref, REPO_ROOT).replace('\\', '/')
    prov = {
        'extracted_from': rel,
        'source_sha256': hashlib.sha256(raw.encode('utf-8')).hexdigest(),
        'css_sha256': hashlib.sha256(css.encode('utf-8')).hexdigest(),
        'css_bytes': len(css.encode('utf-8')),
        'note': 'Verbatim <style> body. Do not hand-edit style.css -- re-run '
                'extract_shell.py against the reference instead. Series-specific '
                'additions belong in pastpapers.css, never here.',
    }
    with io.open(os.path.join(TPL, 'PROVENANCE.json'), 'w',
                 encoding='utf-8', newline='\n') as fh:
        json.dump(prov, fh, indent=2)
        fh.write('\n')

    tokens = sorted(set(re.findall(r'--[a-z0-9-]+(?=\s*:)', css)))
    classes = sorted(set(re.findall(r'\.([a-z][a-z0-9-]*)\s*[{,]', css)))
    print('extracted %d bytes of CSS from %s' % (prov['css_bytes'], rel))
    print('  -> %s' % os.path.relpath(out, REPO_ROOT).replace('\\', '/'))
    print('  design tokens (%d): %s' % (len(tokens), ' '.join(tokens)))
    print('  classes (%d): %s' % (len(classes), ' '.join(classes)))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_REF)
