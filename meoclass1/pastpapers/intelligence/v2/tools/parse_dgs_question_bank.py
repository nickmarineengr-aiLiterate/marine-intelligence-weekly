"""Parse the DG Shipping MEO CL-I question bank PDF using layout coordinates.

The PDF is a two-column table: Sr.No | Question. pdfminer's flat text extraction
interleaves the two columns whenever a question spans several lines, so the
numbers must be recovered from x/y geometry rather than reading order.

Reading order within a row
--------------------------
A cell may hold several text fragments that share one baseline. Item 182 is the
case in this document: three fragments sit at y=145.5 with x0 = 53.0 / 359.8 /
456.8, because the source lays the charter limbs out as inline columns. Ordering
body lines by (page, -y) alone leaves those three in pdfminer's container order,
which is not left-to-right, and the item reads as scrambled prose.

x0 is therefore part of the sort key. A whole-document scan finds exactly one
row where container order differs from left-to-right order among body text
(page 16, y=145.5 — item 182); the other same-baseline groups are a Sr.No cell
beside its first body line, which this parser separates before sorting.

Not every oddity is ours to fix. Item 181 prints its limbs lettered a, b, d, c
at descending y: that is the Directorate's own mislettering, the parser reads it
in the order printed, and it is preserved verbatim.
"""
import argparse, json, os, re, sys
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LAParams

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qi_paths

# The PDF binary is deliberately NOT committed: SOURCE_MANIFEST.json carries the
# retrieval recipe and sha256 that re-obtain and re-verify it on demand. Give
# --pdf the path to a re-obtained copy. The default output is the committed
# extract, so re-running this tool regenerates exactly what the repo carries.
_ap = argparse.ArgumentParser(description=__doc__)
_ap.add_argument('--pdf', required=True,
                 help='path to a re-obtained dgs_meo_cl1_written_questions.pdf')
_ap.add_argument('--out', default=qi_paths.EXTRACTED_BANK,
                 help='where to write the extract (default: the committed one)')
_args = _ap.parse_args()
PDF = _args.pdf
OUT = _args.out

lines = []  # (page, y_top, x0, text)
for pno, page in enumerate(extract_pages(PDF, laparams=LAParams(line_margin=0.3))):
    for el in page:
        if not isinstance(el, LTTextContainer):
            continue
        for ln in el:
            txt = ''.join(c.get_text() for c in ln if hasattr(c, 'get_text')) if hasattr(ln, '__iter__') else ln.get_text()
            txt = txt.rstrip('\n')
            if not txt.strip():
                continue
            lines.append((pno, round(ln.y1, 1), round(ln.x0, 1), txt))

# figure out the x threshold: number cells sit far left
xs = sorted({x for _, _, x, _ in lines})
num_x = xs[0]
body_x = None
for x in xs:
    if x > num_x + 5:
        body_x = x
        break
print('num column x=%s  first body x=%s  (all x starts: %s)' % (num_x, body_x, xs[:12]), file=sys.stderr)

# a "number cell" is a line in the left column that is purely an integer
num_cells = []   # (page, y, n)
body_lines = []  # (page, y, x, text)
for pno, y, x, txt in lines:
    s = txt.strip()
    if x <= num_x + 4 and re.fullmatch(r'\d{1,3}', s):
        num_cells.append((pno, y, int(s)))
    else:
        # strip a leading number that pdfminer glued onto the body
        m = re.match(r'^\s*(\d{1,3})\s+(?=[A-Z\u201c(])', txt)
        if x <= num_x + 4 and m:
            num_cells.append((pno, y, int(m.group(1))))
            body_lines.append((pno, y, x, txt[m.end():]))
        else:
            body_lines.append((pno, y, x, txt))

# Some rows have the Sr.No glued to the first body line ("1 During bunkering...").
# Recover those by scanning body lines in reading order and accepting a leading
# integer only when it continues the ascending item sequence.
num_cells.sort(key=lambda t: (t[0], -t[1]))
# x0 is load-bearing: fragments sharing a baseline must read left-to-right.
body_lines.sort(key=lambda t: (t[0], -t[1], t[2]))

known = sorted({n for _, _, n in num_cells})
seen = set(known)
recovered, kept = [], []
last = 0
for pno, y, x, txt in body_lines:
    m = re.match(r'^\s*(\d{1,3})\s+(?=[A-Z“(])', txt)
    if m:
        n = int(m.group(1))
        if n not in seen and last < n <= last + 3:
            recovered.append((pno, y, n))
            seen.add(n)
            kept.append((pno, y, x, txt[m.end():]))
            last = n
            continue
    kept.append((pno, y, x, txt))
    # track sequence position from the geometric number cells too
    while True:
        nxt = [n for n in known if n > last]
        if nxt and nxt[0] <= last + 1:
            last = nxt[0]
        else:
            break
    for p2, y2, n2 in num_cells:
        if (p2, -y2) <= (pno, -y) and n2 > last:
            last = n2

if recovered:
    print('recovered %d glued numbers: %s' % (len(recovered), sorted(n for _, _, n in recovered)), file=sys.stderr)
num_cells = sorted(num_cells + recovered, key=lambda t: (t[0], -t[1]))
body_lines = kept
print('number cells found: %d  (min %d max %d)' % (
    len(num_cells), min(n for _, _, n in num_cells), max(n for _, _, n in num_cells)), file=sys.stderr)

# assign each body line to the last number cell at or above it on the same page,
# carrying the current number across page breaks
items = {}
cur = None
ni = 0
for pno, y, x, txt in body_lines:
    while ni < len(num_cells) and (num_cells[ni][0], -num_cells[ni][1]) <= (pno, -y):
        cur = num_cells[ni][2]
        ni += 1
    if cur is None:
        continue
    items.setdefault(cur, []).append(txt.strip())

items = {n: re.sub(r'\s+', ' ', ' '.join(v)).strip() for n, v in items.items()}
items = {n: t for n, t in items.items() if t and not t.startswith('Question Bank')}

# Post-split: a row whose Sr.No cell landed in the body column leaves the next
# item's number embedded mid-text ("...same. 122 a) What are..."). Split only on a
# number that is exactly the one missing from the sequence, so no legitimate
# numeral inside a question can be mistaken for an item boundary.
for _ in range(6):
    nums = sorted(items)
    gaps = [i for i in range(nums[0], nums[-1] + 1) if i not in items]
    if not gaps:
        break
    progressed = False
    for g in gaps:
        host = max((n for n in items if n < g), default=None)
        if host is None:
            continue
        m = re.search(r'\s%d\s+(?=[a-eiA-Z“(])' % g, items[host])
        if m:
            items[host], items[g] = items[host][:m.start()].strip(), items[host][m.end():].strip()
            progressed = True
    if not progressed:
        break

nums = sorted(items)
print('items: %d  range %d-%d  gaps: %s' % (
    len(items), nums[0], nums[-1], [i for i in range(nums[0], nums[-1] + 1) if i not in items]), file=sys.stderr)

json.dump({'source': 'DG Shipping Question Bank MEO CL-I (archived)',
           'item_count': len(items),
           'items': {str(k): items[k] for k in nums}},
          open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote', OUT, file=sys.stderr)

for n in nums[:6]:
    print('%3d | %s' % (n, items[n][:180]))
print('...')
for n in [15, 18, 54, 72, 85]:
    if n in items:
        print('%3d | %s' % (n, items[n][:400]))
