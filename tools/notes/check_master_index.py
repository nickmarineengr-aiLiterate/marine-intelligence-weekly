import io
import os
import sys
from html.parser import HTMLParser

# FUP-E. These paths were hard-coded to the canonical checkout, so the tool read
# and WROTE there whatever root it was invoked from. That is the same defect that
# made audit_overlap.py escape into a Controller PROTECTED ROOT during job
# AC-000021; this script simply had not been run inside a governed job yet. The
# root now comes from the tool's own location, per miw_paths.py's convention.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from miw_paths import REPO_ROOT  # noqa: E402

INDEX = os.path.join(REPO_ROOT, 'meoclass1', 'oralnotes', 'notes-master-index.html')
REPORT = os.path.join(REPO_ROOT, 'tools', 'notes', '_master_index_balance.txt')
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class B(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.errors=[]
    def handle_starttag(self, tag, attrs):
        if tag not in VOID: self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack:
            self.errors.append('stray </%s> at %s' % (tag, self.getpos())); return
        t,p = self.stack.pop()
        if t != tag:
            self.errors.append('mismatch <%s> line %s closed by </%s> line %s' % (t,p,tag,self.getpos()))

h = open(INDEX, encoding='utf-8').read()
b = B(); b.feed(h)
OUT = open(REPORT, 'w', encoding='utf-8')
print('errors:', b.errors[:30], file=OUT)
print('unclosed at EOF:', b.stack[-10:], file=OUT)
print('total length:', len(h), file=OUT)
print('note-row count:', h.count('class="note-row'), file=OUT)
print('row-matched count:', h.count('note-row row-matched'), file=OUT)
print('row-gap count:', h.count('note-row row-gap'), file=OUT)
print('part-section count:', h.count('class="part-section"'), file=OUT)
OUT.close()
