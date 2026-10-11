import json
r=json.load(open('rows.json'))
enc=','.join(''.join('0123456789abcdefghijklmnopqrstuvwxyz'[c] for c in row).rstrip('0') for row in r['rows'])
html=open('template.html').read().replace('__ROWS__',enc).replace('__LO__',str(r['lo']))
open('/tmp/claude-0/s121/mk/m03/work/index.html','w').write(html)
print(len(html))
