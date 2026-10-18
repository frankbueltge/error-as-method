from PIL import Image
import json,sys
im=Image.open(sys.argv[1]).convert('L'); p=im.load()
W,H=im.size
Y=[5.5+k*(78/17) for k in range(18)]
cols=[]
for x in range(W):
    lit=[]
    for k,yc in enumerate(Y):
        ys=[int(yc-0.5),int(yc+0.5)]
        d=max(255-p[x,y] for y in range(max(0,int(yc)-1),min(H,int(yc)+2)))
        if d>90: lit.append(17-k)   # value index: 0 lowest .. 17 highest
    cols.append(lit)
json.dump(cols,open('cols.json','w'))
# per day
pd=W/61
out=[]
for d in range(61):
    xs=range(round(d*pd),round((d+1)*pd))
    vals=[v for x in xs for v in cols[x]]
    hi=max(vals);lo=min(vals)
    # phase of hi/lo
    xhi=[x-d*pd for x in xs if hi in cols[x]]
    xlo=[x-d*pd for x in xs if lo in cols[x]]
    out.append((d,lo,hi,round(sum(xhi)/len(xhi)/pd*24,1),round(sum(xlo)/len(xlo)/pd*24,1)))
for o in out: print(*o)
json.dump(out,open('days.json','w'))
