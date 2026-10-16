import json
dots=json.load(open('dots.json'))
X0,SPAN=2.8,293.7
out=[]
for x,y,b in dots:
    t=(x-X0)/SPAN*1463
    out.append([round(t,1),round(90-y,1),b])
out.sort()
flat=[]
for t,v,b in out: flat+= [t,v,b]
open('data.js','w').write('const D=['+','.join(str(z) for z in flat)+'];')
print(len(out), min(o[1] for o in out), max(o[1] for o in out), min(o[0] for o in out), max(o[0] for o in out))
