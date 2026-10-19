from PIL import Image
import json
im=Image.open('/tmp/claude-0/s137/mk/m18/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
D=61; w=W/D
prof=[]
for d in range(D):
    a,b=d*w,(d+1)*w
    p=[0.0]*H
    for x in range(int(a),min(W,int(b)+1)):
        ov=max(0,min(b,x+1)-max(a,x))
        if ov<=0: continue
        for y in range(H):
            v=max(0,(225-px[x,y])/225)
            p[y]+=v*ov
    prof.append(p)
# summary: per day, ink-weighted mean y and extent of rows with ink>0.3
for d,p in enumerate(prof):
    rows=[y for y in range(H) if p[y]>0.35]
    tot=sum(p); m=sum(y*p[y] for y in range(H))/tot
    print(d+1, round(tot,1), round(m,1), (min(rows),max(rows)) if rows else None)
json.dump([[round(v,3) for v in p] for p in prof],open('prof.json','w'))
