import json
d=json.load(open('/tmp/claude-0/s130/mk/m16/scratch/series.json'))
s=[int(round(v*10)) for v in d['series']]
data=json.dumps(s,separators=(',',':'))
html=open('/tmp/claude-0/s130/mk/m16/scratch/template.html').read().replace('__DATA__',data)
open('/tmp/claude-0/s130/mk/m16/work/index.html','w').write(html)
print(len(html))
