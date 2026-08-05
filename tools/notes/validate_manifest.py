import json
d = json.load(open(r'F:\marine-intelligence-weekly\meoclass1\oralnotes\notes_content_index.json', encoding='utf-8'))
print('VALID JSON')
print('total_files:', d['total_files'])
print('mgmt files count:', len(d['series']['engineering-management-notes']['files']))
print('has p19-p22:', all('miw-notes-mgmt-p%d.html' % n in d['series']['engineering-management-notes']['files'] for n in (19,20,21,22)))
