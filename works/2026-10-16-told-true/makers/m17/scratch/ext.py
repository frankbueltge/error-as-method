from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s130/mk/m17/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
ink=[[max(0,(235-px[x,y]))/235 for y in range(H)] for x in range(W)]
cols=[]
for x in range(W):
    s=sum(ink[x]); m=sum(y*ink[x][y] for y in range(H))/s if s>0 else None
    cols.append((s,m))
print('ink sum range',min(c[0] for c in cols),max(c[0] for c in cols))
# total ink -> ink per dot
tot=sum(c[0] for c in cols); print('total ink',tot,'per value',tot/1464)
# fold by phase
bins=[[] for _ in range(24)]
for x,(s,m) in enumerate(cols):
    t=(x+0.5)*1464/300
    bins[int(t%24)].append(m)
for h,b in enumerate(bins): print(h,len(b),round(sum(b)/len(b),2))
# test other periods
def amp(P):
    import cmath
    z=sum(cmath.exp(2j*math.pi*((x+0.5)*4.88)/P)*(m-60) for x,(s,m) in enumerate(cols))
    return abs(z)/W
for P in [6,8,10,12,16,20,22,23,24,25,26,30,36,48,72,100,168]:
    print(P,round(amp(P),3))
json.dump([[ink[x][y] for y in range(H)] for x in range(W)],open('ink.json','w'))
