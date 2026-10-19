from PIL import Image
import json
g=Image.open('/tmp/claude-0/s137/mk/m08/work/record.jpg').convert('L'); px=g.load()
W,H=g.size
ink=[[max(0,230-px[x,y])/230 for y in range(H)] for x in range(W)]
xa,xb=2.0,298.0; nd=61; w=(xb-xa)/nd
days=[]
for d in range(nd):
    a=xa+d*w; b=a+w
    prof=[0.0]*H
    for x in range(W):
        ov=max(0,min(b,x+1)-max(a,x))
        if ov<=0: continue
        for y in range(H): prof[y]+=ov*ink[x][y]
    days.append([round(v*100) for v in prof])
cols=[[round(ink[x][y]*99) for y in range(H)] for x in range(W)]
json.dump({'days':days,'cols':cols},open('data.json','w'),separators=(',',':'))
for d,p in enumerate(days):
    nz=[y for y,v in enumerate(p) if v>40]
    print(d, nz[0] if nz else None, nz[-1] if nz else None, sum(p))
