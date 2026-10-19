import json
v=json.load(open('series.json'))
# day 0 first hours: leading columns were empty and borrowed from neighbours; keep as is
data=','.join('%d'%round(a) for a in v)
html=open('template.html').read().replace('/*DATA*/',data)
open('/tmp/claude-0/s137/mk/m12/work/index.html','w').write(html)
print(len(html))
