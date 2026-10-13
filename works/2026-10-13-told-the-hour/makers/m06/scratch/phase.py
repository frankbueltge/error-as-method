import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; p=im.load()
x0=3; pw=294/1464
bins={}
for x in range(3,297):
    h=(x+0.5-x0)/pw; d=int(h//24); ph=int((h%24)//4.8)
    if d%7 in (0,1): continue
    for y in range(H):
        if p[x,y]<140: bins.setdefault(ph,[]).append(y)
for k in sorted(bins):
    v=sorted(bins[k]); print(k, len(v), 'mean',round(sum(v)/len(v),1),'p10',v[len(v)//10],'p90',v[9*len(v)//10])
