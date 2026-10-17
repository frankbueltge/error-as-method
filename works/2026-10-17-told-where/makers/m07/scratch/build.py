import json
days=json.load(open('days.json'))
prof=[[round(v,2) for v in d['p'][:82]] for d in days]
floor=[d['f'] for d in days]
data=json.dumps({'p':prof,'f':floor},separators=(',',':'))
html=open('template.html').read().replace('/*DATA*/null',data)
open('/tmp/claude-0/s133/mk/m07/work/index.html','w').write(html)
