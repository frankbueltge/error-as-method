from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m05/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
d=[[max(0,255-p[x,y])/255 for x in range(W)] for y in range(H)]
P=4.82; x0=3.9; floor=83.5
# day k: from night centre x0+P*k-? Determine day windows centred on gap centres: x0+P*(k+0.5)
tot_ink=sum(map(sum,d)); print('total ink',tot_ink,'per dot',tot_ink/1464)
out=[]
for k in range(-1,62):
    c=x0+P*(k+0.5)
    lo=c-P/2; hi=c+P/2
    if hi<0 or lo>W: continue
    fl=0;en=0;top=None;ink=0
    for x in range(W):
        w=max(0,min(x+1,hi)-max(x,lo))
        if w<=0: continue
        for y in range(H):
            v=d[y][x]*w
            ink+=v
            if y>=81: fl+=v
            else: en+=v*(floor-y)
            if d[y][x]>0.35 and y<81 and (top is None or y<top): top=y
    out.append((k,round(c,1),round(fl,1),round(ink,1),round(en/ (tot_ink/1464)),top))
for o in out: print(o)
