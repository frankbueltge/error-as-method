import json
dots=json.load(open('/tmp/claude-0/s133/mk/m16/scratch/dots.json'))
flat=[]
for k,h,v,w in dots:
    k=max(0,min(60,k))
    flat += [k, h, v]
data=json.dumps(flat,separators=(',',':'))
tpl=open('/tmp/claude-0/s133/mk/m16/scratch/template.html').read()
open('/tmp/claude-0/s133/mk/m16/work/index.html','w').write(tpl.replace('/*DATA*/[]',data))
print(len(data))
