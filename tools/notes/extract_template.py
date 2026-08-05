#!/usr/bin/env python3
"""Extract a reusable page shell + one sample topic block from a reference
miw-notes-mgmt Part file.

Writes:
  template/shell_head.html   everything before the first .topic-block
  template/shell_tail.html   everything after the last .topic-block
  template/sample_topic.html the first .topic-block (reference markup)

Prints shell_head / shell_tail with the <style> and <script> bodies elided so
the structural markup can be reviewed cheaply.

Usage: python extract_template.py <reference-part.html> [outdir]
"""
import io, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OPEN = '<div class="topic-block"'


def split_blocks(h):
    """Return (head, [blocks], tail) using brace-free div depth counting."""
    starts = [m.start() for m in re.finditer(re.escape(OPEN), h)]
    if not starts:
        raise SystemExit('No .topic-block found in reference file.')
    blocks = []
    for s in starts:
        depth = 0
        i = s
        while True:
            m = re.compile(r'<div\b|</div>').search(h, i)
            if not m:
                raise SystemExit('Unbalanced div while scanning topic block.')
            if m.group(0) == '</div>':
                depth -= 1
                if depth == 0:
                    blocks.append((s, m.end()))
                    break
            else:
                depth += 1
            i = m.end()
    head = h[:blocks[0][0]]
    tail = h[blocks[-1][1]:]
    return head, [h[a:b] for a, b in blocks], tail


def elide(s):
    s = re.sub(r'(<style[^>]*>)(.*?)(</style>)',
               lambda m: m.group(1) + '\n/* [[CSS %d chars — carried verbatim]] */\n' % len(m.group(2)) + m.group(3),
               s, flags=re.S)
    s = re.sub(r'(<script(?![^>]*src)[^>]*>)(.{400,}?)(</script>)',
               lambda m: m.group(1) + '\n/* [[JS %d chars — carried verbatim]] */\n' % len(m.group(2)) + m.group(3),
               s, flags=re.S)
    return s


def main():
    ref = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')
    os.makedirs(outdir, exist_ok=True)
    h = open(ref, encoding='utf-8').read()
    head, blocks, tail = split_blocks(h)
    open(os.path.join(outdir, 'shell_head.html'), 'w', encoding='utf-8').write(head)
    open(os.path.join(outdir, 'shell_tail.html'), 'w', encoding='utf-8').write(tail)
    open(os.path.join(outdir, 'sample_topic.html'), 'w', encoding='utf-8').write(blocks[0])
    print('REFERENCE :', os.path.basename(ref))
    print('BLOCKS    :', len(blocks), '| head', len(head), 'ch | tail', len(tail), 'ch')
    print('=' * 70)
    print('--- SHELL HEAD (elided) ---')
    print(elide(head))
    print('=' * 70)
    print('--- SHELL TAIL (elided) ---')
    print(elide(tail))


if __name__ == '__main__':
    main()
