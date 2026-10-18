import json
d=json.load(open('data.json'))
blobs=[[b[0],b[1],b[2],b[3]] for b in d['blobs']]
data=json.dumps({'b':blobs,'z':d['band']},separators=(',',':'))
html=open('template.html').read().replace('/*DATA*/null',data)
open('/tmp/claude-0/s133/mk/m03/work/index.html','w').write(html)
print(len(html))
