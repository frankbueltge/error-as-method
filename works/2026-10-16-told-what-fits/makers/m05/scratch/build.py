import json
d=json.load(open('days.json'))
data=json.dumps({'stats':d['stats'],'prof':[[round(v,2) for v in p] for p in d['prof']]},separators=(',',':'))
html=open('template.html').read().replace('__DATA__',data)
open('/tmp/claude-0/s131/mk/m05/work/index.html','w').write(html)
print(len(html))
