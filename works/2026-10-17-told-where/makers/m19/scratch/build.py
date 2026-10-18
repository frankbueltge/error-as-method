import json
d=json.load(open('cols.json'))
mean=[0 if v is None else v for v in d['mean']]
mx=[0 if v is None else v for v in d['max']]
tpl=open('template.html').read()
html=tpl.replace('__MEAN__',json.dumps(mean)).replace('__MAX__',json.dumps(mx))
open('/tmp/claude-0/s133/mk/m19/work/index.html','w').write(html)
print(len(html))
