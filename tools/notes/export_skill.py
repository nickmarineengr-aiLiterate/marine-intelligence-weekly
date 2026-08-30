import io, sys, os, shutil, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# FUP-E. This was a hard-coded canonical path, and this script WRITES A TRACKED
# FILE (docs/miw-notes-mgmt_SKILL.md), so running it from any other checkout
# would have written into the canonical repository -- a Controller PROTECTED
# ROOT during a governed job. Same defect class as audit_overlap.py, which did
# escape in AC-000021 cycle 0. The root now comes from this file's own location.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from miw_paths import REPO_ROOT  # noqa: E402

R = REPO_ROOT
src = os.path.join(R, 'tools', 'notes', 'SKILL.md')
dst = os.path.join(R, 'docs', 'miw-notes-mgmt_SKILL.md')

banner = (
    "<!-- GENERATED EXPORT — DO NOT HAND-EDIT.\n"
    "     Authoritative source: tools/notes/SKILL.md\n"
    "     Re-export with: python tools/notes/export_skill.py\n"
    "     This copy exists only to be uploaded to Claude Project Knowledge.\n"
    "     Last export: 2026-08-06 -->\n\n"
)
body = open(src, encoding='utf-8').read()
with open(dst, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(banner + body)

for label, p in (('source', src), ('export', dst)):
    b = open(p, 'rb').read()
    print('%-7s %7d B md5=%s has_8a=%s' % (
        label, len(b), hashlib.md5(b).hexdigest()[:12],
        '8a. Manifest authority' in b.decode('utf-8', 'ignore')))
