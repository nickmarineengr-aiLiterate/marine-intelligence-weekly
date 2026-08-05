import io, json, os, re
ROOT = r'F:\marine-intelligence-weekly'
OUT = open(os.path.join(ROOT, 'tools', 'notes', '_qb_matches.txt'), 'w', encoding='utf-8', newline='\n')
def print(*a, **k):
    k['file'] = OUT
    __import__('builtins').print(*a, **k)

d = json.load(open(os.path.join(ROOT, 'meoclass1', 'qb_content_index.json'), encoding='utf-8'))
files = d['files']

# flatten each QB file into a searchable blob: title + tags + all question texts
blobs = {}
for fname, meta in files.items():
    parts = [meta.get('title', '')] + meta.get('tags', []) + [q['text'] for q in meta.get('questions', [])]
    blobs[fname] = (' '.join(parts)).lower()

specs_dir = os.path.join(ROOT, 'tools', 'notes', 'specs')
for pn in (19, 20, 21, 22):
    spec = json.load(open(os.path.join(specs_dir, 'p%d.json' % pn), encoding='utf-8'))
    for t in spec['topics']:
        kws = [k.strip().lower() for k in t.get('kw', '').split(',') if k.strip()]
        # keep distinctive (multi-word or long) terms only
        sig = [k for k in kws if len(k.split()) >= 2 or len(k) > 7]
        hits = {}
        for fname, blob in blobs.items():
            matched = [k for k in sig if k in blob]
            if matched:
                hits[fname] = matched
        print('Part %d T%d - %s' % (pn, t['n'], t['title']))
        if hits:
            for fname, matched in sorted(hits.items(), key=lambda kv: -len(kv[1])):
                print('   %-16s %s  <- %s' % (fname, files[fname]['title'], ', '.join(matched)))
        else:
            print('   (no QB file matches)')
        print()
